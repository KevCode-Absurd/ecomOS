"""Local read-only gallery server.

Serves views computed from the cached snapshot and cached creative images on
127.0.0.1. It never reads credentials and never calls the Meta API. Images are
downloaded once from the CDN URL stored in the snapshot and then served from disk.

"/" serves the same web page as the shared claude.ai page (meta_gallery/web).
The old page stays at /old.

The only writes it accepts are team settings (targets, exclusion presets,
report branding) and team notes on ads, each saved to a local file after
validation. Every other write is rejected.
"""
import argparse
import base64
import json
import mimetypes
import re
import threading
import time
import urllib.request
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from . import ai
from . import products
from . import stock
from . import settings as settings_mod
from .snapshot import DATA
from .view import Engine, ViewError

STATIC = Path(__file__).resolve().parent / 'static'
WEB = Path(__file__).resolve().parent / 'web'
WEB_FILES = ('engine.js', 'app.js', 'insights.js', 'overview.js', 'lab.js', 'studio.js', 'sales.js', 'testlab.js', 'prodads.js', 'report.js', 'brandx.js', 'buyer.js', 'catalog.js')
COMPETITORS = DATA / 'competitors.json'
COMP_MEDIA = DATA / 'comp_media.json'
CATALOG = DATA / 'catalog.json'
CATALOG_IMAGES = DATA / 'catalog_images'
CATALOG_APPROVED = DATA / 'catalog_refresh' / 'approved.json'
CACHE = DATA / 'cache' / 'gallery.json'
IMAGES = DATA / 'images'
SAFE_ID = re.compile(r'^[0-9]{5,25}$')
MAX_BODY = 32_000
MAX_NOTES_BODY = 2_000_000
MAX_AI_BODY = 80_000
MAX_REF_BODY = 4_000_000     # AI routes that can carry one pasted reference image
MAX_REF_IMAGE = 2_500_000
DOCS = ('packs.json', 'playbook.json', 'tests.json', 'catalog_prompt.json', 'client_orders.json')
MAX_DOC = 1_500_000


class Gallery:
    def __init__(self, path=CACHE, settings_path=None, notes_path=None):
        self.path = Path(path)
        self.settings_path = settings_path
        self.notes_path = notes_path
        self._page = None
        self._mtime = None
        self._data = None
        self._engine = None
        self._views = OrderedDict()
        self._lock = threading.Lock()

    @property
    def data(self):
        mtime = self.path.stat().st_mtime
        if mtime != self._mtime:
            with self._lock:
                self._data = json.loads(self.path.read_text(encoding='utf-8'))
                self._engine = Engine(self._data)
                self._views.clear()
                self._page = None
                self._mtime = mtime
        return self._data

    def page_json(self):
        """data.json for the web page: the cache without Meta CDN links."""
        from .share import page_data
        self.data
        with self._lock:
            if self._page is None:
                self._page = json.dumps(page_data(self._data), ensure_ascii=False, separators=(',', ':')).encode('utf-8')
            return self._page

    def notes(self):
        return settings_mod.load_notes(self.notes_path)

    def save_notes(self, body):
        return settings_mod.save_notes(body, self.notes_path)

    @property
    def engine(self):
        self.data
        return self._engine

    def settings(self):
        return settings_mod.load(self.settings_path)

    def save_settings(self, body):
        out = settings_mod.save(body, self.settings_path)
        with self._lock:
            self._views.clear()
        return out

    def meta(self):
        e = self.engine
        return {'meta': self.data['meta'], 'campaigns': e.campaigns(), 'settings': self.settings()}

    def view(self, since, until, keywords, campaign_ids):
        targets = self.settings()['targets']
        e = self.engine
        key = (since, until, tuple(keywords), tuple(sorted(campaign_ids)), targets['roas'], targets['cpa'], self._mtime)
        with self._lock:
            if key in self._views:
                self._views.move_to_end(key)
                return self._views[key]
        v = e.view(since, until, keywords, campaign_ids, targets)
        with self._lock:
            self._views[key] = v
            while len(self._views) > 32:
                self._views.popitem(last=False)
        return v

    def ad(self, ad_id):
        return self.data['ads'].get(ad_id)

    def ad_detail(self, ad_id, since, until, keywords, campaign_ids):
        return self.engine.ad_detail(ad_id, since, until, self.settings()['targets'], keywords, campaign_ids)


