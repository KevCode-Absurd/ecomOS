"""Generator v2 (app/data/generate.py): determinism, orders as the one truth, calibration, unavailable is null.

Runs the generator at small scale into temp folders (a few seconds each). Needs numpy.
"""
import hashlib
import importlib.util
import json
import re
import shutil
import sqlite3
import tempfile
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AS_OF = date(2026, 9, 27)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


gen = load('ecomos_generate_v2', ROOT / 'app' / 'data' / 'generate.py')
COMMON = {'brand', 'simulated', 'source', 'captured_at'}
# Census columns per table from app/contracts/data-sources.md (v2). Renames where the contract
# name collides with a common column: sessions source/medium/campaign -> session_*, reviews source -> review_source.
# Nested line items live in order_lines; utm (source, ...) is flattened to utm_*; Meta windows are suffixed.
CENSUS = {
    'orders': ['id', 'created_at', 'customer_id', 'channel', 'discount', 'discount_codes', 'shipping', 'tax_lines', 'total',
               'total_current', 'refunds', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'landing_page',
               'referrer', 'first_visit_at', 'last_visit_at', 'days_to_conversion', 'order_index', 'status', 'payment_method'],
    'order_lines': ['sku', 'qty', 'qty_current', 'unit_price', 'unit_price_discounted', 'line_total', 'line_discount', 'cost'],
    'customers': ['id', 'orders_count', 'total_spent', 'first_order_at', 'email_consent', 'email_opt_in_level',
                  'email_consent_at', 'sms_consent', 'state'],
    'products': ['sku', 'price', 'compare_at_price', 'stock', 'tracked', 'cost', 'views', 'adds', 'checkouts', 'purchased',
                 'item_revenue', 'cart_to_view', 'purchase_to_view', 'title', 'type', 'weight', 'images'],
    'inventory': ['available', 'on_hand', 'incoming', 'committed', 'tracked'],
    'reversed_orders': ['order_id', 'type', 'reason', 'amount', 'opened_at', 'closed_at', 'outcome'],
    'payouts': ['net', 'status', 'issued_at', 'summary'],
    'abandoned_checkouts': ['abandoned_checkout_url', 'lines', 'discount_codes', 'tax_lines', 'total', 'customer_id'],
    'sessions': ['date', 'session_source', 'session_medium', 'session_campaign', 'channel_group', 'landing_page', 'device',
                 'new_vs_returning', 'sessions', 'engaged_sessions', 'users', 'new_users', 'product_view', 'add_to_cart',
                 'checkout', 'purchase', 'transactions', 'revenue', 'sampled', 'thresholded', 'other_row_loss'],
    'ad_rows': ['date', 'campaign_id', 'adset_id', 'ad_id', 'spend', 'impressions', 'reach', 'clicks', 'link_clicks',
                'purchases', 'purchase_value', 'purchases_7d_click', 'purchases_1d_view', 'add_to_cart', 'initiate_checkout',
                'video_p25', 'video_p100', 'creative_id', 'body', 'title', 'cta', 'image_hash', 'video_id', 'thumbnail_url',
                'is_dynamic'],
    'google_rows': ['row_kind', 'date', 'campaign_id', 'campaign_name', 'campaign_status', 'channel_type', 'bidding', 'spend',
                    'impressions', 'clicks', 'conversions', 'conversion_value', 'all_conversions', 'all_conversion_value',
                    'impression_share', 'top_is', 'abs_top_is', 'lost_is_budget', 'lost_is_rank', 'search_term', 'term_status',
                    'ad_group_id', 'quality_score', 'asset_group_id', 'ad_strength', 'clipped'],
    'flows': ['flow_id', 'flow_name', 'flow_status', 'trigger_type', 'message_id', 'channel', 'subject', 'sends', 'opens',
              'clicks', 'unsubscribes', 'bounces', 'attributed_revenue', 'attributed_orders', 'matched_order_ids'],
    'campaign_sends': ['campaign_id', 'campaign_name', 'status', 'send_time', 'send_strategy', 'audiences', 'use_smart_sending',
                       'attributed_revenue', 'attributed_orders'],
    'tickets': ['id', 'created_at', 'channel', 'reason', 'order_id', 'first_response_min', 'resolved_min', 'csat'],
    'reviews': ['sku', 'rating', 'text', 'date', 'review_source'],
    'speed_runs': ['page', 'variant', 'run', 'load_ms', 'lcp_ms', 'fcp_ms', 'bytes', 'requests'],
    'content_posts': ['platform', 'date', 'format', 'hook', 'views', 'saves', 'clicks', 'matched_orders'],
    'search_console': ['query', 'page', 'clicks', 'impressions', 'position'],
    'marketplace_listings': ['marketplace', 'listing_id', 'price', 'buy_box', 'stock', 'rating', 'reviews'],
    'inbound_pos': ['po_id', 'sku', 'qty', 'eta'],
}


