"""Audit for screen 12-google-ads (contracts/audit.md). `run(brand, window)` returns findings; `RULES` lists them.

Every number comes from api.py, which reads google_rows through app/metrics.py and data/tables.py. No model
call, no connector, no write. Same tables and window give the same output. Rules are owned by this screen.

GADS-R01 brand cannibalisation (MEDIA-C33)
  Fires on the brand Search campaign when its impression share is at or over 85 percent (or days sit over
  the 90 percent ceiling), its ROAS is at least 2x non-brand ROAS, and no brand holdout is in the brain's
  learnings. Stake: brand spend x (1 - proven incremental share); the share is 0 until a holdout measures it,
  so the stake is an upper bound. Source: google_rows campaign rows, app/brain/<brand>/learnings.json.
GADS-R02 budget capped (MEDIA-C40)
  Fires on a Search campaign that lost 5 percent or more of impressions to budget (impression weighted) while
  its ROAS is at or over the comparator: break-even ROAS from finance inputs, else the account's Google ROAS.
  Stake: spend x lost to budget / impression share x campaign ROAS (a paid dollar is worth period ROAS).
GADS-R03 search term waste (MEDIA-C35)
  Fires on a search term marked negative by api.term_rule over 30 days: 0 conversions and spend over 2x the
  campaign CPA, CPA over 2x the campaign CPA, or a job, login or support query. Stake: the term's spend.
GADS-R04 conversion tracking gap (MEDIA-C04)
  Fires when Google conversions in the last full month differ from store paid search orders by 10 percent or
  more. No money: a tracking gap misleads bidding but its cost is not measurable from these tables.
GADS-R05 lost to rank (MEDIA-C35)
  Fires on a non-brand Search campaign losing 30 percent or more of impressions to ad rank. No money: more
  rank buys more non-brand clicks, and whether that pays needs break-even ROAS.

Severity: critical over 5 percent of trailing net revenue; high over 1 percent or 2 or more trailing windows
agreeing; else medium. Confidence per audit.md section 2: 4 windows 0.9, 2 to 3 windows 0.7, 1 window 0.5;
minus 0.2 when an evidence row is thresholded (clipped impression share, hidden search terms). Floor 0.1.
"""
import importlib.util
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCREEN = '12-google-ads'

RULES = [
    {'rule_id': 'GADS-R01', 'name': 'brand cannibalisation', 'entity_type': 'campaign',
     'inputs': ['google_rows.campaign', 'brain.learnings'], 'capability': 'MEDIA-C33', 'owner_screen': SCREEN},
    {'rule_id': 'GADS-R02', 'name': 'budget capped', 'entity_type': 'campaign',
     'inputs': ['google_rows.campaign', 'finance_inputs'], 'capability': 'MEDIA-C40', 'owner_screen': SCREEN},
    {'rule_id': 'GADS-R03', 'name': 'search term waste', 'entity_type': 'metric',
     'inputs': ['google_rows.search_term', 'google_rows.campaign'], 'capability': 'MEDIA-C35', 'owner_screen': SCREEN},
    {'rule_id': 'GADS-R04', 'name': 'conversion tracking gap', 'entity_type': 'metric',
     'inputs': ['google_rows.campaign', 'channels_monthly'], 'capability': 'MEDIA-C04', 'owner_screen': SCREEN},
    {'rule_id': 'GADS-R05', 'name': 'lost to rank', 'entity_type': 'campaign',
     'inputs': ['google_rows.campaign'], 'capability': 'MEDIA-C35', 'owner_screen': SCREEN},
]
AUTONOMY = {'MEDIA-C33': 'human_assist', 'MEDIA-C40': 'human_assist', 'MEDIA-C35': 'human_assist', 'MEDIA-C04': 'human_assist'}
SEV_ORDER = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}


