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


class ShapeMixin:
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


class RulesTest(ShapeMixin, unittest.TestCase):
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

    def test_proof_share_and_our_price(self):
        self.assertEqual(audit.proof_share(['lifetime guarantee', 'new arrivals', '5 star review quote', 'gift']), 0.5)
        self.assertIsNone(audit.proof_share([]))
        self.assertEqual(audit.proof_share({'statement': 20, 'first_person': 1}), 0.0)
        prods = FakeData().tables['products']
        self.assertEqual(audit.our_price_per_pair(prods, None)['value'], 9.5)   # median of 10 and 9 per pair

    def test_positioning_rule_on_bombas_brain(self):
        """On the public Bombas brain the frame is buy it for life, Darn Tough is recommended instead, and our proof share trails."""
        br = audit.brain('bombas')
        if br is None:
            self.skipTest('no bombas brain')
        m = audit.positioning_map(br, None)
        self.assertTrue(m['enough'])
        self.assertTrue(any(p['us'] for p in m['points']))
        self.assertTrue(all(p['x'] is not None and p['y'] is not None for p in m['points']))
        self.assertTrue(all(p['x'] is None or p['y'] is None for p in m['unpriced']))
        fs = audit.positioning_findings(br, None, date(2026, 9, 27))
        self.assertEqual([f['id'] for f in fs], ['01-market-research.PROD-R09.brand'])
        self.assertEqual(fs[0]['severity'], 'high')
        self.assertIn('recommended instead', fs[0]['sentence'])
        self.check_shape(fs[0])

    def test_avatar_theme_and_words(self):
        v = {'job': 'socks that survive a season before holes start', 'pains': ['holes in the heel', 'shedding and pilling'], 'triggers': ['a hole after weeks']}
        self.assertEqual(audit.avatar_theme(v), 'durability')
        self.assertEqual(audit.avatar_theme({'job': 'proof it is worth more than a cheaper multi-pack', 'pains': ['paying a premium'], 'triggers': []}), 'price_value')
        self.assertIsNone(audit.avatar_theme({'job': '', 'pains': [], 'triggers': []}))
        w = audit.avatar_words(v)
        self.assertIn('holes', w)
        self.assertNotIn('socks', w)

    def test_avatar_rules_on_bombas_brain(self):
        br = audit.brain('bombas')
        if br is None:
            self.skipTest('no bombas brain')
        cov = audit.avatar_coverage(br)
        self.assertTrue(cov['rows'] and cov['cols'])
        for r in cov['rows']:
            self.assertEqual(r['not_served'], r['lines_us'] == 0)
        fs = audit.avatar_findings(br, date(2026, 9, 27), 28640586.4)
        r11 = [f for f in fs if f['rule_id'] == 'PROD-R11']
        self.assertTrue(r11)
        for f in r11:
            self.check_shape(f)
            self.assertNotEqual(f['severity'], 'critical')
            if f['money_at_stake']:
                inp = f['money_at_stake']['inputs']
                self.assertEqual(f['money_at_stake']['usd'], round(inp['share_estimate'] * inp['net_revenue_28d'] * inp['complaint_share_of_theme'] * inp['repeat_rate_12m']))
        self.assertIsNone(next((f for f in fs if f['rule_id'] == 'PROD-R11' and f['money_at_stake'] is None and not f.get('money_reason')), None))
        no_net = audit.avatar_findings(br, date(2026, 9, 27), None)
        self.assertTrue(all(f['money_at_stake'] is None and f['money_reason'] for f in no_net if f['rule_id'] == 'PROD-R11'))

    def test_search_groups_and_demand(self):
        """Groups come from the brain; demand sums Search Console rows per group; R13 fires for demand with no page."""
        br = audit.brain('bombas')
        if br is None:
            self.skipTest('no bombas brain')
        groups, questions = audit.search_groups(br)
        self.assertEqual([g['key'] for g in groups], ['brand', 'category', 'competitor', 'problem'])
        self.assertIn('bombas', groups[0]['terms'])
        self.assertEqual(audit.group_of('bombas vs darn tough', groups), 'brand')
        self.assertEqual(audit.group_of('darn tough socks', groups), 'competitor')
        self.assertEqual(audit.group_of('socks holes in heel', groups), 'problem')
        self.assertEqual(audit.group_of('merino socks', groups), 'category')
        data = FakeData()
        data.tables['search_console'] = [
            {'date': '2026-09-20', 'query': 'bombas socks', 'page': '/', 'clicks': 40, 'impressions': 400, 'position': 1.2},
            {'date': '2026-09-21', 'query': 'darn tough vs bombas', 'page': '/', 'clicks': 5, 'impressions': 300, 'position': 8.0},
            {'date': '2026-06-01', 'query': 'old query socks', 'page': '/', 'clicks': 999, 'impressions': 9999, 'position': 1.0}]
        demand, avail = audit.search_demand(data, None, groups, date(2026, 9, 27))
        self.assertTrue(avail['organic'] and not avail['paid'])
        self.assertEqual(demand['brand']['impressions'], 700)     # the versus query names the brand, so it is brand
        self.assertEqual(demand['brand']['clicks'], 45)
        self.assertIsNone(demand['category']['impressions'] if demand['category']['queries'] else None)
        self.assertIsNone(demand['brand']['paid_spend'])
        real_bd = audit.brand_data
        audit.brand_data = lambda b: data
        try:
            t = audit.search_table(br, data, 'x', date(2026, 9, 27))
            fs = audit.search_findings(br, data, 'x', date(2026, 9, 27))
        finally:
            audit.brand_data = real_bd
        self.assertEqual([f['rule_id'] for f in fs], [])   # brand group has pages in the site map
        self.assertTrue(t['groups'][0]['pages'])

    def test_search_unavailable_is_a_connect_finding(self):
        fs = [f for f in audit.run('bombas') if f['rule_id'] in ('PROD-R12', 'PROD-R13')]
        if not fs:
            self.skipTest('search data connected')
        self.assertEqual(fs[0]['status'], 'unavailable')
        self.assertEqual(fs[0]['unavailable']['connector'], 'google_search_console')
        a = next(a for a in api.rank('bombas', {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4})['actions'] if a['rule_id'] == 'PROD-R12')
        self.assertEqual(a['owner'], 'person')
        self.assertTrue(a['title'].startswith('Connect Search Console'))

    def test_falling_behind_ranks_money_then_reach(self):
        f1 = {'id': 'x.PROD-R11.a', 'rule_id': 'PROD-R11', 'status': 'open', 'entity': {'id': 'a', 'label': 'A'}, 'sentence': 's', 'severity': 'high', 'confidence': 0.5,
              'money_at_stake': {'usd': 100, 'formula': 'f'}, 'evidence': [], 'capability': {'id': 'PROD-C12', 'autonomy': 'human_assist'}}
        f2 = dict(f1, id='x.PROD-R09.brand', rule_id='PROD-R09', entity={'id': 'brand', 'label': 'Positioning'}, money_at_stake=None, money_reason='none',
                  evidence=[{'metric': 'frame_mentions', 'value': 9}, {'metric': 'recommended_instead', 'value': 4, 'upvotes': 188}])
        f3 = dict(f1, id='x.PROD-R11.b', rule_id='PROD-R11', entity={'id': 'b', 'label': 'B'}, money_at_stake={'usd': 500, 'formula': 'f'})
        f4 = dict(f1, id='x.PROD-R01.c', rule_id='PROD-R01', entity={'id': 'c', 'label': 'C'})   # not a positioning or avatar rule
        cov = {'rows': [{'key': 'a', 'share': 0.1, 'served_by': []}, {'key': 'b', 'share': 0.2, 'served_by': []}]}
        b = api.falling_behind([f1, f2, f3, f4], cov, [{'label': 'Durability', 'verdict': 'prove'}], {'members': {'bl': ['Bombas']}, 'ours': {'label': 'Bombas'}}, 10000)
        self.assertEqual([r['finding_id'] for r in b['rows']], ['x.PROD-R11.b', 'x.PROD-R11.a', 'x.PROD-R09.brand'])
        self.assertEqual(b['stake_usd'], 600)
        self.assertEqual(b['stake_share_of_net_28d'], 0.06)
        self.assertEqual(b['rows'][2]['reach'], '9 Reddit posts, 188 upvotes on the recommendation instead')
        self.assertEqual(b['counts'], {'positioning': 1, 'avatar': 2})
        self.assertEqual(b['quadrant'], 'bl')
        self.assertEqual(b['prove'], ['Durability'])

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

    def test_rubric_overrides_from_the_audit_docstring(self):
        acts = {a['rule_id']: a for a in self.actions()}
        if 'PROD-R09' in acts:
            self.assertEqual(acts['PROD-R09']['rubric']['reputation'], 5)
        if 'PROD-R11' in acts:
            self.assertGreaterEqual(acts['PROD-R11']['rubric']['satisfaction'], 4)
        for a in self.actions():
            r = a['rubric']
            total = round(sum(api.rank_mod.WEIGHTS[k] * (r[k] if r[k] is not None else 2.5) / 5 for k in api.rank_mod.WEIGHTS), 1)
            self.assertEqual(r['total'], total, a['id'])
            self.assertEqual(r['ease'], {'agent': 5, 'agent_drafts': 4, 'person': 3}[a['owner']] if a['status'] != 'unavailable' else 1)

    def test_every_rule_has_a_recipe_or_a_connect_action(self):
        """depth.md rule 2 on every rule id the audit declares, on synthetic findings where Bombas does not fire them."""
        for rule in audit.RULES:
            f = {'id': f'01-market-research.{rule["rule_id"]}.x', 'screen': '01-market-research', 'rule_id': rule['rule_id'], 'severity': 'medium',
                 'entity': {'type': rule['entity_type'], 'id': 'x', 'label': 'X (product line)', 'category': 'socks'}, 'evidence': [], 'sentence': 's',
                 'capability': dict(audit.CAPABILITY[rule['rule_id']]), 'money_at_stake': None, 'money_reason': 'test', 'confidence': 0.5, 'brain_refs': [],
                 'first_seen': '2026-09-27', 'last_seen': '2026-09-27', 'status': 'open', 'unavailable': None}
            r = api.recipe(f)
            if rule['rule_id'] in ('PROD-R12', 'PROD-R17'):
                self.assertIsNone(r)   # a connect rule: the engine's connect action, retitled in rank
                continue
            self.assertIsNotNone(r, rule['rule_id'])
            self.assertTrue(2 <= len(r['steps']) <= 8, rule['rule_id'])
            self.assertIn(r['artefact']['kind'], api.rank_mod.ARTEFACT_KINDS, rule['rule_id'])
            self.assertIn(r['owner'], ('agent', 'agent_drafts', 'person'))
            self.assertTrue(r.get('stop_rule') and r.get('win_rule') and r.get('check_on'), rule['rule_id'])

    def test_deterministic_order(self):
        a = [x['id'] for x in self.actions()]
        b = [x['id'] for x in self.actions()]
        self.assertEqual(a, b)


