"""API for screen 13-affiliate-marketplace-ads. Endpoints under /api/13-affiliate-marketplace-ads/.

  GET /api/13-affiliate-marketplace-ads/        the whole screen: tiles, partner table, commission tiers, Amazon block,
                                                retail media, billing reconciliation, 12-month chart, findings (audit)
  GET /api/13-affiliate-marketplace-ads/audit   the audit findings only (audit.py, contracts/audit.md shape)

Query: brand (default bombas), window (Nd, default 28d). Read-only: it reads app/data/brands/<brand>/ through
data/tables.py and app/brain/<brand>/ through brain/store.py, and writes nothing.

Where the numbers come from
  affiliate partners      `affiliate_clicks_orders` (affiliate network) joined to `commission_tiers` (brand record).
                          One row per click or per order: affiliate_id, partner_type, click_at, order_at, order_id,
                          amount, ip_or_isp. An order row with no click_at is an order the network credited with no click.
  coupon redemptions      `coupon_redemptions`: code, affiliate_id, redeemed_at, order_id, amount.
  Amazon Ads              `amazon_ads_rows`: Sponsored Products report by ASIN (asin, date, spend, sales).
  affiliate invoice       `affiliate_invoices`: cycle, network_owed. Checked against commission on tracked orders.
  Amazon listings         brain `marketplaces` records (public sample, not signed in). Real, not simulated.
None of the affiliate or Amazon Ads tables is in the Bombas simulated set (data/brands/bombas/README.md), so those
parts read unavailable with the connector that fills them. Every missing value is null, never 0.
"""
import importlib.util
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parents[1]
SLUG = '13-affiliate-marketplace-ads'
DEFAULT_BRAND = 'bombas'

# Rule constants. audit.py reads the same ones, so the table and the findings never disagree.
FAST_SECONDS = 10            # click to order faster than a person can browse and pay
FAST_MIN_ORDERS = 3          # fast orders in the window before an affiliate is flagged
NO_CLICK_MIN_ORDERS = 3      # orders credited with 0 clicks in the window before an affiliate is flagged
LEAK_MIN_REDEMPTIONS = 10    # redemptions of one code before the leak share is read
LEAK_SHARE_MIN = 0.30        # share of a code's redemptions with no click from its affiliate
COOKIE_DAYS = 30             # a click counts for an order placed up to this many days later
INVOICE_GAP_MIN = 0.02       # invoice vs tracked commission gap that counts (room spec: 2 percent)
CHART_MONTHS = 12
PARTNER_TYPES = ['content', 'coupon', 'loyalty', 'influencer']

CONNECTORS = {
    'affiliate_clicks_orders': ('affiliate network', 'Connect the affiliate network (Impact, Refersion or ShareASale) read-only.'),
    'commission_tiers': ('brand record', 'Add the commission tier record: rate by partner type and new or returning customer.'),
    'coupon_redemptions': ('Shopify discounts', 'Connect Shopify discount redemptions and tag each affiliate code.'),
    'amazon_ads_rows': ('Amazon Ads', 'Connect Amazon Ads read-only, or upload the Sponsored Products report by ASIN.'),
    'affiliate_invoices': ('affiliate network invoices', 'Upload the network invoice or payout report for each cycle.'),
}
RETAIL_MEDIA = [
    ('Amazon', 'Amazon Ads', 'amazon'), ('Walmart', 'Walmart Connect', 'walmart'), ('Target', 'Target Roundel', 'target'),
    ('Instacart', 'Instacart Ads', 'instacart'), ('DoorDash', 'DoorDash Ads', 'doordash'), ('Gopuff', 'Gopuff Ads', 'gopuff'),
]


def _load(name, path):
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def metrics():
    return _load('ecomos_metrics', APP / 'metrics.py')


def brain(brand, today):
    """The brand brain (store.py imports `validate` by bare name, so its folder goes on the path)."""
    folder = str(APP / 'brain')
    if folder not in sys.path:
        sys.path.insert(0, folder)
    store = _load('ecomos_brain_store', APP / 'brain' / 'store.py')
    return store.Brain(brand, today=today)


class Unavailable(Exception):
    def __init__(self, reason, fix=None):
        super().__init__(reason)
        self.reason, self.fix = reason, fix


def unavailable_table(name):
    connector, fix = CONNECTORS[name]
    return {'unavailable': True, 'table': name, 'reason': f'the {name} table is not in this data set',
            'connector': connector, 'fix': fix}


