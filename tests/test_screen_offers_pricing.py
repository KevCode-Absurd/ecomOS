"""Screen 04-offers-pricing: audit rules, API shape, and the two metrics it added, on Bombas simulated data.

The metric tests use the server's sample brand (always present). The Bombas tests that need order rows skip
when app/data/brands/bombas/data.sqlite has not been built.
"""
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / 'app' / 'screens' / '04-offers-pricing'
BOMBAS_DB = ROOT / 'app' / 'data' / 'brands' / 'bombas' / 'data.sqlite'
AUDIT_KEYS = ['id', 'screen', 'rule_id', 'severity', 'entity', 'evidence', 'sentence', 'capability', 'money_at_stake',
              'confidence', 'brain_refs', 'first_seen', 'last_seen', 'status', 'unavailable']
EVIDENCE_KEYS = {'metric', 'value', 'unit', 'window', 'ends_on', 'freshness_days', 'baseline', 'baseline_kind',
                 'source', 'simulated'}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


api = load('offers_pricing_api_test', SCREEN / 'api.py')
audit = api.audit


class Req:
    def __init__(self, path, brand='bombas', method='GET'):
        self.path, self.method, self.data, self._brand = path, method, None, brand

    def arg(self, name, default=None):
        return self._brand if name == 'brand' else default


class MetricsTest(unittest.TestCase):
    def setUp(self):
        sys.path.insert(0, str(ROOT / 'app'))
        import server
        self.data = server.Data()
        self.m = audit.metrics()

    def test_order_value_distribution_sums(self):
        r = self.m.compute('order_value_distribution', self.data, window='28d')
        self.assertFalse(r['unavailable'], r.get('reason'))
        self.assertEqual(sum(g['orders'] for g in r['groups']), r['value'])
        self.assertAlmostEqual(sum(g['share'] for g in r['groups']), 1, places=4)
        for g in r['groups']:
            self.assertEqual(g['to'] - g['from'], 5)
            self.assertLessEqual(g['paid_shipping_orders'], g['orders'])

    def test_returns_by_reason(self):
        r = self.m.compute('returns_by_reason', self.data, window='28d')
        self.assertFalse(r['unavailable'], r.get('reason'))
        self.assertEqual(sum(g['returns'] for g in r['groups']), r['value'])
        self.assertNotIn('carrier_returned', [g['reason'] for g in r['groups']])

    def test_window_outside_data_is_unavailable(self):
        r = self.m.compute('order_value_distribution', self.data, window='28d', end='2001-01-31')
        self.assertTrue(r['unavailable'])
        self.assertIsNone(r['value'])


class LadderTest(unittest.TestCase):
    def test_proofless(self):
        self.assertTrue(audit.is_proofless(None))
        self.assertTrue(audit.is_proofless('no public proof; open question for the founder'))
        self.assertFalse(audit.is_proofless('The Happiness Guarantee'))

    def test_band_share(self):
        groups = [{'from': 70, 'to': 75, 'share': 0.1}, {'from': 75, 'to': 80, 'share': 0.2}, {'from': 80, 'to': 85, 'share': 0.3}]
        self.assertEqual(audit.band_share(groups, 75, 85), 0.5)
        self.assertEqual(audit.band_share(groups, 65, 75), 0.1)


class BombasTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.findings = audit.run('bombas')

    def test_contract_shape(self):
        self.assertTrue(self.findings)
        for f in self.findings:
            self.assertEqual(list(f)[:len(AUDIT_KEYS)], AUDIT_KEYS)
            self.assertEqual(f['screen'], '04-offers-pricing')
            self.assertEqual(f['id'], f'04-offers-pricing.{f["rule_id"]}.{f["entity"]["id"]}')
            self.assertIn(f['severity'], ('critical', 'high', 'medium', 'low'))
            for e in f['evidence']:
                self.assertEqual(set(e), EVIDENCE_KEYS)
                self.assertTrue(e['simulated'])
            if f['money_at_stake'] is None:
                self.assertTrue(f['money_reason'])
            if f['status'] == 'unavailable':
                self.assertTrue(f['unavailable']['fix'])
            self.assertLess(len(f['sentence'].split()), 41)
            self.assertNotIn('—', f['sentence'])
        order = [audit.SEVERITY_ORDER[f['severity']] for f in self.findings]
        self.assertEqual(order, sorted(order))

    def test_unanswered_rungs(self):
        rungs = [f for f in self.findings if f['rule_id'] == 'OFFER-R04']
        self.assertTrue(rungs)
        for f in rungs:
            self.assertEqual(f['entity']['type'], 'ladder_rung')
            self.assertTrue(f['entity']['id'].endswith('.deal_breaker'))
            self.assertTrue(f['brain_refs'][0].startswith('bombas.objection_ladders.'))
        answered = {r['theme'] for r in audit.ladder_rungs(audit.Reader(None, 'bombas', audit.last_full_day(None, 'bombas')))
                    if r['proof']}
        self.assertFalse({f['entity']['id'].split('.')[0] for f in rungs} & answered)

    def test_sku_margin_joins_finance_keys(self):
        # S2.3c: products use the finance_inputs SKU keys, so every store SKU has a landed cost and R03 stays quiet
        matched, skus, cogs = audit.sku_join(audit.Reader(None, 'bombas', audit.last_full_day(None, 'bombas')))
        self.assertTrue(skus)
        self.assertEqual(matched, skus)
        self.assertFalse([f for f in self.findings if f['rule_id'] == 'OFFER-R03'])

    def test_deterministic(self):
        self.assertEqual(audit.run('bombas'), self.findings)

    @unittest.skipUnless(BOMBAS_DB.is_file(), 'bombas data.sqlite not built')
    def test_threshold_finding_has_money(self):
        f = next(f for f in self.findings if f['rule_id'] == 'OFFER-R01')
        self.assertEqual(f['status'], 'open')
        m = f['money_at_stake']
        i = m['inputs']
        self.assertAlmostEqual(m['usd'], round(round(i['orders_28d'] * i['share_threshold_to_break_even']) * i['average_label'], 2))
        be = next(e for e in f['evidence'] if e['metric'] == 'free_shipping_threshold_breakeven')
        self.assertGreater(be['value'], be['baseline'])

    @unittest.skipUnless(BOMBAS_DB.is_file(), 'bombas data.sqlite not built')
    def test_overview(self):
        code_or_body = api.handle(Req(['overview']))
        d = code_or_body
        self.assertTrue(d['brand']['simulated'])
        self.assertEqual(len(d['chart']['labels']), 24)
        th = d['threshold']
        self.assertFalse(th['unavailable'])
        self.assertEqual(th['suggested'] % 5, 0)
        self.assertGreaterEqual(th['suggested'], th['break_even'])
        self.assertTrue(all(s['source'] for s in d['stack']))
        singles = [r for r in d['ladder']['rows'] if r['pack'] == 1]
        self.assertTrue(all(r['drop_vs_single'] is None for r in singles))

    def test_read_only_and_bad_brand(self):
        self.assertEqual(api.handle(Req(['overview'], method='POST'))[0], 405)
        self.assertEqual(api.handle(Req(['overview'], brand='../x'))[0], 400)
        self.assertEqual(api.handle(Req(['nope']))[0], 404)

    def test_sample_brand_degrades(self):
        req = Req(['overview'], brand='sample')
        sys.path.insert(0, str(ROOT / 'app'))
        import server
        req.data = server.Data()
        d = api.handle(req)
        self.assertIsNone(d['threshold']['threshold'])
        self.assertTrue(d['threshold']['reason'])
        rank_mod = load('ecomos_rank', ROOT / 'app' / 'rank.py')
        for a in d['plan']:
            self.assertEqual(rank_mod.validate_action(a), [])   # same structure for a brand with no folder
        o = {x['label']: x for x in d['orientation']}
        self.assertIsNone(o['free shipping from']['value'])


class PlanFirstTest(unittest.TestCase):
    """Round 1 feature 1: the plan is the top of the page, every finding ends in an action (depth.md rules 1 to 3, 7, 11)."""

    @classmethod
    def setUpClass(cls):
        cls.rank_mod = load('ecomos_rank', ROOT / 'app' / 'rank.py')
        cls.ranked = api.rank('bombas')
        cls.findings = audit.run('bombas')
        cls.overview = api.handle(Req(['overview']))

    def test_every_action_valid(self):
        self.assertTrue(self.ranked['actions'])
        for a in self.ranked['actions']:
            self.assertEqual(self.rank_mod.validate_action(a), [], a['id'])
            self.assertIn(a['owner'], ('agent', 'agent_drafts', 'person'))
            self.assertTrue(2 <= len(a['steps']) <= 8)
            self.assertTrue(all(s['who'] in ('agent', 'person') for s in a['steps']))
            self.assertIn(a['artefact']['kind'], self.rank_mod.ARTEFACT_KINDS)
            self.assertNotIn('—', a['title'] + a['why'])

    def test_every_finding_maps_to_an_action(self):
        covered = {fid for a in self.ranked['actions'] for fid in a['finding_ids']}
        for f in self.findings:
            if f['status'] in ('open', 'unavailable'):
                self.assertIn(f['id'], covered)
        for a in self.ranked['actions']:
            if a['status'] == 'unavailable':
                self.assertEqual(a['owner'], 'person')
                self.assertEqual(a['artefact']['kind'], 'connector_setup')

    def test_rank_route_uses_the_override_and_is_deterministic(self):
        out = self.rank_mod.rank('04-offers-pricing', 'bombas', self.rank_mod.default_window(28, '2026-09-27'))
        self.assertEqual(out['source'], 'screen')
        again = api.rank('bombas')
        self.assertEqual([a['id'] for a in again['actions']], [a['id'] for a in self.ranked['actions']])
        self.assertEqual([a['id'] for a in out['actions']], [a['id'] for a in self.ranked['actions']])

    def test_threshold_fires_from_aggregates(self):
        f = next(f for f in self.findings if f['rule_id'] == 'OFFER-R01')
        self.assertEqual(f['status'], 'open')
        be = next(e for e in f['evidence'] if e['metric'] == 'free_shipping_threshold_breakeven')
        self.assertGreater(be['value'], be['baseline'])
        a = next(a for a in self.ranked['actions'] if a['rule_id'] == 'OFFER-R01')
        self.assertEqual(a['artefact']['kind'], 'test_brief')
        self.assertTrue(a['artefact']['draft'] and a['stop_rule'] and a['win_rule'] and a['check_on'])
        if f['money_at_stake'] is None:
            self.assertTrue(f['money_reason'])

    def test_overview_puts_the_plan_first(self):
        d = self.overview
        self.assertNotIn('tiles', d)
        self.assertNotIn('insights', d)
        self.assertEqual([a['id'] for a in d['plan']], [a['id'] for a in self.ranked['actions']])
        self.assertTrue(3 <= len(d['orientation']) <= 6)
        for o in d['orientation']:
            if o['value'] is None:
                self.assertTrue(o['title'])  # unavailable carries its reason
        html = (SCREEN / 'index.html').read_text(encoding='utf-8')
        body = html[html.index('<body'):]
        self.assertLess(body.index('id="plan"'), body.index('id="wrong"'))
        self.assertLess(body.index('id="wrong"'), body.index('id="desk"'))
        self.assertLess(body.index('id="desk"'), body.index('id="audit"'))

    def test_no_hex_colours_or_brand_facts_in_js(self):
        import re
        js = (SCREEN / 'screen.js').read_text(encoding='utf-8')
        css = (SCREEN / 'screen.css').read_text(encoding='utf-8')
        self.assertFalse(re.search(r'#[0-9a-fA-F]{3,6}\b', css))
        self.assertFalse(re.search(r"'#[0-9a-fA-F]{3,6}'", js))
        for fact in ('Bombas', 'COMFORT20', '$75', 'Happiness'):
            self.assertNotIn(fact, js)
        self.assertNotIn('—', js)


class ObjectionOfferTest(unittest.TestCase):
    """Round 1 feature 2: every deal-breaker rung without proof becomes an offer or proof spec with its cost."""

    @classmethod
    def setUpClass(cls):
        cls.out = api.actions.rank('bombas')
        cls.rows = cls.out['objections']

    def test_every_open_rung_has_a_priced_spec_and_an_action(self):
        open_rows = [r for r in self.rows if not r['answered']]
        self.assertTrue(open_rows)
        acts = {a['entity']['id']: a for a in self.out['actions'] if a['rule_id'] == 'OFFER-R04'}
        for r in open_rows:
            if r['one_star'] == 0:
                continue
            a = acts[r['theme_key'] + '.deal_breaker']
            self.assertIn(a['artefact']['kind'], ('offer', 'page_section', 'listing_fix'))
            self.assertIn(r['spec'], a['artefact']['draft'])   # proof lines and margin checks may be added around it
            self.assertIn(r['doubt'], r['spec'])
            self.assertTrue(a['win_rule'] and a['stop_rule'] and a['check_on'])
            if r['claim'] != 'none' and r['cost_per_claim'] is not None:
                self.assertAlmostEqual(r['cost_per_claim'], round(sum(p['value'] for p in r['cost_parts']), 2))
            if r['cost_per_1000_orders'] is not None:
                self.assertAlmostEqual(r['cost_per_1000_orders'], round(r['cost_per_claim'] * r['planned_rate'] * 1000, 2))
                self.assertTrue(r['rate_source'].startswith('bombas.'))

    def test_severity_and_rubric_override(self):
        for f in self.out['findings']:
            if f['rule_id'] == 'OFFER-R04' and f['status'] == 'open':
                one = next(e['value'] for e in f['evidence'] if e['metric'] == 'one_star_mentions')
                if one >= audit.TOP_DOUBT:
                    self.assertEqual(f['severity'], 'high')
        for a in self.out['actions']:
            if a['rule_id'] == 'OFFER-R04':
                self.assertGreaterEqual(a['rubric']['reputation'], 4)
                self.assertGreaterEqual(a['rubric']['satisfaction'], 4)

    def test_returns_fixture_is_labelled(self):
        r = self.out['returns']
        if r['unavailable']:
            self.assertTrue(r['fixture'])
            self.assertIn('Fixture', r['fixture_note'])
            self.assertTrue(r['reason'])
        else:
            self.assertFalse(r['fixture'])
        for f in self.out['findings']:
            if f['rule_id'] == 'OFFER-R04' and f['money_at_stake'] is None:
                self.assertTrue(f['money_reason'])


