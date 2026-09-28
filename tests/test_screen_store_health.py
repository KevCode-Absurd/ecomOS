"""Screen 06-store-health: checklist, audit rules, API shape, and the metrics it added, on Bombas simulated data.

The metric tests use the server's sample brand (always present). The Bombas tests skip when
app/data/brands/bombas/data.sqlite has not been built.
"""
import importlib.util
import sys
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / 'app' / 'screens' / '06-store-health'
BOMBAS_DB = ROOT / 'app' / 'data' / 'brands' / 'bombas' / 'data.sqlite'
AUDIT_KEYS = ['id', 'screen', 'rule_id', 'severity', 'entity', 'evidence', 'sentence', 'capability', 'money_at_stake',
              'confidence', 'brain_refs', 'first_seen', 'last_seen', 'status', 'unavailable']
EVIDENCE_KEYS = {'metric', 'value', 'unit', 'window', 'ends_on', 'freshness_days', 'baseline', 'baseline_kind',
                 'source', 'simulated'}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


api = load('store_health_api_test', SCREEN / 'api.py')
audit = api.audit


class Req:
    def __init__(self, path, brand='bombas', method='GET'):
        self.path, self.method, self.data, self._brand = path, method, None, brand

    def arg(self, name, default=None):
        return self._brand if name == 'brand' else default


class MetricsTest(unittest.TestCase):
    """The new metrics on the sample brand (rows in memory)."""

    def setUp(self):
        sys.path.insert(0, str(ROOT / 'app'))
        import server
        self.data = server.Data()
        self.m = audit.metrics()

    def test_reversed_by_month_rates(self):
        r = self.m.compute('reversed_by_month', self.data, window='90d')
        if r['unavailable']:
            self.skipTest(r['reason'])
        for g in r['groups']:
            self.assertAlmostEqual(g['returns_per_1000'], round(g['returns'] / g['paid_orders'] * 1000, 3))

    def test_open_disputes_aged_within_total(self):
        r = self.m.compute('open_disputes', self.data, window='28d')
        if r['unavailable']:
            self.skipTest(r['reason'])
        self.assertLessEqual(r['aged_count'], r['value'])

    def test_rto_null_for_us(self):
        r = self.m.compute('rto_rate', self.data, window='28d')
        self.assertTrue(r['unavailable'])
        self.assertIsNone(r['value'])


