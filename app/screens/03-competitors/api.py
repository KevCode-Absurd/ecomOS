"""Competitors and market screen API: /api/03-competitors/...

Reads the brand brain through app/brain/store.py (the competitors section and
the raw Ad Library records as fallback) and the simulated products_monthly
table through app/data/tables.py. The market model and the audit rules live
in audit.py; this file shapes them for the page. No writes, nothing external.

  GET  plan       the plan board: ranked actions (actions.py) with decisions
                  applied, connect actions, orientation numbers, findings, rules
  GET  overview   the desk: pages side by side, coverage matrix, hook and offer
                  mix, references, price and pack ladder, positioning map,
                  changes, freshness and the re-pull plan
  GET  notes?entity=  POST notes {entity, text}  team notes on a page or action (local, git-ignored)
  GET  briefs     every drafted artefact on the plan, one text per team
  GET  competitor_snapshot  the events.md hand-off rows (also written to fixtures by capture.py)
  GET  experiments          registry rows drafted from open test actions, for 25-experiments
  GET  digest     the weekly competitor brief as plain text, built from the plan
  GET  audit      findings from audit.py (app/contracts/audit.md shape)
  rank(brand, window)  the depth contract override app/rank.py calls

Query `brand` (default bombas) and `today` (YYYY-MM-DD, default the real date)
work on every route. Set BRAIN_ROOT to point at a copy of app/brain (tests do).
"""
from __future__ import annotations

import datetime as dt
import json
import importlib.util
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
BRAIN_ROOT: Path | None = None
SAFE_BRAND = re.compile(r"^[a-z0-9_-]+$")
SIMULATED_NOTE = ("{name} is the sample brand. Its prices per {unit} come from simulated sales. "
                  "Competitor facts are public signals from the Meta Ad Library and public product feeds.")
SIGNAL_NOTE = ("Public signals only. Ad counts and run length show what a brand keeps live, not what works. "
               "Formats and hooks are for layout and mood. Never copy their text, logos, products or faces.")

# The server reloads api.py when it changes but not the modules it loads, so drop this folder's cached modules
# first: a reload then sees every edited file, never a stale mix.
import sys as _sys  # noqa: E402
for _stem in (p.stem for p in HERE.glob("*.py")):
    _sys.modules.pop(f"competitors_{_stem}", None)
_spec = importlib.util.spec_from_file_location("competitors_actions", HERE / "actions.py")
actions = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(actions)
audit = actions.audit
AXES = {
    "durability": {"label": "Durability claim", "max": audit.DURABILITY_MAX,
                   "plain": "1 point each: a guarantee, a lifetime guarantee, durability named in the positioning"},
    "comfort": {"label": "Comfort claim", "max": audit.COMFORT_MAX,
                "plain": "1 point each: comfort named, a relief hook, a proof hook (lab, doctor, athlete or creator)"},
}


def _today(req) -> dt.date:
    t = req.arg("today")
    return dt.date.fromisoformat(t) if t else dt.date.today()


def _brand(req) -> str:
    b = req.arg("brand", "bombas")
    if not SAFE_BRAND.match(b):
        raise ValueError("bad brand")
    return b


def _public(c: dict) -> dict:
    return {k: v for k, v in c.items() if not k.startswith("_")}


def gaps(m: dict) -> dict | None:
    """The widest gap between neighbouring median prices per pair, brand included."""
    pts = [(c["price"]["median"], c["name"]) for c in m["competitors"] if c["price"]["median"] is not None]
    if m["packs"]["available"]:
        pts.append((m["packs"]["median_per_pair"], m["brand"].capitalize()))
    pts.sort()
    best = None
    for (a, an), (b, bn) in zip(pts, pts[1:]):
        if best is None or b - a > best["to"] - best["from"]:
            best = {"from": a, "to": b, "below": an, "above": bn}
    return best


def positioning(m: dict) -> dict:
    comps = m["competitors"]
    split_x = m["category_median"]
    pts = [{"name": c["name"], "brand": False, "x": c["price"]["median"], "low": c["price"]["low"],
            "high": c["price"]["high"], "rough": c["price"]["rough"], "durability": c["durability"],
            "comfort": c["comfort"]} for c in comps]
    packs = m["packs"]
    pts.append({"name": m["brand"].capitalize(), "brand": True,
                "x": packs.get("median_per_pair"), "low": packs.get("low"), "high": packs.get("high"),
                "rough": False, "durability": m["profile"]["durability"], "comfort": m["profile"]["comfort"],
                "simulated": True})
    quads = {}
    for axis, spec in AXES.items():
        split_y = spec["max"] / 2
        q = []
        for hi_x in (False, True):
            for hi_y in (True, False):
                names = [p["name"] for p in pts if not p["brand"] and p["x"] is not None and split_x is not None
                         and (p["x"] >= split_x) == hi_x and (p[axis] >= split_y) == hi_y]
                q.append({"x_high": hi_x, "y_high": hi_y, "competitors": names,
                          "label": f"{'higher' if hi_x else 'lower'} price, {'strong' if hi_y else 'weak'} "
                                   f"{spec['label'].lower()}"})
        quads[axis] = {"split_y": split_y, "quadrants": q,
                       "openness": (f"{sum(1 for x in q if not x['competitors'])} of 4"
                                    if split_x is not None and len(comps) >= 3 else None)}
    kit = {axis: map_kit(m, pts, axis, quads[axis], split_x) for axis in AXES}
    return {"points": pts, "split_x": split_x, "axes": AXES, "quadrants": quads, "kit": kit,
            "not_placed": [p["name"] for p in m["pages"] if p["role"] != "self" and not any(
                audit.pagemod._same(p["name"], q["name"]) for q in pts if q["x"] is not None)]}


