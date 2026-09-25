"""The metric contract in code: one function per metric in contracts/metrics.md.

`compute(name, data, **kw)` returns one metric as a dict:

  value           the number (or a dict of shares for payment_method_mix), null when unavailable
  unit            $, %, x, n, ms, bytes, share, weeks
  higher_is_better
  window          {label, days, start, end} (dates inclusive, ending on the last full day)
  freshness       {last_full_day, latest_row, stale_days, computed_at, tables}
  formula         the contract formula
  inputs          the totals the value came from (numerator, denominator, ...)
  breakdown       optional rows behind the total (never used to make the total)
  note            optional caveat
  unavailable     true when the metric cannot be computed honestly; then
  reason          why, and
  fix             the connector or table that fixes it

Rules: missing input makes the metric unavailable, never 0. Ratios come from
totals in the window, never from averaging rows. Windows end on the last full
day: the day before today, or the last day the source table has, whichever is
earlier; `end=YYYY-MM-DD` overrides it. Market-only metrics (rto_rate,
cod_share) read null with `not_applicable` for a brand whose market has no cash
on delivery.

`pipeline(data, window='28d', windows=4)` returns every pipeline metric for the
current window and the trailing ones, plus money at stake.

Fields read from the tables in contracts/data-sources.md (the generator and the
connectors must produce these names):

  orders          id, created_at, customer_id, status, total, shipping, tax
                  (number, {jurisdiction: amount} or [{jurisdiction, amount}]),
                  refund, payment_method, line_items [{sku, qty}], delivered_at
                  or status "delivered", shipped_at or status "shipped".
                  Optional: shipping_cost, payment_fee.
  sessions        date, product_view, add_to_cart, checkout, purchase (flags per
                  session row, or counts when a row carries `sessions`)
  products        sku, cost
  ad_rows         date, spend, impressions, reach, clicks, purchases, purchase_value
  google_rows     date, spend, impressions, clicks, purchases|conversions,
                  purchase_value|conversion_value
  flows           flow, date|sent_at, order_ids (matched order ids)
  list_growth     date, new_subscribers, unsubscribes, bounces
  reversed_orders order_id, type (return, chargeback, dispute,
                  return_to_sender, rto), amount, opened_at, closed_at, outcome
  payouts         period_end|deposit_date, fees
  cash            date, balance
  speed_runs      page, variant, run, load_ms, lcp_ms, fcp_ms, bytes, requests
"""
from __future__ import annotations

import statistics
from bisect import bisect_left, bisect_right
from datetime import date, datetime, timedelta, timezone

CONNECTORS = {
    'orders': 'Shopify',
    'customers': 'Shopify',
    'sessions': 'GA4',
    'products': 'Shopify plus a cost sheet',
    'ad_rows': 'Meta Ads',
    'google_rows': 'Google Ads',
    'flows': 'Klaviyo',
    'campaign_sends': 'Klaviyo',
    'list_growth': 'Klaviyo',
    'tickets': 'Gorgias',
    'reversed_orders': 'Shopify and gateway disputes',
    'payouts': 'Shopify Payments and Amazon',
    'cash': 'bank or accounting',
    'speed_runs': 'the speed lab',
}

CANCELLED = {'cancelled', 'canceled', 'voided', 'test', 'draft'}
SHIPPED = {'shipped', 'delivered', 'fulfilled', 'in_transit', 'out_for_delivery'}
RETURN_TYPES = {'return', 'returned'}
CHARGEBACK_TYPES = {'chargeback', 'dispute', 'inquiry'}
RTS_TYPES = {'return_to_sender', 'rts', 'carrier_return', 'undeliverable'}
RTO_TYPES = {'rto', 'return_to_origin'}
WON = {'won', 'reversed', 'merchant_won', 'closed_won'}
COD_MARKETS = {'IN', 'PK', 'BD', 'ID', 'PH', 'VN', 'AE', 'SA', 'EG', 'NG', 'LK', 'NP'}
PAYMENT_BUCKETS = {
    'card': {'card', 'credit_card', 'debit_card', 'visa', 'mastercard', 'amex'},
    'wallet': {'shop_pay', 'shopify_pay', 'apple_pay', 'google_pay', 'paypal', 'amazon_pay', 'venmo', 'wallet'},
    'bnpl': {'affirm', 'klarna', 'afterpay', 'sezzle', 'zip', 'bnpl', 'shop_pay_installments'},
    'cod': {'cod', 'cash_on_delivery'},
}
CHARGEBACK_BENCHMARK = 0.009


class Unavailable(Exception):
    """Raised inside a metric function when it cannot answer honestly."""

    def __init__(self, reason, table=None, fix=None):
        super().__init__(reason)
        self.reason, self.table, self.fix = reason, table, fix


# ---------------------------------------------------------------- small helpers

def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def num(value, default=0.0):
    """A number from a cell: None, blank and text give the default."""
    if value is None or value == '' or isinstance(value, bool):
        return default
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, dict):
        return num(value.get('amount', value.get('value')), default)
    try:
        return float(str(value).replace(',', '').replace('$', ''))
    except ValueError:
        return default


def flag(value):
    if isinstance(value, str):
        return value.strip().lower() in ('1', 'true', 'yes', 'y', 't')
    return bool(value)


def day(value):
    """'YYYY-MM-DD' from an ISO date or datetime string, or None."""
    if value is None:
        return None
    if isinstance(value, (date, datetime)):
        return value.isoformat()[:10]
    text = str(value).strip()
    if len(text) < 10:
        return None
    text = text[:10]
    try:
        date.fromisoformat(text)
    except ValueError:
        return None
    return text


def to_date(text):
    return date.fromisoformat(text)


def shift(text, days):
    return (to_date(text) + timedelta(days=days)).isoformat()


def month_of(text):
    return text[:7]


def ratio(n, d):
    return None if not d else n / d


def median(values):
    values = [v for v in values if v is not None]
    return statistics.median(values) if values else None


def first(row, *keys, default=None):
    for key in keys:
        if key in row and row[key] not in (None, ''):
            return row[key]
    return default


def parse_window(text, default='28d'):
    """'28d' or '12w' to a day count."""
    text = (text or default).strip().lower()
    try:
        if text.endswith('d'):
            days = int(text[:-1])
        elif text.endswith('w'):
            days = int(text[:-1]) * 7
        else:
            days = int(text)
    except ValueError:
        raise Unavailable(f'window {text!r} is not a day count like 28d or 12w')
    if days < 1 or days > 400:
        raise Unavailable(f'window must be between 1 and 400 days, not {days}')
    return days


# ---------------------------------------------------------------- dated indexes

_INDEX = {}


