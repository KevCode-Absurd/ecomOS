"""Customers and avatars screen API: /api/02-customers-avatars/...

Brand facts come from app/brain/<brand>/ through app/brain/store.py (avatars, objections,
objection_ladders, language_bank, voice, claims). Repeat by cohort comes from the brand's
simulated aggregates (cohorts.json) through app/data/tables.py. The only write is a
founder-marked voice example, through Brain.put. Nothing external, no model.

  GET  overview          orientation numbers, avatar cards, objection map, language bank,
                         voice sheet
  GET  rank              served by app/rank.py, which calls `rank(brand, window)` below when present
  GET  audit             findings from audit.py (app/contracts/audit.md shape) and RULES
  POST avatars/draft      {segment}: writes the drafted avatar for an unserved situation, tier inferred
  GET  handoff             ready artefacts for 09-creative, 10-copy, 07-landing-pages-cro and 14-email-messaging
  GET  report              a plain-words monthly customer report for the founder, printable
  GET  agenda              every dated move in the next 30 days, and anything overdue
  GET  tests               tests this screen proposes, as experiment registry rows with status proposed
  GET  avatar/<key>/brief  a plain-text one-pager for one avatar, for a creator or agency
  POST voice/check        {text}: pass, warn or fail against the writing rules, voice sheet and claims; no write
  POST messaging/approve  writes the drafted messaging hierarchy as an approved founder positioning record
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
SIMULATED_NOTE = ("{name} is the sample brand. Avatars, objections and customer words come from public reviews "
                  "and its own site. Every sales and repeat number here is simulated.")
PAGE_NAMES = {"": "Homepage", "pages/about-us": "About page", "policies/terms-of-service": "Legal terms",
              "pages/happiness-guarantee": "Guarantee page"}
EXAMPLE_FIELD = re.compile(r"^(liked|disliked)_example_[0-9a-f]{8}$")
UI_AUTONOMY = {"agent_does": "agent", "founder_gate": "founder_gate", "human_assist": "human_assist"}

_spec = importlib.util.spec_from_file_location("customers_avatars_audit", HERE / "audit.py")
audit = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(audit)
_spec = importlib.util.spec_from_file_location("customers_avatars_builds", HERE / "builds.py")
builds = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(builds)


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


# ---------------------------------------------------------------- avatar drafts from gaps

def avatar_drafts(brain: Brain, served: dict) -> list[dict]:
    out = []
    for sg in served["segments"]:
        if sg["verdict"] not in ("gap", "watch"):
            continue
        d = builds.draft_avatar(brain.brand, sg["segment"], brain.records("language_bank"), sg["theirs"], brain.today.isoformat(), audit.source_name)
        if d:
            d["exists"] = any(r.get("id") == d["record"]["id"] for r in brain.raw("avatars"))
            out.append(d)
    return out


def add_avatar_draft(brain: Brain, body: dict):
    """Founder approves a drafted avatar: it is written to the brain as an inferred record, never as a fact."""
    seg = str((body or {}).get("segment") or "")
    served = builds.served(audit.avatar_rows(brain), audit.rungs(brain), brain.records("competitors"), brain.records("positioning"))
    match = next((d for d in avatar_drafts(brain, served) if d["segment"] == seg), None)
    if match is None:
        return 400, {"error": "no draft for that segment"}
    if match["exists"]:
        return 409, {"error": "already in the brain", "record": match["record"]["id"]}
    errs = brain.put(match["record"])
    if errs:
        return 400, {"error": "record not valid", "details": errs}
    return 201, {"ok": True, "record": match["record"]["id"]}


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


def _cohorts(brand: str, avatars: list[dict]) -> dict:
    try:
        from tables import brand_data
        data = brand_data(brand)
        rows, monthly, as_of = data.table("cohorts"), data.table("monthly"), data.brand.get("as_of")
    except (ImportError, ValueError, KeyError, FileNotFoundError) as exc:
        return {"available": False, "reason": f"no cohort table for {brand} ({exc})", "rows": [], "moves": []}
    return builds.cohort_grid(rows, monthly, as_of, avatars)


def _mix(brand: str) -> dict:
    try:
        from tables import brand_data
        data = brand_data(brand)
        monthly, channels, as_of = data.table("monthly"), data.table("channels_monthly"), data.brand.get("as_of")
    except (ImportError, ValueError, KeyError, FileNotFoundError) as exc:
        return {"available": False, "reason": f"no monthly or channel table for {brand} ({exc})", "moves": []}
    return builds.mix(monthly, channels, as_of)


def _paths(brand: str) -> dict:
    return audit.load_paths(brand)


def _moments(brand: str, avatars: list[dict]) -> dict:
    return audit.load_moments(brand, avatars)


def _competitor_names(brain: Brain) -> list[str]:
    return audit.competitor_names(brain)


def _health(brand: str, avatars: list[dict]) -> dict:
    try:
        from tables import brand_data
        data = brand_data(brand)
        monthly, as_of = data.table("monthly"), data.brand.get("as_of")
    except (ImportError, ValueError, KeyError, FileNotFoundError) as exc:
        return {"available": False, "reason": str(exc), "rows": [], "missing": builds.MISSING_LINES, "moves": []}
    return builds.health(monthly, audit.load_cohorts(brand, avatars).get("rows", []), as_of)


def _returns(brain: Brain, avatars: list[dict], all_rungs: list[dict]) -> dict:
    mis = builds.misreads(brain.records("avatars"), avatars, all_rungs, brain.records("language_bank"), brain.records("products"))
    if not mis.get("available"):
        return {"rows": [], "line": mis.get("reason"), "tickets": {"available": False, "reason": mis.get("reason"), "fix": ""}, "refund_share_3m": None}
    buys = builds.avatar_lines(brain.records("avatars"), all_rungs, brain.records("language_bank"), {l["line"] for l in mis["lines"]})
    try:
        from tables import brand_data
        data = brand_data(brain.brand)
        monthly, as_of = data.table("monthly"), data.brand.get("as_of")
    except (ImportError, ValueError, KeyError, FileNotFoundError):
        monthly, as_of = [], (brain.today - dt.timedelta(days=1)).isoformat()
    return builds.return_risk(avatars, buys, mis["lines"], monthly, as_of)


def _split(brain: Brain, avatars: list[dict], all_rungs: list[dict]) -> dict:
    issues = {}
    for r in brain.records("products"):
        v = r.get("value")
        if r.get("field") == "review_summary" and isinstance(v, dict) and v.get("product_line"):
            issues[v["product_line"]] = v.get("issues") or []
    buys = builds.avatar_lines(brain.records("avatars"), all_rungs, brain.records("language_bank"), set(issues))
    return builds.split_check(avatars, all_rungs, buys, issues)


def _hierarchy(brain: Brain, avatars: list[dict], all_rungs: list[dict], lad: dict) -> dict:
    ends = (brain.today - dt.timedelta(days=1)).isoformat()
    th = builds.theme_impact(brain.records("language_bank"), lad["rows"], ends)
    pc = builds.perception(brain.records("positioning") + brain.records("identity"), brain.records("language_bank"), _brand_tokens(brain), audit.source_name)
    texts = {}
    for sec in ("offers", "policies", "claims"):
        for r in brain.records(sec):
            texts[r["id"]] = r.get("text")
    frame = next((r.get("value") for r in brain.records("positioning") if r.get("field") == "frame" and isinstance(r.get("value"), str)), None)
    h = builds.hierarchy(th, pc, lad["rows"], all_rungs, texts, frame, brain.brand, brain.today.isoformat())
    h["approved"] = any(r.get("id") == h["record"]["id"] for r in brain.raw("positioning"))
    return h


def proposed(brain: Brain) -> dict:
    """Tests this screen proposes, in the experiment registry row shape (contracts/events.md)."""
    d = overview(brain)
    rows = builds.proposed_tests(d, brain.brand, d["ends_on"])
    return {"brand": brain.brand, "simulated": True, "status": "proposed", "rows": rows,
            "note": "25-experiments assigns ids, checks audience overlap and reads results. Nothing starts before a person approves."}


def avatar_brief(brain: Brain, key: str):
    if not SAFE_BRAND.match(key or ""):
        return 400, {"error": "bad avatar key"}
    d = overview(brain)
    a = next((x for x in d["avatars"] if x["key"] == key), None)
    if a is None:
        return 404, {"error": "no such avatar", "key": key}
    forbidden = [c["text"] for c in d["voice"]["claims"] if c["tier"] == "forbidden" and c["text"]]
    return {"key": key, "name": a["name"], "text": builds.one_pager(a, d, forbidden)}


def check_line(brain: Brain, body: dict):
    """Check a pasted line against the writing rules, the voice sheet and the claims register. No write."""
    text = str((body or {}).get("text") or "")[:MAX_EXAMPLE]
    v = voice_sheet(brain)
    forbidden = [c["text"] for c in v["claims"] if c["tier"] == "forbidden" and c["text"]]
    disliked = [d["text"] for d in v["disliked"] if d["text"]]
    gap = builds.copy_gap({s_: brain.records(s_) for s_ in audit.OUR_SECTIONS}, brain.records("language_bank"), _brand_tokens(brain), audit.source_name)
    words = [r["word"] for r in gap.get("rows", [])][:12]
    return builds.voice_check(text, forbidden, disliked, words, _brand_tokens(brain))


def approve_hierarchy(brain: Brain):
    avatars = audit.avatar_rows(brain)
    all_rungs = audit.rungs(brain)
    h = _hierarchy(brain, avatars, all_rungs, builds.ladders(all_rungs, avatars))
    if not h["available"]:
        return 409, {"error": "nothing to approve yet: no review theme earns stars"}
    errs = brain.put(h["record"])
    if errs:
        return 400, {"error": "record not valid", "details": errs}
    return 201, {"ok": True, "record": h["record"]["id"]}


def _brand_name(brain: Brain) -> str:
    for r in brain.records("identity"):
        if r.get("field") in ("name", "brand_name") and isinstance(r.get("value"), str):
            return r["value"]
    return brain.brand.capitalize()


def _brand_tokens(brain: Brain) -> set[str]:
    return audit.brand_tokens(brain)


def _formats(brain: Brain, avatars: list[dict]) -> dict:
    f = builds.format_mix(brain.records("learnings"))
    for r in f.get("rows") or []:
        if r["gap"]:
            r["brief"] = builds.format_brief(r, avatars)
    return f


_OVERVIEW_CACHE: dict = {}
_CACHE_MAX = 8


def _data_stamp(brand: str) -> str:
    """Newest modified time of the brand's aggregates, so a data refresh rebuilds the overview."""
    folder = APP / "data" / "brands" / brand / "aggregates"
    try:
        return str(max((p.stat().st_mtime for p in folder.glob("*.json")), default=0))
    except OSError:
        return "0"


