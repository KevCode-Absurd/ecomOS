"""Audit for screen 13-affiliate-marketplace-ads (contracts/audit.md). `run(brand, window)` returns findings; `RULES` lists them.

Every number comes from api.py, which reads the data layer through app/metrics.py and data/tables.py and the brain
through brain/store.py. No model call, no connector, no write. Same tables, brain and window give the same output.
Rules are owned by this screen.

AFFM-R01 coupon leak (MEDIA-C50)
  Fires on an affiliate code with 10 or more redemptions in the window where 30 percent or more have no click from
  that affiliate in the 30-day cookie window: the code is being used by shoppers the affiliate never sent.
  Stake: commission paid on the leaked orders (leaked sales x the affiliate's rate). Source: coupon_redemptions,
  affiliate_clicks_orders, commission_tiers. Severity high: margin paid out now for orders that were not earned.
AFFM-R02 orders with no clicks (MEDIA-C50)
  Fires on an affiliate credited with 3 or more orders and 0 clicks in the window. Stake: commission on those
  orders. Source: affiliate_clicks_orders, commission_tiers. Severity high.
AFFM-R03 fast click to order (MEDIA-C50)
  Fires on an affiliate with 3 or more orders placed under 10 seconds after the click (cookie stuffing). Stake:
  commission on those orders when the rate is on file. Severity medium.
AFFM-R04 Amazon reseller presence (MEDIA-C52)
  Fires when every in-stock Amazon listing in the brain's public sample is sold by a third-party reseller and no
  brand store shows. Source: brain marketplaces records (public, not signed in, not simulated). No money: Amazon
  sales are not connected, so what resellers take cannot be counted. Severity medium (known downstream cost, no
  formula). Confidence 0.5 for one read, minus 0.2 because the read is a sample.
AFFM-R05 network invoice vs tracked orders (MEDIA-C51)
  Fires when the network's last invoice differs from commission on tracked orders by 2 percent or more. Stake:
  the gap, when the network asks for more. Source: affiliate_invoices, affiliate_clicks_orders, commission_tiers.

A rule whose tables are missing emits one finding with status unavailable, the connector and the fix (audit.md 4).
"""
import importlib.util
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCREEN = '13-affiliate-marketplace-ads'

RULES = [
    {'rule_id': 'AFFM-R01', 'name': 'coupon leak', 'entity_type': 'offer',
     'inputs': ['coupon_redemptions', 'affiliate_clicks_orders', 'commission_tiers'], 'capability': 'MEDIA-C50',
     'owner_screen': SCREEN, 'severity': 'high'},
    {'rule_id': 'AFFM-R02', 'name': 'affiliate orders with no clicks', 'entity_type': 'brand',
     'inputs': ['affiliate_clicks_orders', 'commission_tiers'], 'capability': 'MEDIA-C50', 'owner_screen': SCREEN,
     'severity': 'high'},
    {'rule_id': 'AFFM-R03', 'name': 'fast click to order', 'entity_type': 'brand',
     'inputs': ['affiliate_clicks_orders', 'commission_tiers'], 'capability': 'MEDIA-C50', 'owner_screen': SCREEN,
     'severity': 'medium'},
    {'rule_id': 'AFFM-R04', 'name': 'Amazon reseller presence', 'entity_type': 'stage',
     'inputs': ['brain.marketplaces'], 'capability': 'MEDIA-C52', 'owner_screen': SCREEN, 'severity': 'medium'},
    {'rule_id': 'AFFM-R05', 'name': 'network invoice vs tracked orders', 'entity_type': 'metric',
     'inputs': ['affiliate_invoices', 'affiliate_clicks_orders', 'commission_tiers'], 'capability': 'MEDIA-C51',
     'owner_screen': SCREEN, 'severity': 'medium'},
]
RULE = {r['rule_id']: r for r in RULES}
AUTONOMY = {'MEDIA-C50': 'founder_gate', 'MEDIA-C51': 'founder_gate', 'MEDIA-C52': 'human_assist'}
SEV_ORDER = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}


