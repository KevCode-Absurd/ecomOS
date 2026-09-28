"""Screen 11-paid-social: audit rules, API shape, and the page on Bombas simulated data.

The synthetic tests build a tiny ad account in memory so the kill and fatigue rules are proven to fire.
The Bombas tests skip when app/data/brands/bombas/data.sqlite has not been built.
"""
import importlib.util
import sys
import unittest
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / 'app' / 'screens' / '11-paid-social'
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


api = load('paid_social_api_test', SCREEN / 'api.py')
audit = api.audit
AS_OF = date(2026, 9, 27)


def fin_row(field, value, unit):
    return {'field': field, 'scope': 'global', 'scope_key': '', 'value': value, 'unit': unit,
            'effective_from': '2025-01-01', 'effective_to': None}


class FakeData:
    """A 5-week ad account. A: CTR halves in the last 7 days while reach shrinks (fatigue).
    B: ROAS 1.0 every week (kill). C: ROAS 3.2 at low frequency (scale). D and E share one image."""

    def __init__(self):
        self.brand = {'brand': 'fake', 'as_of': AS_OF.isoformat(), 'simulated': True}
        rows = []
        for i in range(35):
            day = AS_OF - timedelta(days=34 - i)
            last_week = i >= 28
            for ad, spend, roas, ctr, reach, image in (
                    ('A', 500, 2.0, 0.006 if last_week else 0.012, 5000 if last_week else 8000, 'h1'),
                    ('B', 400, 1.0, 0.012, 8000, 'h2'),
                    ('C', 300, 3.2, 0.012, 9000, 'h3'),
                    ('D', 200, 2.0, 0.012, 8000, 'h4'),
                    ('E', 200, 2.0, 0.012, 8000, 'h4')):
                imps = 10000
                rows.append({'date': day.isoformat(), 'campaign_id': 'C1', 'campaign_name': 'Prospecting', 'adset_id': 'S1',
                             'ad_id': ad, 'spend': spend, 'impressions': imps, 'reach': reach,
                             'clicks': round(imps * ctr), 'purchases': round(spend * roas / 50),
                             'purchase_value': spend * roas, 'creative_id': 'CR-' + ad, 'image_hash': image,
                             'video_id': None, 'is_dynamic': 1 if ad == 'C' else 0, 'format': 'image'})
        self.tables = {'ad_rows': rows, 'finance_inputs': [fin_row('target_gross_margin', 50.0, 'percent'),
                                                          fin_row('target_contribution_margin', 20.0, 'percent'),
                                                          fin_row('target_cac', 30.0, 'usd')]}

    def table(self, name):
        if name not in self.tables:
            raise KeyError(name)
        return self.tables[name]

    def meta(self, name):
        return {'source': 'test', 'captured_at': '2026-09-28T06:00:00Z'}


class RulesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = FakeData()
        cls.findings = audit.run(None, {'ends_on': AS_OF.isoformat()}, data=cls.data)
        cls.by_id = {f['id']: f for f in cls.findings}

    def test_contract_shape(self):
        self.assertTrue(self.findings)
        for f in self.findings:
            self.assertEqual(list(f)[:len(AUDIT_KEYS)], AUDIT_KEYS)
            self.assertIn(f['severity'], ('critical', 'high', 'medium', 'low'))
            self.assertEqual(f['id'], f'11-paid-social.{f["rule_id"]}.{f["entity"]["id"]}')
            self.assertIn(f['capability']['autonomy'], ('agent_does', 'founder_gate', 'human_assist'))
            self.assertTrue(0.1 <= f['confidence'] <= 1)
            self.assertNotIn('—', f['sentence'])
            self.assertLess(len(f['sentence'].split()), 40)
            for ev in f['evidence']:
                self.assertTrue(EVIDENCE_KEYS <= set(ev))
                self.assertTrue(ev['simulated'])

    def test_kill_fires_with_money(self):
        f = self.by_id['11-paid-social.PAID-R01.B']
        stake = f['money_at_stake']
        i = stake['inputs']
        self.assertEqual(i['break_even_roas'], 2.0)  # 1 / 50 percent gross margin
        self.assertEqual(stake['usd'], round(i['spend_7d'] - i['purchase_value_7d'] / i['break_even_roas']))
        self.assertEqual(stake['usd'], 1400)  # 2,800 spent, 2,800 back, 1,400 short of break-even
        self.assertEqual(f['confidence'], 0.9)  # 4 trailing windows agree
        self.assertEqual(f['capability']['id'], 'MEDIA-C17')

    def test_fatigue_fires_with_money(self):
        f = self.by_id['11-paid-social.PAID-R03.A']
        self.assertEqual(f['capability'], {'id': 'CREA-C15', 'autonomy': 'agent_does'})
        self.assertIn('50 percent', f['sentence'])
        stake = f['money_at_stake']
        self.assertIsNotNone(stake)
        i = stake['inputs']
        self.assertEqual(stake['usd'], round(max(i['spend_7d'] - i['purchases_7d'] * i['cpa_median_4w'], 0)))

    def test_no_false_positives(self):
        ids = {f['entity']['id'] for f in self.findings}
        self.assertNotIn('C', ids)
        self.assertNotIn('D', ids)

    def test_deterministic(self):
        again = audit.run(None, {'ends_on': AS_OF.isoformat()}, data=self.data)
        self.assertEqual(again, self.findings)

    def test_verdicts_and_flags(self):
        rd = audit.Reader(self.data, None, AS_OF)
        th = audit.thresholds(rd)
        self.assertEqual((th['break_even'], th['target_roas'], th['floor']), (2.0, 3.3333, 90.0))
        rows = {r['ad']: r for r in api.creative_rows(audit.ad_windows(rd), th, AS_OF)}
        self.assertEqual(rows['B']['verdict'], 'kill')
        self.assertEqual(rows['C']['verdict'], 'watch')  # 3.2x is under the 3.33x target
        self.assertTrue(rows['D']['shared_creative'] and rows['E']['shared_creative'])
        self.assertFalse(rows['A']['shared_creative'])
        self.assertTrue(rows['C']['dynamic_creative'])
        self.assertEqual(len(rows), 5)  # ad-level rows kept when ads share an image

    def test_missing_ad_rows_is_unavailable_not_zero(self):
        empty = FakeData()
        del empty.tables['ad_rows']
        out = audit.run(None, {'ends_on': AS_OF.isoformat()}, data=empty)
        self.assertEqual({f['rule_id'] for f in out}, {'PAID-R01', 'PAID-R03'})
        for f in out:
            self.assertEqual(f['status'], 'unavailable')
            self.assertIsNone(f['money_at_stake'])
            self.assertEqual(f['unavailable']['inputs'], ['ad_rows'])

    def test_rules_list(self):
        self.assertEqual([r['rule_id'] for r in audit.RULES], ['PAID-R01', 'PAID-R03'])


