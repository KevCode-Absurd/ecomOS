"""API for 17-seo, under /api/17-seo/.

  GET  summary?window=28d     3 tiles, 2 insights (rules with their sentences), organic sessions and
                              Search Console clicks by week for 12 weeks, the query table with the CTR
                              curve, organic landing pages, the rules and the findings
  GET  findings?window=28d    audit.run for the brand, in the audit contract shape

Sessions, conversion and AOV come from app/metrics.py (session_funnel, aov) for brand=bombas.
Search Console rows are read through audit.py (no metric for them in metrics.md yet). Missing numbers
stay null with a reason, never 0. Decisions go through the shared /api/decisions log. Read-only.
"""
import importlib.util
import sys
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCREEN = '17-seo'
BRAND = 'bombas'
CHART_WEEKS = 12
PAGE_ROWS = 10


def _load(name, path):
    mod = sys.modules.get(name)
    if mod is None or getattr(mod, '__file__', None) != str(path):
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod
        spec.loader.exec_module(mod)
    return mod


def audit():
    return _load('seo_audit', HERE / 'audit.py')


def M():
    return audit().metrics_module()


def window_for(req_window):
    days = int((req_window or '28d')[:-1])
    if days < 7 or days > 91:
        raise ValueError('window must be 7d to 91d')
    as_of = M().resolve(None, {'brand': BRAND}).brand['as_of']
    return {'ends_on': as_of, 'days': days, 'trailing': 4}


def prior(w):
    return (date.fromisoformat(w['ends_on']) - timedelta(days=w['days'])).isoformat()


# ---------------------------------------------------------------- tiles

def tile(name, plain, unit, value, prior_value=None, reason=None, window=None, freshness=None):
    out = {'name': name, 'plain': plain, 'unit': unit, 'value': value, 'window': window, 'freshness': freshness}
    if value is None:
        out['unavailable_reason'] = reason
    elif prior_value:
        out['delta'] = round(value / prior_value - 1, 6)
    return out


def tiles(w):
    A = audit()
    label = f"{w['days']} days"
    org, org0 = (A.funnel(BRAND, w['days'], e, channel=A.ORGANIC) for e in (w['ends_on'], prior(w)))
    tot, tot0 = (A.funnel(BRAND, w['days'], e) for e in (w['ends_on'], prior(w)))
    fresh = (org.get('freshness') or {}).get('as_of')
    val = lambda r: None if r.get('unavailable') else r['value']
    share = lambda o, t: round(o['value'] / t['value'], 6) if not o.get('unavailable') and not t.get('unavailable') and t['value'] else None
    wins = A.sc_windows(BRAND, w)
    ctr = ctr0 = None
    if wins:
        ctr = A.ctr_by_group(BRAND, *wins[0])['non_branded']['ctr']
        if len(wins) > 1:
            ctr0 = A.ctr_by_group(BRAND, *wins[1])['non_branded']['ctr']
    return [
        tile('Organic search visits', 'GA4 sessions from unpaid search', 'n', val(org), val(org0), org.get('reason'), label, fresh),
        tile('Organic share of visits', 'Unpaid search sessions over all sessions', '%', share(org, tot), share(org0, tot0),
             org.get('reason') or tot.get('reason'), label, fresh),
        tile('Non-branded CTR', 'Search Console clicks over impressions, queries without the brand name', '%', ctr, ctr0,
             'Search Console is not connected or does not cover this window', label, w['ends_on'] if wins else None),
    ]


# ---------------------------------------------------------------- insights

RULE_TEXT = {
    'SEO-R02': ('SEO-R02: a query in the top 20 percent by impressions whose CTR sits 30 percent or more under the '
                'CTR curve for its position (branded curve twice the non-branded one)'),
    'SEO-R01': 'SEO-R01: Organic Search sessions in the last 7 days fall 15 percent or more against the 7 days before',
}
QUIET = {'SEO-R02': 'Every high impression query gets the CTR its position earns.',
         'SEO-R01': 'Organic visits held within 15 percent of last week.'}


