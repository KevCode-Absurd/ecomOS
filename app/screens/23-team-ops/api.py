"""Team and ops API: /api/23-team-ops/...

  GET overview?brand=bombas   tiles, insights, chart (tickets and orders by month against the median month),
                              workload windows, creative cadence, team signals, cost lines, findings, rules
  GET findings?brand=bombas   the audit findings only (audit.py, contract shape)

Ticket and order counts are read from data.sqlite by audit.py (both from the same file, so ratios hold at any data
scale); net revenue for the software share comes from app/metrics.py; team, operations and decisions come from the
brain; cost lines from finance_inputs. Insights are rules in `insights()`, each with the sentence it produces and
the capability it maps to. Missing is unavailable, never 0. Default brand is bombas (simulated). Read-only.
"""
import importlib.util
import re
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _audit():
    spec = importlib.util.spec_from_file_location('team_ops_audit', HERE / 'audit.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


audit = _audit()
DEFAULT_BRAND = 'bombas'
CHART_MONTHS = 24
DAYS_PER_MONTH = 30.4375


def _tile(name, plain, value, unit, window=None, freshness=None, sources=None, **extra):
    out = {'name': name, 'plain': plain, 'unit': unit, 'value': value, 'window': window, 'freshness': freshness,
           'sources': sources or [], 'unavailable_reason': extra.pop('reason', None), 'fix': extra.pop('fix', None)}
    out.update(extra)
    return out


# ---------------------------------------------------------------- tiles

def tiles(rd, rows, ws, decisions):
    fresh = rd.ends_on.isoformat()
    ss = audit.seasons(rows) if rows else []
    if not ss or ss[0]['ratio'] is None:
        t1 = _tile('Peak-month load', 'Tickets in the busiest month over the median month, last 12 full months.',
                   None, 'x', reason=audit.NO_TICKETS, fix=audit.TICKET_CONNECTOR)
    else:
        s = ss[0]
        t1 = _tile('Peak-month load', f'Tickets in {audit._month_label(s["peak_month"])} over the median month, '
                   f'{s["from"]} to {s["to"]}. The line is {audit.PEAK_RATIO} times.'
                   + (f' The year before: {ss[1]["ratio"]:.1f} times.' if len(ss) > 1 and ss[1]['ratio'] else ''),
                   s['ratio'], 'x', window='12 months', freshness=fresh, sources=[{'table': 'tickets'}],
                   delta=round(s['ratio'] / ss[1]['ratio'] - 1, 4) if len(ss) > 1 and ss[1]['ratio'] else None,
                   higher_is_better=False, tone='bad' if s['ratio'] > audit.PEAK_RATIO else None)
    w = ws[0] if ws else None
    if not w or not w['paid_orders']:
        t2 = _tile('Tickets per 100 orders', 'Support tickets opened per 100 paid orders placed, 28 days.', None, 'n',
                   reason=audit.NO_TICKETS, fix=audit.TICKET_CONNECTOR)
    else:
        now = round(w['tickets'] / w['paid_orders'] * 100, 3)
        prev = [x['tickets'] / x['paid_orders'] * 100 for x in ws[1:] if x and x['paid_orders']]
        med = statistics.median(prev) if len(prev) == audit.TRAILING else None
        t2 = _tile('Tickets per 100 orders', 'Support tickets opened per 100 paid orders placed, 28 days. '
                   f'Median time to resolve: {w["resolve_median"] / 60:.1f} hours.' if w['resolve_median'] is not None
                   else 'Support tickets opened per 100 paid orders placed, 28 days.',
                   now, 'n', window='28d', freshness=fresh, sources=[{'table': 'tickets'}, {'table': 'orders'}],
                   delta=round(now / med - 1, 4) if med else None, higher_is_better=False)
    sops = audit.sop_documents(rd)
    if not sops:
        t3 = _tile('SOP coverage', 'Core roles with a written SOP reviewed in the last 6 months.', None, '%',
                   reason='no SOPs are on file in the brain', fix='upload role SOPs to the brain documents')
    else:
        cur = [d for d in sops if (d.get('last_reviewed') or d.get('date'))]
        t3 = _tile('SOP coverage', f'{len(sops)} SOPs on file. Coverage needs the core role list, which is not in the '
                   'brain yet.', None, '%', reason='the core role list is not in the brain',
                   fix='list core roles in the brain team section', sops=len(sops), dated=len(cur))
    if not decisions:
        t4 = _tile('Decision log complete', 'Founder decisions logged with an owner, a metric and a review date.',
                   None, '%', reason='no founder decisions are logged in the brain', fix='brain decisions section')
    else:
        done = sum(1 for d in decisions if d['complete'])
        t4 = _tile('Decision log complete', f'{done} of {len(decisions)} founder decisions in the brain carry an owner, '
                   'a metric and a review date. The line is 100 percent.', round(done / len(decisions), 4), '%',
                   window='all logged', freshness=fresh, sources=[{'table': 'brain.decisions'}],
                   tone='bad' if done < len(decisions) else None)
    return {'peak_load': t1, 'tickets_per_order': t2, 'sop_coverage': t3, 'decision_log': t4}


# ---------------------------------------------------------------- insights

def insights(rd, rows, decisions):
    """The rules behind the insight cards. Each returns the sentence it produces and its capability."""
    out = []
    rule = (f'peak_month_load: tickets in the busiest full month over the median month of the same 12 months; fires '
            f'over {audit.PEAK_RATIO} times when that calendar month starts within {audit.PEAK_LOOKAHEAD} days '
            f'(audit TEAM-R09)')
    ss = audit.seasons(rows) if rows else []
    if not ss or ss[0]['ratio'] is None:
        out.append({'id': 'peak_load', 'severity': 'high', 'capability': 'MONEY-C38', 'autonomy': 'human_assist',
                    'sentence': f'Peak-month load is unavailable: {audit.NO_TICKETS}.', 'rule': rule})
    else:
        s = ss[0]
        name = audit.MONTH_NAMES[int(s['peak_month'][5:7]) - 1]
        days = (audit.next_start(rd.ends_on, int(s['peak_month'][5:7])) - rd.ends_on).days
        fires = s['ratio'] > audit.PEAK_RATIO and days <= audit.PEAK_LOOKAHEAD
        roles, care = audit.open_roles(rd)
        text = (f'{name} brought {s["ratio"]:.1f} times the tickets of a normal month, and '
                f'{s["peak_per_100"]:.1f} tickets per 100 orders against {s["median_per_100"]:.1f}. '
                f'It starts again in {days} days. {len(care)} of {len(roles)} open roles are in customer care.')
        out.append({'id': 'peak_load', 'severity': 'high' if fires else 'info',
                    'capability': 'MONEY-C38' if fires else None, 'autonomy': 'human_assist', 'sentence': text,
                    'rule': rule,
                    'stub': (f'Draft a {name} care plan: tickets expected by week, hours needed, temp or outsourced cover '
                             f'and routing rules. A person reviews it before anything is booked.') if fires else None})
    rule = ('decision_log_completeness: founder decisions in the brain with an owner, a metric and a review date over '
            'all logged; fires under 100 percent (room spec target, audit TEAM-R11)')
    if not decisions:
        out.append({'id': 'decision_log', 'severity': 'medium', 'capability': 'LOOP-C10', 'autonomy': 'agent_does',
                    'sentence': 'The decision log is unavailable: no founder decisions are in the brain yet.', 'rule': rule})
    else:
        miss = [d for d in decisions if not d['complete']]
        text = (f'{len(miss)} of {len(decisions)} founder decisions have no metric or review date, so none can be '
                f'checked later.' if miss else f'All {len(decisions)} founder decisions carry an owner, a metric and a review date.')
        out.append({'id': 'decision_log', 'severity': 'medium' if miss else 'info',
                    'capability': 'LOOP-C10' if miss else None, 'autonomy': 'agent_does', 'sentence': text, 'rule': rule,
                    'stub': ('Add a metric and a review date to each open decision from its own text, then list them '
                             'for the founder to confirm.') if miss else None})
    return out


# ---------------------------------------------------------------- chart and tables

def chart(rows):
    """Tickets and paid orders per month as a multiple of each one's median month, last 24 full months."""
    if not rows:
        return {'unavailable': True, 'reason': audit.NO_TICKETS, 'fix': audit.TICKET_CONNECTOR}
    rows = rows[-CHART_MONTHS:]
    tm = statistics.median(r['tickets'] for r in rows)
    om = statistics.median(r['paid_orders'] for r in rows if r['paid_orders'])
    return {'labels': [r['month'] for r in rows], 'benchmark': audit.PEAK_RATIO, 'window': f'{len(rows)} months',
            'series': [{'name': 'tickets', 'values': [round(r['tickets'] / tm, 3) for r in rows]},
                       {'name': 'paid orders', 'values': [round(r['paid_orders'] / om, 3) if r['paid_orders'] else None
                                                          for r in rows]}],
            'basis': 'each month over the median month of the same span; full months only'}


def workload(ws):
    if not ws or ws[0] is None:
        return {'unavailable': True, 'reason': audit.NO_TICKETS, 'fix': audit.TICKET_CONNECTOR}
    rows = [{'window': f'{w["start"]} to {w["end"]}', 'tickets': w['tickets'], 'paid_orders': w['paid_orders'],
             'per_100_orders': round(w['tickets'] / w['paid_orders'] * 100, 3) if w['paid_orders'] else None,
             'resolve_hours': round(w['resolve_median'] / 60, 2) if w['resolve_median'] is not None else None,
             'reply_min': w['reply_median']} for w in ws if w]
    return {'unavailable': False, 'rows': rows,
            'note': 'Counted in the simulated table, so counts are a sample and ratios are the part to read.'}


def team_signals(rd):
    roles, care = audit.open_roles(rd)
    pick = lambda sec, fields: [{'ref': r['id'], 'field': r.get('field'), 'text': r.get('text'),
                                 'source': (r.get('source') or {}).get('ref')}
                                for r in rd.records(sec) if r.get('field') in fields]
    return {'open_roles': len(roles), 'care_roles': len(care),
            'team': pick('team', ('hiring_role', 'team_shape', 'outside_agency')),
            'operations': pick('operations', ('fulfillment_fact',))}


def costs(rd):
    """Monthly cost lines from finance_inputs and software as a share of net revenue, 28 days."""
    tools = audit.tool_costs(rd)
    if tools is None:
        return {'unavailable': True, 'reason': 'finance_inputs has no app fees', 'fix': 'finance_inputs'}
    monthly = sum(t['usd_per_month'] for t in tools)
    aov = rd.m('aov')
    share = None
    if not aov.get('unavailable') and aov['inputs'].get('net_revenue'):
        share = round(monthly * audit.WINDOW / DAYS_PER_MONTH / aov['inputs']['net_revenue'], 6)
    lines = {k: sum(r['value'] for r in audit.cost_lines(rd, k)) or None for k in ('headcount_cost', 'agency_fees')}
    return {'unavailable': False, 'tools': tools, 'tools_per_month': monthly, 'share_of_net_revenue': share,
            'net_revenue_28d': aov.get('inputs', {}).get('net_revenue'), 'headcount_per_month': lines.get('headcount_cost'),
            'agency_per_month': lines.get('agency_fees'), 'stage_plan': None,
            'stage_plan_reason': 'no software budget for this revenue stage in the brain',
            'note': 'Cost lines are simulated assumptions in finance_inputs, not Bombas numbers.'}


def overview(data, brand):
    ends_on = audit.last_full_day(data, brand)
    rd = audit.Reader(data, brand, ends_on)
    b = rd.source.brand
    head = {'brand': b.get('brand'), 'name': b.get('name'), 'as_of': b.get('as_of'),
            'simulated': bool(b.get('simulated') or b.get('fictional')), 'market': b.get('market')}
    rows = audit.monthly(rd)
    ws = audit.ticket_windows(rd)
    decisions = audit.decision_records(rd)
    return {'brand': head, 'window': {'ends_on': ends_on.isoformat(), 'days': audit.WINDOW},
            'tiles': tiles(rd, rows, ws, decisions), 'insights': insights(rd, rows, decisions), 'chart': chart(rows),
            'workload': workload(ws), 'cadence': audit.cadence(rd), 'team': team_signals(rd), 'costs': costs(rd),
            'decisions': decisions, 'findings': audit.findings(rd), 'rules': audit.RULES}


def _brand(req):
    brand = req.arg('brand', DEFAULT_BRAND)
    if brand in ('', 'sample'):
        return None
    if not re.fullmatch(r'[a-z0-9-]{1,40}', brand):
        raise ValueError('brand must be a folder name like bombas')
    return brand


def handle(req):
    if req.method != 'GET':
        return 405, {'error': 'read only'}
    try:
        brand = _brand(req)
        data = None if brand else req.data
        if brand:
            audit.brand_data(brand)  # ValueError for an unknown brand
        if req.path == ['overview']:
            return overview(data, brand)
        if req.path == ['findings']:
            return {'findings': audit.run(brand, None, data=data), 'rules': audit.RULES}
    except ValueError as exc:
        return 400, {'error': str(exc)}
    return 404, {'error': 'not found', 'routes': ['overview', 'findings']}
