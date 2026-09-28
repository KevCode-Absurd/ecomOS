"""The changes log and the fact-to-asset trace.

Changes (`changes` section, contract section 4: date, type, what changed, section and record ids, source): every
write through this screen logs one record: a founder edit (with the value before), a document in, records proposed
from it, a proposal accepted or ignored, a conflict settled, a claim tiered, a site snapshot with the fields that
moved. `recent` reads them newest first with counts by kind. Versions (`review/versions.json`) keep the brain
version hash before and after each write, so a package can name the version it was built from.

Trace (`dependents`): what depends on one fact. From records only: other records carrying the same number or code
next to the same keywords, ladder rungs citing the record as proof, open questions answered by it, snippets built
from it, and the brand's own ads that carry the code or promo (the Ad Library read counted them). When the fact
changes, the change record lists its dependents, so the fix names every surface.
"""
from __future__ import annotations

import json
import re

TRACE_SECTIONS = {"offers", "policies", "products", "voice", "claims", "identity", "positioning", "learnings", "diagnosis", "calendar", "operations", "channels", "content", "story_bank"}
KIND_PLURAL = {"record": "records", "ads": "ad records", "rung": "ladder rungs", "question": "questions", "snippet": "snippets"}
KINDS = ["founder_edit", "answer", "approve", "forbid", "document", "proposed", "accepted", "ignored", "conflict", "site", "snapshot", "contract", "permission", "page_id", "snippet", "example", "proof", "retired", "router"]
KIND_LABEL = {"founder_edit": "you edited", "answer": "you answered", "approve": "you approved", "forbid": "you forbade", "document": "file in",
              "proposed": "records proposed", "accepted": "proposal accepted", "ignored": "proposal ignored", "conflict": "conflict settled",
              "site": "site changed", "snapshot": "site snapshot", "contract": "contract on file", "permission": "permission set", "page_id": "page id added",
              "snippet": "snippet locked", "example": "voice example"}


def _short(v) -> str | None:
    if v is None:
        return None
    s = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)
    return s if len(s) <= 160 else s[:157] + "..."


def _source(kind: str, source: str, record: str | None, today: str) -> dict:
    if kind in ("site", "snapshot"):
        return {"type": "site", "ref": source, "captured_at": today}
    if kind in ("document", "proposed"):
        return {"type": "document", "ref": source, "captured_at": today}
    if kind in ("accepted", "ignored"):
        return {"type": "agent", "ref": source, "captured_at": today, "derived_from": [record] if record else []}
    return {"type": "founder", "ref": source, "captured_at": today}


def log(brain, kind: str, section: str | None, record: str | None, what: str, source: str = "05-brand-brain", before=None, after=None) -> str | None:
    """Append one changes record. Never raises: a failed log must not block the write it describes."""
    try:
        n = sum(1 for r in brain.raw("changes")) + 1
        rid = f"{brain.brand}.changes.{brain.today.isoformat().replace('-', '')}_{n:04d}"
        rec = {"id": rid, "brand": brain.brand, "section": "changes", "field": kind if kind in KINDS else "other",
               "value": {"kind": kind, "section": section, "record": record, "what": what[:300], "before": _short(before), "after": _short(after), "source": source},
               "text": f"{KIND_LABEL.get(kind, kind)}: {what[:200]}", "tier": "approved" if kind.startswith(("founder", "answer", "approve", "forbid", "conflict", "contract", "permission", "snippet", "example")) else "evidence",
               "visibility": "private", "source": _source(kind, source, record, brain.today.isoformat())}
        errs = brain.put(rec)
        return None if errs else rid
    except Exception:  # noqa: BLE001
        return None


def version_step(brain, before: str, what: str) -> None:
    try:
        p = brain.dir / "review" / "versions.json"
        rows = json.loads(p.read_text(encoding="utf-8")) if p.is_file() else []
        after = brain.version()
        if after == before:
            return
        rows.append({"at": brain.today.isoformat(), "before": before, "after": after, "what": what[:200]})
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(rows[-500:], indent=1) + "\n", encoding="utf-8")
    except Exception:  # noqa: BLE001
        return


def versions(brain) -> list[dict]:
    p = brain.dir / "review" / "versions.json"
    try:
        return list(reversed(json.loads(p.read_text(encoding="utf-8")))) if p.is_file() else []
    except (OSError, ValueError):
        return []


