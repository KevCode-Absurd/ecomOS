"""Security audit (screen 24, round 0). Findings in the shape of app/contracts/audit.md.

Every number comes from app/metrics.py (reversed orders and payouts from data.sqlite); brand facts come from the
brain (app/brain/store.py: stack, policies). No connector, no model call. Same tables, brain and window give the
same findings, byte for byte.

One rule or more per job in the room spec's JTBD table (room "Security", agent MONEY). A rule whose inputs are not
connected emits one `unavailable` finding at the severity it would have when it fires, naming the connector.

Rules
  SEC-R01  Chargeback rate against 3 lines. 30-day chargeback_rate (chargebacks opened over paid orders placed).
           Lines: 0.15 percent, the internal alert set below the processor's flag (room spec, MONEY-C42);
           0.65 percent, the card network early warning program; 0.9 percent, the card network monitoring program
           (metrics.CHARGEBACK_BENCHMARK). Over 0.9: critical. Over 0.65: high. Over 0.15: medium.
           Money: (rate - 0.15 percent) x paid orders x average disputed amount x scale. MONEY-C42.
           Owner: 24-security. Screen 06 owns STORE-R01 (0.9 line and own baseline); this rule owns the ladder.
  SEC-R02  Dispute win rate under the floor. Disputes won over disputes closed in 28 days, under 50 percent
           (rule constant; the room spec gives no line). Medium, high when 2 windows agree.
           Money: (floor - win rate) x closed disputes x average disputed amount x scale. MONEY-C42.
  SEC-R03  Card testing and false declines. Needs `fraud_signals` (failed authorisations per minute, declines
           later confirmed good). Unavailable: payment gateway logs. High. MONEY-C42.
  SEC-R04  Promo code abuse. Needs card fingerprint and address hash per order with the discount code.
           The generator writes neither. Unavailable: Shopify order risk and payments fingerprints. Medium. MONEY-C42.
  SEC-R05  Return abuse. Needs `return_abuse` (refund without a received return, wardrobing notes).
           Unavailable: Shopify returns plus the warehouse receiving log. Medium. MONEY-C76.
  SEC-R06  Account takeover. Needs `admin_access` and customer login events across Shopify, ad accounts, ESP and
           the processor. Unavailable: platform admin logs. High. MONEY-C43.
  SEC-R07  Bot and agent traffic share. Needs `bot_traffic` by endpoint. Unavailable: edge bot analytics. Medium.
           MONEY-C41.
  SEC-R08  Agent commerce endpoint to review. Fires when the brain's stack names an endpoint that lets AI agents
           read the catalog or build a cart (UCP or MCP). A finding to review, not a defect: the policy for which
           agents may act, and at which step a person must approve, has no record yet. Medium. MONEY-C41.
  SEC-R09  Captcha on storefront forms. Fires when the stack has no form captcha record. Medium. MONEY-C41.
  SEC-R10  Web application defects. Needs `security_scan_findings`. Unavailable: weekly scanner. High. MONEY-C44.
  SEC-R11  Third-party scripts on the storefront. Count of stack records seen on the site that load vendor code
           (platform, theme and the agent endpoint are not scripts). Fires over SCRIPT_MAX (5, rule constant: each
           one runs with the page's access, checkout pages included). A tag manager adds a surface that loads more
           code without a deploy. Medium. SITE-C13.
  SEC-R12  Unknown script hosts. Needs a request log by host; speed_runs carries totals only. Unavailable: speed
           lab request log. Medium. SITE-C13.
  SEC-R13  Admin access and 2FA. Needs `admin_access`. Unavailable: Shopify staff list. High. MONEY-C46.
  SEC-R14  Backup restore tested. Needs `backup_log`. Unavailable: backup provider export. Medium. MONEY-C47.
  SEC-R15  Domain, DNS and lookalikes. Needs `dns_records`, `domain_watch`. Unavailable: DNS audit and brand
           monitoring. Medium. MONEY-C48.
  SEC-R16  Consent manager present. Fires when the stack has no consent record. High. MONEY-C49.
  SEC-R17  Privacy policy age. Fires when the brain's effective date is over POLICY_MAX_AGE (365) days before the
           window end (CCPA and CPRA ask for a yearly update). Medium. MONEY-C49.
  SEC-R18  PCI scope confirmed. Needs `pci_scope`. Unavailable: manual assessment. Medium. MONEY-C74.
  SEC-R19  Email authentication. Needs `email_auth` (SPF, DKIM, DMARC). Unavailable: DNS lookup. High. MONEY-C72.
  SEC-R20  Credential rotation. Needs `credential_inventory`. Unavailable: secrets vault export. Medium. MONEY-C73.
  SEC-R21  Phishing simulation. Needs `phishing_sim`. Unavailable: training platform. Low. MONEY-C75.
  SEC-R22  Vendor risk checks. Needs `vendor_risk`. Unavailable: vendor register. Medium. MONEY-C77.

Scale: data.sqlite may hold a sample of the order history (the dev build runs at scale 0.1) while the daily
aggregate holds all of it. Rates are counted inside data.sqlite. Dollar amounts read from data.sqlite are scaled by
paid orders in the aggregate over paid orders in data.sqlite for the same window (1.0 for a live store).
"""
import importlib.util
import re
import sys
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parents[1]
SCREEN = '24-security'
WINDOW = 28
CB_WINDOW = 30
ALERT_LINE = 0.0015       # internal alert below the processor's flag
EARLY_LINE = 0.0065       # card network early warning program
WIN_FLOOR = 0.50          # dispute win rate floor (rule constant)
SCRIPT_MAX = 5            # third-party scripts on the storefront before the surface is flagged
POLICY_MAX_AGE = 365
SCRIPT_FIELDS_OUT = ('platform', 'theme', 'agent_commerce_endpoint')

