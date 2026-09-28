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


def register(brain) -> dict:
    groups: dict[str, dict] = {}
    for r in brain.records(include_retired=True):
        src = r.get("source") or {}
        key = _key(src.get("ref") or "") or f"(no reference, {src.get('type') or 'unknown'})"
        g = groups.setdefault(key, {"ref": key, "type": src.get("type") or "unknown", "records": 0, "active": 0, "retired": 0, "stale": 0, "sections": {}, "tiers": {}, "first": None, "last": None, "expired": 0})
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
        cap = src.get("captured_at")
        if cap:
            g["first"] = min(g["first"] or cap, cap)
            g["last"] = max(g["last"] or cap, cap)
    rows = []
    for g in groups.values():
        live = g["active"] - g["stale"]
        flag = "all stale" if g["active"] and live <= 0 else ("mostly retired" if g["records"] and g["retired"] > g["active"] else None)
        rows.append(dict(g, sections=sorted(g["sections"].items(), key=lambda kv: -kv[1]), tiers=g["tiers"], flag=flag, strong=(g["tiers"].get("approved", 0) + g["tiers"].get("site_backed", 0))))
    rows.sort(key=lambda g: (-g["active"], g["ref"]))
    by_type: dict[str, int] = {}
    for g in rows:
        by_type[g["type"]] = by_type.get(g["type"], 0) + g["active"]
    return {"sources": rows, "counts": {"sources": len(rows), "records": sum(g["records"] for g in rows), "active": sum(g["active"] for g in rows), "by_type": by_type, "flagged": sum(1 for g in rows if g["flag"])},
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
