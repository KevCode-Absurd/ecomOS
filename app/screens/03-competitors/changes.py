"""Launches and changes in the window: what the tracked pages started, changed or dropped, newest first,
each with follow, watch or ignore and the action.

Sources:
1. Snapshot diffs (snapshot.py): with two ad-level snapshots, per page the ads that are new, the formats
   and offer types that appear or disappear, and angles never seen from that page before.
2. The brain, dated: a page whose longest running ad is under REFRESH_DAYS old has replaced every ad it
   runs (an account refresh), the lookalike page's creation date, and our own launches (September
   flight, new promo codes, variant tests) for context.

Verdict rules:
  follow  a change we answer now: a new offer or a new angle on a direct competitor, a lookalike page.
  watch   a direct competitor refreshed its whole account, or added a format; read it next capture.
  ignore  a basics or apparel page's refresh, or a change with no overlap with our angles.
  ours    our own launch, shown for context.
Rule COMP-R12 puts a direct competitor's full refresh on the plan as a research note (BRN-C11).
"""
from __future__ import annotations

import datetime as dt

REFRESH_DAYS = 14


def _days(a: str, b: dt.date) -> int | None:
    try:
        return (b - dt.date.fromisoformat(a)).days
    except (TypeError, ValueError):
        return None


def diff(prev: dict | None, cur: dict | None) -> list[dict]:
    """Page-level changes between two snapshots. Empty when fewer than two exist."""
    if not prev or not cur:
        return []
    out = []
    when = cur["captured_at"]
    for pid, meta in (cur.get("pages") or {}).items():
        if meta.get("role") == "self":
            continue
        a = [r for r in prev.get("ads") or [] if r["page_id"] == pid]
        b = [r for r in cur.get("ads") or [] if r["page_id"] == pid]
        if not b:
            continue
        old_ids = {r["ad_id"] for r in a}
        new = [r for r in b if r["ad_id"] not in old_ids]
        fa, fb = {r["format"] for r in a}, {r["format"] for r in b}
        oa, ob = {o["tag"] for r in a for o in r["offers"]}, {o["tag"] for r in b for o in r["offers"]}
        ga, gb = {t["tag"] for r in a for t in r["angles"]}, {t["tag"] for r in b for t in r["angles"]}
        name = meta.get("name")
        if new:
            out.append({"when": when, "page": name, "kind": "new_ads", "n": len(new), "text": f"{len(new)} new ads since {prev['captured_at']}"})
        for f in sorted(fb - fa):
            out.append({"when": when, "page": name, "kind": "new_format", "value": f, "text": f"started running {f}"})
        for o in sorted(ob - oa):
            out.append({"when": when, "page": name, "kind": "new_offer", "value": o, "text": f"new offer type: {o.replace('_', ' ')}"})
        for o in sorted(oa - ob):
            out.append({"when": when, "page": name, "kind": "dropped_offer", "value": o, "text": f"dropped offer type: {o.replace('_', ' ')}"})
        for g in sorted(gb - ga):
            out.append({"when": when, "page": name, "kind": "new_angle", "value": g, "text": f"new angle: {g}"})
    return out


