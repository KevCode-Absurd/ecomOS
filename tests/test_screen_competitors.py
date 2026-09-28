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

    def test_winloss_kit_and_rule(self):
        self.assertIn('Screener', self.ls['kit'])
        self.assertIn('Darn Tough', self.ls['kit'])
        self.assertIn('consent', self.ls['kit'])
        self.assertEqual(self.ls['interviews'], 0)
        out = audit.run('bombas', WINDOW, self.tmp)
        f = next(f for f in out if f['rule_id'] == 'COMP-R29')
        acts = api.rank('bombas', {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4})['actions']
        a = next(a for a in acts if a['rule_id'] == 'COMP-R29')
        self.assertEqual(a['owner'], 'person')

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


class TestSearch(TempBrain):
    """2.9: search seeds from public lines; overlap unavailable as a connect action."""
    def setUp(self):
        super().setUp()
        api.BRAIN_ROOT = self.tmp
        self.s = api.handle(Req(['overview']))['search']

    def test_seeds(self):
        by = {r['term']: r for r in self.s['rows']}
        self.assertEqual(by['running socks']['kind'], 'contested')
        self.assertTrue(by['merino socks']['ours'])
        self.assertEqual(by['nurse socks']['kind'], 'gap')
        self.assertIsNone(self.s['overlap'])
        self.assertEqual(audit.searchmod.seeds_from(['Elite running socks, plantar fasciitis relief sock'], []),
                         {'running socks', 'relief socks'})

    def test_rules(self):
        out = audit.run('bombas', WINDOW, self.tmp)
        r23 = next(f for f in out if f['rule_id'] == 'COMP-R23')
        self.assertEqual(r23['status'], 'unavailable')
        self.assertTrue([f for f in out if f['rule_id'] == 'COMP-R22'])


class TestCaptures(TempBrain):
    """3.1: dated page-summary captures; their diff lights launch alerts before any ad-level snapshot."""
    def test_capture_file_on_record(self):
        paths = audit.capmod.captures('bombas')
        self.assertTrue(paths)
        cap = json.loads(paths[0].read_text())
        self.assertEqual(cap['source'], 'brain page summaries')
        self.assertIn('stance', cap['pages'])
        self.assertNotIn('allbirds', cap['pages'])

    def test_diff_rules(self):
        m = audit.market('bombas', dt.date(2026, 9, 28), self.tmp)
        prev = {'captured_at': '2026-09-14', 'pages': audit.capmod.summary(m['pages'])}
        cur = json.loads(json.dumps(prev))
        cur['captured_at'] = '2026-09-28'
        st = cur['pages']['stance']
        st['active_ads'] = 100
        st['offers'] = ['20% off']
        st['angles'] = st['angles'] + ['gifting']
        st['formats'] = dict(st['formats'], carousel=20)
        prev['pages']['stance']['formats'] = {k: v for k, v in prev['pages']['stance']['formats'].items() if k != 'carousel'}
        kinds = {e['kind'] for e in audit.capmod.diff(prev, cur)}
        self.assertEqual(kinds, {'ads_up', 'new_offer', 'new_angle', 'new_format', 'new_flight'})
        self.assertEqual(audit.capmod.diff(None, cur), [])
        ch = audit.changemod.build(m, m['brain'], None, None, dt.date(2026, 9, 28), audit.capmod.diff(prev, cur), 2)
        offer = next(e for e in ch['events'] if e['kind'] == 'new_offer')
        self.assertEqual(offer['verdict'], 'follow')
        m['changes'] = ch
        r24 = audit.rule_new_move(m, '2026-09-27')
        self.assertEqual(len(r24), 2)
        a = api.actions.action(r24[0], m, None)
        self.assertEqual(api.actions.ranker.validate_action(a), [])


class TestPriceMoves(TempBrain):
    """3.2: price moves between dated captures; a sharp cut goes on the plan with a value answer."""
    def test_moves_and_rule(self):
        m = audit.market_full('bombas', dt.date(2026, 9, 28), self.tmp)
        prev = {'captured_at': '2026-09-14', 'pages': audit.capmod.summary(m['pages'])}
        cur = json.loads(json.dumps(prev))
        cur['captured_at'] = '2026-09-28'
        cur['pages']['stance']['price_text'] = '10 to 20 per pair, median about 14'
        moves = audit.capmod.price_moves(prev, cur, audit.parse_band)
        self.assertEqual(len(moves), 1)
        self.assertEqual((moves[0]['kind'], moves[0]['from'], moves[0]['to']), ('cut', 18.0, 14.0))
        m['price_moves'] = {'moves': moves}
        f = audit.rule_price_cut(m, '2026-09-27')[0]
        self.assertEqual(f['severity'], 'high')
        a = api.actions.action(f, m, None)
        self.assertEqual(a['artefact']['kind'], 'copy')
        self.assertIn('reflex', a['artefact']['draft'])
        self.assertEqual(api.actions.ranker.validate_action(a), [])

    def test_no_moves_with_one_capture(self):
        api.BRAIN_ROOT = self.tmp
        pm = api.handle(Req(['overview']))['price_moves']
        self.assertEqual(pm['moves'], [])
        self.assertGreaterEqual(pm['captures'], 1)


class TestLanding(TempBrain):
    """3.3: landing page tracking for the top 3 threats; untracked reads not tracked, never blank."""
    def test_rows_and_rule(self):
        api.BRAIN_ROOT = self.tmp
        ld = api.handle(Req(['overview']))['landing']
        self.assertEqual(len(ld['rows']), 3)
        pts = [r['points'] for r in ld['rows']]
        self.assertEqual(pts, sorted(pts, reverse=True))
        for r in ld['rows']:
            self.assertFalse(r['tracked'])
            self.assertIsNone(r['last_capture'])
            self.assertTrue(r['urls'])
        out = audit.run('bombas', WINDOW, self.tmp)
        self.assertTrue([f for f in out if f['rule_id'] == 'COMP-R26'])


class TestCards(TempBrain):
    """3.5: battlecards per direct page with freshness; stale rule on a late window."""
    def test_cards(self):
        api.BRAIN_ROOT = self.tmp
        bc = api.handle(Req(['overview']))['battlecards']
        self.assertEqual(len(bc['rows']), 5)
        for r in bc['rows']:
            self.assertFalse(r['stale'])
            self.assertTrue(r['claims'])
        late = audit.run('bombas', {'ends_on': '2027-01-10', 'days': 1, 'trailing': 0}, self.tmp)
        self.assertTrue([f for f in late if f['rule_id'] == 'COMP-R27'])
        self.assertFalse([f for f in audit.run('bombas', WINDOW, self.tmp) if f['rule_id'] == 'COMP-R27'])


