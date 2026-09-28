"""API for screen 12-google-ads. Endpoints under /api/12-google-ads/.

  GET /api/12-google-ads/            the whole screen: tiles, split, search terms, impression share,
                                     asset groups, conversion check, 90-day chart, insights (audit)
  GET /api/12-google-ads/audit       the audit findings only (audit.py, contracts/audit.md shape)

Query: brand (default bombas), window (Nd, default 28d). Read-only: it reads app/data/brands/<brand>/
through data/tables.py and app/metrics.py and writes nothing.

Numbers
  spend, conversions, value, ROAS by campaign   metrics.py `spend` with channel=google, by=campaign
                                                (campaign rows only; platform reported)
  brand vs non-brand                            campaigns tagged by name: "brand" and not "non-brand" is
                                                brand; every other campaign (PMax, Demand Gen) is non-brand.
                                                PMax can serve on brand queries; its terms are hidden.
  search terms                                  search_term rows, trailing 30 days. Terms under the privacy
                                                threshold are dropped, so terms never sum to the campaign.
  impression share                              Search campaigns only, weighted by impressions. A day at the
                                                0.9001 ceiling is stored null with `clipped`; it is counted,
                                                never read as a number.
  conversion check                              last full month: Google conversions and value against store
                                                orders and net sales from paid search (channels_monthly).
Every value missing from the data reads null (unavailable), never 0.
"""
import importlib.util
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parents[1]
SLUG = '12-google-ads'
DEFAULT_BRAND = 'bombas'

# Rule constants. audit.py reads the same ones, so the table and the findings never disagree.
TERM_WINDOW_DAYS = 30                 # search_term_waste window in the room spec
WASTE_CPA_MULTIPLE = 2.0              # 0 conversions and spend over 2x the campaign CPA
POOR_CPA_MULTIPLE = 2.0               # converting, but CPA over 2x the campaign CPA
NEW_KEYWORD_MIN_CONV = 10             # conversions in 30 days before a term earns its own keyword
BAD_INTENT = ('job', 'jobs', 'careers', 'login', 'customer service', 'phone number', 'return policy', 'track order')
BUDGET_LOST_MIN = 0.05                # share of impressions lost to budget that counts as capped
RANK_LOST_MIN = 0.30                  # share lost to rank that counts as losing the auction
BRAND_IS_MIN = 0.85                   # brand term already won: the flag on incrementality
BRAND_ROAS_MULTIPLE = 2.0             # brand ROAS this many times non-brand makes the blend misleading
TRACKING_GAP_MIN = 0.10               # conversions vs orders gap that counts as a tracking problem
CHART_DAYS = 90


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


def brand_data(brand):
    """The brand's data layer, the same cached instance metrics.py reads (ValueError for an unknown brand)."""
    return metrics().resolve(None, {'brand': brand})


class Unavailable(Exception):
    def __init__(self, reason, fix=None):
        super().__init__(reason)
        self.reason, self.fix = reason, fix


# ---------------------------------------------------------------- windows

class Win:
    def __init__(self, end, days):
        self.end, self.days = end, days
        self.start = end - timedelta(days=days - 1)
        self.s, self.e = self.start.isoformat(), end.isoformat()

    def has(self, day):
        return self.s <= day <= self.e

    def shift(self, k):
        return Win(self.end - timedelta(days=self.days * k), self.days)

    def dict(self):
        return {'label': f'{self.days}d', 'start': self.s, 'end': self.e, 'days': self.days}


def parse_days(window):
    m = re.fullmatch(r'(\d{1,3})d', str(window or '28d'))
    if not m or not 7 <= int(m.group(1)) <= 120:
        raise ValueError('window must look like 28d, from 7d to 120d')
    return int(m.group(1))


def tag(name):
    """brand or nonbrand from the campaign name; None when there is no name to read."""
    if not name:
        return None
    n = name.lower()
    if re.search(r'non[\s-]?brand', n):
        return 'nonbrand'
    return 'brand' if re.search(r'\bbrand\b', n) else 'nonbrand'


def ratio(a, b, nd=4):
    return round(a / b, nd) if (a is not None and b) else None


