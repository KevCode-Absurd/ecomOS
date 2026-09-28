"""API for 00-today, under /api/00-today/.

  GET  summary?window=28d     pipeline stages (4 trailing windows), money at stake, 3 tiles,
                              2 insights (rules with their sentences), daily revenue for 90 days,
                              the top 10 stub and this screen's decisions
  GET  findings?window=28d    audit.run for the brand, in the audit contract shape
  GET  decisions              this brand's decisions log
  POST decisions              {capability, choice, reason, autonomy, card} appended to
                              app/data/brands/<brand>/decisions.json

Numbers come from app/metrics.py (brand=bombas reads app/data/brands/bombas/). The chart
reads the daily aggregate. Missing numbers stay null with a reason, never 0.
"""
import importlib.util
import json
import re
import sys
import threading
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parents[1]
SCREEN = '00-today'
BRAND = 'bombas'
CHART_DAYS = 90
CHOICES = ('agent', 'person', 'not_now')
AUTONOMY = ('agent_does', 'founder_gate', 'human_assist')
MAX_DECISIONS = 20_000
_lock = threading.Lock()

# stage, label, count field from the pipeline metrics
STAGE_ROWS = (
    ('sessions', 'Sessions'),
    ('product_view', 'Product view'),
    ('add_to_cart', 'Add to cart'),
    ('checkout', 'Checkout'),
    ('purchase', 'Purchase'),
)


def _load(name, path):
    mod = sys.modules.get(name)
    if mod is None or getattr(mod, '__file__', None) != str(path):
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod
        spec.loader.exec_module(mod)
    return mod


def audit():
    return _load('today_audit', HERE / 'audit.py')


def brand_data():
    return audit().metrics_module().resolve(None, {'brand': BRAND})


def decisions_path():
    return APP / 'data' / 'brands' / BRAND / 'decisions.json'


# ---------------------------------------------------------------- numbers

def stage_counts(pipe):
    """Counts per stage for each of the 4 windows, from the pipeline metrics' numerators."""
    by = {m['metric']: m['results'] for m in pipe.get('metrics', [])}
    out = []
    for i, w in enumerate(pipe.get('windows', [])):
        def num(name, key='numerator'):
            r = by.get(name, [None] * 4)[i] or {}
            return None if r.get('unavailable') else (r.get('inputs') or {}).get(key)
        sess = by.get('sessions', [{}] * 4)[i] or {}
        out.append({'window': w,
                    'sessions': None if sess.get('unavailable') else sess.get('value'),
                    'product_view': num('product_view_rate'),
                    'add_to_cart': num('add_to_cart_rate'),
                    'checkout': num('checkout_rate'),
                    'purchase': num('cvr_overall')})
    return out


def stages_view(counts, stake):
    """The 5 stages with this window's count, step rate, own median, 4 windows of counts, and the break."""
    by_stage = {s['stage']: s for s in (stake.get('stages') or [])}
    cur = counts[-1] if counts else {}
    prev_key = None
    rows = []
    for key, label in STAGE_ROWS:
        s = by_stage.get(key, {})
        rows.append({'stage': key, 'label': label, 'value': cur.get(key),
                     'windows': [c.get(key) for c in counts],
                     'rate': s.get('current'), 'median': s.get('median'), 'money': s.get('money'),
                     'from': prev_key, 'is_break': key == stake.get('break_stage')})
        prev_key = key
    return rows


def tile(result, name, plain, unit, prior=None, higher_is_better=True):
    out = {'name': name, 'plain': plain, 'unit': unit, 'value': result.get('value'),
           'window': (result.get('window') or {}).get('label'),
           'freshness': (result.get('freshness') or {}).get('as_of'), 'higher_is_better': higher_is_better}
    if result.get('unavailable'):
        out.update(unavailable_reason=result.get('reason'), fix=result.get('fix'))
    elif prior and not prior.get('unavailable') and prior.get('value'):
        out['delta'] = round(result['value'] / prior['value'] - 1, 6)
    return out


def tiles(pipe):
    by = {m['metric']: m['results'] for m in pipe.get('metrics', [])}
    def pair(name):
        r = by.get(name) or [{}] * 4
        return r[-1] or {}, r[-2] if len(r) > 1 else None
    s, s0 = pair('sessions')
    c, c0 = pair('cvr_overall')
    a, a0 = pair('aov')
    return [tile(s, 'Sessions', 'Visits to the store in the window', 'n', s0),
            tile(c, 'Conversion rate', 'Orders per session', '%', c0),
            tile(a, 'Average order', 'Net revenue per order, before tax and shipping', '$', a0)]


