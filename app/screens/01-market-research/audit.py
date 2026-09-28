"""Products and research audit (screen 01, round 0). Findings in the shape of app/contracts/audit.md.

Sales numbers come from app/metrics.py (`units`, `product_net_sales` from products_monthly). Review
numbers come from the brand brain: the `products.reviews_*` records (public own-site review totals) and
the `objection_ladders` records that were built from them. No connector, no model call. Same tables,
same brain and same window give the same findings, byte for byte.

A line is a SKU title without its pack size (metrics.product_line). The trend window is the last 3
whole months before the window end, against the same 3 months a year earlier, so season does not
read as trend.

Rules
  PROD-R01  Declining line: a line whose units fell on last year over the last 3 whole months, or
            whose unit growth trails the whole store's by 1 point or more, so it is losing share of
            what the store sells. Money: (store growth - line growth) x the line's units a year ago
            x its net sales per unit now: the net sales it would have made had it kept its share.
            Agreement: each of the 3 months where the line also trailed the store. Capability
            PROD-C05 (read trend and saturation together, agent does). Owner: 01-market-research.
  PROD-R02  Review issue: a line whose share of 1 and 2 star reviews is 10 percent or more and at
            least 1.5 times the median across the brand's reviewed lines. Money: the line's net
            sales in the last whole month x (its low-star share - the median share): sales that
            went out into the extra bad experiences. Evidence carries the top issues and the
            objection ladder rungs built from the same reviews. Capability PROD-C06 (sharpen the
            line and its angle, agent does). Owner: 01-market-research; 04-offers reads the ladder.

  PROD-R04  Category behind its market: a category whose 12-month unit growth is below the public growth a
            year of its market in the web pass fixture (fixtures/market_trends.json, url and date on every
            number). Money: (market growth - our growth) x our net sales 12 months. Confidence 0.3 (one
            window, peer baseline). Capability PROD-C05. Owner: 01-market-research.
  PROD-R05  Growing sub-category the brand sells and does not advertise: a market in the web pass growing 4
            percent a year or more (or the gift window, 1 Nov, inside 90 days) whose words appear in the
            brand's product, claim or site records and in none of its active-ad signals. Money: null.
            Capability PROD-C05 (agent does). Owner: 01-market-research.
  PROD-R03  Hero line with no next SKU: a line with 25 percent or more of its category's net sales in
            the last 3 whole months while the candidate pipeline holds no open next-SKU candidate for
            that category. Money: null (an unlaunched SKU has no baseline). Capability PROD-C06
            (extend the line and sharpen the angle, agent does). Owner: 01-market-research.

Money uses net sales, not margin. Review counts are public and real; sales are simulated.
"""
import importlib.util
import json
import statistics
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parents[1]
SCREEN = '01-market-research'

TREND_MONTHS = 3
SHARE_GAP_POINTS = 1.0
LOW_STAR_FLOOR = 0.10
LOW_STAR_TIMES_MEDIAN = 1.5
HERO_SHARE = 0.25  # a line with this share of its category's net sales is a hero

RULES = [
    {'rule_id': 'PROD-R01', 'name': 'Line units down on last year, or growing 1 point or more slower than the store',
     'entity_type': 'sku', 'inputs': ['products_monthly', 'products'], 'capability': 'PROD-C05', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R02', 'name': 'Line with 10 percent or more 1 and 2 star reviews, 1.5 times the brand median',
     'entity_type': 'sku', 'inputs': ['brain.products.reviews_*', 'brain.objection_ladders', 'products_monthly'],
     'capability': 'PROD-C06', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R03', 'name': 'Hero line with 25 percent or more of its category and no next SKU in the pipeline',
     'entity_type': 'sku', 'inputs': ['products_monthly', 'products', 'fixtures.pipeline'], 'capability': 'PROD-C06',
     'owner_screen': SCREEN},
    {'rule_id': 'PROD-R04', 'name': 'Category units growing slower than its public market growth a year (web pass)',
     'entity_type': 'sku', 'inputs': ['products_monthly', 'fixtures.market_trends'], 'capability': 'PROD-C05', 'owner_screen': SCREEN},
    {'rule_id': 'PROD-R05', 'name': 'Sub-category growing 4 percent a year or more (or the gift window within 90 days) that the brand sells and no active ad names',
     'entity_type': 'metric', 'inputs': ['fixtures.market_trends', 'brain.products', 'brain.learnings'], 'capability': 'PROD-C05', 'owner_screen': SCREEN},
]
CAPABILITY = {'PROD-R01': {'id': 'PROD-C05', 'autonomy': 'agent_does'},
              'PROD-R02': {'id': 'PROD-C06', 'autonomy': 'agent_does'},
              'PROD-R03': {'id': 'PROD-C06', 'autonomy': 'agent_does'},
              'PROD-R04': {'id': 'PROD-C05', 'autonomy': 'agent_does'},
              'PROD-R05': {'id': 'PROD-C05', 'autonomy': 'agent_does'}}