def insights(findings):
    out = []
    for rule, name in (('SEO-R02', 'CTR under its position'), ('SEO-R01', 'organic drop')):
        f = next((x for x in findings if x['rule_id'] == rule and x['status'] == 'open'), None)
        if f:
            out.append({'name': name, 'rule': RULE_TEXT[rule], 'severity': 'high' if f['severity'] in ('critical', 'high') else 'medium',
                        'sentence': f['sentence'], 'capability': f['capability']['id'], 'autonomy': f['capability']['autonomy'],
                        'finding': f['id'], 'money': (f['money_at_stake'] or {}).get('usd'), 'confidence': f['confidence']})
        else:
            out.append({'name': name, 'rule': RULE_TEXT[rule], 'severity': 'info', 'sentence': None, 'quiet': QUIET[rule]})
    return out


# ---------------------------------------------------------------- chart and tables

def chart(w):
    """Organic sessions (GA4) and Search Console clicks by week, 12 weeks, oldest first."""
    A = audit()
    end = date.fromisoformat(w['ends_on'])
    weeks = [(end - timedelta(days=7 * k)).isoformat() for k in range(CHART_WEEKS - 1, -1, -1)]
    span = A.sc_span(BRAND)
    sessions, clicks = [], []
    for e in weeks:
        r = A.funnel(BRAND, 7, e, channel=A.ORGANIC)
        sessions.append(None if r.get('unavailable') else r['value'])
        s = (date.fromisoformat(e) - timedelta(days=6)).isoformat()
        if span and s >= span['first'] and e <= span['last']:
            clicks.append(sum(x['clicks'] for x in A.sc_rows(BRAND, s, e)))
        else:
            clicks.append(None)
    if all(v is None for v in sessions + clicks):
        return {'unavailable': True, 'reason': 'no weekly organic data could be read', 'labels': [], 'series': []}
    return {'unavailable': False, 'labels': weeks, 'unit': 'count',
            'series': [{'name': 'Organic sessions (GA4)', 'values': sessions},
                       {'name': 'Search clicks (Search Console)', 'values': clicks}],
            'source': 'session_funnel channel=Organic Search and search_console, 7 days ending on each date'}


def queries(w):
    A = audit()
    wins = A.sc_windows(BRAND, w)
    if not wins:
        return {'unavailable': True, 'reason': 'Search Console is not connected', 'fix': 'Google Search Console', 'rows': []}
    rows = []
    for r in sorted(A.sc_rows(BRAND, *wins[0]), key=lambda r: -r['impressions']):
        exp = A.curve_ctr(r['position'], r['branded'])
        rows.append(dict(r, expected_ctr=round(exp, 4), gap=round(r['ctr'] / exp - 1, 4)))
    return {'unavailable': False, 'rows': rows, 'start': wins[0][0], 'end': wins[0][1]}


def landing_pages(w):
    A = audit()
    r = A.funnel(BRAND, w['days'], w['ends_on'], channel=A.ORGANIC, by='landing_page')
    if r.get('unavailable'):
        return {'unavailable': True, 'reason': r.get('reason'), 'rows': []}
    return {'unavailable': False, 'rows': [{k: g[k] for k in ('landing_page', 'sessions', 'add_to_cart_rate', 'conversion_rate')}
                                           for g in r['groups'][:PAGE_ROWS]]}


# ---------------------------------------------------------------- summary

def summary(req):
    w = window_for(req.arg('window'))
    A = audit()
    findings = A.run(BRAND, w)
    return {
        'brand': M().resolve(None, {'brand': BRAND}).brand, 'simulated': True, 'window': w,
        'tiles': tiles(w), 'insights': insights(findings), 'chart': chart(w),
        'queries': queries(w), 'landing_pages': landing_pages(w),
        'findings': findings, 'rules': A.RULES,
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
