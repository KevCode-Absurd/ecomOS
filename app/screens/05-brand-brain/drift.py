"""Positioning drift from the language bank: the words the positioning claims against the words customers use.

The positioning's key words come from the positioning frame, the one-line pitch and the voice adjectives. The
customers' words come from the language bank: the phrases and the review quotes, praise and complaint apart. For each
positioning word: the share of praise quotes that echo it (the word or its stem) and the share of complaint quotes
that contradict it (the same word in a complaint). The drift list is the customer words used most that the
positioning does not carry. A drift brief is drafted from the counts: what customers say, what we say, the words to
add or drop. Rule BRN-R32 fires when the positioning is echoed by fewer than ECHO_FLOOR of praise quotes, or when a
positioning word appears in more complaints than praise. No survey, no model: word counts from the records. Web pass
idea 25, without the paid survey.
"""
from __future__ import annotations

import re

ECHO_FLOOR = 0.2
STOP = set("""the a an and or of to in on for with is are was were be it its this that these those i my me you your we our us they them their so very just
really also like get got one two pair pairs sock socks bombas brand from have has had this than then there here more most some such only into over about after before because
every which what when who will would could should can not but did does doing done been being too all any each other both same own out off up down back way well still even
been while these those where why how much many little long know think feel felt made make makes made buy bought wear wore worn
proof points point against appears appear carry carries comments comment posts post frame frames reddit first second third four three five percent revenue line sells sell
led lead largest ask asks whether ordinary discussed discussion set sets direct story mark count details everything purchase purchased purchases someone gives give
describes described objections objection positioning under used corp engineered purpose extreme products product life basics growth technical recommends recommended sock's""".split())
GENERIC_PRAISE = {"great", "love", "loved", "best", "good", "nice", "amazing", "awesome", "perfect", "favorite", "favourite", "recommend", "highly", "excellent", "happy", "glad", "really", "definitely", "absolutely", "wonderful", "fantastic"}
SYNONYMS = {"comfort": ["comfort", "comfy", "comfortable", "cozy", "cosy"], "soft": ["soft", "softest", "softness"], "giving": ["give", "gives", "giving", "donate", "donated", "donation", "shelter", "mission"],
            "quality": ["quality", "well made", "well-made", "premium"], "durable": ["durable", "durability", "last", "lasted", "lasts", "hold up", "held up", "wear out", "worn out", "hole", "holes", "pilling"],
            "warm": ["warm", "warmth"], "fit": ["fit", "fits", "fitted", "snug", "tight", "loose"], "thick": ["thick", "thickness", "cushion", "cushioned", "padding"], "price": ["price", "priced", "expensive", "worth", "value", "cost", "overpriced"],
            "everyday": ["everyday", "every day", "daily"], "performance": ["athletic", "performance", "running", "workout", "gym", "hike", "hiking"]}
POS_FIELDS = [("positioning", "frame"), ("identity", "one_line_pitch"), ("voice", "adjectives"), ("positioning", "proof_points")]


def _words(s) -> list[str]:
    return [w for w in (x.strip("'-") for x in re.findall(r"[a-z][a-z'-]{2,}", str(s or "").lower())) if len(w) >= 3 and w not in STOP]


def _key_for(word: str) -> str:
    for k, syns in SYNONYMS.items():
        if word == k or word in syns:
            return k
    return word


def positioning_words(brain) -> tuple[list[str], list[dict]]:
    sources, words = [], []
    for sec, field in POS_FIELDS:
        rows = [r for r in brain.records(sec) if r["id"] == f"{brain.brand}.{sec}.{field}"] or [r for r in brain.records(sec) if r.get("field") == field and not (r.get("field") == "frame" and "reddit" in r["id"])]
        if not rows:
            continue
        r = rows[0]
        if isinstance(r.get("value"), list):
            text = " ".join(str(x) for x in r["value"])  # proof points and adjectives: the list, not the sentence about it
        else:
            text = r.get("text") if isinstance(r.get("text"), str) else str(r.get("value") or "")
        ws = [_key_for(w) for w in _words(text)]
        sources.append({"record": r["id"], "tier": r["tier"], "text": (text or "")[:160]})
        words += ws
    counts: dict[str, int] = {}
    for w in words:
        counts[w] = counts.get(w, 0) + 1
    keys = [w for w, _ in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))]
    return keys[:20], sources


