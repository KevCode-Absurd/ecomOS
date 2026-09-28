"""Wild bets and PR audit (screen 27, round 0). Findings in the shape of app/contracts/audit.md.

Inputs: the brand brain (story_bank, identity, channels, calendar, positioning, competitors, claims,
learnings) through app/brain/store.py; GA4 sessions by channel group through app/metrics.py
(session_funnel) as the PR proxy (direct plus referral visits); ad_rows and content_posts for what
the brand said in the last 90 days; and this screen's fixtures: the simulated wild bet queue
(fixtures/wild_bets.json) and the US moment calendar (fixtures/holiday_calendar.json). No connector,
no model call. Same tables, same brain, same window: same findings, byte for byte.

Most PR numbers have no source yet (press log, media list, listening feed, partner pipeline,
ambassador table, award tracker). Rules on those emit one finding with status unavailable that names
the table and the connector. Never a 0.

Rules (owner of every rule: 27-wild-bets-pr)
  WILD-R01  Story fact with no dated source: a story_bank record whose value carries no date of its
            own (date, year, year_reached, as_of, since). The capture date is when we read it, not
            when it happened, so a journalist cannot use it. Money: none. Low. BRAND-C40.
  WILD-R02  Mission milestone unused: the largest donation count in the brain (story_bank
            mission_proof_* and identity records with items_donated or donations_total) is not named
            in any ad body or title, or any content post hook, in the last 90 days. Money: none, earned
            reach has no dollar value in the data. Medium. BRAND-C40.
  WILD-R03  Competitor-owned frame with no bet: a Reddit frame in positioning with 3 or more mentions,
            none naming the brand, that a competitor is recommended instead on (FRAME_OWNER), and no bet
            in the queue lists it in counters_frame. Money: none. Medium. BRAND-C44.
  WILD-R04  Retail launch with no PR record: a dated retail or partner launch in the brain calendar
            inside the sessions window, with no row in the press log and direct plus referral visits in
            the 14 days after, as a share of all visits, under 1.2x the median share of the 4 prior 14-day
            windows. Share, not count, so the fall season ramp does not read as press. Money: (median share
            minus share after) x all sessions after x session value (GA4 conversion_rate x aov) when the share
            fell, else none. Medium. BRAND-C40.
  WILD-R05  Bet bound incomplete: a bet at bounded or executing with fewer than 8 of 8 bound fields.
            Money: the bet's budget cap, which would go live unbounded. Medium. BRAND-C45.
  WILD-R06  Bet claim not backed: a bet whose brain_ref is missing from the brain, whose claim_refs are
            not tier approved or site_backed, or whose metric is not a room metric. Money: none. High.
            BRAND-C45.
  WILD-R07  Bet overdue at its stage (spec): days in stage over the bet's own planned days. Money:
            budget cap / planned days x days over, capped at the budget cap. Medium. BRAND-C45.
  WILD-R08  Bet shows no lift at its read point (spec): needs bet_read_points. High. REG-C02.
  WILD-R09  Bet shows a real lift (spec): needs bet_read_points. Low (spec says informational). REG-C02.
  WILD-R10  Reputation risk building (spec): needs reputation_monitor_feed. High. BRAND-C54.
  WILD-R11  Media list going stale (spec): needs media_list. Medium. BRAND-C53.
  WILD-R12  Moment coming up with no brief (spec): a high or medium relevance moment within 30 days
            with no brief_id, from the calendar fixture plus store anniversaries from the brain
            calendar. Money: none. Medium. LOOP-C05.
  WILD-R13  Partnership candidate flagged (spec): needs partnership_pipeline. High. BRAND-C71.
  WILD-R14  Ambassador content waiting too long (spec): needs ambassador_program. Low. BRAND-C55.
  WILD-R15  Award deadline close, nothing started (spec): needs award_tracking. Low. BRAND-C61.
"""
import importlib.util
import json
import re
import statistics
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parents[1]
SCREEN = '27-wild-bets-pr'

AD_DAYS = 90
LAUNCH_DAYS = 14
LAUNCH_TRAILING = 4
LAUNCH_LIFT = 1.2
FRAME_MIN_MENTIONS = 3
BRIEF_DAYS = 30
BRIEF_RELEVANCE = ('high', 'medium')
BOUND_FIELDS = ['budget_cap_usd', 'downside_limit', 'control_design', 'cohort', 'stop_rule', 'read_point_date',
                'legal_review_status', 'bound']
