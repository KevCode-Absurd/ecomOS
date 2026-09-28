"""The report builder for 26-reports: periods, numbers, screen findings, decisions, brain changes.

api.py and audit.py both read from here, so the page and the audit see the same report.
Every contract number comes from app/metrics.py. The one number read straight from the
data layer (new versus repeat orders, from the daily aggregate) is marked with
`metric: None`, so rule REPORT-R01 can name it. Other screens' findings come from their
own `audit.run(brand, window)`, discovered by folder and never edited; an audit that
raises is recorded as unavailable for that screen. The brain is read through
app/brain/store.py with `today` set to the report's run day, never the wall clock.
"""
import importlib.util
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parents[1]
SCREEN = '26-reports'
SEVERITY_ORDER = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
CHOICE_LABEL = {'agent': 'Let the agent do it', 'person': 'Send to a person', 'not_now': 'Not now'}
TOP_N = 10
BRAIN_ROWS_PER_SECTION = 2

# key, label, unit, contract metric (None: read from the data layer, not the contract)
LINES = (
    ('net_revenue', 'Net revenue', 'usd', 'aov'),
    ('orders', 'Orders', 'count', 'aov'),
    ('aov', 'Average order', 'usd', 'aov'),
    ('spend', 'Paid spend, Meta and Google', 'usd', 'spend'),
    ('mer', 'MER', 'x', 'mer'),
    ('period_roas', 'Paid ROAS, platform reported', 'x', 'period_roas'),
    ('contribution_margin', 'Contribution margin', 'usd', 'contribution_margin'),
    ('new_customer_share', 'Share of orders from new customers', 'ratio', None),
)
# headline fields the "moved most" and "out of band" rules read, with what drives each
HEADLINE = ('net_revenue', 'orders', 'aov', 'spend', 'mer')
DRIVERS = {'net_revenue': ('orders', 'aov'), 'mer': ('net_revenue', 'spend')}

_cache = {}


def clear_cache():
    _cache.clear()


def cached(key, build):
    if key not in _cache:
        _cache[key] = build()
    return _cache[key]


# ---------------------------------------------------------------- modules

def metrics_module():
    """The server's metrics module when loaded, else app/metrics.py loaded here."""
    mod = sys.modules.get('ecomos_metrics')
    if mod is None:
        spec = importlib.util.spec_from_file_location('ecomos_metrics', APP / 'metrics.py')
        mod = importlib.util.module_from_spec(spec)
        sys.modules['ecomos_metrics'] = mod
        spec.loader.exec_module(mod)
    return mod


def brand_data(brand):
    return metrics_module().resolve(None, {'brand': brand})


def brain_modules():
    path = str(APP / 'brain')
    if path not in sys.path:
        sys.path.insert(0, path)
    import package  # noqa: E402  app/brain/package.py
    import store  # noqa: E402  app/brain/store.py
    return store, package


# ---------------------------------------------------------------- periods

def day(iso):
    return date.fromisoformat(iso)


def period(brand, kind='week'):
    """week: the 7 days to the last full day. month: the last closed calendar month."""
    as_of = day(brand_data(brand).brand['as_of'])
    if kind == 'month':
        end = as_of if (as_of + timedelta(days=1)).day == 1 else as_of.replace(day=1) - timedelta(days=1)
        start = end.replace(day=1)
        prior_end = start - timedelta(days=1)
        prior_start = prior_end.replace(day=1)
        label = end.strftime('%B %Y')
    elif kind == 'week':
        end, start = as_of, as_of - timedelta(days=6)
        prior_end, prior_start = start - timedelta(days=1), start - timedelta(days=7)
        label = f'Week to {end.day} {end.strftime("%b %Y")}'
    else:
        raise ValueError('period must be week or month')
    return window_of(kind, start, end, prior_start, prior_end, label)


