import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from datetime import date, timedelta
from pathlib import Path

from meta_gallery import settings as settings_mod
from meta_gallery.graph_client import Graph, load_env, to_row
from meta_gallery.metrics import collection_roas, derive
from meta_gallery.server import Gallery, make_handler
from meta_gallery.share import page_data
from meta_gallery.snapshot import build, classify
from meta_gallery.themes import tag
from meta_gallery.view import Engine, ViewError

SINCE = '2026-01-01'
UNTIL = '2026-03-31'  # 90 days


def iso(i):
    return (date.fromisoformat(SINCE) + timedelta(days=i)).isoformat()


def ad_row(i, creative, campaign='Evergreen', camp_id='900'):
    return {'id': str(100000 + i), 'name': f'Ad {i}', 'effective_status': 'PAUSED', 'status': 'ACTIVE',
            'campaign_id': camp_id, 'campaign_name': campaign, 'adset_id': '800', 'adset_name': 'Set',
            'creative_id': creative, 'amount_spent': {'value': '1', 'unit': 'INR'}}


def day(i, d, spend, purchases=None, value=None, impr=1000, clicks=20):
    return {'id': str(100000 + i), 'date_start': iso(d), 'date_stop': iso(d), 'amount_spent': {'value': str(spend)},
            'omni_purchase': None if purchases is None else str(purchases),
            'omni_purchase_values': None if value is None else {'value': str(value)},
            'impressions': str(impr), 'link_click': str(clicks)}


def synthetic_capture(n_static=35):
    creatives = [{'id': f'c{i}', 'object_type': 'SHARE', 'image_hash': 'h1' if i < 2 else f'h{i}'} for i in range(n_static)]
    creatives += [{'id': 'vid', 'object_type': 'VIDEO', 'video_id': '1'},
                  {'id': 'cat', 'object_type': 'SHARE', 'product_set_id': '5'},
                  {'id': 'car', 'object_type': 'SHARE', 'child_attachments': [{'name': 'Card', 'image_hash': 'k1', 'link': 'https://x'}]},
                  {'id': 'flex', 'object_type': 'SHARE'}]
    ads = [ad_row(i, f'c{i}') for i in range(n_static)]
    ads += [ad_row(100, 'vid'), ad_row(101, 'cat'), ad_row(102, 'car'), ad_row(103, 'flex', 'EOSS Sale - 25/08', '901')]
    daily = []
    for i in range(n_static):
        for d in range(60, 90):  # last 30 days only
            daily.append(day(i, d, 10 - i * 0.1, 1 if (i == 0 and d == 89) else None, 500 if (i == 0 and d == 89) else None))
    for i, s in ((100, 900), (101, 800), (102, 700)):
        for d in range(0, 90):
            daily.append(day(i, d, s, 1, s * 3))
    for d in range(30, 90):  # the sale campaign ad
        daily.append(day(103, d, 1000, 1, 5000))
    monthly = {'age': [], 'gender': [], 'publisher_platform': []}
    for m_start, m_stop in (('2026-01-01', '2026-01-31'), ('2026-02-01', '2026-02-28'), ('2026-03-01', '2026-03-31')):
        for i in (0, 100):
            monthly['age'] += [{'id': str(100000 + i), 'date_start': m_start, 'date_stop': m_stop, 'age': '25-34',
                                'amount_spent': {'value': '60'}, 'omni_purchase': '1', 'omni_purchase_values': {'value': '300'}},
                               {'id': str(100000 + i), 'date_start': m_start, 'date_stop': m_stop, 'age': '35-44',
                                'amount_spent': {'value': '40'}, 'omni_purchase': None, 'omni_purchase_values': None}]
            monthly['gender'] += [{'id': str(100000 + i), 'date_start': m_start, 'date_stop': m_stop, 'gender': 'female',
                                   'amount_spent': {'value': '100'}, 'omni_purchase': '1', 'omni_purchase_values': {'value': '300'}}]
    return {'version': 2, 'captured_at': '2026-04-01T06:00:00+05:30', 'source': 'synthetic', 'ad_account_id': '1',
            'window': {'since': SINCE, 'until': UNTIL},
            'account': [{'name': 'Test', 'timezone_name': 'Asia/Kolkata', 'amount_spent': {'unit': 'INR'}}],
            'ads': ads, 'creatives': creatives, 'videos': [], 'images': [{'hash': 'k1', 'url': 'https://img'}],
            'adsets': [{'id': '800', 'is_dynamic_creative': False, 'attribution_setting': '1d_view_7d_click'}],
            'daily': daily, 'monthly': monthly}