@unittest.skipUnless(BOMBAS_DB.is_file(), 'bombas data.sqlite not built')
class BombasTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = api.handle(Req(['overview']))
        cls.rd = audit.Reader(None, 'bombas', date.fromisoformat(cls.d['window']['ends_on']))

    def test_shape(self):
        d = self.d
        self.assertTrue(d['brand']['simulated'])
        self.assertEqual(set(d['tiles']), {'checklist', 'chargebacks', 'returns', 'uptime'})
        self.assertEqual(len(d['insights']), 2)
        self.assertEqual(len(d['chart']['labels']), 24)
        self.assertEqual(len(d['chart']['labels']), len(set(d['chart']['labels'])))

    def test_checklist_items(self):
        for i in self.d['checklist']:
            self.assertIn(i['status'], ('pass', 'fail', 'unavailable'))
            self.assertTrue(i['source'] and i['source'].get('ref'), i['key'])
            self.assertIn(i['capability'], audit.AUTONOMY)
            if i['status'] == 'unavailable' and i['source']['kind'] == 'table':
                self.assertTrue(i['connector'] or i['detail'])

    def test_uptime_unavailable_with_connector(self):
        t = self.d['tiles']['uptime']
        self.assertIsNone(t['value'])
        self.assertTrue(t['fix'])
        self.assertTrue(self.d['uptime']['unavailable'])

    def test_cod_legs_null_for_us(self):
        r = self.d['reversed']
        self.assertFalse(r['cod_market'])
        self.assertIsNone(r['return_to_origin'])
        self.assertNotIn('cod', self.d['payments']['groups'])

    def test_payment_shares_sum(self):
        p = self.d['payments']
        self.assertAlmostEqual(sum(r['share'] for r in p['rows']), 1, places=3)

    def test_chargeback_rate_matches_inputs(self):
        cb = self.d['reversed']['chargebacks']
        self.assertAlmostEqual(cb['rate'], cb['chargebacks'] / cb['paid_orders'], places=5)
        self.assertEqual(cb['benchmark'], 0.009)

    def test_findings_contract_shape(self):
        fs = self.d['findings']
        self.assertTrue(fs)
        for f in fs:
            self.assertEqual(list(f)[:len(AUDIT_KEYS)], AUDIT_KEYS)
            self.assertTrue(f['id'].startswith('06-store-health.' + f['rule_id'] + '.'))
            self.assertIn(f['severity'], audit.SEVERITY_ORDER)
            for e in f['evidence']:
                self.assertEqual(set(e), EVIDENCE_KEYS)
            if f['money_at_stake'] is None:
                self.assertTrue(f['money_reason'])
            else:
                self.assertGreaterEqual(f['money_at_stake']['usd'], 0)
            self.assertLessEqual(len(f['sentence'].split()), 40)
        order = [(audit.SEVERITY_ORDER[f['severity']]) for f in fs]
        self.assertEqual(order, sorted(order))

    def test_each_checklist_fail_has_a_finding(self):
        ids = {f['entity']['id'] for f in self.d['findings'] if f['rule_id'] in ('STORE-R01', 'STORE-R02')}
        for i in self.d['checklist']:
            if i['status'] == 'fail':
                self.assertIn('chargeback_rate' if i['key'] == 'chargeback_rate' else i['key'], ids | {'chargeback_rate'})
                if i['key'] != 'chargeback_rate':
                    self.assertIn(i['key'], ids)

    def test_dispute_money_redoes(self):
        f = next((f for f in self.d['findings'] if f['entity']['id'] == 'disputes_answered'), None)
        if f is None:
            self.skipTest('no aged disputes in this build')
        m = f['money_at_stake']
        self.assertAlmostEqual(m['usd'], round(m['inputs']['aged_disputed_amount'] * m['inputs']['scale'], 2), places=2)

    def test_monitor_unavailable_finding(self):
        f = next(f for f in self.d['findings'] if f['rule_id'] == 'STORE-R04')
        self.assertEqual(f['status'], 'unavailable')
        self.assertEqual(f['evidence'], [])
        self.assertTrue(f['unavailable']['connector'])

    def test_chargeback_rule_fires_over_benchmark(self):
        real = audit.chargeback_now
        try:
            audit.chargeback_now = lambda rd: {'unavailable': False, 'rate': 0.012, 'chargebacks': 120,
                                               'paid_orders': 10000, 'amount': 9600.0, 'avg_amount': 80.0,
                                               'by_reason': [], 'own': 0.003, 'benchmark': 0.009,
                                               'over_benchmark': True, 'over_own': True, 'fires': True}
            fs = audit.rule_chargeback(self.rd)
        finally:
            audit.chargeback_now = real
        self.assertEqual(len(fs), 1)
        m = fs[0]['money_at_stake']
        self.assertAlmostEqual(m['usd'], round((0.012 - 0.003) * 10000 * 80.0 * m['inputs']['scale'], 2), places=2)

    def test_deterministic(self):
        self.assertEqual(audit.run('bombas'), audit.run('bombas'))

    def test_rules_listed(self):
        self.assertEqual({r['rule_id'] for r in audit.RULES}, {'STORE-R01', 'STORE-R02', 'STORE-R04'})

    def test_read_only(self):
        self.assertEqual(api.handle(Req(['overview'], method='POST'))[0], 405)
        self.assertEqual(api.handle(Req(['overview'], brand='../x'))[0], 400)


if __name__ == '__main__':
    unittest.main()
