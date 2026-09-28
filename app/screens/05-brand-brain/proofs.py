"""Proof requests for claims not yet approved: what would move each claim to approved, who can confirm it, drafted.

Every claim below approved (site backed, reported, evidence, inferred, unverified) is used somewhere: the ladder
rungs that cite it and the surfaces those rungs feed. The request names the evidence that earns approval by the
claim's category (a spec sheet or test for a material claim, the policy page and its terms for a guarantee, the
impact count for a donation claim, the certificate for a certification, the source page and a person for the rest),
the person who can confirm it, and the weight (the one-star lines behind the rungs that use it). Confirming writes
the evidence onto the record and approves it; the scanner stops flagging it as unapproved. Capability BRN-C03.
"""
from __future__ import annotations

EVIDENCE = [
    (("material", "comfort", "construction", "fabric"), "a spec sheet, a lab test or the factory's material declaration", "product"),
    (("guarantee", "return", "refund", "warranty"), "the policy page as published and the terms behind it", "customer experience"),
    (("donat", "giving", "mission", "charity"), "the impact count and the last partner report", "impact"),
    (("certif", "b corp", "organic", "recycled"), "the certificate and its expiry", "operations"),
    (("price", "value", "cheap", "afford"), "the price list and the compare-at proof", "finance"),
]


def _evidence_for(category: str, text: str) -> tuple[str, str]:
    hay = f"{category} {text}".lower()
    for words, ev, who in EVIDENCE:
        if any(w in hay for w in words):
            return ev, who
    return "the source page and a person who can confirm it in writing", "the founder"


def requests(brain, desk: dict, ladders: list[dict]) -> dict:
    one_star = {}
    for lad in ladders:
        v = lad.get("value") if isinstance(lad.get("value"), dict) else {}
        for rung in v.get("rungs") or []:
            for pid in rung.get("proof_ids") or []:
                one_star[pid] = one_star.get(pid, 0) + ((rung.get("counts") or {}).get("one_star") or 0)
    rows = []
    for c in desk.get("claims") or []:
        if c["tier"] in ("approved", "forbidden"):
            continue
        ev, who = _evidence_for(str(c.get("category") or ""), str(c.get("text") or ""))
        used = c.get("used_by") or []
        surfaces = sorted({u for x in used for u in (x.get("uses") or [])})
        weight = one_star.get(c["id"], 0)
        src = c.get("source") or {}
        draft = (f"Proof request: {c['text'][:200]}\n\nWhy: this claim answers {len(used)} doubt{'s' if len(used) != 1 else ''} on the ladder" + (f" with {weight} one-star lines behind them" if weight else "") + f", and runs on {', '.join(surfaces) or 'copy'}. Today it is {c['tier'].replace('_', ' ')}" + (f" from {src.get('ref')}" if src.get("ref") else "") + ".\n\n"
                 f"What we need from {who}: {ev}. One file or one line in writing is enough.\n\nWhen it lands: the claim is approved with the evidence on the record; the scanner stops flagging it; every surface may say it.")
        rows.append({"id": c["id"], "text": c["text"], "tier": c["tier"], "category": c.get("category"), "used_by": len(used), "surfaces": surfaces, "one_star": weight, "evidence": ev, "who": who, "source_ref": src.get("ref"), "draft": draft})
    rows.sort(key=lambda r: (-r["one_star"], -r["used_by"], r["id"]))
    return {"requests": rows, "counts": {"claims": len(rows), "used": sum(1 for r in rows if r["used_by"]), "one_star": sum(r["one_star"] for r in rows)},
            "note": "One request per claim below approved, ranked by the one-star lines behind the doubts it answers. Send the request to the person named; put the evidence on the record here and the claim is approved."}


def approve_with_evidence(brain, rid: str, evidence: str, ref: str | None) -> dict | tuple[int, dict]:
    evidence = (evidence or "").strip()[:400]
    if len(evidence) < 4:
        return 400, {"error": "evidence is required: what you saw, in a line"}
    raw = next((r for r in brain.raw("claims") if r.get("id") == rid), None)
    if raw is None:
        return 404, {"error": "no such claim", "id": rid}
    if raw.get("tier") == "forbidden":
        return 400, {"error": "a forbidden claim is not approved with evidence; unforbid it first", "id": rid}
    was = {"type": (raw.get("source") or {}).get("type"), "ref": (raw.get("source") or {}).get("ref"), "tier": raw.get("tier")}
    ev = list(raw.get("evidence") or []) + [{"quote": evidence, "ref": (ref or "").strip()[:200] or f"founder, {brain.today.isoformat()}"}]
    rec = dict(raw, tier="approved", confidence=1.0, status="active", evidence=ev, source={"type": "founder", "ref": f"05-brand-brain proof request for {rid}", "captured_at": brain.today.isoformat(), "was": was})
    rec.pop("expires_at", None)
    return {"record": rec, "was": was["tier"]}
