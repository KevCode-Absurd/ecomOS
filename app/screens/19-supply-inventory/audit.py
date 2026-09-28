"""Supply and inventory audit (screen 19, round 0). Findings in the shape of app/contracts/audit.md.

Order totals and net revenue come from app/metrics.py (aov). Stock, receipts and sell-through by SKU are read from
data.sqlite (`inventory`, `inbound_pos`, `order_lines` joined to `orders`, `products`) with GROUP BY queries: the
metric contract has no SKU stock metrics yet (FEATURES.md proposes stock_cover_days, reorder_point_units and
safety_stock_units for a contract session). Landed cost per unit is `finance_inputs.cogs_landed` beside the brand's
aggregates. No connector, no model call. Same tables, brain and window give the same findings.

Words
  on hand          units on hand on the window's last day, summed over locations (Shopify InventoryLevel).
  velocity         units sold on paid orders per day, trailing 14 days (room spec); 28 days is the second window.
  cover            on hand / velocity, in days.
  lead time        median days from ordered_on to eta over received POs in the last 365 days, per SKU. The table has
                   no received date, so eta stands for the receipt.
  safety stock     SERVICE_Z x standard deviation of daily units (56 days) x sqrt(lead time).
  reorder point    velocity x lead time + safety stock.
  recommended PO   velocity x (lead time + REVIEW_DAYS) + safety stock - on hand - open PO units, floor 0.
  net per unit     line total minus line discount over units, paid orders, 28 days.

Rules (one per job in the room's JTBD table; chargebacks and return to sender are owned by 06-store-health)
  SUPPLY-R01  Runs out before the next PO lands. Open PO exists and cover (14-day velocity) is under the days to its
              earliest eta. Money: gap days x velocity x net per unit. Critical on a hero SKU (top HERO_COUNT by
              28-day net sales), else by stake. PROD-C22, founder gate. Owner: 19-supply-inventory.
  SUPPLY-R02  Under its reorder point with nothing on order. No open PO and on hand under the reorder point.
              Money: days a PO placed today lands after stock runs out (lead time minus cover, floor 0) x velocity x
              net per unit. PROD-C22, founder gate. Owner: 19-supply-inventory.
  SUPPLY-R03  Landed cost moved with no margin recheck. The current cogs_landed row differs from the one before by
              more than LANDED_MOVE, the change took effect in the last 365 days, and the brain holds no margin gate
              record after it. One brand finding: one recheck covers every SKU that moved. Money: sum of cost change
              x units sold in 28 days. PROD-C23, agent does. Owner: 19-supply-inventory.
  SUPPLY-R04  Supplier or country concentration. Needs supplier_master. PROD-C23. Unavailable today.
  SUPPLY-R05  Supplier scorecard slipping 2 periods in a row. Needs supplier_scorecard. PROD-C69. Unavailable.
  SUPPLY-R06  3PL dispatch SLA missed. Needs fulfilment_sla. PROD-C53. Unavailable.
  SUPPLY-R07  Courier 10 points worse than the best in a zone. Needs courier_scorecard. PROD-C59. Unavailable.
  SUPPLY-R08  Carrier exceptions closing their attempt window in 4 hours. Needs carrier_exception_queue. PROD-C56.
  SUPPLY-R09  Carrier billed more than the dispatch weight (plus COD remittance where the market has COD).
              Needs carrier_billing. MONEY-C52. Unavailable.
  SUPPLY-R10  Dead stock. Units older than DEAD_DAYS (first in, first out against receipts) on a SKU with more than
              SLOW_COVER days of cover at 28-day velocity. Money: aged units x landed cost. PROD-C27, founder gate.
  SUPPLY-R11  Price lock ending in 30 days. Needs supplier_contracts. LOOP-C28. Unavailable.
  SUPPLY-R12  PO, invoice and receipt do not match. Needs three_way_match. MONEY-C53. Unavailable.
  SUPPLY-R13  Commodity input up 8 percent since the last lock. Needs commodity_index. PROD-C18. Unavailable.
  SUPPLY-R14  Peak readiness under 80 percent with 45 days to go. Needs peak_season_plan (staffing and WMS load
              tests); the stock part alone is an insight on the screen, not the metric. PROD-C72. Unavailable.

Scale: data.sqlite may hold a sample of the order history (the dev build runs at scale 0.1) and stock follows the
sample. Units and dollars are scaled by paid orders in the aggregate over paid orders in data.sqlite for the same
window (1.0 for a live store). Days and rates are not scaled.
"""
import importlib.util
import json
import math
import statistics
import sys
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parents[1]
SCREEN = '19-supply-inventory'
WINDOW = 28
VELOCITY_DAYS = 14       # room spec: trailing 14-day average daily units
SIGMA_DAYS = 56          # daily units used for the demand standard deviation
LEAD_LOOKBACK = 365
SERVICE_Z = 1.65         # 95 percent service level
REVIEW_DAYS = 30         # a PO covers lead time plus one month
HERO_COUNT = 5
LANDED_MOVE = 0.05       # room spec: landed cost moved more than 5 percent
DEAD_DAYS = 180
SLOW_COVER = 120
PAID = ('paid', 'partially_refunded', 'refunded')
SEVERITY_ORDER = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}

