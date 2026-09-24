import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from meta_gallery import ai, products


def page(code='GHCSBG-6129', pics=2, extra_products=()):
    state = {
        'ProductType:1': {
            '__typename': 'ProductType', 'name': 'Celestial Navaratna 18K Gold Bracelet', 'slug': 'celestial-navaratna-18k-gold-bracelet',
            'product_code': code, 'description': 'A  bracelet\nwith 9 stones.', 'avatar_url': 'https://cdn-assets.gehnaindia.com/avatar',
            'social_badge': {'value': 'IN <span>10+</span> CARTS THIS SEASON'},
            'as_website_pictures': [{'asset_type': 'image', 'large': f'https://cdn-assets.gehnaindia.com/large{i}', 'medium': f'https://cdn-assets.gehnaindia.com/m{i}'} for i in range(pics)]
            + [{'asset_type': 'video', 'original': 'https://cdn-assets.gehnaindia.com/video'}],
            'variation': {'__ref': 'VariationType:9'},
            'metal_karatage': [{'__ref': 'PropertyType:210'}], 'gemstone': [{'__ref': 'PropertyType:361'}], 'gemstone_color': [{'__ref': 'PropertyType:443'}],
            'product_length': [{'__ref': 'PropertyType:555'}], 'order_type': {'__ref': 'PropertyType:356'},
            'metal_karatages': [{'metal_karatage': '18K Yellow Gold', 'selected': True}, {'metal_karatage': '14K Yellow Gold', 'selected': False}],
            'expected_delivery_date_range': ['2026-09-27', '2026-09-28'], 'is_ship_fast_tag_applicable': True, 'is_stock_available_at_gehna_store': True,
            'frequent_questions': [{'question': 'Is this BIS hallmarked?', 'answer': '<div>Yes, all our gold is <strong>BIS hallmarked</strong>.&nbsp;<br></div>'}],
        },
        'VariationType:9': {'selling_price': 21000, 'special_price': 19999, 'gold_weight': 0.71, 'gross_weight': 2.05, 'gem_stone_weight': 6.7,
                            'emi_table': [{'no_of_month': 3, 'down_payment': 4000, 'emi_amount': 5333}, {'no_of_month': 6, 'down_payment': 4000, 'emi_amount': 2667}]},
        'PropertyType:210': {'name': '18K Yellow Gold'}, 'PropertyType:361': {'name': 'Navratna Stones'}, 'PropertyType:443': {'name': 'Multicolor'},
        'PropertyType:555': {'name': '7 Inches'}, 'PropertyType:356': {'name': 'Stock'},
        'ROOT_QUERY': {'googleReview': {'averageRating': 4.8, 'totalReviewCount': 514, 'reviews': [
            {'starRating': 'FIVE', 'comment': 'Loved the jewellery, the details and the quality of stone is just incredible.', 'reviewer': {'displayName': 'A Person'}},
            {'starRating': 'THREE', 'comment': 'It was fine but took a while to reach me at home in the city.'}]}},
        **{f'ProductType:{i + 2}': p for i, p in enumerate(extra_products)},
    }
    data = {'props': {'pageProps': {'initialApolloState': state}}}
    return f'<html><script id="__NEXT_DATA__" type="application/json">{json.dumps(data)}</script></html>'


JPEG = b'\xff\xd8\xff\xe0' + b'0' * 100
AVIF = b'\x00\x00\x00\x1cftypavif' + b'0' * 100


class SlugTest(unittest.TestCase):
    def test_slugify_matches_site_urls(self):
        self.assertEqual(products.slugify('Celestial Navaratna 18K Gold Bracelet '), 'celestial-navaratna-18k-gold-bracelet')
        self.assertEqual(products.slugify('Lustrous Pearl 18K Gold Pendant (without chain)'), 'lustrous-pearl-18k-gold-pendant')
        self.assertEqual(products.slugify(' Intricate Filigree & Pearl 18K Gold Dangle Earrings'), 'intricate-filigree-pearl-18k-gold-dangle-earrings')

    def test_base_code_drops_size(self):
        self.assertEqual(products.base_code('GHCSRG-6538_17'), 'GHCSRG-6538')


