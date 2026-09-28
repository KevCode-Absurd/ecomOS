"""Screen 09-creative: audit rules, API shape, and the page data on Bombas simulated data.

Pure rule functions are tested on small inputs so each rule is proven to fire.
The Bombas tests skip when app/data/brands/bombas/data.sqlite has not been built.
"""
import importlib.util
import json
import sys
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / 'app' / 'screens' / '09-creative'
BOMBAS_DB = ROOT / 'app' / 'data' / 'brands' / 'bombas' / 'data.sqlite'
AUDIT_KEYS = ['id', 'screen', 'rule_id', 'severity', 'entity', 'evidence', 'sentence', 'capability', 'money_at_stake',
              'confidence', 'brain_refs', 'first_seen', 'last_seen', 'status', 'unavailable']
EVIDENCE_KEYS = {'metric', 'value', 'unit', 'window', 'ends_on', 'freshness_days', 'baseline', 'baseline_kind',
                 'source', 'simulated'}
END = date(2026, 9, 27)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


api = load('creative_api_test', SCREEN / 'api.py')
audit = api.audit


def check_finding(tc, f):
    for k in AUDIT_KEYS:
        tc.assertIn(k, f)
    tc.assertEqual(f['screen'], '09-creative')
    tc.assertIn(f['severity'], ('critical', 'high', 'medium', 'low'))
    tc.assertIn(f['status'], ('open', 'resolved', 'unavailable', 'snoozed'))
    tc.assertEqual(f['id'], f"09-creative.{f['rule_id']}.{f['entity']['id']}")
    tc.assertIn(f['rule_id'], [r['rule_id'] for r in audit.RULES])
    tc.assertIn(f['capability']['autonomy'], ('agent_does', 'founder_gate', 'human_assist'))
    tc.assertTrue(0 <= f['confidence'] <= 1)
    tc.assertNotIn('—', f['sentence'])
    tc.assertLessEqual(len(f['sentence'].split()), 40)
    for e in f['evidence']:
        tc.assertTrue(EVIDENCE_KEYS <= set(e))
        tc.assertTrue(e['simulated'])
    if f['money_at_stake'] is None:
        tc.assertTrue(f.get('money_reason'))
    else:
        tc.assertGreaterEqual(f['money_at_stake']['usd'], 0)
        tc.assertTrue(f['money_at_stake']['formula'])
    if f['status'] == 'unavailable':
        tc.assertEqual(f['evidence'], [])
        tc.assertTrue(f['unavailable']['inputs'] and f['unavailable']['fix'])


