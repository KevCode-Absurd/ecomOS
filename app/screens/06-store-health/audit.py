"""Store health audit (screen 06, round 0). Findings in the shape of app/contracts/audit.md.

Every number comes from app/metrics.py; brand facts come from the brain (app/brain/store.py: stack, policies,
site_map). No connector, no model call. Same tables, brain and window give the same findings.

The setup checklist (`checklist()`) is the room spec's launch and hygiene list. Each item is pass, fail or
unavailable, with the source it read. api.py shows it; the rules below turn its fails into findings.

Rules
  STORE-R01  Chargeback rate over the line. Fires when the 30-day chargeback_rate is over the 0.9 percent card
             network benchmark (metrics.CHARGEBACK_BENCHMARK), or more than 20 percent over the brand's own rate
             for the 90 days before (room spec). Money: excess chargebacks (rate now minus the lower of benchmark
             and own rate, times paid orders) times the average disputed amount, scaled to the order totals.
             Capability SITE-C67 (founder gate). Owner: 06-store-health.
  STORE-R02  Setup checklist item failed. One finding per failed item that no other rule owns. Today the only
             item with a money formula is `disputes_answered`: chargebacks and inquiries still waiting for a
             response DISPUTE_DAYS days or more after they opened. A dispute with no response by its due date is
             lost by default; the table carries no due date, so DISPUTE_DAYS is the rule constant. Money: their
             disputed amount, scaled to the order totals.
             Capability per item (disputes: MONEY-C52a, human assist). Owner: 06-store-health.
  STORE-R04  Uptime and checkout monitor. Needs `uptime_checks` and `checkout_synthetic_tests` (room spec, SITE-C65).
             No synthetic monitor is connected, so it emits one `unavailable` finding at the severity it would have
             when it fires (a checkout that fails 2 checks in a row loses every order: critical).
             Capability SITE-C65 (agent does). Owner: 06-store-health.

Scale: data.sqlite may hold a sample of the order history (the dev build runs at scale 0.1) while the daily
aggregate holds all of it. Rates are counted inside data.sqlite. Dollar amounts read from data.sqlite are scaled
by paid orders in the aggregate over paid orders in data.sqlite for the same window (1.0 for a live store).
"""
import importlib.util
import sys
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parents[1]
SCREEN = '06-store-health'
WINDOW = 28
CB_WINDOW = 30           # room spec: chargeback rate for the last 30 days
CB_BASELINE = 90         # against the brand's trailing 90 days
CB_OVER = 0.20           # more than 20 percent over its own baseline
DISPUTE_DAYS = 21        # a dispute still waiting this long after it opened is most likely past its evidence deadline
POLICY_MAX_AGE = 365     # a privacy policy older than a year is stale for CCPA and CPRA annual updates
CONCENTRATION = 0.35     # one return reason over 35 percent of returns is a concentration

RULES = [
    {'rule_id': 'STORE-R01', 'name': 'Chargeback rate over the benchmark or own baseline', 'entity_type': 'metric',
     'inputs': ['orders', 'reversed_orders'], 'capability': 'SITE-C67', 'owner_screen': SCREEN},
    {'rule_id': 'STORE-R02', 'name': 'Setup checklist item failed', 'entity_type': 'metric',
     'inputs': ['reversed_orders', 'brain.stack', 'brain.policies', 'brain.site_map'], 'capability': 'MONEY-C52a',
     'owner_screen': SCREEN},
    {'rule_id': 'STORE-R04', 'name': 'Uptime and checkout monitor', 'entity_type': 'stage',
     'inputs': ['uptime_checks', 'checkout_synthetic_tests'], 'capability': 'SITE-C65', 'owner_screen': SCREEN},
]
AUTONOMY = {'SITE-C02': 'founder_gate', 'SITE-C09': 'founder_gate', 'SITE-C13': 'human_assist',
            'SITE-C14': 'founder_gate', 'SITE-C15': 'founder_gate', 'SITE-C18': 'human_assist',
            'SITE-C59': 'human_assist', 'SITE-C65': 'agent_does', 'SITE-C67': 'founder_gate',
            'SITE-C70': 'founder_gate', 'SITE-C78': 'founder_gate', 'ORG-C23': 'human_assist',
            'MONEY-C52a': 'human_assist', 'LIFE-C26': 'founder_gate'}