BACKED_TIERS = ('approved', 'site_backed')
EARNED_CHANNELS = ('Direct', 'Referral')
DATE_KEYS = ('date', 'year', 'year_reached', 'as_of', 'since')
# A frame counts as owned when Reddit recommends a competitor instead on it.
FRAME_OWNER = {'buy_it_for_life': 'reddit_recommended_darn_tough', 'worth_the_price': 'reddit_recommended_kirkland'}
ROOM_METRICS = ['active_bets_by_stage', 'bet_bound_completeness', 'bet_read_point_lift', 'bet_cycle_time_days',
                'pr_coverage_count', 'media_list_coverage', 'partnership_pipeline_count',
                'partnership_reputation_flags', 'ambassador_active_count', 'ambassador_content_approval_rate',
                'referral_order_share', 'event_attendance', 'award_submission_status', 'reputation_alert_count',
                'holiday_calendar_readiness']

CAPABILITY = {
    'WILD-R01': {'id': 'BRAND-C40', 'autonomy': 'human_assist'},
    'WILD-R02': {'id': 'BRAND-C40', 'autonomy': 'human_assist'},
    'WILD-R03': {'id': 'BRAND-C44', 'autonomy': 'agent_does'},
    'WILD-R04': {'id': 'BRAND-C40', 'autonomy': 'human_assist'},
    'WILD-R05': {'id': 'BRAND-C45', 'autonomy': 'founder_gate'},
    'WILD-R06': {'id': 'BRAND-C45', 'autonomy': 'founder_gate'},
    'WILD-R07': {'id': 'BRAND-C45', 'autonomy': 'founder_gate'},
    'WILD-R08': {'id': 'REG-C02', 'autonomy': 'agent_does'},
    'WILD-R09': {'id': 'REG-C02', 'autonomy': 'agent_does'},
    'WILD-R10': {'id': 'BRAND-C54', 'autonomy': 'founder_gate'},
    'WILD-R11': {'id': 'BRAND-C53', 'autonomy': 'agent_does'},
    'WILD-R12': {'id': 'LOOP-C05', 'autonomy': 'founder_gate'},
    'WILD-R13': {'id': 'BRAND-C71', 'autonomy': 'human_assist'},
    'WILD-R14': {'id': 'BRAND-C55', 'autonomy': 'founder_gate'},
    'WILD-R15': {'id': 'BRAND-C61', 'autonomy': 'human_assist'},
}
_R = [
    ('WILD-R01', 'Story fact with no date of its own', 'metric', ['brain.story_bank']),
    ('WILD-R02', 'Largest mission milestone not named in 90 days of ads or posts', 'metric',
     ['brain.story_bank', 'brain.identity', 'ad_rows', 'content_posts']),
    ('WILD-R03', 'Competitor-owned frame with no bet against it', 'metric',
     ['brain.positioning', 'brain.competitors', 'fixtures/wild_bets.json']),
    ('WILD-R04', 'Retail launch with no press record and no earned traffic lift', 'stage',
     ['brain.calendar', 'sessions', 'pr_coverage']),
    ('WILD-R05', 'Bet at bounded or executing with fewer than 8 of 8 bound fields', 'offer', ['fixtures/wild_bets.json']),
    ('WILD-R06', 'Bet claim not tier approved or site_backed, or bet not tied to the brain', 'offer',
     ['fixtures/wild_bets.json', 'brain.claims', 'brain.identity']),
    ('WILD-R07', 'Bet has sat in its stage past its own plan', 'offer', ['fixtures/wild_bets.json']),
    ('WILD-R08', 'Bet shows no lift over control at its read point', 'offer', ['bet_read_points']),
    ('WILD-R09', 'Bet beat its control by more than its own bar', 'offer', ['bet_read_points']),
    ('WILD-R10', 'Mentions jumped over 2x the trailing average with a negative tilt', 'brand', ['reputation_monitor_feed']),
    ('WILD-R11', 'Contacts on the current media list need a re-check', 'metric', ['media_list']),
    ('WILD-R12', 'Moment within 30 days with no brief', 'metric', ['fixtures/holiday_calendar.json', 'brain.calendar']),
    ('WILD-R13', 'Partnership candidate with an open reputation flag', 'brand', ['partnership_pipeline']),
    ('WILD-R14', 'Ambassador submissions past the review deadline', 'metric', ['ambassador_program']),
    ('WILD-R15', 'Eligible award deadline within 21 days, nothing submitted', 'metric', ['award_tracking']),
]
RULES = [{'rule_id': r, 'name': n, 'entity_type': t, 'inputs': i, 'capability': CAPABILITY[r]['id'],
          'owner_screen': SCREEN} for r, n, t, i in _R]
