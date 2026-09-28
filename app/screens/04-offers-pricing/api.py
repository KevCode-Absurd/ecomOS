"""Offers and pricing API: /api/04-offers-pricing/...

  GET overview?brand=bombas   the plan (ranked actions) with orientation numbers, then the desk: offer stack,
                              threshold economics, discount policy, pack ladder, guarantee table, findings, rules
  GET findings?brand=bombas   the audit findings only (audit.py, contract shape)
  GET rank?brand=bombas       ranked actions (depth.md section 5), from actions.rank; app/rank.py calls rank() too

Numbers come from app/metrics.py, the brand's aggregates (monthly, daily, products_monthly), finance_inputs and the
brain, all through audit.Reader. Insights are rules in `insights()`, each with the sentence it produces and the
capability it maps to. Missing is unavailable, never 0. Default brand is bombas (simulated). Read-only.
"""
import calendar
import importlib.util
import math
import re
import statistics
import sys
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _actions():
    name = 'offers_pricing_actions'
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, HERE / 'actions.py')
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


actions = _actions()
audit = actions.audit
model = actions.model
DEFAULT_BRAND = 'bombas'
CHART_MONTHS = 24
CREEP_POINTS = 5          # room spec: discount share up more than 5 points over 3 months is creep
STACK = [  # the offer stack, in the order a shopper meets it: (brain record key, label)
    ('offers.free_shipping_threshold_usd', 'Free shipping threshold'),
    ('offers.standard_shipping_cost', 'Shipping under the threshold'),
    ('offers.first_order_code', 'First-order code'),
    ('offers.promo_share_active_ads', 'Code in live ads'),
    ('offers.bundles_pack_ladder', 'Pack ladder'),
    ('offers.guarantee', 'Guarantee'),
    ('policies.returns_window_days', 'Return window'),
    ('offers.gifting', 'Gifting'),
]


def _tile(name, plain, value, unit, window=None, freshness=None, sources=None, **extra):
    out = {'name': name, 'plain': plain, 'unit': unit, 'value': value, 'window': window, 'freshness': freshness,
           'sources': sources or [], 'unavailable_reason': extra.pop('reason', None), 'fix': extra.pop('fix', None)}
    out.update(extra)
    return out


def _full(month_row):
    y, m = map(int, month_row['month'].split('-'))
    return month_row.get('days') == calendar.monthrange(y, m)[1]


# ---------------------------------------------------------------- offer stack

def _brief(value):
    if isinstance(value, dict):
        return ', '.join(f'{k.replace("_", " ")} {v}' for k, v in value.items())
    if isinstance(value, list):
        return ', '.join(str(v) for v in value)
    return str(value)


def offer_stack(rd):
    out = []
    for key, label in STACK:
        rec = rd.record(f'{rd.brand}.{key}') if rd.brand else None
        if not rec:
            out.append({'item': label, 'id': None, 'value': None, 'text': None, 'source': None, 'ref': None,
                        'date': None, 'tier': None, 'unavailable_reason': 'not in the brain'})
            continue
        src = rec.get('source') or {}
        out.append({'item': label, 'id': rec['id'], 'value': _brief(rec.get('value')), 'text': rec.get('text'),
                    'source': src.get('type'), 'ref': src.get('ref'), 'date': rec.get('date'), 'tier': rec.get('tier')})
    return out


# ---------------------------------------------------------------- free shipping threshold

