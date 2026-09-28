"""Screen 27-wild-bets-pr: API shape, audit shape and determinism, rules firing on Bombas, writing rules,
and that every claim in the simulated bet queue is tier approved or site_backed in the brain.

Tests that read Bombas tables skip when app/data/brands/bombas/data.sqlite has not been built.
"""
import copy
import importlib.util
import json
import re
import sys
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / 'app' / 'screens' / '27-wild-bets-pr'
BOMBAS_DB = ROOT / 'app' / 'data' / 'brands' / 'bombas' / 'data.sqlite'
AUDIT_KEYS = ['id', 'screen', 'rule_id', 'severity', 'entity', 'evidence', 'sentence', 'capability', 'money_at_stake',
              'confidence', 'brain_refs', 'first_seen', 'last_seen', 'status', 'unavailable']
EVIDENCE_KEYS = {'metric', 'value', 'unit', 'window', 'ends_on', 'freshness_days', 'baseline', 'baseline_kind',
                 'source', 'simulated'}
ENTITY_TYPES = {'brand', 'stage', 'page', 'device', 'sku', 'campaign', 'adset', 'ad', 'flow', 'offer', 'ladder_rung',
                'metric'}
SPEC_RULES = {'WILD-R07', 'WILD-R08', 'WILD-R09', 'WILD-R10', 'WILD-R11', 'WILD-R12', 'WILD-R13', 'WILD-R14',
              'WILD-R15'}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


api = load('wild_bets_api_test', SCREEN / 'api.py')
audit = api.audit


class Req:
    def __init__(self, path, method='GET', **args):
        self.path, self.method, self.args, self.data = path, method, args, None

    def arg(self, name, default=None):
        return self.args.get(name, default)


def em_dash_free(text):
    return '—' not in text and '–' not in text


class TestStatic(unittest.TestCase):
    def test_rules_cover_the_room_spec(self):
        ids = {r['rule_id'] for r in audit.RULES}
        self.assertEqual(len(ids), 15)
        self.assertTrue(SPEC_RULES <= ids)
        for r in audit.RULES:
            self.assertEqual(set(r), {'rule_id', 'name', 'entity_type', 'inputs', 'capability', 'owner_screen'})
            self.assertIn(r['entity_type'], ENTITY_TYPES)
            self.assertIn(r['rule_id'], audit.__doc__)
            self.assertEqual(r['owner_screen'], '27-wild-bets-pr')

    def test_read_only_and_bad_brand(self):
        self.assertEqual(api.handle(Req(['overview'], method='POST'))[0], 405)
        self.assertEqual(api.handle(Req(['overview'], brand='../x'))[0], 400)
        self.assertEqual(api.handle(Req(['nope']))[0], 404)

    def test_queue_has_5_simulated_bets_tied_to_brain_and_metric(self):
        doc = audit.fixture('wild_bets.json')
        self.assertTrue(doc['simulated'])
        self.assertEqual(len(doc['bets']), 5)
        for b in doc['bets']:
            self.assertTrue(b['brain_ref'].startswith('bombas.'))
            self.assertIn(b['metric'], audit.ROOM_METRICS)
            self.assertTrue(b['claim_refs'])

    def test_every_bet_claim_is_approved_or_site_backed(self):
        br = audit.brain('bombas', today=date(2026, 9, 27))
        for b in audit.bets():
            self.assertIsNotNone(br.get(b['brain_ref']), b['brain_ref'])
            for rid in b['claim_refs']:
                rec = br.get(rid)
                self.assertIsNotNone(rec, rid)
                self.assertIn(rec.get('tier'), ('approved', 'site_backed'), rid)
            self.assertEqual(audit.bet_check(b, br), [])

    def test_unbacked_claim_fires_r06(self):
        br = audit.brain('bombas', today=date(2026, 9, 27))
        bad = copy.deepcopy(audit.bets()[0])
        bad['claim_refs'] = ['bombas.identity.founded']  # tier reported
        fs = audit.r06([bad], br, date(2026, 9, 27))
        self.assertEqual([f['rule_id'] for f in fs], ['WILD-R06'])
        self.assertIn('tier reported', fs[0]['sentence'])

    def test_bound_and_overdue_rules(self):
        end = date(2026, 9, 27)
        fs = audit.r05_r07(audit.bets(), end)
        by = {(f['rule_id'], f['entity']['id']) for f in fs}
        self.assertIn(('WILD-R05', 'wb-03'), by)
        self.assertIn(('WILD-R07', 'wb-04'), by)
        r07 = next(f for f in fs if f['rule_id'] == 'WILD-R07')
        self.assertEqual(r07['money_at_stake']['usd'], round(min(25000, 25000 / 30 * 27)))


