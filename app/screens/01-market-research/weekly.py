"""The weekly research note for a brand: the digest since the last note, the desk report and the week plan (with the load by owner) written to one dated markdown file.

    python3 app/screens/01-market-research/weekly.py --brand bombas
    python3 app/screens/01-market-research/weekly.py --brand sample --print

Writes fixtures/reports/<brand>/<date>.md (the desk's own date, the last full day in the data) and prints the path. Nothing
runs against the network or a model; it reads the same api the page reads. Scheduling it (a Routine, a cron) is the lead's
call and lives outside this folder; the Exports section lists past notes.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPORTS_DIR = HERE / 'fixtures' / 'reports'


def _api():
    sys.path.insert(0, str(HERE.parents[2] / 'app' / 'brain'))
    spec = importlib.util.spec_from_file_location('ecomos_research_api_weekly', HERE / 'api.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build(brand: str | None, api=None) -> dict:
    api = api or _api()
    data = None if brand else api.sample_data()
    dg = api.digest(data, brand)
    rp = api.desk_report(data, brand)
    wk = api.week_plan(data, brand)
    text = dg['text'] + '\n\n---\n\n' + rp['text'] + '\n\n---\n\n' + wk['text'] + '\n'
    return {'brand': brand or 'sample', 'date': rp['ends_on'], 'text': text, 'changes': dg['changes'], 'since': dg['since']}


def write(brand: str | None, api=None) -> Path:
    note = build(brand, api)
    d = REPORTS_DIR / note['brand']
    d.mkdir(parents=True, exist_ok=True)
    p = d / f'{note["date"]}.md'
    p.write_text(note['text'], encoding='utf-8')
    return p


def past(brand: str | None) -> list[dict]:
    d = REPORTS_DIR / (brand or 'sample')
    out = []
    for p in sorted(d.glob('*.md'), reverse=True) if d.is_dir() else []:
        rel = p.relative_to(HERE) if str(p).startswith(str(HERE)) else Path('fixtures') / 'reports' / (brand or 'sample') / p.name
        out.append({'date': p.stem, 'path': str(rel), 'bytes': p.stat().st_size})
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description='Write the weekly research note for a brand.')
    ap.add_argument('--brand', default='bombas')
    ap.add_argument('--print', action='store_true', dest='do_print', help='print the note instead of writing it')
    args = ap.parse_args(argv)
    brand = None if args.brand in ('', 'sample') else args.brand
    if args.do_print:
        print(build(brand)['text'])
        return 0
    p = write(brand)
    print(f'wrote {p}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
