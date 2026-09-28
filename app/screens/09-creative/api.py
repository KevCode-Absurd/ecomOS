"""Creative API: /api/09-creative/...

  GET overview?brand=bombas   tiles, format table, insights, chart, findings, rules
  GET findings?brand=bombas   the audit findings only (audit.py, contract shape)

Every number comes from app/metrics.py and the brain through audit.Reader. Insights are rules in
`insights()`, each with the sentence it produces and the capability it maps to. Missing is
unavailable, never 0. Default brand is bombas (simulated). Read-only: nothing here writes anywhere.
"""
import importlib.util
import re
import statistics
from datetime import timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _audit():
    spec = importlib.util.spec_from_file_location('creative_audit', HERE / 'audit.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


audit = _audit()
DEFAULT_BRAND = 'bombas'
W = audit.WINDOW


def _tile(name, plain, value, unit, window, as_of, reason=None, fix=None, **extra):
    out = {'name': name, 'plain': plain, 'unit': unit, 'value': value, 'window': window, 'freshness': as_of,
           'unavailable_reason': reason if value is None else None, 'fix': fix if value is None else None,
           'sources': [{'table': 'ad_rows'}]}
    out.update(extra)
    return out


def tiles(rd, fw, counts):
    as_of = rd.ends_on.isoformat()
    now, base = counts[0], statistics.median(counts[1:]) if len(counts) > 1 else None
    new_ads = _tile('New ads launched', 'Ads whose first day of spend fell in the last 28 days.', now, 'n', f'{W}d', as_of,
                    delta=round(now / base - 1, 4) if base else None, delta_label='vs median of 4 prior windows',
                    inputs={'new_ads': now, 'prior_windows': counts[1:]})
    total = sum(f['spend'] for f in fw[0].values())
    video = fw[0].get('video', {}).get('spend')
    share = round(video / total, 4) if total and video is not None else None
    prev_total = sum(f['spend'] for f in fw[1].values()) if len(fw) > 1 else 0
    prev_video = fw[1].get('video', {}).get('spend') if len(fw) > 1 else None
    prev = round(prev_video / prev_total, 4) if prev_total and prev_video is not None else None
    video_share = _tile('Video share of spend', 'Meta spend on video ads over all Meta spend, 28 days.', share, '%',
                        f'{W}d', as_of, reason='no Meta spend in the window', fix='meta_ads',
                        delta=round(share / prev - 1, 4) if share is not None and prev else None,
                        delta_label='vs prior 28d', inputs={'video_spend': video, 'meta_spend': round(total, 2)})
    cols = rd.columns()
    col = next((c for c in audit.HOOK_PLAY_COLUMNS if c in cols), None)
    hook = None
    if col:
        start = (rd.ends_on - timedelta(days=W - 1)).isoformat()
        rows = [r for r in rd.source.table('ad_rows') if r.get('format') == 'video' and start <= r['date'] <= as_of]
        imps = sum(r.get('impressions') or 0 for r in rows)
        plays = sum(r.get(col) or 0 for r in rows)
        hook = round(plays / imps, 4) if imps >= audit.HOOK_MIN_IMPRESSIONS else None
    hook_rate = _tile('Video hook rate', 'Share of video impressions that watched 3 seconds.', hook, '%', f'{W}d', as_of,
                      reason='The Meta pull has no 3-second play count for video ads.',
                      fix='Add 3-second video plays to the Meta ad pull.')
    return {'new_ads': new_ads, 'video_share': video_share, 'hook_rate': hook_rate}


def format_rows(fw):
    """One row per format: 28-day spend, ROAS, ads, and the median ROAS of the 4 windows before."""
    rows = []
    total = sum(f['spend'] for f in fw[0].values())
    for name in sorted(fw[0]):
        f = fw[0][name]
        past = [w[name]['roas'] for w in fw[1:] if name in w and w[name]['roas'] is not None]
        rows.append({'format': name, 'spend': f['spend'], 'share': round(f['spend'] / total, 4) if total else None,
                     'purchase_value': f['purchase_value'], 'roas': f['roas'], 'ads': f['ads'],
                     'roas_median_4w': round(statistics.median(past), 4) if len(past) >= audit.TRAILING else None})
    rows.sort(key=lambda r: -r['spend'])
    return rows


def insights(rows, account_roas, records, findings):
    """The rules behind the insight cards. Each returns the sentence it produces and its capability."""
    out = []
    ranked = [r for r in rows if r['roas'] is not None and (r['share'] or 0) >= audit.FORMAT_MIN_SHARE]
    rule = (f'Rank formats with {round(audit.FORMAT_MIN_SHARE * 100)} percent or more of Meta spend by 28-day ROAS; '
            f'flag one {round(audit.FORMAT_DROP * 100)} percent under its own 4-window median (CREA-R01)')
    if len(ranked) >= 2 and account_roas is not None:
        best = max(ranked, key=lambda r: r['roas'])
        worst = min(ranked, key=lambda r: r['roas'])
        fired = [f for f in findings if f['rule_id'] == 'CREA-R01']
        sentence = fired[0]['sentence'] if fired else (
            f'{best["format"].capitalize()} ads returned {best["roas"]:.2f}x and {worst["format"]} ads '
            f'{worst["roas"]:.2f}x in 28 days. The account returned {account_roas:.2f}x.')
        out.append({'id': 'format_winners', 'severity': fired[0]['severity'] if fired else 'info',
                    'capability': 'CREA-C16', 'autonomy': 'agent_does', 'sentence': sentence, 'rule': rule})
    else:
        out.append({'id': 'format_winners', 'severity': 'info', 'capability': None, 'autonomy': None,
                    'sentence': 'Fewer than 2 formats carry enough spend to compare.', 'rule': rule})
    own = next((r['value'] for r in records if isinstance(r.get('value'), dict) and r['value'].get('role') == 'self'), None)
    comp = [r['value'] for r in records if isinstance(r.get('value'), dict) and r['value'].get('role') == 'competitor'
            and r['value'].get('median_run_days') is not None]
    rule = 'Median days an ad stays live in the Ad Library, own page against each competitor (brain learnings, signal only)'
    if own and own.get('median_run_days') is not None and comp:
        days = sorted(c['median_run_days'] for c in comp)
        longer = sum(1 for d in days if d > own['median_run_days'])
        sentence = (f'Our ads stay live a median {own["median_run_days"]:g} days in the Ad Library. '
                    f'{longer} of {len(comp)} competitors keep theirs {days[0]:g} to {days[-1]:g} days.')
        out.append({'id': 'run_length', 'severity': 'low', 'capability': 'LOOP-C13', 'autonomy': 'agent_does',
                    'sentence': sentence, 'rule': rule,
                    'brain_refs': [r['id'] for r in records if isinstance(r.get('value'), dict) and r['value'].get('role')]})
    else:
        out.append({'id': 'run_length', 'severity': 'info', 'capability': None, 'autonomy': None,
                    'sentence': 'No Ad Library pull is on file, so run length cannot be compared.', 'rule': rule})
    return out


def chart(rd, fw):
    labels = [(rd.ends_on - timedelta(days=W * k)).isoformat() for k in range(len(fw))][::-1]
    names = sorted({n for w in fw for n in w})
    series = [{'name': n.capitalize(), 'values': [w[n]['roas'] if n in w else None for w in fw[::-1]]} for n in names]
    return {'labels': labels, 'series': series, 'window': f'{W}d windows ending on each date',
            'basis': 'platform reported purchase value over spend (Meta 7 day click, 1 day view)'}


def overview(data, brand):
    ends_on = audit.last_full_day(data, brand)
    rd = audit.Reader(data, brand, ends_on)
    b = rd.source.brand
    head = {'brand': b.get('brand'), 'name': b.get('name'), 'as_of': b.get('as_of'),
            'simulated': bool(b.get('simulated') or b.get('fictional')), 'market': b.get('market')}
    findings = audit.run(brand, {'ends_on': ends_on.isoformat()}, data=data)
    first, _ = rd.ads(W)
    if first.get('unavailable'):
        return {'brand': head, 'unavailable': True, 'reason': first.get('reason'), 'fix': first.get('fix'),
                'findings': findings, 'rules': audit.RULES}
    fw = audit.format_windows(rd)
    counts, _ = audit.launches(rd)
    roas = rd.m('period_roas', W, channel='meta')
    account_roas = None if roas.get('unavailable') else roas['value']
    records = audit.brain_records(brand, 'learnings', ends_on)
    rows = format_rows(fw)
    return {'brand': head, 'unavailable': False, 'window': {'ends_on': ends_on.isoformat(), 'days': W},
            'tiles': tiles(rd, fw, counts), 'account_roas': account_roas, 'formats': rows,
            'insights': insights(rows, account_roas, records, findings), 'chart': chart(rd, fw),
            'findings': findings, 'rules': audit.RULES}


def _brand(req):
    brand = req.arg('brand', DEFAULT_BRAND)
    if brand in ('', 'sample'):
        return None
    if not re.fullmatch(r'[a-z0-9-]{1,40}', brand):
        raise ValueError('brand must be a folder name like bombas')
    return brand


def handle(req):
    if req.method != 'GET':
        return 405, {'error': 'read only'}
    try:
        brand = _brand(req)
        data = None if brand else req.data
        if brand:
            audit.brand_data(brand)  # ValueError for an unknown brand
        if req.path == ['overview']:
            return overview(data, brand)
        if req.path == ['findings']:
            return {'findings': audit.run(brand, None, data=data), 'rules': audit.RULES}
    except ValueError as exc:
        return 400, {'error': str(exc)}
    return 404, {'error': 'not found', 'routes': ['overview', 'findings']}