class ThresholdTest(unittest.TestCase):
    """Round 1 feature 3: the free shipping line, its break-even trend, what a different line must achieve."""

    @classmethod
    def setUpClass(cls):
        cls.rd = audit.Reader(None, 'bombas', audit.last_full_day(None, 'bombas'))
        cls.th = api.threshold(cls.rd)

    def test_scenarios_arithmetic(self):
        th = self.th
        self.assertFalse(th['unavailable'])
        rate = th['shipping_listed']
        cur = [r for r in th['scenarios'] if r['current']]
        self.assertEqual(len(cur), 1)
        for r in th['scenarios']:
            if r['current'] or r.get('limit') is None:
                continue
            cf = r['contribution_free']
            want = rate / (rate + cf) if r['kind'] == 'raise' else rate / cf
            self.assertAlmostEqual(r['limit'], round(want, 4))
            self.assertEqual(r['kind'], 'raise' if r['threshold'] > th['threshold'] else 'lower')
            self.assertIn('percent', r['text'])
        self.assertIn(th['suggested'], [r['threshold'] for r in th['scenarios']])

    def test_trend_and_gap(self):
        th = self.th
        self.assertEqual(len(th['trend']), 12)
        self.assertAlmostEqual(th['gap'], round(th['break_even'] - th['threshold'], 2))
        for r in th['trend']:
            self.assertEqual(r['threshold'], th['threshold'])

    def test_fixture_labelled_and_no_shares_from_it(self):
        th = self.th
        if th['fixture']:
            self.assertIn('Fixture', th['fixture_note'])
            self.assertIsNone(th['share_just_under'])
            self.assertIsNone(th['share_below'])
            self.assertTrue(th['distribution_unavailable'])
            for r in th['scenarios']:
                self.assertIsNone(r.get('band_orders_28d'))

    def test_pull_rule_unavailable_without_orders_and_stale_rule_threshold(self):
        fs = {f['rule_id']: f for f in audit.run('bombas')}
        if self.th['fixture']:
            self.assertEqual(fs['OFFER-R06']['status'], 'unavailable')
        now = audit.break_even(self.rd, self.rd.ends_on)['value']
        then = audit.break_even(self.rd, self.rd.ends_on - audit.timedelta(days=364))['value']
        self.assertEqual('OFFER-R05' in fs, abs(now / then - 1) > audit.STALE_MOVE)

    def test_test_brief_carries_the_walk_away_limit(self):
        a = next(a for a in api.actions.rank('bombas')['actions'] if a['rule_id'] == 'OFFER-R01')
        self.assertIn('walk away', a['artefact']['draft'])


class PackLadderTest(unittest.TestCase):
    """Round 1 feature 4: the pack ladder verdict per line and its arithmetic, merged into one action per verdict."""

    @classmethod
    def setUpClass(cls):
        cls.rd = audit.Reader(None, 'bombas', audit.last_full_day(None, 'bombas'))
        cls.lad, cls.rows = audit.ladder_moves(cls.rd)
        cls.pb = audit._playbook()
        cls.out = api.actions.rank('bombas')

    def test_trade_up_arithmetic(self):
        for r in self.rows:
            if r['verdict'] in ('push', 'deepen'):
                self.assertTrue(r['saving'] < self.pb.MIN_SAVING or r['single_share'] > self.pb.SINGLE_SHARE_PUSH)
                self.assertAlmostEqual(r['test_price'], round(r['single_per_item'] * r['pack'] * (1 - self.pb.TARGET_SAVING), 2))
                self.assertAlmostEqual(r['give_away_12m'], round(max(r['test_cut'], 0) * (r['packs'] - r['single_packs']), 2))
                if r['trade_up_needed'] is not None:
                    self.assertEqual(r['verdict'] == 'deepen', r['trade_up_needed'] <= self.pb.VIABLE_TRADE_UP)
            if r['verdict'] == 'add':
                self.assertIn(r['category'], self.pb.REPEAT_CATEGORIES)
                self.assertAlmostEqual(r['new_margin'], round(r['new_price'] - r['new_cogs'], 2))

    def test_one_action_per_verdict_covers_every_ladder_finding(self):
        fids = {f['id'] for f in self.out['findings'] if f['rule_id'] in ('OFFER-R07', 'OFFER-R09') and f['status'] == 'open'}
        acts = [a for a in self.out['actions'] if a['rule_id'] in ('OFFER-R07', 'OFFER-R09')]
        self.assertEqual(len({a['id'] for a in acts}), len(acts))
        covered = {fid for a in acts for fid in a['finding_ids']}
        self.assertEqual(fids, covered)
        kinds = {a['id'].rsplit('.', 1)[-1]: a['artefact']['kind'] for a in acts}
        want = {'push': 'page_section', 'deepen': 'price_change', 'add': 'offer'}
        for k, v in kinds.items():
            self.assertEqual(v, want[k])
        for a in acts:
            self.assertTrue(a['artefact']['draft'])
            self.assertTrue(a['stop_rule'] and a['win_rule'])
            if a['id'].endswith('.push'):
                self.assertIn('Most popular', a['artefact']['draft'])

    def test_margin_uses_finance_cost(self):
        cogs = api.model.cogs_by_sku(self.rd, self.rd.ends_on)
        for r in self.lad['rows']:
            if r['margin_per_pack'] is not None:
                self.assertAlmostEqual(r['margin_per_pack'], round(r['price_per_pack'] - cogs[r['sku']], 2))


class FirstOrderTest(unittest.TestCase):
    """Round 1 feature 5: the first-order code against offers that keep the list price, with the test brief."""

    @classmethod
    def setUpClass(cls):
        cls.rd = audit.Reader(None, 'bombas', audit.last_full_day(None, 'bombas'))
        cls.fo = audit.first_order(cls.rd)
        cls.out = api.actions.rank('bombas')

    def test_options_arithmetic(self):
        fo = self.fo
        self.assertFalse(fo['unavailable'])
        base = fo['full_price']['contribution']
        code = next(r for r in fo['rows'] if r['key'] == 'code')
        self.assertAlmostEqual(code['price_paid'], round(fo['gross_order'] * (1 - fo['code_pct'] / 100), 2))
        self.assertEqual(code['under_line'], code['price_paid'] < fo['threshold'])
        for r in fo['rows']:
            if r.get('unavailable'):
                self.assertTrue(r['reason'])
                continue
            self.assertAlmostEqual(r['cost'], round(base - r['contribution'], 2), places=1)
            self.assertAlmostEqual(r['payback'], round(r['contribution'] / fo['new_cac'], 2), places=1)
            if r.get('cvr_limit') is not None:
                self.assertAlmostEqual(r['cvr_limit'], round(1 - code['contribution'] / r['contribution'], 4))

    def test_rule_and_action(self):
        f = next((f for f in self.out['findings'] if f['rule_id'] == 'OFFER-R08'), None)
        share = api.model.brain_value(self.rd, 'offers.promo_share_active_ads')[0]
        if share['ads_with_code'] / share['active_ads'] <= audit._playbook().CODE_ADS_SHARE or not self.fo['best_key']:
            self.assertIsNone(f)
            return
        m = f['money_at_stake']
        i = m['inputs']
        self.assertAlmostEqual(m['usd'], round(round(i['discounts_28d'] * i['new_customer_share'], 2) * (1 - i['better_offer_cost'] / i['code_cost']), 2), places=0)
        a = next(a for a in self.out['actions'] if a['rule_id'] == 'OFFER-R08')
        self.assertEqual(a['artefact']['kind'], 'test_brief')
        self.assertIn('conversion', a['artefact']['draft'])
        best = next(r for r in self.fo['rows'] if r['key'] == self.fo['best_key'])
        self.assertTrue(best['keeps_price'])


class WaterfallTest(unittest.TestCase):
    """Round 1 feature 6: margin waterfall per offer and the red line."""

    @classmethod
    def setUpClass(cls):
        cls.out = api.actions.rank('bombas')
        cls.falls = cls.out['waterfalls']

    def test_steps_add_up(self):
        self.assertTrue(self.falls)
        for w in self.falls:
            st = {s['label']: s['value'] for s in w['steps']}
            if w['missing']:
                self.assertIsNone(w['contribution'])
                continue
            downs = sum(s['value'] for s in w['steps'] if s['kind'] == 'down' and s['label'] not in ('Discount', 'Paid media'))
            self.assertAlmostEqual(w['price_paid'], round(st['List price'] - st['Discount'], 2))
            self.assertAlmostEqual(w['before_media'], round(w['price_paid'] - downs, 2), places=1)
            self.assertAlmostEqual(w['contribution'], round(w['before_media'] - st['Paid media'], 2))

    def test_red_line_rule(self):
        pb = audit._playbook()
        for w in self.falls:
            if w['key'].startswith('first_'):
                self.assertEqual(w['red_line'], pb.RED_LINE_FIRST_ORDER)
                self.assertEqual(w['clears'], w['contribution'] >= pb.RED_LINE_FIRST_ORDER)
        under = {w['key'] for w in self.falls if w['status'] == 'live' and w['clears'] is False}
        fired = {f['entity']['id'] for f in self.out['findings'] if f['rule_id'] == 'OFFER-R10'}
        self.assertEqual(under, fired)
        covered = {fid for a in self.out['actions'] for fid in a['finding_ids']}
        for f in self.out['findings']:
            if f['rule_id'] == 'OFFER-R10':
                self.assertIn(f['id'], covered)
                self.assertNotIn('$-', f['sentence'])


class PromoCalendarTest(unittest.TestCase):
    """Round 1 feature 7: promo windows by date rule, last year's numbers, due windows become dated offers."""

    @classmethod
    def setUpClass(cls):
        cls.rd = audit.Reader(None, 'bombas', audit.last_full_day(None, 'bombas'))
        cls.cal = audit.promo_calendar(cls.rd)
        cls.out = api.actions.rank('bombas')

    def test_date_rules(self):
        from datetime import date
        m = api.model
        self.assertEqual(m.window_dates(('bfcm',), 2025), (date(2025, 11, 28), date(2025, 12, 1)))
        self.assertEqual(m.window_dates(('bfcm',), 2026), (date(2026, 11, 27), date(2026, 11, 30)))
        self.assertEqual(m.window_dates(('nth_weekday', 5, 6, 2, -10), 2026)[1], date(2026, 5, 10))   # Mother's Day
        self.assertEqual(m.window_dates(('nth_weekday', 5, 0, -1, -3), 2026)[1], date(2026, 5, 25))   # Memorial Day
        self.assertEqual(m.window_dates(('nth_weekday', 9, 0, 1, -3), 2026)[1], date(2026, 9, 7))     # Labor Day

    def test_every_due_window_is_a_dated_offer(self):
        end = self.rd.ends_on.isoformat()
        for w in self.cal:
            self.assertGreaterEqual(w['end'], end)
            if w['last_year']:
                ly = w['last_year']
                self.assertAlmostEqual(ly['lift'], round(ly['net_per_day'] / ly['baseline_per_day'] - 1, 4))
        due = {'04-offers-pricing.OFFER-R11.window_' + w['key'] for w in self.cal if w['due']}
        fired = {f['id'] for f in self.out['findings'] if f['rule_id'] == 'OFFER-R11'}
        self.assertEqual(due, fired)
        for a in self.out['actions']:
            if a['rule_id'] == 'OFFER-R11':
                gift = next(w for w in self.cal if a['entity']['id'] == 'window_' + w['key'])['gifting']
                self.assertIn(a['artefact']['kind'], ('offer', 'landing_page') if gift else ('offer',))
                self.assertIn('Approve by', a['artefact']['draft'])
                self.assertTrue(a['check_on'])
                m = a['money_at_stake']
                if m:
                    i = m['inputs']
                    self.assertAlmostEqual(m['usd_revenue'], round((i['net_per_day_window'] - i['net_per_day_28d_before']) * i['days'], 2), places=0)

    def test_bfcm_matches_the_round0_depth(self):
        b = api.bfcm(self.rd)
        w = next(w for w in self.cal if w['key'] == 'bfcm')
        if not b['unavailable'] and w['last_year']:
            self.assertEqual(b['start'], w['last_year']['start'])
            self.assertAlmostEqual(b['depth'], w['last_year']['depth'], places=3)


class GiftingTest(unittest.TestCase):
    """Round 1 feature 8: gift-led lines, order-by dates, the holiday landing page, the gift card ledger."""

    @classmethod
    def setUpClass(cls):
        cls.rd = audit.Reader(None, 'bombas', audit.last_full_day(None, 'bombas'))
        cls.g = audit.gifting(cls.rd)
        cls.out = api.actions.rank('bombas')

    def test_index_and_order_by(self):
        from datetime import date
        g = self.g
        for r in g['lines']:
            if r['q4_share'] is not None:
                self.assertAlmostEqual(r['index'], round(r['q4_share'] / g['store_q4_share'], 2), places=2)
                self.assertEqual(r['gift_led'], r['q4_share'] >= g['ratio'] * g['store_q4_share'])
        gday = date.fromisoformat(g['gift_day'])
        for o in g['ship_by']:
            if o['order_by']:
                d = date.fromisoformat(o['order_by'])
                self.assertLess(d, gday)
                self.assertLess(d.weekday(), 5)

    def test_gifting_rides_on_the_holiday_action(self):
        fids = {f['id']: f for f in self.out['findings']}
        covered = {fid: a for a in self.out['actions'] for fid in a['finding_ids']}
        for fid, f in fids.items():
            if f['rule_id'] in ('OFFER-R12', 'OFFER-R13'):
                self.assertIn(fid, covered)
        hol = next((a for a in self.out['actions'] if a['entity']['id'] == 'window_holiday_gifting'), None)
        if hol and any(f['rule_id'] == 'OFFER-R12' for f in fids.values()):
            self.assertEqual(hol['artefact']['kind'], 'landing_page')
            self.assertIn('Order-by dates', hol['artefact']['draft'])
            self.assertIn('04-offers-pricing.OFFER-R12.gifting', hol['finding_ids'])
        led = any(r['gift_led'] for r in self.g['lines'])
        self.assertEqual('04-offers-pricing.OFFER-R12.gifting' in fids, not led)

    def test_ledger_is_a_connect_action(self):
        a = next((a for a in self.out['actions'] if '04-offers-pricing.OFFER-R13.gift_card_liability' in a['finding_ids']), None)
        if self.g['ledger']['unavailable']:
            self.assertEqual(a['owner'], 'person')
            self.assertEqual(a['artefact']['kind'], 'connector_setup')


