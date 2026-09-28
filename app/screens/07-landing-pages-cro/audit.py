"""Audit for 07-landing-pages-cro: where the page part of the buy path is broken, with proof and money.

Findings follow app/contracts/audit.md. Every number comes from app/metrics.py (session_funnel, aov).
Brand facts come from app/brain/<brand>/ through store.Brain. No connector, no model, no wall clock:
the same tables, brain and window give the same findings.

Rules
  CRO-R07  Device break. Owner: 07-landing-pages-cro.
           For each device, each step (sessions to add to cart, add to cart to checkout, checkout to
           purchase) in the current window against the median of the TRAILING windows before it
           (session_funnel with device=). The break is the step with the most money. Fires when the
           rate sits more than MIN_GAP_REL below its median. Stake = (median - current) x volume into
           the step x value per unit downstream (later step rates x AOV). Desktop's rate on the same
           step is written as context, never as the baseline. Severity: critical over 5 percent of net
           revenue in the window, high over 1 percent or when 2 or more windows agree, else medium.
           Net revenue here is GA4 purchases x AOV, so both sides share one scale. Capability SITE-C44.
           Inputs: sessions (GA4), aggregates/daily (AOV).
  CRO-R02  Message mismatch on a paid social lander. Owner: 07-landing-pages-cro.
           Promise elements come from the brain's Ad Library records (PROMISES). A page carries an
           element when a site-captured brain record whose source or evidence is that page holds one of
           the element's terms. A lander whose page was captured and misses an element fires. Stake =
           (the lander's own median paid social conversion - current) x paid social sessions x AOV;
           null when the lander is at or above its median. The stake is the lander's drop; the
           mismatch is the named cause, not a proven one. Severity as CRO-R07. Capability SITE-C36.
           A lander with no captured page emits status unavailable (message_match_score cannot be
           read). Inputs: sessions (GA4), aggregates/daily (AOV), brain offers, learnings, story_bank,
           claims, voice, identity, policies.
"""
import importlib.util
import statistics
import sys
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import urlparse

APP = Path(__file__).resolve().parents[2]
SCREEN = '07-landing-pages-cro'
TRAILING = 6            # windows before the current one for the own median
AGREE_WINDOWS = 4       # current plus 3 before, checked for agreement
MIN_GAP_REL = 0.01      # below 1 percent of the median is noise
FRESHNESS_DAYS = 1      # generated data is captured the morning after the last full day
PAID_SOCIAL = 'Paid Social'

STEPS = (  # step, count in, label, what the rate says
    ('add_to_cart', 'sessions', 'Add to cart', 'of sessions add to cart'),
    ('checkout', 'add_to_cart', 'Checkout', 'of carts reach checkout'),
    ('purchase', 'checkout', 'Purchase', 'of checkouts become orders'),
)
RATE_KEY = {'add_to_cart': 'add_to_cart_rate', 'checkout': 'checkout_rate', 'purchase': 'purchase_rate'}
DEVICE_LABEL = {'mobile': 'Mobile', 'desktop': 'Desktop', 'tablet': 'Tablet'}

# Elements an ad promises, from Ad Library records in the brain, and the words that show a page keeps them.
PROMISES = (
    {'element': 'offer', 'record': 'offers.first_order_code', 'reach': 'offers.promo_share_active_ads',
     'terms': ('comfort20', '20% off', '20 percent off')},
    {'element': 'comfort hook', 'record': 'learnings.hook_types', 'reach': None, 'terms': ('comfort',)},
    {'element': 'giving line', 'record': 'story_bank.mission_line_in_ads', 'reach': None,
     'terms': ('donate', 'one purchased')},
)
PROMISE_WORDS = {'comfort hook': 'comfort', 'giving line': 'one item donated for each item bought'}
PAGE_SECTIONS = ('claims', 'offers', 'policies', 'voice', 'identity', 'story_bank')