def engine():
    return Engine(build(synthetic_capture()))


class MetricTests(unittest.TestCase):
    def test_missing_values_stay_unavailable(self):
        m = derive(500.0, None, None, 1000.0, 0.0)
        self.assertIsNone(m['roas'])
        self.assertIsNone(m['cpa'])
        self.assertIsNone(m['link_cpc'])
        self.assertEqual(m['link_ctr'], 0.0)

    def test_period_roas_is_value_over_spend(self):
        ads = [{'metrics': derive(100.0, 1.0, 500.0, 1, 1)}, {'metrics': derive(300.0, None, None, 1, 1)}]
        total = collection_roas(ads)
        self.assertAlmostEqual(total['roas'], 500 / 400)
        self.assertEqual(total['ads_without_reported_value'], 1)


class SnapshotTests(unittest.TestCase):
    def test_classify(self):
        self.assertEqual(classify({'image_hash': 'x'}), 'static_image')
        self.assertEqual(classify({'image_hash': 'x', 'child_attachments': [{}]}), 'carousel')
        self.assertEqual(classify({'product_set_id': '1', 'image_hash': 'x'}), 'catalog_dynamic')
        self.assertEqual(classify({'object_type': 'VIDEO'}), 'video')
        self.assertEqual(classify({'object_type': 'SHARE'}), 'unconfirmed_mixed')
        self.assertEqual(classify(None), 'unknown')

    def test_missing_creative_fails_loudly(self):
        cap = synthetic_capture()
        cap['ads'].append(ad_row(200, 'missing'))
        with self.assertRaises(ValueError):
            build(cap)

    def test_old_capture_rejected(self):
        with self.assertRaises(ValueError):
            build({'periods': {}})

    def test_duplicate_daily_rows_ignored(self):
        cap = synthetic_capture()
        cap['daily'].append(dict(cap['daily'][0]))
        snap = build(cap)
        self.assertEqual(len(snap['daily']['100000']), 30)


