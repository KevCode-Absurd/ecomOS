"""Screen 16-organic-content, round 0: api shape, audit shape and determinism, rules fire on Bombas, wording."""
import importlib.util
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / 'app' / 'screens' / '16-organic-content'
SQLITE = ROOT / 'app' / 'data' / 'brands' / 'bombas' / 'data.sqlite'


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


api = _load('organic_api_test', SCREEN / 'api.py')
audit = api.audit

FINDING_KEYS = ['id', 'screen', 'rule_id', 'severity', 'entity', 'evidence', 'sentence', 'capability', 'money_at_stake',
                'confidence', 'brain_refs', 'first_seen', 'last_seen', 'status', 'unavailable']
EVIDENCE_KEYS = {'metric', 'value', 'unit', 'window', 'ends_on', 'freshness_days', 'baseline', 'baseline_kind', 'source',
                 'simulated'}
EM_DASH = '—'


@unittest.skipUnless(SQLITE.is_file(), 'bombas data.sqlite not built (see app/data/brands/bombas/README.md)')
class OrganicContentScreen(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.overview = api.overview(None, 'bombas')
        cls.findings = audit.run('bombas')

    def test_api_shape(self):
        o = self.overview
        self.assertFalse(o['unavailable'])
        self.assertTrue(o['brand']['simulated'])
        self.assertEqual(set(o['tiles']), {'posts', 'orders_per_1k', 'organic_sessions'})
        for t in o['tiles'].values():
            for k in ('name', 'plain', 'unit', 'value', 'window', 'freshness', 'unavailable_reason', 'sources'):
                self.assertIn(k, t)
            if t['value'] is None:
                self.assertTrue(t['unavailable_reason'])
        self.assertEqual(len(o['insights']), 2)
        for i in o['insights']:
            self.assertTrue(i['rule'] and i['sentence'])
        c = o['chart']
        self.assertTrue(c['labels'])
        for s in c['series']:
            self.assertEqual(len(s['values']), len(c['labels']))
        self.assertEqual(o['rules'], audit.RULES)

    def test_handle_routes(self):
        class Req:
            method, path, data = 'GET', ['findings'], None
            def arg(self, k, d=None):
                return d
        out = api.handle(Req())
        self.assertIn('findings', out)
        Req.path = ['nope']
        self.assertEqual(api.handle(Req())[0], 404)

    def test_audit_shape(self):
        ids = {r['rule_id'] for r in audit.RULES}
        self.assertEqual(ids, {f'ORG-R{n:02d}' for n in range(1, 17)})
        for f in self.findings:
            self.assertEqual([k for k in f if k in FINDING_KEYS], FINDING_KEYS)
            self.assertIn(f['severity'], ('critical', 'high', 'medium', 'low'))
            self.assertIn(f['status'], ('open', 'unavailable'))
            self.assertEqual(f['id'], f'{f["screen"]}.{f["rule_id"]}.{f["entity"]["id"]}')
            self.assertIn(f['capability']['autonomy'], ('agent_does', 'founder_gate', 'human_assist'))
            self.assertTrue(0 <= f['confidence'] <= 1)
            if f['status'] == 'unavailable':
                self.assertEqual(f['evidence'], [])
                self.assertIsNone(f['money_at_stake'])
                self.assertTrue(f['unavailable']['inputs'] and f['unavailable']['fix'])
            for e in f['evidence']:
                self.assertTrue(EVIDENCE_KEYS <= set(e))
                self.assertTrue(e['simulated'])
            if f['money_at_stake'] is None:
                self.assertTrue(f.get('money_reason'))
            else:
                self.assertGreaterEqual(f['money_at_stake']['usd'], 0)
        # every rule with a table the US brand lacks says unavailable, never a zero; IN-only rule is silent
        rules_seen = {f['rule_id'] for f in self.findings}
        self.assertNotIn('ORG-R03', rules_seen)
        for rid in ('ORG-R01', 'ORG-R04', 'ORG-R06', 'ORG-R11', 'ORG-R14', 'ORG-R15'):
            self.assertIn(rid, rules_seen)

    def test_deterministic(self):
        again = audit.run('bombas')
        self.assertEqual(json.dumps(self.findings, sort_keys=True), json.dumps(again, sort_keys=True))

    def test_findings_shape_on_bombas(self):
        # On the scale 1.0 rebuild of 28 Sep every hook sells within 5 percent of the median, so ORG-R16 does not
        # trip (FEATURES.md, round 1 job 1). Round 0 promises the shape: every finding is open or unavailable,
        # open findings carry money computed in code, unavailable ones name inputs and a connector.
        self.assertTrue(self.findings)
        for f in self.findings:
            self.assertIn(f['status'], ('open', 'unavailable'))
            if f['status'] == 'open':
                self.assertTrue(f['money_at_stake'] is None or f['money_at_stake']['usd'] >= 0)
            else:
                self.assertTrue(f['unavailable']['inputs'] and f['unavailable']['connector'])
        hook = [f for f in self.findings if f['rule_id'] == 'ORG-R16' and f['status'] == 'open']
        for h in hook:
            i = h['money_at_stake']['inputs']
            expect = round(max((i['median_orders_per_1k'] - i['hook_orders_per_1k']) / 1000 * i['hook_views'] * i['aov_90d'], 0))
            self.assertEqual(h['money_at_stake']['usd'], expect)

    def test_no_em_dashes(self):
        texts = [f['sentence'] for f in self.findings] + [i['sentence'] for i in self.overview['insights']]
        texts += [i['rule'] for i in self.overview['insights']]
        texts += [t['plain'] for t in self.overview['tiles'].values()]
        for t in texts:
            self.assertNotIn(EM_DASH, t)
            self.assertLessEqual(len(t.split()), 40 if t in texts[:len(self.findings)] else 60)
            self.assertIsNone(re.search(r'\b(should|try|consider)\b', t, re.I) if t in texts[:len(self.findings)] else None)
        for path in (SCREEN / 'screen.js', SCREEN / 'index.html', SCREEN / 'api.py', SCREEN / 'audit.py'):
            self.assertNotIn(EM_DASH, path.read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
