"""The hand-offs inbox: briefs other screens hand to the brand brain on the shared hand-offs table (events.md), read
by `to` (the brain's slug or name) or by kind `brain_record`. The brain never edits another screen's rows, so its
own ledger (`team.inbox_<id>`) says what it did with each: accepted (the draft went through the document extractor
into the review queue as proposed records) or dismissed, with a why. Rule BRN-R43 keeps a brief unread for 3 days
on the master list.
"""
from __future__ import annotations

import datetime as dt
import re

TO_US = {"05-brand-brain", "brand brain", "brain", "brand-brain", "05-brand-brain "}
UNREAD_DAYS = 3


def _key(hid: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", (hid or "").lower()).strip("_")[:40]


def for_us(rows: list[dict]) -> list[dict]:
    return [r for r in rows if str(r.get("to") or "").strip().lower() in TO_US or r.get("kind") == "brain_record"]


def ledger(brain) -> dict[str, dict]:
    out = {}
    for r in brain.records("team"):
        f = r.get("field") or ""
        if f.startswith("inbox_") and isinstance(r.get("value"), dict):
            out[r["value"].get("handoff") or f[6:]] = dict(r["value"], record=r["id"])
    return out


def view(brain, rows: list[dict]) -> dict:
    led = ledger(brain)
    items = []
    for r in for_us(rows):
        hid = r.get("id") or ""
        l = led.get(hid)
        when = str(r.get("time") or "")[:10]
        try:
            age = (brain.today - dt.date.fromisoformat(when)).days if when else None
        except ValueError:
            age = None
        state = (l.get("state") if l else "new")
        items.append({"id": hid, "from_screen": r.get("from_screen"), "to": r.get("to"), "kind": r.get("kind"), "title": r.get("title"), "why": r.get("why"), "draft": (r.get("draft") or "")[:4000],
                      "draft_chars": len(r.get("draft") or ""), "owner": r.get("owner"), "status": r.get("status"), "time": r.get("time"), "day": when or None, "age_days": age,
                      "state": state, "handled_on": (l or {}).get("on"), "records": (l or {}).get("records") or [], "note": (l or {}).get("why"), "overdue": state == "new" and age is not None and age >= UNREAD_DAYS})
    order = {"new": 0, "accepted": 1, "dismissed": 2}
    items.sort(key=lambda x: (order.get(x["state"], 9), -(x["age_days"] or 0)))
    return {"items": items, "counts": {"briefs": len(items), "new": sum(1 for x in items if x["state"] == "new"), "overdue": sum(1 for x in items if x["overdue"]), "accepted": sum(1 for x in items if x["state"] == "accepted")},
            "note": "Briefs other screens hand to the brain on the shared hand-offs table. Accept one and its draft goes through the document extractor into the review queue as proposed records; dismiss one with a why. The brain never edits another screen's rows; this ledger is its own."}


def ledger_record(brain, hid: str, state: str, records: list[str], why: str, title: str) -> dict:
    today = brain.today.isoformat()
    return {"id": f"{brain.brand}.team.inbox_{_key(hid)}", "brand": brain.brand, "section": "team", "field": f"inbox_{_key(hid)}",
            "value": {"handoff": hid, "state": state, "on": today, "records": records[:50], "why": (why or "")[:200] or None, "title": (title or "")[:120]},
            "text": f"Hand-off {hid} ({(title or '')[:60]}) {state} on {today}" + (f": {len(records)} record{'s' if len(records) != 1 else ''} proposed" if state == "accepted" else (f": {why.strip()[:120]}" if why and why.strip() else "")) + ".",
            "tier": "approved", "confidence": 1.0, "visibility": "private", "source": {"type": "founder", "ref": "05-brand-brain hand-offs inbox", "captured_at": today}}
