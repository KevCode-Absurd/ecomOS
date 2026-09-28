"""Screen 25-experiments: api shape, audit shape and determinism, rules on fed entries and on Bombas, wording."""
import importlib.util
import json
import re
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / 'app' / 'screens' / '25-experiments'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


api = load('exp_api_test', FOLDER / 'api.py')
audit = api.audit

FIELDS = ['id', 'screen', 'rule_id', 'severity', 'entity', 'evidence', 'sentence', 'capability', 'money_at_stake',
          'confidence', 'brain_refs', 'first_seen', 'last_seen', 'status', 'unavailable']
EVIDENCE = {'metric', 'value', 'unit', 'window', 'ends_on', 'freshness_days', 'baseline', 'baseline_kind', 'source',
            'simulated'}
END = date(2026, 9, 27)
_CACHE = {}


def overview():
    if 'ov' not in _CACHE:
        _CACHE['ov'] = api.overview('bombas')
    return _CACHE['ov']


class FakeReader:
    def __init__(self, entries=()):
        self.ends_on, self.brand, self._entries = END, 'bombas', list(entries)

    def m(self, name, days=28, **kw):
        return {'value': None, 'unavailable': True, 'reason': 'not fed', 'fix': 'none'}

    def record(self, rid):
        return {'id': rid, 'section': 'learnings'} if rid == 'bombas.learnings.ok' else None

    def entries(self):
        return self._entries


def entry(**kw):
    e = {'id': 'T1', 'brand': 'bombas', 'hypothesis': 'h', 'variant': {'control': 'a', 'treatment': 'b'},
         'metric': {'name': 'aov', 'min_days': 28, 'registered_on': '2026-08-01'}, 'audience': ['x'],
         'start': '2026-08-02', 'read_point': '2026-10-30', 'end': None, 'status': 'running', 'result': None,
         'decision': None, 'learnings_ref': None, 'retro': None, 'park': None, 'brain_refs': []}
    e.update(kw)
    return e


class Rules(unittest.TestCase):
    def test_metric_registered_after_start_fires(self):
        e = entry(metric={'name': 'aov', 'min_days': 28, 'registered_on': '2026-08-10'})
        self.assertEqual([f['rule_id'] for f in audit.rule_no_metric(FakeReader(), e)], ['EXP-R01'])
        self.assertEqual(audit.rule_no_metric(FakeReader(), entry()), [])

    def test_early_read_fires_only_under_minimum(self):
        early = entry(result={'read_on': '2026-08-20', 'direction': 'up', 'lift': 0.1})
        late = entry(result={'read_on': '2026-09-20', 'direction': 'up', 'lift': 0.1})
        self.assertEqual(len(audit.rule_early_read(FakeReader(), early)), 1)
        self.assertEqual(audit.rule_early_read(FakeReader(), late), [])

    def test_learning_written_back_is_quiet(self):
        res = {'read_on': '2026-09-20', 'direction': 'up', 'lift': 0.1}
        self.assertEqual(audit.rule_learning(FakeReader(), entry(result=res, learnings_ref='bombas.learnings.ok')), [])
        self.assertEqual(len(audit.rule_learning(FakeReader(), entry(result=res))), 1)

    def test_read_point_too_small(self):
        e = entry(metric={'name': 'repeat_rate_90d', 'min_days': 30, 'registered_on': '2026-08-01'},
                  read_point='2026-09-15')
        f = audit.rule_small(FakeReader(), e)
        self.assertEqual(f[0]['rule_id'], 'EXP-R07')
        self.assertEqual(f[0]['evidence'][0]['baseline'], 90)

    def test_winner_without_money_input_has_null_stake_not_zero(self):
        e = entry(status='done', result={'read_on': '2026-08-01', 'direction': 'up', 'lift': 0.05},
                  decision={'choice': 'roll_out', 'on': '2026-08-02', 'rolled_out_on': None})
        f = audit.rule_not_rolled(FakeReader(), e, None, None)[0]
        self.assertIsNone(f['money_at_stake'])
        self.assertTrue(f['money_reason'])

    def test_overlap_needs_shared_audience_and_time(self):
        a = entry(id='A', audience=['site'])
        b = entry(id='B', audience=['site'], start='2026-09-01')
        c = entry(id='C', audience=['amazon'], start='2026-09-01')
        self.assertEqual(len(audit.rule_overlap(FakeReader(), [a, b])), 1)
        self.assertEqual(audit.rule_overlap(FakeReader(), [a, c]), [])


class Bombas(unittest.TestCase):
    def test_api_shape(self):
        d = overview()
        for k in ('brand', 'window', 'registry', 'by_status', 'tiles', 'insights', 'chart', 'findings', 'rules'):
            self.assertIn(k, d)
        self.assertTrue(d['brand']['simulated'] and d['registry_simulated'])
        self.assertEqual(len(d['tiles']), 3)
        self.assertEqual(len(d['insights']), 2)
        self.assertEqual(len(d['registry']), 6)
        self.assertEqual(len(d['chart']['labels']), len(d['chart']['days_run']))
        for t in d['tiles'].values():
            self.assertIsInstance(t['value'], int)
        for i in d['insights']:
            self.assertTrue(i['rule'] and i['sentence'])

    def test_audit_shape(self):
        fs = audit.run('bombas', {'ends_on': END.isoformat()})
        self.assertTrue(fs)
        rule_ids = {r['rule_id'] for r in audit.RULES}
        for f in fs:
            self.assertEqual(list(f)[:len(FIELDS)], FIELDS)
            self.assertIn(f['rule_id'], rule_ids)
            self.assertIn(f['severity'], ('critical', 'high', 'medium', 'low'))
            self.assertTrue(f['id'].startswith(f'25-experiments.{f["rule_id"]}.'))
            self.assertIn(f['capability']['autonomy'], ('agent_does', 'founder_gate', 'human_assist'))
            for ev in f['evidence']:
                self.assertEqual(set(ev), EVIDENCE)
                self.assertTrue(ev['simulated'])
            if f['money_at_stake'] is None:
                self.assertTrue(f['money_reason'])
            else:
                self.assertGreater(f['money_at_stake']['usd'], 0)
            if f['status'] == 'unavailable':
                self.assertEqual(f['evidence'], [])
                self.assertTrue(f['unavailable']['fix'])

    def test_audit_is_deterministic(self):
        w = {'ends_on': END.isoformat()}
        self.assertEqual(json.dumps(audit.run('bombas', w), sort_keys=True),
                         json.dumps(audit.run('bombas', w), sort_keys=True))

    def test_rules_fire_on_bombas(self):
        fired = {f['rule_id'] for f in audit.run('bombas', {'ends_on': END.isoformat()})}
        for r in ('EXP-R01', 'EXP-R02', 'EXP-R03', 'EXP-R04', 'EXP-R05', 'EXP-R06'):
            self.assertIn(r, fired)

    def test_no_em_dashes_and_short_sentences(self):
        d = overview()
        texts = [f['sentence'] for f in d['findings']] + [i['sentence'] for i in d['insights']]
        texts += [t['plain'] for t in d['tiles'].values()]
        for s in texts:
            self.assertNotIn('—', s)
            self.assertNotIn('–', s)
            self.assertLessEqual(len(s.split()), 40, s)
            self.assertIsNone(re.search(r'\b(should|try|consider)\b', s, re.I), s)
        for name in ('index.html', 'screen.js', 'api.py', 'audit.py', 'FEATURES.md'):
            self.assertNotIn('—', (FOLDER / name).read_text(encoding='utf-8'), name)


if __name__ == '__main__':
    unittest.main()
