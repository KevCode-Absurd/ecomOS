"""Screen 01-market-research: the products metric, audit rules, API shape, and the page on Bombas data.

Synthetic tests build a tiny catalog in memory so the declining-line and review rules are proven to fire
and to stay quiet. The Bombas tests skip when app/data/brands/bombas/data.sqlite has not been built.
"""
import importlib.util
import json
import sys
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / 'app' / 'screens' / '01-market-research'
BOMBAS_DB = ROOT / 'app' / 'data' / 'brands' / 'bombas' / 'data.sqlite'
AUDIT_KEYS = ['id', 'screen', 'rule_id', 'severity', 'entity', 'evidence', 'sentence', 'capability', 'money_at_stake',
              'confidence', 'brain_refs', 'first_seen', 'last_seen', 'status', 'unavailable']
EVIDENCE_KEYS = {'metric', 'value', 'unit', 'window', 'ends_on', 'freshness_days', 'baseline', 'baseline_kind',
                 'source', 'simulated'}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


api = load('market_research_api_test', SCREEN / 'api.py')
audit = api.audit
metrics = audit.metrics()


class FakeData:
    """Two lines over 25 months. The store grows 20 percent a year; Tee grows `tee_growth`."""

    def __init__(self, tee_growth=0.2, with_products=True):
        self.brand = {'brand': 'fake', 'name': 'Fake', 'as_of': '2026-09-27', 'simulated': True}
        rows = []
        for i in range(25):
            y, m = 2024 + (8 + i) // 12, (8 + i) % 12 + 1
            month = f'{y}-{m:02d}'
            year = 1 if month >= '2025-09' else 0
            sock = round(1000 * (1.2 ** year))
            tee = round(200 * ((1 + tee_growth) ** year))
            rows.append({'month': month, 'sku': 'S-1', 'category': 'socks', 'units': sock, 'net_sales': sock * 10.0})
            rows.append({'month': month, 'sku': 'S-3', 'category': 'socks', 'units': sock, 'net_sales': sock * 25.0})
            rows.append({'month': month, 'sku': 'T-1', 'category': 'tshirts', 'units': tee, 'net_sales': tee * 30.0})
        self.tables = {'products_monthly': rows}
        if with_products:
            self.tables['products'] = [
                {'sku': 'S-1', 'title': 'Crew Sock', 'category': 'socks', 'price': 10.0, 'items_per_unit': 1},
                {'sku': 'S-3', 'title': 'Crew Sock 3-Pack', 'category': 'socks', 'price': 27.0, 'items_per_unit': 3},
                {'sku': 'T-1', 'title': 'Tee', 'category': 'tshirts', 'price': 30.0, 'items_per_unit': 1}]

    def table(self, name):
        if name not in self.tables:
            raise KeyError(name)
        return self.tables[name]

    def meta(self, name):
        return {'source': 'test', 'captured_at': '2026-09-28T06:00:00Z'}


def review(key, line, total, low, rating=4.5):
    return {'key': key, 'line': line, 'record': f'fake.products.reviews_{key}', 'product': line, 'pdp': None,
            'reviews': total, 'rating': rating, 'low_star': low, 'low_star_share': round(low / total, 4),
            'praise': ['soft'], 'issues': ['hard to pull on', 'rolls down'], 'captured_at': '2026-09-20'}


class MetricTest(unittest.TestCase):
    def test_units_by_line_whole_months(self):
        r = metrics.compute('units', FakeData(), window='92d', end='2026-08-31', by='line')
        self.assertFalse(r['unavailable'])
        self.assertEqual(r['months'], ['2026-06', '2026-07', '2026-08'])
        lines = {g['line']: g for g in r['groups']}
        self.assertEqual(set(lines), {'Crew Sock', 'Tee'})
        self.assertEqual(lines['Crew Sock']['units'], 3 * 2 * 1200)
        self.assertEqual(r['value'], sum(g['units'] for g in r['groups']))

    def test_line_falls_back_to_category(self):
        r = metrics.compute('units', FakeData(with_products=False), window='92d', end='2026-08-31', by='line')
        self.assertEqual({g['line'] for g in r['groups']}, {'socks', 'tshirts'})

    def test_no_whole_month_is_unavailable_not_zero(self):
        r = metrics.compute('product_net_sales', FakeData(), window='10d')
        self.assertTrue(r['unavailable'])
        self.assertIsNone(r['value'])

    def test_missing_table_is_unavailable(self):
        d = FakeData()
        del d.tables['products_monthly']
        self.assertTrue(metrics.compute('units', d, window='92d', end='2026-08-31')['unavailable'])


