"""Experiments and memory audit (screen 25, round 0). Findings in the shape of app/contracts/audit.md.

Reads the experiment registry (fixtures/registry.json until the shared `registry` table exists, shape in
app/contracts/events.md), the brain (app/brain/store.py) and app/metrics.py for every outcome number. No connector,
no model call. Same registry, brain and window give the same findings byte for byte.

"Today" is the window end: the brand's last full day. Registry facts (dates, a missing field) are read directly, so
their confidence is 0.9; a rule that also needs a metric window takes that window's confidence.

Rules (owner of all: 25-experiments; other screens read them from the findings table)
  EXP-R01  No pre-registered metric. A running or done entry whose metric is missing, or was registered after the
           start. Capability LOOP-C08 (founder gate). Medium. Money null: no metric, no baseline.
  EXP-R02  Read before its minimum sample. A result whose read_on is fewer than metric.min_days after the start.
           Capability LOOP-C08 (founder gate). Medium. Money null: an early read has no settled effect.
  EXP-R03  Winner not rolled out. A done entry with decision roll_out and no rolled_out_on, more than
           ROLLOUT_GRACE days after the decision. Money, for a returns metric: current returns per paid order for the
           reason (returns_by_reason, 28 days) times the recorded lift, times orders in the window (the aov metric's
           count), times the average refund for that reason. A floor: lost repeat orders are not counted. Other metrics: null with the reason. Severity from stake per the contract.
           Capability REG-C03 (agent does).
  EXP-R04  Learning not written back. An entry with a result whose learnings_ref is empty or is not a record in the
           brain's `learnings` section. Capability REG-C04 (agent does). Medium.
  EXP-R05  Stale hypothesis. A parked entry whose park reason has expired, or a proposed entry older than
           STALE_DAYS with no start. Capability REG-C05 (agent does). Low.
  EXP-R06  Read overdue. A running entry past its read point by more than OVERDUE_GRACE days with no result.
           Capability REG-C02 (agent does). High: the loop is stuck and the wait grows daily.
  EXP-R07  Read point too small. A running entry whose start to read point span is under metric.min_days, or under
           the floor for its metric in MIN_DAYS. Capability LOOP-C08 (founder gate). Medium.
  EXP-R08  Overlap. Two running entries share an audience while their start to read point spans overlap.
           Capability LOOP-C35 (agent does). Medium. Entity is the later-starting entry.
  EXP-R09  Unreadable read. An entry at or past its read point whose metric has no formula in the metric contract, or
           whose metric returns unavailable now. Status `unavailable` with the fix. Capability REG-C03 (agent does).
  EXP-R10  Retro missing. A done entry with no retro. Capability LOOP-C25 (agent does). Low.
"""
import importlib.util
import json
import sys
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parents[1]
SCREEN = '25-experiments'
REGISTRY = HERE / 'fixtures' / 'registry.json'
WINDOW = 28
OVERDUE_GRACE = 3      # days past a read point before an unread entry is overdue ("more than a few days")
ROLLOUT_GRACE = 14     # days after a roll_out decision before it counts as not rolled out
STALE_DAYS = 90        # a proposed entry with no start this old is stale
# Metrics the contract computes, with the floor on days for a real signal (LOOP-C08: slow metrics need longer).
MIN_DAYS = {'aov': 28, 'cvr_overall': 14, 'add_to_cart_rate': 14, 'checkout_rate': 14, 'returns_by_reason': 45,
            'repeat_rate_90d': 90, 'cpa': 14, 'period_roas': 14, 'return_rate': 45}
# How each contract metric is asked for. Anything not here has no formula yet and reads unavailable.
QUERY = {'aov': {}, 'cvr_overall': {}, 'add_to_cart_rate': {}, 'checkout_rate': {}, 'returns_by_reason': {},
         'return_rate': {}, 'repeat_rate_90d': {}, 'cpa': {}, 'period_roas': {}}

