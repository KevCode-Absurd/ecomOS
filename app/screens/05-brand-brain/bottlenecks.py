"""Bottlenecks and unlocks: the brain's diagnosis, the master list items that address each bottleneck, and the
idea bank's best unlocks for it, ranked in code.

Diagnosis records (diagnosis section: summary, bottleneck_<n> with a theme and quote counts, strength_<n>, test_queue)
name the pressure points. Each bottleneck maps to the idea bank's fixed taxonomy by generic keywords, the brand's store
tags come from its own records (market, platform, channel mix, paid split, catalogue size), and `intelligence.ideas`
filters and ranks the bank. Ideas are referenced by id, never copied. A founder picks an idea by writing a `plans`
record (`plans.idea_<id>`), which audit.py turns into a finding (BRN-R22) and rank() into a test brief action, so a
picked idea lands on the master list. Master-list actions are matched to a bottleneck by word overlap with its theme.
"""
from __future__ import annotations

import datetime as dt
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
try:
    from intelligence import ideas as IDEAS
except Exception:  # noqa: BLE001
    IDEAS = None

# generic words to the bank's fixed bottleneck codes (ideas/README.md)
CODE_WORDS = [
    ("trust_brand", ["durab", "quality", "trust", "believe", "guarantee", "review", "reputation", "authentic"]),
    ("conversion", ["price", "objection", "fit", "sizing", "size", "convert", "doubt", "compare", "checkout", "pdp", "listing"]),
    ("margin_cogs", ["margin", "cost", "discount", "price war", "cogs"]),
    ("repeat_retention", ["repeat", "retention", "churn", "come back", "second order", "loyal"]),
    ("acquisition_efficiency", ["cpa", "cac", "roas", "paid", "ad cost", "efficien"]),
    ("acquisition_volume", ["traffic", "reach", "awareness", "volume", "new customer"]),
    ("aov", ["aov", "basket", "pack size", "bundle", "order value"]),
    ("fulfilment_cx", ["shipping", "delivery", "return", "support", "ticket", "slow"]),
    ("cash_inventory", ["stock", "inventory", "cash"]),
    ("site_speed", ["speed", "slow page", "lcp"]),
    ("measurement_data", ["tracking", "attribution", "measure", "pixel"]),
    ("risk_compliance", ["claim", "compliance", "fraud", "policy"]),
]
STOP = set("the a an and or of to in on for with is are was were be it its this that these those at from by as not no vs".split())


def codes_for(text: str) -> list[str]:
    t = (text or "").lower().replace("_", " ")
    out = [code for code, words in CODE_WORDS if any(w in t for w in words)]
    return out or ["conversion"]


def store_tags(brain) -> set[str]:
    tags = {"one_off", "us"}
    recs = {(r["section"], r.get("field")): r for r in brain.records()}
    hq = recs.get(("identity", "headquarters"))
    if hq and isinstance(hq.get("value"), dict) and str(hq["value"].get("country") or "").upper() not in ("", "US", "USA"):
        tags.discard("us")
    plat = recs.get(("stack", "platform"))
    if plat and "shopify" in str(plat.get("value") or plat.get("text") or "").lower():
        tags.add("shopify")
    mix = recs.get(("economics", "channel_mix"))
    if mix and isinstance(mix.get("value"), dict):
        v = mix["value"]
        if (v.get("marketplaces_pct") or 0) >= 25:
            tags.add("marketplace_heavy")
        if (v.get("dtc_site_pct") or 0) >= 90:
            tags.add("dtc_only")
    split = recs.get(("economics", "paid_media_split"))
    if split and isinstance(split.get("value"), dict) and (split["value"].get("meta_pct") or 0) >= 40:
        tags.add("paid_social_led")
    lines = recs.get(("products", "lines"))
    if lines and isinstance(lines.get("value"), list):
        tags.add("catalogue" if len(lines["value"]) >= 5 else "hero_sku")
    rev = recs.get(("economics", "revenue_point_usd"))
    if rev and isinstance(rev.get("value"), (int, float)) and rev["value"] >= 5_000_000:
        tags.add("scaling_store")
    return tags


def _words(s: str) -> set[str]:
    return {w for w in re.findall(r"[a-z]{4,}", (s or "").lower().replace("_", " ")) if w not in STOP}


