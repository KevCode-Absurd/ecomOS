"""Customers and avatars audit: who we think buys, whether customers said it, and what still has no answer.

Contract: app/contracts/audit.md. `run(brand, window)` reads only app/brain/<brand>/
(through app/brain/store.py) and app/data/brands/<brand>/ (through app/data/tables.py),
and returns findings sorted by severity. No connector, no model, no writes. Same brain,
same tables, same window, same output. The screen api reuses the builders below
(`avatar_rows`, `objection_rows`, `language_rows`, `ad_angles`) so the page and the audit
read the same numbers.

Rules (thresholds are constants below):

CUST-R01 ungrounded avatar. An avatar record has no customer quotes, or all of its quotes
    come from fewer than MIN_SOURCES (2) independent sources (web hosts). The room spec
    says an avatar stays provisional until a pattern shows across independent sources.
    Severity medium (a gap with a known downstream cost, no money formula). Capability
    BRAND-C11 (assemble and gate the full avatar record, founder gate).
    Owner: 02-customers-avatars.
CUST-R02 uncovered top objection. For each avatar, its top objection is the ladder rung
    that names it with the most one-star mentions (ties: the higher rung). When that
    rung has no proof record (`proof_ids` empty), one finding per rung, naming every
    avatar it is top for. Severity medium. Capability BRAND-C13 (objection map and
    remover pairing, agent does). Owner: 02-customers-avatars. Screen 04 owns OFFER-R04
    (deal-breaker rung with no proof, read with returns); this rule is about which
    avatars are left without an answer, so it keeps its own id.
CUST-R03 objection coverage in ads. Each named objection theme should appear as an angle
    in at least one live Meta ad. Needs an angle per ad in the paid social ad table. When
    no ad row names an angle the rule emits one `unavailable` finding (never 0 percent).
    Severity medium. Capability CREA-C03 (define ad angles, agent does).
    Owner: 02-customers-avatars.

CUST-R04 proof not landing. A ladder rung has proof on file, yet one-star mentions are 2x the
    five-star ones or more, with 10 or more (builds.NOT_LANDING_*). Severity medium. Capability
    SITE-C38 (PDP first screen). Owner: 02-customers-avatars.
CUST-R05 avatar misread on a product line. The avatar buys the line (2 or more linked reviews), a top
    complaint shares words with the avatar's job or pains, and the line's 1 and 2 star share is at or
    above the median line. Severity high at 1.5x the median or more, else medium. Capability by the
    complaint: SITE-C38 fit, PROD-C73 wear, CREA-C24 feel, LIFE-C27 order. Reputation override: 4
    (a review theme on the buy path). Owner: 02-customers-avatars.
CUST-R06 unserved buying situation. 2 or more competitors in the brain push a buying situation and
    we hold no avatar with quotes for it (builds.SITUATIONS). Severity medium. Capability BRAND-C16.
    Owner: 02-customers-avatars.
CUST-R07 returning buyers bought back through paid ads. A quarter or more of returning orders in
    the latest full month came through paid social or paid search (channels_monthly). Severity
    medium. Capability MEDIA-C12. Unavailable when the channel table is missing.
    Owner: 02-customers-avatars; screen 11 reads it.
CUST-R08 calendar retention cliff. Half or more of the cohorts alive in one calendar month fell 40
    percent or more at once (cohorts.json). Severity medium. Capability LIFE-C20.
CUST-R09 retention age break. After the peak return month, active share falls 20 percent or more
    from one month to the next, cliff months left out. Severity medium. Capability LIFE-C08.
CUST-R10 split product line. Praise and complaints on a line name the same trait. Severity low.
    Capability CREA-C24.

Money at stake is null for every rule: an evidence or proof gap has no revenue formula
yet (`money_reason` says so). Confidence: one brain snapshot is one window (0.5), minus
0.2 when an input record is past `expires_at`.
"""
from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path
from urllib.parse import urlparse

