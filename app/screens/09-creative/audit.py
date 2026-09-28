"""Creative audit (screen 09, round 0). Findings in the shape of app/contracts/audit.md.

Every number comes from app/metrics.py (Meta ad-level rows, `ad_rows`) and the brand brain
(`app/brain/<brand>/`). No connector, no model call. Same tables, brain and window give the same
findings, byte for byte.

Rules (one per room job that the data can answer; the JTBD table in FEATURES.md maps the rest)
  CREA-R01  Format below its own median: a format (image, video, carousel) with 28-day platform ROAS
            10 percent or more under the median of its 4 trailing 28-day windows, and at least 5 percent
            of Meta spend. Money: spend_28d x (roas_median_4w - roas_28d), the purchase value the format
            would have returned at its own median. Capability CREA-C16 (agent does). Owner: 09-creative.
  CREA-R02  Starved winner: an ad live 14 days or more with 28-day ROAS at least 1.25 x the account's
            Meta ROAS, 5 or more purchases, and under 2 percent of Meta spend. It is under-tested, not
            worn out. Money: null ("no baseline": the return on extra spend is not measured yet).
            Capability CREA-C15 (agent does). Owner: 09-creative. Fatigue itself (CTR down, frequency up)
            is PAID-R03, owned by 11-paid-social; this screen reads it from the findings table.
  CREA-R03  Hook and angle tags: `ad_rows` carries no hook type or angle tag, so winners cannot be split
            by hook or angle. Unavailable until tags exist. Capability CREA-C03 (agent does).
  CREA-R04  Hook rate: 3-second video plays over impressions for video ads with 500 or more impressions,
            under 0.75 x the account median of video ads. Unavailable when `ad_rows` has no 3-second
            play column. Capability CREA-C04 (agent does). Money: null ("no baseline").
  CREA-R05  New ad volume: ads with a first spend day in the last 28 days, 25 percent or more under the
            median of the 4 trailing 28-day windows. Money: null ("no money formula yet").
            Capability CREA-C18 (agent does). Owner: 09-creative.
  CREA-R06  Competitor format gap: a format that 3 or more competitors run on over 20 percent of their
            Ad Library ads, with no own ad in that format in the trailing 90 days. Reads brain
            `learnings` records with role competitor. Signal only, never proof. Money: null
            ("signal only"). Capability LOOP-C13 (agent does). Owner: 09-creative.
"""
import importlib.util
import statistics
import sys
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parents[1]
SCREEN = '09-creative'

WINDOW = 28
TRAILING = 4
FORMAT_DROP = 0.10
FORMAT_MIN_SHARE = 0.05
STARVED_ROAS_X = 1.25
STARVED_MAX_SHARE = 0.02
STARVED_MIN_PURCHASES = 5
STARVED_MIN_DAYS = 14
HOOK_RATE_X = 0.75
HOOK_MIN_IMPRESSIONS = 500
VOLUME_DROP = 0.25
GAP_MIN_COMPETITORS = 3
GAP_MIN_SHARE = 0.20
GAP_OWN_DAYS = 90
HOOK_TAG_COLUMNS = ('hook_type', 'angle', 'angle_tag', 'hook_tag')
HOOK_PLAY_COLUMNS = ('video_3s', 'video_3s_plays', 'video_play_3s')

RULES = [
    {'rule_id': 'CREA-R01', 'name': 'Format ROAS 10 percent under its own 4-window median', 'entity_type': 'metric',
     'inputs': ['ad_rows'], 'capability': 'CREA-C16', 'owner_screen': SCREEN},
    {'rule_id': 'CREA-R02', 'name': 'Winning ad starved of spend', 'entity_type': 'ad',
     'inputs': ['ad_rows'], 'capability': 'CREA-C15', 'owner_screen': SCREEN},
    {'rule_id': 'CREA-R03', 'name': 'No hook or angle tag on ads', 'entity_type': 'brand',
     'inputs': ['ad_rows.hook_type', 'ad_rows.angle'], 'capability': 'CREA-C03', 'owner_screen': SCREEN},
    {'rule_id': 'CREA-R04', 'name': 'Video hook rate under 0.75 x the account median', 'entity_type': 'ad',
     'inputs': ['ad_rows.video_3s'], 'capability': 'CREA-C04', 'owner_screen': SCREEN},
    {'rule_id': 'CREA-R05', 'name': 'New ads launched 25 percent under the 4-window median', 'entity_type': 'brand',
     'inputs': ['ad_rows'], 'capability': 'CREA-C18', 'owner_screen': SCREEN},
    {'rule_id': 'CREA-R06', 'name': 'Format 3 competitors run at volume and we do not', 'entity_type': 'metric',
     'inputs': ['brain.learnings (Ad Library format counts)', 'ad_rows'], 'capability': 'LOOP-C13',
     'owner_screen': SCREEN},
]
CAPABILITY = {r['rule_id']: {'id': r['capability'], 'autonomy': 'agent_does'} for r in RULES}
SEVERITY_ORDER = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}