AUTONOMY = {'PROD-C22': 'founder_gate', 'PROD-C23': 'agent_does', 'PROD-C69': 'agent_does',
            'PROD-C53': 'human_assist', 'PROD-C59': 'founder_gate', 'PROD-C56': 'founder_gate',
            'MONEY-C52': 'agent_does', 'PROD-C27': 'founder_gate', 'LOOP-C28': 'agent_does',
            'MONEY-C53': 'founder_gate', 'PROD-C18': 'agent_does', 'PROD-C72': 'founder_gate'}

# Rules whose inputs no connector fills yet: rule id -> (name, entity, table, connector, fix, severity, capability)
MISSING = [
    ('SUPPLY-R04', 'Supplier or country concentration', ('brand', 'suppliers', 'Suppliers'), 'supplier_master',
     'PO history with supplier and country', 'Add a supplier and country to each PO, or upload a supplier list. '
     'Then the share from one supplier and one country is counted.', 'high', 'PROD-C23'),
    ('SUPPLY-R05', 'Supplier scorecard slipping', ('brand', 'suppliers', 'Suppliers'), 'supplier_scorecard',
     'PO receipts with dates and inspection results', 'Record the day each PO arrived and any defects found. '
     'Then each supplier gets an on-time and defect score.', 'medium', 'PROD-C69'),
    ('SUPPLY-R06', '3PL dispatch time', ('stage', 'fulfilment', '3PL dispatch'), 'fulfilment_sla',
     '3PL or WMS dispatch log', 'Connect the 3PL dispatch log. Then orders shipped late against the contract are '
     'counted.', 'high', 'PROD-C53'),
    ('SUPPLY-R07', 'Courier by zone', ('stage', 'delivery', 'Courier by zone'), 'courier_scorecard',
     'shipping app or carrier tracking feed', 'Connect the shipping app. Then return to sender, first attempt and '
     'days to deliver are counted by courier and zone.', 'medium', 'PROD-C59'),
    ('SUPPLY-R08', 'Carrier exceptions near the attempt window', ('stage', 'delivery_exceptions', 'Carrier exceptions'),
     'carrier_exception_queue', 'carrier exception feed', 'Connect carrier tracking with exception events. Then '
     'parcels about to be sent back are listed while there is still time.', 'high', 'PROD-C56'),
    ('SUPPLY-R09', 'Carrier billing against dispatch weight', ('stage', 'carrier_billing', 'Carrier billing'),
     'carrier_billing', 'carrier invoice files', 'Upload carrier invoices. Then billed weight is checked against '
     'the packed weight at dispatch.', 'medium', 'MONEY-C52'),
    ('SUPPLY-R11', 'Supplier price lock ending', ('brand', 'supplier_contracts', 'Supplier contracts'),
     'supplier_contracts', 'contract list', 'Enter each supplier contract with its price lock end date.', 'medium',
     'LOOP-C28'),
    ('SUPPLY-R12', 'PO, invoice and receipt match', ('stage', 'payables', 'Supplier invoices'), 'three_way_match',
     'accounts payable and goods receipt records', 'Connect the accounts payable tool and record goods received '
     'per PO. Then invoices that do not match are held.', 'high', 'MONEY-C53'),
    ('SUPPLY-R13', 'Commodity input cost', ('brand', 'commodities', 'Cotton and wool prices'), 'commodity_index',
     'commodity price feed', 'Map each SKU to its main fibre and add a price feed. Then cost rises since the last '
     'lock are shown.', 'medium', 'PROD-C18'),
    ('SUPPLY-R14', 'Peak season readiness', ('stage', 'peak_season', 'Q4 and Black Friday readiness'),
     'peak_season_plan', 'peak plan with staffing and system load tests', 'Enter the peak plan: stock target, '
     'warehouse staff booked and the last load test. Stock is already counted.', 'medium', 'PROD-C72'),
]