class GuaranteeTest(unittest.TestCase):
    """Round 1 feature 9: the guarantee as an offer, where it is stated, the doubts it answers, claims against plan."""

    @classmethod
    def setUpClass(cls):
        cls.rd = audit.Reader(None, 'bombas', audit.last_full_day(None, 'bombas'))
        cls.g = audit.guarantee(cls.rd)
        cls.out = api.actions.rank('bombas')

    def test_page_types(self):
        m, pb = api.model, audit._playbook()
        self.assertEqual(m.page_type('https://x.com/', pb.PAGE_TYPES), 'home page')
        self.assertEqual(m.page_type('https://x.com/products/sock-4', pb.PAGE_TYPES), 'product page')
        self.assertEqual(m.page_type('https://x.com/policies/refund-policy', pb.PAGE_TYPES), 'policy page')
        for t in self.g['terms']:
            self.assertEqual(t['selling'], t['page_type'] in pb.SELLING_PAGES)

    def test_rule_and_action(self):
        fs = {f['rule_id']: f for f in self.out['findings']}
        should = bool(self.g['terms']) and not self.g['on_selling_page'] and bool(self.g['answers'])
        self.assertEqual('OFFER-R14' in fs, should)
        self.assertEqual(self.g['one_star_answered'], sum(a['one_star'] or 0 for a in self.g['answers']))
        if should:
            a = next(a for a in self.out['actions'] if a['rule_id'] == 'OFFER-R14')
            self.assertEqual(a['artefact']['kind'], 'page_section')
            self.assertEqual(a['steps'][0]['who'], 'agent')
            if not a.get('registry'):   # a move covered by a running test reads the test first
                self.assertIn('read-only', a['steps'][0]['text'])
            for t in self.g['terms']:
                if t['id'].endswith('offers.guarantee'):
                    self.assertIn(t['text'], a['artefact']['draft'])
        if self.rd.m('returns_by_reason', audit.WINDOW).get('unavailable'):
            self.assertEqual(fs['OFFER-R15']['status'], 'unavailable')


class RankCompleteTest(unittest.TestCase):
    """Round 1 feature 10: rank covers every rule with real titles, steps and artefacts; connect actions merge by source."""

    @classmethod
    def setUpClass(cls):
        cls.rank_mod = load('ecomos_rank', ROOT / 'app' / 'rank.py')
        cls.out = api.actions.rank('bombas')
        cls.acts = cls.out['actions']

    def test_every_rule_has_a_builder_or_is_connect_only(self):
        connect_only = {'OFFER-R03', 'OFFER-R13', 'OFFER-R28'}
        for r in audit.RULES:
            self.assertTrue(r['rule_id'] in api.actions.BUILDERS or r['rule_id'] in connect_only
                            or r['rule_id'] in ('OFFER-R07', 'OFFER-R09'), r['rule_id'])
            self.assertIn(r['rule_id'], audit.__doc__)

    def test_open_actions_are_real_work(self):
        default_titles = set()
        for f in self.out['findings']:
            if f['status'] == 'open':
                default_titles.add(self.rank_mod.action_from_finding(f)['title'])
        for a in self.acts:
            self.assertEqual(self.rank_mod.validate_action(a), [])
            if a['status'] != 'open':
                continue
            self.assertNotIn(a['title'], default_titles)
            self.assertTrue(a['artefact'].get('draft'), a['id'])
            self.assertTrue(a.get('win_rule') or a.get('stop_rule'), a['id'])
            self.assertTrue(a.get('check_on'), a['id'])
            self.assertTrue(any(s['who'] == 'person' for s in a['steps']), a['id'])   # a person approves before anything ships
            self.assertIn(a['owner'], ('agent_drafts', 'person'))   # nothing ships without a person
            self.assertLess(len(a['title'].split()), 20)

    def test_connect_actions_merge_by_source(self):
        con = [a for a in self.acts if a['status'] == 'unavailable']
        labels = [a['artefact']['label'] for a in con]
        self.assertEqual(len(labels), len(set(labels)))
        unavailable = {f['id'] for f in self.out['findings'] if f['status'] == 'unavailable'}
        self.assertEqual(unavailable, {fid for a in con for fid in a['finding_ids']})

    def test_finding_ids_are_unique_across_actions(self):
        ids = [fid for a in self.acts for fid in a['finding_ids']]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(set(ids), {f['id'] for f in self.out['findings'] if f['status'] in ('open', 'unavailable')})

    def test_same_inputs_same_order_and_older_window(self):
        again = api.actions.rank('bombas')
        self.assertEqual([a['id'] for a in again['actions']], [a['id'] for a in self.acts])
        older = api.actions.rank('bombas', {'ends_on': '2026-06-30'})
        self.assertEqual(older['window']['ends_on'], '2026-06-30')
        for a in older['actions']:
            self.assertEqual(self.rank_mod.validate_action(a), [])


class PositionTest(unittest.TestCase):
    """Round 2 feature 1: price and offer position against the competitor set."""

    @classmethod
    def setUpClass(cls):
        cls.rd = audit.Reader(None, 'bombas', audit.last_full_day(None, 'bombas'))
        cls.cp = audit.competitor_position(cls.rd)
        cls.out = api.actions.rank('bombas')

    def test_parsing(self):
        m = api.model
        self.assertEqual(m._median_price('18 to 35 per pair, median 25'), 25.0)
        self.assertEqual(m._median_price('median about 32 per pair (pack parsing rough)'), 32.0)
        self.assertIsNone(m._median_price('from 18 per pair'))
        self.assertEqual(m._pct('bundle save up to 15% off'), 15.0)

    def test_rule_matches_its_inputs(self):
        cp, pb = self.cp, audit._playbook()
        us = cp['us']
        proof_led = [c for c in cp['competitors'] if c['price'] is not None and c['price'] > us['price'] and c['discount_in_ads'] == 0]
        should = us['price'] < cp['set_median_price'] and us['code_share'] > pb.CODE_ADS_SHARE and len(proof_led) >= pb.MIN_PROOF_LED
        fired = [f for f in self.out['findings'] if f['rule_id'] == 'OFFER-R16']
        self.assertEqual(bool(fired), should)
        if fired:
            self.assertEqual(set(fired[0]['brain_refs']), {c['id'] for c in proof_led})
            a = next(a for a in self.out['actions'] if a['rule_id'] == 'OFFER-R16')
            self.assertEqual(a['artefact']['kind'], 'ad_brief')
            self.assertEqual(a['rubric']['reputation'], 5)
            self.assertIn('nothing is copied', a['artefact']['draft'])


class ParityTest(unittest.TestCase):
    """Round 2 feature 2: marketplace listings against the site price per item."""

    @classmethod
    def setUpClass(cls):
        cls.rd = audit.Reader(None, 'bombas', audit.last_full_day(None, 'bombas'))
        cls.mp = audit.marketplace_parity(cls.rd)
        cls.out = api.actions.rank('bombas')

    def test_title_pack(self):
        pats = audit._playbook().PACK_PATTERNS
        m = api.model
        self.assertEqual(m.title_pack("Men's Originals Ankle Socks White Large (4 Pair)", pats), 4)
        self.assertEqual(m.title_pack('Ankle Socks, 6-Pack Cushioned', pats), 6)
        self.assertEqual(m.title_pack('Socks 7 Pairs, 6 Black + 1 Grey', pats), 7)
        self.assertEqual(m.title_pack('Womens No Show Socks,(Black,Medium, 2pcs)', pats), 2)
        self.assertIsNone(m.title_pack('Women\'s Originals Ankle Socks, (Grey/Blue)', pats))

    def test_gap_and_rule(self):
        gap = audit._playbook().PARITY_GAP
        for r in self.mp['rows']:
            if r['gap'] is not None:
                self.assertAlmostEqual(r['per_item'], round(r['price'] / r['pack'], 2))
                self.assertEqual(r['undercut'], r['per_item'] < r['site_per_item'] * (1 - gap))
            else:
                self.assertTrue(r['reason'])
                self.assertFalse(r['undercut'])
        under = [r for r in self.mp['rows'] if r['undercut']]
        f = next((f for f in self.out['findings'] if f['rule_id'] == 'OFFER-R17'), None)
        self.assertEqual(bool(f), bool(under))
        if f:
            self.assertEqual(set(f['brain_refs']), {r['id'] for r in under})
            a = next(a for a in self.out['actions'] if a['rule_id'] == 'OFFER-R17')
            self.assertEqual(a['owner'], 'person')
            self.assertEqual(a['artefact']['kind'], 'listing_fix')
            self.assertNotIn('(-', a['artefact']['draft'])


class DisciplineTest(unittest.TestCase):
    """Round 2 feature 3: discount discipline scorecard, creep and always-on rules, the drafted policy."""

    @classmethod
    def setUpClass(cls):
        cls.rd = audit.Reader(None, 'bombas', audit.last_full_day(None, 'bombas'))
        cls.d = audit.discipline(cls.rd)
        cls.out = api.actions.rank('bombas')

    def test_scorecard(self):
        ty = self.d['this_year']
        self.assertTrue(ty)
        self.assertEqual(ty['promo_days'], len(ty['promo_dates']))
        self.assertTrue(0 <= ty['always_on_share'] <= 1)
        self.assertTrue(0 <= ty['promo_net_share'] <= 1)

    def test_always_on_rides_on_the_code_test(self):
        pb = audit._playbook()
        ty = self.d['this_year']
        f = next((f for f in self.out['findings'] if f['rule_id'] == 'OFFER-R19'), None)
        share = api.model.brain_value(self.rd, 'offers.promo_share_active_ads')[0]
        should = ty['always_on_share'] > pb.ALWAYS_ON and share['ads_with_code'] / share['active_ads'] > pb.CODE_ADS_SHARE
        self.assertEqual(bool(f), should)
        if f:
            host = next(a for a in self.out['actions'] if f['id'] in a['finding_ids'])
            if any(a['rule_id'] == 'OFFER-R08' for a in self.out['actions']):
                self.assertEqual(host['rule_id'], 'OFFER-R08')
            else:
                self.assertEqual(host['artefact']['kind'], 'policy')

    def test_policy_draft_uses_brand_history(self):
        pol = self.out['discipline']['policy']
        self.assertIn('Depth cap', pol)
        self.assertIn(f'{self.d["this_year"]["always_on_share"] * 100:.0f} percent', pol)


class GiftPickTest(unittest.TestCase):
    """Round 2 feature 4: the first-order gift is a named item picked by value over landed cost."""

    def test_pick_and_use(self):
        rd = audit.Reader(None, 'bombas', audit.last_full_day(None, 'bombas'))
        cands = api.model.gwp_candidates(rd, audit._playbook().GWP_RATIO)
        self.assertTrue(cands)
        self.assertEqual([c['ratio'] for c in cands], sorted([c['ratio'] for c in cands], reverse=True))
        for c in cands:
            self.assertAlmostEqual(c['ratio'], round(c['value'] / c['cost'], 2))
            self.assertEqual(c['qualifies'], c['value'] / c['cost'] >= audit._playbook().GWP_RATIO)
        fo = audit.first_order(rd)
        g = next(r for r in fo['rows'] if r['key'] == 'gwp')
        self.assertEqual(g['gift']['sku'], cands[0]['sku'])
        self.assertAlmostEqual(g['extra_item'], cands[0]['cost'])
        w = next(w for w in audit.offer_waterfalls(rd) if w['key'] == 'first_gwp')
        cost = next(s['value'] for s in w['steps'] if s['label'] == 'Landed cost')
        self.assertAlmostEqual(cost, round(fo['cogs'] + cands[0]['cost'], 2), places=1)


class CartLadderTest(unittest.TestCase):
    """Round 2 feature 5: a second cart reward past the free shipping line, and the brand's own tools in the steps."""

    @classmethod
    def setUpClass(cls):
        cls.rd = audit.Reader(None, 'bombas', audit.last_full_day(None, 'bombas'))
        cls.cl = audit.cart_ladder(cls.rd)
        cls.out = api.actions.rank('bombas')

    def test_arithmetic(self):
        cl = self.cl
        self.assertEqual(cl['tier2'] % 5, 0)
        self.assertGreater(cl['tier2'], cl['tiers'][0]['at'])
        cm = api.model.contribution_28d(self.rd)['before_media_share']
        self.assertAlmostEqual(cl['pays_after'], round(cl['gift_cost'] / cm, 2))
        self.assertAlmostEqual(cl['cover'], round(cl['climb'] / cl['pays_after'], 2))
        if cl['leak_share'] is None:
            self.assertTrue(cl['leak_reason'])

    def test_rule_and_tools_from_the_brain(self):
        app = api.model.brain_value(self.rd, 'stack.upsell_app')[0]
        f = next((f for f in self.out['findings'] if f['rule_id'] == 'OFFER-R20'), None)
        self.assertEqual(bool(f), bool(app))
        if f:
            a = next(a for a in self.out['actions'] if a['rule_id'] == 'OFFER-R20')
            self.assertIn(app, a['title'])
            self.assertEqual(a['artefact']['kind'], 'page_section')
        ab = api.model.brain_value(self.rd, 'stack.ab_testing')[0]
        t = next(a for a in self.out['actions'] if a['rule_id'] == 'OFFER-R01')
        if ab:
            self.assertTrue(any(ab in s['text'] for s in t['steps']))