SEVERITY_ORDER = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}

_MODS = {}


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def metrics():
    if 'metrics' not in _MODS:
        _MODS['metrics'] = _load('ecomos_metrics_store_health', APP / 'metrics.py')
    return _MODS['metrics']


def brand_data(brand):
    if 'tables' not in _MODS:
        _MODS['tables'] = _load('ecomos_tables_store_health', APP / 'data' / 'tables.py')
    return _MODS['tables'].brand_data(brand)


def brain(brand):
    """The brand's brain records, or None when the brand has no brain folder."""
    if not brand or not (APP / 'brain' / brand).is_dir():
        return None
    if 'store' not in _MODS:
        path = str(APP / 'brain')
        if path not in sys.path:
            sys.path.insert(0, path)  # store.py imports validate.py by name
        _MODS['store'] = _load('ecomos_brain_store_store_health', APP / 'brain' / 'store.py')
    return _MODS['store'].Brain(brand)


class Reader:
    """One brand, one window end. m(name, days, end, **kw) is metrics.compute with the brand filled in."""

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

    def table(self, name):
        try:
            return self.source.table(name)
        except (KeyError, ValueError):
            return None

    def record(self, rid):
        return self._brain.get(rid) if self._brain else None

    def records(self, section):
        return self._brain.records(section) if self._brain else []

    def scale(self, days=WINDOW):
        """Paid orders in the aggregate over paid orders counted in data.sqlite, same window. 1.0 when they agree."""
        mix = self.m('payment_method_mix', days)
        aov = self.m('aov', days)
        if mix.get('unavailable') or aov.get('unavailable') or not mix['inputs']['orders']:
            return None
        return round(aov['inputs']['orders'] / mix['inputs']['orders'], 4)

    def net_revenue(self, days=WINDOW):
        aov = self.m('aov', days)
        return None if aov.get('unavailable') else aov['inputs']['net_revenue']


def last_full_day(data, brand):
    source = brand_data(brand) if brand else data
    return date.fromisoformat(source.brand['as_of'])


def _ev(metric, value, unit, ends_on, baseline=None, baseline_kind=None, window='28d', source='orders'):
    return {'metric': metric, 'value': value, 'unit': unit, 'window': window, 'ends_on': ends_on.isoformat(),
            'freshness_days': 1, 'baseline': baseline, 'baseline_kind': baseline_kind, 'source': source,
            'simulated': True}


def _severity(stake, net_28d, windows_agree):
    if stake is not None and net_28d and stake > 0.05 * net_28d:
        return 'critical'
    if windows_agree >= 2 or (stake is not None and net_28d and stake > 0.01 * net_28d):
        return 'high'
    return 'medium'


def _finding(rule_id, entity, severity, evidence, sentence, capability, money, confidence, brain_refs, ends_on,
             status='open', unavailable=None, money_reason=None):
    f = {'id': f'{SCREEN}.{rule_id}.{entity["id"]}', 'screen': SCREEN, 'rule_id': rule_id, 'severity': severity,
         'entity': entity, 'evidence': evidence, 'sentence': sentence,
         'capability': {'id': capability, 'autonomy': AUTONOMY[capability]},
         'money_at_stake': money, 'confidence': confidence, 'brain_refs': brain_refs,
         'first_seen': ends_on.isoformat(), 'last_seen': ends_on.isoformat(), 'status': status,
         'unavailable': unavailable}
    if money is None:
        f['money_reason'] = money_reason or 'no baseline'
    return f


# ---------------------------------------------------------------- inputs shared with api.py

