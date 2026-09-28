"""Screen 22-measurement: audit rules, API shape and the page on Bombas simulated data.

The Bombas tests skip when app/data/brands/bombas/data.sqlite has not been built. The empty-brand test
proves that missing tables read unavailable, never 0.
"""
import importlib.util
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / 'app' / 'screens' / '22-measurement'
BOMBAS_DB = ROOT / 'app' / 'data' / 'brands' / 'bombas' / 'data.sqlite'
AUDIT_KEYS = ['id', 'screen', 'rule_id', 'severity', 'entity', 'evidence', 'sentence', 'capability', 'money_at_stake',
              'confidence', 'brain_refs', 'first_seen', 'last_seen', 'status', 'unavailable']
EVIDENCE_KEYS = {'metric', 'value', 'unit', 'window', 'ends_on', 'freshness_days', 'baseline', 'baseline_kind',
                 'source', 'simulated'}
ENTITY_TYPES = {'brand', 'stage', 'page', 'device', 'sku', 'campaign', 'adset', 'ad', 'flow', 'offer', 'ladder_rung', 'metric'}
EM_DASH = '—'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


api = load('measurement_api_test', SCREEN / 'api.py')
audit = api.audit


class Req:
    def __init__(self, path, method='GET', **args):
        self.path, self.method, self.args, self.data = path, method, args, None

    def arg(self, name, default=None):
        return self.args.get(name, default)


class EmptyBrand:
    """A brand with no tables connected at all."""
    brand = {'brand': 'empty', 'as_of': '2026-09-27', 'simulated': True}

    def table(self, name):
        raise KeyError(name)

    def _sql(self, query):
        raise KeyError('data.sqlite')


def strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from strings(v)


class TestRules(unittest.TestCase):
    def test_every_rule_has_capability_and_owner(self):
        ids = [r['rule_id'] for r in audit.RULES]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(ids), 16)
        for r in audit.RULES:
            self.assertRegex(r['rule_id'], r'^MEAS-R\d\d$')
            self.assertEqual(r['owner_screen'], '22-measurement')
            self.assertTrue(r['capability'] and r['inputs'] and r['job'])
            self.assertIn(r['entity_type'], ENTITY_TYPES)
            self.assertIn(r['rule_id'], audit.__doc__)

    def test_room_jobs_covered(self):
        caps = {r['capability'] for r in audit.RULES}
        for c in ('MONEY-C20', 'MONEY-C21', 'MONEY-C22', 'MONEY-C23', 'MONEY-C24', 'BRN-C06', 'BRN-C02', 'DIAG-C01',
                  'MONEY-C30', 'MONEY-C63', 'LIFE-C12', 'MONEY-C65'):
            self.assertIn(c, caps)

    def test_empty_brand_reads_unavailable_never_zero(self):
        rd = audit.Reader(EmptyBrand(), None, audit.last_full_day(EmptyBrand(), None))
        ws = audit.windows(rd)
        self.assertIsNone(ws[0]['store'])
        self.assertIsNone(audit.mer(ws[0]))
        self.assertIsNone(audit.capture(ws[0]))
        self.assertIsNone(audit.overlap(ws[0]))
        findings = audit.run(None, None, data=EmptyBrand())
        self.assertTrue(findings)
        for f in findings:
            self.assertNotEqual(f['status'], 'resolved')
            if f['status'] == 'unavailable':
                self.assertEqual(f['evidence'], [])
                self.assertIsNone(f['money_at_stake'])
                self.assertTrue(f['unavailable']['inputs'] and f['unavailable']['fix'])
        tiles = api.tiles(ws, '2026-09-27')
        for t in tiles.values():
            self.assertIsNone(t['value'])
            self.assertTrue(t['unavailable_reason'])