SEVERITY_ORDER = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}

# Review records name their line in a short key; the store names it by SKU title.
REVIEW_LINE = {'ankle': 'Ankle Sock', 'calf': 'Calf Sock', 'no_show': 'No Show Sock',
               'merino': 'Merino Wool Calf Sock', 'slippers': 'Gripper Slipper', 'underwear': 'Boxer Brief',
               't_shirts': 'Pima Cotton Tee', 'compression': 'Compression Sock'}

_MODS = {}


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def metrics():
    if 'metrics' not in _MODS:
        _MODS['metrics'] = _load('ecomos_metrics_research', APP / 'metrics.py')
    return _MODS['metrics']


def brand_data(brand):
    if 'tables' not in _MODS:
        _MODS['tables'] = _load('ecomos_tables_research', APP / 'data' / 'tables.py')
    return _MODS['tables'].brand_data(brand)


def brain(brand, today=None):
    """The brand's brain store, or None when the brand has no brain folder."""
    import sys
    if str(APP / 'brain') not in sys.path:
        sys.path.insert(0, str(APP / 'brain'))
    import store
    if not (APP / 'brain' / str(brand)).is_dir():
        return None
    return store.Brain(brand, today=today)


def slug(line):
    return str(line).lower().replace(' ', '-')


def month_add(month, k):
    y, m = int(month[:4]), int(month[5:7]) + k
    y += (m - 1) // 12
    return f'{y}-{(m - 1) % 12 + 1:02d}'


def month_end(month):
    return metrics().month_end(month)


def last_full_day(data, brand):
    source = brand_data(brand) if brand else data
    return date.fromisoformat(source.brand['as_of'])


def last_whole_month(ends_on):
    """The last month that ends on or before ends_on."""
    m = ends_on.strftime('%Y-%m')
    return m if month_end(m) <= ends_on else month_add(m, -1)


class Reader:
    """One brand, one window end. m(name, first_month, last_month, **kw) is metrics.compute over whole months."""

    def __init__(self, data, brand, ends_on):
        self.data, self.brand, self.ends_on = data, brand, ends_on
        self.last_month = last_whole_month(ends_on)

    def m(self, name, first, last, **kw):
        start = date.fromisoformat(first + '-01')
        end = month_end(last)
        q = {'window': f'{(end - start).days + 1}d', 'end': end.isoformat(), **kw}
        if self.brand:
            q['brand'] = self.brand
        return metrics().compute(name, self.data, **q)

    def lines(self, first, last):
        r = self.m('units', first, last, by='line')
        return r, ({g['line']: g for g in r['groups']} if not r.get('unavailable') else {})


# ---------------------------------------------------------------- trend

