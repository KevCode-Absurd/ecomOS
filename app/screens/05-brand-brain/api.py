"""Brand brain screen API: /api/05-brand-brain/...

Reads app/brain/<brand>/ through app/brain/store.py and keeper.py. The only
writes go through Brain.put and Brain.retire: a founder answer to an open
question, and accept or ignore on a proposed record. Nothing external.

  GET  overview                 T0 card, section table, tiles, insights, chart, ladders,
                                open questions, review queue, conflicts
  GET  records?section=<name>   one section's records with tier, date, source and evidence
  GET  audit                    findings from audit.py (app/contracts/audit.md shape)
  POST questions/<field>        {answer}: writes a founder record, marks the question answered
  POST review/<record id>       {choice: accept | ignore}

Query `brand` (default bombas) and `today` (YYYY-MM-DD, default the real date)
work on every route. Set BRAIN_ROOT to point at a copy of app/brain (tests do).
"""
from __future__ import annotations

import datetime as dt
import importlib.util
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parents[1]
if str(APP / "brain") not in sys.path:
    sys.path.insert(0, str(APP / "brain"))

import keeper  # noqa: E402
from package import t0_card  # noqa: E402
from store import SECTIONS, Brain  # noqa: E402

BRAIN_ROOT: Path | None = None
SAFE_BRAND = re.compile(r"^[a-z0-9_-]+$")
QUESTION_ROUND_AT = 4
CHART_DAYS = 30
SIMULATED_NOTE = ("Bombas is the sample brand. Brain records come from public sources. "
                  "Every sales and ad number in ecomOS is simulated.")
META_SECTIONS = {"freshness", "open_questions", "changes"}

_spec = importlib.util.spec_from_file_location("brand_brain_audit", HERE / "audit.py")
audit = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(audit)


def _brain(req) -> Brain:
    brand = req.arg("brand", "bombas")
    if not SAFE_BRAND.match(brand):
        raise ValueError("bad brand")
    t = req.arg("today")
    today = dt.date.fromisoformat(t) if t else dt.date.today()
    return Brain(brand, BRAIN_ROOT, today)


def _source(r: dict) -> dict:
    s = r.get("source") or {}
    ref = s.get("ref") or ""
    return {"type": s.get("type") or "none", "ref": ref, "link": ref if ref.startswith("http") else None}


def record_view(r: dict) -> dict:
    return {"id": r["id"], "field": r.get("field"), "text": r.get("text") or (
                r["value"] if isinstance(r.get("value"), str) else json.dumps(r.get("value"))[:300]),
            "tier": r["tier"], "status": r["status"], "date": r["date"], "age_days": r["age_days"],
            "confidence": r["confidence"], "visibility": r["visibility"], "source": _source(r),
            "evidence": [{"quote": e.get("quote"), "ref": e.get("ref")} for e in (r.get("evidence") or [])]}


def section_table(brain: Brain) -> list[dict]:
    stats = brain.section_stats()
    out = []
    for sec in SECTIONS:
        st = stats[sec]
        confs = [r["confidence"] for r in brain.records(sec) if isinstance(r["confidence"], (int, float))]
        age = (brain.today - dt.date.fromisoformat(st["last_update"])).days if st["last_update"] else None
        out.append({"section": sec, "records": st["count"], "last_update": st["last_update"],
                    "freshness_days": age, "stale": st["stale"],
                    "confidence": round(sum(confs) / len(confs), 2) if confs else None,
                    "meta": sec in META_SECTIONS})
    return out


def open_questions(brain: Brain, bank: list[dict]) -> list[dict]:
    out = []
    for oq in brain.records("open_questions"):
        v = oq.get("value") or {}
        out.append({"id": oq["id"], "field": oq["field"], "question": v.get("question") or oq.get("text"),
                    "section": v.get("section"), "why": v.get("why"), "who_can_answer": v.get("who_can_answer"),
                    "answered_on": v.get("answered_on"), "answer_record": v.get("answer_record"),
                    "weight": audit.question_weight(oq, bank)})
    out.sort(key=lambda q: (bool(q["answered_on"]), -q["weight"], q["field"]))
    return out


