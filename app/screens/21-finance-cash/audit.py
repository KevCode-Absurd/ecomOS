"""Finance and cash audit (screen 21, round 0). Findings in the shape of app/contracts/audit.md.

Every number is computed here in code from the brand's aggregates, data.sqlite, finance_inputs (app/data/finance.py)
and the brain (app/brain/store.py). No connector, no model call. Same tables, brain and window give the same findings.

How money is scaled. A brand folder keeps its aggregates at the brand's real size and may keep data.sqlite at a
smaller dev scale (0.1). Totals in dollars always come from the aggregates. data.sqlite only gives rates that hold at
any scale: cost per dollar of net revenue for fees, fulfillment and returns, and days of stock on hand.

Margin ladder (per month, used by the rules and by api.py)
  gross margin   (net sales - COGS) / net sales. Units and net sales by SKU from `products_monthly`; COGS is units
                 times `cogs_landed` in force, averaged over the month's days. A month with any day and SKU
                 without a cost row reads None, never 0.
  CM1            net revenue - COGS - payment fees (percent of order total plus fixed, per channel row)
  CM2            CM1 + shipping charged - fulfillment (packaging, pick and pack, mean USPS label; orders carry no
                 zone yet) - returns cost (returns x returns_processing, refunds, chargebacks not won)
  CM3            CM2 - paid media (`paid_media_monthly`, every platform). All paid spend is charged to the online
                 store, since retail (POS) orders have no card fee rows and read None.

Rules (the room spec's insight table, agents/rooms/rooms.json room "Finance and cash")
  FIN-R01  Margin leak by SKU. Units rose each of the last 3 full months while CM3 stayed negative in all 3.
           CM3 per SKU = net sales - COGS - net sales x (store cost rate after COGS + paid media rate), costs spread
           by revenue share. Money: last month's loss. Severity high when the loss grew, else medium; raised by
           the contract's stake bands. Capability MONEY-C02 (agent does). Owner: 21-finance-cash.
  FIN-R02  Cash below floor. The 13-week forecast low point under the brand's stated cash floor. Needs a bank
           ledger and a floor; unavailable until both exist. Severity critical. MONEY-C06. Owner: 21.
  FIN-R03  Promo missed break-even. Needs a pre-launch promo model; unavailable. Severity high. MONEY-C05. Owner: 21.
  FIN-R04  CAC payback outruns the cash cycle. Needs days payable outstanding (AP); unavailable. High. MONEY-C09.
  FIN-R05  Platform and books gap over 2 percent with no named cause. Needs finance_inputs.pnl_actual; unavailable.
           High. MONEY-C15. Owner: 21.
  FIN-R06  Payout deposit stuck past the source's SLA. `payouts` says what Shopify sent; a bank ledger says what
           landed. Unavailable without the ledger. High. MONEY-C52. Owner: 21.
  FIN-R07  COD remittance stuck. Markets IN only; a US brand emits nothing. High. MONEY-C52. Owner: 21.
  FIN-R08  Inventory cash overhang. Days of stock on hand (mean on_hand over the 28 days / units sold per day,
           data.sqlite `inventory` and order lines) over the SKU's supplier lead time (median eta - ordered_on in
           `inbound_pos`) plus 30 days. Money: excess days x full-scale COGS per day (last full month units from
           `products_monthly` x cost in force). That is cash tied up, not revenue lost, so severity stays the room's
           medium. Windows agree = trailing 28-day windows (of 4) that also sit over the line. MONEY-C07 (human
           assist). Owner: 21.
  FIN-R09  Subscription churn spike. Runs only when the data layer has `subscription_cohorts`; a store with no
           subscriptions emits nothing. High. MONEY-C18. Owner: 21.
  FIN-R10  Budget overrun over 10 percent by category. Needs `budget_annual`; unavailable. Medium. MONEY-C11.
  FIN-R11  Sales tax nexus crossed with no registration on file. Needs registrations (`sales_tax_filings`);
           unavailable. Critical. MONEY-C12 (human assist). Owner: 21.
"""
import calendar
import importlib.util
import json
import statistics
import sys
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parents[1]
SCREEN = '21-finance-cash'
WINDOW = 28
TRAILING = 4
OVERHANG_DAYS = 30            # room spec: DIO over lead time by more than 30 days
LABEL_CARRIER = 'usps'        # free standard shipping goes out on the ground carrier
FEE_CHANNEL = {'web': 'online_store'}   # Shopify order channel -> finance_inputs payment fee key
SHIPPED = ('web',)            # retail (POS) orders leave the store in hand: no label, packing or 3PL cost
PAID_STATES = ('paid', 'partially_refunded', 'refunded')
SEVERITY_ORDER = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}

