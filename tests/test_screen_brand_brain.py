"""Tests for screen 05-brand-brain on the Bombas brain: audit.py in the contract shape and the api
(overview, records, answer box, review queue). Writes go to a temp copy of app/brain, never the repo."""
import base64
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
        # R03 fires once per open question; which questions are open moves with the brain.
        bank = audit.keeper.load_bank()
        heavy = [q for q in audit.Brain('bombas', None, dt.date.fromisoformat(DAY)).records('open_questions')
                 if not (q.get('value') or {}).get('answered_on') and audit.question_weight(q, bank) >= audit.HIGH_WEIGHT]
        fired = any(i.startswith('05-brand-brain.BRN-R03.question_') for i in ids)
        self.assertEqual(fired, bool(heavy), ids)
        self.assertIn('05-brand-brain.BRN-R02.section_economics', ids)
        self.assertIn('05-brand-brain.BRN-R04.mission_trust.rung_1.donation_pledge', ids)
        rules = {r['rule_id'] for r in audit.RULES}
        self.assertLessEqual({'BRN-R01', 'BRN-R02', 'BRN-R03', 'BRN-R04', 'BRN-R05', 'BRN-R06', 'BRN-R07', 'BRN-R08', 'BRN-R09', 'BRN-R10', 'BRN-R11', 'BRN-R12', 'BRN-R13', 'BRN-R14', 'BRN-R15', 'BRN-R16', 'BRN-R17', 'BRN-R18', 'BRN-R19', 'BRN-R20', 'BRN-R21', 'BRN-R22'}, rules)


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
        # One insight per open-conflict plus the founder round when 4 or more questions wait.
        waiting = [q for q in d['questions'] if not q['answered_on']]
        expected = (1 if len(waiting) >= api.QUESTION_ROUND_AT else 0) + len(d['conflicts'])
        self.assertEqual(len(d['insights']), expected)
        self.assertLessEqual({i['capability'] for i in d['insights']}, {'BRN-C07', 'BRN-C05'})
        self.assertIn('simulated', d['simulated_note'])
        self.assertIn('brand card (T0)', d['t0'])
        self.assertEqual(len(d['chart']['labels']), len(d['chart']['values']))
        self.assertEqual(d['chart']['labels'][-1], DAY)
        secs = {s['section']: s for s in d['sections']}
        self.assertIsNone(secs['plans']['confidence'])  # empty section: unavailable, not 0
        self.assertEqual(secs['claims']['records'], 6)
        self.assertTrue(d['ladders'] and d['ladders'][0]['rungs'])
        # Only open conflicts reach the screen; a founder-settled one stays in review/conflicts.json as resolved.
        self.assertTrue(all(c['status'] == 'open' for c in d['conflicts']))

    def test_records(self):
        d = api.handle(Req(['records'], query={'section': ['claims']}))
        r = d['records'][0]
        self.assertEqual({'tier', 'date', 'source', 'evidence'} - set(r), set())
        self.assertTrue(r['source']['link'].startswith('https://'))
        self.assertTrue(r['evidence'][0]['quote'])
        self.assertEqual(api.handle(Req(['records'], query={'section': ['nope']}))[0], 404)

    def test_answer_writes_founder_record(self):
        # Answer whichever question is open first; the set moves with the brain.
        first = next(q for q in api.handle(Req(['overview']))['questions'] if not q['answered_on'])
        field = first['field']
        status, res = api.handle(Req(['questions', field], 'POST', body={'answer': '58%'}))
        self.assertEqual(status, 201)
        section = res['record'].split('.')[1]
        rec = next(r for r in self.section(section) if r['id'] == res['record'])
        self.assertEqual(rec['source']['type'], 'founder')
        self.assertEqual(rec['value'], 58.0)
        oq = next(r for r in self.section('open_questions') if r['field'] == field)
        self.assertEqual(oq['value']['answered_on'], DAY)
        ids = {f['id'] for f in api.handle(Req(['audit']))['findings']}
        self.assertNotIn(f'05-brand-brain.BRN-R03.question_{field}', ids)
        self.assertEqual(api.handle(Req(['questions', field], 'POST', body={'answer': ' '}))[0], 400)
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


class Round1TopSection(TempBrain):
    """Round 1 (depth contract): the master list, the editable profile and files in."""

    def test_master_list(self):
        d = api.handle(Req(['master']))
        self.assertEqual(d['brand'], 'bombas')
        self.assertLessEqual(len(d['top']), 10)
        self.assertTrue(d['top'])
        for a in d['top']:
            self.assertIn(a['owner'], ('agent', 'agent_drafts', 'person'))
            self.assertTrue(a['steps'] and a['artefact']['kind'])
            self.assertIn('total', a['rubric'])
            self.assertNotEqual(a['status'], 'unavailable')
        self.assertTrue(all(a['status'] == 'unavailable' for a in d['connect']))
        self.assertEqual(d['counts']['screens'], len([s for s in d['screens']]))
        self.assertTrue(d['bottlenecks'][0]['screen'])
        self.assertEqual(d['brain_version'], api.Brain('bombas', self.tmp, dt.date.fromisoformat(DAY)).version())

    def test_profile_winning_record_per_field(self):
        p = api.handle(Req(['profile']))
        secs = {s['section']: s for s in p['sections']}
        self.assertEqual([s['section'] for s in p['sections']], [s for s, _, _ in api.PROFILE_SECTIONS])
        pos = {f['key']: f for f in secs['positioning']['fields']}
        # 6 frame records exist; the profile shows one, the best tier, and says how many it stands for
        self.assertEqual(sum(1 for f in secs['positioning']['fields'] if f['key'] == 'frame'), 1)
        self.assertGreater(pos['frame']['variants'], 1)
        ident = {f['key']: f for f in secs['identity']['fields']}
        self.assertEqual(ident['giving_model']['tier'], 'approved')   # founder record wins over site
        self.assertEqual(ident['category']['tier'], 'site_backed')
        self.assertTrue(secs['identity']['flows_to'])
        self.assertIsInstance(p['approved_share'], float)
        # a field the list names but the brain lacks shows as unavailable, editable
        first = [f for f in secs['positioning']['fields'] if f['text'] is None]
        self.assertTrue(all(f['editable'] for f in first))

    def test_profile_edit_writes_approved_record_that_wins(self):
        status, res = api.handle(Req(['profile', 'positioning', 'price_frame'], method='POST', body={'text': 'Premium basics, priced per wear not per pair.'}))
        self.assertEqual(status, 201)
        self.assertEqual(res['record'], 'bombas.positioning.price_frame')
        self.assertIn('offers', res['flows_to'])
        rows = self.section('positioning')
        rec = next(r for r in rows if r['id'] == 'bombas.positioning.price_frame')
        self.assertEqual(rec['tier'], 'approved')
        self.assertEqual(rec['source']['type'], 'founder')
        self.assertEqual(rec['confidence'], 1.0)
        self.assertTrue(rec.get('history'))   # the inferred value moved into history
        p = api.handle(Req(['profile']))
        pos = {f['key']: f for f in next(s for s in p['sections'] if s['section'] == 'positioning')['fields']}
        self.assertEqual(pos['price_frame']['tier'], 'approved')
        self.assertEqual(pos['price_frame']['text'], 'Premium basics, priced per wear not per pair.')
        # records read through the store see the founder value; the inferred one is retired into history, not deleted
        recs = api.handle(Req(['records'], query={'section': ['positioning']}))['records']
        self.assertEqual(next(r for r in recs if r['field'] == 'price_frame')['tier'], 'approved')

    def test_profile_edit_rejects_empty_and_unknown(self):
        self.assertEqual(api.handle(Req(['profile', 'positioning', 'frame'], method='POST', body={'text': '  '}))[0], 400)
        self.assertEqual(api.handle(Req(['profile', 'nope', 'frame'], method='POST', body={'text': 'x'}))[0], 404)
        self.assertEqual(api.handle(Req(['profile', 'positioning', '../x'], method='POST', body={'text': 'x'}))[0], 404)

    def test_documents_in(self):
        self.assertEqual(api.handle(Req(['documents']))['count'], 0)
        status, res = api.handle(Req(['documents'], method='POST', body={'name': 'brand book v3.md', 'text': '# Voice\nShort. Warm. Digits.', 'note': 'from the agency'}))
        self.assertEqual(status, 201)
        self.assertEqual(res['document']['name'], DAY + '-brand book v3.md')
        self.assertEqual(res['records_changed_count'], 0)   # a 3-word line under a heading is too short for a record; the file is read and kept
        self.assertIn('nothing to propose', res['next'])
        status, res2 = api.handle(Req(['documents'], method='POST', body={'url': 'https://example.com/deck'}))
        self.assertEqual(status, 201)
        self.assertEqual(res2['document']['tags'], ['url'])
        d = api.handle(Req(['documents']))
        self.assertEqual(d['count'], 2)
        self.assertEqual({x['added_by'] for x in d['documents']}, {'founder'})
        self.assertTrue((self.tmp / 'bombas' / 'documents' / res['document']['name']).is_file())
        manifest = json.loads((self.tmp / 'bombas' / 'documents' / 'manifest.json').read_text())
        self.assertEqual(len(manifest), 2)
        self.assertTrue(all(m['file'].startswith('documents/') for m in manifest))
        self.assertEqual([m['extracted'] for m in manifest], [True, False])   # the text file was read, the url is kept as it is
        # a second file with the same name gets its own name, nothing is overwritten
        status, res3 = api.handle(Req(['documents'], method='POST', body={'name': 'brand book v3.md', 'text': 'v2'}))
        self.assertEqual(status, 201)
        self.assertNotEqual(res3['document']['name'], res['document']['name'])

    def test_documents_reject_bad_input(self):
        self.assertEqual(api.handle(Req(['documents'], method='POST', body={'name': '../x.md', 'text': 'x'}))[0], 400)
        self.assertEqual(api.handle(Req(['documents'], method='POST', body={'name': 'x.md'}))[0], 400)
        self.assertEqual(api.handle(Req(['documents'], method='POST', body={'url': 'ftp://x'}))[0], 400)
        self.assertEqual(api.handle(Req(['documents'], method='POST', body={'name': 'x.bin', 'content_base64': '***'}))[0], 400)

    def test_page_has_the_plan_first(self):
        html = (SCREEN / 'index.html').read_text(encoding='utf-8')
        self.assertLess(html.index('id="ask"'), html.index('id="plan"'))   # the ask box is a tool line above the plan, not a section
        self.assertLess(html.index('id="plan"'), html.index('id="profile"'))
        self.assertLess(html.index('id="profile"'), html.index('id="drop"'))
        self.assertLess(html.index('id="drop"'), html.index('id="audit"'))
        self.assertNotIn('id="tiles"', html)
        self.assertNotIn('id="chart"', html)
        self.assertNotIn('—', html)


class Round1Market(TempBrain):
    """Round 1 feature 1: the Ad Library pages against the brand, format and hook mix, gaps, re-pull cost."""

    def test_pages_against_the_brand(self):
        d = api.handle(Req(['competitors']))
        self.assertEqual(d['us']['role'], 'self')
        self.assertEqual(d['pages'][0]['role'], 'self')
        self.assertGreaterEqual(d['competitors_pulled'], 10)
        for p in d['pages']:
            if not p['pulled']:
                self.assertIsNone(p['ads_seen'])  # unavailable, never 0
                self.assertEqual(p['verdict']['kind'], 'wait')
                continue
            self.assertAlmostEqual(sum(p['format_share'].values()), 1.0, places=1)
            self.assertIn(p['verdict']['kind'], ('info', 'new', 'watch', 'keep'))
            self.assertTrue(p['ad_library_url'].startswith('https://www.facebook.com/ads/library/'))
        self.assertIn('Allbirds', d['not_pulled'])
        self.assertTrue(d['proposed'] and d['proposed'][0]['name'])
        # medians only over pages with 20 or more ads seen
        self.assertEqual(d['medians']['n'], sum(1 for p in d['pages'] if p['role'] == 'competitor' and p['pulled'] and p['ads_seen'] >= 20))

    def test_gaps_are_rules_in_numbers(self):
        d = api.handle(Req(['competitors']))
        kinds = {(g['kind'], g['key']) for g in d['gaps']}
        self.assertIn(('format', 'dco'), kinds)
        self.assertIn(('hook', 'question'), kinds)
        for g in d['gaps']:
            self.assertLess(g['us'], g['them'] if g['them'] else 1)
            self.assertTrue(g['leaders'] and g['record_ids'])
        ids = {f['id'] for f in api.handle(Req(['audit']))['findings']}
        self.assertIn('05-brand-brain.BRN-R05.format_dco', ids)
        self.assertIn('05-brand-brain.BRN-R06.hook_question', ids)
        f = next(f for f in api.handle(Req(['audit']))['findings'] if f['id'] == '05-brand-brain.BRN-R05.format_dco')
        self.assertEqual(f['capability']['id'], 'CREA-C19')
        self.assertEqual({e['metric'] for e in f['evidence']} & {'format_share_us', 'format_share_competitor_median'}, {'format_share_us', 'format_share_competitor_median'})

    def test_snapshot_stale_rule(self):
        # 8 days later every page is past the 7 day shelf life: one BRN-R07 finding per pulled competitor
        later = (dt.date.fromisoformat(DAY) + dt.timedelta(days=8)).isoformat()
        findings = api.handle(Req(['audit'], query={'today': [later]}))['findings']
        stale = [f for f in findings if f['rule_id'] == 'BRN-R07']
        self.assertGreaterEqual(len(stale), 10)
        self.assertTrue(all(f['severity'] == 'low' and f['capability']['id'] == 'BRN-C11' for f in stale))
        self.assertFalse([f for f in api.handle(Req(['audit']))['findings'] if f['rule_id'] == 'BRN-R07'])

    def test_repull_shows_cost_and_caps_never_runs(self):
        r = api.handle(Req(['competitors']))['repull']
        self.assertTrue(r['by_page_id_only'])
        self.assertGreater(r['estimate_usd'], 0)
        self.assertLessEqual(r['estimate_usd'], r['cap_per_run_usd'])
        self.assertEqual(r['pages'], 12)
        self.assertIsNone(r['week_spent_usd'])  # unavailable, not 0

    def test_page_has_market_between_files_and_desk(self):
        html = (SCREEN / 'index.html').read_text(encoding='utf-8')
        self.assertLess(html.index('id="drop"'), html.index('id="market"'))
        self.assertLess(html.index('id="market"'), html.index('id="audit"'))