def recent(brain, days: int = 7) -> dict:
    rows = []
    for r in brain.records("changes"):
        v = r.get("value") if isinstance(r.get("value"), dict) else {}
        rows.append({"id": r["id"], "date": None if r["date"] == "undated" else r["date"], "kind": v.get("kind") or r.get("field"), "label": KIND_LABEL.get(v.get("kind") or r.get("field"), r.get("field")),
                     "section": v.get("section"), "record": v.get("record"), "what": v.get("what") or r.get("text"), "before": v.get("before"), "after": v.get("after"), "source": v.get("source"), "age_days": r["age_days"]})
    rows.sort(key=lambda x: ((x["date"] or ""), x["id"]), reverse=True)
    week = [x for x in rows if x["age_days"] is not None and x["age_days"] <= days]
    by_kind = {}
    for x in week:
        by_kind[x["kind"]] = by_kind.get(x["kind"], 0) + 1
    return {"changes": rows[:200], "week": week, "counts": {"total": len(rows), "week": len(week), "by_kind": by_kind}, "days": days, "versions": versions(brain)[:20]}


# ---------------------------------------------------------------- the trace

def _numbers(v) -> set[str]:
    s = v if isinstance(v, str) else json.dumps(v)
    return {x.replace(",", "") for x in re.findall(r"(?<![A-Za-z0-9])\d[\d,]*(?:\.\d+)?(?![A-Za-z])", s or "") if float(x.replace(",", "")) >= 5}


def _codes(v) -> set[str]:
    s = v if isinstance(v, str) else json.dumps(v)
    return {c for c in re.findall(r"\b[A-Z][A-Z0-9]{4,}\b", s or "") if any(ch.isdigit() for ch in c) or len(c) >= 6}


def _keywords(field: str) -> set[str]:
    return {w for w in (field or "").lower().split("_") if len(w) > 3 and w not in ("usd", "days", "pct")}


def dependents(brain, record_id: str) -> dict:
    parts = record_id.split(".")
    if len(parts) < 3:
        return {"record": record_id, "dependents": [], "counts": {}}
    section = parts[1]
    rec = next((r for r in brain.records(section) if r["id"] == record_id), None)
    if rec is None:
        return {"record": record_id, "dependents": [], "counts": {}, "reason": "no such record"}
    nums, codes, kws = _numbers(rec.get("value")) | _numbers(rec.get("text")), _codes(rec.get("value")) | _codes(rec.get("text")), _keywords(rec.get("field") or "")
    out = []
    for r in brain.records():
        if r["id"] == record_id or r["section"] in ("changes", "freshness", "language_bank"):
            continue
        if r["section"] not in TRACE_SECTIONS and r["section"] not in ("objection_ladders", "open_questions"):
            continue
        blob = f"{r.get('field') or ''} {r.get('text') or ''} {json.dumps(r.get('value'))}".lower()
        v = r.get("value")
        # ladder rungs that cite it as proof
        if r["section"] == "objection_ladders" and isinstance(v, dict):
            for rung in v.get("rungs") or []:
                if record_id in (rung.get("proof_ids") or []):
                    out.append({"kind": "rung", "id": r["id"], "label": f"{v.get('theme') or r.get('field')} rung {rung.get('level')}", "why": "cites it as proof", "surfaces": rung.get("uses") or []})
            continue
        if r["section"] == "open_questions" and isinstance(v, dict) and v.get("answer_record") == record_id:
            out.append({"kind": "question", "id": r["id"], "label": (v.get("question") or "")[:80], "why": "answered by it", "surfaces": []})
            continue
        if (r.get("field") or "").startswith("snippet_") and (nums & _numbers(v)) or ((r.get("field") or "").startswith("snippet_") and codes & _codes(v)):
            out.append({"kind": "snippet", "id": r["id"], "label": (r.get("field") or "")[8:].replace("_", " ") + " line", "why": "carries the same number or code", "surfaces": ["every draft that pastes it"]})
            continue
        hit_code = codes & _codes(v) | (codes & _codes(r.get("text")))
        hit_num = (nums & _numbers(v)) and (kws & set(blob.replace("_", " ").split()))
        if hit_code or hit_num:
            ads = None
            if isinstance(v, dict):
                ads = v.get("ads") or v.get("ads_with_code")
            out.append({"kind": "ads" if ads else "record", "id": r["id"], "label": (r.get("text") or r.get("field") or "")[:90], "why": ("code " + ", ".join(sorted(hit_code))) if hit_code else "same number next to the same words",
                        "surfaces": [f"{ads} active ads"] if ads else [], "ads": ads})
    counts = {}
    for d in out:
        counts[d["kind"]] = counts.get(d["kind"], 0) + 1
    ads_total = sum(d["ads"] for d in out if d.get("ads"))
    return {"record": record_id, "field": rec.get("field"), "value": _short(rec.get("value")), "dependents": out, "counts": counts, "ads": ads_total or None,
            "summary": (", ".join(f"{n} {KIND_PLURAL.get(k, k) if n != 1 else KIND_PLURAL.get(k, k).rstrip('s')}" for k, n in counts.items()) + (f", {ads_total} active ads" if ads_total else "")) or "nothing found that depends on it",
            "note": "From records only: same number or code next to the same words, rungs citing it, questions it answered, snippets built on it, and ads the Ad Library read counted. Live ads and emails join when Meta and Klaviyo connect."}
