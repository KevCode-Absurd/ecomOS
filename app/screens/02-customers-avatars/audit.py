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
    Money (builds.paid_stake): (paid share now minus the own 12-month median) x returning orders x paid
    spend per paid order, cost-side. Null with the reason when the share sits at or under its median,
    history is under 4 months or spend is missing. The 25 percent line is a target, not the baseline.
    Owner: 02-customers-avatars; screen 11 reads it.
CUST-R08 calendar retention cliff. Half or more of the cohorts alive in one calendar month fell 40
    percent or more at once (cohorts.json). Severity medium. Capability LIFE-C20.
    Money (builds._cliff_stake): per cohort, (share the month before x the median step at that age outside cliff
    months, 4 or more, minus the share in the cliff month) x cohort size, summed, x that month's AOV. The note
    says whether the same month last year is in the grid, since part of a cliff can be the season.
    When the monthly table holds the same step a year earlier (builds._season_check), that is the baseline:
    the stake is only the fall beyond last year's x the month before's returning orders x AOV, null when the
    fall is no worse (the season). The stake against a normal month stays as `season_usd`.
CUST-R09 retention age break. After the peak return month, active share falls 20 percent or more
    from one month to the next, cliff months left out. Severity medium. Capability LIFE-C08.
    Money (builds._age_stake): share in month k x (the fall at the break minus the median fall at the other
    ages after the peak, 4 or more) x the median cohort size x the median AOV of 12 months, per cohort.
CUST-R10 split product line. Praise and complaints on a line name the same trait. Severity low.
    Capability CREA-C24.

CUST-R11 review theme costs stars. A theme's impact (share of rated reviews x star gap) is below
    zero with 8 or more reviews (builds.theme_impact). High when rising, else medium. Capability BRAND-C13.
CUST-R12 buyer words we never say. 3 or more of the top 20 praise words are absent from every
    site and founder record in the brain (builds.copy_gap). Severity medium. Capability BRAND-C14.
CUST-R13 provisional avatars. One or more avatars fail a core evidence check (builds.gate). One
    finding for the set; the fix is the post-purchase survey. Severity medium. Capability LIFE-C50.
CUST-R14 under-researched avatar. A force (push, pull, anxiety, habit) has no line, or anxiety
    plus habit is under 15 percent (builds.forces). Severity low. Capability BRAND-C05.
CUST-R15 avatar moment coming. An avatar moment's ads-live date is within 45 days or past
    (builds.moments). High when past, else medium. Capability LIFE-C20.
CUST-R16 order-level paths unreadable. No customer_paths aggregate, so gateway products,
    second-order paths and order-gap timing cannot run. Status unavailable. Capability LIFE-C12.
    When the aggregate exists, R16 fires once per gateway or path move instead (medium).

CUST-R17 perception gap. Under half of the top 20 praise words appear in our positioning records
    (builds.perception). Severity medium. Capability BRAND-C59.
CUST-R18 claim under fire. 3 or more 1 and 2 star reviews use a live claim's own feature words
    (builds.claims_fire). Severity high. Capability BRN-C03. Reputation 5 (a claim buyers dispute).
CUST-R19 lookalike page. The Ad Library pull marks a page as a likely impostor. Severity high.
    Capability MONEY-C48; a person reports it, never the agent. Reputation 5 (someone using our name).
CUST-R20 pushed offer answers no doubt. The promo our ads carry most is proof for no ladder rung
    (builds.offer_map). Severity medium. Capability LIFE-C42.
CUST-R21 doubt season. A ladder theme's share of complaints in a 3-month window is 1.5x its year
    share (builds.doubt_timing). High when the season has started, else medium. Capability SITE-C38.
CUST-R22 no approved messaging hierarchy. The brain holds no positioning.messaging_hierarchy
    record. Severity low. Capability BRAND-C33.
CUST-R23 brand health line falling. Repeat in months 1 to 3 down 3 points over the last 3 cohorts,
    or tickets per 1,000 orders up 20 percent over 3 months (builds.health). Severity medium.
    Capability LIFE-C20.

CUST-R24 avatar may be two buyers. Two product lines each hold 30 percent or more of the avatar's
    linked reviews and draw different complaints (builds.split_check). Severity medium. Capability BRAND-C12.
CUST-R25 avatar our ads never speak to. An avatar with 12 percent or more of buyers matches no live
    ad hook (builds.ad_voice). Severity medium. Capability CREA-C06.

CUST-R26 avatar with high return risk. Return risk at 1.25x the median avatar or more (builds.return_risk).
    Severity medium. Capability LIFE-C07. Satisfaction 4 (returns), per this docstring.
CUST-R27 marketplace-led avatar. Half or more of its linked reviews come from Amazon and Amazon one and two
    star reviews name its doubts (builds.marketplace). Severity medium. Capability PROD-C34.
CUST-R28 price-led avatar. Price rungs hold 30 percent or more of its one-star mentions (builds.price_doubts).
    Severity medium. Capability LIFE-C39.
CUST-R29 records due for a re-check. Avatar or ladder records expire within 30 days (builds.rechecks).
    One finding for the set. Severity low. Capability BRAND-C15.
CUST-R30 thin read. Avatar quotes under 60 in all, or fewer than 30 live ads read (builds.strength rules).
    One finding per thin block. Severity low. Capability BRAND-C01.
CUST-R31 reviews and sales disagree on who buys. An avatar's share of sales through the lines it buys is
    1.5x its share from reviews or under 1 / 1.5, or sales give it a share and reviews give none
    (builds.sales_share; products_monthly with the SKU to line fixture). One finding per avatar.
    Severity low. Capability LIFE-C29. Unavailable when the line sales cannot be read.