def trend(rd):
    """Per line: units in the last 3 whole months against the same months a year back, and against the store."""
    last = rd.last_month
    first = month_add(last, 1 - TREND_MONTHS)
    now_r, now = rd.lines(first, last)
    ago_r, ago = rd.lines(month_add(first, -12), month_add(last, -12))
    if now_r.get('unavailable') or ago_r.get('unavailable'):
        bad = now_r if now_r.get('unavailable') else ago_r
        return {'unavailable': True, 'reason': bad.get('reason'), 'fix': bad.get('fix')}
    store_growth = now_r['value'] / ago_r['value'] - 1 if ago_r['value'] else None
    monthly = []  # (month, {line: growth}, store growth) for each of the 3 months
    for k in range(TREND_MONTHS):
        mo = month_add(first, k)
        a_r, a = rd.lines(mo, mo)
        b_r, b = rd.lines(month_add(mo, -12), month_add(mo, -12))
        if a_r.get('unavailable') or b_r.get('unavailable') or not b_r['value']:
            continue
        monthly.append((mo, {l: a[l]['units'] / b[l]['units'] - 1 for l in a if l in b and b[l]['units']},
                        a_r['value'] / b_r['value'] - 1))
    rows = []
    for line, g in now.items():
        p = ago.get(line)
        growth = g['units'] / p['units'] - 1 if p and p['units'] else None
        gap = round((growth - store_growth) * 100, 2) if growth is not None and store_growth is not None else None
        trailed = sum(1 for _, lg, sg in monthly if line in lg and lg[line] < sg)
        rows.append({'line': line, 'skus': g['skus'], 'units': g['units'], 'units_year_ago': p['units'] if p else None,
                     'net_sales': g['net_sales'], 'net_per_unit': g['net_per_unit'],
                     'growth': round(growth, 4) if growth is not None else None, 'gap_points': gap,
                     'months_trailing_store': trailed, 'months_checked': len(monthly)})
    rows.sort(key=lambda r: -r['units'])
    return {'unavailable': False, 'first': first, 'last': last, 'year_ago': [month_add(first, -12), month_add(last, -12)],
            'store_units': now_r['value'], 'store_units_year_ago': ago_r['value'],
            'store_growth': round(store_growth, 4) if store_growth is not None else None, 'lines': rows,
            'freshness': now_r.get('freshness')}


def declining(row):
    """'down' when units fell on last year, 'losing_share' when growth trails the store by the gap, else None."""
    if row['growth'] is None or row['gap_points'] is None:
        return None
    if row['growth'] < 0:
        return 'down'
    if row['gap_points'] <= -SHARE_GAP_POINTS:
        return 'losing_share'
    return None


# ---------------------------------------------------------------- reviews

def review_lines(br):
    """One row per reviewed line from the brain's products.reviews_* records."""
    if br is None:
        return []
    out = []
    for rec in br.records('products'):
        v = rec.get('value')
        if not rec['id'].startswith(f'{br.brand}.products.reviews_') or not isinstance(v, dict):
            continue
        dist = v.get('yotpo_star_distribution') or {}
        total = v.get('yotpo_review_total')
        low = (dist.get('1') or 0) + (dist.get('2') or 0) if dist else None
        out.append({'key': v.get('product_line'), 'line': REVIEW_LINE.get(v.get('product_line')),
                    'record': rec['id'], 'product': v.get('yotpo_product'), 'pdp': v.get('pdp'),
                    'reviews': total, 'rating': v.get('yotpo_average'),
                    'low_star': low, 'low_star_share': round(low / total, 4) if total and low is not None else None,
                    'praise': v.get('praise') or [], 'issues': v.get('issues') or [],
                    'captured_at': (rec.get('source') or {}).get('captured_at')})
    return out


def ladders(br):
    """Objection ladders with the review records each rung was built from."""
    if br is None:
        return []
    out = []
    for rec in br.records('objection_ladders'):
        v = rec.get('value') or {}
        rungs = []
        for r in v.get('rungs') or []:
            c = r.get('counts') or {}
            rungs.append({'level': r.get('level'), 'doubt': r.get('doubt'), 'one_star': c.get('one_star'),
                          'five_star': c.get('five_star'), 'proof': bool(r.get('proof')),
                          'from_reviews': [d for d in r.get('derived_from') or [] if '.products.reviews_' in d]})
        counts = v.get('counts') or {}
        out.append({'id': rec['id'], 'theme': v.get('theme'), 'what_works': v.get('what_works') or [],
                    'what_fails': v.get('what_fails') or [], 'one_star': counts.get('one_star'),
                    'five_star': counts.get('five_star'), 'rungs': rungs,
                    'reviews_records': sorted({d for r in rungs for d in r['from_reviews']})})
    return out


def median_low_star(reviews):
    shares = [r['low_star_share'] for r in reviews if r['low_star_share'] is not None]
    return round(statistics.median(shares), 4) if len(shares) >= 3 else None


# ---------------------------------------------------------------- findings

def _ev(metric, value, unit, ends_on, window, baseline=None, baseline_kind=None, source='products_monthly',
        simulated=True, freshness_days=1, **extra):
    out = {'metric': metric, 'value': value, 'unit': unit, 'window': window, 'ends_on': ends_on,
           'freshness_days': freshness_days, 'baseline': baseline, 'baseline_kind': baseline_kind, 'source': source,
           'simulated': simulated}
    out.update(extra)
    return out


