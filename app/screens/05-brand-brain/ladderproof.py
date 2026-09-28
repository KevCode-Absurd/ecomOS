"""Ladder proof matrix: every objection rung by the surface it is meant for, and whether the proof is on file.

Each objection ladder rung names a doubt, the one-star and five-star lines behind it, the surfaces it is used on
(`uses`: ad copy, product page, Amazon listing, CX macro, offer) and the records that prove the answer (`proof_ids`).
The matrix reads those records: a rung whose proof is an approved or site-backed record is proved on every surface it
is used on; a rung whose proof is a lower tier is weak until the claim is tiered; a rung with no proof id, or an id the
brain no longer holds, is a gap on each surface, and the gap carries a proof brief plus the records already on file
that could stand as proof (ranked by word overlap with the doubt and the one-star lines). A proof that fails a surface's
channel rules (Amazon: no promotional wording; Meta: no personal attributes) is blocked on that surface only. The
founder picks a record as proof and the ladder record is updated as a founder edit. Rule BRN-R23 turns each unproved
rung into a brief on the master list. Nothing here is a model's judgement: ids, tiers, word overlap and regexes.
"""
from __future__ import annotations

import re

SURFACES = [("copy", "Ad copy", "meta"), ("pdp", "Product page", None), ("amazon_listing", "Amazon listing", "amazon"), ("cx_macro", "CX macro", None), ("offer", "Offer", None)]
PROOF_TIERS = ("approved", "site_backed")
CANDIDATE_SECTIONS = ("claims", "policies", "offers", "products", "identity")
STOP = set("the a an and or of to in on for with is are was were be it its this that these those they them you your we our at from by as not no so if but than then there here can will just also very more most any all each every one".split())


def _words(s) -> set[str]:
    return {w for w in re.findall(r"[a-z]{4,}", (s or "").lower().replace("_", " ")) if w not in STOP}


def _pretty(s: str) -> str:
    return (s or "").replace("_", " ")


def candidates(brain, rung: dict, top: int = 3) -> list[dict]:
    """Records on file that could prove this rung, ranked by word overlap with the doubt and the one-star lines."""
    need = _words(rung.get("doubt")) | set().union(*[_words(x) for x in (rung.get("one_star") or [])[:3]]) | set().union(*[_words(x) for x in (rung.get("five_star") or [])[:3]])
    out = []
    for sec in CANDIDATE_SECTIONS:
        for r in brain.records(sec):
            if r["tier"] == "forbidden":
                continue
            text = r.get("text") if isinstance(r.get("text"), str) else str(r.get("value") or "")
            hit = need & (_words(text) | _words(r.get("field") or ""))
            if len(hit) >= 2:
                out.append({"id": r["id"], "tier": r["tier"], "text": text[:160], "overlap": sorted(hit)[:5], "usable": r["tier"] in PROOF_TIERS})
    out.sort(key=lambda c: (-len(c["overlap"]), not c["usable"], c["id"]))
    return out[:top]


def _brief(theme: str, rung: dict, cands: list[dict], surfaces: list[str]) -> str:
    counts = rung.get("counts") or {}
    lines = [f"Proof brief: {_pretty(theme)}, rung {rung.get('level')}",
             f"Doubt: {rung.get('doubt')}",
             f"Weight: {counts.get('one_star', 'n/a')} one-star lines, {counts.get('five_star', 'n/a')} five-star lines.",
             "Used on: " + ", ".join(_pretty(s) for s in surfaces) + ".",
             "What counts as proof: a policy, a product fact, an offer term or a tiered claim in the brain, approved or backed by the site. Never a review quote as a testimonial."]
    if rung.get("one_star"):
        lines.append("The doubt in their words: " + " | ".join(str(x)[:90] for x in rung["one_star"][:2]))
    if rung.get("five_star"):
        lines.append("What the happy ones say (a lead, not a claim): " + " | ".join(str(x)[:90] for x in rung["five_star"][:2]))
    if cands:
        lines.append("On file already: " + " | ".join(f"{c['id']} [{_pretty(c['tier'])}]" for c in cands))
        lines.append("Pick one as the proof, or draft the missing fact and get it approved.")
    else:
        lines.append("On file already: nothing that names this doubt. Draft the fact, source it, approve it, then attach it.")
    return "\n".join(lines)


