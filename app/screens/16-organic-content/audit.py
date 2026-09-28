"""Organic and content audit (screen 16, round 0). Findings in the shape of app/contracts/audit.md.

Numbers come from the `content_posts` table (platform exports: platform, date, format, hook, views,
saves, clicks, matched_orders), `app/metrics.py` (aov, session_funnel) and the brand brain
(`app/brain/<brand>/`). No connector, no model call. Same tables, brain and window give the same
findings, byte for byte. The metric contract has no content metric yet; the post sums below are
plain window totals over `content_posts` and are listed in FEATURES.md for a contract session.

Rules. R01 to R15 are the room spec's insights in order; R16 is the hook read behind ORG-C16.
A rule whose table is not connected emits one `unavailable` finding, never a 0.
  ORG-R01  Posting floor missed: posts published this week under the floor planned in the calendar.
           Needs `content_calendar` (planned posts and floor). Capability ORG-C02.
  ORG-R02  Holiday gap: a US holiday or retail moment within 14 days with no script assigned. The
           holiday list is a rule constant (US_MOMENTS); scripts need `content_calendar`. ORG-C02.
  ORG-R03  Festival gap: the same for India festivals. Market IN only; a US brand emits nothing.
  ORG-R04  Stranger-blind viral post: a top 3 post by views in 30 days with no SKU tag and no CTA tag.
           Needs `content_posts.sku_tag` and `content_posts.cta_tag`. Capability ORG-C16.
  ORG-R05  Broad low-value hit: posts in the top quartile by views in 30 days with matched orders under
           the floor (ORDERS_FLOOR, a rule default until the brand sets one in the brain). Money: null,
           the floor is not the brand's own history. Capability ORG-C16.
  ORG-R06  Unused UGC: verified reviews or photos unposted over 21 days. Needs `ugc_assets`. ORG-C11.
  ORG-R07  Asset expiring unused: shelf life ends within 7 days and reuse count is 0. Needs
           `asset_library`. Capability ORG-C13.
  ORG-R08  Claims gate pattern: one claims rule held 3 or more posts this month. Needs
           `claims_gate_log`. Capability LOOP-C12.
  ORG-R09  Creator seeding, no yield: seeded over 21 days ago, no content delivered. Needs
           `creator_seeding`. Capability ORG-C14.
  ORG-R10  DM funnel leak: over 70 percent of DM threads end with no captured contact. Needs
           `dm_funnel`. Capability ORG-C10.
  ORG-R11  Dead or mismatched link on a live post. Needs `link_check_log`. Capability ORG-C12.
  ORG-R12  Comment response lag: a message needing a reply waited over 24 hours. Needs `inbox_log`.
           Capability ORG-C09.
  ORG-R13  Community going quiet: active member rate down 10 points or more month over month. Needs
           `community_roster`. Capability LIFE-C53.
  ORG-R14  YouTube search share falling against the prior period. Needs `youtube_studio_export`.
           Capability ORG-C38.
  ORG-R15  Founder over budget: share of posts with the founder on camera above the plan's target.
           Needs `content_posts.founder_on_camera` and a target in brain `content`. Capability ORG-C03.
  ORG-R16  Hook sells under the brand's median: a hook with 5 or more posts in 90 days whose matched
           orders per 1,000 views are under 0.75 x the median of the brand's hooks in the same window.
           Money: (median rate - hook rate) x hook views x aov_90d, the orders the hook's views would
           have matched at the median rate. Capability ORG-C16. Owner: 16-organic-content.
All rules are owned by 16-organic-content.
"""
import importlib.util
import statistics
import sys
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parents[1]
SCREEN = '16-organic-content'

POST_WINDOW = 30
HOOK_WINDOW = 90
SESSION_WINDOW = 28
ORDERS_FLOOR = 5
HOOK_RATE_X = 0.75
HOOK_MIN_POSTS = 5
HOLIDAY_DAYS = 14
TOP_QUARTILE = 0.25
# US holidays and retail moments, 2026 and early 2027 (rule constant, public calendar).
US_MOMENTS = [
    ('2026-10-12', 'Columbus Day'), ('2026-10-31', 'Halloween'), ('2026-11-11', 'Veterans Day'),
    ('2026-11-26', 'Thanksgiving'), ('2026-11-27', 'Black Friday'), ('2026-11-30', 'Cyber Monday'),
    ('2026-12-01', 'Giving Tuesday'), ('2026-12-25', 'Christmas'), ('2027-01-01', "New Year's Day"),
    ('2027-02-14', "Valentine's Day"),
]