def _confidence(windows_agree):
    return 0.9 if windows_agree >= 4 else 0.7 if windows_agree >= 2 else 0.5


def _severity(stake, net_28d, windows_agree):
    if stake is not None and net_28d and stake > 0.05 * net_28d:
        return 'critical'
    if windows_agree >= 2 or (stake is not None and net_28d and stake > 0.01 * net_28d):
        return 'high'
    return 'medium'


def _finding(rule_id, line, ends_on, severity, evidence, sentence, stake, confidence, brain_refs=(), money_reason=None):
    out = {'id': f'{SCREEN}.{rule_id}.{slug(line)}', 'screen': SCREEN, 'rule_id': rule_id, 'severity': severity,
           'entity': {'type': 'sku', 'id': slug(line), 'label': f'{line} (product line)'}, 'evidence': evidence,
           'sentence': sentence, 'capability': dict(CAPABILITY[rule_id]), 'money_at_stake': stake,
           'confidence': confidence, 'brain_refs': list(brain_refs), 'first_seen': ends_on.isoformat(),
           'last_seen': ends_on.isoformat(), 'status': 'open', 'unavailable': None}
    if stake is None:
        out['money_reason'] = money_reason or 'no baseline'
    return out


def _unavailable(rule_id, ends_on, reason, inputs, connector, fix):
    return {'id': f'{SCREEN}.{rule_id}.brand', 'screen': SCREEN, 'rule_id': rule_id, 'severity': 'medium',
            'entity': {'type': 'brand', 'id': 'brand', 'label': 'Product lines'}, 'evidence': [],
            'sentence': reason, 'capability': dict(CAPABILITY[rule_id]), 'money_at_stake': None,
            'money_reason': 'inputs unavailable', 'confidence': 0.1, 'brain_refs': [],
            'first_seen': ends_on.isoformat(), 'last_seen': ends_on.isoformat(), 'status': 'unavailable',
            'unavailable': {'inputs': inputs, 'connector': connector, 'fix': fix}}


def _span(first, last):
    a = date.fromisoformat(first + '-01').strftime('%b')
    b = date.fromisoformat(last + '-01').strftime('%b %Y')
    return f'{a} to {b}'


def declining_findings(tr, ends_on, net_28d):
    out = []
    end = month_end(tr['last']).isoformat()
    window = f'{TREND_MONTHS} months'
    for r in tr['lines']:
        kind = declining(r)
        if not kind:
            continue
        sg = tr['store_growth']
        lost_units = round((sg - r['growth']) * r['units_year_ago'])
        usd = max(round(lost_units * r['net_per_unit']), 0) if r['net_per_unit'] else None
        stake = None if usd is None else {
            'usd': usd, 'formula': '(store_growth - line_growth) * units_year_ago * net_per_unit',
            'inputs': {'store_growth': sg, 'line_growth': r['growth'], 'units_year_ago': r['units_year_ago'],
                       'net_per_unit': r['net_per_unit']}, 'window': window}
        agree = r['months_trailing_store']
        evidence = [
            _ev('units', r['units'], 'count', end, window, r['units_year_ago'], 'own_median',
                note=f'baseline is the same {TREND_MONTHS} months a year earlier'),
            _ev('unit_growth', r['growth'], 'ratio', end, window, sg, 'threshold',
                note=f'baseline is the whole store; the rule fires at {SHARE_GAP_POINTS:g} point behind'),
            _ev('months_trailing_store', agree, 'count', end, window, r['months_checked'], 'threshold'),
            _ev('net_per_unit', r['net_per_unit'], 'usd', end, window)]
        span = _span(tr['first'], tr['last'])
        if kind == 'down':
            sentence = (f'{r["line"]} sold {r["units"]:,} units from {span}, down {abs(round(r["growth"] * 100, 1))} '
                        f'percent on last year. The store grew {round(sg * 100, 1)} percent.')
        else:
            sentence = (f'{r["line"]} units grew {round(r["growth"] * 100, 1)} percent on last year from {span}. '
                        f'The store grew {round(sg * 100, 1)} percent, so the line is losing share.')
        out.append(_finding('PROD-R01', r['line'], ends_on, _severity(usd, net_28d, agree), evidence, sentence, stake,
                            _confidence(agree)))
    return out


