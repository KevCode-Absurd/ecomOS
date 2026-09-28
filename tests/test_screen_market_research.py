"""Screen 01-market-research: the products metric, audit rules, API shape, and the page on Bombas data.

Synthetic tests build a tiny catalog in memory so the declining-line and review rules are proven to fire
and to stay quiet. The Bombas tests skip when app/data/brands/bombas/data.sqlite has not been built.
"""
import importlib.util
import json
import sys
import unittest
import statistics
from datetime import date, timedelta
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
            if (a.get('entity') or {}).get('candidate'):
                self.assertTrue(rules <= set(api.CANDIDATE_RULES), rules)     # one card per candidate
            elif rules == {'PROD-R30'}:
                self.assertEqual({(f.split('.')[2]).split('-')[0] for f in a['finding_ids']}, {'reddit'})   # one listening post across subreddits
            elif 'PROD-R32' in rules:
                self.assertTrue(rules <= {'PROD-R31', 'PROD-R32'}, rules)   # one Amazon stance card
            elif 'PROD-R35' in rules:
                self.assertTrue(rules <= {'PROD-R07', 'PROD-R35'}, rules)   # a founder question rides on its theme card
            elif rules in ({'PROD-R41'}, {'PROD-R42'}, {'PROD-R43'}):
                pass                                                          # one brain refresh card, one assumptions card, one thin-reads card
            else:
                self.assertTrue(rules <= {'PROD-R05', 'PROD-R06', 'PROD-R20', 'PROD-R33'}, rules)   # one brief per lane
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

    def test_one_action_per_candidate(self):
        acts = self.actions()
        seen = {}
        for a in acts:
            ent = a.get('entity') or {}
            if ent.get('candidate'):
                self.assertNotIn(ent['id'], seen, 'two actions on one candidate')
                seen[ent['id']] = a
        covered = [fid for a in acts for fid in a['finding_ids']]
        self.assertEqual(len(covered), len(set(covered)))

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

    def test_every_card_lists_what_it_covers(self):
        acts = self.actions()
        for a in acts:
            self.assertEqual([c['id'] for c in a['covers']], list(a['finding_ids']), a['id'])
            for c in a['covers']:
                self.assertTrue(c['sentence'])
                self.assertTrue(c['rule'])
            self.assertEqual(api.rank_mod.validate_action(a), [], a['id'])
        merged = [a for a in acts if len(a['covers']) > 1]
        self.assertTrue(merged)
        self.assertTrue(all(len({c['rule_id'] for c in a['covers']}) >= 1 for a in merged))

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
        self._handoff_paths = (api.HANDOFF_PATH, api.TESTS_PATH)      # every candidate write also rewrites the hand-off files: keep them in the temp folder
        api.HANDOFF_PATH, api.TESTS_PATH = self.tmp.parent / 'handoff.json', self.tmp.parent / 'tests.json'

    def tearDown(self):
        audit.PIPELINE_PATH = self.real
        api.HANDOFF_PATH, api.TESTS_PATH = self._handoff_paths

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
        real_fx = audit.market_trends
        try:
            audit.PIPELINE_PATH = self.tmp
            audit.market_trends = lambda: {'launches': []}   # a web pass with no brand field applies to any brand; no lanes key means the default lanes
            self.tmp.write_text(json.dumps({'rows': [{'candidate_id': 'a', 'brand': 'fake', 'name': 'Merino hiking sock', 'stage': 'screened', 'angle_text': ''},
                                                     {'candidate_id': 'b', 'brand': 'fake', 'name': 'x', 'stage': 'killed', 'angle_text': 'compression'}]}), encoding='utf-8')
            lanes = audit.candidate_lanes('fake')
            self.assertEqual(audit.candidate_lanes(None), {})
        finally:
            audit.PIPELINE_PATH = self.real2
            audit.market_trends = real_fx
        self.assertEqual(audit.lanes_for('fake'), [])   # the real fixture names bombas: any other brand reads no lanes
        self.assertEqual(audit.lanes_for(None), [])
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

    def test_listing_complaints_rate_and_rule(self):
        class B:
            brand = 'fake'
            def records(self, sec):
                if sec == 'products':
                    return [{'value': {'asin': 'A1', 'kind': 'issues', 'themes': {'durability': 18, 'general': 46, 'price_value': 31}}},
                            {'value': {'asin': 'A1', 'kind': 'praise', 'themes': {'comfort': 36, 'general': 45}}},
                            {'value': {'asin': 'A2', 'kind': 'issues', 'themes': {'fit_sizing': 1}}},
                            {'value': {'asin': 'A2', 'kind': 'praise', 'themes': {'comfort': 5}}}]
                if sec == 'marketplaces':
                    return [{'value': {'asin': 'A1', 'title': 'Ankle sock', 'stars': 4.5, 'reviews_count': 2914, 'price_usd': 23.23}}]
                return []
        rows = {r['asin']: r for r in audit.listing_complaints(B())}
        a1 = rows['A1']
        self.assertEqual(a1['mined'], 176)
        self.assertEqual(a1['top_complaint'], 'price_value')       # general is left out
        self.assertEqual(a1['top_rate'], round(31 / 176, 4))
        self.assertEqual(a1['title'], 'Ankle sock')
        self.assertEqual(rows['A2']['mined'], 6)
        fs = audit.complaint_findings(B(), date(2026, 9, 27))
        self.assertEqual([f['entity']['id'] for f in fs], ['a1'])    # A2 has too few mined reviews
        self.assertIn('price and worth', fs[0]['sentence'])
        self.check_shape(fs[0])

    def test_angle_confidence_and_gates(self):
        comps = [{'name': 'Rival', 'text': 'vermont-made merino socks with a lifetime guarantee, durability first'}]
        none = audit.angle_confidence({'angle_text': None, 'angle_source': None}, comps)
        self.assertEqual((none['score'], none['label']), (0, 'none'))
        copy = audit.angle_confidence({'angle_text': 'Vermont-made merino socks with a lifetime guarantee and durability', 'angle_source': 'review gap PROD-R06'}, comps)
        self.assertEqual(copy['copied']['competitor'], 'Rival')
        self.assertEqual(copy['score'], 2)      # filled and sourced, not owned
        own = audit.angle_confidence({'angle_text': 'A wide soft cuff that pulls on without a fight for long shifts', 'angle_source': 'review gap: hard to pull on (finding PROD-R02)'}, comps)
        self.assertEqual((own['score'], own['label']), (3, 'solid'))
        gate = {'unavailable': False, 'passes_floor': True, 'margin_pct': 40.0, 'floor_pct': 22.0, 'contribution_usd': 10.0}
        rows = [{'field': 'target_cac', 'scope': 'global', 'scope_key': '', 'value': 12.0, 'unit': 'usd', 'effective_from': '2025-01-01', 'effective_to': None}]
        fin = metrics.finance.Finance(rows)
        gl = audit.go_live_gates({'category': 'socks', 'screen_result': {'store_fit': 'pass'}}, own, gate, ['SOCKS'], fin, '2026-09-27', 1.5)
        self.assertEqual(gl['passed'], 5)
        self.assertEqual(gl['gates']['ad_cost_ceiling']['status'], 'pass')   # 10 x 1.5 = 15 against 12
        gl2 = audit.go_live_gates({'category': 'hats', 'screen_result': {}}, none, {'unavailable': True, 'reason': 'no price'}, ['SOCKS'], None, '2026-09-27', None)
        self.assertEqual(gl2['passed'], 0)
        self.assertEqual(gl2['gates']['brand_threshold']['status'], 'fail')
        self.assertEqual(gl2['gates']['ad_cost_ceiling']['status'], 'unavailable')
        self.assertEqual(audit.compliance_status({'compliance': {'labelling': 'pass', 'category_certification': 'pass'}}), 'pass')
        self.assertEqual(audit.compliance_status({'compliance': {'labelling': 'pass'}}), 'unavailable')
        self.assertEqual(audit.compliance_status({'compliance': {'labelling': 'fail'}}), 'fail')

    def test_scorecard_scores_weights_and_review_due(self):
        sc = audit.score_candidate({'name': 'X', 'screen_result': {'demand': 'pass', 'competition': 'pass', 'store_fit': 'pass'}, 'cash_plan': None},
                                   {'angle': {'score': 3}, 'compliance': 'pass'}, {'unavailable': False, 'margin_pct': 40.0, 'floor_pct': 22.0}, {'tag': 'seasonal'},
                                   [{'verdict': 'funded', 'candidates': ['X']}])
        self.assertEqual(sc, {'demand': 5, 'margin': 5, 'differentiation': 5, 'compliance': 5, 'cash_timing': 1})
        sc2 = audit.score_candidate({'name': 'Y', 'screen_result': {}}, {'angle': {'score': 0}, 'compliance': 'unavailable'}, {'unavailable': True}, {'tag': None}, [])
        self.assertEqual(sc2, {'demand': None, 'margin': None, 'differentiation': 0, 'compliance': None, 'cash_timing': None})
        class B:
            brand = 'fake'
            def get(self, rid):
                return {'id': rid, 'value': {'demand': 1, 'margin': 1, 'differentiation': 1, 'compliance': 1, 'cash_timing': 1}} if rid.endswith('shortlist_weights') else None
            def records(self, sec):
                return []
        w, src = audit.shortlist_weights(B())
        self.assertEqual(w, {k: 20.0 for k in audit.CRITERIA})
        self.assertTrue(src.endswith('shortlist_weights'))
        self.assertEqual(audit.shortlist_weights(None)[0], audit.DEFAULT_WEIGHTS)
        self.real4 = audit.PIPELINE_PATH
        try:
            audit.PIPELINE_PATH = self.tmp
            self.tmp.write_text(json.dumps({'rows': [{'candidate_id': 'a', 'brand': None, 'name': 'Due one', 'stage': 'shortlisted', 'category': 'socks', 'planned_price': 20.0, 'review_date': '2026-09-20', 'screen_result': {}},
                                                     {'candidate_id': 'b', 'brand': None, 'name': 'Later', 'stage': 'screened', 'category': 'socks', 'planned_price': 20.0, 'review_date': '2026-10-20', 'screen_result': {}}]}), encoding='utf-8')
            fs = audit.shortlist_findings(None, FakeData(), None, audit.Reader(FakeData(), None, date(2026, 9, 27)), date(2026, 9, 27))
        finally:
            audit.PIPELINE_PATH = self.real4
        self.assertEqual([f['entity']['id'] for f in fs], ['a'])
        self.assertIn('review date (2026-09-20) has arrived', fs[0]['sentence'])
        self.assertIn('Decision: go', fs[0]['entity']['memo'])
        self.check_shape(fs[0])

    def test_video_signals_count_platforms(self):
        br = audit.brain('bombas')
        if br is None:
            self.skipTest('no bombas brain')
        v = audit.video_signals(br, 'bombas', date(2026, 9, 27))
        for r in v['rows']:
            n = len(r['platforms'])
            self.assertEqual(r['verdict'], 'pattern' if n >= 2 else 'single' if n == 1 else 'none')
            if 'reddit' in r['platforms']:
                self.assertGreaterEqual(r['reddit_mentions'], audit.REDDIT_MIN_MENTIONS)
            if 'creator ads' in r['platforms']:
                self.assertTrue(r['creator_pages'])
        fs = audit.video_findings(br, 'bombas', date(2026, 9, 27))
        for f in fs:
            self.check_shape(f)
            row = next(r for r in v['rows'] if r['key'] == f['entity']['id'])
            self.assertEqual(row['verdict'], 'single')
            self.assertTrue(row['candidates'])
        self.assertEqual(audit.reddit_lane_mentions(None), {})   # no brand, no web pass, no lanes

    def test_trend_history_verdicts(self):
        steady = {'series': [{'year': 2021, 'value_usd': 100}, {'year': 2023, 'value_usd': 110}, {'year': 2025, 'value_usd': 121}, {'year': 2030, 'value_usd': 160}]}
        h = audit.trend_history(steady, 2026)
        self.assertEqual((h['history_years'], h['history_points'], h['forecast_points'], h['verdict']), (4, 3, 1, 'steady'))
        self.assertAlmostEqual(h['long_growth'], 0.0489, places=3)
        spike = {'series': [{'year': 2021, 'value_usd': 100}, {'year': 2024, 'value_usd': 103}, {'year': 2025, 'value_usd': 140}]}
        self.assertEqual(audit.trend_history(spike, 2026)['verdict'], 'fad_risk')
        fc = {'series': [{'year': 2025, 'value_usd': 100}, {'year': 2033, 'value_usd': 150}]}
        self.assertEqual(audit.trend_history(fc, 2026)['verdict'], 'forecast_only')
        self.assertAlmostEqual(audit.trend_history(fc, 2026)['forecast_growth'], 0.0520, places=3)
        self.assertEqual(audit.trend_history({'series': []}, 2026)['verdict'], 'no_series')
        self.assertEqual(audit.trend_history({'series': [{'year': 2021, 'value_usd': 100}, {'year': 2025, 'value_usd': 90}]}, 2026)['verdict'], 'falling')

    def test_audience_surfaces_verdicts(self):
        D = date(2026, 9, 27)
        self.assertEqual(audit.audience_surfaces(None, D)['rows'], [])
        self.assertEqual(audit.audience_findings(None, D), [])

        class FakeBrain:
            brand = 'fake'

            def records(self, sec):
                if sec == 'language_bank':
                    return ([{'value': {'subreddit': 'BigSub', 'weight': 600, 'theme': 'praise', 'themes': ['durability']}}] * 25 +
                            [{'value': {'subreddit': 'SmallSub', 'weight': 10, 'theme': 'complaint', 'themes': ['fit_sizing']}}] * 3)
                if sec == 'objection_ladders':
                    return [{'value': {'theme': 'durability', 'counts': {'sources': {'trustpilot': 40, 'amazon': 5, 'reddit': 9}}}}]
                if sec == 'channels':
                    return [{'text': 'The brand sells on Amazon and posts on TikTok.', 'value': {}}]
                return []

        rows = {r['key']: r for r in audit.audience_surfaces(FakeBrain(), D)['rows']}
        self.assertEqual(rows['reddit:bigsub']['verdict'], 'gap')
        self.assertEqual((rows['reddit:bigsub']['quotes'], rows['reddit:bigsub']['upvotes'], rows['reddit:bigsub']['top_theme']), (25, 15000, 'durability'))
        self.assertEqual(rows['reddit:smallsub']['verdict'], 'watch')
        self.assertEqual(rows['reviews:trustpilot']['verdict'], 'gap')
        self.assertEqual(rows['reviews:amazon']['verdict'], 'present')
        self.assertNotIn('reviews:reddit', rows)
        self.assertEqual(rows['social:tiktok']['verdict'], 'not_pulled')
        found = audit.audience_findings(FakeBrain(), D)
        self.assertEqual(sorted(f['id'] for f in found), [f'{audit.SCREEN}.PROD-R30.reddit-bigsub', f'{audit.SCREEN}.PROD-R30.reviews-trustpilot'])
        big = next(f for f in found if 'bigsub' in f['id'])
        self.assertEqual(big['severity'], 'high')
        self.assertIsNone(big['money_at_stake'])
        for f in found:
            self.check_shape(f)

    def test_marketplace_read(self):
        D = date(2026, 9, 27)
        self.assertEqual(audit.pack_units_from_title("Men's Originals Ankle Socks White Large (4 Pair)"), 4)
        self.assertEqual(audit.pack_units_from_title('Women Ankle 6-Pack Cushioned'), 6)
        self.assertEqual(audit.pack_units_from_title('No Show (Black, Medium, 2pcs)'), 2)
        self.assertEqual(audit.pack_units_from_title('Ankle Socks, Grey'), 1)
        self.assertEqual(audit.marketplace_read(None, None)['rows'], [])

        class FakeBrain:
            brand = 'fake'

            def records(self, sec):
                if sec == 'marketplaces':
                    return [{'id': 'fake.marketplaces.amazon_presence', 'field': 'amazon_presence', 'text': 'resellers only', 'source': {'captured_at': '2026-09-20'},
                             'value': {'brand_store': False, 'sold_by_brand': False, 'resellers_seen': ['Shop A'], 'aplus_content_seen': False, 'asins_read': ['A1', 'A2'], 'lines_not_found': ['slippers'], 'listings_in_stock': 1}},
                            {'id': 'l1', 'field': 'amazon_listing', 'value': {'asin': 'A1', 'title': 'Ankle 4 Pack', 'price_usd': 40.0, 'stars': 4.5, 'reviews_count': 300, 'seller': None}},
                            {'id': 'l2', 'field': 'amazon_listing', 'value': {'asin': 'A2', 'title': 'Ankle single', 'price_usd': 22.0, 'stars': 4.4, 'reviews_count': 100, 'seller': None}},
                            {'id': 'l3', 'field': 'amazon_listing', 'value': {'asin': 'A3', 'title': 'Calf 8-Pack', 'price_usd': 40.0, 'stars': 5.0, 'reviews_count': 2, 'seller': None}},
                            {'id': 'l4', 'field': 'amazon_listing', 'value': {'asin': 'A4', 'title': 'Calf 3 Pairs', 'price_usd': 33.0, 'stars': 4.6, 'reviews_count': 50, 'seller': 'Fake Official'}}]
                return []

            def get(self, rid):
                return {'value': {'min_usd': 10.0}} if rid.endswith('price_ladder_socks') else None

        m = audit.marketplace_read(FakeBrain(), None)
        rows = {r['asin']: r for r in m['rows']}
        self.assertEqual(m['site_per_pair']['value'], 10.0)
        self.assertEqual((rows['A1']['pack_units'], rows['A1']['per_pair'], rows['A1']['spread'], rows['A1']['verdict']), (4, 10.0, 0.0, 'reseller'))
        self.assertEqual((rows['A2']['per_pair'], rows['A2']['spread'], rows['A2']['verdict']), (22.0, 1.2, 'price_spread'))
        self.assertEqual(rows['A3']['verdict'], 'unverified')
        self.assertEqual((rows['A4']['sold_by_brand'], rows['A4']['verdict']), (True, 'brand_sells'))
        self.assertEqual((m['summary']['judged'], m['summary']['unverified'], m['summary']['ratings']), (3, 1, 450))
        found = audit.marketplace_findings(FakeBrain(), None, D)
        self.assertEqual([f['id'] for f in found], [f'{audit.SCREEN}.PROD-R31.amazon', f'{audit.SCREEN}.PROD-R32.a2'])
        self.assertEqual(found[0]['severity'], 'high')
        self.assertIn('Shop A', found[0]['sentence'])
        self.assertIn('120 percent above', found[1]['sentence'])
        for f in found:
            self.assertIsNone(f['money_at_stake'])
            self.check_shape(f)

    def test_launch_cadence(self):
        D = date(2026, 9, 27)
        self.assertEqual(audit.launch_date('2026-09-24'), date(2026, 9, 24))
        self.assertEqual(audit.launch_date('2026-09'), date(2026, 9, 15))
        self.assertEqual(audit.launch_date('2025'), date(2025, 7, 1))
        self.assertIsNone(audit.launch_date('soon'))
        self.assertAlmostEqual(audit.months_between(date(2025, 9, 27), D), 12.0, places=2)
        fx = {'captured_at': '2026-09-28', 'markets': [], 'preferences': [], 'launches': [
            {'brand': 'Rival A', 'what': 'merino crew', 'sub_category': 'merino', 'date': '2026-08', 'price_usd': 25, 'channel': 'dtc', 'sources': [{'url': 'https://a'}]},
            {'brand': 'Rival B', 'what': 'merino hiker', 'sub_category': 'merino', 'date': '2026-02-01', 'price_usd': 30, 'channel': 'dtc', 'sources': [{'url': 'https://b'}]},
            {'brand': 'Rival A', 'what': 'compression calf', 'sub_category': 'compression', 'date': '2026-06', 'price_usd': None, 'channel': 'dtc', 'sources': []},
            {'brand': 'Fake', 'what': 'compression calf of ours', 'sub_category': 'compression', 'date': '2025-12', 'price_usd': 20, 'channel': 'dtc', 'sources': []},
            {'brand': 'Rival C', 'what': 'future thing', 'sub_category': 'merino', 'date': '2027-01', 'price_usd': None, 'channel': 'dtc', 'sources': []}]}

        class FakeBrain:
            brand = 'fake'

            def records(self, sec):
                if sec == 'products':
                    return [{'text': 'We sell merino calf socks and compression socks.', 'value': {}}]
                return []

        saved = audit.market_trends
        audit.market_trends = lambda: fx
        try:
            c = audit.launch_cadence(FakeBrain(), D)
            self.assertEqual(c['launches_read'], 4)   # the future launch is dropped
            self.assertEqual(c['ours'], {'n_12m': 1, 'n_24m': 1, 'months_since_last': 9.4})
            self.assertEqual(c['competitor_median_12m'], 1.5)
            lanes = {r['key']: r for r in c['lanes']}
            self.assertEqual((lanes['merino']['verdict'], lanes['merino']['theirs_12m'], lanes['merino']['brands_24m']), ('in_play', 2, ['Rival A', 'Rival B']))
            self.assertEqual(lanes['compression']['verdict'], 'matched')
            self.assertEqual(lanes['guarantee']['verdict'], 'proof')
            found = audit.cadence_findings(FakeBrain(), D)
            self.assertEqual([f['id'] for f in found], [f'{audit.SCREEN}.PROD-R33.merino'])
            self.assertIn('Rival A, Rival B launched 2 times', found[0]['sentence'])
            self.check_shape(found[0])
        finally:
            audit.market_trends = saved

    def test_open_questions(self):
        D = date(2026, 9, 27)
        self.assertEqual(audit.open_questions(None, D)['rows'], [])

        class FakeBrain:
            brand = 'fake'

            def records(self, sec):
                if sec == 'open_questions':
                    return [{'id': 'fake.open_questions.ladder_durability_3', 'field': 'ladder_durability_3', 'value': {'question': 'What proof answers "will it last"? 35 complaint quotes raise it and no policy, offer or claim covers it.', 'who_can_answer': 'the founder', 'asked_on': None, 'answered_on': None}},
                            {'id': 'fake.open_questions.ladder_fit_and_sizing_2', 'field': 'ladder_fit_and_sizing_2', 'value': {'question': 'What proof answers "does it fit"? 3 complaint quotes raise it.', 'who_can_answer': 'the founder', 'asked_on': '2026-09-01', 'answered_on': None}},
                            {'id': 'fake.open_questions.ladder_comfort_and_feel_1', 'field': 'ladder_comfort_and_feel_1', 'value': {'question': 'What proof answers "is it soft"? 9 complaint quotes raise it.', 'who_can_answer': 'the founder', 'asked_on': '2026-09-20', 'answered_on': '2026-09-22'}}]
                if sec == 'claims':
                    return [{'text': 'Our lifetime guarantee replaces any pair.', 'value': {}}]
                return []

        rows = {r['theme']: r for r in audit.open_questions(FakeBrain(), D)['rows']}
        self.assertEqual((rows['durability']['verdict'], rows['durability']['quotes'], rows['durability']['doubt'], rows['durability']['records_answer_theme']), ('never_asked', 35, 'will it last', True))
        self.assertEqual((rows['fit_sizing']['verdict'], rows['fit_sizing']['days_open']), ('overdue', 26))
        self.assertEqual(rows['comfort']['verdict'], 'answered')
        found = audit.question_findings(FakeBrain(), D)
        self.assertEqual([f['id'] for f in found], [f'{audit.SCREEN}.PROD-R35.ladder_durability_3'])   # 3 quotes is under the floor; answered never fires
        self.assertEqual(found[0]['severity'], 'medium')
        self.assertEqual(found[0]['entity']['id'], 'durability')
        self.check_shape(found[0])

    def test_pulls_freshness(self):
        D = date(2026, 9, 27)
        self.assertEqual(audit.pulls(None, None, D)['rows'], [])
        br = audit.brain('bombas')
        p = audit.pulls(br, 'bombas', D)
        rows = {r['key']: r for r in p['rows']}
        self.assertEqual(set(rows), {'reddit', 'amazon_reviews', 'ad_library', 'amazon_listings', 'listing_seller', 'instagram', 'web_pass'})
        self.assertEqual(rows['instagram']['verdict'], 'mock')
        self.assertEqual(rows['listing_seller']['verdict'], 'mock')   # the mock listing pull is on file
        self.assertEqual(rows['reddit']['verdict'], 'fresh')
        self.assertEqual(rows['reddit']['age_days'], 0)                      # captured after the window end reads as 0 days, never negative
        self.assertEqual(rows['reddit']['next_due'], '2026-10-28')
        self.assertGreater(rows['reddit']['estimate_usd'], 0)
        self.assertLessEqual(rows['reddit']['estimate_usd'], p['caps']['per_run_usd'])
        self.assertEqual(rows['ad_library']['window_days'], 7 if audit.candidate_lanes('bombas') or [c for c in audit.pipeline('bombas') if c.get('stage') not in audit.CLOSED_STAGES] else 30)   # open candidates set the short window
        late = audit.pulls(br, 'bombas', date(2026, 11, 30))
        self.assertEqual({r['key']: r['verdict'] for r in late['rows'] if r['key'] in ('reddit', 'amazon_reviews')}, {'reddit': 'due', 'amazon_reviews': 'due'})
        found = audit.pull_findings(br, 'bombas', D)
        self.assertEqual(sorted(f['id'].split('.')[-1] for f in found), ['instagram', 'listing_seller'])   # both mock today
        for f in found:
            self.assertIsNone(f['money_at_stake'])
            self.check_shape(f)
        self.assertNotIn('APIFY', json.dumps(found))                        # no token, no key, ever

    def test_listing_pull(self):
        import importlib.util as iu
        spec = iu.spec_from_file_location('listing_pull_t', SCREEN / 'listing_pull.py')
        mod = iu.module_from_spec(spec)
        spec.loader.exec_module(mod)
        rows = mod.rows_from([{'asin': 'X1', 'title': 'T', 'url': 'u', 'price': {'value': 30.0, 'currency': '$'}, 'stars': 4.4, 'reviewsCount': 12, 'brand': 'Fake', 'seller': {'name': 'Fake'}, 'userName': 'never'},
                              {'asin': 'X2', 'title': 'T2', 'price': 20, 'seller': 'Some Outlet'}], 'Fake')
        self.assertEqual((rows[0]['seller'], rows[0]['third_party_seller'], rows[0]['price_usd'], rows[0]['ratings']), ('Fake', False, 30.0, 12))
        self.assertEqual((rows[1]['seller'], rows[1]['third_party_seller'], rows[1]['price_usd']), ('Some Outlet', True, 20.0))
        self.assertNotIn('userName', json.dumps(rows))
        fx = json.loads((SCREEN / 'fixtures' / 'amazon_listings.json').read_text(encoding='utf-8'))
        self.assertEqual((fx['brand'], fx['mode']), ('bombas', 'mock'))
        self.assertIsNone(audit.listing_pull_for(None))
        br = audit.brain('bombas')
        m = audit.marketplace_read(br, None)
        self.assertEqual(m['pull']['mode'], 'mock')
        self.assertFalse(m['pull']['sellers_used'])
        self.assertTrue(all(r['seller'] is None for r in m['rows']))      # a mock seller is never read as fact
        saved = audit.listing_pull
        try:
            audit.listing_pull = lambda: {'brand': 'bombas', 'mode': 'live', 'captured_at': '2026-09-27', 'actor': 'x', 'usd': 1.0,
                                          'rows': [{'asin': 'B08CS397JX', 'seller': 'Coastal Co. Goods', 'price_usd': 23.23, 'stars': 4.5, 'ratings': 2914}]}
            live = audit.marketplace_read(br, None)
            row = next(r for r in live['rows'] if r['asin'] == 'B08CS397JX')
            self.assertEqual((row['seller'], row['seller_read'], row['sold_by_brand']), ('Coastal Co. Goods', True, False))
            self.assertTrue(live['pull']['sellers_used'])
            pr = {r['key']: r for r in audit.pulls(br, 'bombas', date(2026, 9, 27))['rows']}['listing_seller']
            self.assertEqual(pr['verdict'], 'fresh')
        finally:
            audit.listing_pull = saved
        pr = {r['key']: r for r in audit.pulls(br, 'bombas', date(2026, 9, 27))['rows']}['listing_seller']
        self.assertEqual(pr['verdict'], 'mock')

    def test_first_run_moq_gate(self):
        D = date(2026, 9, 27)
        self.real2 = audit.PIPELINE_PATH
        try:
            audit.PIPELINE_PATH = self.tmp
            rows = [{'candidate_id': 'a', 'brand': 'fake', 'name': 'A', 'stage': 'gated'},
                    {'candidate_id': 'b', 'brand': 'fake', 'name': 'B', 'stage': 'shortlisted', 'first_run': {'units': 500, 'moq_units': 2000, 'format': 'custom box', 'cash_usd': 30000, 'lower_moq_option': None}},
                    {'candidate_id': 'c', 'brand': 'fake', 'name': 'C', 'stage': 'gated', 'first_run': {'units': 500, 'moq_units': 500, 'format': 'stock sleeve', 'cash_usd': 4000, 'lower_moq_option': 'stock blank plus sleeve, MOQ 300'}},
                    {'candidate_id': 'd', 'brand': 'fake', 'name': 'D', 'stage': 'screened'},
                    {'candidate_id': 'e', 'brand': 'fake', 'name': 'E', 'stage': 'gated', 'first_run': {'units': 500, 'moq_units': 500, 'format': 'custom', 'cash_usd': 10000, 'lower_moq_option': None}}]
            self.tmp.write_text(json.dumps({'rows': rows}), encoding='utf-8')
            fr = audit.first_run_read('fake', D, 100000.0)
            v = {r['candidate_id']: r['verdict'] for r in fr['rows']}
            self.assertEqual(v, {'a': 'no_plan', 'b': 'full_moq_risk', 'c': 'sized', 'd': 'not_yet', 'e': 'sized'})   # e: 10 percent of revenue, MOQ not over
            self.assertEqual(next(r for r in fr['rows'] if r['candidate_id'] == 'b')['cash_share_28d'], 0.3)
            found = audit.first_run_findings('fake', D, 100000.0)
            self.assertEqual([f['id'].split('.')[-1] for f in found], ['b', 'a'])
            b = found[0]
            self.assertEqual(b['money_at_stake']['usd'], 30000)
            self.assertIn('2,000 above the 500 units wanted', b['sentence'])
            for f in found:
                self.check_shape(f)
            unknown = {r['candidate_id']: r['verdict'] for r in audit.first_run_read('fake', D, None)['rows']}
            self.assertEqual(unknown['e'], 'full_moq_risk')   # revenue unknown and no option: a risk
            self.assertEqual(unknown['c'], 'sized')
        finally:
            audit.PIPELINE_PATH = self.real2

    def test_ledger_week_reads_only(self):
        import sqlite3
        p = ROOT / 'tests' / '_spend_test.sqlite'
        try:
            con = sqlite3.connect(p)
            con.execute('CREATE TABLE spend (request_id TEXT PRIMARY KEY, provider TEXT NOT NULL, reserved INTEGER NOT NULL, actual INTEGER, status TEXT NOT NULL)')
            con.executemany('INSERT INTO spend VALUES (?,?,?,?,?)', [
                ('apify:fake:2026-W40:trudax~reddit-scraper-lite:a1', 'apify', 2_600_000, 1_200_000, 'settled'),
                ('apify:fake:2026-W40:junglee~amazon-crawler:b2', 'apify', 770_000, 8_640_000, 'bound_exceeded'),
                ('apify:fake:2026-W40:axesso_data~amazon-reviews-scraper:c3', 'apify', 500_000, None, 'reserved'),
                ('apify:fake:2026-W39:trudax~reddit-scraper-lite:d4', 'apify', 1_000_000, 900_000, 'settled'),
                ('apify:other:2026-W40:trudax~reddit-scraper-lite:e5', 'apify', 1_000_000, 900_000, 'settled')])
            con.commit(); con.close()
            lw = audit.ledger_week('fake', date(2026, 9, 28), path=p)
            self.assertEqual((lw['week'], lw['runs_week'], lw['spent_week_usd'], lw['reserved_open_usd'], lw['over_bound_week']), ('2026-W40', 3, 10.34, 0.5, 1))
            self.assertEqual((lw['spent_all_usd'], lw['runs_all']), (11.24, 4))
            self.assertEqual(lw['by_actor_week'][0], ('junglee~amazon-crawler', 8.64))
            self.assertFalse(audit.ledger_week('fake', date(2026, 9, 28), path=ROOT / 'tests' / '_no_ledger.sqlite')['available'])
            self.assertFalse(audit.ledger_week(None, date(2026, 9, 28), path=p)['available'])
            self.assertEqual(sqlite3.connect(p).execute('SELECT COUNT(*) FROM spend').fetchone()[0], 5)   # nothing written
        finally:
            p.unlink(missing_ok=True)

    def test_brain_launches_join_the_cadence(self):
        D = date(2026, 9, 27)

        class FakeBrain:
            brand = 'fake'

            def records(self, sec):
                if sec == 'calendar':
                    return [{'id': 'fake.calendar.launch_merino_2025', 'field': 'launch_merino_2025', 'value': {'year': 2025, 'category': 'merino socks'}, 'text': 'Fake launched merino socks in 2025.', 'source': {'type': 'press', 'ref': 'https://p', 'captured_at': '2026-09-28'}},
                            {'id': 'fake.calendar.launch_slippers_2026', 'field': 'launch_slippers_2026', 'value': {'date': '2026-08-01', 'categories': ['slippers']}, 'text': 'Fake launched slippers.', 'source': {}},
                            {'id': 'fake.calendar.store_2025', 'field': 'store_2025', 'value': {'month': '2025-10'}, 'text': 'A store opened.', 'source': {}}]
                if sec == 'products':
                    return [{'text': 'We sell merino socks and slippers.', 'value': {}}]
                return []

        lanes = [('merino', 'Merino', ['merino', 'wool']), ('footwear', 'Slippers', ['slipper'])]
        bl = audit.brain_launches(FakeBrain(), lanes)
        self.assertEqual([(l['date'], l['lanes']) for l in bl], [('2025', ['merino']), ('2026-08-01', ['footwear'])])   # stores are not launches
        fx = {'captured_at': '2026-09-28', 'markets': [], 'preferences': [], 'lanes': [{'key': k, 'label': l, 'terms': t, 'kind': 'product'} for k, l, t in lanes], 'launches': [
            {'brand': 'Rival', 'what': 'merino crew', 'sub_category': 'merino', 'date': '2026-08', 'price_usd': 25, 'channel': 'dtc', 'sources': []},
            {'brand': 'Rival B', 'what': 'merino hiker', 'sub_category': 'merino', 'date': '2026-02', 'price_usd': 30, 'channel': 'dtc', 'sources': []},
            {'brand': 'fake', 'what': 'our slipper (press)', 'sub_category': 'footwear', 'date': '2026-07-20', 'price_usd': 40, 'channel': 'dtc', 'sources': []}]}
        saved = audit.market_trends
        audit.market_trends = lambda: fx
        try:
            c = audit.launch_cadence(FakeBrain(), D)
            me = next(b for b in c['brands'] if b['self'])
            self.assertEqual((me['n_24m'], me['from_brain']), (2, 1))              # the press slipper and the brain slipper 12 days apart count once; merino 2025 joins from the brain
            lanes_v = {r['key']: r for r in c['lanes']}
            self.assertEqual(lanes_v['merino']['verdict'], 'matched')            # our 2025 merino launch is inside 24 months
            self.assertEqual(lanes_v['merino']['our_last']['date'], '2025')
        finally:
            audit.market_trends = saved

    def test_override_and_companion_rules(self):
        D = date(2026, 9, 27)
        self.real2 = audit.PIPELINE_PATH
        try:
            audit.PIPELINE_PATH = self.tmp
            rows = [{'candidate_id': 'a', 'brand': 'fake', 'name': 'A', 'stage': 'researched', 'screen_result': {'demand': 'pass', 'competition': 'fail', 'store_fit': 'pass'}, 'log': [{'on': '2026-09-20', 'who': 'person', 'what': 'moved to researched'}]},
                    {'candidate_id': 'b', 'brand': 'fake', 'name': 'B', 'stage': 'researched', 'screen_result': {'demand': 'pass', 'competition': 'fail', 'store_fit': 'pass'}, 'log': [{'on': '2026-09-20', 'who': 'person', 'what': 'override: competition fail accepted because the 3 rivals are all under $10 a pair'}]},
                    {'candidate_id': 'c', 'brand': 'fake', 'name': 'C', 'stage': 'screened', 'screen_result': {'demand': 'fail', 'competition': 'fail', 'store_fit': 'pass'}, 'log': []},
                    {'candidate_id': 'd', 'brand': 'fake', 'name': 'D', 'stage': 'gated', 'screen_result': {'demand': 'pass', 'competition': 'pass', 'store_fit': 'pass'}, 'compliance': {'labelling': 'fail'}, 'log': []}]
            self.tmp.write_text(json.dumps({'rows': rows}), encoding='utf-8')
            ov = {r['candidate_id']: r for r in audit.override_read('fake', D)}
            self.assertEqual(set(ov), {'a', 'b', 'd'})            # c is still at screened: a failed check there is not an override yet
            self.assertEqual((ov['a']['verdict'], ov['b']['verdict'], ov['d']['verdict']), ('unlogged', 'logged', 'unlogged'))
            self.assertEqual(ov['d']['failed'], ['compliance labelling'])
            found = audit.override_findings('fake', D)
            self.assertEqual(sorted(f['id'].split('.')[-1] for f in found), ['a', 'd'])
            for f in found:
                self.check_shape(f)
            # the override write (the hand-off file it rewrites goes to the temp folder)
            saved_paths = (api.HANDOFF_PATH, api.TESTS_PATH)
            api.HANDOFF_PATH, api.TESTS_PATH = self.tmp.parent / 'handoff.json', self.tmp.parent / 'tests.json'
            code = api.candidate_update('fake', 'a', {'override_reason': 'competition fail accepted: the rivals are resellers', 'who': 'person'}, D)
            api.HANDOFF_PATH, api.TESTS_PATH = saved_paths
            self.assertEqual(code['changes'], ['override: competition fail accepted: the rivals are resellers'])
            self.assertEqual({r['candidate_id']: r['verdict'] for r in audit.override_read('fake', D)}['a'], 'logged')
        finally:
            audit.PIPELINE_PATH = self.real2

    def test_companion_rule_on_bombas(self):
        data = None
        rd = audit.Reader(None, 'bombas', date(2026, 9, 27))
        rows = audit.companion_read('bombas', data, rd, date(2026, 9, 27))
        self.assertTrue(all(r['tag'] == 'trending' for r in rows))
        for f in audit.companion_findings('bombas', data, rd, date(2026, 9, 27)):
            self.check_shape(f)

    def test_order_by_date_and_lead_time(self):
        D = date(2026, 9, 27)
        self.assertEqual(audit.order_by_date(['11', '12'], D, 45), ('2026-09-03', '2026-11-01'))     # 45 days of lead plus 14 of safety before 1 Nov
        self.assertEqual(audit.order_by_date(['3'], D, 30), ('2027-01-16', '2027-03-01'))           # the next March, not the past one
        self.assertEqual(audit.order_by_date(['11'], D, None), (None, None))
        self.assertEqual(audit.lead_time_for({'lead_time_days': 40}, None), (40, 'candidate'))
        self.assertEqual(audit.lead_time_for({}, None), (None, None))

        class B:
            brand = 'fake'

            def get(self, rid):
                return {'id': rid, 'value': 60} if rid == 'fake.learnings.lead_time_days' else None

            def records(self, sec):
                return []
        self.assertEqual(audit.lead_time_for({}, B()), (60, 'fake.learnings.lead_time_days'))
        # on Bombas: the gift box is seasonal at gated with no lead time on file
        audit.PIPELINE_PATH = self.real   # the seeded pipeline, not this test's empty one
        rd = audit.Reader(None, 'bombas', D)
        found = audit.order_findings('bombas', None, audit.brain('bombas'), rd, D)
        self.assertEqual([f['id'].split('.')[-1] for f in found], ['cand-003'])
        self.assertEqual(found[0]['severity'], 'medium')
        self.assertIn('no lead time is on file', found[0]['sentence'])
        self.check_shape(found[0])
        r = api.recipe(found[0])
        self.assertIn('lead time', r['title'])

    def test_brain_freshness(self):
        D = date(2026, 9, 27)
        self.assertEqual(audit.brain_freshness(None, D)['rows'], [])
        self.assertIn('objection_ladders', audit.sections_read())
        self.assertIn('marketplaces', audit.sections_read())

        class FakeBrain:
            brand = 'fake'

            def records(self, sec):
                if sec == 'freshness':
                    return [{'field': 'avatars', 'value': {'last_updated': '2026-09-20', 'record_count': 5, 'stale_count': 0, 'conflict_count': 0, 'confidence': 0.6}},
                            {'field': 'competitors', 'value': {'last_updated': '2026-08-01', 'record_count': 9, 'stale_count': 0, 'conflict_count': 0, 'confidence': 0.7}},
                            {'field': 'claims', 'value': {'last_updated': '2026-09-27', 'record_count': 6, 'stale_count': 2, 'conflict_count': 0, 'confidence': 0.8}},
                            {'field': 'identity', 'value': {'last_updated': '2026-09-27', 'record_count': 6, 'stale_count': 0, 'conflict_count': 1, 'confidence': 0.9}}]
                return []

        rows = {r['section']: r for r in audit.brain_freshness(FakeBrain(), D)['rows']}
        self.assertEqual((rows['avatars']['verdict'], rows['avatars']['age_days'], rows['avatars']['ttl_days']), ('fresh', 7, 30))
        self.assertEqual(rows['competitors']['verdict'], 'stale')          # 57 days against a 14-day TTL
        self.assertEqual(rows['claims']['verdict'], 'stale')               # stale records inside the TTL
        self.assertEqual(rows['identity']['verdict'], 'conflict')
        self.assertEqual(rows['language_bank']['verdict'], 'unknown')      # no freshness record never reads fresh
        self.assertIn('PROD-R07', rows['objection_ladders']['readers'])
        found = audit.freshness_findings(FakeBrain(), D)
        self.assertEqual([f['id'].split('.')[-1] for f in found], ['identity', 'competitors', 'claims'])
        self.assertEqual(found[0]['severity'], 'medium')
        for f in found:
            self.check_shape(f)
        bombas = audit.brain_freshness(audit.brain('bombas'), D)
        self.assertTrue(all(r['verdict'] in ('fresh', 'unknown', 'stale', 'conflict', 'no_ttl') for r in bombas['rows']))
        self.assertNotIn('config', {r['section'] for r in bombas['rows']})
        self.assertTrue(any(r['verdict'] == 'fresh' for r in bombas['rows']))

    def test_assumptions_block_and_rule(self):
        D = date(2026, 9, 27)
        self.assertEqual(audit.assumptions(None)['rows'], [])
        br = audit.brain('bombas')
        rows = {r['field']: r for r in audit.assumptions(br)['rows']}
        self.assertEqual(rows['repeat_rate_12m']['verdict'], 'confirmed')
        self.assertEqual(rows['gross_margin']['verdict'], 'unconfirmed')
        self.assertEqual(rows['giving_units']['verdict'], 'unused')
        self.assertIn('PROD-R11', rows['repeat_rate_12m']['readers'])
        found = audit.assumption_findings(br, D)
        self.assertEqual(sorted(f['id'].split('.')[-1] for f in found), ['category_mix', 'gross_margin', 'return_share'])
        for f in found:
            self.assertEqual(f['severity'], 'low')
            self.check_shape(f)
        acts = [a for a in api.rank('bombas', {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4})['actions'] if a.get('rule_id') == 'PROD-R42']
        self.assertEqual(len(acts), 1)                       # one card for all three
        self.assertEqual(len(acts[0]['finding_ids']), 3)
        self.assertEqual(acts[0]['owner'], 'person')

    def test_read_strength(self):
        D = date(2026, 9, 27)
        rd = audit.Reader(None, 'bombas', D)
        st = audit.read_strength(audit.brain('bombas'), 'bombas', None, rd, D)
        rows = {r['key']: r for r in st['rows']}
        self.assertEqual(set(rows), set(audit.READ_FLOORS))
        self.assertEqual(rows['returns']['verdict'], 'unavailable')
        self.assertIn(rows['conversation']['verdict'], ('ok', 'strong'))
        self.assertGreater(rows['conversation']['sources'], 2)
        self.assertEqual(rows['sales']['sample'], 12)
        self.assertEqual(audit.strength_of_rule(st, 'PROD-R07')['key'], 'conversation')
        self.assertIsNone(audit.strength_of_rule(st, 'PROD-R14'))
        for f in audit.strength_findings(audit.brain('bombas'), 'bombas', None, rd, D):
            self.check_shape(f)
        acts = api.rank('bombas', {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4})['actions']
        a7 = next(a for a in acts if a.get('rule_id') == 'PROD-R07')
        self.assertEqual(a7['read_strength']['read'], 'Conversation and themes')
        sample = api.sample_data()
        ss = audit.read_strength(None, None, sample, audit.Reader(sample, None, date(2026, 9, 24)), date(2026, 9, 24))
        self.assertEqual({r['key']: r['verdict'] for r in ss['rows'] if r['key'] in ('sales', 'returns', 'ads')}, {'sales': 'ok', 'returns': 'ok', 'ads': 'unavailable'})   # returns: one source, so never strong

    def test_line_theme_matrix(self):
        D = date(2026, 9, 27)
        self.assertEqual(audit.line_of_title("Women's Cushioned No Show Socks - 4 Pack"), 'no_show')
        self.assertEqual(audit.line_of_title("Men's Originals Ankle Socks"), 'ankle')
        self.assertEqual(audit.line_of_title('Gripper Slipper'), 'slippers')
        self.assertEqual(audit.line_of_title('Mystery item'), 'other')
        self.assertEqual(audit.theme_of_phrase('hole in the heel after two wears'), 'durability')
        self.assertEqual(audit.theme_of_phrase('runs small, too tight'), 'fit_sizing')
        self.assertEqual(audit.line_theme_matrix(None)['rows'], [])
        m = audit.line_theme_matrix(audit.brain('bombas'))
        self.assertTrue(m['rows'])
        self.assertTrue(all(r['total'] == sum(r['themes'].values()) for r in m['rows']))
        self.assertTrue(all(c['key'] in audit.THEME_LABEL for c in m['cols']))
        self.assertEqual(m['rows'][0]['key'], 'ankle')                     # the ankle line: 88 quotes, price and worth leads
        for r in m['rows']:
            self.assertIn(r['verdict'], ('concentrated', 'spread', 'thin'))
            if r['verdict'] == 'concentrated':
                self.assertGreaterEqual(r['total'], audit.LINE_MIN_QUOTES)
                self.assertGreaterEqual(r['top_share'], audit.THEME_CONCENTRATION)
        found = audit.line_theme_findings(audit.brain('bombas'), D)
        self.assertEqual([f['id'].split('.')[-1] for f in found], ['ankle'])
        for f in found:
            self.check_shape(f)
            self.assertEqual(f['capability']['id'], 'PROD-C34')
            self.assertIn('listing', api.recipe(f)['title'])

    def test_research_log_and_owner(self):
        D = date(2026, 9, 27)
        self.real2 = audit.PIPELINE_PATH
        saved_paths = (api.HANDOFF_PATH, api.TESTS_PATH)
        api.HANDOFF_PATH, api.TESTS_PATH = self.tmp.parent / 'handoff.json', self.tmp.parent / 'tests.json'   # writes stay in the temp folder
        try:
            audit.PIPELINE_PATH = self.tmp
            self.tmp.write_text(json.dumps({'rows': [{'candidate_id': 'a', 'brand': 'fake', 'name': 'A', 'stage': 'shortlisted', 'log': [{'on': '2026-09-20', 'who': 'person', 'what': 'shortlisted'}]},
                                                     {'candidate_id': 'b', 'brand': 'fake', 'name': 'B', 'stage': 'go', 'owner': 'Sam', 'first_run': {'units': 500, 'moq_units': 500, 'format': 'box', 'cash_usd': 4000}},
                                                     {'candidate_id': 'c', 'brand': 'fake', 'name': 'C', 'stage': 'researched'}]}), encoding='utf-8')
            lg = audit.research_log('fake')
            self.assertEqual(lg['columns'], audit.LOG_COLUMNS)
            self.assertEqual(len(lg['rows']), 3)
            self.assertTrue(all(set(r) == set(audit.LOG_COLUMNS) for r in lg['rows']))
            b = next(r for r in lg['rows'] if r['candidate_id'] == 'b')
            self.assertEqual((b['owner'], b['first_run_units'], b['first_run_cash_usd'], b['tech_pack_status']), ('Sam', 500, 4000, 'none'))
            found = audit.owner_findings('fake', D)
            self.assertEqual([f['id'].split('.')[-1] for f in found], ['a'])     # b has Sam, c is before shortlisted
            self.check_shape(found[0])
            api.candidate_update('fake', 'a', {'owner': 'Ana', 'who': 'person'}, D)
            self.assertEqual(audit.owner_findings('fake', D), [])
            r = api.candidate_update('fake', 'a', {'stage': 'go', 'who': 'person'}, D)
            self.assertEqual(r['proposed_test']['owner'], 'Ana')
        finally:
            audit.PIPELINE_PATH = self.real2
            api.HANDOFF_PATH, api.TESTS_PATH = saved_paths

    def test_sample_gate(self):
        D = date(2026, 9, 27)
        self.real2 = audit.PIPELINE_PATH
        try:
            audit.PIPELINE_PATH = self.tmp
            self.tmp.write_text(json.dumps({'rows': [{'candidate_id': 'a', 'brand': 'fake', 'name': 'A', 'stage': 'shortlisted'},
                                                     {'candidate_id': 'b', 'brand': 'fake', 'name': 'B', 'stage': 'gated', 'first_run': {'units': 500}},
                                                     {'candidate_id': 'c', 'brand': 'fake', 'name': 'C', 'stage': 'gated'},
                                                     {'candidate_id': 'd', 'brand': 'fake', 'name': 'D', 'stage': 'shortlisted', 'sample': {'ordered_on': '2026-09-01', 'received_on': '2026-09-10', 'through_own_chain': True, 'result': 'pass'}},
                                                     {'candidate_id': 'e', 'brand': 'fake', 'name': 'E', 'stage': 'shortlisted', 'sample': {'ordered_on': '2026-09-01', 'received_on': '2026-09-10', 'result': 'fail', 'notes': 'seam split'}}]}), encoding='utf-8')
            v = {r['candidate_id']: r['verdict'] for r in audit.sample_read('fake', D)['rows']}
            self.assertEqual(v, {'a': 'none', 'b': 'none', 'd': 'tested_pass', 'e': 'tested_fail'})   # c: gated with no first run is not at the gate yet
            found = {f['id'].split('.')[-1]: f for f in audit.sample_findings('fake', D)}
            self.assertEqual(set(found), {'a', 'b', 'e'})
            self.assertEqual((found['a']['severity'], found['b']['severity'], found['e']['severity']), ('medium', 'high', 'high'))
            for f in found.values():
                self.check_shape(f)
            self.assertIn('back', api.recipe(found['e'])['title'])
            r = api.candidate_update('fake', 'a', {'sample': {'ordered_on': '2026-09-20'}, 'who': 'person'}, D)
            self.assertEqual(r['changes'], ['sample ordered'])
            self.assertEqual({x['candidate_id']: x['verdict'] for x in audit.sample_read('fake', D)['rows']}['a'], 'ordered')
        finally:
            audit.PIPELINE_PATH = self.real2

    def test_kill_memory(self):
        D = date(2026, 9, 27)
        self.assertEqual(audit.content_words('Merino hiking sock 4-Pack', 'a merino sock for hikers'), {'merino', 'hiking', 'hiker'})
        self.real2 = audit.PIPELINE_PATH
        try:
            audit.PIPELINE_PATH = self.tmp
            self.tmp.write_text(json.dumps({'rows': [{'candidate_id': 'k1', 'brand': 'fake', 'name': 'Merino hiking crew sock', 'stage': 'screened', 'angle_text': 'a merino crew for hikers with a blister tab'},
                                                     {'candidate_id': 'n1', 'brand': 'fake', 'name': 'Merino hiking crew, second try', 'stage': 'screened', 'angle_text': 'merino crew for hikers'},
                                                     {'candidate_id': 'n2', 'brand': 'fake', 'name': 'Cotton dress sock', 'stage': 'screened', 'angle_text': 'a thin dress sock'},
                                                     {'candidate_id': 'k2', 'brand': 'fake', 'name': 'Old idea', 'stage': 'killed', 'killed_on': '2026-01-01', 'kill_reason': 'no demand', 'angle_text': 'cotton dress sock thin'}]}), encoding='utf-8')
            r = api.candidate_update('fake', 'k1', {'stage': 'killed', 'kill_reason': 'the margin gate failed twice', 'who': 'person'}, D)
            self.assertEqual(r['changes'], ['screened to killed', 'killed: the margin gate failed twice'])
            km = audit.kill_memory('fake', D)
            k = {x['candidate_id']: x for x in km['rows']}
            self.assertEqual((k['k1']['killed_on'], k['k1']['reason'], k['k1']['in_hold'], k['k1']['hold_until']), ('2026-09-27', 'the margin gate failed twice', True, '2026-12-26'))
            self.assertEqual([x['candidate_id'] for x in k['k1']['lookalikes']], ['n1'])
            self.assertFalse(k['k2']['in_hold'])                          # 269 days: the hold is over, n2 is not flagged
            found = audit.kill_findings('fake', D)
            self.assertEqual([f['id'].split('.')[-1] for f in found], ['n1'])
            self.assertIn('killed 0 days ago because the margin gate failed twice', found[0]['sentence'])
            self.check_shape(found[0])
        finally:
            audit.PIPELINE_PATH = self.real2

    def test_one_sku_first(self):
        D = date(2026, 9, 27)
        self.real2 = audit.PIPELINE_PATH
        try:
            audit.PIPELINE_PATH = self.tmp
            self.tmp.write_text(json.dumps({'rows': [{'candidate_id': 'a', 'brand': 'fake', 'name': 'A', 'stage': 'gated', 'first_run': {'units': 500}, 'variants': 4},
                                                     {'candidate_id': 'b', 'brand': 'fake', 'name': 'B', 'stage': 'gated', 'first_run': {'units': 500}, 'variants': 1},
                                                     {'candidate_id': 'c', 'brand': 'fake', 'name': 'C', 'stage': 'gated', 'variants': 3},
                                                     {'candidate_id': 'd', 'brand': 'fake', 'name': 'D', 'stage': 'go', 'first_run': {'units': 500}, 'variants': 3}]}), encoding='utf-8')
            found = audit.variant_findings('fake', D)
            self.assertEqual([f['id'].split('.')[-1] for f in found], ['a'])     # b is one SKU, c has no first run yet, d is past go
            self.assertIn('4 variants', found[0]['sentence'])
            self.check_shape(found[0])
            self.assertIn('one SKU', api.recipe(found[0])['title'])
            r = api.candidate_update('fake', 'a', {'variants': '1', 'who': 'person'}, D)
            self.assertEqual(r['changes'], ['1 variant'])
            self.assertEqual(audit.variant_findings('fake', D), [])
            self.assertEqual({x['candidate_id']: x['variants'] for x in audit.first_run_read('fake', D, None)['rows']}['a'], 1)
        finally:
            audit.PIPELINE_PATH = self.real2

    def test_custom_packaging_after_proof(self):
        D = date(2026, 9, 27)
        self.real2 = audit.PIPELINE_PATH
        try:
            audit.PIPELINE_PATH = self.tmp
            self.tmp.write_text(json.dumps({'rows': [{'candidate_id': 'a', 'brand': 'fake', 'name': 'A', 'stage': 'gated', 'first_run': {'units': 500, 'format': 'Fully custom printed box, embossed lid'}},
                                                     {'candidate_id': 'b', 'brand': 'fake', 'name': 'B', 'stage': 'gated', 'first_run': {'units': 500, 'format': 'Custom sleeve'}, 'sample': {'ordered_on': '2026-09-01', 'received_on': '2026-09-10', 'through_own_chain': True, 'result': 'pass'}},
                                                     {'candidate_id': 'c', 'brand': 'fake', 'name': 'C', 'stage': 'gated', 'first_run': {'units': 500, 'format': 'Stock blank with a label'}},
                                                     {'candidate_id': 'd', 'brand': 'fake', 'name': 'D', 'stage': 'go', 'first_run': {'units': 500, 'format': 'Custom box'}},
                                                     {'candidate_id': 'e', 'brand': 'fake', 'name': 'E', 'stage': 'gated'}]}), encoding='utf-8')
            self.assertEqual(audit.custom_format('Fully custom printed box, embossed lid'), ['custom', 'printed', 'embossed'])
            self.assertEqual(audit.custom_format('Stock blank'), [])
            read = audit.packaging_read('fake', D)
            self.assertEqual({r['candidate_id']: r['verdict'] for r in read['rows']}, {'a': 'custom_before_proof', 'b': 'custom_after_proof', 'c': 'stock'})   # d is past go, e has no first run
            found = audit.packaging_findings('fake', D)
            self.assertEqual([f['id'].split('.')[-1] for f in found], ['a'])
            self.assertIn('no sample is on file', found[0]['sentence'])
            self.check_shape(found[0])
            rec = api.recipe(found[0])
            self.assertIn('stock packaging', rec['title'])
            self.assertIn('custom, printed, embossed', rec['title'])
            self.assertIn('PROD-R49', api.CANDIDATE_RULES)
            r = api.candidate_update('fake', 'a', {'first_run': {'units': 500, 'format': 'Stock blank with a sleeve'}, 'who': 'person'}, D)
            self.assertIn('first run', ' '.join(r['changes']))
            self.assertEqual(audit.packaging_findings('fake', D), [])
        finally:
            audit.PIPELINE_PATH = self.real2

    def test_audit_memo(self):
        D = date(2026, 9, 27)
        self.real2 = audit.PIPELINE_PATH
        was = audit.MEMO_ON
        try:
            audit.PIPELINE_PATH = self.tmp
            audit.memo_clear()
            audit.MEMO_ON = True
            rows = [{'candidate_id': 'a', 'brand': 'fake', 'name': 'A', 'stage': 'gated', 'first_run': {'units': 500}, 'variants': 4}]
            self.tmp.write_text(json.dumps({'rows': rows}), encoding='utf-8')
            k1 = audit.memo_key('fake', D)
            self.assertEqual(k1, audit.memo_key('fake', D))
            rows[0]['variants'] = 1
            self.tmp.write_text(json.dumps({'rows': rows}), encoding='utf-8')      # a second write inside the same clock tick still changes the key: small files are keyed by content
            self.assertNotEqual(k1, audit.memo_key('fake', D))
            self.assertNotEqual(audit.memo_key('fake', D), audit.memo_key("fake", D - timedelta(days=1)))
            st = audit.memo_stats()
            self.assertEqual((st['runs'], st['served'], st['on']), (0, 0, True))
            self.assertIn('runs once per state', st['rule'])
            # the sample brand through the api: one run, then served, then a run again after a pipeline write
            a1 = api.rank('sample', None)
            n = audit.memo_stats()['runs']
            a2 = api.rank('sample', None)
            self.assertEqual(audit.memo_stats()['runs'], n)
            self.assertGreaterEqual(audit.memo_stats()['served'], 1)
            self.assertEqual([x['id'] for x in a1['actions']], [x['id'] for x in a2['actions']])
            rows[0]['variants'] = 3
            self.tmp.write_text(json.dumps({'rows': rows}), encoding='utf-8')
            api.rank('sample', None)
            self.assertEqual(audit.memo_stats()['runs'], n + 1)
            self.assertLessEqual(audit.memo_stats()['states'], audit.MEMO_KEEP)
            # the caller gets its own copy: mutating it does not leak into the next read
            f1 = audit.run(None, {'ends_on': D.isoformat()}, data=api.sample_data())
            if f1:
                f1[0]['sentence'] = 'changed by the caller'
                f2 = audit.run(None, {'ends_on': D.isoformat()}, data=api.sample_data())
                self.assertNotEqual(f2[0]['sentence'], 'changed by the caller')
            # two reader objects for the same brand and window keep their own state: they never evict each other
            class Other:
                def __init__(self, inner): self.inner = inner
                def __getattr__(self, k): return getattr(self.inner, k)
            other = Other(api.sample_data())
            audit.run(None, {'ends_on': D.isoformat()}, data=api.sample_data())
            audit.run(None, {'ends_on': D.isoformat()}, data=other)
            n2 = audit.memo_stats()['runs']
            audit.run(None, {'ends_on': D.isoformat()}, data=api.sample_data())
            audit.run(None, {'ends_on': D.isoformat()}, data=other)
            self.assertEqual(audit.memo_stats()['runs'], n2)
            audit.MEMO_ON = False
            r = audit.memo_stats()['runs']
            audit.run(None, {'ends_on': D.isoformat()}, data=api.sample_data())
            self.assertEqual(audit.memo_stats()['runs'], r + 1)
        finally:
            audit.MEMO_ON = was
            audit.memo_clear()
            audit.PIPELINE_PATH = self.real2

    def test_launch_readiness(self):
        D = date(2026, 9, 27)
        self.real2 = audit.PIPELINE_PATH
        try:
            audit.PIPELINE_PATH = self.tmp
            full = {'candidate_id': 'a', 'brand': 'fake', 'name': 'A', 'stage': 'go', 'screen_result': {'demand': 'pass', 'competition': 'pass', 'store_fit': 'pass'}, 'angle_text': 'a warmer cuff', 'angle_source': 'review gap on Amazon',
                    'compliance': {'labelling': 'pass', 'category_certification': 'pass'}, 'tech_packs': [{'version': 2, 'tolerances': 'x', 'bom': 'y', 'packaging_cost': 1.2, 'status': 'current'}],
                    'sample': {'ordered_on': '2026-08-01', 'received_on': '2026-08-10', 'through_own_chain': True, 'result': 'pass'}, 'first_run': {'units': 500, 'moq_units': 300, 'format': 'stock sleeve', 'cash_usd': 100, 'lower_moq_option': 'stock blank at 200'},
                    'owner': 'Sam', 'variants': 1, 'planned_price': 20, 'cogs_estimate': 4}
            bare = {'candidate_id': 'b', 'brand': 'fake', 'name': 'B', 'stage': 'go'}
            early = {'candidate_id': 'c', 'brand': 'fake', 'name': 'C', 'stage': 'researched'}
            short = dict(bare, candidate_id='d', name='D', stage='shortlisted', first_run={'units': 100})
            short_nr = dict(bare, candidate_id='e', name='E', stage='shortlisted')
            self.tmp.write_text(json.dumps({'rows': [full, bare, early, short, short_nr]}), encoding='utf-8')
            data = api.sample_data()
            D = audit.last_full_day(data, None)
            rd = audit.Reader(data, None, D)
            read = audit.launch_readiness('fake', data, None, rd, D)
            by = {r['candidate_id']: r for r in read['rows']}
            self.assertNotIn('c', by)                                   # before shortlisted with no first run
            self.assertEqual(sum(1 for i in read['items'] if i['hard']), 8)
            self.assertEqual(len(read['items']), 15)
            self.assertEqual(by['b']['verdict'], 'not_ready')
            self.assertEqual(len(by['b']['hard_open']), 8)
            a = by['a']
            self.assertNotIn('margin', {k for k in a['hard_open']} - {'margin'})   # everything but the margin and ad-cost reads (which need finance inputs) passes
            self.assertEqual([i['status'] for i in a['checklist'] if i['key'] in ('demand_screen', 'angle', 'compliance', 'tech_pack', 'sample', 'first_run', 'owner', 'one_sku', 'kill_hold')], ['pass'] * 9)
            self.assertEqual(next(i for i in a['checklist'] if i['key'] == 'packaging')['status'], 'pass')
            self.assertEqual(read['rows'][0]['stage'], 'go')            # not ready and at go sorts first
            found = audit.readiness_findings('fake', data, None, rd, D)
            ids = [f['id'].split('.')[-1] for f in found]
            self.assertIn('b', ids)
            self.assertIn('d', ids)                                     # shortlisted with a first run decided
            self.assertNotIn('e', ids)                                  # shortlisted, no money committed yet
            fb = next(f for f in found if f['id'].endswith('.b'))
            self.assertEqual(fb['severity'], 'high')
            self.assertIn('8 hard stops open', fb['sentence'])
            self.check_shape(fb)
            rec = api.recipe(fb)
            self.assertEqual(rec['owner'], 'person')
            self.assertIn('hard stop', rec['title'])
            self.assertIn('PROD-R50', api.CANDIDATE_RULES)
            rows = {r['candidate_id']: r for r in api.handoff_rows('fake')}
            self.assertIsNone(rows['a']['readiness'])                  # no data folder for a fake brand: the verdict reads null, never invented
        finally:
            audit.PIPELINE_PATH = self.real2

    def test_price_band_gate(self):
        D = date(2026, 9, 27)
        self.real2 = audit.PIPELINE_PATH
        try:
            audit.PIPELINE_PATH = self.tmp
            self.tmp.write_text(json.dumps({'rows': [{'candidate_id': 'a', 'brand': 'fake', 'name': 'A', 'stage': 'researched', 'planned_price': 8.0},
                                                     {'candidate_id': 'b', 'brand': 'fake', 'name': 'B', 'stage': 'gated', 'planned_price': 14.0},
                                                     {'candidate_id': 'c', 'brand': 'fake', 'name': 'C', 'stage': 'gated', 'planned_price': 14.0, 'price_band_check': 'sells as a bundle part'},
                                                     {'candidate_id': 'd', 'brand': 'fake', 'name': 'D', 'stage': 'screened', 'planned_price': 8.0},
                                                     {'candidate_id': 'e', 'brand': 'fake', 'name': 'E', 'stage': 'gated', 'planned_price': 68.0, 'pack_units': 4},
                                                     {'candidate_id': 'f', 'brand': 'fake', 'name': 'F', 'stage': 'gated'},
                                                     {'candidate_id': 'g', 'brand': 'fake', 'name': 'G', 'stage': 'researched', 'planned_price': 8.0, 'offer_structure': '3-pack at 24'}]}), encoding='utf-8')
            read = audit.price_band_read('fake')
            by = {r['candidate_id']: r['verdict'] for r in read['rows']}
            self.assertEqual(by, {'a': 'reject', 'b': 'caution', 'c': 'below_target', 'd': 'not_yet', 'e': 'in_target', 'f': 'no_price', 'g': 'caution'})
            self.assertEqual(read['rows'][0]['candidate_id'], 'a')
            found = audit.price_band_findings('fake', D)
            self.assertEqual([f['id'].split('.')[-1] for f in found], ['a', 'b', 'g'])
            fa = next(f for f in found if f['id'].endswith('.a'))
            self.assertEqual(fa['severity'], 'high')
            self.assertIn('$8', fa['sentence'])
            self.check_shape(fa)
            self.assertIn('offer structure', api.recipe(fa)['title'])
            fb = next(f for f in found if f['id'].endswith('.b'))
            self.assertIn('caution band', api.recipe(fb)['title'])
            self.assertIn('PROD-R51', api.CANDIDATE_RULES)
            r = api.candidate_update('fake', 'b', {'price_band_check': 'checked: bundle part', 'who': 'person'}, D)
            self.assertIn('price band check set', r['changes'])
            self.assertEqual([f['id'].split('.')[-1] for f in audit.price_band_findings('fake', D)], ['a', 'g'])
        finally:
            audit.PIPELINE_PATH = self.real2

    def test_margin_points_and_cost_basis(self):
        D = date(2026, 9, 27)
        rows = [{'field': 'shipping_label', 'scope': 'carrier_zone', 'scope_key': 'usps:zones_1_4', 'value': 4.0, 'unit': 'usd_per_order', 'effective_from': '2025-01-01', 'effective_to': None},
                {'field': 'packaging', 'scope': 'global', 'scope_key': '', 'value': 1.0, 'unit': 'usd_per_order', 'effective_from': '2025-01-01', 'effective_to': None},
                {'field': 'threepl_pick_pack', 'scope': 'global', 'scope_key': '', 'value': 3.0, 'unit': 'usd_per_order', 'effective_from': '2025-01-01', 'effective_to': None},
                {'field': 'payment_fee_percent', 'scope': 'channel', 'scope_key': 'online_store', 'value': 3.0, 'unit': 'percent', 'effective_from': '2025-01-01', 'effective_to': None},
                {'field': 'payment_fee_fixed', 'scope': 'channel', 'scope_key': 'online_store', 'value': 0.3, 'unit': 'usd_per_order', 'effective_from': '2025-01-01', 'effective_to': None},
                {'field': 'target_contribution_margin', 'scope': 'global', 'scope_key': '', 'value': 25.0, 'unit': 'percent', 'effective_from': '2025-01-01', 'effective_to': None}]
        fin = metrics.finance.Finance(rows)
        cand = {'candidate_id': 'a', 'name': 'A', 'category': 'socks', 'stage': 'gated', 'planned_price': 20.0, 'price_low': 8.0, 'price_high': 24.0, 'cogs_estimate': 4.0, 'bulk_cogs': 3.0, 'pack_units': 1}
        pts = audit.margin_points(cand, fin, None, D.isoformat(), 2.0, 25.0)
        self.assertEqual(pts['planned']['price'], 20.0)
        self.assertTrue(pts['planned']['passes'])
        self.assertFalse(pts['low']['passes'])                       # 8 - 4 cost - 4 fulfilment - 0.39 fee is under water
        self.assertEqual(pts['low']['contribution_usd'], -0.39)
        self.assertGreater(pts['bulk']['margin_pct'], pts['planned']['margin_pct'])
        self.assertEqual(audit.margin_points({'planned_price': 20.0}, fin, None, D.isoformat(), 2.0, 25.0)['low']['unavailable'], 'not entered')
        self.assertEqual(audit.cost_basis({'cogs_estimate': 4.0}, {'value': 4.0}), 'estimate')
        self.assertEqual(audit.cost_basis({'cogs_estimate': 4.0, 'cogs_source': 'quote'}, {'value': 4.0}), 'quote')
        self.assertEqual(audit.cost_basis({}, {'value': 4.0}), 'category_median')
        self.assertEqual(audit.cost_basis({}, {'value': None}), 'none')
        self.assertIn('PROD-R52', api.CANDIDATE_RULES)
        self.assertIn('PROD-R53', api.CANDIDATE_RULES)
        self.tmp.write_text(json.dumps({'rows': [dict(cand, brand='fake')]}), encoding='utf-8')
        self.assertEqual(api.candidate_update('fake', 'a', {'cogs_source': 'nonsense', 'who': 'person'}, D)[0], 400)
        self.assertEqual(api.candidate_update('fake', 'a', {'quote_on': 'yesterday', 'who': 'person'}, D)[0], 400)
        r = api.candidate_update('fake', 'a', {'cogs_source': 'quote', 'quote_on': '2026-09-20', 'price_low': '9', 'who': 'person'}, D)
        self.assertEqual(r['changes'], ['price low set', 'cost source quote', 'quote date set'])
        self.assertEqual((r['candidate']['cogs_source'], r['candidate']['quote_on'], r['candidate']['price_low']), ('quote', '2026-09-20', 9.0))

    def test_identical_sellers_cash_test(self):
        D = date(2026, 9, 27)
        self.real2 = audit.PIPELINE_PATH
        saved = audit.listing_pull
        try:
            audit.PIPELINE_PATH = self.tmp
            self.tmp.write_text(json.dumps({'rows': [{'candidate_id': 'a', 'brand': 'fake', 'name': 'Merino calf sock with a wear-life promise', 'stage': 'researched'},
                                                     {'candidate_id': 'b', 'brand': 'fake', 'name': 'Merino calf sock, planned', 'stage': 'gated', 'cash_test_plan': '3 weeks, $2,000 cap, stop when contribution is under ad cost for 7 days'},
                                                     {'candidate_id': 'c', 'brand': 'fake', 'name': 'Holiday gift box', 'stage': 'gated'},
                                                     {'candidate_id': 'd', 'brand': 'fake', 'name': 'Merino calf sock, screened', 'stage': 'screened'}]}), encoding='utf-8')
            live = {'brand': 'fake', 'mode': 'live', 'captured_at': '2026-09-27', 'rows': [{'asin': 'B1', 'title': 'Merino Wool Calf Socks 3-Pack', 'seller': 'Shop One', 'offers_count': 14},
                                                                                            {'asin': 'B2', 'title': 'Merino Calf Sock Men', 'seller': 'Shop Two', 'offers_count': None}]}
            audit.listing_pull = lambda: live
            read = audit.identical_sellers_read('fake', None)
            by = {r['candidate_id']: r for r in read['rows']}
            self.assertNotIn('d', by)
            self.assertEqual((by['a']['verdict'], by['a']['sellers'], by['a']['basis']), ('cash_test', 14, 'offer count on the listing'))
            self.assertEqual([m['asin'] for m in by['a']['matches']], ['B1', 'B2'])
            self.assertEqual(by['b']['verdict'], 'cash_test_planned')
            self.assertEqual(by['c']['verdict'], 'no_match')
            found = audit.identical_seller_findings('fake', None, D)
            self.assertEqual([f['id'].split('.')[-1] for f in found], ['a'])
            self.assertIn('14 sellers', found[0]['sentence'])
            self.check_shape(found[0])
            self.assertIn('cash test', api.recipe(found[0])['title'])
            self.assertIn('PROD-R54', api.CANDIDATE_RULES)
            # distinct sellers count when no listing carries an offer count
            live['rows'] = [{'asin': f'B{i}', 'title': 'Merino Calf Sock', 'seller': f'Shop {i}', 'offers_count': None} for i in range(10)]
            self.assertEqual((audit.identical_sellers_read('fake', None)['rows'][0]['sellers'], audit.identical_sellers_read('fake', None)['rows'][0]['basis']), (10, 'distinct sellers across matching listings'))
            # a mock pull never counts
            live['mode'] = 'mock'
            self.assertEqual({r['verdict'] for r in audit.identical_sellers_read('fake', None)['rows']}, {'not_read'})
            self.assertEqual(audit.identical_seller_findings('fake', None, D), [])
        finally:
            audit.listing_pull = saved
            audit.PIPELINE_PATH = self.real2

    def test_sourcing_channel_comparison(self):
        D = date(2026, 9, 27)
        self.real2 = audit.PIPELINE_PATH
        try:
            audit.PIPELINE_PATH = self.tmp
            self.tmp.write_text(json.dumps({'rows': [{'candidate_id': 'a', 'brand': 'fake', 'name': 'A', 'stage': 'gated', 'first_run': {'units': 500}},
                                                     {'candidate_id': 'b', 'brand': 'fake', 'name': 'B', 'stage': 'gated', 'first_run': {'units': 500}, 'sourcing': {'channel': 'agent', 'cost_usd': 4.0, 'days': 45}},
                                                     {'candidate_id': 'c', 'brand': 'fake', 'name': 'C', 'stage': 'go', 'first_run': {'units': 500}, 'sourcing': {'channel': 'agent', 'cost_usd': 4.0, 'days': 45, 'alternatives': [{'channel': 'domestic', 'cost_usd': 6.5, 'days': 12, 'branding': 'label only'}]}},
                                                     {'candidate_id': 'd', 'brand': 'fake', 'name': 'D', 'stage': 'gated'}]}), encoding='utf-8')
            read = audit.sourcing_read('fake')
            by = {r['candidate_id']: r for r in read['rows']}
            self.assertNotIn('d', by)                                   # no first run decided yet
            self.assertEqual((by['a']['verdict'], by['b']['verdict'], by['c']['verdict']), ('no_channel', 'one_channel', 'compared'))
            self.assertEqual((by['c']['cheapest'], by['c']['fastest']), ('sourcing agent', 'domestic supplier'))
            self.assertEqual(read['rows'][0]['candidate_id'], 'a')
            found = audit.sourcing_findings('fake', D)
            self.assertEqual([f['id'].split('.')[-1] for f in found], ['a', 'b'])
            self.assertIn('no sourcing channel', found[0]['sentence'])
            self.check_shape(found[0])
            self.assertIn('sourcing channel', api.recipe(found[0])['title'])
            self.assertIn('Compare sourcing agent', api.recipe(found[1])['title'])
            self.assertIn('PROD-R55', api.CANDIDATE_RULES)
            self.assertEqual(api.candidate_update('fake', 'a', {'sourcing': {'channel': 'moon'}, 'who': 'person'}, D)[0], 400)
            r = api.candidate_update('fake', 'a', {'sourcing': {'channel': 'marketplace_direct', 'cost_usd': '3.8', 'days': '60', 'alternatives': [{'channel': 'domestic', 'cost_usd': '6', 'days': '10'}, {'channel': ''}]}, 'who': 'person'}, D)
            self.assertEqual(r['changes'], ['sourcing marketplace_direct, 1 alternative'])
            self.assertEqual(audit.sourcing_read('fake')['rows'][-1]['verdict'], 'compared')
            self.assertEqual([f['id'].split('.')[-1] for f in audit.sourcing_findings('fake', D)], ['b'])
        finally:
            audit.PIPELINE_PATH = self.real2

    def test_requote_steps(self):
        D = date(2026, 9, 27)
        self.real2 = audit.PIPELINE_PATH
        try:
            audit.PIPELINE_PATH = self.tmp
            self.tmp.write_text(json.dumps({'rows': [{'candidate_id': 'a', 'brand': 'fake', 'name': 'A', 'stage': 'go', 'units_ordered': 1200, 'cogs_source': 'quote', 'quote_units': 500, 'quote_on': '2026-03-01'},
                                                     {'candidate_id': 'b', 'brand': 'fake', 'name': 'B', 'stage': 'go', 'units_ordered': 600, 'cogs_source': 'quote', 'quote_units': 1000},
                                                     {'candidate_id': 'c', 'brand': 'fake', 'name': 'C', 'stage': 'go', 'units_ordered': 700, 'cogs_source': 'estimate'},
                                                     {'candidate_id': 'd', 'brand': 'fake', 'name': 'D', 'stage': 'gated', 'cogs_source': 'quote'},
                                                     {'candidate_id': 'e', 'brand': 'fake', 'name': 'E', 'stage': 'go', 'units_ordered': 400, 'cogs_source': 'quote'}]}), encoding='utf-8')
            read = audit.requote_read('fake')
            by = {r['candidate_id']: r for r in read['rows']}
            self.assertEqual({k: v['verdict'] for k, v in by.items()}, {'a': 'requote_due', 'b': 'covered', 'c': 'no_quote', 'd': 'no_orders', 'e': 'covered'})
            self.assertEqual((by['a']['crossed'], by['a']['next_step'], by['e']['next_step']), ([500, 1000], None, 500))
            found = audit.requote_findings('fake', D)
            self.assertEqual([f['id'].split('.')[-1] for f in found], ['a'])
            self.assertIn('1,200 units ordered in total, past the 1,000 step, on a quote for 500 units from 2026-03-01', found[0]['sentence'])
            self.check_shape(found[0])
            self.assertIn('Re-quote A at 1,200 units', api.recipe(found[0])['title'])
            self.assertIn('PROD-R56', api.CANDIDATE_RULES)
            r = api.candidate_update('fake', 'e', {'units_add': '150', 'who': 'person'}, D)
            self.assertEqual(r['changes'], ['150 units ordered, 550 in total'])
            self.assertEqual({x['candidate_id']: x['verdict'] for x in audit.requote_read('fake')['rows']}['e'], 'requote_due')    # a quote with no units on it does not cover a crossed step
            r = api.candidate_update('fake', 'e', {'quote_units': 1000, 'who': 'person'}, D)
            self.assertEqual({x['candidate_id']: x['verdict'] for x in audit.requote_read('fake')['rows']}['e'], 'covered')
            self.assertEqual(api.candidate_update('fake', 'e', {'units_add': '-5', 'who': 'person'}, D)[0], 400)
        finally:
            audit.PIPELINE_PATH = self.real2

    def test_cost_floor(self):
        self.real2 = audit.PIPELINE_PATH
        try:
            audit.PIPELINE_PATH = self.tmp
            self.tmp.write_text(json.dumps({'rows': [{'candidate_id': 'a', 'brand': 'fake', 'name': 'A', 'stage': 'gated', 'cogs_estimate': 9.0, 'cost_floor': {'usd': 3.0, 'source': 'alibaba listing', 'on': '2026-09-01'}},
                                                     {'candidate_id': 'b', 'brand': 'fake', 'name': 'B', 'stage': 'gated', 'cogs_estimate': 5.0, 'cost_floor': {'usd': 3.0}},
                                                     {'candidate_id': 'c', 'brand': 'fake', 'name': 'C', 'stage': 'gated', 'cogs_estimate': 5.0},
                                                     {'candidate_id': 'd', 'brand': 'fake', 'name': 'D', 'stage': 'researched', 'cogs_estimate': 5.0},
                                                     {'candidate_id': 'e', 'brand': 'fake', 'name': 'E', 'stage': 'gated', 'cost_floor': {'usd': 3.0}}]}), encoding='utf-8')
            data = api.sample_data()
            D = audit.last_full_day(data, None)
            rd = audit.Reader(data, None, D)
            read = audit.cost_floor_read('fake', data, None, rd, D)
            by = {r['candidate_id']: r for r in read['rows']}
            self.assertNotIn('d', by)
            self.assertEqual({k: v['verdict'] for k, v in by.items()}, {'a': 'above', 'b': 'in_line', 'c': 'no_check', 'e': 'no_cost'})
            self.assertEqual(by['a']['multiple'], 3.0)
            found = audit.cost_floor_findings('fake', data, None, rd, D)
            self.assertEqual([(f['id'].split('.')[-1], f['severity']) for f in found], [('a', 'medium'), ('c', 'low')])
            self.assertIn('3 times the $3.00', found[0]['sentence'])
            self.check_shape(found[0])
            self.assertIn('Re-source A', api.recipe(found[0])['title'])
            self.assertIn('reverse-image search', api.recipe(found[1])['title'])
            self.assertIn('PROD-R57', api.CANDIDATE_RULES)
            r = api.candidate_update('fake', 'c', {'cost_floor': {'usd': '2.5', 'source': 'reverse-image search, supplier marketplace'}, 'who': 'person'}, D)
            self.assertEqual(r['changes'], ['cost floor $2.50'])
            self.assertEqual({x['candidate_id']: x['verdict'] for x in audit.cost_floor_read('fake', data, None, rd, D)['rows']}['c'], 'in_line')
            self.assertEqual(api.candidate_update('fake', 'c', {'cost_floor': {'usd': 0}, 'who': 'person'}, D)[0], 400)
        finally:
            audit.PIPELINE_PATH = self.real2

    def test_post_launch_read_before_the_test(self):
        D = date(2026, 9, 27)
        self.real2 = audit.PIPELINE_PATH
        try:
            audit.PIPELINE_PATH = self.tmp
            full = {'metric': 'units', 'direction': 'up', 'floor': 300, 'read_on': '2026-12-15', 'owner': 'Sam'}
            self.tmp.write_text(json.dumps({'rows': [{'candidate_id': 'a', 'brand': 'fake', 'name': 'A', 'stage': 'go'},
                                                     {'candidate_id': 'b', 'brand': 'fake', 'name': 'B', 'stage': 'shortlisted', 'launch_target': '2026-11-20', 'post_launch': {'metric': 'units', 'floor': 300}},
                                                     {'candidate_id': 'c', 'brand': 'fake', 'name': 'C', 'stage': 'go', 'post_launch': full},
                                                     {'candidate_id': 'd', 'brand': 'fake', 'name': 'D', 'stage': 'gated'}]}), encoding='utf-8')
            self.assertEqual(audit.post_launch_read_of({'post_launch': full})['complete'], True)
            self.assertEqual(audit.post_launch_read_of({'post_launch': {'metric': 'moon', 'floor': 1}})['missing'], ['metric', 'direction', 'read date', 'owner'])
            found = audit.post_launch_findings('fake', D)
            self.assertEqual([f['id'].split('.')[-1] for f in found], ['a', 'b'])
            self.assertIn('set to launch 2026-11-20', found[1]['sentence'])
            self.assertIn('missing: direction, read date, owner', found[1]['sentence'])
            self.check_shape(found[0])
            self.assertEqual(api.recipe(found[0])['owner'], 'person')
            self.assertIn('PROD-R58', api.CANDIDATE_RULES)
            self.assertEqual(api.candidate_update('fake', 'a', {'post_launch': {'metric': 'moon'}, 'who': 'person'}, D)[0], 400)
            self.assertEqual(api.candidate_update('fake', 'a', {'post_launch': {'metric': 'units', 'direction': 'sideways'}, 'who': 'person'}, D)[0], 400)
            r = api.candidate_update('fake', 'a', {'post_launch': full, 'who': 'person'}, D)
            self.assertEqual(r['changes'], ['post-launch read set'])
            self.assertEqual([f['id'].split('.')[-1] for f in audit.post_launch_findings('fake', D)], ['b'])
            # the proposed test takes the metric and the read date from the candidate
            row = next(c for c in audit.pipeline('fake') if c['candidate_id'] == 'a')
            t = api.propose_test('fake', row, D)
            self.assertEqual((t['metric']['name'], t['metric']['direction'], t['metric']['floor'], t['read_point']), ('units', 'up', 300.0, '2026-12-15'))
            # the readiness checklist carries it as a soft item
            data = api.sample_data()
            E = audit.last_full_day(data, None)
            rows = {r['candidate_id']: r for r in audit.launch_readiness('fake', data, None, audit.Reader(data, None, E), E)['rows']}
            items = {i['key']: i for i in rows['a']['checklist']}
            self.assertEqual((items['post_launch']['status'], items['post_launch']['hard']), ('pass', False))
            self.assertIn('units up 300 by 2026-12-15, read by Sam', items['post_launch']['why'])
            self.assertEqual({i['key']: i['status'] for i in rows['b']['checklist']}['post_launch'], 'open')
        finally:
            audit.PIPELINE_PATH = self.real2

    def test_quick_screen_before_research_time(self):
        D = date(2026, 9, 27)
        self.real2 = audit.PIPELINE_PATH
        try:
            audit.PIPELINE_PATH = self.tmp
            allyes = {k: True for k, _ in audit.QUICK_SCREEN_POINTS}
            self.tmp.write_text(json.dumps({'rows': [{'candidate_id': 'a', 'brand': 'fake', 'name': 'A', 'stage': 'screened', 'hours_logged': 2.0},
                                                     {'candidate_id': 'b', 'brand': 'fake', 'name': 'B', 'stage': 'researched', 'hours_logged': 0, 'quick_screen': dict(allyes, weight_size=False)},
                                                     {'candidate_id': 'c', 'brand': 'fake', 'name': 'C', 'stage': 'screened', 'hours_logged': 0},
                                                     {'candidate_id': 'd', 'brand': 'fake', 'name': 'D', 'stage': 'gated', 'hours_logged': 5, 'quick_screen': allyes},
                                                     {'candidate_id': 'e', 'brand': 'fake', 'name': 'E', 'stage': 'researched', 'hours_logged': 1, 'quick_screen': {'felt_problem': True}}]}), encoding='utf-8')
            read = audit.quick_screen_read('fake')
            by = {r['candidate_id']: r for r in read['rows']}
            self.assertEqual(len(read['points']), 10)
            self.assertEqual({k: v['verdict'] for k, v in by.items()}, {'a': 'not_run', 'b': 'drops', 'c': 'not_run', 'd': 'clear', 'e': 'partial'})
            self.assertEqual({k: v['research_before_screen'] for k, v in by.items()}, {'a': True, 'b': False, 'c': False, 'd': False, 'e': True})
            self.assertEqual(by['b']['no'], ['weight_size'])
            found = audit.quick_screen_findings('fake', D)
            self.assertEqual(sorted(f['id'].split('.')[-1] for f in found), ['a', 'e'])
            fa = next(f for f in found if f['id'].endswith('.a'))
            self.assertIn('2 research hours logged at screened with 0 of 10', fa['sentence'])
            self.assertEqual(fa['severity'], 'low')
            self.check_shape(fa)
            self.assertIn('quick screen', api.recipe(fa)['title'])
            self.assertIn('PROD-R59', api.CANDIDATE_RULES)
            r = api.candidate_update('fake', 'a', {'quick_screen': {'felt_problem': 'y', 'not_novelty': 'n', 'moon': 'y'}, 'who': 'person'}, D)
            self.assertEqual(r['changes'], ['quick screen 2 of 10, no on not_novelty'])
            self.assertEqual(audit.quick_screen_of(r['candidate'])['verdict'], 'drops')
            r = api.candidate_update('fake', 'a', {'quick_screen': {k: 'yes' for k, _ in audit.QUICK_SCREEN_POINTS}, 'who': 'person'}, D)
            self.assertEqual(audit.quick_screen_of(r['candidate'])['verdict'], 'clear')
            self.assertEqual(sorted(f['id'].split('.')[-1] for f in audit.quick_screen_findings('fake', D)), ['e'])
        finally:
            audit.PIPELINE_PATH = self.real2

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

    def test_tech_pack_versions_and_rule(self):
        today = date(2026, 9, 28)
        code, out = api.candidate_add('fake', {'name': 'Spec me', 'category': 'socks', 'planned_price': 20}, today)
        cid = out['candidate']['candidate_id']
        api.candidate_update('fake', cid, {'stage': 'gated'}, today)
        fs = audit.tech_pack_findings('fake', today)
        self.assertEqual([f['entity']['id'] for f in fs], [cid])
        self.assertIn('no spec yet', fs[0]['sentence'])
        self.check_shape(fs[0])
        r = api.candidate_update('fake', cid, {'tech_pack': {'tolerances': 'length plus or minus 5 mm', 'bom': '', 'packaging_cost': 0.4}}, today)
        self.assertEqual(r['candidate']['tech_packs'][-1]['version'], 'v1')
        self.assertEqual(audit.tech_pack_status(r['candidate'])['status'], 'partial')
        self.assertIn('bom', audit.tech_pack_status(r['candidate'])['missing'])
        self.assertTrue(audit.tech_pack_findings('fake', today))
        r = api.candidate_update('fake', cid, {'tech_pack': {'tolerances': 'length plus or minus 5 mm', 'bom': '62% cotton, 33% nylon, 5% spandex', 'packaging_cost': 0.4}}, today)
        packs = r['candidate']['tech_packs']
        self.assertEqual([p['version'] for p in packs], ['v1', 'v2'])
        self.assertEqual([p['status'] for p in packs], ['superseded', 'current'])
        self.assertEqual(audit.tech_pack_status(r['candidate'])['status'], 'current')
        self.assertEqual(audit.tech_pack_findings('fake', today), [])

    def test_hours_budget_and_sprawl(self):
        self.assertEqual(audit.hours_budget(None)[0], audit.DEFAULT_HOURS_BUDGET)
        self.tmp.write_text(json.dumps({'rows': [{'candidate_id': 'a', 'brand': 'fake', 'name': 'Sprawl', 'stage': 'researched', 'hours_logged': 25.0},
                                                 {'candidate_id': 'b', 'brand': 'fake', 'name': 'Fine', 'stage': 'researched', 'hours_logged': 10.0},
                                                 {'candidate_id': 'c', 'brand': 'fake', 'name': 'Dead', 'stage': 'killed', 'hours_logged': 99.0}]}), encoding='utf-8')
        t = audit.hours_table('fake', None)
        by = {r['candidate_id']: r for r in t['rows']}
        self.assertEqual(by['a']['hours_allowed'], 20)     # 4 screened plus 16 researched
        self.assertEqual(by['a']['over_by'], 5.0)
        self.assertEqual(by['b']['over_by'], 0)
        fs = audit.hours_findings('fake', None, date(2026, 9, 27))
        self.assertEqual([f['entity']['id'] for f in fs], ['a'])
        self.assertIn('25 research hours against 20', fs[0]['sentence'])
        self.check_shape(fs[0])

    def test_funnel_counts_stages_reached(self):
        rows = [audit.candidate_view(r, date(2026, 9, 27)) for r in [
            {'candidate_id': 'a', 'name': 'a', 'stage': 'gated', 'screen_in_date': '2026-09-20', 'time_box_days': 10},
            {'candidate_id': 'b', 'name': 'b', 'stage': 'screened', 'screen_in_date': '2026-09-20', 'time_box_days': 10},
            {'candidate_id': 'c', 'name': 'c', 'stage': 'killed', 'screen_in_date': '2026-09-01', 'time_box_days': 3}]]
        self.assertEqual([f['n'] for f in audit.pipeline_funnel(rows)], [2, 1, 1, 0, 0])
        self.assertFalse(rows[2]['over_box'])   # killed candidates never stall


