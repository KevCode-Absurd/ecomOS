"""API for 07-landing-pages-cro, under /api/07-landing-pages-cro/.

  GET  summary?window=28d     funnel by device (break marked per device) and by source, money at stake
                              by device, page registry, message match on paid social landers, the PDP
                              objection-proof map, the test registry, 3 tiles, 2 insights (rules with
                              their sentences), conversion rate by device for 12 weeks, the findings
  GET  findings?window=28d    audit.run for the brand, in the audit contract shape

Numbers come from app/metrics.py (session_funnel, aov, lcp_ms) for brand=bombas, which reads
app/data/brands/bombas/. Brand facts come from app/brain/bombas/. Missing numbers stay null with a
reason, never 0. Decisions go through the shared /api/decisions log. Read-only otherwise.
"""
import importlib.util
import json
import math
import re
import sys
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent
SCREEN = '07-landing-pages-cro'
BRAND = 'bombas'
CHART_WEEKS = 12
SOURCE_ROWS = 8
MDE = 0.10              # relative lift for the sample size example
MIN_TEST_DAYS = 14

# page type from the URL path, when site_map does not list the page
PATH_TYPES = ((r'^/$', 'home'), (r'^/products/', 'PDP'), (r'^/collections/', 'collection'), (r'^/pages/', 'lander'),
              (r'^/cart', 'cart'), (r'^/account', 'account'), (r'^/policies/', 'legal'))


def _load(name, path):
    mod = sys.modules.get(name)
    if mod is None or getattr(mod, '__file__', None) != str(path):
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod
        spec.loader.exec_module(mod)
    return mod


def audit():
    return _load('cro_audit', HERE / 'audit.py')


def M():
    return audit().metrics_module()


def window_for(req_window):
    days = int((req_window or '28d')[:-1])
    if days < 7 or days > 91:
        raise ValueError('window must be 7d to 91d')
    as_of = M().resolve(None, {'brand': BRAND}).brand['as_of']
    return {'ends_on': as_of, 'days': days, 'trailing': 4}


# ---------------------------------------------------------------- funnel

def funnel_by_device(db):
    if db['unavailable']:
        return {'unavailable': True, 'reason': db['reason'], 'fix': db['fix'], 'rows': []}
    rows = []
    for d in db['devices']:
        c = d['counts']
        rows.append({'device': d['device'], 'label': d['label'], 'sessions': c['sessions'], 'add_to_cart': c['add_to_cart'],
                     'checkout': c['checkout'], 'purchase': c['purchase'], 'conversion_rate': c['conversion_rate'],
                     'steps': [{k: s.get(k) for k in ('step', 'label', 'current', 'median', 'money', 'windows_agreeing')}
                               for s in d['steps']],
                     'break_step': d['break_step'], 'break_money': d['break_money'], 'money': d['money']})
    return {'unavailable': False, 'rows': rows, 'aov': db['aov'], 'net_revenue_est': db['net_revenue_est'],
            'basis': 'Each step against its own median of the 6 windows before. The break is the step with the most money.'}


def funnel_by_source(w):
    r = M().compute('session_funnel', None, brand=BRAND, window=f"{w['days']}d", end=w['ends_on'], by='channel_group')
    if r.get('unavailable'):
        return {'unavailable': True, 'reason': r.get('reason'), 'fix': r.get('fix'), 'rows': []}
    groups = r['groups']
    top, rest = groups[:SOURCE_ROWS], groups[SOURCE_ROWS:]
    rows = [dict(g, source=g['channel_group']) for g in top]
    if rest:
        t = {f: sum(g[f] for g in rest) for f in ('sessions', 'product_view', 'add_to_cart', 'checkout', 'purchase')}
        rows.append(dict(t, source=f'{len(rest)} other sources', **M().funnel_rates(t)))
    return {'unavailable': False, 'rows': rows, 'total': r['inputs'], 'rates': r['rates'], 'basis': r.get('basis')}


# ---------------------------------------------------------------- pages

def path_type(path):
    return next((t for pat, t in PATH_TYPES if re.search(pat, path)), 'other')


def site_map_pages(b):
    """Pages the brain's site_map lists, with the type it gives them."""
    out = {}
    for rec in b.records('site_map'):
        v = rec.get('value')
        items = [v] if isinstance(v, dict) else v if isinstance(v, list) else []
        for it in items:
            if isinstance(it, dict) and it.get('url') and not it['url'].endswith('.xml'):
                out[urlparse(it['url']).path or '/'] = {'type': it.get('type'), 'record': rec['id']}
    return out


def speed(page):
    r = M().compute('lcp_ms', None, brand=BRAND, page=page, device='mobile')
    return {'lcp_ms': r.get('value'), 'reason': r.get('reason')}


