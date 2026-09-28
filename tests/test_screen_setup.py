"""Tests for app/screens/setup/api.py: the onboarding flow, on a temp copy of the Bombas brain."""
import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API = ROOT / 'app' / 'screens' / 'setup' / 'api.py'


def load_api():
    spec = importlib.util.spec_from_file_location('setup_api_under_test', API)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


class Req:
    def __init__(self, method, path, body=None, brand='bombas'):
        self.method, self.path, self.body = method, path, body
        self.query = {'brand': [brand]} if brand else {}

    def arg(self, name, default=None):
        v = self.query.get(name)
        return v[0] if v else default


class SetupApiTest(unittest.TestCase):
    def setUp(self):
        self.api = load_api()
        self.tmp = Path(tempfile.mkdtemp())
        brain, data = self.tmp / 'brain', self.tmp / 'data'
        src = ROOT / 'app' / 'brain' / 'bombas'
        (brain / 'bombas').mkdir(parents=True)
        for f in list(src.glob('*.json')) + [src / 'BRAIN.md']:
            shutil.copy(f, brain / 'bombas' / f.name)
        (data / 'bombas').mkdir(parents=True)
        shutil.copy(ROOT / 'app' / 'data' / 'brands' / 'bombas' / 'finance_inputs.json', data / 'bombas')
        self.api.BRAIN_ROOT, self.api.DATA_ROOT = brain, data
        self.brain, self.data = brain / 'bombas', data / 'bombas'

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def call(self, method, path, body=None, brand='bombas'):
        return self.api.handle(Req(method, path, body, brand))

    def assertError(self, result, status=400):
        self.assertIsInstance(result, tuple)
        self.assertEqual(result[0], status)

    def test_state_has_every_step(self):
        s = self.call('GET', ['state'])
        self.assertTrue(s['simulated'])
        self.assertGreater(len(s['sections']['rows']), 10)
        self.assertIn('diagnosis', s['sections']['empty'])
        self.assertTrue(any(c['category'] == 'store' for c in s['categories']))
        self.assertTrue(s['finance']['fields'])

    def test_unknown_brand_and_route(self):
        self.assertError(self.call('GET', ['state'], brand='nobody'))
        self.assertError(self.call('GET', ['state'], brand='../etc'))
        self.assertError(self.call('GET', ['nope']), 404)

    def test_crawl_reads_brain_md_and_saves_website(self):
        r = self.call('POST', ['crawl'], {'url': 'https://www.bombas.com/'})
        self.assertEqual(r['url'], 'www.bombas.com')
        self.assertTrue(r['matches_brand'])
        self.assertEqual(r['records'], sum(x['records'] or 0 for x in r['sections']['rows']))
        saved = json.loads((self.brain / 'connections.json').read_text())
        self.assertEqual(saved['website']['mode'], 'mock')
        self.assertError(self.call('POST', ['crawl'], {'url': 'nothing'}))

    def test_document_writes_manifest_line(self):
        r = self.call('POST', ['documents'], {'file': 'C:\\docs\\Brand Book.pdf', 'note': 'the 2025 book',
                                              'sections': ['voice', 'bogus'], 'visibility': 'public'})
        self.assertEqual(r['file'], 'documents/Brand Book.pdf')
        rows = json.loads((self.brain / 'documents' / 'manifest.json').read_text())
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['sections'], ['voice'])
        self.assertEqual(rows[0]['visibility'], 'public')
        self.assertError(self.call('POST', ['documents'], {'file': '.env'}))
        self.assertError(self.call('POST', ['documents'], {'file': ''}))

    def test_connect_skip_declined(self):
        r = self.call('POST', ['connect'], {'category': 'store', 'choice': 'connect', 'source': 'shopify'})
        self.assertEqual(r['source'], 'shopify')
        self.call('POST', ['connect'], {'category': 'finance', 'choice': 'declined'})
        self.call('POST', ['connect'], {'category': 'reviews', 'choice': 'skip', 'source': 'judgeme'})
        saved = json.loads((self.brain / 'connections.json').read_text())['choices']
        self.assertIsNone(saved['reviews']['source'])
        self.assertError(self.call('POST', ['connect'], {'category': 'store', 'choice': 'connect', 'source': 'klaviyo'}))
        self.assertError(self.call('POST', ['connect'], {'category': 'public', 'choice': 'skip'}))
        self.assertError(self.call('POST', ['connect'], {'category': 'store', 'choice': 'maybe'}))
        a = self.call('GET', ['audit'])
        self.assertIn('shopify', a['connected'])
        self.assertIn('quickbooks', a['declined'])
        for q in a['questions']:
            self.assertNotIn('quickbooks', q['connect'])
            self.assertNotIn('q.products.hero', q['id'])  # shopify answers it

    def test_finance_row_closes_prior_and_blocks_overlap(self):
        r = self.call('POST', ['finance'], {'field': 'packaging', 'scope': 'global', 'value': '1.25',
                                            'effective_from': '2026-10-01', 'confidence': 'invoice'})
        self.assertEqual(r['unit'], 'usd_per_order')
        self.assertEqual(r['scope_key'], '')
        doc = json.loads((self.data / 'finance_inputs.json').read_text())
        same = [x for x in doc['rows'] if x['field'] == 'packaging' and not x.get('scope_key')]
        self.assertEqual(sum(1 for x in same if not x.get('effective_to')), 1)
        self.assertTrue(any(x.get('effective_to') == '2026-09-30' for x in same))
        self.assertEqual(doc['rows_count'], len(doc['rows']))
        self.assertError(self.call('POST', ['finance'], {'field': 'packaging', 'scope': 'global', 'value': 2,
                                                         'effective_from': '2026-10-01'}))
        self.assertError(self.call('POST', ['finance'], {'field': 'nope', 'value': 1, 'effective_from': '2026-10-01'}))
        self.assertError(self.call('POST', ['finance'], {'field': 'cogs_landed', 'scope': 'sku', 'value': 1,
                                                         'effective_from': '2026-10-01'}))
        self.assertError(self.call('POST', ['finance'], {'field': 'packaging', 'value': 'x', 'effective_from': '2026-10-02'}))
        self.assertError(self.call('POST', ['finance'], {'field': 'packaging', 'value': -1, 'effective_from': '2026-10-02'}))

    def test_finance_metrics_show_missing_fields(self):
        (self.data / 'finance_inputs.json').unlink()
        m = {x['metric']: x for x in self.call('GET', ['state'])['finance']['metrics']}
        self.assertFalse(m['gross_margin']['available'])
        self.assertEqual(m['gross_margin']['missing'], ['cogs_landed'])
        self.assertIn('cogs_landed', m['contribution_margin (per order, per channel, total)']['missing'])

    def test_audit_top5_and_answer_becomes_founder_record(self):
        a = self.call('GET', ['audit'])
        self.assertLessEqual(len(a['questions']), 5)
        first = a['questions'][0]
        r = self.call('POST', ['answer'], {'question_id': first['id'], 'answer': 'About 62 percent after fees.'})
        rec = r['record']
        self.assertEqual(rec['source']['type'], 'founder')
        section = rec['section']
        saved = json.loads((self.brain / f'{section}.json').read_text())
        self.assertTrue(any(x['id'] == rec['id'] for x in saved))
        after = self.call('GET', ['audit'])
        self.assertNotIn(first['id'], [q['id'] for q in after['questions']])
        self.assertError(self.call('POST', ['answer'], {'question_id': first['id'], 'answer': '  '}))
        self.assertError(self.call('POST', ['answer'], {'question_id': 'q.none', 'answer': 'x'}))

    def test_claim_answers_are_approved(self):
        r = self.call('POST', ['answer'], {'question_id': 'q.claims.approved', 'answer': 'Only the donation pledge.'})
        self.assertEqual(r['record']['tier'], 'approved')


if __name__ == '__main__':
    unittest.main()
