import unittest

from meta_gallery import valuerules as vr


class ValueRulesTest(unittest.TestCase):
    def test_sale_words(self):
        for n in ['AOF - Sales Campaign - EOSS', "BFCM '25 - Pre Sale", 'BL - TOF - 2 days to go EOSS Sale', 'BL - TOF - Akshaya Tritiya - 48 hours left', 'Festive Countdown 24 hours', 'Navratri campaign']:
            self.assertTrue(vr.is_sale(n), n)
        for n in ['BL - TOF - Navrathna Video ad', 'BL - TOF - Rings Collection', 'Wholesale buyers', '5% OFF with code']:
            self.assertFalse(vr.is_sale(n), n)

    def test_build_splits_sale(self):
        rows = [{'age': '35-44', 'gender': 'female', 'amount_spent': {'value': '100'}, 'omni_purchase': '2', 'omni_purchase_values': {'value': '900'}, 'name': 'BL - TOF - Rings'},
                {'age': '35-44', 'gender': 'female', 'amount_spent': {'value': '50'}, 'omni_purchase': None, 'omni_purchase_values': None, 'name': 'EOSS sale - Countdown'},
                {'impression_device': 'iphone', 'amount_spent': '10', 'omni_purchase': '1', 'omni_purchase_values': '300', 'name': 'x'}]
        d = vr.build(rows)
        self.assertEqual(d['segments']['ag']['female|35-44'], {'all': [150, 2, 900], 'sale': [50, 0, 0]})
        self.assertEqual(d['segments']['dev']['iphone']['all'], [10, 1, 300])
        self.assertEqual(d['sale_campaigns'], ['EOSS sale - Countdown'])


if __name__ == '__main__':
    unittest.main()
