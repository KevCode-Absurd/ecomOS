"""A snapshot before every bulk move, and a restore from it. Before a source approve or retire, a section undo, a
restore from an export or a batch of answers from a note, the touched sections are written as a small export bundle
under `review/snapshots/`, so the move can be undone as a whole through the same restore planner an export uses
(re-add what went missing, change what moved, retire what was added; a dry run first, nothing deleted). The newest
30 snapshots are kept.
"""
from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path

FORMAT = "ecomOS brain export v1"
KEEP = 30


def folder(brain) -> Path:
    return brain.dir / "review" / "snapshots"


def take(brain, sections: list[str], reason: str) -> dict | None:
    """Write the bundle; never raises (a failed snapshot must not block the move). Returns {file, sections, records} or None."""
    secs = [s for s in dict.fromkeys(sections) if s and (brain.dir / f"{s}.json").is_file()]
    if not secs:
        return None
    try:
        now = dt.datetime.now(dt.timezone.utc)
        slug = re.sub(r"[^a-z0-9]+", "-", (reason or "move").lower()).strip("-")[:40] or "move"
        name = f"{brain.today.isoformat()}-{now.strftime('%H%M%S')}-{slug}.json"
        bundle = {"format": FORMAT, "brand": brain.brand, "exported_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "version": brain.version(), "reason": (reason or "")[:200],
                  "snapshot": True, "sections": {s: brain.raw(s) for s in secs}}
        folder(brain).mkdir(parents=True, exist_ok=True)
        (folder(brain) / name).write_text(json.dumps(bundle, ensure_ascii=False), encoding="utf-8")
        _prune(brain)
        return {"file": name, "sections": secs, "records": sum(len(v) for v in bundle["sections"].values())}
    except OSError:
        return None


def _prune(brain) -> None:
    files = sorted(folder(brain).glob("*.json"))
    for p in files[:-KEEP] if len(files) > KEEP else []:
        try:
            p.unlink()
        except OSError:
            pass


def listing(brain) -> dict:
    rows = []
    if folder(brain).is_dir():
        for p in sorted(folder(brain).glob("*.json"), reverse=True):
            try:
                b = json.loads(p.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            rows.append({"file": p.name, "taken_at": b.get("exported_at"), "reason": b.get("reason"), "version": b.get("version"), "sections": sorted((b.get("sections") or {}).keys()),
                         "records": sum(len(v) for v in (b.get("sections") or {}).values() if isinstance(v, list))})
    return {"snapshots": rows, "counts": {"snapshots": len(rows)}, "keep": KEEP,
            "note": "Taken before every bulk move: a source approve or retire, a section undo, a restore from an export, a batch of answers from a note. Restore a section from one through the same planner an export uses; the restore itself takes a snapshot first."}


def load(brain, name: str) -> dict | None:
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{6}-[a-z0-9-]{1,40}\.json", name or ""):
        return None
    p = folder(brain) / name
    if not p.is_file():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
