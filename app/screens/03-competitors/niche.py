"""Is a niche big enough to matter at our numbers? The bar in buyers, from the brand's own economics, and the
candidate niches this screen found, each with the signal we have and the demand we still need.

The bar (BRAND-C23): a niche matters when it can add MATTER_SHARE (1 percent) of trailing 12-month revenue.
  buyers a year = revenue x MATTER_SHARE / (AOV x orders per buyer a year)
  orders per buyer a year = 1 + repeat rate (a floor: repeat buyers often order more than twice)
  contribution = that revenue x contribution margin
Inputs from the brain (economics.aov_usd, repeat_rate_12m, contribution_margin_model) and the aggregates
(revenue); a missing input makes the bar unavailable, never 0.

Candidates: angles the tracked pages put CANDIDATE_MIN (5 percent) or more of their ads on (coverage.py,
summed over formats), where our share is under a third of theirs. Signal: pages serving it and their share
of ads. Demand (search volume for the niche) needs a keyword source and reads unavailable.
Rule COMP-R20: the biggest candidate becomes a sizing note with the bar to beat (BRAND-C23, agent).
"""
from __future__ import annotations

import json
from pathlib import Path

MATTER_SHARE, CANDIDATE_MIN, UNDER = 0.01, 0.05, 1 / 3
AGG = Path(__file__).resolve().parents[2] / "data" / "brands"


def revenue_12m(brand: str) -> float | None:
    p = AGG / brand / "aggregates" / "calibration.json"
    try:
        rows = json.loads(p.read_text(encoding="utf-8"))["rows"]
        return float(rows["revenue_last_12m"]["total"])
    except (OSError, ValueError, KeyError, TypeError):
        return None


def build(m: dict, brain) -> dict:
    get = lambda k: (brain.get(f"{brain.brand}.{k}") or {}).get("value")  # noqa: E731
    aov, repeat = get("economics.aov_usd"), get("economics.repeat_rate_12m")
    cm = (get("economics.contribution_margin_model") or {}).get("contribution_margin_pct")
    rev = revenue_12m(m["brand"])
    bar = None
    if all(isinstance(x, (int, float)) for x in (aov, repeat, rev)) and aov:
        target = rev * MATTER_SHARE
        opb = 1 + repeat
        bar = {"revenue": round(target), "buyers": round(target / (aov * opb)), "aov": aov, "orders_per_buyer": round(opb, 2),
               "contribution": round(target * cm / 100) if isinstance(cm, (int, float)) else None, "revenue_12m": round(rev),
               "share": MATTER_SHARE}
    cov = m["coverage"]
    cands = []
    for row in cov["rows"]:
        cells = cov["cells"][row["key"]]
        them = sum(c["them"] or 0 for c in cells.values())
        us = sum(c["us"] or 0 for c in cells.values())
        pages = sorted({p for c in cells.values() for p in c["pages"]})
        if them >= CANDIDATE_MIN and us < them * UNDER:
            cands.append({"angle": row["key"], "label": row["label"], "their_share": round(them, 3), "our_share": round(us, 3),
                          "pages": pages, "demand": None})
    cands.sort(key=lambda c: (-c["their_share"], c["angle"]))
    return {"bar": bar, "candidates": cands, "demand_reason": "search demand per niche needs a keyword source; not connected",
            "rule": f"A niche matters when it can add {int(MATTER_SHARE * 100)} percent of 12-month revenue. Candidates: angles with "
                    f"{int(CANDIDATE_MIN * 100)} percent or more of their ads where our share is under a third of theirs."}


def draft(c: dict, bar: dict | None, brand: str) -> str:
    b = (f"The bar: {bar['buyers']:,} buyers a year (${bar['revenue']:,} at ${bar['aov']} and {bar['orders_per_buyer']} orders each), "
         f"about ${bar['contribution']:,} contribution." if bar and bar.get("contribution") is not None else "The bar: unavailable.")
    return "\n".join([f"Sizing note: is '{c['label'].lower()}' big enough for {brand}?", b,
                      f"Signal: {len(c['pages'])} tracked pages put {round(c['their_share'] * 100)} percent of their ads here; we put "
                      f"{round(c['our_share'] * 100)} percent.",
                      "Find: search demand for the niche's terms, the share of our reviews that mention it, and Reddit threads.",
                      "Answer in 3 lines: over or under the bar, the evidence, and the first test if over."])
