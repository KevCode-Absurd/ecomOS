"""Review comparison: our review themes (objection ladders: one-star and five-star counts per theme) against
the claims the tracked pages lead with on the same theme. Where they lead with a claim on the theme our
one-star reviews hit hardest, they are attacking where we are weak.

Theme to claim map (a rule, not judgement): durability -> durability angle; comfort_and_feel -> comfort;
fit_and_sizing -> fit; price_and_value -> a percent-off offer; mission_trust -> giving. Competitor review
counts are not in the brain (no competitor review pull yet) and read unavailable.

Rule COMP-R17: one of our TOP_THEMES (2) themes with the most one-star reviews is led with by
ATTACK_PAGES (2) or more direct pages. Answer: say our guarantee against it and send the top doubt to product (LIFE-C42).
"""
from __future__ import annotations

ATTACK_PAGES, TOP_THEMES = 2, 2
THEME_CLAIM = {"durability": ("angle", "durability"), "comfort_and_feel": ("angle", "comfort"), "fit_and_sizing": ("angle", "fit"),
               "price_and_value": ("offer", "percent_off"), "mission_trust": ("angle", "giving")}


def build(m: dict, brain, offer_types) -> dict:
    rows = []
    for r in brain.records("objection_ladders"):
        v = r.get("value") if isinstance(r.get("value"), dict) else {}
        rungs = v.get("rungs") or []
        one = sum((x.get("counts") or {}).get("one_star") or 0 for x in rungs)
        five = sum((x.get("counts") or {}).get("five_star") or 0 for x in rungs)
        theme = v.get("theme")
        kind, tag = THEME_CLAIM.get(theme, (None, None))
        leaders, direct = [], 0
        for p in m["pages"]:
            if p["role"] == "self" or p["source"] == "none":
                continue
            hit = (kind == "angle" and any(a["tag"] == tag for a in p["angles"])) or (
                kind == "offer" and tag in offer_types(p.get("offers_seen") or []))
            if hit:
                leaders.append(p["name"])
                direct += p["frame"] == "direct"
        top = max(rungs, key=lambda x: (x.get("counts") or {}).get("one_star") or 0) if rungs else {}
        rows.append({"theme": theme, "label": str(theme).replace("_", " "), "one_star": one, "five_star": five,
                     "praise_share": round(five / (one + five), 3) if one + five else None, "ladder": r["id"],
                     "top_doubt": top.get("doubt"), "proof": next((x.get("proof") for x in rungs if x.get("proof_ids")), None),
                     "no_proof": [x["doubt"] for x in rungs if not x.get("proof_ids")],
                     "claim": tag, "leaders": leaders, "direct_leaders": direct, "their_reviews": None})
    rows.sort(key=lambda x: (-x["one_star"], x["theme"]))
    worst = rows[0] if rows else None
    attack = next((r for r in rows[:TOP_THEMES] if r["direct_leaders"] >= ATTACK_PAGES), None)
    return {"rows": rows, "worst": worst["theme"] if worst else None, "attack": attack,
            "their_reviews_reason": "no competitor review pull yet; Amazon reviews by ASIN would fill it",
            "rule": f"Attacked: one of our {TOP_THEMES} themes with the most one-star reviews is led with by {ATTACK_PAGES} or more direct pages."}


def draft(a: dict, brand: str) -> str:
    return "\n".join([f"Answer the attack on {a['label']}.",
                      f"Ours: {a['one_star']} one-star and {a['five_star']} five-star reviews on {a['label']}. Top doubt: {a['top_doubt']}.",
                      f"Theirs: {', '.join(a['leaders'])} lead with {a['claim']}.",
                      f"Say: {a['proof'] or 'no proof on file; add it first'}",
                      ("Doubts with no proof: " + "; ".join(a["no_proof"]) + ".") if a["no_proof"] else "Every doubt has proof on file.",
                      "Ship: the guarantee line on the product page and in 2 ads; a ticket to product with the top doubt and its reviews.",
                      f"Never promise more than the {brand} guarantee says."])
