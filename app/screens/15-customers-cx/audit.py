"""Customers and CX audit (screen 15, round 0). Findings in the shape of app/contracts/audit.md.

Order totals come from app/metrics.py (aov). The CX numbers (tickets, CSAT, first reply, repeat by cohort) have no
metric in the contract yet, so they are counted here from data.sqlite with GROUP BY queries, orders and tickets from
the same file so rates hold at any data scale. They are listed in FEATURES.md as a contract proposal. Brand facts
come from the brain (app/brain/store.py: objection_ladders, policies). No connector, no model call. Same tables,
brain and window give the same findings.

Rules. CX-R01 to CX-R15 are the room spec's insights, in its order ("Customers and CX" in agents/rooms/rooms.json).
A rule whose inputs are not connected emits one `unavailable` finding at the severity the spec gives it.
  CX-R01  Silent churn risk. A customer past their own reorder window with no support contact and no email or SMS
          engagement. Needs churn_risk_scores and per-customer engagement. LIFE-C33, high.
  CX-R02  Refund missing tax reversal. A completed refund with no sales tax adjustment after 15 days. Needs
          tax_adjustments. LIFE-C55, high.
  CX-R03  Unprofitable VIP. A VIP by revenue with negative true profit over 12 months. Needs a loyalty tier and a
          support and shipping cost per order. LIFE-C62, medium.
  CX-R04  Unanswered negative review. A review at 2 stars or below with no reply after 5 days. Needs
          reviews.responded_at. LIFE-C28, medium.
  CX-R05  Failed-delivery loop. 2 or more failed delivery attempts on one order with no rebooking. Needs
          carrier_delivery_events. PROD-C56, medium.
  CX-R06  Crisis signal. One complaint theme over 3 times its trailing 14-day daily average across public
          channels. Needs public mention monitoring. BRAND-C54, high.
  CX-R07  Privacy request deadline at risk. An open data request within 3 days of its legal deadline. Needs
          privacy_requests. LIFE-C66, high.
  CX-R08  Identity fragmentation. One email or phone on 2 or more unmerged profiles with orders. Needs
          identity_graph (customers carry no email or phone). LIFE-C48, medium.
  CX-R09  Ticket reason drift. One reason's share of tickets up more than DRIFT_PP points, last 28 days against
          the 28 before. Reads tickets. LIFE-C27, medium. Money: null until finance_inputs carries a cost per
          ticket.
  CX-R10  Return to origin in one zone. Markets IN only: a US brand reads null and the rule emits nothing.
  CX-R11  Return to sender in one zone or carrier. Needs a zone or carrier on each order or carrier_delivery_events.
          LIFE-C26, medium.
  CX-R12  Marketplace rating gap. Needs marketplace ratings per SKU (marketplace_listings is empty and reviews
          carry the site only). LIFE-C28, medium.
  CX-R13  AI agent overreach. Needs ai_agent_action_log. LIFE-C49, high.
  CX-R14  Marketplace seller queue backlog. Needs marketplace_tickets. LIFE-C67, medium.
  CX-R15  WISMO surge in one lane. Needs a zone or carrier per ticket. LIFE-C24, medium.
Rules from the room's metric benchmarks, read on the brand as a whole:
  CX-R16  Where-is-my-order tickets over WISMO_TARGET of paid orders, 28 days (wismo_ticket_rate benchmark).
          Money: excess tickets x cost per ticket, null until finance_inputs has one. LIFE-C24.
  CX-R17  Support CSAT under CSAT_TARGET: share of rated tickets scored 4 or 5, 28 days (support_csat benchmark).
          Unavailable when under CSAT_MIN_RESPONSE of tickets are rated. Money: null, no link from a rating to a
          lost order yet. LIFE-C29.
  CX-R18  First reply over target, per channel: chat FIRST_REPLY_TARGET['chat'] minutes, email 24 hours
          (first_response_time benchmark). Channels without a target are not judged. Money: null. LIFE-C27.
  CX-R19  Repeat within 90 days of the newest mature cohort under the median of the 4 cohorts before it
          (repeat_purchase_rate, own history). Money: (median - rate) x first-time customers x aov x scale. LIFE-C33.
Owner of every rule: 15-customers-cx.

Windows: 28 days ending on the brand's last full day, plus 4 trailing 28-day windows for the own median and for
counting how many windows agree. Scale: data.sqlite may hold a sample of the history (dev builds run at 0.1);
dollar stakes are scaled by paid orders in the daily aggregate over paid orders in data.sqlite, same window.
"""
import importlib.util
import statistics
import sys
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parents[1]
SCREEN = '15-customers-cx'
WINDOW = 28
TRAILING = 4
DRIFT_PP = 0.10            # room spec: a reason's share up more than 10 points
WISMO_REASON = 'where is my order'
WISMO_TARGET = 0.05        # room spec: under 5 percent of orders
CSAT_TARGET = 0.90         # room spec: above 90 percent satisfied
CSAT_MIN_RESPONSE = 0.05   # room spec: unavailable under a 5 percent response rate
FIRST_REPLY_TARGET = {'chat': 60, 'email': 24 * 60}  # minutes; room spec: chat under 1 hour, email under 24 hours
REPEAT_DAYS = 90
PAID = ('paid', 'partially_refunded', 'refunded')
TICKET_CONNECTOR = 'helpdesk export (Gorgias or equivalent)'
SEVERITY_ORDER = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}