def registry(w, b, captured):
    r = M().compute('session_funnel', None, brand=BRAND, window=f"{w['days']}d", end=w['ends_on'], by='landing_page')
    by_page = {g['landing_page']: g for g in (r.get('groups') or [])}
    listed = site_map_pages(b)
    rows = []
    for page in sorted(set(by_page) | set(listed), key=lambda p: (-(by_page.get(p) or {}).get('sessions', 0), p)):
        g = by_page.get(page)
        sm = listed.get(page)
        sp = speed(page)
        rows.append({'page': page, 'type': sm['type'] if sm else path_type(page), 'type_from': 'site_map' if sm else 'path rule',
                     'in_site_map': bool(sm), 'captured': page in captured,
                     'sessions': g['sessions'] if g else None, 'add_to_cart_rate': g['add_to_cart_rate'] if g else None,
                     'conversion_rate': g['conversion_rate'] if g else None,
                     'lcp_ms': sp['lcp_ms'], 'speed_reason': sp['reason']})
    return {'unavailable': bool(r.get('unavailable')), 'reason': r.get('reason'), 'rows': rows,
            'speed_note': rows[0]['speed_reason'] if rows and rows[0]['lcp_ms'] is None else None}


def message_match(ld):
    if ld['unavailable']:
        return {'unavailable': True, 'reason': ld['reason'], 'rows': []}
    rows = []
    for p in ld['pages']:
        m = p['match']
        rows.append({'page': p['page'], 'sessions': p['sessions'], 'conversion_rate': p['conversion_rate'], 'median': p['median'],
                     'captured': m['captured'], 'score': m['score'], 'page_records': m['page_records'],
                     'elements': [{k: e.get(k) for k in ('element', 'words', 'record', 'reach', 'status', 'page_record', 'page_says', 'elsewhere')}
                                  for e in m['elements']]})
    return {'unavailable': False, 'rows': rows,
            'rule': 'A promise element matches when a site-captured brain record for that page holds one of its words. '
                    'A page never captured reads not checked, not mismatch.'}


def proof_map(b, pdp, captured):
    """Each objection ladder rung: its proof record, where that proof lives, and whether it is on the PDP."""
    rows = []
    for rec in b.records('objection_ladders'):
        v = rec.get('value') or {}
        for rung in v.get('rungs') or []:
            ids = rung.get('proof_ids') or []
            has = bool(ids) and 'no public proof' not in (rung.get('proof') or '').lower()
            where = sorted({p for i in ids for p in audit().record_pages(b.get(i) or {})}) if has else []
            if not has:
                status = 'no proof'
            elif pdp in where:
                status = 'on the PDP'
            elif pdp not in captured:
                status = 'proof exists, PDP not captured'
            else:
                status = 'proof exists, not on the PDP'
            rows.append({'ladder': v.get('theme'), 'level': rung.get('level'), 'doubt': rung.get('doubt'),
                         'one_star': (rung.get('counts') or {}).get('one_star'), 'proof_ids': ids, 'proof_pages': where,
                         'status': status, 'record': rec['id']})
    with_proof = sum(r['status'] != 'no proof' for r in rows)
    on_pdp = sum(r['status'] == 'on the PDP' for r in rows)
    return {'pdp': pdp, 'pdp_captured': pdp in captured, 'rows': rows, 'rungs': len(rows), 'with_proof': with_proof,
            'proof_placement_coverage': round(on_pdp / len(rows), 4) if rows and pdp in captured else None,
            'coverage_reason': None if pdp in captured else 'the PDP has no page capture in the brain, so placement is unknown'}


# ---------------------------------------------------------------- tests

def sample_size(p, mde):
    """Visitors per arm for 80 percent power, 5 percent two-sided (Lehr): 16 p (1 - p) / (p mde)^2."""
    if not p or not mde:
        return None
    return math.ceil(16 * p * (1 - p) / (p * mde) ** 2)


def test_registry(db):
    doc = json.loads((HERE / 'fixtures' / 'test_registry.json').read_text(encoding='utf-8'))
    mobile = next((d for d in db.get('devices') or [] if d['device'] == 'mobile'), None)
    example = None
    if mobile:
        p = mobile['counts']['add_to_cart_rate']
        n = sample_size(p, MDE)
        daily = mobile['counts']['sessions'] / db['window']['days']
        days = math.ceil(2 * n / daily) if daily else None
        example = {'metric': 'add_to_cart_rate on mobile', 'baseline': p, 'mde': MDE, 'sample_per_arm': n,
                   'daily_sessions': round(daily), 'days_to_sample': days, 'read_after_days': max(days or 0, MIN_TEST_DAYS)}
    return dict(doc, example=example)


# ---------------------------------------------------------------- tiles, insights, chart

def tile(name, plain, unit, value, prior=None, reason=None, window=None, freshness=None):
    out = {'name': name, 'plain': plain, 'unit': unit, 'value': value, 'window': window, 'freshness': freshness}
    if value is None:
        out['unavailable_reason'] = reason
    elif prior:
        out['delta'] = round(value / prior - 1, 6)
    return out