AUTONOMY = {'MONEY-C41': 'human_assist', 'MONEY-C42': 'human_assist', 'MONEY-C43': 'human_assist',
            'MONEY-C44': 'human_assist', 'MONEY-C46': 'human_assist', 'MONEY-C47': 'human_assist',
            'MONEY-C48': 'human_assist', 'MONEY-C49': 'human_assist', 'MONEY-C50': 'human_assist',
            'MONEY-C72': 'human_assist', 'MONEY-C73': 'founder_gate', 'MONEY-C74': 'founder_gate',
            'MONEY-C75': 'human_assist', 'MONEY-C76': 'human_assist', 'MONEY-C77': 'founder_gate',
            'MONEY-C81': 'founder_gate', 'SITE-C13': 'human_assist'}
SEVERITY_ORDER = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}

# Rules whose inputs are not in the data layer yet: (rule_id, name, entity, severity, capability, inputs, connector,
# fix, sentence). The sentence says what cannot be seen; it is shown with the unavailable tag.
MISSING = [
    ('SEC-R03', 'Card testing and false declines', ('stage', 'checkout_payments', 'Card payments at checkout'), 'high',
     'MONEY-C42', ['fraud_signals'], 'payment gateway logs (failed authorisations, declines)',
     'Connect the gateway log read-only so failed card attempts per minute and declines can be counted.',
     'Failed card attempts and wrongly declined orders cannot be counted. A card-testing burst would show only as chargebacks weeks later.'),
    ('SEC-R04', 'Promo code abuse', ('offer', 'discount_codes', 'Discount codes'), 'medium', 'MONEY-C42',
     ['orders.card_fingerprint', 'orders.address_hash'], 'Shopify order risk and Shopify Payments card fingerprints',
     'Read the order risk and payment fingerprint fields so repeat cards and addresses behind one code show up.',
     'Repeat cards and addresses behind a first-order code cannot be matched. The order table has no card or address fingerprint.'),
    ('SEC-R05', 'Return abuse', ('stage', 'returns', 'Returns and refunds'), 'medium', 'MONEY-C76',
     ['return_abuse'], 'Shopify returns plus the warehouse receiving log',
     'Connect the receiving log so refunds can be matched to items that came back.',
     'Refunds without a received item and serial returners cannot be told apart. There is no receiving log to match against.'),
    ('SEC-R06', 'Account takeover', ('stage', 'admin_logins', 'Staff and customer logins'), 'high', 'MONEY-C43',
     ['admin_access', 'login_events'], 'platform admin logs (Shopify, Meta, ESP, processor)',
     'Connect the admin logs read-only so logins from new places or devices can be compared across systems.',
     'A login from a new place on one system and a permission change on another cannot be seen together. No login log is connected.'),
    ('SEC-R07', 'Bot and agent traffic share', ('stage', 'traffic', 'Site traffic'), 'medium', 'MONEY-C41',
     ['bot_traffic'], 'edge bot analytics (for example Cloudflare)',
     'Connect the edge bot report so the share of automated requests by endpoint is counted.',
     'The share of traffic that is not a person cannot be counted, on checkout or anywhere else. No bot report is connected.'),
    ('SEC-R10', 'Web application defects', ('stage', 'storefront_code', 'Storefront and checkout code'), 'high',
     'MONEY-C44', ['security_scan_findings'], 'weekly automated security scanner',
     'Run a weekly scan of the storefront and checkout and keep its findings with an owner and a fix date.',
     'Nobody has scanned the storefront or checkout code for known defects. Open issues and their age are unknown.'),
    ('SEC-R12', 'Unknown script hosts', ('stage', 'script_hosts', 'Script hosts'), 'medium', 'SITE-C13',
     ['speed_runs.request_hosts'], 'speed lab request log by host',
     'Keep the request list of each lab run so every host that serves code can be named and checked.',
     'Hosts that serve code on the page cannot be listed. The speed lab keeps totals only, not each request.'),
    ('SEC-R13', 'Admin access and 2FA', ('stage', 'admin_access', 'Staff admin access'), 'high', 'MONEY-C46',
     ['admin_access'], 'Shopify admin staff list (read-only)',
     'Connect the staff list so roles, 2FA and last login can be checked for every account.',
     'Who has admin access, with what role and whether 2FA is on, cannot be checked. The staff list is not connected.'),
    ('SEC-R14', 'Backup restore tested', ('stage', 'backups', 'Store backups'), 'medium', 'MONEY-C47',
     ['backup_log'], 'backup provider export',
     'Connect the backup export and log a restore test at least every 30 days.',
     'There is no record of a backup or of a restore that worked. Recovery time after a break is unknown.'),
    ('SEC-R15', 'Domain, DNS and lookalikes', ('stage', 'domain', 'Domain and DNS'), 'medium', 'MONEY-C48',
     ['dns_records', 'domain_watch'], 'DNS audit and brand domain monitoring',
     'Run a DNS audit and a weekly lookalike domain search on the brand name.',
     'Dangling DNS records and new lookalike domains cannot be seen. No DNS audit or domain watch has run.'),
    ('SEC-R18', 'PCI scope confirmed', ('stage', 'pci_scope', 'Payment card scope'), 'medium', 'MONEY-C74',
     ['pci_scope'], 'manual assessment of the payment flow',
     'Record which self-assessment form applies to each payment flow and when it was last confirmed.',
     'Which payment card self-assessment applies, and when it was last confirmed, is not on file.'),
    ('SEC-R19', 'Email authentication', ('stage', 'email_domain', 'Sending domains'), 'high', 'MONEY-C72',
     ['email_auth'], 'DNS lookup of SPF, DKIM and DMARC',
     'Run the DNS lookup for every sending domain and store the DMARC policy.',
     'Whether mail from the brand domain can be faked is unknown. SPF, DKIM and DMARC have not been checked.'),
    ('SEC-R20', 'Credential rotation', ('stage', 'credentials', 'API keys and tokens'), 'medium', 'MONEY-C73',
     ['credential_inventory'], 'secrets vault export or a manual key list',
     'List every key with its holder and last rotation date.',
     'Which keys exist, who holds them and when they were last changed is not on file.'),
    ('SEC-R21', 'Phishing simulation', ('stage', 'staff_training', 'Staff training'), 'low', 'MONEY-C75',
     ['phishing_sim'], 'training platform export',
     'Run a phishing test for staff with admin access and keep the click and report counts.',
     'No phishing test has been run, so how many staff would click a fake login link is unknown.'),
    ('SEC-R22', 'Vendor risk checks', ('stage', 'vendors', 'Vendors with data access'), 'medium', 'MONEY-C77',
     ['vendor_risk'], 'vendor register (manual)',
     'Keep one register of vendors with data access, their risk check and a signed data agreement.',
     'No vendor register exists, so which tools got customer data before a risk check is unknown.'),
]

