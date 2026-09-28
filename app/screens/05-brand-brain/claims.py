"""Claims desk for the brand brain screen: what we can and cannot say, and a scanner for any draft.

Reads only the brain. Rules, no model:
- `desk(brain)`: every claims record with tier, category, source, age, where the ladders use it, and the verdict
  (usable, needs your call, forbidden). Tier counts for the bar. Untiered claims older than UNTIERED_DAYS are
  the finding BRN-R13 in audit.py.
- `scan(brain, text)`: checks a draft (ad, email, page section) against the brain. Hits:
    forbidden      a phrase the founder forbade (claims tier forbidden) appears;
    needs_proof    an absolute or medical word appears with no approved claim behind it (generic list);
    stale_fact     a number in the draft disagrees with the brain (free shipping threshold, returns window,
                   first order discount, giving count) by keyword;
    unapproved     a sentence leans on a claim whose tier is not approved or site backed;
    reading_level  the draft reads above the tenth grade (Flesch-Kincaid, computed in code).
  Every hit names the record and the fix. A draft with a forbidden or stale hit fails; the rest is a warning.
"""
from __future__ import annotations

import datetime as dt
import re

UNTIERED_DAYS = 7
USABLE = ("approved", "site_backed")
NEEDS_PROOF = ["guaranteed to", "the best", "#1", "number one", "clinically proven", "doctor recommended", "cures", "heals",
               "medical grade", "never fails", "100 percent", "100%", "world's", "worlds", "softest", "strongest", "only sock",
               "risk free", "risk-free", "scientifically", "lab tested", "proven to"]
STOP = set("the a an and or of to in on for with is are was were be it its this that these those you your we our us they them by as at from not no".split())
FORBID_LEAD = re.compile(r"\b(?:never say|do not say|don't say|must not say|never claim|forbidden:?|cannot say)\b\s*", re.I)
GRADE_MAX = 10.0


def _sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+|\n+", (text or "").strip())
    return [p.strip() for p in parts if p.strip()]


