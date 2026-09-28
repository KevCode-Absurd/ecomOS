"""Rank for screen 04 (depth.md section 5): every audit finding becomes an action a person can approve today.

`rank(brand, window)` runs audit.run, starts each action from app/rank.py's default (rubric, owner, capability),
then a builder per rule writes the real title, owner, steps with who, the artefact with its drafted text, the
size, the win and stop rules and the check date. Unavailable findings keep rank.py's connect action. No model call;
same tables, brain and window give the same actions in the same order.
"""
import importlib.util
import json
import math
import sys
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parents[1]
SCREEN = '04-offers-pricing'


def _load(name, path):
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


audit = _load('offers_pricing_audit_mod', HERE / 'audit.py')
model = _load('offers_pricing_model', HERE / 'model.py')
playbook = _load('offers_pricing_playbook', HERE / 'playbook.py')
RANK = _load('ecomos_rank', APP / 'rank.py')
FIXTURES = HERE / 'fixtures'


def money(v, digits=None):
    if v is None:
        return 'unavailable'
    if digits is None:
        digits = 0 if abs(v) >= 1000 else 2
    return f'${v:,.{digits}f}'


def pct(v, digits=1):
    return 'unavailable' if v is None else f'{v * 100:.{digits}f} percent'


def step(n, who, text):
    return {'n': n, 'who': who, 'text': text}


def steps(*rows):
    return [step(i + 1, who, text) for i, (who, text) in enumerate(rows)]


# ---------------------------------------------------------------- context shared by the builders

class Ctx:
    """Numbers several builders need, computed once per rank call."""

    def __init__(self, rd):
        self.rd = rd
        self.end = rd.ends_on
        self.threshold, _ = audit.threshold_usd(rd)
        self.be = audit.break_even(rd, self.end)
        self.contribution = model.contribution_28d(rd)
        self.totals = model.window_totals(rd)
        self.po = model.per_order(self.totals)
        self.objections = objection_map(rd)
        self.ladder, self.ladder_rows = audit.ladder_moves(rd)
        self.first_order = audit.first_order(rd)
        self.waterfalls = audit.offer_waterfalls(rd, self.objections)
        self.calendar = audit.promo_calendar(rd)
        self.gifting = audit.gifting(rd)
        self.ship_rate = (model.brain_value(rd, 'offers.standard_shipping_cost')[0] or {}).get('cost_usd') if rd.brand else None
        self.scenarios = (model.threshold_scenarios(rd, self.threshold, self.ship_rate, self.be['value'], (self.po or {}).get('units') or 1)
                          if self.threshold is not None and self.be.get('value') is not None else [])

    def check_on(self, days):
        return (self.end + timedelta(days=days)).isoformat()


# ---------------------------------------------------------------- builders, one per rule

def threshold_action(f, a, ctx):
    t, be = ctx.threshold, ctx.be
    new = math.ceil(be['value'] / 5) * 5
    stake = f.get('money_at_stake')
    size = (f'{money(stake["usd"])} of labels in 28 days on orders from ${t:,.0f} to ${be["value"]:,.2f}' if stake else
            f'Label cost on orders from ${t:,.0f} to ${be["value"]:,.2f} is unavailable until order rows connect')
    sc = next((x for x in ctx.scenarios if x['threshold'] == new), {})
    brief = '\n'.join([
        f'Test brief: free shipping at ${new} against ${t:,.0f}',
        f'Why: break-even is ${be["value"]:,.2f} (AOV {money(be["aov"])} plus the {money(be["label"])} label over a '
        f'{be["gross_margin"] * 100:.0f} percent margin). Every free order under it ships at a loss on the label.',
        f'Arms: A keeps ${t:,.0f}. B moves the line to ${new}. Same cart bar, same copy, only the number changes.',
        'Split: 50/50 by visitor, new and returning, all devices, 28 days.',
        (f'The bar B must clear: {sc["text"]} The rest pay the {money(ctx.ship_rate)} rate or add an item.'
         if sc.get('limit') is not None else 'The walk-away limit is unavailable: contribution inputs are missing.'),
        'Primary metric: contribution per visitor (net minus landed cost, label, pick and pack, fees).',
        'Guard: conversion rate by arm, AOV by arm, share of orders in the $10 under each line.',
        'Win: contribution per visitor up in B with conversion down less than 3 percent relative.',
        'Stop: conversion in B down more than 5 percent relative for 7 days in a row.',
    ])
    a.update({
        'title': f'Test free shipping at ${new} against ${t:,.0f}',
        'why': f['sentence'] + f' Break-even is AOV {money(be["aov"])} plus the {money(be["label"])} label over a '
               f'{be["gross_margin"] * 100:.0f} percent margin.' + (f' ${new} {sc["text"][0].lower()}{sc["text"][1:]}' if sc.get('limit') is not None else ''),
        'owner': 'agent_drafts',
        'artefact': {'kind': 'test_brief', 'label': f'Test brief: free shipping at ${new} against ${t:,.0f}', 'draft': brief},
        'steps': steps(
            ('agent', f'Count orders from ${t:,.0f} to ${new} in the last 28 days and the label they cost.'),
            ('agent', 'Draft the test brief and the cart bar line for both arms.'),
            ('person', 'Approve the brief. Set arm B in the shipping rates app. Nothing changes before that.'),
            ('agent', 'Read conversion, AOV and contribution per visitor by arm every 7 days.'),
            ('agent', f'Call the test on {ctx.check_on(35)} with the win and stop rules.')),
        'size': {'text': size, 'usd': stake['usd'] if stake else None},
        'win_rule': 'Contribution per visitor up in B, conversion down less than 3 percent relative.',
        'stop_rule': 'Conversion in B down more than 5 percent relative for 7 days in a row.',
        'check_on': ctx.check_on(35), 'time_to_ship_hours': 4,
    })
    return a


