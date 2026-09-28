"""Offer economics for screen 04: window totals from the daily aggregate, landed cost per unit from finance_inputs,
and the per-order money of an offer from price down to contribution.

Shared by audit.py (rules) and api.py (the plan and the desk). Every number is arithmetic on the brand's tables,
finance_inputs and brain records. A missing input makes the step unavailable (None) with the field it waits for;
nothing is filled with a default or an industry average.
"""
import calendar
import math
import re
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
    full = full_months(rd, rd.ends_on, months)
    products = {p['sku']: p for p in (rd.table('products') or []) if p.get('sku')}
    cogs = cogs_by_sku(rd, rd.ends_on)
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
            'list_per_item': round(p['price'] / size, 2) if p.get('price') and size else None,
            'cogs_per_pack': cogs.get(sku), 'margin_per_pack': round(per_pack - cogs[sku], 2) if per_pack and sku in cogs else None,
            'margin_per_item': round((per_pack - cogs[sku]) / size, 2) if per_pack and size and sku in cogs else None})
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
            'basis': 'net sales over packs sold, 12 full months; price per item is after discounts',
            'margin': ('margin per pack is price paid minus cogs_landed in force today' if cogs else
                       'unavailable: no cogs_landed keyed by SKU'),
            'lines': line_summary(out)}


def line_summary(rows):
    """One row per product line: its rungs, the single's share of the line's packs, the deepest saving per item,
    and the margin per order of the single and of the best-selling multi-pack."""
    lines = {}
    for r in rows:
        lines.setdefault(r['line'], []).append(r)
    out = []
    for line, rs in lines.items():
        packs = sum(r['packs'] for r in rs)
        single = next((r for r in rs if r['pack'] == 1), None)
        multis = [r for r in rs if (r['pack'] or 0) > 1]
        top = max(multis, key=lambda r: r['packs']) if multis else None
        out.append({'line': line, 'category': rs[0]['category'], 'rungs': [r['pack'] for r in rs],
                    'packs': packs, 'revenue': round(sum(r['revenue'] for r in rs), 2),
                    'single_sku': single['sku'] if single else None, 'pack_sku': top['sku'] if top else None,
                    'pack': top['pack'] if top else None,
                    'single_share': round(single['packs'] / packs, 4) if single and packs else None,
                    'single_packs': single['packs'] if single else None,
                    'saving': top['drop_vs_single'] if top else None,
                    'single_per_item': single['price_per_item'] if single else None,
                    'pack_per_item': top['price_per_item'] if top else None,
                    'single_margin': single['margin_per_pack'] if single else None,
                    'pack_margin': top['margin_per_pack'] if top else None,
                    'pack_price': top['price_per_pack'] if top else None,
                    'single_cogs': single['cogs_per_pack'] if single else None,
                    'pack_cogs': top['cogs_per_pack'] if top else None})
    out.sort(key=lambda r: -r['revenue'])
    return out




# ---------------------------------------------------------------- first-order offer

