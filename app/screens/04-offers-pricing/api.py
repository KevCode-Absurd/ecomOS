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
import json
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


def _approvals():
    name = 'offers_pricing_approvals'
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, HERE / 'approvals.py')
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


approvals = _approvals()
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

def _month_ends(end, n=13):
    out, y, m = [], end.year, end.month
    for _ in range(n):
        last = date(y, m, calendar.monthrange(y, m)[1])
        if last <= end:
            out.append(last)
        m -= 1
        if m == 0:
            y, m = y - 1, 12
    return sorted(out)[-12:]


def threshold(rd):
    """Free shipping line: break-even and its trend, the order value bins (or a labelled fixture), the orders just
    under and over, what each nearby line must achieve to pay, and the rule."""
    t, rec = audit.threshold_usd(rd)
    be = audit.break_even(rd, rd.ends_on)
    dist = rd.m('order_value_distribution', audit.WINDOW, step=5)
    rate = (model.brain_value(rd, 'offers.standard_shipping_cost')[0] or {}).get('cost_usd') if rd.brand else None
    out = {'threshold': t, 'threshold_source': (rec or {}).get('source'), 'break_even': be.get('value'),
           'break_even_inputs': {k: be.get(k) for k in ('aov', 'label', 'gross_margin', 'label_rows')},
           'break_even_formula': 'AOV + average label / gross margin (room spec free_shipping_threshold_breakeven)',
           'margin_basis': 'target gross margin from finance_inputs', 'shipping_listed': rate,
           'unavailable': t is None or be.get('value') is None,
           'reason': None if t is not None else 'no threshold in the brain'}
    if out['unavailable']:
        out['reason'] = out['reason'] or be.get('reason')
        out['fix'] = be.get('fix')
        return out
    band = audit.BAND_USD
    out['trend'] = [{'month': d.strftime('%Y-%m'), 'break_even': audit.break_even(rd, d).get('value'), 'threshold': t}
                    for d in _month_ends(rd.ends_on)]
    fixture = bool(dist.get('unavailable'))
    if fixture:
        fx = json.loads((HERE / 'fixtures' / 'order_value_distribution.json').read_text(encoding='utf-8'))
        groups = fx['groups']
        out.update({'distribution_unavailable': dist.get('reason'), 'fix': dist.get('fix'), 'fixture_note': fx['note'],
                    'fixture_threshold': fx.get('threshold_in_fixture')})
    else:
        groups = dist['groups']
    ft = out.get('fixture_threshold') or t  # a fixture is drawn around its own line
    lo, hi = max(0, ft - 40), ft + 60
    out.update({
        'fixture': fixture, 'band': band,
        'bins': [dict(g, share_paid=round(g['share'] * g['paid_shipping_orders'] / g['orders'], 6) if g['orders'] else None,
                      share_free=round(g['share'] * (1 - g['paid_shipping_orders'] / g['orders']), 6) if g['orders'] else None)
                 for g in groups if lo <= g['from'] < hi],
        'shade': [ft - band, ft], 'window': (dist.get('window') or {}), 'basis': dist.get('basis'),
        'orders_sample': None if fixture else dist['value'],
        'share_just_under': None if fixture else audit.band_share(groups, t - band, t),
        'share_just_over': None if fixture else audit.band_share(groups, t, t + band),
        'share_below': None if fixture else audit.band_share(groups, 0, t),
        'above_aov': round(t / be['aov'] - 1, 4), 'gap': round(be['value'] - t, 2), 'suggested': math.ceil(be['value'] / 5) * 5 if t < be['value'] else None,
        'rule': (f'Move when the threshold is under break-even (suggest break-even rounded up to $5). A threshold '
                 f'that works shows more orders in the ${band} just over it than the ${band} just under it.'),
    })
    if not fixture:
        out['share_ship_free'] = round(1 - out['share_below'], 6)
    units = (model.per_order(model.window_totals(rd)) or {}).get('units') or 1
    out['scenarios'] = model.threshold_scenarios(rd, t, rate, be['value'], units, None if fixture else groups,
                                                 be.get('orders'))
    out['scenario_rule'] = ('A higher line: the rest of the orders between the lines pay the listed shipping rate, so the '
                            'move pays while fewer walk away than the limit. A lower line: those orders stop paying '
                            'shipping, so it pays only if orders in the band rise by the limit. Midpoint order, '
                            'contribution before media from finance inputs.')
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

