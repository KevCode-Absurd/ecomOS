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
DECISIONS_PATH = rank_mod.DECISIONS   # the shared decisions log the kit's decision row writes; tests point this elsewhere
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
    fx = audit.web_pass(br)
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
    if rid == 'PROD-R26':
        ent = f.get('entity') or {}
        label = (ent.get('label') or '').lower()
        other = {'reddit': 'an Instagram or TikTok keyword pull and the creator ads on the lane', 'instagram': 'Reddit threads and the creator ads on the lane', 'creator ads': 'Reddit threads and an Instagram or TikTok keyword pull'}.get(ent.get('platform'), 'a second platform')
        return {
            'title': f'Confirm {label} demand on a second platform before funding {", ".join((ent.get("candidates") or [])[:1]) or "the candidate"}',
            'owner': 'agent',
            'artefact': {'kind': 'research_note', 'label': f'a demand read on {label}: what each platform shows (posts, mentions, creators, run lengths) and whether it is one clip or a pattern'},
            'steps': [
                {'n': 1, 'who': 'agent', 'text': f'Read {other}; the keyword pull runs under the brand\'s Apify caps and stores no usernames.'},
                {'n': 2, 'who': 'agent', 'text': 'Count the independent sources above the floor and check the 180-day view, not the 30-day spike (bank idea PRD-018).'},
                {'n': 3, 'who': 'agent', 'text': 'Write pattern or single source with the numbers; a single source keeps the candidate at its stage with the demand check marked fail.'},
                {'n': 4, 'who': 'person', 'text': 'Confirm from the card.'}],
            'size': {'text': f'1 platform ({ent.get("platform")}) against 2 needed', 'usd': None},
            'stop_rule': 'no funding on one platform\'s demand', 'check_on': _check_on(f, 7), 'time_to_ship_hours': 2,
            'win_rule': '2 or more platforms above the floor, or the demand check set to fail',
        }
    if rid == 'PROD-R27':
        ent = f.get('entity') or {}
        missing = ', '.join(m.replace('_', ' ') for m in (ent.get('missing') or [])) or 'the spec'
        return {
            'title': f'Write the spec for {ent.get("label")} so sourcing can quote it: {missing}',
            'owner': 'agent',
            'artefact': {'kind': 'ticket', 'label': f'a versioned tech pack for {ent.get("label")}: tolerances, the bill of materials with fibre content, and the packaging cost line, ready for an RFQ'},
            'steps': [
                {'n': 1, 'who': 'agent', 'text': 'Draft the pack from the angle and the closest live SKU: construction, yarn and fibre content, sizes and tolerances.'},
                {'n': 2, 'who': 'agent', 'text': 'Fill the BOM lines and the packaging cost from the finance inputs (packaging per order) or a quote.'},
                {'n': 3, 'who': 'person', 'text': 'Review the lines and save the pack from the card as the current version. Sourcing sends the RFQ from it.'}],
            'size': {'text': f'{ent.get("version") or "no version"} at {ent.get("stage")}', 'usd': None},
            'stop_rule': 'no RFQ without a current pack', 'check_on': _check_on(f, 7), 'time_to_ship_hours': 4,
            'win_rule': 'a current pack with tolerances, BOM and packaging cost',
        }
    if rid == 'PROD-R28':
        ent = f.get('entity') or {}
        return {
            'title': (f'Stop the research clock on {ent.get("label")}: {ent.get("hours_logged"):g} hours against {ent.get("hours_allowed"):g}'
                      if ent.get('hours_logged') is not None and ent.get('hours_allowed') is not None else f'Stop the research clock on {ent.get("label")}'),
            'owner': 'agent_drafts',
            'artefact': {'kind': 'research_note', 'label': f'a 1-page close-out for {ent.get("label")}: what the hours answered, the one open question if any, and the decision'},
            'steps': [
                {'n': 1, 'who': 'agent', 'text': 'List what the logged hours produced (checks, angle, gate, spec) and what is still open.'},
                {'n': 2, 'who': 'agent', 'text': 'Draft the close-out: advance with a named question and a hard cap of 2 more hours, or kill with the reason.'},
                {'n': 3, 'who': 'person', 'text': 'Decide from the card. No more hours log against the candidate until then.'}],
            'size': {'text': (f'{ent.get("hours_logged"):g} of {ent.get("hours_allowed"):g} hours used' if ent.get('hours_logged') is not None and ent.get('hours_allowed') is not None else 'hours unavailable'), 'usd': None},
            'stop_rule': 'no new hours without a named question', 'check_on': _check_on(f, 2), 'time_to_ship_hours': 1,
            'win_rule': 'a stage change or a kill logged',
        }
    if rid == 'PROD-R29':
        ent = f.get('entity') or {}
        label = (ent.get('label') or '').lower()
        return {
            'title': f'Run the multi-year check on {label} before funding {", ".join((ent.get("candidates") or [])[:1]) or "the candidate"}',
            'owner': 'agent',
            'artefact': {'kind': 'research_note', 'label': f'a trend history for {label}: 3 to 5 years of the exact term from public sources with a url and a date per point, the 12-month rate against the multi-year rate, and fad or trend'},
            'steps': [
                {'n': 1, 'who': 'agent', 'text': 'Pull yearly points for the exact lane term (not the broad category) from public sources; every point keeps its url and date.'},
                {'n': 2, 'who': 'agent', 'text': 'Compute the last-year rate and the multi-year rate; a last year over twice the multi-year rate reads as a spike.'},
                {'n': 3, 'who': 'agent', 'text': 'Write the series into the web pass fixture so the lane map and the pattern tag read it next run.'},
                {'n': 4, 'who': 'person', 'text': 'Read the verdict on the candidate card; a spike sends it back to screened.'}],
            'size': {'text': f'{ent.get("verdict", "").replace("_", " ")} on {ent.get("market") or "no market"}', 'usd': None},
            'stop_rule': 'no funding on a forecast alone', 'check_on': _check_on(f, 7), 'time_to_ship_hours': 2,
            'win_rule': '3 or more years of history on file for the lane',
        }
    if rid == 'PROD-R30':
        ent = f.get('entity') or {}
        label = ent.get('label') or 'the surface'
        theme = (ent.get('top_theme') or 'the loudest theme').lower()
        if ent.get('kind') == 'forum':
            return {
                'title': f'Open a listening post on {label} and answer {theme} there as the brand',
                'owner': 'agent_drafts',
                'artefact': {'kind': 'research_note', 'label': f'a listening brief for {label}: the weekly thread pull under the Reddit cap, the {theme} answer with the brand\'s proof, the disclosure line, and the log of threads that name a competitor'},
                'steps': [
                    {'n': 1, 'who': 'agent', 'text': f'Pull the top threads on {label} that name the category each week under the brand\'s Reddit cap; store counts and short quotes, never usernames.'},
                    {'n': 2, 'who': 'agent', 'text': f'Draft the {theme} answer from the objection ladder proof, with a plain disclosure that the poster works for the brand.'},
                    {'n': 3, 'who': 'person', 'text': f'Post the answer on {label} as the brand where the subreddit rules allow it; no Reddit user is ever quoted in an ad.'},
                    {'n': 4, 'who': 'agent', 'text': 'Write a channels record for the surface so this read closes, and log each thread that recommends a competitor into the competitors section.'}],
                'size': {'text': f'{ent.get("quotes") or 0} quotes, {(ent.get("upvotes") or 0):,} upvotes', 'usd': None},
                'stop_rule': 'stop when a mod removes a post or the subreddit rules bar brand replies', 'check_on': _check_on(f, 14), 'time_to_ship_hours': 3,
                'win_rule': 'a channels record names the surface and the loudest theme has a posted answer',
            }
        if ent.get('kind') == 'reviews':
            return {
                'title': f'Claim the brand profile on {label} and answer the {theme} reviews',
                'owner': 'person',
                'artefact': {'kind': 'brain_record', 'label': f'a channels record for {label}: the claimed profile url, who answers reviews, the {theme} reply template, and the review count at claim'},
                'steps': [
                    {'n': 1, 'who': 'person', 'text': f'Claim or verify the brand profile on {label} from the brand email.'},
                    {'n': 2, 'who': 'agent', 'text': f'Draft the reply template for {theme} from the objection ladder proof; one paragraph, no promotion.'},
                    {'n': 3, 'who': 'person', 'text': 'Answer the open 1 and 2 star reviews first, newest first.'},
                    {'n': 4, 'who': 'agent', 'text': 'Write the channels record and add the source to the next review pull.'}],
                'size': {'text': f'{ent.get("quotes") or 0} review quotes on file', 'usd': None},
                'stop_rule': 'stop if the profile is held by a reseller and cannot be claimed', 'check_on': _check_on(f, 14), 'time_to_ship_hours': 2,
                'win_rule': f'the profile is claimed and the {theme} reviews have a brand reply',
            }
        return {
            'title': f'Open a brand account on {label} and post the {theme} answer',
            'owner': 'person',
            'artefact': {'kind': 'brain_record', 'label': f'a channels record for {label}: the account, who posts, and the first 3 posts on {theme}'},
            'steps': [
                {'n': 1, 'who': 'person', 'text': f'Open the brand account on {label}.'},
                {'n': 2, 'who': 'agent', 'text': f'Draft 3 posts on {theme} from the objection ladder proof and the language bank.'},
                {'n': 3, 'who': 'person', 'text': 'Post them and write the channels record.'}],
            'size': {'text': f'{ent.get("posts") or 0} posts in the pull', 'usd': None},
            'stop_rule': 'stop if the surface bars brand accounts', 'check_on': _check_on(f, 14), 'time_to_ship_hours': 3,
            'win_rule': 'a channels record names the surface',
        }
    if rid == 'PROD-R31':
        ent = f.get('entity') or {}
        resellers = ', '.join(ent.get('resellers') or []) or 'the resellers'
        missing = ', '.join(x.replace('_', ' ') for x in (ent.get('lines_not_found') or []))
        return {
            'title': f'Decide the Amazon stance: enrol Brand Registry and take the seller of record from {resellers}',
            'owner': 'person',
            'artefact': {'kind': 'policy', 'label': f'an Amazon channel policy: Brand Registry filed, the stance (sell direct, one authorised reseller, or stay off), the listing plan for the {ent.get("listings") or 0} listings and the price floor per pair'},
            'steps': [
                {'n': 1, 'who': 'person', 'text': 'File Brand Registry with the registered trademark; it is the door to the brand store, A+ content and listing control.'},
                {'n': 2, 'who': 'agent', 'text': f'Draft the stance memo: what the {ent.get("ratings") or 0:,} public ratings say about demand, the per-pair price on the listings against the site (${ent.get("median_per_pair") or 0:,.2f} against ${ent.get("site_per_pair") or 0:,.2f}), and the margin gate for selling direct.'},
                {'n': 3, 'who': 'person', 'text': 'Choose: sell direct, appoint one authorised reseller under a price floor, or stay off and report the rest.'},
                {'n': 4, 'who': 'agent', 'text': 'Write the marketplaces record with the stance and the date; the listing check re-runs on the next pull.' + (f' Lines not found on Amazon ({missing}) enter the listing plan only if the stance is sell direct.' if missing else '')}],
            'size': {'text': f'{ent.get("listings") or 0} listings, {ent.get("ratings") or 0:,} ratings, {len(ent.get("resellers") or [])} resellers seen', 'usd': None},
            'stop_rule': 'no listing work before Brand Registry is filed', 'check_on': _check_on(f, 30), 'time_to_ship_hours': 6,
            'win_rule': 'Brand Registry active and a marketplaces record naming the stance',
        }
    if rid == 'PROD-R32':
        ent = f.get('entity') or {}
        return {
            'title': f'Check the {ent.get("way") or "off"}-price listing {ent.get("id")} against the site price and the seller',
            'owner': 'agent',
            'artefact': {'kind': 'report', 'label': f'a price integrity row for {ent.get("id")}: seller of record, price per pair against the site, whether the offer is the brand\'s product, and the step (report, price floor, or leave)'},
            'steps': [
                {'n': 1, 'who': 'agent', 'text': 'Read the seller of record and the offer count on the listing (the listing actor, under the Apify caps).'},
                {'n': 2, 'who': 'agent', 'text': f'Compare the per-pair price (${ent.get("per_pair") or 0:,.2f}) with the site (${ent.get("site_per_pair") or 0:,.2f}); a listing under the site price with few ratings is checked as a possible copy, not assumed one.'},
                {'n': 3, 'who': 'person', 'text': 'Decide: report the listing, set a reseller price floor, or leave it.'}],
            'size': {'text': f'{abs(round((ent.get("spread") or 0) * 100))} percent {ent.get("way")} the site, {ent.get("ratings") or 0:,} ratings', 'usd': None},
            'stop_rule': 'no report without the seller read', 'check_on': _check_on(f, 14), 'time_to_ship_hours': 1,
            'win_rule': 'seller read and a decision on the row',
        }
    if rid == 'PROD-R33':
        ent = f.get('entity') or {}
        label = (ent.get('label') or 'the lane').lower()
        nw = ent.get('newest') or {}
        return {
            'title': f'Answer the {label} launch cadence: brief the next SKU there before {nw.get("brand") or "the competitors"} own the lane',
            'owner': 'agent',
            'artefact': {'kind': 'research_note', 'label': f'a next-SKU brief for {label}: the {ent.get("theirs_24m") or 0} competitor launches with price and date, the gap they leave, the candidate spec and price, and the screen-in row for the pipeline'},
            'steps': [
                {'n': 1, 'who': 'agent', 'text': f'List the {ent.get("theirs_24m") or 0} competitor launches in {label} with price, channel and claim from the web pass; newest first.'},
                {'n': 2, 'who': 'agent', 'text': 'Read the reviews on the newest one for the gap it leaves (fit, price, durability, style); that gap is the candidate angle.'},
                {'n': 3, 'who': 'agent', 'text': 'Write the candidate into the pipeline at screened with the angle and its source; the margin gate and the time box start there.'},
                {'n': 4, 'who': 'person', 'text': 'Approve the screen-in from the card, or mark the lane as one we hold with the current line.'}],
            'size': {'text': f'{ent.get("theirs_12m") or 0} competitor launches in 12 months, {len(ent.get("brands") or [])} brands, ours none in 24', 'usd': None},
            'stop_rule': 'no brief if the lane fails the demand screen', 'check_on': _check_on(f, 14), 'time_to_ship_hours': 3,
            'win_rule': 'a screened candidate in the lane, or a founder note that the current line holds it',
        }
    if rid == 'PROD-R34':
        ent = f.get('entity') or {}
        line = ent.get('label') or 'the line'
        reason = (ent.get('top_reason') or 'the top reason').replace('_', ' ')
        fix = {'size or fit': 'a size guide and a fit note on the page', 'not as expected': 'photos, dimensions and a plain description that match the product', 'damaged in transit': 'packaging and the carrier',
               'changed mind': 'the offer and the page promise', 'arrived late': 'the shipping promise and the carrier', 'wrong item': 'the pick and pack step'}.get(reason, 'the product, the page and the packaging')
        return {
            'title': f'Cut the returns on {line}: read the {reason} returns and fix {fix.split(" and ")[0]}',
            'owner': 'agent',
            'artefact': {'kind': 'research_note', 'label': f'a returns read for {line}: the reasons with counts, 10 customer notes per top reason, the fix ({fix}), and the rate to hold after it'},
            'steps': [
                {'n': 1, 'who': 'agent', 'text': f'Pull the {ent.get("returns") or 0} returns on {line} with their reasons and any customer notes; group by reason.'},
                {'n': 2, 'who': 'agent', 'text': f'For {reason}, draft the fix: {fix}.'},
                {'n': 3, 'who': 'person', 'text': 'Approve the fix; a product change goes to sourcing, a page change to the landing page desk.'},
                {'n': 4, 'who': 'agent', 'text': f'Re-read the rate after 60 days against the store median ({round((ent.get("median") or 0) * 100, 1)} percent).'}],
            'size': {'text': f'{round((ent.get("rate") or 0) * 100, 1)} percent of {ent.get("units") or 0:,} units', 'usd': None},
            'stop_rule': 'stop if the reasons are spread thin with no top reason over 30 percent', 'check_on': _check_on(f, 60), 'time_to_ship_hours': 3,
            'win_rule': 'the line\'s return rate within 1.2 times the store median over the next 60 days',
        }
    if rid == 'PROD-R35':
        ent = f.get('entity') or {}
        doubt = ent.get('doubt') or 'the doubt'
        return {
            'title': f'Ask the founder what proof answers "{doubt}"',
            'owner': 'agent_drafts',
            'artefact': {'kind': 'brain_record', 'label': f'the founder\'s answer as a record: a claim, policy or offer that answers "{doubt}" (approved, since the founder gave it), or a note that no proof exists and the doubt is a product or offer problem'},
            'steps': [
                {'n': 1, 'who': 'agent', 'text': f'Draft the question with the 3 strongest of the {ent.get("quotes") or 0} complaint quotes and the proof that would answer it (a guarantee, a policy, a spec, a test).'},
                {'n': 2, 'who': 'person', 'text': 'Answer in a line from the plan, or say no proof exists yet.'},
                {'n': 3, 'who': 'agent', 'text': 'Write the answer as a claims, policies or offers record and set answered_on; the theme card and the ad brief read it next run.'},
                {'n': 4, 'who': 'agent', 'text': 'With no proof, log it on the theme as a product or offer gap and open a candidate note if the fix is a product.'}],
            'size': {'text': f'{ent.get("quotes") or 0} complaint quotes, {(ent.get("verdict") or "").replace("_", " ")}', 'usd': None},
            'stop_rule': 'one ask per question; no re-ask inside 14 days', 'check_on': _check_on(f, 14), 'time_to_ship_hours': 1,
            'win_rule': 'answered_on set and a record that answers the doubt',
        }
    if rid == 'PROD-R36':
        ent = f.get('entity') or {}
        label = ent.get('label') or 'the pull'
        v = ent.get('verdict')
        est = f'about ${ent["estimate_usd"]:,.2f}' if ent.get('estimate_usd') is not None else 'no price on file'
        caps = f'${ent.get("per_run_cap") or 0:,.0f} a run and ${ent.get("per_week_cap") or 0:,.0f} a week'
        if v == 'unset':
            return {
                'title': f'Set the actor for {label} so the seller of record can be read',
                'owner': 'person',
                'artefact': {'kind': 'connector_setup', 'label': 'the listing actor and its price per 1,000 results in the brand\'s apify.json and the connector price table (a contract ask)'},
                'steps': [{'n': 1, 'who': 'person', 'text': 'Pick a listing details actor on the Apify Store that returns the seller of record and the offer count per ASIN; note its price per 1,000 results.'},
                          {'n': 2, 'who': 'person', 'text': 'Set amazon_reviews.listing_actor in the brand\'s apify.json and ask for the price to be added to the connector table.'},
                          {'n': 3, 'who': 'agent', 'text': 'Run it in mock mode against the fixture shape, then a person approves the live run under the caps.'}],
                'size': {'text': 'one actor to name', 'usd': None}, 'stop_rule': 'no live run without a price on file', 'check_on': _check_on(f, 14), 'time_to_ship_hours': 1,
                'win_rule': 'a listing actor named with a price, and the seller column filled on the next pull',
            }
        return {
            'title': f'Approve the {"refresh" if v == "due" else "first live run"} of {label} ({est}, caps {caps})',
            'owner': 'person',
            'artefact': {'kind': 'connector_setup', 'label': f'a run of {label} under the caps, its rows extracted into the brain sections it fills, and the desk re-run'},
            'steps': [{'n': 1, 'who': 'person', 'text': f'From a session that allows paid calls, run: {ent.get("command") or "the pull script for this brand"}. The connector reserves the estimate in the ledger and stops at the caps.'},
                      {'n': 2, 'who': 'agent', 'text': 'Extract the rows into the brain sections the pull fills; usernames are never stored, quotes stay short.'},
                      {'n': 3, 'who': 'agent', 'text': f'Re-run this desk; the blocks it feeds ({", ".join(ent.get("feeds") or [])}) read the new capture.'}],
            'size': {'text': f'{(v or "due").replace("_", " ")}; {est}', 'usd': ent.get('estimate_usd')},
            'stop_rule': 'stop at the per-run or weekly cap; never raise a cap from a run', 'check_on': _check_on(f, 7), 'time_to_ship_hours': 1,
            'win_rule': 'a live capture dated inside the window',
        }
    if rid == 'PROD-R37':
        ent = f.get('entity') or {}
        name = ent.get('label') or 'the candidate'
        if ent.get('verdict') == 'no_plan':
            return {
                'title': f'Size the first run for {name}: units, the format and its MOQ, the cash it ties up',
                'owner': 'agent',
                'artefact': {'kind': 'research_note', 'label': f'a first-run plan for {name}: units wanted, the fully custom format and its MOQ, a lower-MOQ format and its MOQ, cash out for each, and which one the first run takes (bank idea BRD-249)'},
                'steps': [
                    {'n': 1, 'who': 'agent', 'text': 'Set the units the demand case supports for the first 90 days from the demand pattern and the lane signals.'},
                    {'n': 2, 'who': 'agent', 'text': 'Ask the supplier for the MOQ of the fully custom format and of a lower-MOQ alternative (stock blank plus a sleeve or label, a simpler pack); write both with cash out.'},
                    {'n': 3, 'who': 'person', 'text': 'Pick the format for the first run; a lower-MOQ format tests real demand before the custom run.'},
                    {'n': 4, 'who': 'agent', 'text': 'Write it on the candidate (first run: units, MOQ, format, cash, the option) so the cash plan and the scorecard read it.'}],
                'size': {'text': f'{ent.get("stage")}, no first run on file', 'usd': None},
                'stop_rule': 'no purchase order before the first run is sized', 'check_on': _check_on(f, 7), 'time_to_ship_hours': 2,
                'win_rule': 'a first run on the candidate with both formats costed',
            }
        return {
            'title': f'Cut the first-run risk on {name}: cost a lower-MOQ format before committing ${(ent.get("cash_usd") or 0):,.0f}',
            'owner': 'agent',
            'artefact': {'kind': 'research_note', 'label': f'a lower-MOQ option for {name}: the alternative format, its MOQ and cash, the sell-through read point, and when the custom format follows (bank idea BRD-249)'},
            'steps': [
                {'n': 1, 'who': 'agent', 'text': f'Ask the supplier for the MOQ difference between the {ent.get("format") or "custom"} format and a lower-MOQ alternative (a stock blank with a sleeve or label, a simpler pack).'},
                {'n': 2, 'who': 'agent', 'text': 'Cost both runs: units, cash out, and cash conversion days against the demand pattern.'},
                {'n': 3, 'who': 'person', 'text': 'Choose the lower-MOQ format for the first run if the difference is meaningful; move to the custom format once sell-through proves the demand.'},
                {'n': 4, 'who': 'agent', 'text': 'Write the option on the candidate and track the first run cash against the demand it validated.'}],
            'size': {'text': f'${(ent.get("cash_usd") or 0):,.0f} at full MOQ' + (f', {ent.get("moq_units"):,} MOQ against {ent.get("units"):,} wanted' if ent.get('moq_units') and ent.get('units') else ''), 'usd': ent.get('cash_usd')},
            'stop_rule': 'no full-MOQ order until sell-through on the first run is read', 'check_on': _check_on(f, 14), 'time_to_ship_hours': 2,
            'win_rule': 'a lower-MOQ option noted on the candidate, or a founder note that the full run is the choice',
        }
    if rid == 'PROD-R38':
        ent = f.get('entity') or {}
        return {
            'title': f'Log why {ent.get("label") or "the candidate"} moved on with {", ".join(ent.get("failed") or []) or "a failed check"}, or send it back',
            'owner': 'agent_drafts',
            'artefact': {'kind': 'brain_record', 'label': 'an override line in the candidate log: the rule overridden, the exact signal that justified it, who decided (bank idea PRD-113)'},
            'steps': [{'n': 1, 'who': 'agent', 'text': 'Draft the override line from the log and the checks: which rule, what signal argued against it, when it was carried past.'},
                      {'n': 2, 'who': 'person', 'text': 'Confirm the reason in one line on the pipeline row (Log override), or send the candidate back a stage.'},
                      {'n': 3, 'who': 'agent', 'text': 'Re-read the candidate; an override with a reason closes this, a second unexplained pass reopens it.'}],
            'size': {'text': f'{len(ent.get("failed") or [])} failed, at {ent.get("stage")}', 'usd': None}, 'stop_rule': 'no further stage without the line', 'check_on': _check_on(f, 3), 'time_to_ship_hours': 0.5,
            'win_rule': 'a log line naming the override and its signal',
        }
    if rid == 'PROD-R39':
        ent = f.get('entity') or {}
        return {
            'title': f'Name the evergreen companion before the first run of {ent.get("label") or "the trending candidate"}',
            'owner': 'agent',
            'artefact': {'kind': 'research_note', 'label': 'the evergreen companion: the line or candidate that sells all year beside this trend, its share of the first run cash, and the read point for the trend (bank idea PRD-047)'},
            'steps': [{'n': 1, 'who': 'agent', 'text': 'List the store\'s lines tagged evergreen and any open candidate tagged evergreen; if none, screen one in from the hero lines.'},
                      {'n': 2, 'who': 'agent', 'text': 'Size the first run so the trend is a share of the cash, not all of it; write it on the first-run plan.'},
                      {'n': 3, 'who': 'person', 'text': 'Pick the companion from the card, or accept the trend alone with a note.'}],
            'size': {'text': f'trending, at {ent.get("stage")}', 'usd': None}, 'stop_rule': 'no MOQ order on a trend alone', 'check_on': _check_on(f, 7), 'time_to_ship_hours': 1,
            'win_rule': 'an evergreen line or candidate named beside the trend',
        }
    if rid == 'PROD-R40':
        ent = f.get('entity') or {}
        name = ent.get('label') or 'the candidate'
        if ent.get('lead_time_days') is None:
            return {
                'title': f'Set the lead time for {name} so its order-by date can be read',
                'owner': 'agent',
                'artefact': {'kind': 'brain_record', 'label': f'the lead time in days on {name} (from the supplier quote), or a brand default in learnings.lead_time_days'},
                'steps': [{'n': 1, 'who': 'agent', 'text': 'Read the supplier quote or the tech pack for production plus transit days; with none, use the brand default and say so.'},
                          {'n': 2, 'who': 'person', 'text': 'Enter the lead time on the pattern row; the order-by date and the calendar read it at once.'}],
                'size': {'text': 'one number', 'usd': None}, 'stop_rule': 'no cash plan without a lead time', 'check_on': _check_on(f, 7), 'time_to_ship_hours': 0.5,
                'win_rule': 'an order-by date on the candidate',
            }
        return {
            'title': f'Decide the first run of {name} before {ent.get("order_by")}: the order must go in for the {str(ent.get("peak") or "")[:7]} peak',
            'owner': 'agent',
            'artefact': {'kind': 'research_note', 'label': f'the first-run decision for {name}: units, format, cash and the purchase order date, sized from the demand pattern and the margin gate'},
            'steps': [{'n': 1, 'who': 'agent', 'text': f'Size the first run (units, format, MOQ, cash) from the demand pattern and the gate; the order-by date is {ent.get("order_by")} with {ent.get("lead_time_days")} days of lead time and {audit.ORDER_SAFETY_DAYS} of safety.'},
                      {'n': 2, 'who': 'person', 'text': 'Decide: order by the date, order a smaller lower-MOQ run, or skip this peak and note it.'},
                      {'n': 3, 'who': 'agent', 'text': 'Write the first run on the candidate and the order date into the cash plan; the calendar carries it.'}],
            'size': {'text': f'{ent.get("days")} days to the order-by date' if (ent.get('days') or 0) >= 0 else f'{-(ent.get("days") or 0)} days past the order-by date', 'usd': None},
            'stop_rule': 'no order after the order-by date without a note that the peak is skipped', 'check_on': ent.get('order_by') or _check_on(f, 7), 'time_to_ship_hours': 2,
            'win_rule': 'a first run decided and a purchase order date in the cash plan',
        }
    if rid == 'PROD-R41':
        ent = f.get('entity') or {}
        sec = ent.get('label') or 'the section'
        if ent.get('verdict') == 'conflict':
            return {
                'title': f'Settle the open conflict in the brain\'s {sec} section before this desk reads it again',
                'owner': 'person',
                'artefact': {'kind': 'brain_record', 'label': f'the kept value in {sec}, decided by the founder on the brand brain screen, and the conflict marked resolved'},
                'steps': [{'n': 1, 'who': 'agent', 'text': 'List the conflicting values with their sources and dates.'}, {'n': 2, 'who': 'person', 'text': 'Pick the kept value on the brand brain screen.'},
                          {'n': 3, 'who': 'agent', 'text': f'Re-run this desk; the {len(ent.get("readers") or [])} rules that read {sec} pick the kept value up.'}],
                'size': {'text': f'{len(ent.get("open_conflicts") or [])} conflict{"s" if len(ent.get("open_conflicts") or []) != 1 else ""}', 'usd': None}, 'stop_rule': 'no rule on this desk overrides a founder decision', 'check_on': _check_on(f, 7), 'time_to_ship_hours': 0.5,
                'win_rule': 'no open conflict on the section',
            }
        return {
            'title': f'Refresh the brain\'s {sec} section: {ent.get("age_days") if ent.get("age_days") is not None else "unknown"} days old against a {ent.get("ttl_days") or "?"}-day TTL',
            'owner': 'agent',
            'artefact': {'kind': 'brain_record', 'label': f'the {sec} section re-read from its sources (a pull under the caps where one feeds it, else the site or the founder) and its freshness record updated'},
            'steps': [{'n': 1, 'who': 'agent', 'text': f'Find what feeds {sec} (the pulls block names the actor where one does) and estimate the run.'},
                      {'n': 2, 'who': 'person', 'text': 'Approve the paid pull, or answer the founder fields yourself on the brand brain screen.'},
                      {'n': 3, 'who': 'agent', 'text': f'Merge the new records, retire the stale ones, and re-run the {len(ent.get("readers") or [])} rules here that read {sec}.'}],
            'size': {'text': f'read by {len(ent.get("readers") or [])} rules', 'usd': None}, 'stop_rule': 'stop at the per-run or weekly cap', 'check_on': _check_on(f, 7), 'time_to_ship_hours': 1,
            'win_rule': 'the section inside its TTL with no stale records',
        }
    if rid == 'PROD-R42':
        ent = f.get('entity') or {}
        return {
            'title': f'Confirm or correct the {ent.get("label") or "assumption"} ({ent.get("short") or ""}) that {len(ent.get("readers") or [])} rules price with',
            'owner': 'person',
            'artefact': {'kind': 'brain_record', 'label': f'the {ent.get("label")} assumption with status founder (kept or corrected), its as-of date and source, in the brand\'s assumptions file'},
            'steps': [{'n': 1, 'who': 'agent', 'text': f'Show the number, its {ent.get("status")} source{"s" if len(ent.get("sources") or []) != 1 else ""} and the rules that read it: {", ".join(ent.get("readers") or [])}.'},
                      {'n': 2, 'who': 'person', 'text': 'Confirm it, or give the real number; a real store connection replaces it outright.'},
                      {'n': 3, 'who': 'agent', 'text': 'Write the status and re-run the desk; the money on those rules moves with it.'}],
            'size': {'text': f'{ent.get("status")}, as of {ent.get("as_of") or "undated"}', 'usd': None}, 'stop_rule': 'no money claim in a memo rests on an unconfirmed assumption without saying so', 'check_on': _check_on(f, 14), 'time_to_ship_hours': 0.5,
            'win_rule': 'status founder on the assumption',
        }
    if rid == 'PROD-R43':
        ent = f.get('entity') or {}
        return {
            'title': f'Widen the {(ent.get("label") or "read").lower()} read before acting on the {len(ent.get("rules") or [])} rules that stand on it',
            'owner': 'person',
            'artefact': {'kind': 'connector_setup', 'label': f'the {(ent.get("label") or "read").lower()} read above its floor: a pull or a web pass approved and run under the caps, then the desk re-run'},
            'steps': [{'n': 1, 'who': 'agent', 'text': 'Name the pull or the web pass that widens this read (the pulls block has the command and the estimate).'},
                      {'n': 2, 'who': 'person', 'text': 'Approve the paid call, or accept the thin read with a note on the cards that stand on it.'},
                      {'n': 3, 'who': 'agent', 'text': f'Re-run the desk; the rules on this read ({", ".join(ent.get("rules") or [])}) re-score with the wider sample.'}],
            'size': {'text': '; '.join(ent.get('why') or []), 'usd': None}, 'stop_rule': 'stop at the per-run or weekly cap', 'check_on': _check_on(f, 7), 'time_to_ship_hours': 1,
            'win_rule': 'the read at or above every floor',
        }
    if rid == 'PROD-R44':
        ent = f.get('entity') or {}
        theme = (ent.get('theme_label') or 'the theme').lower()
        return {
            'title': f'Fix the {ent.get("label") or "line"} listing and page for {theme}: {round((ent.get("share") or 0) * 100)} percent of its complaints',
            'owner': 'agent_drafts',
            'artefact': {'kind': 'listing_fix', 'label': f'the {ent.get("label")} listing and PDP changes for {theme}: the answer in the bullets and the first image, the size or care note where it belongs, and the review reply template'},
            'steps': [{'n': 1, 'who': 'agent', 'text': f'Read the {ent.get("total") or 0} complaint quotes on {theme} and name the 3 concrete causes (fit, wear, pack, expectation).'},
                      {'n': 2, 'who': 'agent', 'text': 'Draft the listing bullets, the first-image note and the PDP section that answer them with the proof on file; a product cause goes to the candidate pipeline as a fix.'},
                      {'n': 3, 'who': 'person', 'text': 'Approve and publish the copy on the marketplace and the site.'},
                      {'n': 4, 'who': 'agent', 'text': 'Re-read the theme share on new reviews after 60 days.'}],
            'size': {'text': f'{ent.get("total") or 0} quotes, {", ".join(ent.get("sources") or [])}', 'usd': None}, 'stop_rule': 'no claim the proof does not back', 'check_on': _check_on(f, 60), 'time_to_ship_hours': 3,
            'win_rule': f'{theme} under 30 percent of new complaint quotes on the line',
        }
    if rid == 'PROD-R45':
        ent = f.get('entity') or {}
        return {
            'title': f'Name the owner of {ent.get("label") or "the candidate"} before its test runs',
            'owner': 'person',
            'artefact': {'kind': 'ticket', 'label': f'the owner on {ent.get("label")}: the person who reads the test at its read point and runs the diagnosis if it underperforms (bank idea PRD-126)'},
            'steps': [{'n': 1, 'who': 'person', 'text': 'Enter the owner on the pipeline row (Owner).'}, {'n': 2, 'who': 'agent', 'text': 'Put the owner on the proposed test and the calendar entry for the review date.'}],
            'size': {'text': f'at {ent.get("stage")}', 'usd': None}, 'stop_rule': 'no go without an owner', 'check_on': _check_on(f, 3), 'time_to_ship_hours': 0.2,
            'win_rule': 'an owner named on the candidate',
        }
    return None


