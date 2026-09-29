import datetime as dt
import json
import os
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from unittest import mock

from meta_gallery import live_refresh as lr
from meta_gallery import team
from meta_gallery.server import Gallery, make_handler
from meta_gallery.snapshot import build
from tests.test_meta_gallery import synthetic_capture

TOKEN = 'EAAtesttoken' + 'Q' * 60
MBKEY = 'mb_testkey' + 'W' * 40


class FakeGraph:
    """Answers the read-only GETs live_refresh makes, from fixed rows."""
    account = 'act_1'

    def __init__(self, fail=False):
        self.fail, self.calls = fail, []

    def paged(self, path, **p):
        self.calls.append(p)
        if self.fail:
            raise RuntimeError(f'HTTP 400: bad token {TOKEN}')
        tr = json.loads(p['time_range'])
        if p.get('breakdowns'):
            dim = p['breakdowns']
            val = {'age': '25-34', 'gender': 'female', 'publisher_platform': 'instagram'}[dim]
            return [{'ad_id': '100000', 'ad_name': 'Ad 0', dim: val, 'spend': '70', 'date_start': tr['since'], 'date_stop': tr['until'],
                     'actions': [{'action_type': 'omni_purchase', 'value': '1'}], 'action_values': [{'action_type': 'omni_purchase', 'value': '900'}]}]
        days = [dt.date.fromisoformat(tr['since']) + dt.timedelta(days=i) for i in range(7)]
        if 'video_play_actions' in p['fields']:
            return [{'ad_id': '100100', 'ad_name': 'Ad 100', 'spend': '50', 'impressions': '1000', 'date_start': d.isoformat(), 'date_stop': d.isoformat(),
                     'actions': [{'action_type': 'video_view', 'value': '25'}], 'video_play_actions': [{'action_type': 'video_view', 'value': '40'}]}
                    for d in days]
        rows = []
        for d in days:
            rows.append({'ad_id': '100000', 'ad_name': 'Ad 0', 'spend': '12.5', 'impressions': '900', 'date_start': d.isoformat(), 'date_stop': d.isoformat(),
                         'actions': [{'action_type': 'omni_purchase', 'value': '1'}, {'action_type': 'link_click', 'value': '9'}],
                         'action_values': [{'action_type': 'omni_purchase', 'value': '800'}]})
            rows.append({'ad_id': '555555', 'ad_name': 'Brand new ad', 'spend': '20', 'impressions': '500', 'date_start': d.isoformat(), 'date_stop': d.isoformat()})
        return rows

    def get(self, path, **p):
        self.calls.append(p)
        if path.endswith('/insights'):
            return {'data': [{'spend': '123456.78'}]}
        assert 'ids' not in p, 'the ids= form is deprecated in Graph API v26'
        return self._lookup(path).get(path, {})

    def _lookup(self, ids):
        if '555555' in ids:
            return {'555555': {'id': '555555', 'name': 'Brand new ad', 'effective_status': 'ACTIVE', 'status': 'ACTIVE', 'campaign_id': '900',
                               'adset_id': '801', 'creative': {'id': 'cnew'}, 'campaign': {'name': 'Evergreen'}, 'adset': {'name': 'New set'}}}
        if 'cnew' in ids:
            return {'cnew': {'id': 'cnew', 'object_type': 'SHARE', 'image_hash': 'hnew', 'image_url': 'https://img/new', 'body': 'New'}}
        if '801' in ids:
            return {'801': {'id': '801', 'name': 'New set', 'is_dynamic_creative': False,
                            'attribution_spec': [{'event_type': 'CLICK_THROUGH', 'window_days': 7}]}}
        return {}


ORDER_DAYS = {'2026-04-01'}