class ParseTest(unittest.TestCase):
    def test_reads_product_price_emi_and_photos(self):
        p = products.parse_product(page(), 'GHCSBG-6129')
        self.assertEqual(p['code'], 'GHCSBG-6129')
        self.assertTrue(p['code_match'])
        self.assertEqual(p['price'], 19999)
        self.assertEqual(p['emi_months'], 6)
        self.assertEqual(p['badge'], 'IN 10+ CARTS THIS SEASON')
        self.assertEqual(p['description'], 'A bracelet with 9 stones.')
        self.assertEqual([x['url'] for x in p['photos']], ['https://cdn-assets.gehnaindia.com/large0', 'https://cdn-assets.gehnaindia.com/large1'])

    def test_page_facts(self):
        p = products.parse_product(page(), 'GHCSBG-6129', today='2026-09-24')
        texts = [f['text'] for f in p['facts']]
        groups = {f['group'] for f in p['facts']}
        self.assertIn('18K Yellow Gold', texts)
        self.assertIn('Gold weight 0.71 g net, gross weight 2.05 g', texts)
        self.assertIn('Stones: Navratna Stones, 6.7 ct', texts)
        self.assertIn('Length 7 Inches', texts)
        self.assertIn('Also made in 14K Yellow Gold', texts)
        self.assertIn('Ready stock', texts)
        self.assertIn('EMI: ₹4,000 down, then ₹2,667 a month for 6 months', texts)
        self.assertIn('Delivered in about 4 days, fully insured', texts)
        self.assertIn('Site badge: In 10+ carts this season', texts)
        self.assertIn('Rated 4.8 out of 5 from 514 Google reviews of the store', texts)
        self.assertIn('Is this BIS hallmarked? Yes, all our gold is BIS hallmarked.', texts)
        self.assertIn('Lifetime exchange', texts)
        self.assertNotIn('Certified diamonds', texts)
        reviews = [t for t in texts if t.startswith('A store review')]
        self.assertEqual(len(reviews), 1)          # 5 stars only
        self.assertNotIn('A Person', ' '.join(texts))  # never reviewer names
        self.assertEqual(groups, {'product', 'price', 'delivery', 'proof', 'trust', 'faq', 'review', 'story'})

    def test_flags_a_different_code(self):
        p = products.parse_product(page('GHCSER-7863'), 'GHCSER-732')
        self.assertFalse(p['code_match'])

    def test_picks_the_product_with_the_wanted_code(self):
        other = {'name': 'Other', 'product_code': 'GHX-1', 'as_website_pictures': []}
        p = products.parse_product(page('GHCSBG-6129', extra_products=[other]), 'GHX-1_18')
        self.assertEqual(p['name'], 'Other')

    def test_avatar_when_no_photos(self):
        p = products.parse_product(page(pics=0))
        self.assertEqual(len(p['photos']), 1)

    def test_no_next_data(self):
        self.assertIsNone(products.parse_product('<html></html>'))


class FetchTest(unittest.TestCase):
    def test_product_caches_photos_and_falls_back_from_avif(self):
        calls = []

        def fake_get(url, accept='*/*', limit=0, timeout=0):
            calls.append(url)
            if url.endswith('/celestial-navaratna-18k-gold-bracelet'):
                return 200, page().encode()
            if url.endswith('large0'):
                return 200, JPEG
            if url.endswith('large1'):
                return 200, AVIF
            if '_next/image' in url:
                return 200, b'RIFF0000WEBP' + b'0' * 50
            return 404, b''

        with tempfile.TemporaryDirectory() as d, mock.patch.object(products, '_get', fake_get):
            meta = products.product('Celestial Navaratna 18K Gold Bracelet', 'GHCSBG-6129', folder=d)
            self.assertEqual([p['file'] for p in meta['photos']], ['1.jpg', '2.webp'])
            self.assertEqual(meta['url'], 'https://www.gehnaindia.com/celestial-navaratna-18k-gold-bracelet')
            n = len(calls)
            products.product('Celestial Navaratna 18K Gold Bracelet', 'GHCSBG-6129', folder=d)
            self.assertEqual(len(calls), n)  # served from cache
            got = products.photo_bytes(meta['slug'], [2], folder=d)
            self.assertEqual(got[0][1], 'image/webp')
            self.assertIsNone(products.photo_path('../etc', '1.jpg', folder=d))
            self.assertIsNone(products.photo_path(meta['slug'], 'product.json', folder=d))

    def test_missing_page(self):
        with tempfile.TemporaryDirectory() as d, mock.patch.object(products, '_get', lambda *a, **k: (404, b'')):
            with self.assertRaises(products.ProductError):
                products.product('Nope Ring', folder=d)