def diagnosis(brain) -> dict:
    recs = {r.get("field"): r for r in brain.records("diagnosis")}
    summary = recs.get("summary")
    bottlenecks, strengths = [], []
    for f, r in sorted(recs.items(), key=lambda kv: kv[0] or ""):
        v = r.get("value") if isinstance(r.get("value"), dict) else {}
        if (f or "").startswith("bottleneck_"):
            bottlenecks.append({"key": f, "rank": int(f.split("_")[-1]) if f.split("_")[-1].isdigit() else 9, "theme": v.get("theme") or f, "text": r.get("text"),
                                "numbers": {k: x for k, x in v.items() if isinstance(x, (int, float))}, "where": v.get("where") or [], "record": r["id"], "tier": r["tier"], "date": r["date"]})
        elif (f or "").startswith("strength_"):
            strengths.append({"key": f, "theme": v.get("theme") or f, "text": r.get("text"), "numbers": {k: x for k, x in v.items() if isinstance(x, (int, float))}, "record": r["id"]})
    bottlenecks.sort(key=lambda b: b["rank"])
    tq = recs.get("test_queue")
    tests = tq.get("value") if tq and isinstance(tq.get("value"), list) else []
    return {"summary": summary.get("text") if summary else None, "summary_record": summary["id"] if summary else None, "as_of": (summary.get("value") or {}).get("as_of") if summary and isinstance(summary.get("value"), dict) else None,
            "basis": (summary.get("value") or {}).get("basis") if summary and isinstance(summary.get("value"), dict) else None,
            "bottlenecks": bottlenecks, "strengths": strengths, "test_queue": [str(t) for t in tests], "test_queue_record": tq["id"] if tq else None}


REJECT_REVIEW_DAYS = 90


def rejected_ideas(brain) -> dict[str, dict]:
    """Ideas the founder rejected, with the reason and the review date: learnings records `rejected_idea_<id>`."""
    out = {}
    for r in brain.records("learnings"):
        if (r.get("field") or "").startswith("rejected_idea_") and isinstance(r.get("value"), dict):
            v = r["value"]
            iid = v.get("idea_id") or (r.get("field") or "")[14:].upper().replace("_", "-")
            review_on = v.get("review_on")
            due = None
            try:
                due = (dt.date.fromisoformat(review_on) - brain.today).days if review_on else None
            except ValueError:
                due = None
            out[iid] = {"record": r["id"], "idea_id": iid, "title": v.get("title"), "reason": v.get("reason"), "bottleneck": v.get("bottleneck"), "rejected_on": None if r["date"] == "undated" else r["date"],
                        "review_on": review_on, "days_to_review": due, "due": due is not None and due <= 0, "out": due is None or due > 0}
    return out


def picked_ideas(brain) -> dict[str, dict]:
    out = {}
    for r in brain.records("plans"):
        if (r.get("field") or "").startswith("idea_") and isinstance(r.get("value"), dict):
            out[r["value"].get("idea_id") or (r.get("field") or "")[5:]] = {"record": r["id"], "status": r["value"].get("status"), "bottleneck": r["value"].get("bottleneck"), "date": None if r["date"] == "undated" else r["date"], "why": r["value"].get("why")}
    return out


def unlocks(brain, master_actions: list[dict], per: int = 5) -> dict:
    d = diagnosis(brain)
    tags = store_tags(brain)
    picked = picked_ideas(brain)
    rejected = rejected_ideas(brain)
    keep_out = {k for k, v in rejected.items() if v["out"]}
    bank = IDEAS.load() if IDEAS else []
    out = []
    for b in d["bottlenecks"]:
        codes = codes_for(b["theme"] + " " + (b["text"] or ""))
        theme_key = _words(b["theme"])
        theme_words = theme_key | _words((b["text"] or "")[:160])
        on_list = []
        for a in master_actions:
            if a.get("status") == "unavailable":
                continue
            aw = _words(a.get("title", "")) | _words(a.get("why", "")[:200]) | _words((a.get("entity") or {}).get("label", ""))
            overlap = theme_words & aw
            if (theme_key & aw) or len(overlap) >= 2:
                on_list.append({"id": a["id"], "title": a["title"], "screen": a.get("screen"), "owner": a["owner"], "total": (a.get("rubric") or {}).get("total"), "overlap": sorted(overlap)[:4], "decision": a.get("decision")})
        on_list.sort(key=lambda x: -(x["total"] or 0))
        ideas = []
        if bank:
            sel = IDEAS.filter_ideas(bank, set(codes), tags, None, None, set(picked) | keep_out)
            sel = IDEAS.rank(sel, set(codes))
            # an idea must name the theme (a theme-key word in its title, hypothesis or signal); then by fit, then by the bank's score
            def hit(it):
                hay = _words(it["title"]) | _words(it.get("hypothesis", "")) | _words(it["signal"].get("check", ""))
                return len(theme_key & hay) * 3 + len(theme_words & hay)
            named = [it for it in sel if theme_key & (_words(it["title"]) | _words(it.get("hypothesis", "")) | _words(it["signal"].get("check", "")))]
            named.sort(key=lambda it: (-hit(it), -IDEAS.score(it, set(codes))))
            pool = named if len(named) >= per else named + [it for it in sel if it not in named][: per - len(named)]
            for it in pool[:per]:
                e = it["expected_effect"]
                back = rejected.get(it["id"])
                ideas.append({"id": it["id"], "title": it["title"], "domain": it["domain"], "score": IDEAS.score(it, set(codes)), "lever": it.get("lever"),
                              "was_rejected": {"on": back["rejected_on"], "reason": back["reason"], "review_on": back["review_on"]} if back else None,
                              "hypothesis": it.get("hypothesis"), "signal": it["signal"].get("check"), "metric": e.get("metric"), "direction": e.get("direction"), "size": e.get("size"), "basis": e.get("basis"),
                              "effort": it["effort"].get("size"), "cost": it.get("cost"), "risk": it["risk"].get("level"), "reversible": it["risk"].get("reversible"), "steps": (it.get("steps") or [])[:4],
                              "theme_hits": hit(it), "confidence": it.get("confidence")})
        out.append(dict(b, codes=codes, on_list=on_list, ideas=ideas, picked=[dict(v, idea_id=k) for k, v in picked.items() if v.get("bottleneck") == b["key"]],
                        rejected=[v for v in rejected.values() if v.get("bottleneck") == b["key"]]))
    return {"diagnosis": {k: d[k] for k in ("summary", "summary_record", "as_of", "basis", "strengths", "test_queue", "test_queue_record")}, "bottlenecks": out, "store_tags": sorted(tags),
            "bank": {"ideas": len(bank), "available": bool(bank)}, "picked": len(picked), "rejected": len(rejected), "rejected_due": sum(1 for v in rejected.values() if v["due"]),
            "rejected_list": sorted(rejected.values(), key=lambda v: (v["review_on"] or "9999", v["idea_id"])),
            "note": "Bottlenecks come from the diagnosis in the brain (public sources and simulated data, a hypothesis to test). Items on the list are matched by words; ideas come from the bank filtered by the bottleneck code and this brand's store tags, ranked in code by evidence, ease, safety and fit. Pick an idea and it becomes a plan record and a test brief on the master list."}


