"""Team and ops audit (screen 23, round 0). Findings in the shape of app/contracts/audit.md.

Team and ops has few platform tables. What exists: `tickets` (volume, channel, resolution time, a workload signal),
`orders` (the volume the team handles), `ad_rows` and `content_posts` (creative output cadence), the brain through
app/brain/store.py (team, operations, decisions, calendar, documents) and `finance_inputs.json` (headcount, app and
agency cost lines). Order totals for scaling come from app/metrics.py (aov). Ticket and order counts are read from
data.sqlite with GROUP BY queries, both from the same file so ratios hold at any data scale. No connector, no model
call. Same tables, brain and window give the same findings.

Rules. TEAM-R01 to TEAM-R08 are the room spec's insights, in its order ("Team and ops" in agents/rooms/rooms.json).
A rule whose inputs are not connected emits one `unavailable` finding at the severity the spec gives it.
  TEAM-R01  SOP gap. A core role has no SOP, or its SOP is over 6 months old. Needs sop_register (brain documents
            tagged as SOPs, uploaded by the founder). MONEY-C33, medium.
  TEAM-R02  Hiring trigger crossed. A silo past its hiring trigger for over 4 weeks with no open req. Needs
            hiring_triggers; the brain holds open roles from job posts but no trigger. MONEY-C31, high.
  TEAM-R03  Vendor SLA breach. vendor_sla_hit_rate under 90 percent for a vendor in the month. Needs vendor_sla;
            the brain names the 3PL network and agencies but no written SLA. MONEY-C36, high.
  TEAM-R04  Decision log gap. No decision logged in a period the weekly review was held. Needs meeting_log.
            LOOP-C10, medium.
  TEAM-R05  CS cost drift. cs_cost_per_ticket over 115 percent of its trailing 90-day average. Needs a care cost
            per period; finance_inputs holds headcount for the whole company, not the care team. MONEY-C38, medium.
  TEAM-R06  Tooling misfit. tooling_spend_pct_revenue over 125 percent of the brand's stage plan. Tool costs are in
            finance_inputs (app_fees); the stage plan is not in the brain. MONEY-C39, medium.
  TEAM-R07  Offboarding gap. An exited employee with access still active past the same day. Needs hr_records.
            MONEY-C69, critical.
  TEAM-R08  SaaS renewal window closing. Auto-renew inside 30 days with no usage review. Needs saas_contracts with
            renewal dates. MONEY-C78, medium.
Rules from the round 0 brief (cadence and capacity), read on the brand as a whole:
  TEAM-R09  Peak-month support load. In each of the last 2 seasons the busiest full month had over PEAK_RATIO
            times the tickets of that year's median month, and the same calendar month starts within
            PEAK_LOOKAHEAD days. Team signal: open roles in the brain that name customer care. Money: null until
            finance_inputs carries a care cost per ticket. MONEY-C38.
  TEAM-R10  Resolution time drift. Median minutes to resolve, 28 days, over DRIFT times the own median of the 4
            windows before (cs_resolution_time). Money: null, same reason. MONEY-C38.
  TEAM-R11  Decision log incomplete. Founder decisions in the brain without an owner, a metric and a review date
            (decision_log_completeness under 100 percent). Money: null, a decision with no metric has no outcome to
            price. LOOP-C10.
  TEAM-R12  Decision backlog. Rows in app/data/decisions.json sent to a person more than BACKLOG_DAYS days before
            the window end, with no later choice on the same screen and capability. MONEY-C35.
Owner of every rule: 23-team-ops.

Windows: 28 days ending on the brand's last full day, plus 4 trailing 28-day windows. Months: full calendar months
the tickets table covers. Scale: data.sqlite may hold a sample (dev builds run at 0.1); counts quoted at full size
are scaled by paid orders in the daily aggregate over paid orders in data.sqlite, same 28 days.
"""
import importlib.util
import json
import statistics
import sys
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parents[1]
SCREEN = '23-team-ops'
WINDOW = 28
TRAILING = 4
PEAK_RATIO = 1.5        # round 0: the busiest month over 1.5 times the median month
PEAK_LOOKAHEAD = 90     # days: the peak month starts within this many days of the window end
DRIFT = 1.15            # room spec: 15 percent over the trailing average
BACKLOG_DAYS = 7
SOP_MAX_AGE_DAYS = 183  # room spec: an SOP over 6 months old is not current
CARE_WORDS = ('customer care', 'customer experience', 'customer service', 'support', 'care ', 'cx ')
PAID = ('paid', 'partially_refunded', 'refunded')
PAID_SQL = ', '.join(f"'{s}'" for s in PAID)
DECISIONS = APP / 'data' / 'decisions.json'
SEVERITY_ORDER = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
MONTH_NAMES = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
               'November', 'December']