SEVERITY_ORDER = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}

# Spec rules whose table has no source yet: severity, the sentence, the connector and the fix.
MISSING = {
    'WILD-R08': ('high', 'bet_read_points', 'experiment registry',
                 'No bet has a read point log yet, so no lift against control can be read.',
                 'Log each bet read in the experiment registry at its read point date.'),
    'WILD-R09': ('low', 'bet_read_points', 'experiment registry',
                 'No bet has a read point log yet, so no win against control can be read.',
                 'Log each bet read in the experiment registry at its read point date.'),
    'WILD-R10': ('high', 'reputation_monitor_feed', 'social listening',
                 'No listening feed is connected, so a spike in brand mentions cannot be seen.',
                 'Connect a social listening or review feed (read only).'),
    'WILD-R11': ('medium', 'media_list', 'media list build',
                 'No media list is built for any story yet, so stale contacts cannot be counted.',
                 'Build a media list for the next story or launch.'),
    'WILD-R13': ('high', 'partnership_pipeline', 'partnership pipeline',
                 'No partnership pipeline is on file, so partner reputation flags cannot be read.',
                 'Start the partnership pipeline with the candidates on the table now.'),
    'WILD-R14': ('low', 'ambassador_program', 'ambassador program table',
                 'No ambassador program is set up, so late reviews cannot be counted.',
                 'Set up the ambassador program table.'),
    'WILD-R15': ('low', 'award_tracking', 'award tracker',
                 'No awards are tracked yet, so close deadlines cannot be seen.',
                 'List the awards and best-of lists the brand is eligible for.'),
}

_MODS = {}


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def metrics():
    if 'metrics' not in _MODS:
        _MODS['metrics'] = _load('ecomos_metrics_wild', APP / 'metrics.py')
    return _MODS['metrics']


def brand_data(brand):
    if 'tables' not in _MODS:
        _MODS['tables'] = _load('ecomos_tables_wild', APP / 'data' / 'tables.py')
    return _MODS['tables'].brand_data(brand)


def brain(brand, today=None):
    """The brand's brain store, or None when the brand has no brain folder."""
    import sys
    if str(APP / 'brain') not in sys.path:
        sys.path.insert(0, str(APP / 'brain'))
    import store
    if not brand or not (APP / 'brain' / str(brand)).is_dir():
        return None
    return store.Brain(brand, today=today)


def fixture(name):
    return json.loads((HERE / 'fixtures' / name).read_text(encoding='utf-8'))


def last_full_day(data, brand):
    source = brand_data(brand) if brand else data
    return date.fromisoformat(source.brand['as_of'])


def key(rid):
    return rid.split('.', 2)[-1]


def _table(data, name):
    try:
        return data.table(name)
    except (KeyError, ValueError):
        return None


def _m(data, brand, name, days, end, **kw):
    q = {'window': f'{days}d', 'end': end.isoformat(), **kw}
    if brand:
        q['brand'] = brand
    return metrics().compute(name, data, **q)


def earned_sessions(data, brand, days, end):
    """Direct and referral sessions for the window ending `end`: {Direct, Referral, total, all, share}, or None."""
    r = _m(data, brand, 'session_funnel', days, end, by='channel_group')
    if r.get('unavailable'):
        return None
    by = {g['channel_group']: g['sessions'] for g in r.get('groups') or []}
    out = {c: by.get(c, 0) for c in EARNED_CHANNELS}
    out['total'] = sum(out[c] for c in EARNED_CHANNELS)
    out['all'] = r['value']
    out['share'] = out['total'] / r['value'] if r['value'] else None
    return out


def session_value(data, brand, end):
    """GA4 conversion rate x aov for the 28 days to `end`, with inputs, or None. The conversion rate comes
    from the same sessions table as the earned share, so both sides of the stake share one scale."""
    f = _m(data, brand, 'session_funnel', 28, end)
    a = _m(data, brand, 'aov', 28, end)
    cr = (f.get('rates') or {}).get('conversion_rate') if not f.get('unavailable') else None
    if cr is None or a.get('unavailable') or a.get('value') is None:
        return None
    return {'value': round(cr * a['value'], 4), 'conversion_rate': cr, 'aov': a['value']}


