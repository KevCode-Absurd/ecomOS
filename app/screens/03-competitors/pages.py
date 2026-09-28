"""The tracked Ad Library pages, one row per page, us included: the model behind the side-by-side table,
the coverage matrix and the hook and offer mix.

Sources, best first:
1. An ad-level snapshot from snapshot.py (fixtures/snapshots/<brand>/<date>.json) when one exists:
   every number is computed from its ad rows.
2. The brain: `competitors` records (adlib_* page summaries from the Apify pull, the detailed
   per-brand records with positioning, price band, hook labels and the longest ad), the
   `learnings` adlib_*_formats records (median days live, long runners), `positioning.competitive_frame`
   (which pages are direct and which are basics or apparel) and the Reddit "recommended instead" counts.

A number the source cannot give is None and renders "unavailable": offer share, main call to action
and ads new in 14 days need ad-level rows. Angle tags come from snapshot.ANGLES rules over the page's
hook labels, positioning, push line and the quoted ads; each tag keeps the word that set it and where
the word was found. Run length is a signal, never proof that an ad works.
"""
from __future__ import annotations

import datetime as dt
import re
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent

FORMAT_KEYS = {"video": "video", "image": "image", "carousel": "carousel", "dco": "dynamic", "dynamic": "dynamic",
               "dpa": "catalog", "catalog": "catalog"}
FORMAT_ORDER = ["video", "image", "carousel", "dynamic", "catalog"]
LINE_KEYS = {"statement": "statement", "question": "question", "first_person": "first_person", "number": "number",
             "offer": "offer", "problem": "problem", "quote": "quote", "none": "none"}
NEW_DAYS = 14


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(s or "").lower()).strip("_")


def _norm_formats(d: dict | None) -> dict:
    out: dict[str, int] = {}
    for k, v in (d or {}).items():
        if isinstance(v, int):
            key = FORMAT_KEYS.get(str(k).lower(), "other")
            out[key] = out.get(key, 0) + v
    return out


def _mix(d: dict) -> dict:
    n = sum(d.values())
    return {k: round(v / n, 3) for k, v in d.items()} if n else {}


def _same(a: str, b: str) -> bool:
    """Page names match loosely: 'Darn Tough Vermont Socks' is 'Darn Tough Vermont' is 'Darn Tough'."""
    x, y = slug(a), slug(b)
    return bool(x and y) and (x == y or x.startswith(y) or y.startswith(x))


def tag_sources(sources: list[tuple[str, str]], angles) -> list[dict]:
    """Angle tags over (where, text) pairs. First hit per angle wins; the word and where it was found are kept."""
    out = []
    for key, label, words in angles:
        hit = None
        for where, text in sources:
            t = f" {str(text or '').lower()} "
            for w in words:
                if w in t:
                    hit = {"tag": key, "label": label, "word": w.strip(), "where": where}
                    break
            if hit:
                break
        if hit:
            out.append(hit)
    return out


def _snapshot_page(rows: list[dict], captured: str, snap) -> dict:
    s = snap.summarise(rows)
    cap = dt.date.fromisoformat(captured)
    new = sum(1 for r in rows if r["start"] and (cap - dt.date.fromisoformat(r["start"])).days < NEW_DAYS)
    return {"active_ads": s["active"], "sample_ads": s["ads"], "formats": _norm_formats(s["formats"]),
            "median_days": s["median_days"], "longest_days": s["longest_days"],
            "long_runners_30d": sum(1 for r in rows if (r["days_live"] or 0) >= 30),
            "offer_share": s["offer_share"], "main_cta": s["cta"], "new_14d": new,
            "first_lines": s["first_lines"], "offers_seen": sorted(s["offers"]),
            "angle_counts": s["angles"], "source": "snapshot"}


