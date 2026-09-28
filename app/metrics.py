"""The metric contract in code: one function per metric in contracts/metrics.md.

server.py calls `compute(name, data, **query)` for one metric and
`pipeline(data, names, **query)` for the pipeline group with 4 trailing windows.
`data` is server.Data: `data.brand`, `data.table(name)` (KeyError when the table
is missing) and `data.meta(name)` (source and captured_at, for freshness).

Every answer is one of two shapes:
  {value, unit, unavailable: False, window, freshness, inputs, ...}
  {value: None, unavailable: True, reason, fix, window, freshness}
A missing table, field, blank cell or a window the data does not cover gives the
second shape, never 0. `brand=bombas` in the query reads app/data/brands/bombas/
(data/tables.py BrandData: aggregates first, data.sqlite when a metric needs rows)
instead of the server's sample brand. Ratios are window totals over window totals. Windows end
on brand.json `as_of` (the last full day) unless `end` asks for an earlier day.

Words used by more than one metric
  paid order   financial_status paid, partially_refunded or refunded, not cancelled
  net revenue  line subtotal minus discounts on paid orders; before tax, shipping
               charged and refunds (refunds are counted as a returns cost)
  day          the date of `created_at` for orders, `date` for daily tables
"""
import importlib.util
import json
import re
import statistics
from datetime import date, datetime, timedelta
from pathlib import Path

# Which connector fills a table for a real brand. Shown as `fix` when it is missing.
CONNECTOR = {
    'orders': 'shopify', 'customers': 'shopify', 'reversed_orders': 'shopify',
    'sessions': 'ga4', 'ad_rows': 'meta_ads', 'google_rows': 'google_ads',
    'flows': 'klaviyo', 'campaign_sends': 'klaviyo', 'payouts': 'shopify_payments',
    'speed_runs': 'speed_lab', 'carrier_events': 'carrier_events',
    'cash_balances': 'accounting', 'shipping_labels': 'shipping_labels',
    'finance_inputs': 'finance_inputs',
}
PAID_STATES = ('paid', 'partially_refunded', 'refunded')
COD_MARKETS = ('IN',)  # markets where cash on delivery, and so return to origin, exist
WALLETS = ('shop_pay', 'apple_pay', 'google_pay', 'paypal', 'amazon_pay')
BNPL = ('affirm', 'klarna', 'afterpay', 'sezzle')
FILTERS = ('device', 'channel', 'by', 'page', 'variant')
CHARGEBACK_BENCHMARK = 0.009
TRAILING_FOR_MEDIAN = 6
COHORTS = 6

# Paid channels: table, the brand.json channels key that says the brand runs it,
# and the table's field for each contract field.
PAID = {
    'meta': {'table': 'ad_rows', 'brand_key': 'paid_social',
             'fields': {'spend': 'spend', 'impressions': 'impressions', 'clicks': 'clicks',
                        'purchases': 'purchases', 'purchase_value': 'purchase_value', 'reach': 'reach'}},
    'google': {'table': 'google_rows', 'brand_key': 'google_ads',
               'fields': {'spend': 'cost', 'impressions': 'impressions', 'clicks': 'clicks',
                          'purchases': 'conversions', 'purchase_value': 'conversion_value'}},
}
PAID_UNITS = {'spend': 'usd', 'impressions': 'count', 'clicks': 'count', 'purchases': 'count', 'purchase_value': 'usd'}
SPEED = {'fully_loaded_ms': 'load_ms', 'lcp_ms': 'lcp_ms', 'fcp_ms': 'fcp_ms', 'bytes': 'bytes', 'requests': 'requests'}

METRICS = {}


def metric(*names, filters=()):
    def wrap(fn):
        for name in names:
            METRICS[name] = (fn, set(filters))
        return fn
    return wrap


class Unavailable(Exception):
    def __init__(self, reason, fix=None, **extra):
        super().__init__(reason)
        self.reason, self.fix, self.extra = reason, fix, extra


# ---------------------------------------------------------------- windows

class Window:
    def __init__(self, start, end):
        self.start, self.end = start, end
        self.days = (end - start).days + 1
        self.s, self.e = start.isoformat(), end.isoformat()

    def has(self, day):
        return self.s <= day <= self.e

    def shift(self, windows):
        """The window `windows` whole windows earlier."""
        step = timedelta(days=self.days * windows)
        return Window(self.start - step, self.end - step)

    def dict(self):
        return {'label': f'{self.days}d', 'start': self.s, 'end': self.e, 'days': self.days}


def last_full_day(data):
    raw = (data.brand or {}).get('as_of')
    if not raw:
        raise Unavailable('brand.json has no as_of day, so a window has no end', fix='brand.json')
    return date.fromisoformat(raw)


def parse_window(data, window=None, end=None):
    days = 28
    if window:
        m = re.fullmatch(r'(\d{1,3})d', str(window))
        if not m or not 1 <= int(m.group(1)) <= 400:
            raise ValueError('window must look like 28d, from 1d to 400d')
        days = int(m.group(1))
    last = last_full_day(data)
    stop = last
    if end:
        try:
            stop = date.fromisoformat(str(end))
        except ValueError:
            raise ValueError('end must be a day like 2026-09-24')
        if stop > last:
            raise ValueError(f'end is after the last full day, {last.isoformat()}')
    return Window(stop - timedelta(days=days - 1), stop)


def month_end(month):
    y, m = int(month[:4]), int(month[5:7])
    nxt = date(y + (m == 12), m % 12 + 1, 1)
    return nxt - timedelta(days=1)


def to_dt(value):
    return datetime.fromisoformat(str(value).replace('Z', '+00:00'))


# ---------------------------------------------------------------- context

class Ctx:
    """One metric call: the data, the window, the tables read (for freshness), notes."""

    def __init__(self, data):
        self.data, self.win, self.used, self.notes, self.filters = data, None, [], [], {}

    def rows(self, name):
        try:
            rows = self.data.table(name)
        except KeyError:
            raise Unavailable(f'the {name} table is not connected', fix=CONNECTOR.get(name))
        except ValueError:
            raise Unavailable(f'the {name} table is unreadable', fix=CONNECTOR.get(name))
        if name not in self.used:
            self.used.append(name)
        return rows

    def freshness(self):
        out = {'as_of': (self.data.brand or {}).get('as_of'), 'sources': []}
        for name in self.used:
            try:
                meta = self.data.meta(name)
            except (KeyError, ValueError):
                meta = {}
            out['sources'].append({'table': name, 'source': meta.get('source'), 'captured_at': meta.get('captured_at')})
        return out

    def base(self):
        out = {'window': self.win.dict() if self.win else None, 'freshness': self.freshness()}
        if self.filters:
            out['filters'] = dict(self.filters)
        if self.notes:
            out['notes'] = list(self.notes)
        return out

    def ok(self, value, unit, inputs=None, **extra):
        out = {'value': value, 'unit': unit, 'unavailable': False}
        out.update(self.base())
        if inputs is not None:
            out['inputs'] = inputs
        out.update(extra)
        return out

    def unavailable(self, exc):
        out = {'value': None, 'unavailable': True, 'reason': exc.reason, 'fix': exc.fix}
        out.update(self.base())
        out.update(exc.extra)
        return out


def need(rows, fields, table):
    if not rows:
        raise Unavailable(f'the {table} table has no rows', fix=CONNECTOR.get(table))
    missing = [f for f in fields if f not in rows[0]]
    if missing:
        raise Unavailable(f'the {table} table has no {", ".join(missing)} field', fix=CONNECTOR.get(table))


def cover(win, first, last, table):
    """The window must sit inside the days the table covers, or the totals would read low."""
    if not first or win.s < first or win.e > last:
        raise Unavailable(f'{table} covers {first} to {last}, not all of {win.s} to {win.e}',
                          fix=CONNECTOR.get(table))


def ratio(num, den, what):
    if not den:
        raise Unavailable(f'no {what} in this window, so the rate has no base')
    return round(num / den, 6)


def money(x):
    return round(x, 2)


_PREP = {}


def prep(key, rows, build):
    """Cache work derived from a table while the table object is the same one."""
    hit = _PREP.get(key)
    if hit and hit[0] is rows:
        return hit[1]
    value = build(rows)
    _PREP[key] = (rows, value)
    return value


def check_device(device, known):
    if device and device not in known:
        raise ValueError('device must be one of ' + ', '.join(known))


# ---------------------------------------------------------------- orders

def net_revenue(o):
    disc = o.get('discount')
    if isinstance(disc, dict):
        disc = disc.get('amount')
    return (o.get('subtotal') or 0) - (disc or 0)


def _build_orders(rows):
    days = [str(o.get('created_at') or '')[:10] for o in rows]
    paid, by_day, customers = [], {}, {}
    for day, o in zip(days, rows):
        if o.get('financial_status') not in PAID_STATES or o.get('cancelled_at'):
            continue
        net = net_revenue(o)
        paid.append((day, o.get('device'), net, o))
        agg = by_day.setdefault((day, o.get('device')), [0, 0.0])
        agg[0] += 1
        agg[1] += net
        if o.get('customer_id') is not None:
            customers.setdefault(o['customer_id'], []).append((to_dt(o['created_at']), net, bool(o.get('customer_is_new'))))
    for lst in customers.values():
        lst.sort(key=lambda t: t[0])
    return {'paid': paid, 'by_day': by_day, 'customers': customers, 'first': min(days) if days else None,
            'last': max(days) if days else None, 'devices': sorted({str(d) for d in (o.get('device') for o in rows) if d})}


def orders(ctx):
    rows = ctx.rows('orders')
    need(rows, ('created_at', 'financial_status', 'subtotal'), 'orders')
    return prep('orders', rows, _build_orders)


def order_totals(ctx, win, device=None):
    """Paid orders and net revenue in the window. A brand folder answers from its daily aggregate."""
    if hasattr(ctx.data, 'order_day_totals'):
        try:
            o = ctx.data.order_day_totals()
        except KeyError:
            raise Unavailable('the orders aggregate is missing', fix=CONNECTOR['orders'])
        if 'daily' not in ctx.used:
            ctx.used.append('daily')
        if device:
            raise Unavailable('orders by device are not in the daily aggregate', fix=CONNECTOR['orders'])
    else:
        o = orders(ctx)
    check_device(device, o['devices'])
    cover(win, o['first'], o['last'], 'orders')
    n, net = 0, 0.0
    for (day, dev), (cnt, rev) in o['by_day'].items():
        if win.has(day) and (device is None or dev == device):
            n += cnt
            net += rev
    return n, net


def paid_in_window(ctx, win, device=None):
    o = orders(ctx)
    check_device(device, o['devices'])
    cover(win, o['first'], o['last'], 'orders')
    return [r for r in o['paid'] if win.has(r[0]) and (device is None or r[1] == device)]


# ---------------------------------------------------------------- sessions

