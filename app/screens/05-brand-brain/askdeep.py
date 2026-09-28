"""Ask the brain, deeper: typed answers for the questions a founder asks most, computed from the records, before the
keyword search runs.

Five intents, matched by words and numbers in the question:
- a number check ("is free shipping over $50?", "returns 60 days?"): the stated number against the record, yes or no
  with the record's value and id;
- a count ("how many durability complaints?", "one-star on fit?"): the ladder theme's counts, or the language bank's
  theme totals;
- a comparison ("who wins on durability?", "us vs darn tough"): the names Reddit recommends instead on that doubt and
  the counter-proposal on the master list;
- the next move ("what should we do first?", "biggest bottleneck?"): the diagnosis's first bottleneck and the top
  action on the plan;
- a peak ("when is black friday?", "are we ready for cyber monday?"): the date, days to go and the checks waiting.
Anything else falls through to the keyword search. Every answer names its records; nothing is inferred by a model.
"""
from __future__ import annotations

import re

NUM = re.compile(r"\$?\s*(\d+(?:\.\d+)?)\s*(percent|%|days?|dollars?|usd)?", re.I)
FACT_TOPICS = [("free shipping", "offers", "free_shipping_threshold_usd", "the free shipping threshold", "$"), ("returns", "policies", "returns_window_days", "the returns window", "days"), ("return window", "policies", "returns_window_days", "the returns window", "days"),
               ("shipping cost", "offers", "standard_shipping_cost", "standard shipping", "$"), ("standard shipping", "offers", "standard_shipping_cost", "standard shipping", "$"), ("first order", "offers", "first_order_code", "the first order code", "percent")]
COUNT_WORDS = re.compile(r"\b(how many|count|number of|one[- ]star|five[- ]star|complaints?|quotes?)\b", re.I)
COMPARE = re.compile(r"\b(who wins|wins on|beats? us|better than us|vs\.?|versus|compare|against)\b", re.I)
NEXT = re.compile(r"\b(what (?:should|do) we do (?:first|next)|biggest bottleneck|bottleneck|first move|top action|what matters most|where to start)\b", re.I)
PEAK = re.compile(r"\b(black friday|cyber monday|giving tuesday|christmas|holiday|bfcm|peak|prime day|deal days)\b", re.I)
THEMES = ["durability", "price_and_value", "fit_and_sizing", "order_and_delivery", "comfort_and_feel", "marketplace_trust", "mission_trust"]
THEME_WORDS = {"durability": ["durab", "hole", "pill", "last", "wear out"], "price_and_value": ["price", "expensive", "worth", "value", "cost"], "fit_and_sizing": ["fit", "size", "sizing", "slip"], "order_and_delivery": ["deliver", "shipping", "order", "arrive"], "comfort_and_feel": ["comfort", "soft", "feel", "cushion"], "marketplace_trust": ["amazon", "marketplace", "seller", "counterfeit"], "mission_trust": ["mission", "giving", "donat"]}


def _rec(brain, section, field):
    rows = [r for r in brain.records(section) if r.get("field") == field]
    rows.sort(key=lambda r: ({"approved": 0, "site_backed": 1}.get(r["tier"], 2), r["id"]))
    return rows[0] if rows else None


def _num(v):
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, dict):
        for k in ("cost_usd", "discount_pct", "value", "amount"):
            if isinstance(v.get(k), (int, float)):
                return float(v[k])
    if isinstance(v, str):
        m = re.search(r"\d+(?:\.\d+)?", v)
        return float(m.group(0)) if m else None
    return None


def _theme(q: str) -> str | None:
    ql = q.lower()
    for t, ws in THEME_WORDS.items():
        if any(w in ql for w in ws):
            return t
    return None


