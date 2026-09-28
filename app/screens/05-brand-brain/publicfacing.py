"""Public-facing preview per capability: what an agent that talks to customers gets, and what it loses.

The overlay flags a capability as public-facing; until it does, the founder can flag one here as a founder record
(`team.public_capabilities`, a list of capability ids), and the package and brain file routes honour it. The preview
builds the package twice, as it stands and as public-facing, and lists what the public version leaves out: the T2
records dropped (private ones), the T1 summaries that changed, the tokens saved, and whether the brand card itself
changed. A leak is a private record the public version would still carry; the package builder never carries one, so
the preview reads 0 leaks and says so. Capability LOOP-C22 owns access; this screen owns the flag until the overlay
carries it (a contract ask).
"""
from __future__ import annotations

import re


def flagged(brain) -> list[str]:
    r = next((x for x in brain.records("team") if x.get("field") == "public_capabilities"), None)
    v = r.get("value") if r else None
    return [str(c) for c in v if isinstance(c, str)] if isinstance(v, list) else []


def is_public(brain, cap_id: str, overlay_cap: dict) -> tuple[bool, str]:
    if overlay_cap.get("public_facing"):
        return True, "overlay"
    if cap_id in flagged(brain):
        return True, "founder"
    return False, "none"


def flag_record(brain, caps: list[str]) -> dict:
    caps = sorted({c.strip().upper() for c in caps if re.fullmatch(r"[A-Z]{2,6}-C\d{2,3}", str(c).strip().upper())})
    return {"id": f"{brain.brand}.team.public_capabilities", "brand": brain.brand, "section": "team", "field": "public_capabilities", "value": caps,
            "text": ("Public-facing capabilities (private records left out of their packages): " + ", ".join(caps) + ".") if caps else "No capability flagged public-facing by the founder.",
            "tier": "approved", "confidence": 1.0, "visibility": "private", "source": {"type": "founder", "ref": "05-brand-brain public-facing preview", "captured_at": brain.today.isoformat()}}


def preview(brain, cap_id: str, package_mod, root) -> dict | tuple[int, dict]:
    try:
        cap = package_mod.resolve(cap_id)
    except KeyError as exc:
        return 404, {"error": str(exc), "capability": cap_id}
    normal = package_mod.package(brain.brand, dict(cap, public_facing=False), root=root, today=brain.today, use_cache=False)
    public = package_mod.package(brain.brand, dict(cap, public_facing=True), root=root, today=brain.today, use_cache=False)
    n_ids = {r["id"] for r in normal["records"]}
    p_ids = {r["id"] for r in public["records"]}
    active = {r["id"]: r for r in brain.records()}
    dropped = [{"id": rid, "section": rid.split(".")[1], "text": (active.get(rid) or {}).get("text") or "", "visibility": (active.get(rid) or {}).get("visibility")} for rid in sorted(n_ids - p_ids)]
    t1_normal = {p.get("section"): p["text"] for p in normal["parts"] if p["tier"] == "T1"}
    t1_public = {p.get("section"): p["text"] for p in public["parts"] if p["tier"] == "T1"}
    changed = [s for s in t1_normal if t1_public.get(s) != t1_normal[s]]
    t0_changed = normal["parts"][0]["text"] != public["parts"][0]["text"]
    leaks = [r["id"] for r in public["records"] if (active.get(r["id"]) or {}).get("visibility") == "private"]
    is_pub, why = is_public(brain, cap_id, cap)
    return {"capability": cap_id, "public_facing": is_pub, "flagged_by": why, "tokens": {"normal": normal["tokens"], "public": public["tokens"], "saved": normal["tokens"] - public["tokens"]},
            "records": {"normal": len(n_ids), "public": len(p_ids), "dropped": dropped}, "summaries_changed": changed, "brand_card_changed": t0_changed, "leaks": leaks,
            "text": public["text"], "note": "Built twice, as it stands and as public-facing. Dropped records are the private ones a customer-facing agent never reads; a changed summary is one that was written from private records. Leaks read 0 because the builder never carries a private record into a public package; the visibility audit is where a wrong flag is fixed."}
