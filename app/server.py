"""ecomOS local server: one process, one data layer, one folder per screen.

Read-only against the outside world. It binds 127.0.0.1 only, reads no
credentials and calls no external API. The only file it writes is
`data/decisions.json` (the founder's choices on action buttons).

Run from anywhere:  python app/server.py [--port 8770]
Then open           http://127.0.0.1:8770

Routes
  GET  /                              the shell (web/index.html): nav across screens
  GET  /web/<file>                    ui-kit.css, ui-kit.js, charts.js, shell.js, kit.html (the kit demo)
  GET  /screens/<slug>/               that screen's index.html (renders inside the shell)
  GET  /screens/<slug>/<file>         screen.js, screen.css, fixtures/<name>.json
  GET  /api/screens                   the 28 screens from screens/INDEX.md, with built flags
  GET  /api/brand                     data/sample-brand/brand.json
  GET  /api/tables                    tables present in data/sample-brand/ with row counts
  GET  /api/tables/<name>?limit=N     rows of one table (JSON or CSV on disk)
  GET  /api/metrics                   metric names and groups from contracts/metrics.md
  GET  /api/metrics/pipeline?window=28d the pipeline group, 4 trailing windows (optional device=)
  GET  /api/metrics/<name>?window=28d one metric via metrics.py: window=Nd, end=YYYY-MM-DD, plus the
                                      filters that metric takes (device, channel, by, page, variant)
  GET  /api/decisions?screen=<slug>   the decisions log
  POST /api/decisions                 append one decision {screen, capability, choice, reason}
  ANY  /api/<slug>/...                handed to screens/<slug>/api.py: handle(req)

A screen's api.py exposes `handle(req)`. `req` has method, path (list of parts
after /api/<slug>), query (dict of lists), body (parsed JSON or None), slug and
`data` (the Data layer: brand, table(name), tables(), metric(name, **kw)).
It returns a JSON-able object for 200, or a (status, object) pair.
"""
import argparse
import csv
import importlib.util
import json
import mimetypes
import re
import sys
import threading
import time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

APP = Path(__file__).resolve().parent
WEB = APP / 'web'
SCREENS = APP / 'screens'
DATA = APP / 'data'
SAMPLE = DATA / 'sample-brand'
CONTRACTS = APP / 'contracts'
DECISIONS = DATA / 'decisions.json'

SAFE_SLUG = re.compile(r'^[0-9]{2}-[a-z0-9-]{2,40}$')
SAFE_FILE = re.compile(r'^[A-Za-z0-9_.-]{1,80}$')
SAFE_NAME = re.compile(r'^[a-z0-9_]{1,40}$')
WEB_FILES = ('index.html', 'shell.js', 'ui-kit.css', 'ui-kit.js', 'charts.js', 'kit.html')
SCREEN_FILES = ('index.html', 'screen.js', 'screen.css')
CHOICES = ('agent', 'person', 'not_now')
MAX_BODY = 32_000
MAX_DECISIONS = 20_000


def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


# ---------------------------------------------------------------- screens

def read_index():
    """The screen list from screens/INDEX.md: folder, room, purpose, in file order."""
    rows = []
    path = SCREENS / 'INDEX.md'
    if not path.is_file():
        return rows
    for line in path.read_text(encoding='utf-8').splitlines():
        if not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) < 3 or cells[0] in ('Folder', '') or set(cells[0]) <= set('-: '):
            continue
        slug = cells[0].strip('`')
        if not SAFE_SLUG.match(slug):
            continue
        rows.append({'slug': slug, 'room': cells[1], 'purpose': cells[2]})
    return rows


def screens_list():
    out = []
    for row in read_index():
        folder = SCREENS / row['slug']
        out.append(dict(row, built=(folder / 'index.html').is_file(), api=(folder / 'api.py').is_file()))
    return out


# ---------------------------------------------------------------- metric contract

def read_metric_contract():
    """Metric names and their group from contracts/metrics.md (first column of each table)."""
    path = CONTRACTS / 'metrics.md'
    metrics, group = [], ''
    if not path.is_file():
        return metrics
    for line in path.read_text(encoding='utf-8').splitlines():
        if line.startswith('## '):
            group = line[3:].strip()
            continue
        if not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) < 2 or cells[0] == 'Metric' or set(cells[0]) <= set('-: '):
            continue
        for name in cells[0].split(','):
            name = name.strip().strip('`')
            if SAFE_NAME.match(name):
                metrics.append({'name': name, 'group': group, 'formula': cells[1]})
    return metrics


# ---------------------------------------------------------------- data layer

def _coerce(value):
    if value is None or value == '':
        return None
    if value in ('true', 'false'):
        return value == 'true'
    try:
        if re.fullmatch(r'-?\d+', value):
            return int(value)
        if re.fullmatch(r'-?\d*\.\d+(e-?\d+)?', value, re.I):
            return float(value)
    except (TypeError, ValueError):
        pass
    return value


