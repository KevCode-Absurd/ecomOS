"""Measurement and data health audit (screen 22, round 0). Findings in the shape of app/contracts/audit.md.

Measurement compares what each platform says against the store. The store's paid orders are the truth.
Paid spend, platform purchases and GA4 funnel totals come from app/metrics.py. Store orders, GA4 daily
purchases and the fixture spend for YouTube creators, TikTok, Pinterest and other are counted in
data.sqlite with one GROUP BY each, like metrics.sql_paid_orders, so every ratio compares rows from the
same file and holds at any data scale. No connector, no model call. Same tables, same window, same
output, byte for byte. Window: 28 days ending on the brand's last full day, 4 trailing windows.

Rules (one per room insight, then one per room job the insights leave out)
  MEAS-R01  GA4 tracking gap. 6 checks on the GA4 sessions table against the store: purchase capture
            (GA4 purchases / store web orders >= 95 percent, critical), revenue capture (GA4 revenue /
            store web net revenue within 10 percent), no sampled rows, no thresholded rows, unassigned
            channel group under 2 percent of sessions, and a GA4 purchase on every day the store took a
            web order. Fires when any check fails; high when a critical one fails. Money:
            (0.95 - capture) x store web orders x AOV, the revenue GA4 cannot credit. MONEY-C20.
  MEAS-R02  Meta match quality below Meta's good band. Needs `pixel_capi_events`; unavailable until the
            Meta events manager is read. MONEY-C21.
  MEAS-R03  UTM leakage. Per paid platform with spend in the window: store orders from that platform
            with source, medium and campaign present and a paid medium / all store orders from it.
            Fires under 90 percent. Money: (1 - compliance) x platform spend 28d, spend whose orders
            cannot be tied to a campaign. A platform with no source mapping reads unavailable. MONEY-C22.
  MEAS-R04  Attribution gap widening. Per channel (Meta, Google): |platform purchase value - store net
            revenue from orders whose last click was that channel| / store value. Fires when the gap is
            over 5 percent and wider than the prior 28 days. The store's last click stands in for a
            data-driven model, which is not connected. Money: platform value - store value when
            positive, the value the platform claims beyond the store. MONEY-C23.
  MEAS-R05  Bot-driven spend spike. Needs a bot score per session; unavailable. MONEY-C24.
  MEAS-R06  Order count mismatch. Per platform per day: |platform orders - store orders| / store orders.
            GA4 against store web orders; Meta and Google against store orders with that last click.
            Fires when 2 days in a row are over 3 percent in the last 7 days. Money is null: the gap is
            priced once, in R01 and R04. MONEY-C24.
  MEAS-R07  Metric definition drift. Conversion rate has 2 definitions in active use: GA4 purchases /
            sessions (metrics.session_funnel) and store web orders / sessions. Fires when they differ by
            more than 5 percent. Low. BRN-C06.
  MEAS-R08  Daily trust check. For the last full day: every source has rows, GA4 capture within 5
            points of its 28-day rate, spend and platform purchases present. Fires on warn or fail.
            BRN-C02.
  MEAS-R09  Funnel step decay. session_funnel step rates for 28 days against the 90 days before it.
            Fires when a step fell more than 15 percent. DIAG-C01.
  MEAS-R10  RFM migration. Needs `rfm_scores` for 2 periods; unavailable. LIFE-C12.
  MEAS-R11  Source gone stale. A daily source whose last row is before the window end. BRN-C02.
  MEAS-R12  Attribution overlap. Sum of Meta and Google claimed purchases / store orders whose last click
            was paid social or paid search. Fires over 110 percent (platforms claim more orders than
            the store saw from them). Money: (claimed - store orders) x AOV. MONEY-C23.
  MEAS-R13  Incrementality untested. One per paid platform with 5 percent or more of paid spend and no
            `holdout_tests` row: unavailable with the test named. MONEY-C23.
  MEAS-R14  Tag fires more than once. Needs `tag_manager_log`; unavailable. MONEY-C65.
  MEAS-R15  Modeled contribution against platform claims. Needs `mmm_outputs`; unavailable. MONEY-C63.
  MEAS-R16  Dashboards on a stale or second definition. Needs a dashboard registry; unavailable. MONEY-C30.

Owner of every rule: 22-measurement.
"""
import importlib.util
import statistics
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parents[1]
SCREEN = '22-measurement'
DAYS = 28
TRAILING = 4

GA4_CAPTURE_MIN = 0.95
GA4_REVENUE_BAND = 0.10
UNASSIGNED_MAX = 0.02
UTM_MIN = 0.90
GAP_MIN = 0.05
DAILY_VARIANCE = 0.03
DRIFT_MIN = 0.05
TRUST_CAPTURE_POINTS = 0.05
FUNNEL_DROP = 0.15
OVERLAP_MAX = 1.10
HOLDOUT_SHARE = 0.05

PAID_STATES = ('paid', 'partially_refunded', 'refunded')
ORGANIC_MEDIUMS = ('social', 'organic', 'referral', '(none)', 'none', '')
# How store orders map to each paid platform: last-click channel and utm_source values.
PLATFORMS = {
    'meta': {'label': 'Meta', 'acq': 'paid_social', 'sources': ('facebook', 'instagram'), 'holdout': 'Meta conversion lift test (holdout of 10 percent of the audience for 4 weeks)'},
    'google': {'label': 'Google', 'acq': 'paid_search', 'sources': ('google',), 'mediums': ('cpc',), 'holdout': 'geo holdout (pause Google in matched states for 4 weeks)'},
    'youtube_creator': {'label': 'YouTube creators', 'sources': ('youtube',), 'holdout': 'geo holdout on creator posts with a matched control region'},
    'tiktok': {'label': 'TikTok', 'sources': ('tiktok',), 'holdout': 'TikTok conversion lift study or geo holdout'},
    'pinterest': {'label': 'Pinterest', 'sources': ('pinterest',), 'holdout': 'geo holdout (pause Pinterest in matched states for 4 weeks)'},
    'other': {'label': 'Other paid', 'sources': (), 'holdout': 'geo holdout once the spend is mapped to a platform'},
}