class Dated:
    """A table sorted by one date field, so a window is a bisect, not a scan."""

    def __init__(self, rows, field):
        pairs = []
        for row in rows:
            if not isinstance(row, dict):
                continue
            d = day(row.get(field))
            if d:
                pairs.append((d, row))
        pairs.sort(key=lambda p: p[0])
        self.dates = [p[0] for p in pairs]
        self.rows = [p[1] for p in pairs]
        self.undated = len(rows) - len(pairs)

    @property
    def latest(self):
        return self.dates[-1] if self.dates else None

    @property
    def earliest(self):
        return self.dates[0] if self.dates else None

    def between(self, start, end):
        lo = bisect_left(self.dates, start)
        hi = bisect_right(self.dates, end)
        return self.rows[lo:hi]


def dated(data, table, field):
    rows = data.table(table)
    key = (table, field, id(rows), len(rows))
    hit = _INDEX.get(key)
    if hit is None:
        if len(_INDEX) > 64:
            _INDEX.clear()
        hit = _INDEX[key] = Dated(rows, field)
    return hit


# ---------------------------------------------------------------- context

class Ctx:
    """What one metric call sees: the data layer, the window, the query args."""

    def __init__(self, data, spec, kw, offset=0):
        self.data = data
        self.spec = spec
        self.kw = kw
        self.offset = offset  # 0 is the current window, 1 the one before, and so on
        self.tables = []
        self.gaps = []  # coverage notes: a table that covers only part of the window
        self.days = parse_window(kw.get('window'), spec.get('window', '28d'))
        self.end = None
        self.start = None
        self.latest = None

    @property
    def brand(self):
        return self.data.brand

    def index(self, table, field):
        try:
            idx = dated(self.data, table, field)
        except KeyError:
            raise Unavailable(f'table {table} is missing', table)
        if table not in self.tables:
            self.tables.append(table)
        return idx

    def raw(self, table):
        try:
            rows = self.data.table(table)
        except KeyError:
            raise Unavailable(f'table {table} is missing', table)
        if table not in self.tables:
            self.tables.append(table)
        return rows

    def set_window(self, table, field, days=None, offset=None):
        """End on the last full day of `table`, then `days` back. offset=1 is the window before."""
        offset = self.offset if offset is None else offset
        idx = self.index(table, field)
        if not idx.dates:
            raise Unavailable(f'table {table} has no rows with a {field} date', table)
        yesterday = (datetime.now(timezone.utc).date() - timedelta(days=1)).isoformat()
        self.latest = idx.latest
        end = day(self.kw.get('end')) or min(idx.latest, yesterday)
        days = days or self.days
        self.end = shift(end, -days * offset)
        self.start = shift(self.end, -(days - 1))
        return idx

    def rows(self, table, field, start=None, end=None, continuous=True):
        """Rows of `table` dated in the window.

        A table with rows but none carrying `field` is unavailable, not empty.
        A continuous table (sessions, orders, ad rows, daily lists) that does
        not reach the window is unavailable too; one that covers only part of
        it is a reading with a coverage note. Event tables (reversed orders,
        flows) pass continuous=False: an empty window there is a real 0.
        """
        idx = self.index(table, field)
        start, end = start or self.start, end or self.end
        if not idx.dates:
            if idx.undated:
                raise Unavailable(f'{table} rows carry no {field} date', table)
            raise Unavailable(f'{table} has no rows', table)
        if continuous:
            if start > idx.latest or end < idx.earliest:
                raise Unavailable(f'no {table} rows dated between {start} and {end} (table covers {idx.earliest} to {idx.latest})', table)
            if start < idx.earliest or end > idx.latest:
                note = f'{table} covers {idx.earliest} to {idx.latest}, not the whole window'
                if note not in self.gaps:
                    self.gaps.append(note)
        return idx.between(start, end)

    def window_dict(self, label='current'):
        return {'label': label, 'days': self.days, 'start': self.start, 'end': self.end}

    def freshness(self):
        yesterday = (datetime.now(timezone.utc).date() - timedelta(days=1))
        stale = None
        if self.latest:
            stale = max(0, (yesterday - to_date(self.latest)).days)
        return {'last_full_day': self.end, 'latest_row': self.latest, 'stale_days': stale,
                'computed_at': now_iso(), 'tables': list(self.tables)}


# ---------------------------------------------------------------- orders

def order_ok(o):
    return str(o.get('status') or '').lower() not in CANCELLED


def order_paid(o):
    status = str(first(o, 'financial_status', default='') or '').lower()
    if status:
        return status in ('paid', 'partially_refunded', 'refunded', 'partially_paid')
    return order_ok(o) and num(o.get('total')) > 0


def order_shipped(o):
    return bool(first(o, 'shipped_at', 'fulfilled_at', 'delivered_at')) or str(o.get('status') or '').lower() in SHIPPED


def order_delivered(o):
    return bool(o.get('delivered_at')) or str(o.get('status') or '').lower() == 'delivered'


def tax_lines(o):
    """[(jurisdiction, amount)] from a number, a dict or a list of lines."""
    tax = first(o, 'tax', 'taxes', 'tax_lines', 'total_tax')
    if tax is None:
        return []
    if isinstance(tax, dict):
        return [(str(k), num(v)) for k, v in tax.items()]
    if isinstance(tax, list):
        out = []
        for line in tax:
            if isinstance(line, dict):
                out.append((str(first(line, 'jurisdiction', 'state', 'title', 'name', default='unknown')), num(first(line, 'amount', 'price'))))
        return out
    where = first(o, 'tax_jurisdiction', 'ship_state', 'shipping_state', 'state', default='unknown')
    return [(str(where), num(tax))]


def tax_total(o):
    return sum(a for _, a in tax_lines(o))


def net_revenue(o):
    """What the brand keeps of the product price: total minus shipping charged, tax and refunds."""
    if 'net_revenue' in o and o['net_revenue'] not in (None, ''):
        return num(o['net_revenue'])
    return num(o.get('total')) - num(o.get('shipping')) - tax_total(o) - num(o.get('refund'))


def check_orders(rows):
    if rows and not any('total' in o or 'net_revenue' in o for o in rows if isinstance(o, dict)):
        raise Unavailable('orders rows carry no total', 'orders')


def orders_in(ctx, start=None, end=None):
    rows = [o for o in ctx.rows('orders', 'created_at', start, end) if order_ok(o)]
    check_orders(rows)
    return rows


def line_items(o):
    items = first(o, 'line_items', 'items', 'lines', default=[])
    return [i for i in items if isinstance(i, dict)] if isinstance(items, list) else []


