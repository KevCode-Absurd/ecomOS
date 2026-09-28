"""One record's history, and restoring an earlier value as a founder edit.

Every put that changes a value moves the old value into the record's `history` (store.put), and every write on this
screen logs a changes record naming the record. `timeline` merges the two into one list, oldest first: each earlier
value with when it was replaced and the source it came from, each change with its kind and what was written, and the
current value last. `restore` takes one earlier value and writes it back as an approved founder record with the
source it was restored from; the value it replaces goes into history like any other change, so a restore can itself be
undone. Nothing is deleted and nothing is rewritten in place.
"""
from __future__ import annotations

import json


def _short(v, n: int = 160) -> str:
    s = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)
    return s if len(s) <= n else s[: n - 1] + "…"


def timeline(brain, rid: str) -> dict | None:
    rec = brain.get(rid)
    if rec is None:
        return None
    items = []
    hist = rec.get("history") or []
    for i, h in enumerate(hist):
        items.append({"kind": "value", "index": i, "when": h.get("changed_at"), "value": h.get("value"), "value_text": _short(h.get("value")), "source_ref": h.get("source_ref"), "source_type": h.get("source_type"),
                      "tier": h.get("tier"), "reason": h.get("reason"), "restorable": h.get("value") != rec.get("value"), "same_as_current": h.get("value") == rec.get("value")})
    for c in brain.records("changes"):
        v = c.get("value") if isinstance(c.get("value"), dict) else {}
        if v.get("record") == rid:
            items.append({"kind": "change", "change_kind": v.get("kind"), "when": c["date"] if c["date"] != "undated" else None, "what": v.get("what"), "before": v.get("before"), "after": v.get("after"), "source": v.get("source"), "record": c["id"]})
    items.sort(key=lambda x: ((x.get("when") or ""), 0 if x["kind"] == "value" else 1))
    current = {"kind": "current", "when": rec["date"] if rec["date"] != "undated" else None, "value": rec.get("value"), "value_text": _short(rec.get("value")), "text": rec.get("text"), "tier": rec["tier"], "status": rec["status"],
               "source_type": (rec.get("source") or {}).get("type"), "source_ref": (rec.get("source") or {}).get("ref"), "restored_from": (rec.get("source") or {}).get("restored_from")}
    return {"record": rid, "section": rec["section"], "field": rec.get("field"), "current": current, "items": items,
            "counts": {"values": len(hist), "changes": sum(1 for x in items if x["kind"] == "change"), "restorable": sum(1 for x in items if x["kind"] == "value" and x["restorable"])},
            "note": "Each earlier value is kept when a change replaces it; each write on this screen logs a change. Restore writes the earlier value back as your approved record; the value it replaces joins the history, so a restore can be undone."}


def _fmt(v) -> str:
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v)


def _mirrors(text, value) -> bool:
    """True when the record's text is just its value written out (a number or the same string)."""
    if not isinstance(text, str) or value is None or isinstance(value, (bool, dict, list)):
        return False
    if isinstance(value, (int, float)):
        try:
            return float(text.strip().replace("$", "").replace(",", "")) == float(value)
        except ValueError:
            return False
    return text.strip() == str(value).strip()


def restore(brain, rid: str, index) -> dict | tuple[int, dict]:
    try:
        idx = int(index)
    except (TypeError, ValueError):
        return 400, {"error": "index must be a number"}
    section = rid.split(".")[1] if rid.count(".") >= 2 else None
    raw = next((r for r in brain.raw(section) if r.get("id") == rid), None) if section else None
    if raw is None:
        return 404, {"error": "no such record", "id": rid}
    hist = raw.get("history") or []
    if not (0 <= idx < len(hist)):
        return 404, {"error": "no history entry at that index", "id": rid, "entries": len(hist)}
    h = hist[idx]
    if h.get("value") == raw.get("value"):
        return 400, {"error": "that value is already the current one", "id": rid}
    was = {"type": (raw.get("source") or {}).get("type"), "ref": (raw.get("source") or {}).get("ref"), "tier": raw.get("tier")}
    new = dict(raw, value=h.get("value"), tier="approved", confidence=1.0, status="active",
               source={"type": "founder", "ref": f"05-brand-brain restore of {rid}", "captured_at": brain.today.isoformat(), "was": was,
                       "restored_from": {"index": idx, "changed_at": h.get("changed_at"), "source_ref": h.get("source_ref")}})
    if _mirrors(raw.get("text"), raw.get("value")) and isinstance(h.get("value"), (str, int, float)) and not isinstance(h.get("value"), bool):
        new["text"] = _fmt(h["value"])  # the text mirrored the value; keep it mirrored
    new.pop("expires_at", None)
    return {"record": new, "before": raw.get("value"), "after": h.get("value")}
