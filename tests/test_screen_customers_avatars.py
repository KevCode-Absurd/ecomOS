"""Tests for screen 02-customers-avatars on the Bombas brain and simulated cohorts: audit.py in the
contract shape, the two insight rules, the repeat chart and the founder voice example write.
Writes go to a temp copy of app/brain, never the repo."""
import importlib.util
import json
import re
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
            if f['money_at_stake'] is None:
                self.assertTrue(f['money_reason'])
            else:
                self.assertTrue({'usd', 'formula', 'inputs', 'window'} <= set(f['money_at_stake']))
                self.assertGreater(f['money_at_stake']['usd'], 0)
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
        self.assertEqual({r['rule_id'] for r in audit.RULES}, {f'CUST-R{n:02d}' for n in range(1, 31)})


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


class PaidStake(unittest.TestCase):
    """Feature 6.10: money at stake on paid returning orders, against the brand's own 12-month median."""

    def tables(self):
        from tables import brand_data
        data = brand_data('bombas')
        return data.table('channels_monthly'), data.table('paid_media_monthly')

    def test_flat_share_gives_no_money_and_a_reason(self):
        channels, paid = self.tables()
        st = api.builds.paid_stake(channels, paid, '2026-08')
        self.assertIsNone(st['usd'])
        self.assertIn('median', st['reason'])

    def test_rise_above_median_is_priced_from_inputs(self):
        channels, paid = self.tables()
        channels = [dict(r) for r in channels]
        for r in channels:
            if r['month'] == '2026-08' and r['channel'] == 'paid_social':
                r['new_customer_orders'] = round(r['new_customer_orders'] * 0.8)
        st = api.builds.paid_stake(channels, paid, '2026-08')
        self.assertGreater(st['usd'], 0)
        i = st['inputs']
        redo = (i['paid_share_now'] - i['paid_share_median_12m']) * i['returning_orders'] * i['paid_spend'] / i['paid_orders']
        self.assertLess(abs(redo - st['usd']) / st['usd'], 0.01)
        self.assertEqual(set(st), {'usd', 'median', 'formula', 'inputs', 'window'})

    def test_missing_spend_is_null_not_zero(self):
        channels, _ = self.tables()
        channels = [dict(r) for r in channels]
        for r in channels:
            if r['month'] == '2026-08' and r['channel'] == 'paid_social':
                r['new_customer_orders'] = round(r['new_customer_orders'] * 0.8)
        st = api.builds.paid_stake(channels, None, '2026-08')
        self.assertIsNone(st['usd'])
        self.assertIn('spend', st['reason'])

    def test_short_history_has_no_baseline(self):
        channels, paid = self.tables()
        short = [r for r in channels if r['month'] >= '2026-06']
        self.assertIn('no baseline', api.builds.paid_stake(short, paid, '2026-08')['reason'])


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
        self.assertEqual(rules, {f'CUST-R{n:02d}' for n in range(1, 31) if n != 23})

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

    def test_top_actions_lead_with_money_then_the_compression_misread(self):
        from_server = rank_engine.rank('02-customers-avatars', 'bombas', RANK_WINDOW, use_override=True)
        self.assertEqual(from_server['source'], 'screen')
        acts = from_server['actions']
        self.assertEqual(acts[0]['rule_id'], 'CUST-R08')
        self.assertTrue(acts[0]['money_at_stake']['usd'] > 0)
        top_unpriced = next(a for a in acts if not a.get('money_at_stake'))
        self.assertEqual(top_unpriced['rule_id'], 'CUST-R05')
        self.assertIn('compression', top_unpriced['title'])

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
        self.assertTrue(acts['02-customers-avatars.CUST-R11.theme_delivery']['title'].startswith('Lift stars on delivery'))
        merged = next(a for a in acts.values() if '02-customers-avatars.CUST-R11.theme_price_value' in a['finding_ids'])
        self.assertEqual(merged['rule_id'], 'CUST-R04')

    def test_moment_rule_window(self):
        f = audit.run('bombas', {'ends_on': '2026-07-01', 'days': 28}, self.tmp)
        self.assertFalse([x for x in f if x['rule_id'] == 'CUST-R15'])


class Perception(TempBrain):
    """Feature 3.1: positioning words against buyer praise words, both ways."""

    def test_score_and_lists(self):
        x = api.handle(Req(['overview']))['perception']
        self.assertTrue(x['available'])
        self.assertAlmostEqual(x['score'], sum(t['in_positioning'] for t in x['theirs']) / len(x['theirs']), places=3)
        words = {t['word']: t for t in x['theirs']}
        self.assertFalse(words['soft']['in_positioning'])
        self.assertTrue(words['comfort']['in_positioning'])
        self.assertIn('performance', x['unechoed'])
        self.assertEqual(x['action']['steps'][-1]['who'], 'person')

    def test_founder_frame_changes_score(self):
        rows = self.section('positioning')
        for r in rows:
            if r['id'] == 'bombas.positioning.frame':
                r['value'] = r['value'] + ', soft socks that stay in place and never slip'
        self.write('positioning', rows)
        words = {t['word']: t for t in api.handle(Req(['overview']))['perception']['theirs']}
        self.assertTrue(words['soft']['in_positioning'])
        self.assertTrue(words['slip']['in_positioning'])


class ClaimsFire(TempBrain):
    """Feature 3.2: claims whose feature words sit in 1 and 2 star reviews."""

    def test_calf_claim_under_fire(self):
        x = api.handle(Req(['overview']))['claims_fire']
        rows = {r['id']: r for r in x['rows']}
        calf = rows['bombas.claims.calf_socks_benefit']
        self.assertEqual(calf['verdict'], 'under_fire')
        self.assertIn('stay', calf['words'])
        self.assertNotIn('calf', calf['words'])
        self.assertEqual(calf['action']['capability']['id'], 'BRN-C03')
        for r in x['rows']:
            self.assertEqual(r['verdict'] == 'under_fire', r['hits'] >= 3)
            self.assertEqual(r['action'] is not None, r['verdict'] == 'under_fire')

    def test_forbidden_claims_skipped(self):
        x = api.builds.claims_fire([{'id': 'b.claims.x', 'tier': 'forbidden', 'text': 'stay up heel'}], [], set(), audit.source_name)
        self.assertEqual(x['rows'], [])