def customer_orders(ctx):
    """customer_id -> sorted list of order dates, across the whole table."""
    idx = ctx.index('orders', 'created_at')
    by = {}
    guests = 0
    for d, o in zip(idx.dates, idx.rows):
        if not order_ok(o):
            continue
        cid = first(o, 'customer_id', 'customer', 'email')
        if cid is None:
            guests += 1
            continue
        by.setdefault(str(cid), []).append((d, o))
    return by, guests


# ---------------------------------------------------------------- sessions

def funnel_totals(rows):
    """Totals of a session window: sessions, product_view, add_to_cart, checkout, purchase."""
    tot = {'sessions': 0, 'product_view': 0, 'add_to_cart': 0, 'checkout': 0, 'purchase': 0}
    for row in rows:
        if 'sessions' in row:
            weight = num(row.get('sessions'))
            tot['sessions'] += weight
            for key in ('product_view', 'add_to_cart', 'checkout', 'purchase'):
                tot[key] += num(row.get(key))
        else:
            tot['sessions'] += 1
            for key in ('product_view', 'add_to_cart', 'checkout', 'purchase'):
                tot[key] += 1 if flag(row.get(key)) else 0
    return tot


def funnel(ctx, start=None, end=None):
    tot = funnel_totals(ctx.rows('sessions', 'date', start, end))
    if not tot['sessions']:
        raise Unavailable('no sessions in the window', 'sessions')
    return tot


def window_orders(ctx, start=None, end=None):
    rows = orders_in(ctx, start, end)
    return {'orders': len(rows), 'net_revenue': sum(net_revenue(o) for o in rows)}


# ---------------------------------------------------------------- pipeline metrics

def m_sessions(ctx):
    ctx.set_window('sessions', 'date')
    tot = funnel(ctx)
    return {'value': tot['sessions'], 'inputs': tot}


def m_product_view_rate(ctx):
    ctx.set_window('sessions', 'date')
    tot = funnel(ctx)
    return {'value': ratio(tot['product_view'], tot['sessions']),
            'inputs': {'numerator': tot['product_view'], 'denominator': tot['sessions']}}


def m_add_to_cart_rate(ctx):
    ctx.set_window('sessions', 'date')
    tot = funnel(ctx)
    return {'value': ratio(tot['add_to_cart'], tot['sessions']),
            'inputs': {'numerator': tot['add_to_cart'], 'denominator': tot['sessions']}}


def m_checkout_rate(ctx):
    ctx.set_window('sessions', 'date')
    tot = funnel(ctx)
    if not tot['add_to_cart']:
        raise Unavailable('no sessions with add to cart in the window', 'sessions')
    return {'value': ratio(tot['checkout'], tot['add_to_cart']),
            'inputs': {'numerator': tot['checkout'], 'denominator': tot['add_to_cart']}}


def m_cvr_overall(ctx):
    ctx.set_window('sessions', 'date')
    tot = funnel(ctx)
    orders = window_orders(ctx)
    return {'value': ratio(orders['orders'], tot['sessions']),
            'inputs': {'numerator': orders['orders'], 'denominator': tot['sessions']}}


def m_aov(ctx):
    ctx.set_window('orders', 'created_at')
    orders = window_orders(ctx)
    if not orders['orders']:
        raise Unavailable('no orders in the window', 'orders')
    return {'value': orders['net_revenue'] / orders['orders'],
            'inputs': {'numerator': round(orders['net_revenue'], 2), 'denominator': orders['orders']}}


def cohort_months(ctx, maturity_days, count=6):
    """The last `count` full calendar months whose customers have had `maturity_days` to act."""
    matured = to_date(ctx.end) - timedelta(days=maturity_days)
    last = matured.replace(day=1) - timedelta(days=1)  # last day of the last full month before matured
    months = []
    cursor = last.replace(day=1)
    for _ in range(count):
        months.append(cursor.isoformat()[:7])
        cursor = (cursor - timedelta(days=1)).replace(day=1)
    months.reverse()
    return months, last.isoformat()


def m_repeat_rate_90d(ctx):
    ctx.set_window('orders', 'created_at')
    months, last_day = cohort_months(ctx, 90)
    by, guests = customer_orders(ctx)
    cohorts = {m: {'cohort': m, 'first_time': 0, 'repeated': 0} for m in months}
    for dates in by.values():
        first_day = dates[0][0]
        m = month_of(first_day)
        if m not in cohorts:
            continue
        cohorts[m]['first_time'] += 1
        if len(dates) > 1 and (to_date(dates[1][0]) - to_date(first_day)).days <= 90:
            cohorts[m]['repeated'] += 1
    first_time = sum(c['first_time'] for c in cohorts.values())
    repeated = sum(c['repeated'] for c in cohorts.values())
    if not first_time:
        raise Unavailable(f'no first-time customers with a customer_id in the cohorts {months[0]} to {months[-1]}', 'orders')
    rows = []
    for c in cohorts.values():
        rows.append(dict(c, rate=ratio(c['repeated'], c['first_time'])))
    out = {'value': repeated / first_time,
           'window': {'label': 'cohorts', 'days': 90, 'start': months[0] + '-01', 'end': last_day,
                      'note': f'first orders in the 6 months to {last_day}, each given 90 days'},
           'inputs': {'numerator': repeated, 'denominator': first_time}, 'breakdown': rows}
    if guests:
        out['note'] = f'{guests} orders without a customer_id are not counted'
    return out


STAGES = [
    # stage, the rate metric, what the gap multiplies (volume key), what one unit is worth
    ('sessions', 'sessions'),
    ('product_view_rate', 'sessions'),
    ('add_to_cart_rate', 'sessions'),
    ('checkout_rate', 'add_to_cart'),
    ('cvr_overall', 'sessions'),
    ('aov', 'orders'),
]


def stage_values(ctx, offset):
    """All pipeline stage values for one trailing window, or None where the data is missing."""
    ctx.set_window('sessions', 'date', offset=offset)
    try:
        tot = funnel(ctx)
    except Unavailable:
        tot = None
    try:
        orders = window_orders(ctx)
    except Unavailable:
        orders = None
    vals = {'sessions': tot['sessions'] if tot else None,
            'product_view_rate': ratio(tot['product_view'], tot['sessions']) if tot else None,
            'add_to_cart_rate': ratio(tot['add_to_cart'], tot['sessions']) if tot else None,
            'checkout_rate': ratio(tot['checkout'], tot['add_to_cart']) if tot else None,
            'cvr_overall': ratio(orders['orders'], tot['sessions']) if tot and orders else None,
            'aov': ratio(orders['net_revenue'], orders['orders']) if orders else None}
    volumes = {'sessions': tot['sessions'] if tot else None,
               'product_view': tot['product_view'] if tot else None,
               'add_to_cart': tot['add_to_cart'] if tot else None,
               'checkout': tot['checkout'] if tot else None,
               'orders': orders['orders'] if orders else None,
               'net_revenue': orders['net_revenue'] if orders else None}
    return vals, volumes, ctx.window_dict('current' if offset == 0 else f'prior {offset}')


