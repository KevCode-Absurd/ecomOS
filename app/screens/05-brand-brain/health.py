"""Brain health for the brand brain screen: freshness by confidence per section, and connectors.

Reads only the brain (app/brain/<brand>/), the question bank and the sources registry. Every weak cell or
section ends in an action with an owner: re-crawl (agent, through the public source that fills the section),
ask the founder (agent drafts the question round, the founder answers), or connect (a person adds a
read-only source in Setup). Unavailable is never 0: a section with no records reads "no records", a source
that never pulled reads "never pulled".
"""
from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parents[1]
if str(APP / "brain") not in sys.path:
    sys.path.insert(0, str(APP / "brain"))

import keeper  # noqa: E402
from store import SECTIONS  # noqa: E402

# shelf life per section, days, from app/contracts/brand-brain.md section 4 (None: never expires)
SHELF_DAYS = {"identity": 180, "diagnosis": 90, "story_bank": 90, "voice": 60, "visual": 90, "products": 7, "offers": 1,
              "policies": 30, "claims": 30, "avatars": 30, "objections": 30, "objection_ladders": 30, "language_bank": 30,
              "competitors": 14, "positioning": 60, "channels": 30, "calendar": 30, "economics": 30, "operations": 30,
              "marketplaces": 14, "stack": 14, "site_map": 7, "content": 30, "seo_facts": 30, "team": 90, "decisions": None,
              "learnings": 90, "open_questions": None, "changes": None, "freshness": 1, "plans": 30, "assumptions": 30}
META_SECTIONS = {"freshness", "open_questions", "changes", "assumptions"}
TIERS = ["approved", "site_backed", "reported", "evidence", "inferred", "unverified", "forbidden"]
TIER_LABEL = {"approved": "Approved", "site_backed": "Site backed", "reported": "Reported", "evidence": "Evidence",
              "inferred": "Inferred", "unverified": "Unverified", "forbidden": "Forbidden"}
STRONG = {"approved", "site_backed", "reported"}
WEAK = {"inferred", "unverified"}
WEAK_SHARE = 0.5            # a section is weak when half or more of its records are inferred or unverified
RECRAWL_CAP = {"site": "BRN-C01", "meta_ad_library": "BRN-C11", "apify_meta_ad_library": "BRN-C11", "reddit": "BRN-C11", "apify_reddit": "BRN-C11"}


def rooms_by_section(bank: list[dict]) -> dict[str, set]:
    out: dict[str, set] = {}
    for q in bank:
        for f in q["fills"]:
            out.setdefault(f.split(".")[0], set()).update(q["unblocks_rooms"])
    return out


def sources_by_section(registry: dict) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    for sid, s in registry.items():
        for sec in s.get("fills_sections") or []:
            out.setdefault(sec, []).append({"id": sid, "name": s.get("name"), "access": s.get("access"), "category": s.get("category")})
    for sec in out:
        out[sec].sort(key=lambda s: (s["access"] != "public", s["id"]))
    return out


