"""Email and messaging audit (screen 14, round 0). Findings in the shape of app/contracts/audit.md.

Inputs are the Klaviyo-shaped `flows` and `campaign_sends` tables, paid orders and `inventory` from the
brand's data.sqlite, plus the brain (`calendar`, `offers`). Order-matched flow revenue and list growth come
from app/metrics.py. The generator names the flow column `flow_name` and stores `matched_order_ids` as JSON
text, so `EmailData` hands metrics.py the contract names (`flow`, a list) and reads order rows for the
window only. No connector, no model call. Same tables and window give the same findings, byte for byte.

Rules (one per insight in the room spec, ids fixed; all owned by 14-email-messaging)
  EMAIL-R01  Flow revenue mismatch: platform-reported revenue for a flow differs from order-matched revenue
             by more than 15 percent, for a flow with 20 or more matched orders in 28 days. Money: null,
             a reporting gap is not lost revenue. Capability LIFE-C20.
  EMAIL-R02  Quiet hours breach. Unavailable: the send log has no per-contact send time or market.
  EMAIL-R03  Flow collision. Unavailable: needs contact-level sends (esp_sends).
  EMAIL-R04  Deliverability drop. Unavailable: the feed has bounces but no spam complaints, and placement
             without complaints would read complaints as 0.
  EMAIL-R05  Stale segment. Unavailable: no `segments` table.
  EMAIL-R06  Discount fired too early. Unavailable: no `flow_defs` with the discount step.
  EMAIL-R07  Consent gap. Unavailable: needs contact-level sends against a consent log.
  EMAIL-R08  List decay. Unavailable: needs 180 days of contact-level opens and clicks.
  EMAIL-R09  WhatsApp underused for high-value sends. Unavailable: no `whatsapp_events`.
  EMAIL-R10  Welcome flow drop-off: the fall between 2 consecutive welcome messages (sends, all channels,
             28 days) is more than 2 times the flow's average step drop. Needs 3 or more messages. Money:
             (drop - average drop) x sends at the earlier step x order-matched revenue per welcome send.
             Capability LIFE-C04.
  EMAIL-R11  Win-back timing off brand cadence. Unavailable: the trigger delay lives in `flow_defs`.
  EMAIL-R12  Sunset not enforced, audience proxy: email campaigns in 28 days went to an audience larger
             than the engaged segment (`Engaged 90d`) and no live flow is named sunset. The spec's
             per-contact test (6 unopened sends in a row) needs esp_sends; this proxy counts contacts
             outside the engaged segment, so confidence carries the 0.2 proxy penalty. Money: contacts
             outside the segment x the broad send's unsubscribe and bounce rate, summed over broad sends,
             x order-matched flow revenue per engaged subscriber in 28 days. Capability LIFE-C08.
  EMAIL-R13  Test hygiene. Unavailable: no `test_registry`.
  EMAIL-R14  Honesty: a campaign in 28 days whose name claims a deadline or scarcity ("last call", "last
             chance", "ends", "only", "selling out") with no brain `calendar` or `offers` record dated from
             the send to 60 days after it. Money: null, a trust risk with no order count. Capability LOOP-C12.
  EMAIL-R15  Back-in-stock false trigger: a campaign in 28 days named restock or back in stock with no SKU
             whose on-hand units rose in the 24 hours before the send (`inventory`, summed over locations).
             Money: null. Capability LIFE-C11.
"""
import importlib.util
import json
import re
import statistics
import sys
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parents[1]
SCREEN = '14-email-messaging'

WINDOW = 28
TRAILING = 4
MISMATCH_PCT = 0.15
MISMATCH_MIN_ORDERS = 20
WELCOME_DROP_TIMES = 2
ENGAGED_AUDIENCE = 'Engaged 90d'
CLAIM_AHEAD_DAYS = 60
SCARCITY = re.compile(r'\b(last call|last chance|ends (today|tonight|soon|sunday|monday)|only \d+ left|selling out|final hours)\b', re.I)
RESTOCK = re.compile(r'\b(restock|back in stock)\b', re.I)

