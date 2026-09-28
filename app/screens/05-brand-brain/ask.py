"""Ask the brain: a plain question answered from records with tier, source and date, or turned into an open question.

No model. Keyword scoring in code over every active record: the query's words are matched against the record's
field, text and value, with a bonus for a match in the field name, a stronger tier and a newer date. A "can we
say" question is routed to the claims tiers first: an approved or site-backed claim that covers the words answers
yes, a forbidden one answers never, and no match answers "not on file". When nothing scores, the question can be
saved as an open question (`open_questions` record) with the asker's note, so an agent or the founder picks it up.
"""
from __future__ import annotations

import re

STOP = set("the a an and or of to in on for with is are was were be it its this that these those you your we our us they them by as at from not no do does can could what which who how when where why say about have has any".split())
TIER_BONUS = {"approved": 3.0, "site_backed": 2.5, "reported": 1.5, "evidence": 1.0, "inferred": 0.5, "unverified": 0.25, "forbidden": 2.0}
COVER_YES = 0.6
SUPERLATIVES = {"most", "best", "softest", "strongest", "only", "number", "#1", "guaranteed", "proven", "cures", "world's", "worlds", "ever", "never"}
CAN_WE_SAY = re.compile(r"\b(can|could|may|allowed to|ok to|okay to)\s+(we|i)\s+(say|claim|write|promise|state)\b", re.I)


def words(q: str) -> list[str]:
    return [w for w in re.findall(r"[a-z0-9$%]+", (q or "").lower()) if w not in STOP and len(w) > 1]


def _blob(r: dict) -> str:
    v = r.get("value")
    vt = v if isinstance(v, str) else (" ".join(str(x) for x in v) if isinstance(v, list) else (" ".join(f"{k} {x}" for k, x in v.items()) if isinstance(v, dict) else str(v)))
    return f"{r.get('field') or ''} {r.get('text') or ''} {vt}".lower()


def search(brain, q: str, limit: int = 8) -> dict:
    qs = words(q)
    if not qs:
        return {"query": q, "words": [], "answers": [], "can_we_say": None, "count": 0}
    scored = []
    for r in brain.records():
        if r["section"] in ("freshness", "language_bank"):
            continue
        blob = _blob(r)
        field = (r.get("field") or "").lower().replace("_", " ")
        hit = [w for w in qs if w in blob]
        if not hit:
            continue
        score = len(hit) / len(qs) * 10 + sum(2.0 for w in qs if w in field) + TIER_BONUS.get(r["tier"], 0) + (1.0 if r["age_days"] is not None and r["age_days"] <= 30 else 0)
        src = r.get("source") or {}
        scored.append({"score": round(score, 2), "id": r["id"], "section": r["section"], "field": r.get("field"), "tier": r["tier"],
                       "text": (r.get("text") or (r["value"] if isinstance(r.get("value"), str) else str(r.get("value"))))[:300],
                       "date": None if r["date"] == "undated" else r["date"], "source": {"type": src.get("type"), "ref": src.get("ref"), "link": src.get("ref") if str(src.get("ref") or "").startswith("http") else None},
                       "matched": hit})
    scored.sort(key=lambda x: (-x["score"], x["id"]))
    answers = scored[:limit]
    cws = None
    if CAN_WE_SAY.search(q or ""):
        ask_words = [w for w in qs if w not in ("say", "claim", "write", "promise", "state", "our", "socks")]
        claims = [a for a in scored if a["section"] == "claims"]
        cover = lambda a: (len([w for w in ask_words if w in a["matched"]]) / len(ask_words)) if ask_words else 0
        forb = [a for a in claims if a["tier"] == "forbidden" and cover(a) >= 0.5]
        ok = [a for a in claims if a["tier"] in ("approved", "site_backed") and cover(a) >= COVER_YES]
        superlative = [w for w in ask_words if w in SUPERLATIVES]
        if forb:
            cws = {"verdict": "never", "text": "No. A forbidden phrase covers this: " + forb[0]["text"], "record": forb[0]["id"]}
        elif superlative:
            cws = {"verdict": "needs_proof", "text": f"Not as written: \"{superlative[0]}\" is a superlative and no approved claim backs it. Say what a live page says instead.", "record": ok[0]["id"] if ok else None}
        elif ok:
            cws = {"verdict": "yes", "text": "Yes, with the claim as written: " + ok[0]["text"], "record": ok[0]["id"]}
        elif claims:
            cws = {"verdict": "not_yet", "text": "Not as written. The closest claim on file: " + claims[0]["text"] + (" (not approved or site backed)" if claims[0]["tier"] not in ("approved", "site_backed") else " (check the wording matches)"), "record": claims[0]["id"]}
        else:
            cws = {"verdict": "not_on_file", "text": "Not on file. Add it as an approved claim, or save the question.", "record": None}
    return {"query": q, "words": qs, "answers": answers, "can_we_say": cws, "count": len(scored),
            "note": "Keyword match over the brain, best first. Tier and date tell you how far to trust each line. No answer: save it as an open question."}


def to_open_question(brain, q: str, why: str = "", who: str = "the founder") -> dict:
    field = "ask_" + re.sub(r"[^a-z0-9]+", "_", (q or "").lower()).strip("_")[:40]
    rec = {"id": f"{brain.brand}.open_questions.{field}", "brand": brain.brand, "section": "open_questions", "field": field,
           "value": {"question": q.strip(), "section": "open_questions", "why": why.strip()[:200] or "asked on the brain screen with no answer on file",
                     "who_can_answer": who, "asked_on": brain.today.isoformat(), "answered_on": None},
           "text": q.strip(), "tier": "unverified", "visibility": "private",
           "source": {"type": "founder", "ref": "05-brand-brain ask", "captured_at": brain.today.isoformat()}}
    errs = brain.put(rec)
    return {"ok": not errs, "record": rec["id"], "errors": errs}
