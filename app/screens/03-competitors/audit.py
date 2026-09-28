"""Competitors and market audit, plus the market model the screen api reads.

Contract: app/contracts/audit.md. `run(brand, window)` reads only
app/brain/<brand>/ (through app/brain/store.py, plus the per-competitor records
in raw/b-adlibrary/ as a fallback) and app/data/brands/<brand>/ (through
app/data/tables.py) and returns findings sorted by severity. No connector, no
model, no writes. Same brain, same tables, same window, same output.

Competitor numbers are public signals from the Meta Ad Library and public
product feeds. Run length is a signal, never proof that an ad works. Bombas
prices per pair come from the simulated `products_monthly` table.

Rules (thresholds are constants below):

COMP-R01 unclaimed angle. An angle the brand holds in the brain (ANGLES, each
    tied to a brain record) that none of the tracked competitors shows in its
    hooks, positioning or push, while the brand runs it in under
    ANGLE_SHARE_MAX (25 percent) of its active ads. Severity medium (a gap
    with no money formula). Capability BRAND-C21 (founder gate).
    Owner: 03-competitors.
COMP-R02 price gap. price_position_index (brand median price per pair /
    median of the competitors' median price per pair x 100) is outside the
    band PRICE_BAND (85 to 115). One capture, so severity medium and the
    baseline is a peer band. Capability BRAND-C24 (founder gate).
    Owner: 03-competitors.
COMP-R03 same offer type, run longer. A competitor shows an offer type the
    brand also has (OFFER_TYPES) and its longest-running ad has been live
    longer than the brand has run that offer type in ads. Severity medium.
    Capability BRAND-C24 (a guarantee or discount is a premium signal).
    Owner: 03-competitors.
COMP-R04 lookalike page. The brain has a competitors record whose verdict is
    an impostor or lookalike page. Severity medium (known downstream cost, no
    money formula). Capability MONEY-C48 (human assist). Owner: 03-competitors.
COMP-R05 coverage gap. A cell of the creative coverage matrix (coverage.py:
    angle by format) where the tracked pages put RULE_MIN (3 percent) or more of
    their ads and we put none, and the brain holds our proof for the angle. Top
    RULE_TOP (3) cells by their share. Severity medium. Capability CREA-C06
    (agent does the brief; a person approves before anything is made).
    Estimated from page-level mixes until an ad-level snapshot exists, so
    confidence 0.3; 0.5 with a snapshot. Owner: 03-competitors.
COMP-R06 first line gap. A first line kind (mix.py) at FL_SHARE (5 percent)
    or more of the ads on FL_PAGES (3) or more tracked pages and under FL_OURS
    (2 percent) of ours. Severity low (a copy test, not a break). Capability
    CREA-C04 (agent does the hook bank). Owner: 03-competitors.
COMP-R07 offer we hold and never say. An offer type seen on OFFER_PAGES (3) or
    more tracked pages, held in our brain (free shipping threshold, guarantee,
    pack ladder, gifting) and in none of our ads. Severity medium. Capability
    LIFE-C47 (offer test). Owner: 03-competitors.
COMP-R08 discount on most ads. OUR_PROMO (50 percent) or more of our active
    ads push a code while NO_OFFER_PAGES (2) or more direct competitors show no
    offer. Severity medium (the room's "discounting undercuts a premium
    position" rule, read from ads because competitor discount depth is not
    captured). Capability LIFE-C38 (founder gate). Owner: 03-competitors.
COMP-R09 shallow pack ladder. The median per-pair saving from a single pair to
    the biggest pack across our styles (ladder.py, simulated net prices) is under
    LADDER_MIN (10 percent) while a tracked page advertises a bundle saving of
    BUNDLE_MIN (15 percent) or more. Severity medium. Capability LIFE-C39
    (founder gate). Owner: 03-competitors.
COMP-R10 priced above with no proof. A style's single pair sits above the
    median of the direct peers' medians and the brain has no proof point for
    that style. Severity medium. Capability CREA-C31 (price framing on the
    page). Owner: 03-competitors.
COMP-R11 open strong-claim corner. On the positioning map (price per pair
    split at the tracked median, claim score split at the middle of its scale),
    a strong-claim quadrant with no tracked brand in it, with 3 or more brands
    placed. Severity medium. Capability BRAND-C20 (test the positioning line
    that takes it). Owner: 03-competitors.
COMP-R12 direct competitor refreshed its ads. A direct competitor whose oldest
    active ad is under REFRESH_DAYS (14) days old has replaced every ad it runs
    (changes.py). Severity low. Capability BRN-C11 (agent reads the new flight).
    Owner: 03-competitors.
COMP-R13 tracked page with no page id. A page in the competitive frame with no
    Ad Library page id: it cannot be pulled (page ids only, never keyword).
    Severity low. Capability BRN-C11; owner person (paste the id). Owner screen
    03-competitors.
COMP-R14 stale capture. The oldest competitor capture is older than
    STALE_DAYS (14). Severity medium. Capability BRN-C11; owner person (approves
    the Apify spend shown before the run). Owner: 03-competitors.

Rubric overrides (depth.md section 4 allows reputation and satisfaction per rule):
COMP-R01 reputation 5: an unclaimed angle is a competitor position gap named in
    the brain. COMP-R02 reputation 3: price sits inside the positioning.
    COMP-R04 reputation 5 and satisfaction 4: a page that impersonates
    the brand is a trust break, and shoppers who buy from it open tickets.

Money at stake is null for every rule: none of these gaps has a baseline in
the brand's own history yet. Confidence: one capture is one window (0.5),
minus 0.2 when the baseline is a peer band, minus 0.2 when the input record
is past its expires_at. Floor 0.1.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import statistics
import sys
from pathlib import Path

APP = Path(__file__).resolve().parents[2]
for _p in (APP / "brain", APP / "data"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from store import Brain, with_defaults  # noqa: E402

HERE = Path(__file__).resolve().parent


def _local(name: str):
    import importlib.util
    key = f"competitors_{name}"
    if key in sys.modules:
        return sys.modules[key]
    spec = importlib.util.spec_from_file_location(key, HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[key] = mod
    spec.loader.exec_module(mod)
    return mod


snap = _local("snapshot")
pagemod = _local("pages")
covmod = _local("coverage")
laddermod = _local("ladder")
mixmod = _local("mix")
refmod = _local("references")
changemod = _local("changes")

SCREEN = "03-competitors"
SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}
PRICE_BAND = (85, 115)
STALE_DAYS = 14
ANGLE_SHARE_MAX = 0.25
DURABILITY_MAX = 3
COMFORT_MAX = 3
NOT_COMPETITORS = {"competitor_set", "lookalike_page"}

# Angles the brand can own. `keys` match competitor hooks, positioning and push, and the brand's own hooks.
ANGLES = [
    {"key": "giving", "label": "giving", "keys": ["giving", "donat", "mission", "one purchased"],
     "brain_ref": "identity.giving_model"},
    {"key": "b_corp", "label": "B Corp", "keys": ["b corp", "b-corp", "bcorp"],
     "brain_ref": "identity.b_corp_certified"},
    {"key": "comfort_relief", "label": "comfort and relief", "keys": ["relief", "comfort"],
     "brain_ref": "claims.brand_positioning"},
]
OFFER_TYPES = [
    {"key": "guarantee", "label": "guarantee", "keys": ["guarantee"], "brain_ref": "offers.guarantee"},
    {"key": "discount", "label": "discount", "keys": ["discount", "% off", "bundle save", "code"],
     "brain_ref": "offers.first_order_code", "share_ref": "offers.promo_share_active_ads"},
]
RULES = [
    {"rule_id": "COMP-R01", "name": "unclaimed angle", "entity_type": "offer",
     "inputs": ["brain competitors", "brain learnings.hook_types", "brain story_bank"],
     "capability": "BRAND-C21", "owner_screen": SCREEN},
    {"rule_id": "COMP-R02", "name": "price gap", "entity_type": "metric",
     "inputs": ["brain competitors price_band_usd", "products_monthly"], "capability": "BRAND-C24",
     "owner_screen": SCREEN},
    {"rule_id": "COMP-R03", "name": "same offer type, run longer", "entity_type": "offer",
     "inputs": ["brain competitors", "brain offers", "brain learnings.hook_types"], "capability": "BRAND-C24",
     "owner_screen": SCREEN},
    {"rule_id": "COMP-R04", "name": "lookalike page", "entity_type": "page",
     "inputs": ["brain competitors.lookalike_page"], "capability": "MONEY-C48", "owner_screen": SCREEN},
    {"rule_id": "COMP-R05", "name": "coverage gap: an angle and format they run and we do not", "entity_type": "ad",
     "inputs": ["brain competitors", "brain learnings", "brain positioning.proof_points", "Ad Library snapshot"],
     "capability": "CREA-C06", "owner_screen": SCREEN},
    {"rule_id": "COMP-R06", "name": "first line kind they use and we do not", "entity_type": "ad",
     "inputs": ["brain competitors hook_types", "brain learnings adlib formats"], "capability": "CREA-C04",
     "owner_screen": SCREEN},
    {"rule_id": "COMP-R07", "name": "offer we hold and never say while they do", "entity_type": "offer",
     "inputs": ["brain competitors offers_seen", "brain offers"], "capability": "LIFE-C47", "owner_screen": SCREEN},
    {"rule_id": "COMP-R09", "name": "shallow pack ladder while a peer sells bundles", "entity_type": "offer",
     "inputs": ["products_monthly", "brain competitors offers_seen and hook_types"], "capability": "LIFE-C39",
     "owner_screen": SCREEN},
    {"rule_id": "COMP-R10", "name": "priced above the direct median with no proof", "entity_type": "sku",
     "inputs": ["products_monthly", "brain competitors price_band_usd", "brain positioning.proof_points"],
     "capability": "CREA-C31", "owner_screen": SCREEN},
    {"rule_id": "COMP-R11", "name": "open strong-claim corner on the positioning map", "entity_type": "brand",
     "inputs": ["brain competitors price_band_usd, hook_types, positioning"], "capability": "BRAND-C20",
     "owner_screen": SCREEN},
    {"rule_id": "COMP-R12", "name": "direct competitor replaced every ad in 14 days", "entity_type": "page",
     "inputs": ["brain competitors longest_running_ad", "Ad Library snapshot"], "capability": "BRN-C11", "owner_screen": SCREEN},
    {"rule_id": "COMP-R13", "name": "tracked page with no page id", "entity_type": "page",
     "inputs": ["brain positioning.competitive_frame", "config/apify.json pages"], "capability": "BRN-C11", "owner_screen": SCREEN},
    {"rule_id": "COMP-R14", "name": "stale competitor capture", "entity_type": "brand",
     "inputs": ["brain competitors captured_at", "Ad Library snapshot"], "capability": "BRN-C11", "owner_screen": SCREEN},
    {"rule_id": "COMP-R08", "name": "discount on most ads while direct peers run none", "entity_type": "offer",
     "inputs": ["brain offers.promo_share_active_ads", "brain competitors offers_seen"], "capability": "LIFE-C38",
     "owner_screen": SCREEN},
]
RUBRIC_OVERRIDES = {"COMP-R01": {"reputation": 5}, "COMP-R02": {"reputation": 3}, "COMP-R04": {"reputation": 5, "satisfaction": 4}}
AUTONOMY = {"BRN-C11": "agent_does", "BRAND-C20": "agent_does", "LIFE-C39": "founder_gate", "CREA-C31": "agent_does", "CREA-C06": "agent_does", "CREA-C04": "agent_does", "LIFE-C47": "agent_does", "LIFE-C38": "founder_gate", "BRAND-C21": "founder_gate", "BRAND-C24": "founder_gate", "MONEY-C48": "human_assist"}


# ---------------------------------------------------------------- reading

def _num(s):
    return float(s) if s is not None else None


def parse_band(text: str | None) -> dict:
    """'12 to 25 per pair, median about 18' -> low, high, median per pair. A range quoted per product
    is not a per pair range, so only its median is kept. 'rough' in the text marks rough parsing."""
    t = (text or "").lower()
    med = re.search(r"median(?: about)? (\d+(?:\.\d+)?)", t)
    rng = re.search(r"(\d+(?:\.\d+)?) to (\d+(?:\.\d+)?) per (pair|product)", t)
    frm = re.search(r"from (\d+(?:\.\d+)?) per pair", t)
    low = high = None
    if rng and rng.group(3) == "pair":
        low, high = float(rng.group(1)), float(rng.group(2))
    elif frm:
        low = float(frm.group(1))
    return {"low": low, "high": high, "median": _num(med.group(1)) if med else None,
            "rough": "rough" in t, "per_product_range": bool(rng and rng.group(3) == "product"),
            "text": text}


def _raw_competitors(brain: Brain) -> list[dict]:
    path = brain.dir / "raw" / "b-adlibrary" / "competitors.json"
    if not path.exists():
        return []
    return [with_defaults(r, brain.today) for r in json.loads(path.read_text(encoding="utf-8"))]


def _hits(text: str, keys: list[str]) -> bool:
    t = text.lower()
    return any(k in t for k in keys)


DURABILITY_PARTS = [("a guarantee", ["guarantee"]), ("a lifetime promise", ["lifetime"]), ("durability named", ["durab"])]
COMFORT_PARTS = [("comfort named", ["comfort"]), ("a relief hook", ["relief"]),
                 ("a proof hook (lab, doctor, athlete or creator)", ["lab tested", "doctor", "athlete testimonial", "creator testimonial"])]


def score_parts(texts: list[str], axis: str) -> list[dict]:
    """Which claim points a page has and which it misses, for the positioning moves."""
    t = " ".join(texts).lower()
    parts = DURABILITY_PARTS if axis == "durability" else COMFORT_PARTS
    return [{"part": name, "has": any(k in t for k in keys)} for name, keys in parts]


def durability_score(texts: list[str]) -> int:
    """0 to 3: a guarantee is claimed, the guarantee is lifetime, durability is named in the positioning."""
    t = " ".join(texts).lower()
    return int("guarantee" in t) + int("lifetime" in t) + int("durab" in t)


def comfort_score(texts: list[str]) -> int:
    """0 to 3: comfort is named, a relief hook runs, a proof hook runs (lab, doctor, athlete or creator)."""
    t = " ".join(texts).lower()
    proof = any(k in t for k in ("lab tested", "doctor", "athlete testimonial", "creator testimonial"))
    return int("comfort" in t) + int("relief" in t) + int(proof)


def competitors(brain: Brain) -> list[dict]:
    """The competitor set as dicts: brain records first, raw Ad Library records for anything missing."""
    recs = {r["id"]: dict(r, origin="brain") for r in brain.records("competitors")}
    for r in _raw_competitors(brain):
        recs.setdefault(r["id"], dict(r, origin="raw b-adlibrary"))
    out = []
    for rid in sorted(recs):
        r = recs[rid]
        v = r.get("value")
        if r.get("field") in NOT_COMPETITORS or not isinstance(v, dict) or not v.get("name"):
            continue
        hooks = list(v.get("hook_types") or [])
        texts = hooks + [v.get("positioning") or "", v.get("what_they_push") or ""]
        longest = v.get("longest_running_ad") or {}
        out.append({"id": rid, "name": v["name"], "positioning": v.get("positioning"),
                    "what_they_push": v.get("what_they_push"), "formats": list(v.get("formats") or []),
                    "hooks": hooks, "active_ads": v.get("active_ads_seen"),
                    "longest_days": longest.get("days_running"), "longest_start": longest.get("start_date"),
                    "longest_url": longest.get("ad_url"), "ad_library_url": v.get("ad_library_url"),
                    "price": parse_band(v.get("price_band_usd")), "price_ref": v.get("price_ref"),
                    "durability": durability_score(texts), "comfort": comfort_score(texts),
                    "captured_at": r["date"], "age_days": r["age_days"], "expired": r["expired"],
                    "origin": r["origin"], "_texts": texts})
    return out


def lookalike(brain: Brain) -> dict | None:
    for r in brain.records("competitors"):
        v = r.get("value")
        if isinstance(v, dict) and re.search(r"impostor|lookalike", str(v.get("verdict") or r.get("field")), re.I):
            return {"id": r["id"], "page_id": v.get("page_id"), "verdict": v.get("verdict"),
                    "ads_seen": v.get("ads_seen"), "created": v.get("created"), "links_to": v.get("links_to"),
                    "text": r.get("text"), "ref": (r.get("source") or {}).get("ref"), "captured_at": r["date"]}
    return None


def _value(brain: Brain, key: str):
    rec = brain.get(f"{brain.brand}.{key}")
    return rec.get("value") if rec and rec["status"] != "retired" else None


def brand_profile(brain: Brain) -> dict:
    """The brand's own public signals: hooks by count, active ads, claims, offers."""
    hooks = _value(brain, "learnings.hook_types") or {}
    snap = _value(brain, "learnings.active_ads_snapshot") or {}
    texts = [str(_value(brain, k) or "") for k in
             ("identity.one_line_pitch", "claims.brand_positioning", "offers.guarantee")] + list(hooks)
    active = snap.get("active_ads")
    return {"hooks": hooks, "active_ads": active, "formats": snap.get("formats") or {},
            "durability": durability_score(texts), "comfort": comfort_score(texts), "_texts": texts}