_MODS = {}


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def metrics():
    if 'metrics' not in _MODS:
        _MODS['metrics'] = _load('ecomos_metrics_creative', APP / 'metrics.py')
    return _MODS['metrics']


def brand_data(brand):
    if 'tables' not in _MODS:
        _MODS['tables'] = _load('ecomos_tables_creative', APP / 'data' / 'tables.py')
    return _MODS['tables'].brand_data(brand)


def brain_records(brand, section, today):
    """Brain records for one section, or [] when the brand has no brain."""
    if not brand or not (APP / 'brain' / brand).is_dir():
        return []
    if 'brain' not in _MODS:
        if str(APP / 'brain') not in sys.path:
            sys.path.insert(0, str(APP / 'brain'))  # store.py imports its sibling validate.py
        _MODS['brain'] = _load('ecomos_brain_creative', APP / 'brain' / 'store.py')
    return _MODS['brain'].Brain(brand, today=today).records(section)


class Reader:
    """One brand, one window end. m(name, days, end, **kw) is metrics.compute with brand and end filled in."""

    def __init__(self, data, brand, ends_on):
        self.data, self.brand, self.ends_on = data, brand, ends_on
        self.source = data if data is not None else brand_data(brand)

    def m(self, name, days, end=None, **kw):
        q = {'window': f'{days}d', 'end': (end or self.ends_on).isoformat(), **kw}
        if self.brand:
            q['brand'] = self.brand
        return metrics().compute(name, self.data, **q)

    def ads(self, days=WINDOW, end=None):
        r = self.m('spend', days, end, channel='meta', by='ad')
        return r, ({g['ad']: g for g in r['groups']} if not r.get('unavailable') else {})

    def columns(self):
        try:
            rows = self.source.table('ad_rows')
        except (KeyError, ValueError):
            return set()
        return set(rows[0]) if rows else set()


def last_full_day(data, brand):
    source = brand_data(brand) if brand else data
    return date.fromisoformat(source.brand['as_of'])


def _roas(spend, value):
    return round(value / spend, 4) if spend else None


def format_windows(rd, weeks=TRAILING + 1):
    """Per format: spend, purchase value, ROAS and ad count for the current 28 days and the 4 before, newest first."""
    out = []
    for k in range(weeks):
        _, ads = rd.ads(WINDOW, rd.ends_on - timedelta(days=WINDOW * k))
        by = {}
        for ad in ads.values():
            f = by.setdefault(ad.get('format') or 'unknown', {'spend': 0.0, 'purchase_value': 0.0, 'ads': 0})
            f['spend'] += ad['spend']
            f['purchase_value'] += ad['purchase_value']
            f['ads'] += 1
        for f in by.values():
            f['spend'] = round(f['spend'], 2)
            f['purchase_value'] = round(f['purchase_value'], 2)
            f['roas'] = _roas(f['spend'], f['purchase_value'])
        out.append(by)
    return out


def launches(rd, weeks=TRAILING + 1):
    """New ads per 28-day window (first spend day inside it), newest first. First day read over the 400 days the metric layer allows."""
    r, ads = rd.ads(400)
    counts = []
    for k in range(weeks):
        end = rd.ends_on - timedelta(days=WINDOW * k)
        start = end - timedelta(days=WINDOW - 1)
        counts.append(sum(1 for a in ads.values() if a.get('first_day') and start.isoformat() <= a['first_day'] <= end.isoformat()))
    return counts, (r.get('window') or {})