def threshold(rd):
    t, rec = audit.threshold_usd(rd)
    be = audit.break_even(rd, rd.ends_on)
    dist = rd.m('order_value_distribution', audit.WINDOW, step=5)
    out = {'threshold': t, 'threshold_source': (rec or {}).get('source'), 'break_even': be.get('value'),
           'break_even_inputs': {k: be.get(k) for k in ('aov', 'label', 'gross_margin', 'label_rows')},
           'break_even_formula': 'AOV + average label / gross margin (room spec free_shipping_threshold_breakeven)',
           'margin_basis': 'target gross margin from finance_inputs; per-SKU cost does not join to products yet',
           'unavailable': t is None or be.get('value') is None or bool(dist.get('unavailable')),
           'reason': None if t is not None else 'no threshold in the brain'}
    if out['unavailable']:
        out['reason'] = out['reason'] or be.get('reason') or dist.get('reason')
        out['fix'] = be.get('fix') or dist.get('fix')
        return out
    band = audit.BAND_USD
    groups = dist['groups']
    under = audit.band_share(groups, t - band, t)
    over = audit.band_share(groups, t, t + band)
    below = audit.band_share(groups, 0, t)
    aov = be['aov']
    suggested = math.ceil(be['value'] / 5) * 5 if t < be['value'] else None
    lo, hi = max(0, t - 40), t + 60
    out.update({
        'band': band, 'share_just_under': under, 'share_just_over': over, 'share_below': below,
        'share_ship_free': round(1 - below, 6), 'above_aov': round(t / aov - 1, 4),
        'suggested': suggested,
        'suggested_share_below_now': audit.band_share(groups, 0, suggested) if suggested else None,
        'bins': [g for g in groups if lo <= g['from'] < hi], 'orders_sample': dist['value'],
        'shipping_paid_avg': (round(sum(g['shipping_charged'] for g in groups) / paying, 2)
                              if (paying := sum(g['paid_shipping_orders'] for g in groups)) else None),
        'shipping_listed': ((rd.record(f'{rd.brand}.offers.standard_shipping_cost') or {}).get('value') or {}).get('cost_usd')
                           if rd.brand else None,
        'window': dist['window'], 'basis': dist['basis'],
        'rule': (f'Move when the threshold is under break-even (suggest break-even rounded up to $5). A threshold '
                 f'that works shows more orders in the ${band} just over it than the ${band} just under it.'),
    })
    return out


# ---------------------------------------------------------------- discount policy

def discount_months(rd):
    rows = rd.table('monthly')
    if not rows:
        return None
    out = []
    for r in rows:
        gross, disc, orders, net = r.get('gross_sales'), r.get('discounts'), r.get('orders'), r.get('net_sales')
        out.append({'month': r['month'], 'full': _full(r), 'days': r.get('days'),
                    'discount_share': round(disc / gross, 6) if gross and disc is not None else None,
                    'aov': round(net / orders, 2) if orders and net is not None else None,
                    'discounts': disc, 'gross_sales': gross})
    return out


def bfcm(rd):
    """Discount depth over the last Black Friday to Cyber Monday against the 28 days before it."""
    rows = rd.table('daily')
    if not rows:
        return {'unavailable': True, 'reason': 'the daily aggregate is missing'}
    by = {r['date']: r for r in rows}
    year = rd.ends_on.year
    for y in (year, year - 1):
        nov = [date(y, 11, d) for d in range(1, 31) if date(y, 11, d).weekday() == 3]
        fri = nov[3] + timedelta(days=1)
        mon = fri + timedelta(days=3)
        if mon <= rd.ends_on:
            break
    else:
        return {'unavailable': True, 'reason': 'no Black Friday in the data yet'}

    def depth(days):
        rs = [by[d.isoformat()] for d in days if d.isoformat() in by]
        if len(rs) < len(days):
            return None
        g = sum(r['gross_sales'] for r in rs)
        return round(sum(r['discounts'] for r in rs) / g, 6) if g else None

    event = [fri + timedelta(days=i) for i in range(4)]
    before = [fri - timedelta(days=i) for i in range(1, 29)]
    d_event, d_before = depth(event), depth(before)
    if d_event is None or d_before is None:
        return {'unavailable': True, 'reason': 'the daily aggregate does not cover the event and the 28 days before'}
    orders = sum(by[d.isoformat()]['orders'] for d in event)
    return {'unavailable': False, 'start': fri.isoformat(), 'end': mon.isoformat(), 'depth': d_event,
            'baseline': d_before, 'points': round((d_event - d_before) * 100, 2), 'orders': orders}