class ProductAdsTest(unittest.TestCase):
    def test_prompt_has_facts_rules_and_reference(self):
        p = {'name': 'Celestial Navaratna 18K Gold Bracelet', 'code': 'GHCSBG-6129', 'price': 19999, 'emi_months': 6, 'sold': '20 sold in 60 days'}
        with mock.patch.object(ai, 'load_brand', return_value={}):
            text = ai.product_prompt(p, 4, 2, True, 'portrait')
        self.assertIn('Images 1 to 2 are the site photos', text)
        self.assertIn('Image 3 is a style reference', text)
        self.assertIn('Rs 19,999', text)
        self.assertIn('20 sold in 60 days', text)
        self.assertIn('1024x1280', text)
        self.assertIn('never invent discounts', text)
        with mock.patch.object(ai, 'load_brand', return_value={}):
            text = ai.product_prompt(dict(p, facts=['Lifetime exchange', '7 day return']), 3, 1, False)
        self.assertIn('the only claims you may use', text)
        self.assertIn('- Lifetime exchange', text)

    def test_make_product_ads_saves_copy_with_each_image(self):
        plan = json.dumps({'concepts': [{'name': 'Gift box', 'angle': 'gifting', 'idea': 'Bracelet in an open gift box.', 'primary_text': 'Line 1.\nLine 2.',
                                         'headline': 'Made for her wrist', 'description': 'Shop the bracelet', 'uses': ['Lifetime exchange'],
                                         'primary_alt': ['Alt 1', 'Alt 2', 'Alt 3'], 'headline_alt': ['H2']}]})
        cfg = {'openai_key': 'k', 'anthropic_key': 'a', 'AI_IMAGE_MODEL': 'm', 'AI_IMAGE_FALLBACK': 'm'}
        seen = {}

        def fake_variant(cfg_, prompt, images, size, quality):
            seen['images'] = images
            seen['prompt'] = prompt
            return b'\x89PNG\r\n\x1a\n', 'm'

        with tempfile.TemporaryDirectory() as d, mock.patch.object(ai, 'settings', return_value=cfg), \
                mock.patch.object(ai, '_ask', return_value=(plan, 'x', 'claude')), mock.patch.object(ai, 'make_variant', fake_variant), \
                mock.patch.object(ai, 'load_brand', return_value={}):
            made = ai.make_product_ads({'name': 'Celestial', 'slug': 'celestial'}, [(JPEG, 'image/jpeg')], 1, 'square', 'low', ref_bytes=JPEG, out_dir=d)
            self.assertEqual(made[0]['headline'], 'Made for her wrist')
            self.assertEqual(made[0]['angle'], 'gifting')
            self.assertEqual(made[0]['primary_alt'], ['Alt 1', 'Alt 2'])
            self.assertEqual(made[0]['headline_alt'], ['H2'])
            self.assertIn('built on: Lifetime exchange', seen['prompt'])
            self.assertEqual(len(seen['images']), 2)
            self.assertIn('Image 2 is a style reference', seen['prompt'])
            listed = ai.list_product_ads('celestial', out_dir=d)
            self.assertEqual(listed[0]['primary_text'], 'Line 1.\nLine 2.')
            self.assertIsNotNone(ai.product_ad_path('celestial', listed[0]['file'], out_dir=d))
            self.assertIsNone(ai.product_ad_path('../x', listed[0]['file'], out_dir=d))

    def test_no_photos_refuses_images(self):
        cfg = {'openai_key': 'k', 'anthropic_key': ''}
        with mock.patch.object(ai, 'settings', return_value=cfg):
            with self.assertRaises(ai.AIError):
                ai.make_product_ads({'name': 'X', 'slug': 'x-ring'}, [], 2)

    def test_edit_sends_the_real_image_type(self):
        sent = {}

        def fake_post(url, headers, body, cfg, timeout=0):
            sent['body'] = body
            return {'data': [{'b64_json': ''}]}

        with mock.patch.object(ai, '_post', fake_post):
            ai._edit({'openai_key': 'k'}, 'm', 'p', [JPEG, b'RIFF0000WEBP0000'], '1024x1024', 'low')
        self.assertIn(b'Content-Type: image/webp', sent['body'])
        self.assertIn(b'filename="reference2.webp"', sent['body'])