CAPABILITY = {
    'FIN-R01': {'id': 'MONEY-C02', 'autonomy': 'agent_does'},
    'FIN-R02': {'id': 'MONEY-C06', 'autonomy': 'agent_does'},
    'FIN-R03': {'id': 'MONEY-C05', 'autonomy': 'founder_gate'},
    'FIN-R04': {'id': 'MONEY-C09', 'autonomy': 'agent_does'},
    'FIN-R05': {'id': 'MONEY-C15', 'autonomy': 'agent_does'},
    'FIN-R06': {'id': 'MONEY-C52', 'autonomy': 'agent_does'},
    'FIN-R07': {'id': 'MONEY-C52', 'autonomy': 'agent_does'},
    'FIN-R08': {'id': 'MONEY-C07', 'autonomy': 'human_assist'},
    'FIN-R09': {'id': 'MONEY-C18', 'autonomy': 'agent_does'},
    'FIN-R10': {'id': 'MONEY-C11', 'autonomy': 'agent_does'},
    'FIN-R11': {'id': 'MONEY-C12', 'autonomy': 'human_assist'},
}
RULES = [
    {'rule_id': 'FIN-R01', 'name': 'Margin leak by SKU', 'entity_type': 'sku',
     'inputs': ['products_monthly', 'finance_inputs.cogs_landed', 'orders', 'reversed_orders', 'paid_media_monthly']},
    {'rule_id': 'FIN-R02', 'name': 'Cash below floor', 'entity_type': 'metric',
     'inputs': ['bank_ledger', 'brain.finance.min_cash_floor', 'finance_inputs.cash_balance']},
    {'rule_id': 'FIN-R03', 'name': 'Promo missed break-even', 'entity_type': 'offer', 'inputs': ['promo_models', 'orders']},
    {'rule_id': 'FIN-R04', 'name': 'CAC payback outruns cash cycle', 'entity_type': 'metric',
     'inputs': ['accounts_payable', 'inventory', 'payouts', 'orders']},
    {'rule_id': 'FIN-R05', 'name': 'Platform and books gap unexplained', 'entity_type': 'metric',
     'inputs': ['finance_inputs.pnl_actual', 'orders', 'ad_rows', 'payouts']},
    {'rule_id': 'FIN-R06', 'name': 'Payout deposit stuck', 'entity_type': 'metric', 'inputs': ['payouts', 'bank_ledger']},
    {'rule_id': 'FIN-R07', 'name': 'COD remittance stuck', 'entity_type': 'metric', 'inputs': ['cod_remittance'],
     'markets': ['IN']},
    {'rule_id': 'FIN-R08', 'name': 'Inventory cash overhang', 'entity_type': 'sku',
     'inputs': ['inventory', 'inbound_pos', 'orders', 'products_monthly', 'finance_inputs.cogs_landed']},
    {'rule_id': 'FIN-R09', 'name': 'Subscription churn spike', 'entity_type': 'metric',
     'inputs': ['subscription_cohorts'], 'applies_to': 'subscription stores'},
    {'rule_id': 'FIN-R10', 'name': 'Budget overrun', 'entity_type': 'metric', 'inputs': ['budget_annual']},
    {'rule_id': 'FIN-R11', 'name': 'Sales tax nexus exposure', 'entity_type': 'metric',
     'inputs': ['orders.tax_lines', 'sales_tax_filings']},
]
for _r in RULES:
    _r['capability'] = CAPABILITY[_r['rule_id']]['id']
    _r['owner_screen'] = SCREEN

_MODS = {}
_CACHE = {}


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def finance_mod():
    if 'finance' not in _MODS:
        _MODS['finance'] = _load('ecomos_finance_21', APP / 'data' / 'finance.py')
    return _MODS['finance']


def brand_data(brand):
    if 'tables' not in _MODS:
        _MODS['tables'] = _load('ecomos_tables_21', APP / 'data' / 'tables.py')
    return _MODS['tables'].brand_data(brand)


def brain(brand):
    if not brand or not (APP / 'brain' / brand).is_dir():
        return None
    if 'store' not in _MODS:
        path = str(APP / 'brain')
        if path not in sys.path:
            sys.path.insert(0, path)  # store.py imports validate.py by name
        _MODS['store'] = _load('ecomos_brain_store_21', APP / 'brain' / 'store.py')
    return _MODS['store'].Brain(brand)


def r2(x):
    return None if x is None else round(x, 2)


def rate(num, den):
    return None if num is None or not den else round(num / den, 6)


def add(a, b):
    """None-propagating sum: a missing part makes the whole unknown, never a partial total."""
    return None if a is None or b is None else a + b


class Reader:
    """One brand and one window end. Tables through the data layer, finance_inputs through finance.py."""

    def __init__(self, data, brand, ends_on):
        self.brand, self.ends_on = brand, ends_on
        self.source = brand_data(brand) if brand else data
        self._brain = brain(brand)
        rows = self.finance_rows()
        self.fin = finance_mod().Finance(rows) if rows else None

    def table(self, name):
        try:
            return self.source.table(name)
        except (KeyError, ValueError):
            return None

    def has_table(self, name):
        return self.table(name) is not None

    def sql(self, query):
        """GROUP BY reads on data.sqlite. None when the brand has no row file."""
        fn = getattr(self.source, '_sql', None)
        if fn is None:
            return None
        try:
            return fn(query)
        except KeyError:
            return None

    def record(self, rid):
        return self._brain.get(rid) if self._brain else None

    def finance_rows(self):
        try:
            return self.source.table('finance_inputs')
        except (KeyError, ValueError):
            pass
        path = Path(getattr(self.source, 'folder', '') or '') / 'finance_inputs.json'
        if path.is_file():
            doc = json.loads(path.read_text(encoding='utf-8'))
            return doc.get('rows') if isinstance(doc, dict) else doc
        return None

    def target(self, field):
        v = self.fin.value(field, self.ends_on.isoformat()) if self.fin else None
        return None if v is None else round(v / 100, 6)

    def market(self):
        return (getattr(self.source, 'brand', None) or {}).get('market') or 'US'


