"""Offer economics for screen 04: window totals from the daily aggregate, landed cost per unit from finance_inputs,
and the per-order money of an offer from price down to contribution.

Shared by audit.py (rules) and api.py (the plan and the desk). Every number is arithmetic on the brand's tables,
finance_inputs and brain records. A missing input makes the step unavailable (None) with the field it waits for;
nothing is filled with a default or an industry average.
"""
import calendar
import math
from datetime import date, timedelta

WINDOW = 28
SPEND_KEYS = ('meta_spend', 'google_spend', 'other_paid_spend')
SUM_KEYS = ('orders', 'web_orders', 'new_customer_orders', 'returning_customer_orders', 'net_sales', 'gross_sales',
            'discounts', 'shipping', 'units', 'refunds_on_orders') + SPEND_KEYS


def window_totals(rd, end=None, days=WINDOW):
    """Sums of the daily aggregate over the `days` ending on `end`. None when a day is missing."""
    end = end or rd.ends_on
    rows = rd.table('daily') or []
    by = {r['date']: r for r in rows}
    days_list = [(end - timedelta(days=i)).isoformat() for i in range(days)]
    if any(d not in by for d in days_list):
        return None
    out = {k: 0.0 for k in SUM_KEYS}
    for d in days_list:
        r = by[d]
        for k in SUM_KEYS:
            v = r.get(k)
            if v is None and k in SPEND_KEYS:
                continue
            if v is None:
                return None
            out[k] += v
    out['spend'] = sum(out[k] for k in SPEND_KEYS)
    out['start'], out['end'], out['days'] = days_list[-1], days_list[0], days
    return out


def per_order(t):
    """Average order money from window totals."""
    if not t or not t['orders']:
        return None
    o = t['orders']
    return {'gross': t['gross_sales'] / o, 'discount': t['discounts'] / o, 'net': t['net_sales'] / o,
            'units': t['units'] / o, 'shipping_charged': t['shipping'] / o, 'spend': t['spend'] / o,
            'new_share': t['new_customer_orders'] / o}


def full_months(rd, upto=None, n=3):
    """The last `n` full months in the monthly aggregate ending on or before `upto`'s month."""
    rows = rd.table('monthly') or []
    out = []
    for r in rows:
        y, m = map(int, r['month'].split('-'))
        if r.get('days') == calendar.monthrange(y, m)[1] and (upto is None or r['month'] <= upto.strftime('%Y-%m')):
            out.append(r['month'])
    return out[-n:]


def cogs_by_sku(rd, day):
    f = rd.fin()
    if not f:
        return {}
    return {str(r['scope_key']): float(r['value']) for r in f.in_force('cogs_landed', day.isoformat())}


def cogs_ratio(rd, end=None, months=3):
    """Landed cost over net sales from products_monthly and cogs_landed, last `months` full months.
    Returns dict(ratio, per_unit, covered, skus, missing, months) or dict(ratio=None, reason, fix)."""
    end = end or rd.ends_on
    ms = full_months(rd, end, months)
    rows = [r for r in (rd.table('products_monthly') or []) if r['month'] in ms]
    if not rows:
        return {'ratio': None, 'reason': 'the products_monthly aggregate is missing', 'fix': 'shopify'}
    cogs = cogs_by_sku(rd, end)
    if not cogs:
        return {'ratio': None, 'reason': 'no cogs_landed in finance_inputs', 'fix': 'finance_inputs.cogs_landed'}
    skus = sorted({r['sku'] for r in rows})
    missing = [s for s in skus if s not in cogs]
    cost = net = units = 0.0
    for r in rows:
        if r['sku'] in cogs:
            cost += cogs[r['sku']] * (r['units'] or 0)
            net += r['net_sales'] or 0
            units += r['units'] or 0
    if not net:
        return {'ratio': None, 'reason': 'no net sales on SKUs with a landed cost', 'fix': 'finance_inputs.cogs_landed'}
    return {'ratio': round(cost / net, 6), 'per_unit': round(cost / units, 4) if units else None,
            'covered': len(skus) - len(missing), 'skus': len(skus), 'missing': missing,
            'months': f'{ms[0]} to {ms[-1]}' if ms else None}


def fin_value(rd, field, day, key=None, unit=None):
    f = rd.fin()
    return f.value(field, day.isoformat(), key, unit) if f else None


def brain_value(rd, key):
    rec = rd.record(f'{rd.brand}.{key}') if rd.brand else None
    return (rec or {}).get('value'), rec


