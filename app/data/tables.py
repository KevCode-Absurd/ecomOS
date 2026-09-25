"""Read the data layer: one call per table, JSON or CSV, typed rows.

    from app.data.tables import load_table, list_tables
    meta, rows = load_table("orders")            # sample brand by default
    meta, rows = load_table("sessions", brand_dir=Path("app/data/some-brand"))

`meta` is the manifest entry (file, format, rows, source, shaped_like, captured_at).
The manifest, tables.json, is itself a table with one row per table, so the
server lists it like any other.
CSV cells come back typed: int, float, bool, None for an empty cell, else str.
A table that is not in the manifest raises KeyError, so a metric can report
unavailable with the table name instead of pretending it is 0.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SAMPLE = HERE / "sample-brand"


def _cell(v):
    if v == "":
        return None
    if v == "true":
        return True
    if v == "false":
        return False
    try:
        return int(v)
    except ValueError:
        pass
    try:
        return float(v)
    except ValueError:
        return v


def manifest(brand_dir: Path = SAMPLE) -> dict:
    return json.loads((brand_dir / "tables.json").read_text(encoding="utf-8"))


def list_tables(brand_dir: Path = SAMPLE) -> list[str]:
    return [t["table"] for t in manifest(brand_dir)["rows"]]


def load_table(name: str, brand_dir: Path = SAMPLE):
    entries = {t["table"]: t for t in manifest(brand_dir)["rows"]}
    entry = entries[name]
    path = brand_dir / entry["file"]
    if entry["format"] == "json":
        doc = json.loads(path.read_text(encoding="utf-8"))
        rows = doc.pop("rows")
        meta = dict(entry)
        meta.update({k: v for k, v in doc.items() if k not in ("rows_count",)})
        return meta, rows
    with path.open(encoding="utf-8", newline="") as f:
        rows = [{k: _cell(v) for k, v in r.items()} for r in csv.DictReader(f)]
    return dict(entry), rows


if __name__ == "__main__":
    import sys
    names = sys.argv[1:] or list_tables()
    for n in names:
        meta, rows = load_table(n)
        print(f"{n:22s} {len(rows):7d} rows  {meta['format']}  first keys: {list(rows[0].keys())[:6] if rows else []}")
