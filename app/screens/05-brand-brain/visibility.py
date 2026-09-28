"""Public and private audit: what in the brain is marked public that should stay inside, what is private that came
from public sources, and what a public-facing agent would read.

Every record carries a visibility (public or private; the store defaults it from the source type: site, ad library,
press, review and interview records are public, everything else private). Two mismatches are flagged, in code:
1. leak: a record marked public whose source is not a public one (a connector number, a founder answer, an agent
   synthesis, a document, a ticket) in a section that is private by nature (economics, decisions, team, operations,
   learnings, channels, plans). A public-facing agent would read it. Severity medium.
2. over-restricted: a record marked private that came from a public source in a section that is public by nature
   (identity, products, offers, policies, claims, positioning, calendar, visual, voice). Public-facing agents lose a
   fact anyone can read on the site. Severity low.
A fix flips the visibility on the record (the source and value stay; the change is logged). The public preview is the
T0 card built with public records only, so the founder sees what a public-facing capability gets. Rule BRN-R28.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BRAIN_DIR = HERE.parents[1] / "brain"
if str(BRAIN_DIR) not in sys.path:
    sys.path.insert(0, str(BRAIN_DIR))
from package import t0_card  # noqa: E402
from store import PUBLIC_SOURCES, SECTIONS  # noqa: E402

PRIVATE_BY_NATURE = {"economics", "decisions", "team", "operations", "learnings", "channels", "plans", "diagnosis", "open_questions", "assumptions"}
PUBLIC_BY_NATURE = {"identity", "products", "offers", "policies", "claims", "positioning", "calendar", "visual", "voice", "site_map", "seo_facts", "marketplaces", "story_bank"}
SKIP = {"freshness", "changes"}


def audit(brain) -> dict:
    leaks, restricted, by_section = [], [], {}
    for r in brain.records():
        sec = r["section"]
        if sec in SKIP:
            continue
        vis = r.get("visibility") or "private"
        src = (r.get("source") or {}).get("type")
        row = by_section.setdefault(sec, {"section": sec, "public": 0, "private": 0, "leaks": 0, "restricted": 0})
        row[vis] += 1
        item = {"id": r["id"], "section": sec, "field": r.get("field"), "source": src, "tier": r["tier"], "text": (r.get("text") or str(r.get("value")))[:140]}
        if vis == "public" and src not in PUBLIC_SOURCES and sec in PRIVATE_BY_NATURE:
            leaks.append(dict(item, fix="private", why=f"{(src or 'unknown').replace('_', ' ')} data in {sec.replace('_', ' ')} is not public information"))
            row["leaks"] += 1
        elif vis == "private" and src in PUBLIC_SOURCES and sec in PUBLIC_BY_NATURE:
            restricted.append(dict(item, fix="public", why=f"it came from {src.replace('_', ' ')}, which anyone can read"))
            row["restricted"] += 1
    rows = [by_section[s] for s in SECTIONS if s in by_section]
    pub = sum(r["public"] for r in rows)
    priv = sum(r["private"] for r in rows)
    try:
        preview = t0_card(brain, public=True)
    except Exception:  # noqa: BLE001
        preview = None
    return {"rows": rows, "leaks": leaks, "restricted": restricted, "preview": preview,
            "counts": {"public": pub, "private": priv, "leaks": len(leaks), "restricted": len(restricted), "public_share": round(pub / (pub + priv), 3) if pub + priv else None},
            "rules": {"public_sources": sorted(PUBLIC_SOURCES), "private_by_nature": sorted(PRIVATE_BY_NATURE), "public_by_nature": sorted(PUBLIC_BY_NATURE)},
            "note": "Public means a public-facing agent (a shopping assistant, a support bot, a page writer) may read it. The store marks site, ad library, press, review and interview records public and the rest private; this audit catches the records that landed on the wrong side. A fix flips the flag and logs it; nothing else changes."}


def set_visibility(brain, rid: str, visibility: str) -> dict | tuple[int, dict]:
    if visibility not in ("public", "private"):
        return 400, {"error": "visibility must be public or private"}
    parts = rid.split(".")
    if len(parts) < 3 or parts[1] not in SECTIONS:
        return 404, {"error": "no such record", "id": rid}
    raw = next((r for r in brain.raw(parts[1]) if r.get("id") == rid), None)
    if raw is None:
        return 404, {"error": "no such record", "id": rid}
    before = raw.get("visibility") or "private"
    if before == visibility:
        return {"id": rid, "visibility": visibility, "changed": False}
    new = dict(raw, visibility=visibility)
    errs = brain.put(new)
    if errs:
        return 400, {"error": "; ".join(errs)}
    return {"id": rid, "visibility": visibility, "before": before, "changed": True}
