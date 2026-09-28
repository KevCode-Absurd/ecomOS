"""Store health API: /api/06-store-health/...

  GET overview?brand=bombas   setup checklist, reversed orders (3 legs), payment mix, apps and scripts, uptime,
                              tiles, insights, chart, findings
  GET findings?brand=bombas   the audit findings only (audit.py, contract shape)

Numbers come from app/metrics.py (reversed orders from data.sqlite), brand facts from the brain (stack, policies,
site_map), all through audit.Reader. Insights are rules in `insights()`, each with the sentence it produces and the
capability it maps to. Missing is unavailable, never 0. Cash on delivery legs read null unless the market uses them.
Default brand is bombas (simulated). Read-only.
"""
import importlib.util
import re
import statistics
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _audit():
    spec = importlib.util.spec_from_file_location('store_health_audit', HERE / 'audit.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


audit = _audit()
DEFAULT_BRAND = 'bombas'
CHART_MONTHS = 24
TRAILING = 4
# Stack record field -> what the tool does, in plain words. Fields not listed show their record text.
TOOL_JOB = {'reviews_app': 'Reviews', 'upsell_app': 'Cart upsells', 'tag_manager': 'Tag manager',
            'cookie_consent': 'Consent banner', 'ab_testing': 'A/B tests', 'performance_vendor': 'Speed and edge',
            'form_security': 'Form captcha', 'agent_commerce_endpoint': 'AI shopping agent endpoint',
            'theme': 'Theme', 'platform': 'Platform'}
METHOD = {'card': 'Card', 'shop_pay': 'Shop Pay', 'paypal': 'PayPal', 'apple_pay': 'Apple Pay',
          'google_pay': 'Google Pay', 'card_present': 'Card in store', 'affirm': 'Affirm', 'klarna': 'Klarna',
          'afterpay': 'Afterpay', 'cod': 'Cash on delivery'}


def _tile(name, plain, value, unit, window=None, freshness=None, sources=None, **extra):
    out = {'name': name, 'plain': plain, 'unit': unit, 'value': value, 'window': window, 'freshness': freshness,
           'sources': sources or [], 'unavailable_reason': extra.pop('reason', None), 'fix': extra.pop('fix', None)}
    out.update(extra)
    return out


def _cod_market(rd):
    return str((rd.source.brand or {}).get('market') or '').upper() in audit.metrics().COD_MARKETS


# ---------------------------------------------------------------- reversed orders

def returns_windows(rd):
    return [rd.m('returns_by_reason', audit.WINDOW, end=rd.ends_on - timedelta(days=audit.WINDOW * k))
            for k in range(TRAILING + 1)]


def reversed_legs(rd):
    """The 3 legs: returns, return to sender (plus return to origin where cash on delivery exists), chargebacks."""
    rets = returns_windows(rd)
    now = rets[0]
    if now.get('unavailable'):
        returns = {'unavailable': True, 'reason': now['reason'], 'fix': now.get('fix')}
    else:
        n = now['inputs']['paid_orders']
        prev = [w['inputs']['returns'] / w['inputs']['paid_orders'] for w in rets[1:]
                if not w.get('unavailable') and w['inputs']['paid_orders']]
        returns = {'unavailable': False, 'returns': now['value'], 'paid_orders': n,
                   'per_1000': round(now['value'] / n * 1000, 2) if n else None,
                   'median_per_1000': round(statistics.median(prev) * 1000, 2) if len(prev) == TRAILING else None,
                   'refunded': round(sum(g['amount'] for g in now['groups']), 2),
                   'by_reason': [dict(g, share=round(g['returns'] / now['value'], 4) if now['value'] else None)
                                 for g in now['groups']],
                   'window': now['window'], 'basis': now.get('basis')}
    rts = rd.m('return_to_sender_rate', audit.WINDOW)
    sender = ({'unavailable': True, 'reason': rts['reason'], 'fix': rts.get('fix')} if rts.get('unavailable') else
              {'unavailable': False, 'rate': rts['value'], 'returned': rts['inputs']['numerator'],
               'orders': rts['inputs']['denominator'], 'per_1000': round(rts['value'] * 1000, 2),
               'basis': rts.get('basis'), 'window': rts['window']})
    rto = rd.m('rto_rate', audit.WINDOW)
    cb = audit.chargeback_now(rd)
    win = rd.m('dispute_win_rate', audit.WINDOW)
    disp = audit.disputes(rd)
    pay = rd.m('payout_reversals', audit.WINDOW)
    charge = dict(cb)
    charge.update({
        'win_rate': None if win.get('unavailable') else win['value'],
        'closed': None if win.get('unavailable') else win['inputs']['denominator'],
        'open': None if disp.get('unavailable') else disp['value'],
        'open_amount': None if disp.get('unavailable') else disp['amount'],
        'aged': None if disp.get('unavailable') else disp['aged_count'],
        'aged_amount': None if disp.get('unavailable') else disp['aged_amount'],
        'inquiries_open': None if disp.get('unavailable') else (disp['by_type'].get('inquiry') or {}).get('count', 0),
        'dispute_days': audit.DISPUTE_DAYS,
        'payouts': None if pay.get('unavailable') else {k: pay.get(k) for k in ('charges_gross', 'refunds_gross', 'net')}
                   | {'adjustments_gross': pay['value'], 'window': pay['window']},
    })
    cod = _cod_market(rd)
    return {'returns': returns, 'return_to_sender': sender, 'chargebacks': charge,
            # Market-only legs: null for a US brand, and the page hides them.
            'return_to_origin': (None if rto.get('unavailable') else rto['value']) if cod else None,
            'cod_market': cod, 'cod_note': None if cod else rto.get('reason')}


def payment_mix(rd):
    mix = rd.m('payment_method_mix', audit.CB_WINDOW)
    if mix.get('unavailable'):
        return {'unavailable': True, 'reason': mix['reason'], 'fix': mix.get('fix')}
    n = mix['inputs']['orders']
    rows = [{'method': METHOD.get(m, m.replace('_', ' ')), 'key': m,
             'group': audit.metrics().pay_group(m), 'share': s, 'orders': round(s * n)}
            for m, s in mix['by_method'].items()]
    groups = {g: v for g, v in mix['value'].items() if not (g == 'cod' and v is None)}
    return {'unavailable': False, 'rows': rows, 'groups': groups, 'orders': n, 'window': mix['window'],
            'bnpl_offered': (mix['counts'].get('bnpl') or 0) > 0}


# ---------------------------------------------------------------- apps and scripts

def page_weight(rd):
    """Median bytes and requests per page and device from speed_runs, when the lab has runs. Per-app weight needs a
    request log by script host, which speed_runs does not carry."""
    rows = rd.table('speed_runs')
    if not rows:
        return {'unavailable': True, 'reason': 'no speed runs recorded', 'fix': 'speed_lab'}
    dev = 'device' if 'device' in rows[0] else 'variant'
    by = {}
    for r in rows:
        if r.get('bytes') is not None and r.get('requests') is not None:
            by.setdefault((r['page'], r[dev]), []).append(r)
    out = [{'page': p, 'device': d, 'runs': len(rs), 'bytes': statistics.median(r['bytes'] for r in rs),
            'requests': statistics.median(r['requests'] for r in rs)} for (p, d), rs in sorted(by.items())]
    return {'unavailable': not out, 'rows': out, 'source': rows[0].get('source'),
            'note': 'Page weight is the median of the lab runs. Weight per app needs a request log by script host; '
                    'speed_runs has totals only.'}


def apps(rd):
    out = []
    for r in rd.records('stack'):
        field = r.get('field') or ''
        if field in ('platform', 'theme') or field.startswith('platform_cost'):
            continue
        src = r.get('source') or {}
        onsite = src.get('type') == 'site'
        out.append({'tool': r.get('value') if isinstance(r.get('value'), str) else None, 'job': TOOL_JOB.get(field),
                    'text': r.get('text'), 'seen': 'on the storefront' if onsite else 'named in ' + (src.get('type') or 'a source'),
                    'onsite': onsite, 'ref': r['id'], 'url': src.get('ref'), 'date': r.get('date'), 'tier': r.get('tier'),
                    'monthly_cost': None, 'revenue_attributed': None, 'script_bytes': None})
    out.sort(key=lambda a: (not a['onsite'], a['job'] or 'zz'))
    return {'rows': out, 'onsite': sum(1 for a in out if a['onsite']),
            'cost_reason': 'no app inventory yet: stack records carry no monthly cost, owner or revenue link',
            'weight': page_weight(rd)}


# ---------------------------------------------------------------- uptime

def uptime(rd):
    have = rd.table('uptime_checks'), rd.table('checkout_synthetic_tests')
    if all(have):
        return {'unavailable': False, 'note': 'monitor connected; the incident timeline is a later round'}
    return {'unavailable': True, 'reason': 'no synthetic monitor connected',
            'missing': [t for t, h in zip(('uptime_checks', 'checkout_synthetic_tests'), have) if not h],
            'fix': 'Connect a synthetic monitor (uptime checks every 5 minutes, a test order per payment method daily). '
                   'It fills uptime_checks and checkout_synthetic_tests.', 'connector': 'synthetic monitor'}


# ---------------------------------------------------------------- tiles, insights, chart

def tiles(rd, items, legs, up):
    fresh = rd.ends_on.isoformat()
    passed = sum(1 for i in items if i['status'] == 'pass')
    failed = sum(1 for i in items if i['status'] == 'fail')
    t1 = _tile('Setup checklist', f'{passed} of {len(items)} items pass, {failed} fail and '
               f'{len(items) - passed - failed} cannot be checked yet. Unchecked items count as not done.',
               round(passed / len(items), 4) if items else None, '%', freshness=fresh,
               sources=[{'table': 'brain'}, {'table': 'reversed_orders'}, {'table': 'orders'}],
               tone='bad' if failed else None)
    cb = legs['chargebacks']
    if cb['unavailable']:
        t2 = _tile('Chargeback rate', 'Chargebacks over paid orders, 30 days.', None, '%', reason=cb['reason'], fix=cb.get('fix'))
    else:
        t2 = _tile('Chargeback rate', f'Chargebacks over paid orders, 30 days. The card network line is '
                   f'{cb["benchmark"] * 100:.1f} percent.' + (f' Your 90 days before: {cb["own"] * 100:.2f} percent.'
                                                              if cb['own'] is not None else ''),
                   cb['rate'], '%', window='30d', freshness=fresh, sources=[{'table': 'reversed_orders'}, {'table': 'orders'}],
                   delta=round(cb['rate'] / cb['own'] - 1, 4) if cb['own'] else None, higher_is_better=False,
                   tone='bad' if cb['fires'] else None)
    r = legs['returns']
    if r['unavailable']:
        t3 = _tile('Returns per 1,000 orders', 'Returns opened over paid orders, 28 days.', None, 'n',
                   reason=r['reason'], fix=r.get('fix'))
    else:
        t3 = _tile('Returns per 1,000 orders', 'Returns opened over paid orders placed, 28 days. Carrier returns are '
                   'counted apart.' + (f' Own median of the 4 windows before: {r["median_per_1000"]:.1f}.'
                                       if r['median_per_1000'] is not None else ''),
                   r['per_1000'], 'n', window='28d', freshness=fresh, sources=[{'table': 'reversed_orders'}, {'table': 'orders'}],
                   delta=round(r['per_1000'] / r['median_per_1000'] - 1, 4) if r['median_per_1000'] else None,
                   higher_is_better=False)
    t4 = _tile('Uptime and checkout', 'Share of checks where the store loaded and a test order went through, 30 days.',
               None, '%', reason=up.get('reason'), fix=up.get('connector'))
    return {'checklist': t1, 'chargebacks': t2, 'returns': t3, 'uptime': t4}


def insights(rd, legs):
    """The rules behind the insight cards. Each returns the sentence it produces and its capability."""
    out = []
    cb = legs['chargebacks']
    rule = (f'chargeback_rate, 30 days, fires over the {audit.metrics().CHARGEBACK_BENCHMARK * 100:.1f} percent card '
            f'network benchmark or more than {audit.CB_OVER * 100:.0f} percent over the brand\'s own 90 days before '
            f'(room spec)')
    if cb['unavailable']:
        out.append({'id': 'chargebacks', 'severity': 'medium', 'capability': 'SITE-C67', 'autonomy': 'founder_gate',
                    'sentence': f'The chargeback rate is unavailable: {cb["reason"]}.', 'rule': rule})
    else:
        s = (f'Chargebacks are {cb["rate"] * 100:.2f} percent of paid orders in 30 days, '
             + ('over' if cb['over_benchmark'] else 'under') + f' the {cb["benchmark"] * 100:.1f} percent line.')
        if cb['own'] is not None:
            s += f' The 90 days before ran {cb["own"] * 100:.2f} percent.'
        if cb['by_reason']:
            top = cb['by_reason'][0]
            s += f' Top reason: {top[0].replace("_", " ")} ({top[1]} of {cb["chargebacks"]}).'
        out.append({'id': 'chargebacks', 'severity': 'high' if cb['fires'] else 'info',
                    'capability': 'SITE-C67' if cb['fires'] else None, 'autonomy': 'founder_gate', 'sentence': s,
                    'rule': rule, 'stub': ('Review checkout fraud and address checks for the reasons behind the rise. Nothing on the '
                             'store changes until you approve.') if cb['fires'] else None})
    r = legs['returns']
    rule = (f'returns_by_reason, 28 days: the top reason over {audit.CONCENTRATION * 100:.0f} percent of returns is a '
            f'concentration; its rate is set against its own median of the 4 windows before')
    if r['unavailable'] or not r['by_reason']:
        out.append({'id': 'return_reason', 'severity': 'medium', 'capability': 'LIFE-C26', 'autonomy': 'founder_gate',
                    'sentence': 'Return reasons are unavailable: ' + (r.get('reason') or 'no returns') + '.', 'rule': rule})
    else:
        top = r['by_reason'][0]
        prev = [w for w in returns_windows(rd)[1:] if not w.get('unavailable')]
        rates = [next((g['per_order'] for g in w['groups'] if g['reason'] == top['reason']), 0) for w in prev]
        med = statistics.median(rates) if len(rates) == TRAILING else None
        conc = top['share'] > audit.CONCENTRATION
        s = (f'"{top["reason"].capitalize()}" is {top["share"] * 100:.0f} percent of returns in 28 days: '
             f'{top["per_order"] * 1000:.1f} per 1,000 orders')
        s += f', own median {med * 1000:.1f}.' if med is not None else '.'
        out.append({'id': 'return_reason', 'severity': 'medium' if conc else 'info',
                    'capability': 'LIFE-C26' if conc else None, 'autonomy': 'founder_gate', 'sentence': s,
                    'rule': rule, 'stub': (f'Draft the returns and exchange changes aimed at "{top["reason"]}" returns, for example '
                             f'an exchange-first path. Nothing changes on the store until you approve.') if conc else None})
    return out


def chart(rd):
    """Returns and chargebacks per 1,000 paid orders by month, 24 months, from 2 whole-month windows (400 day cap)."""
    end = rd.ends_on
    first = date(end.year - 2 + (end.month == 12), end.month % 12 + 1, 1)
    mid = date(first.year + 1, first.month, 1)
    parts = [rd.m('reversed_by_month', (mid - first).days, end=mid - timedelta(days=1)),
             rd.m('reversed_by_month', (end - mid).days + 1, end=end)]
    bad = next((p for p in parts if p.get('unavailable')), None)
    if bad:
        return {'unavailable': True, 'reason': bad['reason'], 'fix': bad.get('fix')}
    rows = [g for p in parts for g in p['groups']][-CHART_MONTHS:]
    return {'labels': [g['month'] for g in rows], 'returns': [g['returns_per_1000'] for g in rows],
            'carrier_returns': [g['carrier_returns_per_1000'] for g in rows],
            'chargebacks': [g['chargebacks_per_1000'] for g in rows],
            'inquiries': [g['inquiries_per_1000'] for g in rows],
            'benchmark_per_1000': audit.metrics().CHARGEBACK_BENCHMARK * 1000,
            'partial': [g['month'] for g in rows if g['partial']], 'window': f'{len(rows)} months',
            'basis': 'each leg opened in the month over paid orders placed in the same month'}


def overview(data, brand):
    ends_on = audit.last_full_day(data, brand)
    rd = audit.Reader(data, brand, ends_on)
    b = rd.source.brand
    head = {'brand': b.get('brand'), 'name': b.get('name'), 'as_of': b.get('as_of'),
            'simulated': bool(b.get('simulated') or b.get('fictional')), 'market': b.get('market')}
    items = audit.checklist(rd)
    findings = audit.findings(rd, items)
    legs = reversed_legs(rd)
    up = uptime(rd)
    return {'brand': head, 'window': {'ends_on': ends_on.isoformat(), 'days': audit.WINDOW},
            'checklist': items, 'reversed': legs, 'payments': payment_mix(rd), 'apps': apps(rd), 'uptime': up,
            'tiles': tiles(rd, items, legs, up), 'insights': insights(rd, legs), 'chart': chart(rd),
            'findings': findings, 'rules': audit.RULES}


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
