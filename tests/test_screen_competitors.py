"""Tests for screen 03-competitors on the Bombas brain: audit.py in the contract shape and the api
(overview tiles, insights, chart, map, price ladder, board, lookalike). Edits go to a temp copy of app/brain."""
import datetime as dt
import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / 'app' / 'screens' / '03-competitors'
BRAIN = ROOT / 'app' / 'brain'
DAY = '2026-09-28'
WINDOW = {'ends_on': '2026-09-27', 'days': 1, 'trailing': 0}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


audit = load('competitors_audit_t', SCREEN / 'audit.py')
api = load('competitors_api_t', SCREEN / 'api.py')

FIELDS = ['id', 'screen', 'rule_id', 'severity', 'entity', 'evidence', 'sentence', 'capability', 'money_at_stake',
          'confidence', 'brain_refs', 'first_seen', 'last_seen', 'status', 'unavailable']
EVIDENCE = {'metric', 'value', 'unit', 'window', 'ends_on', 'freshness_days', 'baseline', 'baseline_kind', 'source', 'simulated'}
ENTITY_TYPES = {'brand', 'stage', 'page', 'device', 'sku', 'campaign', 'adset', 'ad', 'flow', 'offer', 'ladder_rung', 'metric'}


class Req:
    def __init__(self, path, method='GET', query=None):
        self.method, self.path, self.body = method, path, None
        self.query = dict({'today': [DAY]}, **(query or {}))

    def arg(self, name, default=None):
        v = self.query.get(name)
        return v[0] if v else default