class Win:
    def __init__(self, end, days):
        self.end, self.days = end, days
        self.start = end - timedelta(days=days - 1)
        self.s, self.e = self.start.isoformat(), end.isoformat()

    def has(self, day):
        return day is not None and self.s <= str(day)[:10] <= self.e

    def shift(self, k):
        return Win(self.end - timedelta(days=self.days * k), self.days)

    def dict(self):
        return {'label': f'{self.days}d', 'start': self.s, 'end': self.e, 'days': self.days}


def parse_days(window):
    m = re.fullmatch(r'(\d{1,3})d', str(window or '28d'))
    if not m or not 7 <= int(m.group(1)) <= 120:
        raise ValueError('window must look like 28d, from 7d to 120d')
    return int(m.group(1))


def ratio(a, b, nd=4):
    return round(a / b, nd) if (a is not None and b) else None


def usd(x):
    return None if x is None else round(x, 2)


def ts(v):
    if not v:
        return None
    return datetime.fromisoformat(str(v).replace('Z', '+00:00')).replace(tzinfo=None)


# ---------------------------------------------------------------- the data

class Screen:
    """One brand's inputs for this screen. Each table is rows or None (not connected)."""

    def __init__(self, brand):
        self.brand = brand
        try:
            self.data = metrics().resolve(None, {'brand': brand})
        except ValueError:
            raise Unavailable(f'no data folder for brand {brand}', fix='data layer')
        info = self.data.brand
        if not info.get('as_of'):
            raise Unavailable('the brand has no last full day', fix='tables.json as_of')
        self.as_of = date.fromisoformat(info['as_of'])
        self.simulated = bool(info.get('simulated'))
        self.freshness_days = 1
        self.tables = {name: self._table(name) for name in CONNECTORS}
        self.brain = brain(brand, self.as_of)

    def _table(self, name):
        try:
            rows = self.data.table(name)
        except (KeyError, ValueError):
            return None
        return rows or None

    def rows(self, name):
        return self.tables.get(name)

    def tier_rates(self):
        """affiliate_id -> {partner_type, rate}; rate is the new-customer rate when both are on file."""
        out = {}
        for r in self.rows('commission_tiers') or []:
            a = out.setdefault(r['affiliate_id'], {'partner_type': r.get('partner_type'), 'rate': None})
            if r.get('rate') is not None and (a['rate'] is None or r.get('customer_status') in (None, 'new')):
                a['rate'] = r['rate']
        return out

    # ---- brain: Amazon listings and channels

    def listings(self):
        recs = [r for r in self.brain.records('marketplaces') if r.get('field') == 'amazon_listing']
        presence = self.presence()
        resellers = set((presence or {}).get('value', {}).get('resellers_seen') or [])
        out = []
        for r in recs:
            v = r.get('value') or {}
            price = listing_price(v.get('price'))
            in_stock = price is not None and 'unavailable' not in str(v.get('availability') or '').lower()
            out.append({'asin': v.get('asin'), 'title': v.get('title'), 'line': v.get('line'), 'rating': v.get('rating'),
                        'ratings': v.get('review_count'), 'price': price, 'in_stock': in_stock,
                        'seller': v.get('seller_shown'),
                        'sold_by': None if not v.get('seller_shown') else 'reseller' if v['seller_shown'] in resellers else 'brand',
                        'captured_at': (r.get('source') or {}).get('captured_at'), 'brain_ref': r['id']})
        return out

    def presence(self):
        return next((r for r in self.brain.records('marketplaces') if r.get('field') == 'amazon_presence'), None)

    def channel_refs(self, word):
        return [r['id'] for r in self.brain.records('channels') if re.search(r'\b' + word + r'\b', (r.get('text') or '').lower())]


def listing_price(text):
    m = re.match(r'\s*\$([\d,]+(?:\.\d+)?)', str(text or ''))
    return float(m.group(1).replace(',', '')) if m else None


# ---------------------------------------------------------------- rules on rows (pure, so tests can feed them)

