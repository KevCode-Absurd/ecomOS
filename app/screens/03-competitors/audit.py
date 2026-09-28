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
COMP-R15 lost by name. A named alternative recommended instead of us on Reddit
    MIN_TIMES (2) or more times (losses.py), with the reason a rule reads from
    their ad angles. Severity medium. Capability BRAND-C57 (the compare block and
    support macro). Reputation 4: the reason sits on a review theme. Owner:
    03-competitors.
COMP-R16 a lower rung is gaining. Interest in a lower rung of the category
    ladder (category.py: doing nothing, cheap multipacks) rising faster than
    interest in the category. Needs a search trends source, so it reads
    unavailable and becomes a connect action (person). Capability BRAND-C18.
    Owner: 03-competitors.
COMP-R17 they attack where we are weak. One of our 2 review themes with the most
    one-star reviews (reviews.py) is led with by ATTACK_PAGES (2) or more direct pages.
    Severity high: a deal-breaker theme under a competitor's lead claim.
    Capability LIFE-C42 (guarantee and risk reversal, founder gate).
    Reputation 4, satisfaction 4. Owner: 03-competitors.
COMP-R18 Amazon undercuts our site. A style with 2 or more Amazon listings whose
    median price per pair is 15 percent or more below our site's net price per
    pair (market_presence.py). Severity medium. Capability PROD-C46 (agent
    checks sellers and prices). Confidence 0.3: site prices are simulated.
    Owner: 03-competitors.
COMP-R19 we ship new ads slower. Our estimated launch rate (velocity.py: active
    ads / median days live x 7) is under half the direct pages' median. Severity
    medium. Capability CREA-C06 (a weekly creative volume plan). Confidence 0.3:
    both sides are estimates. Owner: 03-competitors.
COMP-R20 a niche to size. The biggest candidate niche (niche.py: an angle with 5
    percent or more of their ads where our share is under a third of theirs),
    with the bar in buyers from our own economics. Severity low. Capability
    BRAND-C23 (agent writes the sizing note). Owner: 03-competitors.
COMP-R21 discounting undercuts a premium position. Our premium signal score
    (premium.py) is at or above the direct median while our discount runs 10
    points or more deeper than theirs. Severity medium. Capability LIFE-C38
    (discount policy, founder gate). Reputation 3. Owner: 03-competitors.
COMP-R22 search terms they go after that we never say. 3 or more seed terms
    (search.py) from the tracked pages' public lines that our own lines never
    say. Severity low. Capability BRAND-C07 (the agent writes a keyword
    check brief for the Google Ads and SEO screens). Owner: 03-competitors.
COMP-R23 search overlap unknown. Rankings, bids and volumes need a keyword
    source, so the overlap reads unavailable: a connect action. Capability
    BRAND-C07. Owner: 03-competitors.
COMP-R24 a direct competitor started a new offer or angle. Between the latest
    two page-summary captures (capture.py), a direct page shows an offer or an
    angle it did not show before. Severity medium. Capability CREA-C06 (brief
    our counter). Owner: 03-competitors.
COMP-R25 a competitor cut its price sharply. A tracked page's median price per
    pair fell 15 percent or more between the latest two captures (capture.py),
    the room's price-cut rule. Severity high for a direct page, medium else.
    Capability CREA-C31 (answer with value framing, never a reflex match).
    Owner: 03-competitors.
COMP-R26 a top threat's landing pages are not tracked. One finding for the top
    3 threat pages (landing.py) with no landing page capture. Severity low.
    Capability BRN-C01 (site crawl, snapshot and diff; agent does it, public
    read). Owner: 03-competitors.
COMP-R27 battlecard facts are stale. A direct page's record behind its battlecard
    was last checked more than 90 days ago. Severity low. Capability BRAND-C57
    (agent re-verifies and refreshes the card). Owner: 03-competitors.
COMP-R28 the positioning line was never tested against shopper frames. The top
    Reddit category frame (frames.py) is not in our frame's words and no
    positioning test is on file. Severity medium. Capability BRAND-C20.
    Reputation 3. Owner: 03-competitors.
COMP-R29 no win-loss research against the names we lose to. Alternatives are
    recommended instead of us (losses.py) and no win-loss interviews are on file.
    Severity low. Capability BRAND-C58 (human assist: a person runs the
    interviews; the agent writes the kit and codes the answers). Owner:
    03-competitors.
