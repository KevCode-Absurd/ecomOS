"""Product pages and photos from gehnaindia.com, for building ads of best-selling pieces.

Read-only: it only GETs public product pages and their photos, and caches them under
data/products/<slug>/. The page URL is the product name as a slug (checked against the
product code on the page). Nothing is ever posted to the site.
"""
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

from .snapshot import DATA

SITE = 'https://www.gehnaindia.com'
PRODUCTS = DATA / 'products'
SAFE_SLUG = re.compile(r'^[a-z0-9][a-z0-9-]{1,120}$')
MAX_PHOTOS = 4
MAX_PAGE = 3_000_000
MAX_PHOTO = 6_000_000
UA = 'Mozilla/5.0 (ecomOS gallery; read-only)'
CACHE_DAYS = 7


class ProductError(Exception):
    """A message that is safe to show in the page."""


def slugify(name):
    """Gehna's product URL: lower case, no brackets part, words joined by hyphens."""
    s = str(name or '').lower().replace('&', ' ')
    s = re.sub(r'\(.*?\)', ' ', s)
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s


def base_code(code):
    """GHCSRG-6538_17 and GHCSRG-6538 are the same piece in different sizes."""
    return str(code or '').strip().upper().split('_')[0]


def image_kind(data):
    if data[:3] == b'\xff\xd8\xff':
        return 'image/jpeg'
    if data[:8] == b'\x89PNG\r\n\x1a\n':
        return 'image/png'
    if data[8:12] == b'WEBP':
        return 'image/webp'
    return None


def _get(url, accept='*/*', limit=MAX_PAGE, timeout=20):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': accept})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read(limit + 1)
    except urllib.error.HTTPError as e:
        return e.code, b''
    except Exception as e:  # network, DNS, timeout
        raise ProductError(f'Could not reach gehnaindia.com: {getattr(e, "reason", e)}') from None


def parse_product(html, want_code=''):
    """The product from a Gehna product page (Next.js data). Returns a dict or None."""
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.S)
    if not m:
        return None
    try:
        state = json.loads(m.group(1))['props']['pageProps']['initialApolloState']
    except (ValueError, KeyError, TypeError):
        return None
    products = [v for k, v in state.items() if k.startswith('ProductType:') and isinstance(v, dict)]
    if not products:
        return None
    want = base_code(want_code)
    p = next((x for x in products if want and base_code(x.get('product_code')) == want), None) or products[0]
    var = p.get('variation') or {}
    var = state.get(var.get('__ref'), {}) if isinstance(var, dict) and var.get('__ref') else var
    photos = []
    for pic in p.get('as_website_pictures') or []:
        if isinstance(pic, dict) and pic.get('asset_type', 'image') == 'image':
            url = pic.get('large') or pic.get('original') or pic.get('medium')
            if isinstance(url, str) and url.startswith('https://'):
                photos.append({'url': url, 'thumb': pic.get('medium') or pic.get('thumb') or url})
    if not photos and isinstance(p.get('avatar_url'), str) and p['avatar_url'].startswith('https://'):
        photos.append({'url': p['avatar_url'], 'thumb': p['avatar_url']})
    price = var.get('special_price') or var.get('selling_price')
    return {
        'name': str(p.get('name') or '').strip(),
        'code': str(p.get('product_code') or ''),
        'code_match': bool(want) and base_code(p.get('product_code')) == want,
        'slug': str(p.get('slug') or ''),
        'price': price if isinstance(price, (int, float)) else None,
        'description': re.sub(r'\s+', ' ', str(p.get('description') or ''))[:900],
        'badge': re.sub(r'<[^>]+>', '', str((p.get('social_badge') or {}).get('value') or '')),
        'emi_months': max([e.get('no_of_month') or 0 for e in var.get('emi_table') or [] if isinstance(e, dict)] or [0]) or None,
        'photos': photos[:MAX_PHOTOS],
    }


def _photo_bytes(url):
    """One product photo as JPEG, PNG or WebP bytes. The CDN may send AVIF, so fall back to the
    site's own image resizer, which converts to WebP or JPEG."""
    status, data = _get(url, 'image/webp,image/jpeg,image/png;q=0.9,*/*;q=0.5', MAX_PHOTO)
    if status == 200 and data and len(data) <= MAX_PHOTO and image_kind(data):
        return data
    proxy = f"{SITE}/_next/image?url={urllib.parse.quote(url, safe='')}&w=1080&q=85"
    status, data = _get(proxy, 'image/webp,image/jpeg', MAX_PHOTO)
    if status == 200 and data and len(data) <= MAX_PHOTO and image_kind(data):
        return data
    return None


def product(name, code='', folder=None, refresh=False):
    """Product facts and local photo files for a product name. Cached for a week."""
    slug = slugify(name)
    if not SAFE_SLUG.match(slug):
        raise ProductError('This product name cannot be turned into a page address.')
    root = Path(folder or PRODUCTS) / slug
    meta_path = root / 'product.json'
    if not refresh and meta_path.is_file() and time.time() - meta_path.stat().st_mtime < CACHE_DAYS * 86400:
        try:
            meta = json.loads(meta_path.read_text(encoding='utf-8'))
            if all((root / f['file']).is_file() for f in meta.get('photos', [])):
                return meta
        except (ValueError, KeyError, TypeError):
            pass
    # A 14K sale is usually listed under the 18K page of the same design.
    for page_slug in dict.fromkeys([slug, slug.replace('-14k-', '-18k-')]):
        status, raw = _get(f'{SITE}/{page_slug}', 'text/html')
        if status == 200 and raw:
            break
    else:
        raise ProductError(f'No product page found at gehnaindia.com/{slug}.')
    info = parse_product(raw.decode('utf-8', 'replace'), code)
    if not info:
        raise ProductError('The product page did not have product data.')
    root.mkdir(parents=True, exist_ok=True)
    photos = []
    for i, ph in enumerate(info['photos']):
        data = _photo_bytes(ph['url'])
        if not data:
            continue
        ext = {'image/jpeg': 'jpg', 'image/png': 'png', 'image/webp': 'webp'}[image_kind(data)]
        name_ = f'{i + 1}.{ext}'
        (root / name_).write_bytes(data)
        photos.append({'file': name_, 'kind': image_kind(data)})
    meta = {**{k: v for k, v in info.items() if k != 'photos'}, 'slug': slug, 'url': f'{SITE}/{page_slug}',
            'photos': photos, 'fetched': time.strftime('%Y-%m-%d %H:%M')}
    meta_path.write_text(json.dumps(meta, ensure_ascii=False), encoding='utf-8')
    return meta


def photo_path(slug, file, folder=None):
    if not SAFE_SLUG.match(str(slug)) or not re.match(r'^[1-9]\.(jpg|png|webp)$', str(file)):
        return None
    p = Path(folder or PRODUCTS) / slug / file
    return p if p.is_file() else None


def photo_bytes(slug, picks=None, folder=None):
    """[(bytes, media type)] for the chosen photos (1-based file order), all photos if none chosen."""
    meta_path = Path(folder or PRODUCTS) / str(slug) / 'product.json'
    if not SAFE_SLUG.match(str(slug)) or not meta_path.is_file():
        return []
    meta = json.loads(meta_path.read_text(encoding='utf-8'))
    out = []
    for i, ph in enumerate(meta.get('photos', [])):
        if picks and (i + 1) not in picks:
            continue
        p = photo_path(slug, ph['file'], folder)
        if p:
            out.append((p.read_bytes(), ph.get('kind') or 'image/jpeg'))
    return out[:3]