def window_of(kind, start, end, prior_start, prior_end, label=None):
    return {'kind': kind, 'label': label or f'{(end - start).days + 1} days to {end.isoformat()}',
            'start': start.isoformat(), 'end': end.isoformat(), 'days': (end - start).days + 1,
            'prior_start': prior_start.isoformat(), 'prior_end': prior_end.isoformat(),
            'prior_days': (prior_end - prior_start).days + 1,
            # decisions and brain changes are logged up to the morning the report runs
            'log_start': (start + timedelta(days=1)).isoformat(), 'log_end': (end + timedelta(days=1)).isoformat(),
            'noun': 'week' if kind == 'week' else 'month' if kind == 'month' else 'period'}


def from_audit_window(window, brand):
    """audit.run's {ends_on, days} as a report period; the prior period is the same length before it."""
    w = dict(window or {})
    end = day(w.get('ends_on') or brand_data(brand).brand['as_of'])
    days = int(w.get('days') or 7)
    start = end - timedelta(days=days - 1)
    prior_days = int(w.get('prior_days') or days)
    prior_end = start - timedelta(days=1)
    kind = 'week' if days == 7 else 'month' if start.day == 1 and (end + timedelta(days=1)).day == 1 else 'period'
    return window_of(kind, start, end, prior_end - timedelta(days=prior_days - 1), prior_end)


# ---------------------------------------------------------------- numbers

def contract(brand, end, days):
    """Contract numbers for one window, each {value, metric, unavailable, reason, fix}."""
    def build():
        M = metrics_module()
        q = {'brand': brand, 'window': f'{days}d', 'end': end}
        res = {n: M.compute(n, None, **q) for n in ('aov', 'spend', 'mer', 'period_roas', 'contribution_margin')}
        out = {}
        for key, _, _, metric in LINES:
            if metric is None:
                continue
            r = res[metric]
            if r.get('unavailable'):
                out[key] = {'value': None, 'metric': metric, 'unavailable': True, 'reason': r.get('reason'), 'fix': r.get('fix')}
                continue
            value = (r.get('inputs') or {}).get(key) if key in ('net_revenue', 'orders') else r.get('value')
            out[key] = {'value': value, 'metric': metric, 'unavailable': value is None,
                        'reason': None if value is not None else f'{metric} gave no {key}', 'fix': None}
        out['_by_channel'] = None if res['spend'].get('unavailable') else res['spend'].get('by_channel')
        out['_freshness'] = (res['aov'].get('freshness') or {}).get('as_of')
        return out
    return cached(('contract', brand, end, days), build)


def summary_sheet(brand, start, end):
    """Sums of the daily aggregate for the window: what a report reads when it skips the contract."""
    def build():
        try:
            rows = brand_data(brand).table('daily')
        except (KeyError, ValueError) as exc:
            return {'unavailable': True, 'reason': f'daily aggregate unreadable: {exc}'}
        keep = [r for r in rows if start <= r['date'] <= end]
        want = (day(end) - day(start)).days + 1
        if len(keep) < want:
            return {'unavailable': True, 'reason': f'daily aggregate has {len(keep)} of {want} days'}
        out = {'unavailable': False, 'days': len(keep)}
        for f in ('net_sales', 'orders', 'meta_spend', 'google_spend', 'new_customer_orders', 'returning_customer_orders'):
            vals = [r.get(f) for r in keep]
            out[f] = None if any(v is None for v in vals) else round(sum(vals), 2)
        return out
    return cached(('sheet', brand, start, end), build)


def new_share(sheet):
    if sheet.get('unavailable'):
        return None
    n, r = sheet.get('new_customer_orders'), sheet.get('returning_customer_orders')
    return round(n / (n + r), 6) if n is not None and r is not None and (n + r) else None