class Round1Coverage(TempBrain):
    """Round 1 feature 2: the coverage matrix, angles by page, gaps with a drafted brief."""

    def test_matrix_shape_and_gaps(self):
        c = api.handle(Req(['coverage']))
        self.assertEqual(c['cols'][0]['key'], 'us')
        self.assertGreaterEqual(len(c['cols']), 4)
        keys = {r['key'] for r in c['rows']}
        for r in c['rows']:
            self.assertIn('us', c['cells'][r['key']])
        gap_keys = {g['angle'] for g in c['gaps']}
        self.assertIn('durability', gap_keys)
        self.assertTrue(gap_keys <= keys)
        for g in c['gaps']:
            self.assertEqual(c['cells'][g['angle']]['us']['us'], 0)
            self.assertTrue(g['competitors'])
            self.assertIn('Concept brief', g['brief'])
            self.assertIn('Never their text, logos, products or faces', g['brief'])
            self.assertNotIn('—', g['brief'])
        # a lead is ours alone; a contested angle is both
        for l in c['leads']:
            self.assertGreater(c['cells'][l['angle']]['us']['us'], 0)
            self.assertEqual(len(c['cells'][l['angle']]), 1)
        self.assertTrue(any(u['angle'] == 'durability' for u in c['unused_own']))

    def test_brief_uses_only_approved_or_site_backed_proof(self):
        c = api.handle(Req(['coverage']))
        g = next(g for g in c['gaps'] if g['angle'] == 'durability')
        usable = [x for x in g['proof']['claims'] if x['tier'] in ('approved', 'site_backed')]
        self.assertTrue(usable)
        self.assertIn('Proof we can use', g['brief'])
        self.assertIn('[site backed]', g['brief'])

    def test_angle_gap_findings_carry_the_draft(self):
        findings = [f for f in api.handle(Req(['audit']))['findings'] if f['rule_id'] == 'BRN-R08']
        self.assertTrue(findings)
        ids = {f['entity']['id'] for f in findings}
        self.assertIn('angle_durability', ids)
        for f in findings:
            self.assertEqual(f['capability']['id'], 'CREA-C06')
            self.assertIn(f['severity'], ('high', 'medium'))
            self.assertTrue(f['draft'].startswith('Concept brief'))
            self.assertLess(len(f['sentence'].split()), 40)
        three = [f for f in findings if f['evidence'][0]['value'] >= 3]
        self.assertTrue(all(f['severity'] == 'high' for f in three))

    def test_angles_of_carries_every_angle_in_a_label(self):
        self.assertEqual(api.market.angles_of('seasonal comfort'), ['comfort', 'seasonal'])
        self.assertEqual(api.market.angles_of('lifetime guarantee'), ['durability'])
        self.assertEqual(api.market.angles_of('catalog retargeting'), [])


class Round1Signals(TempBrain):
    """Round 1 feature 3: the recommended-instead signal, the category frames and the competitor sets as actions."""

    def test_recommended_instead_with_doubt_proof_and_where(self):
        sg = api.handle(Req(['signals']))
        self.assertTrue(sg['recommended'])
        self.assertEqual(sg['recommended'][0]['competitor'], 'Darn Tough')  # most threads first
        for r in sg['recommended']:
            self.assertTrue(r['where'])
            self.assertIn(r['proof_status'], ('no ladder', 'no proof on the deal-breaker rung', 'proof on file'))
            self.assertIn('never quoted', r['never'])
        dt_ = sg['recommended'][0]
        self.assertEqual(dt_['doubt_angle'], 'durability')
        self.assertEqual(dt_['proof_status'], 'no proof on the deal-breaker rung')
        self.assertIn('retargeting ad', dt_['where'])

    def test_frames_against_our_frame(self):
        sg = api.handle(Req(['signals']))
        self.assertEqual(sg['top_frame']['frame'], 'buy_it_for_life')
        self.assertIs(sg['top_frame']['covered_by_our_frame'], False)
        self.assertTrue(sg['our_frame']['id'].endswith('.positioning.frame'))
        self.assertEqual(sg['competitor_frame']['tier'], 'approved')
        self.assertIn('direct', sg['sets'])
        self.assertTrue(all(n['tracked'] for n in sg['sets']['direct']))

    def test_signal_findings(self):
        findings = api.handle(Req(['audit']))['findings']
        r09 = [f for f in findings if f['rule_id'] == 'BRN-R09']
        self.assertEqual(len(r09), 4)
        top = next(f for f in r09 if f['entity']['id'] == 'recommended_darn_tough')
        self.assertEqual(top['severity'], 'high')
        self.assertEqual(top['capability']['id'], 'BRAND-C57')
        self.assertTrue(top['where'])
        self.assertNotIn('u/', top['sentence'])
        r10 = {f['entity']['id'] for f in findings if f['rule_id'] == 'BRN-R10'}
        self.assertEqual(r10, {'frame_buy_it_for_life', 'frame_mission'})

    def test_page_id_write_flows_to_pages_and_repull(self):
        before = api.handle(Req(['competitors']))['repull']['pages']
        status, res = api.handle(Req(['competitors', 'page-id'], 'POST', body={'name': 'Uniqlo', 'page_id': '123456789012'}))
        self.assertEqual(status, 201)
        rec = next(r for r in self.section('competitors') if r['id'] == res['record'])
        self.assertEqual((rec['source']['type'], rec['tier'], rec['value']), ('founder', 'approved', '123456789012'))
        d = api.handle(Req(['competitors']))
        row = next(p for p in d['pages'] if p['name'] == 'Uniqlo')
        self.assertEqual(row['verdict']['text'], 'Pull pending')
        self.assertEqual(d['repull']['pages'], before + 1)
        self.assertNotIn('Uniqlo', [p['name'] for p in d['proposed']])
        self.assertEqual(api.handle(Req(['competitors', 'page-id'], 'POST', body={'name': 'Uniqlo', 'page_id': 'abc'}))[0], 400)


class Round1Health(TempBrain):
    """Round 1 feature 4: freshness by confidence per section, each weak row ending in an action; approve or forbid a record."""

    def test_heatmap_rows_cols_and_verdicts(self):
        h = api.handle(Req(['health']))
        self.assertEqual([c['key'] for c in h['cols']], api.health.TIERS)
        keys = [r['key'] for r in h['rows']]
        self.assertNotIn('freshness', keys)
        self.assertIn('plans', keys)
        self.assertEqual(h['cells']['plans'], {})   # no records: an empty row, never a 0
        self.assertEqual(sum(c['us'] for c in h['cells']['claims'].values()), 6)
        by = {s['section']: s for s in h['sections']}
        self.assertEqual(by['objection_ladders']['verdict']['kind'], 'ask')
        self.assertEqual(by['objection_ladders']['verdict']['owner'], 'agent_drafts')
        self.assertTrue(by['objection_ladders']['verdict']['steps'])
        self.assertEqual(by['claims']['verdict']['kind'], 'ok')
        self.assertIsNone(by['plans']['age_days'])
        self.assertEqual(h['sections'][0]['verdict']['kind'], 'ask')  # weak rows first
        self.assertGreater(h['strong_share'], 0)

    def test_stale_section_becomes_recrawl(self):
        rows = self.section('policies')
        for r in rows:
            r['expires_at'] = '2026-01-01'
        self.write('policies', rows)
        by = {s['section']: s for s in api.handle(Req(['health']))['sections']}
        v = by['policies']['verdict']
        self.assertEqual((v['kind'], v['capability'], v['owner']), ('recrawl', 'BRN-C01', 'agent'))
        self.assertEqual(by['policies']['stale'], 10)

    def test_empty_needed_section_becomes_connect_or_ask(self):
        self.write('economics', [])
        by = {s['section']: s for s in api.handle(Req(['health']))['sections']}
        v = by['economics']['verdict']
        self.assertIn(v['kind'], ('connect', 'ask'))
        self.assertEqual(v['owner'], 'person' if v['kind'] == 'connect' else 'agent_drafts')
        self.assertTrue(v['steps'])

    def test_weak_section_rule_and_cell_records(self):
        ids = {f['id'] for f in api.handle(Req(['audit']))['findings']}
        self.assertIn('05-brand-brain.BRN-R11.section_objection_ladders', ids)
        cell = api.handle(Req(['health', 'cell'], query={'section': ['positioning'], 'tier': ['inferred']}))
        self.assertEqual(len(cell['records']), 6)
        self.assertTrue(all(r['tier'] == 'inferred' for r in cell['records']))
        self.assertEqual(api.handle(Req(['health', 'cell'], query={'section': ['nope'], 'tier': ['inferred']}))['records'], [])

    def test_approve_and_forbid_write_founder_records(self):
        rid = 'bombas.positioning.frame'
        status, res = api.handle(Req(['approve', rid], 'POST', body={'choice': 'approve'}))
        self.assertEqual((status, res['tier'], res['was']), (201, 'approved', 'inferred'))
        rec = next(r for r in self.section('positioning') if r['id'] == rid)
        self.assertEqual((rec['tier'], rec['source']['type'], rec['source']['was']['tier']), ('approved', 'founder', 'inferred'))
        self.assertTrue(rec.get('history'))
        prof = api.handle(Req(['profile']))
        f = next(f for s in prof['sections'] if s['section'] == 'positioning' for f in s['fields'] if f['key'] == 'frame')
        self.assertEqual(f['tier'], 'approved')
        status, res = api.handle(Req(['approve', 'bombas.claims.donation_pledge'], 'POST', body={'choice': 'forbid'}))
        self.assertEqual((status, res['tier']), (201, 'forbidden'))
        self.assertEqual(api.handle(Req(['approve', 'bombas.claims.nope'], 'POST', body={'choice': 'approve'}))[0], 404)
        self.assertEqual(api.handle(Req(['approve', rid], 'POST', body={'choice': 'maybe'}))[0], 400)


class Round1Connectors(TempBrain):
    """Round 1 feature 5: what is connected, what each fills, unavailable never zero, connect steps."""

    def test_categories_and_sources(self):
        cn = api.handle(Req(['health']))['connectors']
        self.assertGreaterEqual(cn['counts']['sources'], 80)
        by = {c['category']: c for c in cn['categories']}
        self.assertIn(by['public']['verdict']['kind'], ('keep', 'fix'))   # fix when a public source failed over 10 percent of its pulls
        self.assertTrue(by['public']['via'])
        if by['public']['verdict']['kind'] == 'fix':
            self.assertIn('pulls failed', by['public']['verdict']['reason'])
        self.assertEqual(by['store']['verdict']['text'], 'Connect one')
        self.assertEqual(len(by['store']['steps']), 4)
        self.assertEqual(by['store']['steps'][0]['who'], 'person')
        self.assertIsNone(by['store']['last_pull'])
        self.assertEqual(cn['categories'][0]['verdict']['kind'], 'stop')  # the category that unblocks most rooms first
        src = {r['id']: r for r in cn['sources']}
        self.assertEqual(src['site']['status'], 'connected')
        self.assertIsNotNone(src['site']['pulls'])
        self.assertIsNone(src['shopify']['pulls'])      # never pulled: unavailable, not 0
        self.assertIsNone(src['shopify']['health'])
        self.assertEqual(src['shopify']['status'], 'not connected')
        self.assertTrue(src['shopify']['unblocks_rooms'])
        self.assertIn(src['apify_reddit']['status'], ('connected', 'not connected'))

    def test_upload_counts_as_connected_once_a_document_lands(self):
        cn = api.handle(Req(['health']))['connectors']
        self.assertEqual(next(r for r in cn['sources'] if r['id'] == 'upload')['status'], 'not connected')
        api.handle(Req(['documents'], 'POST', body={'name': 'notes.md', 'text': '# Notes'}))
        cn = api.handle(Req(['health']))['connectors']
        up = next(r for r in cn['sources'] if r['id'] == 'upload')
        self.assertEqual((up['status'], up['last_pull']), ('connected', DAY))


class Round1Conflicts(TempBrain):
    """Round 1 feature 6: conflicts with the site-wins default and a founder decision that writes the resolution."""

    def inject(self):
        rows = self.section('offers')
        rows.append({'id': 'bombas.offers.returns_window_days', 'brand': 'bombas', 'section': 'offers', 'field': 'returns_window_days',
                     'value': 30, 'text': 'Returns within 30 days.', 'tier': 'site_backed', 'confidence': 0.9,
                     'source': {'type': 'site', 'ref': 'https://bombas.com/pages/returns', 'captured_at': DAY}})
        self.write('offers', rows)
        conflicts = json.loads((self.tmp / 'bombas' / 'review' / 'conflicts.json').read_text(encoding='utf-8'))
        conflicts.append({'id': 'bombas.conflict.offers.returns_window_days', 'brand': 'bombas', 'section': 'offers', 'field': 'returns_window_days',
                          'status': 'open', 'raised_at': DAY, 'kept': 'bombas.offers.returns_window_days', 'needs_founder': False, 'rule': 'site ranks above document',
                          'values': [{'value': 30, 'text': 'Returns within 30 days.', 'source_type': 'site', 'source_ref': 'https://bombas.com/pages/returns', 'record_id': 'bombas.offers.returns_window_days', 'confidence': 0.9},
                                     {'value': 60, 'text': 'Returns within 60 days.', 'source_type': 'document', 'source_ref': 'brand-book.pdf', 'record_id': 'bombas.offers.returns_window_days', 'confidence': 0.75}]})
        (self.tmp / 'bombas' / 'review' / 'conflicts.json').write_text(json.dumps(conflicts), encoding='utf-8')

    def test_open_conflict_shows_default_and_fires_rule(self):
        self.inject()
        cv = api.handle(Req(['conflicts']))
        self.assertEqual(cv['counts'], {'open': 1, 'settled': 1, 'needs_founder': 0})
        c = cv['open'][0]
        self.assertEqual((c['default_source'], c['kept_value']['value']), ('site', 30))
        self.assertIn('paid social', c['reads_by'])
        ids = {f['id']: f for f in api.handle(Req(['audit']))['findings']}
        f = ids['05-brand-brain.BRN-R12.conflict_offers_returns_window_days']
        self.assertEqual((f['severity'], f['capability']['id']), ('medium', 'BRN-C05'))
        self.assertIn('"30" is kept until you decide', f['sentence'])

    def test_founder_decides_writes_record_and_decision(self):
        self.inject()
        status, res = api.handle(Req(['conflicts', 'bombas.conflict.offers.returns_window_days'], 'POST', body={'record_id': 'bombas.offers.returns_window_days', 'index': 1, 'reason': 'the brand book is current'}))
        self.assertEqual(status, 201)
        rec = next(r for r in self.section('offers') if r['id'] == 'bombas.offers.returns_window_days')
        self.assertEqual((rec['value'], rec['tier'], rec['source']['type']), (60, 'approved', 'founder'))
        self.assertEqual(rec['history'][-1]['value'], 30)
        lane = json.loads((self.tmp / 'bombas' / 'raw' / 'z-founder' / 'offers.json').read_text(encoding='utf-8'))
        self.assertIn('bombas.offers.returns_window_days', {r['id'] for r in lane})
        cv = api.handle(Req(['conflicts']))
        self.assertEqual(cv['counts']['open'], 0)
        settled = next(c for c in cv['settled'] if c['id'] == 'bombas.conflict.offers.returns_window_days')
        self.assertEqual((settled['status'], settled['chosen']['source_type'], settled['resolved_at']), ('resolved_by_founder', 'document', DAY))
        dec = next(r for r in self.section('decisions') if r['id'] == res['decision'])
        self.assertIn('kept "Returns within 60 days."', dec['text'])
        self.assertIn('the brand book is current', dec['text'])
        self.assertNotIn('05-brand-brain.BRN-R12.conflict_offers_returns_window_days', {f['id'] for f in api.handle(Req(['audit']))['findings']})
        prof = api.handle(Req(['profile']))
        f = next(f for s_ in prof['sections'] if s_['section'] == 'offers' for f in s_['fields'] if f['key'] == 'returns_window_days')
        self.assertEqual(f['tier'], 'approved')

    def test_typed_value_and_bad_input(self):
        self.inject()
        status, res = api.handle(Req(['conflicts', 'bombas.conflict.offers.returns_window_days'], 'POST', body={'text': '45'}))
        self.assertEqual(status, 201)
        rec = next(r for r in self.section('offers') if r['id'] == 'bombas.offers.returns_window_days')
        self.assertEqual(rec['value'], 45.0)
        self.assertEqual(api.handle(Req(['conflicts', 'nope'], 'POST', body={'text': 'x'}))[0], 404)
        self.assertEqual(api.handle(Req(['conflicts', 'bombas.conflict.identity.giving_model'], 'POST', body={}))[0], 400)

    def test_profile_edit_lands_in_founder_lane(self):
        api.handle(Req(['profile', 'positioning', 'frame'], 'POST', body={'text': 'Comfort that lasts, and a pair given for every pair bought.'}))
        lane = json.loads((self.tmp / 'bombas' / 'raw' / 'z-founder' / 'positioning.json').read_text(encoding='utf-8'))
        self.assertEqual(lane[-1]['id'], 'bombas.positioning.frame')
        self.assertEqual(lane[-1]['tier'], 'approved')


