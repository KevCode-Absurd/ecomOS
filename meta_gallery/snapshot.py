"""Build the gallery cache from a read-only Meta capture.

Input: a raw capture JSON (data/meta-gallery/raw/*.json) holding Meta read
responses. Output: data/meta-gallery/cache/gallery.json.

Capture version 2 holds one year of data:
  ads        one row per ad that spent in the window (names, campaign, creative id, totals)
  daily      ad x day rows: spend, purchases, purchase value, impressions, link clicks
  monthly    ad x calendar month rows for age, gender and publisher_platform
  creatives, videos, images, adsets   creative and ad set details

The cache keeps daily rows per ad so the local server can total any date range
without calling Meta. The browser only ever reads data through the local server.
"""
import argparse
import json
from collections import defaultdict
from datetime import date, datetime, timezone
from pathlib import Path

from .metrics import num
from .themes import tag

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'data' / 'meta-gallery'
FORMATS = ['static_image', 'video', 'carousel', 'catalog_dynamic', 'unconfirmed_mixed']
TYPE_LABELS = {
    'all': 'All formats',
    'static_image': 'Single image',
    'video': 'Video',
    'carousel': 'Carousel',
    'catalog_dynamic': 'Catalog',
    'unconfirmed_mixed': 'Flexible / mixed',
    'unknown': 'Creative type not retrieved',
}
TYPE_NOTES = {
    'video': 'Video ad. Meta returns only a 160px video thumbnail here. Use "Watch video" to see it.',
    'carousel': 'Carousel ad. Every card is listed below. Metrics cover the whole ad, not single cards.',
    'catalog_dynamic': ('Catalog ad. Meta picks products from the catalog for each viewer, so no single image '
                        'represents it. The picture is a small Meta thumbnail.'),
    'unconfirmed_mixed': ('Flexible or mixed-media ad. Meta did not expose one image or video for it and may rotate '
                          'several assets. The picture is a small Meta thumbnail.'),
}
BREAKDOWN_DIMS = ['age', 'gender', 'publisher_platform']


def rows(block):
    if block is None:
        return []
    if isinstance(block, dict):
        for key in ('ad_entities', 'ad_creatives', 'ad_videos', 'ad_images'):
            if key in block:
                block = block[key]
                break
        else:
            return []
    if isinstance(block, str):
        block = json.loads(block)
    return block


def classify(creative):
    if not creative:
        return 'unknown'
    if creative.get('product_set_id'):
        return 'catalog_dynamic'
    if creative.get('video_id') or creative.get('object_type') == 'VIDEO':
        return 'video'
    if creative.get('child_attachments'):
        return 'carousel'
    if creative.get('image_hash'):
        return 'static_image'
    return 'unconfirmed_mixed'


def day_index(since, iso):
    return (date.fromisoformat(iso) - date.fromisoformat(since)).days


