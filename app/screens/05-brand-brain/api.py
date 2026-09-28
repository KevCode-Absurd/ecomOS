"""Brand brain screen API: /api/05-brand-brain/...

Reads app/brain/<brand>/ through app/brain/store.py and keeper.py. The only
writes go through Brain.put and Brain.retire: a founder answer to an open
question, and accept or ignore on a proposed record. Nothing external.

  GET  overview                 T0 card, section table, tiles, insights, chart, ladders,
                                open questions, review queue, conflicts
  GET  master?window=28d        the orchestrator's master list: every screen's rank merged
                                (app/rank.py): top 10 to approve, connect strip, bottlenecks
  GET  profile                  the editable brand profile: one winning record per field in
                                identity, positioning, voice, visual, products, offers,
                                policies, claims, with tier, source, date and where it flows
  POST profile/<section>/<field> {text}: writes an approved founder record that wins the merge
  GET  documents                the documents manifest with what each file changed
  POST documents                {name, text | content_base64 | url, note}: stores the file
                                under documents/ and adds a manifest line; never blocked
  GET  competitors              the Ad Library pages against the brand: format and hook mix per page,
                                competitor medians, the gaps, proposed pages, and the cost of a re-pull
  GET  coverage                 angles by page: our ad count per angle against each competitor page, gaps with a
                                drafted concept brief, our own ground, contested angles
  GET  signals                  what buyers say elsewhere: recommended-instead per competitor with the doubt behind
                                it, our proof status and where to answer; category frames against our frame; the
                                competitor sets; proposed pages waiting on a page id
  POST competitors/page-id      {name, page_id}: writes an approved founder record competitors.page_id_<slug>;
                                the page joins the page list and the next pull estimate
  GET  health                   freshness by confidence: sections by tier with counts, freshness, the one action
                                per section (connect, ask the founder, re-crawl), and the connectors
  GET  health/cell?section=&tier=  the records in one heatmap cell, best first
  POST approve/<record id>      {choice: approve | forbid}: the founder settles a record; it becomes an approved
                                (or forbidden) founder record with the old tier in history
  GET  conflicts                open and settled conflicts with the default winner named and who reads the field
  POST conflicts/<id>           {record_id | index | text, reason}: the founder decides; writes an approved founder
                                record for the field, marks the conflict resolved, logs a decisions record
  GET  records?section=<name>   one section's records with tier, date, source and evidence
  GET  audit                    findings from audit.py (app/contracts/audit.md shape)
  POST questions/<field>        {answer}: writes a founder record, marks the question answered
  POST review/<record id>       {choice: accept | ignore}

Query `brand` (default bombas) and `today` (YYYY-MM-DD, default the real date)
work on every route. Set BRAIN_ROOT to point at a copy of app/brain (tests do).
"""
from __future__ import annotations

import base64
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
_hspec = importlib.util.spec_from_file_location("brand_brain_health", HERE / "health.py")
health = importlib.util.module_from_spec(_hspec)
_hspec.loader.exec_module(health)
_mspec = importlib.util.spec_from_file_location("brand_brain_market", HERE / "market.py")
market = importlib.util.module_from_spec(_mspec)
_mspec.loader.exec_module(market)
_rspec = importlib.util.spec_from_file_location("ecomos_rank_bb", APP / "rank.py")
rank_mod = importlib.util.module_from_spec(_rspec)
_rspec.loader.exec_module(rank_mod)

# the editable profile: sections in reading order, the fields a founder edits first, and where each section flows
PROFILE_SECTIONS = [
    ("identity", "Identity", ["category", "one_line_pitch", "giving_model", "founded", "headquarters", "certification_bcorp"]),
    ("positioning", "Positioning", ["frame", "category_frame", "price_frame", "competitive_frame", "proof_points"]),
    ("voice", "Voice", []),
    ("visual", "Visual", []),
    ("products", "Products", ["lines", "price_ladder_socks", "pack_sizes", "materials"]),
    ("offers", "Offers", ["free_shipping_threshold_usd", "standard_shipping_cost", "guarantee", "first_order_code", "bundles_pack_ladder"]),
    ("policies", "Policies", ["returns_window_days", "refund_method", "happiness_guarantee", "exchanges", "shipping_options"]),
    ("claims", "Claims", []),
]
FLOWS_TO = {"identity": "every screen", "positioning": "market research, customers, competitors, offers, creative, copy, landing pages, SEO, answer engines",
            "voice": "copy, creative, email, organic, CX", "visual": "creative, landing pages, organic",
            "products": "offers, creative, copy, Google Ads, marketplaces, supply, SEO", "offers": "paid social, Google Ads, email, landing pages, finance",
            "policies": "CX, store health, landing pages, security", "claims": "copy, creative, landing pages, answer engines, marketplaces"}