CUST-R32 weak cohort. A first-order month repeats in months 1 to 3 at under 0.8x the grid's median
    (builds.cohort_grid). One finding per cohort. Severity medium. Capability LIFE-C07. Money
    (builds._weak_stake): (median repeat minus the cohort's) x cohort size x the cohort month's AOV; the note
    says whether the same month last year was weak too (the season).

Money at stake is null for evidence and proof gaps, which have no revenue formula yet (`money_reason`
says so); R07, R08, R09 and R32 carry a stake against the brand's own history when it exists. Confidence:
one brain snapshot is one window (0.5), minus 0.2 when an input record is past `expires_at`.
"""
from __future__ import annotations

import datetime as dt
import re
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
    {"rule_id": "CUST-R11", "name": "review theme costs stars", "entity_type": "brand",
     "inputs": ["brain language_bank"], "capability": "BRAND-C13", "owner_screen": SCREEN},
    {"rule_id": "CUST-R12", "name": "buyer words we never say", "entity_type": "brand",
     "inputs": ["brain language_bank", "brain site and founder records"], "capability": "BRAND-C14", "owner_screen": SCREEN},
    {"rule_id": "CUST-R13", "name": "provisional avatars", "entity_type": "brand",
     "inputs": ["brain avatars", "brain objection_ladders"], "capability": "LIFE-C50", "owner_screen": SCREEN},
    {"rule_id": "CUST-R14", "name": "under-researched avatar", "entity_type": "brand",
     "inputs": ["brain avatars", "brain language_bank", "brain competitors"], "capability": "BRAND-C05", "owner_screen": SCREEN},
    {"rule_id": "CUST-R15", "name": "avatar moment coming", "entity_type": "brand",
     "inputs": ["brain avatars", "monthly"], "capability": "LIFE-C20", "owner_screen": SCREEN},
    {"rule_id": "CUST-R16", "name": "order-level paths", "entity_type": "metric",
     "inputs": ["customer_paths"], "capability": "LIFE-C12", "owner_screen": SCREEN},
    {"rule_id": "CUST-R17", "name": "perception gap", "entity_type": "brand",
     "inputs": ["brain positioning", "brain identity", "brain language_bank"], "capability": "BRAND-C59", "owner_screen": SCREEN},
    {"rule_id": "CUST-R18", "name": "claim under fire", "entity_type": "brand",
     "inputs": ["brain claims", "brain language_bank"], "capability": "BRN-C03", "owner_screen": SCREEN},
    {"rule_id": "CUST-R19", "name": "lookalike page", "entity_type": "brand",
     "inputs": ["brain competitors"], "capability": "MONEY-C48", "owner_screen": SCREEN},
    {"rule_id": "CUST-R20", "name": "pushed offer answers no doubt", "entity_type": "offer",
     "inputs": ["brain offers", "brain objection_ladders"], "capability": "LIFE-C42", "owner_screen": SCREEN},
    {"rule_id": "CUST-R21", "name": "doubt season", "entity_type": "ladder_rung",
     "inputs": ["brain objection_ladders", "brain language_bank"], "capability": "SITE-C38", "owner_screen": SCREEN},
    {"rule_id": "CUST-R22", "name": "no approved messaging hierarchy", "entity_type": "brand",
     "inputs": ["brain positioning"], "capability": "BRAND-C33", "owner_screen": SCREEN},
    {"rule_id": "CUST-R23", "name": "brand health line falling", "entity_type": "metric",
     "inputs": ["monthly", "cohorts"], "capability": "LIFE-C20", "owner_screen": SCREEN},
    {"rule_id": "CUST-R24", "name": "avatar may be two buyers", "entity_type": "brand",
     "inputs": ["brain avatars", "brain products review_summary", "brain language_bank"], "capability": "BRAND-C12", "owner_screen": SCREEN},
    {"rule_id": "CUST-R25", "name": "avatar our ads never speak to", "entity_type": "brand",
     "inputs": ["brain avatars", "brain learnings hook_types"], "capability": "CREA-C06", "owner_screen": SCREEN},
    {"rule_id": "CUST-R26", "name": "avatar with high return risk", "entity_type": "brand",
     "inputs": ["brain products review_summary", "brain avatars", "brain language_bank"], "capability": "LIFE-C07", "owner_screen": SCREEN},
    {"rule_id": "CUST-R27", "name": "marketplace-led avatar", "entity_type": "brand",
     "inputs": ["brain avatars", "brain language_bank"], "capability": "PROD-C34", "owner_screen": SCREEN},
    {"rule_id": "CUST-R28", "name": "price-led avatar", "entity_type": "brand",
     "inputs": ["brain avatars", "brain objection_ladders", "brain offers"], "capability": "LIFE-C39", "owner_screen": SCREEN},
    {"rule_id": "CUST-R29", "name": "records due for a re-check", "entity_type": "brand",
     "inputs": ["brain avatars", "brain objection_ladders"], "capability": "BRAND-C15", "owner_screen": SCREEN},
    {"rule_id": "CUST-R30", "name": "thin read", "entity_type": "brand",
     "inputs": ["brain avatars", "brain learnings hook_types"], "capability": "BRAND-C01", "owner_screen": SCREEN},
    {"rule_id": "CUST-R31", "name": "reviews and sales disagree on who buys", "entity_type": "brand",
     "inputs": ["products_monthly", "fixtures sku_lines", "brain avatars", "brain language_bank"], "capability": "LIFE-C29", "owner_screen": SCREEN},
    {"rule_id": "CUST-R32", "name": "weak cohort", "entity_type": "metric",
     "inputs": ["cohorts", "monthly"], "capability": "LIFE-C07", "owner_screen": SCREEN},
]
AUTONOMY = {"BRAND-C11": "founder_gate", "BRAND-C13": "agent_does", "CREA-C03": "agent_does", "SITE-C38": "human_assist",
            "PROD-C73": "human_assist", "CREA-C24": "agent_does", "LIFE-C27": "human_assist", "BRAND-C16": "founder_gate",
            "MEDIA-C12": "human_assist", "LIFE-C20": "agent_does", "LIFE-C08": "founder_gate", "BRAND-C14": "agent_does",
            "LIFE-C50": "founder_gate", "BRAND-C05": "human_assist", "LIFE-C12": "founder_gate", "BRAND-C59": "agent_does",
            "BRN-C03": "founder_gate", "MONEY-C48": "human_assist", "LIFE-C42": "founder_gate", "BRAND-C33": "founder_gate",
            "BRAND-C12": "agent_does", "CREA-C06": "agent_does", "LIFE-C07": "founder_gate", "PROD-C34": "human_assist",
            "LIFE-C39": "founder_gate", "BRAND-C15": "agent_does", "BRAND-C01": "agent_does",
            "LIFE-C29": "founder_gate"}
SILENT_MIN_SHARE = 0.12
MOMENT_WARN_DAYS = 45
NO_DATA = "no revenue formula for this rule yet"


# ---------------------------------------------------------------- shared builders

OWN = "Our site"
OWN_HOSTS: set[str] = set()   # the brand's own hosts, read from the brain by own_hosts(brain) before any builder runs
SOURCE_NAMES = {"own_site_yotpo": OWN, "own_site": OWN, "trustpilot.com": "Trustpilot", "trustpilot": "Trustpilot",
                "amazon.com": "Amazon", "amazon": "Amazon", "amazon_customers_say": "Amazon",
                "nordstrom.com": "Nordstrom", "target.com": "Target", "sitejabber.com": "Sitejabber",
                "yahoo.com": "Press", "retailer": "Other retailers", "reddit": "Reddit", "reddit.com": "Reddit"}


def host(ref: str | None) -> str | None:
    h = urlparse(ref or "").netloc
    return h[4:] if h.startswith("www.") else (h or None)


def source_name(s: str | None) -> str:
    if s and (s in OWN_HOSTS or any(s.endswith("." + h) for h in OWN_HOSTS)):
        return OWN
    return SOURCE_NAMES.get(s or "", s or "unknown")


def own_hosts(brain: Brain) -> set[str]:
    """The brand's own web hosts from the brain (site map and identity urls), so its site reads as our site for any brand."""
    hosts = set()
    for sec in ("site_map", "identity", "sources"):
        for r in brain.records(sec):
            v = r.get("value")
            for url in re.findall(r"https?://[^\s\"',\]]+", json_text(v) + " " + str((r.get("source") or {}).get("ref") or "")):
                h = host(url)
                if h and brain.brand.lower() in h:
                    hosts.add(h)
                    hosts.add(".".join(h.split(".")[-2:]))
    OWN_HOSTS.clear()
    OWN_HOSTS.update(hosts)
    return hosts


def json_text(v) -> str:
    import json as _json
    try:
        return _json.dumps(v)
    except (TypeError, ValueError):
        return str(v)


def key(rid: str) -> str:
    return rid.split(".")[-1]


def expired(rec: dict, today: dt.date) -> bool:
    exp = rec.get("expires_at")
    return bool(exp) and dt.date.fromisoformat(exp[:10]) < today


def avatar_rows(brain: Brain) -> list[dict]:
    """One row per active avatar: share, intensity, job, quotes with links, grounding."""
    own_hosts(brain)
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
                    "tier": a["tier"], "date": a["date"], "expired": expired(a, brain.today), "expires_at": (a.get("expires_at") or "")[:10] or None,
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


AD_NAME = re.compile(r"(?:^|[|\s_-])(AV|ANG|FMT|HK)-([a-z0-9_]+)", re.I)


def parse_ad_name(name: str) -> dict:
    """Read the avatar, angle, format and hook tags from an ad name that follows the convention in builds.naming()."""
    out = {}
    for m in AD_NAME.finditer(str(name or "")):
        out[{"AV": "avatar", "ANG": "angle", "FMT": "format", "HK": "hook"}[m.group(1).upper()]] = m.group(2).lower()
    return out


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
    for g in groups:
        if not g.get("angle"):
            tag = parse_ad_name(g.get("name") or g.get("ad_name") or g.get("label") or "")
            if tag.get("angle"):
                g["angle"] = tag["angle"]
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
            "unavailable": unavailable, "money_reason": NO_MONEY if rule_id in ("CUST-R01", "CUST-R02", "CUST-R03", "CUST-R04", "CUST-R13", "CUST-R14") else NO_DATA}


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
    out = builds.mix(monthly, channels, as_of)
    if out.get("available"):
        try:
            paid = data.table("paid_media_monthly")
        except (ValueError, KeyError, FileNotFoundError):
            paid = None
        out["stake"] = builds.paid_stake(channels, paid, out["latest"])
    return out


