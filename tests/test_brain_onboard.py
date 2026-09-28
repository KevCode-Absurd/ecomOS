"""Tests for app/brain/onboard.py and the setup screen's onboard routes. Offline: fixtures only."""
import hashlib
import importlib.util
import json
import shutil
import socket
import sys
import tempfile
import unittest
import urllib.request
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'app' / 'brain'))

from app.brain import onboard  # noqa: E402

REAL = ROOT / 'app' / 'brain' / 'bombas'
PAID = ('adlibrary', 'amazon_reviews', 'reddit')
FREE = ('site', 'stack', 'adlib_pages', 'amazon_discover', 'reddit_plan', 'press', 'jobs')
TODAY = '2026-09-28'


def tree_hash(folder: Path) -> str:
    h = hashlib.sha256()
    for f in sorted(folder.rglob('*')):
        if f.is_file():
            h.update(str(f.relative_to(folder)).encode())
            h.update(f.read_bytes())
    return h.hexdigest()


class NoNetwork:
    """Any socket connect or urlopen is counted and refused."""
    def __init__(self):
        self.calls = []

    def _refuse(self, *a, **k):
        self.calls.append(a[:2])
        raise OSError('network call in a fixture run')

    def __enter__(self):
        self.patches = [mock.patch.object(socket.socket, 'connect', self._refuse),
                        mock.patch.object(socket, 'create_connection', self._refuse),
                        mock.patch.object(urllib.request, 'urlopen', self._refuse)]
        for p in self.patches:
            p.start()
        return self

    def __exit__(self, *exc):
        for p in self.patches:
            p.stop()


def run(out: Path, **kw):
    r = onboard.Runner('bombas', 'https://bombas.com', 'Bombas', mode='mock', fixtures=True, out=out,
                       today=TODAY, echo=None, **kw)
    return r, r.run(compare=True)


class OnboardFixtureRun(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp())
        cls.before = tree_hash(REAL)
        with NoNetwork() as net:
            cls.runner, cls.summary = run(cls.tmp / 'full')
        cls.net_calls = net.calls
        cls.log = onboard.read_log(cls.tmp / 'full' / 'bombas')
        cls.steps = {r['step']: r for r in cls.log if r['step'] in onboard.STEP_NAMES}

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp)

    def test_every_step_logged_in_order(self):
        order = [r['step'] for r in self.log if r['step'] in onboard.STEP_NAMES]
        self.assertEqual(order, onboard.STEP_NAMES)
        self.assertEqual(self.log[0]['step'], 'start')
        self.assertEqual(self.log[-1]['step'], 'done')
        for r in self.steps.values():
            for key in ('step', 'started', 'finished', 'records', 'cost_usd', 'status'):
                self.assertIn(key, r, r['step'])
            self.assertNotEqual(r['status'], 'error', f"{r['step']}: {r.get('note')}")
        for name in FREE:
            self.assertGreater(self.steps[name]['records'], 0, name)

    def test_paid_steps_show_an_estimate_and_run_in_mock(self):
        for name in PAID:
            r = self.steps[name]
            self.assertEqual(r['status'], 'mock', name)
            self.assertGreater(r['estimate_usd'], 0, name)
            self.assertEqual(r['cost_usd'], 0.0, name)
        self.assertLessEqual(self.summary['committed_usd'], 10.0)
        self.assertEqual(self.summary['cost_usd'], 0.0)

    def test_record_count_within_five_percent(self):
        c = self.summary['compare']
        self.assertTrue(c['ok'], c['outside'])
        covered = set(c['covered'])
        for s in ('identity', 'products', 'offers', 'policies', 'claims', 'language_bank', 'stack', 'team'):
            self.assertIn(s, covered)
        for row in c['rows']:
            if row['covered']:
                self.assertLessEqual(row['lost'], 0.05 * row['real'] + 1e-9, row['section'])

    def test_no_network_call(self):
        self.assertEqual(self.net_calls, [])

    def test_real_brain_untouched(self):
        self.assertEqual(tree_hash(REAL), self.before)
        self.assertTrue((self.tmp / 'full' / 'bombas' / 'BRAIN.md').is_file())

    def test_at_most_five_questions_written(self):
        qs = self.summary['questions']
        self.assertTrue(0 < len(qs) <= 5)
        oq = json.loads((self.tmp / 'full' / 'bombas' / 'open_questions.json').read_text())
        keeper = [r for r in oq if '.open_questions.keeper_' in r['id']]
        self.assertEqual(len(keeper), len(qs))
        self.assertEqual([r['value']['bank_id'] for r in keeper], [q['id'] for q in qs])

    def test_refused_paid_step_does_not_stop_free_ones(self):
        with NoNetwork() as net:
            _, s = run(self.tmp / 'capped', max_usd=0.4)
        self.assertEqual(net.calls, [])
        steps = {r['step']: r for r in onboard.read_log(self.tmp / 'capped' / 'bombas') if r['step'] in onboard.STEP_NAMES}
        for name in PAID:
            self.assertEqual(steps[name]['status'], 'refused', name)
            self.assertIn('over the', steps[name]['note'])
        for name in FREE + ('merge', 'ladders', 'router', 'questions'):
            self.assertIn(steps[name]['status'], ('ok', 'mock'), name)
        self.assertIn('search refused', steps['amazon_discover']['note'])
        self.assertEqual(s['committed_usd'], 0.0)
        self.assertTrue(s['questions'])

    def test_status_reads_the_log(self):
        st = onboard.status('bombas', self.tmp / 'full')
        self.assertTrue(st['done'])
        self.assertEqual(len(st['lanes']), len(onboard.LANES))
        self.assertEqual(st['progress'], {'finished': len(onboard.LANES), 'total': len(onboard.LANES)})
        self.assertGreater(st['estimate_usd'], 0)
        self.assertEqual(len(st['questions']), len(self.summary['questions']))


