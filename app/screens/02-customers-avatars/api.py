"""Customers and avatars screen API: /api/02-customers-avatars/...

Brand facts come from app/brain/<brand>/ through app/brain/store.py (avatars, objections,
objection_ladders, language_bank, voice, claims). Repeat by cohort comes from the brand's
simulated aggregates (cohorts.json) through app/data/tables.py. The only write is a
founder-marked voice example, through Brain.put. Nothing external, no model.

  GET  overview          orientation numbers, avatar cards, objection map, language bank,
                         voice sheet
  GET  rank              served by app/rank.py, which calls `rank(brand, window)` below when present
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


# ---------------------------------------------------------------- orientation

def daily_window(brand: str, ends_on: str, days: int = 28) -> dict:
    """Trailing `days` of the daily aggregate ending on or before `ends_on`. Unavailable when short, never 0."""
    try:
        from tables import brand_data
        rows = brand_data(brand).table("daily")
    except (ImportError, ValueError, KeyError, FileNotFoundError) as exc:
        return {"unavailable": True, "reason": f"no daily table for {brand} ({exc})", "rows": []}
    rows = [r for r in rows if isinstance(r, dict) and str(r.get("date", ""))[:10] <= ends_on]
    rows = rows[-days:]
    if len(rows) < days:
        return {"unavailable": True, "reason": f"only {len(rows)} of {days} days in the daily table", "rows": rows}
    return {"unavailable": False, "rows": rows, "start": rows[0]["date"], "end": rows[-1]["date"]}


def orientation(brain: Brain, avatars: list[dict], all_rungs: list[dict], chart: dict, ends_on: str) -> list[dict]:
    """3 to 6 small numbers beside the plan: where customers stand, not the answer."""
    win = daily_window(brain.brand, ends_on)
    new_c = ret_share = None
    if not win["unavailable"]:
        new_c = sum(r.get("new_customer_orders") or 0 for r in win["rows"])
        orders = sum(r.get("orders") or 0 for r in win["rows"])
        ret = sum(r.get("returning_customer_orders") or 0 for r in win["rows"])
        ret_share = round(ret / orders, 4) if orders else None
    rep = None if chart["unavailable"] else chart["values"][-1]
    with_proof = sum(1 for a in avatars if a.get("top_objection") and a["top_objection"]["proof"])
    open_rungs = sum(1 for r in all_rungs if not r["proof_ids"])
    dates = [a["date"] for a in avatars if a["date"] != "undated"]
    fresh = (brain.today - dt.date.fromisoformat(min(dates))).days if dates else None
    why = win.get("reason")
    return [
        {"label": "new customers, 28d", "value": new_c, "unit": "n", "title": "first orders in the last 28 days, simulated",
         "unavailable_label": None if new_c is not None else "unavailable", "reason": why},
        {"label": "returning share of orders", "value": ret_share, "unit": "%", "title": "returning orders over all orders, 28 days, simulated"},
        {"label": "repeat in 3 months", "value": rep, "unit": "%",
         "title": "latest full cohort, active again in months 1 to 3, upper bound, simulated"},
        {"label": "avatars with proof", "value": with_proof if avatars else None, "unit": "n", "suffix": f" of {len(avatars)}",
         "title": "avatars whose top doubt has a proof record"},
        {"label": "rungs without proof", "value": open_rungs if all_rungs else None, "unit": "n",
         "tone": "bad" if open_rungs else None, "title": "objection ladder rungs with no proof record"},
        {"label": "oldest avatar check", "value": fresh, "unit": "n", "suffix": " days ago",
         "title": "days since the oldest avatar record was last dated"},
    ]


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
    return {"brand": brain.brand, "today": brain.today.isoformat(), "ends_on": ends_on, "version": brain.version(),
            "simulated_note": SIMULATED_NOTE, "orientation": orientation(brain, avatars, all_rungs, chart, ends_on),
            "avatars": avatars,
            "objections": objections, "angles": {k: angles[k] for k in ("available", "reason", "ads")},
            "language": audit.language_rows(brain), "voice": voice_sheet(brain)}


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


# ---------------------------------------------------------------- rank (depth contract section 5)

_rank_engine = None


def _engine():
    """app/rank.py, loaded once. The screen dresses its default actions with real titles."""
    global _rank_engine
    if _rank_engine is None:
        spec = importlib.util.spec_from_file_location("customers_avatars_rank_engine", APP / "rank.py")
        _rank_engine = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_rank_engine)
    return _rank_engine


def _title(f: dict) -> str | None:
    ent = f["entity"]
    if f["rule_id"] == "CUST-R01":
        return f"Back the {ent['label']} avatar with a second source"
    if f["rule_id"] == "CUST-R02":
        doubt = next((r for r in f["sentence"].split('"')[1:2]), ent["label"])
        return f"Answer \"{doubt}\""
    if f["rule_id"] == "CUST-R03" and f["status"] == "unavailable":
        return "Name the angle on every Meta ad so objection coverage can be read"
    if f["rule_id"] == "CUST-R03":
        return f"Brief an ad that answers the {ent['label']} doubt"
    return None


def rank(brand: str, window: dict) -> dict:
    eng = _engine()
    findings = audit.run(brand, window, BRAIN_ROOT)
    nr = eng.net_revenue_28d(brand, window)
    actions = []
    for f in findings:
        if f.get("status") not in ("open", "unavailable"):
            continue
        a = eng.action_from_finding(f, nr)
        a["title"] = _title(f) or a["title"]
        actions.append(a)
    return {"actions": actions}