def brand_ads_with(brain: Brain, profile: dict, keys: list[str]) -> int:
    """Active brand ads that carry an angle: hook counts that match, or a story_bank share like '2 of 23'."""
    n = sum(c for h, c in profile["hooks"].items() if isinstance(c, int) and _hits(h, keys))
    for r in brain.records("story_bank"):
        v = r.get("value") if isinstance(r.get("value"), dict) else {}
        if _hits(" ".join([r.get("field") or "", str(v.get("line") or "")]), keys):
            m = re.match(r"(\d+) of (\d+)", str(v.get("share") or ""))
            if m:
                n = max(n, int(m.group(1)))
    return n


def last_full_month(as_of: str) -> str:
    d = dt.date.fromisoformat(as_of)
    if (d + dt.timedelta(days=1)).month != d.month:
        return d.strftime("%Y-%m")
    return (d.replace(day=1) - dt.timedelta(days=1)).strftime("%Y-%m")


def brand_packs(brand: str) -> dict:
    """Sock packs from the simulated products_monthly table: net price per pack and per pair, last full month.
    Returns {available: False, reason} when the data layer has no table for the brand."""
    try:
        import tables
        data = tables.brand_data(brand)
        rows = data.table("products_monthly")
        as_of = data.brand.get("as_of")
        simulated = bool(data.meta("products_monthly").get("simulated"))
    except (ValueError, KeyError, OSError) as exc:
        return {"available": False, "reason": f"no products_monthly for {brand}: {exc}", "packs": []}
    month = last_full_month(as_of) if as_of else max(r["month"] for r in rows)
    packs = []
    for r in rows:
        if r.get("month") != month or r.get("category") != "socks" or not r.get("units"):
            continue
        parts = str(r["sku"]).split("-")
        try:
            pairs = int(parts[-1])
        except ValueError:
            continue
        per_pack = r["net_sales"] / r["units"]
        style = laddermod.style_of(r["sku"])
        packs.append({"sku": r["sku"], "label": f"{(style[0] if style else parts[1]).capitalize()}, "
                      f"{'single' if pairs == 1 else str(pairs) + '-pack'}", "pairs": pairs,
                      "units": r["units"], "per_pack": round(per_pack, 2), "per_pair": round(per_pack / pairs, 2)})
    packs.sort(key=lambda p: (p["per_pair"], p["sku"]))
    if not packs:
        return {"available": False, "reason": f"no sock rows in products_monthly for {month}", "packs": []}
    # unit weighted median per pair: each pack sold counts once
    total = sum(p["units"] for p in packs)
    run = 0
    median = packs[-1]["per_pair"]
    for p in packs:
        run += p["units"]
        if run * 2 >= total:
            median = p["per_pair"]
            break
    return {"available": True, "month": month, "as_of": as_of, "simulated": simulated, "packs": packs,
            "median_per_pair": median, "low": packs[0]["per_pair"], "high": packs[-1]["per_pair"]}


