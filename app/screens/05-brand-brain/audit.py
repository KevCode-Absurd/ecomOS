"""Brand brain audit: where the brain itself is too old, too empty or too weak to lean on.

Contract: app/contracts/audit.md. `run(brand, window)` reads only
app/brain/<brand>/ (through app/brain/store.py and keeper.py) and returns
findings sorted by severity. No connector, no model, no writes. Same brain,
same window, same output.

Rules (thresholds are constants below):

BRN-R01 stale section. A section has records past `expires_at`, or its newest
    record is older than SHELF_DAYS (180). Severity low (a record past its
    shelf life is hygiene, audit.md section 5). Capability BRN-C12.
    Owner: 05-brand-brain.
BRN-R02 empty section a room needs. A field in app/brain/questions.bank.json
    has no active record, grouped by section; the rooms are the union of the
    bank questions that fill it. Severity medium (known downstream cost, no
    money formula). Capability BRN-C07. Owner: 05-brand-brain.
BRN-R03 unanswered high-weight question. A record in open_questions.json with
    no answered_on and a weight of HIGH_WEIGHT (8) or more. Weight comes from
    the bank question with the same id suffix, else the bank question that
    fills the whole section, else DEFAULT_WEIGHT (5). Severity high when the
    weight is 10, else medium. Capability BRN-C07 (founder gate).
    Owner: 05-brand-brain.
BRN-R04 unapproved claim used by copy. An objection ladder rung whose `uses`
    includes copy cites a claims record whose tier is not approved. Severity
    medium. Capability BRN-C03. Owner: 05-brand-brain; screen 04 owns the
    rung-with-no-proof rule (OFFER-R04), so it is not repeated here.
BRN-R05 format gap against competitors. In the Ad Library pull (market.py),
    the competitor median share of a format is at least 15 percent and the
    brand's share is under half of it. One finding per format. Severity
    medium. Capability CREA-C19 (select ad format). Reputation override 3:
    a creative coverage gap. Owner: 05-brand-brain (the brain holds the pull);
    screen 09 reads it from the findings table.
BRN-R06 hook-form gap against competitors. Same test on hook forms
    (question, first person, number, offer), plus a form the brand never uses
    while 3 or more competitor pages run it 5 times or more. Severity medium.
    Capability CREA-C04 (hook bank). Reputation override 3. Owner: 05-brand-brain.
BRN-R08 angle gap against competitors. In the coverage matrix (market.py),
    an angle that one or more competitor pages run and none of our ads lead
    with. Severity high when 3 or more pages run it, else medium. Capability
    CREA-C06 (concept brief). Reputation override 5 when the angle is one the
    brain's own positioning names (a competitor position gap), else 3.
    Owner: 05-brand-brain.
BRN-R09 recommended instead with no answer. A competitor that public threads
    recommend instead of the brand (competitors records with
    `recommended_instead`). Severity high at 3 or more threads, else medium.
    Capability BRAND-C57 (battlecard, agent does; the copy it feeds is
    approved on its own screen). Reputation override 5: a competitor position
    gap named in the brain. Owner: 05-brand-brain.
BRN-R10 category frame not carried. The frame buyers use most in public
    threads (positioning.reddit_frames) has no line in the brand's positioning
    frame; or the brand has a giving model and public threads read it as a
    marketing brand more often than a giving brand. Severity medium.
    Capability CREA-C03 (angles and positioning). Reputation override 3.
    Owner: 05-brand-brain.
BRN-R11 section a room needs is mostly inferred or unverified. Half or more
    of a section's active records are inferred or unverified and a room reads
    it (health.py, WEAK_SHARE 0.5). Severity medium. Capability BRN-C07
    (founder round, agent drafts). Owner: 05-brand-brain.
BRN-R07 competitor snapshot stale. A configured Ad Library page was captured
    more than SNAPSHOT_STALE_DAYS (7) ago, or never. Severity low. Capability
    BRN-C11 (competitor snapshot, signals only). Owner: 05-brand-brain.

Money at stake is null for every rule: a brain gap has no revenue formula yet.
Confidence: one snapshot is one window (0.5), minus 0.2 when the input record
is past its shelf life.
"""
from __future__ import annotations