def partners(events, tiers, win, redemptions=None):
    """Per affiliate in the window: clicks, orders, sales, commission and fraud flags by rule."""
    by = {}
    for r in events or []:
        a = by.setdefault(r['affiliate_id'], {'affiliate_id': r['affiliate_id'], 'name': r.get('affiliate_name') or r['affiliate_id'],
                                              'partner_type': r.get('partner_type'), 'clicks': 0, 'orders': set(), 'sales': 0.0,
                                              'fast_orders': 0, 'no_click_orders': 0})
        if win.has(r.get('click_at')):
            a['clicks'] += 1
        if r.get('order_id') and win.has(r.get('order_at')):
            if r['order_id'] not in a['orders']:
                a['orders'].add(r['order_id'])
                a['sales'] += r.get('amount') or 0
                c, o = ts(r.get('click_at')), ts(r.get('order_at'))
                if c is None:
                    a['no_click_orders'] += 1
                elif (o - c).total_seconds() < FAST_SECONDS:
                    a['fast_orders'] += 1
    leaks = {c['affiliate_id']: c for c in coupon_leaks(redemptions, events, win)}
    out = []
    for a in by.values():
        tier = (tiers or {}).get(a['affiliate_id'], {})
        rate = tier.get('rate')
        orders = len(a['orders'])
        flags = []
        if a['fast_orders'] >= FAST_MIN_ORDERS:
            flags.append(f"{a['fast_orders']} orders under {FAST_SECONDS}s from click")
        if orders >= NO_CLICK_MIN_ORDERS and a['clicks'] == 0:
            flags.append(f'{orders} orders, 0 clicks')
        if a['affiliate_id'] in leaks:
            flags.append(f"code leak {leaks[a['affiliate_id']]['leak_share'] * 100:.0f} percent")
        out.append({'affiliate_id': a['affiliate_id'], 'name': a['name'],
                    'partner_type': a['partner_type'] or tier.get('partner_type'), 'clicks': a['clicks'], 'orders': orders,
                    'sales': usd(a['sales']), 'cvr': ratio(orders, a['clicks']), 'rate': rate,
                    'commission': usd(a['sales'] * rate) if rate is not None else None,
                    'fast_orders': a['fast_orders'], 'no_click_orders': a['no_click_orders'], 'flags': flags})
    out.sort(key=lambda p: (-(p['sales'] or 0), p['affiliate_id']))
    return out


def no_click_affiliates(rows):
    """Insight rule: an affiliate credited with orders but no clicks in the window."""
    return [p for p in rows if p['orders'] >= NO_CLICK_MIN_ORDERS and p['clicks'] == 0]


def coupon_leaks(redemptions, events, win):
    """Insight rule: an affiliate's code redeemed on orders with no click from that affiliate in the cookie window.

    A code on a deal site gets used by shoppers the affiliate never sent, and the affiliate is paid for them."""
    if not redemptions:
        return []
    clicked = {}
    for r in events or []:
        if r.get('click_at') and r.get('order_id'):
            c, o = ts(r['click_at']), ts(r.get('order_at'))
            if o is None or (o - c).days <= COOKIE_DAYS:
                clicked.setdefault(r['affiliate_id'], set()).add(r['order_id'])
    codes = {}
    for r in redemptions:
        if not r.get('affiliate_id') or not win.has(r.get('redeemed_at')):
            continue
        c = codes.setdefault((r['affiliate_id'], r['code']), {'affiliate_id': r['affiliate_id'], 'code': r['code'],
                                                              'redemptions': 0, 'leaked': 0, 'leaked_sales': 0.0,
                                                              'leaked_sales_known': True})
        c['redemptions'] += 1
        if r.get('order_id') not in clicked.get(r['affiliate_id'], set()):
            c['leaked'] += 1
            if r.get('amount') is None:
                c['leaked_sales_known'] = False
            else:
                c['leaked_sales'] += r['amount']
    out = []
    for c in codes.values():
        c['leak_share'] = ratio(c['leaked'], c['redemptions'])
        if c['redemptions'] >= LEAK_MIN_REDEMPTIONS and c['leak_share'] >= LEAK_SHARE_MIN:
            c['leaked_sales'] = usd(c['leaked_sales']) if c.pop('leaked_sales_known') else None
            out.append(c)
        else:
            c.pop('leaked_sales_known')
    out.sort(key=lambda c: (-c['leaked'], c['code']))
    return out


def months_back(end, n):
    y, m = end.year, end.month
    out = []
    for _ in range(n):
        out.append(f'{y}-{m:02d}')
        y, m = (y, m - 1) if m > 1 else (y - 1, 12)
    return out[::-1]


def orders_by_type(events, end):
    """Affiliate orders by partner type per month, 12 months to the window end. None per series when not connected."""
    months = months_back(end, CHART_MONTHS)
    partial = end.month == (end + timedelta(days=1)).month
    out = {'labels': months, 'partial_last': partial, 'series': []}
    if events is None:
        out['series'] = [{'name': t, 'values': [None] * CHART_MONTHS} for t in PARTNER_TYPES]
        out['unavailable'] = unavailable_table('affiliate_clicks_orders')
        return out
    seen, counts = set(), {}
    for r in events:
        if not r.get('order_id') or not r.get('order_at') or r['order_id'] in seen:
            continue
        mk = str(r['order_at'])[:7]
        if mk in months:
            seen.add(r['order_id'])
            t = r.get('partner_type') or 'unknown'
            counts.setdefault(t, {m: 0 for m in months})[mk] += 1
    out['series'] = [{'name': t, 'values': [counts[t][m] for m in months]} for t in sorted(counts)]
    out['unavailable'] = None
    return out