APP = Path(__file__).resolve().parents[2]
for p in (APP / "brain", APP / "data", APP):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from store import Brain  # noqa: E402
import importlib.util as _ilu  # noqa: E402

_bspec = _ilu.spec_from_file_location("customers_avatars_builds_audit", Path(__file__).resolve().parent / "builds.py")
builds = _ilu.module_from_spec(_bspec)
_bspec.loader.exec_module(builds)

SCREEN = "02-customers-avatars"
MIN_SOURCES = 2
SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}
NO_MONEY = "evidence gap: no revenue formula for a missing quote or proof yet"

RULES = [
    {"rule_id": "CUST-R01", "name": "ungrounded avatar", "entity_type": "brand",
     "inputs": ["brain avatars"], "capability": "BRAND-C11", "owner_screen": SCREEN},
    {"rule_id": "CUST-R02", "name": "uncovered top objection", "entity_type": "ladder_rung",
     "inputs": ["brain avatars", "brain objection_ladders"], "capability": "BRAND-C13", "owner_screen": SCREEN},
    {"rule_id": "CUST-R03", "name": "objection coverage in ads", "entity_type": "brand",
     "inputs": ["brain objection_ladders", "ad_rows.angle"], "capability": "CREA-C03", "owner_screen": SCREEN},
    {"rule_id": "CUST-R04", "name": "proof not landing", "entity_type": "ladder_rung",
     "inputs": ["brain objection_ladders"], "capability": "SITE-C38", "owner_screen": SCREEN},
    {"rule_id": "CUST-R05", "name": "avatar misread on a product line", "entity_type": "sku",
     "inputs": ["brain products review_summary", "brain avatars", "brain language_bank"], "capability": "SITE-C38", "owner_screen": SCREEN},
    {"rule_id": "CUST-R06", "name": "unserved buying situation", "entity_type": "brand",
     "inputs": ["brain competitors", "brain avatars"], "capability": "BRAND-C16", "owner_screen": SCREEN},
    {"rule_id": "CUST-R07", "name": "returning buyers bought back through paid ads", "entity_type": "metric",
     "inputs": ["channels_monthly"], "capability": "MEDIA-C12", "owner_screen": SCREEN},
    {"rule_id": "CUST-R08", "name": "calendar retention cliff", "entity_type": "metric",
     "inputs": ["cohorts"], "capability": "LIFE-C20", "owner_screen": SCREEN},
    {"rule_id": "CUST-R09", "name": "retention age break", "entity_type": "metric",
     "inputs": ["cohorts"], "capability": "LIFE-C08", "owner_screen": SCREEN},
    {"rule_id": "CUST-R10", "name": "split product line", "entity_type": "sku",
     "inputs": ["brain products review_summary"], "capability": "CREA-C24", "owner_screen": SCREEN},
]
AUTONOMY = {"BRAND-C11": "founder_gate", "BRAND-C13": "agent_does", "CREA-C03": "agent_does", "SITE-C38": "human_assist",
            "PROD-C73": "human_assist", "CREA-C24": "agent_does", "LIFE-C27": "human_assist", "BRAND-C16": "founder_gate",
            "MEDIA-C12": "human_assist", "LIFE-C20": "agent_does", "LIFE-C08": "founder_gate"}
NO_DATA = "no revenue formula for this rule yet"


# ---------------------------------------------------------------- shared builders

SOURCE_NAMES = {"shop.bombas.com": "Bombas site", "bombas.com": "Bombas site", "own_site_yotpo": "Bombas site",
                "own_site": "Bombas site", "trustpilot.com": "Trustpilot", "trustpilot": "Trustpilot",
                "amazon.com": "Amazon", "amazon": "Amazon", "amazon_customers_say": "Amazon",
                "nordstrom.com": "Nordstrom", "target.com": "Target", "sitejabber.com": "Sitejabber",
                "yahoo.com": "Press", "retailer": "Other retailers", "reddit": "Reddit", "reddit.com": "Reddit"}