def overview(brain: Brain) -> dict:
    """The page's data, built once per brand, day, brain version and data state; callers get a copy."""
    import copy
    key = (brain.brand, brain.today.isoformat(), brain.version(), _data_stamp(brain.brand), str(BRAIN_ROOT))
    hit = _OVERVIEW_CACHE.get(key)
    if hit is None:
        hit = _build_overview(brain)
        if len(_OVERVIEW_CACHE) >= _CACHE_MAX:
            _OVERVIEW_CACHE.pop(next(iter(_OVERVIEW_CACHE)))
        _OVERVIEW_CACHE[key] = hit
    return copy.deepcopy(hit)


def _build_overview(brain: Brain) -> dict:
    ends_on = (brain.today - dt.timedelta(days=1)).isoformat()
    avatars = audit.avatar_rows(brain)
    all_rungs = audit.rungs(brain)
    angles = audit.ad_angles(brain.brand, ends_on)
    objections = audit.objection_rows(brain, all_rungs, angles)
    for a in avatars:
        top = audit.top_objection(a["id"], all_rungs)
        a["top_objection"] = None if top is None else {"id": top["id"], "doubt": top["doubt"], "one_star": top["one_star"],
                                                        "five_star": top["five_star"], "proof": bool(top["proof_ids"]),
                                                        "proof_text": top["proof"] if top["proof_ids"] else None}
        mine = [r for r in all_rungs if a["id"] in r["avatars"]]
        a["rungs"] = {"total": len(mine), "proven": sum(1 for r in mine if r["proof_ids"])}
        a["channels"] = builds.channels(a, a["count_by_source"], audit.source_name)
        a["next"] = builds.next_build(a, top)
    chart = repeat_by_cohort(brain.brand)
    gate = builds.gate(avatars, all_rungs)
    lad = builds.ladders(all_rungs, avatars)
    frc = builds.forces(avatars, all_rungs, brain.records("language_bank"), _competitor_names(brain))
    srv = builds.served(avatars, all_rungs, brain.records("competitors"), brain.records("positioning"))
    win = daily_window(brain.brand, ends_on)
    opd = sum(r.get("orders") or 0 for r in win["rows"]) / len(win["rows"]) if not win["unavailable"] else None
    focus = builds.focus(avatars, srv, builds.ad_voice(avatars, brain.records("learnings")), lad["rows"])
    out = {"brand": brain.brand, "today": brain.today.isoformat(), "ends_on": ends_on, "version": brain.version(), "focus": focus,
            "simulated_note": SIMULATED_NOTE.format(name=_brand_name(brain)), "orientation": orientation(brain, avatars, all_rungs, chart, ends_on),
            "avatars": avatars,
            "objections": objections, "angles": {k: angles[k] for k in ("available", "reason", "ads")},
            "language": audit.language_rows(brain), "voice": voice_sheet(brain),
            "cohorts": _cohorts(brain.brand, avatars), "mix": _mix(brain.brand),
            "misreads": builds.misreads(brain.records("avatars"), avatars, all_rungs, brain.records("language_bank"), brain.records("products")),
            "served": srv,
            "drafts": avatar_drafts(brain, srv),
            "coverage": builds.coverage(avatars, all_rungs), "ladders": lad,
            "copy_gap": builds.copy_gap({sec: brain.records(sec) for sec in ("voice", "claims", "identity", "offers", "policies", "products", "visual", "story_bank")},
                                        brain.records("language_bank"), _brand_tokens(brain), audit.source_name),
            "paths": _paths(brain.brand), "gate": gate,
            "price": builds.price_doubts(avatars, all_rungs, brain.records("offers"), brain.records("products")),
            "rechecks": builds.rechecks(avatars, brain.records("objection_ladders"), brain.today.isoformat()),
            "marketplace": builds.marketplace(avatars, all_rungs, brain.records("language_bank"), audit.source_name),
            "macros": builds.macros(lad["rows"], all_rungs, {r["id"]: r.get("text") for r in brain.records("policies") if r.get("text")}), "returns": _returns(brain, avatars, all_rungs), "ad_voice": builds.ad_voice(avatars, brain.records("learnings")), "split": _split(brain, avatars, all_rungs),
            "naming": builds.naming(avatars, all_rungs, builds.hooks(brain.records("language_bank"), all_rungs, avatars, _brand_tokens(brain), audit.source_name)["rows"]),
            "timing": builds.doubt_timing(all_rungs, brain.records("language_bank"), ends_on, audit.source_name), "health": _health(brain.brand, avatars), "hierarchy": _hierarchy(brain, avatars, all_rungs, lad),
            "offer_map": builds.offer_map(avatars, all_rungs, brain.records("offers"), brain.records("policies") + brain.records("claims")),
            "lookalikes": builds.lookalikes(brain.records("competitors"), _brand_name(brain)),
            "claims_fire": builds.claims_fire(brain.records("claims"), brain.records("language_bank"), _brand_tokens(brain), audit.source_name,
                                              audit.product_words(brain)),
            "perception": builds.perception(brain.records("positioning") + brain.records("identity"), brain.records("language_bank"),
                                            _brand_tokens(brain), audit.source_name), "survey": builds.survey(gate["rows"], lad["rows"], frc["rows"], srv["segments"], opd),
            "moments": _moments(brain.brand, avatars),
            "forces": frc,
            "hooks": builds.hooks(brain.records("language_bank"), all_rungs, avatars, _brand_tokens(brain), audit.source_name),
            "themes": builds.theme_impact(brain.records("language_bank"), lad["rows"], ends_on),
            "words": builds.words(brain.records("language_bank"), all_rungs, avatars, _brand_tokens(brain), audit.source_name), "formats": _formats(brain, avatars)}
    out["strength"] = builds.strength(out)
    builds.card_meta(out)
    out["compare"] = builds.compare_rows(out)
    out["blocks"] = builds.block_notes(out)
    return out


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
    if req.method == "GET" and parts == ["handoff"]:
        d = overview(brain)
        return {"brand": brain.brand, "brain_version": d["version"], "simulated": True, "packs": builds.handoff(d),
                "note": "Reading screens pick these up from here or from the brain records they come from. Nothing is sent anywhere."}
    if req.method == "GET" and parts == ["report"]:
        d = overview(brain)
        w = {"ends_on": d["ends_on"], "days": 28, "trailing": 4}
        acts = rank(brain.brand, w)["actions"]
        eng = _engine()
        acts.sort(key=eng.sort_key)
        ag = builds.agenda(d, acts, builds.proposed_tests(d, brain.brand, d["ends_on"]), brain.today.isoformat())
        return builds.report(d, acts, ag, _brand_name(brain))
    if req.method == "GET" and parts == ["agenda"]:
        d = overview(brain)
        w = {"ends_on": d["ends_on"], "days": 28, "trailing": 4}
        acts = rank(brain.brand, w)["actions"]
        return builds.agenda(d, acts, builds.proposed_tests(d, brain.brand, d["ends_on"]), brain.today.isoformat())
    if req.method == "GET" and parts == ["tests"]:
        return proposed(brain)
    if req.method == "GET" and len(parts) == 3 and parts[0] == "avatar" and parts[2] == "brief":
        return avatar_brief(brain, parts[1])
    if req.method == "POST" and parts == ["voice", "check"]:
        return check_line(brain, req.body)
    if req.method == "POST" and parts == ["messaging", "approve"]:
        return approve_hierarchy(brain)
    if req.method == "POST" and parts == ["avatars", "draft"]:
        return add_avatar_draft(brain, req.body)
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


