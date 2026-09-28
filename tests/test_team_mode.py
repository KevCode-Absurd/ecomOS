import json
import os
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from unittest import mock

from meta_gallery import ai, team
from meta_gallery.server import Gallery, make_handler
from meta_gallery.snapshot import build
from tests.test_meta_gallery import synthetic_capture

CODE_OWNER = 'owner-code-123456'
CODE_TEAM = 'team-code-abcdefg'


class TeamModeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from http.server import ThreadingHTTPServer
        cls.tmp = tempfile.TemporaryDirectory()
        cls.env = mock.patch.dict(os.environ, {
            'TEAM_MODE': '1', 'TEAM_SECRET': 'x' * 40, 'TEAM_OWNERS': 'kevin', 'TEAM_STATE': cls.tmp.name,
            'TEAM_CODES': f'kevin:{team.hash_code(CODE_OWNER)},asha:{team.hash_code(CODE_TEAM)}',
            'TEAM_DAILY_IMAGES': '4', 'TEAM_MONTHLY_IMAGES': '100', 'TEAM_DAILY_ASKS': '2'})
        cls.env.start()
        path = Path(cls.tmp.name) / 'gallery.json'
        path.write_text(json.dumps(build(synthetic_capture())), encoding='utf-8')
        g = Gallery(path, settings_path=Path(cls.tmp.name) / 'settings.json', notes_path=Path(cls.tmp.name) / 'notes.json')
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), make_handler(g))
        cls.base = f'http://127.0.0.1:{cls.server.server_address[1]}'
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.bodies = []

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.env.stop()
        cls.tmp.cleanup()

    def call(self, path, body=None, cookie=None):
        headers = {'Content-Type': 'application/json'}
        if cookie:
            headers['Cookie'] = cookie
        req = urllib.request.Request(self.base + path, data=None if body is None else json.dumps(body).encode(),
                                     method='GET' if body is None else 'POST', headers=headers)
        try:
            r = urllib.request.urlopen(req)
            status, data, hdrs = r.status, r.read(), r.headers
        except urllib.error.HTTPError as e:
            status, data, hdrs = e.code, e.read(), e.headers
        self.bodies.append(data)
        return status, data, hdrs

    def login(self, code):
        status, _, hdrs = self.call('/team/login', {'code': code})
        self.assertEqual(status, 200)
        return hdrs['Set-Cookie'].split(';')[0]

    def test_1_locked_without_code(self):
        status, data, _ = self.call('/')
        self.assertEqual(status, 200)
        self.assertIn(b'invite code', data)
        self.assertEqual(self.call('/data.json')[0], 401)
        self.assertEqual(self.call('/api/ai-status')[0], 401)
        self.assertEqual(self.call('/api/ask', {'prompt': 'x' * 30})[0], 401)
        self.assertEqual(self.call('/team/login', {'code': 'wrong-code-000'})[0], 401)
        self.assertEqual(self.call('/data.json', cookie='eg_session=kevin|9999999999|bad')[0], 401)

    def test_2_signed_in_can_read(self):
        c = self.login(CODE_TEAM)
        self.assertEqual(self.call('/data.json', cookie=c)[0], 200)
        status, data, _ = self.call('/', cookie=c)
        self.assertIn(b'teamBadge', data)
        me = json.loads(self.call('/team/me', cookie=c)[1])
        self.assertEqual((me['name'], me['owner'], me['daily_images']), ('asha', False, 4))

    def test_3_owner_only_writes(self):
        c = self.login(CODE_TEAM)
        self.assertEqual(self.call('/api/settings', {'targets': {'roas': 3, 'cpa': 900}}, cookie=c)[0], 403)
        self.assertEqual(self.call('/api/stock-check', {'limit': 1}, cookie=c)[0], 403)

    def test_4_caps_and_refunds(self):
        c = self.login(CODE_TEAM)
        # 5 images asked, 4 allowed: refused before any paid call.
        status, data, _ = self.call('/api/variants', {'ad_id': '1000001', 'n': 5}, cookie=c)
        self.assertEqual(status, 429)
        with mock.patch.object(ai, 'ask_json', side_effect=ai.AIError('provider down')):
            self.assertEqual(self.call('/api/ask', {'prompt': 'y' * 30}, cookie=c)[0], 502)
        self.assertEqual(json.loads(self.call('/team/me', cookie=c)[1])['asks_today'], 0)  # refunded
        with mock.patch.object(ai, 'ask_json', return_value={'ok': 1}):
            self.assertEqual(self.call('/api/ask', {'prompt': 'y' * 30}, cookie=c)[0], 200)
            self.assertEqual(self.call('/api/ask', {'prompt': 'y' * 30}, cookie=c)[0], 200)
            self.assertEqual(self.call('/api/ask', {'prompt': 'y' * 30}, cookie=c)[0], 429)
        log = (Path(self.tmp.name) / 'usage_log.jsonl').read_text().splitlines()
        self.assertTrue(any('"who": "asha"' in x and '/api/ask' in x for x in log))

    def test_5_bad_origin_blocked(self):
        c = self.login(CODE_OWNER)
        req = urllib.request.Request(self.base + '/api/save/notes.json', data=b'{}', method='POST',
                                     headers={'Content-Type': 'application/json', 'Cookie': c, 'Origin': 'https://evil.example'})
        with self.assertRaises(urllib.error.HTTPError) as e:
            urllib.request.urlopen(req)
        self.assertEqual(e.exception.code, 403)

    def test_6_keys_never_sent(self):
        cfg = ai.settings()
        keys = [k for k in (cfg['anthropic_key'], cfg['openai_key'], os.environ['TEAM_SECRET']) if k]
        c = self.login(CODE_OWNER)
        for path in ('/', '/api/ai-status', '/team/me', '/data.json', '/settings.json', '/app.js', '/lab.js'):
            self.call(path, cookie=c)
        for body in self.bodies:
            for k in keys:
                self.assertNotIn(k.encode(), body)
            self.assertNotIn(CODE_OWNER.encode(), body)
            self.assertNotIn(CODE_TEAM.encode(), body)


if __name__ == '__main__':
    unittest.main()