def host(ref: str | None) -> str | None:
    h = urlparse(ref or "").netloc
    return h[4:] if h.startswith("www.") else (h or None)


def source_name(s: str | None) -> str:
    return SOURCE_NAMES.get(s or "", s or "unknown")


def key(rid: str) -> str:
    return rid.split(".")[-1]


def expired(rec: dict, today: dt.date) -> bool:
    exp = rec.get("expires_at")
    return bool(exp) and dt.date.fromisoformat(exp[:10]) < today


def avatar_rows(brain: Brain) -> list[dict]:
    """One row per active avatar: share, intensity, job, quotes with links, grounding."""
    out = []
    for a in brain.records("avatars"):
        v = a.get("value") if isinstance(a.get("value"), dict) else {}
        quotes = [{"quote": e.get("quote"), "ref": e.get("ref"), "source": source_name(host(e.get("ref"))) if host(e.get("ref")) else None}
                  for e in (a.get("evidence") or []) if e.get("quote")]
        sources = sorted({q["source"] for q in quotes if q["source"]})
        if not quotes or a["tier"] == "inferred":
            grounding = "inferred"
        elif len(sources) < MIN_SOURCES:
            grounding = "single_source"
        else:
            grounding = "grounded"
        out.append({"id": a["id"], "key": key(a["id"]), "name": v.get("name") or (f"{v['situation'].capitalize()} (Reddit)" if v.get("situation") else None)
                    or a.get("text") or key(a["id"]),
                    "share_estimate": v.get("share_estimate"), "intensity": v.get("intensity"),
                    "job": v.get("job"), "triggers": v.get("triggers") or [], "pains": v.get("pains") or [],
                    "quotes": quotes, "quote_count": len(quotes), "sources": sources, "grounding": grounding,
                    "tier": a["tier"], "date": a["date"], "expired": expired(a, brain.today),
                    "count_by_source": v.get("count_by_source") or ({"reddit": v["mentions"]} if v.get("mentions") else {}), "emotional_driver": v.get("emotional_driver"),
                    "note": a.get("notes")})
    out.sort(key=lambda r: (-(r["share_estimate"] or -1), r["name"]))
    return out


def rungs(brain: Brain) -> list[dict]:
    """Every ladder rung, flat, with its theme, counts, proof and the avatars it names."""
    out = []
    for lad in brain.records("objection_ladders"):
        v = lad.get("value") or {}
        theme = v.get("theme") or lad.get("field")
        for r in v.get("rungs") or []:
            c = r.get("counts") or {}
            out.append({"ladder": lad["id"], "theme": theme, "level": r.get("level"), "id": f"{theme}.{r.get('level')}",
                        "doubt": r.get("doubt"), "one_star": c.get("one_star"), "five_star": c.get("five_star"),
                        "sources": c.get("sources") or {}, "proof": r.get("proof"), "proof_ids": r.get("proof_ids") or [],
                        "avatars": r.get("avatars") or [], "derived_from": r.get("derived_from") or [],
                        "one_star_quotes": [q for q in r.get("one_star") or [] if isinstance(q, str)],
                        "five_star_quotes": [q for q in r.get("five_star") or [] if isinstance(q, str)],
                        "uses": r.get("uses") or [], "expired": expired(lad, brain.today)})
    return out


def top_objection(avatar_id: str, all_rungs: list[dict]) -> dict | None:
    mine = [r for r in all_rungs if avatar_id in r["avatars"]]
    if not mine:
        return None
    return max(mine, key=lambda r: ((r["one_star"] or 0), r["level"] or 0))


