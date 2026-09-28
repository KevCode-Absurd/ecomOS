"""Screen 19-supply-inventory, round 0: api shape, audit shape and determinism, rules fire on Bombas, wording."""
import importlib.util
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / 'app' / 'screens' / '19-supply-inventory'
SQLITE = ROOT / 'app' / 'data' / 'brands' / 'bombas' / 'data.sqlite'


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


api = _load('supply_inventory_api_test', FOLDER / 'api.py')
audit = api.audit

FIELDS = ['id', 'screen', 'rule_id', 'severity', 'entity', 'evidence', 'sentence', 'capability', 'money_at_stake',
          'confidence', 'brain_refs', 'first_seen', 'last_seen', 'status', 'unavailable']
EVIDENCE = {'metric', 'value', 'unit', 'window', 'ends_on', 'freshness_days', 'baseline', 'baseline_kind', 'source',
            'simulated'}


class Req:
    def __init__(self, path, brand='bombas', method='GET'):
        self.path, self.method, self.data, self._brand = path, method, None, brand

    def arg(self, name, default=None):
        return self._brand if name == 'brand' else default


@unittest.skipUnless(SQLITE.is_file(), 'bombas data.sqlite not built')
class SupplyInventoryScreen(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.overview = api.handle(Req(['overview']))
        cls.findings = audit.run('bombas')

    def test_api_shape(self):
        o = self.overview
        for key in ('brand', 'window', 'tiles', 'insights', 'chart', 'skus', 'findings', 'rules'):
            self.assertIn(key, o)
        self.assertTrue(o['brand']['simulated'])
        self.assertEqual(len(o['tiles']), 3)
        for t in o['tiles'].values():
            for key in ('name', 'plain', 'unit', 'value', 'unavailable_reason'):
                self.assertIn(key, t)
            self.assertIsNotNone(t['value'])
        self.assertEqual(len(o['insights']), 2)
        for i in o['insights']:
            self.assertTrue(i['rule'] and i['sentence'])
        c = o['chart']
        self.assertEqual(len(c['labels']), len(c['cover']))
        self.assertEqual(len(c['labels']), len(c['lands']))
        self.assertEqual(len(o['skus']), 25)

    def test_routes(self):
        self.assertEqual(api.handle(Req(['overview'], method='POST'))[0], 405)
        self.assertEqual(api.handle(Req(['nope']))[0], 404)
        self.assertEqual(api.handle(Req(['overview'], brand='../x'))[0], 400)
        self.assertIn('findings', api.handle(Req(['findings'])))

    def test_audit_shape(self):
        self.assertTrue(self.findings)
        for f in self.findings:
            self.assertEqual(list(f)[:len(FIELDS)], FIELDS)
            self.assertEqual(f['screen'], '19-supply-inventory')
            self.assertEqual(f['id'], f'19-supply-inventory.{f["rule_id"]}.{f["entity"]["id"]}')
            self.assertIn(f['severity'], ('critical', 'high', 'medium', 'low'))
            self.assertIn(f['capability']['autonomy'], ('agent_does', 'founder_gate', 'human_assist'))
            self.assertTrue(0.1 <= f['confidence'] <= 1)
            for e in f['evidence']:
                self.assertEqual(set(e), EVIDENCE)
                self.assertTrue(e['simulated'])
            if f['money_at_stake'] is None:
                self.assertTrue(f['money_reason'])
            else:
                self.assertGreaterEqual(f['money_at_stake']['usd'], 0)
                self.assertTrue(f['money_at_stake']['formula'])
            if f['status'] == 'unavailable':
                self.assertEqual(f['evidence'], [])
                self.assertIsNone(f['money_at_stake'])
                self.assertTrue(f['unavailable']['inputs'] and f['unavailable']['fix'])
        order = [audit.SEVERITY_ORDER[f['severity']] for f in self.findings]
        self.assertEqual(order, sorted(order))

    def test_every_rule_listed_and_emitted(self):
        ids = {r['rule_id'] for r in audit.RULES}
        self.assertEqual(len(ids), 14)
        self.assertTrue({f['rule_id'] for f in self.findings} <= ids)

    def test_deterministic(self):
        self.assertEqual(json.dumps(self.findings, sort_keys=True), json.dumps(audit.run('bombas'), sort_keys=True))

    def test_rules_fire_on_bombas(self):
        fired = {f['rule_id'] for f in self.findings if f['status'] == 'open'}
        # R02 fires on the scale 0.1 build but not on the scale 1.0 rebuild of 28 Sep (FEATURES.md, round 1 job 1).
        for rule in ('SUPPLY-R01', 'SUPPLY-R03'):
            self.assertIn(rule, fired)
        r01 = [f for f in self.findings if f['rule_id'] == 'SUPPLY-R01']
        self.assertTrue(any(f['severity'] == 'critical' for f in r01))
        for f in r01:
            inp = f['money_at_stake']['inputs']
            self.assertAlmostEqual(f['money_at_stake']['usd'],
                                   inp['gap_days'] * inp['units_per_day_14d'] * inp['net_per_unit'],
                                   delta=0.02 * f['money_at_stake']['usd'] + 50)

    def test_unavailable_never_zero(self):
        for f in self.findings:
            if f['status'] == 'unavailable':
                self.assertNotIn(' 0 ', f['sentence'])
        for r in self.overview['skus']:
            if r['lead_days'] is None:
                self.assertIsNone(r['reorder_point'])

    def test_wording(self):
        texts = [f['sentence'] for f in self.findings] + [i['sentence'] for i in self.overview['insights']]
        texts += [t['plain'] for t in self.overview['tiles'].values()]
        for s in texts:
            self.assertNotIn('—', s)
            self.assertNotIn('–', s)
            self.assertIsNone(re.search(r'\b(should|try|consider|GPT)\b|\.env', s), s)
        for f in self.findings:
            self.assertLessEqual(len(f['sentence'].split()), 40, f['sentence'])
        page = (FOLDER / 'screen.js').read_text() + (FOLDER / 'index.html').read_text()
        self.assertNotIn('—', page)


if __name__ == '__main__':
    unittest.main()
