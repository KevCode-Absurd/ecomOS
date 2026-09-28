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
        self.assertLessEqual({'BRN-R01', 'BRN-R02', 'BRN-R03', 'BRN-R04', 'BRN-R05', 'BRN-R06', 'BRN-R07', 'BRN-R08', 'BRN-R09', 'BRN-R10'}, rules)


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
        self.assertEqual(res['records_changed_count'], 0)
        status, res2 = api.handle(Req(['documents'], method='POST', body={'url': 'https://example.com/deck'}))
        self.assertEqual(status, 201)
        self.assertEqual(res2['document']['tags'], ['url'])
        d = api.handle(Req(['documents']))
        self.assertEqual(d['count'], 2)
        self.assertEqual({x['added_by'] for x in d['documents']}, {'founder'})
        self.assertTrue((self.tmp / 'bombas' / 'documents' / res['document']['name']).is_file())
        manifest = json.loads((self.tmp / 'bombas' / 'documents' / 'manifest.json').read_text())
        self.assertEqual(len(manifest), 2)
        self.assertTrue(all(m['file'].startswith('documents/') and not m['extracted'] for m in manifest))
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