def usd(x):
    return None if x is None else round(x, 2)


# ---------------------------------------------------------------- the data

class Google:
    """Google rows for one brand, split by row kind once. KeyError when the table is missing."""

    def __init__(self, brand):
        self.brand = brand
        self.data = brand_data(brand)
        info = self.data.brand
        if not info.get('as_of'):
            raise Unavailable('the brand has no last full day', fix='tables.json as_of')
        self.as_of = date.fromisoformat(info['as_of'])
        self.simulated = bool(info.get('simulated'))
        try:
            rows = self.data.table('google_rows')
        except KeyError:
            raise Unavailable('the google_rows table is not connected', fix='google_ads')
        except ValueError:
            raise Unavailable('the google_rows table is unreadable', fix='google_ads')
        self.campaign = [r for r in rows if r.get('row_kind') == 'campaign']
        self.terms = [r for r in rows if r.get('row_kind') == 'search_term']
        self.assets = [r for r in rows if r.get('row_kind') == 'asset_group']
        if not self.campaign:
            raise Unavailable('google_rows has no campaign rows', fix='google_ads')
        days = sorted(str(r['date']) for r in self.campaign)
        self.first, self.last = days[0], days[-1]
        self.freshness_days = 1  # captured the morning after the last full day (tables.py)

    def covers(self, win):
        return self.first <= win.s and win.e <= self.last

    def metric(self, name, win, **kw):
        return metrics().compute(name, None, brand=self.brand, window=f'{win.days}d', end=win.e, **kw)

    # ---- campaigns and the split

    def campaigns(self, win):
        """Per campaign from metrics.py (platform reported), with the brand tag and Google's own fields."""
        res = self.metric('spend', win, channel='google', by='campaign')
        if res.get('unavailable'):
            raise Unavailable(res.get('reason'), res.get('fix'))
        meta = {}
        for r in self.campaign:
            meta.setdefault(r['campaign_name'], {'campaign_id': r['campaign_id'], 'channel_type': r.get('channel_type'),
                                                'bidding': r.get('bidding'), 'status': r.get('campaign_status')})
        out = []
        for g in res['groups']:
            m = meta.get(g['campaign'], {})
            out.append({'campaign': g['campaign'], **m, 'tag': tag(g['campaign']), 'spend': g['spend'],
                        'conversions': g['purchases'], 'value': g['purchase_value'], 'roas': g['roas'], 'cpa': g['cpa']})
        return out

    def split(self, win):
        rows = self.campaigns(win)
        total = sum(r['spend'] for r in rows)
        out = {}
        for t in ('brand', 'nonbrand'):
            mine = [r for r in rows if r['tag'] == t]
            spend = sum(r['spend'] for r in mine)
            conv = sum(r['conversions'] for r in mine)
            value = sum(r['value'] for r in mine)
            out[t] = {'campaigns': [r['campaign'] for r in mine], 'spend': usd(spend), 'conversions': conv,
                      'value': usd(value), 'roas': ratio(value, spend), 'cpa': usd(spend / conv) if conv else None,
                      'share_of_spend': ratio(spend, total)}
        out['total'] = {'spend': usd(total), 'conversions': sum(r['conversions'] for r in rows),
                        'value': usd(sum(r['value'] for r in rows)),
                        'roas': ratio(sum(r['value'] for r in rows), total)}
        return out, rows

    # ---- impression share

    def impression_share(self, win):
        out = []
        by = {}
        for r in self.campaign:
            if win.has(str(r['date'])):
                by.setdefault(r['campaign_name'], []).append(r)
        for name, rows in sorted(by.items()):
            search = rows[0].get('channel_type') == 'SEARCH'
            row = {'campaign': name, 'tag': tag(name), 'channel_type': rows[0].get('channel_type'), 'days': len(rows),
                   'impression_share': None, 'lost_is_budget': None, 'lost_is_rank': None, 'clipped_days': 0,
                   'reason': None if search else 'not reported for this campaign type'}
            if search:
                for key in ('impression_share', 'lost_is_budget', 'lost_is_rank'):
                    num = den = 0.0
                    for r in rows:
                        if r.get(key) is not None and r.get('impressions'):
                            num += r[key] * r['impressions']
                            den += r['impressions']
                    row[key] = round(num / den, 4) if den else None
                row['clipped_days'] = sum(1 for r in rows if r.get('clipped'))
                if row['clipped_days']:
                    row['note'] = f"{row['clipped_days']} days over 90 percent are stored empty, so the share reads low"
            out.append(row)
        return out

    # ---- search terms

    def search_terms(self, end):
        win = Win(end, TERM_WINDOW_DAYS)
        camp = {}
        for r in self.campaign:
            if win.has(str(r['date'])):
                c = camp.setdefault(r['campaign_id'], [0.0, 0.0])
                c[0] += r['spend'] or 0
                c[1] += r['conversions'] or 0
        terms = {}
        for r in self.terms:
            if not win.has(str(r['date'])):
                continue
            key = (r['campaign_id'], r['search_term'])
            t = terms.setdefault(key, {'campaign_id': r['campaign_id'], 'campaign': r['campaign_name'], 'term': r['search_term'],
                                       'status': r.get('term_status'), 'spend': 0.0, 'clicks': 0, 'impressions': 0,
                                       'conversions': 0.0, 'days': 0})
            t['spend'] += r['spend'] or 0
            t['clicks'] += r['clicks'] or 0
            t['impressions'] += r['impressions'] or 0
            t['conversions'] += r['conversions'] or 0
            t['days'] += 1
            if r.get('term_status') == 'ADDED':
                t['status'] = 'ADDED'
        out = []
        for t in terms.values():
            cs, cc = camp.get(t['campaign_id'], (0.0, 0.0))
            ccpa = cs / cc if cc else None
            t['spend'] = usd(t['spend'])
            t['conversions'] = int(round(t['conversions']))
            t['cpa'] = usd(t['spend'] / t['conversions']) if t['conversions'] else None
            t['campaign_cpa'] = usd(ccpa)
            t['tag'] = tag(t['campaign'])
            t['action'], t['why'] = term_rule(t, ccpa)
            out.append(t)
        out.sort(key=lambda t: (-t['spend'], t['term']))
        summary = {'window': win.dict(), 'terms': len(out),
                   'negatives': sum(1 for t in out if t['action'] == 'negative'),
                   'new_keywords': sum(1 for t in out if t['action'] == 'new keyword'),
                   'negative_spend': usd(sum(t['spend'] for t in out if t['action'] == 'negative')),
                   'rules': {'negative': f'0 conversions and spend over {WASTE_CPA_MULTIPLE:g}x the campaign CPA; or CPA over '
                                         f'{POOR_CPA_MULTIPLE:g}x the campaign CPA; or a job, login or support query',
                             'new keyword': f'not yet a keyword, {NEW_KEYWORD_MIN_CONV} or more conversions in '
                                            f'{TERM_WINDOW_DAYS} days, CPA at or under the campaign CPA'},
                   'note': 'Terms under 10 impressions are hidden by Google, so terms never add up to the campaign.'}
        return out, summary


