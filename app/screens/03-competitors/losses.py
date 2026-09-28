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
against a named competitor needs win-loss interviews (BRAND-C58) and reads unavailable until then.
"""
from __future__ import annotations

MIN_TIMES = 2
THEME_LADDER = {"durability": "durability", "value": "price_and_value", "style": None, "unknown": None}
THEME_LABEL = {"durability": "last longer", "value": "cost less", "style": "look better", "unknown": "win for a reason we cannot read"}


def _same(a: str, b: str) -> bool:
    x, y = (str(v or "").lower().replace(" ", "") for v in (a, b))
    return bool(x and y) and (x.startswith(y) or y.startswith(x))


def build(m: dict, brain) -> dict:
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
    for x in rows:
        x["answer"] = answer(x, m["brand"].capitalize())
    return {"rows": rows, "frames": frames, "win_rate": None,
            "win_rate_reason": "no win-loss interviews on file; run 5 against the top name (BRAND-C58)",
            "rule": f"On the plan when recommended instead of us {MIN_TIMES} or more times. The reason is a rule over their "
                    "ad angles and whether they are a tracked, priced page. Reddit counts only; never quoted, no usernames."}


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