def merge_lanes(actions, brand=None):
    """One action per lane: a PROD-R05 market finding and a PROD-R06 competitor finding on the same lane share the brief."""
    r06 = [a for a in actions if a.get('rule_id') == 'PROD-R06']
    keep = []
    for a in actions:
        if a.get('rule_id') not in ('PROD-R05', 'PROD-R20', 'PROD-R33'):
            keep.append(a)
            continue
        key = (a.get('entity') or {}).get('id') or ''
        if a.get('rule_id') in ('PROD-R20', 'PROD-R33'):
            host = next((b for b in r06 if (b.get('entity') or {}).get('id') == key), None)
        else:
            words = set(audit.MARKET_WORDS.get(key, []))
            host = next((b for b in r06 if words & set(next((t for k, _, t in audit.lanes_for(brand) if k == (b.get('entity') or {}).get('id')), []))), None)
        if host is None:
            keep.append(a)
            continue
        host['finding_ids'] = sorted(set(host['finding_ids']) | set(a['finding_ids']))
        host['why'] = host['why'] + ' ' + a['why']
        host['brain_refs'] = sorted(set(host.get('brain_refs') or []) | set(a.get('brain_refs') or []))
        host['rubric']['confidence'] = max(host['rubric'].get('confidence') or 0, a['rubric'].get('confidence') or 0)
    return keep