RULES = [
    {'rule_id': 'CRO-R07', 'name': 'Device break in the buy path with money at stake', 'entity_type': 'device',
     'inputs': ['sessions', 'aggregates/daily'], 'capability': 'SITE-C44', 'owner_screen': SCREEN},
    {'rule_id': 'CRO-R02', 'name': 'Ad promise missing on the paid social lander', 'entity_type': 'page',
     'inputs': ['sessions', 'aggregates/daily', 'brain: offers, learnings, story_bank, claims, voice, identity, policies'],
     'capability': 'SITE-C36', 'owner_screen': SCREEN},
]
SEVERITY_ORDER = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}


def _load(name, path):
    mod = sys.modules.get(name)
    if mod is None:
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod
        spec.loader.exec_module(mod)
    return mod


def metrics_module():
    """The server's metrics module when loaded, else app/metrics.py loaded here."""
    return _load('ecomos_metrics', APP / 'metrics.py')


def brain(brand, as_of):
    """The brand brain read as of the morning after the last full day, so stale flags are deterministic."""
    folder = str(APP / 'brain')
    if folder not in sys.path:
        sys.path.insert(0, folder)
    store = _load('ecomos_brain_store', APP / 'brain' / 'store.py')
    return store.Brain(brand, today=date.fromisoformat(as_of) + timedelta(days=1))


# ---------------------------------------------------------------- words

def usd(x):
    return f'${round(x):,}'


def pct(x):
    return f'{x * 100:.{2 if x < 0.1 else 1}f} percent'


def day_label(iso):
    d = date.fromisoformat(iso)
    return f'{d.day} {d.strftime("%b")}'


# ---------------------------------------------------------------- numbers

def window_of(brand, window):
    M = metrics_module()
    data = M.resolve(None, {'brand': brand})
    w = dict(window or {})
    return {'ends_on': w.get('ends_on') or data.brand['as_of'], 'days': int(w.get('days') or 28),
            'trailing': int(w.get('trailing') or 4)}


def ends(w, count):
    return [(date.fromisoformat(w['ends_on']) - timedelta(days=w['days'] * k)).isoformat() for k in range(count)]


def funnel_windows(brand, w, count, **filters):
    """session_funnel for `count` windows, newest first. by= results keep their groups."""
    M = metrics_module()
    q = {'brand': brand, 'window': f"{w['days']}d", **filters}
    return [M.compute('session_funnel', None, end=e, **q) for e in ends(w, count)]


def aov(brand, w):
    return metrics_module().compute('aov', None, brand=brand, window=f"{w['days']}d", end=w['ends_on'])


def group_rows(runs, by):
    """{key: [counts or None per window]} from by= runs."""
    out = {}
    for i, r in enumerate(runs):
        for g in ([] if r.get('unavailable') else r.get('groups') or []):
            out.setdefault(g[by], [None] * len(runs))[i] = g
    return out


def step_view(series, aov_value):
    """Per step: current rate, own median, gap, volume in, value downstream, money. series[0] is now."""
    now = series[0]
    rates = [None if s is None else {k: s.get(RATE_KEY[k]) for k in RATE_KEY} for s in series]
    out = []
    for i, (step, into, label, says) in enumerate(STEPS):
        past = [r[step] for r in rates[1:TRAILING + 1] if r and r[step] is not None]
        cur = rates[0][step]
        if cur is None or len(past) < 3:
            out.append({'step': step, 'label': label, 'current': cur, 'median': None, 'money': None,
                        'reason': f'only {len(past)} earlier windows; the median needs 3'})
            continue
        median = statistics.median(past)
        downstream = aov_value
        for later, _, _, _ in STEPS[i + 1:]:
            downstream *= rates[0][later] or 0
        gap = max(median - cur, 0.0)
        # windows agreeing: this window and each one before it while it stays below its own median
        agree = 0
        for k in range(AGREE_WINDOWS):
            r = rates[k] if k < len(rates) else None
            hist = [x[step] for x in rates[k + 1:k + 1 + TRAILING] if x and x[step] is not None]
            if r is None or r[step] is None or len(hist) < 3 or r[step] >= statistics.median(hist):
                break
            agree += 1
        out.append({'step': step, 'label': label, 'says': says, 'current': round(cur, 6), 'median': round(median, 6),
                    'gap': round(gap, 6), 'volume': now[into], 'value_per_unit': round(downstream, 2),
                    'money': round(gap * now[into] * downstream, 2), 'windows_agreeing': agree})
    return out


