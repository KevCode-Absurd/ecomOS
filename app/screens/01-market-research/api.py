"""Market and product research API: /api/01-market-research/...

  GET overview?brand=bombas   head, orientation numbers, what is wrong (findings grouped by rule),
                              the desk (demand by line, price bands, review mining, candidate pipeline),
                              the audit (findings and rules)
  GET findings?brand=bombas   the audit findings only (audit.py, contract shape)
  GET rank?brand=bombas&window=28d
                              served by app/server.py through app/rank.py, which calls this module's
                              rank(brand, window): real titles, steps and artefacts per rule (depth.md 5)

Sales numbers come from app/metrics.py through audit.Reader. List prices come from the products table.
Review totals, ladders and competitor price bands come from the brand brain (app/brain/store.py).
Missing is unavailable, never 0. Default brand is bombas (simulated sales, public brain). Read-only.
Screen JS holds no brand fact: every name, price, threshold and sentence comes from here.
"""
import datetime as dt
import importlib.util
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parents[1]
SCREEN = '01-market-research'


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


audit = _load('market_research_audit', HERE / 'audit.py')
rank_mod = _load('market_research_rank_engine', APP / 'rank.py')
DEFAULT_BRAND = 'bombas'
CATEGORY_WORD = {'socks': 'sock', 'slippers': 'slipper', 'tshirts': 't-shirt', 'underwear': 'underwear', 'footwear': 'footwear'}

# The candidate pipeline and its margin gate, from the room spec (candidate_pipeline, margin_gate_calc).
PIPELINE_COLUMNS = ['candidate', 'category', 'stage', 'screen_result', 'time_box_days', 'hours_logged',
                    'angle', 'planned_price', 'contribution_margin_pct_modelled', 'gate']
MARGIN_GATE = ('contribution margin modelled = (planned price - COGS - shipping - duty - payment fee) / planned price. '
               'Below the brand floor, a candidate cannot move to sourcing spend.')


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


# ---------------------------------------------------------------- brain reads

def brain_value(br, rid):
    if br is None:
        return None
    r = br.get(rid)
    return r.get('value') if r else None


def brain_date(br):
    """Days since the newest dated record in the sections this screen reads, or None."""
    if br is None:
        return None
    newest = None
    for sec in ('positioning', 'diagnosis', 'competitors', 'avatars', 'products', 'seo_facts', 'learnings', 'economics'):
        for r in br.records(sec):
            if r['date'] != 'undated' and (newest is None or r['date'] > newest):
                newest = r['date']
    return newest


def product_lines(br):
    v = brain_value(br, f'{br.brand}.products.lines') if br else None
    return [str(x) for x in v] if isinstance(v, list) else []


# ---------------------------------------------------------------- orientation

def orientation(tr, br, ends_on, findings):
    """3 to 6 small numbers beside the plan. Null renders unavailable; never 0 for unknown."""
    open_f = [f for f in findings if f['status'] == 'open']
    stake = [f['money_at_stake']['usd'] for f in open_f if f.get('money_at_stake')]
    lines = product_lines(br)
    newest = brain_date(br)
    fresh = max((ends_on - dt.date.fromisoformat(newest)).days, 0) if newest else None
    revenue = brain_value(br, f'{br.brand}.economics.revenue_point_usd') if br else None
    items = [
        {'label': 'units, last 3 months', 'value': None if tr.get('unavailable') else tr['store_units'], 'unit': 'n',
         'delta': None if tr.get('unavailable') else tr['store_growth'], 'higher_is_better': True,
         'title': 'whole months against the same months a year earlier, simulated'},
        {'label': 'lines losing share', 'value': None if tr.get('unavailable') else sum(1 for r in tr['lines'] if audit.declining(r)),
         'unit': 'n', 'tone': 'bad' if not tr.get('unavailable') and any(audit.declining(r) for r in tr['lines']) else None},
        {'label': 'product lines in the brain', 'value': len(lines) or None, 'unit': 'n', 'title': ', '.join(lines)},
        {'label': 'annual revenue, public band', 'value': revenue, 'unit': '$', 'title': 'economics.revenue_point_usd, the simulation point'},
        {'label': 'open findings', 'value': len(open_f), 'unit': 'n', 'tone': 'bad' if open_f else 'good'},
        {'label': 'stake known', 'value': sum(stake) if stake else None, 'unit': '$', 'title': 'sum of money at stake where a formula exists'},
        {'label': 'brain read', 'value': fresh, 'unit': 'd', 'suffix': ' ago', 'title': 'days since the newest research record'},
    ]
    return items


# ---------------------------------------------------------------- desk tables (round 0, restyled as verdicts)

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
        return {'unavailable': True, 'reason': 'the products table is not connected', 'fix': 'shopify', 'rows': [],
                'competitors': comps, 'band': None}
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
    """One row per reviewed line: what works, what fails, and the objection ladders built from its reviews."""
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


# ---------------------------------------------------------------- the trend desk: category mix against the public market

def public_mix(br):
    """The public category mix records the brain holds, as bands to compare our simulated mix against."""
    out = []
    if br is None:
        return out
    for r in br.records('economics'):
        v = r.get('value')
        if not isinstance(v, dict):
            continue
        if 'socks_and_slippers_pct' in v:
            out.append({'categories': ['socks', 'slippers'], 'share': v['socks_and_slippers_pct'] / 100, 'as_of': v.get('as_of'), 'record': r['id'], 'text': r.get('text')})
            out.append({'categories': ['underwear', 'tshirts'], 'share': v['underwear_and_tshirts_pct'] / 100, 'as_of': v.get('as_of'), 'record': r['id'], 'text': r.get('text')})
        if 'footwear_share_pct' in v:
            out.append({'categories': ['footwear', 'slippers'], 'share': v['footwear_share_pct'] / 100, 'as_of': v.get('as_of'), 'record': r['id'], 'text': r.get('text')})
    return out


def trends(br, mix):
    """The industry and sub-industry strips: public markets from the web pass, each tied to our category and its coverage."""
    fx = audit.market_trends()
    words = audit.brand_words(br)
    ads = audit.ad_words(br)
    ours = {r['category']: r for r in (mix.get('rows') or [])}
    markets = []
    for m in (fx or {}).get('markets') or []:
        key = m.get('key')
        cat = audit.MARKET_CATEGORY.get(key)
        our = ours.get(cat) if cat else None
        srcs = m.get('sources') or []
        markets.append({'key': key, 'label': m.get('label'), 'size_usd': m.get('size_usd'), 'size_year': m.get('size_year'),
                        'cagr_pct': m.get('cagr_pct'), 'cagr_window': m.get('cagr_window'), 'direction': m.get('direction'),
                        'series': m.get('series') or [], 'drivers': m.get('drivers') or [], 'sources': srcs,
                        'our_category': cat, 'covered': audit.market_covered(key, words) if words else None,
                        'advertised': any(w in ads for w in audit.MARKET_WORDS.get(key, [])) if ads else None,
                        'finding_id': f'{SCREEN}.PROD-R05.{key}',
                        'our_growth': our.get('growth') if our else None, 'our_net_share': our.get('net_share') if our else None,
                        'gap_points': round(our['growth'] * 100 - m['cagr_pct'], 1) if our and our.get('growth') is not None and isinstance(m.get('cagr_pct'), (int, float)) else None})
    return {'captured_at': (fx or {}).get('captured_at'), 'note': (fx or {}).get('note'), 'markets': markets,
            'on_file': fx is not None, 'public_mix': public_mix(br)}


# ---------------------------------------------------------------- rank: findings to actions with real steps

def _cat_word(f):
    return CATEGORY_WORD.get((f.get('entity') or {}).get('category') or '', 'category')


def _line(f):
    return (f.get('entity') or {}).get('label', '').replace(' (product line)', '')


def _ev_value(f, metric):
    for e in f.get('evidence') or []:
        if e.get('metric') == metric:
            return e.get('value')
    return None


def _check_on(f, days):
    end = f.get('last_seen') or f.get('first_seen')
    return (dt.date.fromisoformat(str(end)[:10]) + dt.timedelta(days=days)).isoformat() if end else None


