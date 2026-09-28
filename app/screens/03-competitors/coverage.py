"""The creative coverage matrix: angles by format, our share of ads against theirs in every cell.

Model after the Meta gallery's coverage map (meta_gallery/web/buyer.js, bdCoverage), turned to face
the competitors: rows are the angles from snapshot.ANGLES, columns the formats, and each cell holds
the share of our active ads and the share of the tracked pages' ads in that angle and format.

With an ad-level snapshot every cell is counted from ad rows. Without one it is estimated from what
the brain holds per page, and says so:
  them: a page's ads in a format, split evenly over the angles tagged on that page, summed over pages,
        divided by all their ads.
  us:   our ads carrying the angle (hook label counts) times our share of ads in that format, divided
        by our active ads.
A gap is a cell where they put 3 percent or more of their ads and we put none. A gap becomes a brief:
the angle, the format spec, the pages that run it (signals for layout and mood only) and our proof
for the angle from the brain. A gap with no proof in the brain says so and asks for the proof first.
"""
from __future__ import annotations

FORMATS = ["video", "image", "carousel", "dynamic", "catalog"]
GAP_MIN = 0.03          # their share of ads in a cell before an empty cell of ours counts as a gap
OVER_X = 1.5            # our share this many times theirs: far ahead, check the spend is not wasted
RULE_MIN = 0.03          # a gap this big, with proof on file, becomes an audit finding (COMP-R05)
RULE_TOP = 3
FORMAT_SPEC = {
    "video": "15 to 30 seconds. Say the proof in the first 3 seconds. Captions on.",
    "image": "1 static image. The proof is the headline. Product on a plain ground.",
    "carousel": "4 to 5 cards, one proof point a card, the pack on the last card.",
    "dynamic": "Dynamic creative: 3 first lines and 3 headlines, all carrying the proof.",
    "catalog": "Catalog ad with the proof line as the frame overlay.",
}
PROOF_WORDS = {
    "relief": ["compression", "arch", "relief", "support"], "comfort": ["comfort", "cushion", "arch", "seamless"],
    "durability": ["guarantee", "last"], "performance": ["blister", "arch", "athletic", "performance"],
    "fit": ["seamless", "blister", "stay"], "material": ["merino", "cotton", "wool"], "style": ["color", "colour", "style"],
    "proof": ["review", "rated", "stars"], "giving": ["donat", "given", "giving"], "gifting": ["gift"],
}


def proof_points(brain) -> list[str]:
    out = []
    for key in ("positioning.proof_points",):
        v = (brain.get(f"{brain.brand}.{key}") or {}).get("value")
        if isinstance(v, list):
            out += [str(x) for x in v]
    for key in ("offers.gifting", "offers.guarantee", "identity.giving_model"):
        v = (brain.get(f"{brain.brand}.{key}") or {}).get("value")
        if isinstance(v, str):
            out.append(v)
    return out


def proof_for(points: list[str], angle: str) -> str | None:
    for p in points:
        if any(w in p.lower() for w in PROOF_WORDS.get(angle, [angle])):
            return p
    return None


def _cells_snapshot(rows: list[dict], angles: list[str]) -> tuple[dict, int]:
    total = len(rows)
    out = {a: {f: 0 for f in FORMATS} for a in angles}
    for r in rows:
        f = r["format"] if r["format"] in FORMATS else None
        if not f:
            continue
        for t in r["angles"]:
            if t["tag"] in out:
                out[t["tag"]][f] += 1
    return out, total