def merge_surfaces(actions):
    """One action for the forums: the highest-scored PROD-R30 forum finding hosts the other subreddits, so the plan shows one
    listening post, not one card per subreddit. Review and social surfaces keep their own card."""
    forums = [a for a in actions if a.get('rule_id') == 'PROD-R30' and (a.get('entity') or {}).get('kind') == 'forum']
    if len(forums) < 2:
        return actions
    forums.sort(key=lambda a: -((a.get('rubric') or {}).get('total') or 0))
    host = forums[0]
    keep = []
    for a in actions:
        if a is host or a not in forums:
            keep.append(a)
            continue
        host['finding_ids'] = sorted(set(host['finding_ids']) | set(a['finding_ids']))
        host['why'] = host['why'] + ' ' + a['why']
        host['rubric']['confidence'] = max(host['rubric'].get('confidence') or 0, a['rubric'].get('confidence') or 0)
    others = [(a.get('entity') or {}).get('label') for a in forums[1:]]
    host['title'] = host['title'].replace(' and answer', f' plus {", ".join(o for o in others if o)} and answer', 1)
    host['size'] = {'text': f'{len(forums)} subreddits: ' + (host.get('size') or {}).get('text', ''), 'usd': None}
    return keep


def merge_marketplace(actions):
    """One card for Amazon: PROD-R32 price-spread listings join the PROD-R31 stance card when it exists, else the
    highest-scored spread hosts the rest, so the plan shows one marketplace decision, not one card per ASIN."""
    spreads = [a for a in actions if a.get('rule_id') == 'PROD-R32']
    if not spreads:
        return actions
    host = next((a for a in actions if a.get('rule_id') == 'PROD-R31'), None)
    spreads.sort(key=lambda a: -((a.get('rubric') or {}).get('total') or 0))
    if host is None:
        host = spreads[0]
    keep = []
    for a in actions:
        if a is host or a not in spreads:
            keep.append(a)
            continue
        host['finding_ids'] = sorted(set(host['finding_ids']) | set(a['finding_ids']))
        host['why'] = host['why'] + ' ' + a['why']
        host['rubric']['confidence'] = max(host['rubric'].get('confidence') or 0, a['rubric'].get('confidence') or 0)
    n = len(spreads)
    if host.get('rule_id') == 'PROD-R31':
        host['title'] = host['title'] + f'; {n} listing{"s" if n != 1 else ""} priced off the site'
    elif n > 1:
        host['title'] = f'Check {n} Amazon listings priced off the site price, starting with {(host.get("entity") or {}).get("id")}'
    return keep