def build(scale, out):
    return gen.Gen('bombas', scale=scale, seed=7, as_of=AS_OF, log=lambda *_: None).run(out)


def fingerprint(folder):
    db = sqlite3.connect(folder / 'data.sqlite')
    out = {}
    for (name,) in db.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
        h = hashlib.sha256()
        for row in db.execute(f'SELECT * FROM {name} ORDER BY rowid'):
            h.update(repr(row).encode())
        out[name] = h.hexdigest()
    db.close()
    for p in sorted((folder / 'aggregates').glob('*.json')):
        out[p.name] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


class Determinism(unittest.TestCase):
    def test_same_inputs_same_rows(self):
        a, b = Path(tempfile.mkdtemp()), Path(tempfile.mkdtemp())
        try:
            build(0.002, a)
            build(0.002, b)
            fa, fb = fingerprint(a), fingerprint(b)
            self.assertGreater(len(fa), 20)
            self.assertEqual(fa, fb)
        finally:
            shutil.rmtree(a, ignore_errors=True)
            shutil.rmtree(b, ignore_errors=True)


class Bombas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dir = Path(tempfile.mkdtemp())
        cls.g = build(0.01, cls.dir)
        cls.db = sqlite3.connect(cls.dir / 'data.sqlite')
        cls.agg = {p.stem: json.loads(p.read_text())['rows'] for p in (cls.dir / 'aggregates').glob('*.json')}

    @classmethod
    def tearDownClass(cls):
        cls.db.close()
        shutil.rmtree(cls.dir, ignore_errors=True)

    def one(self, q, *args):
        return self.db.execute(q, args).fetchone()[0]

    def cols(self, table):
        return [r[1] for r in self.db.execute(f'PRAGMA table_info({table})')]

    # ---- shape
    def test_window_is_24_months_daily_ending_last_full_day(self):
        days = [r['date'] for r in self.agg['daily']]
        self.assertEqual(len(days), 730)
        self.assertEqual(days[-1], AS_OF.isoformat())
        self.assertEqual(days[0], '2024-09-28')
        first, last = self.db.execute('SELECT min(created_at), max(created_at) FROM orders').fetchone()
        self.assertGreaterEqual(first, '2024-09-28T04:00:00Z')
        self.assertLess(last, '2026-09-28T04:00:00Z')

    def test_every_contract_table_exists_with_census_columns(self):
        text = (ROOT / 'app' / 'contracts' / 'data-sources.md').read_text(encoding='utf-8')
        named = set(re.findall(r'^### `(\w+)`', text, re.M))
        named |= set(re.findall(r'^\| `(\w+)`', text, re.M))
        tables = {r[0] for r in self.db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertEqual(sorted(named - tables), [])
        for table, cols in CENSUS.items():
            have = set(self.cols(table))
            self.assertEqual(sorted(set(cols) - have), [], table)
            self.assertTrue(COMMON <= have, table)

    def test_every_row_is_simulated(self):
        for (t,) in self.db.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall():
            self.assertEqual(self.one(f'SELECT count(*) FROM {t} WHERE simulated IS NOT 1 OR brand IS NOT ?', 'bombas'), 0, t)
        for name, rows in self.agg.items():
            doc = json.loads((self.dir / 'aggregates' / f'{name}.json').read_text())
            self.assertTrue(doc['simulated'], name)

    # ---- orders are the one truth
    def test_order_money_adds_up_from_lines(self):
        bad = self.one('''SELECT count(*) FROM orders o JOIN (SELECT order_id, sum(unit_price*qty) g, sum(line_total) n, sum(line_discount) d
                          FROM order_lines GROUP BY order_id) l ON l.order_id = o.id
                          WHERE abs(o.subtotal - l.g) > 0.02 OR abs(o.subtotal - o.discount - l.n) > 0.02 OR abs(o.discount - l.d) > 0.02
                             OR abs(o.total - (o.subtotal - o.discount + o.shipping + o.tax)) > 0.02
                             OR abs(o.total_current - (o.total - o.refunds)) > 0.02''')
        self.assertEqual(bad, 0)
        self.assertEqual(self.one('SELECT count(*) FROM orders WHERE id NOT IN (SELECT order_id FROM order_lines)'), 0)

    def test_aggregates_match_orders(self):
        daily = self.agg['daily']
        self.assertEqual(sum(r['orders'] for r in daily), self.one('SELECT count(*) FROM orders'))
        self.assertAlmostEqual(sum(r['net_sales'] for r in daily), self.one('SELECT sum(subtotal - discount) FROM orders'), delta=1.0)
        monthly = self.agg['monthly']
        self.assertEqual(sum(m['orders'] for m in monthly), sum(r['orders'] for r in daily))

    def test_sessions_imply_orders(self):
        tx = self.one('SELECT sum(transactions) FROM sessions')
        web = self.one("SELECT count(*) FROM orders WHERE channel = 'web'")
        self.assertEqual(tx, sum(r['ga4_transactions'] for r in self.agg['daily']))
        self.assertLessEqual(tx, web)
        self.assertAlmostEqual(tx / web, 0.93, delta=0.01)
        by_day = dict(self.db.execute('SELECT date, sum(transactions) FROM sessions GROUP BY date').fetchall())
        for r in self.agg['daily']:
            self.assertEqual(by_day.get(r['date'], 0), r['ga4_transactions'])
        self.assertEqual(self.one('SELECT count(*) FROM sessions WHERE sessions < transactions OR checkout < transactions'), 0)

    def test_meta_purchases_are_an_attributed_subset_with_overlap(self):
        meta = self.one('SELECT sum(purchases) FROM ad_rows')
        click = self.one('SELECT sum(purchases_7d_click) FROM ad_rows')
        view = self.one('SELECT sum(purchases_1d_view) FROM ad_rows')
        self.assertEqual(meta, click + view)
        self.assertEqual(meta, sum(r['meta_purchases'] for r in self.agg['daily']))
        ps = self.one("SELECT count(*) FROM orders WHERE acquisition_channel = 'paid_social'")
        self.assertLess(click, ps)
        self.assertGreater(view, 0)  # view credit sits on orders other channels also claim
        # every order Meta credits by utm names an ad that has rows
        missing = self.one("""SELECT count(*) FROM orders WHERE utm_medium = 'paid_social'
                              AND utm_content NOT IN (SELECT DISTINCT ad_id FROM ad_rows)""")
        self.assertEqual(missing, 0)
        self.assertEqual(self.one('SELECT count(*) FROM ad_rows WHERE spend > 0 AND impressions = 0'), 0)

    def test_google_conversions_subset_and_terms_do_not_reconcile(self):
        conv = self.one("SELECT sum(conversions) FROM google_rows WHERE row_kind = 'campaign'")
        self.assertEqual(conv, sum(r['google_conversions'] for r in self.agg['daily']))
        terms = self.one("SELECT sum(conversions) FROM google_rows WHERE row_kind = 'search_term'")
        search = self.one("SELECT sum(conversions) FROM google_rows WHERE row_kind = 'campaign' AND channel_type = 'SEARCH'")
        self.assertLessEqual(terms, search)
        self.assertEqual(self.one("SELECT count(*) FROM google_rows WHERE clipped = 1 AND impression_share IS NOT NULL"), 0)

    def test_klaviyo_matched_orders_exist_and_overlap(self):
        ids = set()
        rev = 0.0
        for table in ('flows', 'campaign_sends'):
            for m, r, n in self.db.execute(f'SELECT matched_order_ids, attributed_revenue, attributed_orders FROM {table}'):
                got = json.loads(m)
                self.assertEqual(len(got), n)
                ids.update(got)
                rev += r
        self.assertEqual(len(ids), sum(r['klaviyo_attributed_orders'] for r in self.agg['daily']))
        self.db.execute('CREATE TEMP TABLE k(id INTEGER PRIMARY KEY)')
        self.db.executemany('INSERT INTO k VALUES (?)', [(i,) for i in ids])
        self.assertEqual(self.one('SELECT count(*) FROM k WHERE id NOT IN (SELECT id FROM orders)'), 0)
        self.assertAlmostEqual(rev, self.one('SELECT sum(total) FROM orders WHERE id IN (SELECT id FROM k)'), delta=1.0)
        email = self.one("SELECT count(*) FROM orders WHERE acquisition_channel IN ('email', 'sms')")
        self.assertGreater(len(ids), email)  # overlap: Klaviyo also claims orders from other channels
        both = self.one("""SELECT count(*) FROM orders WHERE id IN (SELECT id FROM k) AND acquisition_channel = 'paid_social'""")
        self.assertGreater(both, 0)
        self.db.execute('DROP TABLE k')

    def test_payouts_sum_orders_less_fees(self):
        gross = self.one('SELECT sum(charges_gross) FROM payouts')
        sp = self.one("SELECT sum(total) FROM orders WHERE payment_method != 'paypal'")
        self.assertAlmostEqual(gross, sp, delta=1.0)
        net, fee, refunds, adj = self.db.execute(
            'SELECT sum(net), sum(charges_fee), sum(refunds_gross), sum(adjustments_gross) FROM payouts').fetchone()
        self.assertAlmostEqual(net, gross - fee + refunds + adj, delta=1.0)
        self.assertGreater(fee, 0)
        paid_refunds = self.one("SELECT sum(refunds) FROM orders WHERE payment_method != 'paypal'")
        self.assertAlmostEqual(-refunds, paid_refunds, delta=1.0)
        for (s,) in self.db.execute('SELECT summary FROM payouts LIMIT 5'):
            self.assertIn('charges_gross', json.loads(s))

    def test_returns_and_tickets_tie_to_orders(self):
        self.assertEqual(self.one('SELECT count(*) FROM reversed_orders WHERE order_id NOT IN (SELECT id FROM orders)'), 0)
        self.assertEqual(self.one("""SELECT count(*) FROM reversed_orders r JOIN orders o ON o.id = r.order_id
                                     WHERE r.opened_at < o.created_at OR r.amount > o.total + 0.01"""), 0)
        refunded = self.one("SELECT sum(amount) FROM reversed_orders WHERE outcome = 'refunded' AND type = 'return'")
        self.assertAlmostEqual(refunded, self.one('SELECT sum(refunds) FROM orders'), delta=1.0)
        self.assertEqual(self.one("SELECT count(*) FROM reversed_orders WHERE type NOT IN ('return', 'chargeback', 'inquiry')"), 0)
        rate = self.one("SELECT count(*) FROM reversed_orders WHERE type = 'return' AND reason != 'carrier_returned'") / \
            self.one("SELECT count(*) FROM orders WHERE channel = 'web'")
        self.assertAlmostEqual(rate, 0.06, delta=0.01)
        self.assertEqual(self.one('SELECT count(*) FROM tickets WHERE order_id IS NOT NULL AND order_id NOT IN (SELECT id FROM orders)'), 0)
        self.assertEqual(self.one('''SELECT count(*) FROM tickets t JOIN orders o ON o.id = t.order_id
                                     WHERE t.created_at < substr(o.created_at, 1, 10)'''), 0)
        self.assertGreater(self.one('SELECT count(*) FROM tickets WHERE order_id IS NULL'), 0)

    def test_reviews_tie_to_products(self):
        self.assertEqual(self.one('SELECT count(*) FROM reviews WHERE sku NOT IN (SELECT sku FROM products)'), 0)
        self.assertGreater(self.one('SELECT count(*) FROM reviews'), 0)
        self.assertEqual(self.one('SELECT count(*) FROM order_lines WHERE sku NOT IN (SELECT sku FROM products)'), 0)

    def test_customers_tie_to_orders(self):
        self.assertEqual(self.one('SELECT count(*) FROM orders WHERE customer_id NOT IN (SELECT id FROM customers)'), 0)
        bad = self.one('''SELECT count(*) FROM customers c JOIN (SELECT customer_id, count(*) n FROM orders GROUP BY customer_id) o
                          ON o.customer_id = c.id WHERE c.orders_count < o.n''')
        self.assertEqual(bad, 0)

    def test_inventory_never_negative(self):
        self.assertEqual(self.one('SELECT count(*) FROM inventory WHERE available < 0 OR on_hand < 0'), 0)

    # ---- calibration
    def test_calibration_hits(self):
        cal = self.agg['calibration']
        a = self.g.p
        total = cal['revenue_last_12m']['total']
        self.assertTrue(a['revenue_low'] * 0.01 <= total <= a['revenue_high'] * 0.01, total)
        self.assertAlmostEqual(total / (a['revenue_point'] * 0.01), 1.0, delta=0.04)
        aov = self.one('SELECT avg(subtotal - discount) FROM orders')
        self.assertAlmostEqual(aov / a['aov'], 1.0, delta=0.05)
        self.assertAlmostEqual(cal['repeat_12m']['generated'], a['repeat_12m'], delta=0.03)
        self.assertLess(cal['seasonality_last_12m']['max_abs_diff'], 0.10)
        self.assertAlmostEqual(cal['category_mix_net_sales']['socks_slippers'], 0.93, delta=0.02)
        mix = cal['acquisition_mix_web_orders']['generated']
        self.assertAlmostEqual(mix['paid_social'], 0.35, delta=0.02)
        self.assertAlmostEqual(mix['email'] + mix['sms'], 0.10, delta=0.02)
        man = json.loads((self.dir / 'manifest.json').read_text())
        self.assertEqual(man['fields']['revenue_band']['origin'], 'brain')
        self.assertEqual(man['fields']['channel_mix']['origin'], 'fallback (generic)')
        self.assertIn('return_rate', man['placeholders'])

    def test_monthly_index_follows_seasonality(self):
        # December and November are the peaks; February is the low, as in the brain index
        m = {r['month']: r['net_sales'] for r in self.agg['monthly']}
        self.assertGreater(m['2025-12'], m['2025-11'] > m['2025-10'])
        self.assertGreater(m['2025-11'], 1.6 * m['2026-02'])

    # ---- unavailable is null, never 0
    def test_no_zeros_where_unavailable(self):
        q = self.one
        self.assertEqual(q("SELECT count(*) FROM orders WHERE journey_ready = 0 AND (utm_source IS NOT NULL OR landing_page IS NOT NULL OR days_to_conversion IS NOT NULL)"), 0)
        self.assertGreater(q('SELECT count(*) FROM orders WHERE journey_ready = 0'), 0)
        self.assertEqual(q("SELECT count(*) FROM orders WHERE channel = 'pos' AND (landing_page IS NOT NULL OR journey_ready IS NOT NULL)"), 0)
        self.assertEqual(q('SELECT count(*) FROM customers WHERE state IS NOT NULL'), 0)
        self.assertEqual(q('SELECT count(*) FROM marketplace_listings'), 0)
        self.assertEqual(q("SELECT count(*) FROM reversed_orders WHERE type = 'rto'"), 0)
        self.assertEqual(q("SELECT count(*) FROM flows WHERE channel = 'sms' AND opens IS NOT NULL"), 0)
        self.assertEqual(q("SELECT count(*) FROM ad_rows WHERE format != 'video' AND (video_p25 IS NOT NULL OR video_id IS NOT NULL)"), 0)
        self.assertEqual(q('SELECT count(*) FROM tickets WHERE csat = 0'), 0)
        self.assertEqual(q("SELECT count(*) FROM google_rows WHERE channel_type != 'SEARCH' AND row_kind = 'campaign' AND impression_share IS NOT NULL"), 0)
        self.assertEqual(q("SELECT count(*) FROM orders WHERE utm_source = '' OR landing_page = ''"), 0)


if __name__ == '__main__':
    unittest.main()
