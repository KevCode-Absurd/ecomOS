"""Screen 14-email-messaging: audit rules, API shape, and the page data on Bombas simulated data.

The synthetic tests feed the rules a tiny flow and campaign log so rules that do not fire on Bombas are
proven to fire. The Bombas tests skip when app/data/brands/bombas/data.sqlite has not been built.
"""
import importlib.util
import json
import sys
import unittest
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / 'app' / 'screens' / '14-email-messaging'
BOMBAS_DB = ROOT / 'app' / 'data' / 'brands' / 'bombas' / 'data.sqlite'
AUDIT_KEYS = ['id', 'screen', 'rule_id', 'severity', 'entity', 'evidence', 'sentence', 'capability', 'money_at_stake',
              'confidence', 'brain_refs', 'first_seen', 'last_seen', 'status', 'unavailable']
EVIDENCE_KEYS = {'metric', 'value', 'unit', 'window', 'ends_on', 'freshness_days', 'baseline', 'baseline_kind',
                 'source', 'simulated'}
DASHES = ('—', '–')


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


api = load('email_messaging_api_test', SCREEN / 'api.py')
audit = api.audit
END = date(2026, 9, 27)


class Req:
    def __init__(self, path, brand='bombas', method='GET'):
        self.path, self.method, self._brand = path, method, brand

    def arg(self, name, default=None):
        return self._brand if name == 'brand' else default


class FakeReader:
    """A 28-day log: a welcome flow whose step 2 loses 80 percent, a checkout flow the platform over-counts
    by 50 percent, a broad campaign past the engaged segment and a restock send with no restock."""

    def __init__(self):
        self.ends_on = END
        day = END.isoformat()
        f = lambda fid, name, mid, ch, sends, rev: {
            'date': day, 'flow_id': fid, 'flow': name, 'flow_status': 'live', 'message_id': mid, 'channel': ch,
            'sends': sends, 'opens': sends // 2, 'clicks': sends // 10, 'unsubscribes': 1, 'bounces': 1,
            'attributed_revenue': rev, 'attributed_orders': 30}
        self.tables = {
            'flows': [f('F-1', 'Welcome Series', 'FM-1', 'email', 1000, 500.0), f('F-1', 'Welcome Series', 'FM-2', 'email', 150, 100.0),
                      f('F-1', 'Welcome Series', 'FM-3', 'email', 148, 0.0), f('F-1', 'Welcome Series', 'FM-4', 'email', 146, 0.0),
                      f('F-2', 'Abandoned Checkout', 'FM-5', 'email', 800, 3000.0)],
            'campaign_sends': [
                {'campaign_id': 'KC-1', 'campaign_name': 'News', 'subject': 'News', 'channel': 'email', 'send_time': day + 'T18:00:00Z',
                 'audiences': 'Engaged 90d', 'sends': 1000, 'opens': 400, 'clicks': 40, 'unsubscribes': 2, 'bounces': 3, 'attributed_revenue': 50.0},
                {'campaign_id': 'KC-2', 'campaign_name': 'Restock: best sellers', 'subject': 'Restock: best sellers', 'channel': 'email',
                 'send_time': day + 'T18:00:00Z', 'audiences': 'All subscribers', 'sends': 3000, 'opens': 900, 'clicks': 90,
                 'unsubscribes': 15, 'bounces': 15, 'attributed_revenue': 80.0}],
            'inventory': [{'date': (END - timedelta(days=1)).isoformat(), 'sku': 'S1', 'on_hand': 50},
                          {'date': day, 'sku': 'S1', 'on_hand': 40}],
        }
        self.matched = {'value': 2600.0, 'unavailable': False, 'inputs': {'net_revenue_all_orders': 100000.0},
                        'by_flow': [{'flow': 'Abandoned Checkout', 'orders': 40, 'net_revenue': 2000.0},
                                    {'flow': 'Welcome Series', 'orders': 25, 'net_revenue': 600.0}]}

    def rows(self, name):
        return self.tables.get(name)

    def m(self, name, days=28, end=None, **kw):
        return self.matched

    def span(self, days=28, end=None):
        end = end or self.ends_on
        return (end - timedelta(days=days - 1)).isoformat(), end.isoformat()


