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
  OFFER-R03  Margin after discount per SKU. Needs cogs_landed keyed by the store's SKUs. Unavailable while no
             finance_inputs SKU key matches a product SKU. Capability MONEY-C05 (founder gate). Owner: 04.
  OFFER-R04  A deal-breaker rung with no proof: the top rung of an objection ladder whose proof is empty or
             "no public proof", with one-star mentions. Money, when a return reason maps to the theme: returns
             per paid order now minus the own median of the 4 trailing 28-day windows, times the 28-day order
             total, times (average refund + returns_processing). Lost orders are not measurable, so the money is a
             floor, or null when returns are within 5 percent of the median. Capability LIFE-C36 (founder gate).
             Owner: 04-offers-pricing; 10-copy and 07-landing-pages-cro read it from the findings table.
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
RETURNS_NOISE = 0.05    # returns within 5 percent of the own median carry no money
LABEL_CARRIER = 'usps'  # free standard shipping goes out on the ground carrier
# Return reasons that are the same doubt as a ladder theme. A theme with no reason here has no money.
THEME_REASONS = {'durability': ('hole or defect',), 'fit_and_sizing': ('size or fit',),
                 'order_and_delivery': ('wrong item', 'arrived late')}

RULES = [
    {'rule_id': 'OFFER-R01', 'name': 'Free shipping threshold under break-even', 'entity_type': 'offer',
     'inputs': ['brain.offers.free_shipping_threshold_usd', 'orders', 'finance_inputs.shipping_label',
                'finance_inputs.target_gross_margin'], 'capability': 'MONEY-C05', 'owner_screen': SCREEN},
    {'rule_id': 'OFFER-R03', 'name': 'Margin after discount per SKU', 'entity_type': 'sku',
     'inputs': ['finance_inputs.cogs_landed keyed by product SKU', 'products'], 'capability': 'MONEY-C05',
     'owner_screen': SCREEN},
    {'rule_id': 'OFFER-R04', 'name': 'Deal-breaker objection rung with no proof', 'entity_type': 'ladder_rung',
     'inputs': ['brain.objection_ladders', 'reversed_orders', 'finance_inputs.returns_processing'],
     'capability': 'LIFE-C36', 'owner_screen': SCREEN},
]
CAPABILITY = {'OFFER-R01': {'id': 'MONEY-C05', 'autonomy': 'founder_gate'},
              'OFFER-R03': {'id': 'MONEY-C05', 'autonomy': 'founder_gate'},
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
    if now.get('unavailable') or not reasons:
        return None
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
        sev = 'high' if stake is not None and net_28d and stake > 0.01 * net_28d else 'medium'
        out.append(_finding('OFFER-R04', entity, sev, evidence, sentence, money, 0.5, [r['ladder']], end,
                            money_reason=reason))
    return out


def run(brand, window=None, data=None):
    """Findings for one brand, sorted by severity then money at stake. `window` is {ends_on} or None."""
    ends_on = date.fromisoformat(window['ends_on']) if window and window.get('ends_on') else last_full_day(data, brand)
    rd = Reader(data, brand, ends_on)
    out = rule_threshold(rd) + rule_sku_margin(rd) + rule_unanswered(rd)
    out.sort(key=lambda f: (SEVERITY_ORDER[f['severity']], -((f.get('money_at_stake') or {}).get('usd') or -1), f['id']))
    return out