class ViewTests(unittest.TestCase):
    def test_range_totals_and_previous_period(self):
        e = engine()
        v = e.view('2026-03-02', '2026-03-31')  # 30 days
        self.assertEqual(v['range']['days'], 30)
        self.assertEqual(v['previous']['since'], '2026-01-31')
        self.assertTrue(v['previous']['complete'])
        spend = sum(10 - i * 0.1 for i in range(35)) * 30 + (900 + 800 + 700 + 1000) * 30
        self.assertAlmostEqual(v['totals']['spend'], spend, places=4)
        self.assertAlmostEqual(v['totals']['roas'], v['totals']['purchase_value'] / v['totals']['spend'])
        # static ads did not spend in the previous 30 days
        self.assertAlmostEqual(v['previous_totals']['spend'], (900 + 800 + 700 + 1000) * 30)

    def test_previous_period_outside_window_is_marked_incomplete(self):
        v = engine().view('2026-01-01', '2026-01-10')
        self.assertEqual(v['previous']['days_covered'], 0)
        self.assertIsNone(v['previous_totals'])
        v = engine().view('2026-01-06', '2026-01-15')
        self.assertFalse(v['previous']['complete'])

    def test_bad_dates(self):
        with self.assertRaises(ViewError):
            engine().view('2026-03-10', '2026-03-01')
        with self.assertRaises(ViewError):
            engine().view('2027-01-01', '2027-02-01')

    def test_top_30_per_format(self):
        v = engine().view('2026-03-02', '2026-03-31')
        cols = v['collections']
        self.assertEqual(cols['static_image']['size'], 30)
        self.assertEqual(cols['static_image']['ad_ids'][0], '100000')
        self.assertNotIn('100100', cols['static_image']['ad_ids'])
        self.assertEqual(cols['video']['ad_ids'], ['100100'])
        self.assertEqual(cols['all']['ad_ids'][:4], ['100103', '100100', '100101', '100102'])
        self.assertEqual(cols['all']['size'], 30)

    def test_keyword_exclusion_recalculates_everything(self):
        e = engine()
        base = e.view('2026-03-02', '2026-03-31')
        v = e.view('2026-03-02', '2026-03-31', keywords=['  SALE '])
        self.assertEqual(v['exclusions']['keywords'], ['sale'])
        self.assertEqual(v['exclusions']['ads'], 1)
        self.assertAlmostEqual(v['exclusions']['spend'], 30000)
        self.assertAlmostEqual(base['totals']['spend'] - v['totals']['spend'], 30000)
        self.assertNotIn('100103', v['collections']['all']['ad_ids'])
        self.assertNotIn('unconfirmed_mixed', v['by_type'])
        self.assertAlmostEqual(v['previous_totals']['spend'], (900 + 800 + 700) * 30)
        by_id = e.view('2026-03-02', '2026-03-31', campaign_ids=['901'])
        self.assertAlmostEqual(by_id['totals']['spend'], v['totals']['spend'])

    def test_missing_value_stays_unavailable_in_range(self):
        v = engine().view('2026-03-02', '2026-03-31')
        m = v['ads']['100001']['view']['metrics']
        self.assertIsNone(m['purchase_value'])
        self.assertIsNone(m['roas'])
        self.assertEqual(v['ads']['100000']['view']['metrics']['purchase_value'], 500.0)

    def test_shared_image_keeps_ad_level_metrics(self):
        v = engine().view('2026-03-02', '2026-03-31')
        a, b = v['ads']['100000']['view'], v['ads']['100001']['view']
        self.assertEqual(a['same_media_ads'], ['100001'])
        self.assertNotEqual(a['metrics']['spend'], b['metrics']['spend'])

    def test_verdicts(self):
        V = Engine.verdict
        m = lambda spend, roas: {'spend': spend, 'roas': roas}
        self.assertEqual(V(m(1000, 4.0), 3.0, 500)['code'], 'scale')
        self.assertEqual(V(m(1000, 2.5), 3.0, 500)['code'], 'watch')
        self.assertEqual(V(m(1000, 1.0), 3.0, 500)['code'], 'cut')
        self.assertEqual(V(m(100, 1.0), 3.0, 500)['code'], 'not_enough_data')
        self.assertEqual(V(m(700, None), 3.0, 500)['code'], 'watch')
        self.assertEqual(V(m(1000, None), 3.0, 500)['code'], 'cut')
        self.assertEqual(V(m(1000, 4.0), None, None)['code'], 'no_target')

    def test_saved_targets_override_average(self):
        v = engine().view('2026-03-02', '2026-03-31', targets={'roas': 10.0, 'cpa': None})
        self.assertEqual(v['targets']['roas'], 10.0)
        self.assertEqual(v['targets']['roas_source'], 'saved')
        self.assertEqual(v['ads']['100100']['view']['verdict']['code'], 'cut')

    def test_fatigue(self):
        cap = synthetic_capture()
        # ad 100101: strong for 60 days, then CTR and ROAS fall in the last 7 days
        cap['daily'] = [r for r in cap['daily'] if r['id'] != '100101']
        for d in range(0, 90):
            late = d >= 83
            cap['daily'].append(day(101, d, 800, 1, 800 if late else 4000, impr=10000, clicks=100 if late else 300))
        e = Engine(build(cap))
        f = e.fatigue('100101', e.idx('2026-03-31'))
        self.assertEqual(f['code'], 'declining')
        self.assertEqual(e.fatigue('100100', e.idx('2026-03-31'))['code'], 'stable')
        self.assertEqual(e.fatigue('100000', e.idx('2026-02-15'))['code'], 'not_running')

    def test_breakdowns_by_month_and_separate(self):
        e = engine()
        v = e.view('2026-02-20', '2026-03-20')
        self.assertEqual(v['demographics_buckets'], [['2026-02-01', '2026-02-28'], ['2026-03-01', '2026-03-31']])
        self.assertFalse(v['demographics_exact'])
        age = v['ads']['100100']['view']['demographics']['age']
        self.assertEqual(age['25-34']['spend'], 120.0)  # two whole months, not the daily total
        self.assertIsNone(age['35-44']['roas'])
        exact = e.view('2026-03-01', '2026-03-31')
        self.assertTrue(exact['demographics_exact'])
        self.assertEqual(exact['demographics_all']['gender']['female']['spend'], 200.0)
        det = e.ad_detail('100100', '2026-03-01', '2026-03-31')
        self.assertEqual(det['detail']['breakdowns']['gender']['female']['spend'], 100.0)
        self.assertAlmostEqual(det['detail']['metrics']['spend'], 900 * 31)

    def test_ad_detail_series(self):
        det = engine().ad_detail('100100', '2026-03-10', '2026-03-20')['detail']
        self.assertEqual(len(det['daily']), 11 + 6)  # 6 lead-in days for the rolling line
        self.assertEqual(sum(1 for d in det['daily'] if d['in_range']), 11)