class Round1Questions(TempBrain):
    """Round 1 feature 7: every open question ranked by weight times rooms unblocked, pull-first hints, inline answers."""

    def test_ranked_list_merges_brain_and_bank(self):
        qv = api.handle(Req(['questions']))
        kinds = {q['kind'] for q in qv['questions']}
        self.assertEqual(kinds, {'brain', 'bank'})
        imp = [q['importance'] for q in qv['questions'] if not q['answered_on']]
        self.assertEqual(imp, sorted(imp, reverse=True))
        self.assertEqual(qv['top'][0]['id'], 'q.economics.gross_margin')
        self.assertTrue(qv['top'][0]['connect'])
        self.assertIn('Pull first', qv['top'][0]['hint'])
        self.assertIn('21-finance-cash', qv['top'][0]['screens'])
        self.assertEqual(len(qv['top']), 5)
        self.assertTrue(qv['counts']['round_due'])
        ladder = next(q for q in qv['questions'] if q['kind'] == 'brain')
        self.assertEqual(ladder['section'], 'objection_ladders')
        self.assertIn('05-brand-brain', ladder['screens'])

    def test_bank_answer_writes_founder_record_and_drops_the_question(self):
        status, res = api.handle(Req(['questions', 'bank', 'q.economics.gross_margin'], 'POST', body={'answer': '58%'}))
        self.assertEqual((status, res['record']), (201, 'bombas.economics.gross_margin_pct'))
        rec = next(r for r in self.section('economics') if r['id'] == res['record'])
        self.assertEqual((rec['value'], rec['tier'], rec['source']['type']), (58.0, 'approved', 'founder'))
        self.assertIn('finance', res['unblocks'])
        ids = {q['id'] for q in api.handle(Req(['questions']))['questions']}
        self.assertNotIn('q.economics.gross_margin', ids)
        self.assertEqual(api.handle(Req(['questions', 'bank', 'q.nope'], 'POST', body={'answer': 'x'}))[0], 404)
        self.assertEqual(api.handle(Req(['questions', 'bank', 'q.claims.approved'], 'POST', body={'answer': ' '}))[0], 400)


class Round1Decisions(TempBrain):
    """Round 1 feature 8: the decisions timeline, and approvals reflected on the master list."""

    def test_timeline_merges_action_and_brain_decisions(self):
        path = self.tmp / 'decisions.json'
        path.write_text(json.dumps([
            {'screen': '05-brand-brain', 'capability': 'CREA-C06', 'choice': 'agent', 'reason': 'go', 'time': '2026-09-28T10:00:00Z', 'finding_id': '05-brand-brain.BRN-R08.angle_durability'},
            {'screen': '04-offers-pricing', 'capability': 'LIFE-C36', 'choice': 'not_now', 'reason': '', 'time': '2026-09-27T10:00:00Z', 'finding_id': 'x'}]), encoding='utf-8')
        old = api.DECISIONS_PATH
        api.DECISIONS_PATH = path
        try:
            d = api.handle(Req(['decisions']))
        finally:
            api.DECISIONS_PATH = old
        self.assertEqual({k: d['counts'][k] for k in ('action', 'snoozed', 'brain')}, {'action': 1, 'snoozed': 1, 'brain': 2})
        self.assertEqual(d['items'][0]['kind'], 'action')
        self.assertEqual(d['items'][0]['choice'], 'agent')
        times = [it.get('time') or it.get('date') for it in d['items']]
        self.assertEqual(times, sorted(times, reverse=True))
        brain_items = [it for it in d['items'] if it['kind'] == 'brain']
        self.assertTrue(all(it['text'] and it['who'] for it in brain_items))
        self.assertEqual(d['last'], '2026-09-28T10:00:00Z')

    def test_conflict_decision_shows_in_the_timeline(self):
        Round1Conflicts.inject(self)
        api.handle(Req(['conflicts', 'bombas.conflict.offers.returns_window_days'], 'POST', body={'index': 1, 'reason': 'brand book'}))
        d = api.handle(Req(['decisions']))
        self.assertTrue(any(it['kind'] == 'brain' and 'returns window days' in it['title'] for it in d['items']))

    def test_approved_master_item_carries_its_decision(self):
        path = self.tmp / 'decisions.json'
        m0 = api.handle(Req(['master']))
        first = m0['top'][0]
        path.write_text(json.dumps([{'screen': first['screen'], 'capability': first['capability']['id'], 'choice': 'agent', 'reason': 'go', 'time': DAY + 'T10:00:00Z', 'finding_id': first['id']}]), encoding='utf-8')
        m = api.rank_mod.master('bombas', {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4}, decisions_path=path)
        a = next(x for x in m['actions'] if x['id'] == first['id'])
        self.assertEqual(a['decision']['choice'], 'agent')
        self.assertEqual(a['status'], 'open')
        self.assertIn('id="progress"', (SCREEN / 'index.html').read_text(encoding='utf-8'))


class Round1FilesIn(TempBrain):
    """Round 1 feature 9: a text file is read into proposed records with source and date; what each file changed shows."""

    NOTE = "# Founder notes\n\nWe tried a referral program in 2025. It did not move repeat rate.\n\n## Offers\nFree shipping threshold: $50\n- Bundles: 4 pack saves 10 percent\n\n## Voice\n- Never say the softest socks in the world.\n\nDecision: we decided to keep the giving line in catalog ads.\nGross margin: 58%\n"

    def test_markdown_lands_as_proposed_records(self):
        status, res = api.handle(Req(['documents'], 'POST', body={'name': 'call-notes.md', 'text': self.NOTE}))
        self.assertEqual(status, 201)
        ex = res['extraction']
        self.assertGreaterEqual(ex['proposed'], 5)
        self.assertEqual(ex['forbidden'], 1)
        self.assertIn('offers', ex['sections'])
        self.assertIn('review queue', res['next'])
        offers = self.section('offers')
        rec = next(r for r in offers if r['id'].endswith('_free_shipping_threshold'))
        self.assertEqual((rec['status'], rec['tier'], rec['value'], rec['source']['type']), ('proposed', 'unverified', 50.0, 'document'))
        self.assertEqual(rec['source']['captured_at'], DAY)
        self.assertTrue(rec['evidence'][0]['quote'])
        forbidden = [r for r in self.section('claims') if r.get('status') == 'proposed']
        self.assertEqual(forbidden[0]['tier'], 'forbidden')
        # not in the brain until accepted: the profile and the section counts ignore proposed records
        self.assertFalse([r for r in api.handle(Req(['records'], query={'section': ['offers']}))['records'] if 'call_notes' in r['id']])
        queue = api.handle(Req(['overview']))['review']
        self.assertTrue(any('call_notes' in r['id'] for r in queue))
        docs = api.handle(Req(['documents']))
        d = next(x for x in docs['documents'] if x['name'].endswith('call-notes.md'))
        self.assertTrue(d['extracted'])
        self.assertEqual(d['proposed'], ex['proposed'])
        self.assertIn('waiting in the review queue', d['what_changed'])
        api.handle(Req(['review', rec['id']], 'POST', body={'choice': 'accept'}))
        d = next(x for x in api.handle(Req(['documents']))['documents'] if x['name'].endswith('call-notes.md'))
        self.assertEqual(d['accepted'], 1)

    def test_binary_and_url_are_kept_not_read(self):
        status, res = api.handle(Req(['documents'], 'POST', body={'name': 'deck.pdf', 'content_base64': 'JVBERi0xLjQK'}))
        self.assertEqual((status, res['records_changed_count'], res['extraction']), (201, 0, None))
        status, res = api.handle(Req(['documents'], 'POST', body={'url': 'https://example.com/brand-book'}))
        self.assertEqual((status, res['extraction']), (201, None))
        d = next(x for x in api.handle(Req(['documents']))['documents'] if x['name'].endswith('deck.pdf'))
        self.assertIn('kept as a file', d['what_changed'])

    def test_re_read_and_determinism(self):
        api.handle(Req(['documents'], 'POST', body={'name': 'again.txt', 'text': self.NOTE}))
        name = next(x['name'] for x in api.handle(Req(['documents']))['documents'] if x['name'].endswith('again.txt'))
        status, res = api.handle(Req(['documents', 'extract'], 'POST', body={'name': name}))
        self.assertEqual(status, 201)
        a = api.ingest.extract(self.NOTE, 'bombas', 'documents/x.md', DAY)
        b = api.ingest.extract(self.NOTE, 'bombas', 'documents/x.md', DAY)
        self.assertEqual(json.dumps(a), json.dumps(b))
        self.assertEqual(api.handle(Req(['documents', 'extract'], 'POST', body={'name': 'nope.md'}))[0], 404)


class Round1RankAndFlows(TempBrain):
    """Round 1 feature 10: rank() with real titles, steps and drafts; the flow proof of where an edit goes."""

    W = {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4}

    def test_rank_override_is_picked_up_and_valid(self):
        r = api.rank_mod.rank('05-brand-brain', 'bombas', self.W)
        self.assertEqual(r['source'], 'screen')
        findings = {f['id'] for f in api.audit.run('bombas', self.W, self.tmp)}
        covered = {fid for a in r['actions'] for fid in a['finding_ids']}
        self.assertEqual(findings, covered)
        for a in r['actions']:
            self.assertEqual(api.rank_mod.validate_action(a), [])
            self.assertNotIn('—', a['title'])
            self.assertLess(len(a['title']), 120)
        by_rule = {}
        for a in r['actions']:
            by_rule.setdefault(a['rule_id'], a)
        self.assertTrue(by_rule['BRN-R08']['artefact']['draft'].startswith('Concept brief'))
        self.assertEqual(by_rule['BRN-R08']['owner'], 'agent_drafts')
        self.assertEqual(by_rule['BRN-R07']['owner'] if 'BRN-R07' in by_rule else 'agent', 'agent')
        self.assertEqual(by_rule['BRN-R04']['owner'], 'person')
        self.assertTrue(by_rule['BRN-R05']['stop_rule'] and by_rule['BRN-R05']['check_on'])
        self.assertTrue(by_rule['BRN-R09']['title'].startswith('Answer the '))
        self.assertGreaterEqual(by_rule['BRN-R09']['rubric']['reputation'], 5)
        # a title never repeats the capability name as the default does
        self.assertFalse(any(a['title'].startswith('Write standardized') or a['title'].startswith('Claim tiering') for a in r['actions']))

    def test_rank_deterministic_and_top_is_a_brief(self):
        a = api.rank('bombas', self.W)['actions']
        b = api.rank('bombas', self.W)['actions']
        self.assertEqual(json.dumps(a), json.dumps(b))
        self.assertEqual(a[0]['rule_id'], 'BRN-R08')
        self.assertEqual(a[0]['severity'], 'high')

    def test_flows_name_the_readers(self):
        fl = api.handle(Req(['flows']))
        by = {s['section']: s for s in fl['sections']}
        self.assertIn('02-customers-avatars', by['positioning']['read_by'])
        self.assertIn('01-market-research', by['positioning']['read_by'])
        self.assertIsNone(by['positioning']['last_read'])
        self.assertTrue(by['positioning']['last_read_reason'])
        # a caller that names itself stamps the read log; the flow proof then shows the reader and the time
        api.handle(Req(['records'], query={'section': ['positioning'], 'reader': ['10-copy']}))
        api.handle(Req(['profile'], query={'reader': ['02-customers-avatars']}))
        by = {s['section']: s for s in api.handle(Req(['flows']))['sections']}
        self.assertEqual(by['positioning']['read_by_log'], ['02-customers-avatars', '10-copy'])
        self.assertEqual(by['positioning']['last_reader'], '02-customers-avatars')
        self.assertTrue(by['positioning']['last_read'])
        self.assertTrue((self.tmp / 'bombas' / 'reads.log.jsonl').is_file())
        self.assertGreaterEqual(fl['screens_scanned'], 20)
        api.handle(Req(['profile', 'positioning', 'frame'], 'POST', body={'text': 'Comfort that lasts.'}))
        by = {s['section']: s for s in api.handle(Req(['flows']))['sections']}
        self.assertEqual((by['positioning']['approved'], by['positioning']['last_founder_edit']), (1, DAY))


class Round2Claims(TempBrain):
    """Round 2 feature 1: the claims desk and the draft scanner."""

    def test_desk_lists_claims_with_use_and_verdict(self):
        cd = api.handle(Req(['claims']))
        self.assertEqual(cd['total'], 6)
        self.assertEqual(cd['usable'], 6)
        by = {c['field']: c for c in cd['claims']}
        self.assertEqual(by['calf_socks_benefit']['verdict']['kind'], 'keep')
        self.assertIn('copy', by['calf_socks_benefit']['surfaces'])
        self.assertEqual(len(by['calf_socks_benefit']['used_by']), 2)
        self.assertEqual(cd['forbidden_phrases'], [])

    def test_add_forbid_and_untiered_rule(self):
        status, res = api.handle(Req(['claims'], 'POST', body={'text': 'the softest socks in the world', 'tier': 'forbidden'}))
        self.assertEqual((status, res['tier']), (201, 'forbidden'))
        cd = api.handle(Req(['claims']))
        self.assertEqual(cd['forbidden'], 1)
        self.assertEqual(cd['forbidden_phrases'][0]['phrase'], 'the softest socks in the world')
        status, res = api.handle(Req(['claims'], 'POST', body={'text': 'Every pair is knit in a family-owned mill.', 'tier': 'approved'}))
        self.assertEqual((status, res['tier']), (201, 'approved'))
        self.assertEqual(api.handle(Req(['claims'], 'POST', body={'text': 'x', 'tier': 'approved'}))[0], 400)
        # an untiered claim older than 7 days needs a call and fires BRN-R13
        rows = self.section('claims')
        rows.append({'id': 'bombas.claims.arch_relief', 'brand': 'bombas', 'section': 'claims', 'field': 'arch_relief', 'value': 'benefit claim', 'text': 'Arch support relieves foot pain on long shifts.',
                     'tier': 'unverified', 'source': {'type': 'agent', 'ref': 'draft', 'captured_at': '2026-09-10'}})
        self.write('claims', rows)
        cd = api.handle(Req(['claims']))
        self.assertEqual(next(c for c in cd['claims'] if c['field'] == 'arch_relief')['verdict']['kind'], 'fix')
        f = next(f for f in api.handle(Req(['audit']))['findings'] if f['id'] == '05-brand-brain.BRN-R13.claim_arch_relief')
        self.assertEqual((f['severity'], f['capability']['id']), ('medium', 'BRN-C03'))
        self.assertIn('18 days', f['sentence'])
        a = next(a for a in api.rank('bombas', {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4})['actions'] if a['rule_id'] == 'BRN-R13')
        self.assertEqual((a['owner'], a['rubric']['reputation']), ('person', 5))

    def test_scanner_blocks_stale_numbers_and_forbidden_phrases(self):
        api.handle(Req(['claims'], 'POST', body={'text': 'the softest socks in the world', 'tier': 'forbidden'}))
        r = api.handle(Req(['scan'], 'POST', body={'text': 'The softest socks in the world. Free shipping on orders over $50. Returns within 60 days. Clinically proven comfort.'}))
        self.assertEqual(r['verdict'], 'fail')
        kinds = [h['kind'] for h in r['hits']]
        self.assertIn('forbidden', kinds)
        self.assertEqual(kinds.count('stale_fact'), 2)
        self.assertIn('needs_proof', kinds)
        stale = next(h for h in r['hits'] if h['kind'] == 'stale_fact' and 'shipping' in h['match'].lower())
        self.assertEqual(stale['record'], 'bombas.offers.free_shipping_threshold_usd')
        self.assertIn('75', stale['fix'])
        ok = api.handle(Req(['scan'], 'POST', body={'text': 'Free shipping on orders over $75. Returns within 30 days. Every pair gives a pair.'}))
        self.assertEqual((ok['verdict'], ok['hits']), ('pass', []))
        self.assertLess(ok['reading_grade'], 10)
        self.assertEqual(api.handle(Req(['scan'], 'POST', body={'text': '  '}))[0], 400)

    def test_scanner_flags_unapproved_claim_and_reading_grade(self):
        rows = self.section('claims')
        for r in rows:
            if r['id'] == 'bombas.claims.ankle_socks_benefit':
                r['tier'] = 'inferred'
        self.write('claims', rows)
        r = api.handle(Req(['scan'], 'POST', body={'text': 'Our ankle socks are moisture-wicking with a blister tab, a cushioned footbed and Honeycomb arch support.'}))
        self.assertEqual(r['verdict'], 'warn')
        self.assertEqual(r['hits'][0]['kind'], 'unapproved')
        self.assertEqual(r['hits'][0]['record'], 'bombas.claims.ankle_socks_benefit')
        hard = 'Notwithstanding the aforementioned considerations, our organisation systematically operationalises multidimensional comfort methodologies across heterogeneous consumer populations, thereby facilitating unprecedented satisfaction outcomes.'
        r = api.handle(Req(['scan'], 'POST', body={'text': hard}))
        self.assertTrue(any(h['kind'] == 'reading_level' for h in r['hits']))