AUTONOMY = {'MONEY-C31': 'human_assist', 'MONEY-C33': 'human_assist', 'MONEY-C35': 'human_assist',
            'MONEY-C36': 'human_assist', 'MONEY-C38': 'human_assist', 'MONEY-C39': 'human_assist',
            'MONEY-C69': 'founder_gate', 'MONEY-C78': 'founder_gate', 'LOOP-C10': 'agent_does'}


def _r(rule_id, name, entity_type, inputs, capability):
    return {'rule_id': rule_id, 'name': name, 'entity_type': entity_type, 'inputs': inputs, 'capability': capability,
            'owner_screen': SCREEN}


RULES = [
    _r('TEAM-R01', 'SOP gap', 'metric', ['sop_register', 'brain.documents'], 'MONEY-C33'),
    _r('TEAM-R02', 'Hiring trigger crossed', 'metric', ['hiring_triggers', 'brain.team'], 'MONEY-C31'),
    _r('TEAM-R03', 'Vendor SLA breach', 'metric', ['vendor_sla'], 'MONEY-C36'),
    _r('TEAM-R04', 'Decision log gap', 'metric', ['decision_log', 'meeting_log'], 'LOOP-C10'),
    _r('TEAM-R05', 'CS cost drift', 'metric', ['tickets', 'finance_inputs.care_cost'], 'MONEY-C38'),
    _r('TEAM-R06', 'Tooling misfit', 'metric', ['finance_inputs.app_fees', 'brain.stage_tooling_plan'], 'MONEY-C39'),
    _r('TEAM-R07', 'Offboarding gap', 'metric', ['hr_records'], 'MONEY-C69'),
    _r('TEAM-R08', 'SaaS renewal window closing', 'metric', ['saas_contracts'], 'MONEY-C78'),
    _r('TEAM-R09', 'Peak-month support load', 'metric', ['tickets', 'orders', 'brain.team'], 'MONEY-C38'),
    _r('TEAM-R10', 'Resolution time drift', 'metric', ['tickets'], 'MONEY-C38'),
    _r('TEAM-R11', 'Decision log incomplete', 'metric', ['brain.decisions'], 'LOOP-C10'),
    _r('TEAM-R12', 'Decision backlog', 'metric', ['app/data/decisions.json'], 'MONEY-C35'),
]

# Spec rules whose inputs no connector fills yet: (rule, severity, entity id, label, sentence, connector, fix, refs).
NOT_CONNECTED = [
    ('TEAM-R02', 'high', 'hiring_trigger', 'Hiring triggers by team',
     'No team has a written hiring trigger, so nobody can see when a team crossed it or how long a hire took.',
     'hiring trigger log (manual) against finance data',
     'Write one trigger metric and threshold per team, then log the date it is crossed.', ('team.hiring_role',)),
    ('TEAM-R03', 'high', 'vendor_sla', 'Vendor and 3PL SLAs',
     'No written SLA is on file for the 3PLs or agencies, so missed targets cannot be counted.',
     'vendor SLA sheet plus 3PL and agency monthly reports',
     'Enter each vendor SLA metric and target, then the monthly actual from its report.',
     ('operations.fulfillment_fact.1', 'operations.fulfillment_fact.2', 'team.outside_agency')),
    ('TEAM-R04', 'medium', 'decision_log_vs_review', 'Decisions logged in weeks with a review',
     'Meetings are not logged, so a weekly review with no decision logged cannot be seen.',
     'calendar export plus a meeting log', 'Log each weekly trading review with the date and whether it was held.', ()),
    ('TEAM-R05', 'medium', 'cs_cost_per_ticket', 'Care cost per ticket',
     'Care team cost is not split out of company headcount, so cost per ticket cannot be read.',
     'finance_inputs care cost (payroll split or outsourced care invoices)',
     'Add a monthly care team cost to finance_inputs, split from headcount.', ()),
    ('TEAM-R06', 'medium', 'tooling_vs_stage_plan', 'Software spend against the stage plan',
     'Software costs are known but there is no stage plan to judge them against.',
     'stage tooling plan in the brain', 'Write a software budget as a share of revenue for this revenue stage.', ()),
    ('TEAM-R07', 'critical', 'offboarding', 'Access removed on exit',
     'Exits are not logged, so an account left open after someone leaves cannot be seen.',
     'HR system export (exits, access revoked, checklist)',
     'Export exits with exit date, access revoked date and checklist status.', ()),
    ('TEAM-R08', 'medium', 'saas_renewals', 'Software renewals in the next 60 days',
     'No renewal dates are on file, so a tool can auto-renew before anyone reviews its use.',
     'billing exports with renewal dates', 'Add renewal date, auto-renew and last 90 days of use per tool.', ()),
]