def unit_value(volumes, stage):
    """Downstream net revenue per unit at the stage's numerator, in the current window."""
    rev = volumes.get('net_revenue')
    if rev is None:
        return None
    if stage == 'sessions':
        return ratio(rev, volumes.get('sessions'))
    if stage == 'product_view_rate':
        return ratio(rev, volumes.get('product_view'))
    if stage == 'add_to_cart_rate':
        return ratio(rev, volumes.get('add_to_cart'))
    if stage == 'checkout_rate':
        return ratio(rev, volumes.get('checkout'))
    if stage == 'cvr_overall':
        return ratio(rev, volumes.get('orders'))
    if stage == 'aov':
        return 1.0
    return None


def stakes(ctx, windows=4):
    """money_at_stake per stage from the current window against the trailing median."""
    windows = max(2, min(int(windows), 13))
    series = [stage_values(ctx, i) for i in range(windows)]
    current_vals, current_vol, current_win = series[0]
    ctx.set_window('sessions', 'date', offset=0)  # back to the current window for the caller
    priors = [s[0] for s in series[1:]]
    rows = []
    for stage, volume_key in STAGES:
        cur = current_vals.get(stage)
        prior = [p.get(stage) for p in priors if p.get(stage) is not None]
        med = median(prior)
        row = {'stage': stage, 'current': cur, 'prior': [p.get(stage) for p in priors], 'prior_median': med,
               'volume': current_vol.get(volume_key) if stage != 'sessions' else 1,
               'unit_value': unit_value(current_vol, stage), 'gap': None, 'stake': None}
        if cur is None or med is None or len(prior) < 2:
            row['unreadable'] = 'fewer than 2 prior windows' if (cur is not None and len(prior) < 2) else 'no data in the window'
        else:
            row['gap'] = med - cur
            row['change'] = ratio(cur - med, med)
            if row['gap'] > 0 and row['volume'] is not None and row['unit_value'] is not None:
                row['stake'] = row['gap'] * row['volume'] * row['unit_value']
            else:
                row['stake'] = 0.0
        rows.append(row)
    return rows, [s[2] for s in series]


def m_money_at_stake(ctx):
    rows, wins = stakes(ctx, ctx.kw.get('windows') or 4)
    readable = [r for r in rows if r.get('stake') is not None]
    if not readable:
        raise Unavailable('fewer than 2 prior windows have sessions and orders, so there is no trailing median yet', 'sessions')
    top = max(readable, key=lambda r: r['stake'])
    out = {'value': top['stake'], 'stage': top['stage'] if top['stake'] > 0 else None,
           'inputs': {'gap': top['gap'], 'volume': top['volume'], 'unit_value': top['unit_value'],
                      'prior_windows': len(wins) - 1, 'baseline': 'own trailing median'},
           'breakdown': rows, 'windows': wins}
    if top['stake'] <= 0:
        out['note'] = 'no stage is below its own trailing median'
    unreadable = [r['stage'] for r in rows if r.get('unreadable')]
    if unreadable:
        out['note'] = (out.get('note', '') + ' ' if out.get('note') else '') + 'unreadable: ' + ', '.join(unreadable)
    return out


# ---------------------------------------------------------------- reversed orders

def reversed_rows(ctx, types, field='opened_at', start=None, end=None):
    return [r for r in ctx.rows('reversed_orders', field, start, end, continuous=False) if str(r.get('type') or '').lower() in types]


def reversed_order_ids(ctx, types):
    ids = set()
    for r in ctx.raw('reversed_orders'):
        if isinstance(r, dict) and str(r.get('type') or '').lower() in types and r.get('order_id') is not None:
            ids.add(str(r['order_id']))
    return ids


def m_return_rate(ctx):
    ctx.set_window('orders', 'created_at')
    orders = orders_in(ctx)
    delivered = [o for o in orders if order_delivered(o)]
    if not delivered:
        raise Unavailable('no delivered orders in the window: orders need delivered_at or status "delivered"', 'orders')
    try:
        returned_ids = reversed_order_ids(ctx, RETURN_TYPES)
        returned = sum(1 for o in delivered if str(o.get('id')) in returned_ids)
    except Unavailable:
        if not any('return' in o for o in delivered):
            raise
        returned = sum(1 for o in delivered if flag(o.get('return')) or num(o.get('return')) > 0)
    return {'value': returned / len(delivered), 'inputs': {'numerator': returned, 'denominator': len(delivered)}}


def m_chargeback_rate(ctx):
    ctx.set_window('orders', 'created_at')
    paid = [o for o in orders_in(ctx) if order_paid(o)]
    if not paid:
        raise Unavailable('no paid orders in the window', 'orders')
    opened = reversed_rows(ctx, CHARGEBACK_TYPES)
    return {'value': len(opened) / len(paid), 'inputs': {'numerator': len(opened), 'denominator': len(paid)},
            'benchmark': {'max': CHARGEBACK_BENCHMARK, 'label': 'under 0.9 percent'}}


def m_dispute_win_rate(ctx):
    ctx.set_window('reversed_orders', 'opened_at')
    closed = reversed_rows(ctx, CHARGEBACK_TYPES, field='closed_at')
    if not closed:
        raise Unavailable('no disputes closed in the window', 'reversed_orders')
    won = [r for r in closed if str(r.get('outcome') or '').lower() in WON]
    return {'value': len(won) / len(closed), 'inputs': {'numerator': len(won), 'denominator': len(closed)}}


def m_return_to_sender_rate(ctx):
    ctx.set_window('orders', 'created_at')
    shipped = [o for o in orders_in(ctx) if order_shipped(o)]
    if not shipped:
        raise Unavailable('no shipped orders in the window: orders need shipped_at or a shipped status', 'orders')
    rts_ids = reversed_order_ids(ctx, RTS_TYPES)
    back = sum(1 for o in shipped if str(o.get('id')) in rts_ids)
    return {'value': back / len(shipped), 'inputs': {'numerator': back, 'denominator': len(shipped)}}


def cod_market(brand):
    market = str(brand.get('market') or 'US').upper()
    methods = {str(m).lower() for m in (brand.get('payment_methods') or [])}
    return market in COD_MARKETS or bool(methods & PAYMENT_BUCKETS['cod'])


def not_applicable(ctx, why):
    return {'value': None, 'unavailable': False, 'not_applicable': True, 'reason': why,
            'window': ctx.window_dict() if ctx.end else None}