COMP-R30 the season is close and we run no gifting ad. Black Friday within 60
    days (season.py), 2 or more direct pages run a gifting or season angle, and
    none of our ads does. Severity high inside 60 days. Capability CREA-C06.
    Owner: 03-competitors.

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
capmod = _local("capture")
landmod = _local("landing")
framemod = _local("frames")
handmod = _local("handoff")
seasonmod = _local("season")
lossmod = _local("losses")
catmod = _local("category")
revmod = _local("reviews")
mktmod = _local("market_presence")
velmod = _local("velocity")
nichemod = _local("niche")
premmod = _local("premium")
searchmod = _local("search")
inpmod = _local("inputs")

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
    {"rule_id": "COMP-R15", "name": "lost by name: recommended instead of us", "entity_type": "brand",
     "inputs": ["brain competitors recommended_instead", "brain objection_ladders", "tracked page angles"],
     "capability": "BRAND-C57", "owner_screen": SCREEN},
    {"rule_id": "COMP-R16", "name": "a lower rung of the ladder is gaining", "entity_type": "ladder_rung",
     "inputs": ["search trends by rung"], "capability": "BRAND-C18", "owner_screen": SCREEN},
    {"rule_id": "COMP-R17", "name": "they lead with the theme we get the most one-star reviews on", "entity_type": "ladder_rung",
     "inputs": ["brain objection_ladders", "tracked page angles and offers"], "capability": "LIFE-C42", "owner_screen": SCREEN},
    {"rule_id": "COMP-R18", "name": "Amazon price per pair undercuts our site", "entity_type": "sku",
     "inputs": ["brain marketplaces", "products_monthly"], "capability": "PROD-C46", "owner_screen": SCREEN},
    {"rule_id": "COMP-R19", "name": "we ship new ads far slower than direct pages", "entity_type": "brand",
     "inputs": ["brain learnings adlib formats (median days live)", "active ads"], "capability": "CREA-C06", "owner_screen": SCREEN},
    {"rule_id": "COMP-R20", "name": "a niche they serve that we barely do, to size against our bar", "entity_type": "brand",
     "inputs": ["coverage matrix", "brain economics", "calibration revenue"], "capability": "BRAND-C23", "owner_screen": SCREEN},
    {"rule_id": "COMP-R21", "name": "discount deeper than the category while showing premium signals", "entity_type": "offer",
     "inputs": ["brain competitors offers and hooks", "brain offers", "brain positioning.proof_points"], "capability": "LIFE-C38",
     "owner_screen": SCREEN},
    {"rule_id": "COMP-R22", "name": "search terms they go after that we never say", "entity_type": "brand",
     "inputs": ["brain competitors positioning, push, hook_types", "brain products.materials"], "capability": "BRAND-C07",
     "owner_screen": SCREEN},
    {"rule_id": "COMP-R23", "name": "search overlap: rankings and bids", "entity_type": "brand",
     "inputs": ["keyword rankings and bids"], "capability": "BRAND-C07", "owner_screen": SCREEN},
    {"rule_id": "COMP-R24", "name": "a direct competitor started a new offer or angle", "entity_type": "page",
     "inputs": ["page-summary captures", "Ad Library snapshot"], "capability": "CREA-C06", "owner_screen": SCREEN},
    {"rule_id": "COMP-R25", "name": "a competitor cut its price per pair 15 percent or more", "entity_type": "page",
     "inputs": ["page-summary captures (price band)"], "capability": "CREA-C31", "owner_screen": SCREEN},
    {"rule_id": "COMP-R26", "name": "top threats' landing pages not tracked", "entity_type": "page",
     "inputs": ["threat verdicts", "brain competitors price_ref"], "capability": "BRN-C01", "owner_screen": SCREEN},
    {"rule_id": "COMP-R27", "name": "battlecard facts past 90 days", "entity_type": "page",
     "inputs": ["brain competitors captured_at"], "capability": "BRAND-C57", "owner_screen": SCREEN},
    {"rule_id": "COMP-R28", "name": "positioning line not tested against the top shopper frame", "entity_type": "brand",
     "inputs": ["brain positioning.reddit_frames", "brain positioning.frame", "brain learnings"], "capability": "BRAND-C20",
     "owner_screen": SCREEN},
    {"rule_id": "COMP-R29", "name": "no win-loss interviews against the names we lose to", "entity_type": "brand",
     "inputs": ["brain competitors recommended_instead", "win-loss interviews"], "capability": "BRAND-C58", "owner_screen": SCREEN},
    {"rule_id": "COMP-R30", "name": "holiday season close and no gifting ad", "entity_type": "brand",
     "inputs": ["calendar (US holidays)", "tracked page angles", "brain offers.gifting"], "capability": "CREA-C06", "owner_screen": SCREEN},
    {"rule_id": "COMP-R31", "name": "the same loss reason repeats against one named competitor", "entity_type": "brand",
     "inputs": ["win-loss interviews logged on this screen"], "capability": "BRAND-C58", "owner_screen": SCREEN},
    {"rule_id": "COMP-R32", "name": "a positioning line won its poll", "entity_type": "brand",
     "inputs": ["positioning polls logged on this screen"], "capability": "BRAND-C20", "owner_screen": SCREEN},
    {"rule_id": "COMP-R33", "name": "a logged price sits outside the page's public price band", "entity_type": "page",
     "inputs": ["prices seen logged on this screen", "brain competitors price_ref"], "capability": "BRAND-C24", "owner_screen": SCREEN},
    {"rule_id": "COMP-R34", "name": "logged rival prices due a re-check", "entity_type": "brand",
     "inputs": ["prices seen logged on this screen"], "capability": "BRN-C11", "owner_screen": SCREEN},
    {"rule_id": "COMP-R35", "name": "rival site traffic by channel (visits, share by source)", "entity_type": "brand",
     "inputs": ["a site traffic estimate source"], "capability": "BRAND-C07", "owner_screen": SCREEN},
    {"rule_id": "COMP-R36", "name": "a direct page launched a burst of new ads between 2 ad-level snapshots", "entity_type": "page",
     "inputs": ["2 ad-level snapshots"], "capability": "BRN-C11", "owner_screen": SCREEN},
    {"rule_id": "COMP-R08", "name": "discount on most ads while direct peers run none", "entity_type": "offer",
     "inputs": ["brain offers.promo_share_active_ads", "brain competitors offers_seen"], "capability": "LIFE-C38",
     "owner_screen": SCREEN},
]
# what a strategist groups the findings by on the page (depth.md section 2: grouped by bottleneck)
RULE_GROUP = {"COMP-R01": "creative", "COMP-R05": "creative", "COMP-R06": "creative", "COMP-R03": "offer", "COMP-R07": "offer",
              "COMP-R08": "offer", "COMP-R09": "offer", "COMP-R02": "price", "COMP-R10": "price", "COMP-R11": "position",
              "COMP-R04": "watch", "COMP-R12": "watch", "COMP-R13": "watch", "COMP-R14": "watch", "COMP-R15": "lost", "COMP-R16": "lost", "COMP-R17": "lost", "COMP-R18": "price", "COMP-R19": "creative", "COMP-R20": "position", "COMP-R21": "offer", "COMP-R22": "position", "COMP-R23": "position", "COMP-R24": "watch", "COMP-R25": "price", "COMP-R26": "watch", "COMP-R27": "watch", "COMP-R28": "position", "COMP-R29": "lost", "COMP-R30": "creative", "COMP-R31": "lost", "COMP-R32": "position", "COMP-R33": "price", "COMP-R34": "watch", "COMP-R35": "watch", "COMP-R36": "watch"}
GROUP_LABEL = {"lost": "Shoppers we lose, by name", "creative": "Ads they run that we do not", "offer": "Offers they say that we do not",
               "price": "Price against theirs", "position": "Corners of the map", "watch": "Watch and protect"}
RUBRIC_OVERRIDES = {"COMP-R01": {"reputation": 5}, "COMP-R02": {"reputation": 3}, "COMP-R04": {"reputation": 5, "satisfaction": 4},
                    "COMP-R15": {"reputation": 4}, "COMP-R17": {"reputation": 4, "satisfaction": 4},
                    "COMP-R21": {"reputation": 3}, "COMP-R28": {"reputation": 3}}
AUTONOMY = {"BRAND-C58": "human_assist", "BRN-C01": "agent_does", "BRAND-C07": "agent_does", "BRAND-C23": "agent_does", "PROD-C46": "agent_does", "LIFE-C42": "founder_gate", "BRAND-C18": "agent_does", "BRAND-C57": "agent_does", "BRN-C11": "agent_does", "BRAND-C20": "agent_does", "LIFE-C39": "founder_gate", "CREA-C31": "agent_does", "CREA-C06": "agent_does", "CREA-C04": "agent_does", "LIFE-C47": "agent_does", "LIFE-C38": "founder_gate", "BRAND-C21": "founder_gate", "BRAND-C24": "founder_gate", "MONEY-C48": "human_assist"}


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