class Round2SiteDiff(TempBrain):
    """Round 2 feature 2: the diff between the two newest site snapshots, each change ending in an action."""

    def second_crawl(self, value=80, date='2026-10-05'):
        p = self.tmp / 'bombas' / 'raw' / 'a-site' / 'offers.json'
        rows = json.loads(p.read_text(encoding='utf-8'))
        rows[0]['value'] = value
        rows[0]['source']['captured_at'] = date
        p.write_text(json.dumps(rows), encoding='utf-8')

    def test_one_snapshot_is_unavailable_not_a_fake_diff(self):
        sd = api.handle(Req(['site', 'diff']))
        self.assertEqual(len(sd['snapshots']), 1)
        self.assertEqual(sd['snapshots'][0]['date'], DAY)
        self.assertIsNone(sd['counts']['changes'])
        self.assertIn('next crawl', sd['unavailable_reason'])
        self.assertEqual(api.handle(Req(['site', 'reviewed'], 'POST', body={'ids': ['x']}))[0], 400)
        self.assertFalse([f for f in api.handle(Req(['audit']))['findings'] if f['rule_id'] == 'BRN-R14'])

    def test_second_snapshot_gives_changes_with_actions_and_rule(self):
        api.handle(Req(['site', 'diff']))
        self.second_crawl()
        status, res = api.handle(Req(['site', 'snapshot'], 'POST', body={}))
        self.assertEqual((status, res['date']), (201, '2026-10-05'))
        sd = api.handle(Req(['site', 'diff']))
        self.assertEqual(sd['pair'], DAY + '..2026-10-05')
        self.assertEqual(sd['counts'], {'changes': 1, 'open': 1, 'high': 1, 'by_section': {'offers': 1}})
        c = sd['changes'][0]
        self.assertEqual((c['id'], c['change'], c['old'], c['new'], c['severity']), ('bombas.offers.free_shipping_threshold_usd', 'changed', 75, 80, 'high'))
        self.assertEqual(c['action']['owner'], 'agent_drafts')
        f = next(f for f in api.handle(Req(['audit']))['findings'] if f['rule_id'] == 'BRN-R14')
        self.assertEqual((f['severity'], f['capability']['id']), ('high', 'BRN-C01'))
        self.assertIn('changed from 75 to 80', f['sentence'])
        a = next(a for a in api.rank('bombas', {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4})['actions'] if a['rule_id'] == 'BRN-R14')
        self.assertTrue(a['title'].startswith('Carry the new free shipping threshold'))
        self.assertEqual(api.rank_mod.validate_action(a), [])
        status, res = api.handle(Req(['site', 'reviewed'], 'POST', body={'ids': [c['id']]}))
        self.assertEqual((status, res['reviewed']), (201, 1))
        sd = api.handle(Req(['site', 'diff']))
        self.assertEqual(sd['counts']['open'], 0)
        self.assertTrue(sd['changes'][0]['reviewed'])
        self.assertFalse([f for f in api.handle(Req(['audit']))['findings'] if f['rule_id'] == 'BRN-R14'])


class Round2Parity(TempBrain):
    """Round 2 feature 3: marketplace listings against the site, MAP and seller checks, unavailable until set."""

    def test_strip_reads_pack_price_and_floor(self):
        pv = api.handle(Req(['parity']))
        self.assertEqual(pv['counts']['listings'], 34)
        self.assertIsNone(pv['counts']['below_map'])       # MAP unset: unavailable, not 0
        self.assertIsNone(pv['counts']['unrecognised'])
        self.assertEqual(pv['counts']['seller_unknown'], 34)
        four = next(l for l in pv['listings'] if l['asin'] == 'B0CVLKH8M2')
        self.assertEqual((four['pack'], four['line'], four['site_floor_usd']), (4, 'socks', 13.0))
        self.assertAlmostEqual(four['per_pair_usd'], round(four['price_usd'] / 4, 2))
        self.assertEqual(api.parity.pack_count("Women's Solids Ankle White Socks Medium (4 Pack)"), 4)
        self.assertEqual(api.parity.pack_count('Single sock'), 1)
        kinds = {f['entity']['id']: f for f in api.handle(Req(['audit']))['findings'] if f['rule_id'] in ('BRN-R15', 'BRN-R16')}
        self.assertEqual(kinds['map_unset']['status'], 'unavailable')
        self.assertEqual(kinds['seller_unknown']['status'], 'unavailable')
        self.assertIn('Selling Partner', kinds['seller_unknown']['unavailable']['connector'])

    def test_map_and_sellers_turn_checks_on(self):
        status, res = api.handle(Req(['parity', 'map'], 'POST', body={'usd': '9.00'}))
        self.assertEqual((status, res['record']), (201, 'bombas.offers.map_usd_per_pair'))
        pv = api.handle(Req(['parity']))
        self.assertEqual(pv['map_usd_per_pair'], 9.0)
        self.assertGreater(pv['counts']['below_map'], 0)
        worst = pv['listings'][0]
        self.assertEqual(worst['verdict']['kind'], 'stop')
        f = next(f for f in api.handle(Req(['audit']))['findings'] if f['rule_id'] == 'BRN-R15' and f['status'] == 'open')
        self.assertEqual(f['entity']['type'], 'sku')
        self.assertIn('below your $9.00 minimum', f['sentence'])
        a = next(a for a in api.rank('bombas', {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4})['actions'] if a['rule_id'] == 'BRN-R15' and a['status'] == 'open')
        self.assertTrue(a['title'].startswith('Send a MAP notice'))
        self.assertEqual(a['rubric']['reputation'], 5)
        # sellers: set the list, then a listing with a foreign seller is unrecognised
        rows = self.section('marketplaces')
        rows[0]['value']['seller'] = 'SockDealsUSA'
        self.write('marketplaces', rows)
        status, res = api.handle(Req(['parity', 'sellers'], 'POST', body={'names': 'Bombas, Bombas LLC'}))
        self.assertEqual(status, 201)
        pv = api.handle(Req(['parity']))
        self.assertEqual(pv['counts']['unrecognised'], 1)
        f = next(f for f in api.handle(Req(['audit']))['findings'] if f['rule_id'] == 'BRN-R16' and f['status'] == 'open')
        self.assertIn('SockDealsUSA', f['sentence'])
        self.assertEqual(api.handle(Req(['parity', 'map'], 'POST', body={'usd': 'abc'}))[0], 400)
        self.assertEqual(api.handle(Req(['parity', 'nope'], 'POST', body={}))[0], 404)


class Round2Contracts(TempBrain):
    """Round 2 feature 4: the vendor contract register with alert windows by vendor type."""

    def test_known_vendors_without_contract(self):
        cr = api.handle(Req(['contracts']))
        self.assertEqual(cr['counts']['on_file'], 0)
        self.assertGreaterEqual(cr['counts']['known_without_contract'], 8)
        names = {c['vendor'] for c in cr['contracts']}
        self.assertIn('Shopify', names)
        self.assertIn('Flexport', names)
        self.assertNotIn('custom React storefront theme', names)
        self.assertTrue(all(c['verdict']['kind'] == 'wait' and c['action']['owner'] == 'person' for c in cr['contracts']))
        self.assertIsNone(cr['next'])
        f = next(f for f in api.handle(Req(['audit']))['findings'] if f['rule_id'] == 'BRN-R18')
        self.assertEqual(f['entity']['id'], 'contracts_missing')
        self.assertIn('no contract on file', f['sentence'])

    def test_add_contract_inside_window_fires_and_calendar(self):
        status, res = api.handle(Req(['contracts'], 'POST', body={'vendor': 'Flexport', 'type': '3pl', 'renewal_date': '2026-11-30', 'notice_days': 60, 'rate_card': '$4.10 per order'}))
        self.assertEqual((status, res['window_days']), (201, 90))
        cr = api.handle(Req(['contracts']))
        c = next(x for x in cr['contracts'] if x['vendor'] == 'Flexport')
        self.assertEqual((c['on_file'], c['days_left'], c['verdict']['kind']), (True, 63, 'stop'))
        self.assertEqual(cr['next']['vendor'], 'Flexport')
        self.assertEqual(cr['calendar'][0]['days_left'], 63)
        self.assertEqual(cr['counts']['known_without_contract'], sum(1 for x in cr['contracts'] if not x['on_file']))
        f = next(f for f in api.handle(Req(['audit']))['findings'] if f['rule_id'] == 'BRN-R17')
        self.assertEqual(f['severity'], 'high')
        self.assertIn('renews in 63 days; last terms were $4.10 per order', f['sentence'])
        a = next(a for a in api.rank('bombas', {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4})['actions'] if a['rule_id'] == 'BRN-R17')
        self.assertTrue(a['title'].startswith('Renegotiate or renew Flexport'))
        status, res = api.handle(Req(['contracts'], 'POST', body={'vendor': 'Yotpo', 'type': 'app'}))
        self.assertEqual(status, 201)
        cr = api.handle(Req(['contracts']))
        self.assertEqual(next(x for x in cr['contracts'] if x['vendor'] == 'Yotpo')['verdict']['kind'], 'fix')
        self.assertTrue([f for f in api.handle(Req(['audit']))['findings'] if f['rule_id'] == 'BRN-R18' and f['entity']['id'] == 'contract_yotpo'])
        self.assertEqual(api.handle(Req(['contracts'], 'POST', body={'vendor': 'X', 'renewal_date': 'soon'}))[0], 400)


class Round2Legal(TempBrain):
    """Round 2 feature 5: the US disclosure checks and the gate for a pasted draft."""

    def test_site_checks_pass_fail_unavailable_na(self):
        lg = api.handle(Req(['legal']))
        by = {c['key']: c for c in lg['checks']}
        self.assertEqual(by['privacy_policy']['status'], 'pass')
        self.assertEqual(by['cookie_consent']['status'], 'pass')
        self.assertEqual(by['can_spam']['status'], 'unavailable')
        self.assertEqual(by['auto_renewal']['status'], 'na')
        self.assertEqual(lg['counts']['fail'], 0)
        self.assertFalse([f for f in api.handle(Req(['audit']))['findings'] if f['rule_id'] == 'BRN-R19'])
        rows = [r for r in self.section('stack') if r.get('field') != 'cookie_consent']
        self.write('stack', rows)
        by = {c['key']: c for c in api.handle(Req(['legal']))['checks']}
        self.assertEqual(by['cookie_consent']['status'], 'fail')
        self.assertEqual(by['cookie_consent']['action']['owner'], 'person')
        f = next(f for f in api.handle(Req(['audit']))['findings'] if f['rule_id'] == 'BRN-R19')
        self.assertEqual((f['severity'], f['capability']['id'], f['entity']['id']), ('high', 'LOOP-C27', 'cookie_consent'))
        a = next(a for a in api.rank('bombas', {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4})['actions'] if a['rule_id'] == 'BRN-R19')
        self.assertEqual(a['rubric']['reputation'], 5)

    def test_gate_by_kind(self):
        r = api.handle(Req(['legal', 'gate'], 'POST', body={'kind': 'email', 'text': 'Big sale this week. Free shipping over $75.'}))
        self.assertEqual((r['verdict'], {m['key'] for m in r['missing']}), ('fail', {'unsubscribe', 'postal_address'}))
        r = api.handle(Req(['legal', 'gate'], 'POST', body={'kind': 'email', 'text': 'Big sale. Unsubscribe any time. Bombas, 881 Broadway, New York, NY 10003.'}))
        self.assertEqual(r['verdict'], 'pass')
        r = api.handle(Req(['legal', 'gate'], 'POST', body={'kind': 'ad', 'text': 'Our creator partner wears them on every shift.'}))
        self.assertEqual(r['missing'][0]['key'], 'paid_disclosure')
        r = api.handle(Req(['legal', 'gate'], 'POST', body={'kind': 'ad', 'text': 'Paid partnership. Our creator wears them on every shift.'}))
        self.assertEqual(r['verdict'], 'pass')
        r = api.handle(Req(['legal', 'gate'], 'POST', body={'kind': 'subscription', 'text': 'Socks every month.'}))
        self.assertEqual({m['key'] for m in r['missing']}, {'auto_renewal_terms', 'cancellation', 'renewal_price'})
        r = api.handle(Req(['legal', 'gate'], 'POST', body={'kind': 'pdp', 'text': 'Free shipping over $50. Rated 4.8 from 12,000 reviews.'}))
        self.assertEqual(r['verdict'], 'fail')     # a stale brain number from the claims scanner also blocks
        self.assertTrue(any(h['kind'] == 'stale_fact' for h in r['claims']['hits']))
        self.assertEqual(api.handle(Req(['legal', 'gate'], 'POST', body={'kind': 'email', 'text': ' '}))[0], 400)


