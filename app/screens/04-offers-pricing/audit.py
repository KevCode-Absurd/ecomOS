"""Offers and pricing audit (screen 04, round 0). Findings in the shape of app/contracts/audit.md.

Every number comes from app/metrics.py, the brand's aggregates, finance_inputs (app/data/finance.py) and the
brain (app/brain/store.py). No connector, no model call. Same tables, brain and window give the same findings.

Rules
  OFFER-R01  Free shipping threshold under break-even. Break-even is the room spec's
             free_shipping_threshold_breakeven: AOV + average label cost / gross margin rate. AOV is the 28-day
             `aov` metric; the label is the mean of the USPS zone bands in force in finance_inputs (orders carry no
             zone yet); the margin is target_gross_margin (per-SKU COGS does not join to products yet, see
             OFFER-R03). Fires when the threshold in the brain's offers record is under break-even. Money: orders
             that shipped free with a value from the threshold up to break-even, 28 days, times the average label.
             Their share comes from `order_value_distribution`, their count from the 28-day order total.
             Windows agree = how many of the 4 trailing 28-day windows also put break-even over the threshold.
             Without order rows the rule still fires from the aggregates and finance_inputs (break-even needs
             no order rows); money is null and names the orders table it waits on.
             Capability MONEY-C05 (founder gate). Owner: 04-offers-pricing.
  OFFER-R05  Free shipping threshold stale: break-even today against break-even 364 days before moved more than
             STALE_MOVE (5 percent) and the threshold did not move (room spec: free shipping threshold stale).
             No money: the move itself is priced by OFFER-R01. Capability MONEY-C05 (founder gate).
  OFFER-R06  Threshold not pulling: the $10 just over the line holds no more orders than the $10 just under
             (order_value_distribution, 28 days). Unavailable without order rows. Money: orders just under
             times the listed shipping rate they pay, a floor on the shipping friction. Capability MONEY-C05.
  OFFER-R07  Pack ladder not moving shoppers up: a line with a single and a multi-pack where the pack saves less
             than MIN_SAVING per item or singles are over SINGLE_SHARE_PUSH of the line's packs (12 full months,
             products_monthly). The finding carries the deeper price test's arithmetic: the cut given to shoppers
             who already buy the pack, the margin each trade-up adds, and the share of single buyers who must trade
             up to pay for it. Verdict `deepen` when that share is under VIABLE_TRADE_UP, else `push` (keep the price,
             preselect the pack and show price per item). Money null: the trade-up rate is what the test finds.
             Capability LIFE-C39 (founder gate). Thresholds in playbook.py.
  OFFER-R08  First-order code is the default way in: the brain's first-order code sits in more than
             playbook.CODE_ADS_SHARE of active ads, and an offer that keeps the list price
             (playbook.FIRST_ORDER_OPTIONS) keeps more contribution per first order (model.first_order_options).
             Money: discount dollars on new-customer orders in 28 days (discounts x new-customer order share; orders
             do not carry the code yet) times the share of the code's cost the better offer saves. Equal
             conversion is assumed; the test brief states how much conversion the offer can lose. Confidence 0.4.
             Capability LIFE-C02 (founder gate).
  OFFER-R09  A line in a repeat-buy category (playbook.REPEAT_CATEGORIES) sold only as a single. Proposal: a pack of
             the most common multi-pack size in that category (else 3) at NEW_PACK_SAVING off per item, with its
             margin per pack from cogs_landed x size. Capability LIFE-C39 (founder gate).
  OFFER-R10  A live offer under the margin red line: one order from list price to contribution after paid media
             (offer_waterfalls, finance_inputs costs, the brain's modelled return rates). A first order must pay its
             own media (playbook.RED_LINE_FIRST_ORDER); any other order must keep target_contribution_margin.
             Proposed offers carry the same check on the desk and cannot clear approval under it. Money null: the
             share of orders on the offer needs order rows. Capability MONEY-C05 (founder gate).
  OFFER-R11  A promo window is due (its approval date, start minus the window's lead days, is within
             playbook.PROMO_ALERT_DAYS or past) and no brain `plans` record names it. Windows are US retail date
             rules in playbook.PROMO_WINDOWS. Money: last year's net sales in the window above the 28 days before it
             (usd_revenue), times the 28-day contribution before media share (usd). Severity high when approval is
             14 days away or less. Capability LIFE-C38 (founder gate).
  OFFER-R12  No line sells as a gift: the brand runs a gifting program or a gift card (brain offers.gifting,
             products.gift_card) and no product line's November and December share of its 12 months reaches
             playbook.GIFT_LED_RATIO times the store's own share. Money null. The action is the holiday gifting
             landing page (merged into the holiday window's action when that window is due). Capability LIFE-C40.
  OFFER-R13  Gift card liability and redemption (room spec): unavailable until the gift_card_ledger table
             connects. Capability LIFE-C58 (human assist).
  OFFER-R14  Guarantee not stated where the doubt is: every brain record of the guarantee (playbook.GUARANTEE_KEYS)
             traces to a source page whose type (playbook.PAGE_TYPES by url path) is not a selling page (product,
             collection, cart, home), while ladder rungs cite it as their proof. Money null. Action: a guarantee
             block on the product page and in the cart, drafted from the brain's own terms. Rubric override:
             reputation 4 (a review theme in the ladder), satisfaction 4 (returns and CX). Capability LIFE-C42.
  OFFER-R15  Guarantee claims against plan (room spec: guarantee cost above plan): returns per order for the
             claim reasons against the brain's planned rate, fires above playbook.CLAIM_OVER_PLAN times plan.
             Unavailable until reversed_orders connects. Capability LIFE-C42.
  OFFER-R16  Discount-led in a proof-led set: our paid price per item in the main category is under the set's median,
             our first-order code is in more than playbook.CODE_ADS_SHARE of active ads, and at least
             playbook.MIN_PROOF_LED competitors priced above us show no discount in their ads. Competitor ads are
             signals only. Money null. Reputation 5 (a competitor position gap named in the brain). The action is
             3 ad briefs that lead with proof instead of the code. Capability BRN-C11 (founder gate).
  OFFER-R17  Marketplace listings under the site price (room spec: MAP violation, competitor price move): a
             listing in the brain's marketplaces section whose price over the pack count in its title is more than
             playbook.PARITY_GAP under the site's paid price per item at the same pack size (main category, 12 full
             months). One finding for all such listings. Money null: the sales they take are not in the data; the
             channel's last full month from marketplace_monthly is shown for scale. Reputation 4 override (price
             integrity across channels). Capability PROD-C46 (human assist): a person checks the seller.
  OFFER-R18  Discount creep (room spec): discount share of gross in the last full month more than
             playbook.CREEP_POINTS points above the month 3 before. Money: the extra points times the month's gross.
             The action is a discount policy. Capability LIFE-C38 (founder gate).
  OFFER-R19  Always-on discounting: more than playbook.ALWAYS_ON of the year's discount dollars go out on ordinary
             days (not promo days, model.discount_discipline) while the first-order code is in more than
             playbook.CODE_ADS_SHARE of active ads. Rides on the first-order code test when it fires. Money null.
             Capability LIFE-C38 (founder gate).
  OFFER-R03  Margin after discount per SKU. Needs cogs_landed keyed by the store's SKUs. Unavailable while no
             finance_inputs SKU key matches a product SKU. Capability MONEY-C05 (founder gate). Owner: 04.
  OFFER-R04  A deal-breaker rung with no proof: the top rung of an objection ladder whose proof is empty or
             "no public proof", with one-star mentions. Money, when a return reason maps to the theme: returns
             per paid order now minus the own median of the 4 trailing 28-day windows, times the 28-day order
             total, times (average refund + returns_processing). Lost orders are not measurable, so the money is a
             floor, or null when returns are within 5 percent of the median. Capability LIFE-C36 (founder gate).
             Severity high when the stake passes 1 percent of 28-day net, or the rung has TOP_DOUBT (20) or more
             one-star mentions. Owner: 04-offers-pricing; 10-copy and 07-landing-pages-cro read it from the
             findings table. The action is an offer spec or a proof spec from playbook.THEME_OFFERS.
             Rubric override (depth.md section 4): reputation 4 (a review theme in a deal-breaker rung) and
             satisfaction 4 (a returns and CX theme) for every rung, so the rank follows severity and stake
             rather than words in the doubt.
"""
import importlib.util
import json
import math
import re
import statistics
import sys
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parents[1]
SCREEN = '04-offers-pricing'
WINDOW = 28
TRAILING = 4
BAND_USD = 10          # the "just under" and "just over" bands either side of the threshold
STALE_MOVE = 0.05       # break-even moved more than 5 percent in a year: the threshold is stale
TOP_DOUBT = 20         # one-star mentions that make a rung a top doubt (severity high)
RETURNS_NOISE = 0.05    # returns within 5 percent of the own median carry no money
LABEL_CARRIER = 'usps'  # free standard shipping goes out on the ground carrier
# Return reasons that are the same doubt as a ladder theme. A theme with no reason here has no money.
THEME_REASONS = {'durability': ('hole or defect',), 'fit_and_sizing': ('size or fit',),
                 'order_and_delivery': ('wrong item', 'arrived late')}

