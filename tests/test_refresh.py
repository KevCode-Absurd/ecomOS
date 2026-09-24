import json
import unittest
from datetime import datetime, timezone

from meta_gallery.refresh import apply_sales, merge_meta, month_summary, shift_month
from meta_gallery.snapshot import build

NOW = datetime(2026, 9, 24, 3, 0, tzinfo=timezone.utc)


def row(ad, d, spend, purchases=None, value=None):
    return {'id': ad, 'name': 'Ad', 'date_start': d, 'date_stop': d, 'amount_spent': {'value': str(spend), 'unit': 'INR'},
            'omni_purchase': None if purchases is None else str(purchases),
            'omni_purchase_values': None if value is None else {'value': str(value), 'unit': 'INR'},
            'impressions': '100', 'link_click': '5'}


def capture():
    ads = [{'id': 'a1', 'name': 'Ad', 'campaign_id': 'c', 'campaign_name': 'C', 'adset_id': 's', 'adset_name': 'S',
            'creative_id': 'cr1', 'effective_status': 'ACTIVE', 'status': 'ACTIVE',
            'amount_spent': {'value': '300', 'unit': 'INR'}, 'omni_purchase': '1',
            'omni_purchase_values': {'value': '900', 'unit': 'INR'}, 'impressions': '300', 'link_click': '15'}]
    return {'version': 2, 'captured_at': '2026-09-23T16:20:31Z', 'source': 'test', 'ad_account_id': 'act_1',
            'window': {'since': '2026-09-01', 'until': '2026-09-03'}, 'account': [{'name': 'Test'}],
            'ads': ads, 'creatives': [{'id': 'cr1', 'image_hash': 'h'}], 'videos': [], 'images': [], 'adsets': [],
            'daily': [row('a1', '2026-09-01', 100), row('a1', '2026-09-02', 100), row('a1', '2026-09-03', 100, 1, 900)],
            'monthly': {'age': [{'date_start': '2026-09-01', 'date_stop': '2026-09-03', 'age': '25-34', 'id': 'a1',
                                 'amount_spent': {'value': '300'}, 'omni_purchase': '1', 'omni_purchase_values': {'value': '900'}}],
                        'gender': [], 'publisher_platform': []},
            'video_daily': []}


class MetaRefreshTests(unittest.TestCase):
    def test_repull_replaces_days_and_extends_window(self):
        new = [row('a1', '2026-09-03', 150, 2, 1500), row('a1', '2026-09-04', 80)]
        cap, checks = merge_meta(capture(), '2026-09-03', '2026-09-04', new, account_total=430.0, now=NOW)
        self.assertEqual(cap['window'], {'since': '2026-09-01', 'until': '2026-09-04'})
        self.assertEqual(sorted(r['date_start'] for r in cap['daily']), ['2026-09-01', '2026-09-02', '2026-09-03', '2026-09-04'])
        ad = cap['ads'][0]
        self.assertEqual(ad['amount_spent']['value'], '430.00')  # 300 - 100 + 150 + 80
        self.assertEqual(ad['omni_purchase'], '2')
        self.assertEqual(checks['daily_spend_window'], 430.0)
        spend = sum(r[1] for r in build(cap)['daily']['a1'])
        self.assertEqual(spend, 430.0)

    def test_old_capture_is_not_changed(self):
        base = capture()
        before = json.dumps(base)
        merge_meta(base, '2026-09-03', '2026-09-03', [row('a1', '2026-09-03', 150)], now=NOW)
        self.assertEqual(json.dumps(base), before)

    def test_new_ad_without_details_fails(self):
        with self.assertRaises(ValueError):
            merge_meta(capture(), '2026-09-03', '2026-09-03', [row('zz', '2026-09-03', 5)], now=NOW)

    def test_rows_outside_range_fail(self):
        with self.assertRaises(ValueError):
            merge_meta(capture(), '2026-09-03', '2026-09-03', [row('a1', '2026-09-02', 5)], now=NOW)

    def test_undated_breakdown_replaces_month_bucket(self):
        age = [{'age': '25-34', 'id': 'a1', 'amount_spent': {'value': '330'}, 'omni_purchase': '2', 'omni_purchase_values': {'value': '1500'}}]
        cap, _ = merge_meta(capture(), '2026-09-01', '2026-09-04', [row('a1', '2026-09-04', 30)], {'age': age}, now=NOW)
        self.assertEqual(len(cap['monthly']['age']), 1)
        self.assertEqual(cap['monthly']['age'][0]['date_stop'], '2026-09-04')
        with self.assertRaises(ValueError):  # undated rows must cover one month from the 1st
            merge_meta(capture(), '2026-09-02', '2026-09-04', [row('a1', '2026-09-04', 30)], {'age': age}, now=NOW)


