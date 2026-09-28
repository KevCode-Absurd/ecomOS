"""Tests for screen 05-brand-brain on the Bombas brain: audit.py in the contract shape and the api
(overview, records, answer box, review queue). Writes go to a temp copy of app/brain, never the repo."""
import datetime as dt
import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / 'app' / 'screens' / '05-brand-brain'
BRAIN = ROOT / 'app' / 'brain'
DAY = '2026-09-28'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


audit = load('brand_brain_audit_t', SCREEN / 'audit.py')
api = load('brand_brain_api_t', SCREEN / 'api.py')

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
            self.assertTrue(f['id'].startswith('05-brand-brain.' + f['rule_id'] + '.'))
            for row in f['evidence']:
                self.assertEqual(set(row), EVIDENCE)
            self.assertIn(f['capability']['autonomy'], ('agent_does', 'founder_gate', 'human_assist'))
            self.assertIsNone(f['money_at_stake'])
            self.assertLess(len(f['sentence'].split()), 40)
            self.assertNotIn('—', f['sentence'])
        order = [audit.SEVERITY_ORDER[f['severity']] for f in findings]
        self.assertEqual(order, sorted(order))

    def test_deterministic(self):
        self.assertEqual(json.dumps(audit.run('bombas', WINDOW)), json.dumps(audit.run('bombas', WINDOW)))

    def test_rules_fire_on_bombas(self):
        ids = {f['id'] for f in audit.run('bombas', WINDOW)}
        self.assertIn('05-brand-brain.BRN-R03.question_gross_margin', ids)
        self.assertIn('05-brand-brain.BRN-R02.section_economics', ids)
        self.assertIn('05-brand-brain.BRN-R04.mission_trust.rung_1.donation_pledge', ids)
        rules = {r['rule_id'] for r in audit.RULES}
        self.assertEqual(rules, {'BRN-R01', 'BRN-R02', 'BRN-R03', 'BRN-R04'})


class AuditRules(TempBrain):
    def test_stale_section(self):
        rows = self.section('team')
        rows[0]['expires_at'] = '2026-01-01'
        self.write('team', rows)
        found = [f for f in audit.run('bombas', WINDOW, self.tmp) if f['rule_id'] == 'BRN-R01']
        self.assertEqual([f['entity']['id'] for f in found], ['section_team'])
        self.assertEqual(found[0]['severity'], 'low')

    def test_approved_claim_drops_finding(self):
        rows = self.section('claims')
        for r in rows:
            if r['id'] == 'bombas.claims.donation_pledge':
                r['tier'] = 'approved'
        self.write('claims', rows)
        ids = {f['id'] for f in audit.run('bombas', WINDOW, self.tmp)}
        self.assertNotIn('05-brand-brain.BRN-R04.mission_trust.rung_1.donation_pledge', ids)


class Api(TempBrain):
    def test_overview(self):
        d = api.handle(Req(['overview']))
        self.assertEqual(len(d['tiles']), 3)
        self.assertEqual(len(d['insights']), 2)
        self.assertEqual({i['capability'] for i in d['insights']}, {'BRN-C07', 'BRN-C05'})
        self.assertIn('simulated', d['simulated_note'])
        self.assertIn('brand card (T0)', d['t0'])
        self.assertEqual(len(d['chart']['labels']), len(d['chart']['values']))
        self.assertEqual(d['chart']['labels'][-1], DAY)
        secs = {s['section']: s for s in d['sections']}
        self.assertIsNone(secs['decisions']['confidence'])  # empty section: unavailable, not 0
        self.assertEqual(secs['claims']['records'], 6)
        self.assertTrue(d['ladders'] and d['ladders'][0]['rungs'])
        self.assertEqual(len(d['conflicts']), 1)

    def test_records(self):
        d = api.handle(Req(['records'], query={'section': ['claims']}))
        r = d['records'][0]
        self.assertEqual({'tier', 'date', 'source', 'evidence'} - set(r), set())
        self.assertTrue(r['source']['link'].startswith('https://'))
        self.assertTrue(r['evidence'][0]['quote'])
        self.assertEqual(api.handle(Req(['records'], query={'section': ['nope']}))[0], 404)

    def test_answer_writes_founder_record(self):
        status, res = api.handle(Req(['questions', 'gross_margin'], 'POST', body={'answer': '58%'}))
        self.assertEqual(status, 201)
        rec = next(r for r in self.section('economics') if r['id'] == res['record'])
        self.assertEqual(rec['source']['type'], 'founder')
        self.assertEqual(rec['value'], 58.0)
        oq = next(r for r in self.section('open_questions') if r['field'] == 'gross_margin')
        self.assertEqual(oq['value']['answered_on'], DAY)
        ids = {f['id'] for f in api.handle(Req(['audit']))['findings']}
        self.assertNotIn('05-brand-brain.BRN-R03.question_gross_margin', ids)
        self.assertEqual(api.handle(Req(['questions', 'gross_margin'], 'POST', body={'answer': ' '}))[0], 400)
        self.assertEqual(api.handle(Req(['questions', 'nope'], 'POST', body={'answer': 'x'}))[0], 404)

    def test_review_queue(self):
        rows = self.section('team')
        rows.append({'id': 'bombas.team.proposed_one', 'brand': 'bombas', 'section': 'team', 'field': 'proposed_one',
                     'value': 'x', 'text': 'A proposed fact.', 'status': 'proposed'})
        rows.append({'id': 'bombas.team.proposed_two', 'brand': 'bombas', 'section': 'team', 'field': 'proposed_two',
                     'value': 'y', 'text': 'Another proposed fact.', 'status': 'proposed'})
        self.write('team', rows)
        queue = api.handle(Req(['overview']))['review']
        self.assertEqual({r['id'] for r in queue}, {'bombas.team.proposed_one', 'bombas.team.proposed_two'})
        self.assertEqual(api.handle(Req(['review', 'bombas.team.proposed_one'], 'POST', body={'choice': 'accept'}))['status'], 'active')
        self.assertEqual(api.handle(Req(['review', 'bombas.team.proposed_two'], 'POST', body={'choice': 'ignore'}))['status'], 'retired')
        self.assertEqual(api.handle(Req(['overview']))['review'], [])
        self.assertEqual(api.handle(Req(['review', 'bombas.team.proposed_one'], 'POST', body={'choice': 'accept'}))[0], 404)

    def test_repo_brain_untouched(self):
        before = (BRAIN / 'bombas' / 'open_questions.json').read_bytes()
        api.handle(Req(['questions', 'aov'], 'POST', body={'answer': '$62'}))
        self.assertEqual((BRAIN / 'bombas' / 'open_questions.json').read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
