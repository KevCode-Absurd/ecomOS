"""Screen 21-finance-cash: API shape, audit shape and determinism, rules firing on Bombas simulated data.

Tests that need order rows skip when app/data/brands/bombas/data.sqlite has not been built.
"""
import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / 'app' / 'screens' / '21-finance-cash'
BOMBAS_DB = ROOT / 'app' / 'data' / 'brands' / 'bombas' / 'data.sqlite'
AUDIT_KEYS = ['id', 'screen', 'rule_id', 'severity', 'entity', 'evidence', 'sentence', 'capability', 'money_at_stake',
              'confidence', 'brain_refs', 'first_seen', 'last_seen', 'status', 'unavailable']
EVIDENCE_KEYS = {'metric', 'value', 'unit', 'window', 'ends_on', 'freshness_days', 'baseline', 'baseline_kind',
                 'source', 'simulated'}
ROOM_RULES = ['FIN-R%02d' % i for i in range(1, 12)]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


api = load('finance_cash_api_test', SCREEN / 'api.py')
audit = api.audit


class Req:
    def __init__(self, path, brand='bombas', method='GET'):
        self.path, self.method, self.data, self._brand = path, method, None, brand

    def arg(self, name, default=None):
        return self._brand if name == 'brand' else default


class RulesTest(unittest.TestCase):
    def test_every_room_rule_is_listed(self):
        self.assertEqual([r['rule_id'] for r in audit.RULES], ROOM_RULES)
        for r in audit.RULES:
            self.assertEqual(r['owner_screen'], '21-finance-cash')
            self.assertEqual(r['capability'], audit.CAPABILITY[r['rule_id']]['id'])
            self.assertIn(audit.CAPABILITY[r['rule_id']]['autonomy'], ('agent_does', 'founder_gate', 'human_assist'))

    def test_bad_requests(self):
        self.assertEqual(api.handle(Req(['overview'], method='POST'))[0], 405)
        self.assertEqual(api.handle(Req(['overview'], brand='../x'))[0], 400)
        self.assertEqual(api.handle(Req(['nope']))[0], 404)


@unittest.skipUnless(BOMBAS_DB.is_file(), 'bombas data.sqlite not built')
class BombasTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.overview = api.handle(Req(['overview']))
        cls.findings = cls.overview['findings']

    def test_api_shape(self):
        o = self.overview
        for k in ('brand', 'window', 'tiles', 'insights', 'chart', 'ladder', 'skus', 'channels', 'cash', 'findings', 'rules'):
            self.assertIn(k, o)
        self.assertTrue(o['brand']['simulated'])
        self.assertEqual(sorted(o['tiles']), ['contribution', 'gross', 'mer'])
        for t in o['tiles'].values():
            self.assertIsNotNone(t['value'], t)
            self.assertTrue(t['sources'])
        self.assertEqual(len(o['insights']), 2)
        for i in o['insights']:
            self.assertTrue(i['rule'] and i['sentence'] and i['capability'])
        c = o['chart']
        self.assertEqual(len(c['labels']), len(c['gross_margin']))
        self.assertEqual(len(c['labels']), len(c['cm3_rate']))
        json.dumps(o)

    def test_ladder_adds_up(self):
        rows = {r['line']: r['usd'] for r in self.overview['ladder']['rows']}
        cm1 = rows['Net revenue'] + rows['Product cost (COGS)'] + rows['Payment fees']
        self.assertAlmostEqual(cm1, rows['CM1'], delta=5)
        cm2 = rows['CM1'] + rows['Shipping charged'] + rows['Fulfillment'] + rows['Returns and chargebacks']
        self.assertAlmostEqual(cm2, rows['CM2'], delta=5)
        self.assertAlmostEqual(rows['CM2'] + rows['Paid media'], rows['CM3'], delta=5)

    def test_unavailable_months_read_none(self):
        rd = audit.Reader(None, 'bombas', audit.last_full_day(None, 'bombas'))
        months = {m['month']: m for m in audit.margin_months(rd)}
        for m in ('2024-10', '2024-11', '2024-12'):  # cost rows start 2025-01-01
            self.assertIsNone(months[m]['cogs'])
            self.assertIsNone(months[m]['gross_margin'])
            self.assertTrue(months[m]['reason'])
        self.assertIsNotNone(months['2025-01']['gross_margin'])
        pnl = {m['month']: m for m in audit.pnl_months(rd)}
        self.assertIsNone(pnl['2024-11']['web_cm3'])
        self.assertIsNone(pnl['2024-11']['web_cm3_rate'])
        self.assertIsNone(pnl['2025-06']['pos_cm2_rate'])  # no card fee rows for retail
        self.assertIn('2024-11', self.overview['chart']['unavailable_months'])

    def test_audit_shape(self):
        self.assertTrue(self.findings)
        for f in self.findings:
            self.assertEqual(list(f)[:len(AUDIT_KEYS)], AUDIT_KEYS)
            self.assertIn(f['severity'], ('critical', 'high', 'medium', 'low'))
            self.assertEqual(f['id'], f"21-finance-cash.{f['rule_id']}.{f['entity']['id']}")
            self.assertIn(f['status'], ('open', 'unavailable'))
            self.assertTrue(0.1 <= f['confidence'] <= 1)
            for e in f['evidence']:
                self.assertEqual(set(e), EVIDENCE_KEYS)
                self.assertTrue(e['simulated'])
            if f['money_at_stake'] is None:
                self.assertTrue(f['money_reason'])
            else:
                self.assertGreaterEqual(f['money_at_stake']['usd'], 0)
                self.assertTrue(f['money_at_stake']['formula'])
            if f['status'] == 'unavailable':
                self.assertEqual(f['evidence'], [])
                self.assertEqual(set(f['unavailable']), {'inputs', 'connector', 'fix'})
        order = [audit.SEVERITY_ORDER[f['severity']] for f in self.findings]
        self.assertEqual(order, sorted(order))

    def test_audit_deterministic(self):
        a = audit.run('bombas')
        b = audit.run('bombas')
        self.assertEqual(json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True))

    def test_rules_fire_on_bombas(self):
        leaks = [f for f in self.findings if f['rule_id'] == 'FIN-R01' and f['status'] == 'open']
        self.assertTrue(leaks)
        for f in leaks:
            m = f['money_at_stake']
            i = m['inputs']
            loss = (i['units'] * (i['per_unit_ops'] + i['paid_per_unit']) + i['net_sales'] * i['revenue_cost_rate']
                    + i['cogs'] - i['net_sales'])
            self.assertAlmostEqual(loss, m['usd'], delta=1)
        self.assertNotIn('FIN-R07', {f['rule_id'] for f in self.findings})  # COD: markets IN only
        self.assertNotIn('FIN-R09', {f['rule_id'] for f in self.findings})  # no subscription table

    def test_no_em_dashes(self):
        texts = [f['sentence'] for f in self.findings] + [i['sentence'] for i in self.overview['insights']]
        texts += [t['plain'] for t in self.overview['tiles'].values()]
        for s in texts:
            self.assertNotIn('—', s)
            self.assertNotIn('–', s)
        for f in self.findings:
            self.assertLessEqual(len(f['sentence'].split()), 40, f['sentence'])


if __name__ == '__main__':
    unittest.main()