def planned_rate(rd, rate_key):
    """The planned claim rate from a brain record (percent of orders), as a ratio, with its record id."""
    if not rate_key:
        return None, None
    key, field = rate_key
    val, rec = model.brain_value(rd, key)
    v = val.get(field) if isinstance(val, dict) else None
    return (v / 100, rec['id']) if isinstance(v, (int, float)) else (None, None)


def objection_map(rd):
    """Every deal-breaker rung (top rung of each ladder) with the offer or proof that answers it, what in the brain
    already covers it, the cost of one claim from finance_inputs, and the returns behind it where they exist."""
    windows = audit.returns_windows(rd)
    rows = []
    for r in audit.ladder_rungs(rd):
        pb = playbook.offer_for(r['theme'])
        covered = []
        for key in pb['covers']:
            rec = rd.record(f'{rd.brand}.{key}') if rd.brand else None
            if rec:
                covered.append({'id': rec['id'], 'text': rec.get('text'), 'source': (rec.get('source') or {}).get('ref')})
        cost = model.claim_cost(rd, pb['cost'])
        rate, rate_id = planned_rate(rd, pb['rate_key'])
        per_1000 = round(cost['value'] * rate * 1000, 2) if cost.get('value') is not None and rate is not None else None
        st = audit.reason_stats(windows, r['reasons'])
        if st is None:
            ret = {'per_1000': None, 'reason': 'no return reason maps to this doubt'}
        elif st.get('unavailable'):
            ret = {'per_1000': None, 'reason': st['reason'], 'fix': st.get('fix')}
        else:
            ret = {'per_1000': round(st['rate'] * 1000, 2) if st['rate'] is not None else None,
                   'median_per_1000': round(st['median'] * 1000, 2) if st['median'] is not None else None}
        ret['reasons'] = r['reasons']
        theme = (r['theme'] or '').replace('_', ' ')
        row = {'theme': theme, 'theme_key': r['theme'], 'ladder': r['ladder'], 'rung': f'{r["level"]} of {r["levels"]}',
               'doubt': r['doubt'], 'one_star': r['one_star'], 'answered': r['proof'] is not None, 'proof': r['proof'],
               'offer': pb['name'], 'gets': pb['gets'], 'kind': pb['kind'], 'where': pb['where'], 'claim': pb['cost'],
               'covered_by': covered, 'cost_per_claim': cost.get('value'), 'cost_parts': cost.get('parts'),
               'cost_reason': cost.get('reason'), 'planned_rate': rate, 'rate_source': rate_id,
               'cost_per_1000_orders': per_1000, 'returns': ret, 'sources': r.get('sources')}
        row['spec'] = offer_spec(row)
        rows.append(row)
    return rows


