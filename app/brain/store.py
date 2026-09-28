"""Read and write one brand's brain: records by section, plus the documents manifest.

Usage: from store import Brain; b = Brain("example"); b.records("offers")

A brand brain is a folder `app/brain/<brand>/` with one JSON file per section
(a list of records) and `documents/manifest.json`. See
app/contracts/brand-brain.md section 3. Only id, brand, section and a value or
text are required, so the store fills the optional fields with their contract
defaults on read and never writes those defaults back. Nothing is deleted: a
changed value keeps its prior value in `history`, and removal is status
`retired`. No third-party packages.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path

import validate

HERE = Path(__file__).resolve().parent
SECTIONS = list(validate.SCHEMA["properties"]["section"]["enum"])
PUBLIC_SOURCES = {"site", "ad_library", "press", "review", "interview"}
TIER_RANK = {"approved": 0, "site_backed": 1, "reported": 2, "evidence": 3,
             "inferred": 4, "unverified": 5, "forbidden": 6}


def record_date(rec: dict) -> str:
    """The date a record was last known true, or "undated"."""
    src = rec.get("source") or {}
    hist = rec.get("history") or []
    for d in (src.get("captured_at"), rec.get("valid_from"),
              hist[-1].get("changed_at") if hist else None):
        if d:
            return str(d)[:10]
    return "undated"


def with_defaults(rec: dict, today: dt.date) -> dict:
    """A copy of the record with contract defaults and a computed state."""
    out = dict(rec)
    src = rec.get("source") or {}
    out.setdefault("tier", "unverified")
    out.setdefault("confidence", None)
    out.setdefault("status", "active")
    public = src.get("type") in PUBLIC_SOURCES
    out.setdefault("visibility", "public" if public else "private")
    out["date"] = record_date(rec)
    if out["date"] != "undated":
        out["age_days"] = (today - dt.date.fromisoformat(out["date"])).days
    else:
        out["age_days"] = None
    exp = rec.get("expires_at")
    out["expired"] = bool(exp) and dt.date.fromisoformat(exp) < today
    if out["status"] == "active" and out["expired"]:
        out["status"] = "stale"
    return out


class Brain:
    def __init__(self, brand: str, root: Path | None = None, today: dt.date | None = None):
        self.brand = brand
        self.root = Path(root) if root else HERE
        self.dir = self.root / brand
        self.today = today or dt.date.today()
        if not self.dir.is_dir():
            raise FileNotFoundError(f"no brain folder for {brand}: {self.dir}")

    # reading

    def section_path(self, section: str) -> Path:
        return self.dir / f"{section}.json"

    def raw(self, section: str) -> list[dict]:
        path = self.section_path(section)
        if not path.exists():
            return []
        return json.loads(path.read_text(encoding="utf-8"))

    def records(self, section: str | None = None, include_retired: bool = False) -> list[dict]:
        """Records with defaults applied. Retired and proposed records are left out unless asked."""
        sections = [section] if section else SECTIONS
        out = []
        for sec in sections:
            for rec in self.raw(sec):
                r = with_defaults(rec, self.today)
                if include_retired or r["status"] not in ("retired", "proposed"):
                    out.append(r)
        return out

    def get(self, rid: str) -> dict | None:
        section = rid.split(".")[1]
        for rec in self.raw(section):
            if rec.get("id") == rid:
                return with_defaults(rec, self.today)
        return None

    def section_stats(self) -> dict[str, dict]:
        """Per section: record count, stale count, last dated update."""
        stats = {}
        for sec in SECTIONS:
            recs = self.records(sec)
            dates = [r["date"] for r in recs if r["date"] != "undated"]
            stats[sec] = {"count": len(recs),
                          "stale": sum(1 for r in recs if r["status"] == "stale"),
                          "last_update": max(dates) if dates else None}
        return stats

    def documents(self) -> list[dict]:
        path = self.dir / "documents" / "manifest.json"
        if not path.exists():
            return []
        return json.loads(path.read_text(encoding="utf-8"))

    def version(self) -> str:
        """A short hash over every section file and the manifest. Changes when any record changes."""
        h = hashlib.sha256()
        for path in sorted(self.dir.glob("*.json")) + [self.dir / "documents" / "manifest.json"]:
            if path.exists():
                h.update(path.name.encode())
                h.update(path.read_bytes())
        return h.hexdigest()[:12]

    # writing

    def put(self, rec: dict) -> list[str]:
        """Add a record or update one by id. A changed value moves the old value into history.

        Returns validation errors; nothing is written when there are any.
        """
        errs = validate.check_record(rec, rec.get("section"))
        if errs:
            return errs
        section = rec["section"]
        data = self.raw(section)
        new = dict(rec)
        for i, old in enumerate(data):
            if old.get("id") != rec["id"]:
                continue
            hist = list(old.get("history") or [])
            if "value" in old and old.get("value") != rec.get("value"):
                entry = {"value": old["value"], "changed_at": record_date(old) if record_date(old) != "undated"
                         else self.today.isoformat()}
                if (old.get("source") or {}).get("ref"):
                    entry["source_ref"] = old["source"]["ref"]
                hist.append(entry)
            if hist:
                new["history"] = hist
            data[i] = new
            break
        else:
            data.append(new)
        errs = []
        for r in data:
            errs.extend(validate.check_record(r, section))
        if errs:
            return errs
        self._write(section, data)
        return []

    def retire(self, rid: str) -> bool:
        section = rid.split(".")[1]
        data = self.raw(section)
        for rec in data:
            if rec.get("id") == rid:
                rec["status"] = "retired"
                self._write(section, data)
                return True
        return False

    def _write(self, section: str, data: list[dict]) -> None:
        text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
        self.section_path(section).write_text(text, encoding="utf-8")