class FakeMetabase:
    """Dashboard cards: 1 order on each day in ORDER_DAYS, month cards add the days up."""
    def card(self, dash, dc, params):
        maps = [{'parameter_id': lr.RANGE_PARAM, 'target': ['dimension', 1]}] if dash == 6 else \
               [{'parameter_id': lr.GA_FROM, 'target': 'a'}, {'parameter_id': 'to', 'target': 'b'}]
        got = params(maps)
        if dash == 26:
            return {725: [['Meta/Ad', '/', 30], ['Meta/Ad', '/p', 5]], 731: [['Meta/Ad', 2]], 751: [['New Users', 100]]}[dc]
        if dc == lr.TRAFFIC_CARD:
            return [['2026-04-01T00:00:00', 500, 20, 1000, 1], ['2025-01-01T00:00:00', 1, 1, 1, 1]]
        a, b = got[0]['value'].split('~')
        n = sum(1 for d in ORDER_DAYS if a <= d <= b)
        if not n:
            return [[None]] if dc in (387, 386) else []
        rows = {387: [[1000 * n]], 280: [[None, n]], 281: [[n]], 289: [['Stock', 1000 * n, None, n]], 386: [[None]], 278: [[0]],
                287: [[1000 * n, '18K Yellow Gold', n]], 290: [[1000 * n, 'Rings', None, n]], 284: [], 297: [['10000-25000', n]], 296: [],
                294: [['Razor Pay', n]], 277: [[1000 * n, None, 'GHR-1', 'Ring', n]], 292: [], 285: [], 283: []}
        return rows[dc]


class LiveRefreshTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        t = Path(self.tmp.name)
        (t / 'raw').mkdir()
        (t / 'raw' / 'mcp_capture_2026-04-01_1y.json').write_text(json.dumps(synthetic_capture()), encoding='utf-8')
        (t / 'sales.json').write_text(json.dumps({'months': {}, 'daily': {'2026-03-15': {'items': 0}}, 'ga': []}), encoding='utf-8')
        self.patches = [mock.patch.object(lr, 'RAW', t / 'raw'), mock.patch.object(lr, 'CACHE', t / 'cache' / 'gallery.json'),
                        mock.patch.object(lr, 'SALES', t / 'sales.json'), mock.patch.object(lr, 'TRAFFIC', t / 'traffic.json'),
                        mock.patch.dict(os.environ, {'TEAM_STATE': str(t / 'state'), 'META_ACCESS_TOKEN': TOKEN, 'META_AD_ACCOUNT_ID': '1',
                                                     'METABASE_API_KEY': MBKEY}),
                        mock.patch.object(lr, 'load_env', return_value={})]
        for p in self.patches:
            p.start()
        self.t = t

    def tearDown(self):
        for p in reversed(self.patches):
            p.stop()
        self.tmp.cleanup()

    def test_meta_refresh_merges_days_new_ads_and_breakdowns(self):
        g = FakeGraph()
        out = lr.meta_refresh(dt.date(2026, 3, 27), dt.date(2026, 4, 2), graph=g)
        self.assertEqual(out['new_ads'], 1)
        self.assertTrue(all(c.get('filtering') is None or 'spend' in c['filtering'] for c in g.calls))
        cap = json.loads(lr.newest_capture_file().read_text())
        self.assertEqual(cap['window']['until'], '2026-04-02')
        self.assertIn('555555', {a['id'] for a in cap['ads']})
        self.assertIn('cnew', {c['id'] for c in cap['creatives']})
        self.assertEqual(cap['account_spend_check']['account_total_spend'], 123456.78)
        # This month's and last month's breakdown rows replaced by the fresh ones.
        starts = {r['date_start'] for r in cap['monthly']['age'] if r['id'] == '100000' and r['age'] == '25-34' and r['amount_spent']['value'] == '70'}
        self.assertEqual(starts, {'2026-03-01', '2026-04-01'})
        self.assertTrue(cap['video_daily'] and cap['video_daily'][0]['cost_per_video_view']['value'] == '2.0')
        snap = json.loads(lr.CACHE.read_text())
        self.assertEqual(snap['meta']['window']['until'], '2026-04-02')
        self.assertNotIn(TOKEN, lr.CACHE.read_text() + json.dumps(cap))

    def test_sales_and_traffic_refresh(self):
        mb = FakeMetabase()
        out = lr.sales_refresh(dt.date(2026, 3, 27), dt.date(2026, 4, 2), mb=mb)
        self.assertEqual(out['months_checked'], ['2026-03', '2026-04'])
        sales = json.loads(lr.SALES.read_text())
        self.assertEqual(sales['daily']['2026-04-01']['orders'], 1)
        self.assertEqual(sales['ga'], [['2026-04-01', 500, 20, 1000, 1]])
        tr = lr.traffic_refresh(dt.date(2026, 4, 2), mb=mb)
        self.assertEqual(tr, {'weeks': 12, 'until': '2026-04-02'})
        self.assertEqual(json.loads(lr.TRAFFIC.read_text())['weeks'][0]['landings'], {'Meta/Ad': 35})

    def test_metabase_password_sign_in(self):
        seen = []

        class R:
            def __init__(self, body):
                self.body = body

            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

            def read(self):
                return json.dumps(self.body).encode()

        def fake_open(req, timeout=None):
            seen.append((req.full_url, dict(req.header_items())))
            if req.full_url.endswith('/api/session'):
                return R({'id': '0f1e2d3c-4b5a-6978-8796-a5b4c3d2e1f0'})
            return R({'dashcards': []})
        mb = lr.Metabase('https://mb.example', None, 'me@x.com', 'pw-secret-1')
        with mock.patch.object(lr.urllib.request, 'urlopen', fake_open):
            mb.dash(6)
            mb.dash(26)
        self.assertEqual(seen[0][0], 'https://mb.example/api/session')
        self.assertEqual(seen[1][1].get('X-metabase-session'), '0f1e2d3c-4b5a-6978-8796-a5b4c3d2e1f0')
        self.assertEqual(len([u for u, _ in seen if u.endswith('/api/session')]), 1)

    def test_replace_falls_back_when_windows_locks_the_file(self):
        dst = self.t / 'x.json'
        dst.write_text('old')
        tmp = self.t / 'x.tmp'
        tmp.write_text('new')
        with mock.patch.object(Path, 'replace', side_effect=PermissionError('[WinError 5] Access is denied')), mock.patch.object(lr.time, 'sleep'):
            lr._replace(tmp, dst)
        self.assertEqual(dst.read_text(), 'new')
        self.assertFalse(tmp.exists())

    def test_browser_session_is_used_without_sign_in(self):
        seen = []

        class R:
            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

            def read(self):
                return b'{"dashcards": []}'

        def fake_open(req, timeout=None):
            seen.append((req.full_url, dict(req.header_items())))
            return R()
        mb = lr.Metabase('https://mb.example', session='11111111-2222-3333-4444-555555555555')
        with mock.patch.object(lr.urllib.request, 'urlopen', fake_open):
            mb.dash(6)
        self.assertEqual([u for u, _ in seen], ['https://mb.example/api/dashboard/6'])
        self.assertEqual(seen[0][1]['X-metabase-session'], '11111111-2222-3333-4444-555555555555')

    def test_run_records_errors_without_secrets_and_keeps_going(self):
        with mock.patch.object(lr, '_graph', return_value=FakeGraph(fail=True)), mock.patch.object(lr, '_metabase', return_value=FakeMetabase()):
            res = lr.run('asha', today=dt.date(2026, 4, 3))
        self.assertFalse(res['ok'])
        self.assertIn('error', res['parts']['meta'])
        self.assertNotIn('error', res['parts']['sales'])
        blob = json.dumps(lr.status()) + (self.t / 'state' / 'refresh.json').read_text()
        self.assertNotIn(TOKEN, blob)
        self.assertNotIn(MBKEY, blob)
        self.assertNotIn('QQQQQQQQQQ', blob)

    def test_cooldown_only_in_team_mode(self):
        with mock.patch.object(lr, 'run'):
            lr.start('kevin')
            lr._state['running'] = False
            lr.start('kevin')  # on a laptop there is no wait
            lr._state['running'] = False
        with mock.patch.object(lr, 'run'), mock.patch.dict(os.environ, {'TEAM_MODE': '1'}):
            with self.assertRaises(ValueError) as e:  # the shared app waits 30 minutes
                lr.start('asha')
        self.assertIn('Next refresh after', str(e.exception))

    def test_restore_uses_newer_disk_copy(self):
        store = self.t / 'store'
        store.mkdir()
        (store / 'sales.json').write_text(json.dumps({'months': {}, 'daily': {'2026-04-02': {}}, 'ga': []}))
        (store / 'traffic.json').write_text(json.dumps({'weeks': [{'until': '2000-01-01'}]}))
        lr.TRAFFIC.write_text(json.dumps({'weeks': [{'until': '2026-04-02'}]}))
        with mock.patch.dict(os.environ, {'REFRESH_STORE': str(store)}):
            used = lr.restore()
        self.assertEqual(used, ['sales.json'])
        self.assertIn('2026-04-02', json.loads(lr.SALES.read_text())['daily'])
        self.assertEqual(json.loads(lr.TRAFFIC.read_text())['weeks'][0]['until'], '2026-04-02')


