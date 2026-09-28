"""API for screen 08-site-speed, under /api/08-site-speed/. Read only.

  GET overview?brand=bombas   per-page speed table, targets, 3 tiles, 2 insights, LCP chart, fix chain with
                              a developer brief stub per fix, filmstrip on the slowest page, script inventory
  GET findings?brand=bombas   audit.run in the audit.md shape

brand defaults to bombas; `sample` reads the server's sample brand. Every number comes from audit.build,
which calls app/metrics.py. Missing inputs come back unavailable with a reason, never 0.
"""
import importlib.util
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SAFE_BRAND = re.compile(r'^[a-z0-9-]{2,40}$')


def _audit():
    name = 'site_speed_audit'
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, HERE / 'audit.py')
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod
        spec.loader.exec_module(mod)
    return sys.modules[name]


audit = _audit()


def source(req, brand):
    if brand == 'sample':
        return req.data
    return audit.tables().brand_data(brand)


def tiles(s):
    slow, t, cost = s['slowest'], s['targets'], s['cost_of_slowness']
    speed_off = s['speed']['unavailable']
    reason = s['speed'].get('reason') if speed_off else None
    return {
        'lcp': {'name': 'Slowest page, mobile LCP', 'plain': 'when the main image shows on a slow phone',
                'value': slow['lcp_ms'] if slow else None, 'unit': 'ms', 'target': t['lcp_ms'],
                'page': slow['label'] if slow else None, 'unavailable_reason': reason or (None if slow else 'no mobile run'),
                'fix': 'speed_lab', 'tone': 'bad' if slow and slow['over_lcp_target'] else 'good'},
        'weight': {'name': 'Page weight, mobile', 'plain': 'data one visit to the slowest page downloads',
                   'value': slow['bytes'] if slow else None, 'unit': 'bytes', 'target': t['bytes'],
                   'unavailable_reason': reason or (None if slow else 'no mobile run'), 'fix': 'speed_lab',
                   'tone': 'bad' if slow and slow['bytes'] > t['bytes'] else 'good'},
        'cost': {'name': 'Cost of slowness, 28 days', 'plain': 'orders lost to main-image time over 2.5 s on mobile',
                 'value': cost['usd'] if cost else None, 'unit': '$', 'money': cost,
                 'unavailable_reason': None if cost else ('; '.join(s['money']['missing']) or reason or 'no speed run'),
                 'fix': 'ga4', 'tone': 'bad' if cost and cost['usd'] > 0 else None},
    }


def insights(s):
    """Two rules. Each returns the sentence it produces, or an unavailable line with why."""
    out = []
    mobile = [r for r in s['speed']['rows'] if r['device'] == 'mobile']
    over = [r for r in mobile if r['over_lcp_target']]
    rule1 = 'a page whose median mobile LCP is over 2,500 ms'
    if s['speed']['unavailable'] or not mobile:
        out.append({'id': 'lcp_over_target', 'rule': rule1, 'fired': False, 'unavailable': True,
                    'sentence': 'No mobile speed run is on file, so this rule cannot run.', 'capability': 'SITE-C21'})
    elif over:
        w = max(over, key=lambda r: r['lcp_ms'])
        out.append({'id': 'lcp_over_target', 'rule': rule1, 'fired': True, 'severity': 'high', 'capability': 'SITE-C26',
                    'sentence': f'{len(over)} of {len(mobile)} pages show their main image after 2.5 s on mobile. '
                                f'The slowest is {w["label"]} at {w["lcp_ms"] / 1000:.1f} s.',
                    'evidence': [f'{r["label"]}: {r["lcp_ms"]:,} ms' for r in over]})
    else:
        out.append({'id': 'lcp_over_target', 'rule': rule1, 'fired': False, 'severity': 'info', 'capability': None,
                    'sentence': f'All {len(mobile)} measured pages show their main image within 2.5 s on mobile.'})
    budget = s['assumption']['script_budget_kb']
    rule2 = f'an outside script over {budget} KB on the slowest page'
    measured = [x for x in s['scripts'] if x['kb'] is not None]
    heavy = [x for x in measured if x['over_budget']]
    if not measured:
        out.append({'id': 'script_over_budget', 'rule': rule2, 'fired': False, 'unavailable': True,
                    'sentence': 'No script weights are on file, so this rule cannot run.', 'capability': 'SITE-C21'})
    elif heavy:
        kb = sum(x['kb'] for x in heavy)
        ms = sum(x['est_ms'] for x in heavy)
        blocking = sum(1 for x in heavy if x['blocking'])
        out.append({'id': 'script_over_budget', 'rule': rule2, 'fired': True, 'severity': 'medium', 'capability': 'SITE-C23',
                    'sentence': f'{len(heavy)} outside scripts are over the {budget} KB budget. Together they add {kb} KB '
                                f'and about {ms / 1000:.1f} s on slow 4G. {blocking} of them block the page.',
                    'evidence': [f'{x["name"]}: {x["kb"]} KB' for x in heavy]})
    else:
        out.append({'id': 'script_over_budget', 'rule': rule2, 'fired': False, 'severity': 'info', 'capability': None,
                    'sentence': f'Every measured outside script is under {budget} KB.'})
    return out


def chart(s):
    rows = s['speed']['rows']
    pages = []
    for r in rows:
        if r['label'] not in pages:
            pages.append(r['label'])
    val = {(r['label'], r['device']): r['lcp_ms'] for r in rows}
    return {'labels': pages, 'series': [{'name': d.capitalize(), 'values': [val.get((p, d)) for p in pages]}
                                        for d in audit.DEVICES],
            'benchmark': s['targets']['lcp_ms'], 'benchmark_label': 'Target', 'unit': 'ms'}


def overview(req, brand):
    s = audit.build(source(req, brand), brand)
    s['tiles'] = tiles(s)
    s['insights'] = insights(s)
    s['chart'] = chart(s)
    return s


def handle(req):
    if req.method != 'GET':
        return 405, {'error': 'this screen is read only'}
    brand = req.arg('brand', 'bombas') or 'bombas'
    if not SAFE_BRAND.match(brand):
        return 400, {'error': 'bad brand'}
    part = req.path[0] if req.path else 'overview'
    try:
        if part == 'overview':
            return overview(req, brand)
        if part == 'findings':
            data = source(req, brand)
            return {'brand': data.brand, 'findings': audit.run(brand, data=data)}
    except ValueError as exc:
        return 400, {'error': str(exc)}
    return 404, {'error': 'unknown endpoint', 'endpoints': ['overview', 'findings']}
