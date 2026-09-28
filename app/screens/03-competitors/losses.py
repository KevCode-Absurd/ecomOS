"""Why we lose the ones we lose, by name: the alternatives shoppers recommend instead of us, the reason a
rule reads for each, our own weak point on that reason, and the answer we write.

Sources: `competitors` records with recommended_instead (Reddit threads, counted, usernames never stored,
never quoted as a testimonial), the tracked pages' angle tags, `objection_ladders` one-star counts per
theme and the proof on file for each rung, `positioning.reddit_frames`.

Reason rule for a named alternative, first match wins:
  durability  the page runs a durability or guarantee angle
  style       the page runs a style angle
  value       the alternative is not a tracked page and has no price band: a cheaper rung of the ladder
  unknown     none of the above
Rule COMP-R15: an alternative recommended instead of us MIN_TIMES (2) or more times. The answer is a
"how we compare" page section and support macro from verified brain facts (BRAND-C57). The win rate
against a named competitor needs win-loss interviews (BRAND-C58) and reads unavailable until then. Interviews are
logged on the page (inputs.py): win rate = wins / (wins + losses) per name; COMP-R29 holds until MIN_INTERVIEWS (5)
are logged. With INTERVIEW_THEME_MIN (3) or more logged losses to a name, the reason is the top coded loss reason, not
the ad-angle rule, and the answer draws on that reason's objection ladder.
"""
from __future__ import annotations

MIN_TIMES = 2
MIN_INTERVIEWS = 5    # COMP-R29 stays on the plan until this many interviews are logged
THEME_LADDER = {"durability": "durability", "value": "price_and_value", "style": None, "unknown": None}
INTERVIEW_THEME_MIN = 3   # logged losses to one name before its reason comes from the interviews, not the ad-angle rule
# interview reason code -> theme, what shoppers say the rival does, our objection ladder theme
REASON_THEME = {"price and value": ("value", "cost less", "price_and_value"), "durability": ("durability", "last longer", "durability"),
                "fit and sizing": ("fit", "fit better", "fit_and_sizing"), "comfort and feel": ("comfort", "feel better", "comfort_and_feel"),
                "style": ("style", "look better", None), "availability": ("availability", "arrive sooner or stay in stock", "order_and_delivery"),
                "trust": ("trust", "feel safer to buy from", None), "other": ("unknown", "win for a reason we cannot read", None)}
THEME_LABEL = {"durability": "last longer", "value": "cost less", "style": "look better", "unknown": "win for a reason we cannot read"}


def _same(a: str, b: str) -> bool:
    x, y = (str(v or "").lower().replace(" ", "") for v in (a, b))
    return bool(x and y) and (x.startswith(y) or y.startswith(x))


def build(m: dict, brain, interviews: list[dict] | None = None, win_loss=None) -> dict:
    ladders = {}
    for r in brain.records("objection_ladders"):
        v = r.get("value") if isinstance(r.get("value"), dict) else {}
        rungs = v.get("rungs") or []
        ladders[v.get("theme")] = {"id": r["id"], "one_star": sum((x.get("counts") or {}).get("one_star") or 0 for x in rungs),
                                   "no_proof": [x["doubt"] for x in rungs if not x.get("proof_ids")],
                                   "proof": next((x.get("proof") for x in rungs if x.get("proof_ids")), None),
                                   "top_doubt": max(rungs, key=lambda x: (x.get("counts") or {}).get("one_star") or 0)["doubt"] if rungs else None}
    frames = (brain.get(f"{brain.brand}.positioning.reddit_frames") or {}).get("value") or {}
    rows = []
    for r in brain.records("competitors"):
        v = r.get("value") if isinstance(r.get("value"), dict) else {}
        if v.get("recommended_instead") is None:
            continue
        name = v.get("competitor")
        page = next((p for p in m["pages"] if p["role"] != "self" and _same(p["name"], name)), None)
        tags = {a["tag"]: a for a in (page or {}).get("angles") or []}
        priced = page is not None and page.get("price_text")
        if "durability" in tags:
            theme, why = "durability", f"their ads run durability (\"{tags['durability']['word']}\")"
        elif "style" in tags:
            theme, why = "style", f"their ads run style (\"{tags['style']['word']}\")"
        elif page is None or not priced:
            theme, why = "value", "not a tracked page and no price band: a cheaper rung"
        else:
            theme, why = "unknown", "no rule matched"
        lad = ladders.get(THEME_LADDER[theme]) if THEME_LADDER[theme] else None
        rows.append({"key": name.lower().replace(" ", "_"), "name": name, "times": v["recommended_instead"],
                     "upvotes": v.get("upvotes"), "where": v.get("subreddits") or [], "tracked": page is not None,
                     "theme": theme, "theme_label": THEME_LABEL[theme], "why": why, "record": r["id"],
                     "our_one_star": lad["one_star"] if lad else None, "top_doubt": lad["top_doubt"] if lad else None,
                     "no_proof": lad["no_proof"] if lad else [], "proof": lad["proof"] if lad else None,
                     "ladder": lad["id"] if lad else None, "fires": v["recommended_instead"] >= MIN_TIMES})
    rows.sort(key=lambda x: (-x["times"], -(x["upvotes"] or 0), x["name"]))
    names = [x["name"] for x in rows] + [p["name"] for p in m["pages"] if p["role"] != "self" and not any(_same(p["name"], x["name"]) for x in rows)]
    wl = win_loss(interviews or [], names) if win_loss else {"rows": [], "n": 0, "win_rate": None}
    top = next((x for x in rows if x["fires"]), rows[0] if rows else None)
    top_wl = next((w for w in wl["rows"] if top and w["name"] == top["name"]), None)
    for x in rows:
        x["win_loss"] = next((w for w in wl["rows"] if w["name"] == x["name"]), None)
        x["theme_source"] = "rule"
        w = x["win_loss"]
        if w and w["losses"] >= INTERVIEW_THEME_MIN:   # first-party reasons beat the ad-angle rule
            reason, n = next(iter(w["reasons"].items()))
            theme, label, ladder = REASON_THEME[reason]
            lad = ladders.get(ladder) if ladder else None
            x.update({"theme": theme, "theme_label": label, "theme_source": "interviews", "reason": reason,
                      "why": f"{n} of {w['losses']} logged losses name {reason}",
                      "our_one_star": lad["one_star"] if lad else None, "top_doubt": lad["top_doubt"] if lad else None,
                      "no_proof": lad["no_proof"] if lad else [], "proof": lad["proof"] if lad else None, "ladder": lad["id"] if lad else None})
    for x in rows:
        x["answer"] = answer(x, m["brand"].capitalize())
    return {"rows": rows, "frames": frames, "win_rate": top_wl["win_rate"] if top_wl else None, "win_rate_name": top["name"] if top else None,
            "win_loss": wl, "names": names, "min_interviews": MIN_INTERVIEWS, "kit": interview_kit(rows, m["brand"].capitalize(), term=(m.get("term") or {}).get("plural", "products")),
            "reason_codes": REASON_CODES, "interviews": wl["n"],
            "win_rate_reason": (f"no win-loss interviews against {top['name']} on file; run {MIN_INTERVIEWS} (BRAND-C58)" if top else
                                "no named alternative on file") if not (top_wl and top_wl["n"]) else None,
            "rule": f"On the plan when recommended instead of us {MIN_TIMES} or more times. The reason is a rule over their "
                    "ad angles and whether they are a tracked, priced page. Reddit counts only; never quoted, no usernames."}


