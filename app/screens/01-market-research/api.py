"""Products and research API: /api/01-market-research/...

  GET overview?brand=bombas   tiles, demand by line, price bands, review mining, candidate pipeline,
                              insights, chart, findings
  GET findings?brand=bombas   the audit findings only (audit.py, contract shape)

Sales numbers come from app/metrics.py through audit.Reader. List prices come from the products table.
Review totals, ladders and competitor price bands come from the brand brain (app/brain/store.py).
Insights are rules in `insights()`, each with the sentence it produces and the capability it maps to.
Missing is unavailable, never 0. Default brand is bombas (simulated sales, public brain). Read-only.
"""
import importlib.util
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _audit():
    spec = importlib.util.spec_from_file_location('market_research_audit', HERE / 'audit.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


audit = _audit()
DEFAULT_BRAND = 'bombas'
CHART_MONTHS = 12
CHART_TOP_LINES = 5
HERO_SHARE = 0.25  # a line with this share of its category's net sales is a hero
CATEGORY_WORD = {'socks': 'sock', 'slippers': 'slipper', 'tshirts': 't-shirt'}

# The candidate pipeline and its margin gate, from the room spec (candidate_pipeline, margin_gate_calc).
PIPELINE_COLUMNS = ['candidate', 'category', 'stage', 'screen_result', 'time_box_days', 'hours_logged',
                    'angle', 'planned_price', 'contribution_margin_pct_modelled', 'gate']
MARGIN_GATE = ('contribution margin modelled = (planned price - COGS - shipping - duty - payment fee) / planned price. '
               'Below the brand floor, a candidate cannot move to sourcing spend.')


def _tile(name, plain, value, unit, **extra):
    out = {'name': name, 'plain': plain, 'unit': unit, 'value': value}
    out.update(extra)
    return out


def _unavail(name, plain, unit, reason, fix):
    return _tile(name, plain, None, unit, unavailable_reason=reason, fix=fix)


def source_of(data, brand):
    return audit.brand_data(brand) if brand else data


def products(data, brand):
    """The products table (list price, pack size, category) or None."""
    try:
        return source_of(data, brand).table('products')
    except (KeyError, ValueError):
        return None


def finance_floor(data, brand, ends_on):
    """The brand's target contribution margin in percent, from finance_inputs, or None."""
    source = source_of(data, brand)
    rows = None
    try:
        rows = source.table('finance_inputs')
    except (KeyError, ValueError):
        path = Path(getattr(source, 'folder', '') or '') / 'finance_inputs.json'
        if path.is_file():
            doc = json.loads(path.read_text(encoding='utf-8'))
            rows = doc.get('rows') if isinstance(doc, dict) else doc
    if not rows:
        return None
    return audit.metrics().finance.Finance(rows).value('target_contribution_margin', ends_on.isoformat())


# ---------------------------------------------------------------- tiles

def tiles(tr, reviews):
    plain_units = 'Units sold in the last 3 whole months, against the same 3 months a year earlier.'
    if tr.get('unavailable'):
        units = _unavail('Units, last 3 months', plain_units, 'n', tr.get('reason'), tr.get('fix'))
        losing = _unavail('Lines losing share', 'Lines that sold less, or grew slower than the store.', 'n',
                          tr.get('reason'), tr.get('fix'))
    else:
        g = tr['store_growth']
        units = _tile('Units, last 3 months', plain_units, tr['store_units'], 'n', delta=g,
                      delta_label=f'vs {tr["year_ago"][0]} to {tr["year_ago"][1]}',
                      window=f'{tr["first"]} to {tr["last"]}', freshness=(tr.get('freshness') or {}).get('as_of'),
                      sources=(tr.get('freshness') or {}).get('sources'))
        hit = [r['line'] for r in tr['lines'] if audit.declining(r)]
        losing = _tile('Lines losing share', f'Of {len(tr["lines"])} lines, how many sold less than last year or grew '
                       f'{audit.SHARE_GAP_POINTS:g} point or more slower than the store. '
                       + (f'{", ".join(hit)}.' if hit else 'None.'), len(hit), 'n',
                       window=f'{tr["first"]} to {tr["last"]}', tone='bad' if hit else 'good')
    rated = [r for r in reviews if r['rating'] is not None]
    if rated:
        low = min(rated, key=lambda r: r['rating'])
        worst = _tile('Lowest rated line', f'{low["line"] or low["key"]}: {low["rating"]} stars from {low["reviews"]:,} '
                      f'reviews on the brand site. Reviews are public, not simulated.', low['rating'], 'stars',
                      window='all reviews to capture', freshness=low['captured_at'], tone='bad' if low['rating'] < 4.3 else None)
    else:
        worst = _unavail('Lowest rated line', 'Average star rating of the weakest line.', 'stars',
                         'no review totals on file', 'reviews')
    return {'units': units, 'losing': losing, 'rating': worst}


# ---------------------------------------------------------------- tables

def demand(tr, reviews):
    """One row per line: units, growth, gap to the store, net sales, and the line's reviews when on file."""
    if tr.get('unavailable'):
        return []
    by = {r['line']: r for r in reviews if r['line']}
    out = []
    for r in tr['lines']:
        rv = by.get(r['line']) or {}
        out.append({'line': r['line'], 'skus': len(r['skus']), 'units': r['units'], 'units_year_ago': r['units_year_ago'],
                    'growth': r['growth'], 'gap_points': r['gap_points'], 'net_sales': r['net_sales'],
                    'rating': rv.get('rating'), 'reviews': rv.get('reviews'), 'low_star_share': rv.get('low_star_share'),
                    'status': {'down': 'down', 'losing_share': 'losing share'}.get(audit.declining(r), 'holding')})
    return out


def competitor_bands(br):
    """Each competitor's per-pair price band parsed from the brain's text. Unparsed parts stay None."""
    if br is None:
        return []
    out = []
    for rec in br.records('competitors'):
        v = rec.get('value')
        if not isinstance(v, dict) or not v.get('price_band_usd'):
            continue
        text = v['price_band_usd']
        med = re.search(r'median (?:about )?(\d+(?:\.\d+)?)', text)
        rng = re.search(r'(\d+(?:\.\d+)?) to (\d+(?:\.\d+)?) per pair', text)
        low = re.search(r'from (\d+(?:\.\d+)?) per pair', text)
        out.append({'id': rec['id'], 'name': v.get('name'), 'text': text,
                    'median': float(med.group(1)) if med else None,
                    'low': float(rng.group(1)) if rng else float(low.group(1)) if low else None,
                    'high': float(rng.group(2)) if rng else None, 'captured_at': (rec.get('source') or {}).get('captured_at')})
    return out


def price_bands(prods, comps):
    """Per line: list price per pair across its packs, against the competitor median band (socks only)."""
    if not prods:
        return {'unavailable': True, 'reason': 'the products table is not connected', 'fix': 'shopify', 'rows': []}
    medians = [c['median'] for c in comps if c['median'] is not None]
    band = (min(medians), max(medians)) if medians else None
    lines = {}
    for p in prods:
        if p.get('price') is None or not p.get('items_per_unit'):
            continue
        line = audit.metrics().product_line(p.get('title'))
        per = round(p['price'] / p['items_per_unit'], 2)
        g = lines.setdefault(line, {'line': line, 'category': p.get('category'), 'packs': [], 'per_pair': []})
        g['packs'].append(p.get('title'))
        g['per_pair'].append(per)
    rows = []
    for g in lines.values():
        lo, hi = min(g['per_pair']), max(g['per_pair'])
        if g['category'] != 'socks' or band is None:
            position = None
        else:
            position = 'below' if hi < band[0] else 'above' if lo > band[1] else 'inside'
        rows.append({'line': g['line'], 'category': g['category'], 'packs': len(g['packs']), 'per_pair_low': lo,
                     'per_pair_high': hi, 'band_low': band[0] if band and g['category'] == 'socks' else None,
                     'band_high': band[1] if band and g['category'] == 'socks' else None, 'position': position})
    rows.sort(key=lambda r: (r['category'] != 'socks', r['per_pair_low']))
    return {'unavailable': False, 'rows': rows, 'band': band, 'competitors': comps,
            'basis': ('list price over pairs or items in the pack, from the simulated catalog; competitor medians are per pair '
                      'from their public catalogs, as the brand brain holds them')}


def review_mining(reviews, lads):
    """One tile per reviewed line: what works, what fails, and the objection ladders built from its reviews."""
    out = []
    for rv in sorted(reviews, key=lambda r: -(r['reviews'] or 0)):
        hits = [l for l in lads if rv['record'] in l['reviews_records']]
        out.append({'line': rv['line'] or rv['key'], 'product': rv['product'], 'pdp': rv['pdp'], 'rating': rv['rating'],
                     'reviews': rv['reviews'], 'low_star_share': rv['low_star_share'], 'works': rv['praise'],
                     'fails': rv['issues'], 'record': rv['record'],
                     'ladders': [{'id': l['id'], 'theme': l['theme'],
                                  'rungs': [{'level': g['level'], 'doubt': g['doubt'], 'one_star': g['one_star'],
                                             'proof': g['proof']} for g in l['rungs'] if rv['record'] in g['from_reviews']]}
                                 for l in hits]})
    return out


def ladder_summary(lads):
    return [{'id': l['id'], 'theme': l['theme'], 'one_star': l['one_star'], 'five_star': l['five_star'],
             'what_works': l['what_works'], 'what_fails': l['what_fails']} for l in lads]


# ---------------------------------------------------------------- insights

def insights(tr, bands, pipeline):
    """The rules behind the insight cards. Each returns the sentence it produces and its capability."""
    out = []
    rule = (f'a line with {round(HERO_SHARE * 100)} percent or more of its category\'s net sales in the last 3 whole '
            f'months, and no next-SKU candidate open in the pipeline')
    if tr.get('unavailable'):
        out.append({'id': 'hero_no_extension', 'severity': 'info', 'capability': None, 'autonomy': None,
                    'sentence': 'Line sales are not connected, so the hero line cannot be named.', 'rule': rule})
    else:
        cat = {}
        for r in tr['lines']:
            cat.setdefault(audit_category(r, bands), []).append(r)
        heroes = []
        for c, rows in cat.items():
            total = sum(r['net_sales'] for r in rows)
            for r in rows:
                if total and r['net_sales'] / total >= HERO_SHARE and len(rows) > 1:
                    heroes.append((r, c, r['net_sales'] / total))
        heroes.sort(key=lambda h: -h[0]['net_sales'])
        open_next = [p for p in pipeline if p.get('stage') not in ('go', 'kill')]
        if heroes and not open_next:
            r, c, share = heroes[0]
            out.append({'id': 'hero_no_extension', 'severity': 'medium', 'capability': 'PROD-C06', 'autonomy': 'agent',
                        'sentence': f'{r["line"]} brings in {round(share * 100)} percent of {CATEGORY_WORD.get(c, c)} sales with no next SKU '
                                    f'in the pipeline. The pipeline is empty.', 'rule': rule})
        else:
            out.append({'id': 'hero_no_extension', 'severity': 'info', 'capability': None, 'autonomy': None,
                        'sentence': 'Every hero line has a next SKU open in the pipeline.' if heroes else
                                    'No line holds a quarter of its category.', 'rule': rule})
    rule = 'sock lines whose per-pair list price sits below, inside or above the band of competitor median prices'
    rows = [r for r in bands.get('rows') or [] if r['position']]
    if not rows or not bands.get('band'):
        out.append({'id': 'price_band', 'severity': 'info', 'capability': None, 'autonomy': None,
                    'sentence': 'No competitor price band is on file, so price position cannot be read.', 'rule': rule})
    else:
        lo, hi = bands['band']
        below = [r['line'] for r in rows if r['position'] == 'below']
        above = [r['line'] for r in rows if r['position'] == 'above']
        sentence = (f'{len(below)} of {len(rows)} sock lines sell for less per pair than the lowest competitor median '
                    f'of ${lo:,.0f}.')
        inside = [r['line'] for r in rows if r['position'] == 'inside']
        if inside:
            sentence += f' {", ".join(inside)} {"sits" if len(inside) == 1 else "sit"} inside the ${lo:,.0f} to ${hi:,.0f} band.'
        if above:
            sentence += f' {len(above)} {"sits" if len(above) == 1 else "sit"} above it.'
        out.append({'id': 'price_band', 'severity': 'medium' if below else 'info', 'capability': 'PROD-C04',
                    'autonomy': 'agent', 'sentence': sentence, 'rule': rule})
    return out


def audit_category(row, bands):
    for b in bands.get('rows') or []:
        if b['line'] == row['line']:
            return b['category']
    return 'store'


# ---------------------------------------------------------------- chart

def chart(rd):
    last = rd.last_month
    first = audit.month_add(last, 1 - CHART_MONTHS)
    r = rd.m('units', first, last, by='line_month')
    if r.get('unavailable'):
        return {'unavailable': True, 'reason': r.get('reason'), 'fix': r.get('fix')}
    months = r['months']
    totals = {}
    for g in r['groups']:
        totals[g['line']] = totals.get(g['line'], 0) + g['units']
    top = [l for l, _ in sorted(totals.items(), key=lambda kv: -kv[1])[:CHART_TOP_LINES]]
    series = {l: {m: None for m in months} for l in top}
    other = {m: None for m in months}
    for g in r['groups']:
        if g['line'] in series:
            series[g['line']][g['month']] = g['units']
        else:
            other[g['month']] = (other[g['month']] or 0) + g['units']
    out = [{'name': l, 'values': [series[l][m] for m in months]} for l in top]
    if len(totals) > len(top):
        out.append({'name': f'Other {len(totals) - len(top)} lines', 'values': [other[m] for m in months]})
    return {'labels': months, 'series': out, 'window': f'{months[0]} to {months[-1]}', 'notes': r.get('notes')}


# ---------------------------------------------------------------- overview

def overview(data, brand):
    ends_on = audit.last_full_day(data, brand)
    rd = audit.Reader(data, brand, ends_on)
    b = source_of(data, brand).brand
    head = {'brand': b.get('brand'), 'name': b.get('name'), 'as_of': b.get('as_of'),
            'simulated': bool(b.get('simulated') or b.get('fictional')), 'market': b.get('market')}
    br = audit.brain(brand, today=ends_on) if brand else None
    tr = audit.trend(rd)
    reviews = audit.review_lines(br)
    lads = audit.ladders(br)
    bands = price_bands(products(data, brand), competitor_bands(br))
    pipeline = []  # seeded empty: no candidate has been screened yet
    floor = finance_floor(data, brand, ends_on)
    findings = audit.run(brand, {'ends_on': ends_on.isoformat()}, data=data)
    return {'brand': head, 'window': {'ends_on': ends_on.isoformat(), 'trend': None if tr.get('unavailable') else
                                      {'months': [tr['first'], tr['last']], 'year_ago': tr['year_ago']}},
            'tiles': tiles(tr, reviews), 'demand': demand(tr, reviews), 'store_growth': tr.get('store_growth'),
            'price_bands': bands, 'reviews': review_mining(reviews, lads), 'ladders': ladder_summary(lads),
            'pipeline': {'columns': PIPELINE_COLUMNS, 'rows': pipeline, 'gate_rule': MARGIN_GATE,
                         'floor_pct': floor, 'floor_source': 'finance_inputs.target_contribution_margin' if floor is not None else None},
            'insights': insights(tr, bands, pipeline), 'chart': chart(rd), 'findings': findings, 'rules': audit.RULES}


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
        if req.path == ['findings']:
            return {'findings': audit.run(brand, None, data=data), 'rules': audit.RULES}
    except ValueError as exc:
        return 400, {'error': str(exc)}
    return 404, {'error': 'not found', 'routes': ['overview', 'findings']}
