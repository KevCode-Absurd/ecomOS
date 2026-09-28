"""Audit for 26-reports: is the weekly or monthly report honest and complete.

Findings follow app/contracts/audit.md. The report is built in report.py from
app/metrics.py, the other screens' audits and the brain. No connector, no model, no
wall clock: the same tables, brain and window give the same findings.

Rules (all owned by 26-reports; source: room "Reviews and reports")
  REPORT-R01  A report claim cites no metric. Every line in "what changed" and every top 10
              row that quotes a number must name the contract metric (or the finding's
              evidence metrics) it came from. Fires per claim with a number and no metric.
              Severity medium. Money null: a claim has no stake of its own. LOOP-C01.
  REPORT-R02  A report number differs from the metric contract. The summary sheet (sums of
              the daily aggregate, what a report reads when it skips the contract) against the
              contract for net revenue, orders, Meta spend and Google spend. Fires when the gap
              is over TOLERANCE of the contract value. Stake = the absolute gap in dollars
              (orders: gap x contract AOV). Severity: critical over 5 percent of trailing 28-day
              net revenue, high over 1 percent or when the prior period differs too, else
              medium. LOOP-C41.
  REPORT-R03  A report period with no decisions. No row in the decisions log and no decision
              record in the brain dated inside the period (logged up to the morning the report
              runs). Stake = money at stake of the top 10 findings, none of them decided.
              Severity high over 1 percent of trailing 28-day net revenue, else medium. LOOP-C01.
  REPORT-R04  An unavailable metric shown as a number. A report line marked unavailable that
              carries a value, or a screen finding with status unavailable that carries money
              at stake or evidence values. Severity high. Money null. LOOP-C41.
  REPORT-R05  A screen's audit could not run. The report lists that screen as unavailable and
              keeps going. Status unavailable, severity medium. DIAG-C02.
"""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCREEN = '26-reports'
TOLERANCE = 0.005           # a gap under half a percent of the contract value is rounding
FRESHNESS_DAYS = 1          # generated data is captured the morning after the last full day

RULES = [
    {'rule_id': 'REPORT-R01', 'name': 'Report claim cites no metric', 'entity_type': 'metric',
     'inputs': ['app/metrics.py', 'aggregates/daily', 'other screens findings'], 'capability': 'LOOP-C01', 'owner_screen': SCREEN},
    {'rule_id': 'REPORT-R02', 'name': 'Report number differs from the metric contract', 'entity_type': 'metric',
     'inputs': ['aggregates/daily', 'app/metrics.py aov and spend'], 'capability': 'LOOP-C41', 'owner_screen': SCREEN},
    {'rule_id': 'REPORT-R03', 'name': 'Report period with no decisions', 'entity_type': 'brand',
     'inputs': ['decisions log', 'brain decisions', 'other screens findings'], 'capability': 'LOOP-C01', 'owner_screen': SCREEN},
    {'rule_id': 'REPORT-R04', 'name': 'Unavailable metric shown as a number', 'entity_type': 'metric',
     'inputs': ['app/metrics.py', 'other screens findings'], 'capability': 'LOOP-C41', 'owner_screen': SCREEN},
    {'rule_id': 'REPORT-R05', 'name': 'Screen audit could not run', 'entity_type': 'stage',
     'inputs': ['app/screens/*/audit.py'], 'capability': 'DIAG-C02', 'owner_screen': SCREEN},
]
SEVERITY_ORDER = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
# summary sheet field, contract key, label, unit
RECONCILE = (
    ('net_sales', 'net_revenue', 'Net revenue', 'usd'),
    ('orders', 'orders', 'Orders', 'count'),
    ('meta_spend', 'meta', 'Meta spend', 'usd'),
    ('google_spend', 'google', 'Google spend', 'usd'),
)


def report():
    mod = sys.modules.get('reports_report')
    if mod is None or getattr(mod, '__file__', None) != str(HERE / 'report.py'):
        spec = importlib.util.spec_from_file_location('reports_report', HERE / 'report.py')
        mod = importlib.util.module_from_spec(spec)
        sys.modules['reports_report'] = mod
        spec.loader.exec_module(mod)
    return mod


def usd(x):
    return f'${round(x):,}'


def num(x, unit):
    if unit == 'usd':
        return usd(x)
    if unit == 'count':
        return f'{round(x):,}'
    if unit == 'ratio':
        return f'{x * 100:.1f} percent'
    return f'{x:.2f}x'


def finding(rule_id, severity, entity, sentence, capability, evidence, money, confidence, p, **extra):
    f = {'id': f"{SCREEN}.{rule_id}.{entity['id']}", 'screen': SCREEN, 'rule_id': rule_id, 'severity': severity,
         'entity': entity, 'evidence': evidence, 'sentence': sentence,
         'capability': {'id': capability, 'autonomy': 'agent_does'},
         'money_at_stake': money, 'confidence': confidence, 'brain_refs': extra.pop('brain_refs', []),
         'first_seen': extra.pop('first_seen', p['end']), 'last_seen': p['end'],
         'status': extra.pop('status', 'open'), 'unavailable': extra.pop('unavailable', None)}
    if money is None:
        f['money_reason'] = extra.pop('money_reason', 'no money formula for this rule')
    f.update(extra)
    return f


