"""Creative velocity and share of voice: how fast each page ships new ads, and its share of the ads live.

Launch rate per week, estimated by Little's law on a steady account: new ads a week = active ads / days
an ad stays live x 7. The median days live stands in for the mean, so it is an estimate and says so.
With two ad-level snapshots it is counted instead: ads first seen in the window / weeks.
Our own count for the month (learnings.september_flight) is shown beside our estimate as a check.
Share of voice: a page's active ads over all active ads on the direct pages plus ours. Ad counts are not
spend; share of voice here is a signal of how much a page tests, never of how much it spends.

Rule COMP-R19: our launch rate is under SLOW_SHARE (half) of the direct pages' median launch rate. Answer:
a weekly creative volume plan fed by the coverage gaps and the hook bank (CREA-C06).
"""
from __future__ import annotations

import datetime as dt
import statistics

SLOW_SHARE = 0.5


def launch_rate(active, median_days):
    if not isinstance(active, int) or not isinstance(median_days, (int, float)) or median_days <= 0:
        return None
    return round(active / max(median_days, 1) * 7, 1)


def build(m: dict, brain) -> dict:
    rows = []
    for p in m["pages"]:
        if p["source"] == "none":
            continue
        rows.append({"name": p["name"], "role": p["role"], "frame": p["frame"], "active_ads": p["active_ads"],
                     "median_days": p["median_days"], "rate": launch_rate(p["active_ads"], p["median_days"]),
                     "counted": p.get("new_14d") / 2 if isinstance(p.get("new_14d"), int) else None})
    direct = [r for r in rows if r["frame"] == "direct"]
    us = next((r for r in rows if r["role"] == "self"), None)
    pool = [r["active_ads"] for r in direct + ([us] if us else []) if isinstance(r["active_ads"], int)]
    total = sum(pool) if pool else None
    for r in rows:
        r["share"] = round(r["active_ads"] / total, 3) if total and isinstance(r["active_ads"], int) and (r in direct or r is us) else None
    rates = [r["rate"] for r in direct if r["rate"] is not None]
    med = round(statistics.median(rates), 1) if rates else None
    sep = (brain.get(f"{brain.brand}.learnings.september_flight") or {}).get("value") or {}
    counted_month = sep.get("started_since_2026_09_01") if isinstance(sep.get("started_since_2026_09_01"), int) else None
    today = brain.today
    days_in = (today - dt.date(today.year, today.month, 1)).days or 1
    our_counted = round(counted_month / days_in * 7, 1) if counted_month is not None else None
    slow = bool(us and us["rate"] is not None and med and us["rate"] < med * SLOW_SHARE)
    rows.sort(key=lambda r: -(r["rate"] or -1))
    return {"rows": rows, "direct_median_rate": med, "our_rate": us["rate"] if us else None, "our_counted_rate": our_counted,
            "our_counted_note": f"{counted_month} new ads since the 1st of the month" if counted_month is not None else None,
            "slow": slow, "bar": round(med * SLOW_SHARE, 1) if med else None,
            # the next step is at most double what we ship now: a plan the team can keep, not the peers' pace
            "target": round(min(med * SLOW_SHARE, 2 * (our_counted or (us or {}).get("rate") or 0)), 1) if med and us else None,
            "rule": f"Launch rate = active ads / median days live x 7 (an estimate). Slow: under {int(SLOW_SHARE * 100)} percent of "
                    "the direct median. Share of voice counts ads, not spend."}


def now_rate(v: dict):
    """What we ship today: the counted rate when the brain has one, else the estimate."""
    return v["our_counted_rate"] if v.get("our_counted_rate") is not None else v.get("our_rate")


def draft(v: dict, gaps: list[str]) -> str:
    return "\n".join([f"Creative volume plan: {v['target']} new ads a week, double the {now_rate(v)} we ship now.",
                      f"Why: direct pages ship a median {v['direct_median_rate']} new ads a week (estimate from ad life). "
                      f"Our estimate on the same method: {v['our_rate']}.",
                      "Feed: " + ("; ".join(gaps[:4]) if gaps else "the coverage gaps and the hook bank") + ".",
                      "Each week: 2 new concepts, 3 new first lines on the best 2 ads, 1 new format. Kill anything 30 percent over "
                      "target cost per order after 7 days.",
                      "Budget stays flat: new ads take share from the oldest, weakest ads.",
                      "Never copy their text, logos, products or faces."])
