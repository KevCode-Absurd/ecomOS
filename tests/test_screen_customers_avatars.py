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
        self.assertEqual({r['rule_id'] for r in audit.RULES}, {f'CUST-R{n:02d}' for n in range(1, 17)})


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
        self.assertNotIn('tiles', d)
        self.assertNotIn('insights', d)
        self.assertTrue(3 <= len(d['orientation']) <= 6)
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

    def test_repeat_chart_from_cohorts(self):
        c = api.repeat_by_cohort('bombas')
        self.assertFalse(c['unavailable'])
        self.assertLessEqual(len(c['values']), api.CHART_COHORTS)
        row = c['rows'][-1]
        self.assertAlmostEqual(row['rate'], round(min(row['active_m1_m3'] / row['customers'], 1), 4))
        self.assertLess(c['labels'][-1], '2026-07')
        o = {x['label']: x for x in api.overview(api._brain(Req(['overview'])))['orientation']}
        self.assertEqual(o['repeat in 3 months']['value'], c['values'][-1])

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


rank_engine = load('customers_avatars_rank_t', ROOT / 'app' / 'rank.py')
RANK_WINDOW = {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4}


class Round1Plan(TempBrain):
    """Feature 1.1: the plan first, orientation beside it, every finding ends in an action."""

    def test_page_order_plan_first_audit_last(self):
        html = (SCREEN / 'index.html').read_text(encoding='utf-8')
        body = html[html.index('<div class="screen">'):]
        ids = [body.index(f'id="{x}"') for x in ('plan', 'wrong', 'actions', 'avatars', 'audit')]
        self.assertEqual(ids, sorted(ids))
        self.assertNotIn('id="tiles"', html)
        first = body.index('<section')
        self.assertTrue(body[first:first + 60].startswith('<section class="section" id="plan-wrap">'))

    def test_orientation_numbers(self):
        d = api.handle(Req(['overview']))
        o = {x['label']: x for x in d['orientation']}
        self.assertEqual(o['rungs without proof']['value'], sum(1 for r in audit.rungs(api._brain(Req(['overview']))) if not r['proof_ids']))
        self.assertTrue(0 < o['returning share of orders']['value'] < 1)
        self.assertIsInstance(o['new customers, 28d']['value'], int)

    def test_orientation_unavailable_not_zero(self):
        win = api.daily_window('bombas', '2020-01-01')
        self.assertTrue(win['unavailable'])

    def test_every_finding_maps_to_a_valid_action(self):
        out = api.rank('bombas', RANK_WINDOW)
        acts = out['actions']
        self.assertTrue(acts)
        covered = {fid for a in acts for fid in a['finding_ids']}
        findings = audit.run('bombas', RANK_WINDOW, self.tmp)
        for f in findings:
            if f['status'] in ('open', 'unavailable'):
                self.assertIn(f['id'], covered)
        for a in acts:
            self.assertEqual(rank_engine.validate_action(a), [], a['id'])
            if a['status'] == 'unavailable':
                self.assertEqual(a['owner'], 'person')
        self.assertEqual(len({a['title'] for a in acts}), len(acts))

    def test_rank_deterministic(self):
        strip = lambda o: json.dumps([{k: v for k, v in a.items()} for a in o['actions']], sort_keys=True)
        self.assertEqual(strip(api.rank('bombas', RANK_WINDOW)), strip(api.rank('bombas', RANK_WINDOW)))