def merge_questions(actions):
    """A founder question (PROD-R35) rides on its theme's PROD-R07 card when that card is open, so one theme is one card."""
    hosts = {(a.get('entity') or {}).get('id'): a for a in actions if a.get('rule_id') == 'PROD-R07'}
    keep = []
    for a in actions:
        if a.get('rule_id') != 'PROD-R35':
            keep.append(a)
            continue
        host = hosts.get((a.get('entity') or {}).get('id'))
        if host is None:
            keep.append(a)
            continue
        host['finding_ids'] = sorted(set(host['finding_ids']) | set(a['finding_ids']))
        host['why'] = host['why'] + ' ' + a['why']
        host['brain_refs'] = sorted(set(host.get('brain_refs') or []) | set(a.get('brain_refs') or []))
        host['steps'] = host['steps'] + [{'n': len(host['steps']) + 1, 'who': 'person', 'text': f'Answer the open question on this theme: {(a.get("entity") or {}).get("question")}'}]
    return keep


def merge_freshness(actions):
    """One brain refresh card: the highest-scored PROD-R41 section hosts the rest, conflicts first."""
    rows = [a for a in actions if a.get('rule_id') == 'PROD-R41']
    if len(rows) < 2:
        return actions
    rows.sort(key=lambda a: (0 if (a.get('entity') or {}).get('verdict') == 'conflict' else 1, -((a.get('rubric') or {}).get('total') or 0)))
    host = rows[0]
    keep = []
    for a in actions:
        if a is host or a not in rows:
            keep.append(a)
            continue
        host['finding_ids'] = sorted(set(host['finding_ids']) | set(a['finding_ids']))
        host['why'] = host['why'] + ' ' + a['why']
        host['brain_refs'] = sorted(set(host.get('brain_refs') or []) | set(a.get('brain_refs') or []))
    others = [(a.get('entity') or {}).get('label') for a in rows[1:]]
    host['title'] = host['title'] + f'; also {", ".join(o for o in others if o)}'
    return keep


def merge_assumptions(actions):
    """One card for the unconfirmed assumptions: the one most rules read hosts the rest."""
    rows = [a for a in actions if a.get('rule_id') == 'PROD-R42']
    if len(rows) < 2:
        return actions
    rows.sort(key=lambda a: (-len((a.get('entity') or {}).get('readers') or []), a['id']))
    host = rows[0]
    keep = []
    for a in actions:
        if a is host or a not in rows:
            keep.append(a)
            continue
        host['finding_ids'] = sorted(set(host['finding_ids']) | set(a['finding_ids']))
        host['why'] = host['why'] + ' ' + a['why']
        host['brain_refs'] = sorted(set(host.get('brain_refs') or []) | set(a.get('brain_refs') or []))
    host['title'] = f'Confirm or correct {len(rows)} assumptions the desk prices with: ' + ', '.join((a.get('entity') or {}).get('label') or '' for a in rows)
    return keep


def merge_strength(actions):
    """One card for the thin reads: the read with the most rules on it hosts the rest."""
    rows = [a for a in actions if a.get('rule_id') == 'PROD-R43']
    if len(rows) < 2:
        return actions
    rows.sort(key=lambda a: (-len((a.get('entity') or {}).get('rules') or []), a['id']))
    host = rows[0]
    keep = []
    for a in actions:
        if a is host or a not in rows:
            keep.append(a)
            continue
        host['finding_ids'] = sorted(set(host['finding_ids']) | set(a['finding_ids']))
        host['why'] = host['why'] + ' ' + a['why']
    host['title'] = f'Widen {len(rows)} thin reads before acting on what stands on them: ' + ', '.join(((a.get('entity') or {}).get('label') or '').lower() for a in rows)
    return keep


CANDIDATE_RULES = ('PROD-R14', 'PROD-R15', 'PROD-R16', 'PROD-R18', 'PROD-R21', 'PROD-R23', 'PROD-R24', 'PROD-R25', 'PROD-R27', 'PROD-R28', 'PROD-R37', 'PROD-R38', 'PROD-R39', 'PROD-R40', 'PROD-R45')


def merge_candidates(actions):
    """One action per candidate: the highest-scored finding on a candidate hosts the others (its steps stay; the
    other findings' sentences join the why and their ids the finding_ids), so a founder sees one card per idea."""
    by_cand = {}
    for a in actions:
        ent = a.get('entity') or {}
        if a.get('rule_id') in CANDIDATE_RULES and ent.get('candidate'):
            by_cand.setdefault(ent.get('id'), []).append(a)
    drop = set()
    for cid, group in by_cand.items():
        if len(group) < 2:
            continue
        group.sort(key=rank_mod.sort_key)
        host = group[0]
        extra = []
        for a in group[1:]:
            host['finding_ids'] = sorted(set(host['finding_ids']) | set(a['finding_ids']))
            extra.append(a['why'])
            drop.add(a['id'])
        host['why'] = host['why'] + ' Also: ' + ' '.join(extra)
        host['title'] = host['title'] + f' (+{len(group) - 1} more on this candidate)'
        host['size'] = {'text': f'{len(group)} open items on the candidate', 'usd': (host.get('size') or {}).get('usd')}
    return [a for a in actions if a['id'] not in drop]


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


_SAMPLE = {}


def sample_data():
    """The server's reader for the sample brand (app/data/sample-brand), for the rank route, which gets no request object."""
    if 'data' not in _SAMPLE:
        spec = importlib.util.spec_from_file_location('ecomos_server_research', APP / 'server.py')
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _SAMPLE['data'] = mod.Data()
    return _SAMPLE['data']