def review_findings(reviews, lads, rd, tr, ends_on, net_28d):
    out = []
    base = median_low_star(reviews)
    if base is None:
        return out
    last = tr.get('last') if not tr.get('unavailable') else None
    month = rd.lines(last, last)[1] if last else {}
    for rv in reviews:
        share = rv['low_star_share']
        if share is None or share < LOW_STAR_FLOOR or share < LOW_STAR_TIMES_MEDIAN * base:
            continue
        line = rv['line'] or rv['key']
        month_net = (month.get(rv['line']) or {}).get('net_sales')
        stake, reason = None, None
        if month_net is None:
            reason = 'no sales for this line in the last whole month'
        else:
            stake = {'usd': round(month_net * (share - base)), 'formula': 'net_sales_last_month * (low_star_share - median_low_star_share)',
                     'inputs': {'net_sales_last_month': month_net, 'low_star_share': share, 'median_low_star_share': base},
                     'window': f'1 month ({last})'}
        fresh = (ends_on - date.fromisoformat(rv['captured_at'][:10])).days if rv['captured_at'] else None
        rung_hits = [(l, g) for l in lads for g in l['rungs'] if rv['record'] in g['from_reviews']]
        evidence = [
            _ev('low_star_share', share, 'ratio', ends_on.isoformat(), 'all reviews to capture', base, 'own_median',
                source=rv['record'], simulated=False, freshness_days=max(fresh or 0, 0),
                note='baseline is the median across the brand\'s reviewed lines'),
            _ev('reviews', rv['reviews'], 'count', ends_on.isoformat(), 'all reviews to capture', source=rv['record'],
                simulated=False, freshness_days=max(fresh or 0, 0)),
            _ev('rating', rv['rating'], 'stars', ends_on.isoformat(), 'all reviews to capture', source=rv['record'],
                simulated=False, freshness_days=max(fresh or 0, 0), top_issues=rv['issues'][:3])]
        for l, g in rung_hits:
            evidence.append(_ev('ladder_rung_one_star', g['one_star'], 'count', ends_on.isoformat(), 'at ladder build',
                                source=l['id'], simulated=False, rung=f'{l["theme"]}.level_{g["level"]}', doubt=g['doubt'],
                                proof_on_file=g['proof']))
        if month_net is not None:
            evidence.append(_ev('net_sales', month_net, 'usd', month_end(last).isoformat(), '1 month'))
        top = rv['issues'][0] if rv['issues'] else 'no issue named'
        sentence = (f'{round(share * 100, 1)} percent of {rv["reviews"]:,} {line} reviews are 1 or 2 stars. '
                    f'The brand median is {round(base * 100, 1)} percent. The top issue is: {top}.')
        usd = stake['usd'] if stake else None
        refs = [rv['record']] + sorted({l['id'] for l, _ in rung_hits})
        out.append(_finding('PROD-R02', line, ends_on, _severity(usd, net_28d, 1), evidence, sentence, stake,
                            _confidence(1), refs, reason))
    return out



# ---------------------------------------------------------------- hero line, pipeline

def pipeline(brand):
    """Open next-SKU candidates from this screen's fixture (fixtures/pipeline.json, list of rows). Empty when absent."""
    path = HERE / 'fixtures' / 'pipeline.json'
    if not path.is_file():
        return []
    import json
    doc = json.loads(path.read_text(encoding='utf-8'))
    rows = doc.get('rows') if isinstance(doc, dict) else doc
    return [r for r in rows or [] if not brand or r.get('brand') in (None, brand)]


def line_category(line, prods):
    """The category of a line from the products table, else the line itself when lines are categories."""
    for p in prods or []:
        if metrics().product_line(p.get('title')) == line:
            return p.get('category') or line
    return line