class Req:
    def __init__(self, method, path, body=None, brand='bombas'):
        self.method, self.path, self.body = method, path, body
        self.query = {'brand': [brand]} if brand else {}

    def arg(self, name, default=None):
        v = self.query.get(name)
        return v[0] if v else default


class SetupOnboardRoutes(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location('setup_api_onboard_test', ROOT / 'app' / 'screens' / 'setup' / 'api.py')
        self.api = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = self.api
        spec.loader.exec_module(self.api)
        self.tmp = Path(tempfile.mkdtemp())
        self.api.ONBOARD_ROOT = self.tmp

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_status_shape_before_any_run(self):
        st = self.api.handle(Req('GET', ['onboard', 'status'], brand='newbrand'))
        self.assertFalse(st['started'])
        self.assertEqual([l['step'] for l in st['lanes']], onboard.STEP_NAMES)
        self.assertEqual(st['questions'], [])
        for key in ('progress', 'records', 'cost_usd', 'estimate_usd', 'mode'):
            self.assertIn(key, st)

    def test_start_runs_in_background_and_status_returns_the_log(self):
        with NoNetwork() as net:
            r = self.api.handle(Req('POST', ['onboard', 'start'], {'url': 'candles.example', 'name': 'Candle Co',
                                                                  'fixtures': True}, brand='candleco'))
            self.assertTrue(r['started'])
            self.api._runs['candleco'].join(60)
        self.assertEqual(net.calls, [])
        st = self.api.handle(Req('GET', ['onboard', 'status'], brand='candleco'))
        self.assertTrue(st['done'])
        by = {l['step']: l for l in st['lanes']}
        self.assertEqual([l['step'] for l in st['lanes'] if l['status'] == 'error'], [])
        self.assertEqual(by['site']['status'], 'skipped')  # no saved pages for a new brand
        self.assertEqual(by['adlibrary']['status'], 'waiting')  # nothing confirmed yet
        self.assertEqual(by['reddit']['status'], 'waiting')
        self.assertIn('estimate_usd', by['amazon_discover'])
        self.assertLessEqual(len(st['questions']), 5)

    def test_bad_input(self):
        self.assertEqual(self.api.handle(Req('GET', ['onboard', 'status'], brand='Bad Brand!'))[0], 400)
        self.assertEqual(self.api.handle(Req('POST', ['onboard', 'start'], {'url': 'nope'}))[0], 400)
        self.assertEqual(self.api.handle(Req('GET', ['onboard', 'nothing']))[0], 404)

    def test_mock_run_never_writes_a_real_brain(self):
        with self.assertRaises(ValueError):
            onboard.Runner('bombas', 'bombas.com', 'Bombas', mode='mock', out=onboard.HERE)


if __name__ == '__main__':
    unittest.main()