class Round2Voice(TempBrain):
    """Round 2 features 6 and 7: the voice sheet with examples, and the approved snippets with a stale check."""

    def test_sheet_fields_examples_and_text(self):
        vs = api.handle(Req(['voice']))
        self.assertEqual((vs['filled'], vs['of'], vs['ready']), (0, 8, False))
        self.assertEqual(len(vs['site_lines']), 3)
        self.assertIn('unavailable (founder to add)', vs['sheet_text'])
        api.handle(Req(['profile', 'voice', 'words_avoided'], 'POST', body={'text': 'premium, elevate, leverage'}))
        status, res = api.handle(Req(['voice', 'example'], 'POST', body={'kind': 'liked', 'text': 'Socks so comfortable you forget you have them on.', 'why': 'plain, one benefit'}))
        self.assertEqual((status, res['count']), (201, 1))
        api.handle(Req(['voice', 'example'], 'POST', body={'kind': 'disliked', 'text': 'Elevate your sock game with premium comfort technology.'}))
        vs = api.handle(Req(['voice']))
        self.assertEqual((vs['filled'], len(vs['examples']['liked']), len(vs['examples']['disliked'])), (1, 1, 1))
        self.assertIn('Copy we like:', vs['sheet_text'])
        self.assertIn('Words we avoid: premium, elevate, leverage', vs['sheet_text'])
        prof = api.handle(Req(['profile']))
        keys = [f['key'] for sec in prof['sections'] if sec['section'] == 'voice' for f in sec['fields']]
        self.assertEqual(keys[:3], ['adjectives', 'writes_like', 'do_list'])
        # the scanner reads the avoid list
        r = api.handle(Req(['scan'], 'POST', body={'text': 'Elevate your everyday with our premium socks.'}))
        self.assertEqual(sorted(h['match'] for h in r['hits'] if h['kind'] == 'avoided_word'), ['elevate', 'premium'])
        self.assertEqual(api.handle(Req(['voice', 'example'], 'POST', body={'kind': 'meh', 'text': 'x'}))[0], 400)

    def test_snippets_built_locked_and_stale(self):
        sn = api.handle(Req(['voice']))['snippets']
        by = {r['key']: r for r in sn['snippets']}
        self.assertEqual(by['free_shipping']['use'], 'Free shipping on orders over $75.')
        self.assertEqual(by['returns']['use'], 'Returns within 30 days, refunded to the original payment method.')
        self.assertEqual(by['first_order']['status'], 'proposed')
        self.assertEqual(sn['counts']['stale'], 0)
        status, res = api.handle(Req(['voice', 'snippet', 'free_shipping'], 'POST', body={'text': 'Free shipping on every order over $75, no code needed.'}))
        self.assertEqual((status, res['status']), (201, 'locked'))
        # the threshold moves on the site: the locked line is stale and ends in a re-approve action
        rows = self.section('offers')
        for r in rows:
            if r['id'] == 'bombas.offers.free_shipping_threshold_usd':
                r['value'] = 80
        self.write('offers', rows)
        by = {r['key']: r for r in api.handle(Req(['voice']))['snippets']['snippets']}
        self.assertEqual(by['free_shipping']['status'], 'stale')
        self.assertEqual(by['free_shipping']['use'], 'Free shipping on orders over $80.')   # the stale lock is not pasted
        self.assertEqual(by['free_shipping']['action']['owner'], 'person')
        self.assertEqual(api.handle(Req(['voice', 'snippet', 'nope'], 'POST', body={'text': 'x y z w'}))[0], 404)


class Round2BattlecardsAsk(TempBrain):
    """Round 2 features 8 and 9: battlecards per competitor, and ask the brain with sources."""

    def test_cards_from_the_brain(self):
        bc = api.handle(Req(['battlecards']))
        self.assertEqual(bc['counts']['cards'], 5)
        by = {c['competitor']: c for c in bc['cards']}
        dt_ = by['Darn Tough Vermont']
        self.assertEqual(dt_['verdict']['kind'], 'stop')
        self.assertEqual(dt_['recommended_instead']['threads'], 4)
        self.assertIn('Durability and guarantee', [a['label'] for a in dt_['they_win']])
        self.assertTrue(any(w['line'] for w in dt_['how_we_win']))
        self.assertIn('Never their text, logos, products or faces', dt_['text'])
        self.assertNotIn('u/', dt_['text'])
        self.assertEqual(bc['cards'][0]['verdict']['kind'], 'stop')

    def test_ask_answers_with_tier_and_source(self):
        r = api.handle(Req(['ask'], query={'q': ['what is the free shipping threshold']}))
        self.assertEqual(r['answers'][0]['id'], 'bombas.offers.free_shipping_threshold_usd')
        self.assertEqual(r['answers'][0]['tier'], 'site_backed')
        self.assertTrue(r['answers'][0]['source']['link'].startswith('https://'))
        self.assertIsNone(r['can_we_say'])
        r = api.handle(Req(['ask'], query={'q': ['can we say our socks are the most comfortable']}))
        self.assertEqual(r['can_we_say']['verdict'], 'needs_proof')
        r = api.handle(Req(['ask'], query={'q': ['can we say every item purchased donates one item']}))
        self.assertEqual((r['can_we_say']['verdict'], r['can_we_say']['record']), ('yes', 'bombas.claims.donation_pledge'))
        api.handle(Req(['claims'], 'POST', body={'text': 'the softest socks in the world', 'tier': 'forbidden'}))
        r = api.handle(Req(['ask'], query={'q': ['can we say the softest socks in the world']}))
        self.assertEqual(r['can_we_say']['verdict'], 'never')
        self.assertEqual(api.handle(Req(['ask'], query={'q': ['']}))['answers'], [])

    def test_unanswered_becomes_an_open_question(self):
        status, res = api.handle(Req(['ask', 'open'], 'POST', body={'q': 'What is the warranty on slippers?', 'why': 'asked by CX'}))
        self.assertEqual(status, 201)
        rec = next(r for r in self.section('open_questions') if r['id'] == res['record'])
        self.assertEqual(rec['value']['question'], 'What is the warranty on slippers?')
        qv = api.handle(Req(['questions']))
        self.assertIn(res['record'], {q['id'] for q in qv['questions']})
        self.assertEqual(api.handle(Req(['ask', 'open'], 'POST', body={'q': 'x'}))[0], 400)


class Round2PermissionsExport(TempBrain):
    """Round 2 feature 10: the permission map, restricted by default, and the brain export."""

    def test_defaults_and_set(self):
        pm = api.handle(Req(['permissions']))
        self.assertEqual([c['key'] for c in pm['cols']], ['founder', 'in_house', 'agency', 'specialist'])
        by = {s['key']: s for s in pm['sections']}
        self.assertEqual(by['claims']['levels'], {'founder': 'full', 'in_house': 'read', 'agency': 'none', 'specialist': 'none'})
        self.assertEqual(by['economics']['levels']['in_house'], 'read')
        self.assertEqual(pm['counts']['explicit'], 0)
        f = next(f for f in api.handle(Req(['audit']))['findings'] if f['rule_id'] == 'BRN-R20')
        self.assertEqual((f['severity'], f['capability']['id']), ('low', 'LOOP-C29'))
        status, res = api.handle(Req(['permissions', 'claims'], 'POST', body={'roles': {'agency': 'read', 'specialist': 'read', 'in_house': 'full'}}))
        self.assertEqual((status, res['roles']['founder'], res['roles']['agency']), (201, 'full', 'read'))
        pm = api.handle(Req(['permissions']))
        by = {s['key']: s for s in pm['sections']}
        self.assertTrue(by['claims']['explicit'])
        self.assertEqual(by['claims']['levels']['agency'], 'read')
        self.assertEqual(pm['cells']['claims']['agency']['us'], 1)
        self.assertEqual(api.handle(Req(['permissions', 'claims'], 'POST', body={'roles': {'agency': 'owner'}}))[0], 400)
        self.assertEqual(api.handle(Req(['permissions', 'freshness'], 'POST', body={'roles': {'agency': 'read'}}))[0], 404)

    def test_export_carries_everything(self):
        api.handle(Req(['documents'], 'POST', body={'name': 'notes.md', 'text': '# Offers\nFree shipping threshold: $75'}))
        b = api.handle(Req(['export']))
        self.assertEqual(b['brand'], 'bombas')
        self.assertGreaterEqual(b['counts']['records'], 600)
        self.assertIn('claims', b['sections'])
        self.assertEqual(b['counts']['documents'], 1)
        self.assertEqual(len(b['document_files']), 1)
        self.assertTrue(b['router_md'].startswith('#') or b['router_md'] == '')
        self.assertEqual(b['version'], api.Brain('bombas', self.tmp, dt.date.fromisoformat(DAY)).version())
        self.assertIn('revoke', b['note'])


class Round3ChangesTrace(TempBrain):
    """Round 3 features 1 and 2: the changes log with versions, and the fact-to-asset trace."""

    def test_every_write_logs_a_change_with_before(self):
        self.assertEqual(api.handle(Req(['changes']))['counts']['total'], 0)
        api.handle(Req(['profile', 'offers', 'free_shipping_threshold_usd'], 'POST', body={'text': '80'}))
        api.handle(Req(['approve', 'bombas.positioning.frame'], 'POST', body={'choice': 'approve'}))
        api.handle(Req(['documents'], 'POST', body={'name': 'n.md', 'text': '# Offers\nBundle: 4 pack saves 10 percent'}))
        ch = api.handle(Req(['changes']))
        kinds = [x['kind'] for x in ch['changes']]
        self.assertIn('founder_edit', kinds)
        self.assertIn('approve', kinds)
        self.assertIn('document', kinds)
        edit = next(x for x in ch['changes'] if x['kind'] == 'founder_edit')
        self.assertEqual((edit['before'], edit['after'], edit['section']), ('75', '80.0', 'offers'))
        self.assertGreaterEqual(ch['counts']['week'], 3)
        self.assertGreaterEqual(len(ch['versions']), 2)
        self.assertNotEqual(ch['versions'][0]['before'], ch['versions'][0]['after'])
        self.assertTrue((self.tmp / 'bombas' / 'changes.json').is_file())

    def test_site_change_logs_with_dependents(self):
        api.handle(Req(['site', 'diff']))
        Round2SiteDiff.second_crawl(self)
        api.handle(Req(['site', 'snapshot'], 'POST', body={}))
        ch = api.handle(Req(['changes']))
        site = next(x for x in ch['changes'] if x['kind'] == 'site')
        self.assertIn('75 to 80', site['what'])
        self.assertIn('Depends on it', site['what'])
        self.assertEqual(site['source'], 'site crawl')

    def test_dependents_find_ads_rungs_and_snippets(self):
        d = api.handle(Req(['dependents'], query={'record': ['bombas.offers.first_order_code_confirmed']}))
        self.assertEqual(d['ads'], 23)
        self.assertTrue(any(x['kind'] == 'ads' and '21 active ads' in x['surfaces'] for x in d['dependents']))
        d = api.handle(Req(['dependents'], query={'record': ['bombas.claims.calf_socks_benefit']}))
        self.assertEqual(d['counts'].get('rung'), 2)
        api.handle(Req(['voice', 'snippet', 'free_shipping'], 'POST', body={'text': 'Free shipping on orders over $75.'}))
        d = api.handle(Req(['dependents'], query={'record': ['bombas.offers.free_shipping_threshold_usd']}))
        self.assertIn('snippet', d['counts'])
        self.assertEqual(api.handle(Req(['dependents'], query={'record': ['nope']}))[0], 400)
        self.assertIn('reason', api.handle(Req(['dependents'], query={'record': ['bombas.offers.nope']})))


class Round3Assumptions(TempBrain):
    """Round 3 feature 3: the assumptions register with confirm and correct."""

    def test_register_and_rule(self):
        ar = api.handle(Req(['assumptions']))
        self.assertEqual(ar['total'], 12)
        by = {a['field']: a for a in ar['assumptions']}
        self.assertEqual(by['gross_margin']['status'], 'modelled')
        self.assertEqual(by['aov_usd']['status'], 'founder')
        self.assertIn('finance', by['gross_margin']['rooms'])
        self.assertEqual(ar['assumptions'][0]['status'], 'modelled')   # modelled first
        f = next(f for f in api.handle(Req(['audit']))['findings'] if f['id'] == '05-brand-brain.BRN-R21.assumption_gross_margin')
        self.assertEqual((f['severity'], f['capability']['id'], f['entity']['type']), ('medium', 'BRN-C07', 'metric'))
        a = next(a for a in api.rank('bombas', {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4})['actions'] if a['rule_id'] == 'BRN-R21')
        self.assertTrue(a['title'].startswith('Confirm or correct'))

    def test_confirm_and_correct_write_founder_records(self):
        status, res = api.handle(Req(['assumptions', 'gross_margin'], 'POST', body={'choice': 'confirm'}))
        self.assertEqual((status, res['record'], res['status']), (201, 'bombas.economics.gross_margin_model', 'founder'))
        by = {a['field']: a for a in api.handle(Req(['assumptions']))['assumptions']}
        self.assertEqual(by['gross_margin']['status'], 'founder')
        self.assertFalse([f for f in api.handle(Req(['audit']))['findings'] if f['id'] == '05-brand-brain.BRN-R21.assumption_gross_margin'])
        status, res = api.handle(Req(['assumptions', 'return_share'], 'POST', body={'value': '3.8'}))
        self.assertEqual(status, 201)
        rec = next(r for r in self.section('economics') if r['id'] == 'bombas.economics.return_share_model')
        self.assertEqual((rec['value'], rec['tier'], rec['source']['type']), (3.8, 'approved', 'founder'))
        self.assertEqual(api.handle(Req(['assumptions', 'nope'], 'POST', body={'choice': 'confirm'}))[0], 404)
        self.assertEqual(api.handle(Req(['assumptions', 'return_share'], 'POST', body={}))[0], 400)


class Round3Facts(TempBrain):
    """Round 3 feature 4: store facts for AI shopping agents, built from records, approved once, exported."""

    def test_pairs_built_from_records(self):
        fp = api.handle(Req(['facts']))
        by = {r['key']: r for r in fp['pairs']}
        self.assertEqual(by['free_shipping']['answer'], 'Yes. Standard shipping is free on orders over $75.')
        self.assertIn('30 days', by['returns']['answer'])
        self.assertEqual(by['ship_where']['status'], 'unavailable')
        self.assertEqual(fp['counts']['approved'], 0)
        self.assertEqual(api.handle(Req(['facts', 'export']))['count'], 0)

    def test_approve_export_and_stale(self):
        status, res = api.handle(Req(['facts', 'free_shipping'], 'POST', body={'answer': 'Yes. Standard shipping is free on every order over $75.'}))
        self.assertEqual((status, res['status']), (201, 'approved'))
        api.handle(Req(['facts', 'ship_where'], 'POST', body={'answer': 'We ship to every US state.'}))
        e = api.handle(Req(['facts', 'export']))
        self.assertEqual(e['count'], 2)
        self.assertEqual(e['jsonld']['@type'], 'FAQPage')
        self.assertIn('Q: Where do you ship?', e['text'])
        rows = self.section('offers')
        for r in rows:
            if r['id'] == 'bombas.offers.free_shipping_threshold_usd':
                r['value'] = 80
        self.write('offers', rows)
        by = {r['key']: r for r in api.handle(Req(['facts']))['pairs']}
        self.assertEqual(by['free_shipping']['status'], 'stale')
        self.assertEqual(api.handle(Req(['facts', 'export']))['count'], 1)
        self.assertEqual(api.handle(Req(['facts', 'nope'], 'POST', body={'answer': 'x y z w'}))[0], 404)


class Round3Channels(TempBrain):
    """Round 3 feature 5: channel rule sets on top of the brain scan."""

    def test_channel_rules(self):
        r = api.handle(Req(['scan'], 'POST', body={'text': 'Free shipping on every 4 pack. Best seller. See www.example.com', 'channel': 'amazon'}))
        self.assertEqual(r['channel'], 'amazon')
        kinds = [h['match'] for h in r['channel_hits']]
        self.assertTrue(any('promotional' in m for m in kinds))
        self.assertTrue(any('external links' in m for m in kinds))
        self.assertEqual(r['verdict'], 'fail')
        r = api.handle(Req(['scan'], 'POST', body={'text': 'Shop the 4 pack now!', 'channel': 'google'}))
        self.assertTrue(any('exclamation' in h['match'] for h in r['channel_hits']))
        r = api.handle(Req(['scan'], 'POST', body={'text': 'Socks so soft you forget them. Reply STOP to opt out. From Bombas.', 'channel': 'sms'}))
        self.assertEqual((r['verdict'], r['channel_hits']), ('pass', []))
        r = api.handle(Req(['scan'], 'POST', body={'text': 'Socks so soft you forget them.', 'channel': 'sms'}))
        self.assertEqual({h['kind'] for h in r['channel_hits']}, {'channel_missing'})
        r = api.handle(Req(['scan'], 'POST', body={'text': 'Are you overweight? Try our socks.', 'channel': 'meta'}))
        self.assertEqual(r['channel_hits'][0]['severity'], 'fail')
        r = api.handle(Req(['scan'], 'POST', body={'text': 'Plain line.', 'channel': 'nope'}))
        self.assertIsNone(r['channel'])
        self.assertEqual(r['channels'], ['amazon', 'email', 'google', 'meta', 'sms'])