class Lookalikes(TempBrain):
    """Feature 3.3: impostor pages from the Ad Library pull become a person-owned report."""

    def test_lookalike(self):
        x = api.handle(Req(['overview']))['lookalikes']
        self.assertEqual(len(x['rows']), 1)
        r = x['rows'][0]
        self.assertEqual(r['links_to'], 'sockscool.com')
        self.assertEqual(r['action']['owner'], 'person')
        self.assertEqual(r['action']['steps'][0]['who'], 'person')
        self.assertIn('sockscool.com', r['action']['draft'])

    def test_none(self):
        self.assertEqual(api.builds.lookalikes([], 'X')['rows'], [])


class OfferMap(TempBrain):
    """Feature 3.4: offers and policies against each avatar's doubts; the pushed offer read against them."""

    def test_offer_map(self):
        x = api.handle(Req(['overview']))['offer_map']
        rungs = audit.rungs(api._brain(Req(['overview'])))
        for r in x['rows']:
            for c in x['cols']:
                n = sum(1 for g in rungs if 'bombas.avatars.' + r['key'] in g['avatars'] and c['key'] in g['proof_ids'])
                self.assertEqual(x['cells'][r['key']][c['key']]['us'], n or None)
        self.assertEqual(x['push']['ads'], 21)
        self.assertIsNotNone(x['action'])
        self.assertIn('Daily Compression Wearer', x['bare'])
        self.assertNotIn('first order code confirmed', [c['label'] for c in x['cols']])


class Hierarchy(TempBrain):
    """Feature 3.5: a messaging hierarchy from buyer evidence, written on approval."""

    def test_hierarchy_and_approve(self):
        h = api.handle(Req(['overview']))['hierarchy']
        self.assertEqual(h['lead_theme'], 'comfort')
        self.assertEqual(len(h['proofs']), 3)
        fives = [p['five_star'] for p in h['proofs']]
        self.assertEqual(fives, sorted(fives, reverse=True))
        self.assertEqual(h['doubt']['id'], 'durability.3')
        self.assertFalse(h['approved'])
        code, res = api.handle(Req(['messaging', 'approve'], 'POST', body={}))
        self.assertEqual(code, 201)
        rec = next(r for r in self.section('positioning') if r['id'] == res['record'])
        self.assertEqual(rec['source']['type'], 'founder')
        self.assertTrue(api.handle(Req(['overview']))['hierarchy']['approved'])


class VoiceCheck(TempBrain):
    """Feature 3.6: a pasted line is checked against the rules; nothing is written."""

    def test_bad_line_fails(self):
        before = json.dumps(self.section('voice'))
        r = api.handle(Req(['voice', 'check'], 'POST', body={'text': 'The most comfortable socks — leverage our revolutionary tech.'}))
        self.assertEqual(r['verdict'], 'fail')
        st = {c['key']: c['status'] for c in r['checks']}
        self.assertEqual(st['dash'], 'fail')
        self.assertEqual(st['inflated'], 'fail')
        self.assertEqual(st['claim'], 'warn')
        self.assertEqual(json.dumps(self.section('voice')), before)

    def test_good_line_passes(self):
        r = api.handle(Req(['voice', 'check'], 'POST', body={'text': 'Soft socks that stay in place. Worth it after every wash.'}))
        self.assertEqual(r['verdict'], 'pass')

    def test_disliked_line_warns(self):
        api.handle(Req(['voice', 'examples'], 'POST', body={'kind': 'disliked', 'text': 'Crafted for the discerning modern sock lover.'}))
        r = api.handle(Req(['voice', 'check'], 'POST', body={'text': 'Crafted for the discerning modern sock lover.'}))
        self.assertEqual({c['key']: c['status'] for c in r['checks']}['disliked'], 'warn')


class Health(unittest.TestCase):
    """Feature 3.7: brand health line from store data; missing lines wait on connectors, never zero."""

    def test_health(self):
        from tables import brand_data
        monthly = brand_data('bombas').table('monthly')
        x = api.builds.health(monthly, [], '2026-09-27')
        self.assertTrue(x['available'])
        self.assertEqual(x['months'][-1], '2026-08')
        self.assertEqual(len(x['rows'][0]['values']), 12)
        self.assertTrue(all(v is None for v in x['rows'][1]['values']))
        self.assertEqual(len(x['missing']), 3)

    def test_ticket_rise_fires(self):
        from tables import brand_data
        monthly = [dict(r) for r in brand_data('bombas').table('monthly')]
        for r in monthly[-4:-1]:
            r['tickets'] = r['tickets'] * 2
        x = api.builds.health(monthly, [], '2026-09-27')
        self.assertIn('tickets', [m['key'] for m in x['moves']])


class OnePager(TempBrain):
    """Feature 3.8: a plain-text one-pager per avatar."""

    def test_one_pager(self):
        r = api.handle(Req(['avatar', 'daily_compression_wearer', 'brief']))
        t = r['text']
        for part in ('JOB:', 'DOUBTS, TOP FIRST:', 'NO PROOF YET', 'NEXT BUILD:', 'DO NOT SAY:'):
            self.assertIn(part, t)
        self.assertNotIn('\u2014', t)
        self.assertEqual(api.handle(Req(['avatar', 'nobody', 'brief']))[0], 404)
        self.assertEqual(api.handle(Req(['avatar', '../x', 'brief']))[0], 400)


class DoubtTiming(TempBrain):
    """Feature 3.9: doubt seasons from review dates, normalised by all complaints in the same months."""

    def test_timing(self):
        x = api.handle(Req(['overview']))['timing']
        for m in x['moves']:
            self.assertGreaterEqual(m['lift'], 1.5)
            self.assertTrue(m['draft'].startswith('DRAFT'))
        themes = [m['theme'] for m in x['moves']]
        self.assertIn('price_and_value', themes)
        for r in x['rows']:
            self.assertEqual(len(x['cells'][r['key']]), 12)

    def test_even_spread_has_no_season(self):
        recs, rungs = [], []
        for t in ('a', 'b'):
            ids = []
            for m in range(1, 13):
                rid = f'{t}{m}'
                recs.append({'id': rid, 'value': {'reviews': [{'star': 1, 'date': f'2025-{m:02d}-10', 'source': 'amazon'}]}})
                ids.append(rid)
            rungs.append({'theme': t, 'derived_from': ids})
        self.assertEqual(api.builds.doubt_timing(rungs, recs, '2026-09-27', audit.source_name)['moves'], [])