RULES = [
    {'rule_id': 'SEC-R01', 'name': 'Chargeback rate against the alert and card network lines', 'entity_type': 'metric',
     'inputs': ['orders', 'reversed_orders'], 'capability': 'MONEY-C42', 'owner_screen': SCREEN},
    {'rule_id': 'SEC-R02', 'name': 'Dispute win rate under the floor', 'entity_type': 'metric',
     'inputs': ['orders', 'reversed_orders'], 'capability': 'MONEY-C42', 'owner_screen': SCREEN},
    {'rule_id': 'SEC-R08', 'name': 'Agent commerce endpoint to review', 'entity_type': 'stage',
     'inputs': ['brain.stack'], 'capability': 'MONEY-C41', 'owner_screen': SCREEN},
    {'rule_id': 'SEC-R09', 'name': 'Captcha on storefront forms', 'entity_type': 'stage',
     'inputs': ['brain.stack'], 'capability': 'MONEY-C41', 'owner_screen': SCREEN},
    {'rule_id': 'SEC-R11', 'name': 'Third-party scripts on the storefront', 'entity_type': 'stage',
     'inputs': ['brain.stack'], 'capability': 'SITE-C13', 'owner_screen': SCREEN},
    {'rule_id': 'SEC-R16', 'name': 'Consent manager present', 'entity_type': 'stage',
     'inputs': ['brain.stack'], 'capability': 'MONEY-C49', 'owner_screen': SCREEN},
    {'rule_id': 'SEC-R17', 'name': 'Privacy policy age', 'entity_type': 'stage',
     'inputs': ['brain.policies'], 'capability': 'MONEY-C49', 'owner_screen': SCREEN},
] + [{'rule_id': m[0], 'name': m[1], 'entity_type': m[2][0], 'inputs': m[5], 'capability': m[4],
      'owner_screen': SCREEN} for m in MISSING]
