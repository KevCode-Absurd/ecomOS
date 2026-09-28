"""Screen 15-customers-cx: API shape, audit shape and determinism, rules firing on Bombas simulated data.

The Bombas tests skip when app/data/brands/bombas/data.sqlite has not been built.
"""
import importlib.util
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / 'app' / 'screens' / '15-customers-cx'
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


api = load('customers_cx_api_test', SCREEN / 'api.py')
audit = api.audit


class Req:
    def __init__(self, path, brand='bombas', method='GET', data=None):
        self.path, self.method, self.data, self._brand = path, method, data, brand

    def arg(self, name, default=None):
        return self._brand if name == 'brand' else default


def sentences(obj):
    """Every founder-facing string: finding and insight sentences, tile text."""
    out = [f['sentence'] for f in obj.get('findings', [])]
    out += [i['sentence'] for i in obj.get('insights', [])]
    out += [t['plain'] for t in obj.get('tiles', {}).values()]
    return out


@unittest.skipUnless(BOMBAS_DB.is_file(), 'bombas data.sqlite not built')
class BombasTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.overview = api.handle(Req(['overview']))
        cls.findings = audit.run('bombas')

    def test_api_shape(self):
        d = self.overview
        for k in ('brand', 'window', 'tiles', 'insights', 'chart', 'reasons', 'repeat', 'reviews', 'ladders',
                  'findings', 'rules'):
            self.assertIn(k, d)
        self.assertTrue(d['brand']['simulated'])
        self.assertGreaterEqual(len(d['tiles']), 3)
        for t in d['tiles'].values():
            for k in ('name', 'plain', 'unit', 'value', 'unavailable_reason'):
                self.assertIn(k, t)
            if t['value'] is None:
                self.assertTrue(t['unavailable_reason'])
        self.assertEqual(len(d['insights']), 2)
        for i in d['insights']:
            self.assertTrue(i['rule'] and i['sentence'])
        c = d['chart']
        self.assertFalse(c.get('unavailable'))
        self.assertEqual(len(c['labels']), api.CHART_MONTHS)
        for s in c['series']:
            self.assertEqual(len(s['values']), len(c['labels']))
        self.assertEqual(len(d['ladders']), 7)

    def test_rates_from_counts(self):
        r = self.overview['reasons']
        self.assertEqual(sum(x['tickets'] for x in r['rows']), r['tickets'])
        for x in r['rows']:
            self.assertAlmostEqual(x['share'], round(x['tickets'] / r['tickets'], 4))
        for c in self.overview['repeat']['cohorts']:
            self.assertAlmostEqual(c['rate'], round(c['repeat'] / c['customers'], 6))

    def test_audit_shape(self):
        ids = {r['rule_id'] for r in audit.RULES}
        self.assertEqual(len(ids), len(audit.RULES))
        for r in audit.RULES:
            self.assertEqual(set(r) - {'markets'}, {'rule_id', 'name', 'entity_type', 'inputs', 'capability', 'owner_screen'})
        for f in self.findings:
            self.assertEqual(list(f)[:len(AUDIT_KEYS)], AUDIT_KEYS)
            self.assertEqual(f['id'], f'{f["screen"]}.{f["rule_id"]}.{f["entity"]["id"]}')
            self.assertIn(f['rule_id'], ids)
            self.assertIn(f['severity'], ('critical', 'high', 'medium', 'low'))
            self.assertIn(f['entity']['type'], ENTITY_TYPES)
            self.assertIn(f['capability']['autonomy'], ('agent_does', 'founder_gate', 'human_assist'))
            self.assertTrue(0.1 <= f['confidence'] <= 1)
            for e in f['evidence']:
                self.assertEqual(set(e), EVIDENCE_KEYS)
                self.assertTrue(e['simulated'])
            if f['money_at_stake'] is None:
                self.assertTrue(f['money_reason'])
            else:
                self.assertGreaterEqual(f['money_at_stake']['usd'], 0)
            if f['status'] == 'unavailable':
                self.assertEqual(f['evidence'], [])
                self.assertTrue(f['unavailable']['inputs'] and f['unavailable']['fix'])
            else:
                self.assertTrue(f['evidence'])
        order = [audit.SEVERITY_ORDER[f['severity']] for f in self.findings]
        self.assertEqual(order, sorted(order))

    def test_every_spec_rule_accounted(self):
        # CX-R01 to R15 are the room spec's rules; R10 is India only and reads null for a US brand.
        seen = {f['rule_id'] for f in self.findings}
        for n in range(1, 16):
            rid = f'CX-R{n:02d}'
            if rid == 'CX-R10':
                self.assertNotIn(rid, seen)
            elif rid != 'CX-R09':  # R09 reads tickets and emits only when it fires
                self.assertIn(rid, seen)

    def test_rules_fire_on_bombas(self):
        fired = [f for f in self.findings if f['status'] == 'open']
        self.assertTrue(fired)
        self.assertIn('CX-R17', {f['rule_id'] for f in fired})
        for f in fired:
            for num in re.findall(r'\d+(?:\.\d+)?', f['sentence']):
                if num in ('4', '5', '28', '90', '60'):
                    continue  # rule constants: the score line, the window, the target
                vals = [e['value'] for e in f['evidence']] + [e['baseline'] for e in f['evidence']]
                self.assertTrue(any(isinstance(v, (int, float)) and num in (f'{v:.0f}', f'{v * 100:.0f}', f'{v * 100:.1f}')
                                    for v in vals), (num, f['sentence']))

    def test_deterministic(self):
        again = audit.run('bombas')
        self.assertEqual(json.dumps(self.findings, sort_keys=True), json.dumps(again, sort_keys=True))

    def test_no_em_dashes(self):
        for s in sentences(self.overview):
            self.assertNotIn('—', s)
            self.assertNotIn('–', s)
            self.assertNotRegex(s.lower(), r'\b(should|try|consider)\b')

    def test_findings_route(self):
        d = api.handle(Req(['findings']))
        self.assertEqual(len(d['findings']), len(self.findings))
        self.assertEqual(api.handle(Req(['nope']))[0], 404)
        self.assertEqual(api.handle(Req(['overview'], method='POST'))[0], 405)
        self.assertEqual(api.handle(Req(['overview'], brand='../x'))[0], 400)


class SourceTest(unittest.TestCase):
    def test_no_em_dashes_in_source_text(self):
        for name in ('api.py', 'audit.py', 'screen.js', 'index.html'):
            text = (SCREEN / name).read_text(encoding='utf-8')
            self.assertNotIn('—', text, name)


if __name__ == '__main__':
    unittest.main()