CAPABILITY = {
    'MEAS-R01': ('MONEY-C20', 'human_assist'), 'MEAS-R02': ('MONEY-C21', 'agent_does'),
    'MEAS-R03': ('MONEY-C22', 'human_assist'), 'MEAS-R04': ('MONEY-C23', 'agent_does'),
    'MEAS-R05': ('MONEY-C24', 'agent_does'), 'MEAS-R06': ('MONEY-C24', 'agent_does'),
    'MEAS-R07': ('BRN-C06', 'agent_does'), 'MEAS-R08': ('BRN-C02', 'agent_does'),
    'MEAS-R09': ('DIAG-C01', 'agent_does'), 'MEAS-R10': ('LIFE-C12', 'founder_gate'),
    'MEAS-R11': ('BRN-C02', 'agent_does'), 'MEAS-R12': ('MONEY-C23', 'agent_does'),
    'MEAS-R13': ('MONEY-C23', 'agent_does'), 'MEAS-R14': ('MONEY-C65', 'human_assist'),
    'MEAS-R15': ('MONEY-C63', 'human_assist'), 'MEAS-R16': ('MONEY-C30', 'agent_does'),
}
RULES = [
    {'rule_id': 'MEAS-R01', 'name': 'GA4 tracking gap: a setup check failed', 'entity_type': 'metric',
     'inputs': ['sessions', 'orders'], 'job': 'audit GA4 setup end to end'},
    {'rule_id': 'MEAS-R02', 'name': 'Meta match quality below the good band', 'entity_type': 'metric',
     'inputs': ['pixel_capi_events'], 'job': 'audit the Meta pixel and CAPI'},
    {'rule_id': 'MEAS-R03', 'name': 'UTM leakage: under 90 percent of a platform\'s orders carry a valid tag', 'entity_type': 'stage',
     'inputs': ['orders', 'ad_rows', 'google_rows', 'paid_other_spend'], 'job': 'enforce UTM and campaign-link discipline'},
    {'rule_id': 'MEAS-R04', 'name': 'Attribution gap over 5 percent and wider than last period', 'entity_type': 'stage',
     'inputs': ['ad_rows', 'google_rows', 'orders'], 'job': 'reconcile attribution models and run incrementality checks'},
    {'rule_id': 'MEAS-R05', 'name': 'Spend spike on a day with bot traffic above normal', 'entity_type': 'brand',
     'inputs': ['bot_scores'], 'job': 'reconcile GA4, Meta, Shopify and marketplace order counts'},
    {'rule_id': 'MEAS-R06', 'name': 'Order count off by over 3 percent 2 days in a row', 'entity_type': 'stage',
     'inputs': ['sessions', 'ad_rows', 'google_rows', 'orders'], 'job': 'reconcile GA4, Meta, Shopify and marketplace order counts'},
    {'rule_id': 'MEAS-R07', 'name': 'A metric defined two ways in active use', 'entity_type': 'metric',
     'inputs': ['sessions', 'orders'], 'job': 'maintain the metric contract and revenue definitions'},
    {'rule_id': 'MEAS-R08', 'name': 'Yesterday\'s trust check came back warn or fail', 'entity_type': 'brand',
     'inputs': ['orders', 'sessions', 'ad_rows', 'google_rows', 'paid_other_spend'], 'job': 'run the daily data-quality trust check'},
    {'rule_id': 'MEAS-R09', 'name': 'Funnel step down over 15 percent against its own 90 days', 'entity_type': 'stage',
     'inputs': ['sessions'], 'job': 'diagnose funnel and landing-page performance; triage a metric movement'},
    {'rule_id': 'MEAS-R10', 'name': 'Loyal customers moving to At Risk above the usual count', 'entity_type': 'brand',
     'inputs': ['rfm_scores'], 'job': 'build RFM and cohort segmentation'},
    {'rule_id': 'MEAS-R11', 'name': 'A source missed its daily refresh', 'entity_type': 'metric',
     'inputs': ['orders', 'sessions', 'ad_rows', 'google_rows', 'paid_other_spend'], 'job': 'run the daily data-quality trust check'},
    {'rule_id': 'MEAS-R12', 'name': 'Platforms claim over 110 percent of the store\'s paid orders', 'entity_type': 'brand',
     'inputs': ['ad_rows', 'google_rows', 'orders'], 'job': 'reconcile attribution models and run incrementality checks'},
    {'rule_id': 'MEAS-R13', 'name': 'A paid platform with no incrementality test on file', 'entity_type': 'stage',
     'inputs': ['holdout_tests'], 'job': 'reconcile attribution models and run incrementality checks'},
    {'rule_id': 'MEAS-R14', 'name': 'A tag fires more than once per event', 'entity_type': 'brand',
     'inputs': ['tag_manager_log'], 'job': 'audit tag management and server-side tracking'},
    {'rule_id': 'MEAS-R15', 'name': 'Modeled contribution far from what the platform claims', 'entity_type': 'brand',
     'inputs': ['mmm_outputs'], 'job': 'build marketing mix modeling for cross-channel budget allocation'},
    {'rule_id': 'MEAS-R16', 'name': 'A dashboard shows a number on a second definition', 'entity_type': 'brand',
     'inputs': ['dashboard_registry'], 'job': 'keep the standard dashboards current; ask any question about the numbers'},
]
for _r in RULES:
    _r['capability'], _r['owner_screen'] = CAPABILITY[_r['rule_id']][0], SCREEN
SEVERITY_ORDER = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}

_MODS = {}


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def metrics():
    if 'metrics' not in _MODS:
        _MODS['metrics'] = _load('ecomos_metrics_meas', APP / 'metrics.py')
    return _MODS['metrics']


def brand_data(brand):
    if 'tables' not in _MODS:
        _MODS['tables'] = _load('ecomos_tables_meas', APP / 'data' / 'tables.py')
    return _MODS['tables'].brand_data(brand)


class Missing(Exception):
    """A table this screen needs is not connected."""


def last_full_day(data, brand):
    source = brand_data(brand) if brand else data
    return date.fromisoformat(source.brand['as_of'])


def _win(end, days=DAYS):
    return (end - timedelta(days=days - 1)).isoformat(), end.isoformat()


def _div(a, b):
    return None if a is None or not b else a / b


def _r(x, n=4):
    return None if x is None else round(x, n)


