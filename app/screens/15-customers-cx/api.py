"""Customers and CX API: /api/15-customers-cx/...

  GET overview?brand=bombas   tiles, insights, chart (tickets per 100 orders by reason, monthly), reasons table,
                              channels, repeat by cohort, reviews, objection ladders, findings, rules
  GET findings?brand=bombas   the audit findings only (audit.py, contract shape)

Ticket, CSAT, reply and repeat numbers are counted in data.sqlite by audit.py (tickets and orders from the same
file, so rates hold at any data scale); order totals come from app/metrics.py; ladders and policies from the brain.
Insights are rules in `insights()`, each with the sentence it produces and the capability it maps to. Missing is
unavailable, never 0. Default brand is bombas (simulated). Read-only.
"""
import importlib.util
import re
import statistics
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _audit():
    spec = importlib.util.spec_from_file_location('customers_cx_audit', HERE / 'audit.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


audit = _audit()
DEFAULT_BRAND = 'bombas'
CHART_MONTHS = 12
CHART_REASONS = 5  # the rest are summed as "other"


def _tile(name, plain, value, unit, window=None, freshness=None, sources=None, **extra):
    out = {'name': name, 'plain': plain, 'unit': unit, 'value': value, 'window': window, 'freshness': freshness,
           'sources': sources or [], 'unavailable_reason': extra.pop('reason', None), 'fix': extra.pop('fix', None)}
    out.update(extra)
    return out


NO_TICKETS = 'the ticket table or data.sqlite is not connected'


def _median(vals):
    vals = [v for v in vals if v is not None]
    return statistics.median(vals) if len(vals) == audit.TRAILING else None


# ---------------------------------------------------------------- tiles

def tiles(rd, ws, cohorts):
    fresh = rd.ends_on.isoformat()
    src = [{'table': 'tickets'}, {'table': 'orders'}]
    w = ws[0] if ws else None
    if not w:
        t1 = _tile('Where is my order', 'Where-is-my-order tickets over paid orders, 28 days.', None, '%',
                   reason=NO_TICKETS, fix=audit.TICKET_CONNECTOR)
        t2 = _tile('Support CSAT', 'Share of rated tickets scored 4 or 5, 28 days.', None, '%', reason=NO_TICKETS,
                   fix=audit.TICKET_CONNECTOR)
        t3 = _tile('First reply', 'Median minutes to the first reply, 28 days.', None, 'min', reason=NO_TICKETS,
                   fix=audit.TICKET_CONNECTOR)
    else:
        now, med = audit.wismo(w), _median([audit.wismo(x) for x in ws[1:]])
        t1 = _tile('Where is my order', f'"Where is my order" tickets over paid orders placed, 28 days. The usual line '
                   f'is {audit.WISMO_TARGET * 100:.0f} percent.' + (f' Own median of the 4 windows before: '
                                                                    f'{med * 100:.2f} percent.' if med else ''),
                   now, '%', window='28d', freshness=fresh, sources=src,
                   delta=round(now / med - 1, 4) if now is not None and med else None, higher_is_better=False,
                   tone='bad' if now is not None and now > audit.WISMO_TARGET else None)
        c, cmed = audit.csat(w), _median([audit.csat(x) for x in ws[1:]])
        if c is None:
            t2 = _tile('Support CSAT', 'Share of rated tickets scored 4 or 5, 28 days.', None, '%',
                       reason='under 5 percent of tickets carry a rating', fix=audit.TICKET_CONNECTOR)
        else:
            t2 = _tile('Support CSAT', f'Share of rated tickets scored 4 or 5, 28 days. {w["rated"] / w["tickets"] * 100:.0f} '
                       f'percent of tickets were rated. The line is {audit.CSAT_TARGET * 100:.0f} percent.',
                       c, '%', window='28d', freshness=fresh, sources=[{'table': 'tickets'}],
                       delta=round(c / cmed - 1, 4) if cmed else None, higher_is_better=True,
                       tone='bad' if c < audit.CSAT_TARGET else None)
        r = w['reply_all']
        rmed = _median([x['reply_all'] for x in ws[1:] if x])
        chat = w['reply_median'].get('chat')
        email = w['reply_median'].get('email')
        t3 = _tile('First reply', 'Median minutes from a new ticket to the first reply, all channels, 28 days.'
                   + (f' Chat {chat:.0f} (line 60), email {email:.0f} (line 1,440).' if chat is not None and email is not None else ''),
                   r, 'min', window='28d', freshness=fresh, sources=[{'table': 'tickets'}],
                   delta=round(r / rmed - 1, 4) if r is not None and rmed else None, higher_is_better=False,
                   tone='bad' if chat is not None and chat > audit.FIRST_REPLY_TARGET['chat'] else None)
    if not cohorts:
        t4 = _tile('Repeat within 90 days', 'First-time buyers who order again within 90 days, newest full cohort.',
                   None, '%', reason='the order table is not connected', fix='shopify')
    else:
        last = cohorts[-1]
        med = statistics.median([c['rate'] for c in cohorts[-audit.TRAILING - 1:-1]]) if len(cohorts) > audit.TRAILING else None
        t4 = _tile('Repeat within 90 days', f'First-time buyers from {last["cohort"]} who ordered again within 90 days.'
                   + (f' The 4 cohorts before: {med * 100:.1f} percent.' if med else ''),
                   last['rate'], '%', window=f'cohort {last["cohort"]}', freshness=fresh, sources=[{'table': 'orders'}],
                   delta=round(last['rate'] / med - 1, 4) if med else None, higher_is_better=True)
    return {'wismo': t1, 'csat': t2, 'first_reply': t3, 'repeat': t4}


# ---------------------------------------------------------------- insights

def insights(rd, ws):
    """The rules behind the insight cards. Each returns the sentence it produces and its capability."""
    out = []
    rule = (f'ticket_volume_by_reason, 28 days against the 28 before: fires when one reason\'s share of tickets grows '
            f'more than {audit.DRIFT_PP * 100:.0f} points (room spec, ticket reason drift)')
    if not ws or ws[0] is None or ws[1] is None:
        out.append({'id': 'reason_drift', 'severity': 'medium', 'capability': 'LIFE-C27', 'autonomy': 'human_assist',
                    'sentence': f'Ticket reasons are unavailable: {NO_TICKETS}.', 'rule': rule})
    else:
        now, before = audit.shares(ws[0]), audit.shares(ws[1])
        moves = sorted(((now[k] - before.get(k, 0.0), k) for k in now), reverse=True)
        up, reason = moves[0]
        top = max(now, key=now.get)
        fires = up > audit.DRIFT_PP
        s = (f'"{audit._label(reason)}" tickets went from {before.get(reason, 0) * 100:.0f} percent to '
             f'{now[reason] * 100:.0f} percent of contacts.' if fires else
             f'"{audit._label(top)}" is {now[top] * 100:.0f} percent of {ws[0]["tickets"]:,} tickets in 28 days. '
             f'The biggest rise is "{reason}", up {up * 100:.1f} points, under the {audit.DRIFT_PP * 100:.0f} point line.')
        out.append({'id': 'reason_drift', 'severity': 'medium' if fires else 'info',
                    'capability': 'LIFE-C27' if fires else None, 'autonomy': 'human_assist', 'sentence': s, 'rule': rule,
                    'stub': (f'Draft reply templates and tagging rules for "{reason}" tickets and send them to the support '
                             f'lead. Nothing changes in the helpdesk until a person approves.') if fires else None})
    rule = (f'wismo_ticket_rate, 28 days: "where is my order" tickets over paid orders placed; fires over the '
            f'{audit.WISMO_TARGET * 100:.0f} percent line (room spec benchmark) or over 2 times the own median of the '
            f'4 windows before')
    if not ws or ws[0] is None:
        out.append({'id': 'wismo', 'severity': 'medium', 'capability': 'LIFE-C24', 'autonomy': 'founder_gate',
                    'sentence': f'The where-is-my-order rate is unavailable: {NO_TICKETS}.', 'rule': rule})
    else:
        now = audit.wismo(ws[0])
        med = _median([audit.wismo(x) for x in ws[1:]])
        fires = now > audit.WISMO_TARGET or (med is not None and now > 2 * med)
        n = ws[0]['reasons'].get(audit.WISMO_REASON, {}).get('tickets', 0)
        s = (f'"Where is my order" is {now * 100:.2f} percent of paid orders in 28 days ({n:,} tickets), '
             + ('over' if now > audit.WISMO_TARGET else 'under') + f' the {audit.WISMO_TARGET * 100:.0f} percent line.')
        if med is not None:
            s += f' Own median {med * 100:.2f} percent.'
        out.append({'id': 'wismo', 'severity': 'medium' if fires else 'info', 'capability': 'LIFE-C24' if fires else None,
                    'autonomy': 'founder_gate', 'sentence': s, 'rule': rule,
                    'stub': 'Draft a new order status and tracking message plan. Nothing is sent until you approve.'
                    if fires else None})
    return out


# ---------------------------------------------------------------- chart and tables

def chart(rd):
    """Tickets per 100 paid orders by reason, by month, 12 months, the top reasons stacked and the rest as other."""
    end = rd.ends_on
    first = date(end.year - 1 + (end.month == 12), end.month % 12 + 1, 1)
    s, e = first.isoformat(), end.isoformat()
    t = rd.sql(f"SELECT substr(created_at, 1, 7) AS month, reason, COUNT(*) AS n FROM tickets "
               f"WHERE substr(created_at, 1, 10) BETWEEN '{s}' AND '{e}' GROUP BY month, reason")
    o = rd.sql(f"SELECT substr(created_at, 1, 7) AS month, COUNT(*) AS n FROM orders WHERE status IN ({audit.PAID_SQL}) "
               f"AND substr(created_at, 1, 10) BETWEEN '{s}' AND '{e}' GROUP BY month")
    if t is None or o is None or not t:
        return {'unavailable': True, 'reason': NO_TICKETS, 'fix': audit.TICKET_CONNECTOR}
    orders = {r['month']: r['n'] for r in o}
    months = sorted(orders)[-CHART_MONTHS:]
    totals = {}
    for r in t:
        totals[r['reason']] = totals.get(r['reason'], 0) + r['n']
    top = [k for k, _ in sorted(totals.items(), key=lambda kv: (-kv[1], kv[0]))][:CHART_REASONS]
    cell = {(r['month'], r['reason']): r['n'] for r in t}

    def per100(month, reasons):
        n = orders.get(month)
        return round(sum(cell.get((month, x), 0) for x in reasons) / n * 100, 3) if n else None

    series = [{'name': k, 'values': [per100(m, [k]) for m in months]} for k in top]
    rest = [k for k in totals if k not in top]
    series.append({'name': 'other', 'values': [per100(m, rest) for m in months]})
    partial = [m for m in months if m == end.strftime('%Y-%m') and (end + timedelta(days=1)).month == end.month]
    return {'labels': months, 'series': series, 'partial': partial, 'window': f'{len(months)} months',
            'basis': 'tickets opened in the month over paid orders placed in the same month'}


def reasons(ws):
    if not ws or ws[0] is None:
        return {'unavailable': True, 'reason': NO_TICKETS, 'fix': audit.TICKET_CONNECTOR}
    w, before = ws[0], audit.shares(ws[1]) if ws[1] else {}
    rows = [{'reason': k, 'tickets': g['tickets'], 'share': round(g['tickets'] / w['tickets'], 4),
             'share_before': before.get(k), 'per_100_orders': round(g['tickets'] / w['paid_orders'] * 100, 3),
             'csat': round(g['good'] / g['rated'], 4) if g['rated'] >= 20 else None, 'rated': g['rated']}
            for k, g in w['reasons'].items()]
    rows.sort(key=lambda r: (-r['tickets'], r['reason']))
    chans = [{'channel': c, 'tickets': n, 'share': round(n / w['tickets'], 4), 'first_reply_min': w['reply_median'].get(c),
              'target_min': audit.FIRST_REPLY_TARGET.get(c)} for c, n in sorted(w['channels'].items(), key=lambda kv: -kv[1])]
    return {'unavailable': False, 'rows': rows, 'channels': chans, 'tickets': w['tickets'], 'paid_orders': w['paid_orders'],
            'window': {'start': w['start'], 'end': w['end']},
            'note': 'CSAT per reason shows when 20 or more tickets were rated.'}


def review_mix(rd):
    s = (rd.ends_on - timedelta(days=audit.WINDOW - 1)).isoformat()
    rows = rd.sql(f"SELECT review_source AS source, rating, COUNT(*) AS n FROM reviews "
                  f"WHERE date BETWEEN '{s}' AND '{rd.ends_on.isoformat()}' GROUP BY source, rating")
    if rows is None:
        return {'unavailable': True, 'reason': 'the reviews table is not connected', 'fix': 'reviews app export'}
    n = sum(r['n'] for r in rows)
    if not n:
        return {'unavailable': True, 'reason': 'no reviews in the window', 'fix': 'reviews app export'}
    by_star = {str(k): sum(r['n'] for r in rows if r['rating'] == k) for k in range(1, 6)}
    return {'unavailable': False, 'reviews': n, 'by_star': by_star, 'sources': sorted({r['source'] for r in rows}),
            'average': round(sum(r['rating'] * r['n'] for r in rows) / n, 2),
            'low_share': round((by_star['1'] + by_star['2']) / n, 4), 'window': '28d',
            'replied': None, 'replied_reason': 'the reviews export carries no reply date'}


def ladders(rd):
    out = []
    for r in rd._brain.records('objection_ladders') if rd._brain else []:
        v = r.get('value') or {}
        rungs = v.get('rungs') if isinstance(v, dict) else None
        if not rungs:
            continue  # the section also holds non-ladder records
        last = rungs[-1]
        c = sum((x.get('counts') or {}).get('one_star', 0) for x in rungs)
        out.append({'theme': v.get('theme'), 'ref': r['id'], 'rungs': len(rungs), 'complaints': c,
                    'top_doubt': last.get('doubt'), 'top_complaints': (last.get('counts') or {}).get('one_star'),
                    'has_proof': bool(last.get('proof')) and 'no public proof' not in str(last.get('proof')).lower(),
                    'sources': (last.get('counts') or {}).get('sources') or {}})
    out.sort(key=lambda x: -x['complaints'])
    return out


def overview(data, brand):
    ends_on = audit.last_full_day(data, brand)
    rd = audit.Reader(data, brand, ends_on)
    b = rd.source.brand
    head = {'brand': b.get('brand'), 'name': b.get('name'), 'as_of': b.get('as_of'),
            'simulated': bool(b.get('simulated') or b.get('fictional')), 'market': b.get('market')}
    ws = audit.ticket_windows(rd)
    cohorts = audit.repeat_cohorts(rd)
    guarantee = rd.record('policies.happiness_guarantee')
    return {'brand': head, 'window': {'ends_on': ends_on.isoformat(), 'days': audit.WINDOW},
            'tiles': tiles(rd, ws, cohorts), 'insights': insights(rd, ws), 'chart': chart(rd), 'reasons': reasons(ws),
            'repeat': {'unavailable': cohorts is None, 'cohorts': (cohorts or [])[-12:], 'days': audit.REPEAT_DAYS},
            'reviews': review_mix(rd), 'ladders': ladders(rd),
            'policy': {'ref': guarantee['id'], 'text': guarantee.get('text')} if guarantee else None,
            'findings': audit.findings(rd), 'rules': audit.RULES}


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
