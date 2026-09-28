"""How we write: the voice sheet every writing agent loads, and the approved snippets it pastes word for word.

Voice sheet (`sheet`): the contract's voice fields (adjectives, writes like, do list, do-not list, tone by context,
reading level, words used, words avoided) as founder or site-backed records, unavailable when missing; liked and
disliked examples the founder pasted (`voice.liked_example_<n>`, `voice.disliked_example_<n>`); the site's own
lines the crawl quoted as evidence; and a copy-ready sheet in plain text built from what is on file. The scanner
(claims.py) reads `words_avoided` from here.

Snippets (`snippets`): fixed lines agents never rewrite, built in code from the records they depend on (free
shipping, standard shipping, returns, guarantee, giving, first order code). The founder locks the exact wording
as `voice.snippet_<key>` (approved). A locked snippet whose numbers no longer match its records is stale and
ends in a re-approve action; that is the fact-to-asset trace in miniature.
"""
from __future__ import annotations

import re

VOICE_FIELDS = [
    ("adjectives", "Personality in 3 to 5 words", "warm, plain, funny, direct"),
    ("writes_like", "Writes like", "a friend who knows socks, not a brand"),
    ("do_list", "Do", "short lines; digits; name the benefit before the feature"),
    ("do_not_list", "Do not", "no hype, no exclamation marks, no jargon"),
    ("tone_by_context", "Tone by context", "ads: playful; CX: calm and plain; policies: friendly but exact"),
    ("reading_level", "Reading level", "below grade 8"),
    ("words_used", "Words we use", "comfort, feel, give, pair"),
    ("words_avoided", "Words we avoid", "premium, elevate, leverage, unlock"),
]
EXAMPLES_NEEDED = 3
SNIPPET_KEYS = ["free_shipping", "standard_shipping", "returns", "guarantee", "giving", "first_order"]


def _rec(brain, section, field):
    rows = [r for r in brain.records(section) if r.get("field") == field]
    rows.sort(key=lambda r: ({"approved": 0, "site_backed": 1}.get(r["tier"], 2), r["date"] == "undated", ""))
    return rows[0] if rows else None


def _text(r) -> str | None:
    if not r:
        return None
    v = r.get("value")
    if isinstance(v, list):
        return ", ".join(str(x) for x in v)
    if isinstance(v, str) and v.strip():
        return v.strip()
    return r.get("text")


def words_avoided(brain) -> list[str]:
    r = _rec(brain, "voice", "words_avoided")
    t = _text(r) or ""
    return [w.strip().lower() for w in re.split(r"[,;\n]+", t) if w.strip()]


def examples(brain) -> dict:
    out = {"liked": [], "disliked": []}
    for r in brain.records("voice"):
        f = r.get("field") or ""
        for kind in ("liked", "disliked"):
            if f.startswith(f"{kind}_example"):
                v = r.get("value") if isinstance(r.get("value"), dict) else {}
                out[kind].append({"id": r["id"], "text": v.get("text") or r.get("text") or "", "why": v.get("why"), "date": None if r["date"] == "undated" else r["date"], "source": (r.get("source") or {}).get("type")})
    for k in out:
        out[k].sort(key=lambda x: x["id"])
    return out


def site_lines(brain) -> list[dict]:
    """Lines the crawl quoted from the brand's own pages: the brand's voice as it stands."""
    out = []
    for r in brain.records("voice"):
        if r["tier"] != "site_backed" or (r.get("field") or "").startswith(("liked", "disliked", "snippet_")):
            continue
        for e in (r.get("evidence") or [])[:1]:
            if e.get("quote"):
                out.append({"id": r["id"], "field": r.get("field"), "quote": e["quote"][:200], "ref": e.get("ref"), "note": r.get("text")})
    return out


def sheet(brain) -> dict:
    fields = []
    for key, label, example in VOICE_FIELDS:
        r = _rec(brain, "voice", key)
        fields.append({"key": key, "label": label, "text": _text(r), "tier": r["tier"] if r else None, "record": r["id"] if r else None,
                       "date": (None if not r or r["date"] == "undated" else r["date"]), "example": example})
    ex = examples(brain)
    lines = site_lines(brain)
    filled = sum(1 for f in fields if f["text"])
    text = ["Voice sheet: " + brain.brand, ""]
    for f in fields:
        text.append(f"{f['label']}: " + (f["text"] if f["text"] else "unavailable (founder to add)"))
    if lines:
        text.append("")
        text.append("Lines from our own pages:")
        text += [f"- {l['quote']}" for l in lines[:6]]
    if ex["liked"]:
        text.append("")
        text.append("Copy we like:")
        text += [f"- {e['text']}" + (f" (why: {e['why']})" if e.get("why") else "") for e in ex["liked"]]
    if ex["disliked"]:
        text.append("")
        text.append("Copy we do not like:")
        text += [f"- {e['text']}" + (f" (why: {e['why']})" if e.get("why") else "") for e in ex["disliked"]]
    text.append("")
    text.append("Rules for every agent: short sentences, digits, no em dashes, claims only from the approved list, snippets pasted word for word.")
    return {"fields": fields, "filled": filled, "of": len(fields), "examples": ex, "examples_needed": EXAMPLES_NEEDED, "site_lines": lines,
            "sheet_text": "\n".join(text), "readers": ["copy", "creative", "email", "CX", "organic"],
            "ready": filled >= 4 and len(ex["liked"]) >= EXAMPLES_NEEDED,
            "note": "Agents load this sheet before writing. Fields come from your profile edits or the crawl; examples are yours. Words avoided feed the draft scanner."}


def _money(v) -> str:
    return f"${v:,.0f}" if isinstance(v, (int, float)) and float(v).is_integer() else (f"${v:,.2f}" if isinstance(v, (int, float)) else str(v))