def first_order_options(rd, options, pack=None, end=None):
    """Per-order money of each first-order offer at the average list-price order: price paid, extra cost, label net
    of shipping charged (the free shipping line counts after discount), contribution before media and payback on
    the paid media spent per new customer. Returns dict with the inputs and rows, or dict(unavailable, reason)."""
    end = end or rd.ends_on
    t = window_totals(rd, end)
    po = per_order(t)
    cr = cogs_ratio(rd, end)
    code, _ = brain_value(rd, 'offers.first_order_code')
    thr, _ = brain_value(rd, 'offers.free_shipping_threshold_usd')
    ship, _ = brain_value(rd, 'offers.standard_shipping_cost')
    rate = (ship or {}).get('cost_usd') if isinstance(ship, dict) else None
    pct_off = (code or {}).get('discount_pct') if isinstance(code, dict) else None
    label = label_average(rd, end)
    pick = fin_value(rd, 'threepl_pick_pack', end, unit='usd_per_order')
    pick_unit = fin_value(rd, 'threepl_pick_pack', end, unit='usd_per_unit')
    pack_fee = fin_value(rd, 'packaging', end)
    fee_pct = fin_value(rd, 'payment_fee_percent', end, 'online_store')
    fee_fix = fin_value(rd, 'payment_fee_fixed', end, 'online_store')
    ic = item_cost(rd, end)
    need = {'daily aggregate': po, 'cogs_landed': cr.get('ratio'), 'first-order code in the brain': pct_off,
            'free shipping threshold in the brain': thr, 'shipping rate in the brain': rate, 'shipping_label': label,
            'threepl_pick_pack': pick, 'packaging': pack_fee, 'payment fees': fee_pct if fee_fix is not None else None,
            'item cost': ic.get('value')}
    miss = [k for k, v in need.items() if v is None]
    if miss:
        return {'unavailable': True, 'reason': 'missing ' + ', '.join(miss)}
    g = po['gross']
    cogs = cr['ratio'] * po['net']
    units = po['units']
    new_cac = t['spend'] / t['new_customer_orders'] if t['new_customer_orders'] else None
    target_cac = fin_value(rd, 'target_cac', end)
    dollar_off = math.ceil(g * pct_off / 100 / 2 / 5) * 5

    def money(price, extra_item=0.0, extra_units=0):
        # the average order ships free; the label stays with the brand so offers compare on price and item cost.
        # An offer that takes the basket under the line is flagged: the shopper then pays shipping or adds an item.
        cost = (cogs + extra_item + pack_fee + pick + (pick_unit or 0) * max(units - 1 + extra_units, 0)
                + price * fee_pct / 100 + fee_fix + label)
        c = price - cost
        return {'price_paid': round(price, 2), 'under_line': price < thr, 'extra_item': round(extra_item, 2),
                'contribution': round(c, 2), 'payback': round(c / new_cac, 2) if new_cac else None}

    base = money(g)
    rows = []
    for o in options:
        k = o['key']
        if k == 'code':
            m = money(g * (1 - pct_off / 100))
            m['terms'] = f'{pct_off:.0f} percent off the first order'
        elif k == 'gwp':
            m = money(g, extra_item=ic['value'], extra_units=1)
            m['terms'] = 'one free item in the box (median landed cost per item)'
        elif k == 'free_ship':
            # costs the label only on first orders under the line; their share needs order rows
            dist = rd.m('order_value_distribution', WINDOW, end, step=5)
            if dist.get('unavailable'):
                rows.append(dict(o, unavailable=True, terms='no shipping charge on the first order, any value',
                                 reason='the share of first orders under the line needs order rows'))
                continue
            under = sum(x['share'] for x in dist['groups'] if x['to'] <= thr)
            m = money(g)
            m['contribution'] = round(m['contribution'] - under * (rate - 0), 2)
            m['payback'] = round(m['contribution'] / new_cac, 2) if new_cac else None
            m['terms'] = f'no shipping charge on the first order; {under * 100:.0f} percent of orders sit under the line'
        elif k == 'dollar_off':
            m = money(g - dollar_off if g >= thr else g)
            m['terms'] = f'${dollar_off} off a first order of ${thr:,.0f} or more'
        elif k == 'pack':
            if not pack or pack.get('pack_price') is None:
                rows.append(dict(o, unavailable=True, reason='no multi-pack in the catalogue'))
                continue
            cut = round(pack['pack_price'] * 0.15, 2)
            m = money(g - cut)
            m['terms'] = f'15 percent off the {pack["pack"]}-pack ({pack["line"]}) on the first order'
        m['cost'] = round(base['contribution'] - m['contribution'], 2)
        rows.append(dict(o, **m))
    code_row = next((r for r in rows if r['key'] == 'code' and not r.get('unavailable')), None)
    for r in rows:
        if r.get('unavailable') or not code_row or r['key'] == 'code':
            continue
        # how much first-order conversion this offer can lose against the code before it earns less per visitor
        r['cvr_limit'] = round(1 - code_row['contribution'] / r['contribution'], 4) if r['contribution'] > code_row['contribution'] else None
    keep = [r for r in rows if not r.get('unavailable') and r['keeps_price']]
    best = max(keep, key=lambda r: r['contribution']) if keep else None
    better = best if best and code_row and best['contribution'] > code_row['contribution'] else None
    return {'unavailable': False, 'best_key': better['key'] if better else None,
            'best_gain': round(better['contribution'] - code_row['contribution'], 2) if better else None,
            'new_discounts_28d': round(t['discounts'] * po['new_share'], 2),
            'gross_order': round(g, 2), 'net_order': round(po['net'], 2), 'cogs': round(cogs, 2),
            'threshold': thr, 'shipping_rate': rate, 'code_pct': pct_off, 'new_cac': round(new_cac, 2) if new_cac else None,
            'target_cac': target_cac, 'full_price': base, 'rows': rows,
            'new_orders_28d': t['new_customer_orders'], 'discounts_28d': round(t['discounts'], 2),
            'new_share': round(po['new_share'], 4), 'window': {'start': t['start'], 'end': t['end']},
            'basis': ('The average order at list price, 28 days; landed cost from the cogs ratio; the label stays with '
                      'the brand. The line counts after discount: an offer that takes the basket under it is flagged, '
                      'because the shopper then pays shipping or adds an item')}