def offer_spec(row):
    """The drafted spec for one rung: what the shopper gets, what already covers it, where it shows, what it costs."""
    lines = [f'{"Offer" if row["kind"] == "offer" else "Proof"} spec: {row["offer"]}',
             f'Answers: "{row["doubt"]}" ({row["one_star"]} one-star mentions, rung {row["rung"]} of the {row["theme"]} ladder).',
             f'What the shopper gets: {row["gets"]}']
    if row['covered_by']:
        lines.append('Already true in policy, not said where the doubt is: ' + ' '.join(c['text'] for c in row['covered_by'] if c['text']))
    else:
        lines.append('Nothing in the brain covers it yet. The founder sets the terms.')
    lines.append(f'Where it shows: {row["where"]}.')
    if row['claim'] == 'none':
        lines.append('Cost: none per order. It is proof, not a new promise.')
    elif row['cost_per_claim'] is None:
        lines.append(f'Cost per claim: unavailable, {row["cost_reason"]}.')
    else:
        parts = ', '.join(f'{p["label"]} {money(p["value"])}' for p in row['cost_parts'])
        lines.append(f'Cost per claim: {money(row["cost_per_claim"])} ({parts}).')
        if row['cost_per_1000_orders'] is not None:
            lines.append(f'At the planned {row["planned_rate"] * 100:.1f} percent claim rate: {money(row["cost_per_1000_orders"])} '
                         f'per 1,000 orders. That rate covers all causes, so it is a ceiling for this doubt.')
        else:
            lines.append('Claim rate: unavailable until returns by reason connect. Cap it in the test at 2 percent of orders.')
    lines.append('Stop: claims above 2 times the planned rate for 2 weeks, or margin per order under the red line.')
    return '\n'.join(lines)


def rung_action(f, a, ctx):
    theme_key = f['entity']['id'].split('.')[0]
    row = next((r for r in ctx.objections if r['theme_key'] == theme_key), None)
    doubt = row['doubt'] if row else f['entity']['label'].split(': ', 1)[-1]
    if not row:
        return a
    kind = row['kind']
    who_ships = {'offer': 'Add the promise line to the product page, the cart and the ads that meet this doubt.',
                 'page_section': 'Add the section to the product page price block.',
                 'listing_fix': 'Update the marketplace title, first image and first bullet.'}[kind]
    size = (f'{money(row["cost_per_1000_orders"])} per 1,000 orders at the planned claim rate' if row['cost_per_1000_orders'] is not None
            else f'{money(row["cost_per_claim"])} per claim' if row['cost_per_claim'] else 'no cost per order')
    a.update({
        'title': f'Launch "{row["offer"].split(":")[0]}" to answer "{doubt}"',
        'why': f['sentence'] + (' The policy already covers it but the page does not say so.' if row['covered_by'] and kind == 'offer' else ''),
        'owner': 'agent_drafts',
        'artefact': {'kind': kind, 'label': row['offer'], 'draft': row['spec']},
        'steps': steps(
            ('agent', f'Pull the {row["one_star"]} one-star quotes and the returns behind "{doubt}".'),
            ('agent', 'Draft the spec and the one-line promise, priced from finance inputs.'),
            ('person', 'Approve the terms and the cost per claim. Nothing ships before that.'),
            ('agent', who_ships),
            ('agent', f'Read claims and add to cart rate every 7 days; call it on {ctx.check_on(42)}.')),
        'size': {'text': size, 'usd': None},
        'win_rule': 'Add to cart rate on the product page up, and returns for this doubt not up more than 10 percent.',
        'stop_rule': 'Claims above 2 times the planned rate for 2 weeks, or margin per order under the red line.',
        'check_on': ctx.check_on(42), 'time_to_ship_hours': 6 if kind == 'offer' else 3,
    })
    return a