AUTONOMY = {'LIFE-C24': 'founder_gate', 'LIFE-C26': 'founder_gate', 'LIFE-C27': 'human_assist',
            'LIFE-C28': 'human_assist', 'LIFE-C29': 'founder_gate', 'LIFE-C33': 'agent_does',
            'LIFE-C48': 'founder_gate', 'LIFE-C49': 'founder_gate', 'LIFE-C55': 'human_assist',
            'LIFE-C62': 'founder_gate', 'LIFE-C66': 'founder_gate', 'LIFE-C67': 'founder_gate',
            'PROD-C56': 'founder_gate', 'BRAND-C54': 'founder_gate', 'MONEY-C09': 'agent_does'}


def _r(rule_id, name, entity_type, inputs, capability, **extra):
    return dict({'rule_id': rule_id, 'name': name, 'entity_type': entity_type, 'inputs': inputs,
                 'capability': capability, 'owner_screen': SCREEN}, **extra)


RULES = [
    _r('CX-R01', 'Silent churn risk', 'brand', ['churn_risk_scores', 'engagement_events'], 'LIFE-C33'),
    _r('CX-R02', 'Refund missing tax reversal', 'metric', ['tax_adjustments'], 'LIFE-C55'),
    _r('CX-R03', 'Unprofitable VIP', 'metric', ['loyalty_tiers', 'support_cost_per_ticket', 'shipping_labels'], 'LIFE-C62'),
    _r('CX-R04', 'Unanswered negative review', 'metric', ['reviews.responded_at'], 'LIFE-C28'),
    _r('CX-R05', 'Failed-delivery loop', 'metric', ['carrier_delivery_events'], 'PROD-C56'),
    _r('CX-R06', 'Crisis signal', 'metric', ['public_mentions'], 'BRAND-C54'),
    _r('CX-R07', 'Privacy request deadline at risk', 'metric', ['privacy_requests'], 'LIFE-C66'),
    _r('CX-R08', 'Identity fragmentation', 'metric', ['identity_graph'], 'LIFE-C48'),
    _r('CX-R09', 'Ticket reason drift', 'metric', ['tickets'], 'LIFE-C27'),
    _r('CX-R10', 'Return to origin in one zone', 'metric', ['carrier_delivery_events.rto'], 'LIFE-C26', markets=['IN']),
    _r('CX-R11', 'Return to sender in one zone or carrier', 'metric', ['carrier_delivery_events'], 'LIFE-C26'),
    _r('CX-R12', 'Marketplace rating gap', 'sku', ['marketplace_listings', 'reviews'], 'LIFE-C28'),
    _r('CX-R13', 'AI agent overreach', 'metric', ['ai_agent_action_log'], 'LIFE-C49'),
    _r('CX-R14', 'Marketplace seller queue backlog', 'metric', ['marketplace_tickets'], 'LIFE-C67'),
    _r('CX-R15', 'WISMO surge in one lane', 'metric', ['tickets', 'carrier_delivery_events'], 'LIFE-C24'),
    _r('CX-R16', 'Where-is-my-order tickets over 5 percent of orders', 'metric', ['tickets', 'orders'], 'LIFE-C24'),
    _r('CX-R17', 'Support CSAT under 90 percent', 'metric', ['tickets'], 'LIFE-C29'),
    _r('CX-R18', 'First reply over target', 'metric', ['tickets'], 'LIFE-C27'),
    _r('CX-R19', 'Repeat within 90 days under own median', 'metric', ['orders'], 'LIFE-C33'),
]