class Round3Package(TempBrain):
    """Round 3 feature 6: what an agent reads, the T1 summaries and the package for a capability."""

    def test_summaries_and_package(self):
        sm = api.handle(Req(['summaries']))
        by = {r['section']: r for r in sm['sections']}
        self.assertTrue(by['claims']['text'].startswith('## claims (T1): 6 records'))
        self.assertGreater(by['claims']['tokens'], 20)
        self.assertGreater(sm['t0_tokens'], 50)
        p = api.handle(Req(['package'], query={'capability': ['CREA-C06']}))
        self.assertEqual(p['capability'], 'CREA-C06')
        self.assertLessEqual(p['tokens'], p['budget'])
        self.assertEqual(p['parts'][0]['tier'], 'T0')
        self.assertTrue(any(x['tier'] == 'T1' for x in p['parts']))
        self.assertEqual(api.handle(Req(['package'], query={'capability': ['nope']}))[0], 400)
        self.assertEqual(api.handle(Req(['package'], query={'capability': ['ZZZ-C99']}))[0], 404)


class Round3Learn(TempBrain):
    """Round 3 feature 7: words the founder cuts and adds across edits, proposed to the voice sheet."""

    def test_edits_become_proposals_and_apply(self):
        start = api.handle(Req(['learn']))['counts']   # the sample brain already holds a few founder edits with history
        self.assertNotIn('premium', {p['word'] for p in api.handle(Req(['learn']))['avoid']})
        api.handle(Req(['profile', 'positioning', 'frame'], 'POST', body={'text': 'Premium everyday comfort you can feel on the first wear.'}))
        api.handle(Req(['profile', 'positioning', 'frame'], 'POST', body={'text': 'Everyday comfort you can feel on the first wear, and a pair given for every pair.'}))
        api.handle(Req(['profile', 'identity', 'one_line_pitch'], 'POST', body={'text': 'Premium socks engineered to elevate comfort.'}))
        api.handle(Req(['profile', 'identity', 'one_line_pitch'], 'POST', body={'text': 'Socks made for comfort you feel, and a pair given for every pair.'}))
        lv = api.handle(Req(['learn']))
        self.assertGreaterEqual(lv['counts']['edits'], start['edits'] + 2)
        avoid = {p['word']: p for p in lv['avoid']}
        self.assertIn('premium', avoid)
        self.assertEqual(avoid['premium']['times'], 2)
        self.assertIn('elevate', avoid)      # hype word, cut once
        use = {p['word'] for p in lv['use']}
        self.assertIn('given', use)
        self.assertTrue(avoid['premium']['evidence'][0]['before'])
        status, res = api.handle(Req(['learn', 'apply'], 'POST', body={'kind': 'avoided', 'words': ['premium', 'elevate']}))
        self.assertEqual((status, res['words']), (201, ['premium', 'elevate']))
        vs = api.handle(Req(['voice']))
        self.assertEqual(next(f for f in vs['fields'] if f['key'] == 'words_avoided')['text'], 'premium, elevate')
        self.assertNotIn('premium', {p['word'] for p in api.handle(Req(['learn']))['avoid']})
        r = api.handle(Req(['scan'], 'POST', body={'text': 'Premium comfort.'}))
        self.assertTrue(any(h['kind'] == 'avoided_word' for h in r['hits']))
        self.assertEqual(api.handle(Req(['learn', 'apply'], 'POST', body={'kind': 'x', 'words': ['a']}))[0], 400)


class Round3ReportDigest(TempBrain):
    """Round 3 features 8 and 10: the weekly report and the founder round digest, in plain words."""

    def test_report_reads_the_week(self):
        api.handle(Req(['profile', 'offers', 'free_shipping_threshold_usd'], 'POST', body={'text': '80'}))
        api.handle(Req(['questions', 'bank', 'q.economics.gross_margin'], 'POST', body={'answer': '58%'}))
        rp = api.handle(Req(['report'], query={'days': ['7']}))
        self.assertTrue(rp['text'].startswith('Brand brain, week to ' + DAY))
        self.assertGreaterEqual(rp['counts']['changes'], 2)
        self.assertEqual(rp['counts']['questions_answered'], 1)
        self.assertIn('Top moves from the brain screen:', rp['text'])
        self.assertGreaterEqual(rp['counts']['top'], 3)
        self.assertNotIn('—', rp['text'])
        self.assertIn('Site: 1 snapshot on file', rp['text'])
        self.assertEqual(api.handle(Req(['report'], query={'days': ['x']}))['days'], 7)

    def test_digest_is_the_founder_round(self):
        dg = api.handle(Req(['digest']))
        self.assertEqual(dg['questions'], 5)
        self.assertIn('1. What is your gross margin', dg['text'])
        self.assertIn('Pull first', dg['text'])
        self.assertIn('Approve today:', dg['text'])
        self.assertIsNone(dg['delivery']['slack'])
        api.handle(Req(['documents'], 'POST', body={'name': 'n.md', 'text': '# Offers\nFree shipping threshold: $75\n- Bundles: 4 pack saves 10 percent'}))
        dg = api.handle(Req(['digest']))
        self.assertGreaterEqual(dg['proposed'], 1)


class Round3Review(TempBrain):
    """Round 3 feature 9: the review queue grouped by source with the record each proposal would replace, and bulk actions."""

    def test_grouped_with_before_and_bulk(self):
        # the active value is set here, so the test never depends on what the repo brain holds today
        api.handle(Req(['profile', 'offers', 'free_shipping_threshold_usd'], 'POST', body={'text': '75'}))
        api.handle(Req(['documents'], 'POST', body={'name': 'call.md', 'text': '# Offers\nFree shipping threshold: $75\nFirst order code: WELCOME25\n- Bundles: 4 pack saves 10 percent\n\n# Voice\nWe write like a friend who knows socks and never oversells.'}))
        rv = api.handle(Req(['review']))
        self.assertEqual(rv['counts']['groups'], 1)
        g = rv['groups'][0]
        self.assertTrue(g['source'].endswith('call.md'))
        fs = next(r for r in g['records'] if r['id'].endswith('_free_shipping_threshold'))
        self.assertEqual((fs['change'], fs['before']['id']), ('same value', 'bombas.offers.free_shipping_threshold_usd'))
        fo = next(r for r in g['records'] if r['id'].endswith('_first_order_code'))
        self.assertEqual(fo['change'], 'replaces')
        self.assertIn(fo['before']['id'], ('bombas.offers.first_order_code', 'bombas.offers.first_order_code_confirmed'))
        voice = next(r for r in g['records'] if r['section'] == 'voice')
        self.assertEqual(voice['change'], 'new field')
        self.assertEqual(rv['counts']['duplicates'], 1)
        adds = [r['id'] for r in g['records'] if r['change'] != 'same value']
        status, res = api.handle(Req(['review', 'bulk'], 'POST', body={'choice': 'accept', 'ids': adds}))
        self.assertEqual((status, res['ok'], len(res['done'])), (201, True, len(adds)))
        status, res = api.handle(Req(['review', 'bulk'], 'POST', body={'choice': 'ignore', 'ids': [fs['id']]}))
        self.assertEqual(status, 201)
        self.assertEqual(api.handle(Req(['review']))['counts']['proposed'], 0)
        self.assertEqual(api.handle(Req(['review', 'bulk'], 'POST', body={'choice': 'accept', 'ids': []}))[0], 400)
        kinds = [x['kind'] for x in api.handle(Req(['changes']))['changes']]
        self.assertIn('accepted', kinds)
        self.assertIn('ignored', kinds)


class Round4Unlocks(TempBrain):
    """Round 4 feature 1: the bottlenecks with what is on the list for each and the idea bank's unlocks; picking one."""

    def test_bottlenecks_unlocks_and_tags(self):
        u = api.handle(Req(['bottlenecks']))
        self.assertEqual(len(u['bottlenecks']), 3)
        self.assertEqual(u['bottlenecks'][0]['theme'], 'durability_vs_price')
        self.assertIn('trust_brand', u['bottlenecks'][0]['codes'])
        self.assertTrue(any('durability' in x['title'].lower() for x in u['bottlenecks'][0]['on_list']))
        self.assertTrue(u['bottlenecks'][0]['ideas'])
        self.assertLessEqual(len(u['bottlenecks'][0]['ideas']), 5)
        self.assertTrue(all(i['id'] and i['signal'] for b in u['bottlenecks'] for i in b['ideas']))
        self.assertIn('shopify', u['store_tags'])
        self.assertIn('paid_social_led', u['store_tags'])
        self.assertTrue(u['diagnosis']['test_queue'])
        self.assertTrue(u['diagnosis']['summary'])

    def test_pick_becomes_plan_finding_and_brief(self):
        u = api.handle(Req(['bottlenecks']))
        idea = u['bottlenecks'][0]['ideas'][0]['id']
        status, res = api.handle(Req(['bottlenecks', 'pick'], 'POST', body={'idea_id': idea, 'bottleneck': 'bottleneck_1', 'why': 'fits the durability story'}))
        self.assertEqual(status, 201)
        rec = next(r for r in self.section('plans') if r['id'] == res['record'])
        self.assertEqual((rec['value']['idea_id'], rec['value']['status'], rec['tier']), (idea, 'picked', 'approved'))
        u = api.handle(Req(['bottlenecks']))
        self.assertNotIn(idea, [i['id'] for i in u['bottlenecks'][0]['ideas']])
        self.assertEqual(u['bottlenecks'][0]['picked'][0]['idea_id'], idea)
        f = next(f for f in api.handle(Req(['audit']))['findings'] if f['rule_id'] == 'BRN-R22')
        self.assertEqual(f['capability']['id'], 'PROP-C06')
        a = next(a for a in api.rank('bombas', {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4})['actions'] if a['rule_id'] == 'BRN-R22')
        self.assertEqual((a['owner'], a['artefact']['kind']), ('agent_drafts', 'test_brief'))
        self.assertTrue(a['artefact']['draft'].startswith('Test brief for ' + idea))
        self.assertEqual(api.rank_mod.validate_action(a), [])
        self.assertEqual(api.handle(Req(['bottlenecks', 'pick'], 'POST', body={'idea_id': 'nope'}))[0], 400)
        self.assertEqual(api.handle(Req(['bottlenecks', 'pick'], 'POST', body={'idea_id': 'ZZZ-999'}))[0], 404)


class Round4LadderProof(TempBrain):
    """Round 4 feature 3: the ladder proof matrix, rungs by surface; the gap brief; attaching a record as proof; rule BRN-R23."""

    def test_matrix_shape_and_gaps(self):
        m = api.handle(Req(['ladders', 'proof']))
        self.assertEqual([c['key'] for c in m['cols']], ['copy', 'pdp', 'amazon_listing', 'cx_macro', 'offer'])
        self.assertEqual(m['counts']['rungs'], len(m['rows']))
        self.assertEqual(m['counts']['rungs'], m['counts']['proved'] + m['counts']['weak'] + m['counts']['missing'])
        cell = m['cells']['price_and_value.1']
        self.assertEqual((cell['copy']['us'], cell['copy']['status'], cell['copy']['tier']), (2, 'proved', 'site_backed'))
        self.assertNotIn('offer', cell)  # the rung is not used on the offer
        gap = next(g for g in m['gaps'] if g['key'] == 'durability.3')
        self.assertEqual((gap['status'], gap['proof_ids'], gap['one_star']), ('missing', [], 35))
        self.assertEqual(m['cells']['durability.3']['copy']['us'], 0)
        self.assertTrue(m['cells']['durability.3']['copy']['act'])
        self.assertIn('Proof brief: durability, rung 3', gap['brief'])
        self.assertIn('Never a review quote as a testimonial', gap['brief'])
        self.assertTrue(gap['candidates'] and all(c['tier'] != 'forbidden' for c in gap['candidates']))
        self.assertEqual(m['gaps'][0]['one_star'], max(g['one_star'] for g in m['gaps']))
        self.assertEqual(m['counts']['one_star_unproved'], sum(g['one_star'] for g in m['gaps']))

    def test_rule_and_action(self):
        m = api.handle(Req(['ladders', 'proof']))
        fs = [f for f in api.handle(Req(['audit']))['findings'] if f['rule_id'] == 'BRN-R23']
        self.assertEqual(len(fs), m['counts']['missing'])
        f = next(f for f in fs if f['entity']['id'] == 'rung_durability_3')
        self.assertEqual((f['severity'], f['capability']['id']), ('medium', 'BRN-C03'))
        self.assertIn('35 one-star lines', f['sentence'])
        self.assertIn('bombas.objection_ladders.durability', f['brain_refs'])
        acts = [a for a in api.rank('bombas', {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4})['actions'] if a['rule_id'] == 'BRN-R23']
        self.assertEqual(len(acts), len(fs))
        a = next(a for a in acts if a['entity']['id'] == 'rung_durability_3')
        self.assertTrue(a['title'].startswith('Brief the proof for durability rung 3'))
        self.assertEqual((a['owner'], a['artefact']['kind']), ('agent_drafts', 'brain_record'))
        self.assertTrue(a['artefact']['draft'].startswith('Proof brief: durability, rung 3'))
        self.assertEqual(api.rank_mod.validate_action(a), [])

    def test_attach_proof_is_a_founder_edit(self):
        status, res = api.handle(Req(['ladders', 'proof'], 'POST', body={'theme': 'durability', 'level': 3, 'record_id': 'bombas.products.heel_hole_durability'}))
        self.assertEqual((status, res['usable'], res['proof_tier']), (201, False, 'evidence'))
        m = api.handle(Req(['ladders', 'proof']))
        r = next(r for r in m['rungs'] if r['key'] == 'durability.3')
        self.assertEqual((r['status'], r['tier']), ('weak', 'evidence'))
        self.assertEqual(m['cells']['durability.3']['copy']['us'], 1)
        status, res = api.handle(Req(['ladders', 'proof'], 'POST', body={'theme': 'durability', 'level': '3', 'record_id': 'bombas.policies.happiness_guarantee'}))
        self.assertEqual((status, res['usable']), (201, True))
        m = api.handle(Req(['ladders', 'proof']))
        r = next(r for r in m['rungs'] if r['key'] == 'durability.3')
        self.assertEqual((r['status'], r['proof_ids']), ('proved', ['bombas.products.heel_hole_durability', 'bombas.policies.happiness_guarantee']))
        self.assertNotIn('rung_durability_3', [f['entity']['id'] for f in api.handle(Req(['audit']))['findings'] if f['rule_id'] == 'BRN-R23'])
        lad = next(x for x in self.section('objection_ladders') if x['id'] == 'bombas.objection_ladders.durability')
        self.assertEqual((lad['tier'], lad['source']['type'], lad['source']['was']['tier']), ('approved', 'founder', 'approved'))  # the second attach follows the first founder edit
        self.assertTrue(lad.get('history'))  # the value before each attach is kept
        self.assertEqual(lad['value']['rungs'][2]['proof_ids'][-1], 'bombas.policies.happiness_guarantee')
        self.assertTrue(any(c['kind'] == 'proof' for c in api.handle(Req(['changes']))['changes']))
        # the founder record survives a re-read and the other rungs are untouched
        self.assertEqual(lad['value']['rungs'][0]['proof_ids'], ['bombas.policies.happiness_guarantee'])
        self.assertEqual(api.handle(Req(['ladders', 'proof'], 'POST', body={'theme': 'nope', 'level': 1, 'record_id': 'bombas.policies.happiness_guarantee'}))[0], 404)
        self.assertEqual(api.handle(Req(['ladders', 'proof'], 'POST', body={'theme': 'durability', 'level': 9, 'record_id': 'bombas.policies.happiness_guarantee'}))[0], 404)
        self.assertEqual(api.handle(Req(['ladders', 'proof'], 'POST', body={'theme': 'durability', 'level': 3, 'record_id': 'bombas.x.y'}))[0], 404)
        self.assertEqual(api.handle(Req(['ladders', 'proof'], 'POST', body={'theme': 'durability', 'level': 'x', 'record_id': 'bombas.policies.happiness_guarantee'}))[0], 400)

    def test_forbidden_proof_is_refused_and_flagged(self):
        api.handle(Req(['approve', 'bombas.claims.guarantee_promise'], 'POST', body={'choice': 'forbid'}))
        status, res = api.handle(Req(['ladders', 'proof'], 'POST', body={'theme': 'durability', 'level': 3, 'record_id': 'bombas.claims.guarantee_promise'}))
        self.assertEqual(status, 400)
        m = api.handle(Req(['ladders', 'proof']))
        self.assertTrue(all(c['id'] != 'bombas.claims.guarantee_promise' for g in m['gaps'] for c in g['candidates']))

    def test_example_brand_reads_unavailable(self):
        shutil.copytree(BRAIN / 'example', self.tmp / 'example')
        m = api.handle(Req(['ladders', 'proof'], query={'brand': ['example']}))
        self.assertTrue(m['unavailable_reason'])
        self.assertEqual((m['rows'], m['counts']['rungs']), ([], 0))


