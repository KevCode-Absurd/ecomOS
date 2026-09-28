"""A contradiction check before a write: when a founder edits a profile fact, find every active record that carries a
different number or code next to the same words, and stop the save until the founder has seen them.

The check is code, not judgement. The words come from the field name (`free_shipping_threshold_usd` gives `free`,
`shipping`, `threshold`); a record shares the words when any of them appears in its field, text or value. It
contradicts the new text when both carry a number (or a code) and none of them match. Records that carry the same
number are listed as agreeing. Numbers are compared by the field's unit (dollars, days, percent, a year), so a shipping
threshold in dollars is never held against an ad count. A text with no number and no code is unchecked: nothing in
code can say two sentences disagree.

A save over a contradiction is allowed but never silent: the write is logged as an override and a plans record
`plans.settle_<field>` holds every contradicting record until the founder settles each one (fix it, retire it, or
mark it done after editing). Rule BRN-R38 keeps the plan on the master list until nothing is left.
"""
from __future__ import annotations

import json
import re

FACT_SECTIONS = {"offers", "policies", "products", "claims", "identity", "positioning", "calendar", "operations", "channels", "content", "story_bank", "voice"}
STOP = {"usd", "days", "pct", "count", "text", "name", "note", "default", "line", "lines", "list", "code", "year", "date", "confirmed"}
UNITS = {"usd": r"(?:\$\s*(\d[\d,]*(?:\.\d+)?)|(\d[\d,]*(?:\.\d+)?)\s*(?:dollars?|usd|bucks))",
         "days": r"(\d[\d,]*)\s*-?\s*(?:days?|day\b)",
         "pct": r"(\d[\d,]*(?:\.\d+)?)\s*(?:%|percent|pct)",
         "year": r"\b((?:19|20)\d{2})\b",
         "hours": r"(\d[\d,]*)\s*-?\s*(?:hours?|hrs?)\b"}
UNIT_WORDS = {"usd": "usd", "dollars": "usd", "price": "usd", "cost": "usd", "threshold": "usd", "days": "days", "window": "days", "pct": "pct", "percent": "pct", "rate": "pct",
              "year": "year", "founded": "year", "since": "year", "hours": "hours"}


def _keywords(field: str) -> set[str]:
    return {w for w in (field or "").lower().split("_") if len(w) > 3 and w not in STOP}


def unit_of(field: str) -> str | None:
    for w in (field or "").lower().split("_"):
        if w in UNIT_WORDS:
            return UNIT_WORDS[w]
    return None


def _blob(r: dict) -> str:
    v = r.get("value")
    return f"{r.get('field') or ''} {r.get('text') or ''} {v if isinstance(v, str) else json.dumps(v)}".lower()


def _unit_numbers(blob: str, unit: str | None, changes_mod) -> set[str]:
    """The numbers in a record that carry the field's unit; every number of 5 or more when the field has no unit."""
    if unit is None:
        return changes_mod._numbers(blob)
    out = set()
    for m in re.finditer(UNITS[unit], blob):
        x = next((g for g in m.groups() if g), None)
        if x:
            x = x.replace(",", "")
            try:
                float(x)
            except ValueError:
                continue
            out.add(x)
    return out


def _shares(blob: str, kws: set[str]) -> bool:
    hits = sum(1 for k in kws if re.search(rf"(?<![a-z]){re.escape(k)}", blob))
    return hits >= min(2, len(kws)) and hits > 0


