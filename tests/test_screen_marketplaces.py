"""Screen 20-marketplaces: api shape, audit shape and determinism, rules fire on Bombas, plain writing."""
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / 'app' / 'screens' / '20-marketplaces'


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, FOLDER / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


API = load('test_mkt_api', 'api.py')
AUDIT = load('test_mkt_audit', 'audit.py')
FIELDS = ['id', 'screen', 'rule_id', 'severity', 'entity', 'evidence', 'sentence', 'capability', 'money_at_stake',
          'confidence', 'brain_refs', 'first_seen', 'last_seen', 'status', 'unavailable']
EV_FIELDS = {'metric', 'value', 'unit', 'window', 'ends_on', 'freshness_days', 'baseline', 'baseline_kind', 'source',
             'simulated'}


class ApiShape(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = API.build('bombas')

    def test_top_level(self):
        d = self.d
        self.assertFalse(d['unavailable'])
        self.assertTrue(d['simulated'])
        for key in ('tiles', 'chart', 'listings', 'trust_ladder', 'connectors', 'as_of', 'window'):
            self.assertIn(key, d)

    def test_three_tiles(self):
        tiles = self.d['tiles']
        self.assertEqual(len(tiles), 3)
        for t in tiles:
            self.assertIn('simulated', t)
            if t['value'] is None:
                self.assertTrue(t['unavailable_reason'])
        share = next(t for t in tiles if t['id'] == 'marketplace_share')['value']
        self.assertTrue(0.05 < share < 0.12)  # founder calibration: 8 percent

    def test_chart(self):
        c = self.d['chart']
        self.assertEqual(len(c['labels']), API.CHART_MONTHS)
        self.assertTrue(all(len(s['values']) == API.CHART_MONTHS for s in c['series']))
        self.assertIn('Amazon', [s['name'] for s in c['series']])

    def test_listings_from_brain(self):
        rows = self.d['listings']['rows']
        self.assertGreaterEqual(len(rows), 20)
        self.assertEqual(len({r['asin'] for r in rows}), len(rows))

    def test_missing_tables_are_not_zero(self):
        settle = next(c for c in self.d['connectors'] if c['table'] == 'settlement_reports')
        self.assertFalse(settle['connected'])
        self.assertTrue(settle['fix'])

    def test_unknown_brand(self):
        self.assertTrue(API.build('no_such_brand_xyz')['unavailable'])

    def test_bad_window(self):
        with self.assertRaises(ValueError):
            API.parse_days('3d')


class AuditShape(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.f = AUDIT.run('bombas')

    def test_contract_fields(self):
        for f in self.f:
            for key in FIELDS:
                self.assertIn(key, f)
            self.assertIn(f['severity'], ('critical', 'high', 'medium', 'low'))
            self.assertIn(f['status'], ('open', 'unavailable'))
            self.assertIn(f['capability']['autonomy'], ('agent_does', 'founder_gate', 'human_assist'))
            self.assertTrue(f['id'].startswith('20-marketplaces.' + f['rule_id'] + '.'))
            self.assertTrue(0.1 <= f['confidence'] <= 1)
            for row in f['evidence']:
                self.assertTrue(EV_FIELDS <= set(row))
            if f['money_at_stake'] is None:
                self.assertTrue(f.get('money_reason'))
            if f['status'] == 'unavailable':
                self.assertEqual(f['evidence'], [])
                self.assertTrue(f['unavailable']['fix'])

    def test_every_room_rule_is_accounted_for(self):
        ids = {f['rule_id'] for f in self.f}
        self.assertEqual(len(AUDIT.TABLE_RULES), 13)
        for rid in AUDIT.TABLE_RULES:
            self.assertIn(rid, ids)

    def test_rules_fire_on_bombas(self):
        fired = {f['rule_id'] for f in self.f if f['status'] == 'open'}
        self.assertTrue({'MKT-R14', 'MKT-R15', 'MKT-R16'} <= fired, fired)

    def test_deterministic(self):
        self.assertEqual(self.f, AUDIT.run('bombas'))

    def test_sorted(self):
        order = [AUDIT.SEV_ORDER[f['severity']] for f in self.f]
        self.assertEqual(order, sorted(order))

    def test_future_window_refused(self):
        with self.assertRaises(ValueError):
            AUDIT.run('bombas', {'ends_on': '2099-01-01'})

    def test_writing(self):
        for f in self.f:
            s = f['sentence']
            self.assertNotIn('—', s)
            self.assertNotIn('–', s)
            self.assertLess(len(s.split()), 40, s)
            for word in ('should', 'try ', 'consider'):
                self.assertNotIn(word, s.lower())
        for t in API.build('bombas')['tiles']:
            self.assertNotIn('—', t['plain'] + t['name'])

    def test_page_files_have_no_em_dash(self):
        for name in ('index.html', 'screen.js', 'api.py', 'audit.py'):
            self.assertNotIn('—', (FOLDER / name).read_text(encoding='utf-8'), name)


class PureRules(unittest.TestCase):
    def test_share_drop_money_in_code(self):
        months = ('2026-03', '2026-04', '2026-05', '2026-06', '2026-07')
        rows = [{'month': m, 'marketplace': 'amazon', 'net_sales': v} for m, v in zip(months, (100, 100, 100, 100, 60))]
        out = API.share_drops(rows, {m: 1000.0 for m in months}, '2026-07')
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]['stake'], 40.0)  # (0.10 - 0.06) x 1000
        self.assertEqual(out[0]['windows_below'], 4)

    def test_share_drop_needs_full_history(self):
        rows = [{'month': '2026-07', 'marketplace': 'amazon', 'net_sales': 1}]
        self.assertEqual(API.share_drops(rows, {'2026-07': 10.0}, '2026-07'), [])

    def test_rating_outlier(self):
        ls = [{'asin': str(i), 'stars': 4.6, 'ratings': 50} for i in range(5)]
        ls += [{'asin': 'x', 'stars': 4.1, 'ratings': 50}, {'asin': 'y', 'stars': 3.0, 'ratings': 2}]
        self.assertEqual([o['asin'] for o in API.rating_outliers(ls)], ['x'])  # y has under 5 ratings


if __name__ == '__main__':
    unittest.main()