def m_rto_rate(ctx):
    brand = ctx.brand
    if not cod_market(brand):
        return not_applicable(ctx, f'market {brand.get("market", "US")} has no cash on delivery, so return to origin reads null')
    ctx.set_window('orders', 'created_at')
    cod = [o for o in orders_in(ctx) if str(o.get('payment_method') or '').lower() in PAYMENT_BUCKETS['cod']]
    if not cod:
        raise Unavailable('no cash-on-delivery orders in the window', 'orders')
    rto_ids = reversed_order_ids(ctx, RTO_TYPES)
    back = sum(1 for o in cod if str(o.get('id')) in rto_ids)
    return {'value': back / len(cod), 'inputs': {'numerator': back, 'denominator': len(cod)}}


def m_payment_method_mix(ctx):
    ctx.set_window('orders', 'created_at')
    orders = orders_in(ctx)
    if not orders:
        raise Unavailable('no orders in the window', 'orders')
    raw, buckets = {}, {'card': 0, 'wallet': 0, 'bnpl': 0, 'cod': 0, 'other': 0}
    for o in orders:
        method = str(o.get('payment_method') or 'unknown').lower()
        raw[method] = raw.get(method, 0) + 1
        for bucket, names in PAYMENT_BUCKETS.items():
            if method in names:
                buckets[bucket] += 1
                break
        else:
            buckets['other'] += 1
    total = len(orders)
    shares = {k: v / total for k, v in buckets.items()}
    if not cod_market(ctx.brand):
        shares['cod'] = None
    return {'value': shares, 'inputs': {'orders': total, 'counts': buckets},
            'breakdown': sorted(({'method': k, 'orders': v, 'share': v / total} for k, v in raw.items()), key=lambda r: -r['orders'])}


# ---------------------------------------------------------------- paid

PAID_SOURCES = {'meta': 'ad_rows', 'google': 'google_rows'}


def paid_totals(rows):
    tot = {'spend': 0.0, 'impressions': 0.0, 'reach': 0.0, 'clicks': 0.0, 'purchases': 0.0, 'purchase_value': 0.0, 'rows': 0}
    for r in rows:
        tot['rows'] += 1
        tot['spend'] += num(first(r, 'spend', 'cost', 'amount_spent'))
        tot['impressions'] += num(r.get('impressions'))
        tot['reach'] += num(r.get('reach'))
        tot['clicks'] += num(first(r, 'clicks', 'link_clicks'))
        tot['purchases'] += num(first(r, 'purchases', 'conversions', 'orders'))
        tot['purchase_value'] += num(first(r, 'purchase_value', 'conversion_value', 'revenue'))
    return tot


def paid(ctx, source=None):
    """Totals per channel in the window. source: meta, google or all (default)."""
    source = (source or ctx.kw.get('source') or 'all').lower()
    wanted = list(PAID_SOURCES) if source == 'all' else [source]
    if any(s not in PAID_SOURCES for s in wanted):
        raise Unavailable(f'source must be one of meta, google, all, not {source!r}')
    tables = [PAID_SOURCES[s] for s in wanted]
    present = [t for t in tables if ctx.data.table_path(t)]
    if not present:
        raise Unavailable('no ad tables: ' + ', '.join(tables) + ' are missing', tables[0])
    if ctx.end is None:
        ctx.set_window(present[0], 'date')
    per, total = {}, paid_totals([])
    for name, table in zip(wanted, tables):
        if table not in present:
            per[name] = None
            continue
        tot = paid_totals(ctx.rows(table, 'date'))
        per[name] = tot
        for k in total:
            total[k] += tot[k]
    missing = [t for t in tables if t not in present]
    return total, per, missing


def paid_metric(key, unit):
    def fn(ctx):
        total, per, missing = paid(ctx)
        if not total['rows']:
            raise Unavailable('no ad rows in the window', 'ad_rows')
        out = {'value': total[key], 'inputs': {k: total[k] for k in total}, 'breakdown': per, 'unit': unit}
        if missing:
            out['partial'] = True
            out['note'] = 'missing ' + ', '.join(missing) + ', so this covers ' + ', '.join(k for k, v in per.items() if v)
        return out
    return fn


def m_period_roas(ctx):
    total, per, missing = paid(ctx)
    if not total['spend']:
        raise Unavailable('no spend in the window', 'ad_rows')
    out = {'value': total['purchase_value'] / total['spend'],
           'inputs': {'numerator': total['purchase_value'], 'denominator': total['spend']},
           'breakdown': {k: (ratio(v['purchase_value'], v['spend']) if v else None) for k, v in per.items()}}
    if missing:
        out['partial'] = True
        out['note'] = 'missing ' + ', '.join(missing)
    return out


def m_mer(ctx):
    ctx.set_window('orders', 'created_at')
    revenue = window_orders(ctx)
    total, per, missing = paid(ctx)
    if not total['spend']:
        raise Unavailable('no marketing spend in the window', 'ad_rows')
    out = {'value': revenue['net_revenue'] / total['spend'],
           'inputs': {'numerator': round(revenue['net_revenue'], 2), 'denominator': total['spend'], 'orders': revenue['orders']}}
    if missing:
        out['partial'] = True
        out['note'] = 'spend misses ' + ', '.join(missing) + ', so MER reads high'
    return out


def m_cpa(ctx):
    total, per, missing = paid(ctx)
    if not total['purchases']:
        raise Unavailable('no purchases attributed in the window', 'ad_rows')
    out = {'value': total['spend'] / total['purchases'],
           'inputs': {'numerator': total['spend'], 'denominator': total['purchases']}}
    if missing:
        out['partial'] = True
        out['note'] = 'missing ' + ', '.join(missing)
    return out


def m_frequency(ctx):
    total, per, missing = paid(ctx, 'meta')
    if not total['reach']:
        raise Unavailable('no reach in the window: reach comes from Meta ad rows', 'ad_rows')
    return {'value': total['impressions'] / total['reach'],
            'inputs': {'numerator': total['impressions'], 'denominator': total['reach']},
            'note': 'reach is summed from daily rows, so true window frequency is higher'}


# ---------------------------------------------------------------- retention