if __name__ == '__main__':
    unittest.main()


class CatalogStoryTest(unittest.TestCase):
    def test_story_uses_page_facts_and_body_part(self):
        p = {'name': 'Celestial Bracelet', 'slug': 'celestial', 'cat': 'Bracelets', 'facts': [
            {'group': 'trust', 'text': 'BIS hallmarked gold'}, {'group': 'trust', 'text': 'Lifetime exchange'}, {'group': 'trust', 'text': '7 day return'},
            {'group': 'product', 'text': 'Gold weight 0.71 g net'}, {'group': 'proof', 'text': 'Rated 4.8 out of 5 from 514 Google reviews of the store'},
            {'group': 'price', 'text': 'Price ₹22,210, inclusive of all taxes'}]}
        c = ai.story_concepts(p, 15)
        self.assertEqual(len(c), 15)
        self.assertEqual(c[0]['shot'], 'hero')
        worn = next(x for x in c if x['shot'] == 'worn')
        self.assertIn('wrist', worn['prompt'])
        why = next(x for x in c if x['shot'] == 'benefits')
        self.assertIn('BIS hallmarked gold; Lifetime exchange; 7 day return', why['prompt'])
        self.assertIn('Price ₹22,210', next(x for x in c if x['shot'] == 'price')['prompt'])
        self.assertEqual(len(ai.story_concepts(p, 5)), 5)
        self.assertIn('exact same piece', ai.story_prompt(p, c[0]))

    def test_story_skips_cards_without_facts(self):
        c = ai.story_concepts({'name': 'X', 'cat': 'Rings', 'facts': []}, 15)
        self.assertNotIn('proof', [x['shot'] for x in c])
        self.assertNotIn('price', [x['shot'] for x in c])

    def test_catalog_image_keeps_the_piece_whatever_the_prompt(self):
        cfg = {'openai_key': 'k', 'anthropic_key': '', 'AI_IMAGE_MODEL': 'm', 'AI_IMAGE_FALLBACK': 'm'}
        seen = {}

        def fake_variant(cfg_, prompt, images, size, quality):
            seen['prompt'] = prompt
            return b'\x89PNG\r\n\x1a\n', 'm'

        with tempfile.TemporaryDirectory() as d, mock.patch.object(ai, 'settings', return_value=cfg), mock.patch.object(ai, 'make_variant', fake_variant):
            made = ai.make_catalog_image('GHCSBG-6129', JPEG, 'Put it on a red background', 'high', out_dir=d)
            self.assertTrue(made['file'].endswith('.png'))
            self.assertIn('red background', seen['prompt'])
            self.assertIn('exact same piece', seen['prompt'])
            self.assertEqual(list(ai.list_catalog_images(out_dir=d)), ['GHCSBG-6129'])
            self.assertIsNone(ai.catalog_image_path('../x', made['file'], out_dir=d))
            with self.assertRaises(ai.AIError):
                ai.make_catalog_image('bad code!', JPEG, out_dir=d)