def hero_findings(tr, ends_on, prods, pipe):
    """PROD-R03: the biggest line of each category with 25 percent or more of it and no open candidate."""
    out = []
    cats = {}
    for r in tr['lines']:
        cats.setdefault(line_category(r['line'], prods), []).append(r)
    open_by_cat = {}
    for p in pipe:
        if p.get('stage') not in ('go', 'kill', 'killed'):
            open_by_cat.setdefault(p.get('category'), []).append(p)
    end = month_end(tr['last']).isoformat()
    window = f'{TREND_MONTHS} months'
    for cat, rows in cats.items():
        total = sum(r['net_sales'] for r in rows)
        if not total or len(rows) < 2:
            continue
        top = max(rows, key=lambda r: r['net_sales'])
        share = top['net_sales'] / total
        if share < HERO_SHARE or open_by_cat.get(cat):
            continue
        evidence = [
            _ev('category_share_net_sales', round(share, 4), 'ratio', end, window, HERO_SHARE, 'threshold',
                note=f'share of {cat} net sales across {len(rows)} lines'),
            _ev('net_sales', top['net_sales'], 'usd', end, window),
            _ev('open_candidates', 0, 'count', ends_on.isoformat(), 'pipeline now', 1, 'threshold', source='fixtures.pipeline',
                simulated=False, freshness_days=0)]
        sentence = (f'{top["line"]} brings in {round(share * 100)} percent of {cat} net sales over {_span(tr["first"], tr["last"])}. '
                    f'No next SKU for {cat} is open in the pipeline.')
        f = _finding('PROD-R03', top['line'], ends_on, 'medium', evidence, sentence, None, 0.7,
                     money_reason='an unlaunched SKU has no baseline to price the gap')
        f['entity']['category'] = cat
        out.append(f)
    return out


def net_28d(rd):
    r = metrics().compute('aov', rd.data, window='28d', end=rd.ends_on.isoformat(),
                          **({'brand': rd.brand} if rd.brand else {}))
    return (r.get('inputs') or {}).get('net_revenue') if not r.get('unavailable') else None


def run(brand, window=None, data=None):
    """Findings for one brand and window ({ends_on, days, trailing}), sorted by severity then stake."""
    data = data if data is not None else (brand_data(brand) if brand else None)
    ends_on = date.fromisoformat(window['ends_on']) if window and window.get('ends_on') else last_full_day(data, brand)
    rd = Reader(data, brand, ends_on)
    tr = trend(rd)
    net = net_28d(rd)
    br = brain(brand, today=ends_on) if brand else None
    out = []
    if tr.get('unavailable'):
        out.append(_unavailable('PROD-R01', ends_on, 'Product sales by month are not connected, so line trends cannot be read.',
                                ['products_monthly'], tr.get('fix') or 'shopify', 'Connect the store (read only).'))
    else:
        out += declining_findings(tr, ends_on, net)
        try:
            prods = (data if data is not None else brand_data(brand)).table('products')
        except (KeyError, ValueError):
            prods = None
        out += hero_findings(tr, ends_on, prods, pipeline(brand))
    reviews = review_lines(br)
    if not reviews:
        out.append(_unavailable('PROD-R02', ends_on, 'No review totals are on file for any line, so review issues cannot be read.',
                                ['brain.products.reviews_*'], 'reviews', 'Add the review capture for each line to the brand brain.'))
    else:
        out += review_findings(reviews, ladders(br), rd, tr, ends_on, net)
    out += trend_findings(br, category_mix(data, brand, rd), ends_on)
    out.sort(key=lambda f: (SEVERITY_ORDER[f['severity']], -((f['money_at_stake'] or {}).get('usd') or 0), f['id']))
    return out


# ---------------------------------------------------------------- category mix, 12 whole months

MIX_MONTHS = 12


def category_mix(data, brand, rd):
    """Our units and net sales by category over the last 12 whole months against the 12 before, from products_monthly."""
    try:
        rows = (brand_data(brand) if brand else data).table('products_monthly')
    except (KeyError, ValueError) as exc:
        return {'unavailable': True, 'reason': f'products_monthly is not connected ({exc})', 'fix': 'shopify', 'rows': []}
    last = rd.last_month
    first = month_add(last, 1 - MIX_MONTHS)
    p_first, p_last = month_add(first, -12), month_add(last, -12)
    now, ago, series = {}, {}, {}
    months = [month_add(first, k) for k in range(MIX_MONTHS)]
    for r in rows:
        cat = r.get('category') or 'other'
        m = r.get('month')
        if first <= m <= last:
            g = now.setdefault(cat, {'units': 0, 'net_sales': 0.0})
            g['units'] += r.get('units') or 0
            g['net_sales'] += r.get('net_sales') or 0.0
            series.setdefault(cat, {mm: None for mm in months})[m] = (series.get(cat, {}).get(m) or 0) + (r.get('units') or 0)
        elif p_first <= m <= p_last:
            g = ago.setdefault(cat, {'units': 0, 'net_sales': 0.0})
            g['units'] += r.get('units') or 0
            g['net_sales'] += r.get('net_sales') or 0.0
    total_units = sum(g['units'] for g in now.values())
    total_net = sum(g['net_sales'] for g in now.values())
    out = []
    for cat, g in now.items():
        a = ago.get(cat)
        out.append({'category': cat, 'units': g['units'], 'net_sales': round(g['net_sales'], 2),
                    'unit_share': round(g['units'] / total_units, 4) if total_units else None,
                    'net_share': round(g['net_sales'] / total_net, 4) if total_net else None,
                    'growth': round(g['units'] / a['units'] - 1, 4) if a and a['units'] else None,
                    'net_growth': round(g['net_sales'] / a['net_sales'] - 1, 4) if a and a['net_sales'] else None,
                    'series': [series[cat][m] for m in months]})
    out.sort(key=lambda r: -r['net_sales'])
    return {'unavailable': False, 'first': first, 'last': last, 'months': months, 'rows': out,
            'store_growth': round(sum(g['units'] for g in now.values()) / sum(g['units'] for g in ago.values()) - 1, 4) if ago and sum(g['units'] for g in ago.values()) else None}