# ---------------------------------------------------------------- pack ladder

def pack_size(sku, products):
    p = products.get(sku) or {}
    if p.get('items_per_unit'):
        return int(p['items_per_unit']), 'products.items_per_unit'
    m = re.search(r'-(\d+)$', sku)
    return (int(m.group(1)), 'sku suffix') if m else (None, None)


def ladder(rd, months=12):
    rows = rd.table('products_monthly')
    if not rows:
        return {'unavailable': True, 'reason': 'the products_monthly aggregate is missing', 'fix': 'shopify'}
    full = [m['month'] for m in (discount_months(rd) or []) if m['full']][-months:]
    products = {p['sku']: p for p in (rd.table('products') or []) if p.get('sku')}
    agg = {}
    for r in rows:
        if r['month'] in full:
            a = agg.setdefault(r['sku'], {'units': 0, 'net_sales': 0.0, 'category': r.get('category')})
            a['units'] += r['units'] or 0
            a['net_sales'] += r['net_sales'] or 0
    total = sum(a['net_sales'] for a in agg.values())
    lines = {}
    for sku, a in agg.items():
        size, basis = pack_size(sku, products)
        line = sku.rsplit('-', 1)[0]
        p = products.get(sku) or {}
        per_pack = a['net_sales'] / a['units'] if a['units'] else None
        lines.setdefault(line, []).append({
            'sku': sku, 'line': line, 'title': p.get('title'), 'category': a['category'], 'pack': size,
            'pack_basis': basis, 'packs': a['units'], 'revenue': round(a['net_sales'], 2),
            'revenue_share': round(a['net_sales'] / total, 6) if total else None,
            'price_per_pack': round(per_pack, 2) if per_pack else None,
            'price_per_item': round(per_pack / size, 2) if per_pack and size else None,
            'list_per_item': round(p['price'] / size, 2) if p.get('price') and size else None})
    out = []
    for line, rs in sorted(lines.items(), key=lambda kv: -sum(r['revenue'] for r in kv[1])):
        rs.sort(key=lambda r: r['pack'] or 0)
        single = next((r for r in rs if r['pack'] == 1), None)
        prev = None
        for r in rs:
            bigger = (r['pack'] or 0) > 1  # two singles in a line are two products, not a rung
            r['drop_vs_single'] = (round(1 - r['price_per_item'] / single['price_per_item'], 4)
                                   if bigger and single and r['price_per_item'] else None)
            r['drop_vs_prev_rung'] = (round(1 - r['price_per_item'] / prev['price_per_item'], 4)
                                      if bigger and prev and (prev['pack'] or 0) < r['pack'] and r['price_per_item']
                                      and prev['price_per_item'] else None)
            if prev is None or (r['pack'] or 0) > (prev['pack'] or 0):
                prev = r
        out.extend(rs)
    by_size = {}
    for r in out:
        s = by_size.setdefault(r['pack'], {'pack': r['pack'], 'revenue': 0.0, 'packs': 0})
        s['revenue'] += r['revenue']
        s['packs'] += r['packs']
    sizes = [dict(s, revenue=round(s['revenue'], 2), revenue_share=round(s['revenue'] / total, 6) if total else None)
             for _, s in sorted(by_size.items(), key=lambda kv: kv[0] or 0)]
    multi = sum(s['revenue'] for s in sizes if (s['pack'] or 0) > 1)
    return {'unavailable': False, 'months': f'{full[0]} to {full[-1]}' if full else None, 'rows': out,
            'by_size': sizes, 'multi_share': round(multi / total, 6) if total else None,
            'basis': 'net sales over packs sold, 12 full months; price per pair is after discounts',
            'margin': 'unavailable: cost per SKU does not join to products yet'}


# ---------------------------------------------------------------- rules behind the desk lines, chart