CAPABILITY = {'EXP-R01': {'id': 'LOOP-C08', 'autonomy': 'founder_gate'},
              'EXP-R02': {'id': 'LOOP-C08', 'autonomy': 'founder_gate'},
              'EXP-R03': {'id': 'REG-C03', 'autonomy': 'agent_does'},
              'EXP-R04': {'id': 'REG-C04', 'autonomy': 'agent_does'},
              'EXP-R05': {'id': 'REG-C05', 'autonomy': 'agent_does'},
              'EXP-R06': {'id': 'REG-C02', 'autonomy': 'agent_does'},
              'EXP-R07': {'id': 'LOOP-C08', 'autonomy': 'founder_gate'},
              'EXP-R08': {'id': 'LOOP-C35', 'autonomy': 'agent_does'},
              'EXP-R09': {'id': 'REG-C03', 'autonomy': 'agent_does'},
              'EXP-R10': {'id': 'LOOP-C25', 'autonomy': 'agent_does'}}
_NAMES = {'EXP-R01': 'Test with no pre-registered metric', 'EXP-R02': 'Test read before its minimum sample',
          'EXP-R03': 'Winner not rolled out', 'EXP-R04': 'Learning not written back to the brain',
          'EXP-R05': 'Stale hypothesis', 'EXP-R06': 'Read overdue', 'EXP-R07': 'Read point too small',
          'EXP-R08': 'Two running tests overlap', 'EXP-R09': 'Unreadable read', 'EXP-R10': 'Retro missing'}
_INPUTS = {'EXP-R03': ['registry', 'returns_by_reason'], 'EXP-R04': ['registry', 'brain.learnings'],
           'EXP-R09': ['registry', 'metric contract']}
RULES = [{'rule_id': r, 'name': _NAMES[r], 'entity_type': 'metric' if r == 'EXP-R09' else 'experiment',
          'inputs': _INPUTS.get(r, ['registry']), 'capability': CAPABILITY[r]['id'], 'owner_screen': SCREEN}
         for r in CAPABILITY]
SEVERITY_ORDER = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}

_MODS = {}


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def metrics():
    if 'metrics' not in _MODS:
        _MODS['metrics'] = _load('ecomos_metrics_experiments', APP / 'metrics.py')
    return _MODS['metrics']


def brand_data(brand):
    if 'tables' not in _MODS:
        _MODS['tables'] = _load('ecomos_tables_experiments', APP / 'data' / 'tables.py')
    return _MODS['tables'].brand_data(brand)


def brain(brand):
    if not brand or not (APP / 'brain' / brand).is_dir():
        return None
    if 'store' not in _MODS:
        path = str(APP / 'brain')
        if path not in sys.path:
            sys.path.insert(0, path)  # store.py imports validate.py by name
        _MODS['store'] = _load('ecomos_brain_store_experiments', APP / 'brain' / 'store.py')
    return _MODS['store'].Brain(brand)


def registry(brand):
    """Registry entries for one brand. The fixture is the seed until the shared `registry` table exists."""
    if not REGISTRY.is_file():
        return []
    doc = json.loads(REGISTRY.read_text(encoding='utf-8'))
    return [e for e in doc.get('entries', []) if e.get('brand') == brand]


def last_full_day(brand):
    return date.fromisoformat(brand_data(brand).brand['as_of'])


def d(value):
    return date.fromisoformat(value) if value else None


class Reader:
    def __init__(self, brand, ends_on):
        self.brand, self.ends_on = brand, ends_on
        self._brain = brain(brand)
        self._cache = {}

    def m(self, name, days=WINDOW, **kw):
        key = (name, days, tuple(sorted(kw.items())))
        if key not in self._cache:
            q = {'window': f'{days}d', 'end': self.ends_on.isoformat(), 'brand': self.brand, **kw}
            self._cache[key] = metrics().compute(name, None, **q)
        return self._cache[key]

    def record(self, rid):
        return self._brain.get(rid) if self._brain and rid else None

    def entries(self):
        return registry(self.brand)


def outcome(rd, entry):
    """The entry's metric now, from app/metrics.py. {value, unit, unavailable, reason, fix, inputs}."""
    met = entry.get('metric') or {}
    name = met.get('name')
    if not name:
        return {'value': None, 'unavailable': True, 'reason': 'no metric registered', 'fix': 'register a metric'}
    if name not in QUERY:
        return {'value': None, 'unavailable': True, 'reason': f'{name} has no formula in the metric contract',
                'fix': 'add the metric to app/contracts/metrics.md'}
    r = rd.m(name, **QUERY[name])
    if r.get('unavailable'):
        return {'value': None, 'unavailable': True, 'reason': r.get('reason'), 'fix': r.get('fix')}
    if name == 'returns_by_reason' and met.get('reason'):
        g = next((g for g in r.get('groups', []) if g['reason'] == met['reason']), None)
        if not g:
            return {'value': None, 'unavailable': True, 'reason': f'no returns with reason {met["reason"]}',
                    'fix': 'shopify'}
        return {'value': g['per_order'], 'unit': 'ratio', 'unavailable': False,
                'inputs': {'returns': g['returns'], 'amount': g['amount'], 'paid_orders': r['inputs']['paid_orders']},
                'label': f'{met["reason"]} returns per paid order'}
    return {'value': r['value'], 'unit': r.get('unit'), 'unavailable': False, 'inputs': r.get('inputs'),
            'label': name.replace('_', ' ')}