def lines(brand, p):
    """What changed: each line with this period, the period before and the change."""
    cur = contract(brand, p['end'], p['days'])
    pri = contract(brand, p['prior_end'], p['prior_days'])
    sheet = summary_sheet(brand, p['start'], p['end'])
    psheet = summary_sheet(brand, p['prior_start'], p['prior_end'])
    out = []
    for key, label, unit, metric in LINES:
        if metric is None:
            c = {'value': new_share(sheet), 'reason': sheet.get('reason')}
            b = {'value': new_share(psheet)}
            c['unavailable'] = c['value'] is None
            source = 'aggregates/daily new and returning customer orders (read directly, not a contract metric)'
        else:
            c, b = cur[key], pri[key]
            source = f'app/metrics.py {metric}'
        row = {'key': key, 'label': label, 'unit': unit, 'metric': metric, 'source': source,
               'value': None if c.get('unavailable') else c['value'],
               'prior': None if b.get('unavailable') else b.get('value'),
               'unavailable': bool(c.get('unavailable')), 'reason': c.get('reason'), 'fix': c.get('fix')}
        row['delta'] = (round(row['value'] / row['prior'] - 1, 6)
                        if row['value'] is not None and row['prior'] else None)
        out.append(row)
    return out


def channel_mix(brand, p):
    """Paid spend share by channel, this period and the one before, from the spend metric."""
    cur = contract(brand, p['end'], p['days'])['_by_channel']
    pri = contract(brand, p['prior_end'], p['prior_days'])['_by_channel']
    if not cur:
        return {'unavailable': True, 'reason': 'spend by channel unavailable', 'rows': []}
    tot, ptot = sum(cur.values()), sum((pri or {}).values())
    rows = [{'channel': ch, 'spend': round(v, 2), 'share': round(v / tot, 6) if tot else None,
             'prior_share': round(pri[ch] / ptot, 6) if pri and ptot and ch in pri else None}
            for ch, v in sorted(cur.items())]
    return {'unavailable': False, 'rows': rows, 'metric': 'spend', 'note': 'Meta and Google only; other paid channels are not in the contract spend yet.'}


def windows_back(p, n):
    """(end, days, label) for n periods back to back, newest first: 7-day weeks, or closed calendar months."""
    out = []
    end = day(p['end'])
    for _ in range(n):
        if p['kind'] == 'month':
            start = end.replace(day=1)
            out.append((end.isoformat(), (end - start).days + 1, end.strftime('%b %Y')))
            end = start - timedelta(days=1)
        else:
            out.append((end.isoformat(), p['days'], end.isoformat()))
            end = end - timedelta(days=p['days'])
    return out


def series(brand, key, p, n):
    """One headline value for n periods back to back, newest first."""
    out = []
    for end, days, _ in windows_back(p, n):
        c = contract(brand, end, days)[key]
        out.append(None if c.get('unavailable') else c['value'])
    return out


def trend_chart(brand, p, n=13):
    """Net revenue per period for the last n periods (weeks, or closed calendar months)."""
    wins = windows_back(p, n)
    values = series(brand, 'net_revenue', p, n)
    return {'unavailable': all(v is None for v in values), 'labels': [w[2] for w in wins][::-1], 'values': values[::-1],
            'unit': 'usd', 'metric': 'aov (net_revenue input)', 'kind': p['kind'],
            'source': 'app/metrics.py aov, net revenue input: line subtotal minus discounts on paid orders'}


# ---------------------------------------------------------------- other screens

def discover_audits():
    """(slug, run) for every app/screens/<nn>-<slug>/audit.py but this one. Import errors become a raising run."""
    out = []
    for path in sorted((APP / 'screens').glob('*/audit.py')):
        slug = path.parent.name
        if slug == SCREEN:
            continue
        name = 'reports_src_' + re.sub(r'\W', '_', slug)
        try:
            mod = sys.modules.get(name)
            if mod is None or getattr(mod, '__file__', None) != str(path):
                spec = importlib.util.spec_from_file_location(name, path)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                sys.modules[name] = mod
            out.append((slug, mod.run))
        except Exception as exc:  # a broken import is that screen's problem, not the report's
            def broken(brand, window, _exc=exc):
                raise _exc
            out.append((slug, broken))
    return out