RULES.sort(key=lambda r: r['rule_id'])

_MODS = {}


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def metrics():
    if 'metrics' not in _MODS:
        _MODS['metrics'] = _load('ecomos_metrics_security', APP / 'metrics.py')
    return _MODS['metrics']


def brand_data(brand):
    if 'tables' not in _MODS:
        _MODS['tables'] = _load('ecomos_tables_security', APP / 'data' / 'tables.py')
    return _MODS['tables'].brand_data(brand)


def brain(brand):
    """The brand's brain records, or None when the brand has no brain folder."""
    if not brand or not (APP / 'brain' / brand).is_dir():
        return None
    if 'store' not in _MODS:
        path = str(APP / 'brain')
        if path not in sys.path:
            sys.path.insert(0, path)  # store.py imports validate.py by name
        _MODS['store'] = _load('ecomos_brain_store_security', APP / 'brain' / 'store.py')
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

    def record(self, key):
        """A brain record by `<section>.<key>`, or None."""
        return self._brain.get(f'{self.brand}.{key}') if self._brain and self.brand else None

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


def _ev(metric, value, unit, ends_on, baseline=None, baseline_kind=None, window='30d', source='reversed_orders'):
    return {'metric': metric, 'value': value, 'unit': unit, 'window': window, 'ends_on': ends_on.isoformat(),
            'freshness_days': 1, 'baseline': baseline, 'baseline_kind': baseline_kind, 'source': source,
            'simulated': True}


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