# ---------------------------------------------------------------- the web pass (fixtures/market_trends.json)

def market_trends():
    """The public web pass this screen keeps as a fixture: markets, preferences, launches, each with url and date.
    None when the file is absent. Never a number without a source."""
    path = HERE / 'fixtures' / 'market_trends.json'
    if not path.is_file():
        return None
    import json
    return json.loads(path.read_text(encoding='utf-8'))


# words that tie a public market or sub-category to what the brand sells; the brand side is read from the brain
MARKET_CATEGORY = {'socks_us': 'socks', 'socks_global': 'socks', 'slippers_us': 'slippers', 'mens_underwear_us': 'underwear',
                   'womens_underwear_us': 'underwear', 'basics_tshirts': 'tshirts', 'footwear_casual': 'footwear',
                   'compression_socks': 'socks', 'athletic_socks': 'socks', 'merino_wool_socks': 'socks',
                   'gifting_socks': 'socks', 'sustainable_apparel': None}
MARKET_WORDS = {'compression_socks': ['compression'], 'athletic_socks': ['athletic', 'performance', 'running', 'sport'],
                'merino_wool_socks': ['merino'], 'gifting_socks': ['gift'], 'sustainable_apparel': ['sustainab', 'recycled', 'organic'],
                'slippers_us': ['slipper'], 'mens_underwear_us': ['underwear', 'boxer', 'brief'], 'womens_underwear_us': ['underwear', 'bralette', 'hipster'],
                'basics_tshirts': ['t-shirt', 'tshirt', ' tee ', ' tees'], 'footwear_casual': ['clog', 'moccasin', 'sandal', 'footwear'], 'socks_us': ['sock'], 'socks_global': ['sock']}


def brand_words(br):
    """Lower-case text of the brain's product, claim and site records, for keyword coverage checks."""
    if br is None:
        return ''
    parts = []
    for sec in ('products', 'claims', 'site_map', 'offers'):
        for r in br.records(sec):
            parts.append(str(r.get('text') or ''))
            v = r.get('value')
            parts.append(v if isinstance(v, str) else __import__('json').dumps(v))
    return ' '.join(parts).lower()


def market_covered(key, words):
    """True when the brand's own records name the sub-category the market row describes."""
    return any(w in words for w in MARKET_WORDS.get(key, [key.split('_')[0]]))


def ad_words(br):
    """Lower-case text of the brand's own active-ad signals in the brain (learnings with role self, offers seen in ads)."""
    if br is None:
        return ''
    parts = []
    for r in br.records('learnings'):
        v = r.get('value')
        if isinstance(v, dict) and v.get('role') == 'competitor':
            continue
        if (r.get('source') or {}).get('type') != 'ad_library':
            continue
        parts.append(str(r.get('text') or ''))
        parts.append(json.dumps(v))
        for e in r.get('evidence') or []:
            parts.append(str(e.get('quote') or ''))
    for r in br.records('offers'):
        if (r.get('source') or {}).get('type') == 'ad_library':
            parts.append(str(r.get('text') or ''))
    return ' '.join(parts).lower()


TREND_MIN_CAGR = 4.0
GIFT_WINDOW_DAYS = 90