def build(capture):
    if capture.get('version') != 2:
        raise ValueError('This builder needs a version 2 capture (one year of daily rows).')
    window = capture['window']
    creatives = {c['id']: c for c in rows(capture.get('creatives'))}
    videos = {v['id']: v for v in rows(capture.get('videos'))}
    images = {i['hash']: i for i in rows(capture.get('images'))}
    adsets = {a['id']: a for a in rows(capture.get('adsets'))}
    account_rows = rows(capture.get('account'))
    account = account_rows[0] if account_rows else {}

    ads = {}
    missing = []
    for r in rows(capture['ads']):
        if (num(r.get('amount_spent')) or 0) <= 0:
            continue
        if r.get('creative_id') not in creatives:
            missing.append(r['id'])
        ads[r['id']] = _ad_record(r['id'], r, creatives, adsets, videos, images)
        ads[r['id']]['tags'] = tag(ads[r['id']])
    if missing:
        raise ValueError(f'Creative details missing for ads that spent: {missing}')

    daily = defaultdict(list)
    seen = set()
    n_days = day_index(window['since'], window['until']) + 1
    for r in rows(capture['daily']):
        key = (r['id'], r['date_start'])
        if key in seen or r['id'] not in ads:
            continue
        seen.add(key)
        d = day_index(window['since'], r['date_start'])
        if not 0 <= d < n_days:
            continue
        daily[r['id']].append([d, num(r.get('amount_spent')) or 0.0, num(r.get('omni_purchase')),
                               num(r.get('omni_purchase_values')), num(r.get('impressions')) or 0.0,
                               num(r.get('link_click')) or 0.0])
    for v in daily.values():
        v.sort()

    # Video rows: [day, spend, impressions, 3s plays (derived), thruplays, p25, p50, p75, p100, watch seconds, starts]
    video = defaultdict(list)
    seen = set()
    for r in rows(capture.get('video_daily')):
        key = (r['id'], r['date_start'])
        if key in seen or r['id'] not in ads:
            continue
        seen.add(key)
        d = day_index(window['since'], r['date_start'])
        if not 0 <= d < n_days:
            continue
        spend = num(r.get('amount_spent')) or 0.0
        cpv = num(r.get('cost_per_video_view'))
        starts = num(r.get('video_play_actions')) or 0.0
        avg = num(r.get('video_avg_time_watched_actions'))
        video[r['id']].append([d, spend, num(r.get('impressions')) or 0.0,
                               round(spend / cpv, 1) if cpv else 0.0,  # no cost per 3s play means no 3s plays
                               num(r.get('video_thruplay_watched_actions')) or 0.0,
                               num(r.get('video_p25_watched_actions')) or 0.0, num(r.get('video_p50_watched_actions')) or 0.0,
                               num(r.get('video_p75_watched_actions')) or 0.0, num(r.get('video_p100_watched_actions')) or 0.0,
                               avg * starts if avg is not None else None, starts])
    for v in video.values():
        v.sort()

    monthly = {}
    buckets = set()
    for dim in BREAKDOWN_DIMS:
        per_ad = defaultdict(list)
        seen = set()
        for r in rows((capture.get('monthly') or {}).get(dim)):
            key = (r['id'], r['date_start'], r.get(dim))
            if key in seen or r['id'] not in ads:
                continue
            seen.add(key)
            buckets.add((r['date_start'], r['date_stop']))
            per_ad[r['id']].append([r['date_start'], r['date_stop'], r.get(dim) or 'unknown',
                                    num(r.get('amount_spent')) or 0.0, num(r.get('omni_purchase')),
                                    num(r.get('omni_purchase_values'))])
        monthly[dim] = dict(per_ad)

    return {
        'meta': {
            'version': 2,
            'account_id': capture['ad_account_id'],
            'account_name': account.get('name'),
            'currency': (account.get('amount_spent') or {}).get('unit') or 'INR',
            'timezone': account.get('timezone_name'),
            'captured_at': capture['captured_at'],
            'built_at': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'source': capture['source'],
            'window': window,
            'account_spend_check': capture.get('account_spend_check'),
            'breakdown_buckets': [list(b) for b in sorted(buckets)],
            'collection_rule': ('Each view shows up to 30 ads ranked by spend in the selected dates, either across all '
                                'formats or within one format. Paused and inactive ads are included when they spent.'),
            'attribution_note': ('Metrics are Meta defaults for each ad set attribution setting '
                                 '(shown per ad). No attribution override was applied.'),
            'formats': ['all'] + FORMATS,
            'format_labels': {k: TYPE_LABELS[k] for k in ['all'] + FORMATS},
        },
        'ads': ads,
        'daily': dict(daily),
        'video': dict(video),
        'monthly': monthly,
    }


