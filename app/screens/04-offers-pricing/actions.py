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
        self.first_order['gifts'] = model.gwp_candidates(rd, playbook.GWP_RATIO)
        self.first_order['gift_bar'] = playbook.GWP_RATIO
        self.waterfalls = audit.offer_waterfalls(rd, self.objections)
        self.calendar = audit.promo_calendar(rd)
        self.gifting = audit.gifting(rd)
        self.guarantee = audit.guarantee(rd)
        self.position = audit.competitor_position(rd)
        self.parity = audit.marketplace_parity(rd)
        self.discipline = audit.discipline(rd)
        self.cart = audit.cart_ladder(rd)
        self.depth = model.depth_by_line(rd, playbook.DEPTH_TIERS)
        self.cohorts = audit.cohort_curve(rd)
        self.costs = audit.cost_moves(rd)
        self.referral = audit.referral(rd)
        self.loyalty = audit.loyalty(rd)
        self.depth_history = audit.depth_history(rd)
        self.bundles = audit.bundle_pairs(rd)
        self.launched = audit.launched_offers(rd)
        self.plans = _load('offers_pricing_approvals', HERE / 'approvals.py').planned(rd) if rd.brand else {}
        self.proposed_rows = (_load('offers_pricing_approvals', HERE / 'approvals.py').outbox_rows(rd.brand) if rd.brand else [])
        self.registry = model.registry(rd, playbook.REGISTRY_SURFACES, playbook.PRICE_TEST_WORDS)
        self.welcome = audit.welcome(rd)
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
            ('person', f'Approve the brief. Set arm B in {tool(ctx, "ab_testing", "the test tool")}. Nothing changes before that.'),
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
    done = next((e for e in (ctx.registry.get('entries') or []) if e['status'] == 'done' and row['ladder'] in e['brain_refs']
                 and (e.get('result') or {}).get('lift') is not None), None)
    if done:
        res = done['result']
        proof = (f'{done["id"]} found: {res.get("note") or done["hypothesis"]}. That is the proof for this doubt.')
        a.update({
            'title': f'Roll out the {done["id"]} result and say it where "{doubt}" is asked',
            'why': f['sentence'] + ' ' + proof,
            'owner': 'agent_drafts',
            'artefact': {'kind': 'page_section', 'label': f'Proof line from {done["id"]} for the product page',
                         'draft': proof + f'\nTreatment that won: {done["variant"].get("treatment")}.\n\n' + row['spec']},
            'steps': steps(('agent', f'Confirm {done["id"]} was rolled out to every page in its audience.'),
                           ('agent', 'Draft the proof line from the result, in plain words, with the number.'),
                           ('person', 'Approve the line and the claim tier.'),
                           ('agent', 'Add it next to the size selector and to the ads that meet this doubt.')),
            'win_rule': 'Returns for this doubt stay at the tested level; add to cart rate up.',
            'stop_rule': 'Returns for this doubt back above the control level for 4 weeks.',
            'check_on': ctx.check_on(28), 'time_to_ship_hours': 3, 'brain_refs': (a.get('brain_refs') or []) + [done['id']],
            'size': {'text': f'{row["one_star"]} one-star mentions; {done["id"]} moved {done["metric"]} {abs(res["lift"]) * 100:.0f} percent', 'usd': None}})
        return a
    who_ships = {'offer': 'Add the promise line to the product page, the cart and the ads that meet this doubt.',
                 'page_section': 'Add the section to the product page price block.',
                 'listing_fix': 'Update the marketplace title, first image and first bullet.'}[kind]
    size = (f'{money(row["cost_per_1000_orders"])} per 1,000 orders at the planned claim rate' if row['cost_per_1000_orders'] is not None
            else f'{money(row["cost_per_claim"])} per claim' if row['cost_per_claim']
            else f'{row["one_star"]} one-star mentions to answer; no claim cost, only the listing work')
    a.update({
        'title': f'Launch "{row["offer"].split(":")[0]}" to answer "{doubt}"',
        'why': f['sentence'] + (' The policy already covers it but the page does not say so.' if row['covered_by'] and kind == 'offer' else ''),
        'owner': 'agent_drafts',
        'artefact': {'kind': kind, 'label': row['offer'], 'draft': row['spec']},
        'steps': steps(
            ('agent', f'Pull the {row["one_star"]} one-star quotes and returns for "{doubt}".'),
            ('agent', 'Draft the spec and the one-line promise, priced from finance inputs.'),
            ('person', 'Approve the terms and the cost per claim. Nothing ships before that.'),
            ('agent', who_ships),
            ('agent', f'Read claims and add to cart rate every 7 days; call it on {ctx.check_on(42)}.')),
        'size': {'text': size, 'usd': None},
        'win_rule': 'Add to cart rate on the product page up, and returns for this doubt not up more than 10 percent.',
        'stop_rule': ('Marketplace sessions to orders down for 2 weeks against the 4 weeks before; put the old listing back.'
                      if kind == 'listing_fix' else
                      'Claims above 2 times the planned rate for 2 weeks, or margin per order under the red line.'),
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
            ('person', f'Approve the offer and the variants. The media buyer launches the pairs; the site arm runs in {tool(ctx, "ab_testing", "the test tool")}.'),
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
    dl = ctx.depth
    if w['key'] == 'bfcm' and not dl.get('unavailable'):
        tiers = {}
        for r in dl['rows']:
            tiers.setdefault(r['tier'], []).append(r['sku'])
        worst = min((r for r in dl['rows'] if r.get('units_needed_at_20')), key=lambda r: -r['units_needed_at_20'], default=None)
        if worst:
            lines.append(f'Volume check: at 20 percent off, {worst["sku"]} must sell {worst["units_needed_at_20"]:.2f} times the units to keep '
                         f'the same contribution before media; its break-even discount is {worst["break_even_discount"] * 100:.0f} percent.')
        lines.append(f'Depth by line (keeps the {dl["target"] * 100:.0f} percent red line after media): ' +
                     '; '.join(f'{t}: {", ".join(v)}' for t, v in tiers.items()) + '.')
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


def guarantee_action(f, a, ctx):
    g = ctx.guarantee
    t = {x['id'].split('.', 1)[1]: x for x in g['terms']}
    repl = model.claim_cost(ctx.rd, 'replacement')
    plan = g['planned']
    copy = [x['text'] for k, x in t.items() if k in ('offers.guarantee', 'policies.exchanges') and x.get('text')]
    per_1000 = (round(repl['value'] * plan['replacement'] * 1000, 2)
                if repl.get('value') is not None and plan.get('replacement') else None)
    lines = ['Page section: the guarantee where the doubt is',
             'Where: the product page under the price and the add to cart button; the cart above checkout; the size selector for the exchange line.',
             'Copy from the brain\'s own terms (the founder approves the wording):'] + [f'- "{c}"' for c in copy] + [
             'Doubts it answers: ' + '; '.join(f'"{x["doubt"]}" ({x["one_star"]} one-star)' for x in g['answers']) + '.']
    if per_1000 is not None:
        lines.append(f'Cost: saying it louder can raise claims. Planned: {plan["refund_or_replace"] * 100:.1f} percent of orders refunded '
                     f'or replaced, {plan["replacement"] * 100:.1f} of them replacements. A replacement costs {money(repl["value"])}, '
                     f'{money(per_1000)} per 1,000 orders at plan.')
    lines += [f'Stop: claims above {playbook.CLAIM_OVER_PLAN:.1f} times plan for 2 weeks.',
              'Win: product page add to cart rate up, one-star mentions for these doubts down next quarter.']
    a.update({
        'title': 'Put the guarantee on the product page and in the cart',
        'owner': 'agent_drafts',
        'artefact': {'kind': 'page_section', 'label': 'Guarantee block for the product page and the cart', 'draft': '\n'.join(lines)},
        'steps': steps(('agent', 'Check the live product page and cart for a guarantee line, read-only.'),
                       ('agent', 'Draft the block from the brain\'s approved terms and the doubts it answers.'),
                       ('person', 'Approve the wording. Legal checks the claim tier.'),
                       ('person', 'The site team adds the block to the product template and the cart.'),
                       ('agent', f'Read add to cart rate and claims weekly; call it on {ctx.check_on(42)}.')),
        'size': {'text': f'{g["one_star_answered"]} one-star mentions cite doubts it answers' +
                         (f'; {money(per_1000)} per 1,000 orders in claims at plan' if per_1000 is not None else ''), 'usd': None},
        'win_rule': 'Product page add to cart rate up; one-star mentions for these doubts down next quarter.',
        'stop_rule': f'Claims above {playbook.CLAIM_OVER_PLAN:.1f} times plan for 2 weeks.',
        'check_on': ctx.check_on(42), 'time_to_ship_hours': 6})
    return a


def stale_action(f, a, ctx):
    ev = {e['metric']: e for e in f['evidence']}
    be = ev.get('free_shipping_threshold_breakeven', {})
    new = math.ceil(be['value'] / 5) * 5 if be.get('value') else None
    a.update({
        'title': f'Re-decide the free shipping line against a ${be.get("value", 0):,.2f} break-even',
        'owner': 'agent_drafts',
        'artefact': {'kind': 'report', 'label': 'Free shipping line review', 'draft': '\n'.join([
            f'Break-even moved from ${be.get("baseline", 0):,.2f} to ${be.get("value", 0):,.2f} in a year; the line stayed at ${ctx.threshold:,.0f}.',
            'Inputs that moved: ' + '; '.join(f'{k.replace("_", " ")} {v["baseline"]} to {v["value"]}' for k, v in ev.items() if v.get('baseline') is not None) + '.',
            f'Options: keep the line, or test ${new} (break-even rounded up to $5).' if new else 'Options: keep the line.'])},
        'steps': steps(('agent', 'Recompute break-even with the label and AOV in force today.'),
                       ('agent', 'Draft the review with the options and what each must achieve.'),
                       ('person', 'Decide: keep the line or approve a test.')),
        'win_rule': 'A decision logged with the break-even it was made on.', 'stop_rule': 'Re-decide if break-even moves 5 percent again.',
        'check_on': ctx.check_on(90), 'time_to_ship_hours': 2})
    return a


def pull_action(f, a, ctx):
    t = ctx.threshold
    a.update({
        'title': f'Show shoppers how far they are from free shipping at ${t:,.0f}',
        'owner': 'agent_drafts',
        'artefact': {'kind': 'page_section', 'label': 'Free shipping progress bar for the cart and the header', 'draft': '\n'.join([
            f'Page section: a progress bar in the cart and the header: "You are $X from free shipping" up to ${t:,.0f}.',
            'Under it, one add-on that closes the gap: the single item priced nearest the gap.',
            'Win: more orders in the $10 over the line than under it within 28 days.',
            'Stop: conversion down more than 3 percent relative for 7 days.'])},
        'steps': steps(('agent', 'Pick the add-on items that close the most common gaps.'),
                       ('agent', 'Draft the bar copy and the add-on block.'),
                       ('person', 'Approve. The site team ships the bar.'),
                       ('agent', f'Read the orders just under and over the line weekly; call it on {ctx.check_on(28)}.')),
        'win_rule': 'More orders in the $10 over the line than under it within 28 days.',
        'stop_rule': 'Conversion down more than 3 percent relative for 7 days.', 'check_on': ctx.check_on(28), 'time_to_ship_hours': 6})
    return a


def claims_action(f, a, ctx):
    a.update({
        'title': 'Find what is driving guarantee claims over plan',
        'owner': 'agent_drafts',
        'artefact': {'kind': 'policy', 'label': 'Guarantee terms review', 'draft': '\n'.join([
            f['sentence'],
            'Review: claims by reason and by product line, the lines over plan, and the terms that invite abuse.',
            'Options: fix the product behind the top reason, tighten the window, or require a photo for replacements.'])},
        'steps': steps(('agent', 'Split claims by reason and by product line.'),
                       ('agent', 'Draft the review and the options.'),
                       ('person', 'Decide the change. CX updates the macros.')),
        'win_rule': 'Claims back under plan within 56 days.', 'stop_rule': 'Undo a terms change that lifts one-star mentions on the guarantee.', 'check_on': ctx.check_on(56), 'time_to_ship_hours': 4})
    return a


# What each move changes and for how long, for the test calendar. A move that shares a surface with another cannot
# run at the same time, and no test runs inside a promo window (the window changes every surface).
def surfaces(a):
    """(surfaces, days) a move changes. Two moves on one surface cannot run at once; different elements can."""
    r, kind = a.get('rule_id'), (a.get('artefact') or {}).get('kind')
    ent = (a.get('entity') or {}).get('id') or ''
    if r in ('OFFER-R01', 'OFFER-R20'):
        return ['cart rewards'], 35
    if r in ('OFFER-R08', 'OFFER-R10'):
        return ['first order offer', 'ad angle'], 35
    if r == 'OFFER-R16':
        return ['ad angle'], 28
    if r == 'OFFER-R04':
        if kind == 'listing_fix':
            return ['marketplace listing'], 28
        return (['product page promise: ' + ent.split('.')[0].replace('_', ' '), 'product page promise slot'] if kind == 'offer'
                else ['product page price block']), 42
    if r == 'OFFER-R14':
        return ['product page guarantee block', 'cart trust line'], 42
    if r == 'OFFER-R07':
        return (['product page pack selector'] if ent == 'push' else ['pack price']), 35
    if r == 'OFFER-R09':
        return ['new packs'], 56
    if r == 'OFFER-R31':
        return ['first order offer', 'ad angle'], 35
    if r == 'OFFER-R32':
        return ['first order offer', 'pop-up'], 35
    if r == 'OFFER-R29':
        return ['product page price block'], 35
    if r == 'OFFER-R26':
        return ['bundles'], 35
    if r == 'OFFER-R24':
        return ['loyalty'], 90
    if r == 'OFFER-R23':
        return ['referral'], 56
    if r == 'OFFER-R22':
        return ['list price'], 35
    if r == 'OFFER-R21':
        return ['second-order flow'], 70
    return None, None


APPROVAL_DAYS = 7


def test_calendar(actions, ctx):
    """Sequence the open moves: earliest start after approval, no two moves on one surface at once, none inside a
    promo window. Returns rows in plan order with start, end and what each waits for."""
    freeze = [(date.fromisoformat(w['start']), date.fromisoformat(w['end']), w['name']) for w in ctx.calendar if w['days_to_start'] < 120]
    busy = []   # (surface, start, end, title)
    for e in (ctx.registry.get('entries') or []):
        if e['status'] == 'running' and e['surface'] and e['until'] and e['until'] >= ctx.end.isoformat():
            busy.append((e['surface'], date.fromisoformat(e['start'] or ctx.end.isoformat()), date.fromisoformat(e['until']),
                         f'{e["id"]} (running)'))
    rows = []
    # approved moves (an active plan record in the brain) take their surfaces first, then the rest in plan order
    order = sorted(actions, key=lambda a: 0 if (ctx.plans.get(a['id']) or {}).get('status') == 'active' else 1)
    for a in order:
        sf_list, days = surfaces(a) if a.get('status') == 'open' else (None, None)
        if not sf_list:
            continue
        start = ctx.end + timedelta(days=APPROVAL_DAYS)
        waits = []
        moved = True
        while moved:
            moved = False
            end = start + timedelta(days=days - 1)
            for sf, s0, s1, title in busy:
                if sf in sf_list and s0 <= end and start <= s1:
                    start, moved = s1 + timedelta(days=1), True
                    waits.append(title)
                    break
            if moved:
                continue
            for f0, f1, name in freeze:
                if f0 <= end and start <= f1:
                    start, moved = f1 + timedelta(days=1), True
                    waits.append(name)
                    break
        end = start + timedelta(days=days - 1)
        for sf in sf_list:
            busy.append((sf, start, end, a['title']))
        freeze_hit = any(w in [f[2] for f in freeze] for w in waits)
        rows.append({'id': a['id'], 'title': a['title'], 'surfaces': sf_list, 'days': days, 'start': start.isoformat(),
                     'approved': (ctx.plans.get(a['id']) or {}).get('status') == 'active',
                     'status': 'waits' if waits and not freeze_hit else 'after_freeze' if freeze_hit else 'ready',
                     'end': end.isoformat(), 'waits_for': list(dict.fromkeys(waits)), 'owner': a['owner']})
    return rows


def covered_by_registry(actions, ctx):
    """A move whose surface and brain records match a running registry test is already being tested: it becomes
    'read the test, then roll out'. A move that only shares the surface waits in the calendar."""
    running = [e for e in (ctx.registry.get('entries') or []) if e['status'] == 'running' and e['surface']]
    for a in actions:
        if a.get('status') != 'open':
            continue
        sf, _ = surfaces(a)
        refs = set(a.get('brain_refs') or [])
        for e in running:
            if sf and e['surface'] in sf and refs & set(e['brain_refs']):
                res = e.get('result') or {}
                early = (f' Early read on {res["read_on"]}: {res["direction"]} {abs(res["lift"]) * 100:.0f} percent ({res.get("note") or "no note"}).'
                         if res.get('lift') is not None else '')
                a['registry'] = {'id': e['id'], 'relation': 'covered', 'until': e['until']}
                a['title'] = f'Read {e["id"]} on {e["until"]}, then roll out: {a["title"][0].lower()}{a["title"][1:]}'
                a['why'] = a['why'] + f' {e["id"]} already tests this on {e["metric"]}.' + early
                a['artefact'] = dict(a['artefact'], draft=f'Already running as {e["id"]} until {e["until"]}. Roll out this spec only if it holds.\n\n'
                                     + (a['artefact'].get('draft') or ''))
                a['steps'] = steps(('agent', f'Read {e["id"]} at its read point, {e["until"]}, against its metric ({e["metric"]}).'),
                                   ('person', 'Decide: roll out, keep testing or stop. The experiments screen logs it.'),
                                   ('agent', 'If it rolls out, apply the spec below to every page it names.'),
                                   ('agent', 'Recheck the metric 28 days after roll-out.'))
                a['check_on'] = e['until']
                a['time_to_ship_hours'] = 1
                break
    return actions


def add_priors(actions, ctx):
    """Every open move cites the brand's finished tests on its surface: the result and the learning, as priors."""
    done = [e for e in (ctx.registry.get('entries') or []) if e['status'] == 'done' and e['surface']]
    for a in actions:
        if a.get('status') != 'open':
            continue
        sf, _ = surfaces(a)
        pri = [e for e in done if sf and e['surface'] in sf and e['id'] not in (a.get('brain_refs') or [])]
        if not pri:
            continue
        lines = []
        for e in pri:
            res = e.get('result') or {}
            what = res.get('note') or (f'{res.get("direction")} {abs(res["lift"]) * 100:.0f} percent' if res.get('lift') is not None else 'no read')
            lines.append(f'{e["id"]} ({e["hypothesis"]}): {what}.' + (f' Learning: {e["learning"]}' if e.get('learning') else ''))
        a['priors'] = [e['id'] for e in pri]
        a['why'] = a['why'] + ' Prior on this surface: ' + ' '.join(lines)
        a['artefact'] = dict(a['artefact'], draft=(a['artefact'].get('draft') or '') + '\n\nPriors from the registry:\n' + '\n'.join('- ' + x for x in lines))
    return actions


# Which waterfall prices each move (audit.offer_waterfalls keys). A move with a check cannot be approved by the
# founder while its offer sits under the red line (room spec: the red line blocks approval).
MARGIN_CHECK = {'OFFER-R08': 'first_gwp', 'OFFER-R10': 'first_gwp'}


def attach_margin_checks(actions, ctx):
    falls = {w['key']: w for w in ctx.waterfalls or []}
    promise = next((w for w in ctx.waterfalls or [] if w['key'] == 'promise'), None)
    wear = next((r for r in ctx.objections if r['claim'] == 'replacement' and r['planned_rate'] is not None and r['cost_per_claim']), None)
    for a in actions:
        if a.get('status') != 'open':
            continue
        w = falls.get(MARGIN_CHECK.get(a.get('rule_id')))
        if a.get('rule_id') == 'OFFER-R04' and wear and (a.get('entity') or {}).get('id', '').startswith(wear['theme_key']):
            w = promise
        if not w:
            continue
        a['margin_check'] = {'offer': w['name'], 'contribution': w['contribution'], 'red_line': w['red_line'],
                             'red_line_kind': w['red_line_kind'], 'clears': w['clears']}
        line = (f'Margin check: {w["name"].lower()} keeps {money(w["contribution"])} after media; red line: {w["red_line_kind"]}; '
                + ('clears it.' if w['clears'] else 'under it, so it cannot be approved as it stands.'))
        a['artefact'] = dict(a['artefact'], draft=(a['artefact'].get('draft') or '') + '\n' + line)
    return actions


def flag_stale_inputs(actions, ctx):
    """A move that rests on a brain record older than playbook.STALE_DAYS says which one and refreshes it first."""
    for a in actions:
        if a.get('status') != 'open':
            continue
        old = []
        for rid in a.get('brain_refs') or []:
            rec = ctx.rd.record(rid) if isinstance(rid, str) and rid.count('.') >= 2 else None
            d = (rec or {}).get('date')
            try:
                age = (ctx.end - date.fromisoformat(str(d)[:10])).days
            except ValueError:
                continue
            if age > playbook.STALE_DAYS:
                old.append((rid, age))
        if not old:
            continue
        a['stale_inputs'] = [{'id': r, 'days': n} for r, n in old]
        a['why'] = a['why'] + ' ' + '; '.join(f'{r} is {n} days old' for r, n in old) + '.'
        if len(a['steps']) < 8:
            a['steps'] = steps(('person', 'Refresh ' + ', '.join(r for r, _ in old) + ' on the brand brain screen.'),
                               *[(x['who'], x['text']) for x in a['steps']])
    return actions


def merge_into(actions, child, parent):
    """A child rule's finding rides on the parent rule's action when both fire (one move fixes both)."""
    host = next((a for a in actions if a.get('rule_id') == parent and a.get('status') == 'open'), None)
    if not host:
        return actions
    keep = []
    for a in actions:
        if a.get('rule_id') == child and a.get('status') == 'open':
            host['finding_ids'] = host['finding_ids'] + a['finding_ids']
            host['why'] = host['why'] + ' ' + a['why']
            continue
        keep.append(a)
    return keep


def merge_connect(actions):
    """One connect action per missing connector, listing every rule that waits on it."""
    keep, groups = [], {}
    for a in actions:
        if a.get('status') == 'unavailable':
            con = ((a.get('artefact') or {}).get('label') or '').split(' connected')[0] or 'the source'
            groups.setdefault(con, []).append(a)
        else:
            keep.append(a)
    for con, members in groups.items():
        if len(members) == 1:
            keep.append(members[0])
            continue
        best = max(members, key=lambda m: m['rubric']['total'])
        a = dict(best)
        names = [m['entity']['label'] for m in members]
        a.update({'id': f'{SCREEN}.connect.{con}', 'finding_ids': [fid for m in members for fid in m['finding_ids']],
                  'title': f'Connect {con}, read-only, so {len(members)} rules can run',
                  'why': 'Waiting on it: ' + '; '.join(names) + '.',
                  'entity': {'type': 'connector', 'id': con, 'label': con},
                  'steps': steps(('person', f'Connect {con} in Setup with a read-only key.'),
                                 ('agent', 'Pull the last 28 days and 4 windows before.'),
                                 ('agent', 'Run the ' + str(len(members)) + ' rules and post the findings here.'))})
        keep.append(a)
    return keep


def position_action(f, a, ctx):
    cp = ctx.position
    us = cp['us']
    frame, _ = model.brain_value(ctx.rd, 'positioning.price_frame')
    g = ctx.guarantee or {}
    term = next((t['text'] for t in g.get('terms', []) if t['id'].endswith('offers.guarantee')), None)
    top_doubt = max((r for r in ctx.objections if not r['answered']), key=lambda r: r['one_star'], default=None)
    proof = [c for c in cp['competitors'] if c['proof_hooks']]
    lines = ['Ad briefs: lead with proof, not the code',
             f'Why: we sell at {money(us["price"])} an item against a set median of {money(cp["set_median_price"])} and still lead with '
             f'{us["discount_in_ads"]:.0f} percent off. The set sells proof: ' + '; '.join(f'{c["name"]} ({", ".join(c["proof_hooks"])})' for c in proof[:3]) +
             '. Their ads are signals for the angle only; nothing is copied.']
    if term:
        lines.append(f'Brief 1, the guarantee: open on the promise in our own words: "{term}" No code in the ad.')
    if top_doubt:
        lines.append(f'Brief 2, the top doubt: answer "{top_doubt["doubt"]}" ({top_doubt["one_star"]} one-star mentions) with '
                     f'{top_doubt["offer"].split(":")[0].lower()} once approved.')
    if frame:
        lines.append(f'Brief 3, price per wear: the brand\'s own price frame, "{frame}", with the pack price per item.')
    lines += ['Test: each brief runs next to the current code ad in the same ad set, same budget.',
              'Win: contribution per new visitor at or above the code ad. Stop: cost per first order above the target for 7 days.']
    a.update({
        'title': 'Lead 3 ads with proof instead of the code',
        'size': {'text': f'{us["code_share"] * 100:.0f} percent of active ads carry the code today; 3 proof ads run beside them', 'usd': None},
        'owner': 'agent_drafts',
        'artefact': {'kind': 'ad_brief', 'label': '3 ad briefs that lead with proof', 'draft': '\n'.join(lines)},
        'steps': steps(('agent', 'Pull the guarantee terms, the top open doubt and the price frame from the brain.'),
                       ('agent', 'Draft 3 briefs with first line, first frame and no code.'),
                       ('person', 'Approve the briefs. Creative makes them; the media buyer runs them next to the code ads.'),
                       ('agent', f'Read contribution per new visitor by ad weekly; call it on {ctx.check_on(28)}.')),
        'win_rule': 'Contribution per new visitor at or above the code ad.',
        'stop_rule': 'Cost per first order above the target for 7 days.', 'check_on': ctx.check_on(28), 'time_to_ship_hours': 8})
    return a


def parity_action(f, a, ctx):
    mp = ctx.parity
    under = [r for r in mp['rows'] if r['undercut']]
    rows = [f'- {r["channel"]} {r["asin"]}: {r["pack"]} items at {money(r["price"])}, {money(r["per_item"])} an item against '
            f'{money(r["site_per_item"])} on the site ({-r["gap"] * 100:.0f} percent under). Seller: {r["seller"] or "unknown"}.' for r in under]
    a.update({
        'title': f'Check the sellers on {len(under)} marketplace listings priced under the site',
        'owner': 'person',
        'artefact': {'kind': 'listing_fix', 'label': f'Price parity list for {len(under)} listings', 'draft': '\n'.join(
            ['Price parity list: listings under the site price per item'] + rows + [
             'For each: an authorised seller gets the minimum advertised price; an unknown seller goes to brand protection; '
             'a lookalike gets the real-product proof on our own listing.',
             'Win: no listing more than 10 percent under the site in 28 days. Stop: none; recheck monthly.'])},
        'steps': steps(('person', 'Open each listing and note the seller and whether it is our product and pack.'),
                       ('agent', 'Draft the parity policy line and the brand protection report for unknown sellers.'),
                       ('person', 'Send the minimum price to authorised sellers; file the report for the rest.'),
                       ('agent', f'Recheck the listing prices on {ctx.check_on(28)}.')),
        'size': {'text': f'{len(under)} listings, down to {-min(r["gap"] for r in under) * 100:.0f} percent under the site' +
                         ''.join(f'; {k} sold {money(v)} in {mp["channel_month"]}' for k, v in (mp.get('channel_sales') or {}).items()), 'usd': None},
        'win_rule': 'No listing more than 10 percent under the site price per item in 28 days.',
        'stop_rule': 'Stop chasing a listing once its seller is confirmed authorised and priced at the minimum.', 'check_on': ctx.check_on(28), 'time_to_ship_hours': 6})
    return a


def discount_policy(ctx):
    d = ctx.discipline
    ty, ly = d.get('this_year') or {}, d.get('last_year') or {}
    bf = next((w for w in ctx.calendar if w['key'] == 'bfcm'), None)
    depth = (bf or {}).get('last_year') or {}
    lines = ['Discount policy (draft for the founder)']
    if depth.get('depth') is not None:
        lines.append(f'1. Depth cap: no offer deeper than last Black Friday, {depth["depth"] * 100:.1f} percent of gross.')
    if ty:
        lines.append(f'2. Promo days: at most {max(ty["promo_days"], ly.get("promo_days") or 0)} a year (this year {ty["promo_days"]}, last year {ly.get("promo_days", "unavailable")}).')
    lines.append('3. No stacking: one code per order; the first-order code for new customers only.')
    if ty and ty.get('always_on_share') is not None:
        lines.append(f'4. Always-on: {ty["always_on_share"] * 100:.0f} percent of discount dollars go out on ordinary days. The code leaves ads that reach '
                     'returning customers; a price-keeping offer takes its place where it tests better.')
    if d.get('blended_90d') is not None:
        lines.append(f'5. Review monthly: the blended 90-day discount rate is {d["blended_90d"] * 100:.1f} percent against '
                     f'{(d.get("blended_90d_last_year") or 0) * 100:.1f} percent a year ago.')
    return '\n'.join(lines)


def discount_action(f, a, ctx):
    a.update({
        'title': 'Set the discount rules: depth cap, promo days, no stacking',
        'owner': 'agent_drafts',
        'artefact': {'kind': 'policy', 'label': 'Discount policy', 'draft': discount_policy(ctx)},
        'steps': steps(('agent', 'Pull discount share by day and by month, and last year\'s promo days.'),
                       ('agent', 'Draft the policy with caps from the brand\'s own history.'),
                       ('person', 'Approve the policy. It is saved to the brain as a plan.'),
                       ('agent', 'Check every new offer against it before it reaches approval.')),
        'win_rule': 'Blended 90-day discount rate at or under last year.', 'stop_rule': 'Revisit a cap that cuts net sales more than 5 percent in a window.',
        'check_on': ctx.check_on(30), 'time_to_ship_hours': 2})
    return a


def tool(ctx, key, fallback):
    """The brand's own tool for a job from the brain stack, else a plain word."""
    v, _ = model.brain_value(ctx.rd, f'stack.{key}')
    return v if isinstance(v, str) and v else fallback


def cart_action(f, a, ctx):
    cl = ctx.cart
    app = tool(ctx, 'upsell_app', 'the cart app')
    lines = ['Page section: a two-tier progress bar in the cart and the header',
             f'Tier 1 at ${cl["tiers"][0]["at"]:,.0f}: {cl["tiers"][0]["reward"]}.',
             f'Tier 2 at ${cl["tier2"]:,.0f}: {cl["tiers"][1]["reward"]}. Costs {money(cl["gift_cost"])} with the pick fee.',
             f'Why it pays: a shopper who climbs from tier 1 adds ${cl["climb"]:,.0f}; the gift is paid for after {money(cl["pays_after"])}, '
             f'so the climb covers it {cl["cover"]:.1f} times.',
             'Leak: orders already past tier 2 get the gift for nothing. ' + (f'They are {cl["leak_share"] * 100:.0f} percent of orders.'
                                                                              if cl['leak_share'] is not None else cl['leak_reason'][0].upper() + cl['leak_reason'][1:] + '.'),
             'Copy: "You are $X from free shipping", then "You are $X from a free gift".',
             'Win: share of orders at or past tier 2 up, margin per order up. Stop: margin per order down 2 weeks in a row.']
    a.update({
        'title': f'Add a second cart reward at ${cl["tier2"]:,.0f} in {app}',
        'size': {'text': f'{money(cl["gift_cost"])} a gift; each climber adds ${cl["climb"]:,.0f} and pays for it {cl["cover"]:.1f} times', 'usd': None},
        'owner': 'agent_drafts',
        'artefact': {'kind': 'page_section', 'label': 'Two-tier cart progress bar', 'draft': '\n'.join(lines)},
        'steps': steps(('agent', 'Pick the gift item and confirm stock for 60 days.'),
                       ('agent', f'Draft the tiers, the bar copy and the {app} set-up notes.'),
                       ('person', f'Approve the tiers. The site team sets them in {app}.'),
                       ('agent', f'Read the share of orders past each tier and margin per order weekly; call it on {ctx.check_on(35)}.')),
        'win_rule': 'Share of orders at or past tier 2 up with margin per order up.',
        'stop_rule': 'Margin per order down 2 weeks in a row.', 'check_on': ctx.check_on(35), 'time_to_ship_hours': 6})
    return a


def second_order_action(f, a, ctx):
    cc = ctx.cohorts
    cl = ctx.cart
    push = next((r for r in ctx.ladder_rows if r['verdict'] == 'push'), None)
    lines = ['Flow spec: the second-order offer',
             f'Who: first-time buyers, from their first order. {cc["new_customers_latest"]:,} joined in {cc["latest_cohort"]}.',
             f'When: send by day {cc["send_by_day"]}, before the drop after month {cc["drop_after_month"]}. '
             f'Curve, months 1 to {len(cc["curve"])}: ' + ', '.join(f'{x * 100:.1f}' for x in cc['curve']) + ' percent active.',
             'Offer: no percent off. Past buyers already trust the product; a code only trains them to wait.']
    if push:
        lines.append(f'Upgrade: move a single buyer to the {push["pack"]}-pack at {money(push["pack_per_item"])} an item; each trade-up adds {money(push["gain_per_trade_up"])}.')
    if cl:
        lines.append(f'Reward: the cart gift at ${cl["tier2"]:,.0f} ({cl["tiers"][1]["reward"]}).')
    lines += ['Messages: 3 over 10 days: the refill reminder, the pack upgrade, the last call with the gift.',
              'Win: month 2 active share up 1 point in the test cohort. Stop: unsubscribes above 1 percent a send.']
    a.update({
        'title': f'Send first-time buyers a second-order offer by day {cc["send_by_day"]}',
        'size': {'text': f'{cc["new_customers_latest"]:,} new customers a month; 1 point of month 2 repeat is {round(cc["new_customers_latest"] / 100):,} more second orders', 'usd': None},
        'owner': 'agent_drafts',
        'artefact': {'kind': 'flow', 'label': 'Second-order flow: 3 messages, no percent off', 'draft': '\n'.join(lines)},
        'steps': steps(('agent', 'Pull the cohort curve and the pack each first order bought.'),
                       ('agent', f'Draft the 3 messages and the upgrade offer for {tool(ctx, "email_app", "the email tool")}.'),
                       ('person', 'Approve the messages. The retention lead loads the flow with a 20 percent holdout.'),
                       ('agent', f'Read month 2 active share against the holdout; call it on {ctx.check_on(70)}.')),
        'win_rule': 'Month 2 active share up 1 point against the holdout.',
        'stop_rule': 'Unsubscribes above 1 percent a send.', 'check_on': ctx.check_on(70), 'time_to_ship_hours': 8})
    return a


def cost_action(f, a, ctx):
    cm = ctx.costs
    hit = [r for r in cm['rows'] if r['fires']][:6]
    cp = ctx.position or {}
    us = cp.get('us') or {}
    rows = [f'- {r["sku"]}: cost {money(r["cost_then"])} to {money(r["cost_now"])} (+{r["cost_move"] * 100:.0f} percent), price '
            f'{money(r["price_then"])} to {money(r["price_now"])}. Test {money(r["test_price"])} (+{money(r["test_raise"])}); '
            f'it can lose {r["cvr_limit"] * 100:.1f} percent of conversion and still earn more.' for r in hit]
    head = (f' We sell at {money(us["price"])} an item against a set median of {money(cp["set_median_price"])}.'
            if us.get('price') and cp.get('set_median_price') else '')
    a.update({
        'title': f'Test a price rise on the {len(hit)} packs whose cost rose most',
        'why': f['sentence'] + head,
        'owner': 'agent_drafts',
        'artefact': {'kind': 'price_change', 'label': 'Price test brief: restore margin dollars', 'draft': '\n'.join(
            ['Price test brief: pass the cost rise through', f'Cost months: in force today against a year ago. Price months: {cm["months"]["recent"]} against {cm["months"]["year_ago"]}.']
            + rows + [f'Arms: A keeps today\'s price. B shows the test price. 50/50 by visitor in {tool(ctx, "ab_testing", "the test tool")}, 28 days.',
                      'Primary metric: gross margin per visitor on these packs.',
                      'Win: margin per visitor up in B. Stop: conversion in B down more than the limit above for 7 days.'])},
        'steps': steps(('agent', 'Confirm the cost rows and the paid price per pack.'),
                       ('agent', 'Draft the price test with the conversion each pack can lose.'),
                       ('person', 'Approve the test prices. Nothing changes before that.'),
                       ('agent', f'Read margin per visitor weekly; call it on {ctx.check_on(35)}.')),
        'size': {'text': f'{money(cm["leak_12m"])} of margin a year leaks at today\'s prices', 'usd': (f.get('money_at_stake') or {}).get('usd')},
        'win_rule': 'Gross margin per visitor up in B.', 'stop_rule': 'Conversion in B down more than the pack\'s limit for 7 days.',
        'check_on': ctx.check_on(35), 'time_to_ship_hours': 4})
    return a


def referral_action(f, a, ctx):
    ro = ctx.referral
    lines = ['Offer spec: give one, get one',
             f'Terms: {ro["terms"]}.',
             f'Cost: {money(ro["cost_per_referral"])} per referred first order (2 items at landed cost and the pick fee), '
             f'{ro["share_of_cac"] * 100:.0f} percent of the {money(ro["paid_cac"])} paid media spends per new customer.',
             f'Cap: stop if cost per referred customer passes {money(ro["cap"])}, half of paid CAC.',
             'Where: the order confirmation page, the second-order flow, the account page.',
             'Win: referred first orders at or above 2 percent of new customers in 56 days. Stop: the cap above, or fraud above 5 percent of referrals.']
    a.update({
        'title': 'Launch a give-one-get-one referral paid in product',
        'owner': 'agent_drafts',
        'artefact': {'kind': 'offer', 'label': 'Referral offer spec', 'draft': '\n'.join(lines)},
        'steps': steps(('agent', 'Confirm the gift item has stock for 90 days.'),
                       ('agent', 'Draft the offer, the page copy and the confirmation-page block.'),
                       ('person', 'Approve. The retention lead picks the referral tool and sets it up.'),
                       ('agent', f'Read referred orders and cost per referral monthly; call it on {ctx.check_on(56)}.')),
        'size': {'text': f'{money(ro["cost_per_referral"])} per referred customer against {money(ro["paid_cac"])} paid', 'usd': None},
        'win_rule': 'Referred first orders at or above 2 percent of new customers in 56 days.',
        'stop_rule': f'Cost per referred customer above {money(ro["cap"])}.', 'check_on': ctx.check_on(56), 'time_to_ship_hours': 10})
    return a


def loyalty_action(f, a, ctx):
    lo = ctx.loyalty
    lines = ['Offer spec: points paid in product',
             f'Earn: {lo["earn"] * 100:.0f} percent back in points on every order.',
             f'Redeem: points buy product only, never cash off. In cash the program would cost {lo["cash_share_of_margin"] * 100:.1f} percent of '
             f'gross margin; in product it costs {lo["product_share_of_margin"] * 100:.1f} percent, because a reward item costs its landed cost.',
             'Tiers: none at launch. One rule is easier to read and to price.',
             (f'First reward: worth {money(lo["first_reward"]["value"])}, reached in {lo["first_reward"]["orders_to_reach"]} orders at the '
              f'{money(lo["first_reward"]["aov"])} AOV, inside the {money(lo["first_reward"]["band"][0])} to {money(lo["first_reward"]["band"][1])} band; '
              f'paid in product it costs {money(lo["first_reward"]["cost_in_product"])}.' if lo.get('first_reward') else 'First reward: unavailable, no AOV.'),
             'Where: the account page, the order confirmation, the second-order flow.',
             f'Stop: reward cost above {lo["cap"] * 100:.0f} percent of gross margin (our own cap, not a benchmark).',
             'Win: month 2 active share up 1 point for members against non-members in 90 days.']
    a.update({
        'title': f'Launch {lo["earn"] * 100:.0f} percent back in points, paid in product',
        'owner': 'agent_drafts',
        'artefact': {'kind': 'offer', 'label': 'Loyalty offer spec', 'draft': '\n'.join(lines)},
        'steps': steps(('agent', 'Price the earn rate against gross margin from finance inputs.'),
                       ('agent', 'Draft the terms and the account page block.'),
                       ('person', f'Approve. The retention lead sets it up in {tool(ctx, "loyalty_app", "the loyalty tool")}.'),
                       ('agent', f'Read member repeat rate and reward cost monthly; call it on {ctx.check_on(90)}.')),
        'size': {'text': f'{lo["product_share_of_margin"] * 100:.1f} percent of gross margin paid in product', 'usd': None},
        'win_rule': 'Month 2 active share up 1 point for members against non-members in 90 days.',
        'stop_rule': f'Reward cost above {lo["cap"] * 100:.0f} percent of gross margin.', 'check_on': ctx.check_on(90), 'time_to_ship_hours': 12})
    return a


def bundle_action(f, a, ctx):
    bp = ctx.bundles
    top = bp['pairs'][:3]
    rows = [f'- {p["a_title"]} ({money(p["price_a"])}) with {p["b_title"]} ({money(p["price_b"])}): bundle at {money(p["bundle_price"])}, '
            f'{p["orders_both"]} orders had both, {p["lift"]:.1f} times chance. Margin: '
            + (money(p['bundle_margin']) if p['bundle_margin'] is not None else f'unavailable, {p["margin_reason"]}') + '.' for p in top]
    a.update({
        'title': f'Build {len(top)} "complete the set" bundles from pairs people already buy',
        'owner': 'agent_drafts',
        'artefact': {'kind': 'offer', 'label': f'{len(top)} bundle offers', 'draft': '\n'.join(
            [f'Offer spec: bundles from pairs, {bp["rule"]}.'] + rows +
            [f'Where: the product page of the first item ("complete the set"), the cart upsell in {tool(ctx, "upsell_app", "the cart app")}.',
             'Win: bundle take rate at or above 5 percent of orders with either item in 28 days, margin per order up.',
             'Stop: margin per order down 2 weeks in a row.'])},
        'steps': steps(('agent', 'Pull the pairs, paid prices and landed cost.'),
                       ('agent', 'Draft the bundle prices, names and the page block.'),
                       ('person', 'Approve the bundles. Ops creates them in the store.'),
                       ('agent', f'Read take rate and margin per order weekly; call it on {ctx.check_on(35)}.')),
        'size': {'text': f'{sum(p["orders_both"] for p in top)} orders in {pair_window_text(bp)} already hold a pair', 'usd': None},
        'win_rule': 'Bundle take rate at or above 5 percent of orders with either item in 28 days.',
        'stop_rule': 'Margin per order down 2 weeks in a row.', 'check_on': ctx.check_on(35), 'time_to_ship_hours': 8})
    return a


def pair_window_text(bp):
    return f'{bp["window"]["start"]} to {bp["window"]["end"]}'


def launched_action(f, a, ctx):
    o = next((x for x in ctx.launched if 'launched_' + x['id'].split('.')[-1] == f['entity']['id']), None)
    if not o:
        return a
    b, af = o['before'] or {}, o['after'] or {}
    lines = [f'Read of a launched offer: {o["label"]}', f'Live since {o["valid_from"]}; check date {o["check_on"]}.',
             (f'Net sales per day {money(af.get("net_per_day"))} against {money(b.get("net_per_day"))} in the 28 days before; '
              f'AOV {money(af.get("aov"))} against {money(b.get("aov"))}; discounts {pct(af.get("discount_share"))} of gross against {pct(b.get("discount_share"))}.'
              if b and af else 'Before and after numbers are unavailable for these dates.'),
             'These are store-wide numbers. The test result, when there is one, is in the registry.',
             f'Stop rule from the plan: {o["stop_rule"] or "none written"}.',
             'Decide: keep it live, change it, or end it. Mark the offer record accordingly on the brand brain screen.']
    a.update({'title': f'Read the launched offer: {o["label"]}', 'owner': 'agent_drafts',
              'artefact': {'kind': 'report', 'label': 'Launched offer read', 'draft': '\n'.join(lines)},
              'steps': steps(('agent', 'Pull the before and after numbers and the registry result, if any.'),
                             ('agent', 'Draft the read with the stop rule from the plan.'),
                             ('person', 'Decide: keep, change or end the offer.')),
              'size': {'text': 'one live offer past its check date', 'usd': None},
              'win_rule': 'The plan\'s win rule holds.', 'stop_rule': o['stop_rule'] or 'Margin per order down 2 weeks in a row.',
              'check_on': ctx.check_on(7), 'time_to_ship_hours': 1})
    return a


def bnpl_action(f, a, ctx):
    b = audit.bnpl_band(ctx.rd)
    a.update({
        'title': f'Test a pay-in-installments line on packs from ${b["min_usd"]}',
        'owner': 'agent_drafts',
        'artefact': {'kind': 'test_brief', 'label': 'Installments line test brief', 'draft': '\n'.join([
            'Test brief: a pay-in-installments line under the price',
            'First check: does the checkout already offer installments? The brain does not say. If yes, this is only the page line.',
            f'Where: the product pages of {len(b["packs"])} packs priced at ${b["min_usd"]} or more ({b["revenue_share"] * 100:.0f} percent of revenue).',
            f'Arms: A as today. B adds one line under the price. 50/50 in {tool(ctx, "ab_testing", "the test tool")}, 28 days.',
            'Primary metric: profit per visitor on those pages, after the provider fee.',
            'Win: profit per visitor up in B. Stop: return rate on installment orders above the store rate for 4 weeks.'])},
        'steps': steps(('person', 'Confirm whether the checkout offers installments and at what fee.'),
                       ('agent', 'Draft the line and the test brief.'),
                       ('person', 'Approve. The site team adds the line to arm B.'),
                       ('agent', f'Read profit per visitor weekly; call it on {ctx.check_on(35)}.')),
        'size': {'text': f'{b["revenue_share"] * 100:.0f} percent of revenue sells at ${b["min_usd"]} or more', 'usd': None},
        'win_rule': 'Profit per visitor up in B.', 'stop_rule': 'Return rate on installment orders above the store rate for 4 weeks.',
        'check_on': ctx.check_on(35), 'time_to_ship_hours': 4})
    return a


def match_action(f, a, ctx):
    a.update({'title': 'Make the free shipping line the same everywhere', 'owner': 'person',
              'artefact': {'kind': 'brain_record', 'label': 'One free shipping line in the offers, the policy and the cart bar',
                           'draft': f['sentence'] + '\nPick one line. Update the brain record, the shipping policy page, the cart bar and the shipping app to it on the same day.'},
              'steps': steps(('person', 'Pick the line the store actually charges by, in the shipping app.'),
                             ('person', 'Correct the brain record on the brand brain screen.'),
                             ('person', 'Update the policy page and the cart bar the same day.')),
              'size': {'text': 'every order between the two lines sees two different promises', 'usd': None},
              'win_rule': 'One line in the offers, the policy and the cart.', 'stop_rule': 'None; this is a fix.',
              'check_on': ctx.check_on(7), 'time_to_ship_hours': 1})
    return a


def cohort_action(f, a, ctx):
    a.update({'title': 'Cut the first-order code depth or swap it for a gift', 'owner': 'agent_drafts',
              'artefact': {'kind': 'test_brief', 'label': 'First-order offer test judged on repeat', 'draft': '\n'.join([
                  f['sentence'], 'Arms: A keeps the code. B offers a free item and no percent off.',
                  'Primary metric: profit per visitor on the first order; second metric: repeat within 180 days.',
                  'Win: B keeps profit per visitor and lifts repeat. Stop: first-order conversion in B down 25 percent for 7 days.'])},
              'steps': steps(('agent', 'Split first orders by code and read repeat by group.'),
                             ('agent', 'Draft the test brief.'), ('person', 'Approve the test.'),
                             ('agent', f'Read the repeat rate at 90 and 180 days; first call on {ctx.check_on(90)}.')),
              'size': {'text': 'every first order won with a code', 'usd': None},
              'win_rule': 'B keeps profit per visitor and lifts repeat.', 'stop_rule': 'First-order conversion in B down 25 percent for 7 days.',
              'check_on': ctx.check_on(90), 'time_to_ship_hours': 4})
    return a


def welcome_action(f, a, ctx):
    """OFFER-R32: a holdout on the welcome code, judged on profit per visitor over the first order."""
    w = ctx.welcome
    need = w['required_new_share']
    hold = 10
    draft = '\n'.join([
        f'Test brief: does {w["code"]} pay for itself?',
        f['sentence'],
        f'Arms: A shows the pop-up and {w["code"]} as today. B, {hold} percent of new visitors, shows the pop-up with no code.',
        f'Read: first orders per 1,000 new visitors, and profit per visitor after the code, per arm. 28 days.',
        f'Win for the code: A beats B on profit per visitor. That means at least {need * 100:.0f} percent of code orders are new.',
        f'Else: drop the code depth or swap it for a gift, and keep the email capture.',
        f'Stop: B first orders down 40 percent against A for 7 days.',
        f'Basis: {w["basis"]}.'])
    a.update({'title': f'Hold {w["code"]} back from {hold} percent of new visitors for 28 days', 'owner': 'agent_drafts',
              'artefact': {'kind': 'test_brief', 'label': f'{w["code"]} holdout test brief', 'draft': draft},
              'steps': steps(('agent', 'Draft the holdout brief and the no-code pop-up copy.'),
                             ('person', 'Approve the holdout share and the stop rule.'),
                             ('person', f'Set the pop-up tool to hold back {hold} percent of new visitors.'),
                             ('agent', f'Read profit per visitor per arm weekly; call it on {ctx.check_on(35)}.')),
              'size': {'text': f'{money(w["code_dollars_30d"])} a month in code dollars; the code needs {need * 100:.0f} percent new orders',
                       'usd': None},
              'win_rule': f'Keep the code if A beats B on profit per visitor over 28 days.',
              'stop_rule': 'B first orders down 40 percent against A for 7 days.',
              'check_on': ctx.check_on(35), 'time_to_ship_hours': 3})
    return a


def bunches(rd):
    """Order-value bunches and the tiers above them, from real order bins only (never from the fixture)."""
    dist = rd.m('order_value_distribution', audit.WINDOW, step=5)
    if dist.get('unavailable'):
        return {'unavailable': True, 'reason': dist.get('reason')}
    return {'unavailable': False, 'peaks': model.order_bunches(dist['groups']), 'orders': dist['value'],
            'rule': 'the 3 biggest bunches of order value at least $20 apart; each tier $10 above its bunch, rounded up to $5'}


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
            'Label: mark the pack "Most popular" when it already sells the most units of its line, and list it between the single '
            'and the next size up so it reads as the middle choice. Measure the mix of pack sizes, not only conversion.',
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
RUBRIC_OVERRIDE = {'OFFER-R04': {'reputation': 4, 'satisfaction': 4}, 'OFFER-R14': {'reputation': 4, 'satisfaction': 4},
                   'OFFER-R16': {'reputation': 5}, 'OFFER-R17': {'reputation': 4}, 'OFFER-R21': {'satisfaction': 3},
                   'OFFER-R24': {'satisfaction': 3}}


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
            'OFFER-R10': red_line_action, 'OFFER-R11': promo_action, 'OFFER-R12': gifting_action,
            'OFFER-R14': guarantee_action, 'OFFER-R05': stale_action, 'OFFER-R06': pull_action, 'OFFER-R15': claims_action,
            'OFFER-R16': position_action, 'OFFER-R17': parity_action, 'OFFER-R18': discount_action,
            'OFFER-R19': discount_action, 'OFFER-R20': cart_action, 'OFFER-R21': second_order_action,
            'OFFER-R22': cost_action, 'OFFER-R23': referral_action, 'OFFER-R24': loyalty_action,
            'OFFER-R25': discount_action, 'OFFER-R26': bundle_action,
            'OFFER-R27': launched_action, 'OFFER-R29': bnpl_action,
            'OFFER-R30': match_action, 'OFFER-R31': cohort_action, 'OFFER-R32': welcome_action}


def build(f, rd, ctx, nr):
    a = RANK.action_from_finding(f, nr)
    a['screen'] = SCREEN
    if f.get('status') == 'unavailable':
        return a
    if f['rule_id'] in RUBRIC_OVERRIDE:
        rescore(a, RUBRIC_OVERRIDE[f['rule_id']])
    fn = BUILDERS.get(f['rule_id'])
    return fn(f, a, ctx) if fn else a


def ends_on(brand, window, data=None):
    last = audit.last_full_day(data, brand)
    want = (window or {}).get('ends_on')
    if want:
        want = date.fromisoformat(str(want)[:10])
        return min(want, last)
    return last


def rank(brand='bombas', window=None, data=None):
    """Ranked actions for a brand folder, or for a data source with no folder (the sample brand): data is then
    the server's Data and brand is None. Structure is fixed; content is the brand's (depth.md section 8)."""
    end = ends_on(brand, window, data)
    w = {'ends_on': end.isoformat(), 'days': audit.WINDOW}
    findings = audit.run(brand, w, data=data)
    rd = audit.Reader(data, brand, end)
    ctx = Ctx(rd)
    nr = RANK.net_revenue_28d(brand, w) if brand else None
    actions = [build(f, rd, ctx, nr) for f in findings if f.get('status') in ('open', 'unavailable', None)]
    actions = merge_connect(merge_gifting(merge_red_line(merge_ladder(actions, ctx)), ctx))
    actions = merge_into(merge_into(actions, 'OFFER-R05', 'OFFER-R01'), 'OFFER-R06', 'OFFER-R01')
    actions = merge_into(merge_into(actions, 'OFFER-R19', 'OFFER-R08'), 'OFFER-R31', 'OFFER-R08')
    actions = flag_stale_inputs(attach_margin_checks(add_priors(covered_by_registry(actions, ctx), ctx), ctx), ctx)
    actions = [a for a in actions if not RANK.validate_action(a)]
    actions.sort(key=RANK.sort_key)
    calendar = test_calendar(actions, ctx)
    return {'screen': SCREEN, 'brand': brand, 'window': w, 'simulated': True, 'net_revenue_28d': nr,
            'actions': actions, 'findings': findings, 'objections': ctx.objections, 'returns': returns_block(rd),
            'ladder': dict(ctx.ladder, moves=ctx.ladder_rows), 'first_order': ctx.first_order, 'waterfalls': ctx.waterfalls, 'calendar': ctx.calendar, 'gifting': ctx.gifting, 'guarantee': ctx.guarantee, 'position': ctx.position, 'parity': ctx.parity,
            'discipline': dict(ctx.discipline, policy=discount_policy(ctx), windows=ctx.depth_history, window_creep_points=playbook.WINDOW_CREEP_POINTS), 'cart': ctx.cart, 'tests': calendar, 'depth': ctx.depth, 'cohorts': ctx.cohorts, 'costs': ctx.costs, 'registry': ctx.registry, 'referral': ctx.referral, 'loyalty': ctx.loyalty, 'bundles': ctx.bundles, 'proposed_tests': ctx.proposed_rows, 'launched': ctx.launched, 'discount_cohorts': audit.discount_cohorts(rd), 'welcome': ctx.welcome, 'bunches': bunches(rd),
            'subscription': model.subscription_note(rd, ctx.cohorts, (ctx.depth or {}).get('rows'), (ctx.depth or {}).get('target'))}
