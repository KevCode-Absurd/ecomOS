"""Tests for screen 03-competitors on the Bombas brain: audit.py in the contract shape and the api
(plan, rank, pages, coverage, mix, references, ladder, map, changes, freshness). Edits go to a temp copy of app/brain."""
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
        self.assertEqual(next(o for o in p['orient'] if o['label'] == 'pages tracked')['value'], 12)
        self.assertEqual({g['key'] for g in p['groups']}, set(audit.RULE_GROUP.values()))
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
        self.assertNotIn('board', self.d)
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
        self.assertNotIn('prices', self.d)

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


class TestReferences(TempBrain):
    """1.5: longest running ads as signals; relevance from rules; a brief that says what to borrow and never copy."""
    def setUp(self):
        super().setUp()
        api.BRAIN_ROOT = self.tmp
        self.r = api.handle(Req(['overview']))['references']

    def test_refs(self):
        refs = self.r['refs']
        self.assertEqual(len(refs), 11)
        scores = [x['score'] for x in refs]
        self.assertEqual(scores, sorted(scores, reverse=True))
        for x in refs:
            self.assertEqual(x['rights'], 'reference_only')
            self.assertLessEqual(x['score'], 1.0)
            self.assertIn('Never copy', x['brief'])
            self.assertIn('never passed', x['brief'])
            if x['days'] < audit.refmod.WATCH_DAYS:
                self.assertFalse(x['suggested'])
                self.assertEqual(x['verdict']['text'], 'Too new')
            self.assertIsNone(x['versions'])

    def test_score_is_sum_of_reasons(self):
        w = audit.refmod.WEIGHTS
        comrad = next(x for x in self.r['refs'] if x['page'] == 'Comrad Socks')
        self.assertEqual(comrad['score'], 1.0)
        self.assertEqual(len(comrad['reasons']), 4)
        quince = next(x for x in self.r['refs'] if x['page'] == 'Quince')
        self.assertEqual(quince['score'], w['long'])

    def test_ours(self):
        self.assertEqual(self.r['ours'][0]['days'], 193)
        self.assertEqual(self.r['ours'][0]['rights'], 'own_brand')


class TestLadder(TempBrain):
    """1.6: price and pack ladder against the bands; shallow ladder and above-with-no-proof rules."""
    def setUp(self):
        super().setUp()
        api.BRAIN_ROOT = self.tmp
        self.l = api.handle(Req(['overview']))['ladder']

    def test_ladders(self):
        l = self.l
        self.assertTrue(l['available'])
        self.assertEqual(l['month'], '2026-08')
        self.assertEqual(l['direct_median'], 25.0)
        ank = next(x for x in l['ladders'] if x['style'] == "men's ankle")
        self.assertEqual(ank['single'], 13.11)
        self.assertEqual(ank['biggest_pairs'], 4)
        self.assertAlmostEqual(ank['saving'], round(1 - ank['biggest'] / ank['single'], 3))
        for x in l['ladders']:
            self.assertEqual([s['pairs'] for s in x['steps']], sorted(s['pairs'] for s in x['steps']))
        self.assertEqual(l['bundle']['page'], 'Feetures')
        self.assertTrue(l['shallow'])
        self.assertEqual(audit.laddermod.pairs_in_title("Men's Originals Ankle Socks White Large (4 Pair)"), 4)
        self.assertEqual(audit.laddermod.pairs_in_title('Socks, 6-Pack Cushioned'), 6)
        self.assertIsNone(audit.laddermod.pairs_in_title('Womens Cushioned No Show Socks'))

    def test_rules(self):
        out = audit.run('bombas', WINDOW, self.tmp)
        r9 = [f for f in out if f['rule_id'] == 'COMP-R09']
        self.assertEqual(len(r9), 1)
        self.assertTrue(r9[0]['evidence'][0]['simulated'])
        self.assertFalse([f for f in out if f['rule_id'] == 'COMP-R10'])

    def test_above_no_proof_fires(self):
        def lift(rows):
            for r in rows:
                if r['field'] == 'proof_points':
                    r['value'] = ['B Corp certified']
            return rows
        self.edit('positioning', lift)
        m = audit.market_full('bombas', dt.date(2026, 9, 28), self.tmp)
        lad = m['ladder']
        lad['direct_median'] = 20.0
        for x in lad['ladders']:
            if x['single'] and x['single'] > 20:
                x['vs_direct_median'] = 'above'
        lad['above_no_proof'] = [x for x in lad['ladders'] if x['vs_direct_median'] == 'above' and not x['proof']]
        out = audit.rule_ladder(m, '2026-09-27')
        r10 = [f for f in out if f['rule_id'] == 'COMP-R10']
        self.assertTrue(r10)
        a = api.actions.action(r10[0], m, None)
        self.assertEqual(a['artefact']['kind'], 'page_section')
        self.assertEqual(api.actions.ranker.validate_action(a), [])