def build(brain, frame: dict | None, snap_mod, snapshot: dict | None, profile: dict) -> list[dict]:
    """All tracked pages plus the brand's own row (role self), in frame order."""
    recs = [r for r in brain.records("competitors") if isinstance(r.get("value"), dict)]
    adlib = [r for r in recs if r.get("field") == "competitor" and r["value"].get("page")]
    detail = [r for r in recs if r["value"].get("name") and r.get("field") not in ("competitor_set", "lookalike_page")]
    reddit = [r for r in recs if r["value"].get("recommended_instead") is not None]
    learn = {}
    for r in brain.records("learnings"):
        v = r.get("value")
        if isinstance(v, dict) and v.get("page") and v.get("signal_only"):
            learn[slug(v["page"])] = v
    frame = frame if isinstance(frame, dict) else {}
    names: list[tuple[str, str]] = [(n, "direct") for n in frame.get("direct") or []]
    names += [(n, "basics") for n in frame.get("basics_apparel") or []]
    if not names:  # no frame in the brain: every page with a record, direct by default
        seen = []
        for r in detail + adlib:
            n = r["value"].get("name") or r["value"].get("page")
            if not any(_same(n, s) for s in seen):
                seen.append(n)
        names = [(n, "direct") for n in seen]
    snap_rows = {}
    if snapshot:
        for r in snapshot.get("ads") or []:
            snap_rows.setdefault(r["page_id"], []).append(r)
    out = []
    for name, fr in names:
        d = next((r for r in detail if _same(r["value"]["name"], name)), None)
        a = next((r for r in adlib if _same(r["value"]["page"], name)), None)
        dv, av = (d or {}).get("value") or {}, (a or {}).get("value") or {}
        lv = next((v for k, v in learn.items() if _same(k, name)), {})
        rd = next((r["value"] for r in reddit if _same(r["value"].get("competitor"), name)), None)
        page_id = str(dv.get("page_id") or av.get("page_id") or "") or None
        longest = dv.get("longest_running_ad") or {}
        manual = dv.get("active_ads_seen")
        pulled = av.get("active_ads")
        actives = [x for x in (manual, pulled) if isinstance(x, int)]
        row = {"key": slug(name), "name": name, "frame": fr, "role": "competitor", "page_id": page_id,
               "record_ids": [r["id"] for r in (d, a) if r],
               "positioning": dv.get("positioning"), "push": dv.get("what_they_push"),
               "price_text": dv.get("price_band_usd"), "ad_library_url": dv.get("ad_library_url") or (
                   f"https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=US&view_all_page_id={page_id}"
                   if page_id else None),
               "active_ads": max(actives) if actives else None,
               "sample_ads": av.get("ads_seen"), "formats": _norm_formats(av.get("formats")),
               "median_days": lv.get("median_run_days"), "long_runners_30d": lv.get("long_runners_30d"),
               "longest_days": longest.get("days_running") or av.get("longest_run_days"),
               "longest_start": longest.get("start_date"), "longest_url": longest.get("ad_url"),
               "offers_seen": list(av.get("offers_seen") or []), "platforms": sorted(av.get("platforms") or []), "offer_share": None, "main_cta": None, "new_14d": None,
               "first_lines": {LINE_KEYS.get(k, "statement"): v for k, v in (av.get("hook_types") or {}).items()},
               "hook_labels": list(dv.get("hook_types") or []),
               "quotes": [e.get("quote") for e in ((a or {}).get("evidence") or []) if e.get("quote")],
               "reddit": rd, "captured_at": (a or d or {}).get("date"), "age_days": (a or d or {}).get("age_days"),
               "source": "brain" if (a or d) else "none"}
        if page_id and page_id in snap_rows:
            row.update(_snapshot_page(snap_rows[page_id], snapshot["captured_at"], snap_mod))
            row["captured_at"] = snapshot["captured_at"]
            row["age_days"] = (brain.today - dt.date.fromisoformat(snapshot["captured_at"])).days
        srcs = [("hook label", h) for h in row["hook_labels"]] + [("positioning", row["positioning"]), ("push line", row["push"])]
        srcs += [("quoted ad", q) for q in row["quotes"] if not re.search(r"\{\{", q or "")]
        row["angles"] = tag_sources(srcs, snap_mod.ANGLES)
        row["format_mix"] = _mix(row["formats"])
        out.append(row)
    try:
        cfg_pages = (snap_mod.config(brain.brand, brain.dir.parent).get("meta_ad_library") or {}).get("pages") or []
    except (OSError, ValueError):
        cfg_pages = []
    self_id = next((str(p["page_id"]) for p in cfg_pages if p.get("role") == "self" and p.get("page_id")), None)
    out.append(self_row(brain, profile, snap_mod, snapshot, snap_rows, self_id))
    return out


