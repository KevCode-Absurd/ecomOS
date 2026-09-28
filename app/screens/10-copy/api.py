"""Copy screen API: /api/10-copy/...

Reads the brain (app/brain/<brand>/ through app/brain/store.py), the screen fixtures
(simulated copy sets, checker rules) and the ad table through the server's Data.metric
(spend by ad, Meta). Read-only: nothing here writes anywhere.

  GET  overview                 tiles, insights, chart (claims by tier), claims, voice rules,
                                live copy with its checks, message match table, copy set stub
  GET  language?theme=&star=    language bank rows: theme, star, phrase, source, never-testimonial
  POST check                    {text}: every sentence against the claims records, plus the voice check
  GET  audit                    findings from audit.py (app/contracts/audit.md shape)

Query `brand` (default bombas) and `today` (YYYY-MM-DD, default the real date) work on every
route. Set BRAIN_ROOT to point at a copy of app/brain (tests do).
"""
from __future__ import annotations

import datetime as dt
import importlib.util
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

_spec = importlib.util.spec_from_file_location("screen_10_copy_audit", HERE / "audit.py")
audit = importlib.util.module_from_spec(_spec)
sys.modules["screen_10_copy_audit"] = audit
_spec.loader.exec_module(audit)
copylib = audit.copylib

from store import TIER_RANK  # noqa: E402  (app/brain is on sys.path through copylib)

BRAIN_ROOT: Path | None = None
DEFAULT_BRAND = "bombas"
SAFE_BRAND = re.compile(r"^[a-z0-9_-]{1,40}$")
MAX_TEXT = 4000


def _brand(req) -> str:
    brand = req.arg("brand", DEFAULT_BRAND)
    if not SAFE_BRAND.match(brand or ""):
        raise ValueError("brand must be a folder name like bombas")
    return brand


def _brain(req, brand):
    t = req.arg("today")
    return copylib.brain_for(brand, BRAIN_ROOT, dt.date.fromisoformat(t) if t else dt.date.today())


def _metric(req):
    return audit.metric_fn(getattr(req, "data", None))


# ---------------------------------------------------------------- tiles, insights, chart

def tiles(rows, inv) -> list[dict]:
    if not inv["available"]:
        na = {"value": None, "unavailable_reason": inv["reason"], "fix": inv.get("fix") or "Meta Ads (ad level)"}
        return [dict(na, name="Live ads with a flagged claim", plain="Live ads running a line the claim check flags"),
                dict(na, name="Message match", plain="Share of ad promises the landing page also says"),
                dict(na, name="Voice compliance", plain="Share of live copy sets that pass the voice rules")]
    live = [r for r in rows if r["live"] and r["live"]["live_ads"]]
    win = f"live on {inv['window']['end']}"
    flagged_ads = sum(r["live"]["live_ads"] for r in live if r["check"]["flagged"])
    items = sum(r["match"]["total"] for r in live)
    matched = sum(r["match"]["matched"] for r in live)
    voice_ok = sum(1 for r in live if r["check"]["voice"]["pass"])
    return [
        {"name": "Live ads with a flagged claim", "plain": "Live ads running a line the claim check flags",
         "value": flagged_ads, "unit": "n", "window": win, "tone": "bad" if flagged_ads else "good"},
        {"name": "Message match", "plain": "Share of ad promises the landing page also says (target 100 percent)",
         "value": matched / items if items else None, "unit": "%", "window": win,
         "unavailable_reason": None if items else "no live ad names a claim or offer",
         "tone": "bad" if items and matched < items else None},
        {"name": "Voice compliance", "plain": "Share of live copy sets that pass the voice rules",
         "value": voice_ok / len(live) if live else None, "unit": "%", "window": win,
         "unavailable_reason": None if live else "no live ads in the window",
         "tone": "bad" if live and voice_ok < len(live) else None},
    ]


def insights(rows, inv) -> list[dict]:
    """Two rules: a live ad using an unapproved claim; a voice rule broken in live copy."""
    if not inv["available"]:
        return []
    out = []
    live = [r for r in rows if r["live"] and r["live"]["live_ads"]]
    bad = [r for r in live if r["check"]["flagged"]]
    if bad:
        ads = sum(r["live"]["live_ads"] for r in bad)
        worst = max(bad, key=lambda r: (r["check"]["never_testimonial"] or any(
            x["risks"] for x in r["check"]["sentences"]), r["live"]["spend"]))
        line = next(s for s in worst["check"]["sentences"] if s["verdict"] == "flagged")
        out.append({"rule": "live ad copy has a line whose claim record is not approved or site_backed, "
                            "or no record, a risk pattern or a Reddit testimonial",
                    "severity": "high",
                    "sentence": (f"{ads} live ads use a claim that is not approved. The {worst['set']['name']} ad says "
                                 f"\"{audit._short(line['text'], 50)}\": {audit._reason(line['reasons'][0])}."),
                    "capability": "LOOP-C12", "autonomy": "agent",
                    "evidence": "copy sets: " + ", ".join(f"{r['set']['id']} ({r['live']['live_ads']} ads, "
                                                          f"${r['live']['spend']:,.0f} in 7 days)" for r in bad)})
    broke = [r for r in live if not r["check"]["voice"]["pass"]]
    if broke:
        ads = sum(r["live"]["live_ads"] for r in broke)
        w = max(broke, key=lambda r: (len(r["check"]["voice"]["breaks"]), r["live"]["spend"]))
        out.append({"rule": "live ad copy has an em dash, an inflated word, a sentence over 20 words "
                            "or a reading grade over 10",
                    "severity": "medium",
                    "sentence": (f"{copylib.plural(ads, 'live ad')} break a voice rule. The {w['set']['name']} ad has "
                                 f"{copylib.voice_short(w['check']['voice'])}."),
                    "capability": "CREA-C26", "autonomy": "agent",
                    "evidence": "copy sets: " + ", ".join(f"{r['set']['id']} ({', '.join(r['check']['voice']['breaks'])})"
                                                          for r in broke)})
    return out