# Spec rules whose inputs no connector fills yet: (rule, severity, entity id, label, sentence, connector, fix).
NOT_CONNECTED = [
    ('CX-R01', 'high', 'silent_churn', 'Customers past their reorder window',
     'Nobody can see which customers are past their usual reorder time with no contact either way.',
     'churn scoring job (LIFE-C33) plus Klaviyo profile engagement',
     'Score churn weekly from order recency and join email and SMS engagement per customer.'),
    ('CX-R02', 'high', 'refund_tax_reversal', 'Refunds with a tax adjustment',
     'Refunds cannot be matched to a sales tax adjustment, so tax may still be owed on money already given back.',
     'accounting or Avalara or TaxJar export', 'Export tax adjustments with the refund id they reverse.'),
    ('CX-R03', 'medium', 'vip_profit', 'VIP customers on true profit',
     'VIP customers are ranked by revenue only. Returns, support and shipping cost per customer are not counted.',
     'loyalty tiers plus support and shipping cost in finance_inputs',
     'Add a cost per ticket and a label cost per order to finance_inputs and connect loyalty tiers.'),
    ('CX-R04', 'medium', 'negative_review_reply', 'Replies to reviews at 2 stars or below',
     'The reviews export has no reply date, so unanswered bad reviews cannot be counted.',
     'reviews app export with reply dates', 'Pull reviews with responded_at from the reviews app.'),
    ('CX-R05', 'medium', 'failed_delivery_loop', 'Orders with repeated failed deliveries',
     'Failed delivery attempts are not tracked, so an order that keeps failing is found only when the customer writes in.',
     'carrier tracking events', 'Connect carrier tracking events with attempt number and outcome.'),
    ('CX-R06', 'high', 'crisis_signal', 'Complaint spikes in public channels',
     'Public mentions are not watched, so a complaint spike shows up only in tickets days later.',
     'social and review mention monitoring', 'Connect a mention monitor that tags each mention with a theme.'),
    ('CX-R07', 'high', 'privacy_deadline', 'Privacy requests near their legal deadline',
     'Privacy requests are not logged, so a missed legal deadline cannot be seen.',
     'privacy request log (manual until an intake form exists)',
     'Log each access or deletion request with the date received and its legal deadline.'),
    ('CX-R08', 'medium', 'identity_fragmentation', 'Customers split across profiles',
     'Customer records carry no email or phone, so one person on 2 profiles cannot be found. Repeat rate may read low.',
     'identity resolution job (LIFE-C48)', 'Match orders, tickets and email contacts on email and phone.'),
    ('CX-R11', 'medium', 'return_to_sender_lane', 'Return to sender by zone and carrier',
     'Orders carry no shipping zone or carrier, so a bad lane cannot be told apart from the rest.',
     'carrier tracking events or a shipping label export', 'Add carrier and destination zone to each shipment.'),
    ('CX-R12', 'medium', 'marketplace_rating_gap', 'Marketplace rating next to site rating',
     'Marketplace ratings are not connected. Only site reviews are read, so a worse Amazon rating stays hidden.',
     'Amazon Seller Central and Google reviews pulls', 'Pull rating and review count per SKU from each marketplace.'),
    ('CX-R13', 'high', 'ai_agent_actions', 'AI support agent actions against its limits',
     'No AI support agent action log exists, so refunds or changes above its limit cannot be caught.',
     'AI support agent action log', 'Log every agent action with its amount and the limit in force.'),
    ('CX-R14', 'medium', 'marketplace_queue', 'Marketplace buyer messages past their deadline',
     'Marketplace buyer messages are not connected, so late replies there are not seen.',
     'marketplace seller console export', 'Export marketplace messages with status and reply deadline.'),
    ('CX-R15', 'medium', 'wismo_lane', 'Where-is-my-order tickets by zone and carrier',
     'Tickets carry no zone or carrier, so a lane with many where-is-my-order tickets cannot be found.',
     'carrier tracking events joined to tickets by order', 'Connect carrier events so each ticket gets a lane.'),
]