class Reader:
    """One brand, one window end. m() is metrics.compute; sql() is the brand's data.sqlite, read only."""

    def __init__(self, data, brand, ends_on):
        self.data, self.brand, self.ends_on = data, brand, ends_on
        self.source = brand_data(brand) if brand else data
        b = self.source.brand or {}
        self.simulated = bool(b.get('simulated') or b.get('fictional'))

    def m(self, name, days=DAYS, end=None, **kw):
        q = {'window': f'{days}d', 'end': (end or self.ends_on).isoformat(), **kw}
        if self.brand:
            q['brand'] = self.brand
        return metrics().compute(name, self.data, **q)

    def sql(self, query, table):
        fn = getattr(self.source, '_sql', None)
        if fn is None:
            raise Missing(table)
        try:
            return fn(query)
        except KeyError:
            raise Missing(table)
        except Exception as exc:  # a table absent from data.sqlite
            if 'no such table' in str(exc):
                raise Missing(table)
            raise

    # ---- store (the truth)
    def store(self, end=None, days=DAYS):
        s, e = _win(end or self.ends_on, days)
        states = ', '.join(f"'{x}'" for x in PAID_STATES)
        rows = self.sql(
            "SELECT channel, acquisition_channel AS acq, lower(coalesce(utm_source, '')) AS src, "
            "lower(coalesce(utm_medium, '')) AS med, (coalesce(utm_campaign, '') != '') AS tagged, "
            "COUNT(*) AS n, SUM(subtotal - coalesce(discount, 0)) AS net FROM orders "
            f"WHERE status IN ({states}) AND substr(created_at, 1, 10) BETWEEN '{s}' AND '{e}' "
            "GROUP BY 1, 2, 3, 4, 5 ORDER BY 1, 2, 3, 4, 5", 'orders')
        rows = [dict(r) for r in rows]
        if not rows:
            raise Missing('orders')
        return rows

    def store_daily(self, end=None, days=DAYS):
        s, e = _win(end or self.ends_on, days)
        states = ', '.join(f"'{x}'" for x in PAID_STATES)
        rows = self.sql(
            "SELECT substr(created_at, 1, 10) AS day, channel, acquisition_channel AS acq, COUNT(*) AS n FROM orders "
            f"WHERE status IN ({states}) AND substr(created_at, 1, 10) BETWEEN '{s}' AND '{e}' GROUP BY 1, 2, 3 ORDER BY 1, 2, 3",
            'orders')
        out = {}
        for r in rows:
            d = out.setdefault(r['day'], {'web': 0, 'all': 0, 'paid_social': 0, 'paid_search': 0})
            d['all'] += r['n']
            if r['channel'] == 'web':
                d['web'] += r['n']
            if r['acq'] in d:
                d[r['acq']] += r['n']
        return out

    def ga4_daily(self, end=None, days=DAYS):
        s, e = _win(end or self.ends_on, days)
        rows = self.sql("SELECT date AS day, SUM(transactions) AS purchases, SUM(revenue) AS revenue, SUM(sessions) AS sessions "
                        f"FROM sessions WHERE date BETWEEN '{s}' AND '{e}' GROUP BY 1 ORDER BY 1", 'sessions')
        return {r['day']: dict(r) for r in rows}

    def ga4_health(self, end=None, days=DAYS):
        s, e = _win(end or self.ends_on, days)
        r = self.sql("SELECT SUM(sessions) AS sessions, SUM(transactions) AS purchases, SUM(revenue) AS revenue, "
                     "SUM(CASE WHEN sampled THEN 1 ELSE 0 END) AS sampled, SUM(CASE WHEN thresholded THEN 1 ELSE 0 END) AS thresholded, "
                     "SUM(CASE WHEN coalesce(channel_group, '') IN ('', 'Unassigned', '(other)') THEN sessions ELSE 0 END) AS unassigned "
                     f"FROM sessions WHERE date BETWEEN '{s}' AND '{e}'", 'sessions')[0]
        return dict(r)

    def ga4_by_source(self, end=None, days=DAYS):
        s, e = _win(end or self.ends_on, days)
        rows = self.sql("SELECT lower(session_source) AS src, channel_group, SUM(sessions) AS sessions FROM sessions "
                        f"WHERE date BETWEEN '{s}' AND '{e}' GROUP BY 1, 2 ORDER BY 1, 2", 'sessions')
        return [dict(r) for r in rows]

    def other_spend(self, end=None, days=DAYS):
        s, e = _win(end or self.ends_on, days)
        rows = self.sql("SELECT platform, SUM(spend) AS spend, MAX(date) AS last FROM paid_other_spend "
                        f"WHERE date BETWEEN '{s}' AND '{e}' GROUP BY 1 ORDER BY 1", 'paid_other_spend')
        return {r['platform']: {'spend': round(r['spend'], 2), 'last': r['last']} for r in rows}

    def platform(self, channel, end=None, days=DAYS):
        """Spend, purchases and purchase value a platform reports for the window, or None when not connected."""
        out = {}
        for name in ('spend', 'purchases', 'purchase_value'):
            r = self.m(name, days, end, channel=channel)
            if r.get('unavailable'):
                return None
            out[name] = r['value']
        return out

    def platform_daily(self, channel, end=None, days=DAYS):
        r = self.m('purchases', days, end, channel=channel, by='day')
        if r.get('unavailable'):
            return None
        return {g['day']: g['purchases'] for g in r['groups']}


# ---------------------------------------------------------------- store rollups

def store_totals(rows):
    t = {'orders': 0, 'net': 0.0, 'web_orders': 0, 'web_net': 0.0, 'paid_social': 0, 'paid_social_net': 0.0,
         'paid_search': 0, 'paid_search_net': 0.0}
    for r in rows:
        t['orders'] += r['n']
        t['net'] += r['net'] or 0
        if r['channel'] == 'web':
            t['web_orders'] += r['n']
            t['web_net'] += r['net'] or 0
        if r['acq'] in ('paid_social', 'paid_search'):
            t[r['acq']] += r['n']
            t[r['acq'] + '_net'] += r['net'] or 0
    return {k: (round(v, 2) if isinstance(v, float) else v) for k, v in t.items()}


def platform_orders(rows, key):
    """Store orders from one paid platform, and how many carry a valid tag (source, paid medium, campaign)."""
    spec = PLATFORMS[key]
    n = valid = 0
    for r in rows:
        mine = (r['src'] in spec['sources'] and (not spec.get('mediums') or r['med'] in spec['mediums'])) or \
               (spec.get('acq') and r['acq'] == spec['acq'])
        if not mine:
            continue
        n += r['n']
        if r['src'] and r['tagged'] and r['med'] not in ORGANIC_MEDIUMS:
            valid += r['n']
    return n, valid