class SettingsTests(unittest.TestCase):
    def test_validate_cleans_input(self):
        s = settings_mod.validate({'targets': {'roas': '3.5', 'cpa': ''}, 'evil': 1,
                                   'presets': [{'name': ' No sale ', 'keywords': ['SALE', ''], 'campaign_ids': ['123456', 'x']}],
                                   'branding': {'agency': 'A\nB', 'client': 'C' * 200}})
        self.assertEqual(s['targets'], {'roas': 3.5, 'cpa': None})
        self.assertNotIn('evil', s)
        self.assertEqual(s['presets'][0], {'name': 'No sale', 'keywords': ['sale'], 'campaign_ids': ['123456']})
        self.assertEqual(s['branding']['agency'], 'A B')
        self.assertEqual(len(s['branding']['client']), 80)
        with self.assertRaises(ValueError):
            settings_mod.validate({'targets': {'roas': -1}})


class ThemeTests(unittest.TestCase):
    def ad(self, name='', camp='', head='', body='', typ='static_image'):
        return {'name': name, 'campaign_name': camp, 'creative': {'type': typ, 'headline': head, 'primary_text': body}}

    def test_angle_product_hook(self):
        t = tag(self.ad('Social proof - earrings', 'BL - TOF', body='Why do 8,500+ customers love us?'))
        self.assertEqual(t['angle']['code'], 'social_proof')
        self.assertEqual(t['product']['code'], 'earrings')
        self.assertEqual(t['hook']['code'], 'question')
        self.assertTrue(t['angle']['why'])

    def test_whole_words_only(self):
        # "Catalogue Sales" must not count as a sale, and "ring" must not match inside "string"
        t = tag(self.ad('All Products - Catalogue Sales', 'Conversions', typ='catalog_dynamic'))
        self.assertEqual(t['angle']['code'], 'catalog')
        self.assertEqual(t['product']['code'], 'mixed')
        self.assertEqual(tag(self.ad('Stringent quality'))['product']['code'], 'mixed')
        self.assertEqual(tag(self.ad('EOSS sale countdown'))['angle']['code'], 'offer')

    def test_no_text(self):
        t = tag(self.ad('Ad 1'))
        self.assertEqual(t['hook']['code'], 'none')
        self.assertEqual(t['angle']['code'], 'showcase')

    def test_every_ad_is_tagged_in_the_cache(self):
        snap = build(synthetic_capture())
        self.assertTrue(all('tags' in ad for ad in snap['ads'].values()))


class VideoTests(unittest.TestCase):
    def test_video_rows(self):
        cap = synthetic_capture()
        base = {'id': '100100', 'amount_spent': {'value': '100'}, 'impressions': '1000', 'video_play_actions': '400',
                'video_thruplay_watched_actions': '50', 'video_p25_watched_actions': '200', 'video_p50_watched_actions': '120',
                'video_p75_watched_actions': '80', 'video_p100_watched_actions': '40', 'video_avg_time_watched_actions': '3'}
        cap['video_daily'] = [dict(base, date_start=iso(80), date_stop=iso(80), cost_per_video_view='0.5'),
                              dict(base, date_start=iso(81), date_stop=iso(81), cost_per_video_view=None),
                              dict(base, date_start=iso(81), date_stop=iso(81), cost_per_video_view='9')]  # duplicate day ignored
        rows = build(cap)['video']['100100']
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0][3], 200.0)   # 3s plays = spend / cost per 3s play
        self.assertEqual(rows[1][3], 0.0)     # no cost per play means no plays, not missing spend
        self.assertEqual(rows[0][9], 1200.0)  # watch seconds = avg x starts
        self.assertEqual(rows[0][10], 400.0)


class ShareTests(unittest.TestCase):
    def test_page_data_strips_cdn_links(self):
        cache = build(synthetic_capture())
        for ad in cache['ads'].values():
            ad['creative']['display_image_url'] = 'https://scontent.xx.fbcdn.net/x.jpg?token=abc'
            for card in ad['creative'].get('cards') or []:
                card['image_url'] = 'https://scontent.xx.fbcdn.net/c.jpg'
        out = json.dumps(page_data(cache))
        self.assertNotIn('fbcdn', out)
        self.assertIn('fbcdn', json.dumps(cache))  # the original is untouched


