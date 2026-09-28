"""Tests for screen 10-copy on the Bombas brain: the claim checker and QA gate, the voice rules,
message match, the language bank, the copy set stub, audit.py in the contract shape, and the api.
Live-ad tests use a fake metric; the Bombas data.sqlite tests skip when it has not been built."""
import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / 'app' / 'screens' / '10-copy'
BOMBAS_DB = ROOT / 'app' / 'data' / 'brands' / 'bombas' / 'data.sqlite'
DAY = '2026-09-28'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


api = load('copy_api_t', SCREEN / 'api.py')
audit = api.audit
lib = api.copylib

FIELDS = ['id', 'screen', 'rule_id', 'severity', 'entity', 'evidence', 'sentence', 'capability', 'money_at_stake',
          'confidence', 'brain_refs', 'first_seen', 'last_seen', 'status', 'unavailable']
EVIDENCE = {'metric', 'value', 'unit', 'window', 'ends_on', 'freshness_days', 'baseline', 'baseline_kind', 'source', 'simulated'}


class FakeData:
    """Data.metric stand-in: one live ad per copy set (MA-00010 runs AC-01 ... MA-00019 runs AC-10), plus 1 ended ad."""

    def __init__(self, unavailable=False):
        self.unavailable = unavailable

    def metric(self, name, **kw):
        if self.unavailable:
            return {'value': None, 'unavailable': True, 'reason': 'ad_rows is missing', 'fix': 'Meta Ads'}
        groups = [{'ad': f'MA-{10 + i:05d}', 'spend': 100.0 + i, 'impressions': 1000, 'purchases': 3,
                   'campaign_name': 'Prospecting | Broad', 'format': 'image', 'last_day': '2026-09-27'} for i in range(10)]
        groups.append({'ad': 'MA-00020', 'spend': 50.0, 'last_day': '2026-09-24', 'format': 'image'})
        return {'value': sum(g['spend'] for g in groups), 'unavailable': False,
                'window': {'start': '2026-09-21', 'end': '2026-09-27', 'days': 7}, 'groups': groups}


class Req:
    def __init__(self, path, method='GET', query=None, body=None, data=None):
        self.method, self.path, self.body, self.data = method, path, body, data or FakeData()
        self.query = dict({'today': [DAY]}, **(query or {}))

    def arg(self, name, default=None):
        v = self.query.get(name)
        return v[0] if v else default