def recipe(f):
    """Per rule: title, why, owner, artefact, steps, size, stop rule, check date. Every step names who does it."""
    rid = f['rule_id']
    line = _line(f)
    if rid == 'PROD-R01':
        growth = _ev_value(f, 'unit_growth')
        store = next((e.get('baseline') for e in f['evidence'] if e.get('metric') == 'unit_growth'), None)
        m = f.get('money_at_stake') or {}
        return {
            'title': f'Find why {line} is losing share and brief the fix',
            'owner': 'agent', 'artefact': {'kind': 'research_note', 'label': f'a 1-page read on {line}: price, reviews, ads, stock, with the fix named'},
            'steps': [
                {'n': 1, 'who': 'agent', 'text': f'Split {line} units by SKU and month for the 3 months and the same months a year earlier.'},
                {'n': 2, 'who': 'agent', 'text': 'Check the 4 usual causes in order: stock-outs, price moves, review score drop, ad spend on the line.'},
                {'n': 3, 'who': 'agent', 'text': 'Write the read with the cause ranked by evidence and one action per cause: restock, price test, review fix, ad brief.'},
                {'n': 4, 'who': 'person', 'text': 'Pick the action. It goes to the screen that owns it (offers, creative, supply).'},
                {'n': 5, 'who': 'agent', 'text': 'Re-read the line after the next whole month. The finding resolves when growth is within 1 point of the store.'}],
            'size': {'text': f'{rank_mod_money(m)} of net sales the line would have kept at store growth', 'usd': m.get('usd')} if m else None,
            'stop_rule': 'stop the fix if the line is within 1 point of the store for 2 whole months',
            'check_on': _check_on(f, 31), 'time_to_ship_hours': 4,
            'win_rule': f'{line} unit growth within 1 point of the store, 2 months running' + (f' (now {round(growth * 100, 1)} percent against {round(store * 100, 1)})' if growth is not None and store is not None else ''),
        }
    if rid == 'PROD-R02':
        top = next((e.get('top_issues') for e in f['evidence'] if e.get('top_issues')), None) or []
        rungs = [e for e in f['evidence'] if e.get('rung')]
        m = f.get('money_at_stake') or {}
        return {
            'title': f'Fix the top complaint on {line}: {top[0] if top else "the top issue"}',
            'owner': 'agent_drafts', 'artefact': {'kind': 'page_section', 'label': f'a PDP proof section for {line} answering "{top[0] if top else "the top issue"}", plus a product ticket when the cause is the product'},
            'steps': [
                {'n': 1, 'who': 'agent', 'text': f'Read the 1 and 2 star reviews for {line} and count the issues: ' + ', '.join(top[:3]) + '.'},
                {'n': 2, 'who': 'agent', 'text': 'Sort each issue as product (needs a spec change), fit (needs a size guide or fit note) or expectation (needs the PDP to say it first).'},
                {'n': 3, 'who': 'agent', 'text': 'Draft the PDP section that answers the expectation and fit issues with the proof on file' + (f' (ladder rungs: {", ".join(e["rung"] for e in rungs[:3])})' if rungs else '') + '.'},
                {'n': 4, 'who': 'person', 'text': 'Approve the section. Send product issues to supply as a spec ticket.'},
                {'n': 5, 'who': 'agent', 'text': 'Track the 1 and 2 star share of new reviews for 60 days.'}],
            'size': {'text': f'{rank_mod_money(m)} of last month\'s sales went into the extra bad experiences', 'usd': m.get('usd')} if m else None,
            'stop_rule': 'stop if the 1 and 2 star share of new reviews is under the brand median for 60 days',
            'check_on': _check_on(f, 60), 'time_to_ship_hours': 6,
            'win_rule': 'low-star share of new reviews at or under the brand median',
        }
    if rid == 'PROD-R03':
        cat = _cat_word(f)
        share = _ev_value(f, 'category_share_net_sales')
        return {
            'title': f'Plan the next {cat} SKU beside {line}',
            'owner': 'agent', 'artefact': {'kind': 'research_note', 'label': f'3 next-SKU candidates for {cat} with the angle, the price point and the demand check, added to the pipeline with a time box'},
            'steps': [
                {'n': 1, 'who': 'agent', 'text': f'Read {line} reviews for the unmet asks (what buyers wish it did) and the sizes, colours and packs that sell out first.'},
                {'n': 2, 'who': 'agent', 'text': 'Check the category conversation and competitor launches for the sub-category buyers are moving to.'},
                {'n': 3, 'who': 'agent', 'text': 'Write 3 candidates, each with an angle that is not a competitor claim, a planned price and a 10-day research time box. Add them to the pipeline.'},
                {'n': 4, 'who': 'person', 'text': 'Kill or keep each candidate. Kept ones go to the margin gate.'}],
            'size': {'text': f'{line} is {round(share * 100)} percent of {cat} sales' if share is not None else 'size unavailable', 'usd': None},
            'stop_rule': 'stop when 1 candidate for the category is open in the pipeline',
            'check_on': _check_on(f, 14), 'time_to_ship_hours': 8,
            'win_rule': '1 or more open next-SKU candidates for the category',
        }
    if rid == 'PROD-R04':
        m = f.get('money_at_stake') or {}
        cat = line
        return {
            'title': f'Close the growth gap on {cat} against its market',
            'owner': 'agent', 'artefact': {'kind': 'research_note', 'label': f'a read on why {cat} trails its market, with the 3 moves ranked (range, price, reach)'},
            'steps': [
                {'n': 1, 'who': 'agent', 'text': f'Compare {cat} unit growth by month with the market growth line and name the months that fell behind.'},
                {'n': 2, 'who': 'agent', 'text': 'Check range breadth, price position and paid reach for the category against the 3 closest competitors.'},
                {'n': 3, 'who': 'agent', 'text': 'Write the read with the one move most likely to close the gap and the number it must move.'},
                {'n': 4, 'who': 'person', 'text': 'Approve the move. It goes to offers, creative or supply.'},
                {'n': 5, 'who': 'agent', 'text': 'Re-read after the next whole month.'}],
            'size': {'text': f'{rank_mod_money(m)} of sales the category would add at market pace', 'usd': m.get('usd')} if m else None,
            'stop_rule': 'stop when the category grows at or above its market rate for 2 whole months',
            'check_on': _check_on(f, 31), 'time_to_ship_hours': 4, 'win_rule': 'category unit growth at or above the market rate',
        }
    if rid == 'PROD-R05':
        key = (f.get('entity') or {}).get('id') or ''
        label = (f.get('entity') or {}).get('label') or key
        gift = key == 'gifting_socks'
        cagr = _ev_value(f, 'market_cagr_pct')
        return {
            'title': (f'Brief a gifting flight before the holiday window' if gift else f'Brief the first ad for {label}'),
            'owner': 'agent_drafts',
            'artefact': {'kind': 'ad_brief', 'label': (f'a gift-flight brief: 3 hooks, packs and price points, the send dates, the measure'
                                                     if gift else f'an ad brief for {label}: 3 hooks from the brain, the proof on file, the line and the offer')},
            'steps': [
                {'n': 1, 'who': 'agent', 'text': (f'Pull the gift packs, the gift card and last year\'s November and December sales by line.' if gift else
                                                  f'Pull the lines, claims and review praise that name {label} in the brain.')},
                {'n': 2, 'who': 'agent', 'text': 'Read what the 3 closest competitors run on it in the Ad Library (format, hook, offer), signals only.'},
                {'n': 3, 'who': 'agent', 'text': 'Draft the brief: 3 hooks, the proof for each, the product and the offer, one static and one video.'},
                {'n': 4, 'who': 'person', 'text': 'Approve the brief. Creative makes the ads; paid social sets the test.'},
                {'n': 5, 'who': 'agent', 'text': 'Read the test at 14 days: cost per order against the account median.'}],
            'size': {'text': (f'{label}: {cagr} percent a year' if cagr is not None else 'growth rate unavailable') + ', no active ad names it', 'usd': None},
            'stop_rule': 'stop the flight if cost per order is over 1.3 times the account median for 7 days',
            'check_on': _check_on(f, 14 if not gift else 7), 'time_to_ship_hours': 6,
            'win_rule': 'at least 1 active ad names the lane and its cost per order is at or under the account median',
        }
    if rid == 'PROD-R06':
        ent = f.get('entity') or {}
        label = (ent.get('label') or ent.get('id') or '').lower()
        names = ent.get('names') or 'the competitors'
        sold = ent.get('sold')
        proof = ent.get('kind') == 'proof'
        n = _ev_value(f, 'competitors_pushing')
        if sold:
            title = f'Brief our answer on {label}: {names} run it, we do not'
            kind, art = 'ad_brief', f'an ad brief on {label}: our proof against theirs, 3 hooks, one static and one video, signals only from their ads'
        elif proof:
            title = f'Build the proof for {label} before we advertise it'
            kind, art = 'research_note', f'a proof plan for {label}: what we can claim today, what needs a test or a policy, and the first ad it unlocks'
        else:
            title = f'Screen a {label} candidate: {names} push it and we have no line'
            kind, art = 'research_note', f'a fast screen of {label} as a next SKU: demand, competition, store fit, with a go or kill'
        return {
            'title': title, 'owner': 'agent_drafts' if sold else 'agent',
            'artefact': {'kind': kind, 'label': art},
            'steps': [
                {'n': 1, 'who': 'agent', 'text': f'Read the {n} competitor pages on {label} in the Ad Library by page id: format, hook, run length, offer. Signals only, nothing copied.'},
                {'n': 2, 'who': 'agent', 'text': ('Pull our own proof for it from the brain: claims, review praise, ladder rungs with proof.' if sold else
                                                  'Check the brain for anything we already hold on it: a claim, a review theme, a past test.')},
                {'n': 3, 'who': 'agent', 'text': ('Draft the brief: the one claim we can back, 3 hooks, product and offer, one static and one video.' if sold else
                                                  ('Write the proof plan: claim by tier, what needs a test or a policy, the first ad it unlocks.' if proof else
                                                   'Run the fast screen: demand signal, sellers already in it, fit with our lines and price ladder.'))},
                {'n': 4, 'who': 'person', 'text': ('Approve the brief. Creative makes the ads; paid social sets the test.' if sold else 'Decide: go to the pipeline, or kill it and log why.')},
                {'n': 5, 'who': 'agent', 'text': 'Re-read the Ad Library on the next pull. The finding resolves when an active ad of ours names the lane.'}],
            'size': {'text': f'{n} competitors, {_ev_value(f, "competitor_active_ads")} active ads on it', 'usd': None},
            'stop_rule': 'stop if the competitors drop the lane (no ad live 30 days) before we ship',
            'check_on': _check_on(f, 14), 'time_to_ship_hours': 6 if sold else 8,
            'win_rule': 'an active ad of ours names the lane, or the candidate has a logged go or kill',
        }
    if rid == 'PROD-R07':
        ent = f.get('entity') or {}
        label = (ent.get('label') or ent.get('id') or '').lower()
        doubt = ent.get('doubt') or label
        onsite = ent.get('answered_on_site')
        c, p = _ev_value(f, 'complaint_quotes'), next((e.get('baseline') for e in f['evidence'] if e.get('metric') == 'complaint_quotes'), None)
        return {
            'title': f'Answer "{doubt}" in an ad and on the page',
            'owner': 'agent_drafts',
            'artefact': {'kind': 'ad_brief', 'label': f'an ad brief that answers "{doubt}" with the proof on file, plus the PDP section that carries the same answer'},
            'steps': [
                {'n': 1, 'who': 'agent', 'text': f'Pull the {c} complaint quotes and {p} praise quotes on {label} from the ladder, with the rung each sits on.'},
                {'n': 2, 'who': 'agent', 'text': ('Pull the site proof that already answers it (claims, guarantee, policy) and check its claim tier.' if onsite else
                                                  'Find or build the proof: a claim the founder can approve, a policy, or a test result. Nothing ships on an unapproved claim.')},
                {'n': 3, 'who': 'agent', 'text': 'Draft the ad brief: the doubt in the buyer\'s words as the hook, the proof as the answer, one static and one video. Reddit words inform the hook and are never quoted as a testimonial.'},
                {'n': 4, 'who': 'agent', 'text': 'Draft the PDP section with the same answer next to the price.'},
                {'n': 5, 'who': 'person', 'text': 'Approve the claim tier and the brief. Creative and landing pages ship them.'},
                {'n': 6, 'who': 'agent', 'text': 'Read at 30 days: 1-star share of new reviews on the theme and cost per order of the ad against the account median.'}],
            'size': {'text': f'{c} complaint quotes against {p} praise, no active ad answers it', 'usd': None},
            'stop_rule': 'stop the ad if cost per order is over 1.3 times the account median for 7 days; keep the page section',
            'check_on': _check_on(f, 30), 'time_to_ship_hours': 8,
            'win_rule': 'complaint quotes on the theme fall below praise quotes in new reviews over 60 days',
        }
    if rid == 'PROD-R08':
        ent = f.get('entity') or {}
        label = ent.get('label') or ent.get('id') or ''
        names = ent.get('names') or 'competitors'
        return {
            'title': f'Decide our position on {label.lower()}: claim it, counter it, or leave it',
            'owner': 'agent',
            'artefact': {'kind': 'research_note', 'label': f'a 1-page position on {label.lower()}: what we can claim with proof, what {names} claim, the counter-position, and the brain record to write'},
            'steps': [
                {'n': 1, 'who': 'agent', 'text': f'List what {names} claim on {label.lower()} in their ads (signals only) and where their proof sits.'},
                {'n': 2, 'who': 'agent', 'text': 'Check our own facts: materials, factories, policies, certifications. Name what we can claim today with a source.'},
                {'n': 3, 'who': 'agent', 'text': 'Write the position: claim it (with the proof), counter it (what we offer instead, in the buyer\'s words), or leave it (why it does not move our buyer).'},
                {'n': 4, 'who': 'person', 'text': 'Pick one. The choice is written to the brain as an approved positioning record.'},
                {'n': 5, 'who': 'agent', 'text': 'If claimed or countered, hand the line to copy and creative as a brief.'}],
            'size': {'text': f'{_ev_value(f, "competitors_claiming_it")} competitor pages claim it', 'usd': None},
            'stop_rule': 'stop if the survey trend turns down in the next web pass',
            'check_on': _check_on(f, 30), 'time_to_ship_hours': 4,
            'win_rule': 'an approved positioning record on the preference exists in the brain',
        }
    if rid == 'PROD-R09':
        ent = f.get('entity') or {}
        frame = ent.get('frame') or 'the category frame'
        comp = ent.get('competitor') or 'the competitor'
        share = ent.get('proof_share')
        peer = ent.get('peer_proof_share')
        return {
            'title': f'Take a position on "{frame}": put our proof next to the price',
            'owner': 'agent_drafts',
            'artefact': {'kind': 'page_section', 'label': f'a proof section for the top sock PDPs (guarantee, construction, wear-life numbers) and 2 ad hooks that answer "{frame}" against {comp}'},
            'steps': [
                {'n': 1, 'who': 'agent', 'text': f'Read the Reddit threads framed as "{frame}" and list the proof they trust ({comp} is recommended instead). Reddit is never quoted as a testimonial.'},
                {'n': 2, 'who': 'agent', 'text': 'Pull our proof points from the brain (guarantee, construction, reviews with a wear-life number) and tier each claim.'},
                {'n': 3, 'who': 'agent', 'text': 'Draft the PDP proof section next to the price and 2 ad hooks that lead with the proof, not the mission.'},
                {'n': 4, 'who': 'person', 'text': 'Approve the claims and the section. Landing pages and creative ship them.'},
                {'n': 5, 'who': 'agent', 'text': 'Re-read the map on the next Ad Library pull: the finding resolves when our proof share of hooks reaches the competitor median.'}],
            'size': {'text': (f'proof in {round(share * 100)} percent of our hook types against a competitor median of {round(peer * 100)}' if share is not None and peer is not None else 'proof share unavailable'), 'usd': None},
            'stop_rule': 'stop the ad hooks if cost per order is over 1.3 times the account median for 7 days; keep the page section',
            'check_on': _check_on(f, 30), 'time_to_ship_hours': 10,
            'win_rule': 'proof share of active hook types at or above the competitor median, and the brand named in the next Reddit pull on the frame',
        }
    if rid == 'PROD-R10':
        ent = f.get('entity') or {}
        label = ent.get('label') or ent.get('id') or 'this avatar'
        names = ent.get('names') or 'competitors'
        return {
            'title': f'Screen an offer for {label}: {names} pitch to them and we have nothing on file',
            'owner': 'agent',
            'artefact': {'kind': 'research_note', 'label': f'a fast screen for {label}: the job ({(ent.get("job") or "")[:80]}), which line could serve it, the demand signal, and a go or kill'},
            'steps': [
                {'n': 1, 'who': 'agent', 'text': f'Read what {names} say to {label} in their ads (signals only) and which product they lead with.'},
                {'n': 2, 'who': 'agent', 'text': 'Check our catalog and reviews for anything that already serves the job; note the gap if nothing does.'},
                {'n': 3, 'who': 'agent', 'text': 'Run the fast screen: demand, competition, store fit. Write a go (candidate to the pipeline with a time box) or a kill with the reason.'},
                {'n': 4, 'who': 'person', 'text': 'Decide. A go writes the candidate; a kill writes a decision so it is not re-argued.'}],
            'size': {'text': f'{_ev_value(f, "competitors_serving")} competitor pages pitch to them', 'usd': None},
            'stop_rule': 'stop at the time box: 10 days of research, then decide',
            'check_on': _check_on(f, 10), 'time_to_ship_hours': 6,
            'win_rule': 'a logged go or kill for the avatar',
        }
    if rid == 'PROD-R11':
        ent = f.get('entity') or {}
        label = ent.get('label') or ent.get('id') or 'this avatar'
        theme = audit.THEME_LABEL.get(ent.get('theme'), ent.get('theme') or 'their theme').lower()
        m = f.get('money_at_stake') or {}
        in_ads = ent.get('in_ads')
        return {
            'title': f'Win back {label}: answer {theme} where they buy',
            'owner': 'agent_drafts',
            'artefact': {'kind': 'offer', 'label': f'an offer and message spec for {label}: the proof for {theme} next to the price, a guarantee or fit promise where the brain holds one, an email to past buyers, and the ad hook' + ('' if in_ads else ' (no active ad speaks to them today)')},
            'steps': [
                {'n': 1, 'who': 'agent', 'text': f'Pull the avatar record, its quotes and the {theme} ladder rungs with proof.'},
                {'n': 2, 'who': 'agent', 'text': 'Draft the spec: the one promise that answers their top doubt, where it shows (PDP, cart, post-purchase email, ad), and the offer if one is needed (a replacement pledge, a fit exchange, a pack price per wear).'},
                {'n': 3, 'who': 'agent', 'text': 'Size it: the share of buyers, the repeat revenue at risk, the cost of the promise from finance inputs.'},
                {'n': 4, 'who': 'person', 'text': 'Approve the promise and its cost. Offers, email and creative ship their parts.'},
                {'n': 5, 'who': 'agent', 'text': 'Read at 60 days: repeat rate of buyers who saw the promise against those who did not, and the theme\'s complaint share in new reviews.'}],
            'size': {'text': f'{rank_mod_money(m)} of repeat revenue at risk in 28 days', 'usd': m.get('usd')} if m else None,
            'stop_rule': 'stop the offer if its cost passes 2 percent of the segment\'s net revenue in the window; keep the proof on the page',
            'check_on': _check_on(f, 60), 'time_to_ship_hours': 12,
            'win_rule': 'repeat rate of the segment up 2 points, or complaint share on the theme under 50 percent in new reviews',
        }
    if rid == 'PROD-R13':
        ent = f.get('entity') or {}
        label = (ent.get('label') or ent.get('id') or '').lower()
        terms = ', '.join(ent.get('terms') or [])
        kind = {'competitor': 'page_section', 'brand': 'page_section', 'category': 'landing_page', 'problem': 'page_section'}.get(ent.get('id'), 'page_section')
        return {
            'title': f'Build the page that answers {label}',
            'owner': 'agent_drafts',
            'artefact': {'kind': kind, 'label': (f'a category lander for {terms}' if kind == 'landing_page' else f'a page section (or FAQ page) that answers {terms}, with the proof on file')},
            'steps': [
                {'n': 1, 'who': 'agent', 'text': f'List the queries in the group by impressions and the page each one lands on today.'},
                {'n': 2, 'who': 'agent', 'text': 'Draft the page from the brain: the answer in the buyer\'s words, the proof, the product it leads to, approved claims only.'},
                {'n': 3, 'who': 'person', 'text': 'Approve the copy and the claims. Landing pages ship it; SEO sets the internal links.'},
                {'n': 4, 'who': 'agent', 'text': 'Read at 28 days: impressions, clicks and position for the group against this window.'}],
            'size': {'text': (f'{_ev_value(f, "impressions"):,} impressions, {_ev_value(f, "clicks"):,} clicks in 28 days with no page'
                              if _ev_value(f, 'impressions') is not None and _ev_value(f, 'clicks') is not None else 'demand unavailable, no page'), 'usd': None},
            'stop_rule': 'stop if clicks on the group do not rise within 2 windows; keep the page if position improves',
            'check_on': _check_on(f, 28), 'time_to_ship_hours': 8,
            'win_rule': 'clicks on the group up 20 percent over the next 28 days, or position under 10',
        }
    if rid == 'PROD-R14':
        ent = f.get('entity') or {}
        age, box = _ev_value(f, 'candidate_pipeline_age_days'), next((e.get('baseline') for e in f['evidence'] if e.get('metric') == 'candidate_pipeline_age_days'), None)
        return {
            'title': f'Decide or kill {ent.get("label")}: {age} days at {ent.get("stage")}, box was {box}',
            'owner': 'agent_drafts',
            'artefact': {'kind': 'research_note', 'label': f'a 1-page decision memo on {ent.get("label")}: what the research found in the box, the go, hold or kill, and the reason logged'},
            'steps': [
                {'n': 1, 'who': 'agent', 'text': 'Pull the candidate\'s log, hours and check results. Name what the time box answered and what it did not.'},
                {'n': 2, 'who': 'agent', 'text': 'Draft the memo: go to the next stage (with the one open question and a new box), or kill (with the reason so it is not re-argued).'},
                {'n': 3, 'who': 'person', 'text': 'Decide from the card: advance or kill. The choice writes to the pipeline and the decisions log.'}],
            'size': {'text': f'{_ev_value(f, "research_hours_logged") or 0} hours logged', 'usd': None},
            'stop_rule': 'no new box without a named open question', 'check_on': _check_on(f, 3), 'time_to_ship_hours': 1,
            'win_rule': 'the candidate has a stage change or a kill logged',
        }
    if rid == 'PROD-R15':
        ent = f.get('entity') or {}
        failed = ', '.join(c.replace('_', ' ') for c in (ent.get('failed') or []))
        return {
            'title': f'Kill {ent.get("label")} or fix the failed checks: {failed}',
            'owner': 'agent',
            'artefact': {'kind': 'research_note', 'label': f'the fast-check record for {ent.get("label")}: each failed check with its number, and the kill or the one change that would flip it'},
            'steps': [
                {'n': 1, 'who': 'agent', 'text': f'Re-read the failed checks ({failed}) with the numbers behind them: sellers counted, lines it would sit beside, the demand signal.'},
                {'n': 2, 'who': 'agent', 'text': 'Write the kill with the reason, or the one change (price, angle, channel) that would pass the checks.'},
                {'n': 3, 'who': 'person', 'text': 'Confirm the kill from the card, or reset the checks with the change and a new time box.'}],
            'size': {'text': f'{len(ent.get("failed") or [])} of 3 checks failed', 'usd': None},
            'stop_rule': 'a killed candidate stays killed for 90 days', 'check_on': _check_on(f, 3), 'time_to_ship_hours': 1,
            'win_rule': 'the candidate is killed or passes 2 of 3 checks',
        }
    if rid == 'PROD-R16':
        ent = f.get('entity') or {}
        gap = (ent.get('floor_pct') or 0) - (ent.get('margin_pct') or 0)
        price = ent.get('price') or 0
        need = round(price * gap / 100, 2)
        return {
            'title': f'Close a {gap:g}-point margin gap on {ent.get("label")}: price, cost or channel',
            'owner': 'agent',
            'artefact': {'kind': 'price_change', 'label': f'the 3 ways to pass the gate for {ent.get("label")}: the price that passes at today\'s cost (about ${need:g} more a unit), the landed cost that passes at today\'s price, or a pack that spreads the per-order cost; with the recommendation'},
            'steps': [
                {'n': 1, 'who': 'agent', 'text': 'Re-run the gate with each lever alone: price up, landed cost down (a quote or a spec change), a bigger pack.'},
                {'n': 2, 'who': 'agent', 'text': ('The landed cost is an estimate from the category median; ask sourcing for a quote before deciding.' if ent.get('estimated_cogs') else 'Check the entered landed cost against the latest quote.')},
                {'n': 3, 'who': 'agent', 'text': 'Write the recommendation with the number each lever moves and the one the buyer will accept (review price signal, competitor band).'},
                {'n': 4, 'who': 'person', 'text': 'Pick the lever or kill the candidate. The candidate\'s price or cost is updated from the card.'}],
            'size': {'text': (f'{ent.get("margin_pct"):g} percent modelled against a {ent.get("floor_pct"):g} percent floor' if ent.get('margin_pct') is not None and ent.get('floor_pct') is not None else 'margin gap unavailable'), 'usd': None},
            'stop_rule': 'no sourcing spend until the modelled margin passes the floor', 'check_on': _check_on(f, 7), 'time_to_ship_hours': 2,
            'win_rule': 'modelled contribution margin at or above the brand floor',
        }
    if rid == 'PROD-R18':
        ent = f.get('entity') or {}
        peak = ' and '.join(ent.get('peak_months') or []) or 'the peak months'
        draft = (f'Cash plan for {ent.get("label")}\n'
                 f'Peak: months {peak}. {ent.get("cash_timing") or ""}\n'
                 f'Order by: lead time back from month {min(ent.get("peak_months") or ["11"])}. Lead time: unavailable, no operations record holds it; ask supply.\n'
                 f'Cash out: units ordered x landed cost, paid before the peak. Cash in: sales in the peak months.\n'
                 f'First run: size it at the share a new SKU takes of the category in its first season, from the products table when connected.')
        return {
            'title': f'Attach a cash plan to {ent.get("label")} for its {peak} peak',
            'owner': 'agent_drafts',
            'artefact': {'kind': 'research_note', 'label': f'a cash plan for {ent.get("label")}: order-by date, units, cash out and cash in by month', 'draft': draft},
            'steps': [
                {'n': 1, 'who': 'agent', 'text': 'Read the category\'s 12-month series and name the peak months and their share.'},
                {'n': 2, 'who': 'agent', 'text': 'Ask supply for the lead time (no operations record holds it) and set the order-by month.'},
                {'n': 3, 'who': 'agent', 'text': 'Size the first run from the landed cost and the category\'s first-season share; write cash out and cash in by month.'},
                {'n': 4, 'who': 'person', 'text': 'Approve the plan. It is attached to the candidate from the card and the finding resolves.'}],
            'size': {'text': f'{round((_ev_value(f, "top2_month_share") or 0) * 100)} percent of the category\'s units land in 2 months', 'usd': None},
            'stop_rule': 'no shortlist without a cash plan', 'check_on': _check_on(f, 7), 'time_to_ship_hours': 2,
            'win_rule': 'a cash plan attached to the candidate',
        }
    if rid == 'PROD-R19':
        ent = f.get('entity') or {}
        label = (ent.get('label') or '').lower()
        return {
            'title': f'Find the room in {label}: {ent.get("sellers")} sellers, so only a named angle gets in',
            'owner': 'agent',
            'artefact': {'kind': 'research_note', 'label': f'a room read on {label}: the {ent.get("sellers")} sellers by price and claim, the angle none of them owns, and go or no-go on a candidate'},
            'steps': [
                {'n': 1, 'who': 'agent', 'text': f'List the {ent.get("sellers")} sellers (pages advertising plus launches) with their price band and lead claim, from the brain and the web pass.'},
                {'n': 2, 'who': 'agent', 'text': 'Name the angle none of them owns, from the review complaints and Reddit language on the lane.'},
                {'n': 3, 'who': 'agent', 'text': 'Write go (screen a candidate with that angle) or no-go (crowded, no owned angle) with the numbers.'},
                {'n': 4, 'who': 'person', 'text': 'Decide. A go screens the candidate in from the desk.'}],
            'size': {'text': f'trend score {ent.get("trend")}, {ent.get("sellers")} sellers', 'usd': None},
            'stop_rule': 'no candidate on the lane without an angle no seller owns', 'check_on': _check_on(f, 14), 'time_to_ship_hours': 3,
            'win_rule': 'a logged go with an angle, or a logged no-go',
        }
    if rid == 'PROD-R20':
        ent = f.get('entity') or {}
        label = (ent.get('label') or '').lower()
        n = _ev_value(f, 'ad_library_spend_signal')
        return {
            'title': f'Screen a {label} candidate: {n} advertisers have funded it for 90 days or more',
            'owner': 'agent',
            'artefact': {'kind': 'research_note', 'label': f'a fast screen for a {label} candidate: what {ent.get("names")} sell on it (price, claim, format), the angle open to us, demand and store fit, with a go or kill'},
            'steps': [
                {'n': 1, 'who': 'agent', 'text': f'Read the long-running ads of {ent.get("names")} on {label} by page id: product, price, claim, format. Signals only; nothing copied.'},
                {'n': 2, 'who': 'agent', 'text': 'Run the 3 fast checks (demand, competition, store fit) with the numbers and name the angle none of them owns.'},
                {'n': 3, 'who': 'agent', 'text': 'Screen the candidate into the pipeline with a 10-day box, or log the kill.'},
                {'n': 4, 'who': 'person', 'text': 'Confirm from the pipeline card.'}],
            'size': {'text': f'{n} advertisers at 90+ days, longest {_ev_value(f, "longest_run_days")} days', 'usd': None},
            'stop_rule': 'a run length is a funded test, never proof of profit: the margin gate still decides', 'check_on': _check_on(f, 10), 'time_to_ship_hours': 3,
            'win_rule': 'an open candidate on the lane, or a logged kill',
        }
    if rid == 'PROD-R21':
        ent = f.get('entity') or {}
        return {
            'title': (f'Recheck the price of {ent.get("label")}: reviewers say ${ent.get("review_median"):g} a pair, the plan says ${ent.get("planned_per_pair"):g}'
                      if ent.get('review_median') is not None and ent.get('planned_per_pair') is not None else f'Recheck the price of {ent.get("label")} against the review signal'),
            'owner': 'agent',
            'artefact': {'kind': 'research_note', 'label': f'a price read for {ent.get("label")}: what reviewers say a pair is worth by source and star, the competitor band, our own per-pair ladder, and the price or the proof that closes the gap'},
            'steps': [
                {'n': 1, 'who': 'agent', 'text': 'Split the price mentions by star: what 1-star buyers say they paid against what 5-star buyers say it is worth.'},
                {'n': 2, 'who': 'agent', 'text': 'Put the planned price beside the competitor band and our own per-pair ladder.'},
                {'n': 3, 'who': 'agent', 'text': 'Write the two ways to close the gap: a lower price that still passes the margin gate, or the proof that earns the premium (wear life, guarantee).'},
                {'n': 4, 'who': 'person', 'text': 'Pick one and update the candidate\'s planned price or angle from the card.'}],
            'size': {'text': f'{round((ent.get("gap") or 0) * 100)} percent above what reviewers say', 'usd': None},
            'stop_rule': 'no funding while the plan sits more than 15 percent above the review signal without a named proof', 'check_on': _check_on(f, 7), 'time_to_ship_hours': 2,
            'win_rule': 'planned price within 15 percent of the review median, or a proof the founder approved for the premium',
        }
    if rid == 'PROD-R22':
        ent = f.get('entity') or {}
        th = audit.THEME_LABEL.get(ent.get('complaint'), ent.get('complaint') or 'the complaint').lower()
        return {
            'title': f'Build the angle on {th}: {round((ent.get("rate") or 0) * 100)} percent of mined reviews on {ent.get("asin")} say it',
            'owner': 'agent',
            'artefact': {'kind': 'brain_record', 'label': f'an angle record for the brain: the complaint in the buyer\'s words, the product change or proof that answers it, and the listing line that says so ({ent.get("asin")})'},
            'steps': [
                {'n': 1, 'who': 'agent', 'text': f'Read the mined complaint quotes on {ent.get("asin")} for {th} and sort them: product (spec), listing (wrong expectation), fulfilment (the seller).'},
                {'n': 2, 'who': 'agent', 'text': 'Write the angle: what the next SKU or the listing must say to remove the complaint, with the proof.'},
                {'n': 3, 'who': 'agent', 'text': 'Propose the record to the brain (review queue) and, if the fix is the listing, a listing fix for the marketplaces desk.'},
                {'n': 4, 'who': 'person', 'text': 'Accept the record. Creative, copy and marketplaces read it from the brain.'}],
            'size': {'text': f'{round((ent.get("rate") or 0) * 100)} percent of mined reviews', 'usd': None},
            'stop_rule': 'stop if the complaint share falls under 15 percent in the next review pull', 'check_on': _check_on(f, 30), 'time_to_ship_hours': 3,
            'win_rule': 'an accepted angle record in the brain and the complaint share under 15 percent on the next pull',
        }
    if rid == 'PROD-R23':
        ent = f.get('entity') or {}
        return {
            'title': f'Write the point of difference for {ent.get("label")} before it goes further',
            'owner': 'agent',
            'artefact': {'kind': 'research_note', 'label': f'an angle for {ent.get("label")}: the difference in the buyer\'s words, the source it rests on (a review gap, a teardown, field research), and the check that it is not a competitor\'s claim'},
            'steps': [
                {'n': 1, 'who': 'agent', 'text': 'Read the review complaints and Reddit language on the candidate\'s lane for the unmet ask.'},
                {'n': 2, 'who': 'agent', 'text': 'Draft the angle in one line with its source named, and check its words against every competitor pitch in the brain.'},
                {'n': 3, 'who': 'person', 'text': 'Approve the angle from the card. It is written to the candidate and the gates re-run.'}],
            'size': {'text': f'angle confidence 0 of 3 at {ent.get("stage")}', 'usd': None},
            'stop_rule': 'no funding gate without an angle', 'check_on': _check_on(f, 5), 'time_to_ship_hours': 2,
            'win_rule': 'angle confidence 2 or more',
        }
    if rid == 'PROD-R24':
        ent = f.get('entity') or {}
        return {
            'title': f'Run the compliance check on {ent.get("label")}: {ent.get("passed")} of {ent.get("of")} gates passed',
            'owner': 'agent_drafts',
            'artefact': {'kind': 'ticket', 'label': f'a compliance checklist for {ent.get("label")}: labelling (fibre content, country of origin, care), category certification if any, with pass or fail per line and the source'},
            'steps': [
                {'n': 1, 'who': 'agent', 'text': 'Fill the checklist from the candidate\'s spec: fibre content and country of origin labels, care labels, any category certification.'},
                {'n': 2, 'who': 'agent', 'text': 'Mark each line pass, fail or needs a document, with the rule it rests on.'},
                {'n': 3, 'who': 'person', 'text': 'Confirm the lines and set compliance on the candidate from the card.'}],
            'size': {'text': f'{ent.get("passed")} of {ent.get("of")} gates passed, compliance not run', 'usd': None},
            'stop_rule': 'not fundable until both compliance lines pass', 'check_on': _check_on(f, 7), 'time_to_ship_hours': 2,
            'win_rule': 'labelling and category certification both pass',
        }
    if rid == 'PROD-R25':
        ent = f.get('entity') or {}
        return {
            'title': (f'Decide on {ent.get("label")}: the review date has arrived, it scores {ent.get("total"):g} ({str(ent.get("verdict") or "").replace("_", " ")})'
                      if ent.get('total') is not None else f'Decide on {ent.get("label")}: the review date has arrived'),
            'owner': 'agent_drafts',
            'artefact': {'kind': 'research_note', 'label': f'the go or no-go memo for {ent.get("label")} with the scorecard, the gates and the decision line', 'draft': ent.get('memo')},
            'steps': [
                {'n': 1, 'who': 'agent', 'text': 'Refresh the scorecard and the gates for the candidate; the memo above is the draft.'},
                {'n': 2, 'who': 'person', 'text': 'Decide go, hold or kill. Go moves it to sourcing; hold sets a new review date and names the open question; kill logs the reason.'},
                {'n': 3, 'who': 'agent', 'text': 'Write the decision to the pipeline and the decisions log so it is not re-argued.'}],
            'size': {'text': (f'{ent.get("total"):g} of 100 on the scorecard' if ent.get('total') is not None else 'score unavailable'), 'usd': None},
            'stop_rule': 'a hold without a new review date is a kill', 'check_on': _check_on(f, 1), 'time_to_ship_hours': 1,
            'win_rule': 'a logged go, hold with a new date, or kill',
        }
    return None