def image_path(creative):
    key = creative.get('image_hash') or f"creative_{creative.get('id')}"
    return IMAGES / f'{key}.jpg'


def cache_image(creative, timeout=10):
    """Download the creative's display image once. Returns the local path or None."""
    url = creative.get('display_image_url') or creative.get('image_url') or creative.get('thumbnail_url')
    return download(url, image_path(creative), timeout)


def cache_card(card, timeout=10):
    """Download one carousel card image once."""
    if not card.get('image_hash'):
        return None
    return download(card.get('image_url'), IMAGES / f"{card['image_hash']}.jpg", timeout)


_FAILED = {}           # path -> time of last failed download
RETRY_AFTER = 600      # seconds before a failed image is tried again


def download(url, path, timeout=10):
    if path.exists() and path.stat().st_size > 0:
        return path
    if not url or not url.startswith('https://'):
        return None
    # A failed image is not retried on every page load, so one bad link cannot hold the page up.
    if time.time() - _FAILED.get(str(path), 0) < RETRY_AFTER:
        return None
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'ecomOS-gallery/0.2'})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read()
    except Exception:
        body = None
    if not body:
        _FAILED[str(path)] = time.time()
        return None
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(body)
    return path


def image_bytes(ad):
    """The ad's cached image as (bytes, media type), downloading it once if needed."""
    path = cache_image(ad['creative']) if ad else None
    if not path:
        return None, None
    data = path.read_bytes()
    kind = 'image/png' if data[:8] == b'\x89PNG\r\n\x1a\n' else 'image/webp' if data[8:12] == b'WEBP' else 'image/jpeg'
    return data, kind


_COMP_MEDIA = {'mtime': None, 'data': {}}


def comp_image(ad_id):
    """A competitor ad image from the saved Ad Library snapshot, as JPEG bytes (or None)."""
    ad_id = str(ad_id or '')
    if not SAFE_ID.match(ad_id) or not COMP_MEDIA.is_file():
        return None
    mtime = COMP_MEDIA.stat().st_mtime
    if _COMP_MEDIA['mtime'] != mtime:
        try:
            _COMP_MEDIA['data'] = json.loads(COMP_MEDIA.read_text(encoding='utf-8'))
        except ValueError:
            _COMP_MEDIA['data'] = {}
        _COMP_MEDIA['mtime'] = mtime
    item = _COMP_MEDIA['data'].get(ad_id) or {}
    try:
        return base64.b64decode(item['img']) if item.get('img') else None
    except (ValueError, TypeError):
        return None


def pasted_image(value):
    """A reference image pasted in the page: base64 JPEG, PNG or WebP, size-capped. Returns bytes or None."""
    if not isinstance(value, str) or not value:
        return None
    if value.startswith('data:'):
        value = value.split(',', 1)[-1]
    try:
        data = base64.b64decode(value, validate=True)
    except (ValueError, TypeError):
        raise ValueError('The pasted image could not be read.')
    if len(data) > MAX_REF_IMAGE:
        raise ValueError('The pasted image is too large.')
    if not (data[:3] == b'\xff\xd8\xff' or data[:8] == b'\x89PNG\r\n\x1a\n' or data[8:12] == b'WEBP'):
        raise ValueError('The pasted file is not a JPEG, PNG or WebP image.')
    return data


_CATALOG = {'mtime': None, 'data': {}}


def catalog_item(code):
    """A best seller from catalog.json (read-only copy of the Meta catalog for the top 100)."""
    if not CATALOG.is_file() or not ai.SAFE_CODE.match(str(code)):
        return None
    mtime = CATALOG.stat().st_mtime
    if _CATALOG['mtime'] != mtime:
        try:
            _CATALOG['data'] = {p['code']: p for p in json.loads(CATALOG.read_text(encoding='utf-8')).get('products', [])}
        except (ValueError, KeyError, TypeError):
            _CATALOG['data'] = {}
        _CATALOG['mtime'] = mtime
    return _CATALOG['data'].get(str(code))