_MODS = {}


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def metrics():
    if 'metrics' not in _MODS:
        _MODS['metrics'] = _load('ecomos_metrics_customers_cx', APP / 'metrics.py')
    return _MODS['metrics']


def brand_data(brand):
    if 'tables' not in _MODS:
        _MODS['tables'] = _load('ecomos_tables_customers_cx', APP / 'data' / 'tables.py')
    return _MODS['tables'].brand_data(brand)


def brain(brand):
    """The brand's brain records, or None when the brand has no brain folder."""
    if not brand or not (APP / 'brain' / brand).is_dir():
        return None
    if 'store' not in _MODS:
        path = str(APP / 'brain')
        if path not in sys.path:
            sys.path.insert(0, path)  # store.py imports validate.py by name
        _MODS['store'] = _load('ecomos_brain_store_customers_cx', APP / 'brain' / 'store.py')
    return _MODS['store'].Brain(brand)


def last_full_day(data, brand):
    source = brand_data(brand) if brand else data
    return date.fromisoformat(source.brand['as_of'])


class Reader:
    """One brand, one window end. m() is metrics.compute with the brand filled in; sql() reads data.sqlite and
    returns None when it is absent, so every CX number reads unavailable, never 0."""

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

    def sql(self, query):
        fn = getattr(self.source, '_sql', None)
        if fn is None:
            return None
        try:
            return fn(query)
        except KeyError:
            return None
        except Exception as exc:  # a table missing from data.sqlite
            if 'no such table' in str(exc):
                return None
            raise

    def record(self, rid):
        return self._brain.get(f'{self.brand}.{rid}') if self._brain and self.brand else None

    def ref(self, rid):
        """The brain id when the record exists, for brain_refs."""
        rec = self.record(rid)
        return [rec['id']] if rec else []

    def windows(self):
        """The current 28-day window and the 4 before it, newest first, as (start, end) days."""
        out = []
        for k in range(TRAILING + 1):
            end = self.ends_on - timedelta(days=WINDOW * k)
            out.append((end - timedelta(days=WINDOW - 1), end))
        return out


# ---------------------------------------------------------------- CX numbers (shared with api.py)

PAID_SQL = ', '.join(f"'{s}'" for s in PAID)


def ticket_windows(rd):
    """Per 28-day window, newest first: tickets by reason and channel, rated and satisfied counts, first reply
    minutes by channel, paid orders placed. None when data.sqlite or the tickets table is absent."""
    if 'windows' in rd._memo:
        return rd._memo['windows']
    wins = rd.windows()
    first, last = wins[-1][0].isoformat(), wins[0][1].isoformat()
    rows = rd.sql(f"SELECT substr(created_at, 1, 10) AS day, reason, channel, first_response_min AS fr, csat "
                  f"FROM tickets WHERE substr(created_at, 1, 10) BETWEEN '{first}' AND '{last}'")
    span = rd.sql("SELECT MIN(substr(created_at, 1, 10)) AS first, MAX(substr(created_at, 1, 10)) AS last FROM tickets")
    orders = rd.sql(f"SELECT substr(created_at, 1, 10) AS day, COUNT(*) AS n FROM orders WHERE status IN ({PAID_SQL}) "
                    f"AND substr(created_at, 1, 10) BETWEEN '{first}' AND '{last}' GROUP BY day")
    out = None
    if rows is not None and orders is not None and span and span[0]['first']:
        out = []
        by_day = {r['day']: r['n'] for r in orders}
        for s, e in wins:
            if span[0]['first'] > s.isoformat() or span[0]['last'] < e.isoformat():
                out.append(None)  # the tickets table does not cover this window
                continue
            s_, e_ = s.isoformat(), e.isoformat()
            w = [r for r in rows if s_ <= r['day'] <= e_]
            reasons, channels, reply = {}, {}, {}
            rated = good = 0
            for r in w:
                g = reasons.setdefault(r['reason'], {'tickets': 0, 'rated': 0, 'good': 0})
                g['tickets'] += 1
                channels[r['channel']] = channels.get(r['channel'], 0) + 1
                if r['fr'] is not None:
                    reply.setdefault(r['channel'], []).append(r['fr'])
                if r['csat'] is not None:
                    rated += 1
                    g['rated'] += 1
                    if r['csat'] >= 4:
                        good += 1
                        g['good'] += 1
            out.append({'start': s_, 'end': e_, 'tickets': len(w), 'paid_orders': sum(n for d, n in by_day.items() if s_ <= d <= e_),
                        'reasons': reasons, 'channels': channels, 'rated': rated, 'good': good,
                        'reply_median': {c: statistics.median(v) for c, v in sorted(reply.items())},
                        'reply_all': statistics.median([x for v in reply.values() for x in v]) if reply else None})
    rd._memo['windows'] = out
    return out