class PipelineTest(ShapeMixin, unittest.TestCase):
    """The one thing this screen writes: candidates. Rules R14 and R15 read them."""

    def setUp(self):
        import tempfile
        self.tmp = Path(tempfile.mkdtemp()) / 'pipeline.json'
        self.real = audit.PIPELINE_PATH
        audit.PIPELINE_PATH = self.tmp

    def tearDown(self):
        audit.PIPELINE_PATH = self.real

    def test_add_advance_hours_kill_round_trip(self):
        today = date(2026, 9, 28)
        code, out = api.candidate_add('fake', {'name': 'Kids gift pack', 'category': 'socks', 'planned_price': '29.5', 'time_box_days': 7, 'who': 'person'}, today)
        self.assertEqual(code, 201)
        cid = out['candidate']['candidate_id']
        self.assertEqual(out['candidate']['stage'], 'screened')
        self.assertEqual(out['candidate']['planned_price'], 29.5)
        self.assertEqual(api.candidate_update('fake', cid, {'stage': 'nope'}, today)[0], 400)
        r = api.candidate_update('fake', cid, {'stage': 'researched', 'hours_add': 2.5, 'screen_result': {'demand': 'pass', 'competition': 'fail', 'store_fit': 'fail'}}, today)
        self.assertEqual(r['candidate']['stage'], 'researched')
        self.assertEqual(r['candidate']['hours_logged'], 2.5)
        self.assertEqual(len(r['candidate']['log']), 2)
        rows = audit.pipeline('fake')
        self.assertEqual([x['candidate_id'] for x in rows], [cid])
        fs = audit.pipeline_findings('fake', date(2026, 10, 10))
        self.assertEqual(sorted(f['rule_id'] for f in fs), ['PROD-R14', 'PROD-R15'])   # 12 days on a 7-day box, 2 checks failed
        for f in fs:
            self.assertTrue(f['id'].endswith(cid))
        api.candidate_update('fake', cid, {'stage': 'killed'}, today)
        self.assertEqual(audit.pipeline_findings('fake', date(2026, 10, 10)), [])
        self.assertEqual(api.candidate_update('fake', 'cand-999', {'stage': 'go'}, today)[0], 404)
        self.assertEqual(api.candidate_add('fake', {'name': ''}, today)[0], 400)

    def test_margin_gate_arithmetic_and_floor(self):
        """Every term named; the margin is the arithmetic of the steps; below the floor fires R16."""
        rows = [{'field': 'cogs_landed', 'scope': 'sku', 'scope_key': 'BMB-SK-X-1', 'value': 4.0, 'unit': 'usd_per_unit', 'effective_from': '2025-01-01', 'effective_to': None},
                {'field': 'cogs_landed', 'scope': 'sku', 'scope_key': 'BMB-SK-X-4', 'value': 14.0, 'unit': 'usd_per_unit', 'effective_from': '2025-01-01', 'effective_to': None},
                {'field': 'shipping_label', 'scope': 'carrier_zone', 'scope_key': 'usps:zones_1_4', 'value': 4.0, 'unit': 'usd_per_order', 'effective_from': '2025-01-01', 'effective_to': None},
                {'field': 'packaging', 'scope': 'global', 'scope_key': '', 'value': 1.0, 'unit': 'usd_per_order', 'effective_from': '2025-01-01', 'effective_to': None},
                {'field': 'threepl_pick_pack', 'scope': 'global', 'scope_key': '', 'value': 3.0, 'unit': 'usd_per_order', 'effective_from': '2025-01-01', 'effective_to': None},
                {'field': 'payment_fee_percent', 'scope': 'channel', 'scope_key': 'online_store', 'value': 3.0, 'unit': 'percent', 'effective_from': '2025-01-01', 'effective_to': None},
                {'field': 'payment_fee_fixed', 'scope': 'channel', 'scope_key': 'online_store', 'value': 0.3, 'unit': 'usd_per_order', 'effective_from': '2025-01-01', 'effective_to': None},
                {'field': 'target_contribution_margin', 'scope': 'global', 'scope_key': '', 'value': 25.0, 'unit': 'percent', 'effective_from': '2025-01-01', 'effective_to': None}]
        fin = metrics.finance.Finance(rows)
        cand = {'name': 'Test sock', 'category': 'socks', 'planned_price': 20.0, 'pack_units': 1}
        g = audit.margin_gate(cand, fin, None, '2026-09-27', 2.0, 25.0)
        self.assertFalse(g['unavailable'])
        self.assertEqual(g['cogs']['value'], 4.0)          # the single-unit SKU, not the 4-pack
        steps = {s['label']: s['value'] for s in g['steps']}
        self.assertEqual(steps['fulfilment'], 4.0)          # (4 + 1 + 3) over 2 units an order
        self.assertEqual(steps['payment fee'], 0.75)        # 3 percent of 20 plus 0.30 over 2 units
        self.assertEqual(g['contribution_usd'], round(20 - 4 - 4 - 0.75, 2))
        self.assertEqual(g['margin_pct'], round((20 - 4 - 4 - 0.75) / 20 * 100, 1))
        self.assertTrue(g['passes_floor'])
        g2 = audit.margin_gate(dict(cand, planned_price=10.0, cogs_estimate=5.0), fin, None, '2026-09-27', 2.0, 25.0)
        self.assertFalse(g2['passes_floor'])
        self.assertEqual(g2['cogs']['basis'], 'entered on the candidate')
        g3 = audit.margin_gate(dict(cand, planned_price=None), fin, None, '2026-09-27', 2.0, 25.0)
        self.assertTrue(g3['unavailable'])
        g4 = audit.margin_gate(dict(cand, pack_units=4), fin, None, '2026-09-27', 2.0, 25.0)
        self.assertEqual(g4['cogs']['value'], 16.0)

    def test_saturation_ladder_and_lane_map(self):
        self.assertEqual([audit.saturation_grade(n) for n in (0, 1, 2, 4, 5, 9)], ['green', 'green', 'amber', 'amber', 'red', 'red'])
        br = audit.brain('bombas')
        if br is None:
            self.skipTest('no bombas brain')
        m = audit.lane_map(br, date(2026, 9, 27))
        by = {p['key']: p for p in m['points']}
        for p in m['points']:
            self.assertEqual(p['x'], p['competitors_n'] + p['launches_theirs'])
            if p['y'] is not None:
                self.assertTrue(-1 <= p['y'] <= 1)
        fs = audit.lane_map_findings(br, date(2026, 9, 27))
        for f in fs:
            self.check_shape(f)
            self.assertEqual(f['severity'], 'low')
            self.assertNotIn(f['entity']['id'], audit.PROOF_LANES)
            self.assertGreaterEqual(by[f['entity']['id']]['x'], audit.SATURATION_FULL)
            self.assertGreaterEqual(by[f['entity']['id']]['y'], audit.TREND_UP)

    def test_spend_signal_bands_and_rule(self):
        self.assertEqual([audit.run_band(d) for d in (0, 13, 14, 29, 30, 89, 90, 343, None)],
                         ['under 14 days', 'under 14 days', '14 to 29 days', '14 to 29 days', '30 to 89 days', '30 to 89 days', '90 days or more', '90 days or more', None])
        br = audit.brain('bombas')
        if br is None:
            self.skipTest('no bombas brain')
        sp = audit.spend_signal(br, 'bombas', date(2026, 9, 27))
        for r in sp['rows']:
            self.assertEqual(sum(r['bands'].values()), len([1 for _ in r['funded']]) + (r['bands']['under 14 days'] + r['bands']['14 to 29 days'] + r['bands']['30 to 89 days']))
            if r['verdict'] == 'funded':
                self.assertGreaterEqual(len(r['funded']), audit.FUNDED_MIN_ADVERTISERS)
        fs = audit.spend_findings(br, 'bombas', date(2026, 9, 27))
        for f in fs:
            self.check_shape(f)
            row = next(r for r in sp['rows'] if r['key'] == f['entity']['id'])
            self.assertEqual(row['verdict'], 'funded')
            self.assertEqual(row['candidates'], [])
            self.assertNotEqual(row['kind'], 'proof')

    def test_candidate_lanes_from_name_and_angle(self):
        self.real2 = audit.PIPELINE_PATH
        try:
            audit.PIPELINE_PATH = self.tmp
            self.tmp.write_text(json.dumps({'rows': [{'candidate_id': 'a', 'brand': 'fake', 'name': 'Merino hiking sock', 'stage': 'screened', 'angle_text': ''},
                                                     {'candidate_id': 'b', 'brand': 'fake', 'name': 'x', 'stage': 'killed', 'angle_text': 'compression'}]}), encoding='utf-8')
            lanes = audit.candidate_lanes('fake')
        finally:
            audit.PIPELINE_PATH = self.real2
        self.assertEqual(lanes.get('merino'), ['Merino hiking sock'])
        self.assertEqual(lanes.get('performance'), ['Merino hiking sock'])
        self.assertNotIn('compression', lanes)   # killed candidates do not count

    def test_review_price_signal_reads_per_pair_only(self):
        class B:
            brand = 'fake'
            def records(self, sec):
                if sec != 'language_bank':
                    return []
                mk = lambda src, q, star=1: {'id': 'fake.language_bank.' + src, 'value': {'reviews': [{'source': src, 'star': star, 'quote': q, 'url': 'u'}]}}
                return [mk('amazon', 'One pair of socks for $30 is way overpriced.'),
                        mk('own_site_yotpo', 'For $10 a pair, you would hope for better socks.'),
                        mk('amazon', 'Came to over $50 for the package of 4 socks.'),          # a pack, not a pair
                        mk('reddit', 'the $30 pair from walmart are not the same', None),     # Reddit is left out
                        mk('amazon', 'shipping cost an additional $25 for the socks')]         # no pair in the words around it
        sig = audit.review_price_signal(B())
        self.assertEqual(sig['n'], 2)
        self.assertEqual(sig['median_per_pair'], 20.0)
        self.assertEqual(sig['by_source'], {'amazon': 1, 'own': 1})
        self.real3 = audit.PIPELINE_PATH
        try:
            audit.PIPELINE_PATH = self.tmp
            self.tmp.write_text(json.dumps({'rows': [{'candidate_id': 'a', 'brand': 'fake', 'name': 'Pricey sock', 'stage': 'screened', 'category': 'socks', 'planned_price': 96.0, 'pack_units': 4},
                                                     {'candidate_id': 'b', 'brand': 'fake', 'name': 'Fair sock', 'stage': 'screened', 'category': 'socks', 'planned_price': 22.0, 'pack_units': 1}]}), encoding='utf-8')
            fs = audit.review_price_findings(B(), 'fake', date(2026, 9, 27))
        finally:
            audit.PIPELINE_PATH = self.real3
        self.assertEqual([f['entity']['id'] for f in fs], ['a'])   # 24 a pair is 20 percent over 20; 22 is 10 percent
        self.assertIn('around $20', fs[0]['sentence'])
        self.check_shape(fs[0])

    def test_demand_pattern_tags(self):
        even = {'rows': [{'category': 'socks', 'series': [100] * 12}], 'months': [f'2026-{m:02d}' for m in range(1, 13)], 'last': '2026-12'}
        peaked = {'rows': [{'category': 'socks', 'series': [50] * 10 + [300, 400]}], 'months': even['months'], 'last': '2026-12'}
        fx = {'markets': [{'key': 'socks_us', 'cagr_pct': 9.0}], 'launches': []}
        self.assertEqual(audit.demand_pattern('socks', even, {'markets': [], 'launches': []})['tag'], 'evergreen')
        self.assertEqual(audit.demand_pattern('socks', even, fx)['tag'], 'trending')
        p = audit.demand_pattern('socks', peaked, fx)
        self.assertEqual(p['tag'], 'seasonal')
        self.assertEqual(p['peak_months'], ['12', '11'])
        self.assertEqual(p['top2_share'], 0.5833)
        self.assertEqual(audit.demand_pattern('socks', even, {'markets': [], 'launches': []}, 'Holiday gift box')['tag'], 'seasonal')
        self.assertIsNone(audit.demand_pattern('hats', even, fx)['tag'])

    def test_funnel_counts_stages_reached(self):
        rows = [audit.candidate_view(r, date(2026, 9, 27)) for r in [
            {'candidate_id': 'a', 'name': 'a', 'stage': 'gated', 'screen_in_date': '2026-09-20', 'time_box_days': 10},
            {'candidate_id': 'b', 'name': 'b', 'stage': 'screened', 'screen_in_date': '2026-09-20', 'time_box_days': 10},
            {'candidate_id': 'c', 'name': 'c', 'stage': 'killed', 'screen_in_date': '2026-09-01', 'time_box_days': 3}]]
        self.assertEqual([f['n'] for f in audit.pipeline_funnel(rows)], [2, 1, 1, 0, 0])
        self.assertFalse(rows[2]['over_box'])   # killed candidates never stall


class Req:
    def __init__(self, path, brand='bombas', method='GET'):
        self.method, self.path, self.query, self.data = method, path, {'brand': [brand]}, None

    def arg(self, name, default=None):
        v = self.query.get(name)
        return v[0] if v else default


class ApiTest(unittest.TestCase):
    def test_read_only_and_bad_brand(self):
        self.assertEqual(api.handle(Req(['overview'], method='POST'))[0], 405)
        self.assertEqual(api.handle(Req(['findings'], method='POST'))[0], 405)
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
