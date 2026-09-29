"""Undo from the changes list: one click on a logged change puts the brain back the way it was before that change,
without deleting anything.

Each change row names a record and, for a value change, the value before. Undo works out in code what reverses it:
a value change restores the earlier value from the record's history (a founder record, so the value it replaces
joins the history too); an approve or forbid puts the tier and the source back to what `was`; a record the change
created is retired; a retire is lifted. A batch line (a source review, a document read) cannot be undone in one
step and says so: undo each record from its history instead. An undone change is marked, so it is never undone
twice, and the undo is itself a logged change.
"""
from __future__ import annotations

import re

CREATE_KINDS = {"founder_edit", "answer", "remember", "audience", "reason", "owner", "rule", "lock", "asset", "consent", "peak", "number", "override", "brand", "logo", "correction", "proof", "confirm", "visibility", "example", "snippet", "page_id", "permission", "contract"}


def _derived(was: dict) -> list[str]:
    """The record ids an agent or inferred source was derived from: kept under `was` at approve, else parsed from its ref."""
    if isinstance(was.get("derived_from"), list) and was["derived_from"]:
        return [str(x) for x in was["derived_from"]]
    return re.findall(r"[a-z0-9_-]+\.[a-z_]+\.[A-Za-z0-9_.-]+", str(was.get("ref") or ""))


def _raw(brain, rid: str):
    parts = (rid or "").split(".")
    if len(parts) < 3:
        return None
    return next((r for r in brain.raw(parts[1]) if r.get("id") == rid), None)


def plan(brain, row: dict, changes_mod, assume_value: str | None = None) -> dict:
    """What undoing this change would do: {can, how, index, reason, record}. `assume_value` is the record's value once
    newer lines are undone first (the section undo plans in sequence)."""
    kind, rid = row.get("kind"), row.get("record")
    out = {"change": row.get("id"), "record": rid, "kind": kind, "can": False, "how": None, "reason": None}
    if row.get("undone"):
        out["reason"] = f"already undone on {row['undone']}"
        return out
    if not rid or rid.split(".")[1:2] == ["changes"]:
        out["reason"] = "this line names no record to put back"
        return out
    if kind in ("approve",) and row.get("record", "").split(".")[1:2] == ["team"] and "source_review" in rid:
        out["reason"] = "a source review approves many records at once: undo each from its history"
        return out
    raw = _raw(brain, rid)
    if raw is None:
        out["reason"] = "the record is gone from the brain"
        return out
    src = raw.get("source") or {}
    hist = raw.get("history") or []
    if kind == "retired":
        if raw.get("status") == "retired":
            out.update(can=True, how="unretire", reason=f"bring {rid} back as active")
        else:
            out["reason"] = "the record is already active"
        return out
    if raw.get("status") == "retired":
        out["reason"] = "the record is retired; bring it back from its own history first"
        return out
    if kind in ("approve", "forbid") and isinstance(src.get("was"), dict) and src["was"].get("tier") and src["was"].get("tier") != raw.get("tier"):
        was = src["was"]
        if was.get("type") in ("agent", "inferred") and not _derived(was):
            out["reason"] = "the earlier source was an agent's and its record list was lost at approve; edit the record instead"
            return out
        out.update(can=True, how="tier", tier=was["tier"], reason=f"put the tier back to {was['tier']} with its {was.get('type') or 'earlier'} source")
        return out
    before, after = row.get("before"), row.get("after")
    if before is not None and after is not None:
        now = assume_value if assume_value is not None else changes_mod._short(raw.get("value"))
        if now != after:
            out["reason"] = f"the value moved on since this change (now {now}); restore from the record's history instead"
            return out
        idx = next((i for i in range(len(hist) - 1, -1, -1) if changes_mod._short(hist[i].get("value")) == before), None)
        if idx is None:
            out["reason"] = "the earlier value is not in the record's history"
            return out
        out.update(can=True, how="restore", index=idx, reason=f"put {before} back in place of {after}")
        return out
    if before is None and kind in CREATE_KINDS and not hist:
        out.update(can=True, how="retire", reason=f"retire {rid}, which this change created; it stays in the file")
        return out
    out["reason"] = "nothing in code reverses this line; edit the record instead"
    return out