def ladder(rd, months=12):
    return model.ladder(rd, months)


# ---------------------------------------------------------------- rules behind the desk lines, chart

def creep_rule(months):
    """Room spec discount creep: the sentence it produces and its capability."""
    full = [m for m in (months or []) if m['full'] and m['discount_share'] is not None]
    rule = (f'discount share of gross, last full month against 3 months before; more than {CREEP_POINTS} points up is creep '
            f'(room spec: discount creep)')
    if len(full) < 4:
        return {'id': 'creep', 'severity': 'medium', 'capability': 'LIFE-C38', 'autonomy': 'founder_gate',
                'sentence': 'Discount creep cannot be checked: fewer than 4 full months of data.', 'rule': rule}
    else:
        a, b = full[-4], full[-1]
        pts = (b['discount_share'] - a['discount_share']) * 100
        yoy = next((m for m in full if m['month'] == f'{int(b["month"][:4]) - 1}{b["month"][4:]}'), None)
        s = (f'Discounts were {a["discount_share"] * 100:.1f} percent of gross in {a["month"]} and '
             f'{b["discount_share"] * 100:.1f} percent in {b["month"]}. ')
        s += ('That is creep. ' if pts > CREEP_POINTS else 'No creep. ')
        if yoy:
            s += f'Same month last year: {yoy["discount_share"] * 100:.1f} percent.'
        return {'id': 'creep', 'severity': 'high' if pts > CREEP_POINTS else 'info',
                'capability': 'LIFE-C38' if pts > CREEP_POINTS else None, 'autonomy': 'founder_gate', 'sentence': s,
                'rule': rule}


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


DESK_KEYS = ('objections', 'returns', 'ladder', 'first_order', 'waterfalls', 'calendar', 'gifting', 'guarantee', 'position',
             'parity', 'discipline', 'cart', 'tests', 'depth', 'cohorts', 'costs', 'registry', 'referral', 'loyalty',
             'subscription', 'bundles')


def with_decisions(acts, today=None, path=None):
    """depth.md rule 14: decisions from the log show on each move; 'not now' hides a move for 14 days.
    Returns (plan, snoozed) where snoozed lists the hidden moves with the day they come back."""
    rk = actions.RANK
    kw = {'path': path} if path else {}
    kept = rk.apply_decisions([dict(a) for a in acts], today=today, **kw)
    ids = {a['id'] for a in kept}
    dec = rk.decisions_by_finding(**kw)
    snoozed = []
    for a in acts:
        if a['id'] not in ids:
            d = dec.get(a['id']) or {}
            back = None
            try:
                back = (date.fromisoformat(str(d.get('time'))[:10]) + timedelta(days=rk.SNOOZE_DAYS)).isoformat()
            except ValueError:
                back = None
            snoozed.append({'id': a['id'], 'title': a['title'], 'back_on': back, 'reason': d.get('reason')})
    return kept, snoozed