def chargeback_now(rd):
    """30-day chargeback rate, the 90 days before it as the own baseline, and the benchmark."""
    now = rd.m('chargeback_rate', CB_WINDOW)
    base = rd.m('chargeback_rate', CB_BASELINE, end=rd.ends_on - timedelta(days=CB_WINDOW))
    bench = metrics().CHARGEBACK_BENCHMARK
    if now.get('unavailable'):
        return {'unavailable': True, 'reason': now['reason'], 'fix': now.get('fix'), 'benchmark': bench}
    own = None if base.get('unavailable') else base['value']
    over_bench = now['value'] > bench
    over_own = own is not None and now['value'] > own * (1 + CB_OVER)
    count = now['inputs']['numerator']
    return {'unavailable': False, 'rate': now['value'], 'chargebacks': count, 'paid_orders': now['inputs']['denominator'],
            'amount': now.get('amount'), 'avg_amount': round(now['amount'] / count, 2) if count and now.get('amount') else None,
            'by_reason': now.get('by_reason') or [], 'own': own, 'benchmark': bench, 'over_benchmark': over_bench,
            'over_own': over_own, 'fires': over_bench or over_own,
            'window': now['window'], 'baseline_window': None if base.get('unavailable') else base['window']}


def disputes(rd):
    return rd.m('open_disputes', WINDOW, older_than=DISPUTE_DAYS)


def _rec(rd, rid):
    return rd.record(f'{rd.brand}.{rid}') if rd.brand else None


def _src(rec, table=None):
    if rec:
        s = rec.get('source') or {}
        return {'kind': 'brain', 'ref': rec['id'], 'type': s.get('type'), 'url': s.get('ref'), 'seen': rec.get('date')}
    return {'kind': 'table', 'ref': table}


def _item(key, group, label, status, detail, source, capability, connector=None):
    return {'key': key, 'group': group, 'label': label, 'status': status, 'detail': detail, 'source': source,
            'capability': capability, 'autonomy': AUTONOMY.get(capability), 'connector': connector}


def _missing(key, group, label, table, connector, capability, detail):
    return _item(key, group, label, 'unavailable', detail, {'kind': 'table', 'ref': table}, capability, connector)


