"""Tests for app/server.py: routes, the data layer, decisions log, screen apis, path safety."""
import importlib.util
import json
import shutil
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVER_PY = ROOT / 'app' / 'server.py'
spec = importlib.util.spec_from_file_location('ecomos_server', SERVER_PY)
server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(server)


class ServerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp())
        sample = cls.tmp / 'sample'
        sample.mkdir()
        shutil.copy(server.SAMPLE / 'brand.json', sample / 'brand.json')
        (sample / 'orders.json').write_text(json.dumps([{'id': 'o1', 'total': 80.5}, {'id': 'o2', 'total': 91}]), encoding='utf-8')
        (sample / 'sessions.csv').write_text('date,source,add_to_cart\n2026-09-01,meta,1\n2026-09-02,google,\n', encoding='utf-8')
        (sample / 'broken.json').write_text('{"rows": 1}', encoding='utf-8')
        screens = cls.tmp / 'screens'
        (screens / '00-today').mkdir(parents=True)
        (screens / '00-today' / 'index.html').write_text('<h1>today</h1>', encoding='utf-8')
        (screens / '00-today' / 'api.py').write_text(
            'def handle(req):\n'
            '    if req.path == ["echo"]:\n'
            '        return {"method": req.method, "path": req.path, "q": req.arg("q"), "body": req.body,\n'
            '                "brand": req.data.brand["brand"], "orders": len(req.data.table("orders"))}\n'
            '    if req.path == ["teapot"]:\n'
            '        return 418, {"error": "short and stout"}\n'
            '    raise RuntimeError("boom")\n', encoding='utf-8')
        cls.data = server.Data(sample)
        cls.decisions = server.Decisions(cls.tmp / 'decisions.json')
        cls.apis = server.ScreenApis(screens)
        cls.httpd = ThreadingHTTPServer(('127.0.0.1', 0), server.make_handler(cls.data, cls.decisions, cls.apis))
        cls.port = cls.httpd.server_address[1]
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def call(self, path, method='GET', body=None):
        data = json.dumps(body).encode('utf-8') if body is not None else None
        req = urllib.request.Request(f'http://127.0.0.1:{self.port}{path}', data=data, method=method,
                                     headers={'Content-Type': 'application/json'} if data else {})
        try:
            with urllib.request.urlopen(req, timeout=5) as res:
                raw = res.read()
                return res.status, (json.loads(raw) if res.headers.get('Content-Type', '').startswith('application/json') else raw)
        except urllib.error.HTTPError as exc:
            raw = exc.read()
            return exc.code, (json.loads(raw) if raw[:1] in (b'{', b'[') else raw)

    # ---- static and shell
    def test_shell_and_web_files(self):
        status, body = self.call('/')
        self.assertEqual(status, 200)
        self.assertIn(b'ecomOS', body)
        for name in server.WEB_FILES:
            self.assertEqual(self.call('/web/' + name)[0], 200, name)
        self.assertEqual(self.call('/web/server.py')[0], 404)
        self.assertEqual(self.call('/web/../server.py')[0], 404)
        self.assertEqual(self.call('/screens/00-today/../../server.py')[0], 404)

    def test_screen_static(self):
        status, body = self.call('/screens/00-today/')
        self.assertEqual(status, 200)
        self.assertIn(b'today', body)
        self.assertEqual(self.call('/screens/00-today/api.py')[0], 404)
        self.assertEqual(self.call('/screens/99-nope/')[0], 404)

    # ---- api
    def test_screens_list_reads_index(self):
        status, body = self.call('/api/screens')
        self.assertEqual(status, 200)
        slugs = [s['slug'] for s in body['screens']]
        self.assertEqual(len(slugs), 28)
        self.assertEqual(slugs[0], '00-today')
        self.assertEqual(slugs[-1], '27-wild-bets-pr')
        self.assertTrue(all(s['room'] and s['purpose'] for s in body['screens']))

    def test_brand_and_tables(self):
        status, brand = self.call('/api/brand')
        self.assertEqual(status, 200)
        self.assertTrue(brand['fictional'])
        self.assertEqual(brand['market'], 'US')
        status, body = self.call('/api/tables')
        names = {t['name']: t for t in body['tables']}
        self.assertEqual(names['orders']['rows'], 2)
        self.assertEqual(names['sessions']['rows'], 2)
        self.assertEqual(names['broken']['error'], 'unreadable')
        self.assertNotIn('brand', names)
        status, body = self.call('/api/tables/sessions?limit=1')
        self.assertEqual(body['total'], 2)
        self.assertEqual(body['rows'], [{'date': '2026-09-01', 'source': 'meta', 'add_to_cart': 1}])
        status, body = self.call('/api/tables/sessions')
        self.assertIsNone(body['rows'][1]['add_to_cart'], 'blank CSV cells are null, not 0')
        status, body = self.call('/api/tables/missing')
        self.assertEqual(status, 404)
        self.assertTrue(body['unavailable'])
        self.assertEqual(self.call('/api/tables/brand')[0], 404)

    def test_metrics_contract(self):
        status, body = self.call('/api/metrics')
        names = [m['name'] for m in body['metrics']]
        self.assertIn('add_to_cart_rate', names)
        self.assertIn('period_roas', names)
        self.assertIn('rto_rate', names)
        self.assertEqual(len(names), len(set(names)))
        status, body = self.call('/api/metrics/add_to_cart_rate?window=28d')
        self.assertEqual(status, 200)
        self.assertIsNone(body['value'])
        self.assertTrue(body['unavailable'])
        self.assertIn('formula', body)
        self.assertEqual(self.call('/api/metrics/not_a_metric')[0], 404)

    def test_decisions_log(self):
        status, body = self.call('/api/decisions', 'POST', {'screen': '00-today', 'capability': 'CRO.pdp.diagnose', 'choice': 'agent', 'reason': 'x' * 400, 'autonomy': 'founder_gate'})
        self.assertEqual(status, 201, body)
        row = body['decision']
        self.assertEqual(len(row['reason']), 300)
        self.assertTrue(row['time'].endswith('Z'))
        self.assertEqual(row['autonomy'], 'founder_gate')
        self.assertEqual(self.call('/api/decisions', 'POST', {'screen': '00-today', 'capability': 'x', 'choice': 'maybe'})[0], 400)
        self.assertEqual(self.call('/api/decisions', 'POST', {'screen': '../etc', 'capability': 'x', 'choice': 'agent'})[0], 400)
        self.assertEqual(self.call('/api/decisions', 'POST', {'screen': '00-today', 'capability': '', 'choice': 'agent'})[0], 400)
        status, body = self.call('/api/decisions?screen=00-today')
        self.assertEqual(status, 200)
        self.assertGreaterEqual(body['total'], 1)
        self.assertEqual(body['decisions'][-1]['capability'], 'CRO.pdp.diagnose')
        self.assertEqual(self.call('/api/decisions?screen=05-brand-brain')[1]['total'], 0)
        on_disk = json.loads((self.tmp / 'decisions.json').read_text(encoding='utf-8'))
        self.assertEqual(on_disk[-1]['choice'], 'agent')

    def test_screen_api(self):
        status, body = self.call('/api/00-today/echo?q=7', 'POST', {'a': 1})
        self.assertEqual(status, 200, body)
        self.assertEqual(body, {'method': 'POST', 'path': ['echo'], 'q': '7', 'body': {'a': 1}, 'brand': 'Tallgrass Goods', 'orders': 2})
        self.assertEqual(self.call('/api/00-today/teapot')[0], 418)
        status, body = self.call('/api/00-today/other')
        self.assertEqual(status, 500)
        self.assertIn('boom', body['error'])
        self.assertEqual(self.call('/api/01-market-research/x')[0], 404)
        self.assertEqual(self.call('/api/nothing')[0], 404)

    def test_bad_body(self):
        req = urllib.request.Request(f'http://127.0.0.1:{self.port}/api/decisions', data=b'{not json', method='POST')
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(req, timeout=5)
        self.assertEqual(ctx.exception.code, 400)


class ContractParsingTest(unittest.TestCase):
    def test_real_index_and_contract(self):
        self.assertEqual(len(server.read_index()), 28)
        metrics = server.read_metric_contract()
        self.assertGreaterEqual(len(metrics), 25)
        groups = {m['group'] for m in metrics}
        self.assertTrue(any(g.startswith('Pipeline') for g in groups))
        self.assertTrue(all(m['formula'] for m in metrics))

    def test_coerce(self):
        self.assertEqual(server._coerce('12'), 12)
        self.assertEqual(server._coerce('0.5'), 0.5)
        self.assertEqual(server._coerce('-3.25'), -3.25)
        self.assertIsNone(server._coerce(''))
        self.assertEqual(server._coerce('2026-09-01'), '2026-09-01')
        self.assertEqual(server._coerce('sku-001'), 'sku-001')


if __name__ == '__main__':
    unittest.main()