RULES = [
    {'rule_id': 'SUPPLY-R01', 'name': 'Runs out before the next PO lands', 'entity_type': 'sku',
     'inputs': ['inventory', 'inbound_pos', 'order_lines', 'orders'], 'capability': 'PROD-C22', 'owner_screen': SCREEN},
    {'rule_id': 'SUPPLY-R02', 'name': 'Under the reorder point with nothing on order', 'entity_type': 'sku',
     'inputs': ['inventory', 'inbound_pos', 'order_lines', 'orders'], 'capability': 'PROD-C22', 'owner_screen': SCREEN},
    {'rule_id': 'SUPPLY-R03', 'name': 'Landed cost moved with no margin recheck', 'entity_type': 'brand',
     'inputs': ['finance_inputs', 'order_lines', 'brain.decisions'], 'capability': 'PROD-C23', 'owner_screen': SCREEN},
    {'rule_id': 'SUPPLY-R10', 'name': 'Dead stock', 'entity_type': 'sku',
     'inputs': ['inventory', 'inbound_pos', 'order_lines', 'finance_inputs'], 'capability': 'PROD-C27',
     'owner_screen': SCREEN},
] + [{'rule_id': m[0], 'name': m[1], 'entity_type': m[2][0], 'inputs': [m[3]], 'capability': m[7],
      'owner_screen': SCREEN} for m in MISSING]
RULES.sort(key=lambda r: r['rule_id'])

_MODS = {}


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def metrics():
    if 'metrics' not in _MODS:
        _MODS['metrics'] = _load('ecomos_metrics_supply', APP / 'metrics.py')
    return _MODS['metrics']


def brand_data(brand):
    if 'tables' not in _MODS:
        _MODS['tables'] = _load('ecomos_tables_supply', APP / 'data' / 'tables.py')
    return _MODS['tables'].brand_data(brand)


def brain(brand):
    if not brand or not (APP / 'brain' / brand).is_dir():
        return None
    if 'store' not in _MODS:
        path = str(APP / 'brain')
        if path not in sys.path:
            sys.path.insert(0, path)  # store.py imports validate.py by name
        _MODS['store'] = _load('ecomos_brain_store_supply', APP / 'brain' / 'store.py')
    return _MODS['store'].Brain(brand)


class Reader:
    """One brand, one window end. m() is metrics.compute with the brand filled in; sql() reads data.sqlite."""

    def __init__(self, data, brand, ends_on):
        self.data, self.brand, self.ends_on = data, brand, ends_on
        self.source = brand_data(brand) if brand else data
        self._brain = brain(brand)
        self._memo = {}

    def m(self, name, days=WINDOW, end=None, **kw):
        q = {'window': f'{days}d', 'end': (end or self.ends_on).isoformat(), **kw}
        if self.brand:
            q['brand'] = self.brand
        key = (name, tuple(sorted(q.items())))
        if key not in self._memo:
            self._memo[key] = metrics().compute(name, self.data, **q)
        return self._memo[key]

    def sql(self, query):
        """Rows from data.sqlite. KeyError when the brand has no data.sqlite or the table is missing."""
        fn = getattr(self.source, '_sql', None)
        if fn is None:
            raise KeyError('data.sqlite')
        try:
            return fn(query)
        except Exception as exc:  # sqlite3.OperationalError: no such table
            if isinstance(exc, KeyError):
                raise
            raise KeyError(str(exc))

    def has_table(self, name):
        try:
            self.source.table(name)
            return True
        except (KeyError, ValueError):
            return False

    def record(self, rid):
        return self._brain.get(rid) if self._brain else None

    def records(self, section):
        return self._brain.records(section) if self._brain else []

    def finance_rows(self, field):
        folder = getattr(self.source, 'folder', None)
        path = folder / 'finance_inputs.json' if folder else None
        if not path or not path.is_file():
            return None
        return [r for r in json.loads(path.read_text(encoding='utf-8'))['rows'] if r.get('field') == field]


def last_full_day(data, brand):
    source = brand_data(brand) if brand else data
    return date.fromisoformat(source.brand['as_of'])


def _d(day):
    return day.isoformat()


def _ev(metric, value, unit, ends_on, baseline=None, baseline_kind=None, window='14d', source='inventory',
        freshness=1):
    return {'metric': metric, 'value': value, 'unit': unit, 'window': window, 'ends_on': _d(ends_on),
            'freshness_days': freshness, 'baseline': baseline, 'baseline_kind': baseline_kind, 'source': source,
            'simulated': True}


