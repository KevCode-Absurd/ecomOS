"""The web pass for a brand: the public read of its category (lanes, markets, preferences, launches) with a url and a date on
every number, kept as fixtures/web_pass/<brand>.json and read by the research desk.

    python3 app/screens/01-market-research/web_pass.py --brand tallgrass --init      # write a template to fill
    python3 app/screens/01-market-research/web_pass.py --brand tallgrass --check     # validate a filled file
    python3 app/screens/01-market-research/web_pass.py --brand bombas --check        # the legacy fixture checks too

No model and no network run here: a research session fills the template from public sources (research firms, press,
surveys, the brands' own sites), one url and one date per number, and the checker refuses a number without a source.
The desk reads the file only when its brand field matches the brand asked for.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WEB_PASS_DIR = HERE / 'fixtures' / 'web_pass'
LEGACY = HERE / 'fixtures' / 'market_trends.json'
KEY_RE = re.compile(r'^[a-z0-9_]{2,40}$')
DATE_RE = re.compile(r'^\d{4}(-\d{2}(-\d{2})?)?$')
DIRECTIONS = ('up', 'flat', 'down')
CHANNELS = ('dtc', 'wholesale', 'retail_store', 'marketplace', 'other')


def path_for(brand: str) -> Path:
    return WEB_PASS_DIR / f'{brand}.json'


def template(brand: str, category: str, today: dt.date | None = None) -> dict:
    today = today or dt.date.today()
    return {
        'brand': brand,
        'captured_at': today.isoformat(),
        'note': f'Public web pass for {brand} ({category}). Signals, not proof. Every number cites a url and a date. Market sizes vary by definition; treat as ranges. Fill every TODO or delete the entry; the checker refuses a number without a source.',
        'lanes': [
            {'key': 'TODO_lane_key', 'label': 'TODO Lane label', 'kind': 'product', 'terms': ['TODO words that name the lane in a title, an ad or a review']},
            {'key': 'guarantee', 'label': 'Guarantee and durability proof', 'kind': 'proof', 'terms': ['guarantee', 'lifetime', 'warranty', 'buy it for life']},
        ],
        'markets': [
            {'key': f'{category.lower().replace(" ", "_")}_us', 'label': f'US {category}', 'size_usd': None, 'size_year': None, 'cagr_pct': None, 'cagr_window': 'TODO 2026 to 2033',
             'series': [{'year': today.year - 1, 'value_usd': None}, {'year': today.year + 7, 'value_usd': None}], 'direction': 'up', 'drivers': ['TODO'],
             'sources': [{'url': 'TODO https://', 'publisher': 'TODO', 'date': 'TODO 2026', 'what': 'TODO what the page gives'}]},
        ],
        'preferences': [
            {'key': 'sustainability', 'label': 'Sustainability', 'direction': 'up', 'evidence': 'TODO the survey number in a sentence',
             'sources': [{'url': 'TODO https://', 'publisher': 'TODO', 'date': 'TODO 2026-01-01', 'what': 'TODO'}]},
        ],
        'launches': [
            {'brand': 'TODO competitor', 'what': 'TODO what launched', 'sub_category': 'TODO_lane_key', 'date': 'TODO 2026-01', 'price_usd': None, 'channel': 'dtc',
             'sources': [{'url': 'TODO https://', 'publisher': 'TODO', 'date': 'TODO 2026-01-01', 'what': 'TODO'}]},
        ],
    }


def _todo(x) -> bool:
    return isinstance(x, str) and x.strip().upper().startswith('TODO')


def check(doc: dict, brand: str | None = None) -> list[str]:
    """Every problem in a web pass file, in plain words. Empty means the desk can read it."""
    errs: list[str] = []
    if not isinstance(doc, dict):
        return ['the file is not an object']
    if brand and doc.get('brand') != brand:
        errs.append(f'brand is {doc.get("brand")!r}, expected {brand!r}')
    if not DATE_RE.match(str(doc.get('captured_at') or '')):
        errs.append('captured_at must be a date')

    def sources_ok(where, srcs):
        if not srcs:
            errs.append(f'{where}: no source; every number needs a url and a date')
            return
        for i, s in enumerate(srcs):
            url = str(s.get('url') or '')
            if _todo(url) or not url.startswith('http'):
                errs.append(f'{where} source {i + 1}: url missing')
            if _todo(s.get('date')) or not DATE_RE.match(str(s.get('date') or '')):
                errs.append(f'{where} source {i + 1}: date missing or not a date')

    keys = set()
    for i, l in enumerate(doc.get('lanes') or []):
        where = f'lane {i + 1}'
        if not KEY_RE.match(str(l.get('key') or '')) or _todo(l.get('key')):
            errs.append(f'{where}: key must be a short lower-case id')
        elif l['key'] in keys:
            errs.append(f'{where}: duplicate key {l["key"]}')
        else:
            keys.add(l['key'])
        if _todo(l.get('label')) or not l.get('label'):
            errs.append(f'{where}: label missing')
        terms = [t for t in (l.get('terms') or []) if not _todo(t)]
        if not terms:
            errs.append(f'{where}: terms missing (the words that name the lane)')
        if l.get('kind') not in ('product', 'proof'):
            errs.append(f'{where}: kind must be product or proof')
    if not keys:
        errs.append('no lanes: the desk needs at least one')
    for i, m in enumerate(doc.get('markets') or []):
        where = f'market {i + 1} ({m.get("key")})'
        if not KEY_RE.match(str(m.get('key') or '')):
            errs.append(f'{where}: key must be a short lower-case id')
        if m.get('size_usd') is None and m.get('cagr_pct') is None and not any(p.get('value_usd') for p in m.get('series') or []) and not any(re.search(r'\d', str(d)) for d in m.get('drivers') or []):
            errs.append(f'{where}: no number at all (size, growth, a series point, or a driver with a figure)')
        if m.get('direction') not in DIRECTIONS:
            errs.append(f'{where}: direction must be up, flat or down')
        for p in m.get('series') or []:
            if p.get('value_usd') is None:
                errs.append(f'{where}: series point {p.get("year")} has no value; delete the point or fill it')
        sources_ok(where, m.get('sources'))
    for i, p in enumerate(doc.get('preferences') or []):
        where = f'preference {i + 1} ({p.get("key")})'
        if p.get('direction') not in DIRECTIONS:
            errs.append(f'{where}: direction must be up, flat or down')
        if _todo(p.get('evidence')) or not p.get('evidence'):
            errs.append(f'{where}: evidence sentence missing')
        sources_ok(where, p.get('sources'))
    for i, l in enumerate(doc.get('launches') or []):
        where = f'launch {i + 1} ({l.get("brand")})'
        if _todo(l.get('brand')) or not l.get('brand'):
            errs.append(f'{where}: brand missing')
        if _todo(l.get('what')) or not l.get('what'):
            errs.append(f'{where}: what launched is missing')
        if _todo(l.get('date')) or not DATE_RE.match(str(l.get('date') or '')):
            errs.append(f'{where}: date missing (2026, 2026-01 or 2026-01-15)')
        if _todo(l.get('sub_category')):
            errs.append(f'{where}: sub_category missing (a lane key, or other)')
        if l.get('channel') not in CHANNELS:
            errs.append(f'{where}: channel must be one of {", ".join(CHANNELS)}')
        sources_ok(where, l.get('sources'))
    return errs


def load(brand: str) -> tuple[dict | None, Path | None]:
    p = path_for(brand)
    if p.is_file():
        return json.loads(p.read_text(encoding='utf-8')), p
    if LEGACY.is_file():
        doc = json.loads(LEGACY.read_text(encoding='utf-8'))
        if doc.get('brand') == brand:
            return doc, LEGACY
    return None, None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description='Write or check the web pass for a brand.')
    ap.add_argument('--brand', required=True)
    ap.add_argument('--category', default='the category')
    ap.add_argument('--init', action='store_true', help='write fixtures/web_pass/<brand>.json as a template to fill')
    ap.add_argument('--check', action='store_true', help='validate the file and list what is missing')
    ap.add_argument('--force', action='store_true', help='overwrite an existing template')
    args = ap.parse_args(argv)
    if not KEY_RE.match(args.brand):
        print('brand must be a folder name like bombas', file=sys.stderr)
        return 2
    if args.init:
        p = path_for(args.brand)
        if p.is_file() and not args.force:
            print(f'{p} exists; use --force to overwrite', file=sys.stderr)
            return 2
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(template(args.brand, args.category), indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        print(f'wrote {p}: fill every TODO, then run --check')
        return 0
    doc, p = load(args.brand)
    if doc is None:
        print(f'no web pass for {args.brand}: run --init first', file=sys.stderr)
        return 2
    errs = check(doc, args.brand)
    print(f'{p}: {len(doc.get("lanes") or [])} lanes, {len(doc.get("markets") or [])} markets, {len(doc.get("preferences") or [])} preferences, {len(doc.get("launches") or [])} launches')
    for e in errs:
        print(' -', e)
    print('ok: the desk can read it' if not errs else f'{len(errs)} problems')
    return 0 if not errs else 1


if __name__ == '__main__':
    raise SystemExit(main())
