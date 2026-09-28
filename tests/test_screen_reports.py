"""26-reports round 0: api shape, audit shape and determinism, rules fire on Bombas,
a raising screen audit is reported as unavailable, no em dashes in sentences.

The real run reads every other screen's audit (about 20 seconds), so it happens once per
class and is shared. Tests that need a broken screen swap report.discover_audits.
"""
import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / 'app' / 'screens' / '26-reports'
HAVE_DATA = (ROOT / 'app' / 'data' / 'brands' / 'bombas' / 'aggregates' / 'daily.json').is_file()
FINDING_KEYS = ['id', 'screen', 'rule_id', 'severity', 'entity', 'evidence', 'sentence', 'capability',
                'money_at_stake', 'confidence', 'brain_refs', 'first_seen', 'last_seen', 'status', 'unavailable']
EVIDENCE_KEYS = {'metric', 'value', 'unit', 'window', 'ends_on', 'freshness_days', 'baseline', 'baseline_kind', 'source', 'simulated'}
EM_DASH = '—'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


class Req:
    def __init__(self, route, method='GET', body=None, **query):
        self.path, self.method, self.body = [route], method, body
        self.query = {k: [v] for k, v in query.items()}

    def arg(self, name, default=None):
        v = self.query.get(name)
        return v[0] if v else default