def label_average(rd, day, carrier='usps'):
    f = rd.fin()
    if not f:
        return None
    rows = [r for r in f.in_force('shipping_label', day.isoformat()) if str(r.get('scope_key') or '').startswith(carrier)]
    return round(sum(float(r['value']) for r in rows) / len(rows), 4) if rows else None


def contribution_28d(rd, end=None):
    """Contribution margin of the average order over 28 days: net minus landed cost, fulfilment, payment fees,
    returns processing and paid media. Returns dict with the steps, or dict(value=None, reason, fix)."""
    end = end or rd.ends_on
    t = window_totals(rd, end)
    po = per_order(t)
    if not po:
        return {'value': None, 'reason': 'the daily aggregate does not cover 28 days', 'fix': 'shopify'}
    cr = cogs_ratio(rd, end)
    if cr['ratio'] is None:
        return {'value': None, 'reason': cr['reason'], 'fix': cr['fix']}
    steps = order_steps(rd, end, po['net'], po['units'], free_shipping=None, shipping_charged=po['shipping_charged'],
                        cogs=cr['ratio'] * po['net'])
    missing = [s['label'] for s in steps if s['value'] is None]
    if missing:
        return {'value': None, 'reason': 'missing ' + ', '.join(missing), 'fix': 'finance_inputs'}
    before_media = po['net'] - sum(s['value'] for s in steps)
    after = before_media - po['spend']
    return {'value': round(after / po['net'], 6), 'per_order': round(after, 2), 'before_media': round(before_media, 2),
            'before_media_share': round(before_media / po['net'], 6), 'net': round(po['net'], 2),
            'spend_per_order': round(po['spend'], 2), 'window': {'start': t['start'], 'end': t['end']},
            'target': fin_value(rd, 'target_contribution_margin', end)}


def order_steps(rd, day, net, units, free_shipping, shipping_charged=None, cogs=None, returns_rate=None):
    """Cost steps for one order after its price: landed cost, packaging, pick and pack, label, payment fee,
    returns processing. free_shipping True means the brand pays the label with no shipping charged; None means
    use the charged shipping on the average order (label minus what the shopper paid)."""
    label = label_average(rd, day)
    pack = fin_value(rd, 'packaging', day)
    pick = fin_value(rd, 'threepl_pick_pack', day, unit='usd_per_order')
    pick_unit = fin_value(rd, 'threepl_pick_pack', day, unit='usd_per_unit')
    fee_pct = fin_value(rd, 'payment_fee_percent', day, 'online_store')
    fee_fix = fin_value(rd, 'payment_fee_fixed', day, 'online_store')
    proc = fin_value(rd, 'returns_processing', day)
    steps = [{'key': 'cogs', 'label': 'Landed cost', 'value': None if cogs is None else round(cogs, 2),
              'source': 'finance_inputs.cogs_landed'},
             {'key': 'packaging', 'label': 'Packaging', 'value': pack, 'source': 'finance_inputs.packaging'},
             {'key': 'pick_pack', 'label': 'Pick and pack',
              'value': None if pick is None else round(pick + (pick_unit or 0) * max(units - 1, 0), 2),
              'source': 'finance_inputs.threepl_pick_pack'}]
    if label is None:
        ship = None
    elif free_shipping is True:
        ship = label
    elif free_shipping is False:
        ship = label - (shipping_charged or 0)
    else:
        ship = label - (shipping_charged or 0)
    steps.append({'key': 'label', 'label': 'Shipping label, net of shipping charged', 'value': None if ship is None else round(ship, 2),
                  'source': 'finance_inputs.shipping_label'})
    fee = None if fee_pct is None or fee_fix is None else round(net * fee_pct / 100 + fee_fix, 2)
    steps.append({'key': 'payment', 'label': 'Payment fee', 'value': fee, 'source': 'finance_inputs.payment_fee_*'})
    if returns_rate is not None:
        steps.append({'key': 'returns', 'label': 'Returns processing', 'value': None if proc is None else round(returns_rate * proc, 2),
                      'source': 'finance_inputs.returns_processing'})
    return steps


