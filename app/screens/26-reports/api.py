"""API for 26-reports, under /api/26-reports/.

  GET  summary?period=week|month   the report: what changed (this period against the one before),
                                   3 tiles, 2 insights (rules with their sentences), net revenue
                                   by period for the chart, the top 10 findings across screens by
                                   money at stake with their decision status, what shipped (the
                                   decisions log and brain decisions), what the brain learned,
                                   open questions, the brain's T0 card, and this screen's audit
  GET  findings?period=week|month  audit.run in the audit contract shape, plus RULES
  GET  decisions                   this brand's decisions log
  POST decisions                   {capability, choice, reason, autonomy, card} appended to
                                   app/data/brands/<brand>/decisions.json

week is the 7 days to the last full day; month is the last closed calendar month. Numbers
come from app/metrics.py through report.py. Missing numbers stay null with a reason, never 0.
"""
import importlib.util
import json
import re
import sys
import threading
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parents[1]
SCREEN = '26-reports'
BRAND = 'bombas'
PERIODS = ('week', 'month')
BAND_WINDOWS = 6             # the normal band is the min to max of the 6 periods before the last 2
CHOICES = ('agent', 'person', 'not_now')
AUTONOMY = ('agent_does', 'founder_gate', 'human_assist')
MAX_DECISIONS = 20_000
_lock = threading.Lock()


def _load(name, path):
    mod = sys.modules.get(name)
    if mod is None or getattr(mod, '__file__', None) != str(path):
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod
        spec.loader.exec_module(mod)
    return mod


def audit():
    return _load('reports_audit', HERE / 'audit.py')


def report():
    return audit().report()


# ---------------------------------------------------------------- wording

def pct(x, signed=True):
    return f"{'+' if signed and x > 0 else ''}{x * 100:.1f} percent"


def show(x, unit):
    if x is None:
        return 'unavailable'
    return audit().num(x, unit)


# ---------------------------------------------------------------- insights

def moved_most(lines, p, brand):
    """Insight 1: the headline field with the largest absolute percent change, and what drove it."""
    rule = ('largest absolute percent change among net revenue, orders, average order, paid spend and MER, '
            f"this {p['noun']} against the one before; the cause is the driver that moved most")
    by = {l['key']: l for l in lines}
    live = [by[k] for k in report().HEADLINE if by[k]['delta'] is not None]
    if not live:
        return {'name': 'one number that moved most', 'rule': rule, 'severity': 'info', 'sentence': None,
                'quiet': f"No headline number has both this {p['noun']} and the one before."}
    top = max(live, key=lambda l: (abs(l['delta']), l['key']))
    cause = None
    drivers = [by[k] for k in report().DRIVERS.get(top['key'], ()) if by[k]['delta'] is not None]
    if drivers:
        d = max(drivers, key=lambda l: abs(l['delta']))
        cause = f"{d['label'].lower()} ({pct(d['delta'])})"
    elif top['key'] == 'spend':
        R = report()
        cur = R.contract(brand, p['end'], p['days'])['_by_channel'] or {}
        pri = R.contract(brand, p['prior_end'], p['prior_days'])['_by_channel'] or {}
        moves = {c: cur[c] - pri[c] for c in cur if c in pri}
        if moves:
            c = max(sorted(moves), key=lambda k: abs(moves[k]))
            cause = f"{c.capitalize()} ({'+' if moves[c] > 0 else '-'}{audit().usd(abs(moves[c]))})"
    tail = f", mostly from {cause}." if cause else f", from {show(top['prior'], top['unit'])} to {show(top['value'], top['unit'])}."
    return {'name': 'one number that moved most', 'rule': rule, 'severity': 'medium',
            'sentence': f"{top['label']} moved {pct(top['delta'])} this {p['noun']}{tail}",
            'capability': 'LOOP-C01', 'autonomy': 'agent_does', 'card': f"{SCREEN}.moved_most.{p['kind']}.{p['end']}",
            'evidence': f"{top['label']}: {show(top['value'], top['unit'])} against {show(top['prior'], top['unit'])} ({top['source']})."}


def out_of_band(p, brand):
    """Insight 2: a headline field outside its normal band for the last 2 periods running."""
    R = report()
    n = BAND_WINDOWS + 2
    rule = (f"a headline number sits outside its normal band (min to max of the {BAND_WINDOWS} {p['noun']}s before) "
            f"for 2 {p['noun']}s running")
    labels = {k: l for k, l, _, _ in R.LINES}
    units = {k: u for k, _, u, _ in R.LINES}
    hits = []
    for key in R.HEADLINE:
        vals = R.series(brand, key, p, n)
        base = [v for v in vals[2:] if v is not None]
        if vals[0] is None or vals[1] is None or len(base) < BAND_WINDOWS:
            continue
        lo, hi = min(base), max(base)
        if all(v < lo or v > hi for v in vals[:2]):
            mid = (lo + hi) / 2
            hits.append((abs(vals[0] - mid) / mid if mid else 0, key, vals, lo, hi))
    if not hits:
        return {'name': 'metric out of band 2+ periods', 'rule': rule, 'severity': 'info', 'sentence': None,
                'quiet': f"Every headline number sat inside its normal range in at least one of the last 2 {p['noun']}s."}
    _, key, vals, lo, hi = max(hits, key=lambda h: (h[0], h[1]))
    u = units[key]
    return {'name': 'metric out of band 2+ periods', 'rule': rule, 'severity': 'high',
            'sentence': (f"{labels[key]} has been outside its normal range for 2 {p['noun']}s running: "
                         f"{show(vals[1], u)}, then {show(vals[0], u)}, against {show(lo, u)} to {show(hi, u)}."),
            'capability': 'LOOP-C01', 'autonomy': 'agent_does', 'card': f"{SCREEN}.out_of_band.{key}.{p['end']}",
            'evidence': f"{len(hits)} headline number{'s' if len(hits) != 1 else ''} out of band. Values are from app/metrics.py."}