def window_numbers(rd, end=None):
    """Everything one 28-day window needs, computed once. Missing tables read None, never 0."""
    end = end or rd.ends_on
    out = {'end': end.isoformat(), 'store': None, 'meta': rd.platform('meta', end), 'google': rd.platform('google', end),
           'other_spend': None, 'ga4': None, 'missing': []}
    try:
        out['rows'] = rd.store(end)
        out['store'] = store_totals(out['rows'])
    except Missing:
        out['rows'] = None
        out['missing'].append('orders')
    try:
        out['ga4'] = rd.ga4_health(end)
        if not out['ga4'].get('sessions'):
            out['ga4'] = None
            out['missing'].append('sessions')
    except Missing:
        out['missing'].append('sessions')
    try:
        out['other_spend'] = rd.other_spend(end)
    except Missing:
        out['missing'].append('paid_other_spend')
    for c in ('meta', 'google'):
        if out[c] is None:
            out['missing'].append({'meta': 'ad_rows', 'google': 'google_rows'}[c])
    return out


def spend_by_platform(w):
    out = {}
    for c in ('meta', 'google'):
        if w[c] is not None:
            out[c] = w[c]['spend']
    for p, v in (w['other_spend'] or {}).items():
        out[p] = v['spend']
    return out


def mer(w):
    """Store net revenue (all paid orders) over all paid spend. None when either side is missing."""
    if w['store'] is None or w['meta'] is None or w['google'] is None or w['other_spend'] is None:
        return None
    spend = sum(spend_by_platform(w).values())
    return {'value': _r(_div(w['store']['net'], spend)), 'net_revenue': w['store']['net'], 'spend': round(spend, 2),
            'spend_by_platform': spend_by_platform(w)}


def capture(w):
    if w['ga4'] is None or w['store'] is None or not w['store']['web_orders']:
        return None
    return _r(w['ga4']['purchases'] / w['store']['web_orders'])


def overlap(w):
    if w['store'] is None or w['meta'] is None or w['google'] is None:
        return None
    claimed = w['meta']['purchases'] + w['google']['purchases']
    store_paid = w['store']['paid_social'] + w['store']['paid_search']
    return {'claimed': int(round(claimed)), 'store_paid': store_paid, 'store_orders': w['store']['orders'],
            'store_web_orders': w['store']['web_orders'], 'value': _r(_div(claimed, store_paid)),
            'of_all_orders': _r(_div(claimed, w['store']['web_orders']))}


def gap(w, c):
    spec = PLATFORMS[c]
    if w['store'] is None or w[c] is None:
        return None
    store_v = w['store'][spec['acq'] + '_net']
    return {'platform_value': round(w[c]['purchase_value'], 2), 'store_value': store_v,
            'value': _r(_div(abs(w[c]['purchase_value'] - store_v), store_v))}


def aov(w):
    return None if w['store'] is None or not w['store']['orders'] else round(w['store']['net'] / w['store']['orders'], 2)


# ---------------------------------------------------------------- finding helpers

def _ev(rd, metric, value, unit, baseline=None, baseline_kind=None, window=f'{DAYS}d', source='orders', **extra):
    row = {'metric': metric, 'value': value, 'unit': unit, 'window': window, 'ends_on': rd.ends_on.isoformat(),
           'freshness_days': 1, 'baseline': baseline, 'baseline_kind': baseline_kind, 'source': source,
           'simulated': rd.simulated}
    row.update(extra)
    return row


def _confidence(agree):
    return 0.9 if agree >= 4 else 0.7 if agree >= 2 else 0.5


def _severity(stake, net_28d, agree, floor='medium'):
    if stake is not None and net_28d and stake > 0.05 * net_28d:
        return 'critical'
    if agree >= 2 or (stake is not None and net_28d and stake > 0.01 * net_28d):
        return 'high'
    return floor


def _cap(rule_id):
    cid, autonomy = CAPABILITY[rule_id]
    return {'id': cid, 'autonomy': autonomy}


def _finding(rd, rule_id, entity, severity, evidence, sentence, stake, confidence, brain_refs=(), money_reason=None):
    out = {'id': f'{SCREEN}.{rule_id}.{entity["id"]}', 'screen': SCREEN, 'rule_id': rule_id, 'severity': severity,
           'entity': entity, 'evidence': evidence, 'sentence': sentence, 'capability': _cap(rule_id),
           'money_at_stake': stake, 'confidence': confidence, 'brain_refs': list(brain_refs),
           'first_seen': rd.ends_on.isoformat(), 'last_seen': rd.ends_on.isoformat(), 'status': 'open', 'unavailable': None}
    if stake is None:
        out['money_reason'] = money_reason or 'no baseline'
    return out


def _unavailable(rd, rule_id, entity, severity, sentence, inputs, connector, fix, brain_refs=()):
    return {'id': f'{SCREEN}.{rule_id}.{entity["id"]}', 'screen': SCREEN, 'rule_id': rule_id, 'severity': severity,
            'entity': entity, 'evidence': [], 'sentence': sentence, 'capability': _cap(rule_id), 'money_at_stake': None,
            'confidence': 0.1, 'brain_refs': list(brain_refs),
            'first_seen': rd.ends_on.isoformat(), 'last_seen': rd.ends_on.isoformat(), 'status': 'unavailable',
            'unavailable': {'inputs': list(inputs), 'connector': connector, 'fix': fix}, 'money_reason': 'inputs unavailable'}


def _pct(x, n=1):
    v = round(x * 100, n)
    return f'{v:.{n}f}'.rstrip('0').rstrip('.') if n else f'{v:.0f}'


# ---------------------------------------------------------------- rules