def pct(v, d=2):
    return f'{v * 100:.{d}f} percent'


# ---------------------------------------------------------------- inputs shared with api.py

def chargebacks(rd):
    """30-day chargeback rate against the 3 lines, with the average disputed amount."""
    now = rd.m('chargeback_rate', CB_WINDOW)
    lines = {'alert': ALERT_LINE, 'early_warning': EARLY_LINE, 'network': metrics().CHARGEBACK_BENCHMARK}
    if now.get('unavailable'):
        return {'unavailable': True, 'reason': now['reason'], 'fix': now.get('fix'), 'lines': lines}
    rate, count = now['value'], now['inputs']['numerator']
    over = [k for k, v in lines.items() if rate > v]
    return {'unavailable': False, 'rate': rate, 'chargebacks': count, 'paid_orders': now['inputs']['denominator'],
            'amount': now.get('amount'),
            'avg_amount': round(now['amount'] / count, 2) if count and now.get('amount') else None,
            'by_reason': now.get('by_reason') or [], 'lines': lines, 'over': over,
            'gap_to_alert': round(ALERT_LINE - rate, 6), 'window': now['window']}


def win_rate(rd, end=None):
    w = rd.m('dispute_win_rate', WINDOW, end=end)
    if w.get('unavailable'):
        return {'unavailable': True, 'reason': w['reason'], 'fix': w.get('fix')}
    return {'unavailable': False, 'rate': w['value'], 'won': w['inputs']['numerator'],
            'closed': w['inputs']['denominator'], 'open_now': w.get('open_now'), 'window': w['window']}


def win_windows(rd, n=4):
    """Win rate for the current 28 days and the n-1 windows before it."""
    return [win_rate(rd, rd.ends_on - timedelta(days=WINDOW * k)) for k in range(n)]


def avg_disputed(rd):
    """Average disputed amount of chargebacks opened in the 28-day window, or None."""
    c = rd.m('chargeback_rate', WINDOW)
    if c.get('unavailable') or not c['inputs']['numerator'] or not c.get('amount'):
        return None
    return round(c['amount'] / c['inputs']['numerator'], 2)


def payouts(rd):
    p = rd.m('payout_reversals', WINDOW)
    if p.get('unavailable'):
        return {'unavailable': True, 'reason': p['reason'], 'fix': p.get('fix')}
    scale = rd.scale()
    return {'unavailable': False, 'adjustments': p['value'], 'refunds': p.get('refunds_gross'), 'scale': scale,
            'adjustments_scaled': None if scale is None else round(p['value'] * scale, 2),
            'charges': p.get('charges_gross'), 'net': p.get('net'), 'payouts': p['inputs']['payouts'],
            'window': p['window'], 'holds': None,
            'holds_reason': 'payouts carry no hold or reserve field; a held payout needs the processor balance feed'}


_HOST = re.compile(r'(?:https?:)?//([a-z0-9.-]+\.[a-z]{2,})', re.I)


def scripts(rd):
    """Stack records seen on the storefront that load vendor code, with the hosts their evidence names."""
    rows = []
    for r in rd.records('stack'):
        field = r.get('field') or ''
        if field in SCRIPT_FIELDS_OUT or field.startswith('platform') or (r.get('source') or {}).get('type') != 'site':
            continue
        hosts = sorted({h.lower() for e in (r.get('evidence') or []) for h in _HOST.findall(str(e.get('quote') or ''))})
        rows.append({'field': field, 'tool': r.get('value') if isinstance(r.get('value'), str) else None,
                     'text': r.get('text'), 'hosts': hosts, 'ref': r['id'], 'seen': (r.get('source') or {}).get('captured_at')})
    rows.sort(key=lambda x: x['field'])
    return {'rows': rows, 'count': len(rows), 'max': SCRIPT_MAX,
            'tag_manager': any(x['field'] == 'tag_manager' for x in rows),
            'hosts_named': sorted({h for x in rows for h in x['hosts']}),
            'unknown_hosts': None,
            'unknown_reason': 'speed_runs keeps totals per run, not each request, so hosts outside the stack records cannot be listed'}