class Req:
    def __init__(self, path, brand='bombas', method='GET'):
        self.method, self.path, self.query, self.data = method, path, {'brand': [brand]}, None

    def arg(self, name, default=None):
        v = self.query.get(name)
        return v[0] if v else default


@unittest.skipUnless(BOMBAS_DB.is_file(), 'bombas data.sqlite not built')
class BombasTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.o = api.handle(Req(['overview']))

    def test_simulated_and_tiles(self):
        o = self.o
        self.assertTrue(o['brand']['simulated'])
        self.assertFalse(o['unavailable'])
        for key in ('pacing', 'roas', 'mer', 'cpa'):
            t = o['tiles'][key]
            self.assertIsNotNone(t['value'], key)
            self.assertTrue(t['window'])
            self.assertEqual(t['freshness'], o['brand']['as_of'])
        p = o['tiles']['pacing']['inputs']
        self.assertAlmostEqual(o['tiles']['pacing']['value'], p['spend_mtd'] / p['days_elapsed'] * p['days_in_month'], places=1)

    def test_kill_list_matches_findings(self):
        kills = {r['ad'] for r in self.o['kill_scale']['kill']}
        found = {f['entity']['id'] for f in self.o['findings'] if f['rule_id'] == 'PAID-R01'}
        self.assertEqual(kills, found)
        self.assertTrue(kills)
        for r in self.o['kill_scale']['kill']:
            self.assertGreater(r['money_at_stake']['usd'], 0)
        for r in self.o['kill_scale']['scale']:
            self.assertLess(r['frequency'], 2.5)
            self.assertGreaterEqual(r['roas'], self.o['thresholds']['target_roas'])

    def test_creatives_are_ad_level(self):
        ads = [r['ad'] for r in self.o['creatives']]
        self.assertEqual(len(ads), len(set(ads)))

    def test_chart_90_days(self):
        c = self.o['chart']
        self.assertEqual(len(c['labels']), 90)
        self.assertEqual(c['labels'][-1], self.o['brand']['as_of'])
        self.assertEqual(len(c['spend']), 90)

    def test_insights_are_rules(self):
        ids = [i['id'] for i in self.o['insights']]
        self.assertEqual(ids, ['kill_scale', 'fatigue'])
        for i in self.o['insights']:
            self.assertTrue(i['rule'] and i['sentence'])

    def test_bad_input(self):
        self.assertEqual(api.handle(Req(['overview'], brand='../x'))[0], 400)
        self.assertEqual(api.handle(Req(['overview'], method='POST'))[0], 405)
        self.assertEqual(api.handle(Req(['nope']))[0], 404)


class PageTest(unittest.TestCase):
    def test_files_and_simulated_line(self):
        for f in ('index.html', 'screen.js', 'api.py', 'audit.py', 'FEATURES.md'):
            self.assertTrue((SCREEN / f).is_file(), f)
        js = (SCREEN / 'screen.js').read_text(encoding='utf-8')
        self.assertIn('simulated data', js)
        for text in (js, (SCREEN / 'index.html').read_text(encoding='utf-8')):
            self.assertNotIn('—', text)
            self.assertNotIn('GPT', text)


if __name__ == '__main__':
    unittest.main()
