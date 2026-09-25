"""Value rules data: which buyers are worth more, with sale campaigns taken out.

Meta value rules let a Sales ad set bid more or less for a group of people (age, gender, location,
operating system, device, placement and more) without excluding anyone. The Next moves tab suggests a
rule set from 90 days of results. Sale, festival offer and countdown campaigns sold on the discount, so
they are kept apart and taken out on the page (all minus sale).

Input: campaign level insight rows for the last 90 days with one of these breakdowns:
  age + gender, publisher_platform + platform_position, impression_device.
Each row: {campaign name, spend, purchases, purchase value, and the breakdown keys}.

    python -m meta_gallery.valuerules ROWS.json [--since D --until D]    # writes data/meta-gallery/valuerules.json
"""
import argparse
import json
import re
from pathlib import Path

from .snapshot import DATA

OUT = DATA / 'valuerules.json'
# Same words as SALE_RE in web/app.js. Navratna is a jewellery style, not a sale.
SALE_RE = re.compile(r'\b(sale|sales campaign|pre[- ]?sale|bfcm|black ?friday|cyber ?monday|eoss|end of season|clearance|deal of the day|'
                     r'[1-9]\d ?% ?off|discount|coupon|countdown|\d+ (hours?|days?) (left|to go)|last \d+ (hours?|days?)|'
                     r'akshaya tritiya|navratri|navaratri|diwali|dhanteras|raksha ?bandhan|rakhi)\b', re.I)


def is_sale(name):
    return bool(SALE_RE.search(name or ''))


def _num(x):
    if isinstance(x, dict):
        x = x.get('value')
    try:
        return float(x or 0)
    except (TypeError, ValueError):
        return 0.0


def key_of(r):
    if 'age' in r and 'gender' in r:
        return 'ag', f"{r['gender']}|{r['age']}"
    if 'publisher_platform' in r:
        return 'pl', f"{r['publisher_platform']}|{r.get('platform_position', '')}"
    if 'impression_device' in r:
        return 'dev', r['impression_device']
    return None, None


def build(rows, since=None, until=None):
    seg = {'ag': {}, 'pl': {}, 'dev': {}}
    sale_names = set()
    for r in rows:
        dim, k = key_of(r)
        if not dim:
            continue
        cell = seg[dim].setdefault(k, {'all': [0, 0, 0], 'sale': [0, 0, 0]})
        s = _num(r.get('amount_spent', r.get('spend'))); p = int(_num(r.get('omni_purchase', r.get('purchases'))))
        v = _num(r.get('omni_purchase_values', r.get('purchase_value')))
        parts = ['all'] + (['sale'] if is_sale(r.get('name') or r.get('campaign_name')) else [])
        if len(parts) == 2:
            sale_names.add(r.get('name') or r.get('campaign_name'))
        for part in parts:
            c = cell[part]
            c[0] = round(c[0] + s, 2); c[1] += p; c[2] = round(c[2] + v, 2)
    return {'version': 1, 'window': {'since': since, 'until': until}, 'source': 'Meta Ads Manager, read-only',
            'note': 'all = whole account; sale = campaigns named as a sale, festival offer or countdown. The page uses all minus sale.',
            'sale_campaigns': sorted(sale_names), 'segments': seg}


def main(argv=None):
    ap = argparse.ArgumentParser(description='Build valuerules.json from campaign level breakdown rows.')
    ap.add_argument('rows')
    ap.add_argument('--since')
    ap.add_argument('--until')
    a = ap.parse_args(argv)
    rows = json.loads(Path(a.rows).read_text(encoding='utf-8'))
    doc = build(rows, a.since, a.until)
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding='utf-8')
    print('Wrote', OUT, '-', len(doc['sale_campaigns']), 'sale campaigns kept apart')


if __name__ == '__main__':
    main()