def _ev(metric, value, unit, ends_on, baseline=None, baseline_kind=None, window=f'{WINDOW}d', source='ad_rows'):
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


def _finding(rule_id, entity, ends_on, severity, evidence, sentence, stake, confidence, money_reason=None, brain_refs=()):
    out = {'id': f'{SCREEN}.{rule_id}.{entity["id"]}', 'screen': SCREEN, 'rule_id': rule_id, 'severity': severity,
           'entity': entity, 'evidence': evidence, 'sentence': sentence, 'capability': dict(CAPABILITY[rule_id]),
           'money_at_stake': stake, 'confidence': confidence, 'brain_refs': list(brain_refs),
           'first_seen': ends_on.isoformat(), 'last_seen': ends_on.isoformat(), 'status': 'open', 'unavailable': None}
    if stake is None:
        out['money_reason'] = money_reason or 'no baseline'
    return out


def _unavailable(rule_id, ends_on, severity, sentence, inputs, connector, fix):
    return {'id': f'{SCREEN}.{rule_id}.brand', 'screen': SCREEN, 'rule_id': rule_id, 'severity': severity,
            'entity': {'type': 'brand', 'id': 'brand', 'label': 'Meta account'}, 'evidence': [], 'sentence': sentence,
            'capability': dict(CAPABILITY[rule_id]), 'money_at_stake': None, 'money_reason': 'inputs unavailable',
            'confidence': 0.1, 'brain_refs': [], 'first_seen': ends_on.isoformat(), 'last_seen': ends_on.isoformat(),
            'status': 'unavailable', 'unavailable': {'inputs': inputs, 'connector': connector, 'fix': fix}}


def format_findings(fw, ends_on, net_28d):
    now, out = fw[0], []
    total = sum(f['spend'] for f in now.values())
    for name in sorted(now):
        f = now[name]
        past = [w[name]['roas'] for w in fw[1:] if name in w and w[name]['roas'] is not None]
        if f['roas'] is None or len(past) < TRAILING or not total or f['spend'] / total < FORMAT_MIN_SHARE:
            continue
        base = round(statistics.median(past), 4)
        if f['roas'] > base * (1 - FORMAT_DROP):
            continue
        usd = round(max(f['spend'] * (base - f['roas']), 0))
        stake = {'usd': usd, 'formula': 'spend_28d * (roas_median_4w - roas_28d)',
                 'inputs': {'spend_28d': f['spend'], 'roas_28d': f['roas'], 'roas_median_4w': base}, 'window': f'{WINDOW}d'}
        agree = 1 + (1 if fw[1].get(name, {}).get('roas') is not None and fw[1][name]['roas'] < base else 0)
        drop = round((1 - f['roas'] / base) * 100)
        evidence = [_ev('platform_roas', f['roas'], 'x', ends_on, base, 'own_median'),
                    _ev('spend', f['spend'], 'usd', ends_on),
                    _ev('spend_share', round(f['spend'] / total, 4), 'ratio', ends_on, FORMAT_MIN_SHARE, 'threshold'),
                    _ev('ads', f['ads'], 'count', ends_on)]
        sentence = (f'{name.capitalize()} ads returned {f["roas"]:.2f}x on ${f["spend"]:,.0f} in 28 days. '
                    f'Their own median is {base:.2f}x, {drop} percent higher.')
        out.append(_finding('CREA-R01', {'type': 'metric', 'id': f'format_{name}', 'label': f'{name.capitalize()} ads, platform ROAS'},
                            ends_on, _severity(usd, net_28d, agree), evidence, sentence, stake, _confidence(agree)))
    return out


