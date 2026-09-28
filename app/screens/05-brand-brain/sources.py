"""Where every fact came from: the sources register. Every source reference in the brain with the records it fills,
the sections, the tiers, the first and last capture, and the type, so provenance is one table, not a hunt.

A source is the `source.ref` on a record (a url, a file name, an actor, a screen). The register groups records by
reference (the url without its query string), counts them by section and tier, notes the capture dates and the
share of records still active, and flags a reference that fills only stale or expired records (a re-pull or a
retire). Founder writes are one row per screen block. A CSV of the records, one row each with id, section, field,
value, tier, status, visibility, source type, reference, captured date and expiry, is the same data for a
spreadsheet. Capability BRN-C02 (collection with freshness).
"""
from __future__ import annotations

import csv
import io
import json


def _key(ref: str) -> str:
    ref = (ref or "").strip()
    return ref.split("?", 1)[0].rstrip("/") if "://" in ref else ref


def origin(src: dict) -> dict:
    """The source a record came from: a founder approval keeps the original under `was`, and that is the provenance."""
    src = src or {}
    was = src.get("was")
    if src.get("type") == "founder" and isinstance(was, dict) and was.get("ref") and was.get("type") not in (None, "founder"):
        return {"type": was.get("type"), "ref": was["ref"], "captured_at": src.get("captured_at")}
    return src


def register(brain) -> dict:
    groups: dict[str, dict] = {}
    for r in brain.records(include_retired=True):
        src = origin(r.get("source") or {})
        key = _key(src.get("ref") or "") or f"(no reference, {src.get('type') or 'unknown'})"
        g = groups.setdefault(key, {"ref": key, "type": src.get("type") or "unknown", "records": 0, "active": 0, "retired": 0, "stale": 0, "sections": {}, "tiers": {}, "first": None, "last": None, "expired": 0, "retired_approvable": 0})
        g["records"] += 1
        if r["status"] == "retired":
            g["retired"] += 1
        else:
            g["active"] += 1
        if r["status"] == "stale":
            g["stale"] += 1
        if r.get("expired"):
            g["expired"] += 1
        g["sections"][r["section"]] = g["sections"].get(r["section"], 0) + 1
        g["tiers"][r["tier"]] = g["tiers"].get(r["tier"], 0) + 1
        if r["status"] == "retired" and r["tier"] in APPROVABLE_TIERS:
            g["retired_approvable"] += 1
        cap = src.get("captured_at")
        if cap:
            g["first"] = min(g["first"] or cap, cap)
            g["last"] = max(g["last"] or cap, cap)
    rows = []
    rv = reviews(brain)
    for g in groups.values():
        live = g["active"] - g["stale"]
        g["approvable"] = sum(n for t, n in g["tiers"].items() if t in APPROVABLE_TIERS) - g["retired_approvable"]
        g["reviewed_on"] = (rv.get(g["ref"]) or {}).get("on")
        flag = "all stale" if g["active"] and live <= 0 else ("mostly retired" if g["records"] and g["retired"] > g["active"] else None)
        rows.append(dict(g, sections=sorted(g["sections"].items(), key=lambda kv: -kv[1]), tiers=g["tiers"], flag=flag, strong=(g["tiers"].get("approved", 0) + g["tiers"].get("site_backed", 0))))
    rows.sort(key=lambda g: (-g["active"], g["ref"]))
    by_type: dict[str, int] = {}
    for g in rows:
        by_type[g["type"]] = by_type.get(g["type"], 0) + g["active"]
    return {"sources": rows, "counts": {"sources": len(rows), "records": sum(g["records"] for g in rows), "active": sum(g["active"] for g in rows), "by_type": by_type, "flagged": sum(1 for g in rows if g["flag"]), "approvable": sum(g["approvable"] for g in rows), "reviewed": sum(1 for g in rows if g["reviewed_on"])},
            "note": "One row per source reference, with the records it fills by section and tier and the capture dates. A reference whose records are all stale is a re-pull or a retire. Founder writes are one row per screen block."}