_MODS = {}


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def metrics():
    if 'metrics' not in _MODS:
        _MODS['metrics'] = _load('ecomos_metrics_team_ops', APP / 'metrics.py')
    return _MODS['metrics']


def brand_data(brand):
    if 'tables' not in _MODS:
        _MODS['tables'] = _load('ecomos_tables_team_ops', APP / 'data' / 'tables.py')
    return _MODS['tables'].brand_data(brand)


def brain(brand):
    """The brand's brain, or None when the brand has no brain folder."""
    if not brand or not (APP / 'brain' / brand).is_dir():
        return None
    if 'store' not in _MODS:
        path = str(APP / 'brain')
        if path not in sys.path:
            sys.path.insert(0, path)  # store.py imports validate.py by name
        _MODS['store'] = _load('ecomos_brain_store_team_ops', APP / 'brain' / 'store.py')
    return _MODS['store'].Brain(brand)


def last_full_day(data, brand):
    source = brand_data(brand) if brand else data
    return date.fromisoformat(source.brand['as_of'])


class Reader:
    """One brand, one window end. m() is metrics.compute with the brand filled in; sql() reads data.sqlite and
    returns None when it is absent, so every number reads unavailable, never 0."""

    def __init__(self, data, brand, ends_on):
        self.data, self.brand, self.ends_on = data, brand, ends_on
        self.source = brand_data(brand) if brand else data
        self._brain = brain(brand)
        self._memo = {}

    def m(self, name, days=WINDOW, end=None, **kw):
        q = {'window': f'{days}d', 'end': (end or self.ends_on).isoformat(), **kw}
        if self.brand:
            q['brand'] = self.brand
        key = (name, tuple(sorted(q.items())))
        if key not in self._memo:
            self._memo[key] = metrics().compute(name, self.data, **q)
        return self._memo[key]

    def sql(self, query):
        fn = getattr(self.source, '_sql', None)
        if fn is None:
            return None
        try:
            return fn(query)
        except KeyError:
            return None
        except Exception as exc:  # a table missing from data.sqlite
            if 'no such table' in str(exc):
                return None
            raise

    def records(self, section):
        return self._brain.records(section) if self._brain else []

    def documents(self):
        return self._brain.documents() if self._brain else []

    def windows(self):
        """The current 28-day window and the 4 before it, newest first, as (start, end) days."""
        return [(self.ends_on - timedelta(days=WINDOW * k + WINDOW - 1), self.ends_on - timedelta(days=WINDOW * k))
                for k in range(TRAILING + 1)]


# ---------------------------------------------------------------- numbers (shared with api.py)

def _month_end(ym):
    y, m = int(ym[:4]), int(ym[5:7])
    return date(y + (m == 12), m % 12 + 1, 1) - timedelta(days=1)


