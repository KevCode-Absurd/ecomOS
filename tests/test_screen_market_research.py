"""Screen 01-market-research: the products metric, audit rules, API shape, and the page on Bombas data.

Synthetic tests build a tiny catalog in memory so the declining-line and review rules are proven to fire
and to stay quiet. The Bombas tests skip when app/data/brands/bombas/data.sqlite has not been built.
"""
import importlib.util
import json
import sys
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / 'app' / 'screens' / '01-market-research'
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


api = load('market_research_api_test', SCREEN / 'api.py')
audit = api.audit
metrics = audit.metrics()


class FakeData:
    """Two lines over 25 months. The store grows 20 percent a year; Tee grows `tee_growth`."""

    def __init__(self, tee_growth=0.2, with_products=True, with_ankle=False):
        self.brand = {'brand': 'fake', 'name': 'Fake', 'as_of': '2026-09-27', 'simulated': True}
        rows = []
        for i in range(25):
            y, m = 2024 + (8 + i) // 12, (8 + i) % 12 + 1
            month = f'{y}-{m:02d}'
            year = 1 if month >= '2025-09' else 0
            sock = round(1000 * (1.2 ** year))
            tee = round(200 * ((1 + tee_growth) ** year))
            rows.append({'month': month, 'sku': 'S-1', 'category': 'socks', 'units': sock, 'net_sales': sock * 10.0})
            rows.append({'month': month, 'sku': 'S-3', 'category': 'socks', 'units': sock, 'net_sales': sock * 25.0})
            rows.append({'month': month, 'sku': 'T-1', 'category': 'tshirts', 'units': tee, 'net_sales': tee * 30.0})
            if with_ankle:
                rows.append({'month': month, 'sku': 'S-9', 'category': 'socks', 'units': 100, 'net_sales': 100 * 12.0})
        self.tables = {'products_monthly': rows}
        if with_products:
            self.tables['products'] = [
                {'sku': 'S-1', 'title': 'Crew Sock', 'category': 'socks', 'price': 10.0, 'items_per_unit': 1},
                {'sku': 'S-3', 'title': 'Crew Sock 3-Pack', 'category': 'socks', 'price': 27.0, 'items_per_unit': 3},
                {'sku': 'T-1', 'title': 'Tee', 'category': 'tshirts', 'price': 30.0, 'items_per_unit': 1}]
            if with_ankle:
                self.tables['products'].append({'sku': 'S-9', 'title': 'Ankle Sock', 'category': 'socks', 'price': 12.0, 'items_per_unit': 1})

    def table(self, name):
        if name not in self.tables:
            raise KeyError(name)
        return self.tables[name]

    def meta(self, name):
        return {'source': 'test', 'captured_at': '2026-09-28T06:00:00Z'}


def review(key, line, total, low, rating=4.5):
    return {'key': key, 'line': line, 'record': f'fake.products.reviews_{key}', 'product': line, 'pdp': None,
            'reviews': total, 'rating': rating, 'low_star': low, 'low_star_share': round(low / total, 4),
            'praise': ['soft'], 'issues': ['hard to pull on', 'rolls down'], 'captured_at': '2026-09-20'}


class MetricTest(unittest.TestCase):
    def test_units_by_line_whole_months(self):
        r = metrics.compute('units', FakeData(), window='92d', end='2026-08-31', by='line')
        self.assertFalse(r['unavailable'])
        self.assertEqual(r['months'], ['2026-06', '2026-07', '2026-08'])
        lines = {g['line']: g for g in r['groups']}
        self.assertEqual(set(lines), {'Crew Sock', 'Tee'})
        self.assertEqual(lines['Crew Sock']['units'], 3 * 2 * 1200)
        self.assertEqual(r['value'], sum(g['units'] for g in r['groups']))

    def test_line_falls_back_to_category(self):
        r = metrics.compute('units', FakeData(with_products=False), window='92d', end='2026-08-31', by='line')
        self.assertEqual({g['line'] for g in r['groups']}, {'socks', 'tshirts'})

    def test_no_whole_month_is_unavailable_not_zero(self):
        r = metrics.compute('product_net_sales', FakeData(), window='10d')
        self.assertTrue(r['unavailable'])
        self.assertIsNone(r['value'])

    def test_missing_table_is_unavailable(self):
        d = FakeData()
        del d.tables['products_monthly']
        self.assertTrue(metrics.compute('units', d, window='92d', end='2026-08-31')['unavailable'])