class AvatarBuilds(TempBrain):
    """Feature 1.2: every avatar card ends in the next build with an owner, steps and a draft."""

    def cards(self):
        return {a['key']: a for a in api.handle(Req(['overview']))['avatars']}

    def test_every_card_has_a_next_build(self):
        for a in self.cards().values():
            n = a['next']
            self.assertIn(n['kind'], ('offer', 'page_section', 'research_note', 'ad_brief'))
            self.assertIn(n['owner'], ('agent', 'agent_drafts'))
            self.assertTrue(2 <= len(n['steps']) <= 8)
            self.assertTrue(all(s['who'] in ('agent', 'person') for s in n['steps']))
            self.assertTrue(n['draft'].startswith('DRAFT'))
            self.assertNotIn('—', n['draft'] + n['title'] + n['why'])
            self.assertEqual(n['id'], '02-customers-avatars.build.' + a['key'])

    def test_rule_order(self):
        c = self.cards()
        self.assertEqual(c['durability_disappointed_repeat_customer']['next']['kind'], 'offer')
        self.assertEqual(c['reddit_runner']['next']['kind'], 'research_note')
        self.assertEqual(c['everyday_comfort_seeker']['next']['kind'], 'ad_brief')
        self.assertIn('Proof:', c['everyday_comfort_seeker']['next']['draft'])

    def test_proof_moves_offer_to_ad_brief(self):
        rows = self.section('objection_ladders')
        for lad in rows:
            if lad['id'] == 'bombas.objection_ladders.durability':
                lad['value']['rungs'][2]['proof_ids'] = ['bombas.policies.happiness_guarantee']
                lad['value']['rungs'][2]['proof'] = 'Holes in 60 days get a free pair.'
        self.write('objection_ladders', rows)
        n = self.cards()['durability_disappointed_repeat_customer']['next']
        self.assertEqual(n['kind'], 'ad_brief')
        self.assertIn('Holes in 60 days get a free pair.', n['draft'])

    def test_no_page_section_without_offer_use(self):
        rows = self.section('objection_ladders')
        for lad in rows:
            if lad['id'] == 'bombas.objection_ladders.durability':
                lad['value']['rungs'][2]['uses'] = ['copy', 'pdp']
        self.write('objection_ladders', rows)
        self.assertEqual(self.cards()['durability_disappointed_repeat_customer']['next']['kind'], 'page_section')

    def test_channels_and_no_reddit_testimonial(self):
        c = self.cards()
        self.assertEqual(c['reddit_runner']['channels'], [{'channel': 'Reddit', 'n': 5}])
        self.assertIn('our site', [x['channel'] for x in c['daily_compression_wearer']['channels']])
        for a in c.values():
            self.assertNotIn('(Reddit)', a['next']['draft'].split('Customer line:')[-1] if 'Customer line:' in a['next']['draft'] else '')


class Coverage(TempBrain):
    """Feature 1.3: avatar by channel, gaps carry a brief; format mix us against the category."""

    def test_cells_count_doubts_and_proof(self):
        d = api.handle(Req(['overview']))
        c = d['coverage']
        brain = api._brain(Req(['overview']))
        rungs = audit.rungs(brain)
        for row in c['rows']:
            aid = 'bombas.avatars.' + row['key']
            for col in c['cols']:
                cell = c['cells'][row['key']][col['key']]
                need = [r for r in rungs if aid in r['avatars'] and col['key'] in r['uses']]
                if not need:
                    self.assertIsNone(cell['us'])
                    continue
                self.assertEqual(cell['them'], len(need))
                self.assertEqual(cell['us'], sum(1 for r in need if r['proof_ids']))
                if cell['open']:
                    b = cell['brief']
                    self.assertTrue(b['draft'].startswith('DRAFT'))
                    self.assertEqual(b['owner'], 'agent_drafts')
                    self.assertTrue(2 <= len(b['steps']) <= 8)
        self.assertEqual(c['gaps'], sum(1 for r in c['rows'] for col in c['cols'] if c['cells'][r['key']][col['key']].get('open')))
        self.assertIn('Runner (Reddit)', c['skipped'])

    def test_format_mix_and_gap_brief(self):
        f = api.handle(Req(['overview']))['formats']
        self.assertTrue(f['available'])
        for r in f['rows']:
            self.assertTrue(0 <= r['us'] <= 1 and 0 <= r['them'] <= 1)
            self.assertEqual(r['gap'], r['them'] >= 0.15 and r['us'] < r['them'] * 0.5)
            self.assertEqual('brief' in r, r['gap'])
        self.assertIn('dynamic creative', f['gaps'])

    def test_format_mix_unavailable_without_pull(self):
        rows = [r for r in self.section('learnings') if not (isinstance(r.get('value'), dict) and r['value'].get('role') == 'self')]
        self.write('learnings', rows)
        f = api.handle(Req(['overview']))['formats']
        self.assertFalse(f['available'])
        self.assertTrue(f['reason'])


