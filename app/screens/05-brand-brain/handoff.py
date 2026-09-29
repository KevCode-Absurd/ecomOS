"""A hand-off pack for a named person: the brain in one page, the brand book, the red lines and the 10 questions,
in reading order, as one markdown file with the person's name and role on it, and a team record that says who got
what and when.

The pack is built from the same builders the package block uses, so it is true to the records on the day. The team
record `team.handoff_<name>` waits for that person's quiz: when their answers are scored with their name (feature
8.4 with `who`), the record takes the score and the date. Rule BRN-R39 keeps a hand-off on the master list while
the quiz is unanswered after 7 days, or answered under 70 percent.
"""
from __future__ import annotations

import datetime as dt
import re

QUIZ_DUE_DAYS = 7
PASS_PCT = 70


def slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", (name or "").lower()).strip("_")[:40]


def _embed(text: str) -> list[str]:
    """A document inside the pack: its title dropped, its headings one level down so the pack's own parts stay the parts."""
    out = []
    for ln in (text or "").splitlines():
        if ln.startswith("# "):
            continue
        out.append("#" + ln if ln.startswith("#") else ln)
    return out or ["unavailable"]


def build(brain, to: str, role: str, pieces: dict) -> dict:
    """pieces: {onepage: {text}, brandbook: {text}, redlines: [{phrase, reason}], quiz: {text, questions}, tokens: fn}."""
    name = pieces.get("name") or brain.brand.title()
    today = brain.today.isoformat()
    out = [f"# {name}: hand-off for {to}" + (f" ({role})" if role else ""), "",
           f"Prepared {today} from the brand brain, version {brain.version()}. Read in this order. Then answer the questions at the end and send them back; they are scored against the records, not against anyone's memory.", ""]
    out += ["## 1. The brain in one page", ""]
    out += _embed((pieces.get("onepage") or {}).get("text", ""))
    out += ["", "## 2. The brand book", ""]
    out += _embed((pieces.get("brandbook") or {}).get("text", ""))
    lines = pieces.get("redlines") or []
    out += ["", "## 3. The lines we never cross", ""]
    out += [f"- {x.get('phrase') or x.get('text')}" + (f": {x['reason']}" if x.get("reason") else "") for x in lines] or ["none on file"]
    q = pieces.get("quiz") or {}
    out += ["", "## 4. Your 10 questions", "", "Answer each in one line, in order, and send the list back to the founder. The answers are checked against the records."]
    out += [""] + (q.get("text", "").splitlines() or ["the brain holds no question yet"])
    text = "\n".join(out).rstrip() + "\n"
    return {"text": text, "tokens": pieces["tokens"](text) if pieces.get("tokens") else None, "to": to, "role": role, "key": slug(to), "name": name,
            "pieces": {"onepage": bool((pieces.get("onepage") or {}).get("text")), "brandbook": bool((pieces.get("brandbook") or {}).get("text")), "redlines": len(lines), "quiz": len(q.get("questions") or [])},
            "sections": [ln[3:] for ln in out if ln.startswith("## ")], "version": brain.version(),
            "note": "One file, true to the records today. Their quiz answers, scored with their name, close the hand-off."}


def record(brain, pack: dict) -> dict:
    today = brain.today.isoformat()
    return {"id": f"{brain.brand}.team.handoff_{pack['key']}", "brand": brain.brand, "section": "team", "field": f"handoff_{pack['key']}",
            "value": {"to": pack["to"], "role": pack.get("role") or None, "on": today, "version": pack["version"], "pieces": pack["pieces"], "quiz_questions": pack["pieces"]["quiz"],
                      "checked_on": None, "score": None, "of": None, "pct": None},
            "text": f"Hand-off to {pack['to']}" + (f" ({pack['role']})" if pack.get("role") else "") + f" on {today}: one page, brand book, {pack['pieces']['redlines']} red lines and {pack['pieces']['quiz']} questions. Quiz not answered yet.",
            "tier": "approved", "confidence": 1.0, "visibility": "private",
            "source": {"type": "founder", "ref": "05-brand-brain hand-off", "captured_at": today}}


def handoffs(brain) -> list[dict]:
    out = []
    for r in brain.records("team"):
        if not (r.get("field") or "").startswith("handoff_") or not isinstance(r.get("value"), dict):
            continue
        v = r["value"]
        on = v.get("on")
        due = (dt.date.fromisoformat(on) + dt.timedelta(days=QUIZ_DUE_DAYS)).isoformat() if on else None
        days = (brain.today - dt.date.fromisoformat(on)).days if on else None
        if v.get("checked_on"):
            state = "passed" if (v.get("pct") or 0) >= PASS_PCT else "failed"
        else:
            state = "overdue" if due and due < brain.today.isoformat() else "waiting"
        out.append({"record": r["id"], "key": r["field"][8:], "to": v.get("to"), "role": v.get("role"), "on": on, "days": days, "due": due, "state": state,
                    "checked_on": v.get("checked_on"), "score": v.get("score"), "of": v.get("of"), "pct": v.get("pct"), "misses": v.get("misses") or [], "version": v.get("version")})
    order = {"failed": 0, "overdue": 1, "waiting": 2, "passed": 3}
    out.sort(key=lambda x: (order[x["state"]], x["on"] or ""))
    return out


def scored(brain, who: str, result: dict) -> dict | None:
    """The hand-off record for `who` with the quiz result on it, or None when there is no hand-off for that name."""
    key = slug(who)
    if not key:
        return None
    raw = next((r for r in brain.raw("team") if r.get("field") == f"handoff_{key}" and r.get("status", "active") != "retired"), None)
    if raw is None or not isinstance(raw.get("value"), dict):
        return None
    today = brain.today.isoformat()
    v = dict(raw["value"], checked_on=today, score=result.get("score"), of=result.get("of"), pct=result.get("pct"),
             misses=[{"n": m.get("n"), "question": str(m.get("question"))[:100]} for m in (result.get("misses") or [])][:10])
    new = dict(raw, value=v, text=f"Hand-off to {v.get('to')}" + (f" ({v['role']})" if v.get("role") else "") + f" on {v.get('on')}: quiz scored {today}, {v['score']} of {v['of']} ({v['pct']} percent), " + ("passed." if (v["pct"] or 0) >= PASS_PCT else "under the bar; walk them through the misses."))
    return new