def term_rule(t, campaign_cpa):
    """The negatives-to-add and new-keywords rules, in that order. Returns (action, why)."""
    term = (t['term'] or '').lower()
    if any(re.search(r'\b' + re.escape(w) + r'\b', term) for w in BAD_INTENT):
        return 'negative', 'not a shopping search'
    if campaign_cpa is None:
        return 'keep', 'campaign has no conversions to compare against'
    if t['conversions'] == 0 and t['spend'] >= WASTE_CPA_MULTIPLE * campaign_cpa:
        return 'negative', f"${t['spend']:,.0f} spent, 0 conversions"
    if t['conversions'] and t['cpa'] >= POOR_CPA_MULTIPLE * campaign_cpa and t['spend'] >= WASTE_CPA_MULTIPLE * campaign_cpa:
        return 'negative', f"CPA {t['cpa'] / campaign_cpa:.1f}x the campaign"
    if t['status'] != 'ADDED' and t['conversions'] >= NEW_KEYWORD_MIN_CONV and t['cpa'] <= campaign_cpa:
        return 'new keyword', f"{t['conversions']} conversions at or under campaign CPA"
    return 'keep', 'already a keyword' if t['status'] == 'ADDED' else 'under the thresholds'


def _asset_groups(g, win):
    groups = {}
    for r in g.assets:
        if not win.has(str(r['date'])):
            continue
        a = groups.setdefault(r['asset_group_id'], {'asset_group': r['asset_group_id'], 'campaign': r['campaign_name'],
                                                    'strength_days': {}, 'latest': None, 'latest_day': ''})
        s = r.get('ad_strength')
        a['strength_days'][s] = a['strength_days'].get(s, 0) + 1
        if str(r['date']) >= a['latest_day']:
            a['latest'], a['latest_day'] = s, str(r['date'])
    out = []
    for a in groups.values():
        out.append({'asset_group': a['asset_group'], 'campaign': a['campaign'], 'ad_strength': a['latest'],
                    'days': sum(a['strength_days'].values()), 'strength_days': a['strength_days'],
                    'spend': None, 'conversions': None, 'value': None,
                    'reason': 'no spend by asset group in this data'})
    return out