class TestCalendarTest(unittest.TestCase):
    """Round 2 feature 6: moves on one surface never overlap, and none runs inside a promo window."""

    @classmethod
    def setUpClass(cls):
        cls.out = api.actions.rank('bombas')
        cls.tests = cls.out['tests']

    def test_no_overlap_on_a_surface_and_no_test_in_a_window(self):
        from datetime import date
        self.assertTrue(self.tests)
        spans = [(sf, date.fromisoformat(t['start']), date.fromisoformat(t['end'])) for t in self.tests for sf in t['surfaces']]
        for i, (sf, a0, a1) in enumerate(spans):
            for sf2, b0, b1 in spans[i + 1:]:
                if sf == sf2:
                    self.assertFalse(a0 <= b1 and b0 <= a1, sf)
        wins = [(date.fromisoformat(w['start']), date.fromisoformat(w['end'])) for w in self.out['calendar'] if w['days_to_start'] < 120]
        for t in self.tests:
            s0, s1 = date.fromisoformat(t['start']), date.fromisoformat(t['end'])
            self.assertEqual((s1 - s0).days + 1, t['days'])
            for w0, w1 in wins:
                self.assertFalse(s0 <= w1 and w0 <= s1, t['title'])

    def test_every_open_move_with_a_surface_is_scheduled_once(self):
        ids = [t['id'] for t in self.tests]
        self.assertEqual(len(ids), len(set(ids)))
        for a in self.out['actions']:
            if a['status'] == 'open' and api.actions.surfaces(a)[0]:
                self.assertIn(a['id'], ids)


class DepthTest(unittest.TestCase):
    """Round 2 feature 7: promo depth by line against the red line, carried into the Black Friday spec."""

    def test_depth_keeps_the_red_line(self):
        rd = audit.Reader(None, 'bombas', audit.last_full_day(None, 'bombas'))
        pb = audit._playbook()
        dl = api.model.depth_by_line(rd, pb.DEPTH_TIERS)
        self.assertFalse(dl['unavailable'])
        for r in dl['rows']:
            if r['max_depth'] is not None:
                self.assertIn(r['max_depth'], pb.DEPTH_TIERS)
                self.assertGreaterEqual(r['share_at_depth'], dl['target'])
                deeper = [d for d in pb.DEPTH_TIERS if d > r['max_depth']]
                self.assertTrue(all(d > r['max_depth'] for d in deeper))
            else:
                self.assertEqual(r['tier'], 'gift, no discount')
        out = api.actions.rank('bombas')
        bf = next((a for a in out['actions'] if a['entity']['id'] == 'window_bfcm'), None)
        if bf:
            self.assertIn('Depth by line', bf['artefact']['draft'])


class SecondOrderTest(unittest.TestCase):
    """Round 2 feature 8: the cohort curve and the second-order flow."""

    def test_curve_and_flow(self):
        rd = audit.Reader(None, 'bombas', audit.last_full_day(None, 'bombas'))
        cc = audit.cohort_curve(rd)
        self.assertFalse(cc['unavailable'])
        drops = [cc['curve'][k] - cc['curve'][k + 1] for k in range(len(cc['curve']) - 1)]
        self.assertEqual(cc['drop_after_month'], drops.index(max(drops)) + 1)
        self.assertEqual(cc['send_by_day'], 30 * cc['drop_after_month'] - 7)
        out = api.actions.rank('bombas')
        a = next((a for a in out['actions'] if a['rule_id'] == 'OFFER-R21'), None)
        if a:
            self.assertEqual(a['artefact']['kind'], 'flow')
            self.assertIn('no percent off', a['artefact']['draft'])
            self.assertIn(a['id'], [t['id'] for t in out['tests']])


class CostPriceTest(unittest.TestCase):
    """Round 2 feature 9: cost rose, price did not."""

    def test_leak_arithmetic_and_rule(self):
        rd = audit.Reader(None, 'bombas', audit.last_full_day(None, 'bombas'))
        cm = audit.cost_moves(rd)
        self.assertFalse(cm['unavailable'])
        pb = audit._playbook()
        for r in cm['rows']:
            leak = (r['cost_now'] - r['cost_then']) - (r['price_now'] - r['price_then'])
            self.assertAlmostEqual(r['leak_per_pack'], round(leak, 2), places=2)
            self.assertEqual(r['fires'], r['cost_now'] / r['cost_then'] - 1 > pb.COST_MOVE and leak > 0)
            self.assertEqual(r['test_price'] % pb.PRICE_STEP, 0)
            self.assertGreaterEqual(r['test_price'], r['price_now'])
            m1 = r['price_now'] - r['cost_now']
            self.assertAlmostEqual(r['cvr_limit'], round(1 - m1 / (m1 + r['test_raise']), 4), places=3)
        out = api.actions.rank('bombas')
        f = next((f for f in out['findings'] if f['rule_id'] == 'OFFER-R22'), None)
        self.assertEqual(bool(f), any(r['fires'] for r in cm['rows']))
        if f:
            self.assertAlmostEqual(f['money_at_stake']['usd'], round(cm['leak_12m'] * 28 / 365, 2))
            a = next(a for a in out['actions'] if a['rule_id'] == 'OFFER-R22')
            self.assertEqual(a['artefact']['kind'], 'price_change')


class DeskTabsTest(unittest.TestCase):
    """Round 2 feature 10: the desk is 4 job tabs, every rule with an action sits in one, and CSS keeps phone width."""

    def test_tabs_cover_the_rules(self):
        import re
        js = (SCREEN / 'screen.js').read_text(encoding='utf-8')
        self.assertIn('UI.tabs', js)
        in_tabs = set(re.findall(r"'(OFFER-R\d+)'", js[js.index('const TABS'):js.index('const openIn')]))
        connect_only = {'OFFER-R03', 'OFFER-R13', 'OFFER-R28'}
        for r in audit.RULES:
            if r['rule_id'] not in connect_only:
                self.assertIn(r['rule_id'], in_tabs)
        css = (SCREEN / 'screen.css').read_text(encoding='utf-8')
        self.assertIn('max-width: 720px', css)


class RegistryTest(unittest.TestCase):
    """Round 3 feature 1: the experiment registry blocks surfaces, covers duplicate moves, proves doubts; elasticity."""

    @classmethod
    def setUpClass(cls):
        cls.out = api.actions.rank('bombas')
        cls.reg = cls.out['registry']

    def test_running_tests_hold_their_surface(self):
        from datetime import date
        if self.reg['unavailable']:
            return
        end = self.out['window']['ends_on']
        for e in self.reg['entries']:
            if e['status'] != 'running' or not e['surface'] or not e['until'] or e['until'] < end:
                continue
            for t in self.out['tests']:
                if e['surface'] in t['surfaces']:
                    self.assertGreater(t['start'], e['until'], (e['id'], t['title']))

    def test_covered_moves_read_the_test_first(self):
        for a in self.out['actions']:
            if a.get('registry'):
                self.assertIn(a['registry']['id'], a['title'])
                self.assertIn(a['registry']['id'], a['steps'][0]['text'])
                self.assertEqual(a['check_on'], a['registry']['until'])

    def test_elasticity_is_unavailable_without_price_tests(self):
        if self.reg['unavailable']:
            return
        if not any(e['price_test'] and e['status'] == 'done' for e in self.reg['entries']):
            self.assertIsNone(self.reg['elasticity'])
            self.assertTrue(self.reg['elasticity_reason'])


class ReferralTest(unittest.TestCase):
    """Round 3 feature 2: a referral offer paid in product, capped at half of paid CAC."""

    def test_referral(self):
        rd = audit.Reader(None, 'bombas', audit.last_full_day(None, 'bombas'))
        ro = audit.referral(rd)
        self.assertFalse(ro['unavailable'])
        self.assertAlmostEqual(ro['cap'], round(ro['paid_cac'] * audit._playbook().REFERRAL_CAC_SHARE, 2))
        self.assertEqual(ro['clears'], ro['cost_per_referral'] <= ro['paid_cac'] * audit._playbook().REFERRAL_CAC_SHARE)
        out = api.actions.rank('bombas')
        has = api.model.has_program(rd, audit._playbook().PROGRAM_WORDS['referral'])
        f = next((f for f in out['findings'] if f['rule_id'] == 'OFFER-R23'), None)
        self.assertEqual(bool(f), not has and ro['clears'])
        if f:
            a = next(a for a in out['actions'] if a['rule_id'] == 'OFFER-R23')
            self.assertIn('Cap', a['artefact']['draft'])
            self.assertTrue(a['stop_rule'])


class LoyaltyTest(unittest.TestCase):
    """Round 3 feature 3: loyalty paid in product against a gross margin cap."""

    def test_loyalty(self):
        rd = audit.Reader(None, 'bombas', audit.last_full_day(None, 'bombas'))
        lo = audit.loyalty(rd)
        self.assertFalse(lo['unavailable'])
        self.assertAlmostEqual(lo['cash_share_of_margin'], round(lo['earn'] / lo['gross_margin'], 4), places=3)
        self.assertLess(lo['product_share_of_margin'], lo['cash_share_of_margin'])
        fr = lo['first_reward']
        pb = audit._playbook()
        self.assertTrue(pb.LOYALTY_ORDERS_TO_FIRST[0] <= fr['orders_to_reach'] <= pb.LOYALTY_ORDERS_TO_FIRST[1])
        self.assertLessEqual(fr['value'], fr['band'][1] + 0.01)
        out = api.actions.rank('bombas')
        f = next((f for f in out['findings'] if f['rule_id'] == 'OFFER-R24'), None)
        has = api.model.has_program(rd, audit._playbook().PROGRAM_WORDS['loyalty'])
        self.assertEqual(bool(f), not has and lo['product_clears'])
        if f:
            a = next(a for a in out['actions'] if a['rule_id'] == 'OFFER-R24')
            self.assertIn('never cash', a['artefact']['draft'])


class WindowCreepTest(unittest.TestCase):
    """Round 3 feature 4: promo window depth year on year."""

    def test_history_and_rule(self):
        rd = audit.Reader(None, 'bombas', audit.last_full_day(None, 'bombas'))
        hist = audit.depth_history(rd)
        self.assertTrue(hist)
        for h in hist:
            self.assertLess(h['before']['start'], h['last']['start'])
            self.assertAlmostEqual(h['points'], round((h['last']['depth'] - h['before']['depth']) * 100, 2), places=2)
        fired = {f['entity']['id'] for f in audit.run('bombas') if f['rule_id'] == 'OFFER-R25'}
        self.assertEqual(fired, {'window_creep_' + h['key'] for h in hist if h['points'] > audit._playbook().WINDOW_CREEP_POINTS})


class SubscriptionNoteTest(unittest.TestCase):
    def test_note_is_parked_and_creates_no_action(self):
        out = api.actions.rank('bombas')
        sn = out['subscription']
        self.assertTrue(sn['parked'])
        self.assertEqual(len(sn['questions']), 3)
        self.assertFalse([a for a in out['actions'] if 'subscri' in a['title'].lower()])


class DepthRulesTest(unittest.TestCase):
    """Round 3 feature 6: depth.md section 3 applied to this screen."""

    @classmethod
    def setUpClass(cls):
        cls.out = api.actions.rank('bombas')

    def test_rule5_sized_with_a_stop_rule(self):
        for a in self.out['actions']:
            if a['status'] != 'open':
                continue
            self.assertTrue((a.get('size') or {}).get('text'), a['id'])
            self.assertTrue(a.get('stop_rule'), a['id'])
            self.assertTrue(a.get('check_on'), a['id'])

    def test_rule12_words(self):
        import re
        bad = re.compile(r'\b(should|consider|leverage)\b|\u2014', re.I)
        for a in self.out['actions']:
            for t in [a['title'], a['why'], a['artefact'].get('draft') or ''] + [x['text'] for x in a['steps']]:
                self.assertFalse(bad.search(t), (a['id'], t[:80]))

    def test_every_desk_block_ends_in_an_action_line(self):
        import re
        js = (SCREEN / 'screen.js').read_text(encoding='utf-8')
        self.assertIn("id.indexOf('desk-') === 0 && !node.querySelector('.act-line')", js)
        blocks = re.findall(r"function (\w+Block)\(", js)
        body = {b: js[js.index('function ' + b + '('):] for b in blocks}
        for b, src in body.items():
            end = src.find('\n  }\n')
            chunk = src[:end]
            if "section('desk-" in chunk:
                self.assertIn('actionLine(', chunk, b)

    def test_headings_are_questions_or_orders(self):
        import re
        js = (SCREEN / 'screen.js').read_text(encoding='utf-8')
        for t in re.findall(r"const head = \{ title: '([^']+)'", js):
            self.assertTrue(t.endswith('?') or t.split()[0] in ('Should',) or '?' in t, t)


class PlugAndPlayTest(unittest.TestCase):
    """Round 3 feature 7: depth.md rule 11, the same screen for a second brand (the sample brand, no brain folder)."""

    def test_sample_brand_plan(self):
        sys.path.insert(0, str(ROOT / 'app'))
        import server
        req = Req(['overview'], brand='sample')
        req.data = server.Data()
        d = api.handle(req)
        for k in api.DESK_KEYS:
            self.assertIn(k, d)
        covered = {fid for a in d['plan'] for fid in a['finding_ids']}
        for f in d['findings']:
            if f['status'] in ('open', 'unavailable'):
                self.assertIn(f['id'], covered)
        self.assertTrue(any(a['status'] == 'unavailable' for a in d['plan']))   # missing sources show as connect moves
        self.assertFalse(d['brand']['name'] == 'Bombas')
        reg = d['registry']
        if not reg['unavailable']:
            for e in reg['entries']:
                self.assertIn(e['status'], ('running', 'done', 'parked', 'proposed', None))


