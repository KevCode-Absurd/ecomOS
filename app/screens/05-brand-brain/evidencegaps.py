"""Strong records without evidence: a record at tier site_backed or evidence should carry the quote it rests on
(`evidence: [{quote, ref}]`) or be a quote itself. In the fact sections, one that carries neither is a tier the
records cannot back, and every package hands it to agents as a strong fact. Each gap ends in one of three moves:
the agent re-reads the source and attaches the quote (a url or a file), the founder approves it by hand (it becomes
a founder fact, on their word), or it is retired. Rule BRN-R41 keeps the list on the master list.
"""
from __future__ import annotations

FACT_SECTIONS = {"identity", "positioning", "products", "offers", "policies", "claims", "voice", "visual", "story_bank", "content", "seo_facts",
                 "avatars", "calendar", "economics", "operations", "channels", "stack", "site_map", "diagnosis"}
STRONG = ("site_backed", "evidence")
QUOTE_KEYS = ("reviews", "quotes", "pdp", "url", "urls", "evidence_urls")


def _is_quote_itself(rec: dict) -> bool:
    v = rec.get("value")
    return isinstance(v, dict) and any(k in v for k in QUOTE_KEYS)


def _fix(src: dict) -> tuple[str, str]:
    ref = str(src.get("ref") or "")
    if ref.startswith("http"):
        return "re-read", "re-read the page and attach the line that backs it"
    if ref.startswith("apify:"):
        return "attach", "the actor run is the source: attach the item text as the quote, or approve it by hand"
    if ref and "." in ref.rsplit("/", 1)[-1]:
        return "re-read", "re-read the file and attach the line that backs it"
    return "decide", "no source to re-read: approve it by hand or retire it"


def gaps(brain) -> dict:
    rows = []
    for r in brain.records():
        if r["section"] not in FACT_SECTIONS or r.get("tier") not in STRONG:
            continue
        if r.get("evidence") or _is_quote_itself(r):
            continue
        src = r.get("source") or {}
        kind, fix = _fix(src)
        rows.append({"id": r["id"], "section": r["section"], "field": r.get("field"), "tier": r["tier"], "text": str(r.get("text") or r.get("value"))[:160],
                     "source_type": src.get("type"), "source_ref": str(src.get("ref") or "")[:120], "date": None if r["date"] == "undated" else r["date"], "fix_kind": kind, "fix": fix})
    rows.sort(key=lambda x: ({"site_backed": 0, "evidence": 1}[x["tier"]], x["section"], x["id"]))
    by_section: dict[str, int] = {}
    for x in rows:
        by_section[x["section"]] = by_section.get(x["section"], 0) + 1
    checked = sum(1 for r in brain.records() if r["section"] in FACT_SECTIONS and r.get("tier") in STRONG)
    return {"gaps": rows, "counts": {"gaps": len(rows), "checked": checked, "by_section": dict(sorted(by_section.items(), key=lambda kv: -kv[1])), "by_fix": {k: sum(1 for x in rows if x["fix_kind"] == k) for k in ("re-read", "attach", "decide")}},
            "note": "Strong-tier records in the fact sections with no quote behind them. Attach the quote, approve by hand (it becomes your fact), or retire. Quotes themselves (the language bank, review summaries) are not counted."}