def catalog_image(code):
    """The product's current catalog image, downloaded once from the Gehna CDN."""
    item = catalog_item(code)
    url = item and item.get('image_url')
    if not url or not url.startswith('https://cdn-assets.gehnaindia.com/'):
        return None
    for ext in ('jpg', 'png', 'webp'):
        path = CATALOG_IMAGES / f'{code}.{ext}'
        if path.is_file() and path.stat().st_size:
            return path
    try:
        data = products._photo_bytes(url)
    except products.ProductError:
        data = None
    if not data:
        return None
    ext = {'image/jpeg': 'jpg', 'image/png': 'png', 'image/webp': 'webp'}[products.image_kind(data)]
    CATALOG_IMAGES.mkdir(parents=True, exist_ok=True)
    path = CATALOG_IMAGES / f'{code}.{ext}'
    path.write_bytes(data)
    return path


TYPE_WORDS = [('earring', 'Earrings'), ('jhumk', 'Earrings'), ('chain', 'Chains'), ('necklace', 'Chains'), ('bracelet', 'Bracelets'),
              ('bangle', 'Bracelets'), ('pendant', 'Pendants'), ('ring', 'Rings'), ('nose', 'Nosepins')]


def typecat(name):
    n = str(name).lower()
    return next((c for w, c in TYPE_WORDS if w in n), 'Other')


def load_approved():
    try:
        return json.loads(CATALOG_APPROVED.read_text(encoding='utf-8'))
    except (FileNotFoundError, ValueError):
        return {}


def save_approved(body):
    """body: {code, file}. file null clears it. Only files that exist are accepted."""
    code, name = str(body.get('code') or ''), body.get('file')
    if not catalog_item(code):
        raise ValueError('Unknown product.')
    data = load_approved()
    if name:
        if not ai.catalog_image_path(code, str(name)):
            raise ValueError('Unknown image.')
        data[code] = str(name)
    else:
        data.pop(code, None)
    CATALOG_APPROVED.parent.mkdir(parents=True, exist_ok=True)
    CATALOG_APPROVED.write_text(json.dumps(data, indent=1), encoding='utf-8')
    return {'approved': data}


def catalog_csv():
    """Approved images as a list to upload by hand: the catalog id and the local file to host and link."""
    import csv
    import io
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(['id', 'title', 'current_image_link', 'new_image_file', 'link'])
    for code, name in sorted(load_approved().items()):
        item = catalog_item(code) or {}
        w.writerow([code, item.get('name', ''), item.get('image_url', ''), f'data/meta-gallery/catalog_refresh/{code}/{name}', item.get('url', '')])
    return buf.getvalue()


def save_doc(name, body):
    """Team documents written by the page (copy packs, playbook, test tracker): any JSON object, size-capped."""
    if name not in DOCS or not isinstance(body, dict):
        raise ValueError('Bad document.')
    path = DATA / name
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(body, ensure_ascii=False, indent=1), encoding='utf-8')
    tmp.replace(path)
    return {'saved': name}


def query_filters(qs):
    since = (qs.get('since') or [None])[0]
    until = (qs.get('until') or [None])[0]
    kw = [k for part in qs.get('kw', []) for k in part.split(',')]
    camps = [c for part in qs.get('camp', []) for c in part.split(',') if SAFE_ID.match(c)]
    return since, until, kw, camps