def self_row(brain, profile: dict, snap_mod, snapshot, snap_rows, self_id: str | None = None) -> dict:
    """The brand's own page from the brain: hook labels carry counts, so its angle tags carry counts too."""
    brand = brain.brand
    get = lambda k: (brain.get(f"{brand}.{k}") or {}).get("value")  # noqa: E731
    fm = next((v for r in brain.records("learnings") if isinstance(v := r.get("value"), dict)
               and v.get("role") == "self" and v.get("signal_only")), {})
    share = get("offers.promo_share_active_ads") or {}
    hooks = profile.get("hooks") or {}
    active = profile.get("active_ads")
    snapf = _norm_formats(profile.get("formats"))
    counts: dict[str, int] = {}
    words: dict[str, dict] = {}
    for label, n in hooks.items():
        for t in tag_sources([("hook label", label)], snap_mod.ANGLES):
            counts[t["tag"]] = counts.get(t["tag"], 0) + (n if isinstance(n, int) else 0)
            words.setdefault(t["tag"], t)
    mission = get("story_bank.mission_line_in_ads") or {}
    m = re.match(r"(\d+) of (\d+)", str(mission.get("share") or ""))
    if m:
        counts["giving"] = max(counts.get("giving", 0), int(m.group(1)))
        words.setdefault("giving", {"tag": "giving", "label": "Giving and mission", "word": "donated", "where": "story bank"})
    long = get("learnings.long_running_ads") or []
    longest = max(long, key=lambda x: x.get("days_running") or 0) if isinstance(long, list) and long else {}
    row = {"key": slug(brand), "name": brand.capitalize(), "frame": "self", "role": "self", "page_id": self_id,
           "record_ids": [f"{brand}.learnings.hook_types", f"{brand}.learnings.active_ads_snapshot"],
           "positioning": get("positioning.frame"), "push": None, "price_text": None, "ad_library_url": None,
           "active_ads": active, "sample_ads": sum(_norm_formats(fm.get("formats")).values()) or None,
           # the page-level pull splits dynamic creative from catalog; the manual snapshot folds them together
           "formats": _norm_formats(fm.get("formats")) or snapf,
           "median_days": fm.get("median_run_days"), "long_runners_30d": fm.get("long_runners_30d"),
           "longest_days": longest.get("days_running"), "longest_start": longest.get("start_date"),
           "longest_url": longest.get("ad_url"), "long_ads": long if isinstance(long, list) else [],
           "offers_seen": [v["promo"] for r in brain.records("offers") if isinstance(v := r.get("value"), dict) and v.get("promo")],
           "offer_share": round(share["ads_with_code"] / share["active_ads"], 3)
           if isinstance(share.get("ads_with_code"), int) and share.get("active_ads") else None,
           "main_cta": None, "new_14d": None, "platforms": sorted(fm.get("platforms") or []),
           "first_lines": {LINE_KEYS.get(k, "statement"): v for k, v in (fm.get("hook_types") or {}).items()},
           "hook_labels": list(hooks), "quotes": [], "reddit": None,
           "captured_at": (brain.get(f"{brand}.learnings.hook_types") or {}).get("date"),
           "age_days": (brain.get(f"{brand}.learnings.hook_types") or {}).get("age_days"), "source": "brain",
           "angles": [dict(words[k], n=counts[k]) for k in words], "angle_counts": counts}
    sep = get("learnings.september_flight") or {}
    if isinstance(sep.get("started_since_2026_09_01"), int):
        row["new_since_month_start"] = sep["started_since_2026_09_01"]
    if snapshot and self_id and self_id in snap_rows:
        row.update(_snapshot_page(snap_rows[self_id], snapshot["captured_at"], snap_mod))
    row["format_mix"] = _mix(row["formats"])
    return row