def conversion_check(g):
    """Last full month: Google conversions and value against store orders and net sales from paid search."""
    month_end = g.as_of if (g.as_of + timedelta(days=1)).day == 1 else g.as_of.replace(day=1) - timedelta(days=1)
    month = month_end.strftime('%Y-%m')
    win = Win(month_end, month_end.day)
    if not g.covers(win):
        raise Unavailable(f'google_rows does not cover {month}', fix='google_ads')
    conv = sum(r['conversions'] or 0 for r in g.campaign if win.has(str(r['date'])))
    value = sum(r['conversion_value'] or 0 for r in g.campaign if win.has(str(r['date'])))
    try:
        chan = g.data.table('channels_monthly')
    except (KeyError, ValueError):
        raise Unavailable('the store orders by channel are not connected', fix='shopify')
    ps = next((r for r in chan if r.get('month') == month and r.get('channel') == 'paid_search'), None)
    if not ps or not ps.get('orders'):
        raise Unavailable(f'no paid search orders on file for {month}', fix='shopify')
    orders, net = ps['orders'], ps['net_sales']
    return {'month': month, 'window': win.dict(), 'google_conversions': int(round(conv)), 'google_value': usd(value),
            'store_orders': orders, 'store_net_sales': usd(net),
            'conversion_gap': ratio(conv - orders, orders), 'value_gap': ratio(value - net, net),
            'google_value_per_conversion': usd(value / conv) if conv else None,
            'store_aov': usd(net / orders),
            'value_per_conversion_gap': ratio(value / conv - net / orders, net / orders) if conv else None,
            'basis': 'Google conversions by click date, all campaigns. Store orders are paid search orders by UTM, net of '
                     'discounts, before tax and shipping. Google counts some organic and direct orders too.'}


def daily(g, end):
    win = Win(end, CHART_DAYS)
    days = [(win.start + timedelta(days=i)).isoformat() for i in range(CHART_DAYS)]
    idx = {d: i for i, d in enumerate(days)}
    series = {k: [None] * CHART_DAYS for k in ('brand_spend', 'nonbrand_spend', 'brand_conversions', 'nonbrand_conversions')}
    for r in g.campaign:
        i = idx.get(str(r['date']))
        t = tag(r['campaign_name'])
        if i is None or t is None:
            continue
        for k, col in (('spend', 'spend'), ('conversions', 'conversions')):
            key = f'{t}_{k}'
            if r.get(col) is not None:
                series[key][i] = round((series[key][i] or 0) + r[col], 2)
    return {'window': win.dict(), 'labels': days, **series}


# ---------------------------------------------------------------- the payload