def item_cost(rd, day=None):
    """Median landed cost of one item (a pair, one garment) across SKUs: cogs_landed over the pack size in the SKU."""
    import re
    import statistics
    day = day or rd.ends_on
    cogs = cogs_by_sku(rd, day)
    per = []
    for sku, c in cogs.items():
        m = re.search(r'-(\d+)$', sku)
        if m and int(m.group(1)) > 0:
            per.append(c / int(m.group(1)))
    if not per:
        return {'value': None, 'reason': 'no cogs_landed keyed by SKU', 'fix': 'finance_inputs.cogs_landed'}
    return {'value': round(statistics.median(per), 2), 'skus': len(per),
            'basis': f'median landed cost per item across {len(per)} SKUs (cogs_landed over pack size)'}


def claim_cost(rd, kind, day=None):
    """Cost of one claim on a promise, from finance_inputs. kind: replacement, exchange or none."""
    day = day or rd.ends_on
    if kind == 'none':
        return {'value': 0.0, 'parts': [], 'basis': 'proof on a page or listing; no cost per order'}
    label = label_average(rd, day)
    pick = fin_value(rd, 'threepl_pick_pack', day, unit='usd_per_order')
    pack = fin_value(rd, 'packaging', day)
    parts = [('outbound label', label, 'finance_inputs.shipping_label'), ('pick and pack', pick, 'finance_inputs.threepl_pick_pack'),
             ('packaging', pack, 'finance_inputs.packaging')]
    if kind == 'replacement':
        ic = item_cost(rd, day)
        parts.insert(0, ('item', ic['value'], ic.get('basis') or 'finance_inputs.cogs_landed'))
    else:
        parts.insert(0, ('returns processing', fin_value(rd, 'returns_processing', day), 'finance_inputs.returns_processing'))
    missing = [p[0] for p in parts if p[1] is None]
    out = {'parts': [{'label': p[0], 'value': p[1], 'source': p[2]} for p in parts]}
    if missing:
        out.update(value=None, reason='missing ' + ', '.join(missing), fix='finance_inputs')
    else:
        out.update(value=round(sum(p[1] for p in parts), 2))
    return out


def contribution_free(rd, day, value, units):
    """Contribution before media of one order of `value` that ships free: value minus landed cost (cogs ratio),
    packaging, pick and pack, payment fee and the label. None with the missing input when one is absent."""
    cr = cogs_ratio(rd, day)
    if cr['ratio'] is None:
        return None, cr['reason']
    steps = order_steps(rd, day, value, units, free_shipping=True, cogs=cr['ratio'] * value)
    miss = [s['label'] for s in steps if s['value'] is None]
    if miss:
        return None, 'missing ' + ', '.join(miss)
    return round(value - sum(s['value'] for s in steps), 2), None


def threshold_scenarios(rd, threshold, ship_rate, break_even, units, groups=None, orders_28d=None, step=5, span=2):
    """What each nearby free shipping line must achieve to pay. For a higher line: the share of orders in the band
    between the lines that can walk away before the move loses money (the rest pay shipping). For a lower line: the
    rise in orders in the band needed to pay for the shipping no longer charged. Midpoint order of each band."""
    day = rd.ends_on
    cands = sorted({threshold + step * k for k in range(-span, span + 1)} |
                   ({math.ceil(break_even / step) * step} if break_even else set()))
    out = []
    for c in cands:
        row = {'threshold': c, 'current': c == threshold, 'covers_break_even': bool(break_even and c >= break_even)}
        if c == threshold:
            row['text'] = 'Today.'
            out.append(row)
            continue
        lo, hi = (threshold, c) if c > threshold else (c, threshold)
        mid = (lo + hi) / 2
        cf, why = contribution_free(rd, day, mid, units)
        row.update({'band': [lo, hi], 'mid_order': mid, 'contribution_free': cf})
        share = None
        if groups:
            share = round(sum(g['share'] for g in groups if g['from'] >= lo and g['to'] <= hi), 6)
        row['band_share'] = share
        row['band_orders_28d'] = round(share * orders_28d) if share is not None and orders_28d else None
        if cf is None or ship_rate is None:
            row.update({'limit': None, 'text': 'unavailable: ' + (why or 'no shipping rate in the brain')})
        elif c > threshold:
            lim = ship_rate / (ship_rate + cf)
            row.update({'kind': 'raise', 'limit': round(lim, 4),
                        'text': f'Pays if fewer than {lim * 100:.0f} percent of orders between ${lo:,.0f} and ${hi:,.0f} walk away.'})
        else:
            need = ship_rate / cf
            row.update({'kind': 'lower', 'limit': round(need, 4),
                        'text': f'Pays only if orders between ${lo:,.0f} and ${hi:,.0f} rise {need * 100:.0f} percent.'})
        out.append(row)
    return out