SESSION_FIELDS = ('sessions', 'product_view', 'add_to_cart', 'checkout')


def _build_sessions(rows):
    by_day, blanks = {}, set()
    for r in rows:
        key = (str(r['date']), r.get('device'))
        agg = by_day.setdefault(key, [0, 0, 0, 0])
        for i, f in enumerate(SESSION_FIELDS):
            if r.get(f) is None:
                blanks.add((key, f))
            else:
                agg[i] += r[f]
    days = [k[0] for k in by_day]
    return {'by_day': by_day, 'blanks': blanks, 'first': min(days) if days else None,
            'last': max(days) if days else None, 'devices': sorted({str(k[1]) for k in by_day if k[1]})}


def session_totals(ctx, win, device=None):
    rows = ctx.rows('sessions')
    need(rows, ('date', 'device') + SESSION_FIELDS, 'sessions')
    s = prep('sessions', rows, _build_sessions)
    check_device(device, s['devices'])
    cover(win, s['first'], s['last'], 'sessions')
    tot = [0, 0, 0, 0]
    for key, agg in s['by_day'].items():
        if win.has(key[0]) and (device is None or key[1] == device):
            for i in range(4):
                tot[i] += agg[i]
    for key, field in s['blanks']:
        if win.has(key[0]) and (device is None or key[1] == device):
            raise Unavailable(f'sessions has blank {field} cells in this window', fix='ga4')
    return dict(zip(SESSION_FIELDS, tot))


# ---------------------------------------------------------------- pipeline

def _device(ctx, kw):
    device = kw.get('device') or None
    if device:
        ctx.filters['device'] = device
    return device


@metric('sessions', filters=('device',))
def m_sessions(ctx, name, kw):
    t = session_totals(ctx, ctx.win, _device(ctx, kw))
    return ctx.ok(t['sessions'], 'count')


STAGE_RATES = {
    'product_view_rate': ('product_view', 'sessions', 'sessions'),
    'add_to_cart_rate': ('add_to_cart', 'sessions', 'sessions'),
    'checkout_rate': ('checkout', 'add_to_cart', 'sessions with add to cart'),
}


@metric(*STAGE_RATES, filters=('device',))
def m_stage_rate(ctx, name, kw):
    num, den, what = STAGE_RATES[name]
    t = session_totals(ctx, ctx.win, _device(ctx, kw))
    return ctx.ok(ratio(t[num], t[den], what), 'ratio', {'numerator': t[num], 'denominator': t[den]})


@metric('cvr_overall', filters=('device',))
def m_cvr(ctx, name, kw):
    device = _device(ctx, kw)
    n, _ = order_totals(ctx, ctx.win, device)
    s = session_totals(ctx, ctx.win, device)['sessions']
    return ctx.ok(ratio(n, s, 'sessions'), 'ratio', {'numerator': n, 'denominator': s})


@metric('aov', filters=('device',))
def m_aov(ctx, name, kw):
    n, net = order_totals(ctx, ctx.win, _device(ctx, kw))
    if not n:
        raise Unavailable('no paid orders in this window')
    return ctx.ok(money(net / n), 'usd', {'net_revenue': money(net), 'orders': n})


def mature_cohorts(ctx, days):
    """The last COHORTS monthly cohorts of first-time customers where everyone has had `days` days."""
    o = orders(ctx)
    end = ctx.win.end
    months = sorted({c[0][0].strftime('%Y-%m') for c in o['customers'].values() if c[0][2]})
    first_day = o['first']
    ok = [m for m in months if m + '-01' >= first_day and month_end(m) + timedelta(days=days) <= end]
    if not ok:
        raise Unavailable(f'no monthly cohort of first orders has had {days} days yet')
    ok = ok[-COHORTS:]
    ctx.win = None
    return ok, o['customers']


def cohort_window(months, days):
    return {'label': f'{len(months)} monthly cohorts', 'start': months[0] + '-01',
            'end': month_end(months[-1]).isoformat(), 'basis': f'first orders; each cohort has had {days} days'}


@metric('repeat_rate_90d')
def m_repeat(ctx, name, kw):
    months, customers = mature_cohorts(ctx, 90)
    rows = {m: [0, 0] for m in months}
    for lst in customers.values():
        first, _, is_new = lst[0]
        m = first.strftime('%Y-%m')
        if not is_new or m not in rows:
            continue
        rows[m][0] += 1
        if any(first < t <= first + timedelta(days=90) for t, _, _ in lst[1:]):
            rows[m][1] += 1
    firsts = sum(v[0] for v in rows.values())
    repeat = sum(v[1] for v in rows.values())
    cohorts = [{'cohort': m, 'customers': v[0], 'repeat': v[1], 'rate': round(v[1] / v[0], 6) if v[0] else None}
               for m, v in rows.items()]
    out = ctx.ok(ratio(repeat, firsts, 'first-time customers'), 'ratio',
                 {'numerator': repeat, 'denominator': firsts}, cohorts=cohorts)
    out['window'] = cohort_window(months, 90)
    return out


MONEY_STAGES = (  # stage, count in, count out
    ('product_view', 'sessions', 'product_view'),
    ('add_to_cart', 'product_view', 'add_to_cart'),
    ('checkout', 'add_to_cart', 'checkout'),
    ('purchase', 'checkout', 'orders'),
)


def stage_counts(ctx, win, device):
    t = session_totals(ctx, win, device)
    t['orders'], t['net_revenue'] = order_totals(ctx, win, device)
    return t


def stage_rates(t):
    return {s: (t[b] / t[a] if t[a] else None) for s, a, b in MONEY_STAGES}


@metric('money_at_stake', filters=('device',))
def m_money_at_stake(ctx, name, kw):
    device = _device(ctx, kw)
    now = stage_counts(ctx, ctx.win, device)
    cur = stage_rates(now)
    if not now['orders']:
        raise Unavailable('no paid orders in this window, so a unit has no value')
    aov = now['net_revenue'] / now['orders']
    history = []
    for k in range(1, TRAILING_FOR_MEDIAN + 1):
        try:
            history.append(stage_rates(stage_counts(ctx, ctx.win.shift(k), device)))
        except Unavailable:
            break
    if len(history) < 3:
        raise Unavailable(f'only {len(history)} earlier windows in the data; the median needs 3')
    stages = []
    for i, (stage, into, out) in enumerate(MONEY_STAGES):
        past = [h[stage] for h in history if h[stage] is not None]
        if cur[stage] is None or not past:
            raise Unavailable(f'the {stage} stage has no base in this window')
        median = statistics.median(past)
        downstream = aov
        for later, _, _ in MONEY_STAGES[i + 1:]:
            downstream *= cur[later] or 0
        gap = max(median - cur[stage], 0.0)
        stages.append({'stage': stage, 'current': round(cur[stage], 6), 'median': round(median, 6),
                       'gap': round(gap, 6), 'volume': now[into], 'value_per_unit': money(downstream),
                       'money': money(gap * now[into] * downstream)})
    top = max(stages, key=lambda s: s['money'])
    ctx.notes.append(f'Baseline is the median of the {len(history)} windows before this one. '
                     'No peer band is connected. Seasonal peaks are not adjusted.')
    return ctx.ok(top['money'], 'usd', {'aov': money(aov), 'orders': now['orders']},
                  break_stage=top['stage'] if top['money'] > 0 else None, stages=stages,
                  basis='own trailing median', total=money(sum(s['money'] for s in stages)))


# ---------------------------------------------------------------- reversed orders

def reversed_rows(ctx, kind):
    rows = ctx.rows('reversed_orders')
    need(rows, ('order_id', 'type', 'opened_at'), 'reversed_orders')
    return [r for r in rows if r.get('type') == kind]


def return_window_days(brand):
    m = re.search(r'(\d+)[- ]day', str((brand.get('policies') or {}).get('returns') or ''))
    return int(m.group(1)) if m else 30

def brand_sql(ctx):
    """data.sqlite's query function for a brand folder, or None for the sample brand (rows in memory)."""
    if getattr(ctx.data, 'sqlite', None) is None:
        return None
    return ctx.data._sql


def sql_rows(ctx, query, tables):
    try:
        rows = ctx.data._sql(query)
    except KeyError:
        raise Unavailable(f'the {tables[-1]} table is not connected', fix=CONNECTOR.get(tables[-1]))
    for t in tables:
        if t not in ctx.used:
            ctx.used.append(t)
    return rows


def sql_paid_orders(ctx, win):
    """Paid orders placed in the window, counted in data.sqlite so rates hold at any data scale."""
    paid = ', '.join(f"'{s}'" for s in PAID_STATES)
    span = sql_rows(ctx, 'SELECT MIN(substr(created_at, 1, 10)) AS first, MAX(substr(created_at, 1, 10)) AS last FROM orders',
                    ('orders',))
    cover(win, span[0]['first'], span[0]['last'], 'orders')
    return sql_rows(ctx, f"SELECT COUNT(*) AS n FROM orders WHERE status IN ({paid}) "
                         f"AND substr(created_at, 1, 10) BETWEEN '{win.s}' AND '{win.e}'", ('orders',))[0]['n']


@metric('return_rate')
def m_return_rate(ctx, name, kw):
    o = orders(ctx)
    cover(ctx.win, o['first'], o['last'], 'orders')
    delivered = set()
    for _, _, _, r in o['paid']:
        at = (r.get('fulfilment') or {}).get('delivered_at')
        if at and ctx.win.has(str(at)[:10]):
            delivered.add(r['id'])
    returns = [r for r in reversed_rows(ctx, 'return') if r['order_id'] in delivered]
    returned = {r['order_id'] for r in returns}
    by_reason, by_outcome = {}, {}
    for r in returns:
        by_reason[r.get('reason')] = by_reason.get(r.get('reason'), 0) + 1
        by_outcome[r.get('outcome')] = by_outcome.get(r.get('outcome'), 0) + 1
    days = return_window_days(ctx.data.brand)
    complete = ctx.win.end + timedelta(days=days) <= last_full_day(ctx.data)
    if not complete:
        ctx.notes.append(f'Returns can open up to {days} days after delivery, so this window is still filling.')
    return ctx.ok(ratio(len(returned), len(delivered), 'delivered orders'), 'ratio',
                  {'numerator': len(returned), 'denominator': len(delivered)}, complete=complete,
                  by_reason=sorted(by_reason.items(), key=lambda kv: -kv[1]), by_outcome=by_outcome,
                  basis='orders delivered in the window, returns opened any time up to as_of')