# ---------------------------------------------------------------- the market model

def market(brand: str, today: dt.date, root: Path | None = None) -> dict:
    brain = Brain(brand, root, today)
    comps = competitors(brain)
    prof = brand_profile(brain)
    packs = brand_packs(brand)
    medians = [c["price"]["median"] for c in comps if c["price"]["median"] is not None]
    cat_median = round(statistics.median(medians), 2) if medians else None
    index = (round(packs["median_per_pair"] / cat_median * 100, 1)
             if packs["available"] and cat_median else None)

    angles = []
    for a in ANGLES:
        held = _value(brain, a["brain_ref"]) is not None
        users = [c["name"] for c in comps if _hits(" ".join(c["_texts"]), a["keys"])]
        angles.append({"key": a["key"], "label": a["label"], "held": held,
                       "brain_ref": f"{brand}.{a['brain_ref']}", "competitors_using": users,
                       "brand_ads": brand_ads_with(brain, prof, a["keys"]), "brand_active_ads": prof["active_ads"]})
    for c in comps:
        c["gap_to_own"] = [a["label"] for a in angles if a["held"] and c["name"] not in a["competitors_using"]]

    snapshot = snap.load(brand)
    pages = pagemod.build(brain, _value(brain, "positioning.competitive_frame"), snap, snapshot, prof)
    us = next(p for p in pages if p["role"] == "self")
    top = pagemod.our_top_angles(us)
    for p in pages:
        if p["role"] != "self":
            p["verdict"] = pagemod.verdict(p, us, top)
    cov = covmod.matrix(pages, snap.ANGLES, snapshot, brain)
    points = covmod.proof_points(brain)
    refs = refmod.build(pages, top, snap.FORMAT_LABEL, lambda a: covmod.proof_for(points, a))
    return {"brand": brand, "brain": brain, "competitors": comps, "profile": prof, "packs": packs,
            "references": refs, "ladder": None, "mix": mixmod.build(pages, brain, snap),
            "coverage": cov,
            "coverage_direct": covmod.matrix(pages, snap.ANGLES, snapshot, brain, direct_only=True),
            "pages": pages, "snapshot": {k: v for k, v in (snapshot or {}).items() if k != "ads"} or None,
            "our_top_angles": top,
            "category_median": cat_median, "price_position_index": index, "angles": angles,
            "offer_runs": offer_runs(brain, comps, prof), "lookalike": lookalike(brain),
            "competitor_set": _value(brain, "competitors.competitor_set") or []}