class TestMap(TempBrain):
    """1.7: positioning map on the kit chart, sized by active ads, each corner ends in a move."""
    def setUp(self):
        super().setUp()
        api.BRAIN_ROOT = self.tmp
        self.pos = api.handle(Req(['overview']))['positioning']

    def test_kit_props(self):
        for axis, k in self.pos['kit'].items():
            self.assertEqual(len(k['quadrants']), 4)
            self.assertEqual(len(k['moves']), 4)
            us = [p for p in k['points'] if p['us']]
            self.assertEqual(len(us), 1)
            self.assertEqual(us[0]['size'], 23)
            self.assertEqual(k['midX'], 25.0)
            kinds = [mv['kind'] for mv in k['moves']]
            self.assertEqual(kinds.count('hold'), 1)
        self.assertIn('Allbirds', self.pos['not_placed'])
        dur = self.pos['kit']['durability']
        contest = next(mv for mv in dur['moves'] if mv['kind'] == 'contest')
        self.assertIn('Feetures', contest['text'])
        self.assertIn('lifetime', contest['text'])

    def test_open_corner_rule(self):
        out = audit.run('bombas', WINDOW, self.tmp)
        self.assertFalse([f for f in out if f['rule_id'] == 'COMP-R11'])
        def drop(rows):
            return [r for r in rows if r['field'] not in ('feetures', 'darn_tough')]
        self.edit('competitors', drop)
        shutil.rmtree(self.tmp / 'bombas' / 'raw' / 'b-adlibrary')
        out = audit.run('bombas', WINDOW, self.tmp)
        r11 = [f for f in out if f['rule_id'] == 'COMP-R11']
        self.assertTrue(r11)
        acts = api.rank('bombas', {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4})['actions']
        a = next(a for a in acts if a['rule_id'] == 'COMP-R11')
        self.assertEqual(a['artefact']['kind'], 'test_brief')


class TestChanges(TempBrain):
    """1.8: launches and changes, newest first, each with follow, watch or ignore; snapshot diffs when two exist."""
    def setUp(self):
        super().setUp()
        api.BRAIN_ROOT = self.tmp
        self.ch = api.handle(Req(['overview']))['changes']

    def test_events(self):
        ev = self.ch['events']
        whens = [e['when'] for e in ev]
        self.assertEqual(whens, sorted(whens, reverse=True))
        stance = next(e for e in ev if e['page'] == 'Stance')
        self.assertEqual((stance['kind'], stance['verdict']), ('refresh', 'watch'))
        tj = next(e for e in ev if e['page'] == 'Tommy John')
        self.assertEqual(tj['verdict'], 'ignore')
        lk = next(e for e in ev if e['kind'] == 'lookalike')
        self.assertEqual(lk['verdict'], 'follow')
        self.assertTrue(all(e['when'] >= self.ch['window_start'] for e in ev))
        self.assertEqual(self.ch['snapshots'], 0)

    def test_snapshot_diff(self):
        def ad(pid, aid, fmt, offers=(), angles=()):
            return {'page_id': pid, 'ad_id': aid, 'format': fmt, 'offers': [{'tag': o} for o in offers],
                    'angles': [{'tag': a} for a in angles], 'role': 'competitor'}
        prev = {'captured_at': '2026-09-14', 'pages': {'1': {'name': 'Stance', 'role': 'competitor'}},
                'ads': [ad('1', 'a', 'video')]}
        cur = {'captured_at': '2026-09-28', 'pages': {'1': {'name': 'Stance', 'role': 'competitor'}},
               'ads': [ad('1', 'a', 'video'), ad('1', 'b', 'carousel', ['percent_off'], ['comfort'])]}
        kinds = {e['kind'] for e in audit.changemod.diff(prev, cur)}
        self.assertEqual(kinds, {'new_ads', 'new_format', 'new_offer', 'new_angle'})
        self.assertEqual(audit.changemod.diff(None, cur), [])

    def test_rule_r12(self):
        out = audit.run('bombas', WINDOW, self.tmp)
        r12 = [f for f in out if f['rule_id'] == 'COMP-R12']
        self.assertEqual([f['entity']['id'] for f in r12], ['refresh_stance'])