def first_order_action(f, a, ctx):
    fo = ctx.first_order
    code = next(r for r in fo['rows'] if r['key'] == 'code')
    best = max((r for r in fo['rows'] if not r.get('unavailable') and r['keeps_price']), key=lambda r: r['contribution'])
    under = (f' It also takes the average basket from {money(fo["gross_order"])} to {money(code["price_paid"])}, under the '
             f'${fo["threshold"]:,.0f} line, so the shopper pays shipping or adds an item.') if code['under_line'] else ''
    brief = '\n'.join([
        f'Test brief: {best["name"].lower()} against the {fo["code_pct"]:.0f} percent code',
        f'Why: the code keeps {money(code["contribution"])} per first order; {best["terms"]} keeps {money(best["contribution"])}. '
        f'Paid media per new customer is {money(fo["new_cac"])}, so payback moves from {code["payback"]:.2f}x to {best["payback"]:.2f}x.' + under,
        f'Arms: A keeps the code in ads and on the site. B swaps it for: {best["terms"]}. Same creative, only the offer line changes.',
        'Split: 50/50 by visitor on new visitors; ad variants in pairs so each ad runs both offers.',
        'Primary metric: first-order contribution per new visitor.',
        f'The bar B must clear: it can lose up to {best["cvr_limit"] * 100:.0f} percent of first-order conversion and still earn more per visitor.',
        f'Win: contribution per new visitor up in B. Stop: new-customer conversion in B down more than {best["cvr_limit"] * 100:.0f} percent for 7 days.',
    ])
    a.update({
        'title': f'Test {best["name"].lower()} against the {fo["code_pct"]:.0f} percent first-order code',
        'why': f['sentence'] + under,
        'owner': 'agent_drafts',
        'artefact': {'kind': 'test_brief', 'label': f'Test brief and ad variants: {best["name"].lower()} against the code', 'draft': brief},
        'steps': steps(
            ('agent', 'List the active ads that carry the code and the site places it shows.'),
            ('agent', 'Draft the test brief and one offer-line variant per ad.'),
            ('person', 'Approve the offer and the variants. The media buyer launches the pairs.'),
            ('agent', 'Read first-order conversion and contribution per new visitor by arm every 7 days.'),
            ('agent', f'Call it on {ctx.check_on(35)} with the win and stop rules.')),
        'size': {'text': (f'Up to {money(f["money_at_stake"]["usd"])} in 28 days at equal conversion' if f.get('money_at_stake') else
                          f'{money(code["cost"] - best["cost"])} more kept per first order'), 'usd': (f.get('money_at_stake') or {}).get('usd')},
        'win_rule': 'Contribution per new visitor up in B.',
        'stop_rule': f'New-customer conversion in B down more than {best["cvr_limit"] * 100:.0f} percent for 7 days.',
        'check_on': ctx.check_on(35), 'time_to_ship_hours': 6,
    })
    return a


def promo_action(f, a, ctx):
    key = f['entity']['id'][len('window_'):]
    w = next((x for x in ctx.calendar if x['key'] == key), None)
    if not w:
        return a
    ly = w['last_year'] or {}
    start = date.fromisoformat(w['start'])
    approve = date.fromisoformat(w['approve_by'])
    d = lambda x: x.isoformat()
    lines = [f'Offer spec: {w["name"]}, {w["start"]} to {w["end"]}',
             f'Approve by {w["approve_by"]}. Creative and email briefs by {d(approve + timedelta(days=7))}. '
             f'Site and emails loaded by {d(start - timedelta(days=7))}.',
             f'Default offer for this window: {w["offer"]}']
    if ly:
        lines.append(f'Last year ({ly["start"]} to {ly["end"]}): net sales {ly["lift"] * 100:.0f} percent above the 28 days before, '
                     f'discounts {ly["depth"] * 100:.1f} percent of gross against {ly["baseline_depth"] * 100:.1f} percent before.')
        po = ctx.po
        cr = model.cogs_ratio(ctx.rd)
        if po and cr.get('ratio') is not None:
            cogs = cr['ratio'] * po['net']
            at_last = model.waterfall(ctx.rd, po['gross'], po['gross'] * ly['depth'], cogs, po['units'], ships_free=True, media=0)
            at_base = model.waterfall(ctx.rd, po['gross'], po['discount'], cogs, po['units'], ships_free=True, media=0)
            if at_last['before_media'] is not None and at_base['before_media'] is not None:
                lines.append(f'Margin check: at last year\'s depth the average order keeps {money(at_last["before_media"])} before media, '
                             f'against {money(at_base["before_media"])} at the last 28 days\' depth. Cap the depth at last year\'s.')
    lines += ['Win: net sales in the window at or above last year with discount depth at or below last year.',
              'Stop: pull the offer early if margin per order before media falls under the red line for 2 days.']
    a.update({
        'title': f'Build the {w["name"]} offer by {w["approve_by"]}',
        'owner': 'agent_drafts',
        'artefact': {'kind': 'offer', 'label': f'{w["name"]} offer spec with dates', 'draft': '\n'.join(lines)},
        'steps': steps(
            ('agent', f'Pull last year\'s {w["name"]} numbers and the pack and gift lines in stock.'),
            ('agent', 'Draft the offer spec, the margin check and the dated prep plan.'),
            ('person', f'Approve the offer by {w["approve_by"]}. Nothing ships before that.'),
            ('agent', f'Draft the ad, email and site banner briefs by {d(approve + timedelta(days=7))}.'),
            ('person', f'Load the site and emails by {d(start - timedelta(days=7))}. Check stock on the offer lines.'),
            ('agent', f'Read sales and depth daily in the window; report on {d(date.fromisoformat(w["end"]) + timedelta(days=3))}.')),
        'size': {'text': (f'{money(f["money_at_stake"]["usd_revenue"])} of net sales rode on this window last year'
                          if f.get('money_at_stake') else 'last year unavailable'), 'usd': (f.get('money_at_stake') or {}).get('usd')},
        'win_rule': 'Net sales in the window at or above last year, discount depth at or below last year.',
        'stop_rule': 'Margin per order before media under the red line for 2 days in the window.',
        'check_on': w['approve_by'], 'time_to_ship_hours': 12,
    })
    return a


