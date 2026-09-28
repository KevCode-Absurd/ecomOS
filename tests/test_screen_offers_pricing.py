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
        self.assertEqual(d['plan'], [])
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
            self.assertEqual(a['artefact']['draft'], r['spec'])
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
        a = next((a for a in self.out['actions'] if a['rule_id'] == 'OFFER-R13'), None)
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
            self.assertIn('read-only', a['steps'][0]['text'])
            for t in self.g['terms']:
                if t['id'].endswith('offers.guarantee'):
                    self.assertIn(t['text'], a['artefact']['draft'])
        if self.rd.m('returns_by_reason', audit.WINDOW).get('unavailable'):
            self.assertEqual(fs['OFFER-R15']['status'], 'unavailable')


if __name__ == '__main__':
    unittest.main()