def insights(findings, stake):
    """2 rules, each with the sentence it produced (or null when the rule is quiet)."""
    top = next((f for f in findings if f['rule_id'] == 'TODAY-R01' and f['status'] == 'open'), None)
    trend = next((f for f in findings if f['rule_id'] == 'TODAY-R02'), None)
    out = []
    rule1 = ('highest-stake stage from money_at_stake (own median of 6 earlier windows), '
             'ranked by stake then confidence; fires when a stage is more than 1 percent below its median')
    if top:
        m = top['money_at_stake']['usd']
        out.append({'name': 'top break named', 'rule': rule1, 'severity': 'high' if top['severity'] in ('critical', 'high') else 'medium',
                    'sentence': (f"{top['entity']['label']} is costing about ${m:,} in the last {stake['window']['days']} days, "
                                 f"since {audit().day_label(top['first_seen'])}."),
                    'capability': 'PROP-C06', 'autonomy': 'agent_does', 'finding': top['id'],
                    'evidence': top['sentence']})
    else:
        out.append({'name': 'top break named', 'rule': rule1, 'severity': 'info', 'sentence': None,
                    'quiet': 'No stage sits more than 1 percent below its own median this window.'})
    rule2 = "a stage's step rate fell for 2 windows running (current < previous < the one before)"
    if trend:
        out.append({'name': 'trend alert', 'rule': rule2, 'severity': 'medium', 'sentence': trend['sentence'],
                    'capability': 'DIAG-C03', 'autonomy': 'agent_does', 'finding': trend['id']})
    else:
        out.append({'name': 'trend alert', 'rule': rule2, 'severity': 'info', 'sentence': None,
                    'quiet': 'No stage has fallen 2 windows running.'})
    return out


def revenue_chart(data, days=CHART_DAYS):
    try:
        rows = data.table('daily')
    except (KeyError, ValueError) as exc:
        return {'unavailable': True, 'reason': f'daily aggregate unreadable: {exc}', 'labels': [], 'values': []}
    end = date.fromisoformat(data.brand['as_of'])
    start = (end - timedelta(days=days - 1)).isoformat()
    keep = [r for r in rows if start <= r['date'] <= end.isoformat()]
    return {'unavailable': False, 'labels': [r['date'] for r in keep],
            'values': [r.get('net_sales') for r in keep], 'unit': 'usd',
            'source': 'aggregates/daily net_sales (line subtotal minus discounts, all orders)'}


def top10():
    doc = json.loads((HERE / 'fixtures' / 'top10_stub.json').read_text(encoding='utf-8'))
    return doc


def summary(req):
    window = req.arg('window') or '28d'
    data = brand_data()
    pipe = req.data.pipeline(window=window, brand=BRAND)
    stake = req.data.metric('money_at_stake', window=window, brand=BRAND)
    days = int(window[:-1])
    findings = audit().run(BRAND, {'ends_on': data.brand['as_of'], 'days': days, 'trailing': 4})
    counts = stage_counts(pipe)
    return {
        'brand': data.brand, 'simulated': True, 'window': window, 'windows': pipe.get('windows'),
        'stages': stages_view(counts, stake) if not stake.get('unavailable') else [],
        'money_at_stake': {k: stake.get(k) for k in ('value', 'unavailable', 'reason', 'fix', 'break_stage',
                                                       'total', 'basis', 'notes', 'window', 'inputs')},
        'tiles': tiles(pipe), 'insights': insights(findings, stake if not stake.get('unavailable') else {'window': {'days': days}}),
        'findings': findings, 'chart': revenue_chart(data), 'top10': top10(),
        'decisions': read_decisions(),
    }


# ---------------------------------------------------------------- decisions

def read_decisions():
    path = decisions_path()
    if not path.is_file():
        return []
    try:
        rows = json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return []
    return rows if isinstance(rows, list) else []


def validate(body):
    if not isinstance(body, dict):
        raise ValueError('body must be an object')
    capability = str(body.get('capability') or '').strip()
    choice = str(body.get('choice') or '')
    if not re.fullmatch(r'[A-Za-z0-9_.:-]{1,80}', capability):
        raise ValueError('capability must be a capability id')
    if choice not in CHOICES:
        raise ValueError('choice must be one of ' + ', '.join(CHOICES))
    row = {'screen': SCREEN, 'brand': BRAND, 'capability': capability, 'choice': choice,
           'reason': str(body.get('reason') or '').strip()[:300],
           'time': datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')}
    if body.get('autonomy') in AUTONOMY:
        row['autonomy'] = body['autonomy']
    card = str(body.get('card') or '')
    if re.fullmatch(r'[A-Za-z0-9_.:-]{1,120}', card):
        row['card'] = card
    return row


def append_decision(body):
    row = validate(body)
    path = decisions_path()
    with _lock:
        rows = read_decisions()
        if len(rows) >= MAX_DECISIONS:
            raise ValueError('decisions log is full')
        rows.append(row)
        tmp = path.with_suffix('.json.tmp')
        tmp.write_text(json.dumps(rows, indent=1), encoding='utf-8')
        tmp.replace(path)
    return row


# ---------------------------------------------------------------- routes

def handle(req):
    route = req.path[0] if req.path else ''
    try:
        if route == 'summary' and req.method == 'GET':
            return summary(req)
        if route == 'findings' and req.method == 'GET':
            window = req.arg('window') or '28d'
            as_of = brand_data().brand['as_of']
            return {'findings': audit().run(BRAND, {'ends_on': as_of, 'days': int(window[:-1]), 'trailing': 4}),
                    'rules': audit().RULES, 'simulated': True}
        if route == 'decisions':
            if req.method == 'POST':
                return 201, {'ok': True, 'decision': append_decision(req.body)}
            return {'decisions': read_decisions()}
    except ValueError as exc:
        return 400, {'error': str(exc)}
    return 404, {'error': 'not found', 'routes': ['summary', 'findings', 'decisions']}
