"""API for screen 20-marketplaces. Endpoints under /api/20-marketplaces/.

  GET /api/20-marketplaces/        the whole screen: tiles, 12-month chart, Amazon listings, the data it needs, findings
  GET /api/20-marketplaces/audit   the audit findings only (audit.py, contracts/audit.md shape)

Query: brand (default bombas), window (Nd, default 28d). Read-only: it reads app/data/brands/<brand>/ through
metrics.resolve (data/tables.py) and app/brain/<brand>/ through brain/store.py, and writes nothing.

Where the numbers come from
  marketplace sales     aggregate `marketplace_monthly` (month, marketplace, net_sales). For Bombas it is a simulated
                        fixture at the brain's marketplace share of revenue, split Amazon 80 and TikTok Shop 20. It is not
                        in `orders`, so it is added to DTC `monthly` and `wholesale_monthly` for the share of revenue.
  Amazon listings       brain `marketplaces`: a public sample (search pull plus offer pages, not signed in). Real, not
                        simulated. One row per ASIN; the 2 capture kinds are merged by ASIN.
  Amazon reviews        `reviews` rows with review_source amazon, counted with one GROUP BY on data.sqlite.
  marketplace trust     brain `objection_ladders` record marketplace_trust (fake listings and short packs).
Listing health, Buy Box, account health, settlements, dark stores, ad credits, IPI, traffic, feeds and compliance
docs have no table in the Bombas set, so they read unavailable with the connector that fills them. Never 0.

Screen 13 owns Amazon Ads and reseller presence on Amazon (AFFM-R04). This screen is the marketplace channel itself.
"""
import importlib.util
import re
import statistics
import sys
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parents[1]
SLUG = '20-marketplaces'
DEFAULT_BRAND = 'bombas'

# Rule constants. audit.py reads the same ones.
MIN_RATINGS = 5          # room spec: review_rating_avg unavailable under 5 reviews on a SKU-channel pair
RATING_GAP = 0.3         # stars below the median of the brand's other ASINs on the same channel
DROP_MIN = 0.10          # last full month's daily sales rate this far under the 4-month median
TRAILING = 4             # windows in an own median
CHART_MONTHS = 12
MARKETPLACES = {'amazon': 'Amazon', 'tiktok_shop': 'TikTok Shop', 'walmart': 'Walmart', 'target_plus': 'Target Plus',
                'ebay': 'eBay'}

# The room spec's tables (FEATURES.md, "Data this screen needs"): name -> (connector, fix).
CONNECTORS = {
    'marketplace_listings': ('seller portal exports', 'Connect Amazon Seller Central, Walmart Seller Center and TikTok Shop read-only, or upload each listing export.'),
    'buybox_snapshots': ('Buy Box tracker', 'Connect a Buy Box tracker (Keepa or a seller tool) for every live ASIN.'),
    'map_policy': ('brand record', 'Add the MAP price per SKU to the brand brain.'),
    'amazon_ads_rows': ('Amazon Ads', 'Connect Amazon Ads read-only so the rule knows which ASINs run ads.'),
    'account_health_metrics': ('account health exports', 'Upload the account health page from each seller portal each week.'),
    'rapid_delivery_orders': ('rapid delivery exports', 'Connect Instacart, DoorDash or Gopuff order and ad exports.'),
    'settlement_reports': ('settlement reports', 'Upload each marketplace settlement report per payout cycle.'),
    'dark_store_inventory': ('dark store feed', 'Connect the platform dark store inventory feed.'),
    'ad_credit_ledger': ('ad credit ledger', 'Upload each platform ad credit statement with its expiry date.'),
    'amazon_inventory': ('Amazon inventory report', 'Connect the Seller Central inventory and IPI report.'),
    'amazon_traffic_sales': ('Amazon Business Reports', 'Connect the Seller Central Business Report by ASIN (sessions and units).'),
    'compliance_docs': ('compliance docs', 'Add FTC Care Labeling and Prop 65 documents per SKU with expiry dates.'),
    'catalogue_feed': ('catalogue feed', 'Point the screen at the shared catalogue feed and its last sync time.'),
}


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