def screen_findings(brand, p):
    """Every other screen's findings for the period. A screen whose audit raises is unavailable, not a crash."""
    def build():
        window = {'ends_on': p['end'], 'days': p['days'], 'trailing': 4}
        screens, findings = [], []
        for slug, run in discover_audits():
            try:
                got = run(brand, dict(window))
                if not isinstance(got, list):
                    raise TypeError(f'audit.run returned {type(got).__name__}, not a list')
            except Exception as exc:
                screens.append({'screen': slug, 'status': 'unavailable', 'findings': None,
                                'reason': f'{type(exc).__name__}: {str(exc)[:160]}'})
                continue
            screens.append({'screen': slug, 'status': 'ok', 'findings': len(got), 'reason': None})
            findings.extend(f for f in got if isinstance(f, dict))
        return {'screens': screens, 'findings': findings}
    return cached(('screens', brand, p['end'], p['days']), build)


def stake(f):
    return (f.get('money_at_stake') or {}).get('usd')


def rank_key(f):
    s = stake(f)
    return (s is None, -(s or 0), SEVERITY_ORDER.get(f.get('severity'), 9), -(f.get('confidence') or 0), str(f.get('id')))


def decision_for(f, decisions):
    rows = [d for d in decisions if d.get('card') == f.get('id')]
    if not rows:
        return {'status': 'none', 'label': 'No decision yet', 'time': None}
    d = rows[-1]
    return {'status': d.get('choice'), 'label': CHOICE_LABEL.get(d.get('choice'), d.get('choice')), 'time': d.get('time')}


def top10(findings, decisions):
    live = [f for f in findings if f.get('status') not in ('resolved', 'snoozed')]
    out = []
    for i, f in enumerate(sorted(live, key=rank_key)[:TOP_N], 1):
        out.append({'rank': i, 'id': f.get('id'), 'screen': f.get('screen'), 'rule_id': f.get('rule_id'),
                    'severity': f.get('severity'), 'status': f.get('status'), 'label': (f.get('entity') or {}).get('label'),
                    'sentence': f.get('sentence'), 'usd': stake(f), 'money_reason': f.get('money_reason'),
                    'confidence': f.get('confidence'), 'capability': f.get('capability') or {},
                    'evidence_metrics': sorted({e.get('metric') for e in f.get('evidence') or [] if e.get('metric')}),
                    'decision': decision_for(f, decisions)})
    return out


# ---------------------------------------------------------------- decisions and brain

def decisions_log(brand):
    path = APP / 'data' / 'brands' / brand / 'decisions.json'
    if not path.is_file():
        return []
    try:
        rows = json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return []
    return [r for r in rows if isinstance(r, dict)] if isinstance(rows, list) else []


def brain(brand, p):
    store, _ = brain_modules()
    return store.Brain(brand, today=day(p['log_end']))


def in_log(iso, p):
    return bool(iso) and p['log_start'] <= str(iso)[:10] <= p['log_end']


def shipped(brand, p):
    """Decisions made in the period: the screens' decisions log plus decision records in the brain."""
    out = []
    for d in decisions_log(brand):
        if in_log(d.get('time'), p):
            out.append({'date': str(d['time'])[:10], 'source': 'decisions log', 'screen': d.get('screen'),
                        'capability': d.get('capability'), 'choice': d.get('choice'),
                        'text': CHOICE_LABEL.get(d.get('choice'), d.get('choice')) + ' on ' + str(d.get('capability'))
                        + (f": {d['reason']}" if d.get('reason') else ''), 'ref': d.get('card')})
    try:
        recs = brain(brand, p).records('decisions')
    except FileNotFoundError:
        recs = []
    for r in recs:
        if in_log(r.get('date'), p):
            out.append({'date': r['date'], 'source': 'brain', 'screen': None, 'capability': None, 'choice': None,
                        'text': clip(r.get('text') or json.dumps(r.get('value'))), 'ref': r['id']})
    return sorted(out, key=lambda d: (d['date'], d['ref'] or ''))