def last_full_day(data, brand):
    source = brand_data(brand) if brand else data
    return date.fromisoformat(source.brand['as_of'])


# ---------------------------------------------------------------- months and costs

def month_days(rd):
    """The dates each month covers in the daily aggregate, up to the window end."""
    out = {}
    for r in rd.table('daily') or ():
        if r.get('date') and r['date'] <= rd.ends_on.isoformat():
            out.setdefault(r['date'][:7], []).append(r['date'])
    return out


def is_full(month, days):
    y, m = map(int, month.split('-'))
    return len(days) == calendar.monthrange(y, m)[1]


def unit_cost(rd, sku, days):
    """cogs_landed averaged over the days (units are monthly), or None when any day has no row."""
    if not rd.fin or not days:
        return None
    vals = [rd.fin.value('cogs_landed', d, sku) for d in days]
    return None if any(v is None for v in vals) else sum(vals) / len(vals)


def sku_months(rd):
    """Per month and SKU: units, net sales, unit cost and COGS (None when a cost row is missing)."""
    key = ('sku_months', id(rd.source), rd.ends_on)
    if key in _CACHE:
        return _CACHE[key]
    days = month_days(rd)
    out = {}
    for r in rd.table('products_monthly') or ():
        m = r.get('month')
        if m not in days or r.get('units') is None:
            continue
        cost = unit_cost(rd, r['sku'], days[m])
        out.setdefault(m, []).append({'sku': r['sku'], 'category': r.get('category'), 'units': r['units'],
                                      'net_sales': r.get('net_sales'), 'unit_cost': r2(cost),
                                      'cogs': None if cost is None else r2(cost * r['units'])})
    _CACHE[key] = out
    return out


def margin_months(rd):
    """Gross margin by month for store orders (web and retail), at the brand's real size."""
    days = month_days(rd)
    out = []
    for m, rows in sorted(sku_months(rd).items()):
        net = sum(r['net_sales'] or 0 for r in rows)
        missing = [r['sku'] for r in rows if r['cogs'] is None and r['units']]
        cogs = None if missing else sum(r['cogs'] or 0 for r in rows)
        out.append({'month': m, 'days': len(days[m]), 'full': is_full(m, days[m]), 'net_revenue': r2(net),
                    'units': sum(r['units'] for r in rows), 'cogs': r2(cogs),
                    'gross_margin': None if cogs is None else rate(net - cogs, net),
                    'costed_skus': len(rows) - len(missing), 'skus': len(rows),
                    'reason': None if not missing else
                    (f'no cost rows in force for {len(missing)} of {len(rows)} SKUs' if len(missing) < len(rows)
                     else 'no cost rows in force this month')})
    return out


def _label(rd, day):
    rows = [r for r in rd.fin.in_force('shipping_label', day) if str(r.get('scope_key') or '').startswith(LABEL_CARRIER)]
    return statistics.mean(float(r['value']) for r in rows) if rows else None