def gifting_page(ctx, w=None):
    """The holiday gifting landing page spec, drafted from the brain and the data."""
    g, pb = ctx.gifting, playbook
    rows = {r['line']: r for r in ctx.ladder.get('rows', [])} if not ctx.ladder.get('unavailable') else {}
    boxes = [r for r in ctx.ladder.get('rows', []) if (r.get('pack') or 0) >= pb.GIFT_PACK_MIN]
    boxes.sort(key=lambda r: -r['revenue'])
    card = g.get('gift_card') or {}
    lines = [f'Landing page spec: holiday gifts' + (f', live {w["start"]} to {w["end"]}' if w else '')]
    lines.append('1. Hero: the gift boxes, the price, and the order-by date for arrival by ' + g['gift_day'] + '.')
    if boxes:
        lines.append('2. Gift boxes: ' + '; '.join(f'{r["sku"]} ({r["pack"]} items) at {money(r["price_per_pack"])}' for r in boxes[:4]) + '.')
    else:
        lines.append('2. Gift boxes: no pack of ' + str(pb.GIFT_PACK_MIN) + ' or more in the catalogue; the pack offer adds one.')
    if card.get('denominations_usd'):
        d = card['denominations_usd']
        lines.append(f'3. Gift card: {card.get("name") or "digital gift card"}, ${min(d)} to ${max(d)}, delivered by email, the last-minute answer.')
    if g.get('program'):
        lines.append(f'4. Bulk and corporate gifting: {g["program"]}. Link: {g.get("program_source") or "the bulk gifting page"}.')
    ship = '; '.join(f'{o["name"]} order by {o["order_by"]}' for o in g['ship_by'] if o['order_by'])
    if ship:
        lines.append(f'5. Order-by dates for {g["gift_day"]}: {ship}. Show them in the header bar and the cart.')
    lines.append('6. Proof: the guarantee line and the review count under each box.')
    lines.append('Win: gift box share of revenue in the window above the store share; gift card sales up on last year.')
    lines.append('Stop: none. Pull the order-by bar the day after the last date.')
    return '\n'.join(lines)


def gifting_action(f, a, ctx):
    a.update({
        'title': 'Build the holiday gifting page and push the gift boxes',
        'owner': 'agent_drafts',
        'artefact': {'kind': 'landing_page', 'label': 'Holiday gifting landing page spec', 'draft': gifting_page(ctx)},
        'steps': steps(('agent', 'Pick the gift boxes and pull their price and reviews.'),
                       ('agent', 'Draft the page, the order-by bar and 3 ad briefs for the gift boxes.'),
                       ('person', 'Approve the page. The site team builds it.'),
                       ('agent', 'Read gift box share of revenue weekly through the window.')),
        'win_rule': 'Gift box share of revenue in the window above the store share.', 'stop_rule': 'Pull the order-by bar after the last date.',
        'check_on': ctx.check_on(28), 'time_to_ship_hours': 12})
    return a


def merge_gifting(actions, ctx):
    """When the holiday gifting window is due, the gifting finding rides on its action and the page is its artefact."""
    hol = next((a for a in actions if a.get('rule_id') == 'OFFER-R11' and a['entity']['id'] == 'window_holiday_gifting'), None)
    if not hol:
        return actions
    w = next((x for x in ctx.calendar if x['key'] == 'holiday_gifting'), None)
    hol['title'] = f'Build the holiday gifting page and offer by {w["approve_by"]}' if w else hol['title']
    hol['steps'][1] = step(2, 'agent', 'Draft the offer spec, the gifting landing page, the order-by bar and the margin check.')
    hol['artefact'] = {'kind': 'landing_page', 'label': 'Holiday gifting landing page and offer spec',
                       'draft': hol['artefact']['draft'] + '\n\n' + gifting_page(ctx, w)}
    keep = []
    for a in actions:
        if a.get('rule_id') == 'OFFER-R12':
            hol['finding_ids'] = hol['finding_ids'] + a['finding_ids']
            hol['why'] = hol['why'] + ' ' + a['why']
            continue
        keep.append(a)
    return keep


