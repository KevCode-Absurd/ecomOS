"""Copy audit: live ad copy that makes a claim the brain does not back, promises what its page
does not say, or breaks the voice rules.

Contract: app/contracts/audit.md. `run(brand, window, data=None, root=None)` reads the brain
(app/brain/<brand>/ through store.py), the screen fixtures (simulated copy sets and the
checker rules) and the ad table through app/metrics.py (spend by ad, Meta). No connector,
no model, no writes. Same inputs, same output.

Live ad: an ad in the ad table that spent on the window's last day (7 day window). Each
simulated ad runs one simulated copy set (fixtures/ad_copy.json, ad number modulo set count).
The finding entity is the copy set; its evidence names how many live ads run it.

Rules:

COPY-R01 unapproved claim in live copy. A live copy set has a line the claim check flags:
    a claim whose brain record is not tier approved or site_backed, a claim-like line with
    no record, a risk pattern (unproven superlative, durability promise, guarantee that does
    not match policy, health claim, named competitor) or Reddit words used as a testimonial.
    Severity high when a risk pattern or a Reddit testimonial fires, else medium.
    Capability LOOP-C12 (pre-delivery integrity gate, agent does). Owner: 10-copy.
COPY-R02 message mismatch. A live copy set names a claim or offer (matched to a brain record)
    that the landing page's captured records do not carry. Severity high when a missing item
    is an offer or price, else medium. Page records are brain records captured from that exact
    URL, not a live page scrape. Capability SITE-C39 (on-page persuasion copy, human assist).
    Owner: 10-copy; screen 07 owns page conversion, not message match.
COPY-R03 voice rule broken in live copy. A live copy set has an em dash, an inflated word,
    a sentence over 20 words or a reading grade over 10. Severity low (hygiene).
    Capability CREA-C26 (core copy rules, agent does). Owner: 10-copy.

Money at stake is null for every rule: a rejected ad or a broken promise has no revenue
formula in metrics.md yet. Spend on the live ads is written as evidence instead.
Confidence: one snapshot is one window (0.5); the ad table is fresh on the window end.
When the ad table cannot be read, each rule emits one `unavailable` finding.
"""
from __future__ import annotations

import datetime as dt
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parents[1]


def _lib():
    """copylib.py next to this file, under a name no other screen can shadow."""
    name = "screen_10_copy_lib"
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, HERE / "copylib.py")
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod
        spec.loader.exec_module(mod)
    return sys.modules[name]


copylib = _lib()

SCREEN = "10-copy"
WINDOW_DAYS = 7
SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}
HIGH_RISK = {"superlative", "durability_promise", "guarantee_mismatch", "health", "competitor"}

RULES = [
    {"rule_id": "COPY-R01", "name": "unapproved claim in live copy", "entity_type": "ad",
     "inputs": ["ad_rows", "brain claims, offers, policies, language_bank", "fixtures/ad_copy.json"],
     "capability": "LOOP-C12", "owner_screen": SCREEN},
    {"rule_id": "COPY-R02", "name": "message mismatch between ad and landing page", "entity_type": "ad",
     "inputs": ["ad_rows", "brain claims, offers, policies, voice by source URL", "fixtures/ad_copy.json"],
     "capability": "SITE-C39", "owner_screen": SCREEN},
    {"rule_id": "COPY-R03", "name": "voice rule broken in live copy", "entity_type": "ad",
     "inputs": ["ad_rows", "fixtures/copy_rules.json", "fixtures/ad_copy.json"],
     "capability": "CREA-C26", "owner_screen": SCREEN},
]
AUTONOMY = {"LOOP-C12": "agent_does", "SITE-C39": "human_assist", "CREA-C26": "agent_does"}
MONEY_REASON = "copy risk has no revenue formula yet; spend on the live ads is in evidence"

_METRICS = None


def metric_fn(data=None):
    """The server's Data.metric when given, else app/metrics.py compute (brand= picks the folder)."""
    global _METRICS
    if data is not None and hasattr(data, "metric"):
        return data.metric
    if _METRICS is None:
        spec = importlib.util.spec_from_file_location("copy_audit_metrics", APP / "metrics.py")
        _METRICS = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_METRICS)
    return lambda name, **kw: _METRICS.compute(name, None, **kw)