def _api():
    spec = importlib.util.spec_from_file_location('screen_api_13_affiliate_audit', HERE / 'api.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


API = _api()


def money(x):
    return f'${x:,.0f}'


def pct(x):
    return f'{x * 100:.0f} percent'


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


def finding(rule_id, entity, evidence, sentence, stake, conf, first_seen, last_seen, brain_refs=(), money_reason=None):
    rule = RULE[rule_id]
    cap = rule['capability']
    out = {'id': f'{SCREEN}.{rule_id}.{entity["id"]}', 'screen': SCREEN, 'rule_id': rule_id, 'severity': rule['severity'],
           'entity': entity, 'evidence': evidence, 'sentence': sentence,
           'capability': {'id': cap, 'autonomy': AUTONOMY[cap]}, 'money_at_stake': stake, 'confidence': conf,
           'brain_refs': list(brain_refs), 'first_seen': first_seen, 'last_seen': last_seen, 'status': 'open',
           'unavailable': None}
    if stake is None:
        out['money_reason'] = money_reason or 'no baseline'
    return out


def unavailable(rule_id, missing, reason=None):
    rule = RULE[rule_id]
    names = [API.CONNECTORS[m][0] for m in missing] or ['brand brain']
    fix = ' '.join(API.CONNECTORS[m][1] for m in missing) or 'Add an Amazon listing sample to the brain marketplaces section.'
    sentence = reason or f'The {rule["name"]} check cannot run. It needs {", ".join(names)}. Not connected yet.'
    return {'id': f'{SCREEN}.{rule_id}.account', 'screen': SCREEN, 'rule_id': rule_id, 'severity': rule['severity'],
            'entity': {'type': 'metric', 'id': 'account', 'label': rule['name']}, 'evidence': [], 'sentence': sentence,
            'capability': {'id': rule['capability'], 'autonomy': AUTONOMY[rule['capability']]},
            'money_at_stake': None, 'confidence': 0.1, 'brain_refs': [],
            'first_seen': None, 'last_seen': None, 'status': 'unavailable',
            'unavailable': {'inputs': missing, 'connector': ', '.join(names), 'fix': fix}, 'money_reason': 'inputs unavailable'}


def missing(s, names):
    return [n for n in names if s.rows(n) is None]


def commission_stake(sales, rate, formula_label, win):
    if sales is None or rate is None:
        return None
    return {'usd': round(sales * rate, 2), 'formula': f'{formula_label} x commission_rate',
            'inputs': {formula_label: sales, 'commission_rate': rate}, 'window': win['label']}


# ---------------------------------------------------------------- rules

def r01_coupon_leak(s, win, w):
    gone = missing(s, ['coupon_redemptions', 'affiliate_clicks_orders'])
    if gone:
        return [unavailable('AFFM-R01', gone)]
    tiers = s.tier_rates()
    out = []
    for c in API.coupon_leaks(s.rows('coupon_redemptions'), s.rows('affiliate_clicks_orders'), win):
        rate = tiers.get(c['affiliate_id'], {}).get('rate')
        stake = commission_stake(c['leaked_sales'], rate, 'leaked_sales', w)
        evidence = [ev('code_redemptions', c['redemptions'], 'count', w, s.freshness_days, s.simulated, source='coupon_redemptions'),
                    ev('redemptions_without_click', c['leaked'], 'count', w, s.freshness_days, s.simulated, source='coupon_redemptions'),
                    ev('leak_share', c['leak_share'], 'ratio', w, s.freshness_days, s.simulated, API.LEAK_SHARE_MIN, 'threshold',
                       source='coupon_redemptions'),
                    ev('leaked_sales', c['leaked_sales'], 'usd', w, s.freshness_days, s.simulated, source='coupon_redemptions')]
        sentence = (f'Code {c["code"]} was used {c["redemptions"]} times in {win.days} days. {c["leaked"]} of those orders, '
                    f'{pct(c["leak_share"])}, had no click from its affiliate.')
        out.append(finding('AFFM-R01', {'type': 'offer', 'id': c['code'], 'label': f'affiliate code {c["code"]}'}, evidence,
                           sentence, stake, confidence(1), win.e, win.e,
                           money_reason='no commission rate or order value on file for the leaked orders'))
    return out


def _partner_rule(s, win, w, rule_id, pick, count_key, sentence_fn):
    gone = missing(s, ['affiliate_clicks_orders'])
    if gone:
        return [unavailable(rule_id, gone)]
    rows = API.partners(s.rows('affiliate_clicks_orders'), s.tier_rates(), win)
    out = []
    for p in pick(rows):
        n = p[count_key]
        share = n / p['orders'] if p['orders'] else None
        sales = round(p['sales'] * share, 2) if share is not None and p['sales'] is not None else None
        stake = commission_stake(sales, p['rate'], 'flagged_sales', w)
        evidence = [ev('orders', p['orders'], 'count', w, s.freshness_days, s.simulated, source='affiliate_clicks_orders'),
                    ev('clicks', p['clicks'], 'count', w, s.freshness_days, s.simulated, source='affiliate_clicks_orders'),
                    ev(count_key, n, 'count', w, s.freshness_days, s.simulated,
                       API.NO_CLICK_MIN_ORDERS if rule_id == 'AFFM-R02' else API.FAST_MIN_ORDERS, 'threshold',
                       source='affiliate_clicks_orders'),
                    ev('flagged_sales', sales, 'usd', w, s.freshness_days, s.simulated, source='affiliate_clicks_orders')]
        out.append(finding(rule_id, {'type': 'brand', 'id': f'affiliate_{p["affiliate_id"]}', 'label': p['name']}, evidence,
                           sentence_fn(p, win), stake, confidence(1), win.e, win.e,
                           money_reason='no commission rate on file for this affiliate'))
    return out


def r02_no_clicks(s, win, w):
    return _partner_rule(s, win, w, 'AFFM-R02', API.no_click_affiliates, 'orders',
                         lambda p, win: f'{p["name"]} was credited with {p["orders"]} orders in {win.days} days and sent '
                                        f'0 clicks. Sales on those orders were {money(p["sales"])}.')


def r03_fast(s, win, w):
    return _partner_rule(s, win, w, 'AFFM-R03', lambda rows: [p for p in rows if p['fast_orders'] >= API.FAST_MIN_ORDERS],
                         'fast_orders',
                         lambda p, win: f'{p["name"]} had {p["fast_orders"]} orders placed under {API.FAST_SECONDS} seconds '
                                        f'after the click in {win.days} days. A shopper cannot browse and pay that fast.')


def r04_resellers(s, win, w):
    a = API.amazon_block(s, win)
    if not a['presence_ref'] or not a['asins_read']:
        return [unavailable('AFFM-R04', [], reason='The Amazon reseller check cannot run. The brain has no Amazon listing '
                                                   'sample. Add one to the marketplaces section.')]
    if not a['in_stock'] or a['resold_in_stock'] < a['in_stock'] or a['brand_store']:
        return []
    captured = a['captured_at'] or win.e
    fresh = max((date.fromisoformat(win.e) - date.fromisoformat(captured[:10])).days, 0)
    pw = {'label': 'sample', 'end': captured[:10]}
    evidence = [ev('asins_read', a['asins_read'], 'count', pw, fresh, False, source='brain.marketplaces', flag='sampled'),
                ev('listings_in_stock', a['in_stock'], 'count', pw, fresh, False, source='brain.marketplaces', flag='sampled'),
                ev('in_stock_sold_by_resellers', a['resold_in_stock'], 'count', pw, fresh, False, a['in_stock'], 'threshold',
                   source='brain.marketplaces', flag='sampled'),
                ev('resellers_seen', len(a['resellers']), 'count', pw, fresh, False, source='brain.marketplaces'),
                ev('brand_store_seen', 0, 'count', pw, fresh, False, source='brain.marketplaces'),
                ev('lowest_reseller_price', a['lowest_reseller_price'], 'usd', pw, fresh, False, source='brain.marketplaces')]
    sentence = (f'All {a["in_stock"]} in-stock {s.brand.capitalize()} listings in a sample of {a["asins_read"]} Amazon ASINs are sold by '
                f'{len(a["resellers"])} resellers, from ${a["lowest_reseller_price"]:,.2f}. No brand store showed.')
    refs = [a['presence_ref']] + [l['brain_ref'] for l in a['listings'] if l['in_stock']]
    return [finding('AFFM-R04', {'type': 'stage', 'id': 'amazon_listings', 'label': 'Amazon listings'}, evidence, sentence,
                    None, confidence(1, sampled=True), captured[:10], win.e, brain_refs=refs,
                    money_reason='Amazon sales are not connected, so what resellers sell cannot be counted')]


def r05_invoice(s, win, w):
    gone = missing(s, ['affiliate_invoices', 'affiliate_clicks_orders', 'commission_tiers'])
    if gone:
        return [unavailable('AFFM-R05', gone)]
    parts = API.partners(s.rows('affiliate_clicks_orders'), s.tier_rates(), win)
    b = API.billing(s, parts)
    if b['unavailable'] or b['gap_share'] is None or abs(b['gap_share']) < API.INVOICE_GAP_MIN:
        return []
    stake = {'usd': b['gap'], 'formula': 'network_owed - tracked_commission',
             'inputs': {'network_owed': b['network_owed'], 'tracked_commission': b['tracked_commission']},
             'window': w['label']} if b['gap'] > 0 else None
    evidence = [ev('network_owed', b['network_owed'], 'usd', w, s.freshness_days, s.simulated, source='affiliate_invoices'),
                ev('tracked_commission', b['tracked_commission'], 'usd', w, s.freshness_days, s.simulated,
                   source='affiliate_clicks_orders'),
                ev('gap_share', b['gap_share'], 'ratio', w, s.freshness_days, s.simulated, API.INVOICE_GAP_MIN, 'threshold')]
    more = 'more' if b['gap'] > 0 else 'less'
    sentence = (f'The network invoice for {b["cycle"]} asks {money(abs(b["gap"]))} {more} than commission on tracked orders, '
                f'{pct(abs(b["gap_share"]))} off.')
    return [finding('AFFM-R05', {'type': 'metric', 'id': f'invoice_{b["cycle"]}', 'label': f'invoice {b["cycle"]}'}, evidence,
                    sentence, stake, confidence(1), win.e, win.e, money_reason='the invoice asks for less than tracked')]


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
    win = API.Win(end, days)
    w = win.dict()
    out = r01_coupon_leak(s, win, w) + r02_no_clicks(s, win, w) + r03_fast(s, win, w) + r04_resellers(s, win, w) + \
        r05_invoice(s, win, w)
    out.sort(key=lambda f: (SEV_ORDER[f['severity']], f['status'] != 'open',
                            -((f['money_at_stake'] or {}).get('usd') or -1), f['id']))
    return out


if __name__ == '__main__':
    import json
    import sys
    print(json.dumps(run(sys.argv[1] if len(sys.argv) > 1 else 'bombas'), indent=1))