def _r(rule_id, name, entity_type, inputs, capability, autonomy, severity, markets=None):
    out = {'rule_id': rule_id, 'name': name, 'entity_type': entity_type, 'inputs': inputs, 'capability': capability,
           'autonomy': autonomy, 'severity': severity, 'owner_screen': SCREEN}
    if markets:
        out['markets'] = markets
    return out


RULES = [
    _r('ORG-R01', 'Posting floor missed this week', 'brand', ['content_calendar'], 'ORG-C02', 'agent_does', 'medium'),
    _r('ORG-R02', 'US holiday within 14 days has no script', 'brand', ['content_calendar'], 'ORG-C02', 'agent_does', 'medium'),
    _r('ORG-R03', 'India festival within 14 days has no script', 'brand', ['content_calendar'], 'ORG-C02', 'agent_does',
       'medium', markets=['IN']),
    _r('ORG-R04', 'Top 3 post by views names no product and gives no next step', 'metric',
       ['content_posts.sku_tag', 'content_posts.cta_tag'], 'ORG-C16', 'agent_does', 'medium'),
    _r('ORG-R05', 'Top quartile posts by views sold under the orders floor', 'metric',
       ['content_posts'], 'ORG-C16', 'agent_does', 'medium'),
    _r('ORG-R06', 'Verified reviews and UGC unposted over 21 days', 'brand', ['ugc_assets'], 'ORG-C11', 'agent_does', 'low'),
    _r('ORG-R07', 'Assets retire this week without reuse', 'brand', ['asset_library'], 'ORG-C13', 'agent_does', 'low'),
    _r('ORG-R08', 'One claims rule held 3 or more posts this month', 'brand', ['claims_gate_log'], 'LOOP-C12',
       'agent_does', 'medium'),
    _r('ORG-R09', 'Seeded creators delivered nothing in 3 weeks', 'brand', ['creator_seeding'], 'ORG-C14',
       'founder_gate', 'medium'),
    _r('ORG-R10', 'Over 70 percent of DM threads capture no contact', 'brand', ['dm_funnel'], 'ORG-C10',
       'founder_gate', 'medium'),
    _r('ORG-R11', 'Live post links to a dead or mismatched page', 'brand', ['link_check_log'], 'ORG-C12',
       'agent_does', 'high'),
    _r('ORG-R12', 'Messages waiting over 24 hours for a reply', 'brand', ['inbox_log'], 'ORG-C09', 'human_assist', 'medium'),
    _r('ORG-R13', 'Community active rate down 10 points month over month', 'brand', ['community_roster'], 'LIFE-C53',
       'founder_gate', 'low'),
    _r('ORG-R14', 'YouTube search share of views falling', 'brand', ['youtube_studio_export'], 'ORG-C38',
       'human_assist', 'low'),
    _r('ORG-R15', 'Founder on camera above the plan', 'brand',
       ['content_posts.founder_on_camera', 'brain.content (founder_camera_target)'], 'ORG-C03', 'human_assist', 'low'),
    _r('ORG-R16', 'Hook sells under 0.75 x the median hook', 'metric', ['content_posts'], 'ORG-C16', 'agent_does', 'medium'),
]
BY_ID = {r['rule_id']: r for r in RULES}
SEVERITY_ORDER = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}

