"""Screen 23-team-ops: API shape, audit shape and determinism, rules firing on Bombas simulated data.

The Bombas tests skip when app/data/brands/bombas/data.sqlite has not been built.
"""
import importlib.util
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / 'app' / 'screens' / '23-team-ops'
BOMBAS_DB = ROOT / 'app' / 'data' / 'brands' / 'bombas' / 'data.sqlite'
AUDIT_KEYS = ['id', 'screen', 'rule_id', 'severity', 'entity', 'evidence', 'sentence', 'capability', 'money_at_stake',
              'confidence', 'brain_refs', 'first_seen', 'last_seen', 'status', 'unavailable']
EVIDENCE_KEYS = {'metric', 'value', 'unit', 'window', 'ends_on', 'freshness_days', 'baseline', 'baseline_kind',
                 'source', 'simulated'}
ENTITY_TYPES = {'brand', 'stage', 'page', 'device', 'sku', 'campaign', 'adset', 'ad', 'flow', 'offer', 'ladder_rung',
                'metric'}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


api = load('team_ops_api_test', SCREEN / 'api.py')
audit = api.audit


class Req:
    def __init__(self, path, brand='bombas', method='GET', data=None):
        self.path, self.method, self.data, self._brand = path, method, data, brand

    def arg(self, name, default=None):
        return self._brand if name == 'brand' else default


def sentences(obj):
    out = [f['sentence'] for f in obj.get('findings', [])]
    out += [i['sentence'] for i in obj.get('insights', [])]
    out += [t['plain'] for t in obj.get('tiles', {}).values()]
    return out


class RulesTest(unittest.TestCase):
    def test_rules_listed(self):
        ids = [r['rule_id'] for r in audit.RULES]
        self.assertEqual(ids, [f'TEAM-R{n:02d}' for n in range(1, 13)])
        for r in audit.RULES:
            self.assertEqual(set(r), {'rule_id', 'name', 'entity_type', 'inputs', 'capability', 'owner_screen'})
            self.assertEqual(r['owner_screen'], '23-team-ops')
            self.assertIn(r['capability'], audit.AUTONOMY)
            self.assertIn(r['rule_id'], audit.__doc__)

    def test_room_spec_rules_all_present(self):
        """Every insight in the room spec maps to a rule with the spec's capability."""
        spec = {'TEAM-R01': 'MONEY-C33', 'TEAM-R02': 'MONEY-C31', 'TEAM-R03': 'MONEY-C36', 'TEAM-R04': 'LOOP-C10',
                'TEAM-R05': 'MONEY-C38', 'TEAM-R06': 'MONEY-C39', 'TEAM-R07': 'MONEY-C69', 'TEAM-R08': 'MONEY-C78'}
        caps = {r['rule_id']: r['capability'] for r in audit.RULES}
        for rid, cap in spec.items():
            self.assertEqual(caps[rid], cap)

    def test_bad_requests(self):
        self.assertEqual(api.handle(Req(['overview'], method='POST'))[0], 405)
        self.assertEqual(api.handle(Req(['overview'], brand='../x'))[0], 400)
        self.assertEqual(api.handle(Req(['nope']))[0], 404)