def m_revenue_by_flow_order_matched(ctx):
    ctx.set_window('orders', 'created_at')
    orders = {str(o.get('id')): o for o in orders_in(ctx)}
    flows = ctx.raw('flows')
    by, seen = {}, set()
    for f in flows:
        if not isinstance(f, dict):
            continue
        ids = first(f, 'order_ids', 'matched_order_ids', 'orders_matched', default=[])
        if not isinstance(ids, list):
            continue
        name = str(first(f, 'flow', 'name', default='unknown'))
        row = by.setdefault(name, {'flow': name, 'orders': 0, 'revenue': 0.0})
        for oid in ids:
            o = orders.get(str(oid))
            if o is None:
                continue
            row['orders'] += 1
            row['revenue'] += net_revenue(o)
            seen.add(str(oid))
    if not flows:
        raise Unavailable('flows table has no rows', 'flows')
    total = sum(net_revenue(orders[oid]) for oid in seen)
    return {'value': total, 'inputs': {'matched_orders': len(seen), 'orders_in_window': len(orders)},
            'breakdown': sorted(by.values(), key=lambda r: -r['revenue']),
            'note': 'an order matched to 2 flows counts once in the total and in each flow below'}


def m_list_growth(ctx):
    ctx.set_window('list_growth', 'date')
    rows = ctx.rows('list_growth', 'date')
    if not rows:
        raise Unavailable('no list rows in the window', 'list_growth')
    new = sum(num(first(r, 'new_subscribers', 'new', 'subscribed')) for r in rows)
    unsub = sum(num(first(r, 'unsubscribes', 'unsubscribed')) for r in rows)
    bounced = sum(num(first(r, 'bounces', 'bounced')) for r in rows)
    return {'value': new - unsub - bounced, 'inputs': {'new_subscribers': new, 'unsubscribes': unsub, 'bounces': bounced}}


def m_ltv_180d(ctx):
    ctx.set_window('orders', 'created_at')
    months, last_day = cohort_months(ctx, 180)
    by, guests = customer_orders(ctx)
    cohorts = {m: {'cohort': m, 'customers': 0, 'revenue': 0.0} for m in months}
    for dates in by.values():
        first_day = dates[0][0]
        m = month_of(first_day)
        if m not in cohorts:
            continue
        limit = shift(first_day, 180)
        cohorts[m]['customers'] += 1
        cohorts[m]['revenue'] += sum(net_revenue(o) for d, o in dates if d <= limit)
    customers = sum(c['customers'] for c in cohorts.values())
    revenue = sum(c['revenue'] for c in cohorts.values())
    if not customers:
        raise Unavailable(f'no first-time customers with a customer_id in the cohorts {months[0]} to {months[-1]}', 'orders')
    rows = [dict(c, ltv=ratio(c['revenue'], c['customers'])) for c in cohorts.values()]
    out = {'value': revenue / customers,
           'window': {'label': 'cohorts', 'days': 180, 'start': months[0] + '-01', 'end': last_day,
                      'note': f'first orders in the 6 months to {last_day}, each given 180 days'},
           'inputs': {'numerator': round(revenue, 2), 'denominator': customers}, 'breakdown': rows}
    if guests:
        out['note'] = f'{guests} orders without a customer_id are not counted'
    return out


# ---------------------------------------------------------------- money

def m_contribution_margin(ctx):
    ctx.set_window('orders', 'created_at')
    orders = orders_in(ctx)
    if not orders:
        raise Unavailable('no orders in the window', 'orders')
    brand = ctx.brand
    revenue = sum(net_revenue(o) for o in orders)

    # COGS from line items and product cost
    costs = {}
    for p in ctx.raw('products'):
        if isinstance(p, dict) and p.get('sku') is not None and p.get('cost') not in (None, ''):
            costs[str(p['sku'])] = num(p['cost'])
    if not costs:
        raise Unavailable('products carry no cost, so COGS is unknown', 'products',
                          'a cost sheet with cost per sku (products table)')
    cogs, missing_skus, no_lines = 0.0, set(), 0
    for o in orders:
        lines = line_items(o)
        if not lines:
            no_lines += 1
        for line in lines:
            sku = str(line.get('sku'))
            if sku in costs:
                cogs += costs[sku] * num(first(line, 'qty', 'quantity', default=1), 1)
            else:
                missing_skus.add(sku)

    # shipping cost paid by the brand
    if any('shipping_cost' in o for o in orders):
        shipping = sum(num(o.get('shipping_cost')) for o in orders)
        shipping_from = 'orders.shipping_cost'
    elif num((brand.get('fulfilment') or {}).get('cost_per_order_usd')):
        shipping = num(brand['fulfilment']['cost_per_order_usd']) * len(orders)
        shipping_from = 'brand.json fulfilment.cost_per_order_usd'
    else:
        raise Unavailable('no shipping cost: add shipping_cost to orders or fulfilment.cost_per_order_usd to brand.json',
                          'orders', '3PL invoices (orders.shipping_cost)')

    # payment fees
    if any('payment_fee' in o for o in orders):
        fees = sum(num(o.get('payment_fee')) for o in orders)
        fees_from = 'orders.payment_fee'
    elif ctx.data.table_path('payouts'):
        field = 'period_end' if any('period_end' in r for r in ctx.raw('payouts') if isinstance(r, dict)) else 'deposit_date'
        rows = ctx.rows('payouts', field)
        if not rows:
            raise Unavailable('no payouts in the window', 'payouts')
        fees = sum(num(r.get('fees')) for r in rows)
        fees_from = 'payouts.fees'
    else:
        raise Unavailable('no payment fees: add payment_fee to orders or a payouts table', 'payouts')

    # returns cost
    returns = sum(num(r.get('amount')) for r in reversed_rows(ctx, RETURN_TYPES))

    # marketing spend, all channels
    total, per, missing = paid(ctx)
    marketing = total['spend']

    value = revenue - cogs - shipping - fees - returns - marketing
    out = {'value': value,
           'inputs': {'net_revenue': round(revenue, 2), 'cogs': round(cogs, 2), 'shipping': round(shipping, 2),
                      'payment_fees': round(fees, 2), 'returns_cost': round(returns, 2), 'marketing': round(marketing, 2),
                      'orders': len(orders)},
           'sources': {'shipping': shipping_from, 'payment_fees': fees_from, 'marketing': ', '.join(k for k, v in per.items() if v)},
           'margin_rate': ratio(value, revenue)}
    notes = []
    if missing_skus:
        notes.append(f'{len(missing_skus)} skus have no cost')
    if no_lines:
        notes.append(f'{no_lines} orders have no line items')
    if missing:
        notes.append('spend misses ' + ', '.join(missing))
    if notes:
        out['note'] = '; '.join(notes)
    return out


