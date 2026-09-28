import json, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.reg = json.loads((ROOT / 'app' / 'inspiration' / 'registry.json').read_text(encoding='utf-8'))

    def test_every_source_is_complete(self):
        ids = set()
        for s in self.reg['sources']:
            for key in ('id', 'domain', 'kind', 'access', 'yields', 'puller', 'cost_note', 'fixture', 'refresh'):
                self.assertIn(key, s, s.get('id'))
            self.assertIn(s['domain'], self.reg['domains'])
            self.assertIn(s['access'], ('public', 'key', 'paid'))
            self.assertNotIn(s['id'], ids); ids.add(s['id'])
            if s['access'] == 'paid':
                self.assertIn('USD', s['cost_note'], s['id'])

    def test_every_domain_has_a_source_and_rules(self):
        for d in self.reg['domains']:
            self.assertTrue(any(s['domain'] == d for s in self.reg['sources']), d)
            self.assertTrue(any(d in r['domains'] for r in self.reg['relevance_rules']), d)

    def test_rules_have_weights_and_brain_fields(self):
        for r in self.reg['relevance_rules']:
            self.assertTrue(0 < r['weight'] <= 1.0)
            if r['id'] != 'own_brand':
                self.assertTrue(r['brain_fields'], r['id'])
        self.assertEqual(self.reg['show_threshold'], 0.3)

    def test_rights_and_contract_present(self):
        self.assertIn('reference_only', self.reg['rights'])
        self.assertEqual(self.reg['rights']['quote_max_chars'], 140)
        self.assertTrue((ROOT / self.reg['contract']).exists())
        text = (ROOT / 'app' / 'contracts' / 'inspiration.md').read_text(encoding='utf-8')
        self.assertNotIn('—', text)


if __name__ == '__main__':
    unittest.main()
