"""Asset rights and expiry: the photos, videos, music, fonts and creator content the brand uses under a licence, with
who holds the rights, where the asset is live, and when the right ends. Ends in a renewal request or a takedown.

An asset is a founder record in the content section (`asset_<slug>`: name, kind, rights holder, licence, where it is
used, expires on, live). The register sorts by days left: expired while live is a takedown or a renewal today; inside
the window (30 days for creator and music, 60 for photo, video and font) is a renewal request now; no expiry date is
a question. Rule BRN-R30 puts each of those on the master list with the request or the takedown note drafted from the
record. Nothing here reads a DAM: assets are what the founder puts on file, until a DAM connector exists. Web pass 15.
"""
from __future__ import annotations

import datetime as dt
import re

KINDS = ("photo", "video", "music", "font", "creator", "illustration", "other")
WINDOW_DAYS = {"photo": 60, "video": 60, "font": 60, "illustration": 60, "music": 30, "creator": 30, "other": 30}


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", (s or "").lower()).strip("_")[:60]


def stored(brain) -> list[dict]:
    out = []
    for r in brain.records("content"):
        if (r.get("field") or "").startswith("asset_") and isinstance(r.get("value"), dict):
            v = r["value"]
            out.append({"record": r["id"], "key": r["field"][6:], "name": v.get("name") or r["field"][6:], "kind": v.get("kind") if v.get("kind") in KINDS else "other", "rights_holder": v.get("rights_holder"), "licence": v.get("licence"),
                        "where": v.get("where") or [], "expires_on": v.get("expires_on"), "live": bool(v.get("live", True)), "note": v.get("note"), "date": None if r["date"] == "undated" else r["date"]})
    return out


def register(brain) -> dict:
    today = brain.today
    rows = []
    for a in stored(brain):
        days_left = None
        if a["expires_on"]:
            try:
                days_left = (dt.date.fromisoformat(a["expires_on"]) - today).days
            except ValueError:
                days_left = None
        window = WINDOW_DAYS[a["kind"]]
        if a["expires_on"] and days_left is None:
            state, verdict = "bad_date", {"kind": "fix", "text": "Date unreadable"}
        elif not a["expires_on"]:
            state, verdict = "no_date", {"kind": "wait", "text": "No expiry on file"}
        elif days_left < 0 and a["live"]:
            state, verdict = "expired_live", {"kind": "stop", "text": f"Expired {-days_left} d ago, still live"}
        elif days_left < 0:
            state, verdict = "expired", {"kind": "keep", "text": "Expired, not live"}
        elif days_left <= window:
            state, verdict = "inside_window", {"kind": "fix", "text": f"{days_left} d left"}
        else:
            state, verdict = "ok", {"kind": "keep", "text": f"{days_left} d left"}
        rows.append(dict(a, days_left=days_left, window_days=window, state=state, verdict=verdict, action=_action(a, state, days_left)))
    rows.sort(key=lambda r: ({"expired_live": 0, "inside_window": 1, "no_date": 2, "bad_date": 2, "ok": 3, "expired": 4}[r["state"]], r["days_left"] if r["days_left"] is not None else 10 ** 6, r["name"]))
    nxt = next((r for r in rows if r["state"] in ("inside_window", "ok") and r["days_left"] is not None), None)
    return {"assets": rows, "kinds": list(KINDS), "windows": WINDOW_DAYS,
            "counts": {"on_file": len(rows), "expired_live": sum(1 for r in rows if r["state"] == "expired_live"), "inside_window": sum(1 for r in rows if r["state"] == "inside_window"), "no_date": sum(1 for r in rows if r["state"] in ("no_date", "bad_date")), "live": sum(1 for r in rows if r["live"])},
            "next": {"name": nxt["name"], "days_left": nxt["days_left"], "expires_on": nxt["expires_on"]} if nxt else None,
            "note": "Assets are what you put on file; no DAM is connected. Windows: 30 days for creator content and music, 60 for photo, video, font and illustration. An expired asset that is still live ends in a takedown or a renewal today."}


def _action(a: dict, state: str, days_left) -> dict | None:
    who = a.get("rights_holder") or "the rights holder"
    where = ", ".join(a.get("where") or []) or "where it is live"
    if state == "expired_live":
        return {"title": f"Take down or renew {a['name']}: the right expired and it is still live on {where}", "owner": "person", "capability": "LOOP-C29",
                "draft": f"To {who}: the licence for {a['name']} ({a['kind']}) ended on {a['expires_on']}. We would like to renew it for the same use ({where}). Please send the terms. Until then we take it down."}
    if state == "inside_window":
        return {"title": f"Renew the right to {a['name']} before {a['expires_on']} ({days_left} days)", "owner": "agent_drafts", "capability": "LOOP-C29",
                "draft": f"To {who}: our licence for {a['name']} ({a['kind']}), used on {where}, ends on {a['expires_on']}. We would like to renew for another term on the same use. Please confirm the price and the term."}
    if state in ("no_date", "bad_date"):
        return {"title": f"Put the expiry date of {a['name']} on file", "owner": "person", "capability": "LOOP-C29", "draft": None}
    return None


def record(brain, body: dict) -> dict | tuple[int, dict]:
    name = str(body.get("name") or "").strip()[:100]
    if not name:
        return 400, {"error": "name is required"}
    kind = str(body.get("kind") or "other")
    if kind not in KINDS:
        return 400, {"error": "kind must be one of " + ", ".join(KINDS)}
    exp = str(body.get("expires_on") or "").strip() or None
    if exp:
        try:
            dt.date.fromisoformat(exp)
        except ValueError:
            return 400, {"error": "expires_on must be a date like 2026-12-31"}
    where = body.get("where") if isinstance(body.get("where"), list) else [x.strip() for x in str(body.get("where") or "").split(",") if x.strip()]
    key = slug(name)
    if not key:
        return 400, {"error": "name needs letters or digits"}
    v = {"name": name, "kind": kind, "rights_holder": str(body.get("rights_holder") or "").strip()[:100] or None, "licence": str(body.get("licence") or "").strip()[:160] or None, "where": [str(x)[:60] for x in where][:10],
         "expires_on": exp, "live": bool(body.get("live", True)), "note": str(body.get("note") or "").strip()[:200] or None}
    text = f"{name} ({kind}): rights held by {v['rights_holder'] or 'unknown'}" + (f", licence {v['licence']}" if v["licence"] else "") + (f", used on {', '.join(v['where'])}" if v["where"] else "") + (f", expires {exp}" if exp else ", no expiry on file") + ("; live." if v["live"] else "; not live.")
    return {"id": f"{brain.brand}.content.asset_{key}", "brand": brain.brand, "section": "content", "field": f"asset_{key}", "value": v, "text": text, "tier": "approved", "confidence": 1.0, "visibility": "private",
            "source": {"type": "founder", "ref": "05-brand-brain asset rights", "captured_at": brain.today.isoformat()}}