RULE_JOB = {"CUST-R01": "avatars", "CUST-R05": "avatars", "CUST-R06": "avatars", "CUST-R13": "avatars", "CUST-R14": "avatars",
            "CUST-R02": "doubts", "CUST-R03": "doubts", "CUST-R04": "doubts", "CUST-R11": "doubts", "CUST-R12": "doubts",
            "CUST-R10": "offers", "CUST-R18": "offers", "CUST-R20": "offers", "CUST-R21": "offers",
            "CUST-R07": "retention", "CUST-R08": "retention", "CUST-R09": "retention", "CUST-R15": "retention", "CUST-R16": "retention",
            "CUST-R23": "retention", "CUST-R24": "avatars", "CUST-R25": "avatars", "CUST-R26": "avatars", "CUST-R27": "avatars", "CUST-R28": "offers",
            "CUST-R29": "avatars", "CUST-R30": "avatars", "CUST-R17": "brand", "CUST-R19": "brand", "CUST-R22": "brand"}
EASE = {"agent": 5, "agent_drafts": 4, "person_draft": 3, "person": 2}


def _plans(brand: str, window: dict) -> dict:
    """The drafted work behind each finding, keyed by the finding's entity id, from the same builders the page uses."""
    ends = window["ends_on"]
    brain = Brain(brand, BRAIN_ROOT, dt.date.fromisoformat(ends) + dt.timedelta(days=1))
    avatars = audit.with_tops(audit.avatar_rows(brain), audit.rungs(brain))
    all_rungs = audit.rungs(brain)
    d = audit.desk(brain, avatars, all_rungs)
    plans = {}
    for a in avatars:
        plans[("CUST-R01", a["key"])] = builds.next_build(dict(a, quotes=[]), None) if a["grounding"] != "grounded" else None
        if a["grounding"] != "grounded":
            have = ", ".join(a["sources"]) or "no source"
            p = plans[("CUST-R01", a["key"])]
            p["title"] = f"Back the {a['name']} avatar with a second source"
            p["draft"] = "\n".join([f"DRAFT research note: second source for {a['name']}",
                                    f"Have: {a['quote_count']} quotes from {have}",
                                    "Need: 5 quotes from 2 or more independent sources, with links",
                                    "Where to look: review sites, marketplace reviews and our own site reviews not yet used",
                                    "Reddit lines count as language only, never as a testimonial"])
            p["owner"] = "agent_drafts"
            p["steps"] = p["steps"][:2] + [{"n": 3, "who": "agent", "text": "Write the quotes into the avatar record as a draft."},
                                           {"n": 4, "who": "person", "text": "Approve the record. The card re-grades itself."}]
    for row in d["ladders"]["rows"]:
        if row["action"]:
            plans[("rung", row["id"])] = row["action"]
    for r in d["misreads"].get("rows", []):
        plans[("CUST-R05", f"{r['line']}.{r['avatar_key']}")] = r["action"]
    for l in d["misreads"].get("lines", []):
        if l.get("action"):
            plans[("CUST-R10", "split_" + l["line"])] = l["action"]
    for sg in d["served"]["segments"]:
        if sg["action"]:
            plans[("CUST-R06", "situation_" + sg["segment"].replace(" ", "_"))] = sg["action"]
    for r in d["themes"].get("rows", []):
        if r.get("action"):
            plans[("CUST-R11", "theme_" + r["theme"])] = r["action"]
    if d["copy_gap"].get("action"):
        plans[("CUST-R12", "copy_gap")] = d["copy_gap"]["action"]
    win = daily_window(brand, ends)
    opd = sum(r.get("orders") or 0 for r in win["rows"]) / len(win["rows"]) if not win["unavailable"] else None
    sv = builds.survey(d["gate"]["rows"], builds.ladders(all_rungs, avatars)["rows"], d["forces"]["rows"], d["served"]["segments"], opd)
    plans[("CUST-R13", "provisional_avatars")] = sv["action"]
    for r in d["forces"]["rows"]:
        if r.get("action"):
            plans[("CUST-R14", "forces_" + r["key"])] = r["action"]
    for r in d["moments"].get("rows", []):
        plans[("CUST-R15", "moment_" + r["label"].lower().replace(" ", "_").replace("'", ""))] = r["action"]
    nm = builds.naming(avatars, all_rungs, [])
    plans[("CUST-R03", "ad_angles")] = nm["action"]
    if d["perception"].get("action"):
        plans[("CUST-R17", "perception_gap")] = d["perception"]["action"]
    for r in d["claims_fire"]["rows"]:
        if r["action"]:
            plans[("CUST-R18", "claim_" + r["id"].split(".")[-1])] = r["action"]
    for r in d["lookalikes"]["rows"]:
        plans[("CUST-R19", f"lookalike_{r['page_id']}")] = r["action"]
    if d["offer_map"].get("action"):
        plans[("CUST-R20", "pushed_offer")] = d["offer_map"]["action"]
    for m in d["timing"]["moves"]:
        plans[("CUST-R21", "season_" + m["theme"])] = m
    h = _hierarchy(brain, avatars, all_rungs, builds.ladders(all_rungs, avatars))
    plans[("CUST-R22", "messaging_hierarchy")] = {"title": "Approve one messaging hierarchy for every page and email", "kind": "brain_record",
        "owner": "person", "capability": {"id": "BRAND-C33", "autonomy": "founder_gate"}, "draft": "DRAFT " + h["record"]["text"],
        "steps": [{"n": 1, "who": "agent", "text": "Build the hierarchy from buyer evidence (done on this screen)."},
                  {"n": 2, "who": "person", "text": "Read it and press Approve. It becomes a positioning record."},
                  {"n": 3, "who": "agent", "text": "Check pages and emails against the lead line on the next audit."}]}
    for m in d["health"].get("moves", []):
        plans[("CUST-R23", "health_" + m["key"])] = m
    for r in d["split"]["rows"]:
        if r["verdict"] == "split" and r["action"]:
            plans[("CUST-R24", "split_" + r["key"])] = r["action"]
    for r in d["returns"].get("rows", []):
        if r.get("action"):
            plans[("CUST-R26", "returns_" + r["key"])] = r["action"]
    for r in d["marketplace"]["rows"]:
        if r["action"]:
            plans[("CUST-R27", "market_" + r["key"])] = r["action"]
    for r in d["price"]["rows"]:
        if r["action"]:
            plans[("CUST-R28", "price_" + r["key"])] = r["action"]
    if d["rechecks"].get("action"):
        plans[("CUST-R29", "rechecks")] = d["rechecks"]["action"]
    widen = {"kind": "research_note", "owner": "agent_drafts", "capability": {"id": "BRAND-C01", "autonomy": "agent_does"},
             "steps": [{"n": 1, "who": "agent", "text": "Plan the extra pulls by page id, inside the weekly cap, with the cost."},
                       {"n": 2, "who": "person", "text": "Approve the spend before any pull runs."},
                       {"n": 3, "who": "agent", "text": "Run the pulls and re-read the thin block."}]}
    plans[("CUST-R30", "thin_quotes")] = dict(widen, title="Widen the avatar quotes to 5 per avatar from 2 sources",
                                              draft="DRAFT pull plan\nReviews on our site, Amazon and review sites for each avatar's moments\nTarget: 5 quotes from 2 sources per avatar")
    plans[("CUST-R30", "thin_ads")] = dict(widen, title="Read every live ad, not a sample, by page id",
                                           draft="DRAFT pull plan\nAd Library by our page id, all active ads with hooks and formats\nTarget: every live ad")
    for r in d["ad_voice"].get("rows", []):
        if r["action"]:
            plans[("CUST-R25", "silent_" + r["key"])] = dict(r["action"], title=f"Give {r['name']} an ad: {r['action']['title'][0].lower()}{r['action']['title'][1:]}")
    for m in d["mix"].get("moves", []):
        if m["id"].endswith(".paid_returning"):
            plans[("CUST-R07", "returning_via_paid")] = m
    for m in d["cohorts"].get("moves", []):
        if ".retention.calendar_" in m["id"]:
            plans[("CUST-R08", "calendar_" + m["id"].split("calendar_")[1])] = m
        if m["id"].endswith(".age_break"):
            cb = d["cohorts"].get("age_break") or {}
            plans[("CUST-R09", f"age_month_{cb.get('month')}")] = m
    return plans