import datetime as dt
import importlib.util
import json
import sys
from pathlib import Path

APP = Path(__file__).resolve().parents[2]
BRAIN_DIR = APP / "brain"
if str(BRAIN_DIR) not in sys.path:
    sys.path.insert(0, str(BRAIN_DIR))

import keeper  # noqa: E402
from store import SECTIONS, Brain  # noqa: E402

SCREEN = "05-brand-brain"
SHELF_DAYS = 180
HIGH_WEIGHT = 8
DEFAULT_WEIGHT = 5
SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}
META_SECTIONS = {"freshness", "open_questions", "changes"}

RULES = [
    {"rule_id": "BRN-R01", "name": "stale section", "entity_type": "brand",
     "inputs": ["brain sections"], "capability": "BRN-C12", "owner_screen": SCREEN},
    {"rule_id": "BRN-R02", "name": "empty section a room needs", "entity_type": "brand",
     "inputs": ["brain sections", "questions.bank.json"], "capability": "BRN-C07", "owner_screen": SCREEN},
    {"rule_id": "BRN-R03", "name": "unanswered high-weight question", "entity_type": "brand",
     "inputs": ["open_questions", "questions.bank.json"], "capability": "BRN-C07", "owner_screen": SCREEN},
    {"rule_id": "BRN-R04", "name": "unapproved claim used by copy", "entity_type": "ladder_rung",
     "inputs": ["objection_ladders", "claims"], "capability": "BRN-C03", "owner_screen": SCREEN},
    {"rule_id": "BRN-R05", "name": "format gap against competitors", "entity_type": "brand",
     "inputs": ["competitors (Ad Library pull)", "learnings", "config/apify.json"], "capability": "CREA-C19", "owner_screen": SCREEN},
    {"rule_id": "BRN-R06", "name": "hook-form gap against competitors", "entity_type": "brand",
     "inputs": ["competitors (Ad Library pull)", "learnings", "config/apify.json"], "capability": "CREA-C04", "owner_screen": SCREEN},
    {"rule_id": "BRN-R07", "name": "competitor snapshot stale", "entity_type": "brand",
     "inputs": ["competitors (Ad Library pull)", "config/apify.json"], "capability": "BRN-C11", "owner_screen": SCREEN},
    {"rule_id": "BRN-R08", "name": "angle gap against competitors", "entity_type": "brand",
     "inputs": ["competitors (Ad Library pull)", "learnings.hook_types", "claims", "objection_ladders"], "capability": "CREA-C06", "owner_screen": SCREEN},
    {"rule_id": "BRN-R09", "name": "recommended instead with no answer", "entity_type": "brand",
     "inputs": ["competitors (reddit_recommended)", "objection_ladders"], "capability": "BRAND-C57", "owner_screen": SCREEN},
    {"rule_id": "BRN-R10", "name": "category frame not carried", "entity_type": "brand",
     "inputs": ["positioning.reddit_frames", "positioning.frame", "identity.giving_model", "story_bank"], "capability": "CREA-C03", "owner_screen": SCREEN},
    {"rule_id": "BRN-R11", "name": "section a room needs is mostly inferred or unverified", "entity_type": "brand",
     "inputs": ["brain sections", "questions.bank.json"], "capability": "BRN-C07", "owner_screen": SCREEN},
]
AUTONOMY = {"BRN-C12": "agent_does", "BRN-C07": "founder_gate", "BRN-C03": "agent_does",
            "CREA-C19": "agent_does", "CREA-C04": "agent_does", "BRN-C11": "agent_does", "CREA-C06": "agent_does",
            "BRAND-C57": "agent_does", "CREA-C03": "agent_does"}

_hspec = importlib.util.spec_from_file_location("brand_brain_health", Path(__file__).resolve().parent / "health.py")
health = importlib.util.module_from_spec(_hspec)
_hspec.loader.exec_module(health)
_mspec = importlib.util.spec_from_file_location("brand_brain_market", Path(__file__).resolve().parent / "market.py")
market = importlib.util.module_from_spec(_mspec)
_mspec.loader.exec_module(market)