class Req:
    def __init__(self, path, brand='bombas', method='GET', body=None):
        self.method, self.path, self.query, self.data, self.body = method, path, {'brand': [brand]}, None, body or {}

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


class DecisionMemoryTest(unittest.TestCase):
    """The founder's choices in the shared decisions log ride on the plan: a "not now" parks an action for 14 days."""

    def test_not_now_parks_and_returns(self):
        base = api.rank('bombas', {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4})['actions']
        target = base[0]
        tmp = ROOT / 'tests' / '_decisions_test.json'
        saved = api.DECISIONS_PATH
        try:
            tmp.write_text(json.dumps([
                {'screen': '01-market-research', 'capability': target['capability']['id'], 'choice': 'not_now', 'reason': 'after the holiday push', 'time': '2026-09-20T10:00:00Z', 'finding_id': target['id']},
                {'screen': '01-market-research', 'capability': base[1]['capability']['id'], 'choice': 'person', 'reason': '', 'time': '2026-09-21T10:00:00Z', 'finding_id': base[1]['id']},
                {'screen': '01-market-research', 'capability': base[2]['capability']['id'], 'choice': 'not_now', 'reason': 'old', 'time': '2026-08-01T10:00:00Z', 'finding_id': base[2]['id']}]), encoding='utf-8')
            api.DECISIONS_PATH = tmp
            r = api.rank('bombas', {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4})
            ids = [a['id'] for a in r['actions']]
            self.assertNotIn(target['id'], ids)                       # parked, off the plan
            self.assertEqual([a['id'] for a in r['parked']], [target['id']])
            self.assertEqual(r['parked'][0]['returns_on'], '2026-10-04')
            self.assertEqual(r['parked'][0]['decision']['reason'], 'after the holiday push')
            kept = next(a for a in r['actions'] if a['id'] == base[1]['id'])
            self.assertEqual(kept['decision']['choice'], 'person')     # a person choice stays, on the card
            self.assertIn(base[2]['id'], ids)                          # an old "not now" has expired
            self.assertEqual(r['decided'], 2)   # the person choice and the expired not-now both stay visible on their cards
            self.assertEqual(api.handle(Req(['parked']))['parked'][0]['id'], target['id'])
        finally:
            api.DECISIONS_PATH = saved
            tmp.unlink(missing_ok=True)

    def test_decisions_on_desk(self):
        base = api.rank('bombas', {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4})['actions']
        tmp = ROOT / 'tests' / '_decisions_desk.json'
        saved = api.DECISIONS_PATH
        try:
            tmp.write_text(json.dumps([
                {'screen': '01-market-research', 'capability': base[0]['capability']['id'], 'choice': 'person', 'reason': 'Sam takes it', 'time': '2026-09-21T10:00:00Z', 'finding_id': base[0]['id']},
                {'screen': '01-market-research', 'capability': base[1]['capability']['id'], 'choice': 'not_now', 'reason': 'later', 'time': '2026-09-22T10:00:00Z', 'finding_id': base[1]['id']},
                {'screen': '01-market-research', 'capability': 'PROD-C99', 'choice': 'agent', 'reason': '', 'time': '2026-08-01T10:00:00Z', 'finding_id': '01-market-research.PROD-R99.gone'},
                {'screen': '05-brand-brain', 'capability': 'BRAIN-C01', 'choice': 'agent', 'reason': '', 'time': '2026-09-23T10:00:00Z'}]), encoding='utf-8')
            api.DECISIONS_PATH = tmp
            d = api.decisions_on_desk(None, 'bombas')
            self.assertEqual(d['total_on_screen'], 3)                              # the brain screen's decision is not ours
            self.assertEqual([x['on'] for x in d['rows']], ['2026-09-22', '2026-09-21', '2026-08-01'])   # newest first
            self.assertEqual([x['state'] for x in d['rows']], ['parked', 'open', 'gone'])
            self.assertEqual(d['rows'][1]['title'], base[0]['title'])
            self.assertEqual(d['counts'], {'agent': 1, 'person': 1, 'not_now': 1})
        finally:
            api.DECISIONS_PATH = saved
            tmp.unlink(missing_ok=True)

    def test_no_log_means_nothing_parked(self):
        saved = api.DECISIONS_PATH
        try:
            api.DECISIONS_PATH = ROOT / 'tests' / '_no_such_decisions.json'
            r = api.rank('bombas', {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4})
            self.assertEqual(r['parked'], [])
            self.assertEqual(r['decided'], 0)
        finally:
            api.DECISIONS_PATH = saved