class TestFreshness(TempBrain):
    """1.9: freshness per page, the re-pull plan with its estimate first, page ids only; unavailable never zero."""
    def setUp(self):
        super().setUp()
        api.BRAIN_ROOT = self.tmp
        self.fr = api.handle(Req(['overview']))['freshness']

    def test_rows(self):
        allbirds = next(r for r in self.fr['rows'] if r['name'] == 'Allbirds')
        self.assertEqual(allbirds['kind'], 'na')
        self.assertIsNone(allbirds['age_days'])
        self.assertIsNone(allbirds['page_id'])
        for r in self.fr['rows']:
            if r['source'] != 'none':
                self.assertIsInstance(r['age_days'], int)

    def test_plan_estimate_and_caps(self):
        p = self.fr['plan']
        self.assertEqual(len(p['pages']), 12)
        self.assertEqual(p['skipped'], ['Allbirds'])
        self.assertTrue(all(x['page_id'] for x in p['pages']))
        self.assertEqual(p['max_items'], 12 * p['limit_per_page'])
        self.assertLessEqual(p['estimate_usd'], p['cap_per_run_usd'])
        self.assertNotIn('token', json.dumps({k: v for k, v in p.items() if k != 'token'}).lower())
        self.assertIn('--live', self.fr['command'])

    def test_snapshot_rows_keep_no_competitor_text(self):
        item = {'ad_archive_id': '123', 'page_id': '150444458302730', 'page_name': 'Stance', 'is_active': True,
                'start_date': 1758067200, 'publisher_platform': ['FACEBOOK'],
                'snapshot': {'body': {'text': 'Why do socks slip? Get 20% off with code SAVE20.'}, 'display_format': 'VIDEO',
                             'cta_text': 'Shop Now', 'link_url': 'https://www.stance.com/x'}}
        row = audit.snap.ad_row(item, 'competitor', dt.date(2026, 9, 28))
        self.assertNotIn('first_line', row)
        self.assertNotIn('slip?', json.dumps(row))
        self.assertEqual(row['first_line_kind'], 'question')
        self.assertEqual(row['format'], 'video')
        self.assertEqual({o['tag'] for o in row['offers']}, {'percent_off', 'code'})
        self.assertIn({'tag': 'fit', 'word': 'slip'}, row['angles'])
        own = audit.snap.ad_row(item, 'self', dt.date(2026, 9, 28))
        self.assertEqual(own['first_line'], 'Why do socks slip?')

    def test_rules_r13(self):
        out = audit.run('bombas', WINDOW, self.tmp)
        r13 = [f for f in out if f['rule_id'] == 'COMP-R13']
        self.assertEqual([f['entity']['id'] for f in r13], ['no_id_allbirds'])
        self.assertFalse([f for f in out if f['rule_id'] == 'COMP-R14'])
        acts = api.rank('bombas', {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4})['actions']
        a = next(a for a in acts if a['rule_id'] == 'COMP-R13')
        self.assertEqual(a['owner'], 'person')

    def test_stale_rule(self):
        late = {'ends_on': '2026-10-20', 'days': 1, 'trailing': 0}
        out = audit.run('bombas', late, self.tmp)
        self.assertTrue([f for f in out if f['rule_id'] == 'COMP-R14'])


class TestLosses(TempBrain):
    """2.1: who we lose to by name, the reason by rule, the answer from verified facts."""
    def setUp(self):
        super().setUp()
        api.BRAIN_ROOT = self.tmp
        self.ls = api.handle(Req(['overview']))['losses']

    def test_rows_and_reasons(self):
        by = {r['name']: r for r in self.ls['rows']}
        self.assertEqual(by['Darn Tough']['theme'], 'durability')
        self.assertEqual(by['Uniqlo']['theme'], 'value')
        self.assertEqual(by['Stance']['theme'], 'style')
        self.assertIsNone(by['Stance']['our_one_star'])
        self.assertFalse(by['Kirkland']['fires'])
        self.assertIsNone(self.ls['win_rate'])
        for r in self.ls['rows']:
            self.assertIn('never quoted', r['answer'])
            self.assertIn('never disparage', r['answer'])

    def test_rule_r15(self):
        out = audit.run('bombas', WINDOW, self.tmp)
        ids = sorted(f['entity']['id'] for f in out if f['rule_id'] == 'COMP-R15')
        self.assertEqual(ids, ['lost_darn_tough', 'lost_stance', 'lost_uniqlo'])


