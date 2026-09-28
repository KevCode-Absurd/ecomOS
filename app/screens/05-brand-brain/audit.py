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

Money at stake is null for every rule: a brain gap has no revenue formula yet.
Confidence: one snapshot is one window (0.5), minus 0.2 when the input record
is past its shelf life.
"""
from __future__ import annotations

import datetime as dt
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
]
AUTONOMY = {"BRN-C12": "agent_does", "BRN-C07": "founder_gate", "BRN-C03": "agent_does"}


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


def run(brand: str, window: dict | None = None, root: Path | None = None) -> list[dict]:
    today = _today(window)
    brain = Brain(brand, root, today)
    ends_on = (today - dt.timedelta(days=1)).isoformat()
    try:
        bank = keeper.load_bank()
    except (OSError, ValueError, KeyError):
        bank = None
    out = rule_stale(brain, ends_on) + rule_claims(brain, ends_on)
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