def chart(claims) -> dict:
    tiers = sorted(TIER_RANK, key=TIER_RANK.get)
    sections = sorted({c["section"] for c in claims})
    return {"labels": [t.replace("_", " ") for t in tiers],
            "series": [{"name": s, "values": [sum(1 for c in claims if c["section"] == s and c["tier"] == t)
                                              for t in tiers]} for s in sections],
            "allowed": sum(1 for c in claims if c["allowed"]), "total": len(claims)}


# ---------------------------------------------------------------- views

def voice_view(brain, rules) -> dict:
    v = rules["voice"]
    brand_do = []
    for rid in v["do_refs"]:
        rec = brain.get(rid)
        if rec:
            brand_do.append({"rule": rec.get("text") or str(rec.get("value")), "ref": rid, "tier": rec["tier"]})
    return {"do": v["do"], "do_not": v["do_not"], "brand_do": brand_do, "inflated_words": v["inflated_words"],
            "max_grade": v["max_grade"], "max_sentence_words": v["max_sentence_words"]}


def live_view(rows, inv) -> list[dict]:
    out = []
    for r in rows:
        cs, chk = r["set"], r["check"]
        out.append({"id": cs["id"], "name": cs["name"], "format": cs["format"], "headline": cs["headline"],
                    "primary_text": cs["primary_text"], "cta": cs["cta"], "destination_url": cs["destination_url"],
                    "live_ads": r["live"]["live_ads"] if r["live"] else None,
                    "spend_7d": r["live"]["spend"] if r["live"] else None,
                    "claims": chk["claims"], "flagged": chk["flagged"], "never_testimonial": chk["never_testimonial"],
                    "voice_breaks": chk["voice"]["breaks"], "grade": chk["voice"]["grade"],
                    "sentences": chk["sentences"]})
    out.sort(key=lambda x: (-(x["live_ads"] or 0), x["id"]))
    return out


def match_view(rows) -> list[dict]:
    out = []
    for r in rows:
        mm = r["match"]
        out.append(dict(mm, live_ads=r["live"]["live_ads"] if r["live"] else None))
    out.sort(key=lambda m: (m["score"] is None, m["score"] if m["score"] is not None else 0, m["set_id"]))
    return out


def overview(req) -> dict:
    brand = _brand(req)
    brain = _brain(req, brand)
    rules = copylib.rules()
    sets = copylib.copy_sets()
    inv = copylib.ad_inventory(_metric(req), brand, sets, audit.WINDOW_DAYS)
    rows = audit.evaluate(brand, inv, brain, rules, sets)
    claims = copylib.claim_records(brain, rules)
    return {"brand": brand, "today": brain.today.isoformat(), "brain_version": brain.version(),
            "simulated_note": copylib.SIMULATED_NOTE,
            "inventory": {k: inv.get(k) for k in ("available", "reason", "fix", "window", "spend_total")}
            | {"ads": len(inv["ads"]), "live_ads": sum(1 for a in inv["ads"] if a["live"])},
            "tiles": tiles(rows, inv), "insights": insights(rows, inv), "chart": chart(claims),
            "claims": claims, "allowed_tiers": rules["allowed_tiers"], "voice": voice_view(brain, rules),
            "copy": live_view(rows, inv), "match": match_view(rows),
            "stub": copylib.copy_set_stub(brain, rules)}


def language(req) -> dict:
    brain = _brain(req, _brand(req))
    rows = copylib.language_rows(brain)
    themes = sorted({r["theme"] for r in rows})
    theme, star = req.arg("theme", ""), req.arg("star", "")
    if theme:
        rows = [r for r in rows if r["theme"] == theme]
    if star == "none":
        rows = [r for r in rows if not r["stars"]]
    elif star:
        if not star.isdigit():
            raise ValueError("star must be 1 to 5 or none")
        rows = [r for r in rows if int(star) in r["stars"]]
    return {"themes": themes, "rows": rows, "total": len(rows),
            "never_testimonial": sum(1 for r in rows if r["never_testimonial"])}


def check(req):
    text = str((req.body or {}).get("text") or "").strip()
    if not text:
        return 400, {"error": "text is empty"}
    if len(text) > MAX_TEXT:
        return 400, {"error": f"text is over {MAX_TEXT} characters"}
    brain = _brain(req, _brand(req))
    return copylib.check_text(text, brain)


def handle(req):
    parts = req.path
    try:
        if req.method == "GET" and parts == ["overview"]:
            return overview(req)
        if req.method == "GET" and parts == ["language"]:
            return language(req)
        if req.method == "POST" and parts == ["check"]:
            return check(req)
        if req.method == "GET" and parts == ["audit"]:
            brand = _brand(req)
            findings = audit.run(brand, None, getattr(req, "data", None), BRAIN_ROOT)
            return {"findings": findings, "rules": audit.RULES}
    except ValueError as exc:
        return 400, {"error": str(exc)}
    except FileNotFoundError as exc:
        return 404, {"error": str(exc)}
    return 404, {"error": "not found", "path": parts}
