"""Battlecards: how we win against each competitor, built from the brain and refreshed with every pull.

One card per competitor page the brain tracks (market.py pages), from records only:
- what they push (positioning, price band, what_they_push, angles from their hooks);
- where they beat us on the coverage matrix (angles they run that we do not) and where we hold ground;
- the doubt they exploit (the angle's ladder in our brain) and our proof status on its deal-breaker rung;
- public threads that recommend them instead (count, upvotes), never quoted;
- how we win: lines built from approved or site-backed claims and proof points that answer their angle;
- lines for CX (a macro) and for copy (a first line), drafted from those claims; owner agent drafts, you approve.
Deterministic, no model. Ships as `artefact research_note` for BRAND-C57. Layout and mood only from competitor
ads; never their text, logos, products or faces.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
_m = importlib.util.spec_from_file_location("brand_brain_market_bc", HERE / "market.py")
market = importlib.util.module_from_spec(_m)
_m.loader.exec_module(market)


def _usable_claims(brain) -> list[dict]:
    return [r for r in brain.records("claims") if r["tier"] in ("approved", "site_backed")]


def _proof_lines(brain, angles: list[str], claims: list[dict]) -> list[dict]:
    """Claims that answer the competitor's angles, by word overlap with the angle vocabulary."""
    out, seen = [], set()
    for key in angles:
        words = next((w for k, _, w in market.ANGLES if k == key), [])
        for c in claims:
            t = (c.get("text") or "").lower()
            if c["id"] in seen or not any(w in t for w in words):
                continue
            seen.add(c["id"])
            out.append({"angle": key, "claim": c["id"], "text": c.get("text"), "tier": c["tier"]})
    return out


def cards(brain) -> dict:
    d = market.pages(brain)
    cov = market.coverage(brain)
    sg = market.signals(brain)
    us_angles = {r["key"] for r in cov["rows"] if (cov["cells"].get(r["key"], {}).get("us", {}).get("us") or 0) > 0}
    proof_points = next((r for r in brain.records("positioning") if r["id"] == f"{brain.brand}.positioning.proof_points"), None)
    pp = proof_points.get("value") if proof_points and isinstance(proof_points.get("value"), list) else []
    claims = _usable_claims(brain)
    rec_by = {r["slug"]: r for r in sg["recommended"]}
    out = []
    for p in d["pages"]:
        if p["role"] != "competitor" or not p.get("angles"):
            continue
        their = []
        for lbl in p["angles"]:
            their += [a for a in market.angles_of(lbl) if a not in their]
        they_win = [a for a in their if a not in us_angles]
        contested = [a for a in their if a in us_angles]
        rec = rec_by.get(p["slug"]) or next((r for k, r in rec_by.items() if k and (k in p["slug"] or p["slug"].startswith(k))), None)
        lead = their[0] if their else None
        ladder = market._ladder_for(brain, lead) if lead else None
        db = (ladder or {}).get("deal_breaker") or {}
        proofs = _proof_lines(brain, their, claims)
        how_we_win = []
        for a in their[:3]:
            pr = next((x for x in proofs if x["angle"] == a), None)
            if pr:
                how_we_win.append({"angle": a, "label": market.ANGLE_LABEL.get(a, a), "line": pr["text"], "claim": pr["claim"], "status": "proof on file"})
            else:
                how_we_win.append({"angle": a, "label": market.ANGLE_LABEL.get(a, a), "line": None, "claim": None, "status": "no usable claim: answer the open question or approve one"})
        cx_line = next((f"{w['line']}" for w in how_we_win if w["line"]), None)
        copy_line = None
        if pp:
            copy_line = f"{pp[0][0].upper() + pp[0][1:]}." if isinstance(pp[0], str) else None
        card = {
            "competitor": p["name"], "slug": p["slug"], "page_id": p["page_id"], "ad_library_url": p["ad_library_url"], "captured_at": p["captured_at"],
            "positioning": p.get("positioning"), "price_band": p.get("price_band"), "pushes": p.get("what_they_push"), "ads_seen": p["ads_seen"],
            "long_runner_share": p["long_runner_share"], "flags": p["flags"],
            "their_angles": [{"key": a, "label": market.ANGLE_LABEL.get(a, a)} for a in their],
            "they_win": [{"key": a, "label": market.ANGLE_LABEL.get(a, a)} for a in they_win],
            "contested": [{"key": a, "label": market.ANGLE_LABEL.get(a, a)} for a in contested],
            "recommended_instead": {"threads": rec["threads"], "upvotes": rec["upvotes"], "subreddits": rec["subreddits"]} if rec else None,
            "doubt": {"angle": lead, "label": market.ANGLE_LABEL.get(lead, lead) if lead else None, "ladder": (ladder or {}).get("theme"),
                      "deal_breaker": db.get("doubt"), "has_proof": db.get("has_proof"), "one_star": db.get("one_star")} if lead else None,
            "how_we_win": how_we_win, "cx_line": cx_line, "copy_line": copy_line,
            "proof_gaps": [w["label"] for w in how_we_win if not w["line"]],
            "record_ids": p["record_ids"][:3] + ([rec["record_id"]] if rec else []),
        }
        card["verdict"] = _verdict(card)
        card["text"] = _text(brain.brand, card)
        out.append(card)
    order = {"stop": 0, "fix": 1, "keep": 2}
    out.sort(key=lambda c: (order.get(c["verdict"]["kind"], 9), -(c["ads_seen"] or 0)))
    return {"cards": out, "counts": {"cards": len(out), "with_gaps": sum(1 for c in out if c["proof_gaps"]), "recommended_instead": sum(1 for c in out if c["recommended_instead"])},
            "note": "Built from the brain on every load: their angles from their hooks, our proof from approved or site-backed claims. Never their text, logos, products or faces. Threads are counted, never quoted."}