def insights(th, months, findings):
    """The rules behind the insight cards. Each returns the sentence it produces and its capability."""
    out = []
    if th['unavailable']:
        out.append({'id': 'threshold', 'severity': 'medium', 'capability': 'MONEY-C05', 'autonomy': 'founder_gate',
                    'sentence': f'Free shipping economics are unavailable: {th["reason"]}.', 'rule': th['rule'] if 'rule' in th else ''})
    else:
        pull = th['share_just_over'] > th['share_just_under']
        s = (f'{th["share_just_over"] * 100:.1f} percent of orders land in the ${th["band"]} just over the ${th["threshold"]:,.0f} line '
             f'and {th["share_just_under"] * 100:.1f} percent in the ${th["band"]} just under. ')
        s += 'The line pulls baskets up. ' if pull else 'The line is not pulling baskets up. '
        if th['suggested']:
            s += f'It sits under the ${th["break_even"]:,.2f} break-even; ${th["suggested"]} would cover the label.'
        else:
            s += 'It sits at or over break-even.'
        stake = next((f['money_at_stake'] for f in findings if f['rule_id'] == 'OFFER-R01' and f['money_at_stake']), None)
        out.append({'id': 'threshold', 'severity': 'high' if th['suggested'] else 'info', 'capability': 'MONEY-C05',
                    'autonomy': 'founder_gate', 'sentence': s, 'rule': th['rule'],
                    'stub': (f'Model a move of the free shipping threshold from ${th["threshold"]:,.0f} to ${th["suggested"]} '
                             f'before any change: margin, AOV shift and orders now just under the new line '
                             f'({th["suggested_share_below_now"] * 100:.0f} percent of orders sit below ${th["suggested"]} today). '
                             + (f'Label cost on free orders under break-even: ${stake["usd"]:,.0f} in 28 days. ' if stake else '')
                             + 'Nothing on the store changes; your choice is logged.') if th['suggested'] else None})
    full = [m for m in (months or []) if m['full'] and m['discount_share'] is not None]
    rule = (f'discount share of gross, last full month against 3 months before; more than {CREEP_POINTS} points up is creep '
            f'(room spec: discount creep)')
    if len(full) < 4:
        out.append({'id': 'creep', 'severity': 'medium', 'capability': 'LIFE-C38', 'autonomy': 'founder_gate',
                    'sentence': 'Discount creep cannot be checked: fewer than 4 full months of data.', 'rule': rule})
    else:
        a, b = full[-4], full[-1]
        pts = (b['discount_share'] - a['discount_share']) * 100
        yoy = next((m for m in full if m['month'] == f'{int(b["month"][:4]) - 1}{b["month"][4:]}'), None)
        s = (f'Discounts were {a["discount_share"] * 100:.1f} percent of gross in {a["month"]} and '
             f'{b["discount_share"] * 100:.1f} percent in {b["month"]}. ')
        s += ('That is creep. ' if pts > CREEP_POINTS else 'No creep. ')
        if yoy:
            s += f'Same month last year: {yoy["discount_share"] * 100:.1f} percent.'
        out.append({'id': 'creep', 'severity': 'high' if pts > CREEP_POINTS else 'info',
                    'capability': 'LIFE-C38' if pts > CREEP_POINTS else None, 'autonomy': 'founder_gate', 'sentence': s,
                    'rule': rule})
    return out


def chart(months):
    if not months:
        return {'unavailable': True, 'reason': 'the monthly aggregate is missing', 'fix': 'shopify'}
    rows = months[-CHART_MONTHS:]
    return {'labels': [m['month'] for m in rows], 'aov': [m['aov'] for m in rows],
            'discount_share': [m['discount_share'] for m in rows],
            'partial': [m['month'] for m in rows if not m['full']], 'window': f'{len(rows)} months',
            'basis': 'AOV is net sales over orders; discount share is discounts over gross sales'}


