"""Hook and offer mix: the first lines and offers each tracked page leads with, against ours, and the
answer for each gap.

First lines: the kind of the first line of each ad (question, number, first person, quote, offer,
problem, plain statement), counted per page by the Ad Library pull. Offers: the offers seen in a
page's ads, sorted into types by snapshot.OFFERS rules. For us the brain also holds offers we have
but may not advertise (free shipping threshold, guarantee, pack ladder, gifting), so a gap can be
"we hold it and never say it".

Gap rules (constants below):
  first line: a kind at FL_SHARE (5 percent) or more of the ads on FL_PAGES (3) or more tracked pages,
              and under FL_OURS (2 percent) of ours. Answer: a hook bank brief in that kind (CREA-C04).
  offer:      an offer type seen on OFFER_PAGES (3) or more tracked pages, held in our brain, and in
              none of our ads. Answer: an offer test (LIFE-C47).
  discount:   OUR_PROMO (50 percent) or more of our ads push a code while NO_OFFER_PAGES (2) or more
              direct competitors show no offer at all. Answer: a no-code ad test (LIFE-C38).
Signals only: kinds and types, never their lines.
"""
from __future__ import annotations

import re

KINDS = ["statement", "question", "first_person", "number", "offer", "problem", "quote"]
FL_SHARE, FL_PAGES, FL_OURS = 0.05, 3, 0.02
OFFER_PAGES, OUR_PROMO, NO_OFFER_PAGES = 3, 0.5, 2
HELD = [("free_shipping", "offers.free_shipping_threshold_usd", "free shipping over ${v}"),
        ("guarantee", "offers.guarantee", "{v}"),
        ("bundle", "offers.bundles_pack_ladder", "packs: {v}"),
        ("gift_with_purchase", "offers.gifting", "{v}")]
KIND_EXAMPLE = {"question": "a question the shopper already asks", "number": "a number first: a count, a time, a price per pair",
                "first_person": "a customer voice in the first person", "quote": "a short quote in marks",
                "problem": "the problem first, then the relief", "offer": "the offer first"}


def offer_types(texts: list[str], rules) -> list[str]:
    out = []
    for t in texts:
        tl = str(t).lower()
        for key, _label, rx in rules:
            if rx.search(tl) and key not in out:
                out.append(key)
        if re.search(r"\b\d{1,2}\s?%", tl) and "percent_off" not in out:
            out.append("percent_off")
    return out