RULES = [
    {'rule_id': 'OFFER-R01', 'name': 'Free shipping threshold under break-even', 'entity_type': 'offer',
     'inputs': ['brain.offers.free_shipping_threshold_usd', 'orders', 'finance_inputs.shipping_label',
                'finance_inputs.target_gross_margin'], 'capability': 'MONEY-C05', 'owner_screen': SCREEN},
    {'rule_id': 'OFFER-R05', 'name': 'Free shipping threshold stale against break-even', 'entity_type': 'offer',
     'inputs': ['brain.offers.free_shipping_threshold_usd', 'daily', 'finance_inputs.shipping_label',
                'finance_inputs.target_gross_margin'], 'capability': 'MONEY-C05', 'owner_screen': SCREEN},
    {'rule_id': 'OFFER-R06', 'name': 'Free shipping threshold not pulling baskets up', 'entity_type': 'offer',
     'inputs': ['brain.offers.free_shipping_threshold_usd', 'orders'], 'capability': 'MONEY-C05', 'owner_screen': SCREEN},
    {'rule_id': 'OFFER-R07', 'name': 'Pack ladder not moving shoppers up', 'entity_type': 'sku',
     'inputs': ['products_monthly', 'finance_inputs.cogs_landed'], 'capability': 'LIFE-C39', 'owner_screen': SCREEN},
    {'rule_id': 'OFFER-R08', 'name': 'First-order code is the default way in', 'entity_type': 'offer',
     'inputs': ['brain.offers.first_order_code', 'brain.offers.promo_share_active_ads', 'daily', 'finance_inputs'],
     'capability': 'LIFE-C02', 'owner_screen': SCREEN},
    {'rule_id': 'OFFER-R09', 'name': 'Basics line sold only as a single', 'entity_type': 'sku',
     'inputs': ['products_monthly', 'finance_inputs.cogs_landed'], 'capability': 'LIFE-C39', 'owner_screen': SCREEN},
    {'rule_id': 'OFFER-R10', 'name': 'Live offer under the margin red line', 'entity_type': 'offer',
     'inputs': ['daily', 'finance_inputs', 'brain.offers', 'brain.economics.return_share_model'],
     'capability': 'MONEY-C05', 'owner_screen': SCREEN},
    {'rule_id': 'OFFER-R11', 'name': 'Promo window due with no offer planned', 'entity_type': 'offer',
     'inputs': ['daily', 'brain.plans', 'brain.calendar'], 'capability': 'LIFE-C38', 'owner_screen': SCREEN},
    {'rule_id': 'OFFER-R12', 'name': 'No line sells as a gift', 'entity_type': 'offer',
     'inputs': ['products_monthly', 'monthly', 'brain.offers.gifting', 'brain.products.gift_card'],
     'capability': 'LIFE-C40', 'owner_screen': SCREEN},
    {'rule_id': 'OFFER-R13', 'name': 'Gift card liability and redemption', 'entity_type': 'metric',
     'inputs': ['gift_card_ledger'], 'capability': 'LIFE-C58', 'owner_screen': SCREEN},
    {'rule_id': 'OFFER-R14', 'name': 'Guarantee not stated where the doubt is', 'entity_type': 'offer',
     'inputs': ['brain.offers.guarantee', 'brain.policies', 'brain.claims', 'brain.objection_ladders'],
     'capability': 'LIFE-C42', 'owner_screen': SCREEN},
    {'rule_id': 'OFFER-R15', 'name': 'Guarantee claims against the planned rate', 'entity_type': 'offer',
     'inputs': ['reversed_orders', 'brain.economics.return_share_model'], 'capability': 'LIFE-C42', 'owner_screen': SCREEN},
    {'rule_id': 'OFFER-R16', 'name': 'Discount-led in a proof-led set', 'entity_type': 'offer',
     'inputs': ['brain.competitors', 'brain.offers.promo_share_active_ads', 'products_monthly'],
     'capability': 'BRN-C11', 'owner_screen': SCREEN},
    {'rule_id': 'OFFER-R17', 'name': 'Marketplace listings under the site price', 'entity_type': 'offer',
     'inputs': ['brain.marketplaces', 'products_monthly', 'marketplace_monthly'], 'capability': 'PROD-C46', 'owner_screen': SCREEN},
    {'rule_id': 'OFFER-R18', 'name': 'Discount creep', 'entity_type': 'offer', 'inputs': ['monthly'],
     'capability': 'LIFE-C38', 'owner_screen': SCREEN},
    {'rule_id': 'OFFER-R19', 'name': 'Always-on discounting', 'entity_type': 'offer',
     'inputs': ['daily', 'brain.offers.promo_share_active_ads'], 'capability': 'LIFE-C38', 'owner_screen': SCREEN},
    {'rule_id': 'OFFER-R03', 'name': 'Margin after discount per SKU', 'entity_type': 'sku',
     'inputs': ['finance_inputs.cogs_landed keyed by product SKU', 'products'], 'capability': 'MONEY-C05',
     'owner_screen': SCREEN},
    {'rule_id': 'OFFER-R04', 'name': 'Deal-breaker objection rung with no proof', 'entity_type': 'ladder_rung',
     'inputs': ['brain.objection_ladders', 'reversed_orders', 'finance_inputs.returns_processing'],
     'capability': 'LIFE-C36', 'owner_screen': SCREEN},
]
CAPABILITY = {'OFFER-R01': {'id': 'MONEY-C05', 'autonomy': 'founder_gate'},
              'OFFER-R03': {'id': 'MONEY-C05', 'autonomy': 'founder_gate'},
              'OFFER-R05': {'id': 'MONEY-C05', 'autonomy': 'founder_gate'},
              'OFFER-R07': {'id': 'LIFE-C39', 'autonomy': 'founder_gate'},
              'OFFER-R08': {'id': 'LIFE-C02', 'autonomy': 'founder_gate'},
              'OFFER-R09': {'id': 'LIFE-C39', 'autonomy': 'founder_gate'},
              'OFFER-R10': {'id': 'MONEY-C05', 'autonomy': 'founder_gate'},
              'OFFER-R11': {'id': 'LIFE-C38', 'autonomy': 'founder_gate'},
              'OFFER-R12': {'id': 'LIFE-C40', 'autonomy': 'founder_gate'},
              'OFFER-R13': {'id': 'LIFE-C58', 'autonomy': 'human_assist'},
              'OFFER-R14': {'id': 'LIFE-C42', 'autonomy': 'founder_gate'},
              'OFFER-R15': {'id': 'LIFE-C42', 'autonomy': 'founder_gate'},
              'OFFER-R16': {'id': 'BRN-C11', 'autonomy': 'founder_gate'},
              'OFFER-R17': {'id': 'PROD-C46', 'autonomy': 'human_assist'},
              'OFFER-R18': {'id': 'LIFE-C38', 'autonomy': 'founder_gate'},
              'OFFER-R19': {'id': 'LIFE-C38', 'autonomy': 'founder_gate'},
              'OFFER-R06': {'id': 'MONEY-C05', 'autonomy': 'founder_gate'},
              'OFFER-R04': {'id': 'LIFE-C36', 'autonomy': 'founder_gate'}}