def _today(window) -> dt.date:
    """Ages count from the day after the window's last full day."""
    if window and window.get("ends_on"):
        return dt.date.fromisoformat(str(window["ends_on"])) + dt.timedelta(days=1)
    return dt.date.today()


def _row(metric, value, unit, ends_on, freshness_days, baseline, source):
    return {"metric": metric, "value": value, "unit": unit, "window": "as of now",
            "ends_on": ends_on, "freshness_days": freshness_days, "baseline": baseline,
            "baseline_kind": "threshold", "source": source, "simulated": False}


def _finding(rule_id, severity, entity, evidence, sentence, brain_refs, ends_on, confidence=0.5):
    cap = next(r["capability"] for r in RULES if r["rule_id"] == rule_id)
    return {"id": f"{SCREEN}.{rule_id}.{entity['id']}", "screen": SCREEN, "rule_id": rule_id,
            "severity": severity, "entity": entity, "evidence": evidence, "sentence": sentence,
            "capability": {"id": cap, "autonomy": AUTONOMY[cap]},
            "money_at_stake": None,
            "confidence": round(max(0.1, confidence), 2), "brain_refs": brain_refs,
            "first_seen": ends_on, "last_seen": ends_on, "status": "open", "unavailable": None,
            "money_reason": "brain gap: no revenue formula yet"}


def question_weight(oq: dict, bank: list[dict]) -> int:
    """Weight of an open_questions record, looked up in the question bank."""
    field, section = oq.get("field"), (oq.get("value") or {}).get("section")
    for q in bank:
        if q["id"].split(".")[-1] == field and any(f.split(".")[0] == section for f in q["fills"]):
            return q["weight"]
    whole = [q["weight"] for q in bank if section in q["fills"]]
    return max(whole) if whole else DEFAULT_WEIGHT


def rule_stale(brain: Brain, ends_on: str) -> list[dict]:
    out = []
    for sec, st in brain.section_stats().items():
        if sec in META_SECTIONS or not st["count"]:
            continue
        age = (brain.today - dt.date.fromisoformat(st["last_update"])).days if st["last_update"] else None
        old = age is not None and age > SHELF_DAYS
        if not st["stale"] and not old:
            continue
        ev = [_row("stale_records", st["stale"], "n", ends_on, age, 0, f"brain.{sec}"),
              _row("days_since_update", age, "days", ends_on, age, SHELF_DAYS, f"brain.{sec}")]
        if st["stale"]:
            sentence = f"{st['stale']} of {st['count']} {sec} records are past their shelf life."
        else:
            sentence = f"The {sec} section was last updated {age} days ago. The shelf life is {SHELF_DAYS} days."
        ids = [r["id"] for r in brain.records(sec) if r["status"] == "stale"][:10]
        out.append(_finding("BRN-R01", "low", {"type": "brand", "id": f"section_{sec}", "label": sec},
                            ev, sentence, ids, ends_on, 0.5 - 0.2))
    return out


def rule_empty(brain: Brain, bank: list[dict], ends_on: str) -> list[dict]:
    by_sec: dict[str, dict] = {}
    for g in keeper.gaps(brain, bank):
        if g["kind"] != "empty":
            continue
        s = by_sec.setdefault(g["section"], {"fields": [], "rooms": set()})
        s["fields"].append(g["field"])
        s["rooms"].update(g["rooms"])
    out = []
    for sec in sorted(by_sec):
        s = by_sec[sec]
        rooms = sorted(s["rooms"])
        ev = [_row("empty_fields", len(s["fields"]), "n", ends_on, None, 0, "questions.bank.json"),
              _row("rooms_blocked", len(rooms), "n", ends_on, None, 0, "questions.bank.json")]
        names = ", ".join(f.split(".", 1)[1].replace("_", " ") for f in s["fields"])
        sentence = (f"{sec.replace('_', ' ')} has no record for {names}. "
                    f"{len(rooms)} rooms need it: {', '.join(r.replace('_', ' ') for r in rooms)}.")
        out.append(_finding("BRN-R02", "medium", {"type": "brand", "id": f"section_{sec}", "label": sec},
                            ev, sentence, [], ends_on))
    return out