def make_handler(gallery):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            pass

        def send_json(self, obj, status=200):
            body = json.dumps(obj, ensure_ascii=False).encode('utf-8')
            self.send_response(status)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Cache-Control', 'no-store')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def send_bytes(self, body, ctype, cache='no-cache'):
            self.send_response(200)
            self.send_header('Content-Type', ctype)
            self.send_header('Cache-Control', cache)
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def send_file(self, path, cache='no-cache'):
            body = path.read_bytes()
            self.send_response(200)
            self.send_header('Content-Type', mimetypes.guess_type(str(path))[0] or 'application/octet-stream')
            self.send_header('Cache-Control', cache)
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            url = urlparse(self.path)
            parts = [p for p in url.path.split('/') if p]
            qs = parse_qs(url.query)
            try:
                if not parts:
                    page = (WEB / 'index.html').read_text(encoding='utf-8')
                    doc = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
                           '<meta name="viewport" content="width=device-width, initial-scale=1"></head><body>'
                           + page + '</body></html>')
                    return self.send_bytes(doc.encode('utf-8'), 'text/html; charset=utf-8')
                if len(parts) == 1 and parts[0] in WEB_FILES:
                    return self.send_bytes((WEB / parts[0]).read_bytes(), 'text/javascript; charset=utf-8')
                if parts == ['data.json']:
                    return self.send_bytes(gallery.page_json(), 'application/json; charset=utf-8')
                if parts == ['thumbs.json']:
                    # No embedded previews locally; the page loads each image from /img/<ad id>.
                    return self.send_json({'error': 'not used locally'}, 404)
                if parts == ['settings.json']:
                    return self.send_json(gallery.settings())
                if parts == ['notes.json']:
                    return self.send_json(gallery.notes())
                if parts == ['competitors.json']:
                    if COMPETITORS.is_file():
                        return self.send_file(COMPETITORS)
                    return self.send_json({'error': 'not found'}, 404)
                if len(parts) == 1 and parts[0] in DOCS + ('brand.json', 'sales.json', 'comp_media.json', 'catalog.json', 'geo.json', 'traffic.json', 'stock.json'):
                    path = DATA / parts[0]
                    return self.send_file(path) if path.is_file() else self.send_json({})
                if parts == ['breakdowns.json']:
                    return self.send_json(ai.load_breakdowns())
                if parts == ['api', 'ai-status']:
                    return self.send_json(ai.status())
                if len(parts) == 3 and parts[:2] == ['api', 'variants'] and SAFE_ID.match(parts[2]):
                    return self.send_json(ai.list_variants(parts[2]))
                if len(parts) == 3 and parts[0] == 'variants':
                    path = ai.variant_path(parts[1], parts[2])
                    if path:
                        return self.send_file(path, cache='max-age=86400')
                    return self.send_json({'error': 'not found'}, 404)
                if parts == ['api', 'product']:
                    name = (qs.get('name') or [''])[0][:200]
                    code = (qs.get('code') or [''])[0][:60]
                    try:
                        meta = products.product(name, code, refresh=(qs.get('refresh') or [''])[0] == '1')
                    except products.ProductError as e:
                        return self.send_json({'error': str(e)}, 502)
                    meta = dict(meta, photos=[dict(ph, src=f"/product-photo/{meta['slug']}/{ph['file']}") for ph in meta.get('photos', [])])
                    return self.send_json({'product': meta, 'ads': ai.list_product_ads(meta['slug'])})
                if len(parts) == 3 and parts[0] == 'product-photo':
                    path = products.photo_path(parts[1], parts[2])
                    return self.send_file(path, cache='max-age=86400') if path else self.send_json({'error': 'not found'}, 404)
                if len(parts) == 3 and parts[0] == 'product-ads':
                    path = ai.product_ad_path(parts[1], parts[2])
                    return self.send_file(path, cache='max-age=86400') if path else self.send_json({'error': 'not found'}, 404)
                if len(parts) == 2 and parts[0] == 'catalog-image':
                    path = catalog_image(parts[1])
                    return self.send_file(path, cache='max-age=3600') if path else self.send_json({'error': 'image unavailable'}, 404)
                if parts == ['api', 'catalog-refresh']:
                    return self.send_json({'made': ai.list_catalog_images(), 'approved': load_approved(), 'default_prompt': ai.CATALOG_PROMPT,
                                           'styles': {k: {'name': v[0], 'prompt': v[1]} for k, v in ai.CATALOG_STYLES.items()}})
                if len(parts) == 3 and parts[0] == 'catalog-refresh':
                    path = ai.catalog_image_path(parts[1], parts[2])
                    return self.send_file(path, cache='max-age=86400') if path else self.send_json({'error': 'not found'}, 404)
                if len(parts) == 3 and parts[:2] == ['api', 'product-story']:
                    return self.send_json(ai.list_story(parts[2]))
                if len(parts) == 3 and parts[0] == 'product-story':
                    path = ai.story_path(parts[1], parts[2])
                    return self.send_file(path, cache='max-age=86400') if path else self.send_json({'error': 'not found'}, 404)
                if parts == ['api', 'catalog-export.csv']:
                    return self.send_bytes(catalog_csv().encode('utf-8'), 'text/csv; charset=utf-8')
                if parts == ['old']:
                    return self.send_file(STATIC / 'index.html')
                if parts == ['report']:
                    return self.send_file(STATIC / 'report.html')
                if parts[0] == 'static' and len(parts) == 2 and re.match(r'^[\w.-]+$', parts[1]):
                    path = STATIC / parts[1]
                    return self.send_file(path) if path.is_file() else self.send_json({'error': 'not found'}, 404)
                if parts == ['api', 'meta']:
                    return self.send_json(gallery.meta())
                if parts == ['api', 'view']:
                    return self.send_json(gallery.view(*query_filters(qs)))
                if parts == ['api', 'settings']:
                    return self.send_json(gallery.settings())
                if len(parts) == 3 and parts[:2] == ['api', 'ad'] and SAFE_ID.match(parts[2]):
                    ad = gallery.ad_detail(parts[2], *query_filters(qs))
                    return self.send_json(ad) if ad else self.send_json({'error': 'not found'}, 404)
                if len(parts) == 2 and parts[0] == 'img' and SAFE_ID.match(parts[1]):
                    ad = gallery.ad(parts[1])
                    path = cache_image(ad['creative']) if ad else None
                    if path:
                        return self.send_file(path, cache='max-age=86400')
                    return self.send_json({'error': 'image unavailable'}, 404)
                if len(parts) == 3 and parts[0] == 'card' and SAFE_ID.match(parts[1]) and parts[2].isdigit():
                    ad = gallery.ad(parts[1])
                    cards = ad['creative'].get('cards') or [] if ad else []
                    idx = int(parts[2])
                    path = cache_card(cards[idx]) if idx < len(cards) else None
                    if path:
                        return self.send_file(path, cache='max-age=86400')
                    return self.send_json({'error': 'image unavailable'}, 404)
                return self.send_json({'error': 'not found'}, 404)
            except ViewError as e:
                return self.send_json({'error': str(e)}, 400)
            except FileNotFoundError:
                return self.send_json({'error': 'Gallery cache missing. Run: python -m meta_gallery.snapshot'}, 503)

        def do_POST(self):
            url = urlparse(self.path)
            savers = {'/api/settings': (gallery.save_settings, MAX_BODY),
                      '/api/save/settings.json': (gallery.save_settings, MAX_BODY),
                      '/api/save/notes.json': (gallery.save_notes, MAX_NOTES_BODY),
                      '/api/breakdown': (self.ai_breakdown, MAX_AI_BODY),
                      '/api/variants': (self.ai_variants, MAX_REF_BODY),
                      '/api/ask': (self.ai_ask, MAX_REF_BODY),
                      '/api/competitor-variants': (self.ai_competitor, MAX_REF_BODY),
                      '/api/product-ads': (self.ai_product_ads, MAX_REF_BODY),
                      '/api/catalog-premium': (self.ai_catalog_premium, MAX_AI_BODY),
                      '/api/catalog-approve': (save_approved, MAX_BODY),
                      '/api/product-story': (self.ai_product_story, MAX_AI_BODY),
                      '/api/stock-check': (lambda body: stock.run(limit=min(int(body.get('limit') or 150), 300)), MAX_BODY)}
            for doc in DOCS:
                savers['/api/save/' + doc] = ((lambda d: lambda body: save_doc(d, body))(doc), MAX_DOC)
            if url.path not in savers:
                return self.send_json({'error': 'read-only'}, 405)
            save, limit = savers[url.path]
            # Only same-origin JSON from the local page. This blocks other websites posting here.
            origin = self.headers.get('Origin')
            host = self.headers.get('Host', '')
            if host.split(':')[0] not in ('127.0.0.1', 'localhost') or (origin and origin != f'http://{host}'):
                return self.send_json({'error': 'forbidden origin'}, 403)
            if (self.headers.get('Content-Type') or '').split(';')[0].strip() != 'application/json':
                return self.send_json({'error': 'JSON only'}, 415)
            length = int(self.headers.get('Content-Length') or 0)
            if not 0 < length <= limit:
                return self.send_json({'error': 'body too large or empty'}, 413)
            try:
                body = json.loads(self.rfile.read(length).decode('utf-8'))
                return self.send_json(save(body))
            except (ai.AIError, products.ProductError) as e:
                return self.send_json({'error': str(e)}, 502)
            except (ValueError, UnicodeDecodeError, TypeError) as e:
                return self.send_json({'error': str(e)}, 400)

        def ai_breakdown(self, body):
            """body: {ad_id, facts}. facts is the ad data the page shows (same as the shared page sends Claude)."""
            ad_id = str(body.get('ad_id') or '')
            ad = gallery.ad(ad_id) if SAFE_ID.match(ad_id) else None
            if not ad:
                raise ValueError('Unknown ad.')
            facts = body.get('facts') if isinstance(body.get('facts'), dict) else {}
            data, kind = image_bytes(ad)
            result = ai.breakdown(facts, data, kind or 'image/jpeg')
            return ai.save_breakdown(ad_id, result)

        def ai_ask(self, body):
            prompt = body.get('prompt')
            if not isinstance(prompt, str) or not 20 <= len(prompt) <= 70_000:
                raise ValueError('Bad prompt.')
            ad_id = str(body.get('image_ad_id') or '')
            data, kind = image_bytes(gallery.ad(ad_id)) if SAFE_ID.match(ad_id) else (None, None)
            ref = pasted_image(body.get('ref_image')) or comp_image(body.get('comp_ad_id'))
            if ref:
                data = [(data, kind or 'image/jpeg'), (ref, 'image/jpeg')] if data else [(ref, 'image/jpeg')]
            return {'json': ai.ask_json(prompt, data, kind or 'image/jpeg')}

        def ai_competitor(self, body):
            base_id = str(body.get('base_ad_id') or '')
            ad = gallery.ad(base_id) if SAFE_ID.match(base_id) else None
            if not ad:
                raise ValueError('Unknown ad.')
            comp = body.get('comp') if isinstance(body.get('comp'), dict) else {}
            facts = body.get('facts') if isinstance(body.get('facts'), dict) else {}
            data, kind = image_bytes(ad)
            made = ai.make_competitor_variants(base_id, comp, facts, data, ai.load_breakdowns().get(base_id), body.get('n', 3),
                                               body.get('size', 'square'), body.get('quality', 'medium'), media_type=kind or 'image/jpeg',
                                               ref_bytes=pasted_image(body.get('ref_image')) or comp_image(comp.get('ad_id')))
            return {'made': made, 'base_ad_id': base_id}

        def ai_variants(self, body):
            ad_id = str(body.get('ad_id') or '')
            ad = gallery.ad(ad_id) if SAFE_ID.match(ad_id) else None
            if not ad:
                raise ValueError('Unknown ad.')
            data, kind = image_bytes(ad)
            bd = ai.load_breakdowns().get(ad_id)
            facts = body.get('facts') if isinstance(body.get('facts'), dict) else {}
            facts.setdefault('headline', ad['creative'].get('headline') or '')
            facts.setdefault('primary_text', (ad['creative'].get('primary_text') or '')[:1200])
            made = ai.make_variants(ad_id, facts, data, bd, body.get('n', 3), body.get('size', 'square'), body.get('quality', 'medium'),
                                    media_type=kind or 'image/jpeg', ref_bytes=pasted_image(body.get('ref_image')),
                                    ref_role='product' if body.get('ref_role') == 'product' else 'layout')
            return {'made': made, 'all': ai.list_variants(ad_id)}

        def ai_product_ads(self, body):
            """body: {name, code, picks, facts, n, size, quality, ref_image | ref_ad_id, sold, copy_only}.
            Photos come from the product's page on gehnaindia.com. The style reference is a pasted image or one of the account's ads."""
            name = str(body.get('name') or '')[:200]
            if not name.strip():
                raise ValueError('Pick a product.')
            meta = products.product(name, str(body.get('code') or '')[:60])
            picks = [int(x) for x in body.get('picks') or [] if isinstance(x, int) and 1 <= x <= products.MAX_PHOTOS]
            photos = products.photo_bytes(meta['slug'], picks)
            ref = pasted_image(body.get('ref_image'))
            ref_id = str(body.get('ref_ad_id') or '')
            if not ref and SAFE_ID.match(ref_id):
                ref, _ = image_bytes(gallery.ad(ref_id))
            # facts: the page facts the user kept ticked (default all). Only text, size-capped.
            picked = body.get('facts')
            facts = [str(x)[:400] for x in picked if isinstance(x, str)][:40] if isinstance(picked, list) else [x['text'] for x in meta.get('facts', [])]
            p = dict(meta, sold=str(body.get('sold') or '')[:160], facts=facts)
            n = max(1, min(5, int(body.get('n') or 4)))
            size = body.get('size') if body.get('size') in ai.SIZES else 'square'
            if body.get('copy_only'):
                return {'copy': ai.product_copy(p, n, photos, ref, size), 'slug': meta['slug']}
            made = ai.make_product_ads(p, photos, n, size, body.get('quality', 'medium'), ref,
                                       extra={'ref_ad_id': ref_id if SAFE_ID.match(ref_id) and not body.get('ref_image') else ''})
            return {'made': made, 'all': ai.list_product_ads(meta['slug']), 'slug': meta['slug']}

        def ai_catalog_premium(self, body):
            """body: {code, prompt, quality, size}. Makes 1 premium version of the product's current catalog image."""
            code = str(body.get('code') or '')
            path = catalog_image(code)
            if not path:
                raise ValueError('The catalog image for this product could not be loaded.')
            made = ai.make_catalog_image(code, path.read_bytes(), str(body.get('prompt') or ''), body.get('quality', 'high'),
                                           size=str(body.get('size') or 'square'))
            return {'made': made, 'all': ai.list_catalog_images().get(code, [])}

        def ai_product_story(self, body):
            """body: {code, n, size, quality}. The product's photos and page facts come from its page on the website."""
            item = catalog_item(str(body.get('code') or ''))
            if not item or not item.get('url'):
                raise ValueError('This product is not in the catalog list.')
            slug = item['url'].rstrip('/').split('/')[-1]
            meta = products.product(item.get('name') or slug, item['code'], slug=slug)
            p = dict(meta, facts=meta.get('facts') or [], cat=typecat(item.get('name') or ''))
            made = ai.make_story(p, products.photo_bytes(meta['slug']), body.get('n', 10), body.get('size', 'square'), body.get('quality', 'medium'))
            return {'made': made, 'all': ai.list_story(meta['slug']), 'slug': meta['slug']}

        def reject(self):
            self.send_json({'error': 'read-only'}, 405)

        do_PUT = do_DELETE = do_PATCH = reject

    return Handler