class Ladders(TempBrain):
    """Feature 1.4: every rung gets a verdict; every rung without proof gets a copy or offer action."""

    def ladders(self):
        return api.handle(Req(['overview']))['ladders']

    def test_verdict_rules(self):
        for r in self.ladders()['rows']:
            one, five = r['one_star'], r['five_star']
            if not r['proof_ids']:
                self.assertEqual(r['verdict'], 'answer')
                self.assertIn(r['action']['kind'], ('offer', 'copy'))
                self.assertEqual(r['action']['kind'] == 'offer', 'offer' in r['uses'])
            elif one >= 10 and one >= 2 * max(five, 1):
                self.assertEqual(r['verdict'], 'not_landing')
                self.assertEqual(r['action']['kind'], 'page_section')
            elif five > one:
                self.assertEqual(r['verdict'], 'lead')
                self.assertEqual(r['action']['kind'], 'ad_brief')
            else:
                self.assertEqual(r['verdict'], 'keep')
                self.assertIsNone(r['action'])

    def test_bombas_counts_and_order(self):
        L = self.ladders()
        self.assertEqual(L['counts']['answer'], 5)
        self.assertEqual(L['rows'][0]['id'], 'durability.3')
        order = [r['verdict'] for r in L['rows']]
        rank = {'answer': 0, 'not_landing': 1, 'lead': 2, 'keep': 3}
        self.assertEqual(order, sorted(order, key=rank.get))

    def test_actions_have_owner_steps_draft(self):
        for r in self.ladders()['rows']:
            a = r['action']
            if a:
                self.assertEqual(a['owner'], 'agent_drafts')
                self.assertTrue(2 <= len(a['steps']) <= 8)
                self.assertTrue(a['draft'].startswith('DRAFT'))
                self.assertNotIn('—', a['draft'])


class Words(TempBrain):
    """Feature 1.5: their words per rung, split doubt and win, Reddit marked language only, a copy brief per rung."""

    def test_words_link_to_rungs_and_split(self):
        W = api.handle(Req(['overview']))['words']
        self.assertTrue(W['rows'])
        rungs = {r['id']: r for r in audit.rungs(api._brain(Req(['overview'])))}
        for row in W['rows']:
            derived = set(rungs[row['id']]['derived_from'])
            for w in row['doubt_words'] + row['win_words']:
                self.assertIn(w['id'], derived)
                self.assertLessEqual(len(w['text'].split()), 15)
                self.assertEqual(w['language_only'], w['source'] == 'Reddit')
            self.assertLessEqual(len(row['doubt_words']), 6)
            self.assertTrue(row['brief']['head'][0].startswith('COPY BRIEF'))
            self.assertEqual(row['brief']['owner'], 'agent_drafts')
        stars = [w['star'] for r in W['rows'] for w in r['doubt_words'] if isinstance(w['star'], int)]
        self.assertTrue(stars and max(stars) <= 2)

    def test_generic_phrases_dropped(self):
        builds = api.builds
        self.assertTrue(builds._generic('Great socks!', {'bombas'}))
        self.assertTrue(builds._generic('Bombas socks', {'bombas'}))
        self.assertFalse(builds._generic('No slipping', {'bombas'}))


class Cohorts(unittest.TestCase):
    """Feature 1.6: cohort grid from cohorts.json with the breaks named and a retention move per break."""

    def grid(self, rows=None, as_of='2026-09-27'):
        from tables import brand_data
        data = brand_data('bombas')
        return api.builds.cohort_grid(rows if rows is not None else data.table('cohorts'), data.table('monthly'), as_of, [])

    def test_cells_from_table_and_unended_months_blank(self):
        from tables import brand_data
        src = {r['cohort']: r for r in brand_data('bombas').table('cohorts')}
        g = self.grid()
        self.assertTrue(g['available'])
        for r in g['rows']:
            for k, v in enumerate(r['values'], start=1):
                cal = api.builds._add(r['cohort'], k)
                if cal >= '2026-09':
                    self.assertIsNone(v)
                elif v is not None:
                    self.assertAlmostEqual(v, round(src[r['cohort']]['active_by_month'][k] / src[r['cohort']]['customers'], 4))
            self.assertTrue(any(v is not None for v in r['values']))

    def test_breaks_and_moves(self):
        g = self.grid()
        self.assertEqual(g['peak_month'], 2)
        self.assertEqual(g['calendar_break']['month'], '2026-01')
        ids = [m['id'] for m in g['moves']]
        self.assertIn('02-customers-avatars.retention.second_order', ids)
        self.assertIn('02-customers-avatars.retention.calendar_2026-01', ids)
        for m in g['moves']:
            self.assertEqual(rank_engine.validate_action(dict(m, rubric={'total': 0})), [])
            self.assertIn(m['artefact']['kind'], rank_engine.ARTEFACT_KINDS)
            self.assertTrue(m['artefact']['draft'].startswith('DRAFT'))
            self.assertRegex(m['why'], r'\d')

    def test_value_12m_only_for_full_cohorts(self):
        for r in self.grid()['rows']:
            if r['value_12m'] is not None:
                self.assertTrue(all(v is not None for v in r['values']))

    def test_empty_table_unavailable(self):
        self.assertFalse(self.grid(rows=[])['available'])


