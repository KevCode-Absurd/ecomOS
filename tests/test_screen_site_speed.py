"""Screen 08-site-speed: audit rules in the contract shape, the API, and the fixture read, on Bombas simulated data.

Speed runs and the brain are always present. Money needs session rows from data.sqlite (git-ignored);
those tests skip when it has not been built, and the unavailable path is tested either way.
"""
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / 'app' / 'screens' / '08-site-speed'
BOMBAS_DB = ROOT / 'app' / 'data' / 'brands' / 'bombas' / 'data.sqlite'
AUDIT_KEYS = ['id', 'screen', 'rule_id', 'severity', 'entity', 'evidence', 'sentence', 'capability', 'money_at_stake',
              'confidence', 'brain_refs', 'first_seen', 'last_seen', 'status', 'unavailable']
EVIDENCE_KEYS = {'metric', 'value', 'unit', 'window', 'ends_on', 'freshness_days', 'baseline', 'baseline_kind',
                 'source', 'simulated'}
ENTITY_TYPES = {'brand', 'stage', 'page', 'device', 'sku', 'campaign', 'adset', 'ad', 'flow', 'offer', 'ladder_rung', 'metric'}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


api = load('site_speed_api_test', SCREEN / 'api.py')
audit = api.audit


class Req:
    def __init__(self, path, brand='bombas', method='GET'):
        self.path, self.method, self.data, self._brand = path, method, None, brand

    def arg(self, name, default=None):
        return self._brand if name == 'brand' else default


class SpeedTableTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s = audit.build(audit.tables().brand_data('bombas'), 'bombas')

    def test_fixture_read_through_metrics(self):
        sp = self.s['speed']
        self.assertFalse(sp['unavailable'], sp.get('reason'))
        self.assertTrue(sp['adapted'])
        self.assertEqual(len(sp['rows']), 6)                        # 3 pages x 2 devices
        runs = audit.SpeedData(audit.tables().brand_data('bombas')).table('speed_runs')
        home = sorted(r['lcp_ms'] for r in runs if r['page'] == '/' and r['device'] == 'mobile')
        row = next(r for r in sp['rows'] if r['page'] == '/' and r['device'] == 'mobile')
        self.assertEqual(row['lcp_ms'], home[1])                     # median of 3

    def test_slowest_and_chain(self):
        slow = self.s['slowest']
        self.assertEqual(slow['lcp_ms'], max(r['lcp_ms'] for r in self.s['speed']['rows'] if r['device'] == 'mobile'))
        chain = self.s['chain']
        self.assertEqual([c['step'] for c in chain], list(range(1, len(chain) + 1)))
        saved = sum(c['lcp_ms_saved'] or 0 for c in chain)
        self.assertLessEqual(saved, slow['lcp_ms'] - audit.LCP_TARGET_MS)
        for c in chain:
            self.assertIsNone(c['evidence_run'])                     # nothing measured yet
            self.assertEqual(c['brief']['capability'], 'SITE-C32')
            self.assertIn(c['autonomy'], ('agent_does', 'founder_gate', 'human_assist'))
            if c['expected_ms_saved'] is None:
                self.assertTrue(c['basis'])

    def test_scripts_join_brain(self):
        refs = {s['brain_ref'] for s in self.s['scripts']}
        self.assertIn('bombas.stack.tag_manager', refs)
        for s in self.s['scripts']:
            if s['kb'] is None:
                self.assertIsNone(s['over_budget'])
            self.assertIsNone(s['revenue_link'])


class AuditTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.findings = audit.run('bombas')

    def test_contract_shape(self):
        self.assertTrue(self.findings)
        for f in self.findings:
            self.assertEqual(list(f)[:len(AUDIT_KEYS)], AUDIT_KEYS)
            self.assertEqual(f['id'], f'08-site-speed.{f["rule_id"]}.{f["entity"]["id"]}')
            self.assertIn(f['severity'], ('critical', 'high', 'medium', 'low'))
            self.assertIn(f['entity']['type'], ENTITY_TYPES)
            for e in f['evidence']:
                self.assertEqual(set(e), EVIDENCE_KEYS)
                self.assertTrue(e['simulated'])
            if f['money_at_stake'] is None:
                self.assertTrue(f['money_reason'])
            if f['status'] == 'unavailable':
                self.assertTrue(f['unavailable']['fix'])
                self.assertEqual(f['evidence'], [])
            self.assertLess(len(f['sentence'].split()), 41)
            self.assertNotIn('—', f['sentence'])
            self.assertNotIn('should', f['sentence'])
        order = [(audit.SEVERITY_ORDER[f['severity']], -((f['money_at_stake'] or {}).get('usd') or 0)) for f in self.findings]
        self.assertEqual(order, sorted(order))
        self.assertEqual({r['rule_id'] for r in audit.RULES}, {f['rule_id'] for f in self.findings})

    def test_deterministic(self):
        self.assertEqual(audit.run('bombas'), self.findings)

    def test_non_blocking_script_has_no_money(self):
        for f in self.findings:
            if f['rule_id'] == 'SPEED-R02' and 'after the page shows' in f['sentence']:
                self.assertIsNone(f['money_at_stake'])

    @unittest.skipUnless(BOMBAS_DB.is_file(), 'bombas data.sqlite not built')
    def test_slow_page_and_heavy_script_have_money(self):
        r01 = next(f for f in self.findings if f['rule_id'] == 'SPEED-R01')
        m = r01['money_at_stake']
        i = m['inputs']
        self.assertAlmostEqual(m['usd'], round(i['mobile_sessions_28d'] * i['seconds_over_target'] * i['loss_per_second_assumed']
                                               * i['cvr_overall'] * i['aov'], 2), places=0)
        heavy = [f for f in self.findings if f['rule_id'] == 'SPEED-R02' and f['money_at_stake']]
        self.assertTrue(heavy)
        for f in heavy:
            self.assertLessEqual(f['money_at_stake']['usd'], m['usd'] + 0.01)   # capped at the typical gap

    def test_images_unavailable(self):
        f = next(f for f in self.findings if f['rule_id'] == 'SPEED-R03')
        self.assertEqual(f['status'], 'unavailable')


class ApiTest(unittest.TestCase):
    @unittest.skipUnless(BOMBAS_DB.is_file(), 'bombas data.sqlite not built')
    def test_overview(self):
        d = api.handle(Req(['overview']))
        self.assertTrue(d['brand']['simulated'])
        self.assertEqual(set(d['tiles']), {'lcp', 'weight', 'cost'})
        self.assertEqual(d['tiles']['cost']['value'], d['cost_of_slowness']['usd'])
        self.assertEqual(len(d['insights']), 2)
        self.assertTrue(all(i['rule'] and i['sentence'] for i in d['insights']))
        self.assertEqual(len(d['chart']['labels']), 3)
        self.assertEqual(d['chart']['benchmark'], 2500)
        self.assertTrue(d['film']['before']['frames'] and d['film']['after']['frames'])

    def test_read_only_and_bad_input(self):
        self.assertEqual(api.handle(Req(['overview'], method='POST'))[0], 405)
        self.assertEqual(api.handle(Req(['overview'], brand='../x'))[0], 400)
        self.assertEqual(api.handle(Req(['nope']))[0], 404)

    def test_sample_brand_degrades(self):
        sys.path.insert(0, str(ROOT / 'app'))
        import server
        req = Req(['overview'], brand='sample')
        req.data = server.Data()
        d = api.handle(req)
        self.assertIn('tiles', d)
        self.assertEqual(d['scripts'], [])                           # no brain for the sample brand


if __name__ == '__main__':
    unittest.main()