def ratio(a, b, nd=4):
    return round(a / b, nd) if (a is not None and b) else None


def usd(x):
    return None if x is None else round(x, 2)


def parse_days(window):
    m = re.fullmatch(r'(\d{1,3})d', str(window or '28d'))
    if not m or not 7 <= int(m.group(1)) <= 120:
        raise ValueError('window must look like 28d, from 7d to 120d')
    return int(m.group(1))


def month_days(month):
    y, m = int(month[:4]), int(month[5:7])
    nxt = date(y + (m == 12), m % 12 + 1, 1)
    return (nxt - date(y, m, 1)).days


def months_back(end_month, n):
    y, m = int(end_month[:4]), int(end_month[5:7])
    out = []
    for _ in range(n):
        out.append(f'{y}-{m:02d}')
        y, m = (y, m - 1) if m > 1 else (y - 1, 12)
    return out[::-1]


def last_full_month(end):
    """The last month that ends on or before `end`."""
    if (end + timedelta(days=1)).day == 1:
        return end.strftime('%Y-%m')
    first = end.replace(day=1) - timedelta(days=1)
    return first.strftime('%Y-%m')


def price_of(v):
    if isinstance(v, (int, float)):
        return round(float(v), 2)
    m = re.match(r'\s*\$([\d,]+(?:\.\d+)?)', str(v or ''))
    return round(float(m.group(1).replace(',', '')), 2) if m else None


def stock_of(text):
    t = str(text or '').strip().lower()
    if not t:
        return None
    if 'unavailable' in t or 'out of stock' in t:
        return False
    return True if 'in stock' in t else None


# ---------------------------------------------------------------- the data

class Screen:
    """One brand's inputs for this screen. Each spec table is rows or None (not connected)."""

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

    def agg(self, name):
        try:
            return self.data.table(name) or None
        except (KeyError, ValueError):
            return None

    def first_day(self):
        daily = self.agg('daily')
        return date.fromisoformat(min(r['date'] for r in daily)) if daily else None

    def amazon_review_count(self):
        """Reviews with review_source amazon, one GROUP BY. None when data.sqlite is absent."""
        try:
            rows = self.data._sql("SELECT review_source AS s, COUNT(*) AS n FROM reviews GROUP BY review_source")
        except Exception:
            return None
        return sum(r['n'] for r in rows if str(r['s'] or '').lower() == 'amazon')

    # ---- brain

    def listings(self):
        """Amazon listings in the brain, merged by ASIN. Real public sample, never simulated."""
        by = {}
        for r in self.brain.records('marketplaces'):
            if r.get('field') != 'amazon_listing':
                continue
            v = r.get('value') or {}
            asin = v.get('asin')
            if not asin:
                continue
            row = by.setdefault(asin, {'asin': asin, 'title': None, 'stars': None, 'ratings': None, 'price': None,
                                       'in_stock': None, 'availability': None, 'seller': None, 'captured_at': None,
                                       'brain_refs': []})
            row['brain_refs'].append(r['id'])
            title = v.get('title')
            if title and (row['title'] is None or len(title) < len(row['title'])):
                row['title'] = title
            for key, val in (('stars', v.get('stars', v.get('rating'))),
                             ('ratings', v.get('reviews_count', v.get('review_count'))),
                             ('price', price_of(v.get('price_usd', v.get('price')))),
                             ('seller', v.get('seller') or v.get('seller_shown')),
                             ('availability', v.get('availability') or None)):
                if val is not None and row[key] is None:
                    row[key] = val
            if row['in_stock'] is None:
                row['in_stock'] = stock_of(v.get('availability'))
            cap = (r.get('source') or {}).get('captured_at')
            if cap and (row['captured_at'] is None or cap > row['captured_at']):
                row['captured_at'] = cap
        out = sorted(by.values(), key=lambda l: (-(l['ratings'] or 0), l['asin']))
        for l in out:
            l['buyable'] = False if (l['in_stock'] is False or l['price'] is None) else (True if l['in_stock'] else None)
            l['problem'] = ('currently unavailable' if l['in_stock'] is False else
                            'no price shown' if l['price'] is None else None)
        return out

    def ladder(self, theme='marketplace_trust'):
        return next((r for r in self.brain.records('objection_ladders')
                     if (r.get('value') or {}).get('theme') == theme), None)