class NotesTests(unittest.TestCase):
    def test_validate_notes(self):
        n = settings_mod.validate_notes({'123456': [{'text': ' Hi\n there ', 'by': 'K' * 90, 'date': '2026-09-23', 'x': 1}], '654321': []})
        self.assertEqual(n, {'123456': [{'text': 'Hi  there', 'by': 'K' * 40, 'date': '2026-09-23'}]})
        for bad in ([], {'abc': []}, {'123456': [{'text': '', 'date': '2026-09-23'}]}, {'123456': [{'text': 'a', 'date': 'soon'}]}):
            with self.assertRaises(ValueError):
                settings_mod.validate_notes(bad)


class AITests(unittest.TestCase):
    def setUp(self):
        from meta_gallery import ai
        self.ai = ai
        self.tmp = tempfile.TemporaryDirectory()
        self.env = Path(self.tmp.name) / '.env'

    def tearDown(self):
        self.tmp.cleanup()

    def test_status_without_keys(self):
        self.env.write_text('OTHER=1\n', encoding='utf-8')
        st = self.ai.status(self.env)
        self.assertFalse(st['breakdown'])
        self.assertFalse(st['variants'])
        self.assertNotIn('key', json.dumps(st).lower().replace('keys', ''))

    def test_status_never_returns_keys(self):
        self.env.write_text('OPENAI_API_KEY=sk-test-SECRET-123456789\nANTHROPIC_API_KEY=sk-ant-SECRET-987654321\n', encoding='utf-8')
        st = self.ai.status(self.env)
        self.assertTrue(st['breakdown'] and st['variants'])
        self.assertEqual(st['breakdown_provider'], 'claude')
        self.assertNotIn('SECRET', json.dumps(st))

    def test_clean_breakdown_bounds_and_defaults(self):
        b = self.ai.clean_breakdown({'verdict': 'great', 'summary': 'x' * 900, 'why': ['plain', {'point': 'p', 'evidence': 'e'}, 5],
                                     'structure': {'hook': 'h', 'evil': 'y'}, 'keep': list('abcdefghij'), 'extra': 1})
        self.assertEqual(b['verdict'], 'mixed')
        self.assertEqual(len(b['summary']), 400)
        self.assertEqual(b['why'][0], {'point': 'plain', 'evidence': ''})
        self.assertNotIn('evil', b['structure'])
        self.assertEqual(len(b['keep']), 8)
        self.assertNotIn('extra', b)

    def test_json_from_fenced_reply(self):
        self.assertEqual(self.ai._json_from('Here:\n```json\n{"summary": "ok"}\n```'), {'summary': 'ok'})

    def test_errors_scrub_keys(self):
        cfg = {'openai_key': 'sk-live-ABCDEFGHIJKLMNOP', 'anthropic_key': ''}
        self.assertNotIn('ABCDEFGH', self.ai._scrub('bad key sk-live-ABCDEFGHIJKLMNOP given', cfg))

    def test_make_variants_saves_files(self):
        import base64
        self.env.write_text('OPENAI_API_KEY=sk-test-123456789012345\n', encoding='utf-8')
        calls = []
        png = base64.b64encode(b'\x89PNG\r\n\x1a\nfake').decode()
        def fake_post(url, headers, body, cfg, timeout=240):
            calls.append((url, body))
            self.assertIn(b'name="image[]"', body)
            self.assertIn(b'name="model"', body)
            return {'data': [{'b64_json': png}]}
        orig = self.ai._post
        self.ai._post = fake_post
        try:
            out = self.ai.make_variants('120244547906610138', {'headline': 'Gold studs'}, b'jpgbytes', {'keep': ['warm light']}, n=2,
                                        env_path=self.env, out_dir=Path(self.tmp.name) / 'v', plan=False)
        finally:
            self.ai._post = orig
        self.assertEqual(len(calls), 2)
        self.assertTrue(all('file' in m for m in out))
        listed = self.ai.list_variants('120244547906610138', out_dir=Path(self.tmp.name) / 'v')
        self.assertEqual(len(listed), 2)
        self.assertIsNone(self.ai.variant_path('120244547906610138', '../.env', out_dir=Path(self.tmp.name) / 'v'))
        self.assertIsNone(self.ai.variant_path('../../x', 'a.png', out_dir=Path(self.tmp.name) / 'v'))

    def test_concepts_one_close_rest_new(self):
        cfg = {'anthropic_key': '', 'openai_key': 'sk-test-123456789012345', 'AI_OPENAI_TEXT_MODEL': 'm', 'AI_TEXT_MODEL': 'm'}
        orig = self.ai._ask
        self.ai._ask = lambda *a, **k: (json.dumps({'concepts': [
            {'name': 'A', 'closeness': 'new', 'idea': 'same ad, new light'},
            {'name': 'B', 'closeness': 'new', 'principle': 'price clarity', 'idea': 'flat lay with price'},
            {'name': 'C', 'closeness': 'new', 'idea': 'worn at a wedding'}]}), 'm', 'openai')
        try:
            out = self.ai.plan_concepts(cfg, {}, {}, 3, b'x', 'image/jpeg')
        finally:
            self.ai._ask = orig
        self.assertEqual([c['closeness'] for c in out], ['close', 'new', 'new'])
        p = self.ai.concept_prompt({}, {'keep': ['warm light']}, out[1])
        self.assertIn('NEW ad', p)
        self.assertIn('price clarity', p)
        self.ai._ask = lambda *a, **k: ('no json here', 'm', 'openai')
        try:
            fb = self.ai.plan_concepts(cfg, {}, {}, 2, b'x', 'image/jpeg')
        finally:
            self.ai._ask = orig
        self.assertEqual(len(fb), 2)

    def test_fallback_model_when_first_is_unavailable(self):
        self.env.write_text('OPENAI_API_KEY=sk-test-123456789012345\nAI_IMAGE_MODEL=new-model\n', encoding='utf-8')
        seen = []
        def fake_post(url, headers, body, cfg, timeout=240):
            model = body.split(b'name="model"\r\n\r\n')[1].split(b'\r\n')[0].decode()
            seen.append(model)
            if model == 'new-model':
                raise self.ai.AIError('404: The model new-model does not exist')
            return {'data': [{'b64_json': 'aGk='}]}
        orig = self.ai._post
        self.ai._post = fake_post
        try:
            cfg = self.ai.settings(self.env)
            data, model = self.ai.make_variant(cfg, 'p', b'x', '1024x1024', 'low')
        finally:
            self.ai._post = orig
        self.assertEqual(model, 'gpt-image-2')
        self.assertEqual(seen, ['new-model', 'gpt-image-2'])

    def test_competitor_reference_goes_to_both_models(self):
        import base64
        self.env.write_text('OPENAI_API_KEY=sk-test-123456789012345\n', encoding='utf-8')
        png = base64.b64encode(b'\x89PNG\r\n\x1a\nfake').decode()
        text_bodies, image_bodies = [], []
        plan = json.dumps({'concepts': [{'name': 'Flat lay', 'idea': 'product on linen, same framing'}]})
        def fake_post(url, headers, body, cfg, timeout=240):
            if 'responses' in url:
                text_bodies.append(json.loads(body))
                return {'output_text': plan}
            image_bodies.append(body)
            return {'data': [{'b64_json': png}]}
        orig = self.ai._post
        self.ai._post = fake_post
        try:
            out = self.ai.make_competitor_variants('120244547906610138', {'brand': 'X', 'headline': 'h', 'ad_id': '123456'}, {'headline': 'Gold'},
                                                   b'ownjpg', {}, n=1, env_path=self.env, out_dir=Path(self.tmp.name) / 'cv', ref_bytes=b'refjpg')
        finally:
            self.ai._post = orig
        imgs = [c for c in text_bodies[0]['input'][0]['content'] if c['type'] == 'input_image']
        self.assertEqual(len(imgs), 2)
        self.assertIn('Image 2 is the competitor ad', text_bodies[0]['input'][0]['content'][0]['text'])
        self.assertEqual(image_bodies[0].count(b'name="image[]"'), 2)
        self.assertIn(b'refjpg', image_bodies[0])
        self.assertIn(b'Never copy its text, logo', image_bodies[0])
        self.assertEqual(out[0]['comp_ad_id'], '123456')


class ServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from http.server import ThreadingHTTPServer
        cls.tmp = tempfile.TemporaryDirectory()
        path = Path(cls.tmp.name) / 'gallery.json'
        path.write_text(json.dumps(build(synthetic_capture())), encoding='utf-8')
        cls.gallery = Gallery(path, settings_path=Path(cls.tmp.name) / 'settings.json', notes_path=Path(cls.tmp.name) / 'notes.json')
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), make_handler(cls.gallery))
        cls.base = f'http://127.0.0.1:{cls.server.server_address[1]}'
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.tmp.cleanup()

    def get(self, path):
        return json.load(urllib.request.urlopen(self.base + path))

    def post(self, path, body, headers=None):
        req = urllib.request.Request(self.base + path, data=json.dumps(body).encode(), method='POST',
                                     headers=headers or {'Content-Type': 'application/json'})
        return urllib.request.urlopen(req)

    def test_view_endpoint(self):
        v = self.get('/api/view?since=2026-03-02&until=2026-03-31&kw=sale')
        self.assertEqual(v['exclusions']['ads'], 1)
        self.assertNotIn('breakdowns', v['ads']['100100']['view'])
        d = self.get('/api/ad/100100?since=2026-03-02&until=2026-03-31')
        self.assertIn('breakdowns', d['detail'])

    def test_bad_range_is_400(self):
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(self.base + '/api/view?since=2026-03-10&until=2026-03-01')
        self.assertEqual(ctx.exception.code, 400)

    def test_meta_lists_campaigns(self):
        m = self.get('/api/meta')
        self.assertEqual({c['id'] for c in m['campaigns']}, {'900', '901'})

    def test_settings_roundtrip_changes_verdicts(self):
        out = json.load(self.post('/api/settings', {'targets': {'roas': 50}, 'presets': [], 'branding': {}}))
        self.assertEqual(out['targets']['roas'], 50.0)
        v = self.get('/api/view?since=2026-03-02&until=2026-03-31')
        self.assertEqual(v['targets']['roas'], 50.0)
        self.post('/api/settings', {'targets': {}, 'presets': [], 'branding': {}})

    def test_settings_rejects_other_origins_and_non_json(self):
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            self.post('/api/settings', {}, {'Content-Type': 'application/json', 'Origin': 'https://evil.example'})
        self.assertEqual(ctx.exception.code, 403)
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            self.post('/api/settings', {}, {'Content-Type': 'text/plain'})
        self.assertEqual(ctx.exception.code, 415)

    def test_other_writes_rejected(self):
        for method in ('POST', 'PUT', 'DELETE'):
            req = urllib.request.Request(self.base + '/api/view', data=b'{}', method=method)
            with self.assertRaises(urllib.error.HTTPError) as ctx:
                urllib.request.urlopen(req)
            self.assertEqual(ctx.exception.code, 405)

    def test_web_page_and_data(self):
        html = urllib.request.urlopen(self.base + '/').read().decode()
        self.assertTrue(html.startswith('<!doctype html>'))
        self.assertIn('tab-insights', html)
        self.assertIn('tab-overview', html)
        for f in ('engine.js', 'app.js', 'insights.js', 'overview.js', 'lab.js', 'studio.js'):
            self.assertEqual(urllib.request.urlopen(self.base + '/' + f).status, 200)
        d = self.get('/data.json')
        self.assertIn('100100', d['ads'])
        self.assertNotIn('display_image_url', json.dumps(d))
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(self.base + '/thumbs.json')
        self.assertEqual(ctx.exception.code, 404)
        self.assertEqual(self.get('/notes.json'), {})

    def test_save_endpoints(self):
        out = json.load(self.post('/api/save/settings.json', {'targets': {'roas': 4}, 'presets': [], 'branding': {}}))
        self.assertEqual(out['targets']['roas'], 4.0)
        self.assertEqual(self.get('/settings.json')['targets']['roas'], 4.0)
        self.post('/api/save/settings.json', {'targets': {}, 'presets': [], 'branding': {}})
        notes = {'100100': [{'text': 'New hook', 'by': 'Kevin', 'date': '2026-09-23'}]}
        self.assertEqual(json.load(self.post('/api/save/notes.json', notes)), notes)
        self.assertEqual(self.get('/notes.json'), notes)
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            self.post('/api/save/notes.json', {'bad id': []})
        self.assertEqual(ctx.exception.code, 400)
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            self.post('/api/save/notes.json', notes, {'Content-Type': 'application/json', 'Origin': 'https://evil.example'})
        self.assertEqual(ctx.exception.code, 403)
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            self.post('/api/save/data.json', {})
        self.assertEqual(ctx.exception.code, 405)
        self.post('/api/save/notes.json', {})

    def test_ai_routes(self):
        from meta_gallery import ai
        st = self.get('/api-status'.replace('-', '/ai-', 1))
        self.assertIn('variants', st)
        self.assertIsInstance(self.get('/breakdowns.json'), dict)
        self.assertEqual(self.get('/api/variants/100100'), [])
        for bad in ('/variants/100100/..%2F.env', '/variants/abc/a.png'):
            with self.assertRaises(urllib.error.HTTPError) as ctx:
                urllib.request.urlopen(self.base + bad)
            self.assertEqual(ctx.exception.code, 404)
        orig = ai.breakdown
        ai.breakdown = lambda facts, data, kind: {'summary': 'Clear hook', 'why': ['bright gold'], 'provider': 'claude', 'model': 'm'}
        tmp_bd = Path(self.tmp.name) / 'bd.json'
        orig_path = ai.BREAKDOWNS
        ai.BREAKDOWNS = tmp_bd
        try:
            out = json.load(self.post('/api/breakdown', {'ad_id': '100100', 'facts': {'x': 1}}))
            self.assertEqual(out['summary'], 'Clear hook')
            self.assertEqual(self.get('/breakdowns.json')['100100']['why'][0]['point'], 'bright gold')
            with self.assertRaises(urllib.error.HTTPError) as ctx:
                self.post('/api/breakdown', {'ad_id': '100100'}, {'Content-Type': 'application/json', 'Origin': 'https://evil.example'})
            self.assertEqual(ctx.exception.code, 403)
        finally:
            ai.breakdown = orig
            ai.BREAKDOWNS = orig_path

    def test_pasted_reference_goes_to_variants(self):
        import base64
        from meta_gallery import ai, server
        jpg = b'\xff\xd8\xff\xe0' + b'x' * 50
        self.assertEqual(server.pasted_image('data:image/jpeg;base64,' + base64.b64encode(jpg).decode()), jpg)
        self.assertIsNone(server.pasted_image(None))
        with self.assertRaises(ValueError):
            server.pasted_image(base64.b64encode(b'not an image').decode())
        seen = {}
        orig_mv, orig_img = ai.make_variants, server.image_bytes
        ai.make_variants = lambda *a, **k: seen.update(k) or []
        server.image_bytes = lambda ad: (b'\xff\xd8\xffown', 'image/jpeg')
        try:
            self.post('/api/variants', {'ad_id': '100100', 'n': 2, 'ref_image': base64.b64encode(jpg).decode()})
            self.assertEqual(seen['ref_bytes'], jpg)
            self.assertEqual(seen['ref_role'], 'layout')
            self.post('/api/variants', {'ad_id': '100100', 'ref_image': base64.b64encode(jpg).decode(), 'ref_role': 'product'})
            self.assertEqual(seen['ref_role'], 'product')
            self.assertIn('Image 2 is a Gehna product photo', ai.plan_prompt({}, {}, 2, True, 'product'))
            with self.assertRaises(urllib.error.HTTPError) as ctx:
                self.post('/api/variants', {'ad_id': '100100', 'ref_image': base64.b64encode(b'<svg>').decode()})
            self.assertEqual(ctx.exception.code, 400)
        finally:
            ai.make_variants, server.image_bytes = orig_mv, orig_img

    def test_no_secrets_in_ui_assets(self):
        root = Path(__file__).resolve().parent.parent / 'meta_gallery'
        for f in list((root / 'static').iterdir()) + list((root / 'web').iterdir()):
            text = f.read_text(encoding='utf-8')
            self.assertNotIn('access_token', text)
            self.assertNotIn('META_ACCESS_TOKEN', text)
            self.assertNotIn('graph.facebook.com', text)


