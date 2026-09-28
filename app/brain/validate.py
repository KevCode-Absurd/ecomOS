"""Validate brand brain record files against app/brain/schema.json.

Usage: python3 app/brain/validate.py app/brain/example
       python3 app/brain/validate.py app/brain/bombas/offers.json

A brain folder holds one JSON file per section, each a list of records. The
checks here are the ones the contract names: required fields, allowed values,
one active record per (section, field) when the value is a scalar, no em dash
in any string, unique ids, derived records naming their sources, and the file
name matching the section. No third-party packages.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMA = json.loads((HERE / "schema.json").read_text(encoding="utf-8"))
SECTIONS = set(SCHEMA["properties"]["section"]["enum"])
SOURCE_TYPES = set(SCHEMA["properties"]["source"]["properties"]["type"]["enum"])
TIERS = set(SCHEMA["properties"]["tier"]["enum"])
STATUSES = set(SCHEMA["properties"]["status"]["enum"])
VISIBILITY = set(SCHEMA["properties"]["visibility"]["enum"])
REQUIRED = SCHEMA["required"]
ALLOWED = set(SCHEMA["properties"].keys())
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ID = re.compile(SCHEMA["properties"]["id"]["pattern"])
EM_DASH = "—"


def _strings(value):
    """Yield every string inside a nested value."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for v in value.values():
            yield from _strings(v)
    elif isinstance(value, list):
        for v in value:
            yield from _strings(v)


def check_record(rec: dict, expect_section: str | None = None) -> list[str]:
    errs = []
    if not isinstance(rec, dict):
        return ["record is not an object"]
    rid = rec.get("id", "<no id>")
    for key in REQUIRED:
        if key not in rec:
            errs.append(f"{rid}: missing {key}")
    for key in rec:
        if key not in ALLOWED:
            errs.append(f"{rid}: unknown key {key}")
    if errs:
        return errs
    if not ID.match(rec["id"]):
        errs.append(f"{rid}: id must look like brand.section.field")
    if rec["section"] not in SECTIONS:
        errs.append(f"{rid}: unknown section {rec['section']}")
    if expect_section and rec["section"] != expect_section:
        errs.append(f"{rid}: section {rec['section']} in file for {expect_section}")
    if not rec["id"].startswith(f"{rec['brand']}.{rec['section']}."):
        errs.append(f"{rid}: id must start with brand.section")
    src = rec["source"]
    if not isinstance(src, dict):
        errs.append(f"{rid}: source must be an object")
    else:
        for key in ("type", "ref", "captured_at"):
            if not src.get(key):
                errs.append(f"{rid}: source.{key} is required")
        if src.get("type") not in SOURCE_TYPES:
            errs.append(f"{rid}: source.type {src.get('type')} not allowed")
        if src.get("captured_at") and not DATE.match(str(src["captured_at"])):
            errs.append(f"{rid}: source.captured_at must be YYYY-MM-DD")
        if src.get("type") in ("agent", "inferred") and not src.get("derived_from"):
            errs.append(f"{rid}: {src.get('type')} records must list derived_from record ids")
    conf = rec["confidence"]
    if not isinstance(conf, (int, float)) or not 0 <= conf <= 1:
        errs.append(f"{rid}: confidence must be a number from 0 to 1")
    if rec["tier"] not in TIERS:
        errs.append(f"{rid}: tier {rec['tier']} not allowed")
    if rec["status"] not in STATUSES:
        errs.append(f"{rid}: status {rec['status']} not allowed")
    if rec["visibility"] not in VISIBILITY:
        errs.append(f"{rid}: visibility {rec['visibility']} not allowed")
    if rec["tier"] == "inferred" and rec["source"].get("type") not in ("inferred", "agent"):
        errs.append(f"{rid}: tier inferred needs source.type inferred or agent")
    if rec["tier"] == "approved" and rec["source"].get("type") != "founder":
        errs.append(f"{rid}: tier approved needs source.type founder")
    for key in ("valid_from", "expires_at"):
        if key in rec and not DATE.match(str(rec[key])):
            errs.append(f"{rid}: {key} must be YYYY-MM-DD")
    for ev in rec.get("evidence", []) or []:
        if not isinstance(ev, dict) or not ev.get("quote") or not ev.get("ref"):
            errs.append(f"{rid}: every evidence item needs quote and ref")
    for s in _strings(rec):
        if EM_DASH in s:
            errs.append(f"{rid}: em dash in text")
            break
    return errs


def check_file(path: Path) -> list[str]:
    section = path.stem
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{path.name}: not valid JSON ({exc})"]
    if not isinstance(data, list):
        return [f"{path.name}: must be a list of records"]
    errs = []
    expect = section if section in SECTIONS else None
    if expect is None and section not in ("sources", "assumptions"):
        errs.append(f"{path.name}: file name is not a section")
    for rec in data:
        errs.extend(check_record(rec, expect))
    ids = Counter(r.get("id") for r in data if isinstance(r, dict))
    for rid, n in ids.items():
        if n > 1:
            errs.append(f"{rid}: id appears {n} times")
    active = Counter(
        (r.get("section"), r.get("field"))
        for r in data
        if isinstance(r, dict) and r.get("status") == "active" and not isinstance(r.get("value"), (list, dict))
    )
    for (sec, field), n in active.items():
        if n > 1:
            errs.append(f"{sec}.{field}: {n} active records for one scalar field")
    return errs


def check_path(target: Path) -> list[str]:
    if target.is_dir():
        files = sorted(p for p in target.glob("*.json") if p.stem not in ("sources", "assumptions"))
        errs = []
        for p in files:
            errs.extend(check_file(p))
        return errs
    return check_file(target)


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    total = 0
    for arg in argv[1:]:
        errs = check_path(Path(arg))
        total += len(errs)
        for e in errs:
            print(e)
        if not errs:
            print(f"{arg}: ok")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
