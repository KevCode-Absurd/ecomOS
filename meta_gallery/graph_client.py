"""Direct Meta Marketing API route (read-only). Use once the Meta app is reactivated.

Commands:
  python -m meta_gallery.graph_client check
      Verifies the token, granted permissions, expiry and ad account access.
  python -m meta_gallery.graph_client capture
      Writes a version 2 raw capture (same shape as the MCP capture): one year of
      ad x day rows plus monthly age, gender and platform rows,
      then run: python -m meta_gallery.snapshot

Only HTTP GET is ever issued. The token is read from .env on the backend,
sent in the query string to graph.facebook.com only, and scrubbed from any
printed error. It is never written to the capture or shown in the browser.

Status: written against the documented Graph API but not yet run against a
live token, because the Meta app currently returns error 200 "API access
deactivated". Run `check` first after reactivation.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from .snapshot import DATA, ROOT

GRAPH = 'https://graph.facebook.com/' + os.environ.get('META_GRAPH_VERSION', 'v23.0')


def load_env(path=ROOT / '.env'):
    """Parse KEY=VALUE lines. Lines without '=' are ignored, never executed or echoed."""
    env = {}
    if path.exists():
        for line in path.read_text(encoding='utf-8-sig').splitlines():
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, value = line.split('=', 1)
            env[key.strip()] = value.strip().strip('"').strip("'")
    return env


class Graph:
    def __init__(self, token, account_id):
        self.token = token
        self.account = 'act_' + account_id.replace('act_', '')

    def get(self, path, **params):
        params['access_token'] = self.token
        url = f"{GRAPH}/{path.lstrip('/')}?{urllib.parse.urlencode(params)}"
        try:
            with urllib.request.urlopen(urllib.request.Request(url, method='GET'), timeout=60) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as exc:
            body = exc.read().decode('utf-8', 'replace')
            raise RuntimeError(self.scrub(f'HTTP {exc.code}: {body[:600]}')) from None
        except Exception as exc:  # network errors
            raise RuntimeError(self.scrub(str(exc))) from None

    def paged(self, path, **params):
        out = []
        data = self.get(path, **params)
        while True:
            out.extend(data.get('data', []))
            nxt = data.get('paging', {}).get('next')
            if not nxt:
                return out
            query = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(nxt).query))
            query.pop('access_token', None)
            data = self.get(path, **query)

    def scrub(self, text):
        return text.replace(self.token, '<token>') if self.token else text


def graph_from_env():
    env = {**load_env(), **{k: v for k, v in os.environ.items() if k.startswith('META_')}}
    token, account = env.get('META_ACCESS_TOKEN'), env.get('META_AD_ACCOUNT_ID')
    if not token or not account:
        sys.exit('META_ACCESS_TOKEN and META_AD_ACCOUNT_ID must be set in .env')
    return Graph(token, account)


def check():
    g = graph_from_env()
    ok = True
    try:
        info = g.get('debug_token', input_token=g.token).get('data', {})
        exp = info.get('expires_at')
        print('Token valid:', info.get('is_valid'))
        print('Token type:', info.get('type'), '| app id:', info.get('app_id'))
        print('Expires:', 'never' if not exp else datetime.fromtimestamp(exp, timezone.utc).isoformat())
        dax = info.get('data_access_expires_at')
        if dax:
            print('Data access expires:', datetime.fromtimestamp(dax, timezone.utc).isoformat())
        print('Scopes:', ', '.join(info.get('scopes', [])))
    except RuntimeError as exc:
        ok = False
        print('Token check failed:', exc)
    try:
        perms = g.get('me/permissions').get('data', [])
        print('Granted:', ', '.join(p['permission'] for p in perms if p.get('status') == 'granted'))
        extra = {'ads_management', 'business_management', 'pages_manage_ads'} & {p['permission'] for p in perms if p.get('status') == 'granted'}
        if extra:
            print('Note: token also holds write-capable scopes:', ', '.join(sorted(extra)),
                  '- this tool only sends GET requests, but a read-only token (ads_read) is safer.')
    except RuntimeError as exc:
        ok = False
        print('Permission check failed:', exc)
    try:
        acct = g.get(g.account, fields='name,currency,timezone_name,account_status')
        print('Account:', acct.get('name'), acct.get('currency'), acct.get('timezone_name'), 'status', acct.get('account_status'))
        rows = g.get(f'{g.account}/insights', date_preset='last_7d', fields='spend,impressions').get('data', [])
        print('Reporting read OK. Last 7 days spend:', rows[0].get('spend') if rows else '0 (no rows)')
        ads = g.get(f'{g.account}/ads', fields='id,creative{id}', limit=1).get('data', [])
        print('Creative read OK:' if ads else 'Creative read returned no ads', ads[0]['creative']['id'] if ads else '')
    except RuntimeError as exc:
        ok = False
        print('Account/reporting check failed:', exc)
    return ok


def action(actions, kind):
    for a in actions or []:
        if a.get('action_type') == kind:
            return a.get('value')
    return None


def to_row(r):
    """Map a Graph insights row to the MCP field names the snapshot expects."""
    return {
        'id': r['ad_id'], 'name': r.get('ad_name'), 'campaign_id': r.get('campaign_id'),
        'campaign_name': r.get('campaign_name'), 'adset_id': r.get('adset_id'), 'adset_name': r.get('adset_name'),
        'amount_spent': {'value': r.get('spend')}, 'impressions': r.get('impressions'),
        'omni_purchase': action(r.get('actions'), 'omni_purchase'),
        'omni_purchase_values': ({'value': v} if (v := action(r.get('action_values'), 'omni_purchase')) else None),
        'link_click': action(r.get('actions'), 'link_click'),
        'purchase_roas': action(r.get('purchase_roas'), 'omni_purchase'),
        'age': r.get('age'), 'gender': r.get('gender'),
        'publisher_platform': r.get('publisher_platform'), 'platform_position': r.get('platform_position'),
        'date_start': r.get('date_start'), 'date_stop': r.get('date_stop'),
    }


def creative_record(c):
    link = (c.get('object_story_spec') or {}).get('link_data') or {}
    out = {k: c.get(k) for k in ('id', 'name', 'object_type', 'body', 'title', 'call_to_action_type', 'image_hash',
                                'image_url', 'thumbnail_url', 'video_id', 'product_set_id', 'effective_object_story_id')}
    out['link_url'] = c.get('link_url') or link.get('link')
    out['child_attachments'] = link.get('child_attachments')
    if c.get('asset_feed_spec'):
        out['image_hash'] = None  # flexible / dynamic asset feed: not one static image
    return out


def by_ids(g, ids, fields):
    out = {}
    ids = list(ids)
    for i in range(0, len(ids), 50):
        out.update(g.get('', ids=','.join(ids[i:i + 50]), fields=fields))
    return out


def capture(days=365):
    """Write a version 2 raw capture: one year of ad x day rows plus monthly breakdowns."""
    g = graph_from_env()
    until = date.today() - timedelta(days=1)
    since = until - timedelta(days=days - 1)
    tr = json.dumps({'since': since.isoformat(), 'until': until.isoformat()})
    spend_filter = json.dumps([{'field': 'spend', 'operator': 'GREATER_THAN', 'value': 0}])
    meta_fields = 'ad_id,ad_name,adset_id,adset_name,campaign_id,campaign_name,spend,impressions,actions,action_values'
    ads = [to_row(r) for r in g.paged(f'{g.account}/insights', level='ad', time_range=tr, fields=meta_fields,
                                      filtering=spend_filter, limit=500)]
    ad_meta = by_ids(g, [r['id'] for r in ads], 'id,effective_status,status,creative{id}')
    for r in ads:
        m = ad_meta.get(r['id'], {})
        r.update(effective_status=m.get('effective_status'), status=m.get('status'),
                 creative_id=(m.get('creative') or {}).get('id'))
    print(f'{len(ads)} ads with spend from {since} to {until}')

    daily = [to_row(r) for r in g.paged(f'{g.account}/insights', level='ad', time_range=tr, time_increment=1,
                                        fields='ad_id,spend,impressions,actions,action_values',
                                        filtering=spend_filter, limit=500)]
    print(f'{len(daily)} ad-day rows')
    monthly = {}
    for dim in ('age', 'gender', 'publisher_platform'):
        monthly[dim] = [to_row(r) for r in g.paged(f'{g.account}/insights', level='ad', time_range=tr,
                                                   time_increment='monthly', breakdowns=dim,
                                                   fields='ad_id,spend,actions,action_values',
                                                   filtering=spend_filter, limit=500)]
        print(f'{len(monthly[dim])} monthly {dim} rows')

    cfields = ('id,name,object_type,body,title,call_to_action_type,image_hash,image_url,thumbnail_url,video_id,'
               'product_set_id,effective_object_story_id,link_url,object_story_spec,asset_feed_spec')
    creatives = [creative_record(c) for c in by_ids(g, {r['creative_id'] for r in ads if r['creative_id']}, cfields).values()]
    videos = [dict(v, id=k) for k, v in by_ids(g, {c['video_id'] for c in creatives if c.get('video_id')},
                                               'id,title,length,permalink_url,picture').items()]
    hashes = sorted({a.get('image_hash') for c in creatives for a in (c.get('child_attachments') or []) if a.get('image_hash')})
    images = []
    for i in range(0, len(hashes), 50):
        images += g.get(f'{g.account}/adimages', hashes=json.dumps(hashes[i:i + 50]), fields='hash,url,width,height').get('data', [])
    adsets = []
    for aid, a in by_ids(g, {r['adset_id'] for r in ads}, 'id,is_dynamic_creative,attribution_spec').items():
        spec = a.get('attribution_spec') or []
        setting = '_'.join(f"{s.get('window_days')}d_{s.get('event_type', '').lower().replace('click_through', 'click').replace('view_through', 'view').replace('engaged_video_view', 'ev')}" for s in spec)
        adsets.append({'id': aid, 'is_dynamic_creative': a.get('is_dynamic_creative'), 'attribution_setting': setting or None})
    acct = g.get(g.account, fields='name,currency,timezone_name')
    capture_obj = {
        'version': 2,
        'captured_at': datetime.now().astimezone().isoformat(timespec='seconds'),
        'source': f'Meta Marketing API {GRAPH.rsplit("/", 1)[-1]} (read-only GET)',
        'ad_account_id': g.account.replace('act_', ''),
        'window': {'since': since.isoformat(), 'until': until.isoformat()},
        'account': [{'id': g.account, 'name': acct.get('name'), 'timezone_name': acct.get('timezone_name'),
                     'amount_spent': {'unit': acct.get('currency')}}],
        'ads': ads, 'creatives': creatives, 'videos': videos, 'images': images, 'adsets': adsets,
        'daily': daily, 'monthly': monthly,
    }
    out = DATA / 'raw' / f"graph_capture_{datetime.now().strftime('%Y-%m-%d_%H%M')}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(capture_obj, ensure_ascii=False), encoding='utf-8')
    print('Wrote', out, '- now run: python -m meta_gallery.snapshot', out)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('command', choices=['check', 'capture'])
    args = parser.parse_args(argv)
    if args.command == 'check':
        sys.exit(0 if check() else 1)
    capture()


if __name__ == '__main__':
    main()