def conflicts(brain: Brain) -> list[dict]:
    path = brain.dir / "review" / "conflicts.json"
    rows = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    return [c for c in rows if c.get("status", "open") == "open"]


def review_queue(brain: Brain) -> list[dict]:
    return [dict(record_view(r), section=r["section"])
            for r in brain.records(include_retired=True) if r["status"] == "proposed"]


def ladders(brain: Brain) -> list[dict]:
    out = []
    for lad in brain.records("objection_ladders"):
        v = lad.get("value") or {}
        rungs = [{"level": r.get("level"), "doubt": r.get("doubt"), "one_star": (r.get("one_star") or [])[:2],
                  "five_star": (r.get("five_star") or [])[:1], "counts": r.get("counts") or {},
                  "proof": r.get("proof"), "proof_ids": r.get("proof_ids") or [], "uses": r.get("uses") or []}
                 for r in v.get("rungs") or []]
        out.append({"id": lad["id"], "theme": v.get("theme") or lad.get("field"), "rungs": rungs,
                    "date": lad["date"], "tier": lad["tier"]})
    return out


def chart(brain: Brain) -> dict:
    """Records added per day: each record counts once, on its earliest known date."""
    first: dict[str, int] = {}
    undated = 0
    for r in brain.records(include_retired=True):
        dates = [h.get("changed_at")[:10] for h in (r.get("history") or []) if h.get("changed_at")]
        if r["date"] != "undated":
            dates.append(r["date"])
        if not dates:
            undated += 1
            continue
        d = min(dates)
        first[d] = first.get(d, 0) + 1
    days = [(brain.today - dt.timedelta(days=i)).isoformat() for i in range(CHART_DAYS - 1, -1, -1)]
    earlier = sum(n for d, n in first.items() if d < days[0])
    return {"labels": days, "values": [first.get(d, 0) for d in days], "earlier": earlier, "undated": undated}


def tiles(sections, questions, conflict_rows, bank_gaps) -> list[dict]:
    waiting = sum(1 for q in questions if not q["answered_on"])
    empty = sorted({g["section"] for g in bank_gaps if g["kind"] == "empty"})
    return [
        {"name": "Open questions", "plain": "Questions waiting on a founder answer", "value": waiting,
         "unit": "n", "window": "as of now", "tone": "bad" if waiting >= QUESTION_ROUND_AT else None},
        {"name": "Conflicts", "plain": "Facts where two sources disagree", "value": len(conflict_rows),
         "unit": "n", "window": "as of now", "tone": "bad" if conflict_rows else "good"},
        {"name": "Sections a room is missing", "plain": "Sections with a field a room needs and no record",
         "value": len(empty), "unit": "n", "window": "as of now", "tone": "bad" if empty else "good"},
    ]


def _short(ref: str) -> str:
    return re.sub(r"^https?://", "", ref or "a source").rstrip("/")


def insights(questions, conflict_rows) -> list[dict]:
    """Two rules from the room spec: founder question round due, and source conflict."""
    out = []
    waiting = [q for q in questions if not q["answered_on"]]
    if len(waiting) >= QUESTION_ROUND_AT:
        out.append({"rule": f"open_questions_count >= {QUESTION_ROUND_AT}", "severity": "high",
                    "sentence": f"{len(waiting)} open questions are waiting. It is time for a founder round.",
                    "capability": "BRN-C07", "autonomy": "founder_gate",
                    "evidence": f"highest weight: {waiting[0]['question']}"})
    for c in conflict_rows:
        vals = c.get("values") or []
        if len(vals) < 2:
            continue
        a, b = vals[0], vals[1]
        kept = next((v for v in vals if v.get("record_id") == c.get("kept")), a)
        out.append({"rule": "two sources disagree on the same field", "severity": "high",
                    "sentence": (f"{_short(a['source_ref'])} says \"{a['value']}\". "
                                 f"{_short(b['source_ref'])} says \"{b['value']}\". "
                                 f"\"{kept['value']}\" is kept until you say otherwise."),
                    "capability": "BRN-C05", "autonomy": "agent",
                    "evidence": f"{c['section']}.{c['field']}, rule: {c.get('rule')}"})
    return out