@metric('returns_by_reason')
def m_returns_by_reason(ctx, name, kw):
    """Returns opened in the window by reason: count, refunded amount and returns per paid order placed in the
    same window (both counts from the same source, so the rate holds at any data scale). Carrier returns excluded."""
    if getattr(ctx.data, 'sqlite', None) is not None:
        sql = ctx.data._sql
        paid = ', '.join(f"'{s}'" for s in PAID_STATES)
        try:
            span = sql('SELECT MIN(substr(created_at, 1, 10)) AS first, MAX(substr(created_at, 1, 10)) AS last FROM orders')
            cover(ctx.win, span[0]['first'], span[0]['last'], 'orders')
            n = sql(f"SELECT COUNT(*) AS n FROM orders WHERE status IN ({paid}) "
                    f"AND substr(created_at, 1, 10) BETWEEN '{ctx.win.s}' AND '{ctx.win.e}'")[0]['n']
            rows = sql("SELECT reason, COUNT(*) AS returns, SUM(COALESCE(amount, 0)) AS amount FROM reversed_orders "
                       f"WHERE type = 'return' AND substr(opened_at, 1, 10) BETWEEN '{ctx.win.s}' AND '{ctx.win.e}' "
                       "GROUP BY reason")
        except KeyError:
            raise Unavailable('the reversed_orders table is not connected', fix=CONNECTOR['reversed_orders'])
        for t in ('orders', 'reversed_orders'):
            if t not in ctx.used:
                ctx.used.append(t)
        by = {r['reason']: [r['returns'], r['amount']] for r in rows}
    else:
        n = len(paid_in_window(ctx, ctx.win))
        by = {}
        for r in reversed_rows(ctx, 'return'):
            if ctx.win.has(str(r.get('opened_at') or '')[:10]):
                b = by.setdefault(r.get('reason'), [0, 0.0])
                b[0] += 1
                b[1] += r.get('amount') or 0
    if not n:
        raise Unavailable('no paid orders in this window, so returns have no base')
    by.pop('carrier_returned', None)
    groups = [{'reason': k, 'returns': v[0], 'amount': money(v[1]), 'per_order': round(v[0] / n, 6)}
              for k, v in sorted(by.items(), key=lambda kv: -kv[1][0])]
    total = sum(g['returns'] for g in groups)
    return ctx.ok(total, 'count', {'returns': total, 'paid_orders': n}, groups=groups,
                  basis='returns opened in the window; per_order is over paid orders placed in the same window')


@metric('chargeback_rate')
def m_chargeback_rate(ctx, name, kw):
    if brand_sql(ctx):
        n = sql_paid_orders(ctx, ctx.win)
        rows = sql_rows(ctx, "SELECT reason, COUNT(*) AS n, SUM(COALESCE(amount, 0)) AS amount FROM reversed_orders "
                             f"WHERE type = 'chargeback' AND substr(opened_at, 1, 10) BETWEEN '{ctx.win.s}' AND '{ctx.win.e}' "
                             "GROUP BY reason", ('orders', 'reversed_orders'))
        by_reason = {r['reason']: r['n'] for r in rows}
        count, amount = sum(by_reason.values()), sum(r['amount'] or 0 for r in rows)
    else:
        n, _ = order_totals(ctx, ctx.win)
        cbs = [r for r in reversed_rows(ctx, 'chargeback') if ctx.win.has(str(r['opened_at'])[:10])]
        by_reason = {}
        for r in cbs:
            by_reason[r.get('reason')] = by_reason.get(r.get('reason'), 0) + 1
        count, amount = len(cbs), sum(r.get('amount') or 0 for r in cbs)
    value = ratio(count, n, 'paid orders')
    return ctx.ok(value, 'ratio', {'numerator': count, 'denominator': n},
                  benchmark={'max': CHARGEBACK_BENCHMARK, 'over': value > CHARGEBACK_BENCHMARK}, amount=money(amount),
                  by_reason=sorted(by_reason.items(), key=lambda kv: -kv[1]),
                  basis='chargebacks opened in the window over paid orders placed in the window')


@metric('dispute_win_rate')
def m_dispute_win_rate(ctx, name, kw):
    if brand_sql(ctx):
        sql_paid_orders(ctx, ctx.win)  # the window must sit inside the order history
        rows = sql_rows(ctx, "SELECT outcome, COUNT(*) AS n FROM reversed_orders WHERE type = 'chargeback' AND "
                             f"(outcome IN ('open', 'needs_response') OR substr(closed_at, 1, 10) BETWEEN '{ctx.win.s}' AND '{ctx.win.e}') "
                             "GROUP BY outcome", ('orders', 'reversed_orders'))
        by = {r['outcome']: r['n'] for r in rows}
        won, closed = by.get('won', 0), by.get('won', 0) + by.get('lost', 0)
        return ctx.ok(ratio(won, closed, 'closed disputes'), 'ratio', {'numerator': won, 'denominator': closed},
                      open_now=by.get('open', 0) + by.get('needs_response', 0))
    o = orders(ctx)
    cover(ctx.win, o['first'], o['last'], 'orders')
    cbs = reversed_rows(ctx, 'chargeback')
    closed = [r for r in cbs if r.get('closed_at') and ctx.win.has(str(r['closed_at'])[:10]) and r.get('outcome') in ('won', 'lost')]
    won = sum(1 for r in closed if r['outcome'] == 'won')
    still_open = sum(1 for r in cbs if r.get('outcome') == 'open')
    return ctx.ok(ratio(won, len(closed), 'closed disputes'), 'ratio',
                  {'numerator': won, 'denominator': len(closed)}, open_now=still_open)


@metric('return_to_sender_rate')
def m_return_to_sender(ctx, name, kw):
    if brand_sql(ctx):
        try:
            ctx.data.table('carrier_events')
        except (KeyError, ValueError):
            # No carrier feed: the Shopify return a carrier sends back (reason carrier_returned) stands in.
            n = sql_paid_orders(ctx, ctx.win)
            back = sql_rows(ctx, "SELECT COUNT(DISTINCT order_id) AS n FROM reversed_orders WHERE reason = 'carrier_returned' "
                                 f"AND substr(opened_at, 1, 10) BETWEEN '{ctx.win.s}' AND '{ctx.win.e}'",
                            ('orders', 'reversed_orders'))[0]['n']
            return ctx.ok(ratio(back, n, 'paid orders'), 'ratio', {'numerator': back, 'denominator': n},
                          basis='carrier returns opened in the window over paid orders placed in the window; '
                                'no carrier_events feed, so shipped orders are not counted')
    events = ctx.rows('carrier_events')
    need(events, ('order_id', 'event', 'date'), 'carrier_events')
    o = orders(ctx)
    cover(ctx.win, o['first'], o['last'], 'orders')
    shipped = {r['id'] for _, _, _, r in o['paid']
               if (r.get('fulfilment') or {}).get('shipped_at') and ctx.win.has(str(r['fulfilment']['shipped_at'])[:10])}
    back = {e['order_id'] for e in events if e.get('event') == 'return_to_sender' and e['order_id'] in shipped}
    return ctx.ok(ratio(len(back), len(shipped), 'shipped orders'), 'ratio',
                  {'numerator': len(back), 'denominator': len(shipped)})


def market(ctx):
    return str((ctx.data.brand or {}).get('market') or '').upper()


@metric('rto_rate')
def m_rto_rate(ctx, name, kw):
    if market(ctx) not in COD_MARKETS:
        raise Unavailable(f'market {market(ctx) or "unset"} has no cash on delivery, so there is no return to origin leg',
                          not_applicable=True)
    cod = [r for _, _, _, r in paid_in_window(ctx, ctx.win) if r.get('payment_method') == 'cod']
    ids = {r['id'] for r in cod}
    rto = {r['order_id'] for r in reversed_rows(ctx, 'rto') if r['order_id'] in ids}
    return ctx.ok(ratio(len(rto), len(cod), 'cash on delivery orders'), 'ratio',
                  {'numerator': len(rto), 'denominator': len(cod)})


def pay_group(method):
    if method == 'cod':
        return 'cod'
    if method in WALLETS:
        return 'wallet'
    if method in BNPL:
        return 'bnpl'
    if method == 'card':
        return 'card'
    return 'other'


@metric('payment_method_mix')
def m_payment_mix(ctx, name, kw):
    if brand_sql(ctx):
        sql_paid_orders(ctx, ctx.win)
        paid = ', '.join(f"'{s}'" for s in PAID_STATES)
        counts = {r['m']: r['n'] for r in sql_rows(
            ctx, f"SELECT COALESCE(payment_method, 'unknown') AS m, COUNT(*) AS n FROM orders WHERE status IN ({paid}) "
                 f"AND substr(created_at, 1, 10) BETWEEN '{ctx.win.s}' AND '{ctx.win.e}' GROUP BY m", ('orders',))}
    else:
        counts = {}
        for _, _, _, r in paid_in_window(ctx, ctx.win):
            m = r.get('payment_method') or 'unknown'
            counts[m] = counts.get(m, 0) + 1
    if not counts:
        raise Unavailable('no paid orders in this window')
    by_method, by_group = {}, {'card': 0, 'wallet': 0, 'bnpl': 0, 'cod': 0}
    for m, c in counts.items():
        by_method[m] = c
        by_group[pay_group(m)] = by_group.get(pay_group(m), 0) + c
    n = sum(counts.values())
    shares = {g: round(c / n, 6) for g, c in by_group.items()}
    if market(ctx) not in COD_MARKETS:
        shares['cod'] = None
    return ctx.ok(shares, 'share', {'orders': n}, counts=by_group,
                  by_method={m: round(c / n, 6) for m, c in sorted(by_method.items(), key=lambda kv: -kv[1])})


@metric('reversed_by_month')
def m_reversed_by_month(ctx, name, kw):
    """The reversed-order legs by calendar month inside the window: paid orders placed, returns opened (carrier returns
    out), carrier returns, chargebacks and inquiries opened, each also per 1,000 paid orders. Months the window cuts
    are flagged partial, never dropped silently."""
    if brand_sql(ctx):
        paid = ', '.join(f"'{s}'" for s in PAID_STATES)
        sql_paid_orders(ctx, ctx.win)
        orders_m = {r['m']: r['n'] for r in sql_rows(
            ctx, f"SELECT substr(created_at, 1, 7) AS m, COUNT(*) AS n FROM orders WHERE status IN ({paid}) "
                 f"AND substr(created_at, 1, 10) BETWEEN '{ctx.win.s}' AND '{ctx.win.e}' GROUP BY m", ('orders',))}
        rev = sql_rows(ctx, "SELECT substr(opened_at, 1, 7) AS m, type, reason = 'carrier_returned' AS carrier, COUNT(*) AS n "
                            f"FROM reversed_orders WHERE substr(opened_at, 1, 10) BETWEEN '{ctx.win.s}' AND '{ctx.win.e}' "
                            "GROUP BY m, type, carrier", ('orders', 'reversed_orders'))
    else:
        orders_m = {}
        for day, _, _, _ in paid_in_window(ctx, ctx.win):
            orders_m[day[:7]] = orders_m.get(day[:7], 0) + 1
        agg = {}
        for r in ctx.rows('reversed_orders'):
            day = str(r.get('opened_at') or '')[:10]
            if ctx.win.has(day):
                k = (day[:7], r.get('type'), r.get('reason') == 'carrier_returned')
                agg[k] = agg.get(k, 0) + 1
        rev = [{'m': k[0], 'type': k[1], 'carrier': k[2], 'n': v} for k, v in agg.items()]
    legs = {m: {'returns': 0, 'carrier_returns': 0, 'chargebacks': 0, 'inquiries': 0} for m in orders_m}
    for r in rev:
        if r['m'] not in legs:
            continue
        if r['type'] == 'return':
            key = 'carrier_returns' if r['carrier'] else 'returns'
        else:
            key = {'chargeback': 'chargebacks', 'inquiry': 'inquiries'}.get(r['type'])
        if key:
            legs[r['m']][key] += r['n']
    groups = []
    for m in sorted(orders_m):
        n = orders_m[m]
        g = {'month': m, 'paid_orders': n, 'partial': f'{m}-01' < ctx.win.s or month_end(m).isoformat() > ctx.win.e,
             **legs[m]}
        for k in ('returns', 'carrier_returns', 'chargebacks', 'inquiries'):
            g[f'{k}_per_1000'] = round(legs[m][k] / n * 1000, 3) if n else None
        groups.append(g)
    if not groups:
        raise Unavailable('no paid orders in this window')
    return ctx.ok(len(groups), 'count', {'months': len(groups)}, groups=groups,
                  basis='each leg opened in the month over paid orders placed in the same month')