@unittest.skipUnless(BOMBAS_DB.is_file(), 'bombas data.sqlite not built')
class TestBombas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.o = api.handle(Req(['overview']))
        cls.f = audit.run('bombas')

    def test_api_shape(self):
        o = self.o
        for k in ('brand', 'window', 'tiles', 'insights', 'chart', 'bets', 'launches', 'stories', 'calendar', 'metrics',
                  'actions', 'findings', 'rules'):
            self.assertIn(k, o)
        self.assertTrue(o['brand']['simulated'])
        self.assertEqual(len(o['tiles']), 3)
        self.assertEqual(len(o['insights']), 2)
        for i in o['insights']:
            self.assertTrue(i['rule'] and i['sentence'])
        self.assertFalse(o['chart'].get('unavailable'))
        self.assertEqual(len(o['chart']['labels']), api.CHART_WEEKS)
        press = o['tiles']['press']
        self.assertIsNone(press['value'])
        self.assertTrue(press['unavailable_reason'])
        for m in o['metrics']:
            if m['value'] is None:
                self.assertTrue(m['unavailable_reason'] and m['source'])

    def test_audit_shape(self):
        for f in self.f:
            self.assertEqual([k for k in AUDIT_KEYS if k in f], AUDIT_KEYS)
            self.assertIn(f['severity'], ('critical', 'high', 'medium', 'low'))
            self.assertIn(f['entity']['type'], ENTITY_TYPES)
            self.assertIn(f['capability']['autonomy'], ('agent_does', 'founder_gate', 'human_assist'))
            self.assertTrue(f['id'].startswith(f'27-wild-bets-pr.{f["rule_id"]}.'))
            self.assertTrue(0 <= f['confidence'] <= 1)
            for e in f['evidence']:
                self.assertTrue(EVIDENCE_KEYS <= set(e))
            if f['money_at_stake'] is None:
                self.assertTrue(f.get('money_reason'))
            else:
                self.assertGreaterEqual(f['money_at_stake']['usd'], 0)
                self.assertTrue(f['money_at_stake']['formula'] and f['money_at_stake']['inputs'])
            if f['status'] == 'unavailable':
                self.assertEqual(f['evidence'], [])
                self.assertTrue(f['unavailable']['inputs'] and f['unavailable']['connector'])
        self.assertEqual(len({f['id'] for f in self.f}), len(self.f))

    def test_deterministic(self):
        self.assertEqual(json.dumps(audit.run('bombas')), json.dumps(self.f))

    def test_every_rule_emits_or_is_readable(self):
        fired = {f['rule_id'] for f in self.f}
        for r in ('WILD-R01', 'WILD-R02', 'WILD-R03', 'WILD-R04', 'WILD-R05', 'WILD-R07', 'WILD-R12'):
            self.assertIn(r, fired)
        for r in ('WILD-R08', 'WILD-R10', 'WILD-R11', 'WILD-R13', 'WILD-R14', 'WILD-R15'):
            self.assertIn(r, {f['rule_id'] for f in self.f if f['status'] == 'unavailable'})

    def test_round0_audits_on_bombas(self):
        by = {}
        for f in self.f:
            by.setdefault(f['rule_id'], []).append(f)
        self.assertIn('200 million', by['WILD-R02'][0]['sentence'])
        self.assertIn('frame-buy-it-for-life', {f['entity']['id'] for f in by['WILD-R03']})
        self.assertNotIn('frame-worth-the-price', {f['entity']['id'] for f in by['WILD-R03']})  # WB-05 counters it
        self.assertTrue(any(f['money_at_stake'] for f in by['WILD-R04']))
        self.assertIn('moment-world-homeless-day', {f['entity']['id'] for f in by['WILD-R12']})

    def test_no_em_dashes_and_short_sentences(self):
        texts = [f['sentence'] for f in self.f] + [i['sentence'] for i in self.o['insights']]
        texts += [t['plain'] for t in self.o['tiles'].values()]
        for t in texts:
            self.assertTrue(em_dash_free(t), t)
            self.assertLessEqual(len(re.findall(r'[.!?](\s|$)', t)), 2, t)
            self.assertNotRegex(t.lower(), r'\b(should|try|consider)\b')
        for p in (SCREEN / 'screen.js', SCREEN / 'index.html', SCREEN / 'fixtures' / 'wild_bets.json',
                  SCREEN / 'fixtures' / 'holiday_calendar.json'):
            self.assertTrue(em_dash_free(p.read_text(encoding='utf-8')), p)

    def test_page_says_simulated(self):
        js = (SCREEN / 'screen.js').read_text(encoding='utf-8')
        self.assertIn('simulated data', js)
        self.assertNotIn('GPT', js)
        self.assertNotIn('.env', js)


if __name__ == '__main__':
    unittest.main()