SEVERITY_ORDER = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}

_MODS = {}


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def metrics():
    if 'metrics' not in _MODS:
        _MODS['metrics'] = _load('ecomos_metrics_offers', APP / 'metrics.py')
    return _MODS['metrics']


def brand_data(brand):
    if 'tables' not in _MODS:
        _MODS['tables'] = _load('ecomos_tables_offers', APP / 'data' / 'tables.py')
    return _MODS['tables'].brand_data(brand)


def brain(brand):
    """The brand's brain records, or None when the brand has no brain folder."""
    if not brand or not (APP / 'brain' / brand).is_dir():
        return None
    if 'store' not in _MODS:
        path = str(APP / 'brain')
        if path not in sys.path:
            sys.path.insert(0, path)  # store.py imports validate.py by name
        _MODS['store'] = _load('ecomos_brain_store_offers', APP / 'brain' / 'store.py')
    return _MODS['store'].Brain(brand)


def is_proofless(proof):
    return not proof or str(proof).lower().startswith('no public proof')


class Reader:
    """One brand, one window end. m(name, days, end, **kw) is metrics.compute with the brand filled in."""

    def __init__(self, data, brand, ends_on):
        self.data, self.brand, self.ends_on = data, brand, ends_on
        self.source = brand_data(brand) if brand else data
        self._brain = brain(brand)
        self._fin = None

    def m(self, name, days=WINDOW, end=None, **kw):
        q = {'window': f'{days}d', 'end': (end or self.ends_on).isoformat(), **kw}
        if self.brand:
            q['brand'] = self.brand
        return metrics().compute(name, self.data, **q)

    def table(self, name):
        try:
            return self.source.table(name)
        except (KeyError, ValueError):
            return None

    def record(self, rid):
        return self._brain.get(rid) if self._brain else None

    def records(self, section):
        return self._brain.records(section) if self._brain else []

    def finance_rows(self):
        try:
            return self.source.table('finance_inputs')
        except (KeyError, ValueError):
            pass
        path = Path(getattr(self.source, 'folder', '') or '') / 'finance_inputs.json'
        if path.is_file():
            doc = json.loads(path.read_text(encoding='utf-8'))
            return doc.get('rows') if isinstance(doc, dict) else doc
        return None

    def fin(self):
        if self._fin is None:
            rows = self.finance_rows()
            self._fin = metrics().finance.Finance(rows) if rows else False
        return self._fin or None


def last_full_day(data, brand):
    source = brand_data(brand) if brand else data
    return date.fromisoformat(source.brand['as_of'])


def _ev(metric, value, unit, ends_on, baseline=None, baseline_kind=None, window='28d', source='orders'):
    return {'metric': metric, 'value': value, 'unit': unit, 'window': window, 'ends_on': ends_on.isoformat(),
            'freshness_days': 1, 'baseline': baseline, 'baseline_kind': baseline_kind, 'source': source,
            'simulated': True}


def _confidence(windows_agree):
    return 0.9 if windows_agree >= 4 else 0.7 if windows_agree >= 2 else 0.5


def _severity(stake, net_28d, windows_agree):
    if stake is not None and net_28d and stake > 0.05 * net_28d:
        return 'critical'
    if windows_agree >= 2 or (stake is not None and net_28d and stake > 0.01 * net_28d):
        return 'high'
    return 'medium'


def _finding(rule_id, entity, severity, evidence, sentence, money, confidence, brain_refs, ends_on,
             status='open', unavailable=None, money_reason=None):
    f = {'id': f'{SCREEN}.{rule_id}.{entity["id"]}', 'screen': SCREEN, 'rule_id': rule_id, 'severity': severity,
         'entity': entity, 'evidence': evidence, 'sentence': sentence, 'capability': dict(CAPABILITY[rule_id]),
         'money_at_stake': money, 'confidence': confidence, 'brain_refs': brain_refs,
         'first_seen': ends_on.isoformat(), 'last_seen': ends_on.isoformat(), 'status': status,
         'unavailable': unavailable}
    if money is None:
        f['money_reason'] = money_reason or 'no baseline'
    return f


# ---------------------------------------------------------------- inputs shared with api.py

def threshold_usd(rd):
    rec = rd.record(f'{rd.brand}.offers.free_shipping_threshold_usd') if rd.brand else None
    if rec and isinstance(rec.get('value'), (int, float)):
        return float(rec['value']), rec
    return None, rec


def label_cost(rd, day):
    """Mean USPS label across the zone bands in force on `day`, with the rows used. None when none are on file."""
    f = rd.fin()
    if not f:
        return None, []
    rows = [r for r in f.in_force('shipping_label', day.isoformat())
            if str(r.get('scope_key') or '').startswith(LABEL_CARRIER)]
    if not rows:
        return None, []
    return round(statistics.mean(float(r['value']) for r in rows), 4), rows


def gross_margin(rd, day):
    f = rd.fin()
    v = f.value('target_gross_margin', day.isoformat()) if f else None
    return (v / 100) if v else None


def break_even(rd, end):
    """free_shipping_threshold_breakeven for the 28 days ending `end`: dict with the inputs, or dict with reason."""
    aov = rd.m('aov', WINDOW, end)
    if aov.get('unavailable'):
        return {'value': None, 'reason': aov.get('reason'), 'fix': aov.get('fix')}
    label, rows = label_cost(rd, end)
    if label is None:
        return {'value': None, 'reason': 'no shipping label cost in finance_inputs', 'fix': 'finance_inputs.shipping_label'}
    gm = gross_margin(rd, end)
    if not gm:
        return {'value': None, 'reason': 'no gross margin in finance_inputs', 'fix': 'finance_inputs.target_gross_margin'}
    return {'value': round(aov['value'] + label / gm, 2), 'aov': aov['value'], 'label': label, 'gross_margin': gm,
            'orders': aov['inputs']['orders'], 'net_revenue': aov['inputs']['net_revenue'],
            'label_rows': [r.get('scope_key') for r in rows],
            'formula': 'aov + average_label / gross_margin'}


def band_share(groups, lo, hi):
    """Share of orders with a value in [lo, hi). Bins must align with lo and hi."""
    return round(sum(g['share'] for g in groups if g['from'] >= lo and g['to'] <= hi), 6)


# ---------------------------------------------------------------- rules