class RuleUnits(unittest.TestCase):
    def test_format_rule_fires_with_money_in_code(self):
        now = {'carousel': {'spend': 1000.0, 'purchase_value': 1500.0, 'roas': 1.5, 'ads': 2},
               'image': {'spend': 4000.0, 'purchase_value': 8000.0, 'roas': 2.0, 'ads': 5}}
        past = {'carousel': {'spend': 1000.0, 'purchase_value': 2000.0, 'roas': 2.0, 'ads': 2},
                'image': {'spend': 4000.0, 'purchase_value': 8000.0, 'roas': 2.0, 'ads': 5}}
        fs = audit.format_findings([now, past, past, past, past], END, 100000)
        self.assertEqual([f['entity']['id'] for f in fs], ['format_carousel'])
        self.assertEqual(fs[0]['money_at_stake']['usd'], 500)  # 1000 x (2.0 - 1.5)
        check_finding(self, fs[0])

    def test_volume_rule(self):
        fs = audit.volume_findings([4, 10, 12, 10, 11], END)
        self.assertEqual(len(fs), 1)
        self.assertIsNone(fs[0]['money_at_stake'])
        check_finding(self, fs[0])
        self.assertEqual(audit.volume_findings([10, 10, 12, 10, 11], END), [])

    def test_starved_winner(self):
        ads = {'A': {'ad': 'A', 'spend': 100.0, 'roas': 4.0, 'purchases': 8, 'first_day': '2026-08-01', 'last_day': '2026-09-27',
                     'format': 'image', 'campaign_name': 'P'},
               'B': {'ad': 'B', 'spend': 9900.0, 'roas': 2.0, 'purchases': 300, 'first_day': '2026-08-01',
                     'last_day': '2026-09-27', 'format': 'image', 'campaign_name': 'P'}}
        fs = audit.starved_findings(ads, END, 2.0)
        self.assertEqual([f['entity']['id'] for f in fs], ['A'])
        check_finding(self, fs[0])

    def test_competitor_gap_is_signal_only(self):
        recs = [{'id': f'x.learnings.c{i}', 'value': {'role': 'competitor', 'page': f'C{i}', 'formats': {'dco': 50, 'image': 50}}}
                for i in range(3)]
        fs = audit.gap_findings(recs, {'image', 'video'}, END)
        self.assertEqual([f['entity']['id'] for f in fs], ['gap_dco'])
        self.assertEqual(fs[0]['severity'], 'low')
        self.assertEqual(len(fs[0]['brain_refs']), 3)
        check_finding(self, fs[0])
        self.assertEqual(audit.gap_findings(recs, {'dco', 'image'}, END), [])

    def test_rules_list(self):
        self.assertEqual([r['rule_id'] for r in audit.RULES], [f'CREA-R0{i}' for i in range(1, 7)])
        for r in audit.RULES:
            self.assertEqual(set(r), {'rule_id', 'name', 'entity_type', 'inputs', 'capability', 'owner_screen'})


@unittest.skipUnless(BOMBAS_DB.is_file(), 'bombas data.sqlite not built')
class Bombas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.findings = audit.run('bombas')
        cls.overview = api.overview(None, 'bombas')

    def test_shape(self):
        self.assertTrue(self.findings)
        for f in self.findings:
            check_finding(self, f)

    def test_deterministic(self):
        again = audit.run('bombas', {'ends_on': self.overview['window']['ends_on']})
        self.assertEqual(json.dumps(self.findings, sort_keys=True), json.dumps(again, sort_keys=True))

    def test_open_findings_carry_money_and_unavailable_name_inputs(self):
        # On the scale 1.0 rebuild of 28 Sep none of the threshold rules trips (see FEATURES.md, round 1 job 1),
        # so round 0 promises the shape, not a firing: open findings carry money, unavailable ones name their inputs.
        opened = [f for f in self.findings if f['status'] == 'open']
        for f in opened:
            self.assertTrue(f['money_at_stake'])
        unavailable = [f for f in self.findings if f['status'] == 'unavailable']
        self.assertTrue(self.findings)
        for f in unavailable:
            self.assertTrue(f['unavailable']['inputs'])

    def test_unavailable_never_zero(self):
        for f in self.findings:
            if f['status'] == 'unavailable':
                self.assertIsNone(f['money_at_stake'])
        hook = self.overview['tiles']['hook_rate']
        if hook['value'] is None:
            self.assertTrue(hook['unavailable_reason'])

    def test_api_shape(self):
        o = self.overview
        self.assertTrue(o['brand']['simulated'])
        self.assertEqual(len(o['tiles']), 3)
        self.assertEqual(len(o['insights']), 2)
        for i in o['insights']:
            self.assertTrue(i['rule'] and i['sentence'])
        self.assertTrue(o['chart']['labels'] and o['chart']['series'])
        for s in o['chart']['series']:
            self.assertEqual(len(s['values']), len(o['chart']['labels']))
        self.assertTrue(o['formats'])

    def test_no_em_dashes(self):
        text = json.dumps(self.overview, ensure_ascii=False)
        self.assertNotIn('—', text)
        for p in ('screen.js', 'index.html', 'api.py', 'audit.py'):
            self.assertNotIn('—', (SCREEN / p).read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