class PriorsTest(unittest.TestCase):
    """Round 3 feature 8: moves cite the brand's finished tests on their surface."""

    def test_priors_attach_by_surface(self):
        class Ctx:
            registry = {'entries': [{'id': 'EXP-9', 'status': 'done', 'surface': 'cart rewards', 'hypothesis': 'a lower line',
                                     'result': {'note': 'margin per order down $2.40', 'lift': None}, 'learning': 'Keep the line.'}]}
        a = {'status': 'open', 'rule_id': 'OFFER-R01', 'why': 'Base.', 'artefact': {'kind': 'test_brief', 'draft': 'Brief.'},
             'entity': {'id': 'free_shipping_threshold'}, 'brain_refs': []}
        b = {'status': 'open', 'rule_id': 'OFFER-R16', 'why': 'Base.', 'artefact': {'kind': 'ad_brief', 'draft': 'x'},
             'entity': {'id': 'price_position'}, 'brain_refs': []}
        out = api.actions.add_priors([a, b], Ctx())
        self.assertEqual(out[0]['priors'], ['EXP-9'])
        self.assertIn('Keep the line.', out[0]['why'])
        self.assertIn('Priors from the registry', out[0]['artefact']['draft'])
        self.assertNotIn('priors', out[1])


class DecisionsTest(unittest.TestCase):
    """Round 3 feature 9: depth.md rule 14, not now snoozes a move for 14 days and decisions show on the move."""

    def test_snooze_and_show(self):
        import json, tempfile
        from datetime import date
        acts = api.actions.rank('bombas')['actions'][:3]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'decisions.json'
            path.write_text(json.dumps([
                {'finding_id': acts[0]['id'], 'choice': 'not_now', 'time': '2026-09-27T10:00:00Z', 'reason': 'after BFCM'},
                {'finding_id': acts[1]['id'], 'choice': 'agent', 'time': '2026-09-27T10:00:00Z'}]), encoding='utf-8')
            plan, snoozed = api.with_decisions(acts, today=date(2026, 9, 28), path=path)
            self.assertNotIn(acts[0]['id'], [a['id'] for a in plan])
            self.assertEqual(snoozed[0]['back_on'], '2026-10-11')
            shown = next(a for a in plan if a['id'] == acts[1]['id'])
            self.assertEqual(shown['decision']['choice'], 'agent')
            later, _ = api.with_decisions(acts, today=date(2026, 10, 20), path=path)
            self.assertIn(acts[0]['id'], [a['id'] for a in later])   # back after 14 days


class ApprovalsTest(unittest.TestCase):
    """Round 4 feature 1: a move saved to the brain through Brain.put, and its proposed registry row."""

    def setUp(self):
        import shutil, tempfile
        self.tmp = Path(tempfile.mkdtemp())
        shutil.copytree(ROOT / 'app' / 'brain' / 'bombas', self.tmp / 'bombas')
        self.acts = api.actions.rank('bombas')['actions']

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _load(self, rid):
        sys.path.insert(0, str(ROOT / 'app' / 'brain'))
        import store
        from datetime import date
        b = store.Brain('bombas', self.tmp, date(2026, 9, 28))
        return next((r for r in b.raw('plans') if r['id'] == rid), None)

    def test_proposed_and_founder_records(self):
        from datetime import date
        bf = next(a for a in self.acts if a['entity']['id'] == 'window_bfcm')
        r = api.approve('bombas', {'id': bf['id'], 'mode': 'founder'}, brain_root=self.tmp, outbox=self.tmp / 'out', today=date(2026, 9, 28))
        self.assertEqual(r['errors'], [])
        rec = self._load(r['record'])
        self.assertEqual((rec['status'], rec['tier'], rec['source']['type']), ('active', 'approved', 'founder'))
        self.assertEqual(rec['value']['window'], 'bfcm')
        self.assertEqual(rec['value']['move_id'], bf['id'])
        other = next(a for a in self.acts if a['status'] == 'open' and a['id'] != bf['id'])
        r2 = api.approve('bombas', {'id': other['id']}, brain_root=self.tmp, outbox=self.tmp / 'out', today=date(2026, 9, 28))
        rec2 = self._load(r2['record'])
        self.assertEqual((rec2['status'], rec2['source']['type']), ('proposed', 'agent'))
        self.assertTrue(rec2['source']['derived_from'])
        rows = api.approvals.outbox_rows('bombas', self.tmp / 'out')
        self.assertTrue(all(x['status'] == 'proposed' and x['proposed_by'] == '04-offers-pricing' for x in rows))
        self.assertTrue(all(x['metric']['name'] == 'profit_per_visitor' and x['metric']['registered_on'] == '2026-09-28' for x in rows))
        # saving again updates the same record, no duplicate
        api.approve('bombas', {'id': other['id']}, brain_root=self.tmp, outbox=self.tmp / 'out', today=date(2026, 9, 28))
        sys.path.insert(0, str(ROOT / 'app' / 'brain'))
        import store
        ids = [x['id'] for x in store.Brain('bombas', self.tmp).raw('plans')]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(api.approvals.outbox_rows('bombas', self.tmp / 'out')), 2)

    def test_offer_record_planned_then_live(self):
        from datetime import date
        sys.path.insert(0, str(ROOT / 'app' / 'brain'))
        import store
        off = next(a for a in self.acts if a['status'] == 'open' and a['artefact']['kind'] in api.approvals.OFFER_KINDS)
        early = api.launched('bombas', {'id': off['id']}, brain_root=self.tmp, today=date(2026, 9, 28))
        self.assertTrue(early['errors'])   # cannot launch before the founder approves
        r = api.approve('bombas', {'id': off['id'], 'mode': 'founder'}, brain_root=self.tmp, outbox=self.tmp / 'out', today=date(2026, 9, 28))
        b = store.Brain('bombas', self.tmp, date(2026, 9, 28))
        rec = next(x for x in b.raw('offers') if x['id'] == r['offer'])
        self.assertEqual((rec['status'], rec['value']['state']), ('proposed', 'planned'))
        self.assertNotIn(r['offer'], [x['id'] for x in b.records('offers')])   # not read as live by other screens
        lv = api.launched('bombas', {'id': off['id']}, brain_root=self.tmp, today=date(2026, 10, 5))
        self.assertEqual(lv['errors'], [])
        b = store.Brain('bombas', self.tmp, date(2026, 10, 5))
        live = next(x for x in b.records('offers') if x['id'] == r['offer'])
        self.assertEqual((live['value']['state'], live['valid_from']), ('live', '2026-10-05'))

    def test_red_line_blocks_founder_approval(self):
        from datetime import date
        checked = [a for a in self.acts if a.get('margin_check')]
        self.assertTrue(checked)
        a = dict(checked[0], margin_check=dict(checked[0]['margin_check'], clears=False))
        orig = api.actions.rank
        api.actions.rank = lambda brand, window=None, data=None: {'actions': [a]}
        try:
            r = api.approve('bombas', {'id': a['id'], 'mode': 'founder'}, brain_root=self.tmp, outbox=self.tmp / 'out', today=date(2026, 9, 28))
            self.assertTrue(r['errors'])
            self.assertIsNone(r['record'])
            ok = api.approve('bombas', {'id': a['id'], 'mode': 'proposed'}, brain_root=self.tmp, outbox=self.tmp / 'out', today=date(2026, 9, 28))
            self.assertEqual(ok['errors'], [])   # it can still be proposed for review
        finally:
            api.actions.rank = orig
        for c in checked:
            self.assertIn('Margin check', c['artefact']['draft'])

    def test_rejects(self):
        with self.assertRaises(ValueError):
            api.approve('bombas', {'id': 'nope'}, brain_root=self.tmp, outbox=self.tmp / 'out')
        con = next((a for a in self.acts if a['status'] == 'unavailable'), None)
        if con:
            with self.assertRaises(ValueError):
                api.approve('bombas', {'id': con['id']}, brain_root=self.tmp, outbox=self.tmp / 'out')
        with self.assertRaises(ValueError):
            api.approve('bombas', {'id': self.acts[0]['id'], 'mode': 'maybe'}, brain_root=self.tmp, outbox=self.tmp / 'out')

    def test_real_brain_untouched_by_tests(self):
        sys.path.insert(0, str(ROOT / 'app' / 'brain'))
        import store
        self.assertFalse([r for r in store.Brain('bombas').raw('plans') if (r.get('value') or {}).get('screen') == '04-offers-pricing'])


class BundlePairsTest(unittest.TestCase):
    """Round 4 feature 3: bundles from pairs, real on the sample brand's orders, a connect move for Bombas."""

    def test_sample_brand_pairs(self):
        sys.path.insert(0, str(ROOT / 'app'))
        import server
        d = server.Data()
        rd = audit.Reader(d, None, audit.last_full_day(d, None))
        pb = audit._playbook()
        bp = audit.bundle_pairs(rd)
        self.assertFalse(bp['unavailable'])
        for p in bp['pairs']:
            self.assertGreaterEqual(p['orders_both'], pb.PAIR_MIN_ORDERS)
            self.assertGreaterEqual(p['lift'], pb.PAIR_MIN_LIFT)
            self.assertAlmostEqual(p['bundle_price'], round((p['price_a'] + p['price_b']) * (1 - pb.BUNDLE_SAVING), 2))
        out = api.actions.rank(None, None, data=d)
        if bp['pairs']:
            a = next(a for a in out['actions'] if a['rule_id'] == 'OFFER-R26')
            self.assertEqual(a['artefact']['kind'], 'offer')
            self.assertTrue(a['stop_rule'] and a['size']['text'])

    def test_bombas_waits_on_orders(self):
        f = next(f for f in audit.run('bombas') if f['rule_id'] == 'OFFER-R26')
        rd = audit.Reader(None, 'bombas', audit.last_full_day(None, 'bombas'))
        if not rd.table('orders'):
            self.assertEqual(f['status'], 'unavailable')


class ApprovedFirstTest(unittest.TestCase):
    """Round 4 feature 5: an approved move takes its surface first in the test calendar."""

    def test_approved_first(self):
        out = api.actions.rank('bombas')
        tests = out['tests']
        # pick the later of two moves that share a surface and mark it approved
        by_sf = {}
        for t in tests:
            for sf in t['surfaces']:
                by_sf.setdefault(sf, []).append(t)
        pair = next((v for v in by_sf.values() if len(v) >= 2), None)
        if not pair:
            return
        late = max(pair, key=lambda t: t['start'])
        ctx_plans = {late['id']: {'status': 'active'}}
        orig = api.actions.Ctx.__init__

        def init(self, rd):
            orig(self, rd)
            self.plans = ctx_plans
        api.actions.Ctx.__init__ = init
        try:
            again = api.actions.rank('bombas')['tests']
        finally:
            api.actions.Ctx.__init__ = orig
        moved = next(t for t in again if t['id'] == late['id'])
        self.assertTrue(moved['approved'])
        self.assertLessEqual(moved['start'], min(t['start'] for t in again if set(t['surfaces']) & set(moved['surfaces'])))


class LaunchedReadTest(unittest.TestCase):
    """Round 4 feature 6: a launched offer past its check date gets a before and after read."""

    def test_launched_offer_read(self):
        import shutil, tempfile
        from datetime import date
        tmp = Path(tempfile.mkdtemp())
        shutil.copytree(ROOT / 'app' / 'brain' / 'bombas', tmp / 'bombas')
        try:
            acts = api.actions.rank('bombas')['actions']
            off = next(a for a in acts if a['status'] == 'open' and a['artefact']['kind'] in api.approvals.OFFER_KINDS)
            off = dict(off, check_on='2026-09-10')
            orig = api.actions.rank
            api.actions.rank = lambda brand, window=None, data=None: {'actions': [off]}
            try:
                api.approve('bombas', {'id': off['id'], 'mode': 'founder'}, brain_root=tmp, outbox=tmp / 'out', today=date(2026, 8, 20))
                api.launched('bombas', {'id': off['id']}, brain_root=tmp, today=date(2026, 8, 25))
            finally:
                api.actions.rank = orig
            audit.BRAIN_ROOT = tmp
            try:
                rd = audit.Reader(None, 'bombas', audit.last_full_day(None, 'bombas'))
                lo = audit.launched_offers(rd)
                self.assertEqual(len(lo), 1)
                self.assertTrue(lo[0]['due'])
                self.assertTrue(lo[0]['before'] and lo[0]['after'])
                f = next(f for f in audit.run('bombas') if f['rule_id'] == 'OFFER-R27')
                self.assertEqual(f['evidence'][0]['baseline_kind'], 'own_median')      # audit.md kinds (round 8)
                self.assertIn('against 28d before launch', f['evidence'][0]['window'])
                a = next(a for a in api.actions.rank('bombas')['actions'] if a['rule_id'] == 'OFFER-R27')
                self.assertEqual(a['artefact']['kind'], 'report')
                self.assertIn('store-wide', a['artefact']['draft'])
                self.assertIn('tier', lo[0])      # round 6 feature 9: a tier offer reads unavailable without order rows
                if lo[0]['tier']:
                    self.assertTrue(lo[0]['tier_read']['unavailable'])
                    self.assertIn('unavailable', a['artefact']['draft'])
            finally:
                audit.BRAIN_ROOT = None
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class UpsellConnectTest(unittest.TestCase):
    def test_upsell_is_a_connect_move_for_the_named_app(self):
        rd = audit.Reader(None, 'bombas', audit.last_full_day(None, 'bombas'))
        app = api.model.brain_value(rd, 'stack.upsell_app')[0]
        out = api.actions.rank('bombas')
        f = next((f for f in out['findings'] if f['rule_id'] == 'OFFER-R28'), None)
        self.assertEqual(bool(f), bool(app) and not rd.table('upsell_events'))
        if f:
            a = next(a for a in out['actions'] if f['id'] in a['finding_ids'])
            self.assertEqual(a['owner'], 'person')
            self.assertIn(app, a['title'])


