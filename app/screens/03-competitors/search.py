"""Search overlap: which search terms the tracked pages go after, which we share, and which we leave.

Real overlap (the keywords both rank or bid on, positions, volume) needs a keyword source and reads
unavailable; rule COMP-R23 turns that into a connect action. Rule COMP-R22: GAP_TERMS (3) or more seeds
they use and our lines never say become a keyword check brief (agent). What we can do today is a seed list built by
rules from public lines in the brain: every phrase ending in the brand's category word (socks for a sock brand; up to 3 words before it) in
each page's positioning, push line and hook labels (kept as the word before it plus the category word),
plus "<material or angle word> <category word>" from its angle tags. A seed on 2 or more pages is contested; a seed only they use is a gap for us to check; a seed
in our own lines is ours. The list goes to the Google Ads and SEO screens as a keyword check brief.
"""
from __future__ import annotations

import re

STOP = {"and", "or", "the", "with", "for", "of", "a", "to", "in", "our", "your", "their", "new", "best", "online-only"}
GAP_TERMS = 3
def seeds_from(texts: list[str], angle_words: list[str], term: str = "socks") -> set[str]:
    """term is the brand's category word from the brain (audit.category_term): socks, hats, candles."""
    one = term[:-1] if term.endswith("s") else term
    phrase = re.compile(r"((?:[a-z][a-z-]*\s){0,3}" + re.escape(one) + r"s?)\b")
    out = set()
    for t in texts:
        for m in phrase.finditer(str(t or "").lower()):
            words = [w for w in m.group(1).split() if w not in STOP]
            if len(words) >= 2:   # the word right before the category word carries the intent: running, merino, relief
                out.add(f"{words[-2]} {term}")
    for w in angle_words:
        if w and len(w) > 3:
            out.add(f"{w} {term}")
    return out


def build(m: dict, brain) -> dict:
    term = (m.get("term") or {}).get("plural", "socks")
    get = lambda k: (brain.get(f"{brain.brand}.{k}") or {}).get("value")  # noqa: E731
    by_page = {}
    for p in m["pages"]:
        if p["role"] == "self" or p["source"] == "none":
            continue
        words = [a["word"] for a in p["angles"] if a["tag"] in ("material", "relief", "performance", "durability")]
        by_page[p["name"]] = seeds_from(p["hook_labels"] + [p["positioning"], p["push"]], words, term)
    us = next(p for p in m["pages"] if p["role"] == "self")
    ours_texts = list(m["profile"]["_texts"]) + [str(x) for x in (get("products.materials") or [])] + list(us["hook_labels"])
    ours = seeds_from(ours_texts, [a["word"] for a in us["angles"] if a["tag"] in ("material", "relief", "performance", "durability")], term)
    ours |= {f"{x.split('/')[0].split()[0].strip()} {term}" for x in (get("products.materials") or []) if isinstance(x, str)}
    terms = {}
    for page, ss in by_page.items():
        for s in ss:
            terms.setdefault(s, []).append(page)
    rows = []
    for t, pages in terms.items():
        mine = any(set(t.split()) <= set(o.split()) for o in ours)
        rows.append({"term": t, "pages": sorted(pages), "n": len(pages), "ours": mine,
                     "kind": "shared" if mine else ("contested" if len(pages) >= 2 else "gap")})
    rows.sort(key=lambda r: (-r["n"], r["ours"], r["term"]))
    return {"rows": rows, "ours_only": sorted(o for o in ours if o not in terms), "overlap": None,
            "overlap_reason": "no keyword source: rankings, bids and volumes need a search data connector",
            "rule": f"Seeds by rule from public lines: phrases ending in the category word ({term}), plus material and angle words. "
                    "Contested: on 2 or more pages. Gap: only they use it. Shared: in our lines too."}


def draft(s: dict, brand: str) -> str:
    gaps = [r["term"] for r in s["rows"] if not r["ours"]][:12]
    shared = [r["term"] for r in s["rows"] if r["ours"]][:8]
    return "\n".join([f"Keyword check brief for {brand}.",
                      "Check volume, cost per click and who ranks for: " + (", ".join(gaps) if gaps else "none") + ".",
                      "Defend where we already say it: " + (", ".join(shared) if shared else "none") + ".",
                      "Hand the terms with volume to the Google Ads and SEO screens. Never bid on a competitor's brand name "
                      "without the founder's yes."])