def tiles(g, win):
    now, rows = g.split(win)
    prior_win = win.shift(1)
    prior = None
    if g.covers(prior_win):
        prior, _ = g.split(prior_win)

    def delta(a, b):
        return ratio(a - b, b) if (a is not None and b) else None

    p = prior or {'total': {}, 'brand': {}, 'nonbrand': {}}
    return [
        {'id': 'google_spend', 'name': 'Google spend', 'plain': 'all campaigns', 'value': now['total']['spend'], 'unit': '$',
         'delta': delta(now['total']['spend'], p['total'].get('spend'))},
        {'id': 'google_roas', 'name': 'Google ROAS', 'plain': 'as Google reports it', 'value': now['total']['roas'], 'unit': 'x',
         'delta': delta(now['total']['roas'], p['total'].get('roas'))},
        {'id': 'nonbrand_roas', 'name': 'Non-brand ROAS', 'plain': 'without your own name', 'value': now['nonbrand']['roas'],
         'unit': 'x', 'delta': delta(now['nonbrand']['roas'], p['nonbrand'].get('roas'))},
        {'id': 'brand_share', 'name': 'Brand share of spend', 'plain': 'spend on your own name', 'value': now['brand']['share_of_spend'],
         'unit': '%', 'delta': delta(now['brand']['share_of_spend'], p['brand'].get('share_of_spend')), 'higher_is_better': False},
    ], now, rows


def build(brand=DEFAULT_BRAND, window='28d'):
    days = parse_days(window)
    try:
        g = Google(brand)
    except Unavailable as exc:
        return {'screen': SLUG, 'brand': brand, 'unavailable': True, 'reason': exc.reason, 'fix': exc.fix}
    win = Win(g.as_of, days)
    out = {'screen': SLUG, 'brand': brand, 'simulated': g.simulated, 'as_of': g.as_of.isoformat(), 'window': win.dict(),
           'unavailable': False}
    if not g.covers(win):
        return dict(out, unavailable=True, reason=f'google_rows covers {g.first} to {g.last}, not all of {win.s} to {win.e}',
                    fix='google_ads')
    t, split, rows = tiles(g, win)
    out['tiles'] = t
    split['brand']['incrementality'] = brand_flag(g, win, split)
    out['split'] = split
    out['campaigns'] = rows
    out['impression_share'] = g.impression_share(win)
    terms, summary = g.search_terms(g.as_of)
    out['search_terms'] = {'summary': summary, 'rows': terms}
    out['asset_groups'] = _asset_groups(g, win)
    try:
        out['conversion_check'] = dict(conversion_check(g), unavailable=False)
    except Unavailable as exc:
        out['conversion_check'] = {'unavailable': True, 'reason': exc.reason, 'fix': exc.fix}
    out['chart'] = daily(g, g.as_of)
    return out


def brand_flag(g, win, split):
    """The incrementality flag on brand: the term is already won and no holdout says the spend adds orders."""
    is_rows = [r for r in g.impression_share(win) if r['tag'] == 'brand' and r['impression_share'] is not None]
    brand_is = max((r['impression_share'] for r in is_rows), default=None)
    clipped = sum(r['clipped_days'] for r in g.impression_share(win) if r['tag'] == 'brand')
    holdout = holdout_on_file(g.brand)
    flagged = bool(split['brand']['spend']) and not holdout and (
        (brand_is is not None and brand_is >= BRAND_IS_MIN) or clipped > 0)
    return {'flagged': flagged, 'impression_share': brand_is, 'clipped_days': clipped, 'holdout_on_file': holdout,
            'rule': f'brand impression share at or over {BRAND_IS_MIN:.0%} (or days over 90 percent) and no brand holdout on file',
            'text': ('Untested. Brand ads may be buying orders that would come through organic search anyway.'
                     if flagged else 'A brand holdout is on file.' if holdout else 'Brand is not yet dominant on its own term.')}


def holdout_on_file(brand):
    """True when the brain's learnings hold a brand search holdout record."""
    path = APP / 'brain' / brand / 'learnings.json'
    if not path.is_file():
        return False
    try:
        recs = json.loads(path.read_text(encoding='utf-8'))
    except ValueError:
        return False
    recs = recs.get('records', []) if isinstance(recs, dict) else recs
    return any('holdout' in str(r.get('id', '')) and 'brand' in str(r.get('id', '')) for r in recs if isinstance(r, dict))


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
    spec = importlib.util.spec_from_file_location('screen_audit_12_google_ads', HERE / 'audit.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