class BriefPackTest(unittest.TestCase):
    def test_brief_pack_lists_every_open_move(self):
        d = api.handle(Req(['briefs']))
        acts = [a for a in api.actions.rank('bombas')['actions'] if a['status'] == 'open']
        self.assertEqual(d['moves'], len(acts))
        for a in acts:
            self.assertIn(a['title'], d['text'])
        self.assertIn('Stop if:', d['text'])
        self.assertNotIn('\u2014', d['text'])


class StaleInputsTest(unittest.TestCase):
    def test_old_record_adds_a_refresh_step(self):
        from datetime import date

        class Rd:
            def record(self, rid):
                return {'date': '2026-01-02'} if rid == 'bombas.offers.old' else {'date': '2026-09-20'}

        class Ctx:
            rd, end = Rd(), date(2026, 9, 27)
        a = {'status': 'open', 'why': 'Base.', 'brain_refs': ['bombas.offers.old', 'bombas.offers.new'],
             'steps': [{'n': 1, 'who': 'agent', 'text': 'Draft.'}, {'n': 2, 'who': 'person', 'text': 'Approve.'}]}
        out = api.actions.flag_stale_inputs([a], Ctx())[0]
        self.assertEqual([x['id'] for x in out['stale_inputs']], ['bombas.offers.old'])
        self.assertEqual(out['steps'][0]['who'], 'person')
        self.assertIn('Refresh bombas.offers.old', out['steps'][0]['text'])
        self.assertEqual([x['n'] for x in out['steps']], [1, 2, 3])


class StackReadBackTest(unittest.TestCase):
    def test_planned_and_live_offers_show_in_the_stack(self):
        import shutil, tempfile
        from datetime import date
        tmp = Path(tempfile.mkdtemp())
        shutil.copytree(ROOT / 'app' / 'brain' / 'bombas', tmp / 'bombas')
        try:
            acts = api.actions.rank('bombas')['actions']
            offs = [a for a in acts if a['status'] == 'open' and a['artefact']['kind'] in api.approvals.OFFER_KINDS
                    and (a.get('margin_check') or {}).get('clears') is not False][:2]
            for a in offs:
                api.approve('bombas', {'id': a['id'], 'mode': 'founder'}, brain_root=tmp, outbox=tmp / 'out', today=date(2026, 9, 28))
            api.launched('bombas', {'id': offs[0]['id']}, brain_root=tmp, today=date(2026, 9, 28))
            audit.BRAIN_ROOT = tmp
            try:
                rd = audit.Reader(None, 'bombas', audit.last_full_day(None, 'bombas'))
                stack = api.offer_stack(rd)
            finally:
                audit.BRAIN_ROOT = None
            states = sorted(r['state'] for r in stack if r.get('state'))
            self.assertEqual(states, ['live', 'planned'])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class BreakEvenDiscountTest(unittest.TestCase):
    def test_cap_and_multiple(self):
        rd = audit.Reader(None, 'bombas', audit.last_full_day(None, 'bombas'))
        dl = api.model.depth_by_line(rd, audit._playbook().DEPTH_TIERS)
        for r in dl['rows']:
            self.assertTrue(0 < r['break_even_discount'] < 1)
            if r['units_needed_at_20'] is not None:
                self.assertGreater(r['units_needed_at_20'], 1)
                self.assertGreater(r['break_even_discount'], 0.2)
        bf = next((a for a in api.actions.rank('bombas')['actions'] if a['entity']['id'] == 'window_bfcm'), None)
        if bf:
            self.assertIn('Volume check', bf['artefact']['draft'])


class BnplTest(unittest.TestCase):
    def test_band_and_rule(self):
        rd = audit.Reader(None, 'bombas', audit.last_full_day(None, 'bombas'))
        b = audit.bnpl_band(rd)
        self.assertTrue(0 <= b['revenue_share'] <= 1)
        out = api.actions.rank('bombas')
        f = next((f for f in out['findings'] if f['rule_id'] == 'OFFER-R29'), None)
        self.assertEqual(bool(f), not b['named'] and bool(b['packs']))
        if f:
            a = next(a for a in out['actions'] if a['rule_id'] == 'OFFER-R29')
            self.assertEqual(a['steps'][0]['who'], 'person')   # first confirm what checkout already offers
            self.assertIn('profit per visitor', a['artefact']['draft'])


class ThresholdMatchTest(unittest.TestCase):
    def test_mismatch_fires_on_a_copy_of_the_brain(self):
        import shutil, tempfile, json
        tmp = Path(tempfile.mkdtemp())
        shutil.copytree(ROOT / 'app' / 'brain' / 'bombas', tmp / 'bombas')
        try:
            self.assertFalse([f for f in audit.run('bombas') if f['rule_id'] == 'OFFER-R30'])
            sys.path.insert(0, str(ROOT / 'app' / 'brain'))
            import store
            b = store.Brain('bombas', tmp)
            rec = next(r for r in b.raw('policies') if r['id'] == 'bombas.policies.shipping_options')
            opts = [dict(o, threshold_usd=60) if o.get('cost_usd') == 0 else o for o in rec['value']]
            self.assertEqual(b.put(dict(rec, value=opts)), [])
            audit.BRAIN_ROOT = tmp
            try:
                f = next(f for f in audit.run('bombas') if f['rule_id'] == 'OFFER-R30')
                self.assertEqual(f['severity'], 'high')
            finally:
                audit.BRAIN_ROOT = None
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class DiscountCohortTest(unittest.TestCase):
    def test_sample_cohorts_and_bombas_unavailable(self):
        sys.path.insert(0, str(ROOT / 'app'))
        import server
        d = server.Data()
        rd = audit.Reader(d, None, audit.last_full_day(d, None))
        dc = audit.discount_cohorts(rd)
        self.assertFalse(dc['unavailable'])
        for k in ('discounted', 'full_price'):
            if dc[k]['repeat'] is not None:
                self.assertTrue(0 <= dc[k]['repeat'] <= 1)
                self.assertGreaterEqual(dc[k]['customers'], audit._playbook().COHORT_MIN)
        fired = [f for f in audit.run(None, None, data=d) if f['rule_id'] == 'OFFER-R31']
        pb = audit._playbook()
        should = (dc['discounted']['repeat'] is not None and dc['full_price']['repeat']
                  and dc['discounted']['repeat'] < dc['full_price']['repeat'] * (1 - pb.COHORT_GAP))
        self.assertEqual(bool(fired), bool(should))
        rb = audit.Reader(None, 'bombas', audit.last_full_day(None, 'bombas'))
        if not rb.table('orders'):
            self.assertEqual(next(f for f in audit.run('bombas') if f['rule_id'] == 'OFFER-R31')['status'], 'unavailable')


class BunchesTest(unittest.TestCase):
    def test_peaks(self):
        g = [{'from': f, 'to': f + 5, 'share': s} for f, s in [(50, .05), (55, .12), (60, .06), (70, .03), (105, .09), (110, .04), (175, .02), (180, .05), (185, .01)]]
        p = api.model.order_bunches(g)
        self.assertEqual([x['at'] for x in p], [57.5, 107.5, 182.5])
        self.assertEqual([x['tier'] for x in p], [70, 120, 195])

    def test_real_rows_only(self):
        b = api.actions.bunches(audit.Reader(None, 'bombas', audit.last_full_day(None, 'bombas')))
        rd = audit.Reader(None, 'bombas', audit.last_full_day(None, 'bombas'))
        if rd.m('order_value_distribution', 28, step=5).get('unavailable'):
            self.assertTrue(b['unavailable'])   # never computed from the fixture


class NoThresholdInJsTest(unittest.TestCase):
    """Round 6 feature 1: no threshold, market or brand word written in screen.js; no zero stands in for unknown."""

    def test_js(self):
        import re
        js = (SCREEN / 'screen.js').read_text(encoding='utf-8')
        texts = re.findall(r"(?:title|sub|text|label): '([^']*)'", js)
        for t in texts:
            self.assertFalse(re.search(r'\b\d+ percent\b', t), t)
            self.assertNotIn('US ', t)
        self.assertNotRegex(js, r'\|\| 0\b')
        self.assertNotRegex(js, r'\?\? 0\b')
        d = api.handle(Req(['overview']))
        for k in ('single_share_push', 'min_saving', 'depth_cut', 'approval_days', 'parity_gap', 'snooze_days'):
            self.assertIsNotNone(d['settings'][k])


class SizedStopTest(unittest.TestCase):
    """Round 6 feature 2: depth.md rules 5 and 12 on both brands. Every move that changes money or traffic
    carries a size, a stop rule and a check date; titles and steps stay under 20 words; no banned words."""

    def check(self, acts):
        import re
        for a in acts:
            if a['artefact']['kind'] != 'connector_setup':
                self.assertTrue((a.get('size') or {}).get('text'), a['id'])
                self.assertTrue(a.get('stop_rule'), a['id'])
                self.assertTrue(a.get('check_on'), a['id'])
            for t in [a['title']] + [s['text'] for s in a['steps']]:
                self.assertLess(len(t.split()), 20, t)
            self.assertNotRegex(a['title'] + a.get('why', ''), r'(?i)\b(should|consider|leverage)\b')

    def test_bombas(self):
        self.check(api.actions.rank('bombas')['actions'])

    def test_sample(self):
        sys.path.insert(0, str(ROOT / 'app'))
        import server
        self.check(api.actions.rank(None, None, server.Data())['actions'])


class BlockLineTest(unittest.TestCase):
    """Round 6 feature 3: depth.md rule 9 and section 2. Every desk block ends in a real next move: the move its
    rules made, or the reason it is unavailable. No block ends in a generic line."""

    def test_every_block_mapped(self):
        import re
        js = (SCREEN / 'screen.js').read_text(encoding='utf-8')
        ids = set(re.findall(r"section\('(desk-[a-z]+)'", js))
        mapped = set(re.findall(r"'(desk-[a-z]+)': \[", js))
        self.assertEqual(ids - mapped - {'desk-stack', 'desk-subscription'}, set())
        self.assertNotIn('waits on the source named above', js)


class BlindSpotsTest(unittest.TestCase):
    """Round 6 feature 4: price sensitivity and gift card balances say unavailable on the page, with what fills them.
    No number stands in for them."""

    def test_bombas(self):
        d = api.handle(Req(['overview']))
        keys = {x['key']: x for x in d['blind_spots']}
        for k in ('price_sensitivity', 'gift_card_balances'):
            self.assertIn(k, keys)
            self.assertTrue(keys[k]['reason'] and keys[k]['needs'] and keys[k]['fills'])
        ids = {a['id'] for a in d['plan']}
        for x in d['blind_spots']:
            if x['action_id']:
                self.assertIn(x['action_id'], ids)

    def test_price_read_clears_it(self):
        ranked = {'actions': [], 'registry': {'elasticity': {'tests': ['EXP-1'], 'reads': []}},
                  'gifting': {'ledger': {'unavailable': False}}, 'bundles': {}, 'returns': {}}
        self.assertEqual(api.blind_spots(ranked), [])


class PhoneTest(unittest.TestCase):
    """Round 6 feature 5: the 360 px pass. Buttons keep a 32 px tap target on phones; no fixed widths past 360 px."""

    def test_css(self):
        import re
        css = (SCREEN / 'screen.css').read_text(encoding='utf-8')
        self.assertIn('min-height: 32px', css)
        for w in re.findall(r'(?<!max-)(?<!min-)width:\s*(\d+)px', css):
            self.assertLessEqual(int(w), 360, w)


class WelcomeCodeTest(unittest.TestCase):
    """Round 6 feature 6: room job LIFE-C02. The welcome code's required new share, OFFER-R32 and its holdout test."""

    def reader(self, orders, flows=None, registry=None):
        import datetime as dtm
        class Src:
            brand = {}
        class R:
            brand = None
            ends_on = dtm.date(2026, 9, 24)
            source = Src()
            def table(self, name):
                return {'orders': orders, 'flows': flows, 'registry': registry}.get(name)
            def record(self, key):
                return None
            def records(self, section):
                return []
        return R()

    def order(self, cid, day, code=None, amount=0, subtotal=100, cogs=40):
        return {'customer_id': cid, 'created_at': day + 'T10:00:00Z', 'subtotal': subtotal, 'cogs': cogs,
                'discount': {'code': code, 'amount': amount} if code else None}

    def test_required_share(self):
        orders = [self.order(1, '2026-09-01', 'HELLO', 10), self.order(2, '2026-09-02', 'HELLO', 10), self.order(3, '2026-09-03'),
                  self.order(1, '2026-09-10'), self.order(4, '2026-01-01', 'HELLO', 10)]
        flows = [{'flow': 'Welcome Series', 'message_id': 'F-01-M1', 'date': '2026-09-01', 'sends': 8},
                 {'flow': 'Welcome Series', 'message_id': 'F-01-M2', 'date': '2026-09-01', 'sends': 7}]
        w = api.model.welcome_code(self.reader(orders, flows), 90, ('welcome',))
        self.assertEqual((w['code'], w['code_orders'], w['full_price_orders'], w['new_customers']), ('HELLO', 2, 1, 3))
        self.assertEqual(w['code_dollars'], 20)
        self.assertEqual(w['margin_after_code'], 100)          # 2 x (100 - 10 - 40)
        self.assertAlmostEqual(w['required_new_share'], 20 / 120, 4)
        self.assertEqual(w['signups'], 8)                      # first message only
        self.assertEqual(w['signup_to_order'], 0.25)

    def test_no_orders_unavailable(self):
        self.assertTrue(api.model.welcome_code(self.reader([]), 90, ('welcome',))['unavailable'])

    def test_sample_rule_and_action(self):
        sys.path.insert(0, str(ROOT / 'app'))
        import server
        r = api.actions.rank(None, None, server.Data())
        a = next(x for x in r['actions'] if x['rule_id'] == 'OFFER-R32')
        self.assertEqual(a['artefact']['kind'], 'test_brief')
        self.assertIn('profit per visitor', a['artefact']['draft'])
        self.assertTrue(a['stop_rule'] and a['check_on'])

    def test_bombas_connect(self):
        f = [x for x in audit.run('bombas') if x['rule_id'] == 'OFFER-R32']
        self.assertEqual([x['status'] for x in f], ['unavailable'])