def check(brain, section: str, field: str, text: str, changes_mod, exclude_id: str | None = None) -> dict:
    nums = changes_mod._numbers(text)
    codes = changes_mod._codes(text)
    kws = _keywords(field)
    rid = exclude_id or f"{brain.brand}.{section}.{field}"
    current = next((r for r in brain.raw(section) if r.get("id") == rid), None)
    out = {"section": section, "field": field, "text": text, "numbers": sorted(nums, key=float), "codes": sorted(codes), "words": sorted(kws),
           "current": ({"value": current.get("value"), "text": current.get("text"), "tier": current.get("tier")} if current else None),
           "conflicts": [], "agrees": [], "checked": bool((nums or codes) and kws), "unit": unit_of(field)}
    if not out["checked"]:
        out["verdict"] = "unchecked"
        out["reason"] = ("no number or code in the new text" if not (nums or codes) else "the field name has no word to match on")
        out["count"] = 0
        return out
    unit = out["unit"]
    for r in brain.records():
        if r["id"] == rid or r["section"] not in FACT_SECTIONS:
            continue
        blob = _blob(r)
        if not _shares(blob, kws):
            continue
        r_nums = _unit_numbers(blob, unit, changes_mod)
        r_codes = changes_mod._codes(r.get("value")) | changes_mod._codes(r.get("text")) if "code" in blob else set()
        row = {"id": r["id"], "section": r["section"], "field": r.get("field"), "tier": r.get("tier"), "says": str(r.get("text") or r.get("value"))[:160],
               "source": (r.get("source") or {}).get("ref"), "numbers": sorted(r_nums, key=float), "codes": sorted(r_codes)}
        if nums and r_nums:
            (out["agrees"] if r_nums & nums else out["conflicts"]).append(dict(row, kind="number"))
        elif codes and r_codes:
            (out["agrees"] if r_codes & codes else out["conflicts"]).append(dict(row, kind="code"))
    tier_rank = {"approved": 0, "site_backed": 1, "reported": 2, "evidence": 3, "inferred": 4, "unverified": 5}
    out["conflicts"].sort(key=lambda c: (tier_rank.get(c["tier"], 9), c["id"]))
    out["count"] = len(out["conflicts"])
    out["verdict"] = "conflicts" if out["conflicts"] else "clear"
    out["sentence"] = (f"{out['count']} record{'s say' if out['count'] != 1 else ' says'} a different {'number' if nums else 'code'} next to the same words: "
                       + "; ".join(f"{c['id']} says {c['says'][:60]}" for c in out["conflicts"][:3]) + ("." if out["count"] <= 3 else f" and {out['count'] - 3} more.")
                       if out["conflicts"] else ("clear: " + (f"{len(out['agrees'])} record{'s carry' if len(out['agrees']) != 1 else ' carries'} the same value" if out["agrees"] else "no other record carries a number next to these words") + "."))
    return out


def plan_record(brain, rid: str, chk: dict) -> dict:
    field = chk["field"]
    return {"id": f"{brain.brand}.plans.settle_{field}", "brand": brain.brand, "section": "plans", "field": f"settle_{field}",
            "value": {"record": rid, "value": chk["numbers"] or chk["codes"], "text": chk["text"][:200], "opened_on": brain.today.isoformat(),
                      "conflicts": [{"id": c["id"], "says": c["says"][:120], "tier": c["tier"], "done": False} for c in chk["conflicts"]]},
            "text": f"{field.replace('_', ' ')} saved over {chk['count']} contradiction{'s' if chk['count'] != 1 else ''}: settle each record that still says something else.",
            "tier": "approved", "confidence": 1.0, "visibility": "private",
            "source": {"type": "founder", "ref": "05-brand-brain contradiction check", "captured_at": brain.today.isoformat()}}


def open_plans(brain) -> list[dict]:
    out = []
    for r in brain.records("plans"):
        if (r.get("field") or "").startswith("settle_") and isinstance(r.get("value"), dict):
            v = r["value"]
            cs = v.get("conflicts") or []
            left = [c for c in cs if not c.get("done")]
            out.append({"plan": r["id"], "field": r["field"][7:], "record": v.get("record"), "value": v.get("value"), "text": v.get("text"), "opened_on": v.get("opened_on"),
                        "conflicts": cs, "left": len(left), "total": len(cs)})
    out.sort(key=lambda x: (-x["left"], x["field"]))
    return out


def settle(brain, plan_id: str, rid: str, how: str) -> dict | tuple[int, dict]:
    """Settle one contradicting record: `retire` retires it, `done` marks it fixed by hand. The plan retires when none is left."""
    if how not in ("retire", "done"):
        return 400, {"error": "how is retire or done"}
    raw = next((r for r in brain.raw("plans") if r.get("id") == plan_id and r.get("status", "active") != "retired"), None)
    if raw is None or not isinstance(raw.get("value"), dict):
        return 404, {"error": "no open settle plan with that id", "plan": plan_id}
    cs = list(raw["value"].get("conflicts") or [])
    hit = next((c for c in cs if c.get("id") == rid), None)
    if hit is None:
        return 404, {"error": "that record is not on the plan", "plan": plan_id, "record": rid}
    retired = brain.retire(rid) if how == "retire" else False
    hit["done"] = True
    hit["how"] = how
    hit["settled_on"] = brain.today.isoformat()
    left = [c for c in cs if not c.get("done")]
    new = dict(raw, value=dict(raw["value"], conflicts=cs))
    if not left:
        new["status"] = "retired"
    errs = brain.put(new)
    if errs:
        return 400, {"error": "plan not valid", "details": errs}
    return {"ok": True, "plan": plan_id, "record": rid, "how": how, "retired": retired, "left": len(left), "closed": not left}