def net_28d(data, brand, end):
    r = _m(data, brand, 'aov', 28, end)
    return (r.get('inputs') or {}).get('net_revenue') if not r.get('unavailable') else None


# ---------------------------------------------------------------- shared shapes

def _ev(metric, value, unit, ends_on, window, baseline=None, baseline_kind=None, source='brain', simulated=True,
        freshness_days=1, **extra):
    out = {'metric': metric, 'value': value, 'unit': unit, 'window': window, 'ends_on': ends_on,
           'freshness_days': freshness_days, 'baseline': baseline, 'baseline_kind': baseline_kind, 'source': source,
           'simulated': simulated}
    out.update(extra)
    return out


def _finding(rule_id, entity, ends_on, severity, evidence, sentence, stake, confidence, brain_refs=(), money_reason=None):
    out = {'id': f'{SCREEN}.{rule_id}.{entity["id"]}', 'screen': SCREEN, 'rule_id': rule_id, 'severity': severity,
           'entity': entity, 'evidence': evidence, 'sentence': sentence, 'capability': dict(CAPABILITY[rule_id]),
           'money_at_stake': stake, 'confidence': confidence, 'brain_refs': list(brain_refs),
           'first_seen': ends_on.isoformat(), 'last_seen': ends_on.isoformat(), 'status': 'open', 'unavailable': None}
    if stake is None:
        out['money_reason'] = money_reason or 'no baseline'
    return out


def _unavailable(rule_id, ends_on, severity, reason, inputs, connector, fix):
    return {'id': f'{SCREEN}.{rule_id}.brand', 'screen': SCREEN, 'rule_id': rule_id, 'severity': severity,
            'entity': {'type': 'brand', 'id': 'brand', 'label': 'Wild bets and PR'}, 'evidence': [],
            'sentence': reason, 'capability': dict(CAPABILITY[rule_id]), 'money_at_stake': None,
            'money_reason': 'inputs unavailable', 'confidence': 0.1, 'brain_refs': [],
            'first_seen': ends_on.isoformat(), 'last_seen': ends_on.isoformat(), 'status': 'unavailable',
            'unavailable': {'inputs': inputs, 'connector': connector, 'fix': fix}}


def slug(text):
    return re.sub(r'[^a-z0-9]+', '-', str(text).lower()).strip('-')


def _ago(br, rec):
    """Freshness in days of a brain record against the brain's today (0 when captured on or after it)."""
    return max(rec.get('age_days') or 0, 0) if rec.get('age_days') is not None else None


def _day(d):
    return f'{d.day} {d.strftime("%b")}'


# ---------------------------------------------------------------- brain readers

def undated_stories(br):
    """story_bank records whose value names no date of its own."""
    out = []
    for rec in br.records('story_bank'):
        v = rec.get('value')
        if isinstance(v, dict) and any(v.get(k) for k in DATE_KEYS):
            continue
        out.append(rec)
    return out


def milestones(br):
    """Donation count records, largest first: (count, record)."""
    out = []
    for section in ('story_bank', 'identity'):
        for rec in br.records(section):
            v = rec.get('value')
            if isinstance(v, dict):
                n = v.get('items_donated') or v.get('donations_total')
                if isinstance(n, (int, float)):
                    out.append((n, rec))
    out.sort(key=lambda t: (-t[0], t[1]['id']))
    return out


def milestone_patterns(n):
    """Ways a count is written: 200 million, 200M, 200,000,000, 200000000."""
    m = n / 1_000_000
    word = f'{m:g}'
    return [f'{word} million', f'{word}m', f'{int(n):,}', str(int(n))]


def mentions(texts, pats):
    return sum(1 for t in texts if t and any(p in str(t).lower() for p in pats))


def launches(br):
    """Dated retail and partner launches from the brain calendar: (date, record)."""
    out = []
    for rec in br.records('calendar'):
        v = rec.get('value') or {}
        k = key(rec['id'])
        if not isinstance(v, dict) or not (k.startswith('flagship_store') or v.get('partners')):
            continue
        d = v.get('date') or (v.get('month') and v['month'] + '-01') or (v.get('start_month') and v['start_month'] + '-01')
        if d:
            out.append((date.fromisoformat(d), rec))
    out.sort(key=lambda t: (t[0], t[1]['id']))
    return out