class AnswerTest(unittest.TestCase):
    """A founder answer goes through the brain store into a temp brain root, never the shared one."""

    def _brain(self):
        import tempfile, sys
        root = Path(tempfile.mkdtemp())
        (root / 'fake').mkdir()
        (root / 'fake' / 'open_questions.json').write_text(json.dumps([{'id': 'fake.open_questions.ladder_durability_3', 'brand': 'fake', 'section': 'open_questions', 'field': 'ladder_durability_3',
            'value': {'question': 'What proof answers "will it last"?', 'who_can_answer': 'the founder', 'asked_on': None, 'answered_on': None}, 'text': 'What proof answers "will it last"?', 'tier': 'unverified', 'status': 'active'}]), encoding='utf-8')
        (root / 'fake' / 'claims.json').write_text('[]', encoding='utf-8')
        sys.path.insert(0, str(ROOT / 'app' / 'brain'))
        import store
        return store.Brain('fake', root=root), root

    def test_claim_written_and_question_closed(self):
        br, root = self._brain()
        code, out = api.answer_question('fake', {'question_id': 'fake.open_questions.ladder_durability_3', 'answer': 'Every pair carries the Happiness Guarantee: a hole inside a year is replaced.', 'kind': 'claim', 'who': 'kevin'}, date(2026, 9, 28), brain=br)
        self.assertEqual(code, 201, out)
        self.assertEqual(out['written'], ['fake.claims.answer_ladder_durability_3'])
        rec = br.get('fake.claims.answer_ladder_durability_3')
        self.assertEqual((rec['tier'], rec['status'], rec['source']['type'], rec['added_by']), ('approved', 'active', 'founder', 'kevin'))
        q = br.get('fake.open_questions.ladder_durability_3')
        self.assertEqual((q['value']['answered_on'], q['value']['asked_on'], q['value']['answer_kind']), ('2026-09-28', '2026-09-28', 'claim'))
        self.assertEqual(audit.open_questions(br, date(2026, 9, 28))['rows'][0]['verdict'], 'answered')

    def test_none_marks_answered_without_a_record(self):
        br, root = self._brain()
        code, out = api.answer_question('fake', {'question_id': 'fake.open_questions.ladder_durability_3', 'answer': 'No proof yet; it is a product problem.', 'kind': 'none'}, date(2026, 9, 28), brain=br)
        self.assertEqual((code, out['written']), (201, []))
        self.assertEqual(br.get('fake.open_questions.ladder_durability_3')['value']['answered_on'], '2026-09-28')
        self.assertEqual(br.records('claims'), [])

    def test_refusals(self):
        br, root = self._brain()
        self.assertEqual(api.answer_question('fake', {'question_id': 'fake.open_questions.nope', 'answer': 'x', 'kind': 'claim'}, date(2026, 9, 28), brain=br)[0], 404)
        self.assertEqual(api.answer_question('fake', {'question_id': 'fake.open_questions.ladder_durability_3', 'answer': '', 'kind': 'claim'}, date(2026, 9, 28), brain=br)[0], 400)
        self.assertEqual(api.answer_question('fake', {'question_id': 'fake.open_questions.ladder_durability_3', 'answer': 'x', 'kind': 'rumour'}, date(2026, 9, 28), brain=br)[0], 400)
        self.assertEqual(api.answer_question(None, {'question_id': 'x', 'answer': 'x'}, date(2026, 9, 28))[0], 400)