class TestCategory(TempBrain):
    """2.2: the category ladder from doing nothing up, our rung marked, a move per rung."""
    def setUp(self):
        super().setUp()
        api.BRAIN_ROOT = self.tmp
        self.c = api.handle(Req(['overview']))['category']

    def test_rungs(self):
        keys = [r['key'] for r in self.c['rungs']]
        self.assertEqual(keys, ['premium', 'direct', 'adjacent', 'value', 'do_nothing'])
        by = {r['key']: r for r in self.c['rungs']}
        self.assertEqual(by['premium']['members'], ['Comrad Socks'])
        self.assertIn('Kirkland', by['value']['members'])
        self.assertEqual(len(by['adjacent']['members']), 7)
        self.assertEqual(self.c['our_rung'], 'direct')
        self.assertTrue(by['direct']['ours'])
        for r in self.c['rungs']:
            self.assertIsNone(r['trend'])
            self.assertTrue(r['move'] and r['capability'])

    def test_r16_is_a_connect_action(self):
        out = audit.run('bombas', WINDOW, self.tmp)
        f = next(f for f in out if f['rule_id'] == 'COMP-R16')
        self.assertEqual(f['status'], 'unavailable')
        acts = api.rank('bombas', {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4})['actions']
        a = next(a for a in acts if a['rule_id'] == 'COMP-R16')
        self.assertEqual((a['owner'], a['artefact']['kind']), ('person', 'connector_setup'))


class TestReviews(TempBrain):
    """2.3: our review themes against the claims they lead with; attacked theme on the plan."""
    def setUp(self):
        super().setUp()
        api.BRAIN_ROOT = self.tmp
        self.rv = api.handle(Req(['overview']))['reviews']

    def test_rows(self):
        rows = self.rv['rows']
        self.assertEqual([r['one_star'] for r in rows], sorted((r['one_star'] for r in rows), reverse=True))
        self.assertEqual(self.rv['attack']['theme'], 'durability')
        self.assertIn('Darn Tough Vermont', self.rv['attack']['leaders'])
        for r in rows:
            self.assertIsNone(r['their_reviews'])

    def test_rule_r17(self):
        out = audit.run('bombas', WINDOW, self.tmp)
        f = next(f for f in out if f['rule_id'] == 'COMP-R17')
        self.assertEqual(f['severity'], 'high')
        acts = api.rank('bombas', {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4})['actions']
        self.assertEqual(acts[0]['rule_id'], 'COMP-R17')


class TestPresence(TempBrain):
    """2.4: Amazon listings by style against our site's price per pair; theirs unavailable."""
    def setUp(self):
        super().setUp()
        api.BRAIN_ROOT = self.tmp
        self.pr = api.handle(Req(['overview']))['presence']

    def test_styles(self):
        by = {s['style']: s for s in self.pr['styles']}
        self.assertTrue(by['ankle']['undercut'])
        self.assertFalse(by['no show']['undercut'])
        self.assertAlmostEqual(by['ankle']['gap'], round(1 - by['ankle']['amazon_per_pair'] / by['ankle']['site_per_pair'], 3))
        self.assertIsNone(self.pr['theirs'])
        self.assertEqual(audit.mktmod.style_of_title("Women's Cushioned No Show Socks - 4 Pack"), 'no show')

    def test_rule_r18(self):
        out = audit.run('bombas', WINDOW, self.tmp)
        f = next(f for f in out if f['rule_id'] == 'COMP-R18')
        self.assertEqual(f['confidence'], 0.3)
        self.assertTrue(any(e['simulated'] for e in f['evidence']))


class TestVelocity(TempBrain):
    """2.5: launch rate estimate, share of voice by ads, slow-shipping rule with a plan that doubles the pace."""
    def setUp(self):
        super().setUp()
        api.BRAIN_ROOT = self.tmp
        self.v = api.handle(Req(['overview']))['velocity']

    def test_rates(self):
        self.assertEqual(audit.velmod.launch_rate(23, 12), round(23 / 12 * 7, 1))
        self.assertIsNone(audit.velmod.launch_rate(None, 12))
        shares = [r['share'] for r in self.v['rows'] if r['share'] is not None]
        self.assertAlmostEqual(sum(shares), 1, delta=0.01)
        self.assertTrue(self.v['slow'])
        self.assertLessEqual(self.v['target'], self.v['bar'])
        self.assertLessEqual(self.v['target'], 2 * self.v['our_counted_rate'] + 0.1)

    def test_rule_r19(self):
        out = audit.run('bombas', WINDOW, self.tmp)
        f = next(f for f in out if f['rule_id'] == 'COMP-R19')
        self.assertEqual(f['confidence'], 0.3)