def _severity(stake, net_28d, windows_agree):
    if stake is not None and net_28d and stake > 0.05 * net_28d:
        return 'critical'
    if windows_agree >= 2 or (stake is not None and net_28d and stake > 0.01 * net_28d):
        return 'high'
    return 'medium'


def _confidence(windows, fresh=True):
    c = 0.9 if windows >= 4 else 0.7 if windows >= 2 else 0.5
    return round(max(0.1, c - (0 if fresh else 0.2)), 2)


def _finding(rule_id, entity, severity, evidence, sentence, capability, money, confidence, brain_refs, ends_on,
             status='open', unavailable=None, money_reason=None):
    f = {'id': f'{SCREEN}.{rule_id}.{entity["id"]}', 'screen': SCREEN, 'rule_id': rule_id, 'severity': severity,
         'entity': entity, 'evidence': evidence, 'sentence': sentence,
         'capability': {'id': capability, 'autonomy': AUTONOMY[capability]},
         'money_at_stake': money, 'confidence': confidence, 'brain_refs': brain_refs,
         'first_seen': _d(ends_on), 'last_seen': _d(ends_on), 'status': status, 'unavailable': unavailable}
    if money is None:
        f['money_reason'] = money_reason or 'no baseline'
    return f


def _money(usd, formula, inputs, window):
    return {'usd': round(max(0.0, usd)), 'formula': formula, 'inputs': inputs, 'window': window}


def _fmt_int(n):
    return f'{int(round(n)):,}'


def _day(d):
    return f'{d.day} {d.strftime("%b")}'


# ---------------------------------------------------------------- the SKU table (shared with api.py)

def _scale(rd):
    """Paid orders in the aggregate over paid orders in data.sqlite, 28 days. None when either is missing."""
    aov = rd.m('aov', WINDOW)
    start = rd.ends_on - timedelta(days=WINDOW - 1)
    paid = ', '.join(f"'{s}'" for s in PAID)
    n = rd.sql(f"SELECT COUNT(*) AS n FROM orders WHERE status IN ({paid}) "
               f"AND substr(created_at, 1, 10) BETWEEN '{_d(start)}' AND '{_d(rd.ends_on)}'")[0]['n']
    if aov.get('unavailable') or not n:
        return None
    return round(aov['inputs']['orders'] / n, 4)


def _landed(rows, sku, day):
    """(current row, row before it) for one SKU at `day`, from finance_inputs.cogs_landed."""
    mine = sorted((r for r in rows or [] if r.get('scope') == 'sku' and r.get('scope_key') == sku),
                  key=lambda r: r['effective_from'])
    live = [r for r in mine if r['effective_from'] <= _d(day)]
    if not live:
        return None, None
    return live[-1], (live[-2] if len(live) > 1 else None)


def supply(rd):
    """Per SKU stock, velocity, lead time, open POs, reorder point and landed cost. Cached on the Reader.
    Returns {'unavailable': True, reason, missing} when a table is missing."""
    if 'supply' in rd._memo:
        return rd._memo['supply']
    try:
        out = _supply(rd)
    except KeyError as exc:
        out = {'unavailable': True, 'reason': f'stock tables are not connected ({exc.args[0]})',
               'missing': ['inventory', 'inbound_pos', 'order_lines'], 'fix': 'shopify'}
    rd._memo['supply'] = out
    return out