def generated(brain) -> list[dict]:
    """Snippet text built from the records it depends on. The numbers are the records', never typed here."""
    out = []
    fs = _rec(brain, "offers", "free_shipping_threshold_usd")
    if fs and isinstance(fs.get("value"), (int, float)):
        out.append({"key": "free_shipping", "label": "Free shipping line", "text": f"Free shipping on orders over {_money(fs['value'])}.", "records": [fs["id"]], "numbers": [float(fs["value"])]})
    sc = _rec(brain, "offers", "standard_shipping_cost")
    if sc and isinstance(sc.get("value"), dict) and isinstance(sc["value"].get("cost_usd"), (int, float)):
        cond = sc["value"].get("condition") or ""
        out.append({"key": "standard_shipping", "label": "Standard shipping line", "text": f"Standard shipping is {_money(sc['value']['cost_usd'])}" + (f" on {cond}" if cond else "") + ".", "records": [sc["id"]], "numbers": [float(sc["value"]["cost_usd"])] + ([float(fs["value"])] if fs and isinstance(fs.get("value"), (int, float)) and str(int(fs["value"])) in cond else [])})
    rw = _rec(brain, "policies", "returns_window_days")
    rm = _rec(brain, "policies", "refund_method")
    if rw and isinstance(rw.get("value"), (int, float)):
        out.append({"key": "returns", "label": "Returns line", "text": f"Returns within {int(rw['value'])} days" + (f", refunded to the {_text(rm)}" if rm and _text(rm) else "") + ".", "records": [rw["id"]] + ([rm["id"]] if rm else []), "numbers": [float(rw["value"])]})
    g = _rec(brain, "policies", "happiness_guarantee") or _rec(brain, "offers", "guarantee")
    if g and _text(g):
        out.append({"key": "guarantee", "label": "Guarantee line", "text": _text(g)[0].upper() + _text(g)[1:].rstrip(".") + ".", "records": [g["id"]], "numbers": [float(x) for x in re.findall(r"\d+", _text(g))[:2]]})
    tag = _rec(brain, "voice", "donation_tagline")
    gm = _rec(brain, "identity", "giving_model")
    if tag and _text(tag):
        out.append({"key": "giving", "label": "Giving line", "text": _text(tag), "records": [tag["id"]] + ([gm["id"]] if gm else []), "numbers": []})
    elif gm and _text(gm):
        out.append({"key": "giving", "label": "Giving line", "text": _text(gm)[0].upper() + _text(gm)[1:].rstrip(".") + ".", "records": [gm["id"]], "numbers": []})
    fo = _rec(brain, "offers", "first_order_code")
    code = _rec(brain, "offers", "first_order_code_confirmed")
    if fo and isinstance(fo.get("value"), dict) and isinstance(fo["value"].get("discount_pct"), (int, float)):
        c = _text(code) or fo["value"].get("code") or ""
        out.append({"key": "first_order", "label": "First order line", "text": f"{int(fo['value']['discount_pct'])} percent off your first order" + (f" with code {c}" if c else "") + ".", "records": [fo["id"]] + ([code["id"]] if code else []), "numbers": [float(fo["value"]["discount_pct"])]})
    return out


def _nums(text: str) -> list[float]:
    return [float(x.replace(",", "")) for x in re.findall(r"\d[\d,]*(?:\.\d+)?", text or "")]


def snippets(brain) -> dict:
    gen = {g["key"]: g for g in generated(brain)}
    locked = {}
    for r in brain.records("voice"):
        f = r.get("field") or ""
        if f.startswith("snippet_") and r["tier"] == "approved":
            locked[f[len("snippet_"):]] = r
    rows = []
    for key in SNIPPET_KEYS:
        g, lk = gen.get(key), locked.get(key)
        if not g and not lk:
            rows.append({"key": key, "label": key.replace("_", " ").capitalize() + " line", "status": "unavailable", "reason": "no record in the brain to build it from",
                         "generated": None, "locked": None, "records": [], "action": None})
            continue
        lt = _text(lk) if lk else None
        stale = False
        if lt and g:
            want = set(g["numbers"])
            have = set(_nums(lt))
            stale = bool(want) and not want <= have
        status = "stale" if stale else ("locked" if lt else "proposed")
        rows.append({"key": key, "label": (g or {}).get("label") or key.replace("_", " ").capitalize() + " line", "status": status,
                     "generated": (g or {}).get("text"), "locked": lt, "locked_record": lk["id"] if lk else None, "locked_date": (None if not lk or lk["date"] == "undated" else lk["date"]),
                     "records": (g or {}).get("records") or [], "use": (g or {}).get("text") if status != "locked" else lt,
                     "reason": ("the locked wording carries a number the brain no longer holds" if stale else ("your exact wording, pasted word for word" if lt else "built from the records; lock it to fix the wording")),
                     "action": ({"title": f"Re-approve the {(g or {}).get('label', key).lower()}", "owner": "person", "capability": "BRN-C08",
                                 "steps": [{"n": 1, "who": "agent", "text": f"Show the locked line next to the line built from the current records: {(g or {}).get('text')}"},
                                           {"n": 2, "who": "person", "text": "Lock the new wording, or keep the old one on purpose."},
                                           {"n": 3, "who": "agent", "text": "Find live ads, emails and pages carrying the old line and propose the edits."}]} if stale else None)})
    counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("locked", "proposed", "stale", "unavailable")}
    all_text = "\n".join(f"{r['label']}: {r['use']}" for r in rows if r.get("use"))
    return {"snippets": rows, "counts": counts, "all_text": all_text,
            "note": "Agents paste these word for word and never rewrite them. Built from the records; lock a line to fix its wording. A locked line whose number the brain no longer holds is stale."}