class Data:
    """Reads the sample brand's tables from disk, cached by mtime.

    A table is `data/sample-brand/<name>.json` (a list, or an object with a
    `rows` list) or `<name>.csv` (numeric strings coerced, blanks to null).
    Missing tables raise KeyError so a metric can say unavailable, never 0.
    """

    def __init__(self, folder=SAMPLE):
        self.folder = Path(folder)
        self._cache = {}
        self._lock = threading.Lock()
        self._metrics_mod = None
        self._metrics_mtime = None

    @property
    def brand(self):
        return self._load(self.folder / 'brand.json')

    def _load(self, path):
        mtime = path.stat().st_mtime
        with self._lock:
            hit = self._cache.get(path)
            if hit and hit[0] == mtime:
                return hit[1]
        if path.suffix == '.json':
            value = json.loads(path.read_text(encoding='utf-8'))
        else:
            with path.open(encoding='utf-8', newline='') as fh:
                value = [{k: _coerce(v) for k, v in row.items()} for row in csv.DictReader(fh)]
        with self._lock:
            self._cache[path] = (mtime, value)
        return value

    def table_path(self, name):
        if not SAFE_NAME.match(name) or name == 'brand':
            return None
        for ext in ('.json', '.csv'):
            path = self.folder / (name + ext)
            if path.is_file():
                return path
        return None

    def table(self, name):
        path = self.table_path(name)
        if path is None:
            raise KeyError(name)
        value = self._load(path)
        if isinstance(value, dict) and isinstance(value.get('rows'), list):
            return value['rows']
        if isinstance(value, list):
            return value
        raise ValueError(f'table {name} is not a list of rows')

    def tables(self):
        out = []
        for path in sorted(self.folder.glob('*')):
            if path.suffix not in ('.json', '.csv') or path.stem == 'brand' or not SAFE_NAME.match(path.stem):
                continue
            try:
                rows = self.table(path.stem)
                out.append({'name': path.stem, 'rows': len(rows), 'format': path.suffix[1:]})
            except (ValueError, json.JSONDecodeError):
                out.append({'name': path.stem, 'rows': None, 'format': path.suffix[1:], 'error': 'unreadable'})
        return out

    def meta(self, name):
        """Where a table came from and when: the JSON header, or its row in the tables.json manifest."""
        path = self.table_path(name)
        if path is None:
            raise KeyError(name)
        value = self._load(path)
        if isinstance(value, dict):
            return {k: v for k, v in value.items() if k != 'rows' and not isinstance(v, (list, dict))}
        try:
            manifest = self.table('tables')
        except (KeyError, ValueError):
            return {}
        row = next((r for r in manifest if isinstance(r, dict) and r.get('table') == name), {})
        return {k: row[k] for k in ('source', 'captured_at', 'shaped_like', 'rows') if k in row}

    def _metrics(self):
        """metrics.py next to server.py, reloaded when it changes. None if it is missing."""
        path = APP / 'metrics.py'
        if not path.is_file():
            return None
        mtime = path.stat().st_mtime
        if self._metrics_mod is None or mtime != self._metrics_mtime:
            self._metrics_mod = load_module('ecomos_metrics', path)
            self._metrics_mtime = mtime
        return self._metrics_mod

    def metric(self, name, **kw):
        """One metric from the contract: value, window, freshness, formula, or unavailable with reason."""
        contract = {m['name']: m for m in read_metric_contract()}
        if name not in contract:
            raise KeyError(name)
        mod = self._metrics()
        base = {'metric': name, 'group': contract[name]['group'], 'formula': contract[name]['formula']}
        if mod is None or not hasattr(mod, 'compute'):
            return dict(base, value=None, unavailable=True,
                        reason='metrics.py is not built yet (Phase A session 3)', fix='app/metrics.py')
        result = mod.compute(name, self, **kw)
        return dict(base, **result) if isinstance(result, dict) else dict(base, value=result)

    def pipeline(self, **kw):
        """The Pipeline group of the contract, 4 trailing windows each. Bad query values raise ValueError."""
        names = [m['name'] for m in read_metric_contract() if m['group'].startswith('Pipeline')]
        mod = self._metrics()
        if mod is None or not hasattr(mod, 'pipeline'):
            return {'unavailable': True, 'reason': 'metrics.py is missing', 'fix': 'app/metrics.py', 'metrics': []}
        return mod.pipeline(self, names, **kw)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------- decisions