def rule_questions(brain: Brain, bank: list[dict], ends_on: str) -> list[dict]:
    out = []
    for oq in brain.records("open_questions"):
        v = oq.get("value") or {}
        if v.get("answered_on"):
            continue
        w = question_weight(oq, bank)
        if w < HIGH_WEIGHT:
            continue
        ev = [_row("question_weight", w, "n", ends_on, None, HIGH_WEIGHT, "open_questions")]
        sentence = f"No answer yet to: {v.get('question') or oq.get('text')} {v.get('why') or ''}".strip()
        out.append(_finding("BRN-R03", "high" if w >= 10 else "medium",
                            {"type": "brand", "id": f"question_{oq['field']}", "label": oq["field"]},
                            ev, sentence, [oq["id"]], ends_on))
    return out


def rule_claims(brain: Brain, ends_on: str) -> list[dict]:
    claims = {r["id"]: r for r in brain.records("claims")}
    out = []
    for lad in brain.records("objection_ladders"):
        v = lad.get("value")
        if not isinstance(v, dict):
            continue  # founder answers to ladder questions live here too; only ladders have rungs
        theme = v.get("theme") or lad.get("field")
        for rung in v.get("rungs") or []:
            if "copy" not in (rung.get("uses") or []):
                continue
            for pid in rung.get("proof_ids") or []:
                c = claims.get(pid)
                if not c or c["tier"] == "approved":
                    continue
                counts = rung.get("counts") or {}
                ev = [_row("one_star_mentions", counts.get("one_star"), "n", ends_on, c["age_days"], None,
                           "objection_ladders"),
                      _row("claim_tier_approved", 0, "flag", ends_on, c["age_days"], 1, "claims")]
                sentence = (f"Copy on the {theme.replace('_', ' ')} ladder, rung {rung.get('level')}, leans on "
                            f"the {c['field'].replace('_', ' ')} claim. It is {c['tier'].replace('_', ' ')}, "
                            f"not approved.")
                ent = {"type": "ladder_rung", "id": f"{theme}.rung_{rung.get('level')}.{pid.split('.')[-1]}",
                       "label": f"{theme}, rung {rung.get('level')}: {rung.get('doubt')}"}
                out.append(_finding("BRN-R04", "medium", ent, ev, sentence, [lad["id"], pid], ends_on))
    return out


def _pct(x) -> str:
    return f"{round(x * 100)} percent" if isinstance(x, (int, float)) else "unavailable"


def rule_competitor_gaps(brain: Brain, ends_on: str) -> list[dict]:
    out = []
    for g in market.gaps(brain):
        rid = "BRN-R05" if g["kind"] == "format" else "BRN-R06"
        if g["kind"] == "long_runner":
            continue  # reported on the screen; a rule for it needs the brand's own ad rows (screen 09)
        ev = [_row(f"{g['kind']}_share_us", g["us"], "share", ends_on, None, g["them"], "competitors (Ad Library pull)"),
              _row(f"{g['kind']}_share_competitor_median", g["them"], "share", ends_on, None, None, "competitors (Ad Library pull)"),
              _row("ads_seen_us", g["us_total"], "n", ends_on, None, None, "learnings")]
        lead = ", ".join(f"{x['name']} {_pct(x['share'])}" for x in g["leaders"][:2])
        what = g["label"].lower() + (" ads" if g["kind"] == "format" else " hooks")
        if g.get("never"):
            sentence = f"We run no {what}. {len(g['leaders'])} competitor pages do: {lead}."
        else:
            sentence = f"{_pct(g['us'])} of our ads are {what}. The competitor median is {_pct(g['them'])}: {lead}."
        ent = {"type": "brand", "id": f"{g['kind']}_{g['key']}", "label": f"{g['label']} {'ads' if g['kind'] == 'format' else 'hooks'}"}
        f = _finding(rid, "medium", ent, ev, sentence, g["record_ids"][:6], ends_on, 0.5)
        f["gap"] = {k: g[k] for k in ("kind", "key", "label", "us", "them", "us_n", "us_total", "leaders")}
        out.append(f)
    return out