def merge_lanes(actions):
    """One action per lane: a PROD-R05 market finding and a PROD-R06 competitor finding on the same lane share the brief."""
    r06 = [a for a in actions if a.get('rule_id') == 'PROD-R06']
    keep = []
    for a in actions:
        if a.get('rule_id') not in ('PROD-R05', 'PROD-R20'):
            keep.append(a)
            continue
        key = (a.get('entity') or {}).get('id') or ''
        if a.get('rule_id') == 'PROD-R20':
            host = next((b for b in r06 if (b.get('entity') or {}).get('id') == key), None)
        else:
            words = set(audit.MARKET_WORDS.get(key, []))
            host = next((b for b in r06 if words & set(next((t for k, _, t in audit.SUBCATS if k == (b.get('entity') or {}).get('id')), []))), None)
        if host is None:
            keep.append(a)
            continue
        host['finding_ids'] = sorted(set(host['finding_ids']) | set(a['finding_ids']))
        host['why'] = host['why'] + ' ' + a['why']
        host['brain_refs'] = sorted(set(host.get('brain_refs') or []) | set(a.get('brain_refs') or []))
        host['rubric']['confidence'] = max(host['rubric'].get('confidence') or 0, a['rubric'].get('confidence') or 0)
    return keep


def rank_mod_money(m):
    usd = (m or {}).get('usd')
    return f'${usd:,.0f}' if isinstance(usd, (int, float)) else 'stake unavailable'