def overview(brain: Brain) -> dict:
    bank = keeper.load_bank()
    sections = section_table(brain)
    questions = open_questions(brain, bank)
    conf = conflicts(brain)
    g = keeper.gaps(brain, bank)
    return {"brand": brain.brand, "today": brain.today.isoformat(), "version": brain.version(),
            "simulated_note": SIMULATED_NOTE, "t0": t0_card(brain, False),
            "tiles": tiles(sections, questions, conf, g), "insights": insights(questions, conf),
            "chart": chart(brain), "sections": sections, "ladders": ladders(brain),
            "questions": questions, "review": review_queue(brain), "conflicts": conf}


def _coerce(text: str):
    t = text.strip().replace(",", "")
    try:
        return float(t.rstrip("%")) if t.rstrip("%").replace(".", "", 1).lstrip("-").isdigit() else text.strip()
    except ValueError:
        return text.strip()


def answer(brain: Brain, field: str, body: dict):
    text = str((body or {}).get("answer") or "").strip()
    if not text:
        return 400, {"error": "answer is empty"}
    oq = next((r for r in brain.raw("open_questions") if r.get("field") == field), None)
    if oq is None:
        return 404, {"error": "no open question", "field": field}
    v = dict(oq.get("value") or {})
    section = v.get("section") if v.get("section") in SECTIONS else "open_questions"
    rid = f"{brain.brand}.{section}.{field}"
    rec = {"id": rid, "brand": brain.brand, "section": section, "field": field, "value": _coerce(text),
           "text": text, "tier": "approved", "confidence": 1.0, "visibility": "private",
           "source": {"type": "founder", "ref": f"05-brand-brain answer to {oq['id']}",
                      "captured_at": brain.today.isoformat()}}
    errs = brain.put(rec)
    if errs:
        return 400, {"error": "record not valid", "details": errs}
    v.update(answered_on=brain.today.isoformat(), answer_record=rid)
    errs = brain.put(dict(oq, value=v))
    if errs:
        return 400, {"error": "question not updated", "details": errs}
    return 201, {"ok": True, "record": rid, "question": oq["id"]}


def review(brain: Brain, rid: str, body: dict):
    choice = (body or {}).get("choice")
    if choice not in ("accept", "ignore"):
        return 400, {"error": "choice must be accept or ignore"}
    parts = rid.split(".")
    if len(parts) < 3 or parts[1] not in SECTIONS:
        return 404, {"error": "no such record", "id": rid}
    rec = next((r for r in brain.raw(parts[1]) if r.get("id") == rid), None)
    if rec is None or rec.get("status") != "proposed":
        return 404, {"error": "no proposed record", "id": rid}
    if choice == "ignore":
        brain.retire(rid)
        return {"ok": True, "id": rid, "status": "retired"}
    errs = brain.put(dict(rec, status="active"))
    if errs:
        return 400, {"error": "record not valid", "details": errs}
    return {"ok": True, "id": rid, "status": "active"}


def handle(req):
    try:
        brain = _brain(req)
    except (ValueError, FileNotFoundError) as exc:
        return 404, {"error": str(exc)}
    parts = req.path
    if req.method == "GET" and parts == ["overview"]:
        return overview(brain)
    if req.method == "GET" and parts == ["records"]:
        sec = req.arg("section", "")
        if sec not in SECTIONS:
            return 404, {"error": "no such section", "section": sec}
        return {"section": sec, "records": [record_view(r) for r in brain.records(sec)]}
    if req.method == "GET" and parts == ["audit"]:
        ends = (brain.today - dt.timedelta(days=1)).isoformat()
        findings = audit.run(brain.brand, {"ends_on": ends, "days": 1, "trailing": 0}, BRAIN_ROOT)
        return {"findings": findings, "rules": audit.RULES, "brain_version": brain.version()}
    if req.method == "POST" and len(parts) == 2 and parts[0] == "questions":
        return answer(brain, parts[1], req.body)
    if req.method == "POST" and len(parts) == 2 and parts[0] == "review":
        return review(brain, parts[1], req.body)
    return 404, {"error": "not found", "path": parts}
