"""Tests for screen 03-competitors on the Bombas brain: audit.py in the contract shape and the api
(overview tiles, insights, chart, map, price ladder, board, lookalike). Edits go to a temp copy of app/brain."""
import datetime as dt
import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / 'app' / 'screens' / '03-competitors'
BRAIN = ROOT / 'app' / 'brain'
DAY = '2026-09-28'
WINDOW = {'ends_on': '2026-09-27', 'days': 1, 'trailing': 0}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


audit = load('competitors_audit_t', SCREEN / 'audit.py')
api = load('competitors_api_t', SCREEN / 'api.py')

FIELDS = ['id', 'screen', 'rule_id', 'severity', 'entity', 'evidence', 'sentence', 'capability', 'money_at_stake',
          'confidence', 'brain_refs', 'first_seen', 'last_seen', 'status', 'unavailable']
EVIDENCE = {'metric', 'value', 'unit', 'window', 'ends_on', 'freshness_days', 'baseline', 'baseline_kind', 'source', 'simulated'}
ENTITY_TYPES = {'brand', 'stage', 'page', 'device', 'sku', 'campaign', 'adset', 'ad', 'flow', 'offer', 'ladder_rung', 'metric'}


class Req:
    def __init__(self, path, method='GET', query=None):
        self.method, self.path, self.body = method, path, None
        self.query = dict({'today': [DAY]}, **(query or {}))

    def arg(self, name, default=None):
        v = self.query.get(name)
        return v[0] if v else default


