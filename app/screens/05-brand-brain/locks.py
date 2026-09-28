"""Locked zones: the lines and facts an agent may not change, and the check that catches a draft that changed them.

Four kinds of lock, all from records: the locked snippet lines (voice, from the snippets block); the locked facts
(the free shipping threshold, the standard shipping cost, the returns window, the first order code: approved or site
backed records, so a draft that states another value is wrong); the logo rules (visual.logo_rules, the never list);
and the founder's own locked lines (`content.locked_<slug>`: a line that must appear word for word in every draft of a
given kind or channel, such as a disclaimer or the legal footer). The review route runs `check`: a required line
absent from a draft in its scope fails; a line that appears altered (a sentence with most of the locked line's words
but not the line itself) fails; a locked fact stated with another value is the claims scan's stale-fact fail. Web
pass idea 23: agents fill the open zones and never touch the locked ones.
"""
from __future__ import annotations

import re

SCOPES = ("all", "email", "ad", "pdp", "policy", "amazon", "meta", "google", "sms", "site")
FACT_FIELDS = [("offers", "free_shipping_threshold_usd", "free shipping threshold"), ("offers", "standard_shipping_cost", "standard shipping cost"), ("policies", "returns_window_days", "returns window"), ("offers", "first_order_code", "first order code")]
STOP = set("the a an and or of to in on for with is are was were be it its this that you your we our at from by as".split())


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", (s or "").lower()).strip("_")[:60]


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9$%. ]+", " ", (s or "").lower())).strip()


def _words(s: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9$%.]+", _norm(s)) if w not in STOP}


def _rec(brain, section, field):
    rows = [r for r in brain.records(section) if r.get("field") == field]
    rows.sort(key=lambda r: ({"approved": 0, "site_backed": 1}.get(r["tier"], 2), r["id"]))
    return rows[0] if rows else None


def founder_lines(brain) -> list[dict]:
    out = []
    for r in brain.records("content"):
        if (r.get("field") or "").startswith("locked_") and isinstance(r.get("value"), dict) and r["value"].get("text"):
            v = r["value"]
            out.append({"record": r["id"], "key": r["field"][7:], "label": v.get("label") or r["field"][7:].replace("_", " "), "text": v["text"], "scope": [s for s in (v.get("scope") or ["all"]) if s in SCOPES] or ["all"], "required": bool(v.get("required", True)), "date": None if r["date"] == "undated" else r["date"]})
    return out


def zones(brain, voice_mod=None) -> dict:
    lines = []
    if voice_mod is not None:
        try:
            for row in voice_mod.snippets(brain).get("snippets") or []:
                if row.get("status") == "locked" and row.get("locked"):
                    lines.append({"kind": "snippet", "key": row["key"], "label": row.get("label") or row["key"], "text": row["locked"], "scope": ["all"], "required": False, "record": row.get("locked_record")})
        except Exception:  # noqa: BLE001
            pass
    for fl in founder_lines(brain):
        lines.append(dict(fl, kind="line"))
    facts = []
    for sec, field, label in FACT_FIELDS:
        r = _rec(brain, sec, field)
        if r is not None and r["tier"] in ("approved", "site_backed"):
            v = r.get("value")
            facts.append({"kind": "fact", "key": field, "label": label, "value": v if not isinstance(v, dict) else (v.get("code") or v), "record": r["id"], "tier": r["tier"]})
    logo = _rec(brain, "visual", "logo_rules")
    logo_rules = {"available": bool(logo), "never": (logo.get("value") or {}).get("never") if logo and isinstance(logo.get("value"), dict) else [], "record": logo["id"] if logo else None}
    return {"lines": lines, "facts": facts, "logo": logo_rules, "scopes": list(SCOPES),
            "counts": {"lines": len(lines), "required": sum(1 for x in lines if x["required"]), "facts": len(facts), "logo_rules": len(logo_rules["never"] or [])},
            "note": "Locked zones are what an agent never rewrites: the locked lines word for word, the facts with their values, the logo rules. A required line must appear in every draft of its scope; the review route fails a draft that drops or alters one. Agents fill everything else."}


def check(brain, text: str, channel: str | None, kind: str | None, voice_mod=None) -> list[dict]:
    z = zones(brain, voice_mod)
    t = _norm(text)
    sentences = [s.strip() for s in re.split(r"(?<=[.!?\n])\s+", text or "") if s.strip()]
    hits = []
    for ln in z["lines"]:
        locked = _norm(ln["text"])
        in_scope = "all" in ln["scope"] or (channel and channel in ln["scope"]) or (kind and kind in ln["scope"])
        if locked and locked in t:
            continue
        lw = _words(ln["text"])
        altered = None
        for s in sentences:
            sw = _words(s)
            if lw and len(lw & sw) / len(lw) >= 0.6:
                altered = s
                break
        if altered:
            hits.append({"kind": "locked_altered", "severity": "fail", "match": altered[:90], "record": ln.get("record"), "tier": "locked", "fix": f"Use the locked line word for word: {ln['text']}"})
        elif ln["required"] and in_scope:
            hits.append({"kind": "locked_missing", "severity": "fail", "match": ln["label"], "record": ln.get("record"), "tier": "locked", "fix": f"Add the required line word for word: {ln['text']}"})
    return hits


def record(brain, body: dict) -> dict | tuple[int, dict]:
    text = str(body.get("text") or "").strip()[:400]
    if len(text) < 4:
        return 400, {"error": "text is required: the line, word for word"}
    label = str(body.get("label") or "").strip()[:80] or text[:40]
    scope = body.get("scope") if isinstance(body.get("scope"), list) else [x.strip() for x in str(body.get("scope") or "all").split(",") if x.strip()]
    bad = [s for s in scope if s not in SCOPES]
    if bad:
        return 400, {"error": "scope must be from " + ", ".join(SCOPES)}
    key = slug(label)
    if not key:
        return 400, {"error": "label needs letters or digits"}
    v = {"label": label, "text": text, "scope": scope or ["all"], "required": bool(body.get("required", True))}
    return {"id": f"{brain.brand}.content.locked_{key}", "brand": brain.brand, "section": "content", "field": f"locked_{key}", "value": v,
            "text": f"Locked line ({', '.join(v['scope'])}{', required' if v['required'] else ''}): {text}", "tier": "approved", "confidence": 1.0, "visibility": "private",
            "source": {"type": "founder", "ref": "05-brand-brain locked zones", "captured_at": brain.today.isoformat()}}
