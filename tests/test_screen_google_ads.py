"""Screen 12-google-ads: the term rules, the brand tag, and (when data.sqlite is built) the api and audit on Bombas."""
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / 'app' / 'screens' / '12-google-ads'
SQLITE = ROOT / 'app' / 'data' / 'brands' / 'bombas' / 'data.sqlite'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


api = load('gads_api_test', FOLDER / 'api.py')
audit = load('gads_audit_test', FOLDER / 'audit.py')

FIELDS = ['id', 'screen', 'rule_id', 'severity', 'entity', 'evidence', 'sentence', 'capability', 'money_at_stake',
          'confidence', 'brain_refs', 'first_seen', 'last_seen', 'status', 'unavailable']
EVIDENCE = {'metric', 'value', 'unit', 'window', 'ends_on', 'freshness_days', 'baseline', 'baseline_kind', 'source', 'simulated'}


class Rules(unittest.TestCase):
    def term(self, **kw):
        t = {'term': 'merino wool socks', 'status': 'NONE', 'spend': 100.0, 'conversions': 0, 'cpa': None}
        t.update(kw)
        return t

    def test_zero_conversion_waste_is_a_negative(self):
        self.assertEqual(api.term_rule(self.term(spend=100.0), 40.0)[0], 'negative')
        self.assertEqual(api.term_rule(self.term(spend=70.0), 40.0)[0], 'keep')

    def test_poor_cpa_is_a_negative(self):
        self.assertEqual(api.term_rule(self.term(spend=400.0, conversions=4, cpa=100.0), 40.0)[0], 'negative')

    def test_bad_intent_is_a_negative_even_without_cpa(self):
        self.assertEqual(api.term_rule(self.term(term='bombas careers'), None)[0], 'negative')

    def test_new_keyword_needs_volume_and_cpa(self):
        self.assertEqual(api.term_rule(self.term(spend=380.0, conversions=10, cpa=38.0), 40.0)[0], 'new keyword')
        self.assertEqual(api.term_rule(self.term(spend=90.0, conversions=9, cpa=10.0), 40.0)[0], 'keep')
        self.assertEqual(api.term_rule(self.term(status='ADDED', spend=380.0, conversions=10, cpa=38.0), 40.0)[0], 'keep')

    def test_brand_tag(self):
        self.assertEqual(api.tag('Brand | Search'), 'brand')
        self.assertEqual(api.tag('Non-brand | Search | Socks'), 'nonbrand')
        self.assertEqual(api.tag('Shopping | PMax'), 'nonbrand')
        self.assertIsNone(api.tag(None))

    def test_window_bounds(self):
        self.assertEqual(api.parse_days('28d'), 28)
        with self.assertRaises(ValueError):
            api.parse_days('3d')

    def test_rules_list_the_contract_fields(self):
        for r in audit.RULES:
            self.assertEqual(set(r), {'rule_id', 'name', 'entity_type', 'inputs', 'capability', 'owner_screen'})


@unittest.skipUnless(SQLITE.is_file(), 'bombas data.sqlite not built (python3 app/data/generate.py --brand bombas --scale 0.1)')
class OnBombas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out = api.build('bombas', '28d')
        cls.findings = audit.run('bombas', {'days': 28})

    def test_screen_payload(self):
        o = self.out
        self.assertFalse(o['unavailable'])
        self.assertTrue(o['simulated'])
        self.assertGreaterEqual(len(o['tiles']), 3)
        s = o['split']
        self.assertAlmostEqual(s['brand']['spend'] + s['nonbrand']['spend'], s['total']['spend'], places=1)
        self.assertAlmostEqual(s['brand']['share_of_spend'] + s['nonbrand']['share_of_spend'], 1, places=3)
        self.assertAlmostEqual(s['total']['roas'], s['total']['value'] / s['total']['spend'], places=3)
        self.assertIn('flagged', s['brand']['incrementality'])
        self.assertEqual(len(o['chart']['labels']), 90)

    def test_split_matches_the_metric_contract(self):
        m = api.metrics().compute('spend', None, brand='bombas', window='28d', channel='google')
        self.assertAlmostEqual(m['value'], self.out['split']['total']['spend'], places=1)

    def test_non_search_campaigns_read_unavailable_not_zero(self):
        for r in self.out['impression_share']:
            if r['channel_type'] != 'SEARCH':
                self.assertIsNone(r['impression_share'])
                self.assertTrue(r['reason'])

    def test_asset_group_spend_is_unavailable(self):
        self.assertTrue(self.out['asset_groups'])
        self.assertIsNone(self.out['asset_groups'][0]['spend'])

    def test_conversion_check_states_the_gap(self):
        c = self.out['conversion_check']
        self.assertFalse(c['unavailable'])
        self.assertAlmostEqual(c['conversion_gap'], (c['google_conversions'] - c['store_orders']) / c['store_orders'], places=3)

    def test_findings_follow_the_audit_contract(self):
        ids = {f['rule_id'] for f in self.findings}
        self.assertIn('GADS-R01', ids)
        self.assertIn('GADS-R02', ids)
        for f in self.findings:
            self.assertEqual(list(f)[:len(FIELDS)], FIELDS)
            self.assertIn(f['severity'], ('critical', 'high', 'medium', 'low'))
            self.assertTrue(f['id'].startswith('12-google-ads.' + f['rule_id'] + '.'))
            self.assertLessEqual(len(f['sentence'].split()), 40)
            self.assertNotIn('—', f['sentence'])
            self.assertNotRegex(f['sentence'].lower(), r'\b(should|try|consider)\b')
            for e in f['evidence']:
                self.assertTrue(EVIDENCE <= set(e))
            if f['money_at_stake'] is None:
                self.assertTrue(f['money_reason'])
            else:
                self.assertGreaterEqual(f['money_at_stake']['usd'], 0)
                self.assertTrue(f['money_at_stake']['formula'])

    def test_money_on_the_two_required_findings(self):
        by = {f['rule_id']: f for f in self.findings}
        for rid in ('GADS-R01', 'GADS-R02'):
            self.assertIsNotNone(by[rid]['money_at_stake'])
        r02 = by['GADS-R02']['money_at_stake']
        i = r02['inputs']
        self.assertAlmostEqual(r02['usd'], i['spend'] * i['lost_is_budget'] / i['impression_share'] * i['campaign_roas'], places=0)

    def test_run_is_deterministic_and_sorted(self):
        again = audit.run('bombas', {'days': 28})
        self.assertEqual(json.dumps(again, sort_keys=True), json.dumps(self.findings, sort_keys=True))
        order = [audit.SEV_ORDER[f['severity']] for f in self.findings]
        self.assertEqual(order, sorted(order))


if __name__ == '__main__':
    unittest.main()