class ChangesTest(unittest.TestCase):
    def test_snapshot_and_diff(self):
        saved = api.SEEN_DIR
        api.SEEN_DIR = ROOT / 'tests' / '_seen'
        try:
            c0 = api.handle(Req(['changes']))
            self.assertFalse(c0['available'])
            code, snap = api.handle(Req(['snapshot'], method='POST'))
            self.assertEqual(code, 201)
            self.assertGreater(snap['findings'], 50)
            c1 = api.handle(Req(['changes']))
            self.assertTrue(c1['available'])
            self.assertTrue(c1['quiet'])
            # doctor the snapshot: drop one finding, add a stale one, lower one severity, halve one stake
            p = api._seen_path('bombas')
            doc = json.loads(p.read_text(encoding='utf-8'))
            ids = list(doc['findings'])
            dropped = ids[0]
            del doc['findings'][dropped]
            doc['findings']['01-market-research.PROD-R99.gone'] = {'severity': 'low', 'status': 'open', 'stake_usd': None, 'sentence': 'an old finding'}
            hi = next(i for i in ids[1:] if doc['findings'][i]['severity'] in ('high', 'critical'))
            doc['findings'][hi]['severity'] = 'low'
            st = next(i for i in ids[1:] if doc['findings'][i]['stake_usd'])
            doc['findings'][st]['stake_usd'] = doc['findings'][st]['stake_usd'] / 2
            p.write_text(json.dumps(doc), encoding='utf-8')
            c2 = api.handle(Req(['changes']))
            self.assertEqual([x['id'] for x in c2['new']], [dropped])
            self.assertEqual([x['id'] for x in c2['gone']], ['01-market-research.PROD-R99.gone'])
            self.assertIn(hi, [x['id'] for x in c2['worse']])
            self.assertIn(st, [x['id'] for x in c2['stake_moves']])
            self.assertFalse(c2['quiet'])
        finally:
            import shutil
            shutil.rmtree(api.SEEN_DIR, ignore_errors=True)
            api.SEEN_DIR = saved