class Mix(unittest.TestCase):
    """Feature 1.7: returning share this year against last, the channel waterfall, and the moves."""

    def tables(self):
        from tables import brand_data
        data = brand_data('bombas')
        return data.table('monthly'), data.table('channels_monthly')

    def test_share_and_waterfall_add_up(self):
        monthly, channels = self.tables()
        x = api.builds.mix(monthly, channels, '2026-09-27')
        self.assertTrue(x['available'])
        self.assertEqual(x['latest'], '2026-08')
        m = {r['month']: r for r in monthly}['2026-08']
        self.assertAlmostEqual(x['share_now'], round(m['returning_customer_orders'] / m['orders'], 4))
        wf = x['waterfall']
        self.assertEqual(wf[0]['value'] + sum(s['value'] for s in wf[1:-1]), wf[-1]['value'])
        self.assertEqual(len(x['series']['this_year']), 12)

    def test_paid_returning_move_fires_and_is_valid(self):
        x = api.builds.mix(*self.tables(), '2026-09-27')
        self.assertGreaterEqual(x['paid_share_returning'], 0.25)
        mv = {m['id']: m for m in x['moves']}['02-customers-avatars.retention.paid_returning']
        self.assertEqual(rank_engine.validate_action(dict(mv, rubric={'total': 0})), [])
        self.assertIn('never writes', ' '.join(s['text'] for s in mv['steps']))

    def test_share_fall_names_worst_channel(self):
        monthly, channels = self.tables()
        monthly = [dict(r) for r in monthly]
        for r in monthly:
            if r['month'] == '2026-08':
                r['returning_customer_orders'] = r['orders'] * 0.30
        channels = [dict(r) for r in channels]
        for r in channels:
            if r['month'] == '2026-08' and r['channel'] == 'email':
                r['new_customer_orders'] = r['orders']
        x = api.builds.mix(monthly, channels, '2026-09-27')
        fall = {m['id']: m for m in x['moves']}['02-customers-avatars.retention.share_fall']
        self.assertIn('email', fall['title'])

    def test_short_history_unavailable(self):
        monthly, channels = self.tables()
        self.assertFalse(api.builds.mix(monthly[-5:], channels, '2026-09-27')['available'])


class Served(TempBrain):
    """Feature 1.8: avatars by reach and how well we serve them; situations the category serves and we do not."""

    def served(self):
        return api.handle(Req(['overview']))['served']

    def test_points_and_quadrants(self):
        x = self.served()
        rungs = audit.rungs(api._brain(Req(['overview'])))
        for p in x['points']:
            mine = [r for r in rungs if 'bombas.avatars.' + p['key'] in r['avatars']]
            one, five = sum(r['one_star'] or 0 for r in mine), sum(r['five_star'] or 0 for r in mine)
            self.assertAlmostEqual(p['y'], round(five / (one + five), 4))
            big, well = p['x'] >= x['mid_x'], p['y'] >= x['mid_y']
            self.assertEqual(p['quadrant'], {(True, True): 'core', (True, False): 'fix_first', (False, True): 'scale', (False, False): 'park'}[(big, well)])
        self.assertIn('Daily Compression Wearer', [u['name'] for u in x['unplaced']])
        fix = [v['name'] for v in x['verdicts'] if v['quadrant'] == 'fix_first']
        self.assertIn('Durability Disappointed Repeat Customer', fix)

    def test_situation_gap_has_research_action(self):
        segs = {s['segment']: s for s in self.served()['segments']}
        hike = segs['hiking and outdoor']
        self.assertEqual(hike['verdict'], 'gap')
        self.assertGreaterEqual(len(hike['theirs']), 2)
        self.assertEqual(hike['action']['kind'], 'research_note')
        self.assertEqual(hike['action']['steps'][-1]['who'], 'person')
        for s in segs.values():
            self.assertEqual(s['action'] is None, s['verdict'] in ('hold', 'own'))
        self.assertNotIn('Fit and Sizing Uncertain Buyer', segs['running']['ours'])

    def test_no_competitor_positioning_means_no_gap(self):
        rows = [r for r in self.section('competitors') if not (isinstance(r.get('value'), dict) and r['value'].get('positioning'))]
        self.write('competitors', rows)
        self.assertFalse([s for s in self.served()['segments'] if s['verdict'] == 'gap'])