CAP = {'LIFE-C03': 'founder_gate', 'LIFE-C04': 'founder_gate', 'LIFE-C06': 'founder_gate', 'LIFE-C08': 'founder_gate',
       'LIFE-C11': 'founder_gate', 'LIFE-C12': 'founder_gate', 'LIFE-C16': 'founder_gate', 'LIFE-C17': 'founder_gate',
       'LIFE-C19': 'agent_does', 'LIFE-C20': 'agent_does', 'LOOP-C12': 'agent_does'}

# rule_id, name, entity type, inputs, capability, severity when it fires, unavailable text (None when computable)
_SPEC = [
    ('EMAIL-R01', 'Flow revenue in the ESP differs from real orders by more than 15 percent', 'flow',
     ['flows', 'orders'], 'LIFE-C20', 'medium', None),
    ('EMAIL-R02', 'Messages sent outside allowed local hours', 'brand', ['esp_sends.sent_at', 'consent_log.market'],
     'LIFE-C03', 'high', ('Quiet hours cannot be checked: the send log has no send time or market per contact.',
                          'klaviyo_events', 'Connect the ESP event export with send time per contact.')),
    ('EMAIL-R03', 'Contacts messaged by 2 or more flows on the same day', 'brand', ['esp_sends.contact_id', 'esp_sends.flow_id'],
     'LIFE-C12', 'medium', ('Flow collisions cannot be counted: sends are daily totals, not per contact.',
                            'klaviyo_events', 'Connect the ESP event export with contact and flow per send.')),
    ('EMAIL-R04', 'Inbox placement down more than 5 points against its 30-day average', 'metric',
     ['flows.bounces', 'esp_sends.spam_complaints'], 'LIFE-C16', 'high',
     ('Inbox placement cannot be computed: the feed has bounces but no spam complaints.',
      'klaviyo_events', 'Connect the ESP complaint feed (Marked as Spam events).')),
    ('EMAIL-R05', 'Segment feeding a live flow not recomputed in 7 days', 'brand', ['segments.last_computed_at'],
     'LIFE-C12', 'medium', ('Segment freshness cannot be checked: there is no segments table.',
                            'klaviyo_segments', 'Connect ESP segments with their last computed date.')),
    ('EMAIL-R06', 'Abandonment flow offers a discount on message 1', 'flow', ['flow_defs.discount_step_index'],
     'LIFE-C06', 'medium', ('Discount timing cannot be checked: flow steps and offers are not on file.',
                            'klaviyo_flows', 'Connect ESP flow definitions or enter the discount step per flow.')),
    ('EMAIL-R07', 'Sends to contacts with no valid consent on that channel', 'brand', ['consent_log', 'esp_sends.contact_id'],
     'LIFE-C03', 'high', ('Consent gaps cannot be counted: sends are not logged per contact.',
                          'klaviyo_events', 'Connect the ESP consent API and the per-contact send log.')),
    ('EMAIL-R08', 'More than 35 percent of the list not engaged in 180 days', 'brand', ['esp_sends.opened', 'esp_sends.clicked'],
     'LIFE-C16', 'medium', ('List decay cannot be measured: opens and clicks are daily totals, not per contact.',
                            'klaviyo_profiles', 'Connect ESP profiles with last open and last click dates.')),
    ('EMAIL-R09', 'High-value sends used SMS or email although the contact opted into WhatsApp', 'brand', ['whatsapp_events'],
     'LIFE-C17', 'low', ('WhatsApp use cannot be checked: there is no WhatsApp events log.',
                         'whatsapp_bsp', 'Connect the WhatsApp Business account export, if the brand uses it.')),
    ('EMAIL-R10', 'Welcome flow step drop more than 2 times the average step drop', 'flow', ['flows'],
     'LIFE-C04', 'medium', None),
    ('EMAIL-R11', 'Win-back fires on a default delay, not the brand repeat cadence', 'flow', ['flow_defs.trigger_rule', 'orders'],
     'LIFE-C08', 'medium', ('Win-back timing cannot be checked: the flow trigger delay is not on file.',
                            'klaviyo_flows', 'Connect ESP flow definitions or enter the win-back delay.')),
    ('EMAIL-R12', 'Campaigns mailed beyond the engaged segment with no sunset flow', 'brand', ['campaign_sends', 'flows'],
     'LIFE-C08', 'medium', None),
    ('EMAIL-R13', 'Test called before its sample or read window', 'brand', ['test_registry'],
     'LIFE-C19', 'low', ('Test hygiene cannot be checked: there is no test registry.',
                         'test_registry', 'Log each email and SMS test with its sample size and read window.')),
    ('EMAIL-R14', 'Deadline or scarcity claim with no calendar or offer record behind it', 'campaign',
     ['campaign_sends', 'brain.calendar', 'brain.offers'], 'LOOP-C12', 'medium', None),
    ('EMAIL-R15', 'Restock send with no restock in inventory', 'campaign', ['campaign_sends', 'inventory'],
     'LIFE-C11', 'medium', None),
]
RULES = [{'rule_id': r, 'name': n, 'entity_type': t, 'inputs': i, 'capability': c, 'owner_screen': SCREEN}
         for r, n, t, i, c, _, _ in _SPEC]