def _ev(metric, value, unit, ends_on, baseline=None, baseline_kind=None, window='registry', source='registry'):
    return {'metric': metric, 'value': value, 'unit': unit, 'window': window, 'ends_on': ends_on.isoformat(),
            'freshness_days': 1, 'baseline': baseline, 'baseline_kind': baseline_kind, 'source': source,
            'simulated': True}


def _entity(e):
    return {'type': 'experiment', 'id': e['id'], 'label': e['hypothesis']}


def _finding(rule_id, entity, severity, evidence, sentence, end, brain_refs, money=None, money_reason=None,
             confidence=0.9, status='open', unavailable=None):
    f = {'id': f'{SCREEN}.{rule_id}.{entity["id"]}', 'screen': SCREEN, 'rule_id': rule_id, 'severity': severity,
         'entity': entity, 'evidence': evidence, 'sentence': sentence, 'capability': dict(CAPABILITY[rule_id]),
         'money_at_stake': money, 'confidence': confidence, 'brain_refs': sorted(set(brain_refs)),
         'first_seen': end.isoformat(), 'last_seen': end.isoformat(), 'status': status, 'unavailable': unavailable}
    if money is None:
        f['money_reason'] = money_reason or 'no baseline'
    return f


def short(e):
    """The idea in a few words, for sentences."""
    return f'{e["id"]} ({e["variant"]["treatment"]})'


# ---------------------------------------------------------------- rules

def rule_no_metric(rd, e):
    if e['status'] not in ('running', 'done') or not e.get('start'):
        return []
    met = e.get('metric') or {}
    reg = d(met.get('registered_on'))
    start = d(e['start'])
    if met.get('name') and reg and reg <= start:
        return []
    late = met.get('name') and reg and reg > start
    s = (f'{short(e)} started {start.day} {start:%b} with no success metric agreed before launch.' if not late else
         f'{short(e)} started {start.day} {start:%b}; its metric was set {(reg - start).days} days later.')
    ev = [_ev('metric_registered', 1 if late else 0, 'count', rd.ends_on, baseline=1, baseline_kind='threshold')]
    return [_finding('EXP-R01', _entity(e), 'medium', ev, s, rd.ends_on, e.get('brain_refs', []),
                     money_reason='no metric, no baseline')]


def rule_early_read(rd, e):
    res, met = e.get('result') or {}, e.get('metric') or {}
    if not res.get('read_on') or not e.get('start') or not met.get('min_days'):
        return []
    ran = (d(res['read_on']) - d(e['start'])).days
    if ran >= met['min_days']:
        return []
    s = (f'{short(e)} was read after {ran} days. Its minimum was {met["min_days"]} days, so the '
         f'{abs(res.get("lift") or 0) * 100:.0f} percent read is not settled.')
    ev = [_ev('days_before_read', ran, 'days', rd.ends_on, baseline=met['min_days'], baseline_kind='threshold')]
    return [_finding('EXP-R02', _entity(e), 'medium', ev, s, rd.ends_on, e.get('brain_refs', []),
                     money_reason='early read: no settled effect to price')]