class RulesTest(unittest.TestCase):
    def check_shape(self, f):
        self.assertEqual(list(f)[:len(AUDIT_KEYS)], AUDIT_KEYS)
        self.assertIn(f['severity'], ('critical', 'high', 'medium', 'low'))
        self.assertTrue(f['id'].startswith('01-market-research.' + f['rule_id'] + '.'))
        for e in f['evidence']:
            self.assertTrue(EVIDENCE_KEYS <= set(e), e)
        if f['money_at_stake'] is None:
            self.assertTrue(f.get('money_reason'))
        else:
            self.assertGreaterEqual(f['money_at_stake']['usd'], 0)
            self.assertTrue(f['money_at_stake']['formula'])

    def test_declining_line_fires_with_money(self):
        fs = [f for f in audit.run(None, data=FakeData(tee_growth=0.05)) if f['rule_id'] == 'PROD-R01']
        self.assertEqual(len(fs), 1)
        f = fs[0]
        self.check_shape(f)
        self.assertEqual(f['entity']['id'], 'tee')
        self.assertIn('losing share', f['sentence'])
        inp = f['money_at_stake']['inputs']
        expect = round(round((inp['store_growth'] - inp['line_growth']) * inp['units_year_ago']) * inp['net_per_unit'])
        self.assertEqual(f['money_at_stake']['usd'], expect)
        self.assertEqual(f['severity'], 'high')  # 3 of 3 months trailed the store

    def test_units_down_says_down(self):
        f = next(f for f in audit.run(None, data=FakeData(tee_growth=-0.3)) if f['rule_id'] == 'PROD-R01')
        self.assertIn('down 30.0 percent', f['sentence'])

    def test_no_false_positive(self):
        self.assertFalse([f for f in audit.run(None, data=FakeData()) if f['rule_id'] == 'PROD-R01'])

    def test_no_brain_makes_review_rule_unavailable(self):
        f = next(f for f in audit.run(None, data=FakeData()) if f['rule_id'] == 'PROD-R02')
        self.assertEqual(f['status'], 'unavailable')
        self.assertEqual(f['evidence'], [])
        self.assertIsNone(f['money_at_stake'])

    def test_review_issue_fires_with_money(self):
        data = FakeData()
        rd = audit.Reader(data, None, date(2026, 9, 27))
        tr = audit.trend(rd)
        reviews = [review('crew', 'Crew Sock', 1000, 40), review('a', None, 1000, 50), review('b', None, 1000, 60),
                   review('tee', 'Tee', 1000, 200, rating=4.0)]
        lads = [{'id': 'fake.objection_ladders.fit', 'theme': 'fit', 'what_works': [], 'what_fails': [], 'one_star': 5,
                 'five_star': 1, 'reviews_records': ['fake.products.reviews_tee'],
                 'rungs': [{'level': 1, 'doubt': 'will it fit', 'one_star': 5, 'five_star': 1, 'proof': False,
                            'from_reviews': ['fake.products.reviews_tee']}]}]
        fs = audit.review_findings(reviews, lads, rd, tr, date(2026, 9, 27), None)
        self.assertEqual([f['entity']['id'] for f in fs], ['tee'])
        f = fs[0]
        self.check_shape(f)
        self.assertIn('fake.objection_ladders.fit', f['brain_refs'])
        self.assertTrue(any(e.get('rung') == 'fit.level_1' for e in f['evidence']))
        inp = f['money_at_stake']['inputs']
        self.assertEqual(inp['net_sales_last_month'], 240 * 30.0)
        self.assertEqual(f['money_at_stake']['usd'], round(inp['net_sales_last_month'] * (0.2 - 0.055)))

    def test_deterministic(self):
        d = FakeData(tee_growth=0.05)
        self.assertEqual(json.dumps(audit.run(None, data=d)), json.dumps(audit.run(None, data=d)))

    def test_rules_list(self):
        self.assertEqual({r['rule_id'] for r in audit.RULES}, {'PROD-R01', 'PROD-R02'})
        for r in audit.RULES:
            self.assertEqual(r['owner_screen'], '01-market-research')


