"""Audit for screen 20-marketplaces (contracts/audit.md). `run(brand, window)` returns findings; `RULES` lists them.

Every number comes from api.py, which reads the data layer through app/metrics.py and data/tables.py and the brain
through brain/store.py. No model call, no connector, no write. Same tables, brain and window give the same output.
All rules are owned by this screen. Amazon Ads and reseller presence belong to screen 13 (AFFM-R04), not here.

Room spec rules (FEATURES.md, "Insights specified"). Each reads a table the Bombas set does not have yet, so each
emits one finding with status unavailable naming the connector, until the table exists:
MKT-R01 listing failing channel spec (PROD-C63): listing_health_score under 95 percent, or any open image or
  attribute error. Input marketplace_listings. Severity high.
MKT-R02 Buy Box lost on an advertised SKU (PROD-C46): buy_box_win_rate under 80 percent while ads run. Inputs
  buybox_snapshots, amazon_ads_rows. Severity high.
MKT-R03 MAP violation (PROD-C46): a tracked reseller price over 10 percent below MAP. Inputs buybox_snapshots,
  map_policy. Severity medium.
MKT-R04 account health near suspension (PROD-C38): the channel's own warning line crossed. Input
  account_health_metrics. Severity critical.
MKT-R05 true ROAS far below reported (PROD-C49): reported over true by more than 20 percent. Input
  rapid_delivery_orders. Severity medium.
MKT-R06 settlement shortfall (ORCH-C03): expected minus paid beyond rounding on a closed cycle. Input
  settlement_reports. Severity high.
MKT-R07 dark store stockout risk (PROD-C51): fill rate under 70 percent 2 days running on a hero SKU. Input
  dark_store_inventory. Severity high.
MKT-R08 ad credit going unused (PROD-C50): under 50 percent used with under 10 days left. Input ad_credit_ledger.
  Severity medium.
MKT-R09 IPI under the storage limit line (PROD-C39). Input amazon_inventory. Severity high.
MKT-R10 sales drop is conversion, not traffic (PROD-C40): over 70 percent of a drop from conversion. Input
  amazon_traffic_sales. Severity medium.
MKT-R11 stale marketplace listing (PROD-C44): not updated in 90 days on Walmart, Target Plus, eBay or TikTok Shop.
  Input marketplace_listings. Severity low.
MKT-R12 compliance document missing (PROD-C45): Care Labeling or Prop 65 document missing or expired on a live SKU.
  Input compliance_docs. Severity high.
MKT-R13 catalogue feed stale (PROD-C47): no sync in 24 hours. Input catalogue_feed. Severity medium.

Rules on what the brand has now:
MKT-R14 Amazon ASIN rated under the brand's other ASINs (PROD-C38): an ASIN with 5 or more ratings sits 0.3 stars
  or more under the median of the brand's other rated ASINs (room spec benchmark for review_rating_avg). Source:
  brain marketplaces (public sample, not simulated). No money: Amazon sales by ASIN are not connected. Medium.
MKT-R15 marketplace trust rung with no proof (PROD-C34): a rung of the marketplace_trust ladder (fake listings,
  short packs) has complaint quotes and no public proof. Source: brain objection_ladders. No money. Medium.
MKT-R16 Amazon listings that cannot be bought (PROD-C63): ASINs in the public sample that say currently unavailable
  or show no price. Source: brain marketplaces. No money: Amazon sales by ASIN are not connected. Medium.
MKT-R17 marketplace share below own median (PROD-C40): a marketplace's share of all revenue in the last full month
  is 10 percent or more under its median share of the 4 full months before. Share, so seasonality cancels.
  Stake: (median share - share) x all revenue in the month. Source: marketplace_monthly, monthly,
  wholesale_monthly. Severity critical over 5 percent of trailing 28-day net revenue, high over 1 percent or with
  2 or more windows agreeing, else medium.

A rule whose inputs are missing emits one finding with status unavailable, the connector and the fix (audit.md 4).
"""
import importlib.util
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCREEN = '20-marketplaces'


def _rule(rid, name, entity, inputs, cap, sev):
    return {'rule_id': rid, 'name': name, 'entity_type': entity, 'inputs': inputs, 'capability': cap,
            'owner_screen': SCREEN, 'severity': sev}


