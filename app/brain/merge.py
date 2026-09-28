"""Merge a brand's raw extractor output into its brain, then publish.

Usage: python3 app/brain/merge.py bombas [--today 2026-09-28]

Reads `app/brain/<brand>/raw/<extractor>/*.json` (one folder per extractor, each
with record files named by section plus a `sources.json`) and writes:

- `<section>.json`: the merged records, one active record per (section, field)
  when the value is a scalar, list items deduped by text similarity;
- `sources.json`: the union of the raw source lists, one entry per url;
- `review/conflicts.json`: one entry per field where sources disagree, with
  every value. It lives under `review/` because the brain folder only holds
  section files, and the review queue is where the founder clears conflicts;
- `freshness.json`: one record per section;
- `assumptions.json` and `open_questions.json`, when the brand folder has a
  `calibrate.py` with `build(records, today) -> (assumptions, questions)`;
- `BRAIN.md`, through router.py.

Merge rules (app/contracts/brand-brain.md section 6): founder wins over
everything, then connector, site, document, ad library, interview, press,
review and ticket, agent, inferred. Ties go to higher confidence, then the
newer capture. Losers are never dropped: their value, source and record id go
into the winner's `history`. Two scalar values that differ raise a conflict.
Confidence starts from the record (or a base for its source type), rises 0.05
for each other source that agrees, and drops 0.1 while a conflict is open.
No third-party packages. No network calls.
"""
from __future__ import annotations

import argparse
import copy
import datetime as dt
import importlib.util
import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from store import record_date  # noqa: E402

RANK = {"founder": 100, "connector": 90, "site": 80, "document": 70, "ad_library": 60,
        "interview": 55, "press": 50, "review": 40, "ticket": 40, "agent": 20, "inferred": 10}
BASE_CONFIDENCE = {"founder": 1.0, "connector": 0.95, "site": 0.9, "document": 0.75, "ad_library": 0.8,
                   "interview": 0.7, "press": 0.6, "review": 0.5, "ticket": 0.5, "agent": 0.4, "inferred": 0.4}
AGREE_BONUS = 0.05
CONFLICT_PENALTY = 0.1
MAX_CONFIDENCE = 0.98
SIMILAR = 0.85
GATED = {"identity", "claims", "decisions"}
SOURCE_ALIASES = {"url": ("url", "ref"), "captured_at": ("captured_at", "date", "date_accessed"),
                  "type": ("type", "kind", "source_type"), "ok": ("ok", "accessible", "used")}


def _stype(rec: dict) -> str:
    return (rec.get("source") or {}).get("type", "inferred")


def _is_scalar(rec: dict) -> bool:
    return "value" in rec and rec["value"] is not None and not isinstance(rec["value"], (list, dict))


def _norm(value) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(value).lower()).strip()


def same_value(a, b) -> bool:
    """Equal numbers within 1 percent, or equal text after lowercasing and dropping punctuation."""
    if isinstance(a, bool) or isinstance(b, bool):
        return a is b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(a - b) <= 0.01 * max(abs(a), abs(b), 1e-9)
    return _norm(a) == _norm(b)


def similar_text(a: str, b: str) -> bool:
    """Near-duplicate list items: close character match or heavy word overlap."""
    na, nb = _norm(a), _norm(b)
    if not na or not nb:
        return False
    wa, wb = set(na.split()), set(nb.split())
    if len(wa & wb) / len(wa | wb) >= 0.8:
        return True
    return SequenceMatcher(None, na, nb).ratio() >= SIMILAR


def _value_text(rec: dict) -> str:
    val = rec.get("value")
    if isinstance(val, dict):
        return " ".join(str(v) for v in val.values() if isinstance(v, (str, int, float)))
    if isinstance(val, list):
        return " ".join(str(v) for v in val)
    return "" if val is None else str(val)


def near_duplicate(a: dict, b: dict) -> bool:
    """Two list items say the same thing: the texts match and, when both have values, the values match too.

    Checking both stops templated sentences ("Customers use language like X") and
    shared keys ({"speaker": ...}) from merging items that differ where it counts."""
    if not similar_text(a.get("text", ""), b.get("text", "")):
        return False
    va, vb = _value_text(a), _value_text(b)
    return not (va and vb) or similar_text(va, vb)


def strength(rec: dict) -> tuple:
    """Sort key: source rank, then confidence, then capture date."""
    conf = rec.get("confidence")
    conf = BASE_CONFIDENCE.get(_stype(rec), 0.4) if conf is None else conf
    return (RANK.get(_stype(rec), 0), conf, (rec.get("source") or {}).get("captured_at", ""))