def market_full(brand: str, today: dt.date, root: Path | None = None) -> dict:
    m = market(brand, today, root)
    m["ladder"] = laddermod.build(m, m["brain"])
    cur = snap.load(brand)
    prev = snap.load(brand, before=cur["captured_at"]) if cur else None
    m["changes"] = changemod.build(m, m["brain"], prev, cur, today)
    return m


def offer_runs(brain: Brain, comps: list[dict], prof: dict) -> list[dict]:
    """Per offer type the brand holds: how long the brand has run it in ads, and the longest competitor run."""
    out = []
    for o in OFFER_TYPES:
        rec = _value(brain, o["brain_ref"])
        if rec is None:
            continue
        in_ads = brand_ads_with(brain, prof, o["keys"])
        share = _value(brain, o["share_ref"]) if o.get("share_ref") else None
        if isinstance(share, dict) and isinstance(share.get("ads_with_code"), int):
            in_ads = max(in_ads, share["ads_with_code"])
        days = 0
        if isinstance(rec, dict) and rec.get("first_seen_in_ads") and rec.get("last_seen_in_ads"):
            days = (dt.date.fromisoformat(rec["last_seen_in_ads"]) - dt.date.fromisoformat(rec["first_seen_in_ads"])).days
            in_ads = max(in_ads, 1)
        refs = [f"{brain.brand}.{o['brain_ref']}"] + ([f"{brain.brand}.{o['share_ref']}"] if share else [])
        users = [c for c in comps if _hits(" ".join(c["hooks"]), o["keys"]) and c["longest_days"] is not None]
        users.sort(key=lambda c: (-c["longest_days"], c["name"]))
        out.append({"key": o["key"], "label": o["label"], "brain_ref": refs[0], "brain_refs": refs,
                    "brand_days": days, "brand_ads": in_ads, "brand_active_ads": prof["active_ads"],
                    "competitors": [{"name": c["name"], "id": c["id"], "days": c["longest_days"]} for c in users]})
    return out