def order_months(rd):
    """Per month and store channel from data.sqlite: net revenue and every cost up to CM2, at the file's own scale.

    Costs use the finance_inputs rows in force on each order day. Any missing row makes that cost None for the
    month. Returns None when the brand has no data.sqlite."""
    key = ('order_months', id(rd.source), rd.ends_on)
    if key in _CACHE:
        return _CACHE[key]
    paid = "status IN ('paid', 'partially_refunded', 'refunded')"
    days = rd.sql(f"SELECT substr(created_at, 1, 10) AS d, channel, COUNT(*) AS orders, "
                  f"SUM(subtotal - discount) AS net, SUM(shipping) AS shipping, SUM(total) AS total, "
                  f"SUM(units) AS units FROM orders WHERE {paid} GROUP BY 1, 2")
    if days is None or not rd.fin:
        _CACHE[key] = None
        return None
    lines = rd.sql(f"SELECT substr(o.created_at, 1, 10) AS d, o.channel, l.sku, SUM(l.qty) AS qty "
                   f"FROM order_lines l JOIN orders o ON o.id = l.order_id WHERE o.{paid} GROUP BY 1, 2, 3")
    rev = rd.sql("SELECT substr(r.opened_at, 1, 10) AS d, o.channel, r.type, r.outcome, COUNT(*) AS n, "
                 "SUM(r.amount) AS amount FROM reversed_orders r JOIN orders o ON o.id = r.order_id GROUP BY 1, 2, 3, 4")
    end = rd.ends_on.isoformat()
    f = rd.fin
    acc = {}

    def slot(d, ch):
        return acc.setdefault((d[:7], ch), {'month': d[:7], 'channel': ch, 'orders': 0, 'net': 0.0, 'shipping': 0.0,
                                            'units': 0, 'cogs': 0.0, 'payment_fees': 0.0, 'fee_fixed': 0.0,
                                            'fulfillment': 0.0, 'returns_cost': 0.0,
                                            'first': d, 'last': d})

    for r in days:
        d, ch = r['d'], r['channel']
        if d > end:
            continue
        s = slot(d, ch)
        s['first'], s['last'] = min(s['first'], d), max(s['last'], d)
        s['orders'] += r['orders']
        s['net'] += r['net'] or 0
        s['shipping'] += r['shipping'] or 0
        s['units'] += r['units'] or 0
        fee_key = FEE_CHANNEL.get(ch, ch)
        pct, fixed = f.value('payment_fee_percent', d, fee_key), f.value('payment_fee_fixed', d, fee_key)
        s['payment_fees'] = add(s['payment_fees'], None if pct is None or fixed is None
                                else (r['total'] or 0) * pct / 100 + fixed * r['orders'])
        s['fee_fixed'] = add(s['fee_fixed'], None if fixed is None else fixed * r['orders'])
        if ch in SHIPPED:
            pack, label = f.value('packaging', d), _label(rd, d)
            pick = f.value('threepl_pick_pack', d, unit='usd_per_order')
            extra = f.value('threepl_pick_pack', d, unit='usd_per_unit') or 0.0  # optional second row
            ful = None if pack is None or pick is None or label is None else (
                (pack + pick + label) * r['orders'] + extra * max((r['units'] or 0) - r['orders'], 0))
            s['fulfillment'] = add(s['fulfillment'], ful)
    for r in lines or ():
        d = r['d']
        if d > end or (d[:7], r['channel']) not in acc:
            continue
        s = acc[(d[:7], r['channel'])]
        unit = f.value('cogs_landed', d, r['sku'])
        s['cogs'] = add(s['cogs'], None if unit is None else unit * r['qty'])
        if r['channel'] in SHIPPED:  # a SKU with its own box (the gift box) pays the difference over the global one
            own, base = f.value('packaging', d, r['sku']), f.value('packaging', d)
            if own is not None and base is not None and s['fulfillment'] is not None:
                s['fulfillment'] += (own - base) * r['qty']
    for r in rev or ():
        d = r['d']
        if not d or d > end or (d[:7], r['channel']) not in acc:
            continue
        s = acc[(d[:7], r['channel'])]
        if r['type'] == 'return':
            each = f.value('returns_processing', d)
            cost = None if each is None else each * r['n'] + ((r['amount'] or 0) if r['outcome'] == 'refunded' else 0)
            s['returns_cost'] = add(s['returns_cost'], cost)
        elif r['type'] == 'chargeback' and r['outcome'] != 'won':
            s['returns_cost'] = add(s['returns_cost'], r['amount'] or 0)
    out = {}
    for (m, ch), s in acc.items():
        net = s['net']
        cm1 = None if s['cogs'] is None or s['payment_fees'] is None else net - s['cogs'] - s['payment_fees']
        cm2 = None if cm1 is None or s['fulfillment'] is None or s['returns_cost'] is None else (
            cm1 + s['shipping'] - s['fulfillment'] - s['returns_cost'])
        row = {k: (r2(v) if isinstance(v, float) else v) for k, v in s.items()}
        row.update({'cm1': r2(cm1), 'cm2': r2(cm2), 'cm1_rate': rate(cm1, net), 'cm2_rate': rate(cm2, net)})
        for k in ('cogs', 'payment_fees', 'shipping', 'fulfillment', 'returns_cost'):
            row[k + '_rate'] = rate(s[k], net)
        # Per unit costs for SKU margins: per-order costs (fulfillment and fixed fees, less shipping charged) spread
        # over units, since a single pair ships in the same box as a 4-pack. The rest scales with revenue.
        per_order = None if s['fulfillment'] is None or s['fee_fixed'] is None else s['fulfillment'] + s['fee_fixed'] - s['shipping']
        row['per_unit_ops'] = None if per_order is None or not s['units'] else round(per_order / s['units'], 4)
        row['revenue_cost_rate'] = (None if s['payment_fees'] is None or s['fee_fixed'] is None or s['returns_cost'] is None
                                    else rate(s['payment_fees'] - s['fee_fixed'] + s['returns_cost'], net))
        out.setdefault(m, {})[ch] = row
    _CACHE[key] = out
    return out


