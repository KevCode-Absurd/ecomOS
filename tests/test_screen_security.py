"""Screen 24-security: API shape, audit shape and determinism, rules on Bombas simulated data, wording.

The Bombas tests skip when app/data/brands/bombas/data.sqlite has not been built. The brain-only rules
(scripts, agent endpoint, consent, captcha, privacy age) and the unavailable rules need no data.sqlite.
"""
import importlib.util
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / 'app' / 'screens' / '24-security'
BOMBAS_DB = ROOT / 'app' / 'data' / 'brands' / 'bombas' / 'data.sqlite'
AUDIT_KEYS = ['id', 'screen', 'rule_id', 'severity', 'entity', 'evidence', 'sentence', 'capability', 'money_at_stake',
              'confidence', 'brain_refs', 'first_seen', 'last_seen', 'status', 'unavailable']
EVIDENCE_KEYS = {'metric', 'value', 'unit', 'window', 'ends_on', 'freshness_days', 'baseline', 'baseline_kind',
                 'source', 'simulated'}
ENTITY_TYPES = {'brand', 'stage', 'page', 'device', 'sku', 'campaign', 'adset', 'ad', 'flow', 'offer', 'ladder_rung',
                'metric'}
EM_DASH = '—'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


api = load('security_api_test', SCREEN / 'api.py')
audit = api.audit


class Req:
    def __init__(self, path, brand='bombas', method='GET'):
        self.path, self.method, self.data, self._brand = path, method, None, brand

    def arg(self, name, default=None):
        return self._brand if name == 'brand' else default


def strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from strings(v)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            yield from strings(v)


class StaticTest(unittest.TestCase):
    def test_rules_cover_every_room_job(self):
        caps = {r['capability'] for r in audit.RULES}
        for c in ('MONEY-C41', 'MONEY-C42', 'MONEY-C43', 'MONEY-C44', 'SITE-C13', 'MONEY-C46', 'MONEY-C47',
                  'MONEY-C48', 'MONEY-C49', 'MONEY-C74', 'MONEY-C72', 'MONEY-C73', 'MONEY-C75', 'MONEY-C76',
                  'MONEY-C77'):
            self.assertIn(c, caps)
        ids = [r['rule_id'] for r in audit.RULES]
        self.assertEqual(len(ids), len(set(ids)))
        for r in audit.RULES:
            self.assertEqual(set(r), {'rule_id', 'name', 'entity_type', 'inputs', 'capability', 'owner_screen'})
            self.assertIn(r['rule_id'], audit.__doc__)
            self.assertIn(r['capability'], audit.AUTONOMY)

    def test_no_em_dashes_in_screen_files(self):
        for name in ('api.py', 'audit.py', 'screen.js', 'index.html', 'FEATURES.md'):
            self.assertNotIn(EM_DASH, (SCREEN / name).read_text(encoding='utf-8'), name)

    def test_post_is_refused(self):
        self.assertEqual(api.handle(Req(['overview'], method='POST'))[0], 405)

    def test_bad_brand_is_400(self):
        self.assertEqual(api.handle(Req(['overview'], brand='../x'))[0], 400)