SPEC = {s[0]: s for s in _SPEC}
SEVERITY_ORDER = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_MODS = {}


def metrics():
    if 'metrics' not in _MODS:
        _MODS['metrics'] = _load('ecomos_metrics_email', APP / 'metrics.py')
    return _MODS['metrics']


def brand_data(brand):
    if 'tables' not in _MODS:
        _MODS['tables'] = _load('ecomos_tables_email', APP / 'data' / 'tables.py')
    return _MODS['tables'].brand_data(brand)


def brain(brand):
    if 'store' not in _MODS:
        brain_dir = str(APP / 'brain')
        if brain_dir not in sys.path:
            sys.path.insert(0, brain_dir)
        _MODS['store'] = _load('ecomos_brain_store_email', APP / 'brain' / 'store.py')
    try:
        return _MODS['store'].Brain(brand)
    except (FileNotFoundError, ValueError, KeyError):
        return None


class EmailData:
    """The brand's data layer with the email tables in contract names and order rows for one span.

    flows and campaign_sends: `flow` is `flow_name`, `sent_at` is `send_time` (flows: the day),
    `matched_order_ids` a list. orders: paid-state rows
    created on or after `since` (status read as financial_status), from data.sqlite with one query.
    Everything else is the brand folder unchanged. Missing data.sqlite raises KeyError: unavailable."""

    def __init__(self, bd, since):
        self._bd, self._since, self._cache = bd, since, {}

    def __getattr__(self, name):
        return getattr(self._bd, name)

    def table(self, name):
        if name in self._cache:
            return self._cache[name]
        if name in ('flows', 'campaign_sends'):
            rows = [dict(r, flow=r.get('flow_name'), sent_at=r.get('send_time', r.get('date')),
                         matched_order_ids=json.loads(r.get('matched_order_ids') or '[]'))
                    for r in self._bd.table(name)]
        elif name == 'orders':
            rows = self._bd._sql('SELECT id, created_at, customer_id, status AS financial_status, subtotal, discount '
                                 f"FROM orders WHERE created_at >= '{self._since.isoformat()}' ORDER BY id")
        else:
            rows = self._bd.table(name)
        self._cache[name] = rows
        return rows


_DATA = {}


def email_data(brand, ends_on):
    since = ends_on - timedelta(days=WINDOW * 2 + 1)
    bd = brand_data(brand)
    key = (brand, since, bd.sqlite.stat().st_mtime if bd.sqlite.is_file() else None)
    if key not in _DATA:
        _DATA.clear()
        _DATA[key] = EmailData(bd, since)
    return _DATA[key]