class WeeklyNoteTest(unittest.TestCase):
    def test_weekly_note_writes_and_lists(self):
        import importlib.util as iu, tempfile
        spec = iu.spec_from_file_location('weekly_t', SCREEN / 'weekly.py')
        wk = iu.module_from_spec(spec)
        spec.loader.exec_module(wk)
        saved = wk.REPORTS_DIR
        wk.REPORTS_DIR = Path(tempfile.mkdtemp())
        try:
            note = wk.build('bombas', api)
            self.assertIn('# Research desk', note['text'])
            self.assertIn('WEEK PLAN', note['text'])
            p = wk.write('bombas', api)
            self.assertTrue(p.is_file())
            self.assertEqual(p.stem, note['date'])
            self.assertEqual([r['date'] for r in wk.past('bombas')], [note['date']])
            self.assertEqual(wk.past('nobody'), [])
            s = wk.build(None, api)
            self.assertIn('Tallgrass Goods', s['text'])
        finally:
            wk.REPORTS_DIR = saved
        r = api.handle(Req(['reports']))
        self.assertIn('weekly.py --brand bombas', r['command'])


class WeekPlanTest(unittest.TestCase):
    def test_week_plan(self):
        w = api.handle(Req(['week']))
        t = w['text']
        for head in ('WEEK PLAN', 'DUE (', 'THE TOP 5 THIS WEEK', 'HOURS LEFT', 'SPEND THIS WEEK', 'PULLS A PERSON CAN APPROVE'):
            self.assertIn(head, t)
        self.assertTrue(all(i['days'] <= 7 for i in w['due']))
        self.assertEqual(len(w['top']), 5)
        self.assertTrue(w['hours'])
        self.assertIsNotNone(w['spend']['cap'])
        fits = [p for p in w['pulls'] if p['fits'] is True]
        self.assertTrue(all((p['estimate_usd'] or 0) <= (w['spend']['left'] if w['spend']['left'] is not None else w['spend']['cap']) for p in fits))
        s = api.handle(Req(['week'], brand='sample'))
        self.assertIn('ledger or cap unavailable', s['text'])