def orientation(rd, th):
    """3 to 6 small numbers beside the plan (depth.md section 2). Null is unavailable with its reason."""
    aov = rd.m('aov', audit.WINDOW)
    code, _ = model.brain_value(rd, 'offers.promo_share_active_ads')
    code = code if isinstance(code, dict) else {}
    cm = model.contribution_28d(rd)
    months = [m for m in (discount_months(rd) or []) if m['full']]
    last = next((r for r in reversed(rd.table('monthly') or []) if r['month'] == months[-1]['month']), None) if months else None
    refunds = (round(last['refunds_on_orders'] / last['net_sales'], 6)
               if last and last.get('net_sales') and last.get('refunds_on_orders') is not None else None)
    return [
        {'label': 'AOV, 28 days', 'value': None if aov.get('unavailable') else aov['value'], 'unit': '$',
         'title': aov.get('reason') or 'net sales over orders, 28 days'},
        {'label': 'free shipping from', 'value': th.get('threshold'), 'unit': '$', 'title': 'brain offers record'},
        {'label': 'orders under it', 'value': th.get('share_below'), 'unit': '%',
         'title': 'share of orders below the threshold' if th.get('share_below') is not None else
         'unavailable: ' + str(th.get('reason') or 'order value bins need the orders table')},
        {'label': 'refunds, share of net', 'value': refunds, 'unit': '%',
         'title': f'refunds on orders over net sales, {months[-1]["month"]}' if refunds is not None else 'monthly aggregate missing'},
        {'label': 'ads with the code', 'value': (round(code['ads_with_code'] / code['active_ads'], 4)
                                                 if code.get('active_ads') else None), 'unit': '%',
         'title': f'{code.get("ads_with_code")} of {code.get("active_ads")} active ads carry the first-order code'
                  if code.get('active_ads') else 'no ad library record in the brain'},
        {'label': 'contribution margin', 'value': cm.get('value'), 'unit': '%',
         'tone': 'bad' if cm.get('value') is not None and cm.get('target') and cm['value'] * 100 < cm['target'] else None,
         'title': (f'after landed cost, fulfilment, fees and paid media, 28 days; target {cm["target"]:.0f} percent'
                   if cm.get('value') is not None and cm.get('target') else 'unavailable: ' + str(cm.get('reason')))},
    ]


def overview(data, brand):
    ends_on = audit.last_full_day(data, brand)
    rd = audit.Reader(data, brand, ends_on)
    b = rd.source.brand
    head = {'brand': b.get('brand'), 'name': b.get('name'), 'as_of': b.get('as_of'),
            'simulated': bool(b.get('simulated') or b.get('fictional')), 'market': b.get('market')}
    if brand:
        ranked = actions.rank(brand, {'ends_on': ends_on.isoformat()})
        findings, plan = ranked['findings'], ranked['actions']
        objections, returns = ranked['objections'], ranked['returns']
    else:
        findings, plan = audit.run(brand, {'ends_on': ends_on.isoformat()}, data=data), []
        objections, returns = [], {'unavailable': True, 'reason': 'no brand folder', 'groups': []}
    months = discount_months(rd)
    th = threshold(rd)
    return {'brand': head, 'window': {'ends_on': ends_on.isoformat(), 'days': audit.WINDOW},
            'orientation': orientation(rd, th), 'plan': plan,
            'stack': offer_stack(rd), 'threshold': th, 'bfcm': bfcm(rd), 'ladder': ladder(rd),
            'objections': objections, 'returns': returns, 'creep': insights(th, months, findings)[1], 'chart': chart(months),
            'findings': findings, 'rules': audit.RULES}


def rank(brand='bombas', window=None):
    """Ranked actions for app/rank.py and the master list (depth.md section 5)."""
    out = actions.rank(brand, window)
    for k in ('findings', 'objections', 'returns'):
        out.pop(k, None)
    return out


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
        if req.path == ['rank'] and brand:
            return rank(brand, {'ends_on': req.arg('ends_on')} if req.arg('ends_on') else None)
        if req.path == ['findings']:
            return {'findings': audit.run(brand, None, data=data), 'rules': audit.RULES}
    except ValueError as exc:
        return 400, {'error': str(exc)}
    return 404, {'error': 'not found', 'routes': ['overview', 'findings', 'rank']}
