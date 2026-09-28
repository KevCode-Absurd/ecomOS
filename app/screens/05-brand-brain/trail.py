"""Who read what: the audit trail of reads on the brain, by reader and by section, and which facts each agent was
handed.

Two logs, both under the brand folder: the store's read log (`reads.log.jsonl`: section, reader, at), stamped by
every route that reads a section when the caller names itself with `?reader=`, and this screen's record-read log
(`review/agent-reads.jsonl`: reader, record ids, at), written when a package or a brain file is built for a
capability, because that is the moment an agent is handed facts. `weekly` sums both over the window: reads per
reader and section, the facts handed most often, private facts handed to public-facing readers (a cross-check with
the visibility audit), and one line per reader. Unavailable until something is logged. Web pass idea 24.
"""
from __future__ import annotations

import datetime as dt
import json

MAX_RECORDS_PER_LINE = 400


def log_records(brain, reader: str, record_ids: list[str], public_facing: bool = False) -> None:
    try:
        p = brain.dir / "review" / "agent-reads.jsonl"
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps({"reader": str(reader)[:80], "records": [str(x) for x in record_ids][:MAX_RECORDS_PER_LINE], "public_facing": bool(public_facing), "at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}) + "\n")
    except OSError:
        return


def record_reads(brain) -> list[dict]:
    p = brain.dir / "review" / "agent-reads.jsonl"
    if not p.is_file():
        return []
    out = []
    for ln in p.read_text(encoding="utf-8").splitlines():
        try:
            row = json.loads(ln)
        except ValueError:
            continue
        if isinstance(row, dict) and row.get("reader"):
            out.append(row)
    return out


def _kind(reader: str) -> str:
    if reader[:2].isdigit() and "-" in reader:
        return "screen"
    if "-C" in reader and reader.split("-C")[0].isalpha():
        return "capability"
    return "other"


def weekly(brain, days: int = 7) -> dict:
    since = (brain.today - dt.timedelta(days=days)).isoformat()
    reads = [r for r in brain.reads() if str(r.get("at") or "")[:10] >= since]
    recs = [r for r in record_reads(brain) if str(r.get("at") or "")[:10] >= since]
    if not reads and not recs:
        return {"available": False, "days": days, "reason": "nothing read with a name in the window; screens and agents name themselves with ?reader=, and a package build logs the facts it hands over",
                "readers": [], "sections": [], "facts": [], "private_to_public": [], "counts": {"reads": 0, "readers": 0, "facts_handed": 0}}
    by_reader: dict[str, dict] = {}
    by_section: dict[str, dict] = {}
    for r in reads:
        rd = by_reader.setdefault(r["reader"], {"reader": r["reader"], "kind": _kind(r["reader"]), "reads": 0, "sections": set(), "last": None, "facts": 0, "public_facing": False})
        rd["reads"] += 1
        rd["sections"].add(r.get("section"))
        rd["last"] = max(rd["last"] or "", r.get("at") or "")
        sc = by_section.setdefault(r.get("section"), {"section": r.get("section"), "reads": 0, "readers": set(), "last": None})
        sc["reads"] += 1
        sc["readers"].add(r["reader"])
        sc["last"] = max(sc["last"] or "", r.get("at") or "")
    fact_count: dict[str, dict] = {}
    active = {r["id"]: r for r in brain.records()}
    private_to_public = []
    for row in recs:
        rd = by_reader.setdefault(row["reader"], {"reader": row["reader"], "kind": _kind(row["reader"]), "reads": 0, "sections": set(), "last": None, "facts": 0, "public_facing": False})
        rd["facts"] += len(row.get("records") or [])
        rd["public_facing"] = rd["public_facing"] or bool(row.get("public_facing"))
        rd["last"] = max(rd["last"] or "", row.get("at") or "")
        for rid in row.get("records") or []:
            fc = fact_count.setdefault(rid, {"id": rid, "times": 0, "readers": set(), "section": rid.split(".")[1] if rid.count(".") >= 2 else None})
            fc["times"] += 1
            fc["readers"].add(row["reader"])
            rec = active.get(rid)
            if row.get("public_facing") and rec is not None and rec.get("visibility") == "private":
                private_to_public.append({"id": rid, "reader": row["reader"], "at": row.get("at")})
    readers = sorted(({**v, "sections": sorted(x for x in v["sections"] if x)} for v in by_reader.values()), key=lambda v: (-(v["reads"] + v["facts"]), v["reader"]))
    sections = sorted(({**v, "readers": sorted(v["readers"])} for v in by_section.values()), key=lambda v: (-v["reads"], v["section"] or ""))
    facts = sorted(({**v, "readers": sorted(v["readers"]), "text": (active.get(v["id"]) or {}).get("text") or None, "tier": (active.get(v["id"]) or {}).get("tier"), "still_active": v["id"] in active} for v in fact_count.values()), key=lambda v: (-v["times"], v["id"]))
    lines = [f"Reads on the brain, last {days} days: {len(reads)} section reads by {len(readers)} readers; {sum(v['facts'] for v in readers)} facts handed to agents."]
    for v in readers[:8]:
        lines.append(f"- {v['reader']} ({v['kind']}): {v['reads']} section reads" + (f", {v['facts']} facts" if v["facts"] else "") + (f"; sections {', '.join(v['sections'][:5])}" if v["sections"] else ""))
    if facts:
        lines.append("Facts handed most: " + "; ".join(f"{f['id']} ({f['times']})" for f in facts[:5]))
    if private_to_public:
        lines.append(f"Private facts handed to a public-facing reader: {len(private_to_public)}. Check the visibility audit.")
    return {"available": True, "days": days, "since": since, "readers": readers, "sections": sections, "facts": facts[:60], "private_to_public": private_to_public[:20],
            "counts": {"reads": len(reads), "readers": len(readers), "facts_handed": sum(v["facts"] for v in readers), "distinct_facts": len(facts), "private_to_public": len(private_to_public)},
            "text": "\n".join(lines), "note": "Section reads come from the store's read log; facts handed come from package and brain file builds, logged under the capability. A reader that does not name itself is not here. Review it weekly; a fact handed to many agents is one to keep right."}
