"""The metric contract in code: one function per metric in contracts/metrics.md.

server.py calls `compute(name, data, **query)` for one metric and
`pipeline(data, names, **query)` for the pipeline group with 4 trailing windows.
`data` is server.Data: `data.brand`, `data.table(name)` (KeyError when the table
is missing) and `data.meta(name)` (source and captured_at, for freshness).

Every answer is one of two shapes:
  {value, unit, unavailable: False, window, freshness, inputs, ...}
  {value: None, unavailable: True, reason, fix, window, freshness}
A missing table, field, blank cell or a window the data does not cover gives the
second shape, never 0. Ratios are window totals over window totals. Windows end
on brand.json `as_of` (the last full day) unless `end` asks for an earlier day.

Words used by more than one metric
  paid order   financial_status paid, partially_refunded or refunded, not cancelled
  net revenue  line subtotal minus discounts on paid orders; before tax, shipping
               charged and refunds (refunds are counted as a returns cost)
  day          the date of `created_at` for orders, `date` for daily tables
"""
import re
import statistics
from datetime import date, datetime, timedelta

# Which connector fills a table for a real brand. Shown as `fix` when it is missing.
CONNECTOR = {
    'orders': 'shopify', 'customers': 'shopify', 'reversed_orders': 'shopify',
    'sessions': 'ga4', 'ad_rows': 'meta_ads', 'google_rows': 'google_ads',
    'flows': 'klaviyo', 'campaign_sends': 'klaviyo', 'payouts': 'shopify_payments',
    'speed_runs': 'speed_lab', 'carrier_events': 'carrier_events',
    'cash_balances': 'accounting', 'shipping_labels': 'shipping_labels',
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
    """Paid orders and net revenue in the window."""
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


@metric('chargeback_rate')
def m_chargeback_rate(ctx, name, kw):
    n, _ = order_totals(ctx, ctx.win)
    cbs = [r for r in reversed_rows(ctx, 'chargeback') if ctx.win.has(str(r['opened_at'])[:10])]
    value = ratio(len(cbs), n, 'paid orders')
    return ctx.ok(value, 'ratio', {'numerator': len(cbs), 'denominator': n},
                  benchmark={'max': CHARGEBACK_BENCHMARK, 'over': value > CHARGEBACK_BENCHMARK},
                  basis='chargebacks opened in the window over paid orders placed in the window')


@metric('dispute_win_rate')
def m_dispute_win_rate(ctx, name, kw):
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
    rows = paid_in_window(ctx, ctx.win)
    if not rows:
        raise Unavailable('no paid orders in this window')
    by_method, by_group = {}, {'card': 0, 'wallet': 0, 'bnpl': 0, 'cod': 0}
    for _, _, _, r in rows:
        m = r.get('payment_method') or 'unknown'
        by_method[m] = by_method.get(m, 0) + 1
        g = pay_group(m)
        by_group[g] = by_group.get(g, 0) + 1
    n = len(rows)
    shares = {g: round(c / n, 6) for g, c in by_group.items()}
    if market(ctx) not in COD_MARKETS:
        shares['cod'] = None
    return ctx.ok(shares, 'share', {'orders': n}, counts=by_group,
                  by_method={m: round(c / n, 6) for m, c in sorted(by_method.items(), key=lambda kv: -kv[1])})


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


def paid_totals(ctx, kw, by=None):
    chans = paid_channels(ctx, kw)
    if not chans:
        raise Unavailable('brand.json lists no paid channel')
    if by == 'ad' and chans != ['meta']:
        raise ValueError('by=ad needs channel=meta; Google rows are by campaign and search term')
    tot = {f: 0.0 for f in PAID_UNITS}
    tot['reach'] = None
    by_channel, groups, creatives = {}, {}, {}
    for c in chans:
        spec = PAID[c]
        rows = ctx.rows(spec['table'])
        need(rows, ('date',) + tuple(spec['fields'].values()), spec['table'])
        first, last = prep(spec['table'] + ':span', rows, _build_span)
        cover(ctx.win, first, last, spec['table'])
        ch = {f: 0.0 for f in spec['fields']}
        for r in rows:
            if not ctx.win.has(str(r['date'])):
                continue
            for f, col in spec['fields'].items():
                if r.get(col) is None:
                    raise Unavailable(f'{spec["table"]} has blank {col} cells in this window', fix=CONNECTOR[spec['table']])
                ch[f] += r[col]
            if by:
                key = r.get('ad_id') if by == 'ad' else (r.get('campaign_name') or r.get('campaign'))
                g = groups.setdefault((c, key), {'channel': c, by: key, **{f: 0.0 for f in PAID_UNITS}})
                for f in PAID_UNITS:
                    g[f] += r[spec['fields'][f]]
                if by == 'ad':
                    g['ad_name'] = r.get('ad_name')
                    g['creative_id'] = r.get('creative_id')
                    g['dynamic_creative'] = g.get('dynamic_creative', False) or bool(r.get('is_dynamic_creative'))
                    creatives.setdefault(r.get('creative_id'), set()).add(key)
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
            if by == 'ad':
                g['shared_creative'] = len(creatives.get(g['creative_id'], ())) > 1
            out_groups.append(g)
        out_groups.sort(key=lambda g: -g['spend'])
    return tot, by_channel, out_groups


def paid_by(ctx, kw):
    by = kw.get('by') or None
    if by and by not in ('campaign', 'ad'):
        raise ValueError('by must be campaign or ad')
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

def payout_totals(ctx, gateways):
    """Fees, refunds and chargebacks from settlements, pro rata by days of overlap with the window."""
    rows = ctx.rows('payouts')
    need(rows, ('gateway', 'period_start', 'period_end', 'fees', 'refunds', 'chargebacks'), 'payouts')
    mine = [r for r in rows if r['gateway'] in gateways]
    if not mine:
        raise Unavailable('no payouts for the store gateways', fix='shopify_payments')
    cover(ctx.win, min(r['period_start'] for r in mine), max(r['period_end'] for r in mine), 'payouts')
    tot = {'fees': 0.0, 'refunds': 0.0, 'chargebacks': 0.0}
    for r in mine:
        s, e = date.fromisoformat(r['period_start']), date.fromisoformat(r['period_end'])
        overlap = (min(e, ctx.win.end) - max(s, ctx.win.start)).days + 1
        if overlap <= 0:
            continue
        share = overlap / ((e - s).days + 1)
        tot['fees'] += share * (r['fees'] or 0)
        tot['refunds'] += share * (r['refunds'] or 0)
        tot['chargebacks'] += share * ((r['chargebacks'] or 0) + (r.get('chargeback_fees') or 0))
    return tot


@metric('contribution_margin')
def m_contribution_margin(ctx, name, kw):
    paid = paid_in_window(ctx, ctx.win)
    if not paid:
        raise Unavailable('no paid orders in this window')
    if any(r.get('cogs') is None for _, _, _, r in paid):
        raise Unavailable('some orders have no cost of goods', fix='cost sheet')
    net = sum(n for _, _, n, _ in paid)
    known = {'net_revenue': money(net), 'cogs': money(sum(r['cogs'] for _, _, _, r in paid)),
             'shipping_charged': money(sum(r.get('shipping') or 0 for _, _, _, r in paid))}
    gateways = sorted({r.get('gateway') for _, _, _, r in paid if r.get('gateway')})
    pay = payout_totals(ctx, gateways)
    known.update({'payment_fees': money(pay['fees']), 'returns_cost': money(pay['refunds']),
                  'chargebacks': money(pay['chargebacks'])})
    tot, _, _ = paid_totals(ctx, {})
    known['marketing_spend'] = money(tot['spend'])
    if 'shipping_cost' in paid[0][3]:
        if any(r.get('shipping_cost') is None for _, _, _, r in paid):
            raise Unavailable('some orders have no shipping cost', fix='shipping_labels', known_inputs=known)
        known['shipping_cost'] = money(sum(r['shipping_cost'] for _, _, _, r in paid))
    else:
        try:
            labels = ctx.rows('shipping_labels')
        except Unavailable as exc:
            raise Unavailable('no shipping label cost: orders carry what the customer paid for shipping, '
                              'not what the brand paid the carrier', fix=exc.fix, known_inputs=known)
        need(labels, ('order_id', 'cost'), 'shipping_labels')
        ids = {r['id'] for _, _, _, r in paid}
        known['shipping_cost'] = money(sum(r['cost'] or 0 for r in labels if r['order_id'] in ids))
    value = (net + known['shipping_charged'] - known['cogs'] - known['shipping_cost'] - known['payment_fees']
             - known['returns_cost'] - known['chargebacks'] - known['marketing_spend'])
    ctx.notes.append('Fees, refunds and chargebacks come from settlements, pro rata by days in the window.')
    return ctx.ok(money(value), 'usd', known, margin_rate=round(value / net, 6) if net else None)


@metric('cash_runway_weeks')
def m_runway(ctx, name, kw):
    rows = ctx.rows('cash_balances')
    need(rows, ('date', 'cash'), 'cash_balances')
    inside = sorted((str(r['date']), r['cash']) for r in rows if ctx.win.has(str(r['date'])) and r['cash'] is not None)
    if len(inside) < 2:
        raise Unavailable('fewer than 2 cash balances in this window', fix='accounting')
    weeks = max(ctx.win.days / 7, 1)
    burn = (inside[0][1] - inside[-1][1]) / weeks
    if burn <= 0:
        return ctx.ok(None, 'weeks', {'cash': money(inside[-1][1]), 'weekly_net_burn': money(burn)}, not_burning=True)
    return ctx.ok(round(inside[-1][1] / burn, 1), 'weeks', {'cash': money(inside[-1][1]), 'weekly_net_burn': money(burn)})


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

def compute(name, data, **kw):
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
    try:
        win = parse_window(data, kw.get('window'), kw.get('end'))
    except Unavailable as exc:
        return {'unavailable': True, 'reason': exc.reason, 'fix': exc.fix, 'metrics': []}
    windows = [win.shift(k) for k in (3, 2, 1, 0)]
    query = {k: v for k, v in kw.items() if k in ('device',) and v}
    out = []
    for name in names:
        results = []
        for w in windows:
            q = dict(query, window=f'{w.days}d', end=w.e)
            if query.get('device') and 'device' not in METRICS.get(name, (None, set()))[1]:
                q.pop('device')
            results.append(data.metric(name, **q))
        out.append({'metric': name, 'unit': next((r.get('unit') for r in results if r.get('unit')), None),
                    'values': [r.get('value') for r in results], 'results': results})
    return {'as_of': (data.brand or {}).get('as_of'), 'window': f'{win.days}d', 'filters': query,
            'windows': [w.dict() for w in windows], 'metrics': out}