@unittest.skipUnless(BOMBAS_DB.is_file(), 'bombas data.sqlite not built')
class TestBombas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.overview = api.overview(None, 'bombas')
        cls.findings = cls.overview['findings']

    def test_api_shape(self):
        d = self.overview
        for k in ('brand', 'window', 'tiles', 'insights', 'reconciliation', 'trust', 'incrementality', 'chart', 'findings', 'rules'):
            self.assertIn(k, d)
        self.assertTrue(d['brand']['simulated'])
        self.assertEqual(sorted(d['tiles']), ['capture', 'mer', 'overlap'])
        for t in d['tiles'].values():
            self.assertIsInstance(t['value'], float)
            self.assertTrue(t['formula'] and t['plain'])
        self.assertEqual(len(d['insights']), 2)
        for i in d['insights']:
            self.assertTrue(i['sentence'] and i['rule'])
        self.assertEqual(len(d['chart']['labels']), api.CHART_DAYS)
        self.assertEqual(len(d['chart']['series']), 4)
        for s in d['chart']['series']:
            self.assertEqual(len(s['values']), api.CHART_DAYS)
        for row in d['incrementality']:
            self.assertIsNone(row['lift'])
            self.assertEqual(row['status'], 'unavailable')
            self.assertTrue(row['test'])
        self.assertIn(d['trust']['status'], ('pass', 'warn', 'fail'))

    def test_handle_routes(self):
        self.assertEqual(api.handle(Req(['nope']))[0], 404)
        self.assertEqual(api.handle(Req(['overview'], method='POST'))[0], 405)
        self.assertEqual(api.handle(Req(['overview'], brand='../x'))[0], 400)
        out = api.handle(Req(['findings'], brand='bombas'))
        self.assertEqual(out['findings'], self.findings)

    def test_period_roas_and_mer_from_totals(self):
        rec = self.overview['reconciliation']
        t = rec['total']
        self.assertAlmostEqual(t['period_roas'], round(t['claimed_value'] / t['spend'], 4))
        rows = {r['source']: r for r in rec['rows']}
        self.assertAlmostEqual(t['spend'], round(rows['Meta']['spend'] + rows['Google']['spend'], 2), places=1)
        m = self.overview['tiles']['mer']
        self.assertAlmostEqual(m['value'], round(m['inputs']['net_revenue'] / m['inputs']['spend'], 4))
        self.assertAlmostEqual(m['inputs']['spend'], sum(m['inputs']['spend_by_platform'].values()), places=1)
        self.assertGreater(len(m['inputs']['spend_by_platform']), 2)  # breakdown kept apart from the total
        # The total is not an average of the rows' ROAS.
        self.assertNotAlmostEqual(t['period_roas'], (rows['Meta']['roas'] + rows['Google']['roas']) / 2, places=3)

    def test_audit_contract_shape(self):
        self.assertTrue(self.findings)
        for f in self.findings:
            self.assertEqual(list(f)[:len(AUDIT_KEYS)], AUDIT_KEYS)
            self.assertEqual(f['screen'], '22-measurement')
            self.assertEqual(f['id'], f'22-measurement.{f["rule_id"]}.{f["entity"]["id"]}')
            self.assertIn(f['severity'], ('critical', 'high', 'medium', 'low'))
            self.assertIn(f['entity']['type'], ENTITY_TYPES)
            self.assertIn(f['capability']['autonomy'], ('agent_does', 'founder_gate', 'human_assist'))
            self.assertEqual(f['capability']['id'], audit.CAPABILITY[f['rule_id']][0])
            self.assertTrue(0.1 <= f['confidence'] <= 1)
            self.assertIn(f['status'], ('open', 'unavailable'))
            for e in f['evidence']:
                self.assertTrue(EVIDENCE_KEYS <= set(e))
                self.assertTrue(e['simulated'])
            if f['money_at_stake'] is None:
                self.assertTrue(f.get('money_reason'))
            else:
                self.assertGreaterEqual(f['money_at_stake']['usd'], 0)
                self.assertTrue(f['money_at_stake']['formula'] and f['money_at_stake']['inputs'])
        order = [(audit.SEVERITY_ORDER[f['severity']]) for f in self.findings]
        self.assertEqual(order, sorted(order))
        self.assertEqual(len({f['id'] for f in self.findings}), len(self.findings))

    def test_deterministic(self):
        a = json.dumps(audit.run('bombas'), sort_keys=True)
        b = json.dumps(audit.run('bombas', {'ends_on': '2026-09-27'}), sort_keys=True)
        self.assertEqual(a, b)

    def test_rules_fire_on_bombas(self):
        fired = {f['rule_id'] for f in self.findings if f['status'] == 'open'}
        for r in ('MEAS-R01', 'MEAS-R03', 'MEAS-R06'):
            self.assertIn(r, fired)
        staked = [f for f in self.findings if f['money_at_stake']]
        self.assertTrue(staked)

    def test_ga4_money_recomputes(self):
        f = next(x for x in self.findings if x['rule_id'] == 'MEAS-R01')
        i = f['money_at_stake']['inputs']
        self.assertEqual(f['money_at_stake']['usd'],
                         round((i['capture_target'] - i['ga4_capture']) * i['store_web_orders'] * i['aov']))
        cap = self.overview['tiles']['capture']
        self.assertAlmostEqual(cap['value'], round(cap['inputs']['ga4_purchases'] / cap['inputs']['store_web_orders'], 4))

    def test_utm_money_recomputes(self):
        for f in (x for x in self.findings if x['rule_id'] == 'MEAS-R03' and x['status'] == 'open'):
            i = f['money_at_stake']['inputs']
            self.assertEqual(f['money_at_stake']['usd'], round((1 - i['utm_compliance']) * i['platform_spend_28d']))

    def test_incrementality_unavailable_names_test(self):
        inc = [f for f in self.findings if f['rule_id'] == 'MEAS-R13']
        self.assertTrue(inc)
        for f in inc:
            self.assertEqual(f['status'], 'unavailable')
            self.assertIn('Test to run', f['sentence'])

    def test_no_em_dashes_and_short_sentences(self):
        for s in strings(self.overview):
            self.assertNotIn(EM_DASH, s)
        for f in self.findings:
            self.assertLessEqual(len(f['sentence'].split()), 40, f['sentence'])
            self.assertNotRegex(f['sentence'].lower(), r'\b(should|try|consider)\b')
        for path in ('index.html', 'screen.js', 'audit.py', 'api.py'):
            self.assertNotIn(EM_DASH, (SCREEN / path).read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