def category_term(brain: Brain) -> dict:
    """The category word for this brand, from the brain, never typed: the pull config's category_term, else the
    first product line, else "products". Screens say "socks" for a sock brand and "hats" for a hat brand."""
    term = None
    try:
        cfg = json.loads((brain.dir / "config" / "apify.json").read_text(encoding="utf-8"))
        term = (cfg.get("reddit") or {}).get("category_term")
    except (OSError, ValueError):
        term = None
    if not term:
        lines = _value(brain, "products.lines")
        term = str(lines[0]).lower() if isinstance(lines, list) and lines else "products"
    plural = term.lower().strip()
    # the price unit is read from the competitors' public price bands ("12 to 25 per pair"), never typed
    units = [u for r in brain.records("competitors") if isinstance(r.get("value"), dict)
             for u in re.findall(r"per (\w+)", str(r["value"].get("price_band_usd") or "").lower()) if u != "product"]
    unit = max(set(units), key=lambda u: (units.count(u), u)) if units else "unit"
    return {"plural": plural, "singular": plural[:-1] if plural.endswith("s") else plural, "unit": unit}


def brand_packs(brand: str, category: str = "socks") -> dict:
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
        if r.get("month") != month or r.get("category") != category or not r.get("units"):
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
        return {"available": False, "reason": f"no {category} rows in products_monthly for {month}", "packs": []}
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

# Thresholds a brand can tune (depth.md section 8): a `plans` record with field competitor_thresholds whose
# value is {name: number}. Unknown names are ignored. Defaults are the constants in each module.
_self = sys.modules[__name__]
TUNABLE = {"price_band_low": (_self, "PRICE_BAND", 0), "price_band_high": (_self, "PRICE_BAND", 1),
           "stale_days": (_self, "STALE_DAYS", None), "angle_share_max": (_self, "ANGLE_SHARE_MAX", None),
           "threat_points": (pagemod, "THREAT_AT", None), "watch_points": (pagemod, "WATCH_AT", None),
           "coverage_gap_min": (covmod, "GAP_MIN", None), "surge": (capmod, "SURGE", None), "price_move": (capmod, "PRICE_MOVE", None),
           "discount_deeper_points": (premmod, "DEEPER", None), "ladder_min_saving": (laddermod, "LADDER_MIN", None),
           "undercut": (mktmod, "UNDERCUT", None)}


# the range a threshold may be tuned to on the page (inputs.py kind threshold); outside it the change is refused
BURST_ADS = 10   # new ads on one direct page between 2 ad-level snapshots that make a burst (COMP-R36)
CORNER_FRAME = {"durability": "buy_it_for_life", "comfort": None}   # the shopper frame that asks for a strong claim on each axis
PRICE_STREAK = 2   # captures in a row outside the price band before the drift is confirmed (the room's rule)
TUNE_RANGE = {"price_band_low": (50, 100), "price_band_high": (100, 200), "stale_days": (3, 90), "angle_share_max": (0.05, 0.6),
              "threat_points": (2, 6), "watch_points": (1, 5), "coverage_gap_min": (0.01, 0.2), "surge": (0.1, 1.0),
              "price_move": (0.05, 0.5), "discount_deeper_points": (1, 40), "ladder_min_saving": (0.02, 0.4), "undercut": (0.05, 0.5)}


def apply_thresholds(brain: Brain) -> dict:
    """Reset every tunable to its default, apply the brand's competitor_thresholds record, then the latest change made on
    this screen for each name (newest wins). Returns what is in force and where each value came from."""
    rec = next((r for r in brain.records("plans") if r.get("field") == "competitor_thresholds" and isinstance(r.get("value"), dict)), None)
    over = dict(rec["value"]) if rec else {}
    screen = inpmod.thresholds(inpmod.read(brain.brand, "threshold"))
    over.update({k: v["value"] for k, v in screen.items()})
    out = {}
    for name, (mod, attr, idx) in TUNABLE.items():
        if not hasattr(mod, "_default_" + attr):   # the default lives on the module, so every loaded copy shares it
            setattr(mod, "_default_" + attr, getattr(mod, attr))
        default = getattr(mod, "_default_" + attr)
        cur = list(getattr(mod, attr)) if idx is not None else getattr(mod, attr)
        base = default[idx] if idx is not None else default
        val = over.get(name, base) if isinstance(over.get(name, base), (int, float)) else base
        if idx is not None:
            cur[idx] = val
            setattr(mod, attr, tuple(cur))
        else:
            setattr(mod, attr, val)
        src = "screen" if name in screen else "brain" if name in over and val == over[name] else "default"
        out[name] = {"value": val, "default": base, "source": src, "range": TUNE_RANGE.get(name),
                     "changed_on": screen[name]["date"] if name in screen else None}
    return {"values": out, "record": rec["id"] if rec else None}


def market(brand: str, today: dt.date, root: Path | None = None) -> dict:
    brain = Brain(brand, root, today)
    thresholds = apply_thresholds(brain)
    comps = competitors(brain)
    prof = brand_profile(brain)
    term = category_term(brain)
    packs = brand_packs(brand, term["plural"])
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
                       "brand_ads": brand_ads_with(brain, prof, a["keys"]) if prof["active_ads"] is not None else None,
                       "brand_active_ads": prof["active_ads"]})
    for c in comps:
        c["gap_to_own"] = [a["label"] for a in angles if a["held"] and c["name"] not in a["competitors_using"]]

    snapshot = snap.load(brand)
    pages = pagemod.build(brain, _value(brain, "positioning.competitive_frame"), snap, snapshot, prof)
    us = next(p for p in pages if p["role"] == "self")
    top = pagemod.our_top_angles(us)
    for p in pages:
        if p["role"] != "self":
            p["verdict"] = pagemod.verdict(p, us, top)
    # the brand-held angles (R01) are checked against every tracked page with data, not only the detailed records
    live = [p for p in pages if p["role"] != "self" and p["source"] != "none"]
    for a in angles:
        spec = next(x for x in ANGLES if x["key"] == a["key"])
        a["competitors_using"] = [p["name"] for p in live if _hits(" ".join(
            [str(x or "") for x in p["hook_labels"] + p["quotes"] + [p["positioning"], p["push"]]]), spec["keys"])]
        a["pages_checked"] = len(live)
    cov = covmod.matrix(pages, snap.ANGLES, snapshot, brain)
    points = covmod.proof_points(brain)
    refs = refmod.build(pages, top, snap.FORMAT_LABEL, lambda a: covmod.proof_for(points, a))
    return {"brand": brand, "brain": brain, "competitors": comps, "profile": prof, "packs": packs,
            "references": refs, "ladder": None, "thresholds": thresholds, "term": term, "mix": mixmod.build(pages, brain, snap),
            "coverage": cov,
            "coverage_direct": covmod.matrix(pages, snap.ANGLES, snapshot, brain, direct_only=True),
            "pages": pages, "snapshot": {k: v for k, v in (snapshot or {}).items() if k != "ads"} or None,
            "our_top_angles": top,
            "category_median": cat_median, "price_position_index": index, "angles": angles,
            "offer_runs": offer_runs(brain, comps, prof), "lookalike": lookalike(brain),
            "competitor_set": _value(brain, "competitors.competitor_set") or []}


