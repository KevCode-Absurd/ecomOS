"""Data for the web page (local app and the shared claude.ai page).

`page_data(cache)` removes Meta CDN image links (they expire and carry
signed tokens) and returns what the page loads as data.json.

`python -m meta_gallery.share OUT_DIR` writes data.json and, when Pillow is
installed and images are cached, thumbs.json (small previews as base64) for
publishing the shared page.
"""
import argparse
import base64
import io
import json
from pathlib import Path

from .snapshot import DATA


def page_data(cache):
    out = json.loads(json.dumps(cache))
    for ad in out['ads'].values():
        c = ad['creative']
        c.pop('display_image_url', None)
        for card in c.get('cards') or []:
            card.pop('image_url', None)
    out['meta']['source'] = 'Meta Ads MCP connector, read-only (snapshot)' if 'MCP' in (out['meta'].get('source') or '') else out['meta'].get('source')
    return out


def thumbs(cache, image_path, size=360):
    try:
        from PIL import Image
    except ImportError:
        return None
    images, amap = {}, {}
    for ad_id, ad in cache['ads'].items():
        p = image_path(ad['creative'])
        if not p.exists():
            continue
        key = p.stem
        if key not in images:
            try:
                im = Image.open(p).convert('RGB')
            except Exception:
                continue
            im.thumbnail((size, size))
            buf = io.BytesIO()
            im.save(buf, 'JPEG', quality=64, optimize=True, progressive=True)
            images[key] = base64.b64encode(buf.getvalue()).decode()
        amap[ad_id] = key
    return {'ads': amap, 'images': images}


def main(argv=None):
    from .server import image_path
    parser = argparse.ArgumentParser(description='Write data files for the web page.')
    parser.add_argument('out_dir')
    args = parser.parse_args(argv)
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    cache = json.loads((DATA / 'cache' / 'gallery.json').read_text(encoding='utf-8'))
    (out / 'data.json').write_text(json.dumps(page_data(cache), ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    t = thumbs(cache, image_path)
    if t:
        (out / 'thumbs.json').write_text(json.dumps(t, separators=(',', ':')), encoding='utf-8')
    print('Wrote', out)


if __name__ == '__main__':
    main()