def anniversaries(br, ends_on, horizon=90):
    """Brain calendar launches with a day-exact date whose anniversary falls in the next `horizon` days."""
    out = []
    for rec in br.records('calendar'):
        v = rec.get('value') or {}
        k = key(rec['id'])
        if not isinstance(v, dict) or not k.startswith('flagship_store') or not v.get('date'):
            continue
        d = date.fromisoformat(v['date'])
        nxt = d.replace(year=ends_on.year)
        if nxt <= ends_on:
            nxt = d.replace(year=ends_on.year + 1)
        if (nxt - ends_on).days <= horizon:
            years = nxt.year - d.year
            out.append({'moment': f'{v.get("city")} store {years}-year mark', 'date': nxt.isoformat(),
                        'relevance': 'medium', 'why': 'store anniversary', 'brief_id': None, 'brain_ref': rec['id']})
    return out


def calendar_moments(br, ends_on, horizon=90):
    cal = fixture('holiday_calendar.json')
    rows = [dict(m) for m in cal['moments']] + (anniversaries(br, ends_on, horizon) if br else [])
    for m in rows:
        m['days_away'] = (date.fromisoformat(m['date']) - ends_on).days
    rows = [m for m in rows if 0 <= m['days_away'] <= horizon]
    rows.sort(key=lambda m: (m['date'], m['moment']))
    return rows


def bets():
    return fixture('wild_bets.json')['bets']


def bound_filled(bet):
    return sum(1 for f in BOUND_FIELDS if bet.get(f) not in (None, ''))


def days_in_stage(bet, ends_on):
    return (ends_on - date.fromisoformat(bet['stage_entered'])).days


def bet_check(bet, br):
    """What is wrong with a bet's ties to the brain: a list of plain reasons (empty when sound)."""
    bad = []
    if br is None or br.get(bet.get('brain_ref') or '') is None:
        bad.append(f'brain record {bet.get("brain_ref")} is not in the brain')
    for rid in bet.get('claim_refs') or []:
        rec = br.get(rid) if br else None
        if rec is None:
            bad.append(f'claim {rid} is not in the brain')
        elif rec.get('tier', 'unverified') not in BACKED_TIERS:
            bad.append(f'claim {rid} is tier {rec.get("tier", "unverified")}')
    if not bet.get('claim_refs'):
        bad.append('no claim record named')
    if bet.get('metric') not in ROOM_METRICS:
        bad.append(f'metric {bet.get("metric")} is not a room metric')
    return bad


# ---------------------------------------------------------------- rules

def r01(br, ends_on):
    out = []
    recs = br.records('story_bank')
    for rec in undated_stories(br):
        k = key(rec['id'])
        ev = [_ev('fact_date', None, 'date', ends_on.isoformat(), 'record', source='brain.story_bank', simulated=False,
                  freshness_days=_ago(br, rec), captured_at=(rec.get('source') or {}).get('captured_at'),
                  source_type=(rec.get('source') or {}).get('type')),
              _ev('story_records', len(recs), 'count', ends_on.isoformat(), 'current', source='brain.story_bank',
                  simulated=False)]
        label = k.replace('_', ' ')
        out.append(_finding('WILD-R01', {'type': 'metric', 'id': slug(k), 'label': f'Story: {label}'}, ends_on, 'low', ev,
                            f'The story "{label}" has no date of its own, only the day it was read. '
                            f'A journalist cannot check when it happened.',
                            None, 0.5, [rec['id']], money_reason='a story fact has no dollar value'))
    return out