class GraphTests(unittest.TestCase):
    def test_token_scrubbed(self):
        g = Graph('SECRET123', '42')
        self.assertEqual(g.scrub('bad SECRET123 here'), 'bad <token> here')
        self.assertEqual(g.account, 'act_42')

    def test_env_parser_ignores_malformed_lines(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / '.env'
            p.write_text('META_AD_ACCOUNT_ID=act_1\nstray-value-without-key\n# comment\n', encoding='utf-8')
            self.assertEqual(load_env(p), {'META_AD_ACCOUNT_ID': 'act_1'})

    def test_graph_row_mapping(self):
        r = to_row({'ad_id': '1', 'spend': '10', 'impressions': '100',
                    'actions': [{'action_type': 'omni_purchase', 'value': '2'}, {'action_type': 'link_click', 'value': '5'}],
                    'action_values': [{'action_type': 'omni_purchase', 'value': '50'}]})
        self.assertEqual((r['omni_purchase'], r['link_click'], r['omni_purchase_values']['value']), ('2', '5', '50'))
        empty = to_row({'ad_id': '2', 'spend': '10', 'impressions': '100'})
        self.assertIsNone(empty['omni_purchase'])
        self.assertIsNone(empty['omni_purchase_values'])


if __name__ == '__main__':
    unittest.main()