def _words(s: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9']+", (s or "").lower()) if w not in STOP and len(w) > 2}


def _syllables(word: str) -> int:
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    groups = re.findall(r"[aeiouy]+", w)
    n = len(groups)
    if w.endswith("e") and not w.endswith(("le", "ee")) and n > 1:
        n -= 1
    return max(1, n)


def reading_grade(text: str) -> float | None:
    """Flesch-Kincaid grade level, in code. None when there is too little text."""
    sents = _sentences(text)
    words = re.findall(r"[A-Za-z][A-Za-z']*", text or "")
    if len(words) < 8 or not sents:
        return None
    syl = sum(_syllables(w) for w in words)
    grade = 0.39 * (len(words) / len(sents)) + 11.8 * (syl / len(words)) - 15.59
    return round(max(0.0, grade), 1)


def forbidden_phrases(brain) -> list[dict]:
    out = []
    for r in brain.records("claims"):
        if r["tier"] != "forbidden":
            continue
        raw = r.get("text") or (r.get("value") if isinstance(r.get("value"), str) else "")
        phrase = FORBID_LEAD.split(raw)[-1].strip().strip(".").strip('"').strip("'") if raw else ""
        if len(phrase) >= 4:
            out.append({"id": r["id"], "phrase": phrase, "text": raw})
    return out


def desk(brain) -> dict:
    ladders = [r for r in brain.records("objection_ladders") if isinstance(r.get("value"), dict)]
    used: dict[str, list[dict]] = {}
    for lad in ladders:
        theme = lad["value"].get("theme") or lad.get("field")
        for rung in lad["value"].get("rungs") or []:
            for pid in rung.get("proof_ids") or []:
                used.setdefault(pid, []).append({"ladder": lad["id"], "theme": theme, "level": rung.get("level"), "uses": rung.get("uses") or []})
    rows = []
    counts = {t: 0 for t in ("approved", "site_backed", "reported", "evidence", "inferred", "unverified", "forbidden")}
    for r in brain.records("claims"):
        tier = r["tier"] if r["tier"] in counts else "unverified"
        counts[tier] += 1
        src = r.get("source") or {}
        val = r.get("value")
        category = None
        if isinstance(val, str) and " claim" in val:
            category = val.split(" claim")[0].split(":")[0].strip()
        elif isinstance(val, dict):
            category = val.get("category")
        where = used.get(r["id"], [])
        surfaces = sorted({u for w in where for u in w["uses"]})
        if tier in USABLE:
            v = {"kind": "keep", "text": "Usable", "reason": f"{tier.replace('_', ' ')}; {len(where)} rung{'s' if len(where) != 1 else ''} use it"}
        elif tier == "forbidden":
            v = {"kind": "stop", "text": "Forbidden", "reason": "never appears in copy; the scanner blocks it"}
        else:
            age = r["age_days"]
            v = {"kind": "fix" if (age is not None and age > UNTIERED_DAYS) else "watch", "text": "Needs your call",
                 "reason": f"{tier}; " + (f"{age} days untiered" if age is not None else "undated") + (f"; used by {len(where)} rungs" if where else "")}
        rows.append({"id": r["id"], "field": r.get("field"), "text": r.get("text") or (val if isinstance(val, str) else ""), "tier": tier, "category": category,
                     "source": {"type": src.get("type"), "ref": src.get("ref")}, "date": None if r["date"] == "undated" else r["date"], "age_days": r["age_days"],
                     "confidence": r["confidence"], "used_by": where, "surfaces": surfaces, "verdict": v, "expires_at": r.get("expires_at")})
    order = {"stop": 0, "fix": 1, "watch": 2, "keep": 3}
    rows.sort(key=lambda x: (order.get(x["verdict"]["kind"], 9), -len(x["used_by"]), x["id"]))
    return {"claims": rows, "counts": counts, "total": len(rows), "usable": sum(counts[t] for t in USABLE),
            "needs_call": sum(1 for x in rows if x["verdict"]["kind"] in ("fix", "watch")), "forbidden": counts["forbidden"],
            "forbidden_phrases": forbidden_phrases(brain), "untiered_days": UNTIERED_DAYS,
            "note": "A claim is usable in customer-facing copy only when it is approved by you or quoted from a live page. Forbidden phrases block a draft in the scanner."}


def _words_avoided(brain) -> list[str]:
    r = next((x for x in brain.records("voice") if x.get("field") == "words_avoided"), None)
    if not r:
        return []
    v = r.get("value")
    t = ", ".join(v) if isinstance(v, list) else (v if isinstance(v, str) else (r.get("text") or ""))
    return [w.strip().lower() for w in re.split(r"[,;\n]+", t) if len(w.strip()) > 1]


def _brain_facts(brain) -> list[dict]:
    """Numbers the scanner can check a draft against, by keyword. Generic keywords, the numbers come from the brain."""
    facts = []
    def rec(section, field):
        return next((r for r in brain.records(section) if r.get("field") == field and r["tier"] in USABLE), None)
    r = rec("offers", "free_shipping_threshold_usd")
    if r and isinstance(r.get("value"), (int, float)):
        facts.append({"id": r["id"], "keywords": ["free shipping", "ships free"], "kind": "usd", "value": float(r["value"]), "label": "free shipping threshold"})
    r = rec("policies", "returns_window_days")
    if r and isinstance(r.get("value"), (int, float)):
        facts.append({"id": r["id"], "keywords": ["return", "returns", "refund"], "kind": "days", "value": float(r["value"]), "label": "returns window in days"})
    r = rec("offers", "first_order_code")
    if r and isinstance(r.get("value"), dict) and isinstance(r["value"].get("discount_pct"), (int, float)):
        facts.append({"id": r["id"], "keywords": ["first order", "welcome", "% off", "percent off"], "kind": "pct", "value": float(r["value"]["discount_pct"]), "label": "first order discount"})
    r = rec("offers", "standard_shipping_cost")
    if r and isinstance(r.get("value"), dict) and isinstance(r["value"].get("cost_usd"), (int, float)):
        facts.append({"id": r["id"], "keywords": ["shipping cost", "shipping is", "standard shipping"], "kind": "usd", "value": float(r["value"]["cost_usd"]), "label": "standard shipping cost"})
    return facts


def scan(brain, text: str) -> dict:
    text = text or ""
    hits = []
    low = text.lower()
    for fp in forbidden_phrases(brain):
        if fp["phrase"].lower() in low:
            hits.append({"kind": "forbidden", "severity": "fail", "match": fp["phrase"], "record": fp["id"], "tier": "forbidden",
                         "fix": "Remove it. The founder forbade this phrase."})
    approved_text = " ".join((r.get("text") or "").lower() for r in brain.records("claims") if r["tier"] in USABLE)
    for w in NEEDS_PROOF:
        if w in low and w not in approved_text:
            hits.append({"kind": "needs_proof", "severity": "warn", "match": w, "record": None, "tier": None,
                         "fix": "Back it with an approved claim, or soften it to what a live page says."})
    sents = _sentences(text)
    for fact in _brain_facts(brain):
        for s in sents:
            sl = s.lower()
            if not any(k in sl for k in fact["keywords"]):
                continue
            if fact["kind"] == "usd":
                nums = [float(x.replace(",", "")) for x in re.findall(r"\$\s?(\d[\d,]*(?:\.\d+)?)", s)]
            elif fact["kind"] == "pct":
                nums = [float(x) for x in re.findall(r"(\d+(?:\.\d+)?)\s?(?:%|percent)", sl)]
            else:
                nums = [float(x) for x in re.findall(r"(\d+)\s?(?:-?\s?days?|day)", sl)]
            for n in nums:
                if abs(n - fact["value"]) > 0.01:
                    hits.append({"kind": "stale_fact", "severity": "fail", "match": s[:120], "record": fact["id"], "tier": "brain",
                                 "fix": f"The brain says {fact['label']} is {fact['value']:g}. The draft says {n:g}."})
    weak = [r for r in brain.records("claims") if r["tier"] not in USABLE and r["tier"] != "forbidden"]
    for r in weak:
        cw = _words(r.get("text") or "")
        if len(cw) < 4:
            continue
        for s in sents:
            if len(cw & _words(s)) >= 4:
                hits.append({"kind": "unapproved", "severity": "warn", "match": s[:120], "record": r["id"], "tier": r["tier"],
                             "fix": "Approve the claim in the claims desk, or drop the sentence."})
                break
    for w in _words_avoided(brain):
        if re.search(r"\b" + re.escape(w) + r"\b", low):
            hits.append({"kind": "avoided_word", "severity": "warn", "match": w, "record": f"{brain.brand}.voice.words_avoided", "tier": "voice",
                         "fix": "A word on the voice sheet's avoid list. Swap it for a plain one."})
    grade = reading_grade(text)
    if grade is not None and grade > GRADE_MAX:
        hits.append({"kind": "reading_level", "severity": "warn", "match": f"grade {grade}", "record": None, "tier": None,
                     "fix": f"Shorter sentences and plainer words. Target is below grade {GRADE_MAX:g}."})
    fails = sum(1 for h in hits if h["severity"] == "fail")
    warns = len(hits) - fails
    return {"verdict": "fail" if fails else ("warn" if warns else "pass"), "fails": fails, "warns": warns, "hits": hits,
            "reading_grade": grade, "words": len(re.findall(r"[A-Za-z][A-Za-z']*", text)), "sentences": len(sents),
            "checked": {"forbidden_phrases": len(forbidden_phrases(brain)), "facts": len(_brain_facts(brain)), "weak_claims": len(weak)}}