class TempBrain(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        shutil.copytree(BRAIN / 'bombas', self.tmp / 'bombas')

    def tearDown(self):
        api.BRAIN_ROOT = None
        shutil.rmtree(self.tmp)

    def edit(self, name, fn):
        path = self.tmp / 'bombas' / f'{name}.json'
        rows = json.loads(path.read_text(encoding='utf-8'))
        path.write_text(json.dumps(fn(rows)), encoding='utf-8')


class TestParse(unittest.TestCase):
    def test_bands(self):
        b = audit.parse_band('12 to 25 per pair, median about 18')
        self.assertEqual((b['low'], b['high'], b['median'], b['rough']), (12.0, 25.0, 18.0, False))
        b = audit.parse_band('10 to 59 per product, median about 19 per pair (pack parsing rough)')
        self.assertEqual((b['low'], b['high'], b['median'], b['rough']), (None, None, 19.0, True))
        b = audit.parse_band('from 18 per pair, median 25')
        self.assertEqual((b['low'], b['high'], b['median']), (18.0, None, 25.0))
        self.assertIsNone(audit.parse_band(None)['median'])

    def test_scores(self):
        self.assertEqual(audit.durability_score(['lifetime guarantee', 'durability first']), 3)
        self.assertEqual(audit.durability_score(['style']), 0)
        self.assertEqual(audit.comfort_score(['comfort', 'problem to relief', 'lab tested claim']), 3)

    def test_last_full_month(self):
        self.assertEqual(audit.last_full_month('2026-09-27'), '2026-08')
        self.assertEqual(audit.last_full_month('2026-09-30'), '2026-09')


class TestAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.findings = audit.run('bombas', WINDOW)

    def test_contract_shape(self):
        self.assertTrue(self.findings)
        for f in self.findings:
            for k in FIELDS:
                self.assertIn(k, f)
            self.assertEqual(f['screen'], '03-competitors')
            self.assertTrue(f['id'].startswith('03-competitors.' + f['rule_id'] + '.'))
            self.assertIn(f['severity'], audit.SEVERITY_ORDER)
            self.assertIn(f['entity']['type'], ENTITY_TYPES)
            self.assertIn(f['capability']['autonomy'], {'agent_does', 'founder_gate', 'human_assist'})
            self.assertIsNone(f['money_at_stake'])
            self.assertTrue(f['money_reason'])
            self.assertTrue(0.1 <= f['confidence'] <= 1)
            self.assertLessEqual(len(f['sentence'].split()), 40)
            self.assertNotIn('—', f['sentence'])
            for row in f['evidence']:
                self.assertEqual(set(row), EVIDENCE)
        rule_ids = {r['rule_id'] for r in audit.RULES}
        self.assertTrue({f['rule_id'] for f in self.findings} <= rule_ids)

    def test_unclaimed_angle(self):
        ids = {f['id'] for f in self.findings if f['rule_id'] == 'COMP-R01'}
        self.assertIn('03-competitors.COMP-R01.angle_giving', ids)
        self.assertNotIn('03-competitors.COMP-R01.angle_comfort_relief', ids)
        giving = next(f for f in self.findings if f['id'] == '03-competitors.COMP-R01.angle_giving')
        self.assertIn('bombas.identity.giving_model', giving['brain_refs'])
        self.assertEqual(giving['capability']['id'], 'BRAND-C21')

    def test_price_gap(self):
        f = next(f for f in self.findings if f['rule_id'] == 'COMP-R02')
        self.assertEqual(f['status'], 'open')
        brand = next(r for r in f['evidence'] if r['metric'] == 'brand_price_per_pair')
        comp = next(r for r in f['evidence'] if r['metric'] == 'competitor_median_price_per_pair')
        idx = next(r for r in f['evidence'] if r['metric'] == 'price_position_index')
        self.assertTrue(brand['simulated'])
        self.assertFalse(comp['simulated'])
        self.assertEqual(comp['baseline_kind'], 'peer_band')
        self.assertAlmostEqual(idx['value'], round(brand['value'] / comp['value'] * 100, 1))
        self.assertLess(idx['value'], audit.PRICE_BAND[0])
        self.assertIn('below', f['sentence'])

    def test_offer_run_and_lookalike(self):
        r3 = [f for f in self.findings if f['rule_id'] == 'COMP-R03']
        self.assertEqual([f['entity']['id'] for f in r3], ['guarantee'])
        self.assertIn('Smartwool', r3[0]['sentence'])
        r4 = [f for f in self.findings if f['rule_id'] == 'COMP-R04']
        self.assertEqual(len(r4), 1)
        self.assertEqual(r4[0]['capability']['id'], 'MONEY-C48')

    def test_deterministic(self):
        self.assertEqual(json.dumps(audit.run('bombas', WINDOW)), json.dumps(self.findings))

    def test_sorted(self):
        keys = [audit.SEVERITY_ORDER[f['severity']] for f in self.findings]
        self.assertEqual(keys, sorted(keys))


class TestAuditEdits(TempBrain):
    def test_no_competitors_is_unavailable(self):
        self.edit('competitors', lambda rows: [r for r in rows if r['field'] in ('competitor_set',)])
        shutil.rmtree(self.tmp / 'bombas' / 'raw')
        out = audit.run('bombas', WINDOW, self.tmp)
        un = [f for f in out if f['status'] == 'unavailable']
        self.assertEqual({f['rule_id'] for f in un}, {'COMP-R01', 'COMP-R02', 'COMP-R03'})
        for f in un:
            self.assertEqual(f['evidence'], [])
            self.assertTrue(f['unavailable']['inputs'])
        self.assertFalse([f for f in out if f['rule_id'] == 'COMP-R04'])

    def test_raw_fallback(self):
        self.edit('competitors', lambda rows: [r for r in rows if r['field'] != 'stance'])
        names = [c['name'] for c in audit.market('bombas', dt.date(2026, 9, 28), self.tmp)['competitors']]
        self.assertIn('Stance', names)

    def test_claimed_angle_resolves(self):
        def add_giving(rows):
            for r in rows:
                if r['field'] == 'stance':
                    r['value']['hook_types'].append('giving back')
            return rows
        self.edit('competitors', add_giving)
        out = audit.run('bombas', WINDOW, self.tmp)
        self.assertNotIn('03-competitors.COMP-R01.angle_giving', {f['id'] for f in out})


class TestApi(TempBrain):
    def setUp(self):
        super().setUp()
        api.BRAIN_ROOT = self.tmp
        self.d = api.handle(Req(['overview']))

    def test_overview_has_no_tiles_or_chart(self):
        for k in ('tiles', 'insights', 'chart', 'actions'):
            self.assertNotIn(k, self.d)

    def test_plan_route(self):
        p = api.handle(Req(['plan']))
        self.assertEqual(p['window']['ends_on'], '2026-09-27')
        self.assertTrue(p['actions'])
        labels = [o['label'] for o in p['orient']]
        self.assertTrue(3 <= len(labels) <= 6)
        self.assertIn('price index', labels)
        idx = next(o for o in p['orient'] if o['label'] == 'price index')
        self.assertEqual(idx['value'], self.d['price_position_index'])
        self.assertEqual(p['rules'], audit.RULES)

    def test_notes_say_simulated_and_public(self):
        self.assertIn('simulated', self.d['simulated_note'])
        self.assertIn('public signals', self.d['simulated_note'])
        self.assertIn('Never copy', self.d['signal_note'])
        self.assertNotIn('GPT', json.dumps(self.d))

    def test_cards_and_board(self):
        for c in self.d['competitors']:
            self.assertFalse([k for k in c if k.startswith('_')])
            self.assertIn('giving', c['gap_to_own'])
        self.assertTrue(self.d['board'][-1]['brand'])
        self.assertEqual(self.d['lookalike']['links_to'], 'sockscool.com')
        self.assertNotIn('lookalike_page', [c['id'].split('.')[-1] for c in self.d['competitors']])

    def test_map_and_prices(self):
        pos = self.d['positioning']
        self.assertEqual(pos['split_x'], 25.0)
        brand = next(p for p in pos['points'] if p['brand'])
        self.assertTrue(brand['simulated'])
        for axis in ('durability', 'comfort'):
            placed = sum(len(q['competitors']) for q in pos['quadrants'][axis]['quadrants'])
            self.assertEqual(placed, 5)
        pr = self.d['prices']
        self.assertTrue(pr['available'])
        self.assertEqual(pr['month'], '2026-08')
        row = pr['rows'][0]
        self.assertEqual(set(row['cells']), {c['name'] for c in pr['competitors']})
        stance = row['cells']['Stance']
        self.assertAlmostEqual(stance['diff'], round(row['per_pair'] - 18.0, 2))

    def test_audit_route_and_errors(self):
        a = api.handle(Req(['audit']))
        self.assertTrue(a['findings'] and a['rules'])
        self.assertEqual(api.handle(Req(['nope']))[0], 404)
        self.assertEqual(api.handle(Req(['overview'], query={'brand': ['../x']}))[0], 400)
        self.assertEqual(api.handle(Req(['overview'], query={'brand': ['nobrand']}))[0], 404)


class TestPages(TempBrain):
    """1.2: the tracked pages side by side, with a verdict and its reason in numbers."""
    def setUp(self):
        super().setUp()
        api.BRAIN_ROOT = self.tmp
        self.p = api.handle(Req(['overview']))['pages']

    def test_twelve_pages_and_us(self):
        rows = self.p['rows']
        comps = [r for r in rows if r['role'] != 'self']
        self.assertEqual(len(comps), 12)
        self.assertEqual(sum(r['frame'] == 'direct' for r in comps), 5)
        self.assertEqual(rows[-1]['role'], 'self')
        self.assertEqual(rows[-1]['active_ads'], 23)
        self.assertAlmostEqual(rows[-1]['offer_share'], round(21 / 23, 3))
        pills = {p['key']: p['n'] for p in self.p['pills']}
        self.assertEqual(pills['all'], 12)
        self.assertEqual(pills['threat'], sum(r['verdict']['text'] == 'Threat' for r in comps))

    def test_unavailable_not_zero(self):
        allbirds = next(r for r in self.p['rows'] if r['name'] == 'Allbirds')
        self.assertIsNone(allbirds['active_ads'])
        self.assertEqual(allbirds['verdict']['kind'], 'na')
        for r in self.p['rows']:
            if r['source'] != 'snapshot':
                self.assertIsNone(r['main_cta'])
                self.assertIsNone(r['new_14d'])

    def test_verdict_points_add_up(self):
        for r in self.p['rows']:
            if r['role'] == 'self' or r['verdict']['kind'] == 'na':
                continue
            v = r['verdict']
            pts = sum(int(w.rsplit('(+', 1)[1].rstrip(')')) for w in v['why'])
            self.assertEqual(pts, v['points'])
            want = 'Threat' if pts >= 4 else 'Watch' if pts >= 2 else 'Ignore'
            self.assertEqual(v['text'], want)

    def test_angle_tags_keep_the_word(self):
        feet = next(r for r in self.p['rows'] if r['name'] == 'Feetures')
        relief = next(a for a in feet['angles'] if a['tag'] == 'relief')
        self.assertEqual((relief['word'], relief['where']), ('relief', 'hook label'))
        us = self.p['rows'][-1]
        self.assertEqual(self.p['our_top_angles'], ['comfort', 'relief'])
        self.assertTrue(all('n' in a for a in us['angles']))

    def test_battlecard_is_signal_only(self):
        for r in self.p['rows']:
            if r['role'] == 'self':
                continue
            self.assertIn('brain verifies', r['battlecard'])
            self.assertNotIn('quotes', r)


class TestCoverage(TempBrain):
    """1.3: angles by format, our share against theirs; gaps carry a brief; COMP-R05 on the biggest gaps with proof."""
    def setUp(self):
        super().setUp()
        api.BRAIN_ROOT = self.tmp
        self.c = api.handle(Req(['overview']))['coverage']

    def test_shape_and_estimate_flag(self):
        c = self.c['all']
        self.assertEqual([x['key'] for x in c['cols']], audit.covmod.FORMATS)
        self.assertEqual(len(c['rows']), len(audit.snap.ANGLES))
        self.assertTrue(c['estimated'])
        self.assertEqual(c['our_ads'], 23)
        self.assertLessEqual(len(self.c['direct']['pages']), len(c['pages']))
        for row in c['cells'].values():
            for cell in row.values():
                for side in ('us', 'them'):
                    if cell[side] is not None:
                        self.assertTrue(0 <= cell[side] <= 1)

    def test_their_shares_sum_to_tagged_ads(self):
        c = self.c['all']
        total = sum(cell['them'] for row in c['cells'].values() for cell in row.values())
        self.assertLessEqual(total, 1.02)
        self.assertGreater(total, 0.3)

    def test_gap_rule_and_brief(self):
        c = self.c['all']
        for g in c['gaps']:
            cell = c['cells'][g['angle']][g['format']]
            self.assertEqual(cell['kind'], 'gap')
            self.assertGreaterEqual(cell['them'], audit.covmod.GAP_MIN)
            self.assertFalse(cell['us'])
            self.assertIn('Never copy', cell['brief'])
            if not cell['proof']:
                self.assertIn('none in the brain', cell['brief'])

    def test_rule_r05_top_gaps_with_proof(self):
        out = audit.run('bombas', WINDOW, self.tmp)
        r5 = [f for f in out if f['rule_id'] == 'COMP-R05']
        self.assertTrue(1 <= len(r5) <= audit.covmod.RULE_TOP)
        for f in r5:
            self.assertEqual(f['confidence'], 0.3)
            self.assertEqual(f['capability']['id'], 'CREA-C06')
        acts = api.rank('bombas', {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4})['actions']
        for f in r5:
            a = next(a for a in acts if f['id'] in a['finding_ids'])
            self.assertEqual(a['artefact']['kind'], 'ad_brief')
            self.assertTrue(a['artefact']['draft'])


class TestMix(TempBrain):
    """1.4: first line kinds and offer types against ours; each gap has an answer with an owner."""
    def setUp(self):
        super().setUp()
        api.BRAIN_ROOT = self.tmp
        self.mx = api.handle(Req(['overview']))['mix']

    def test_shares_sum_to_one(self):
        for r in self.mx['rows']:
            if r['n']:
                self.assertAlmostEqual(sum(v for v in r['shares'].values() if v), 1, delta=0.01)
        self.assertEqual(self.mx['rows'][-1]['role'], 'self')

    def test_gaps(self):
        by = {(g['kind'], g['key']): g for g in self.mx['gaps']}
        q = by[('first_line', 'question')]
        self.assertGreaterEqual(len(q['pages']), audit.mixmod.FL_PAGES)
        self.assertEqual(q['owner'], 'agent')
        fs = by[('offer', 'free_shipping')]
        self.assertIn('75', fs['held']['text'])
        d = by[('discount', 'discount_heavy')]
        self.assertAlmostEqual(d['ours'], round(21 / 23, 3))
        for g in self.mx['gaps']:
            self.assertIn(g['answer'], ('copy', 'offer'))
            self.assertTrue(g['draft'])

    def test_rules_r06_to_r08_rank(self):
        out = audit.run('bombas', WINDOW, self.tmp)
        ids = {f['rule_id'] for f in out}
        self.assertTrue({'COMP-R06', 'COMP-R07', 'COMP-R08'} <= ids)
        acts = api.rank('bombas', {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4})['actions']
        kinds = {a['rule_id']: a['artefact']['kind'] for a in acts}
        self.assertEqual(kinds['COMP-R06'], 'copy')
        self.assertEqual(kinds['COMP-R07'], 'test_brief')
        self.assertEqual(kinds['COMP-R08'], 'test_brief')
        r6 = next(a for a in acts if a['rule_id'] == 'COMP-R06')
        self.assertEqual(r6['title'], 'Write 6 question first lines and test the best 2')


class TestRank(TempBrain):
    """Depth contract rules 2, 3 and 13: owner, steps and artefact on every action; every finding ends in one."""
    W = {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4}

    def setUp(self):
        super().setUp()
        api.BRAIN_ROOT = self.tmp
        self.out = api.rank('bombas', self.W)

    def test_every_action_valid(self):
        acts = self.out['actions']
        self.assertTrue(acts)
        for a in acts:
            self.assertEqual(api.actions.ranker.validate_action(a), [], a['id'])
            self.assertIn(a['owner'], ('agent', 'agent_drafts', 'person'))
            self.assertIn(a['artefact']['kind'], api.actions.ranker.ARTEFACT_KINDS)
            for s in a['steps']:
                self.assertIn(s['who'], ('agent', 'person'))
            self.assertTrue(a['check_on'])
            self.assertNotIn('\u2014', json.dumps(a))
            self.assertNotIn('should', a['title'].lower())

    def test_every_finding_maps_to_an_action(self):
        findings = audit.run('bombas', self.W, self.tmp)
        covered = {i for a in self.out['actions'] for i in a['finding_ids']}
        for f in findings:
            if f['status'] in ('open', 'unavailable'):
                self.assertIn(f['id'], covered)

    def test_unavailable_maps_to_connect(self):
        self.edit('competitors', lambda rows: [r for r in rows if r['field'] in ('competitor_set',)])
        shutil.rmtree(self.tmp / 'bombas' / 'raw')
        out = api.rank('bombas', self.W)
        con = [a for a in out['actions'] if a['status'] == 'unavailable']
        self.assertTrue(con)
        for a in con:
            self.assertEqual(a['owner'], 'person')
            self.assertEqual(a['artefact']['kind'], 'connector_setup')

    def test_drafts_never_copy(self):
        for a in self.out['actions']:
            if a['artefact']['kind'] == 'ad_brief':
                self.assertIn('Never copy', a['artefact']['draft'])

    def test_deterministic(self):
        self.assertEqual(json.dumps(api.rank('bombas', self.W)['actions']), json.dumps(self.out['actions']))

    def test_app_rank_uses_override(self):
        r = api.actions.ranker.rank('03-competitors', 'bombas', self.W)
        self.assertEqual(r['source'], 'screen')


class TestPage(unittest.TestCase):
    """Depth rules 1 and 11: the plan comes first; no brand fact is written in the page."""
    def test_plan_first(self):
        html = (SCREEN / 'index.html').read_text(encoding='utf-8')
        body = html.split('screen-head', 1)[1]
        self.assertLess(body.index('id="plan"'), body.index('id="wrong"'))
        for gone in ('id="tiles"', 'id="insights"', 'id="chart"', 'id="lookalike"'):
            self.assertNotIn(gone, html)

    def test_no_brand_facts_in_js(self):
        js = (SCREEN / 'screen.js').read_text(encoding='utf-8')
        for word in ('Bombas', 'Stance', 'Darn Tough', 'Smartwool', 'Feetures', 'Comrad', 'COMFORT20'):
            self.assertNotIn(word, js)
        self.assertNotIn('GPT', js)


if __name__ == '__main__':
    unittest.main()
