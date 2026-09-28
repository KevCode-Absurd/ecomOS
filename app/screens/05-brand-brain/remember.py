"""Remember this: paste a chat, a call note or a message, and the sentences worth keeping become proposals the founder
ticks into the brain as approved records.

The extractor reuses the rules in ingest.py (headings, key: value lines, bullets, tried-and-failed, never-say,
decided) on the pasted text, then adds the sentence patterns a chat carries: "from now on", "going forward", "we
always", "we never", "remember that", "our X is Y". Each proposal has a kind (decision, red line, learning, fact), the
section and field it would fill, the sentence it came from and, for a fact, the value parsed from it. Nothing is
written until the founder confirms ticked items; a confirmed item is an approved founder record with the sentence as
evidence: a decision (decisions section, dated, with the reason when the sentence has one), a red line (a forbidden
claim the scanner blocks), a learning (what was tried and how it went), a fact (the field in its section). Web pass
idea 11. No model: patterns and the founder's tick.
"""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
_ispec = importlib.util.spec_from_file_location("brand_brain_ingest_for_remember", HERE / "ingest.py")
ingest = importlib.util.module_from_spec(_ispec)
_ispec.loader.exec_module(ingest)

FROM_NOW = re.compile(r"\b(from now on|going forward|starting (?:today|now|next)|we (?:will|'ll) always|we always|let's always|always)\b", re.I)
NEVER = re.compile(r"\b(we never|never again|let's never|do not ever|don't ever|never)\b", re.I)
REMEMBER = re.compile(r"\b(remember that|remember:|note that|for the record|to be clear|keep in mind)\b", re.I)
FACT = re.compile(r"\b(?:our|the|remember that(?: our| the)?|note that(?: our| the)?)\s+([a-z0-9][a-z0-9 ]{1,40}?)\s+(?:is|are|will be|costs?|runs?|stays?)\s+([^.;\n]{2,80})", re.I)
REASON = re.compile(r"\b(because|since|so that|as)\b\s+([^.;\n]{4,160})", re.I)
MAX_ITEMS = 40


def _sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+|\n+", text or "")
    return [p.strip() for p in parts if len(p.strip()) >= 12]


def _strip_lead(s: str) -> str:
    return re.sub(r"^\s*(?:[-*•]\s*|\[[^\]]*\]\s*|[A-Z][a-z]+:\s*|\d{1,2}:\d{2}\s*)", "", s).strip()


def propose(brain, text: str) -> dict:
    today = brain.today.isoformat()
    items: list[dict] = []
    seen: set[str] = set()

    def add(kind, section, field, sentence, value=None, why=None):
        key = re.sub(r"[^a-z0-9]+", " ", sentence.lower()).strip()[:60]
        if key in seen or len(items) >= MAX_ITEMS:
            return
        seen.add(key)
        items.append({"n": len(items) + 1, "kind": kind, "section": section, "field": ingest.slug(field, 50), "text": sentence.strip()[:400], "value": value, "why": why, "tick": kind != "fact" or value is not None})

    # the chat patterns first: they carry the value and the reason
    for s in _sentences(text):
        s2 = _strip_lead(s)
        if not s2:
            continue
        m_reason = REASON.search(s2)
        reason = m_reason.group(2).strip() if m_reason else None
        if ingest.FORBID.search(s2) or (NEVER.search(s2) and re.search(r"\b(say|claim|promise|call|use the word|write)\b", s2, re.I)):
            phrase = re.split(r"\b(?:never say|do not say|don't say|must not say|must never say|never claim|never write|never use the word|never call it|we never say)\b", s2, maxsplit=1, flags=re.I)
            tail = phrase[-1].strip().strip('"\'.') if len(phrase) > 1 else ""
            tail = re.split(r"[,;:]", tail, maxsplit=1)[0].strip().strip('"\'.')
            add("red_line", "claims", "never_say_" + (tail[:30] or s2[:30]), s2, tail or None, reason)
        elif ingest.DECIDED.search(s2) or FROM_NOW.search(s2):
            add("decision", "decisions", s2[:50], s2, None, reason)
        elif ingest.TRIED.search(s2):
            add("learning", "learnings", s2[:50], s2, None, reason)
        elif REMEMBER.search(s2) or FACT.search(s2):
            m = FACT.search(s2)
            if m:
                field = m.group(1).strip()
                sec = ingest.section_for(field + " " + s2, None) or ingest.section_for(s2, "identity")
                add("fact", sec, field, s2, ingest._coerce(m.group(2).strip()), reason)
            else:
                add("decision", "decisions", s2[:50], s2, None, reason)
    # then the file rules: headings, key: value lines and bullets the sentence pass does not see
    for r in ingest.extract(text, brain.brand, f"documents/remember-{today}.txt", today):
        f = r["field"]
        fld = f.split("_", 1)[1] if "_" in f else f
        kind = {"decisions": "decision", "learnings": "learning"}.get(r["section"], "red_line" if r["section"] == "claims" and r.get("tier") == "forbidden" else "fact")
        add(kind, r["section"], fld, r["text"], r.get("value") if kind == "fact" else None)
    counts = {k: sum(1 for i in items if i["kind"] == k) for k in ("decision", "red_line", "learning", "fact")}
    return {"items": items, "counts": dict(counts, total=len(items)), "sentences": len(_sentences(text)),
            "note": "Patterns over your text: decisions (we decided, from now on), red lines (never say), learnings (we tried, did not work), facts (our X is Y, key: value). Tick what is true, edit the section or field, confirm. Each becomes an approved founder record with the sentence as evidence; nothing else is written."}