def rule_not_rolled(rd, e, net_28d, orders_28d):
    dec, res = e.get('decision') or {}, e.get('result') or {}
    if e['status'] != 'done' or dec.get('choice') != 'roll_out' or dec.get('rolled_out_on'):
        return []
    waited = (rd.ends_on - d(dec['on'])).days
    if waited <= ROLLOUT_GRACE:
        return []
    met = e.get('metric') or {}
    out = outcome(rd, e)
    ev = [_ev('days_since_roll_out_decision', waited, 'days', rd.ends_on, baseline=ROLLOUT_GRACE,
              baseline_kind='threshold')]
    money, reason, conf = None, None, 0.9
    lift = res.get('lift')
    if met.get('name') == 'returns_by_reason' and not out['unavailable'] and lift is not None and lift < 0:
        inp = out['inputs']
        avg_refund = round(inp['amount'] / inp['returns'], 2) if inp['returns'] else None
        ev.append(_ev('returns_per_order', out['value'], 'ratio', rd.ends_on, window=f'{WINDOW}d',
                      source='returns_by_reason'))
        if avg_refund is None or orders_28d is None:
            reason = 'no refunds for this reason in the window'
        else:
            # Rates and the average refund hold at any data scale; the order count is the aov metric's own.
            avoidable = out['value'] * -lift * orders_28d
            money = {'usd': round(avoidable * avg_refund, 2),
                     'formula': 'rate_now x -lift x orders_28d x avg_refund',
                     'inputs': {'rate_now': out['value'], 'lift': lift, 'orders_28d': orders_28d,
                                'avg_refund': avg_refund},
                     'window': f'{WINDOW}d',
                     'note': 'refunds only; lost repeat orders are not counted, so this is a floor', 'floor': True}
            conf = 0.5  # one 28-day window of returns
    elif out['unavailable']:
        reason = f'outcome unavailable: {out["reason"]}'
    else:
        reason = 'no money formula for this metric yet'
    stake = money['usd'] if money else None
    sev = ('critical' if stake and net_28d and stake > 0.05 * net_28d else
           'high' if stake and net_28d and stake > 0.01 * net_28d else 'medium')
    s = (f'{short(e)} won and was approved for roll out on {d(dec["on"]).day} {d(dec["on"]):%b}. '
         f'It is still not live {waited} days later.')
    return [_finding('EXP-R03', _entity(e), sev, ev, s, rd.ends_on, e.get('brain_refs', []), money, reason, conf)]


def rule_learning(rd, e):
    if not e.get('result') or e['status'] not in ('done', 'running'):
        return []
    ref = e.get('learnings_ref')
    rec = rd.record(ref)
    if rec and rec.get('section') == 'learnings':
        return []
    read_on = d(e['result']['read_on'])
    s = (f'{short(e)} was read on {read_on.day} {read_on:%b} and nothing from it is in the brand brain. '
         f'The next ranking will not know it was tried.')
    ev = [_ev('learnings_records', 0, 'count', rd.ends_on, baseline=1, baseline_kind='threshold',
              source='brain.learnings')]
    return [_finding('EXP-R04', _entity(e), 'medium', ev, s, rd.ends_on, e.get('brain_refs', []),
                     money_reason='memory gap: no money formula')]


def rule_stale(rd, e):
    park = e.get('park') or {}
    if e['status'] == 'parked' and park.get('expires') and d(park['expires']) < rd.ends_on:
        n = (rd.ends_on - d(park['expires'])).days
        s = f'{short(e)} was parked because "{park["reason"]}". That reason expired {n} days ago.'
        ev = [_ev('days_past_park_expiry', n, 'days', rd.ends_on, baseline=0, baseline_kind='threshold')]
    elif e['status'] == 'proposed' and not e.get('start'):
        reg = d((e.get('metric') or {}).get('registered_on'))
        if not reg or (rd.ends_on - reg).days <= STALE_DAYS:
            return []
        n = (rd.ends_on - reg).days
        s = f'{short(e)} was proposed {n} days ago and never started.'
        ev = [_ev('days_since_proposed', n, 'days', rd.ends_on, baseline=STALE_DAYS, baseline_kind='threshold')]
    else:
        return []
    return [_finding('EXP-R05', _entity(e), 'low', ev, s, rd.ends_on, e.get('brain_refs', []),
                     money_reason='parked idea: no money formula')]


def rule_overdue(rd, e):
    if e['status'] != 'running' or e.get('result') or not e.get('read_point'):
        return []
    n = (rd.ends_on - d(e['read_point'])).days
    if n <= OVERDUE_GRACE:
        return []
    s = f'{short(e)} passed its read point {n} days ago with no result recorded yet.'
    ev = [_ev('days_past_read_point', n, 'days', rd.ends_on, baseline=OVERDUE_GRACE, baseline_kind='threshold')]
    return [_finding('EXP-R06', _entity(e), 'high', ev, s, rd.ends_on, e.get('brain_refs', []),
                     money_reason='no result yet, so no effect to price')]