def last_full_day(brand):
    return date.fromisoformat(brand_data(brand).brand['as_of'])


class Reader:
    """One brand, one window end. m() is metrics.compute on EmailData; rows() reads a table or None."""

    def __init__(self, brand, ends_on):
        self.brand, self.ends_on = brand, ends_on
        self.data = email_data(brand, ends_on)

    def m(self, name, days=WINDOW, end=None, **kw):
        return metrics().compute(name, self.data, window=f'{days}d', end=(end or self.ends_on).isoformat(), **kw)

    def rows(self, name):
        try:
            return self.data.table(name)
        except (KeyError, ValueError):
            return None

    def span(self, days=WINDOW, end=None):
        end = end or self.ends_on
        return (end - timedelta(days=days - 1)).isoformat(), end.isoformat()


# ---------------------------------------------------------------- aggregates in code

def _msg_num(mid):
    m = re.search(r'(\d+)$', str(mid))
    return int(m.group(1)) if m else 0


def flow_stats(rd, end=None):
    """Per flow: sends, opens, clicks, unsubscribes, bounces, platform revenue and orders, 28 days. None when flows is absent."""
    rows = rd.rows('flows')
    if rows is None:
        return None
    s, e = rd.span(end=end)
    out = {}
    for r in rows:
        if not (s <= str(r['date']) <= e):
            continue
        f = out.setdefault(r['flow'], {'flow': r['flow'], 'flow_id': r.get('flow_id'), 'status': r.get('flow_status'),
                                       'channels': set(), 'messages': {}, 'sends': 0, 'opens': 0, 'email_sends': 0,
                                       'clicks': 0, 'unsubscribes': 0, 'bounces': 0, 'platform_revenue': 0.0,
                                       'platform_orders': 0})
        f['channels'].add(r['channel'])
        f['messages'][r['message_id']] = f['messages'].get(r['message_id'], 0) + (r['sends'] or 0)
        for k in ('sends', 'clicks', 'unsubscribes', 'bounces'):
            f[k] += r[k] or 0
        if r['channel'] == 'email':
            f['email_sends'] += r['sends'] or 0
            f['opens'] += r['opens'] or 0
        f['platform_revenue'] += r['attributed_revenue'] or 0
        f['platform_orders'] += r['attributed_orders'] or 0
    for f in out.values():
        f['channels'] = sorted(f['channels'])
        f['platform_revenue'] = round(f['platform_revenue'], 2)
        f['steps'] = [{'message_id': k, 'sends': v} for k, v in sorted(f['messages'].items(), key=lambda kv: _msg_num(kv[0]))]
        del f['messages']
    return out


def campaigns(rd, end=None, channel=None):
    """Campaigns sent in the window, one row each: send-day counts plus platform revenue over all its rows."""
    rows = rd.rows('campaign_sends')
    if rows is None:
        return None
    s, e = rd.span(end=end)
    out = {}
    for r in rows:
        sent = str(r.get('send_time') or '')[:10]
        if not (s <= sent <= e) or (channel and r['channel'] != channel):
            continue
        c = out.setdefault(r['campaign_id'], {'campaign_id': r['campaign_id'], 'name': r['campaign_name'],
                                              'subject': r.get('subject'), 'channel': r['channel'], 'sent_on': sent,
                                              'audience': r.get('audiences'), 'sends': 0, 'opens': 0, 'clicks': 0,
                                              'unsubscribes': 0, 'bounces': 0, 'platform_revenue': 0.0})
        for k in ('sends', 'opens', 'clicks', 'unsubscribes', 'bounces'):
            c[k] += r.get(k) or 0
        c['platform_revenue'] += r.get('attributed_revenue') or 0
    for c in out.values():
        c['platform_revenue'] = round(c['platform_revenue'], 2)
    return sorted(out.values(), key=lambda c: (c['sent_on'], c['campaign_id']))


