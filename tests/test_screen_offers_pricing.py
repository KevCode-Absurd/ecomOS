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


if __name__ == '__main__':
    unittest.main()
