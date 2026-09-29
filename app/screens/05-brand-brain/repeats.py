"""What buyers say most: the language bank's review phrases counted by word and by exact line, per theme (praise,
complaint, mixed, result), against the strong claims. A word said 5 times or more with no approved or site backed
claim carrying it is a claim the brand could make on its buyers' word: the agent drafts it as a review-backed claim
(tier evidence) with the quotes attached, and the founder approves or not. Rule BRN-R44 keeps the uncovered words
on the master list. Reviews are counted, never quoted as testimonials; usernames are never stored.
"""
from __future__ import annotations

import re

STOP = {"the", "and", "for", "with", "that", "this", "from", "are", "was", "were", "has", "have", "its", "our", "you", "your", "but", "can", "all", "any", "one", "per",
        "than", "then", "they", "them", "their", "will", "each", "more", "most", "also", "when", "what", "which", "about", "these", "those", "very", "just", "really",
        "socks", "sock", "pair", "pairs", "bombas", "product", "products", "would", "could", "been", "them", "into", "only", "some", "much", "too", "not", "ever", "got", "get", "buy", "bought"}
GENERIC = {"great", "good", "best", "love", "loved", "perfect", "nice", "awesome", "amazing", "excellent", "wonderful", "fantastic", "happy", "show", "well", "recommend", "highly", "like", "these"}  # praise with no fact in it, or a product term (no show)
MIN_MENTIONS = 5
STRONG = ("approved", "site_backed")
THEMES = ("praise", "complaint", "mixed", "result", "surprise", "gift")


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9 ]+", " ", (s or "").lower()).strip()


def _words(s: str) -> list[str]:
    return [w for w in _norm(s).split() if len(w) >= 4 and w not in STOP]


def _stem(w: str) -> str:
    for suf in ("iest", "ier", "ing", "ness", "est", "ers", "er", "ed", "ly", "es", "s"):
        if w.endswith(suf) and len(w) - len(suf) >= 4:
            return w[: -len(suf)]
    return w


def build(brain) -> dict:
    claims = [c for c in brain.records("claims") if c.get("tier") in STRONG]
    claim_words = {}
    for c in claims:
        for w in _words(c.get("text") or ""):
            claim_words.setdefault(_stem(w), c["id"])
    themes = {}
    lines = {}
    for r in brain.records("language_bank"):
        v = r.get("value") if isinstance(r.get("value"), dict) else {}
        phrase = str(v.get("phrase") or "")
        theme = str(v.get("theme") or "other")
        if not phrase:
            continue
        key = _norm(phrase)
        ln = lines.setdefault(key, {"phrase": phrase, "theme": theme, "times": 0, "products": set()})
        ln["times"] += 1
        if v.get("asin"):
            ln["products"].add(str(v["asin"]))
        t = themes.setdefault(theme, {"theme": theme, "phrases": 0, "words": {}})
        t["phrases"] += 1
        seen = set()
        for w in _words(phrase):
            st = _stem(w)
            if st in seen:
                continue
            seen.add(st)
            e = t["words"].setdefault(st, {"word": st, "mentions": 0, "products": set(), "samples": []})
            e["mentions"] += 1
            if v.get("asin"):
                e["products"].add(str(v["asin"]))
            if len(e["samples"]) < 3 and phrase not in e["samples"]:
                e["samples"].append(phrase[:80])
    out_themes = []
    for theme in sorted(themes, key=lambda t: (THEMES.index(t) if t in THEMES else 9)):
        t = themes[theme]
        words = sorted(t["words"].values(), key=lambda e: (-e["mentions"], e["word"]))[:15]
        rows = [{"word": e["word"], "mentions": e["mentions"], "products": len(e["products"]), "samples": e["samples"], "covered_by": claim_words.get(e["word"]),
                 "generic": e["word"] in GENERIC,
                 "claimable": theme == "praise" and e["mentions"] >= MIN_MENTIONS and not claim_words.get(e["word"]) and e["word"] not in GENERIC} for e in words]
        out_themes.append({"theme": theme, "phrases": t["phrases"], "words": rows})
    repeats = sorted([{"phrase": x["phrase"], "theme": x["theme"], "times": x["times"], "products": len(x["products"])} for x in lines.values() if x["times"] >= 2], key=lambda x: (-x["times"], x["phrase"]))[:20]
    claimable = [w for t in out_themes for w in t["words"] if w["claimable"]]
    return {"themes": out_themes, "repeats": repeats, "claimable": claimable,
            "counts": {"phrases": sum(t["phrases"] for t in out_themes), "themes": len(out_themes), "repeats": len(repeats), "claimable": len(claimable), "strong_claims": len(claims)},
            "note": f"Review phrases counted by word and by exact line per theme. A praise word said {MIN_MENTIONS} times or more with no strong claim carrying it can become a review-backed claim, drafted with the quotes attached, for you to approve. Counts only; reviews are never quoted as testimonials."}


def claim_record(brain, word: str, view: dict) -> dict | None:
    hit = next((w for t in view["themes"] if t["theme"] == "praise" for w in t["words"] if w["word"] == word), None)
    if hit is None or not hit["claimable"]:
        return None
    quotes = []
    for r in brain.records("language_bank"):
        v = r.get("value") if isinstance(r.get("value"), dict) else {}
        phrase = str(v.get("phrase") or "")
        if word in {_stem(x) for x in _words(phrase)} and str(v.get("theme")) == "praise":
            quotes.append({"quote": phrase[:200], "ref": f"language bank {r['id']}", "captured_at": brain.today.isoformat()})
        if len(quotes) >= 5:
            break
    today = brain.today.isoformat()
    return {"id": f"{brain.brand}.claims.buyers_say_{word}", "brand": brain.brand, "section": "claims", "field": f"buyers_say_{word}",
            "value": {"word": word, "mentions": hit["mentions"], "products": hit["products"], "basis": "review phrases in the language bank"},
            "text": f"Buyers say '{word}': {hit['mentions']} review phrases across {hit['products']} product{'s' if hit['products'] != 1 else ''} use the word.",
            "tier": "evidence", "confidence": 0.6, "visibility": "private", "evidence": quotes,
            "source": {"type": "review", "ref": "05-brand-brain what buyers say most", "captured_at": today}}