def _ad_record(ad_id, row, creatives, adsets, videos, images):
    c = creatives.get(row.get('creative_id'), {})
    ctype = classify(c)
    adset = adsets.get(row.get('adset_id'), {})
    flags = []
    if ctype in TYPE_NOTES:
        flags.append(TYPE_NOTES[ctype])
    if adset.get('is_dynamic_creative'):
        flags.append('Ad set uses dynamic creative. The asset shown may not be the only one delivered.')
    if 'dynamic' in (row.get('campaign_name') or '').lower() and ctype == 'static_image' and not adset.get('is_dynamic_creative'):
        flags.append('Campaign name says "Dynamic", but Meta reports the ad set does not use dynamic creative '
                     'and the creative has one image. Treated as a single image.')

    video = videos.get(c.get('video_id')) if c.get('video_id') else None
    cards = []
    for a in c.get('child_attachments') or []:
        img = images.get(a.get('image_hash')) or {}
        cards.append({'headline': a.get('name'), 'description': (a.get('description') or '').strip() or None,
                      'link': a.get('link'), 'cta': a.get('call_to_action_type'),
                      'image_hash': a.get('image_hash'), 'image_url': img.get('url')})

    if ctype == 'static_image':
        display, quality = c.get('image_url'), 'full'
    elif ctype == 'carousel' and cards and cards[0]['image_url']:
        display, quality = cards[0]['image_url'], 'full'
    elif video and video.get('picture'):
        display, quality = video['picture'], 'thumbnail_160'
    else:
        display, quality = c.get('thumbnail_url'), 'thumbnail_64'

    story = c.get('effective_object_story_id')
    links = [x['link'] for x in cards if x.get('link')]
    return {
        'id': ad_id,
        'name': row.get('name'),
        'effective_status': row.get('effective_status'),
        'status': row.get('status'),
        'campaign_id': row.get('campaign_id'),
        'campaign_name': row.get('campaign_name'),
        'adset_id': row.get('adset_id'),
        'adset_name': row.get('adset_name'),
        'attribution_setting': adset.get('attribution_setting'),
        'is_dynamic_creative': adset.get('is_dynamic_creative'),
        'flags': flags,
        'creative': {
            'id': c.get('id', row.get('creative_id')),
            'type': ctype,
            'type_label': TYPE_LABELS[ctype],
            'name': c.get('name'),
            'image_hash': c.get('image_hash') if ctype == 'static_image' else None,
            'display_image_url': display,
            'display_quality': quality,
            'primary_text': c.get('body'),
            'headline': c.get('title'),
            'cta': c.get('call_to_action_type'),
            'link_url': c.get('link_url') or (links[0] if links and len(set(links)) == 1 else None),
            'cards': cards,
            'video_id': c.get('video_id'),
            'video': ({'length': video.get('length'), 'title': video.get('title'),
                       'url': 'https://www.facebook.com' + video['permalink_url'] if video.get('permalink_url') else None}
                      if video else None),
            'product_set_id': c.get('product_set_id'),
            'object_story_id': story,
            'post_url': f'https://www.facebook.com/{story}' if story else None,
        },
    }


def newest_capture():
    files = sorted((DATA / 'raw').glob('*.json'), key=lambda p: p.stat().st_mtime)
    for f in reversed(files):
        try:
            with f.open(encoding='utf-8') as fh:
                head = fh.read(200)
        except OSError:
            continue
        if '"version": 2' in head or '"version":2' in head:
            return f
    raise SystemExit('No version 2 raw capture found in data/meta-gallery/raw')


def main(argv=None):
    parser = argparse.ArgumentParser(description='Build the Meta gallery cache from a raw capture.')
    parser.add_argument('capture', nargs='?', help='Raw capture JSON (default: newest version 2 file in data/meta-gallery/raw)')
    parser.add_argument('--out', default=str(DATA / 'cache' / 'gallery.json'))
    args = parser.parse_args(argv)
    path = Path(args.capture) if args.capture else newest_capture()
    snapshot = build(json.loads(path.read_text(encoding='utf-8')))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(snapshot, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    w = snapshot['meta']['window']
    spend = sum(r[1] for v in snapshot['daily'].values() for r in v)
    print(f'Built from {path.name}')
    print(f"{w['since']} to {w['until']}: {len(snapshot['ads'])} ads with spend, total spend {spend:,.2f}")
    print(f'Wrote {out}')


if __name__ == '__main__':
    main()
