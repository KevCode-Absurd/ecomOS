"""The founder round as a checklist: the week's 5 questions, the proposed updates to clear, the 3 moves to approve and
the reviews due, as ticks that persist, closed with one dated decision.

The digest (3.10) says what the round holds; this is the same list with a box per item. Ticks live in a founder
record for the round (`team.round_<date>`), so the round reopens where it was left. Closing the round writes a
decisions record with what was done and what was carried over, which the next round lists first. Items are built
from the modules: questions ranked, the review queue, the master list, the owners block. Nothing here answers or
approves anything itself: each item links to its block, and the tick records that it was done there.
"""
from __future__ import annotations

import datetime as dt

MAX_Q, MAX_MOVES, MAX_REVIEWS = 5, 3, 3


def _round_key(brain) -> str:
    d = brain.today
    monday = d - dt.timedelta(days=d.weekday())
    return monday.isoformat()


def state(brain) -> dict:
    key = _round_key(brain)
    r = next((x for x in brain.records("team") if x.get("field") == f"round_{key.replace('-', '')}"), None)
    v = r.get("value") if r and isinstance(r.get("value"), dict) else {}
    return {"key": key, "record": r["id"] if r else None, "ticked": {k for k, val in (v.get("ticked") or {}).items() if val}, "closed": bool(v.get("closed_on")), "closed_on": v.get("closed_on")}


def build(brain, questions: list[dict], review_count: int, actions: list[dict], owners: dict, carried: list[str]) -> dict:
    st = state(brain)
    items = []
    for q in [x for x in questions if not x.get("answered_on")][:MAX_Q]:
        items.append({"key": "q:" + str(q.get("id") or q.get("field")), "kind": "question", "label": q["question"], "hint": q.get("hint"), "block": "questions"})
    if review_count:
        items.append({"key": "review:queue", "kind": "review", "label": f"Clear the {review_count} proposed update{'s' if review_count != 1 else ''} in the review queue", "hint": None, "block": "review"})
    for a in [x for x in actions if x.get("status") != "unavailable" and not x.get("decision")][:MAX_MOVES]:
        items.append({"key": "act:" + a["id"], "kind": "move", "label": a["title"], "hint": f"{a['owner'].replace('_', ' ')}, {a['rubric']['total']}/100", "block": "plan"})
    for r in [x for x in owners.get("rows") or [] if x.get("state") == "overdue"][:MAX_REVIEWS]:
        items.append({"key": "rev:" + r["section"], "kind": "review_due", "label": f"Review {r['label']}" + (f" ({r['owner']})" if r.get("owner") else ""), "hint": f"{-r['due_in']} days overdue", "block": "owners"})
    for c in carried[:5]:
        items.append({"key": "carry:" + c[:60], "kind": "carried", "label": "Carried over: " + c, "hint": None, "block": "plan"})
    for it in items:
        it["done"] = it["key"] in st["ticked"]
    done = sum(1 for it in items if it["done"])
    return {"round": st["key"], "closed": st["closed"], "closed_on": st["closed_on"], "items": items, "counts": {"items": len(items), "done": done, "left": len(items) - done},
            "text": "\n".join([f"Founder round of {st['key']}: {done} of {len(items)} done"] + [f"[{'x' if it['done'] else ' '}] {it['label']}" + (f" ({it['hint']})" if it.get("hint") else "") for it in items]),
            "note": "The digest as a checklist that remembers its ticks for the week. Each item happens on its block; the tick records it was done. Close the round and the next one lists what was carried over first."}


def tick_record(brain, st: dict, key: str, done: bool, close: bool = False, summary: str | None = None) -> dict:
    rk = st["key"]
    ticked = {k: True for k in st["ticked"]}
    if key:
        if done:
            ticked[key] = True
        else:
            ticked.pop(key, None)
    v = {"round": rk, "ticked": ticked, "closed_on": brain.today.isoformat() if close else (st["closed_on"] if st["closed"] else None), "summary": summary}
    return {"id": f"{brain.brand}.team.round_{rk.replace('-', '')}", "brand": brain.brand, "section": "team", "field": f"round_{rk.replace('-', '')}", "value": v,
            "text": f"Founder round of {rk}: {len(ticked)} item{'s' if len(ticked) != 1 else ''} done" + (f", closed {v['closed_on']}." if v["closed_on"] else "."), "tier": "approved", "confidence": 1.0, "visibility": "private",
            "source": {"type": "founder", "ref": "05-brand-brain founder round", "captured_at": brain.today.isoformat()}}


def close_decision(brain, rk: str, done: list[str], carried: list[str]) -> dict:
    return {"id": f"{brain.brand}.decisions.round_{rk.replace('-', '')}_closed", "brand": brain.brand, "section": "decisions", "field": f"round_{rk.replace('-', '')}_closed",
            "value": {"round": rk, "done": done[:20], "carried": carried[:20], "closed_on": brain.today.isoformat()},
            "text": f"Founder round of {rk} closed on {brain.today.isoformat()}: {len(done)} done" + (f", {len(carried)} carried over: " + "; ".join(c[:60] for c in carried[:3]) if carried else "") + ".",
            "tier": "approved", "confidence": 1.0, "visibility": "private", "source": {"type": "founder", "ref": "05-brand-brain founder round", "captured_at": brain.today.isoformat()}}
