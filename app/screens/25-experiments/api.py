"""Experiments and memory API: /api/25-experiments/...

  GET overview?brand=bombas   registry, tiles, insights, chart, outcomes, findings
  GET findings?brand=bombas   the audit findings only (audit.py, contract shape)

The registry is fixtures/registry.json until the shared `registry` table exists (shape in contracts/events.md).
Outcome numbers come from app/metrics.py through audit.outcome; a metric with no formula reads unavailable, never 0.
Insights are rules in `insights()`, each with the sentence it produces and its capability. Default brand is bombas
(simulated). Read-only.
"""
import importlib.util
import re
from datetime import timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _audit():
    spec = importlib.util.spec_from_file_location('experiments_audit', HERE / 'audit.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


audit = _audit()
DEFAULT_BRAND = 'bombas'
STATUS_ORDER = ('running', 'proposed', 'parked', 'done')
RESULT_WORD = {'up': 'up', 'down': 'down', 'flat': 'flat'}
WORDS = {'returns_by_reason': 'returns per order', 'add_to_cart_rate': 'add to cart rate', 'aov': 'AOV',
         'cpa': 'cost per order', 'marketplace_conversion': 'listing conversion'}


def _tile(name, plain, value, unit, window, freshness, reason=None):
    return {'name': name, 'plain': plain, 'unit': unit, 'value': value, 'window': window, 'freshness': freshness,
            'sources': [{'table': 'registry'}], 'unavailable_reason': reason, 'fix': None}


def week(end):
    """The current week, Monday to Sunday, holding the window end."""
    start = end - timedelta(days=end.weekday())
    return start, start + timedelta(days=6)


def rows(rd):
    out = []
    for e in rd.entries():
        start, rp = audit.d(e.get('start')), audit.d(e.get('read_point'))
        res, met = e.get('result') or {}, e.get('metric') or {}
        now = audit.outcome(rd, e)
        out.append({
            'id': e['id'], 'hypothesis': e['hypothesis'], 'status': e['status'], 'owner': e.get('owner'),
            'metric': met.get('name'), 'min_days': met.get('min_days'), 'variant': e['variant'],
            'audience': e.get('audience') or [], 'start': e.get('start'), 'read_point': e.get('read_point'),
            'days_run': (min(rd.ends_on, rp or rd.ends_on) - start).days if start else None,
            'days_to_read': (rp - rd.ends_on).days if rp else None,
            'result': res.get('direction'), 'lift': res.get('lift'), 'read_on': res.get('read_on'),
            'decision': (e.get('decision') or {}).get('choice'), 'learnings_ref': e.get('learnings_ref'),
            'park': e.get('park'), 'source': e.get('source'), 'brain_refs': e.get('brain_refs', []),
            'outcome_now': now.get('value'), 'outcome_unit': now.get('unit'), 'outcome_label': now.get('label'),
            'outcome_unavailable': now.get('reason') if now['unavailable'] else None,
        })
    return out


def tiles(rd, reg):
    end = rd.ends_on
    w0, w1 = week(end)
    fresh = end.isoformat()
    running = [r for r in reg if r['status'] == 'running']
    due = [r for r in running if r['read_point'] and w0 <= audit.d(r['read_point']) <= w1]
    stale = [r for r in reg if r['read_point'] and audit.d(r['read_point']) < end and not r['result']
             and r['status'] == 'running']
    return {
        'running': _tile('Running now', 'Registry entries with status running', len(running), 'n', 'as of now', fresh),
        'due': _tile('Reads due this week', f'Running entries whose read point falls {w0.day} to {w1.day} {w1:%b}',
                     len(due), 'n', 'this week', fresh),
        'stale': _tile('Past read point, no result', 'Target 0. Today is past the read point and no result is recorded',
                       len(stale), 'n', 'as of now', fresh),
    }


def insights(rd, reg):
    """Two rules from the room spec. Each returns one card; the sentence is filled in code."""
    end = rd.ends_on
    out = []
    # Rule 1, stale unread entry: running, past read point by more than the grace, no result.
    late = sorted([r for r in reg if r['status'] == 'running' and not r['result'] and r['read_point']
                   and (end - audit.d(r['read_point'])).days > audit.OVERDUE_GRACE],
                  key=lambda r: (r['read_point'], r['id']))
    rule1 = f'status = running and today - read_point > {audit.OVERDUE_GRACE} days and result is null'
    if late:
        r = late[0]
        n = (end - audit.d(r['read_point'])).days
        s = f'{r["id"]} ({r["variant"]["treatment"]}) passed its read point {n} days ago with no result recorded yet.'
        if len(late) > 1:
            s += f' {len(late) - 1} more are late.'
        out.append({'id': 'stale', 'severity': 'high', 'capability': 'REG-C02', 'autonomy': 'agent_does',
                    'sentence': s, 'rule': rule1,
                    'stub': f'Take the read for {r["id"]} now from the data layer, record it in the registry and '
                            f'show the result here. Nothing on the store changes; your choice is logged.'})
    else:
        out.append({'id': 'stale', 'severity': 'info', 'capability': None, 'autonomy': None, 'rule': rule1,
                    'sentence': 'Every running test past its read point has a result recorded.'})
    # Rule 2, read point reached: the latest entry with a result read at or after its read point.
    rule2 = 'read_on >= read_point and result is recorded; sentence names the direction and the lift'
    read = sorted([r for r in reg if r['result'] and r['read_point'] and r['read_on']
                   and audit.d(r['read_on']) >= audit.d(r['read_point'])], key=lambda r: (r['read_on'], r['id']))
    if read:
        r = read[-1]
        s = (f'{r["id"]} ({r["variant"]["treatment"]}) hit its read point; result is '
             f'{RESULT_WORD.get(r["result"], "unreadable")}: {r["lift"] * 100:+.0f} percent on {WORDS.get(r["metric"], r["metric"])}.')
        if r['decision'] == 'roll_out':
            s += ' It was approved for roll out.'
        out.append({'id': 'read', 'severity': 'high', 'capability': 'REG-C03', 'autonomy': 'agent_does',
                    'sentence': s, 'rule': rule2,
                    'stub': f'Show the brand memory for {r["id"]}: the result, the decision and what the brain holds '
                            f'about it. Nothing on the store changes; your choice is logged.'})
    else:
        out.append({'id': 'read', 'severity': 'info', 'capability': None, 'autonomy': None, 'rule': rule2,
                    'sentence': 'No test has reached its read point with a result yet.'})
    return out


def chart(reg):
    """Days run so far against the minimum days each test needs (LOOP-C08). Parked and proposed have no run."""
    rs = [r for r in reg if r['days_run'] is not None]
    return {'labels': [r['id'] for r in rs], 'days_run': [r['days_run'] for r in rs],
            'min_days': [r['min_days'] for r in rs],
            'basis': 'days from start to today, or to the read point once passed; minimum from the registered metric'}


def overview(brand):
    ends_on = audit.last_full_day(brand)
    rd = audit.Reader(brand, ends_on)
    b = audit.brand_data(brand).brand
    head = {'brand': b.get('brand'), 'name': b.get('name'), 'as_of': b.get('as_of'),
            'simulated': bool(b.get('simulated') or b.get('fictional')), 'market': b.get('market')}
    reg = rows(rd)
    by_status = {s: [r['id'] for r in reg if r['status'] == s] for s in STATUS_ORDER}
    return {'brand': head, 'window': {'ends_on': ends_on.isoformat(), 'days': audit.WINDOW},
            'registry_simulated': True, 'registry': reg, 'by_status': by_status, 'tiles': tiles(rd, reg),
            'insights': insights(rd, reg), 'chart': chart(reg),
            'findings': audit.run(brand, {'ends_on': ends_on.isoformat()}), 'rules': audit.RULES}


def _brand(req):
    brand = req.arg('brand', DEFAULT_BRAND) or DEFAULT_BRAND
    if not re.fullmatch(r'[a-z0-9-]{1,40}', brand):
        raise ValueError('brand must be a folder name like bombas')
    return brand


def handle(req):
    if req.method != 'GET':
        return 405, {'error': 'read only'}
    try:
        brand = _brand(req)
        audit.brand_data(brand)  # ValueError for an unknown brand
        if req.path == ['overview']:
            return overview(brand)
        if req.path == ['findings']:
            return {'findings': audit.run(brand), 'rules': audit.RULES}
    except ValueError as exc:
        return 400, {'error': str(exc)}
    return 404, {'error': 'not found', 'routes': ['overview', 'findings']}