def _supply(rd):
    E = rd.ends_on
    paid = ', '.join(f"'{s}'" for s in PAID)
    inv = rd.sql(f"SELECT sku, SUM(on_hand) AS on_hand, SUM(available) AS available, MAX(captured_at) AS captured_at, "
                 f"COUNT(*) AS locations FROM inventory WHERE date = '{_d(E)}' GROUP BY sku")
    if not inv:
        raise KeyError(f'inventory has no rows for {_d(E)}')
    s56 = E - timedelta(days=SIGMA_DAYS - 1)
    daily = rd.sql(f"SELECT l.sku, substr(o.created_at, 1, 10) AS day, SUM(l.qty) AS units, "
                   f"SUM(l.line_total - l.line_discount) AS net FROM order_lines l JOIN orders o ON o.id = l.order_id "
                   f"WHERE o.status IN ({paid}) AND substr(o.created_at, 1, 10) BETWEEN '{_d(s56)}' AND '{_d(E)}' "
                   f"GROUP BY l.sku, day")
    pos = rd.sql("SELECT po_id, sku, qty, ordered_on, eta, status FROM inbound_pos")
    products = {r['sku']: r for r in rd.sql("SELECT sku, title, category, price FROM products")}
    landed_rows = rd.finance_rows('cogs_landed')
    scale = _scale(rd)
    days = [_d(E - timedelta(days=i)) for i in range(SIGMA_DAYS)]
    by = {}
    for r in daily:
        by.setdefault(r['sku'], {})[r['day']] = (r['units'], r['net'])
    s14, s28 = _d(E - timedelta(days=VELOCITY_DAYS - 1)), _d(E - timedelta(days=WINDOW - 1))
    lead_from = _d(E - timedelta(days=LEAD_LOOKBACK))
    dead_from = _d(E - timedelta(days=DEAD_DAYS))
    rows = []
    for i in inv:
        sku = i['sku']
        d = by.get(sku, {})
        u14 = sum(v[0] for k, v in d.items() if k >= s14)
        u28 = sum(v[0] for k, v in d.items() if k >= s28)
        n28 = sum(v[1] for k, v in d.items() if k >= s28)
        series = [d.get(k, (0, 0))[0] for k in days]
        v14, v28 = u14 / VELOCITY_DAYS, u28 / WINDOW
        mine = [p for p in pos if p['sku'] == sku]
        leads = [(date.fromisoformat(p['eta']) - date.fromisoformat(p['ordered_on'])).days for p in mine
                 if p['status'] == 'received' and p['eta'] >= lead_from and p['eta'] <= _d(E)]
        open_pos = sorted((p for p in mine if p['status'] == 'open' and p['eta'] > _d(E)), key=lambda p: p['eta'])
        received_recent = sum(p['qty'] for p in mine if p['status'] == 'received' and dead_from < p['eta'] <= _d(E))
        lead = statistics.median(leads) if leads else None
        cover14 = i['on_hand'] / v14 if v14 else None
        cover28 = i['on_hand'] / v28 if v28 else None
        safety = SERVICE_Z * statistics.pstdev(series) * math.sqrt(lead) if lead is not None else None
        rop = v14 * lead + safety if lead is not None else None
        on_order = sum(p['qty'] for p in open_pos)
        next_eta = date.fromisoformat(open_pos[0]['eta']) if open_pos else None
        to_next = (next_eta - E).days if next_eta else None
        rec = (max(0.0, v14 * (lead + REVIEW_DAYS) + safety - i['on_hand'] - on_order)
               if lead is not None else None)
        cur, prev = _landed(landed_rows, sku, E)
        p = products.get(sku, {})
        rows.append({
            'sku': sku, 'title': p.get('title') or sku, 'category': p.get('category'), 'price': p.get('price'),
            'on_hand': i['on_hand'], 'available': i['available'], 'locations': i['locations'],
            'captured_at': i['captured_at'], 'units_14d': u14, 'units_28d': u28, 'net_28d': round(n28, 2),
            'velocity_14d': round(v14, 3), 'velocity_28d': round(v28, 3),
            'net_per_unit': round(n28 / u28, 2) if u28 else None,
            'cover_days': round(cover14, 1) if cover14 is not None else None,
            'cover_days_28': round(cover28, 1) if cover28 is not None else None,
            'lead_days': lead, 'lead_pos': len(leads), 'safety_units': round(safety, 1) if safety is not None else None,
            'reorder_point': round(rop, 1) if rop is not None else None, 'on_order': on_order,
            'open_pos': [x['po_id'] for x in open_pos], 'next_eta': _d(next_eta) if next_eta else None,
            'days_to_next': to_next, 'recommended_po': round(rec, 1) if rec is not None else None,
            'received_recent': received_recent,
            'landed_cost': cur['value'] if cur else None, 'landed_from': cur['effective_from'] if cur else None,
            'landed_prev': prev['value'] if prev else None,
        })
    # Hero SKUs: top HERO_COUNT by 28-day net sales.
    for rank, r in enumerate(sorted(rows, key=lambda r: (-r['net_28d'], r['sku']))):
        r['hero'] = rank < HERO_COUNT
        r['rank'] = rank + 1
    rows.sort(key=lambda r: (r['cover_days'] if r['cover_days'] is not None else 1e9, r['sku']))
    fresh = (date.fromisoformat(max(r['captured_at'] for r in rows)[:10]) - E).days
    return {'unavailable': False, 'rows': rows, 'scale': scale, 'ends_on': _d(E), 'freshness_days': max(fresh, 0),
            'landed_known': landed_rows is not None}


def scaled(v, scale):
    """Units or dollars at the order totals (see Scale in the docstring). None stays None."""
    return None if v is None or scale is None else round(v * scale)