# ---------------------------------------------------------------- verdicts

THREAT_AT, WATCH_AT = 4, 2


def verdict(p: dict, us: dict, our_top: list[str]) -> dict:
    """threat, watch or ignore from points a strategist would count, each with its number."""
    if p["source"] == "none":
        return {"kind": "na", "text": "No data", "points": 0, "short": "no page id yet",
                "reason": "No page id and no capture. Paste the page id to track it.", "why": []}
    why, short = [], []
    pts = 0
    if p["frame"] == "direct":
        pts += 2
        why.append("direct competitor (+2)")
        short.append("direct")
    ours = us.get("active_ads")
    if isinstance(p["active_ads"], int) and isinstance(ours, int) and ours and p["active_ads"] >= 2 * ours:
        pts += 1
        x = round(p["active_ads"] / ours, 1)
        why.append(f"{p['active_ads']} active ads, {x:g}x ours (+1)")
        short.append(f"{x:g}x our ads")
    if isinstance(p["median_days"], (int, float)) and p["median_days"] >= 30:
        pts += 1
        why.append(f"median ad live {p['median_days']:g} days, keeps winners (+1)")
        short.append(f"ads live {p['median_days']:g} days")
    shared = [a["label"].lower() for a in p["angles"] if a["tag"] in our_top]
    if shared:
        pts += 1
        why.append(f"runs our angle: {', '.join(shared)} (+1)")
        short.append(f"runs {shared[0]}")
    rd = p.get("reddit") or {}
    if rd.get("recommended_instead"):
        pts += 1
        why.append(f"recommended instead of us {rd['recommended_instead']} times on Reddit (+1)")
        short.append(f"Reddit picks them {rd['recommended_instead']}x")
    kind, text = ("stop", "Threat") if pts >= THREAT_AT else ("watch", "Watch") if pts >= WATCH_AT else ("keep", "Ignore")
    return {"kind": kind, "text": text, "points": pts, "why": why,
            "short": f"{pts} pts: " + (", ".join(short) if short else "nothing above the bar"),
            "reason": f"{pts} points: " + ("; ".join(why) if why else "no signal above the bar")}


def our_top_angles(us: dict, n: int = 2) -> list[str]:
    c = us.get("angle_counts") or {}
    return [k for k, _ in sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))[:n]]


def median(xs):
    xs = [x for x in xs if isinstance(x, (int, float))]
    return statistics.median(xs) if xs else None


def battlecard(p: dict, us: dict, price_us: float | None, gaps: list[str]) -> str:
    """A support and sales card against one page, from verified brain fields only. Signals, never their copy."""
    name, brand = p["name"], us["name"]
    theirs = ", ".join(a["label"].lower() for a in p["angles"]) or "no angle tagged"
    top = sorted((us.get("angle_counts") or {}).items(), key=lambda kv: -kv[1])[:2]
    ours = ", ".join(f"{next((a['label'].lower() for a in us['angles'] if a['tag'] == k), k)} ({n} ads)" for k, n in top)
    lines = [f"Battlecard: {brand} against {name}.",
             f"They lead with: {theirs}.",
             f"We lead with: {ours or 'unavailable'} of {us.get('active_ads') if us.get('active_ads') is not None else 'unavailable'} active ads."]
    if p.get("price_text"):
        lines.append(f"Their price: {p['price_text']}." + (f" Ours nets ${price_us:.2f} a pair (simulated)." if price_us else ""))
    if gaps:
        lines.append(f"What we have that they do not show: {', '.join(gaps)}.")
    if p.get("offers_seen"):
        lines.append(f"Their offers seen: {', '.join(p['offers_seen'])}.")
    lines.append("Say only what the brain verifies. Refresh this card when the next capture lands.")
    return "\n".join(lines)
