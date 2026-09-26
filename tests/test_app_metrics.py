"""Tests for app/metrics.py: every metric in contracts/metrics.md answers, and missing data is unavailable, never 0."""
import importlib.util
import json
import shutil
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('ecomos_server', ROOT / 'app' / 'server.py')
server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(server)
spec = importlib.util.spec_from_file_location('ecomos_metrics', ROOT / 'app' / 'metrics.py')
metrics = importlib.util.module_from_spec(spec)
spec.loader.exec_module(metrics)

END = '2026-09-24'            # the last full day every test pins
FIRST = date(2025, 12, 1)     # first day of fixture data
DAYS = (date(2026, 9, 25) - FIRST).days  # rows up to and including END
METHODS = ['card', 'shop_pay', 'paypal', 'affirm', 'card', 'apple_pay']


def iso(d):
    return d.isoformat()


def in_window(day, days=28, end=END):
    end = date.fromisoformat(end)
    return end - timedelta(days=days - 1) <= day <= end


def build_fixtures(folder):
    """Small tables shaped like contracts/data-sources.md, with a drop in add to cart in the current window."""
    folder.mkdir(parents=True, exist_ok=True)
    shutil.copy(server.SAMPLE / 'brand.json', folder / 'brand.json')
    sessions, orders, reversed_orders, ad_rows, google_rows, list_growth = [], [], [], [], [], []
    for d in range(DAYS):
        day = FIRST + timedelta(days=d)
        atc = 12 if in_window(day) else 20
        sessions.append({'date': iso(day), 'sessions': 100, 'product_view': 60, 'add_to_cart': atc, 'checkout': 10, 'purchase': 6})
        for j in range(5):
            oid = f'o{d}-{j}'
            tax = {'OH': 5} if j % 2 == 0 else [{'jurisdiction': 'CA', 'amount': 5}]
            orders.append({'id': oid, 'created_at': iso(day) + 'T10:00:00Z', 'customer_id': f'c{d * 5 + j}',
                           'status': 'delivered', 'delivered_at': iso(day + timedelta(days=3)), 'total': 91.95,
                           'shipping': 6.95, 'tax': tax, 'refund': 0, 'payment_method': METHODS[j],
                           'line_items': [{'sku': 's1', 'qty': 1}, {'sku': 's2', 'qty': 1}],
                           'shipping_cost': 8, 'payment_fee': 2.5})
            if j == 1 and d % 10 == 0:
                reversed_orders.append({'order_id': oid, 'type': 'return', 'reason': 'size', 'amount': 80,
                                        'opened_at': iso(day + timedelta(days=5)), 'closed_at': iso(day + timedelta(days=12)), 'outcome': 'refunded'})
        if d >= 30:  # one repeat order a day from the customer who bought 30 days ago
            orders.append({'id': f'r{d}', 'created_at': iso(day) + 'T12:00:00Z', 'customer_id': f'c{(d - 30) * 5}',
                           'status': 'delivered', 'delivered_at': iso(day + timedelta(days=3)), 'total': 91.95,
                           'shipping': 6.95, 'tax': {'OH': 5}, 'refund': 0, 'payment_method': METHODS[5],
                           'line_items': [{'sku': 's1', 'qty': 1}, {'sku': 's2', 'qty': 1}], 'shipping_cost': 8, 'payment_fee': 2.5})
        for ad in ('ad1', 'ad2'):
            ad_rows.append({'date': iso(day), 'campaign': 'prospecting', 'ad_set': 'broad', 'ad': ad, 'creative_id': 'cr1',
                            'spend': 100, 'impressions': 10000, 'reach': 5000, 'clicks': 200, 'purchases': 2, 'purchase_value': 300})
        google_rows.append({'date': iso(day), 'campaign': 'brand', 'search_term': 'tallgrass', 'spend': 20, 'impressions': 1000,
                            'clicks': 50, 'conversions': 1, 'conversion_value': 100})
        list_growth.append({'date': iso(day), 'list': 'main', 'new_subscribers': 10, 'unsubscribes': 2, 'bounces': 1})
    # 3 cancelled orders in the current window: never counted
    for k in range(3):
        orders.append({'id': f'x{k}', 'created_at': '2026-09-1%dT09:00:00Z' % k, 'customer_id': f'g{k}', 'status': 'cancelled',
                       'total': 91.95, 'shipping': 6.95, 'tax': {'OH': 5}, 'refund': 0, 'payment_method': 'card',
                       'line_items': [{'sku': 's1', 'qty': 1}], 'shipping_cost': 0, 'payment_fee': 0})
    # chargebacks: 2 opened in the 90 day window, 1 before it; 3 closed in the window
    reversed_orders += [
        {'order_id': 'o250-0', 'type': 'chargeback', 'reason': 'fraud', 'amount': 91.95, 'opened_at': '2026-08-20', 'closed_at': '2026-09-10', 'outcome': 'won'},
        {'order_id': 'o260-0', 'type': 'chargeback', 'reason': 'not received', 'amount': 91.95, 'opened_at': '2026-09-01', 'closed_at': '2026-09-20', 'outcome': 'lost'},
        {'order_id': 'o100-0', 'type': 'chargeback', 'reason': 'fraud', 'amount': 91.95, 'opened_at': '2026-03-20', 'closed_at': '2026-07-01', 'outcome': 'won'},
        {'order_id': 'o280-2', 'type': 'return_to_sender', 'reason': 'bad address', 'amount': 0, 'opened_at': '2026-09-12', 'closed_at': None, 'outcome': None},
    ]
    flows = [
        {'flow': 'welcome', 'message': 'w1', 'date': '2026-09-02', 'sends': 500, 'opens': 200, 'clicks': 40, 'unsubscribes': 2, 'order_ids': ['o290-0', 'o291-1', 'o292-2', 'o10-0']},
        {'flow': 'winback', 'message': 'wb1', 'date': '2026-09-05', 'sends': 300, 'opens': 90, 'clicks': 12, 'unsubscribes': 1, 'order_ids': ['o292-2', 'o293-3']},
    ]
    products = [{'sku': 's1', 'title': 'Skillet', 'type': 'cast iron', 'price': 60, 'cost': 30},
                {'sku': 's2', 'title': 'Napkins', 'type': 'linen', 'price': 32, 'cost': 30},
                {'sku': 's3', 'title': 'Board', 'type': 'wooden boards', 'price': 48, 'cost': None}]
    payouts = [{'period_end': iso(date(2026, 9, 24) - timedelta(days=7 * i)), 'gross': 5000, 'fees': 150, 'refunds': 80, 'chargebacks': 0, 'net': 4770} for i in range(20)]
    cash = [{'date': iso(date(2026, 9, 24) - timedelta(days=7 * (12 - i))), 'balance': 100000 - 1000 * i} for i in range(13)]
    speed_runs = []
    for variant, base in (('baseline', 3000), ('fixed', 2000)):
        for run, bump in enumerate((0, 200, 100), start=1):
            speed_runs.append({'page': 'home', 'variant': variant, 'run': run, 'load_ms': base + bump, 'lcp_ms': base - 800 + bump,
                               'fcp_ms': 900 + bump, 'bytes': 2_400_000, 'requests': 80})
    for name, rows in {'sessions': sessions, 'orders': orders, 'reversed_orders': reversed_orders, 'ad_rows': ad_rows,
                       'google_rows': google_rows, 'list_growth': list_growth, 'flows': flows, 'products': products,
                       'payouts': payouts, 'cash': cash, 'speed_runs': speed_runs}.items():
        (folder / (name + '.json')).write_text(json.dumps({'brand': 'Tallgrass Goods', 'source': 'test', 'rows': rows}), encoding='utf-8')
    return {'orders': orders, 'reversed_orders': reversed_orders}


class FixtureMetricsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp())
        cls.fixture = build_fixtures(cls.tmp / 'sample')
        cls.data = server.Data(cls.tmp / 'sample')

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def metric(self, name, **kw):
        kw.setdefault('end', END)
        out = self.data.metric(name, **kw)
        self.assertEqual(out['metric'], name)
        self.assertIn('formula', out)
        return out

    def ok(self, name, **kw):
        out = self.metric(name, **kw)
        self.assertFalse(out.get('unavailable'), out.get('reason'))
        self.assertIsNotNone(out['value'], name)
        self.assertIn('window', out)
        self.assertIn('freshness', out)
        return out

    def orders_in(self, days, end=END):
        return [o for o in self.fixture['orders'] if o['status'] != 'cancelled' and in_window(date.fromisoformat(o['created_at'][:10]), days, end)]

    # ---- pipeline
    def test_sessions_and_rates(self):
        s = self.ok('sessions')
        self.assertEqual(s['value'], 2800)
        self.assertEqual(s['window'], {'label': 'current', 'days': 28, 'start': '2026-08-28', 'end': '2026-09-24'})
        self.assertEqual(s['freshness']['last_full_day'], END)
        self.assertEqual(s['freshness']['tables'], ['sessions'])
        self.assertAlmostEqual(self.ok('product_view_rate')['value'], 0.6)
        self.assertAlmostEqual(self.ok('add_to_cart_rate')['value'], 0.12)
        self.assertAlmostEqual(self.ok('add_to_cart_rate', window='7d', end='2026-06-30')['value'], 0.2)
        self.assertAlmostEqual(self.ok('checkout_rate')['value'], 10 / 12)
        cvr = self.ok('cvr_overall')
        self.assertEqual(cvr['inputs'], {'numerator': 28 * 6, 'denominator': 2800})
        self.assertAlmostEqual(cvr['value'], 168 / 2800)
        self.assertEqual(sorted(cvr['freshness']['tables']), ['orders', 'sessions'])

    def test_aov_from_totals(self):
        aov = self.ok('aov')
        self.assertAlmostEqual(aov['value'], 80.0, places=6)  # total minus shipping, tax and refund
        self.assertEqual(aov['inputs']['denominator'], 168)
        self.assertEqual(aov['unit'], '$')

    def test_repeat_rate_cohorts(self):
        out = self.ok('repeat_rate_90d')
        self.assertAlmostEqual(out['value'], 0.2)
        self.assertEqual(out['window']['label'], 'cohorts')
        self.assertEqual([c['cohort'] for c in out['breakdown']], ['2025-12', '2026-01', '2026-02', '2026-03', '2026-04', '2026-05'])
        self.assertTrue(all(abs(c['rate'] - 0.2) < 1e-9 for c in out['breakdown']))

    def test_money_at_stake_names_the_break(self):
        out = self.ok('money_at_stake')
        self.assertEqual(out['stage'], 'add_to_cart_rate')
        stage = next(r for r in out['breakdown'] if r['stage'] == 'add_to_cart_rate')
        self.assertAlmostEqual(stage['prior_median'], 0.2)
        self.assertAlmostEqual(stage['gap'], 0.08)
        self.assertEqual(stage['volume'], 2800)
        self.assertAlmostEqual(stage['unit_value'], 168 * 80 / 336)
        self.assertAlmostEqual(out['value'], 0.08 * 2800 * 168 * 80 / 336)
        self.assertEqual(len(out['windows']), 4)
        self.assertEqual(out['windows'][1]['end'], '2026-08-27')
        checkout = next(r for r in out['breakdown'] if r['stage'] == 'checkout_rate')
        self.assertEqual(checkout['stake'], 0.0, 'a stage above its median has nothing at stake')

    def test_pipeline_endpoint(self):
        out = self.data.pipeline(window='28d', windows='4', end=END)
        self.assertEqual(out['windows'], 4)
        atc = out['metrics']['add_to_cart_rate']
        self.assertEqual(len(atc['values']), 4)
        self.assertAlmostEqual(atc['values'][0], 0.12)
        self.assertAlmostEqual(atc['values'][1], 0.2)
        self.assertAlmostEqual(atc['prior_median'], 0.2)
        self.assertAlmostEqual(atc['delta'], -0.4)
        self.assertEqual(atc['windows'][2]['label'], 'prior 2')
        self.assertEqual(atc['windows'][3]['start'], '2026-06-05')
        self.assertEqual(out['break']['stage'], 'add_to_cart_rate')
        self.assertGreater(out['break']['money_at_stake'], 0)
        self.assertEqual(len(out['metrics']['repeat_rate_90d']['values']), 1, 'cohort metrics have no trailing windows')
        self.assertEqual(set(out['metrics']), {'sessions', 'product_view_rate', 'add_to_cart_rate', 'checkout_rate', 'cvr_overall', 'aov', 'repeat_rate_90d'})

    # ---- reversed orders
    def test_reversed_orders(self):
        delivered = self.orders_in(90)
        self.assertEqual(len(delivered), 90 * 6)
        returned = {r['order_id'] for r in self.fixture['reversed_orders'] if r['type'] == 'return'}
        expected = sum(1 for o in delivered if o['id'] in returned)
        rr = self.ok('return_rate')
        self.assertEqual(rr['window']['days'], 90)
        self.assertEqual(rr['inputs'], {'numerator': expected, 'denominator': 540})
        cb = self.ok('chargeback_rate')
        self.assertEqual(cb['inputs'], {'numerator': 2, 'denominator': 540})
        self.assertEqual(cb['benchmark']['max'], 0.009)
        dw = self.ok('dispute_win_rate')
        self.assertEqual(dw['inputs'], {'numerator': 2, 'denominator': 3})
        rts = self.ok('return_to_sender_rate')
        self.assertEqual(rts['inputs'], {'numerator': 1, 'denominator': 540})

    def test_rto_is_null_for_us(self):
        out = self.metric('rto_rate')
        self.assertIsNone(out['value'])
        self.assertFalse(out['unavailable'])
        self.assertTrue(out['not_applicable'])
        self.assertIn('cash on delivery', out['reason'])

    def test_payment_method_mix(self):
        out = self.ok('payment_method_mix')
        n = 540
        self.assertAlmostEqual(out['value']['card'], 180 / n)
        self.assertAlmostEqual(out['value']['wallet'], 270 / n)
        self.assertAlmostEqual(out['value']['bnpl'], 90 / n)
        self.assertIsNone(out['value']['cod'], 'cod share reads null for a US brand')
        self.assertEqual(out['breakdown'][0]['method'], 'card')

    # ---- paid
    def test_paid_sums_and_ratios(self):
        spend = self.ok('spend')
        self.assertEqual(spend['value'], 6160)
        self.assertEqual(spend['breakdown']['meta']['spend'], 5600)
        self.assertEqual(spend['breakdown']['google']['spend'], 560)
        self.assertEqual(self.ok('spend', source='meta')['value'], 5600)
        self.assertEqual(self.ok('impressions')['value'], 2 * 10000 * 28 + 1000 * 28)
        self.assertEqual(self.ok('clicks')['value'], 400 * 28 + 50 * 28)
        self.assertEqual(self.ok('purchases')['value'], 4 * 28 + 28)
        self.assertEqual(self.ok('purchase_value')['value'], 600 * 28 + 100 * 28)
        self.assertAlmostEqual(self.ok('period_roas')['value'], 19600 / 6160)
        self.assertAlmostEqual(self.ok('cpa')['value'], 44.0)
        freq = self.ok('frequency')
        self.assertAlmostEqual(freq['value'], 2.0)
        self.assertIn('reach', freq['note'])
        mer = self.ok('mer')
        self.assertAlmostEqual(mer['value'], 168 * 80 / 6160)
        self.assertTrue(self.metric('spend', source='tiktok')['unavailable'])

    # ---- retention
    def test_flow_revenue_list_growth_ltv(self):
        flow = self.ok('revenue_by_flow_order_matched')
        self.assertAlmostEqual(flow['value'], 4 * 80)
        by = {r['flow']: r for r in flow['breakdown']}
        self.assertEqual(by['welcome']['orders'], 3, 'o10-0 is outside the window')
        self.assertEqual(by['winback']['orders'], 2)
        self.assertEqual(self.ok('list_growth')['value'], 28 * 7)
        ltv = self.ok('ltv_180d')
        self.assertAlmostEqual(ltv['value'], 96.0)
        self.assertEqual([c['cohort'] for c in ltv['breakdown']], ['2025-09', '2025-10', '2025-11', '2025-12', '2026-01', '2026-02'])
        self.assertEqual(ltv['breakdown'][0]['customers'], 0)
        self.assertIsNone(ltv['breakdown'][0]['ltv'])

    # ---- money
    def test_contribution_margin(self):
        out = self.ok('contribution_margin')
        orders = self.orders_in(28)
        returns = sum(r['amount'] for r in self.fixture['reversed_orders'] if r['type'] == 'return' and in_window(date.fromisoformat(r['opened_at']), 28))
        expected = 168 * 80 - 168 * 60 - 168 * 8 - 168 * 2.5 - returns - 6160
        self.assertEqual(len(orders), 168)
        self.assertAlmostEqual(out['value'], expected, places=6)
        self.assertEqual(out['inputs']['returns_cost'], returns)
        self.assertEqual(out['sources']['payment_fees'], 'orders.payment_fee')
        self.assertEqual(out['sources']['marketing'], 'meta, google')

    def test_cash_runway_and_sales_tax(self):
        cash = self.ok('cash_runway_weeks')
        self.assertAlmostEqual(cash['value'], 88.0)
        self.assertEqual(cash['inputs']['weekly_net_burn'], 1000.0)
        tax = self.ok('sales_tax_collected')
        self.assertAlmostEqual(tax['value'], 168 * 5)
        self.assertEqual({r['jurisdiction'] for r in tax['breakdown']}, {'OH', 'CA'})

    # ---- speed
    def test_speed_from_lab_runs(self):
        out = self.ok('fully_loaded_ms')
        self.assertEqual(out['value'], 3100)
        self.assertEqual(out['inputs']['variant'], 'baseline')
        self.assertEqual(self.ok('fully_loaded_ms', variant='fixed')['value'], 2100)
        self.assertEqual(self.ok('lcp_ms')['value'], 2300)
        self.assertEqual(self.ok('fcp_ms')['value'], 1000)
        self.assertEqual(self.ok('bytes')['value'], 2_400_000)
        self.assertEqual(self.ok('requests')['value'], 80)
        self.assertTrue(self.metric('lcp_ms', page='pdp')['unavailable'])

    # ---- every metric answers
    def test_every_contract_metric_answers(self):
        for row in self.data.contract():
            out = self.metric(row['name'])
            if row['name'] == 'rto_rate':
                continue
            self.assertFalse(out.get('unavailable'), f"{row['name']}: {out.get('reason')}")
            self.assertIsNotNone(out['value'], row['name'])
        names = {m['name'] for m in server.read_metric_contract()}
        self.assertTrue(names <= set(metrics.METRICS), names - set(metrics.METRICS))

    def test_shopify_shaped_orders_and_missing_legs(self):
        """Orders with nested fulfilment, cancelled_at and financial_status; a reversal leg with no rows is unavailable."""
        tmp = Path(tempfile.mkdtemp())
        try:
            sample = tmp / 'sample'
            sample.mkdir()
            shutil.copy(server.SAMPLE / 'brand.json', sample / 'brand.json')
            orders = []
            for i in range(10):
                o = {'id': i, 'created_at': f'2026-09-{10 + i:02d}T10:00:00Z', 'customer_id': f'c{i}', 'total': 100, 'shipping': 0,
                     'tax': 5, 'refund': {'amount': 10} if i == 0 else None, 'payment_method': 'card', 'gateway': 'shopify_payments',
                     'financial_status': 'paid', 'fulfillment_status': 'delivered', 'cancelled_at': None,
                     'fulfilment': {'carrier': 'UPS', 'shipped_at': f'2026-09-{11 + i:02d}', 'delivered_at': f'2026-09-{13 + i:02d}'},
                     'line_items': [{'sku': 's1', 'qty': 2}], 'cogs': 40}
                if i == 9:
                    o.update(financial_status='voided', fulfillment_status=None, cancelled_at='2026-09-19T11:00:00Z', fulfilment={})
                if i == 8:
                    o.update(fulfillment_status='in_transit', fulfilment={'carrier': 'USPS', 'shipped_at': '2026-09-19', 'delivered_at': None})
                orders.append(o)
            (sample / 'orders.json').write_text(json.dumps({'rows': orders}), encoding='utf-8')
            (sample / 'reversed_orders.json').write_text(json.dumps({'rows': [
                {'order_id': 1, 'type': 'return', 'amount': 100, 'opened_at': '2026-09-15', 'closed_at': '2026-09-20', 'outcome': 'refunded'},
                {'order_id': 2, 'type': 'chargeback', 'amount': 100, 'opened_at': '2026-09-16', 'closed_at': None, 'outcome': 'open'}]}), encoding='utf-8')
            (sample / 'payouts.json').write_text(json.dumps({'rows': [
                {'gateway': 'shopify_payments', 'period_end': '2026-09-21', 'gross': 900, 'fees': 27},
                {'gateway': 'amazon', 'period_end': '2026-09-21', 'gross': 5000, 'fees': 1100}]}), encoding='utf-8')
            (sample / 'ad_rows.json').write_text(json.dumps([{'date': '2026-09-20', 'spend': 50, 'impressions': 1, 'reach': 1, 'clicks': 1, 'purchases': 1, 'purchase_value': 100}]), encoding='utf-8')
            data = server.Data(sample)
            aov = data.metric('aov', end='2026-09-24')
            self.assertEqual(aov['inputs']['denominator'], 9, 'the voided order with cancelled_at is not counted')
            self.assertAlmostEqual(aov['value'], (9 * 95 - 10) / 9)
            rr = data.metric('return_rate', end='2026-09-24')
            self.assertEqual(rr['inputs'], {'numerator': 1, 'denominator': 8}, 'delivered from the nested fulfilment object')
            cb = data.metric('chargeback_rate', end='2026-09-24')
            self.assertEqual(cb['inputs'], {'numerator': 1, 'denominator': 9})
            self.assertTrue(data.metric('dispute_win_rate', end='2026-09-24')['unavailable'], 'an open dispute is not closed')
            rts = data.metric('return_to_sender_rate', end='2026-09-24')
            self.assertTrue(rts['unavailable'], 'no return_to_sender rows at all means the feed is not connected, not 0')
            self.assertIsNone(rts['value'])
            self.assertIn('carrier', rts['fix'])
            cm = data.metric('contribution_margin', end='2026-09-24')
            self.assertFalse(cm['unavailable'], cm.get('reason'))
            self.assertEqual(cm['inputs']['cogs'], 360, 'cogs from the order, not the product sheet')
            self.assertEqual(cm['inputs']['payment_fees'], 27, 'Amazon settlements are not payment fees for Shopify orders')
            self.assertEqual(cm['inputs']['shipping'], 9 * 9.5)
            self.assertEqual(cm['sources']['cogs'], 'orders.cogs')
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_list_growth_without_a_list_table(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            sample = tmp / 'sample'
            sample.mkdir()
            shutil.copy(server.SAMPLE / 'brand.json', sample / 'brand.json')
            (sample / 'flows.json').write_text(json.dumps({'rows': [
                {'flow': 'Welcome Series', 'message_id': 'F-01-M1', 'date': '2026-09-20', 'sends': 30, 'unsubscribes': 1, 'bounces': 4, 'matched_order_ids': []},
                {'flow': 'Welcome Series', 'message_id': 'F-01-M2', 'date': '2026-09-22', 'sends': 25, 'unsubscribes': 2, 'bounces': 3, 'matched_order_ids': []},
                {'flow': 'Winback', 'message_id': 'F-05-M1', 'date': '2026-09-21', 'sends': 100, 'unsubscribes': 3, 'bounces': 9, 'matched_order_ids': []}]}), encoding='utf-8')
            (sample / 'campaign_sends.json').write_text(json.dumps({'rows': [
                {'campaign': 'Labor Day', 'sent_at': '2026-09-19T14:00:00Z', 'sends': 500, 'unsubscribes': 4, 'bounces': 20, 'matched_order_ids': []}]}), encoding='utf-8')
            data = server.Data(sample)
            out = data.metric('list_growth', end='2026-09-24')
            self.assertFalse(out['unavailable'], out.get('reason'))
            self.assertEqual(out['value'], 30 - (1 + 2 + 3 + 4))
            self.assertEqual(out['inputs']['new_subscribers'], 30)
            self.assertIsNone(out['inputs']['bounces'])
            self.assertIn('not a list export', out['note'])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_compound_stage_ranks_after_the_stage_that_explains_it(self):
        out = self.ok('money_at_stake')
        rows = {r['stage']: r for r in out['breakdown']}
        self.assertTrue(rows['cvr_overall']['compound'])
        self.assertFalse(rows['checkout_rate']['compound'])
        self.assertIn('compound', out['inputs']['ranking'])

    def test_bad_window(self):
        out = self.metric('sessions', window='abc')
        self.assertTrue(out['unavailable'])
        self.assertIsNone(out['value'])

    def test_trailing_offset(self):
        prior = metrics.compute('sessions', self.data, offset=2, end=END)
        self.assertEqual(prior['window'], {'label': 'prior 2', 'days': 28, 'start': '2026-07-03', 'end': '2026-07-30'})
        self.assertEqual(prior['value'], 2800)


class MissingDataTest(unittest.TestCase):
    """The real sample folder has only brand.json until the generator runs: everything is unavailable, nothing is 0."""

    def test_real_sample_brand_never_zero(self):
        data = server.Data(server.SAMPLE)
        present = {t['name'] for t in data.tables()}
        for row in data.contract():
            out = data.metric(row['name'])
            if row['name'] == 'rto_rate':
                self.assertTrue(out['not_applicable'])
                continue
            if present:
                self.assertNotEqual(out['value'], 0, row['name'])
                continue
            self.assertTrue(out['unavailable'], row['name'])
            self.assertIsNone(out['value'], row['name'])
            self.assertTrue(out['reason'], row['name'])
            self.assertTrue(out['fix'], row['name'])
        pipe = data.pipeline()
        self.assertIn('metrics', pipe)
        if not present:
            self.assertIsNone(pipe['break'])
            self.assertTrue(pipe['money_at_stake']['unavailable'])

    def test_generated_sample_brand(self):
        """With session 2's tables on disk, every metric answers except the legs the generator says are not connected."""
        data = server.Data(server.SAMPLE)
        if 'orders' not in {t['name'] for t in data.tables()}:
            self.skipTest('generate.py has not run')
        not_connected = {'return_to_sender_rate', 'cash_runway_weeks'}
        for row in data.contract():
            out = data.metric(row['name'])
            if row['name'] == 'rto_rate':
                self.assertTrue(out['not_applicable'])
            elif row['name'] in not_connected:
                self.assertTrue(out['unavailable'], row['name'])
                self.assertTrue(out['fix'], row['name'])
            else:
                self.assertFalse(out.get('unavailable'), f"{row['name']}: {out.get('reason')}")
                self.assertIsNotNone(out['value'], row['name'])
        pipe = data.pipeline()
        self.assertEqual(pipe['break']['stage'], 'checkout_rate', 'the planted story: mobile checkout broke on 2026-08-21')
        self.assertGreater(pipe['break']['money_at_stake'], 0)
        self.assertEqual(pipe['metrics']['sessions']['window']['end'], data.brand['as_of'])
        self.assertLess(data.metric('chargeback_rate')['value'], 0.009)

    def test_missing_table_names_the_connector(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            sample = tmp / 'sample'
            sample.mkdir()
            shutil.copy(server.SAMPLE / 'brand.json', sample / 'brand.json')
            (sample / 'sessions.json').write_text(json.dumps([{'date': '2026-09-01', 'product_view': 1, 'add_to_cart': 1, 'checkout': 0, 'purchase': 0},
                                                              {'date': '2026-09-02', 'product_view': 0, 'add_to_cart': 0}]), encoding='utf-8')
            data = server.Data(sample)
            out = data.metric('cvr_overall', end='2026-09-02')
            self.assertTrue(out['unavailable'])
            self.assertIsNone(out['value'])
            self.assertEqual(out['fix_table'], 'orders')
            self.assertIn('Shopify', out['fix'])
            self.assertEqual(out['window']['end'], '2026-09-02')
            atc = data.metric('add_to_cart_rate', end='2026-09-02')
            self.assertEqual(atc['value'], 0.5)
            self.assertEqual(atc['inputs'], {'numerator': 1, 'denominator': 2})
            self.assertEqual(atc['coverage'], ['sessions covers 2026-09-01 to 2026-09-02, not the whole window'])
            (sample / 'orders.json').write_text(json.dumps([{'id': 'o1', 'total': 80}]), encoding='utf-8')
            undated = data.metric('cvr_overall', end='2026-09-02')
            self.assertTrue(undated['unavailable'], 'orders without created_at are unknown, not 0')
            self.assertIn('created_at', undated['reason'])
            checkout = data.metric('checkout_rate', end='2026-09-02')
            self.assertEqual(checkout['value'], 0.0, 'no checkouts is a real reading: 0 of 1 add to cart')
            self.assertEqual(checkout['inputs'], {'numerator': 0, 'denominator': 1})
            empty = data.metric('sessions', end='2025-01-01')
            self.assertTrue(empty['unavailable'])
            self.assertIn('no sessions', empty['reason'])
            self.assertTrue(data.metric('spend')['unavailable'])
            self.assertEqual(data.metric('spend')['fix_connector'], 'Meta Ads')
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    unittest.main()
