"""Records expiring this week: what goes stale next, grouped by the source that refreshes it, with the re-pull or the
confirmation that keeps it true.

Every record with an expiry inside the window (7 days, and the ones already past) is listed by section and source
type. A public source (site, review, ad library, press) is re-pulled read-only by its connector; a founder or
document record is confirmed by the founder, which extends its expiry by the section's shelf life. Rule BRN-R36
puts one action per source type on the master list (the agent re-pulls, or the founder confirms). Nothing here
refreshes on its own: a re-pull is an agent action inside its caps, a confirmation is a founder tick.
"""
from __future__ import annotations

import datetime as dt

WINDOW_DAYS = 7
PULL = {"site": "re-crawl the site (read-only, free)", "review": "re-pull the reviews (Apify, inside the caps)", "ad_library": "re-pull the Ad Library pages (Apify, inside the caps)", "press": "one press search", "connector": "the connector's next scheduled pull",
        "interview": "a founder check", "founder": "confirm still true", "document": "confirm still true or drop a newer file", "agent": "re-run the synthesis after its inputs refresh", "inferred": "confirm or replace with a sourced record", "ticket": "the support desk's next pull"}


def expiring(brain, shelf_days: dict, window: int = WINDOW_DAYS) -> dict:
    today = brain.today
    end = today + dt.timedelta(days=window)
    rows = []
    for r in brain.records():
        exp = r.get("expires_at")
        if not exp:
            continue
        try:
            d = dt.date.fromisoformat(str(exp)[:10])
        except ValueError:
            continue
        if d <= end:
            src = (r.get("source") or {}).get("type") or "inferred"
            rows.append({"id": r["id"], "section": r["section"], "field": r.get("field"), "expires_at": d.isoformat(), "days": (d - today).days, "expired": d < today, "source": src, "tier": r["tier"], "text": (r.get("text") or str(r.get("value")))[:120],
                         "refresh": PULL.get(src, "confirm or re-pull"), "confirmable": src in ("founder", "document", "interview", "inferred", "agent")})
    rows.sort(key=lambda x: (x["days"], x["section"], x["id"]))
    by_source: dict[str, dict] = {}
    for x in rows:
        g = by_source.setdefault(x["source"], {"source": x["source"], "records": 0, "expired": 0, "sections": set(), "refresh": x["refresh"], "confirmable": x["confirmable"], "earliest": x["expires_at"]})
        g["records"] += 1
        g["expired"] += 1 if x["expired"] else 0
        g["sections"].add(x["section"])
        g["earliest"] = min(g["earliest"], x["expires_at"])
    groups = sorted(({**g, "sections": sorted(g["sections"])} for g in by_source.values()), key=lambda g: (-g["records"], g["source"]))
    return {"window_days": window, "rows": rows[:300], "groups": groups, "counts": {"records": len(rows), "expired": sum(1 for x in rows if x["expired"]), "sources": len(groups), "confirmable": sum(1 for x in rows if x["confirmable"])},
            "note": "Records with an expiry inside the next 7 days, plus the ones already past it, by the source that refreshes them. A public source is re-pulled read-only by the agent; a founder or document record is confirmed by you, which extends its expiry by the section's shelf life."}


def confirmed(brain, rid: str, shelf_days: dict) -> dict | tuple[int, dict]:
    section = rid.split(".")[1] if rid.count(".") >= 2 else None
    raw = next((r for r in brain.raw(section) if r.get("id") == rid), None) if section else None
    if raw is None:
        return 404, {"error": "no such record", "id": rid}
    src = (raw.get("source") or {}).get("type") or "inferred"
    if src not in ("founder", "document", "interview", "inferred", "agent"):
        return 400, {"error": f"a {src} record is refreshed by its source, not confirmed by hand", "id": rid}
    days = shelf_days.get(section) or 30
    new_exp = (brain.today + dt.timedelta(days=days)).isoformat()
    new = dict(raw, expires_at=new_exp, source=dict(raw.get("source") or {}, confirmed_on=brain.today.isoformat()))
    return {"record": new, "expires_at": new_exp, "days": days}


# ---------------------------------------------------------------- old approvals: still true? (10.2)

OLD_FACTOR = 3
OLD_MIN_DAYS, OLD_MAX_DAYS = 30, 365


def old_limit(section: str, shelf_days: dict) -> int:
    return max(OLD_MIN_DAYS, min(OLD_MAX_DAYS, (shelf_days.get(section) or 30) * OLD_FACTOR))


def old_approvals(brain, shelf_days: dict) -> dict:
    """Approved records on the founder's word with no expiry, last confirmed (or captured) longer ago than 3 times the
    section's shelf life (30 to 365 days). They never enter the expiring flow, so nothing asks whether they still hold."""
    rows = []
    for r in brain.records():
        src = r.get("source") or {}
        if r.get("tier") != "approved" or src.get("type") != "founder" or r.get("expires_at") or r["section"] in ("changes", "freshness", "team", "decisions", "plans"):
            continue
        last = str(src.get("confirmed_on") or src.get("captured_at") or "")[:10]
        if not last:
            continue
        try:
            age = (brain.today - dt.date.fromisoformat(last)).days
        except ValueError:
            continue
        limit = old_limit(r["section"], shelf_days)
        if age > limit:
            rows.append({"id": r["id"], "section": r["section"], "field": r.get("field"), "text": str(r.get("text") or r.get("value"))[:160], "last": last, "age_days": age, "limit_days": limit,
                         "was": (src.get("was") or {}).get("type"), "confirmable": True})
    rows.sort(key=lambda x: (-(x["age_days"] - x["limit_days"]), x["id"]))
    return {"rows": rows, "counts": {"records": len(rows), "sections": len({x["section"] for x in rows})},
            "note": "Approved on your word, never given an expiry, and not confirmed for longer than 3 times the section's shelf life. Confirm the ones that still hold (they get an expiry and join the weekly check); retire the rest."}
