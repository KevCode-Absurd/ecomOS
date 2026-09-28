"""Audience profiles every generator picks one of: the avatars as briefs, with the doubts each raises and the proof
that answers them, the founder's approval, and a default per surface.

Each avatar record (name, share estimate, job, triggers, pains, emotional driver, evidence quotes) becomes a profile
card: the doubts it raises come from the objection ladder rungs that name it, with each rung's proof status; the
surfaces from those rungs' uses; a one-paragraph line a generator reads. The founder approves a profile in the claims
desk (tier approved) and picks the default profile per surface (ads, email, pdp, cx, social) as a founder record
(`avatars.defaults`). The brain file lists the profiles under judgement rules with the defaults first, so every
generator writes for a named person. Rule BRN-R33: no approved profile, or no default for ads. Web pass idea 22.
"""
from __future__ import annotations

SURFACES = ("ads", "email", "pdp", "cx", "social")


def defaults(brain) -> dict:
    r = next((x for x in brain.records("avatars") if x.get("field") == "defaults" and isinstance(x.get("value"), dict)), None)
    return {k: v for k, v in (r["value"] if r else {}).items() if k in SURFACES and isinstance(v, str)}


def profiles(brain, ladderproof_mod=None) -> dict:
    rungs_by_avatar: dict[str, list[dict]] = {}
    if ladderproof_mod is not None:
        try:
            for lad in brain.records("objection_ladders"):
                v = lad.get("value") if isinstance(lad.get("value"), dict) else {}
                for rung in v.get("rungs") or []:
                    for aid in rung.get("avatars") or []:
                        proofs = [p for p in (rung.get("proof_ids") or []) if isinstance(p, str)]
                        rungs_by_avatar.setdefault(aid, []).append({"theme": v.get("theme"), "level": rung.get("level"), "doubt": rung.get("doubt"), "one_star": (rung.get("counts") or {}).get("one_star"), "has_proof": bool(proofs), "proof": rung.get("proof") if proofs else None, "uses": rung.get("uses") or []})
        except Exception:  # noqa: BLE001
            rungs_by_avatar = {}
    dflt = defaults(brain)
    notes = {r["field"][5:]: r for r in brain.records("avatars") if (r.get("field") or "").startswith("note_") and isinstance(r.get("value"), dict)}
    rows = []
    for r in brain.records("avatars"):
        if r.get("field") != "avatar" or not isinstance(r.get("value"), dict):
            continue
        v = r["value"]
        doubts = sorted(rungs_by_avatar.get(r["id"], []), key=lambda d: -(d.get("one_star") or 0))
        surfaces = sorted({u for d in doubts for u in d["uses"]})
        line = f"{v.get('name')}: wants {v.get('job')}." + (f" Buys when: {', '.join(v.get('triggers') or [])}." if v.get("triggers") else "") + (f" Fears: {', '.join(v.get('pains') or [])}." if v.get("pains") else "") + (f" Feels: {v.get('emotional_driver')}." if v.get("emotional_driver") else "")
        if doubts:
            line += " Doubts to answer: " + "; ".join(f"{d['doubt']}" + (" (proof on file)" if d["has_proof"] else " (no proof: do not claim it)") for d in doubts[:3]) + "."
        key = r["id"].rsplit(".", 1)[-1]
        note = notes.get(key)
        if note:
            line += f" Founder's note: {note['value'].get('note')}"
        rows.append({"note": note["value"].get("note") if note else None, "note_date": (None if not note or note["date"] == "undated" else note["date"]),"id": r["id"], "key": r["id"].rsplit(".", 1)[-1], "name": v.get("name"), "share": v.get("share_estimate"), "intensity": v.get("intensity"), "job": v.get("job"), "triggers": v.get("triggers") or [], "pains": v.get("pains") or [], "driver": v.get("emotional_driver"),
                     "tier": r["tier"], "approved": r["tier"] == "approved", "evidence": len(r.get("evidence") or []), "quote": ((r.get("evidence") or [{}])[0].get("quote") if r.get("evidence") else None), "doubts": doubts[:5], "surfaces": surfaces, "line": line,
                     "default_for": [s for s, aid in dflt.items() if aid == r["id"]], "source": (r.get("source") or {}).get("type"), "date": None if r["date"] == "undated" else r["date"]})
    rows.sort(key=lambda x: (-(x["share"] or 0), x["name"] or ""))
    return {"profiles": rows, "defaults": dflt, "surfaces": list(SURFACES),
            "counts": {"profiles": len(rows), "approved": sum(1 for x in rows if x["approved"]), "with_doubts": sum(1 for x in rows if x["doubts"]), "defaults_set": len(dflt), "share_covered": round(sum(x["share"] or 0 for x in rows), 2) if rows else None},
            "note": "Profiles are the avatar records, built from reviews; the doubts come from the ladder rungs that name each one. Approve a profile in the records browser or the claims desk, and pick the default per surface. Every generator writes for one named profile, the default unless the brief names another."}


def note_record(brain, key: str, note: str) -> dict | tuple[int, dict]:
    note = (note or "").strip()[:400]
    if not any(r["id"].rsplit(".", 1)[-1] == key and r.get("field") == "avatar" for r in brain.records("avatars")):
        return 404, {"error": "no avatar with that key", "key": key}
    name = next(((r.get("value") or {}).get("name") for r in brain.records("avatars") if r["id"].rsplit(".", 1)[-1] == key), key)
    return {"id": f"{brain.brand}.avatars.note_{key}", "brand": brain.brand, "section": "avatars", "field": f"note_{key}", "value": {"avatar": key, "note": note or None}, "text": f"Founder's note on {name}: {note}" if note else f"Founder's note on {name} cleared.",
            "tier": "approved", "confidence": 1.0, "visibility": "private", "source": {"type": "founder", "ref": "05-brand-brain audience profiles", "captured_at": brain.today.isoformat()}}


def set_default(brain, surface: str, avatar_id: str) -> dict | tuple[int, dict]:
    if surface not in SURFACES:
        return 400, {"error": "surface must be one of " + ", ".join(SURFACES)}
    if avatar_id and not any(r["id"] == avatar_id and r.get("field") == "avatar" for r in brain.records("avatars")):
        return 404, {"error": "no avatar with that id", "avatar_id": avatar_id}
    cur = defaults(brain)
    if avatar_id:
        cur[surface] = avatar_id
    else:
        cur.pop(surface, None)
    names = {r["id"]: (r.get("value") or {}).get("name") for r in brain.records("avatars") if r.get("field") == "avatar"}
    text = "Default audience per surface: " + ("; ".join(f"{s}: {names.get(a) or a}" for s, a in cur.items()) or "none set") + "."
    return {"id": f"{brain.brand}.avatars.defaults", "brand": brain.brand, "section": "avatars", "field": "defaults", "value": cur, "text": text, "tier": "approved", "confidence": 1.0, "visibility": "private",
            "source": {"type": "founder", "ref": "05-brand-brain audience profiles", "captured_at": brain.today.isoformat()}}