def ev(p, metric, value, unit, source, baseline=None, baseline_kind='threshold', ends_on=None):
    return {'metric': metric, 'value': value, 'unit': unit, 'window': f"{p['days']}d", 'ends_on': ends_on or p['end'],
            'freshness_days': FRESHNESS_DAYS, 'baseline': baseline, 'baseline_kind': baseline_kind,
            'source': source, 'simulated': True}


def severity_by_share(share, agree=False, floor='medium'):
    if share is not None and share > 0.05:
        return 'critical'
    if (share is not None and share > 0.01) or agree:
        return 'high'
    return floor


def trailing_net(brand, p):
    c = report().contract(brand, p['end'], 28)['net_revenue']
    return None if c.get('unavailable') else c['value']


# ---------------------------------------------------------------- rules

def r01(brand, p, claims):
    out = []
    for c in claims:
        if not c['has_number'] or c.get('metric') or c.get('brain_ref') or c.get('status') == 'unavailable':
            continue
        key = c['id'].split('.', 1)[1]
        value = c.get('value')
        out.append(finding(
            'REPORT-R01', 'medium', {'type': 'metric', 'id': key, 'label': c['label']},
            f"The report states {c['label'].lower()} with no metric behind it. "
            f"It reads the daily summary directly, so the number cannot be checked against the contract.",
            'LOOP-C01',
            [ev(p, key, value, 'ratio' if isinstance(value, float) and value <= 1 else 'number',
                'aggregates/daily (not a contract metric)')],
            None, 0.9, p, money_reason='a claim with no metric has no stake of its own', claim=c['id']))
    return out


def r02(brand, p, net28):
    R = report()
    cur = R.contract(brand, p['end'], p['days'])
    pri = R.contract(brand, p['prior_end'], p['prior_days'])
    sheet = R.summary_sheet(brand, p['start'], p['end'])
    psheet = R.summary_sheet(brand, p['prior_start'], p['prior_end'])
    if sheet.get('unavailable') or cur['net_revenue'].get('unavailable'):
        reason = sheet.get('reason') if sheet.get('unavailable') else cur['net_revenue'].get('reason')
        return [finding('REPORT-R02', 'high', {'type': 'brand', 'id': brand, 'label': brand.capitalize()},
                        f'The report numbers cannot be checked against the contract: {reason}.', 'LOOP-C41', [],
                        None, 0.1, p, status='unavailable', money_reason='inputs unavailable',
                        unavailable={'inputs': ['aggregates/daily', 'orders'], 'connector': 'shopify',
                                     'fix': 'Connect Shopify, or rebuild the simulated tables with app/data/generate.py.'})]

    def contract_value(c, key):
        if key in ('meta', 'google'):
            return (c.get('_by_channel') or {}).get(key)
        v = c.get(key) or {}
        return None if v.get('unavailable') else v.get('value')

    aov = contract_value(cur, 'aov')
    out = []
    for field, key, label, unit in RECONCILE:
        mine, theirs = sheet.get(field), contract_value(cur, key)
        if mine is None or not theirs:
            continue
        gap = abs(mine - theirs)
        if gap <= TOLERANCE * theirs:
            continue
        pm, pt = psheet.get(field), contract_value(pri, key)
        agree = pm is not None and bool(pt) and abs(pm - pt) > TOLERANCE * pt
        if unit == 'usd':
            usd_gap, formula, inputs = gap, 'abs(summary_sheet - contract)', {'summary_sheet': mine, 'contract': theirs}
        elif aov:
            usd_gap, formula = gap * aov, 'abs(summary_orders - contract_orders) x contract_aov'
            inputs = {'summary_orders': mine, 'contract_orders': theirs, 'contract_aov': aov}
        else:
            usd_gap = None
        money = None if usd_gap is None else {'usd': round(usd_gap), 'formula': formula, 'inputs': inputs, 'window': f"{p['days']}d"}
        share = usd_gap / net28 if usd_gap is not None and net28 else None
        rel = gap / theirs
        out.append(finding(
            'REPORT-R02', severity_by_share(share, agree), {'type': 'metric', 'id': key, 'label': label},
            f"{label} in the summary sheet is {num(mine, unit)} for the {p['noun']} to {R.day(p['end']).day} "
            f"{R.day(p['end']).strftime('%b')}. The metric contract says {num(theirs, unit)}, {rel * 100:.1f} percent apart.",
            'LOOP-C41',
            [ev(p, f'{key}_summary_sheet', mine, unit, 'aggregates/daily', baseline=theirs),
             ev(p, f'{key}_contract', theirs, unit, 'app/metrics.py ' + ('spend' if key in ('meta', 'google') else 'aov'))]
            + ([ev(p, f'{key}_summary_sheet', pm, unit, 'aggregates/daily', baseline=pt, ends_on=p['prior_end'])] if agree else []),
            money, 0.7 if agree else 0.5, p, money_reason='no contract AOV to value the gap',
            first_seen=p['prior_start'] if agree else p['start'],
            share_of_net_revenue_28d=round(share, 6) if share is not None else None))
    return out