class TestTrustTest(unittest.TestCase):
    """Round 6 feature 7: room job LIFE-C47, is any test untrustworthy. OFFER-R33 and model.test_trust."""

    def entry(self, **kw):
        e = {'id': 'E1', 'status': 'running', 'surface': 'first order offer', 'start': '2026-08-01', 'until': '2026-10-01',
             'metric': 'profit_per_visitor', 'registered_on': '2026-07-30', 'min_days': 28, 'result': None, 'hypothesis': 'h'}
        e.update(kw)
        return e

    def keys(self, entries):
        import datetime as dtm
        pb = api.actions.playbook
        t = api.model.test_trust(entries, dtm.date(2026, 9, 24), pb.OFFER_SURFACES, pb.BAD_OFFER_METRICS, pb.TEST_MIN_DAYS)
        return {r['id']: [p['key'] for p in r['problems']] for r in t['rows']}

    def test_each_problem(self):
        self.assertEqual(self.keys([self.entry()]), {})
        self.assertEqual(self.keys([self.entry(metric=None)]), {'E1': ['no_metric']})
        self.assertEqual(self.keys([self.entry(registered_on='2026-08-05')]), {'E1': ['late_metric']})
        self.assertEqual(self.keys([self.entry(result={'read_on': '2026-09-01'})]), {'E1': ['early_look']})
        self.assertEqual(self.keys([self.entry(until='2026-09-01')]), {'E1': ['overdue']})
        self.assertEqual(self.keys([self.entry(status='done', until='2026-08-20')]), {'E1': ['short']})
        self.assertEqual(self.keys([self.entry(metric='aov')]), {'E1': ['wrong_metric']})
        self.assertEqual(self.keys([self.entry(), self.entry(id='E2')]), {'E1': ['collision'], 'E2': ['collision']})

    def test_bombas_rule(self):
        f = [x for x in audit.run('bombas') if x['rule_id'] == 'OFFER-R33']
        self.assertEqual(len(f), 1)
        a = next(x for x in api.actions.rank('bombas')['actions'] if x['rule_id'] == 'OFFER-R33')
        self.assertEqual((a['owner'], a['artefact']['kind']), ('person', 'report'))
        self.assertIn('EXP-005', a['artefact']['draft'])     # an offer test judged on aov


class PriceMovesTest(unittest.TestCase):
    """Round 6 feature 8: room jobs BRN-C11 and PROD-C46, did a competitor or reseller move price. OFFER-R34."""

    def reader(self, comps, listings):
        class R:
            def records(self, sec):
                return {'competitors': comps, 'marketplaces': listings}.get(sec, [])
        return R()

    def listing(self, rid, asin, price, on, history=()):
        return {'id': rid, 'value': {'channel': 'amazon', 'asin': asin, 'price_usd': price}, 'source': {'captured_at': on},
                'history': list(history)}

    def test_move_from_same_item_history(self):
        old = {'value': {'asin': 'A1', 'price_usd': 40.0}, 'changed_at': '2026-08-01'}
        pm = api.model.price_moves(self.reader([], [self.listing('l1', 'A1', 36.0, '2026-09-01', [old])]), 0.05)
        self.assertFalse(pm['unavailable'])
        self.assertEqual([m['change'] for m in pm['moves']], [-0.1])

    def test_merged_duplicate_is_not_a_move(self):
        dup = {'value': {'asin': 'A2', 'price_usd': 20.0}, 'changed_at': '2026-08-01', 'reason': 'near duplicate', 'record_id': 'l2'}
        same_day = {'value': {'asin': 'A1', 'price_usd': 20.0}, 'changed_at': '2026-09-01'}
        pm = api.model.price_moves(self.reader([], [self.listing('l1', 'A1', 36.0, '2026-09-01', [dup, same_day])]), 0.05)
        self.assertTrue(pm['unavailable'])
        self.assertIn('one capture', pm['reason'])

    def test_competitor_band(self):
        c = {'id': 'c1', 'value': {'name': 'Rival', 'price_band_usd': 'median 14'}, 'source': {'captured_at': '2026-09-01'},
             'history': [{'value': {'name': 'Rival', 'price_band_usd': 'median 16'}, 'changed_at': '2026-08-01'}]}
        pm = api.model.price_moves(self.reader([c], []), 0.05)
        self.assertEqual(pm['moves'][0]['name'], 'Rival')
        self.assertEqual(pm['moves'][0]['change'], -0.125)

    def test_bombas_recapture(self):
        a = next(x for x in api.actions.rank('bombas')['actions'] if any('OFFER-R34' in f for f in x['finding_ids']))
        self.assertEqual((a['status'], a['owner'], a['artefact']['kind']), ('unavailable', 'person', 'connector_setup'))
        self.assertIn('again on', a['title'])


class TierLiftTest(unittest.TestCase):
    """Round 6 feature 9: room job LIFE-C40, is the gift lifting the tier we want. model.tier_lift."""

    def orders(self, day0, n, value, cogs=30):
        from datetime import timedelta
        return [{'created_at': (day0 + timedelta(days=i % 28)).isoformat() + 'T10:00:00Z', 'subtotal': value, 'cogs': cogs,
                 'discount': None} for i in range(n)]

    def test_lift(self):
        from datetime import date
        start = date(2026, 9, 1)
        before = self.orders(date(2026, 8, 4), 10, 60) + self.orders(date(2026, 8, 4), 10, 100)   # half over $90
        after = self.orders(start, 5, 60) + self.orders(start, 15, 100)                            # 75 percent over
        t = api.model.tier_lift(before + after, 90, start, date(2026, 9, 28))
        self.assertEqual((t['before']['share_over'], t['after']['share_over'], t['lift_points']), (0.5, 0.75, 25.0))
        self.assertEqual(t['before']['margin_per_order'], 50.0)
        self.assertEqual(t['margin_change'], 10.0)

    def test_too_soon_and_no_rows(self):
        from datetime import date
        self.assertTrue(api.model.tier_lift([], 90, date(2026, 9, 1), date(2026, 9, 28))['unavailable'])
        o = self.orders(date(2026, 8, 4), 5, 100)
        self.assertEqual(api.model.tier_lift(o, 90, date(2026, 9, 25), date(2026, 9, 28))['reason'], 'less than 7 days since launch')


class ClaimStressTest(unittest.TestCase):
    """Round 6 feature 10: room job LIFE-C42, does the guarantee break margin if claims run high. OFFER-R35."""

    def rd(self):
        return audit.Reader(None, 'bombas', audit.last_full_day(None, 'bombas'))

    def test_bombas_holds(self):
        gs = audit.guarantee_stress(self.rd())
        self.assertFalse(gs['unavailable'])
        one, two = gs['rows'][0], gs['rows'][1]
        self.assertAlmostEqual(two['claims_per_order'], 2 * one['claims_per_order'], delta=0.011)
        self.assertAlmostEqual(gs['contribution_per_order'] - gs['breaks_at'] * gs['planned_cost_per_order'],
                               gs['target'] * gs['net'], delta=0.2)
        self.assertGreater(gs['breaks_at'], api.actions.playbook.CLAIM_STRESS)
        self.assertEqual([f for f in audit.run('bombas') if f['rule_id'] == 'OFFER-R35'], [])

    def test_fires_when_claims_are_heavy(self):
        orig = audit.guarantee
        audit.guarantee = lambda rd: dict(orig(rd), planned={'replacement': 0.05, 'refund': 0.12, 'refund_or_replace': 0.17})
        try:
            f = [x for x in audit.run('bombas') if x['rule_id'] == 'OFFER-R35']
            self.assertEqual(len(f), 1)
            self.assertIn(f[0]['severity'], ('high', 'critical'))   # raised by money share (round 8)
            a = next(x for x in api.actions.rank('bombas')['actions'] if x['rule_id'] == 'OFFER-R35')
            self.assertEqual(a['artefact']['kind'], 'policy')
        finally:
            audit.guarantee = orig

    def test_no_plan_unavailable(self):
        self.assertTrue(api.model.guarantee_stress(self.rd(), {}, (1, 2))['unavailable'])


class PaidPriceTest(unittest.TestCase):
    """Round 7 feature 1: what shoppers really pay per product, and OFFER-R36 when a product leans on the code."""

    def reader(self, orders, products):
        import datetime as dtm
        class R:
            brand = None
            ends_on = dtm.date(2026, 9, 24)
            def table(self, name):
                return {'orders': orders, 'products': products}.get(name)
        return R()

    def test_paid_and_code_share(self):
        products = [{'sku': 'A', 'title': 'Pan', 'price': 100}, {'sku': 'B', 'title': 'Lid', 'price': 50}]
        orders = [{'created_at': '2026-09-01T10:00:00Z', 'subtotal': 150, 'discount': {'code': 'X', 'amount': 15},
                   'line_items': [{'sku': 'A', 'qty': 1, 'line_total': 100}, {'sku': 'B', 'qty': 1, 'line_total': 50}]},
                  {'created_at': '2026-09-02T10:00:00Z', 'subtotal': 100, 'discount': None,
                   'line_items': [{'sku': 'A', 'qty': 1, 'line_total': 100}]}]
        pp = api.model.paid_prices(self.reader(orders, products), 90, 1)
        by = {r['sku']: r for r in pp['rows']}
        self.assertEqual((by['A']['paid'], by['A']['kept'], by['A']['code_share']), (95.0, 0.95, 0.5))
        self.assertEqual((by['B']['paid'], by['B']['code_share']), (45.0, 1.0))
        self.assertEqual(pp['rows'][0]['sku'], 'B')

    def test_unavailable(self):
        self.assertTrue(api.model.paid_prices(self.reader([], []), 90, 1)['unavailable'])

    def test_sample_quiet_and_bombas_silent(self):
        sys.path.insert(0, str(ROOT / 'app'))
        import server
        rd = audit.Reader(server.Data(), None, audit.last_full_day(server.Data(), None))
        pp = audit.paid_prices(rd)
        self.assertFalse(pp['unavailable'])
        self.assertLess(max(r['code_share'] for r in pp['rows'] if r['judged']), api.actions.playbook.CODE_DEPENDENT)
        self.assertEqual([f for f in audit.run('bombas') if f['rule_id'] == 'OFFER-R36'], [])

    def test_fires(self):
        pbs = (api.actions.playbook, audit._playbook())
        orig = pbs[0].CODE_DEPENDENT
        for pb in pbs:
            pb.CODE_DEPENDENT = 0.30
        try:
            sys.path.insert(0, str(ROOT / 'app'))
            import server
            r = api.actions.rank(None, None, server.Data())
            a = next(x for x in r['actions'] if x['rule_id'] == 'OFFER-R36')
            self.assertIn('profit per visitor', a['artefact']['draft'])
        finally:
            for pb in pbs:
                pb.CODE_DEPENDENT = orig


class AttachTest(unittest.TestCase):
    """Round 7 feature 2: room job LIFE-C41, which top products rarely get a second item. OFFER-R37."""

    def test_rates_and_partner(self):
        import datetime as dtm
        products = [{'sku': s_, 'title': s_, 'price': 10, 'cost': 4} for s_ in 'ABC']
        mk = lambda skus: {'created_at': '2026-09-01T10:00:00Z', 'line_items': [{'sku': x} for x in skus]}
        orders = [mk('A')] * 3 + [mk('AB')] + [mk('BC')] * 2 + [mk('C')]
        class R:
            brand = None
            ends_on = dtm.date(2026, 9, 24)
            def table(self, name):
                return {'orders': orders, 'products': products}.get(name)
        ar = api.model.attach_rates(R(), 90, 1)
        by = {r['sku']: r for r in ar['rows']}
        self.assertEqual((by['A']['orders'], by['A']['attach'], by['A']['partner']), (4, 0.25, 'B'))
        self.assertEqual((by['B']['attach'], by['B']['partner'], by['B']['partner_margin']), (1.0, 'C', 6))
        self.assertEqual(ar['median'], 0.6667)

    def test_sample_fires(self):
        sys.path.insert(0, str(ROOT / 'app'))
        import server
        r = api.actions.rank(None, None, server.Data())
        a = next(x for x in r['actions'] if x['rule_id'] == 'OFFER-R37')
        self.assertEqual(a['artefact']['kind'], 'page_section')
        self.assertIn('profit per visitor', a['artefact']['draft'])
        self.assertIn('No discount', a['artefact']['draft'])


class CodeReturnsTest(unittest.TestCase):
    """Round 7 feature 3: do code orders come back more. model.returns_by_code and OFFER-R38."""

    def test_split(self):
        import datetime as dtm
        mk = lambda code, back: {'created_at': '2026-06-01T10:00:00Z', 'subtotal': 100,
                                 'discount': {'code': 'X', 'amount': 10} if code else None,
                                 'return': 'R1' if back else None, 'refund': {'amount': 90} if back else None}
        orders = [mk(True, True)] * 2 + [mk(True, False)] * 8 + [mk(False, True)] + [mk(False, False)] * 9
        class R:
            ends_on = dtm.date(2026, 9, 24)
            def table(self, name):
                return orders if name == 'orders' else None
        rc = api.model.returns_by_code(R(), 180, 30)
        self.assertEqual((rc['code']['returned'], rc['full_price']['returned'], rc['ratio']), (0.2, 0.1, 2.0))
        self.assertEqual(rc['code']['refund_share'], 0.2)            # 180 / 900

    def test_sample_quiet(self):
        sys.path.insert(0, str(ROOT / 'app'))
        import server
        rd = audit.Reader(server.Data(), None, audit.last_full_day(server.Data(), None))
        rc = audit.returns_by_code(rd)
        self.assertLess(rc['ratio'], api.actions.playbook.RETURN_RATIO)
        self.assertEqual([f for f in audit.run(None, None, server.Data()) if f['rule_id'] == 'OFFER-R38'], [])