# ---------------------------------------------------------------- blocks

def amazon_block(s, win):
    listings = s.listings()
    ads = s.rows('amazon_ads_rows')
    per = {}
    for r in ads or []:
        if win.has(r.get('date')):
            p = per.setdefault(r['asin'], [0.0, 0.0])
            p[0] += r.get('spend') or 0
            p[1] += r.get('sales') or 0
    for l in listings:
        if ads is None:
            l['spend'] = l['ad_sales'] = l['acos'] = None
        else:
            sp, sa = per.get(l['asin'], (None, None))
            l['spend'], l['ad_sales'] = usd(sp), usd(sa)
            l['acos'] = ratio(sp, sa)
    in_stock = [l for l in listings if l['in_stock']]
    resold = [l for l in in_stock if l['sold_by'] == 'reseller']
    pres = s.presence()
    pv = (pres or {}).get('value') or {}
    total_spend = sum(p[0] for p in per.values()) if ads is not None else None
    total_sales = sum(p[1] for p in per.values()) if ads is not None else None
    return {'listings': listings, 'asins_read': len(listings), 'in_stock': len(in_stock), 'resold_in_stock': len(resold),
            'reseller_share': ratio(len(resold), len(in_stock)), 'resellers': sorted({l['seller'] for l in resold}),
            'lowest_reseller_price': min((l['price'] for l in resold), default=None),
            'brand_store': pv.get('brand_store'), 'aplus_seen': pv.get('aplus_content_seen'),
            'lines_not_found': pv.get('lines_not_found') or [], 'presence_ref': (pres or {}).get('id'),
            'presence_text': (pres or {}).get('text'), 'captured_at': ((pres or {}).get('source') or {}).get('captured_at'),
            'ads': unavailable_table('amazon_ads_rows') if ads is None else
            {'unavailable': False, 'spend': usd(total_spend), 'sales': usd(total_sales), 'acos': ratio(total_spend, total_sales)},
            'source': 'brain.marketplaces: public sample, not signed in. Not simulated.'}


def retail_media(s):
    out = []
    for label, network, word in RETAIL_MEDIA:
        refs = s.channel_refs(word) if word != 'amazon' else [r['id'] for r in s.brain.records('marketplaces')
                                                               if r.get('field') == 'amazon_presence']
        out.append({'platform': label, 'network': network, 'brief_status': None, 'reported_roas': None,
                    'in_brain': bool(refs), 'brain_refs': refs,
                    'reason': 'no brief on file and no connector to this ads console'})
    return {'rows': out, 'note': 'Status and ROAS are entered by hand once a brief exists. Live numbers stay unavailable '
                                 'until the ads console is connected.'}


def billing(s, parts):
    inv = s.rows('affiliate_invoices')
    if inv is None:
        return unavailable_table('affiliate_invoices')
    last = sorted(inv, key=lambda r: str(r.get('cycle')))[-1]
    tracked = None if any(p['commission'] is None for p in parts) or not parts else usd(sum(p['commission'] for p in parts))
    owed = last.get('network_owed')
    return {'unavailable': tracked is None, 'cycle': last.get('cycle'), 'network_owed': usd(owed), 'tracked_commission': tracked,
            'gap': usd(owed - tracked) if (owed is not None and tracked is not None) else None,
            'gap_share': ratio(owed - tracked, tracked) if (owed is not None and tracked) else None,
            'reason': None if tracked is not None else 'commission on tracked orders needs a rate for every partner',
            'fix': None if tracked is not None else CONNECTORS['commission_tiers'][1]}


def commission_table(s):
    tiers = s.rows('commission_tiers')
    if tiers is None:
        grid = [{'partner_type': t, 'new_rate': None, 'returning_rate': None, 'partners': None} for t in PARTNER_TYPES]
        return {'unavailable': unavailable_table('commission_tiers'), 'rows': grid}
    grid = {}
    for r in tiers:
        g = grid.setdefault(r.get('partner_type') or 'unknown', {'partner_type': r.get('partner_type') or 'unknown',
                                                                 'new_rate': None, 'returning_rate': None, 'partners': set()})
        g['partners'].add(r['affiliate_id'])
        key = 'returning_rate' if r.get('customer_status') == 'returning' else 'new_rate'
        if r.get('rate') is not None:
            g[key] = r['rate'] if g[key] is None else max(g[key], r['rate'])
    rows = [dict(g, partners=len(g['partners'])) for g in grid.values()]
    return {'unavailable': None, 'rows': sorted(rows, key=lambda g: g['partner_type'])}