# rule_id: (sentence, connector, fix) when the rule's table is not connected.
UNAVAILABLE = {
    'ORG-R01': ('No content calendar is connected, so this week\'s posts cannot be checked against a plan.',
                'content calendar export', 'Connect the content calendar and set a weekly posting floor.'),
    'ORG-R04': ('Posts carry no SKU or CTA tag, so a viral post that sold nothing cannot be spotted.',
                'platform insights (Instagram, TikTok)', 'Tag each post with the SKU it shows and its call to action.'),
    'ORG-R06': ('No UGC library is connected, so unused reviews and photos cannot be counted.',
                'reviews app export plus manual intake', 'Connect the UGC intake list with a posted flag.'),
    'ORG-R07': ('No asset library is connected, so assets about to retire cannot be listed.',
                'asset tagging tool', 'Tag assets with a shelf-life end date and the surfaces they ran on.'),
    'ORG-R08': ('No claims gate log is on file, so held posts cannot be counted.',
                'claims gate script (ORG-C15)', 'Run the claims gate before each post and keep its log.'),
    'ORG-R09': ('No creator seeding tracker is connected, so seeded creators with no content cannot be found.',
                'seeding tracker (sheet or CRM)', 'Connect the seeding sheet with seeded date and content delivered.'),
    'ORG-R10': ('No DM funnel data is connected, so contact capture from DMs is unknown.',
                'DM automation tool plus CRM', 'Connect the DM tool so each thread records a captured contact.'),
    'ORG-R11': ('No link check has run, so dead or mismatched post links cannot be found.',
                'link crawler', 'Run a daily link check on posts from the last 90 days.'),
    'ORG-R12': ('No inbox log is connected, so reply wait times are unknown.',
                'unified inbox export', 'Connect the social inbox with received and first reply times.'),
    'ORG-R13': ('No community roster is connected, so member activity is unknown.',
                'Discord or SMS platform export', 'Connect the community roster with last active dates.'),
    'ORG-R14': ('No YouTube Studio export is connected, so search share of views is unknown.',
                'YouTube Studio API', 'Connect YouTube Studio with views by traffic source.'),
    'ORG-R15': ('Posts are not tagged for the founder on camera and no on-camera target is set.',
                'post tags plus the on-camera plan', 'Tag posts that show the founder and set a monthly target.'),
}

_MODS = {}


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def metrics():
    if 'metrics' not in _MODS:
        _MODS['metrics'] = _load('ecomos_metrics_organic', APP / 'metrics.py')
    return _MODS['metrics']


def brand_data(brand):
    if 'tables' not in _MODS:
        _MODS['tables'] = _load('ecomos_tables_organic', APP / 'data' / 'tables.py')
    return _MODS['tables'].brand_data(brand)


def brain_records(brand, section, today):
    """Brain records for one section, or [] when the brand has no brain."""
    if not brand or not (APP / 'brain' / brand).is_dir():
        return []
    if 'brain' not in _MODS:
        if str(APP / 'brain') not in sys.path:
            sys.path.insert(0, str(APP / 'brain'))  # store.py imports its sibling validate.py
        _MODS['brain'] = _load('ecomos_brain_organic', APP / 'brain' / 'store.py')
    return _MODS['brain'].Brain(brand, today=today).records(section)


class Reader:
    """One brand, one window end. m() is metrics.compute with brand and end filled in; posts() reads content_posts."""

    def __init__(self, data, brand, ends_on):
        self.data, self.brand, self.ends_on = data, brand, ends_on
        self.source = data if data is not None else brand_data(brand)

    def m(self, name, days, end=None, **kw):
        q = {'window': f'{days}d', 'end': (end or self.ends_on).isoformat(), **kw}
        if self.brand:
            q['brand'] = self.brand
        return metrics().compute(name, self.data, **q)

    def all_posts(self):
        """Every content_posts row, or None when the table is missing (unavailable, never 0)."""
        try:
            return self.source.table('content_posts')
        except (KeyError, ValueError):
            return None

    def posts(self, days, end=None):
        rows = self.all_posts()
        if rows is None:
            return None
        end = end or self.ends_on
        start = (end - timedelta(days=days - 1)).isoformat()
        return sorted((r for r in rows if start <= r['date'] <= end.isoformat()),
                      key=lambda r: (r['date'], r['platform'], r.get('hook') or ''))

    def columns(self):
        rows = self.all_posts()
        return set(rows[0]) if rows else set()

    def aov(self, days=HOOK_WINDOW):
        r = self.m('aov', days)
        return None if r.get('unavailable') else r['value']


def last_full_day(data, brand):
    source = brand_data(brand) if brand else data
    return date.fromisoformat(source.brand['as_of'])


def post_label(p):
    return f'{p["platform"].capitalize()} {p.get("format") or "post"} on {p["date"]}, {p.get("hook") or "no hook"}'


def per_1k(orders, views):
    return round(orders / views * 1000, 4) if views else None


