"""Tests for app/metrics.py: every contract metric answers, gaps are unavailable (never 0), ratios from totals."""
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


server = load('ecomos_server_m', ROOT / 'app' / 'server.py')
metrics = load('ecomos_metrics_m', ROOT / 'app' / 'metrics.py')
CONTRACT = [m['name'] for m in server.read_metric_contract()]


def order(i, day, device='mobile', subtotal=100.0, discount=None, status='paid', method='card', **extra):
    row = {'id': i, 'created_at': f'{day}T12:00:00Z', 'customer_id': 1000 + i, 'customer_is_new': True,
           'subtotal': subtotal, 'discount': discount, 'shipping': 0.0, 'tax': 0.0, 'tax_lines': [],
           'financial_status': status, 'cancelled_at': None, 'device': device, 'payment_method': method,
           'gateway': 'shopify_payments', 'cogs': 40.0,
           'fulfilment': {'shipped_at': f'{day}T13:00:00Z', 'delivered_at': f'{day}T18:00:00Z'}}
    row.update(extra)
    return row


class FixtureBrand(unittest.TestCase):
    """A tiny brand on disk: 2 days of sessions and orders, as_of 2026-09-02."""

    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())
        brand = json.loads((server.SAMPLE / 'brand.json').read_text(encoding='utf-8'))
        brand['as_of'] = '2026-09-02'
        self.brand = brand
        self.write('brand.json', brand)

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def write(self, name, value):
        path = self.dir / name
        if name.endswith('.csv'):
            path.write_text(value, encoding='utf-8')
        else:
            path.write_text(json.dumps(value), encoding='utf-8')

    def data(self):
        return server.Data(self.dir)

    def sessions(self):
        self.write('sessions.csv',
                   'date,source,medium,device,sessions,product_view,add_to_cart,checkout,purchase\n'
                   '2026-09-01,google,organic,mobile,100,50,10,1,1\n'
                   '2026-09-02,google,organic,mobile,900,450,90,81,2\n'
                   '2026-09-02,google,organic,desktop,100,60,20,10,1\n')


class EmptyBrandTest(FixtureBrand):
    def test_every_metric_unavailable_when_no_tables(self):
        data = self.data()
        for name in CONTRACT:
            result = data.metric(name)
            self.assertIsNone(result['value'], name)
            self.assertTrue(result['unavailable'], name)
            self.assertTrue(result['reason'], name)
            self.assertIn('formula', result)

    def test_missing_table_names_the_connector(self):
        result = self.data().metric('sessions')
        self.assertEqual(result['fix'], 'ga4')
        self.assertIn('sessions', result['reason'])
        self.assertEqual(self.data().metric('spend')['fix'], 'meta_ads')

    def test_pipeline_without_tables(self):
        body = self.data().pipeline()
        self.assertEqual(len(body['windows']), 4)
        for m in body['metrics']:
            self.assertEqual(m['values'], [None] * 4, m['metric'])


