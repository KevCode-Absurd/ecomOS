"""What is new for a reader since its last read: an agent or a screen that built a package before gets, next time,
the records added to that package, the ones gone from it, and the ones changed since the day of its last read,
with the change lines. It reads the agent-reads log (which records were handed to whom, when) and the changes list;
nothing here is judgement. A reader that never built the package reads unavailable.
"""
from __future__ import annotations

import datetime as dt


def last_read(reads: list[dict], reader: str) -> dict | None:
    mine = [r for r in reads if r.get("reader") == reader]
    return mine[-1] if mine else None


def build(brain, reader: str, capability: str, current_ids: list[str], reads: list[dict], changes_rows: list[dict]) -> dict:
    lr = last_read(reads, reader)
    if lr is None:
        return {"available": False, "reader": reader, "capability": capability, "reason": f"{reader} has not built a package on this brain yet; the first build is the baseline", "current": len(current_ids)}
    at = str(lr.get("at") or "")
    read_day = at[:10] if at else None
    since_day = min(read_day, brain.today.isoformat()) if read_day else brain.today.isoformat()
    then = set(lr.get("records") or [])
    now = list(current_ids)
    added = [i for i in now if i not in then]
    gone = sorted(i for i in then if i not in set(now))
    changed = []
    seen = set()
    for x in changes_rows:
        rid = x.get("record")
        if not rid or rid not in set(now) or rid in added or (x.get("date") or "") < since_day or x.get("undone"):
            continue
        if rid in seen:
            continue
        seen.add(rid)
        changed.append({"id": rid, "kind": x.get("kind"), "what": x.get("what"), "before": x.get("before"), "after": x.get("after"), "date": x.get("date")})
    lines = [f"# What is new for {reader} on {capability}", "", f"Since your last read on {read_day or 'an unknown day'}: {len(added)} added, {len(gone)} gone, {len(changed)} changed. Read these first; the rest of the package is as you had it.", ""]
    if added:
        lines += ["## Added", ""] + [f"- {i}" for i in added[:40]] + [""]
    if gone:
        lines += ["## Gone (retired or no longer in scope)", ""] + [f"- {i}" for i in gone[:40]] + [""]
    if changed:
        lines += ["## Changed", ""] + [f"- {c['id']}: {c['what']}" + (f" (before: {c['before']})" if c.get("before") is not None else "") for c in changed[:40]] + [""]
    if not (added or gone or changed):
        lines += ["Nothing changed for you.", ""]
    return {"available": True, "reader": reader, "capability": capability, "last_read_at": at or None, "since_day": since_day, "then": len(then), "now": len(now),
            "added": added, "gone": gone, "changed": changed, "counts": {"added": len(added), "gone": len(gone), "changed": len(changed)}, "text": "\n".join(lines).rstrip() + "\n",
            "note": "Added and gone come from the records handed at the last read against the package now; changed comes from the changes list on or after the day of that read."}