def objection_rows(brain: Brain, all_rungs: list[dict], angles: dict) -> list[dict]:
    """One row per named objection: the avatars its rungs name, proof or open question, coverage."""
    names = {a["id"]: a["name"] for a in avatar_rows(brain)}
    out = []
    for o in brain.records("objections"):
        v = o.get("value") if isinstance(o.get("value"), dict) else {}
        linked = [r for r in all_rungs if o["id"] in r["derived_from"]]
        avatars = sorted({a for r in linked for a in r["avatars"]})
        open_rungs = [r["id"] for r in linked if not r["proof_ids"]]
        if not linked:
            status = "not on a ladder"
        elif open_rungs:
            status = "open question"
        else:
            status = "proof on file"
        themes = sorted({r["theme"] for r in linked})
        ads = angles["by_theme"].get(themes[0]) if angles["available"] and themes else None
        out.append({"id": o["id"], "objection": v.get("objection") or o.get("text"), "proof": v.get("proof") or None,
                    "status": status, "open_rungs": open_rungs, "proof_ids": sorted({p for r in linked for p in r["proof_ids"]}),
                    "themes": themes, "avatars": [{"id": a, "name": names.get(a, key(a))} for a in avatars],
                    "mentions": v.get("count_in_sample"),
                    "quotes": v.get("count_in_sample") if isinstance(v.get("count_in_sample"), int) else len(o.get("evidence") or []),
                    "quote": ((o.get("evidence") or [{}])[0]).get("quote"),
                    "quote_ref": ((o.get("evidence") or [{}])[0]).get("ref"),
                    "ads": {"value": None if not angles["available"] else sum(angles["by_theme"].get(t, 0) for t in themes),
                            "unavailable_reason": None if angles["available"] else angles["reason"]},
                    "pages": {"value": None, "unavailable_reason": "no live page scan yet"}})
    order = {"open question": 0, "not on a ladder": 1, "proof on file": 2}
    out.sort(key=lambda r: (order[r["status"]], -r["quotes"], r["id"]))
    return out


def language_rows(brain: Brain) -> dict:
    """Language bank by theme: phrases with counts, and mentions by source per theme."""
    themes: dict[str, dict] = {}
    for p in brain.records("language_bank"):
        v = p.get("value") if isinstance(p.get("value"), dict) else {}
        by_source = v.get("count_by_source")
        if not by_source:
            by_source = {}
            for e in p.get("evidence") or []:
                h = source_name(host(e.get("ref")))
                by_source[h] = by_source.get(h, 0) + 1
        else:
            merged: dict[str, int] = {}
            for k, n in by_source.items():
                if n:
                    merged[source_name(k)] = merged.get(source_name(k), 0) + n
            by_source = merged
        count = v.get("count") if isinstance(v.get("count"), int) else v.get("count_in_sample")
        if not isinstance(count, int):
            count = sum(by_source.values()) or None
        t = themes.setdefault(v.get("theme") or "other", {"theme": v.get("theme") or "other", "phrases": [],
                                                          "mentions": 0, "by_source": {}})
        t["phrases"].append({"id": p["id"], "phrase": v.get("phrase") or p.get("text"), "count": count,
                             "by_source": by_source,
                             "quote": ((p.get("evidence") or [{}])[0]).get("quote") or
                                      ((v.get("reviews") or [{}])[0]).get("quote"),
                             "ref": ((p.get("evidence") or [{}])[0]).get("ref") or ((v.get("reviews") or [{}])[0]).get("url")})
        t["mentions"] += count or 0
        for s, n in by_source.items():
            t["by_source"][s] = t["by_source"].get(s, 0) + n
    out = sorted(themes.values(), key=lambda t: (-t["mentions"], t["theme"]))
    for t in out:
        t["phrases"].sort(key=lambda p: (-(p["count"] or 0), p["phrase"] or ""))
    return {"themes": out, "phrases": sum(len(t["phrases"]) for t in out)}


