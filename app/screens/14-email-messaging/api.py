"""Email and messaging API: /api/14-email-messaging/...

  GET overview?brand=bombas   tiles, flow table, insights, chart, findings, rules
  GET findings?brand=bombas   the audit findings only (audit.py, contract shape)

Order-matched flow revenue and list growth come from app/metrics.py through audit.Reader; per-flow sends
and the campaign unsubscribe rate are summed in audit.py from the Klaviyo-shaped tables. Insights are rules
in `insights()`, each with the sentence it produces and its capability. Missing is unavailable, never 0.
Default brand is bombas (simulated). Read-only: nothing here writes anywhere.
"""
import importlib.util
import re
from datetime import timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _audit():
    spec = importlib.util.spec_from_file_location('email_messaging_audit', HERE / 'audit.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


audit = _audit()
DEFAULT_BRAND = 'bombas'
AUTONOMY_KIT = {'agent_does': 'agent', 'founder_gate': 'founder_gate', 'human_assist': 'human_assist'}


def _tile(name, plain, r, unit, **extra):
    """A kit tile from one metric result. Unavailable carries the reason and the fix."""
    out = {'name': name, 'plain': plain, 'unit': unit, 'value': None if r.get('unavailable') else r.get('value'),
           'window': (r.get('window') or {}).get('label'), 'freshness': (r.get('freshness') or {}).get('as_of'),
           'unavailable_reason': r.get('reason'), 'fix': r.get('fix'), 'sources': (r.get('freshness') or {}).get('sources')}
    out.update(extra)
    return out


def _delta(now, before):
    if now is None or not before or before < 0 or now < 0:  # a ratio of negative counts reads backwards
        return None
    return round(now / before - 1, 4)


def tiles(rd, as_of):
    prev_end = rd.ends_on - timedelta(days=audit.WINDOW)
    flow = rd.m('revenue_by_flow_order_matched')
    flow_prev = rd.m('revenue_by_flow_order_matched', end=prev_end)
    share = flow.get('share_of_revenue')
    flow_plain = 'Store revenue from orders matched to a flow send, by customer and time. Not the email platform\'s own count.'
    if share is not None:
        flow_plain += f' {round(share * 100, 1)} percent of store revenue in the same orders.'
    growth = rd.m('list_growth')
    growth_prev = rd.m('list_growth', end=prev_end)
    unsub = audit.unsubscribe_rate(rd)
    unsub_prev = audit.unsubscribe_rate(rd, prev_end)
    src = [{'table': 'campaign_sends', 'source': 'generator'}]
    unsub_r = ({'value': unsub['value'], 'window': {'label': f'{audit.WINDOW}d'}, 'freshness': {'as_of': as_of, 'sources': src}}
               if unsub and unsub['value'] is not None else
               {'unavailable': True, 'reason': 'no email campaign was sent in the window, or campaigns are not connected',
                'fix': 'klaviyo', 'window': {'label': f'{audit.WINDOW}d'}})
    return {
        'flow_revenue': _tile('Flow revenue, real orders', flow_plain, flow, '$',
                              delta=_delta(flow.get('value'), flow_prev.get('value')), share_of_revenue=share,
                              inputs=flow.get('inputs')),
        'list_growth': _tile('Net list growth', 'New email subscribers minus unsubscribes and bounces, flows and campaigns.',
                             growth, 'n', delta=_delta(growth.get('value'), growth_prev.get('value')), inputs=growth.get('inputs')),
        'unsubscribe_rate': _tile('Campaign unsubscribe rate', 'Unsubscribes per delivered email campaign send. Under 0.2 percent is typical.',
                                  unsub_r, '%', delta=_delta(unsub and unsub['value'], unsub_prev and unsub_prev['value']),
                                  higher_is_better=False, inputs=unsub and {k: unsub[k] for k in ('unsubscribes', 'delivered', 'campaigns')}),
    }


def flow_rows(stats, mismatch):
    by = {m['flow']: m for m in mismatch}
    out = []
    for name, f in sorted(stats.items(), key=lambda kv: kv[1]['flow_id'] or kv[0]):
        m = by.get(name, {})
        out.append({'flow': name, 'flow_id': f['flow_id'], 'channels': ', '.join(f['channels']), 'messages': len(f['steps']),
                    'sends': f['sends'], 'open_rate': round(f['opens'] / f['email_sends'], 4) if f['email_sends'] else None,
                    'click_rate': round(f['clicks'] / f['sends'], 4) if f['sends'] else None,
                    'unsubscribe_rate': round(f['unsubscribes'] / f['sends'], 4) if f['sends'] else None,
                    'platform_revenue': f['platform_revenue'], 'matched_revenue': m.get('matched_revenue'),
                    'matched_orders': m.get('matched_orders'), 'gap': m.get('gap')})
    return out


def insights(mismatch, findings):
    """The rules behind the insight cards. Each returns the sentence it produces and its capability."""
    out = []
    rule = (f'EMAIL-R01: platform revenue vs order-matched revenue per flow, 28 days; fires above '
            f'{round(audit.MISMATCH_PCT * 100)} percent for flows with {audit.MISMATCH_MIN_ORDERS} or more matched orders')
    fired = [f for f in findings if f['rule_id'] == 'EMAIL-R01' and f['status'] == 'open']
    if fired:
        s = (f'{len(fired)} flows disagree with real orders. ' if len(fired) > 1 else '') + fired[0]['sentence']
        out.append({'id': 'flow_mismatch', 'severity': 'medium', 'capability': 'LIFE-C20', 'autonomy': 'agent_does',
                    'sentence': s, 'rule': rule})
    else:
        checked = [m for m in mismatch if m['gap'] is not None and (m['matched_orders'] or 0) >= audit.MISMATCH_MIN_ORDERS]
        if checked:
            plat = sum(m['platform_revenue'] for m in checked)
            real = sum(m['matched_revenue'] for m in checked)
            worst = max(checked, key=lambda m: abs(m['gap']))
            s = (f'All {len(checked)} flows are within {round(audit.MISMATCH_PCT * 100)} percent of real orders. '
                 f'The platform shows ${plat:,.0f} and orders show ${real:,.0f}. {worst["flow"]} is furthest off at '
                 f'{abs(round(worst["gap"] * 100))} percent.')
        else:
            s = 'No flow has enough matched orders to check against the platform count.'
        out.append({'id': 'flow_mismatch', 'severity': 'info', 'capability': 'LIFE-C20', 'autonomy': 'agent_does',
                    'sentence': s, 'rule': rule})
    sun = next((f for f in findings if f['rule_id'] == 'EMAIL-R12' and f['status'] == 'open'), None)
    rule = (f'EMAIL-R12: email campaigns sent to more people than the "{audit.ENGAGED_AUDIENCE}" segment, 28 days, '
            f'with no live sunset flow')
    if sun:
        stake = sun['money_at_stake']
        s = sun['sentence'] + (f' That is ${stake["usd"]:,} of flow revenue every 28 days at risk.' if stake else '')
        out.append({'id': 'sunset', 'severity': sun['severity'], 'capability': 'LIFE-C08', 'autonomy': 'founder_gate',
                    'sentence': s, 'rule': rule})
    else:
        out.append({'id': 'sunset', 'severity': 'info', 'capability': None, 'autonomy': None,
                    'sentence': 'Every email campaign in 28 days went to the engaged segment or a smaller one.', 'rule': rule})
    return out


def chart(mismatch):
    if not mismatch:
        return {'unavailable': True, 'reason': 'no flow sends in the window', 'fix': 'klaviyo'}
    short = [re.sub(r'\s*\b(Series|Abandoned|Abandonment)\b\s*', ' ', m['flow']).strip() for m in mismatch]
    return {'labels': short, 'flows': [m['flow'] for m in mismatch], 'platform': [m['platform_revenue'] for m in mismatch],
            'matched': [m['matched_revenue'] for m in mismatch], 'window': f'{audit.WINDOW}d',
            'basis': 'platform is the email platform\'s attributed revenue; real orders are net revenue of orders matched to a send'}


def overview(brand):
    ends_on = audit.last_full_day(brand)
    rd = audit.Reader(brand, ends_on)
    b = rd.data.brand
    head = {'brand': b.get('brand'), 'name': b.get('name'), 'as_of': b.get('as_of'),
            'simulated': bool(b.get('simulated') or b.get('fictional')), 'market': b.get('market')}
    findings = audit.run(brand, {'ends_on': ends_on.isoformat()}, reader=rd)
    out = {'brand': head, 'window': {'ends_on': ends_on.isoformat(), 'days': audit.WINDOW},
           'tiles': tiles(rd, b.get('as_of')), 'findings': findings, 'rules': audit.RULES}
    stats = audit.flow_stats(rd)
    if stats is None:
        out.update(unavailable=True, reason='Email flows and campaigns are not connected.', fix='klaviyo')
        return out
    matched = rd.m('revenue_by_flow_order_matched')
    mismatch = audit.mismatch_rows(stats, matched if not matched.get('unavailable') else {})
    out.update(unavailable=False, flows=flow_rows(stats, mismatch), insights=insights(mismatch, findings),
               chart=chart(mismatch), campaigns=audit.campaigns(rd))
    return out


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