def overview(data, brand):
    ends_on = audit.last_full_day(data, brand)
    rd = audit.Reader(data, brand, ends_on)
    b = rd.source.brand
    head = {'brand': b.get('brand'), 'name': b.get('name'), 'as_of': b.get('as_of'),
            'simulated': bool(b.get('simulated') or b.get('fictional')), 'market': b.get('market')}
    # one path for every brand: a brand folder, or a data source with no folder (the sample brand)
    ranked = actions.rank(brand, {'ends_on': ends_on.isoformat()}, data=None if brand else data)
    desk = {k: ranked[k] for k in DESK_KEYS}
    plan, snoozed = with_decisions(ranked['actions'])
    made = approvals.planned(rd) if brand else {}
    for a in plan:
        if a['id'] in made:
            a['plan_record'] = made[a['id']]
    planned = [a for a in plan if a.get('plan_record')]
    plan = [a for a in plan if not a.get('plan_record')]
    months = discount_months(rd)
    th = threshold(rd)
    return {'brand': head, 'window': {'ends_on': ends_on.isoformat(), 'days': audit.WINDOW},
            'orientation': orientation(rd, th), 'plan': plan, 'snoozed': snoozed,
            'planned': [{'id': a['id'], 'title': a['title'], 'kind': a['artefact']['kind'],
                         'can_launch': a['plan_record']['status'] == 'active' and a['artefact']['kind'] in approvals.OFFER_KINDS,
                         **a['plan_record']} for a in planned],
            'stack': offer_stack(rd), 'threshold': th, 'bfcm': bfcm(rd), **desk,
            'creep': creep_rule(months), 'chart': chart(months), 'findings': ranked['findings'], 'rules': audit.RULES}


def rank(brand='bombas', window=None):
    """Ranked actions for app/rank.py and the master list (depth.md section 5)."""
    out = actions.rank(brand, window)
    for k in ('findings',) + DESK_KEYS:
        out.pop(k, None)
    return out


def _brand(req):
    brand = req.arg('brand', DEFAULT_BRAND)
    if brand in ('', 'sample'):
        return None
    if not re.fullmatch(r'[a-z0-9-]{1,40}', brand):
        raise ValueError('brand must be a folder name like bombas')
    return brand


def approve(brand, body, brain_root=None, outbox=None, today=None):
    """POST approve {id, mode}: save one ranked move to the brain as a plan record (Brain.put) and propose its
    registry row. mode proposed (review queue) or founder (approved). Nothing else on the store changes."""
    body = body if isinstance(body, dict) else {}
    mode = body.get('mode') or 'proposed'
    if mode not in approvals.MODES:
        raise ValueError('mode must be proposed or founder')
    ranked = actions.rank(brand)
    act = next((a for a in ranked['actions'] if a['id'] == body.get('id')), None)
    if not act:
        raise ValueError('no open move with that id')
    if act.get('status') == 'unavailable':
        raise ValueError('a connect move is done in Setup, not saved as a plan')
    sf, _ = actions.surfaces(act)
    kw = {'brain_root': brain_root, 'today': today}
    if outbox:
        kw['outbox'] = outbox
    return approvals.save(brand, act, mode, sf, **kw)


def launched(brand, body, brain_root=None, today=None):
    """POST launched {id}: the approved offer is live; its offers record turns active from today."""
    body = body if isinstance(body, dict) else {}
    ranked = actions.rank(brand)
    act = next((a for a in ranked['actions'] if a['id'] == body.get('id')), None)
    if not act:
        raise ValueError('no move with that id')
    return approvals.launch(brand, act, brain_root=brain_root, today=today)


def handle(req):
    if req.method == 'POST' and req.path == ['launched']:
        try:
            brand = _brand(req)
            if not brand:
                return 400, {'error': 'launches need a brand folder'}
            out = launched(brand, req.body)
            return (400, out) if out['errors'] else out
        except ValueError as exc:
            return 400, {'error': str(exc)}
    if req.method == 'POST' and req.path == ['approve']:
        try:
            brand = _brand(req)
            if not brand:
                return 400, {'error': 'approvals need a brand folder'}
            out = approve(brand, req.body)
            return (400, out) if out['errors'] else out
        except ValueError as exc:
            return 400, {'error': str(exc)}
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
    return 404, {'error': 'not found', 'routes': ['overview', 'findings', 'rank', 'POST approve', 'POST launched']}