def prefetch_images(gallery, workers=8):
    """Download every creative and carousel card image, 8 at a time."""
    jobs = {}
    for ad in gallery.data['ads'].values():
        c = ad['creative']
        jobs.setdefault(str(image_path(c)), (cache_image, c))
        for card in c.get('cards') or []:
            if card.get('image_hash'):
                jobs.setdefault(card['image_hash'], (cache_card, card))
    todo = list(jobs.values())
    ok = missing = 0
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for i, result in enumerate(pool.map(lambda job: job[0](job[1]), todo), 1):
            if result:
                ok += 1
            else:
                missing += 1
            if i % 50 == 0 or i == len(todo):
                print(f'{i}/{len(todo)} checked', flush=True)
    print(f'Images cached: {ok}. Unavailable: {missing}.')
    return ok, missing


def main(argv=None):
    parser = argparse.ArgumentParser(description='Serve the local Meta ad gallery.')
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--prefetch-images', action='store_true', help='Download all creative images, then exit.')
    args = parser.parse_args(argv)
    gallery = Gallery()
    if args.prefetch_images:
        prefetch_images(gallery)
        return
    server = ThreadingHTTPServer(('127.0.0.1', args.port), make_handler(gallery))
    print(f'Gallery running at http://127.0.0.1:{args.port}  (Ctrl+C to stop)')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