def tiles(w, ld):
    q = {'brand': BRAND, 'window': f"{w['days']}d"}
    prior_end = (date.fromisoformat(w['ends_on']) - timedelta(days=w['days'])).isoformat()
    now, before = (M().compute('session_funnel', None, end=e, **q) for e in (w['ends_on'], prior_end))
    mob, mob0 = (M().compute('session_funnel', None, end=e, device='mobile', **q) for e in (w['ends_on'], prior_end))
    rate = lambda r: None if r.get('unavailable') else r['rates']['conversion_rate']
    label = f"{w['days']} days"
    fresh = (now.get('freshness') or {}).get('as_of')
    top = next((p for p in ld.get('pages') or [] if p['match']['captured']), None)
    return [
        tile('Conversion rate', 'GA4 purchases per session, all devices', '%', rate(now), rate(before), now.get('reason'), label, fresh),
        tile('Mobile conversion rate', 'GA4 purchases per mobile session', '%', rate(mob), rate(mob0), mob.get('reason'), label, fresh),
        tile('Message match, top paid lander', (f"Ad promises kept on the {audit().page_label(top['page'])}" if top else
                                                'No paid lander has a page capture'),
             '%', top['match']['score'] if top else None, None,
             'no paid social lander has a page capture in the brain', 'current pages', fresh),
    ]


def insights(findings):
    """2 rules, each with the sentence it produced (or a quiet line when the rule has nothing to say)."""
    mob = next((f for f in findings if f['rule_id'] == 'CRO-R07' and f['entity']['id'] == 'mobile' and f['status'] == 'open'), None)
    mis = next((f for f in findings if f['rule_id'] == 'CRO-R02' and f['status'] == 'open'), None)
    rule1 = ('CRO-R07 on mobile: each step against its own median of the 6 windows before; the break is the step '
             'with the most money; fires more than 1 percent below the median')
    rule2 = ('CRO-R02: a promise from the Ad Library records (offer, hook, giving line) is missing from a captured '
             'paid social lander; ranked by paid social sessions')
    out = []
    for name, f, rule, quiet in (('mobile break', mob, rule1, 'No mobile step sits more than 1 percent below its own median.'),
                                 ('lander mismatch', mis, rule2, 'Every captured paid social lander keeps the ad promises.')):
        if f:
            stake = (f['money_at_stake'] or {}).get('usd')
            out.append({'name': name, 'rule': rule, 'severity': 'high' if f['severity'] in ('critical', 'high') else 'medium',
                        'sentence': f['sentence'], 'capability': f['capability']['id'], 'autonomy': f['capability']['autonomy'],
                        'finding': f['id'], 'money': stake, 'confidence': f['confidence']})
        else:
            out.append({'name': name, 'rule': rule, 'severity': 'info', 'sentence': None, 'quiet': quiet})
    return out


def chart(w):
    """Conversion rate by device for 12 weeks, oldest first."""
    end = date.fromisoformat(w['ends_on'])
    weeks = [(end - timedelta(days=7 * k)).isoformat() for k in range(CHART_WEEKS - 1, -1, -1)]
    series = {}
    for i, e in enumerate(weeks):
        r = M().compute('session_funnel', None, brand=BRAND, window='7d', end=e, by='device')
        for g in ([] if r.get('unavailable') else r['groups']):
            series.setdefault(g['device'], [None] * len(weeks))[i] = g['conversion_rate']
    if not series:
        return {'unavailable': True, 'reason': 'no weekly sessions could be read', 'labels': [], 'series': []}
    order = [d for d in ('mobile', 'desktop', 'tablet') if d in series] + sorted(set(series) - {'mobile', 'desktop', 'tablet'})
    return {'unavailable': False, 'labels': weeks, 'unit': 'ratio',
            'series': [{'name': audit().DEVICE_LABEL.get(d, d), 'values': series[d]} for d in order],
            'source': 'session_funnel by device, 7-day windows ending on each date'}


# ---------------------------------------------------------------- summary

def summary(req):
    w = window_for(req.arg('window'))
    A = audit()
    data = M().resolve(None, {'brand': BRAND})
    db = A.device_breaks(BRAND, w)
    ld = A.landers(BRAND, w)
    findings = A.run(BRAND, w)
    b = A.brain(BRAND, w['ends_on'])
    captured = set(A.site_records(b))
    reg = registry(w, b, captured)
    pdp = next((r['page'] for r in reg['rows'] if r['type'] == 'PDP' and r['sessions']), None)
    return {
        'brand': data.brand, 'simulated': True, 'window': w,
        'funnel_device': funnel_by_device(db), 'funnel_source': funnel_by_source(w),
        'registry': reg, 'message_match': message_match(ld), 'proof_map': proof_map(b, pdp, captured),
        'tests': test_registry(db), 'tiles': tiles(w, ld), 'insights': insights(findings),
        'chart': chart(w), 'findings': findings, 'rules': A.RULES,
    }


def handle(req):
    route = req.path[0] if req.path else ''
    try:
        if route == 'summary' and req.method == 'GET':
            return summary(req)
        if route == 'findings' and req.method == 'GET':
            return {'findings': audit().run(BRAND, window_for(req.arg('window'))), 'rules': audit().RULES, 'simulated': True}
    except ValueError as exc:
        return 400, {'error': str(exc)}
    return 404, {'error': 'not found', 'routes': ['summary', 'findings']}