@metric('open_disputes')
def m_open_disputes(ctx, name, kw):
    """Chargebacks and inquiries still waiting for a response at the window end: count and disputed amount, and the
    part opened `older_than` days or more before it (default 21)."""
    older = int(kw.get('older_than') or 21)
    cut = (ctx.win.end - timedelta(days=older)).isoformat()
    if brand_sql(ctx):
        rows = sql_rows(ctx, f"SELECT type, substr(opened_at, 1, 10) <= '{cut}' AS aged, COUNT(*) AS n, "
                             "SUM(COALESCE(amount, 0)) AS amount FROM reversed_orders WHERE type IN ('chargeback', 'inquiry') "
                             f"AND outcome IN ('open', 'needs_response') AND substr(opened_at, 1, 10) <= '{ctx.win.e}' "
                             "GROUP BY type, aged", ('reversed_orders',))
    else:
        agg = {}
        for r in ctx.rows('reversed_orders'):
            day = str(r.get('opened_at') or '')[:10]
            if r.get('type') in ('chargeback', 'inquiry') and r.get('outcome') in ('open', 'needs_response') and day <= ctx.win.e:
                a = agg.setdefault((r['type'], day <= cut), [0, 0.0])
                a[0] += 1
                a[1] += r.get('amount') or 0
        rows = [{'type': k[0], 'aged': k[1], 'n': v[0], 'amount': v[1]} for k, v in agg.items()]
    out = {'count': 0, 'amount': 0.0, 'aged_count': 0, 'aged_amount': 0.0, 'by_type': {}}
    for r in rows:
        t = out['by_type'].setdefault(r['type'], {'count': 0, 'amount': 0.0, 'aged_count': 0, 'aged_amount': 0.0})
        for o in (out, t):
            o['count'] += r['n']
            o['amount'] += r['amount'] or 0
            if r['aged']:
                o['aged_count'] += r['n']
                o['aged_amount'] += r['amount'] or 0
    for o in [out, *out['by_type'].values()]:
        o['amount'], o['aged_amount'] = money(o['amount']), money(o['aged_amount'])
    return ctx.ok(out.pop('count'), 'count', {'older_than_days': older, 'opened_on_or_before': cut}, **out,
                  basis='disputes with outcome open or needs_response, opened by the window end')


@metric('payout_reversals')
def m_payout_reversals(ctx, name, kw):
    """What left the payouts in the window: refunds and adjustments (chargeback withdrawals and reversals), with gross
    charges and fees, summed over payouts issued in the window."""
    rows = ctx.rows('payouts')
    if rows and 'issued_at' in rows[0]:  # Shopify Payments payout: refunds and adjustments are negative
        need(rows, ('issued_at', 'charges_gross', 'refunds_gross', 'adjustments_gross'), 'payouts')
        pick = lambda r: (str(r['issued_at'])[:10], r.get('charges_gross') or 0, r.get('charges_fee') or 0,
                          r.get('refunds_gross') or 0, r.get('adjustments_gross') or 0, r.get('net') or 0)
    else:  # gateway settlement rows: refunds and chargebacks are positive amounts taken out
        need(rows, ('deposit_date', 'gross', 'refunds', 'chargebacks'), 'payouts')
        pick = lambda r: (str(r['deposit_date'])[:10], r.get('gross') or 0, r.get('fees') or 0, -(r.get('refunds') or 0),
                          -((r.get('chargebacks') or 0) + (r.get('chargeback_fees') or 0)), r.get('net') or 0)
    inside = [pick(r) for r in rows if ctx.win.has(pick(r)[0])]
    if not inside:
        raise Unavailable('no payouts issued in this window', fix=CONNECTOR['payouts'])
    tot = {k: money(sum(r[i] for r in inside)) for i, k in ((1, 'charges_gross'), (2, 'charges_fee'),
                                                          (3, 'refunds_gross'), (5, 'net'))}
    adj = money(sum(r[4] for r in inside))
    return ctx.ok(adj, 'usd', {'payouts': len(inside)}, **tot,
                  basis='payouts issued in the window; value is adjustments (chargeback withdrawals); refunds and adjustments are negative')


# ---------------------------------------------------------------- order value (04)

def _order_value_sql(ctx, win, step):
    """Order value bins from data.sqlite with one GROUP BY, for a brand folder whose orders are too many to load."""
    sql = getattr(ctx.data, '_sql', None)
    if sql is None or not getattr(ctx.data, 'sqlite', None):
        raise Unavailable('the orders table is unreadable', fix=CONNECTOR['orders'])
    paid = ', '.join(f"'{s}'" for s in PAID_STATES)
    try:
        span = sql('SELECT MIN(substr(created_at, 1, 10)) AS first, MAX(substr(created_at, 1, 10)) AS last FROM orders')
        cover(win, span[0]['first'], span[0]['last'], 'orders')
        rows = sql(
            f'SELECT CAST((subtotal - COALESCE(discount, 0)) / {step} AS INTEGER) AS bin, COUNT(*) AS orders, '
            f'SUM(subtotal - COALESCE(discount, 0)) AS value, SUM(CASE WHEN shipping > 0 THEN 1 ELSE 0 END) AS paid_shipping, '
            f'SUM(COALESCE(shipping, 0)) AS shipping FROM orders WHERE status IN ({paid}) '
            f"AND substr(created_at, 1, 10) BETWEEN '{win.s}' AND '{win.e}' GROUP BY bin ORDER BY bin")
    except KeyError:
        raise Unavailable('the orders table is not connected', fix=CONNECTOR['orders'])
    if 'orders' not in ctx.used:
        ctx.used.append('orders')
    return {r['bin']: [r['orders'], r['value'], r['paid_shipping'], r['shipping']] for r in rows}