def ad_angles(brand: str, ends_on: str | None = None) -> dict:
    """Meta ads per objection theme from the paid social ad table, if it names an angle."""
    try:
        import metrics
        from tables import brand_data
        res = metrics.compute("spend", brand_data(brand), channel="meta", by="ad",
                              **({"end": ends_on} if ends_on else {}))
    except (ImportError, ValueError, KeyError) as exc:
        return {"available": False, "reason": f"the ad table could not be read ({exc})", "by_theme": {}, "ads": 0}
    if res.get("unavailable"):
        return {"available": False, "reason": res.get("reason"), "by_theme": {}, "ads": 0}
    groups = res.get("groups") or []
    named = [g for g in groups if g.get("angle")]
    if not named:
        return {"available": False, "ads": len(groups), "by_theme": {},
                "reason": f"none of the {len(groups)} Meta ads in the window names an angle"}
    by_theme: dict[str, int] = {}
    for g in named:
        by_theme[g["angle"]] = by_theme.get(g["angle"], 0) + 1
    return {"available": True, "reason": None, "by_theme": by_theme, "ads": len(groups)}


# ---------------------------------------------------------------- findings

def _ev(metric, value, unit, ends_on, source, baseline=None, baseline_kind="threshold", fresh=0, simulated=False):
    return {"metric": metric, "value": value, "unit": unit, "window": "as of latest brain", "ends_on": ends_on,
            "freshness_days": fresh, "baseline": baseline, "baseline_kind": baseline_kind, "source": source,
            "simulated": simulated}


def _finding(rule_id, severity, entity, evidence, sentence, capability, confidence, refs, ends_on,
             status="open", unavailable=None):
    return {"id": f"{SCREEN}.{rule_id}.{entity['id']}", "screen": SCREEN, "rule_id": rule_id, "severity": severity,
            "entity": entity, "evidence": evidence, "sentence": sentence,
            "capability": {"id": capability, "autonomy": AUTONOMY[capability]},
            "money_at_stake": None, "confidence": round(max(confidence, 0.1), 2),
            "brain_refs": refs, "first_seen": ends_on, "last_seen": ends_on, "status": status,
            "unavailable": unavailable, "money_reason": NO_MONEY if rule_id in ("CUST-R01", "CUST-R02", "CUST-R03", "CUST-R04") else NO_DATA}


def _plural(n, word):
    return f"{n} {word}" + ("" if n == 1 else "s")


def r01(brain, avatars, ends_on):
    out = []
    for a in avatars:
        if a["grounding"] == "grounded":
            continue
        fresh = (brain.today - dt.date.fromisoformat(a["date"])).days if a["date"] != "undated" else None
        ev = [_ev("quotes", a["quote_count"], "n", ends_on, "brain.avatars", fresh=fresh),
              _ev("independent_sources", len(a["sources"]), "n", ends_on, "brain.avatars", baseline=MIN_SOURCES, fresh=fresh)]
        if a["quote_count"] == 0:
            s = f"{a['name']} has no customer quotes. It is a guess until customers say it."
        else:
            s = (f"{a['name']} rests on {_plural(a['quote_count'], 'quote')} from 1 source, {a['sources'][0]}. "
                 f"It stays provisional until a second source agrees.")
        out.append(_finding("CUST-R01", "medium", {"type": "brand", "id": a["key"], "label": a["name"]}, ev, s,
                            "BRAND-C11", 0.5 - (0.2 if a["expired"] else 0), [a["id"]], ends_on))
    return out