def hook_rates(posts):
    """Per hook: posts, views, matched orders and matched orders per 1,000 views. Rows with a blank cell are skipped."""
    by = {}
    for p in posts:
        if p.get('views') is None or p.get('matched_orders') is None:
            continue
        h = by.setdefault(p.get('hook') or 'untagged', {'posts': 0, 'views': 0, 'orders': 0})
        h['posts'] += 1
        h['views'] += p['views']
        h['orders'] += p['matched_orders']
    for h in by.values():
        h['per_1k'] = per_1k(h['orders'], h['views'])
    return by


def _ev(metric, value, unit, ends_on, window, baseline=None, baseline_kind=None, source='content_posts'):
    return {'metric': metric, 'value': value, 'unit': unit, 'window': window, 'ends_on': ends_on.isoformat(),
            'freshness_days': 1, 'baseline': baseline, 'baseline_kind': baseline_kind, 'source': source, 'simulated': True}


def _confidence(windows_agree, peer=False):
    c = 0.9 if windows_agree >= 4 else 0.7 if windows_agree >= 2 else 0.5
    return round(max(c - (0.2 if peer else 0), 0.1), 2)


def _severity(stake, net_28d, windows_agree):
    if stake is not None and net_28d and stake > 0.05 * net_28d:
        return 'critical'
    if windows_agree >= 2 or (stake is not None and net_28d and stake > 0.01 * net_28d):
        return 'high'
    return 'medium'


def _cap(rule_id):
    r = BY_ID[rule_id]
    return {'id': r['capability'], 'autonomy': r['autonomy']}


def _finding(rule_id, entity, ends_on, severity, evidence, sentence, stake, confidence, money_reason=None, brain_refs=()):
    out = {'id': f'{SCREEN}.{rule_id}.{entity["id"]}', 'screen': SCREEN, 'rule_id': rule_id, 'severity': severity,
           'entity': entity, 'evidence': evidence, 'sentence': sentence, 'capability': _cap(rule_id),
           'money_at_stake': stake, 'confidence': confidence, 'brain_refs': list(brain_refs),
           'first_seen': ends_on.isoformat(), 'last_seen': ends_on.isoformat(), 'status': 'open', 'unavailable': None}
    if stake is None:
        out['money_reason'] = money_reason or 'no baseline'
    return out


def _unavailable(rule_id, ends_on, sentence=None, connector=None, fix=None, label='Organic content'):
    rule = BY_ID[rule_id]
    base = UNAVAILABLE.get(rule_id, (None, None, None))
    return {'id': f'{SCREEN}.{rule_id}.brand', 'screen': SCREEN, 'rule_id': rule_id, 'severity': rule['severity'],
            'entity': {'type': 'brand', 'id': 'brand', 'label': label}, 'evidence': [],
            'sentence': sentence or base[0], 'capability': _cap(rule_id), 'money_at_stake': None,
            'confidence': 0.1, 'brain_refs': [],
            'first_seen': ends_on.isoformat(), 'last_seen': ends_on.isoformat(), 'status': 'unavailable',
            'unavailable': {'inputs': list(rule['inputs']), 'connector': connector or base[1], 'fix': fix or base[2]},
            'money_reason': 'inputs unavailable'}


def next_moment(ends_on):
    """The first US moment within HOLIDAY_DAYS after the window end, as (date, name, days away), else None."""
    for d, name in US_MOMENTS:
        days = (date.fromisoformat(d) - ends_on).days
        if 0 < days <= HOLIDAY_DAYS:
            return d, name, days
    return None


def holiday_finding(rd):
    """ORG-R02. The holiday list is known; scripts are not, so a near moment makes an unavailable finding."""
    near = next_moment(rd.ends_on)
    if near is None:
        return []  # no moment within 14 days: nothing to say
    d, name, days = near
    return [_unavailable('ORG-R02', rd.ends_on,
                         f'{name} is in {days} days. No content calendar is connected, so its script cannot be checked.',
                         'content calendar export', 'Connect the content calendar with a script per holiday slot.')]