# ---------------------------------------------------------------- tiles

def tile(line, name, plain, unit, p):
    out = {'name': name, 'plain': plain, 'unit': unit, 'value': line['value'], 'window': p['label'],
           'higher_is_better': True, 'metric': line['metric']}
    if line['unavailable']:
        out.update(unavailable_reason=line['reason'], fix=line['fix'])
    elif line['delta'] is not None:
        out['delta'] = line['delta']
    return out


def tiles(lines, top, p):
    by = {l['key']: l for l in lines}
    money = [t['usd'] for t in top if t['usd'] is not None]
    stake = {'name': 'Top 10 money at stake', 'unit': '$', 'window': p['label'],
             'plain': 'Money at stake across the 10 biggest findings from every screen',
             'value': round(sum(money), 2) if money else None, 'higher_is_better': False}
    if not money:
        stake['unavailable_reason'] = 'no finding in the top 10 has a money figure'
    return [tile(by['net_revenue'], 'Net revenue', 'Line subtotal minus discounts on paid orders', '$', p),
            tile(by['mer'], 'MER', 'Net revenue per dollar of Meta and Google spend', 'x', p),
            stake]


# ---------------------------------------------------------------- summary

def summary(req):
    kind = req.arg('period') or 'week'
    if kind not in PERIODS:
        raise ValueError('period must be week or month')
    A, R = audit(), report()
    p = R.period(BRAND, kind)
    e = A.evaluate(BRAND, p)
    data = R.brand_data(BRAND)
    return {
        'brand': data.brand, 'simulated': True, 'period': p, 'periods': list(PERIODS),
        't0_card': R.t0_card(BRAND, p),
        'tiles': tiles(e['lines'], e['top10'], p),
        'insights': [moved_most(e['lines'], p, BRAND), out_of_band(p, BRAND)],
        'what_changed': e['lines'], 'channel_mix': R.channel_mix(BRAND, p),
        'chart': R.trend_chart(BRAND, p),
        'top10': e['top10'], 'shipped': e['shipped'], 'brain': R.brain_changes(BRAND, p),
        'open_questions': R.open_questions(BRAND, p, e['screen_findings']),
        'screens': e['screens'], 'findings': e['findings'], 'rules': A.RULES,
        'decisions': read_decisions(),
    }


# ---------------------------------------------------------------- decisions

def decisions_path():
    return APP / 'data' / 'brands' / BRAND / 'decisions.json'


def read_decisions():
    return report().decisions_log(BRAND)


def validate(body):
    if not isinstance(body, dict):
        raise ValueError('body must be an object')
    capability = str(body.get('capability') or '').strip()
    choice = str(body.get('choice') or '')
    if not re.fullmatch(r'[A-Za-z0-9_.:-]{1,80}', capability):
        raise ValueError('capability must be a capability id')
    if choice not in CHOICES:
        raise ValueError('choice must be one of ' + ', '.join(CHOICES))
    row = {'screen': SCREEN, 'brand': BRAND, 'capability': capability, 'choice': choice,
           'reason': str(body.get('reason') or '').strip()[:300],
           'time': datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')}
    if body.get('autonomy') in AUTONOMY:
        row['autonomy'] = body['autonomy']
    card = str(body.get('card') or '')
    if re.fullmatch(r'[A-Za-z0-9_.:-]{1,160}', card):
        row['card'] = card
    return row


def append_decision(body):
    row = validate(body)
    path = decisions_path()
    with _lock:
        rows = read_decisions()
        if len(rows) >= MAX_DECISIONS:
            raise ValueError('decisions log is full')
        rows.append(row)
        tmp = path.with_suffix('.json.tmp')
        tmp.write_text(json.dumps(rows, indent=1), encoding='utf-8')
        tmp.replace(path)
    return row


# ---------------------------------------------------------------- routes

def handle(req):
    route = req.path[0] if req.path else ''
    try:
        if route == 'summary' and req.method == 'GET':
            return summary(req)
        if route == 'findings' and req.method == 'GET':
            kind = req.arg('period') or 'week'
            if kind not in PERIODS:
                raise ValueError('period must be week or month')
            p = report().period(BRAND, kind)
            return {'findings': audit().evaluate(BRAND, p)['findings'], 'rules': audit().RULES,
                    'period': p, 'simulated': True}
        if route == 'decisions':
            if req.method == 'POST':
                return 201, {'ok': True, 'decision': append_decision(req.body)}
            return {'decisions': read_decisions()}
    except ValueError as exc:
        return 400, {'error': str(exc)}
    return 404, {'error': 'not found', 'routes': ['summary', 'findings', 'decisions']}
