"""Competitor moves scored against the bottleneck: counter-proposals, ranked in code.

A move is a signal already in the brain: an angle competitors run that we do not (coverage gaps), a format or hook
form they run more (market gaps), a name Reddit recommends instead of us on a doubt (recommended instead), a frame
Reddit uses that our positioning does not carry, an angle we contest with a competitor, and a name Reddit
recommends that we do not track. Each move is matched to the diagnosis's bottlenecks by words (the bottleneck's
theme and text against the move's angle, doubt or frame) and scored: fit (the matched bottleneck's rank: 3 for the
first, 2 for the second, 1 for the third, 0 for none) times 10, plus evidence (competitor count, mentions or threads,
capped at 10). A move that matches no bottleneck is a watch item, never a counter-proposal. Each counter-proposal
carries the 3 response options (match, hold, counter) in plain words and links to the master-list action that
already exists for it, so deciding here is deciding there. Competitor ads are signals: layout and mood only.
"""
from __future__ import annotations

import re

STOP = set("the a an and or of to in on for with is are was were be it its this that these those at from by as not no vs our we us they them".split())
FIT_WEIGHT = {1: 3, 2: 2, 3: 1}


def _words(s) -> set[str]:
    return {w for w in re.findall(r"[a-z]{4,}", str(s or "").lower().replace("_", " ")) if w not in STOP}


def _bottleneck_words(b: dict) -> tuple[set[str], set[str]]:
    key = _words(b["theme"])
    return key, key | _words((b.get("text") or "")[:200])


