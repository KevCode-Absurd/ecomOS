"""Wild bets and PR API: /api/27-wild-bets-pr/...

  GET overview?brand=bombas   tiles, insights, chart, bet queue, launches, story bank dating, moment
                              calendar, room metrics with their sources, actions, findings
  GET findings?brand=bombas   the audit findings only (audit.py, contract shape)

Traffic numbers come from app/metrics.py (session_funnel by channel group): direct plus referral visits
are the PR proxy until a press log exists. Stories, milestones, frames and launches come from the brand
brain (app/brain/store.py). The bet queue and the moment calendar are this screen's simulated fixtures.
Insights are rules in `insights()`, each with the sentence it produces and the capability it maps to.
Missing is unavailable, never 0. Default brand is bombas (simulated tables, public brain). Read-only.
"""
import importlib.util
import re
import statistics
from datetime import timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _audit():
    spec = importlib.util.spec_from_file_location('wild_bets_audit', HERE / 'audit.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


audit = _audit()
DEFAULT_BRAND = 'bombas'
STAGES = ['idea', 'bounded', 'executing', 'at read point', 'scaled', 'killed']
TRAILING = 4
CHART_WEEKS = 56
SPIKE_X = 1.5  # a week of earned visits at this multiple of its own 4-week median reads as a spike
STORY_HOOKS = ('giving story', 'founder story')
READINESS_DAYS = 60

# Room actions from the room spec (label, capability, autonomy as the catalogue sets it).
ACTIONS = [
    ('Log a new wild bet idea', 'BRAND-C44', 'agent_does'),
    ('Approve the bound and move to executing', 'BRAND-C45', 'founder_gate'),
    ('Approve the execution brief', 'BRAND-C46', 'founder_gate'),
    ('Pull the read point result', 'REG-C02', 'agent_does'),
    ('Approve a PR angle to pitch', 'BRAND-C40', 'human_assist'),
    ('Build the media list for a story', 'BRAND-C53', 'agent_does'),
    ('Source new partnership candidates', 'BRAND-C70', 'agent_does'),
    ('Run reputation check on a partner', 'BRAND-C71', 'human_assist'),
]

# The room metrics that have no source yet: plain words, the table that fills them, the reason.
NOT_CONNECTED = [
    ('bet_read_point_lift', 'Lift over control at the read point', 'bet_read_points', 'no bet has reached its read point'),
    ('pr_coverage_count', 'Press placements landed', 'pr_coverage', 'no media monitoring connected'),
    ('media_list_coverage', 'Verified contacts matched to the story', 'media_list', 'no media list built yet'),
    ('partnership_pipeline_count', 'Partner candidates by stage', 'partnership_pipeline', 'pipeline is empty'),
    ('partnership_reputation_flags', 'Open partner reputation flags', 'partnership_pipeline', 'no check has run'),
    ('ambassador_active_count', 'Active ambassadors', 'ambassador_program', 'no program set up'),
    ('ambassador_content_approval_rate', 'Ambassador content passed', 'ambassador_program', 'no submissions'),
    ('referral_order_share', 'Orders from a referral', 'orders.referral_code', 'no referral tracking set up'),
    ('event_attendance', 'People at the last event', 'events_and_popups', 'no event has run'),
    ('award_submission_status', 'Awards tracked, submitted or won', 'award_tracking', 'no awards tracked yet'),
    ('reputation_alert_count', 'Open reputation alerts', 'reputation_monitor_feed', 'no listening connector attached'),
]


def _tile(name, plain, value, unit, **extra):
    out = {'name': name, 'plain': plain, 'unit': unit, 'value': value}
    out.update(extra)
    return out


def _unavail(name, plain, unit, reason, fix):
    return _tile(name, plain, None, unit, unavailable_reason=reason, fix=fix)


def source_of(data, brand):
    return audit.brand_data(brand) if brand else data


# ---------------------------------------------------------------- traffic

def earned_windows(data, brand, days, ends_on, n):
    """n consecutive windows of `days` ending on ends_on, newest first; None where unavailable."""
    return [audit.earned_sessions(data, brand, days, ends_on - timedelta(days=days * k)) for k in range(n)]


# ---------------------------------------------------------------- bets

def bet_rows(queue, br, ends_on):
    rows = []
    for b in queue:
        claims = []
        for rid in b.get('claim_refs') or []:
            rec = br.get(rid) if br else None
            claims.append({'id': rid, 'tier': rec.get('tier', 'unverified') if rec else None,
                           'text': rec.get('text') if rec else None})
        n = audit.days_in_stage(b, ends_on)
        rows.append({'bet_id': b['bet_id'], 'title': b['title'], 'idea': b['idea'], 'stage': b['stage'],
                     'days_in_stage': n, 'planned_stage_days': b.get('planned_stage_days'),
                     'overdue': bool(b.get('planned_stage_days')) and n > b['planned_stage_days'],
                     'bound_filled': audit.bound_filled(b) if b['stage'] != 'idea' else None,
                     'bound_total': len(audit.BOUND_FIELDS), 'budget_cap_usd': b.get('budget_cap_usd'),
                     'read_point_date': b.get('read_point_date'), 'metric': b['metric'],
                     'brain_ref': b['brain_ref'], 'counters_frame': b.get('counters_frame'), 'claims': claims,
                     'ties_ok': not audit.bet_check(b, br), 'simulated': True})
    return rows


def by_stage(queue):
    counts = {s: 0 for s in STAGES}
    for b in queue:
        counts[b['stage']] = counts.get(b['stage'], 0) + 1
    return counts


# ---------------------------------------------------------------- tiles

def tiles(queue, weeks28, ends_on):
    st = by_stage(queue)
    parts = [f'{v} {k}' for k, v in st.items() if v]
    bets = _tile('Wild bets in the queue', 'Bets by stage: ' + ', '.join(parts) + '. Simulated queue.', len(queue), 'n',
                 window='current', tone=None)
    now, prior = weeks28[0], weeks28[1:]
    plain = 'Direct and referral visits in the last 28 days, the PR proxy until a press log exists.'
    if now is None or any(p is None for p in prior):
        earned = _unavail('Direct and referral visits', plain, 'n', 'sessions are not connected', 'ga4')
    else:
        med = statistics.median(p['total'] for p in prior)
        earned = _tile('Direct and referral visits', plain + f' Own median of the {TRAILING} windows before: {round(med):,}.',
                       now['total'], 'n', delta=round(now['total'] / med - 1, 4) if med else None,
                       delta_label=f'vs own median of {TRAILING} prior 28-day windows', window=f'28 days to {ends_on}',
                       freshness=ends_on.isoformat(), sources=[{'table': 'sessions'}])
    press = _unavail('Press placements, 28 days', 'Confirmed press placements landed. Source: media coverage log.', 'n',
                     'no media monitoring connected', 'media monitoring feed')
    return {'bets': bets, 'earned': earned, 'press': press}


# ---------------------------------------------------------------- insights

def insights(weeks7, posts, ends_on):
    """The rules behind the insight cards. Each returns the sentence it produces and its capability."""
    out = []
    rule = (f'direct plus referral visits in the last 7 days at {SPIKE_X:g}x or more of the median of the '
            f'{TRAILING} weeks before reads as a press or word-of-mouth spike')
    now, prior = weeks7[0], weeks7[1:TRAILING + 1]
    if now is None or any(p is None for p in prior):
        out.append({'id': 'earned_spike', 'severity': 'info', 'capability': None, 'autonomy': None, 'rule': rule,
                    'sentence': 'Sessions are not connected, so a press spike cannot be seen.'})
    else:
        med = statistics.median(p['total'] for p in prior)
        x = round(now['total'] / med, 2) if med else None
        if x is not None and x >= SPIKE_X:
            out.append({'id': 'earned_spike', 'severity': 'medium', 'capability': 'BRAND-C40', 'autonomy': 'human_assist',
                        'rule': rule, 'sentence': f'Direct and referral visits jumped to {now["total"]:,} last week, '
                                                  f'{x}x the {round(med):,} weekly median.'})
        else:
            out.append({'id': 'earned_spike', 'severity': 'info', 'capability': 'BRAND-C40', 'autonomy': 'human_assist',
                        'rule': rule, 'sentence': f'Direct and referral visits were {now["total"]:,} last week, {x}x the '
                                                  f'{round(med):,} weekly median. No press spike shows.'})
    rule = (f'matched orders per 1,000 views on giving and founder story posts against all other posts, last '
            f'{audit.AD_DAYS} days')
    if posts is None:
        out.append({'id': 'story_posts', 'severity': 'info', 'capability': None, 'autonomy': None, 'rule': rule,
                    'sentence': 'Social posts are not connected, so story formats cannot be compared.'})
    else:
        start = (ends_on - timedelta(days=audit.AD_DAYS - 1)).isoformat()
        cur = [p for p in posts if start <= str(p.get('date')) <= ends_on.isoformat()]
        story = [p for p in cur if str(p.get('hook') or '').lower() in STORY_HOOKS]
        other = [p for p in cur if p not in story]

        def rate(ps):
            views = sum(p.get('views') or 0 for p in ps)
            return round(sum(p.get('matched_orders') or 0 for p in ps) / views * 1000, 3) if views else None

        a, b = rate(story), rate(other)
        if a is None or b is None:
            out.append({'id': 'story_posts', 'severity': 'info', 'capability': None, 'autonomy': None, 'rule': rule,
                        'sentence': 'Too few posts in the window to compare story formats.'})
        else:
            word = 'more' if a > b else 'fewer'
            out.append({'id': 'story_posts', 'severity': 'medium' if a > b else 'info', 'capability': 'BRAND-C40',
                        'autonomy': 'human_assist', 'rule': rule,
                        'sentence': f'{len(story)} giving and founder story posts drew {a} matched orders per 1,000 views, '
                                    f'{word} than the {b} for {len(other)} other posts.'
                        if a > b else
                                    f'{len(story)} giving and founder story posts drew {a} matched orders per 1,000 views, '
                                    f'against {b} for {len(other)} other posts.'})
    return out


# ---------------------------------------------------------------- chart

def chart(data, brand, ends_on):
    wins = earned_windows(data, brand, 7, ends_on, CHART_WEEKS)[::-1]
    labels = [(ends_on - timedelta(days=7 * k)).isoformat() for k in range(CHART_WEEKS)][::-1]
    if all(w is None for w in wins):
        return {'unavailable': True, 'reason': 'sessions are not connected', 'fix': 'ga4'}
    series = [{'name': c, 'values': [w[c] if w else None for w in wins]} for c in audit.EARNED_CHANNELS]
    return {'labels': labels, 'series': series, 'window': f'{CHART_WEEKS} weeks to {ends_on}', 'unit': 'n'}


# ---------------------------------------------------------------- tables

def launch_rows(data, brand, br):
    out = []
    first = audit._sessions_first(data, brand)
    for d, rec in audit.launches(br) if br else []:
        v = rec.get('value') or {}
        label = f'{v["city"]} store opening' if v.get('city') else ' and '.join(v.get('partners') or []) + ' rollout'
        row = {'launch': label, 'date': d.isoformat(), 'brain_ref': rec['id'], 'press_logged': None,
               'share_after': None, 'share_before': None, 'lift': None}
        base_start = d - timedelta(days=audit.LAUNCH_DAYS * audit.LAUNCH_TRAILING)
        if first and base_start >= first:
            after = audit.earned_sessions(data, brand, audit.LAUNCH_DAYS, d + timedelta(days=audit.LAUNCH_DAYS - 1))
            prior = [audit.earned_sessions(data, brand, audit.LAUNCH_DAYS, d - timedelta(days=1 + audit.LAUNCH_DAYS * k))
                     for k in range(audit.LAUNCH_TRAILING)]
            if after and all(prior):
                base = statistics.median(p['share'] for p in prior)
                row.update(share_after=round(after['share'], 4), share_before=round(base, 4),
                           lift=round(after['share'] / base, 2) if base else None)
        out.append(row)
    return out


def story_rows(br):
    if br is None:
        return {'unavailable': True, 'rows': []}
    undated = {r['id'] for r in audit.undated_stories(br)}
    rows = [{'id': r['id'], 'text': r.get('text'), 'tier': r.get('tier'), 'source_type': (r.get('source') or {}).get('type'),
             'captured_at': (r.get('source') or {}).get('captured_at'), 'dated': r['id'] not in undated}
            for r in br.records('story_bank')]
    return {'unavailable': False, 'rows': rows, 'dated': sum(1 for r in rows if r['dated']), 'total': len(rows)}


def calendar(br, ends_on):
    rows = audit.calendar_moments(br, ends_on)
    soon = [m for m in rows if m['days_away'] <= READINESS_DAYS]
    ready = {'value': round(sum(1 for m in soon if m.get('brief_id')) / len(soon), 4) if soon else None,
             'moments': len(soon), 'window': f'next {READINESS_DAYS} days',
             'unavailable_reason': None if soon else 'calendar has no entries in that window'}
    return {'rows': rows, 'readiness': ready, 'simulated': True}


def room_metrics(queue):
    st = by_stage(queue)
    staged = [b for b in queue if b['stage'] != 'idea']
    out = [{'name': 'active_bets_by_stage', 'plain': 'Bets in each stage', 'value': st, 'source': 'fixtures/wild_bets.json',
            'simulated': True},
           {'name': 'bet_bound_completeness', 'plain': 'Bound fields filled, bets past idea',
            'value': {b['bet_id']: f'{audit.bound_filled(b)} of 8' for b in staged} or None,
            'source': 'fixtures/wild_bets.json', 'simulated': True}]
    for name, plain, table, reason in NOT_CONNECTED:
        out.append({'name': name, 'plain': plain, 'value': None, 'source': table, 'unavailable_reason': reason})
    return out


# ---------------------------------------------------------------- overview

def overview(data, brand):
    ends_on = audit.last_full_day(data, brand)
    src = source_of(data, brand)
    b = src.brand
    head = {'brand': b.get('brand'), 'name': b.get('name'), 'as_of': b.get('as_of'),
            'simulated': bool(b.get('simulated') or b.get('fictional')), 'market': b.get('market')}
    br = audit.brain(brand, today=ends_on) if brand else None
    queue = audit.bets()
    weeks7 = earned_windows(data, brand, 7, ends_on, TRAILING + 1)
    weeks28 = earned_windows(data, brand, 28, ends_on, TRAILING + 1)
    posts = audit._table(src, 'content_posts')
    findings = audit.run(brand, {'ends_on': ends_on.isoformat()}, data=data)
    launches = launch_rows(data, brand, br)
    ch = chart(data, brand, ends_on)
    if not ch.get('unavailable'):
        ch['note'] = 'Weeks end on the date shown. Launches from the brain: ' + (
            '; '.join(f'{r["launch"]} {r["date"]}' for r in launches) or 'none on file') + '.'
    return {'brand': head, 'window': {'ends_on': ends_on.isoformat()},
            'tiles': tiles(queue, weeks28, ends_on), 'insights': insights(weeks7, posts, ends_on),
            'chart': ch, 'bets': bet_rows(queue, br, ends_on), 'stages': STAGES,
            'bound_fields': audit.BOUND_FIELDS, 'launches': launches, 'stories': story_rows(br),
            'calendar': calendar(br, ends_on), 'metrics': room_metrics(queue),
            'actions': [{'label': l, 'capability': c, 'autonomy': a} for l, c, a in ACTIONS],
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