class Misreads(TempBrain):
    """Feature 1.9: review themes by line against each avatar's job; misreads become page, copy or product actions."""

    def misreads(self):
        return api.handle(Req(['overview']))['misreads']

    def test_rule_holds_for_every_row(self):
        x = self.misreads()
        self.assertTrue(x['available'])
        med = x['median']
        for r in x['rows']:
            self.assertGreaterEqual(r['neg_share'], med)
            self.assertGreaterEqual(r['links'], 2)
            self.assertTrue(r['hits'])
            a = r['action']
            self.assertIn(a['kind'], rank_engine.ARTEFACT_KINDS)
            self.assertEqual(a['owner'] == 'person', a['kind'] == 'ticket')
            self.assertTrue(a['draft'].startswith('DRAFT'))
        top = x['rows'][0]
        self.assertEqual((top['avatar'], top['line']), ('Daily Compression Wearer', 'compression'))

    def test_line_verdicts(self):
        x = self.misreads()
        lines = {l['line']: l for l in x['lines']}
        self.assertEqual(lines['compression']['verdict'], 'problem')
        self.assertEqual(lines['no_show']['verdict'], 'split')
        self.assertIn('heel', lines['no_show']['polar'])
        self.assertIsNotNone(lines['no_show']['action'])
        for l in x['lines']:
            self.assertEqual(l['action'] is not None, l['verdict'] == 'split')

    def test_no_summaries_unavailable(self):
        self.write('products', [r for r in self.section('products') if r.get('field') != 'review_summary'])
        self.assertFalse(self.misreads()['available'])


class RankRound1(TempBrain):
    """Feature 1.10: rank gives every rule a real title, owner, steps and a drafted artefact."""

    def test_every_rule_fires_on_bombas(self):
        rules = {f['rule_id'] for f in audit.run('bombas', RANK_WINDOW, self.tmp)}
        self.assertEqual(rules, {f'CUST-R{n:02d}' for n in range(1, 17)})

    def test_open_actions_carry_drafts(self):
        acts = api.rank('bombas', RANK_WINDOW)['actions']
        for a in acts:
            self.assertEqual(rank_engine.validate_action(a), [], a['id'])
            self.assertIn(a['artefact']['kind'], rank_engine.ARTEFACT_KINDS)
            if a['status'] == 'open':
                self.assertTrue((a['artefact']['draft'] or '').startswith('DRAFT'), a['id'])
                self.assertNotIn('Draft the artefact', ' '.join(s['text'] for s in a['steps']))
            self.assertTrue(0 <= a['rubric']['total'] <= 100)
            self.assertNotIn('—', a['title'] + a['why'])

    def test_top_action_is_the_compression_misread(self):
        from_server = rank_engine.rank('02-customers-avatars', 'bombas', RANK_WINDOW, use_override=True)
        self.assertEqual(from_server['source'], 'screen')
        top = from_server['actions'][0]
        self.assertEqual(top['rule_id'], 'CUST-R05')
        self.assertIn('compression', top['title'])

    def test_person_tickets_score_ease_3(self):
        for a in api.rank('bombas', RANK_WINDOW)['actions']:
            if a['owner'] == 'person' and a['status'] == 'open':
                self.assertEqual(a['rubric']['ease'], 3)
            if a['status'] == 'unavailable':
                self.assertEqual(a['rubric']['ease'], 1)


class ThemeImpact(TempBrain):
    """Feature 2.1: theme impact = share x star gap, each negative theme tied to its ladder fix."""

    def test_impact_arithmetic_and_links(self):
        x = api.handle(Req(['overview']))['themes']
        self.assertTrue(x['available'])
        for r in x['rows']:
            self.assertAlmostEqual(r['impact'], round(r['share'] * (r['avg_with'] - r['avg_without']), 3), places=2)
            self.assertGreaterEqual(r['reviews'], 8)
            if r['action']:
                self.assertTrue(r['action']['draft'].startswith('DRAFT'))
        rows = {r['theme']: r for r in x['rows']}
        self.assertLess(rows['price_value']['impact'], 0)
        self.assertGreater(rows['comfort']['impact'], 0)
        self.assertIn('order_and_delivery', rows['delivery']['ladders'])
        self.assertTrue(rows['comfort']['action']['title'].startswith('Lead'))
        self.assertEqual([r['impact'] for r in x['rows']], sorted(r['impact'] for r in x['rows']))

    def test_rising_rule(self):
        b = api.builds
        recs = []
        for i in range(20):
            recs.append({'id': f'x{i}', 'value': {'themes': ['fit'] if i < 8 else ['comfort'], 'reviews': [{'star': 1 if i < 8 else 5, 'date': '2026-09-01' if i < 6 else '2025-01-01'}]}})
        x = b.theme_impact(recs, [], '2026-09-27')
        fit = {r['theme']: r for r in x['rows']}['fit']
        self.assertTrue(fit['rising'])

    def test_too_few_reviews_unavailable(self):
        self.assertFalse(api.builds.theme_impact([], [], '2026-09-27')['available'])