def build(m: dict, brain, prev: dict | None, cur: dict | None, today: dt.date, page_diffs: list[dict] | None = None,
          captures: int = 0) -> dict:
    top = set(m["our_top_angles"])
    frame = {p["name"]: p["frame"] for p in m["pages"]}
    events = []
    for e in page_diffs or []:
        direct = frame.get(e["page"]) == "direct"
        if e["kind"] in ("new_offer", "new_angle") and direct:
            v = ("follow", "Follow", "Answer it: brief our counter this week.")
        elif e["kind"] in ("ads_up", "new_format", "new_flight") and direct:
            v = ("watch", "Watch", "Read what they pushed; brief an answer if it overlaps our angles.")
        else:
            v = ("ignore", "Ignore", "No overlap with our frame.")
        events.append(dict(e, verdict=v[0], verdict_text=v[1], action=v[2], source="page summary diff", direct=direct))
    for e in diff(prev, cur):
        direct = frame.get(e["page"]) == "direct"
        if e["kind"] in ("new_offer", "new_angle") and direct:
            v = ("follow", "Follow", "Answer it: brief our counter this week.")
        elif e["kind"] in ("new_format", "new_ads") and direct:
            v = ("watch", "Watch", "Read the new ads' angles next capture.")
        else:
            v = ("ignore", "Ignore", "No overlap with our angles or frame.")
        events.append(dict(e, verdict=v[0], verdict_text=v[1], action=v[2], source="snapshot diff"))
    for p in m["pages"]:
        if p["role"] == "self" or p.get("longest_days") is None:
            continue
        if p["longest_days"] < REFRESH_DAYS:
            start = (today - dt.timedelta(days=p["longest_days"])).isoformat() if not p.get("longest_start") else p["longest_start"]
            direct = p["frame"] == "direct"
            shared = [a["label"].lower() for a in p["angles"] if a["tag"] in top]
            v = ("watch", "Watch", "Read the new flight's angles and offers; brief an answer if one overlaps ours.") if direct else \
                ("ignore", "Ignore", "Basics page; no action unless it starts selling socks.")
            events.append({"when": start, "page": p["name"], "kind": "refresh", "n": p.get("active_ads"),
                           "text": f"replaced every ad: the oldest of {p.get('active_ads')} active ads is {p['longest_days']} days old"
                                   + (f"; runs our angle {shared[0]}" if shared else ""),
                           "verdict": v[0], "verdict_text": v[1], "action": v[2], "source": "brain page summary",
                           "direct": direct})
    lk = m.get("lookalike")
    if lk and lk.get("created"):
        events.append({"when": lk["created"], "page": "lookalike page", "kind": "lookalike",
                       "text": f"page {lk.get('page_id')} created; {lk.get('ads_seen')} ads link to {lk.get('links_to')}",
                       "verdict": "follow", "verdict_text": "Follow", "action": "Report it. The action is on the plan.",
                       "source": "brain competitors"})
    get = lambda k: (brain.get(f"{brain.brand}.{k}") or {}).get("value")  # noqa: E731
    name = m["brand"].capitalize()
    for r in brain.records("offers"):
        v = r.get("value") if isinstance(r.get("value"), dict) else {}
        if v.get("promo") and v.get("first_seen"):
            events.append({"when": v["first_seen"], "page": name, "kind": "ours", "text": f"promo '{v['promo']}' first seen in {v.get('ads')} ads",
                           "verdict": "ours", "verdict_text": "Ours", "action": None, "source": "brain offers"})
    vt = get("learnings.variant_testing") or {}
    if vt.get("date"):
        events.append({"when": vt["date"], "page": name, "kind": "ours", "text": f"{vt.get('image_variants')} image variants in test",
                       "verdict": "ours", "verdict_text": "Ours", "action": None, "source": "brain learnings"})
    sep = get("learnings.september_flight") or {}
    if isinstance(sep.get("started_since_2026_09_01"), int):
        events.append({"when": "2026-09-01", "page": name, "kind": "ours",
                       "text": f"{sep['started_since_2026_09_01']} new ads this month: " + ", ".join(sep.get("products") or []),
                       "verdict": "ours", "verdict_text": "Ours", "action": None, "source": "brain learnings"})
    events.sort(key=lambda e: (e["when"] or "", e["page"]), reverse=True)
    window_start = (today - dt.timedelta(days=28)).isoformat()
    inwin = [e for e in events if (e["when"] or "") >= window_start]
    return {"events": inwin, "older": len(events) - len(inwin), "window_start": window_start,
            "snapshots": 2 if prev and cur else (1 if cur else 0), "captures": captures,
            "counts": {k: sum(1 for e in inwin if e["verdict"] == k) for k in ("follow", "watch", "ignore", "ours")},
            "rule": f"A page whose oldest active ad is under {REFRESH_DAYS} days old has replaced every ad. Follow: a new offer or angle "
                    "on a direct competitor, or a lookalike page. Watch: a direct refresh or new format. Ignore: basics pages."}