def r02(data, br, ends_on):
    ms = milestones(br)
    if not ms:
        return [_unavailable('WILD-R02', ends_on, 'medium', 'No donation milestone is in the brain, so its use in ads cannot be read.',
                             ['brain.story_bank', 'brain.identity'], 'brand brain', 'Add the donation count to the brain.')]
    ads, posts = _table(data, 'ad_rows'), _table(data, 'content_posts')
    if ads is None and posts is None:
        return [_unavailable('WILD-R02', ends_on, 'medium', 'Ads and posts are not connected, so milestone use cannot be read.',
                             ['ad_rows', 'content_posts'], 'meta, instagram, tiktok', 'Connect Meta ads and social posts (read only).')]
    n, rec = ms[0]
    start = (ends_on - timedelta(days=AD_DAYS - 1)).isoformat()
    end = ends_on.isoformat()
    pats = milestone_patterns(n)
    win = f'{AD_DAYS}d'
    ev, said = [], 0
    ad_count = post_count = giving = None
    if ads is not None:
        cur = [a for a in ads if start <= str(a.get('date')) <= end]
        texts = {}
        for a in cur:
            texts.setdefault(a.get('ad_id'), ' '.join(str(a.get(f) or '') for f in ('body', 'title')))
        ad_count = len(texts)
        hit = mentions(texts.values(), pats)
        said += hit
        ev += [_ev('ads_live', ad_count, 'count', end, win, source='ad_rows'),
               _ev('ads_naming_milestone', hit, 'count', end, win, source='ad_rows')]
    if posts is not None:
        cur = [p for p in posts if start <= str(p.get('date')) <= end]
        post_count = len(cur)
        hit = mentions([p.get('hook') for p in cur], pats)
        giving = sum(1 for p in cur if 'giving' in str(p.get('hook') or '').lower())
        said += hit
        ev += [_ev('posts', post_count, 'count', end, win, source='content_posts'),
               _ev('posts_naming_milestone', hit, 'count', end, win, source='content_posts'),
               _ev('giving_story_posts', giving, 'count', end, win, source='content_posts')]
    if said:
        return []
    ev.insert(0, _ev('largest_milestone', n, 'items', end, 'record', source=f'brain.{rec["section"]}', simulated=False,
                     freshness_days=_ago(br, rec), tier=rec.get('tier')))
    refs = [rec['id']]
    live = br.get(f'{br.brand}.story_bank.mission_line_in_ads')
    if live:
        refs.append(live['id'])
    words = f'{n / 1_000_000:g} million'
    s = f'The {words} donations milestone is in 0 of {ad_count if ad_count is not None else "unavailable"} ads and 0 of ' \
        f'{post_count if post_count is not None else "unavailable"} posts in the last {AD_DAYS} days.'
    if giving:
        s += f' {giving} giving story posts ran without it.'
    return [_finding('WILD-R02', {'type': 'metric', 'id': f'milestone-{int(n)}', 'label': f'{words} donations'}, ends_on,
                     'medium', ev, s, None, 0.5, refs, money_reason='earned reach has no dollar value in the data')]


def r03(br, ends_on, queue):
    out = []
    countered = {b.get('counters_frame') for b in queue if b.get('stage') != 'killed'}
    for rec in br.records('positioning'):
        v = rec.get('value')
        if not isinstance(v, dict) or not key(rec['id']).startswith('reddit_frame_'):
            continue
        frame = v.get('frame')
        owner_key = FRAME_OWNER.get(frame)
        owner = br.get(f'{br.brand}.competitors.{owner_key}') if owner_key else None
        if (v.get('mentions') or 0) < FRAME_MIN_MENTIONS or v.get('mentions_brand') or owner is None or frame in countered:
            continue
        ov = owner.get('value') or {}
        ev = [_ev('frame_mentions', v.get('mentions'), 'count', ends_on.isoformat(), 'capture', source='brain.positioning',
                  simulated=False, freshness_days=_ago(br, rec)),
              _ev('frame_mentions_brand', v.get('mentions_brand'), 'count', ends_on.isoformat(), 'capture',
                  source='brain.positioning', simulated=False, freshness_days=_ago(br, rec)),
              _ev('recommended_instead', ov.get('recommended_instead'), 'count', ends_on.isoformat(), 'capture',
                  source='brain.competitors', simulated=False, freshness_days=_ago(br, owner),
                  competitor=ov.get('competitor'), upvotes=ov.get('upvotes')),
              _ev('bets_against_frame', 0, 'count', ends_on.isoformat(), 'current', source='fixtures/wild_bets.json')]
        words = frame.replace('_', ' ')
        out.append(_finding('WILD-R03', {'type': 'metric', 'id': f'frame-{slug(frame)}', 'label': f'Frame: {words}'}, ends_on,
                            'medium', ev,
                            f'"{words.capitalize()}" comes up in {v.get("mentions")} Reddit threads and 0 name the brand. '
                            f'{ov.get("competitor")} is recommended instead {ov.get("recommended_instead")} times, and no bet '
                            f'in the queue takes it on.',
                            None, 0.5, [rec['id'], owner['id'], f'{br.brand}.positioning.competitive_frame'],
                            money_reason='a frame has no dollar value until a bet reads against control'))
    return out