def controls(rd):
    """Consent, captcha, privacy policy age and the agent endpoint, each from one brain record."""
    cmp_ = rd.record('stack.cookie_consent')
    cap = rd.record('stack.form_security')
    agent = rd.record('stack.agent_commerce_endpoint')
    priv = rd.record('policies.privacy_effective_date')
    age = None
    if priv and priv.get('value'):
        age = (rd.ends_on - date.fromisoformat(str(priv['value'])[:10])).days
    return {'consent': {'present': bool(cmp_), 'tool': cmp_.get('value') if cmp_ else None,
                        'ref': cmp_['id'] if cmp_ else None},
            'captcha': {'present': bool(cap), 'tool': cap.get('value') if cap else None,
                        'ref': cap['id'] if cap else None},
            'agent_endpoint': {'present': bool(agent), 'text': agent.get('text') if agent else None,
                               'value': agent.get('value') if agent else None, 'ref': agent['id'] if agent else None,
                               'url': (agent.get('source') or {}).get('ref') if agent else None},
            'privacy': {'effective': priv.get('value') if priv else None, 'age_days': age, 'max_days': POLICY_MAX_AGE,
                        'ref': priv['id'] if priv else None}}


# ---------------------------------------------------------------- rules

def rule_chargeback(rd):
    end = rd.ends_on
    cb = chargebacks(rd)
    if cb['unavailable']:
        return [_finding('SEC-R01', {'type': 'metric', 'id': 'chargeback_rate', 'label': 'Chargeback rate'}, 'medium',
                         [], 'The chargeback rate cannot be counted.', 'MONEY-C42', None, 0.5, [], end,
                         status='unavailable', unavailable={'inputs': ['orders', 'reversed_orders'],
                                                            'connector': 'Shopify orders and payments disputes',
                                                            'fix': cb.get('fix') or cb['reason']},
                         money_reason='chargebacks unavailable')]
    if not cb['over']:
        return []
    top = cb['over'][-1]
    sev = {'network': 'critical', 'early_warning': 'high', 'alert': 'medium'}[top]
    evidence = [_ev('chargeback_rate', cb['rate'], 'ratio', end, baseline=v, baseline_kind='threshold')
                for k, v in cb['lines'].items()]
    scale = rd.scale(CB_WINDOW)
    money, reason = None, None
    if cb['avg_amount'] is None or scale is None:
        reason = 'average disputed amount or order totals unavailable'
    else:
        excess = (cb['rate'] - ALERT_LINE) * cb['paid_orders']
        money = {'usd': round(max(0.0, excess * cb['avg_amount'] * scale), 2),
                 'formula': '(rate_now - alert_line) x paid_orders x avg_disputed_amount x scale',
                 'inputs': {'rate_now': cb['rate'], 'alert_line': ALERT_LINE, 'paid_orders': cb['paid_orders'],
                            'avg_disputed_amount': cb['avg_amount'], 'scale': scale}, 'window': '30d'}
    label = {'network': 'the 0.9 percent card network line', 'early_warning': 'the 0.65 percent early warning line',
             'alert': 'the 0.15 percent alert line'}[top]
    s = f'Chargebacks are {pct(cb["rate"])} of paid orders in 30 days, over {label}.'
    return [_finding('SEC-R01', {'type': 'metric', 'id': 'chargeback_rate', 'label': 'Chargeback rate'}, sev, evidence,
                     s, 'MONEY-C42', money, 0.5, [], end, money_reason=reason)]