def unsubscribe_rate(rd, end=None):
    """Email campaign unsubscribes over delivered (sends minus bounces), 28 days. None when no campaign sent."""
    cs = campaigns(rd, end, channel='email')
    if not cs:
        return None
    unsub = sum(c['unsubscribes'] for c in cs)
    delivered = sum(c['sends'] - c['bounces'] for c in cs)
    return {'value': round(unsub / delivered, 6) if delivered else None, 'unsubscribes': unsub,
            'delivered': delivered, 'campaigns': len(cs)}


# ---------------------------------------------------------------- findings

def _ev(metric, value, unit, ends_on, baseline=None, baseline_kind=None, window=f'{WINDOW}d', source='flows', **extra):
    out = {'metric': metric, 'value': value, 'unit': unit, 'window': window, 'ends_on': ends_on.isoformat(),
           'freshness_days': 1, 'baseline': baseline, 'baseline_kind': baseline_kind, 'source': source, 'simulated': True}
    out.update(extra)
    return out


def _confidence(windows_agree, penalty=0.0):
    base = 0.9 if windows_agree >= 4 else 0.7 if windows_agree >= 2 else 0.5
    return round(max(base - penalty, 0.1), 2)


def _severity(stake, net_28d, windows_agree, floor='medium'):
    if stake is not None and net_28d and stake > 0.05 * net_28d:
        return 'critical'
    if windows_agree >= 2 or (stake is not None and net_28d and stake > 0.01 * net_28d):
        return 'high'
    return floor


def _finding(rule_id, entity, ends_on, severity, evidence, sentence, stake, confidence, brain_refs=(), money_reason=None):
    cap = SPEC[rule_id][4]
    out = {'id': f'{SCREEN}.{rule_id}.{entity["id"]}', 'screen': SCREEN, 'rule_id': rule_id, 'severity': severity,
           'entity': entity, 'evidence': evidence, 'sentence': sentence,
           'capability': {'id': cap, 'autonomy': CAP[cap]}, 'money_at_stake': stake, 'confidence': confidence,
           'brain_refs': list(brain_refs), 'first_seen': ends_on.isoformat(), 'last_seen': ends_on.isoformat(),
           'status': 'open', 'unavailable': None}
    if stake is None:
        out['money_reason'] = money_reason or 'no baseline'
    return out


def _unavailable(rule_id, ends_on, sentence=None, inputs=None, connector=None, fix=None):
    rid, _, etype, spec_inputs, cap, sev, text = SPEC[rule_id]
    sentence, connector, fix = (sentence or text[0], connector or text[1], fix or text[2])
    return {'id': f'{SCREEN}.{rule_id}.brand', 'screen': SCREEN, 'rule_id': rule_id, 'severity': sev,
            'entity': {'type': 'brand', 'id': 'brand', 'label': 'Email and SMS program'}, 'evidence': [],
            'sentence': sentence, 'capability': {'id': cap, 'autonomy': CAP[cap]}, 'money_at_stake': None,
            'confidence': 0.1, 'brain_refs': [],
            'first_seen': ends_on.isoformat(), 'last_seen': ends_on.isoformat(), 'status': 'unavailable',
            'unavailable': {'inputs': list(inputs or spec_inputs), 'connector': connector, 'fix': fix},
            'money_reason': 'inputs unavailable'}


def mismatch_rows(stats, matched):
    """Per flow: platform revenue, order-matched revenue, gap. matched is the metric's by_flow list."""
    by = {g['flow']: g for g in matched.get('by_flow') or []}
    out = []
    for name, f in sorted(stats.items(), key=lambda kv: kv[1]['flow_id'] or kv[0]):
        g = by.get(name)
        m_rev = g['net_revenue'] if g else None
        gap = round(f['platform_revenue'] / m_rev - 1, 4) if m_rev else None
        out.append({'flow': name, 'flow_id': f['flow_id'], 'platform_revenue': f['platform_revenue'],
                    'platform_orders': f['platform_orders'], 'matched_revenue': m_rev,
                    'matched_orders': g['orders'] if g else None, 'gap': gap})
    return out


