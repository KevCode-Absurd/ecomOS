"""The red lines register: every line the brand never crosses, in one list with the reason, who set it and when.

Entries come from the records: forbidden claims (never say), the founder's blocking channel rules, the required locked
lines, the logo never list, rejected ideas with their review date, and decisions whose sentence says never or always.
Each entry carries the reason when one is on file; a red line without a reason is a question for the founder, because
an agent that knows why a line exists keeps it under pressure and a person who reads the register later can trust
it. The reason is written onto the record (a forbidden claim's value becomes {phrase, reason}; the scanner keeps
reading the text). A plain register to copy or print. Capability BRN-C08 (decisions log and red-line register).
"""
from __future__ import annotations

import re

NEVER_ALWAYS = re.compile(r"\b(never|always|must not|do not|don't|no longer)\b", re.I)


def _reason(r) -> str | None:
    v = r.get("value")
    if isinstance(v, dict):
        return v.get("reason") or v.get("why") or None
    return None


def register(brain, claims_mod=None, locks_mod=None, bottlenecks_mod=None) -> dict:
    rows = []
    for r in brain.records("claims"):
        if r["tier"] == "forbidden":
            v = r.get("value")
            raw_phrase = (v.get("phrase") if isinstance(v, dict) else (v if isinstance(v, str) else None)) or str(r.get("text") or "")
            phrase = re.sub(r"^\s*(?:never say|do not say|don't say)[:\s]*", "", raw_phrase, flags=re.I).strip().strip('"\'').rstrip(".")
            rows.append({"kind": "never_say", "label": "Never say", "text": phrase, "why": _reason(r), "set_by": (r.get("source") or {}).get("type"), "date": None if r["date"] == "undated" else r["date"], "record": r["id"], "scope": "every surface", "editable": True})
        f = r.get("field") or ""
        v = r.get("value") if isinstance(r.get("value"), dict) else {}
        if f.startswith("channel_rule_") and v.get("kind") in ("fail", "must"):
            rows.append({"kind": "channel_rule", "label": f"{str(v.get('channel')).capitalize()} rule ({v['kind']})", "text": ("must contain " if v["kind"] == "must" else "") + f"'{v.get('pattern')}'", "why": v.get("why"), "set_by": "founder", "date": None if r["date"] == "undated" else r["date"], "record": r["id"], "scope": v.get("channel"), "editable": True})
    for r in brain.records("content"):
        f = r.get("field") or ""
        v = r.get("value") if isinstance(r.get("value"), dict) else {}
        if f.startswith("locked_") and v.get("text") and v.get("required", True):
            rows.append({"kind": "required_line", "label": "Required line", "text": v["text"], "why": v.get("reason") or v.get("label"), "set_by": "founder", "date": None if r["date"] == "undated" else r["date"], "record": r["id"], "scope": ", ".join(v.get("scope") or ["all"]), "editable": True})
    logo = next((r for r in brain.records("visual") if r.get("field") == "logo_rules" and isinstance(r.get("value"), dict)), None)
    if logo:
        for n in logo["value"].get("never") or []:
            rows.append({"kind": "logo", "label": "Logo, never", "text": str(n), "why": None, "set_by": "founder", "date": None if logo["date"] == "undated" else logo["date"], "record": logo["id"], "scope": "every creative", "editable": False})
    for r in brain.records("learnings"):
        f = r.get("field") or ""
        v = r.get("value") if isinstance(r.get("value"), dict) else {}
        if f.startswith("rejected_idea_"):
            rows.append({"kind": "rejected_idea", "label": "Rejected idea", "text": f"{v.get('idea_id')}: {v.get('title')}", "why": v.get("reason"), "set_by": "founder", "date": None if r["date"] == "undated" else r["date"], "record": r["id"], "scope": f"until {v.get('review_on')}", "editable": True})
    for r in brain.records("decisions"):
        text = str(r.get("text") or "")
        if NEVER_ALWAYS.search(text):
            v = r.get("value") if isinstance(r.get("value"), dict) else {}
            rows.append({"kind": "decision", "label": "Decision", "text": text[:200], "why": v.get("reason"), "set_by": (r.get("source") or {}).get("type"), "date": None if r["date"] == "undated" else r["date"], "record": r["id"], "scope": "the brand", "editable": True})
    rows.sort(key=lambda x: ({"never_say": 0, "required_line": 1, "channel_rule": 2, "logo": 3, "decision": 4, "rejected_idea": 5}[x["kind"]], x["text"] or ""))
    no_reason = [x for x in rows if not x["why"] and x["editable"]]
    lines = [f"Red lines for {brain.brand}, {brain.today.isoformat()}: {len(rows)} lines, {len(no_reason)} without a reason", ""]
    for x in rows:
        lines.append(f"- {x['label']}: {x['text']}" + (f" ({x['scope']})" if x["scope"] else "") + (f". Why: {x['why']}" if x["why"] else ". Why: not on file") + (f". Set {x['date']}" if x["date"] else ""))
    return {"lines": rows, "counts": {"total": len(rows), "without_reason": len(no_reason), "by_kind": {k: sum(1 for x in rows if x["kind"] == k) for k in ("never_say", "required_line", "channel_rule", "logo", "decision", "rejected_idea")}}, "text": "\n".join(lines),
            "note": "One list of what the brand never crosses, from the records: forbidden claims, required lines, blocking channel rules, the logo never list, rejected ideas, decisions that say never or always. Give each a reason: agents keep a line they understand, and a new person can trust it."}


def with_reason(brain, rid: str, reason: str) -> dict | tuple[int, dict]:
    reason = (reason or "").strip()[:300]
    if not reason:
        return 400, {"error": "reason is required"}
    section = rid.split(".")[1] if rid.count(".") >= 2 else None
    raw = next((r for r in brain.raw(section) if r.get("id") == rid), None) if section else None
    if raw is None:
        return 404, {"error": "no such record", "id": rid}
    v = raw.get("value")
    if isinstance(v, dict):
        new_v = dict(v, reason=reason)
    elif isinstance(v, str) and raw.get("tier") == "forbidden":
        new_v = {"phrase": v, "reason": reason}
    else:
        new_v = {"value": v, "reason": reason} if not isinstance(v, dict) else dict(v, reason=reason)
    return {"record": dict(raw, value=new_v), "reason": reason}
