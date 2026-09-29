"""Refresh the dashboard data from the server, on command (the Refresh data button).

Two sources, both read only:
  Meta ads   Meta Marketing API with a read-only token (ads_read, read_insights). HTTP GET only.
             The last 7 days are pulled again (Meta keeps adding late purchases), plus this
             month's age, gender and platform rows and the video rows. New ads get their ad and
             creative details. Then the gallery cache is rebuilt.
  Metabase   Metabase API key. Only dashboard card queries (a POST that runs a saved question,
             nothing is saved). Website sales for the whole current month, checked against
             Metabase's own month totals, and 12 weeks of Google Analytics traffic.

Secrets come from the environment (Render) or .env: META_ACCESS_TOKEN, META_AD_ACCOUNT_ID,
METABASE_URL, METABASE_API_KEY. They are never written to a file, a log line or a response.

On a host with a persistent disk, set REFRESH_STORE (start.sh does). Fresh files are copied
there, and restore() puts back whichever copy holds newer data after a redeploy.
"""
import datetime as dt
import json
import os
import re
import shutil
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from . import refresh as rf
from .graph_client import Graph, action, by_ids, creative_record, load_env
from .snapshot import DATA, ROOT, build

IST = dt.timezone(dt.timedelta(hours=5, minutes=30))
COOLDOWN_MIN = 30
CACHE = DATA / 'cache' / 'gallery.json'
SALES = DATA / 'sales.json'
TRAFFIC = DATA / 'traffic.json'
RAW = DATA / 'raw'
SECRET_KEYS = ('META_ACCESS_TOKEN', 'METABASE_API_KEY', 'METABASE_PASSWORD', 'METABASE_SESSION')
ENV_KEYS = ('META_ACCESS_TOKEN', 'META_AD_ACCOUNT_ID', 'METABASE_URL', 'METABASE_API_KEY', 'METABASE_USER', 'METABASE_PASSWORD', 'METABASE_SESSION')

_lock = threading.Lock()
_state = {'running': False, 'step': '', 'steps': [], 'started_at': None, 'by': None}


# ---------- settings ----------

def _env():
    env = dict(load_env(ROOT / '.env'))
    for k in ENV_KEYS:
        if os.environ.get(k):
            env[k] = os.environ[k]
    return {k: (v or '').strip() for k, v in env.items()}


def configured():
    e = _env()
    return {'meta': bool(e.get('META_ACCESS_TOKEN') and e.get('META_AD_ACCOUNT_ID')),
            'metabase': bool(e.get('METABASE_API_KEY') or e.get('METABASE_SESSION') or (e.get('METABASE_USER') and e.get('METABASE_PASSWORD')))}


def cooldown_min():
    # One person on a laptop can refresh any time; the shared team app waits 30 minutes between refreshes.
    return COOLDOWN_MIN if os.environ.get('TEAM_MODE') == '1' else 0


