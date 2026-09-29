"""Answer open questions from a pasted document: a call note, a supplier email, a policy page. Each open question
(the brain's own and the bank's) is matched in code against the sentences of the text; a sentence that carries most
of the question's words, with a number where the question wants one, is proposed as the answer. The founder
confirms each in a click and the existing answer routes write the record, so nothing here writes on its own.
"""
from __future__ import annotations

import re

STOP = {"what", "which", "when", "where", "does", "have", "with", "that", "this", "from", "your", "our", "the", "and", "for",
        "are", "is", "how", "many", "much", "do", "you", "any", "their", "there", "into", "than", "then", "will", "should", "brand", "store", "who", "ask", "did", "does", "can"}
UNIT_WORDS = {"usd": r"\$\s*\d|\d\s*(?:dollars?|usd)", "days": r"\d+\s*-?\s*days?", "pct": r"\d+(?:\.\d+)?\s*(?:%|percent)", "count": r"\b\d+\b", "hours": r"\d+\s*hours?"}


def _sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+|\n+", text or "")
    return [re.sub(r"^\s*(?:[-*•]\s*|\d+[.)]\s*)", "", p).strip() for p in parts if len(p.strip()) >= 12]


def _words(s: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", (s or "").lower()) if len(w) >= 3 and w not in STOP}


UNIT_ALIASES = {"usd": "usd", "dollars": "usd", "dollar": "usd", "price": "usd", "cost": "usd", "days": "days", "day": "days", "window": "days",
                "pct": "pct", "percent": "pct", "rate": "pct", "hours": "hours", "hour": "hours", "count": "count", "many": "count"}


def _unit(field: str, question: str = "") -> str | None:
    """The unit an answer should carry, read from the field name first, then the question's own words."""
    for text in ((field or "").lower().replace("_", " "), (question or "").lower()):
        for w in re.findall(r"[a-z]+", text):
            if w in UNIT_ALIASES:
                return UNIT_ALIASES[w]
    return None


def propose(text: str, questions: list[dict]) -> dict:
    sents = _sentences(text)
    out, unmatched = [], []
    for q in questions:
        if q.get("answered_on"):
            continue
        qw = _words(q.get("question") or "")
        fw = _words((q.get("field") or "").replace("_", " ")) if not str(q.get("field") or "").startswith("ask_") else set()
        kws = qw if len(qw) >= 3 else (qw | fw)  # the question's own words first; the field name helps a short one
        if not kws:
            continue
        unit = _unit(q.get("field") or "", q.get("question") or "")
        best = None
        for sent in sents:
            sw = _words(sent)
            hit = kws & sw
            if not hit:
                continue
            score = len(hit) / len(kws)
            has_unit = bool(unit and re.search(UNIT_WORDS[unit], sent, re.I))
            if unit and not has_unit:
                score *= 0.6
            if best is None or score > best["score"]:
                best = {"score": round(score, 2), "sentence": sent[:300], "matched": sorted(hit), "has_unit": has_unit}
        need = 0.5 if len(kws) >= 2 else 1.0
        if best and best["score"] >= need and len(best["matched"]) >= min(2, len(kws)):
            out.append({"id": q["id"], "kind": q.get("kind"), "field": q.get("field"), "section": q.get("section"), "question": q.get("question"),
                        "answer": best["sentence"], "score": best["score"], "matched": best["matched"], "unit": unit, "has_unit": best["has_unit"],
                        "route": (f"questions/bank/{q['id']}" if q.get("kind") == "bank" else f"questions/{q.get('field')}")})
        else:
            unmatched.append(q["id"])
    out.sort(key=lambda x: -x["score"])
    return {"proposals": out, "counts": {"sentences": len(sents), "questions": sum(1 for q in questions if not q.get("answered_on")), "proposed": len(out), "unmatched": len(unmatched)},
            "note": "A sentence that carries most of a question's words, with a number where the question wants one. Confirm each; the record is written as your approved answer, and the question closes."}