class RulesTest(unittest.TestCase):
    def check_shape(self, f):
        self.assertEqual(list(f)[:len(AUDIT_KEYS)], AUDIT_KEYS)
        self.assertIn(f['severity'], ('critical', 'high', 'medium', 'low'))
        self.assertTrue(f['id'].startswith('01-market-research.' + f['rule_id'] + '.'))
        for e in f['evidence']:
            self.assertTrue(EVIDENCE_KEYS <= set(e), e)
        if f['money_at_stake'] is None:
            self.assertTrue(f.get('money_reason'))
        else:
            self.assertGreaterEqual(f['money_at_stake']['usd'], 0)
            self.assertTrue(f['money_at_stake']['formula'])

    def test_declining_line_fires_with_money(self):
        fs = [f for f in audit.run(None, data=FakeData(tee_growth=0.05)) if f['rule_id'] == 'PROD-R01']
        self.assertEqual(len(fs), 1)
        f = fs[0]
        self.check_shape(f)
        self.assertEqual(f['entity']['id'], 'tee')
        self.assertIn('losing share', f['sentence'])
        inp = f['money_at_stake']['inputs']
        expect = round(round((inp['store_growth'] - inp['line_growth']) * inp['units_year_ago']) * inp['net_per_unit'])
        self.assertEqual(f['money_at_stake']['usd'], expect)
        self.assertEqual(f['severity'], 'high')  # 3 of 3 months trailed the store

    def test_units_down_says_down(self):
        f = next(f for f in audit.run(None, data=FakeData(tee_growth=-0.3)) if f['rule_id'] == 'PROD-R01')
        self.assertIn('down 30.0 percent', f['sentence'])

    def test_no_false_positive(self):
        self.assertFalse([f for f in audit.run(None, data=FakeData()) if f['rule_id'] == 'PROD-R01'])

    def test_no_brain_makes_review_rule_unavailable(self):
        f = next(f for f in audit.run(None, data=FakeData()) if f['rule_id'] == 'PROD-R02')
        self.assertEqual(f['status'], 'unavailable')
        self.assertEqual(f['evidence'], [])
        self.assertIsNone(f['money_at_stake'])

    def test_review_issue_fires_with_money(self):
        data = FakeData()
        rd = audit.Reader(data, None, date(2026, 9, 27))
        tr = audit.trend(rd)
        reviews = [review('crew', 'Crew Sock', 1000, 40), review('a', None, 1000, 50), review('b', None, 1000, 60),
                   review('tee', 'Tee', 1000, 200, rating=4.0)]
        lads = [{'id': 'fake.objection_ladders.fit', 'theme': 'fit', 'what_works': [], 'what_fails': [], 'one_star': 5,
                 'five_star': 1, 'reviews_records': ['fake.products.reviews_tee'],
                 'rungs': [{'level': 1, 'doubt': 'will it fit', 'one_star': 5, 'five_star': 1, 'proof': False,
                            'from_reviews': ['fake.products.reviews_tee']}]}]
        fs = audit.review_findings(reviews, lads, rd, tr, date(2026, 9, 27), None)
        self.assertEqual([f['entity']['id'] for f in fs], ['tee'])
        f = fs[0]
        self.check_shape(f)
        self.assertIn('fake.objection_ladders.fit', f['brain_refs'])
        self.assertTrue(any(e.get('rung') == 'fit.level_1' for e in f['evidence']))
        inp = f['money_at_stake']['inputs']
        self.assertEqual(inp['net_sales_last_month'], 240 * 30.0)
        self.assertEqual(f['money_at_stake']['usd'], round(inp['net_sales_last_month'] * (0.2 - 0.055)))

    def test_hero_line_without_next_sku_fires(self):
        fs = [f for f in audit.run(None, data=FakeData(with_ankle=True)) if f['rule_id'] == 'PROD-R03']
        self.assertEqual([f['entity']['id'] for f in fs], ['crew-sock'])
        f = fs[0]
        self.check_shape(f)
        self.assertEqual(f['entity']['category'], 'socks')
        self.assertIn('No next SKU for socks', f['sentence'])
        self.assertIsNone(f['money_at_stake'])
        share = next(e for e in f['evidence'] if e['metric'] == 'category_share_net_sales')
        self.assertGreaterEqual(share['value'], 0.25)

    def test_hero_rule_quiet_with_one_line_per_category(self):
        self.assertFalse([f for f in audit.run(None, data=FakeData()) if f['rule_id'] == 'PROD-R03'])

    def test_deterministic(self):
        d = FakeData(tee_growth=0.05)
        self.assertEqual(json.dumps(audit.run(None, data=d)), json.dumps(audit.run(None, data=d)))

    def test_rules_list(self):
        ids = [r['rule_id'] for r in audit.RULES]
        self.assertEqual(ids, sorted(set(ids)))
        self.assertTrue({'PROD-R01', 'PROD-R02', 'PROD-R03', 'PROD-R04', 'PROD-R05'} <= set(ids))
        for r in audit.RULES:
            self.assertEqual(r['owner_screen'], '01-market-research')
            self.assertIn(r['rule_id'], audit.CAPABILITY)

    def test_trend_rules_from_a_web_pass(self):
        """R04 fires when our category trails the market; R05 when a growing lane is sold and not advertised."""
        fx = {'captured_at': '2026-09-28', 'markets': [
            {'key': 'socks_us', 'label': 'US socks', 'size_usd': 9e9, 'size_year': 2025, 'cagr_pct': 30.0, 'direction': 'up',
             'sources': [{'url': 'https://example.org/socks', 'publisher': 'Example', 'date': '2026-01'}]},
            {'key': 'merino_wool_socks', 'label': 'Merino socks', 'size_usd': 4e8, 'cagr_pct': 6.2, 'direction': 'up',
             'sources': [{'url': 'https://example.org/merino', 'publisher': 'Example', 'date': '2026-03'}]},
            {'key': 'compression_socks', 'label': 'Compression', 'size_usd': 2e9, 'cagr_pct': 6.1, 'direction': 'up', 'sources': []},
            {'key': 'slippers_us', 'label': 'Slippers', 'size_usd': None, 'cagr_pct': 1.0, 'direction': 'flat', 'sources': []}]}
        real = audit.market_trends
        audit.market_trends = lambda: fx
        try:
            class B:
                brand = 'fake'
                def records(self, sec):
                    if sec == 'products':
                        return [{'text': 'merino wool calf sock, compression sock, slipper', 'value': None, 'source': {}, 'evidence': []}]
                    if sec == 'learnings':
                        return [{'text': 'active ads: compression socks', 'value': {'role': 'self'}, 'source': {'type': 'ad_library'}, 'evidence': []}]
                    return []
            data = FakeData()
            rd = audit.Reader(data, None, date(2026, 9, 27))
            mix = audit.category_mix(data, None, rd)
            fs = audit.trend_findings(B(), mix, date(2026, 9, 27))
        finally:
            audit.market_trends = real
        by = {f['id']: f for f in fs}
        r04 = by['01-market-research.PROD-R04.socks']
        self.assertEqual(r04['money_at_stake']['formula'], '(market_cagr - our_growth) * our_net_sales_12m')
        self.assertGreater(r04['money_at_stake']['usd'], 0)
        self.assertIn('01-market-research.PROD-R05.merino_wool_socks', by)      # sold, growing, not advertised
        self.assertNotIn('01-market-research.PROD-R05.compression_socks', by)   # sold and advertised
        self.assertNotIn('01-market-research.PROD-R05.slippers_us', by)         # not growing
        for f in fs:
            self.check_shape(f)

    def test_lane_rule_from_competitor_signals(self):
        """R06 fires for a lane 2 competitors push with a long runner that we do not advertise; quiet when advertised."""
        class B:
            brand = 'fake'
            def records(self, sec):
                if sec == 'competitors':
                    return [{'id': 'fake.competitors.a', 'value': {'name': 'A', 'active_ads_seen': 40, 'positioning': 'merino socks with a lifetime guarantee',
                                                                   'hook_types': ['lifetime guarantee'], 'longest_running_ad': {'days_running': 90}}, 'evidence': []},
                            {'id': 'fake.competitors.b', 'value': {'page': 'B', 'active_ads': 20, 'longest_run_days': 45, 'hook_types': {'statement': 20}}, 'evidence': [{'quote': 'merino wool all day'}]},
                            {'id': 'fake.competitors.c', 'value': {'page': 'C', 'active_ads': 5, 'longest_run_days': 3, 'hook_types': {'statement': 5}}, 'evidence': [{'quote': 'new arrival style-led'}]}]
                if sec == 'products':
                    return [{'text': 'merino wool calf sock', 'value': None, 'source': {}, 'evidence': []}]
                if sec == 'learnings':
                    return [{'text': 'active ads: compression socks and a guarantee hook', 'value': {'role': 'self'}, 'source': {'type': 'ad_library'}, 'evidence': []}]
                return []
        real = audit.market_trends
        audit.market_trends = lambda: {'launches': []}
        try:
            rows = {r['key']: r for r in audit.subcategory_table(B(), date(2026, 9, 27))}
            fs = audit.subcategory_findings(B(), date(2026, 9, 27))
        finally:
            audit.market_trends = real
        self.assertEqual(rows['merino']['verdict'], 'follow')
        self.assertEqual(rows['style']['verdict'], 'ignore')      # one page, 3-day ads, no launch
        self.assertEqual(rows['guarantee']['verdict'], 'watch')   # one page pushes it
        ids = [f['id'] for f in fs]
        self.assertEqual(ids, ['01-market-research.PROD-R06.merino'])
        self.assertIn('2 competitors push merino and wool', fs[0]['sentence'])
        self.check_shape(fs[0])

    def test_rank_merges_market_and_competitor_lane(self):
        acts = api.rank('bombas', {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4})['actions']
        merged = [a for a in acts if len(a['finding_ids']) > 1]
        for a in merged:
            rules = {fid.split('.')[1] for fid in a['finding_ids']}
            self.assertEqual(rules, {'PROD-R05', 'PROD-R06'})
        covered = [fid for a in acts for fid in a['finding_ids']]
        self.assertEqual(len(covered), len(set(covered)))   # one action per finding

    def test_conversation_rule_from_ladders(self):
        """R07 fires for a complaint-led theme with no ad answer; a praise-led theme is a strength, not a finding."""
        class B:
            brand = 'fake'
            def records(self, sec):
                if sec == 'objection_ladders':
                    return [{'id': 'fake.objection_ladders.durability', 'field': 'durability', 'value': {'theme': 'durability',
                             'counts': {'one_star': 30, 'five_star': 5, 'sources': {'own_site': 20, 'amazon': 15}},
                             'rungs': [{'level': 1, 'doubt': 'will it get a hole', 'counts': {'one_star': 30}, 'proof': 'guarantee'}]}},
                            {'id': 'fake.objection_ladders.comfort_and_feel', 'field': 'comfort_and_feel', 'value': {'theme': 'comfort_and_feel',
                             'counts': {'one_star': 2, 'five_star': 40, 'sources': {'own_site': 42}}, 'rungs': []}}]
                if sec == 'claims':
                    return [{'text': 'a guarantee that replaces a pair that fails', 'value': None, 'source': {}, 'evidence': []}]
                if sec == 'learnings':
                    return [{'text': 'active ads: comfort you notice', 'value': {'role': 'self'}, 'source': {'type': 'ad_library'}, 'evidence': []}]
                return []
        rows = {r['theme']: r for r in audit.conversation(B())['rows']}
        self.assertEqual(rows['durability']['verdict'], 'gap')
        self.assertTrue(rows['durability']['answered_on_site'])
        self.assertFalse(rows['durability']['answered_in_ads'])
        self.assertEqual(rows['durability']['by_source'], {'own_site': 20, 'amazon': 15})
        self.assertEqual(rows['comfort']['verdict'], 'strength')
        fs = audit.conversation_findings(B(), date(2026, 9, 27))
        self.assertEqual([f['id'] for f in fs], ['01-market-research.PROD-R07.durability'])
        self.assertIn('30 complaint quotes against 5 praise', fs[0]['sentence'])
        self.assertIn('will it get a hole', fs[0]['sentence'])
        self.check_shape(fs[0])

    def test_social_pull_stores_no_usernames(self):
        import importlib.util as iu
        spec = iu.spec_from_file_location('social_pull_t', SCREEN / 'social_pull.py')
        sp = iu.module_from_spec(spec)
        spec.loader.exec_module(sp)
        items = [{'caption': 'Love these socks @someone, so comfortable', 'hashtags': ['socks', 'comfy'], 'likesCount': 10, 'commentsCount': 2,
                  'timestamp': '2026-09-01T00:00:00Z', 'url': 'https://www.instagram.com/p/x/', 'type': 'Image', 'hashtag': 'socks',
                  'ownerUsername': 'secret_person', 'ownerId': '123', 'ownerFullName': 'Secret Person'}]
        out = sp.summarise(items, ['socks'], {'mode': 'mock'})
        dump = json.dumps(out)
        self.assertNotIn('secret_person', dump)
        self.assertNotIn('Secret Person', dump)
        self.assertNotIn('@someone', dump)
        self.assertEqual(out['themes']['comfort']['posts'], 1)
        self.assertEqual(out['co_hashtags'], [['comfy', 1]] if isinstance(out['co_hashtags'][0], list) else [('comfy', 1)])
        fx = json.loads((SCREEN / 'fixtures' / 'social_pull.json').read_text(encoding='utf-8'))

        def keys(o):
            if isinstance(o, dict):
                for k, v in o.items():
                    yield k.lower()
                    yield from keys(v)
            elif isinstance(o, list):
                for v in o:
                    yield from keys(v)
        self.assertFalse([k for k in keys(fx) if 'owner' in k or 'user' in k])
        self.assertIn(fx['mode'], ('mock', 'live'))

    def test_preference_rule_needs_a_rival_claim_and_no_record(self):
        fx = {'preferences': [
            {'key': 'made_in_usa', 'label': 'Made in USA', 'direction': 'flat', 'evidence': '75 pct prefer US made', 'sources': [{'url': 'https://example.org/u', 'publisher': 'Example', 'date': '2025-06'}]},
            {'key': 'durability', 'label': 'Durability', 'direction': 'up', 'evidence': '47 pct define quality by durability', 'sources': [{'url': 'https://example.org/d', 'publisher': 'Example', 'date': '2026-03'}]},
            {'key': 'secondhand_resale', 'label': 'Resale', 'direction': 'up', 'evidence': 'resale grew 14 pct', 'sources': [{'url': 'https://example.org/r', 'publisher': 'Example', 'date': '2025-03'}]}]}
        real = audit.market_trends
        audit.market_trends = lambda: fx
        try:
            class B:
                brand = 'fake'
                def records(self, sec):
                    if sec == 'competitors':
                        return [{'id': 'fake.competitors.a', 'value': {'name': 'A', 'active_ads_seen': 10, 'positioning': 'made in usa merino with a lifetime guarantee',
                                                                       'longest_running_ad': {'days_running': 50}}, 'evidence': []}]
                    if sec == 'claims':
                        return [{'text': 'a guarantee that replaces a pair that fails', 'value': None, 'source': {}, 'evidence': []}]
                    if sec == 'learnings':
                        return [{'text': 'active ads: comfort', 'value': {'role': 'self'}, 'source': {'type': 'ad_library'}, 'evidence': []}]
                    return []
            rows = {r['key']: r for r in audit.preferences(B())}
            fs = audit.preference_findings(B(), date(2026, 9, 27))
        finally:
            audit.market_trends = real
        self.assertEqual(rows['made_in_usa']['verdict'], 'gap')
        self.assertEqual(rows['durability']['verdict'], 'prove')
        self.assertEqual(rows['secondhand_resale']['verdict'], 'watch')
        self.assertEqual([f['id'] for f in fs], ['01-market-research.PROD-R08.made_in_usa'])
        self.assertIn('A claim it and no record of ours does', fs[0]['sentence'])
        self.check_shape(fs[0])

    def test_web_pass_fixture_cites_every_number(self):
        fx = audit.market_trends()
        self.assertIsNotNone(fx)
        for m in fx['markets']:
            if m.get('size_usd') is not None or m.get('cagr_pct') is not None:
                self.assertTrue(m['sources'] and all(s.get('url') and s.get('date') for s in m['sources']), m['key'])
        for p in fx['preferences'] + fx['launches']:
            self.assertTrue(p['sources'] and all(s.get('url') for s in p['sources']))
        self.assertNotIn('\u2014', json.dumps(fx))