def pnl_months(rd):
    """The ladder per month at the brand's real size: store channels from the aggregates, rates from order rows.

    Each month: gross margin (all store orders), online store CM1, CM2 and CM3 in dollars and as a share of its
    net revenue, retail (POS) CM2 when its fees exist, wholesale and marketplace revenue, and paid media."""
    gm = {r['month']: r for r in margin_months(rd)}
    om = order_months(rd) or {}
    chan = {}  # channels_monthly splits store orders by acquisition channel; `pos` is retail, the rest the online store
    for r in rd.table('channels_monthly') or ():
        c = chan.setdefault(r['month'], {'web': 0.0, 'pos': None})
        if r['channel'] == 'pos':
            c['pos'] = r.get('net_sales')
        else:
            c['web'] = add(c['web'], r.get('net_sales'))
    paid = {}
    for r in rd.table('paid_media_monthly') or ():
        paid.setdefault(r['month'], {})[r['platform']] = r.get('spend')
    whole = {}
    for r in rd.table('wholesale_monthly') or ():
        whole[r['month']] = whole.get(r['month'], 0.0) + (r.get('net_sales') or 0)
    market = {}
    for r in rd.table('marketplace_monthly') or ():
        market[r['month']] = market.get(r['month'], 0.0) + (r.get('net_sales') or 0)
    out = []
    for m in sorted(gm):
        g = gm[m]
        web_net = r2((chan.get(m) or {}).get('web'))
        pos_net = (chan.get(m) or {}).get('pos')
        spend = paid.get(m)
        spend_total = None if not spend or any(v is None for v in spend.values()) else sum(spend.values())
        w = (om.get(m) or {}).get('web') or {}
        p = (om.get(m) or {}).get('pos') or {}
        row = {'month': m, 'days': g['days'], 'full': g['full'], 'store_net_revenue': g['net_revenue'],
               'cogs': g['cogs'], 'gross_margin': g['gross_margin'], 'web_net_revenue': web_net,
               'pos_net_revenue': pos_net, 'paid_media': r2(spend_total),
               'paid_media_by_platform': spend or {},
               'paid_share': rate(spend_total, add(web_net, pos_net)),
               'wholesale_net_revenue': r2(whole.get(m)), 'marketplace_net_revenue': r2(market.get(m)),
               'rates_from_rows': bool(w), 'store_units': g['units'],
               'per_unit_ops': w.get('per_unit_ops'), 'revenue_cost_rate': w.get('revenue_cost_rate'),
               'paid_per_unit': None if spend_total is None or not g['units'] else round(spend_total / g['units'], 4)}
        for k in ('cogs', 'payment_fees', 'shipping', 'fulfillment', 'returns_cost', 'cm1', 'cm2'):
            rt = w.get(k + '_rate')  # dollars scale by the exact ratio; the rounded rate is for display
            row['web_' + k] = None if rt is None or web_net is None else r2(w[k] / w['net'] * web_net)
            row['web_' + k + '_rate'] = rt
        cm3 = None if row['web_cm2'] is None or spend_total is None else row['web_cm2'] - spend_total
        row['web_cm3'] = r2(cm3)
        row['web_cm3_rate'] = rate(cm3, web_net)
        row['pos_cm2_rate'] = p.get('cm2_rate')
        row['pos_reason'] = None if p.get('cm2_rate') is not None else (
            'no payment fee rows for the pos channel' if p else 'no retail order rows')
        out.append(row)
    return out


def month_label(month):
    y, m = month.split('-')
    return f'{calendar.month_abbr[int(m)]} {y}'


def last_full(rows, n=1):
    full = [r for r in rows if r['full']]
    return full[-n:] if n > 1 else (full[-1] if full else None)


# ---------------------------------------------------------------- findings

def _ev(metric, value, unit, ends_on, baseline=None, baseline_kind=None, window='28d', source='orders'):
    return {'metric': metric, 'value': value, 'unit': unit, 'window': window, 'ends_on': ends_on.isoformat(),
            'freshness_days': 1, 'baseline': baseline, 'baseline_kind': baseline_kind, 'source': source,
            'simulated': True}


def _confidence(windows_agree):
    return 0.9 if windows_agree >= 4 else 0.7 if windows_agree >= 2 else 0.5


def _escalate(severity, stake, net_28d):
    """The contract's money bands can raise a rule's severity, never lower it."""
    if stake is not None and net_28d:
        if stake > 0.05 * net_28d:
            return 'critical'
        if stake > 0.01 * net_28d and SEVERITY_ORDER[severity] > SEVERITY_ORDER['high']:
            return 'high'
    return severity


def _finding(rule_id, entity, severity, evidence, sentence, money, confidence, brain_refs, ends_on,
             status='open', unavailable=None, money_reason=None):
    f = {'id': f'{SCREEN}.{rule_id}.{entity["id"]}', 'screen': SCREEN, 'rule_id': rule_id, 'severity': severity,
         'entity': entity, 'evidence': evidence, 'sentence': sentence, 'capability': dict(CAPABILITY[rule_id]),
         'money_at_stake': money, 'confidence': confidence, 'brain_refs': brain_refs,
         'first_seen': ends_on.isoformat(), 'last_seen': ends_on.isoformat(), 'status': status,
         'unavailable': unavailable}
    if money is None:
        f['money_reason'] = money_reason or 'no baseline'
    return f