def starved_findings(ads, ends_on, account_roas):
    total = sum(a['spend'] for a in ads.values())
    if not total or account_roas is None:
        return []
    out = []
    first_ok = (ends_on - timedelta(days=STARVED_MIN_DAYS - 1)).isoformat()
    for ad_id in sorted(ads):
        a = ads[ad_id]
        share = a['spend'] / total
        if (a['roas'] is None or a['roas'] < STARVED_ROAS_X * account_roas or share >= STARVED_MAX_SHARE
                or (a.get('purchases') or 0) < STARVED_MIN_PURCHASES or not a.get('first_day') or a['first_day'] > first_ok
                or a.get('last_day', '') < ends_on.isoformat()):
            continue
        evidence = [_ev('platform_roas', a['roas'], 'x', ends_on, account_roas, 'threshold'),
                    _ev('spend_share', round(share, 4), 'ratio', ends_on, STARVED_MAX_SHARE, 'threshold'),
                    _ev('spend', a['spend'], 'usd', ends_on), _ev('purchases', a['purchases'], 'count', ends_on)]
        sentence = (f'{ad_id} returned {a["roas"]:.2f}x in 28 days against {account_roas:.2f}x for the account. '
                    f'It got {share * 100:.1f} percent of spend, ${a["spend"]:,.0f}.')
        label = f'{ad_id} ({a.get("format") or "ad"}, {a.get("campaign_name") or a.get("campaign_id")})'
        f = _finding('CREA-R02', {'type': 'ad', 'id': ad_id, 'label': label}, ends_on, 'medium', evidence, sentence,
                     None, 0.5, 'no baseline: the return on extra spend is not measured yet')
        if a.get('dynamic_creative'):
            f['flags'] = ['dynamic creative: mixed assets, read as one ad']
        out.append(f)
    return out


def hook_rate_findings(rows, ads, ends_on, col):
    """CREA-R04 when a 3-second play column exists. rows are raw ad_rows inside the 28-day window."""
    plays, imps = {}, {}
    for r in rows:
        if r.get('format') != 'video' or r.get(col) is None:
            continue
        plays[r['ad_id']] = plays.get(r['ad_id'], 0) + r[col]
        imps[r['ad_id']] = imps.get(r['ad_id'], 0) + (r.get('impressions') or 0)
    rates = {a: round(plays[a] / imps[a], 4) for a in plays if imps[a] >= HOOK_MIN_IMPRESSIONS}
    if len(rates) < 3:
        return []
    med = round(statistics.median(rates.values()), 4)
    out = []
    for a in sorted(rates):
        if rates[a] >= HOOK_RATE_X * med:
            continue
        evidence = [_ev('hook_rate', rates[a], 'ratio', ends_on, med, 'own_median'),
                    _ev('impressions', imps[a], 'count', ends_on)]
        sentence = (f'{a} stops {rates[a] * 100:.1f} percent of viewers in 3 seconds. '
                    f'The median video ad stops {med * 100:.1f} percent.')
        out.append(_finding('CREA-R04', {'type': 'ad', 'id': a, 'label': a}, ends_on, 'medium', evidence, sentence,
                            None, 0.5))
    return out


def volume_findings(counts, ends_on):
    now, past = counts[0], counts[1:]
    if len(past) < TRAILING:
        return []
    base = statistics.median(past)
    if not base or now > base * (1 - VOLUME_DROP):
        return []
    agree = 1 + (1 if past[0] < base else 0)
    evidence = [_ev('new_ads', now, 'count', ends_on, base, 'own_median'),
                _ev('new_ads_prior_windows', past, 'count', ends_on, window=f'{WINDOW * TRAILING}d')]
    sentence = (f'{now} new ads started spending in the last 28 days. '
                f'The median for the 4 windows before was {base:g}.')
    return [_finding('CREA-R05', {'type': 'brand', 'id': 'new_ads', 'label': 'New ads launched'}, ends_on,
                     'high' if agree >= 2 else 'medium', evidence, sentence, None, _confidence(agree),
                     'no money formula yet')]


def own_formats(ads):
    """Formats our own account ran, with dynamic creative read as dco and catalog campaigns as dpa."""
    out = set()
    for a in ads.values():
        out.add(a.get('format') or 'unknown')
        if a.get('dynamic_creative'):
            out.add('dco')
        name = (a.get('campaign_name') or '').lower()
        if 'catalog' in name or 'dpa' in name or 'advantage+ catalog' in name:
            out.add('dpa')
    return out


