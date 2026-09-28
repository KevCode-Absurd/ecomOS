"""Tests for app/rank.py (depth.md sections 4 and 5): findings to rubric-scored actions, the shape every
screen's rank route must keep, determinism, the master list split into top, connect and bottlenecks, and the
server's fallback rank route. Runs on the repo's Bombas brain and aggregates; writes nothing."""
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / 'app'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


rank = load('ecomos_rank_t', APP / 'rank.py')
WINDOW = {'ends_on': '2026-09-27', 'days': 28, 'trailing': 4}
FINDING = {'id': '11-paid-social.PAID-R03.adset_1', 'screen': '11-paid-social', 'rule_id': 'PAID-R03', 'severity': 'high',
           'entity': {'type': 'adset', 'id': '1', 'label': 'Prospecting, Comfort'}, 'evidence': [],
           'sentence': 'This ad set has shown the same 3 ads 4.6 times per person this week.',
           'capability': {'id': 'CREA-C15', 'autonomy': 'agent_does'},
           'money_at_stake': {'usd': 3118, 'formula': 'x', 'inputs': {}, 'window': '7d'}, 'confidence': 0.8,
           'brain_refs': [], 'first_seen': '2026-09-24', 'last_seen': '2026-09-27', 'status': 'open', 'unavailable': None}


class Scoring(unittest.TestCase):
    def test_rubric_from_fields(self):
        r = rank.score(FINDING, 100000)   # 3.1 percent of net revenue
        self.assertEqual(r['revenue'], 4)
        self.assertEqual(r['ease'], 5)
        self.assertEqual(r['confidence'], 4)
        self.assertEqual(set(r), {'revenue', 'profit', 'reputation', 'satisfaction', 'ease', 'confidence', 'total'})
        self.assertTrue(0 <= r['total'] <= 100)

    def test_no_money_uses_severity(self):
        f = dict(FINDING, money_at_stake=None)
        self.assertEqual(rank.score(f, 100000)['revenue'], 3)
        self.assertEqual(rank.score(dict(f, severity='critical'), None)['revenue'], 4)

    def test_unknown_confidence_is_neutral_not_zero(self):
        r = rank.score(dict(FINDING, confidence=None), None)
        self.assertIsNone(r['confidence'])
        r0 = rank.score(dict(FINDING, confidence=0.0), None)
        self.assertGreater(r['total'], r0['total'])

    def test_owner_from_autonomy_and_unavailable(self):
        self.assertEqual(rank.owner_of(FINDING), 'agent')
        self.assertEqual(rank.owner_of(dict(FINDING, capability={'id': 'LIFE-C36', 'autonomy': 'founder_gate'})), 'agent_drafts')
        self.assertEqual(rank.owner_of(dict(FINDING, capability={'id': 'X', 'autonomy': 'human_assist'})), 'person')
        self.assertEqual(rank.owner_of(dict(FINDING, status='unavailable')), 'person')


class Actions(unittest.TestCase):
    def test_action_shape(self):
        a = rank.action_from_finding(FINDING, 100000)
        self.assertEqual(rank.validate_action(a), [])
        self.assertEqual(a['finding_ids'], [FINDING['id']])
        self.assertIn(a['owner'], rank.OWNERS)
        self.assertTrue(2 <= len(a['steps']) <= 8)
        self.assertTrue(all(s['who'] in rank.OWNERS and s['text'] for s in a['steps']))
        self.assertIn(a['artefact']['kind'], rank.ARTEFACT_KINDS)
        self.assertEqual(a['check_on'], '2026-10-04')
        self.assertNotIn('—', a['title'] + a['why'])

    def test_unavailable_becomes_connect_action(self):
        f = dict(FINDING, status='unavailable', evidence=[], unavailable={'inputs': ['ad_rows'], 'connector': 'Meta', 'fix': 'Add a read-only token in Setup.'})
        a = rank.action_from_finding(f, None)
        self.assertEqual(a['owner'], 'person')
        self.assertEqual(a['artefact']['kind'], 'connector_setup')
        self.assertTrue(a['title'].startswith('Connect Meta'))
        self.assertEqual(a['steps'][0]['text'], 'Add a read-only token in Setup.')
        self.assertEqual(a['rubric']['ease'], 1)

    def test_validate_rejects_bad_actions(self):
        a = rank.action_from_finding(FINDING, None)
        self.assertTrue(rank.validate_action(dict(a, owner='robot')))
        self.assertTrue(rank.validate_action(dict(a, steps=[])))
        self.assertTrue(rank.validate_action(dict(a, artefact={})))

    def test_sort_pins_critical_then_total(self):
        low = rank.action_from_finding(dict(FINDING, id='a', severity='low', money_at_stake=None, confidence=0.3), None)
        crit = rank.action_from_finding(dict(FINDING, id='b', severity='critical', money_at_stake=None), None)
        high = rank.action_from_finding(FINDING, 100000)
        out = sorted([low, high, crit], key=rank.sort_key)
        self.assertEqual([a['id'] for a in out], ['b', FINDING['id'], 'a'])