def monthly(rd):
    """Full calendar months the tickets table covers, oldest first: tickets, paid orders, median resolve minutes.
    None when data.sqlite or the tickets table is absent."""
    if 'monthly' in rd._memo:
        return rd._memo['monthly']
    t = rd.sql("SELECT substr(created_at, 1, 7) AS month, COUNT(*) AS n, MIN(substr(created_at, 1, 10)) AS first "
               "FROM tickets GROUP BY month ORDER BY month")
    o = rd.sql(f"SELECT substr(created_at, 1, 7) AS month, COUNT(*) AS n FROM orders WHERE status IN ({PAID_SQL}) "
               f"GROUP BY month")
    out = None
    if t and o is not None:
        span = rd.sql("SELECT MIN(substr(created_at, 1, 10)) AS first FROM tickets")[0]['first']
        orders = {r['month']: r['n'] for r in o}
        out = [{'month': r['month'], 'tickets': r['n'], 'paid_orders': orders.get(r['month']),
                'per_100_orders': round(r['n'] / orders[r['month']] * 100, 3) if orders.get(r['month']) else None}
               for r in t if r['month'] + '-01' >= span and _month_end(r['month']) <= rd.ends_on]
    rd._memo['monthly'] = out
    return out


def ticket_windows(rd):
    """Per 28-day window, newest first: tickets, paid orders, median resolve and first reply minutes. None when
    data.sqlite or the tickets table is absent; a window the table does not cover is None."""
    if 'windows' in rd._memo:
        return rd._memo['windows']
    wins = rd.windows()
    first, last = wins[-1][0].isoformat(), wins[0][1].isoformat()
    rows = rd.sql(f"SELECT substr(created_at, 1, 10) AS day, resolved_min AS rm, first_response_min AS fr FROM tickets "
                  f"WHERE substr(created_at, 1, 10) BETWEEN '{first}' AND '{last}'")
    span = rd.sql("SELECT MIN(substr(created_at, 1, 10)) AS first, MAX(substr(created_at, 1, 10)) AS last FROM tickets")
    orders = rd.sql(f"SELECT substr(created_at, 1, 10) AS day, COUNT(*) AS n FROM orders WHERE status IN ({PAID_SQL}) "
                    f"AND substr(created_at, 1, 10) BETWEEN '{first}' AND '{last}' GROUP BY day")
    out = None
    if rows is not None and orders is not None and span and span[0]['first']:
        out = []
        by_day = {r['day']: r['n'] for r in orders}
        for s, e in wins:
            s_, e_ = s.isoformat(), e.isoformat()
            if span[0]['first'] > s_ or span[0]['last'] < e_:
                out.append(None)
                continue
            w = [r for r in rows if s_ <= r['day'] <= e_]
            rm = [r['rm'] for r in w if r['rm'] is not None]
            fr = [r['fr'] for r in w if r['fr'] is not None]
            out.append({'start': s_, 'end': e_, 'tickets': len(w),
                        'paid_orders': sum(n for d, n in by_day.items() if s_ <= d <= e_),
                        'resolve_median': statistics.median(rm) if rm else None,
                        'reply_median': statistics.median(fr) if fr else None})
    rd._memo['windows'] = out
    return out


def scale(rd, w):
    """Paid orders in the daily aggregate over paid orders in data.sqlite, same window. 1.0 for a live store."""
    aov = rd.m('aov', WINDOW)
    if aov.get('unavailable') or not w or not w['paid_orders']:
        return None
    return round(aov['inputs']['orders'] / w['paid_orders'], 4)


def seasons(rows):
    """The last 2 twelve-month spans of full months, newest first: peak month, median month and their ratio."""
    out = []
    end = len(rows)
    for _ in range(2):
        span = rows[max(0, end - 12):end]
        if len(span) < 6:
            break
        med = statistics.median(r['tickets'] for r in span)
        peak = max(span, key=lambda r: (r['tickets'], r['month']))
        out.append({'from': span[0]['month'], 'to': span[-1]['month'], 'peak_month': peak['month'],
                    'peak_tickets': peak['tickets'], 'median_tickets': med,
                    'ratio': round(peak['tickets'] / med, 4) if med else None,
                    'peak_per_100': peak['per_100_orders'],
                    'median_per_100': statistics.median(r['per_100_orders'] for r in span if r['per_100_orders'] is not None)})
        end -= 12
    return out


def next_start(ends_on, month_num):
    """The first day of the next occurrence of a calendar month after ends_on."""
    y = ends_on.year if month_num > ends_on.month else ends_on.year + 1
    return date(y, month_num, 1)


def open_roles(rd):
    """Open roles from job posts in the brain: all of them, and the ones that name customer care."""
    roles = [r for r in rd.records('team') if r.get('field') == 'hiring_role']
    care = [r for r in roles if any(w in (r.get('text') or '').lower() + ' ' for w in CARE_WORDS)]
    return roles, care