# Rubric overrides the audit docstring declares per rule (depth.md section 4: a screen may raise reputation or
# satisfaction for a specific rule; it may not change the weights).
RUBRIC_OVERRIDES = {'PROD-R07': {'reputation': 4}, 'PROD-R09': {'reputation': 5}, 'PROD-R11': {'satisfaction': 4}}


def rescore(a, f, nr):
    """The rubric from the finding, the ease from the owner the recipe set, the overrides from the audit, the total recomputed."""
    r = rank_mod.score(f, nr)
    r['ease'] = {'agent': 5, 'agent_drafts': 4, 'person': 3}[a['owner']] if f.get('status') != 'unavailable' else 1
    for k, v in RUBRIC_OVERRIDES.get(f.get('rule_id'), {}).items():
        r[k] = max(r[k] if r[k] is not None else 0, v)
    r['total'] = round(sum(rank_mod.WEIGHTS[k] * (r[k] if r[k] is not None else 2.5) / 5 for k in rank_mod.WEIGHTS), 1)
    return r


def rank(brand, window=None):
    """Depth contract section 5: every audit finding becomes an action with an owner, steps and an artefact."""
    window = window or rank_mod.default_window()
    nr = rank_mod.net_revenue_28d(brand, window)
    findings = audit.run(brand, window)
    actions = []
    for f in findings:
        if f.get('status') not in ('open', 'unavailable', None):
            continue
        a = rank_mod.action_from_finding(f, nr)
        r = recipe(f) if f.get('status') != 'unavailable' else None
        if f.get('status') == 'unavailable' and f.get('rule_id') == 'PROD-R17':
            a['title'] = 'Connect the store so actual margin by SKU can be read against the gate model'
            a['steps'] = [{'n': 1, 'who': 'person', 'text': 'In Setup, connect the store (read only) so orders and order lines load.'},
                          {'n': 2, 'who': 'agent', 'text': 'Join order lines to the landed costs on file and compute contribution margin by SKU for the window.'},
                          {'n': 3, 'who': 'agent', 'text': 'Compare each launched SKU\'s actual margin with its gate model and report any 5-point shortfall here.'}]
        if f.get('status') == 'unavailable' and f.get('rule_id') == 'PROD-R12':
            a['title'] = 'Connect Search Console so search demand for the brand and the category can be read'
            a['steps'] = [{'n': 1, 'who': 'person', 'text': 'In Setup, add a read-only Search Console credential for the brand\'s property.'},
                          {'n': 2, 'who': 'agent', 'text': 'Pull 16 months of query, page, clicks, impressions and position into search_console.'},
                          {'n': 3, 'who': 'agent', 'text': 'Run PROD-R13 on the brand, category, competitor and problem term groups and report the gaps here.'}]
        if r:
            a.update({k: v for k, v in r.items() if v is not None})
        a['rubric'] = rescore(a, f, nr)
        a['screen'] = SCREEN
        if not rank_mod.validate_action(a):
            actions.append(a)
    actions = merge_lanes(actions)
    actions.sort(key=rank_mod.sort_key)
    return {'screen': SCREEN, 'brand': brand, 'window': window, 'actions': actions, 'net_revenue_28d': nr}