def check_shape(t, f):
    t.assertEqual(list(f)[:len(AUDIT_KEYS)], AUDIT_KEYS)
    t.assertTrue(f['id'].startswith(f'14-email-messaging.{f["rule_id"]}.'))
    t.assertIn(f['severity'], ('critical', 'high', 'medium', 'low'))
    t.assertIn(f['status'], ('open', 'unavailable'))
    t.assertIn(f['capability']['autonomy'], ('agent_does', 'founder_gate', 'human_assist'))
    t.assertTrue(0.1 <= f['confidence'] <= 1)
    for e in f['evidence']:
        t.assertTrue(EVIDENCE_KEYS <= set(e))
        t.assertTrue(e['simulated'])
        t.assertIsNotNone(e['value'])
    if f['money_at_stake'] is None:
        t.assertTrue(f.get('money_reason'))
    else:
        t.assertGreaterEqual(f['money_at_stake']['usd'], 0)
        t.assertTrue(f['money_at_stake']['formula'] and f['money_at_stake']['inputs'])
    if f['status'] == 'unavailable':
        t.assertEqual(f['evidence'], [])
        t.assertTrue(f['unavailable']['inputs'] and f['unavailable']['fix'])
    for d in DASHES:
        t.assertNotIn(d, f['sentence'])
    t.assertLessEqual(len(f['sentence'].split()), 40)


class TestRulesSynthetic(unittest.TestCase):
    def setUp(self):
        self._brain = audit.brain
        audit.brain = lambda brand: None
        self.fs = audit.run('bombas', {'ends_on': END.isoformat()}, reader=FakeReader())
        self.by = {}
        for f in self.fs:
            self.by.setdefault(f['rule_id'], []).append(f)

    def tearDown(self):
        audit.brain = self._brain

    def test_every_rule_is_listed_and_accounted_for(self):
        self.assertEqual([r['rule_id'] for r in audit.RULES], [f'EMAIL-R{n:02d}' for n in range(1, 16)])
        for r in audit.RULES:
            self.assertEqual(r['owner_screen'], '14-email-messaging')

    def test_mismatch_welcome_sunset_restock_fire(self):
        self.assertEqual([f['entity']['id'] for f in self.by['EMAIL-R01']], ['F-2'])
        r10 = self.by['EMAIL-R10'][0]
        self.assertIn('FM-1', r10['entity']['id'])
        self.assertGreater(r10['money_at_stake']['usd'], 0)
        r12 = self.by['EMAIL-R12'][0]
        self.assertEqual(r12['evidence'][0]['value'], 2000)
        self.assertEqual(r12['money_at_stake']['inputs']['contacts_lost_outside_segment'], 20)
        self.assertEqual(self.by['EMAIL-R15'][0]['entity']['id'], 'KC-2')

    def test_shape(self):
        for f in self.fs:
            check_shape(self, f)


@unittest.skipUnless(BOMBAS_DB.is_file(), 'bombas data.sqlite not built')
class TestBombas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fs = audit.run('bombas')
        cls.ov = api.handle(Req(['overview']))

    def test_audit_shape_and_determinism(self):
        for f in self.fs:
            check_shape(self, f)
        self.assertEqual(json.dumps(self.fs, sort_keys=True), json.dumps(audit.run('bombas'), sort_keys=True))
        rules = {f['rule_id'] for f in self.fs}
        self.assertTrue({'EMAIL-R02', 'EMAIL-R04', 'EMAIL-R13'} <= rules)

    def test_rules_fire_on_bombas(self):
        open_ = [f for f in self.fs if f['status'] == 'open']
        self.assertTrue(open_)
        self.assertTrue(any(f['money_at_stake'] for f in open_))
        order = [(audit.SEVERITY_ORDER[f['severity']], -((f['money_at_stake'] or {}).get('usd') or 0)) for f in self.fs]
        self.assertEqual(order, sorted(order))

    def test_api_shape(self):
        ov = self.ov
        self.assertTrue(ov['brand']['simulated'])
        self.assertEqual(set(ov['tiles']), {'flow_revenue', 'list_growth', 'unsubscribe_rate'})
        for t in ov['tiles'].values():
            self.assertTrue(t['value'] is not None or t['unavailable_reason'])
        self.assertEqual(len(ov['insights']), 2)
        for i in ov['insights']:
            self.assertTrue(i['rule'] and i['sentence'])
            for d in DASHES:
                self.assertNotIn(d, i['sentence'])
        c = ov['chart']
        self.assertEqual(len(c['labels']), len(c['platform']))
        self.assertEqual(len(c['labels']), len(c['matched']))
        self.assertEqual(api.handle(Req(['nope']))[0], 404)
        self.assertEqual(api.handle(Req(['overview'], method='POST'))[0], 405)
        self.assertEqual(api.handle(Req(['overview'], brand='../x'))[0], 400)


if __name__ == '__main__':
    unittest.main()
