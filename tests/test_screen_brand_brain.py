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
        # R03 fires once per open question; which questions are open moves with the brain.
        bank = audit.keeper.load_bank()
        heavy = [q for q in audit.Brain('bombas', None, dt.date.fromisoformat(DAY)).records('open_questions')
                 if not (q.get('value') or {}).get('answered_on') and audit.question_weight(q, bank) >= audit.HIGH_WEIGHT]
        fired = any(i.startswith('05-brand-brain.BRN-R03.question_') for i in ids)
        self.assertEqual(fired, bool(heavy), ids)
        self.assertIn('05-brand-brain.BRN-R02.section_economics', ids)
        self.assertIn('05-brand-brain.BRN-R04.mission_trust.rung_1.donation_pledge', ids)
        rules = {r['rule_id'] for r in audit.RULES}
        self.assertLessEqual({'BRN-R01', 'BRN-R02', 'BRN-R03', 'BRN-R04', 'BRN-R05', 'BRN-R06', 'BRN-R07', 'BRN-R08', 'BRN-R09', 'BRN-R10', 'BRN-R11', 'BRN-R12', 'BRN-R13', 'BRN-R14', 'BRN-R15', 'BRN-R16', 'BRN-R17', 'BRN-R18', 'BRN-R19'}, rules)


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
        self.assertEqual(d['counts'], {'action': 1, 'snoozed': 1, 'brain': 2})
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