# ---------------------------------------------------------------- overview

BEHIND_RULES = {'PROD-R09': 'positioning', 'PROD-R08': 'positioning', 'PROD-R06': 'positioning', 'PROD-R10': 'avatar', 'PROD-R11': 'avatar', 'PROD-R07': 'avatar'}


def falling_behind(findings, cov, prefs, mp, net_28d_value):
    """Section 9: every positioning and avatar gap the audit found, ranked by money at stake, then reach, then severity.
    Reach is the share of buyers for an avatar, the competitor pages or upvotes for a positioning gap."""
    rows = []
    share_by = {r['key']: r for r in (cov or {}).get('rows') or []}
    for f in findings:
        kind = BEHIND_RULES.get(f['rule_id'])
        if not kind or f['status'] != 'open':
            continue
        ent = f.get('entity') or {}
        m = f.get('money_at_stake') or {}
        usd = m.get('usd') if isinstance(m.get('usd'), (int, float)) else None
        reach, reach_n = None, None
        if f['rule_id'] in ('PROD-R10', 'PROD-R11'):
            av = share_by.get(ent.get('id')) or {}
            if av.get('share') is not None:
                reach, reach_n = f'{round(av["share"] * 100)} percent of buyers', av['share']
            elif av.get('served_by'):
                reach, reach_n = f'{len(av["served_by"])} competitor pages pitch to them', len(av['served_by']) / 100
        elif f['rule_id'] == 'PROD-R09':
            up = next((e.get('upvotes') for e in f['evidence'] if e.get('metric') == 'recommended_instead'), None)
            n = next((e.get('value') for e in f['evidence'] if e.get('metric') == 'frame_mentions'), None)
            reach, reach_n = (f'{n} Reddit posts, {up} upvotes on the recommendation instead' if n is not None else None), (up or 0) / 10000
        elif f['rule_id'] == 'PROD-R06':
            n = next((e.get('value') for e in f['evidence'] if e.get('metric') == 'competitor_active_ads'), None)
            k = next((e.get('value') for e in f['evidence'] if e.get('metric') == 'competitors_pushing'), None)
            reach, reach_n = (f'{k} competitor pages, {n} active ads' if n is not None else None), (n or 0) / 10000
        elif f['rule_id'] == 'PROD-R08':
            k = next((e.get('value') for e in f['evidence'] if e.get('metric') == 'competitors_claiming_it'), None)
            reach, reach_n = (f'{k} competitor pages claim it' if k is not None else None), (k or 0) / 100
        elif f['rule_id'] == 'PROD-R07':
            c = next((e.get('value') for e in f['evidence'] if e.get('metric') == 'complaint_quotes'), None)
            reach, reach_n = (f'{c} complaint quotes' if c is not None else None), (c or 0) / 1000
        rows.append({'finding_id': f['id'], 'rule_id': f['rule_id'], 'kind': kind, 'label': ent.get('label') or ent.get('id'), 'sentence': f['sentence'],
                     'severity': f['severity'], 'confidence': f['confidence'], 'usd': usd, 'formula': m.get('formula'), 'money_reason': f.get('money_reason'),
                     'reach': reach, 'reach_n': reach_n, 'capability': f['capability']['id'], 'autonomy': f['capability']['autonomy']})
    order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
    rows.sort(key=lambda r: (0 if r['usd'] is not None else 1, -(r['usd'] or 0), -(r['reach_n'] or 0), order.get(r['severity'], 9), r['finding_id']))
    stake = [r['usd'] for r in rows if r['usd'] is not None]
    return {'rows': rows, 'stake_usd': sum(stake) if stake else None, 'stake_share_of_net_28d': (sum(stake) / net_28d_value) if stake and net_28d_value else None,
            'counts': {'positioning': sum(1 for r in rows if r['kind'] == 'positioning'), 'avatar': sum(1 for r in rows if r['kind'] == 'avatar')},
            'quadrant': next((q for q, members in ((mp or {}).get('members') or {}).items() if (mp or {}).get('ours', {}).get('label') in members), None),
            'prove': [p['label'] for p in prefs or [] if p.get('verdict') == 'prove']}


