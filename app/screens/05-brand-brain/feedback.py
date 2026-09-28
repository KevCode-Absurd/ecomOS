"""What agents got wrong: a founder's correction of an agent's output becomes a learning agents read, and the fact it
misused goes to review.

A correction carries the capability that wrote it, the wrong line, what was wrong, the right line when the founder
gives one, and the record the agent misused when one is named. It is written as a learnings record
(`learnings.agent_wrong_<n>`), the brain file lists the recent corrections under strict rules so the same slip is
not repeated, and the misused record gets a review flag (`team.review_now_<section>`, read by the owners block as
overdue today). The trail can then show which agents were handed that fact. Nothing here retrains anything: it is a
record an agent reads before writing, and a review a person does.
"""
from __future__ import annotations

import re

KINDS = ("wrong_fact", "wrong_tone", "forbidden_said", "made_up", "off_audience", "other")


def corrections(brain) -> list[dict]:
    out = []
    for r in brain.records("learnings"):
        if (r.get("field") or "").startswith("agent_wrong_") and isinstance(r.get("value"), dict):
            v = r["value"]
            out.append({"record": r["id"], "capability": v.get("capability"), "kind": v.get("kind"), "wrong": v.get("wrong"), "what": v.get("what"), "right": v.get("right"), "fact": v.get("fact"), "date": None if r["date"] == "undated" else r["date"]})
    out.sort(key=lambda x: (x["date"] or "", x["record"]), reverse=True)
    return out


def record(brain, body: dict, n: int) -> dict | tuple[int, dict]:
    wrong = str(body.get("wrong") or "").strip()[:400]
    what = str(body.get("what") or "").strip()[:300]
    if not wrong or not what:
        return 400, {"error": "wrong (the agent's line) and what (what was wrong) are required"}
    cap = str(body.get("capability") or "").strip().upper()[:20]
    if cap and not re.fullmatch(r"[A-Z]{2,6}-C\d{2,3}", cap):
        return 400, {"error": "capability must be an id like CREA-C06, or empty"}
    kind = str(body.get("kind") or "other")
    if kind not in KINDS:
        return 400, {"error": "kind must be one of " + ", ".join(KINDS)}
    fact = str(body.get("fact") or "").strip()[:160] or None
    if fact and not any(r["id"] == fact for r in brain.records()):
        return 404, {"error": "no active record with that id", "fact": fact}
    right = str(body.get("right") or "").strip()[:400] or None
    v = {"capability": cap or None, "kind": kind, "wrong": wrong, "what": what, "right": right, "fact": fact}
    text = (f"{cap} " if cap else "An agent ") + f"wrote \"{wrong[:120]}\": {what}" + (f" Write instead: \"{right[:120]}\"" if right else "") + (f" (misused {fact})" if fact else "")
    return {"id": f"{brain.brand}.learnings.agent_wrong_{n:03d}", "brand": brain.brand, "section": "learnings", "field": f"agent_wrong_{n:03d}", "value": v, "text": text, "tier": "approved", "confidence": 1.0, "visibility": "private",
            "source": {"type": "founder", "ref": "05-brand-brain what agents got wrong", "captured_at": brain.today.isoformat()}, "evidence": [{"quote": wrong[:300], "ref": f"agent output, {brain.today.isoformat()}"}]}


def summary(brain) -> dict:
    cs = corrections(brain)
    by_cap: dict[str, int] = {}
    by_kind: dict[str, int] = {}
    for c in cs:
        by_cap[c["capability"] or "unnamed"] = by_cap.get(c["capability"] or "unnamed", 0) + 1
        by_kind[c["kind"] or "other"] = by_kind.get(c["kind"] or "other", 0) + 1
    return {"corrections": cs[:100], "counts": {"total": len(cs), "by_capability": by_cap, "by_kind": by_kind, "with_fact": sum(1 for c in cs if c["fact"])},
            "kinds": list(KINDS), "note": "Every correction is a learning agents read before writing, listed in the brain file. Name the record the agent misused and it goes to review today; the trail shows who else was handed it."}