def checklist(rd):
    """The room spec's setup list. Each item reads one source and says pass, fail or unavailable."""
    out = []
    plat = _rec(rd, 'stack.platform')
    out.append(_item('platform', 'Foundation', 'Store platform on file', 'pass' if plat else 'unavailable',
                     plat['value'] if plat else 'no stack record in the brain', _src(plat), 'SITE-C02'))
    out.append(_missing('staff_2fa', 'Foundation', 'Staff accounts use 2-step login', 'staff_accounts',
                        'Shopify admin (staff and permissions, read-only)', 'SITE-C02',
                        'The staff list is not connected, so 2-step login cannot be checked.'))

    mix = rd.m('payment_method_mix', CB_WINDOW)
    if mix.get('unavailable'):
        out.append(_item('payment_methods', 'Payments', 'Card and at least 1 wallet take orders', 'unavailable',
                         mix['reason'], {'kind': 'table', 'ref': 'orders'}, 'SITE-C09', mix.get('fix')))
    else:
        c = mix['counts']
        ok = c.get('card', 0) > 0 and c.get('wallet', 0) > 0
        out.append(_item('payment_methods', 'Payments', 'Card and at least 1 wallet take orders', 'pass' if ok else 'fail',
                         f'{c.get("card", 0):,} card and {c.get("wallet", 0):,} wallet orders in 30 days.',
                         {'kind': 'table', 'ref': 'orders'}, 'SITE-C09'))
    out.append(_missing('payment_go_live', 'Payments', 'Every payment method passed a live test order',
                        'checkout_synthetic_tests', 'synthetic checkout monitor', 'SITE-C09',
                        'No go-live test log. Orders show methods that were used, not that each one works today.'))
    d = disputes(rd)
    if d.get('unavailable'):
        out.append(_item('disputes_answered', 'Payments', f'No dispute waiting {DISPUTE_DAYS} days or more for a response',
                         'unavailable', d['reason'], {'kind': 'table', 'ref': 'reversed_orders'}, 'MONEY-C52a', d.get('fix')))
    else:
        out.append(_item('disputes_answered', 'Payments', f'No dispute waiting {DISPUTE_DAYS} days or more for a response',
                         'fail' if d['aged_count'] else 'pass',
                         f'{d["aged_count"]:,} of {d["value"]:,} open disputes opened on or before '
                         f'{d["inputs"]["opened_on_or_before"]} and still have no response.',
                         {'kind': 'table', 'ref': 'reversed_orders'}, 'MONEY-C52a'))
    cb = chargeback_now(rd)
    if cb['unavailable']:
        out.append(_item('chargeback_rate', 'Payments', 'Chargebacks under 0.9 percent of paid orders', 'unavailable',
                         cb['reason'], {'kind': 'table', 'ref': 'reversed_orders'}, 'SITE-C67', cb.get('fix')))
    else:
        out.append(_item('chargeback_rate', 'Payments', 'Chargebacks under 0.9 percent of paid orders',
                         'fail' if cb['over_benchmark'] else 'pass',
                         f'{cb["rate"] * 100:.2f} percent in 30 days ({cb["chargebacks"]:,} of {cb["paid_orders"]:,}).',
                         {'kind': 'table', 'ref': 'reversed_orders'}, 'SITE-C67'))
    out.append(_missing('address_validation', 'Payments', 'Addresses checked against USPS at checkout',
                        'checkout_orders.address_validated', 'Shopify checkout settings or an address app', 'SITE-C67',
                        'Orders do not record whether the address was validated.'))

    ret = _rec(rd, 'policies.returns_window_days')
    out.append(_item('returns_policy', 'Policies', 'Return policy published', 'pass' if ret else 'unavailable',
                     ret['text'] if ret else 'no return policy record in the brain', _src(ret), 'SITE-C18'))
    ship = _rec(rd, 'policies.shipping_options')
    out.append(_item('shipping_options', 'Policies', 'Shipping options and prices published',
                     'pass' if ship else 'unavailable', ship['text'] if ship else 'no shipping record in the brain',
                     _src(ship), 'SITE-C18'))
    priv = _rec(rd, 'policies.privacy_effective_date')
    if priv and priv.get('value'):
        age = (rd.ends_on - date.fromisoformat(str(priv['value'])[:10])).days
        out.append(_item('privacy_current', 'Policies', f'Privacy policy updated in the last {POLICY_MAX_AGE} days',
                         'pass' if age <= POLICY_MAX_AGE else 'fail', f'Effective {priv["value"]}, {age} days ago.',
                         _src(priv), 'SITE-C78'))
    else:
        out.append(_item('privacy_current', 'Policies', f'Privacy policy updated in the last {POLICY_MAX_AGE} days',
                         'unavailable', 'no privacy policy date in the brain', _src(None, 'brain.policies'), 'SITE-C78'))
    cmp_ = _rec(rd, 'stack.cookie_consent')
    out.append(_item('consent_banner', 'Privacy', 'Consent manager installed', 'pass' if cmp_ else 'unavailable',
                     (cmp_['value'] + ' is on the storefront.') if cmp_ else 'no consent tool in the stack records',
                     _src(cmp_), 'SITE-C78'))
    out.append(_missing('consent_gate', 'Privacy', 'Tracking scripts wait for consent', 'consent_test_log',
                        'consent test run (a browser pass per region)', 'SITE-C78',
                        'A banner is not a gate. No test has checked that tags hold until consent.'))

    out.append(_missing('uptime', 'Monitoring', 'Store uptime watched every few minutes', 'uptime_checks',
                        'synthetic monitor (uptime checks)', 'SITE-C65', 'No uptime monitor is connected.'))
    out.append(_missing('checkout_test', 'Monitoring', 'A test order runs through checkout daily',
                        'checkout_synthetic_tests', 'synthetic monitor (transaction checks)', 'SITE-C65',
                        'No synthetic checkout test is connected.'))

    crawl = _rec(rd, 'site_map.crawl_access')
    if crawl:
        v = str(crawl.get('value') or '').lower()
        ok = 'products' in v and 'crawlable' in v and 'checkout' in v and 'disallowed' in v
        out.append(_item('crawl_access', 'Search', 'Products open to search engines, checkout closed',
                         'pass' if ok else 'fail', crawl['value'], _src(crawl), 'ORG-C23'))
    else:
        out.append(_item('crawl_access', 'Search', 'Products open to search engines, checkout closed', 'unavailable',
                         'no robots record in the brain', _src(None, 'brain.site_map'), 'ORG-C23'))
    smap = _rec(rd, 'site_map.sitemap_index')
    has_pdp = smap and any((s or {}).get('type') == 'PDP' for s in (smap.get('value') or []))
    out.append(_item('sitemap', 'Search', 'Sitemap lists product pages', 'pass' if has_pdp else 'unavailable',
                     smap['text'] if smap else 'no sitemap record in the brain', _src(smap), 'ORG-C23'))
    out.append(_missing('structured_data', 'Search', 'Product pages carry valid structured data', 'structured_data_audit',
                        'schema crawl (validator run over the sitemap)', 'ORG-C23', 'No schema crawl has run.'))
    legal = _rec(rd, 'site_map.legal_pages')
    a11y = legal and any('accessib' in str((p or {}).get('url', '')) for p in (legal.get('value') or []))
    out.append(_item('a11y_statement', 'Accessibility', 'Accessibility page published',
                     'pass' if a11y else ('fail' if legal else 'unavailable'),
                     'An accessibility page is in the pages sitemap.' if a11y else
                     ('The legal pages list has no accessibility page.' if legal else 'no legal pages record in the brain'),
                     _src(legal, 'brain.site_map'), 'SITE-C59'))
    out.append(_missing('a11y_scan', 'Accessibility', 'Key templates pass an accessibility scan', 'accessibility_scan',
                        'accessibility scan (automated plus a keyboard pass)', 'SITE-C59', 'No scan has run.'))
    out.append(_missing('app_costs', 'Apps', 'Every app has a cost and an owner', 'app_inventory',
                        'app inventory (manual entry until the Shopify apps list is connected)', 'SITE-C13',
                        'Stack records name the tools but carry no monthly cost or owner.'))
    out.append(_missing('staging', 'Apps', 'Staging matches the live theme', 'staging_sync_log', 'theme sync log',
                        'SITE-C70', 'No staging sync is logged.'))
    return out


