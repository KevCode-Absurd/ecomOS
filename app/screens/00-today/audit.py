"""Audit for 00-today: where the buy path is broken, with proof and money at stake.

Findings follow app/contracts/audit.md. Every number comes from app/metrics.py
(money_at_stake, aov). No connector, no model, no wall clock: the same tables and
window give the same findings.

Rules
  TODAY-R01  Pipeline break. Owner: 00-today.
             For each stage (product view, add to cart, checkout, purchase) the step rate
             in the current window against the median of the 6 windows before it
             (metrics.money_at_stake). Fires when the rate sits more than MIN_GAP_REL
             below that median. Stake = (median - current) x volume into the stage x value
             per unit downstream. Severity: critical over 5 percent of net revenue in the
             window, high over 1 percent or when 2 or more windows agree, else medium.
             Inputs: sessions (GA4), daily aggregate (orders). Capability: per stage, STAGES.
  TODAY-R02  Trend alert. Owner: 00-today.
             A stage rate has fallen 2 windows running (current below the window before,
             which is below the one before that). Severity medium. The stake sits on
             TODAY-R01, so money is null here. Capability DIAG-C03.
"""
import importlib.util
import sys
from datetime import date, timedelta
from pathlib import Path

APP = Path(__file__).resolve().parents[2]
SCREEN = '00-today'
MIN_GAP_REL = 0.01          # below 1 percent of the median is noise, no finding
AGREE_WINDOWS = 4           # windows checked for agreement (current plus 3 before)
FRESHNESS_DAYS = 1          # generated data is captured the morning after the last full day

# stage: label, what enters it, verb, capability that fixes it
STAGES = {
    'product_view': {'label': 'Product views', 'into': 'sessions', 'rate': 'of sessions view a product',
                     'capability': {'id': 'SITE-C55', 'autonomy': 'human_assist'}},
    'add_to_cart': {'label': 'Add to cart', 'into': 'product_view', 'rate': 'of product viewers add to cart',
                    'capability': {'id': 'SITE-C38', 'autonomy': 'human_assist'}},
    'checkout': {'label': 'Checkout', 'into': 'add_to_cart', 'rate': 'of carts reach checkout',
                 'capability': {'id': 'SITE-C18', 'autonomy': 'human_assist'}},
    'purchase': {'label': 'Purchase', 'into': 'checkout', 'rate': 'of checkouts become orders',
                 'capability': {'id': 'SITE-C67', 'autonomy': 'founder_gate'}},
}

RULES = [
    {'rule_id': 'TODAY-R01', 'name': 'Pipeline break with money at stake', 'entity_type': 'stage',
     'inputs': ['sessions', 'aggregates/daily'], 'capability': 'per stage: ' + ', '.join(
         f"{k} {v['capability']['id']}" for k, v in STAGES.items()), 'owner_screen': SCREEN},
    {'rule_id': 'TODAY-R02', 'name': 'Stage rate fell 2 windows running', 'entity_type': 'stage',
     'inputs': ['sessions', 'aggregates/daily'], 'capability': 'DIAG-C03', 'owner_screen': SCREEN},
]
SEVERITY_ORDER = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}


def metrics_module():
    """The server's metrics module when loaded, else app/metrics.py loaded here."""
    mod = sys.modules.get('ecomos_metrics')
    if mod is None:
        spec = importlib.util.spec_from_file_location('ecomos_metrics', APP / 'metrics.py')
        mod = importlib.util.module_from_spec(spec)
        sys.modules['ecomos_metrics'] = mod
        spec.loader.exec_module(mod)
    return mod


def usd(x):
    return f'${round(x):,}'


def pct(x):
    return f'{x * 100:.{2 if x < 0.1 else 1}f} percent'


def day_label(iso):
    d = date.fromisoformat(iso)
    return f'{d.day} {d.strftime("%b")}'


def normal_window(brand, window, M):
    data = M.resolve(None, {'brand': brand})
    w = dict(window or {})
    ends_on = w.get('ends_on') or data.brand['as_of']
    return {'ends_on': ends_on, 'days': int(w.get('days') or 28), 'trailing': int(w.get('trailing') or 4)}


def unavailable_finding(rule_id, brand, window, reason, fix, severity):
    return {
        'id': f'{SCREEN}.{rule_id}.{brand}', 'screen': SCREEN, 'rule_id': rule_id, 'severity': severity,
        'entity': {'type': 'brand', 'id': brand, 'label': brand.capitalize()}, 'evidence': [],
        'sentence': f'The pipeline cannot be called healthy or broken: {reason}.',
        'capability': {'id': 'DIAG-C02', 'autonomy': 'agent_does'},
        'money_at_stake': None, 'money_reason': 'inputs unavailable', 'confidence': 0.1, 'brain_refs': [],
        'first_seen': window['ends_on'], 'last_seen': window['ends_on'], 'status': 'unavailable',
        'unavailable': {'inputs': ['sessions', 'aggregates/daily'], 'connector': fix or 'ga4',
                        'fix': 'Connect GA4 and Shopify, or rebuild the simulated tables with app/data/generate.py.'},
    }