def returns_block(rd):
    """returns_by_reason for the window, or the labelled fixture when the metric is unavailable."""
    m = rd.m('returns_by_reason', audit.WINDOW)
    if not m.get('unavailable'):
        orders = m['inputs']['paid_orders']
        return {'unavailable': False, 'fixture': False, 'window': m['window'], 'paid_orders': orders,
                'groups': [dict(g, per_1000=round(g['returns'] / orders * 1000, 2) if orders else None) for g in m['groups']]}
    fx = json.loads((FIXTURES / 'returns_by_reason.json').read_text(encoding='utf-8'))
    orders = fx['inputs']['paid_orders']
    return {'unavailable': True, 'reason': m.get('reason'), 'fix': m.get('fix'), 'fixture': True, 'fixture_note': fx['note'],
            'groups': [dict(g, per_1000=round(g['returns'] / orders * 1000, 2)) for g in fx['groups']]}


def ladder_group_action(members, rows, verdict, ctx):
    """One action for every line that shares a pack ladder verdict (push, deepen or add)."""
    by = {r['line']: r for r in rows}
    lines = [by[m['entity']['id']] for m in members if m['entity']['id'] in by]
    lines.sort(key=lambda r: -r['revenue'])
    best = max(members, key=lambda m: m['rubric']['total'])
    a = dict(best)
    n = len(lines)
    a.update({'id': f'{SCREEN}.{best["rule_id"]}.{verdict}', 'finding_ids': [m['id'] for m in members],
              'severity': min((m['severity'] for m in members), key=lambda s: RANK.SEV_ORDER.get(s, 9)),
              'entity': {'type': 'sku', 'id': verdict, 'label': f'{n} product lines'}})
    if verdict == 'push':
        body = [f'- {r["line"]}: single {money(r["single_per_item"])} an item, {r["pack"]}-pack {money(r["pack_per_item"])} '
                f'({r["saving"] * 100:.1f} percent off). Singles {r["single_share"] * 100:.0f} percent of packs. '
                f'Each trade-up adds {money(r["gain_per_trade_up"])} margin.' for r in lines]
        worst = max(lines, key=lambda r: r['trade_up_needed'] or 0)
        draft = '\n'.join(['Page spec: preselect the pack and show price per item', 'Lines, 12 full months:'] + body + [
            f'Why not a deeper price: on {worst["line"]} a 15 percent saving gives {money(worst["give_away_12m"])} a year to '
            f'shoppers who already buy the pack; {worst["trade_up_needed"] * 100:.0f} percent of single buyers would have to trade up to pay for it.',
            'Page: preselect the pack. Show the price per item under each option. Add "Save N percent an item" on the pack.',
            'Ads: one ad per line that leads with the pack price per item.',
            'Win: single share of packs down 5 points in 28 days and margin per order up.',
            'Stop: product page conversion down more than 3 percent relative for 7 days.'])
        a.update({'title': f'Preselect the pack and show price per item on {n} lines',
                  'why': f'Singles are {min(r["single_share"] for r in lines) * 100:.0f} to {max(r["single_share"] for r in lines) * 100:.0f} '
                         f'percent of packs on these lines. A deeper pack price would give away more than it wins, so move shoppers with the page.',
                  'owner': 'agent_drafts',
                  'artefact': {'kind': 'page_section', 'label': f'Pack selector spec for {n} product pages, plus {n} ad briefs', 'draft': draft},
                  'steps': steps(('agent', 'Pull each line\'s pack sales and margin per pack for 12 months.'),
                                 ('agent', 'Draft the pack selector: pack preselected, price per item under each option.'),
                                 ('agent', 'Draft one ad brief per line that leads with the pack price per item.'),
                                 ('person', 'Approve the page spec and the briefs. The site team ships the selector.'),
                                 ('agent', f'Read single share of packs and margin per order weekly; call it on {ctx.check_on(35)}.')),
                  'size': {'text': 'Each shopper who moves from a single to the pack adds '
                                   f'{money(min(r["gain_per_trade_up"] for r in lines))} to {money(max(r["gain_per_trade_up"] for r in lines))} margin', 'usd': None},
                  'win_rule': 'Single share of packs down 5 points in 28 days and margin per order up.',
                  'stop_rule': 'Product page conversion down more than 3 percent relative for 7 days.',
                  'check_on': ctx.check_on(35), 'time_to_ship_hours': 8})
    elif verdict == 'deepen':
        body = [f'- {r["line"]}: {r["pack"]}-pack from {money(r["pack_price"])} to {money(r["test_price"])} '
                f'(15 percent off per item). Gives {money(r["give_away_12m"])} a year to current pack buyers. Each trade-up adds '
                f'{money(r["gain_per_trade_up_at_test"])}. Pays when {r["trade_up_needed"] * 100:.0f} percent of single buyers trade up.' for r in lines]
        draft = '\n'.join(['Test brief: a deeper pack price', 'Lines, 12 full months:'] + body + [
            'Arms: A keeps today\'s pack price. B shows the test price. 50/50 by visitor, 28 days.',
            'Win: trade-ups in B pass the pay-back share above, measured as single orders that became pack orders.',
            'Stop: margin per order in B down more than 5 percent for 7 days.'])
        a.update({'title': f'Test a deeper pack price on {n} line' + ('s' if n > 1 else ''),
                  'why': ' '.join(m['why'] for m in members[:2]) + ' The price cut pays back if enough singles trade up.',
                  'owner': 'agent_drafts',
                  'artefact': {'kind': 'price_change', 'label': 'Pack price test brief', 'draft': draft},
                  'steps': steps(('agent', 'Confirm the pack and single sales and cost per pack for 12 months.'),
                                 ('agent', 'Draft the test brief with the pay-back share.'),
                                 ('person', 'Approve the test price. Set arm B in the store.'),
                                 ('agent', f'Read trade-ups and margin per order weekly; call it on {ctx.check_on(35)}.')),
                  'size': {'text': f'{money(sum(r["give_away_12m"] for r in lines))} a year given to pack buyers if it ships without enough trade-ups', 'usd': None},
                  'win_rule': 'Trade-ups pass the pay-back share.', 'stop_rule': 'Margin per order in B down more than 5 percent for 7 days.',
                  'check_on': ctx.check_on(35), 'time_to_ship_hours': 4})
    else:
        body = [f'- {r["line"]} ({r["category"]}): a {r["new_pack"]}-pack at {money(r["new_price"])} '
                f'({money(r["single_per_item"] * 0.9)} an item, 10 percent off). Margin per pack {money(r["new_margin"])} against '
                f'{money(r["single_margin"])} on a single. Each trade-up adds {money(r["gain_per_trade_up"])}.' for r in lines]
        draft = '\n'.join(['Offer spec: add a multi-pack to lines sold only as singles', 'Lines, 12 full months:'] + body + [
            'Where: the product page pack selector, the cart upsell, one ad per line.',
            'Win: pack takes 20 percent of the line\'s packs in 56 days with margin per order up.',
            'Stop: line revenue down for 4 weeks after launch.'])
        a.update({'title': f'Add a multi-pack to {n} basics lines sold only as singles',
                  'why': f'{n} lines in repeat-buy categories sell {sum(r["single_packs"] for r in lines):,} singles a year and no pack.',
                  'owner': 'agent_drafts',
                  'artefact': {'kind': 'offer', 'label': f'Pack offer spec for {n} lines', 'draft': draft},
                  'steps': steps(('agent', 'Confirm single sales and landed cost per item for each line.'),
                                 ('agent', 'Draft the pack spec, price and page copy for each line.'),
                                 ('person', 'Approve the packs and prices. Ops creates the SKUs.'),
                                 ('agent', 'Add the packs to the selector, the cart upsell and one ad per line.'),
                                 ('agent', f'Read pack share of the line weekly; call it on {ctx.check_on(56)}.')),
                  'size': {'text': f'Each trade-up adds {money(min(r["gain_per_trade_up"] for r in lines))} to '
                                   f'{money(max(r["gain_per_trade_up"] for r in lines))} margin', 'usd': None},
                  'win_rule': 'Pack takes 20 percent of the line\'s packs in 56 days with margin per order up.',
                  'stop_rule': 'Line revenue down for 4 weeks after launch.', 'check_on': ctx.check_on(56), 'time_to_ship_hours': 16})
    return a


