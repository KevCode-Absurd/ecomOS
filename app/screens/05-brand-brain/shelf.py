"""Shelf life per section, set by the founder: how many days a record in a section stays fresh before it counts as
due for a look. The defaults live in health.SHELF_DAYS (offers 1 day, products 7, claims 30, identity 180). A founder
record `team.shelf_<section>` overrides one section; every reader of the table (the heatmap, owners' default cadence,
what goes stale this week, the confirm that moves an expiry on, the connector freshness) reads the overlaid table.
Reset retires the record; nothing is deleted.
"""
from __future__ import annotations

MIN_DAYS, MAX_DAYS = 1, 365


def overrides(brain) -> dict[str, dict]:
    out = {}
    for r in brain.records("team"):
        f = r.get("field") or ""
        if f.startswith("shelf_") and isinstance(r.get("value"), dict) and isinstance(r["value"].get("days"), int):
            out[f[6:]] = {"days": r["value"]["days"], "record": r["id"], "on": r["date"] if r["date"] != "undated" else None, "why": r["value"].get("why")}
    return out


def table(brain, base: dict) -> dict:
    t = dict(base)
    for sec, o in overrides(brain).items():
        if sec in t:
            t[sec] = o["days"]
    return t


def view(brain, base: dict, stats: dict, meta: set) -> dict:
    ov = overrides(brain)
    rows = []
    for sec, default in base.items():
        if sec in meta or default is None:
            continue
        o = ov.get(sec)
        st = stats.get(sec) or {}
        rows.append({"section": sec, "default_days": default, "days": o["days"] if o else default, "set": bool(o), "record": o["record"] if o else None, "set_on": o["on"] if o else None,
                     "why": o["why"] if o else None, "records": st.get("count"), "stale": st.get("stale")})
    rows.sort(key=lambda r: (not r["set"], r["days"], r["section"]))
    return {"sections": rows, "counts": {"sections": len(rows), "set": sum(1 for r in rows if r["set"])},
            "note": "Days a record stays fresh in each section before it is due for a look. The heatmap, the owners' default cadence, what goes stale this week and the confirm that moves an expiry on all read this table."}


def record(brain, section: str, days: int, why: str) -> dict:
    return {"id": f"{brain.brand}.team.shelf_{section}", "brand": brain.brand, "section": "team", "field": f"shelf_{section}", "value": {"days": days, "why": (why or "")[:200] or None},
            "text": f"{section.replace('_', ' ')} records stay fresh for {days} day{'s' if days != 1 else ''}" + (f": {why.strip()[:160]}" if why and why.strip() else "."),
            "tier": "approved", "confidence": 1.0, "visibility": "private",
            "source": {"type": "founder", "ref": "05-brand-brain shelf life", "captured_at": brain.today.isoformat()}}