@unittest.skipUnless(BOMBAS_DB.is_file(), 'bombas data.sqlite not built')
class BombasTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ov = api.handle(Req(['overview']))
        cls.fs = cls.ov['findings']

    def test_api_shape(self):
        ov = self.ov
        for k in ('brand', 'window', 'tiles', 'insights', 'chart', 'chargebacks', 'win_rate', 'payouts', 'scripts',
                  'controls', 'coverage', 'findings', 'rules'):
            self.assertIn(k, ov)
        self.assertTrue(ov['brand']['simulated'])
        self.assertEqual(len(ov['tiles']), 3)
        for t in ov['tiles'].values():
            if t['value'] is None:
                self.assertTrue(t['unavailable_reason'])
        self.assertEqual(len(ov['insights']), 2)
        for i in ov['insights']:
            self.assertTrue(i['rule'] and i['sentence'])
        c = ov['chart']
        self.assertFalse(c.get('unavailable'), c.get('reason'))
        self.assertEqual(len(c['labels']), len(c['chargebacks']))
        self.assertEqual(c['lines_per_1000'], {'alert': 1.5, 'early_warning': 6.5, 'network': 9.0})
        self.assertEqual(len(ov['coverage']), len(audit.RULES))
        json.dumps(ov)

    def test_findings_route(self):
        out = api.handle(Req(['findings']))
        self.assertEqual(out['findings'], self.fs)
        self.assertEqual(api.handle(Req(['nope']))[0], 404)

    def test_audit_shape(self):
        self.assertTrue(self.fs)
        order = audit.SEVERITY_ORDER
        self.assertEqual([order[f['severity']] for f in self.fs], sorted(order[f['severity']] for f in self.fs))
        for f in self.fs:
            self.assertEqual(list(f)[:len(AUDIT_KEYS)], AUDIT_KEYS)
            self.assertEqual(f['id'], f'24-security.{f["rule_id"]}.{f["entity"]["id"]}')
            self.assertIn(f['severity'], order)
            self.assertIn(f['entity']['type'], ENTITY_TYPES)
            self.assertIn(f['status'], ('open', 'unavailable'))
            self.assertEqual(f['capability']['autonomy'], audit.AUTONOMY[f['capability']['id']])
            self.assertTrue(0.1 <= f['confidence'] <= 1)
            for e in f['evidence']:
                self.assertEqual(set(e), EVIDENCE_KEYS)
                self.assertTrue(e['simulated'])
            if f['money_at_stake'] is None:
                self.assertTrue(f['money_reason'])
            else:
                self.assertGreaterEqual(f['money_at_stake']['usd'], 0)
            if f['status'] == 'unavailable':
                self.assertEqual(f['evidence'], [])
                self.assertEqual(set(f['unavailable']), {'inputs', 'connector', 'fix'})
                self.assertIsNone(f['money_at_stake'])
            else:
                self.assertIsNone(f['unavailable'])

    def test_deterministic(self):
        a = audit.run('bombas')
        b = audit.run('bombas')
        self.assertEqual(json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True))
        self.assertEqual(json.dumps(a, sort_keys=True), json.dumps(self.fs, sort_keys=True))

    def test_rules_fire_on_bombas(self):
        by = {f['rule_id']: f for f in self.fs}
        opened = {r for r, f in by.items() if f['status'] == 'open'}
        self.assertTrue(opened, 'at least one rule fires')
        self.assertIn('SEC-R08', opened)  # UCP/MCP endpoint in the brain
        self.assertIn('SEC-R11', opened)  # 7 vendor scripts over 5
        self.assertEqual(by['SEC-R11']['evidence'][0]['value'], 7)
        for r in ('SEC-R03', 'SEC-R04', 'SEC-R06', 'SEC-R07', 'SEC-R10', 'SEC-R13'):
            self.assertEqual(by[r]['status'], 'unavailable', r)
            self.assertTrue(by[r]['unavailable']['connector'])
        # consent (OneTrust), captcha (hCaptcha) and a privacy policy under a year old pass
        for r in ('SEC-R09', 'SEC-R16', 'SEC-R17'):
            self.assertNotIn(r, by)

    def test_money_is_arithmetic(self):
        for f in self.fs:
            m = f['money_at_stake']
            if not m:
                continue
            i = m['inputs']
            if f['rule_id'] == 'SEC-R02':
                want = (i['win_floor'] - i['win_rate']) * i['disputes_closed'] * i['avg_disputed_amount'] * i['scale']
            else:
                want = (i['rate_now'] - i['alert_line']) * i['paid_orders'] * i['avg_disputed_amount'] * i['scale']
            self.assertAlmostEqual(m['usd'], round(max(0.0, want), 2), places=2)

    def test_win_rate_rule_matches_metric(self):
        w = audit.win_rate(audit.Reader(None, 'bombas', audit.last_full_day(None, 'bombas')))
        fired = any(f['rule_id'] == 'SEC-R02' for f in self.fs)
        if w['unavailable'] or not w['closed']:
            self.assertFalse(fired and not w['unavailable'])
        else:
            self.assertEqual(fired, w['rate'] < audit.WIN_FLOOR)

    def test_unavailable_never_zero(self):
        t = self.ov['tiles']['win_rate']
        if not self.ov['win_rate']['unavailable'] and not self.ov['win_rate']['closed']:
            self.assertIsNone(t['value'])
        self.assertIsNone(self.ov['payouts'].get('holds'))
        self.assertIsNone(self.ov['scripts']['unknown_hosts'])

    def test_no_em_dashes_in_sentences(self):
        for s in strings(self.ov):
            self.assertNotIn(EM_DASH, s)
        for f in self.fs:
            self.assertLessEqual(len(f['sentence'].split()), 40, f['sentence'])
            self.assertNotRegex(f['sentence'].lower(), r'\b(should|try|consider)\b')
            self.assertNotIn('GPT', f['sentence'])
        for i in self.ov['insights']:
            self.assertFalse(re.search(r'\bGPT\b|\.env', i['sentence']))


if __name__ == '__main__':
    unittest.main()