def matrix(brain, claims_mod=None) -> dict:
    ladders = [r for r in brain.records("objection_ladders") if isinstance(r.get("value"), dict)]
    active = {r["id"]: r for r in brain.records()}
    cols = [{"key": k, "label": lab, "title": f"rungs used on the {lab.lower()}"} for k, lab, _ in SURFACES]
    rows, cells, gaps, weak, blocked, rungs_out = [], {}, [], [], [], []
    if not ladders:
        return {"rows": [], "cols": cols, "cells": {}, "gaps": [], "weak": [], "blocked": [], "rungs": [],
                "counts": {"rungs": 0, "proved": 0, "weak": 0, "missing": 0, "cells_used": 0, "cells_gap": 0}, "unavailable_reason": "no objection ladders in the brain yet; the customers screen builds them from reviews",
                "note": "Each cell: the rung's proof on that surface. 2 proved (approved or site backed), 1 weak (a lower tier) or blocked by the surface's rules, 0 no proof on file."}
    for lad in ladders:
        v = lad["value"]
        theme = v.get("theme") or lad.get("field") or lad["id"].rsplit(".", 1)[-1]
        for rung in v.get("rungs") or []:
            level = rung.get("level")
            key = f"{theme}.{level}"
            uses = [u for u in (rung.get("uses") or []) if u in {s[0] for s in SURFACES}]
            counts = rung.get("counts") or {}
            proof_ids = [p for p in (rung.get("proof_ids") or []) if isinstance(p, str)]
            proofs = [active[p] for p in proof_ids if p in active]
            lost = [p for p in proof_ids if p not in active]
            tiers = [p["tier"] for p in proofs]
            if any(t == "forbidden" for t in tiers):
                status, best = "forbidden", "forbidden"
            elif any(t in PROOF_TIERS for t in tiers):
                status = "proved"
                best = "approved" if "approved" in tiers else "site_backed"
            elif proofs:
                status, best = "weak", sorted(tiers, key=lambda t: ["reported", "evidence", "inferred", "unverified"].index(t) if t in ("reported", "evidence", "inferred", "unverified") else 9)[0]
            else:
                status, best = "missing", None
            score = {"proved": 2, "weak": 1, "missing": 0, "forbidden": 0}[status]
            rows.append({"key": key, "label": f"{_pretty(theme).capitalize()} {level}: {rung.get('doubt')}", "sub": f"{counts.get('one_star', 'n/a')} one-star, {counts.get('five_star', 'n/a')} five-star", "theme": theme, "level": level})
            cells[key] = {}
            proof_text = " ".join(str(p.get("text") or p.get("value") or "") for p in proofs)
            for skey, slabel, channel in SURFACES:
                if skey not in uses:
                    continue
                cell = {"us": score, "unit": "n", "status": status, "tier": best, "label": {"proved": f"proved, {_pretty(best)}", "weak": f"weak, {_pretty(best)}", "missing": "no proof on file", "forbidden": "proof is a forbidden claim"}[status], "act": status in ("missing", "forbidden"), "proof_ids": proof_ids}
                if status == "proved" and channel and claims_mod is not None and proof_text:
                    try:
                        hits = [h for h in claims_mod.channel_scan(brain, proof_text, channel).get("channel_hits", []) if h.get("severity") == "fail"]
                    except Exception:  # noqa: BLE001
                        hits = []
                    if hits:
                        cell.update(us=1, status="blocked", label=f"blocked on {slabel.lower()}: {hits[0].get('reason') or hits[0].get('rule')}", fix=hits[0].get("fix"), act=True)
                        blocked.append({"rung": key, "surface": skey, "surface_label": slabel, "reason": hits[0].get("reason"), "fix": hits[0].get("fix"), "proof_ids": proof_ids})
                cells[key][skey] = cell
            cands = candidates(brain, rung) if status in ("missing", "forbidden") else []
            item = {"key": key, "theme": theme, "level": level, "doubt": rung.get("doubt"), "status": status, "tier": best, "uses": uses, "proof_ids": proof_ids, "lost_ids": lost,
                    "one_star": counts.get("one_star"), "five_star": counts.get("five_star"), "proof": rung.get("proof"), "record": lad["id"], "candidates": cands,
                    "brief": _brief(theme, rung, cands, uses) if status in ("missing", "forbidden") else None}
            rungs_out.append(item)
            if status in ("missing", "forbidden"):
                gaps.append(item)
            elif status == "weak":
                weak.append(item)
    gaps.sort(key=lambda g: -(g["one_star"] or 0))
    used = sum(len(c) for c in cells.values())
    gap_cells = sum(1 for c in cells.values() for x in c.values() if x["status"] in ("missing", "forbidden"))
    counts = {"rungs": len(rows), "proved": sum(1 for r in rungs_out if r["status"] == "proved"), "weak": len(weak), "missing": len(gaps), "blocked": len(blocked), "cells_used": used, "cells_gap": gap_cells,
              "one_star_unproved": sum(g["one_star"] or 0 for g in gaps), "one_star_total": sum(r["one_star"] or 0 for r in rungs_out)}
    return {"rows": rows, "cols": cols, "cells": cells, "gaps": gaps, "weak": weak, "blocked": blocked, "rungs": rungs_out, "counts": counts, "unavailable_reason": None,
            "note": "Each cell: the rung's proof on that surface. 2 proved (approved or site backed), 1 weak (a lower tier) or blocked by the surface's rules, 0 no proof on file. An empty cell means the rung is not used there."}