# ---------------------------------------------------------------- margin waterfall per offer

def waterfall(rd, list_price, discount=0.0, cogs=None, units=1.0, extra_item=0.0, extra_units=0, ships_free=True,
              shipping_charged=0.0, media=None, claim=None, end=None):
    """One order from list price down to contribution after media. Each step is a cost from finance_inputs or a
    brain model rate, named with its source. A missing input makes its step and every total after it unavailable.
    claim: (rate, cost per claim) for a promise that adds claims on top of the modelled returns."""
    end = end or rd.ends_on
    price = list_price - discount
    rm, rm_rec = brain_value(rd, 'economics.return_share_model')
    rm = rm if isinstance(rm, dict) else {}
    refund = (rm.get('refund_pct') or 0) / 100 if rm else None
    replace = (rm.get('replacement_under_guarantee_pct') or 0) / 100 if rm else None
    proc = fin_value(rd, 'returns_processing', end)
    repl = claim_cost(rd, 'replacement', end).get('value')
    label = label_average(rd, end)
    pick = fin_value(rd, 'threepl_pick_pack', end, unit='usd_per_order')
    pick_unit = fin_value(rd, 'threepl_pick_pack', end, unit='usd_per_unit') or 0
    pack = fin_value(rd, 'packaging', end)
    fee_pct = fin_value(rd, 'payment_fee_percent', end, 'online_store')
    fee_fix = fin_value(rd, 'payment_fee_fixed', end, 'online_store')

    def v(x, *parts):
        return None if x is None or any(p is None for p in parts) else round(x, 2)

    steps = [{'label': 'List price', 'value': round(list_price, 2), 'kind': 'total', 'source': 'order'},
             {'label': 'Discount', 'value': round(discount, 2), 'kind': 'down', 'source': 'offer'},
             {'label': 'Landed cost', 'value': v((cogs or 0) + extra_item, cogs), 'kind': 'down', 'source': 'finance_inputs.cogs_landed'},
             {'label': 'Pick, pack, box', 'value': v((pick or 0) + (pack or 0) + pick_unit * max(units - 1 + extra_units, 0), pick, pack),
              'kind': 'down', 'source': 'finance_inputs.threepl_pick_pack, packaging'},
             {'label': 'Shipping, net', 'value': v((label or 0) - (0 if ships_free else shipping_charged), label), 'kind': 'down',
              'source': 'finance_inputs.shipping_label'},
             {'label': 'Payment fee', 'value': v(price * (fee_pct or 0) / 100 + (fee_fix or 0), fee_pct, fee_fix), 'kind': 'down',
              'source': 'finance_inputs.payment_fee_*'},
             {'label': 'Returns', 'value': v(price * (refund or 0) + (refund or 0) * (proc or 0) + (replace or 0) * (repl or 0), refund, proc, repl),
              'kind': 'down', 'source': (rm_rec or {}).get('id') or 'economics.return_share_model (missing)'}]
    if claim:
        rate, cost = claim
        steps.append({'label': 'Promise claims', 'value': v((rate or 0) * (cost or 0), rate, cost), 'kind': 'down', 'source': 'playbook claim cost'})
    before = None if any(s['value'] is None for s in steps) else round(price - sum(s['value'] for s in steps[2:]), 2)
    steps.append({'label': 'Before media', 'value': before, 'kind': 'sub', 'source': 'computed'})
    steps.append({'label': 'Paid media', 'value': v(media, media), 'kind': 'down', 'source': 'daily spend'})
    after = None if before is None or media is None else round(before - media, 2)
    steps.append({'label': 'Contribution', 'value': after, 'kind': 'total', 'source': 'computed'})
    target = fin_value(rd, 'target_contribution_margin', end)
    share = round(after / price, 4) if after is not None and price else None
    return {'steps': steps, 'price_paid': round(price, 2), 'before_media': before, 'contribution': after,
            'contribution_share': share, 'red_line': target / 100 if target is not None else None,
            'clears': None if share is None or target is None else share >= target / 100,
            'missing': [s['label'] for s in steps if s['value'] is None]}