class TempBrain(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        shutil.copytree(BRAIN / 'bombas', self.tmp / 'bombas')

    def tearDown(self):
        api.BRAIN_ROOT = None
        shutil.rmtree(self.tmp)

    def edit(self, name, fn):
        path = self.tmp / 'bombas' / f'{name}.json'
        rows = json.loads(path.read_text(encoding='utf-8'))
        path.write_text(json.dumps(fn(rows)), encoding='utf-8')


class TestParse(unittest.TestCase):
    def test_bands(self):
        b = audit.parse_band('12 to 25 per pair, median about 18')
        self.assertEqual((b['low'], b['high'], b['median'], b['rough']), (12.0, 25.0, 18.0, False))
        b = audit.parse_band('10 to 59 per product, median about 19 per pair (pack parsing rough)')
        self.assertEqual((b['low'], b['high'], b['median'], b['rough']), (None, None, 19.0, True))
        b = audit.parse_band('from 18 per pair, median 25')
        self.assertEqual((b['low'], b['high'], b['median']), (18.0, None, 25.0))
        self.assertIsNone(audit.parse_band(None)['median'])

    def test_scores(self):
        self.assertEqual(audit.durability_score(['lifetime guarantee', 'durability first']), 3)
        self.assertEqual(audit.durability_score(['style']), 0)
        self.assertEqual(audit.comfort_score(['comfort', 'problem to relief', 'lab tested claim']), 3)

    def test_last_full_month(self):
        self.assertEqual(audit.last_full_month('2026-09-27'), '2026-08')
        self.assertEqual(audit.last_full_month('2026-09-30'), '2026-09')


class TestAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.findings = audit.run('bombas', WINDOW)

    def test_contract_shape(self):
        self.assertTrue(self.findings)
        for f in self.findings:
            for k in FIELDS:
                self.assertIn(k, f)
            self.assertEqual(f['screen'], '03-competitors')
            self.assertTrue(f['id'].startswith('03-competitors.' + f['rule_id'] + '.'))
            self.assertIn(f['severity'], audit.SEVERITY_ORDER)
            self.assertIn(f['entity']['type'], ENTITY_TYPES)
            self.assertIn(f['capability']['autonomy'], {'agent_does', 'founder_gate', 'human_assist'})
            self.assertIsNone(f['money_at_stake'])
            self.assertTrue(f['money_reason'])
            self.assertTrue(0.1 <= f['confidence'] <= 1)
            self.assertLessEqual(len(f['sentence'].split()), 40)
            self.assertNotIn('—', f['sentence'])
            for row in f['evidence']:
                self.assertEqual(set(row), EVIDENCE)
        rule_ids = {r['rule_id'] for r in audit.RULES}
        self.assertTrue({f['rule_id'] for f in self.findings} <= rule_ids)

    def test_unclaimed_angle(self):
        ids = {f['id'] for f in self.findings if f['rule_id'] == 'COMP-R01'}
        self.assertIn('03-competitors.COMP-R01.angle_giving', ids)
        self.assertNotIn('03-competitors.COMP-R01.angle_comfort_relief', ids)
        giving = next(f for f in self.findings if f['id'] == '03-competitors.COMP-R01.angle_giving')
        self.assertIn('bombas.identity.giving_model', giving['brain_refs'])
        self.assertEqual(giving['capability']['id'], 'BRAND-C21')

    def test_price_gap(self):
        f = next(f for f in self.findings if f['rule_id'] == 'COMP-R02')
        self.assertEqual(f['status'], 'open')
        brand = next(r for r in f['evidence'] if r['metric'] == 'brand_price_per_pair')
        comp = next(r for r in f['evidence'] if r['metric'] == 'competitor_median_price_per_pair')
        idx = next(r for r in f['evidence'] if r['metric'] == 'price_position_index')
        self.assertTrue(brand['simulated'])
        self.assertFalse(comp['simulated'])
        self.assertEqual(comp['baseline_kind'], 'peer_band')
        self.assertAlmostEqual(idx['value'], round(brand['value'] / comp['value'] * 100, 1))
        self.assertLess(idx['value'], audit.PRICE_BAND[0])
        self.assertIn('below', f['sentence'])

    def test_offer_run_and_lookalike(self):
        r3 = [f for f in self.findings if f['rule_id'] == 'COMP-R03']
        self.assertEqual([f['entity']['id'] for f in r3], ['guarantee'])
        self.assertIn('Smartwool', r3[0]['sentence'])
        r4 = [f for f in self.findings if f['rule_id'] == 'COMP-R04']
        self.assertEqual(len(r4), 1)
        self.assertEqual(r4[0]['capability']['id'], 'MONEY-C48')

    def test_deterministic(self):
        self.assertEqual(json.dumps(audit.run('bombas', WINDOW)), json.dumps(self.findings))

    def test_sorted(self):
        keys = [audit.SEVERITY_ORDER[f['severity']] for f in self.findings]
        self.assertEqual(keys, sorted(keys))


class TestAuditEdits(TempBrain):
    def test_no_competitors_is_unavailable(self):
        self.edit('competitors', lambda rows: [r for r in rows if r['field'] in ('competitor_set',)])
        shutil.rmtree(self.tmp / 'bombas' / 'raw')
        out = audit.run('bombas', WINDOW, self.tmp)
        un = [f for f in out if f['status'] == 'unavailable']
        self.assertEqual({f['rule_id'] for f in un}, {'COMP-R01', 'COMP-R02', 'COMP-R03'})
        for f in un:
            self.assertEqual(f['evidence'], [])
            self.assertTrue(f['unavailable']['inputs'])
        self.assertFalse([f for f in out if f['rule_id'] == 'COMP-R04'])

    def test_raw_fallback(self):
        self.edit('competitors', lambda rows: [r for r in rows if r['field'] != 'stance'])
        names = [c['name'] for c in audit.market('bombas', dt.date(2026, 9, 28), self.tmp)['competitors']]
        self.assertIn('Stance', names)

    def test_claimed_angle_resolves(self):
        def add_giving(rows):
            for r in rows:
                if r['field'] == 'stance':
                    r['value']['hook_types'].append('giving back')
            return rows
        self.edit('competitors', add_giving)
        out = audit.run('bombas', WINDOW, self.tmp)
        self.assertNotIn('03-competitors.COMP-R01.angle_giving', {f['id'] for f in out})


class TestApi(TempBrain):
    def setUp(self):
        super().setUp()
        api.BRAIN_ROOT = self.tmp
        self.d = api.handle(Req(['overview']))

    def test_tiles_insights_chart(self):
        d = self.d
        self.assertEqual(len(d['tiles']), 3)
        self.assertEqual(d['tiles'][0]['value'], 5)
        self.assertEqual(d['tiles'][2]['value'], 67 + 29 + 331 + 699 + 608)
        self.assertEqual(len(d['insights']), 2)
        for i in d['insights']:
            self.assertTrue(i['rule'] and i['sentence'] and i['capability'])
        self.assertEqual(d['chart']['labels'][-1], 'Bombas')
        self.assertEqual(d['chart']['values'][-1], 23)
        self.assertEqual(len(d['chart']['labels']), len(d['chart']['values']))

    def test_notes_say_simulated_and_public(self):
        self.assertIn('simulated', self.d['simulated_note'])
        self.assertIn('public signals', self.d['simulated_note'])
        self.assertIn('Never copy', self.d['signal_note'])
        self.assertNotIn('GPT', json.dumps(self.d))

    def test_cards_and_board(self):
        for c in self.d['competitors']:
            self.assertFalse([k for k in c if k.startswith('_')])
            self.assertIn('giving', c['gap_to_own'])
        self.assertTrue(self.d['board'][-1]['brand'])
        self.assertEqual(self.d['lookalike']['links_to'], 'sockscool.com')
        self.assertNotIn('lookalike_page', [c['id'].split('.')[-1] for c in self.d['competitors']])

    def test_map_and_prices(self):
        pos = self.d['positioning']
        self.assertEqual(pos['split_x'], 25.0)
        brand = next(p for p in pos['points'] if p['brand'])
        self.assertTrue(brand['simulated'])
        for axis in ('durability', 'comfort'):
            placed = sum(len(q['competitors']) for q in pos['quadrants'][axis]['quadrants'])
            self.assertEqual(placed, 5)
        pr = self.d['prices']
        self.assertTrue(pr['available'])
        self.assertEqual(pr['month'], '2026-08')
        row = pr['rows'][0]
        self.assertEqual(set(row['cells']), {c['name'] for c in pr['competitors']})
        stance = row['cells']['Stance']
        self.assertAlmostEqual(stance['diff'], round(row['per_pair'] - 18.0, 2))

    def test_audit_route_and_errors(self):
        a = api.handle(Req(['audit']))
        self.assertTrue(a['findings'] and a['rules'])
        self.assertEqual(api.handle(Req(['nope']))[0], 404)
        self.assertEqual(api.handle(Req(['overview'], query={'brand': ['../x']}))[0], 400)
        self.assertEqual(api.handle(Req(['overview'], query={'brand': ['nobrand']}))[0], 404)


if __name__ == '__main__':
    unittest.main()