def red_line_action(f, a, ctx):
    w = next((x for x in ctx.waterfalls if x['key'] == f['entity']['id']), None)
    a.update({
        'title': f'Reprice {f["entity"]["label"].lower()}: it is under the red line',
        'owner': 'agent_drafts',
        'artefact': {'kind': 'price_change', 'label': f'Price or offer change for {f["entity"]["label"].lower()}',
                     'draft': '\n'.join(['Margin check: ' + f['entity']['label']] +
                                         [f'{st["label"]}: {money(st["value"])}' for st in (w or {}).get('steps', [])] +
                                         ['Change the discount, the item or the media behind it until it clears the red line.'])},
        'steps': steps(('agent', 'Rebuild the waterfall with the costs in force today.'),
                       ('agent', 'Draft the smallest price or offer change that clears the red line.'),
                       ('person', 'Approve the change. Nothing ships before that.'),
                       ('agent', f'Re-run the check on {ctx.check_on(28)}.')),
        'stop_rule': 'Contribution after media under the red line for 2 weeks after the change.',
        'win_rule': 'Contribution after media at or over the red line.', 'check_on': ctx.check_on(28), 'time_to_ship_hours': 4})
    return a


def merge_red_line(actions):
    """A live first-order offer under the red line is fixed by the first-order test: one action, both findings."""
    fo = next((a for a in actions if a.get('rule_id') == 'OFFER-R08'), None)
    keep = []
    for a in actions:
        if fo and a.get('rule_id') == 'OFFER-R10' and a['entity']['id'].startswith('first_'):
            fo['finding_ids'] = fo['finding_ids'] + a['finding_ids']
            fo['why'] = fo['why'] + ' ' + a['why']
            continue
        keep.append(a)
    return keep