def r04(data, brand, br, ends_on):
    out = []
    fr = _m(data, brand, 'session_funnel', 7, ends_on)
    if fr.get('unavailable'):
        return [_unavailable('WILD-R04', ends_on, 'medium', 'Sessions are not connected, so launch traffic cannot be read.',
                             ['sessions'], 'ga4', 'Connect GA4 (read only).')]
    first_day = _sessions_first(data, brand)
    press = _table(data, 'pr_coverage')
    for d, rec in launches(br):
        after_end = d + timedelta(days=LAUNCH_DAYS - 1)
        base_start = d - timedelta(days=LAUNCH_DAYS * LAUNCH_TRAILING)
        if first_day is None or base_start < first_day or after_end > ends_on:
            continue
        logged = [p for p in press or [] if p.get('story') and slug(key(rec['id'])) in slug(p['story'])]
        if logged:
            continue
        after = earned_sessions(data, brand, LAUNCH_DAYS, after_end)
        prior = [earned_sessions(data, brand, LAUNCH_DAYS, d - timedelta(days=1 + LAUNCH_DAYS * k))
                 for k in range(LAUNCH_TRAILING)]
        if after is None or any(p is None or not p['all'] for p in prior) or not after['all']:
            continue
        base = statistics.median(p['share'] for p in prior)
        ratio = round(after['share'] / base, 2) if base else None
        if ratio is not None and ratio >= LAUNCH_LIFT:
            continue
        win = f'{LAUNCH_DAYS}d'
        ev = [_ev('earned_share', round(after['share'], 4), 'share', after_end.isoformat(), win, round(base, 4),
                  'own_median', source='sessions', direct=after['Direct'], referral=after['Referral'],
                  sessions=after['all']),
              _ev('lift_vs_prior', ratio, 'x', after_end.isoformat(), win, LAUNCH_LIFT, 'threshold', source='sessions'),
              _ev('pr_coverage_count', None, 'count', after_end.isoformat(), win, source='pr_coverage',
                  unavailable='no media monitoring connected' if press is None else None)]
        stake, reason = None, 'earned share at or above its pre-launch median; no loss to count'
        if after['share'] < base:
            sv = session_value(data, brand, after_end)
            if sv is None:
                reason = 'session value unavailable'
            else:
                lost = (base - after['share']) * after['all']
                stake = {'usd': round(lost * sv['value']),
                         'formula': '(median_prior_share - share_after) * sessions_after * conversion_rate * aov',
                         'inputs': {'median_prior_share': round(base, 4), 'share_after': round(after['share'], 4),
                                    'sessions_after': after['all'], 'conversion_rate': sv['conversion_rate'], 'aov': sv['aov']},
                         'window': win}
        v = rec.get('value') or {}
        label = (f'{v["city"]} store opening' if v.get('city') else
                 ' and '.join(v.get('partners') or []) + ' rollout')
        when = f'on {_day(d)} {d.year}' if v.get('date') else d.strftime('in %B %Y')
        s = (f'No press placement is logged for the {label} {when}. Direct and referral visits were '
             f'{after["share"] * 100:.1f} percent of all visits in the {LAUNCH_DAYS} days after, against '
             f'{base * 100:.1f} percent before.')
        out.append(_finding('WILD-R04', {'type': 'stage', 'id': slug(key(rec['id'])), 'label': label}, ends_on, 'medium', ev,
                            s, stake, 0.7, [rec['id']], money_reason=reason))
    return out


def _sessions_first(data, brand):
    """The first day the sessions table covers, from the metric layer's own window check."""
    source = brand_data(brand) if brand else data
    try:
        rows = source.table('sessions')
    except (KeyError, ValueError):
        return None
    ds = [r['date'] for r in rows if r.get('date')]
    return date.fromisoformat(min(ds)) if ds else None


def r05_r07(queue, ends_on):
    out = []
    for b in queue:
        ent = {'type': 'offer', 'id': slug(b['bet_id']), 'label': f'{b["bet_id"]} {b["title"]}'}
        cap = b.get('budget_cap_usd')
        filled = bound_filled(b)
        if b['stage'] in ('bounded', 'executing') and filled < len(BOUND_FIELDS):
            missing = [f for f in BOUND_FIELDS if b.get(f) in (None, '')]
            ev = [_ev('bet_bound_completeness', filled, 'fields', ends_on.isoformat(), 'current', len(BOUND_FIELDS),
                      'threshold', source='fixtures/wild_bets.json', missing=missing)]
            stake = None if cap is None else {'usd': cap, 'formula': 'budget_cap_usd', 'inputs': {'budget_cap_usd': cap},
                                              'window': 'bet'}
            out.append(_finding('WILD-R05', ent, ends_on, 'medium', ev,
                                f'{b["bet_id"]} is at {b["stage"]} with {filled} of 8 bound fields. Missing: '
                                f'{", ".join(m.replace("_", " ") for m in missing)}.',
                                stake, 0.9, [b['brain_ref']], money_reason='no budget cap set'))
        n = days_in_stage(b, ends_on)
        plan = b.get('planned_stage_days')
        if plan and n > plan and b['stage'] not in ('scaled', 'killed'):
            over = n - plan
            ev = [_ev('bet_cycle_time_days', n, 'days', ends_on.isoformat(), 'current', plan, 'threshold',
                      source='fixtures/wild_bets.json', stage_entered=b['stage_entered'])]
            stake = None
            if cap:
                usd = round(min(cap, cap / plan * over))
                stake = {'usd': usd, 'formula': 'min(budget_cap_usd, budget_cap_usd / planned_stage_days * days_over)',
                         'inputs': {'budget_cap_usd': cap, 'planned_stage_days': plan, 'days_over': over}, 'window': 'bet'}
            out.append(_finding('WILD-R07', ent, ends_on, 'medium', ev,
                                f'{b["bet_id"]} has sat in {b["stage"]} for {n} days, past its own plan of {plan}.',
                                stake, 0.9, [b['brain_ref']], money_reason='no budget cap set'))
    return out