def reject(brain, idea_id: str, bottleneck_key: str | None, reason: str, review_on: str | None) -> dict:
    """A rejected idea with its reason and review date: a learnings record agents read before proposing."""
    bank = IDEAS.load() if IDEAS else []
    it = next((x for x in bank if x["id"] == idea_id), None)
    if it is None:
        return {"ok": False, "error": "no such idea", "id": idea_id}
    if review_on:
        try:
            dt.date.fromisoformat(review_on)
        except ValueError:
            return {"ok": False, "error": "review_on must be a date like 2026-12-31"}
    else:
        review_on = (brain.today + dt.timedelta(days=REJECT_REVIEW_DAYS)).isoformat()
    field = "rejected_idea_" + re.sub(r"[^a-z0-9]+", "_", idea_id.lower()).strip("_")
    rec = {"id": f"{brain.brand}.learnings.{field}", "brand": brain.brand, "section": "learnings", "field": field,
           "value": {"idea_id": it["id"], "title": it["title"], "bottleneck": bottleneck_key, "reason": reason[:200] or None, "review_on": review_on, "kind": "rejected_idea"},
           "text": f"Rejected idea {it['id']}: {it['title']}" + (f". Reason: {reason[:140]}" if reason else ".") + f" Review on {review_on}; agents do not propose it before then.",
           "tier": "approved", "confidence": 1.0, "visibility": "private",
           "source": {"type": "founder", "ref": "05-brand-brain bottlenecks and unlocks", "captured_at": brain.today.isoformat()}}
    return {"ok": True, "record": rec}


def pick(brain, idea_id: str, bottleneck_key: str | None, why: str) -> dict:
    bank = IDEAS.load() if IDEAS else []
    it = next((x for x in bank if x["id"] == idea_id), None)
    if it is None:
        return {"ok": False, "error": "no such idea", "id": idea_id}
    field = "idea_" + re.sub(r"[^a-z0-9]+", "_", idea_id.lower()).strip("_")
    e = it["expected_effect"]
    rec = {"id": f"{brain.brand}.plans.{field}", "brand": brain.brand, "section": "plans", "field": field,
           "value": {"idea_id": it["id"], "title": it["title"], "bottleneck": bottleneck_key, "status": "picked", "why": why[:200] or None, "metric": e.get("metric"), "direction": e.get("direction"),
                     "effort": it["effort"].get("size"), "cost": it.get("cost"), "risk": it["risk"].get("level"), "signal": it["signal"].get("check"), "steps": (it.get("steps") or [])[:6]},
           "text": f"Picked idea {it['id']}: {it['title']}" + (f" for {bottleneck_key.replace('_', ' ')}" if bottleneck_key else "") + (f". Why: {why[:120]}" if why else "."),
           "tier": "approved", "confidence": 1.0, "visibility": "private",
           "source": {"type": "founder", "ref": "05-brand-brain bottlenecks and unlocks", "captured_at": brain.today.isoformat()}}
    return {"ok": True, "record": rec}