def gap_days(r):
    """(gap with 14-day velocity, gap with 28-day velocity, kind). kind 'po' when an open PO sets the date."""
    if r['days_to_next'] is not None:
        lands = r['days_to_next']
        kind = 'po'
    elif r['lead_days'] is not None:
        lands = r['lead_days']
        kind = 'lead'
    else:
        return None, None, None
    g14 = max(0.0, lands - r['cover_days']) if r['cover_days'] is not None else None
    g28 = max(0.0, lands - r['cover_days_28']) if r['cover_days_28'] is not None else None
    return g14, g28, kind


# ---------------------------------------------------------------- rules

def _net_28d(rd):
    aov = rd.m('aov', WINDOW)
    return None if aov.get('unavailable') else aov['inputs']['net_revenue']


def _unavailable_all(rd, sup, rule_id, name, entity_type, capability, severity):
    return [_finding(rule_id, {'type': entity_type, 'id': 'all', 'label': name}, severity, [],
                     f'{name} is unavailable: the stock tables are not connected.', capability, None, 0.1, [],
                     rd.ends_on, status='unavailable', money_reason='inputs unavailable',
                     unavailable={'inputs': sup['missing'], 'connector': 'Shopify inventory and orders',
                                  'fix': 'Connect Shopify with inventory read access. Then stock, sell-through and '
                                         'POs by SKU are read daily.'})]


def rule_stockout(rd):
    sup = supply(rd)
    if sup['unavailable']:
        return _unavailable_all(rd, sup, 'SUPPLY-R01', 'Stock cover against the next PO', 'sku', 'PROD-C22', 'critical')
    sc, net28, E = sup['scale'], _net_28d(rd), rd.ends_on
    out = []
    for r in sup['rows']:
        g14, g28, kind = gap_days(r)
        if kind != 'po' or not g14:
            continue
        agree = 1 + (1 if g28 else 0)
        price = r['net_per_unit']
        stake = None
        if sc is not None and price is not None:
            stake = _money(g14 * r['velocity_14d'] * sc * price, 'gap_days * units_per_day_14d * net_per_unit',
                           {'gap_days': round(g14, 1), 'units_per_day_14d': round(r['velocity_14d'] * sc, 1),
                            'net_per_unit': price}, f'{VELOCITY_DAYS}d')
        usd = stake['usd'] if stake else None
        sev = 'critical' if r['hero'] and agree >= 2 else _severity(usd, net28, agree)
        runs_out = E + timedelta(days=round(r['cover_days']))
        eta = date.fromisoformat(r['next_eta'])
        ev = [_ev('stock_cover_days', r['cover_days'], 'days', E, r['days_to_next'], 'threshold',
                  freshness=sup['freshness_days']),
              _ev('stock_cover_days', r['cover_days_28'], 'days', E, r['days_to_next'], 'threshold', window='28d',
                  source='order_lines', freshness=sup['freshness_days']),
              _ev('on_hand_units', scaled(r['on_hand'], sc), 'units', E, window='1d', freshness=sup['freshness_days']),
              _ev('units_per_day', round(r['velocity_14d'] * sc, 1) if sc else None, 'units', E, source='order_lines'),
              _ev('days_to_next_receipt', r['days_to_next'], 'days', E, window='open POs', source='inbound_pos')]
        sentence = (f'{r["title"]} has {r["cover_days"]:.0f} days of stock. The next PO lands {_day(eta)}, '
                    f'so it sells out around {_day(runs_out)} and is gone for {g14:.0f} days.')
        out.append(_finding('SUPPLY-R01', {'type': 'sku', 'id': r['sku'], 'label': r['title']}, sev, ev, sentence,
                            'PROD-C22', stake, _confidence(agree, sup['freshness_days'] < 2), [], E))
    return out