def r01(rows, ends_on):
    out = []
    for r in rows:
        if r['gap'] is None or (r['matched_orders'] or 0) < MISMATCH_MIN_ORDERS or abs(r['gap']) <= MISMATCH_PCT:
            continue
        pct = abs(round(r['gap'] * 100))
        ev = [_ev('platform_flow_revenue', r['platform_revenue'], 'usd', ends_on),
              _ev('order_matched_flow_revenue', r['matched_revenue'], 'usd', ends_on, source='orders'),
              _ev('revenue_gap', r['gap'], 'ratio', ends_on, MISMATCH_PCT, 'threshold'),
              _ev('matched_orders', r['matched_orders'], 'count', ends_on, MISMATCH_MIN_ORDERS, 'threshold', source='orders')]
        sentence = (f'{r["flow"]} shows ${r["platform_revenue"]:,.0f} in your email platform but ${r["matched_revenue"]:,.0f} '
                    f'in real orders over 28 days, a {pct} percent gap.')
        out.append(_finding('EMAIL-R01', {'type': 'flow', 'id': r['flow_id'], 'label': r['flow']}, ends_on, 'medium', ev,
                            sentence, None, _confidence(1), money_reason='reporting gap, not lost revenue'))
    return out


def welcome(stats):
    return next((f for n, f in sorted(stats.items()) if 'welcome' in n.lower()), None)


def r10(stats, matched, ends_on, net_28d):
    f = welcome(stats)
    if not f or len(f['steps']) < 3:
        return []
    steps = f['steps']
    drops = [1 - steps[i + 1]['sends'] / steps[i]['sends'] if steps[i]['sends'] else None for i in range(len(steps) - 1)]
    if any(d is None for d in drops):
        return []
    avg = statistics.mean(drops)
    out = []
    by = {g['flow']: g for g in matched.get('by_flow') or []}
    for i, d in enumerate(drops):
        if avg <= 0 or d <= WELCOME_DROP_TIMES * avg:
            continue
        a, b = steps[i], steps[i + 1]
        g = by.get(f['flow'])
        stake = None
        if g and f['sends']:
            per_send = round(g['net_revenue'] / f['sends'], 4)
            usd = round(max(d - avg, 0) * a['sends'] * per_send)
            stake = {'usd': usd, 'formula': '(step_drop - average_step_drop) x sends_at_step_a x matched_revenue_per_welcome_send',
                     'inputs': {'step_drop': round(d, 4), 'average_step_drop': round(avg, 4), 'sends_at_step_a': a['sends'],
                                'matched_revenue_per_welcome_send': per_send}, 'window': f'{WINDOW}d'}
        ev = [_ev('step_drop', round(d, 4), 'ratio', ends_on, round(avg, 4), 'own_median', note='baseline is the average step drop in this flow'),
              _ev('sends_step_a', a['sends'], 'count', ends_on), _ev('sends_step_b', b['sends'], 'count', ends_on)]
        sentence = (f'{round(d * 100)} percent of new subscribers drop off between welcome message {i + 1} and {i + 2}. '
                    f'The average step loses {round(avg * 100)} percent.')
        out.append(_finding('EMAIL-R10', {'type': 'flow', 'id': f'{f["flow_id"]}.{a["message_id"]}', 'label': f'{f["flow"]}, {a["message_id"]} to {b["message_id"]}'},
                            ends_on, _severity(stake and stake['usd'], net_28d, 1), ev, sentence, stake, _confidence(1)))
    return out


def broad_sends(rd, end=None):
    """Email campaigns in the window sent to more people than the engaged segment. None when no engaged send exists."""
    cs = campaigns(rd, end, channel='email') or []
    engaged = [c['sends'] for c in cs if c['audience'] == ENGAGED_AUDIENCE and c['sends']]
    if not engaged:
        return None, []
    size = max(engaged)
    return size, [c for c in cs if c['audience'] != ENGAGED_AUDIENCE and c['sends'] > size]


