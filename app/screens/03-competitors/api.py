"""Competitors and market screen API: /api/03-competitors/...

Reads the brand brain through app/brain/store.py (the competitors section and
the raw Ad Library records as fallback) and the simulated products_monthly
table through app/data/tables.py. The market model and the audit rules live
in audit.py; this file shapes them for the page. No writes, nothing external.

  GET  plan       the plan board: ranked actions (actions.py) with decisions
                  applied, connect actions, orientation numbers, findings, rules
  GET  overview   the desk: competitor cards, positioning map, price ladder,
                  what they run board, lookalike record, widest price gap
  GET  audit      findings from audit.py (app/contracts/audit.md shape)
  rank(brand, window)  the depth contract override app/rank.py calls

Query `brand` (default bombas) and `today` (YYYY-MM-DD, default the real date)
work on every route. Set BRAIN_ROOT to point at a copy of app/brain (tests do).
"""
from __future__ import annotations

import datetime as dt
import importlib.util
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
BRAIN_ROOT: Path | None = None
SAFE_BRAND = re.compile(r"^[a-z0-9_-]+$")
SIMULATED_NOTE = ("{name} is the sample brand. Its prices per pair come from simulated sales. "
                  "Competitor facts are public signals from the Meta Ad Library and public product feeds.")
SIGNAL_NOTE = ("Public signals only. Ad counts and run length show what a brand keeps live, not what works. "
               "Formats and hooks are for layout and mood. Never copy their text, logos, products or faces.")

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
    return {"points": pts, "split_x": split_x, "axes": AXES, "quadrants": quads}


def price_table(m: dict) -> dict:
    comps = [c for c in m["competitors"] if c["price"]["median"] is not None]
    rows = []
    for p in m["packs"]["packs"]:
        row = {"label": p["label"], "per_pack": p["per_pack"], "per_pair": p["per_pair"], "cells": {}}
        for c in comps:
            b = c["price"]
            if b["low"] is not None and p["per_pair"] < b["low"]:
                pos = "below"
            elif b["high"] is not None and p["per_pair"] > b["high"]:
                pos = "above"
            elif b["low"] is not None and b["high"] is not None:
                pos = "inside"
            else:
                pos = "below median" if p["per_pair"] < b["median"] else "above median"
            row["cells"][c["name"]] = {"diff": round(p["per_pair"] - b["median"], 2), "position": pos}
        rows.append(row)
    return {"month": m["packs"].get("month"), "available": m["packs"]["available"],
            "reason": m["packs"].get("reason"),
            "competitors": [{"name": c["name"], "band": c["price"]["text"], "low": c["price"]["low"],
                             "high": c["price"]["high"], "median": c["price"]["median"],
                             "rough": c["price"]["rough"], "ref": c["price_ref"]} for c in comps],
            "rows": rows}


def board(m: dict) -> list[dict]:
    out = [{"name": c["name"], "formats": c["formats"], "hooks": c["hooks"], "active_ads": c["active_ads"],
            "longest_days": c["longest_days"], "brand": False} for c in m["competitors"]]
    prof = m["profile"]
    out.append({"name": m["brand"].capitalize(), "brand": True,
                "formats": [f"{k} {v}" for k, v in prof["formats"].items()],
                "hooks": [f"{k} {v}" for k, v in sorted(prof["hooks"].items(), key=lambda kv: -kv[1])],
                "active_ads": prof["active_ads"], "longest_days": None})
    return out


def orientation(m: dict) -> list[dict]:
    """3 to 6 small numbers beside the plan: where the competitive position stands today."""
    comps = m["competitors"]
    ads = [c["active_ads"] for c in comps if isinstance(c["active_ads"], int)]
    ages = [c["age_days"] for c in comps if c["age_days"] is not None]
    lo, hi = audit.PRICE_BAND
    idx = m["price_position_index"]
    return [
        {"label": "competitor pages", "value": len(comps), "unit": "n", "title": "competitor pages tracked in the brain"},
        {"label": "our active ads", "value": m["profile"]["active_ads"], "unit": "n", "title": "latest Ad Library capture"},
        {"label": "theirs, median a page", "value": sorted(ads)[len(ads) // 2] if ads else None, "unit": "n",
         "title": "median active ads across tracked pages, public signal"},
        {"label": "snapshot age", "value": max(ages) if ages else None, "unit": "n", "suffix": " days",
         "title": "days since the oldest competitor capture"},
        {"label": "price index", "value": idx, "unit": "n", "tone": None if idx is None else ("bad" if not lo <= idx <= hi else "good"),
         "title": f"our price per pair / tracked median x 100, band {lo} to {hi}, simulated brand price"},
    ]


def rank(brand: str = "bombas", window: dict | None = None) -> dict:
    """The screen's ranked actions (depth.md section 5). app/rank.py and the server call this."""
    out = actions.build(brand, window, BRAIN_ROOT)
    out.pop("findings", None)
    return out


def plan(brand: str, today: dt.date) -> dict:
    """The plan board: ranked actions with decisions applied, the findings they close, and the orientation."""
    window = actions.ranker.default_window(28, (today - dt.timedelta(days=1)).isoformat())
    out = actions.build(brand, window, BRAIN_ROOT)
    acts = actions.ranker.apply_decisions(out["actions"], today)
    m = audit.market(brand, today, BRAIN_ROOT)
    return {"brand": brand, "window": window, "brain_version": out["brain_version"], "simulated": True,
            "orient": orientation(m), "actions": [a for a in acts if a.get("status") != "unavailable"],
            "connect": [a for a in acts if a.get("status") == "unavailable"],
            "snoozed": len(out["actions"]) - len(acts), "findings": out["findings"], "rules": audit.RULES}


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


def overview(brand: str, today: dt.date) -> dict:
    m = audit.market(brand, today, BRAIN_ROOT)
    brain = m.pop("brain")
    name = brand.capitalize()
    return {"brand": brand, "today": today.isoformat(), "version": brain.version(),
            "simulated_note": SIMULATED_NOTE.format(name=name), "signal_note": SIGNAL_NOTE,
            "competitors": [_public(c) for c in m["competitors"]], "angles": m["angles"],
            "positioning": positioning(m), "prices": price_table(m), "board": board(m),
            "lookalike": m["lookalike"], "gap": gaps(m), "pages": page_rows(m),
            "coverage": {"all": m["coverage"], "direct": m["coverage_direct"]}, "mix": m["mix"],
            "category_median": m["category_median"], "price_position_index": m["price_position_index"]}


def handle(req):
    try:
        brand, today = _brand(req), _today(req)
    except ValueError as exc:
        return 400, {"error": str(exc)}
    try:
        if req.method == "GET" and req.path == ["overview"]:
            return overview(brand, today)
        if req.method == "GET" and req.path == ["plan"]:
            return plan(brand, today)
        if req.method == "GET" and req.path == ["audit"]:
            ends = (today - dt.timedelta(days=1)).isoformat()
            findings = audit.run(brand, {"ends_on": ends, "days": 1, "trailing": 0}, BRAIN_ROOT)
            return {"findings": findings, "rules": audit.RULES}
    except FileNotFoundError as exc:
        return 404, {"error": str(exc)}
    return 404, {"error": "not found", "path": req.path}