# ---------------------------------------------------------------- findings

def _row(metric, value, unit, window, ends_on, freshness_days, baseline, baseline_kind, source, simulated=False):
    return {"metric": metric, "value": value, "unit": unit, "window": window, "ends_on": ends_on,
            "freshness_days": freshness_days, "baseline": baseline, "baseline_kind": baseline_kind,
            "source": source, "simulated": simulated}


def _finding(rule_id, severity, entity, evidence, sentence, brain_refs, ends_on, confidence, money_reason):
    cap = next(r["capability"] for r in RULES if r["rule_id"] == rule_id)
    return {"id": f"{SCREEN}.{rule_id}.{entity['id']}", "screen": SCREEN, "rule_id": rule_id,
            "severity": severity, "entity": entity, "evidence": evidence, "sentence": sentence,
            "capability": {"id": cap, "autonomy": AUTONOMY[cap]}, "money_at_stake": None,
            "money_reason": money_reason, "confidence": round(max(0.1, confidence), 2), "brain_refs": brain_refs,
            "first_seen": ends_on, "last_seen": ends_on, "status": "open", "unavailable": None}


def _unavailable(rule_id, severity, entity, inputs, connector, fix, ends_on):
    f = _finding(rule_id, severity, entity, [], "This check cannot run yet.", [], ends_on, 0.1, "inputs missing")
    f.update(status="unavailable", unavailable={"inputs": inputs, "connector": connector, "fix": fix})
    return f


def _fresh(comps):
    ages = [c["age_days"] for c in comps if c["age_days"] is not None]
    return max(ages) if ages else None


def rule_angles(m, ends_on):
    out = []
    comps = m["competitors"]
    n = len(comps)
    for a in m["angles"]:
        active = a["brand_active_ads"]
        if not a["held"] or a["competitors_using"] or not active:
            continue
        if a["brand_ads"] / active >= ANGLE_SHARE_MAX:
            continue
        ev = [_row("competitors_using_angle", 0, "n", "latest capture", ends_on, _fresh(comps), 0, "threshold",
                   "ad_library"),
              _row("competitors_tracked", n, "n", "latest capture", ends_on, _fresh(comps), None, "threshold",
                   "ad_library"),
              _row("brand_ads_with_angle", a["brand_ads"], "n", "latest capture", ends_on, _fresh(comps),
                   round(active * ANGLE_SHARE_MAX, 1), "threshold", "ad_library"),
              _row("brand_active_ads", active, "n", "latest capture", ends_on, _fresh(comps), None, "threshold",
                   "ad_library")]
        sentence = (f"None of the {n} tracked brands runs a {a['label']} angle. "
                    f"Bombas runs it in {a['brand_ads']} of {active} active ads.").replace("Bombas", m["brand"].capitalize())
        conf = 0.5 - (0.2 if any(c["expired"] for c in comps) else 0)
        ent = {"type": "offer", "id": f"angle_{a['key']}", "label": f"{a['label']} angle"}
        refs = [a["brain_ref"], f"{m['brand']}.competitors.competitor_set"]
        out.append(_finding("COMP-R01", "medium", ent, ev, sentence, refs, ends_on, conf,
                            "no baseline: an unused angle has no revenue history"))
    return out