def brand_tokens(brain: Brain) -> set[str]:
    """Words of the brand's own name, from the brain identity, so a phrase that only names the brand counts as generic."""
    toks = {brain.brand.lower()}
    for r in brain.records("identity"):
        if r.get("field") in ("name", "brand_name", "legal_name") and isinstance(r.get("value"), str):
            toks.update(t.lower().strip(".,") for t in r["value"].split())
    return toks


def competitor_names(brain: Brain) -> list[str]:
    """Competitor names from the brain, including brands Reddit recommends instead."""
    names = set()
    for r in brain.records("competitors"):
        v = r.get("value")
        if isinstance(v, dict):
            names.update(x for x in (v.get("name"), v.get("competitor")) if isinstance(x, str))
    for r in brain.records("positioning"):
        v = r.get("value")
        if isinstance(v, dict):
            for k in ("direct", "reddit_recommended_instead"):
                names.update(x for x in v.get(k) or [] if isinstance(x, str))
    return sorted(names)


def product_words(brain: Brain) -> set[str]:
    """Words that name the brand's product lines, from the brain's product records."""
    out = set()
    for r in brain.records("products"):
        v = r.get("value")
        if r.get("field") == "lines" and isinstance(v, list):
            out.update(w.lower() for x in v if isinstance(x, str) for w in re.findall(r"[A-Za-z]+", x))
        if isinstance(v, dict) and isinstance(v.get("product_line"), str):
            out.update(w for w in re.findall(r"[a-z]+", v["product_line"].lower()))
    return out