class RefreshEndpointTests(unittest.TestCase):
    def test_team_members_can_refresh_once_per_30_minutes(self):
        from http.server import ThreadingHTTPServer
        tmp = tempfile.TemporaryDirectory()
        code = 'team-code-xyz-123'
        env = mock.patch.dict(os.environ, {'TEAM_MODE': '1', 'TEAM_SECRET': 'x' * 40, 'TEAM_STATE': tmp.name,
                                           'TEAM_CODES': f'asha:{team.hash_code(code)}', 'METABASE_API_KEY': MBKEY})
        env.start()
        no_env_file = mock.patch.object(lr, 'load_env', return_value={})
        no_env_file.start()
        try:
            path = Path(tmp.name) / 'gallery.json'
            path.write_text(json.dumps(build(synthetic_capture())), encoding='utf-8')
            srv = ThreadingHTTPServer(('127.0.0.1', 0), make_handler(Gallery(path, settings_path=Path(tmp.name) / 's.json',
                                                                             notes_path=Path(tmp.name) / 'n.json')))
            base = f'http://127.0.0.1:{srv.server_address[1]}'
            threading.Thread(target=srv.serve_forever, daemon=True).start()

            def call(p, body=None, cookie=None):
                h = {'Content-Type': 'application/json', **({'Cookie': cookie} if cookie else {})}
                req = urllib.request.Request(base + p, data=None if body is None else json.dumps(body).encode(), method='GET' if body is None else 'POST', headers=h)
                try:
                    r = urllib.request.urlopen(req)
                    return r.status, r.read(), r.headers
                except urllib.error.HTTPError as e:
                    return e.code, e.read(), e.headers
            self.assertEqual(call('/api/refresh')[0], 401)
            self.assertEqual(call('/api/refresh', {})[0], 401)
            cookie = call('/team/login', {'code': code})[2]['Set-Cookie'].split(';')[0]
            with mock.patch.object(lr, 'run'):
                s, body, _ = call('/api/refresh', {}, cookie)
                self.assertEqual(s, 200, body)
                lr._state['running'] = False
                s, body, _ = call('/api/refresh', {}, cookie)
                self.assertEqual(s, 400)
                self.assertIn(b'Next refresh after', body)
            s, body, _ = call('/api/refresh', cookie=cookie)
            st = json.loads(body)
            self.assertEqual(st['configured'], {'meta': False, 'metabase': True})
            self.assertNotIn(MBKEY.encode(), body)
            self.assertIn(b'refreshBox', call('/', cookie=cookie)[1])
            srv.shutdown()
        finally:
            no_env_file.stop()
            env.stop()
            tmp.cleanup()


if __name__ == '__main__':
    unittest.main()
