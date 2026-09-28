"""Longest running ads as signals: one reference per tracked page, plus our own long runners.

A page's longest running ad and the share of its ads live 30 days or more show what it keeps live.
That is a signal, never proof that the ad works. Each reference carries the reason it matters to this
brand, computed from rules over brain fields (app/contracts/inspiration.md): it runs one of our top
angles, its page keeps half or more of its ads live 30 days, it has run 3x our median ad or longer, it
is a direct competitor. Score is the capped sum of the rule weights; a reference under SHOW_MIN is listed
but not suggested. Rights are reference_only for competitors and own_brand for ours: shown for layout,
mood, format and cadence, never passed to a generation, copy or brief call as an asset.

"Use as reference" produces a brief that says what to borrow and what never to copy.
"""
from __future__ import annotations

STUDY_DAYS, WATCH_DAYS = 90, 30
SHOW_MIN = 0.3
WEIGHTS = {"angle": 0.4, "keeps": 0.3, "long": 0.2, "direct": 0.1}
KEEP_MIN = 0.5          # half or more of a page's ads live 30 days or more: it keeps what works
BORROW = ["layout: where the product, the proof and the text sit", "pacing of the first 3 seconds",
          "mood: light, colour and setting"]
NEVER = ["their text or claims", "logos", "products", "faces"]


def _dominant(formats: dict, labels: dict) -> str | None:
    if not formats:
        return None
    k = max(formats.items(), key=lambda kv: (kv[1], kv[0]))[0]
    return labels.get(k, k).lower()


def build(pages: list[dict], top_angles: list[str], labels: dict, proof_for) -> dict:
    us = next(p for p in pages if p["role"] == "self")
    our_median = us.get("median_days")
    refs = []
    for p in pages:
        if p["role"] == "self" or p.get("longest_days") is None:
            continue
        days = p["longest_days"]
        reasons, score = [], 0.0
        shared = [a for a in p["angles"] if a["tag"] in top_angles]
        if shared:
            score += WEIGHTS["angle"]
            reasons.append(f"Runs one of our top angles: {shared[0]['label'].lower()} (\"{shared[0]['word']}\" in the {shared[0]['where']})")
        n = p.get("sample_ads")
        keep = round(p["long_runners_30d"] / n, 3) if isinstance(p.get("long_runners_30d"), int) and n else None
        if keep is not None and keep >= KEEP_MIN:
            score += WEIGHTS["keeps"]
            reasons.append(f"Keeps {round(keep * 100)} percent of its ads live 30 days or more")
        if isinstance(our_median, (int, float)) and our_median and days >= 3 * our_median:
            score += WEIGHTS["long"]
            reasons.append(f"Live {days} days, {round(days / our_median)}x our median ad")
        if p["frame"] == "direct":
            score += WEIGHTS["direct"]
            reasons.append("Direct competitor")
        kind, text = (("scale", "Study") if days >= STUDY_DAYS else ("watch", "Watch") if days >= WATCH_DAYS else ("na", "Too new"))
        angle = shared[0]["tag"] if shared else (top_angles[0] if top_angles else None)
        ref = {"key": p["key"], "page": p["name"], "frame": p["frame"], "days": days, "start": p.get("longest_start"),
               "url": p.get("longest_url") or p.get("ad_library_url"), "exact_ad": bool(p.get("longest_url")),
               "page_format": _dominant(p["formats"], labels), "keep_rate": keep, "long_runners": p.get("long_runners_30d"),
               "median_days": p.get("median_days"), "versions": None, "score": round(min(score, 1.0), 2),
               "reasons": reasons, "verdict": {"kind": kind, "text": text}, "rights": "reference_only",
               "suggested": score >= SHOW_MIN and days >= WATCH_DAYS}
        ref["brief"] = brief(ref, angle, proof_for(angle) if angle else None, labels)
        refs.append(ref)
    refs.sort(key=lambda r: (-r["score"], -r["days"], r["page"]))
    ours = [{"page": us["name"], "days": x.get("days_running"), "start": x.get("start_date"), "url": x.get("ad_url"),
             "format": x.get("format"), "hook": x.get("hook"), "rights": "own_brand"} for x in us.get("long_ads") or []]
    return {"refs": refs, "ours": ours, "our_median": our_median, "study_days": STUDY_DAYS, "watch_days": WATCH_DAYS,
            "rule": f"Study at {STUDY_DAYS} days or more, watch at {WATCH_DAYS} to {STUDY_DAYS - 1}. Relevance: top angle "
                    f"{WEIGHTS['angle']}, keeps {round(KEEP_MIN * 100)} percent of ads 30 days {WEIGHTS['keeps']}, 3x our median {WEIGHTS['long']}, direct "
                    f"{WEIGHTS['direct']}; suggested at {SHOW_MIN} or more."}


def brief(ref: dict, angle: str | None, proof: str | None, labels: dict) -> str:
    since = f" since {ref['start']}" if ref.get("start") else ""
    lines = [f"Reference brief: {ref['page']}'s longest running ad, live {ref['days']} days{since}.",
             f"Open it: {ref['url'] or 'no link in the capture'}" + ("" if ref["exact_ad"] else " (page view; the exact ad is not in the capture)") + ".",
             "Borrow: " + "; ".join(BORROW) + ".",
             f"Map it to our angle: {angle or 'unavailable'}" + (f", with our proof: {proof}." if proof else ". No proof in the brain yet."),
             "Never copy: " + ", ".join(NEVER) + ".",
             "Rights: reference only. It is never passed to a generation, copy or brief call as an asset.",
             "Why this one: " + ("; ".join(ref["reasons"]) if ref["reasons"] else "no relevance rule fired") + "."]
    return "\n".join(lines)
