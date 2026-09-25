import json
import tempfile
import unittest
from pathlib import Path

from meta_gallery import stock


def page(order=None, extra=None, var_extra=None, rng=None, code='GHCSBG-6129'):
    state = {'Variation:1': {'selling_price': 22210, **(var_extra or {})}}
    p = {'product_code': code, 'name': 'Celestial Navaratna 18K Gold Bracelet', 'variation': {'__ref': 'Variation:1'}, **(extra or {})}
    if order:
        state['OrderType:1'] = {'name': order}
        p['order_type'] = [{'__ref': 'OrderType:1'}]
    if rng:
        p['expected_delivery_date_range'] = rng
    state['ProductType:1'] = p
    data = {'props': {'pageProps': {'initialApolloState': state}}}
    return f'<html><script id="__NEXT_DATA__" type="application/json">{json.dumps(data)}</script></html>'


class StockTest(unittest.TestCase):
    def test_ready_and_made(self):
        self.assertEqual(stock.status_from_page(page('Stock'))[0], 'ready')
        st, info = stock.status_from_page(page('Made To Order', rng=['2026-10-01', '2026-10-09']), today='2026-09-25')
        self.assertEqual(st, 'made')
        self.assertEqual(info['days'], 14)
        self.assertEqual(stock.status_from_page(page(extra={'is_ship_fast_tag_applicable': True}))[0], 'ready')

    def test_out_and_gone(self):
        self.assertEqual(stock.status_from_page(page('Stock', extra={'is_in_stock': False}))[0], 'out')
        self.assertEqual(stock.status_from_page(page('Stock', var_extra={'stock_status': 'OUT_OF_STOCK'}))[0], 'out')
        self.assertEqual(stock.status_from_page('<html>no data</html>')[0], 'gone')
        self.assertEqual(stock.status_from_page(page())[0], 'unknown')

    def test_quantity_zero_alone_is_not_out(self):
        # Made to order pieces can show 0 in stock and still be sold.
        self.assertEqual(stock.status_from_page(page('Made To Order', var_extra={'qty': 0}))[0], 'made')

    def test_run_writes_file(self):
        with tempfile.TemporaryDirectory() as d:
            cat = Path(d) / 'catalog.json'
            cat.write_text(json.dumps({'products': [{'code': 'A-1', 'name': 'One', 'url': 'u1'}, {'code': 'B-2', 'name': 'Two', 'url': 'u2'}]}))
            fake = lambda it, today=None: {**it, 'status': 'ready' if it['code'] == 'A-1' else 'gone'}
            doc = stock.run(cat, Path(d) / 'stock.json', check=fake)
            self.assertEqual(doc['counts']['ready'], 1)
            self.assertEqual(doc['counts']['gone'], 1)
            saved = json.loads((Path(d) / 'stock.json').read_text())
            self.assertEqual(saved['products']['A-1']['rank'], 1)


if __name__ == '__main__':
    unittest.main()