def rule_threshold(rd):
    end = rd.ends_on
    t, rec = threshold_usd(rd)
    refs = [f'{rd.brand}.offers.free_shipping_threshold_usd', f'{rd.brand}.offers.standard_shipping_cost']
    entity = {'type': 'offer', 'id': 'free_shipping_threshold', 'label': f'Free shipping at ${t:,.0f}' if t else 'Free shipping'}
    if t is None:
        return [_finding('OFFER-R01', entity, 'medium', [], 'The free shipping threshold is not in the brain.', None,
                         0.1, refs, end, status='unavailable', money_reason='no threshold',
                         unavailable={'inputs': ['brain.offers.free_shipping_threshold_usd'], 'connector': 'brand brain',
                                      'fix': 'Add the free shipping threshold to the brain offers section.'})]
    be = break_even(rd, end)
    dist = rd.m('order_value_distribution', WINDOW, end, step=5)
    if be['value'] is None:
        return [_finding('OFFER-R01', entity, 'medium', [], 'Break-even for free shipping cannot be computed yet.', None,
                         0.1, refs, end, status='unavailable', money_reason='inputs missing',
                         unavailable={'inputs': [be.get('fix') or 'orders'], 'connector': be.get('fix'),
                                      'fix': be.get('reason')})]
    if t >= be['value']:
        return []
    agree = 1
    for k in range(1, TRAILING):
        prev = break_even(rd, end - timedelta(days=WINDOW * k))
        if prev['value'] is not None and prev['value'] > t:
            agree += 1
    top = math.floor(be['value'] / 5) * 5  # bins are $5; the stake counts whole bins under break-even
    evidence = [
        _ev('free_shipping_threshold', t, 'usd', end, source='brain.offers', window='current'),
        _ev('free_shipping_threshold_breakeven', be['value'], 'usd', end, baseline=t, baseline_kind='threshold',
            source='aov, finance_inputs'),
        _ev('aov', be['aov'], 'usd', end, source='daily'),
        _ev('average_label', be['label'], 'usd_per_order', end, source='finance_inputs.shipping_label', window='in force'),
        _ev('gross_margin', be['gross_margin'], 'ratio', end, source='finance_inputs.target_gross_margin', window='in force'),
    ]
    if dist.get('unavailable'):
        # break-even is known from the aggregates; the orders it costs need order rows, so money waits on them
        sentence = (f'Free shipping starts at ${t:,.0f}, under the ${be["value"]:,.2f} break-even. '
                    f'Orders from ${t:,.0f} to ${be["value"]:,.2f} ship free without covering the label.')
        return [_finding('OFFER-R01', entity, 'high' if agree >= 2 else 'medium', evidence, sentence, None,
                         0.5 if agree >= 2 else 0.3, refs, end,
                         money_reason='order value bins need the orders table: ' + str(dist.get('reason')))]
    share = band_share(dist['groups'], t, top)
    free_orders = round(share * be['orders'])
    stake = round(free_orders * be['label'], 2)
    money = {'usd': stake, 'formula': 'orders_28d x share_threshold_to_break_even x average_label',
             'inputs': {'orders_28d': be['orders'], 'share_threshold_to_break_even': share,
                        'band': f'${t:,.0f} to ${top:,.0f}', 'average_label': be['label']}, 'window': '28d'}
    evidence.append(_ev('share_threshold_to_break_even', share, 'ratio', end))
    sentence = (f'Free shipping starts at ${t:,.0f}, under the ${be["value"]:,.2f} break-even. '
                f'{share * 100:.1f} percent of orders ship free between ${t:,.0f} and ${top:,.0f}.')
    return [_finding('OFFER-R01', entity, _severity(stake, be['net_revenue'], agree), evidence, sentence, money,
                     _confidence(agree), refs, end)]


def rule_stale(rd):
    end = rd.ends_on
    t, rec = threshold_usd(rd)
    if t is None:
        return []
    now, then = break_even(rd, end), break_even(rd, end - timedelta(days=364))
    if now['value'] is None or then['value'] is None:
        return []
    move = now['value'] / then['value'] - 1
    if abs(move) <= STALE_MOVE:
        return []
    entity = {'type': 'offer', 'id': 'free_shipping_threshold_stale', 'label': f'Free shipping at ${t:,.0f}'}
    evidence = [_ev('free_shipping_threshold_breakeven', now['value'], 'usd', end, baseline=then['value'],
                    baseline_kind='same_window_last_year', source='aov, finance_inputs'),
                _ev('aov', now['aov'], 'usd', end, baseline=then['aov'], baseline_kind='same_window_last_year', source='daily'),
                _ev('average_label', now['label'], 'usd_per_order', end, baseline=then['label'],
                    baseline_kind='same_window_last_year', source='finance_inputs.shipping_label', window='in force')]
    sentence = (f'Break-even for free shipping moved from ${then["value"]:,.2f} to ${now["value"]:,.2f} in a year, '
                f'{move * 100:+.1f} percent. The ${t:,.0f} line did not move.')
    return [_finding('OFFER-R05', entity, 'medium', evidence, sentence, None, 0.7,
                     [f'{rd.brand}.offers.free_shipping_threshold_usd'], end, money_reason='priced by OFFER-R01')]


def rule_pull(rd):
    end = rd.ends_on
    t, _ = threshold_usd(rd)
    if t is None:
        return []
    entity = {'type': 'offer', 'id': 'free_shipping_pull', 'label': f'Free shipping at ${t:,.0f}'}
    dist = rd.m('order_value_distribution', WINDOW, end, step=5)
    if dist.get('unavailable'):
        return [_finding('OFFER-R06', entity, 'medium', [], 'Whether the free shipping line pulls baskets up is unknown '
                         'without order rows.', None, 0.1, [f'{rd.brand}.offers.free_shipping_threshold_usd'], end,
                         status='unavailable', money_reason='order value bins need the orders table',
                         unavailable={'inputs': ['orders'], 'connector': dist.get('fix') or 'shopify',
                                      'fix': 'Connect the store orders, read-only, so order values can be binned.'})]
    under, over = band_share(dist['groups'], t - BAND_USD, t), band_share(dist['groups'], t, t + BAND_USD)
    if over > under:
        return []
    rate = ((rd.record(f'{rd.brand}.offers.standard_shipping_cost') or {}).get('value') or {}).get('cost_usd') if rd.brand else None
    aov = rd.m('aov', WINDOW)
    orders = None if aov.get('unavailable') else aov['inputs']['orders']
    money = None
    if rate and orders:
        n = round(under * orders)
        money = {'usd': round(n * rate, 2), 'formula': 'orders_28d x share_just_under x shipping_rate',
                 'inputs': {'orders_28d': orders, 'share_just_under': under, 'shipping_rate': rate}, 'window': '28d'}
    evidence = [_ev('share_just_under', under, 'ratio', end), _ev('share_just_over', over, 'ratio', end,
                                                                 baseline=under, baseline_kind='just_under')]
    sentence = (f'{over * 100:.1f} percent of orders land in the ${BAND_USD} over the ${t:,.0f} line and '
                f'{under * 100:.1f} percent in the ${BAND_USD} under it. The line is not pulling baskets up.')
    return [_finding('OFFER-R06', entity, 'medium', evidence, sentence, money, 0.7,
                     [f'{rd.brand}.offers.free_shipping_threshold_usd'], end, money_reason=None if money else 'no shipping rate')]


def _playbook():
    if 'playbook' not in _MODS:
        _MODS['playbook'] = _load('offers_pricing_playbook_audit', HERE / 'playbook.py')
    return _MODS['playbook']


def _model():
    if 'model' not in _MODS:
        _MODS['model'] = _load('offers_pricing_model_audit', HERE / 'model.py')
    return _MODS['model']


def ladder_moves(rd):
    """Per line: the pack ladder verdict and its arithmetic. Shared with actions.py and the desk."""
    pb, lad = _playbook(), _model().ladder(rd)
    if lad.get('unavailable'):
        return lad, []
    rows = []
    for ln in lad['lines']:
        if ln['single_sku'] and ln['pack_sku'] and ln['saving'] is not None:
            weak = ln['saving'] < pb.MIN_SAVING
            stuck = ln['single_share'] is not None and ln['single_share'] > pb.SINGLE_SHARE_PUSH
            if not (weak or stuck):
                rows.append(dict(ln, verdict='keep'))
                continue
            n = ln['pack']
            new_price = round(ln['single_per_item'] * n * (1 - pb.TARGET_SAVING), 2)
            cut = round(ln['pack_price'] - new_price, 2)
            pack_packs = ln['packs'] - ln['single_packs']
            give = round(max(cut, 0) * pack_packs, 2)
            gain_now = (round(ln['pack_margin'] - ln['single_margin'], 2)
                        if ln['pack_margin'] is not None and ln['single_margin'] is not None else None)
            gain_new = (round(new_price - ln['pack_cogs'] - ln['single_margin'], 2)
                        if ln['pack_cogs'] is not None and ln['single_margin'] is not None else None)
            need = round(give / gain_new / ln['single_packs'], 4) if gain_new and gain_new > 0 and ln['single_packs'] else None
            verdict = 'deepen' if need is not None and need <= pb.VIABLE_TRADE_UP else 'push'
            rows.append(dict(ln, verdict=verdict, weak=weak, stuck=stuck, test_price=new_price, test_cut=cut,
                             give_away_12m=give, gain_per_trade_up=gain_now, gain_per_trade_up_at_test=gain_new,
                             trade_up_needed=need))
        elif ln['single_sku'] and not ln['pack_sku'] and (ln['category'] or '').lower() in pb.REPEAT_CATEGORIES:
            sizes = [r['pack'] for r in lad['rows'] if r['category'] == ln['category'] and (r['pack'] or 0) > 1]
            n = max(set(sizes), key=sizes.count) if sizes else pb.DEFAULT_NEW_PACK
            price = round(ln['single_per_item'] * n * (1 - pb.NEW_PACK_SAVING), 2)
            cogs = round(ln['single_cogs'] * n, 2) if ln['single_cogs'] is not None else None
            rows.append(dict(ln, verdict='add', new_pack=n, new_price=price, new_cogs=cogs,
                             new_margin=round(price - cogs, 2) if cogs is not None else None,
                             gain_per_trade_up=round(price - cogs - ln['single_margin'], 2)
                             if cogs is not None and ln['single_margin'] is not None else None))
        else:
            rows.append(dict(ln, verdict='keep'))
    return lad, rows