def rank(brand, window=None):
    """Depth contract section 5: every audit finding becomes an action with an owner, steps and an artefact."""
    window = window or rank_mod.default_window()
    data = None
    if brand in (None, '', 'sample'):
        brand, data = None, sample_data()
    last = audit.last_full_day(data, brand).isoformat()
    if str(window.get('ends_on') or '') > last:
        window = dict(window, ends_on=last)   # the window never runs past the last full day in the data
    nr = rank_mod.net_revenue_28d(brand, window) if brand else None
    findings = audit.run(brand, window, data=data)
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
        if f.get('status') == 'unavailable' and (f.get('unavailable') or {}).get('connector') == 'web_pass':
            a['title'] = 'Run the web pass for this brand so the market, lane and launch reads can start'
            a['steps'] = [{'n': 1, 'who': 'agent', 'text': f'Write the template: python3 app/screens/01-market-research/web_pass.py --brand {brand or "sample"} --init --category "<the category>".'},
                          {'n': 2, 'who': 'agent', 'text': 'Fill it from public sources in a research session: the lanes the category splits into, market sizes and growth, the shifting preferences, competitor launches; one url and one date per number.'},
                          {'n': 3, 'who': 'person', 'text': f'Check it: python3 app/screens/01-market-research/web_pass.py --brand {brand or "sample"} --check. The desk reads it once the check passes.'}]
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
    actions = merge_strength(merge_assumptions(merge_freshness(merge_questions(merge_marketplace(merge_surfaces(merge_candidates(merge_lanes(actions, brand))))))))
    for a in actions:   # a merge can lift the host's confidence; the total follows the rubric
        r = a['rubric']
        r['total'] = round(sum(rank_mod.WEIGHTS[k] * (r[k] if r[k] is not None else 2.5) / 5 for k in rank_mod.WEIGHTS), 1)
    actions.sort(key=rank_mod.sort_key)
    # the founder's decisions (the shared log app/data/decisions.json, written by the decision row): a "not now" parks the
    # action for 14 days and it leaves the plan; an "agent" or "person" choice rides on the card so it is not re-argued
    # the strength of the read each card rests on, from its rule
    br_s = audit.brain(brand) if brand else None
    rd_s = audit.Reader(data, brand, dt.date.fromisoformat(window['ends_on']))
    strength = audit.read_strength(br_s, brand, data, rd_s, dt.date.fromisoformat(window['ends_on']))
    for a in actions:
        sr = audit.strength_of_rule(strength, a.get('rule_id'))
        a['read_strength'] = {'read': sr['label'], 'verdict': sr['verdict'], 'sample': sr['sample'], 'sources': sr['sources'], 'age_days': sr['age_days']} if sr else None
    # what each card covers: every finding behind it, so a merged card reads as a checklist, never a black box
    by_id = {f['id']: f for f in findings}
    names = {r['rule_id']: r['name'] for r in audit.RULES}
    for a in actions:
        a['covers'] = [{'id': fid, 'rule_id': by_id[fid].get('rule_id'), 'rule': names.get(by_id[fid].get('rule_id'), ''), 'severity': by_id[fid].get('severity'),
                        'status': by_id[fid].get('status'), 'sentence': by_id[fid].get('sentence'), 'stake_usd': (by_id[fid].get('money_at_stake') or {}).get('usd')}
                       for fid in a.get('finding_ids') or [] if fid in by_id]
    before = list(actions)
    actions = rank_mod.apply_decisions(actions, today=dt.date.fromisoformat(window['ends_on']), path=DECISIONS_PATH)
    parked = [a for a in before if a.get('status') == 'snoozed']
    for a in parked:
        when = dt.date.fromisoformat(str((a.get('decision') or {}).get('time') or window['ends_on'])[:10])
        a['returns_on'] = (when + dt.timedelta(days=rank_mod.SNOOZE_DAYS)).isoformat()
    return {'screen': SCREEN, 'brand': brand, 'window': window, 'actions': actions, 'parked': parked, 'net_revenue_28d': nr,
            'decided': sum(1 for a in actions if a.get('decision'))}


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
                     'gates': gates_block(brand, data, br, rd, ends_on, findings), 'scorecard': scorecard_block(brand, data, br, rd, ends_on, findings),
                     'video': audit.video_signals(br, brand, ends_on), 'tech_packs': tech_pack_block(brand, findings),
                     'hours': dict(audit.hours_table(brand, br), findings={f['entity']['id']: f['id'] for f in findings if f['rule_id'] == 'PROD-R28'}),
                     'trend_checks': audit.trend_checks(br, brand, ends_on), 'surfaces': audit.audience_surfaces(br, ends_on), 'marketplace': audit.marketplace_read(br, products(data, brand)), 'cadence': audit.launch_cadence(br, ends_on), 'returns': audit.return_rates(data, brand, ends_on), 'questions': audit.open_questions(br, ends_on), 'pulls': audit.pulls(br, brand, ends_on), 'first_runs': audit.first_run_read(brand, ends_on, audit.net_28d(rd)), 'brain_freshness': audit.brain_freshness(br, ends_on), 'assumptions': audit.assumptions(br), 'strength': audit.read_strength(br, brand, data, rd, ends_on), 'line_themes': audit.line_theme_matrix(br)},
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
    write_handoff(brand, today)
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
    if body.get('owner') is not None:
        row['owner'] = str(body['owner']).strip()[:60] or None
        changes.append(f'owner {row["owner"] or "cleared"}')
    if body.get('lead_time_days') is not None:
        row['lead_time_days'] = int(_num(body['lead_time_days'], 1) or 0) or None
        changes.append(f'lead time {row["lead_time_days"]} days')
    if body.get('override_reason') is not None:
        reason = str(body['override_reason']).strip()[:300]
        if reason:
            changes.append(f'override: {reason}')
    if isinstance(body.get('first_run'), dict):
        fr = body['first_run']
        row['first_run'] = {'units': int(_num(fr.get('units')) or 0) or None, 'moq_units': int(_num(fr.get('moq_units')) or 0) or None, 'format': str(fr.get('format') or '').strip()[:120] or None,
                            'cash_usd': _num(fr.get('cash_usd')), 'lower_moq_option': str(fr.get('lower_moq_option') or '').strip()[:300] or None, 'decided_on': today.isoformat()}
        changes.append('first run sized')
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
    if isinstance(body.get('tech_pack'), dict):
        tp = body['tech_pack']
        packs = row.setdefault('tech_packs', [])
        for p in packs:
            if p.get('status') == 'current':
                p['status'] = 'superseded'
        packs.append({'version': f'v{len(packs) + 1}', 'tolerances': str(tp.get('tolerances') or '').strip()[:300] or None, 'bom': str(tp.get('bom') or '').strip()[:600] or None,
                      'packaging_cost': _num(tp.get('packaging_cost')), 'status': 'current', 'updated_at': today.isoformat(), 'note': str(tp.get('note') or '').strip()[:200] or None})
        changes.append(f'tech pack v{len(packs)} added')
    if not changes:
        return 400, {'error': 'nothing to change'}
    row.setdefault('log', []).append({'on': today.isoformat(), 'who': str(body.get('who') or 'person')[:20], 'what': '; '.join(changes)})
    _write_pipeline(doc)
    write_handoff(brand, today)
    test = propose_test(brand, row, today) if row.get('stage') == 'go' and body.get('stage') == 'go' else None
    return {'ok': True, 'candidate': row, 'changes': changes, 'proposed_test': test}


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
    fx = audit.web_pass(brand)
    by_entity = {f['entity']['id']: f['id'] for f in findings if f['rule_id'] == 'PROD-R18'}
    cats = [dict(audit.demand_pattern(r['category'], mix, fx), kind='category') for r in (mix.get('rows') or [])] if not mix.get('unavailable') else []
    cands = []
    br = audit.brain(brand) if brand else None
    by_order = {f['entity']['id']: f['id'] for f in findings if f['rule_id'] == 'PROD-R40'}
    for c in audit.pipeline(brand):
        p = audit.demand_pattern(c.get('category'), mix, fx, c.get('name'))
        lead, lead_src = audit.lead_time_for(c, br)
        order_by, peak = audit.order_by_date(p.get('peak_months'), rd.ends_on, lead) if p['tag'] == 'seasonal' else (None, None)
        cands.append(dict(p, kind='candidate', candidate_id=c.get('candidate_id'), name=c.get('name'), stage=c.get('stage'), closed=c.get('stage') in audit.CLOSED_STAGES,
                          cash_plan=c.get('cash_plan'), finding_id=by_entity.get(c.get('candidate_id')), lead_time_days=lead, lead_time_source=lead_src, order_by=order_by, peak=peak,
                          days_to_order=(dt.date.fromisoformat(order_by) - rd.ends_on).days if order_by else None, first_run_decided=bool(c.get('first_run')), order_finding_id=by_order.get(c.get('candidate_id'))))
    return {'categories': cats, 'candidates': cands, 'unavailable': mix.get('reason') if mix.get('unavailable') else None, 'safety_days': audit.ORDER_SAFETY_DAYS,
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


def tech_pack_block(brand, findings):
    by_entity = {f['entity']['id']: f['id'] for f in findings if f['rule_id'] == 'PROD-R27'}
    rows = []
    for c in audit.pipeline(brand):
        tp = audit.tech_pack_status(c)
        rows.append({'candidate_id': c.get('candidate_id'), 'name': c.get('name'), 'stage': c.get('stage'), 'closed': c.get('stage') in audit.CLOSED_STAGES,
                     'needs_spec': c.get('stage') in audit.STAGES and audit.STAGES.index(c['stage']) >= audit.SPEC_STAGE_MIN, 'status': tp['status'], 'version': tp['version'],
                     'missing': tp['missing'], 'pack': tp['pack'], 'versions': len(c.get('tech_packs') or []), 'finding_id': by_entity.get(c.get('candidate_id'))})
    return {'rows': rows, 'lines': list(audit.TECH_PACK_LINES), 'rule': f'a candidate at {audit.STAGES[audit.SPEC_STAGE_MIN]} or later needs a current pack with tolerances, a BOM and a packaging cost line; saving a pack supersedes the last one'}


def pipeline_block(brand, ends_on, findings, floor):
    rows = [audit.candidate_view(r, ends_on) for r in audit.pipeline(brand)]
    by_entity = {}
    for f in findings:
        if f['rule_id'] in ('PROD-R14', 'PROD-R15', 'PROD-R03'):
            by_entity.setdefault(f['entity']['id'], []).append(f['id'])
    for r in rows:
        r['finding_ids'] = by_entity.get(r.get('candidate_id'), [])
    open_rows = [r for r in rows if not r['closed']]
    tests = proposed_tests(brand or 'sample')
    return {'rows': rows, 'funnel': audit.pipeline_funnel(rows), 'stages': audit.STAGES, 'checks': list(audit.SCREEN_CHECKS),
            'handoff': {'rows': len(rows), 'go': sum(1 for r in rows if r.get('stage') == 'go'), 'with_cost': sum(1 for r in rows if r.get('cogs_estimate') is not None), 'file': 'fixtures/product_candidates.json', 'read_by': ['04-offers-pricing', '19-supply-inventory']},
            'proposed_tests': [{'id': x['id'], 'name': x['name'], 'read_point': x['read_point'], 'status': x['status']} for x in tests],
            'open': len(open_rows), 'over_box': sum(1 for r in open_rows if r['over_box']), 'hours': round(sum(r.get('hours_logged') or 0 for r in rows), 1),
            'gate_rule': MARGIN_GATE, 'floor_pct': floor, 'floor_source': 'finance_inputs.target_contribution_margin' if floor is not None else None,
            'rule': f'a candidate fires when it passes its time box, or fails {audit.SCREEN_FAIL_AT} of the {len(audit.SCREEN_CHECKS)} fast checks'}


def candidate_brief(data, brand, cid):
    """One page per candidate, assembled from every block of the desk: the artefact that goes to creative (angle, avatar,
    proof) and sourcing (spec, margin, cash timing). Plain text a founder can paste; every number comes from the blocks."""
    o = overview(data, brand)
    d = o['desk']
    pipe = next((r for r in (d['pipeline'].get('rows') or []) if r.get('candidate_id') == cid), None)
    if pipe is None:
        raise ValueError(f'no candidate {cid}')

    def row_of(block, key='rows'):
        rows = (d.get(block) or {}).get(key) if isinstance(d.get(block), dict) else d.get(block)
        return next((r for r in rows or [] if r.get('candidate_id') == cid), None)

    margin, gates, score, pack, hours, pattern = row_of('margin'), row_of('gates'), row_of('scorecard'), row_of('tech_packs'), row_of('hours'), row_of('pattern', 'candidates')
    price_row = next((r for r in (d.get('price_signal') or {}).get('candidates') or [] if r.get('candidate_id') == cid), None)
    lanes = [r for r in (d.get('video') or {}).get('rows') or [] if pipe.get('name') in (r.get('candidates') or [])]
    checks = [r for r in (d.get('trend_checks') or {}).get('rows') or [] if pipe.get('name') in (r.get('candidates') or [])]
    acts = [a for a in rank(brand or 'sample', {'ends_on': o['window']['ends_on'], 'days': 28, 'trailing': 4})['actions'] if (a.get('entity') or {}).get('candidate') == cid or cid in json.dumps(a.get('finding_ids') or [])]
    na = 'unavailable'
    g = (margin or {}).get('gate') or {}
    lines = [f'CANDIDATE BRIEF: {pipe.get("name")}', f'{o["brand"].get("brand")}, {o["window"]["ends_on"]}. Stage {pipe.get("stage")}, screened in {pipe.get("screen_in_date") or na}, {pipe.get("hours_logged") or 0} h logged. Simulated sales; public reviews and ads.', '',
             'THE ANGLE', f'{pipe.get("angle_text") or "none yet"}', f'Source: {pipe.get("angle_source") or "none"}. Confidence: {((gates or {}).get("angle") or {}).get("label") or na}.', '',
             'THE DEMAND CASE']
    lines.append(f'Fast checks: ' + ', '.join(f'{k} {v or "unchecked"}' for k, v in (pipe.get('screen_result') or {}).items()))
    for r in lanes:
        lines.append(f'Lane {r.get("label")}: {({"pattern": "a pattern across platforms", "single": "one platform only", "none": "no platform above the floor"}).get(r.get("verdict"), r.get("verdict"))}; platforms {", ".join(r.get("platforms") or []) or "none"}; Instagram posts {r.get("instagram_posts") if r.get("instagram_posts") is not None else na}{" (mock)" if r.get("instagram_mode") == "mock" else ""}; Reddit {r.get("reddit_mentions") or 0} mentions, {r.get("reddit_upvotes") or 0} upvotes; creator ads {", ".join(r.get("creator_pages") or []) or "none"}.')
    for r in checks:
        lines.append(f'Trend on {r.get("label")}: {r.get("verdict", "").replace("_", " ")} ({r.get("market") or "no series"}, {r.get("history_years") or 0} years of history).')
    if pattern:
        lines.append(f'Demand pattern: {pattern.get("tag")}; {pattern.get("why")}. Cash timing: {pattern.get("cash_timing")}. Cash plan: {pattern.get("cash_plan") or "none attached"}.')
    lines += ['', 'THE MONEY']
    if margin:
        lines.append(f'Planned price ${(margin.get("price") or 0):,.2f} for {margin.get("pack_units") or 1} unit(s). Modelled contribution margin: ' + (f'{g.get("margin_pct"):g} percent' if g.get('margin_pct') is not None else na) + (f' against a floor of {g.get("floor_pct"):g} percent ({"passes" if g.get("margin_pct") >= g.get("floor_pct") else "fails"}).' if g.get('floor_pct') is not None and g.get('margin_pct') is not None else ' (no floor on file).'))
        if g.get('lines'):
            lines.append('Waterfall: ' + '; '.join(f'{l.get("label")} ${(l.get("usd") or 0):,.2f}' for l in g['lines']))
    if price_row:
        lines.append(f'Review price signal: per pair ${(price_row.get("per_pair") or 0):,.2f} planned against what reviewers say a pair is worth; gap {round((price_row.get("gap") or 0) * 100)} percent.')
    lines += ['', 'THE GATES']
    if gates:
        for k, v in (gates.get('gates') or {}).items():
            v = v if isinstance(v, dict) else {'status': v}
            lines.append(f'{audit.GATE_LABEL.get(k, k)}: {v.get("status") or na}' + (f' ({v.get("why")})' if v.get('why') else ''))
        lines.append(f'Compliance: {gates.get("compliance") or na}.')
    if score:
        lines += ['', 'THE SCORECARD', f'{score.get("total")} of 100, verdict {score.get("verdict", "").replace("_", " ")}; ' + ', '.join(f'{audit.CRITERIA_LABEL[k]} {v if v is not None else "n/a"}' for k, v in (score.get('scores') or {}).items()) + f'. Review date {score.get("review_date") or na}.']
    lines += ['', 'THE SPEC AND THE CLOCK']
    if pack:
        lines.append(f'Tech pack: {pack.get("status", "").replace("_", " ")}' + (f', version {pack.get("version")}' if pack.get('version') else '') + (f', missing {", ".join(m.replace("_", " ") for m in pack.get("missing") or [])}' if pack.get('missing') else '') + '.')
    if hours:
        lines.append(f'Hours: {hours.get("hours_logged")} logged of {hours.get("hours_allowed")} allowed through {hours.get("stage")}' + (f', over by {hours.get("over_by")}' if hours.get('over_by') else '') + '.')
    lines.append(f'Time box: {pipe.get("time_box_days")} days, {pipe.get("days_left") if pipe.get("days_left") is not None else na} left.')
    frr = next((r for r in (d.get('first_runs') or {}).get('rows') or [] if r.get('candidate_id') == cid), None)
    if frr:
        lines.append('First run: ' + (f'{frr.get("units") or na} units, {frr.get("format") or "format unstated"}, MOQ {frr.get("moq_units") or na}, cash ${(frr.get("cash_usd") or 0):,.0f}, lower-MOQ option: {frr.get("lower_moq_option") or "none noted"}' if frr.get('verdict') not in ('no_plan', 'not_yet') else frr.get('verdict', '').replace('_', ' ')) + '.')
    lines += ['', 'OPEN ACTIONS ON THIS CANDIDATE']
    lines += [f'- {a.get("title")} ({a.get("owner")})' for a in acts] or ['- none']
    lines += ['', 'LOG'] + [f'- {l.get("on")} {l.get("who")}: {l.get("what")}' for l in pipe.get('log') or []]
    return {'candidate_id': cid, 'name': pipe.get('name'), 'text': '\n'.join(lines), 'sections': ['angle', 'demand', 'money', 'gates', 'scorecard', 'spec', 'actions', 'log']}


# ---------------------------------------------------------------- the hand-off (events contract: product_candidates, and a proposed test on go)

HANDOFF_PATH = HERE / 'fixtures' / 'product_candidates.json'
TESTS_PATH = HERE / 'fixtures' / 'proposed_tests.json'


def handoff_rows(brand):
    """The product_candidates hand-off (events.md): one row per candidate with what offers and supply need: the stage and the
    decision, planned price, the landed cost estimate, pack units, the first run, the current tech pack, the angle and the
    review date. Numbers are the candidate's own inputs; the gate verdicts live on this desk."""
    rows = []
    for c in audit.pipeline(brand):
        tp = audit.tech_pack_status(c)
        price, cogs = c.get('planned_price'), c.get('cogs_estimate')
        rows.append({'candidate_id': c.get('candidate_id'), 'brand': c.get('brand'), 'name': c.get('name'), 'category': c.get('category'), 'stage': c.get('stage'),
                     'decision': 'go' if c.get('stage') == 'go' else 'no_go' if c.get('stage') == 'killed' else 'open',
                     'planned_price_usd': price, 'landed_cost_estimate_usd': cogs, 'pack_units': c.get('pack_units') or 1,
                     'gross_margin_pct_from_estimates': round((price - cogs) / price * 100, 1) if price and cogs is not None and price > 0 else None,
                     'first_run': c.get('first_run'), 'tech_pack_version': tp.get('version'), 'tech_pack_status': tp.get('status'),
                     'angle_text': c.get('angle_text'), 'angle_source': c.get('angle_source'), 'review_date': c.get('review_date'), 'source_finding': c.get('source_finding'),
                     'updated_at': (c.get('log') or [{}])[-1].get('on'), 'simulated': bool(c.get('simulated', True))})
    return rows


def write_handoff(brand, today):
    """Rewrite fixtures/product_candidates.json after every candidate write, so offers and supply read one file."""
    doc = {'table': 'product_candidates', 'brand': brand, 'written_by': SCREEN, 'written_on': today.isoformat(),
           'note': 'The events contract hand-off from 01-market-research: candidates with landed cost and go or no-go. Read by 04-offers-pricing and 19-supply-inventory. Simulated until a real store connects.',
           'rows': handoff_rows(brand)}
    HANDOFF_PATH.write_text(json.dumps(doc, indent=1), encoding='utf-8')
    return doc


def propose_test(brand, cand, today):
    """On a go, a proposed experiment in the registry shape (events.md, 25-experiments): the angle is the hypothesis, the
    metric is contribution margin, the read point is the review date. Appended to fixtures/proposed_tests.json; only
    25-experiments sets results. One row per candidate; a second go refreshes it."""
    doc = json.loads(TESTS_PATH.read_text(encoding='utf-8')) if TESTS_PATH.is_file() else {'table': 'registry_proposed', 'rows': []}
    rows = [r for r in doc.get('rows') or [] if not (r.get('brand') == brand and r.get('candidate_id') == cand.get('candidate_id'))]
    read_point = cand.get('review_date') or (today + dt.timedelta(days=audit.REVIEW_DAYS)).isoformat()
    rows.append({'id': f'EXP-P-{cand.get("candidate_id")}', 'brand': brand, 'candidate_id': cand.get('candidate_id'), 'name': f'Launch test: {cand.get("name")}', 'screen': SCREEN, 'capability_id': 'PROD-C11',
                 'hypothesis': cand.get('angle_text') or f'{cand.get("name")} sells at its planned price with contribution margin at or above the gate',
                 'source': {'type': 'finding', 'ref': cand.get('source_finding'), 'index': None}, 'idea_id': None, 'owner': cand.get('owner') or 'person',
                 'metric': {'name': 'contribution_margin', 'direction': 'up', 'min_days': 28, 'registered_on': today.isoformat()},
                 'variant': {'control': 'the current line', 'treatment': cand.get('name')}, 'audience': [cand.get('category') or 'all'],
                 'start': None, 'read_point': read_point, 'end': None, 'status': 'proposed', 'result': None, 'decision': None, 'learnings_ref': None, 'retro': None, 'park': None,
                 'brain_refs': [], 'proposed_on': today.isoformat(), 'simulated': True})
    doc['rows'] = rows
    doc['note'] = 'Proposed by 01-market-research on a go decision; the shared registry (25-experiments) takes these rows once it exists.'
    TESTS_PATH.write_text(json.dumps(doc, indent=1), encoding='utf-8')
    return rows[-1]


def proposed_tests(brand):
    doc = json.loads(TESTS_PATH.read_text(encoding='utf-8')) if TESTS_PATH.is_file() else {'rows': []}
    return [r for r in doc.get('rows') or [] if r.get('brand') == brand]


# ---------------------------------------------------------------- the research calendar (round 5.3)

CALENDAR_DAYS = 45


def calendar_items(data, brand, horizon_days=CALENDAR_DAYS):
    """Every dated thing on this desk in the next horizon: candidate review dates and time-box ends, the check dates of the
    open actions, the parked actions' return dates, the pulls' next due dates, and the gift window. Each item names the
    action it opens. Past-due items stay at the top."""
    r = rank(brand or 'sample', None)
    ends_on = dt.date.fromisoformat(r['window']['ends_on'])
    last = ends_on + dt.timedelta(days=horizon_days)
    by_finding = {fid: a for a in r['actions'] for fid in a.get('finding_ids') or []}
    by_cand = {(a.get('entity') or {}).get('id'): a for a in r['actions'] if (a.get('entity') or {}).get('candidate')}
    items = []

    def add(when, kind, title, text, action=None, finding_id=None, tone='accent', candidate=None):
        if not when:
            return
        d = dt.date.fromisoformat(str(when)[:10])
        if d > last:
            return
        a = action or (by_finding.get(finding_id) if finding_id else None) or (by_cand.get(candidate) if candidate else None)
        items.append({'when': d.isoformat(), 'days': (d - ends_on).days, 'kind': kind, 'title': title, 'text': text, 'action_id': a['id'] if a else None,
                      'action_title': a['title'] if a else None, 'tone': 'bad' if d < ends_on else tone})

    for c in audit.pipeline(brand or 'sample'):
        if c.get('stage') in audit.CLOSED_STAGES:
            continue
        cv = audit.candidate_view(c, ends_on)
        if c.get('screen_in_date') and c.get('time_box_days'):
            add((dt.date.fromisoformat(c['screen_in_date']) + dt.timedelta(days=int(c['time_box_days']))).isoformat(), 'time_box', f'Time box ends: {c.get("name")}',
                f'{c.get("time_box_days")} days from {c.get("screen_in_date")}; ' + ('over by ' + str(-cv['days_left']) + ' days' if cv['days_left'] is not None and cv['days_left'] < 0 else f'{cv["days_left"]} days left'),
                finding_id=f'{SCREEN}.PROD-R14.{c.get("candidate_id")}', tone='warn', candidate=c.get('candidate_id'))
        if c.get('review_date'):
            add(c['review_date'], 'review', f'Review date: {c.get("name")}', 'the scorecard memo is read and the founder decides go, hold or kill', finding_id=f'{SCREEN}.PROD-R25.{c.get("candidate_id")}', tone='accent', candidate=c.get('candidate_id'))
    br0 = audit.brain(brand) if brand else None
    rd0 = audit.Reader(data if data is not None else (None if brand else sample_data()), brand, ends_on)
    mix0 = audit.category_mix(data if data is not None else (None if brand else sample_data()), brand, rd0)
    fx0 = audit.web_pass(brand)
    for c in audit.pipeline(brand or 'sample'):
        if c.get('stage') in audit.CLOSED_STAGES:
            continue
        p = audit.demand_pattern(c.get('category'), mix0, fx0, c.get('name'))
        if p['tag'] != 'seasonal':
            continue
        lead, _ = audit.lead_time_for(c, br0)
        ob, peak = audit.order_by_date(p.get('peak_months'), ends_on, lead)
        if ob:
            add(ob, 'order_by', f'Order by: {c.get("name")}', f'{lead} days of lead time plus {audit.ORDER_SAFETY_DAYS} of safety before the {str(peak)[:7]} peak' + ('; first run decided' if c.get('first_run') else '; no first run yet'),
                finding_id=f'{SCREEN}.PROD-R40.{c.get("candidate_id")}', tone='warn', candidate=c.get('candidate_id'))
    for a in r['actions'][:10]:
        if a.get('check_on') and a.get('status') != 'unavailable':
            add(a['check_on'], 'check', f'Check: {a["title"][:70]}', a.get('win_rule') or '', action=a, tone='good')
    for a in r.get('parked') or []:
        add(a.get('returns_on'), 'parked', f'Back on the plan: {a["title"][:60]}', (a.get('decision') or {}).get('reason') or 'parked with not now', action=a, tone='na')
    br = audit.brain(brand) if brand else None
    for p in audit.pulls(br, brand, ends_on)['rows']:
        if p.get('next_due'):
            add(p['next_due'], 'pull', f'Pull due: {p["label"]}', f'{p["window_days"]}-day window; ' + (f'about ${p["estimate_usd"]:,.2f} a run' if p.get('estimate_usd') is not None else 'no price on file'), finding_id=p['finding_id'], tone='warn')
    gift = dt.date(ends_on.year, 11, 1)
    if 0 <= (gift - ends_on).days <= horizon_days:
        fxg = next((m for m in (audit.web_pass(brand) or {}).get('markets') or [] if 'gift' in str(m.get('key') or '')), None)
        why = (fxg.get('drivers') or [''])[0] if fxg else 'the US holiday gift window; stock and the gift offer must be live before it'
        add(gift.isoformat(), 'window', 'The gift window opens', why, finding_id=f'{SCREEN}.PROD-R05.{fxg["key"]}' if fxg else None, tone='accent')
    items.sort(key=lambda i: (i['when'], i['kind'], i['title']))
    return {'ends_on': ends_on.isoformat(), 'horizon_days': horizon_days, 'items': items, 'overdue': sum(1 for i in items if i['days'] < 0), 'this_week': sum(1 for i in items if 0 <= i['days'] <= 7)}


# ---------------------------------------------------------------- the creative hand-off (round 5.4, room job: hand a validated angle and avatar to creative)

CREATIVE_RULES = ('PROD-R07', 'PROD-R08', 'PROD-R09', 'PROD-R10', 'PROD-R11', 'PROD-R35')
FRAME_THEME = {'buy it for life': 'durability', 'durab': 'durability', 'comfort': 'comfort', 'worth': 'price_value', 'value': 'price_value', 'fit': 'fit_sizing'}
PREFERENCE_THEME = {'durability': 'durability', 'natural_fibres': 'comfort', 'sustainability': 'mission', 'made_in_usa': 'mission', 'gifting': None, 'comfort': 'comfort', 'price_value': 'price_value'}
REVIEW_SOURCES = ('amazon', 'own_site', 'own_site_yotpo', 'trustpilot', 'retailer', 'amazon_customers_say')


def _theme_of(f, br):
    ent = f.get('entity') or {}
    rid = f.get('rule_id')
    if rid in ('PROD-R07', 'PROD-R35'):
        return ent.get('id') if ent.get('id') in audit.THEME_LABEL else None
    if rid == 'PROD-R11':
        return ent.get('theme')
    if rid == 'PROD-R10':
        rec = br.get((f.get('brain_refs') or [None])[0]) if br else None
        return audit.avatar_theme((rec or {}).get('value') or {}) if rec else None
    if rid == 'PROD-R09':
        frame = str(ent.get('frame') or '').lower()
        return next((th for k, th in FRAME_THEME.items() if k in frame), None)
    if rid == 'PROD-R08':
        return PREFERENCE_THEME.get(ent.get('id'))
    return None


def creative_handoff(brand, finding_id):
    """The angle brief creative builds on, for a buyer, theme, positioning or preference card: the angle, the buyer, the doubt,
    the proof on file, what buyers say (review sources only, never Reddit), the words to use, the do-not list, and the hand-off
    terms. Every line comes from the brain and this desk; nothing is invented."""
    r = rank(brand or 'sample', None)
    findings = {f['id']: f for f in audit.run(brand, {'ends_on': r['window']['ends_on']}, data=None if brand else sample_data())}
    f = findings.get(finding_id)
    if f is None:
        raise ValueError(f'no finding {finding_id}')
    if f.get('rule_id') not in CREATIVE_RULES:
        raise ValueError(f'{f.get("rule_id")} is not a creative hand-off rule; use the action brief')
    a = next((x for x in r['actions'] if finding_id in (x.get('finding_ids') or [])), None)
    br = audit.brain(brand) if brand else None
    theme = _theme_of(f, br)
    ent = f.get('entity') or {}
    na = 'unavailable'
    lines = [f'CREATIVE HAND-OFF: {(a or {}).get("title") or f["sentence"][:80]}', f'{brand or "sample"}, {r["window"]["ends_on"]}. From {finding_id}. Owner: {(a or {}).get("owner") or na}.', '',
             'THE ANGLE', f['sentence'], ((a or {}).get('why') or '') if not ((a or {}).get('why') or '').startswith(f['sentence'][:40]) else '', '', 'THE BUYER']
    avatars = []
    if br is not None:
        for rec in br.records('avatars'):
            v = rec.get('value') or {}
            if not v.get('name'):
                continue
            hit = (f.get('rule_id') in ('PROD-R10', 'PROD-R11') and (ent.get('label') == v['name'] or ent.get('id') == rec.get('field'))) or (theme and audit.avatar_theme(v) == theme)
            if hit:
                avatars.append(v)
    for v in avatars[:3]:
        lines.append(f'{v["name"]}' + (f' ({round((v.get("share_estimate") or 0) * 100)} percent of buyers, {v.get("intensity") or na} intensity)' if v.get('share_estimate') is not None else '') + f': {v.get("job") or na}.')
        lines.append(f'  Triggers: {", ".join(v.get("triggers") or []) or na}. Pains: {", ".join(v.get("pains") or []) or na}. Driver: {v.get("emotional_driver") or na}.')
    if not avatars:
        lines.append('No avatar in the brain carries this theme; creative builds on the doubt below.')
    lines += ['', 'THE DOUBT']
    rung = None
    if br is not None and theme:
        for rec in br.records('objection_ladders'):
            v = rec.get('value') or {}
            if audit.LADDER_THEME.get(v.get('theme')) != theme:
                continue
            rungs = v.get('rungs') or []
            rung = max(rungs, key=lambda g: ((g.get('counts') or {}).get('one_star') or 0)) if rungs else None
            lines.append(f'Theme: {audit.THEME_LABEL.get(theme, theme)}. Complaint quotes {(v.get("counts") or {}).get("one_star") or 0}, praise {(v.get("counts") or {}).get("five_star") or 0}.')
            for g in rungs:
                lines.append(f'  Rung {g.get("level")}: "{g.get("doubt")}" ({(g.get("counts") or {}).get("one_star") or 0} one-star) ' + ('proof on file' if g.get('proof') else 'no proof on file'))
            what_fails = v.get('what_fails') or []
            if what_fails:
                lines.append('  What fails: ' + '; '.join(str(x) for x in what_fails[:4]))
    if ent.get('doubt') and not rung:
        lines.append(f'"{ent["doubt"]}"')
    if len(lines) and lines[-1] == 'THE DOUBT':
        lines.append('No ladder maps to this card; the sentence above is the doubt.')
    lines += ['', 'THE PROOF ON FILE']
    proof = []
    if rung and rung.get('proof'):
        proof.append(f'Ladder proof: {rung["proof"]}')
    if br is not None:
        words = audit.ANSWER_WORDS.get(theme, []) if theme else []
        for sec in ('claims', 'identity', 'offers', 'policies'):
            for rec in br.records(sec):
                text = str(rec.get('text') or '')
                if words and any(w in text.lower() for w in words):
                    proof.append(f'{sec}, {rec.get("tier") or "tier unknown"}: {text}')
    lines += proof[:8] or ['No claim, policy or offer on file answers this theme. Ask the founder before any claim goes into copy.']
    lines += ['', 'WHAT BUYERS SAY (reviews only, never Reddit)']
    praise, complaint = [], []
    if br is not None:
        for rec in br.records('language_bank'):
            v = rec.get('value') or {}
            if v.get('subreddit'):
                continue
            revs = [x for x in v.get('reviews') or [] if x.get('source') in REVIEW_SOURCES]
            if not revs or (theme and theme not in (v.get('themes') or [])):
                continue
            q = (revs[0].get('quote') or v.get('phrase') or '').strip()
            if not q:
                continue
            item = f'"{q[:160]}" ({revs[0].get("source")}, {revs[0].get("star") or "star unknown"} star)'
            (praise if v.get('theme') == 'praise' else complaint).append(item)
    lines += ['Praise:'] + (praise[:4] or ['  none on file']) + ['Complaints:'] + (complaint[:4] or ['  none on file'])
    lines += ['', 'THE WORDS TO USE', 'Buyers say: ' + ('; '.join(p.split('"')[1][:60] for p in praise[:5]) if praise else na) + '.',
              'Answer words on this theme: ' + (', '.join(audit.ANSWER_WORDS.get(theme, [])) if theme else na) + '.',
              '', 'DO NOT', '- Quote a Reddit user, or any forum post, as a testimonial.', '- Name, show or copy a competitor: no logos, products, faces or text.',
              '- Make a claim that is not in the proof above; a doubt with no proof goes back to the founder.', '- Invent a number. Digits, short sentences, no jargon.',
              '', 'HAND-OFF']
    if a:
        lines += [f'Owner: {a.get("owner")}. Artefact: {(a.get("artefact") or {}).get("label") or (a.get("artefact") or {}).get("kind")}.', f'Win rule: {a.get("win_rule") or na}. Check on: {a.get("check_on") or na}.']
    return {'finding_id': finding_id, 'rule_id': f.get('rule_id'), 'theme': theme, 'title': (a or {}).get('title'), 'text': '\n'.join(lines), 'avatars': [v['name'] for v in avatars], 'quotes': len(praise) + len(complaint)}


# ---------------------------------------------------------------- the desk report (round 5.5)

def _n(rows, pred):
    return sum(1 for r in rows or [] if pred(r))


def desk_report(data, brand):
    """One markdown page: the plan (top 10 with owner, score and stake), the connect list, the parked list, what is due, and
    one gap line per desk block with its count. Every number is the desk's own; the page a founder pastes into a weekly note."""
    o = overview(data, brand)
    r = rank(brand or 'sample', None)
    cal = calendar_items(data, brand)
    d = o['desk']
    head = o['brand']
    open_acts = [a for a in r['actions'] if a.get('status') != 'unavailable']
    connect = [a for a in r['actions'] if a.get('status') == 'unavailable']
    money = lambda v: f'${v:,.0f}' if isinstance(v, (int, float)) else 'n/a'   # noqa: E731
    L = [f'# Research desk: {head.get("brand")}', f'{o["window"]["ends_on"]}, {len(open_acts)} open actions, {len(connect)} waiting on a source, {len(r.get("parked") or [])} parked. {head.get("simulated_note") or ""}', '',
         '## The plan, top 10']
    for i, a in enumerate(open_acts[:10], 1):
        L.append(f'{i}. {a["title"]} ({a.get("owner")}, {round((a.get("rubric") or {}).get("total") or 0)} of 100, stake {money((a.get("money_at_stake") or {}).get("usd"))}, check {a.get("check_on") or "n/a"})')
    if len(open_acts) > 10:
        L.append(f'... and {len(open_acts) - 10} more on the desk.')
    if connect:
        L += ['', '## Connect first'] + [f'- {a["title"]}' for a in connect]
    if r.get('parked'):
        L += ['', '## Parked'] + [f'- {a["title"]} (back {a.get("returns_on")}; {(a.get("decision") or {}).get("reason") or "no note"})' for a in r['parked']]
    L += ['', f'## Due: {cal["overdue"]} overdue, {cal["this_week"]} in 7 days, {len(cal["items"])} in {cal["horizon_days"]} days']
    L += [f'- {i["when"]}: {i["title"]}' for i in cal['items'][:12]]
    L += ['', '## The desk, block by block']
    rows = lambda k, key='rows': ((d.get(k) or {}).get(key) if isinstance(d.get(k), dict) else d.get(k)) or []   # noqa: E731
    lines = [
        ('Trends', f'{_n(rows("trends", "markets"), lambda m: m.get("verdict") == "gap")} market rows under-advertised of {len(rows("trends", "markets"))}' if (d.get('trends') or {}).get('on_file') else 'no web pass on file'),
        ('Lanes', f'{_n(rows("lanes"), lambda x: x.get("verdict") == "follow")} lanes to follow of {len(rows("lanes"))}'),
        ('Launch cadence', f'{_n(rows("cadence", "lanes"), lambda x: x.get("verdict") == "in_play")} lanes in play with none of ours; our cadence {((d.get("cadence") or {}).get("ours") or {}).get("n_12m", "n/a")} in 12 months'),
        ('Conversation', f'{_n(rows("conversation"), lambda x: x.get("verdict") == "gap")} themes complaint-led and unanswered of {len(rows("conversation"))}'),
        ('Surfaces', f'{_n(rows("surfaces"), lambda x: x.get("verdict") == "gap")} surfaces with reach and no presence'),
        ('Open questions', f'{_n(rows("questions"), lambda x: x.get("verdict") in ("never_asked", "overdue"))} questions wait on the founder'),
        ('Preferences', f'{_n(d.get("preferences") or [], lambda x: x.get("verdict") == "gap")} gaps, {_n(d.get("preferences") or [], lambda x: x.get("verdict") == "prove")} to prove'),
        ('Positioning', f'{len(rows("map", "frames"))} Reddit frames, {len(rows("map", "points"))} priced pages on the map'),
        ('Avatars', f'{_n(rows("avatars"), lambda x: x.get("verdict") in ("gap", "under"))} of {len(rows("avatars"))} avatars unserved or under-served'),
        ('Search', f'{len(rows("search", "groups"))} term groups; Search Console ' + ('connected' if (d.get("search") or {}).get("available") else 'not connected')),
        ('Falling behind', f'{len(rows("behind"))} items, stake {money((d.get("behind") or {}).get("stake_usd"))}'),
        ('Returns', f'{_n(rows("returns"), lambda x: x.get("verdict") == "high")} lines returning high' if not (d.get('returns') or {}).get('unavailable') else 'unavailable: ' + str((d.get('returns') or {}).get('reason'))),
        ('Pipeline', f'{(d.get("pipeline") or {}).get("open", 0)} open candidates, {(d.get("pipeline") or {}).get("over_box", 0)} past their box; hand-off {((d.get("pipeline") or {}).get("handoff") or {}).get("go", 0)} at go'),
        ('Margin gate', f'{_n(rows("margin"), lambda x: ((x.get("gate") or {}).get("verdict") == "fail"))} candidates below the floor of {len(rows("margin"))}'),
        ('First run', f'{_n(rows("first_runs"), lambda x: x.get("verdict") in ("no_plan", "full_moq_risk"))} candidates to size or de-risk'),
        ('Gates', f'{_n(rows("gates"), lambda x: x.get("passed") == x.get("of"))} candidates pass every gate of {len(rows("gates"))}'),
        ('Scorecard', ', '.join(f'{v} {k.replace("_", " ")}' for k, v in sorted(__import__("collections").Counter(x.get("verdict") for x in rows("scorecard")).items()))),
        ('Tech packs', f'{_n(rows("tech_packs"), lambda x: x.get("needs_spec") and x.get("status") != "current")} candidates need a spec'),
        ('Hours', f'{_n(rows("hours"), lambda x: (x.get("over_by") or 0) > 0)} candidates over their hours budget'),
        ('Video signals', f'{_n(rows("video"), lambda x: x.get("verdict") == "single")} candidate lanes on one platform only'),
        ('Trend checks', f'{_n(rows("trend_checks"), lambda x: x.get("candidates") and x.get("verdict") != "steady")} candidate lanes on a forecast or a spike'),
        ('Marketplace', (('the brand is not the seller of record; ' if ((d.get("marketplace") or {}).get("presence") or {}).get("sold_by_brand") is False else '') + f'{((d.get("marketplace") or {}).get("summary") or {}).get("spread_listings", 0)} listings off the site price') if (d.get('marketplace') or {}).get('presence') else 'no marketplace read'),
        ('Pulls', f'{_n(rows("pulls"), lambda x: x.get("verdict") != "fresh")} pulls not fresh of {len(rows("pulls"))}'),
    ]
    L += [f'- **{k}**: {v}.' for k, v in lines]
    L += ['', f'Rules: {len(audit.RULES)}. Findings: {sum(len(a.get("finding_ids") or []) for a in r["actions"])} across {len(r["actions"])} cards. Simulated sales; public reviews, ads and markets.']
    return {'brand': brand or 'sample', 'ends_on': o['window']['ends_on'], 'text': '\n'.join(L), 'blocks': len(lines)}


# ---------------------------------------------------------------- since you last looked (round 5.9)

SEEN_DIR = HERE / 'fixtures' / 'seen'


def _seen_path(brand):
    return SEEN_DIR / f'{brand or "sample"}.json'


def take_snapshot(data, brand, today):
    """Write what the desk shows now: every finding's severity, status and stake, keyed by id, so the next visit can say
    what is new, gone or changed. Taken only when a person clicks Mark as seen."""
    findings = audit.run(brand, None, data=data)
    doc = {'brand': brand or 'sample', 'taken_on': today.isoformat(), 'findings': {f['id']: {'severity': f.get('severity'), 'status': f.get('status'), 'stake_usd': (f.get('money_at_stake') or {}).get('usd'), 'sentence': f.get('sentence')} for f in findings}}
    p = _seen_path(brand)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(doc, indent=1), encoding='utf-8')
    return {'taken_on': doc['taken_on'], 'findings': len(doc['findings'])}