def _verdict(c: dict) -> dict:
    if c["recommended_instead"] and c["proof_gaps"]:
        return {"kind": "stop", "text": "Losing", "reason": f"recommended instead in {c['recommended_instead']['threads']} threads and we lack proof on {', '.join(c['proof_gaps'][:2]).lower()}"}
    if c["proof_gaps"]:
        return {"kind": "fix", "text": "Proof gap", "reason": "no usable claim for " + ", ".join(c["proof_gaps"][:2]).lower()}
    if c["they_win"]:
        return {"kind": "fix", "text": "Angle gap", "reason": "they run " + ", ".join(a["label"].lower() for a in c["they_win"][:2]) + " and we do not"}
    return {"kind": "keep", "text": "Covered", "reason": "every angle they run has a usable claim behind our answer"}


def _text(brand: str, c: dict) -> str:
    lines = [f"Battlecard: {brand} against {c['competitor']}", ""]
    if c["positioning"]:
        lines.append(f"They say: {c['positioning']}")
    if c["price_band"]:
        lines.append(f"Their price: {c['price_band']}")
    if c["pushes"]:
        lines.append(f"They push now: {c['pushes']}")
    lines.append("Their angles: " + (", ".join(a["label"].lower() for a in c["their_angles"]) or "none read"))
    if c["they_win"]:
        lines.append("Where they run and we do not: " + ", ".join(a["label"].lower() for a in c["they_win"]))
    if c["recommended_instead"]:
        r = c["recommended_instead"]
        lines.append(f"Public threads recommend them instead {r['threads']} times ({r['upvotes']} upvotes). Not quoted.")
    if c["doubt"] and c["doubt"]["deal_breaker"]:
        lines.append(f"The doubt they exploit: {c['doubt']['deal_breaker']} " + ("(proof on file)" if c["doubt"]["has_proof"] else "(no proof on our ladder yet)"))
    lines.append("")
    lines.append("How we win:")
    for w in c["how_we_win"]:
        lines.append(f"- {w['label']}: " + (w["line"] if w["line"] else f"[{w['status']}]"))
    if c["cx_line"]:
        lines.append("")
        lines.append(f"CX macro: {c['cx_line']}")
    if c["copy_line"]:
        lines.append(f"Copy first line: {c['copy_line']}")
    lines.append("")
    lines.append("Rule: layout and mood only from their ads. Never their text, logos, products or faces.")
    return "\n".join(lines)
