"""Tests for screen 00-today on the Bombas simulated set: the brand loader, audit.py in the
contract shape, the api (summary, findings, decisions). data.sqlite is git-ignored; tests that
need the session rows run when it exists and the unavailable path is tested either way."""
import importlib.util
import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TODAY = ROOT / 'app' / 'screens' / '00-today'
BOMBAS = ROOT / 'app' / 'data' / 'brands' / 'bombas'
HAS_SQLITE = (BOMBAS / 'data.sqlite').is_file()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


server = load('ecomos_server_t', ROOT / 'app' / 'server.py')
metrics = load('ecomos_metrics', ROOT / 'app' / 'metrics.py')  # the name audit.py and the server share
tables = load('ecomos_tables_t', ROOT / 'app' / 'data' / 'tables.py')
audit = load('today_audit', TODAY / 'audit.py')
api = load('today_api_t', TODAY / 'api.py')

FIELDS = ['id', 'screen', 'rule_id', 'severity', 'entity', 'evidence', 'sentence', 'capability', 'money_at_stake',
          'confidence', 'brain_refs', 'first_seen', 'last_seen', 'status', 'unavailable']
EVIDENCE = {'metric', 'value', 'unit', 'window', 'ends_on', 'freshness_days', 'baseline', 'baseline_kind', 'source', 'simulated'}


class Req:
    def __init__(self, path, method='GET', query=None, body=None):
        self.method, self.path, self.query, self.body = method, path, query or {}, body
        self.data = server.Data()
        self.slug = '00-today'

    def arg(self, name, default=None):
        v = self.query.get(name)
        return v[0] if v else default


class BrandLoaderTest(unittest.TestCase):
    def test_brand_record_and_daily_aggregate(self):
        d = tables.BrandData('bombas')
        self.assertEqual(d.brand['as_of'], '2026-09-27')
        self.assertEqual(d.brand['market'], 'US')
        self.assertTrue(d.brand['simulated'])
        daily = d.table('daily')
        self.assertEqual(len(daily), 730)
        self.assertEqual(d.meta('daily')['source'], 'generator')

    def test_unknown_brand_and_big_tables(self):
        with self.assertRaises(ValueError):
            tables.BrandData('../etc')
        with self.assertRaises(KeyError):
            tables.BrandData('bombas').table('no_such_table')
        if HAS_SQLITE:
            with self.assertRaises(ValueError):   # 11M rows: read through the aggregate
                tables.BrandData('bombas').table('orders')

    def test_aov_from_the_aggregate_through_the_server(self):
        r = server.Data().metric('aov', window='28d', brand='bombas')
        self.assertFalse(r['unavailable'], r.get('reason'))
        self.assertTrue(60 < r['value'] < 90, r['value'])
        self.assertEqual(r['window']['end'], '2026-09-27')
        self.assertEqual(r['freshness']['sources'][0]['table'], 'daily')

    def test_sample_brand_is_unchanged_without_brand(self):
        self.assertNotEqual(server.Data().brand.get('as_of'), None)
        self.assertEqual(server.Data().metric('aov', brand='')['window']['end'], server.Data().brand['as_of'])

    def test_device_split_is_unavailable_not_zero(self):
        r = server.Data().metric('aov', brand='bombas', device='mobile')
        self.assertTrue(r['unavailable'])
        self.assertIsNone(r['value'])


class AuditTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.findings = audit.run('bombas')

    def test_contract_shape(self):
        self.assertTrue(self.findings)
        for f in self.findings:
            self.assertEqual([k for k in FIELDS if k not in f], [], f['id'])
            self.assertRegex(f['id'], r'^00-today\.TODAY-R\d\d\.[a-z_]+$')
            self.assertEqual(f['id'], f"{f['screen']}.{f['rule_id']}.{f['entity']['id']}")
            self.assertIn(f['severity'], ('critical', 'high', 'medium', 'low'))
            self.assertIn(f['status'], ('open', 'resolved', 'unavailable', 'snoozed'))
            self.assertIn(f['capability']['autonomy'], ('agent_does', 'founder_gate', 'human_assist'))
            self.assertTrue(0.1 <= f['confidence'] <= 1)
            for e in f['evidence']:
                self.assertEqual(EVIDENCE - set(e), set(), f['id'])
                self.assertTrue(e['simulated'])
            if f['money_at_stake'] is None:
                self.assertTrue(f.get('money_reason'))
            else:
                self.assertGreaterEqual(f['money_at_stake']['usd'], 0)
                self.assertIn('x', f['money_at_stake']['formula'])

    def test_wording(self):
        for f in self.findings:
            s = f['sentence']
            self.assertLessEqual(len(s.split()), 40, s)
            self.assertNotIn('—', s)
            self.assertIsNone(re.search(r'\b(should|try|consider)\b', s, re.I), s)

    def test_rules_listed(self):
        self.assertEqual([r['rule_id'] for r in audit.RULES], ['TODAY-R01', 'TODAY-R02'])
        for r in audit.RULES:
            self.assertEqual(r['owner_screen'], '00-today')

    def test_deterministic(self):
        self.assertEqual(json.dumps(audit.run('bombas'), sort_keys=True), json.dumps(self.findings, sort_keys=True))

    @unittest.skipUnless(HAS_SQLITE, 'data.sqlite not built (python3 app/data/generate.py --brand bombas)')
    def test_pipeline_break_has_money(self):
        breaks = [f for f in self.findings if f['rule_id'] == 'TODAY-R01' and f['status'] == 'open']
        self.assertTrue(breaks)
        top = breaks[0]
        stake = top['money_at_stake']
        i = stake['inputs']
        redo = (i['median_rate'] - i['current_rate']) * i['volume_in'] * i['value_per_unit']
        self.assertAlmostEqual(stake['usd'], redo, delta=stake['usd'] * 1e-4)  # inputs are written rounded
        self.assertGreater(stake['usd'], 0)
        rate = next(e for e in top['evidence'] if e['metric'].endswith('_step_rate'))
        self.assertLess(rate['value'], rate['baseline'])
        self.assertEqual(rate['baseline_kind'], 'own_median')

    def test_unavailable_when_sessions_are_missing(self):
        real = tables.BrandData('bombas')
        fake = tables.BrandData('bombas')
        fake.sqlite = Path(tempfile.gettempdir()) / 'no-such-ecomos.sqlite'
        mod = audit.metrics_module()._TABLES   # the server may have reloaded ecomos_metrics
        saved = mod._BRANDS.get('bombas')
        mod._BRANDS['bombas'] = fake
        try:
            out = audit.run('bombas')
        finally:
            mod._BRANDS['bombas'] = saved or real
        self.assertEqual(len(out), 1)
        f = out[0]
        self.assertEqual(f['status'], 'unavailable')
        self.assertEqual(f['evidence'], [])
        self.assertIsNone(f['money_at_stake'])
        self.assertTrue(f['unavailable']['fix'])


class ApiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp())
        cls.saved_path = api.decisions_path
        api.decisions_path = lambda: cls.tmp / 'decisions.json'

    @classmethod
    def tearDownClass(cls):
        api.decisions_path = cls.saved_path
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_summary(self):
        d = api.handle(Req(['summary']))
        self.assertTrue(d['simulated'])
        self.assertEqual(d['brand']['brand'], 'bombas')
        self.assertEqual(len(d['tiles']), 3)
        self.assertEqual([i['name'] for i in d['insights']], ['top break named', 'trend alert'])
        for i in d['insights']:
            self.assertTrue(i['rule'])
        self.assertEqual(len(d['chart']['labels']), 90)
        self.assertEqual(d['chart']['labels'][-1], '2026-09-27')
        self.assertTrue(all(isinstance(v, float) for v in d['chart']['values']))
        self.assertEqual(len(d['top10']['cards']), 10)
        self.assertTrue(d['top10']['stub'])
        self.assertEqual(len(d['windows']), 4)
        if HAS_SQLITE:
            self.assertEqual([s['stage'] for s in d['stages']], ['sessions', 'product_view', 'add_to_cart', 'checkout', 'purchase'])
            self.assertEqual(sum(s['is_break'] for s in d['stages']), 1)
            for s in d['stages']:
                self.assertEqual(len(s['windows']), 4)
            self.assertGreater(d['money_at_stake']['value'], 0)
            self.assertTrue(d['insights'][0]['sentence'])
        else:
            self.assertTrue(d['money_at_stake']['unavailable'])
            self.assertIsNone(d['tiles'][0]['value'])

    def test_findings_route(self):
        d = api.handle(Req(['findings']))
        self.assertTrue(d['findings'])
        self.assertEqual(len(d['rules']), 2)

    def test_decisions_write_to_the_brand_log(self):
        status, body = api.handle(Req(['decisions'], 'POST', body={'capability': 'PROP-C06', 'choice': 'agent',
                                                                  'autonomy': 'agent_does', 'card': 'stub-02', 'reason': 'go'}))
        self.assertEqual(status, 201)
        self.assertEqual(body['decision']['brand'], 'bombas')
        rows = json.loads((self.tmp / 'decisions.json').read_text(encoding='utf-8'))
        self.assertEqual(rows[-1]['card'], 'stub-02')
        self.assertEqual(api.handle(Req(['decisions']))['decisions'][-1]['choice'], 'agent')
        self.assertEqual(api.handle(Req(['decisions'], 'POST', body={'capability': 'X', 'choice': 'maybe'}))[0], 400)
        self.assertEqual(api.handle(Req(['decisions'], 'POST', body={'capability': 'bad id!', 'choice': 'agent'}))[0], 400)

    def test_unknown_route(self):
        self.assertEqual(api.handle(Req(['nope']))[0], 404)

    def test_page_says_simulated(self):
        html = (TODAY / 'index.html').read_text(encoding='utf-8')
        self.assertIn('simulated data', html)
        self.assertIn('simulated data', (TODAY / 'screen.js').read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