SEV = {'critical': 4, 'high': 3, 'medium': 2, 'low': 1}


def changes_since(data, brand):
    """The diff between the desk now and the last snapshot: new findings, gone findings, severity moved up or down, stake moved
    20 percent or more. No snapshot means nothing to compare, said so."""
    p = _seen_path(brand)
    now = {f['id']: f for f in audit.run(brand, None, data=data)}
    if not p.is_file():
        return {'available': False, 'reason': 'no snapshot yet; Mark as seen takes one', 'now': len(now)}
    doc = json.loads(p.read_text(encoding='utf-8'))
    then = doc.get('findings') or {}
    new = [{'id': i, 'sentence': f.get('sentence'), 'severity': f.get('severity')} for i, f in now.items() if i not in then]
    gone = [{'id': i, 'sentence': f.get('sentence'), 'severity': f.get('severity')} for i, f in then.items() if i not in now]
    worse, better, stake_moves = [], [], []
    for i, f in now.items():
        o = then.get(i)
        if not o:
            continue
        a, b = SEV.get(o.get('severity'), 0), SEV.get(f.get('severity'), 0)
        if b > a:
            worse.append({'id': i, 'from': o.get('severity'), 'to': f.get('severity'), 'sentence': f.get('sentence')})
        elif b < a:
            better.append({'id': i, 'from': o.get('severity'), 'to': f.get('severity'), 'sentence': f.get('sentence')})
        s0, s1 = o.get('stake_usd'), (f.get('money_at_stake') or {}).get('usd')
        if s0 and s1 and abs(s1 - s0) / s0 >= 0.2:
            stake_moves.append({'id': i, 'from': s0, 'to': s1, 'sentence': f.get('sentence')})
    return {'available': True, 'taken_on': doc.get('taken_on'), 'then': len(then), 'now': len(now), 'new': new, 'gone': gone, 'worse': worse, 'better': better, 'stake_moves': stake_moves,
            'quiet': not (new or gone or worse or better or stake_moves)}