def trend_findings(br, mix, ends_on):
    """PROD-R04 and PROD-R05 from the web pass fixture against our category mix and our active ads."""
    fx = market_trends()
    if not fx:
        return [_unavailable('PROD-R05', ends_on, 'No web pass is on file, so the category trend cannot be read.',
                             ['fixtures/market_trends.json'], 'web_pass', 'Run the research web pass for this brand.')]
    words = brand_words(br)
    ads = ad_words(br)
    ours = {r['category']: r for r in (mix.get('rows') or [])} if not mix.get('unavailable') else {}
    out = []
    for m in fx.get('markets') or []:
        key = m.get('key')
        cagr = m.get('cagr_pct')
        src = (m.get('sources') or [{}])[0]
        cite = f"{src.get('publisher') or 'public source'}, {src.get('date') or 'undated'}"
        cat = MARKET_CATEGORY.get(key)
        our = ours.get(cat) if cat else None
        # R04: our category grows slower than its public market
        if our and our.get('growth') is not None and isinstance(cagr, (int, float)) and our['growth'] * 100 < cagr:
            lost = round((cagr / 100 - our['growth']) * our['net_sales'])
            stake = {'usd': max(lost, 0), 'formula': '(market_cagr - our_growth) * our_net_sales_12m',
                     'inputs': {'market_cagr': cagr / 100, 'our_growth': our['growth'], 'our_net_sales_12m': our['net_sales']}, 'window': '12 months'}
            ev = [_ev('unit_growth_12m', our['growth'], 'ratio', month_end(mix['last']).isoformat(), '12 months', cagr / 100, 'peer_band',
                      note=f'baseline is the public market growth a year ({cite})'),
                  _ev('net_sales_12m', our['net_sales'], 'usd', month_end(mix['last']).isoformat(), '12 months')]
            sentence = (f'{cat} units grew {round(our["growth"] * 100, 1)} percent in 12 months. The {m.get("label")} market grows '
                        f'{cagr} percent a year ({cite}), so the line is losing share of its market.')
            out.append(_finding('PROD-R04', cat, ends_on, 'medium', ev, sentence, stake, 0.3, [f'fixtures.market_trends.{key}']))
        # R05: a growing sub-category the brand sells and does not advertise
        growing = isinstance(cagr, (int, float)) and cagr >= TREND_MIN_CAGR and m.get('direction') == 'up'
        gifting = key == 'gifting_socks' and 0 <= (date(ends_on.year, 11, 1) - ends_on).days <= GIFT_WINDOW_DAYS
        if not (growing or gifting):
            continue
        if not words or not market_covered(key, words):
            continue
        if any(w in ads for w in MARKET_WORDS.get(key, [])):
            continue
        size = m.get('size_usd')
        ev = [_ev('market_cagr_pct', cagr, 'percent', src.get('date') or ends_on.isoformat(), m.get('cagr_window') or 'forecast', TREND_MIN_CAGR, 'threshold',
                  source=src.get('url'), simulated=False, freshness_days=0, note=cite),
              _ev('market_size_usd', size, 'usd', str(m.get('size_year') or ''), 'year', source=src.get('url'), simulated=False, freshness_days=0),
              _ev('active_ads_naming_it', 0, 'count', ends_on.isoformat(), 'active ads now', 1, 'threshold', source='brain.learnings', simulated=False, freshness_days=0)]
        if gifting:
            sentence = (f'Socks are a holiday gift category ({cite}) and the window opens in {(date(ends_on.year, 11, 1) - ends_on).days} days. '
                        f'No active ad names a gift.')
        else:
            sentence = (f'{m.get("label")} grows {cagr} percent a year' + (f' on ${size / 1e9:,.1f} billion' if size else '') +
                        f' ({cite}). The brand\'s own records carry it and no active ad names it.')
        f = _finding('PROD-R05', key, ends_on, 'medium', ev, sentence, None, 0.5, [f'fixtures.market_trends.{key}', f'{br.brand}.learnings.hook_types' if br else ''],
                     money_reason='no share of the sub-category is measurable without search or marketplace data')
        f['entity'] = {'type': 'metric', 'id': key, 'label': m.get('label') or key, 'category': cat}
        f['id'] = f'{SCREEN}.PROD-R05.{key}'
        f['brain_refs'] = [x for x in f['brain_refs'] if x]
        out.append(f)
    return out
