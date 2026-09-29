"""The round-over-round report: this founder round against the last one, in numbers from the records and the
runtime logs, as one copyable page. What got done and carried, how trust moved, what was written (edits, answers,
approvals, source reviews, retires, undos, saves over a contradiction), and what is still open (contradictions to
settle, questions with no answer, hand-offs waiting on a quiz, expiries this week). Nothing here judges; each line
says where the number came from. Unavailable stays unavailable (a trust line needs 2 points, a previous round needs
a closed one).
"""
from __future__ import annotations

import datetime as dt

WRITE_KINDS = ("founder_edit", "answer", "approve", "source_review", "retired", "undo", "override", "settled", "handoff", "number", "confirm", "correction")


def _week(key: str) -> tuple[str, str]:
    start = dt.date.fromisoformat(key)
    return start.isoformat(), (start + dt.timedelta(days=6)).isoformat()


def previous_round(brain, current_key: str) -> dict | None:
    rounds = []
    for r in brain.records("team", include_retired=True):
        v = r.get("value") if isinstance(r.get("value"), dict) else {}
        if (r.get("field") or "").startswith("round_") and v.get("round") and v["round"] < current_key and r.get("field") != "round_schedule":
            rounds.append((v["round"], v, r["id"]))
    if not rounds:
        return None
    key, v, rid = max(rounds, key=lambda x: x[0])
    closed = next((d for d in brain.records("decisions") if (d.get("field") or "") == f"round_{key.replace('-', '')}_closed"), None)
    cv = closed.get("value") if closed and isinstance(closed.get("value"), dict) else {}
    return {"round": key, "record": rid, "ticked": sum(1 for k, t in (v.get("ticked") or {}).items() if t), "closed_on": v.get("closed_on"),
            "done": cv.get("done") or [], "carried": cv.get("carried") or [], "summary": v.get("summary")}


def _count_kinds(rows: list[dict], start: str, end: str) -> dict:
    out = {k: 0 for k in WRITE_KINDS}
    total = 0
    for x in rows:
        d = x.get("date") or ""
        if start <= d <= end:
            total += 1
            if x.get("kind") in out:
                out[x["kind"]] += 1
    return {"total": total, "by_kind": {k: n for k, n in out.items() if n}}


def _trust_at(points: list[dict], on_or_before: str) -> dict | None:
    cands = [p for p in points if (p.get("date") or "") <= on_or_before]
    return cands[-1] if cands else None


def build(brain, current: dict, trust_points: list[dict], changes_rows: list[dict], open_now: dict) -> dict:
    key = current["round"]
    start, end = _week(key)
    prev = previous_round(brain, key)
    prev_week = _week(prev["round"]) if prev else None
    writes_now = _count_kinds(changes_rows, start, end)
    writes_prev = _count_kinds(changes_rows, *prev_week) if prev_week else None
    t_now = trust_points[-1] if trust_points else None
    t_start = _trust_at(trust_points, (dt.date.fromisoformat(start) - dt.timedelta(days=1)).isoformat()) if trust_points else None
    trust = None
    if t_now and t_start and t_now is not t_start and t_now.get("overall") is not None and t_start.get("overall") is not None:
        movers = []
        for sec, val in (t_now.get("sections") or {}).items():
            was = (t_start.get("sections") or {}).get(sec)
            if isinstance(val, (int, float)) and isinstance(was, (int, float)) and val != was:
                movers.append({"section": sec, "from": was, "to": val, "delta": round(val - was, 1)})
        movers.sort(key=lambda m: -abs(m["delta"]))
        trust = {"from": t_start["overall"], "to": t_now["overall"], "delta": round(t_now["overall"] - t_start["overall"], 1), "from_date": t_start["date"], "to_date": t_now["date"], "movers": movers[:5]}
    lines = [f"# Founder round of {key}: the report", "", f"Built {brain.today.isoformat()} from the records and the logs. Compared with the round of {prev['round']}." if prev else f"Built {brain.today.isoformat()} from the records and the logs. No earlier round on file to compare with.", ""]
    lines += ["## This round", "", f"- {current['counts']['done']} of {current['counts']['items']} items done, {current['counts']['left']} left" + (f", closed {current['closed_on']}" if current.get("closed") else ", still open")]
    if prev:
        lines += ["", "## Last round", "", f"- {prev['ticked']} items ticked" + (f", closed {prev['closed_on']}" if prev["closed_on"] else ", never closed") + (f", {len(prev['carried'])} carried over" if prev["carried"] else "")]
        lines += [f"  - carried: {c}" for c in prev["carried"][:5]]
    lines += ["", "## Trust", ""]
    lines.append(f"- Brain trust {trust['from']} to {trust['to']} ({'+' if trust['delta'] >= 0 else ''}{trust['delta']}) between {trust['from_date']} and {trust['to_date']}" if trust else "- unavailable: the trust line needs a point before this round and one since (the trust block writes one a day it runs)")
    if trust and trust["movers"]:
        lines += [f"  - {m['section'].replace('_', ' ')}: {m['from']} to {m['to']}" for m in trust["movers"]]
    lines += ["", "## Written this round", "", f"- {writes_now['total']} changes logged" + (f" (last round {writes_prev['total']})" if writes_prev else "")]
    lines += [f"  - {k.replace('_', ' ')}: {n}" for k, n in writes_now["by_kind"].items()]
    lines += ["", "## Still open", ""]
    for label, n in open_now.items():
        lines.append(f"- {label}: {n if n is not None else 'unavailable'}")
    text = "\n".join(lines) + "\n"
    return {"round": key, "week": {"start": start, "end": end}, "previous": prev, "this": {"done": current["counts"]["done"], "items": current["counts"]["items"], "left": current["counts"]["left"], "closed": current.get("closed"), "closed_on": current.get("closed_on")},
            "trust": trust, "writes": {"this": writes_now, "previous": writes_prev}, "open": open_now, "text": text,
            "note": "This round against the last, in numbers from the records and the logs. Copy it into the round note or the digest. A line that says unavailable needs its source to run first."}