def broad_low_value(posts, ends_on):
    """ORG-R05 over the 30-day window: top quartile by views, matched orders under ORDERS_FLOOR each."""
    rows = [p for p in posts if p.get('views') is not None and p.get('matched_orders') is not None]
    if len(rows) < 4:
        return []
    ranked = sorted(rows, key=lambda p: (-p['views'], p['date'], p['platform']))
    top = ranked[:max(1, round(len(ranked) * TOP_QUARTILE))]
    low = [p for p in top if p['matched_orders'] < ORDERS_FLOOR]
    if not low:
        return []
    views = sum(p['views'] for p in low)
    orders = sum(p['matched_orders'] for p in low)
    w = f'{POST_WINDOW}d'
    evidence = [_ev('top_quartile_posts', len(top), 'count', ends_on, w),
                _ev('posts_under_floor', len(low), 'count', ends_on, w),
                _ev('views', views, 'count', ends_on, w),
                _ev('matched_orders', orders, 'count', ends_on, w, ORDERS_FLOOR, 'threshold')]
    evidence += [dict(_ev('post_matched_orders', p['matched_orders'], 'count', ends_on, w, ORDERS_FLOOR, 'threshold'),
                      post=post_label(p), views=p['views']) for p in low]
    sentence = (f'{len(low)} of the top {len(top)} posts by views in 30 days sold under {ORDERS_FLOOR} orders each. '
                f'They reached {views:,} views and matched {orders} orders.')
    return [_finding('ORG-R05', {'type': 'metric', 'id': 'top_reach_posts', 'label': 'Top quartile posts by views, 30 days'},
                     ends_on, 'medium', evidence, sentence, None, 0.5,
                     'no baseline: the orders floor is a rule default until the brand sets one')]


def stranger_blind(posts, ends_on):
    """ORG-R04 when posts carry sku_tag and cta_tag: top 3 by views in 30 days with neither tag."""
    rows = sorted((p for p in posts if p.get('views') is not None), key=lambda p: (-p['views'], p['date'], p['platform']))
    out = []
    for p in rows[:3]:
        if p.get('sku_tag') or p.get('cta_tag'):
            continue
        evidence = [dict(_ev('views', p['views'], 'count', ends_on, f'{POST_WINDOW}d'), post=post_label(p))]
        sentence = f'{post_label(p)} got {p["views"]:,} views but named no product and gave no next step.'
        out.append(_finding('ORG-R04', {'type': 'metric', 'id': f'post_{p["platform"]}_{p["date"]}', 'label': post_label(p)},
                            ends_on, 'medium', evidence, sentence, None, 0.5, 'no baseline: no order-matched value for an untagged post'))
    return out


def founder_share(posts, ends_on, target):
    """ORG-R15 when posts are tagged: founder_on_camera share over 30 days above the brain's target (0 to 1)."""
    tagged = [p for p in posts if p.get('founder_on_camera') is not None]
    goal = target.get('value')
    if not tagged or not isinstance(goal, (int, float)):
        return []
    share = round(sum(1 for p in tagged if p['founder_on_camera']) / len(tagged), 4)
    if share <= goal:
        return []
    evidence = [_ev('founder_camera_share', share, 'ratio', ends_on, f'{POST_WINDOW}d', goal, 'threshold'),
                _ev('posts', len(tagged), 'count', ends_on, f'{POST_WINDOW}d')]
    sentence = f'{round(share * 100)} percent of posts need the founder on camera, above the {round(goal * 100)} percent plan.'
    return [_finding('ORG-R15', {'type': 'metric', 'id': 'founder_camera_share', 'label': 'Founder on camera share'},
                     ends_on, 'low', evidence, sentence, None, 0.5, 'no money formula yet', [target['id']])]