def r01_ga4(rd, ws, net_28d):
    w = ws[0]
    ent = {'type': 'metric', 'id': 'ga4_audit_score', 'label': 'GA4 setup checks'}
    if w['ga4'] is None or w['store'] is None:
        return [_unavailable(rd, 'MEAS-R01', ent, 'high', 'GA4 setup cannot be checked: GA4 sessions or store orders are not connected.',
                             ['sessions', 'orders'], 'ga4, shopify', 'Connect GA4 (read only) and the Shopify store.')]
    g, st = w['ga4'], w['store']
    cap = capture(w)
    rev = _div(g['revenue'], st['web_net'])
    try:
        ga_days = rd.ga4_daily()
        st_days = rd.store_daily()
    except Missing:
        ga_days, st_days = {}, {}
    blank_days = sum(1 for d, v in st_days.items() if v['web'] and not (ga_days.get(d) or {}).get('purchases'))
    unassigned = _div(g['unassigned'], g['sessions'])
    checks = [
        {'check': 'purchase capture', 'critical': True, 'value': cap, 'pass': cap is not None and cap >= GA4_CAPTURE_MIN,
         'rule': f'GA4 purchases / store web orders >= {GA4_CAPTURE_MIN}'},
        {'check': 'revenue capture', 'critical': True, 'value': _r(rev), 'pass': rev is not None and abs(rev - 1) <= GA4_REVENUE_BAND,
         'rule': f'GA4 revenue / store web net revenue within {GA4_REVENUE_BAND}'},
        {'check': 'purchase event every day', 'critical': True, 'value': blank_days, 'pass': blank_days == 0,
         'rule': 'a GA4 purchase on every day the store took a web order'},
        {'check': 'no sampled rows', 'critical': False, 'value': g['sampled'], 'pass': not g['sampled'], 'rule': 'sampled rows = 0'},
        {'check': 'no thresholded rows', 'critical': False, 'value': g['thresholded'], 'pass': not g['thresholded'],
         'rule': 'thresholded rows = 0'},
        {'check': 'channel grouping', 'critical': False, 'value': _r(unassigned), 'pass': unassigned is not None and unassigned < UNASSIGNED_MAX,
         'rule': f'unassigned sessions / sessions < {UNASSIGNED_MAX}'},
    ]
    failed = [c for c in checks if not c['pass']]
    if not failed:
        return []
    top = sorted(failed, key=lambda c: (not c['critical'], c['check']))[0]
    stake, money_reason = None, None
    if cap is not None and cap < GA4_CAPTURE_MIN and aov(w):
        usd = round((GA4_CAPTURE_MIN - cap) * st['web_orders'] * aov(w))
        stake = {'usd': usd, 'formula': '(capture_target - ga4_capture) x store_web_orders x aov',
                 'inputs': {'capture_target': GA4_CAPTURE_MIN, 'ga4_capture': cap, 'store_web_orders': st['web_orders'],
                            'aov': aov(w)}, 'window': f'{DAYS}d'}
    else:
        money_reason = 'no purchase gap to price; the failed checks change how numbers read, not how many orders there are'
    agree = sum(1 for x in ws if capture(x) is not None and capture(x) < GA4_CAPTURE_MIN) if top['check'] == 'purchase capture' else 1
    evidence = [_ev(rd, 'ga4_purchase_capture', cap, 'ratio', GA4_CAPTURE_MIN, 'threshold', source='sessions, orders'),
                _ev(rd, 'ga4_purchases', g['purchases'], 'count', source='sessions'),
                _ev(rd, 'store_web_orders', st['web_orders'], 'count'),
                _ev(rd, 'ga4_revenue_capture', _r(rev), 'ratio', 1.0, 'threshold', source='sessions, orders'),
                _ev(rd, 'ga4_checks_failed', len(failed), 'count', 0, 'threshold', source='sessions',
                    checks=[{k: c[k] for k in ('check', 'critical', 'value', 'pass', 'rule')} for c in checks])]
    top_text = {'purchase capture': f'purchase capture at {_pct(cap)} percent of store web orders',
                'revenue capture': f'revenue capture at {_pct(rev or 0)} percent of store web revenue',
                'purchase event every day': f'no purchase recorded on {blank_days} days with orders'}.get(top['check'], top['check'])
    sentence = f'{len(failed)} of {len(checks)} GA4 checks failed, including {top_text}.'
    if top['check'] == 'purchase capture':
        sentence += f' GA4 missed {st["web_orders"] - int(g["purchases"]):,} of {st["web_orders"]:,} web orders in {DAYS} days.'
    sev = _severity(stake['usd'] if stake else None, net_28d, agree, 'high' if top['critical'] else 'medium')
    return [_finding(rd, 'MEAS-R01', ent, sev, evidence, sentence, stake, _confidence(agree), money_reason=money_reason)]


def r02_capi(rd):
    return [_unavailable(rd, 'MEAS-R02', {'type': 'metric', 'id': 'capi_match_quality', 'label': 'Meta event match quality'}, 'medium',
                         'Meta match quality cannot be read. The pixel and Conversions API event log is not connected.',
                         ['pixel_capi_events'], 'meta_events_manager', 'Connect Meta Events Manager (read only) for the pixel dataset.',
                         ['bombas.stack.tag_manager'])]


def r03_utm(rd, ws, net_28d):
    w, out = ws[0], []
    if w['rows'] is None:
        return [_unavailable(rd, 'MEAS-R03', {'type': 'stage', 'id': 'utm', 'label': 'UTM tags'}, 'medium',
                             'UTM tags cannot be checked: store orders are not connected.', ['orders'], 'shopify',
                             'Connect the Shopify store (read only).')]
    spend = spend_by_platform(w)
    for key in sorted(spend):
        if not spend[key]:
            continue
        spec = PLATFORMS.get(key, {'label': key, 'sources': ()})
        ent = {'type': 'stage', 'id': f'paid.{key}', 'label': f'{spec["label"]} paid, all campaigns'}
        if not spec['sources'] and not spec.get('acq'):
            out.append(_unavailable(rd, 'MEAS-R03', ent, 'medium',
                                    f'{spec["label"]} spent ${spend[key]:,.0f} in {DAYS} days, but its links are not mapped to the UTM convention.',
                                    ['utm_convention'], 'utm_convention', 'Name the utm_source this spend uses in the UTM convention.',
                                    ['bombas.economics.paid_media_split']))
            continue
        n, valid = platform_orders(w['rows'], key)
        if not n:
            continue
        rate = valid / n
        if rate >= UTM_MIN:
            continue
        agree = 1
        for x in ws[1:]:
            if x['rows'] is not None:
                pn, pv = platform_orders(x['rows'], key)
                agree += 1 if pn and pv / pn < UTM_MIN else 0
        usd = round((1 - rate) * spend[key])
        stake = {'usd': usd, 'formula': '(1 - utm_compliance) x platform_spend_28d',
                 'inputs': {'utm_compliance': _r(rate), 'platform_spend_28d': spend[key]}, 'window': f'{DAYS}d'}
        landed = []
        try:
            for s in rd.ga4_by_source():
                if s['src'] in spec['sources'] and spec['sources'] != ('google',):
                    landed.append({'channel_group': s['channel_group'], 'sessions': s['sessions']})
        except Missing:
            pass
        evidence = [_ev(rd, 'utm_compliance_rate', _r(rate), 'ratio', UTM_MIN, 'threshold'),
                    _ev(rd, 'store_orders_from_platform', n, 'count'),
                    _ev(rd, 'orders_with_valid_utm', valid, 'count'),
                    _ev(rd, 'platform_spend', spend[key], 'usd', source='paid_other_spend' if key not in ('meta', 'google') else
                        {'meta': 'ad_rows', 'google': 'google_rows'}[key])]
        if landed:
            evidence.append(_ev(rd, 'ga4_sessions_by_channel_group', sum(l['sessions'] for l in landed), 'count', source='sessions',
                                groups=landed))
        where = ''
        if landed:
            top = max(landed, key=lambda l: l['sessions'])['channel_group']
            where = f' GA4 files its visits under {top}.'
        sentence = (f'{_pct(1 - rate, 0)} percent of {n:,} orders from {spec["label"]} arrive with no valid campaign tag.'
                    f'{where}')
        out.append(_finding(rd, 'MEAS-R03', ent, _severity(usd, net_28d, agree), evidence, sentence, stake, _confidence(agree),
                            ['bombas.economics.paid_media_split']))
    return out