def _row(metric, value, unit, ends_on, baseline, source, simulated, window=f"{WINDOW_DAYS}d"):
    return {"metric": metric, "value": value, "unit": unit, "window": window, "ends_on": ends_on,
            "freshness_days": 0 if simulated else None, "baseline": baseline, "baseline_kind": "threshold",
            "source": source, "simulated": simulated}


def _finding(rule_id, severity, entity, evidence, sentence, brain_refs, ends_on, confidence=0.5):
    cap = next(r["capability"] for r in RULES if r["rule_id"] == rule_id)
    return {"id": f"{SCREEN}.{rule_id}.{entity['id']}", "screen": SCREEN, "rule_id": rule_id,
            "severity": severity, "entity": entity, "evidence": evidence, "sentence": sentence,
            "capability": {"id": cap, "autonomy": AUTONOMY[cap]}, "money_at_stake": None,
            "confidence": round(max(0.1, confidence), 2), "brain_refs": sorted(set(brain_refs)),
            "first_seen": ends_on, "last_seen": ends_on, "status": "open", "unavailable": None,
            "money_reason": MONEY_REASON}


def _live_rows(live, ends_on):
    return [_row("live_ads", live["live_ads"], "n", ends_on, None, "ad_rows", True),
            _row("spend_live_ads", live["spend"], "usd", ends_on, None, "ad_rows", True)]


def _short(text, n=60):
    """A line fit to quote inside a sentence: no inner quotes, no end stop, at most n characters."""
    text = " ".join(str(text).replace("\u201c", "").replace("\u201d", "").replace('"', "")
                    .replace("\u2014", ",").replace("\u2013", ",").split()).replace(". ,", ",").rstrip(".!?")
    return text if len(text) <= n else text[: n - 3].rstrip() + "..."


def _reason(text):
    return str(text).rstrip(".")


def rule_claims(cs, chk, live, ends_on):
    flagged = [s for s in chk["sentences"] if s["verdict"] == "flagged"]
    if not flagged:
        return None
    risky = any(r["id"] in HIGH_RISK for s in flagged for r in s["risks"]) or chk["never_testimonial"]
    first = flagged[0]
    sentence = (f"\"{_short(first['text'])}\" runs in {copylib.plural(live['live_ads'], 'live ad')}. "
                f"It is flagged: {_reason(first['reasons'][0])}.")
    if len(flagged) > 1:
        more = len(flagged) - 1
        sentence += f" {copylib.plural(more, 'more line')} in this set {'is' if more == 1 else 'are'} flagged."
    ev = [_row("flagged_lines", len(flagged), "n", ends_on, 0, "claim check", True)] + _live_rows(live, ends_on)
    refs = []
    for s in flagged:
        for m in s["matches"]:
            if not m["allowed"]:
                ev.append(_row(f"tier_{m['id'].split('.')[-1]}", m["tier"], "tier", ends_on, "site_backed",
                               f"brain.{m['id'].split('.')[1]}", False, "as of now"))
                refs.append(m["id"])
        refs += [r["brain_ref"] for r in s["risks"] if r.get("brain_ref")]
        if s["testimonial"]:
            refs.append(s["testimonial"]["id"])
    ent = {"type": "ad", "id": cs["id"], "label": cs["name"]}
    return _finding("COPY-R01", "high" if risky else "medium", ent, ev, sentence, refs, ends_on)


def rule_match(cs, mm, live, ends_on):
    if not mm["gaps"]:
        return None
    gap = mm["gaps"][0]
    money_kind = any(g["kind"] in ("offer", "price") for g in mm["gaps"])
    sentence = f"The {cs['name']} ad promises {gap['label']}, but the page it sends to does not say it."
    if len(mm["gaps"]) > 1:
        more = len(mm["gaps"]) - 1
        sentence += f" {copylib.plural(more, 'more promise')} {'is' if more == 1 else 'are'} missing there."
    ev = [_row("message_match_score", mm["score"], "pct", ends_on, 100, "brain records by page URL", False,
               "as of now"),
          _row("promise_items_missing", len(mm["gaps"]), "n", ends_on, 0, "brain records by page URL", False,
               "as of now")] + _live_rows(live, ends_on)
    ent = {"type": "ad", "id": cs["id"], "label": cs["name"]}
    refs = [g["ref"] for g in mm["gaps"]]
    return _finding("COPY-R02", "high" if money_kind else "medium", ent, ev, sentence, refs, ends_on)