def r02(brain, avatars, all_rungs, ends_on):
    by_rung: dict[str, dict] = {}
    for a in avatars:
        top = top_objection(a["id"], all_rungs)
        if top is None or top["proof_ids"]:
            continue
        by_rung.setdefault(top["id"], {"rung": top, "avatars": []})["avatars"].append(a)
    out = []
    for rid in sorted(by_rung):
        rung, avs = by_rung[rid]["rung"], by_rung[rid]["avatars"]
        names = ", ".join(a["name"] for a in avs) if len(avs) <= 2 else f"{len(avs)} avatars, led by {avs[0]['name']}"
        n1 = rung["one_star"]
        ev = [_ev("one_star_mentions", n1, "n", ends_on, "brain.objection_ladders"),
              _ev("proof_records", 0, "n", ends_on, "brain.objection_ladders", baseline=1),
              _ev("avatars_left_open", len(avs), "n", ends_on, "brain.avatars")]
        count = f"{n1} one-star reviews ask" if isinstance(n1, int) else "Reviews ask"
        s = f"{count} \"{rung['doubt']}\" and nothing on file answers it. It is the top doubt for {names}."
        refs = [rung["ladder"]] + [a["id"] for a in avs]
        out.append(_finding("CUST-R02", "medium", {"type": "ladder_rung", "id": rid, "label": f"{rung['theme']}, rung {rung['level']}"},
                            ev, s, "BRAND-C13", 0.5 - (0.2 if rung["expired"] else 0), refs, ends_on))
    return out


def r03(brain, all_rungs, angles, ends_on):
    themes = sorted({r["theme"] for r in all_rungs})
    refs = sorted({r["ladder"] for r in all_rungs})
    if not themes:
        return []
    if not angles["available"]:
        return [_finding("CUST-R03", "medium", {"type": "brand", "id": "ad_angles", "label": "Objection themes in Meta ads"},
                         [], f"Ad coverage for {_plural(len(themes), 'objection theme')} cannot be read. "
                             f"{angles['reason'][:1].upper()}{angles['reason'][1:]}.", "CREA-C03", 0.5, refs, ends_on, status="unavailable",
                         unavailable={"inputs": ["ad_rows.angle"], "connector": "meta_ads",
                                      "fix": "Name the angle in each ad or ad set name, or tag it in the ad table."})]
    out = []
    for t in themes:
        if angles["by_theme"].get(t):
            continue
        lad = next(r["ladder"] for r in all_rungs if r["theme"] == t)
        ev = [_ev("ads_with_angle", 0, "n", ends_on, "ad_rows", baseline=1, simulated=True)]
        out.append(_finding("CUST-R03", "medium", {"type": "brand", "id": f"angle_{t}", "label": t.replace("_", " ")},
                            ev, f"No live Meta ad answers the {t.replace('_', ' ')} doubt. {angles['ads']} ads ran in the window.",
                            "CREA-C03", 0.5, [lad], ends_on))
    return out


def load_cohorts(brand: str, avatars: list[dict]) -> dict:
    try:
        from tables import brand_data
        data = brand_data(brand)
        rows, monthly, as_of = data.table("cohorts"), data.table("monthly"), data.brand.get("as_of")
    except (ImportError, ValueError, KeyError, FileNotFoundError) as exc:
        return {"available": False, "reason": f"no cohort table for {brand} ({exc})", "rows": [], "moves": []}
    return builds.cohort_grid(rows, monthly, as_of, avatars)


def load_mix(brand: str) -> dict:
    try:
        from tables import brand_data
        data = brand_data(brand)
        monthly, channels, as_of = data.table("monthly"), data.table("channels_monthly"), data.brand.get("as_of")
    except (ImportError, ValueError, KeyError, FileNotFoundError) as exc:
        return {"available": False, "reason": f"no monthly or channel table for {brand} ({exc})", "moves": []}
    return builds.mix(monthly, channels, as_of)


def with_tops(avatars, all_rungs):
    for a in avatars:
        top = top_objection(a["id"], all_rungs)
        a["top_objection"] = None if top is None else {"id": top["id"], "doubt": top["doubt"], "one_star": top["one_star"],
                                                        "five_star": top["five_star"], "proof": bool(top["proof_ids"]),
                                                        "proof_text": top["proof"] if top["proof_ids"] else None}
    return avatars