def decision_records(rd):
    """Founder decisions in the brain and whether each carries an owner, a metric and a review date."""
    out = []
    for r in rd.records('decisions'):
        v = r.get('value') if isinstance(r.get('value'), dict) else {}
        owner = r.get('owner') or v.get('owner') or r.get('added_by')
        metric = r.get('metric') or v.get('metric')
        review = r.get('review_date') or v.get('review_date')
        out.append({'id': r['id'], 'text': r.get('text'), 'date': (r.get('source') or {}).get('captured_at'),
                    'owner': owner, 'metric': metric, 'review_date': review,
                    'complete': bool(owner and metric and review)})
    return out


def sop_documents(rd):
    """Brain documents the founder tagged as SOPs. An empty list means none were uploaded."""
    return [d for d in rd.documents() if 'sop' in str(d.get('kind') or d.get('type') or '').lower()
            or 'sop' in [str(t).lower() for t in d.get('tags') or []]]


def decision_log():
    """The action-button log, or None when app/data/decisions.json does not exist yet."""
    if not DECISIONS.exists():
        return None
    try:
        rows = json.loads(DECISIONS.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return None
    return rows if isinstance(rows, list) else rows.get('decisions') if isinstance(rows, dict) else None


def cadence(rd):
    """Creative output per 28-day window, newest first: Meta ads first seen, and organic posts. A window a table
    does not cover is None."""
    wins = rd.windows()
    first, last = wins[-1][0].isoformat(), wins[0][1].isoformat()
    ads = rd.sql(f"SELECT d, COUNT(*) AS n FROM (SELECT ad_id, MIN(date) AS d FROM ad_rows GROUP BY ad_id) "
                 f"WHERE d BETWEEN '{first}' AND '{last}' GROUP BY d")
    ad_span = rd.sql("SELECT MIN(date) AS first FROM ad_rows")
    posts = rd.sql(f"SELECT date AS d, COUNT(*) AS n FROM content_posts WHERE date BETWEEN '{first}' AND '{last}' GROUP BY d")
    post_span = rd.sql("SELECT MIN(date) AS first FROM content_posts")
    out = []
    for s, e in wins:
        s_, e_ = s.isoformat(), e.isoformat()

        def count(rows, span):
            if rows is None or not span or not span[0]['first'] or span[0]['first'] > s_:
                return None
            return sum(r['n'] for r in rows if s_ <= r['d'] <= e_)
        out.append({'start': s_, 'end': e_, 'new_ads': count(ads, ad_span), 'posts': count(posts, post_span)})
    return out


def finance_rows(rd):
    """finance_inputs rows: the data layer table, else finance_inputs.json beside the brand's aggregates, else None."""
    if 'finance' not in rd._memo:
        rows = None
        try:
            rows = rd.source.table('finance_inputs')
        except Exception:
            path = getattr(rd.source, 'folder', None)
            if path is not None and (Path(path) / 'finance_inputs.json').is_file():
                rows = json.loads((Path(path) / 'finance_inputs.json').read_text(encoding='utf-8')).get('rows')
        rd._memo['finance'] = rows
    return rd._memo['finance']


def cost_lines(rd, field):
    """Monthly usd rows of one finance_inputs field in force on the window end."""
    end = rd.ends_on.isoformat()
    return [r for r in finance_rows(rd) or [] if r.get('field') == field and r.get('unit') == 'usd_per_month'
            and (r.get('effective_from') or '') <= end and (r.get('effective_to') or '9999') >= end]


def tool_costs(rd):
    """Monthly app fees from finance_inputs in force on the window end, or None."""
    f = finance_rows(rd)
    if f is None:
        return None
    end = rd.ends_on.isoformat()
    rows = [r for r in f or [] if r.get('field') == 'app_fees' and r.get('unit') == 'usd_per_month'
            and (r.get('effective_from') or '') <= end and (r.get('effective_to') or '9999') >= end]
    return sorted(({'tool': r.get('scope_key'), 'usd_per_month': r['value']} for r in rows),
                  key=lambda x: (-x['usd_per_month'], x['tool'])) or None


# ---------------------------------------------------------------- finding helpers

def _ev(metric, value, unit, ends_on, baseline=None, baseline_kind=None, window='28d', source='tickets'):
    return {'metric': metric, 'value': value, 'unit': unit, 'window': window, 'ends_on': ends_on.isoformat(),
            'freshness_days': 1, 'baseline': baseline, 'baseline_kind': baseline_kind, 'source': source,
            'simulated': True}


def _confidence(agree):
    """Contract section 2: 0.9 when 4 trailing windows agree, 0.7 for 2 to 3, 0.5 for 1."""
    return 0.9 if agree >= 4 else 0.7 if agree >= 2 else 0.5


def _cap(rule_id):
    return next(r['capability'] for r in RULES if r['rule_id'] == rule_id)


def _finding(rule_id, entity, severity, evidence, sentence, money, confidence, brain_refs, ends_on,
             status='open', unavailable=None, money_reason=None):
    cap = _cap(rule_id)
    f = {'id': f'{SCREEN}.{rule_id}.{entity["id"]}', 'screen': SCREEN, 'rule_id': rule_id, 'severity': severity,
         'entity': entity, 'evidence': evidence, 'sentence': sentence,
         'capability': {'id': cap, 'autonomy': AUTONOMY[cap]},
         'money_at_stake': money, 'confidence': confidence, 'brain_refs': brain_refs,
         'first_seen': ends_on.isoformat(), 'last_seen': ends_on.isoformat(), 'status': status,
         'unavailable': unavailable}
    if money is None:
        f['money_reason'] = money_reason or 'no baseline'
    return f


def _unavailable(rd, rule_id, severity, entity_id, label, sentence, connector, fix, refs=()):
    inputs = next(r['inputs'] for r in RULES if r['rule_id'] == rule_id)
    return _finding(rule_id, {'type': 'metric', 'id': entity_id, 'label': label}, severity, [], sentence, None, 0.1,
                    list(refs), rd.ends_on, status='unavailable',
                    unavailable={'inputs': inputs, 'connector': connector, 'fix': fix},
                    money_reason='inputs not connected')


def _refs(rd, prefixes):
    """Brain ids that start with any of the given `<section>.<field>` prefixes."""
    out = []
    for p in prefixes:
        for r in rd.records(p.split('.')[0]):
            rid = r['id'][len(rd.brand) + 1:] if rd.brand else r['id']
            if rid == p or rid.startswith(p + '.'):
                out.append(r['id'])
    return out


def _month_label(ym):
    return f'{MONTH_NAMES[int(ym[5:7]) - 1]} {ym[:4]}'


NO_TICKETS = 'the ticket table or the order table is not connected'
TICKET_CONNECTOR = 'helpdesk export (Gorgias or equivalent)'


# ---------------------------------------------------------------- rules

def rule_not_connected(rd):
    return [_unavailable(rd, rid, sev, eid, label, s, conn, fix, _refs(rd, refs))
            for rid, sev, eid, label, s, conn, fix, refs in NOT_CONNECTED]


def rule_sop(rd):
    docs = sop_documents(rd)
    if not docs:
        return [_unavailable(rd, 'TEAM-R01', 'medium', 'sop_coverage', 'SOP coverage by role',
                             'No SOPs are on file, so nobody can tell if a new hire could do a job from what is written down.',
                             'brain documents (founder uploads)',
                             'Upload each role SOP to the brain with its owner and last review date.',
                             _refs(rd, ['team.team_shape']))]
    out = []
    for d in docs:
        reviewed = d.get('last_reviewed') or d.get('date')
        if not reviewed:
            continue
        age = (rd.ends_on - date.fromisoformat(str(reviewed)[:10])).days
        if age <= SOP_MAX_AGE_DAYS:
            continue
        role = d.get('role') or d.get('title') or d.get('id')
        ev = [_ev('sop_age_days', age, 'days', rd.ends_on, baseline=SOP_MAX_AGE_DAYS, baseline_kind='threshold',
                  window='per document', source='brain.documents')]
        out.append(_finding('TEAM-R01', {'type': 'metric', 'id': f'sop.{d.get("id") or role}', 'label': f'SOP for {role}'},
                            'medium', ev, f'{role} has no current written SOP. The last review was {age} days ago.',
                            None, 0.5, [], rd.ends_on, money_reason='no link from an SOP to a lost order yet'))
    return out


def rule_peak(rd):
    rows = monthly(rd)
    if not rows:
        return [_unavailable(rd, 'TEAM-R09', 'high', 'peak_ticket_load', 'Peak-month support load',
                             f'Peak-month load cannot be read: {NO_TICKETS}.', TICKET_CONNECTOR,
                             'Connect the helpdesk export with a created date per ticket.')]
    ss = seasons(rows)
    if not ss or ss[0]['ratio'] is None or ss[0]['ratio'] <= PEAK_RATIO:
        return []
    peak_m = int(ss[0]['peak_month'][5:7])
    starts = next_start(rd.ends_on, peak_m)
    days = (starts - rd.ends_on).days
    if days > PEAK_LOOKAHEAD:
        return []
    agree = sum(1 for s in ss if s['ratio'] and s['ratio'] > PEAK_RATIO and int(s['peak_month'][5:7]) == peak_m)
    ws = ticket_windows(rd)
    sc = scale(rd, ws[0] if ws else None)
    roles, care = open_roles(rd)
    ev = []
    for s in ss:
        w = f'{s["from"]} to {s["to"]}'
        ev.append(_ev('peak_month_tickets_ratio', s['ratio'], 'x', rd.ends_on, baseline=PEAK_RATIO,
                      baseline_kind='threshold', window=w, source='tickets'))
        ev.append(_ev('peak_month_tickets_per_100_orders', s['peak_per_100'], 'per 100 orders', rd.ends_on,
                      baseline=round(s['median_per_100'], 3), baseline_kind='own_median', window=s['peak_month'],
                      source='tickets, orders'))
    if sc is not None:
        ev.append(_ev('peak_month_tickets_full_scale', round(ss[0]['peak_tickets'] * sc), 'count', rd.ends_on,
                      baseline=round(ss[0]['median_tickets'] * sc), baseline_kind='own_median', window=ss[0]['peak_month'],
                      source='tickets x scale'))
    ev.append(_ev('days_to_next_peak_month', days, 'days', rd.ends_on, baseline=PEAK_LOOKAHEAD, baseline_kind='threshold',
                  window='forward', source='calendar'))
    ev.append(_ev('open_roles_in_customer_care', len(care), 'count', rd.ends_on, baseline=len(roles),
                  baseline_kind='threshold', window='job posts', source='brain.team'))
    name = MONTH_NAMES[peak_m - 1]
    prior = f' and {ss[1]["ratio"]:.1f} times in {ss[1]["peak_month"][:4]}' if len(ss) > 1 and ss[1]['ratio'] else ''
    s = (f'{name} tickets ran {ss[0]["ratio"]:.1f} times a normal month in {ss[0]["peak_month"][:4]}{prior}. '
         f'The next {name} starts in {days} days and {len(care)} of {len(roles)} open roles are in customer care.')
    return [_finding('TEAM-R09', {'type': 'metric', 'id': 'peak_ticket_load', 'label': f'{name} support load'},
                     'high' if agree >= 2 else 'medium', ev, s, None, _confidence(agree),
                     [r['id'] for r in roles], rd.ends_on,
                     money_reason='no care cost per ticket in finance_inputs; headcount is not split by team')]


def rule_resolution(rd):
    ws = ticket_windows(rd)
    if not ws or ws[0] is None:
        return [_unavailable(rd, 'TEAM-R10', 'medium', 'cs_resolution_time', 'Resolution time',
                             f'Resolution time cannot be read: {NO_TICKETS}.', TICKET_CONNECTOR,
                             'Connect the helpdesk export with resolved time per ticket.')]
    now = ws[0]['resolve_median']
    prev = [w['resolve_median'] for w in ws[1:] if w and w['resolve_median'] is not None]
    if now is None or len(prev) < TRAILING:
        return []
    med = statistics.median(prev)
    if now <= med * DRIFT:
        return []
    agree = 1 + sum(1 for w in ws[1:3] if w and w['resolve_median'] and w['resolve_median'] > med * DRIFT)
    ev = [_ev('cs_resolution_time', now, 'minutes', rd.ends_on, baseline=med, baseline_kind='own_median')]
    s = (f'Tickets took {now / 60:.1f} hours to resolve at the median over 28 days. '
         f'The 4 windows before ran {med / 60:.1f} hours.')
    return [_finding('TEAM-R10', {'type': 'metric', 'id': 'cs_resolution_time', 'label': 'Resolution time'},
                     'high' if agree >= 2 else 'medium', ev, s, None, _confidence(agree), [], rd.ends_on,
                     money_reason='no link from resolution time to a lost order yet')]


def rule_decision_log(rd):
    recs = decision_records(rd)
    if rd._brain is None:
        return [_unavailable(rd, 'TEAM-R11', 'medium', 'decision_log_completeness', 'Decision log',
                             'The brand has no brain, so founder decisions cannot be read.', 'brand brain',
                             'Start the brain and log each founder decision with an owner, metric and review date.')]
    if not recs:
        return []
    done = sum(1 for r in recs if r['complete'])
    rate = round(done / len(recs), 4)
    if rate >= 1:
        return []
    miss = [r for r in recs if not r['complete']]
    no_metric = sum(1 for r in miss if not r['metric'])
    no_review = sum(1 for r in miss if not r['review_date'])
    ev = [_ev('decision_log_completeness', rate, 'ratio', rd.ends_on, baseline=1.0, baseline_kind='threshold',
              window='all logged', source='brain.decisions'),
          _ev('decisions_without_metric', no_metric, 'count', rd.ends_on, window='all logged', source='brain.decisions'),
          _ev('decisions_without_review_date', no_review, 'count', rd.ends_on, window='all logged',
              source='brain.decisions')]
    s = (f'{len(miss)} of {len(recs)} logged founder decisions have no metric or review date. '
         f'Nobody will know if they worked.')
    return [_finding('TEAM-R11', {'type': 'metric', 'id': 'decision_log_completeness', 'label': 'Decision log'},
                     'medium', ev, s, None, 0.5, [r['id'] for r in miss], rd.ends_on,
                     money_reason='a decision with no metric has no outcome to price')]


def rule_backlog(rd):
    rows = decision_log()
    if rows is None:
        return [_unavailable(rd, 'TEAM-R12', 'medium', 'decision_backlog', 'Decisions sent to a person',
                             'No action has been sent to a person yet, so there is no backlog to read.',
                             'the decision row on any screen (app/data/decisions.json)',
                             'Choose an action on any finding. The choice is logged and read here.')]
    cutoff = (rd.ends_on - timedelta(days=BACKLOG_DAYS)).isoformat()
    last = {}
    for r in rows:
        if not isinstance(r, dict) or not r.get('time'):
            continue
        k = (r.get('screen'), r.get('capability'))
        if str(r['time'])[:10] <= rd.ends_on.isoformat() and (k not in last or str(r['time']) >= str(last[k]['time'])):
            last[k] = r
    stale = sorted((r for r in last.values() if r.get('choice') == 'person' and str(r['time'])[:10] < cutoff),
                   key=lambda r: str(r['time']))
    if not stale:
        return []
    oldest = (rd.ends_on - date.fromisoformat(str(stale[0]['time'])[:10])).days
    ev = [_ev('decisions_waiting_on_a_person', len(stale), 'count', rd.ends_on, baseline=BACKLOG_DAYS,
              baseline_kind='threshold', window='open', source='decisions.json'),
          _ev('oldest_waiting_days', oldest, 'days', rd.ends_on, window='open', source='decisions.json')]
    s = f'{len(stale)} actions were sent to a person over {BACKLOG_DAYS} days ago with no update. The oldest is {oldest} days.'
    return [_finding('TEAM-R12', {'type': 'metric', 'id': 'decision_backlog', 'label': 'Decisions sent to a person'},
                     'medium', ev, s, None, 0.5, [], rd.ends_on, money_reason='the stake sits in the findings behind each action')]


def run(brand, window=None, data=None):
    """Findings for one brand, sorted by severity then money at stake. `window` is {ends_on} or None."""
    ends_on = date.fromisoformat(window['ends_on']) if window and window.get('ends_on') else last_full_day(data, brand)
    return findings(Reader(data, brand, ends_on))


def findings(rd):
    """run() on a Reader the caller already holds, so api.py reuses its queries."""
    out = (rule_peak(rd) + rule_resolution(rd) + rule_decision_log(rd) + rule_backlog(rd) + rule_sop(rd)
           + rule_not_connected(rd))
    out.sort(key=lambda f: (SEVERITY_ORDER[f['severity']], -((f.get('money_at_stake') or {}).get('usd') or -1),
                            f['status'] == 'unavailable', f['id']))
    return out