def attach(brain, theme: str, level, record_id: str) -> dict | tuple[int, dict]:
    """Set a brain record as the proof of one rung: a founder edit on the ladder record. Returns the updated ladder record to put."""
    active = {r["id"]: r for r in brain.records()}
    proof = active.get(record_id)
    if proof is None:
        return 404, {"error": "no active record with that id", "record_id": record_id}
    if proof["tier"] == "forbidden":
        return 400, {"error": "a forbidden claim cannot stand as proof", "record_id": record_id}
    lad = next((r for r in brain.raw("objection_ladders") if isinstance(r.get("value"), dict) and r.get("status", "active") != "retired" and (r["value"].get("theme") or r.get("field")) == theme), None)
    if lad is None:
        return 404, {"error": "no ladder with that theme", "theme": theme}
    try:
        lvl = int(level)
    except (TypeError, ValueError):
        return 400, {"error": "level must be a number"}
    rungs = [dict(r) for r in lad["value"].get("rungs") or []]
    rung = next((r for r in rungs if r.get("level") == lvl), None)
    if rung is None:
        return 404, {"error": "no rung at that level", "theme": theme, "level": lvl}
    ids = [p for p in (rung.get("proof_ids") or []) if p != record_id] + [record_id]
    rung["proof_ids"] = ids
    rung["proof"] = (proof.get("text") if isinstance(proof.get("text"), str) else str(proof.get("value") or ""))[:300]
    was = {"type": (lad.get("source") or {}).get("type"), "ref": (lad.get("source") or {}).get("ref"), "tier": lad.get("tier")}
    new = dict(lad, value=dict(lad["value"], rungs=rungs), tier="approved", confidence=1.0, status="active",
               source={"type": "founder", "ref": f"05-brand-brain ladder proof matrix: rung {lvl} proof {record_id}", "captured_at": brain.today.isoformat(), "was": was})
    new.pop("expires_at", None)
    return {"record": new, "rung": rung, "proof_tier": proof["tier"], "usable": proof["tier"] in PROOF_TIERS}
