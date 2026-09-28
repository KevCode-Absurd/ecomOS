"""Section owners and review cadence: who keeps each part of the brain true, how often it is reviewed, and which
reviews are due.

Each section can have an owner (a role or a named person) and a cadence in days, as a founder record
(`team.owner_<section>`: owner, cadence_days, last_reviewed). Without a record the cadence defaults to the section's
shelf life (health.SHELF_DAYS) and the owner reads unassigned. A review is due when the last review (or, before any,
the last record update) is older than the cadence; overdue reviews are ranked by days over. Mark reviewed writes the
date. Rule BRN-R35 puts each overdue section on the master list for its owner. Meta sections (freshness, changes,
open questions, assumptions) carry no owner: they are the system's.
"""
from __future__ import annotations

import datetime as dt

DEFAULT_CADENCE = 30


def _verdict(state: str, due_in) -> dict:
    if state == "overdue":
        return {"kind": "fix", "text": f"{-due_in} d overdue"}
    if state == "due_soon":
        return {"kind": "watch", "text": f"due in {due_in} d"}
    if state == "ok":
        return {"kind": "keep", "text": f"{due_in} d"}
    if state == "never":
        return {"kind": "wait", "text": "never reviewed"}
    return {"kind": "na", "text": "empty"}


def owners(brain, shelf_days: dict, meta: set, stats: dict) -> dict:
    recs = {}
    review_now = set()
    for r in brain.records("team"):
        f = r.get("field") or ""
        if f.startswith("owner_") and isinstance(r.get("value"), dict):
            recs[f[6:]] = r
        elif f.startswith("review_now_") and isinstance(r.get("value"), dict) and r["value"].get("open", True):
            review_now.add(f[11:])
    rows = []
    today = brain.today
    for sec, st in stats.items():
        if sec in meta:
            continue
        r = recs.get(sec)
        v = r["value"] if r else {}
        cadence = v.get("cadence_days") if isinstance(v.get("cadence_days"), int) and v.get("cadence_days") > 0 else (shelf_days.get(sec) or DEFAULT_CADENCE)
        last_rev = v.get("last_reviewed")
        basis = "review" if last_rev else ("update" if st.get("last_update") else None)
        last = last_rev or st.get("last_update")
        days_since = None
        try:
            days_since = (today - dt.date.fromisoformat(str(last)[:10])).days if last else None
        except ValueError:
            days_since = None
        due_in = (cadence - days_since) if days_since is not None else None
        flagged = sec in review_now
        if not st.get("count"):
            state = "empty"
        elif days_since is None:
            state = "never"
        elif due_in < 0 or flagged:
            state = "overdue"
            if flagged and due_in >= 0:
                due_in = 0
        elif due_in <= 7:
            state = "due_soon"
        else:
            state = "ok"
        rows.append({"section": sec, "label": sec.replace("_", " "), "records": st.get("count", 0), "owner": v.get("owner"), "assigned": bool(v.get("owner")), "cadence_days": cadence, "cadence_default": not (r and v.get("cadence_days")), "flagged": flagged,
                     "last": last, "basis": basis, "days_since": days_since, "due_in": due_in, "state": state, "record": r["id"] if r else None,
                     "verdict": _verdict(state, due_in)})
    rows.sort(key=lambda x: ({"overdue": 0, "due_soon": 1, "never": 2, "ok": 3, "empty": 4}[x["state"]], x["due_in"] if x["due_in"] is not None else 10 ** 6, x["section"]))
    return {"rows": rows, "counts": {"sections": len(rows), "assigned": sum(1 for x in rows if x["assigned"]), "overdue": sum(1 for x in rows if x["state"] == "overdue"), "due_soon": sum(1 for x in rows if x["state"] == "due_soon"), "never": sum(1 for x in rows if x["state"] == "never")},
            "note": "Cadence defaults to the section's shelf life until you set it. Before a first review the clock runs from the last record update. Mark reviewed writes today's date; an overdue section goes on the plan for its owner."}


def record(brain, section: str, body: dict, existing: dict | None) -> dict | tuple[int, dict]:
    owner = str(body.get("owner") if body.get("owner") is not None else (existing or {}).get("owner") or "").strip()[:80] or None
    cad = body.get("cadence_days", (existing or {}).get("cadence_days"))
    try:
        cad = int(cad) if cad not in (None, "") else None
    except (TypeError, ValueError):
        return 400, {"error": "cadence_days must be a number of days"}
    if cad is not None and not (1 <= cad <= 365):
        return 400, {"error": "cadence_days must be between 1 and 365"}
    last = (existing or {}).get("last_reviewed")
    if body.get("reviewed"):
        last = brain.today.isoformat()
    v = {"owner": owner, "cadence_days": cad, "last_reviewed": last}
    text = f"{section.replace('_', ' ')}: " + (f"owned by {owner}" if owner else "no owner") + (f", reviewed every {cad} days" if cad else ", cadence by shelf life") + (f", last reviewed {last}." if last else ".")
    return {"id": f"{brain.brand}.team.owner_{section}", "brand": brain.brand, "section": "team", "field": f"owner_{section}", "value": v, "text": text, "tier": "approved", "confidence": 1.0, "visibility": "private",
            "source": {"type": "founder", "ref": "05-brand-brain section owners", "captured_at": brain.today.isoformat()}}