class Round3Rules(TempBrain):
    """Feature 3.10: round 3 rules fire with their drafted work; approval clears R22."""

    def test_round3(self):
        acts = {a['id']: a for a in api.rank('bombas', RANK_WINDOW)['actions']}
        look = acts['02-customers-avatars.CUST-R19.lookalike_109559148587404']
        self.assertEqual(look['owner'], 'person')
        self.assertEqual(look['rubric']['reputation'], 5)
        self.assertEqual(acts['02-customers-avatars.CUST-R18.claim_calf_socks_benefit']['rubric']['reputation'], 5)
        self.assertIn('02-customers-avatars.CUST-R20.pushed_offer', acts)
        self.assertIn('02-customers-avatars.CUST-R22.messaging_hierarchy', acts)
        api.handle(Req(['messaging', 'approve'], 'POST', body={}))
        ids = {f['id'] for f in audit.run('bombas', RANK_WINDOW, self.tmp)}
        self.assertNotIn('02-customers-avatars.CUST-R22.messaging_hierarchy', ids)


class DeskTabs(unittest.TestCase):
    """Feature 4.1: desk sections grouped into tabs; the plan stays first; every desk section sits in one tab."""

    def test_plan_first_and_every_section_in_a_tab(self):
        import re as _re
        html = (SCREEN / 'index.html').read_text(encoding='utf-8')
        js = (SCREEN / 'screen.js').read_text(encoding='utf-8')
        body = html[html.index('<div class="screen">'):]
        first = body.index('<section')
        self.assertTrue(body[first:first + 60].startswith('<section class="section" id="plan-wrap">'))
        self.assertLess(body.index('id="actions-wrap"'), body.index('id="desk-wrap"'))
        ids = _re.findall(r'<section class="section" id="([a-z-]+)"', body)
        above = {'plan-wrap', 'connect-wrap', 'wrong-wrap', 'actions-wrap', 'agenda-wrap', 'tests-wrap', 'decided-wrap', 'handoff-wrap', 'desk-wrap', 'audit-wrap'}
        desk_block = js[js.index('const DESK = ['):js.index('let deskTabs')]
        grouped = _re.findall(r"'([a-z]+-wrap)'", desk_block)
        self.assertEqual(sorted(set(ids) - above), sorted(grouped))
        self.assertEqual(len(grouped), len(set(grouped)))


class PlanByJob(TempBrain):
    """Feature 4.2: every action carries a job that matches a desk tab."""

    def test_jobs(self):
        js = (SCREEN / 'screen.js').read_text(encoding='utf-8')
        tabs = set(__import__('re').findall(r"key: '([a-z]+)', label", js[js.index('const DESK = ['):js.index('let deskTabs')]))
        acts = api.rank('bombas', RANK_WINDOW)['actions']
        self.assertTrue(acts)
        for a in acts:
            self.assertIn(a['job'], tabs)
        self.assertEqual(set(api.RULE_JOB), {r['rule_id'] for r in audit.RULES})


class ProposedTests(TempBrain):
    """Feature 4.3: proposed tests in the experiment registry shape, metric names from the contract."""

    def test_registry_shape(self):
        sys.path.insert(0, str(ROOT / 'app'))
        import metrics
        x = api.handle(Req(['tests']))
        keys = ['id', 'brand', 'hypothesis', 'source', 'idea_id', 'owner', 'metric', 'variant', 'audience', 'start', 'read_point', 'end',
                'status', 'result', 'decision', 'learnings_ref', 'retro', 'park', 'brain_refs']
        self.assertTrue(x['rows'])
        for r in x['rows']:
            for k in keys:
                self.assertIn(k, r)
            self.assertEqual(r['status'], 'proposed')
            self.assertIn(r['metric']['name'], metrics.METRICS)
            self.assertLessEqual(r['metric']['registered_on'], r['start'])
            self.assertIsNone(r['id'])
        self.assertIn('02-customers-avatars.test.guarantee_vs_discount', [r['proposal_key'] for r in x['rows']])


class Handoff(TempBrain):
    """Feature 4.4: hand-off packs for the four reading screens in events.md."""

    def test_packs(self):
        x = api.handle(Req(['handoff']))
        screens = [p['screen'] for p in x['packs']]
        self.assertEqual(screens, ['09-creative', '10-copy', '07-landing-pages-cro', '14-email-messaging', '15-customers-cx'])
        events = (ROOT / 'app' / 'contracts' / 'events.md').read_text(encoding='utf-8')
        row = next(l for l in events.splitlines() if l.startswith('| 02-customers-avatars'))
        for sc in screens[:4]:
            self.assertIn(sc, row)
        for p in x['packs']:
            self.assertTrue(p['items'])
            for i in p['items']:
                self.assertIn(i['kind'], rank_engine.ARTEFACT_KINDS)
                self.assertNotIn('(language only)', i['draft'])


class Naming(TempBrain):
    """Feature 4.5: the ad naming convention and its parser."""

    def test_parse_and_spec(self):
        n = api.handle(Req(['overview']))['naming']
        self.assertIn('durability', n['angles'])
        tags = audit.parse_ad_name(n['example'])
        self.assertEqual(tags['angle'], n['angles'][0])
        self.assertEqual(tags['avatar'], n['avatars'][0])
        self.assertEqual(tags['format'], 'video')
        self.assertEqual(audit.parse_ad_name('Summer promo 2'), {})
        acts = {a['id']: a for a in api.rank('bombas', RANK_WINDOW)['actions']}
        r03 = acts['02-customers-avatars.CUST-R03.ad_angles']
        self.assertEqual(r03['owner'], 'person')
        self.assertIn('AD NAMING CONVENTION', r03['artefact']['draft'])