@unittest.skipUnless(HAVE_DATA, 'Bombas aggregates are missing')
class ReportsScreen(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api = load('reports_api_test', FOLDER / 'api.py')
        cls.audit = cls.api.audit()
        cls.R = cls.audit.report()
        cls.R.clear_cache()
        cls.week = cls.api.handle(Req('summary', period='week'))
        cls.p = cls.R.period('bombas', 'week')
        cls.findings = cls.audit.run('bombas', {'ends_on': cls.p['end'], 'days': 7, 'trailing': 4})

    # ------------------------------------------------------------ api

    def test_api_shape(self):
        d = self.week
        for key in ('brand', 'simulated', 'period', 'tiles', 'insights', 'what_changed', 'channel_mix', 'chart',
                    'top10', 'shipped', 'brain', 'open_questions', 'screens', 'findings', 'rules', 't0_card'):
            self.assertIn(key, d)
        self.assertTrue(d['simulated'])
        self.assertEqual(len(d['tiles']), 3)
        self.assertEqual(len(d['insights']), 2)
        for i in d['insights']:
            self.assertTrue(i['rule'])
            self.assertTrue(i['sentence'] or i['quiet'])
        self.assertEqual(len(d['chart']['labels']), len(d['chart']['values']))
        self.assertLessEqual(len(d['top10']), 10)
        usd = [t['usd'] for t in d['top10'] if t['usd'] is not None]
        self.assertEqual(usd, sorted(usd, reverse=True))
        for t in d['top10']:
            self.assertIn(t['decision']['status'], ('none', 'agent', 'person', 'not_now'))
        self.assertEqual(self.api.handle(Req('summary', period='year'))[0], 400)
        self.assertEqual(self.api.handle(Req('nope'))[0], 404)

    def test_unavailable_is_never_zero(self):
        for l in self.week['what_changed']:
            if l['unavailable']:
                self.assertIsNone(l['value'], l['key'])
                self.assertTrue(l['reason'])
        margin = next(l for l in self.week['what_changed'] if l['key'] == 'contribution_margin')
        self.assertTrue(margin['unavailable'] or margin['value'] is not None)

    def test_numbers_come_from_the_contract(self):
        M = self.R.metrics_module()
        aov = M.compute('aov', None, brand='bombas', window='7d', end=self.p['end'])
        line = next(l for l in self.week['what_changed'] if l['key'] == 'net_revenue')
        self.assertEqual(line['value'], aov['inputs']['net_revenue'])
        self.assertEqual(line['metric'], 'aov')

    def test_decision_validation(self):
        with self.assertRaises(ValueError):
            self.api.validate({'capability': 'bad id!', 'choice': 'agent'})
        with self.assertRaises(ValueError):
            self.api.validate({'capability': 'LOOP-C01', 'choice': 'maybe'})
        row = self.api.validate({'capability': 'LOOP-C01', 'choice': 'not_now', 'card': '26-reports.x'})
        self.assertEqual(row['screen'], '26-reports')

    # ------------------------------------------------------------ audit

    def test_audit_shape(self):
        self.assertTrue(self.findings)
        rule_ids = {r['rule_id'] for r in self.audit.RULES}
        for f in self.findings:
            for k in FINDING_KEYS:
                self.assertIn(k, f)
            self.assertEqual(f['screen'], '26-reports')
            self.assertIn(f['rule_id'], rule_ids)
            self.assertTrue(f['id'].startswith(f"26-reports.{f['rule_id']}."))
            self.assertIn(f['severity'], ('critical', 'high', 'medium', 'low'))
            self.assertIn(f['status'], ('open', 'resolved', 'unavailable', 'snoozed'))
            self.assertIn(f['capability']['autonomy'], ('agent_does', 'founder_gate', 'human_assist'))
            self.assertTrue(0 <= f['confidence'] <= 1)
            for e in f['evidence']:
                self.assertEqual(set(e) & EVIDENCE_KEYS, EVIDENCE_KEYS)
                self.assertTrue(e['simulated'])
            m = f['money_at_stake']
            if m is None:
                self.assertTrue(f.get('money_reason'))
            else:
                self.assertGreaterEqual(m['usd'], 0)
                self.assertTrue(m['formula'])
            if f['status'] == 'unavailable':
                self.assertIsNone(m)
                self.assertTrue(f['unavailable']['fix'])
        self.assertEqual(len({f['id'] for f in self.findings}), len(self.findings))
        order = [self.audit.SEVERITY_ORDER[f['severity']] for f in self.findings]
        self.assertEqual(order, sorted(order))

    def test_rules_fire_on_bombas(self):
        fired = {f['rule_id'] for f in self.findings if f['status'] == 'open'}
        self.assertIn('REPORT-R01', fired)  # new versus repeat is read from the aggregate, not the contract
        r01 = next(f for f in self.findings if f['rule_id'] == 'REPORT-R01')
        self.assertEqual(r01['entity']['id'], 'new_customer_share')
        for f in self.findings:
            if f['rule_id'] == 'REPORT-R02' and f['money_at_stake']:
                inp = f['money_at_stake']['inputs']
                if 'summary_sheet' in inp:
                    self.assertEqual(f['money_at_stake']['usd'], round(abs(inp['summary_sheet'] - inp['contract'])))

    def test_determinism(self):
        self.R.clear_cache()
        again = self.audit.run('bombas', {'ends_on': self.p['end'], 'days': 7, 'trailing': 4})
        self.assertEqual(json.dumps(self.findings, sort_keys=True), json.dumps(again, sort_keys=True))

    def test_no_em_dashes(self):
        texts = [f['sentence'] for f in self.findings]
        texts += [i.get('sentence') or i.get('quiet') for i in self.week['insights']]
        texts += [t['name'] + t.get('plain', '') for t in self.week['tiles']]
        for t in texts:
            self.assertNotIn(EM_DASH, t)
        for name in ('index.html', 'screen.js', 'api.py', 'audit.py', 'report.py'):
            self.assertNotIn(EM_DASH, (FOLDER / name).read_text(encoding='utf-8'), name)
        for f in self.findings:
            self.assertLessEqual(len(f['sentence'].split()), 40, f['sentence'])
            for word in ('should', 'try ', 'consider'):
                self.assertNotIn(word, f['sentence'].lower())

    # ------------------------------------------------------------ a screen that raises

    def test_raising_screen_audit_is_unavailable(self):
        R = self.R
        real = R.discover_audits

        def boom(brand, window):
            raise RuntimeError('table gone')

        def ok(brand, window):
            return [{'id': '98-ok.OK-R01.x', 'screen': '98-ok', 'rule_id': 'OK-R01', 'severity': 'high',
                     'entity': {'type': 'brand', 'id': 'x', 'label': 'X'}, 'evidence': [], 'sentence': 'Fine.',
                     'capability': {'id': 'DIAG-C02', 'autonomy': 'agent_does'},
                     'money_at_stake': {'usd': 5, 'formula': 'f', 'inputs': {}, 'window': '7d'}, 'confidence': 0.5,
                     'brain_refs': [], 'first_seen': '2026-09-27', 'last_seen': '2026-09-27', 'status': 'open', 'unavailable': None}]
        R.discover_audits = lambda: [('98-ok', ok), ('99-boom', boom)]
        try:
            R.clear_cache()
            d = self.api.handle(Req('summary', period='week'))
            screens = {s['screen']: s for s in d['screens']}
            self.assertEqual(screens['99-boom']['status'], 'unavailable')
            self.assertIn('table gone', screens['99-boom']['reason'])
            self.assertEqual(screens['98-ok']['status'], 'ok')
            self.assertEqual([t['id'] for t in d['top10']], ['98-ok.OK-R01.x'])
            r05 = [f for f in d['findings'] if f['rule_id'] == 'REPORT-R05']
            self.assertEqual(len(r05), 1)
            self.assertEqual(r05[0]['status'], 'unavailable')
            self.assertEqual(r05[0]['entity']['id'], '99-boom')
        finally:
            R.discover_audits = real
            R.clear_cache()


if __name__ == '__main__':
    unittest.main()
