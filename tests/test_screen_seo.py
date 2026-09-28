"""Tests for screen 17-seo on the Bombas simulated set: api shape, audit.py in the contract shape,
determinism, rules firing on Bombas data, and no em dashes in sentences. data.sqlite is git-ignored;
tests that need rows skip when it is absent."""
import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEO = ROOT / 'app' / 'screens' / '17-seo'
HAS_SQLITE = (ROOT / 'app' / 'data' / 'brands' / 'bombas' / 'data.sqlite').is_file()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


metrics = sys.modules.get('ecomos_metrics') or load('ecomos_metrics', ROOT / 'app' / 'metrics.py')
audit = load('seo_audit', SEO / 'audit.py')
api = load('seo_api_t', SEO / 'api.py')

FIELDS = ['id', 'screen', 'rule_id', 'severity', 'entity', 'evidence', 'sentence', 'capability', 'money_at_stake',
          'confidence', 'brain_refs', 'first_seen', 'last_seen', 'status', 'unavailable']
EVIDENCE = {'metric', 'value', 'unit', 'window', 'ends_on', 'freshness_days', 'baseline', 'baseline_kind', 'source', 'simulated'}
SPEC_RULES = {f'SEO-R{n:02d}' for n in range(1, 14)}


class Req:
    def __init__(self, path, method='GET', query=None):
        self.method, self.path, self.query, self.body = method, path, query or {}, None

    def arg(self, name, default=None):
        v = self.query.get(name)
        return v[0] if v else default


class RulesTable(unittest.TestCase):
    def test_every_spec_rule_is_listed(self):
        self.assertEqual({r['rule_id'] for r in audit.RULES}, SPEC_RULES)
        for r in audit.RULES:
            self.assertEqual(set(r), {'rule_id', 'name', 'entity_type', 'inputs', 'capability', 'owner_screen'})
            self.assertEqual(r['owner_screen'], '17-seo')

    def test_ctr_curve(self):
        self.assertAlmostEqual(audit.curve_ctr(1, False), 0.28)
        self.assertAlmostEqual(audit.curve_ctr(1, True), 0.56)
        self.assertLess(audit.curve_ctr(12, False), audit.curve_ctr(5, False))
        self.assertAlmostEqual(audit.curve_ctr(25, False), 0.01)


@unittest.skipUnless(HAS_SQLITE, 'bombas data.sqlite not built')
class AuditOnBombas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.findings = audit.run('bombas', None)

    def test_contract_shape(self):
        for f in self.findings:
            self.assertEqual(list(f)[:len(FIELDS)], FIELDS)
            self.assertIn(f['severity'], ('critical', 'high', 'medium', 'low'))
            self.assertIn(f['status'], ('open', 'unavailable'))
            self.assertTrue(f['id'].startswith('17-seo.' + f['rule_id'] + '.'))
            self.assertIn(f['capability']['autonomy'], ('agent_does', 'founder_gate', 'human_assist'))
            self.assertTrue(0 <= f['confidence'] <= 1)
            for e in f['evidence']:
                self.assertEqual(set(e), EVIDENCE)
                self.assertTrue(e['simulated'])
            if f['money_at_stake'] is None:
                self.assertIn('money_reason', f)
            else:
                self.assertGreaterEqual(f['money_at_stake']['usd'], 0)
                self.assertTrue({'usd', 'formula', 'inputs', 'window'} <= set(f['money_at_stake']))

    def test_deterministic(self):
        self.assertEqual(json.dumps(self.findings, sort_keys=True), json.dumps(audit.run('bombas', None), sort_keys=True))

    def test_every_rule_accounted_for(self):
        ids = {f['rule_id'] for f in self.findings}
        missing = SPEC_RULES - ids
        # rules that read written tables may be quiet; every other rule reads unavailable
        self.assertTrue(missing <= set(audit.LIVE), missing)

    def test_unavailable_never_zero(self):
        un = [f for f in self.findings if f['status'] == 'unavailable']
        self.assertGreaterEqual(len(un), 9)
        for f in un:
            self.assertEqual(f['evidence'], [])
            self.assertIsNone(f['money_at_stake'])
            self.assertTrue(f['unavailable']['connector'] and f['unavailable']['inputs'] and f['unavailable']['fix'])

    def test_ctr_rule_fires_with_money_in_code(self):
        f = next(f for f in self.findings if f['rule_id'] == 'SEO-R02' and f['status'] == 'open')
        m = f['money_at_stake']
        i = m['inputs']
        expect = (i['curve_ctr'] - i['ctr']) * i['impressions'] * i['organic_conversion_rate_on_page'] * i['aov']
        self.assertEqual(m['usd'], round(expect))
        self.assertEqual(f['entity']['id'], 'home')

    def test_sentences(self):
        for f in self.findings:
            self.assertNotIn('—', f['sentence'])
            self.assertNotIn('–', f['sentence'])
            self.assertLess(len(f['sentence'].split()), 40)
            for word in ('should', 'try ', 'consider'):
                self.assertNotIn(word, f['sentence'].lower())


@unittest.skipUnless(HAS_SQLITE, 'bombas data.sqlite not built')
class ApiOnBombas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = api.handle(Req(['summary'], query={'window': ['28d']}))

    def test_summary_shape(self):
        d = self.d
        self.assertTrue(d['simulated'])
        for k in ('tiles', 'insights', 'chart', 'queries', 'landing_pages', 'findings', 'rules', 'window', 'brand'):
            self.assertIn(k, d)
        self.assertEqual(len(d['tiles']), 3)
        self.assertEqual(len(d['insights']), 2)
        for t in d['tiles']:
            self.assertTrue(t['value'] is not None or t.get('unavailable_reason'))
            self.assertNotEqual(t['value'], 0)
        for i in d['insights']:
            self.assertTrue(i['rule'])
            self.assertTrue(i['sentence'] or i['quiet'])
        self.assertFalse(d['chart']['unavailable'])
        self.assertEqual(len(d['chart']['labels']), 12)

    def test_findings_route_and_errors(self):
        r = api.handle(Req(['findings']))
        self.assertTrue(r['simulated'])
        self.assertEqual(r['findings'], self.d['findings'])
        self.assertEqual(api.handle(Req(['summary'], query={'window': ['3d']}))[0], 400)
        self.assertEqual(api.handle(Req(['nope']))[0], 404)

    def test_no_em_dashes(self):
        text = json.dumps(self.d, ensure_ascii=False)
        self.assertNotIn('—', text)
        for f in ('index.html', 'screen.js'):
            self.assertNotIn('—', (SEO / f).read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