# ---------------------------------------------------------------- rules on rows (pure, so tests can feed them)

def rating_outliers(listings):
    """ASINs with at least MIN_RATINGS ratings whose stars sit RATING_GAP or more under the median of the others."""
    rated = [l for l in listings if l['stars'] is not None and (l['ratings'] or 0) >= MIN_RATINGS]
    out = []
    for l in rated:
        others = [o['stars'] for o in rated if o['asin'] != l['asin']]
        if len(others) < TRAILING:
            continue
        med = round(statistics.median(others), 2)
        if round(med - l['stars'], 2) >= RATING_GAP:
            out.append(dict(l, baseline=med, gap=round(med - l['stars'], 2), peers=len(others)))
    return sorted(out, key=lambda l: (l['stars'], -(l['ratings'] or 0), l['asin']))


def weighted_stars(listings):
    rated = [l for l in listings if l['stars'] is not None and (l['ratings'] or 0) >= MIN_RATINGS]
    n = sum(l['ratings'] for l in rated)
    return (round(sum(l['stars'] * l['ratings'] for l in rated) / n, 2) if n else None), n, len(rated)


def monthly_by_marketplace(rows):
    out = {}
    for r in rows or []:
        if r.get('net_sales') is not None:
            out.setdefault(r['marketplace'], {})[r['month']] = out.get(r['marketplace'], {}).get(r['month'], 0.0) + r['net_sales']
    return out


def share_drops(rows, totals, month, first_day=None):
    """Per marketplace: its share of all revenue in `month` against the median share of the 4 full months before it.

    Share, not sales, so a seasonal month (January after December) does not read as a drop. Fires when the share is
    DROP_MIN or more under the median. Months that start before the data does are partial and never count.
    Stake: (median share - share) x all revenue in the month."""
    out = []
    months = months_back(month, TRAILING + 1)
    ok = [m for m in months if totals.get(m) and (first_day is None or date.fromisoformat(m + '-01') >= first_day)]
    if len(ok) < TRAILING + 1:
        return out
    for mp, series in sorted(monthly_by_marketplace(rows).items()):
        if any(m not in series for m in months):
            continue
        shares = [series[m] / totals[m] for m in months[:-1]]
        med = statistics.median(shares)
        cur = series[month] / totals[month]
        drop = ratio(med - cur, med)
        if drop is not None and drop >= DROP_MIN:
            out.append({'marketplace': mp, 'label': MARKETPLACES.get(mp, mp), 'month': month, 'net_sales': usd(series[month]),
                        'share': round(cur, 4), 'median_share': round(med, 4), 'drop': drop, 'revenue': usd(totals[month]),
                        'windows_below': sum(1 for x in shares if cur < x), 'stake': usd((med - cur) * totals[month])})
    return out


def month_totals(rev):
    """All revenue per month, or no entry when any source is missing that month (never a partial sum)."""
    return {m: sum(v.values()) for m, v in rev.items() if None not in v.values()}


# ---------------------------------------------------------------- blocks

def revenue_months(s):
    """Per month: DTC, wholesale and marketplace net sales. None where a source has no row."""
    out = {}
    for name, key in (('monthly', 'dtc'), ('wholesale_monthly', 'wholesale'), ('marketplace_monthly', 'marketplace')):
        for r in s.agg(name) or []:
            if r.get('net_sales') is None:
                continue
            m = out.setdefault(r['month'], {'dtc': None, 'wholesale': None, 'marketplace': None})
            m[key] = (m[key] or 0.0) + r['net_sales']
    return out


def chart(s):
    rows = s.agg('marketplace_monthly')
    end = s.as_of.strftime('%Y-%m')
    labels = months_back(end, CHART_MONTHS)
    partial = last_full_month(s.as_of) != end
    if rows is None:
        return {'labels': labels, 'partial_last': partial, 'series': [{'name': n, 'values': [None] * CHART_MONTHS}
                                                                      for n in ('Amazon', 'TikTok Shop')],
                'unavailable': {'reason': 'no marketplace sales in this data set', 'fix': CONNECTORS['settlement_reports'][1]}}
    by = monthly_by_marketplace(rows)
    series = [{'name': MARKETPLACES.get(mp, mp), 'values': [usd(by[mp].get(m)) for m in labels]} for mp in sorted(by)]
    missing = [MARKETPLACES[k] for k in ('walmart', 'target_plus', 'ebay') if k not in by]
    return {'labels': labels, 'partial_last': partial, 'series': series, 'unavailable': None, 'not_connected': missing}