OUR_SECTIONS = ("voice", "claims", "identity", "offers", "policies", "products", "visual", "story_bank")


def load_moments(brand: str, avatars: list[dict]) -> dict:
    try:
        from tables import brand_data
        data = brand_data(brand)
        monthly, as_of = data.table("monthly"), data.brand.get("as_of")
    except (ImportError, ValueError, KeyError, FileNotFoundError) as exc:
        return {"rows": [], "line": f"No monthly table for {brand} ({exc})."}
    return builds.moments(avatars, monthly, as_of)


def load_paths(brand: str) -> dict:
    try:
        from tables import brand_data
        rows = brand_data(brand).table("customer_paths")
    except (ImportError, ValueError, KeyError, FileNotFoundError):
        return builds.paths(None, f"no customer_paths aggregate for {brand}; order rows are too large to read here")
    return builds.paths(rows)


def load_health(brand: str, avatars: list[dict]) -> dict:
    try:
        from tables import brand_data
        data = brand_data(brand)
        monthly, as_of = data.table("monthly"), data.brand.get("as_of")
    except (ImportError, ValueError, KeyError, FileNotFoundError) as exc:
        return {"available": False, "reason": str(exc), "rows": [], "missing": builds.MISSING_LINES, "moves": []}
    return builds.health(monthly, load_cohorts(brand, avatars).get("rows", []), as_of)


FIXTURES = Path(__file__).resolve().parent / "fixtures"


def load_line_sales(brain: Brain, lines: set[str]) -> dict:
    """Net sales by product line over the last 12 full months, from products_monthly and the SKU to line map
    (a local fixture until the data layer carries one). Unmapped sales are counted, never spread."""
    import json
    try:
        codes = json.loads((FIXTURES / "sku_lines" / f"{brain.brand}.json").read_text(encoding="utf-8")).get("codes") or {}
    except (OSError, ValueError):
        return {"available": False, "reason": "no SKU to product-line map for this brand yet"}
    try:
        from tables import brand_data
        data = brand_data(brain.brand)
        rows, as_of = data.table("products_monthly"), data.brand.get("as_of")
    except (ImportError, ValueError, KeyError, FileNotFoundError) as exc:
        return {"available": False, "reason": f"no products table ({exc})"}
    return builds.line_sales(rows, codes, lines, as_of)