class CopyGap(TempBrain):
    """Feature 2.2: buyer praise words against our site and founder records."""

    def test_gap_rows(self):
        x = api.handle(Req(['overview']))['copy_gap']
        self.assertTrue(x['available'])
        self.assertLessEqual(len(x['rows']), 20)
        for r in x['rows']:
            self.assertGreaterEqual(r['reviews'], 3)
            self.assertNotIn('Reddit', r['sources'])
            self.assertFalse(r['word'].startswith('bomba'))
        words = {r['word']: r for r in x['rows']}
        self.assertEqual(words['soft']['verdict'], 'missing')
        self.assertTrue(x['action']['draft'].startswith('DRAFT'))

    def test_a_founder_record_closes_the_gap(self):
        rows = self.section('voice')
        rows.append({'id': 'bombas.voice.soft_line', 'brand': 'bombas', 'section': 'voice', 'field': 'soft_line', 'value': 'Soft on day one.',
                     'text': 'Soft on day one.', 'tier': 'approved', 'confidence': 1.0, 'visibility': 'private',
                     'source': {'type': 'founder', 'ref': 'test', 'captured_at': '2026-09-28'}})
        self.write('voice', rows)
        words = {r['word']: r for r in api.handle(Req(['overview']))['copy_gap']['rows']}
        self.assertEqual(words['soft']['verdict'], 'used')

    def test_no_own_records_unavailable(self):
        self.assertFalse(api.builds.copy_gap({}, [], set(), audit.source_name)['available'])


class Gate(TempBrain):
    """Feature 2.3: avatar evidence gate; each failed check is a task."""

    def test_checks_and_tasks(self):
        g = api.handle(Req(['overview']))['gate']
        core = [c['key'] for c in g['checks'] if c['core']]
        for r in g['rows']:
            self.assertEqual(r['status'] == 'validated', all(r['checks'][k] for k in core))
            failed = [k for k, v in r['checks'].items() if not v]
            self.assertEqual(sorted(t['check'] for t in r['tasks']), sorted(failed))
            for t in r['tasks']:
                self.assertIn(t['owner'], ('agent', 'agent_drafts', 'person'))
                self.assertEqual(t['steps'][-1]['who'], 'person')
        self.assertEqual(g['tasks'], sum(len(r['tasks']) for r in g['rows']))

    def test_five_quotes_two_sources_validates(self):
        rows = self.section('avatars')
        a = next(r for r in rows if r['id'] == 'bombas.avatars.everyday_comfort_seeker')
        a['evidence'] = a['evidence'] + [{'quote': f'extra line {i}', 'ref': 'https://www.amazon.com/x'} for i in range(3)]
        self.write('avatars', rows)
        g = {r['key']: r for r in api.handle(Req(['overview']))['gate']['rows']}
        self.assertEqual(g['everyday_comfort_seeker']['status'], 'validated')


class Hooks(TempBrain):
    """Feature 2.4: hook bank from phrases repeated across praise reviews."""

    def test_hooks(self):
        h = api.handle(Req(['overview']))['hooks']
        self.assertTrue(h['rows'])
        fill = api.builds.HOOK_FILL
        for r in h['rows']:
            self.assertGreaterEqual(r['reviews'], 3)
            w = r['hook'].split()
            self.assertTrue(2 <= len(w) <= 4)
            self.assertNotIn(w[0], fill)
            self.assertNotIn(w[-1], fill)
            self.assertFalse(any(t.startswith('bomba') for t in w))
            self.assertLessEqual(len(r['avatars']), 3)
        self.assertIn('stay in place', [r['hook'] for r in h['rows']])
        self.assertEqual(h['brief']['owner'], 'agent_drafts')

    def test_reddit_never_counts(self):
        recs = [{'id': f'r{i}', 'value': {'reviews': [{'star': 5, 'source': 'reddit', 'quote': 'stay in place forever'}]}} for i in range(5)]
        self.assertEqual(api.builds.hooks(recs, [], [], set(), audit.source_name)['rows'], [])