class PowerTest(unittest.TestCase):
    """Round 7 feature 4: profit per visitor today, the days a test needs, and OFFER-R39 for thin traffic."""

    def test_formula(self):
        base = {'unavailable': False, 'conversion': 0.02, 'sessions_per_day': 1000}
        k = api.actions.playbook.POWER_K
        d = api.model.detectable_lift(base, 28, k)
        self.assertAlmostEqual(d, (k * 0.98 / (0.02 * 14000)) ** 0.5, 4)
        self.assertIsNone(api.model.detectable_lift({'unavailable': True}, 28, k))

    def test_sample_thin_bombas_not(self):
        sys.path.insert(0, str(ROOT / 'app'))
        import server
        r = api.actions.rank(None, None, server.Data())
        vb = r['baseline']
        self.assertGreater(vb['days_needed'], api.actions.playbook.POWER_MAX_DAYS)
        a = next(x for x in r['actions'] if x['rule_id'] == 'OFFER-R39')
        self.assertEqual(a['artefact']['kind'], 'policy')
        self.assertTrue(all(row['can_see'] for row in r['tests']))
        b = api.actions.rank('bombas')
        self.assertLessEqual(b['baseline']['days_needed'], api.actions.playbook.POWER_MAX_DAYS)
        self.assertFalse(any(x['rule_id'] == 'OFFER-R39' for x in b['actions']))


class CodeLeakTest(unittest.TestCase):
    """Round 7 feature 5 (web pass 3: KeepCart): the first-order code on returning buyers, coupon sites, spikes."""

    def reader(self, orders):
        import datetime as dtm
        class R:
            ends_on = dtm.date(2026, 9, 24)
            def table(self, name):
                return orders if name == 'orders' else None
        return R()

    def order(self, day, code, new, source='google', amount=10):
        return {'created_at': day + 'T10:00:00Z', 'discount': {'code': code, 'amount': amount}, 'customer_is_new': new,
                'utm': {'source': source}}

    def test_signals(self):
        pb = api.actions.playbook
        orders = ([self.order('2026-09-01', 'HELLO', True)] * 5 + [self.order('2026-09-02', 'HELLO', False)] * 3
                  + [self.order('2026-09-03', 'SAVE5', True, source='retailmenot.com')] * 2
                  + [self.order('2026-09-20', 'FLASH', True)] * 25 + [self.order('2026-08-01', 'FLASH', True)])
        cl = api.model.code_leaks(self.reader(orders), 90, pb.COUPON_SITE_WORDS, pb.LEAK_SPIKE, pb.LEAK_SPIKE_MIN)
        self.assertEqual(cl['first_code'], 'FLASH')          # most used by new customers when the brain names none
        cl = api.model.code_leaks(self.reader(orders), 90, pb.COUPON_SITE_WORDS, pb.LEAK_SPIKE, pb.LEAK_SPIKE_MIN, 'hello')
        self.assertEqual(cl['returning']['orders'], 3)
        self.assertEqual(cl['coupon_sites']['orders'], 2)
        self.assertEqual([x['code'] for x in cl['spikes']], ['FLASH'])
        self.assertEqual(cl['returning']['dollars_28d'], round(30 * 28 / 90, 2))

    def test_sample_quiet(self):
        sys.path.insert(0, str(ROOT / 'app'))
        import server
        self.assertEqual([f for f in audit.run(None, None, server.Data()) if f['rule_id'] == 'OFFER-R40'], [])


class ReturnerCodeTest(unittest.TestCase):
    """Round 7 feature 6: do codes bring returning buyers back sooner. model.returner_codes and OFFER-R41."""

    def test_gaps(self):
        import datetime as dtm
        mk = lambda c, day, code=None: {'customer_id': c, 'created_at': day + 'T10:00:00Z',
                                        'discount': {'code': code, 'amount': 5} if code else None}
        orders = [mk(1, '2026-06-01'), mk(1, '2026-07-01', 'BACK'), mk(2, '2026-06-01'), mk(2, '2026-08-01'),
                  mk(3, '2026-01-01'), mk(3, '2026-02-01')]
        class R:
            ends_on = dtm.date(2026, 9, 24)
            def table(self, name):
                return orders if name == 'orders' else None
        rc = api.model.returner_codes(R(), 180)
        self.assertEqual((rc['code']['orders'], rc['code']['median_gap']), (1, 30))
        self.assertEqual((rc['none']['orders'], rc['none']['median_gap']), (1, 61))   # customer 3 is before the window
        self.assertEqual(rc['codes'], [('BACK', 1)])

    def test_sample_fires(self):
        sys.path.insert(0, str(ROOT / 'app'))
        import server
        r = api.actions.rank(None, None, server.Data())
        a = next(x for x in r['actions'] if x['rule_id'] == 'OFFER-R41')
        self.assertIn('profit per recipient', a['artefact']['draft'])
        self.assertTrue(a['stop_rule'] and a['check_on'])


class DepthBandTest(unittest.TestCase):
    """Round 7 feature 7 (web pass 3: Lifetimely): repeat by first-order code depth band."""

    def test_bands(self):
        sys.path.insert(0, str(ROOT / 'app'))
        import server
        rd = audit.Reader(server.Data(), None, audit.last_full_day(server.Data(), None))
        dc = audit.discount_cohorts(rd)
        bands = dc['by_depth']
        self.assertEqual(bands[0]['to'], 0.0)
        self.assertEqual(bands[0]['customers'], dc['full_price']['customers'])
        self.assertEqual(sum(b['customers'] for b in bands[1:]), dc['discounted']['customers'])
        for b in bands:
            if b['customers'] < api.actions.playbook.COHORT_MIN:
                self.assertIsNone(b['repeat'])      # too few is unavailable, never a rate


class StackBlindSpotTest(unittest.TestCase):
    """Round 7 feature 8: an app named in the brain stack with no table shows as a "cannot see yet" line."""

    def test_bombas_rebuy(self):
        d = api.handle(Req(['overview']))
        row = next(x for x in d['blind_spots'] if x['key'] == 'upsell_app')
        self.assertIn('Rebuy', row['reason'])
        self.assertIn(row['action_id'], {a['id'] for a in d['plan']})
        self.assertFalse(any(x['key'] == 'loyalty_app' for x in d['blind_spots']))   # the brain names no loyalty app


class MemoTest(unittest.TestCase):
    """Round 7 feature 9: order-row reads run once per window and settings; the rule and the desk share them."""

    def test_shared_and_keyed(self):
        sys.path.insert(0, str(ROOT / 'app'))
        import server
        data = server.Data()
        end = audit.last_full_day(data, None)
        a = audit.welcome(audit.Reader(data, None, end))
        b = audit.welcome(audit.Reader(data, None, end))
        self.assertIs(a, b)
        from datetime import timedelta
        c = audit.welcome(audit.Reader(data, None, end - timedelta(days=7)))
        self.assertIsNot(a, c)
        self.assertEqual(api.actions.rank(None, None, data)['actions'], api.actions.rank(None, None, data)['actions'])


class OneScaleTest(unittest.TestCase):
    """Round 8 feature 1: a brand with no daily aggregate sizes stakes against net revenue from its order rows."""

    def test_sample_uses_money(self):
        sys.path.insert(0, str(ROOT / 'app'))
        import server
        r = api.actions.rank(None, None, server.Data())
        self.assertIsNotNone(r['net_revenue_28d'])
        staked = [a for a in r['actions'] if (a.get('money_at_stake') or {}).get('usd')]
        top = max(staked, key=lambda a: a['money_at_stake']['usd'])
        self.assertEqual(r['actions'][0]['id'], top['id'])     # the biggest stake leads when nothing is critical

    def test_orders_formula(self):
        import datetime as dtm
        orders = [{'created_at': '2026-09-20T10:00:00Z', 'subtotal': 100, 'discount': {'amount': 10}},
                  {'created_at': '2026-09-21T10:00:00Z', 'subtotal': 50, 'discount': None, 'cancelled_at': '2026-09-21'},
                  {'created_at': '2026-07-01T10:00:00Z', 'subtotal': 70, 'discount': None}]
        class R:
            ends_on = dtm.date(2026, 9, 24)
            def table(self, name):
                return orders if name == 'orders' else None
        self.assertEqual(api.model.net_revenue_orders(R(), 28), 90.0)


class ExposureTest(unittest.TestCase):
    """Round 8 feature 2: moves with no counted stake show the 28-day sales they touch; never as money at stake."""

    def test_bombas(self):
        acts = api.actions.rank('bombas')['actions']
        exp = [a for a in acts if a.get('exposure')]
        self.assertTrue(exp)
        for a in exp:
            self.assertIsNone((a.get('money_at_stake') or {}).get('usd'))
            self.assertGreater(a['exposure']['usd_28d'], 0)
            self.assertTrue(a['exposure']['basis'])
        t = next(a for a in exp if a['rule_id'] == 'OFFER-R01')
        rd = audit.Reader(None, 'bombas', audit.last_full_day(None, 'bombas'))
        self.assertEqual(t['exposure']['usd_28d'], round(api.model.window_totals(rd)['net_sales'], 2))


class WeekTest(unittest.TestCase):
    """Round 8 feature 3: the founder's week from the test calendar; team hours unavailable, never guessed."""

    def test_bombas(self):
        d = api.handle(Req(['overview']))
        wk = d['week']
        ready = [t for t in d['tests'] if t['status'] == 'ready' and t['start'] == wk['start']]
        self.assertEqual(wk['approvals'], len(ready))
        ids = {a['id']: a for a in d['plan']}
        self.assertEqual(wk['hours'], sum(ids[i].get('time_to_ship_hours') or 0 for i in wk['moves']))
        self.assertIsNone(wk['team_hours'])
        self.assertTrue(wk['team_reason'])


class UnlocksTest(unittest.TestCase):
    """Round 8 feature 4: the store connect move lists every desk read waiting on order rows."""

    def test_bombas(self):
        a = next(x for x in api.actions.rank('bombas')['actions'] if x['id'].endswith('.connect.shopify'))
        self.assertEqual(len(a['unlocks']), 5)
        self.assertIn('code leaks', a['why'])
        self.assertIn('5 desk reads', a['title'])

    def test_sample_has_rows(self):
        sys.path.insert(0, str(ROOT / 'app'))
        import server
        acts = api.actions.rank(None, None, server.Data())['actions']
        self.assertFalse(any(a.get('unlocks') for a in acts))


class PlanStaggerTest(unittest.TestCase):
    """Round 8 feature 5: the plan keeps rubric order; each testable move shows when it can start and what it waits for."""

    def test_js_and_calendar(self):
        js = (SCREEN / 'screen.js').read_text(encoding='utf-8')
        self.assertIn("'starts ' + fmt.date(t.start)", js)
        r = api.actions.rank('bombas')
        ids = [a['id'] for a in r['actions']]
        self.assertEqual(r['actions'], sorted(r['actions'], key=api.actions.RANK.sort_key))   # order untouched
        for t in r['tests']:
            self.assertIn(t['id'], ids)
            if t['waits_for']:
                self.assertGreater(t['start'], min(x['start'] for x in r['tests']))


class BaselineKindTest(unittest.TestCase):
    """Round 8 feature 6: every evidence row uses an audit.md baseline kind; the exact comparison stays in the window."""

    def test_both_brands(self):
        sys.path.insert(0, str(ROOT / 'app'))
        import server
        for f in audit.run('bombas') + audit.run(None, None, server.Data()):
            for e in f['evidence']:
                self.assertIn(e['baseline_kind'], audit.BASELINE_KINDS + (None,), (f['rule_id'], e))


class MoneyShapeTest(unittest.TestCase):
    """Round 8 feature 7: money at stake carries usd, formula, inputs and window (audit.md section 1) on every rule."""

    def test_builder_refuses_missing_inputs(self):
        import datetime as dtm
        with self.assertRaises(AssertionError):
            audit._finding('OFFER-R36', {'type': 'sku', 'id': 'x', 'label': 'x'}, 'low', [], 's', {'usd': 1, 'formula': 'f', 'window': '28d'},
                           0.5, [], dtm.date(2026, 9, 24))

    def test_both_brands(self):
        sys.path.insert(0, str(ROOT / 'app'))
        import server
        for f in audit.run('bombas') + audit.run(None, None, server.Data()):
            if f['money_at_stake']:
                self.assertLessEqual({'usd', 'formula', 'inputs', 'window'}, set(f['money_at_stake']), f['rule_id'])


class SeverityWordingTest(unittest.TestCase):
    """Round 8 feature 8: audit.md sections 2 and 7. Severity rises with money share; sentences stay short."""

    def test_money_raises_severity(self):
        import datetime as dtm
        mk = lambda usd, sev: {'status': 'open', 'severity': sev, 'money_at_stake': {'usd': usd}}
        out = audit.severity_from_money([mk(60, 'low'), mk(20, 'medium'), mk(5, 'medium'), mk(60, 'critical')], 1000)
        self.assertEqual([f['severity'] for f in out], ['critical', 'high', 'medium', 'critical'])

    def test_sentences(self):
        import re
        sys.path.insert(0, str(ROOT / 'app'))
        import server
        for f in audit.run('bombas') + audit.run(None, None, server.Data()):
            s_ = f['sentence']
            self.assertLess(len(s_.split()), 40, s_)
            self.assertLessEqual(len(re.findall(r'[.!?](?:\s|$)', s_)), 2, s_)
            self.assertNotRegex(s_, r'(?i)\b(should|try|consider)\b')


if __name__ == '__main__':
    unittest.main()
