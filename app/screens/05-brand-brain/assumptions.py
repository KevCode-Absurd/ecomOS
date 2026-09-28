"""Assumptions register: the numbers the simulation and the diagnosis run on, and which ones only a founder can confirm.

Reads app/brain/<brand>/assumptions.json (written by the brand's calibrate.py: field, value, status founder or sourced or
modelled or derived, unit, as_of, source record ids, reasoning). The effective status is founder when an approved founder
record exists on the first source id; otherwise the file's status. A modelled or sourced assumption that rooms read is
the finding BRN-R21 in audit.py. Confirm writes the current value as an approved founder record on the source id;
correct writes a new value. The generator's input file is never edited here.
"""
from __future__ import annotations

import datetime as dt
import json

STATUS_ORDER = {"modelled": 0, "sourced": 1, "derived": 2, "founder": 3}
STATUS_TEXT = {"modelled": "Modelled, needs your number", "sourced": "From public sources, confirm", "derived": "Derived from other records", "founder": "Confirmed by you"}
STATUS_KIND = {"modelled": "fix", "sourced": "watch", "derived": "keep", "founder": "keep"}


def _summary(v) -> str:
    if isinstance(v, dict):
        keys = [k for k in v if k not in ("history", "series", "monthly_index")]
        return ", ".join(f"{k.replace('_', ' ')} {v[k]}" for k in keys[:4] if not isinstance(v[k], (dict, list))) or json.dumps(v)[:120]
    if isinstance(v, list):
        return ", ".join(str(x if not isinstance(x, dict) else x.get("name") or json.dumps(x)[:30]) for x in v[:5])
    return str(v)


def load(brain) -> list[dict]:
    p = brain.dir / "assumptions.json"
    try:
        rows = json.loads(p.read_text(encoding="utf-8")) if p.is_file() else []
    except (OSError, ValueError):
        rows = []
    return [r for r in rows if isinstance(r, dict) and r.get("field")]


def register(brain, rooms_by_section: dict | None = None) -> dict:
    rooms_by_section = rooms_by_section or {}
    founder = {r["id"]: r for r in brain.records() if r["tier"] == "approved" and (r.get("source") or {}).get("type") == "founder"}
    rows = []
    for a in load(brain):
        sids = a.get("source_ids") or []
        first = sids[0] if sids else None
        fr = founder.get(first) if first else None
        status = "founder" if fr else (a.get("status") if a.get("status") in STATUS_ORDER else "derived")
        section = first.split(".")[1] if first and first.count(".") >= 2 else "economics"
        rooms = sorted(rooms_by_section.get(section, set()))
        age = None
        try:
            as_of = str(a.get("as_of") or "")
            age = (brain.today - dt.date.fromisoformat(as_of if len(as_of) == 10 else as_of + "-01")).days if as_of else None
        except ValueError:
            age = None
        rows.append({"field": a["field"], "label": a["field"].replace("_", " "), "status": status, "file_status": a.get("status"), "unit": a.get("unit"),
                     "as_of": a.get("as_of"), "age_days": age, "value": a.get("value"), "summary": _summary(fr.get("value") if fr else a.get("value")),
                     "source_ids": sids, "source_refs": (a.get("source_refs") or [])[:3], "reasoning": a.get("reasoning") or a.get("note"),
                     "confirmed_record": fr["id"] if fr else None, "confirmed_on": (fr["date"] if fr and fr["date"] != "undated" else None),
                     "rooms": rooms, "target": first,
                     "verdict": {"kind": STATUS_KIND[status], "text": STATUS_TEXT[status], "reason": (a.get("reasoning") or "")[:140]}})
    rows.sort(key=lambda r: (STATUS_ORDER[r["status"]], -len(r["rooms"]), r["field"]))
    counts = {s: sum(1 for r in rows if r["status"] == s) for s in STATUS_ORDER}
    return {"assumptions": rows, "counts": counts, "total": len(rows),
            "note": "The numbers the simulated tables and the diagnosis are built on. Modelled means a benchmark stood in for your number; confirm or correct it and the rooms that read it recompute on the next generator run."}