def rule_angle_gaps(brain: Brain, ends_on: str) -> list[dict]:
    out = []
    c = market.coverage(brain)
    own = {u["angle"] for u in c.get("unused_own") or []}
    for g in c["gaps"]:
        n = len(g["competitors"])
        ev = [_row("competitor_pages_running_angle", n, "n", ends_on, None, 1, "competitors (Ad Library pull)"),
              _row("our_ads_on_angle", 0, "n", ends_on, None, 1, "learnings.hook_types"),
              _row("our_ads_read", g["us_total"], "n", ends_on, None, None, "learnings.hook_types")]
        names = ", ".join(g["competitors"][:3])
        sentence = f"{n} competitor page{'s lead' if n != 1 else ' leads'} with {g['label'].lower()} ({names}). None of our {g['us_total'] or 'read'} ads do."
        f = _finding("BRN-R08", "high" if n >= 3 else "medium", {"type": "brand", "id": f"angle_{g['angle']}", "label": g["label"]},
                     ev, sentence, g["record_ids"][:6], ends_on, 0.5)
        f["draft"] = g["brief"]
        f["own_positioning"] = g["angle"] in own
        out.append(f)
    return out


def rule_signals(brain: Brain, ends_on: str) -> list[dict]:
    out = []
    sg = market.signals(brain)
    for r in sg["recommended"]:
        n = r["threads"] or 0
        lad = r.get("ladder") or {}
        db = lad.get("deal_breaker") or {}
        ev = [_row("threads_recommending_instead", n, "n", ends_on, None, 1, "competitors (reddit_recommended)"),
              _row("upvotes", r["upvotes"], "n", ends_on, None, None, "competitors (reddit_recommended)"),
              _row("deal_breaker_proof", 1 if db.get("has_proof") else 0, "flag", ends_on, None, 1, "objection_ladders")]
        subs = ", ".join("r/" + x for x in r["subreddits"][:2])
        tail = (f"The doubt behind it is {r['doubt_label'].lower()}. Our {lad.get('theme', '').replace('_', ' ')} ladder has no proof on rung {db.get('level')}."
                if lad and not db.get("has_proof") else
                f"The doubt behind it is {r['doubt_label'].lower()}." + (" We have no ladder for it." if not lad else " Proof is on file on the ladder."))
        sentence = f"Public threads recommend {r['competitor']} instead of us {n} time{'s' if n != 1 else ''} ({r['upvotes']} upvotes, {subs}). {tail}"
        f = _finding("BRN-R09", "high" if n >= 3 else "medium", {"type": "brand", "id": f"recommended_{r['slug']}", "label": r["competitor"]},
                     ev, sentence, [r["record_id"]] + ([lad["id"]] if lad else []), ends_on, 0.5)
        f["where"] = r["where"]
        f["doubt_angle"] = r["doubt_angle"]
        out.append(f)
    top = sg.get("top_frame")
    if top and top.get("covered_by_our_frame") is False and sg.get("our_frame"):
        total = sum(x["mentions"] or 0 for x in sg["frames"])
        ev = [_row("frame_mentions", top["mentions"], "n", ends_on, None, None, "positioning.reddit_frames"),
              _row("frame_mentions_total", total, "n", ends_on, None, None, "positioning.reddit_frames"),
              _row("frame_in_our_positioning", 0, "flag", ends_on, None, 1, "positioning.frame")]
        sentence = f"Buyers frame the category as {top['label']} in {top['mentions']} of {total} mentions. Our positioning frame has no line for it."
        out.append(_finding("BRN-R10", "medium", {"type": "brand", "id": f"frame_{top['frame']}", "label": top["label"]},
                            ev, sentence, [sg["sources"]["frames"], sg["our_frame"]["id"]], ends_on, 0.5))
    mm = sg.get("mission_vs_marketing")
    if mm and (mm["mission"] or 0) <= (mm["marketing"] or 0):
        ev = [_row("read_as_marketing_brand", mm["marketing"], "n", ends_on, None, mm["mission"], "positioning.reddit_frames"),
              _row("read_as_giving_brand", mm["mission"], "n", ends_on, None, None, "positioning.reddit_frames")]
        sentence = (f"Public threads read us as a marketing brand {mm['marketing']} times and as a giving brand {mm['mission']} time{'s' if mm['mission'] != 1 else ''}. "
                    + (mm["text"] if mm.get("text") else "The giving model is in the brain and not in the ads."))
        out.append(_finding("BRN-R10", "medium", {"type": "brand", "id": "frame_mission", "label": "mission read as marketing"},
                            ev, sentence, mm["record_ids"], ends_on, 0.5))
    return out