def tiles(s, win, parts, amazon):
    ev = s.rows('affiliate_clicks_orders')
    aff = unavailable_table('affiliate_clicks_orders')
    ads = amazon['ads']
    return [
        {'id': 'affiliate_orders', 'name': 'Affiliate orders', 'plain': 'orders the network credits',
         'value': sum(p['orders'] for p in parts) if ev is not None else None, 'unit': 'n',
         'unavailable_reason': None if ev is not None else 'No affiliate network is connected.',
         'fix': None if ev is not None else aff['connector'], 'simulated': s.simulated},
        {'id': 'amazon_acos', 'name': 'Amazon ACoS', 'plain': 'ad spend / ad sales, Sponsored Products',
         'value': None if ads.get('unavailable') else ads['acos'], 'unit': '%', 'higher_is_better': False,
         'unavailable_reason': 'Amazon Ads is not connected.' if ads.get('unavailable') else None,
         'fix': ads.get('connector') if ads.get('unavailable') else None, 'simulated': s.simulated},
        {'id': 'amazon_reseller_share', 'name': 'Amazon listings sold by resellers',
         'plain': f"{amazon['resold_in_stock']} of {amazon['in_stock']} in-stock listings, public sample",
         'value': amazon['reseller_share'], 'unit': '%', 'higher_is_better': False,
         'unavailable_reason': None if amazon['reseller_share'] is not None else 'No in-stock listing in the brain sample.',
         'fix': None if amazon['reseller_share'] is not None else 'brain marketplaces', 'simulated': False,
         'freshness': amazon['captured_at']},
    ]


def build(brand=DEFAULT_BRAND, window='28d'):
    days = parse_days(window)
    try:
        s = Screen(brand)
    except Unavailable as exc:
        return {'screen': SLUG, 'brand': brand, 'unavailable': True, 'reason': exc.reason, 'fix': exc.fix}
    win = Win(s.as_of, days)
    ev = s.rows('affiliate_clicks_orders')
    red = s.rows('coupon_redemptions')
    parts = partners(ev, s.tier_rates(), win, red) if ev is not None else []
    amazon = amazon_block(s, win)
    out = {'screen': SLUG, 'brand': brand, 'simulated': s.simulated, 'as_of': s.as_of.isoformat(), 'window': win.dict(),
           'unavailable': False}
    out['tiles'] = tiles(s, win, parts, amazon)
    out['partners'] = {'unavailable': unavailable_table('affiliate_clicks_orders') if ev is None else None, 'rows': parts,
                       'rules': {'fast': f'{FAST_MIN_ORDERS} or more orders under {FAST_SECONDS}s from click',
                                 'no_click': f'{NO_CLICK_MIN_ORDERS} or more orders with 0 clicks',
                                 'leak': f"{LEAK_SHARE_MIN * 100:.0f} percent or more of a code's redemptions "
                                         f'(at least {LEAK_MIN_REDEMPTIONS}) with no click from its affiliate in {COOKIE_DAYS} days'}}
    out['commission_tiers'] = commission_table(s)
    out['amazon'] = amazon
    out['retail_media'] = retail_media(s)
    out['billing'] = billing(s, parts) if ev is not None else unavailable_table('affiliate_invoices')
    out['chart'] = orders_by_type(ev, s.as_of)
    out['connectors'] = [dict(unavailable_table(n), connected=s.rows(n) is not None) for n in CONNECTORS]
    return out


def handle(req):
    brand = req.arg('brand', DEFAULT_BRAND)
    window = req.arg('window', '28d')
    if req.method != 'GET':
        return 405, {'error': 'method not allowed'}
    try:
        if req.path in ([], ['summary']):
            out = build(brand, window)
            if not out.get('unavailable'):
                out['findings'] = _audit().run(brand, {'ends_on': out['as_of'], 'days': parse_days(window)})
            return out
        if req.path == ['audit']:
            return {'screen': SLUG, 'brand': brand,
                    'findings': _audit().run(brand, {'days': parse_days(window)}), 'rules': _audit().RULES}
    except ValueError as exc:
        return 400, {'error': str(exc)}
    return 404, {'error': 'not found'}


def _audit():
    """audit.py, loaded fresh so an edit shows on the next request (the server reloads api.py the same way)."""
    spec = importlib.util.spec_from_file_location('screen_audit_13_affiliate', HERE / 'audit.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