def wismo(w):
    if not w or not w['paid_orders']:
        return None
    return round(w['reasons'].get(WISMO_REASON, {}).get('tickets', 0) / w['paid_orders'], 6)


def csat(w):
    """Share of rated tickets scored 4 or 5. None when under CSAT_MIN_RESPONSE of tickets carry a rating."""
    if not w or not w['tickets'] or w['rated'] / w['tickets'] < CSAT_MIN_RESPONSE:
        return None
    return round(w['good'] / w['rated'], 6)


def shares(w):
    return {k: round(v['tickets'] / w['tickets'], 6) for k, v in w['reasons'].items()} if w and w['tickets'] else {}


def repeat_cohorts(rd):
    """First-time customers by month of first order and how many placed a 2nd order within REPEAT_DAYS. A cohort
    counts once everyone in it has had the full REPEAT_DAYS and it starts on or after the first order day."""
    if 'repeat' in rd._memo:
        return rd._memo['repeat']
    rows = rd.sql(
        f"SELECT substr(f.created_at, 1, 7) AS cohort, COUNT(*) AS customers, "
        f"SUM(CASE WHEN s.created_at IS NOT NULL AND julianday(substr(s.created_at, 1, 10)) - "
        f"julianday(substr(f.created_at, 1, 10)) <= {REPEAT_DAYS} THEN 1 ELSE 0 END) AS repeat "
        f"FROM orders f LEFT JOIN orders s ON s.customer_id = f.customer_id AND s.order_index = 2 "
        f"WHERE f.order_index = 1 AND f.status IN ({PAID_SQL}) GROUP BY cohort ORDER BY cohort")
    first = rd.sql('SELECT MIN(substr(created_at, 1, 10)) AS d FROM orders')
    out = None
    if rows is not None and first and first[0]['d']:
        out = []
        for r in rows:
            y, m = int(r['cohort'][:4]), int(r['cohort'][5:7])
            month_end = date(y + (m == 12), m % 12 + 1, 1) - timedelta(days=1)
            if r['cohort'] + '-01' < first[0]['d'] or month_end + timedelta(days=REPEAT_DAYS) > rd.ends_on:
                continue
            out.append({'cohort': r['cohort'], 'customers': r['customers'], 'repeat': r['repeat'],
                        'rate': round(r['repeat'] / r['customers'], 6) if r['customers'] else None})
    rd._memo['repeat'] = out
    return out


def scale(rd, w):
    """Paid orders in the daily aggregate over paid orders in data.sqlite, same window. 1.0 for a live store."""
    aov = rd.m('aov', WINDOW)
    if aov.get('unavailable') or not w or not w['paid_orders']:
        return None
    return round(aov['inputs']['orders'] / w['paid_orders'], 4)


def cost_per_ticket(rd):
    """A support cost per ticket from finance_inputs, when the brand has entered one. None today."""
    try:
        f = rd.source.table('finance_inputs')
    except Exception:
        return None
    vals = [r.get('value') for r in f or [] if r.get('field') == 'support_cost_per_ticket' and r.get('value') is not None]
    return vals[-1] if vals else None