def _missing(rule_id, entity, severity, sentence, inputs, connector, fix, end):
    return _finding(rule_id, entity, severity, [], sentence, None, 0.1, [], end, status='unavailable',
                    money_reason='inputs missing', unavailable={'inputs': inputs, 'connector': connector, 'fix': fix})


def net_28d(rd):
    rows = [r for r in rd.table('daily') or () if r.get('date')]
    start = (rd.ends_on - timedelta(days=WINDOW - 1)).isoformat()
    sel = [r['net_sales'] for r in rows if start <= r['date'] <= rd.ends_on.isoformat() and r.get('net_sales') is not None]
    return sum(sel) if len(sel) == WINDOW else None


def sku_margins(rd, month_row):
    """CM3 per SKU for one month at the brand's real size. None for a SKU without a cost or a month without rates.

    CM3 = net sales - COGS - units x (ops per unit + paid media per unit) - net sales x revenue cost rate.
    Ops per unit: online store fulfillment and fixed fees, less shipping charged, over its units. Paid media per unit:
    all paid spend over store units (the room spec spreads spend pro rata by orders; units stand in for orders
    because order lines are the only per SKU count). Revenue cost rate: percent fees and returns cost over net."""
    m = month_row
    rates = (m.get('per_unit_ops'), m.get('paid_per_unit'), m.get('revenue_cost_rate'))
    out = []
    for s in sku_months(rd).get(m['month'], ()):
        ok = s['cogs'] is not None and s['net_sales'] and s['units'] and None not in rates
        cm3 = (s['net_sales'] - s['cogs'] - s['units'] * (rates[0] + rates[1]) - s['net_sales'] * rates[2]) if ok else None
        out.append({'sku': s['sku'], 'category': s['category'], 'units': s['units'], 'net_sales': r2(s['net_sales']),
                    'net_per_unit': r2(s['net_sales'] / s['units']) if s['units'] and s['net_sales'] else None,
                    'unit_cost': s['unit_cost'], 'cogs': s['cogs'],
                    'gross_margin': rate(s['net_sales'] - s['cogs'], s['net_sales']) if s['cogs'] is not None else None,
                    'cm3': r2(cm3), 'cm3_per_unit': r2(cm3 / s['units']) if cm3 is not None else None,
                    'cm3_rate': rate(cm3, s['net_sales'])})
    out.sort(key=lambda r: (r['cm3_per_unit'] is None, r['cm3_per_unit'] if r['cm3_per_unit'] is not None else 0))
    return out


def rule_margin_leak(rd, pnl):
    """FIN-R01: a SKU whose units rose each of the last 3 full months while its CM3 stayed negative."""
    end = rd.ends_on
    entity = {'type': 'sku', 'id': 'all', 'label': 'Every SKU'}
    months = last_full(pnl, 3)
    if len(months) < 3 or any(m['per_unit_ops'] is None or m['paid_per_unit'] is None or m['revenue_cost_rate'] is None
                              for m in months):
        return [_missing('FIN-R01', entity, 'high', 'Margin after marketing by SKU cannot be read for the last 3 full months.',
                         ['finance_inputs.cogs_landed', 'orders', 'paid_media_monthly'], 'finance_inputs',
                         'Add landed cost, fee and fulfillment rows for every month, and keep order rows loaded.', end)]
    by = {}
    for m in months:
        for s in sku_margins(rd, m):
            if s['cm3'] is not None:
                by.setdefault(s['sku'], []).append(dict(s, month=m['month'], per_unit_ops=m['per_unit_ops'],
                                                        paid_per_unit=m['paid_per_unit'],
                                                        revenue_cost_rate=m['revenue_cost_rate']))
    out, n28 = [], net_28d(rd)
    for sku, rows in sorted(by.items()):
        if len(rows) < 3:
            continue
        if not rows[0]['units'] < rows[1]['units'] < rows[2]['units'] or any(r['cm3'] >= 0 for r in rows):
            continue
        last = rows[-1]
        loss = -last['cm3']
        worse = rows[2]['cm3_per_unit'] < rows[0]['cm3_per_unit']
        money = {'usd': r2(loss),
                 'formula': 'units x (per_unit_ops + paid_per_unit) + net_sales x revenue_cost_rate + cogs - net_sales',
                 'inputs': {k: last[k] for k in ('units', 'net_sales', 'cogs', 'per_unit_ops', 'paid_per_unit',
                                                 'revenue_cost_rate')}, 'window': last['month']}
        ev = [_ev('units', r['units'], 'count', end, window=r['month'], source='products_monthly') for r in rows]
        ev += [_ev('cm3_per_unit', r['cm3_per_unit'], 'usd', end, baseline=0, baseline_kind='threshold', window=r['month'],
                   source='products_monthly, finance_inputs, orders, reversed_orders, paid_media_monthly') for r in rows]
        sentence = (f'{sku} sold more each month but still loses ${-last["cm3_per_unit"]:,.2f} per unit after marketing cost. '
                    f'Units went from {rows[0]["units"]:,} in {month_label(rows[0]["month"])} to {last["units"]:,} in '
                    f'{month_label(last["month"])}.')
        out.append(_finding('FIN-R01', {'type': 'sku', 'id': sku, 'label': sku},
                            _escalate('high' if worse else 'medium', loss, n28), ev, sentence, money, 0.7, [], end))
    return out