def _history_entry(rec: dict, reason: str) -> dict:
    src = rec.get("source") or {}
    entry = {"value": rec.get("value"), "changed_at": src.get("captured_at") or record_date(rec),
             "source_ref": src.get("ref", ""), "source_type": _stype(rec), "record_id": rec["id"], "reason": reason}
    if "value" not in rec:
        entry["text"] = rec.get("text", "")
    return entry


def _confidence(rec: dict, agreeing: int, conflicted: bool) -> float:
    if _stype(rec) == "founder":
        return 1.0
    conf = rec.get("confidence")
    conf = BASE_CONFIDENCE.get(_stype(rec), 0.4) if conf is None else conf
    conf = min(MAX_CONFIDENCE, conf + AGREE_BONUS * agreeing)
    if conflicted:
        conf = max(0.3, conf - CONFLICT_PENALTY)
    return round(conf, 2)


def _absorb(winner: dict, losers: list[dict], reason: str) -> None:
    hist = winner.setdefault("history", [])
    for lo in losers:
        hist.append(_history_entry(lo, reason))
        seen = {(e.get("quote"), e.get("ref")) for e in winner.get("evidence", [])}
        for ev in lo.get("evidence", []) or []:
            if (ev.get("quote"), ev.get("ref")) not in seen:
                winner.setdefault("evidence", []).append(ev)
                seen.add((ev.get("quote"), ev.get("ref")))


def merge_records(records: list[dict], today: str) -> tuple[list[dict], list[dict]]:
    """Merge raw records. Returns (merged records, conflicts). Inputs are not changed."""
    recs = [copy.deepcopy(r) for r in records]
    groups: dict[tuple, list[dict]] = {}
    for r in recs:
        groups.setdefault((r["section"], r.get("field")), []).append(r)
    single_ids = {x["id"] for g in groups.values() if sum(_is_scalar(x) for x in g) > 1 for x in g if _is_scalar(x)}
    counts: dict[str, int] = {}
    for r in recs:
        counts[r["id"]] = counts.get(r["id"], 0) + 1
    single_ids |= {rid for rid, n in counts.items() if n > 1}

    out, conflicts, done = [], [], set()
    for (section, field), group in groups.items():
        members = [r for r in group if r["id"] in single_ids and (_is_scalar(r) or counts[r["id"]] > 1)]
        rest = [r for r in group if r not in members]
        if members:
            ranked = sorted(members, key=strength, reverse=True)
            win, losers = ranked[0], ranked[1:]
            agree = [lo for lo in losers if same_value(win.get("value"), lo.get("value"))]
            differ = [lo for lo in losers if lo not in agree]
            agreeing_sources = {(lo.get("source") or {}).get("ref") for lo in agree} - {(win.get("source") or {}).get("ref")}
            _absorb(win, agree, "agrees")
            _absorb(win, differ, f"lost to {_stype(win)}")
            if differ:
                cid = f"{win['brand']}.conflict.{section}.{field}"
                conflicts.append({
                    "id": cid, "brand": win["brand"], "section": section, "field": field, "status": "open",
                    "raised_at": today, "kept": win["id"], "needs_founder": section in GATED,
                    "rule": f"{_stype(win)} ranks above {', '.join(sorted({_stype(d) for d in differ}))}"
                            if RANK.get(_stype(win), 0) > max(RANK.get(_stype(d), 0) for d in differ)
                            else "same source type: higher confidence, then newer capture",
                    "values": [{"value": r.get("value"), "text": r.get("text", ""), "source_type": _stype(r),
                                "source_ref": (r.get("source") or {}).get("ref", ""), "record_id": r["id"],
                                "confidence": r.get("confidence")} for r in [win] + differ],
                })
                note = f"Conflict {cid} open; kept by merge rule, other values in history."
                win["notes"] = f"{win['notes']} {note}" if win.get("notes") else note
            win["confidence"] = _confidence(win, len(agreeing_sources), bool(differ))
            out.append(win)
            done.add(win["id"])
        out.extend(rest)

    # Dedupe list items within a section by text similarity; the stronger record keeps the rest in history.
    by_section: dict[str, list[dict]] = {}
    for r in out:
        by_section.setdefault(r["section"], []).append(r)
    final = []
    for section, items in by_section.items():
        kept: list[dict] = []
        for r in sorted(items, key=strength, reverse=True):
            if r["id"] in done or _is_scalar(r):
                kept.append(r)
                continue
            twin = next((k for k in kept if k["id"] not in done and not _is_scalar(k)
                         and near_duplicate(k, r)), None)
            if twin is None:
                kept.append(r)
                continue
            _absorb(twin, [r], "near duplicate")
            other = (r.get("source") or {}).get("ref") != (twin.get("source") or {}).get("ref")
            twin["confidence"] = _confidence(twin, 1 if other else 0, False)
        order = {id(r): i for i, r in enumerate(items)}
        final.extend(sorted(kept, key=lambda r: order[id(r)]))

    for r in final:
        if r["id"] not in done and "confidence" not in r and r.get("source"):
            r["confidence"] = _confidence(r, 0, False)
    return final, conflicts