def day(sales, items, sku_code, price, refund=None):
    return {'sales': sales, 'orders': items, 'items': items, 'ot': {'Stock': [sales, items]}, 'refund': refund,
            'ret_items': 1 if refund else 0, 'karat': [['18K Yellow Gold', sales, items]],
            'types': [['g', 'Chain', sales, items]], 'bands': [['g', '10000-25000', items]], 'pay': [['EMI', items]],
            'ret': [], 'skus': [['g', sku_code, 'Ruby Chain', price, items]]}


def sales_file():
    d1, d2 = day(20000, 1, 'CH-1', 20000), day(15000, 1, 'CH-1', 15000)
    month = {'items': 0, 'ot': {}, 'refund': None, 'ret_items': 0, 'karat': [], 'types': [], 'bands': [], 'pay': [], 'ret': [], 'skus': []}
    shift_month(month, d1, 1)
    shift_month(month, d2, 1)
    return {'source': 'test', 'pulled_at': 'x', 'months': {'2026-09': month}, 'daily': {'2026-09-01': d1, '2026-09-02': d2},
            'ga': [['2026-09-01', 100, 5, 20000, 1]], 'daily_pulled_at': 'x'}


class SalesRefreshTests(unittest.TestCase):
    def test_late_order_moves_day_and_month(self):
        late = day(40000, 2, 'CH-1_16', 20000)  # same piece, new code on the day card
        late['skus'].append(['g', 'BR-2', 'Pearl Bracelet', 20000, 1])
        late['skus'][0][4] = 1
        expected = sales_file()['months']['2026-09']
        shift_month(expected, sales_file()['daily']['2026-09-02'], -1)
        shift_month(expected, late, 1)
        pull = {'days': {'2026-09-01': sales_file()['daily']['2026-09-01'], '2026-09-02': late},
                'month_totals': {'2026-09': month_summary(expected)},
                'ga': [['2026-09-02', 120, 6, 40000, 2]]}
        out, report = apply_sales(sales_file(), pull, now=NOW)
        self.assertEqual(report['days_changed'], ['2026-09-02'])
        self.assertEqual(report['ga_changed'], ['2026-09-02'])
        m = out['months']['2026-09']
        self.assertEqual(m['items'], 3)
        self.assertEqual(len(m['skus']), 2)  # the chain stays one row despite the code change
        self.assertEqual([r[0] for r in out['ga']], ['2026-09-01', '2026-09-02'])

    def test_code_only_change_is_reported_apart(self):
        s = sales_file()
        same = json.loads(json.dumps(s['daily']['2026-09-01']))
        same['skus'][0][1] = 'CH-1_16'
        out, report = apply_sales(s, {'days': {'2026-09-01': same}}, now=NOW)
        self.assertEqual((report['days_changed'], report['codes_only']), ([], ['2026-09-01']))
        self.assertEqual(month_summary(out['months']['2026-09']), month_summary(s['months']['2026-09']))

    def test_month_mismatch_fails(self):
        s = sales_file()
        want = month_summary(s['months']['2026-09'])
        want['counts']['items'] += 1
        with self.assertRaises(ValueError):
            apply_sales(s, {'days': {}, 'month_totals': {'2026-09': want}}, now=NOW)

    def test_money_rounding_is_allowed(self):
        s = sales_file()
        want = month_summary(s['months']['2026-09'])
        want['money']['skus'] += 3.5  # month card rounds differently from day cards
        apply_sales(s, {'days': {}, 'month_totals': {'2026-09': want}}, now=NOW)

    def test_new_month_is_built_from_days(self):
        pull = {'days': {'2026-10-01': day(9000, 1, 'PE-3', 9000, refund=500)}}
        out, _ = apply_sales(sales_file(), pull, now=NOW)
        m = out['months']['2026-10']
        self.assertEqual((m['items'], m['refund'], m['ret_items']), (1, 500, 1))


if __name__ == '__main__':
    unittest.main()