def clip(text, n=220):
    text = ' '.join(str(text).split())
    return text if len(text) <= n else text[:n - 1].rstrip() + '...'


def brain_changes(brand, p):
    """Brain records added or changed in the period, newest section first."""
    try:
        b = brain(brand, p)
    except FileNotFoundError:
        return {'unavailable': True, 'reason': f'no brain folder for {brand}', 'rows': [], 'by_section': {}}
    rows = []
    for r in b.records():
        hist = [h for h in r.get('history') or [] if in_log(h.get('changed_at'), p)]
        if in_log(r.get('date'), p) or hist:
            rows.append({'id': r['id'], 'section': r['section'], 'date': r['date'], 'tier': r.get('tier'),
                         'changed': bool(hist), 'text': clip(r.get('text') or json.dumps(r.get('value')), 180)})
    rows.sort(key=lambda x: (x['section'], x['id']))
    by_section = {}
    for r in rows:
        by_section[r['section']] = by_section.get(r['section'], 0) + 1
    # the page lists a few per section; the counts cover every record
    shown, seen = [], {}
    for r in rows:
        seen[r['section']] = seen.get(r['section'], 0) + 1
        if seen[r['section']] <= BRAIN_ROWS_PER_SECTION:
            shown.append(r)
    return {'unavailable': False, 'rows': shown, 'total': len(rows), 'by_section': by_section, 'version': b.version()}


def open_questions(brand, p, findings):
    """The brain's unanswered questions, then the connectors that keep findings unavailable."""
    out = []
    try:
        for r in brain(brand, p).records('open_questions'):
            v = r.get('value') if isinstance(r.get('value'), dict) else {}
            if not v.get('answered_on'):
                out.append({'kind': 'brain', 'ref': r['id'], 'text': clip(v.get('question') or r.get('text'), 200),
                            'who': v.get('who_can_answer')})
    except FileNotFoundError:
        pass
    need = {}
    for f in findings:
        if f.get('status') == 'unavailable':
            conn = str(((f.get('unavailable') or {}).get('connector')) or 'unknown')
            need.setdefault(conn, set()).add(f.get('screen'))
    for conn, screens in sorted(need.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        out.append({'kind': 'connector', 'ref': conn, 'who': 'the founder',
                    'text': f'Connect {conn}: {len(screens)} screen{"s" if len(screens) != 1 else ""} cannot read their rules without it.'})
    return out


def t0_card(brand, p):
    """The brand card as of the morning after the last full day (ages are counted from then)."""
    try:
        store, package = brain_modules()
        today = day(brand_data(brand).brand['as_of']) + timedelta(days=1)
        return package.t0_card(store.Brain(brand, today=today))
    except FileNotFoundError:
        return None


# ---------------------------------------------------------------- claims

def claims(brand, p, report_lines, top):
    """Every sentence the report makes, with what it cites. REPORT-R01 reads this list."""
    out = []
    for r in report_lines:
        if r['value'] is None:
            continue
        out.append({'id': f"line.{r['key']}", 'section': 'what_changed', 'label': r['label'],
                    'metric': r['metric'], 'brain_ref': None, 'has_number': True, 'value': r['value']})
    for t in top:
        has_num = bool(re.search(r'\d', t['sentence'] or ''))
        out.append({'id': f"finding.{t['id']}", 'section': 'top10', 'label': t['label'],
                    'metric': ', '.join(t['evidence_metrics']) or None, 'brain_ref': None,
                    'has_number': has_num, 'value': t['usd'], 'status': t['status']})
    return out