def records_csv(brain, include_retired: bool = False) -> str:
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["id", "section", "field", "value", "text", "tier", "status", "visibility", "confidence", "source_type", "source_ref", "captured_at", "date", "expires_at"])
    for r in brain.records(include_retired=include_retired):
        src = r.get("source") or {}
        v = r.get("value")
        w.writerow([r["id"], r["section"], r.get("field") or "", v if isinstance(v, (str, int, float)) and not isinstance(v, bool) else json.dumps(v, ensure_ascii=False), (r.get("text") or "")[:500], r["tier"], r["status"], r.get("visibility") or "",
                    r.get("confidence") if r.get("confidence") is not None else "", src.get("type") or "", src.get("ref") or "", src.get("captured_at") or "", r.get("date") or "", r.get("expires_at") or ""])
    return buf.getvalue()


# ---------------------------------------------------------------- approve a whole source after a review (8.8)

APPROVABLE_TIERS = ("site_backed", "reported", "evidence", "inferred", "unverified")


def reviews(brain) -> dict[str, dict]:
    """Source reviews on file: key -> {on, records, note}. A founder record team.source_review_<n> per review."""
    out = {}
    for r in brain.records("team"):
        if (r.get("field") or "").startswith("source_review_") and isinstance(r.get("value"), dict):
            v = r["value"]
            key = _key(v.get("ref") or "")
            if key and (key not in out or (v.get("on") or "") > (out[key].get("on") or "")):
                out[key] = {"on": v.get("on"), "records": v.get("records"), "note": v.get("note"), "record": r["id"]}
    return out


def approvable(brain, ref: str, sections: list[str] | None = None) -> list[dict]:
    """Active or stale records from one source reference that are not yet approved or forbidden."""
    key = _key(ref)
    out = []
    for r in _raw_all(brain):
        src = origin(r.get("source") or {})
        if _key(src.get("ref") or "") != key or r.get("status", "active") in ("retired", "proposed"):
            continue
        if r.get("tier", "unverified") not in APPROVABLE_TIERS:
            continue
        if sections and r.get("section") not in sections:
            continue
        out.append(r)
    return out


def _raw_all(brain) -> list[dict]:
    """Every raw record in the brain (no defaults applied), so the approved copy keeps only the keys it had."""
    out = []
    for path in sorted(brain.dir.glob("*.json")):
        out.extend(brain.raw(path.stem))
    return out


def approve_source(brain, ref: str, sections: list[str] | None, note: str) -> dict:
    """The approved copies of every approvable record from the source, plus the review record. Nothing is written here."""
    recs = approvable(brain, ref, sections)
    today = brain.today.isoformat()
    new = []
    for r in recs:
        hist = list(r.get("history") or []) + [{"value": r.get("value"), "changed_at": today, "source_ref": (r.get("source") or {}).get("ref") or "",
                                               "tier": r.get("tier"), "reason": "founder approve after source review"}]
        was = {"type": (r.get("source") or {}).get("type"), "ref": (r.get("source") or {}).get("ref"), "tier": r.get("tier")}
        n = dict(r, tier="approved", confidence=1.0, status="active", history=hist,
                 source={"type": "founder", "ref": f"05-brand-brain source review of {_key(ref)}", "captured_at": today, "was": was})
        n.pop("expires_at", None)
        new.append(n)
    n_prev = sum(1 for r in brain.records("team", include_retired=True) if (r.get("field") or "").startswith("source_review_"))
    review = {"id": f"{brain.brand}.team.source_review_{n_prev + 1:03d}", "brand": brain.brand, "section": "team", "field": f"source_review_{n_prev + 1:03d}",
              "value": {"ref": _key(ref), "on": today, "records": [r["id"] for r in new], "sections": sorted({r["section"] for r in new}), "note": (note or "")[:300],
                        "tiers_before": _count(r.get("tier", "unverified") for r in recs)},
              "text": f"{_key(ref)} reviewed on {today}: {len(new)} record{'s' if len(new) != 1 else ''} approved" + (f". {note.strip()[:200]}" if note and note.strip() else "."),
              "tier": "approved", "confidence": 1.0, "visibility": "private",
              "source": {"type": "founder", "ref": "05-brand-brain source review", "captured_at": today}}
    return {"records": new, "review": review, "counts": {"records": len(new), "by_tier": _count(r.get("tier", "unverified") for r in recs), "by_section": _count(r["section"] for r in new)}}


def _count(items) -> dict:
    out: dict[str, int] = {}
    for x in items:
        out[x] = out.get(x, 0) + 1
    return dict(sorted(out.items(), key=lambda kv: -kv[1]))