class RankTest(unittest.TestCase):
    """depth.md rules 2, 3 and 13 on this screen's rank(): owner, steps, artefact, every finding mapped, deterministic."""

    def actions(self):
        return api.rank('bombas', {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4})['actions']

    def test_every_finding_maps_to_a_valid_action(self):
        findings = [f for f in audit.run('bombas', {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4}) if f['status'] in ('open', 'unavailable')]
        acts = self.actions()
        covered = {fid for a in acts for fid in a['finding_ids']}
        for f in findings:
            self.assertIn(f['id'], covered, f['id'])
        for a in acts:
            self.assertEqual(api.rank_mod.validate_action(a), [], a['id'])
            self.assertIn(a['owner'], ('agent', 'agent_drafts', 'person'))
            self.assertTrue(2 <= len(a['steps']) <= 8)
            self.assertTrue(all(s['who'] in ('agent', 'agent_drafts', 'person') for s in a['steps']))
            self.assertIn(a['artefact']['kind'], api.rank_mod.ARTEFACT_KINDS)
            self.assertNotIn('\u2014', a['title'] + a['why'] + ' '.join(s['text'] for s in a['steps']))
            if a['status'] == 'unavailable':
                self.assertEqual(a['owner'], 'person')
                self.assertEqual(a['artefact']['kind'], 'connector_setup')

    def test_recipes_carry_real_steps(self):
        for a in self.actions():
            if a['status'] == 'unavailable':
                continue
            self.assertNotIn('Read the evidence rows', a['steps'][0]['text'], a['id'])   # not the engine default
            self.assertTrue(a.get('stop_rule') or a.get('win_rule'), a['id'])
            self.assertTrue(a['artefact']['label'])

    def test_deterministic_order(self):
        a = [x['id'] for x in self.actions()]
        b = [x['id'] for x in self.actions()]
        self.assertEqual(a, b)


