"""Measurement and data health API: /api/22-measurement/...

  GET overview?brand=bombas   tiles, insights, reconciliation table, trust check, chart, findings, rules
  GET findings?brand=bombas   the audit findings only (audit.py, contract shape)

The store's paid orders are the truth. Platform numbers are what Meta, Google and GA4 report. Every number
comes from audit.window_numbers (app/metrics.py plus one GROUP BY each on data.sqlite). Insights are rules in
`insights()`, each with the sentence it produces and its capability. Missing is unavailable, never 0.
Default brand is bombas (simulated). Read-only: nothing here writes anywhere.
"""
import importlib.util
import re
from datetime import timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _audit():
    spec = importlib.util.spec_from_file_location('measurement_audit', HERE / 'audit.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


audit = _audit()
DEFAULT_BRAND = 'bombas'
CHART_DAYS = 90
WINDOW = f'{audit.DAYS}d'


def _delta(now, before):
    if now is None or not before:
        return None
    return round(now / before - 1, 4)


def _tile(name, plain, value, unit, ends_on, sources, reason=None, fix=None, **extra):
    out = {'name': name, 'plain': plain, 'unit': unit, 'value': value, 'window': WINDOW, 'freshness': ends_on,
           'sources': [{'table': t} for t in sources], 'unavailable_reason': reason if value is None else None,
           'fix': fix if value is None else None}
    out.update(extra)
    return out


def tiles(ws, ends_on):
    now, prev = ws[0], ws[1]
    m, mp = audit.mer(now), audit.mer(prev)
    o, op = audit.overlap(now), audit.overlap(prev)
    c, cp = audit.capture(now), audit.capture(prev)
    mer_v = m['value'] if m else None
    return {
        'mer': _tile('MER', 'Store net revenue over all paid spend: Meta, Google, YouTube creators, TikTok, Pinterest and other. '
                     'The store\'s own count, 28 days.', mer_v, 'x', ends_on,
                     ['orders', 'ad_rows', 'google_rows', 'paid_other_spend'],
                     reason='store orders or a paid spend source is not connected', fix='shopify, meta_ads, google_ads',
                     delta=_delta(mer_v, mp['value'] if mp else None), inputs=m,
                     formula='store net revenue / (Meta + Google + other paid spend)'),
        'overlap': _tile('Platform claims vs store', 'Purchases Meta and Google claim, over store orders whose last click was '
                         'paid social or paid search. Over 100 percent means both claim the same orders.',
                         o['value'] if o else None, '%', ends_on, ['ad_rows', 'google_rows', 'orders'],
                         reason='an ad platform or the store is not connected', fix='meta_ads, google_ads, shopify',
                         delta=_delta(o['value'] if o else None, op['value'] if op else None), inputs=o,
                         formula='(Meta purchases + Google conversions) / store orders with a paid last click'),
        'capture': _tile('GA4 purchase capture', 'GA4 purchases over store web orders. The rest are orders GA4 never saw.',
                         c, '%', ends_on, ['sessions', 'orders'], reason='GA4 or the store is not connected', fix='ga4, shopify',
                         delta=_delta(c, cp), target=audit.GA4_CAPTURE_MIN,
                         inputs={'ga4_purchases': (now['ga4'] or {}).get('purchases'),
                                 'store_web_orders': (now['store'] or {}).get('web_orders')},
                         formula='GA4 purchases / store web orders'),
    }


def reconciliation(ws):
    """One row per source: what it says against what the store saw. Totals kept apart from the rows."""
    w = ws[0]
    st = w['store']
    rows = []
    if w['ga4'] is not None:
        rows.append({'source': 'GA4', 'basis': 'ecommerce purchases, all web sessions', 'orders': int(w['ga4']['purchases']),
                     'value': round(w['ga4']['revenue'], 2), 'store_orders': st['web_orders'] if st else None,
                     'store_value': st['web_net'] if st else None, 'spend': None})
    for c, label, basis in (('meta', 'Meta', '7-day click and 1-day view'), ('google', 'Google', 'conversions, Google model')):
        if w[c] is None:
            rows.append({'source': label, 'basis': basis, 'orders': None, 'value': None, 'store_orders': None,
                         'store_value': None, 'spend': None, 'unavailable': True})
            continue
        acq = audit.PLATFORMS[c]['acq']
        rows.append({'source': label, 'basis': basis, 'orders': int(round(w[c]['purchases'])),
                     'value': round(w[c]['purchase_value'], 2), 'store_orders': st[acq] if st else None,
                     'store_value': st[acq + '_net'] if st else None, 'spend': w[c]['spend'],
                     'roas': round(w[c]['purchase_value'] / w[c]['spend'], 4) if w[c]['spend'] else None})
    for r in rows:
        r['gap'] = round(r['orders'] / r['store_orders'] - 1, 4) if r.get('orders') is not None and r.get('store_orders') else None
    spend = audit.spend_by_platform(w)
    meta, google = w['meta'], w['google']
    total = None
    if meta is not None and google is not None:
        pv = meta['purchase_value'] + google['purchase_value']
        sp = meta['spend'] + google['spend']
        total = {'claimed_orders': int(round(meta['purchases'] + google['purchases'])), 'claimed_value': round(pv, 2),
                 'spend': round(sp, 2), 'period_roas': round(pv / sp, 4) if sp else None,
                 'store_orders': st['orders'] if st else None, 'store_net': st['net'] if st else None,
                 'basis': 'period ROAS is total claimed value over total spend, Meta and Google only'}
    return {'rows': rows, 'total': total, 'spend_by_platform': spend}


def incrementality(ws):
    """Placeholders: lift reads unavailable with the test named until a holdout_tests row exists."""
    spend = audit.spend_by_platform(ws[0])
    total = sum(spend.values()) or None
    out = []
    for key in sorted(spend, key=lambda k: (-spend[k], k)):
        spec = audit.PLATFORMS.get(key, {'label': key, 'holdout': 'geo holdout'})
        out.append({'platform': spec['label'], 'spend': spend[key], 'share': round(spend[key] / total, 4) if total else None,
                    'lift': None, 'status': 'unavailable', 'test': spec['holdout']})
    return out


def insights(ws, findings):
    """The 2 rules behind the insight cards. Each returns its sentence and capability."""
    out = []
    now, prev = ws[0], ws[1]
    c, cp = audit.capture(now), audit.capture(prev)
    rule = f'GA4 purchases / store web orders, {audit.DAYS} days; fires under {round(audit.GA4_CAPTURE_MIN * 100)} percent'
    if c is None:
        out.append({'id': 'ga4_capture', 'severity': 'high', 'capability': 'MONEY-C20', 'autonomy': 'human_assist',
                    'sentence': 'GA4 capture cannot be read. GA4 or the store is not connected.', 'rule': rule})
    elif c < audit.GA4_CAPTURE_MIN:
        missed = now['store']['web_orders'] - int(now['ga4']['purchases'])
        s = (f'GA4 saw {round(c * 100, 1)} percent of web orders in {audit.DAYS} days. It missed {missed:,} orders, so every '
             f'GA4 conversion rate and channel report reads low.')
        if cp is not None:
            s = s.replace(' It missed', f' The {audit.DAYS} days before were {round(cp * 100, 1)} percent. It missed')
        out.append({'id': 'ga4_capture', 'severity': 'high', 'capability': 'MONEY-C20', 'autonomy': 'human_assist',
                    'sentence': s, 'rule': rule})
    else:
        out.append({'id': 'ga4_capture', 'severity': 'info', 'capability': None, 'autonomy': None,
                    'sentence': f'GA4 saw {round(c * 100, 1)} percent of web orders in {audit.DAYS} days.', 'rule': rule})
    o = audit.overlap(now)
    rule = (f'(Meta purchases + Google conversions) / store orders with a paid last click; double counting over '
            f'{round(audit.OVERLAP_MAX * 100)} percent, under-claiming under 90 percent')
    if o is None:
        out.append({'id': 'overlap', 'severity': 'high', 'capability': 'MONEY-C23', 'autonomy': 'agent_does',
                    'sentence': 'Platform claims cannot be set against store orders. An ad platform or the store is not connected.',
                    'rule': rule})
    else:
        pct = round(o['value'] * 100)
        if o['value'] > audit.OVERLAP_MAX:
            s = (f'Meta and Google claim {o["claimed"]:,} purchases, {pct} percent of the {o["store_paid"]:,} store orders '
                 f'with a paid last click. Both are counting some of the same orders.')
            sev = 'high'
        elif o['value'] < 0.9:
            s = (f'Meta and Google claim {o["claimed"]:,} purchases, {pct} percent of the {o["store_paid"]:,} store orders '
                 f'with a paid last click. They see fewer sales than the store does.')
            sev = 'medium'
        else:
            s = (f'Meta and Google claim {o["claimed"]:,} purchases against {o["store_paid"]:,} store orders with a paid '
                 f'last click, {pct} percent. No double counting at the total. The store took {o["store_orders"]:,} orders in all.')
            sev = 'info'
        gaps = [f for f in findings if f['rule_id'] == 'MEAS-R04' and f['status'] == 'open']
        if gaps:
            s += ' ' + gaps[0]['sentence'].split('. ')[-1]
            sev = 'medium' if sev == 'info' else sev
        out.append({'id': 'overlap', 'severity': sev, 'capability': 'MONEY-C23', 'autonomy': 'agent_does', 'sentence': s,
                    'rule': rule})
    return out


def chart(rd):
    """Orders per day, 90 days: the store's web orders against what GA4, Meta and Google report."""
    end = rd.ends_on
    start = end - timedelta(days=CHART_DAYS - 1)
    labels = [(start + timedelta(days=i)).isoformat() for i in range(CHART_DAYS)]
    try:
        st = rd.store_daily(days=CHART_DAYS)
    except audit.Missing:
        return {'unavailable': True, 'reason': 'Store orders are not connected, so there is nothing to compare against.',
                'fix': 'shopify'}
    series = [{'name': 'Store web orders', 'values': [st[d]['web'] if d in st else None for d in labels]}]
    try:
        ga = rd.ga4_daily(days=CHART_DAYS)
        series.append({'name': 'GA4 purchases', 'values': [int(ga[d]['purchases']) if d in ga else None for d in labels]})
    except audit.Missing:
        pass
    for c, label in (('meta', 'Meta claimed'), ('google', 'Google claimed')):
        daily = rd.platform_daily(c, days=CHART_DAYS)
        if daily is not None:
            series.append({'name': label, 'values': [round(daily[d]) if d in daily else None for d in labels]})
    return {'labels': labels, 'series': series, 'window': f'{CHART_DAYS}d',
            'basis': 'store orders are paid web orders; Meta is 7-day click and 1-day view; Google is its own conversion model'}


def overview(data, brand):
    ends_on = audit.last_full_day(data, brand)
    rd = audit.Reader(data, brand, ends_on)
    b = rd.source.brand or {}
    head = {'brand': b.get('brand'), 'name': b.get('name'), 'as_of': b.get('as_of'), 'simulated': rd.simulated,
            'market': b.get('market')}
    ws = audit.windows(rd)
    findings = audit.run(brand, {'ends_on': ends_on.isoformat()}, data=data, ws=ws)
    return {'brand': head, 'window': {'ends_on': ends_on.isoformat(), 'days': audit.DAYS},
            'tiles': tiles(ws, ends_on.isoformat()), 'insights': insights(ws, findings),
            'reconciliation': reconciliation(ws), 'trust': audit.trust_checks(rd, ws[0]),
            'incrementality': incrementality(ws), 'chart': chart(rd), 'findings': findings, 'rules': audit.RULES,
            'missing': sorted(set(ws[0]['missing']))}


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