class CalendarTest(unittest.TestCase):
    def test_calendar_lists_every_dated_thing(self):
        c = api.handle(Req(['calendar']))
        kinds = {i['kind'] for i in c['items']}
        self.assertTrue({'time_box', 'review', 'check', 'pull'} <= kinds, kinds)
        self.assertIn('window', kinds)                      # 1 Nov is inside 45 days of 27 Sep
        self.assertEqual(c['items'], sorted(c['items'], key=lambda i: (i['when'], i['kind'], i['title'])))
        self.assertTrue(all(i['days'] <= c['horizon_days'] for i in c['items']))
        self.assertGreaterEqual(c['overdue'], 1)            # the seeded gift box is past its 7-day box
        self.assertTrue(all(i['action_id'] for i in c['items'] if i['kind'] in ('review', 'check') or (i['kind'] == 'time_box' and i['days'] < 0)))   # a card whenever a rule fires or the candidate has one
        s = api.handle(Req(['calendar'], brand='sample'))
        self.assertEqual([i['kind'] for i in s['items'] if i['kind'] not in ('pull', 'window', 'check')], [])   # no candidates on the sample brand


class HandoffTest(unittest.TestCase):
    """The events contract hand-off: product_candidates rewritten on every candidate write, a proposed test on a go."""

    def test_handoff_and_proposed_test(self):
        tmp = ROOT / 'tests' / '_pipeline_handoff.json'
        ho = ROOT / 'tests' / '_handoff.json'
        te = ROOT / 'tests' / '_tests.json'
        saved = (audit.PIPELINE_PATH, api.HANDOFF_PATH, api.TESTS_PATH)
        try:
            audit.PIPELINE_PATH, api.HANDOFF_PATH, api.TESTS_PATH = tmp, ho, te
            tmp.write_text(json.dumps({'rows': []}), encoding='utf-8')
            code, out = api.candidate_add('sample', {'name': 'Carbon steel pan', 'category': 'pans', 'planned_price': 90, 'who': 'person'}, date(2026, 9, 27))
            self.assertEqual(code, 201)
            cid = out['candidate']['candidate_id']
            doc = json.loads(ho.read_text(encoding='utf-8'))
            self.assertEqual((doc['table'], doc['brand'], len(doc['rows'])), ('product_candidates', 'sample', 1))
            self.assertEqual(doc['rows'][0]['decision'], 'open')
            self.assertIsNone(doc['rows'][0]['gross_margin_pct_from_estimates'])
            api.candidate_update('sample', cid, {'cogs_estimate': 27, 'angle_text': 'A pan that seasons in one use', 'who': 'person'}, date(2026, 9, 27))
            self.assertEqual(json.loads(ho.read_text(encoding='utf-8'))['rows'][0]['gross_margin_pct_from_estimates'], 70.0)
            self.assertFalse(te.is_file())
            r = api.candidate_update('sample', cid, {'stage': 'go', 'who': 'person'}, date(2026, 9, 27))
            self.assertEqual(r['proposed_test']['status'], 'proposed')
            self.assertEqual(r['proposed_test']['hypothesis'], 'A pan that seasons in one use')
            self.assertEqual(r['proposed_test']['read_point'], '2026-10-11')
            self.assertEqual(r['proposed_test']['metric']['name'], 'contribution_margin')
            self.assertEqual(json.loads(ho.read_text(encoding='utf-8'))['rows'][0]['decision'], 'go')
            self.assertEqual(len(api.proposed_tests('sample')), 1)
            api.candidate_update('sample', cid, {'stage': 'go', 'who': 'person'}, date(2026, 9, 28))   # a second go refreshes, never duplicates
            self.assertEqual(len(api.proposed_tests('sample')), 1)
            self.assertEqual(api.handle(Req(['product_candidates'], brand='sample'))['rows'][0]['candidate_id'], cid)
            self.assertEqual(api.handle(Req(['tests'], brand='sample'))['rows'][0]['id'], f'EXP-P-{cid}')
        finally:
            audit.PIPELINE_PATH, api.HANDOFF_PATH, api.TESTS_PATH = saved
            for p in (tmp, ho, te):
                p.unlink(missing_ok=True)