@unittest.skipUnless(BOMBAS_DB.is_file(), 'bombas data.sqlite not built')
class BombasTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.overview = api.handle(Req(['overview']))
        cls.findings = audit.run('bombas')

    def test_api_shape(self):
        d = self.overview
        for k in ('brand', 'window', 'tiles', 'insights', 'chart', 'workload', 'cadence', 'team', 'costs', 'decisions',
                  'findings', 'rules'):
            self.assertIn(k, d)
        self.assertTrue(d['brand']['simulated'])
        self.assertGreaterEqual(len(d['tiles']), 3)
        for t in d['tiles'].values():
            for k in ('name', 'plain', 'unit', 'value', 'unavailable_reason'):
                self.assertIn(k, t)
            if t['value'] is None:
                self.assertTrue(t['unavailable_reason'])  # unavailable is named, never 0
        self.assertEqual(len(d['insights']), 2)
        for i in d['insights']:
            self.assertTrue(i['rule'] and i['sentence'])
        c = d['chart']
        self.assertFalse(c.get('unavailable'))
        self.assertEqual(len(c['labels']), len(c['series'][0]['values']))
        self.assertIsNone(d['tiles']['sop_coverage']['value'])

    def test_audit_shape(self):
        self.assertTrue(self.findings)
        for f in self.findings:
            self.assertEqual(list(f)[:len(AUDIT_KEYS)], AUDIT_KEYS)
            self.assertEqual(f['id'], f"23-team-ops.{f['rule_id']}.{f['entity']['id']}")
            self.assertIn(f['severity'], audit.SEVERITY_ORDER)
            self.assertIn(f['entity']['type'], ENTITY_TYPES)
            self.assertIn(f['capability']['autonomy'], ('agent_does', 'founder_gate', 'human_assist'))
            self.assertIn(f['status'], ('open', 'unavailable'))
            self.assertTrue(0.1 <= f['confidence'] <= 1)
            for e in f['evidence']:
                self.assertEqual(set(e), EVIDENCE_KEYS)
                self.assertTrue(e['simulated'])
            if f['money_at_stake'] is None:
                self.assertTrue(f.get('money_reason'))
            else:
                self.assertGreaterEqual(f['money_at_stake']['usd'], 0)
            if f['status'] == 'unavailable':
                self.assertEqual(f['evidence'], [])
                self.assertTrue(f['unavailable']['inputs'] and f['unavailable']['connector'] and f['unavailable']['fix'])
        order = [(audit.SEVERITY_ORDER[f['severity']]) for f in self.findings]
        self.assertEqual(order, sorted(order))

    def test_every_rule_reports_or_is_quiet_for_a_reason(self):
        seen = {f['rule_id'] for f in self.findings}
        for rid in ('TEAM-R01', 'TEAM-R02', 'TEAM-R03', 'TEAM-R04', 'TEAM-R05', 'TEAM-R06', 'TEAM-R07', 'TEAM-R08'):
            self.assertIn(rid, seen)

    def test_rules_fire_on_bombas(self):
        open_ = {f['rule_id']: f for f in self.findings if f['status'] == 'open'}
        self.assertIn('TEAM-R09', open_)
        peak = open_['TEAM-R09']
        self.assertEqual(peak['severity'], 'high')
        ratios = [e['value'] for e in peak['evidence'] if e['metric'] == 'peak_month_tickets_ratio']
        self.assertEqual(len(ratios), 2)
        self.assertTrue(all(r > audit.PEAK_RATIO for r in ratios))
        self.assertTrue(peak['brain_refs'])
        self.assertIn('TEAM-R11', open_)
        r07 = next(f for f in self.findings if f['rule_id'] == 'TEAM-R07')
        self.assertEqual((r07['status'], r07['severity']), ('unavailable', 'critical'))

    def test_deterministic(self):
        a = json.dumps(audit.run('bombas'), sort_keys=True)
        b = json.dumps(audit.run('bombas'), sort_keys=True)
        self.assertEqual(a, b)
        self.assertEqual(a, json.dumps(self.findings, sort_keys=True))

    def test_writing(self):
        for s in sentences(self.overview):
            self.assertNotIn('—', s)
            self.assertNotIn('–', s)
            self.assertNotRegex(s.lower(), r'\b(should|try|consider|gpt)\b|\.env')
        for f in self.findings:
            self.assertLessEqual(len(f['sentence'].split()), 40)
            self.assertLessEqual(len(re.findall(r'[.!?](?:\s|$)', f['sentence'])), 2)

    def test_findings_route(self):
        d = api.handle(Req(['findings']))
        self.assertEqual(json.dumps(d['findings'], sort_keys=True), json.dumps(self.findings, sort_keys=True))


if __name__ == '__main__':
    unittest.main()