class TestFrames(TempBrain):
    """3.6: positioning lines against shopper frames; test brief when the top frame is not in our line."""
    def test_frames(self):
        api.BRAIN_ROOT = self.tmp
        fr = api.handle(Req(['overview']))['frames']
        self.assertEqual(fr['frames'][0]['frame'], 'buy_it_for_life')
        self.assertFalse(fr['frames'][0]['in_our_frame'])
        self.assertEqual([x['key'] for x in fr['lines']], ['A', 'B', 'C'])
        self.assertIn('Guarantee', fr['lines'][1]['proof'])
        self.assertIsNone(fr['score'])
        self.assertTrue(fr['fires'])
        out = audit.run('bombas', WINDOW, self.tmp)
        self.assertTrue([f for f in out if f['rule_id'] == 'COMP-R28'])


class TestThresholds(TempBrain):
    """3.8: thresholds the brand tunes with a plans record; defaults come back when the record goes."""
    def test_override_and_reset(self):
        path = self.tmp / 'bombas' / 'plans.json'
        rows = json.loads(path.read_text()) if path.exists() else []
        rows.append({'id': 'bombas.plans.competitor_thresholds', 'brand': 'bombas', 'section': 'plans',
                     'field': 'competitor_thresholds', 'value': {'price_band_low': 40, 'threat_points': 5, 'bogus': 1},
                     'text': 'founder thresholds', 'tier': 'approved'})
        path.write_text(json.dumps(rows))
        out = audit.run('bombas', WINDOW, self.tmp)
        self.assertFalse([f for f in out if f['rule_id'] == 'COMP-R02'])
        m = audit.market('bombas', dt.date(2026, 9, 28), self.tmp)
        th = m['thresholds']['values']
        self.assertEqual((th['price_band_low']['value'], th['price_band_low']['source']), (40, 'brain'))
        self.assertNotIn('bogus', th)
        self.assertEqual(sum(p['verdict']['text'] == 'Threat' for p in m['pages'] if p['role'] != 'self'), 3)
        path.write_text(json.dumps([r for r in rows if r['field'] != 'competitor_thresholds']))
        m = audit.market('bombas', dt.date(2026, 9, 28), self.tmp)
        self.assertEqual(audit.PRICE_BAND, (85, 115))
        self.assertEqual(m['thresholds']['values']['threat_points']['source'], 'default')
        self.assertTrue([f for f in audit.run('bombas', WINDOW, self.tmp) if f['rule_id'] == 'COMP-R02'])


class TestSecondBrand(unittest.TestCase):
    """3.9: plug and play. A minimal second brand renders every route with honest unavailable states and no Bombas fact."""
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        d = self.tmp / 'acme'
        d.mkdir()
        (d / 'identity.json').write_text(json.dumps([{'id': 'acme.identity.one_line_pitch', 'brand': 'acme', 'section': 'identity',
                                                      'field': 'one_line_pitch', 'value': 'warm wool hats'}]))
        (d / 'products.json').write_text(json.dumps([{'id': 'acme.products.lines', 'brand': 'acme', 'section': 'products',
                                                      'field': 'lines', 'value': ['HATS']}]))
        (d / 'competitors.json').write_text(json.dumps([{'id': 'acme.competitors.hatco', 'brand': 'acme', 'section': 'competitors',
            'field': 'hatco', 'value': {'name': 'HatCo', 'positioning': 'merino hats with a lifetime guarantee',
            'price_band_usd': '20 to 40 per pair, median 30', 'hook_types': ['lifetime guarantee', 'comfort'], 'active_ads_seen': 12},
            'source': {'type': 'ad_library', 'captured_at': '2026-09-20'}}]))
        api.BRAIN_ROOT = self.tmp

    def tearDown(self):
        api.BRAIN_ROOT = None
        shutil.rmtree(self.tmp)

    def test_every_route(self):
        q = {'brand': ['acme']}
        out = {k: api.handle(Req([k], query=q)) for k in ('overview', 'plan', 'digest', 'audit')}
        for k, v in out.items():
            self.assertIsInstance(v, dict, k)
        blob = json.dumps(out)
        for word in ('Bombas', 'Stance', 'Darn Tough', 'COMFORT20', 'sock'):
            self.assertNotIn(word, blob)
        o = out['overview']
        self.assertEqual(o['term']['unit'], 'pair')   # its one price band says "per pair"; a band "per hat" would say hat
        self.assertEqual(o['pages']['rows'][0]['name'], 'HatCo')
        self.assertFalse(o['ladder']['available'])
        self.assertIsNone(o['niche']['bar'])
        self.assertIn('error', o['freshness']['plan'])
        # unavailable, never zero: nothing read means None, not 0
        self.assertIsNone(o['coverage']['all']['our_ads'])
        self.assertIsNone(o['presence']['listings'])
        self.assertIsNone(o['premium']['our_depth'])
        self.assertIsNone(o['premium']['rows'][-1]['signals']['no_discount'])
        self.assertIsNone(o['angles'][0]['brand_ads'])
        self.assertIn('hats', o['category']['rungs'][1]['label'].lower().replace('hat ', 'hats '))
        for a in api.rank('acme', {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4})['actions']:
            self.assertEqual(api.actions.ranker.validate_action(a), [])


class TestPlacements(TempBrain):
    """4.1: placements per page; a rival on a new placement is a change; our placements unavailable, not zero."""
    def test_placements_and_new_channel(self):
        api.BRAIN_ROOT = self.tmp
        pl = api.handle(Req(['overview']))['placements']
        self.assertIn('threads', pl['platforms'])
        self.assertFalse(pl['ours_known'])
        self.assertEqual(pl['gaps'], [])
        m = audit.market('bombas', dt.date(2026, 9, 28), self.tmp)
        prev = {'captured_at': '2026-09-14', 'pages': audit.capmod.summary(m['pages'])}
        cur = json.loads(json.dumps(prev))
        cur['captured_at'] = '2026-09-28'
        prev['pages']['stance']['platforms'] = [x for x in prev['pages']['stance']['platforms'] if x != 'threads']
        ev = [e for e in audit.capmod.diff(prev, cur) if e['kind'] == 'new_channel']
        self.assertEqual([e['value'] for e in ev], ['threads'])


