"""Screen 04-offers-pricing: audit rules, API shape, and the two metrics it added, on Bombas simulated data.

The metric tests use the server's sample brand (always present). The Bombas tests that need order rows skip
when app/data/brands/bombas/data.sqlite has not been built.
"""
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / 'app' / 'screens' / '04-offers-pricing'
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


api = load('offers_pricing_api_test', SCREEN / 'api.py')
audit = api.audit


class Req:
    def __init__(self, path, brand='bombas', method='GET'):
        self.path, self.method, self.data, self._brand = path, method, None, brand

    def arg(self, name, default=None):
        return self._brand if name == 'brand' else default


class MetricsTest(unittest.TestCase):
    def setUp(self):
        sys.path.insert(0, str(ROOT / 'app'))
        import server
        self.data = server.Data()
        self.m = audit.metrics()

    def test_order_value_distribution_sums(self):
        r = self.m.compute('order_value_distribution', self.data, window='28d')
        self.assertFalse(r['unavailable'], r.get('reason'))
        self.assertEqual(sum(g['orders'] for g in r['groups']), r['value'])
        self.assertAlmostEqual(sum(g['share'] for g in r['groups']), 1, places=4)
        for g in r['groups']:
            self.assertEqual(g['to'] - g['from'], 5)
            self.assertLessEqual(g['paid_shipping_orders'], g['orders'])

    def test_returns_by_reason(self):
        r = self.m.compute('returns_by_reason', self.data, window='28d')
        self.assertFalse(r['unavailable'], r.get('reason'))
        self.assertEqual(sum(g['returns'] for g in r['groups']), r['value'])
        self.assertNotIn('carrier_returned', [g['reason'] for g in r['groups']])

    def test_window_outside_data_is_unavailable(self):
        r = self.m.compute('order_value_distribution', self.data, window='28d', end='2001-01-31')
        self.assertTrue(r['unavailable'])
        self.assertIsNone(r['value'])


class LadderTest(unittest.TestCase):
    def test_proofless(self):
        self.assertTrue(audit.is_proofless(None))
        self.assertTrue(audit.is_proofless('no public proof; open question for the founder'))
        self.assertFalse(audit.is_proofless('The Happiness Guarantee'))

    def test_band_share(self):
        groups = [{'from': 70, 'to': 75, 'share': 0.1}, {'from': 75, 'to': 80, 'share': 0.2}, {'from': 80, 'to': 85, 'share': 0.3}]
        self.assertEqual(audit.band_share(groups, 75, 85), 0.5)
        self.assertEqual(audit.band_share(groups, 65, 75), 0.1)


class BombasTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.findings = audit.run('bombas')

    def test_contract_shape(self):
        self.assertTrue(self.findings)
        for f in self.findings:
            self.assertEqual(list(f)[:len(AUDIT_KEYS)], AUDIT_KEYS)
            self.assertEqual(f['screen'], '04-offers-pricing')
            self.assertEqual(f['id'], f'04-offers-pricing.{f["rule_id"]}.{f["entity"]["id"]}')
            self.assertIn(f['severity'], ('critical', 'high', 'medium', 'low'))
            for e in f['evidence']:
                self.assertEqual(set(e), EVIDENCE_KEYS)
                self.assertTrue(e['simulated'])
            if f['money_at_stake'] is None:
                self.assertTrue(f['money_reason'])
            if f['status'] == 'unavailable':
                self.assertTrue(f['unavailable']['fix'])
            self.assertLess(len(f['sentence'].split()), 41)
            self.assertNotIn('—', f['sentence'])
        order = [audit.SEVERITY_ORDER[f['severity']] for f in self.findings]
        self.assertEqual(order, sorted(order))

    def test_unanswered_rungs(self):
        rungs = [f for f in self.findings if f['rule_id'] == 'OFFER-R04']
        self.assertTrue(rungs)
        for f in rungs:
            self.assertEqual(f['entity']['type'], 'ladder_rung')
            self.assertTrue(f['entity']['id'].endswith('.deal_breaker'))
            self.assertTrue(f['brain_refs'][0].startswith('bombas.objection_ladders.'))
        answered = {r['theme'] for r in audit.ladder_rungs(audit.Reader(None, 'bombas', audit.last_full_day(None, 'bombas')))
                    if r['proof']}
        self.assertFalse({f['entity']['id'].split('.')[0] for f in rungs} & answered)

    def test_sku_margin_joins_finance_keys(self):
        # S2.3c: products use the finance_inputs SKU keys, so every store SKU has a landed cost and R03 stays quiet
        matched, skus, cogs = audit.sku_join(audit.Reader(None, 'bombas', audit.last_full_day(None, 'bombas')))
        self.assertTrue(skus)
        self.assertEqual(matched, skus)
        self.assertFalse([f for f in self.findings if f['rule_id'] == 'OFFER-R03'])

    def test_deterministic(self):
        self.assertEqual(audit.run('bombas'), self.findings)

    @unittest.skipUnless(BOMBAS_DB.is_file(), 'bombas data.sqlite not built')
    def test_threshold_finding_has_money(self):
        f = next(f for f in self.findings if f['rule_id'] == 'OFFER-R01')
        self.assertEqual(f['status'], 'open')
        m = f['money_at_stake']
        i = m['inputs']
        self.assertAlmostEqual(m['usd'], round(round(i['orders_28d'] * i['share_threshold_to_break_even']) * i['average_label'], 2))
        be = next(e for e in f['evidence'] if e['metric'] == 'free_shipping_threshold_breakeven')
        self.assertGreater(be['value'], be['baseline'])

    @unittest.skipUnless(BOMBAS_DB.is_file(), 'bombas data.sqlite not built')
    def test_overview(self):
        code_or_body = api.handle(Req(['overview']))
        d = code_or_body
        self.assertTrue(d['brand']['simulated'])
        self.assertEqual(set(d['tiles']), {'threshold', 'discount', 'multipack'})
        self.assertEqual(len(d['insights']), 2)
        for i in d['insights']:
            self.assertTrue(i['sentence'] and i['rule'])
        self.assertEqual(len(d['chart']['labels']), 24)
        th = d['threshold']
        self.assertFalse(th['unavailable'])
        self.assertEqual(th['suggested'] % 5, 0)
        self.assertGreaterEqual(th['suggested'], th['break_even'])
        self.assertTrue(all(s['source'] for s in d['stack']))
        singles = [r for r in d['ladder']['rows'] if r['pack'] == 1]
        self.assertTrue(all(r['drop_vs_single'] is None for r in singles))

    def test_read_only_and_bad_brand(self):
        self.assertEqual(api.handle(Req(['overview'], method='POST'))[0], 405)
        self.assertEqual(api.handle(Req(['overview'], brand='../x'))[0], 400)
        self.assertEqual(api.handle(Req(['nope']))[0], 404)

    def test_sample_brand_degrades(self):
        req = Req(['overview'], brand='sample')
        sys.path.insert(0, str(ROOT / 'app'))
        import server
        req.data = server.Data()
        d = api.handle(req)
        self.assertIsNone(d['tiles']['threshold']['value'])
        self.assertTrue(d['tiles']['threshold']['unavailable_reason'])


if __name__ == '__main__':
    unittest.main()