def apply(brain, row: dict, changes_mod, history_mod, founder_put) -> dict | tuple[int, dict]:
    p = plan(brain, row, changes_mod)
    if not p["can"]:
        return 400, {"error": "cannot undo: " + str(p["reason"]), "plan": p}
    rid = p["record"]
    raw = _raw(brain, rid)
    today = brain.today.isoformat()
    if p["how"] == "restore":
        res = history_mod.restore(brain, rid, p["index"])
        if isinstance(res, tuple):
            return res
        errs = founder_put(brain, res["record"], "undo", f"undo of {row.get('id')}: {rid} back to {res['after']} from {res['before']}")
        if errs:
            return 400, {"error": "; ".join(errs)}
        result = {"before": res["before"], "after": res["after"]}
    elif p["how"] == "tier":
        was = raw["source"]["was"]
        hist = list(raw.get("history") or []) + [{"value": raw.get("value"), "changed_at": today, "source_ref": raw["source"].get("ref") or "", "tier": raw.get("tier"), "reason": f"undo of {row.get('kind')}"}]
        source = {"type": was.get("type") or "founder", "ref": was.get("ref") or raw["source"].get("ref"), "captured_at": raw["source"].get("captured_at") or today}
        if source["type"] in ("agent", "inferred"):
            source["derived_from"] = _derived(was)
        new = dict(raw, tier=was["tier"], history=hist, source=source)
        new.pop("confidence", None) if was.get("tier") != "approved" else None
        before_v = brain.version()
        errs = brain.put(new)
        if errs:
            return 400, {"error": "; ".join(errs)}
        changes_mod.log(brain, "undo", raw["section"], rid, f"undo of {row.get('id')}: {rid} tier back to {was['tier']} from {raw.get('tier')}", before=raw.get("tier"), after=was["tier"])
        changes_mod.version_step(brain, before_v, f"undo {row.get('id')}")
        result = {"before": raw.get("tier"), "after": was["tier"]}
    elif p["how"] == "retire":
        before_v = brain.version()
        brain.retire(rid)
        changes_mod.log(brain, "undo", raw["section"], rid, f"undo of {row.get('id')}: {rid} retired, it was created by that change")
        changes_mod.version_step(brain, before_v, f"undo {row.get('id')}")
        result = {"before": "active", "after": "retired"}
    else:
        before_v = brain.version()
        new = dict(raw, status="active")
        errs = brain.put(new)
        if errs:
            return 400, {"error": "; ".join(errs)}
        changes_mod.log(brain, "undo", raw["section"], rid, f"undo of {row.get('id')}: {rid} brought back as active")
        changes_mod.version_step(brain, before_v, f"undo {row.get('id')}")
        result = {"before": "retired", "after": "active"}
    _mark(brain, row.get("id"), today)
    return dict(result, ok=True, how=p["how"], record=rid, change=row.get("id"), next="Undone. The undo is on the list too, so it can be seen and reversed in turn.")


def _mark(brain, change_id: str, today: str) -> None:
    for c in brain.raw("changes"):
        if c.get("id") == change_id and isinstance(c.get("value"), dict):
            c["value"]["undone"] = today
            brain.put(c)
            return


# ---------------------------------------------------------------- a section back to a time (9.2)

def section_rows(rows: list[dict], section: str, since: str) -> list[dict]:
    """The changes in one section on or after a date, newest first, not yet undone."""
    out = [x for x in rows if x.get("section") == section and (x.get("date") or "") >= since and not x.get("undone")]
    out.sort(key=lambda x: ((x.get("date") or ""), x["id"]), reverse=True)
    return out


def section_plan(brain, rows: list[dict], section: str, since: str, changes_mod) -> dict:
    picked = section_rows(rows, section, since)
    plans, value_after = [], {}
    for x in picked:
        pl = plan(brain, x, changes_mod, assume_value=value_after.get(x.get("record")))
        if pl["can"] and pl["how"] == "restore":
            value_after[x["record"]] = x.get("before")  # once this line is undone, the record reads its before value
        plans.append(dict(pl, what=x.get("what"), date=x.get("date"), label=x.get("label")))
    can = [p for p in plans if p["can"]]
    return {"section": section, "since": since, "lines": plans, "counts": {"lines": len(plans), "can": len(can), "cannot": len(plans) - len(can)},
            "records": sorted({p["record"] for p in can if p.get("record")}),
            "note": "Newest first, so each undo sees the state the one after it left. A line that cannot be undone says why and is skipped; the rest still go back."}


def section_apply(brain, rows: list[dict], section: str, since: str, changes_mod, history_mod, founder_put) -> dict:
    picked = section_rows(rows, section, since)
    done, skipped = [], []
    for x in picked:
        res = apply(brain, x, changes_mod, history_mod, founder_put)
        if isinstance(res, tuple):
            skipped.append({"change": x["id"], "reason": res[1].get("error")})
        else:
            done.append({"change": x["id"], "record": res["record"], "how": res["how"]})
    return {"ok": True, "section": section, "since": since, "undone": done, "skipped": skipped, "counts": {"undone": len(done), "skipped": len(skipped)},
            "next": (f"{len(done)} change{'s' if len(done) != 1 else ''} in {section.replace('_', ' ')} undone back to {since}" + (f"; {len(skipped)} skipped, each with its reason" if skipped else "") + ". Every undo is on the list and can be undone in turn.")}