def scrub(text):
    text = str(text)
    e = _env()
    for k in SECRET_KEYS:
        if e.get(k):
            text = text.replace(e[k], '[hidden]')
    text = re.sub(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', '[hidden]', text)
    return re.sub(r'[A-Za-z0-9_\-]{40,}', '[hidden]', text)


def _store():
    p = os.environ.get('REFRESH_STORE')
    return Path(p) if p else None


def _state_file():
    d = Path(os.environ.get('TEAM_STATE') or DATA / 'team')
    d.mkdir(parents=True, exist_ok=True)
    return d / 'refresh.json'


def _last():
    try:
        return json.loads(_state_file().read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return {}


def _save_last(obj):
    p = _state_file()
    tmp = p.with_suffix('.tmp')
    tmp.write_text(json.dumps(obj, indent=1), encoding='utf-8')
    tmp.replace(p)


# ---------- data dates ----------

def _json(path):
    try:
        return json.loads(Path(path).read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return None


def data_dates():
    g, s, t = _json(CACHE) or {}, _json(SALES) or {}, _json(TRAFFIC) or {}
    return {'ads': (g.get('meta') or {}).get('window', {}).get('until'),
            'sales': max(s.get('daily') or {'': 0}) or None,
            'traffic': ((t.get('weeks') or [{}])[0]).get('until')}


def status():
    with _lock:
        st = dict(_state, steps=list(_state['steps']))
    last = _last()
    nxt = None
    if last.get('started_at'):
        nxt = (dt.datetime.fromisoformat(last['started_at']) + dt.timedelta(minutes=cooldown_min())).isoformat(timespec='seconds')
    return {**st, 'configured': configured(), 'dates': data_dates(), 'last': last.get('result'),
            'next_allowed_at': nxt, 'cooldown_min': cooldown_min()}


def start(who):
    cfg = configured()
    if not (cfg['meta'] or cfg['metabase']):
        raise ValueError('Refresh is not set up on the server yet (no Meta token or Metabase key).')
    now = dt.datetime.now(IST)
    with _lock:
        if _state['running']:
            raise ValueError(f"A refresh is already running (started by {_state['by']}).")
        last = _last()
        if last.get('started_at'):
            began = dt.datetime.fromisoformat(last['started_at'])
            ready = began + dt.timedelta(minutes=cooldown_min())
            if now < ready:
                raise ValueError(f"Data was refreshed at {began.strftime('%H:%M')}. Next refresh after {ready.strftime('%H:%M')}.")
        _state.update(running=True, step='Starting', steps=[], started_at=now.isoformat(timespec='seconds'), by=who)
        _save_last({**last, 'started_at': now.isoformat(timespec='seconds')})
    threading.Thread(target=run, args=(who,), daemon=True).start()
    return status()


def _step(text, ok=None):
    with _lock:
        _state['step'] = scrub(text)
        if ok is not None:
            _state['steps'].append({'text': scrub(text), 'ok': ok})


def run(who, today=None):
    today = today or dt.datetime.now(IST).date()
    until = today - dt.timedelta(days=1)
    since = until - dt.timedelta(days=6)
    cfg = configured()
    parts = {}
    try:
        jobs = []
        if cfg['meta']:
            jobs.append(('meta', 'Meta ads', lambda: meta_refresh(since, until)))
        if cfg['metabase']:
            jobs.append(('sales', 'Website sales', lambda: sales_refresh(since, until)))
            jobs.append(('traffic', 'Traffic', lambda: traffic_refresh(until)))
        for key, label, fn in jobs:
            try:
                _step(f'{label}: starting')
                parts[key] = fn()
                _step(f"{label} updated to {until.strftime('%d %b')}", True)
            except Exception as e:  # one source failing does not stop the others
                parts[key] = {'error': scrub(e)}
                _step(f'{label} failed: {scrub(e)}', False)
        persist()
    finally:
        ok = bool(parts) and all('error' not in p for p in parts.values())
        result = {'at': dt.datetime.now(IST).isoformat(timespec='seconds'), 'by': who, 'ok': ok,
                  'parts': parts, 'dates': data_dates()}
        _save_last({**_last(), 'result': result})
        with _lock:
            _state.update(running=False, step='Done' if ok else 'Finished with errors')
    return result


# ---------- Meta (Graph API, GET only) ----------

def _graph():
    e = _env()
    return Graph(e['META_ACCESS_TOKEN'], e['META_AD_ACCOUNT_ID'])


def _money(v):
    return {'value': str(v), 'unit': 'INR'} if v not in (None, '') else None


def _first(lst):
    return (lst or [{}])[0].get('value') if isinstance(lst, list) else lst


def mcp_row(r, extra=()):
    """A Graph insights row in the field names the capture uses (same as the Meta MCP rows)."""
    out = {'date_start': r.get('date_start'), 'date_stop': r.get('date_stop'),
           'amount_spent': _money(r.get('spend')),
           'omni_purchase': action(r.get('actions'), 'omni_purchase'),
           'omni_purchase_values': _money(action(r.get('action_values'), 'omni_purchase')),
           'impressions': r.get('impressions'), 'link_click': action(r.get('actions'), 'link_click'),
           'id': r.get('ad_id'), 'name': r.get('ad_name')}
    for k in extra:
        out[k] = r.get(k)
    return out


VIDEO_FIELDS = ('video_play_actions', 'video_thruplay_watched_actions', 'video_p25_watched_actions', 'video_p50_watched_actions',
                'video_p75_watched_actions', 'video_p100_watched_actions', 'video_avg_time_watched_actions')


def video_row(r):
    spend = float(r.get('spend') or 0)
    views = action(r.get('actions'), 'video_view')
    out = {'date_start': r.get('date_start'), 'date_stop': r.get('date_stop'), 'amount_spent': _money(r.get('spend')),
           'impressions': r.get('impressions'),
           'cost_per_video_view': _money(round(spend / float(views), 2)) if views and float(views) > 0 else None}
    for k in VIDEO_FIELDS:
        out[k] = _first(r.get(k))
    for k in ('reach', 'frequency', 'cpm', 'ctr', 'clicks'):
        out[k] = r.get(k)
    out.update(id=r.get('ad_id'), name=r.get('ad_name'))
    return out


def newest_capture_file():
    best = None
    for f in RAW.glob('*.json'):
        try:
            with f.open(encoding='utf-8') as fh:
                head = fh.read(400)
        except OSError:
            continue
        if '"version": 2' not in head and '"version":2' not in head:
            continue
        cap = _json(f) or {}
        key = ((cap.get('window') or {}).get('until') or '', cap.get('captured_at') or '')
        if best is None or key > best[0]:
            best = (key, f)
    if not best:
        raise RuntimeError('No version 2 capture found to build on.')
    return best[1]


def _attribution(spec):
    return '_'.join(f"{x.get('window_days')}d_{x.get('event_type', '').lower().replace('click_through', 'click').replace('view_through', 'view').replace('engaged_video_view', 'ev')}"
                    for x in spec or []) or None


def _add_new_ads(g, cap, new_ids):
    got = by_ids(g, new_ids, 'id,name,effective_status,status,campaign_id,adset_id,creative{id},campaign{name},adset{name}')
    for aid in new_ids:
        a = got.get(aid) or {}
        cap['ads'].append({'id': aid, 'name': a.get('name'), 'effective_status': a.get('effective_status'), 'status': a.get('status'),
                           'campaign_id': a.get('campaign_id'), 'adset_id': a.get('adset_id'),
                           'creative_id': (a.get('creative') or {}).get('id'),
                           'campaign_name': (a.get('campaign') or {}).get('name'), 'adset_name': (a.get('adset') or {}).get('name'),
                           'amount_spent': None, 'omni_purchase': None, 'omni_purchase_values': None, 'impressions': None, 'link_click': None})
    new = [a for a in cap['ads'] if a['id'] in set(new_ids)]
    cids = {a['creative_id'] for a in new if a.get('creative_id')} - {c['id'] for c in cap['creatives']}
    if cids:
        cf = ('id,name,object_type,body,title,call_to_action_type,image_hash,image_url,thumbnail_url,video_id,'
              'product_set_id,effective_object_story_id,effective_instagram_media_id,link_url,object_story_spec,asset_feed_spec')
        fresh = []
        for c in by_ids(g, cids, cf).values():
            rec = creative_record(c)
            if c.get('effective_instagram_media_id'):
                rec['effective_instagram_media_id'] = c['effective_instagram_media_id']
            fresh.append({k: v for k, v in rec.items() if v is not None})
        cap['creatives'] += fresh
        vids = {c['video_id'] for c in fresh if c.get('video_id')} - {v['id'] for v in cap.get('videos', [])}
        if vids:
            cap.setdefault('videos', []).extend(dict(v, id=k) for k, v in by_ids(g, vids, 'id,title,length,permalink_url,picture').items())
        hashes = sorted({x.get('image_hash') for c in fresh for x in (c.get('child_attachments') or []) if x.get('image_hash')}
                        - {i['hash'] for i in cap.get('images', [])})
        for i in range(0, len(hashes), 50):
            cap.setdefault('images', []).extend(
                g.get(f'{g.account}/adimages', hashes=json.dumps(hashes[i:i + 50]), fields='hash,url,width,height').get('data', []))
    sids = {a['adset_id'] for a in new if a.get('adset_id')} - {s['id'] for s in cap.get('adsets', [])}
    if sids:
        for sid, s in by_ids(g, sids, 'id,name,is_dynamic_creative,attribution_spec').items():
            cap.setdefault('adsets', []).append({'id': sid, 'is_dynamic_creative': s.get('is_dynamic_creative'), 'name': s.get('name'),
                                                 'attribution_setting': _attribution(s.get('attribution_spec'))})


def _months(since, until):
    out, d = [], since.replace(day=1)
    while d <= until:
        nxt = (d.replace(day=28) + dt.timedelta(days=4)).replace(day=1)
        out.append((d, min(until, nxt - dt.timedelta(days=1))))
        d = nxt
    return out


def _replace(tmp, path):
    # Windows refuses to replace a file while another program has it open for a moment
    # (the dashboard reading it, antivirus, a sync tool). Try again, then copy over it.
    for i in range(10):
        try:
            tmp.replace(path)
            return
        except PermissionError:
            time.sleep(0.3 * (i + 1))
    shutil.copyfile(tmp, path)
    tmp.unlink(missing_ok=True)


def _write(path, obj, compact=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(obj, ensure_ascii=False, separators=(',', ':') if compact else None), encoding='utf-8')
    _replace(tmp, path)


def meta_refresh(since, until, graph=None):
    g = graph or _graph()
    cap = _json(newest_capture_file())
    flt = json.dumps([{'field': 'spend', 'operator': 'GREATER_THAN', 'value': 0}])

    def tr(a, b):
        return json.dumps({'since': a.isoformat(), 'until': b.isoformat()})
    _step('Meta ads: daily rows')
    daily = [mcp_row(r) for r in g.paged(f'{g.account}/insights', level='ad', time_range=tr(since, until), time_increment=1,
                                         fields='ad_id,ad_name,spend,impressions,actions,action_values', filtering=flt, limit=500)]
    new_ids = sorted({r['id'] for r in daily} - {a['id'] for a in cap['ads']})
    if new_ids:
        _step(f'Meta ads: adding {len(new_ids)} new ads')
        _add_new_ads(g, cap, new_ids)
    _step('Meta ads: age, gender and platform')
    breakdowns = {d: [] for d in rf.DIMS}
    for a, b in _months(since, until):
        for dim in rf.DIMS:
            rows = g.paged(f'{g.account}/insights', level='ad', time_range=tr(a, b), breakdowns=dim,
                           fields='ad_id,ad_name,spend,actions,action_values', filtering=flt, limit=500)
            breakdowns[dim] += [dict(mcp_row(r, extra=(dim,)), date_start=a.isoformat(), date_stop=b.isoformat()) for r in rows]
    _step('Meta ads: video')
    vfields = 'ad_id,ad_name,spend,impressions,reach,frequency,cpm,ctr,clicks,actions,' + ','.join(VIDEO_FIELDS)
    video = [video_row(r) for r in g.paged(f'{g.account}/insights', level='ad', time_range=tr(since, until), time_increment=1,
                                           fields=vfields, filtering=flt, limit=500) if r.get('video_play_actions')]
    tot = g.get(f'{g.account}/insights', time_range=tr(dt.date.fromisoformat(cap['window']['since']), until), fields='spend').get('data') or [{}]
    account_total = float(tot[0].get('spend') or 0) or None
    _step('Meta ads: rebuilding the dashboard')
    new, checks = rf.merge_meta(cap, since.isoformat(), until.isoformat(), daily, breakdowns, video, account_total)
    out = RAW / f"api_capture_{dt.datetime.now(IST).strftime('%Y-%m-%d_%H%M')}_1y.json"
    _write(out, new)
    _write(CACHE, build(new), compact=True)
    for f in sorted(RAW.glob('api_capture_*_1y.json'))[:-3]:  # keep the newest 3 server captures
        f.unlink(missing_ok=True)
    return {'new_ads': len(new_ids), 'rows': len(daily), 'spend_7d': checks['range_spend_after']}


# ---------- Metabase (API key, saved card queries only) ----------

class Metabase:
    """Signs in with an API key, or with your Metabase email and password (a session that lasts for this refresh)."""
    def __init__(self, base, key=None, user=None, password=None, session=None):
        self.base, self.key, self.user, self.password = base.rstrip('/'), key, user, password
        self.session = session or None  # a browser session id also works (Google sign in accounts)
        self._dash = {}
        self._dlock = threading.Lock()
        self._slock = threading.Lock()

    def _headers(self):
        h = {'Content-Type': 'application/json'}
        if self.key:
            h['x-api-key'] = self.key
            return h
        with self._slock:
            if not self.session:
                req = urllib.request.Request(self.base + '/api/session', method='POST', headers=h,
                                             data=json.dumps({'username': self.user, 'password': self.password}).encode())
                try:
                    with urllib.request.urlopen(req, timeout=60) as r:
                        self.session = json.loads(r.read().decode('utf-8'))['id']
                except urllib.error.HTTPError as e:
                    raise RuntimeError(f'Metabase sign in failed ({e.code}). Check METABASE_USER and METABASE_PASSWORD, '
                                       'or use METABASE_SESSION if you sign in with Google.') from None
                except Exception as e:
                    raise RuntimeError(scrub(f'Metabase could not be reached: {e}')) from None
        h['X-Metabase-Session'] = self.session
        return h

    def _call(self, path, body=None):
        req = urllib.request.Request(self.base + path, data=None if body is None else json.dumps(body).encode(),
                                     method='GET' if body is None else 'POST', headers=self._headers())
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            if e.code == 401 and not self.key:
                raise RuntimeError('Metabase said the sign in has ended (401). Update METABASE_SESSION or the password in .env.') from None
            raise RuntimeError(scrub(f'Metabase {e.code}: {e.read().decode("utf-8", "replace")[:300]}')) from None
        except Exception as e:
            raise RuntimeError(scrub(f'Metabase could not be reached: {e}')) from None

    def dash(self, n):
        with self._dlock:
            if n not in self._dash:
                self._dash[n] = self._call(f'/api/dashboard/{n}')
            return self._dash[n]

    def card(self, dash_id, dc_id, params):
        dc = next(c for c in self.dash(dash_id)['dashcards'] if c['id'] == dc_id)
        body = {'parameters': params(dc.get('parameter_mappings') or [])}
        j = self._call(f"/api/dashboard/{dash_id}/dashcard/{dc_id}/card/{dc['card_id']}/query", body)
        if j.get('error'):
            raise RuntimeError(scrub(f"card {dc_id}: {j['error']}"))
        return (j.get('data') or {}).get('rows') or []


# Same cards as meta_gallery/metabase_pull.js (dashboard card id -> what it holds).
SALES_DASH, RANGE_PARAM, TRAFFIC_CARD = 6, 'a82b2b5d', 766
SALES_CARDS = {'sales': 387, 'orders': 280, 'items': 281, 'ot': 289, 'refund': 386, 'retItems': 278, 'karat': 287,
               'typesG': 290, 'typesS': 284, 'bandsG': 297, 'bandsS': 296, 'pay': 294, 'skusG': 277, 'skusS': 292, 'retG': 285, 'retS': 283}


def _range_params(rng):
    def f(maps):
        m = next((p for p in maps if p.get('parameter_id') == RANGE_PARAM), None)
        return [{'id': RANGE_PARAM, 'type': 'date/range', 'value': rng, 'target': m['target']}] if m and rng else []
    return f


def _sales_entry(mb, rng, day_totals, pool):
    ids = list(SALES_CARDS)
    R = dict(zip(ids, pool.map(lambda k: mb.card(SALES_DASH, SALES_CARDS[k], _range_params(rng)), ids)))

    def first(rows, i, default):
        return rows[0][i] if rows and rows[0][i] is not None else default
    o = {}
    if day_totals:
        o['sales'] = R['sales'][0][0] if R['sales'] else None
        o['orders'] = first(R['orders'], 1, 0)
    o['items'] = first(R['items'], 0, 0)
    o['ot'] = {r[0]: [r[1], r[3]] for r in R['ot']}
    o['refund'] = R['refund'][0][0] if R['refund'] else None
    o['ret_items'] = first(R['retItems'], 0, 0)
    o['karat'] = [[r[1], r[0], r[2]] for r in R['karat']]
    o['types'] = [['g', r[1], r[0], r[3]] for r in R['typesG']] + [['s', r[1], r[0], r[3]] for r in R['typesS']]
    o['bands'] = [['g', r[0], r[1]] for r in R['bandsG']] + [['s', r[0], r[1]] for r in R['bandsS']]
    o['pay'] = [[r[0], r[1]] for r in R['pay']]
    o['ret'] = [[r[2], r[3], r[4], r[5]] for r in R['retG'] + R['retS']]
    o['skus'] = [['g', r[2], r[3], r[0], r[4]] for r in R['skusG']] + [['s', r[2], r[3], r[0], r[4]] for r in R['skusS']]
    return o


def _summary(m):
    def s(rows, i):
        return round(sum(r[i] for r in rows) * 100) / 100
    return {'counts': {'items': m['items'], 'ret_items': m['ret_items'], 'ot': {k: m['ot'][k][1] for k in sorted(m['ot'])},
                       'karat': s(m['karat'], 2), 'types': s(m['types'], 3), 'bands': s(m['bands'], 2), 'pay': s(m['pay'], 1),
                       'skus': s(m['skus'], 4)},
            'money': {'refund': m['refund'] or 0, 'ot': {k: round(m['ot'][k][0] * 100) / 100 for k in sorted(m['ot'])},
                      'karat': s(m['karat'], 1), 'types': s(m['types'], 2), 'skus': s(m['skus'], 3)}}


def _metabase():
    e = _env()
    return Metabase(e.get('METABASE_URL') or 'https://analyze.gehnaindia.com', e.get('METABASE_API_KEY'),
                    e.get('METABASE_USER'), e.get('METABASE_PASSWORD'), e.get('METABASE_SESSION'))


def metabase_pull(mb, since, until):
    """Same output as meta_gallery/metabase_pull.js."""
    out = {'source': 'Metabase dashboard 6, Online Website Sales Analytics (website orders only)',
           'pulled_at': dt.datetime.now(dt.timezone.utc).isoformat(), 'days': {}, 'month_totals': {}, 'ga': []}
    days = [since + dt.timedelta(days=i) for i in range((until - since).days + 1)]
    with ThreadPoolExecutor(max_workers=8) as pool:
        for i, d in enumerate(days, 1):
            _step(f'Website sales: day {i} of {len(days)}')
            out['days'][d.isoformat()] = _sales_entry(mb, f'{d}~{d}', True, pool)
        for a, b in _months(since, until):
            out['month_totals'][a.strftime('%Y-%m')] = _summary(_sales_entry(mb, f'{a}~{b}', False, pool))
    ga = mb.card(SALES_DASH, TRAFFIC_CARD, _range_params(None))
    out['ga'] = sorted([str(r[0])[:10], r[1], r[2], r[3], r[4]] for r in ga if since.isoformat() <= str(r[0])[:10] <= until.isoformat())
    return out


def sales_refresh(since, until, mb=None):
    mb = mb or _metabase()
    pull = metabase_pull(mb, since.replace(day=1), until)  # whole months, so late returns on earlier days are caught
    sales = _json(SALES)
    if not sales:
        raise RuntimeError('sales.json is missing.')
    new, report = rf.apply_sales(sales, pull)
    _write(SALES, new)
    return {'days_changed': len(report['days_changed']), 'months_checked': report['months_checked']}


GA_DASH, GA_FROM = 26, '8f0eb729'


def traffic_refresh(until, mb=None):
    mb = mb or _metabase()

    def params(a, b):
        return lambda maps: [{'id': m['parameter_id'], 'type': 'date/single', 'value': a if m['parameter_id'] == GA_FROM else b,
                              'target': m['target']} for m in maps]
    weeks = []
    for w in range(12):
        _step(f'Traffic: week {w + 1} of 12')
        b = until - dt.timedelta(days=7 * w)
        a = b - dt.timedelta(days=6)
        p = params(a.isoformat(), b.isoformat())
        land, conv, nr = mb.card(GA_DASH, 725, p), mb.card(GA_DASH, 731, p), mb.card(GA_DASH, 751, p)
        src = {}
        for r in land:
            src[r[0]] = src.get(r[0], 0) + r[2]
        weeks.append({'since': a.isoformat(), 'until': b.isoformat(), 'landings': src,
                      'purchases': {r[0]: r[1] for r in conv}, 'users': {r[0]: r[1] for r in nr}})
    old = _json(TRAFFIC) or {}
    _write(TRAFFIC, {'pulled_at': dt.date.today().isoformat(),
                     'source': old.get('source') or 'Google Analytics 4 via Metabase dashboard 26.', 'weeks': weeks})
    return {'weeks': len(weeks), 'until': weeks[0]['until']}


# ---------- keep fresh data across redeploys ----------

def _date_of(path):
    j = _json(path) or {}
    if 'meta' in j:
        return (j['meta'].get('window') or {}).get('until') or ''
    if isinstance(j.get('daily'), dict):
        return max(j['daily'] or {'': 0})
    if 'weeks' in j:
        return (j['weeks'] or [{}])[0].get('until') or ''
    if 'window' in j:
        return j['window'].get('until') or ''
    return ''


def persist():
    store = _store()
    if not store:
        return
    store.mkdir(parents=True, exist_ok=True)
    for p in (CACHE, SALES, TRAFFIC):
        if p.is_file():
            shutil.copy2(p, store / p.name)
    try:
        shutil.copy2(newest_capture_file(), store / 'capture.json')
    except RuntimeError:
        pass


def restore():
    """At start: use the disk copy of each file when it holds newer data than the copy from git."""
    store = _store()
    if not store or not store.is_dir():
        return []
    used = []
    for p in (CACHE, SALES, TRAFFIC):
        s = store / p.name
        if s.is_file() and _date_of(s) > _date_of(p):
            p.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(s, p)
            used.append(p.name)
    s = store / 'capture.json'
    if s.is_file():
        try:
            cur = _date_of(newest_capture_file())
        except RuntimeError:
            cur = ''
        if _date_of(s) > cur:
            RAW.mkdir(parents=True, exist_ok=True)
            shutil.copy2(s, RAW / f'api_capture_{_date_of(s)}_restored_1y.json')
            used.append('capture')
    return used


WIDGET = """<div id="refreshBox" style="position:fixed;right:12px;bottom:48px;z-index:9999;background:#fff;color:#1d1b18;border:1px solid #e2ddd3;border-radius:12px;padding:8px 12px;font:12px/1.45 system-ui,sans-serif;box-shadow:0 2px 10px rgba(0,0,0,.08);max-width:min(300px,calc(100vw - 24px));box-sizing:border-box"></div>
<script>
(() => {
  const box = document.getElementById('refreshBox');
  const day = (s) => s ? new Date(s + 'T00:00:00Z').toLocaleDateString('en-IN', { day: 'numeric', month: 'short', timeZone: 'UTC' }) : 'unavailable';
  const hm = (s) => new Date(s).toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' });
  let wasRunning = false, timer = null;
  const add = (text, color) => { const d = document.createElement('div'); if (color) d.style.color = color; d.textContent = text; box.append(d); };
  const draw = (st, err) => {
    box.textContent = '';
    const d = st.dates || {};
    add(`Ads to ${day(d.ads)} \\u00b7 sales to ${day(d.sales)}`);
    const cf = st.configured || {};
    if (!cf.meta) add('Meta ads: not set up (add META_ACCESS_TOKEN to .env)', '#6b665d');
    if (!cf.metabase) add('Website sales: not set up (add METABASE_USER and METABASE_PASSWORD to .env)', '#6b665d');
    if (st.running) add(`Refreshing: ${st.step}\\u2026`, '#8a5a14');
    else {
      const b = document.createElement('button');
      b.type = 'button';
      b.textContent = 'Refresh data';
      b.style.cssText = 'margin-top:6px;border:0;border-radius:8px;background:#8a5a14;color:#fff;padding:5px 10px;font-weight:600;cursor:pointer';
      const wait = st.next_allowed_at && new Date(st.next_allowed_at) > new Date();
      if (wait) { b.disabled = true; b.style.opacity = '.5'; }
      b.onclick = async () => {
        b.disabled = true;
        const r = await fetch('/api/refresh', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}' });
        const j = await r.json().catch(() => ({}));
        if (!r.ok) draw(st, j.error || 'Refresh did not start.'); else { wasRunning = true; draw(j); poll(); }
      };
      box.append(b);
      if (wait) add(`Next refresh after ${hm(st.next_allowed_at)}`, '#6b665d');
      if (st.last && !st.last.ok) add('Last refresh had errors: ' + Object.entries(st.last.parts || {}).filter(([, v]) => v.error).map(([k, v]) => `${k}: ${v.error}`).join('; '), '#b3261e');
    }
    if (err) add(err, '#b3261e');
  };
  const load = async () => {
    const r = await fetch('/api/refresh'); if (!r.ok) return null;
    const st = await r.json();
    if (!st.configured || !(st.configured.meta || st.configured.metabase)) { box.remove(); return null; }
    draw(st);
    if (wasRunning && !st.running) { wasRunning = false; location.reload(); }
    return st;
  };
  const poll = () => { clearInterval(timer); timer = setInterval(async () => { const st = await load(); if (st && !st.running) clearInterval(timer); }, 4000); };
  load().then((st) => { if (st && st.running) { wasRunning = true; poll(); } });
})();
</script>"""