def load_survey_answers(brain: Brain) -> dict | None:
    """The situation question's answers: the data layer's survey_answers table when it exists, else a local fixture.
    None when neither exists."""
    import json
    try:
        from tables import brand_data
        t = brand_data(brain.brand).table("survey_answers")
        if isinstance(t, dict):
            return t
    except (ImportError, ValueError, KeyError, FileNotFoundError):
        pass
    try:
        return json.loads((FIXTURES / "survey_answers" / f"{brain.brand}.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def load_sales_share(brain: Brain, avatars: list[dict], all_rungs: list[dict]) -> dict:
    """Share of sales per avatar through the lines it buys, next to its share from reviews."""
    mis = builds.misreads(brain.records("avatars"), avatars, all_rungs, brain.records("language_bank"), brain.records("products"))
    if not mis.get("available"):
        return {"available": False, "reason": "no review summary by product line in the brain", "rows": []}
    lines = {l["line"] for l in mis["lines"]}
    buys = builds.avatar_lines(brain.records("avatars"), all_rungs, brain.records("language_bank"), lines)
    return builds.sales_share(avatars, buys, load_line_sales(brain, lines))


def load_returns(brain: Brain, avatars: list[dict], all_rungs: list[dict]) -> dict:
    mis = builds.misreads(brain.records("avatars"), avatars, all_rungs, brain.records("language_bank"), brain.records("products"))
    if not mis.get("available"):
        return {"rows": []}
    buys = builds.avatar_lines(brain.records("avatars"), all_rungs, brain.records("language_bank"), {l["line"] for l in mis["lines"]})
    try:
        from tables import brand_data
        data = brand_data(brain.brand)
        monthly, as_of = data.table("monthly"), data.brand.get("as_of")
    except (ImportError, ValueError, KeyError, FileNotFoundError):
        monthly, as_of = [], (brain.today - dt.timedelta(days=1)).isoformat()
    return builds.return_risk(avatars, buys, mis["lines"], monthly, as_of)


def split_rows(brain: Brain, avatars: list[dict], all_rungs: list[dict]) -> dict:
    issues = {}
    for r in brain.records("products"):
        v = r.get("value")
        if r.get("field") == "review_summary" and isinstance(v, dict) and v.get("product_line"):
            issues[v["product_line"]] = v.get("issues") or []
    buys = builds.avatar_lines(brain.records("avatars"), all_rungs, brain.records("language_bank"), set(issues))
    return builds.split_check(avatars, all_rungs, buys, issues)


def with_tops(avatars, all_rungs):
    for a in avatars:
        top = top_objection(a["id"], all_rungs)
        a["top_objection"] = None if top is None else {"id": top["id"], "doubt": top["doubt"], "one_star": top["one_star"],
                                                        "five_star": top["five_star"], "proof": bool(top["proof_ids"]),
                                                        "proof_text": top["proof"] if top["proof_ids"] else None}
        if "next" not in a:
            a["next"] = builds.next_build(a, top)
    return avatars


def desk(brain: Brain, avatars: list[dict], all_rungs: list[dict]) -> dict:
    """Every desk builder the page and the rules share, computed once."""
    return {"ladders": builds.ladders(all_rungs, avatars),
            "misreads": builds.misreads(brain.records("avatars"), avatars, all_rungs, brain.records("language_bank"), brain.records("products")),
            "served": builds.served(avatars, all_rungs, brain.records("competitors"), brain.records("positioning")),
            "cohorts": load_cohorts(brain.brand, avatars), "mix": load_mix(brain.brand),
            "themes": builds.theme_impact(brain.records("language_bank"), builds.ladders(all_rungs, avatars)["rows"],
                                          (brain.today - dt.timedelta(days=1)).isoformat()),
            "copy_gap": builds.copy_gap({s_: brain.records(s_) for s_ in OUR_SECTIONS}, brain.records("language_bank"),
                                        brand_tokens(brain), source_name),
            "gate": builds.gate(avatars, all_rungs),
            "forces": builds.forces(avatars, all_rungs, brain.records("language_bank"), competitor_names(brain)),
            "moments": load_moments(brain.brand, avatars), "paths": load_paths(brain.brand),
            "perception": builds.perception(brain.records("positioning") + brain.records("identity"), brain.records("language_bank"),
                                            brand_tokens(brain), source_name),
            "claims_fire": builds.claims_fire(brain.records("claims"), brain.records("language_bank"), brand_tokens(brain), source_name,
                                              product_words(brain)),
            "lookalikes": builds.lookalikes(brain.records("competitors"), brain.brand.capitalize()),
            "offer_map": builds.offer_map(avatars, all_rungs, brain.records("offers"), brain.records("policies") + brain.records("claims")),
            "timing": builds.doubt_timing(all_rungs, brain.records("language_bank"), (brain.today - dt.timedelta(days=1)).isoformat(), source_name),
            "hierarchy_approved": any(r.get("field") == "messaging_hierarchy" for r in brain.raw("positioning")),
            "health": load_health(brain.brand, avatars),
            "split": split_rows(brain, avatars, all_rungs),
            "ad_voice": builds.ad_voice(avatars, brain.records("learnings")),
            "returns": load_returns(brain, avatars, all_rungs), "sales_share": load_sales_share(brain, avatars, all_rungs),
            "marketplace": builds.marketplace(avatars, all_rungs, brain.records("language_bank"), source_name),
            "price": builds.price_doubts(avatars, all_rungs, brain.records("offers"), brain.records("products")),
            "rechecks": builds.rechecks(avatars, brain.records("objection_ladders"), brain.today.isoformat())}


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
    return [_with_stake(_finding("CUST-R07", "medium", {"type": "metric", "id": "returning_via_paid", "label": "Returning orders through paid ads"},
                                 ev, s, "MEDIA-C12", 0.5, [], ends_on), x.get("stake"))]


def _with_stake(f: dict, st: dict | None) -> dict:
    """Puts a builder's stake on a finding in the audit.md shape, or its reason when the stake is null."""
    st = st or {}
    if isinstance(st.get("usd"), (int, float)) and st["usd"] > 0:
        f["money_at_stake"] = {k: st[k] for k in ("usd", "formula", "inputs", "window", "note") if k in st}
        f["money_reason"] = None
    elif st.get("reason"):
        f["money_reason"] = st["reason"]
    return f


def r08_r09(d, ends_on):
    c = d["cohorts"]
    if not c.get("available"):
        return []
    out = []
    cb = c.get("calendar_break")
    if cb:
        ev = [_ev("cohorts_falling_together", cb["share"], "%", ends_on, "cohorts", baseline=builds.CLIFF_SHARE, simulated=True),
              _ev("cohorts_alive", cb["cohorts"], "n", ends_on, "cohorts", simulated=True)]
        st = cb.get("stake") or {}
        s = f"In {cb['month']}, {round(cb['share'] * 100)} percent of {cb['cohorts']} cohorts fell 40 percent or more at once."
        if st.get("fall_last_year") is not None:
            ev.append(_ev("returning_fall_into_month", st["fall"], "%", ends_on, "monthly", baseline=st["fall_last_year"], simulated=True))
            ev.append(_ev("returning_fall_same_month_last_year", st["fall_last_year"], "%", ends_on, "monthly", simulated=True))
            s += (f" A year before, returning orders fell {round(st['fall_last_year'] * 100, 1)} percent too: the season."
                  if st.get("usd") is None else f" That is more than last year's {round(st['fall_last_year'] * 100, 1)} percent.")
        else:
            s += " Every past buyer went quiet together."
        out.append(_with_stake(_finding("CUST-R08", "medium", {"type": "metric", "id": "calendar_" + cb["month"], "label": f"Retention cliff, {cb['month']}"},
                                        ev, s, "LIFE-C20", 0.5, [], ends_on), cb.get("stake")))
    ab = c.get("age_break")
    if ab and ab["drop"] is not None and ab["drop"] >= 0.2:
        ev = [_ev("active_share_drop", ab["drop"], "%", ends_on, "cohorts", baseline=0.2, simulated=True)]
        s = f"Active share falls {round(ab['drop'] * 100)} percent from month {ab['month']} to month {ab['month'] + 1} after the first order."
        out.append(_with_stake(_finding("CUST-R09", "medium", {"type": "metric", "id": f"age_month_{ab['month']}", "label": f"Retention break, month {ab['month']}"},
                                        ev, s, "LIFE-C08", 0.5, [], ends_on), ab.get("stake")))
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


def r11_r12(d, ends_on):
    out = []
    x = d["themes"]
    for r in x.get("rows", []) if x.get("available") else []:
        if r["impact"] >= 0:
            continue
        ev = [_ev("theme_share", r["share"], "%", ends_on, "brain.language_bank"),
              _ev("star_gap", r["star_gap"], "n", ends_on, "brain.language_bank", baseline=0)]
        s = (f"Reviews about {r['theme'].replace('_', ' ')} run {abs(r['star_gap'])} stars below the rest. "
             f"They are {round(r['share'] * 100, 1)} percent of rated reviews.")
        out.append(_finding("CUST-R11", "high" if r["rising"] else "medium", {"type": "brand", "id": "theme_" + r["theme"], "label": r["theme"].replace("_", " ")},
                            ev, s, "BRAND-C13", 0.5, [], ends_on))
    g = d["copy_gap"]
    if g.get("available") and g["missing"] >= 3:
        ev = [_ev("praise_words_missing", g["missing"], "n", ends_on, "brain.language_bank", baseline=3)]
        top = ", ".join([r["word"] for r in g["rows"] if r["verdict"] == "missing"][:5])
        s = f"{g['missing']} of the top {len(g['rows'])} praise words never appear in our own words, like {top}."
        out.append(_finding("CUST-R12", "medium", {"type": "brand", "id": "copy_gap", "label": "Buyer words we never say"},
                            ev, s, "BRAND-C14", 0.5, [], ends_on))
    return out


def r13_r14(d, ends_on):
    out = []
    prov = [r for r in d["gate"]["rows"] if r["status"] == "provisional"]
    if prov:
        ev = [_ev("provisional_avatars", len(prov), "n", ends_on, "brain.avatars", baseline=0)]
        s = f"{len(prov)} of {len(d['gate']['rows'])} avatars fail a core evidence check. Briefs on them rest on a guess."
        out.append(_finding("CUST-R13", "medium", {"type": "brand", "id": "provisional_avatars", "label": "Provisional avatars"},
                            ev, s, "LIFE-C50", 0.5, [f"{d['brand']}.avatars.{r['key']}" for r in prov][:10], ends_on))
    for r in d["forces"]["rows"]:
        if not r["under"] or not r["lines"]:
            continue
        ev = [_ev("coded_lines", r["lines"], "n", ends_on, "brain.language_bank"),
              _ev("forces_missing", len(r["missing"]), "n", ends_on, "brain.language_bank", baseline=0)]
        miss = ", ".join(r["missing"]) or "anxiety and habit"
        s = f"We know why {r['name']} buyers like us, but have no lines on {miss}."
        out.append(_finding("CUST-R14", "low", {"type": "brand", "id": "forces_" + r["key"], "label": r["name"]},
                            ev, s, "BRAND-C05", 0.5, [f"{d['brand']}.avatars.{r['key']}"], ends_on))
    return out


def r15_r16(d, ends_on):
    out = []
    end = dt.date.fromisoformat(ends_on)
    for r in d["moments"].get("rows", []):
        days = (dt.date.fromisoformat(r["ad_by"]) - end).days
        if days > MOMENT_WARN_DAYS:
            continue
        ev = [_ev("days_to_ads_live", days, "days", ends_on, "brain.avatars", baseline=MOMENT_WARN_DAYS)]
        s = (f"{r['label']} starts {r['starts']}. Ads for {', '.join(r['avatars'][:2])} need to be live by {r['ad_by']}, "
             f"{days} days away." if days >= 0 else f"{r['label']} ads were due live by {r['ad_by']}.")
        out.append(_finding("CUST-R15", "high" if days < 0 else "medium",
                            {"type": "brand", "id": "moment_" + r["label"].lower().replace(" ", "_").replace("'", ""), "label": r["label"]},
                            ev, s, "LIFE-C20", 0.5, [], ends_on))
    p = d["paths"]
    if not p.get("available"):
        out.append(_finding("CUST-R16", "medium", {"type": "metric", "id": "customer_paths", "label": "Order-level paths"}, [],
                            "Gateway products, second-order paths and win-back timing cannot run. " + p["reason"][:1].upper() + p["reason"][1:] + ".",
                            "LIFE-C12", 0.5, [], ends_on, status="unavailable",
                            unavailable={"inputs": ["customer_paths"], "connector": "shopify",
                                         "fix": "Build the customer_paths aggregate from order rows (first product, next product, order gaps, value cells)."}))
    else:
        for m in p["moves"]:
            key = m["id"].split(".paths.")[1]
            ev = [_ev("paths_rule", 1, "n", ends_on, "customer_paths", simulated=True)]
            out.append(_finding("CUST-R16", "medium", {"type": "metric", "id": "paths_" + key.replace(".", "_"), "label": m["title"][:60]},
                                ev, m["title"] + ".", "LIFE-C12", 0.5, [], ends_on))
    return out


def r17_r23(d, ends_on):
    out = []
    p = d["perception"]
    if p.get("available") and p["score"] is not None and p["score"] < 0.5:
        ev = [_ev("buyer_words_in_positioning", p["score"], "%", ends_on, "brain.positioning", baseline=0.5)]
        miss = ", ".join(t["word"] for t in p["theirs"] if not t["in_positioning"])[:60].rsplit(",", 1)[0]
        s = f"Only {round(p['score'] * 100)} percent of the words buyers praise us with are in our positioning. Missing: {miss}."
        out.append(_finding("CUST-R17", "medium", {"type": "brand", "id": "perception_gap", "label": "Perception gap"}, ev, s, "BRAND-C59", 0.5, [], ends_on))
    for r in d["claims_fire"]["rows"]:
        if r["verdict"] != "under_fire":
            continue
        ev = [_ev("one_two_star_reviews_on_claim_words", r["hits"], "n", ends_on, "brain.language_bank", baseline=builds.CLAIM_HITS)]
        s = f"{r['hits']} reviews of 1 or 2 stars throw this claim's words back at us: {', '.join(r['words'][:3])}. The claim is under fire."
        out.append(_finding("CUST-R18", "high", {"type": "brand", "id": "claim_" + r["id"].split(".")[-1], "label": r["id"].split(".")[-1].replace("_", " ")},
                            ev, s, "BRN-C03", 0.5, [r["id"]], ends_on))
    for r in d["lookalikes"]["rows"]:
        ev = [_ev("impostor_ads_seen", r["ads_seen"], "n", ends_on, "brain.competitors", baseline=0)]
        s = f"A lookalike page ran {r['ads_seen']} ads that send buyers to {r['links_to']}. It uses our name."
        out.append(_finding("CUST-R19", "high", {"type": "brand", "id": f"lookalike_{r['page_id']}", "label": f"Lookalike page {r['page_id']}"},
                            ev, s, "MONEY-C48", 0.5, [r["id"]], ends_on))
    o = d["offer_map"]
    if o.get("action") and o.get("push"):
        ev = [_ev("ads_with_pushed_offer", o["push"]["ads"], "n", ends_on, "brain.offers"),
              _ev("doubts_it_answers", 0, "n", ends_on, "brain.objection_ladders", baseline=1)]
        s = f"{o['push']['ads']} of {o['push']['of']} live ads push a discount that answers none of our buyers' doubts."
        out.append(_finding("CUST-R20", "medium", {"type": "offer", "id": "pushed_offer", "label": "The offer our ads push"}, ev, s, "LIFE-C42", 0.5,
                            [o["push"]["id"]], ends_on))
    for m in d["timing"]["moves"]:
        ev = [_ev("season_lift", m["lift"], "x", ends_on, "brain.language_bank", baseline=builds.SEASON_LIFT)]
        s = f"{m['theme'].replace('_', ' ').capitalize()} complaints peak in {m['season']}: {round(m['share'] * 100)} percent of all complaints then."
        out.append(_finding("CUST-R21", "high" if m["late"] else "medium", {"type": "ladder_rung", "id": "season_" + m["theme"], "label": f"{m['theme'].replace('_', ' ')}, {m['season']}"},
                            ev, s, "SITE-C38", 0.5, [], ends_on))
    if not d["hierarchy_approved"] and any(r["impact"] > 0 for r in d["themes"].get("rows", [])):
        ev = [_ev("approved_hierarchy_records", 0, "n", ends_on, "brain.positioning", baseline=1)]
        out.append(_finding("CUST-R22", "low", {"type": "brand", "id": "messaging_hierarchy", "label": "Messaging hierarchy"}, ev,
                            "No approved lead line, proof points and first doubt to answer. Every page picks its own.", "BRAND-C33", 0.5, [], ends_on))
    for m in d["health"].get("moves", []):
        ev = [_ev("health_line_" + m["key"], 1, "n", ends_on, "monthly", simulated=True)]
        out.append(_finding("CUST-R23", "medium", {"type": "metric", "id": "health_" + m["key"], "label": m["title"][:60]}, ev, m["why"], "LIFE-C20", 0.5, [], ends_on))
    return out


def r24_r25(d, ends_on):
    out = []
    for r in d["split"]["rows"]:
        if r["verdict"] != "split":
            continue
        ev = [_ev("lines_over_30_percent", len(r["big_lines"]), "n", ends_on, "brain.language_bank", baseline=2)]
        s = f"{r['name']} buys {r['big_lines'][0].replace('_', ' ')} and {r['big_lines'][1].replace('_', ' ')} with different complaints. It may be two buyers."
        out.append(_finding("CUST-R24", "medium", {"type": "brand", "id": "split_" + r["key"], "label": r["name"]}, ev, s, "BRAND-C12", 0.5,
                            [f"{d['brand']}.avatars.{r['key']}"], ends_on))
    for r in d["ad_voice"].get("rows", []):
        if r["verdict"] != "silent" or (r["buyer_share"] or 0) < SILENT_MIN_SHARE:
            continue
        ev = [_ev("buyer_share", r["buyer_share"], "%", ends_on, "brain.avatars"),
              _ev("live_ads_matched", 0, "n", ends_on, "brain.learnings", baseline=1)]
        s = f"{r['name']} is about {round(r['buyer_share'] * 100)} percent of buyers. None of our live ads speaks to them."
        out.append(_finding("CUST-R25", "medium", {"type": "brand", "id": "silent_" + r["key"], "label": r["name"]}, ev, s, "CREA-C06", 0.5,
                            [f"{d['brand']}.avatars.{r['key']}"], ends_on))
    return out


def r26_r30(d, avatars, ends_on):
    out = []
    ref = lambda k: [f"{d['brand']}.avatars.{k}"]
    for r in d["returns"].get("rows", []):
        if r["verdict"] != "high":
            continue
        ev = [_ev("return_risk_vs_median", r["ratio"], "x", ends_on, "brain.products.review_summary", baseline=builds.RISK_HIGH)]
        s = f"{r['name']} carries {r['ratio']}x the median return risk, driven by {r['driver'].replace('_', ' ')}: {r['driver_issue']}."
        out.append(_finding("CUST-R26", "medium", {"type": "brand", "id": "returns_" + r["key"], "label": r["name"]}, ev, s, "LIFE-C07", 0.5, ref(r["key"]), ends_on))
    for r in d["marketplace"]["rows"]:
        if r["verdict"] != "marketplace" or not r["amazon_doubts"]:
            continue
        ev = [_ev("amazon_share_of_reviews", r["amazon_share"], "%", ends_on, "brain.language_bank", baseline=builds.MARKET_SHARE)]
        s = f"{round(r['amazon_share'] * 100)} percent of {r['name']}'s reviews are on Amazon, led by \"{r['amazon_doubts'][0]['doubt']}\"."
        out.append(_finding("CUST-R27", "medium", {"type": "brand", "id": "market_" + r["key"], "label": r["name"]}, ev, s, "PROD-C34", 0.5, ref(r["key"]), ends_on))
    for r in d["price"]["rows"]:
        if r["verdict"] != "price_led":
            continue
        ev = [_ev("price_share_of_one_star", r["price_share"], "%", ends_on, "brain.objection_ladders", baseline=builds.PRICE_LED)]
        s = f"{round(r['price_share'] * 100)} percent of {r['name']}'s one-star mentions are about price."
        out.append(_finding("CUST-R28", "medium", {"type": "brand", "id": "price_" + r["key"], "label": r["name"]}, ev, s, "LIFE-C39", 0.5, ref(r["key"]), ends_on))
    rc = d["rechecks"]
    if rc["due"]:
        first = min(r["expires"] for r in rc["rows"] if r["status"] in ("due", "expired"))
        ev = [_ev("records_due", rc["due"], "n", ends_on, "brain.avatars", baseline=0)]
        out.append(_finding("CUST-R29", "low", {"type": "brand", "id": "rechecks", "label": "Records due for a re-check"}, ev,
                            f"{rc['due']} avatar and ladder records stop being trusted by {first}.", "BRAND-C15", 0.5, [], ends_on))
    quotes = sum(a["quote_count"] for a in avatars)
    if quotes < builds.THIN_ITEMS * 2:
        ev = [_ev("avatar_quotes", quotes, "n", ends_on, "brain.avatars", baseline=builds.THIN_ITEMS * 2)]
        out.append(_finding("CUST-R30", "low", {"type": "brand", "id": "thin_quotes", "label": "Avatar quotes"}, ev,
                            f"All avatars together rest on {quotes} quotes, under {builds.THIN_ITEMS * 2}.", "BRAND-C01", 0.5, [], ends_on))
    ads = d["ad_voice"].get("total_ads")
    if ads is not None and ads < builds.THIN_ITEMS:
        ev = [_ev("live_ads_read", ads, "n", ends_on, "brain.learnings", baseline=builds.THIN_ITEMS)]
        out.append(_finding("CUST-R30", "low", {"type": "brand", "id": "thin_ads", "label": "Live ads read"}, ev,
                            f"The ad read rests on {ads} live ads, under {builds.THIN_ITEMS}.", "BRAND-C01", 0.5, [], ends_on))
    return out


def r31(d, ends_on):
    x = d.get("sales_share") or {}
    if not x.get("available"):
        if x.get("reason") and "products table" in str(x.get("reason")):
            return [_finding("CUST-R31", "low", {"type": "brand", "id": "sales_share", "label": "Share of sales by avatar"}, [],
                             "Sales by product line cannot be read, so avatar shares rest on reviews alone.", "LIFE-C29", 0.5, [], ends_on,
                             status="unavailable", unavailable={"inputs": ["products_monthly"], "connector": "shopify",
                                                                "fix": "Connect the store's product sales, read-only."})]
        return []
    out = []
    for r in x["rows"]:
        if r["verdict"] not in ("sales_higher", "reviews_higher", "sales_only"):
            continue
        ev = [_ev("sales_share", r["sales_share"], "%", ends_on, "products_monthly", simulated=True)]
        if r["review_share"] is not None:
            ev.append(_ev("review_share", r["review_share"], "%", ends_on, "brain.avatars"))
            ev.append(_ev("sales_to_review_ratio", r["ratio"], "x", ends_on, "products_monthly", baseline=builds.SALES_GAP))
            s = f"{r['name']} is {round(r['review_share'] * 100)} percent of buyers by reviews but {round(r['sales_share'] * 100, 1)} percent of sales by line."
        else:
            s = f"Reviews give {r['name']} no share; the lines it buys carry {round(r['sales_share'] * 100, 1)} percent of sales."
        out.append(_finding("CUST-R31", "low", {"type": "brand", "id": "salesshare_" + r["key"], "label": r["name"]}, ev, s, "LIFE-C29", 0.5,
                            [f"{d['brand']}.avatars.{r['key']}"], ends_on))
    return out


def r32(d, ends_on):
    c = d["cohorts"]
    if not c.get("available"):
        return []
    out = []
    rows = {r["cohort"]: r for r in c["rows"]}
    for m in c.get("weak") or []:
        r = rows[m]
        ev = [_ev("repeat_m1_m3", r["repeat_m1_m3"], "%", ends_on, "cohorts", baseline=round(builds.WEAK_COHORT * c["repeat_median"], 4), simulated=True),
              _ev("median_repeat_m1_m3", round(c["repeat_median"], 4), "%", ends_on, "cohorts", simulated=True)]
        s = (f"First buyers from {m} came back at {round(r['repeat_m1_m3'] * 100, 1)} percent in months 1 to 3, "
             f"against a median of {round(c['repeat_median'] * 100, 1)} percent.")
        out.append(_with_stake(_finding("CUST-R32", "medium", {"type": "metric", "id": "weak_" + m, "label": f"Weak cohort, {m}"},
                                        ev, s, "LIFE-C07", 0.5, [], ends_on), (c.get("weak_stakes") or {}).get(m)))
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
                + r04(d, all_rungs, ends_on) + r05(d, ends_on) + r06(d, ends_on) + r07(d, ends_on) + r08_r09(d, ends_on) + r10(d, ends_on)
                + r11_r12(d, ends_on) + r13_r14(d, ends_on) + r15_r16(d, ends_on) + r17_r23(d, ends_on) + r24_r25(d, ends_on) + r26_r30(d, avatars, ends_on) + r31(d, ends_on) + r32(d, ends_on))
    findings.sort(key=lambda f: (SEVERITY_ORDER[f["severity"]], f["rule_id"], f["id"]))
    return findings