def device_breaks(brand, window=None):
    """The funnel per device with each step against its own median, and the break (the step with the most money)."""
    w = window_of(brand, window)
    runs = funnel_windows(brand, w, TRAILING + AGREE_WINDOWS, by='device')
    a = aov(brand, w)
    if runs[0].get('unavailable') or a.get('unavailable'):
        bad = runs[0] if runs[0].get('unavailable') else a
        return {'unavailable': True, 'reason': bad.get('reason'), 'fix': bad.get('fix'), 'window': w, 'devices': []}
    total_purchases = runs[0]['inputs']['purchase']
    devices = []
    for dev, series in group_rows(runs, 'device').items():
        if series[0] is None:
            continue
        steps = step_view(series, a['value'])
        live = [s for s in steps if s.get('money') is not None and s['median'] and s['gap'] > MIN_GAP_REL * s['median']]
        brk = max(live, key=lambda s: s['money']) if live else None
        devices.append({'device': dev, 'label': DEVICE_LABEL.get(dev, dev), 'counts': series[0], 'steps': steps,
                        'break_step': brk['step'] if brk else None, 'money': round(sum(s['money'] for s in live), 2) if live else 0.0,
                        'break_money': brk['money'] if brk else None})
    devices.sort(key=lambda d: -d['counts']['sessions'])
    return {'unavailable': False, 'window': w, 'aov': a['value'], 'net_revenue_est': round(total_purchases * a['value'], 2),
            'purchases': total_purchases, 'sampled_rows': runs[0].get('sampled_rows', 0),
            'freshness': runs[0].get('freshness'), 'devices': devices}


# ---------------------------------------------------------------- brain: promises and pages

def page_label(page):
    return 'home page' if page == '/' else page + ' page'


def path_of(url):
    return urlparse(url or '').path or '/'


def record_pages(rec):
    src = rec.get('source') or {}
    refs = [src.get('ref')] + [e.get('ref') for e in rec.get('evidence') or []]
    return {path_of(r) for r in refs if r}


def record_words(rec):
    parts = [rec.get('text') or '', str(rec.get('value') or '')] + [e.get('quote') or '' for e in rec.get('evidence') or []]
    return ' '.join(parts).lower()


def site_records(b):
    """Site-captured records by page path."""
    pages = {}
    for sec in PAGE_SECTIONS:
        for rec in b.records(sec):
            if (rec.get('source') or {}).get('type') != 'site':
                continue
            for p in record_pages(rec):
                pages.setdefault(p, []).append(rec)
    return pages


def promises(b, brand):
    out = []
    for p in PROMISES:
        rec = b.get(f'{brand}.{p["record"]}')
        if rec is None:
            continue
        reach = b.get(f'{brand}.{p["reach"]}') if p['reach'] else None
        v = rec.get('value')
        words = (f"{v['discount_pct']} percent off the {v.get('applies_to', 'order')} with code {v['code']}"
                 if isinstance(v, dict) and v.get('code') else PROMISE_WORDS.get(p['element'], p['element']))
        out.append({'element': p['element'], 'ad_says': rec.get('text'), 'words': words, 'record': rec['id'], 'terms': list(p['terms']),
                    'reach': reach.get('value') if reach else None, 'reach_record': reach['id'] if reach else None,
                    'stale': rec.get('status') == 'stale'})
    return out