def avatar_block(br, findings):
    cov = audit.avatar_coverage(br)
    by_entity = {}
    for f in findings:
        if f['rule_id'] in ('PROD-R10', 'PROD-R11'):
            by_entity[f['entity']['id']] = f['id']
    for r in cov['rows']:
        r['finding_id'] = by_entity.get(r['key'])
    return cov


def head(data, brand, ends_on, br):
    b = source_of(data, brand).brand
    return {'brand': b.get('brand'), 'name': b.get('name'), 'as_of': b.get('as_of'),
            'simulated': bool(b.get('simulated') or b.get('fictional')), 'market': b.get('market'),
            'brain_version': br.version() if br else None,
            'simulated_note': (f'{b.get("name") or "This brand"} is the sample brand. Sales, units and list prices are simulated from a public profile. '
                               'Review counts, ratings, ads seen and competitor prices are public records in the brand brain.')}


def wrong(findings):
    """Section 2: open and unavailable findings grouped by rule, severity first, each with its evidence numbers."""
    order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
    groups = {}
    for f in findings:
        if f['status'] not in ('open', 'unavailable'):
            continue
        g = groups.setdefault(f['rule_id'], {'rule_id': f['rule_id'], 'name': next((r['name'] for r in audit.RULES if r['rule_id'] == f['rule_id']), f['rule_id']),
                                              'severity': f['severity'], 'findings': []})
        if order.get(f['severity'], 9) < order.get(g['severity'], 9):
            g['severity'] = f['severity']
        g['findings'].append({'id': f['id'], 'severity': f['severity'], 'status': f['status'], 'sentence': f['sentence'],
                              'confidence': f['confidence'], 'entity': f['entity'], 'money_at_stake': f.get('money_at_stake'),
                              'money_reason': f.get('money_reason'), 'unavailable': f.get('unavailable'),
                              'evidence': [{'metric': e['metric'], 'value': e['value'], 'unit': e['unit'], 'baseline': e.get('baseline'),
                                            'baseline_kind': e.get('baseline_kind'), 'window': e['window'], 'simulated': e.get('simulated')}
                                           for e in f['evidence'][:4]]})
    return sorted(groups.values(), key=lambda g: (order.get(g['severity'], 9), g['rule_id']))