def customer_quotes(brain) -> tuple[list[str], list[str]]:
    praise, complaint = [], []
    for r in brain.records("language_bank"):
        v = r.get("value") if isinstance(r.get("value"), dict) else {}
        theme = str(v.get("theme") or "")
        bucket = praise if theme in ("praise", "result", "surprise", "gift") else (complaint if theme == "complaint" else None)
        if bucket is None:
            continue
        if v.get("phrase"):
            bucket.append(str(v["phrase"]))
        for q in v.get("reviews") or []:
            if isinstance(q, dict) and q.get("quote"):
                bucket.append(str(q["quote"]))
    return praise, complaint


def _mentions(quotes: list[str], key: str) -> int:
    syns = SYNONYMS.get(key, [key])
    pats = [re.compile(r"\b" + re.escape(s) + r"\w*", re.I) for s in syns]
    return sum(1 for q in quotes if any(p.search(q) for p in pats))


def analysis(brain) -> dict:
    keys, sources = positioning_words(brain)
    praise, complaint = customer_quotes(brain)
    if not keys or not (praise or complaint):
        return {"available": False, "reason": "no positioning frame or no language bank quotes to compare" if not keys else "no customer quotes in the language bank", "positioning": [], "customer_words": [], "sources": sources,
                "counts": {"praise_quotes": len(praise), "complaint_quotes": len(complaint), "positioning_words": len(keys)}}
    rows = []
    for k in keys:
        p, c = _mentions(praise, k), _mentions(complaint, k)
        if len(k) < 4:
            continue
        rows.append({"word": k, "praise": p, "praise_share": round(p / len(praise), 3) if praise else None, "complaint": c, "complaint_share": round(c / len(complaint), 3) if complaint else None,
                     "verdict": "contradicted" if c > p and c >= 3 else ("echoed" if praise and p / len(praise) >= 0.05 else "not echoed")})
    cust: dict[str, int] = {}
    for q in praise:
        seen = set()
        for w in _words(q):
            k = _key_for(w)
            if k not in seen:
                cust[k] = cust.get(k, 0) + 1
                seen.add(k)
    posset = set(keys)
    customer_words = [{"word": w, "praise": n, "praise_share": round(n / len(praise), 3), "in_positioning": w in posset, "generic": w in GENERIC_PRAISE} for w, n in sorted(cust.items(), key=lambda kv: (-kv[1], kv[0]))[:18]]
    echoed_any = sum(1 for q in praise if any(_mentions([q], k) for k in keys[:8])) if praise else 0
    echo_share = round(echoed_any / len(praise), 3) if praise else None
    contradicted = [r for r in rows if r["verdict"] == "contradicted"]
    missing = [w for w in customer_words if not w["in_positioning"] and not w["generic"]][:6]
    drift = (echo_share is not None and echo_share < ECHO_FLOOR) or bool(contradicted)
    brief = [f"Positioning drift check for {brain.brand}", f"We say: {', '.join(keys[:8])}.", f"Customers who praise us say: {', '.join(w['word'] for w in customer_words[:8])}.",
             f"{round((echo_share or 0) * 100)} percent of {len(praise)} praise quotes echo one of our top 8 words. Generic praise (great, love, best) is not counted as a candidate."]
    if contradicted:
        brief.append("Contradicted in complaints: " + "; ".join(f"{r['word']} ({r['complaint']} complaints, {r['praise']} praise)" for r in contradicted) + ". Prove it or drop it from the frame.")
    if missing:
        brief.append("Words customers use that the frame does not: " + ", ".join(f"{w['word']} ({w['praise']})" for w in missing) + ". Candidates to add, with proof.")
    brief.append("Next: redraft the frame with the customers' words, keep every claim tied to a record, and re-run this check.")
    return {"available": True, "positioning": rows, "customer_words": customer_words, "sources": sources, "echo_share": echo_share, "echo_floor": ECHO_FLOOR, "contradicted": [r["word"] for r in contradicted], "missing": [w["word"] for w in missing], "drift": drift,
            "counts": {"praise_quotes": len(praise), "complaint_quotes": len(complaint), "positioning_words": len(keys), "echoed": sum(1 for r in rows if r["verdict"] == "echoed"), "not_echoed": sum(1 for r in rows if r["verdict"] == "not echoed"), "contradicted": len(contradicted)},
            "brief": "\n".join(brief), "note": "Word counts over the language bank's praise and complaint quotes against the words in the positioning frame, the pitch, the voice adjectives and the proof points. Synonyms are grouped (comfort with comfy and cosy, giving with donate and shelter). No survey and no model; a word echoed in praise is one the customers give us."}