class HandoffCreativeTest(unittest.TestCase):
    def test_theme_handoff_reads_reviews_never_reddit(self):
        h = api.handle(Req(['handoff', f'{audit.SCREEN}.PROD-R07.durability']))
        self.assertEqual(h['theme'], 'durability')
        t = h['text']
        for head in ('CREATIVE HAND-OFF', 'THE ANGLE', 'THE BUYER', 'THE DOUBT', 'THE PROOF ON FILE', 'WHAT BUYERS SAY', 'THE WORDS TO USE', 'DO NOT', 'HAND-OFF'):
            self.assertIn(head, t)
        self.assertIn('Rung 1:', t)
        self.assertIn('Happiness Guarantee', t)
        br = audit.brain('bombas')
        reddit = {str((r.get('value') or {}).get('phrase') or '')[:60] for r in br.records('language_bank') if (r.get('value') or {}).get('subreddit')}
        quoted = [l for l in t.splitlines() if l.startswith('"')]
        self.assertTrue(quoted)
        for q in quoted:
            self.assertNotIn('reddit', q)
            self.assertFalse(any(rp and rp in q for rp in reddit), q)
        self.assertNotIn('—', t)

    def test_send_to_creative(self):
        import tempfile
        saved = (api.HANDOFFS_DIR, api.HANDOFFS_PATH, audit.SHARED_HANDOFFS_PATH)
        tmp = Path(tempfile.mkdtemp())
        api.HANDOFFS_DIR, api.HANDOFFS_PATH, audit.SHARED_HANDOFFS_PATH = tmp / 'handoffs', tmp / 'creative_handoffs.json', tmp / 'shared' / 'handoffs.json'
        try:
            fid = f'{audit.SCREEN}.PROD-R07.durability'
            code, out = api.handle(Req(['handoff', fid, 'send'], method='POST'))
            self.assertEqual(code, 201)
            row = out['handoff']
            self.assertEqual((row['from'], row['to'], row['finding_id'], row['status']), ('01-market-research', 'creative', fid, 'sent'))
            self.assertTrue((api.HANDOFFS_DIR / 'bombas' / (row['id'][3:] + '.md')).is_file())
            # the same send is one row in the shared log, in the events contract shape, that 09-creative reads by to=creative
            shared = json.loads(audit.SHARED_HANDOFFS_PATH.read_text(encoding='utf-8'))
            self.assertEqual(len(shared), 1)
            sr = shared[0]
            self.assertEqual((sr['from_screen'], sr['to'], sr['kind'], sr['status'], sr['finding_id'], sr['owner']), ('01-market-research', 'creative', 'ad_brief', 'proposed', fid, 'agent_drafts'))
            self.assertEqual(sr['id'], row['shared_id'])
            self.assertTrue(sr['id'].startswith('HO-') and len(sr['id']) == 13)
            self.assertIn('CREATIVE HAND-OFF', sr['draft'])
            for k in ('why', 'win_rule', 'stop_rule', 'check_on', 'capability'):
                self.assertTrue(sr.get(k), k)
            api.handle(Req(['handoff', fid, 'send'], method='POST'))
            sent = api.handoffs_sent('bombas')
            self.assertEqual(len(sent['rows']), 1)      # a second send refreshes the pointer, never duplicates it
            self.assertEqual(len(json.loads(audit.SHARED_HANDOFFS_PATH.read_text(encoding='utf-8'))), 2)   # the shared log is append-only: the resend is a new row
            self.assertEqual(sent['rows'][0]['shared_status'], 'proposed')
            self.assertEqual(sent['shared']['by_status'], {'proposed': 2})
            self.assertIn('never edits', sent['rule'])
            self.assertEqual(api.handoffs_sent('other')['rows'], [])
            self.assertEqual(api.handle(Req(['handoff', 'nope', 'send'], method='POST'))[0], 400)
        finally:
            api.HANDOFFS_DIR, api.HANDOFFS_PATH, audit.SHARED_HANDOFFS_PATH = saved

    def test_go_candidate_handoffs_to_copy_and_landing_pages(self):
        import tempfile
        saved = (api.HANDOFFS_DIR, api.HANDOFFS_PATH, audit.SHARED_HANDOFFS_PATH, audit.PIPELINE_PATH, api.HANDOFF_PATH, api.TESTS_PATH)
        tmp = Path(tempfile.mkdtemp())
        api.HANDOFFS_DIR, api.HANDOFFS_PATH, audit.SHARED_HANDOFFS_PATH = tmp / 'handoffs', tmp / 'creative_handoffs.json', tmp / 'shared' / 'handoffs.json'
        audit.PIPELINE_PATH, api.HANDOFF_PATH, api.TESTS_PATH = tmp / 'pipeline.json', tmp / 'product_candidates.json', tmp / 'proposed_tests.json'
        try:
            rows = [{'candidate_id': 'g1', 'brand': 'bombas', 'name': 'Merino calf sock with a wear-life promise', 'category': 'socks', 'stage': 'go', 'planned_price': 24.0, 'pack_units': 1, 'angle_text': 'a wear-life promise on merino', 'angle_source': 'review gap on Amazon', 'owner': 'Sam', 'offer_structure': '3-pack at 60'},
                    {'candidate_id': 'r1', 'brand': 'bombas', 'name': 'Early idea', 'category': 'socks', 'stage': 'researched'}]
            audit.PIPELINE_PATH.write_text(json.dumps({'rows': rows}), encoding='utf-8')
            code, out = api.handle(Req(['candidates', 'g1', 'handoff', 'copy'], method='POST'))
            self.assertEqual(code, 201)
            self.assertEqual((out['shared']['to'], out['shared']['kind'], out['shared']['status'], out['shared']['from_screen'], out['shared']['owner']), ('copy', 'copy', 'proposed', '01-market-research', 'agent_drafts'))
            t = out['shared']['draft']
            for head in ('LISTING COPY HAND-OFF', 'WHAT TO BUILD', 'THE ANGLE', 'THE PRICE AND THE OFFER', 'FROM THE CANDIDATE BRIEF', 'DO NOT', 'HAND-OFF TERMS'):
                self.assertIn(head, t)
            self.assertIn('a wear-life promise on merino (source: review gap on Amazon)', t)
            self.assertIn('3-pack at 60', t)
            self.assertNotIn('—', t)
            self.assertTrue((api.HANDOFFS_DIR / 'bombas' / 'g1-copy.md').is_file())
            code, out2 = api.handle(Req(['candidates', 'g1', 'handoff', 'landing pages'], method='POST'))
            self.assertEqual((code, out2['shared']['kind'], out2['shared']['to']), (201, 'page_section', 'landing pages'))
            self.assertIn('THE LAUNCH PAGE SECTION HAND-OFF', out2['shared']['draft'])
            self.assertEqual(api.handle(Req(['candidates', 'g1', 'handoff', 'finance'], method='POST'))[0], 400)
            self.assertEqual(api.handle(Req(['candidates', 'r1', 'handoff', 'copy'], method='POST'))[0], 400)   # before shortlisted
            self.assertEqual(api.handle(Req(['candidates', 'nope', 'handoff', 'copy'], method='POST'))[0], 400)
            sent = api.handoffs_sent('bombas')
            self.assertEqual(sorted(r['to'] for r in sent['rows']), ['copy', 'landing pages'])
            self.assertEqual(sent['shared']['by_status'], {'proposed': 2})
            api.handle(Req(['candidates', 'g1', 'handoff', 'copy'], method='POST'))
            self.assertEqual(len(api.handoffs_sent('bombas')['rows']), 2)     # a resend refreshes the pointer
            self.assertEqual(len(json.loads(audit.SHARED_HANDOFFS_PATH.read_text(encoding='utf-8'))), 3)   # and appends to the shared log
        finally:
            api.HANDOFFS_DIR, api.HANDOFFS_PATH, audit.SHARED_HANDOFFS_PATH, audit.PIPELINE_PATH, api.HANDOFF_PATH, api.TESTS_PATH = saved

    def test_team_statuses_feed_the_checklist(self):
        import tempfile
        saved = (audit.SHARED_HANDOFFS_PATH, audit.PIPELINE_PATH)
        tmp = Path(tempfile.mkdtemp())
        audit.SHARED_HANDOFFS_PATH, audit.PIPELINE_PATH = tmp / 'handoffs.json', tmp / 'pipeline.json'
        try:
            audit.PIPELINE_PATH.write_text(json.dumps({'rows': [{'candidate_id': 'g1', 'brand': 'fake', 'name': 'G', 'stage': 'go'}]}), encoding='utf-8')
            fid = f'{audit.SCREEN}.candidate.g1'
            self.assertEqual(audit.team_status('g1', 'copy')['status'], 'none')       # no log yet
            audit.SHARED_HANDOFFS_PATH.write_text(json.dumps([
                {'id': 'HO-1', 'from_screen': audit.SCREEN, 'to': 'copy', 'finding_id': fid, 'status': 'proposed', 'time': '2026-09-20T10:00:00Z'},
                {'id': 'HO-2', 'from_screen': audit.SCREEN, 'to': 'copy', 'finding_id': fid, 'status': 'done', 'time': '2026-09-22T10:00:00Z'},
                {'id': 'HO-3', 'from_screen': audit.SCREEN, 'to': 'landing pages', 'finding_id': fid, 'status': 'proposed', 'time': '2026-09-21T10:00:00Z'},
                {'id': 'HO-4', 'from_screen': '09-creative', 'to': 'landing pages', 'finding_id': fid, 'status': 'done', 'time': '2026-09-23T10:00:00Z'}]), encoding='utf-8')
            self.assertEqual((audit.team_status('g1', 'copy')['status'], audit.team_status('g1', 'copy')['id']), ('done', 'HO-2'))    # the latest row wins
            self.assertEqual(audit.team_status('g1', 'landing pages')['status'], 'proposed')                                          # another screen's row never counts
            data = api.sample_data()
            D = audit.last_full_day(data, None)
            row = audit.launch_readiness('fake', data, None, audit.Reader(data, None, D), D)['rows'][0]
            items = {i['key']: i for i in row['checklist']}
            self.assertEqual((items['copy']['status'], items['copy']['why']), ('pass', 'done by copy on 2026-09-22'))
            self.assertEqual((items['page']['status'], items['page']['why']), ('open', 'sent to landing pages, waiting'))
            self.assertFalse(items['copy']['hard'])
            self.assertFalse(row['launch_ready'])
            self.assertEqual(row['teams']['page']['status'], 'proposed')
        finally:
            audit.SHARED_HANDOFFS_PATH, audit.PIPELINE_PATH = saved

    def test_launch_plan_dates_work_back_from_the_target(self):
        import tempfile
        saved = (audit.SHARED_HANDOFFS_PATH, audit.PIPELINE_PATH, api.HANDOFF_PATH, api.TESTS_PATH)
        tmp = Path(tempfile.mkdtemp())
        audit.SHARED_HANDOFFS_PATH, audit.PIPELINE_PATH, api.HANDOFF_PATH, api.TESTS_PATH = tmp / 'handoffs.json', tmp / 'pipeline.json', tmp / 'pc.json', tmp / 'pt.json'
        try:
            data = api.sample_data()
            D = audit.last_full_day(data, None)
            target = D + timedelta(days=90)
            audit.PIPELINE_PATH.write_text(json.dumps({'rows': [       # rows for the sample brand, read with brand None
                {'candidate_id': 'g1', 'brand': 'sample', 'name': 'G', 'category': 'socks', 'stage': 'go', 'launch_target': target.isoformat(), 'lead_time_days': 40, 'cogs_source': 'quote', 'sample': {'result': 'pass'}, 'review_date': (target + timedelta(days=10)).isoformat()},
                {'candidate_id': 'g2', 'brand': 'sample', 'name': 'H', 'category': 'socks', 'stage': 'shortlisted'},
                {'candidate_id': 'r1', 'brand': 'sample', 'name': 'R', 'category': 'socks', 'stage': 'researched'}]}), encoding='utf-8')
            lp = api.launch_plan(data, None, 'g1')
            by = {x['key']: x for x in lp['steps']}
            self.assertEqual(lp['target'], target.isoformat())
            self.assertEqual(by['order']['due'], (target - timedelta(days=40 + audit.ORDER_SAFETY_DAYS)).isoformat())
            self.assertEqual(by['quote']['due'], (target - timedelta(days=40 + audit.ORDER_SAFETY_DAYS + api.LAUNCH_QUOTE_DAYS)).isoformat())
            self.assertEqual(by['copy']['due'], (target - timedelta(days=14)).isoformat())
            self.assertEqual(by['page']['due'], (target - timedelta(days=10)).isoformat())
            self.assertEqual(by['stock']['due'], (target - timedelta(days=audit.ORDER_SAFETY_DAYS)).isoformat())
            self.assertEqual(by['read']['due'], (target + timedelta(days=28)).isoformat())      # 28 days after launch beats the earlier review date
            self.assertEqual((by['quote']['state'], by['sample']['state'], by['order']['state'], by['copy']['state']), ('done', 'done', 'due', 'due'))
            self.assertEqual(lp['overdue'], 0)
            self.assertIn('LAUNCH PLAN: G', lp['text'])
            lp2 = api.launch_plan(data, None, 'g2')                     # no target, no lead time: the dates are honest blanks
            self.assertIsNone(lp2['target'])
            self.assertEqual({x['state'] for x in lp2['steps'] if x['key'] != 'target'}, {'no_date'})
            self.assertEqual(next(x for x in lp2['steps'] if x['key'] == 'target')['state'], 'due')
            self.assertEqual([c['candidate_id'] for c in api.launch_candidates(None)], ['g1', 'g2'])
            with self.assertRaises(ValueError):
                api.launch_plan(data, None, 'nope')
            # the launch steps ride the calendar
            cal = api.calendar_items(data, None, horizon_days=120)
            launch = [i for i in cal['items'] if i['kind'] == 'launch']
            self.assertTrue(any(i['title'].startswith('First order placed: G') for i in launch))
            self.assertFalse(any('Supplier quote' in i['title'] for i in launch))     # done steps stay off the calendar
            out = api.handle(Req(['candidates', 'g1', 'launch'], brand='sample'))
            self.assertEqual(out['candidate_id'], 'g1')
            self.assertEqual(api.handle(Req(['candidates', 'nope', 'launch'], brand='sample'))[0], 404)
            r = api.candidate_update('sample', 'g1', {'ordered_on': 'soon', 'who': 'person'}, D)
            self.assertEqual(r[0], 400)
            r = api.candidate_update('sample', 'g1', {'ordered_on': D.isoformat(), 'who': 'person'}, D)
            self.assertEqual(r['changes'], ['ordered on set'])
            self.assertEqual({x['key']: x['state'] for x in api.launch_plan(data, None, 'g1')['steps']}['order'], 'done')
        finally:
            audit.SHARED_HANDOFFS_PATH, audit.PIPELINE_PATH, api.HANDOFF_PATH, api.TESTS_PATH = saved

    def test_launch_steps_and_handoffs_in_week_plan_and_report(self):
        import tempfile
        saved = (audit.SHARED_HANDOFFS_PATH, audit.PIPELINE_PATH, api.HANDOFF_PATH, api.TESTS_PATH, api.HANDOFFS_DIR, api.HANDOFFS_PATH)
        tmp = Path(tempfile.mkdtemp())
        audit.SHARED_HANDOFFS_PATH, audit.PIPELINE_PATH, api.HANDOFF_PATH, api.TESTS_PATH, api.HANDOFFS_DIR, api.HANDOFFS_PATH = tmp / 'handoffs.json', tmp / 'pipeline.json', tmp / 'pc.json', tmp / 'pt.json', tmp / 'ho', tmp / 'ch.json'
        try:
            data = api.sample_data()
            D = audit.last_full_day(data, None)
            audit.PIPELINE_PATH.write_text(json.dumps({'rows': [{'candidate_id': 'g1', 'brand': 'sample', 'name': 'G', 'category': 'socks', 'stage': 'go', 'launch_target': (D + timedelta(days=12)).isoformat(), 'lead_time_days': 5, 'angle_text': 'a', 'angle_source': 'review gap', 'planned_price': 20}]}), encoding='utf-8')
            api.handle(Req(['candidates', 'g1', 'handoff', 'copy'], brand='sample', method='POST'))
            wp = api.week_plan(data, None)
            self.assertIn('LAUNCH STEPS THIS WEEK', wp['text'])
            self.assertTrue(any(i['kind'] == 'launch' for i in wp['launch']))
            self.assertIn('HAND-OFFS OUT', wp['text'])
            self.assertIn('to copy, proposed', wp['text'])
            self.assertIn('1 waiting on a team', wp['text'])
            rp = api.desk_report(data, None)
            self.assertIn('## Launch plans', rp['text'])
            self.assertIn('- G (go): target ' + (D + timedelta(days=12)).isoformat(), rp['text'])
            self.assertIn('## Hand-offs sent (1 proposed)', rp['text'])
            for head in ('Launch readiness', 'Price band', 'Margin points', 'Cost floors', 'Identical sellers', 'Opportunity', 'Sourcing', 'Re-quote', 'Floors'):
                self.assertIn(head, rp['text'])
        finally:
            audit.SHARED_HANDOFFS_PATH, audit.PIPELINE_PATH, api.HANDOFF_PATH, api.TESTS_PATH, api.HANDOFFS_DIR, api.HANDOFFS_PATH = saved

    def test_candidate_report_has_every_section(self):
        rp = api.handle(Req(['candidates', 'cand-003', 'report']))
        self.assertEqual(rp['sections'], ['brief', 'checklist', 'launch_plan', 'handoffs'])
        for head in ('# Holiday gift box', '## The brief', '## The launch checklist', '## The launch plan', '## Hand-offs sent'):
            self.assertIn(head, rp['text'])
        self.assertIn('Not at the checklist yet', rp['text'])          # gated, no first run: honest
        self.assertNotIn('—', rp['text'])
        self.assertEqual(api.handle(Req(['candidates', 'nope', 'report']))[0], 404)

    def test_avatar_handoff_names_the_buyer(self):
        fid = next(f['id'] for f in audit.run('bombas', {'ends_on': '2026-09-27'}) if f['rule_id'] == 'PROD-R11')
        h = api.creative_handoff('bombas', fid)
        self.assertTrue(h['avatars'])
        self.assertIn('Triggers:', h['text'])

    def test_handoff_refuses_a_candidate_rule(self):
        fid = next(f['id'] for f in audit.run('bombas', {'ends_on': '2026-09-27'}) if f['rule_id'] == 'PROD-R14')
        self.assertEqual(api.handle(Req(['handoff', fid]))[0], 400)
        self.assertEqual(api.handle(Req(['handoff', 'nope']))[0], 400)


class ReportTest(unittest.TestCase):
    def test_report_covers_every_block(self):
        rp = api.handle(Req(['report']))
        t = rp['text']
        for head in ('# Research desk', '## The plan, top 10', '## Connect first', '## Due:', '## The desk, block by block'):
            self.assertIn(head, t)
        top = api.rank('bombas', None)['actions'][0]['title']
        self.assertIn(top, t)
        self.assertGreaterEqual(rp['blocks'], 20)
        self.assertIn('**Marketplace**: the brand is not the seller of record', t)
        self.assertNotIn('—', t)
        s = api.handle(Req(['report'], brand='sample'))
        self.assertIn('Tallgrass Goods', s['text'])
        self.assertIn('no web pass on file', s['text'])


class BriefTest(unittest.TestCase):
    def test_candidate_brief_reads_every_block(self):
        b = api.handle(Req(['candidates', 'cand-003', 'brief']))
        self.assertEqual(b['candidate_id'], 'cand-003')
        t = b['text']
        for head in ('CANDIDATE BRIEF', 'THE ANGLE', 'THE DEMAND CASE', 'THE MONEY', 'THE GATES', 'THE SCORECARD', 'THE SPEC AND THE CLOCK', 'OPEN ACTIONS', 'LOG'):
            self.assertIn(head, t)
        self.assertIn('Holiday gift box', t)
        self.assertIn('Demand pattern: seasonal', t)
        self.assertIn('Planned price $68.00 for 4 unit(s)', t)
        self.assertIn('of 100, verdict', t)
        self.assertNotIn('—', t)
        self.assertEqual(api.handle(Req(['candidates', 'nope', 'brief']))[0], 400)

    def test_brief_is_read_only(self):
        self.assertEqual(api.handle(Req(['candidates', 'cand-003', 'brief'], method='POST'))[0], 405)


class WebPassTest(unittest.TestCase):
    """web_pass.py: a template a research session fills, a checker that refuses a number without a source, and the desk
    reading the brand's own file first."""

    @classmethod
    def setUpClass(cls):
        import importlib.util as iu
        spec = iu.spec_from_file_location('web_pass_t', SCREEN / 'web_pass.py')
        cls.wp = iu.module_from_spec(spec)
        spec.loader.exec_module(cls.wp)

    def test_template_fails_until_filled(self):
        t = self.wp.template('fakebrand', 'kitchen goods', date(2026, 9, 27))
        errs = self.wp.check(t, 'fakebrand')
        self.assertTrue(any('url missing' in e for e in errs))
        self.assertTrue(any('key must be' in e for e in errs))
        t['lanes'] = [{'key': 'pans', 'label': 'Pans', 'kind': 'product', 'terms': ['pan', 'skillet']}]
        t['markets'] = [{'key': 'cookware_us', 'label': 'US cookware', 'size_usd': 5e9, 'size_year': 2025, 'cagr_pct': 3.1, 'cagr_window': '2026 to 2033', 'series': [], 'direction': 'up', 'drivers': [],
                         'sources': [{'url': 'https://example.org/report', 'publisher': 'Example', 'date': '2026', 'what': 'size and growth'}]}]
        t['preferences'] = []
        t['launches'] = [{'brand': 'Rival', 'what': 'a carbon steel pan', 'sub_category': 'pans', 'date': '2026-03', 'price_usd': 90, 'channel': 'dtc',
                          'sources': [{'url': 'https://example.org/press', 'publisher': 'Press', 'date': '2026-03-02', 'what': 'launch'}]}]
        self.assertEqual(self.wp.check(t, 'fakebrand'), [])
        self.assertEqual(self.wp.check(t, 'otherbrand'), ["brand is 'fakebrand', expected 'otherbrand'"])
        t['markets'][0]['sources'] = []
        self.assertIn('market 1 (cookware_us): no source; every number needs a url and a date', self.wp.check(t, 'fakebrand'))

    def test_legacy_fixture_checks(self):
        doc, p = self.wp.load('bombas')
        self.assertEqual(p.name, 'market_trends.json')
        self.assertEqual(self.wp.check(doc, 'bombas'), [])
        self.assertEqual(self.wp.load('nobody'), (None, None))

    def test_desk_reads_the_brands_own_file_first(self):
        p = self.wp.path_for('bombas')
        self.assertFalse(p.is_file())
        p.parent.mkdir(parents=True, exist_ok=True)
        try:
            p.write_text(json.dumps({'brand': 'bombas', 'captured_at': '2026-09-27', 'lanes': [{'key': 'pans', 'label': 'Pans', 'terms': ['pan'], 'kind': 'product'}], 'markets': [], 'preferences': [], 'launches': []}), encoding='utf-8')
            self.assertEqual(audit.lanes_for('bombas'), [('pans', 'Pans', ['pan'])])
            self.assertEqual(audit.web_pass('bombas')['captured_at'], '2026-09-27')
        finally:
            p.unlink()
        self.assertEqual(len(audit.lanes_for('bombas')), 10)   # back to the legacy fixture

    def test_history_and_diff(self):
        import tempfile
        prev = {'brand': 'h', 'captured_at': '2026-09-01', 'lanes': [{'key': 'a'}], 'markets': [{'key': 'm1', 'label': 'M1', 'cagr_pct': 4.0, 'size_usd': 100}], 'preferences': [{'key': 'p1', 'direction': 'up'}],
                'launches': [{'brand': 'R', 'what': 'old thing', 'date': '2026-05'}]}
        cur = {'brand': 'h', 'captured_at': '2026-09-28', 'lanes': [{'key': 'a'}, {'key': 'b'}], 'markets': [{'key': 'm1', 'label': 'M1', 'cagr_pct': 5.5, 'size_usd': 100}, {'key': 'm2', 'label': 'M2', 'cagr_pct': 1}],
               'preferences': [{'key': 'p1', 'direction': 'down'}, {'key': 'p2', 'direction': 'up'}], 'launches': [{'brand': 'R', 'what': 'old thing', 'date': '2026-05'}, {'brand': 'S', 'what': 'new thing', 'date': '2026-09'}]}
        d = self.wp.diff(prev, cur)
        self.assertEqual(([l['what'] for l in d['launches_new']], d['launches_gone'], [m['key'] for m in d['markets_moved']], [m['key'] for m in d['markets_new']], [p['key'] for p in d['preferences_new']], d['preferences_turned'], [l['key'] for l in d['lanes_new']]),
                         (['new thing'], [], ['m1'], ['m2'], ['p2'], [{'key': 'p1', 'from': 'up', 'to': 'down'}], ['b']))
        saved = self.wp.HISTORY_DIR
        self.wp.HISTORY_DIR = Path(tempfile.mkdtemp())
        try:
            self.assertFalse(self.wp.changes_since_last('h', cur)['available'])       # nothing kept yet
            self.assertIsNotNone(self.wp.snapshot('h', prev))
            self.assertIsNone(self.wp.snapshot('h', prev))                          # the same capture is not copied twice
            ch = self.wp.changes_since_last('h', cur)
            self.assertTrue(ch['available'])
            self.assertEqual((ch['previous'], ch['current'], ch['quiet'], len(ch['launches_new'])), ('2026-09-01', '2026-09-28', False, 1))
            self.wp.snapshot('h', cur)
            self.assertEqual(self.wp.changes_since_last('h', cur)['previous'], '2026-09-01')   # the current capture is never its own baseline
        finally:
            self.wp.HISTORY_DIR = saved
        b = audit.web_pass_changes('bombas')
        self.assertIn('available', b)

    def test_connect_action_names_the_command(self):
        r = api.rank('sample', {'ends_on': '2026-09-24', 'days': 28, 'trailing': 4})
        a = next(x for x in r['actions'] if (x.get('title') or '').startswith('Run the web pass'))
        self.assertIn('web_pass.py --brand sample --init', a['steps'][0]['text'])
        self.assertIn('--check', a['steps'][2]['text'])


