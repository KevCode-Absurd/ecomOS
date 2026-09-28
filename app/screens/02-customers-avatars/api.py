"""Customers and avatars screen API: /api/02-customers-avatars/...

Brand facts come from app/brain/<brand>/ through app/brain/store.py (avatars, objections,
objection_ladders, language_bank, voice, claims). Repeat by cohort comes from the brand's
simulated aggregates (cohorts.json) through app/data/tables.py. The only write is a
founder-marked voice example, through Brain.put. Nothing external, no model.

  GET  overview          tiles, insights, chart, avatar cards, objection map, language bank,
                         voice sheet
  GET  audit             findings from audit.py (app/contracts/audit.md shape) and RULES
  POST voice/examples    {kind: liked | disliked, text, note?}: writes a founder voice record

Query `brand` (default bombas) and `today` (YYYY-MM-DD, default the real date) work on
every route. Set BRAIN_ROOT to point at a copy of app/brain (tests do).
"""
from __future__ import annotations

import datetime as dt
import hashlib
import importlib.util
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent
APP = HERE.parents[1]
for p in (APP / "brain", APP / "data"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from store import Brain  # noqa: E402

BRAIN_ROOT: Path | None = None
SAFE_BRAND = re.compile(r"^[a-z0-9_-]+$")
MAX_EXAMPLE = 600
REPEAT_MONTHS = 3
CHART_COHORTS = 12
SIMULATED_NOTE = ("Bombas is the sample brand. Avatars, objections and customer words come from public reviews "
                  "and the Bombas site. Every sales and repeat number here is simulated.")
PAGE_NAMES = {"": "Homepage", "pages/about-us": "About page", "policies/terms-of-service": "Legal terms",
              "pages/happiness-guarantee": "Guarantee page"}
EXAMPLE_FIELD = re.compile(r"^(liked|disliked)_example_[0-9a-f]{8}$")
UI_AUTONOMY = {"agent_does": "agent", "founder_gate": "founder_gate", "human_assist": "human_assist"}

_spec = importlib.util.spec_from_file_location("customers_avatars_audit", HERE / "audit.py")
audit = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(audit)


def _brain(req) -> Brain:
    brand = req.arg("brand", "bombas")
    if not SAFE_BRAND.match(brand):
        raise ValueError("bad brand")
    t = req.arg("today")
    today = dt.date.fromisoformat(t) if t else dt.date.today()
    return Brain(brand, BRAIN_ROOT, today)


# ---------------------------------------------------------------- repeat by cohort

def _month_end(month: str) -> dt.date:
    y, m = (int(x) for x in month.split("-"))
    return dt.date(y + m // 12, m % 12 + 1, 1) - dt.timedelta(days=1)


def _add_months(month: str, n: int) -> str:
    y, m = (int(x) for x in month.split("-"))
    m += n
    return f"{y + (m - 1) // 12}-{(m - 1) % 12 + 1:02d}"


def repeat_by_cohort(brand: str) -> dict:
    """Share of each first-order month's customers active again in months 1 to 3.

    From cohorts.json (active customers per month since the first order). A customer active
    in 2 of those months counts twice, so this is an upper bound, capped at 100 percent.
    A cohort shows only once its 3rd month has ended.
    """
    try:
        from tables import brand_data
        data = brand_data(brand)
        rows = data.table("cohorts")
        as_of = data.brand.get("as_of")
    except (ImportError, ValueError, KeyError) as exc:
        return {"unavailable": True, "reason": f"no cohort table for {brand} ({exc})", "fix": "shopify", "labels": [], "values": []}
    end = dt.date.fromisoformat(as_of)
    out = []
    for r in rows:
        act, n = r.get("active_by_month") or [], r.get("customers")
        if not n or _month_end(_add_months(r["cohort"], REPEAT_MONTHS)) > end or len(act) <= REPEAT_MONTHS:
            continue
        back = sum(act[1:REPEAT_MONTHS + 1])
        out.append({"cohort": r["cohort"], "customers": n, "active_m1_m3": back, "rate": round(min(back / n, 1.0), 4)})
    out = out[-CHART_COHORTS:]
    if not out:
        return {"unavailable": True, "reason": "no cohort has had 3 full months yet", "fix": None, "labels": [], "values": []}
    return {"unavailable": False, "labels": [c["cohort"] for c in out], "values": [c["rate"] for c in out],
            "rows": out, "as_of": as_of, "simulated": True,
            "basis": "customers active again in months 1 to 3 after the first order, over the cohort; upper bound"}


# ---------------------------------------------------------------- voice sheet

def _context(ref: str | None) -> str:
    u = urlparse(ref or "")
    path = u.path.strip("/")
    return PAGE_NAMES.get(path, path.replace("-", " ").split("/")[-1].capitalize() or (u.netloc or "Unknown"))


def voice_sheet(brain: Brain) -> dict:
    do, do_not, contexts, liked, disliked = [], [], {}, [], []
    for r in brain.records("voice"):
        field = r.get("field") or ""
        if EXAMPLE_FIELD.match(field):
            v = r.get("value") if isinstance(r.get("value"), dict) else {}
            row = {"id": r["id"], "text": v.get("example") or r.get("text"), "note": v.get("note"), "date": r["date"]}
            (liked if field.startswith("liked") else disliked).append(row)
            continue
        src = (r.get("source") or {}).get("ref")
        quote = next((e.get("quote") for e in r.get("evidence") or [] if e.get("quote")), None)
        row = {"id": r["id"], "rule": r.get("text"), "example": quote or (r["value"] if isinstance(r.get("value"), str) else None),
               "source": src, "tier": r["tier"]}
        (do_not if r["tier"] == "forbidden" else do).append(row)
        for e in r.get("evidence") or [{"ref": src, "quote": None}]:
            c = contexts.setdefault(_context(e.get("ref")), {"context": _context(e.get("ref")), "tone": [], "refs": []})
            tone = r["value"] if isinstance(r.get("value"), str) else r.get("text")
            if tone not in c["tone"]:
                c["tone"].append(tone)
            if e.get("ref") and e["ref"] not in c["refs"]:
                c["refs"].append(e["ref"])
    for c in brain.records("claims"):
        if c["tier"] == "forbidden":
            do_not.append({"id": c["id"], "rule": c.get("text"), "example": None,
                           "source": (c.get("source") or {}).get("ref"), "tier": c["tier"]})
    for d in disliked:
        do_not.append({"id": d["id"], "rule": "Founder marked this as not us.", "example": d["text"], "source": None,
                       "tier": "approved"})
    liked.sort(key=lambda x: x["date"], reverse=True)
    disliked.sort(key=lambda x: x["date"], reverse=True)
    return {"do": do, "do_not": do_not, "contexts": sorted(contexts.values(), key=lambda c: c["context"]),
            "liked": liked, "disliked": disliked,
            "claims": [{"id": c["id"], "text": c.get("text"), "tier": c["tier"]} for c in brain.records("claims")]}


def add_example(brain: Brain, body: dict):
    kind = (body or {}).get("kind")
    text = str((body or {}).get("text") or "").strip()
    note = str((body or {}).get("note") or "").strip()[:200] or None
    if kind not in ("liked", "disliked"):
        return 400, {"error": "kind must be liked or disliked"}
    if not text:
        return 400, {"error": "example is empty"}
    if len(text) > MAX_EXAMPLE:
        return 400, {"error": f"example is over {MAX_EXAMPLE} characters"}
    digest = hashlib.sha1(text.encode("utf-8")).hexdigest()[:8]
    field = f"{kind}_example_{digest}"
    rid = f"{brain.brand}.voice.{field}"
    other = f"{brain.brand}.voice.{'disliked' if kind == 'liked' else 'liked'}_example_{digest}"
    value = {"kind": kind, "example": text}
    if note:
        value["note"] = note
    rec = {"id": rid, "brand": brain.brand, "section": "voice", "field": field, "value": value,
           "text": f"Founder marked as {kind}: {text}", "tier": "approved", "confidence": 1.0, "visibility": "private",
           "source": {"type": "founder", "ref": "02-customers-avatars voice sheet", "captured_at": brain.today.isoformat()}}
    errs = brain.put(rec)
    if errs:
        return 400, {"error": "record not valid", "details": errs}
    if any(r.get("id") == other for r in brain.raw("voice")):
        brain.retire(other)
    return 201, {"ok": True, "record": rid}


# ---------------------------------------------------------------- tiles, insights

def tiles(avatars, objections, chart) -> list[dict]:
    grounded = sum(1 for a in avatars if a["grounding"] == "grounded")
    proven = sum(1 for o in objections if o["status"] == "proof on file")
    rep = {"name": "Repeat within 3 months", "plain": "Latest cohort's first-time buyers active again in months 1 to 3",
           "unit": "%", "higher_is_better": True}
    if chart["unavailable"]:
        rep.update(value=None, unavailable_reason=chart["reason"], fix=chart.get("fix"), window="cohorts")
    else:
        vals = chart["values"]
        rep.update(value=vals[-1], window=f"cohort {chart['labels'][-1]}, simulated",
                   delta=round(vals[-1] / vals[-2] - 1, 4) if len(vals) > 1 and vals[-2] else None)
    return [
        {"name": "Grounded avatars", "plain": f"Avatars with quotes from {audit.MIN_SOURCES} or more sources, of {len(avatars)}",
         "value": grounded if avatars else None, "unit": f"of {len(avatars)}", "window": "as of latest brain",
         "unavailable_reason": None if avatars else "no avatar records yet", "fix": "BRAND-C11",
         "tone": "bad" if avatars and grounded * 2 < len(avatars) else None},
        {"name": "Objection coverage", "plain": "Named objections where every rung has a proof record",
         "value": round(proven / len(objections), 4) if objections else None, "unit": "%", "window": "as of latest brain",
         "unavailable_reason": None if objections else "objection map is empty", "fix": "BRAND-C13",
         "higher_is_better": True},
        rep,
    ]


def insights(avatars, all_rungs, ends_on) -> list[dict]:
    """Two rules: an avatar whose top objection has no proof, and an avatar with no quotes or 1 source."""
    out = []
    for f in audit.r02(None, avatars, all_rungs, ends_on):
        out.append({"rule": "avatar's top objection rung (most one-star mentions) has no proof record",
                    "severity": "medium", "sentence": f["sentence"], "capability": "BRAND-C13", "autonomy": "agent",
                    "evidence": f"rung {f['entity']['id']}; refs: {', '.join(f['brain_refs'])}"})
    bare = [a for a in avatars if a["quote_count"] == 0]
    thin = [a for a in avatars if a["quote_count"] and a["grounding"] != "grounded"]
    for a in bare:
        out.append({"rule": "avatar has 0 customer quotes", "severity": "medium",
                    "sentence": f"{a['name']} has no customer quotes. It is a guess until customers say it.",
                    "capability": "BRAND-C01", "autonomy": "agent", "evidence": a["id"]})
    if thin:
        share = sum(a["share_estimate"] or 0 for a in thin)
        known = [a for a in thin if a["share_estimate"] is not None]
        tail = f" They cover about {round(share * 100)} percent of buyers." if known else ""
        out.append({"rule": f"avatar quotes come from fewer than {audit.MIN_SOURCES} sources", "severity": "medium",
                    "sentence": f"{len(thin)} of {len(avatars)} avatars rest on quotes from 1 source each.{tail}",
                    "capability": "BRAND-C11", "autonomy": "founder_gate",
                    "evidence": "; ".join(f"{a['name']}: {a['sources'][0]}" for a in thin)})
    return out


def overview(brain: Brain) -> dict:
    ends_on = (brain.today - dt.timedelta(days=1)).isoformat()
    avatars = audit.avatar_rows(brain)
    all_rungs = audit.rungs(brain)
    angles = audit.ad_angles(brain.brand, ends_on)
    objections = audit.objection_rows(brain, all_rungs, angles)
    for a in avatars:
        top = audit.top_objection(a["id"], all_rungs)
        a["top_objection"] = None if top is None else {"id": top["id"], "doubt": top["doubt"], "one_star": top["one_star"],
                                                        "proof": bool(top["proof_ids"])}
    chart = repeat_by_cohort(brain.brand)
    return {"brand": brain.brand, "today": brain.today.isoformat(), "version": brain.version(),
            "simulated_note": SIMULATED_NOTE, "tiles": tiles(avatars, objections, chart),
            "insights": insights(avatars, all_rungs, ends_on), "chart": chart, "avatars": avatars,
            "objections": objections, "angles": {k: angles[k] for k in ("available", "reason", "ads")},
            "language": audit.language_rows(brain), "voice": voice_sheet(brain),
            "decision": {"capability": "BRAND-C15", "autonomy": "agent",
                         "label": "Re-check every avatar against the newest reviews and tickets"}}


def handle(req):
    try:
        brain = _brain(req)
    except (ValueError, FileNotFoundError) as exc:
        return 404, {"error": str(exc)}
    parts = req.path
    if req.method == "GET" and parts == ["overview"]:
        return overview(brain)
    if req.method == "GET" and parts == ["audit"]:
        ends = (brain.today - dt.timedelta(days=1)).isoformat()
        findings = audit.run(brain.brand, {"ends_on": ends, "days": 1, "trailing": 0}, BRAIN_ROOT)
        return {"findings": findings, "rules": audit.RULES, "brain_version": brain.version()}
    if req.method == "POST" and parts == ["voice", "examples"]:
        return add_example(brain, req.body)
    return 404, {"error": "not found", "path": parts}