class Round4SelfAudit(TempBrain):
    """Round 4 feature 4: the brain audits itself; regenerate the router; retire a duplicate; rules BRN-R24 and R25."""

    def test_self_audit_shape_and_router_rule(self):
        sa = api.handle(Req(['selfaudit']))
        self.assertEqual(sa['counts']['total'], len(sa['proposals']) + len(sa['duplicates']) + len(sa['missing_files']))
        self.assertTrue(all(p['fix']['who'] in ('agent', 'person') and p['fix']['text'] for p in sa['proposals']))
        self.assertFalse(sa['reads']['available'])  # no read logged in a fresh copy: unavailable, not zero
        self.assertIsNone(sa['counts']['unread_sections'])
        self.assertTrue(sa['router']['exists'])
        fs = {f['rule_id']: f for f in api.handle(Req(['audit']))['findings'] if f['rule_id'] in ('BRN-R24', 'BRN-R25')}
        broken = [p for p in sa['proposals'] if p['kind'] in ('drifted', 'broken_link')]
        self.assertEqual('BRN-R24' in fs, bool(broken))
        if broken:
            self.assertEqual(fs['BRN-R24']['capability']['id'], 'BRN-C12')
            a = next(a for a in api.rank('bombas', {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4})['actions'] if a['rule_id'] == 'BRN-R24')
            self.assertTrue(a['title'].startswith('Regenerate BRAIN.md'))
            self.assertEqual((a['owner'], a['artefact']['kind']), ('agent', 'brain_record'))
            self.assertEqual(api.rank_mod.validate_action(a), [])

    def test_regenerate_router_removes_drift(self):
        # a founder edit changes the records, so the router's rows and version line drift
        api.handle(Req(['profile', 'offers', 'free_shipping_threshold_usd'], 'POST', body={'text': '80'}))
        sa = api.handle(Req(['selfaudit']))
        self.assertTrue(any(p['kind'] == 'drifted' for p in sa['proposals']))
        status, res = api.handle(Req(['selfaudit', 'regenerate'], 'POST'))
        self.assertEqual((status, res['ok'], res['drift_after']), (201, True, 0))
        self.assertGreater(res['drift_before'], 0)
        self.assertLessEqual(res['tokens'], 1500)
        sa = api.handle(Req(['selfaudit']))
        self.assertFalse(any(p['kind'] == 'drifted' for p in sa['proposals']))
        self.assertIn('router', [c['kind'] for c in api.handle(Req(['changes']))['changes']])

    def test_duplicates_and_retire(self):
        rows = self.section('policies')
        twin = dict(next(r for r in rows if r['id'] == 'bombas.policies.happiness_guarantee'))
        twin['id'] = 'bombas.policies.happiness_guarantee_copy'
        twin['field'] = 'happiness_guarantee_copy'
        twin['tier'] = 'inferred'
        twin['source'] = {'type': 'inferred', 'ref': 'a second synthesis', 'captured_at': '2026-09-20'}
        twin.pop('history', None)
        self.write('policies', rows + [twin])
        sa = api.handle(Req(['selfaudit']))
        d = next(d for d in sa['duplicates'] if d['retire'] == twin['id'])
        self.assertEqual((d['keep'], d['section'], d['match']), ('bombas.policies.happiness_guarantee', 'policies', 'same text'))
        f = next(f for f in api.handle(Req(['audit']))['findings'] if f['rule_id'] == 'BRN-R25')
        self.assertIn('policies', f['sentence'])
        a = next(a for a in api.rank('bombas', {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4})['actions'] if a['rule_id'] == 'BRN-R25')
        self.assertTrue(a['title'].startswith('Retire 1 duplicate record'))
        self.assertIn(twin['id'], a['artefact']['draft'])
        self.assertEqual(api.rank_mod.validate_action(a), [])
        self.assertEqual(api.handle(Req(['selfaudit', 'retire'], 'POST', body={'retire': 'bombas.policies.happiness_guarantee', 'keep': twin['id']}))[0], 404)  # never the stronger one
        status, res = api.handle(Req(['selfaudit', 'retire'], 'POST', body={'retire': twin['id'], 'keep': d['keep']}))
        self.assertEqual((status, res['retired'], res['kept']), (201, twin['id'], d['keep']))
        self.assertEqual(next(r['status'] for r in self.section('policies') if r['id'] == twin['id']), 'retired')
        self.assertTrue(any(r['id'] == 'bombas.policies.happiness_guarantee' and r.get('status', 'active') == 'active' for r in self.section('policies')))
        self.assertFalse([x for x in api.handle(Req(['selfaudit']))['duplicates'] if x['retire'] == twin['id']])
        self.assertIn('retired', [c['kind'] for c in api.handle(Req(['changes']))['changes']])

    def test_read_coverage_from_the_log(self):
        api.handle(Req(['profile'], query={'reader': ['06-creative']}))
        api.handle(Req(['records', 'voice'], query={'reader': ['06-creative']}))
        sa = api.handle(Req(['selfaudit']))
        self.assertTrue(sa['reads']['available'])
        voice = next(r for r in sa['reads']['sections'] if r['section'] == 'voice')
        self.assertGreaterEqual(voice['reads'], 1)
        self.assertIn('06-creative', voice['readers'])
        self.assertTrue(voice['last_read'])
        self.assertIsInstance(sa['counts']['unread_sections'], int)
        self.assertTrue(all(r['records'] and not r['reads'] for r in sa['reads']['unread']))


class Round4Peaks(TempBrain):
    """Round 4 feature 5: peak readiness; the US peaks from the date, checks against the brain, a decision writes records; rule BRN-R26."""

    def test_calendar_and_checks(self):
        r = api.handle(Req(['peaks']))
        keys = [p['key'] for p in r['peaks']]
        self.assertEqual(keys[:2], ['prime_deal_days_2026', 'black_friday_2026'])  # 28 Sep 2026: deal days first (window), then Black Friday
        bf = next(p for p in r['peaks'] if p['key'] == 'black_friday_2026')
        self.assertEqual((bf['date'], bf['days_to'], bf['kind']), ('2026-11-27', 60, 'sale'))
        self.assertEqual(next(p['date'] for p in r['peaks'] if p['key'] == 'cyber_monday_2026'), '2026-11-30')
        self.assertEqual(next(p['date'] for p in r['peaks'] if p['key'] == 'giving_tuesday_2026'), '2026-12-01')
        ho = next(p for p in r['peaks'] if p['key'] == 'holiday_orderby_2026')
        self.assertTrue(ho['derived'])
        self.assertEqual(ho['date'], '2026-12-11')  # 25 December less 10 business days, the slowest standard promise
        self.assertEqual(next(c['status'] for c in ho['checks'] if c['key'] == 'cutoff'), 'gap')
        byk = {c['key']: c for c in bf['checks']}
        self.assertEqual((byk['offer']['status'], byk['returns_holiday']['status'], byk['email']['status']), ('gap', 'ok', 'unavailable'))
        self.assertIn('60 days', byk['returns_holiday']['evidence'])
        self.assertIn('COMFORT20', byk['offer']['fix'])
        self.assertEqual(bf['counts']['ok'] + bf['counts']['gaps'] + bf['counts']['unavailable'], len(bf['checks']))
        self.assertEqual(bf['readiness_pct'], round(100 * bf['counts']['ok'] / (bf['counts']['ok'] + bf['counts']['gaps'])))
        self.assertIsNone(next(p for p in r['peaks'] if p['key'] == 'prime_deal_days_2026')['date'])
        self.assertTrue(r['heavy_months']['available'])
        self.assertTrue([m for m in r['heavy_months']['months'] if m['month'] == '2026-11' and m['heavy']])

    def test_rule_and_action(self):
        fs = {f['entity']['id']: f for f in api.handle(Req(['audit']))['findings'] if f['rule_id'] == 'BRN-R26'}
        self.assertEqual(fs['peak_black_friday_2026']['severity'], 'medium')  # 60 days
        self.assertEqual(fs['peak_christmas_2026']['severity'], 'low')
        self.assertIn('Black Friday is in 60 days', fs['peak_black_friday_2026']['sentence'])
        acts = {a['entity']['id']: a for a in api.rank('bombas', {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4})['actions'] if a['rule_id'] == 'BRN-R26'}
        a = acts['peak_black_friday_2026']
        self.assertTrue(a['title'].startswith('Get ready for Black Friday (60 days)'))
        self.assertEqual(a['artefact']['kind'], 'offer')
        self.assertTrue(a['artefact']['draft'].startswith('Peak plan: Black Friday, 2026-11-27'))
        self.assertTrue(any(st['who'] == 'person' for st in a['steps']))
        for x in acts.values():
            self.assertEqual(api.rank_mod.validate_action(x), [])

    def test_decide_writes_records_and_clears_gaps(self):
        status, res = api.handle(Req(['peaks', 'plan'], 'POST', body={'peak': 'black_friday_2026', 'offer': '25 percent off sitewide, code BF25, no stacking', 'note': 'ends Monday', 'cutoff': '2026-12-12'}))
        self.assertEqual(status, 201)
        self.assertEqual(res['records'], ['bombas.offers.peak_black_friday_2026', 'bombas.calendar.peak_black_friday_2026', 'bombas.policies.holiday_shipping_cutoff'])
        r = api.handle(Req(['peaks']))
        bf = next(p for p in r['peaks'] if p['key'] == 'black_friday_2026')
        self.assertEqual(next(c['status'] for c in bf['checks'] if c['key'] == 'offer'), 'ok')
        ho = next(p for p in r['peaks'] if p['key'] == 'holiday_orderby_2026')
        self.assertEqual((ho['date'], ho['derived']), ('2026-12-12', False))
        self.assertEqual(next(c['status'] for c in ho['checks'] if c['key'] == 'cutoff'), 'ok')
        self.assertNotIn('peak_holiday_orderby_2026', [f['entity']['id'] for f in api.handle(Req(['audit']))['findings'] if f['rule_id'] == 'BRN-R26'])
        off = next(x for x in self.section('offers') if x['id'] == 'bombas.offers.peak_black_friday_2026')
        self.assertEqual((off['tier'], off['source']['type'], off['value']['offer']), ('approved', 'founder', '25 percent off sitewide, code BF25, no stacking'))
        cal = next(x for x in self.section('calendar') if x['id'] == 'bombas.calendar.peak_black_friday_2026')
        self.assertEqual(cal['value']['date'], '2026-11-27')
        self.assertIn('peak', [c['kind'] for c in api.handle(Req(['changes']))['changes']])
        # the peak records never join the calendar as a second event
        self.assertEqual(len([p for p in r['peaks'] if p['key'] == 'black_friday_2026']), 1)
        self.assertEqual(api.handle(Req(['peaks', 'plan'], 'POST', body={'peak': 'black_friday_2026'}))[0], 400)
        # a forbidden phrase in the offer is refused
        status, res = api.handle(Req(['claims'], 'POST', body={'text': 'lifetime guarantee', 'tier': 'forbidden'}))
        self.assertEqual(status, 201)
        self.assertEqual(api.handle(Req(['peaks', 'plan'], 'POST', body={'peak': 'cyber_monday_2026', 'offer': 'Cyber deal with a lifetime guarantee'}))[0], 400)

    def test_own_calendar_event_joins_the_window(self):
        rows = self.section('calendar')
        rows.append({'id': 'bombas.calendar.launch_slippers_2026', 'brand': 'bombas', 'section': 'calendar', 'field': 'launch_slippers_2026', 'value': {'date': '2026-11-05', 'event': 'Slipper launch'}, 'text': 'A new slipper line launches on 5 November 2026.', 'tier': 'approved', 'confidence': 1.0, 'visibility': 'private', 'source': {'type': 'founder', 'ref': 'test', 'captured_at': '2026-09-28'}})
        self.write('calendar', rows)
        r = api.handle(Req(['peaks']))
        ev = next(p for p in r['peaks'] if p['key'] == 'launch_slippers_2026')
        self.assertEqual((ev['label'], ev['days_to'], ev['kind'], ev['own']), ('Slipper launch', 38, 'event', True))
        self.assertEqual(next(c['status'] for c in ev['checks'] if c['key'] == 'offer'), 'gap')
        self.assertEqual(next(f['severity'] for f in api.handle(Req(['audit']))['findings'] if f['entity']['id'] == 'peak_launch_slippers_2026'), 'medium')