class Req:
    def __init__(self, path, brand='bombas', method='GET'):
        self.method, self.path, self.query, self.data = method, path, {'brand': [brand]}, None

    def arg(self, name, default=None):
        v = self.query.get(name)
        return v[0] if v else default


class ApiTest(unittest.TestCase):
    def test_read_only_and_bad_brand(self):
        self.assertEqual(api.handle(Req(['overview'], method='POST'))[0], 405)
        self.assertEqual(api.handle(Req(['overview'], brand='../x'))[0], 400)
        self.assertEqual(api.handle(Req(['nope']))[0], 404)

    def test_competitor_band_parsing(self):
        class B:
            def records(self, section):
                return [{'id': 'x.competitors.a', 'value': {'name': 'A', 'price_band_usd': '12 to 25 per pair, median about 18'}},
                        {'id': 'x.competitors.b', 'value': {'name': 'B', 'price_band_usd': 'from 18 per pair, median 25'}},
                        {'id': 'x.competitors.set', 'value': ['A', 'B']}]
        c = api.competitor_bands(B())
        self.assertEqual([(x['low'], x['high'], x['median']) for x in c], [(12.0, 25.0, 18.0), (18.0, None, 25.0)])

    def test_price_position(self):
        comps = [{'median': 18.0}, {'median': 32.0}]
        rows = {r['line']: r for r in api.price_bands(FakeData().tables['products'], comps)['rows']}
        self.assertEqual(rows['Crew Sock']['position'], 'below')
        self.assertIsNone(rows['Tee']['position'])  # no competitor for tees