class FixtureMetricsTest(FixtureBrand):
    def test_ratio_is_totals_over_totals(self):
        self.sessions()
        result = self.data().metric('checkout_rate', window='2d')
        # (1 + 81 + 10) / (10 + 90 + 20), not the mean of daily rates
        self.assertAlmostEqual(result['value'], 92 / 120, places=6)
        self.assertEqual(result['inputs'], {'numerator': 92, 'denominator': 120})
        self.assertEqual(result['window'], {'label': '2d', 'start': '2026-09-01', 'end': '2026-09-02', 'days': 2})

    def test_device_filter_and_bad_values(self):
        self.sessions()
        data = self.data()
        self.assertAlmostEqual(data.metric('checkout_rate', window='2d', device='mobile')['value'], 82 / 100)
        with self.assertRaises(ValueError):
            data.metric('checkout_rate', device='tablet')
        with self.assertRaises(ValueError):
            data.metric('sessions', window='forever')
        with self.assertRaises(ValueError):
            data.metric('sessions', end='2026-12-01')
        with self.assertRaises(ValueError):
            data.metric('ltv_180d', device='mobile')

    def test_window_outside_the_data_is_unavailable(self):
        self.sessions()
        result = self.data().metric('sessions', window='28d')
        self.assertTrue(result['unavailable'])
        self.assertIsNone(result['value'])
        self.assertIn('covers', result['reason'])

    def test_blank_cells_are_unavailable_not_zero(self):
        self.write('sessions.csv',
                   'date,device,sessions,product_view,add_to_cart,checkout\n'
                   '2026-09-01,mobile,100,50,,1\n2026-09-02,mobile,100,50,10,1\n')
        data = self.data()
        self.assertTrue(data.metric('add_to_cart_rate', window='2d')['unavailable'])
        self.assertEqual(data.metric('add_to_cart_rate', window='1d')['value'], 0.1)

    def test_missing_field_is_unavailable(self):
        self.write('sessions.csv', 'date,device,sessions\n2026-09-02,mobile,5\n')
        result = self.data().metric('checkout_rate', window='1d')
        self.assertTrue(result['unavailable'])
        self.assertIn('field', result['reason'])

    def test_orders_aov_cvr_and_voided(self):
        self.sessions()
        self.write('orders.json', {'captured_at': '2026-09-03T06:00:00Z', 'source': 'shopify_orders', 'rows': [
            order(1, '2026-09-01', subtotal=100.0),
            order(2, '2026-09-02', subtotal=60.0, discount={'code': 'X', 'amount': 10.0}),
            order(3, '2026-09-02', subtotal=500.0, status='voided'),
        ]})
        data = self.data()
        aov = data.metric('aov', window='2d')
        self.assertEqual(aov['value'], 75.0)
        self.assertEqual(aov['inputs'], {'net_revenue': 150.0, 'orders': 2})
        self.assertEqual(aov['freshness']['sources'][0]['captured_at'], '2026-09-03T06:00:00Z')
        self.assertAlmostEqual(data.metric('cvr_overall', window='2d')['value'], 2 / 1100, places=6)

    def test_rto_and_cod_by_market(self):
        self.write('orders.json', [order(1, '2026-09-01', method='cod'), order(2, '2026-09-02', method='cod'),
                                   order(3, '2026-09-02', method='card')])
        self.write('reversed_orders.json', [{'order_id': 2, 'type': 'rto', 'opened_at': '2026-09-02T10:00:00Z'}])
        us = self.data()
        rto = us.metric('rto_rate', window='2d')
        self.assertTrue(rto['unavailable'])
        self.assertTrue(rto['not_applicable'])
        self.assertIsNone(us.metric('payment_method_mix', window='2d')['value']['cod'])
        self.write('brand.json', dict(self.brand, market='IN'))
        india = self.data()
        self.assertEqual(india.metric('rto_rate', window='2d')['value'], 0.5)
        self.assertAlmostEqual(india.metric('payment_method_mix', window='2d')['value']['cod'], 2 / 3, places=5)

    def test_unknown_metric_function(self):
        result = metrics.compute('not_in_code', self.data())
        self.assertTrue(result['unavailable'])
        self.assertEqual(result['fix'], 'app/metrics.py')


class SampleBrandTest(unittest.TestCase):
    """The generated Tallgrass Goods tables: every metric answers, the planted break is found."""

    @classmethod
    def setUpClass(cls):
        cls.data = server.Data()

    def test_every_contract_metric_has_a_function(self):
        self.assertEqual(sorted(n for n in CONTRACT if n not in metrics.METRICS), [])

    def test_every_metric_answers(self):
        expected_gaps = {'return_to_sender_rate', 'rto_rate', 'cash_runway_weeks', 'contribution_margin'}
        for name in CONTRACT:
            r = self.data.metric(name)
            if name in expected_gaps:
                self.assertTrue(r['unavailable'], name)
                self.assertIsNone(r['value'], name)
                self.assertTrue(r['reason'], name)
            else:
                self.assertFalse(r['unavailable'], (name, r.get('reason')))
                self.assertIsNotNone(r['value'], name)
                self.assertTrue(r['freshness']['sources'], name)
        cm = self.data.metric('contribution_margin')
        self.assertEqual(cm['fix'], 'shipping_labels')
        self.assertIn('cogs', cm['known_inputs'])

    def test_mobile_checkout_break(self):
        r = self.data.metric('money_at_stake', device='mobile')
        self.assertEqual(r['break_stage'], 'checkout')
        self.assertGreater(r['value'], 0)
        stage = next(s for s in r['stages'] if s['stage'] == 'checkout')
        self.assertLess(stage['current'], stage['median'])

    def test_pipeline_four_windows_oldest_first(self):
        body = self.data.pipeline(window='28d')
        ends = [w['end'] for w in body['windows']]
        self.assertEqual(ends[-1], self.data.brand['as_of'])
        self.assertEqual(ends, sorted(ends))
        names = [m['metric'] for m in body['metrics']]
        self.assertIn('checkout_rate', names)
        self.assertIn('money_at_stake', names)
        for m in body['metrics']:
            self.assertEqual(len(m['values']), 4)
            self.assertTrue(all(v is not None for v in m['values']), m['metric'])

    def test_paid_by_ad_keeps_shared_and_dynamic_flags(self):
        r = self.data.metric('spend', channel='meta', by='ad', window='90d')
        ads = r['groups']
        self.assertTrue(any(a['shared_creative'] for a in ads))
        self.assertTrue(any(a['dynamic_creative'] for a in ads))
        self.assertAlmostEqual(sum(a['spend'] for a in ads), r['value'], places=1)
        with self.assertRaises(ValueError):
            self.data.metric('spend', by='ad')

    def test_roas_is_period_totals(self):
        r = self.data.metric('period_roas', channel='meta')
        spend = self.data.metric('spend', channel='meta')['value']
        value = self.data.metric('purchase_value', channel='meta')['value']
        self.assertAlmostEqual(r['value'], value / spend, places=3)


if __name__ == '__main__':
    unittest.main()