# ---------------------------------------------------------------- founder answers written back (round 6.5)

ANSWER_SECTIONS = {'claim': 'claims', 'policy': 'policies', 'offer': 'offers'}


def answer_question(brand, body, today, brain=None):
    """The founder's answer to an open question, written back through the brain store: the answer becomes an approved,
    founder-sourced record in claims, policies or offers (kind), or a note that no proof exists (kind none); the question's
    record gets answered_on. Validation errors come back as 400; nothing is written when there are any."""
    if not brand:
        return 400, {'error': 'the sample brand has no brain to write to'}
    if not isinstance(body, dict):
        return 400, {'error': 'body must be an object'}
    qid = str(body.get('question_id') or '')
    answer = str(body.get('answer') or '').strip()[:600]
    kind = str(body.get('kind') or 'none')
    who = str(body.get('who') or 'founder').strip()[:40] or 'founder'
    if kind not in ('none', *ANSWER_SECTIONS):
        return 400, {'error': 'kind must be claim, policy, offer or none'}
    if not answer:
        return 400, {'error': 'answer is empty'}
    br = brain or audit.brain(brand)
    if br is None:
        return 400, {'error': f'no brain for {brand}'}
    q = br.get(qid)
    if not q or q.get('section') != 'open_questions':
        return 404, {'error': f'no open question {qid}'}
    field = q.get('field') or qid.split('.')[-1]
    written = []
    if kind != 'none':
        section = ANSWER_SECTIONS[kind]
        rec = {'id': f'{brand}.{section}.answer_{field}', 'brand': brand, 'section': section, 'field': f'answer_{field}', 'value': answer, 'text': answer,
               'source': {'type': 'founder', 'ref': f'{who}, research desk answer, {today.isoformat()}', 'captured_at': today.isoformat()},
               'confidence': 1.0, 'tier': 'approved', 'status': 'active', 'visibility': 'public', 'added_by': who,
               'notes': f'Answers the open question {qid}: {(q.get("value") or {}).get("question") or ""}'[:300]}
        errs = br.put(rec)
        if errs:
            return 400, {'error': 'the brain refused the record', 'details': errs}
        written.append(rec['id'])
    qv = dict(q.get('value') or {})
    qv['asked_on'] = qv.get('asked_on') or today.isoformat()
    qv['answered_on'] = today.isoformat()
    qv['answer'] = answer
    qv['answer_kind'] = kind
    keep = ('id', 'brand', 'section', 'field', 'value', 'text', 'source', 'confidence', 'tier', 'status', 'visibility', 'added_by', 'notes', 'evidence', 'expires_at', 'valid_from')
    qrec = {k: v for k, v in q.items() if k in keep}   # the store decorates a read record with dates the validator does not accept
    qrec['value'] = qv
    qrec['notes'] = (f'Answered by {who} on {today.isoformat()}: {answer}' if kind == 'none' else f'Answered by {who} on {today.isoformat()}; record {written[-1]}')[:300]
    errs = br.put(qrec)
    if errs:
        return 400, {'error': 'the brain refused the question update', 'details': errs}
    return 201, {'ok': True, 'question_id': qid, 'answered_on': today.isoformat(), 'written': written, 'kind': kind}


