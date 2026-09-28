"""Change a number safely: change a fact the brand quotes (a threshold, a price, a window, a code) in one place, and
get every place that carries the old value as work to finish.

Before the write, the dependents trace lists the records, ladder rungs, questions, snippets and ads that carry the
old value next to the same words. The record is written as a founder edit (the old value goes into history, the text
is kept mirrored), and a plans record (`plans.update_<field>`) holds the dependents to update with a done flag each.
Rule BRN-R37 keeps the plan on the master list until every dependent is marked done, and the plan retires itself.
Only scalar facts change here: a number, a code or a short value.
"""
from __future__ import annotations

import re


def coerce(text: str):
    t = (text or "").strip()
    m = re.fullmatch(r"\$?\s*(-?\d+(?:\.\d+)?)\s*%?", t)
    if m:
        v = float(m.group(1))
        return int(v) if v.is_integer() else v
    return t


def _mirrors(text, value) -> bool:
    if not isinstance(text, str) or value is None or isinstance(value, (bool, dict, list)):
        return False
    if isinstance(value, (int, float)):
        try:
            return float(text.strip().replace("$", "").replace(",", "")) == float(value)
        except ValueError:
            return False
    return text.strip() == str(value).strip()


def change(brain, rid: str, new_text: str, dependents: dict) -> dict | tuple[int, dict]:
    section = rid.split(".")[1] if rid.count(".") >= 2 else None
    raw = next((r for r in brain.raw(section) if r.get("id") == rid), None) if section else None
    if raw is None:
        return 404, {"error": "no such record", "id": rid}
    if isinstance(raw.get("value"), (dict, list)):
        return 400, {"error": "only a scalar fact changes here (a number, a code or a short value); edit a structured record in the profile", "id": rid}
    new_v = coerce(new_text)
    if new_v == raw.get("value") or (isinstance(new_v, (int, float)) and isinstance(raw.get("value"), (int, float)) and float(new_v) == float(raw["value"])):
        return 400, {"error": "that is already the value", "id": rid}
    was = {"type": (raw.get("source") or {}).get("type"), "ref": (raw.get("source") or {}).get("ref"), "tier": raw.get("tier")}
    rec = dict(raw, value=new_v, tier="approved", confidence=1.0, status="active", source={"type": "founder", "ref": "05-brand-brain change a number safely", "captured_at": brain.today.isoformat(), "was": was})
    if _mirrors(raw.get("text"), raw.get("value")) or not isinstance(raw.get("text"), str):
        rec["text"] = str(new_v)
    rec.pop("expires_at", None)
    deps = [d for d in (dependents.get("dependents") or []) if d.get("id") and d["id"] != rid]
    field = raw.get("field") or rid.rsplit(".", 1)[-1]
    plan = {"id": f"{brain.brand}.plans.update_{field}", "brand": brain.brand, "section": "plans", "field": f"update_{field}",
            "value": {"record": rid, "before": raw.get("value"), "after": new_v, "dependents": [{"id": d["id"], "kind": d.get("kind"), "label": str(d.get("label"))[:120], "surfaces": d.get("surfaces") or [], "done": False} for d in deps], "opened_on": brain.today.isoformat()},
            "text": f"{field.replace('_', ' ')} changed from {raw.get('value')} to {new_v}: {len(deps)} place{'s' if len(deps) != 1 else ''} carry the old value and need updating.", "tier": "approved", "confidence": 1.0, "visibility": "private",
            "source": {"type": "founder", "ref": "05-brand-brain change a number safely", "captured_at": brain.today.isoformat()}}
    return {"record": rec, "plan": plan if deps else None, "before": raw.get("value"), "after": new_v, "dependents": deps}


def pending(brain) -> list[dict]:
    out = []
    for r in brain.records("plans"):
        if (r.get("field") or "").startswith("update_") and isinstance(r.get("value"), dict):
            v = r["value"]
            deps = v.get("dependents") or []
            left = [d for d in deps if not d.get("done")]
            out.append({"plan": r["id"], "field": r["field"][7:], "record": v.get("record"), "before": v.get("before"), "after": v.get("after"), "opened_on": v.get("opened_on"), "dependents": deps, "left": len(left), "total": len(deps), "date": None if r["date"] == "undated" else r["date"]})
    out.sort(key=lambda x: (-x["left"], x["field"]))
    return out


def mark_done(brain, plan_id: str, dep_id: str) -> dict | tuple[int, dict]:
    raw = next((r for r in brain.raw("plans") if r.get("id") == plan_id and r.get("status", "active") != "retired"), None)
    if raw is None or not isinstance(raw.get("value"), dict):
        return 404, {"error": "no open update plan with that id", "plan": plan_id}
    deps = list(raw["value"].get("dependents") or [])
    hit = next((d for d in deps if d.get("id") == dep_id), None)
    if hit is None:
        return 404, {"error": "no such dependent on this plan", "dependent": dep_id}
    hit["done"] = True
    hit["done_on"] = brain.today.isoformat()
    left = sum(1 for d in deps if not d.get("done"))
    rec = dict(raw, value=dict(raw["value"], dependents=deps), text=raw["text"].split(":")[0] + f": {left} place{'s' if left != 1 else ''} still carry the old value." if left else raw["text"].split(":")[0] + ": every dependent updated.")
    return {"record": rec, "left": left}
