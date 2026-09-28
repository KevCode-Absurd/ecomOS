"""The brand's own words: the names and spellings agents must get right, read from the records and checked by the
scanner.

Terms come from the records: the brand name, the product lines, the named programmes and parts in approved and
site-backed claims (capitalised runs of 2 or more words: Happiness Guarantee, Honeycomb Arch Support System), the
codes (COMFORT20), and the founder's own terms (`voice.term_<slug>`: the term, the wrong spellings, a note). The
scanner's spelling check flags a draft that writes a term with other casing (happiness guarantee) or a listed wrong
spelling (Bombass), with the right form. The brain file lists the glossary under strict rules. No dictionary and no
model: the records are the spelling.
"""
from __future__ import annotations

import re

PROPER = re.compile(r"\b((?:[A-Z][a-zA-Z0-9-]+)(?:\s+(?:[A-Z][a-zA-Z0-9-]+|of|and|the)){1,4})\b")
SKIP_WORDS = {"The", "A", "An", "In", "On", "For", "With", "Bombas", "Reddit", "Amazon", "Meta", "Google", "Shark", "Tank", "United", "States", "New", "York", "Season", "Trustpilot"}
SKIP_TERMS = {"Shark Tank", "New York", "United States", "Ad Library", "Meta Ad Library", "B Corp", "Certified B Corp"}


def founder_terms(brain) -> list[dict]:
    out = []
    for r in brain.records("voice"):
        if (r.get("field") or "").startswith("term_") and isinstance(r.get("value"), dict) and r["value"].get("term"):
            v = r["value"]
            out.append({"term": v["term"], "wrong": [w for w in (v.get("wrong") or []) if isinstance(w, str)], "note": v.get("note"), "source": "founder", "record": r["id"]})
    return out


def terms(brain) -> dict:
    found: dict[str, dict] = {}

    def add(term, source, record, note=None, wrong=None):
        t = term.strip()
        if len(t) < 3 or t in SKIP_TERMS or t.lower() in {k.lower() for k in found if k != t}:
            if t.lower() in {k.lower() for k in found} and t not in found:
                return
        if t not in found:
            found[t] = {"term": t, "source": source, "record": record, "note": note, "wrong": list(wrong or [])}
    name = next((r for r in brain.records("identity") if r.get("field") == "name" and isinstance(r.get("value"), str)), None)
    if name:
        add(name["value"], "identity", name["id"], "the brand name, as customers write it")
    else:
        add(brain.brand.replace("_", " ").title(), "brand", None, "the brand name")
    lines = next((r for r in brain.records("products") if r.get("field") == "lines" and isinstance(r.get("value"), list)), None)
    if lines:
        for x in lines["value"]:
            if isinstance(x, str) and x[:1].isupper() and len(x.split()) >= 2:  # a single common word (Socks) is not a spelling rule
                add(x, "products", lines["id"], "a product line")
    for r in brain.records("claims") + brain.records("policies") + brain.records("offers"):
        if r["tier"] not in ("approved", "site_backed"):
            continue
        text = r.get("text") if isinstance(r.get("text"), str) else ""
        for m in PROPER.finditer(text):
            t = m.group(1).strip()
            words = t.split()
            if words[0] in SKIP_WORDS and len(words) == 2 or t in SKIP_TERMS or all(w in SKIP_WORDS for w in words):
                continue
            if m.start() == 0 or text[max(0, m.start() - 2):m.start()].strip() in (".", "!", "?"):
                continue  # a sentence start is not a name
            add(t, r["section"], r["id"], "a named programme or part")
        v = r.get("value")
        code = v.get("code") if isinstance(v, dict) else (v if isinstance(v, str) and r.get("field", "").endswith("code_confirmed") else None)
        if isinstance(code, str) and re.fullmatch(r"[A-Z0-9]{4,20}", code):
            add(code, r["section"], r["id"], "a code, always in capitals")
    for ft in founder_terms(brain):
        found[ft["term"]] = {"term": ft["term"], "source": "founder", "record": ft["record"], "note": ft["note"], "wrong": ft["wrong"]}
    rows = sorted(found.values(), key=lambda x: ({"identity": 0, "brand": 0, "founder": 1, "products": 2}.get(x["source"], 3), x["term"]))
    return {"terms": rows, "counts": {"terms": len(rows), "founder": sum(1 for x in rows if x["source"] == "founder")},
            "note": "Names and spellings from the records: the brand, the product lines, the named programmes and parts in approved or site-backed claims, the codes, and your own terms. The scanner flags other casing or a listed wrong spelling; the brain file lists them under strict rules."}


def check(brain, text: str) -> list[dict]:
    hits = []
    t = text or ""
    for row in terms(brain)["terms"]:
        term = row["term"]
        if len(term) < 3:
            continue
        for m in re.finditer(r"(?<![A-Za-z0-9])" + re.escape(term) + r"(?![A-Za-z0-9])", t, re.I):
            if m.group(0) != term:
                hits.append({"kind": "spelling", "severity": "warn", "match": m.group(0), "record": row.get("record"), "tier": "glossary", "fix": f"Write it as {term}."})
                break
        for w in row.get("wrong") or []:
            if w and re.search(r"(?<![A-Za-z0-9])" + re.escape(w) + r"(?![A-Za-z0-9])", t, re.I):
                hits.append({"kind": "spelling", "severity": "warn", "match": w, "record": row.get("record"), "tier": "glossary", "fix": f"Write it as {term}."})
    return hits


def term_record(brain, body: dict) -> dict | tuple[int, dict]:
    term = str(body.get("term") or "").strip()[:80]
    if len(term) < 2:
        return 400, {"error": "term is required"}
    wrong = body.get("wrong") if isinstance(body.get("wrong"), list) else [x.strip() for x in str(body.get("wrong") or "").split(",") if x.strip()]
    key = re.sub(r"[^a-z0-9]+", "_", term.lower()).strip("_")[:50]
    v = {"term": term, "wrong": [str(w)[:60] for w in wrong][:10], "note": str(body.get("note") or "").strip()[:160] or None}
    return {"id": f"{brain.brand}.voice.term_{key}", "brand": brain.brand, "section": "voice", "field": f"term_{key}", "value": v, "text": f"Write {term}" + (", never " + ", ".join(v["wrong"]) if v["wrong"] else "") + "." + (f" {v['note']}" if v["note"] else ""),
            "tier": "approved", "confidence": 1.0, "visibility": "private", "source": {"type": "founder", "ref": "05-brand-brain glossary", "captured_at": brain.today.isoformat()}}