def records(brain, items: list[dict]) -> tuple[list[dict], list[dict]]:
    today = brain.today.isoformat()
    out, bad = [], []
    for it in items[:MAX_ITEMS]:
        kind = it.get("kind")
        sentence = str(it.get("text") or "").strip()[:400]
        section = str(it.get("section") or "").strip()
        field = ingest.slug(str(it.get("field") or sentence[:40]), 50)
        if not sentence or kind not in ("decision", "red_line", "learning", "fact") or not field:
            bad.append({"item": it, "error": "kind, text and field are required"})
            continue
        src = {"type": "founder", "ref": "05-brand-brain remember this", "captured_at": today}
        ev = [{"quote": sentence[:300], "ref": "pasted note, " + today}]
        if kind == "decision":
            rec = {"id": f"{brain.brand}.decisions.{field}", "brand": brain.brand, "section": "decisions", "field": field, "value": {"decision": sentence, "reason": (it.get("why") or None), "decided_on": today}, "text": sentence + (f" Reason: {it['why']}" if it.get("why") else ""), "tier": "approved", "confidence": 1.0, "visibility": "private", "source": src, "evidence": ev}
        elif kind == "red_line":
            phrase = str(it.get("value") or "").strip().strip('"\'.')
            rec = {"id": f"{brain.brand}.claims.{field}", "brand": brain.brand, "section": "claims", "field": field, "value": phrase or sentence, "text": ("Never say " + phrase.rstrip(".") + ".") if phrase else sentence, "tier": "forbidden", "confidence": 1.0, "visibility": "private", "source": src, "evidence": ev}
        elif kind == "learning":
            rec = {"id": f"{brain.brand}.learnings.{field}", "brand": brain.brand, "section": "learnings", "field": field, "value": {"learning": sentence, "kind": "tried", "noted_on": today}, "text": sentence, "tier": "approved", "confidence": 1.0, "visibility": "private", "source": src, "evidence": ev}
        else:
            if section not in ingest.SECTIONS if hasattr(ingest, "SECTIONS") else False:
                bad.append({"item": it, "error": "unknown section"})
                continue
            rec = {"id": f"{brain.brand}.{section}.{field}", "brand": brain.brand, "section": section, "field": field, "value": it.get("value") if it.get("value") is not None else sentence, "text": sentence, "tier": "approved", "confidence": 1.0, "visibility": "private", "source": src, "evidence": ev}
        out.append(rec)
    return out, bad