def message_match(b, brand, page):
    """Each promise element on one page: match, mismatch, or not checked when the page was never captured."""
    pages = site_records(b)
    recs = pages.get(page, [])
    rows = []
    for p in promises(b, brand):
        hit = next((r for r in recs if any(t in record_words(r) for t in p['terms'])), None)
        anywhere = next((r for rs in pages.values() for r in rs if any(t in record_words(r) for t in p['terms'])), None)
        status = 'not checked' if not recs else 'match' if hit else 'mismatch'
        rows.append(dict(p, status=status, page_record=hit['id'] if hit else None, page_says=hit.get('text') if hit else None,
                         elsewhere=anywhere['id'] if anywhere and not hit else None))
    checked = [r for r in rows if r['status'] != 'not checked']
    score = round(sum(r['status'] == 'match' for r in checked) / len(checked), 4) if checked else None
    return {'page': page, 'captured': bool(recs), 'page_records': [r['id'] for r in recs], 'elements': rows, 'score': score}


def landers(brand, window=None):
    """Paid social landers with their funnel, own median conversion and message match."""
    w = window_of(brand, window)
    runs = funnel_windows(brand, w, TRAILING + AGREE_WINDOWS, channel=PAID_SOCIAL, by='landing_page')
    if runs[0].get('unavailable'):
        return {'unavailable': True, 'reason': runs[0].get('reason'), 'fix': runs[0].get('fix'), 'window': w, 'pages': []}
    b = brain(brand, w['ends_on'])
    out = []
    for page, series in group_rows(runs, 'landing_page').items():
        if series[0] is None:
            continue
        conv = [s['conversion_rate'] if s else None for s in series]
        past = [c for c in conv[1:TRAILING + 1] if c is not None]
        median = statistics.median(past) if len(past) >= 3 else None
        agree = 0
        for k in range(AGREE_WINDOWS):
            hist = [c for c in conv[k + 1:k + 1 + TRAILING] if c is not None]
            if conv[k] is None or len(hist) < 3 or conv[k] >= statistics.median(hist):
                break
            agree += 1
        out.append({'page': page, 'sessions': series[0]['sessions'], 'purchases': series[0]['purchase'],
                    'conversion_rate': conv[0], 'median': round(median, 6) if median is not None else None,
                    'windows_agreeing': agree, 'match': message_match(b, brand, page)})
    out.sort(key=lambda p: -p['sessions'])
    return {'unavailable': False, 'window': w, 'pages': out, 'freshness': runs[0].get('freshness'),
            'sampled_rows': runs[0].get('sampled_rows', 0)}


# ---------------------------------------------------------------- findings

def severity_of(money, net, agree):
    share = money / net if (money is not None and net) else None
    if share is not None and share > 0.05:
        return 'critical', share
    if (share is not None and share > 0.01) or agree >= 2:
        return 'high', share
    return 'medium', share


def confidence_of(agree, sampled, minus=0.0):
    c = 0.9 if agree >= 4 else 0.7 if agree >= 2 else 0.5
    c -= 0.2 if sampled else 0.0
    return round(max(0.1, c - minus), 2)


def unavailable_finding(rule_id, brand, w, entity, reason, fix, severity, inputs, capability):
    return {
        'id': f"{SCREEN}.{rule_id}.{entity['id']}", 'screen': SCREEN, 'rule_id': rule_id, 'severity': severity,
        'entity': entity, 'evidence': [], 'sentence': f"{entity['label']} cannot be checked: {reason}.",
        'capability': capability, 'money_at_stake': None, 'money_reason': 'inputs unavailable', 'confidence': 0.1,
        'brain_refs': [], 'first_seen': w['ends_on'], 'last_seen': w['ends_on'], 'status': 'unavailable',
        'unavailable': {'inputs': inputs, 'connector': fix or 'ga4', 'fix': reason},
    }