def matrix(pages: list[dict], angle_defs, snapshot: dict | None, brain, direct_only: bool = False) -> dict:
    keys = [a[0] for a in angle_defs]
    labels = {a[0]: a[1] for a in angle_defs}
    us = next(p for p in pages if p["role"] == "self")
    comps = [p for p in pages if p["role"] != "self" and p["source"] != "none" and (not direct_only or p["frame"] == "direct")]
    estimated = not (snapshot and all(p["source"] == "snapshot" for p in comps + [us]))
    them = {a: {f: 0.0 for f in FORMATS} for a in keys}
    who = {a: {f: [] for f in FORMATS} for a in keys}
    their_total = 0
    if not estimated:
        rows = [r for r in snapshot["ads"] if r["role"] != "self" and any(r["page_id"] == p["page_id"] for p in comps)]
        counts, their_total = _cells_snapshot(rows, keys)
        for a in keys:
            for f in FORMATS:
                them[a][f] = counts[a][f]
        for p in comps:
            mine = [r for r in rows if r["page_id"] == p["page_id"]]
            for a in keys:
                for f in FORMATS:
                    if any(r["format"] == f and any(t["tag"] == a for t in r["angles"]) for r in mine):
                        who[a][f].append(p["name"])
        us_rows = [r for r in snapshot["ads"] if r["role"] == "self"]
        us_counts, us_total = _cells_snapshot(us_rows, keys)
    else:
        for p in comps:
            n = sum(p["formats"].values())
            tags = [t["tag"] for t in p["angles"] if t["tag"] in them]
            if not n:
                continue
            their_total += n
            for a in tags:
                for f in FORMATS:
                    v = p["formats"].get(f, 0)
                    if v:
                        them[a][f] += v / len(tags)
                        who[a][f].append(p["name"])
        us_total = us.get("active_ads") or 0
        fshare = us.get("format_mix") or {}
        us_counts = {a: {f: (us.get("angle_counts") or {}).get(a, 0) * fshare.get(f, 0) for f in FORMATS} for a in keys}
    points = proof_points(brain)
    cells, gaps = {}, []
    for a in keys:
        cells[a] = {}
        for f in FORMATS:
            t = round(them[a][f] / their_total, 3) if their_total else None
            u = round(us_counts[a][f] / us_total, 3) if us_total else None
            c = {"us": u, "them": t, "unit": "%", "n": len(who[a][f]), "pages": who[a][f]}
            kind = ""
            if t is not None and t >= GAP_MIN and not u:
                kind = "gap"
            elif u and t and u > t * OVER_X and u >= GAP_MIN:
                kind = "over"
            elif u and t and u >= t:
                kind = "lead"
            c["kind"] = kind
            if kind == "gap":
                proof = proof_for(points, a)
                c["gap_id"] = f"coverage_{a}_{f}"
                c["proof"] = proof
                c["brief"] = brief(labels[a], f, c, proof, us)
                gaps.append({"angle": a, "angle_label": labels[a], "format": f, "them": t, "us": u, "n": c["n"],
                             "pages": c["pages"], "proof": proof, "gap_id": c["gap_id"], "brief": c["brief"]})
            cells[a][f] = c
    gaps.sort(key=lambda g: (g["proof"] is None, -g["them"], -g["n"], g["angle"], g["format"]))
    rows = [{"key": a, "label": labels[a], "sub": _row_sub(us, a)} for a in keys]
    return {"rows": rows, "cols": [{"key": f, "label": f.capitalize()} for f in FORMATS], "cells": cells, "gaps": gaps,
            "estimated": estimated, "their_ads": their_total, "our_ads": us_total, "pages": [p["name"] for p in comps],
            "gap_min": GAP_MIN, "over_x": OVER_X}


def _row_sub(us: dict, a: str) -> str:
    n = (us.get("angle_counts") or {}).get(a)
    return f"{n} of our ads" if n else "not in our ads"


def brief(angle_label: str, fmt: str, c: dict, proof: str | None, us: dict) -> str:
    them = f"{round(c['them'] * 100, 1)} percent" if c["them"] is not None else "unavailable"
    lines = [f"Ad brief: {angle_label} as {fmt}.",
             f"Why: {c['n']} tracked pages run {angle_label.lower()} in {fmt}, about {them} of their ads. We run none.",
             f"Format: {FORMAT_SPEC[fmt]}",
             f"Our proof: {proof}." if proof else "Our proof: none in the brain yet. Add the proof record before this ad is made.",
             "Signals for layout and mood only: " + (", ".join(c["pages"][:4]) or "none") + ".",
             "Never copy their text, logos, products or faces."]
    return "\n".join(lines)