def overview(data, brand):
    ends_on = audit.last_full_day(data, brand)
    rd = audit.Reader(data, brand, ends_on)
    br = audit.brain(brand, today=ends_on) if brand else None
    tr = audit.trend(rd)
    reviews = audit.review_lines(br)
    lads = audit.ladders(br)
    bands = price_bands(products(data, brand), competitor_bands(br))
    pipe = audit.pipeline(brand)
    floor = finance_floor(data, brand, ends_on)
    findings = audit.run(brand, {'ends_on': ends_on.isoformat()}, data=data)
    mix = audit.category_mix(data, brand, rd)
    cov = avatar_block(br, findings)
    prefs = audit.preferences(br)
    mp = dict(audit.positioning_map(br, products(data, brand)), frames=audit.reddit_frames(br)[0], instead=audit.reddit_frames(br)[1])
    return {'brand': head(data, brand, ends_on, br),
            'window': {'ends_on': ends_on.isoformat(), 'days': 28,
                       'trend': None if tr.get('unavailable') else {'months': [tr['first'], tr['last']], 'year_ago': tr['year_ago']}},
            'orientation': orientation(tr, br, ends_on, findings),
            'wrong': wrong(findings),
            'desk': {'trends': trends(br, mix), 'mix': mix, 'lanes': audit.subcategory_table(br, ends_on),
                     'conversation': audit.conversation(br), 'preferences': prefs, 'map': mp, 'avatars': cov,
                     'search': audit.search_table(br, data, brand, ends_on),
                     'behind': falling_behind(findings, cov, prefs, mp, audit.net_28d(rd)),
                     'demand': demand(tr, reviews), 'store_growth': tr.get('store_growth'),
                     'demand_unavailable': {'reason': tr.get('reason'), 'fix': tr.get('fix')} if tr.get('unavailable') else None,
                     'price_bands': bands, 'reviews': review_mining(reviews, lads),
                     'pipeline': pipeline_block(brand, ends_on, findings, floor), 'margin': margin_block(brand, data, br, rd, ends_on, findings),
                     'pattern': pattern_block(brand, data, rd, findings), 'lane_map': audit.lane_map(br, ends_on), 'spend': audit.spend_signal(br, brand, ends_on),
                     'price_signal': price_signal_block(br, brand, data, findings), 'complaints': audit.listing_complaints(br),
                     'gates': gates_block(brand, data, br, rd, ends_on, findings), 'scorecard': scorecard_block(brand, data, br, rd, ends_on, findings)},
            'audit': {'findings': findings, 'rules': audit.RULES}}


# ---------------------------------------------------------------- the pipeline: the one thing this screen writes

CANDIDATE_FIELDS = ('name', 'category', 'stage', 'time_box_days', 'hours_logged', 'angle_text', 'angle_source', 'planned_price', 'cogs_estimate',
                    'pack_units', 'cash_plan', 'compliance', 'review_date', 'screen_result', 'source_finding')


def _pipeline_doc():
    if audit.PIPELINE_PATH.is_file():
        doc = json.loads(audit.PIPELINE_PATH.read_text(encoding='utf-8'))
        if isinstance(doc, list):
            doc = {'rows': doc}
    else:
        doc = {'note': 'The candidate pipeline for the research desk, written by this screen\'s api.', 'rows': []}
    doc.setdefault('rows', [])
    return doc


def _write_pipeline(doc):
    audit.PIPELINE_PATH.parent.mkdir(parents=True, exist_ok=True)
    audit.PIPELINE_PATH.write_text(json.dumps(doc, indent=1), encoding='utf-8')


def _num(v, lo=0.0):
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    return x if x >= lo else None


def candidate_add(brand, body, today):
    body = body or {}
    name = str(body.get('name') or '').strip()[:120]
    if not name:
        return 400, {'error': 'name is empty'}
    doc = _pipeline_doc()
    n = 1 + max([int(str(r.get('candidate_id', 'cand-0')).split('-')[-1]) for r in doc['rows'] if str(r.get('candidate_id', '')).startswith('cand-')] or [0])
    row = {'candidate_id': f'cand-{n:03d}', 'brand': brand, 'name': name, 'category': str(body.get('category') or 'socks')[:40], 'stage': 'screened',
           'screen_result': {k: (body.get('screen_result') or {}).get(k) if (body.get('screen_result') or {}).get(k) in ('pass', 'fail') else None for k in audit.SCREEN_CHECKS},
           'time_box_days': int(_num(body.get('time_box_days'), 1) or 10), 'hours_logged': _num(body.get('hours_logged')) or 0.0,
           'angle_text': (str(body.get('angle_text') or '').strip()[:300] or None), 'angle_source': (str(body.get('angle_source') or '').strip()[:300] or None),
           'screen_in_date': today.isoformat(), 'planned_price': _num(body.get('planned_price')), 'cogs_estimate': _num(body.get('cogs_estimate')),
           'pack_units': int(_num(body.get('pack_units'), 1) or 1),
           'cash_plan': (str(body.get('cash_plan') or '').strip()[:300] or None), 'compliance': {'labelling': None, 'category_certification': None},
           'review_date': None, 'source_finding': (str(body.get('source_finding') or '').strip()[:120] or None), 'simulated': True,
           'log': [{'on': today.isoformat(), 'who': str(body.get('who') or 'person')[:20], 'what': 'screened in from the research desk'}]}
    doc['rows'].append(row)
    _write_pipeline(doc)
    return 201, {'ok': True, 'candidate': row}