def device_findings(brand, w, db):
    ev_base = {'window': f"{w['days']}d", 'ends_on': w['ends_on'], 'freshness_days': FRESHNESS_DAYS,
               'source': 'sessions, aggregates/daily', 'simulated': True}
    desktop = next((d for d in db['devices'] if d['device'] == 'desktop'), None)
    out = []
    for d in db['devices']:
        if not d['break_step']:
            continue
        s = next(x for x in d['steps'] if x['step'] == d['break_step'])
        ref = next((x for x in desktop['steps'] if x['step'] == s['step']), None) if desktop and d is not desktop else None
        evidence = [
            dict(ev_base, metric=f"{s['step']}_step_rate", value=s['current'], unit='ratio', baseline=s['median'], baseline_kind='own_median'),
            dict(ev_base, metric='volume_in', value=s['volume'], unit='count', baseline=None, baseline_kind='threshold'),
            dict(ev_base, metric='value_per_unit', value=s['value_per_unit'], unit='usd', baseline=None, baseline_kind='threshold'),
            dict(ev_base, metric='net_revenue_est', value=db['net_revenue_est'], unit='usd', baseline=None, baseline_kind='threshold'),
        ]
        if ref and ref.get('current') is not None:
            evidence.append(dict(ev_base, metric=f"desktop_{s['step']}_step_rate", value=ref['current'], unit='ratio',
                                 baseline=None, baseline_kind='threshold'))
        severity, share = severity_of(s['money'], db['net_revenue_est'], s['windows_agreeing'])
        since = (date.fromisoformat(w['ends_on']) - timedelta(days=w['days'] * max(s['windows_agreeing'], 1) - 1)).isoformat()
        desk = f" Desktop is {pct(ref['current'])}." if ref and ref.get('current') is not None else ''
        out.append({
            'id': f"{SCREEN}.CRO-R07.{d['device']}", 'screen': SCREEN, 'rule_id': 'CRO-R07', 'severity': severity,
            'entity': {'type': 'device', 'id': d['device'], 'label': d['label']}, 'evidence': evidence,
            'sentence': (f"{d['label']}: {pct(s['current'])} {s['says']}, below its own median of {pct(s['median'])} "
                         f"since {day_label(since)}.{desk}"),
            'capability': {'id': 'SITE-C44', 'autonomy': 'agent_does'},
            'money_at_stake': {'usd': round(s['money']), 'formula': '(median_rate - current_rate) x volume_in x value_per_unit',
                               'inputs': {'median_rate': s['median'], 'current_rate': s['current'], 'volume_in': s['volume'],
                                          'value_per_unit': s['value_per_unit']}, 'window': f"{w['days']}d"},
            'confidence': confidence_of(s['windows_agreeing'], db['sampled_rows']), 'brain_refs': [],
            'first_seen': since, 'last_seen': w['ends_on'], 'status': 'open', 'unavailable': None,
            'share_of_net_revenue': round(share, 6) if share is not None else None, 'windows_agreeing': s['windows_agreeing'],
            'step': s['step'],
        })
    return out