def first_order(rd):
    """The first-order options table for the rule and the desk."""
    lad, _ = ladder_moves(rd)
    lines = [] if lad.get('unavailable') else [r for r in lad['lines'] if r['pack_sku']]
    top = max(lines, key=lambda r: r['packs'] - (r['single_packs'] or 0)) if lines else None
    cands = _model().gwp_candidates(rd, _playbook().GWP_RATIO)   # best value over cost first; qualifying or not
    return _model().first_order_options(rd, _playbook().FIRST_ORDER_OPTIONS, top, gift=cands[0] if cands else None)


def rule_first_order(rd):
    end = rd.ends_on
    pb = _playbook()
    share, _ = _model().brain_value(rd, 'offers.promo_share_active_ads')
    if not isinstance(share, dict) or not share.get('active_ads'):
        return []
    ads = share['ads_with_code'] / share['active_ads']
    fo = first_order(rd)
    if fo.get('unavailable') or ads <= pb.CODE_ADS_SHARE:
        return []
    code = next(r for r in fo['rows'] if r['key'] == 'code')
    alts = [r for r in fo['rows'] if not r.get('unavailable') and r['keeps_price'] and r['contribution'] > code['contribution']]
    if not alts:
        return []
    best = max(alts, key=lambda r: r['contribution'])
    spend = round(fo['discounts_28d'] * fo['new_share'], 2)
    saved = round(spend * (1 - best['cost'] / code['cost']), 2) if code['cost'] else None
    money = None if saved is None else {
        'usd': saved, 'formula': 'discounts_28d x new_customer_share x (1 - better_offer_cost / code_cost)',
        'inputs': {'discounts_28d': fo['discounts_28d'], 'new_customer_share': fo['new_share'],
                   'better_offer_cost': best['cost'], 'code_cost': code['cost']},
        'window': '28d', 'note': 'at equal conversion; the test finds the real number'}
    entity = {'type': 'offer', 'id': 'first_order_code', 'label': f'{fo["code_pct"]:.0f} percent first-order code'}
    evidence = [_ev('ads_with_code', round(ads, 4), 'ratio', end, baseline=pb.CODE_ADS_SHARE, baseline_kind='threshold',
                    window='active ads', source='brain.offers.promo_share_active_ads'),
                _ev('first_order_contribution_code', code['contribution'], 'usd', end, baseline=best['contribution'],
                    baseline_kind=best['key'], source='daily, finance_inputs'),
                _ev('first_order_payback_code', code['payback'], 'ratio', end, baseline=best['payback'],
                    baseline_kind=best['key'], source='daily, finance_inputs')]
    sentence = (f'{share["ads_with_code"]} of {share["active_ads"]} active ads carry the {fo["code_pct"]:.0f} percent code. '
                f'It keeps ${code["contribution"]:,.2f} per first order; {best["name"].lower()} keeps ${best["contribution"]:,.2f}.')
    return [_finding('OFFER-R08', entity, 'high', evidence, sentence, money, 0.4,
                     [f'{rd.brand}.offers.first_order_code', f'{rd.brand}.offers.promo_share_active_ads'], end)]


def offer_waterfalls(rd, objections=None):
    """Current and proposed offers, each as one order from list price to contribution after media."""
    model, pb = _model(), _playbook()
    fo = first_order(rd)
    t = model.window_totals(rd)
    po = model.per_order(t)
    thr, _ = threshold_usd(rd)
    if not po or fo.get('unavailable'):
        return []
    cr = model.cogs_ratio(rd)
    cogs = cr['ratio'] * po['net'] if cr.get('ratio') is not None else None
    media_all = po['spend']
    cac = fo['new_cac']
    g, units = po['gross'], po['units']
    code_pct = fo['code_pct'] or 0
    gwp = next((r for r in fo['rows'] if r['key'] == 'gwp' and not r.get('unavailable')), None)
    ic = gwp['extra_item'] if gwp else model.item_cost(rd).get('value')
    out = [
        {'key': 'average', 'name': 'The average order today', 'status': 'live',
         'note': 'All orders, 28 days: discounts, shipping charged and paid media per order as they ran.',
         **model.waterfall(rd, g, po['discount'], cogs, units, ships_free=False, shipping_charged=po['shipping_charged'], media=media_all)},
        {'key': 'first_code', 'name': f'First order with the {code_pct:.0f} percent code', 'status': 'live',
         'note': 'Average list-price order, the code applied, paid media per new customer.',
         **model.waterfall(rd, g, g * code_pct / 100, cogs, units, media=cac)},
        {'key': 'first_gwp', 'name': 'First order with a free item', 'status': 'proposed',
         'note': 'Average list-price order at full price, one item added to the box, paid media per new customer.',
         **model.waterfall(rd, g, 0, cogs, units, extra_item=ic or 0, extra_units=1, media=cac)},
    ]
    if thr and cr.get('ratio') is not None:
        out.append({'key': 'at_line', 'name': f'An order at the ${thr:,.0f} free shipping line', 'status': 'live',
                    'note': 'An order of exactly the line value, shipping free, average discount share and paid media per order.',
                    **model.waterfall(rd, thr * g / po['net'], thr * g / po['net'] - thr, cr['ratio'] * thr, units, media=media_all)})
    wear = next((r for r in (objections or []) if r['claim'] == 'replacement' and r['planned_rate'] is not None and r['cost_per_claim']), None)
    if wear:
        out.append({'key': 'promise', 'name': f'The average order with the {wear["offer"].split(":")[0].lower()}', 'status': 'proposed',
                    'note': f'Adds claims at the planned {wear["planned_rate"] * 100:.1f} percent rate on top of the modelled returns.',
                    **model.waterfall(rd, g, po['discount'], cogs, units, ships_free=False, shipping_charged=po['shipping_charged'],
                                      media=media_all, claim=(wear['planned_rate'], wear['cost_per_claim']))})
    for w in out:
        first = w['key'].startswith('first_')
        line = pb.RED_LINE_FIRST_ORDER if first else w['red_line']
        w['red_line_kind'] = 'first order pays its own media' if first else 'target contribution margin'
        w['red_line'] = line
        w['clears'] = None if line is None or w['contribution'] is None else (
            w['contribution'] >= line * w['price_paid'] if not first else w['contribution'] >= line)
    return out



def rule_red_line(rd):
    end = rd.ends_on
    out = []
    for w in offer_waterfalls(rd):
        if w['status'] != 'live' or w['clears'] is not False:
            continue
        entity = {'type': 'offer', 'id': w['key'], 'label': w['name']}
        first = w['key'].startswith('first_')
        line_text = (f'${w["red_line"]:,.2f} after media' if first else f'{w["red_line"] * 100:.0f} percent of the price paid')
        evidence = [_ev('contribution_after_media', w['contribution'], 'usd', end, baseline=(w['red_line'] if first else
                        round(w['red_line'] * w['price_paid'], 2)), baseline_kind='red_line', source='daily, finance_inputs'),
                    _ev('contribution_before_media', w['before_media'], 'usd', end, source='daily, finance_inputs')]
        kept = (f'loses ${-w["contribution"]:,.2f}' if w['contribution'] < 0 else f'keeps ${w["contribution"]:,.2f}')
        sentence = f'{w["name"]} {kept} after paid media, under the red line of {line_text}.'
        out.append(_finding('OFFER-R10', entity, 'high', evidence, sentence, None, 0.6, [], end,
                            money_reason='the share of orders on this offer needs order rows'))
    return out


def promo_calendar(rd):
    pb = _playbook()
    return _model().promo_calendar(rd, pb.PROMO_WINDOWS, pb.PROMO_ALERT_DAYS)