def r06(queue, br, ends_on):
    out = []
    for b in queue:
        bad = bet_check(b, br)
        if not bad:
            continue
        ev = [_ev('bet_ties_failed', len(bad), 'count', ends_on.isoformat(), 'current', 0, 'threshold',
                  source='fixtures/wild_bets.json', reasons=bad)]
        out.append(_finding('WILD-R06', {'type': 'offer', 'id': slug(b['bet_id']), 'label': f'{b["bet_id"]} {b["title"]}'},
                            ends_on, 'high', ev, f'{b["bet_id"]} leans on something the brain does not back: {bad[0]}.',
                            None, 0.9, [r for r in [b.get('brain_ref')] + list(b.get('claim_refs') or []) if r],
                            money_reason='a claim risk has no dollar value'))
    return out


def r12(br, ends_on):
    out = []
    for m in calendar_moments(br, ends_on):
        if m['days_away'] > BRIEF_DAYS or m.get('brief_id') or m['relevance'] not in BRIEF_RELEVANCE:
            continue
        ev = [_ev('days_away', m['days_away'], 'days', ends_on.isoformat(), 'current', BRIEF_DAYS, 'threshold',
                  source='fixtures/holiday_calendar.json' if not m.get('brain_ref') else 'brain.calendar',
                  moment_date=m['date'], relevance=m['relevance']),
              _ev('brief_linked', False, 'flag', ends_on.isoformat(), 'current', source='fixtures/holiday_calendar.json')]
        refs = [m['brain_ref']] if m.get('brain_ref') else []
        out.append(_finding('WILD-R12', {'type': 'metric', 'id': f'moment-{slug(m["moment"])}', 'label': m['moment']},
                            ends_on, 'medium', ev, f'{m["moment"]} is {m["days_away"]} days away with no brief started.',
                            None, 0.9, refs, money_reason='a calendar moment has no baseline to count against'))
    return out


def run(brand, window=None, data=None):
    """Findings for one brand and window ({ends_on, days, trailing}), sorted by severity then stake."""
    data = data if data is not None else (brand_data(brand) if brand else None)
    ends_on = date.fromisoformat(window['ends_on']) if window and window.get('ends_on') else last_full_day(data, brand)
    br = brain(brand, today=ends_on) if brand else None
    queue = bets()
    out = []
    if br is None:
        for r in ('WILD-R01', 'WILD-R02', 'WILD-R03', 'WILD-R04'):
            out.append(_unavailable(r, ends_on, 'low' if r == 'WILD-R01' else 'medium',
                                    'No brand brain is on file, so stories, milestones, frames and launches cannot be read.',
                                    ['brain'], 'brand brain', 'Build the brand brain for this brand.'))
    else:
        out += r01(br, ends_on)
        out += r02(data, br, ends_on)
        out += r03(br, ends_on, queue)
        out += r04(data, brand, br, ends_on)
    out += r05_r07(queue, ends_on)
    out += r06(queue, br, ends_on)
    out += r12(br, ends_on)
    for rid, (sev, table, conn, reason, fix) in MISSING.items():
        if _table(data, table) is None:
            out.append(_unavailable(rid, ends_on, sev, reason, [table], conn, fix))
    out.sort(key=lambda f: (SEVERITY_ORDER[f['severity']], -((f['money_at_stake'] or {}).get('usd') or 0), f['id']))
    return out