@metric('order_value_distribution')
def m_order_value_distribution(ctx, name, kw):
    """Paid orders by order value (subtotal minus discounts, before tax and shipping) in bins of `step` dollars (default 5).
    Each bin carries orders, share of orders, value, and how many orders paid shipping. For a free shipping threshold."""
    step = int(kw.get('step') or 5)
    if step < 1 or step > 100:
        raise ValueError('step must be 1 to 100 dollars')
    if getattr(ctx.data, 'sqlite', None) is not None:
        bins = _order_value_sql(ctx, ctx.win, step)
    else:
        bins = {}
        for _, _, net, o in paid_in_window(ctx, ctx.win):
            b = bins.setdefault(int(net // step), [0, 0.0, 0, 0.0])
            ship = o.get('shipping')
            b[0] += 1
            b[1] += net
            b[2] += 1 if (ship or 0) > 0 else 0
            b[3] += ship or 0
    n = sum(b[0] for b in bins.values())
    if not n:
        raise Unavailable('no paid orders in this window')
    groups = [{'from': k * step, 'to': (k + 1) * step, 'orders': v[0], 'share': round(v[0] / n, 6),
               'value': money(v[1]), 'paid_shipping_orders': v[2], 'shipping_charged': money(v[3])}
              for k, v in sorted(bins.items())]
    total = sum(g['value'] for g in groups)
    return ctx.ok(n, 'count', {'orders': n, 'value': money(total), 'step': step}, groups=groups,
                  basis='paid orders; order value is subtotal minus discounts, before tax and shipping')


# ---------------------------------------------------------------- session funnel (07)

FUNNEL_FIELDS = ('sessions', 'product_view', 'add_to_cart', 'checkout', 'purchase')
FUNNEL_BY = {'device': 'device', 'channel_group': 'channel_group', 'landing_page': 'landing_page',
             'campaign': 'session_campaign'}
FUNNEL_FILTERS = {'device': 'device', 'channel': 'channel_group', 'page': 'landing_page'}
SAFE_VALUE = re.compile(r"^[A-Za-z0-9 /_.,|&+()'-]{1,120}$")


def funnel_rates(t):
    """Step rates from funnel counts. None where the step has no base."""
    div = lambda a, b: round(t[a] / t[b], 6) if t.get(b) else None
    return {'add_to_cart_rate': div('add_to_cart', 'sessions'), 'checkout_rate': div('checkout', 'add_to_cart'),
            'purchase_rate': div('purchase', 'checkout'), 'conversion_rate': div('purchase', 'sessions')}


def _funnel_sql(ctx, win, where, col):
    sql = ctx.data._sql
    try:
        span = sql('SELECT MIN(date) AS first, MAX(date) AS last FROM sessions')
        cover(win, span[0]['first'], span[0]['last'], 'sessions')
        conds = [f"date BETWEEN '{win.s}' AND '{win.e}'"] + [f"{c} = '{v.replace(chr(39), chr(39) * 2)}'" for c, v in where.items()]
        sums = ', '.join(f'SUM({f}) AS {f}' for f in FUNNEL_FIELDS)
        flags = 'SUM(CASE WHEN sampled THEN 1 ELSE 0 END) AS sampled, SUM(CASE WHEN thresholded THEN 1 ELSE 0 END) AS thresholded'
        key = f'{col} AS grp, ' if col else "'all' AS grp, "
        rows = sql(f"SELECT {key}{sums}, {flags} FROM sessions WHERE {' AND '.join(conds)}"
                   + (f' GROUP BY {col} ORDER BY {col}' if col else ''))
    except KeyError:
        raise Unavailable('the sessions table is not connected', fix=CONNECTOR['sessions'])
    return [r for r in rows if r['sessions']]


def _funnel_rows(ctx, win, where, col):
    rows = ctx.rows('sessions')
    need(rows, ('date',) + FUNNEL_FIELDS + tuple(where) + ((col,) if col else ()), 'sessions')
    first, last = prep('sessions_span', rows, _build_span)
    cover(win, first, last, 'sessions')
    out = {}
    for r in rows:
        if not win.has(str(r['date'])) or any(r.get(c) != v for c, v in where.items()):
            continue
        g = out.setdefault(r.get(col) if col else 'all', {'grp': r.get(col) if col else 'all', 'sampled': 0, 'thresholded': 0,
                                                            **{f: 0 for f in FUNNEL_FIELDS}})
        for f in FUNNEL_FIELDS:
            if r.get(f) is None:
                raise Unavailable(f'sessions has blank {f} cells in this window', fix='ga4')
            g[f] += r[f]
        g['sampled'] += 1 if r.get('sampled') else 0
        g['thresholded'] += 1 if r.get('thresholded') else 0
    return [g for g in out.values() if g['sessions']]


@metric('session_funnel', filters=('device', 'channel', 'page', 'by'))
def m_session_funnel(ctx, name, kw):
    """Sessions to add to cart to checkout to purchase from the GA4 sessions table, with step rates.
    Filters: device, channel (GA4 channel group), page (landing page). by: device, channel_group,
    landing_page or campaign returns `groups`. Purchase is GA4 ecommercePurchases, not Shopify orders."""
    where = {}
    for key, col in FUNNEL_FILTERS.items():
        v = kw.get(key)
        if v:
            if not SAFE_VALUE.match(str(v)):
                raise ValueError(f'{key} has characters a filter cannot take')
            where[col] = str(v)
            ctx.filters[key] = str(v)
    by = kw.get('by') or None
    if by and by not in FUNNEL_BY:
        raise ValueError('by must be one of ' + ', '.join(FUNNEL_BY))
    col = FUNNEL_BY.get(by)
    if by:
        ctx.filters['by'] = by
    if getattr(ctx.data, 'sqlite', None) is not None:
        rows = _funnel_sql(ctx, ctx.win, where, col)
        if 'sessions' not in ctx.used:
            ctx.used.append('sessions')
    else:
        rows = _funnel_rows(ctx, ctx.win, where, col)
    if not rows:
        raise Unavailable('no sessions match these filters in this window', fix=CONNECTOR['sessions'])
    tot = {f: int(sum(r[f] for r in rows)) for f in FUNNEL_FIELDS}
    flags = {'sampled_rows': int(sum(r['sampled'] or 0 for r in rows)), 'thresholded_rows': int(sum(r['thresholded'] or 0 for r in rows))}
    extra = {'rates': funnel_rates(tot), **flags,
             'basis': 'GA4 sessions table; product_view, add_to_cart and checkout are event counts; '
                      'purchase is GA4 ecommercePurchases, not Shopify orders'}
    if by:
        groups = []
        for r in sorted(rows, key=lambda r: -r['sessions']):
            g = {by: r['grp'], **{f: int(r[f]) for f in FUNNEL_FIELDS}}
            g.update(funnel_rates(g))
            groups.append(g)
        extra['groups'] = groups
    return ctx.ok(tot['sessions'], 'count', tot, **extra)


# ---------------------------------------------------------------- paid

def paid_channels(ctx, kw):
    channel = kw.get('channel') or None
    if channel:
        if channel not in PAID:
            raise ValueError('channel must be one of ' + ', '.join(PAID))
        ctx.filters['channel'] = channel
        return [channel]
    runs = (ctx.data.brand or {}).get('channels')
    if not isinstance(runs, dict):
        return list(PAID)
    return [c for c, spec in PAID.items() if runs.get(spec['brand_key']) not in (None, False, 'none')]


def _build_span(rows):
    days = [str(r['date']) for r in rows]
    return (min(days), max(days)) if days else (None, None)


def _build_campaign_rows(rows):
    return [r for r in rows if r.get('row_kind') == 'campaign']


def paid_rows(spec, rows):
    """The rows a paid total sums, and the column for each contract field.

    Google Ads v2 tables (`row_kind` column) hold campaign, search_term and asset_group
    rows that are never summed together: totals read the campaign rows only. They name
    cost `spend`; the older sample brand names it `cost`."""
    fields = dict(spec['fields'])
    if rows and 'row_kind' in rows[0]:
        rows = prep(spec['table'] + ':campaign', rows, _build_campaign_rows)
    if rows and fields.get('spend') == 'cost' and 'cost' not in rows[0] and 'spend' in rows[0]:
        fields['spend'] = 'spend'
    return rows, fields


def shared_key(r):
    """Ads share a creative when they run the same image or video (census shape), else the same creative id."""
    return r.get('image_hash') or r.get('video_id') or r.get('creative_id')


GROUP_KEYS = {'campaign': lambda r: r.get('campaign_name') or r.get('campaign'),
              'adset': lambda r: r.get('adset_id'),
              'ad': lambda r: r.get('ad_id'),
              'day': lambda r: str(r['date'])}


def paid_totals(ctx, kw, by=None):
    chans = paid_channels(ctx, kw)
    if not chans:
        raise Unavailable('brand.json lists no paid channel')
    if by in ('ad', 'adset') and chans != ['meta']:
        raise ValueError(f'by={by} needs channel=meta; Google rows are by campaign and search term')
    tot = {f: 0.0 for f in PAID_UNITS}
    tot['reach'] = None
    by_channel, groups, creatives = {}, {}, {}
    for c in chans:
        spec = PAID[c]
        rows, fields = paid_rows(spec, ctx.rows(spec['table']))
        spec = dict(spec, fields=fields)
        need(rows, ('date',) + tuple(fields.values()), spec['table'])
        first, last = prep(spec['table'] + ':span', rows, _build_span)
        cover(ctx.win, first, last, spec['table'])
        ch = {f: 0.0 for f in fields}
        for r in rows:
            if not ctx.win.has(str(r['date'])):
                continue
            for f, col in fields.items():
                if r.get(col) is None:
                    raise Unavailable(f'{spec["table"]} has blank {col} cells in this window', fix=CONNECTOR[spec['table']])
                ch[f] += r[col]
            if by:
                key = GROUP_KEYS[by](r)
                g = groups.get((c, key))
                if g is None:
                    g = groups[(c, key)] = {'channel': c, by: key, **{f: 0.0 for f in PAID_UNITS}}
                    if 'reach' in fields:
                        g['reach'] = 0.0
                for f in PAID_UNITS:
                    g[f] += r[fields[f]]
                if 'reach' in g:
                    g['reach'] += r[fields['reach']]
                if by in ('ad', 'adset'):
                    g['campaign_id'] = r.get('campaign_id')
                    g['campaign_name'] = r.get('campaign_name')
                    g['adset_name'] = r.get('adset_name')
                if by == 'ad':
                    g['adset_id'] = r.get('adset_id')
                    g['ad_name'] = r.get('ad_name')
                    g['creative_id'] = r.get('creative_id')
                    g['format'] = r.get('format')
                    g['shared_key'] = shared_key(r)
                    g['dynamic_creative'] = g.get('dynamic_creative', False) or bool(r.get('is_dynamic_creative') or r.get('is_dynamic'))
                    g['first_day'] = min(g.get('first_day') or str(r['date']), str(r['date']))
                    g['last_day'] = max(g.get('last_day') or str(r['date']), str(r['date']))
                    creatives.setdefault(shared_key(r), set()).add(key)
        for f in PAID_UNITS:
            tot[f] += ch[f]
        if 'reach' in ch:
            tot['reach'] = (tot['reach'] or 0) + ch['reach']
        by_channel[c] = {f: (money(v) if PAID_UNITS.get(f) == 'usd' else int(round(v))) for f, v in ch.items()}
    out_groups = None
    if by:
        out_groups = []
        for g in groups.values():
            for f in PAID_UNITS:
                g[f] = money(g[f]) if PAID_UNITS[f] == 'usd' else int(round(g[f]))
            g['roas'] = round(g['purchase_value'] / g['spend'], 4) if g['spend'] else None
            g['cpa'] = money(g['spend'] / g['purchases']) if g['purchases'] else None
            g['ctr'] = round(g['clicks'] / g['impressions'], 6) if g['impressions'] else None
            if 'reach' in g:
                g['reach'] = int(round(g['reach']))
                g['frequency'] = round(g['impressions'] / g['reach'], 4) if g['reach'] else None
            if by == 'ad':
                g['shared_creative'] = len(creatives.get(g['shared_key'], ())) > 1
            out_groups.append(g)
        if by == 'day':
            out_groups.sort(key=lambda g: g['day'])
        else:
            out_groups.sort(key=lambda g: -g['spend'])
    return tot, by_channel, out_groups


def paid_by(ctx, kw):
    by = kw.get('by') or None
    if by and by not in GROUP_KEYS:
        raise ValueError('by must be one of ' + ', '.join(GROUP_KEYS))
    if by:
        ctx.filters['by'] = by
    return by


PLATFORM = 'platform reported purchases and value (Meta 7 day click, 1 day view; Google conversions), not matched to orders'


@metric(*PAID_UNITS, filters=('channel', 'by'))
def m_paid_sum(ctx, name, kw):
    by = paid_by(ctx, kw)
    tot, by_channel, groups = paid_totals(ctx, kw, by)
    unit = PAID_UNITS[name]
    value = money(tot[name]) if unit == 'usd' else int(round(tot[name]))
    extra = {'by_channel': {c: v[name] for c, v in by_channel.items()}}
    if groups is not None:
        extra['groups'] = groups
    if name in ('purchases', 'purchase_value'):
        extra['basis'] = PLATFORM
    return ctx.ok(value, unit, **extra)


@metric('period_roas', filters=('channel', 'by'))
def m_roas(ctx, name, kw):
    by = paid_by(ctx, kw)
    tot, by_channel, groups = paid_totals(ctx, kw, by)
    extra = {'by_channel': {c: (round(v['purchase_value'] / v['spend'], 4) if v['spend'] else None) for c, v in by_channel.items()},
             'basis': PLATFORM}
    if groups is not None:
        extra['groups'] = groups
    return ctx.ok(round(ratio(tot['purchase_value'], tot['spend'], 'spend'), 4), 'x',
                  {'purchase_value': money(tot['purchase_value']), 'spend': money(tot['spend'])}, **extra)


@metric('cpa', filters=('channel', 'by'))
def m_cpa(ctx, name, kw):
    by = paid_by(ctx, kw)
    tot, by_channel, groups = paid_totals(ctx, kw, by)
    if not tot['purchases']:
        raise Unavailable('no purchases in this window, so cost per purchase has no base')
    extra = {'by_channel': {c: (money(v['spend'] / v['purchases']) if v['purchases'] else None) for c, v in by_channel.items()},
             'basis': PLATFORM}
    if groups is not None:
        extra['groups'] = groups
    return ctx.ok(money(tot['spend'] / tot['purchases']), 'usd',
                  {'spend': money(tot['spend']), 'purchases': int(round(tot['purchases']))}, **extra)


@metric('frequency', filters=('channel',))
def m_frequency(ctx, name, kw):
    if kw.get('channel') and kw['channel'] != 'meta':
        paid_channels(ctx, kw)
        raise Unavailable(f'{kw["channel"]} reports no reach, so frequency has no base')
    tot, _, _ = paid_totals(ctx, {'channel': 'meta'})
    ctx.notes.append('Reach is summed from daily rows. People seen on more than one day count again, '
                     'so true period frequency is higher. A period pull from Meta gives the exact number.')
    return ctx.ok(round(ratio(tot['impressions'], tot['reach'], 'reach'), 4), 'x',
                  {'impressions': int(tot['impressions']), 'reach_daily_sum': int(tot['reach'])}, approximate=True)


@metric('ctr', filters=('channel', 'by'))
def m_ctr(ctx, name, kw):
    by = paid_by(ctx, kw)
    tot, by_channel, groups = paid_totals(ctx, kw, by)
    extra = {'by_channel': {c: (round(v['clicks'] / v['impressions'], 6) if v['impressions'] else None)
                            for c, v in by_channel.items()}}
    if groups is not None:
        extra['groups'] = groups
    ctx.notes.append('All clicks over impressions, as the platforms report them. Link clicks are not split out.')
    return ctx.ok(ratio(tot['clicks'], tot['impressions'], 'impressions'), 'ratio',
                  {'clicks': int(tot['clicks']), 'impressions': int(tot['impressions'])}, **extra)


@metric('mer')
def m_mer(ctx, name, kw):
    _, net = order_totals(ctx, ctx.win)
    tot, by_channel, _ = paid_totals(ctx, {})
    ctx.notes.append('Revenue is net revenue from the store. Marketplace sales and their ad spend are not in it.')
    return ctx.ok(round(ratio(net, tot['spend'], 'marketing spend'), 4), 'x',
                  {'net_revenue': money(net), 'spend': money(tot['spend'])},
                  spend_by_channel={c: v['spend'] for c, v in by_channel.items()})


# ---------------------------------------------------------------- retention

@metric('revenue_by_flow_order_matched')
def m_flow_revenue(ctx, name, kw):
    rows = ctx.rows('flows')
    need(rows, ('flow', 'date', 'matched_order_ids'), 'flows')
    first, last = prep('flows:span', rows, _build_span)
    cover(ctx.win, first, last, 'flows')
    flows_of = {}
    for r in rows:
        for oid in r.get('matched_order_ids') or ():
            flows_of.setdefault(oid, set()).add(r['flow'])
    paid = paid_in_window(ctx, ctx.win)
    total_net = sum(net for _, _, net, _ in paid)
    matched, by_flow, n = 0.0, {}, 0
    for _, _, net, r in paid:
        names = flows_of.get(r.get('id'))
        if not names:
            continue
        matched += net
        n += 1
        for f in names:
            agg = by_flow.setdefault(f, [0, 0.0])
            agg[0] += 1
            agg[1] += net
    ctx.notes.append('Orders are matched to a flow send by customer and time, from orders, not platform attribution. '
                     'An order matched to 2 flows counts in each flow but once in the total.')
    return ctx.ok(money(matched), 'usd', {'matched_orders': n, 'net_revenue_all_orders': money(total_net)},
                  share_of_revenue=round(matched / total_net, 6) if total_net else None,
                  by_flow=[{'flow': f, 'orders': v[0], 'net_revenue': money(v[1])}
                           for f, v in sorted(by_flow.items(), key=lambda kv: -kv[1][1])])


@metric('list_growth')
def m_list_growth(ctx, name, kw):
    rows = ctx.rows('flows')
    need(rows, ('flow', 'message_id', 'channel', 'date', 'sends', 'unsubscribes', 'bounces'), 'flows')
    first, last = prep('flows:span', rows, _build_span)
    cover(ctx.win, first, last, 'flows')
    welcome = sorted({r['message_id'] for r in rows if 'welcome' in str(r['flow']).lower() and r['channel'] == 'email'})
    if not welcome:
        raise Unavailable('no email welcome flow, so new subscribers cannot be counted', fix='klaviyo_lists')
    new = unsub = bounces = 0
    for r in rows:
        if r['channel'] != 'email' or not ctx.win.has(str(r['date'])):
            continue
        if r['message_id'] == welcome[0]:
            new += r['sends'] or 0
        unsub += r['unsubscribes'] or 0
        bounces += r['bounces'] or 0
    for r in ctx.rows('campaign_sends'):
        if r.get('channel') == 'email' and ctx.win.has(str(r.get('sent_at') or '')[:10]):
            unsub += r.get('unsubscribes') or 0
            bounces += r.get('bounces') or 0
    ctx.notes.append(f'New subscribers are sends of the first welcome email ({welcome[0]}), not a list export. Email only.')
    return ctx.ok(new - unsub - bounces, 'count', {'new_subscribers': new, 'unsubscribes': unsub, 'bounces': bounces})


@metric('ltv_180d')
def m_ltv(ctx, name, kw):
    months, customers = mature_cohorts(ctx, 180)
    rows = {m: [0, 0.0] for m in months}
    for lst in customers.values():
        first, _, is_new = lst[0]
        m = first.strftime('%Y-%m')
        if not is_new or m not in rows:
            continue
        rows[m][0] += 1
        rows[m][1] += sum(net for t, net, _ in lst if t <= first + timedelta(days=180))
    n = sum(v[0] for v in rows.values())
    rev = sum(v[1] for v in rows.values())
    if not n:
        raise Unavailable('no first-time customers in the mature cohorts')
    out = ctx.ok(money(rev / n), 'usd', {'net_revenue': money(rev), 'customers': n},
                 cohorts=[{'cohort': m, 'customers': v[0], 'ltv': money(v[1] / v[0]) if v[0] else None} for m, v in rows.items()])
    out['window'] = cohort_window(months, 180)
    return out


# ---------------------------------------------------------------- money

# Brand-supplied costs (contracts/finance-inputs.md). finance.py resolves the row in
# force on a date; these functions only add up orders against it.
MARKETPLACES = ('amazon', 'walmart', 'target_plus', 'tiktok_shop', 'ebay', 'etsy', 'faire')
MARGIN_FIELDS = {
    'gross': ('cogs_landed',),
    'variable': ('cogs_landed', 'packaging', 'shipping_label', 'threepl_pick_pack',
                 'payment_fee_percent', 'payment_fee_fixed'),
    'returns': ('returns_processing',),
    'operating': ('threepl_storage', 'app_fees', 'agency_fees', 'fixed_costs', 'headcount_cost'),
    'cash': ('cash_balance', 'credit_line_available'),
}


def _finance_module():
    from importlib.util import module_from_spec, spec_from_file_location
    from pathlib import Path
    spec = spec_from_file_location('ecomos_finance', Path(__file__).resolve().parent / 'data' / 'finance.py')
    mod = module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


finance = _finance_module()


_FOLDER_TABLES = {}


def brand_folder_table(ctx, name):
    """A brand folder keeps some tables beside its aggregates (finance_inputs.json, S2.4). None when absent."""
    folder = getattr(ctx.data, 'folder', None)
    path = Path(folder) / f'{name}.json' if folder else None
    if path is None or not path.is_file():
        return None
    key = (str(path), path.stat().st_mtime)
    if _FOLDER_TABLES.get(name, (None,))[0] != key:
        doc = json.loads(path.read_text(encoding='utf-8'))
        rows = doc.get('rows') if isinstance(doc, dict) else doc
        _FOLDER_TABLES[name] = (key, rows if isinstance(rows, list) else None)
    rows = _FOLDER_TABLES[name][1]
    if rows is None:
        return None
    if name not in ctx.used:
        ctx.used.append(name)
    return rows


def fin(ctx, *groups):
    """The Finance resolver, once every field the metric lists has at least one row."""
    fields = [f for g in groups for f in MARGIN_FIELDS[g]]
    try:
        rows = ctx.rows('finance_inputs')
    except Unavailable:
        rows = brand_folder_table(ctx, 'finance_inputs')
    if rows is None:
        raise Unavailable('the brand has not supplied its costs yet, so there is nothing to take from revenue',
                          fix=f'finance_inputs.{fields[0]}', waiting_for=fields)
    f = prep('finance_inputs', rows, finance.Finance)
    missing = [x for x in fields if not f.has(x)]
    if missing:
        raise Unavailable(f'finance inputs have no {", ".join(missing)}', fix=f'finance_inputs.{missing[0]}',
                          waiting_for=missing)
    return f


def lines(o):
    return [li for li in o.get('line_items') or () if li.get('sku') and (li.get('qty') or 0) > 0]


def gross(ctx, f, paid):
    """COGS of units sold, per SKU. Any SKU without a landed cost makes the total unavailable.

    A month with no cogs_landed row in force at all (before the brand's cost sheet starts) reads
    unavailable for that month, never as zero cost; the window total is then unavailable too."""
    by_sku, cogs, missing = {}, 0.0, set()
    by_month, covered = {}, {}
    for day, _, net, o in paid:
        month = str(day)[:7]
        if day not in covered:
            covered[day] = bool(f.in_force('cogs_landed', day))
        bm = by_month.setdefault(month, {'month': month, 'net_revenue': 0.0, 'cogs': 0.0, 'costed': True})
        bm['net_revenue'] += net
        if not covered[day]:
            bm['costed'] = False
        items = lines(o)
        if not items:
            raise Unavailable(f'order {o.get("id")} has no line items, so its cost of goods is unknown', fix='shopify')
        for li in items:
            unit = f.value('cogs_landed', day, li['sku'])
            if unit is None or bm['cogs'] is None:
                bm['cogs'] = None
            else:
                bm['cogs'] += unit * li['qty']
            s = by_sku.setdefault(li['sku'], {'sku': li['sku'], 'units': 0, 'revenue': 0.0, 'cogs': 0.0})
            s['units'] += li['qty']
            s['revenue'] += li.get('line_total') if li.get('line_total') is not None else (li.get('price') or 0) * li['qty']
            unit = f.value('cogs_landed', day, li['sku'])
            if unit is None:
                missing.add(li['sku'])
                s['cogs'] = None
            elif s['cogs'] is not None:
                s['cogs'] += unit * li['qty']
                cogs += unit * li['qty']
    skus = []
    for s in sorted(by_sku.values(), key=lambda s: -s['revenue']):
        margin = None if s['cogs'] is None or not s['revenue'] else round((s['revenue'] - s['cogs']) / s['revenue'], 6)
        skus.append({'sku': s['sku'], 'units': s['units'], 'revenue': money(s['revenue']),
                     'cogs': None if s['cogs'] is None else money(s['cogs']), 'margin': margin})
    months = []
    for m in sorted(by_month.values(), key=lambda m: m['month']):
        ok = m['costed'] and m['cogs'] is not None and m['net_revenue']
        months.append({'month': m['month'], 'net_revenue': money(m['net_revenue']),
                       'cogs': money(m['cogs']) if ok else None,
                       'margin': round((m['net_revenue'] - m['cogs']) / m['net_revenue'], 6) if ok else None})
    ctx.margin_by_month = months
    gaps = [m['month'] for m in sorted(by_month.values(), key=lambda m: m['month']) if not m['costed']]
    if gaps:
        span = gaps[0] if len(gaps) == 1 else f'{gaps[0]} to {gaps[-1]}'
        raise Unavailable(f'no cost rows in force for {span}, so margin for those months is unknown',
                          fix='finance_inputs.cogs_landed', partial=True, months_without_costs=gaps, by_month=months,
                          by_sku=skus, waiting_for=['cogs_landed'])
    if missing:
        have = len(by_sku) - len(missing)
        raise Unavailable(f'COGS on {have} of {len(by_sku)} SKUs sold in this window', fix='finance_inputs.cogs_landed',
                          partial=True, missing_skus=sorted(missing), by_sku=skus, waiting_for=['cogs_landed'])
    return cogs, skus


def order_costs(f, day, o):
    """Fulfillment, payment and marketplace fees for one order, from the rows in force on its day."""
    items = lines(o)
    units = sum(li['qty'] for li in items)
    out = {'fulfillment': 0.0, 'payment_fees': 0.0, 'marketplace_fees': 0.0, 'unshipped': 0}
    pack = [f.value('packaging', day, li['sku']) for li in items]
    pack = max([p for p in pack if p is not None], default=None)
    if pack is None:
        pack = f.value('packaging', day)
    if pack is None:
        raise Unavailable(f'no packaging cost in force on {day}', fix='finance_inputs.packaging', waiting_for=['packaging'])
    pick = f.value('threepl_pick_pack', day, unit='usd_per_order')
    if pick is None:
        raise Unavailable(f'no 3PL pick and pack fee in force on {day}', fix='finance_inputs.threepl_pick_pack',
                          waiting_for=['threepl_pick_pack'])
    extra = f.value('threepl_pick_pack', day, unit='usd_per_unit') or 0.0  # optional second row
    ful = o.get('fulfilment') or {}
    if ful.get('carrier'):
        label = f.label(day, ful['carrier'], ful.get('zone'), o.get('ship_state'))
        if label is None:
            raise Unavailable(f'no shipping label cost for {ful["carrier"]} to {ful.get("zone") or o.get("ship_state")} on {day}',
                              fix='finance_inputs.shipping_label', waiting_for=['shipping_label'])
        out['fulfillment'] = pack + pick + extra * max(units - 1, 0) + label['value']
    else:
        out['unshipped'] = 1
    charged = o.get('total')
    if charged is None:
        charged = net_revenue(o) + (o.get('shipping') or 0) + (o.get('tax') or 0)
    channel = o.get('channel') or 'online_store'
    if channel in MARKETPLACES or f.get('marketplace_fee_percent', day, channel):
        pct = f.value('marketplace_fee_percent', day, channel)
        fixed = f.value('marketplace_fee_fixed', day, channel)
        if pct is None or fixed is None:
            raise Unavailable(f'no marketplace fees for {channel} on {day}', fix='finance_inputs.marketplace_fee_percent',
                              waiting_for=['marketplace_fee_percent', 'marketplace_fee_fixed'])
        out['marketplace_fees'] = charged * pct / 100 + fixed
        if f.get('payment_fee_percent', day, channel) is None:
            return out
    pct = f.value('payment_fee_percent', day, channel)
    fixed = f.value('payment_fee_fixed', day, channel)
    if pct is None or fixed is None:
        raise Unavailable(f'no payment fees for the {channel} channel on {day}', fix='finance_inputs.payment_fee_percent',
                          waiting_for=['payment_fee_percent', 'payment_fee_fixed'])
    out['payment_fees'] = charged * pct / 100 + fixed
    return out


def before_marketing(ctx, f):
    """Per order and per channel: net revenue plus shipping charged, minus COGS, fulfillment and fees."""
    paid = paid_in_window(ctx, ctx.win)
    if not paid:
        raise Unavailable('no paid orders in this window')
    cogs, skus = gross(ctx, f, paid)
    tot = {'orders': len(paid), 'net_revenue': 0.0, 'shipping_charged': 0.0, 'cogs': cogs, 'fulfillment': 0.0,
           'payment_fees': 0.0, 'marketplace_fees': 0.0}
    by_channel, first, unshipped = {}, {'orders': 0, 'contribution': 0.0}, 0
    for day, _, net, o in paid:
        c = order_costs(f, day, o)
        unshipped += c['unshipped']
        oc = sum(f.value('cogs_landed', day, li['sku']) * li['qty'] for li in lines(o))
        ship = o.get('shipping') or 0
        contrib = net + ship - oc - c['fulfillment'] - c['payment_fees'] - c['marketplace_fees']
        tot['net_revenue'] += net
        tot['shipping_charged'] += ship
        for k in ('fulfillment', 'payment_fees', 'marketplace_fees'):
            tot[k] += c[k]
        ch = by_channel.setdefault(o.get('channel') or 'online_store', [0, 0.0, 0.0])
        ch[0] += 1
        ch[1] += net
        ch[2] += contrib
        if o.get('customer_is_new'):
            first['orders'] += 1
            first['contribution'] += contrib
    if unshipped:
        ctx.notes.append(f'{unshipped} paid orders have not shipped, so they carry no label, packing or 3PL cost yet.')
    tot['contribution'] = (tot['net_revenue'] + tot['shipping_charged'] - tot['cogs'] - tot['fulfillment']
                           - tot['payment_fees'] - tot['marketplace_fees'])
    channels = [{'channel': c, 'orders': v[0], 'net_revenue': money(v[1]), 'contribution_before_marketing': money(v[2]),
                 'per_order': money(v[2] / v[0]), 'margin_rate': round(v[2] / v[1], 6) if v[1] else None}
                for c, v in sorted(by_channel.items(), key=lambda kv: -kv[1][1])]
    return tot, channels, first, skus


def returns_cost(ctx, f):
    """Returns opened in the window times the processing fee, refunded revenue, and lost chargebacks."""
    rows = ctx.rows('reversed_orders')
    need(rows, ('order_id', 'type', 'opened_at'), 'reversed_orders')
    fee, refunded, chargebacks, n = 0.0, 0.0, 0.0, 0
    for r in rows:
        day = str(r.get('opened_at') or '')[:10]
        if not ctx.win.has(day):
            continue
        if r['type'] == 'return':
            each = f.value('returns_processing', day)
            if each is None:
                raise Unavailable(f'no returns processing fee in force on {day}', fix='finance_inputs.returns_processing',
                                  waiting_for=['returns_processing'])
            n += 1
            fee += each
            if r.get('outcome') == 'refunded':
                refunded += r.get('amount') or 0
        elif r['type'] == 'chargeback' and r.get('outcome') != 'won':
            chargebacks += (r.get('amount') or 0) + (r.get('fee') or 0)
    return {'returns': n, 'returns_processing': fee, 'refunds': refunded, 'chargebacks': chargebacks}


def contribution(ctx, f):
    tot, channels, first, skus = before_marketing(ctx, f)
    ret = returns_cost(ctx, f)
    spend, _, _ = paid_totals(ctx, {})
    value = (tot['contribution'] - ret['returns_processing'] - ret['refunds'] - ret['chargebacks'] - spend['spend'])
    inputs = {k: (v if k == 'orders' else money(v)) for k, v in tot.items() if k != 'contribution'}
    inputs.update({'returns_cost': money(ret['returns_processing'] + ret['refunds']), 'returns': ret['returns'],
                   'chargebacks': money(ret['chargebacks']), 'marketing_spend': money(spend['spend'])})
    return value, inputs, channels, first, spend['spend']


@metric('gross_margin')
def m_gross_margin(ctx, name, kw):
    f = fin(ctx, 'gross')
    paid = paid_in_window(ctx, ctx.win)
    if not paid:
        raise Unavailable('no paid orders in this window')
    cogs, skus = gross(ctx, f, paid)
    net = sum(n for _, _, n, _ in paid)
    ctx.notes.append('Net revenue is after discounts, before shipping charged and refunds. COGS uses the landed cost in force on each order day.')
    return ctx.ok(ratio(net - cogs, net, 'net revenue'), 'ratio', {'net_revenue': money(net), 'cogs': money(cogs)},
                  by_sku=skus, by_month=getattr(ctx, 'margin_by_month', None), target=_target(f, ctx, 'target_gross_margin'))


@metric('gross_profit_per_order')
def m_gross_profit_per_order(ctx, name, kw):
    f = fin(ctx, 'gross')
    paid = paid_in_window(ctx, ctx.win)
    if not paid:
        raise Unavailable('no paid orders in this window')
    cogs, _ = gross(ctx, f, paid)
    net = sum(n for _, _, n, _ in paid)
    return ctx.ok(money((net - cogs) / len(paid)), 'usd', {'net_revenue': money(net), 'cogs': money(cogs), 'orders': len(paid)})


def _target(f, ctx, field):
    v = f.value(field, ctx.win.e)
    return None if v is None else round(v / 100, 6)


@metric('contribution_margin')
def m_contribution_margin(ctx, name, kw):
    f = fin(ctx, 'variable', 'returns')
    value, inputs, channels, _, _ = contribution(ctx, f)
    net = inputs['net_revenue']
    ctx.notes.append('Per channel is before marketing; paid spend is not split by store channel. '
                     'Returns cost is returns opened in the window, not returns of these orders.')
    return ctx.ok(money(value), 'usd', inputs, per_order=money(value / inputs['orders']),
                  margin_rate=round(value / net, 6) if net else None, by_channel=channels,
                  target=_target(f, ctx, 'target_contribution_margin'))


@metric('break_even_roas')
def m_break_even_roas(ctx, name, kw):
    f = fin(ctx, 'variable')
    tot, _, _, _ = before_marketing(ctx, f)
    rate = tot['contribution'] / tot['net_revenue'] if tot['net_revenue'] else 0
    if rate <= 0:
        raise Unavailable('orders lose money before any marketing, so no ROAS breaks even')
    ctx.notes.append('Before marketing and before returns. A platform ROAS under this loses money on the order.')
    return ctx.ok(round(1 / rate, 4), 'x', {'net_revenue': money(tot['net_revenue']),
                                            'contribution_before_marketing': money(tot['contribution'])},
                  margin_before_marketing=round(rate, 6))


@metric('first_order_payback')
def m_first_order_payback(ctx, name, kw):
    f = fin(ctx, 'variable')
    _, _, first, _ = before_marketing(ctx, f)
    if not first['orders']:
        raise Unavailable('no first orders in this window')
    per_first = first['contribution'] / first['orders']
    target = f.value('target_cac', ctx.win.e)
    try:
        spend, _, _ = paid_totals(ctx, {})
        cac, basis = spend['spend'] / first['orders'], 'actual CAC: all paid spend over first orders in the window'
    except Unavailable:
        if target is None:
            raise Unavailable('no paid spend and no target CAC, so the cost to acquire is unknown',
                              fix='finance_inputs.target_cac', waiting_for=['target_cac'])
        cac, basis = target, 'target CAC, since no paid spend is connected'
    if not cac:
        raise Unavailable('cost to acquire is 0, so payback has no base')
    return ctx.ok(round(per_first / cac, 4), 'x', {'contribution_per_first_order': money(per_first),
                                                   'first_orders': first['orders'], 'cac': money(cac)},
                  basis=basis, pays_back=per_first >= cac,
                  vs_target_cac=round(per_first / target, 4) if target else None)


def operating(ctx, f):
    value, inputs, _, _, _ = contribution(ctx, f)
    monthly = {k: f.monthly(k, ctx.win.start, ctx.win.end) for k in MARGIN_FIELDS['operating']}
    gaps = [k for k, v in monthly.items() if v is None]
    if gaps:
        raise Unavailable(f'{", ".join(gaps)} not in force on every day of this window',
                          fix=f'finance_inputs.{gaps[0]}', waiting_for=gaps)
    inputs.update({k: money(v) for k, v in monthly.items()})
    inputs['contribution_margin'] = money(value)
    return value - sum(monthly.values()), inputs


@metric('operating_margin')
def m_operating_margin(ctx, name, kw):
    f = fin(ctx, 'variable', 'returns', 'operating')
    value, inputs = operating(ctx, f)
    ctx.notes.append('Monthly costs are spread evenly over the days of each month.')
    return ctx.ok(money(value), 'usd', inputs, margin_rate=round(value / inputs['net_revenue'], 6))


@metric('cash_runway_weeks')
def m_runway(ctx, name, kw):
    f = fin(ctx, 'cash', 'variable', 'returns', 'operating')
    cash = f.latest('cash_balance', ctx.win.e)
    credit = f.latest('credit_line_available', ctx.win.e)
    if cash is None or credit is None:
        field = 'cash_balance' if cash is None else 'credit_line_available'
        raise Unavailable(f'no {field} dated on or before {ctx.win.e}', fix=f'finance_inputs.{field}', waiting_for=[field])
    value, inputs = operating(ctx, f)
    burn = -value / (ctx.win.days / 7)
    inputs.update({'cash': money(cash['value']), 'cash_as_of': cash['effective_from'],
                   'credit_line_available': money(credit['value']), 'operating_margin': money(value),
                   'weekly_net_burn': money(burn)})
    if burn <= 0:
        raise Unavailable('the brand made money in this window, so there is no burn to run out', not_burning=True,
                          known_inputs=inputs)
    return ctx.ok(round((cash['value'] + credit['value']) / burn, 1), 'weeks', inputs)


@metric('sales_tax_collected')
def m_sales_tax(ctx, name, kw):
    paid = paid_in_window(ctx, ctx.win)
    by = {}
    for _, _, _, r in paid:
        for line in r.get('tax_lines') or ():
            by[line.get('jurisdiction')] = by.get(line.get('jurisdiction'), 0.0) + (line.get('amount') or 0)
    ctx.notes.append('Tax on paid orders placed in the window. Tax on refunds is not netted out.')
    return ctx.ok(money(sum(by.values())), 'usd', {'orders': len(paid)},
                  by_jurisdiction=[{'jurisdiction': j, 'amount': money(v)} for j, v in sorted(by.items(), key=lambda kv: -kv[1])])


# ---------------------------------------------------------------- products (01)

PRODUCT_BY = ('sku', 'line', 'month', 'line_month')


def product_line(title):
    """The line a SKU belongs to: its title without the pack size ("Ankle Sock 4-Pack" is "Ankle Sock")."""
    return re.sub(r'\s+\d+-Pack$', '', str(title or '').strip()) or None


def product_lines(ctx):
    """sku -> line from the products table. Falls back to the SKU's category when the table is missing."""
    try:
        rows = ctx.rows('products')
    except Unavailable:
        ctx.notes.append('No products table, so lines are the SKU category.')
        return None
    return {r['sku']: product_line(r.get('title')) for r in rows if r.get('sku')}


@metric('units', 'product_net_sales', filters=('by',))
def m_product_sales(ctx, name, kw):
    """Units and net sales from products_monthly. Only whole months inside the window count."""
    rows = ctx.rows('products_monthly')
    need(rows, ('month', 'sku', 'units', 'net_sales'), 'products_monthly')
    by = kw.get('by')
    if by and by not in PRODUCT_BY:
        raise ValueError(f'by must be one of {", ".join(PRODUCT_BY)} for {name}')
    months = sorted({r['month'] for r in rows})
    inside = [m for m in months if ctx.win.s <= m + '-01' and month_end(m).isoformat() <= ctx.win.e]
    if not inside:
        raise Unavailable('no whole month of product sales inside this window', fix='shopify')
    lines = product_lines(ctx) if by in ('line', 'line_month') else None
    field = 'units' if name == 'units' else 'net_sales'
    keep = set(inside)
    total, units, net, groups = 0, 0, 0.0, {}
    for r in rows:
        if r['month'] not in keep:
            continue
        if r.get(field) is None:
            raise Unavailable(f'products_monthly has a blank {field} for {r["sku"]} in {r["month"]}', fix='shopify')
        units += r.get('units') or 0
        net += r.get('net_sales') or 0
        total += r[field]
        if not by:
            continue
        line = (lines or {}).get(r['sku']) or r.get('category') if by in ('line', 'line_month') else None
        key = {'sku': (r['sku'],), 'line': (line,), 'month': (r['month'],), 'line_month': (line, r['month'])}[by]
        g = groups.setdefault(key, {'units': 0, 'net_sales': 0.0, 'skus': set()})
        g['units'] += r.get('units') or 0
        g['net_sales'] += r.get('net_sales') or 0
        g['skus'].add(r['sku'])
    if len(inside) < len({m for m in months if ctx.win.s[:7] <= m <= ctx.win.e[:7]}):
        ctx.notes.append('Part months at either end of the window are left out.')
    extra = {'months': inside}
    if by:
        names = {'sku': ('sku',), 'line': ('line',), 'month': ('month',), 'line_month': ('line', 'month')}[by]
        extra['groups'] = [dict(zip(names, k), units=g['units'], net_sales=money(g['net_sales']),
                                skus=sorted(g['skus']), net_per_unit=money(g['net_sales'] / g['units']) if g['units'] else None)
                           for k, g in sorted(groups.items(), key=lambda kv: tuple(str(x) for x in kv[0]))]
    unit = 'count' if name == 'units' else 'usd'
    return ctx.ok(total if name == 'units' else money(total), unit,
                  {'units': units, 'net_sales': money(net), 'months': len(inside)}, **extra)


# ---------------------------------------------------------------- speed

@metric(*SPEED, filters=('page', 'device', 'variant'))
def m_speed(ctx, name, kw):
    rows = ctx.rows('speed_runs')
    col = SPEED[name]
    need(rows, ('page', 'device', 'variant', 'measured_at', col), 'speed_runs')
    page, device, variant = kw.get('page') or 'pdp', kw.get('device') or 'mobile', kw.get('variant') or 'baseline'
    ctx.filters.update(page=page, device=device, variant=variant)
    inside = [r for r in rows if ctx.win.has(str(r['measured_at'])[:10]) and r['device'] == device
              and r['variant'] == variant and r.get(col) is not None]
    by_page = {}
    for r in inside:
        by_page.setdefault(r['page'], []).append(r[col])
    runs = by_page.get(page)
    if not runs:
        raise Unavailable(f'no {variant} speed runs for {page} on {device} in this window', fix='speed_lab')
    notes = {r.get('note') for r in inside if r.get('note')}
    ctx.notes.extend(sorted(notes))
    unit = 'bytes' if name == 'bytes' else 'count' if name == 'requests' else 'ms'
    return ctx.ok(statistics.median(runs), unit, {'runs': len(runs)},
                  by_page={p: statistics.median(v) for p, v in sorted(by_page.items())}, basis='median of runs in the window')


# ---------------------------------------------------------------- entry points

_TABLES = None


def resolve(data, kw):
    """`brand=<name>` swaps the server's sample brand for app/data/brands/<name>/."""
    global _TABLES
    brand = kw.get('brand')
    if not brand:
        return data
    if _TABLES is None:
        path = Path(__file__).resolve().parent / 'data' / 'tables.py'
        spec = importlib.util.spec_from_file_location('ecomos_tables', path)
        _TABLES = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_TABLES)
    return _TABLES.brand_data(str(brand))  # ValueError for an unknown brand


def compute(name, data, **kw):
    data = resolve(data, kw)
    ctx = Ctx(data)
    if name not in METRICS:
        return ctx.unavailable(Unavailable('metrics.py has no function for this metric yet', fix='app/metrics.py'))
    fn, allowed = METRICS[name]
    for key in FILTERS:
        if kw.get(key) and key not in allowed:
            raise ValueError(f'{key} does not apply to {name}')
    try:
        ctx.win = parse_window(data, kw.get('window'), kw.get('end'))
        return fn(ctx, name, kw)
    except Unavailable as exc:
        return ctx.unavailable(exc)


def pipeline(data, names, **kw):
    """Every pipeline metric for 4 trailing windows, oldest first. `data.metric` adds formula and group."""
    source = resolve(data, kw)
    try:
        win = parse_window(source, kw.get('window'), kw.get('end'))
    except Unavailable as exc:
        return {'unavailable': True, 'reason': exc.reason, 'fix': exc.fix, 'metrics': []}
    windows = [win.shift(k) for k in (3, 2, 1, 0)]
    query = {k: v for k, v in kw.items() if k in ('device',) and v}
    brand = {'brand': kw['brand']} if kw.get('brand') else {}
    out = []
    for name in names:
        results = []
        for w in windows:
            q = dict(query, window=f'{w.days}d', end=w.e)
            if query.get('device') and 'device' not in METRICS.get(name, (None, set()))[1]:
                q.pop('device')
            results.append(data.metric(name, **q, **brand))
        out.append({'metric': name, 'unit': next((r.get('unit') for r in results if r.get('unit')), None),
                    'values': [r.get('value') for r in results], 'results': results})
    return {'as_of': (source.brand or {}).get('as_of'), 'window': f'{win.days}d', 'filters': query, **brand,
            'windows': [w.dict() for w in windows], 'metrics': out}