def answer(brain, q: str, mods: dict, actions: list[dict] | None = None) -> dict | None:
    ql = (q or "").lower().strip()
    if not ql:
        return None
    # a number check
    for topic, sec, field, label, unit in FACT_TOPICS:
        if topic in ql:
            r = _rec(brain, sec, field)
            m = NUM.search(ql.replace(topic, ""))
            if r is None:
                return {"intent": "number", "answer": f"Nothing on file for {label}.", "verdict": "unavailable", "records": []}
            have = _num(r.get("value"))
            shown = f"${have:,.0f}" if unit == "$" and have is not None and have.is_integer() else (f"{have:g} {unit}" if have is not None and unit != "$" else (f"${have:g}" if have is not None else str(r.get("value"))))
            if m and have is not None:
                asked = float(m.group(1))
                same = abs(asked - have) <= 0.005 * max(abs(have), 1)
                return {"intent": "number", "answer": (f"Yes. {label.capitalize()} is {shown}." if same else f"No. {label.capitalize()} is {shown}, not {m.group(1)}.") + f" Source: {r['id']} ({r['tier'].replace('_', ' ')}).", "verdict": "yes" if same else "no", "records": [r["id"]], "value": have}
            return {"intent": "number", "answer": f"{label.capitalize()} is {shown}. Source: {r['id']} ({r['tier'].replace('_', ' ')}).", "verdict": "fact", "records": [r["id"]], "value": have}
    # a count
    if COUNT_WORDS.search(ql):
        theme = _theme(ql)
        lad = next((r for r in brain.records("objection_ladders") if isinstance(r.get("value"), dict) and r["value"].get("theme") == theme), None) if theme else None
        if lad:
            rungs = lad["value"].get("rungs") or []
            one = sum((x.get("counts") or {}).get("one_star") or 0 for x in rungs)
            five = sum((x.get("counts") or {}).get("five_star") or 0 for x in rungs)
            return {"intent": "count", "answer": f"{theme.replace('_', ' ').capitalize()}: {one} one-star and {five} five-star quotes across {len(rungs)} rungs" + ("; the deal-breaker rung is '" + rungs[-1].get("doubt", "") + "'" if rungs else "") + f". Source: {lad['id']}.", "verdict": "fact", "records": [lad["id"]], "numbers": {"one_star": one, "five_star": five, "rungs": len(rungs)}}
        counts = {}
        for r in brain.records("language_bank"):
            v = r.get("value") if isinstance(r.get("value"), dict) else {}
            counts[v.get("theme")] = counts.get(v.get("theme"), 0) + 1
        if counts:
            return {"intent": "count", "answer": "Language bank quotes by theme: " + ", ".join(f"{k} {n}" for k, n in sorted(counts.items(), key=lambda kv: -kv[1]) if k) + ". Name a doubt (durability, price, fit, delivery, comfort) for its ladder counts.", "verdict": "fact", "records": [], "numbers": counts}
        return {"intent": "count", "answer": "No ladder or language bank to count from yet.", "verdict": "unavailable", "records": []}
    # a comparison
    if COMPARE.search(ql):
        try:
            sg = mods["market"].signals(brain)
        except Exception:  # noqa: BLE001
            sg = {}
        theme = _theme(ql)
        recs = sg.get("recommended") or []
        named = [r for r in recs if r["competitor"].lower() in ql or r["slug"].replace("_", " ") in ql]
        on_theme = [r for r in recs if theme and r.get("doubt_angle") and r["doubt_angle"] in theme]
        pick = named or on_theme or recs[:3]
        if pick:
            parts = [f"{r['competitor']} on {r.get('doubt_label', 'a doubt').lower()}: {r['threads']} Reddit threads, {r['upvotes']} upvotes; {r.get('proof_status') or 'proof status unknown'}" for r in pick[:3]]
            act = next((a for a in actions or [] if (a.get("entity") or {}).get("id") in {f"recommended_{r['slug']}" for r in pick}), None)
            return {"intent": "compare", "answer": "Where they win: " + " | ".join(parts) + "." + (f" On the plan: {act['title']}." if act else ""), "verdict": "fact", "records": [r.get("record_id") for r in pick if r.get("record_id")], "action": {"id": act["id"], "title": act["title"]} if act else None}
        return {"intent": "compare", "answer": "No Reddit recommendation or competitor signal on that doubt in the brain.", "verdict": "unavailable", "records": []}
    # the next move
    if NEXT.search(ql):
        d = mods["bottlenecks"].diagnosis(brain)
        top = next((a for a in actions or [] if a.get("status") != "unavailable"), None)
        b = d["bottlenecks"][0] if d["bottlenecks"] else None
        if not b and not top:
            return {"intent": "next", "answer": "No diagnosis and no open action yet.", "verdict": "unavailable", "records": []}
        return {"intent": "next", "answer": (f"The first bottleneck is {b['theme'].replace('_', ' ')}: {(b.get('text') or '')[:160]}" if b else "No diagnosis on file.") + (f" Top action on the plan: {top['title']} ({top['owner'].replace('_', ' ')}, {top['rubric']['total']}/100)." if top else ""), "verdict": "fact", "records": [b["record"]] if b else [], "action": {"id": top["id"], "title": top["title"]} if top else None}
    # a peak
    if PEAK.search(ql):
        try:
            pk = mods["peaks"].readiness(brain, mods["market"].angles_of, mods.get("legal"), mods.get("assumptions"))
        except Exception:  # noqa: BLE001
            pk = {"peaks": []}
        want = next((p for p in pk["peaks"] if any(w in p["label"].lower() for w in ql.split() if len(w) > 3)), None) or (pk["peaks"][0] if pk["peaks"] else None)
        if not want:
            return {"intent": "peak", "answer": "No peak inside the next 90 days.", "verdict": "unavailable", "records": []}
        gaps = [c["label"].lower() for c in want["checks"] if c["status"] == "gap"]
        return {"intent": "peak", "answer": f"{want['label']}: " + (f"{want['date']}, {want['days_to']} days away" if want.get("date") else (want.get("window") or "date unavailable")) + f". Readiness {want['readiness_pct'] if want['readiness_pct'] is not None else 'n/a'} percent; " + (("to decide: " + ", ".join(gaps) + ".") if gaps else "nothing to decide."), "verdict": "fact", "records": [], "peak": want["key"]}
    return None