def r03(brand, p, shipped, top, net28):
    if shipped:
        return []
    undecided = [t for t in top if t['decision']['status'] == 'none' and t['usd'] is not None]
    total = sum(t['usd'] for t in undecided)
    share = total / net28 if net28 else None
    money = {'usd': round(total), 'formula': 'sum of money_at_stake.usd over top 10 findings with no decision',
             'inputs': {t['id']: t['usd'] for t in undecided}, 'window': f"{p['days']}d"} if undecided else None
    R = report()
    return [finding(
        'REPORT-R03', 'high' if share is not None and share > 0.01 else 'medium',
        {'type': 'brand', 'id': f"{p['kind']}_{p['end']}", 'label': f"{brand.capitalize()}, {p['noun']} to {p['end']}"},
        f"No decision was logged for the {p['noun']} from {R.day(p['start']).day} {R.day(p['start']).strftime('%b')} "
        f"to {R.day(p['end']).day} {R.day(p['end']).strftime('%b')}. The top 10 findings hold "
        f"{usd(total)} at stake with no call made.",
        'LOOP-C01',
        [ev(p, 'decisions_in_period', 0, 'count', 'decisions log, brain decisions'),
         ev(p, 'top10_money_at_stake', round(total, 2), 'usd', 'other screens findings')],
        money, 0.9, p, money_reason='no top 10 finding has a money figure')]


def r04(brand, p, report_lines, findings):
    out = []
    for r in report_lines:
        if r['unavailable'] and r['value'] is not None:
            out.append(finding('REPORT-R04', 'high', {'type': 'metric', 'id': r['key'], 'label': r['label']},
                               f"{r['label']} is unavailable but the report shows it as {num(r['value'], r['unit'])}.",
                               'LOOP-C41', [ev(p, r['key'], r['value'], r['unit'], r['source'])], None, 0.9, p,
                               money_reason='a display error has no stake of its own'))
    for f in findings:
        if f.get('status') != 'unavailable':
            continue
        shown = [e for e in f.get('evidence') or [] if isinstance(e, dict) and e.get('value') is not None]
        money = (f.get('money_at_stake') or {}).get('usd')
        if money is None and not shown:
            continue
        what = f'{usd(money)} at stake' if money is not None else f'{len(shown)} evidence values'
        out.append(finding('REPORT-R04', 'high', {'type': 'metric', 'id': str(f.get('id')), 'label': str(f.get('id'))},
                           f"{f.get('screen')} marks {f.get('rule_id')} unavailable but still shows {what}.",
                           'LOOP-C41', [ev(p, 'unavailable_with_values', len(shown) + (money is not None), 'count', f"{f.get('screen')} audit")],
                           None, 0.9, p, money_reason='a display error has no stake of its own'))
    return out


def r05(brand, p, screens):
    out = []
    for s in screens:
        if s['status'] != 'unavailable':
            continue
        out.append(finding('REPORT-R05', 'medium', {'type': 'stage', 'id': s['screen'], 'label': f"Screen {s['screen']}"},
                           f"The {s['screen']} audit could not run, so its findings are missing from this report.",
                           'DIAG-C02', [], None, 0.1, p, status='unavailable', money_reason='inputs unavailable',
                           unavailable={'inputs': [f"app/screens/{s['screen']}/audit.py"], 'connector': s['screen'],
                                        'fix': 'Run that screen audit on its own and fix the error it raises: ' + s['reason']}))
    return out


def evaluate(brand, p):
    """The report pieces and this screen's findings for one period, shared with api.py."""
    R = report()
    rl = R.lines(brand, p)
    sf = R.screen_findings(brand, p)
    decisions = R.decisions_log(brand)
    top = R.top10(sf['findings'], decisions)
    done = R.shipped(brand, p)
    net28 = trailing_net(brand, p)
    cl = R.claims(brand, p, rl, top)
    findings = r01(brand, p, cl) + r02(brand, p, net28) + r03(brand, p, done, top, net28) \
        + r04(brand, p, rl, sf['findings']) + r05(brand, p, sf['screens'])
    findings.sort(key=lambda f: (SEVERITY_ORDER[f['severity']], -((f['money_at_stake'] or {}).get('usd') or -1), f['id']))
    return {'lines': rl, 'screens': sf['screens'], 'screen_findings': sf['findings'], 'top10': top,
            'shipped': done, 'claims': cl, 'net_revenue_28d': net28, 'findings': findings}


def run(brand, window=None):
    """Findings for this screen, sorted by severity then stake. window: {ends_on, days, trailing}."""
    R = report()
    return evaluate(brand, R.from_audit_window(window, brand))['findings']


if __name__ == '__main__':
    import json
    print(json.dumps(run(sys.argv[1] if len(sys.argv) > 1 else 'bombas'), indent=1))