def r04_gap(rd, ws, net_28d):
    out = []
    for c in ('meta', 'google'):
        ent = {'type': 'stage', 'id': f'paid.{c}', 'label': f'{PLATFORMS[c]["label"]} attribution'}
        now, prev = gap(ws[0], c), gap(ws[1], c) if len(ws) > 1 else None
        if now is None:
            out.append(_unavailable(rd, 'MEAS-R04', ent, 'medium', f'{PLATFORMS[c]["label"]} attribution cannot be compared to the store.',
                                    ['ad_rows' if c == 'meta' else 'google_rows', 'orders'], 'meta_ads' if c == 'meta' else 'google_ads',
                                    'Connect the ad account and the store (read only).'))
            continue
        if now['value'] is None or now['value'] <= GAP_MIN or prev is None or prev['value'] is None or now['value'] <= prev['value']:
            continue
        agree = 1 + sum(1 for x in ws[1:] if (gap(x, c) or {}).get('value') is not None and gap(x, c)['value'] > GAP_MIN)
        over = round(now['platform_value'] - now['store_value'])
        stake = None
        if over > 0:
            stake = {'usd': over, 'formula': 'platform_purchase_value - store_last_click_net_revenue',
                     'inputs': {'platform_purchase_value': now['platform_value'], 'store_last_click_net_revenue': now['store_value']},
                     'window': f'{DAYS}d'}
        src = 'ad_rows' if c == 'meta' else 'google_rows'
        evidence = [_ev(rd, 'attribution_model_gap', now['value'], 'ratio', prev['value'], 'own_median', source=f'{src}, orders',
                        note='baseline is the 28 days before; the store last click stands in for a data-driven model'),
                    _ev(rd, 'platform_purchase_value', now['platform_value'], 'usd', source=src),
                    _ev(rd, 'store_last_click_net_revenue', now['store_value'], 'usd')]
        word = 'more' if over > 0 else 'less'
        sentence = (f'{PLATFORMS[c]["label"]} and the store now differ by {_pct(now["value"])} percent on sales value, up from '
                    f'{_pct(prev["value"])} percent. {PLATFORMS[c]["label"]} claims ${abs(over):,} {word} than the store counts.')
        out.append(_finding(rd, 'MEAS-R04', ent, _severity(stake['usd'] if stake else None, net_28d, agree), evidence, sentence,
                            stake, _confidence(agree), money_reason='platform claims less than the store; nothing over-credited'))
    return out


def r05_bots(rd):
    return [_unavailable(rd, 'MEAS-R05', {'type': 'brand', 'id': 'brand', 'label': 'Bot traffic'}, 'medium',
                         'Spend spikes cannot be checked for bot traffic. No bot score per session is connected.',
                         ['bot_scores'], 'cloudflare_bot_analytics', 'Connect a bot score source, such as the CDN\'s bot analytics.',
                         ['bombas.stack.performance_vendor'])]


def _runs(pairs):
    """Longest run of consecutive days over the variance line in the last 7 days, and the days over."""
    best = run = 0
    for _, over in pairs[-7:]:
        run = run + 1 if over else 0
        best = max(best, run)
    return best