class Req:
    def __init__(self, path, brand='bombas', method='GET'):
        self.method, self.path, self.query, self.data = method, path, {'brand': [brand]}, None

    def arg(self, name, default=None):
        v = self.query.get(name)
        return v[0] if v else default


class ApiTest(unittest.TestCase):
    def test_read_only_and_bad_brand(self):
        self.assertEqual(api.handle(Req(['overview'], method='POST'))[0], 405)
        self.assertEqual(api.handle(Req(['overview'], brand='../x'))[0], 400)
        self.assertEqual(api.handle(Req(['nope']))[0], 404)

    def test_competitor_band_parsing(self):
        class B:
            def records(self, section):
                return [{'id': 'x.competitors.a', 'value': {'name': 'A', 'price_band_usd': '12 to 25 per pair, median about 18'}},
                        {'id': 'x.competitors.b', 'value': {'name': 'B', 'price_band_usd': 'from 18 per pair, median 25'}},
                        {'id': 'x.competitors.set', 'value': ['A', 'B']}]
        c = api.competitor_bands(B())
        self.assertEqual([(x['low'], x['high'], x['median']) for x in c], [(12.0, 25.0, 18.0), (18.0, None, 25.0)])

    def test_price_position(self):
        comps = [{'median': 18.0}, {'median': 32.0}]
        rows = {r['line']: r for r in api.price_bands(FakeData().tables['products'], comps)['rows']}
        self.assertEqual(rows['Crew Sock']['position'], 'below')
        self.assertIsNone(rows['Tee']['position'])  # no competitor for tees


@unittest.skipUnless(BOMBAS_DB.is_file(), 'bombas data.sqlite not built')
class BombasTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.o = api.handle(Req(['overview']))

    def test_simulated_and_three_tiles(self):
        o = self.o
        self.assertTrue(o['brand']['simulated'])
        self.assertEqual(set(o['tiles']), {'units', 'losing', 'rating'})
        for t in o['tiles'].values():
            self.assertIsNotNone(t['value'])

    def test_two_insights_one_chart(self):
        o = self.o
        self.assertEqual(len(o['insights']), 2)
        for i in o['insights']:
            self.assertTrue(i['rule'] and i['sentence'])
            self.assertNotIn('—', i['sentence'])
        self.assertEqual(len(o['chart']['labels']), 12)
        self.assertLessEqual(len(o['chart']['series']), 6)

    def test_findings_have_decline_and_review_with_money(self):
        fs = self.o['findings']
        rules = {f['rule_id'] for f in fs if f['status'] == 'open' and f['money_at_stake']}
        self.assertEqual(rules, {'PROD-R01', 'PROD-R02'})
        for f in fs:
            self.assertEqual(list(f)[:len(AUDIT_KEYS)], AUDIT_KEYS)
        r2 = next(f for f in fs if f['rule_id'] == 'PROD-R02')
        self.assertTrue(any('.objection_ladders.' in b for b in r2['brain_refs']))

    def test_demand_prices_reviews_pipeline(self):
        o = self.o
        self.assertEqual(len(o['demand']), 13)
        self.assertTrue(o['price_bands']['band'])
        self.assertTrue(o['reviews'] and all(r['works'] is not None for r in o['reviews']))
        self.assertEqual(o['pipeline']['rows'], [])
        self.assertTrue(o['pipeline']['gate_rule'])

    def test_page_says_simulated(self):
        js = (SCREEN / 'screen.js').read_text(encoding='utf-8')
        self.assertIn('simulated data', js)
        self.assertNotIn('—', js)


if __name__ == '__main__':
    unittest.main()
