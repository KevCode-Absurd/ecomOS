"""Stock check: is each best seller (and each piece a live ad shows) still sold on gehnaindia.com?

The Meta catalog marks every item "in stock", so it cannot tell. The product page can: it says ready
stock or made to order, gives a delivery date, and a removed piece has no page. This reads the pages
(read only), then writes data/meta-gallery/stock.json for the page:

    python -m meta_gallery.stock            # the top 100 sellers in catalog.json, plus pieces live ads name

Status per product: ready (ready stock), made (made to order), out (the page says it cannot be bought),
gone (no product page), unknown (the page did not say). Runs on the computer that runs the gallery.
"""
import argparse
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from . import products
from .snapshot import DATA

STOCK = DATA / 'stock.json'
OUT_KEYS = re.compile(r'(in_stock|is_saleable|is_available|available_for_sale|is_purchasable)$', re.I)


def _flags(obj):
    """Stock-like fields on the page's product and variation, e.g. {'is_in_stock': False}."""
    out = {}
    for k, v in (obj or {}).items():
        if isinstance(v, (bool, int, float)) and not isinstance(v, bool) and re.search(r'(stock|qty|quantity|inventory)', k, re.I):
            out[k] = v
        elif isinstance(v, bool) and re.search(r'(stock|saleable|available|purchasable|sold_out|out_of)', k, re.I):
            out[k] = v
        elif isinstance(v, str) and re.search(r'stock_status|availability', k, re.I):
            out[k] = v[:40]
    return out


def status_from_page(html, code='', today=None):
    """(status, info) from a product page's HTML."""
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.S)
    if not m:
        return 'gone', {}
    try:
        state = json.loads(m.group(1))['props']['pageProps']['initialApolloState']
    except (ValueError, KeyError, TypeError):
        return 'unknown', {}
    items = [v for k, v in state.items() if k.startswith('ProductType:') and isinstance(v, dict)]
    if not items:
        return 'gone', {}
    want = products.base_code(code)
    p = next((x for x in items if want and products.base_code(x.get('product_code')) == want), None) or items[0]
    var = p.get('variation') or {}
    var = state.get(var.get('__ref'), {}) if isinstance(var, dict) and var.get('__ref') else var
    flags = {**_flags(p), **{'variation.' + k: v for k, v in _flags(var).items()}}
    order = [n.lower() for n in products._names(state, p.get('order_type'))]
    days = None
    rng = p.get('expected_delivery_date_range') or []
    if rng:
        try:
            days = int(round((time.mktime(time.strptime(rng[-1], '%Y-%m-%d')) - time.mktime(time.strptime(today or time.strftime('%Y-%m-%d'), '%Y-%m-%d'))) / 86400))
        except (ValueError, TypeError):
            days = None
    price = var.get('special_price') or var.get('selling_price')
    info = {'order_type': order[0] if order else None, 'days': days, 'price': price if isinstance(price, (int, float)) else None,
            'ship_fast': bool(p.get('is_ship_fast_tag_applicable')), 'flags': flags, 'page_code': str(p.get('product_code') or '')}
    said_out = any((v is False and OUT_KEYS.search(k.split('.')[-1])) or (isinstance(v, str) and 'out' in v.lower()) for k, v in flags.items())
    if said_out:
        return 'out', info
    if order and order[0] == 'stock' or info['ship_fast']:
        return 'ready', info
    if order:
        return 'made', info
    return 'unknown', info


def check_one(item, today=None):
    url = item.get('url') or f"{products.SITE}/{products.slugify(item.get('name', ''))}"
    try:
        status_code, raw = products._get(url, 'text/html')
    except products.ProductError as e:
        return {**item, 'status': 'unknown', 'error': str(e)[:120], 'url': url}
    if status_code == 404:
        return {**item, 'status': 'gone', 'url': url}
    if status_code != 200 or not raw:
        return {**item, 'status': 'unknown', 'error': f'HTTP {status_code}', 'url': url}
    st, info = status_from_page(raw.decode('utf-8', 'replace'), item.get('code', ''), today)
    return {**item, 'status': st, 'url': url, **info}


def targets(catalog, ads=None):
    """Top sellers from catalog.json, then pieces named by live ads (from data.json ads) not already in."""
    out, seen = [], set()
    for p in catalog.get('products', []):
        if p.get('code') and p['code'] not in seen:
            seen.add(p['code'])
            out.append({'code': p['code'], 'name': p.get('name', ''), 'url': p.get('url'), 'rank': len(out) + 1})
    for a in (ads or []):
        if a.get('code') and a['code'] not in seen:
            seen.add(a['code'])
            out.append({'code': a['code'], 'name': a.get('name', ''), 'url': a.get('url'), 'rank': None, 'from_ad': a.get('ad_id')})
    return out


def run(catalog_path=None, out=None, limit=None, workers=6, today=None, check=check_one):
    catalog = json.loads(Path(catalog_path or DATA / 'catalog.json').read_text(encoding='utf-8'))
    items = targets(catalog)[:limit] if limit else targets(catalog)
    with ThreadPoolExecutor(max_workers=workers) as ex:
        rows = list(ex.map(lambda it: check(it, today), items))
    doc = {'checked_at': time.strftime('%Y-%m-%dT%H:%M:%S'), 'source': 'gehnaindia.com product pages, read only',
           'counts': {s: sum(1 for r in rows if r['status'] == s) for s in ('ready', 'made', 'out', 'gone', 'unknown')},
           'products': {r['code']: {k: r.get(k) for k in ('name', 'url', 'rank', 'status', 'days', 'price', 'order_type', 'error')} for r in rows}}
    path = Path(out or STOCK)
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding='utf-8')
    tmp.replace(path)
    return doc


def main(argv=None):
    ap = argparse.ArgumentParser(description='Check best sellers on gehnaindia.com and write stock.json.')
    ap.add_argument('--limit', type=int)
    args = ap.parse_args(argv)
    doc = run(limit=args.limit)
    print('Checked', sum(doc['counts'].values()), 'pieces:', ', '.join(f'{k} {v}' for k, v in doc['counts'].items()))


if __name__ == '__main__':
    main()