def desk(brain: Brain, avatars: list[dict], all_rungs: list[dict]) -> dict:
    """Every desk builder the page and the rules share, computed once."""
    return {"ladders": builds.ladders(all_rungs, avatars),
            "misreads": builds.misreads(brain.records("avatars"), avatars, all_rungs, brain.records("language_bank"), brain.records("products")),
            "served": builds.served(avatars, all_rungs, brain.records("competitors"), brain.records("positioning")),
            "cohorts": load_cohorts(brain.brand, avatars), "mix": load_mix(brain.brand)}


def r04(d, all_rungs, ends_on):
    out = []
    lad = {r["id"]: r for r in all_rungs}
    for row in d["ladders"]["rows"]:
        if row["verdict"] != "not_landing":
            continue
        ev = [_ev("one_star_mentions", row["one_star"], "n", ends_on, "brain.objection_ladders"),
              _ev("five_star_mentions", row["five_star"], "n", ends_on, "brain.objection_ladders",
                  baseline=builds.NOT_LANDING_RATIO, baseline_kind="threshold")]
        s = (f"Proof is on file for \"{row['doubt']}\", yet {row['one_star']} one-star reviews raise it "
             f"against {row['five_star']} five-star. The proof is not landing.")
        out.append(_finding("CUST-R04", "medium", {"type": "ladder_rung", "id": row["id"], "label": f"{row['theme']}, rung {row['level']}"},
                            ev, s, "SITE-C38", 0.5 - (0.2 if lad[row["id"]]["expired"] else 0),
                            [lad[row["id"]]["ladder"]] + row["proof_ids"], ends_on))
    return out


def r05(d, ends_on):
    x = d["misreads"]
    if not x.get("available"):
        return []
    out = []
    for r in x["rows"]:
        sev = "high" if r["neg_share"] >= builds.LINE_PROBLEM * r["median"] else "medium"
        ev = [_ev("one_two_star_share", r["neg_share"], "%", ends_on, "brain.products.review_summary",
                  baseline=round(r["median"], 4), baseline_kind="threshold"),
              _ev("linked_reviews", r["links"], "n", ends_on, "brain.language_bank", baseline=builds.MIN_LINKS)]
        s = (f"{r['avatar']} buys {r['line'].replace('_', ' ')} for its job, and the top complaint is \"{r['hits'][0]}\". "
             f"{round(r['neg_share'] * 100, 1)} percent of reviews are 1 or 2 star.")
        out.append(_finding("CUST-R05", sev, {"type": "sku", "id": f"{r['line']}.{r['avatar_key']}", "label": f"{r['line'].replace('_', ' ')}, {r['avatar']}"},
                            ev, s, r["action"]["capability"]["id"], 0.5, [f"{d['brand']}.avatars.{r['avatar_key']}"], ends_on))
    return out


def r06(d, ends_on):
    out = []
    for sg in d["served"]["segments"]:
        if sg["verdict"] != "gap":
            continue
        ev = [_ev("competitors_pushing", len(sg["theirs"]), "n", ends_on, "brain.competitors", baseline=2),
              _ev("our_avatars", 0, "n", ends_on, "brain.avatars", baseline=1)]
        s = f"{len(sg['theirs'])} competitors sell to {sg['segment']} buyers: {', '.join(sg['theirs'][:3])}. We hold no avatar for them."
        out.append(_finding("CUST-R06", "medium", {"type": "brand", "id": "situation_" + sg["segment"].replace(" ", "_"), "label": sg["segment"]},
                            ev, s, "BRAND-C16", 0.5, [], ends_on))
    return out


