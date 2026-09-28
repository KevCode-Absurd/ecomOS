"""Finance and cash API: /api/21-finance-cash/...

  GET overview?brand=bombas   tiles, insights, chart, P&L ladder, margin by SKU, channel lines, cash facts, findings
  GET findings?brand=bombas   the audit findings only (audit.py, contract shape)

Numbers come from audit.py, which reads the brand's aggregates, data.sqlite (rates only), finance_inputs and the
brain. Dollars are at the brand's real size from the aggregates. Insights are rules in `insights()`, each with the
sentence it produces and the capability it maps to. Missing is unavailable, never 0. Default brand is bombas
(simulated). Read-only.
"""
import importlib.util
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _audit():
    spec = importlib.util.spec_from_file_location('finance_cash_audit', HERE / 'audit.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


audit = _audit()
DEFAULT_BRAND = 'bombas'
CHART_MONTHS = 24
MARGIN_GAP_POINTS = 5     # computed gross margin this far over the brain's modelled margin means a cost is missing
OPERATING_FIELDS = ('threepl_storage', 'app_fees', 'agency_fees', 'fixed_costs', 'headcount_cost')
label = audit.month_label


def _tile(name, plain, value, unit, window=None, freshness=None, sources=None, **extra):
    out = {'name': name, 'plain': plain, 'unit': unit, 'value': value, 'window': window, 'freshness': freshness,
           'sources': sources or [], 'unavailable_reason': extra.pop('reason', None), 'fix': extra.pop('fix', None)}
    out.update(extra)
    return out


def _pct(v, d=1):
    return f'{v * 100:.{d}f} percent'


def _usd(v):
    if abs(v) >= 1e6:
        return f'${v / 1e6:,.2f} million'
    return f'${v:,.0f}'


def _model(rd, key):
    rec = rd.record(f'{rd.brand}.economics.{key}') if rd.brand else None
    return (rec or {}).get('value') if isinstance((rec or {}).get('value'), dict) else None


def mer(m):
    return None if not m or not m.get('paid_media') or m.get('store_net_revenue') is None else round(
        m['store_net_revenue'] / m['paid_media'], 4)


# ---------------------------------------------------------------- tiles

def tiles(rd, pnl):
    last = audit.last_full(pnl)
    fresh = rd.ends_on.isoformat()
    if not last:
        na = {'reason': 'no full month in the data', 'fix': 'shopify'}
        return {'gross': _tile('Gross margin', 'Net sales minus product cost.', None, '%', **na),
                'contribution': _tile('Contribution after marketing', 'Online store.', None, '%', **na),
                'mer': _tile('MER', 'Store net sales over paid media.', None, 'x', **na)}
    month = label(last['month'])
    tgm, tcm, tmer = rd.target('target_gross_margin'), rd.target('target_contribution_margin'), rd.target('target_mer')
    if last['gross_margin'] is None:
        t1 = _tile('Gross margin', f'{month}. Net sales minus landed cost of units sold.', None, '%',
                   reason='no landed cost rows in force for this month', fix='finance_inputs.cogs_landed')
    else:
        t1 = _tile('Gross margin', f'{month}, web and retail orders. {_usd(last["store_net_revenue"])} net sales, '
                   f'{_usd(last["cogs"])} landed cost.' + (f' Target {_pct(tgm, 0)}.' if tgm is not None else ''),
                   last['gross_margin'], '%', window=month, freshness=fresh,
                   sources=[{'table': 'products_monthly'}, {'table': 'finance_inputs'}],
                   tone='bad' if tgm is not None and last['gross_margin'] < tgm else None)
    if last['web_cm3_rate'] is None:
        t2 = _tile('Contribution after marketing', f'Online store, {month}.', None, '%',
                   reason='fee, fulfillment, returns or paid media rows are missing for this month',
                   fix='finance_inputs')
    else:
        t2 = _tile('Contribution after marketing', f'Online store, {month}. {_usd(last["web_cm3"])} left from '
                   f'{_usd(last["web_net_revenue"])} after product, fees, fulfillment, returns and all paid media.'
                   + (f' Target {_pct(tcm, 0)}.' if tcm is not None else ''),
                   last['web_cm3_rate'], '%', window=month, freshness=fresh,
                   sources=[{'table': 'channels_monthly'}, {'table': 'orders'}, {'table': 'paid_media_monthly'},
                            {'table': 'finance_inputs'}],
                   tone='bad' if tcm is not None and last['web_cm3_rate'] < tcm else None)
    v = mer(last)
    if v is None:
        t3 = _tile('MER', f'{month}. Store net sales over paid media.', None, 'x', reason='no paid media rows',
                   fix='meta_ads')
    else:
        t3 = _tile('MER', f'{month}. {_usd(last["store_net_revenue"])} store net sales over {_usd(last["paid_media"])} '
                   f'paid media on 6 platforms.' + (f' Target {tmer:.1f}x.' if tmer is not None else ''),
                   v, 'x', window=month, freshness=fresh,
                   sources=[{'table': 'products_monthly'}, {'table': 'paid_media_monthly'}],
                   tone='bad' if tmer is not None and v < tmer else None)
    return {'gross': t1, 'contribution': t2, 'mer': t3}


# ---------------------------------------------------------------- insights

def insights(rd, pnl):
    """The rules behind the insight cards. Each returns the sentence it produces and its capability."""
    out = []
    last = audit.last_full(pnl)
    model = _model(rd, 'gross_margin_model') or {}
    donated = model.get('donated_item_cost_pct')
    modelled = model.get('gross_margin_after_product_and_donation_pct') or next(
        (v for k, v in model.items() if k.startswith('gross_margin')), None)
    rule1 = (f'last full month gross margin against target_gross_margin; when it sits more than {MARGIN_GAP_POINTS} points '
             f'over the brain gross_margin_model and the model has a cost line with no finance_inputs row, name that line')
    if not last or last['gross_margin'] is None:
        out.append({'id': 'margin_basis', 'severity': 'medium', 'capability': 'MONEY-C03', 'autonomy': 'agent_does',
                    'sentence': 'Gross margin is unavailable: no landed cost rows for the last full month.', 'rule': rule1})
    else:
        gm, tgm = last['gross_margin'], rd.target('target_gross_margin')
        s = f'Gross margin was {_pct(gm)} in {label(last["month"])}'
        s += f', against a {_pct(tgm, 0)} target. ' if tgm is not None else '. '
        gap = modelled is not None and gm * 100 - modelled > MARGIN_GAP_POINTS
        if gap and donated:
            s += f'Donated pairs, {donated} percent of net sales in the brain model, carry no cost row.'
        elif modelled is not None:
            s += f'The brain models {modelled} percent.'
        out.append({'id': 'margin_basis', 'severity': 'medium' if gap else 'info',
                    'capability': 'MONEY-C03', 'autonomy': 'agent_does', 'sentence': s.strip(), 'rule': rule1,
                    'evidence': {'gross_margin': gm, 'target': tgm, 'brain_modelled': modelled,
                                 'brain_donated_item_cost_pct': donated,
                                 'brain_ref': f'{rd.brand}.economics.gross_margin_model' if rd.brand else None},
                    'stub': ('Add a landed cost row for donated items, then recompute gross margin and contribution '
                             'for every month. Nothing leaves the app; your choice is logged.') if gap else None})
    rule2 = 'last full month MER (store net sales over all paid media) against target_mer, with the 3 months before it'
    full = [m for m in pnl if m['full'] and mer(m) is not None]
    if not full:
        out.append({'id': 'mer', 'severity': 'medium', 'capability': 'MONEY-C09', 'autonomy': 'agent_does',
                    'sentence': 'MER is unavailable: no paid media rows for a full month.', 'rule': rule2})
    else:
        m, tmer = full[-1], rd.target('target_mer')
        v = mer(m)
        prior = full[-4:-1]
        s = (f'Paid media was {_usd(m["paid_media"])} in {label(m["month"])}, {_pct(m["paid_share"])} of store net sales. '
             f'MER is {v:.2f}x')
        s += f' against a {tmer:.1f}x target' if tmer is not None else ''
        if prior:
            lo, hi = min(mer(p) for p in prior), max(mer(p) for p in prior)
            s += f', and ran {lo:.2f}x to {hi:.2f}x the 3 months before'
        s += '.'
        under = tmer is not None and v < tmer
        out.append({'id': 'mer', 'severity': 'high' if under else 'info', 'capability': 'MONEY-C09',
                    'autonomy': 'agent_does', 'sentence': s, 'rule': rule2,
                    'evidence': {'mer': v, 'target': tmer, 'paid_media': m['paid_media'],
                                 'store_net_revenue': m['store_net_revenue'],
                                 'prior': [{'month': p['month'], 'mer': mer(p)} for p in prior]}})
    return out


# ---------------------------------------------------------------- chart and tables

def chart(pnl):
    if not pnl:
        return {'unavailable': True, 'reason': 'no monthly sales', 'fix': 'shopify'}
    rows = pnl[-CHART_MONTHS:]
    return {'labels': [r['month'] for r in rows], 'gross_margin': [r['gross_margin'] for r in rows],
            'cm3_rate': [r['web_cm3_rate'] for r in rows], 'paid_share': [r['paid_share'] for r in rows],
            'partial': [r['month'] for r in rows if not r['full']],
            'unavailable_months': [r['month'] for r in rows if r['gross_margin'] is None],
            'window': f'{len(rows)} months',
            'basis': ('Gross margin: web and retail orders. Contribution after marketing: online store, with all paid '
                      'media charged to it. Paid share: paid media over store net sales.')}


def ladder(pnl):
    """The P&L ladder for the online store, last full month: each step in dollars and as a share of net revenue."""
    m = audit.last_full(pnl)
    if not m:
        return {'unavailable': True, 'reason': 'no full month in the data'}
    steps = [('Net revenue', 'web_net_revenue', 1, None), ('Product cost (COGS)', 'web_cogs', -1, None),
             ('Payment fees', 'web_payment_fees', -1, None), ('CM1', 'web_cm1', 0, 'after product and payment fees'),
             ('Shipping charged', 'web_shipping', 1, None), ('Fulfillment', 'web_fulfillment', -1, 'packing, pick and pack, label'),
             ('Returns and chargebacks', 'web_returns_cost', -1, 'processing, refunds, chargebacks not won'),
             ('CM2', 'web_cm2', 0, 'after packing and shipping it'), ('Paid media', 'paid_media', -1, 'all 6 platforms'),
             ('CM3', 'web_cm3', 0, 'after the marketing that brought the order in')]
    net = m['web_net_revenue']
    rows = []
    for name, key, sign, note in steps:
        v = m.get(key)
        rows.append({'line': name, 'kind': 'total' if sign == 0 else 'add' if sign > 0 else 'cost',
                     'usd': None if v is None else (v if sign >= 0 else -v),
                     'share': audit.rate(v, net) if v is not None and net else None, 'note': note})
    return {'unavailable': False, 'month': m['month'], 'label': label(m['month']), 'rows': rows,
            'basis': ('Rates from simulated order rows, dollars at full size from the monthly aggregates. Retail (POS) '
                      'orders are left out: ' + (m['pos_reason'] or 'none') + '.')}


def sku_table(rd, pnl):
    m = audit.last_full(pnl)
    if not m:
        return {'unavailable': True, 'reason': 'no full month in the data'}
    rows = audit.sku_margins(rd, m)
    return {'unavailable': False, 'month': m['month'], 'label': label(m['month']), 'rows': rows,
            'per_unit_ops': m['per_unit_ops'], 'paid_per_unit': m['paid_per_unit'],
            'revenue_cost_rate': m['revenue_cost_rate'],
            'basis': ('CM3 per SKU = net sales - COGS - units x (fulfillment and fixed fees less shipping charged, per '
                      'unit + paid media per unit) - net sales x (percent fees + returns cost rate). Worst first.')}


def channel_lines(pnl):
    m = audit.last_full(pnl)
    if not m:
        return []
    return [
        {'line': 'Online store', 'net_revenue': m['web_net_revenue'], 'cm2_rate': m['web_cm2_rate'],
         'cm3_rate': m['web_cm3_rate'], 'note': 'all paid media charged here'},
        {'line': 'Retail stores (POS)', 'net_revenue': m['pos_net_revenue'], 'cm2_rate': m['pos_cm2_rate'],
         'cm3_rate': None, 'note': m['pos_reason']},
        {'line': 'Wholesale sell-in', 'net_revenue': m['wholesale_net_revenue'], 'cm2_rate': None, 'cm3_rate': None,
         'note': 'sell-in has no units by SKU, so product cost is unknown'},
        {'line': 'Marketplaces', 'net_revenue': m['marketplace_net_revenue'], 'cm2_rate': None, 'cm3_rate': None,
         'note': 'no marketplace fee rows in finance inputs'},
    ]


def cash(rd, pnl):
    """Cash facts from finance_inputs. Runway and the 13-week forecast wait for a bank ledger."""
    f, day = rd.fin, rd.ends_on.isoformat()
    if not f:
        return {'unavailable': True, 'reason': 'the brand has not supplied finance inputs', 'fix': 'finance_inputs'}
    bal, credit = f.latest('cash_balance', day), f.latest('credit_line_available', day)
    m = audit.last_full(pnl)
    monthly = None
    if m:
        from datetime import date
        y, mo = map(int, m['month'].split('-'))
        start = date(y, mo, 1)
        end = date(y, mo, m['days'])
        parts = {k: f.monthly(k, start, end) for k in OPERATING_FIELDS}
        monthly = {'month': m['month'], 'parts': {k: audit.r2(v) for k, v in parts.items()},
                   'total': None if any(v is None for v in parts.values()) else audit.r2(sum(parts.values()))}
    return {'unavailable': False, 'cash_balance': None if bal is None else bal['value'],
            'cash_as_of': None if bal is None else bal['effective_from'],
            'credit_line_available': None if credit is None else credit['value'], 'operating_costs': monthly,
            'runway': 'unavailable: retail card fees and a bank ledger are missing, so weekly burn is not known'}


def overview(data, brand):
    ends_on = audit.last_full_day(data, brand)
    rd = audit.Reader(data, brand, ends_on)
    b = rd.source.brand
    head = {'brand': b.get('brand'), 'name': b.get('name'), 'as_of': b.get('as_of'),
            'simulated': bool(b.get('simulated') or b.get('fictional')), 'market': b.get('market')}
    pnl = audit.pnl_months(rd)
    findings = audit.run(brand, {'ends_on': ends_on.isoformat()}, data=data)
    return {'brand': head, 'window': {'ends_on': ends_on.isoformat(), 'days': audit.WINDOW},
            'tiles': tiles(rd, pnl), 'insights': insights(rd, pnl), 'chart': chart(pnl), 'ladder': ladder(pnl),
            'skus': sku_table(rd, pnl), 'channels': channel_lines(pnl), 'cash': cash(rd, pnl),
            'months': pnl[-CHART_MONTHS:], 'findings': findings, 'rules': audit.RULES}


def _brand(req):
    brand = req.arg('brand', DEFAULT_BRAND)
    if brand in ('', 'sample'):
        return None
    if not re.fullmatch(r'[a-z0-9-]{1,40}', brand):
        raise ValueError('brand must be a folder name like bombas')
    return brand


def handle(req):
    if req.method != 'GET':
        return 405, {'error': 'read only'}
    try:
        brand = _brand(req)
        data = None if brand else req.data
        if brand:
            audit.brand_data(brand)  # ValueError for an unknown brand
        if req.path == ['overview']:
            return overview(data, brand)
        if req.path == ['findings']:
            return {'findings': audit.run(brand, None, data=data), 'rules': audit.RULES}
    except ValueError as exc:
        return 400, {'error': str(exc)}
    return 404, {'error': 'not found', 'routes': ['overview', 'findings']}
