"""Trust over time: the brain's trust number and each section's, kept once a day in a small history under the brand
folder, so the chart shows whether the brain is getting more trustworthy.

A point is appended at most once per day, whenever the trust route runs, and on the round close and the digest send.
The history is `review/trust.history.jsonl` (date, overall, per section). The chart reads the last 90 points. No
backfill: the line starts the day this ran first, and says so.
"""
from __future__ import annotations

import json


def append(brain, scores: dict) -> bool:
    p = brain.dir / "review" / "trust.history.jsonl"
    p.parent.mkdir(parents=True, exist_ok=True)
    today = brain.today.isoformat()
    rows = read(brain)
    if rows and rows[-1].get("date") == today:
        return False
    row = {"date": today, "overall": scores.get("overall"), "sections": {r["section"]: r["trust"] for r in scores.get("rows") or [] if r.get("trust") is not None}, "records": sum(r.get("records") or 0 for r in scores.get("rows") or [])}
    with p.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row) + "\n")
    return True


def read(brain, last: int = 90) -> list[dict]:
    p = brain.dir / "review" / "trust.history.jsonl"
    if not p.is_file():
        return []
    out = []
    for ln in p.read_text(encoding="utf-8").splitlines():
        try:
            row = json.loads(ln)
        except ValueError:
            continue
        if isinstance(row, dict) and row.get("date"):
            out.append(row)
    return out[-last:]


def series(brain, sections: list[str] | None = None) -> dict:
    rows = read(brain)
    if not rows:
        return {"available": False, "reason": "no point yet; the first is written the day the trust block runs", "labels": [], "series": []}
    labels = [r["date"] for r in rows]
    out = [{"name": "brain", "values": [r.get("overall") for r in rows]}]
    for sec in sections or []:
        out.append({"name": sec.replace("_", " "), "values": [(r.get("sections") or {}).get(sec) for r in rows]})
    first, last = rows[0], rows[-1]
    return {"available": True, "labels": labels, "series": out, "points": len(rows), "first": first["date"], "last": last["date"], "change": (last.get("overall") - first.get("overall")) if isinstance(first.get("overall"), (int, float)) and isinstance(last.get("overall"), (int, float)) else None,
            "note": f"One point a day since {first['date']}, from the trust block. No backfill."}