class Round4History(TempBrain):
    """Round 4 feature 6: one record's history, and restoring an earlier value as a founder edit that can itself be undone."""

    def test_timeline_merges_values_and_changes(self):
        h = api.handle(Req(['history'], query={'record': ['bombas.identity.giving_model']}))
        self.assertEqual(h['section'], 'identity')
        self.assertGreaterEqual(h['counts']['values'], 1)
        self.assertTrue(all(it['kind'] in ('value', 'change') for it in h['items']))
        self.assertEqual(h['current']['value_text'], h['current']['value_text'])
        api.handle(Req(['profile', 'offers', 'free_shipping_threshold_usd'], 'POST', body={'text': '80'}))
        h = api.handle(Req(['history'], query={'record': ['bombas.offers.free_shipping_threshold_usd']}))
        vals = [it for it in h['items'] if it['kind'] == 'value']
        self.assertEqual(vals[-1]['value'], 75)
        self.assertTrue(vals[-1]['restorable'])
        self.assertTrue([it for it in h['items'] if it['kind'] == 'change' and it['change_kind'] == 'founder_edit'])
        self.assertEqual(api.handle(Req(['history'], query={'record': ['bombas.offers.nope']}))[0], 404)
        self.assertEqual(api.handle(Req(['history'], query={'record': ['bad id']}))[0], 400)

    def test_restore_and_undo(self):
        api.handle(Req(['profile', 'offers', 'free_shipping_threshold_usd'], 'POST', body={'text': '80'}))
        h = api.handle(Req(['history'], query={'record': ['bombas.offers.free_shipping_threshold_usd']}))
        idx = next(it['index'] for it in h['items'] if it['kind'] == 'value' and it['value'] == 75)
        status, res = api.handle(Req(['history', 'restore'], 'POST', body={'record': 'bombas.offers.free_shipping_threshold_usd', 'index': idx}))
        self.assertEqual((status, res['before'], res['after']), (201, 80, 75))
        rec = next(r for r in self.section('offers') if r['id'] == 'bombas.offers.free_shipping_threshold_usd')
        self.assertEqual((rec['value'], rec['tier'], rec['source']['type'], rec['source']['restored_from']['index']), (75, 'approved', 'founder', idx))
        self.assertEqual(rec['history'][-1]['value'], 80)  # the replaced value joins the history
        self.assertEqual(next(f['text'] for s in api.handle(Req(['profile']))['sections'] for f in s['fields'] if f['key'] == 'free_shipping_threshold_usd').strip('$ '), '75')
        self.assertIn('restore', [c['kind'] for c in api.handle(Req(['changes']))['changes']])
        # undo the restore: the 80 is restorable again
        h = api.handle(Req(['history'], query={'record': ['bombas.offers.free_shipping_threshold_usd']}))
        idx80 = next(it['index'] for it in h['items'] if it['kind'] == 'value' and it['value'] == 80)
        self.assertEqual(api.handle(Req(['history', 'restore'], 'POST', body={'record': 'bombas.offers.free_shipping_threshold_usd', 'index': idx80}))[0], 201)
        self.assertEqual(next(r['value'] for r in self.section('offers') if r['id'] == 'bombas.offers.free_shipping_threshold_usd'), 80)
        self.assertEqual(api.handle(Req(['history', 'restore'], 'POST', body={'record': 'bombas.offers.free_shipping_threshold_usd', 'index': 99}))[0], 404)
        self.assertEqual(api.handle(Req(['history', 'restore'], 'POST', body={'record': 'bombas.offers.free_shipping_threshold_usd', 'index': 'x'}))[0], 400)
        h = api.handle(Req(['history'], query={'record': ['bombas.offers.free_shipping_threshold_usd']}))
        same = [it for it in h['items'] if it['kind'] == 'value' and it['same_as_current']]
        self.assertTrue(same)
        self.assertEqual(api.handle(Req(['history', 'restore'], 'POST', body={'record': 'bombas.offers.free_shipping_threshold_usd', 'index': same[0]['index']}))[0], 400)


def _png(w, h, color, filt=0):
    import struct
    import zlib
    raw = b''.join(bytes([filt]) + bytes(color) * w for _ in range(h))

    def chunk(t, d):
        return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    return b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)) + chunk(b'IDAT', zlib.compress(raw)) + chunk(b'IEND', b'')


class Round4Visual(TempBrain):
    """Round 4 feature 7: the palette, contrast pairs, the draft and PNG checks, logo rules; rule BRN-R27."""

    def test_palette_and_contrast(self):
        v = api.handle(Req(['visual']))
        self.assertTrue(v['available'])
        self.assertEqual(v['counts']['colours'], 12)
        blue = next(c for c in v['colours'] if c['key'] == 'color_blue_60')
        self.assertEqual((blue['hex'], blue['role'], blue['tier']), ('#223859', 'accent', 'site_backed'))
        pair = next(p for p in v['pairs'] if p['text'] == 'color_black' and p['background'] == 'color_white')
        self.assertEqual((pair['ratio'], pair['aa']), (20.63, True))
        self.assertEqual(v['counts']['aa_fail'], 0)
        self.assertIn('Conforto', [f['name'] for f in v['fonts']])
        self.assertFalse(v['logo_rules']['available'])

    def test_check_text_and_png(self):
        r = api.handle(Req(['visual', 'check'], 'POST', body={'text': '.h{color:#223859;background:#f8f8f4;font-family: Conforto, Arial} .x{color:#ff00aa} .y{color: rgb(9,135,80)}'}))
        self.assertEqual((r['kind'], r['verdict'], r['counts']), ('text', 'fail', {'colours': 4, 'off': 1, 'fonts': 2, 'off_fonts': 1}))
        self.assertEqual(r['off_palette'][0]['hex'], '#ff00aa')
        self.assertEqual(next(c['nearest'] for c in r['colours'] if c['hex'] == '#098750'), 'color_green_50')
        self.assertEqual([f['name'] for f in r['off_fonts']], ['Arial'])
        ok = api.handle(Req(['visual', 'check'], 'POST', body={'text': 'colours: #223859 #ffffff'}))
        self.assertEqual(ok['verdict'], 'pass')
        img = base64.b64encode(_png(40, 20, (0x22, 0x38, 0x59))).decode()
        r = api.handle(Req(['visual', 'check'], 'POST', body={'content_base64': img, 'name': 'a.png'}))
        self.assertEqual((r['kind'], r['verdict'], r['width'], r['height'], r['on_palette_share']), ('png', 'pass', 40, 20, 1.0))
        self.assertEqual(r['colours'][0]['nearest'], 'color_blue_60')
        r = api.handle(Req(['visual', 'check'], 'POST', body={'content_base64': base64.b64encode(_png(40, 20, (0xff, 0x00, 0xaa), filt=2)).decode()}))
        self.assertEqual((r['verdict'], r['colours'][0]['on_palette']), ('fail', False))
        self.assertEqual(api.handle(Req(['visual', 'check'], 'POST', body={'content_base64': base64.b64encode(b'\xff\xd8\xff\xe0').decode()}))[0], 400)
        self.assertEqual(api.handle(Req(['visual', 'check'], 'POST', body={}))[0], 400)
        shot = (SCREEN / 'round3.png').read_bytes()
        r = api.handle(Req(['visual', 'check'], 'POST', body={'content_base64': base64.b64encode(shot).decode()}))
        self.assertIn(r['verdict'], ('pass', 'warn', 'fail'))
        self.assertTrue(r['colours'])

    def test_logo_rules_and_rule(self):
        self.assertTrue([f for f in api.handle(Req(['audit']))['findings'] if f['rule_id'] == 'BRN-R27'])
        a = next(a for a in api.rank('bombas', {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4})['actions'] if a['rule_id'] == 'BRN-R27')
        self.assertTrue(a['title'].startswith('Complete the visual identity'))
        self.assertEqual(api.rank_mod.validate_action(a), [])
        status, res = api.handle(Req(['visual', 'logo'], 'POST', body={'min_size_px': '120', 'clear_space': 'the height of the mark', 'never': 'stretch it; recolour it', 'backgrounds': 'white, black'}))
        self.assertEqual((status, res['record']), (201, 'bombas.visual.logo_rules'))
        v = api.handle(Req(['visual']))
        self.assertEqual((v['logo_rules']['available'], v['logo_rules']['value']['min_size_px'], v['logo_rules']['value']['never']), (True, 120, ['stretch it', 'recolour it']))
        self.assertFalse([f for f in api.handle(Req(['audit']))['findings'] if f['rule_id'] == 'BRN-R27'])
        self.assertEqual(api.handle(Req(['visual', 'logo'], 'POST', body={}))[0], 400)
        self.assertIn('logo', [c['kind'] for c in api.handle(Req(['changes']))['changes']])

    def test_example_brand_unavailable(self):
        shutil.copytree(BRAIN / 'example', self.tmp / 'example')
        v = api.handle(Req(['visual'], query={'brand': ['example']}))
        self.assertFalse(v['available'])
        r = api.handle(Req(['visual', 'check'], 'POST', query={'brand': ['example']}, body={'text': '#123456'}))
        self.assertEqual(r['verdict'], 'unavailable')


class Round4Decisions(TempBrain):
    """Round 4 feature 8: snooze expiry, superseded rows, undo as an appended clearing row; the log is never rewritten."""

    def _log(self, rows):
        p = self.tmp / 'decisions.json'
        p.write_text(json.dumps(rows), encoding='utf-8')
        return str(p)

    def test_expiry_and_supersede(self):
        path = self._log([
            {'screen': '05-brand-brain', 'capability': 'CREA-C06', 'choice': 'not_now', 'reason': '', 'time': '2026-09-20T10:00:00Z', 'finding_id': '05-brand-brain.BRN-R08.angle_story'},
            {'screen': '05-brand-brain', 'capability': 'CREA-C06', 'choice': 'not_now', 'reason': '', 'time': '2026-09-01T10:00:00Z', 'finding_id': '05-brand-brain.BRN-R08.angle_offer'},
            {'screen': '05-brand-brain', 'capability': 'BRN-C05', 'choice': 'person', 'reason': 'ask ops', 'time': '2026-09-25T10:00:00Z', 'finding_id': '05-brand-brain.BRN-R12.x'},
            {'screen': '05-brand-brain', 'capability': 'BRN-C05', 'choice': 'agent', 'reason': '', 'time': '2026-09-26T10:00:00Z', 'finding_id': '05-brand-brain.BRN-R12.x'},
        ])
        d = api.handle(Req(['decisions'], query={'decisions': [path]}))
        acts = {(it['finding_id'], it['time']): it for it in d['items'] if it['kind'] == 'action'}
        story = acts[('05-brand-brain.BRN-R08.angle_story', '2026-09-20T10:00:00Z')]
        self.assertEqual((story['expires_on'], story['days_left'], story['expired'], story['current']), ('2026-10-04', 6, False, True))
        offer = acts[('05-brand-brain.BRN-R08.angle_offer', '2026-09-01T10:00:00Z')]
        self.assertEqual((offer['expires_on'], offer['expired']), ('2026-09-15', True))
        self.assertTrue(acts[('05-brand-brain.BRN-R12.x', '2026-09-25T10:00:00Z')]['superseded'])
        self.assertTrue(acts[('05-brand-brain.BRN-R12.x', '2026-09-26T10:00:00Z')]['current'])
        self.assertEqual(d['counts']['snoozed'], 1)
        self.assertEqual(d['counts']['expired'], 1)
        self.assertEqual(d['counts']['action'], 1)
        self.assertEqual(d['counts']['superseded'], 1)
        self.assertEqual(d['snooze_days'], api.rank_mod.SNOOZE_DAYS)

    def test_undo_appends_and_clears(self):
        path = self._log([{'screen': '05-brand-brain', 'capability': 'CREA-C06', 'choice': 'not_now', 'reason': '', 'time': '2026-09-27T10:00:00Z', 'finding_id': '05-brand-brain.BRN-R08.angle_story'}])
        status, res = api.handle(Req(['decisions', 'undo'], 'POST', query={'decisions': [path]}, body={'finding_id': '05-brand-brain.BRN-R08.angle_story'}))
        self.assertEqual((status, res['undid']['choice']), (201, 'not_now'))
        rows = json.loads(Path(path).read_text(encoding='utf-8'))
        self.assertEqual(len(rows), 2)  # appended, never rewritten
        self.assertEqual((rows[-1]['choice'], rows[-1]['finding_id']), ('undo', '05-brand-brain.BRN-R08.angle_story'))
        d = api.handle(Req(['decisions'], query={'decisions': [path]}))
        self.assertEqual((d['counts']['snoozed'], d['counts']['undone']), (0, 1))
        # rank's latest-row-wins reading: the action is not snoozed and not counted as decided
        acts = api.rank_mod.apply_decisions([{'id': '05-brand-brain.BRN-R08.angle_story', 'screen': '05-brand-brain', 'capability': {'id': 'CREA-C06'}}], today=dt.date(2026, 9, 28), path=Path(path))
        self.assertEqual(len(acts), 1)
        self.assertEqual(acts[0]['decision']['choice'], 'undo')
        self.assertEqual(api.handle(Req(['decisions', 'undo'], 'POST', query={'decisions': [path]}, body={'finding_id': '05-brand-brain.BRN-R08.angle_story'}))[0], 400)
        self.assertEqual(api.handle(Req(['decisions', 'undo'], 'POST', query={'decisions': [path]}, body={'finding_id': 'nope.x'}))[0], 404)
        self.assertEqual(api.handle(Req(['decisions', 'undo'], 'POST', query={'decisions': [path]}, body={}))[0], 400)
        self.assertIn('decision', [c['kind'] for c in api.handle(Req(['changes']))['changes']])

    def test_path_outside_the_temp_root_is_ignored(self):
        d = api.handle(Req(['decisions'], query={'decisions': ['/etc/passwd']}))
        self.assertIn('items', d)


class Round4SecondBrand(unittest.TestCase):
    """Round 4 feature 2: plug and play. Every route answers for the example brain (7 records), unavailable never zero."""

    ROUTES = [['overview'], ['master'], ['profile'], ['documents'], ['competitors'], ['coverage'], ['signals'], ['health'], ['conflicts'], ['questions'], ['ladders', 'proof'], ['selfaudit'], ['peaks'], ['visual'],
              ['decisions'], ['flows'], ['claims'], ['site', 'diff'], ['parity'], ['contracts'], ['legal'], ['voice'], ['battlecards'], ['permissions'],
              ['export'], ['assumptions'], ['facts'], ['summaries'], ['changes'], ['learn'], ['report'], ['digest'], ['review'], ['bottlenecks'], ['audit']]

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        shutil.copytree(BRAIN / 'example', self.tmp / 'example')
        api.BRAIN_ROOT = self.tmp

    def tearDown(self):
        api.BRAIN_ROOT = None
        shutil.rmtree(self.tmp)

    def req(self, path):
        r = Req(path)
        r.query['brand'] = ['example']
        return r

    def test_every_route_answers_for_a_second_brand(self):
        failed = []
        for path in self.ROUTES:
            try:
                res = api.handle(self.req(path))
            except Exception as exc:  # noqa: BLE001
                failed.append((path, type(exc).__name__ + ': ' + str(exc)[:80]))
                continue
            if isinstance(res, tuple):
                failed.append((path, res))
        self.assertEqual(failed, [])
        ov = api.handle(self.req(['overview']))
        self.assertIn('example is a brain folder', ov['simulated_note'])
        h = api.handle(self.req(['health']))
        self.assertEqual(h['cells']['claims'], {})     # no records: an empty cell, not 0
        self.assertIsNone(api.handle(self.req(['competitors']))['us'])
        self.assertEqual(api.handle(self.req(['parity']))['counts']['listings'], 0)
        self.assertIsNone(api.handle(self.req(['site', 'diff']))['counts']['changes'])
        cv = api.handle(self.req(['coverage']))
        self.assertEqual(cv['gaps'], [])
        r = api.rank('example', {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4})
        self.assertTrue(all(api.rank_mod.validate_action(a) == [] for a in r['actions']))
        # a founder edit works the same way for any brand folder
        status, res = api.handle(Req(['profile', 'positioning', 'frame'], 'POST', query={'brand': ['example']}, body={'text': 'Socks for people who walk all day.'}))
        self.assertEqual(status, 201)
        self.assertTrue((self.tmp / 'example' / 'positioning.json').is_file())

    def test_page_carries_the_brand_on_every_call(self):
        js = (SCREEN / 'screen.js').read_text(encoding='utf-8')
        self.assertIn("new URLSearchParams(location.search).get('brand')", js)
        self.assertIn('const api = (url, opts) => UI.api(withBrand(url), opts)', js)