def rule_win_rate(rd):
    end = rd.ends_on
    ws = win_windows(rd)
    now = ws[0]
    entity = {'type': 'metric', 'id': 'dispute_win_rate', 'label': 'Dispute win rate'}
    if now['unavailable']:
        return [_finding('SEC-R02', entity, 'medium', [], 'The dispute win rate cannot be counted.', 'MONEY-C42', None,
                         0.5, [], end, status='unavailable',
                         unavailable={'inputs': ['reversed_orders'], 'connector': 'Shopify Payments disputes',
                                      'fix': now.get('fix') or now['reason']}, money_reason='disputes unavailable')]
    if not now['closed'] or now['rate'] >= WIN_FLOOR:
        return []
    agree = sum(1 for w in ws if not w['unavailable'] and w['closed'] and w['rate'] < WIN_FLOOR)
    evidence = [_ev('dispute_win_rate', now['rate'], 'ratio', end, baseline=WIN_FLOOR, baseline_kind='threshold',
                    window='28d'),
                _ev('disputes_closed', now['closed'], 'count', end, window='28d')]
    avg = avg_disputed(rd)
    scale = rd.scale()
    money, reason = None, None
    if avg is None or scale is None:
        reason = 'average disputed amount or order totals unavailable'
    else:
        money = {'usd': round(max(0.0, (WIN_FLOOR - now['rate']) * now['closed'] * avg * scale), 2),
                 'formula': '(win_floor - win_rate) x disputes_closed x avg_disputed_amount x scale',
                 'inputs': {'win_floor': WIN_FLOOR, 'win_rate': now['rate'], 'disputes_closed': now['closed'],
                            'avg_disputed_amount': avg, 'scale': scale}, 'window': '28d'}
    sev = 'high' if agree >= 2 else 'medium'
    conf = 0.9 if agree >= 4 else 0.7 if agree >= 2 else 0.5
    s = (f'The store won {now["won"]:,} of {now["closed"]:,} disputes closed in 28 days, {pct(now["rate"], 0)}. '
         f'The floor is {pct(WIN_FLOOR, 0)} and {agree} of the last 4 windows were under it.')
    return [_finding('SEC-R02', entity, sev, evidence, s, 'MONEY-C42', money, conf, [], end, money_reason=reason)]


def rule_agent_endpoint(rd, ctl):
    end = rd.ends_on
    a = ctl['agent_endpoint']
    if not a['present']:
        return []
    evidence = [_ev('agent_endpoint_published', 1, 'flag', end, baseline=0, baseline_kind='threshold', window='as of',
                    source=a['ref'])]
    s = ('The store publishes an endpoint that lets AI agents read the catalog and build a cart. '
         'No record says which agents may use it or where a person must approve.')
    return [_finding('SEC-R08', {'type': 'stage', 'id': 'agent_endpoint', 'label': 'AI shopping agent endpoint'},
                     'medium', evidence, s, 'MONEY-C41', None, 0.5, [a['ref']], end,
                     money_reason='a finding to review: no agent traffic or order data to price')]


def rule_captcha(rd, ctl):
    if ctl['captcha']['present']:
        return []
    end = rd.ends_on
    return [_finding('SEC-R09', {'type': 'stage', 'id': 'form_captcha', 'label': 'Captcha on storefront forms'},
                     'medium', [_ev('form_captcha_present', 0, 'flag', end, baseline=1, baseline_kind='threshold',
                                    window='as of', source='brain.stack')],
                     'No captcha is recorded on the login and contact forms.', 'MONEY-C41', None, 0.5, [], end,
                     money_reason='no bot traffic data to price')]