QUAD_ORDER = [(False, True), (True, True), (False, False), (True, False)]   # kit order: tl, tr, bl, br


def map_kit(m: dict, pts: list[dict], axis: str, q: dict, split_x) -> dict:
    """Props for Charts.positioningMap plus one move per quadrant: hold, contest, claim or skip."""
    spec = AXES[axis]
    size = {p["name"]: p["active_ads"] for p in m["pages"]}
    points = []
    for p in pts:
        if p["x"] is None:
            continue
        n = next((v for k, v in size.items() if audit.pagemod._same(k, p["name"])), None)
        points.append({"label": p["name"], "x": p["x"], "y": p[axis], "us": p["brand"], "size": n,
                       "note": ("simulated net price" if p["brand"] else ("rough price read" if p["rough"] else "public price band"))})
    us = next((p for p in pts if p["brand"]), None)
    moves = []
    texts = m["profile"]["_texts"]
    missing = [x["part"] for x in audit.score_parts(texts, axis) if not x["has"]]
    for hi_x, hi_y in QUAD_ORDER:
        quad = next(x for x in q["quadrants"] if x["x_high"] == hi_x and x["y_high"] == hi_y)
        ours = us is not None and us["x"] is not None and split_x is not None and (us["x"] >= split_x) == hi_x and (us[axis] >= q["split_y"]) == hi_y
        same_side = us is not None and us["x"] is not None and split_x is not None and (us["x"] >= split_x) == hi_x
        if ours:
            kind, text = "hold", (f"Ours. Shared with {', '.join(quad['competitors'])}. Defend it with proof in every ad."
                                  if quad["competitors"] else "Ours alone. Say it in every ad and on every page.")
        elif hi_y and not quad["competitors"]:
            kind, text = "claim", "Open. No tracked brand claims it. Test a positioning line that takes it."
        elif hi_y and same_side:
            kind, text = "contest", (f"{', '.join(quad['competitors'])} hold it. We move in with " +
                                     (" and ".join(missing[:2]) if missing else "a stronger proof") + ".")
        else:
            kind, text = "skip", "Not a target for us on this capture."
        moves.append({"label": quad["label"], "competitors": quad["competitors"], "kind": kind, "text": text,
                      "open": not quad["competitors"]})
    labels = [mv["label"] + (" (open)" if mv["open"] else "") for mv in moves]
    return {"x": {"label": f"Median price per {m['term']['unit']}, US dollars", "unit": "$", "min": 0,
                  "max": max([p["x"] for p in points] + [10]) * 1.15},
            "y": {"label": f"{spec['label']}, 0 to {spec['max']}", "min": -0.3, "max": spec["max"] + 0.3},
            "points": points, "quadrants": labels, "midX": split_x, "midY": q["split_y"], "moves": moves,
            "missing": missing, "plain": spec["plain"]}