def r12(rd, stats, matched, ends_on, net_28d):
    if any('sunset' in n.lower() and (f['status'] or 'live') == 'live' for n, f in stats.items()):
        return []
    size, broad = broad_sends(rd)
    if not broad:
        return []
    agree = 1 + sum(1 for k in range(1, TRAILING) if broad_sends(rd, ends_on - timedelta(days=WINDOW * k))[1])
    outside = max(c['sends'] - size for c in broad)
    lost = sum((c['sends'] - size) * (c['unsubscribes'] + c['bounces']) / c['sends'] for c in broad)
    stake = None
    if not matched.get('unavailable') and matched.get('value'):
        per_sub = round(matched['value'] / size, 4)
        stake = {'usd': round(lost * per_sub), 'formula': 'sum over broad sends of (sends - engaged_segment) x (unsubscribes + bounces) / sends x matched_flow_revenue_per_engaged_subscriber',
                 'inputs': {'broad_sends': len(broad), 'engaged_segment': size, 'contacts_lost_outside_segment': round(lost),
                            'matched_flow_revenue_28d': matched['value'], 'matched_flow_revenue_per_engaged_subscriber': per_sub},
                 'window': f'{WINDOW}d'}
    ev = [_ev('contacts_outside_engaged_segment', outside, 'count', ends_on, 0, 'threshold', source='campaign_sends'),
          _ev('broad_campaigns', len(broad), 'count', ends_on, 0, 'threshold', source='campaign_sends'),
          _ev('contacts_lost_outside_segment', round(lost), 'count', ends_on, source='campaign_sends'),
          _ev('windows_with_broad_sends', agree, 'count', ends_on, window=f'{WINDOW * TRAILING}d', source='campaign_sends')]
    sentence = (f'{outside:,} subscribers outside the engaged segment got {len(broad)} campaigns in 28 days. '
                f'No sunset flow is live, and {round(lost):,} of them left or bounced.')
    return [_finding('EMAIL-R12', {'type': 'brand', 'id': 'broad_audience', 'label': 'Campaigns to all subscribers'}, ends_on,
                     _severity(stake and stake['usd'], net_28d, agree), ev, sentence, stake, _confidence(agree, 0.2))]


def _brain_dates(b):
    """(record id, date) for every calendar and offers record with a date on it."""
    out, ids = [], []
    for sec in ('calendar', 'offers'):
        for rec in b.records(sec) if b else []:
            ids.append(rec['id'])
            v = rec.get('value') if isinstance(rec.get('value'), dict) else {}
            for key in ('date', 'ends_on', 'end_date', 'deadline'):  # expires_at is shelf life, not an offer end
                d = v.get(key)
                if d and re.fullmatch(r'\d{4}-\d{2}-\d{2}', str(d)[:10]):
                    out.append((rec['id'], str(d)[:10]))
    return out, ids


def r14(rd, b, ends_on):
    dated, ids = _brain_dates(b)
    out = []
    for c in campaigns(rd) or []:
        text = f'{c["name"]} {c.get("subject") or ""}'
        hit = SCARCITY.search(text)
        if not hit:
            continue
        horizon = (date.fromisoformat(c['sent_on']) + timedelta(days=CLAIM_AHEAD_DAYS)).isoformat()
        backing = [rid for rid, d in dated if c['sent_on'] <= d <= horizon]
        if backing:
            continue
        ev = [_ev('backing_records', 0, 'count', ends_on, 1, 'threshold', source='brain.calendar, brain.offers'),
              _ev('sends', c['sends'], 'count', ends_on, source='campaign_sends')]
        claim = hit.group(0).lower()
        sentence = (f'"{c["subject"] or c["name"]}" went to {c["sends"]:,} people on {date.fromisoformat(c["sent_on"]).strftime("%-d %b")} '
                    f'and claims "{claim}". No calendar or offer record has a date in the next {CLAIM_AHEAD_DAYS} days.')
        out.append(_finding('EMAIL-R14', {'type': 'campaign', 'id': c['campaign_id'], 'label': c['name']}, ends_on, 'medium',
                            ev, sentence, None, _confidence(1), brain_refs=ids, money_reason='trust risk, no order count'))
    return out