def rule_price(m, ends_on):
    ent = {"type": "metric", "id": "price_position_index", "label": "price per pair versus tracked brands"}
    packs = m["packs"]
    if not packs["available"] or m["category_median"] is None:
        inputs = [] if packs["available"] else ["products_monthly"]
        if m["category_median"] is None:
            inputs.append("competitors.price_band_usd")
        return [_unavailable("COMP-R02", "medium", ent, inputs, "Shopify products and a price capture",
                             "Connect the store and log a public price band for each competitor.", ends_on)]
    idx = m["price_position_index"]
    lo, hi = PRICE_BAND
    if lo <= idx <= hi:
        return []
    diff = round(abs(100 - idx))
    side = "below" if idx < lo else "above"
    price, med = packs["median_per_pair"], m["category_median"]
    month_end = (dt.date.fromisoformat(packs["month"] + "-01") + dt.timedelta(days=32)).replace(day=1) - dt.timedelta(days=1)
    ev = [_row("brand_price_per_pair", price, "usd", packs["month"], month_end.isoformat(),
               (dt.date.fromisoformat(ends_on) - month_end).days, None, "threshold", "products_monthly",
               packs["simulated"]),
          _row("competitor_median_price_per_pair", med, "usd", "latest capture", ends_on, _fresh(m["competitors"]),
               None, "peer_band", "competitors.price_band_usd"),
          _row("price_position_index", idx, "index", "latest capture", ends_on, _fresh(m["competitors"]),
               list(PRICE_BAND), "peer_band", "computed")]
    sentence = (f"{m['brand'].capitalize()} sells socks for ${price:.2f} a pair after discounts. "
                f"The tracked brands' median is ${med:.2f}, so the price sits {diff} percent {side} it.")
    refs = [f"{m['brand']}.competitors.competitor_set", f"{m['brand']}.products.price_ladder_socks"]
    return [_finding("COMP-R02", "medium", ent, ev, sentence, refs, ends_on, 0.5 - 0.2,
                     "no baseline: price response is not measured")]


def rule_offer_runs(m, ends_on):
    out = []
    for o in m["offer_runs"]:
        longer = [c for c in o["competitors"] if c["days"] > o["brand_days"]]
        if not longer:
            continue
        top = longer[0]
        ev = [_row("competitor_longest_ad_days", top["days"], "days", "latest capture", ends_on,
                   _fresh(m["competitors"]), o["brand_days"], "threshold", "ad_library"),
              _row("brand_ads_with_offer", o["brand_ads"], "n", "latest capture", ends_on, _fresh(m["competitors"]),
                   None, "threshold", "ad_library"),
              _row("competitors_with_offer", len(o["competitors"]), "n", "latest capture", ends_on,
                   _fresh(m["competitors"]), None, "threshold", "ad_library")]
        name = m["brand"].capitalize()
        if o["brand_ads"]:
            tail = f"{name} has run its {o['label']} in ads for {o['brand_days']} days."
        else:
            tail = f"{name} has a {o['label']} but no active ad runs it."
        sentence = f"{top['name']} runs a {o['label']} hook and its longest ad has been live {top['days']} days. {tail}"
        ent = {"type": "offer", "id": o["key"], "label": o["label"]}
        out.append(_finding("COMP-R03", "medium", ent, ev, sentence, o["brain_refs"] + [top["id"]], ends_on, 0.5,
                            "no baseline: run length is a signal, not a result"))
    return out


def rule_lookalike(m, ends_on):
    lk = m["lookalike"]
    if not lk:
        return []
    age = (dt.date.fromisoformat(ends_on) - dt.date.fromisoformat(lk["captured_at"])).days + 1 \
        if lk["captured_at"] != "undated" else None
    ev = [_row("lookalike_ads_seen", lk["ads_seen"], "n", "latest capture", ends_on, age, 0, "threshold",
               "ad_library")]
    sentence = (f"A lookalike page ran {lk['ads_seen']} gift sale ads linking to {lk['links_to']}. "
                f"It is not {m['brand'].capitalize()}.")
    ent = {"type": "page", "id": str(lk["page_id"]), "label": "lookalike Facebook page"}
    return [_finding("COMP-R04", "medium", ent, ev, sentence, [lk["id"]], ends_on, 0.5,
                     "no baseline: lost orders to the page are not measurable")]


def rule_coverage(m, ends_on):
    cov = m["coverage"]
    out = []
    picks = [g for g in cov["gaps"] if g["proof"] and g["them"] >= covmod.RULE_MIN][:covmod.RULE_TOP]
    for g in picks:
        ev = [_row("their_share_of_ads", g["them"], "%", "latest capture", ends_on, _fresh(m["competitors"]),
                   covmod.RULE_MIN, "threshold", "ad_library", False),
              _row("our_share_of_ads", g["us"] or 0, "%", "latest capture", ends_on, _fresh(m["competitors"]),
                   0, "threshold", "ad_library", False),
              _row("pages_running_it", g["n"], "n", "latest capture", ends_on, _fresh(m["competitors"]), None,
                   "threshold", "ad_library", False)]
        pct = round(g["them"] * 100)
        sentence = (f"{g['n']} tracked pages run {g['angle_label'].lower()} in {g['format']}, about {pct} percent "
                    f"of their ads. {m['brand'].capitalize()} runs none.")
        ent = {"type": "ad", "id": g["gap_id"], "label": f"{g['angle_label']} in {g['format']}"}
        conf = 0.3 if cov["estimated"] else 0.5
        out.append(_finding("COMP-R05", "medium", ent, ev, sentence, [f"{m['brand']}.positioning.proof_points"], ends_on,
                            conf, "no baseline: an untried cell has no spend history"))
    return out