RULES = [
    _rule('MKT-R01', 'listing failing channel spec', 'metric', ['marketplace_listings'], 'PROD-C63', 'high'),
    _rule('MKT-R02', 'Buy Box lost on an advertised SKU', 'sku', ['buybox_snapshots', 'amazon_ads_rows'], 'PROD-C46', 'high'),
    _rule('MKT-R03', 'MAP violation', 'sku', ['buybox_snapshots', 'map_policy'], 'PROD-C46', 'medium'),
    _rule('MKT-R04', 'account health near suspension', 'metric', ['account_health_metrics'], 'PROD-C38', 'critical'),
    _rule('MKT-R05', 'true ROAS below reported', 'metric', ['rapid_delivery_orders'], 'PROD-C49', 'medium'),
    _rule('MKT-R06', 'settlement shortfall', 'metric', ['settlement_reports'], 'ORCH-C03', 'high'),
    _rule('MKT-R07', 'dark store stockout risk', 'sku', ['dark_store_inventory'], 'PROD-C51', 'high'),
    _rule('MKT-R08', 'ad credit going unused', 'metric', ['ad_credit_ledger'], 'PROD-C50', 'medium'),
    _rule('MKT-R09', 'IPI under the storage limit line', 'metric', ['amazon_inventory'], 'PROD-C39', 'high'),
    _rule('MKT-R10', 'sales drop from conversion', 'metric', ['amazon_traffic_sales'], 'PROD-C40', 'medium'),
    _rule('MKT-R11', 'stale marketplace listing', 'sku', ['marketplace_listings'], 'PROD-C44', 'low'),
    _rule('MKT-R12', 'compliance document missing', 'sku', ['compliance_docs'], 'PROD-C45', 'high'),
    _rule('MKT-R13', 'catalogue feed stale', 'metric', ['catalogue_feed'], 'PROD-C47', 'medium'),
    _rule('MKT-R14', 'Amazon ASIN rated under the others', 'sku', ['brain.marketplaces'], 'PROD-C38', 'medium'),
    _rule('MKT-R15', 'marketplace trust rung with no proof', 'ladder_rung', ['brain.objection_ladders'], 'PROD-C34', 'medium'),
    _rule('MKT-R16', 'Amazon listings that cannot be bought', 'stage', ['brain.marketplaces'], 'PROD-C63', 'medium'),
    _rule('MKT-R17', 'marketplace share below own median', 'stage',
          ['marketplace_monthly', 'monthly', 'wholesale_monthly'], 'PROD-C40', 'high'),
]
RULE = {r['rule_id']: r for r in RULES}
TABLE_RULES = [r['rule_id'] for r in RULES[:13]]
AUTONOMY = {'PROD-C63': 'agent_does', 'PROD-C46': 'agent_does', 'PROD-C38': 'human_assist', 'PROD-C49': 'agent_does',
            'ORCH-C03': 'agent_does', 'PROD-C51': 'human_assist', 'PROD-C50': 'founder_gate', 'PROD-C39': 'agent_does',
            'PROD-C40': 'founder_gate', 'PROD-C44': 'human_assist', 'PROD-C45': 'founder_gate', 'PROD-C47': 'founder_gate',
            'PROD-C34': 'human_assist'}
SEV_ORDER = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}