class ClaimChecker(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.brain = lib.brain_for('bombas')

    def check(self, text):
        return lib.check_text(text, self.brain)

    def test_site_backed_claim_is_allowed(self):
        s = self.check('One purchased = one donated.')['sentences'][0]
        self.assertEqual(s['verdict'], 'allowed')
        self.assertEqual(s['matches'][0]['id'], 'bombas.claims.donation_pledge')
        self.assertIn(s['matches'][0]['tier'], ('approved', 'site_backed'))

    def test_evidence_tier_offer_is_flagged(self):
        s = self.check('Use code COMFORT20 for 20% off.')['sentences'][0]
        self.assertEqual(s['verdict'], 'flagged')
        self.assertEqual(s['matches'][0]['tier'], 'evidence')

    def test_risk_patterns_flag(self):
        res = self.check('The softest socks in the world. Podiatrist recommended. Better than Stance.')
        self.assertEqual(res['flagged'], 3)
        self.assertEqual([s['risks'][0]['id'] for s in res['sentences']], ['superlative', 'health', 'competitor'])

    def test_claim_like_with_no_record_is_flagged(self):
        s = self.check('Free returns for life.')['sentences'][0]
        self.assertEqual(s['verdict'], 'flagged')
        self.assertIn('no claim record', s['reasons'][0])

    def test_plain_line_is_not_a_claim(self):
        self.assertEqual(self.check('Holes in your socks?')['sentences'][0]['verdict'], 'not_a_claim')

    def test_reddit_quote_as_testimonial_is_never_testimonial(self):
        res = self.check('“They’re very comfortable.” says a shopper.')
        self.assertTrue(res['never_testimonial'])
        self.assertTrue(res['sentences'][0]['testimonial']['reddit'])
        self.assertEqual(res['sentences'][0]['verdict'], 'flagged')

    def test_gate_follows_the_brain_tier(self):
        """Tier is read from the brain at run time: a record that drops out of the brain flags the line."""
        r = lib.rules()
        r['claim_patterns'][0] = dict(r['claim_patterns'][0], ref='bombas.claims.no_such_record')
        s = lib.check_text('One purchased = one donated.', self.brain, r)['sentences'][0]
        self.assertEqual(s['verdict'], 'flagged')
        self.assertEqual(s['matches'][0]['tier'], 'missing')


class Voice(unittest.TestCase):
    def test_breaks(self):
        r = lib.rules()
        v = lib.voice_check('Elevate your day — with revolutionary socks that seamlessly unlock unparalleled '
                            'comfort for the modern individual who demands excellence in every single step.', r)
        self.assertEqual(v['em_dashes'], 1)
        self.assertIn('elevate', v['inflated'])
        self.assertEqual(len(v['long_sentences']), 1)
        self.assertGreater(v['grade'], 10)
        self.assertFalse(v['pass'])

    def test_plain_copy_passes(self):
        v = lib.voice_check('Calf socks that stay up all day. A soft heel and a snug fit.', lib.rules())
        self.assertTrue(v['pass'])


class MessageMatchAndBank(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.brain = lib.brain_for('bombas')
        cls.sets = {s['id']: s for s in lib.copy_sets()}

    def mm(self, sid):
        return lib.message_match(self.sets[sid], self.brain, lib.rules(), lib.bank_index(self.brain))

    def test_offer_missing_from_page(self):
        m = self.mm('AC-02')
        self.assertEqual(m['score'], 0)
        self.assertIn('bombas.offers.first_order_code', [g['ref'] for g in m['gaps']])

    def test_full_match(self):
        self.assertEqual(self.mm('AC-08')['score'], 100)

    def test_no_items_is_null_not_zero(self):
        self.assertIsNone(self.mm('AC-09')['score'])

    def test_language_rows(self):
        rows = lib.language_rows(self.brain)
        self.assertEqual(len(rows), len(self.brain.records('language_bank')))
        reddit = [r for r in rows if r['never_testimonial']]
        self.assertTrue(reddit)
        self.assertTrue(all(not r['copy_ready'] for r in reddit))
        self.assertTrue(all(r['link'] is None or r['link'].startswith('http') for r in rows))

    def test_stub_applies_gate(self):
        for f in lib.copy_set_stub(self.brain):
            for line in f['headlines'] + f['primary']:
                self.assertTrue(line['pass'])
                self.assertLessEqual(line['chars'], line['limit'])
                self.assertTrue(all(t in ('approved', 'site_backed') for t in line['tiers'].values()))
            self.assertTrue(any('COMFORT20' in b['text'] or '20%' in b['text'] for b in f['blocked']))


class Audit(unittest.TestCase):
    def test_contract_shape_and_rules(self):
        findings = audit.run('bombas', {'ends_on': '2026-09-27'}, data=FakeData())
        self.assertTrue(findings)
        for f in findings:
            self.assertEqual(list(f)[:len(FIELDS)], FIELDS)
            self.assertEqual(f['id'], f"10-copy.{f['rule_id']}.{f['entity']['id']}")
            self.assertIn(f['severity'], ('critical', 'high', 'medium', 'low'))
            for row in f['evidence']:
                self.assertEqual(set(row), EVIDENCE)
            self.assertIsNone(f['money_at_stake'])
            self.assertTrue(f['money_reason'])
            self.assertLessEqual(len(f['sentence'].split()), 40, f['sentence'])
            self.assertNotIn('—', f['sentence'])
        ids = {f['id'] for f in findings}
        self.assertIn('10-copy.COPY-R01.AC-03', ids)
        self.assertIn('10-copy.COPY-R01.AC-04', ids)
        self.assertIn('10-copy.COPY-R02.AC-02', ids)
        self.assertIn('10-copy.COPY-R03.AC-09', ids)
        self.assertNotIn('10-copy.COPY-R01.AC-08', ids)
        sev = [audit.SEVERITY_ORDER[f['severity']] for f in findings]
        self.assertEqual(sev, sorted(sev))

    def test_deterministic(self):
        a = audit.run('bombas', {'ends_on': '2026-09-27'}, data=FakeData())
        b = audit.run('bombas', {'ends_on': '2026-09-27'}, data=FakeData())
        self.assertEqual(json.dumps(a), json.dumps(b))

    def test_unavailable_when_ad_table_missing(self):
        findings = audit.run('bombas', {'ends_on': '2026-09-27'}, data=FakeData(unavailable=True))
        self.assertEqual(len(findings), len(audit.RULES))
        for f in findings:
            self.assertEqual(f['status'], 'unavailable')
            self.assertEqual(f['evidence'], [])
            self.assertEqual(f['unavailable']['inputs'], ['ad_rows'])

    def test_rules_list(self):
        self.assertEqual([r['rule_id'] for r in audit.RULES], ['COPY-R01', 'COPY-R02', 'COPY-R03'])


class Api(unittest.TestCase):
    def test_overview(self):
        d = api.handle(Req(['overview']))
        self.assertEqual(len(d['tiles']), 3)
        self.assertEqual(d['tiles'][0]['value'], 5)  # AC-02, 03, 04, 06, 07 flagged, 1 live ad each
        self.assertEqual({i['capability'] for i in d['insights']}, {'LOOP-C12', 'CREA-C26'})
        self.assertIn('simulated', d['simulated_note'])
        self.assertEqual(d['inventory']['live_ads'], 10)
        self.assertEqual(sum(sum(s['values']) for s in d['chart']['series']), d['chart']['total'])
        self.assertEqual(len(d['stub']), 3)

    def test_overview_unavailable_is_not_zero(self):
        d = api.handle(Req(['overview'], data=FakeData(unavailable=True)))
        self.assertTrue(all(t['value'] is None for t in d['tiles']))
        self.assertEqual(d['insights'], [])
        self.assertTrue(all(c['live_ads'] is None for c in d['copy']))

    def test_check_and_errors(self):
        res = api.handle(Req(['check'], 'POST', body={'text': 'Lifetime guarantee on every pair.'}))
        self.assertEqual(res['flagged'], 1)
        self.assertEqual(api.handle(Req(['check'], 'POST', body={'text': ' '}))[0], 400)
        self.assertEqual(api.handle(Req(['overview'], query={'brand': ['../x']}))[0], 400)
        self.assertEqual(api.handle(Req(['nope']))[0], 404)

    def test_language_filters(self):
        d = api.handle(Req(['language'], query={'star': ['5']}))
        self.assertTrue(d['rows'] and all(5 in r['stars'] for r in d['rows']))
        d = api.handle(Req(['language'], query={'star': ['none'], 'theme': ['praise']}))
        self.assertTrue(all(not r['stars'] and r['theme'] == 'praise' for r in d['rows']))
        self.assertEqual(api.handle(Req(['language'], query={'star': ['x']}))[0], 400)


@unittest.skipUnless(BOMBAS_DB.is_file(), 'bombas data.sqlite not built')
class BombasLive(unittest.TestCase):
    def test_audit_on_ad_table(self):
        server = load('copy_server_t', ROOT / 'app' / 'server.py')
        findings = audit.run('bombas', {'ends_on': '2026-09-27'}, data=server.Data())
        self.assertTrue(findings)
        self.assertTrue(all(f['status'] == 'open' for f in findings))
        self.assertTrue(any(f['rule_id'] == 'COPY-R01' for f in findings))


if __name__ == '__main__':
    unittest.main()
