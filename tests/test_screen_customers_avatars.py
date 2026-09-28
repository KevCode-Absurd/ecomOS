"""Tests for screen 02-customers-avatars on the Bombas brain and simulated cohorts: audit.py in the
contract shape, the two insight rules, the repeat chart and the founder voice example write.
Writes go to a temp copy of app/brain, never the repo."""
import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / 'app' / 'screens' / '02-customers-avatars'
BRAIN = ROOT / 'app' / 'brain'
DAY = '2026-09-28'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


audit = load('customers_avatars_audit_t', SCREEN / 'audit.py')
api = load('customers_avatars_api_t', SCREEN / 'api.py')

FIELDS = ['id', 'screen', 'rule_id', 'severity', 'entity', 'evidence', 'sentence', 'capability', 'money_at_stake',
          'confidence', 'brain_refs', 'first_seen', 'last_seen', 'status', 'unavailable']
EVIDENCE = {'metric', 'value', 'unit', 'window', 'ends_on', 'freshness_days', 'baseline', 'baseline_kind', 'source', 'simulated'}
WINDOW = {'ends_on': '2026-09-27', 'days': 1, 'trailing': 0}


class Req:
    def __init__(self, path, method='GET', query=None, body=None):
        self.method, self.path, self.body = method, path, body
        self.query = dict({'today': [DAY]}, **(query or {}))

    def arg(self, name, default=None):
        v = self.query.get(name)
        return v[0] if v else default