def _api():
    spec = importlib.util.spec_from_file_location('screen_api_12_google_ads_audit', HERE / 'api.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


API = _api()


def money(x):
    return f'${x:,.0f}'


def money2(x):
    return f'${x:,.2f}'


def pct(x):
    return f'{x * 100:.0f} percent'


def ev(metric, value, unit, win, g, baseline=None, baseline_kind=None, source='google_rows', flag=None):
    row = {'metric': metric, 'value': value, 'unit': unit, 'window': win['label'] if isinstance(win, dict) else win,
           'ends_on': win['end'] if isinstance(win, dict) else g.as_of.isoformat(), 'freshness_days': g.freshness_days,
           'baseline': baseline, 'baseline_kind': baseline_kind, 'source': source, 'simulated': g.simulated}
    if flag:
        row['flag'] = flag
    return row


def confidence(windows, thresholded=False, peer=False):
    c = 0.9 if windows >= 4 else 0.7 if windows >= 2 else 0.5
    c -= 0.2 if thresholded else 0
    c -= 0.2 if peer else 0
    return round(max(c, 0.1), 2)


def severity(stake, net_revenue, windows):
    if stake is not None and net_revenue:
        if stake > 0.05 * net_revenue:
            return 'critical'
        if stake > 0.01 * net_revenue:
            return 'high'
    return 'high' if windows >= 2 else 'medium'


def finding(rule_id, entity, evidence, sentence, cap, stake, conf, sev, first_seen, last_seen, brain_refs=(), money_reason=None):
    out = {'id': f'{SCREEN}.{rule_id}.{entity["id"]}', 'screen': SCREEN, 'rule_id': rule_id, 'severity': sev,
           'entity': entity, 'evidence': evidence, 'sentence': sentence,
           'capability': {'id': cap, 'autonomy': AUTONOMY[cap]}, 'money_at_stake': stake, 'confidence': conf,
           'brain_refs': list(brain_refs), 'first_seen': first_seen, 'last_seen': last_seen, 'status': 'open',
           'unavailable': None}
    if stake is None:
        out['money_reason'] = money_reason or 'no baseline'
    return out


def unavailable(rule, reason, fix):
    return {'id': f'{SCREEN}.{rule["rule_id"]}.account', 'screen': SCREEN, 'rule_id': rule['rule_id'], 'severity': 'medium',
            'entity': {'type': 'metric', 'id': 'account', 'label': rule['name']}, 'evidence': [],
            'sentence': f'The {rule["name"]} check cannot run. {reason[0].upper() + reason[1:]}.',
            'capability': {'id': rule['capability'], 'autonomy': AUTONOMY.get(rule['capability'], 'human_assist')},
            'money_at_stake': None, 'money_reason': 'inputs unavailable', 'confidence': 0.1, 'brain_refs': [],
            'first_seen': None, 'last_seen': None, 'status': 'unavailable',
            'unavailable': {'inputs': rule['inputs'], 'connector': fix, 'fix': f'Connect {fix} read-only.'}}


def run_of(fired):
    """fired: booleans oldest to newest window. How many windows agree, counting back from the newest."""
    n = 0
    for f in reversed(fired):
        if not f:
            break
        n += 1
    return n


# ---------------------------------------------------------------- rules

def windows_for(g, win):
    return [w for w in (win.shift(3), win.shift(2), win.shift(1), win) if g.covers(w)]


def net_revenue(g, win):
    res = g.metric('mer', win)
    return None if res.get('unavailable') else (res.get('inputs') or {}).get('net_revenue')


def r01_brand(g, win, rev):
    wins = windows_for(g, win)
    states = []
    for w in wins:
        split, _ = g.split(w)
        flag = API.brand_flag(g, w, split)
        nb = split['nonbrand']['roas']
        states.append((flag['flagged'] and split['brand']['roas'] is not None and nb is not None
                       and split['brand']['roas'] >= API.BRAND_ROAS_MULTIPLE * nb, split, flag))
    fired, split, flag = states[-1]
    if not fired:
        return []
    agree = run_of([s[0] for s in states])
    b, nb = split['brand'], split['nonbrand']
    w = win.dict()
    brand_is = flag['impression_share']
    stake = {'usd': b['spend'], 'formula': 'brand_spend x (1 - proven_incremental_share)',
             'inputs': {'brand_spend': b['spend'], 'proven_incremental_share': 0}, 'window': w['label'],
             'note': 'upper bound: no brand holdout on file, so no part of the spend is proven to add orders'}
    evidence = [ev('brand_spend', b['spend'], 'usd', w, g),
                ev('brand_share_of_spend', b['share_of_spend'], 'ratio', w, g),
                ev('brand_roas', b['roas'], 'x', w, g, API.BRAND_ROAS_MULTIPLE * nb['roas'], 'threshold'),
                ev('nonbrand_roas', nb['roas'], 'x', w, g),
                ev('brand_impression_share', brand_is, 'ratio', w, g, API.BRAND_IS_MIN, 'threshold',
                   flag='thresholded' if flag['clipped_days'] else None),
                ev('brand_days_over_90_percent', flag['clipped_days'], 'days', w, g),
                ev('brand_holdout_on_file', 0, 'count', w, g, source='brain.learnings')]
    share_txt = 'over 90 percent' if brand_is is None else pct(brand_is) + (' or more' if flag['clipped_days'] else '')
    sentence = (f'Brand search spent {money(b["spend"])} in {win.days} days at {b["roas"]:.1f}x ROAS; non-brand made '
                f'{nb["roas"]:.1f}x. Brand ads show on {share_txt} of searches for the name and no holdout has tested them.')
    first = wins[len(wins) - agree].e
    return [finding('GADS-R01', {'type': 'campaign', 'id': _cid(split, g, 'brand'), 'label': ', '.join(b['campaigns'])},
                    evidence, sentence, 'MEDIA-C33', stake, confidence(agree, bool(flag['clipped_days'])),
                    severity(stake['usd'], rev, agree), first, win.e, brain_refs=[f'{g.brand}.learnings.brand_holdout'])]


def _cid(split, g, t):
    names = set(split[t]['campaigns'])
    ids = sorted({r['campaign_id'] for r in g.campaign if r['campaign_name'] in names})
    return '_'.join(ids) or t


def r02_budget(g, win, rev, comparator, comp_kind):
    wins = windows_for(g, win)
    history = {}
    for w in wins:
        rows = {r['campaign']: r for r in g.campaigns(w)}
        for s in g.impression_share(w):
            c = rows.get(s['campaign'])
            ok = (s['lost_is_budget'] is not None and s['lost_is_budget'] >= API.BUDGET_LOST_MIN and c and c['roas'] is not None
                  and comparator(w) is not None and c['roas'] >= comparator(w))
            history.setdefault(s['campaign'], []).append((w, ok, s, c))
    out = []
    for name, hist in history.items():
        w_now, ok, s, c = hist[-1]
        if not ok or w_now.e != win.e:
            continue
        agree = run_of([h[1] for h in hist])
        w = win.dict()
        stake = None
        reason = None
        if s['impression_share']:
            missed_spend = c['spend'] * s['lost_is_budget'] / s['impression_share']
            stake = {'usd': round(missed_spend * c['roas'], 2),
                     'formula': 'spend x lost_is_budget / impression_share x campaign_roas',
                     'inputs': {'spend': c['spend'], 'lost_is_budget': s['lost_is_budget'],
                                'impression_share': s['impression_share'], 'campaign_roas': c['roas']},
                     'window': w['label'], 'note': 'Google reported value, before margin'}
        else:
            reason = 'impression share is over the 90 percent ceiling every day, so missed spend has no base'
        comp = comparator(win)
        evidence = [ev('lost_is_budget', s['lost_is_budget'], 'ratio', w, g, API.BUDGET_LOST_MIN, 'threshold'),
                    ev('impression_share', s['impression_share'], 'ratio', w, g,
                       flag='thresholded' if s['clipped_days'] else None),
                    ev('campaign_roas', c['roas'], 'x', w, g, comp, comp_kind),
                    ev('spend', c['spend'], 'usd', w, g)]
        sentence = (f'{name} lost {pct(s["lost_is_budget"])} of its impressions to budget in {win.days} days at '
                    f'{c["roas"]:.1f}x ROAS.')
        if stake:
            sentence += f' That is about {money(stake["usd"])} of Google reported sales not bought.'
        first = hist[len(hist) - agree][0].e
        out.append(finding('GADS-R02', {'type': 'campaign', 'id': c['campaign_id'], 'label': name}, evidence, sentence,
                           'MEDIA-C40', stake, confidence(agree, bool(s['clipped_days'])),
                           severity(stake['usd'] if stake else None, rev, agree), first, win.e, money_reason=reason))
    return out


def r03_terms(g, win, rev):
    rows, summary = g.search_terms(win.end)
    out = []
    w = summary['window']
    for t in rows:
        if t['action'] != 'negative':
            continue
        stake = {'usd': t['spend'], 'formula': 'term_spend (spend with no or poor return)', 'inputs': {'term_spend': t['spend']},
                 'window': w['label']}
        evidence = [ev('term_spend', t['spend'], 'usd', w, g, flag='thresholded'),
                    ev('term_conversions', t['conversions'], 'count', w, g),
                    ev('campaign_cpa', t['campaign_cpa'], 'usd', w, g, API.WASTE_CPA_MULTIPLE, 'threshold')]
        conv = 'no conversions' if not t['conversions'] else f'{t["conversions"]} conversions at {money(t["cpa"])} each'
        sentence = (f'"{t["term"]}" spent {money(t["spend"])} in {w["days"]} days with {conv}. '
                    f'The campaign pays {money(t["campaign_cpa"])} per conversion.' if t['campaign_cpa'] else
                    f'"{t["term"]}" spent {money(t["spend"])} in {w["days"]} days. It is {t["why"]}.')
        key = f'{t["campaign_id"]}_{t["term"].replace(" ", "-")}'
        out.append(finding('GADS-R03', {'type': 'metric', 'id': key, 'label': f'search term "{t["term"]}"'}, evidence,
                           sentence, 'MEDIA-C35', stake, confidence(1, True), severity(t['spend'], rev, 1), win.e, win.e))
    return out


def r04_tracking(g, win):
    try:
        c = API.conversion_check(g)
    except API.Unavailable as exc:
        return [unavailable(RULES[3], exc.reason, exc.fix or 'shopify')]
    gap, vgap = c['conversion_gap'], c['value_per_conversion_gap']
    count_off = gap is not None and abs(gap) >= API.TRACKING_GAP_MIN
    value_off = vgap is not None and abs(vgap) >= API.TRACKING_GAP_MIN
    if not (count_off or value_off):
        return []
    w = c['window']
    evidence = [ev('google_conversions', c['google_conversions'], 'count', w, g),
                ev('store_paid_search_orders', c['store_orders'], 'count', w, g, source='channels_monthly'),
                ev('conversion_gap', gap, 'ratio', w, g, API.TRACKING_GAP_MIN, 'threshold'),
                ev('google_value_per_conversion', c['google_value_per_conversion'], 'usd', w, g),
                ev('store_aov', c['store_aov'], 'usd', w, g, source='channels_monthly'),
                ev('value_per_conversion_gap', vgap, 'ratio', w, g, API.TRACKING_GAP_MIN, 'threshold')]
    month = date.fromisoformat(w['end']).strftime('%B')
    if count_off:
        more = 'fewer' if gap < 0 else 'more'
        sentence = (f'In {month} Google counted {c["google_conversions"]:,} conversions. The store got {c["store_orders"]:,} '
                    f'paid search orders, so Google counted {pct(abs(gap))} {more}.')
    else:
        sentence = (f'In {month} Google valued each conversion at {money2(c["google_value_per_conversion"])}. The store\'s '
                    f'paid search order was worth {money2(c["store_aov"])} net, so Google reads {pct(abs(vgap))} '
                    f'{"high" if vgap > 0 else "low"}.')
    return [finding('GADS-R04', {'type': 'metric', 'id': 'conversions_vs_orders', 'label': 'Google conversions vs store orders'},
                    evidence, sentence, 'MEDIA-C04', None, confidence(1), 'medium', w['end'], w['end'],
                    money_reason='tracking gap: its cost is not measurable from these tables')]


def r05_rank(g, win):
    wins = windows_for(g, win)
    history = {}
    for w in wins:
        for s in g.impression_share(w):
            if s['tag'] == 'nonbrand' and s['channel_type'] == 'SEARCH':
                history.setdefault(s['campaign'], []).append((w, s['lost_is_rank'] is not None and s['lost_is_rank'] >= API.RANK_LOST_MIN, s))
    out = []
    ids = {r['campaign_name']: r['campaign_id'] for r in g.campaign}
    for name, hist in history.items():
        w_now, ok, s = hist[-1]
        if not ok or w_now.e != win.e:
            continue
        agree = run_of([h[1] for h in hist])
        w = win.dict()
        evidence = [ev('lost_is_rank', s['lost_is_rank'], 'ratio', w, g, API.RANK_LOST_MIN, 'threshold'),
                    ev('impression_share', s['impression_share'], 'ratio', w, g)]
        sentence = (f'{name} lost {pct(s["lost_is_rank"])} of its impressions to ad rank in {win.days} days. '
                    f'It shows on {pct(s["impression_share"])} of the searches it could win.')
        out.append(finding('GADS-R05', {'type': 'campaign', 'id': ids.get(name, name), 'label': name}, evidence, sentence,
                           'MEDIA-C35', None, confidence(agree), 'high' if agree >= 2 else 'medium',
                           hist[len(hist) - agree][0].e, win.e,
                           money_reason='more rank buys more non-brand clicks; whether that pays needs break-even ROAS'))
    return out


# ---------------------------------------------------------------- entry point

def run(brand, window=None):
    """Findings for one brand and window {ends_on, days, trailing}; sorted by severity, then stake."""
    window = window or {}
    days = int(window.get('days') or 28)
    try:
        g = API.Google(brand)
    except API.Unavailable as exc:
        return [unavailable(r, exc.reason, exc.fix or 'google_ads') for r in RULES]
    end = date.fromisoformat(window['ends_on']) if window.get('ends_on') else g.as_of
    if end > g.as_of:
        raise ValueError(f'ends_on is after the last full day, {g.as_of.isoformat()}')
    win = API.Win(end, days)
    if not g.covers(win):
        return [unavailable(r, f'google_rows covers {g.first} to {g.last}, not all of {win.s} to {win.e}', 'google_ads')
                for r in RULES]
    rev = net_revenue(g, win)
    be = g.metric('break_even_roas', win)
    if not be.get('unavailable') and be.get('value'):
        comparator, kind = (lambda w, v=be['value']: v), 'threshold'
    else:
        comparator, kind = (lambda w: g.split(w)[0]['total']['roas']), 'threshold'
    out = r01_brand(g, win, rev) + r02_budget(g, win, rev, comparator, kind) + r03_terms(g, win, rev) + \
        r04_tracking(g, win) + r05_rank(g, win)
    out.sort(key=lambda f: (SEV_ORDER[f['severity']], -((f['money_at_stake'] or {}).get('usd') or -1), f['id']))
    return out


if __name__ == '__main__':
    import json
    import sys
    print(json.dumps(run(sys.argv[1] if len(sys.argv) > 1 else 'bombas'), indent=1))