class OpportunityTest(unittest.TestCase):
    def test_lane_opportunity_scores_on_stated_weights(self):
        br = audit.brain('bombas')
        data = audit.brand_data('bombas')
        D = audit.last_full_day(data, 'bombas')
        op = audit.lane_opportunity(br, api.products(data, 'bombas'), D)
        rows = op['rows']
        self.assertTrue(rows)
        self.assertEqual(sum(op['weights'].values()), 100)
        self.assertEqual([r['rank'] for r in rows], list(range(1, len(rows) + 1)))
        scores = [r['score'] for r in rows if r['score'] is not None]
        self.assertEqual(scores, sorted(scores, reverse=True))
        for r in rows:
            read = {k: v for k, v in r['parts'].items() if v is not None}
            self.assertEqual(r['parts_read'], len(read))
            if read:
                w = sum(op['weights'][k] for k in read)
                self.assertEqual(r['score'], round(sum(op['weights'][k] * v for k, v in read.items()) / w * 100))   # the score is the arithmetic of its parts
                self.assertTrue(all(0 <= v <= 1 for v in read.values()))
            self.assertIn(r['verdict'], ('strong_no_candidate', 'strong', 'weak', 'thin'))
            if r['parts_read'] < op['min_parts']:
                self.assertEqual(r['verdict'], 'thin')
        self.assertEqual(audit.lane_opportunity(None, [], D)['rows'], [])
        # the score rides on every lane card
        r = api.rank('bombas', None)
        lane_cards = [a for a in r['actions'] if a.get('rule_id') in api.LANE_RULES and a.get('opportunity')]
        self.assertTrue(lane_cards)
        o = lane_cards[0]['opportunity']
        self.assertEqual(set(o), {'score', 'rank', 'of', 'parts', 'parts_read', 'verdict', 'open_candidates'})
        self.assertTrue(all(a.get('opportunity') is None for a in r['actions'] if a.get('rule_id') in api.CANDIDATE_RULES))


class FloorsTest(unittest.TestCase):
    class Stub:
        brand = 'fake'
        def __init__(self, value): self.value = value
        def records(self, section): return []
        def get(self, rid): return {'id': rid, 'value': self.value} if rid == 'fake.learnings.research_floors' and self.value is not None else None

    def test_floors_default_brand_and_invalid(self):
        d = audit.floors_for(None)
        self.assertEqual((d['price_reject_max']['value'], d['price_reject_max']['source'], d['kill_hold_days']['value']), (9.99, 'default', 90))
        self.assertEqual(audit.floors_for('sample')['identical_sellers']['source'], 'default')
        fl = audit.floors_for(self.Stub({'price_reject_max': 14.99, 'identical_sellers': 6, 'first_run_cash_share': 1.5, 'kill_hold_days': -3, 'opp_weight_demand': 50, 'price_caution_low': 30, 'price_caution_high': 20}))
        self.assertEqual((fl['price_reject_max']['value'], fl['price_reject_max']['source']), (14.99, 'brand'))
        self.assertEqual((fl['identical_sellers']['value'], fl['identical_sellers']['source']), (6, 'brand'))
        self.assertEqual((fl['first_run_cash_share']['value'], fl['first_run_cash_share']['source']), (0.25, 'invalid, default used'))   # a share above 1
        self.assertEqual((fl['kill_hold_days']['value'], fl['kill_hold_days']['source']), (90, 'invalid, default used'))              # negative
        self.assertEqual(fl['price_caution_high']['source'], 'invalid, default used')                                                  # low above high
        self.assertEqual(fl['opp_weight_demand']['value'], 50)
        read = audit.floors_read(self.Stub({'identical_sellers': 6}))
        self.assertEqual((read['brand_set'], read['record']), (1, 'fake.learnings.research_floors'))
        self.assertEqual(len(read['rows']), len(audit.FLOOR_DEFAULTS))

    def test_floors_reach_the_rules(self):
        D = date(2026, 9, 27)
        stub = self.Stub({'price_reject_max': 14.99, 'identical_sellers': 3, 'opportunity_strong': 90, 'opp_weight_demand': 100, 'opp_weight_competition': 0, 'opp_weight_price_room': 0, 'opp_weight_complaint_room': 0, 'opp_weight_presence': 0})
        saved = (audit.brain, audit.PIPELINE_PATH, audit.listing_pull)
        import tempfile
        tmp = Path(tempfile.mkdtemp()) / 'pipeline.json'
        try:
            audit.brain = lambda b, today=None: stub if b == 'fake' else None
            audit.PIPELINE_PATH = tmp
            tmp.write_text(json.dumps({'rows': [{'candidate_id': 'a', 'brand': 'fake', 'name': 'Merino calf sock', 'stage': 'researched', 'planned_price': 12.0}]}), encoding='utf-8')
            pb = audit.price_band_read('fake')
            self.assertEqual((pb['reject_max'], pb['floors_source']['price_reject_max'], pb['rows'][0]['verdict']), (14.99, 'brand', 'reject'))   # $12 is under the brand's own line
            self.assertIn('$14.99', audit.price_band_findings('fake', D)[0]['sentence'])
            audit.listing_pull = lambda: {'brand': 'fake', 'mode': 'live', 'rows': [{'asin': 'B1', 'title': 'Merino Calf Sock', 'seller': 'S', 'offers_count': 4}]}
            idn = audit.identical_sellers_read('fake', stub)
            self.assertEqual((idn['floor'], idn['floor_source'], idn['rows'][0]['verdict']), (3, 'brand', 'cash_test'))                 # 4 sellers trips a floor of 3
            op = audit.lane_opportunity(audit.brain('bombas') if False else stub, [], D)
            self.assertEqual((op['weights']['demand'], op['strong']), (100, 90))
        finally:
            audit.brain, audit.PIPELINE_PATH, audit.listing_pull = saved

    def test_proposed_floors_come_from_measured_numbers(self):
        br = audit.brain('bombas')
        data = audit.brand_data('bombas')
        D = audit.last_full_day(data, 'bombas')
        rd = audit.Reader(data, 'bombas', D)
        prods = api.products(data, 'bombas')
        pr = audit.propose_floors(br, prods, rd)
        by = {r['key']: r for r in pr['rows']}
        self.assertEqual(set(by), {'price_target_low'})                        # Bombas has orders but no products table: only the order-value floor is proposed
        self.assertEqual(by['price_target_low']['proposed'], round(audit.aov_28d(rd), 2))
        self.assertTrue(by['price_target_low']['differs'])
        self.assertTrue(all(r['simulated'] for r in pr['rows']))
        sd = api.sample_data()
        prods = api.products(sd, None)
        per_unit = sorted(round(p['price'] / (p.get('items_per_unit') or 1), 2) for p in prods if p.get('price'))
        pr2 = audit.propose_floors(None, prods, audit.Reader(sd, None, audit.last_full_day(sd, None)))
        by2 = {r['key']: r for r in pr2['rows']}
        self.assertEqual(by2['price_reject_max']['proposed'], per_unit[0])     # the sample brand has a catalogue: the cheapest and the median unit price
        self.assertEqual(by2['price_caution_high']['proposed'], round(statistics.median(per_unit), 2))
        self.assertEqual(by2['price_reject_max']['in_force'], 9.99)
        self.assertEqual(audit.propose_floors(None, [], None)['rows'], [])

    def test_set_floors_writes_a_founder_record(self):
        import tempfile, sys
        if str(audit.APP / 'brain') not in sys.path:
            sys.path.insert(0, str(audit.APP / 'brain'))
        import store, shutil
        root = Path(tempfile.mkdtemp())
        shutil.copytree(audit.APP / 'brain' / 'bombas', root / 'bombas')
        br = store.Brain('bombas', root=root, today=date(2026, 9, 28))
        code, out = api.set_floors('bombas', {'price_reject_max': '14.99', 'identical_sellers': 6, 'who': 'kevin'}, date(2026, 9, 28), brain=br)
        self.assertEqual(code, 201, out)
        self.assertEqual(out['set'], {'price_reject_max': 14.99, 'identical_sellers': 6.0})
        rec = br.get('bombas.learnings.research_floors')
        self.assertEqual((rec['tier'], rec['status'], rec['source']['type'], rec['value']['identical_sellers']), ('approved', 'active', 'founder', 6.0))
        self.assertEqual(audit.floors_for(br)['price_reject_max']['source'], 'brand')
        code, out = api.set_floors('bombas', {'kill_hold_days': 120}, date(2026, 9, 29), brain=br)     # a second set merges into the record
        self.assertEqual(code, 201)
        self.assertEqual(set(br.get('bombas.learnings.research_floors')['value']), {'price_reject_max', 'identical_sellers', 'kill_hold_days'})
        self.assertEqual(api.set_floors('bombas', {'moon': 1}, date(2026, 9, 28), brain=br)[0], 400)
        self.assertEqual(api.set_floors('bombas', {'kill_hold_days': 'soon'}, date(2026, 9, 28), brain=br)[0], 400)
        self.assertEqual(api.set_floors(None, {'kill_hold_days': 1}, date(2026, 9, 28))[0], 400)


class LaneOnCandidateTest(unittest.TestCase):
    def test_screen_in_keeps_the_lane(self):
        import tempfile
        saved = (audit.PIPELINE_PATH, api.HANDOFF_PATH, api.TESTS_PATH)
        tmp = Path(tempfile.mkdtemp())
        audit.PIPELINE_PATH, api.HANDOFF_PATH, api.TESTS_PATH = tmp / 'pipeline.json', tmp / 'pc.json', tmp / 'pt.json'
        try:
            D = date(2026, 9, 27)
            keys = [k for k, _, _ in audit.lanes_for('bombas')]
            self.assertIn('underwear', keys)
            self.assertEqual(api.candidate_add('bombas', {'name': 'Boxer brief', 'lane': 'moon'}, D)[0], 400)
            code, out = api.candidate_add('bombas', {'name': 'Everyday brief', 'lane': 'underwear', 'who': 'person'}, D)
            self.assertEqual((code, out['candidate']['lane']), (201, 'underwear'))
            cid = out['candidate']['candidate_id']
            br = audit.brain('bombas')
            data = audit.brand_data('bombas')
            E = audit.last_full_day(data, 'bombas')
            op = {r['key']: r for r in audit.lane_opportunity(br, api.products(data, 'bombas'), E)['rows']}
            self.assertIn('Everyday brief', op['underwear']['open_candidates'])            # the lane on the candidate wins, no word match needed
            self.assertEqual(op['underwear']['verdict'], 'strong')
            self.assertEqual(api.candidate_update('bombas', cid, {'lane': 'moon', 'who': 'person'}, D)[0], 400)
            r = api.candidate_update('bombas', cid, {'lane': 'gifting', 'who': 'person'}, D)
            self.assertEqual(r['changes'], ['lane gifting'])
            self.assertEqual({x['candidate_id']: x['lane'] for x in api.handoff_rows('bombas')}[cid], 'gifting')
            self.assertIn('lane', audit.LOG_COLUMNS)
            self.assertEqual({x['candidate_id']: x['lane'] for x in audit.research_log('bombas')['rows']}[cid], 'gifting')
            rk = api.rank('bombas', None)
            op2 = {r['key']: r for r in audit.lane_opportunity(br, api.products(data, 'bombas'), E)['rows']}
            cards = [a for a in rk['actions'] if a.get('opportunity')]
            self.assertTrue(cards)
            for a in cards:                                                                   # every lane card lists the same open candidates as the read
                self.assertEqual(a['opportunity']['open_candidates'], op2[(a.get('entity') or {}).get('id')]['open_candidates'])
            self.assertIn('Everyday brief', op2['gifting']['open_candidates'])
        finally:
            audit.PIPELINE_PATH, api.HANDOFF_PATH, api.TESTS_PATH = saved


class SecondBrandTest(unittest.TestCase):
    """The desk is not Bombas-shaped: the sample brand (Tallgrass Goods, kitchen goods, no brain, no web pass) reads
    nothing of Bombas and every route still answers."""

    def test_fixtures_are_brand_bound(self):
        self.assertEqual(audit.market_trends().get('brand'), 'bombas')
        self.assertIsNone(audit.web_pass(None))
        self.assertIsNone(audit.web_pass('tallgrass'))
        self.assertEqual(len(audit.lanes_for('bombas')), 10)
        self.assertEqual(audit.lanes_for(None), [])
        self.assertIsNone(audit.social_pull_for(None))
        self.assertEqual(audit.social_pull_for('bombas')['brand'], 'bombas')

    def test_mix_from_orders(self):
        class D:
            brand = {'as_of': '2026-09-24'}

            def table(self, name):
                if name == 'orders':
                    return [{'created_at': '2026-08-03T10:00:00Z', 'subtotal': 100.0, 'discount': {'code': 'X', 'amount': 10.0},
                             'line_items': [{'sku': 'A', 'qty': 2, 'line_total': 60.0}, {'sku': 'B', 'qty': 1, 'line_total': 40.0}]},
                            {'created_at': '2026-08-20T10:00:00Z', 'subtotal': 30.0, 'discount': None, 'cancelled_at': '2026-08-21T00:00:00Z',
                             'line_items': [{'sku': 'A', 'qty': 1, 'line_total': 30.0}]},
                            {'created_at': '2026-07-20T10:00:00Z', 'subtotal': 30.0, 'discount': None, 'line_items': [{'sku': 'A', 'qty': 1, 'line_total': 30.0}]}]
                if name == 'products':
                    return [{'sku': 'A', 'type': 'pans'}, {'sku': 'B', 'type': 'boards'}]
                raise KeyError(name)

        rows = audit.orders_monthly(D())
        self.assertEqual(rows, [{'month': '2026-07', 'category': 'pans', 'units': 1, 'net_sales': 30.0},
                                {'month': '2026-08', 'category': 'boards', 'units': 1, 'net_sales': 36.0},
                                {'month': '2026-08', 'category': 'pans', 'units': 2, 'net_sales': 54.0}])   # the discount is shared by line value; the cancelled order is out
        rd = audit.Reader(D(), None, date(2026, 9, 24))
        m = audit.category_mix(D(), None, rd)
        self.assertFalse(m['unavailable'])
        self.assertEqual(m['basis'], 'order line items by product type (no monthly product table)')
        self.assertEqual({r['category']: r['units'] for r in m['rows']}, {'pans': 3, 'boards': 1})
        self.assertIsNone(m['store_growth'])          # a partial prior year never reads as growth
        self.assertIn('0 of the 12 prior months', m['growth_note'])
        sample = api.sample_data()
        ms = audit.category_mix(sample, None, audit.Reader(sample, None, date(2026, 9, 24)))
        self.assertEqual(len(ms['rows']), 5)
        self.assertIsNone(ms['store_growth'])

    def test_return_rates_by_line(self):
        D = date(2026, 9, 24)

        class Data:
            brand = {'as_of': '2026-09-24'}

            def __init__(self, returns=True):
                self.returns = returns

            def table(self, name):
                if name == 'orders':
                    rows = []
                    for i in range(100):
                        rows.append({'created_at': f'2026-{(i % 12) + 1:02d}-10T10:00:00Z', 'subtotal': 50.0, 'discount': None,
                                     'line_items': [{'sku': 'A', 'qty': 1, 'line_total': 30.0, 'title': 'Skillet 4-Pack'}, {'sku': 'B', 'qty': 1, 'line_total': 20.0, 'title': 'Apron'}]})
                    return rows
                if name == 'products':
                    return [{'sku': 'A', 'title': 'Skillet 4-Pack', 'type': 'pans'}, {'sku': 'B', 'title': 'Apron', 'type': 'linen'}]
                if name == 'reversed_orders' and self.returns:
                    rows = [{'type': 'return', 'sku': 'A', 'reason': 'damaged in transit', 'opened_at': '2026-05-01T00:00:00Z'} for _ in range(20)]
                    rows += [{'type': 'return', 'sku': 'A', 'reason': 'changed mind', 'opened_at': '2026-05-01T00:00:00Z'} for _ in range(5)]
                    rows += [{'type': 'return', 'sku': 'B', 'reason': 'changed mind', 'opened_at': '2026-06-01T00:00:00Z'} for _ in range(6)]
                    rows += [{'type': 'chargeback', 'sku': 'B', 'reason': 'fraud', 'opened_at': '2026-06-01T00:00:00Z'}]
                    return rows
                raise KeyError(name)

        rr = audit.return_rates(Data(), None, D)
        self.assertFalse(rr['unavailable'])
        rows = {r['line']: r for r in rr['rows']}
        self.assertEqual((rows['Skillet']['units'], rows['Skillet']['returns'], rows['Skillet']['rate']), (68, 25, 0.3676))   # 12 whole months, Sep 2025 to Aug 2026: 8 of the 12 order months fall inside
        self.assertEqual(rows['Skillet']['top_reason'], 'damaged in transit')
        self.assertEqual(rows['Apron']['verdict'], 'thin')            # 6 returns: too few to judge
        self.assertEqual(rr['median'], 0.3676)                          # only judged lines set the median
        self.assertEqual(rows['Skillet']['verdict'], 'normal')          # alone, a line is its own median
        found = audit.return_findings(Data(), None, D, None)
        self.assertEqual(found, [])
        miss = audit.return_findings(Data(returns=False), None, D, None)
        self.assertEqual([(f['rule_id'], f['status']) for f in miss], [('PROD-R34', 'unavailable')])
        sample = api.sample_data()
        rs = audit.return_rates(sample, None, D)
        self.assertGreater(len(rs['rows']), 10)
        self.assertTrue(all(r['verdict'] in ('high', 'normal', 'thin') for r in rs['rows']))
        for f in audit.return_findings(sample, None, D, None):
            self.check_shape(f)

    def test_sample_brand_routes(self):
        data = api.sample_data()
        o = api.overview(data, None)
        self.assertEqual(o['brand']['brand'], 'Tallgrass Goods')
        d = o['desk']
        self.assertEqual(d['lanes'], [])
        self.assertEqual(d['cadence']['brands'], [])
        self.assertEqual(d['trend_checks']['rows'], [])
        self.assertEqual(d['video']['rows'], [])
        self.assertEqual(d['lane_map']['points'], [])
        self.assertFalse(d['trends']['on_file'])
        self.assertFalse(d['mix']['unavailable'])   # the mix comes from order line items
        self.assertFalse(d['returns']['unavailable'])
        self.assertEqual({c['category'] for c in d['pattern']['categories']}, {'cast iron', 'gift sets', 'wooden boards', 'linen', 'kitchen tools'})
        self.assertEqual(d['surfaces']['rows'], [])
        self.assertIsNone(d['marketplace']['presence'])
        for f in audit.run(None, None, data=data):
            self.assertIn(f['status'], ('unavailable', 'open'), f['id'])
            if f['status'] == 'open':
                self.assertEqual(f['rule_id'], 'PROD-R34')   # only the return rate reads from orders; the rest say unavailable
        r = api.rank('sample', {'ends_on': '2026-09-24', 'days': 28, 'trailing': 4})
        self.assertTrue(r['actions'])
        for a in r['actions']:
            self.assertIn(a['status'], ('unavailable', 'open'))
            self.assertEqual(api.rank_mod.validate_action(a), [], a['id'])
        self.assertEqual(api.rank(None)['actions'][0]['id'], r['actions'][0]['id'])


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
