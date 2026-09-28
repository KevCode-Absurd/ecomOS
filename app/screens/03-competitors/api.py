"""Competitors and market screen API: /api/03-competitors/...

Reads the brand brain through app/brain/store.py (the competitors section and
the raw Ad Library records as fallback) and the simulated products_monthly
table through app/data/tables.py. The market model and the audit rules live
in audit.py; this file shapes them for the page. No writes, nothing external.

  GET  overview   tiles, 2 insights, chart, competitor cards, positioning map,
                  price ladder, what they run board, lookalike warning, actions
  GET  audit      findings from audit.py (app/contracts/audit.md shape)

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

_spec = importlib.util.spec_from_file_location("competitors_audit", HERE / "audit.py")
audit = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(audit)

ACTIONS = [
    {"label": "Rebuild the positioning map", "capability": "BRAND-C19", "autonomy": "agent_does"},
    {"label": "Search for an unclaimed angle", "capability": "BRAND-C21", "autonomy": "founder_gate"},
    {"label": "Audit pricing position now", "capability": "BRAND-C24", "autonomy": "founder_gate"},
    {"label": "Refresh competitor watch now", "capability": "BRN-C11", "autonomy": "agent_does"},
]
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


def tiles(m: dict) -> list[dict]:
    comps = m["competitors"]
    idx = m["price_position_index"]
    lo, hi = audit.PRICE_BAND
    ads = [c["active_ads"] for c in comps if isinstance(c["active_ads"], int)]
    return [
        {"name": "Competitors tracked", "plain": "Named brands on watch from the Ad Library", "value": len(comps),
         "unit": "n", "window": "latest capture"},
        {"name": "Price position", "plain": f"Price per pair vs the tracked median, x 100. Range {lo} to {hi}.",
         "value": idx, "unit": "index", "window": "latest capture, simulated brand price",
         "tone": None if idx is None else ("bad" if not lo <= idx <= hi else "good"),
         "unavailable_reason": m["packs"].get("reason") if idx is None else None},
        {"name": "Competitor active ads", "plain": f"Sum across tracked brands. {m['brand'].capitalize()} runs "
         f"{m['profile']['active_ads'] if m['profile']['active_ads'] is not None else 'an unknown number of'}.",
         "value": sum(ads) if ads else None, "unit": "n", "window": "latest capture, public signal"},
    ]


def insights(m: dict) -> list[dict]:
    """Two rules: a competitor runs the same offer type longer, and the price per pair sits outside the band."""
    out = []
    name = m["brand"].capitalize()
    for o in m["offer_runs"]:
        longer = [c for c in o["competitors"] if c["days"] > o["brand_days"]]
        if not longer:
            continue
        top = longer[0]
        tail = (f"{name} has run its {o['label']} in ads for {o['brand_days']} days." if o["brand_ads"]
                else f"{name} has a {o['label']} but runs it in 0 of {o['brand_active_ads']} active ads.")
        out.append({"rule": "competitor longest ad days > brand days running the same offer type",
                     "severity": "medium", "capability": "BRAND-C24", "autonomy": "founder_gate",
                     "sentence": f"{top['name']} runs a {o['label']} hook and keeps its longest ad live "
                                 f"{top['days']} days. {tail}",
                     "evidence": f"{len(o['competitors'])} tracked brands show a {o['label']} hook: " +
                                 ", ".join(f"{c['name']} {c['days']} days" for c in o["competitors"]) +
                                 ". Run length is a signal, not a result."})
        break
    idx = m["price_position_index"]
    lo, hi = audit.PRICE_BAND
    if idx is not None and not lo <= idx <= hi:
        p, med = m["packs"]["median_per_pair"], m["category_median"]
        gap = gaps(m)
        out.append({"rule": f"price_position_index outside {lo} to {hi}, one capture", "severity": "medium",
                    "capability": "BRAND-C24", "autonomy": "founder_gate",
                    "sentence": f"{name} sells socks for ${p:.2f} a pair after discounts. The tracked median is "
                                f"${med:.2f}, so {name} sits {round(abs(100 - idx))} percent "
                                f"{'below' if idx < lo else 'above'} the category.",
                    "evidence": (f"Widest empty price band: ${gap['from']:.2f} to ${gap['to']:.2f} a pair, "
                                 f"between {gap['below']} and {gap['above']}. " if gap else "") +
                                f"Brand price is simulated ({m['packs']['month']}). One capture."})
    return out


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


def chart(m: dict) -> dict:
    comps = sorted(m["competitors"], key=lambda c: (-(c["active_ads"] or 0), c["name"]))
    return {"labels": [c["name"] for c in comps] + [m["brand"].capitalize()],
            "values": [c["active_ads"] for c in comps] + [m["profile"]["active_ads"]],
            "brand_index": len(comps)}


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


def overview(brand: str, today: dt.date) -> dict:
    m = audit.market(brand, today, BRAIN_ROOT)
    brain = m.pop("brain")
    name = brand.capitalize()
    return {"brand": brand, "today": today.isoformat(), "version": brain.version(),
            "simulated_note": SIMULATED_NOTE.format(name=name), "signal_note": SIGNAL_NOTE,
            "tiles": tiles(m), "insights": insights(m), "chart": chart(m),
            "competitors": [_public(c) for c in m["competitors"]], "angles": m["angles"],
            "positioning": positioning(m), "prices": price_table(m), "board": board(m),
            "lookalike": m["lookalike"], "actions": ACTIONS,
            "category_median": m["category_median"], "price_position_index": m["price_position_index"]}


def handle(req):
    try:
        brand, today = _brand(req), _today(req)
    except ValueError as exc:
        return 400, {"error": str(exc)}
    try:
        if req.method == "GET" and req.path == ["overview"]:
            return overview(brand, today)
        if req.method == "GET" and req.path == ["audit"]:
            ends = (today - dt.timedelta(days=1)).isoformat()
            findings = audit.run(brand, {"ends_on": ends, "days": 1, "trailing": 0}, BRAIN_ROOT)
            return {"findings": findings, "rules": audit.RULES}
    except FileNotFoundError as exc:
        return 404, {"error": str(exc)}
    return 404, {"error": "not found", "path": req.path}
