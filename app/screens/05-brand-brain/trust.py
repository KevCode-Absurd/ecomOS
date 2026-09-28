"""Section trust, explained: one number per section from four things anyone can check, with the formula shown.

Trust = 40 x the strong share (approved or site backed records over all records) + 30 x freshness (records inside
their shelf life over all records) + 15 x reviewed (1 when the section's review is not overdue, 0.5 when never
reviewed but updated, 0 when overdue) + 15 x owned (1 when a section has an owner, else 0). The brain's trust is the
record-weighted mean. Every input is a count from the records, the heatmap and the owners block; the formula is on
the page. A section under 50 ends in the action the heatmap already names (connect, ask, re-crawl, review).
"""
from __future__ import annotations

WEIGHTS = {"strong": 40, "fresh": 30, "reviewed": 15, "owned": 15}


def scores(brain, heatmap: dict, owners: dict, meta: set) -> dict:
    own = {r["section"]: r for r in owners.get("rows") or []}
    rows = []
    for sec in heatmap.get("sections") or []:
        key = sec["section"]
        if key in meta:
            continue
        counts = sec.get("counts") or {}
        total = sum(v for v in counts.values() if isinstance(v, (int, float)))
        if not total:
            rows.append({"section": key, "label": sec.get("label") or key.replace("_", " "), "records": 0, "trust": None, "parts": None, "verdict": sec.get("verdict"), "reason": "no records"})
            continue
        strong = (counts.get("approved", 0) + counts.get("site_backed", 0)) / total
        stale = sec.get("stale") if isinstance(sec.get("stale"), (int, float)) else 0
        fresh = max(0.0, (total - stale) / total)
        o = own.get(key) or {}
        reviewed = 1.0 if o.get("state") in ("ok", "due_soon") else (0.5 if o.get("state") in ("never",) else 0.0)
        owned = 1.0 if o.get("assigned") else 0.0
        parts = {"strong": round(strong, 3), "fresh": round(fresh, 3), "reviewed": reviewed, "owned": owned}
        trust = round(WEIGHTS["strong"] * strong + WEIGHTS["fresh"] * fresh + WEIGHTS["reviewed"] * reviewed + WEIGHTS["owned"] * owned)
        rows.append({"section": key, "label": sec.get("label") or key.replace("_", " "), "records": total, "trust": trust, "parts": parts, "verdict": sec.get("verdict"), "owner": o.get("owner"), "review_state": o.get("state"),
                     "reason": ("weak: " if trust < 50 else "") + f"{round(strong * 100)} percent strong, {round(fresh * 100)} percent fresh, review {o.get('state') or 'n/a'}, " + ("owned" if owned else "no owner")})
    rows.sort(key=lambda r: (r["trust"] if r["trust"] is not None else 101, r["section"]))
    scored = [r for r in rows if r["trust"] is not None]
    overall = round(sum(r["trust"] * r["records"] for r in scored) / sum(r["records"] for r in scored)) if scored else None
    return {"rows": rows, "overall": overall, "weights": WEIGHTS, "formula": "40 x strong share + 30 x fresh share + 15 x reviewed (1, 0.5 never, 0 overdue) + 15 x owned",
            "counts": {"sections": len(scored), "under_50": sum(1 for r in scored if r["trust"] < 50), "over_80": sum(1 for r in scored if r["trust"] >= 80)},
            "note": "Four counts anyone can check, weighted as shown. Strong is approved or site-backed over all records; fresh is inside the shelf life; reviewed and owned come from the owners block. The brain's number is the record-weighted mean. A weak section ends in the heatmap's own action."}