# ---------------------------------------------------------------- finding helpers

def _ev(metric, value, unit, ends_on, baseline=None, baseline_kind=None, window='28d', source='tickets'):
    return {'metric': metric, 'value': value, 'unit': unit, 'window': window, 'ends_on': ends_on.isoformat(),
            'freshness_days': 1, 'baseline': baseline, 'baseline_kind': baseline_kind, 'source': source,
            'simulated': True}


def _confidence(agree):
    """Contract section 2: 0.9 when 4 trailing windows agree, 0.7 for 2 to 3, 0.5 for 1."""
    return 0.9 if agree >= 4 else 0.7 if agree >= 2 else 0.5


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


def _cap(rule_id):
    return next(r['capability'] for r in RULES if r['rule_id'] == rule_id)


def _unavailable(rd, rule_id, severity, entity_id, label, sentence, inputs, connector, fix, refs=()):
    return _finding(rule_id, {'type': 'metric', 'id': entity_id, 'label': label}, severity, [], sentence,
                    _cap(rule_id), None, 0.1, list(refs), rd.ends_on, status='unavailable',
                    unavailable={'inputs': inputs, 'connector': connector, 'fix': fix},
                    money_reason='inputs not connected')


def _no_tickets(rd, rule_id, severity, entity_id, label):
    return _unavailable(rd, rule_id, severity, entity_id, label,
                        f'{label} cannot be read: the ticket table or the order table is not connected.',
                        ['tickets', 'orders'], TICKET_CONNECTOR,
                        'Connect the helpdesk export with reason, channel, first reply and CSAT per ticket.')


def _pct(x, d=0):
    return f'{x * 100:.{d}f} percent'


def _label(reason):
    return reason[:1].upper() + reason[1:]


# ---------------------------------------------------------------- rules

def rule_not_connected(rd):
    out = []
    for rule_id, sev, eid, label, sentence, connector, fix in NOT_CONNECTED:
        inputs = next(r['inputs'] for r in RULES if r['rule_id'] == rule_id)
        refs = rd.ref('objection_ladders.order_and_delivery') if rule_id in ('CX-R05', 'CX-R15') else []
        out.append(_unavailable(rd, rule_id, sev, eid, label, sentence, inputs, connector, fix, refs))
    return out


def rule_drift(rd):
    ws = ticket_windows(rd)
    if not ws or ws[0] is None or ws[1] is None:
        return [_no_tickets(rd, 'CX-R09', 'medium', 'ticket_reason_drift', 'Ticket reason mix')]
    now, before = shares(ws[0]), shares(ws[1])
    out = []
    for reason in sorted(now):
        a, b = before.get(reason, 0.0), now[reason]
        if b - a <= DRIFT_PP:
            continue
        slug = reason.replace(' ', '_')
        ev = [_ev(f'ticket_share.{slug}', b, 'ratio', rd.ends_on, baseline=a, baseline_kind='threshold'),
              _ev(f'ticket_share_change.{slug}', round(b - a, 6), 'ratio', rd.ends_on, baseline=DRIFT_PP,
                  baseline_kind='threshold')]
        s = f'"{_label(reason)}" tickets went from {a * 100:.0f} percent to {b * 100:.0f} percent of contacts in 28 days.'
        out.append(_finding('CX-R09', {'type': 'metric', 'id': f'ticket_reason.{slug}', 'label': f'{_label(reason)} tickets'},
                            'medium', ev, s, 'LIFE-C27', None, 0.5, [], rd.ends_on,
                            money_reason='no support cost per ticket in finance_inputs'))
    return out