class ScreenRank(unittest.TestCase):
    def test_every_screen_ranks_and_covers_its_findings(self):
        for slug in rank.screen_slugs():
            r = rank.rank(slug, 'bombas', WINDOW)
            findings = [f for f in rank.load_findings(slug, 'bombas', WINDOW) if f.get('status') in ('open', 'unavailable', None)]
            covered = {fid for a in r['actions'] for fid in a['finding_ids']}
            self.assertEqual({f['id'] for f in findings} - covered, set(), slug)
            for a in r['actions']:
                self.assertEqual(rank.validate_action(a), [], (slug, a['id']))
                self.assertEqual(a['screen'], slug)
            self.assertIn(r['source'], ('default', 'screen'))
            self.assertTrue(r['simulated'])

    def test_deterministic(self):
        a = rank.rank('05-brand-brain', 'bombas', WINDOW)
        b = rank.rank('05-brand-brain', 'bombas', WINDOW)
        a.pop('computed_at'); b.pop('computed_at')
        self.assertEqual(json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True))

    def test_net_revenue_from_daily_aggregate(self):
        nr = rank.net_revenue_28d('bombas', WINDOW)
        self.assertIsInstance(nr, float)
        self.assertGreater(nr, 0)
        self.assertIsNone(rank.net_revenue_28d('no-such-brand', WINDOW))


class Master(unittest.TestCase):
    def test_master_split_and_groups(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = rank.master('bombas', WINDOW, decisions_path=Path(tmp) / 'none.json')
        self.assertEqual(m['counts']['screens'], len(rank.screen_slugs()))
        self.assertTrue(all(a['status'] != 'unavailable' for a in m['top']))
        self.assertTrue(all(a['status'] == 'unavailable' for a in m['connect']))
        self.assertLessEqual(len(m['top']), 10)
        ids = [a['id'] for a in m['actions']]
        self.assertEqual(len(ids), len(set(ids)))
        totals = [a['rubric']['total'] for a in m['top'] if a['severity'] != 'critical']
        self.assertEqual(totals, sorted(totals, reverse=True))
        self.assertEqual(m['rubric_weights'], rank.WEIGHTS)
        self.assertEqual(sum(rank.WEIGHTS.values()), 100)
        g = m['bottlenecks'][0]
        self.assertEqual(set(g) >= {'screen', 'open', 'unavailable', 'critical', 'stake_usd', 'score', 'top'}, True)
        self.assertTrue(any(b['stake_usd'] is None for b in m['bottlenecks']))   # unknown stake is null, never 0

    def test_not_now_snoozes_for_14_days(self):
        m = rank.master('bombas', WINDOW, decisions_path=Path('/nonexistent.json'))
        first = m['top'][0]
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'd.json'
            p.write_text(json.dumps([{'screen': first['screen'], 'capability': first['capability']['id'], 'choice': 'not_now',
                                      'finding_id': first['id'], 'time': '2026-09-27T10:00:00Z'}]))
            import datetime as dt
            kept = rank.apply_decisions([dict(first)], today=dt.date(2026, 9, 28), path=p)
            self.assertEqual(kept, [])
            kept = rank.apply_decisions([dict(first)], today=dt.date(2026, 10, 20), path=p)
            self.assertEqual(len(kept), 1)
            self.assertEqual(kept[0]['decision']['choice'], 'not_now')


if __name__ == '__main__':
    unittest.main()