def merge_ladder(actions, ctx):
    rows = {r['line']: r for r in ctx.ladder_rows}
    keep, groups = [], {}
    for a in actions:
        if a.get('rule_id') in ('OFFER-R07', 'OFFER-R09') and a.get('status') == 'open' and a['entity']['id'] in rows:
            groups.setdefault(rows[a['entity']['id']]['verdict'], []).append(a)
        else:
            keep.append(a)
    for verdict, members in groups.items():
        keep.append(ladder_group_action(members, ctx.ladder_rows, verdict, ctx))
    return keep


# Rubric overrides by rule (depth.md section 4 lets a screen raise reputation or satisfaction for a rule; the
# override is written in audit.py's docstring next to the rule). Weights never change.
RUBRIC_OVERRIDE = {'OFFER-R04': {'reputation': 4, 'satisfaction': 4}}


def rescore(a, dims):
    r = dict(a['rubric'])
    for k, v in dims.items():
        r[k] = max(r.get(k) or 0, v)
    total = 0.0
    for k, w in RANK.WEIGHTS.items():
        total += w * (r[k] if r[k] is not None else 2.5) / 5
    r['total'] = round(total, 1)
    a['rubric'] = r
    return a


BUILDERS = {'OFFER-R01': threshold_action, 'OFFER-R04': rung_action, 'OFFER-R08': first_order_action,
            'OFFER-R10': red_line_action, 'OFFER-R11': promo_action, 'OFFER-R12': gifting_action}


def build(f, rd, ctx, nr):
    a = RANK.action_from_finding(f, nr)
    a['screen'] = SCREEN
    if f.get('status') == 'unavailable':
        return a
    if f['rule_id'] in RUBRIC_OVERRIDE:
        rescore(a, RUBRIC_OVERRIDE[f['rule_id']])
    fn = BUILDERS.get(f['rule_id'])
    return fn(f, a, ctx) if fn else a


def ends_on(brand, window):
    last = audit.last_full_day(None, brand)
    want = (window or {}).get('ends_on')
    if want:
        want = date.fromisoformat(str(want)[:10])
        return min(want, last)
    return last


def rank(brand='bombas', window=None):
    end = ends_on(brand, window)
    w = {'ends_on': end.isoformat(), 'days': audit.WINDOW}
    findings = audit.run(brand, w)
    rd = audit.Reader(None, brand, end)
    ctx = Ctx(rd)
    nr = RANK.net_revenue_28d(brand, w)
    actions = [build(f, rd, ctx, nr) for f in findings if f.get('status') in ('open', 'unavailable', None)]
    actions = merge_gifting(merge_red_line(merge_ladder(actions, ctx)), ctx)
    actions = [a for a in actions if not RANK.validate_action(a)]
    actions.sort(key=RANK.sort_key)
    return {'screen': SCREEN, 'brand': brand, 'window': w, 'simulated': True, 'net_revenue_28d': nr,
            'actions': actions, 'findings': findings, 'objections': ctx.objections, 'returns': returns_block(rd),
            'ladder': dict(ctx.ladder, moves=ctx.ladder_rows), 'first_order': ctx.first_order, 'waterfalls': ctx.waterfalls, 'calendar': ctx.calendar, 'gifting': ctx.gifting}