def orientation(m: dict) -> list[dict]:
    """3 to 6 small numbers beside the plan: where the competitive position stands today."""
    comps = [p for p in m["pages"] if p["role"] != "self"]
    ads = sorted(p["active_ads"] for p in comps if isinstance(p["active_ads"], int))
    ages = [p["age_days"] for p in comps if p["age_days"] is not None and p["source"] != "none"]
    lo, hi = audit.PRICE_BAND
    idx = m["price_position_index"]
    threats = sum(1 for p in comps if (p.get("verdict") or {}).get("text") == "Threat")
    return [
        {"label": "pages tracked", "value": len(comps), "unit": "n", "title": "competitor pages in the brain's competitive frame"},
        {"label": "threats", "value": threats, "unit": "n", "tone": "bad" if threats else None, "title": "pages with a threat verdict"},
        {"label": "our active ads", "value": m["profile"]["active_ads"], "unit": "n", "title": "latest Ad Library capture"},
        {"label": "theirs, median a page", "value": ads[len(ads) // 2] if ads else None, "unit": "n",
         "title": "median active ads across tracked pages, public signal"},
        {"label": "price index", "value": idx, "unit": "n", "tone": None if idx is None else ("bad" if not lo <= idx <= hi else "good"),
         "title": f"our price per {m['term']['unit']} / tracked median x 100, band {lo} to {hi}, simulated brand price"},
    ]


def rank(brand: str = "bombas", window: dict | None = None) -> dict:
    """The screen's ranked actions (depth.md section 5). app/rank.py and the server call this."""
    out = actions.build(brand, window, BRAIN_ROOT)
    out.pop("findings", None)
    return out


QUEUE_MAX = 5
OVERDUE_DAYS = 7   # a decided move with no outcome this many days past its check date is overdue


def overdue(acts: list[dict], today: dt.date) -> list[dict]:
    """Decided moves (not snoozed) with no logged outcome, OVERDUE_DAYS or more past their check date, most late first."""
    out = []
    for a in acts:
        d = a.get("decision") or {}
        if not d or d.get("choice") in ("not_now", "undo") or a.get("outcome") or not a.get("check_on"):
            continue
        late = (today - dt.date.fromisoformat(a["check_on"])).days
        if late >= OVERDUE_DAYS:
            out.append({"id": a["id"], "title": a["title"], "check_on": a["check_on"], "days_late": late, "owner": a["owner"]})
    return sorted(out, key=lambda x: (-x["days_late"], x["id"]))


def founder_queue(acts: list[dict], late: list[dict] | None = None) -> dict:
    """The calls only the founder can make, top QUEUE_MAX by plan rank: undecided moves that are founder gated, or that
    an agent drafts and a person approves. Each says what yes sets going next and when it is checked."""
    out = []
    for rank, a in enumerate(acts, 1):
        if a.get("status") == "unavailable" or a.get("decision"):
            continue
        gate = a["capability"]["autonomy"] == "founder_gate"
        if not (gate or a["owner"] == "agent_drafts"):
            continue
        approve = next((st for st in a["steps"] if st["who"] == "person"), None)
        after = next((st["text"] for st in a["steps"] if approve and st["n"] > approve["n"]), None)
        out.append({"id": a["id"], "rank": rank, "title": a["title"], "why": a["why"], "gate": gate,
                    "question": ("Decide: " if gate else "Approve: ") + a["artefact"]["label"],
                    "yes": after or "The agent ships it and reports on the check date.", "check_on": a.get("check_on"),
                    "capability": a["capability"]["id"], "autonomy": a["capability"]["autonomy"], "owner": a["owner"]})
    reads = [{"id": x["id"], "rank": next((i for i, a in enumerate(acts, 1) if a["id"] == x["id"]), None), "title": x["title"], "why": "",
              "gate": False, "question": f"Read the result: {x['days_late']} days past its check date",
              "yes": "Log the outcome on the check due lane; a lost move is held 90 days.", "check_on": x["check_on"],
              "capability": next(a["capability"]["id"] for a in acts if a["id"] == x["id"]),
              "autonomy": next(a["capability"]["autonomy"] for a in acts if a["id"] == x["id"]), "owner": "person", "overdue": True}
             for x in late or []]
    out = reads + out
    return {"items": out[:QUEUE_MAX], "total": len(out), "overdue": len(reads),
            "rule": f"Overdue reads first ({OVERDUE_DAYS} or more days past the check date with no outcome), then undecided moves "
                    f"that are founder gated or drafted for approval, by plan rank; top {QUEUE_MAX}."}


def plan(brand: str, today: dt.date) -> dict:
    """The plan board: ranked actions with decisions applied, the findings they close, and the orientation."""
    window = actions.ranker.default_window(28, (today - dt.timedelta(days=1)).isoformat())
    out = actions.build(brand, window, BRAIN_ROOT)
    acts = actions.ranker.apply_decisions(out["actions"], today)
    m = audit.market(brand, today, BRAIN_ROOT)
    return {"brand": brand, "window": window, "brain_version": out["brain_version"], "simulated": True,
            "orient": orientation(m), "actions": [a for a in acts if a.get("status") != "unavailable"],
            "connect": [a for a in acts if a.get("status") == "unavailable"],
            "snoozed": len(out["actions"]) - len(acts), "findings": out["findings"], "rules": audit.RULES,
            "groups": [{"key": k, "label": v} for k, v in audit.GROUP_LABEL.items()], "rule_group": audit.RULE_GROUP,
            "thresholds": m["thresholds"], "queue": founder_queue(acts, late := overdue(acts, today)), "overdue": late, "held": out.get("held") or [], "hold_days": actions.HOLD_LOST_DAYS,
            "snapshot_age_days": max(ages) if (ages := [p["age_days"] for p in m["pages"] if p["age_days"] is not None]) else None}


def page_rows(m: dict) -> dict:
    """The side-by-side table: every tracked page plus ours, with verdicts, pill counts and a battlecard draft."""
    us = next(p for p in m["pages"] if p["role"] == "self")
    price_us = m["packs"].get("median_per_pair") if m["packs"]["available"] else None
    rows = []
    for p in m["pages"]:
        r = {k: v for k, v in p.items() if k not in ("quotes",)}
        if p["role"] != "self":
            gaps = [a["label"] for a in m["angles"] if a["held"] and p["name"] not in a["competitors_using"]]
            r["battlecard"] = audit.pagemod.battlecard(p, us, price_us, gaps)
            r["quoted_ads"] = len(p["quotes"])
        rows.append(r)
    comps = [r for r in rows if r["role"] != "self"]
    pills = [{"key": "all", "label": "All", "n": len(comps)},
             {"key": "direct", "label": "Direct", "n": sum(r["frame"] == "direct" for r in comps)},
             {"key": "basics", "label": "Basics and apparel", "n": sum(r["frame"] == "basics" for r in comps)},
             {"key": "threat", "label": "Threats", "n": sum(r["verdict"]["text"] == "Threat" for r in comps)}]
    return {"rows": rows, "pills": pills, "our_top_angles": m["our_top_angles"], "snapshot": m["snapshot"],
            "format_labels": audit.snap.FORMAT_LABEL, "line_labels": audit.snap.FIRST_LINE_LABEL,
            "rule": f"Threat at {audit.pagemod.THREAT_AT} points or more, watch at {audit.pagemod.WATCH_AT} to "
                    f"{audit.pagemod.THREAT_AT - 1}. Points: direct competitor 2, active ads 2x ours 1, median ad live "
                    "30 days or more 1, runs one of our top 2 angles 1, recommended instead of us on Reddit 1."}


FRESH_DAYS, AGEING_DAYS = 7, 30


def freshness(m: dict, brand: str) -> dict:
    """Per page: page id, last capture, age, source; the re-pull plan with its estimate. Nothing runs from here."""
    rows = []
    for p in m["pages"]:
        age = p.get("age_days")
        kind = ("na" if p["source"] == "none" else "keep" if age is not None and age <= FRESH_DAYS
                else "watch" if age is not None and age <= AGEING_DAYS else "fix")
        text = {"na": "No capture", "keep": "Fresh", "watch": "Ageing", "fix": "Stale"}[kind]
        rows.append({"name": p["name"], "role": p["role"], "page_id": p["page_id"], "captured_at": p.get("captured_at") if p["source"] != "none" else None,
                     "age_days": age if p["source"] != "none" else None, "source": p["source"], "kind": kind, "text": text})
    try:
        plan_ = audit.snap.plan(brand, BRAIN_ROOT or audit.snap.BRAIN)
    except (OSError, ValueError, KeyError) as exc:
        plan_ = {"error": f"no pull config: {exc}"}
    caps = audit.capmod.captures(brand)
    return {"rows": rows, "plan": plan_, "snapshot": m["snapshot"], "fresh_days": FRESH_DAYS, "ageing_days": AGEING_DAYS,
            "captures": {"n": len(caps), "last": caps[-1].stem if caps else None},
            "command": f"python3 app/screens/03-competitors/snapshot.py --brand {brand} --live",
            "rule": f"Fresh up to {FRESH_DAYS} days, ageing to {AGEING_DAYS}, stale after. A page with no capture reads no capture, never 0."}


def logged_week(brand: str, today: dt.date, days: int = 7) -> dict:
    """What the team logged on this screen in the last `days` days (by the record's own date, else when it was logged)."""
    start = (today - dt.timedelta(days=days - 1)).isoformat()
    recs = [r for r in audit.inpmod.read(brand) if start <= (r.get("date") or r.get("logged_at", "")[:10]) <= today.isoformat()]
    recs.sort(key=lambda r: (r.get("date") or r.get("logged_at", ""), r["id"]))
    counts: dict[str, int] = {}
    for r in recs:
        counts[r["kind"]] = counts.get(r["kind"], 0) + 1
    return {"from": start, "to": today.isoformat(), "n": len(recs), "counts": counts,
            "lines": [audit.inpmod.summary(r) for r in recs]}


def digest(brand: str, today: dt.date) -> dict:
    """The weekly competitor brief: what changed, the top moves, the one number to watch. Built from the plan in code."""
    m = audit.market_full(brand, today, BRAIN_ROOT)
    p = plan(brand, today)
    name = brand.capitalize()
    acts = p["actions"][:5]
    ch = m["changes"]
    lines = [f"Competitor brief for {name}, week of {today.isoformat()}. Simulated sales, public signals.", "",
             "What changed:"]
    changed = [e for e in ch["events"] if e["verdict"] in ("follow", "watch")][:4]
    lines += [f"- {e['page']}: {e['text']} ({e['verdict_text'].lower()})" for e in changed] or ["- nothing that crosses a rule"]
    lines += ["", "Top moves this week:"]
    lines += [f"{i + 1}. {a['title']} ({UI_OWNER.get(a['owner'], a['owner'])})" for i, a in enumerate(acts)] or ["none open"]
    lw = logged_week(brand, today)
    lines += ["", f"What the team logged this week ({lw['n']}):"]
    lines += [f"- {x}" for x in lw["lines"][:6]] or ["- nothing yet: interviews, prices seen and card checks go on the screen"]
    if lw["n"] > 6:
        lines.append(f"- and {lw['n'] - 6} more on the screen")
    threats = [r["name"] for r in m["pages"] if (r.get("verdict") or {}).get("text") == "Threat"]
    v = m["velocity"]
    lines += ["", f"Threats: {', '.join(threats) if threats else 'none'}.",
              f"Pace: we ship about {audit.velmod.now_rate(v)} new ads a week; direct pages about {v['direct_median_rate']} (estimate).",
              f"Price index: {m['price_position_index'] if m['price_position_index'] is not None else 'unavailable'} (100 is the tracked median).",
              "", "Signals only. Never copy their text, logos, products or faces."]
    return {"text": "\n".join(lines), "actions": len(p["actions"]), "changes": len(changed), "week_of": today.isoformat(), "logged": lw}


UI_OWNER = {"agent": "agent does it", "agent_drafts": "agent drafts, you approve", "person": "a person does it"}


STALE_CARD_DAYS = 90


def battlecards(m: dict, pages: dict) -> dict:
    """One battlecard per direct page: the verified differences, the date they were last checked and a freshness flag."""
    rows = []
    for r in pages["rows"]:
        if r["role"] == "self" or r["frame"] != "direct" or r["source"] == "none":
            continue
        age = r.get("card_age_days", r.get("age_days"))
        rows.append({"name": r["name"], "key": r["key"], "verified_on": r.get("card_checked_on") or r.get("captured_at"), "age_days": age,
                     "checked_by": "a person" if r.get("card_checked_on") else "the capture",
                     "stale": age is not None and age > STALE_CARD_DAYS, "card": r["battlecard"],
                     "claims": [ln for ln in r["battlecard"].split("\n")[1:] if ln and not ln.startswith("Say only")]})
    return {"rows": rows, "stale_days": STALE_CARD_DAYS,
            "all_text": "\n\n".join(x["card"] for x in rows),
            "rule": f"A battlecard is stale when its facts were last checked more than {STALE_CARD_DAYS} days ago, by a person or a capture."}


def placements(m: dict) -> dict:
    """Where each page runs its ads (Meta placements from the pull), against ours. Gap: a placement most direct pages use."""
    rows = [{"name": p["name"], "role": p["role"], "frame": p["frame"], "platforms": p.get("platforms") or []}
            for p in m["pages"] if p["source"] != "none"]
    allp = sorted({x for r in rows for x in r["platforms"]})
    direct = [r for r in rows if r["frame"] == "direct" and r["platforms"]]
    us = next((r for r in rows if r["role"] == "self"), None)
    counts = {pl: sum(pl in r["platforms"] for r in direct) for pl in allp}
    gaps = [pl for pl in allp if direct and counts[pl] >= max(2, len(direct) // 2 + 1) and us and us["platforms"] and pl not in us["platforms"]]
    return {"rows": rows, "platforms": allp, "direct_counts": counts, "ours_known": bool(us and us["platforms"]), "gaps": gaps,
            "rule": "A placement most direct pages run and we do not is a gap. Our placements need the ad-level pull when the brain lacks them."}


# Every desk block ends in a line that names the gap and offers the action (depth.md section 2, row 5).
SECTION_RULES = {"review": ["COMP-R32", "COMP-R28", "COMP-R11"], "season": ["COMP-R30"], "history": [], "handoff": [], "macros": ["COMP-R15"], "pages": ["COMP-R15"], "cards": ["COMP-R27"], "landing": ["COMP-R26"], "losses": ["COMP-R31", "COMP-R15", "COMP-R29"],
                 "category": ["COMP-R16"], "reviews": ["COMP-R17"], "coverage": ["COMP-R05", "COMP-R01"], "velocity": ["COMP-R19"],
                 "mix": ["COMP-R06", "COMP-R07", "COMP-R08"], "placements": [], "refs": ["COMP-R03"], "changes": ["COMP-R24", "COMP-R12"],
                 "niche": ["COMP-R20"], "map": ["COMP-R11"], "frames": ["COMP-R32", "COMP-R28"], "premium": ["COMP-R21"],
                 "prices": ["COMP-R25", "COMP-R33", "COMP-R34", "COMP-R09", "COMP-R10", "COMP-R02"], "search": ["COMP-R22", "COMP-R23"], "presence": ["COMP-R18"],
                 "fresh": ["COMP-R14", "COMP-R13"]}
HOLD = {"handoff": "The snapshot is written with each capture; tests are proposed when you approve them.", "history": "Threat trend is drawn from the dated captures.", "pages": "No named loss on this capture; keep the battlecards fresh.", "placements": "Our placements are not in the brain; the pull fills them.",
        "refs": "No offer they keep live that we hold and do not run.", "map": "No open strong-claim corner; contest the one beside us.",
        "category": "Every rung is mapped.", "cards": "Every battlecard is fresh."}


def gap_lines(acts: list[dict]) -> dict:
    by_rule = {}
    for a in acts:
        by_rule.setdefault(a.get("rule_id"), []).append(a)
    out = {}
    for sec, rules in SECTION_RULES.items():
        hit = next((by_rule[r][0] for r in rules if r in by_rule), None)
        if hit:
            n = sum(len(by_rule.get(r, [])) for r in rules)
            text = hit["why"] if hit.get("status") != "unavailable" else f"Unavailable until a source is connected: {hit['title'].split(' so ')[0].removeprefix('Connect ')}."
            out[sec] = {"text": text, "action_id": hit["id"], "title": hit["title"], "owner": hit["owner"],
                        "status": hit.get("status"), "more": n - 1}
        else:
            out[sec] = {"text": HOLD.get(sec, "No gap passes the rules on this capture."), "action_id": None, "title": None,
                        "owner": None, "status": None, "more": 0}
    return out


def macros(m: dict) -> dict:
    """Support answers built from verified brain fields: one per name we lose to, one per top review doubt with proof.
    A doubt with no proof on file gets no answer, only a note to add the proof."""
    name = m["brand"].capitalize()
    out, missing = [], []
    for x in (m.get("losses") or {}).get("rows", []):
        if not x["fires"]:
            continue
        ans = (f"Great question. Many people who like {x['name']} choose {name} for how it feels day to day. "
               + (f"{x['proof']} " if x["proof"] else "") + "If a pair ever lets you down, tell us and we will make it right.")
        out.append({"question": f"How do you compare to {x['name']}?", "answer": ans if x["proof"] else None,
                    "source": x["ladder"] or x["record"], "theme": x["theme"]})
        if not x["proof"]:
            missing.append(f"{x['name']} ({x['theme_label']})")
    for r in (m.get("reviews") or {}).get("rows", [])[:3]:
        q = (r["top_doubt"] or "").rstrip("?")
        if not q:
            continue
        out.append({"question": q[0].upper() + q[1:] + "?", "answer": (f"{r['proof']} If it does not work out, tell us and we will make it right."
                    if r["proof"] else None), "source": r["ladder"], "theme": r["theme"]})
        if not r["proof"]:
            missing.append(r["label"])
    return {"rows": out, "missing": missing, "ready": sum(1 for x in out if x["answer"]),
            "rule": "Answers use only verified brain proof and the guarantee. A doubt with no proof gets no answer until the proof is added. "
                    "Never name a rival negatively."}


def room_metrics(m: dict, pos: dict, cards: dict) -> list[dict]:
    """The metrics the room spec names, each computed from this screen's models or unavailable with the reason."""
    comps = [p for p in m["pages"] if p["role"] != "self"]
    q = pos["quadrants"]["durability"]
    pm = m.get("price_moves") or {}
    v, pr, n, cat = m["velocity"], m["premium"], m["niche"], m["category"]
    us_share = next((r["share"] for r in v["rows"] if r["role"] == "self"), None)
    ages = [r["age_days"] for r in cards["rows"] if r["age_days"] is not None]
    row = lambda k, val, unit, formula, why=None: {"key": k, "value": val, "unit": unit, "formula": formula,  # noqa: E731
                                                    "unavailable": None if val is not None else why}
    return [
        row("competitors_tracked", len(comps), "n", "pages in the brain's competitive frame"),
        row("price_position_index", m["price_position_index"], "index", "our price per unit / tracked median x 100", "no store prices or no bands"),
        row("price_change_count", len(pm.get("moves") or []) if (pm.get("captures") or 0) >= 2 or (pm.get("logged") or {}).get("with_baseline") else None, "n",
            "price moves of 15 percent or more: between the latest two captures, and logged prices against their own 30-day average",
            "needs 2 dated captures or 2 logged prices for one product"),
        row("new_creative_count", None, "n", "ads first seen this period", "needs 2 ad-level snapshots"),
        row("new_launch_count", None, "n", "new products or listings seen", "needs product feed captures"),
        row("positioning_openness_score", sum(1 for x in q["quadrants"] if not x["competitors"]) / 4 if q.get("openness") else None, "%",
            "open quadrants / 4 on the price by durability map", "fewer than 3 brands placed"),
        row("category_ladder_coverage", cat["coverage"], "n", "rungs with at least one member, of 5"),
        row("market_size_estimate", (n.get("bar") or {}).get("buyers"), "n", "buyers a year for 1 percent of revenue", "AOV, repeat rate or revenue missing"),
        row("addressable_niche_size", None, "n", "search demand for the niche x capture rate", "needs a keyword source"),
        row("win_rate_vs_named_competitor", (m.get("losses") or {}).get("win_rate"), "%",
            f"wins / (wins + losses) in win-loss interviews against {(m.get('losses') or {}).get('win_rate_name') or 'the top name'}",
            (m.get("losses") or {}).get("win_rate_reason") or "no interviews on file"),
        row("battlecard_freshness_days", max(ages) if ages else None, "days", "days since the oldest card's facts were checked", "no cards"),
        row("competitor_activity_share", us_share, "%", "our active ads / all active ads on direct pages plus ours", "our active ads unknown"),
        row("premium_signal_score", pr.get("our_score"), "%", "premium signals present / signals known", "no signals read"),
        row("discount_depth_vs_category", (pr["our_depth"] - pr["direct_median_depth"]) if pr.get("our_depth") is not None
            and pr.get("direct_median_depth") is not None else None, "points", "our deepest discount minus the direct median", "offers not read"),
        row("positioning_test_score", m["frames"].get("score"), "points", "share preferring the new line minus the current", "no test on file"),
    ]


def review(m: dict, pos: dict, fr: dict, today: dt.date) -> dict:
    """The quarterly positioning review: where we sit, who moved, how shoppers frame us, and 3 decisions for the founder."""
    name = m["brand"].capitalize()
    q = (today.month - 1) // 3 + 1
    dur = next((mv for mv in pos["kit"]["durability"]["moves"] if mv["kind"] == "hold"), None)
    com = next((mv for mv in pos["kit"]["comfort"]["moves"] if mv["kind"] == "hold"), None)
    threats = [p["name"] for p in m["pages"] if (p.get("verdict") or {}).get("text") == "Threat"]
    top = fr.get("top") or {}
    lad = m.get("ladder") or {}
    decisions = []
    if top and not top.get("in_our_frame"):
        decisions.append(f"Test a line for the {top['label']} frame ({top['mentions']} mentions), or keep ours: {fr.get('our_frame')}.")
    contest = next((mv for mv in pos["kit"]["durability"]["moves"] + pos["kit"]["comfort"]["moves"] if mv["kind"] == "contest"), None)
    if contest:
        decisions.append(f"Contest the {contest['label']} corner, or hold our own. {contest['text']}")
    if m["price_position_index"] is not None:
        decisions.append(f"Hold our price index at {m['price_position_index']} (100 is the tracked median), or move toward the band "
                         f"{audit.PRICE_BAND[0]} to {audit.PRICE_BAND[1]}.")
    lines = [f"Positioning review, Q{q} {today.year}, {name}. Simulated sales, public signals.", "",
             "Where we sit: " + "; ".join(x["label"] for x in (dur, com) if x) + ".",
             f"Threats: {', '.join(threats) or 'none'}.",
             f"How shoppers frame the category: {top.get('label', 'unavailable')} first; our line says it: {'yes' if top.get('in_our_frame') else 'no'}.",
             f"Pack ladder saves {round(lad['median_saving'] * 100)} percent a unit; price index {m['price_position_index']}." if lad.get("median_saving") is not None else "Price: unavailable.",
             "", "Decisions for the founder:"] + [f"{i + 1}. {d}" for i, d in enumerate(decisions)] + ["", "Next review in 90 days, or sooner if a threat's points rise."]
    return {"quarter": f"Q{q} {today.year}", "text": "\n".join(lines), "decisions": decisions}


def overview(brand: str, today: dt.date) -> dict:
    m = audit.market_full(brand, today, BRAIN_ROOT)
    brain = m.pop("brain")
    name = brand.capitalize()
    pos = positioning(m)
    window = actions.ranker.default_window(28, (today - dt.timedelta(days=1)).isoformat())
    ranked = actions.build(brand, window, BRAIN_ROOT)["actions"]
    moves = pos["kit"]["durability"]["moves"] + pos["kit"]["comfort"]["moves"]
    return {"brand": brand, "today": today.isoformat(), "version": brain.version(),
            "simulated_note": SIMULATED_NOTE.format(name=name, unit=m["term"]["unit"]), "term": m["term"], "signal_note": SIGNAL_NOTE,
            "competitors": [_public(c) for c in m["competitors"]], "angles": m["angles"],
            "positioning": pos,
            "lookalike": m["lookalike"], "gap": gaps(m), "pages": (pr := page_rows(m)), "battlecards": (bc := battlecards(m, pr)),
            "room_metrics": room_metrics(m, pos, bc),
            "coverage": {"all": m["coverage"], "direct": m["coverage_direct"]}, "mix": m["mix"], "references": m["references"], "ladder": m["ladder"], "changes": m["changes"], "freshness": freshness(m, brand), "losses": m["losses"], "category": m["category"], "reviews": m["reviews"], "presence": m["presence"], "velocity": m["velocity"], "niche": m["niche"], "premium": m["premium"], "search": m["search"], "price_moves": m["price_moves"], "landing": m["landing"], "placements": placements(m), "season": m["season"],
            "review": review(m, pos, audit.framemod.build(m, brain, moves), today), "macros": macros(m), "history": audit.capmod.history(brand), "gap_lines": gap_lines(ranked),
            "frames": audit.framemod.build(m, brain, moves),
            "category_median": m["category_median"], "price_position_index": m["price_position_index"]}


NOTES = HERE / "fixtures" / "notes"
NOTE_MAX, NOTES_MAX = 500, 2000
SAFE_ENTITY = re.compile(r"^[a-z0-9_.-]{1,80}$")


def notes_path(brand: str) -> Path:
    return NOTES / f"{brand}.json"


def read_notes(brand: str, entity: str | None = None) -> list[dict]:
    try:
        rows = json.loads(notes_path(brand).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        rows = []
    return [r for r in rows if entity is None or r.get("entity") == entity]


def add_note(brand: str, body) -> tuple[int, dict]:
    """A team note on an entity (a page key or an action id). Local file, git-ignored; never sent anywhere."""
    if not isinstance(body, dict):
        return 400, {"error": "body must be an object"}
    entity, text = str(body.get("entity") or ""), str(body.get("text") or "").strip()
    if not SAFE_ENTITY.match(entity) or not text:
        return 400, {"error": "entity (a page key or action id) and text are required"}
    rows = read_notes(brand)
    if len(rows) >= NOTES_MAX:
        return 400, {"error": "notes file is full"}
    row = {"entity": entity, "text": text[:NOTE_MAX].replace("\u2014", ","), "by": str(body.get("by") or "team")[:40],
           "time": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
    rows.append(row)
    notes_path(brand).parent.mkdir(parents=True, exist_ok=True)
    notes_path(brand).write_text(json.dumps(rows, indent=1), encoding="utf-8")
    return 201, {"ok": True, "note": row}


def run_capture(brand: str, today: dt.date) -> tuple[int, dict]:
    """The weekly watch, run by the agent from the page: today's page-summary capture from the brain and the
    competitor_snapshot hand-off. Reads only the brain; nothing external, nothing paid. Once a day."""
    cap = audit.capmod
    if (cap.FOLDER / brand / f"{today.isoformat()}.json").exists():
        return 200, {"ok": True, "already": True, "captured_at": today.isoformat(), "captures": len(cap.captures(brand))}
    m = audit.market_full(brand, today, BRAIN_ROOT)
    cap.write(brand, m["pages"], today)
    audit.handmod.write_snapshot(m, audit.parse_band)
    prev, cur = cap.latest_two(brand)
    return 201, {"ok": True, "already": False, "captured_at": today.isoformat(), "captures": len(cap.captures(brand)),
                 "pages": len(cur["pages"]) if cur else 0, "changes": len(cap.diff(prev, cur)),
                 "since": prev["captured_at"] if prev else None}


KIND_TEAM = {"ad_brief": "creative", "copy": "copy", "test_brief": "growth", "offer": "offers", "page_section": "site",
             "listing_fix": "marketplaces", "ticket": "support", "research_note": "research", "brain_record": "brand brain",
             "connector_setup": "setup", "report": "founder"}


def brief_pack(brand: str, today: dt.date) -> dict:
    """Every drafted artefact on the plan, grouped by the team that ships it, as one text per team."""
    window = actions.ranker.default_window(28, (today - dt.timedelta(days=1)).isoformat())
    acts = actions.ranker.apply_decisions(actions.build(brand, window, BRAIN_ROOT)["actions"], today)
    teams: dict[str, list[dict]] = {}
    for a in acts:
        if a.get("status") == "unavailable":
            continue
        teams.setdefault(KIND_TEAM.get(a["artefact"]["kind"], "other"), []).append(a)
    out = []
    for team, xs in sorted(teams.items()):
        parts = []
        for i, a in enumerate(xs, 1):
            parts += [f"{i}. {a['title']}", f"   Why: {a['why']}", f"   Check on: {a.get('check_on') or 'unavailable'}"
                      + (f"; stop if: {a['stop_rule']}" if a.get("stop_rule") else "")]
            if a["artefact"].get("draft"):
                parts += ["   " + ln for ln in a["artefact"]["draft"].split("\n")]
            parts.append("")
        out.append({"team": team, "n": len(xs), "drafted": sum(1 for a in xs if a["artefact"].get("draft")),
                    "text": f"Brief pack for the {team} team, {brand.capitalize()}, {today.isoformat()}.\n\n" + "\n".join(parts).rstrip()})
    rows = [{"id": a["id"], "brand": brand, "from_screen": audit.SCREEN, "team": KIND_TEAM.get(a["artefact"]["kind"], "other"),
             "kind": a["artefact"]["kind"], "title": a["title"], "why": a["why"], "draft": a["artefact"].get("draft"),
             "win_rule": a.get("win_rule"), "stop_rule": a.get("stop_rule"), "check_on": a.get("check_on"),
             "capability": a["capability"]["id"], "autonomy": a["capability"]["autonomy"], "owner": a["owner"],
             "status": "decided" if a.get("decision") else "proposed", "created": today.isoformat()}
            for a in acts if a.get("status") != "unavailable"]
    return {"teams": out, "total": sum(t["n"] for t in out), "drafted": sum(t["drafted"] for t in out), "rows": rows,
            "fields": list(rows[0]) if rows else [], "note": "Proposed shape for a shared briefs table; see Contract asks."}


def handle(req):
    try:
        brand, today = _brand(req), _today(req)
    except ValueError as exc:
        return 400, {"error": str(exc)}
    try:
        if req.method == "GET" and req.path == ["overview"]:
            return overview(brand, today)
        if req.path == ["notes"]:
            if req.method == "POST":
                return add_note(brand, req.body)
            return {"notes": read_notes(brand, req.arg("entity"))}
        if req.method == "POST" and req.path == ["inputs", "remove"]:
            return audit.inpmod.remove(brand, str((req.body or {}).get("id") or "") if isinstance(req.body, dict) else "")
        if req.path == ["inputs"]:
            if req.method == "POST":
                body = req.body if isinstance(req.body, dict) else {}
                m = audit.market_full(brand, today, BRAIN_ROOT)
                return audit.inpmod.add(brand, str(body.get("kind") or ""), body, {"competitors": m["losses"]["names"],
                                        "pages": [p["name"] for p in m["pages"] if p["role"] != "self"],
                                        "tunable": audit.TUNE_RANGE,
                                        "actions": [a["id"] for a in actions.build(brand, actions.ranker.default_window(28, (today - dt.timedelta(days=1)).isoformat()), BRAIN_ROOT)["actions"]]
                                        if str(body.get("kind")) == "outcome" else [],
                                        "lines": [x["key"] for x in m["frames"]["lines"] if x["key"] != "A"],
                                        "direct": [p["name"] for p in m["pages"] if p["role"] != "self" and p["frame"] == "direct" and p["source"] != "none"]}, today)
            recs = sorted(audit.inpmod.read(brand, req.arg("kind")), key=lambda r: (r.get("logged_at", ""), r["id"]), reverse=True)
            return {"records": [dict(r, summary=audit.inpmod.summary(r)) for r in recs], "reason_codes": audit.inpmod.REASON_CODES,
                    "note": "Logged by the team on this screen. Local file, never sent anywhere. No names or quotes kept."}
        if req.method == "POST" and req.path == ["capture"]:
            return run_capture(brand, today)
        if req.method == "GET" and req.path == ["briefs"]:
            return brief_pack(brand, today)
        if req.method == "GET" and req.path == ["competitor_snapshot"]:
            m = audit.market_full(brand, today, BRAIN_ROOT)
            return {"table": "competitor_snapshot", "brand": brand, "fields": audit.handmod.FIELDS,
                    "rows": audit.handmod.snapshot_rows(m, audit.parse_band)}
        if req.method == "GET" and req.path == ["experiments"]:
            window = actions.ranker.default_window(28, (today - dt.timedelta(days=1)).isoformat())
            acts = actions.build(brand, window, BRAIN_ROOT)["actions"]
            return {"brand": brand, "rows": audit.handmod.experiment_rows(acts, brand),
                    "note": "Drafts in the registry shape; 25-experiments assigns ids and owns results."}
        if req.method == "GET" and req.path == ["digest"]:
            return digest(brand, today)
        if req.method == "GET" and req.path == ["plan"]:
            return plan(brand, today)
        if req.method == "GET" and req.path == ["audit"]:
            ends = (today - dt.timedelta(days=1)).isoformat()
            findings = audit.run(brand, {"ends_on": ends, "days": 1, "trailing": 0}, BRAIN_ROOT)
            return {"findings": findings, "rules": audit.RULES}
    except FileNotFoundError as exc:
        return 404, {"error": str(exc)}
    return 404, {"error": "not found", "path": req.path}