def rule_weak_sections(brain: Brain, ends_on: str) -> list[dict]:
    out = []
    for s in health.heatmap(brain)["sections"]:
        if s["verdict"]["kind"] != "ask" or not s["records"]:
            continue
        ev = [_row("weak_share", round(s["weak_share"], 2), "share", ends_on, s["age_days"], health.WEAK_SHARE, f"brain.{s['section']}"),
              _row("rooms_reading", len(s["rooms"]), "n", ends_on, None, 1, "questions.bank.json")]
        sentence = (f"{round(s['weak_share'] * 100)} percent of {s['section'].replace('_', ' ')} is inferred or unverified. "
                    f"{len(s['rooms'])} rooms read it: {', '.join(r.replace('_', ' ') for r in s['rooms'][:4])}.")
        f = _finding("BRN-R11", "medium", {"type": "brand", "id": f"section_{s['section']}", "label": s["section"]},
                     ev, sentence, [], ends_on, 0.5)
        f["steps"] = s["verdict"]["steps"]
        out.append(f)
    return out


def rule_snapshot_stale(brain: Brain, ends_on: str) -> list[dict]:
    out = []
    d = market.pages(brain)
    for p in d["pages"]:
        if p["role"] != "competitor":
            continue
        age = p["age_days"]
        if p["pulled"] and age is not None and age <= market.SNAPSHOT_STALE_DAYS:
            continue
        if not p["pulled"] and not p["page_id"]:
            continue  # no page id: that is a founder task on the screen, not a stale snapshot
        ev = [_row("competitor_snapshot_age", age, "days", ends_on, age, market.SNAPSHOT_STALE_DAYS, "competitors (Ad Library pull)")]
        sentence = (f"{p['name']} was last captured {age} days ago. The shelf life is {market.SNAPSHOT_STALE_DAYS} days."
                    if age is not None else f"{p['name']} has a page id but no capture yet.")
        out.append(_finding("BRN-R07", "low", {"type": "brand", "id": f"snapshot_{p['slug']}", "label": p["name"]},
                            ev, sentence, p["record_ids"][:3], ends_on, 0.5))
    return out


def run(brand: str, window: dict | None = None, root: Path | None = None) -> list[dict]:
    today = _today(window)
    brain = Brain(brand, root, today)
    ends_on = (today - dt.timedelta(days=1)).isoformat()
    try:
        bank = keeper.load_bank()
    except (OSError, ValueError, KeyError):
        bank = None
    out = rule_stale(brain, ends_on) + rule_claims(brain, ends_on) + rule_competitor_gaps(brain, ends_on) + rule_angle_gaps(brain, ends_on) + rule_signals(brain, ends_on) + rule_weak_sections(brain, ends_on) + rule_snapshot_stale(brain, ends_on)
    if bank is None:
        for rid, sev in (("BRN-R02", "medium"), ("BRN-R03", "medium")):
            f = _finding(rid, sev, {"type": "brand", "id": "question_bank", "label": "question bank"},
                         [], "The question bank could not be read.", [], ends_on)
            f.update(status="unavailable", unavailable={"inputs": ["app/brain/questions.bank.json"],
                     "connector": "none, a repo file", "fix": "Restore questions.bank.json."})
            out.append(f)
    else:
        out += rule_empty(brain, bank, ends_on) + rule_questions(brain, bank, ends_on)
    out.sort(key=lambda f: (SEVERITY_ORDER[f["severity"]], f["id"]))
    return out


if __name__ == "__main__":
    b = sys.argv[1] if len(sys.argv) > 1 else "bombas"
    print(json.dumps(run(b), indent=1))