def rule_promo(rd):
    end = rd.ends_on
    cm = _model().contribution_28d(rd)
    share = cm.get('before_media_share')
    out = []
    for w in promo_calendar(rd):
        if not w['due']:
            continue
        ly = w['last_year']
        money, reason = None, 'last year is not in the daily aggregate'
        if ly and ly['lift'] is not None:
            days = (date.fromisoformat(ly['end']) - date.fromisoformat(ly['start'])).days + 1
            extra = round((ly['net_per_day'] - ly['baseline_per_day']) * days, 2)
            if extra > 0:
                money = {'usd_revenue': extra, 'usd': round(extra * share, 2) if share else None,
                         'formula': '(net_per_day_window - net_per_day_28d_before) x days x contribution_before_media_share',
                         'inputs': {'net_per_day_window': ly['net_per_day'], 'net_per_day_28d_before': ly['baseline_per_day'],
                                    'days': days, 'contribution_before_media_share': share}, 'window': 'last year'}
                if money['usd'] is None:
                    money['usd'] = extra
            else:
                reason = 'last year the window sold no more than the 28 days before it'
        entity = {'type': 'offer', 'id': 'window_' + w['key'], 'label': w['name']}
        evidence = [_ev('days_to_approval', w['days_to_approve'], 'days', end, baseline=_playbook().PROMO_ALERT_DAYS,
                        baseline_kind='threshold', window='calendar', source='playbook.PROMO_WINDOWS'),
                    _ev('plan_in_brain', 0, 'count', end, baseline=1, baseline_kind='threshold', window='brain', source='brain.plans')]
        if ly:
            evidence.append(_ev('window_lift_last_year', ly['lift'], 'ratio', end, baseline=0, baseline_kind='28d_before',
                                window=f'{ly["start"]} to {ly["end"]}', source='daily'))
            evidence.append(_ev('discount_depth_last_year', ly['depth'], 'ratio', end, baseline=ly['baseline_depth'],
                                baseline_kind='28d_before', window=f'{ly["start"]} to {ly["end"]}', source='daily'))
        when = f'{w["days_to_approve"]} days' if w['days_to_approve'] >= 0 else f'{-w["days_to_approve"]} days ago'
        sentence = f'{w["name"]} starts {w["start"]}. The offer must be approved by {w["approve_by"]} ({when}) and none is planned.'
        if ly and ly['lift'] is not None:
            sentence += f' Last year it sold {ly["lift"] * 100:.0f} percent above the 28 days before.'
        out.append(_finding('OFFER-R11', entity, 'high' if w['days_to_approve'] <= 14 else 'medium', evidence, sentence,
                            money, 0.7, [], end, money_reason=None if money else reason))
    return out


def gifting(rd):
    pb = _playbook()
    return _model().gifting(rd, pb.GIFT_LED_RATIO, pb.GIFT_DAY)


def rule_gifting(rd):
    end = rd.ends_on
    g = gifting(rd)
    out = []
    if g['ledger']['unavailable'] and (g['gift_card'] or g['program']):
        out.append(_finding('OFFER-R13', {'type': 'metric', 'id': 'gift_card_liability', 'label': 'Gift card liability'}, 'low', [],
                            'Gift card liability and redemption are unknown: the gift card ledger is not connected.', None,
                            0.1, [g['gift_card_id']] if g['gift_card_id'] else [], end, status='unavailable',
                            money_reason='no ledger', unavailable={'inputs': ['gift_card_ledger'], 'connector': 'shopify',
                                                                  'fix': g['ledger']['fix']}))
    if not (g['program'] or g['gift_card']) or g['store_q4_share'] is None or not g['lines'] or any(r['gift_led'] for r in g['lines']):
        return out
    top = max(g['lines'], key=lambda r: r['index'] or 0)
    evidence = [_ev('best_line_holiday_index', top['index'], 'ratio', end, baseline=_playbook().GIFT_LED_RATIO,
                    baseline_kind='threshold', window=g['months'], source='products_monthly, monthly'),
                _ev('store_nov_dec_share', g['store_q4_share'], 'ratio', end, window=g['months'], source='monthly')]
    sentence = (f'No line sells more at the holidays than the store does. The best holiday index is {top["index"]:.2f} '
                f'against a {_playbook().GIFT_LED_RATIO:.1f} bar, so the gift program is not pulling.')
    refs = [x for x in (g['program_id'], g['gift_card_id']) if x]
    out.append(_finding('OFFER-R12', {'type': 'offer', 'id': 'gifting', 'label': 'Gifting'}, 'medium', evidence, sentence,
                        None, 0.6, refs, end, money_reason='gift sales are not tagged apart from other sales'))
    return out


def guarantee(rd):
    pb = _playbook()
    return _model().guarantee(rd, pb.GUARANTEE_KEYS, pb.PAGE_TYPES, pb.SELLING_PAGES)


def rule_guarantee(rd):
    end = rd.ends_on
    pb = _playbook()
    g = guarantee(rd)
    out = []
    if not g['terms']:
        return out
    refs = [t['id'] for t in g['terms']]
    if not g['on_selling_page'] and g['answers']:
        evidence = [_ev('guarantee_on_selling_pages', 0, 'count', end, baseline=1, baseline_kind='threshold', window='brain',
                        source='brain source urls'),
                    _ev('one_star_mentions_it_answers', g['one_star_answered'], 'count', end, window='ladder',
                        source='brain.objection_ladders')]
        sentence = (f'The guarantee answers {len(g["answers"])} ladder doubts with {g["one_star_answered"]} one-star '
                    f'mentions, but the brain finds it only on the {", ".join(g["stated_on"])}.')
        out.append(_finding('OFFER-R14', {'type': 'offer', 'id': 'guarantee_placement', 'label': 'The guarantee'}, 'medium',
                            evidence, sentence, None, 0.6, refs, end,
                            money_reason='lost orders from an unseen guarantee are not measurable'))
    m = rd.m('returns_by_reason', WINDOW)
    if m.get('unavailable'):
        out.append(_finding('OFFER-R15', {'type': 'offer', 'id': 'guarantee_claims', 'label': 'Guarantee claims'}, 'low', [],
                            'Guarantee claims against the planned rate are unknown: returns by reason are not connected.',
                            None, 0.1, refs, end, status='unavailable', money_reason='no returns',
                            unavailable={'inputs': ['reversed_orders'], 'connector': m.get('fix') or 'shopify',
                                         'fix': 'Connect store returns, read-only, with the return reason.'}))
        return out
    plan = g['planned']['refund_or_replace']
    orders = m['inputs']['paid_orders']
    if plan and orders:
        rate = m['value'] / orders
        if rate > pb.CLAIM_OVER_PLAN * plan:
            evidence = [_ev('returns_per_order', round(rate, 6), 'ratio', end, baseline=plan, baseline_kind='plan',
                            source='reversed_orders')]
            sentence = (f'Returns and replacements run at {rate * 100:.1f} percent of orders against a planned '
                        f'{plan * 100:.1f} percent.')
            out.append(_finding('OFFER-R15', {'type': 'offer', 'id': 'guarantee_claims', 'label': 'Guarantee claims'}, 'high',
                                evidence, sentence, None, 0.7, refs, end, money_reason='cost per claim is in the action'))
    return out


def competitor_position(rd):
    return _model().competitor_position(rd, _playbook().PROOF_HOOK_WORDS)