def rule_voice(cs, chk, live, ends_on, rules):
    v = chk["voice"]
    if v["pass"]:
        return None
    sentence = (f"The {cs['name']} ad runs in {copylib.plural(live['live_ads'], 'live ad')}. "
                f"It has {copylib.voice_short(v)}.")
    ev = [_row("em_dashes", v["em_dashes"], "n", ends_on, 0, "voice check", True),
          _row("inflated_words", len(v["inflated"]), "n", ends_on, 0, "voice check", True),
          _row("long_sentences", len(v["long_sentences"]), "n", ends_on, 0, "voice check", True),
          _row("reading_grade", v["grade"], "grade", ends_on, rules["voice"]["max_grade"], "voice check", True)] \
        + _live_rows(live, ends_on)
    ent = {"type": "ad", "id": cs["id"], "label": cs["name"]}
    return _finding("COPY-R03", "low", ent, ev, sentence, rules["voice"]["do_refs"], ends_on)


def _unavailable(inv, ends_on):
    out = []
    sev = {"COPY-R01": "medium", "COPY-R02": "medium", "COPY-R03": "low"}
    for r in RULES:
        f = _finding(r["rule_id"], sev[r["rule_id"]], {"type": "brand", "id": "ad_inventory", "label": "live ad copy"},
                     [], "Live ads could not be read, so this check did not run on live copy.", [], ends_on)
        f.update(status="unavailable", unavailable={
            "inputs": ["ad_rows"], "connector": "Meta Ads, ad level insights",
            "fix": inv.get("fix") or inv.get("reason") or "Connect Meta Ads or build the brand's data.sqlite."})
        out.append(f)
    return out


def evaluate(brand, inventory, brain, rules=None, sets=None):
    """Checks for every copy set, plus its live ads. Shared with api.py so the page and the audit agree."""
    rules = rules or copylib.rules()
    sets = sets or copylib.copy_sets()
    bank = copylib.bank_index(brain)
    out = []
    for cs in sets:
        chk = copylib.check_text(copylib.set_text(cs), brain, rules, bank)
        mm = copylib.message_match(cs, brain, rules, bank)
        live = inventory["by_set"].get(cs["id"]) if inventory["available"] else None
        out.append({"set": cs, "check": chk, "match": mm,
                    "live": live or ({"live_ads": 0, "spend": 0.0, "ad_ids": []} if inventory["available"] else None)})
    return out


def run(brand: str, window: dict | None = None, data=None, root: Path | None = None) -> list[dict]:
    rules = copylib.rules()
    sets = copylib.copy_sets()
    ends_on = (window or {}).get("ends_on")
    inv = copylib.ad_inventory(metric_fn(data), brand, sets, WINDOW_DAYS, ends_on)
    ends_on = ends_on or (inv.get("window") or {}).get("end") or (dt.date.today() - dt.timedelta(days=1)).isoformat()
    today = dt.date.fromisoformat(ends_on) + dt.timedelta(days=1)
    brain = copylib.brain_for(brand, root, today)
    if not inv["available"]:
        return _unavailable(inv, ends_on)
    out = []
    for row in evaluate(brand, inv, brain, rules, sets):
        live = row["live"]
        if not live or not live["live_ads"]:
            continue
        for f in (rule_claims(row["set"], row["check"], live, ends_on),
                  rule_match(row["set"], row["match"], live, ends_on),
                  rule_voice(row["set"], row["check"], live, ends_on, rules)):
            if f:
                out.append(f)
    out.sort(key=lambda f: (SEVERITY_ORDER[f["severity"]], f["id"]))
    return out


if __name__ == "__main__":
    b = sys.argv[1] if len(sys.argv) > 1 else "bombas"
    print(json.dumps(run(b), indent=1))