def rule_reorder(rd):
    sup = supply(rd)
    if sup['unavailable']:
        return _unavailable_all(rd, sup, 'SUPPLY-R02', 'Reorder points', 'sku', 'PROD-C22', 'high')
    sc, net28, E = sup['scale'], _net_28d(rd), rd.ends_on
    out = []
    for r in sup['rows']:
        if r['open_pos'] or r['reorder_point'] is None or r['on_hand'] >= r['reorder_point']:
            continue
        g14, g28, _ = gap_days(r)
        agree = 1 + (1 if r['cover_days_28'] is not None and r['cover_days_28'] < r['reorder_point'] / max(r['velocity_28d'], 1e-9) else 0)
        stake = None
        if sc is not None and r['net_per_unit'] is not None and g14 is not None:
            stake = _money(g14 * r['velocity_14d'] * sc * r['net_per_unit'],
                           'max(0, lead_days - cover_days) * units_per_day_14d * net_per_unit',
                           {'lead_days': r['lead_days'], 'cover_days': r['cover_days'],
                            'units_per_day_14d': round(r['velocity_14d'] * sc, 1), 'net_per_unit': r['net_per_unit']},
                           f'{VELOCITY_DAYS}d')
        usd = stake['usd'] if stake else None
        sev = 'critical' if r['hero'] and g14 and agree >= 2 else _severity(usd, net28, agree)
        ev = [_ev('on_hand_units', scaled(r['on_hand'], sc), 'units', E, scaled(r['reorder_point'], sc), 'threshold',
                  window='1d', freshness=sup['freshness_days']),
              _ev('reorder_point_units', scaled(r['reorder_point'], sc), 'units', E, source='order_lines'),
              _ev('safety_stock_units', scaled(r['safety_units'], sc), 'units', E, window=f'{SIGMA_DAYS}d',
                  source='order_lines'),
              _ev('lead_time_days', r['lead_days'], 'days', E, window=f'{LEAD_LOOKBACK}d', source='inbound_pos'),
              _ev('stock_cover_days', r['cover_days'], 'days', E, r['lead_days'], 'threshold',
                  freshness=sup['freshness_days'])]
        sentence = (f'{r["title"]} has {_fmt_int(scaled(r["on_hand"], sc) or 0)} units against a reorder point of '
                    f'{_fmt_int(scaled(r["reorder_point"], sc) or 0)}, and no PO is open. '
                    f'A PO placed today lands in {r["lead_days"]:.0f} days. Stock lasts {r["cover_days"]:.0f} days.')
        out.append(_finding('SUPPLY-R02', {'type': 'sku', 'id': r['sku'], 'label': r['title']}, sev, ev, sentence,
                            'PROD-C22', stake, _confidence(agree, sup['freshness_days'] < 2), [], E,
                            money_reason=None if stake else 'no sales in the window'))
    return out


def _margin_gate_after(rd, day):
    """True when the brain holds a margin gate decision dated on or after `day`."""
    for r in rd.records('decisions'):
        text = f'{r.get("id", "")} {r.get("text") or ""}'.lower()
        if 'margin gate' in text or 'margin_gate' in text:
            if (r.get('date') or '') >= day:
                return True
    return False


def landed_moves(rd):
    """SKUs whose current landed cost differs from the row before by more than LANDED_MOVE, changed in the last
    365 days, with no margin gate record since the change. Shared with api.py."""
    sup = supply(rd)
    if sup['unavailable'] or not sup['landed_known']:
        return []
    since = _d(rd.ends_on - timedelta(days=LEAD_LOOKBACK))
    out = []
    for r in sup['rows']:
        new, old = r['landed_cost'], r['landed_prev']
        if new is None or not old or r['landed_from'] < since:
            continue
        move = new / old - 1
        if abs(move) > LANDED_MOVE and not _margin_gate_after(rd, r['landed_from']):
            out.append(dict(r, move=round(move, 4)))
    return out


def rule_landed(rd):
    """One finding for the brand: a supplier price change usually moves many SKUs on one date, and one margin
    recheck covers them all. Evidence names the 3 SKUs with the most money behind the move."""
    sup = supply(rd)
    E = rd.ends_on
    if sup['unavailable']:
        return _unavailable_all(rd, sup, 'SUPPLY-R03', 'Landed cost', 'sku', 'PROD-C23', 'medium')
    entity = {'type': 'brand', 'id': 'landed_cost', 'label': 'Landed cost per SKU'}
    if not sup['landed_known']:
        return [_finding('SUPPLY-R03', entity, 'medium', [],
                         'Landed cost per SKU is unavailable: no cost file is on record.', 'PROD-C23', None, 0.1, [],
                         E, status='unavailable', money_reason='inputs unavailable',
                         unavailable={'inputs': ['finance_inputs.cogs_landed'], 'connector': 'finance inputs',
                                      'fix': 'Enter landed cost per SKU with the date each cost took effect.'})]
    moves = landed_moves(rd)
    if not moves:
        return []
    sc, net28 = sup['scale'], _net_28d(rd)
    ref = f'{rd.brand}.economics.gross_margin_model'
    refs = [ref] if rd.record(ref) else []
    ups = [m for m in moves if m['move'] > 0]
    extra = sum((m['landed_cost'] - m['landed_prev']) * m['units_28d'] for m in ups)
    stake = None
    if sc is not None and ups:
        stake = _money(extra * sc, 'sum over SKUs of (landed_cost_now - landed_cost_before) * units_28d',
                       {'skus': len(ups), 'extra_cost_per_28d_sample': round(extra, 2), 'scale': sc}, f'{WINDOW}d')
    usd = stake['usd'] if stake else None
    top = sorted(moves, key=lambda m: (-(m['landed_cost'] - m['landed_prev']) * m['units_28d'], m['sku']))[:3]
    ev = [_ev('skus_with_landed_move', len(moves), 'count', E, len(sup['rows']), 'threshold', window='current',
              source='finance_inputs')]
    for m in top:
        ev.append(_ev(f'landed_cost_per_unit:{m["sku"]}', m['landed_cost'], 'usd', E, m['landed_prev'], 'threshold',
                      window='current', source='finance_inputs',
                      freshness=(E - date.fromisoformat(m['landed_from'])).days))
    first = min(m['landed_from'] for m in moves)
    took = date.fromisoformat(first)
    med = statistics.median(m['move'] for m in moves)
    sentence = (f'{len(moves)} of {len(sup["rows"])} SKUs cost {abs(med) * 100:.0f} percent '
                f'{"more" if med > 0 else "less"} to land since {_day(took)} {took.year}. '
                f'No margin check is on record since then.')
    return [_finding('SUPPLY-R03', entity, _severity(usd, net28, 1), ev, sentence, 'PROD-C23', stake,
                     _confidence(1), refs, E, money_reason=None if stake else 'cost went down')]