def _dio_windows(rd, sku_filter=None):
    """Days of stock per SKU for the current and 3 trailing 28-day windows, from data.sqlite (scale free)."""
    inv = rd.sql('SELECT date, sku, SUM(on_hand) AS on_hand FROM inventory GROUP BY 1, 2')
    sold = rd.sql("SELECT substr(o.created_at, 1, 10) AS d, l.sku, SUM(l.qty) AS qty FROM order_lines l "
                  "JOIN orders o ON o.id = l.order_id WHERE o.status IN ('paid', 'partially_refunded', 'refunded') "
                  "GROUP BY 1, 2")
    if not inv or not sold:
        return None
    wins = []
    for k in range(TRAILING):
        e = rd.ends_on - timedelta(days=WINDOW * k)
        s = e - timedelta(days=WINDOW - 1)
        wins.append((s.isoformat(), e.isoformat()))
    out = {}
    for i, (s, e) in enumerate(wins):
        stock, units = {}, {}
        for r in inv:
            if s <= r['date'] <= e:
                stock.setdefault(r['sku'], []).append(r['on_hand'] or 0)
        for r in sold:
            if s <= r['d'] <= e:
                units[r['sku']] = units.get(r['sku'], 0) + (r['qty'] or 0)
        for sku, lst in stock.items():
            per_day = units.get(sku, 0) / WINDOW
            out.setdefault(sku, [None] * TRAILING)[i] = {
                'window': f'{s} to {e}', 'on_hand': round(sum(lst) / len(lst), 1), 'units_per_day': round(per_day, 3),
                'dio': round((sum(lst) / len(lst)) / per_day, 1) if per_day else None, 'full': len(lst) == WINDOW}
    return out


def lead_times(rd):
    rows = rd.table('inbound_pos') or ()
    by = {}
    for r in rows:
        if r.get('eta') and r.get('ordered_on'):
            by.setdefault(r['sku'], []).append((date.fromisoformat(r['eta'][:10]) - date.fromisoformat(r['ordered_on'][:10])).days)
    return {k: statistics.median(v) for k, v in by.items()}


def inventory_rows(rd):
    """Per SKU: days of stock now, lead time, the line (lead + 30) and the cash over it. Shared with api.py."""
    dio = _dio_windows(rd)
    if dio is None:
        return None
    leads = lead_times(rd)
    skus = sku_months(rd)
    lf = last_full(margin_months(rd))
    month = skus.get(lf['month'], []) if lf else []
    daily_cogs = {s['sku']: (s['cogs'] / lf['days'] if s['cogs'] is not None else None) for s in month}
    out = []
    for sku, wins in sorted(dio.items()):
        now = wins[0]
        lead = leads.get(sku)
        line = None if lead is None else lead + OVERHANG_DAYS
        excess = None if now is None or now['dio'] is None or line is None else round(now['dio'] - line, 1)
        per_day = daily_cogs.get(sku)
        cash = None if excess is None or excess <= 0 or per_day is None else r2(excess * per_day)
        agree = sum(1 for w in wins if w and w['dio'] is not None and line is not None and w['dio'] > line)
        out.append({'sku': sku, 'dio': None if now is None else now['dio'], 'lead_days': lead, 'line_days': line,
                    'excess_days': excess, 'cogs_per_day': r2(per_day), 'cash_over_line': cash, 'windows_agree': agree,
                    'on_hand_sample': None if now is None else now['on_hand'],
                    'units_per_day_sample': None if now is None else now['units_per_day'], 'windows': wins})
    return out


def rule_overhang(rd):
    """FIN-R08: days of stock over supplier lead time plus 30 days."""
    end = rd.ends_on
    rows = inventory_rows(rd)
    if rows is None:
        return [_missing('FIN-R08', {'type': 'sku', 'id': 'all', 'label': 'Every SKU'}, 'medium',
                         'Days of stock by SKU cannot be read: inventory or order rows are not loaded.',
                         ['inventory', 'order_lines', 'inbound_pos'], 'shopify',
                         'Connect Shopify inventory levels and purchase orders, or rebuild data.sqlite.', end)]
    out = []
    for r in rows:
        if r['excess_days'] is None or r['excess_days'] <= 0:
            continue
        money = None if r['cash_over_line'] is None else {
            'usd': r['cash_over_line'], 'formula': '(days_of_stock - (lead_days + 30)) x cogs_per_day',
            'inputs': {'days_of_stock': r['dio'], 'lead_days': r['lead_days'], 'cogs_per_day': r['cogs_per_day']},
            'window': '28d', 'note': 'cash tied up in stock, not revenue lost'}
        ev = [_ev('days_inventory_outstanding', r['dio'], 'days', end, baseline=r['line_days'], baseline_kind='threshold',
                  source='inventory, order_lines'),
              _ev('supplier_lead_time', r['lead_days'], 'days', end, window='all purchase orders', source='inbound_pos')]
        if r['cogs_per_day'] is not None:
            ev.append(_ev('cogs_per_day', r['cogs_per_day'], 'usd', end, window='last full month',
                          source='products_monthly, finance_inputs'))
        amt = f'${r["cash_over_line"]:,.0f}' if r['cash_over_line'] is not None else 'Cash'
        sentence = (f'{amt} of {r["sku"]} stock sits {r["excess_days"]:.0f} days beyond what lead time needs. '
                    f'Stock covers {r["dio"]:.0f} days; lead time is {r["lead_days"]:.0f}.')
        out.append(_finding('FIN-R08', {'type': 'sku', 'id': r['sku'], 'label': r['sku']}, 'medium', ev, sentence, money,
                            _confidence(r['windows_agree']), [], end, money_reason='no cost row for the last full month'))
    return out