# COMP-R31: the answer to a loss reason repeated 3 or more times against one name: artefact kind, what it is, the move
REASON_MOVE = {
    "price and value": ("offer", "a pack step offer", "Show the saving a pair on the pack ladder and add a pack step that beats their price per pair."),
    "durability": ("page_section", "a durability proof block", "Put the guarantee and the durability proof on the product page, above the fold."),
    "fit and sizing": ("page_section", "a fit and size block", "Add a size finder and a fit note on each product page, with the free exchange."),
    "comfort and feel": ("ad_brief", "2 comfort proof ads", "Brief 2 ads that show the feel: the proof point, a close-up, a wear test."),
    "style": ("ad_brief", "2 style ads", "Brief 2 ads that lead with the look: colours, outfits, the range side by side."),
    "availability": ("ticket", "a stock and delivery ticket", "Open a ticket to fix the stock gaps and say the delivery date on the page."),
    "trust": ("page_section", "a trust block", "Add reviews with counts, the guarantee and the returns promise near the buy button."),
    "other": ("research_note", "a follow-up round", "Run 3 more interviews on this name to find the real reason."),
}
REASON_CODES = ["price and value", "durability", "fit and sizing", "comfort and feel", "style", "availability", "trust", "other"]


def interview_kit(rows: list[dict], brand: str, n: int = 5, term: str = "products") -> str:
    names = [x["name"] for x in rows if x["fires"]][:3] or [x["name"] for x in rows][:3]
    return "\n".join([
        f"Win-loss kit: {n} interviews for each of {', '.join(names) or 'the top named alternatives'}.",
        f"Screener: bought {term} in the last 90 days; looked at {brand} and bought {names[0] if names else 'another brand'} instead "
        f"(loss) or bought {brand} after looking at them (win). 20 minutes, a gift card for their time.",
        "Guide: 1. What were you trying to fix? 2. Which brands did you look at, in order? 3. What made you pick the one you bought?",
        f"4. What almost stopped you buying it? 5. What would have made you pick {brand}? 6. How did price per pair feel?",
        "Coding sheet: one reason code per interview, from: " + ", ".join(REASON_CODES) + ". Quote only with written consent.",
        "Readout: win rate against each name, the repeated reason (3 or more interviews), and one change to test."])


def answer(x: dict, brand: str) -> str:
    lines = [f"How we compare: {brand} against {x['name']}.",
             f"Why shoppers pick them: they {x['theme_label']} ({x['why']}). Recommended instead {x['times']} times, "
             f"{x['upvotes'] if x['upvotes'] is not None else 'unknown'} upvotes.",
             (f"Our weak point there: {x['our_one_star']} one-star reviews on {x['ladder'].split('.')[-1].replace('_', ' ')}; "
              f"top doubt: {x['top_doubt']}.") if x["ladder"] else "Our weak point there: unavailable.",
             f"What we say, verified in the brain: {x['proof']}" if x["proof"] else "What we say: no proof on file. Add it first.",
             ("Doubts with no proof yet: " + "; ".join(x["no_proof"]) + ".") if x["no_proof"] else "Every rung has proof on file.",
             "Use: a compare block on the product page, one FAQ answer, one support macro. Name them only where the law and "
             "platform allow; never disparage.",
             "Reddit is a signal: never quoted as a testimonial, no usernames."]
    return "\n".join(lines)