class TestDigest(TempBrain):
    """2.6: the weekly brief is built in code from the plan, deterministic, signal only."""
    def test_digest(self):
        api.BRAIN_ROOT = self.tmp
        d = api.handle(Req(['digest']))
        self.assertIn('Top moves this week:', d['text'])
        self.assertIn('Never copy', d['text'])
        self.assertIn('1. ', d['text'])
        self.assertNotIn('\u2014', d['text'])
        self.assertEqual(api.handle(Req(['digest']))['text'], d['text'])


class TestNiche(TempBrain):
    """2.7: the bar in buyers from our own economics; candidate niches from the coverage matrix."""
    def setUp(self):
        super().setUp()
        api.BRAIN_ROOT = self.tmp
        self.n = api.handle(Req(['overview']))['niche']

    def test_bar(self):
        b = self.n['bar']
        self.assertEqual(b['buyers'], round(b['revenue_12m'] * 0.01 / (73 * 1.35)))
        self.assertEqual(b['contribution'], round(b['revenue'] * 27.5 / 100))
        for c in self.n['candidates']:
            self.assertGreaterEqual(c['their_share'], audit.nichemod.CANDIDATE_MIN)
            self.assertLess(c['our_share'], c['their_share'] / 3)
            self.assertIsNone(c['demand'])

    def test_bar_unavailable_without_inputs(self):
        self.edit('economics', lambda rows: [r for r in rows if r['field'] != 'aov_usd'])
        n = api.handle(Req(['overview']))['niche']
        self.assertIsNone(n['bar'])


class TestPremium(TempBrain):
    """2.8: premium signal scorecard and discount depth; undercut rule."""
    def setUp(self):
        super().setUp()
        api.BRAIN_ROOT = self.tmp
        self.pr = api.handle(Req(['overview']))['premium']

    def test_scores(self):
        by = {r['name']: r for r in self.pr['rows']}
        self.assertEqual(by['Feetures']['depth'], 15)
        self.assertEqual(by['Stance']['depth'], 0)
        self.assertEqual(by['Bombas']['depth'], 20)
        self.assertTrue(by['Darn Tough Vermont']['signals']['lifetime'])
        n = len(self.pr['signals'])
        for r in self.pr['rows']:
            self.assertAlmostEqual(r['score'], round(sum(r['signals'].values()) / n, 3))
        self.assertTrue(self.pr['fires'])
        self.assertEqual(audit.premmod.depth(['30% off', '50% off']), 50)
        self.assertEqual(audit.premmod.depth([]), 0)

    def test_rule_r21(self):
        out = audit.run('bombas', WINDOW, self.tmp)
        self.assertTrue([f for f in out if f['rule_id'] == 'COMP-R21'])


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

    def test_every_rule_has_a_builder_and_a_group(self):
        ids = [r['rule_id'] for r in audit.RULES]
        self.assertEqual(len(ids), len(set(ids)))
        for rid in ids:
            self.assertIn(rid, api.actions.BUILDERS)
            self.assertIn(rid, audit.RULE_GROUP)
            self.assertIn(audit.RULES[ids.index(rid)]['capability'], audit.AUTONOMY)

    def test_every_open_finding_ranks_at_every_edit(self):
        """Findings from edited brains (no competitors, stale window) still map to valid actions."""
        for window in (self.W, {'ends_on': '2026-10-20', 'days': 28, 'trailing': 4}):
            findings = audit.run('bombas', window, self.tmp)
            acts = api.rank('bombas', window)['actions']
            covered = {i for a in acts for i in a['finding_ids']}
            for f in findings:
                self.assertIn(f['id'], covered)
            for a in acts:
                self.assertEqual(api.actions.ranker.validate_action(a), [])

    def test_not_now_snoozes(self):
        path = self.tmp / 'decisions.json'
        a = self.out['actions'][0]
        path.write_text(json.dumps([{'finding_id': a['id'], 'choice': 'not_now', 'time': '2026-09-27T10:00:00Z'}]))
        kept = api.actions.ranker.apply_decisions([dict(x) for x in self.out['actions']], dt.date(2026, 9, 28), path)
        self.assertNotIn(a['id'], [x['id'] for x in kept])
        later = api.actions.ranker.apply_decisions([dict(x) for x in self.out['actions']], dt.date(2026, 10, 20), path)
        self.assertIn(a['id'], [x['id'] for x in later])

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
