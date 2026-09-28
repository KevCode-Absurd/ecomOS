"""Screen 18-answer-engines: API shape, audit shape and determinism, rules firing on Bombas, and wording.

The Bombas tests skip when app/data/brands/bombas/data.sqlite has not been built.
"""
import importlib.util
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / 'app' / 'screens' / '18-answer-engines'
BOMBAS_DB = ROOT / 'app' / 'data' / 'brands' / 'bombas' / 'data.sqlite'
AUDIT_KEYS = ['id', 'screen', 'rule_id', 'severity', 'entity', 'evidence', 'sentence', 'capability', 'money_at_stake',
              'confidence', 'brain_refs', 'first_seen', 'last_seen', 'status', 'unavailable']
EVIDENCE_KEYS = {'metric', 'value', 'unit', 'window', 'ends_on', 'freshness_days', 'baseline', 'baseline_kind',
                 'source', 'simulated'}
ENTITY_TYPES = {'brand', 'stage', 'page', 'device', 'sku', 'campaign', 'adset', 'ad', 'flow', 'offer', 'ladder_rung',
                'metric'}
DASHES = re.compile('[—–]')


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


api = load('answer_engines_api_test', SCREEN / 'api.py')
audit = api.audit


class Req:
    def __init__(self, path, method='GET', **args):
        self.path, self.method, self.args = path, method, args

    def arg(self, name, default=None):
        return self.args.get(name, default)


class RoutesTest(unittest.TestCase):
    def test_errors(self):
        self.assertEqual(api.handle(Req(['overview'], method='POST'))[0], 405)
        self.assertEqual(api.handle(Req(['overview'], brand='../x'))[0], 400)

    def test_rules_cover_room_insights(self):
        ids = [r['rule_id'] for r in audit.RULES]
        self.assertEqual(ids, [f'AEO-R{n:02d}' for n in range(1, 15)])
        for r in audit.RULES:
            self.assertEqual(set(r), {'rule_id', 'name', 'entity_type', 'inputs', 'capability', 'owner_screen'})
            self.assertIn(r['rule_id'], audit.__doc__)
            self.assertEqual(audit.CAPABILITY[r['rule_id']][0], r['capability'])

    def test_fixture(self):
        fx = audit.prompts()
        self.assertTrue(fx['simulated'])
        for p in fx['prompts']:
            for c in p['needs']:
                self.assertIn(c, audit.FACTS)


@unittest.skipUnless(BOMBAS_DB.is_file(), 'bombas data.sqlite not built')
class BombasTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.o = api.handle(Req(['overview']))
        cls.f = audit.run('bombas')

    def test_api_shape(self):
        o = self.o
        for k in ('brand', 'window', 'tiles', 'engines', 'facts', 'prompts', 'insights', 'chart', 'findings', 'rules'):
            self.assertIn(k, o)
        self.assertTrue(o['brand']['simulated'])
        self.assertEqual(len(o['tiles']), 3)
        self.assertEqual(len(o['insights']), 2)
        for i in o['insights']:
            self.assertTrue(i['rule'] and i['sentence'])
        self.assertFalse(o['chart'].get('unavailable'))
        self.assertEqual(len(o['chart']['labels']), len(o['chart']['series'][0]['values']))
        json.dumps(o)

    def test_unavailable_never_zero(self):
        ai = self.o['tiles']['ai_sessions']
        if ai['value'] is None:
            self.assertTrue(ai['unavailable_reason'])
        for e in self.o['engines']:
            for m in api.ENGINE_METRICS:
                self.assertIsNone(e[m])

    def test_audit_shape(self):
        self.assertTrue(self.f)
        for f in self.f:
            self.assertEqual(list(f)[:len(AUDIT_KEYS)], AUDIT_KEYS)
            self.assertEqual(f['id'], f'{f["screen"]}.{f["rule_id"]}.{f["entity"]["id"]}')
            self.assertIn(f['severity'], audit.SEVERITY_ORDER)
            self.assertIn(f['entity']['type'], ENTITY_TYPES)
            self.assertIn(f['capability']['autonomy'], ('agent_does', 'founder_gate', 'human_assist'))
            self.assertTrue(0.1 <= f['confidence'] <= 1)
            if f['money_at_stake'] is None:
                self.assertTrue(f['money_reason'])
            else:
                self.assertGreaterEqual(f['money_at_stake']['usd'], 0)
            if f['status'] == 'unavailable':
                self.assertEqual(f['evidence'], [])
                self.assertEqual(set(f['unavailable']), {'inputs', 'connector', 'fix'})
            else:
                self.assertIsNone(f['unavailable'])
                for e in f['evidence']:
                    self.assertTrue(EVIDENCE_KEYS <= set(e))
        ids = [f['id'] for f in self.f]
        self.assertEqual(len(ids), len(set(ids)))
        order = [audit.SEVERITY_ORDER[f['severity']] for f in self.f]
        self.assertEqual(order, sorted(order))

    def test_every_rule_reports(self):
        seen = {f['rule_id'] for f in self.f}
        for rid in ('AEO-R01', 'AEO-R02', 'AEO-R04', 'AEO-R05', 'AEO-R06', 'AEO-R07', 'AEO-R08', 'AEO-R10', 'AEO-R11'):
            self.assertIn(rid, seen)

    def test_deterministic(self):
        again = audit.run('bombas')
        self.assertEqual(json.dumps(self.f, sort_keys=True), json.dumps(again, sort_keys=True))

    def test_rules_fire_on_bombas(self):
        open_rules = {f['rule_id'] for f in self.f if f['status'] == 'open'}
        for rid in ('AEO-R09', 'AEO-R12', 'AEO-R13'):
            self.assertIn(rid, open_rules)
        pay = [f for f in self.f if f['id'] == '18-answer-engines.AEO-R12.facts-payment-method']
        self.assertEqual(len(pay), 1)
        self.assertEqual(pay[0]['severity'], 'medium')

    def test_wording(self):
        texts = [f['sentence'] for f in self.f] + [i['sentence'] for i in self.o['insights']]
        texts += [t.get('plain', '') for t in self.o['tiles'].values()]
        for t in texts:
            self.assertFalse(DASHES.search(t), t)
            self.assertNotRegex(t, r'\b(should|try|consider|GPT)\b')
        for f in self.f:
            self.assertLessEqual(len(f['sentence'].split()), 40, f['sentence'])
        page = (SCREEN / 'screen.js').read_text(encoding='utf-8') + (SCREEN / 'index.html').read_text(encoding='utf-8')
        self.assertFalse(DASHES.search(page))
        self.assertIn('simulated', page)


if __name__ == '__main__':
    unittest.main()