def rule_small(rd, e):
    met = e.get('metric') or {}
    if e['status'] != 'running' or not met.get('name') or not e.get('start') or not e.get('read_point'):
        return []
    span = (d(e['read_point']) - d(e['start'])).days
    need = max(met.get('min_days') or 0, MIN_DAYS.get(met['name'], 0))
    if span >= need:
        return []
    s = f'{short(e)} reads after {span} days. {met["name"]} needs {need} days to show a real signal.'
    ev = [_ev('read_span_days', span, 'days', rd.ends_on, baseline=need, baseline_kind='threshold')]
    return [_finding('EXP-R07', _entity(e), 'medium', ev, s, rd.ends_on, e.get('brain_refs', []),
                     money_reason='design gap: no money formula')]


def rule_overlap(rd, entries):
    run = sorted([e for e in entries if e['status'] == 'running' and e.get('start') and e.get('read_point')],
                 key=lambda e: (e['start'], e['id']))
    out = []
    for i, a in enumerate(run):
        for b in run[i + 1:]:
            shared = sorted(set(a.get('audience') or []) & set(b.get('audience') or []))
            if not shared or d(b['start']) > d(a['read_point']) or d(a['start']) > d(b['read_point']):
                continue
            both = (min(d(a['read_point']), d(b['read_point'])) - max(d(a['start']), d(b['start']))).days
            s = (f'{short(b)} and {a["id"]} both run on {shared[0].replace("_", " ")} for {both} days. '
                 f'Neither read can be pinned on one change.')
            ent = dict(_entity(b), id=f'{b["id"]}~{a["id"]}')
            ev = [_ev('shared_days', both, 'days', rd.ends_on, baseline=0, baseline_kind='threshold')]
            out.append(_finding('EXP-R08', ent, 'medium', ev, s, rd.ends_on,
                                a.get('brain_refs', []) + b.get('brain_refs', []),
                                money_reason='contamination: no money formula'))
    return out


def rule_unreadable(rd, e):
    met = e.get('metric') or {}
    if not met.get('name') or not e.get('read_point') or d(e['read_point']) > rd.ends_on:
        return []
    out = outcome(rd, e)
    if not out['unavailable']:
        return []
    s = f'{short(e)} reached its read point, but its read is unreadable: {met["name"]} is missing, not zero.'
    ent = {'type': 'metric', 'id': f'{e["id"]}.{met["name"]}', 'label': met['name']}
    return [_finding('EXP-R09', ent, 'medium', [], s, rd.ends_on, e.get('brain_refs', []),
                     money_reason='metric unavailable', status='unavailable',
                     unavailable={'inputs': [met['name']], 'connector': out.get('fix'),
                                  'fix': f'{out["reason"]}; {out.get("fix")}'})]


def rule_retro(rd, e):
    if e['status'] != 'done' or e.get('retro'):
        return []
    closed = d(e.get('end') or (e.get('result') or {}).get('read_on'))
    n = (rd.ends_on - closed).days if closed else None
    s = f'{short(e)} closed {n} days ago with no retro filed yet.'
    ev = [_ev('days_since_close', n, 'days', rd.ends_on)]
    return [_finding('EXP-R10', _entity(e), 'low', ev, s, rd.ends_on, e.get('brain_refs', []),
                     money_reason='memory gap: no money formula')]


def run(brand, window=None):
    """Findings for one brand, sorted by severity, then money at stake, then id."""
    ends_on = d(window['ends_on']) if window and window.get('ends_on') else last_full_day(brand)
    rd = Reader(brand, ends_on)
    entries = rd.entries()
    aov = rd.m('aov')
    net_28d = None if aov.get('unavailable') else aov['inputs']['net_revenue']
    orders_28d = None if aov.get('unavailable') else aov['inputs']['orders']
    out = []
    for e in entries:
        out += rule_no_metric(rd, e) + rule_early_read(rd, e) + rule_not_rolled(rd, e, net_28d, orders_28d)
        out += rule_learning(rd, e) + rule_stale(rd, e) + rule_overdue(rd, e) + rule_small(rd, e)
        out += rule_unreadable(rd, e) + rule_retro(rd, e)
    out += rule_overlap(rd, entries)
    out.sort(key=lambda f: (SEVERITY_ORDER[f['severity']], -((f.get('money_at_stake') or {}).get('usd') or -1), f['id']))
    return out
