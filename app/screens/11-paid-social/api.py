"""Paid social API: /api/11-paid-social/...

  GET overview?brand=bombas   tiles, kill and scale list, creative table, insights, chart, findings
  GET findings?brand=bombas   the audit findings only (audit.py, contract shape)

Every number comes from app/metrics.py through audit.Reader. Insights are rules in `insights()`,
each with the sentence it produces and the capability it maps to. Missing is unavailable, never 0.
Default brand is bombas (simulated). Read-only: nothing here writes anywhere.
"""
import calendar
import importlib.util
import re
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _audit():
    spec = importlib.util.spec_from_file_location('paid_social_audit', HERE / 'audit.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


audit = _audit()
DEFAULT_BRAND = 'bombas'
CHART_DAYS = 90
AUTONOMY_KIT = {'agent_does': 'agent', 'founder_gate': 'founder_gate', 'human_assist': 'human_assist'}


def _tile(name, plain, r, unit, **extra):
    """A kit tile from one metric result. Unavailable carries the reason and the fix."""
    out = {'name': name, 'plain': plain, 'unit': unit, 'value': None if r.get('unavailable') else r.get('value'),
           'window': (r.get('window') or {}).get('label'), 'freshness': (r.get('freshness') or {}).get('as_of'),
           'unavailable_reason': r.get('reason'), 'fix': r.get('fix'), 'sources': (r.get('freshness') or {}).get('sources')}
    out.update(extra)
    return out


def _delta(now, before):
    if now is None or not before:
        return None
    return round(now / before - 1, 4)


def pacing(rd):
    """Spend pace: this month's spend projected to month end against the 28-day run rate."""
    end = rd.ends_on
    run = rd.m('spend', 28, channel='meta')
    elapsed = end.day
    mtd = rd.m('spend', elapsed, channel='meta')
    days_in_month = calendar.monthrange(end.year, end.month)[1]
    if run.get('unavailable') or mtd.get('unavailable'):
        bad = run if run.get('unavailable') else mtd
        return _tile('Spend pace', 'Meta spend this month against the 28-day run rate.', bad, '$')
    per_day_run = run['value'] / 28
    projected = round(mtd['value'] / elapsed * days_in_month, 2)
    at_run = round(per_day_run * days_in_month, 2)
    plain = (f'${mtd["value"]:,.0f} spent in {elapsed} days of {end.strftime("%B")}. '
             f'The 28-day run rate is ${per_day_run:,.0f} a day, or ${at_run:,.0f} for the month.')
    return _tile('Spend pace, month end', plain, dict(mtd, value=projected), '$', delta=_delta(projected, at_run),
                 delta_label='vs 28-day run rate', window=f'month to date, {elapsed}d',
                 inputs={'spend_mtd': mtd['value'], 'days_elapsed': elapsed, 'days_in_month': days_in_month,
                         'spend_28d': run['value'], 'run_rate_per_day': round(per_day_run, 2)},
                 formula='spend_mtd / days_elapsed x days_in_month, against spend_28d / 28 x days_in_month')


def tiles(rd):
    roas = rd.m('period_roas', 28, channel='meta')
    roas_prev = rd.m('period_roas', 28, rd.ends_on - timedelta(days=28), channel='meta')
    mer = rd.m('mer', 28)
    mer_prev = rd.m('mer', 28, rd.ends_on - timedelta(days=28))
    cpa = rd.m('cpa', 28, channel='meta')
    cpa_prev = rd.m('cpa', 28, rd.ends_on - timedelta(days=28), channel='meta')
    return {
        'pacing': pacing(rd),
        'roas': _tile('Meta ROAS', 'What Meta says it returned per dollar: purchase value over spend, 28-day totals.',
                      roas, 'x', delta=_delta(roas.get('value'), roas_prev.get('value')), basis=roas.get('basis')),
        'mer': _tile('MER', 'Store net revenue over all paid spend (Meta and Google), 28 days. The store\'s own count.',
                     mer, 'x', delta=_delta(mer.get('value'), mer_prev.get('value')),
                     spend_by_channel=mer.get('spend_by_channel')),
        'cpa': _tile('Meta CPA', 'Spend per purchase Meta reports, 28 days.', cpa, '$',
                     delta=_delta(cpa.get('value'), cpa_prev.get('value')), higher_is_better=False),
    }


def creative_rows(windows, th, ends_on):
    """One row per ad (7 days). Ads that share an image keep their own row and carry the flag."""
    now, prev = windows[0], windows[1]
    rows = []
    for ad in now.values():
        p = prev.get(ad['ad'])
        v, why = audit.verdict(ad, p, th, ends_on)
        fat = audit.fatigue(ad, p)
        rows.append({'ad': ad['ad'], 'campaign': ad.get('campaign_name'), 'adset': ad.get('adset_id'),
                     'format': ad.get('format'), 'spend': ad['spend'], 'purchases': ad['purchases'],
                     'purchase_value': ad['purchase_value'], 'roas': ad['roas'], 'cpa': ad['cpa'], 'ctr': ad['ctr'],
                     'ctr_prev': p.get('ctr') if p else None, 'frequency': ad.get('frequency'),
                     'shared_creative': ad.get('shared_creative'), 'dynamic_creative': ad.get('dynamic_creative'),
                     'verdict': v, 'why': why, 'fatigue': bool(fat), 'first_day': ad.get('first_day')})
    rows.sort(key=lambda r: -r['spend'])
    return rows


def kill_scale(rows, findings):
    stake = {f['entity']['id']: f['money_at_stake'] for f in findings if f['rule_id'] == 'PAID-R01'}
    kill = [dict(r, money_at_stake=stake.get(r['ad'])) for r in rows if r['verdict'] == 'kill']
    kill.sort(key=lambda r: -((r['money_at_stake'] or {}).get('usd') or 0))
    scale = sorted([r for r in rows if r['verdict'] == 'scale'], key=lambda r: -(r['roas'] or 0))
    return {'kill': kill, 'scale': scale}


def insights(ks, rows, th, findings):
    """The rules behind the insight cards. Each returns the sentence it produces and its capability."""
    out = []
    nk, ns = len(ks['kill']), len(ks['scale'])
    at_stake = sum((r['money_at_stake'] or {}).get('usd') or 0 for r in ks['kill'])
    if th['break_even'] is None:
        out.append({'id': 'kill_scale', 'severity': 'high', 'capability': 'MEDIA-C17', 'autonomy': 'founder_gate',
                    'sentence': 'Break-even ROAS is unknown, so no ad can be called a kill or a scale.',
                    'rule': 'needs finance_inputs.target_gross_margin'})
    else:
        sentence = f'{nk} ads are under break-even this week and {ns} are ready to scale.'
        if nk:
            sentence += f' The {nk} under break-even did not pay back ${at_stake:,.0f} in 7 days.'
        out.append({'id': 'kill_scale', 'severity': 'high' if nk else 'info', 'capability': 'MEDIA-C17',
                    'autonomy': 'founder_gate', 'sentence': sentence,
                    'rule': (f'kill: 7-day ROAS < {th["break_even"]:.2f}x break-even, live all 7 days, spend >= '
                             f'${th["floor"]:,.0f}. scale: ROAS >= {th["target_roas"]:.2f}x target and frequency < '
                             f'{audit.SCALE_MAX_FREQUENCY}') if th['target_roas'] else 'kill only: no target ROAS on file'})
    tired = [f for f in findings if f['rule_id'] == 'PAID-R03']
    rule = (f'CTR last 7 days vs the 7 before down {round(audit.FATIGUE_CTR_DROP * 100)} percent or more, '
            f'frequency up, spend >= the floor')
    if tired:
        worst = tired[0]
        out.append({'id': 'fatigue', 'severity': worst['severity'] if worst['severity'] != 'critical' else 'high',
                    'capability': 'CREA-C15', 'autonomy': 'agent',
                    'sentence': (f'{len(tired)} ads are wearing out. ' if len(tired) > 1 else '') + worst['sentence'],
                    'rule': rule})
    else:
        checked = sum(1 for r in rows if r['ctr_prev'] is not None and th['floor'] is not None and r['spend'] >= th['floor'])
        out.append({'id': 'fatigue', 'severity': 'info', 'capability': None, 'autonomy': None,
                    'sentence': f'No ad is wearing out. Click rate held within {round(audit.FATIGUE_CTR_DROP * 100)} '
                                f'percent over 14 days for all {checked} ads above the floor.',
                    'rule': rule})
    return out


def chart(rd):
    r = rd.m('spend', CHART_DAYS, channel='meta', by='day')
    if r.get('unavailable'):
        return {'unavailable': True, 'reason': r.get('reason'), 'fix': r.get('fix')}
    days = {g['day']: g for g in r['groups']}
    start = rd.ends_on - timedelta(days=CHART_DAYS - 1)
    labels = [(start + timedelta(days=i)).isoformat() for i in range(CHART_DAYS)]
    return {'labels': labels, 'spend': [days[d]['spend'] if d in days else None for d in labels],
            'purchases': [days[d]['purchases'] if d in days else None for d in labels],
            'window': f'{CHART_DAYS}d', 'basis': 'platform reported purchases (Meta 7 day click, 1 day view)'}


def overview(data, brand):
    ends_on = audit.last_full_day(data, brand)
    rd = audit.Reader(data, brand, ends_on)
    source = audit.brand_data(brand) if brand else data
    b = source.brand
    head = {'brand': b.get('brand'), 'name': b.get('name'), 'as_of': b.get('as_of'),
            'simulated': bool(b.get('simulated') or b.get('fictional')), 'market': b.get('market')}
    first, _ = rd.ads(7)
    if first.get('unavailable'):
        return {'brand': head, 'unavailable': True, 'reason': first.get('reason'), 'fix': first.get('fix'),
                'tiles': tiles(rd), 'findings': audit.run(brand, {'ends_on': ends_on.isoformat()}, data=data)}
    th = audit.thresholds(rd)
    windows = audit.ad_windows(rd)
    findings = audit.run(brand, {'ends_on': ends_on.isoformat()}, data=data)
    rows = creative_rows(windows, th, ends_on)
    ks = kill_scale(rows, findings)
    return {'brand': head, 'unavailable': False, 'window': {'ends_on': ends_on.isoformat(), 'days': 7},
            'tiles': tiles(rd), 'thresholds': th, 'kill_scale': ks, 'creatives': rows,
            'insights': insights(ks, rows, th, findings), 'chart': chart(rd), 'findings': findings,
            'rules': audit.RULES}


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