def rule_mix(m, ends_on):
    out = []
    mx = m["mix"]
    fresh = _fresh(m["competitors"])
    name = m["brand"].capitalize()
    for g in mx["gaps"]:
        if g["kind"] == "first_line":
            ev = [_row("pages_using_kind", len(g["pages"]), "n", "latest capture", ends_on, fresh, mixmod.FL_PAGES,
                       "threshold", "ad_library"),
                  _row("their_median_share", g["their_median"], "%", "latest capture", ends_on, fresh, mixmod.FL_SHARE,
                       "threshold", "ad_library"),
                  _row("our_share", g["ours"] or 0, "%", "latest capture", ends_on, fresh, mixmod.FL_OURS, "threshold",
                       "ad_library")]
            sentence = (f"{len(g['pages'])} tracked pages open ads with a {g['label'].lower()}, a median "
                        f"{round(g['their_median'] * 100)} percent of their ads. {name} opens {round((g['ours'] or 0) * 100)} percent that way.")
            ent = {"type": "ad", "id": f"first_line_{g['key']}", "label": f"{g['label'].lower()} first lines"}
            out.append(_finding("COMP-R06", "low", ent, ev, sentence, [f"{m['brand']}.learnings.hook_types"], ends_on, 0.5,
                                "no baseline: a first line kind we never ran has no history"))
        elif g["kind"] == "offer":
            ev = [_row("pages_showing_offer", len(g["pages"]), "n", "latest capture", ends_on, fresh, mixmod.OFFER_PAGES,
                       "threshold", "ad_library"),
                  _row("our_ads_with_offer", 0, "n", "latest capture", ends_on, fresh, None, "threshold", "ad_library")]
            sentence = (f"{len(g['pages'])} tracked pages show {g['label'].lower()} in ads. {name} has {g['held']['text']} "
                        f"and says it in 0 ads.")
            ent = {"type": "offer", "id": f"offer_{g['key']}", "label": g["label"].lower()}
            out.append(_finding("COMP-R07", "medium", ent, ev, sentence, [g["held"]["ref"]], ends_on, 0.5,
                                "no baseline: the offer has never run in ads"))
        elif g["kind"] == "discount":
            ev = [_row("our_ads_with_code_share", g["ours"], "%", "latest capture", ends_on, fresh, mixmod.OUR_PROMO,
                       "threshold", "ad_library"),
                  _row("direct_pages_without_offer", len(g["pages"]), "n", "latest capture", ends_on, fresh,
                       mixmod.NO_OFFER_PAGES, "threshold", "ad_library")]
            sentence = (f"{round(g['ours'] * 100)} percent of {name} ads push a code. {len(g['pages'])} direct competitors "
                        f"show no offer at all.")
            ent = {"type": "offer", "id": "discount_share", "label": "code on most ads"}
            out.append(_finding("COMP-R08", "medium", ent, ev, sentence, [f"{m['brand']}.offers.promo_share_active_ads"],
                                ends_on, 0.5, "no baseline: margin given up to the code is not in the brain"))
    return out


def rule_ladder(m, ends_on):
    lad = m["ladder"]
    out = []
    if not lad or not lad["available"]:
        return out
    fresh = _fresh(m["competitors"])
    month_end = packs_month_end(m["packs"])
    age = (dt.date.fromisoformat(ends_on) - month_end).days if month_end else None
    name = m["brand"].capitalize()
    if lad["shallow"]:
        b = lad["bundle"]
        ev = [_row("median_pack_saving_per_pair", lad["median_saving"], "%", m["packs"]["month"], month_end.isoformat(), age,
                   laddermod.LADDER_MIN, "threshold", "products_monthly", True),
              _row("peer_bundle_saving", b["pct"] / 100, "%", "latest capture", ends_on, fresh, laddermod.BUNDLE_MIN,
                   "threshold", "ad_library")]
        sentence = (f"{name} packs save a median {round(lad['median_saving'] * 100)} percent a pair against a single. "
                    f"{b['page']} advertises {b['pct']} percent off bundles.")
        out.append(_finding("COMP-R09", "medium", {"type": "offer", "id": "pack_ladder", "label": "pack ladder"}, ev, sentence,
                            [f"{m['brand']}.offers.bundles_pack_ladder"], ends_on, 0.5 - 0.2,
                            "no baseline: pack mix response to a deeper ladder is not measured"))
    for l in lad["above_no_proof"]:
        ev = [_row("single_pair_price", l["single"], "usd", m["packs"]["month"], month_end.isoformat(), age,
                   lad["direct_median"], "peer_band", "products_monthly", True)]
        sentence = (f"{l['style'].capitalize()} sells at ${l['single']:.2f} a pair, above the direct median of "
                    f"${lad['direct_median']:.2f}. The brain has no proof for it.")
        out.append(_finding("COMP-R10", "medium", {"type": "sku", "id": f"style_{pagemod.slug(l['style'])}",
                                                   "label": f"{l['style']} single pair"}, ev, sentence,
                            [f"{m['brand']}.positioning.proof_points"], ends_on, 0.3,
                            "no baseline: conversion at this price is not split by proof"))
    return out


AXIS_MAX = {"durability": DURABILITY_MAX, "comfort": COMFORT_MAX}