def rule_wismo(rd):
    ws = ticket_windows(rd)
    if not ws or ws[0] is None:
        return [_no_tickets(rd, 'CX-R16', 'medium', 'wismo_ticket_rate', 'Where-is-my-order rate')]
    rates = [wismo(w) for w in ws]
    now = rates[0]
    if now is None or now <= WISMO_TARGET:
        return []
    agree = sum(1 for r in rates if r is not None and r > WISMO_TARGET)
    prev = [r for r in rates[1:] if r is not None]
    ev = [_ev('wismo_ticket_rate', now, 'ratio', rd.ends_on, baseline=WISMO_TARGET, baseline_kind='threshold',
              source='tickets, orders')]
    if len(prev) == TRAILING:
        ev.append(_ev('wismo_ticket_rate', now, 'ratio', rd.ends_on, baseline=round(statistics.median(prev), 6),
                      baseline_kind='own_median', source='tickets, orders'))
    cpt = cost_per_ticket(rd)
    sc = scale(rd, ws[0])
    money, reason = None, 'no support cost per ticket in finance_inputs'
    if cpt is not None and sc is not None:
        excess = (now - WISMO_TARGET) * ws[0]['paid_orders']
        money = {'usd': round(max(0.0, excess * cpt * sc), 2), 'formula': '(rate - target) x paid_orders x cost_per_ticket x scale',
                 'inputs': {'rate': now, 'target': WISMO_TARGET, 'paid_orders': ws[0]['paid_orders'],
                            'cost_per_ticket': cpt, 'scale': sc}, 'window': '28d'}
    sev = _severity(money['usd'] if money else None, rd.m('aov').get('inputs', {}).get('net_revenue'), agree)
    s = f'"Where is my order" tickets are {_pct(now, 1)} of paid orders in 28 days. The usual line is 5 percent.'
    return [_finding('CX-R16', {'type': 'metric', 'id': 'wismo_ticket_rate', 'label': 'Where-is-my-order rate'}, sev, ev, s,
                     'LIFE-C24', money, _confidence(agree), rd.ref('objection_ladders.order_and_delivery'), rd.ends_on,
                     money_reason=reason)]


def rule_csat(rd):
    ws = ticket_windows(rd)
    if not ws or ws[0] is None:
        return [_no_tickets(rd, 'CX-R17', 'high', 'support_csat', 'Support CSAT')]
    vals = [csat(w) for w in ws]
    now = vals[0]
    if now is None:
        return [_unavailable(rd, 'CX-R17', 'high', 'support_csat', 'Support CSAT',
                             'Too few tickets carry a CSAT rating to read satisfaction.', ['tickets.csat'],
                             TICKET_CONNECTOR, 'Send the CSAT survey after every solved ticket.')]
    if now >= CSAT_TARGET:
        return []
    agree = sum(1 for v in vals if v is not None and v < CSAT_TARGET)
    w = ws[0]
    worst = sorted(((g['good'] / g['rated'], r) for r, g in w['reasons'].items() if g['rated'] >= 20))
    ev = [_ev('support_csat', now, 'ratio', rd.ends_on, baseline=CSAT_TARGET, baseline_kind='threshold'),
          _ev('csat_response_rate', round(w['rated'] / w['tickets'], 6), 'ratio', rd.ends_on,
              baseline=CSAT_MIN_RESPONSE, baseline_kind='threshold')]
    s = f'{_pct(now)} of rated tickets scored 4 or 5 in 28 days, under the 90 percent line.'
    if worst:
        v, r = worst[0]
        ev.append(_ev(f'support_csat.{r.replace(" ", "_")}', round(v, 6), 'ratio', rd.ends_on, baseline=CSAT_TARGET,
                      baseline_kind='threshold'))
        s += f' "{_label(r)}" is lowest at {_pct(v)}.'
    sev = _severity(None, None, agree)
    return [_finding('CX-R17', {'type': 'metric', 'id': 'support_csat', 'label': 'Support CSAT'}, sev, ev, s, 'LIFE-C29',
                     None, _confidence(agree), rd.ref('objection_ladders.order_and_delivery') + rd.ref('policies.happiness_guarantee'),
                     rd.ends_on, money_reason='no link from a support rating to a lost order yet')]


