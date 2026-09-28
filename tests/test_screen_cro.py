"""Tests for screen 07-landing-pages-cro on the Bombas simulated set: the session_funnel metric,
audit.py in the contract shape, and the api (summary, findings). data.sqlite is git-ignored; tests
that need session rows run when it exists, and the unavailable path is tested either way."""
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CRO = ROOT / 'app' / 'screens' / '07-landing-pages-cro'
HAS_SQLITE = (ROOT / 'app' / 'data' / 'brands' / 'bombas' / 'data.sqlite').is_file()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


metrics = sys.modules.get('ecomos_metrics') or load('ecomos_metrics', ROOT / 'app' / 'metrics.py')
audit = load('cro_audit', CRO / 'audit.py')
api = load('cro_api_t', CRO / 'api.py')

FIELDS = ['id', 'screen', 'rule_id', 'severity', 'entity', 'evidence', 'sentence', 'capability', 'money_at_stake',
          'confidence', 'brain_refs', 'first_seen', 'last_seen', 'status', 'unavailable']
EVIDENCE = {'metric', 'value', 'unit', 'window', 'ends_on', 'freshness_days', 'baseline', 'baseline_kind', 'source', 'simulated'}


class Req:
    def __init__(self, path, method='GET', query=None):
        self.method, self.path, self.query, self.body = method, path, query or {}, None

    def arg(self, name, default=None):
        v = self.query.get(name)
        return v[0] if v else default


class FakeData:
    """A sample-brand shaped data layer with sessions rows, for the python path of session_funnel."""
    brand = {'as_of': '2026-01-28'}
    sqlite = None

    def __init__(self, rows):
        self.rows = rows

    def table(self, name):
        if name != 'sessions':
            raise KeyError(name)
        return self.rows

    def meta(self, name):
        return {'source': 'test'}


class FunnelMetricTest(unittest.TestCase):
    def rows(self):
        out = []
        for day in range(1, 29):
            for dev, s in (('mobile', 100), ('desktop', 50)):
                out.append({'date': f'2026-01-{day:02d}', 'device': dev, 'channel_group': 'Paid Social', 'landing_page': '/',
                            'sessions': s, 'product_view': s, 'add_to_cart': s // 10, 'checkout': s // 20, 'purchase': s // 50,
                            'sampled': 0, 'thresholded': 0})
        return out

    def test_python_path_totals_and_groups(self):
        r = metrics.compute('session_funnel', FakeData(self.rows()), window='28d', by='device')
        self.assertFalse(r['unavailable'])
        self.assertEqual(r['inputs']['sessions'], 28 * 150)
        mob = next(g for g in r['groups'] if g['device'] == 'mobile')
        self.assertAlmostEqual(mob['add_to_cart_rate'], 0.1)
        self.assertAlmostEqual(mob['conversion_rate'], 0.02)
        self.assertAlmostEqual(r['rates']['conversion_rate'], (28 * 3) / (28 * 150), places=6)

    def test_filters_and_unavailable(self):
        d = FakeData(self.rows())
        r = metrics.compute('session_funnel', d, window='28d', device='desktop')
        self.assertEqual(r['value'], 28 * 50)
        self.assertEqual(r['filters'], {'device': 'desktop'})
        self.assertTrue(metrics.compute('session_funnel', d, window='28d', device='watch')['unavailable'])
        self.assertTrue(metrics.compute('session_funnel', FakeData([]), window='28d')['unavailable'])
        with self.assertRaises(ValueError):
            metrics.compute('session_funnel', d, window='28d', by='colour')
        with self.assertRaises(ValueError):
            metrics.compute('session_funnel', d, window='28d', page="/'; drop table x")

    def test_window_outside_the_data_is_unavailable(self):
        late = [r for r in self.rows() if r['date'] >= '2026-01-10']
        r = metrics.compute('session_funnel', FakeData(late), window='28d')
        self.assertTrue(r['unavailable'])
        self.assertIsNone(r['value'])

    def test_sample_size_rule(self):
        self.assertEqual(api.sample_size(0.05, 0.1), 30400)
        self.assertIsNone(api.sample_size(None, 0.1))