def _plan_for(f: dict, plans: dict) -> dict | None:
    rid, eid = f["rule_id"], f["entity"]["id"]
    if rid in ("CUST-R02", "CUST-R04"):
        return plans.get(("rung", eid))
    return plans.get((rid, eid))


def _title(f: dict, plan: dict | None) -> str | None:
    if f["rule_id"] == "CUST-R03" and f["status"] == "unavailable":
        return "Name the angle on every Meta ad so objection coverage can be read"
    if f["rule_id"] == "CUST-R03":
        return f"Brief an ad that answers the {f['entity']['label']} doubt"
    if f["rule_id"] == "CUST-R16" and f["status"] == "unavailable":
        return "Build the customer paths aggregate so gateway and win-back rules can run"
    if f["rule_id"] == "CUST-R11" and plan:
        return f"Lift stars on {f['entity']['label']}: {plan['title'][0].lower()}{plan['title'][1:]}"
    return plan["title"] if plan else None


def _rescore(a: dict, eng) -> None:
    r = a["rubric"]
    if a["status"] == "unavailable":
        r["ease"] = 1
    elif a["owner"] == "person":
        r["ease"] = EASE["person_draft"] if (a["artefact"] or {}).get("draft") else EASE["person"]
    else:
        r["ease"] = EASE[a["owner"]]
    if a["rule_id"] == "CUST-R05":
        r["reputation"] = max(r["reputation"], 4)   # review theme on the buy path, per the audit docstring
    if a["rule_id"] == "CUST-R26":
        r["satisfaction"] = max(r["satisfaction"], 4)   # returns, per the audit docstring
    if a["rule_id"] in ("CUST-R18", "CUST-R19"):
        r["reputation"] = 5                          # a disputed claim or an impostor using our name, per the audit docstring
    total = 0.0
    for k, w in eng.WEIGHTS.items():
        total += w * (r[k] if r[k] is not None else 2.5) / 5
    r["total"] = round(total, 1)