def m_cash_runway_weeks(ctx):
    brand = ctx.brand
    finance = brand.get('finance') or {}
    if ctx.data.table_path('cash'):
        ctx.set_window('cash', 'date')
        rows = ctx.rows('cash', 'date')
        if len(rows) < 2:
            raise Unavailable('fewer than 2 cash balances in the window', 'cash')
        idx = ctx.index('cash', 'date')
        dates = [d for d in idx.dates if ctx.start <= d <= ctx.end]
        start_bal, end_bal = num(rows[0].get('balance')), num(rows[-1].get('balance'))
        weeks = max((to_date(dates[-1]) - to_date(dates[0])).days, 1) / 7
        burn = (start_bal - end_bal) / weeks
        inputs = {'cash_on_hand': end_bal, 'weekly_net_burn': round(burn, 2), 'weeks_measured': round(weeks, 1)}
        if burn <= 0:
            return {'value': None, 'unavailable': False, 'inputs': inputs, 'note': 'cash grew over the window, so there is no burn to divide by'}
        return {'value': end_bal / burn, 'inputs': inputs}
    cash = num(finance.get('cash_on_hand_usd'))
    burn = num(finance.get('weekly_net_burn_usd'))
    if not cash or not burn:
        raise Unavailable('no cash table and brand.json has no finance.cash_on_hand_usd and finance.weekly_net_burn_usd',
                          'cash', 'bank or accounting connector (cash table with date and balance)')
    if burn <= 0:
        return {'value': None, 'unavailable': False, 'inputs': {'cash_on_hand': cash, 'weekly_net_burn': burn},
                'note': 'no burn: the brand is cash positive', 'window': {'label': 'brand record', 'days': None, 'start': None, 'end': None}}
    return {'value': cash / burn, 'inputs': {'cash_on_hand': cash, 'weekly_net_burn': burn},
            'window': {'label': 'brand record', 'days': None, 'start': None, 'end': None}}


def m_sales_tax_collected(ctx):
    ctx.set_window('orders', 'created_at')
    orders = orders_in(ctx)
    if not orders:
        raise Unavailable('no orders in the window', 'orders')
    if not any(first(o, 'tax', 'taxes', 'tax_lines', 'total_tax') is not None for o in orders):
        raise Unavailable('orders carry no tax field', 'orders')
    by = {}
    for o in orders:
        for where, amount in tax_lines(o):
            by[where] = by.get(where, 0.0) + amount
    total = sum(by.values())
    return {'value': total, 'inputs': {'orders': len(orders), 'jurisdictions': len(by)},
            'breakdown': sorted(({'jurisdiction': k, 'amount': round(v, 2)} for k, v in by.items()), key=lambda r: -r['amount'])}


# ---------------------------------------------------------------- speed

def speed_metric(*fields):
    def fn(ctx):
        rows = [r for r in ctx.raw('speed_runs') if isinstance(r, dict)]
        page, variant = ctx.kw.get('page'), ctx.kw.get('variant')
        if page:
            rows = [r for r in rows if str(r.get('page')) == page]
        if variant:
            rows = [r for r in rows if str(r.get('variant')) == variant]
        elif rows and any(str(r.get('variant')) == 'baseline' for r in rows):
            rows = [r for r in rows if str(r.get('variant')) == 'baseline']
            variant = 'baseline'
        values = [num(first(r, *fields), None) for r in rows]
        values = [v for v in values if v is not None]
        if not values:
            raise Unavailable('no speed runs' + (f' for page {page}' if page else '') + (f' variant {variant}' if variant else ''), 'speed_runs')
        groups = {}
        for r in rows:
            v = num(first(r, *fields), None)
            if v is None:
                continue
            groups.setdefault((str(r.get('page')), str(r.get('variant'))), []).append(v)
        return {'value': statistics.median(values),
                'window': {'label': 'lab runs', 'days': None, 'start': None, 'end': None,
                           'note': 'median of runs' + (f', variant {variant}' if variant else '')},
                'inputs': {'runs': len(values), 'page': page, 'variant': variant},
                'breakdown': [{'page': p, 'variant': v, 'runs': len(vals), 'median': statistics.median(vals)} for (p, v), vals in sorted(groups.items())]}
    return fn


# ---------------------------------------------------------------- registry

def spec(fn, group, unit, higher_is_better, window='28d', sources=(), formula=None):
    return {'fn': fn, 'group': group, 'unit': unit, 'higher_is_better': higher_is_better,
            'window': window, 'sources': list(sources), 'formula': formula}


PIPELINE = 'Pipeline (00-today)'
REVERSED = 'Reversed orders (06, 15, 19, 21)'
PAID = 'Paid (11, 12, 13)'
RETENTION = 'Retention (14, 15)'
MONEY = 'Money (21)'
SPEED = 'Speed (08)'

METRICS = {
    'sessions': spec(m_sessions, PIPELINE, 'n', True, sources=['sessions']),
    'product_view_rate': spec(m_product_view_rate, PIPELINE, '%', True, sources=['sessions']),
    'add_to_cart_rate': spec(m_add_to_cart_rate, PIPELINE, '%', True, sources=['sessions']),
    'checkout_rate': spec(m_checkout_rate, PIPELINE, '%', True, sources=['sessions']),
    'cvr_overall': spec(m_cvr_overall, PIPELINE, '%', True, sources=['orders', 'sessions']),
    'aov': spec(m_aov, PIPELINE, '$', True, sources=['orders']),
    'repeat_rate_90d': spec(m_repeat_rate_90d, PIPELINE, '%', True, sources=['orders']),
    'money_at_stake': spec(m_money_at_stake, PIPELINE, '$', False, sources=['sessions', 'orders']),

    'return_rate': spec(m_return_rate, REVERSED, '%', False, '90d', sources=['orders', 'reversed_orders']),
    'chargeback_rate': spec(m_chargeback_rate, REVERSED, '%', False, '90d', sources=['orders', 'reversed_orders']),
    'dispute_win_rate': spec(m_dispute_win_rate, REVERSED, '%', True, '90d', sources=['reversed_orders']),
    'return_to_sender_rate': spec(m_return_to_sender_rate, REVERSED, '%', False, '90d', sources=['orders', 'reversed_orders']),
    'rto_rate': spec(m_rto_rate, REVERSED, '%', False, '90d', sources=['orders', 'reversed_orders']),
    'payment_method_mix': spec(m_payment_method_mix, REVERSED, 'share', None, '90d', sources=['orders']),

    'spend': spec(paid_metric('spend', '$'), PAID, '$', None, sources=['ad_rows', 'google_rows']),
    'impressions': spec(paid_metric('impressions', 'n'), PAID, 'n', None, sources=['ad_rows', 'google_rows']),
    'clicks': spec(paid_metric('clicks', 'n'), PAID, 'n', True, sources=['ad_rows', 'google_rows']),
    'purchases': spec(paid_metric('purchases', 'n'), PAID, 'n', True, sources=['ad_rows', 'google_rows']),
    'purchase_value': spec(paid_metric('purchase_value', '$'), PAID, '$', True, sources=['ad_rows', 'google_rows']),
    'period_roas': spec(m_period_roas, PAID, 'x', True, sources=['ad_rows', 'google_rows']),
    'mer': spec(m_mer, PAID, 'x', True, sources=['orders', 'ad_rows', 'google_rows']),
    'cpa': spec(m_cpa, PAID, '$', False, sources=['ad_rows', 'google_rows']),
    'frequency': spec(m_frequency, PAID, 'x', False, sources=['ad_rows']),

    'revenue_by_flow_order_matched': spec(m_revenue_by_flow_order_matched, RETENTION, '$', True, sources=['orders', 'flows']),
    'list_growth': spec(m_list_growth, RETENTION, 'n', True, sources=['list_growth']),
    'ltv_180d': spec(m_ltv_180d, RETENTION, '$', True, sources=['orders']),

    'contribution_margin': spec(m_contribution_margin, MONEY, '$', True, sources=['orders', 'products', 'reversed_orders', 'ad_rows']),
    'cash_runway_weeks': spec(m_cash_runway_weeks, MONEY, 'weeks', True, '13w', sources=['cash']),
    'sales_tax_collected': spec(m_sales_tax_collected, MONEY, '$', None, sources=['orders']),

    'fully_loaded_ms': spec(speed_metric('load_ms', 'fully_loaded_ms'), SPEED, 'ms', False, sources=['speed_runs'], formula='median load_ms over runs from `speed_runs`'),
    'lcp_ms': spec(speed_metric('lcp_ms'), SPEED, 'ms', False, sources=['speed_runs'], formula='median lcp_ms over runs from `speed_runs`'),
    'fcp_ms': spec(speed_metric('fcp_ms'), SPEED, 'ms', False, sources=['speed_runs'], formula='median fcp_ms over runs from `speed_runs`'),
    'bytes': spec(speed_metric('bytes'), SPEED, 'bytes', False, sources=['speed_runs'], formula='median bytes over runs from `speed_runs`'),
    'requests': spec(speed_metric('requests'), SPEED, 'n', False, sources=['speed_runs'], formula='median requests over runs from `speed_runs`'),
}

