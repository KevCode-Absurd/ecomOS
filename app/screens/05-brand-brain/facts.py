"""Store facts for AI shopping agents and answer engines: question and answer pairs built from the brain, approved once.

Each pair is built in code from the records it depends on (returns, shipping options, free shipping, guarantee, giving,
first order code, pack sizes, materials, gift cards, B Corp) so the numbers are the brain's. The founder approves the
wording as `content.faq_<key>` (approved). An approved answer whose numbers the brain no longer holds is stale and is
not exported. A question the brain cannot answer (where do you ship) reads unavailable until the founder answers it.
Export: a FAQPage JSON-LD block of approved pairs for the site, and the same pairs as plain text for the agentic
sitemap or a knowledge base. Capability LOOP-C38 audits what AI shopping agents say against these and the claims tiers.
"""
from __future__ import annotations

import json
import re

KEYS = ["returns", "shipping", "free_shipping", "guarantee", "giving", "first_order", "pack_sizes", "materials", "gift_cards", "bcorp", "ship_where", "sizing"]
QUESTIONS = {
    "returns": "How do returns and refunds work?", "shipping": "How much is shipping and how long does it take?", "free_shipping": "Do you offer free shipping?",
    "guarantee": "What if I am not happy with my order?", "giving": "What does my purchase do for someone else?", "first_order": "Is there a discount on a first order?",
    "pack_sizes": "What pack sizes can I buy?", "materials": "What are the products made of?", "gift_cards": "Do you sell gift cards?", "bcorp": "Are you a certified B Corp?",
    "ship_where": "Where do you ship?", "sizing": "How do I pick my size?",
}


def _rec(brain, section, field):
    rows = [r for r in brain.records(section) if r.get("field") == field]
    rows.sort(key=lambda r: ({"approved": 0, "site_backed": 1}.get(r["tier"], 2), r["id"]))
    return rows[0] if rows else None


def _money(v) -> str:
    return f"${v:,.0f}" if isinstance(v, (int, float)) and float(v).is_integer() else (f"${v:,.2f}" if isinstance(v, (int, float)) else str(v))


def generated(brain) -> dict[str, dict]:
    g: dict[str, dict] = {}
    rw, rm, ex = _rec(brain, "policies", "returns_window_days"), _rec(brain, "policies", "refund_method"), _rec(brain, "policies", "exchanges")
    if rw and isinstance(rw.get("value"), (int, float)):
        ans = f"Returns are accepted within {int(rw['value'])} days" + (f", refunded to the {rm['value']}" if rm and isinstance(rm.get("value"), str) else "") + "." + (f" {ex['value'][0].upper() + ex['value'][1:]}." if ex and isinstance(ex.get("value"), str) else "")
        g["returns"] = {"answer": ans, "records": [x["id"] for x in (rw, rm, ex) if x]}
    so = _rec(brain, "policies", "shipping_options")
    if so and isinstance(so.get("value"), list) and so["value"]:
        parts = []
        for o in so["value"]:
            if not isinstance(o, dict):
                continue
            cost = "free" if o.get("cost_usd") == 0 else _money(o.get("cost_usd"))
            parts.append(f"{o.get('name')}: {cost}" + (f" on orders over {_money(o['threshold_usd'])}" if o.get("threshold_usd") else "") + (f", {o['business_days']} business days" if o.get("business_days") else ""))
        g["shipping"] = {"answer": "; ".join(parts) + ".", "records": [so["id"]]}
    fs = _rec(brain, "offers", "free_shipping_threshold_usd")
    if fs and isinstance(fs.get("value"), (int, float)):
        g["free_shipping"] = {"answer": f"Yes. Standard shipping is free on orders over {_money(fs['value'])}.", "records": [fs["id"]]}
    hg = _rec(brain, "policies", "happiness_guarantee") or _rec(brain, "offers", "guarantee")
    if hg and isinstance(hg.get("value"), str):
        g["guarantee"] = {"answer": hg["value"][0].upper() + hg["value"][1:].rstrip(".") + ".", "records": [hg["id"]]}
    gm, dm = _rec(brain, "identity", "giving_model"), _rec(brain, "identity", "donation_milestone")
    if gm and isinstance(gm.get("value"), str):
        g["giving"] = {"answer": gm["value"][0].upper() + gm["value"][1:].rstrip(".") + "." + (f" {dm['value'][0].upper() + dm['value'][1:].rstrip('.')}." if dm and isinstance(dm.get("value"), str) else ""), "records": [x["id"] for x in (gm, dm) if x]}
    fo, code = _rec(brain, "offers", "first_order_code"), _rec(brain, "offers", "first_order_code_confirmed")
    if fo and isinstance(fo.get("value"), dict) and isinstance(fo["value"].get("discount_pct"), (int, float)):
        c = (code.get("value") if code and isinstance(code.get("value"), str) else None) or fo["value"].get("code")
        g["first_order"] = {"answer": f"Yes. {int(fo['value']['discount_pct'])} percent off a first order" + (f" with code {c}" if c else "") + ".", "records": [x["id"] for x in (fo, code) if x]}
    ps = _rec(brain, "products", "pack_sizes")
    if ps and isinstance(ps.get("value"), list):
        g["pack_sizes"] = {"answer": "Packs come as " + ", ".join(str(x) for x in ps["value"]) + ".", "records": [ps["id"]]}
    ma = _rec(brain, "products", "materials")
    if ma and isinstance(ma.get("value"), list):
        g["materials"] = {"answer": "Materials include " + ", ".join(str(x) for x in ma["value"]) + ".", "records": [ma["id"]]}
    gc = _rec(brain, "products", "gift_card")
    if gc and isinstance(gc.get("value"), dict) and gc["value"].get("denominations_usd"):
        d = gc["value"]["denominations_usd"]
        g["gift_cards"] = {"answer": f"Yes. {gc['value'].get('name') or 'Digital gift cards'} from {_money(min(d))} to {_money(max(d))}.", "records": [gc["id"]]}
    bc = _rec(brain, "identity", "b_corp_certified") or _rec(brain, "identity", "certification_bcorp")
    if bc and (bc.get("value") is True or (isinstance(bc.get("value"), dict) and bc["value"].get("certified"))):
        since = bc["value"].get("first_certified") if isinstance(bc.get("value"), dict) else None
        g["bcorp"] = {"answer": "Yes, a certified B Corp" + (f" since {since}" if since else "") + ".", "records": [bc["id"]]}
    sg = _rec(brain, "site_map", "facts_pages")
    if sg and isinstance(sg.get("value"), list):
        page = next((p.get("url") for p in sg["value"] if isinstance(p, dict) and "size" in (p.get("url") or "")), None)
        if page:
            g["sizing"] = {"answer": f"Use the size guide at {page}.", "records": [sg["id"]]}
    return g