class Forces(TempBrain):
    """Feature 2.5: four forces per avatar; under-researched avatars get a switch interview plan."""

    def test_rule(self):
        x = api.handle(Req(['overview']))['forces']
        for r in x['rows']:
            n = {k: v['n'] for k, v in r['forces'].items()}
            tot = sum(n.values())
            missing = [k for k, v in n.items() if v < 1]
            self.assertEqual(r['missing'], missing)
            under = bool(missing) or not tot or (n['anxiety'] + n['habit']) / tot < 0.15
            self.assertEqual(r['under'], under)
            self.assertEqual(r['action'] is not None, under)
            if r['action']:
                self.assertEqual(r['action']['owner'], 'person')
        self.assertIn('Durability Disappointed Repeat Customer', [r['name'] for r in x['rows'] if r['under']])

    def test_competitor_name_counts_as_habit(self):
        av = [{'id': 'b.avatars.x', 'key': 'x', 'name': 'X', 'quotes': [{'quote': 'I always wore Darn Tough before', 'source': 'Amazon'}]}]
        x = api.builds.forces(av, [], [], ['Darn Tough'])
        self.assertEqual(x['rows'][0]['forces']['habit']['n'], 1)


class AvatarDraft(TempBrain):
    """Feature 2.6: draft an avatar for an unserved situation and write it, inferred, on approval."""

    def test_draft_shape_and_valid(self):
        sys.path.insert(0, str(ROOT / 'app' / 'brain'))
        import validate
        drafts = {d['segment']: d for d in api.handle(Req(['overview']))['drafts']}
        self.assertIn('hiking and outdoor', drafts)
        rec = drafts['hiking and outdoor']['record']
        self.assertEqual(validate.check_record(rec, 'avatars'), [])
        self.assertEqual(rec['tier'], 'inferred')
        self.assertIsNone(rec['value']['job'])
        for e in rec['evidence']:
            self.assertNotIn('reddit', e['ref'])

    def test_post_writes_once(self):
        code, res = api.handle(Req(['avatars', 'draft'], 'POST', body={'segment': 'hiking and outdoor'}))
        self.assertEqual(code, 201)
        ids = [r['id'] for r in self.section('avatars')]
        self.assertIn('bombas.avatars.situation_hiking_and_outdoor', ids)
        self.assertEqual(api.handle(Req(['avatars', 'draft'], 'POST', body={'segment': 'hiking and outdoor'}))[0], 409)
        self.assertEqual(api.handle(Req(['avatars', 'draft'], 'POST', body={'segment': 'nope'}))[0], 400)


class Moments(unittest.TestCase):
    """Feature 2.7: avatar moments with ship-by dates."""

    def test_moments_from_triggers(self):
        from tables import brand_data
        monthly = brand_data('bombas').table('monthly')
        av = [{'name': 'Gift', 'triggers': ['Christmas']}, {'name': 'Wool', 'triggers': ['winter']}, {'name': 'Mom', 'triggers': ["Mother's Day"]}]
        x = api.builds.moments(av, monthly, '2026-09-27')
        labels = [r['label'] for r in x['rows']]
        self.assertEqual(labels, ['Winter', 'Holiday gifting'])
        hol = x['rows'][1]
        self.assertEqual(hol['starts'], '2026-12-01')
        self.assertEqual(hol['ad_by'], '2026-11-10')
        self.assertEqual(hol['email_by'], '2026-11-17')
        self.assertGreater(hol['sales_index_last_year'], 1)
        self.assertEqual(hol['action']['check_on'], '2026-11-10')

    def test_late_flag_and_rollover(self):
        x = api.builds.moments([{'name': 'Gift', 'triggers': ['holiday']}], [], '2026-11-20')
        r = x['rows'][0]
        self.assertTrue(r['late'])
        self.assertIsNone(r['sales_index_last_year'])