def run(brand, window=None):
    """Findings for this screen, sorted by severity then stake. window: {ends_on, days, trailing}."""
    M = metrics_module()
    w = normal_window(brand, window, M)
    q = {'brand': brand, 'window': f"{w['days']}d"}
    ends = [(date.fromisoformat(w['ends_on']) - timedelta(days=w['days'] * k)).isoformat() for k in range(AGREE_WINDOWS)]
    runs = [M.compute('money_at_stake', None, end=e, **q) for e in ends]
    cur = runs[0]
    if cur.get('unavailable'):
        return [unavailable_finding('TODAY-R01', brand, w, cur.get('reason'), cur.get('fix'), 'high')]
    aov = M.compute('aov', None, end=w['ends_on'], **q)
    net = (aov.get('inputs') or {}).get('net_revenue')
    source = next((s['captured_at'] for s in cur['freshness']['sources'] if s.get('captured_at')), None)
    findings = []
    for s in cur['stages']:
        meta = STAGES[s['stage']]
        # windows agreeing: the current window and each one before it, while it stays below its own median
        agree, since = 0, w['ends_on']
        history = []
        for r in runs:
            st = None if r.get('unavailable') else next(x for x in r['stages'] if x['stage'] == s['stage'])
            history.append(st)
        for r, st in zip(runs, history):
            if st is None or st['current'] >= st['median']:
                break
            agree += 1
            since = r['window']['start']
        ev_base = {'window': f"{w['days']}d", 'ends_on': w['ends_on'], 'freshness_days': FRESHNESS_DAYS,
                   'source': 'sessions, aggregates/daily', 'simulated': True}
        evidence = [
            dict(ev_base, metric=f"{s['stage']}_step_rate", value=s['current'], unit='ratio',
                 baseline=s['median'], baseline_kind='own_median'),
            dict(ev_base, metric=f"{meta['into']}_count", value=s['volume'], unit='count', baseline=None, baseline_kind='threshold'),
            dict(ev_base, metric='value_per_unit', value=s['value_per_unit'], unit='usd', baseline=None, baseline_kind='threshold'),
        ]
        if net is not None:
            evidence.append(dict(ev_base, metric='net_revenue', value=net, unit='usd', baseline=None, baseline_kind='threshold'))
        confidence = 0.9 if agree >= 4 else 0.7 if agree >= 2 else 0.5

        # TODAY-R01
        if s['median'] and s['gap'] > MIN_GAP_REL * s['median']:
            share = s['money'] / net if net else None
            severity = ('critical' if share is not None and share > 0.05 else
                        'high' if (share is not None and share > 0.01) or agree >= 2 else 'medium')
            findings.append({
                'id': f"{SCREEN}.TODAY-R01.{s['stage']}", 'screen': SCREEN, 'rule_id': 'TODAY-R01', 'severity': severity,
                'entity': {'type': 'stage', 'id': s['stage'], 'label': meta['label']}, 'evidence': evidence,
                'sentence': (f"{meta['label']} is costing about {usd(s['money'])} in the {w['days']} days to "
                             f"{day_label(w['ends_on'])}. {pct(s['current'])} {meta['rate']}, against a median of "
                             f"{pct(s['median'])}. Below it since {day_label(since)}."),
                'capability': meta['capability'],
                'money_at_stake': {'usd': round(s['money']), 'formula': '(median_rate - current_rate) x volume_in x value_per_unit',
                                   'inputs': {'median_rate': s['median'], 'current_rate': s['current'],
                                              'volume_in': s['volume'], 'value_per_unit': s['value_per_unit']},
                                   'window': f"{w['days']}d"},
                'confidence': confidence, 'brain_refs': [],
                'first_seen': since, 'last_seen': w['ends_on'], 'status': 'open', 'unavailable': None,
                'share_of_net_revenue': round(share, 6) if share is not None else None,
                'windows_agreeing': agree, 'source_captured_at': source,
            })

        # TODAY-R02
        rates = [h['current'] if h else None for h in history[:3]]
        if None not in rates and rates[0] < rates[1] < rates[2]:
            findings.append({
                'id': f"{SCREEN}.TODAY-R02.{s['stage']}", 'screen': SCREEN, 'rule_id': 'TODAY-R02', 'severity': 'medium',
                'entity': {'type': 'stage', 'id': s['stage'], 'label': meta['label']},
                'evidence': [dict(ev_base, metric=f"{s['stage']}_step_rate", value=r, unit='ratio', ends_on=e,
                                  baseline=None, baseline_kind='threshold') for r, e in zip(rates, ends)],
                'sentence': (f"{meta['label']} has moved down for 2 windows running: {pct(rates[2])}, "
                             f"then {pct(rates[1])}, now {pct(rates[0])}."),
                'capability': {'id': 'DIAG-C03', 'autonomy': 'agent_does'},
                'money_at_stake': None, 'money_reason': 'trend only; the stake is on TODAY-R01',
                'confidence': 0.7, 'brain_refs': [],
                'first_seen': runs[2]['window']['start'], 'last_seen': w['ends_on'], 'status': 'open', 'unavailable': None,
            })
    findings.sort(key=lambda f: (SEVERITY_ORDER[f['severity']], -((f['money_at_stake'] or {}).get('usd') or -1)))
    return findings


if __name__ == '__main__':
    import json
    print(json.dumps(run(sys.argv[1] if len(sys.argv) > 1 else 'bombas'), indent=1))