def _nums(s: str) -> set[str]:
    return {x.replace(",", "") for x in re.findall(r"\d[\d,]*(?:\.\d+)?", s or "")}


def pairs(brain) -> dict:
    g = generated(brain)
    approved = {}
    for r in brain.records("content"):
        f = r.get("field") or ""
        if f.startswith("faq_") and r["tier"] == "approved" and isinstance(r.get("value"), dict):
            approved[f[4:]] = r
    rows = []
    for key in KEYS:
        gen, ap = g.get(key), approved.get(key)
        q = (ap["value"].get("question") if ap else None) or QUESTIONS[key]
        at = ap["value"].get("answer") if ap else None
        if not gen and not at:
            rows.append({"key": key, "question": q, "answer": None, "generated": None, "approved": None, "status": "unavailable", "records": [],
                         "reason": "no record answers it; type the answer and it becomes an approved fact", "export": False})
            continue
        stale = bool(gen and at) and not (_nums(gen["answer"]) <= _nums(at))
        status = "stale" if stale else ("approved" if at else "proposed")
        rows.append({"key": key, "question": q, "answer": at if status == "approved" else (gen["answer"] if gen else at), "generated": gen["answer"] if gen else None, "approved": at,
                     "approved_record": ap["id"] if ap else None, "status": status, "records": (gen or {}).get("records") or [],
                     "reason": ("the approved answer carries a number the brain no longer holds" if stale else ("your wording, exported" if at else "built from the records; approve to export")),
                     "export": status == "approved"})
    counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("approved", "proposed", "stale", "unavailable")}
    return {"pairs": rows, "counts": counts, "note": "Answers are built from the records, so the numbers are the brain's. Approve a wording to export it; a stale approval is not exported until you re-approve."}


def export(brain) -> dict:
    p = pairs(brain)
    ok = [r for r in p["pairs"] if r["export"]]
    jsonld = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": r["question"], "acceptedAnswer": {"@type": "Answer", "text": r["answer"]}} for r in ok]}
    text = "\n\n".join(f"Q: {r['question']}\nA: {r['answer']}" for r in ok)
    return {"count": len(ok), "jsonld": jsonld, "text": text, "skipped": [r["key"] for r in p["pairs"] if not r["export"]],
            "note": "Only approved, non-stale pairs export. Paste the JSON-LD into the FAQ page and the text into the agentic sitemap or knowledge base."}
