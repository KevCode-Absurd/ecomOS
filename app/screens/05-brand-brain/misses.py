"""Questions the brain could not answer: every ask (from the founder or an agent) that found no record, kept as a
miss with who asked and when, grouped by question, so the founder sees what the brain is short of before an agent
writes around the gap.

A miss is decided in code: no typed answer (feature 6.7) with a fact or a yes, no can-we-say verdict except "not on
file", and either no matching record or none that matches half the question's words. Misses live in
`review/ask-misses.jsonl` under the brand folder, runtime state like the read log. A miss becomes an open question in
one click (the existing ask/open route) and then reads as opened. Rule BRN-R40 puts a miss asked twice in 30 days,
or asked by an agent, on the master list for the founder to answer.
"""
from __future__ import annotations

import datetime as dt
import json
import re

WINDOW_DAYS = 30
FILE = "ask-misses.jsonl"


def norm(q: str) -> str:
    return re.sub(r"[^a-z0-9 ]+", " ", (q or "").lower()).strip()


def is_miss(res: dict) -> bool:
    deep = res.get("deep") or {}
    if deep.get("verdict") in ("fact", "yes", "no"):
        return False
    cws = res.get("can_we_say") or {}
    if cws and cws.get("verdict") != "not_on_file":
        return False
    words = res.get("words") or []
    answers = res.get("answers") or []
    if not words:
        return False
    if not answers:
        return True
    best = max(len(a.get("matched") or []) for a in answers)
    return best / len(words) < 0.5


def log(brain, q: str, reader: str, res: dict) -> bool:
    """Append the miss; never raises. Returns True when the ask was a miss."""
    if not is_miss(res):
        return False
    try:
        p = brain.dir / "review" / FILE
        p.parent.mkdir(parents=True, exist_ok=True)
        row = {"q": (q or "").strip()[:300], "reader": (reader or "founder")[:80], "at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "day": brain.today.isoformat(),
               "matches": len(res.get("answers") or []), "words": res.get("words") or []}
        with p.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        return True
    except OSError:
        return True


def read(brain) -> list[dict]:
    p = brain.dir / "review" / FILE
    if not p.is_file():
        return []
    out = []
    for ln in p.read_text(encoding="utf-8").splitlines():
        try:
            out.append(json.loads(ln))
        except ValueError:
            continue
    return out


def _opened(brain) -> dict[str, dict]:
    out = {}
    for r in brain.records("open_questions"):
        v = r.get("value") if isinstance(r.get("value"), dict) else {}
        key = norm(v.get("question") or r.get("text") or "")
        if key:
            out[key] = {"record": r["id"], "answered_on": v.get("answered_on")}
    return out


def grouped(brain, days: int = WINDOW_DAYS) -> dict:
    rows = read(brain)
    since = (brain.today - dt.timedelta(days=days)).isoformat()
    opened = _opened(brain)
    groups: dict[str, dict] = {}
    for x in rows:
        if (x.get("day") or "") < since:
            continue
        key = norm(x.get("q"))
        if not key:
            continue
        g = groups.setdefault(key, {"key": key, "q": x.get("q"), "times": 0, "readers": [], "first": x.get("day"), "last": x.get("day"), "agent_asked": False})
        g["times"] += 1
        rd = x.get("reader") or "founder"
        if rd not in g["readers"]:
            g["readers"].append(rd)
        g["first"] = min(g["first"], x.get("day") or g["first"])
        g["last"] = max(g["last"], x.get("day") or g["last"])
        g["agent_asked"] = g["agent_asked"] or (rd != "founder" and not rd.startswith("founder"))
    out = []
    for g in groups.values():
        op = opened.get(g["key"])
        g["opened"] = op["record"] if op else None
        g["answered_on"] = op["answered_on"] if op else None
        g["state"] = "answered" if g["answered_on"] else ("opened" if op else "unanswered")
        g["due"] = g["state"] == "unanswered" and (g["times"] >= 2 or g["agent_asked"])
        out.append(g)
    out.sort(key=lambda g: (g["state"] != "unanswered", -g["times"], g["last"]), reverse=False)
    return {"misses": out, "counts": {"questions": len(out), "asks": sum(g["times"] for g in out), "unanswered": sum(1 for g in out if g["state"] == "unanswered"), "due": sum(1 for g in out if g["due"]), "by_agents": sum(1 for g in out if g["agent_asked"])},
            "days": days, "available": bool(rows) or (brain.dir / "review" / FILE).is_file(),
            "note": f"Every ask with no record behind it, in the last {days} days, grouped by question. Open one as a question and answer it in the profile; asked twice or asked by an agent, it is on the plan."}
