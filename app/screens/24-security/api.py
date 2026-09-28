"""Security API: /api/24-security/...

  GET overview?brand=bombas   tiles, insights, chart, chargebacks and disputes, payouts, scripts, controls,
                              coverage (what each rule can read), findings, rules
  GET findings?brand=bombas   the audit findings only (audit.py, contract shape)

Numbers come from app/metrics.py (chargebacks, disputes and payouts from data.sqlite); brand facts from the brain
(stack, policies), all through audit.Reader. Insights are rules in `insights()`, each with the sentence it produces
and the capability it maps to. Missing is unavailable, never 0. Default brand is bombas (simulated). Read-only.
"""
import importlib.util
import re
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _audit():
    spec = importlib.util.spec_from_file_location('security_audit', HERE / 'audit.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


audit = _audit()
DEFAULT_BRAND = 'bombas'
CHART_MONTHS = 12


def _tile(name, plain, value, unit, window=None, freshness=None, sources=None, **extra):
    out = {'name': name, 'plain': plain, 'unit': unit, 'value': value, 'window': window, 'freshness': freshness,
           'sources': sources or [], 'unavailable_reason': extra.pop('reason', None), 'fix': extra.pop('fix', None)}
    out.update(extra)
    return out


def tiles(rd, cb, win, sc):
    fresh = rd.ends_on.isoformat()
    if cb['unavailable']:
        t1 = _tile('Chargeback rate', 'Chargebacks over paid orders, 30 days.', None, '%', reason=cb['reason'],
                   fix=cb.get('fix'))
    else:
        t1 = _tile('Chargeback rate', 'Chargebacks opened over paid orders placed, 30 days. Lines: alert 0.15, '
                   'card network early warning 0.65, card network 0.9 percent.', cb['rate'], '%', window='30d',
                   freshness=fresh, sources=[{'table': 'reversed_orders'}, {'table': 'orders'}],
                   higher_is_better=False, tone='bad' if cb['over'] else None)
    if win['unavailable']:
        t2 = _tile('Dispute win rate', 'Disputes won over disputes closed, 28 days.', None, '%', reason=win['reason'],
                   fix=win.get('fix'))
    else:
        t2 = _tile('Dispute win rate', f'Disputes won over disputes closed, 28 days: {win["won"]:,} of '
                   f'{win["closed"]:,}. The floor is {audit.WIN_FLOOR * 100:.0f} percent.',
                   win['rate'] if win['closed'] else None, '%', window='28d', freshness=fresh,
                   sources=[{'table': 'reversed_orders'}], higher_is_better=True,
                   tone='bad' if win['closed'] and win['rate'] < audit.WIN_FLOOR else None,
                   reason=None if win['closed'] else 'no disputes closed in the window')
    t3 = _tile('Vendor scripts on the storefront', f'Tools seen loading code on the site, from the brand record. '
               f'The line is {audit.SCRIPT_MAX}. Hosts outside the record: unavailable, the speed lab keeps totals only.',
               sc['count'] if rd.records('stack') else None, 'n', window='as of', freshness=fresh,
               sources=[{'table': 'brain.stack'}], higher_is_better=False,
               tone='bad' if sc['count'] > audit.SCRIPT_MAX else None,
               reason=None if rd.records('stack') else 'no stack records in the brain')
    return {'chargebacks': t1, 'win_rate': t2, 'scripts': t3}


def insights(cb, win, pay, sc, ctl):
    """The rules behind the insight cards. Each returns the sentence it produces and its capability."""
    out = []
    rule = 'chargeback_rate 30d vs 0.15, 0.65 and 0.9 percent lines; win rate vs 50 percent; payouts scaled'
    if cb['unavailable']:
        out.append({'id': 'chargeback_lines', 'severity': 'medium', 'capability': 'MONEY-C42',
                    'autonomy': audit.AUTONOMY['MONEY-C42'], 'rule': rule,
                    'sentence': f'The chargeback rate is unavailable: {cb["reason"]}.'})
    else:
        if cb['over']:
            s = f'Chargebacks are {cb["rate"] * 100:.2f} percent of paid orders in 30 days, over the ' \
                f'{cb["lines"][cb["over"][-1]] * 100:.2f} percent line.'
        else:
            s = (f'Chargebacks are {cb["rate"] * 100:.2f} percent of paid orders in 30 days, '
                 f'{cb["gap_to_alert"] * 100:.2f} points under the 0.15 percent alert line.')
        if not win['unavailable'] and win['closed']:
            s += f' The store won {win["rate"] * 100:.0f} percent of disputes closed in 28 days.'
        if not pay['unavailable'] and pay['adjustments_scaled'] is not None:
            s += f' Payouts lost ${-pay["adjustments_scaled"]:,.0f} to dispute moves in 28 days.'
        fires = bool(cb['over']) or (not win['unavailable'] and win['closed'] and win['rate'] < audit.WIN_FLOOR)
        out.append({'id': 'chargeback_lines', 'severity': 'high' if cb['over'] else ('medium' if fires else 'info'),
                    'capability': 'MONEY-C42' if fires else None, 'autonomy': audit.AUTONOMY['MONEY-C42'],
                    'sentence': s, 'rule': rule,
                    'stub': ('Build evidence packets for open disputes and review the fraud settings behind lost ones. '
                             'A person does the work; nothing changes on the store until you approve.') if fires else None})
    rule = f'brain.stack: scripts over {audit.SCRIPT_MAX}, tag manager, consent, captcha, agent endpoint'
    parts = [f'{sc["count"]} vendor scripts run on the storefront' + (', one of them a tag manager' if sc['tag_manager'] else '')]
    c, k = ctl['consent'], ctl['captcha']
    parts.append(('consent runs through ' + c['tool']) if c['present'] else 'no consent manager is recorded')
    parts.append(('forms use ' + k['tool'].split(',')[0]) if k['present'] else 'no form captcha is recorded')
    s = parts[0] + '. ' + parts[1][0].upper() + parts[1][1:] + ' and ' + parts[2] + '.'
    if ctl['agent_endpoint']['present']:
        s += ' An AI shopping agent endpoint is published.'
    fires = sc['count'] > audit.SCRIPT_MAX or not c['present'] or not k['present'] or ctl['agent_endpoint']['present']
    out.append({'id': 'storefront_surface', 'severity': 'medium' if fires else 'info',
                'capability': 'SITE-C13' if fires else None, 'autonomy': audit.AUTONOMY['SITE-C13'],
                'sentence': s, 'rule': rule,
                'stub': ('List every script with its owner, what it can read and whether it loads on checkout. '
                         'A person reviews it with you; nothing is removed until you approve.') if fires else None})
    return out


def chart(rd):
    """Chargebacks and inquiries per 1,000 paid orders by month, 12 months, against the 3 lines."""
    end = rd.ends_on
    first = date(end.year - 1 + (end.month == 12), end.month % 12 + 1, 1)
    r = rd.m('reversed_by_month', (end - first).days + 1)
    if r.get('unavailable'):
        return {'unavailable': True, 'reason': r['reason'], 'fix': r.get('fix')}
    rows = r['groups'][-CHART_MONTHS:]
    return {'labels': [g['month'] for g in rows], 'chargebacks': [g['chargebacks_per_1000'] for g in rows],
            'inquiries': [g['inquiries_per_1000'] for g in rows],
            'lines_per_1000': {'alert': round(audit.ALERT_LINE * 1000, 2), 'early_warning': round(audit.EARLY_LINE * 1000, 2),
                               'network': round(audit.metrics().CHARGEBACK_BENCHMARK * 1000, 2)},
            'partial': [g['month'] for g in rows if g['partial']], 'window': f'{len(rows)} months',
            'basis': 'chargebacks and inquiries opened in the month over paid orders placed in the same month'}


def coverage(findings):
    """Every rule and whether it could read its inputs this run: read (fired or passed) or unavailable."""
    by = {f['rule_id']: f for f in findings}
    out = []
    for r in audit.RULES:
        f = by.get(r['rule_id'])
        state = 'unavailable' if f and f['status'] == 'unavailable' else ('fired' if f else 'passed')
        out.append({'rule_id': r['rule_id'], 'name': r['name'], 'capability': r['capability'],
                    'autonomy': audit.AUTONOMY[r['capability']], 'state': state, 'inputs': r['inputs'],
                    'connector': (f.get('unavailable') or {}).get('connector') if f else None})
    return out


def overview(data, brand):
    ends_on = audit.last_full_day(data, brand)
    rd = audit.Reader(data, brand, ends_on)
    b = rd.source.brand
    head = {'brand': b.get('brand'), 'name': b.get('name'), 'as_of': b.get('as_of'),
            'simulated': bool(b.get('simulated') or b.get('fictional')), 'market': b.get('market')}
    cb, win, pay = audit.chargebacks(rd), audit.win_rate(rd), audit.payouts(rd)
    sc, ctl = audit.scripts(rd), audit.controls(rd)
    findings = audit.findings(rd)
    return {'brand': head, 'window': {'ends_on': ends_on.isoformat(), 'days': audit.WINDOW},
            'tiles': tiles(rd, cb, win, sc), 'insights': insights(cb, win, pay, sc, ctl), 'chart': chart(rd),
            'chargebacks': cb, 'win_rate': win, 'payouts': pay, 'scripts': sc, 'controls': ctl,
            'coverage': coverage(findings), 'findings': findings, 'rules': audit.RULES}


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
