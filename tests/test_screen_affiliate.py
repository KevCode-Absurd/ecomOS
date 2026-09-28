"""Screen 13-affiliate-marketplace-ads: the fraud and coupon-leak rules on fed rows, and the api and audit on Bombas."""
import importlib.util
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / 'app' / 'screens' / '13-affiliate-marketplace-ads'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


api = load('affm_api_test', FOLDER / 'api.py')
audit = load('affm_audit_test', FOLDER / 'audit.py')

FIELDS = ['id', 'screen', 'rule_id', 'severity', 'entity', 'evidence', 'sentence', 'capability', 'money_at_stake',
          'confidence', 'brain_refs', 'first_seen', 'last_seen', 'status', 'unavailable']
EVIDENCE = {'metric', 'value', 'unit', 'window', 'ends_on', 'freshness_days', 'baseline', 'baseline_kind', 'source', 'simulated'}
WIN = api.Win(date(2026, 9, 27), 28)


def click(aff, order=None, click_at='2026-09-10T10:00:00', order_at=None, amount=50.0, ptype='content'):
    return {'affiliate_id': aff, 'partner_type': ptype, 'click_at': click_at, 'order_id': order,
            'order_at': order_at, 'amount': amount if order else None}


class Rules(unittest.TestCase):
    def test_orders_with_no_clicks_are_flagged(self):
        rows = [click('A', f'o{i}', click_at=None, order_at='2026-09-12T10:00:00') for i in range(3)]
        rows += [click('B', 'p1', order_at='2026-09-10T11:00:00'), click('B')]
        parts = api.partners(rows, {'A': {'rate': 0.1}}, WIN)
        flagged = api.no_click_affiliates(parts)
        self.assertEqual([p['affiliate_id'] for p in flagged], ['A'])
        a = next(p for p in parts if p['affiliate_id'] == 'A')
        self.assertEqual(a['commission'], 15.0)
        b = next(p for p in parts if p['affiliate_id'] == 'B')
        self.assertIsNone(b['commission'])  # no rate on file: unavailable, never 0

    def test_fast_click_to_order_is_flagged(self):
        rows = [click('F', f'f{i}', click_at='2026-09-10T10:00:00', order_at='2026-09-10T10:00:05') for i in range(3)]
        p = api.partners(rows, {}, WIN)[0]
        self.assertEqual(p['fast_orders'], 3)
        self.assertTrue(any('under 10s' in f for f in p['flags']))

    def test_coupon_leak_needs_volume_and_share(self):
        events = [click('C', f'o{i}', order_at='2026-09-11T10:00:00') for i in range(6)]
        red = [{'code': 'CARL15', 'affiliate_id': 'C', 'redeemed_at': '2026-09-11', 'order_id': f'o{i}', 'amount': 40.0}
               for i in range(10)]
        leaks = api.coupon_leaks(red, events, WIN)
        self.assertEqual(len(leaks), 1)
        self.assertEqual(leaks[0]['leaked'], 4)
        self.assertEqual(leaks[0]['leaked_sales'], 160.0)
        self.assertEqual(api.coupon_leaks(red[:9], events, WIN), [])  # under 10 redemptions: not read

    def test_chart_unavailable_is_null_not_zero(self):
        c = api.orders_by_type(None, date(2026, 9, 27))
        self.assertEqual(len(c['labels']), 12)
        self.assertEqual(c['labels'][-1], '2026-09')
        self.assertTrue(all(v is None for s in c['series'] for v in s['values']))
        self.assertTrue(c['unavailable'])

    def test_listing_price(self):
        self.assertEqual(api.listing_price('$34.92 (shown 2026-09-28)'), 34.92)
        self.assertIsNone(api.listing_price(None))

    def test_rules_list_the_contract_fields(self):
        for r in audit.RULES:
            for k in ('rule_id', 'name', 'entity_type', 'inputs', 'capability', 'owner_screen'):
                self.assertIn(k, r)


class Bombas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out = api.build('bombas')
        cls.findings = audit.run('bombas')

    def test_screen_is_simulated_and_has_three_tiles(self):
        self.assertTrue(self.out['simulated'])
        self.assertEqual(len(self.out['tiles']), 3)

    def test_missing_tables_read_unavailable_with_a_connector(self):
        t = {x['id']: x for x in self.out['tiles']}
        self.assertIsNone(t['affiliate_orders']['value'])
        self.assertIsNone(t['amazon_acos']['value'])
        self.assertTrue(t['affiliate_orders']['fix'])
        self.assertTrue(self.out['partners']['unavailable'])
        self.assertTrue(self.out['billing']['unavailable'])
        for l in self.out['amazon']['listings']:
            self.assertIsNone(l['acos'])

    def test_amazon_sample_from_the_brain(self):
        a = self.out['amazon']
        self.assertEqual(a['asins_read'], 8)
        self.assertEqual(a['in_stock'], 4)
        self.assertEqual(a['reseller_share'], 1.0)

    def test_findings_follow_the_contract(self):
        ids = {f['rule_id']: f for f in self.findings}
        self.assertEqual(ids['AFFM-R04']['status'], 'open')
        self.assertEqual(ids['AFFM-R01']['status'], 'unavailable')
        self.assertTrue(ids['AFFM-R01']['unavailable']['connector'])
        for f in self.findings:
            self.assertEqual(list(f)[:len(FIELDS)], FIELDS)
            self.assertLessEqual(len(f['sentence'].split()), 40)
            self.assertNotIn('—', f['sentence'])
            for e in f['evidence']:
                self.assertTrue(EVIDENCE <= set(e))
        self.assertEqual(self.findings, audit.run('bombas'))  # deterministic


if __name__ == '__main__':
    unittest.main()