def _api():
    spec = importlib.util.spec_from_file_location('screen_api_20_marketplaces_audit', HERE / 'api.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


API = _api()


def pct(x, nd=0):
    return f'{x * 100:.{nd}f} percent'


def ev(metric, value, unit, win, freshness, simulated, baseline=None, baseline_kind=None, source=None, flag=None):
    row = {'metric': metric, 'value': value, 'unit': unit, 'window': win['label'], 'ends_on': win['end'],
           'freshness_days': freshness, 'baseline': baseline, 'baseline_kind': baseline_kind, 'source': source,
           'simulated': simulated}
    if flag:
        row['flag'] = flag
    return row


def confidence(windows, sampled=False, peer=False):
    c = 0.9 if windows >= 4 else 0.7 if windows >= 2 else 0.5
    c -= 0.2 if sampled else 0
    c -= 0.2 if peer else 0
    return round(max(c, 0.1), 2)


def finding(rule_id, entity, evidence, sentence, stake, conf, first_seen, last_seen, brain_refs=(), money_reason=None,
            severity=None):
    rule = RULE[rule_id]
    cap = rule['capability']
    out = {'id': f'{SCREEN}.{rule_id}.{entity["id"]}', 'screen': SCREEN, 'rule_id': rule_id,
           'severity': severity or rule['severity'], 'entity': entity, 'evidence': evidence, 'sentence': sentence,
           'capability': {'id': cap, 'autonomy': AUTONOMY[cap]}, 'money_at_stake': stake, 'confidence': conf,
           'brain_refs': list(brain_refs), 'first_seen': first_seen, 'last_seen': last_seen, 'status': 'open',
           'unavailable': None}
    if stake is None:
        out['money_reason'] = money_reason or 'no baseline'
    return out


def unavailable(rule_id, missing, reason=None):
    rule = RULE[rule_id]
    names = [API.CONNECTORS[m][0] for m in missing if m in API.CONNECTORS] or ['brand brain']
    fix = ' '.join(API.CONNECTORS[m][1] for m in missing if m in API.CONNECTORS) or \
        'Add the missing record to the brand brain.'
    sentence = reason or f'The {rule["name"]} check cannot run. It needs {", ".join(names)}. Not connected yet.'
    return {'id': f'{SCREEN}.{rule_id}.account', 'screen': SCREEN, 'rule_id': rule_id, 'severity': rule['severity'],
            'entity': {'type': 'metric', 'id': 'account', 'label': rule['name']}, 'evidence': [], 'sentence': sentence,
            'capability': {'id': rule['capability'], 'autonomy': AUTONOMY[rule['capability']]},
            'money_at_stake': None, 'money_reason': 'inputs unavailable', 'confidence': 0.1, 'brain_refs': [],
            'first_seen': None, 'last_seen': None, 'status': 'unavailable',
            'unavailable': {'inputs': missing, 'connector': ', '.join(names), 'fix': fix}}


def sample_window(listings, win):
    """Evidence window for a brain read: the capture date, capped at the window end."""
    cap = max((l['captured_at'] for l in listings if l.get('captured_at')), default=None) or win.e
    day = min(cap[:10], win.e)
    fresh = max((date.fromisoformat(win.e) - date.fromisoformat(day)).days, 0)
    return {'label': 'sample', 'end': day}, fresh


def short(title, n=40):
    t = (title or '').replace('Bombas ', '').split(' (')[0].split(',')[0].strip()
    return t if len(t) <= n else t[:n].rsplit(' ', 1)[0]


# ---------------------------------------------------------------- rules

def table_rule(s, rule_id):
    """Room spec rules. Their tables are not in the data set yet, so each reads unavailable until connected."""
    gone = [n for n in RULE[rule_id]['inputs'] if s.rows(n) is None]
    if gone:
        return [unavailable(rule_id, gone)]
    return []  # round 1: the rule body lands with its table


def r14_ratings(s, win, listings):
    rated = [l for l in listings if l['stars'] is not None and (l['ratings'] or 0) >= API.MIN_RATINGS]
    if len(rated) <= API.TRAILING:
        return [unavailable('MKT-R14', [], reason=f'The Amazon rating check cannot run. The brain has fewer than '
                                                  f'{API.TRAILING + 1} ASINs with {API.MIN_RATINGS} or more ratings.')]
    pw, fresh = sample_window(listings, win)
    out = []
    for l in API.rating_outliers(listings):
        evidence = [ev('stars', l['stars'], 'stars', pw, fresh, False, l['baseline'], 'own_median', 'brain.marketplaces',
                       flag='sampled'),
                    ev('ratings', l['ratings'], 'count', pw, fresh, False, API.MIN_RATINGS, 'threshold', 'brain.marketplaces'),
                    ev('gap_to_median', l['gap'], 'stars', pw, fresh, False, API.RATING_GAP, 'threshold', 'brain.marketplaces'),
                    ev('other_asins', l['peers'], 'count', pw, fresh, False, source='brain.marketplaces')]
        sentence = (f'Amazon ASIN {l["asin"]} ({short(l["title"])}) rates {l["stars"]:.1f} stars on {l["ratings"]} ratings. '
                    f'The brand\'s other {l["peers"]} rated ASINs have a median of {l["baseline"]:.1f}.')
        out.append(finding('MKT-R14', {'type': 'sku', 'id': f'amazon_{l["asin"]}', 'label': f'Amazon {l["asin"]}'},
                           evidence, sentence, None, confidence(1, sampled=True), pw['end'], win.e,
                           brain_refs=l['brain_refs'],
                           money_reason='Amazon sales by ASIN are not connected, so lost orders cannot be counted'))
    return out


def r15_trust(s, win):
    ladder = s.ladder()
    if ladder is None:
        return [unavailable('MKT-R15', [], reason='The marketplace trust check cannot run. The brain has no '
                                                  'marketplace_trust ladder yet.')]
    v = ladder.get('value') or {}
    day = min(((ladder.get('source') or {}).get('captured_at') or win.e)[:10], win.e)
    pw = {'label': 'ladder', 'end': day}
    fresh = (date.fromisoformat(win.e) - date.fromisoformat(day)).days
    out = []
    for rung in v.get('rungs') or []:
        proof = str(rung.get('proof') or '').strip().lower()
        counts = rung.get('counts') or {}
        n = counts.get('one_star') or 0
        if n == 0 or (proof and not proof.startswith('no public proof')):
            continue
        amazon = (counts.get('sources') or {}).get('amazon')
        evidence = [ev('one_star_quotes', n, 'count', pw, fresh, False, source='brain.objection_ladders', flag='sampled'),
                    ev('five_star_quotes', counts.get('five_star') or 0, 'count', pw, fresh, False, source='brain.objection_ladders'),
                    ev('amazon_quotes', amazon, 'count', pw, fresh, False, source='brain.objection_ladders'),
                    ev('public_proof', 0, 'count', pw, fresh, False, 1, 'threshold', 'brain.objection_ladders')]
        where = 'Amazon ' if amazon == n else ''
        sentence = (f'{n} one-star {where}quotes doubt the listing is the real product and pack. '
                    f'Nothing public answers it yet.' if 'real product' in (rung.get('doubt') or '') else
                    f'{n} one-star {where}quotes ask "{rung.get("doubt")}". Nothing public answers it yet.')
        refs = [ladder['id']] + [x for x in [rung.get('open_question')] if x] + \
            [x for x in rung.get('derived_from') or [] if '.objections.' in x or '.marketplaces.' in x]
        level = rung.get('level')
        out.append(finding('MKT-R15', {'type': 'ladder_rung', 'id': f'marketplace_trust.rung_{level}',
                                       'label': f'marketplace trust, rung {level}'}, evidence, sentence, None,
                           confidence(1, sampled=True), day, win.e, brain_refs=refs,
                           money_reason='proof gap: lost marketplace orders are not measurable without Amazon sales by ASIN'))
    return out


def r16_not_buyable(s, win, listings):
    if not listings:
        return [unavailable('MKT-R16', [], reason='The Amazon buyability check cannot run. The brain has no Amazon '
                                                  'listing sample. Add one to the marketplaces section.')]
    bad = [l for l in listings if l['buyable'] is False]
    if not bad:
        return []
    pw, fresh = sample_window(listings, win)
    gone = sum(1 for l in bad if l['problem'] == 'currently unavailable')
    no_price = len(bad) - gone
    evidence = [ev('asins_read', len(listings), 'count', pw, fresh, False, source='brain.marketplaces', flag='sampled'),
                ev('asins_not_buyable', len(bad), 'count', pw, fresh, False, 0, 'threshold', 'brain.marketplaces'),
                ev('currently_unavailable', gone, 'count', pw, fresh, False, source='brain.marketplaces'),
                ev('no_price_shown', no_price, 'count', pw, fresh, False, source='brain.marketplaces')]
    sentence = (f'{len(bad)} of {len(listings)} Amazon ASINs in the public sample cannot be bought. '
                f'{gone} say currently unavailable and {no_price} show no price.')
    refs = sorted({r for l in bad for r in l['brain_refs']})
    return [finding('MKT-R16', {'type': 'stage', 'id': 'amazon_buyable', 'label': 'Amazon listings that can be bought'},
                    evidence, sentence, None, confidence(1, sampled=True), pw['end'], win.e, brain_refs=refs,
                    money_reason='Amazon sales by ASIN are not connected, so lost orders cannot be counted')]


def trailing_net_revenue(s, end, days=28):
    daily = s.agg('daily') or []
    start = (end - timedelta(days=days - 1)).isoformat()
    rows = [r for r in daily if start <= r['date'] <= end.isoformat()]
    if len(rows) < days or any(r.get('net_sales') is None for r in rows):
        return None
    return sum(r['net_sales'] for r in rows)


def r17_share(s, win):
    rows = s.agg('marketplace_monthly')
    rev = API.revenue_months(s)
    if rows is None or not rev:
        gone = [n for n in ('marketplace_monthly', 'monthly', 'wholesale_monthly') if s.agg(n) is None]
        return [unavailable('MKT-R17', [], reason=f'The marketplace share check cannot run. It needs '
                                                  f'{", ".join(gone) or "monthly sales"}.')]
    month = API.last_full_month(win.end)
    totals = API.month_totals(rev)
    base = trailing_net_revenue(s, win.end)
    w = {'label': month, 'end': f'{month}-{API.month_days(month):02d}'}
    out = []
    for d in API.share_drops(rows, totals, month, s.first_day()):
        stake = {'usd': d['stake'], 'formula': '(median_share_4m - share) x revenue_month',
                 'inputs': {'median_share_4m': d['median_share'], 'share': d['share'], 'revenue_month': d['revenue']},
                 'window': month}
        big = base and d['stake'] / base
        sev = 'critical' if big and big > 0.05 else 'high' if (big and big > 0.01) or d['windows_below'] >= 2 else 'medium'
        evidence = [ev('marketplace_share', d['share'], 'ratio', w, s.freshness_days, s.simulated, d['median_share'],
                       'own_median', 'marketplace_monthly'),
                    ev('marketplace_net_sales', d['net_sales'], 'usd', w, s.freshness_days, s.simulated,
                       source='marketplace_monthly'),
                    ev('revenue_month', d['revenue'], 'usd', w, s.freshness_days, s.simulated,
                       source='monthly, wholesale_monthly, marketplace_monthly'),
                    ev('windows_below', d['windows_below'], 'count', w, s.freshness_days, s.simulated, API.TRAILING, 'threshold')]
        sentence = (f'{d["label"]} was {pct(d["share"], 1)} of revenue in {month}. '
                    f'Its median over the 4 months before was {pct(d["median_share"], 1)}.')
        out.append(finding('MKT-R17', {'type': 'stage', 'id': f'share_{d["marketplace"]}', 'label': f'{d["label"]} share'},
                           evidence, sentence, stake, confidence(d['windows_below']), w['end'], win.e, severity=sev))
    return out


# ---------------------------------------------------------------- entry point

def run(brand, window=None):
    """Findings for one brand and window {ends_on, days, trailing}; sorted by severity, then stake."""
    window = window or {}
    days = int(window.get('days') or 28)
    try:
        s = API.Screen(brand)
    except API.Unavailable as exc:
        return [unavailable(r['rule_id'], [], reason=f'The {r["name"]} check cannot run. {exc.reason[0].upper() + exc.reason[1:]}.')
                for r in RULES]
    end = date.fromisoformat(window['ends_on']) if window.get('ends_on') else s.as_of
    if end > s.as_of:
        raise ValueError(f'ends_on is after the last full day, {s.as_of.isoformat()}')
    win = Win(end, days)
    listings = s.listings()
    out = []
    for rid in TABLE_RULES:
        out += table_rule(s, rid)
    out += r14_ratings(s, win, listings) + r15_trust(s, win) + r16_not_buyable(s, win, listings) + r17_share(s, win)
    out.sort(key=lambda f: (SEV_ORDER[f['severity']], f['status'] != 'open',
                            -((f['money_at_stake'] or {}).get('usd') or -1), f['id']))
    return out


class Win:
    def __init__(self, end, days):
        self.end, self.days = end, days
        self.e = end.isoformat()


if __name__ == '__main__':
    import json
    import sys
    print(json.dumps(run(sys.argv[1] if len(sys.argv) > 1 else 'bombas'), indent=1))