# ---------------------------------------------------------------- rules

def rule_chargeback(rd):
    end = rd.ends_on
    cb = chargeback_now(rd)
    if cb['unavailable'] or not cb['fires']:
        return []
    line = min(cb['benchmark'], cb['own']) if cb['own'] is not None else cb['benchmark']
    evidence = [_ev('chargeback_rate', cb['rate'], 'ratio', end, baseline=cb['benchmark'], baseline_kind='threshold',
                    window='30d', source='reversed_orders')]
    if cb['own'] is not None:
        evidence.append(_ev('chargeback_rate', cb['rate'], 'ratio', end, baseline=cb['own'], baseline_kind='own_median',
                            window='30d', source='reversed_orders'))
    scale = rd.scale(CB_WINDOW)
    money, reason = None, None
    if cb['avg_amount'] is None or scale is None:
        reason = 'average disputed amount or order totals unavailable'
    else:
        excess = (cb['rate'] - line) * cb['paid_orders']
        money = {'usd': round(max(0.0, excess * cb['avg_amount'] * scale), 2),
                 'formula': '(rate_now - line) x paid_orders x avg_disputed_amount x scale',
                 'inputs': {'rate_now': cb['rate'], 'line': line, 'paid_orders': cb['paid_orders'],
                            'avg_disputed_amount': cb['avg_amount'], 'scale': scale}, 'window': '30d'}
    agree = int(cb['over_benchmark']) + int(cb['over_own'])
    sev = _severity(money['usd'] if money else None, rd.net_revenue(CB_WINDOW), agree)
    s = f'Chargebacks are {cb["rate"] * 100:.2f} percent of paid orders in the last 30 days.'
    s += (f' The card network line is {cb["benchmark"] * 100:.1f} percent' +
          (f' and your usual is {cb["own"] * 100:.2f} percent.' if cb['own'] is not None else '.'))
    return [_finding('STORE-R01', {'type': 'metric', 'id': 'chargeback_rate', 'label': 'Chargeback rate'}, sev, evidence,
                     s, 'SITE-C67', money, 0.7 if agree >= 2 else 0.5, [], end, money_reason=reason)]


