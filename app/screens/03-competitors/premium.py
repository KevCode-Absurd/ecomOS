"""Premium signals and discount depth against the category (room metrics premium_signal_score and
discount_depth_vs_category).

Premium signals per page, each a word rule over hook labels, positioning, push line, quoted ads and offers
(for us: the brand profile, proof points, identity and offers):
  guarantee, lifetime promise, origin or heritage, mission, tested or rated proof, no discount seen.
Score = signals present / signals checked. Discount depth = the deepest percent seen in a page's offers;
a page with ads read and no percent seen reads 0 (measured, from up to 150 ads), a page with nothing read
reads unavailable.

Rule COMP-R21 (the room's "discounting undercuts a premium position"): our premium score is at or above
the direct median while our discount depth is DEEPER (10 points) or more below theirs. Answer: an offer
policy that caps the code and swaps depth for a gift or a pack step (LIFE-C38, founder gate).
"""
from __future__ import annotations

import re
import statistics

DEEPER = 10
SIGNALS = [("guarantee", "Guarantee", ["guarantee"]), ("lifetime", "Lifetime promise", ["lifetime", "for life"]),
           ("origin", "Origin or heritage", ["made in", "vermont", "heritage", "since 19", "since 20"]),
           ("mission", "Mission", ["donat", "b corp", "giving", "give back"]),
           ("proof", "Tested or rated", ["lab tested", "doctor", "review", "rated", "tested", "testimonial"])]


def depth(offers: list[str]) -> int | None:
    nums = [int(x) for o in offers for x in re.findall(r"(\d{1,2})\s?%", str(o))]
    return max(nums) if nums else 0


def build(m: dict, brain, offer_types) -> dict:
    get = lambda k: (brain.get(f"{brain.brand}.{k}") or {}).get("value")  # noqa: E731
    rows = []
    for p in m["pages"]:
        if p["source"] == "none":
            continue
        if p["role"] == "self":
            texts = list(m["profile"]["_texts"]) + [str(x) for x in (get("positioning.proof_points") or [])] + [
                str(get("identity.giving_model") or ""), "b corp" if get("identity.b_corp_certified") else ""]
        else:
            texts = p["hook_labels"] + p["quotes"] + [p["positioning"] or "", p["push"] or ""]
        t = " ".join(texts).lower()
        offers = p.get("offers_seen") or []
        kinds = offer_types(offers)
        has = {k: any(w in t for w in words) for k, _, words in SIGNALS}
        has["no_discount"] = not ({"percent_off", "code"} & set(kinds))
        score = round(sum(has.values()) / len(has), 3)
        rows.append({"name": p["name"], "role": p["role"], "frame": p["frame"], "signals": has, "score": score,
                     "depth": depth(offers) if (p.get("sample_ads") or p["role"] == "self") else None, "offers": offers})
    direct = [r for r in rows if r["frame"] == "direct"]
    us = next((r for r in rows if r["role"] == "self"), None)
    med_score = statistics.median(r["score"] for r in direct) if direct else None
    depths = [r["depth"] for r in direct if r["depth"] is not None]
    med_depth = statistics.median(depths) if depths else None
    gap = (us["depth"] - med_depth) if us and us["depth"] is not None and med_depth is not None else None
    fires = bool(us and med_score is not None and us["score"] >= med_score and gap is not None and gap >= DEEPER)
    return {"rows": rows, "signals": [{"key": k, "label": lbl} for k, lbl, _ in SIGNALS] + [{"key": "no_discount", "label": "No discount seen"}],
            "direct_median_score": med_score, "direct_median_depth": med_depth, "our_score": us["score"] if us else None,
            "our_depth": us["depth"] if us else None, "depth_gap": gap, "fires": fires,
            "rule": f"Premium score = signals present / {len(SIGNALS) + 1}. Undercut: our score at or above the direct median while our "
                    f"discount runs {DEEPER} points or more deeper than theirs. A page with ads read and no percent seen reads 0."}


def draft(pr: dict, brand: str) -> str:
    return "\n".join([f"Offer policy: {brand} shows premium signals ({round(pr['our_score'] * 100)} percent, direct median "
                      f"{round(pr['direct_median_score'] * 100)} percent) and discounts {pr['our_depth']} percent against a direct median of "
                      f"{pr['direct_median_depth']:g}.",
                      "Policy: cap the first order code at 10 percent; replace the rest of the depth with a free pair at the 6-pack or a gift box.",
                      "Keep the full code only in win-back emails to lapsed buyers.",
                      "Test for 14 days on half of new visitors before it becomes the policy. The founder approves."])
