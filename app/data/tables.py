"""Read the data layer: one call per table, JSON or CSV, typed rows.

    from app.data.tables import brand_data
    data = brand_data("bombas")                  # app/data/brands/bombas/: aggregates, then data.sqlite

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
import re
import sqlite3
import threading
from datetime import date, timedelta
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


# ---------------------------------------------------------------- brands/<brand>/ (generator v2)

BRANDS = HERE / "brands"
SAFE_BRAND = re.compile(r"^[a-z0-9_-]{2,40}$")
MAX_SQL_ROWS = 200_000  # a table bigger than this is read through an aggregate, never whole
SESSION_SUMS = ("sessions", "product_view", "add_to_cart", "checkout")


class BrandData:
    """The data layer for app/data/brands/<brand>/, the shape metrics.py expects.

    Aggregates first: `table('daily')` reads aggregates/daily.json. Row tables come from
    data.sqlite only when a metric needs rows: `sessions` is summed by date and device
    (the contract fields), small tables come whole, and a table over MAX_SQL_ROWS raises
    ValueError so a metric says unreadable instead of loading millions of rows. Orders are
    read through `order_day_totals()`, from the daily aggregate. A missing table or a
    missing data.sqlite raises KeyError, so a metric says unavailable, never 0.
    """

    def __init__(self, brand: str):
        if not SAFE_BRAND.match(brand or "") or not (BRANDS / brand / "tables.json").is_file():
            raise ValueError(f"no data folder for brand {brand!r}")
        self.name = brand
        self.folder = BRANDS / brand
        self.sqlite = self.folder / "data.sqlite"
        self._cache = {}
        self._lock = threading.Lock()

    def _json(self, path: Path):
        key = (str(path), path.stat().st_mtime)
        with self._lock:
            if key in self._cache:
                return self._cache[key]
        value = json.loads(path.read_text(encoding="utf-8"))
        with self._lock:
            self._cache[key] = value
        return value

    @property
    def brand(self) -> dict:
        m = self._json(self.folder / "tables.json")
        return {"brand": self.name, "name": self.name.capitalize(), "as_of": m.get("as_of"), "market": "US",
                "currency": "USD", "simulated": bool(m.get("simulated")), "fictional": False, "scale": m.get("scale")}

    def _manifest_row(self, name):
        return next((r for r in self._json(self.folder / "tables.json")["rows"] if r.get("table") == name), None)

    def _captured_at(self):
        as_of = self.brand.get("as_of")
        return f"{(date.fromisoformat(as_of) + timedelta(days=1)).isoformat()}T06:00:00Z" if as_of else None

    def _sql(self, query):
        if not self.sqlite.is_file():
            raise KeyError("data.sqlite")
        key = ("sql", query, self.sqlite.stat().st_mtime)
        with self._lock:
            if key in self._cache:
                return self._cache[key]
        con = sqlite3.connect(f"file:{self.sqlite}?mode=ro", uri=True)
        try:
            con.row_factory = sqlite3.Row
            rows = [dict(r) for r in con.execute(query)]
        finally:
            con.close()
        with self._lock:
            self._cache[key] = rows
        return rows

    def table(self, name: str):
        if not re.fullmatch(r"[a-z0-9_]{1,40}", name or ""):
            raise KeyError(name)
        agg = self.folder / "aggregates" / f"{name}.json"
        if agg.is_file():
            return self._json(agg)["rows"]
        row = self._manifest_row(name)
        if row is None or row.get("where") != "data.sqlite" or not row.get("rows"):
            raise KeyError(name)
        if name == "sessions":
            sums = ", ".join(f"SUM({f}) AS {f}" for f in SESSION_SUMS)
            return self._sql(f"SELECT date, device, {sums} FROM sessions GROUP BY date, device ORDER BY date, device")
        if row["rows"] > MAX_SQL_ROWS:
            raise ValueError(f"{name} has {row['rows']:,} rows; read it through an aggregate")
        return self._sql(f"SELECT * FROM {name}")

    def meta(self, name: str) -> dict:
        agg = self.folder / "aggregates" / f"{name}.json"
        if agg.is_file():
            doc = self._json(agg)
            return {"source": doc.get("source"), "captured_at": doc.get("computed_at"), "simulated": doc.get("simulated")}
        row = self._manifest_row(name)
        if row is None:
            raise KeyError(name)
        return {"source": row.get("source"), "captured_at": self._captured_at(), "shaped_like": row.get("shaped_like"),
                "rows": row.get("rows"), "simulated": True}

    def order_day_totals(self) -> dict:
        """Orders and net revenue per day from aggregates/daily.json, the shape metrics.order_totals reads.
        Every generated order is paid; net_sales is line subtotal minus discounts. No device split."""
        rows = self.table("daily")
        by_day = {(r["date"], None): [r["orders"], float(r["net_sales"])] for r in rows
                  if r.get("orders") is not None and r.get("net_sales") is not None}
        days = sorted(k[0] for k in by_day)
        return {"by_day": by_day, "first": days[0] if days else None, "last": days[-1] if days else None, "devices": []}


_BRANDS = {}


def brand_data(brand: str) -> BrandData:
    """One cached BrandData per brand, so the SQLite sums are read once per server run."""
    if brand not in _BRANDS:
        _BRANDS[brand] = BrandData(brand)
    return _BRANDS[brand]
