import tempfile
import unittest
from pathlib import Path
from intelligence.library import build_index, search_cards, validate_cards


class LibraryTests(unittest.TestCase):
    def test_search_keeps_caveat_and_respects_whole_context_budget(self):
        cards = [dict(id='checkout', title='Guest checkout friction', summary='Remove checkout barriers',
                      use_when='Customers abandon checkout', steps=['Offer guest checkout.'],
                      caveats=['Measure completed orders, not button clicks.'], tags=['checkout'], domain='cro'),
                 dict(id='research', title='Research a product category', summary='Find customer needs',
                      use_when='Selecting a product', steps=['Review customer complaints.'],
                      caveats=[], tags=['research'], domain='product')]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'search.sqlite'; build_index(path,cards)
            result=search_cards(path,'checkout',1000)
            self.assertEqual(result['cards'][0]['id'],'checkout')
            self.assertIn('not button clicks',result['context'])
            self.assertLessEqual(len(result['context'].encode()),1000)
            self.assertEqual(search_cards(path,'checkout',10)['cards'],[])
            self.assertEqual(search_cards(path,'checkout',1000,domain='product')['cards'],[])
            self.assertEqual(search_cards(path,'checkout',1000,max_cards=0)['cards'],[])

    def test_malformed_output_is_not_published(self):
        for output in [None, {'cards':[{}]}, {'cards':'not a list'}]:
            with self.assertRaises(ValueError):validate_cards(output)