def rule_first_reply(rd):
    ws = ticket_windows(rd)
    if not ws or ws[0] is None:
        return [_no_tickets(rd, 'CX-R18', 'high', 'first_response_time', 'First reply time')]
    out = []
    for ch, target in FIRST_REPLY_TARGET.items():
        now = ws[0]['reply_median'].get(ch)
        if now is None or now <= target:
            continue
        agree = sum(1 for w in ws if w and (w['reply_median'].get(ch) or 0) > target)
        ev = [_ev(f'first_response_time.{ch}', now, 'minutes', rd.ends_on, baseline=target, baseline_kind='threshold')]
        prev = [w['reply_median'][ch] for w in ws[1:] if w and ch in w['reply_median']]
        if len(prev) == TRAILING:
            ev.append(_ev(f'first_response_time.{ch}', now, 'minutes', rd.ends_on, baseline=statistics.median(prev),
                          baseline_kind='own_median'))
        n = ws[0]['channels'].get(ch, 0)
        ev.append(_ev(f'tickets.{ch}', n, 'count', rd.ends_on))
        t = f'{target // 60} hours' if target >= 120 else f'{target} minutes'
        s = f'The first reply on {ch} takes {now:.0f} minutes at the median over 28 days. The line is {t}.'
        out.append(_finding('CX-R18', {'type': 'metric', 'id': f'first_response_time.{ch}', 'label': f'First reply on {ch}'},
                            _severity(None, None, agree), ev, s, 'LIFE-C27', None, _confidence(agree), [], rd.ends_on,
                            money_reason='no link from reply time to a lost order yet'))
    return out


def rule_repeat(rd):
    cs = repeat_cohorts(rd)
    if cs is None:
        return [_unavailable(rd, 'CX-R19', 'high', 'repeat_purchase_rate', 'Repeat within 90 days',
                             'Repeat purchase cannot be read: the order table is not connected.', ['orders'],
                             'shopify', 'Connect the store order export with customer id and order number.')]
    if len(cs) < TRAILING + 1:
        return []
    now, prev = cs[-1], [c['rate'] for c in cs[-TRAILING - 1:-1] if c['rate'] is not None]
    if now['rate'] is None or len(prev) < TRAILING:
        return []
    med = statistics.median(prev)
    if now['rate'] >= med:
        return []
    agree = 1 + sum(1 for c in cs[-3:-1] if c['rate'] is not None and c['rate'] < med)
    ws = ticket_windows(rd)
    sc = scale(rd, ws[0] if ws else None)
    aov = rd.m('aov')
    money, reason = None, 'order totals unavailable'
    if sc is not None and not aov.get('unavailable'):
        money = {'usd': round(max(0.0, (med - now['rate']) * now['customers'] * aov['value'] * sc), 2),
                 'formula': '(median_rate - rate) x first_time_customers x aov x scale',
                 'inputs': {'median_rate': round(med, 6), 'rate': now['rate'], 'first_time_customers': now['customers'],
                            'aov': aov['value'], 'scale': sc}, 'window': f'cohort {now["cohort"]}'}
    ev = [_ev('repeat_purchase_rate_90d', now['rate'], 'ratio', rd.ends_on, baseline=round(med, 6),
              baseline_kind='own_median', window=f'cohort {now["cohort"]}', source='orders')]
    sev = _severity(money['usd'] if money else None, aov.get('inputs', {}).get('net_revenue'), agree)
    s = (f'{_pct(now["rate"], 1)} of first-time buyers from {now["cohort"]} ordered again within 90 days. '
         f'The 4 cohorts before ran {_pct(med, 1)}.')
    return [_finding('CX-R19', {'type': 'metric', 'id': 'repeat_purchase_rate', 'label': 'Repeat within 90 days'}, sev, ev, s,
                     'LIFE-C33', money, _confidence(agree), [], rd.ends_on, money_reason=reason)]


def run(brand, window=None, data=None):
    """Findings for one brand, sorted by severity then money at stake. `window` is {ends_on} or None."""
    ends_on = date.fromisoformat(window['ends_on']) if window and window.get('ends_on') else last_full_day(data, brand)
    return findings(Reader(data, brand, ends_on))


def findings(rd):
    """run() on a Reader the caller already holds, so api.py reuses its queries."""
    out = (rule_drift(rd) + rule_wismo(rd) + rule_csat(rd) + rule_first_reply(rd) + rule_repeat(rd)
           + rule_not_connected(rd))
    out.sort(key=lambda f: (SEVERITY_ORDER[f['severity']], -((f.get('money_at_stake') or {}).get('usd') or -1),
                            f['status'] == 'unavailable', f['id']))
    return out