# ---------------------------------------------------------------- the week plan (round 6.7)

def week_plan(data, brand):
    """The next 7 days on this desk in one copyable list: what is due (from the calendar), the hours left in each open
    candidate's budget, the spend left under the weekly cap (from the ledger), and the pulls a person can approve this week
    within it. A Monday list; nothing here runs anything."""
    cal = calendar_items(data, brand, horizon_days=7)
    r = rank(brand or 'sample', None)
    ends_on = cal['ends_on']
    br = audit.brain(brand) if brand else None
    hours = audit.hours_table(brand or 'sample', br)
    hrs = [{'name': h.get('name'), 'stage': h.get('stage'), 'left': round((h.get('hours_allowed') or 0) - (h.get('hours_logged') or 0), 1)} for h in hours.get('rows') or [] if not h.get('closed')]
    pulls = audit.pulls(br, brand, dt.date.fromisoformat(ends_on)) if br is not None else {'rows': [], 'caps': None, 'ledger': None}
    lg = pulls.get('ledger') or {}
    cap = (pulls.get('caps') or {}).get('per_week_usd')
    spent = lg.get('spent_week_usd') if lg.get('available') else None
    left = round(cap - spent, 2) if cap is not None and spent is not None else None
    due_pulls = [p for p in pulls.get('rows') or [] if p.get('verdict') != 'fresh' or (p.get('next_due') and p['next_due'] <= (dt.date.fromisoformat(ends_on) + dt.timedelta(days=7)).isoformat())]
    affordable, budget = [], left if left is not None else (cap if cap is not None else None)
    for p in sorted(due_pulls, key=lambda x: (x.get('estimate_usd') is None, x.get('estimate_usd') or 0)):
        est = p.get('estimate_usd')
        if est is None:
            affordable.append(dict(p, fits=None))
        elif budget is not None and est <= budget:
            affordable.append(dict(p, fits=True))
            budget = round(budget - est, 2)
        else:
            affordable.append(dict(p, fits=False))
    top = [a for a in r['actions'] if a.get('status') != 'unavailable'][:5]
    lines = [f'WEEK PLAN, {ends_on} to {(dt.date.fromisoformat(ends_on) + dt.timedelta(days=7)).isoformat()}: {brand or "sample"}', '',
             f'DUE ({cal["overdue"]} overdue, {cal["this_week"]} this week)'] + [f'- {i["when"]}: {i["title"]}' + (f' ({i["text"]})' if i.get('text') else '') for i in cal['items']] or ['- nothing dated']
    lines += ['', 'THE TOP 5 THIS WEEK'] + [f'- {a["title"]} ({a.get("owner")}, check {a.get("check_on") or "n/a"})' for a in top]
    lines += ['', 'HOURS LEFT IN THE RESEARCH BUDGET'] + ([f'- {h["name"]} ({h["stage"]}): {h["left"]} h' + (' (over)' if h['left'] < 0 else '') for h in hrs] or ['- no open candidate'])
    lines += ['', 'SPEND THIS WEEK'] + [(f'- ${spent:,.2f} of ${cap:,.2f} spent, ${left:,.2f} left' if left is not None else '- ledger or cap unavailable') + (f'; {lg.get("over_bound_week")} run(s) settled over their bound' if lg.get('over_bound_week') else '')]
    lines += ['', 'PULLS A PERSON CAN APPROVE THIS WEEK'] + ([f'- {p["label"]}: {p["verdict"]}' + (f', about ${p["estimate_usd"]:,.2f}' if p.get('estimate_usd') is not None else ', no price on file') + ({True: ' (fits the cap)', False: ' (does not fit this week)', None: ''}[p['fits']]) + (f'; {p["command"]}' if p.get('command') else '') for p in affordable] or ['- every pull is fresh'])
    return {'brand': brand or 'sample', 'from': ends_on, 'text': '\n'.join(lines), 'due': cal['items'], 'hours': hrs, 'spend': {'cap': cap, 'spent': spent, 'left': left}, 'pulls': [{k: p.get(k) for k in ('key', 'label', 'verdict', 'estimate_usd', 'fits')} for p in affordable], 'top': [a['title'] for a in top]}


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
        data = None if brand else (req.data if getattr(req, 'data', None) is not None else sample_data())   # the sample brand reads the server's data, or its own reader
        if brand:
            audit.brand_data(brand)  # ValueError for an unknown brand
        if req.method == 'POST':
            today = audit.last_full_day(data, brand) + dt.timedelta(days=1)
            if req.path == ['snapshot']:
                return 201, take_snapshot(data, brand, today)
            if req.path == ['answers']:
                return answer_question(brand, req.body, today)
            if req.path == ['candidates']:
                return candidate_add(brand or 'sample', req.body, today)
            if len(req.path) == 2 and req.path[0] == 'candidates':
                return candidate_update(brand or 'sample', req.path[1], req.body, today)
            return 405, {'error': 'read only, except the candidate pipeline, the seen snapshot and a founder answer'}
        if req.path == ['overview']:
            return overview(data, brand)
        if req.path == ['findings']:
            return {'findings': audit.run(brand, None, data=data), 'rules': audit.RULES}
        if len(req.path) == 3 and req.path[0] == 'candidates' and req.path[2] == 'brief':
            return candidate_brief(data, brand, req.path[1])
        if req.path == ['product_candidates']:
            return {'table': 'product_candidates', 'brand': brand or 'sample', 'rows': handoff_rows(brand or 'sample'), 'file': str(HANDOFF_PATH.relative_to(APP.parent))}
        if req.path == ['tests']:
            return {'rows': proposed_tests(brand or 'sample'), 'file': str(TESTS_PATH.relative_to(APP.parent))}
        if len(req.path) == 2 and req.path[0] == 'handoff':
            return creative_handoff(brand, req.path[1])
        if req.path == ['changes']:
            return changes_since(data, brand)
        if req.path == ['report']:
            return desk_report(data, brand)
        if req.path == ['log']:
            return audit.research_log(brand or 'sample')
        if req.path == ['week']:
            return week_plan(data, brand)
        if req.path == ['calendar']:
            return calendar_items(data, brand)
        if req.path == ['parked']:
            r = rank(brand or 'sample', None)
            return {'parked': r['parked'], 'decided': r['decided'], 'snooze_days': rank_mod.SNOOZE_DAYS, 'window': r['window']}
    except ValueError as exc:
        return 400, {'error': str(exc)}
    return 404, {'error': 'not found', 'routes': ['overview', 'findings', 'rank', 'parked', 'calendar', 'week', 'report', 'changes', 'log', 'candidates/<id>/brief', 'handoff/<finding_id>', 'product_candidates', 'tests']}