def _verdict(sec: str, st: dict, rooms: list[str], srcs: list[dict], empty_fields: list[str]) -> dict:
    """The one action for a section: connect, ask, recrawl or ok, with capability, owner and steps."""
    public = [s for s in srcs if s["access"] == "public"]
    private = [s for s in srcs if s["access"] != "public"]
    if st["records"] == 0:
        if private and rooms:
            names = ", ".join(s["name"] for s in private[:3])
            return {"kind": "connect", "text": "Connect", "capability": "BRN-C02", "owner": "person", "artefact": "connector_setup",
                    "reason": f"no records; {len(rooms)} rooms need it; {names} fill it",
                    "steps": [{"n": 1, "who": "person", "text": f"In Setup, connect one of: {names}. Read-only keys only."},
                              {"n": 2, "who": "agent", "text": f"Pull {sec.replace('_', ' ')} and propose records into the review queue."},
                              {"n": 3, "who": "person", "text": "Accept the proposed records. The rooms unblock on the next load."}]}
        if rooms:
            return {"kind": "ask", "text": "Ask the founder", "capability": "BRN-C07", "owner": "agent_drafts", "artefact": "brain_record",
                    "reason": f"no records and no source fills it; {len(rooms)} rooms need it",
                    "steps": [{"n": 1, "who": "agent", "text": f"Draft the questions for {sec.replace('_', ' ')}: {', '.join(f.split('.', 1)[-1].replace('_', ' ') for f in empty_fields[:4]) or 'the fields the rooms need'}."},
                              {"n": 2, "who": "person", "text": "Answer them in a line each in the open questions block."},
                              {"n": 3, "who": "agent", "text": "Write the answers as approved records. They win the merge."}]}
        return {"kind": "ok", "text": "Empty, unused", "capability": None, "owner": None, "artefact": None, "reason": "no records and no room needs it yet", "steps": []}
    if st["stale"] or (st["age_days"] is not None and st["shelf_days"] and st["age_days"] > st["shelf_days"]):
        src = public[0] if public else (private[0] if private else None)
        cap = RECRAWL_CAP.get(src["id"], "BRN-C02") if src else "BRN-C02"
        what = f"re-crawl through {src['name']}" if src else "refresh"
        return {"kind": "recrawl", "text": "Re-crawl", "capability": cap, "owner": "agent" if src and src["access"] == "public" else "person", "artefact": "brain_record",
                "reason": f"{st['stale']} stale of {st['records']}; newest record {st['age_days']} days old against a {st['shelf_days']} day shelf",
                "steps": [{"n": 1, "who": "agent", "text": f"Run the {what}, read-only, inside its caps. Estimate first if it is paid."},
                          {"n": 2, "who": "agent", "text": "Diff the new records against the current ones. Changes go to the review queue and the changes log."},
                          {"n": 3, "who": "person", "text": "Accept the changes. Stale records retire, never delete."}]}
    if st["weak_share"] is not None and st["weak_share"] >= WEAK_SHARE and rooms:
        return {"kind": "ask", "text": "Ask the founder", "capability": "BRN-C07", "owner": "agent_drafts", "artefact": "brain_record",
                "reason": f"{round(st['weak_share'] * 100)} percent inferred or unverified; {len(rooms)} rooms read it",
                "steps": [{"n": 1, "who": "agent", "text": f"List the {st['weak']} inferred or unverified {sec.replace('_', ' ')} records, best first."},
                          {"n": 2, "who": "person", "text": "Approve, edit or forbid each from the review panel. One line each."},
                          {"n": 3, "who": "agent", "text": "Approved records win the merge and flow to the rooms on the next load."}]}
    return {"kind": "ok", "text": "Fresh", "capability": None, "owner": None, "artefact": None,
            "reason": f"{st['records']} records, newest {st['age_days']} days old, {round((st['strong_share'] or 0) * 100)} percent approved, site backed or reported", "steps": []}