TIER_RANK = {"approved": 0, "site_backed": 1, "reported": 2, "evidence": 3, "inferred": 4, "unverified": 5, "forbidden": 6}
DOC_MAX_BYTES = 5 * 1024 * 1024
SAFE_FILE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 ._()-]{0,120}$")


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


def _conflict_rows(brain: Brain) -> list[dict]:
    path = brain.dir / "review" / "conflicts.json"
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    except (OSError, ValueError):
        return []


def conflicts(brain: Brain) -> list[dict]:
    return [c for c in _conflict_rows(brain) if c.get("status", "open") == "open"]


DEFAULT_WINNER = ("founder", "connector", "site", "document", "ad_library", "interview", "press", "review", "ticket", "agent", "inferred")


def conflicts_view(brain: Brain) -> dict:
    """Open and settled conflicts with the default winner named (site wins over documents and everything below it)."""
    rows = _conflict_rows(brain)
    out = {"open": [], "settled": []}
    for c in rows:
        vals = c.get("values") or []
        ranked = sorted(vals, key=lambda v: (DEFAULT_WINNER.index(v.get("source_type")) if v.get("source_type") in DEFAULT_WINNER else 99, -(v.get("confidence") or 0)))
        default = ranked[0] if ranked else None
        item = dict(c, default_record=default.get("record_id") if default else None, default_source=default.get("source_type") if default else None,
                    kept_value=next((v for v in vals if v.get("record_id") == c.get("kept")), default),
                    reads_by=sorted(FLOWS_TO.get(c.get("section"), "").split(", ")) if FLOWS_TO.get(c.get("section")) else [])
        (out["open"] if c.get("status", "open") == "open" else out["settled"]).append(item)
    out["open"].sort(key=lambda c: (not c.get("needs_founder"), c.get("raised_at") or ""))
    out["settled"].sort(key=lambda c: -(int((c.get("resolved_at") or c.get("raised_at") or "0").replace("-", "")) if (c.get("resolved_at") or c.get("raised_at")) else 0))
    out["counts"] = {"open": len(out["open"]), "settled": len(out["settled"]), "needs_founder": sum(1 for c in out["open"] if c.get("needs_founder"))}
    out["rule"] = "Default: founder, then connector, then the live site, then documents, the ad library, interviews, press, reviews, tickets, agents, inferred. The kept value stands until you decide."
    return out


def conflict_resolve(brain: Brain, cid: str, body: dict):
    body = body or {}
    rows = _conflict_rows(brain)
    c = next((x for x in rows if x.get("id") == cid), None)
    if c is None:
        return 404, {"error": "no such conflict", "id": cid}
    vals = c.get("values") or []
    chosen = None
    if body.get("record_id"):
        chosen = next((v for v in vals if v.get("record_id") == body["record_id"] and ("index" not in body or vals.index(v) == body["index"])), None)
        if chosen is None and isinstance(body.get("index"), int) and 0 <= body["index"] < len(vals):
            chosen = vals[body["index"]]
    elif isinstance(body.get("index"), int) and 0 <= body["index"] < len(vals):
        chosen = vals[body["index"]]
    text = str(body.get("text") or "").strip()
    if chosen is None and not text:
        return 400, {"error": "send record_id, index or text"}
    section, field = c.get("section"), c.get("field")
    if section not in SECTIONS or not field:
        return 400, {"error": "conflict has no section or field"}
    rid = f"{brain.brand}.{section}.{field}"
    value = chosen.get("value") if chosen else _coerce(text)
    rec_text = (chosen.get("text") or str(chosen.get("value"))) if chosen else text
    reason = str(body.get("reason") or "").strip()[:300]
    rec = {"id": rid, "brand": brain.brand, "section": section, "field": field, "value": value, "text": rec_text,
           "tier": "approved", "confidence": 1.0, "visibility": "private",
           "source": {"type": "founder", "ref": f"05-brand-brain conflict decision on {cid}", "captured_at": brain.today.isoformat()}}
    errs = founder_put(brain, rec)
    if errs:
        return 400, {"error": "record not valid", "details": errs}
    c.update(status="resolved_by_founder", kept=rid, needs_founder=False, resolved_at=brain.today.isoformat(),
             rule="founder decided" + (f": {reason}" if reason else ""),
             chosen={"record_id": chosen.get("record_id") if chosen else None, "source_type": chosen.get("source_type") if chosen else "founder", "value": value})
    (brain.dir / "review").mkdir(parents=True, exist_ok=True)
    (brain.dir / "review" / "conflicts.json").write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    losers = [v for v in vals if v is not chosen]
    drec = {"id": f"{brain.brand}.decisions.conflict_{section}_{field}", "brand": brain.brand, "section": "decisions", "field": f"conflict_{section}_{field}",
            "value": {"conflict": cid, "kept": rid, "chosen_source": chosen.get("source_type") if chosen else "founder", "over": [v.get("source_type") for v in losers], "reason": reason or None},
            "text": f"Conflict on {section.replace('_', ' ')} {field.replace('_', ' ')}: kept \"{str(rec_text)[:80]}\" ({chosen.get('source_type') if chosen else 'typed by the founder'}) over " + (", ".join(f"\"{str(v.get('value'))[:40]}\" ({v.get('source_type')})" for v in losers) or "the other values") + (f". Reason: {reason}" if reason else "."),
            "tier": "approved", "confidence": 1.0, "visibility": "private",
            "source": {"type": "founder", "ref": f"05-brand-brain conflict decision on {cid}", "captured_at": brain.today.isoformat()}}
    founder_put(brain, drec)
    return 201, {"ok": True, "conflict": cid, "record": rid, "decision": drec["id"], "flows_to": FLOWS_TO.get(section, ""), "version": brain.version()}


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