class Decisions:
    """Append-only log at data/decisions.json: {screen, capability, choice, reason, time}."""

    def __init__(self, path=DECISIONS):
        self.path = Path(path)
        self._lock = threading.Lock()

    def read(self):
        if not self.path.is_file():
            return []
        try:
            rows = json.loads(self.path.read_text(encoding='utf-8'))
        except json.JSONDecodeError:
            return []
        return rows if isinstance(rows, list) else []

    @staticmethod
    def validate(body):
        if not isinstance(body, dict):
            raise ValueError('body must be an object')
        screen = str(body.get('screen') or '')
        capability = str(body.get('capability') or '').strip()
        choice = str(body.get('choice') or '')
        reason = str(body.get('reason') or '').strip()[:300]
        if not SAFE_SLUG.match(screen):
            raise ValueError('screen must be a screen folder name like 00-today')
        if not capability or len(capability) > 80 or not re.fullmatch(r'[A-Za-z0-9_.:-]+', capability):
            raise ValueError('capability must be a capability id')
        if choice not in CHOICES:
            raise ValueError('choice must be one of ' + ', '.join(CHOICES))
        row = {'screen': screen, 'capability': capability, 'choice': choice, 'reason': reason, 'time': now_iso()}
        autonomy = body.get('autonomy')
        if autonomy in ('agent', 'founder_gate', 'human_assist'):
            row['autonomy'] = autonomy
        return row

    def append(self, body):
        row = self.validate(body)
        with self._lock:
            rows = self.read()
            if len(rows) >= MAX_DECISIONS:
                raise ValueError('decisions log is full')
            rows.append(row)
            self.path.parent.mkdir(parents=True, exist_ok=True)
            tmp = self.path.with_suffix('.json.tmp')
            tmp.write_text(json.dumps(rows, indent=1), encoding='utf-8')
            tmp.replace(self.path)
        return row


# ---------------------------------------------------------------- screen apis

class Request:
    def __init__(self, method, slug, path, query, body, data):
        self.method, self.slug, self.path, self.query, self.body, self.data = method, slug, path, query, body, data

    def arg(self, name, default=None):
        values = self.query.get(name)
        return values[0] if values else default


class ScreenApis:
    """Loads screens/<slug>/api.py on demand and reloads it when the file changes."""

    def __init__(self, root=SCREENS):
        self.root = Path(root)
        self._mods = {}
        self._lock = threading.Lock()

    def get(self, slug):
        path = self.root / slug / 'api.py'
        if not SAFE_SLUG.match(slug) or not path.is_file():
            return None
        mtime = path.stat().st_mtime
        with self._lock:
            hit = self._mods.get(slug)
            if hit and hit[0] == mtime:
                return hit[1]
            module = load_module('screen_api_' + slug.replace('-', '_'), path)
            self._mods[slug] = (mtime, module)
            return module


# ---------------------------------------------------------------- http