def hook_findings(rd, net_28d):
    """ORG-R16: hooks under 0.75 x the median hook's orders per 1,000 views, 90 days, checked against the 90 days before."""
    ends_on = rd.ends_on
    now = hook_rates(rd.posts(HOOK_WINDOW))
    prev = hook_rates(rd.posts(HOOK_WINDOW, ends_on - timedelta(days=HOOK_WINDOW)))
    ok = {k: v for k, v in now.items() if v['posts'] >= HOOK_MIN_POSTS and v['per_1k'] is not None}
    if len(ok) < 3:
        return []
    med = round(statistics.median(v['per_1k'] for v in ok.values()), 4)
    prev_ok = {k: v for k, v in prev.items() if v['posts'] >= HOOK_MIN_POSTS and v['per_1k'] is not None}
    prev_med = statistics.median(v['per_1k'] for v in prev_ok.values()) if len(prev_ok) >= 3 else None
    aov = rd.aov(HOOK_WINDOW)
    w = f'{HOOK_WINDOW}d'
    out = []
    for hook in sorted(ok):
        h = ok[hook]
        if h['per_1k'] >= HOOK_RATE_X * med:
            continue
        agree = 1 + (1 if prev_med is not None and hook in prev_ok and prev_ok[hook]['per_1k'] < HOOK_RATE_X * prev_med else 0)
        if aov is None:
            stake, reason = None, 'aov unavailable for the window'
        else:
            usd = round(max((med - h['per_1k']) / 1000 * h['views'] * aov, 0))
            stake, reason = {'usd': usd, 'formula': '(median_orders_per_1k - hook_orders_per_1k) / 1000 * hook_views * aov_90d',
                             'inputs': {'median_orders_per_1k': med, 'hook_orders_per_1k': h['per_1k'],
                                        'hook_views': h['views'], 'aov_90d': aov}, 'window': w}, None
        evidence = [_ev('orders_per_1k_views', h['per_1k'], 'ratio', ends_on, w, med, 'own_median'),
                    _ev('posts', h['posts'], 'count', ends_on, w), _ev('views', h['views'], 'count', ends_on, w),
                    _ev('matched_orders', h['orders'], 'count', ends_on, w)]
        if aov is not None:
            evidence.append(_ev('aov', aov, 'usd', ends_on, w, source='daily'))
        if agree >= 2:
            evidence.append(_ev('orders_per_1k_views_prior', prev_ok[hook]['per_1k'], 'ratio', ends_on - timedelta(days=HOOK_WINDOW),
                                w, round(prev_med, 4), 'own_median'))
        sentence = (f'{hook} posts matched {h["per_1k"]:.2f} orders per 1,000 views over 90 days. '
                    f'The median hook matched {med:.2f}, across {h["posts"]} posts and {h["views"]:,} views.')
        usd = stake['usd'] if stake else None
        out.append(_finding('ORG-R16', {'type': 'metric', 'id': 'hook_' + hook.lower().replace(' ', '_'),
                                        'label': f'{hook} hook, orders per 1,000 views'},
                            ends_on, _severity(usd, net_28d, agree), evidence, sentence, stake, _confidence(agree), reason))
    return out


def run(brand, window=None, data=None):
    """Findings for one brand and window ({ends_on, days, trailing}), sorted by severity then stake."""
    data = data if data is not None else (brand_data(brand) if brand else None)
    ends_on = date.fromisoformat(window['ends_on']) if window and window.get('ends_on') else last_full_day(data, brand)
    rd = Reader(data, brand, ends_on)
    market = (rd.source.brand or {}).get('market') or 'US'
    out = [_unavailable('ORG-R01', ends_on)]
    out += holiday_finding(rd)
    if market == 'IN':
        out.append(_unavailable('ORG-R03', ends_on, 'No festive calendar layer is loaded, so festival slots cannot be checked.',
                                'content calendar export', 'Load the India festival layer into the calendar.'))
    cols = rd.columns()
    posts30 = rd.posts(POST_WINDOW)
    if posts30 is None:
        for rid in ('ORG-R04', 'ORG-R05', 'ORG-R16'):
            out.append(_unavailable(rid, ends_on, 'No post export is connected, so post results are unavailable.',
                                    'platform insights (Instagram, TikTok, YouTube)', 'Connect the social accounts read only.'))
    else:
        if not {'sku_tag', 'cta_tag'} <= cols:
            out.append(_unavailable('ORG-R04', ends_on))
        else:
            out += stranger_blind(posts30, ends_on)
        out += broad_low_value(posts30, ends_on)
        mer = rd.m('aov', SESSION_WINDOW)
        net_28d = (mer.get('inputs') or {}).get('net_revenue') if not mer.get('unavailable') else None
        out += hook_findings(rd, net_28d)
    for rid in ('ORG-R06', 'ORG-R07', 'ORG-R08', 'ORG-R09', 'ORG-R10', 'ORG-R11', 'ORG-R12', 'ORG-R13', 'ORG-R14'):
        out.append(_unavailable(rid, ends_on))
    target = next((r for r in brain_records(brand, 'content', ends_on) if r.get('field') == 'founder_camera_target'), None)
    if 'founder_on_camera' not in cols or target is None or posts30 is None:
        out.append(_unavailable('ORG-R15', ends_on))
    else:
        out += founder_share(posts30, ends_on, target)
    out.sort(key=lambda f: (SEVERITY_ORDER[f['severity']], f['status'] == 'unavailable',
                            -((f['money_at_stake'] or {}).get('usd') or 0), f['id']))
    return out
