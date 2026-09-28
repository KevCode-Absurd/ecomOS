"""Validate brand brain record files against app/brain/schema.json.

Usage: python3 app/brain/validate.py app/brain/example
       python3 app/brain/validate.py app/brain/bombas/offers.json

A brain folder holds one JSON file per section, each a list of records. The
checks here are the ones the contract names. Only id, brand, section and a
value or text are required; provenance fields are checked when present. Also:
allowed values, one active record per (section, field) when the value is a
scalar, no em dash in any string, unique ids, derived records naming their
sources, the file name matching the section, and the documents manifest shape.
No third-party packages.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMA = json.loads((HERE / "schema.json").read_text(encoding="utf-8"))
DOC_SCHEMA = json.loads((HERE / "documents.schema.json").read_text(encoding="utf-8"))
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
    if "value" not in rec and "text" not in rec:
        errs.append(f"{rid}: needs a value or a text")
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
    src = rec.get("source")
    if src is not None:
        if not isinstance(src, dict):
            errs.append(f"{rid}: source must be an object")
            src = {}
        for key in ("type", "ref", "captured_at"):
            if not src.get(key):
                errs.append(f"{rid}: source.{key} is required when source is given")
        if src.get("type") not in SOURCE_TYPES:
            errs.append(f"{rid}: source.type {src.get('type')} not allowed")
        if src.get("captured_at") and not DATE.match(str(src["captured_at"])):
            errs.append(f"{rid}: source.captured_at must be YYYY-MM-DD")
        if src.get("type") in ("agent", "inferred") and not src.get("derived_from"):
            errs.append(f"{rid}: {src.get('type')} records must list derived_from record ids")
    else:
        src = {}
    conf = rec.get("confidence")
    if conf is not None and (not isinstance(conf, (int, float)) or not 0 <= conf <= 1):
        errs.append(f"{rid}: confidence must be a number from 0 to 1, or null")
    tier = rec.get("tier", "unverified")
    if tier not in TIERS:
        errs.append(f"{rid}: tier {tier} not allowed")
    if rec.get("status", "active") not in STATUSES:
        errs.append(f"{rid}: status {rec.get('status')} not allowed")
    if rec.get("visibility", "private") not in VISIBILITY:
        errs.append(f"{rid}: visibility {rec.get('visibility')} not allowed")
    if tier == "inferred" and src.get("type") not in ("inferred", "agent"):
        errs.append(f"{rid}: tier inferred needs source.type inferred or agent")
    if tier == "approved" and src.get("type") != "founder":
        errs.append(f"{rid}: tier approved needs source.type founder")
    if tier not in ("unverified", "forbidden") and not src:
        errs.append(f"{rid}: tier {tier} needs a source; leave tier out for an unverified note")
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
        if isinstance(r, dict) and r.get("status", "active") == "active" and "value" in r and not isinstance(r.get("value"), (list, dict))
    )
    for (sec, field), n in active.items():
        if n > 1:
            errs.append(f"{sec}.{field}: {n} active records for one scalar field")
    return errs


DOC_ALLOWED = set(DOC_SCHEMA["items"]["properties"].keys())


def check_manifest(path: Path) -> list[str]:
    """Validate documents/manifest.json: file and added_at required, nothing else."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{path}: not valid JSON ({exc})"]
    if not isinstance(data, list):
        return [f"{path}: must be a list"]
    errs = []
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            errs.append(f"manifest[{i}]: not an object")
            continue
        for key in ("file", "added_at"):
            if not item.get(key):
                errs.append(f"manifest[{i}]: missing {key}")
        for key in item:
            if key not in DOC_ALLOWED:
                errs.append(f"manifest[{i}]: unknown key {key}")
        if item.get("added_at") and not DATE.match(str(item["added_at"])):
            errs.append(f"manifest[{i}]: added_at must be YYYY-MM-DD")
        if item.get("file") and not str(item["file"]).startswith("documents/"):
            errs.append(f"manifest[{i}]: file must live under documents/")
        if item.get("file") and not (path.parent.parent / item["file"]).exists():
            errs.append(f"manifest[{i}]: {item['file']} not found")
        for s in _strings(item):
            if EM_DASH in s:
                errs.append(f"manifest[{i}]: em dash in text")
                break
    return errs


def check_registry(root: Path) -> list[str]:
    """sources.registry.json and questions.bank.json: ids unique, sections known, questions point at real sources."""
    errs = []
    reg = json.loads((root / "sources.registry.json").read_text(encoding="utf-8"))
    ids = Counter(s["id"] for s in reg["sources"])
    errs += [f"registry: source id {i} appears {n} times" for i, n in ids.items() if n > 1]
    for src in reg["sources"]:
        for sec in src.get("fills_sections", []):
            if sec not in SECTIONS:
                errs.append(f"registry: {src['id']} fills unknown section {sec}")
    bank = json.loads((root / "questions.bank.json").read_text(encoding="utf-8"))
    qids = Counter(q["id"] for q in bank["questions"])
    errs += [f"bank: question id {i} appears {n} times" for i, n in qids.items() if n > 1]
    for q in bank["questions"]:
        for key in ("asks", "fills", "answerable_by", "unblocks_rooms", "weight"):
            if key not in q:
                errs.append(f"bank: {q.get('id')} missing {key}")
        for sid in q.get("answerable_by", []):
            if sid not in ids:
                errs.append(f"bank: {q['id']} names unknown source {sid}")
        for f in q.get("fills", []):
            if f.split(".")[0] not in SECTIONS:
                errs.append(f"bank: {q['id']} fills unknown section {f}")
        for s in _strings(q):
            if EM_DASH in s:
                errs.append(f"bank: {q['id']} em dash in text")
                break
    return errs


def check_path(target: Path) -> list[str]:
    if target.is_dir():
        files = sorted(p for p in target.glob("*.json") if p.stem not in ("sources", "assumptions"))
        errs = []
        for p in files:
            errs.extend(check_file(p))
        manifest = target / "documents" / "manifest.json"
        if manifest.exists():
            errs.extend(check_manifest(manifest))
        return errs
    if target.name == "manifest.json":
        return check_manifest(target)
    return check_file(target)


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    total = 0
    if argv[1] == "--registry":
        errs = check_registry(HERE)
        for e in errs:
            print(e)
        print("registry and bank: ok" if not errs else f"{len(errs)} problems")
        return 1 if errs else 0
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