class SplitCheck(TempBrain):
    """Feature 4.6: one avatar or two."""

    def test_split(self):
        x = {r['key']: r for r in api.handle(Req(['overview']))['split']['rows']}
        kid = x['parent_buying_for_kids']
        self.assertEqual(kid['verdict'], 'split')
        self.assertEqual(sorted(kid['big_lines']), ['calf', 'slippers'])
        self.assertEqual(kid['action']['owner'], 'agent_drafts')
        self.assertEqual(kid['action']['steps'][-1]['who'], 'person')
        self.assertEqual(x['daily_compression_wearer']['verdict'], 'focused')

    def test_shared_complaints_do_not_split(self):
        av = [{'id': 'b.avatars.x', 'key': 'x', 'name': 'X'}]
        x = api.builds.split_check(av, [], {'b.avatars.x': {'a': 5, 'b': 5}}, {'a': ['heel slip'], 'b': ['heel slip']})
        self.assertEqual(x['rows'][0]['verdict'], 'focused')


class AdVoice(TempBrain):
    """Feature 4.7: who our live ads speak to, against share of buyers."""

    def test_ad_voice(self):
        x = api.handle(Req(['overview']))['ad_voice']
        self.assertTrue(x['available'])
        rows = {r['key']: r for r in x['rows']}
        self.assertEqual(rows['everyday_comfort_seeker']['verdict'], 'over')
        self.assertEqual(rows['durability_disappointed_repeat_customer']['verdict'], 'silent')
        self.assertIsNotNone(rows['durability_disappointed_repeat_customer']['action'])
        matched = sum(r['ads'] for r in x['rows'])
        self.assertAlmostEqual(matched + sum(u['ads'] for u in x['unmatched']), x['total_ads'], places=0)

    def test_no_hook_read_unavailable(self):
        self.assertFalse(api.builds.ad_voice([], [])['available'])


class Decided(unittest.TestCase):
    """Feature 4.8: the decisions timeline reads the shared decisions route for this screen only."""

    def test_reads_shared_route(self):
        js = (SCREEN / 'screen.js').read_text(encoding='utf-8')
        self.assertIn("api('/api/decisions?screen=' + SLUG)", js)
        self.assertIn('d.screen === SLUG', js)
        self.assertIn('id="decided"', (SCREEN / 'index.html').read_text(encoding='utf-8'))


class Focus(TempBrain):
    """Feature 4.9: which avatar we build for next, from fixed weights."""

    def test_focus(self):
        x = api.handle(Req(['overview']))['focus']
        self.assertAlmostEqual(sum(x['weights'].values()), 1.0)
        for r in x['rows']:
            self.assertAlmostEqual(r['score'], round(100 * sum(x['weights'][k] * v for k, v in r['parts'].items()), 1), places=0)
            for v in r['parts'].values():
                self.assertTrue(0 <= v <= 1)
        self.assertEqual(x['rows'][0]['key'], 'durability_disappointed_repeat_customer')
        self.assertEqual([r['score'] for r in x['rows']], sorted((r['score'] for r in x['rows']), reverse=True))


class Round4Rules(TempBrain):
    """Feature 4.10: split and silent-avatar rules carry their drafted work and a job."""

    def test_round4(self):
        acts = {a['id']: a for a in api.rank('bombas', RANK_WINDOW)['actions']}
        split = acts['02-customers-avatars.CUST-R24.split_parent_buying_for_kids']
        self.assertEqual(split['job'], 'avatars')
        self.assertTrue(split['artefact']['draft'].startswith('DRAFT avatar split'))
        silent = [a for a in acts.values() if a['rule_id'] == 'CUST-R25']
        self.assertEqual(len(silent), 4)
        for a in silent:
            self.assertTrue(a['title'].startswith('Give '))
            self.assertEqual(rank_engine.validate_action(a), [])


class DepthRules(TempBrain):
    """Feature 5.1: depth.md section 3 rules checked against this screen."""

    def test_rule11_no_brand_facts_in_page_code(self):
        brain = api._brain(Req(['overview']))
        names = [n for n in audit.competitor_names(brain) if len(n) > 3] + [brain.brand, 'COMFORT20', 'sockscool']
        for f in ('screen.js', 'index.html'):
            text = (SCREEN / f).read_text(encoding='utf-8').lower()
            for n in names:
                self.assertNotIn(n.lower(), text, f'{n} in {f}')
            self.assertIsNone(__import__('re').search(r'\$\d', text), f'a dollar amount in {f}')

    def test_rule12_plain_words_in_our_writing(self):
        acts = api.rank('bombas', RANK_WINDOW)['actions']
        for a in acts:
            ours = [a['title'], a['why']] + [s['text'] for s in a['steps']]
            for t in ours:
                self.assertNotIn('\u2014', t, a['id'])
                for w in (' should ', ' consider ', ' leverage '):
                    self.assertNotIn(w, ' ' + t.lower() + ' ', a['id'])
                self.assertLessEqual(len(t.split()), 45, a['id'])
        html = (SCREEN / 'index.html').read_text(encoding='utf-8').lower()
        for w in (' should ', ' consider ', ' leverage ', '\u2014'):
            self.assertNotIn(w, html)

    def test_rule4_open_findings_show_numbers(self):
        for f in audit.run('bombas', RANK_WINDOW, self.tmp):
            if f['status'] == 'open':
                self.assertTrue(f['evidence'], f['id'])
                for e in f['evidence']:
                    self.assertTrue(e['metric'] and e['window'], f['id'])

    def test_rule8_simulated_rows_on_data_rules(self):
        data_rules = {r['rule_id'] for r in audit.RULES if any(not i.startswith('brain') for i in r['inputs'])}
        for f in audit.run('bombas', RANK_WINDOW, self.tmp):
            if f['rule_id'] in data_rules and f['status'] == 'open' and f['rule_id'] != 'CUST-R15':
                self.assertTrue(any(e['simulated'] for e in f['evidence']), f['id'])

    def test_rule7_unavailable_never_zero(self):
        d = api.handle(Req(['overview']))
        for o in d['orientation']:
            self.assertTrue(o['value'] is None or isinstance(o['value'], (int, float)))
        self.assertIsNone(api.builds.survey([], [], [], [], None)['days'])
        self.assertFalse(api._paths('bombas')['available'])
        for f in audit.run('bombas', RANK_WINDOW, self.tmp):
            if f['status'] == 'unavailable':
                self.assertEqual(f['evidence'], [])
                self.assertTrue(f['unavailable']['fix'])