def rule_unreadable(rd):
    """The rules whose inputs no connector fills yet. Each emits one unavailable finding, never a 0."""
    end = rd.ends_on
    b = rd.brand or 'brand'
    out = [
        _missing('FIN-R02', {'type': 'metric', 'id': 'cash_low_point_13wk', 'label': '13-week cash low point'}, 'critical',
                 'The 13-week cash forecast cannot be checked against a floor: no bank ledger and no stated cash floor.',
                 ['bank_ledger', f'brain.{b}.finance.min_cash_floor'], 'accounting',
                 'Connect the bank feed or QuickBooks or Xero, and write the minimum cash floor in the brain.', end),
        _missing('FIN-R03', {'type': 'offer', 'id': 'promos', 'label': 'Completed promos'}, 'high',
                 'Promo break-even cannot be checked: no promo was modelled before launch.',
                 ['promo_models'], 'promo gate (MONEY-C05)',
                 'Run the promo break-even check before each sale so the result can be compared after it ends.', end),
        _missing('FIN-R04', {'type': 'metric', 'id': 'cash_conversion_cycle', 'label': 'Cash conversion cycle'}, 'high',
                 'CAC payback cannot be set against the cash cycle: days payable to suppliers are unknown.',
                 ['accounts_payable'], 'accounting', 'Connect bills from QuickBooks or Xero so supplier payment days are known.', end),
        _missing('FIN-R05', {'type': 'metric', 'id': 'platform_books_variance', 'label': 'Platform to books gap'}, 'high',
                 'Shopify, Meta and the processor cannot be matched to the books: no monthly P&L actuals on file.',
                 ['finance_inputs.pnl_actual'], 'accounting', 'Enter monthly P&L actuals as pnl_actual rows or connect the books.', end),
        _missing('FIN-R06', {'type': 'metric', 'id': 'payout_deposit_gap', 'label': 'Shopify Payments deposits'}, 'high',
                 'Payouts Shopify reports as sent cannot be matched to deposits: no bank ledger.',
                 ['bank_ledger'], 'accounting', 'Connect the bank feed so each payout can be found in the bank.', end),
        _missing('FIN-R10', {'type': 'metric', 'id': 'opex_vs_budget', 'label': 'Operating costs against budget'}, 'medium',
                 'Spend against budget cannot be checked: no annual budget on file.',
                 ['budget_annual'], 'budget sheet', 'Upload the annual budget by category and month.', end),
        _missing('FIN-R11', {'type': 'metric', 'id': 'sales_tax_nexus', 'label': 'Sales tax nexus'}, 'critical',
                 'Sales by state cannot be checked against registrations: no registrations or filings on file.',
                 ['sales_tax_filings'], 'Avalara or TaxJar', 'Connect Avalara or TaxJar, or list the states where the brand is registered.', end),
    ]
    if rd.market() in ('IN',):
        out.append(_missing('FIN-R07', {'type': 'metric', 'id': 'cod_remittance_gap', 'label': 'COD remittance'}, 'high',
                            'COD cash cannot be matched to courier remittances: no courier COD report.',
                            ['cod_remittance'], 'courier portal', 'Connect the courier COD report.', end))
    if rd.has_table('subscription_cohorts'):
        out.append(_missing('FIN-R09', {'type': 'metric', 'id': 'subscription_churn_rate', 'label': 'Subscription churn'},
                            'high', 'Subscription churn is not computed in round 0.', ['subscription_cohorts'],
                            'subscription platform', 'Churn by month comes in a later round.', end))
    return out


def run(brand, window=None, data=None):
    """Findings for one brand, sorted by severity then money at stake. `window` is {ends_on} or None."""
    ends_on = date.fromisoformat(window['ends_on']) if window and window.get('ends_on') else last_full_day(data, brand)
    rd = Reader(data, brand, ends_on)
    pnl = pnl_months(rd)
    out = rule_margin_leak(rd, pnl) + rule_overhang(rd) + rule_unreadable(rd)
    out.sort(key=lambda f: (SEVERITY_ORDER[f['severity']], -((f.get('money_at_stake') or {}).get('usd') or -1), f['id']))
    return out
