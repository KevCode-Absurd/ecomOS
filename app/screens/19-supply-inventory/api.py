"""Supply and inventory API: /api/19-supply-inventory/...

  GET overview?brand=bombas   tiles, insights, chart, the SKU stock table, findings and rules
  GET findings?brand=bombas   the audit findings only (audit.py, contract shape)

Stock, sell-through, lead times and reorder points per SKU come from audit.supply() (data.sqlite: inventory,
inbound_pos, order_lines, orders, products; landed cost from finance_inputs). Net revenue comes from app/metrics.py.
Insights are rules in `insights()`, each with the sentence it produces and the capability it maps to. Missing is
unavailable, never 0. Default brand is bombas (simulated). Read-only.
"""
import importlib.util
import re
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _audit():
    spec = importlib.util.spec_from_file_location('supply_inventory_audit', HERE / 'audit.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


audit = _audit()
DEFAULT_BRAND = 'bombas'
CHART_SKUS = 12          # the chart shows the SKUs with the least cover
PEAK_SKU_FLOOR = 0.8     # room spec: readiness under 80 percent
PEAK_MONTHS = (11, 12)   # Q4 peak: Black Friday through December (brain economics.monthly_revenue_shape)


def _tile(name, plain, value, unit, window=None, freshness=None, sources=None, **extra):
    out = {'name': name, 'plain': plain, 'unit': unit, 'value': value, 'window': window, 'freshness': freshness,
           'sources': sources or [], 'unavailable_reason': extra.pop('reason', None), 'fix': extra.pop('fix', None)}
    out.update(extra)
    return out


def _target_cover_days(rd):
    rows = rd.finance_rows('target_inventory_cover') or []
    live = [r for r in rows if r.get('effective_from', '') <= rd.ends_on.isoformat()
            and (r.get('effective_to') or '9999') >= rd.ends_on.isoformat()]
    if not live:
        return None
    r = live[-1]
    return r['value'] * 7 if r.get('unit') == 'weeks' else r['value']


def sku_table(rd, sup):
    sc = sup['scale']
    out = []
    for r in sup['rows']:
        g14, _, kind = audit.gap_days(r)
        out.append({'sku': r['sku'], 'title': r['title'], 'hero': r['hero'],
                    'on_hand': audit.scaled(r['on_hand'], sc),
                    'per_day': round(r['velocity_14d'] * sc, 1) if sc else None,
                    'cover_days': r['cover_days'], 'lead_days': r['lead_days'], 'next_eta': r['next_eta'],
                    'days_to_next': r['days_to_next'], 'on_order': audit.scaled(r['on_order'], sc),
                    'reorder_point': audit.scaled(r['reorder_point'], sc),
                    'safety_units': audit.scaled(r['safety_units'], sc),
                    'recommended_po': audit.scaled(r['recommended_po'], sc),
                    'gap_days': round(g14, 1) if g14 is not None else None, 'gap_kind': kind,
                    'landed_cost': r['landed_cost'],
                    'stock_value': round(audit.scaled(r['on_hand'], sc) * r['landed_cost'])
                    if sc and r['landed_cost'] is not None else None})
    return out


def tiles(rd, sup, table):
    if sup['unavailable']:
        na = {'reason': sup['reason'], 'fix': sup.get('fix')}
        return {'cover': _tile('Stock cover', 'Days of stock left at the last 14 days of sales.', None, 'days', **na),
                'short': _tile('SKUs short before a PO lands', 'SKUs that sell out before stock arrives.', None, 'n', **na),
                'value': _tile('Stock at landed cost', 'Units on hand times landed cost per unit.', None, '$', **na)}
    fresh = sup['ends_on']
    src = [{'table': 'inventory'}, {'table': 'order_lines'}]
    units = sum(r['on_hand'] for r in sup['rows'])
    per_day = sum(r['velocity_14d'] for r in sup['rows'])
    cover = round(units / per_day, 1) if per_day else None
    target = _target_cover_days(rd)
    t1 = _tile('Stock cover, all SKUs', 'Units on hand over units sold a day, last 14 days.'
               + (f' Target is {target:.0f} days ({target / 7:.0f} weeks, finance inputs).' if target else ''),
               cover, 'days', window='14d', freshness=fresh, sources=src,
               delta=round(cover / target - 1, 4) if cover and target else None,
               tone='bad' if cover and target and cover < target else None)
    short = [r for r in table if r['gap_days']]
    heroes = [r for r in short if r['hero']]
    t2 = _tile('SKUs that sell out before stock lands', f'{len(short)} of {len(table)} SKUs run out before the next '
               f'PO arrives, or before a PO placed today would. {len(heroes)} of them are top 5 sellers.',
               len(short), 'n', window='14d', freshness=fresh, sources=src + [{'table': 'inbound_pos'}],
               tone='bad' if short else 'good')
    vals = [r['stock_value'] for r in table]
    if any(v is None for v in vals):
        t3 = _tile('Stock at landed cost', 'Units on hand times landed cost per unit.', None, '$',
                   reason='landed cost is missing for some SKUs', fix='finance inputs')
    else:
        on_order = sum((r['on_order'] or 0) * r['landed_cost'] for r in table)
        t3 = _tile('Stock at landed cost', f'Units on hand times landed cost per unit. Open POs add '
                   f'${on_order:,.0f} more.', sum(vals), '$', window='now', freshness=fresh,
                   sources=[{'table': 'inventory'}, {'table': 'finance_inputs'}])
    return {'cover': t1, 'short': t2, 'value': t3}


def peak_demand(rd, sup):
    """Units sold per SKU in last year's peak months, from data.sqlite. None when those months are not covered."""
    year = rd.ends_on.year - 1 if rd.ends_on.month < PEAK_MONTHS[-1] else rd.ends_on.year
    start = date(year, PEAK_MONTHS[0], 1)
    end = date(year, PEAK_MONTHS[-1], 31)
    if end >= rd.ends_on:
        return None
    paid = ', '.join(f"'{s}'" for s in audit.PAID)
    span = rd.sql('SELECT MIN(substr(created_at, 1, 10)) AS first FROM orders')[0]['first']
    if not span or span > start.isoformat():
        return None
    rows = rd.sql(f"SELECT l.sku, SUM(l.qty) AS units FROM order_lines l JOIN orders o ON o.id = l.order_id "
                  f"WHERE o.status IN ({paid}) AND substr(o.created_at, 1, 10) BETWEEN '{start}' AND '{end}' "
                  f"GROUP BY l.sku")
    return {'start': start.isoformat(), 'end': end.isoformat(), 'units': {r['sku']: r['units'] for r in rows}}


def insights(rd, sup, table):
    """The rules behind the insight cards. Each returns the sentence it produces and its capability."""
    out = []
    rule = ('stock_cover_days (14-day pace) against the days to the next open PO, or the lead time when none is '
            'open; the SKU with the longest gap is named (room spec: reorder breach)')
    if sup['unavailable']:
        out.append({'id': 'runs_out_first', 'severity': 'high', 'capability': 'PROD-C22', 'autonomy': 'founder_gate',
                    'sentence': f'Stock cover is unavailable: {sup["reason"]}.', 'rule': rule})
    else:
        short = sorted((r for r in table if r['gap_days']), key=lambda r: (-r['gap_days'], r['cover_days'], r['sku']))
        if not short:
            out.append({'id': 'runs_out_first', 'severity': 'info', 'capability': None, 'autonomy': 'founder_gate',
                        'rule': rule, 'sentence': 'Every SKU has stock until its next PO lands.'})
        else:
            top = short[0]
            lands = f'the next PO lands {audit._day(date.fromisoformat(top["next_eta"]))}' if top['gap_kind'] == 'po' else \
                f'a PO placed today lands in {top["lead_days"]:.0f} days'
            s = (f'{len(short)} SKUs sell out before new stock lands. {top["title"]} goes first: '
                 f'{top["cover_days"]:.0f} days of cover and {lands}.')
            out.append({'id': 'runs_out_first', 'severity': 'high', 'capability': 'PROD-C22',
                        'autonomy': 'founder_gate', 'sentence': s, 'rule': rule,
                        'stub': 'Draft PO pull-ins and new POs for these SKUs with quantities from the reorder table. '
                                'Nothing is sent to a supplier until you approve.'})
    rule = (f'stock on hand plus open PO units against units sold in last year\'s November and December, per SKU '
            '(the stock part of peak_season_readiness_pct; staffing and system load are not connected). Fires when the '
            f'total is under 100 percent or one SKU is under {PEAK_SKU_FLOOR * 100:.0f} percent')
    peak = None if sup['unavailable'] else peak_demand(rd, sup)
    if peak is None:
        out.append({'id': 'peak_stock', 'severity': 'medium', 'capability': 'PROD-C72', 'autonomy': 'founder_gate',
                    'rule': rule, 'sentence': 'Peak stock is unavailable: last year\'s November and December are not '
                                              'in the order history.'})
    else:
        need = sum(peak['units'].get(r['sku'], 0) for r in sup['rows'])
        have = sum(r['on_hand'] + r['on_order'] for r in sup['rows'])
        low = sorted(((r, (r['on_hand'] + r['on_order']) / peak['units'][r['sku']]) for r in sup['rows']
                      if peak['units'].get(r['sku'])), key=lambda x: (x[1], x[0]['sku']))
        share = have / need if need else None
        sc = sup['scale']
        s = (f'Stock plus open POs is {share * 100:.0f} percent of what sold last November and December '
             f'({audit._fmt_int(audit.scaled(have, sc) or 0)} of {audit._fmt_int(audit.scaled(need, sc) or 0)} units).')
        if low and low[0][1] < PEAK_SKU_FLOOR:
            s += f' {low[0][0]["title"]} is lowest at {low[0][1] * 100:.0f} percent.'
        fires = (share is not None and share < 1) or bool(low and low[0][1] < PEAK_SKU_FLOOR)
        out.append({'id': 'peak_stock', 'severity': 'medium' if fires else 'info',
                    'capability': 'PROD-C72' if fires else None, 'autonomy': 'founder_gate', 'sentence': s,
                    'rule': rule, 'peak_window': [peak['start'], peak['end']],
                    'stub': ('Draft a peak plan: extra POs for the SKUs under last year\'s peak, with landing dates '
                             'before Black Friday. Nothing is ordered until you approve.') if fires else None})
    return out


def chart(sup, table):
    """Days of cover against days until stock lands, for the CHART_SKUS SKUs with the least cover."""
    if sup['unavailable']:
        return {'unavailable': True, 'reason': sup['reason'], 'fix': sup.get('fix')}
    rows = [r for r in table if r['cover_days'] is not None][:CHART_SKUS]
    return {'labels': [r['sku'].split('-', 2)[-1] for r in rows], 'titles': [r['title'] for r in rows],
            'cover': [r['cover_days'] for r in rows],
            'lands': [r['days_to_next'] if r['days_to_next'] is not None else r['lead_days'] for r in rows],
            'window': '14d', 'note': 'Stock lands on the next open PO date, or after the lead time when no PO is open.'}


def overview(data, brand):
    ends_on = audit.last_full_day(data, brand)
    rd = audit.Reader(data, brand, ends_on)
    b = rd.source.brand
    head = {'brand': b.get('brand'), 'name': b.get('name'), 'as_of': b.get('as_of'),
            'simulated': bool(b.get('simulated') or b.get('fictional')), 'market': b.get('market')}
    sup = audit.supply(rd)
    table = [] if sup['unavailable'] else sku_table(rd, sup)
    return {'brand': head, 'window': {'ends_on': ends_on.isoformat(), 'days': audit.VELOCITY_DAYS},
            'scale': None if sup['unavailable'] else sup['scale'],
            'tiles': tiles(rd, sup, table), 'insights': insights(rd, sup, table), 'chart': chart(sup, table),
            'skus': table, 'findings': audit.findings(rd), 'rules': audit.RULES,
            'settings': {'velocity_days': audit.VELOCITY_DAYS, 'service_z': audit.SERVICE_Z,
                         'review_days': audit.REVIEW_DAYS, 'hero_count': audit.HERO_COUNT}}


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