def lander_findings(brand, w, ld, aov_value, net):
    ev_base = {'window': f"{w['days']}d", 'ends_on': w['ends_on'], 'freshness_days': FRESHNESS_DAYS,
               'source': 'sessions, brain', 'simulated': True}
    out = []
    for p in ld['pages']:
        m = p['match']
        entity = {'type': 'page', 'id': p['page'], 'label': p['page']}
        if not m['captured']:
            out.append(unavailable_finding(
                'CRO-R02', brand, w, entity, 'this lander has no page capture in the brain, so its message match is unknown',
                'brain site capture', 'medium', ['brain site capture for ' + p['page']], {'id': 'SITE-C36', 'autonomy': 'agent_does'}))
            continue
        missing = [e for e in m['elements'] if e['status'] == 'mismatch']
        if not missing:
            continue
        e = missing[0]
        gap = max((p['median'] or 0) - p['conversion_rate'], 0.0) if p['median'] is not None else None
        money = round(gap * p['sessions'] * aov_value, 2) if gap else None
        evidence = [
            dict(ev_base, metric='message_match_score', value=m['score'], unit='ratio', baseline=1.0, baseline_kind='threshold'),
            dict(ev_base, metric='paid_social_sessions', value=p['sessions'], unit='count', baseline=None, baseline_kind='threshold'),
            dict(ev_base, metric='paid_social_conversion_rate', value=p['conversion_rate'], unit='ratio', baseline=p['median'],
                 baseline_kind='own_median'),
            dict(ev_base, metric='aov', value=aov_value, unit='usd', baseline=None, baseline_kind='threshold'),
        ]
        severity, share = severity_of(money, net, p['windows_agreeing']) if money else ('medium', None)
        reach = e.get('reach') or {}
        label = page_label(p['page'])
        drop = (f" Paid social converts there at {pct(p['conversion_rate'])}, against its own median of {pct(p['median'])}."
                if money else '')
        stake = None
        if money:
            stake = {'usd': round(money), 'formula': '(median_conversion - current_conversion) x paid_social_sessions x aov',
                     'inputs': {'median_conversion': p['median'], 'current_conversion': p['conversion_rate'],
                                'paid_social_sessions': p['sessions'], 'aov': aov_value}, 'window': f"{w['days']}d"}
        refs = [e['record']] + ([e['reach_record']] if e.get('reach_record') else []) + m['page_records']
        out.append({
            'id': f"{SCREEN}.CRO-R02.{p['page']}", 'screen': SCREEN, 'rule_id': 'CRO-R02', 'severity': severity,
            'entity': entity, 'evidence': evidence,
            'sentence': f"Meta ads promise {e['words']}, but the {label} does not show it.{drop}",
            'capability': {'id': 'SITE-C36', 'autonomy': 'agent_does'},
            'money_at_stake': stake,
            **({} if stake else {'money_reason': 'the lander converts at or above its own median'}),
            'confidence': confidence_of(p['windows_agreeing'], ld['sampled_rows'], minus=0.2),
            'brain_refs': sorted(set(refs)),
            'first_seen': (date.fromisoformat(w['ends_on']) - timedelta(days=w['days'] * max(p['windows_agreeing'], 1) - 1)).isoformat(),
            'last_seen': w['ends_on'], 'status': 'open', 'unavailable': None,
            'share_of_net_revenue': round(share, 6) if share is not None else None,
            'element': e['element'], 'message_match_score': m['score'],
        })
    return out


def run(brand, window=None):
    """Findings for this screen, sorted by severity then stake. window: {ends_on, days, trailing}."""
    w = window_of(brand, window)
    db = device_breaks(brand, w)
    if db['unavailable']:
        return [unavailable_finding('CRO-R07', brand, w, {'type': 'brand', 'id': brand, 'label': 'The funnel by device'},
                                    db['reason'], db['fix'], 'high', ['sessions', 'aggregates/daily'],
                                    {'id': 'SITE-C44', 'autonomy': 'agent_does'})]
    findings = device_findings(brand, w, db)
    ld = landers(brand, w)
    if ld['unavailable']:
        findings.append(unavailable_finding('CRO-R02', brand, w, {'type': 'brand', 'id': brand, 'label': 'Paid social landers'},
                                            ld['reason'], ld['fix'], 'medium', ['sessions'], {'id': 'SITE-C36', 'autonomy': 'agent_does'}))
    else:
        findings += lander_findings(brand, w, ld, db['aov'], db['net_revenue_est'])
    findings.sort(key=lambda f: (SEVERITY_ORDER[f['severity']], f['status'] == 'unavailable',
                                 -((f['money_at_stake'] or {}).get('usd') or -1)))
    return findings


if __name__ == '__main__':
    import json
    print(json.dumps(run(sys.argv[1] if len(sys.argv) > 1 else 'bombas'), indent=1))