class Survey(TempBrain):
    """Feature 2.8: a survey whose questions close named gaps, with days to enough answers."""

    def test_survey(self):
        x = api.handle(Req(['overview']))['survey']
        self.assertEqual(x['questions'][0]['q'], 'Which of these sounds most like you?')
        self.assertIn('Hiking and outdoor buyer', x['questions'][0]['options'])
        self.assertFalse(any('(Reddit)' in o for o in x['questions'][0]['options']))
        opd = x['orders_per_day']
        self.assertAlmostEqual(x['days'], round(385 / (opd * 0.15), 1), places=0)
        self.assertEqual(x['action']['owner'], 'agent_drafts')
        self.assertTrue(x['action']['draft'].startswith('DRAFT'))
        self.assertTrue(all(q['closes'] for q in x['questions']))

    def test_no_orders_days_unavailable(self):
        x = api.builds.survey([], [], [], [], None)
        self.assertIsNone(x['days'])
        self.assertIn('unavailable', x['action']['draft'])


PATHS_FIXTURE = [
    {'kind': 'first_product', 'sku_group': 'ankle', 'first_buyers': 5000, 'repeat_180d': 0.38, 'value_180d': 96.0,
     'next': [{'sku_group': 'quarter', 'share': 0.31, 'median_days': 41}]},
    {'kind': 'first_product', 'sku_group': 'calf', 'first_buyers': 3000, 'repeat_180d': 0.24, 'value_180d': 80.0, 'next': []},
    {'kind': 'first_product', 'sku_group': 'slippers', 'first_buyers': 2000, 'repeat_180d': 0.14, 'value_180d': 70.0, 'next': []},
    {'kind': 'first_product', 'sku_group': 'tiny', 'first_buyers': 20, 'repeat_180d': 0.9, 'value_180d': 70.0, 'next': []},
    {'kind': 'order_gap', 'group': 'all', 'median_days': 62, 'n': 50000},
    {'kind': 'rfm', 'frequency': '3+', 'recency': '91-364', 'customers': 1300, 'prior_customers': 1000, 'revenue_share': 0.1},
]


class Paths(unittest.TestCase):
    """Feature 2.9: order-level rules read the customer_paths aggregate; unavailable without it."""

    def test_rules_on_fixture(self):
        x = api.builds.paths(PATHS_FIXTURE)
        prods = {p['sku_group']: p for p in x['products']}
        self.assertNotIn('tiny', prods)
        self.assertEqual(prods['ankle']['verdict'], 'gateway')
        self.assertEqual(prods['slippers']['verdict'], 'dead_end')
        self.assertEqual(prods['ankle']['next']['sku_group'], 'quarter')
        ids = {m['id'].split('.paths.')[1]: m for m in x['moves']}
        self.assertIn('gateway.ankle', ids)
        self.assertIn('day 36', ids['next.ankle']['title'])
        self.assertIn('day 93', ids['winback']['title'])
        self.assertIn('churning_hv', ids)
        for m in x['moves']:
            self.assertTrue(m['draft'].startswith('DRAFT'))

    def test_bombas_unavailable_not_zero(self):
        d = api._paths('bombas')
        self.assertFalse(d['available'])
        self.assertEqual(d['moves'], [])
        self.assertIn('customer_paths', d['shape'])


class Round2Rules(TempBrain):
    """Feature 2.10: round 2 rules fire and carry their drafted work."""

    def test_round2_rules(self):
        f = {x['id']: x for x in audit.run('bombas', RANK_WINDOW, self.tmp)}
        self.assertIn('02-customers-avatars.CUST-R12.copy_gap', f)
        self.assertIn('02-customers-avatars.CUST-R13.provisional_avatars', f)
        self.assertEqual(f['02-customers-avatars.CUST-R16.customer_paths']['status'], 'unavailable')
        self.assertIn('02-customers-avatars.CUST-R15.moment_winter', f)
        acts = {a['id']: a for a in api.rank('bombas', RANK_WINDOW)['actions']}
        self.assertEqual(acts['02-customers-avatars.CUST-R13.provisional_avatars']['capability']['id'], 'LIFE-C50')
        self.assertTrue(acts['02-customers-avatars.CUST-R13.provisional_avatars']['artefact']['draft'].startswith('DRAFT post-purchase survey'))
        self.assertTrue(acts['02-customers-avatars.CUST-R11.theme_price_value']['title'].startswith('Lift stars on price value'))

    def test_moment_rule_window(self):
        f = audit.run('bombas', {'ends_on': '2026-07-01', 'days': 28}, self.tmp)
        self.assertFalse([x for x in f if x['rule_id'] == 'CUST-R15'])


if __name__ == '__main__':
    unittest.main()