def rule_checklist(rd, items=None):
    end = rd.ends_on
    out = []
    for it in items if items is not None else checklist(rd):
        if it['status'] != 'fail' or it['key'] == 'chargeback_rate':  # STORE-R01 owns the chargeback line
            continue
        entity = {'type': 'metric', 'id': it['key'], 'label': it['label']}
        refs = [it['source']['ref']] if it['source'].get('kind') == 'brain' else []
        if it['key'] == 'disputes_answered':
            d = disputes(rd)
            scale = rd.scale()
            evidence = [_ev('open_disputes_aged', d['aged_count'], 'count', end, baseline=0, baseline_kind='threshold',
                            window='as of', source='reversed_orders'),
                        _ev('open_disputes_aged_amount', d['aged_amount'], 'usd', end, window='as of',
                            source='reversed_orders')]
            money = None if scale is None else {
                'usd': round(d['aged_amount'] * scale, 2), 'formula': 'aged_disputed_amount x scale',
                'inputs': {'aged_disputed_amount': d['aged_amount'], 'aged_disputes': d['aged_count'], 'scale': scale},
                'window': f'open {DISPUTE_DAYS}+ days',
                'note': 'scale is paid orders in the daily totals over paid orders in data.sqlite, 28 days'}
            stake = money['usd'] if money else None
            s = (f'{d["aged_count"]:,} chargebacks and inquiries opened {DISPUTE_DAYS} or more days ago still have no '
                 f'response. A dispute with no response by its due date is lost.')
            sev = _severity(stake, rd.net_revenue(), 0)
            out.append(_finding('STORE-R02', entity, sev, evidence, s, it['capability'], money, 0.7, refs, end,
                                money_reason='order totals unavailable'))
        else:
            evidence = [_ev(it['key'], 0, 'pass', end, baseline=1, baseline_kind='threshold', window='as of',
                            source=it['source']['ref'])]
            out.append(_finding('STORE-R02', entity, 'low', evidence, f'{it["label"]}: no. {it["detail"]}',
                                it['capability'], None, 0.5, refs, end, money_reason='no money formula for this item yet'))
    return out


def rule_monitor(rd):
    end = rd.ends_on
    if rd.table('uptime_checks') and rd.table('checkout_synthetic_tests'):
        return []  # a connected monitor is read by the round that builds the incident timeline
    return [_finding('STORE-R04', {'type': 'stage', 'id': 'checkout', 'label': 'Store and checkout uptime'}, 'critical',
                     [], 'Nobody is watching whether the store loads or a test order goes through. An outage would '
                     'show only in the next day\'s sales.', 'SITE-C65', None, 0.5, [], end, status='unavailable',
                     unavailable={'inputs': ['uptime_checks', 'checkout_synthetic_tests'],
                                  'connector': 'synthetic monitor (uptime and transaction checks)',
                                  'fix': 'Connect a synthetic monitor that loads the home page every 5 minutes and '
                                         'places a test order daily for each payment method.'},
                     money_reason='no monitor, so no outage minutes to price')]


def run(brand, window=None, data=None):
    """Findings for one brand, sorted by severity then money at stake. `window` is {ends_on} or None."""
    ends_on = date.fromisoformat(window['ends_on']) if window and window.get('ends_on') else last_full_day(data, brand)
    return findings(Reader(data, brand, ends_on))


def findings(rd, items=None):
    """run() on a Reader the caller already holds, so api.py reuses its metric calls."""
    out = rule_chargeback(rd) + rule_checklist(rd, items) + rule_monitor(rd)
    out.sort(key=lambda f: (SEVERITY_ORDER[f['severity']], -((f.get('money_at_stake') or {}).get('usd') or -1), f['id']))
    return out