def restock_days(rd):
    """SKU -> {date: on_hand summed over locations}. None when inventory is absent."""
    rows = rd.rows('inventory')
    if rows is None:
        return None
    out = {}
    for r in rows:
        if r.get('on_hand') is None:
            continue
        d = out.setdefault(r['sku'], {})
        d[str(r['date'])] = d.get(str(r['date']), 0) + r['on_hand']
    return out


def r15(rd, ends_on):
    sends = [c for c in campaigns(rd) or [] if RESTOCK.search(f'{c["name"]} {c.get("subject") or ""}')]
    if not sends:
        return []
    inv = restock_days(rd)
    if inv is None:
        return [_unavailable('EMAIL-R15', ends_on, 'Restock sends cannot be checked: there is no inventory feed.',
                             ['inventory'], 'shopify_inventory', 'Connect Shopify inventory levels (read only).')]
    out = []
    for c in sends:
        day = date.fromisoformat(c['sent_on'])
        d0, d1 = (day - timedelta(days=1)).isoformat(), c['sent_on']
        known = [s for s, v in inv.items() if d0 in v and d1 in v]
        if not known:
            continue
        rose = [s for s in known if inv[s][d1] > inv[s][d0]]
        if rose:
            continue
        ev = [_ev('skus_restocked_24h', 0, 'count', ends_on, 1, 'threshold', window='1d', source='inventory'),
              _ev('skus_checked', len(known), 'count', ends_on, window='1d', source='inventory'),
              _ev('sends', c['sends'], 'count', ends_on, source='campaign_sends')]
        sentence = (f'"{c["subject"] or c["name"]}" went to {c["sends"]:,} people on {day.strftime("%-d %b")}. '
                    f'None of the {len(known)} SKUs gained stock in the 24 hours before it.')
        out.append(_finding('EMAIL-R15', {'type': 'campaign', 'id': c['campaign_id'], 'label': c['name']}, ends_on, 'medium',
                            ev, sentence, None, _confidence(1), money_reason='no measurable loss yet'))
    return out


def run(brand, window=None, reader=None):
    """Findings for one brand and window ({ends_on, days, trailing}), sorted by severity then stake."""
    ends_on = date.fromisoformat(window['ends_on']) if window and window.get('ends_on') else last_full_day(brand)
    rd = reader or Reader(brand, ends_on)
    out = [_unavailable(r, ends_on) for r, *_rest, text in _SPEC if text]
    stats = flow_stats(rd)
    if stats is None:
        out += [_unavailable(r, ends_on, 'Email flows and campaigns are not connected, so this rule cannot run.',
                             SPEC[r][3], 'klaviyo', 'Connect Klaviyo (read only).')
                for r in ('EMAIL-R01', 'EMAIL-R10', 'EMAIL-R12', 'EMAIL-R14', 'EMAIL-R15')]
    else:
        matched = rd.m('revenue_by_flow_order_matched')
        net = matched.get('inputs', {}).get('net_revenue_all_orders') if not matched.get('unavailable') else None
        if matched.get('unavailable'):
            out.append(_unavailable('EMAIL-R01', ends_on, 'Real-order flow revenue is unavailable: ' + str(matched.get('reason')),
                                    ['orders', 'flows.matched_order_ids'], matched.get('fix') or 'shopify', 'Connect Shopify orders (read only).'))
        else:
            out += r01(mismatch_rows(stats, matched), ends_on)
        out += r10(stats, matched, ends_on, net)
        out += r12(rd, stats, matched, ends_on, net)
        out += r14(rd, brain(brand), ends_on)
        out += r15(rd, ends_on)
    out.sort(key=lambda f: (SEVERITY_ORDER[f['severity']], -((f['money_at_stake'] or {}).get('usd') or 0), f['id']))
    return out