def heatmap(brain) -> dict:
    """Rows are sections, columns are tiers, cells are record counts. Each row carries freshness and its one action."""
    try:
        bank = keeper.load_bank()
    except (OSError, ValueError, KeyError):
        bank = []
    try:
        registry = keeper.load_registry()
    except (OSError, ValueError, KeyError):
        registry = {}
    rooms = rooms_by_section(bank)
    srcs = sources_by_section(registry)
    empty_by_sec: dict[str, list[str]] = {}
    try:
        for g in keeper.gaps(brain, bank):
            if g["kind"] == "empty":
                empty_by_sec.setdefault(g["section"], []).append(g["field"])
    except (OSError, ValueError, KeyError):
        pass
    rows, cells, sections = [], {}, []
    for sec in SECTIONS:
        if sec in META_SECTIONS:
            continue
        recs = brain.records(sec)
        counts = {t: 0 for t in TIERS}
        for r in recs:
            counts[r["tier"] if r["tier"] in counts else "unverified"] += 1
        ages = [r["age_days"] for r in recs if r["age_days"] is not None]
        confs = [r["confidence"] for r in recs if isinstance(r["confidence"], (int, float))]
        n = len(recs)
        st = {"records": n, "stale": sum(1 for r in recs if r["status"] == "stale"), "age_days": min(ages) if ages else None,
              "oldest_days": max(ages) if ages else None, "undated": n - len(ages), "shelf_days": SHELF_DAYS.get(sec),
              "confidence": round(sum(confs) / len(confs), 2) if confs else None,
              "strong": sum(counts[t] for t in STRONG), "weak": sum(counts[t] for t in WEAK),
              "strong_share": (sum(counts[t] for t in STRONG) / n) if n else None, "weak_share": (sum(counts[t] for t in WEAK) / n) if n else None}
        sec_rooms = sorted(rooms.get(sec, set()))
        v = _verdict(sec, st, sec_rooms, srcs.get(sec, []), empty_by_sec.get(sec, []))
        rows.append({"key": sec, "label": sec.replace("_", " "),
                     "sub": ("no records" if not n else f"{st['age_days']} d old" + (f", shelf {st['shelf_days']} d" if st["shelf_days"] else "") + (f", {st['stale']} stale" if st["stale"] else ""))})
        cells[sec] = {t: {"us": counts[t], "unit": "n"} for t in TIERS if counts[t] or n == 0 and t == "unverified"}
        if n == 0:
            cells[sec] = {}
        sections.append(dict(section=sec, label=sec.replace("_", " "), counts=counts, rooms=sec_rooms, sources=srcs.get(sec, [])[:4],
                             empty_fields=empty_by_sec.get(sec, []), verdict=v, **st))
    order = {"connect": 0, "ask": 1, "recrawl": 2, "ok": 3}
    sections.sort(key=lambda s: (order.get(s["verdict"]["kind"], 9), -(len(s["rooms"])), s["section"]))
    max_cell = max([c["us"] for row in cells.values() for c in row.values()] or [1])
    weak = [s for s in sections if s["verdict"]["kind"] != "ok"]
    return {"rows": rows, "cols": [{"key": t, "label": TIER_LABEL[t]} for t in TIERS], "cells": cells, "max": max_cell,
            "sections": sections, "counts": {"sections": len(sections), "weak": len(weak),
                                             "by_kind": {k: sum(1 for s in sections if s["verdict"]["kind"] == k) for k in order}},
            "records": sum(s["records"] for s in sections), "strong_share": (sum(s["strong"] for s in sections) / max(1, sum(s["records"] for s in sections))) if sections else None,
            "note": "Counts of active records by tier. Row order: connect first, then ask the founder, then re-crawl, then fresh. Shelf lives come from the brain contract."}


def records_in_cell(brain, section: str, tier: str) -> list[dict]:
    if section not in SECTIONS or tier not in TIERS:
        return []
    out = []
    for r in brain.records(section):
        if r["tier"] != tier:
            continue
        src = r.get("source") or {}
        out.append({"id": r["id"], "field": r.get("field"), "text": r.get("text") or (r["value"] if isinstance(r.get("value"), str) else json.dumps(r.get("value"))[:200]),
                    "tier": r["tier"], "date": None if r["date"] == "undated" else r["date"], "confidence": r["confidence"],
                    "source": {"type": src.get("type") or "none", "ref": src.get("ref") or ""}})
    out.sort(key=lambda r: (-(r["confidence"] or 0), r["id"]))
    return out


# ---------------------------------------------------------------- connectors

PUBLIC_LANES = {  # how a source in the registry shows up in the brand's sources.json (lane or extractor names)
    "site": ["own_site", "a-site"], "meta_ad_library": ["adlibrary", "b-adlibrary", "adlibrary-apify"], "apify_meta_ad_library": ["adlibrary-apify", "adlibrary"],
    "press": ["c-press"], "public_reviews": ["retailer", "amazon", "f-reviews"], "own_site_reviews": ["own_site", "f-reviews"],
    "amazon_listings_public": ["amazon", "amazon-apify"], "retailer_reviews": ["retailer"], "job_postings": ["e-job"],
    "reddit": ["reddit", "h-reddit", "reddit-apify"], "apify_reddit": ["reddit-apify", "reddit"], "apify_amazon_reviews": ["amazon-apify"],
}