def rule_position(rd):
    end = rd.ends_on
    pb = _playbook()
    cp = competitor_position(rd)
    us = cp['us']
    if not us or us['price'] is None or cp['set_median_price'] is None or us['code_share'] is None:
        return []
    proof_led = [c for c in cp['competitors'] if c['price'] is not None and c['price'] > us['price'] and c['discount_in_ads'] == 0]
    if not (us['price'] < cp['set_median_price'] and us['code_share'] > pb.CODE_ADS_SHARE and len(proof_led) >= pb.MIN_PROOF_LED):
        return []
    evidence = [_ev('price_per_item', us['price'], 'usd', end, baseline=cp['set_median_price'], baseline_kind='competitor_median',
                    window='12 full months', source='products_monthly, brain.competitors'),
                _ev('ads_with_code', us['code_share'], 'ratio', end, baseline=pb.CODE_ADS_SHARE, baseline_kind='threshold',
                    window='active ads', source='brain.offers.promo_share_active_ads'),
                _ev('proof_led_competitors_priced_above', len(proof_led), 'count', end, baseline=pb.MIN_PROOF_LED,
                    baseline_kind='threshold', window='brain', source='brain.competitors')]
    names = ', '.join(c['name'] for c in proof_led[:3])
    sentence = (f'We sell at ${us["price"]:,.2f} an item, under the set median of ${cp["set_median_price"]:,.0f}, and put a '
                f'{us["discount_in_ads"]:.0f} percent code in {us["code_share"] * 100:.0f} percent of ads. {names} charge more '
                f'and show no discount.')
    return [_finding('OFFER-R16', {'type': 'offer', 'id': 'price_position', 'label': 'Price and offer position'}, 'medium',
                     evidence, sentence, None, 0.5, [c['id'] for c in proof_led], end,
                     money_reason='the price a proof-led message could hold is what the ads test finds')]


def marketplace_parity(rd):
    pb = _playbook()
    return _model().marketplace_parity(rd, pb.PACK_PATTERNS, pb.PARITY_GAP)


def rule_parity(rd):
    end = rd.ends_on
    mp = marketplace_parity(rd)
    under = [r for r in mp['rows'] if r['undercut']]
    if not under:
        return []
    compared = [r for r in mp['rows'] if r['gap'] is not None]
    worst = min(under, key=lambda r: r['gap'])
    evidence = [_ev('listings_under_site_price', len(under), 'count', end, baseline=len(compared), baseline_kind='listings_compared',
                    window='brain', source='brain.marketplaces, products_monthly'),
                _ev('deepest_gap', worst['gap'], 'ratio', end, baseline=-_playbook().PARITY_GAP, baseline_kind='threshold',
                    window='brain', source='brain.marketplaces')]
    unknown = sum(1 for r in under if not r['seller'])
    sentence = (f'{len(under)} of {len(compared)} marketplace listings sell under the site price per item by more than '
                f'{_playbook().PARITY_GAP * 100:.0f} percent, down to {-worst["gap"] * 100:.0f} percent. Seller unknown on {unknown}.')
    return [_finding('OFFER-R17', {'type': 'offer', 'id': 'marketplace_parity', 'label': 'Marketplace price parity'}, 'medium',
                     evidence, sentence, None, 0.5, [r['id'] for r in under], end,
                     money_reason='the sales these listings take from the site are not in the data')]


def discipline(rd):
    return _model().discount_discipline(rd, _playbook().PROMO_DAY_RATIO)


def rule_discount(rd):
    end = rd.ends_on
    pb = _playbook()
    out = []
    mrows = [r for r in (rd.table('monthly') or []) if r.get('gross_sales')]
    fm = set(_model().full_months(rd, end, 60))
    full = [r for r in mrows if r['month'] in fm]
    if len(full) >= 4:
        a, b = full[-4], full[-1]
        sa, sb = a['discounts'] / a['gross_sales'], b['discounts'] / b['gross_sales']
        pts = (sb - sa) * 100
        if pts > pb.CREEP_POINTS:
            money = {'usd': round((sb - sa) * b['gross_sales'], 2), 'formula': '(share_now - share_3_months_before) x gross_last_month',
                     'inputs': {'share_now': round(sb, 4), 'share_3_months_before': round(sa, 4), 'gross_last_month': b['gross_sales']},
                     'window': b['month']}
            ev = [_ev('discount_share_of_gross', round(sb, 4), 'ratio', end, baseline=round(sa, 4), baseline_kind='3_months_before',
                      window=b['month'], source='monthly')]
            out.append(_finding('OFFER-R18', {'type': 'offer', 'id': 'discount_creep', 'label': 'Discount share'}, 'high', ev,
                                f'Discounts went from {sa * 100:.1f} to {sb * 100:.1f} percent of gross between {a["month"]} and {b["month"]}.',
                                money, 0.8, [], end))
    d = discipline(rd)
    ty = d['this_year']
    share, _ = _model().brain_value(rd, 'offers.promo_share_active_ads')
    code_share = share['ads_with_code'] / share['active_ads'] if isinstance(share, dict) and share.get('active_ads') else None
    if ty and ty['always_on_share'] is not None and ty['always_on_share'] > pb.ALWAYS_ON and code_share and code_share > pb.CODE_ADS_SHARE:
        ev = [_ev('discount_dollars_on_ordinary_days', ty['always_on_share'], 'ratio', end, baseline=pb.ALWAYS_ON,
                  baseline_kind='threshold', window='365d', source='daily'),
              _ev('promo_days', ty['promo_days'], 'count', end, window='365d', source='daily')]
        out.append(_finding('OFFER-R19', {'type': 'offer', 'id': 'always_on', 'label': 'Always-on discount'}, 'medium', ev,
                            f'{ty["always_on_share"] * 100:.0f} percent of the year\'s ${ty["discount_dollars"]:,.0f} in discounts went out on '
                            f'ordinary days, not in the {ty["promo_days"]} promo days. The code is the discount program.',
                            None, 0.6, [f'{rd.brand}.offers.first_order_code'], end,
                            money_reason='priced by the first-order code test'))
    return out


def rule_ladder(rd):
    end = rd.ends_on
    pb = _playbook()
    lad, rows = ladder_moves(rd)
    if lad.get('unavailable'):
        entity = {'type': 'sku', 'id': 'pack_ladder', 'label': 'Pack ladder'}
        return [_finding('OFFER-R07', entity, 'medium', [], 'The pack ladder cannot be read: ' + lad['reason'] + '.', None,
                         0.1, [], end, status='unavailable', money_reason='no product sales',
                         unavailable={'inputs': ['products_monthly'], 'connector': lad.get('fix') or 'shopify',
                                      'fix': 'Connect the store orders, read-only, so sales by SKU can be read.'})]
    out = []
    refs = [f'{rd.brand}.offers.bundles_pack_ladder'] if rd.brand else []
    for r in rows:
        name = r['line']
        if r['verdict'] in ('push', 'deepen'):
            entity = {'type': 'sku', 'id': name, 'label': f'{name}: single and {r["pack"]}-pack'}
            evidence = [_ev('pack_saving_per_item', r['saving'], 'ratio', end, baseline=pb.MIN_SAVING, baseline_kind='threshold',
                            window='12 full months', source='products_monthly'),
                        _ev('single_share_of_packs', r['single_share'], 'ratio', end, baseline=pb.SINGLE_SHARE_PUSH,
                            baseline_kind='threshold', window='12 full months', source='products_monthly')]
            if r['trade_up_needed'] is not None:
                evidence.append(_ev('trade_up_needed_for_deeper_price', r['trade_up_needed'], 'ratio', end,
                                    baseline=pb.VIABLE_TRADE_UP, baseline_kind='threshold', window='12 full months',
                                    source='products_monthly, finance_inputs.cogs_landed'))
            sentence = (f'{name}: the {r["pack"]}-pack saves {r["saving"] * 100:.1f} percent per item and singles are '
                        f'{r["single_share"] * 100:.0f} percent of packs sold.')
            sev = 'high' if r['single_share'] > pb.SINGLE_SHARE_PUSH and r['weak'] else 'medium'
            out.append(_finding('OFFER-R07', entity, sev, evidence, sentence, None, 0.7, refs, end,
                                money_reason='the trade-up rate is what the change finds; the arithmetic is in the action'))
        elif r['verdict'] == 'add':
            entity = {'type': 'sku', 'id': name, 'label': f'{name}: single only'}
            evidence = [_ev('packs_sold', r['single_packs'], 'count', end, window='12 full months', source='products_monthly'),
                        _ev('multi_pack_rungs', 0, 'count', end, baseline=1, baseline_kind='threshold', window='catalogue',
                            source='products_monthly')]
            sentence = (f'{name} sells {r["single_packs"]:,} singles a year and has no multi-pack. '
                        f'Basics are bought in multiples.')
            out.append(_finding('OFFER-R09', entity, 'medium', evidence, sentence, None, 0.6, refs, end,
                                money_reason='a new pack has no sales yet; margin per pack is in the action'))
    return out