def r07(d, ends_on):
    x = d["mix"]
    if not x.get("available"):
        return [_finding("CUST-R07", "medium", {"type": "metric", "id": "returning_via_paid", "label": "Returning orders through paid ads"},
                         [], "Returning orders by channel cannot be read. " + str(x.get("reason", "")).capitalize() + ".", "MEDIA-C12", 0.5, [], ends_on,
                         status="unavailable", unavailable={"inputs": ["channels_monthly"], "connector": "shopify",
                                                            "fix": "Connect the store orders with first-order flags, read-only."})]
    if x["paid_share_returning"] is None or x["paid_share_returning"] < builds.PAID_RETURNING:
        return []
    ev = [_ev("paid_share_of_returning_orders", x["paid_share_returning"], "%", ends_on, "channels_monthly",
              baseline=builds.PAID_RETURNING, simulated=True)]
    s = f"{round(x['paid_share_returning'] * 100, 1)} percent of returning orders in {x['latest']} came through paid ads. We pay again for buyers we have."
    return [_finding("CUST-R07", "medium", {"type": "metric", "id": "returning_via_paid", "label": "Returning orders through paid ads"},
                     ev, s, "MEDIA-C12", 0.5, [], ends_on)]


def r08_r09(d, ends_on):
    c = d["cohorts"]
    if not c.get("available"):
        return []
    out = []
    cb = c.get("calendar_break")
    if cb:
        ev = [_ev("cohorts_falling_together", cb["share"], "%", ends_on, "cohorts", baseline=builds.CLIFF_SHARE, simulated=True),
              _ev("cohorts_alive", cb["cohorts"], "n", ends_on, "cohorts", simulated=True)]
        s = f"In {cb['month']}, {round(cb['share'] * 100)} percent of {cb['cohorts']} cohorts fell 40 percent or more at once. Every past buyer went quiet together."
        out.append(_finding("CUST-R08", "medium", {"type": "metric", "id": "calendar_" + cb["month"], "label": f"Retention cliff, {cb['month']}"},
                            ev, s, "LIFE-C20", 0.5, [], ends_on))
    ab = c.get("age_break")
    if ab and ab["drop"] is not None and ab["drop"] >= 0.2:
        ev = [_ev("active_share_drop", ab["drop"], "%", ends_on, "cohorts", baseline=0.2, simulated=True)]
        s = f"Active share falls {round(ab['drop'] * 100)} percent from month {ab['month']} to month {ab['month'] + 1} after the first order."
        out.append(_finding("CUST-R09", "medium", {"type": "metric", "id": f"age_month_{ab['month']}", "label": f"Retention break, month {ab['month']}"},
                            ev, s, "LIFE-C08", 0.5, [], ends_on))
    return out


def r10(d, ends_on):
    x = d["misreads"]
    if not x.get("available"):
        return []
    out = []
    for l in x["lines"]:
        if l["verdict"] != "split":
            continue
        ev = [_ev("shared_traits", len(l["polar"]), "n", ends_on, "brain.products.review_summary", baseline=1)]
        s = f"Buyers praise and blame {l['line'].replace('_', ' ')} for the same thing: {', '.join(l['polar'])}. Set the expectation."
        out.append(_finding("CUST-R10", "low", {"type": "sku", "id": "split_" + l["line"], "label": l["line"].replace("_", " ")},
                            ev, s, "CREA-C24", 0.5, [l["ref"]], ends_on))
    return out


def run(brand: str, window: dict, brain_root: Path | None = None) -> list[dict]:
    ends_on = window["ends_on"]
    today = dt.date.fromisoformat(ends_on) + dt.timedelta(days=1)
    brain = Brain(brand, brain_root, today)
    avatars = avatar_rows(brain)
    all_rungs = rungs(brain)
    angles = ad_angles(brand, ends_on)
    d = desk(brain, with_tops(avatars, all_rungs), all_rungs)
    d["brand"] = brand
    findings = (r01(brain, avatars, ends_on) + r02(brain, avatars, all_rungs, ends_on) + r03(brain, all_rungs, angles, ends_on)
                + r04(d, all_rungs, ends_on) + r05(d, ends_on) + r06(d, ends_on) + r07(d, ends_on) + r08_r09(d, ends_on) + r10(d, ends_on))
    findings.sort(key=lambda f: (SEVERITY_ORDER[f["severity"]], f["rule_id"], f["id"]))
    return findings