def gap_findings(records, own, ends_on):
    comp = [r for r in records if isinstance(r.get('value'), dict) and r['value'].get('role') == 'competitor'
            and isinstance(r['value'].get('formats'), dict)]
    counts, refs = {}, {}
    for r in comp:
        fm = r['value']['formats']
        total = sum(v for v in fm.values() if isinstance(v, (int, float)))
        for name, n in fm.items():
            if total and n / total > GAP_MIN_SHARE:
                counts.setdefault(name, []).append((r['value'].get('page'), round(n / total, 4)))
                refs.setdefault(name, []).append(r['id'])
    out = []
    for name in sorted(counts):
        pages = counts[name]
        if len(pages) < GAP_MIN_COMPETITORS or name in own:
            continue
        evidence = [dict(_ev('competitor_share', share, 'ratio', ends_on, GAP_MIN_SHARE, 'threshold', window='latest pull',
                             source='brain.learnings'), competitor=page) for page, share in pages]
        evidence.append(_ev('own_ads_in_format', 0, 'count', ends_on, window=f'{GAP_OWN_DAYS}d'))
        sentence = (f'{len(pages)} competitors run {name} on over {round(GAP_MIN_SHARE * 100)} percent of their ads. '
                    f'We ran no {name} ad in 90 days.')
        out.append(_finding('CREA-R06', {'type': 'metric', 'id': f'gap_{name}', 'label': f'{name} format gap'}, ends_on,
                            'low', evidence, sentence, None, _confidence(1, peer=True), 'signal only, not a proven winner',
                            refs[name]))
    return out


def run(brand, window=None, data=None):
    """Findings for one brand and window ({ends_on, days, trailing}), sorted by severity then stake."""
    data = data if data is not None else (brand_data(brand) if brand else None)
    ends_on = date.fromisoformat(window['ends_on']) if window and window.get('ends_on') else last_full_day(data, brand)
    rd = Reader(data, brand, ends_on)
    first, ads = rd.ads(WINDOW)
    if first.get('unavailable'):
        fix = 'Connect the Meta ad account (read only).'
        return [_unavailable(r, ends_on, 'high' if r in ('CREA-R01', 'CREA-R05') else 'medium',
                             'Meta ad rows are not connected, so creative rules cannot run.', ['ad_rows'],
                             first.get('fix') or 'meta_ads', fix) for r in ('CREA-R01', 'CREA-R02', 'CREA-R05')]
    roas = rd.m('period_roas', WINDOW, channel='meta')
    account_roas = None if roas.get('unavailable') else roas['value']
    mer = rd.m('mer', WINDOW)
    net_28d = (mer.get('inputs') or {}).get('net_revenue') if not mer.get('unavailable') else None
    cols = rd.columns()
    out = format_findings(format_windows(rd), ends_on, net_28d)
    out += starved_findings(ads, ends_on, account_roas)
    if not cols & set(HOOK_TAG_COLUMNS):
        out.append(_unavailable('CREA-R03', ends_on, 'medium',
                                'Ads carry no hook or angle tag, so winners cannot be split by hook or angle.',
                                ['ad_rows.hook_type', 'ad_rows.angle'], 'creative tagging (themes taxonomy)',
                                'Tag each ad with a hook type and an angle when it is briefed.'))
    play_col = next((c for c in HOOK_PLAY_COLUMNS if c in cols), None)
    if play_col is None:
        out.append(_unavailable('CREA-R04', ends_on, 'medium',
                                'Video ads have no 3-second play count, so hook rate is unavailable.',
                                ['ad_rows.video_3s'], 'meta_ads (video_play_actions, 3 seconds)',
                                'Add 3-second video plays to the Meta ad pull.'))
    else:
        start = (ends_on - timedelta(days=WINDOW - 1)).isoformat()
        rows = [r for r in rd.source.table('ad_rows') if start <= r['date'] <= ends_on.isoformat()]
        out += hook_rate_findings(rows, ads, ends_on, play_col)
    counts, _ = launches(rd)
    out += volume_findings(counts, ends_on)
    records = brain_records(brand, 'learnings', ends_on)
    comp = [r for r in records if isinstance(r.get('value'), dict) and r['value'].get('role') == 'competitor']
    if not comp:
        out.append(_unavailable('CREA-R06', ends_on, 'low', 'No competitor Ad Library pull is on file.',
                                ['brain.learnings (Ad Library format counts)'], 'apify ad library',
                                'Run the Ad Library pull for the competitor set.'))
    else:
        _, own90 = rd.ads(GAP_OWN_DAYS)
        out += gap_findings(records, own_formats(own90), ends_on)
    out.sort(key=lambda f: (SEVERITY_ORDER[f['severity']], -((f['money_at_stake'] or {}).get('usd') or 0), f['id']))
    return out
