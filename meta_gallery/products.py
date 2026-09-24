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
CACHE_DAYS = 1          # prices, stock and delivery dates change, so re-read the page daily


# Promises shown on every Gehna product page (trust strip and "about us" block), read on 24 Sep 2026.
# They are rendered by the site's scripts, so they are not in the page data. Update here if the site changes.
SITE_FACTS = [
    ('trust', 'BIS hallmarked gold'),
    ('trust', '100% natural gemstones'),
    ('trust', 'Lifetime exchange'),
    ('trust', '7 day return'),
    ('trust', '20+ years in business, 8,500+ happy customers, 20,000+ pieces shipped'),
]
DIAMOND_FACT = ('trust', 'Certified diamonds')


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


def _clean(text, n=300):
    text = re.sub(r'<[^>]+>', ' ', str(text or '')).replace('&nbsp;', ' ').replace('&amp;', '&')
    text = re.sub(r'\s+([.,!?;:])', r'\1', re.sub(r'\s+', ' ', text)).strip()
    return text if len(text) <= n else text[:n].rsplit(' ', 1)[0] + '...'


def _names(state, v):
    items = v if isinstance(v, list) else [v] if v else []
    out = []
    for x in items:
        x = state.get(x['__ref'], {}) if isinstance(x, dict) and x.get('__ref') else x
        if isinstance(x, dict) and x.get('name'):
            out.append(str(x['name']).strip())
    return out


def _money(v):
    return f'₹{int(round(v)):,}'


def page_facts(state, p, var, today=None):
    """Everything on the product page that can go into ads, as [{group, text}].
    Groups: product, price, delivery, proof, trust, faq, review, story."""
    f = []
    add = lambda g, t: t and f.append({'group': g, 'text': t})
    karat = _names(state, p.get('metal_karatage'))
    add('product', ', '.join(karat))
    if var.get('gold_weight'):
        add('product', f"Gold weight {var['gold_weight']} g net" + (f", gross weight {var['gross_weight']} g" if var.get('gross_weight') else ''))
    stones = _names(state, p.get('gemstone'))
    colours = [c for c in _names(state, p.get('gemstone_color')) if c.lower() != 'multicolor']
    if stones:
        add('product', 'Stones: ' + ', '.join(stones) + (f" ({', '.join(colours)})" if colours else '') + (f", {var['gem_stone_weight']} ct" if var.get('gem_stone_weight') else ''))
    if var.get('diamond_weight') or _names(state, p.get('diamond_shape')):
        add('product', 'Diamonds: ' + ', '.join(filter(None, [f"{var['diamond_weight']} ct" if var.get('diamond_weight') else '',
                                                              *_names(state, p.get('diamond_quality')), *_names(state, p.get('diamond_shape'))])))
    length = _names(state, p.get('product_length'))
    add('product', f"Length {length[0]}" if length else '')
    others = [k.get('metal_karatage') for k in p.get('metal_karatages') or [] if isinstance(k, dict) and not k.get('selected') and k.get('metal_karatage')]
    add('product', f"Also made in {', '.join(others)}" if others else '')
    order = _names(state, p.get('order_type'))
    add('product', 'Ready stock' if order and order[0].lower() == 'stock' else 'Made to order' if order else '')
    price = var.get('special_price') or var.get('selling_price')
    if isinstance(price, (int, float)):
        add('price', f"Price {_money(price)}, inclusive of all taxes")
    emi = [e for e in var.get('emi_table') or [] if isinstance(e, dict) and e.get('no_of_month')]
    if emi:
        e = max(emi, key=lambda x: x['no_of_month'])
        add('price', f"EMI: {_money(e['down_payment'])} down, then {_money(e['emi_amount'])} a month for {e['no_of_month']} months" if e.get('down_payment') else f"EMI up to {e['no_of_month']} months")
    rng = p.get('expected_delivery_date_range') or []
    if rng and today:
        try:
            days = (time.mktime(time.strptime(rng[-1], '%Y-%m-%d')) - time.mktime(time.strptime(today, '%Y-%m-%d'))) / 86400
            add('delivery', f"Delivered in about {int(round(days))} days, fully insured" if 0 < days <= 15 else '')
        except (ValueError, TypeError):
            pass
    if p.get('is_ship_fast_tag_applicable'):
        add('delivery', 'Ships fast (in stock)')
    if p.get('is_stock_available_at_gehna_store'):
        add('delivery', 'Available to see and pick up at the Gehna store in Chennai')
    badge = _clean((p.get('social_badge') or {}).get('value'), 60)
    add('proof', f"Site badge: {badge.capitalize()}" if badge else '')
    gr = (state.get('ROOT_QUERY') or {}).get('googleReview') or {}
    if gr.get('averageRating') and gr.get('totalReviewCount'):
        add('proof', f"Rated {gr['averageRating']} out of 5 from {gr['totalReviewCount']} Google reviews of the store")
    has_diamond = any(x['text'].startswith('Diamonds') for x in f)
    for g, t in SITE_FACTS + ([DIAMOND_FACT] if has_diamond else []):
        add(g, t)
    for q in p.get('frequent_questions') or []:
        if isinstance(q, dict) and q.get('question') and q.get('answer'):
            add('faq', f"{_clean(q['question'], 120)} {_clean(q['answer'], 260)}")
    for r in (gr.get('reviews') or [])[:12]:
        if isinstance(r, dict) and r.get('starRating') == 'FIVE' and len(_clean(r.get('comment'), 400)) >= 40:
            add('review', 'A store review: "' + _clean(r['comment'], 200) + '"')
        if sum(1 for x in f if x['group'] == 'review') >= 3:
            break
    add('story', _clean(p.get('description'), 700))
    return f


def parse_product(html, want_code='', today=None):
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
        'facts': page_facts(state, p, var, today or time.strftime('%Y-%m-%d')),
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
    """Product facts and local photo files for a product name. Cached for a day."""
    slug = slugify(name)
    if not SAFE_SLUG.match(slug):
        raise ProductError('This product name cannot be turned into a page address.')
    root = Path(folder or PRODUCTS) / slug
    meta_path = root / 'product.json'
    if not refresh and meta_path.is_file() and time.time() - meta_path.stat().st_mtime < CACHE_DAYS * 86400:
        try:
            meta = json.loads(meta_path.read_text(encoding='utf-8'))
            if 'facts' in meta and all((root / f['file']).is_file() for f in meta.get('photos', [])):
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