def build(pages: list[dict], brain, snap_mod) -> dict:
    labels = snap_mod.FIRST_LINE_LABEL
    olabels = {k: lbl for k, lbl, _ in snap_mod.OFFERS}
    us = next(p for p in pages if p["role"] == "self")
    comps = [p for p in pages if p["role"] != "self" and p["source"] != "none"]
    rows = []
    for p in comps + [us]:
        fl = {k: v for k, v in (p.get("first_lines") or {}).items() if isinstance(v, int)}
        n = sum(fl.values())
        shares = {k: round(fl.get(k, 0) / n, 3) for k in KINDS} if n else {k: None for k in KINDS}
        rows.append({"name": p["name"], "role": p["role"], "frame": p["frame"], "n": n or None, "shares": shares,
                     "offers": offer_types(p.get("offers_seen") or [], snap_mod.OFFERS),
                     "offers_seen": p.get("offers_seen") or [], "offer_share": p.get("offer_share")})
    ours = rows[-1]
    held = {}
    for key, ref, tmpl in HELD:
        v = (brain.get(f"{brain.brand}.{ref}") or {}).get("value")
        if v not in (None, "", []):
            held[key] = {"text": tmpl.format(v=", ".join(v) if isinstance(v, list) else v), "ref": f"{brain.brand}.{ref}"}
    gaps = []
    for k in KINDS:
        if k == "statement":
            continue
        users = [r for r in rows[:-1] if (r["shares"].get(k) or 0) >= FL_SHARE]
        mine = ours["shares"].get(k)
        if len(users) >= FL_PAGES and (mine or 0) < FL_OURS:
            gaps.append({"kind": "first_line", "key": k, "label": labels.get(k, k), "pages": [r["name"] for r in users],
                         "their_median": sorted(r["shares"][k] for r in users)[len(users) // 2], "ours": mine,
                         "answer": "copy", "capability": "CREA-C04", "owner": "agent",
                         "draft": hook_brief(k, labels.get(k, k), users, mine, brain)})
    for key, label in olabels.items():
        users = [r for r in rows[:-1] if key in r["offers"]]
        if len(users) >= OFFER_PAGES and key in held and key not in ours["offers"]:
            gaps.append({"kind": "offer", "key": key, "label": label, "pages": [r["name"] for r in users],
                         "ours": None, "held": held[key], "answer": "offer", "capability": "LIFE-C47", "owner": "agent_drafts",
                         "draft": offer_brief(label, held[key]["text"], users, ours)})
    none_direct = [r for r in rows[:-1] if r["frame"] == "direct" and not r["offers"]]
    promo = ours.get("offer_share")
    discount = None
    if promo is not None and promo >= OUR_PROMO and len(none_direct) >= NO_OFFER_PAGES:
        discount = {"kind": "discount", "key": "discount_heavy", "label": "Discount on most ads", "pages": [r["name"] for r in none_direct],
                    "ours": promo, "answer": "offer", "capability": "LIFE-C38", "owner": "agent_drafts",
                    "draft": discount_brief(promo, none_direct, us)}
        gaps.append(discount)
    return {"rows": rows, "kinds": [{"key": k, "label": labels.get(k, k)} for k in KINDS], "held": held,
            "offer_labels": olabels, "gaps": gaps,
            "rules": f"First line gap: a kind at {round(FL_SHARE * 100)} percent or more of ads on {FL_PAGES} or more pages, "
                     f"under {round(FL_OURS * 100)} percent of ours. Offer gap: seen on {OFFER_PAGES} or more pages, held in our "
                     f"brain, in none of our ads. Discount: {round(OUR_PROMO * 100)} percent or more of our ads push a code while "
                     f"{NO_OFFER_PAGES} or more direct competitors show no offer."}


def _praise(brain, n: int = 3) -> list[str]:
    """Short praise phrases from the language bank, as raw words for first lines. Never quoted as a testimonial."""
    out = []
    for r in brain.records("language_bank"):
        v = r.get("value") if isinstance(r.get("value"), dict) else {}
        ph = str(v.get("phrase") or "").strip()
        if v.get("theme") == "praise" and 3 <= len(ph.split()) <= 8 and ph not in out:
            out.append(ph)
        if len(out) >= n:
            break
    return out


def hook_brief(key: str, label: str, users: list[dict], mine, brain) -> str:
    words = _praise(brain)
    lines = [f"Hook bank brief: 6 first lines in the {label.lower()} kind.",
             f"Why: {len(users)} tracked pages open a median {round(sorted(u['shares'][key] for u in users)[len(users) // 2] * 100)} "
             f"percent of their ads this way. Ours: {round((mine or 0) * 100)} percent.",
             f"Shape: {KIND_EXAMPLE.get(key, label)}. Under 12 words. Our product and proof, our voice.",
             ("Customer words to start from (language bank, not for quoting): " + "; ".join(words) + ".") if words else
             "Customer words: none in the language bank yet.",
             "Grade each line on the hook bank rubric. Test the best 2 against the current first line.",
             "Never copy their lines. Kinds only."]
    return "\n".join(lines)


def offer_brief(label: str, held: str, users: list[dict], ours: dict) -> str:
    return "\n".join([f"Offer test: say our {label.lower()} in ads.",
                      f"What we hold: {held}. Our ads never say it.",
                      f"Why: {len(users)} tracked pages show it: " + ", ".join(u["name"] for u in users) + ".",
                      "Test: 3 ads with the line in the first frame against 3 with the current offer. 50 50 split, 14 days.",
                      "Read: click to order rate and net revenue per order. Keep the line if both hold."])


def discount_brief(promo: float, none_direct: list[dict], us: dict) -> str:
    return "\n".join([f"Offer test: fewer ads with a code. {round(promo * 100)} percent of our ads push one now.",
                      f"{len(none_direct)} direct competitors show no offer at all: " + ", ".join(r["name"] for r in none_direct) + ".",
                      "Test: 6 ads that lead with proof and no code against 6 current code ads. Same audience, 14 days.",
                      "Read: net revenue per order and new customer orders. Code ads stay live as control.",
                      "The founder approves any change to the code policy."])