def moves_from(brain, coverage: dict, gaps: list[dict], signals: dict) -> list[dict]:
    out = []
    for g in coverage.get("gaps") or []:
        out.append({"kind": "angle_gap", "key": g["angle"], "label": f"{g['label']} angle: {len(g['competitors'])} competitors run it, we run 0", "words": _words(g["label"]) | _words(g["angle"]),
                    "evidence": len(g["competitors"]), "who": g["competitors"], "action_entity": f"angle_{g['angle']}", "records": g.get("record_ids") or [],
                    "options": {"match": f"Brief 3 concepts on the {g['label'].lower()} angle from the proof we hold.", "hold": "Leave the angle to them while our own ground converts; recheck at the next snapshot.", "counter": f"Answer the angle with proof they cannot copy: our own guarantee, giving or construction facts, on the surfaces the ladder names."}})
    for g in gaps or []:
        lab = f"{g['label']} {'ads' if g['kind'] == 'format' else 'hooks'}: they {round(g['them'] * 100)} percent, we {round(g['us'] * 100)} percent"
        out.append({"kind": f"{g['kind']}_gap", "key": g["key"], "label": lab, "words": _words(g["label"]) | {"creative", "format", "hook"} | ({"catalog", "dynamic", "retargeting"} if g["key"] in ("dco", "dpa") else set()),
                    "evidence": len(g.get("leaders") or []), "who": [x["name"] for x in g.get("leaders") or []], "action_entity": f"{g['kind']}_{g['key']}", "records": g.get("record_ids") or [],
                    "options": {"match": f"Make 3 {g['label'].lower()} {'ads' if g['kind'] == 'format' else 'hooks'} from existing assets and test against our best.", "hold": "Keep our mix; a format share is a signal, not a result.", "counter": f"Test the opposite: our strongest static proof against their {g['label'].lower()} volume, and read the result before copying the mix."}})
    for r in signals.get("recommended") or []:
        out.append({"kind": "recommended_instead", "key": r["slug"], "label": f"Reddit recommends {r['competitor']} instead of us on {r.get('doubt_label', 'a doubt').lower()}: {r['threads']} threads, {r['upvotes']} upvotes", "words": _words(r.get("doubt_label")) | _words(r.get("doubt_angle")) | _words(r["competitor"]),
                    "evidence": min(10, r["threads"] + (r["upvotes"] // 50)), "who": [r["competitor"]], "action_entity": f"recommended_{r['slug']}", "records": [r.get("record_id")],
                    "options": {"match": f"Answer the doubt where they win ({', '.join(r.get('where') or [])[:80] or 'the surfaces the ladder names'}) with the proof on file.", "hold": "Accept the loss on that doubt and lead on our own ground.", "counter": f"Fix the doubt at the root: {r.get('proof_status') or 'proof'} on the deal-breaker rung, then say it on every surface."}})
    for f in signals.get("frames") or []:
        if f.get("covered_by_our_frame"):
            continue
        out.append({"kind": "frame", "key": f["frame"], "label": f"Reddit frames the category as '{f['label']}' ({f['mentions']} mentions); our positioning does not carry it", "words": _words(f["label"]) | set().union(*[_words(a) for a in f.get("angles") or []]) if f.get("angles") else _words(f["label"]),
                    "evidence": min(10, f["mentions"]), "who": [], "action_entity": f"frame_{f['frame']}", "records": [],
                    "options": {"match": f"Add '{f['label']}' to the positioning frame with the proof that earns it.", "hold": "Keep our frame; note the phrase in the language bank for copy.", "counter": "Own a different word for the same job and prove it with our numbers."}})
    for c in coverage.get("contested") or []:
        out.append({"kind": "contested", "key": c["angle"], "label": f"{c['label']} angle is contested: we run {c['us_n']} ads, {', '.join(c['competitors'])} run it too", "words": _words(c["label"]) | _words(c["angle"]),
                    "evidence": len(c["competitors"]), "who": c["competitors"], "action_entity": None, "records": [],
                    "options": {"match": "Keep parity on volume; proof and format decide it.", "hold": "Let the angle run as is and measure it against the rest.", "counter": "Out-prove them: the specific fact, number or guarantee only we can say on this angle."}})
    for p in signals.get("proposed") or []:
        out.append({"kind": "new_name", "key": p["slug"], "label": f"{p['name']} is recommended on Reddit and not tracked (score {p['score']})", "words": _words(p["name"]) | set().union(*[_words(x) for x in p.get("reasons") or []]),
                    "evidence": min(10, int(p.get("score") or 0)), "who": [p["name"]], "action_entity": None, "records": [],
                    "options": {"match": "Paste the page id and pull their ads into the set.", "hold": "Leave them untracked; they sit outside the direct set.", "counter": "Read their Reddit threads only, no pull, and note the doubt they win on."}})
    return out


def counter_proposals(brain, bottlenecks: list[dict], coverage: dict, gaps: list[dict], signals: dict, master_actions: list[dict]) -> dict:
    by_entity = {(a.get("entity") or {}).get("id"): a for a in master_actions if a.get("entity")}
    ranked, watch = [], []
    for m in moves_from(brain, coverage, gaps, signals):
        best, best_fit, overlap_best = None, 0, set()
        for b in bottlenecks:
            key, words = _bottleneck_words(b)
            overlap = m["words"] & words
            hit = bool(key & m["words"]) or len(overlap) >= 2
            fit = FIT_WEIGHT.get(b.get("rank"), 0) if hit else 0
            if fit > best_fit:
                best, best_fit, overlap_best = b, fit, overlap
        a = by_entity.get(m["action_entity"]) if m.get("action_entity") else None
        row = {k: m[k] for k in ("kind", "key", "label", "evidence", "who", "options", "records")}
        row.update(bottleneck=best["key"] if best else None, bottleneck_theme=best["theme"] if best else None, fit=best_fit, overlap=sorted(overlap_best)[:4],
                   score=best_fit * 10 + min(10, m["evidence"]), action=({"id": a["id"], "title": a["title"], "owner": a["owner"], "total": (a.get("rubric") or {}).get("total"), "decision": a.get("decision"), "capability": (a.get("capability") or {}).get("id") if isinstance(a.get("capability"), dict) else a.get("capability")} if a else None))
        (ranked if best_fit else watch).append(row)
    ranked.sort(key=lambda r: (-r["score"], r["label"]))
    watch.sort(key=lambda r: (-r["evidence"], r["label"]))
    return {"counter_proposals": ranked, "watch": watch, "counts": {"moves": len(ranked) + len(watch), "against_bottleneck": len(ranked), "watch": len(watch), "with_action": sum(1 for r in ranked if r["action"])},
            "scoring": "fit (matched bottleneck rank: 3, 2, 1) times 10, plus evidence capped at 10",
            "note": "Moves are the signals already in the brain, matched to the diagnosis by words and scored in code. A move that touches no bottleneck is a watch item. Options are plain words; the decision is taken on the master-list action the move links to. Competitor ads are signals: layout and mood only, never their text, logos, products or faces."}