class TempBrain(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        shutil.copytree(BRAIN / 'bombas', self.tmp / 'bombas')
        api.BRAIN_ROOT = self.tmp

    def tearDown(self):
        api.BRAIN_ROOT = None
        shutil.rmtree(self.tmp)

    def section(self, name):
        return json.loads((self.tmp / 'bombas' / f'{name}.json').read_text(encoding='utf-8'))

    def write(self, name, rows):
        (self.tmp / 'bombas' / f'{name}.json').write_text(json.dumps(rows), encoding='utf-8')


class AuditShape(unittest.TestCase):
    def test_contract_shape(self):
        findings = audit.run('bombas', WINDOW)
        self.assertTrue(findings)
        for f in findings:
            self.assertEqual(list(f)[:len(FIELDS)], FIELDS)
            self.assertIn(f['severity'], ('critical', 'high', 'medium', 'low'))
            self.assertTrue(f['id'].startswith('02-customers-avatars.' + f['rule_id'] + '.'))
            for row in f['evidence']:
                self.assertEqual(set(row), EVIDENCE)
            self.assertIn(f['capability']['autonomy'], ('agent_does', 'founder_gate', 'human_assist'))
            self.assertIsNone(f['money_at_stake'])
            self.assertTrue(f['money_reason'])
            self.assertLess(len(f['sentence'].split()), 40)
            self.assertNotIn('—', f['sentence'])
            for word in ('should', 'try', 'consider'):
                self.assertNotIn(' ' + word + ' ', ' ' + f['sentence'].lower() + ' ')
        order = [audit.SEVERITY_ORDER[f['severity']] for f in findings]
        self.assertEqual(order, sorted(order))

    def test_deterministic(self):
        self.assertEqual(json.dumps(audit.run('bombas', WINDOW)), json.dumps(audit.run('bombas', WINDOW)))

    def test_rules_fire_on_bombas(self):
        found = {f['id']: f for f in audit.run('bombas', WINDOW)}
        self.assertIn('02-customers-avatars.CUST-R01.holiday_gift_buyer', found)
        self.assertNotIn('02-customers-avatars.CUST-R01.durability_disappointed_repeat_customer', found)
        r02 = found['02-customers-avatars.CUST-R02.durability.3']
        self.assertEqual(r02['entity']['type'], 'ladder_rung')
        self.assertIn('bombas.objection_ladders.durability', r02['brain_refs'])
        self.assertIn('bombas.avatars.durability_disappointed_repeat_customer', r02['brain_refs'])
        r03 = found['02-customers-avatars.CUST-R03.ad_angles']
        self.assertEqual(r03['status'], 'unavailable')
        self.assertEqual(r03['evidence'], [])
        self.assertEqual(set(r03['unavailable']), {'inputs', 'connector', 'fix'})
        self.assertEqual({r['rule_id'] for r in audit.RULES}, {'CUST-R01', 'CUST-R02', 'CUST-R03'})


class AuditRules(TempBrain):
    def test_quote_less_avatar_is_inferred(self):
        rows = self.section('avatars')
        rows[0]['evidence'] = []
        self.write('avatars', rows)
        f = next(f for f in audit.run('bombas', WINDOW, self.tmp) if f['entity']['id'] == rows[0]['id'].split('.')[-1])
        self.assertIn('has no customer quotes', f['sentence'])
        d = api.handle(Req(['overview']))
        card = next(a for a in d['avatars'] if a['id'] == rows[0]['id'])
        self.assertEqual(card['grounding'], 'inferred')
        self.assertTrue(any(i['rule'] == 'avatar has 0 customer quotes' for i in d['insights']))

    def test_proof_on_rung_clears_top_objection(self):
        rows = self.section('objection_ladders')
        for lad in rows:
            if lad['id'] == 'bombas.objection_ladders.durability':
                lad['value']['rungs'][2]['proof_ids'] = ['bombas.policies.happiness_guarantee']
        self.write('objection_ladders', rows)
        ids = {f['id'] for f in audit.run('bombas', WINDOW, self.tmp)}
        self.assertNotIn('02-customers-avatars.CUST-R02.durability.3', ids)
        self.assertIn('02-customers-avatars.CUST-R02.fit_and_sizing.3', ids)


class Api(TempBrain):
    def test_overview(self):
        d = api.handle(Req(['overview']))
        self.assertIn('simulated', d['simulated_note'].lower())
        self.assertEqual(len(d['tiles']), 3)
        self.assertEqual(d['tiles'][0]['value'], sum(a['grounding'] == 'grounded' for a in d['avatars']))
        rules = {i['rule'] for i in d['insights']}
        self.assertIn("avatar's top objection rung (most one-star mentions) has no proof record", rules)
        for i in d['insights']:
            self.assertTrue(i['capability'] and i['autonomy'])
        self.assertTrue(d['avatars'] and d['objections'] and d['language']['themes'])
        for a in d['avatars']:
            self.assertLessEqual(len(a['quotes']), 4)
            for q in a['quotes']:
                self.assertTrue(q['ref'].startswith('http'))
        for o in d['objections']:
            self.assertIn(o['status'], ('open question', 'proof on file', 'not on a ladder'))
            self.assertIsNone(o['pages']['value'])
        self.assertTrue(d['voice']['do'])
        self.assertTrue(d['voice']['contexts'])
        self.assertEqual(d['decision']['capability'], 'BRAND-C15')

    def test_repeat_chart_from_cohorts(self):
        c = api.repeat_by_cohort('bombas')
        self.assertFalse(c['unavailable'])
        self.assertLessEqual(len(c['values']), api.CHART_COHORTS)
        row = c['rows'][-1]
        self.assertAlmostEqual(row['rate'], round(min(row['active_m1_m3'] / row['customers'], 1), 4))
        self.assertLess(c['labels'][-1], '2026-07')
        tile = api.overview(api._brain(Req(['overview'])))['tiles'][2]
        self.assertEqual(tile['value'], c['values'][-1])

    def test_liked_and_disliked_examples_write_founder_records(self):
        code, res = api.handle(Req(['voice', 'examples'], 'POST', body={'kind': 'liked', 'text': 'Comfort you can feel.'}))
        self.assertEqual(code, 201)
        rec = next(r for r in self.section('voice') if r['id'] == res['record'])
        self.assertEqual(rec['source']['type'], 'founder')
        self.assertEqual(rec['tier'], 'approved')
        v = api.handle(Req(['overview']))['voice']
        self.assertEqual([x['text'] for x in v['liked']], ['Comfort you can feel.'])
        code, res2 = api.handle(Req(['voice', 'examples'], 'POST', body={'kind': 'disliked', 'text': 'Comfort you can feel.'}))
        self.assertEqual(code, 201)
        v = api.handle(Req(['overview']))['voice']
        self.assertEqual(v['liked'], [])
        self.assertEqual([x['text'] for x in v['disliked']], ['Comfort you can feel.'])
        self.assertTrue(any(x['example'] == 'Comfort you can feel.' for x in v['do_not']))

    def test_bad_example_rejected(self):
        self.assertEqual(api.handle(Req(['voice', 'examples'], 'POST', body={'kind': 'maybe', 'text': 'x'}))[0], 400)
        self.assertEqual(api.handle(Req(['voice', 'examples'], 'POST', body={'kind': 'liked', 'text': ' '}))[0], 400)
        self.assertEqual(api.handle(Req(['voice', 'examples'], 'POST', body={'kind': 'liked', 'text': 'x' * 700}))[0], 400)

    def test_audit_route_and_bad_brand(self):
        d = api.handle(Req(['audit']))
        self.assertTrue(d['findings'])
        self.assertEqual(api.handle(Req(['overview'], query={'brand': ['../x']}))[0], 404)
        self.assertEqual(api.handle(Req(['nope']))[0], 404)


if __name__ == '__main__':
    unittest.main()