def candidate_update(brand, cid, body, today):
    body = body or {}
    doc = _pipeline_doc()
    row = next((r for r in doc['rows'] if r.get('candidate_id') == cid and r.get('brand') in (None, brand)), None)
    if row is None:
        return 404, {'error': 'no such candidate', 'candidate_id': cid}
    changes = []
    if body.get('stage') is not None:
        st = str(body['stage'])
        if st not in audit.STAGES + ['killed']:
            return 400, {'error': 'stage must be one of ' + ', '.join(audit.STAGES + ['killed'])}
        if st != row.get('stage'):
            changes.append(f'{row.get("stage")} to {st}')
            row['stage'] = st
            if st == 'shortlisted' and not row.get('review_date'):
                row['review_date'] = (today + dt.timedelta(days=14)).isoformat()
    if body.get('hours_add') is not None:
        h = _num(body['hours_add'])
        if h is None:
            return 400, {'error': 'hours_add must be a number'}
        row['hours_logged'] = round((row.get('hours_logged') or 0) + h, 2)
        changes.append(f'{h:g} hours logged')
    for k in ('angle_text', 'angle_source', 'cash_plan', 'source_finding'):
        if body.get(k) is not None:
            row[k] = str(body[k]).strip()[:300] or None
            changes.append(k.replace('_', ' ') + ' set')
    for k in ('planned_price', 'cogs_estimate'):
        if body.get(k) is not None:
            row[k] = _num(body[k])
            changes.append(k.replace('_', ' ') + ' set')
    if body.get('pack_units') is not None:
        row['pack_units'] = int(_num(body['pack_units'], 1) or 1)
        changes.append('pack units set')
    if body.get('time_box_days') is not None:
        row['time_box_days'] = int(_num(body['time_box_days'], 1) or row.get('time_box_days') or 10)
        row['screen_in_date'] = today.isoformat()
        changes.append(f'new box of {row["time_box_days"]} days')
    if isinstance(body.get('screen_result'), dict):
        row['screen_result'] = {k: body['screen_result'].get(k) if body['screen_result'].get(k) in ('pass', 'fail') else (row.get('screen_result') or {}).get(k) for k in audit.SCREEN_CHECKS}
        changes.append('checks set')
    if isinstance(body.get('compliance'), dict):
        row['compliance'] = dict(row.get('compliance') or {}, **{k: v for k, v in body['compliance'].items() if v in ('pass', 'fail', None)})
        changes.append('compliance set')
    if body.get('review_date') is not None:
        row['review_date'] = str(body['review_date'])[:10] or None
        changes.append('review date set')
    if not changes:
        return 400, {'error': 'nothing to change'}
    row.setdefault('log', []).append({'on': today.isoformat(), 'who': str(body.get('who') or 'person')[:20], 'what': '; '.join(changes)})
    _write_pipeline(doc)
    return {'ok': True, 'candidate': row, 'changes': changes}


def margin_block(brand, data, br, rd, ends_on, findings):
    fin_rows = audit.finance_rows(data, brand)
    fin = audit.metrics().finance.Finance(fin_rows) if fin_rows else None
    floor = fin.value('target_contribution_margin', ends_on.isoformat()) if fin else None
    upo = audit.units_per_order(data, brand, rd)
    by_entity = {f['entity']['id']: f['id'] for f in findings if f['rule_id'] == 'PROD-R16'}
    rows = []
    for c in audit.pipeline(brand):
        g = audit.margin_gate(c, fin, br, ends_on.isoformat(), upo, floor)
        rows.append({'candidate_id': c.get('candidate_id'), 'name': c.get('name'), 'stage': c.get('stage'), 'closed': c.get('stage') in audit.CLOSED_STAGES,
                     'price': c.get('planned_price'), 'pack_units': c.get('pack_units') or 1, 'gate': g, 'finding_id': by_entity.get(c.get('candidate_id'))})
    actual = next((f for f in findings if f['rule_id'] == 'PROD-R17'), None)
    return {'rows': rows, 'floor_pct': floor, 'floor_source': 'finance_inputs.target_contribution_margin' if floor is not None else None,
            'units_per_order': upo, 'actual_unavailable': actual['id'] if actual else None,
            'formula': '(price - landed cost - donated item - fulfilment - payment fee) / price',
            'bank_rule': f'bank idea PRD-079: at least ${audit.BANK_DOLLAR_FLOOR:g} contribution a unit and {audit.BANK_MULTIPLE:g} times landed cost, shown as a reference, not the gate'}


def pattern_block(brand, data, rd, findings):
    mix = audit.category_mix(data, brand, rd)
    fx = audit.market_trends()
    by_entity = {f['entity']['id']: f['id'] for f in findings if f['rule_id'] == 'PROD-R18'}
    cats = [dict(audit.demand_pattern(r['category'], mix, fx), kind='category') for r in (mix.get('rows') or [])] if not mix.get('unavailable') else []
    cands = []
    for c in audit.pipeline(brand):
        p = audit.demand_pattern(c.get('category'), mix, fx, c.get('name'))
        cands.append(dict(p, kind='candidate', candidate_id=c.get('candidate_id'), name=c.get('name'), stage=c.get('stage'), closed=c.get('stage') in audit.CLOSED_STAGES,
                          cash_plan=c.get('cash_plan'), finding_id=by_entity.get(c.get('candidate_id'))))
    return {'categories': cats, 'candidates': cands, 'unavailable': mix.get('reason') if mix.get('unavailable') else None,
            'rule': f'seasonal when the top 2 months carry {round(audit.SEASONAL_TOP2_SHARE * 100)} percent or more of 12-month units (an even year is 17) or the name says gift; trending at {audit.TRENDING_CAGR:g} percent market growth a year or {audit.TRENDING_LAUNCHES} launches in 24 months; else evergreen',
            'months': mix.get('months')}


def price_signal_block(br, brand, data, findings):
    sig = audit.review_price_signal(br)
    comps = competitor_bands(br)
    meds = [c['median'] for c in comps if c['median'] is not None]
    ours = audit.our_price_per_pair(products(data, brand), br)
    by_entity = {f['entity']['id']: f['id'] for f in findings if f['rule_id'] == 'PROD-R21'}
    cands = []
    for c in audit.pipeline(brand):
        per = (c['planned_price'] / (c.get('pack_units') or 1)) if isinstance(c.get('planned_price'), (int, float)) else None
        cands.append({'candidate_id': c.get('candidate_id'), 'name': c.get('name'), 'category': c.get('category'), 'closed': c.get('stage') in audit.CLOSED_STAGES, 'per_pair': round(per, 2) if per else None,
                      'gap': round(per / sig['median_per_pair'] - 1, 4) if per and sig.get('median_per_pair') else None, 'finding_id': by_entity.get(c.get('candidate_id'))})
    return dict(sig, competitor_band=[min(meds), max(meds)] if meds else None, ours=ours, candidates=cands, gap_rule=audit.REVIEW_PRICE_GAP)


def gates_block(brand, data, br, rd, ends_on, findings):
    rows = audit.candidate_gates(brand, data, br, rd, ends_on)
    by_entity = {}
    for f in findings:
        if f['rule_id'] in ('PROD-R23', 'PROD-R24'):
            by_entity.setdefault(f['entity']['id'], []).append(f['id'])
    for r in rows:
        r['finding_ids'] = by_entity.get(r['candidate_id'], [])
    return {'rows': rows, 'gates': audit.GATES, 'labels': audit.GATE_LABEL,
            'rule': 'angle confidence: filled, names a source, not a competitor claim (3 shared words); gates: provable claim, owned difference, brand threshold (category in the lines and store fit), contribution margin (the gate above), ad-cost ceiling (contribution an order against target CAC)'}


def scorecard_block(brand, data, br, rd, ends_on, findings):
    sc = audit.scorecard(brand, data, br, rd, ends_on)
    by_entity = {f['entity']['id']: f['id'] for f in findings if f['rule_id'] == 'PROD-R25'}
    for r in sc['rows']:
        r['finding_id'] = by_entity.get(r['candidate_id'])
        r['memo'] = audit.memo_text(r, sc['weights'])
    return sc


def pipeline_block(brand, ends_on, findings, floor):
    rows = [audit.candidate_view(r, ends_on) for r in audit.pipeline(brand)]
    by_entity = {}
    for f in findings:
        if f['rule_id'] in ('PROD-R14', 'PROD-R15', 'PROD-R03'):
            by_entity.setdefault(f['entity']['id'], []).append(f['id'])
    for r in rows:
        r['finding_ids'] = by_entity.get(r.get('candidate_id'), [])
    open_rows = [r for r in rows if not r['closed']]
    return {'rows': rows, 'funnel': audit.pipeline_funnel(rows), 'stages': audit.STAGES, 'checks': list(audit.SCREEN_CHECKS),
            'open': len(open_rows), 'over_box': sum(1 for r in open_rows if r['over_box']), 'hours': round(sum(r.get('hours_logged') or 0 for r in rows), 1),
            'gate_rule': MARGIN_GATE, 'floor_pct': floor, 'floor_source': 'finance_inputs.target_contribution_margin' if floor is not None else None,
            'rule': f'a candidate fires when it passes its time box, or fails {audit.SCREEN_FAIL_AT} of the {len(audit.SCREEN_CHECKS)} fast checks'}


def _brand(req):
    brand = req.arg('brand', DEFAULT_BRAND)
    if brand in ('', 'sample'):
        return None
    if not re.fullmatch(r'[a-z0-9-]{1,40}', brand):
        raise ValueError('brand must be a folder name like bombas')
    return brand


def handle(req):
    try:
        brand = _brand(req)
        data = None if brand else req.data
        if brand:
            audit.brand_data(brand)  # ValueError for an unknown brand
        if req.method == 'POST':
            today = audit.last_full_day(data, brand) + dt.timedelta(days=1)
            if req.path == ['candidates']:
                return candidate_add(brand or 'sample', req.body, today)
            if len(req.path) == 2 and req.path[0] == 'candidates':
                return candidate_update(brand or 'sample', req.path[1], req.body, today)
            return 405, {'error': 'read only, except the candidate pipeline'}
        if req.path == ['overview']:
            return overview(data, brand)
        if req.path == ['findings']:
            return {'findings': audit.run(brand, None, data=data), 'rules': audit.RULES}
    except ValueError as exc:
        return 400, {'error': str(exc)}
    return 404, {'error': 'not found', 'routes': ['overview', 'findings', 'rank']}