def open_corners(m) -> list[dict]:
    placed = [c for c in m["competitors"] if c["price"]["median"] is not None]
    split = m["category_median"]
    if split is None or len(placed) < 3:
        return []
    out = []
    for axis, mx in AXIS_MAX.items():
        for hi_x in (False, True):
            names = [c["name"] for c in placed if (c["price"]["median"] >= split) == hi_x and c[axis] >= mx / 2]
            if not names:
                out.append({"axis": axis, "hi_x": hi_x, "label": f"{'higher' if hi_x else 'lower'} price, strong {axis} claim",
                            "placed": len(placed), "split": split})
    return out


def rule_corners(m, ends_on):
    out = []
    for c in open_corners(m):
        ev = [_row("brands_in_corner", 0, "n", "latest capture", ends_on, _fresh(m["competitors"]), 0, "threshold", "competitors"),
              _row("brands_placed", c["placed"], "n", "latest capture", ends_on, _fresh(m["competitors"]), 3, "threshold",
                   "competitors"),
              _row("price_split", c["split"], "usd", "latest capture", ends_on, _fresh(m["competitors"]), None, "peer_band",
                   "competitors.price_band_usd")]
        sentence = f"No tracked brand claims the {c['label']} corner. {c['placed']} brands are placed on the map."
        ent = {"type": "brand", "id": f"corner_{c['axis']}_{'high' if c['hi_x'] else 'low'}", "label": c["label"]}
        out.append(_finding("COMP-R11", "medium", ent, ev, sentence, [f"{m['brand']}.positioning.frame"], ends_on, 0.3,
                            "no baseline: demand for the corner is not measured yet"))
    return out


def rule_refresh(m, ends_on):
    out = []
    for e in (m.get("changes") or {}).get("events", []):
        if e["kind"] != "refresh" or not e.get("direct"):
            continue
        p = next(p for p in m["pages"] if p["name"] == e["page"])
        ev = [_row("oldest_active_ad_days", p["longest_days"], "days", "latest capture", ends_on, _fresh(m["competitors"]),
                   changemod.REFRESH_DAYS, "threshold", "ad_library"),
              _row("active_ads", p["active_ads"], "n", "latest capture", ends_on, _fresh(m["competitors"]), None, "threshold",
                   "ad_library")]
        sentence = (f"{p['name']} replaced every ad: the oldest of its {p['active_ads']} active ads is "
                    f"{p['longest_days']} days old.")
        ent = {"type": "page", "id": f"refresh_{p['key']}", "label": f"{p['name']} new flight"}
        out.append(_finding("COMP-R12", "low", ent, ev, sentence, p["record_ids"], ends_on, 0.5,
                            "no baseline: a competitor's flight has no cost to us until it takes share"))
    return out


def rule_freshness(m, ends_on):
    out = []
    for p in m["pages"]:
        if p["role"] != "self" and not p["page_id"]:
            ev = [_row("page_id_known", 0, "n", "latest capture", ends_on, None, 1, "threshold", "config")]
            ent = {"type": "page", "id": f"no_id_{p['key']}", "label": f"{p['name']} page id"}
            out.append(_finding("COMP-R13", "low", ent, ev, f"{p['name']} is tracked but has no page id, so it is never pulled.",
                                [f"{m['brand']}.positioning.competitive_frame"], ends_on, 0.5, "no baseline: nothing captured"))
    age = _fresh(m["competitors"])
    if age is not None and age > STALE_DAYS:
        ev = [_row("oldest_capture_days", age, "days", "latest capture", ends_on, age, STALE_DAYS, "threshold", "ad_library")]
        out.append(_finding("COMP-R14", "medium", {"type": "brand", "id": "stale_capture", "label": "competitor capture"}, ev,
                            f"The oldest competitor capture is {age} days old, past the {STALE_DAYS} day rule.",
                            [f"{m['brand']}.competitors.competitor_set"], ends_on, 0.5, "no baseline: freshness has no money formula"))
    return out


def packs_month_end(packs):
    if not packs.get("available"):
        return None
    return (dt.date.fromisoformat(packs["month"] + "-01") + dt.timedelta(days=32)).replace(day=1) - dt.timedelta(days=1)


def _today(window) -> dt.date:
    if window and window.get("ends_on"):
        return dt.date.fromisoformat(str(window["ends_on"])) + dt.timedelta(days=1)
    return dt.date.today()


def run(brand: str, window: dict | None = None, root: Path | None = None) -> list[dict]:
    today = _today(window)
    ends_on = (today - dt.timedelta(days=1)).isoformat()
    m = market_full(brand, today, root)
    if not m["competitors"]:
        ent = {"type": "brand", "id": "competitor_set", "label": "competitor set"}
        out = [_unavailable(rid, "medium", ent, ["brain competitors"], "Meta Ad Library (read only)",
                            "Run the Ad Library extractor for the brand's competitor set.", ends_on)
               for rid in ("COMP-R01", "COMP-R03")]
    else:
        out = rule_angles(m, ends_on) + rule_offer_runs(m, ends_on) + rule_coverage(m, ends_on) + rule_mix(m, ends_on)
        out += rule_ladder(m, ends_on) + rule_corners(m, ends_on) + rule_refresh(m, ends_on) + rule_freshness(m, ends_on)
    out += rule_price(m, ends_on) + rule_lookalike(m, ends_on)
    out.sort(key=lambda f: (SEVERITY_ORDER[f["severity"]], f["id"]))
    return out


if __name__ == "__main__":
    b = sys.argv[1] if len(sys.argv) > 1 else "bombas"
    print(json.dumps(run(b, {"ends_on": "2026-09-27", "days": 1, "trailing": 0}), indent=1))