def rule_scripts(rd, sc):
    end = rd.ends_on
    if sc['count'] <= SCRIPT_MAX:
        return []
    evidence = [_ev('third_party_scripts', sc['count'], 'count', end, baseline=SCRIPT_MAX, baseline_kind='threshold',
                    window='as of', source='brain.stack')]
    s = f'{sc["count"]} vendor scripts run on the storefront, over the line of {SCRIPT_MAX}.'
    if sc['tag_manager']:
        s += ' A tag manager can add more without a site change.'
    return [_finding('SEC-R11', {'type': 'stage', 'id': 'storefront_scripts', 'label': 'Third-party scripts'},
                     'medium', evidence, s, 'SITE-C13', None, 0.5, [r['ref'] for r in sc['rows']], end,
                     money_reason='no per-script cost or incident data to price')]


def rule_consent(rd, ctl):
    if ctl['consent']['present']:
        return []
    end = rd.ends_on
    return [_finding('SEC-R16', {'type': 'stage', 'id': 'consent_manager', 'label': 'Consent manager'}, 'high',
                     [_ev('consent_manager_present', 0, 'flag', end, baseline=1, baseline_kind='threshold',
                          window='as of', source='brain.stack')],
                     'No consent manager is recorded on the storefront.', 'MONEY-C49', None, 0.5, [], end,
                     money_reason='no fine or complaint data to price')]


def rule_privacy(rd, ctl):
    end = rd.ends_on
    p = ctl['privacy']
    entity = {'type': 'stage', 'id': 'privacy_policy', 'label': 'Privacy policy'}
    if p['age_days'] is None:
        return [_finding('SEC-R17', entity, 'medium', [], 'The privacy policy date is not on file.', 'MONEY-C49', None,
                         0.5, [], end, status='unavailable',
                         unavailable={'inputs': ['brain.policies.privacy_effective_date'],
                                      'connector': 'brand brain (site capture of the privacy page)',
                                      'fix': 'Capture the privacy page and record its effective date.'},
                         money_reason='no policy date')]
    if p['age_days'] <= POLICY_MAX_AGE:
        return []
    return [_finding('SEC-R17', entity, 'medium',
                     [_ev('privacy_policy_age_days', p['age_days'], 'days', end, baseline=POLICY_MAX_AGE,
                          baseline_kind='threshold', window='as of', source=p['ref'])],
                     f'The privacy policy took effect {p["effective"]}, {p["age_days"]} days ago. The line is '
                     f'{POLICY_MAX_AGE} days.', 'MONEY-C49', None, 0.7, [p['ref']], end,
                     money_reason='no fine or complaint data to price')]


def rule_missing(rd):
    end = rd.ends_on
    out = []
    for rid, name, (etype, eid, label), sev, cap, inputs, connector, fix, sentence in MISSING:
        if all('.' not in t and rd.table(t) for t in inputs):
            continue  # a connected table is read by the round that builds this rule's metric
        out.append(_finding(rid, {'type': etype, 'id': eid, 'label': label}, sev, [], sentence, cap, None, 0.5, [], end,
                            status='unavailable', unavailable={'inputs': inputs, 'connector': connector, 'fix': fix},
                            money_reason=f'{name.lower()}: inputs not connected'))
    return out


def run(brand, window=None, data=None):
    """Findings for one brand, sorted by severity then money at stake. `window` is {ends_on} or None."""
    ends_on = date.fromisoformat(window['ends_on']) if window and window.get('ends_on') else last_full_day(data, brand)
    return findings(Reader(data, brand, ends_on))


def findings(rd):
    """run() on a Reader the caller already holds, so api.py reuses its metric calls."""
    ctl, sc = controls(rd), scripts(rd)
    out = (rule_chargeback(rd) + rule_win_rate(rd) + rule_agent_endpoint(rd, ctl) + rule_captcha(rd, ctl)
           + rule_scripts(rd, sc) + rule_consent(rd, ctl) + rule_privacy(rd, ctl) + rule_missing(rd))
    out.sort(key=lambda f: (SEVERITY_ORDER[f['severity']], f['status'] == 'unavailable',
                            -((f.get('money_at_stake') or {}).get('usd') or -1), f['id']))
    return out
