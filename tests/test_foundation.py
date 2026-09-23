import copy
import tempfile
import unittest
from intelligence.store import Store
from intelligence.context import pack
from intelligence.costs import estimate, token_cost


class FoundationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.store = Store(self.temp.name)
        self.raw = b'Synthetic example: test one landing page variable at a time.'
        self.version = self.store.ingest('synthetic', 'global', self.raw, 'example.txt')['version_id']
        self.passage = self.store.passages(self.version)[0]
        self.card = dict(id='synthetic-card-v1', scope='global', title='Landing page test',
                         claim='Isolate the tested variable.', action='Test one variable.', modules=['CRO'],
                         applies_when={'measurement_ready': True}, do_not_use_when={'tracking_broken': True},
                         unknowns=['No performance lift is established.'],
                         evidence=[dict(passage_id=self.passage['id'], quote='test one landing page variable at a time')],
                         review_due='2099-01-01', dependencies=[])

    def tearDown(self):
        self.store.close()
        self.temp.cleanup()

    def publish(self):
        self.store.review_source(self.version, 'test reviewer', True)
        self.store.classify_origin(self.passage['id'], 'original')
        self.store.add_card(self.card)
        self.store.approve_card(self.card['id'], 'test reviewer')

    def test_idempotent_ingestion_and_no_old_version_reactivation(self):
        self.assertFalse(self.store.ingest('synthetic', 'global', self.raw, 'example.txt')['changed'])
        self.store.ingest('synthetic', 'global', self.raw + b' Updated.', 'example.txt')
        self.assertFalse(self.store.ingest('synthetic', 'global', self.raw, 'example.txt')['is_current'])

    def test_original_and_permission_required(self):
        self.store.add_card(self.card)
        with self.assertRaises(ValueError):
            self.store.approve_card(self.card['id'], 'reviewer')

    def test_exact_quote_required(self):
        self.card['evidence'][0]['quote'] = 'Guaranteed 50 percent lift'
        with self.assertRaises(ValueError):
            self.store.add_card(self.card)

    def test_version_change_removes_published_card(self):
        self.publish()
        self.assertEqual(len(self.store.eligible_cards({'global'})), 1)
        self.store.ingest('synthetic', 'global', self.raw + b' Updated.', 'example.txt')
        self.assertEqual(self.store.eligible_cards({'global'}), [])

    def test_revocation_removes_card(self):
        self.publish()
        self.store.review_source(self.version, 'reviewer', False)
        self.assertEqual(self.store.eligible_cards({'global'}), [])

    def test_generated_analysis_cannot_remain_published(self):
        self.publish()
        self.store.classify_origin(self.passage['id'], 'generated_analysis')
        self.assertEqual(self.store.eligible_cards({'global'}), [])

    def test_scope_filter(self):
        self.publish()
        self.assertEqual(self.store.eligible_cards({'brand-other'}), [])

    def test_private_evidence_cannot_support_global_card(self):
        version = self.store.ingest('private', 'brand-a', self.raw, 'example.txt')['version_id']
        self.card['evidence'][0]['passage_id'] = self.store.passages(version)[0]['id']
        with self.assertRaises(ValueError):
            self.store.add_card(self.card)

    def test_missing_conditions_abstain(self):
        self.assertEqual(pack([self.card], 'landing', {})['selected_ids'], [])

    def test_budget_never_truncates_conditions(self):
        facts = {'measurement_ready': True, 'tracking_broken': False}
        result = pack([self.card], 'landing', facts, budget=100)
        self.assertEqual(result['selected_ids'], [])
        result = pack([self.card], 'landing', facts, budget=6000)
        self.assertIn('do_not_use_when', result['context'])
        self.assertLessEqual(result['used_units'], 6000)

    def test_dependency_cycle_abstains(self):
        other = copy.deepcopy(self.card)
        other['id'] = 'other'
        other['dependencies'] = [self.card['id']]
        self.card['dependencies'] = ['other']
        result = pack([self.card, other], 'landing', {'measurement_ready': True, 'tracking_broken': False})
        self.assertEqual(result['selected_ids'], [])

    def test_costs(self):
        self.assertEqual(float(token_cost('gpt-5.6-luna', 1_000_000, 1_000_000)), 1.4)
        self.assertAlmostEqual(estimate()['subtotal_usd'], 107.676)
        self.assertAlmostEqual(estimate(batch=True)['with_reserve_usd'], 70.1623)


if __name__ == '__main__':
    unittest.main()