@unittest.skipUnless(BOMBAS_DB.is_file(), 'bombas data.sqlite not built')
class BombasTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.o = api.handle(Req(['overview']))

    def test_simulated_and_three_tiles(self):
        o = self.o
        self.assertTrue(o['brand']['simulated'])
        self.assertEqual(set(o['tiles']), {'units', 'losing', 'rating'})
        for t in o['tiles'].values():
            self.assertIsNotNone(t['value'])

    def test_two_insights_one_chart(self):
        o = self.o
        self.assertEqual(len(o['insights']), 2)
        for i in o['insights']:
            self.assertTrue(i['rule'] and i['sentence'])
            self.assertNotIn('—', i['sentence'])
        self.assertEqual(len(o['chart']['labels']), 12)
        self.assertLessEqual(len(o['chart']['series']), 6)

    def test_findings_have_decline_and_review_with_money(self):
        fs = self.o['findings']
        rules = {f['rule_id'] for f in fs if f['status'] == 'open' and f['money_at_stake']}
        self.assertEqual(rules, {'PROD-R01', 'PROD-R02'})
        for f in fs:
            self.assertEqual(list(f)[:len(AUDIT_KEYS)], AUDIT_KEYS)
        r2 = next(f for f in fs if f['rule_id'] == 'PROD-R02')
        self.assertTrue(any('.objection_ladders.' in b for b in r2['brain_refs']))

    def test_demand_prices_reviews_pipeline(self):
        o = self.o
        self.assertEqual(len(o['demand']), 19)  # the 25 finance SKUs roll up to 19 lines by title (S2.3c)
        self.assertTrue(o['price_bands']['band'])
        self.assertTrue(o['reviews'] and all(r['works'] is not None for r in o['reviews']))
        self.assertEqual(o['pipeline']['rows'], [])
        self.assertTrue(o['pipeline']['gate_rule'])

    def test_page_says_simulated(self):
        js = (SCREEN / 'screen.js').read_text(encoding='utf-8')
        self.assertIn('simulated data', js)
        self.assertNotIn('—', js)


if __name__ == '__main__':
    unittest.main()