def rule_dead(rd):
    sup = supply(rd)
    E = rd.ends_on
    if sup['unavailable']:
        return _unavailable_all(rd, sup, 'SUPPLY-R10', 'Dead stock', 'sku', 'PROD-C27', 'medium')
    sc, net28 = sup['scale'], _net_28d(rd)
    out = []
    for r in sup['rows']:
        aged = max(0, r['on_hand'] - r['received_recent'])
        cover = r['cover_days_28']
        if not aged or (cover is not None and cover <= SLOW_COVER):
            continue
        stake = None
        if sc is not None and r['landed_cost'] is not None:
            stake = _money(aged * sc * r['landed_cost'], 'aged_units * landed_cost_per_unit',
                           {'aged_units': scaled(aged, sc), 'landed_cost_per_unit': r['landed_cost']}, 'now')
        usd = stake['usd'] if stake else None
        ev = [_ev('aged_units', scaled(aged, sc), 'units', E, window=f'{DEAD_DAYS}d', source='inbound_pos'),
              _ev('stock_cover_days', cover, 'days', E, SLOW_COVER, 'threshold', window='28d', source='order_lines')]
        sentence = (f'{r["title"]} has {_fmt_int(scaled(aged, sc) or 0)} units older than {DEAD_DAYS} days and '
                    + (f'{cover:.0f} days of cover at the current pace.' if cover is not None else 'no sales in 28 days.'))
        out.append(_finding('SUPPLY-R10', {'type': 'sku', 'id': r['sku'], 'label': r['title']},
                            _severity(usd, net28, 1), ev, sentence, 'PROD-C27', stake, _confidence(1), [], E,
                            money_reason=None if stake else 'no landed cost on file'))
    return out


def rule_missing(rd):
    out = []
    for rule_id, name, entity, table, connector, fix, severity, cap in MISSING:
        if rd.has_table(table):
            continue  # round 0 reads only the tables this brand has; a connected table is evaluated in a later round
        refs = []
        if rule_id == 'SUPPLY-R14':
            ref = f'{rd.brand}.economics.monthly_revenue_shape'
            refs = [ref] if rd.record(ref) else []
        out.append(_finding(rule_id, {'type': entity[0], 'id': entity[1], 'label': entity[2]}, severity, [],
                            f'{name} is unavailable: {table} is not connected.', cap, None, 0.1, refs, rd.ends_on,
                            status='unavailable', money_reason='inputs unavailable',
                            unavailable={'inputs': [table], 'connector': connector, 'fix': fix}))
    return out


def run(brand, window=None, data=None):
    """Findings for one brand, sorted by severity then money at stake. `window` is {ends_on} or None."""
    ends_on = date.fromisoformat(window['ends_on']) if window and window.get('ends_on') else last_full_day(data, brand)
    return findings(Reader(data, brand, ends_on))


def findings(rd):
    """run() on a Reader the caller already holds, so api.py reuses its reads."""
    out = rule_stockout(rd) + rule_reorder(rd) + rule_landed(rd) + rule_dead(rd) + rule_missing(rd)
    out.sort(key=lambda f: (SEVERITY_ORDER[f['severity']], -((f.get('money_at_stake') or {}).get('usd') or -1), f['id']))
    return out