def r06_counts(rd, ws):
    out = []
    try:
        st = rd.store_daily()
    except Missing:
        return [_unavailable(rd, 'MEAS-R06', {'type': 'stage', 'id': 'orders', 'label': 'Order counts'}, 'high',
                             'Order counts cannot be reconciled: store orders are not connected.', ['orders'], 'shopify',
                             'Connect the Shopify store (read only).')]
    series = {}
    try:
        series['ga4'] = ({d: v['purchases'] for d, v in rd.ga4_daily().items()}, 'web', 'GA4', 'sessions')
    except Missing:
        pass
    for c, acq in (('meta', 'paid_social'), ('google', 'paid_search')):
        daily = rd.platform_daily(c)
        if daily is not None:
            series[c] = (daily, acq, PLATFORMS[c]['label'], 'ad_rows' if c == 'meta' else 'google_rows')
    for key in sorted(series):
        daily, col, label, src = series[key]
        pairs, plat_total, store_total = [], 0, 0
        for d in sorted(st):
            s_n, p_n = st[d][col], daily.get(d)
            if p_n is None or not s_n:
                pairs.append((d, False))
                continue
            plat_total += p_n
            store_total += s_n
            pairs.append((d, abs(p_n - s_n) / s_n > DAILY_VARIANCE))
        run = _runs(pairs)
        if run < 2 or not store_total:
            continue
        days_over = sum(1 for _, o in pairs if o)
        diff = int(round(plat_total - store_total))
        var = abs(diff) / store_total
        what = 'web orders' if col == 'web' else 'orders with that last click'
        evidence = [_ev(rd, 'order_count_variance', _r(var), 'ratio', DAILY_VARIANCE, 'threshold', source=f'{src}, orders'),
                    _ev(rd, 'platform_orders', int(round(plat_total)), 'count', source=src),
                    _ev(rd, 'store_orders', store_total, 'count', note=f'store {what}'),
                    _ev(rd, 'days_over_3_percent', days_over, 'count', DAYS, 'threshold'),
                    _ev(rd, 'longest_run_last_7_days', run, 'count', 2, 'threshold', window='7d')]
        sentence = (f'{label} shows {abs(diff):,} {"more" if diff > 0 else "fewer"} orders than Shopify over {DAYS} days. '
                    f'{days_over} of {DAYS} days were more than 3 percent apart.')
        agree = min(TRAILING, 1 + days_over // 7)
        out.append(_finding(rd, 'MEAS-R06', {'type': 'stage', 'id': f'orders.{key}', 'label': f'{label} against Shopify orders'},
                            'high' if days_over >= 14 else 'medium', evidence, sentence, None, _confidence(agree),
                            money_reason='the gap is priced once, in MEAS-R01 for GA4 and MEAS-R04 for ad platforms'))
    return out


def r07_drift(rd, ws):
    w = ws[0]
    ent = {'type': 'metric', 'id': 'conversion_rate', 'label': 'Conversion rate'}
    f = rd.m('session_funnel')
    if f.get('unavailable') or w['store'] is None:
        return []
    ga_cvr = f['rates']['conversion_rate']
    store_cvr = _div(w['store']['web_orders'], f['inputs']['sessions'])
    if store_cvr is None or not ga_cvr or abs(store_cvr / ga_cvr - 1) <= DRIFT_MIN:
        return []
    evidence = [_ev(rd, 'conversion_rate_ga4', _r(ga_cvr, 6), 'ratio', source='sessions', formula='GA4 purchases / sessions'),
                _ev(rd, 'conversion_rate_store', _r(store_cvr, 6), 'ratio', source='orders, sessions', formula='store web orders / sessions'),
                _ev(rd, 'metric_definition_drift', 1, 'count', 0, 'threshold', source='metric contract')]
    sentence = (f'Conversion rate is defined two ways in active use: GA4 purchases over sessions ({_pct(ga_cvr, 2)} percent) '
                f'and store web orders over sessions ({_pct(store_cvr, 2)} percent).')
    return [_finding(rd, 'MEAS-R07', ent, 'low', evidence, sentence, None, 0.5, money_reason='definition gap: no money formula')]


def trust_checks(rd, w):
    """Pass, warn or fail for the last full day. Each check says what it read."""
    day = rd.ends_on.isoformat()
    checks = []

    def add(name, status, detail):
        checks.append({'check': name, 'status': status, 'detail': detail})
    try:
        st = rd.store_daily(days=1).get(day)
        add('store orders present', 'pass' if st and st['all'] else 'fail', f'{(st or {}).get("all", 0)} paid orders on {day}')
    except Missing:
        st = None
        add('store orders present', 'fail', 'orders not connected')
    try:
        ga = rd.ga4_daily(days=1).get(day)
        add('GA4 sessions present', 'pass' if ga and ga['sessions'] else 'fail', f'{(ga or {}).get("sessions", 0) or 0:,} sessions')
    except Missing:
        ga = None
        add('GA4 sessions present', 'fail', 'sessions not connected')
    for c in ('meta', 'google'):
        p = rd.platform(c, days=1)
        add(f'{PLATFORMS[c]["label"]} spend and purchases present', 'pass' if p and p['spend'] and p['purchases'] else 'warn' if p else 'fail',
            'not connected' if p is None else f'${p["spend"]:,.0f} spend, {int(p["purchases"])} purchases')
    try:
        other = rd.other_spend(days=1)
        add('other paid spend present', 'pass' if other else 'warn', f'{len(other)} platforms with spend')
    except Missing:
        add('other paid spend present', 'warn', 'paid_other_spend not connected')
    base = capture(w)
    if ga and st and st['web'] and base is not None:
        day_cap = ga['purchases'] / st['web']
        ok = abs(day_cap - base) <= TRUST_CAPTURE_POINTS
        add('GA4 capture in its usual range', 'pass' if ok else 'warn',
            f'{_pct(day_cap)} percent against {_pct(base)} percent over {DAYS} days')
    status = 'fail' if any(c['status'] == 'fail' for c in checks) else 'warn' if any(c['status'] == 'warn' for c in checks) else 'pass'
    return {'day': day, 'status': status, 'checks': checks}


def r08_trust(rd, ws):
    t = trust_checks(rd, ws[0])
    if t['status'] == 'pass':
        return []
    bad = [c for c in t['checks'] if c['status'] != 'pass']
    evidence = [_ev(rd, 'daily_trust_score', t['status'], 'grade', 'pass', 'threshold', window='1d', source='all sources', checks=t['checks'])]
    sentence = f'Yesterday\'s data quality check came back {t["status"]}: {bad[0]["check"]} ({bad[0]["detail"]}).'
    return [_finding(rd, 'MEAS-R08', {'type': 'brand', 'id': 'brand', 'label': 'Daily trust check'},
                     'high' if t['status'] == 'fail' else 'medium', evidence, sentence, None, 0.5,
                     money_reason='a trust check prices nothing; it gates the numbers other findings use')]


FUNNEL_STEPS = [('add_to_cart_rate', 'Add to cart', 'sessions'), ('checkout_rate', 'Cart to checkout', 'add_to_cart'),
                ('purchase_rate', 'Checkout to purchase', 'checkout')]


def r09_funnel(rd, net_28d):
    now = rd.m('session_funnel')
    base = rd.m('session_funnel', 90, rd.ends_on - timedelta(days=DAYS))
    if now.get('unavailable') or base.get('unavailable'):
        return []
    out = []
    for key, label, vol in FUNNEL_STEPS:
        cur, ref = now['rates'].get(key), base['rates'].get(key)
        if not cur or not ref or cur >= ref * (1 - FUNNEL_DROP):
            continue
        drop = 1 - cur / ref
        evidence = [_ev(rd, key, cur, 'ratio', ref, 'own_median', source='sessions', note='baseline is the 90 days before the window'),
                    _ev(rd, vol, now['inputs'][vol], 'count', source='sessions')]
        sentence = f'{label} conversion fell {_pct(drop, 0)} percent versus your own 90-day average.'
        out.append(_finding(rd, 'MEAS-R09', {'type': 'stage', 'id': key, 'label': label}, 'medium', evidence, sentence, None, 0.5,
                            money_reason='AOV for GA4 purchases is not in the funnel table'))
    return out


def r10_rfm(rd):
    return [_unavailable(rd, 'MEAS-R10', {'type': 'brand', 'id': 'brand', 'label': 'RFM segments'}, 'medium',
                         'Segment moves cannot be counted yet. RFM scores need 2 monthly periods built from orders.',
                         ['rfm_scores'], 'warehouse', 'Build monthly RFM scores from store orders.')]


def r11_stale(rd):
    out = []
    tables = {'orders': "SELECT MAX(substr(created_at, 1, 10)) AS last FROM orders",
              'sessions': "SELECT MAX(date) AS last FROM sessions", 'ad_rows': "SELECT MAX(date) AS last FROM ad_rows",
              'google_rows': "SELECT MAX(date) AS last FROM google_rows", 'paid_other_spend': "SELECT MAX(date) AS last FROM paid_other_spend"}
    for t, q in tables.items():
        try:
            last = rd.sql(q, t)[0]['last']
        except Missing:
            continue
        if last and last < rd.ends_on.isoformat():
            hours = (rd.ends_on - date.fromisoformat(last[:10])).days * 24
            out.append(_finding(rd, 'MEAS-R11', {'type': 'metric', 'id': f'source_freshness_lag.{t}', 'label': t}, 'high',
                                [_ev(rd, 'source_freshness_lag', hours, 'hours', 24, 'threshold', window='1d', source=t, last_row=last)],
                                f'{t} has not refreshed in {hours} hours. Its last row is {last}.', None, 0.9,
                                money_reason='stale data prices nothing; it makes other findings late'))
    return out


def r12_overlap(rd, ws, net_28d):
    o = overlap(ws[0])
    if o is None:
        return [_unavailable(rd, 'MEAS-R12', {'type': 'brand', 'id': 'brand', 'label': 'Attribution overlap'}, 'high',
                             'Platform claims cannot be compared to store orders.', ['ad_rows', 'google_rows', 'orders'],
                             'meta_ads, google_ads, shopify', 'Connect Meta, Google Ads and the store (read only).')]
    if o['value'] is None or o['value'] <= OVERLAP_MAX:
        return []
    extra = o['claimed'] - o['store_paid']
    a = aov(ws[0])
    stake = {'usd': round(extra * a), 'formula': '(claimed_purchases - store_paid_orders) x aov',
             'inputs': {'claimed_purchases': o['claimed'], 'store_paid_orders': o['store_paid'], 'aov': a}, 'window': f'{DAYS}d'}
    agree = sum(1 for x in ws if (overlap(x) or {}).get('value') and overlap(x)['value'] > OVERLAP_MAX)
    evidence = [_ev(rd, 'attribution_overlap', o['value'], 'ratio', OVERLAP_MAX, 'threshold', source='ad_rows, google_rows, orders'),
                _ev(rd, 'claimed_purchases', o['claimed'], 'count', source='ad_rows, google_rows'),
                _ev(rd, 'store_paid_orders', o['store_paid'], 'count')]
    sentence = (f'Meta and Google claim {o["claimed"]:,} purchases. The store saw {o["store_paid"]:,} orders whose last click was paid.')
    return [_finding(rd, 'MEAS-R12', {'type': 'brand', 'id': 'brand', 'label': 'Attribution overlap'},
                     _severity(stake['usd'], net_28d, agree), evidence, sentence, stake, _confidence(agree))]


def r13_incrementality(rd, ws):
    spend = spend_by_platform(ws[0])
    total = sum(spend.values())
    try:
        tested = {r['channel'] for r in rd.sql('SELECT DISTINCT channel FROM holdout_tests', 'holdout_tests')}
    except Missing:
        tested = set()
    out = []
    for key in sorted(spend, key=lambda k: (-spend[k], k)):
        if not total or spend[key] / total < HOLDOUT_SHARE or key in tested:
            continue
        spec = PLATFORMS.get(key, {'label': key, 'holdout': 'geo holdout'})
        out.append(_unavailable(rd, 'MEAS-R13', {'type': 'stage', 'id': f'paid.{key}', 'label': f'{spec["label"]} incrementality'}, 'medium',
                                f'No holdout test on file for {spec["label"]}, which took {_pct(spend[key] / total, 0)} percent of paid spend. '
                                f'Test to run: {spec["holdout"]}.',
                                ['holdout_tests'], 'holdout_tests', f'Run a {spec["holdout"]} and log the result.',
                                ['bombas.economics.paid_media_split']))
    return out


def r14_tags(rd):
    return [_unavailable(rd, 'MEAS-R14', {'type': 'brand', 'id': 'brand', 'label': 'Tag manager'}, 'low',
                         'Duplicate tag fires cannot be counted. The tag manager debug log is not connected.',
                         ['tag_manager_log'], 'gtm_debug_log', 'Export the tag manager preview log or a server container log.',
                         ['bombas.stack.tag_manager', 'bombas.stack.cookie_consent'])]


def r15_mmm(rd):
    return [_unavailable(rd, 'MEAS-R15', {'type': 'brand', 'id': 'brand', 'label': 'Marketing mix model'}, 'low',
                         'No marketing mix model has run, so modeled channel value cannot be set against platform claims.',
                         ['mmm_outputs'], 'mmm_outputs', 'Run a marketing mix model on at least 6 months of spend and orders.',
                         ['bombas.economics.paid_media_split'])]


def r16_dashboards(rd):
    return [_unavailable(rd, 'MEAS-R16', {'type': 'brand', 'id': 'brand', 'label': 'Dashboards'}, 'low',
                         'Dashboards cannot be checked against the metric contract. No list of dashboards and their formulas exists.',
                         ['dashboard_registry'], 'dashboard_registry', 'List each dashboard, its numbers and the formula each uses.',
                         ['bombas.stack.tool_detected.2'])]


def windows(rd):
    return [window_numbers(rd, rd.ends_on - timedelta(days=DAYS * k)) for k in range(TRAILING + 1)]


def run(brand, window=None, data=None, ws=None):
    """Findings for one brand and window ({ends_on, days, trailing}), sorted by severity then stake."""
    data = data if data is not None else (brand_data(brand) if brand else None)
    ends_on = date.fromisoformat(window['ends_on']) if window and window.get('ends_on') else last_full_day(data, brand)
    rd = Reader(data, brand, ends_on)
    ws = ws or windows(rd)
    net_28d = ws[0]['store']['net'] if ws[0]['store'] else None
    out = []
    out += r01_ga4(rd, ws, net_28d)
    out += r02_capi(rd)
    out += r03_utm(rd, ws, net_28d)
    out += r04_gap(rd, ws, net_28d)
    out += r05_bots(rd)
    out += r06_counts(rd, ws)
    out += r07_drift(rd, ws)
    out += r08_trust(rd, ws)
    out += r09_funnel(rd, net_28d)
    out += r10_rfm(rd)
    out += r11_stale(rd)
    out += r12_overlap(rd, ws, net_28d)
    out += r13_incrementality(rd, ws)
    out += r14_tags(rd)
    out += r15_mmm(rd)
    out += r16_dashboards(rd)
    out.sort(key=lambda f: (SEVERITY_ORDER[f['severity']], f['status'] == 'unavailable',
                            -((f['money_at_stake'] or {}).get('usd') or 0), f['id']))
    return out
