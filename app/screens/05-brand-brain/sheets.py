"""Product line fact sheets: one sheet per product line, built from the records, for anyone who writes about a line.
Each sheet holds what the site says about the line (claims by tier), the price ladder and pack sizes, the materials,
what buyers say (review summaries: count, average, praise, issues), the objections that name it, the red lines that
name it, and the claims that still need proof. Lines come from the products `lines` record; the review summaries
map to lines by their product_line key. Everything is matched in code by the line's own words; nothing is written.
"""
from __future__ import annotations

import re

LINE_WORDS = {"socks": ["sock"], "underwear": ["underwear", "boxer", "brief"], "t-shirts": ["t-shirt", "tee", "shirt"], "slippers": ["slipper"],
              "sleeves": ["sleeve"], "bralettes": ["bralette"], "clog": ["clog"], "moccasin": ["moccasin"], "sandals": ["sandal"], "bags": ["bag"], "giftcard": ["gift card"]}
REVIEW_LINE = {"ankle": "socks", "calf": "socks", "no_show": "socks", "merino": "socks", "compression": "socks", "quarter": "socks", "knee": "socks",
               "slippers": "slippers", "underwear": "underwear", "t_shirts": "t-shirts", "tshirts": "t-shirts", "sleeves": "sleeves"}
STRONG = ("approved", "site_backed")


def _name(raw: str) -> str:
    return re.sub(r"\s+", " ", (raw or "").strip().lower())


def lines(brain) -> list[str]:
    rec = next((r for r in brain.records("products") if r.get("field") == "lines" and isinstance(r.get("value"), list)), None)
    names = [_name(x) for x in (rec["value"] if rec else []) if isinstance(x, str)]
    out = []
    for n in names:
        if any(n != o and o in n for o in names):  # "plunge bralettes" folds into "bralettes"
            continue
        if n not in out:
            out.append(n)
    return out


def _mentions(text: str, words: list[str]) -> bool:
    t = (text or "").lower()
    return any(re.search(rf"(?<![a-z]){re.escape(w)}", t) for w in words)


def build(brain, redlines: list[dict], tokens) -> dict:
    prods = brain.records("products")
    claims = brain.records("claims")
    objections = brain.records("objections")
    sheets = []
    for line in lines(brain):
        words = LINE_WORDS.get(line, [line.rstrip("s")])
        key = line.replace("-", "_").replace(" ", "_")
        ladder = next((r for r in prods if r.get("field") == f"price_ladder_{key}" and isinstance(r.get("value"), dict)), None)
        packs = next((r for r in prods if r.get("field") == "pack_sizes" and isinstance(r.get("value"), list)), None) if line in ("socks", "underwear") else None
        mats = next((r for r in prods if r.get("field") == "materials" and isinstance(r.get("value"), list)), None) if line == "socks" else None
        gift = next((r for r in prods if r.get("field") == "gift_card" and isinstance(r.get("value"), dict)), None) if line == "giftcard" else None
        reviews = [r for r in prods if r.get("field") == "review_summary" and isinstance(r.get("value"), dict) and REVIEW_LINE.get(str(r["value"].get("product_line") or "").lower()) == line]
        line_claims = [c for c in claims if _mentions(c.get("text") or "", words) and c.get("tier") != "forbidden"]
        strong = [c for c in line_claims if c.get("tier") in STRONG]
        weak = [c for c in line_claims if c.get("tier") not in STRONG]
        objs = [o for o in objections if _mentions(o.get("text") or "", words)]
        reds = [x for x in redlines if _mentions(str(x.get("phrase") or x.get("text") or ""), words)]
        total_reviews = sum(int(r["value"].get("yotpo_review_total") or 0) for r in reviews)
        avg = (sum(float(r["value"].get("yotpo_average") or 0) * int(r["value"].get("yotpo_review_total") or 0) for r in reviews) / total_reviews) if total_reviews else None
        out = [f"# {line.title()}: fact sheet", ""]
        out += ["## What the site says (use as written)", ""] + ([f"- {c['text']} [{c['tier']}]" for c in strong] or ["- nothing site backed or approved names this line"])
        if weak:
            out += ["", "## Claims that still need proof (do not use in ads yet)", ""] + [f"- {c['text']} [{c['tier']}]" for c in weak]
        out += ["", "## Price and packs", ""]
        if ladder:
            v = ladder["value"]
            out.append(f"- Listed from ${v.get('min_usd'):,.0f} to ${v.get('max_usd'):,.0f} in a {v.get('sample_size')} product sample [{ladder['tier']}]")
        elif gift:
            d = gift["value"].get("denominations_usd") or []
            out.append(f"- Denominations ${d[0]} to ${d[-1]}" if d else "- denominations unavailable")
        else:
            out.append("- price ladder unavailable for this line")
        if packs:
            out.append(f"- Packs: {', '.join(packs['value'])} [{packs['tier']}]")
        if mats:
            out += ["", "## Materials", ""] + [f"- {m}" for m in mats["value"]]
        out += ["", "## What buyers say", ""]
        if reviews:
            out.append(f"- {total_reviews:,} reviews across {len(reviews)} products, average {avg:.2f}")
            for r in reviews:
                out.append(f"- {r['value'].get('yotpo_product')}: {int(r['value'].get('yotpo_review_total') or 0):,} reviews, {float(r['value'].get('yotpo_average') or 0):.2f}. {r.get('text', '').split('. ', 1)[1] if '. ' in (r.get('text') or '') else ''}".rstrip())
        else:
            out.append("- no review summary on file for this line")
        out += ["", "## Objections that name it", ""] + ([f"- {o['text']}" for o in objs[:8]] or ["- none on file"])
        out += ["", "## Never say about it", ""] + ([f"- {x.get('phrase') or x.get('text')}" + (f": {x['reason']}" if x.get("reason") else "") for x in reds] or ["- no red line names this line; the brand-wide red lines still apply"])
        text = "\n".join(out) + "\n"
        sheets.append({"line": line, "title": line.title(), "text": text, "tokens": tokens(text) if tokens else None,
                       "counts": {"claims_strong": len(strong), "claims_weak": len(weak), "reviews": total_reviews, "review_products": len(reviews), "objections": len(objs), "redlines": len(reds)},
                       "price": (ladder["value"] if ladder else None), "average": round(avg, 2) if avg else None,
                       "needs_proof": [{"id": c["id"], "text": c["text"][:120], "tier": c["tier"]} for c in weak][:10],
                       "records": [r["id"] for r in ([ladder] if ladder else []) + ([packs] if packs else []) + ([mats] if mats else []) + reviews + line_claims + objs]})
    sheets.sort(key=lambda s: (-(s["counts"]["claims_strong"] + s["counts"]["review_products"]), s["line"]))
    all_text = "\n\n".join(s["text"] for s in sheets)
    return {"sheets": sheets, "lines": [s["line"] for s in sheets], "text": all_text, "tokens": tokens(all_text) if tokens else None, "version": brain.version(),
            "counts": {"lines": len(sheets), "needs_proof": sum(s["counts"]["claims_weak"] for s in sheets), "thin": sum(1 for s in sheets if s["counts"]["claims_strong"] == 0)},
            "note": "One sheet per product line from the records: what the site says by tier, price and packs, materials, what buyers say, the objections and red lines that name it. A claim under the proof line is not for ads yet."}
