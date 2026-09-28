"""Hand-offs this screen owes other screens (app/contracts/events.md).

competitor_snapshot (read by 02-customers-avatars, 09-creative, 04-offers-pricing): one row per tracked page
with the fields those screens need: verdict and points, active ads, format mix, angle tags, offers seen,
price band per unit, map quadrant on each claim axis, longest ad, capture date and source. Public signals
only, never ad text. Until the shared table exists in the data layer it is written to
fixtures/competitor_snapshot_<brand>.json (served read-only at /screens/03-competitors/fixtures/...) by
capture.py, so a reader never calls this screen's code.

experiments (for 25-experiments): every open action whose artefact is a test becomes a registry row in the
contract shape with status "proposed" once a decision approves it; this screen only drafts the rows.
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "fixtures"
FIELDS = ["brand", "competitor", "page_id", "frame", "verdict", "points", "active_ads", "format_mix", "angles", "offers_seen",
          "price_low", "price_median", "price_high", "price_unit", "quadrant_durability", "quadrant_comfort", "longest_days",
          "captured_at", "source", "simulated"]


def snapshot_rows(m: dict, parse_band) -> list[dict]:
    split = m["category_median"]
    comps = {c["name"]: c for c in m["competitors"]}
    rows = []
    for p in m["pages"]:
        if p["role"] == "self" or p["source"] == "none":
            continue
        band = parse_band(p.get("price_text"))
        c = next((v for k, v in comps.items() if k.lower()[:8] == p["name"].lower()[:8]), None)
        def quad(axis, mx):
            if not c or band["median"] is None or split is None:
                return None
            return f"{'higher' if band['median'] >= split else 'lower'} price, {'strong' if c[axis] >= mx / 2 else 'weak'} {axis}"
        rows.append({"brand": m["brand"], "competitor": p["name"], "page_id": p["page_id"], "frame": p["frame"],
                     "verdict": (p.get("verdict") or {}).get("text"), "points": (p.get("verdict") or {}).get("points"),
                     "active_ads": p["active_ads"], "format_mix": p["format_mix"], "angles": sorted({a["tag"] for a in p["angles"]}),
                     "offers_seen": p.get("offers_seen") or [], "price_low": band["low"], "price_median": band["median"],
                     "price_high": band["high"], "price_unit": (m.get("term") or {}).get("unit"),
                     "quadrant_durability": quad("durability", 3), "quadrant_comfort": quad("comfort", 3),
                     "longest_days": p.get("longest_days"), "captured_at": p.get("captured_at"), "source": p["source"],
                     "simulated": False})
    return rows


def write_snapshot(m: dict, parse_band, folder: Path | None = None) -> Path:
    path = (folder or OUT) / f"competitor_snapshot_{m['brand']}.json"
    path.write_text(json.dumps({"table": "competitor_snapshot", "brand": m["brand"], "fields": FIELDS,
                                "note": "Public signals only. Never ad text. Read-only hand-off; see app/contracts/events.md.",
                                "rows": snapshot_rows(m, parse_band)}, indent=1, sort_keys=True), encoding="utf-8")
    return path


def experiment_rows(actions: list[dict], brand: str) -> list[dict]:
    """Registry rows (events.md shape) drafted from open test actions. Ids are drafts; 25-experiments assigns EXP-nnn."""
    out = []
    for a in actions:
        if a["artefact"]["kind"] != "test_brief" or a.get("status") == "unavailable":
            continue
        out.append({"id": None, "draft_id": a["id"], "brand": brand, "hypothesis": a["title"],
                    "source": {"type": "finding", "ref": a["finding_ids"][0], "index": None}, "idea_id": None, "owner": a["owner"],
                    "metric": None, "variant": {"control": "current", "treatment": a["artefact"]["label"]}, "audience": [],
                    "start": None, "read_point": a.get("check_on"), "end": None, "status": "proposed", "result": None, "decision": None,
                    "learnings_ref": None, "retro": None, "park": None, "brain_refs": a.get("brain_refs") or [],
                    "win_rule": a.get("win_rule"), "stop_rule": a.get("stop_rule")})
    return out