PIPELINE_METRICS = [name for name, s in METRICS.items() if s['group'] == PIPELINE]


def names():
    return list(METRICS)


def describe(name):
    s = METRICS[name]
    return {'name': name, 'group': s['group'], 'unit': s['unit'], 'higher_is_better': s['higher_is_better'],
            'default_window': s['window'], 'sources': s['sources'], 'formula': s['formula']}


def unavailable(name, reason, table=None, fix=None, ctx=None):
    s = METRICS.get(name, {})
    connector = CONNECTORS.get(table, table) if table else None
    out = {'metric': name, 'value': None, 'unit': s.get('unit'), 'higher_is_better': s.get('higher_is_better'),
           'unavailable': True, 'reason': reason,
           'fix': fix or (f'{connector} ({table} table)' if table else 'the query'),
           'window': ctx.window_dict() if ctx and ctx.end else {'label': 'current', 'days': ctx.days if ctx else None, 'start': None, 'end': None},
           'freshness': ctx.freshness() if ctx else None}
    if table:
        out['fix_table'] = table
        out['fix_connector'] = connector
    return out


def compute(name, data, offset=0, **kw):
    """One metric by contract name. Never raises for missing data; returns unavailable instead.

    kw comes from the query string: window (28d), end (YYYY-MM-DD), source, page,
    variant, windows. offset=1 computes the window before the current one.
    """
    if name not in METRICS:
        raise KeyError(name)
    s = METRICS[name]
    kw = {k: v for k, v in kw.items() if isinstance(v, str)}
    try:
        offset = max(0, int(offset))
    except (TypeError, ValueError):
        offset = 0
    try:
        ctx = Ctx(data, s, kw, offset)
    except Unavailable as exc:
        return unavailable(name, exc.reason, exc.table, exc.fix)
    try:
        result = s['fn'](ctx)
    except Unavailable as exc:
        return unavailable(name, exc.reason, exc.table, exc.fix, ctx)
    except KeyError as exc:  # a table read outside ctx (data.table raises KeyError when it is missing)
        table = exc.args[0] if exc.args else None
        if not isinstance(table, str) or data.table_path(table) is not None:
            raise
        return unavailable(name, f'table {table} is missing', table, None, ctx)
    label = 'current' if offset == 0 else f'prior {offset}'
    out = {'metric': name, 'unit': s['unit'], 'higher_is_better': s['higher_is_better'], 'unavailable': False}
    out.update(result)
    out.setdefault('window', ctx.window_dict(label))
    out.setdefault('freshness', ctx.freshness())
    if ctx.gaps:
        out['coverage'] = list(ctx.gaps)
    if s['formula']:
        out.setdefault('formula', s['formula'])
    return out


def pipeline(data, window='28d', windows='4', end=None, **kw):
    """Every pipeline metric for the current window and the trailing ones, plus money at stake.

    Each stage metric carries `values` (current first, then the trailing windows),
    `prior_median` and `delta` against it. `break` names the stage with the most
    money at stake, or null when no stage is below its own trailing median.
    """
    try:
        count = max(2, min(int(windows), 13))
    except (TypeError, ValueError):
        count = 4
    args = {'window': window, 'windows': str(count)}
    if end:
        args['end'] = end
    out = {'window': window, 'windows': count, 'metrics': {}, 'money_at_stake': None, 'break': None}
    for name in PIPELINE_METRICS:
        if name == 'money_at_stake':
            continue
        current = compute(name, data, **args)
        series, wins = [current.get('value')], [current.get('window')]
        if name != 'repeat_rate_90d':  # cohorts are their own window
            for i in range(1, count):
                r = compute(name, data, offset=i, **args)
                series.append(r.get('value'))
                wins.append(r.get('window'))
        prior = [v for v in series[1:] if v is not None]
        med = median(prior) if len(prior) >= 2 else None
        entry = dict(current, values=series, windows=wins, prior_median=med)
        if med and current.get('value') is not None:
            entry['delta'] = ratio(current['value'] - med, med)
        out['metrics'][name] = entry
    stake = compute('money_at_stake', data, **args)
    out['money_at_stake'] = stake
    if not stake.get('unavailable') and stake.get('stage'):
        top = next((r for r in stake['breakdown'] if r['stage'] == stake['stage']), {})
        out['break'] = {'stage': stake['stage'], 'money_at_stake': stake['value'], 'gap': top.get('gap'),
                        'current': top.get('current'), 'prior_median': top.get('prior_median'),
                        'change': top.get('change'), 'window': stake.get('window')}
    return out