class TestGapLines(TempBrain):
    """4.2: every desk block ends in a gap line tied to its action, or says what holds."""
    def test_every_section_has_a_line(self):
        api.BRAIN_ROOT = self.tmp
        d = api.handle(Req(['overview']))
        html = (SCREEN / 'index.html').read_text(encoding='utf-8')
        desk = html.split('id="desk-src"', 1)[1].split('<!-- 6. The audit -->', 1)[0]
        import re as _re
        ids = _re.findall(r'<div (?:class="[^"]*" )?id="([a-z-]+)"', desk)
        ids = [i for i in ids if not i.endswith('-sub')]
        acts = {a['id'] for a in api.rank('bombas', {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4})['actions']}
        for i in ids:
            self.assertIn(i, d['gap_lines'], i)
            g = d['gap_lines'][i]
            self.assertTrue(g['text'])
            if g['action_id']:
                self.assertIn(g['action_id'], acts)
        self.assertEqual(d['gap_lines']['reviews']['action_id'].split('.')[1], 'COMP-R17')


class TestHistory(unittest.TestCase):
    """4.7: threat points per page across dated captures; a page missing from a capture reads None."""
    def test_history(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            (tmp / 'x').mkdir()
            for day, pts in (('2026-09-14', 3), ('2026-09-28', 5)):
                (tmp / 'x' / f'{day}.json').write_text(json.dumps({'captured_at': day, 'pages': {
                    'a': {'name': 'A', 'role': 'competitor', 'points': pts, 'active_ads': 10},
                    **({'b': {'name': 'B', 'role': 'competitor', 'points': 1, 'active_ads': 3}} if day == '2026-09-28' else {})}}))
            h = audit.capmod.history('x', tmp)
            self.assertEqual(h['dates'], ['2026-09-14', '2026-09-28'])
            self.assertEqual(h['rows'][0]['points'], [3, 5])
            self.assertEqual(h['rows'][1]['points'], [None, 1])
        finally:
            shutil.rmtree(tmp)


class TestMacros(TempBrain):
    """4.8: support answers from verified proof only; a doubt with no proof gets no answer."""
    def test_macros(self):
        api.BRAIN_ROOT = self.tmp
        mc = api.handle(Req(['overview']))['macros']
        self.assertTrue(mc['rows'])
        self.assertEqual(mc['ready'], sum(1 for x in mc['rows'] if x['answer']))
        stance = next(x for x in mc['rows'] if 'Stance' in x['question'])
        self.assertIsNone(stance['answer'])
        self.assertIn('Stance', ' '.join(mc['missing']))
        for x in mc['rows']:
            if x['answer']:
                self.assertNotIn('worse', x['answer'].lower())
                self.assertTrue(x['source'])


class TestRoomMetrics(TempBrain):
    """4.9: the room's 15 metrics, each computed or unavailable with a reason; none reads 0 for unknown."""
    def test_metrics(self):
        api.BRAIN_ROOT = self.tmp
        rows = api.handle(Req(['overview']))['room_metrics']
        self.assertEqual(len(rows), 15)
        by = {r['key']: r for r in rows}
        self.assertEqual(by['competitors_tracked']['value'], 12)
        self.assertEqual(by['discount_depth_vs_category']['value'], 20)
        for k in ('new_creative_count', 'win_rate_vs_named_competitor', 'positioning_test_score', 'price_change_count'):
            self.assertIsNone(by[k]['value'])
            self.assertTrue(by[k]['unavailable'])
        for r in rows:
            self.assertTrue(r['formula'])
            if r['value'] is None:
                self.assertTrue(r['unavailable'], r['key'])


class TestHandoff(TempBrain):
    """5.1: the competitor_snapshot hand-off (events.md) and experiment registry drafts."""
    def test_snapshot_and_experiments(self):
        api.BRAIN_ROOT = self.tmp
        snap = api.handle(Req(['competitor_snapshot']))
        self.assertEqual(snap['table'], 'competitor_snapshot')
        self.assertEqual(len(snap['rows']), 11)
        for r in snap['rows']:
            self.assertEqual(set(r), set(audit.handmod.FIELDS))
            self.assertFalse(r['simulated'])
        on_file = json.loads((SCREEN / 'fixtures' / 'competitor_snapshot_bombas.json').read_text())
        self.assertEqual(on_file['fields'], audit.handmod.FIELDS)
        exp = api.handle(Req(['experiments']))['rows']
        self.assertTrue(exp)
        for r in exp:
            self.assertEqual(r['status'], 'proposed')
            self.assertIsNone(r['id'])
            for k in ('hypothesis', 'source', 'variant', 'read_point', 'brain_refs'):
                self.assertIn(k, r)


class TestSeason(TempBrain):
    """5.3: dated season phases from US holidays; gifting gap when the season is close."""
    def test_dates_and_rule(self):
        self.assertEqual(audit.seasonmod.black_friday(2026), dt.date(2026, 11, 27))
        self.assertEqual(audit.seasonmod.black_friday(2025), dt.date(2025, 11, 28))
        api.BRAIN_ROOT = self.tmp
        sn = api.handle(Req(['overview']))['season']
        self.assertEqual(sn['cyber_monday'], '2026-11-30')
        self.assertEqual(sn['ship_cutoff'], '2026-12-17')
        self.assertEqual([p['phase'] for p in sn['phases']], ['Watch', 'Build', 'Defend', 'Gift window', 'Read'])
        self.assertEqual(sn['season_share_pct'], 26)
        self.assertTrue(sn['fires'])
        out = audit.run('bombas', WINDOW, self.tmp)
        self.assertTrue([f for f in out if f['rule_id'] == 'COMP-R30'])
        summer = audit.run('bombas', {'ends_on': '2026-06-01', 'days': 1, 'trailing': 0}, self.tmp)
        self.assertFalse([f for f in summer if f['rule_id'] == 'COMP-R30'])


class TestReview(TempBrain):
    """5.4: the quarterly positioning review with decisions for the founder."""
    def test_review(self):
        api.BRAIN_ROOT = self.tmp
        rv = api.handle(Req(['overview']))['review']
        self.assertEqual(rv['quarter'], 'Q3 2026')
        self.assertEqual(len(rv['decisions']), 3)
        self.assertIn('buy it for life', rv['text'])
        self.assertIn('Decisions for the founder', rv['text'])


PW = Path('/opt/node22/lib/node_modules/playwright')
CHROME = Path('/opt/pw-browsers/chromium')


@unittest.skipUnless(PW.exists() and CHROME.exists(), 'playwright or chromium not installed')
class TestBrowserSmoke(unittest.TestCase):
    """5.6: the page loads in a real browser with no script error, the desk tabs render, the report view renders."""
    def test_page_loads(self):
        import socket, subprocess, time
        with socket.socket() as sk:
            sk.bind(('127.0.0.1', 0))
            port = sk.getsockname()[1]
        srv = subprocess.Popen([sys.executable, str(ROOT / 'app' / 'server.py'), '--port', str(port)], cwd=ROOT,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            for _ in range(50):
                try:
                    socket.create_connection(('127.0.0.1', port), timeout=0.2).close()
                    break
                except OSError:
                    time.sleep(0.1)
            js = f"""
const {{ chromium }} = require('{PW}');
(async () => {{
  const b = await chromium.launch({{ executablePath: '{CHROME}', args: ['--no-sandbox'] }});
  const out = {{}};
  for (const [k, url] of [['main', 'http://127.0.0.1:{port}/screens/03-competitors/'], ['report', 'http://127.0.0.1:{port}/screens/03-competitors/?view=report']]) {{
    const p = await b.newPage({{ viewport: {{ width: 1280, height: 800 }} }});
    const errs = []; p.on('pageerror', (e) => errs.push(String(e)));
    await p.goto(url, {{ waitUntil: 'networkidle' }});
    await p.waitForTimeout(1500);
    const empty = [];
    for (const t of await p.$$('#desk .tab')) {{
      await t.click(); await p.waitForTimeout(200);
      empty.push(...await p.$$eval('#desk .section > [id]:not([id$="-sub"])', (xs) => xs.filter((x) => !x.children.length).map((x) => x.id)));
    }}
    out[k] = {{ errs, empty, tabs: await p.$$eval('#desk .tab', (t) => t.length), plan: await p.$$eval('.plan-item', (t) => t.length),
               moves: await p.$$eval('#r-moves tbody tr', (t) => t.length), queue: await p.$$eval('#r-queue li', (t) => t.length) }};
  }}
  console.log(JSON.stringify(out)); await b.close();
}})();"""
            res = subprocess.run(['node', '-e', js], capture_output=True, text=True, timeout=120)
            out = json.loads(res.stdout.strip().splitlines()[-1])
            self.assertEqual(out['main']['errs'], [])
            self.assertEqual(out['main']['tabs'], 4)
            self.assertEqual(out['main']['empty'], [])   # every desk block renders in its tab, late loaders included
            self.assertGreaterEqual(out['main']['plan'], 5)
            self.assertEqual(out['report']['errs'], [])
            self.assertGreaterEqual(out['report']['moves'], 5)
            self.assertGreaterEqual(out['report']['queue'], 1)
        finally:
            srv.terminate()
            srv.wait(timeout=10)


class TestNotes(TempBrain):
    """5.7: team notes on a page or action, validated, local only."""
    def setUp(self):
        super().setUp()
        self._notes = api.NOTES
        api.NOTES = self.tmp / 'notes'

    def tearDown(self):
        api.NOTES = self._notes
        super().tearDown()

    def post(self, body):
        r = Req(['notes'], method='POST')
        r.body = body
        return api.handle(r)

    def test_add_and_read(self):
        code, out = self.post({'entity': 'stance', 'text': 'Check their fall drop on Monday.'})
        self.assertEqual(code, 201)
        self.post({'entity': 'feetures', 'text': 'Bundle page changed.'})
        got = api.handle(Req(['notes'], query={'entity': ['stance']}))['notes']
        self.assertEqual([n['text'] for n in got], ['Check their fall drop on Monday.'])
        self.assertEqual(len(api.handle(Req(['notes']))['notes']), 2)

    def test_rejects_bad_input(self):
        self.assertEqual(self.post({'entity': '../x', 'text': 'hi'})[0], 400)
        self.assertEqual(self.post({'entity': 'stance', 'text': '  '})[0], 400)
        self.assertEqual(self.post('nope')[0], 400)
        code, out = self.post({'entity': 'stance', 'text': 'x' * 900})
        self.assertEqual(len(out['note']['text']), api.NOTE_MAX)


class TestBriefPack(TempBrain):
    """5.8: every drafted artefact grouped by the team that ships it."""
    def test_pack(self):
        api.BRAIN_ROOT = self.tmp
        b = api.handle(Req(['briefs']))
        teams = {t['team']: t for t in b['teams']}
        self.assertIn('creative', teams)
        self.assertIn('Brief pack for the creative team', teams['creative']['text'])
        self.assertIn('Never copy', teams['creative']['text'])
        self.assertEqual(b['total'], sum(t['n'] for t in b['teams']))
        self.assertNotIn('setup', teams)


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

    def test_money_actions_are_sized_with_a_stop_rule(self):
        """Depth rule 5: an action that changes money or traffic gives a size and a stop or check-again rule with a date."""
        money = {'ad_brief', 'offer', 'test_brief', 'page_section', 'copy', 'price_change', 'listing_fix', 'ticket'}
        for a in self.out['actions']:
            if a['artefact']['kind'] in money and a['status'] != 'unavailable':
                self.assertTrue(a.get('size') and a['size'].get('text'), a['id'])
                self.assertTrue(a.get('stop_rule') or a.get('win_rule'), a['id'])
                self.assertTrue(a.get('stop_rule'), a['id'])
                self.assertRegex(a['check_on'], r'^\d{4}-\d{2}-\d{2}$')

    def test_every_builder_sizes_money_actions(self):
        """Builders for rules that do not fire on this capture still carry a stop rule when they change money."""
        src = (SCREEN / 'actions.py').read_text(encoding='utf-8')
        import re as _re
        for name in ('act_new_move', 'act_card', 'act_above', 'act_corner', 'act_price_cut'):
            body = src.split('def ' + name, 1)[1].split('\ndef ', 1)[0]
            m = _re.search(r'"stop_rule": ([^,]+)', body)
            self.assertIsNotNone(m, name)
            self.assertNotEqual(m.group(1).strip(), 'None', name)

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

    def test_desk_tabs_hold_every_desk_section(self):
        js = (SCREEN / 'screen.js').read_text(encoding='utf-8')
        html = (SCREEN / 'index.html').read_text(encoding='utf-8')
        desk = html.split('id="desk-src"', 1)[1].split('<!-- 6. The audit -->', 1)[0]
        for sec_id in ('pages', 'history', 'cards', 'macros', 'landing', 'losses', 'category', 'reviews', 'coverage', 'velocity', 'mix', 'placements', 'refs', 'changes',
                       'review', 'map', 'frames', 'premium', 'prices', 'presence', 'niche', 'search', 'fresh', 'handoff'):
            self.assertIn(f'id="{sec_id}"', desk)
            self.assertIn(f"'{sec_id}'", js)

    def test_no_unit_word_in_js(self):
        js = (SCREEN / 'screen.js').read_text(encoding='utf-8')
        self.assertNotIn('a pair', js)
        self.assertNotIn('per pair', js)

    def test_no_duplicate_functions(self):
        import re as _re
        js = (SCREEN / 'screen.js').read_text(encoding='utf-8')
        names = _re.findall(r'^\s*(?:async )?function (\w+)\(', js, _re.M)
        dup = sorted({n for n in names if names.count(n) > 1})
        self.assertEqual(dup, [])

    def test_action_lanes(self):
        js = (SCREEN / 'screen.js').read_text(encoding='utf-8')
        self.assertIn("api('/api/decisions?screen=' + SCREEN)", js)
        for k in ("key: 'due'", "key: 'agent'", "key: 'agent_drafts'", "key: 'person'"):
            self.assertIn(k, js)

    def test_report_view(self):
        html = (SCREEN / 'index.html').read_text(encoding='utf-8')
        js = (SCREEN / 'screen.js').read_text(encoding='utf-8')
        self.assertIn('href="?view=report"', html)
        for i in ('r-moves', 'r-queue', 'r-changed', 'r-logged', 'r-threats', 'r-numbers', 'r-caveats'):
            self.assertIn(f'id="{i}"', html)
            self.assertIn(f"'#{i}'", js)

    def test_no_brand_facts_in_js(self):
        js = (SCREEN / 'screen.js').read_text(encoding='utf-8')
        for word in ('Bombas', 'Stance', 'Darn Tough', 'Smartwool', 'Feetures', 'Comrad', 'COMFORT20'):
            self.assertNotIn(word, js)
        self.assertNotIn('GPT', js)


class TempInputs(TempBrain):
    """Round 6: first-party records logged on the page go to a temp inputs folder."""
    def setUp(self):
        super().setUp()
        api.BRAIN_ROOT = self.tmp
        self._folder = api.audit.inpmod.FOLDER
        api.audit.inpmod.FOLDER = self.tmp / 'inputs'

    def tearDown(self):
        api.audit.inpmod.FOLDER = self._folder
        super().tearDown()

    def post(self, body, today=DAY):
        r = Req(['inputs'], method='POST', query={'today': [today]})
        r.body = body
        return api.handle(r)

    def interview(self, outcome, competitor, reason, date=DAY):
        return self.post({'kind': 'interview', 'outcome': outcome, 'competitor': competitor, 'reason': reason, 'date': date})


class TestWinLoss(TempInputs):
    """6.1: win-loss interviews logged on the page fill the win rate and hold COMP-R29 until 5 are on file."""
    def test_validation(self):
        self.assertEqual(self.interview('maybe', 'Darn Tough', 'durability')[0], 400)
        self.assertEqual(self.interview('loss', 'Nobody Inc', 'durability')[0], 400)
        self.assertEqual(self.interview('loss', 'Darn Tough', 'vibes')[0], 400)
        self.assertEqual(self.interview('loss', 'Darn Tough', 'durability', '2030-01-01')[0], 400)
        self.assertEqual(self.post({'kind': 'gossip'})[0], 400)
        code, out = self.interview('loss', 'darn tough', 'durability')
        self.assertEqual(code, 201)
        rec = out['record']
        self.assertEqual(rec['competitor'], 'Darn Tough')
        self.assertEqual(set(rec) - {'id', 'kind', 'outcome', 'competitor', 'reason', 'date', 'by', 'logged_at'}, set())
        got = api.handle(Req(['inputs'], query={'kind': ['interview']}))
        self.assertEqual(len(got['records']), 1)

    def test_win_rate_and_rule(self):
        d = api.handle(Req(['overview']))
        self.assertIsNone(d['losses']['win_rate'])
        m = next(r for r in d['room_metrics'] if r['key'] == 'win_rate_vs_named_competitor')
        self.assertIsNone(m['value'])
        self.assertIn('COMP-R29', [f['rule_id'] for f in api.handle(Req(['plan']))['findings']])
        top = d['losses']['win_rate_name']
        for o in ('win', 'loss', 'loss', 'loss'):
            self.assertEqual(self.interview(o, top, 'durability')[0], 201)
        d = api.handle(Req(['overview']))
        self.assertEqual(d['losses']['win_rate'], 0.25)
        f = next(f for f in api.handle(Req(['plan']))['findings'] if f['rule_id'] == 'COMP-R29')
        self.assertIn(f'{top} (4)', f['sentence'])
        self.interview('win', top, 'comfort and feel')
        f = next(f for f in api.handle(Req(['plan']))['findings'] if f['rule_id'] == 'COMP-R29')
        self.assertNotIn(f'{top} (', f['sentence'])      # this name is covered; the others are still short
        m = next(r for r in api.handle(Req(['overview']))['room_metrics'] if r['key'] == 'win_rate_vs_named_competitor')
        self.assertEqual(m['value'], 0.4)

    def test_reason_codes_match_the_kit(self):
        self.assertEqual(api.audit.inpmod.REASON_CODES, api.audit.lossmod.REASON_CODES)


class TestRepeatLoss(TempInputs):
    """6.2: a loss reason repeated 3 times against one name puts the answer on the plan."""
    def test_rule_and_action(self):
        rank = lambda: api.rank('bombas', {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4})['actions']
        self.assertNotIn('COMP-R31', [a['rule_id'] for a in rank()])
        for r in ('fit and sizing', 'fit and sizing', 'durability'):
            self.interview('loss', 'Stance', r)
        self.assertNotIn('COMP-R31', [a['rule_id'] for a in rank()])
        self.interview('loss', 'Stance', 'fit and sizing')
        self.interview('win', 'Stance', 'comfort and feel')
        a = next(a for a in rank() if a['rule_id'] == 'COMP-R31')
        self.assertEqual(a['severity'], 'high')
        self.assertEqual(a['artefact']['kind'], 'page_section')
        self.assertIn('3 people chose Stance', a['why'])
        self.assertIn('fit and sizing', a['title'])
        self.assertTrue(a['stop_rule'] and a['check_on'] and a['size'])
        self.assertEqual(api.actions.ranker.validate_action(a), [])
        self.assertIn('20 percent of 5 interviews', a['artefact']['draft'])
        self.assertEqual(api.audit.RULE_GROUP['COMP-R31'], 'lost')
        self.assertIn('COMP-R31', api.SECTION_RULES['losses'])

    def test_every_reason_has_a_move(self):
        self.assertEqual(set(api.audit.lossmod.REASON_MOVE), set(api.audit.inpmod.REASON_CODES))
        kinds = {'ad_brief', 'offer', 'page_section', 'ticket', 'research_note'}
        self.assertTrue(all(v[0] in kinds for v in api.audit.lossmod.REASON_MOVE.values()))


class TestPriceSeen(TempInputs):
    """6.3: rival prices logged on the page; a cut of 15 percent against its own 30-day average goes on the plan."""
    def price(self, price, date, units=1, product='Merino crew', page='Darn Tough Vermont', url=''):
        return self.post({'kind': 'price_seen', 'page': page, 'product': product, 'price': price, 'units': units, 'date': date, 'url': url})

    def test_validation(self):
        self.assertEqual(self.price(20, DAY, page='Nobody')[0], 400)
        self.assertEqual(self.price(-1, DAY)[0], 400)
        self.assertEqual(self.price(20, DAY, units=0)[0], 400)
        self.assertEqual(self.price(20, DAY, product='<script>')[0], 400)
        self.assertEqual(self.price(20, DAY, url='http://x.com')[0], 400)
        code, out = self.price(60, DAY, units=3, url='https://example.com/p')
        self.assertEqual(code, 201)
        self.assertEqual(out['record']['per_unit'], 20.0)

    def test_cut_against_trailing_average(self):
        rank = lambda: api.rank('bombas', {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4})['actions']
        d = api.handle(Req(['overview']))
        m = next(r for r in d['room_metrics'] if r['key'] == 'price_change_count')
        self.assertIsNone(m['value'])
        self.price(26, '2026-09-01')
        self.price(24, '2026-09-10')
        self.price(22, '2026-08-01')   # outside the 30 days before the latest record
        self.price(21.25, '2026-09-27')
        pm = api.handle(Req(['overview']))['price_moves']
        mv = pm['logged']['moves'][0]
        self.assertEqual(mv['from'], 25.0)
        self.assertEqual(mv['change'], -0.15)
        self.assertEqual(mv['kind'], 'cut')
        a = next(a for a in rank() if a['rule_id'] == 'COMP-R25')
        self.assertIn('cut the price on Merino crew by 15 percent', a['why'])
        self.assertIn('30-day average', a['why'])
        self.assertEqual(a['severity'], 'high')
        self.assertEqual(api.actions.ranker.validate_action(a), [])
        m = next(r for r in api.handle(Req(['overview']))['room_metrics'] if r['key'] == 'price_change_count')
        self.assertEqual(m['value'], 1)

    def test_no_baseline_no_move(self):
        self.price(10, DAY)
        self.price(30, DAY, product='Hiker')
        pm = api.handle(Req(['overview']))['price_moves']
        self.assertEqual(pm['logged']['moves'], [])
        self.assertEqual(pm['logged']['with_baseline'], 0)
        self.assertEqual(len(pm['recent']), 2)


class TestCardCheck(TempInputs):
    """6.4: a person marks a battlecard checked; freshness counts from the check and the stale finding closes."""
    def check(self, page, date=DAY, dropped=0, today=DAY):
        return self.post({'kind': 'card_check', 'page': page, 'date': date, 'dropped': dropped}, today=today)

    def test_validation(self):
        self.assertEqual(self.check('Quince')[0], 400)        # not a direct page
        self.assertEqual(self.check('Stance', dropped=99)[0], 400)
        self.assertEqual(self.check('Stance', date='2031-01-01')[0], 400)
        self.assertEqual(self.check('stance')[0], 201)

    def test_check_closes_stale_card(self):
        late = {'ends_on': '2027-02-27', 'days': 28, 'trailing': 4}
        stale = [a for a in api.rank('bombas', late)['actions'] if a['rule_id'] == 'COMP-R27']
        self.assertTrue(stale)
        page = stale[0]['entity']['label'].replace(' battlecard', '')
        self.assertEqual(self.check(page, date='2027-02-20', today='2027-02-28')[0], 201)
        left = [a['entity']['label'] for a in api.rank('bombas', late)['actions'] if a['rule_id'] == 'COMP-R27']
        self.assertNotIn(f'{page} battlecard', left)
        d = api.handle(Req(['overview'], query={'today': ['2027-02-28']}))
        card = next(r for r in d['battlecards']['rows'] if r['name'] == page)
        self.assertEqual(card['verified_on'], '2027-02-20')
        self.assertEqual(card['age_days'], 8)
        self.assertEqual(card['checked_by'], 'a person')
        other = next(r for r in d['battlecards']['rows'] if r['name'] != page)
        self.assertEqual(other['checked_by'], 'the capture')


class TestFrameTest(TempInputs):
    """6.5: positioning poll results logged on the page; a win puts the ad test on the plan."""
    def poll(self, asked, new, cur, line='B'):
        return self.post({'kind': 'frame_test', 'line': line, 'asked': asked, 'prefer_new': new, 'prefer_current': cur})

    def test_validation(self):
        self.assertEqual(self.poll(200, 150, 100)[0], 400)   # more preferences than asked
        self.assertEqual(self.poll(10, 5, 5)[0], 400)
        self.assertEqual(self.poll(200, 100, 80, line='A')[0], 400)
        self.assertEqual(self.poll(200, 100, 80, line='b')[0], 201)

    def test_verdicts(self):
        v = api.audit.framemod.verdict
        base = {'line': 'B', 'date': DAY, 'id': 'x'}
        self.assertEqual(v(dict(base, asked=80, prefer_new=60, prefer_current=20))['verdict'], 'keep testing')
        self.assertEqual(v(dict(base, asked=200, prefer_new=110, prefer_current=90))['verdict'], 'win')
        self.assertEqual(v(dict(base, asked=200, prefer_new=100, prefer_current=95))['verdict'], 'keep current')
        self.assertEqual(v(dict(base, asked=200, prefer_new=104, prefer_current=90))['verdict'], 'keep testing')

    def test_win_goes_on_the_plan(self):
        rank = lambda: api.rank('bombas', {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4})['actions']
        ids = [a['rule_id'] for a in rank()]
        self.assertIn('COMP-R28', ids)
        self.assertNotIn('COMP-R32', ids)
        self.poll(200, 100, 95)
        ids = [a['rule_id'] for a in rank()]
        self.assertNotIn('COMP-R28', ids)          # tested now
        self.assertNotIn('COMP-R32', ids)
        self.poll(200, 120, 70)
        a = next(a for a in rank() if a['rule_id'] == 'COMP-R32')
        self.assertIn('by 25 points with 200 shoppers', a['why'])
        self.assertEqual(api.actions.ranker.validate_action(a), [])
        self.assertIn('Ad B first line:', a['artefact']['draft'])
        d = api.handle(Req(['overview']))
        self.assertEqual(d['frames']['score'], 25.0)
        m = next(r for r in d['room_metrics'] if r['key'] == 'positioning_test_score')
        self.assertEqual(m['value'], 25.0)
        self.assertIn('COMP-R32', api.SECTION_RULES['frames'])


class TestThresholdTuning(TempInputs):
    """6.6: thresholds tuned on the page, inside a range, newest wins over the brain record."""
    def tune(self, name, value):
        return self.post({'kind': 'threshold', 'name': name, 'value': value})

    def test_every_tunable_has_a_range(self):
        self.assertEqual(set(api.audit.TUNE_RANGE), set(api.audit.TUNABLE))
        for name, (lo, hi) in api.audit.TUNE_RANGE.items():
            mod, attr, idx = api.audit.TUNABLE[name]
            default = getattr(mod, '_default_' + attr, getattr(mod, attr))
            default = default[idx] if idx is not None else default
            self.assertTrue(lo <= default <= hi, name)

    def test_validation(self):
        self.assertEqual(self.tune('nonsense', 3)[0], 400)
        self.assertEqual(self.tune('stale_days', 400)[0], 400)
        self.assertEqual(self.tune('stale_days', 'x')[0], 400)
        code, out = self.tune('stale_days', 30)
        self.assertEqual(code, 201)
        self.assertEqual(out['record']['value'], 30)

    def test_change_applies_and_newest_wins(self):
        self.tune('threat_points', 3)
        self.tune('threat_points', 5)
        th = api.handle(Req(['plan']))['thresholds']['values']['threat_points']
        self.assertEqual(th['value'], 5)
        self.assertEqual(th['source'], 'screen')
        pages = api.handle(Req(['overview']))['pages']['rows']
        self.assertFalse([r for r in pages if r['role'] != 'self' and r['verdict']['points'] is not None
                          and r['verdict']['points'] < 5 and r['verdict']['text'] == 'Threat'])

    def test_screen_beats_brain_record(self):
        (self.tmp / 'bombas' / 'plans.json').exists() or (self.tmp / 'bombas' / 'plans.json').write_text('[]')
        self.edit('plans', lambda rows: rows + [{'id': 'bombas.plans.competitor_thresholds', 'section': 'plans',
                                                 'field': 'competitor_thresholds', 'value': {'stale_days': 21}}])
        self.assertEqual(api.handle(Req(['plan']))['thresholds']['values']['stale_days']['source'], 'brain')
        self.tune('stale_days', 10)
        v = api.handle(Req(['plan']))['thresholds']['values']['stale_days']
        self.assertEqual((v['value'], v['source']), (10, 'screen'))


class TestRunCapture(TempInputs):
    """6.7: the weekly capture runs from the page, from the brain only, once a day; history and diffs follow."""
    def setUp(self):
        super().setUp()
        self._cap, self._out = api.audit.capmod.FOLDER, api.audit.handmod.OUT
        api.audit.capmod.FOLDER = self.tmp / 'captures'
        api.audit.handmod.OUT = self.tmp
        shutil.copytree(SCREEN / 'fixtures' / 'captures' / 'bombas', self.tmp / 'captures' / 'bombas')

    def tearDown(self):
        api.audit.capmod.FOLDER, api.audit.handmod.OUT = self._cap, self._out
        super().tearDown()

    def capture(self, day):
        r = Req(['capture'], method='POST', query={'today': [day]})
        r.body = {}
        return api.handle(r)

    def test_capture_once_a_day(self):
        real = sorted((SCREEN / 'fixtures' / 'captures' / 'bombas').glob('*.json'))
        code, out = self.capture('2026-10-05')
        self.assertEqual(code, 201)
        self.assertEqual((out['captures'], out['since']), (2, '2026-09-28'))
        self.assertIsInstance(out['changes'], int)
        self.assertTrue((self.tmp / 'captures' / 'bombas' / '2026-10-05.json').exists())
        self.assertTrue((self.tmp / 'competitor_snapshot_bombas.json').exists())
        self.assertEqual(sorted((SCREEN / 'fixtures' / 'captures' / 'bombas').glob('*.json')), real)
        code, out = self.capture('2026-10-05')
        self.assertEqual((code, out['already']), (200, True))
        d = api.handle(Req(['overview'], query={'today': ['2026-10-05']}))
        self.assertEqual(d['history']['dates'], ['2026-09-28', '2026-10-05'])
        self.assertEqual(d['freshness']['captures'], {'n': 2, 'last': '2026-10-05'})

    def test_button_on_page(self):
        js = (SCREEN / 'screen.js').read_text(encoding='utf-8')
        self.assertIn("api(BASE + 'capture', { method: 'POST'", js)


class TestInputsLog(TempInputs):
    """6.8: every logged record listed with a summary; a mistake can be removed and the rules read the file again."""
    def test_list_and_remove(self):
        self.interview('loss', 'Stance', 'style')
        self.post({'kind': 'threshold', 'name': 'stale_days', 'value': 30})
        recs = api.handle(Req(['inputs']))['records']
        self.assertEqual([r['kind'] for r in recs], ['threshold', 'interview'])
        self.assertEqual(recs[1]['summary'], 'loss against Stance: style')
        self.assertEqual(recs[0]['summary'], 'stale days set to 30')
        r = Req(['inputs', 'remove'], method='POST')
        r.body = {'id': recs[0]['id']}
        self.assertEqual(api.handle(r)[0], 200)
        self.assertEqual(api.handle(r)[0], 404)
        self.assertEqual(api.handle(Req(['plan']))['thresholds']['values']['stale_days']['source'], 'default')
        self.assertEqual(len(api.handle(Req(['inputs']))['records']), 1)

    def test_every_kind_has_a_summary_and_label(self):
        js = (SCREEN / 'screen.js').read_text(encoding='utf-8')
        for kind in api.audit.inpmod.VALIDATE:
            self.assertIn(kind + ':', js)
        self.assertIn('id="inputs"', (SCREEN / 'index.html').read_text(encoding='utf-8'))


class TestFounderQueue(TempBrain):
    """6.9: the calls only the founder makes, top 5 by plan rank, each with what yes sets going."""
    def test_queue(self):
        api.BRAIN_ROOT = self.tmp
        p = api.handle(Req(['plan']))
        q = p['queue']
        self.assertTrue(1 <= len(q['items']) <= api.QUEUE_MAX)
        self.assertGreaterEqual(q['total'], len(q['items']))
        ranks = [x['rank'] for x in q['items']]
        self.assertEqual(ranks, sorted(ranks))
        for x in q['items']:
            a = p['actions'][x['rank'] - 1]
            self.assertEqual(a['id'], x['id'])
            self.assertTrue(x['gate'] or a['owner'] == 'agent_drafts')
            self.assertTrue(x['question'].startswith('Decide: ' if x['gate'] else 'Approve: '))
            self.assertTrue(x['yes'])

    def test_decided_moves_leave_the_queue(self):
        acts = [{'id': 'a', 'status': 'open', 'decision': {'choice': 'agent'}, 'capability': {'id': 'X', 'autonomy': 'founder_gate'},
                 'owner': 'agent_drafts', 'steps': [], 'title': 't', 'why': 'w', 'artefact': {'label': 'l'}},
                {'id': 'b', 'status': 'open', 'decision': None, 'capability': {'id': 'X', 'autonomy': 'agent_does'},
                 'owner': 'agent', 'steps': [], 'title': 't', 'why': 'w', 'artefact': {'label': 'l'}}]
        self.assertEqual(api.founder_queue(acts)['items'], [])


class TestInterviewThemes(TempInputs):
    """7.1: with 3 logged losses to a name, the reason and the answer come from the interviews, not the ad-angle rule."""
    def test_interviews_set_the_reason(self):
        row = lambda: next(x for x in api.handle(Req(['overview']))['losses']['rows'] if x['name'] == 'Darn Tough')
        self.assertEqual((row()['theme'], row()['theme_source']), ('durability', 'rule'))
        for r in ('fit and sizing', 'fit and sizing', 'price and value'):
            self.interview('loss', 'Darn Tough', r)
        x = row()
        self.assertEqual((x['theme'], x['theme_source'], x['reason']), ('fit', 'interviews', 'fit and sizing'))
        self.assertEqual(x['why'], '2 of 3 logged losses name fit and sizing')
        self.assertEqual(x['ladder'], 'bombas.objection_ladders.fit_and_sizing')
        self.assertIn('fit better', x['answer'])
        f = next(f for f in api.handle(Req(['plan']))['findings'] if f['rule_id'] == 'COMP-R15' and 'Darn Tough' in f['sentence'])
        self.assertIn('Our interviews say why', f['sentence'])
        self.assertIn('logged_losses_to_name', [e['metric'] for e in f['evidence']])

    def test_every_reason_maps(self):
        self.assertEqual(set(api.audit.lossmod.REASON_THEME), set(api.audit.inpmod.REASON_CODES))
        js = (SCREEN / 'screen.js').read_text(encoding='utf-8')
        for theme, _, _ in api.audit.lossmod.REASON_THEME.values():
            self.assertIn(theme + ":", js)


class TestInterviewCoverage(TempInputs):
    """7.2: COMP-R29 holds until each of the top 3 names we lose to has 5 interviews."""
    def test_per_name(self):
        ls = api.handle(Req(['overview']))['losses']
        names = [x['name'] for x in ls['rows'] if x['fires']][:3]
        self.assertTrue(names)
        size = lambda: next(a for a in api.rank('bombas', {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4})['actions']
                            if a['rule_id'] == 'COMP-R29')['size']['text']
        self.assertEqual(size(), f'{5 * len(names)} interviews left')
        for nm in names:
            for _ in range(5):
                self.interview('loss', nm, 'other')
            if nm != names[-1]:
                self.assertIn('COMP-R29', [f['rule_id'] for f in api.handle(Req(['plan']))['findings']])
        self.assertNotIn('COMP-R29', [f['rule_id'] for f in api.handle(Req(['plan']))['findings']])


class TestBandCheck(TempInputs):
    """7.3: logged prices sit on the band chart; one outside the page's public band puts a band update on the plan."""
    def price(self, price, product, page='Darn Tough Vermont'):
        return self.post({'kind': 'price_seen', 'page': page, 'product': product, 'price': price, 'units': 1, 'date': DAY})

    def test_in_and_out_of_band(self):
        band = lambda: next(b for b in api.handle(Req(['overview']))['ladder']['bands'] if b['name'] == 'Darn Tough Vermont')
        b = band()
        self.assertEqual(b['seen'], [])
        inside = (b['low'] + b['high']) / 2 if b['high'] is not None else b['low'] + 1
        self.price(inside, 'Hiker')
        self.assertEqual([x['in_band'] for x in band()['seen']], [True])
        rank = lambda: api.rank('bombas', {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4})['actions']
        self.assertNotIn('COMP-R33', [a['rule_id'] for a in rank()])
        self.price(b['low'] - 5, 'Light cushion')
        self.assertEqual(len(band()['out_of_band']), 1)
        a = next(a for a in rank() if a['rule_id'] == 'COMP-R33')
        self.assertEqual((a['owner'], a['artefact']['kind']), ('person', 'brain_record'))
        self.assertIn('outside the band on file', a['why'])
        self.assertEqual(api.actions.ranker.validate_action(a), [])
        self.assertIn('COMP-R33', api.SECTION_RULES['prices'])


class TestPriceRecheck(TempInputs):
    """7.4: a logged price older than 14 days is due a re-check; logging a fresh one clears it."""
    def test_recheck(self):
        body = {'kind': 'price_seen', 'page': 'Stance', 'product': 'Crew', 'price': 16, 'units': 1}
        self.post(dict(body, date='2026-09-01'))
        self.post(dict(body, product='Ankle', date='2026-09-20'))
        pm = api.handle(Req(['overview']))['price_moves']
        self.assertEqual([(x['product'], x['age_days']) for x in pm['recheck']], [('Crew', 27)])
        a = next(a for a in api.rank('bombas', {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4})['actions'] if a['rule_id'] == 'COMP-R34')
        self.assertEqual((a['owner'], a['size']['count']), ('person', 1))
        self.assertIn('Stance, Crew: last seen 2026-09-01', a['artefact']['draft'])
        self.assertEqual(api.actions.ranker.validate_action(a), [])
        self.post(dict(body, date=DAY))
        self.assertEqual(api.handle(Req(['overview']))['price_moves']['recheck'], [])
        self.assertNotIn('COMP-R34', [f['rule_id'] for f in api.handle(Req(['plan']))['findings']])


class TestDigestLogged(TempInputs):
    """7.5: the weekly brief says what the team logged this week."""
    def test_logged_in_brief(self):
        g = api.handle(Req(['digest']))
        self.assertEqual(g['logged']['n'], 0)
        self.assertIn('nothing yet', g['text'])
        self.interview('loss', 'Stance', 'style')
        self.interview('win', 'Stance', 'style', date='2026-09-10')   # older than the week
        g = api.handle(Req(['digest']))
        self.assertEqual((g['logged']['n'], g['logged']['counts']), (1, {'interview': 1}))
        self.assertIn('- loss against Stance: style', g['text'])


if __name__ == '__main__':
    unittest.main()