FOUNDER_LANE = "z-founder"


def founder_put(brain: Brain, rec: dict) -> list[str]:
    """Write a founder record to its section file and to raw/z-founder/<section>.json, so merge.py keeps it on a re-merge."""
    errs = brain.put(rec)
    if errs:
        return errs
    lane = brain.dir / "raw" / FOUNDER_LANE
    try:
        lane.mkdir(parents=True, exist_ok=True)
        path = lane / f"{rec['section']}.json"
        rows = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
        rows = [r for r in rows if r.get("id") != rec["id"]] + [rec]
        path.write_text(json.dumps(rows, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    except (OSError, ValueError):
        pass  # the section file is the record of truth; the raw lane is a convenience for re-merges
    return []


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
    errs = founder_put(brain, rec)
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


def _window(req, brain: Brain) -> dict:
    w = req.arg("window", "28d") or "28d"
    days = int(w[:-1]) if re.fullmatch(r"\d+d", w) else 28
    return {"ends_on": (brain.today - dt.timedelta(days=1)).isoformat(), "days": days, "trailing": 4}


def master(brain: Brain, window: dict) -> dict:
    root = (BRAIN_ROOT or (APP / "brain"))
    out = rank_mod.master(brain.brand, window)
    out["brain_version"] = brain.version()
    out["brain_root"] = str(root.name)
    return out


def profile(brain: Brain) -> dict:
    """One winning record per field: the best tier, then the newest. Founder edits are tier approved and win."""
    sections = []
    for sec, label, first in PROFILE_SECTIONS:
        by_field: dict[str, dict] = {}
        for r in brain.records(sec):
            f = r.get("field") or "value"
            key = (TIER_RANK.get(r["tier"], 9), "" if r["date"] == "undated" else "-" + r["date"])
            cur = by_field.get(f)
            if cur is None or key < cur[0]:
                by_field[f] = (key, r)
        order = list(first) + sorted(k for k in by_field if k not in first)
        fields = []
        for f in order:
            if f not in by_field:
                fields.append({"key": f, "text": None, "tier": None, "source": None, "date": None, "confidence": None, "record_id": None, "editable": True})
                continue
            r = by_field[f][1]
            src = _source(r)
            fields.append({"key": f, "text": r.get("text") or (r["value"] if isinstance(r.get("value"), str) else json.dumps(r.get("value"))[:300]),
                           "tier": r["tier"], "source": (src["type"] + (": " + re.sub(r"^https?://", "", src["ref"])[:60] if src["ref"] else "")),
                           "date": None if r["date"] == "undated" else r["date"], "confidence": r["confidence"], "record_id": r["id"],
                           "variants": sum(1 for x in brain.records(sec) if (x.get("field") or "value") == f), "editable": True})
        approved = sum(1 for x in fields if x["tier"] == "approved")
        sections.append({"section": sec, "label": label, "flows_to": FLOWS_TO.get(sec, ""), "fields": fields,
                         "records": len(brain.records(sec)), "approved": approved})
    total = sum(len(x["fields"]) for x in sections)
    appr = sum(x["approved"] for x in sections)
    return {"brand": brain.brand, "today": brain.today.isoformat(), "version": brain.version(), "sections": sections,
            "fields": total, "approved": appr, "approved_share": (appr / total) if total else None}


def profile_edit(brain: Brain, section: str, field: str, body: dict):
    text = str((body or {}).get("text") or "").strip()
    if not text:
        return 400, {"error": "text is empty"}
    if section not in {s for s, _, _ in PROFILE_SECTIONS} or not re.fullmatch(r"[a-z0-9_]{1,60}", field):
        return 404, {"error": "no such profile field", "section": section, "field": field}
    rid = f"{brain.brand}.{section}.{field}"
    rec = {"id": rid, "brand": brain.brand, "section": section, "field": field, "value": _coerce(text), "text": text,
           "tier": "approved", "confidence": 1.0, "visibility": "private",
           "source": {"type": "founder", "ref": "05-brand-brain profile edit", "captured_at": brain.today.isoformat()}}
    errs = founder_put(brain, rec)
    if errs:
        return 400, {"error": "record not valid", "details": errs}
    return 201, {"ok": True, "record": rid, "tier": "approved", "flows_to": FLOWS_TO.get(section, ""), "version": brain.version()}


def documents(brain: Brain) -> dict:
    docs = brain.documents()
    recs = brain.records(include_retired=True)
    out = []
    for d in docs:
        name = Path(d.get("file", "")).name
        changed = [r["id"] for r in recs if name and name in str((r.get("source") or {}).get("ref") or "")]
        out.append(dict(d, name=name, records_changed=changed[:20], records_changed_count=len(changed)))
    out.sort(key=lambda d: d.get("added_at", ""), reverse=True)
    return {"documents": out, "count": len(out)}


def document_add(brain: Brain, body: dict):
    body = body or {}
    url = str(body.get("url") or "").strip()
    name = str(body.get("name") or "").strip()
    note = str(body.get("note") or "").strip()[:300]
    if url:
        if not re.match(r"^https?://[^\s]{4,500}$", url):
            return 400, {"error": "url must start with http or https"}
        name = name or re.sub(r"[^A-Za-z0-9._-]+", "-", re.sub(r"^https?://", "", url))[:80].strip("-") + ".url"
        data = ("[InternetShortcut]\nURL=" + url + "\n").encode("utf-8")
    else:
        if not SAFE_FILE.match(name) or ".." in name:
            return 400, {"error": "name must be a plain file name"}
        if body.get("content_base64") is not None:
            try:
                data = base64.b64decode(str(body["content_base64"]), validate=True)
            except (ValueError, TypeError):
                return 400, {"error": "content_base64 is not valid base64"}
        elif body.get("text") is not None:
            data = str(body["text"]).encode("utf-8")
        else:
            return 400, {"error": "send text, content_base64 or url"}
    if len(data) > DOC_MAX_BYTES:
        return 413, {"error": "file is over 5 MB"}
    ddir = brain.dir / "documents"
    ddir.mkdir(parents=True, exist_ok=True)
    stamp = brain.today.isoformat()
    fname = f"{stamp}-{name}"
    target = ddir / fname
    i = 2
    while target.exists():
        target = ddir / f"{stamp}-{i}-{name}"
        i += 1
    target.write_bytes(data)
    manifest = brain.documents()
    line = {"file": f"documents/{target.name}", "added_at": stamp, "added_by": "founder", "extracted": False}
    if note:
        line["note"] = note
    if url:
        line["tags"] = ["url"]
    manifest.append(line)
    (ddir / "manifest.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")
    return 201, {"ok": True, "document": dict(line, name=target.name, bytes=len(data)), "records_changed_count": 0,
                 "next": "Kept as it is. Extraction into records is proposed through the review queue.", "version": brain.version()}


def competitors(brain: Brain) -> dict:
    d = market.pages(brain)
    d["gaps"] = market.gaps(brain)
    d["repull"] = market.repull(brain)
    d["formats"] = [{"key": k, "label": market.FORMAT_LABEL[k]} for k in market.FORMATS]
    d["hooks"] = [{"key": k, "label": market.HOOK_LABEL[k]} for k in market.HOOKS]
    d["stale_after_days"] = market.SNAPSHOT_STALE_DAYS
    d["brand"], d["today"], d["version"] = brain.brand, brain.today.isoformat(), brain.version()
    return d


def page_id_add(brain: Brain, body: dict):
    name = str((body or {}).get("name") or "").strip()
    pid = str((body or {}).get("page_id") or "").strip()
    if not name or not re.fullmatch(r"[A-Za-z0-9 .&'-]{2,60}", name):
        return 400, {"error": "name must be a plain page name"}
    if not re.fullmatch(r"\d{5,20}", pid):
        return 400, {"error": "page_id must be the numeric Meta page id"}
    slug = market._slug(name)
    rid = f"{brain.brand}.competitors.page_id_{slug}"
    rec = {"id": rid, "brand": brain.brand, "section": "competitors", "field": f"page_id_{slug}", "value": pid,
           "text": f"{name} Meta page id {pid}, added by the founder for the Ad Library pull.",
           "tier": "approved", "confidence": 1.0, "visibility": "private",
           "source": {"type": "founder", "ref": "05-brand-brain competitors page id", "captured_at": brain.today.isoformat()}}
    errs = founder_put(brain, rec)
    if errs:
        return 400, {"error": "record not valid", "details": errs}
    return 201, {"ok": True, "record": rid, "flows_to": "the page list and the next Ad Library pull estimate", "version": brain.version()}


def approve(brain: Brain, rid: str, body: dict):
    choice = (body or {}).get("choice")
    if choice not in ("approve", "forbid"):
        return 400, {"error": "choice must be approve or forbid"}
    parts = rid.split(".")
    if len(parts) < 3 or parts[1] not in SECTIONS:
        return 404, {"error": "no such record", "id": rid}
    rec = next((r for r in brain.raw(parts[1]) if r.get("id") == rid), None)
    if rec is None:
        return 404, {"error": "no such record", "id": rid}
    was = {"type": (rec.get("source") or {}).get("type"), "ref": (rec.get("source") or {}).get("ref"), "tier": rec.get("tier")}
    hist = list(rec.get("history") or []) + [{"value": rec.get("value"), "changed_at": brain.today.isoformat(),
                                             "source_ref": was["ref"] or "", "tier": was["tier"], "reason": f"founder {choice}"}]
    new = dict(rec, tier="approved" if choice == "approve" else "forbidden", confidence=1.0, status="active", history=hist,
               source={"type": "founder", "ref": f"05-brand-brain {choice} of {rid}", "captured_at": brain.today.isoformat(), "was": was})
    new.pop("expires_at", None)
    errs = founder_put(brain, new)
    if errs:
        return 400, {"error": "record not valid", "details": errs}
    return 201, {"ok": True, "record": rid, "tier": new["tier"], "was": rec.get("tier"), "version": brain.version()}


def handle(req):
    try:
        brain = _brain(req)
    except (ValueError, FileNotFoundError) as exc:
        return 404, {"error": str(exc)}
    parts = req.path
    if req.method == "GET" and parts == ["overview"]:
        return overview(brain)
    if req.method == "GET" and parts == ["master"]:
        return master(brain, _window(req, brain))
    if req.method == "GET" and parts == ["profile"]:
        return profile(brain)
    if req.method == "POST" and len(parts) == 3 and parts[0] == "profile":
        return profile_edit(brain, parts[1], parts[2], req.body)
    if req.method == "GET" and parts == ["documents"]:
        return documents(brain)
    if req.method == "POST" and parts == ["documents"]:
        return document_add(brain, req.body)
    if req.method == "GET" and parts == ["competitors"]:
        return competitors(brain)
    if req.method == "GET" and parts == ["conflicts"]:
        cv = conflicts_view(brain)
        cv.update(brand=brain.brand, today=brain.today.isoformat(), version=brain.version())
        return cv
    if req.method == "POST" and len(parts) == 2 and parts[0] == "conflicts":
        return conflict_resolve(brain, parts[1], req.body)
    if req.method == "GET" and parts == ["health"]:
        h = health.heatmap(brain)
        h["connectors"] = health.connectors(brain)
        h.update(brand=brain.brand, today=brain.today.isoformat(), version=brain.version())
        return h
    if req.method == "GET" and parts == ["health", "cell"]:
        sec, tier = req.arg("section", ""), req.arg("tier", "")
        return {"section": sec, "tier": tier, "records": health.records_in_cell(brain, sec, tier)}
    if req.method == "POST" and len(parts) == 2 and parts[0] == "approve":
        return approve(brain, parts[1], req.body)
    if req.method == "GET" and parts == ["signals"]:
        sg = market.signals(brain)
        sg.update(brand=brain.brand, today=brain.today.isoformat(), version=brain.version())
        return sg
    if req.method == "POST" and parts == ["competitors", "page-id"]:
        return page_id_add(brain, req.body)
    if req.method == "GET" and parts == ["coverage"]:
        c = market.coverage(brain)
        c.update(brand=brain.brand, today=brain.today.isoformat(), version=brain.version())
        return c
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