def tiles(s, listings):
    month = last_full_month(s.as_of)
    by = monthly_by_marketplace(s.agg('marketplace_monthly'))
    have = [mp for mp in by if month in by[mp]]
    sales = usd(sum(by[mp][month] for mp in have)) if have else None
    split = ', '.join(f'{MARKETPLACES.get(mp, mp)} ${by[mp][month]:,.0f}' for mp in sorted(have)) if have else None

    rev = revenue_months(s)
    first = s.first_day()
    last12 = months_back(month, 12)
    ok = all(m in rev and None not in rev[m].values() and (first is None or date.fromisoformat(m + '-01') >= first)
             for m in last12)
    share = ratio(sum(rev[m]['marketplace'] for m in last12), sum(sum(rev[m].values()) for m in last12)) if ok else None

    stars, n_ratings, n_asins = weighted_stars(listings)
    captured = max((l['captured_at'] for l in listings if l['captured_at']), default=None)
    return [
        {'id': 'marketplace_net_sales', 'name': 'Marketplace sales', 'plain': split or 'net sales on marketplaces',
         'value': sales, 'unit': '$', 'window': f'{month} (last full month)', 'simulated': s.simulated,
         'unavailable_reason': None if sales is not None else 'No marketplace sales for the last full month.',
         'fix': None if sales is not None else CONNECTORS['settlement_reports'][0]},
        {'id': 'marketplace_share', 'name': 'Marketplace share of revenue',
         'plain': 'marketplace / (site + wholesale + marketplace) net sales', 'value': share, 'unit': '%',
         'window': f'12 full months to {month}', 'simulated': s.simulated,
         'unavailable_reason': None if share is not None else 'A month in the last 12 has no site, wholesale or marketplace row.',
         'fix': None if share is not None else 'data layer'},
        {'id': 'amazon_rating', 'name': 'Amazon star rating',
         'plain': f'weighted by {n_ratings:,} ratings on {n_asins} ASINs, public sample' if stars is not None else 'public sample',
         'value': stars, 'unit': 'stars', 'window': 'lifetime ratings, public sample', 'simulated': False, 'freshness': captured,
         'unavailable_reason': None if stars is not None else f'No ASIN with {MIN_RATINGS} or more ratings in the brain.',
         'fix': None if stars is not None else 'brain marketplaces'},
    ]


def build(brand=DEFAULT_BRAND, window='28d'):
    days = parse_days(window)
    try:
        s = Screen(brand)
    except Unavailable as exc:
        return {'screen': SLUG, 'brand': brand, 'unavailable': True, 'reason': exc.reason, 'fix': exc.fix}
    listings = s.listings()
    ladder = s.ladder()
    out = {'screen': SLUG, 'brand': brand, 'simulated': s.simulated, 'as_of': s.as_of.isoformat(),
           'window': {'label': f'{days}d', 'days': days, 'end': s.as_of.isoformat()}, 'unavailable': False}
    out['tiles'] = tiles(s, listings)
    out['chart'] = chart(s)
    out['listings'] = {'rows': listings, 'asins': len(listings),
                       'not_buyable': sum(1 for l in listings if l['buyable'] is False),
                       'amazon_reviews_in_table': s.amazon_review_count(),
                       'source': 'brain.marketplaces: public sample, not signed in. Not simulated.'}
    out['trust_ladder'] = None if ladder is None else {'id': ladder['id'], 'text': ladder.get('text'),
                                                       'what_fails': (ladder['value'].get('what_fails') or [])[:5]}
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
    """audit.py, loaded fresh so an edit shows on the next request."""
    spec = importlib.util.spec_from_file_location('screen_audit_20_marketplaces', HERE / 'audit.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