@unittest.skipUnless(HAS_SQLITE, 'data.sqlite is absent; rebuild with app/data/generate.py')
class AuditTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.findings = audit.run('bombas')

    def test_contract_shape(self):
        self.assertTrue(self.findings)
        for f in self.findings:
            for k in FIELDS:
                self.assertIn(k, f)
            self.assertTrue(f['id'].startswith('07-landing-pages-cro.'))
            self.assertIn(f['severity'], ('critical', 'high', 'medium', 'low'))
            self.assertIn(f['status'], ('open', 'unavailable'))
            self.assertLessEqual(len(f['sentence'].split()), 40)
            self.assertNotIn('—', f['sentence'])
            for ev in f['evidence']:
                self.assertEqual(set(ev), EVIDENCE)
                self.assertTrue(ev['simulated'])
            if f['status'] == 'unavailable':
                self.assertEqual(f['evidence'], [])
                self.assertIsNone(f['money_at_stake'])

    def test_mobile_break_has_money(self):
        f = next(f for f in self.findings if f['id'] == '07-landing-pages-cro.CRO-R07.mobile')
        self.assertEqual(f['entity'], {'type': 'device', 'id': 'mobile', 'label': 'Mobile'})
        self.assertEqual(f['capability']['id'], 'SITE-C44')
        stake = f['money_at_stake']
        i = stake['inputs']
        redo = (i['median_rate'] - i['current_rate']) * i['volume_in'] * i['value_per_unit']
        self.assertGreater(stake['usd'], 0)
        self.assertAlmostEqual(stake['usd'], redo, delta=max(1, stake['usd'] * 1e-3))

    def test_message_mismatch_on_captured_lander(self):
        f = next(f for f in self.findings if f['rule_id'] == 'CRO-R02' and f['status'] == 'open')
        self.assertEqual(f['entity']['type'], 'page')
        self.assertIn('COMFORT20', f['sentence'])
        self.assertIn('bombas.offers.first_order_code', f['brain_refs'])
        self.assertIsNotNone(f['money_at_stake'])
        self.assertLess(f['message_match_score'], 1)
        uncaptured = [f for f in self.findings if f['rule_id'] == 'CRO-R02' and f['status'] == 'unavailable']
        for u in uncaptured:
            self.assertEqual(u['entity']['type'], 'page')

    def test_deterministic_and_sorted(self):
        again = audit.run('bombas')
        self.assertEqual(again, self.findings)
        order = [audit.SEVERITY_ORDER[f['severity']] for f in again]
        self.assertEqual(order, sorted(order))


@unittest.skipUnless(HAS_SQLITE, 'data.sqlite is absent; rebuild with app/data/generate.py')
class ApiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = api.handle(Req(['summary']))

    def test_summary_blocks(self):
        d = self.d
        self.assertTrue(d['simulated'])
        self.assertEqual(len(d['tiles']), 3)
        self.assertEqual(len(d['insights']), 2)
        self.assertTrue(all(i['sentence'] for i in d['insights']))
        self.assertEqual({r['device'] for r in d['funnel_device']['rows']}, {'mobile', 'desktop', 'tablet'})
        mob = next(r for r in d['funnel_device']['rows'] if r['device'] == 'mobile')
        self.assertIsNotNone(mob['break_step'])
        self.assertEqual(len(d['chart']['labels']), 12)
        self.assertTrue(d['funnel_source']['rows'])
        self.assertEqual(d['tests']['tests'], [])
        self.assertIn('read_date', [f['key'] for f in d['tests']['fields']])

    def test_registry_and_proof_map(self):
        reg = self.d['registry']['rows']
        home = next(r for r in reg if r['page'] == '/')
        self.assertEqual(home['type'], 'home')
        self.assertTrue(home['in_site_map'])
        # pages with no sessions stay unavailable, never 0
        self.assertTrue(any(r['sessions'] is None for r in reg))
        self.assertFalse(any(r['sessions'] == 0 for r in reg))
        pm = self.d['proof_map']
        self.assertEqual(pm['rungs'], len(pm['rows']))
        self.assertTrue(any(r['status'] == 'no proof' for r in pm['rows']))

    def test_routes(self):
        self.assertIn('findings', api.handle(Req(['findings'])))
        self.assertEqual(api.handle(Req(['nope']))[0], 404)
        self.assertEqual(api.handle(Req(['summary'], query={'window': ['400d']}))[0], 400)


if __name__ == '__main__':
    unittest.main()
