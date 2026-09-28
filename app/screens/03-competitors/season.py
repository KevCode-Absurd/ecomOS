"""The holiday season against the rivals: a dated plan by phase, computed from the calendar, and the gifting gap.

US dates in code (app/CLAUDE.md: US holidays by default): Black Friday is the day after the fourth Thursday of
November, Cyber Monday 3 days later, the last gift-shipping day SHIP_CUTOFF (7) days before 24 December.
The season's weight comes from the brain (economics.monthly_revenue_shape nov_dec_share_pct); missing reads
unavailable. Phases: watch, build, defend, gift window, read; each with dates, owner, the moves and the artefact.

Rule COMP-R30: Black Friday is within LEAD_DAYS (60) days, 2 or more direct pages run a gifting or season angle,
and none of our ads does. Answer: a gifting ad brief with our gifting offer from the brain (CREA-C06).
"""
from __future__ import annotations

import datetime as dt

SHIP_CUTOFF, LEAD_DAYS = 7, 60


def black_friday(year: int) -> dt.date:
    d = dt.date(year, 11, 1)
    first_thu = d + dt.timedelta(days=(3 - d.weekday()) % 7)
    return first_thu + dt.timedelta(days=21 + 1)


def build(m: dict, brain, today: dt.date) -> dict:
    bf = black_friday(today.year)
    if bf + dt.timedelta(days=30) < today:
        bf = black_friday(today.year + 1)
    cm = bf + dt.timedelta(days=3)
    xmas = dt.date(bf.year, 12, 24)
    cutoff = xmas - dt.timedelta(days=SHIP_CUTOFF)
    shape = (brain.get(f"{brain.brand}.economics.monthly_revenue_shape") or {}).get("value") or {}
    share = shape.get("nov_dec_share_pct") if isinstance(shape, dict) else None
    gifting = (brain.get(f"{brain.brand}.offers.gifting") or {}).get("value")
    us = next(p for p in m["pages"] if p["role"] == "self")
    ours = (us.get("angle_counts") or {}).get("gifting")
    direct = [p["name"] for p in m["pages"] if p["frame"] == "direct" and any(a["tag"] == "gifting" for a in p["angles"])]
    d = lambda x: x.isoformat()  # noqa: E731
    phases = [
        {"phase": "Watch", "from": d(today), "to": d(bf - dt.timedelta(days=36)), "owner": "agent",
         "moves": "Weekly captures of the direct pages; note who starts gifting and bundle offers.", "artefact": "research_note"},
        {"phase": "Build", "from": d(bf - dt.timedelta(days=35)), "to": d(bf - dt.timedelta(days=8)), "owner": "agent_drafts",
         "moves": "3 gifting ads and a gift guide block from our gifting offer; refresh the battlecards.", "artefact": "ad_brief"},
        {"phase": "Defend", "from": d(bf - dt.timedelta(days=7)), "to": d(cm), "owner": "agent",
         "moves": "Daily capture of the top 3 threats' offers; answer a price cut with value, never a reflex match.", "artefact": "copy"},
        {"phase": "Gift window", "from": d(cm + dt.timedelta(days=1)), "to": d(cutoff), "owner": "agent_drafts",
         "moves": f"Say the last day to order for gifts ({d(cutoff)}) in ads and on the page; gift cards after it.", "artefact": "copy"},
        {"phase": "Read", "from": d(xmas + dt.timedelta(days=2)), "to": d(xmas + dt.timedelta(days=16)), "owner": "agent",
         "moves": "What rivals ran and what we ran; write the learnings to the brain.", "artefact": "report"},
    ]
    days_to_bf = (bf - today).days
    fires = 0 <= days_to_bf <= LEAD_DAYS and len(direct) >= 2 and not ours
    return {"black_friday": d(bf), "cyber_monday": d(cm), "ship_cutoff": d(cutoff), "days_to_black_friday": days_to_bf,
            "season_share_pct": share, "gifting_offer": gifting, "our_gifting_ads": ours, "direct_gifting": direct,
            "phases": phases, "fires": fires,
            "rule": f"Gap: Black Friday within {LEAD_DAYS} days, 2 or more direct pages run a gifting or season angle, none of our ads does. "
                    f"Last gift-shipping day is {SHIP_CUTOFF} days before 24 December."}


def draft(s: dict, brand: str) -> str:
    return "\n".join([f"Gifting ad brief for {brand}, season starting {s['black_friday']}.",
                      f"Why: {', '.join(s['direct_gifting'])} run a gifting or season angle; we run it in 0 ads. "
                      + (f"Nov and Dec are {s['season_share_pct']} percent of our year." if s["season_share_pct"] is not None else ""),
                      f"Offer to feature: {s['gifting_offer'] or 'none in the brain; add one first'}.",
                      "3 ads: a gift box static, a video with the unboxing and the proof, a carousel gift guide by person.",
                      f"Last day to order for gifts: {s['ship_cutoff']}. Gift cards after it.",
                      "Never copy their text, logos, products or faces."])