class ReturnRisk(TempBrain):
    """Feature 5.2: return risk by avatar from the lines it buys; ticket reasons unavailable, never zero."""

    def test_return_risk(self):
        x = api.handle(Req(['overview']))['returns']
        self.assertEqual(x['rows'][0]['key'], 'daily_compression_wearer')
        self.assertEqual(x['rows'][0]['verdict'], 'high')
        self.assertIsNotNone(x['rows'][0]['action'])
        for r in x['rows']:
            self.assertEqual(r['verdict'] == 'high', r['ratio'] >= 1.25)
            self.assertEqual(r['action'] is not None, r['verdict'] == 'high')
        self.assertFalse(x['tickets']['available'])
        self.assertTrue(0 < x['refund_share_3m'] < 0.2)


class Macros(TempBrain):
    """Feature 5.3: support replies per doubt, never promising what is not on file."""

    def test_macros(self):
        x = api.handle(Req(['overview']))['macros']
        lad = {r['id']: r for r in api.handle(Req(['overview']))['ladders']['rows']}
        for m in x['rows']:
            self.assertIn('cx_macro', lad[m['id']]['uses'])
            if lad[m['id']]['proof']:
                self.assertEqual(m['status'], 'ready')
                self.assertIn(lad[m['id']]['proof'], m['draft'])
            else:
                self.assertNotEqual(m['status'], 'ready')
        self.assertEqual(sum(x['counts'].values()), len(x['rows']))


class CellDepth(TempBrain):
    """Feature 5.4: every coverage cell carries the rungs behind its count."""

    def test_cells_carry_rungs(self):
        c = api.handle(Req(['overview']))['coverage']
        for row in c['rows']:
            for col in c['cols']:
                cell = c['cells'][row['key']][col['key']]
                if cell['them'] is None:
                    self.assertEqual(cell['rungs'], [])
                    continue
                self.assertEqual(len(cell['rungs']), cell['them'])
                self.assertEqual(sum(1 for r in cell['rungs'] if r['proof']), cell['us'])
        self.assertIn('onCell: (cell, row, col) => cellPanel(cell, row, col)', (SCREEN / 'screen.js').read_text(encoding='utf-8'))


class MarketVoice(TempBrain):
    """Feature 5.5: avatars whose voice is mostly Amazon get listing work."""

    def test_market(self):
        x = api.handle(Req(['overview']))['marketplace']
        for r in x['rows']:
            self.assertEqual(r['verdict'] == 'marketplace', r['amazon_share'] >= 0.5)
            self.assertNotIn('Reddit', r['sources'])
            if r['action']:
                self.assertEqual(r['action']['kind'], 'listing_fix')
        self.assertEqual(x['rows'][0]['key'], 'in_store_single_pair_trier')


class Rechecks(TempBrain):
    """Feature 5.6: re-check calendar from record expiry dates."""

    def test_rechecks(self):
        x = api.handle(Req(['overview']))['rechecks']
        for r in x['rows']:
            if r['days_left'] is None:
                self.assertEqual(r['status'], 'no_date')
            else:
                self.assertEqual(r['status'], 'expired' if r['days_left'] < 0 else ('due' if r['days_left'] <= 30 else 'ok'))
        self.assertEqual(x['due'], sum(1 for r in x['rows'] if r['status'] in ('due', 'expired')))
        self.assertEqual(x['action']['check_on'], '2026-10-28')

    def test_later_date_expires(self):
        x = api.builds.rechecks([{'id': 'a', 'name': 'A', 'expires_at': '2026-10-28'}], [], '2026-11-01')
        self.assertEqual(x['rows'][0]['status'], 'expired')


class Strength(TempBrain):
    """Feature 5.7: the sample behind each desk block."""

    def test_strength(self):
        rows = api.handle(Req(['overview']))['strength']
        for r in rows:
            if r['n'] is None:
                self.assertEqual(r['verdict'], 'unavailable')
            else:
                self.assertEqual(r['verdict'], 'thin' if r['n'] < r['thin_at'] else 'strong')
        by = {r['block']: r for r in rows}
        self.assertEqual(by['Avatar cards']['verdict'], 'thin')
        self.assertEqual(by['Theme costs']['n'], 300)


class CardMeta(TempBrain):
    """Feature 5.8: each avatar card knows its rank, ad voice, returns, where it speaks and what we do not know."""

    def test_meta(self):
        d = api.handle(Req(['overview']))
        cards = {a['key']: a for a in d['avatars']}
        dur = cards['durability_disappointed_repeat_customer']['meta']
        self.assertEqual(dur['focus_rank'], 1)
        self.assertEqual(dur['ads'], 'silent')
        self.assertIn('5+ quotes', dur['unknown'])
        run = cards['reddit_runner']['meta']
        self.assertIsNone(run['focus_rank'])
        for a in d['avatars']:
            self.assertIn('unknown', a['meta'])


class PriceDoubts(TempBrain):
    """Feature 5.9: price-led avatars and the facts that answer them; pack prices unavailable, never zero."""

    def test_price(self):
        x = api.handle(Req(['overview']))['price']
        f = x['facts']
        self.assertEqual(f['pairs_to_free_shipping'], 6)
        self.assertIsNone(f['pack_prices'])
        for r in x['rows']:
            self.assertEqual(r['verdict'] == 'price_led', r['price_share'] >= 0.3)
            if r['action']:
                self.assertIn('unavailable', r['action']['draft'])
        self.assertEqual(x['rows'][0]['key'], 'in_store_single_pair_trier')