def merge_sources(lists: dict[str, list[dict]]) -> list[dict]:
    """Union of raw source lists, one entry per url, naming every extractor that used it."""
    merged: dict[str, dict] = {}
    for folder, items in sorted(lists.items()):
        for item in items:
            entry = {}
            for key, aliases in SOURCE_ALIASES.items():
                val = next((item[a] for a in aliases if a in item), None)
                if val is not None:
                    entry[key] = val
            for k, v in item.items():
                if not any(k in a for a in SOURCE_ALIASES.values()):
                    entry[k] = v
            url = entry.get("url")
            if not url:
                continue
            if url in merged:
                have = merged[url]
                have["extractors"] = sorted(set(have["extractors"]) | {folder})
                for k, v in entry.items():
                    have.setdefault(k, v)
            else:
                entry["extractors"] = [folder]
                merged[url] = entry
    return list(merged.values())


def freshness(brand: str, records: list[dict], conflicts: list[dict], today: str) -> list[dict]:
    """One freshness record per section, in the record shape so the brain reads it like any section."""
    out = []
    for section in sorted({r["section"] for r in records}):
        recs = [r for r in records if r["section"] == section]
        dates = [d for d in (record_date(r) for r in recs) if d != "undated"]
        confs = [r["confidence"] for r in recs if isinstance(r.get("confidence"), (int, float))]
        stale = sum(1 for r in recs if r.get("expires_at") and r["expires_at"] < today)
        n_conf = sum(1 for c in conflicts if c["section"] == section and c["status"] == "open")
        value = {"last_updated": max(dates) if dates else None, "record_count": len(recs), "stale_count": stale,
                 "conflict_count": n_conf, "confidence": round(sum(confs) / len(confs), 2) if confs else None}
        out.append({
            "id": f"{brand}.freshness.{section}", "brand": brand, "section": "freshness", "field": section,
            "value": value,
            "text": f"{section}: {len(recs)} records, last updated {value['last_updated'] or 'undated'}, "
                    f"{stale} stale, {n_conf} open conflicts.",
            "source": {"type": "agent", "ref": "app/brain/merge.py", "captured_at": today,
                       "derived_from": [r["id"] for r in recs]},
            "visibility": "private",
        })
    return out


def load_raw(brand_dir: Path) -> tuple[list[dict], dict[str, list[dict]]]:
    records, sources = [], {}
    for folder in sorted(p for p in (brand_dir / "raw").iterdir() if p.is_dir()):
        for path in sorted(folder.glob("*.json")):
            data = json.loads(path.read_text(encoding="utf-8"))
            if path.stem == "sources":
                sources[folder.name] = data
            else:
                records.extend(data)
    return records, sources


def _dump(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _calibrator(brand_dir: Path):
    path = brand_dir / "calibrate.py"
    if not path.exists():
        return None
    spec = importlib.util.spec_from_file_location(f"calibrate_{brand_dir.name}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(brand: str, root: Path | None = None, today: str | None = None, publish: bool = True) -> dict:
    root = root or HERE
    today = today or dt.date.today().isoformat()
    brand_dir = root / brand
    raw, raw_sources = load_raw(brand_dir)
    merged, conflicts = merge_records(raw, today)
    sections = sorted({r["section"] for r in merged} - {"freshness", "open_questions"})
    for section in sections:
        _dump(brand_dir / f"{section}.json", [r for r in merged if r["section"] == section])
    _dump(brand_dir / "sources.json", merge_sources(raw_sources))
    _dump(brand_dir / "review" / "conflicts.json", conflicts)
    written = {"sections": sections, "records": len(merged), "raw": len(raw), "conflicts": len(conflicts)}
    cal = _calibrator(brand_dir)
    if cal:
        assumptions, questions = cal.build(merged, today)
        _dump(brand_dir / "assumptions.json", assumptions)
        _dump(brand_dir / "open_questions.json", questions)
        written.update(assumptions=len(assumptions), open_questions=len(questions))
    _dump(brand_dir / "freshness.json", freshness(brand, merged, conflicts, today))
    if publish:
        import router
        router.write(brand, root, dt.date.fromisoformat(today))
    return written


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("brand")
    ap.add_argument("--today")
    ap.add_argument("--no-publish", action="store_true")
    args = ap.parse_args(argv[1:])
    print(json.dumps(run(args.brand, today=args.today, publish=not args.no_publish)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