def sku_join(rd):
    """(matched, product_skus, cogs_skus) between finance_inputs cogs_landed and the products table."""
    f = rd.fin()
    cogs = sorted({str(r.get('scope_key')) for r in (f.rows if f else []) if r.get('field') == 'cogs_landed'})
    products = rd.table('products') or []
    skus = sorted({str(p.get('sku')) for p in products if p.get('sku')})
    if not skus:
        skus = sorted({r['sku'] for r in (rd.table('products_monthly') or []) if r.get('sku')})
    return sorted(set(cogs) & set(skus)), skus, cogs


def rule_sku_margin(rd):
    matched, skus, cogs = sku_join(rd)
    if matched and len(matched) == len(skus):
        return []
    end = rd.ends_on
    entity = {'type': 'metric', 'id': 'margin_after_discount', 'label': 'Margin after discount, per SKU'}
    sentence = (f'Margin per SKU is unavailable. {len(matched)} of {len(skus)} store SKUs have a landed cost '
                f'on file; the cost sheet uses other SKU codes.')
    return [_finding('OFFER-R03', entity, 'medium', [], sentence, None, 0.1, [], end, status='unavailable',
                     money_reason='COGS does not join to products',
                     unavailable={'inputs': ['finance_inputs.cogs_landed', 'products.sku'], 'connector': 'finance_inputs',
                                  'fix': (f'Key cogs_landed by the store SKU (for example {skus[0] if skus else "the SKU"}); '
                                          f'the sheet uses codes like {cogs[0] if cogs else "none"}.')})]


def ladder_rungs(rd):
    """The top rung of every ladder, with its proof state. Shared with the guarantee table in api.py."""
    out = []
    for rec in rd.records('objection_ladders'):
        v = rec.get('value') or {}
        rungs = v.get('rungs') or []
        if not rungs:
            continue
        top = max(rungs, key=lambda r: r.get('level') or 0)
        counts = top.get('counts') or {}
        out.append({'ladder': rec['id'], 'theme': v.get('theme'), 'level': top.get('level'), 'levels': len(rungs),
                    'doubt': top.get('doubt'), 'one_star': counts.get('one_star') or 0,
                    'five_star': counts.get('five_star') or 0, 'by_star': counts.get('by_star'),
                    'sources': counts.get('sources'), 'proof': None if is_proofless(top.get('proof')) else top.get('proof'),
                    'proof_ids': top.get('proof_ids') or [], 'open_question': top.get('open_question'),
                    'reasons': list(THEME_REASONS.get(v.get('theme'), ()))})
    out.sort(key=lambda r: (r['proof'] is not None, -r['one_star']))
    return out


def returns_windows(rd):
    """returns_by_reason for the current and 4 trailing 28-day windows, newest first."""
    return [rd.m('returns_by_reason', WINDOW, rd.ends_on - timedelta(days=WINDOW * k)) for k in range(TRAILING + 1)]


def reason_stats(windows, reasons):
    """(returns now, per-order rate now, own median rate over the 4 windows before, average refund now)."""
    now = windows[0]
    if not reasons:
        return None
    if now.get('unavailable'):
        return {'unavailable': True, 'reason': now.get('reason'), 'fix': now.get('fix')}
    def pick(w):
        gs = [g for g in w['groups'] if g['reason'] in reasons]
        return sum(g['returns'] for g in gs), sum(g['amount'] for g in gs), w['inputs']['paid_orders']
    n, amt, orders = pick(now)
    prev = [pick(w) for w in windows[1:] if not w.get('unavailable')]
    median = round(statistics.median(p[0] / p[2] for p in prev if p[2]), 6) if len(prev) == TRAILING else None
    return {'returns': n, 'rate': round(n / orders, 6) if orders else None, 'median': median,
            'avg_refund': round(amt / n, 2) if n else None, 'windows': len(prev)}


def rule_unanswered(rd):
    end = rd.ends_on
    out = []
    rungs = [r for r in ladder_rungs(rd) if r['proof'] is None and r['one_star'] > 0]
    if not rungs:
        return out
    windows = returns_windows(rd)
    aov = rd.m('aov', WINDOW)
    orders_28d = None if aov.get('unavailable') else aov['inputs']['orders']
    net_28d = None if aov.get('unavailable') else aov['inputs']['net_revenue']
    f = rd.fin()
    fee = f.value('returns_processing', end.isoformat()) if f else None
    for r in rungs:
        theme = r['theme']
        entity = {'type': 'ladder_rung', 'id': f'{theme}.deal_breaker',
                  'label': f'{theme.replace("_", " ").capitalize()}: {r["doubt"]}'}
        evidence = [_ev('one_star_mentions', r['one_star'], 'count', end, source='brain.objection_ladders',
                        window='ladder'),
                    _ev('proof_on_file', 0, 'count', end, baseline=1, baseline_kind='threshold',
                        source='brain.objection_ladders', window='ladder')]
        st = reason_stats(windows, r['reasons'])
        money, reason, second = None, None, ''
        if st is None:
            reason = 'proof gap: no return reason maps to this rung, lost orders not measurable'
        elif st.get('unavailable'):
            reason = f'returns by reason are unavailable ({st["reason"]}); lost orders not measurable'
        else:
            evidence.append(_ev('returns_per_order', st['rate'], 'ratio', end, baseline=st['median'],
                                baseline_kind='own_median' if st['median'] is not None else None,
                                source='reversed_orders'))
            per_k, med_k = st['rate'] * 1000, (st['median'] or 0) * 1000
            second = f' Returns for {" or ".join(r["reasons"])} run {per_k:.1f} per 1,000 orders'
            second += f', own median {med_k:.1f}.' if st['median'] is not None else '.'
            if st['median'] is None:
                reason = 'no baseline'
            elif st['rate'] <= st['median'] * (1 + RETURNS_NOISE):
                reason = 'proof gap: returns within 5 percent of own median, lost orders not measurable'
            elif orders_28d is None or fee is None or st['avg_refund'] is None:
                reason = 'returns cost inputs missing (orders, returns_processing or refunds)'
            else:
                excess = round((st['rate'] - st['median']) * orders_28d)
                usd = round(excess * (st['avg_refund'] + fee), 2)
                money = {'usd': usd, 'formula': '(rate_now - rate_median) x orders_28d x (avg_refund + returns_processing)',
                         'inputs': {'rate_now': st['rate'], 'rate_median': st['median'], 'orders_28d': orders_28d,
                                    'avg_refund': st['avg_refund'], 'returns_processing': fee},
                         'window': '28d', 'floor': True,
                         'note': 'proof gap: returns only, lost orders not measurable'}
        sentence = (f'{r["one_star"]} one-star mentions ask "{r["doubt"]}" and nothing public answers it.{second}')
        if len(sentence.split()) > 40:
            sentence = f'{r["one_star"]} one-star mentions ask "{r["doubt"]}" and nothing public answers it.'
        stake = money['usd'] if money else None
        sev = ('high' if (stake is not None and net_28d and stake > 0.01 * net_28d) or r['one_star'] >= TOP_DOUBT
               else 'medium')
        out.append(_finding('OFFER-R04', entity, sev, evidence, sentence, money, 0.5, [r['ladder']], end,
                            money_reason=reason))
    return out


def run(brand, window=None, data=None):
    """Findings for one brand, sorted by severity then money at stake. `window` is {ends_on} or None."""
    ends_on = date.fromisoformat(window['ends_on']) if window and window.get('ends_on') else last_full_day(data, brand)
    rd = Reader(data, brand, ends_on)
    out = (rule_threshold(rd) + rule_stale(rd) + rule_pull(rd) + rule_first_order(rd) + rule_red_line(rd) + rule_promo(rd) + rule_gifting(rd) + rule_guarantee(rd) + rule_position(rd) + rule_parity(rd) + rule_discount(rd) + rule_ladder(rd) + rule_sku_margin(rd) +
           rule_unanswered(rd))
    out.sort(key=lambda f: (SEVERITY_ORDER[f['severity']], -((f.get('money_at_stake') or {}).get('usd') or -1), f['id']))
    return out