class Round5Rules(TempBrain):
    """Feature 5.10: round 5 rules fire with drafted work."""

    def test_round5(self):
        acts = {a['id']: a for a in api.rank('bombas', RANK_WINDOW)['actions']}
        ret = acts['02-customers-avatars.CUST-R26.returns_daily_compression_wearer']
        self.assertGreaterEqual(ret['rubric']['satisfaction'], 4)
        self.assertEqual(ret['artefact']['kind'], 'flow')
        self.assertIn('02-customers-avatars.CUST-R29.rechecks', acts)
        self.assertEqual(acts['02-customers-avatars.CUST-R30.thin_ads']['steps'][1]['who'], 'person')
        self.assertEqual(len([a for a in acts.values() if a['rule_id'] == 'CUST-R28']), 3)
        for a in acts.values():
            self.assertEqual(rank_engine.validate_action(a), [], a['id'])


class SecondBrand(unittest.TestCase):
    """Feature 6.1: plug and play. Every route renders for the sparse example brand, with no sample-brand fact and honest unavailable states."""

    def setUp(self):
        api.BRAIN_ROOT = None

    def req(self, path, method='GET', body=None):
        return api.handle(Req(path, method, query={'brand': ['example']}, body=body))

    def test_every_route_renders(self):
        d = self.req(['overview'])
        text = json.dumps(d).lower()
        self.assertNotIn('bombas', text)
        self.assertIn('example is the sample brand', d['simulated_note'].lower())
        self.assertFalse(d['cohorts']['available'])
        self.assertFalse(d['copy_gap']['available'])
        self.assertFalse(d['hierarchy']['available'])
        for o in d['orientation'][:3]:
            self.assertIsNone(o['value'])
        for path in (['handoff'], ['tests'], ['audit']):
            self.assertNotIn('bombas', json.dumps(self.req(path)).lower())
        acts = api.rank('example', RANK_WINDOW)['actions']
        self.assertNotIn('bombas', json.dumps(acts).lower())
        for a in acts:
            self.assertEqual(rank_engine.validate_action(a), [], a['id'])
        self.assertNotIn('02-customers-avatars.CUST-R22.messaging_hierarchy', {a['id'] for a in acts})

    def test_nothing_to_approve(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            shutil.copytree(BRAIN / 'example', tmp / 'example')
            api.BRAIN_ROOT = tmp
            self.assertEqual(self.req(['messaging', 'approve'], 'POST', {})[0], 409)
        finally:
            api.BRAIN_ROOT = None
            shutil.rmtree(tmp)


class MergedActions(TempBrain):
    """Feature 6.2: findings that ask for the same draft become one action with every finding id."""

    def test_merge(self):
        acts = api.rank('bombas', RANK_WINDOW)['actions']
        seen = [fid for a in acts for fid in a['finding_ids']]
        self.assertEqual(len(seen), len(set(seen)))
        drafts = [a['artefact']['draft'] for a in acts if a['status'] == 'open' and a['artefact']['draft']]
        self.assertEqual(len(drafts), len(set(drafts)))
        lead = next(a for a in acts if '02-customers-avatars.CUST-R11.theme_durability' in a['finding_ids'])
        self.assertIn('02-customers-avatars.CUST-R02.durability.3', lead['finding_ids'])
        self.assertIn('Also answers 1 more finding.', lead['why'])


class Agenda(TempBrain):
    """Feature 6.3: dated moves in the next 30 days, overdue first, only real dates."""

    def test_agenda(self):
        x = api.handle(Req(['agenda']))
        kinds = {i['kind'] for i in x['items']}
        self.assertIn('ads live', kinds)
        self.assertIn('re-check', kinds)
        dates = [i['date'] for i in x['items']]
        self.assertEqual(dates, sorted(dates))
        for i in x['items']:
            self.assertLessEqual(i['days'], 30)
            self.assertEqual(i['overdue'], i['days'] < 0)
        self.assertEqual(x['overdue'], sum(1 for i in x['items'] if i['overdue']))
        self.assertLess(len(x['items']), 25)


class Compare(TempBrain):
    """Feature 6.4: comparable rows per avatar."""

    def test_compare(self):
        c = api.handle(Req(['overview']))['compare']
        keys = [f['key'] for f in c['fields']]
        for row in c['rows'].values():
            for k in keys:
                self.assertIn(k, row)
        dur = c['rows']['durability_disappointed_repeat_customer']
        self.assertEqual(dur['build_rank'], 1)
        self.assertEqual(dur['proof'], 'no')
        self.assertNotIn('Reddit', dur['win_words'] or '')


class ScriptSyntax(unittest.TestCase):
    """screen.js parses: a syntax slip breaks the whole page."""

    def test_node_check(self):
        import shutil as _sh
        import subprocess
        node = _sh.which('node')
        if not node:
            self.skipTest('node not installed')
        r = subprocess.run([node, '--check', str(SCREEN / 'screen.js')], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)


class RungEvidence(TempBrain):
    """Feature 6.5: each rung carries its lines for the evidence panel."""

    def test_rung_rows_carry_lines(self):
        rows = {r['id']: r for r in api.handle(Req(['overview']))['ladders']['rows']}
        r = rows['durability.3']
        self.assertTrue(r['one_star_quotes'])
        self.assertLessEqual(len(r['one_star_quotes']), 8)
        self.assertIn('sources', r)
        self.assertIn('onRow: (r) => rungPanel(r)', (SCREEN / 'screen.js').read_text(encoding='utf-8'))


class SinceLastVisit(unittest.TestCase):
    """Feature 6.6: per-browser strip; storage wrapped so a blocked store never breaks the page."""

    def test_storage_guarded(self):
        js = (SCREEN / 'screen.js').read_text(encoding='utf-8')
        block = js[js.index('function renderSince'):js.index('// ---------- the monthly report')]
        self.assertEqual(block.count('localStorage'), 2)
        self.assertEqual(block.count('try {'), 2)


class PhoneWidth(unittest.TestCase):
    """Feature 6.7: phone rules present (checked in a 360 px browser for all 5 tabs: page width 360, nothing past the edge)."""

    def test_css(self):
        css = (SCREEN / 'screen.css').read_text(encoding='utf-8')
        self.assertIn('.screen .grid > * { min-width: 0; }', css)
        self.assertIn('@media (max-width: 720px)', css)
        self.assertIn('#desk .tabs { flex-wrap: wrap;', css)


class MonthlyReport(TempBrain):
    """Feature 6.8: a plain-words monthly report from the same builders."""

    def test_report(self):
        r = api.handle(Req(['report']))
        titles = [s['title'] for s in r['sections']]
        self.assertEqual(titles[0], 'The three moves to approve')
        self.assertIn('What we do not know yet', titles)
        self.assertNotIn('\u2014', r['text'])
        for w in (' should ', ' consider ', ' leverage '):
            self.assertNotIn(w, r['text'].lower())
        self.assertIn('simulated', r['text'])
        top = api.rank('bombas', RANK_WINDOW)['actions']
        self.assertTrue(r['sections'][0]['lines'][0].startswith('1. '))

    def test_second_brand_report(self):
        api.BRAIN_ROOT = None
        r = api.handle(Req(['report'], query={'brand': ['example']}))
        self.assertNotIn('bombas', r['text'].lower())


class Cache(TempBrain):
    """Feature 6.9: overview and rank are cached per brain version; a brain edit rebuilds them, and callers get copies."""

    def test_cache_invalidates_on_brain_change(self):
        a = api.handle(Req(['overview']))
        a['avatars'].clear()
        b = api.handle(Req(['overview']))
        self.assertTrue(b['avatars'])
        rows = self.section('objection_ladders')
        for lad in rows:
            if lad['id'] == 'bombas.objection_ladders.durability':
                lad['value']['rungs'][2]['proof_ids'] = ['bombas.policies.happiness_guarantee']
        self.write('objection_ladders', rows)
        c = api.handle(Req(['overview']))
        self.assertNotEqual(a['version'], c['version'])
        self.assertEqual({r['id']: r['verdict'] for r in c['ladders']['rows']}['durability.3'] != 'answer', True)
        r1 = api.rank('bombas', RANK_WINDOW)
        r1['actions'].clear()
        self.assertTrue(api.rank('bombas', RANK_WINDOW)['actions'])


if __name__ == '__main__':
    unittest.main()


class SizedStop(unittest.TestCase):
    """Feature 7.1: depth rule 5. Every action that moves money or traffic carries a size, a stop rule with a count, and a check date."""

    def test_every_money_action_is_sized_with_a_stop(self):
        acts = api.rank('bombas', {'ends_on': '2026-09-27', 'days': 28})['actions']
        moving = [a for a in acts if a['artefact']['kind'] in api.builds.MOVES_MONEY]
        self.assertGreater(len(moving), 20)
        for a in moving:
            self.assertTrue(a['size'] and a['size']['text'], a['id'])
            self.assertRegex(a['stop_rule'] or '', r'\d', a['id'])
            self.assertFalse(a['stop_rule'].startswith('Stop if'), a['id'])
            self.assertTrue(a['check_on'], a['id'])

    def test_other_kinds_get_no_size(self):
        ss = api.builds.size_stop('research_note', [{'metric': 'quotes', 'value': 4, 'unit': 'n'}], None, '2026-10-04')
        self.assertEqual(ss, {'size': None, 'stop_rule': None})

    def test_money_leads_the_size_and_missing_numbers_say_unavailable(self):
        ss = api.builds.size_stop('offer', [], {'usd': 1200}, None)
        self.assertEqual(ss['size'], {'text': '$1,200 at stake; size unavailable', 'usd': 1200})
        ss = api.builds.size_stop('copy', [{'metric': 'one_star_mentions', 'value': None, 'unit': 'n'}], None, None)
        self.assertEqual(ss['size']['text'], 'size unavailable')


class ReadsInOnePass(unittest.TestCase):
    """Feature 7.2: depth rule 10. Every desk block has a question or imperative heading, a rule line, a window and a caveat."""

    DIR = ROOT / 'app' / 'screens' / '02-customers-avatars'
    VERBS = ('Fix', 'Move', 'Stop', 'Build', 'Answer', 'Read', 'Pick', 'Give', 'Run', 'Show', 'Cut', 'Find')

    def desk_ids(self):
        js = (self.DIR / 'screen.js').read_text(encoding='utf-8')
        block = js[js.index('const DESK = ['):js.index('let deskTabs')]
        return re.findall(r"'([a-z]+-wrap)'", block)

    def test_every_desk_block_has_notes(self):
        ids = self.desk_ids()
        self.assertGreater(len(ids), 30)
        self.assertEqual(set(ids), set(api.builds.BLOCKS))

    def test_headings_are_questions_or_imperatives_with_a_rule_line(self):
        html = (self.DIR / 'index.html').read_text(encoding='utf-8')
        for sid in self.desk_ids():
            m = re.search(r'<section[^>]*id="' + sid + r'"[^>]*>\s*<div class="sec-head"><h2>([^<]+)</h2>(.*)', html)
            self.assertIsNotNone(m, sid)
            h = m.group(1)
            self.assertTrue(h.endswith('?') or h.startswith(self.VERBS), h)
            self.assertIn('class="sub"', m.group(2), sid)

    def test_notes_carry_window_and_a_short_caveat(self):
        api.BRAIN_ROOT = None
        for brand in ('bombas', 'example'):
            d = api.handle(Req(['overview'], query={'brand': [brand]}))
            self.assertEqual(set(d['blocks']), set(api.builds.BLOCKS))
            for sid, b in d['blocks'].items():
                self.assertTrue(b['window'], sid)
                for sent in re.split(r'(?<=\.) ', b['caveat']):
                    self.assertLess(len(sent.split()), 20, sent)
                self.assertNotRegex(b['caveat'], r'\b(should|consider|leverage)\b|—')
        d = api.handle(Req(['overview']))
        self.assertIn('simulated', d['blocks']['cohort-wrap']['window'])
        self.assertTrue(d['blocks']['ladders-wrap']['caveat'].startswith('Based on '))


class GapsNotTotals(unittest.TestCase):
    """Feature 7.3: depth rule 9. Every desk block shows a never-tried cell, a cross-source check or a competitor position."""

    def test_every_block_names_a_gap(self):
        for brand in ('bombas', 'example'):
            d = api.handle(Req(['overview'], query={'brand': [brand]}))
            for sid, b in d['blocks'].items():
                g = b['gap']
                self.assertIn(g['kind'], api.builds.GAP_KINDS, sid)
                self.assertTrue(g['text'].endswith('.'), sid)
                self.assertNotRegex(g['text'], r'\b(should|consider|leverage)\b|—')
            if brand == 'bombas':
                self.assertEqual([s for s, b in d['blocks'].items() if b['gap']['kind'] == 'unavailable'], ['paths-wrap'])

    def test_counts_match_the_blocks(self):
        d = api.handle(Req(['overview']))
        g = {s: b['gap']['text'] for s, b in d['blocks'].items()}
        under = sum(1 for r in d['claims_fire']['rows'] if r['verdict'] == 'under_fire')
        self.assertIn(f"{under} of {len(d['claims_fire']['rows'])} under fire", g['claims-wrap'])
        silent = [r for r in d['ad_voice']['rows'] if r['verdict'] == 'silent']
        self.assertTrue(g['voiceads-wrap'].startswith(f"{len(silent)} avatar"))
        self.assertIn(f"{d['ladders']['counts']['answer']} rung", g['ladders-wrap'])

    def test_page_draws_the_gap(self):
        js = (ROOT / 'app' / 'screens' / '02-customers-avatars' / 'screen.js').read_text(encoding='utf-8')
        self.assertIn("'block-gap gap-' + b.gap.kind", js)


class FounderCanDisagree(unittest.TestCase):
    """Feature 7.4: depth rule 14. A decision shows on its action with the date; "Not now" snoozes it 14 days, then it comes back."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.log = self.tmp / 'decisions.json'
        api.DECISIONS_PATH = self.log
        self.acts = api.rank('bombas', RANK_WINDOW)['actions']

    def tearDown(self):
        api.DECISIONS_PATH = None
        shutil.rmtree(self.tmp, ignore_errors=True)

    def write(self, rows):
        self.log.write_text(json.dumps(rows), encoding='utf-8')

    def test_not_now_snoozes_with_the_day_it_comes_back(self):
        a = self.acts[0]
        self.write([{'finding_id': a['id'], 'choice': 'not_now', 'time': RANK_WINDOW['ends_on'] + 'T10:00:00Z', 'screen': '02-customers-avatars'}])
        got = {x['id']: x for x in api.rank('bombas', RANK_WINDOW)['actions']}[a['id']]
        self.assertEqual(got['status'], 'snoozed')
        back = (api.dt.date.fromisoformat(RANK_WINDOW['ends_on']) + api.dt.timedelta(days=14)).isoformat()
        self.assertEqual(got['decision']['back_on'], back)
        later = dict(RANK_WINDOW, ends_on=back)
        again = {x['id']: x for x in api.rank('bombas', later)['actions']}.get(a['id'])
        if again:
            self.assertNotEqual(again['status'], 'snoozed')

    def test_decision_on_a_merged_finding_shows_on_the_lead(self):
        merged = next(x for x in self.acts if len(x['finding_ids']) > 1)
        self.write([{'finding_id': merged['finding_ids'][-1], 'choice': 'agent', 'time': '2026-09-27T09:00:00Z'}])
        got = {x['id']: x for x in api.rank('bombas', RANK_WINDOW)['actions']}[merged['id']]
        self.assertEqual(got['decision']['choice'], 'agent')
        self.assertNotEqual(got['status'], 'snoozed')

    def test_no_log_leaves_actions_open_and_the_cache_clean(self):
        self.assertTrue(all(x['decision'] is None for x in self.acts))
        self.write([{'finding_id': self.acts[0]['id'], 'choice': 'not_now', 'time': '2026-09-27T09:00:00Z'}])
        api.rank('bombas', RANK_WINDOW)
        self.log.unlink()
        self.assertIsNone(api.rank('bombas', RANK_WINDOW)['actions'][0]['decision'])

    def test_report_and_agenda_skip_snoozed(self):
        a = self.acts[0]
        self.write([{'finding_id': a['id'], 'choice': 'not_now', 'time': RANK_WINDOW['ends_on'] + 'T10:00:00Z'}])
        rep = api.handle(Req(['report']))
        self.assertNotIn(a['title'], json.dumps(rep))


class RetentionStake(unittest.TestCase):
    """Feature 7.5: money on the retention cliff and the age break, against the brand's own cohort history."""

    def grid(self, cohorts=None):
        from tables import brand_data
        data = brand_data('bombas')
        return api.builds.cohort_grid(cohorts if cohorts is not None else data.table('cohorts'), data.table('monthly'), '2026-09-27', [])

    def test_cliff_stake_redoes_from_inputs_and_names_the_season(self):
        st = self.grid()['calendar_break']['stake']
        self.assertGreater(st['usd'], 0)
        self.assertAlmostEqual(st['usd'], st['inputs']['lost_orders'] * st['inputs']['aov_month'], delta=st['inputs']['aov_month'])
        self.assertIn('season', st['note'])

    def test_age_stake_redoes_from_inputs(self):
        st = self.grid()['age_break']['stake']
        i = st['inputs']
        redo = i['share_month_k'] * (i['fall_at_break'] - i['median_fall_other_ages']) * i['median_cohort_size'] * i['median_aov_12m']
        self.assertLess(abs(redo - st['usd']) / st['usd'], 0.01)

    def test_findings_carry_the_stake_in_the_contract_shape(self):
        fs = {f['rule_id']: f for f in api.audit.run('bombas', RANK_WINDOW, api.BRAIN_ROOT)}
        for rid in ('CUST-R08', 'CUST-R09'):
            m = fs[rid]['money_at_stake']
            self.assertTrue({'usd', 'formula', 'inputs', 'window'} <= set(m), rid)
            self.assertIsNone(fs[rid]['money_reason'])
        self.assertIsNone(fs['CUST-R07']['money_at_stake'])
        self.assertIn('median', fs['CUST-R07']['money_reason'])

    def test_short_history_has_no_baseline(self):
        self.assertEqual(api.builds._age_stake([], [0.1] * 12, [(0.3, 2), (0.1, 3)], 2, 0.3, {'2026-08': 70})['usd'], None)