_RANK_CACHE: dict = {}


def rank(brand: str, window: dict) -> dict:
    """Every open or unavailable finding as an action with its real title, owner, steps and drafted artefact.
    Cached per brand, window, brain version and data state; callers get a copy."""
    import copy
    ver = Brain(brand, BRAIN_ROOT, dt.date.fromisoformat(window["ends_on"]) + dt.timedelta(days=1)).version()
    key = (brand, window["ends_on"], window.get("days"), ver, _data_stamp(brand), str(BRAIN_ROOT))
    if key not in _RANK_CACHE:
        if len(_RANK_CACHE) >= _CACHE_MAX:
            _RANK_CACHE.pop(next(iter(_RANK_CACHE)))
        _RANK_CACHE[key] = _build_rank(brand, window)
    return copy.deepcopy(_RANK_CACHE[key])


def _build_rank(brand: str, window: dict) -> dict:
    eng = _engine()
    findings = audit.run(brand, window, BRAIN_ROOT)
    nr = eng.net_revenue_28d(brand, window)
    plans = _plans(brand, window)
    actions = []
    for f in findings:
        if f.get("status") not in ("open", "unavailable"):
            continue
        a = eng.action_from_finding(f, nr)
        plan = _plan_for(f, plans)
        a["title"] = _title(f, plan) or a["title"]
        if plan and (f["status"] == "open" or f["rule_id"] == "CUST-R03"):
            a["owner"] = plan.get("owner") or a["owner"]
            a["steps"] = plan.get("steps") or a["steps"]
            art = plan.get("artefact") or {}
            kind = art.get("kind") or plan.get("kind") or a["artefact"]["kind"]
            a["artefact"] = {"kind": kind, "label": art.get("label") or builds_label(kind),
                             "draft": art.get("draft") or plan.get("draft")}
            for k in ("stop_rule", "check_on"):
                if plan.get(k):
                    a[k] = plan[k]
            a["dated"] = bool(plan.get("check_on"))
            a["plan_capability"] = plan.get("capability")
        ss = builds.size_stop(a["artefact"]["kind"], f.get("evidence") or [], f.get("money_at_stake"), a.get("check_on"))
        if ss["size"]:
            a["size"] = ss["size"]
            a["stop_rule"] = a.get("stop_rule") or ss["stop_rule"]
        if (a.get("stop_rule") or "").startswith("Stop if "):
            a["stop_rule"] = a["stop_rule"][len("Stop if "):]
        _rescore(a, eng)
        a["job"] = RULE_JOB.get(f["rule_id"], "avatars")
        a["_artefact_id"] = (plan or {}).get("id") if f["status"] == "open" else None
        actions.append(a)
    return {"actions": merge_same_artefact(actions)}


def merge_same_artefact(actions: list[dict]) -> list[dict]:
    """Findings that ask for the same drafted artefact become one action: the highest-scoring one leads and
    carries every finding id, so the founder approves the work once."""
    out, by = [], {}
    for a in sorted(actions, key=lambda x: (-(x["rubric"]["total"] or 0), x["id"])):
        key = a.pop("_artefact_id", None)
        if key and key in by:
            lead = by[key]
            lead["finding_ids"] = lead["finding_ids"] + [fid for fid in a["finding_ids"] if fid not in lead["finding_ids"]]
            lead.setdefault("also", []).append({"id": a["id"], "rule_id": a["rule_id"], "why": a["why"]})
            continue
        if key:
            by[key] = a
        out.append(a)
    for a in out:
        if a.get("also"):
            a["why"] = a["why"] + " Also answers " + str(len(a["also"])) + " more finding" + ("s" if len(a["also"]) > 1 else "") + "."
    return out


def builds_label(kind: str) -> str:
    return _engine().ARTEFACT_LABEL.get(kind, kind)