def price_streak(brand: str, today: dt.date, idx) -> int:
    """How many captures in a row, newest first and today's index as the latest, sit outside the price band.
    A capture without our index breaks the run: unknown is never counted as outside."""
    series = []
    for pth in capmod.captures(brand):
        c = json.loads(pth.read_text(encoding="utf-8"))
        if c.get("captured_at", "") < today.isoformat():
            series.append((c.get("ours") or {}).get("price_position_index"))
    series.append(idx)
    n = 0
    for v in reversed(series):
        if v is None or PRICE_BAND[0] <= v <= PRICE_BAND[1]:
            break
        n += 1
    return n


def market_full(brand: str, today: dt.date, root: Path | None = None) -> dict:
    m = market(brand, today, root)
    checks = inpmod.card_checks(inpmod.read(brand, "card_check"))
    for p in m["pages"]:   # a battlecard's freshness counts from the latest person check, else from the capture
        c = checks.get(p["name"])
        p["card_checked_on"] = c["date"] if c else None
        p["card_age_days"] = (today - dt.date.fromisoformat(c["date"])).days if c else p.get("age_days")
    m["price_streak"] = price_streak(brand, today, m["price_position_index"])
    m["ladder"] = laddermod.build(m, m["brain"])
    cur = snap.load(brand)
    prev = snap.load(brand, before=cur["captured_at"]) if cur else None
    cprev, ccur = capmod.latest_two(brand)
    m["changes"] = changemod.build(m, m["brain"], prev, cur, today, capmod.diff(cprev, ccur), len(capmod.captures(brand)))
    ch, frame = m["changes"], {p["name"]: p["frame"] for p in m["pages"]}
    site = [r for r in inpmod.read(brand, "site_change") if r["date"] >= ch["window_start"]]
    for r in site:   # changes seen on their sites by a person join the timeline; a visit with no change does not
        if r["what"] == "no_change":
            continue
        direct = frame.get(r["page"]) == "direct"
        v = (("follow", "Follow", "Answer it: brief our counter this week.") if direct and r["what"] in inpmod.SITE_FOLLOW else
             ("watch", "Watch", "Look at it on the next visit; brief an answer if it overlaps our angles.") if direct else
             ("ignore", "Ignore", "No overlap with our frame."))
        ch["events"].append({"when": r["date"], "page": r["page"], "kind": "site_" + r["what"], "value": r["what"],
                             "text": inpmod.SITE_CHANGES[r["what"]] + " (seen on their site)", "url": r.get("url"),
                             "verdict": v[0], "verdict_text": v[1], "action": v[2], "source": "logged", "direct": direct})
        ch["counts"][v[0]] = ch["counts"].get(v[0], 0) + 1
    ch["events"].sort(key=lambda e: (e["when"] or "", e["page"]), reverse=True)
    ch["launches"] = sum(1 for r in site if r["what"] in inpmod.SITE_LAUNCH)
    ch["site_logged"] = len(site)
    ch["site_kinds"] = list(inpmod.SITE_CHANGES)
    m["landing"] = landmod.build(m, cur)
    visits = {}
    for r in inpmod.read(brand, "site_change"):
        visits[r["page"]] = max(visits.get(r["page"], ""), r["date"])
    for row in m["landing"]["rows"]:   # a person's weekly visit counts as tracking until a crawl exists
        v = visits.get(row["name"])
        row["visited_on"] = v
        if v and (today - dt.date.fromisoformat(v)).days <= inpmod.VISIT_DAYS:
            row["tracked"] = True
    m["frame_tests"] = inpmod.read(brand, "frame_test")
    m["frames"] = framemod.build(m, m["brain"])
    m["season"] = seasonmod.build(m, m["brain"], today)
    logged = inpmod.price_moves(inpmod.read(brand, "price_seen"), capmod.PRICE_MOVE,
                                {p["name"]: p["frame"] for p in m["pages"] if p["role"] != "self"})
    m["price_moves"] = {"moves": capmod.price_moves(cprev, ccur, parse_band) + logged["moves"], "captures": len(capmod.captures(brand)),
                        "since": cprev["captured_at"] if cprev else None, "threshold": capmod.PRICE_MOVE,
                        "logged": logged, "trail_days": inpmod.TRAIL_DAYS, "recheck_days": inpmod.RECHECK_DAYS,
                        "recheck": inpmod.recheck(inpmod.read(brand, "price_seen"), today),
                        "pages": [p["name"] for p in m["pages"] if p["role"] != "self" and p["source"] != "none"],
                        "recent": sorted(inpmod.read(brand, "price_seen"), key=lambda r: (r["date"], r["id"]))[-8:][::-1]}
    seen = {}
    for r in sorted(inpmod.read(brand, "price_seen"), key=lambda r: (r["date"], r["id"])):
        seen[(r["page"], r["product"].lower())] = r   # the latest record per page and product
    for b in m["ladder"]["bands"]:
        b["seen"] = []
        for (pg, _), r in sorted(seen.items()):
            if pg != b["name"]:
                continue
            v = r["per_unit"]
            inside = (b["low"] <= v <= b["high"]) if b["low"] is not None and b["high"] is not None else (v >= b["low"]) if b["low"] is not None else None
            b["seen"].append({"product": r["product"], "per_unit": v, "date": r["date"], "in_band": inside, "url": r.get("url")})
        b["out_of_band"] = [x for x in b["seen"] if x["in_band"] is False]
    m["losses"] = lossmod.build(m, m["brain"], inpmod.read(brand, "interview"), inpmod.win_loss)
    m["category"] = catmod.build(m, m["brain"])
    m["velocity"] = velmod.build(m, m["brain"])
    m["niche"] = nichemod.build(m, m["brain"])
    m["search"] = searchmod.build(m, m["brain"])
    m["premium"] = premmod.build(m, m["brain"], lambda texts: mixmod.offer_types(texts, snap.OFFERS))
    m["presence"] = mktmod.build(m, m["brain"], laddermod.pairs_in_title)
    m["reviews"] = revmod.build(m, m["brain"], lambda texts: mixmod.offer_types(texts, snap.OFFERS))
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
        n = a.get("pages_checked", len(comps))
        ev = [_row("competitors_using_angle", 0, "n", "latest capture", ends_on, _fresh(comps), 0, "threshold",
                   "ad_library"),
              _row("competitors_tracked", n, "n", "latest capture", ends_on, _fresh(comps), None, "threshold",
                   "ad_library"),
              _row("brand_ads_with_angle", a["brand_ads"], "n", "latest capture", ends_on, _fresh(comps),
                   round(active * ANGLE_SHARE_MAX, 1), "threshold", "ad_library"),
              _row("brand_active_ads", active, "n", "latest capture", ends_on, _fresh(comps), None, "threshold",
                   "ad_library")]
        sentence = (f"None of the {n} tracked pages runs a {a['label']} angle. "
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
    streak = m.get("price_streak") or 1
    ev.append(_row("captures_outside_band", streak, "n", "dated captures", ends_on, None, PRICE_STREAK, "threshold", "captures"))
    if streak >= PRICE_STREAK:   # the room's rule: outside the range for 2 consecutive captures
        sentence = (f"The brand's price is now {diff} percent {side} the category range, for {streak} captures in a row: "
                    f"${price:.2f} a {m['term']['unit']} against a tracked median of ${med:.2f}.")
    else:
        sentence = (f"{m['brand'].capitalize()} sells {m['term']['plural']} for ${price:.2f} a {m['term']['unit']} after discounts. "
                    f"The tracked brands' median is ${med:.2f}, so the price sits {diff} percent {side} it. "
                    "One capture so far; a second outside the range confirms it.")
    refs = [f"{m['brand']}.competitors.competitor_set", f"{m['brand']}.products.price_ladder_{m['term']['plural']}"]
    return [_finding("COMP-R02", "high" if streak >= PRICE_STREAK else "medium", ent, ev, sentence, refs, ends_on,
                     0.5 if streak >= PRICE_STREAK else 0.3, "no baseline: price response is not measured")]


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
        sentence = (f"{name} packs save a median {round(lad['median_saving'] * 100)} percent a {m['term']['unit']} against a single. "
                    f"{b['page']} advertises {b['pct']} percent off bundles.")
        out.append(_finding("COMP-R09", "medium", {"type": "offer", "id": "pack_ladder", "label": "pack ladder"}, ev, sentence,
                            [f"{m['brand']}.offers.bundles_pack_ladder"], ends_on, 0.5 - 0.2,
                            "no baseline: pack mix response to a deeper ladder is not measured"))
    for l in lad["above_no_proof"]:
        ev = [_row("single_pair_price", l["single"], "usd", m["packs"]["month"], month_end.isoformat(), age,
                   lad["direct_median"], "peer_band", "products_monthly", True)]
        sentence = (f"{l['style'].capitalize()} sells at ${l['single']:.2f} a {m['term']['unit']}, above the direct median of "
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
        frame = CORNER_FRAME.get(c["axis"])
        frames = _value(m["brain"], "positioning.reddit_frames") or {}
        demand = frames.get(frame) if frame and isinstance(frames, dict) else None
        ev.append(_row("shopper_frame_mentions", demand, "n", "reddit capture", ends_on, None, 1, "threshold", "reddit"))
        if demand:   # the room's "open quadrant with real demand"; search demand waits on a keyword source, Reddit frames stand in
            sentence = (f"No tracked brand claims the {c['label']} corner, and shoppers ask for it: {demand} Reddit mentions "
                        f"of {frame.replace('_', ' ')}.")
        else:
            sentence = f"No tracked brand claims the {c['label']} corner. {c['placed']} brands are placed on the map."
        ent = {"type": "brand", "id": f"corner_{c['axis']}_{'high' if c['hi_x'] else 'low'}", "label": c["label"]}
        out.append(_finding("COMP-R11", "high" if demand else "medium", ent, ev, sentence,
                            [f"{m['brand']}.positioning.frame"] + ([f"{m['brand']}.positioning.reddit_frames"] if demand else []), ends_on,
                            0.5 if demand else 0.3, "no baseline: search demand for the corner is not measured yet"))
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


def rule_losses(m, ends_on):
    out = []
    for x in (m.get("losses") or {}).get("rows", []):
        if not x["fires"]:
            continue
        ev = [_row("recommended_instead", x["times"], "n", "latest capture", ends_on, None, lossmod.MIN_TIMES, "threshold", "reddit")]
        if x.get("theme_source") == "interviews":
            ev.append(_row("logged_losses_to_name", x["win_loss"]["losses"], "n", "interviews logged", ends_on, None,
                           lossmod.INTERVIEW_THEME_MIN, "threshold", "team"))
        ev.append(_row("upvotes", x["upvotes"], "n", "latest capture", ends_on, None, None, "threshold", "reddit"))
        if x["our_one_star"] is not None:
            ev.append(_row("our_one_star_on_theme", x["our_one_star"], "n", "reviews on file", ends_on, None, None, "threshold",
                           "objection_ladders"))
        sentence = (f"Reddit recommends {x['name']} instead of us {x['times']} times. "
                    + (f"Our interviews say why: they {x['theme_label']} ({x['why']})." if x.get("theme_source") == "interviews"
                       else f"The rule reads why: they {x['theme_label']}."))
        ent = {"type": "brand", "id": f"lost_{x['key']}", "label": f"lost to {x['name']}"}
        refs = [x["record"]] + ([x["ladder"]] if x["ladder"] else [])
        out.append(_finding("COMP-R15", "medium", ent, ev, sentence, refs, ends_on, 0.6 if x.get("theme_source") == "interviews" else 0.3,
                            "no baseline: lost orders to a named brand are not measured"))
    return out


def rule_attack(m, ends_on):
    a = (m.get("reviews") or {}).get("attack")
    if not a:
        return []
    ev = [_row("our_one_star_on_theme", a["one_star"], "n", "reviews on file", ends_on, None, None, "threshold", "objection_ladders"),
          _row("direct_pages_leading_with_it", a["direct_leaders"], "n", "latest capture", ends_on, _fresh(m["competitors"]),
               revmod.ATTACK_PAGES, "threshold", "ad_library")]
    sentence = (f"{a['label'].capitalize()} draws {a['one_star']} of our one-star reviews, a top 2 theme. "
                f"{a['direct_leaders']} direct competitors lead their ads with it.")
    ent = {"type": "ladder_rung", "id": f"attack_{a['theme']}", "label": f"{a['label']} under attack"}
    return [_finding("COMP-R17", "high", ent, ev, sentence, [a["ladder"]], ends_on, 0.5,
                     "no baseline: reviews are not tied to order value in the brain")]


def rule_presence(m, ends_on):
    out = []
    for st in (m.get("presence") or {}).get("styles", []):
        if not st["undercut"]:
            continue
        ev = [_row("amazon_price_per_pair", st["amazon_per_pair"], "usd", "latest capture", ends_on, None, st["site_per_pair"],
                   "threshold", "marketplaces"),
              _row("site_price_per_pair", st["site_per_pair"], "usd", m["packs"]["month"], ends_on, None, None, "threshold",
                   "products_monthly", True),
              _row("amazon_listings", st["listings"], "n", "latest capture", ends_on, None, mktmod.MIN_LISTINGS, "threshold",
                   "marketplaces")]
        sentence = (f"{st['style'].capitalize()} sells on Amazon at ${st['amazon_per_pair']:.2f} a {m['term']['unit']}. Our site nets "
                    f"${st['site_per_pair']:.2f}, {round(st['gap'] * 100)} percent more.")
        ent = {"type": "sku", "id": f"amazon_{pagemod.slug(st['style'])}", "label": f"{st['style']} on Amazon"}
        out.append(_finding("COMP-R18", "medium", ent, ev, sentence, [f"{m['brand']}.marketplaces"], ends_on, 0.3,
                            "no baseline: orders lost to the cheaper channel are not measured"))
    return out


def rule_velocity(m, ends_on):
    v = m.get("velocity") or {}
    if not v.get("slow"):
        return []
    ev = [_row("our_launch_rate_week", v["our_rate"], "n", "latest capture", ends_on, None, v["bar"], "threshold", "ad_library"),
          _row("direct_median_launch_rate_week", v["direct_median_rate"], "n", "latest capture", ends_on, _fresh(m["competitors"]),
               None, "peer_band", "ad_library")]
    sentence = (f"We ship about {v['our_rate']:g} new ads a week. Direct pages ship a median {v['direct_median_rate']:g}. "
                "Both are estimates from ad life.")
    return [_finding("COMP-R19", "medium", {"type": "brand", "id": "creative_velocity", "label": "creative velocity"}, ev, sentence,
                     [f"{m['brand']}.learnings.september_flight"], ends_on, 0.3, "no baseline: the return on more ads is not measured")]


def rule_niche(m, ends_on):
    n = m.get("niche") or {}
    if not n.get("candidates"):
        return []
    c = n["candidates"][0]
    bar = n.get("bar") or {}
    ev = [_row("their_share_on_angle", c["their_share"], "%", "latest capture", ends_on, _fresh(m["competitors"]), nichemod.CANDIDATE_MIN,
               "threshold", "ad_library"),
          _row("our_share_on_angle", c["our_share"], "%", "latest capture", ends_on, None, round(c["their_share"] * nichemod.UNDER, 3),
               "threshold", "ad_library"),
          _row("buyers_to_matter", bar.get("buyers"), "n", "12 months", ends_on, None, None, "threshold", "economics")]
    sentence = (f"Tracked pages put {round(c['their_share'] * 100)} percent of their ads on {c['label'].lower()}; we put "
                f"{round(c['our_share'] * 100)} percent. It matters at {bar.get('buyers', 'an unknown number of'):,} buyers a year."
                if bar else f"Tracked pages put {round(c['their_share'] * 100)} percent of their ads on {c['label'].lower()}.")
    ent = {"type": "brand", "id": f"niche_{c['angle']}", "label": f"{c['label'].lower()} niche"}
    return [_finding("COMP-R20", "low", ent, ev, sentence, [f"{m['brand']}.economics.aov_usd", f"{m['brand']}.economics.repeat_rate_12m"],
                     ends_on, 0.3, "no baseline: demand for the niche is not measured")]


def rule_premium(m, ends_on):
    pr = m.get("premium") or {}
    if not pr.get("fires"):
        return []
    ev = [_row("our_premium_score", pr["our_score"], "%", "latest capture", ends_on, None, pr["direct_median_score"], "peer_band", "computed"),
          _row("our_discount_depth_pct", pr["our_depth"], "n", "latest capture", ends_on, None, pr["direct_median_depth"], "peer_band",
               "ad_library"),
          _row("depth_gap_points", pr["depth_gap"], "n", "latest capture", ends_on, None, premmod.DEEPER, "threshold", "computed")]
    sentence = (f"We show more premium signals than the direct median and discount {pr['our_depth']} percent. "
                f"Their median discount is {pr['direct_median_depth']:g} percent.")
    return [_finding("COMP-R21", "medium", {"type": "offer", "id": "discount_depth", "label": "discount depth"}, ev, sentence,
                     [f"{m['brand']}.offers.first_order_code"], ends_on, 0.5, "no baseline: margin given to the code is not in the brain")]


def rule_search(m, ends_on):
    s = m.get("search") or {}
    gaps = [r for r in s.get("rows", []) if not r["ours"]]
    out = [_unavailable("COMP-R23", "low", {"type": "brand", "id": "search_overlap", "label": "search overlap"},
                        ["keyword rankings and bids"], "a search data source (read only)",
                        "Connect Search Console for us and a keyword tool for the tracked domains.", ends_on)]
    if len(gaps) >= searchmod.GAP_TERMS:
        ev = [_row("their_terms_we_never_say", len(gaps), "n", "latest capture", ends_on, _fresh(m["competitors"]), searchmod.GAP_TERMS,
                   "threshold", "competitors"),
              _row("contested_terms", sum(1 for r in gaps if r["n"] >= 2), "n", "latest capture", ends_on, None, None, "threshold",
                   "competitors")]
        sentence = f"The tracked pages go after {len(gaps)} search terms our own lines never say, like {gaps[0]['term']}."
        out.append(_finding("COMP-R22", "low", {"type": "brand", "id": "search_seeds", "label": "search seeds"}, ev, sentence,
                            [f"{m['brand']}.products.materials"], ends_on, 0.3, "no baseline: search volume is not connected"))
    return out


def rule_new_move(m, ends_on):
    out = []
    for e in (m.get("changes") or {}).get("events", []):
        if e.get("source") not in ("page summary diff", "snapshot diff", "logged") or e["verdict"] != "follow":
            continue
        p = next((x for x in m["pages"] if x["name"] == e["page"]), None)
        metric = e["kind"] if e.get("source") == "logged" else "new_" + ("offer" if e["kind"] == "new_offer" else "angle")
        ev = [_row(metric, 1, "n", f"since {e.get('since', 'last capture')}", ends_on, None, 0, "threshold",
                   "team" if e.get("source") == "logged" else e["source"])]
        sentence = f"{e['page']} {e['text']}, first seen {e['when']}."
        ent = {"type": "page", "id": f"move_{pagemod.slug(e['page'])}_{e['kind']}_{pagemod.slug(str(e.get('value')))}",
               "label": f"{e['page']}: {e['text']}"}
        out.append(_finding("COMP-R24", "medium", ent, ev, sentence, (p or {}).get("record_ids") or [], ends_on, 0.5,
                            "no baseline: a new competitor move has no cost to us until it takes share"))
    return out


def rule_price_cut(m, ends_on):
    out = []
    for mv in (m.get("price_moves") or {}).get("moves", []):
        if mv["kind"] != "cut":
            continue
        logged = mv.get("source") == "logged"
        src = "team" if logged else "captures"
        win = f"trailing {inpmod.TRAIL_DAYS} days to {mv['when']}" if logged else f"since {mv['since']}"
        ev = [_row("price_per_unit" if logged else "median_price_per_pair", mv["to"], "usd", win, ends_on, None, mv["from"],
                   "trailing" if logged else "threshold", src),
              _row("price_change", mv["change"], "%", win, ends_on, None, -capmod.PRICE_MOVE, "threshold", src)]
        if logged:
            sentence = (f"{mv['page']} cut the price on {mv['product']} by {round(-mv['change'] * 100)} percent, ${mv['to']:.2f} a "
                        f"{m['term']['unit']} against its own {inpmod.TRAIL_DAYS}-day average of ${mv['from']:.2f}.")
        else:
            sentence = f"{mv['page']} cut its median price per {m['term']['unit']} {round(-mv['change'] * 100)} percent, ${mv['from']:.2f} to ${mv['to']:.2f}."
        eid = f"price_cut_{pagemod.slug(mv['page'])}" + (f"_{pagemod.slug(mv['product'])}" if logged else "")
        ent = {"type": "page", "id": eid, "label": f"{mv['page']} price cut"}
        out.append(_finding("COMP-R25", "high" if mv["frame"] == "direct" else "medium", ent, ev, sentence, [], ends_on, 0.5,
                            "no baseline: orders lost to their new price are not measured"))
    return out


def rule_landing(m, ends_on):
    rows = [r for r in (m.get("landing") or {}).get("rows", []) if not r["tracked"]]
    if not rows:
        return []
    ev = [_row("threats_untracked", len(rows), "n", "latest capture", ends_on, None, 0, "threshold", "competitors")]
    sentence = f"{', '.join(r['name'] for r in rows)} are top threats and none of their landing pages is tracked."
    return [_finding("COMP-R26", "low", {"type": "page", "id": "landing_tracking", "label": "threat landing pages"}, ev, sentence,
                     [], ends_on, 0.5, "no baseline: page changes are not captured yet")]


STALE_CARD_DAYS = 90


def rule_cards(m, ends_on):
    out = []
    for p in m["pages"]:
        age = p.get("card_age_days", p.get("age_days"))
        if p["role"] == "self" or p["frame"] != "direct" or p["source"] == "none" or age is None:
            continue
        if age > STALE_CARD_DAYS:
            ev = [_row("battlecard_freshness_days", age, "days", "latest check" if p.get("card_checked_on") else "latest capture", ends_on, age,
                       STALE_CARD_DAYS, "threshold", "team" if p.get("card_checked_on") else "competitors")]
            out.append(_finding("COMP-R27", "low", {"type": "page", "id": f"card_{p['key']}", "label": f"{p['name']} battlecard"}, ev,
                                f"The {p['name']} battlecard rests on facts last checked {age} days ago.", p["record_ids"], ends_on,
                                0.5, "no baseline: a stale claim has no measured cost"))
    return out


def rule_frames(m, ends_on):
    fr = m.get("frames") or {}
    if not fr.get("fires"):
        return []
    t = fr["top"]
    ev = [_row("top_frame_mentions", t["mentions"], "n", "reddit capture", ends_on, None, None, "threshold", "reddit"),
          _row("brand_named_in_frame", t["brand_named"], "n", "reddit capture", ends_on, None, None, "threshold", "reddit")]
    sentence = (f"Shoppers frame the category as {t['label']} ({t['mentions']} mentions). Our line does not say it, "
                "and it was never tested.")
    return [_finding("COMP-R28", "medium", {"type": "brand", "id": "positioning_test", "label": "positioning line"}, ev, sentence,
                     [f"{m['brand']}.positioning.frame", f"{m['brand']}.positioning.reddit_frames"], ends_on, 0.3,
                     "no baseline: no positioning test on file")]


def rule_winloss(m, ends_on):
    ls = m.get("losses") or {}
    fired = [x for x in ls.get("rows", []) if x["fires"]]
    n = ls.get("interviews") or 0
    short = [(x["name"], (x.get("win_loss") or {}).get("n") or 0) for x in fired[:lossmod.MAX_NAMES]]
    short = [(nm, k) for nm, k in short if k < lossmod.MIN_INTERVIEWS]
    if not short:
        return []
    ev = [_row("names_we_lose_to", len(fired), "n", "reddit capture", ends_on, None, 1, "threshold", "reddit"),
          _row("winloss_interviews", n, "n", "logged on this screen", ends_on, None, lossmod.MIN_INTERVIEWS * len(fired[:lossmod.MAX_NAMES]),
               "threshold", "team"),
          _row("names_short_of_interviews", len(short), "n", "logged on this screen", ends_on, None, 0, "threshold", "team")]
    if not n:
        sentence = f"We lose shoppers to {', '.join(x['name'] for x in fired)} and have no win-loss interviews on why."
    else:
        sentence = (f"We lose shoppers to {', '.join(x['name'] for x in fired)}. Still short of {lossmod.MIN_INTERVIEWS} interviews each: "
                    + ", ".join(f"{nm} ({k})" for nm, k in short) + ".")
    return [_finding("COMP-R29", "low", {"type": "brand", "id": "winloss", "label": "win-loss research"}, ev, sentence,
                     [x["record"] for x in fired], ends_on, 0.5, "no baseline: the win rate is unknown")]


def rule_repeat_loss(m, ends_on):
    """COMP-R31: the same coded reason in 3 or more logged losses against the same named competitor."""
    out = []
    wl = (m.get("losses") or {}).get("win_loss") or {}
    for w in wl.get("rows", []):
        rp = w.get("repeat")
        if not rp:
            continue
        ev = [_row("losses_same_reason", rp["n"], "n", "interviews logged", ends_on, None, wl["repeat_at"], "threshold", "team"),
              _row("losses_against_name", w["losses"], "n", "interviews logged", ends_on, None, None, "threshold", "team"),
              _row("win_rate_against_name", w["win_rate"], "ratio", "interviews logged", ends_on, None, None, "threshold", "team")]
        sentence = f"{rp['n']} people chose {w['name']} over us for the same reason: {rp['reason']}."
        key = w["name"].lower().replace(" ", "_")
        out.append(_finding("COMP-R31", "high", {"type": "brand", "id": f"repeat_{key}", "label": f"losses to {w['name']}"}, ev, sentence,
                            [], ends_on, min(0.9, 0.3 + 0.1 * w["n"]), "no baseline: lost orders to a named brand are not measured"))
    return out


def rule_frame_win(m, ends_on):
    """COMP-R32: the latest logged positioning poll is a win for the challenger line."""
    t = (m.get("frames") or {}).get("latest")
    if not t or t["verdict"] != "win":
        return []
    ev = [_row("positioning_test_score", t["score"], "points", f"poll on {t['date']}", ends_on, None, framemod.WIN_POINTS, "threshold", "team"),
          _row("shoppers_asked", t["asked"], "n", f"poll on {t['date']}", ends_on, None, framemod.MIN_N, "threshold", "team")]
    sentence = f"Line {t['line']} beat our current line by {t['score']:g} points with {t['asked']} shoppers. It is not in our ads yet."
    return [_finding("COMP-R32", "high", {"type": "brand", "id": "positioning_winner", "label": "winning positioning line"}, ev, sentence,
                     [f"{m['brand']}.positioning.frame"], ends_on, min(0.9, 0.4 + t["asked"] / 1000), "no baseline: the line has not run in ads")]


def rule_band_out_of_date(m, ends_on):
    """COMP-R33: a price the team saw on a rival's site sits outside the public band the brain holds for that page."""
    out = []
    for b in (m.get("ladder") or {}).get("bands", []):
        xs = b.get("out_of_band") or []
        if not xs:
            continue
        x = max(xs, key=lambda x: x["date"])
        band = f"${b['low']:.2f} to ${b['high']:.2f}" if b["high"] is not None else f"from ${b['low']:.2f}"
        ev = [_row("price_per_unit_seen", x["per_unit"], "usd", f"seen {x['date']}", ends_on, None, [b["low"], b["high"]], "threshold", "team"),
              _row("products_outside_band", len(xs), "n", "logged prices", ends_on, None, 0, "threshold", "team")]
        sentence = (f"{b['name']} sells {x['product']} at ${x['per_unit']:.2f} a {m['term']['unit']}, outside the band on file ({band}). "
                    "Every price finding on them reads an old band.")
        out.append(_finding("COMP-R33", "low", {"type": "page", "id": f"band_{pagemod.slug(b['name'])}", "label": f"{b['name']} price band"}, ev,
                            sentence, [], ends_on, 0.6, "no baseline: the band's age is unknown"))
    return out


def rule_recheck(m, ends_on):
    """COMP-R34: logged products whose latest price is past the re-check age; without a fresh one the price rule loses its baseline."""
    due = (m.get("price_moves") or {}).get("recheck") or []
    if not due:
        return []
    ev = [_row("prices_due_recheck", len(due), "n", "logged prices", ends_on, due[0]["age_days"], 0, "threshold", "team"),
          _row("oldest_price_age_days", due[0]["age_days"], "days", "logged prices", ends_on, due[0]["age_days"], inpmod.RECHECK_DAYS, "threshold", "team")]
    sentence = (f"{len(due)} logged rival price{'s are' if len(due) != 1 else ' is'} more than {inpmod.RECHECK_DAYS} days old; "
                f"the oldest, {due[0]['page']} {due[0]['product']}, was seen {due[0]['age_days']} days ago.")
    return [_finding("COMP-R34", "low", {"type": "brand", "id": "price_recheck", "label": "price re-checks"}, ev, sentence, [], ends_on, 0.8,
                     "no baseline: a missed price cut has no measured cost")]


def rule_burst(m, ends_on):
    """COMP-R36: lights up with the second ad-level snapshot. A direct page with BURST_ADS or more new ads since the last pull."""
    out = []
    frame = {p["name"]: p["frame"] for p in m["pages"]}
    for e in (m.get("changes") or {}).get("events", []):
        if e["kind"] != "new_ads" or e.get("source") != "snapshot diff" or frame.get(e["page"]) != "direct" or (e.get("n") or 0) < BURST_ADS:
            continue
        since = e["text"].split("since ")[-1] if "since " in e["text"] else "the last pull"
        ev = [_row("new_ads_since_last_pull", e["n"], "n", f"since {since}", ends_on, None, BURST_ADS, "threshold", "snapshot diff")]
        out.append(_finding("COMP-R36", "medium", {"type": "page", "id": f"burst_{pagemod.slug(e['page'])}", "label": f"{e['page']} ad burst"}, ev,
                            f"{e['page']} launched {e['n']} new ads since the last pull.", [], ends_on, 0.6,
                            "no baseline: their spend behind the new ads is not public"))
    return out


def rule_season(m, ends_on):
    sn = m.get("season") or {}
    if not sn.get("fires"):
        return []
    ev = [_row("days_to_black_friday", sn["days_to_black_friday"], "days", "calendar", ends_on, None, seasonmod.LEAD_DAYS, "threshold", "calendar"),
          _row("direct_pages_with_gifting", len(sn["direct_gifting"]), "n", "latest capture", ends_on, None, 2, "threshold", "ad_library"),
          _row("our_gifting_ads", 0, "n", "latest capture", ends_on, None, None, "threshold", "ad_library")]
    sentence = (f"Black Friday is {sn['days_to_black_friday']} days away. {len(sn['direct_gifting'])} direct competitors run a gifting "
                "angle; none of our ads does.")
    return [_finding("COMP-R30", "high", {"type": "brand", "id": "season_gifting", "label": "holiday gifting"}, ev, sentence,
                     [f"{m['brand']}.offers.gifting"], ends_on, 0.5, "no baseline: last season's gifting ads are not in the brain")]


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
        out += [_unavailable("COMP-R16", "low", {"type": "ladder_rung", "id": "lower_rungs", "label": "lower rungs of the ladder"},
                             ["search trends by rung"], "a search trends source (read only)",
                             "Connect a search trends source for the category and each lower rung.", ends_on)]
        out += [_unavailable("COMP-R35", "low", {"type": "brand", "id": "rival_traffic", "label": "rival traffic by channel"},
                             ["site visits and share by source per tracked page"], "a site traffic estimate source (read only)",
                             "Connect a site traffic estimate source in Setup, read-only, for the direct pages.", ends_on)]
        out += rule_ladder(m, ends_on) + rule_corners(m, ends_on) + rule_refresh(m, ends_on) + rule_freshness(m, ends_on) + rule_losses(m, ends_on) + rule_attack(m, ends_on) + rule_presence(m, ends_on) + rule_velocity(m, ends_on) + rule_niche(m, ends_on) + rule_premium(m, ends_on) + rule_search(m, ends_on) + rule_new_move(m, ends_on) + rule_price_cut(m, ends_on) + rule_landing(m, ends_on) + rule_cards(m, ends_on) + rule_frames(m, ends_on) + rule_winloss(m, ends_on) + rule_repeat_loss(m, ends_on) + rule_frame_win(m, ends_on) + rule_band_out_of_date(m, ends_on) + rule_recheck(m, ends_on) + rule_burst(m, ends_on) + rule_season(m, ends_on)
    out += rule_price(m, ends_on) + rule_lookalike(m, ends_on)
    out.sort(key=lambda f: (SEVERITY_ORDER[f["severity"]], f["id"]))
    return out


if __name__ == "__main__":
    b = sys.argv[1] if len(sys.argv) > 1 else "bombas"
    print(json.dumps(run(b, {"ends_on": "2026-09-27", "days": 1, "trailing": 0}), indent=1))