def make_handler(data, decisions, apis):
    class Handler(BaseHTTPRequestHandler):
        server_version = 'ecomOS/0.1'

        def log_message(self, fmt, *args):
            sys.stderr.write('%s %s\n' % (time.strftime('%H:%M:%S'), fmt % args))

        def send_bytes(self, body, ctype, status=200, cache='no-cache'):
            self.send_response(status)
            self.send_header('Content-Type', ctype)
            self.send_header('Cache-Control', cache)
            self.send_header('Content-Length', str(len(body)))
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.end_headers()
            if self.command != 'HEAD':
                self.wfile.write(body)

        def send_json(self, obj, status=200):
            self.send_bytes(json.dumps(obj, ensure_ascii=False, default=str).encode('utf-8'),
                            'application/json; charset=utf-8', status)

        def send_file(self, path, root):
            path = path.resolve()
            if root.resolve() not in path.parents or not path.is_file():
                return self.send_json({'error': 'not found'}, 404)
            ctype = mimetypes.guess_type(str(path))[0] or 'application/octet-stream'
            if ctype.startswith('text/') or ctype.endswith('javascript') or ctype.endswith('json'):
                ctype += '; charset=utf-8'
            return self.send_bytes(path.read_bytes(), ctype)

        def read_body(self):
            length = int(self.headers.get('Content-Length') or 0)
            if length > MAX_BODY:
                raise ValueError('body too large')
            raw = self.rfile.read(length) if length else b''
            return json.loads(raw.decode('utf-8')) if raw else None

        def route_api(self, method, parts, qs, body):
            if parts == ['screens']:
                return self.send_json({'screens': screens_list()})
            if parts == ['brand']:
                return self.send_json(data.brand)
            if parts == ['tables']:
                return self.send_json({'tables': data.tables()})
            if len(parts) == 2 and parts[0] == 'tables':
                try:
                    rows = data.table(parts[1])
                except KeyError:
                    return self.send_json({'error': 'table not found', 'table': parts[1], 'unavailable': True}, 404)
                except ValueError as exc:
                    return self.send_json({'error': str(exc)}, 500)
                limit = qs.get('limit', [''])[0]
                out = rows[:int(limit)] if limit.isdigit() else rows
                return self.send_json({'table': parts[1], 'total': len(rows), 'rows': out})
            if parts == ['metrics']:
                return self.send_json({'metrics': read_metric_contract(), 'engine': (APP / 'metrics.py').is_file()})
            if len(parts) == 2 and parts[0] == 'metrics':
                kw = {k: v[0] for k, v in qs.items() if SAFE_NAME.match(k)}
                try:
                    if parts[1] == 'pipeline':
                        return self.send_json(data.pipeline(**kw))
                    return self.send_json(data.metric(parts[1], **kw))
                except KeyError:
                    return self.send_json({'error': 'metric not in contract', 'metric': parts[1]}, 404)
                except ValueError as exc:
                    return self.send_json({'error': str(exc), 'metric': parts[1]}, 400)
            if parts == ['decisions']:
                if method == 'POST':
                    try:
                        return self.send_json({'ok': True, 'decision': decisions.append(body)}, 201)
                    except ValueError as exc:
                        return self.send_json({'error': str(exc)}, 400)
                rows = decisions.read()
                screen = qs.get('screen', [''])[0]
                if screen:
                    rows = [r for r in rows if r.get('screen') == screen]
                return self.send_json({'decisions': rows, 'total': len(rows)})
            if parts and SAFE_SLUG.match(parts[0]):
                module = apis.get(parts[0])
                if module is None or not hasattr(module, 'handle'):
                    return self.send_json({'error': 'this screen has no api.py yet', 'screen': parts[0]}, 404)
                result = module.handle(Request(method, parts[0], parts[1:], qs, body, data))
                if isinstance(result, tuple) and len(result) == 2:
                    return self.send_json(result[1], int(result[0]))
                return self.send_json(result)
            return self.send_json({'error': 'not found'}, 404)

        def route(self, method):
            url = urlparse(self.path)
            parts = [p for p in url.path.split('/') if p]
            qs = parse_qs(url.query)
            if any(p in ('.', '..') for p in parts):
                return self.send_json({'error': 'not found'}, 404)
            if parts and parts[0] == 'api':
                body = None
                if method == 'POST':
                    try:
                        body = self.read_body()
                    except (ValueError, json.JSONDecodeError) as exc:
                        return self.send_json({'error': 'bad body: ' + str(exc)}, 400)
                return self.route_api(method, parts[1:], qs, body)
            if method != 'GET':
                return self.send_json({'error': 'method not allowed'}, 405)
            if not parts:
                return self.send_file(WEB / 'index.html', WEB)
            if parts[0] == 'web' and len(parts) == 2 and parts[1] in WEB_FILES:
                return self.send_file(WEB / parts[1], WEB)
            if parts[0] == 'screens' and len(parts) >= 2 and SAFE_SLUG.match(parts[1]):
                root = apis.root
                folder = root / parts[1]
                rest = parts[2:]
                if not rest or rest == ['index.html']:
                    if not (folder / 'index.html').is_file():
                        return self.send_json({'error': 'screen not built yet', 'screen': parts[1]}, 404)
                    return self.send_file(folder / 'index.html', root)
                if len(rest) == 1 and rest[0] in SCREEN_FILES and SAFE_FILE.match(rest[0]):
                    return self.send_file(folder / rest[0], root)
                if len(rest) == 2 and rest[0] == 'fixtures' and SAFE_FILE.match(rest[1]) and rest[1].endswith(('.json', '.csv', '.png', '.jpg', '.svg', '.txt', '.md')):
                    return self.send_file(folder / 'fixtures' / rest[1], root)
            return self.send_json({'error': 'not found'}, 404)

        def do_GET(self):
            self.safe('GET')

        def do_HEAD(self):
            self.safe('GET')

        def do_POST(self):
            self.safe('POST')

        def safe(self, method):
            try:
                self.route(method)
            except BrokenPipeError:
                pass
            except Exception as exc:  # a screen's api.py may be mid-edit; keep the server up
                sys.stderr.write('error %s %s: %r\n' % (method, self.path, exc))
                try:
                    self.send_json({'error': exc.__class__.__name__ + ': ' + str(exc)}, 500)
                except Exception:
                    pass

    return Handler


def serve(port=8770, host='127.0.0.1'):
    data, decisions, apis = Data(), Decisions(), ScreenApis()
    httpd = ThreadingHTTPServer((host, port), make_handler(data, decisions, apis))
    built = sum(1 for s in screens_list() if s['built'])
    print(f'ecomOS on http://{host}:{port}  ({built} of {len(read_index())} screens built, brand: {data.brand.get("brand", "?")})')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()


def main(argv=None):
    ap = argparse.ArgumentParser(description='ecomOS local server (127.0.0.1 only)')
    ap.add_argument('--port', type=int, default=8770)
    args = ap.parse_args(argv)
    serve(args.port)


if __name__ == '__main__':
    main()