def connectors(brain, today: dt.date | None = None) -> dict:
    """What is connected, what each fills, when it last pulled, and the connect action for what is not."""
    today = today or brain.today
    try:
        registry = keeper.load_registry()
    except (OSError, ValueError, KeyError):
        registry = {}
    src_rows = []
    try:
        src_rows = json.loads((brain.dir / "sources.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        src_rows = []
    by_lane: dict[str, list[dict]] = {}
    for r in src_rows:
        keys = set()
        if r.get("lane"):
            keys.add(str(r["lane"]))
        keys.update(str(x) for x in (r.get("extractors") or []))
        for k in keys:
            by_lane.setdefault(k, []).append(r)
    try:
        bank = keeper.load_bank()
    except (OSError, ValueError, KeyError):
        bank = []
    rooms = rooms_by_section(bank)
    docs = brain.documents()
    rows = []
    for sid, s in registry.items():
        lanes = PUBLIC_LANES.get(sid, [])
        pulls = [r for k in lanes for r in by_lane.get(k, [])]
        dates = [str(r.get("captured_at") or r.get("accessed") or "")[:10] for r in pulls if (r.get("captured_at") or r.get("accessed"))]
        failed = sum(1 for r in pulls if r.get("ok") is False or r.get("accessible") is False)
        last = max(dates) if dates else None
        age = (today - dt.date.fromisoformat(last)).days if last else None
        fills = s.get("fills_sections") or []
        unblocks = sorted({room for sec in fills for room in rooms.get(sec, set())})
        if sid == "upload":
            status = "connected" if docs else "not connected"
            last = max((str(d.get("added_at") or "")[:10] for d in docs), default=None) if docs else None
            age = (today - dt.date.fromisoformat(last)).days if last else None
        elif pulls:
            status = "connected"        # a paid or public source that has pulled into this brain
        elif s.get("access") == "public":
            status = "not pulled"
        else:
            status = "not connected"   # no private connector is live yet; a real key shows here when Setup has it
        shelf = min([SHELF_DAYS.get(sec) or 999 for sec in fills] or [None])
        rows.append({"id": sid, "name": s.get("name"), "category": s.get("category"), "access": s.get("access"), "status": status,
                     "fills_sections": fills, "fills_tables": s.get("fills_tables") or [], "unblocks_rooms": unblocks,
                     "pulls": len(pulls) if pulls else None, "failed": failed if pulls else None, "last_pull": last, "age_days": age,
                     "shelf_days": shelf if shelf != 999 else None, "read_only": s.get("read_only", True), "mock": s.get("mock"),
                     "health": (None if not pulls else round((len(pulls) - failed) / len(pulls), 2)),
                     "verdict": _connector_verdict(status, age, shelf if shelf != 999 else None, failed, len(pulls) if pulls else None, len(unblocks))})
    order = {"stop": 0, "fix": 1, "wait": 2, "keep": 3, "na": 4}
    rows.sort(key=lambda r: (order.get(r["verdict"]["kind"], 9), -len(r["unblocks_rooms"]), r["category"] or "", r["id"]))
    cats: dict[str, dict] = {}
    for r in rows:
        c = cats.setdefault(r["category"] or "other", {"category": r["category"] or "other", "sources": 0, "connected": 0, "unblocks_rooms": set()})
        c["sources"] += 1
        c["connected"] += 1 if r["status"] == "connected" else 0
        c["unblocks_rooms"].update(r["unblocks_rooms"])
    categories = []
    for c in cats.values():
        members = [r for r in rows if (r["category"] or "other") == c["category"]]
        live = [r for r in members if r["status"] == "connected"]
        fills = sorted({sec for r in members for sec in r["fills_sections"]})
        last = max((r["last_pull"] for r in live if r["last_pull"]), default=None)
        age = (today - dt.date.fromisoformat(last)).days if last else None
        rooms_n = len(c["unblocks_rooms"])
        if live:
            v = {"kind": "keep", "text": "Connected", "reason": "via " + ", ".join(r["name"] for r in live[:3])}
            if any(r["verdict"]["kind"] == "fix" for r in live):
                v = {"kind": "fix", "text": "Fix", "reason": "; ".join(r["name"] + ": " + r["verdict"]["reason"] for r in live if r["verdict"]["kind"] == "fix")}
        elif all(r["access"] == "public" for r in members):
            v = {"kind": "wait", "text": "Not pulled", "reason": "public, the brain has not read it yet"}
        elif rooms_n:
            v = {"kind": "stop" if rooms_n >= 4 else "wait", "text": "Connect one", "reason": f"unblocks {rooms_n} rooms; pick one of {len(members)}"}
        else:
            v = {"kind": "na", "text": "Optional", "reason": "no room waits on it"}
        categories.append({"category": c["category"], "label": c["category"].replace("_", " "), "sources": c["sources"], "connected": c["connected"],
                           "via": [r["name"] for r in live], "alternatives": [{"id": r["id"], "name": r["name"], "access": r["access"]} for r in members],
                           "fills_sections": fills, "unblocks_rooms": sorted(c["unblocks_rooms"]), "last_pull": last, "age_days": age, "verdict": v,
                           "steps": _connect_steps(c["category"], [r["name"] for r in members], fills) if not live else []})
    order = {"stop": 0, "fix": 1, "wait": 2, "keep": 3, "na": 4}
    categories.sort(key=lambda c: (order.get(c["verdict"]["kind"], 9), -len(c["unblocks_rooms"]), c["category"]))
    connected = [r for r in rows if r["status"] == "connected"]
    return {"sources": rows, "categories": categories,
            "counts": {"sources": len(rows), "connected": len(connected), "public": sum(1 for r in rows if r["access"] == "public"),
                       "categories_with_a_connection": sum(1 for c in categories if c["connected"])},
            "health_pct": (round(sum(r["health"] for r in connected if r["health"] is not None) / max(1, sum(1 for r in connected if r["health"] is not None)), 2) if any(r["health"] is not None for r in connected) else None),
            "note": "Public sources show their last pull from the brain's source log. Private connectors need a read-only key in Setup; none is live for the sample brand, so their fields read unavailable, never 0."}


def _connect_steps(category: str, names: list[str], fills: list[str]) -> list[dict]:
    pick = ", ".join(names[:4]) + (" or another in the list" if len(names) > 4 else "")
    return [{"n": 1, "who": "person", "text": f"In Setup, pick the {category.replace('_', ' ')} source you use: {pick}. Paste a read-only key. Keys never touch a page."},
            {"n": 2, "who": "agent", "text": "Run the first pull in mock, then live, inside the caps. Fill the tables it owns."},
            {"n": 3, "who": "agent", "text": f"Propose records into the review queue for {', '.join(x.replace('_', ' ') for x in fills[:4]) or 'its sections'}. Rules waiting on this source run again."},
            {"n": 4, "who": "person", "text": "Accept the proposed records. The rooms it unblocks show the numbers on their next load."}]


def _connector_verdict(status: str, age: int | None, shelf: int | None, failed: int, pulls: int | None, rooms_n: int) -> dict:
    if status == "connected":
        if pulls and failed and failed / pulls > 0.1:
            return {"kind": "fix", "text": "Failing", "reason": f"{failed} of {pulls} pulls failed"}
        if age is not None and shelf and age > shelf:
            return {"kind": "fix", "text": "Stale", "reason": f"last pull {age} days ago, shelf {shelf} days"}
        return {"kind": "keep", "text": "Connected", "reason": f"last pull {age} days ago" if age is not None else "connected"}
    if status == "not pulled":
        return {"kind": "wait", "text": "Not pulled", "reason": "a public source the brain has not read yet"}
    if rooms_n:
        return {"kind": "stop" if rooms_n >= 4 else "wait", "text": "Connect", "reason": f"unblocks {rooms_n} rooms"}
    return {"kind": "na", "text": "Optional", "reason": "no room waits on it"}
