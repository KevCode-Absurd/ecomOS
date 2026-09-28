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
BRN-R12 open conflict. Two sources disagree on one field and no founder
    decision exists (review/conflicts.json, status open). Severity high when
    the section is gated (identity, claims, decisions) and needs the founder,
    else medium. Capability BRN-C05 (conflict detection with the site as
    default; the decision is the founder's). Reputation override 5 when the
    field is a claim or policy. Owner: 05-brand-brain.
BRN-R13 claim untiered too long. A claims record with tier unverified,
    inferred, evidence or reported for more than claims.UNTIERED_DAYS (7)
    days (room spec: "{claim} has been untiered for {n} days and needs a
    founder call"). Severity medium; high when a ladder rung uses it in copy.
    Capability BRN-C03. Reputation override 5 (a claim). Owner: 05-brand-brain.
BRN-R14 site changed unnoticed. A record in the site crawl differs between
    the two newest snapshots (sitediff.py) and no person has marked it
    reviewed. Severity from the section: offers, policies, claims and product
    prices high, identity and stack medium, else low. Capability BRN-C01.
    Reputation override 5 for a claim or policy change. Owner: 05-brand-brain.
BRN-R15 marketplace price below MAP. A marketplace listing's price per
    pair (parity.py) sits below the founder's minimum advertised price. Fires
    only when offers.map_usd_per_pair is set; otherwise one unavailable
    finding names the founder record that fills it. Severity high.
    Capability PROD-C46. Reputation override 5. Owner: 05-brand-brain.
BRN-R16 unrecognised marketplace seller. A listing's seller is not in the
    founder's list (offers.marketplace_seller_names). Fires only when the
    pull carried the seller and the list exists; when the seller is missing
    from every listing, one unavailable finding names the connector that
    fills it (Amazon Selling Partner API, or a listing pull with the seller
    field). Severity high. Capability PROD-C46. Owner: 05-brand-brain.
BRN-R17 contract renewal approaching. A stored contract's renewal date is
    inside the alert window for its vendor type (contracts.py WINDOW_DAYS:
    platform and 3PL 90 days, agency and payments 60, apps and SaaS 30), or
    has passed. Severity high for platform, 3PL and agency, else medium.
    Capability LOOP-C28. Owner: 05-brand-brain.
BRN-R18 contract missing renewal date. A stored contract has no renewal
    date (low, one per contract), or vendors the brain knows from the stack
    and partner mentions have no contract on file (medium, one finding).
    Capability LOOP-C28. Owner: 05-brand-brain.
BRN-R19 disclosure missing. A site-level US disclosure check fails
    (legal.py checks): privacy policy with an effective date, state privacy
    notice, terms, returns posted, cookie consent, accessibility statement,
    creator ads labelled. Severity high; it blocks going live. Capability
    LOOP-C27. Reputation override 5 (legal disclosure gap). Owner: 05-brand-brain.
BRN-R20 permission gap. A section with records and no explicit permission
    entry defaults to restricted (health.permissions). One low finding naming
    the count, so the founder sets the map once. Capability LOOP-C29.
    Owner: 05-brand-brain.
BRN-R21 modelled assumption read by rooms. An assumption in
    assumptions.json with status modelled or sourced, no founder record on its
    source id, and rooms that read its section (assumptions.py). Severity
    medium for modelled, low for sourced. Capability BRN-C07 (founder round).
    Owner: 05-brand-brain.
BRN-R22 picked idea without a brief. A plans record `idea_<id>` the founder
    picked from the idea bank (status picked) with no test brief yet. Severity
    medium. Capability PROP-C06 (proposal cards; the brief is drafted, the
    founder approves). Owner: 05-brand-brain.
BRN-R23 objection rung without proof. A ladder rung used on at least one
    surface (ad copy, product page, Amazon listing, CX macro, offer) whose
    proof_ids are empty, point at records the brain no longer holds, or point
    only at a forbidden claim (ladderproof.py). Severity medium when 10 or more
    one-star lines sit behind it, else low. Capability BRN-C03 (claim tiering;
    the proof brief is drafted, the founder approves the record). Owner:
    05-brand-brain.
BRN-R24 brain router drifted or broken. BRAIN.md (the router every agent
    reads first) has a section row or version line that no longer matches the
    records, or a link to a missing file (selfaudit.py over app/brain/audit.py).
    One low finding. Capability BRN-C12 (brain health). Owner: 05-brand-brain.
BRN-R25 duplicate records. Two active records in one section say the same
    thing (same normalised text, or the same scalar value on the same field).
    One low finding naming the pairs; the stronger record is kept and the other
    retired, never deleted. Capability BRN-C12. Owner: 05-brand-brain.
BRN-R26 peak not ready. A peak inside the next 90 days (US retail peaks
    computed from the date, plus the brand's own dated calendar records) with
    at least one gap in its readiness checks (peaks.py): no offer decided, no
    holiday return window, a derived shipping cutoff not confirmed, no gift
    card record, a giving claim not tiered, no creative on the peak's hook.
    Unavailable checks never count. Severity high at 30 days or less, medium
    at 60 or less, else low. Capability BRN-C07 (founder round; the agent
    drafts the briefs, the founder decides the offer). Owner: 05-brand-brain.
BRN-R27 visual identity gaps. No colour token in the visual section, no
    logo rules record, or a text-on-background pair under the 4.5 WCAG
    contrast ratio (visual.py). One low finding naming the gaps. Capability
    CREA-C12 (image accuracy; the palette is the brain's). Owner: 05-brand-brain.
BRN-R28 visibility mismatch. Records marked public whose source is not a
    public one, in a section that is private by nature (a leak to any
    public-facing agent), or private records from public sources in sections
    public by nature (visibility.py). Severity medium with a leak, else low.
    Capability LOOP-C22 (offboarding and access; what leaves the brain).
    Owner: 05-brand-brain.
BRN-R29 rejected idea due for review. A learnings record `rejected_idea_<id>`
    (the founder rejected a bank idea with a reason and a review date) whose
    review date has passed (bottlenecks.py). Severity low. Capability PROP-C06.
    The founder keeps it out for another period or brings it back. Owner:
    05-brand-brain.
BRN-R30 asset right expiring or expired. A content record `asset_<slug>`
    (assets.py) whose right expired while the asset is live (high), ends inside
    its window (medium: 30 days for creator and music, 60 for photo, video,
    font), or has no expiry date (low). Capability LOOP-C29. Owner:
    05-brand-brain.
BRN-R31 consent expiring or expired. A content record `consent_<slug>` (ugc.py)
    whose term ended (medium: the quote or asset may be live in its scope) or
    ends inside 30 days (low). Capability LOOP-C27 (disclosures and
    endorsements). Owner: 05-brand-brain.
BRN-R32 positioning drift. The positioning's top words are echoed by fewer
    than 20 percent of praise quotes in the language bank, or a positioning
    word appears in more complaints than praise (drift.py). One low finding
    with the drift brief. Capability BRAND-C57 (positioning). Owner:
    05-brand-brain.
BRN-R33 audience profiles not set. No avatar record is approved, or no
    default profile is picked for ads (audiences.py), so generators write for
    no one in particular. One low finding. Capability BRN-C10 (avatar and
    language bank maintenance). Owner: 05-brand-brain.
BRN-R34 red lines without a reason. Entries in the red lines register
    (forbidden claims, required lines, blocking channel rules, rejected ideas,
    never or always decisions) with no reason on file (redlines.py). One low
    finding naming the count. Capability BRN-C08. Owner: 05-brand-brain.
BRN-R35 section review overdue. A section with records whose last review
    (or, before any, its last update) is older than its cadence (owners.py:
    the founder's cadence, else the shelf life). Severity medium past twice
    the cadence, else low. Capability BRN-C12. Owner: the section's owner.
BRN-R36 records expiring this week. Records whose expiry falls inside 7
    days, or is past, grouped by source type (expiring.py). One finding per
    source: the agent re-pulls a public source read-only inside its caps, the
    founder confirms a founder or document record. Severity medium when any is
    past, else low. Capability BRN-C02. Owner: 05-brand-brain.
BRN-R37 dependents pending after a number change. A plans record
    `update_<field>` (numbers.py) with dependents not yet marked done: places
    that still carry the old value. Severity medium while any dependent is an
    ad or a snippet, else low. Capability BRN-C01. Owner: 05-brand-brain.
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
    {"rule_id": "BRN-R12", "name": "open conflict", "entity_type": "brand",
     "inputs": ["review/conflicts.json"], "capability": "BRN-C05", "owner_screen": SCREEN},
    {"rule_id": "BRN-R13", "name": "claim untiered too long", "entity_type": "brand",
     "inputs": ["claims", "objection_ladders"], "capability": "BRN-C03", "owner_screen": SCREEN},
    {"rule_id": "BRN-R14", "name": "site changed unnoticed", "entity_type": "brand",
     "inputs": ["snapshots/site", "raw/a-site"], "capability": "BRN-C01", "owner_screen": SCREEN},
    {"rule_id": "BRN-R15", "name": "marketplace price below MAP", "entity_type": "sku",
     "inputs": ["marketplaces", "offers.map_usd_per_pair"], "capability": "PROD-C46", "owner_screen": SCREEN},
    {"rule_id": "BRN-R16", "name": "unrecognised marketplace seller", "entity_type": "sku",
     "inputs": ["marketplaces", "offers.marketplace_seller_names"], "capability": "PROD-C46", "owner_screen": SCREEN},
    {"rule_id": "BRN-R17", "name": "contract renewal approaching", "entity_type": "brand",
     "inputs": ["operations.contract_*"], "capability": "LOOP-C28", "owner_screen": SCREEN},
    {"rule_id": "BRN-R18", "name": "contract missing renewal date", "entity_type": "brand",
     "inputs": ["operations.contract_*", "stack", "team"], "capability": "LOOP-C28", "owner_screen": SCREEN},
    {"rule_id": "BRN-R19", "name": "disclosure missing", "entity_type": "page",
     "inputs": ["policies", "site_map", "stack", "learnings"], "capability": "LOOP-C27", "owner_screen": SCREEN},
    {"rule_id": "BRN-R20", "name": "permission gap", "entity_type": "brand",
     "inputs": ["team.permission_*"], "capability": "LOOP-C29", "owner_screen": SCREEN},
    {"rule_id": "BRN-R21", "name": "modelled assumption read by rooms", "entity_type": "metric",
     "inputs": ["assumptions.json", "questions.bank.json"], "capability": "BRN-C07", "owner_screen": SCREEN},
    {"rule_id": "BRN-R22", "name": "picked idea without a brief", "entity_type": "brand",
     "inputs": ["plans.idea_*"], "capability": "PROP-C06", "owner_screen": SCREEN},
    {"rule_id": "BRN-R23", "name": "objection rung without proof", "entity_type": "brand",
     "inputs": ["objection_ladders", "claims", "policies", "offers", "products"], "capability": "BRN-C03", "owner_screen": SCREEN},
    {"rule_id": "BRN-R24", "name": "brain router drifted or broken", "entity_type": "brand",
     "inputs": ["BRAIN.md", "every section"], "capability": "BRN-C12", "owner_screen": SCREEN},
    {"rule_id": "BRN-R25", "name": "duplicate records", "entity_type": "brand",
     "inputs": ["every section"], "capability": "BRN-C12", "owner_screen": SCREEN},
    {"rule_id": "BRN-R26", "name": "peak not ready", "entity_type": "brand",
     "inputs": ["calendar", "offers", "policies", "products", "identity", "claims", "learnings", "assumptions.json"], "capability": "BRN-C07", "owner_screen": SCREEN},
    {"rule_id": "BRN-R27", "name": "visual identity gaps", "entity_type": "brand",
     "inputs": ["visual"], "capability": "CREA-C12", "owner_screen": SCREEN},
    {"rule_id": "BRN-R28", "name": "visibility mismatch", "entity_type": "brand",
     "inputs": ["every section"], "capability": "LOOP-C22", "owner_screen": SCREEN},
    {"rule_id": "BRN-R29", "name": "rejected idea due for review", "entity_type": "brand",
     "inputs": ["learnings.rejected_idea_*"], "capability": "PROP-C06", "owner_screen": SCREEN},
    {"rule_id": "BRN-R30", "name": "asset right expiring or expired", "entity_type": "brand",
     "inputs": ["content.asset_*"], "capability": "LOOP-C29", "owner_screen": SCREEN},
    {"rule_id": "BRN-R31", "name": "consent expiring or expired", "entity_type": "brand",
     "inputs": ["content.consent_*"], "capability": "LOOP-C27", "owner_screen": SCREEN},
    {"rule_id": "BRN-R32", "name": "positioning drift", "entity_type": "brand",
     "inputs": ["positioning", "identity", "voice", "language_bank"], "capability": "BRAND-C57", "owner_screen": SCREEN},
    {"rule_id": "BRN-R33", "name": "audience profiles not set", "entity_type": "brand",
     "inputs": ["avatars", "objection_ladders"], "capability": "BRN-C10", "owner_screen": SCREEN},
    {"rule_id": "BRN-R34", "name": "red lines without a reason", "entity_type": "brand",
     "inputs": ["claims", "content", "learnings", "decisions", "visual"], "capability": "BRN-C08", "owner_screen": SCREEN},
    {"rule_id": "BRN-R35", "name": "section review overdue", "entity_type": "brand",
     "inputs": ["team.owner_*", "every section"], "capability": "BRN-C12", "owner_screen": SCREEN},
    {"rule_id": "BRN-R36", "name": "records expiring this week", "entity_type": "brand",
     "inputs": ["every section (expires_at)"], "capability": "BRN-C02", "owner_screen": SCREEN},
    {"rule_id": "BRN-R37", "name": "dependents pending after a number change", "entity_type": "brand",
     "inputs": ["plans.update_*"], "capability": "BRN-C01", "owner_screen": SCREEN},
]
AUTONOMY = {"BRN-C12": "agent_does", "BRN-C07": "founder_gate", "BRN-C03": "agent_does",
            "CREA-C19": "agent_does", "CREA-C04": "agent_does", "BRN-C11": "agent_does", "CREA-C06": "agent_does",
            "BRAND-C57": "agent_does", "CREA-C03": "agent_does", "BRN-C05": "founder_gate", "BRN-C01": "agent_does", "PROD-C46": "agent_does", "LOOP-C28": "agent_does", "LOOP-C27": "agent_does", "LOOP-C29": "agent_does", "PROP-C06": "agent_does", "CREA-C12": "agent_does", "LOOP-C22": "founder_gate", "BRN-C10": "agent_does", "BRN-C08": "founder_gate", "BRN-C02": "agent_does"}

_uspec = importlib.util.spec_from_file_location("brand_brain_assumptions", Path(__file__).resolve().parent / "assumptions.py")
assumptions = importlib.util.module_from_spec(_uspec)
_uspec.loader.exec_module(assumptions)
_tspec = importlib.util.spec_from_file_location("brand_brain_contracts", Path(__file__).resolve().parent / "contracts.py")
contracts = importlib.util.module_from_spec(_tspec)
_tspec.loader.exec_module(contracts)
_lspec = importlib.util.spec_from_file_location("brand_brain_legal", Path(__file__).resolve().parent / "legal.py")
legal = importlib.util.module_from_spec(_lspec)
_lspec.loader.exec_module(legal)
_pspec = importlib.util.spec_from_file_location("brand_brain_parity", Path(__file__).resolve().parent / "parity.py")
parity = importlib.util.module_from_spec(_pspec)
_pspec.loader.exec_module(parity)
_nmspec = importlib.util.spec_from_file_location("brand_brain_numbers", Path(__file__).resolve().parent / "numbers.py")
numbers = importlib.util.module_from_spec(_nmspec)
_nmspec.loader.exec_module(numbers)
_exspec = importlib.util.spec_from_file_location("brand_brain_expiring", Path(__file__).resolve().parent / "expiring.py")
expiring = importlib.util.module_from_spec(_exspec)
_exspec.loader.exec_module(expiring)
_owspec = importlib.util.spec_from_file_location("brand_brain_owners", Path(__file__).resolve().parent / "owners.py")
owners = importlib.util.module_from_spec(_owspec)
_owspec.loader.exec_module(owners)
_rlspec = importlib.util.spec_from_file_location("brand_brain_redlines", Path(__file__).resolve().parent / "redlines.py")
redlines = importlib.util.module_from_spec(_rlspec)
_rlspec.loader.exec_module(redlines)
_auspec = importlib.util.spec_from_file_location("brand_brain_audiences", Path(__file__).resolve().parent / "audiences.py")
audiences = importlib.util.module_from_spec(_auspec)
_auspec.loader.exec_module(audiences)
_drspec = importlib.util.spec_from_file_location("brand_brain_drift", Path(__file__).resolve().parent / "drift.py")
drift = importlib.util.module_from_spec(_drspec)
_drspec.loader.exec_module(drift)
_ugspec = importlib.util.spec_from_file_location("brand_brain_ugc", Path(__file__).resolve().parent / "ugc.py")
ugc = importlib.util.module_from_spec(_ugspec)
_ugspec.loader.exec_module(ugc)
_asspec = importlib.util.spec_from_file_location("brand_brain_assets", Path(__file__).resolve().parent / "assets.py")
assets = importlib.util.module_from_spec(_asspec)
_asspec.loader.exec_module(assets)
_bnspec = importlib.util.spec_from_file_location("brand_brain_bottlenecks", Path(__file__).resolve().parent / "bottlenecks.py")
bottlenecks = importlib.util.module_from_spec(_bnspec)
_bnspec.loader.exec_module(bottlenecks)
_vbspec = importlib.util.spec_from_file_location("brand_brain_visibility", Path(__file__).resolve().parent / "visibility.py")
visibility = importlib.util.module_from_spec(_vbspec)
_vbspec.loader.exec_module(visibility)
_vispec = importlib.util.spec_from_file_location("brand_brain_visual", Path(__file__).resolve().parent / "visual.py")
visual = importlib.util.module_from_spec(_vispec)
_vispec.loader.exec_module(visual)
_qspec = importlib.util.spec_from_file_location("brand_brain_peaks", Path(__file__).resolve().parent / "peaks.py")
peaks = importlib.util.module_from_spec(_qspec)
_qspec.loader.exec_module(peaks)
_xspec = importlib.util.spec_from_file_location("brand_brain_selfaudit", Path(__file__).resolve().parent / "selfaudit.py")
selfaudit = importlib.util.module_from_spec(_xspec)
_xspec.loader.exec_module(selfaudit)
_dspec = importlib.util.spec_from_file_location("brand_brain_ladderproof", Path(__file__).resolve().parent / "ladderproof.py")
ladderproof = importlib.util.module_from_spec(_dspec)
_dspec.loader.exec_module(ladderproof)
_sspec = importlib.util.spec_from_file_location("brand_brain_sitediff", Path(__file__).resolve().parent / "sitediff.py")
sitediff = importlib.util.module_from_spec(_sspec)
_sspec.loader.exec_module(sitediff)
_cspec = importlib.util.spec_from_file_location("brand_brain_claims", Path(__file__).resolve().parent / "claims.py")
claims_mod = importlib.util.module_from_spec(_cspec)
_cspec.loader.exec_module(claims_mod)
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
        names = ", ".join((f.split(".", 1)[1] if "." in f else "the whole section").replace("_", " ") for f in s["fields"])
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


def rule_conflicts(brain: Brain, ends_on: str) -> list[dict]:
    out = []
    path = brain.dir / "review" / "conflicts.json"
    try:
        rows = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    except (OSError, ValueError):
        rows = []
    for c in rows:
        if c.get("status", "open") != "open":
            continue
        vals = c.get("values") or []
        age = None
        try:
            age = (brain.today - dt.date.fromisoformat(str(c.get("raised_at"))[:10])).days
        except (TypeError, ValueError):
            pass
        ev = [_row("sources_disagreeing", len(vals), "n", ends_on, age, 1, "review/conflicts.json"),
              _row("days_open", age, "days", ends_on, age, 0, "review/conflicts.json")]
        a, b = (vals + [{}, {}])[:2]
        kept = next((v for v in vals if v.get("record_id") == c.get("kept")), a)
        sentence = (f"{(a.get('source_type') or 'a source').replace('_', ' ')} says \"{str(a.get('value'))[:40]}\" and {(b.get('source_type') or 'another').replace('_', ' ')} says "
                    f"\"{str(b.get('value'))[:40]}\" for {c.get('field', '').replace('_', ' ')}. \"{str(kept.get('value'))[:40]}\" is kept until you decide.")
        f = _finding("BRN-R12", "high" if c.get("needs_founder") else "medium",
                     {"type": "brand", "id": f"conflict_{c.get('section')}_{c.get('field')}", "label": f"{c.get('section')} {c.get('field')}".replace("_", " ")},
                     ev, sentence, [v.get("record_id") for v in vals if v.get("record_id")][:4], ends_on, 0.7)
        f["conflict_id"] = c.get("id")
        out.append(f)
    return out


def rule_untiered_claims(brain: Brain, ends_on: str) -> list[dict]:
    out = []
    for c in claims_mod.desk(brain)["claims"]:
        if c["verdict"]["kind"] != "fix":
            continue
        in_copy = any("copy" in u["uses"] for u in c["used_by"])
        ev = [_row("days_untiered", c["age_days"], "days", ends_on, c["age_days"], claims_mod.UNTIERED_DAYS, "claims"),
              _row("rungs_using_it", len(c["used_by"]), "n", ends_on, None, None, "objection_ladders")]
        sentence = f"The {(c['field'] or '').replace('_', ' ')} claim has been {c['tier']} for {c['age_days']} days and needs your call." + (" Copy uses it." if in_copy else "")
        out.append(_finding("BRN-R13", "high" if in_copy else "medium", {"type": "brand", "id": f"claim_{c['field']}", "label": (c["field"] or "").replace("_", " ")},
                            ev, sentence, [c["id"]], ends_on, 0.7))
    return out


def rule_site_changes(brain: Brain, ends_on: str) -> list[dict]:
    out = []
    try:
        sd = sitediff.diff(brain)
    except (OSError, ValueError):
        return out
    for c in sd.get("changes") or []:
        if c.get("reviewed"):
            continue
        ev = [_row("changed_records", 1, "n", ends_on, None, 0, "snapshots/site"),
              _row("snapshot_pair", None, "text", ends_on, None, None, sd.get("pair") or "")]
        what = (c.get("field") or "").replace("_", " ")
        if c["change"] == "changed":
            sentence = f"{what} changed from {c['old_text']} to {c['new_text']} on the site ({c.get('captured_at') or sd.get('new')})."
        elif c["change"] == "added":
            sentence = f"{what} appeared on the site: {c['new_text']} ({c.get('captured_at') or sd.get('new')})."
        else:
            sentence = f"{what} left the site. It was {c['old_text']}."
        f = _finding("BRN-R14", c["severity"], {"type": "brand", "id": f"change_{c['section']}_{c.get('field') or 'x'}", "label": f"{c['section']} {what}".replace("_", " ")},
                     ev, sentence, [c["id"]], ends_on, 0.9)
        f["site_change"] = {"section": c["section"], "field": c.get("field"), "change": c["change"], "action": c["action"]}
        out.append(f)
    return out


def rule_parity(brain: Brain, ends_on: str) -> list[dict]:
    out = []
    pv = parity.strip(brain)
    if not pv["listings"]:
        return out
    if pv["map_usd_per_pair"] is None:
        f = _finding("BRN-R15", "high", {"type": "brand", "id": "map_unset", "label": "minimum advertised price"}, [],
                     "No minimum advertised price is on file, so no listing can be checked against it.", [], ends_on, 0.5)
        f.update(status="unavailable", unavailable={"inputs": ["offers.map_usd_per_pair"], "connector": "a founder record on the brand brain screen",
                                                    "fix": "Type the MAP per pair in the marketplace parity block. It saves as an approved record."})
        out.append(f)
    else:
        for l in pv["listings"]:
            fl = next((x for x in l["flags"] if x["key"] == "below_map"), None)
            if not fl:
                continue
            ev = [_row("price_per_pair_usd", l["per_pair_usd"], "$", ends_on, None, pv["map_usd_per_pair"], "marketplaces"),
                  _row("listing_price_usd", l["price_usd"], "$", ends_on, None, None, "marketplaces")]
            out.append(_finding("BRN-R15", "high", {"type": "sku", "id": l["asin"], "label": l["title"][:60]}, ev,
                                f"Amazon lists {l['title'][:50]} at ${l['per_pair_usd']:,.2f} a pair, below your ${pv['map_usd_per_pair']:,.2f} minimum.",
                                [l["record"], pv["map_record"]], ends_on, 0.7))
    if pv["counts"]["seller_unknown"] == len(pv["listings"]):
        f = _finding("BRN-R16", "high", {"type": "brand", "id": "seller_unknown", "label": "marketplace sellers"}, [],
                     f"The seller is missing on all {len(pv['listings'])} listings, so an unrecognised seller cannot be seen.", [], ends_on, 0.5)
        f.update(status="unavailable", unavailable={"inputs": ["marketplaces.amazon_listing.seller"], "connector": "Amazon Selling Partner API, or a listing pull with the seller field",
                                                    "fix": "Connect Amazon SP-API in Setup, or re-pull the listings with an actor that returns the seller."})
        out.append(f)
    elif pv["our_sellers"] is None and any(l["seller"] for l in pv["listings"]):
        f = _finding("BRN-R16", "high", {"type": "brand", "id": "sellers_unset", "label": "our seller names"}, [],
                     "Listings carry a seller name but the brain has no list of ours to check against.", [], ends_on, 0.5)
        f.update(status="unavailable", unavailable={"inputs": ["offers.marketplace_seller_names"], "connector": "a founder record on the brand brain screen",
                                                    "fix": "Type your marketplace seller names in the parity block."})
        out.append(f)
    else:
        for l in pv["listings"]:
            fl = next((x for x in l["flags"] if x["key"] == "unrecognised"), None)
            if not fl:
                continue
            ev = [_row("seller_recognised", 0, "flag", ends_on, None, 1, "marketplaces")]
            out.append(_finding("BRN-R16", "high", {"type": "sku", "id": l["asin"], "label": l["title"][:60]}, ev,
                                f"An unrecognised seller, {l['seller']}, is listing {l['title'][:50]} on Amazon.", [l["record"], pv["sellers_record"]], ends_on, 0.7))
    return out


def rule_contracts(brain: Brain, ends_on: str) -> list[dict]:
    out = []
    reg = contracts.register(brain)
    for c in reg["contracts"]:
        k = c["verdict"]["kind"]
        if c["on_file"] and k == "stop":
            ev = [_row("days_to_renewal", c["days_left"], "days", ends_on, None, c["window_days"], "operations"),
                  _row("notice_days", c["notice_days"], "days", ends_on, None, None, "operations")]
            if c["days_left"] is not None and c["days_left"] >= 0:
                sentence = f"{c['vendor']} renews in {c['days_left']} days" + (f"; last terms were {c['rate_card']}" if c["rate_card"] else "") + "."
            else:
                sentence = f"{c['vendor']}'s renewal date passed {-(c['days_left'] or 0)} days ago. It likely auto-renewed on the old terms."
            out.append(_finding("BRN-R17", "high" if c["type"] in ("platform", "3pl", "agency") else "medium",
                                {"type": "brand", "id": f"contract_{c['slug']}", "label": c["vendor"]}, ev, sentence, [c["record"]], ends_on, 0.9))
        elif c["on_file"] and k == "fix":
            ev = [_row("renewal_date_on_file", 0, "flag", ends_on, None, 1, "operations")]
            out.append(_finding("BRN-R18", "low", {"type": "brand", "id": f"contract_{c['slug']}", "label": c["vendor"]}, ev,
                                f"{c['vendor']}'s contract has no renewal date on file and is marked incomplete.", [c["record"]], ends_on, 0.9))
    missing = [c for c in reg["contracts"] if not c["on_file"]]
    if missing:
        ev = [_row("vendors_without_contract", len(missing), "n", ends_on, None, 0, "stack, operations, team")]
        names = ", ".join(c["vendor"] for c in missing[:5]) + (" and more" if len(missing) > 5 else "")
        out.append(_finding("BRN-R18", "medium", {"type": "brand", "id": "contracts_missing", "label": "vendors without a contract on file"}, ev,
                            f"{len(missing)} vendors the brain knows have no contract on file: {names}.", [c["record"] for c in missing[:6]], ends_on, 0.7))
    return out


def rule_legal(brain: Brain, ends_on: str) -> list[dict]:
    out = []
    for c in legal.checks(brain)["checks"]:
        if c["status"] != "fail":
            continue
        ev = [_row("disclosure_present", 0, "flag", ends_on, None, 1, "policies, site_map, stack")]
        out.append(_finding("BRN-R19", "high", {"type": "page", "id": c["key"], "label": c["label"]}, ev,
                            f"{c['label']} is missing ({c['law']}). This blocks going live: {c['why']}.", [e for e in c["evidence"] if "." in e][:3], ends_on, 0.9))
    return out


def rule_assumptions(brain: Brain, bank: list[dict] | None, ends_on: str) -> list[dict]:
    out = []
    rooms = health.rooms_by_section(bank) if bank else {}
    for a in assumptions.register(brain, rooms)["assumptions"]:
        if a["status"] not in ("modelled", "sourced") or not a["rooms"]:
            continue
        ev = [_row("assumption_status_founder", 0, "flag", ends_on, a["age_days"], 1, "assumptions.json"),
              _row("rooms_reading", len(a["rooms"]), "n", ends_on, None, 1, "questions.bank.json")]
        sentence = (f"{a['label']} is {a['status']}, not your number: {a['summary'][:80]}. "
                    f"{len(a['rooms'])} rooms read it: {', '.join(r.replace('_', ' ') for r in a['rooms'][:4])}.")
        out.append(_finding("BRN-R21", "medium" if a["status"] == "modelled" else "low",
                            {"type": "metric", "id": f"assumption_{a['field']}", "label": a["label"]}, ev, sentence, a["source_ids"][:3], ends_on, 0.7))
    return out


def rule_picked_ideas(brain: Brain, ends_on: str) -> list[dict]:
    out = []
    for r in brain.records("plans"):
        v = r.get("value") if isinstance(r.get("value"), dict) else {}
        if not (r.get("field") or "").startswith("idea_") or v.get("status") != "picked":
            continue
        ev = [_row("brief_written", 0, "flag", ends_on, r["age_days"], 1, "plans")]
        sentence = f"You picked idea {v.get('idea_id')}: {str(v.get('title'))[:80]}. No test brief exists yet."
        f = _finding("BRN-R22", "medium", {"type": "brand", "id": f"idea_{(v.get('idea_id') or '').lower().replace('-', '_')}", "label": str(v.get("title"))[:60]},
                     ev, sentence, [r["id"]], ends_on, 0.9)
        f["idea"] = v
        out.append(f)
    return out


def rule_ladder_proof(brain: Brain, ends_on: str) -> list[dict]:
    out = []
    m = ladderproof.matrix(brain)
    for g in m["gaps"]:
        if not g["uses"]:
            continue
        one = g.get("one_star")
        ev = [_row("proof_records", 0, "n", ends_on, None, 1, "objection_ladders"),
              _row("one_star_lines", one, "n", ends_on, None, 10, "objection_ladders"),
              _row("surfaces_used", len(g["uses"]), "n", ends_on, None, 1, "objection_ladders")]
        why = "the proof is a forbidden claim" if g["status"] == "forbidden" else ("its proof ids point at records the brain no longer holds" if g["lost_ids"] else "no proof record is attached")
        sentence = f"Rung {g['level']} of the {g['theme'].replace('_', ' ')} ladder ({g['doubt']}) is used on {len(g['uses'])} surfaces and {why}." + (f" {one} one-star lines sit behind it." if isinstance(one, (int, float)) else "")
        f = _finding("BRN-R23", "medium" if isinstance(one, (int, float)) and one >= 10 else "low",
                     {"type": "brand", "id": f"rung_{g['theme']}_{g['level']}", "label": f"{g['theme'].replace('_', ' ')} rung {g['level']}"},
                     ev, sentence, [g["record"]] + [c["id"] for c in g["candidates"]], ends_on, 0.9)
        f["rung"] = {k: g[k] for k in ("theme", "level", "doubt", "uses", "brief", "candidates", "one_star")}
        out.append(f)
    return out


def rule_visibility(brain: Brain, ends_on: str) -> list[dict]:
    v = visibility.audit(brain)
    if not v["leaks"] and not v["restricted"]:
        return []
    ev = [_row("public_records_from_private_sources", len(v["leaks"]), "n", ends_on, None, 0, "every section"),
          _row("private_records_from_public_sources", len(v["restricted"]), "n", ends_on, None, 0, "every section")]
    parts = []
    if v["leaks"]:
        secs = sorted({x["section"].replace("_", " ") for x in v["leaks"]})
        parts.append(f"{len(v['leaks'])} record{'s' if len(v['leaks']) != 1 else ''} marked public would reach a public-facing agent from {', '.join(secs[:3])}")
    if v["restricted"]:
        parts.append(f"{len(v['restricted'])} public-source record{'s' if len(v['restricted']) != 1 else ''} {'are' if len(v['restricted']) != 1 else 'is'} marked private")
    f = _finding("BRN-R28", "medium" if v["leaks"] else "low", {"type": "brand", "id": "visibility", "label": "public and private flags"}, ev, "; ".join(parts) + ".", [x["id"] for x in (v["leaks"] + v["restricted"])[:6]], ends_on, 0.9)
    f["visibility"] = {"leaks": [{"id": x["id"], "why": x["why"]} for x in v["leaks"][:8]], "restricted": [{"id": x["id"], "why": x["why"]} for x in v["restricted"][:8]]}
    return [f]


def rule_visual(brain: Brain, ends_on: str) -> list[dict]:
    pal = visual.palette(brain)
    gaps = []
    if not pal["available"]:
        gaps.append("no colour token on file")
    if not pal["logo_rules"]["available"]:
        gaps.append("no logo rules on file")
    fails = [p for p in pal["pairs"] if not p["aa"] and not p.get("accent")]
    if fails:
        gaps.append(f"{len(fails)} text and background pair{'s' if len(fails) != 1 else ''} under the 4.5 contrast ratio")
    if not gaps:
        return []
    ev = [_row("colour_tokens", pal["counts"]["colours"], "n", ends_on, None, 1, "visual"), _row("logo_rules", 1 if pal["logo_rules"]["available"] else 0, "flag", ends_on, None, 1, "visual"),
          _row("contrast_pairs_failing", len(fails), "n", ends_on, None, 0, "visual")]
    f = _finding("BRN-R27", "low", {"type": "brand", "id": "visual_identity", "label": "visual identity"}, ev, "The visual identity has gaps: " + ", ".join(gaps) + ".", [c["record"] for c in pal["colours"][:3]], ends_on, 0.9)
    f["visual"] = {"gaps": gaps, "colours": pal["counts"]["colours"], "logo": pal["logo_rules"]["available"], "fails": [f"{p['text']} on {p['background']} ({p['ratio']})" for p in fails[:4]]}
    return [f]


def rule_peaks(brain: Brain, ends_on: str) -> list[dict]:
    out = []
    r = peaks.readiness(brain, market.angles_of, legal, assumptions)
    for p in r["peaks"]:
        gaps = [c for c in p["checks"] if c["status"] == "gap"]
        if not gaps:
            continue
        days = p.get("days_to")
        sev = "high" if days is not None and days <= 30 else ("medium" if days is not None and days <= 60 else "low")
        ev = [_row("days_to_peak", days, "n", ends_on, None, 30, "calendar"), _row("gaps", len(gaps), "n", ends_on, None, 0, "calendar"),
              _row("checks_ok", p["counts"]["ok"], "n", ends_on, None, None, "calendar"), _row("checks_unavailable", p["counts"]["unavailable"], "n", ends_on, None, None, "calendar")]
        when = f"in {days} days" if days is not None else (f"in {p['window']}" if p.get("window") else "with no date yet")
        names = ", ".join(c["label"].lower() for c in gaps[:3]) + (" and more" if len(gaps) > 3 else "")
        f = _finding("BRN-R26", sev, {"type": "brand", "id": f"peak_{p['key']}", "label": p["label"]}, ev,
                     f"{p['label']} is {when} and {len(gaps)} check{'s' if len(gaps) != 1 else ''} wait{'' if len(gaps) != 1 else 's'} on a decision: {names}.", [x for c in gaps for x in c["records"]][:6], ends_on, 0.9 if days is not None else 0.6)
        f["peak"] = {"key": p["key"], "label": p["label"], "date": p.get("date"), "days_to": days, "kind": p["kind"], "gaps": [{k: c[k] for k in ("key", "label", "fix", "who", "capability")} for c in gaps], "unavailable": [c["label"] for c in p["checks"] if c["status"] == "unavailable"]}
        out.append(f)
    return out


def rule_self_audit(brain: Brain, ends_on: str) -> list[dict]:
    out = []
    sa = selfaudit.run(brain)
    drift = [p for p in sa["proposals"] if p["kind"] == "drifted"]
    broken = [p for p in sa["proposals"] if p["kind"] == "broken_link"]
    if drift or broken:
        ev = [_row("router_rows_drifted", len(drift), "n", ends_on, None, 0, "BRAIN.md"), _row("router_links_broken", len(broken), "n", ends_on, None, 0, "BRAIN.md")]
        what = " and ".join(x for x in [f"{len(drift)} row{'s' if len(drift) != 1 else ''} no longer match the records" if drift else "", f"{len(broken)} link{'s' if len(broken) != 1 else ''} point at a missing file" if broken else ""] if x)
        f = _finding("BRN-R24", "low", {"type": "brand", "id": "router", "label": "BRAIN.md router"}, ev, f"BRAIN.md, the router every agent reads first: {what}.", [], ends_on, 0.9)
        f["router"] = {"drifted": [p["target"] for p in drift][:6], "broken": [p["target"] for p in broken][:6]}
        out.append(f)
    dups = sa["duplicates"]
    if dups:
        secs = sorted({d["section"] for d in dups})
        ev = [_row("duplicate_pairs", len(dups), "n", ends_on, None, 0, "every section")]
        f = _finding("BRN-R25", "low", {"type": "brand", "id": "duplicates", "label": "duplicate records"}, ev,
                     f"{len(dups)} pair{'s' if len(dups) != 1 else ''} of records say the same thing in {', '.join(s.replace('_', ' ') for s in secs[:4])}{' and more' if len(secs) > 4 else ''}.",
                     [d["keep"] for d in dups[:6]], ends_on, 0.8)
        f["duplicates"] = dups[:12]
        out.append(f)
    return out


def rule_number_dependents(brain: Brain, ends_on: str) -> list[dict]:
    out = []
    for pl in numbers.pending(brain):
        if not pl["left"]:
            continue
        left = [d for d in pl["dependents"] if not d.get("done")]
        ev = [_row("dependents_left", pl["left"], "n", ends_on, None, 0, "plans"), _row("dependents_total", pl["total"], "n", ends_on, None, None, "plans")]
        sev = "medium" if any(d.get("kind") in ("ad", "snippet") for d in left) else "low"
        f = _finding("BRN-R37", sev, {"type": "brand", "id": f"update_{pl['field']}", "label": f"{pl['field'].replace('_', ' ')} dependents"}, ev,
                     f"{pl['field'].replace('_', ' ')} changed from {pl['before']} to {pl['after']}; {pl['left']} of {pl['total']} places still carry the old value: " + ", ".join(str(d.get('label'))[:40] for d in left[:3]) + ("..." if len(left) > 3 else "") + ".", [pl["plan"], pl["record"]], ends_on, 0.95)
        f["update"] = {"plan": pl["plan"], "field": pl["field"], "before": pl["before"], "after": pl["after"], "left": [{"id": d["id"], "kind": d.get("kind"), "label": d.get("label")} for d in left[:8]]}
        out.append(f)
    return out


def rule_expiring(brain: Brain, ends_on: str) -> list[dict]:
    out = []
    ex = expiring.expiring(brain, health.SHELF_DAYS)
    for g in ex["groups"]:
        ev = [_row("records_expiring", g["records"], "n", ends_on, None, 0, g["source"]), _row("records_expired", g["expired"], "n", ends_on, None, 0, g["source"])]
        f = _finding("BRN-R36", "medium" if g["expired"] else "low", {"type": "brand", "id": f"expiring_{g['source']}", "label": f"{g['source'].replace('_', ' ')} records"}, ev,
                     f"{g['records']} {g['source'].replace('_', ' ')} record{'s' if g['records'] != 1 else ''} in {', '.join(s.replace('_', ' ') for s in g['sections'][:4])}{' and more' if len(g['sections']) > 4 else ''} expire by {ex['window_days']} days from now" + (f", {g['expired']} already past" if g["expired"] else "") + f"; the fix is to {g['refresh']}.", [], ends_on, 0.9)
        f["expiring"] = dict(g, earliest=g["earliest"])
        out.append(f)
    return out


def rule_owners(brain: Brain, ends_on: str) -> list[dict]:
    out = []
    ow = owners.owners(brain, health.SHELF_DAYS, health.META_SECTIONS, brain.section_stats())
    for row in ow["rows"]:
        if row["state"] != "overdue":
            continue
        over = -row["due_in"]
        ev = [_row("days_overdue", over, "n", ends_on, None, 0, "team"), _row("cadence_days", row["cadence_days"], "n", ends_on, None, None, "team")]
        f = _finding("BRN-R35", "medium" if over > row["cadence_days"] else "low", {"type": "brand", "id": f"review_{row['section']}", "label": f"{row['label']} review"}, ev,
                     f"{row['label'].capitalize()} ({row['records']} records) was last {'reviewed' if row['basis'] == 'review' else 'updated'} {row['days_since']} days ago; its cadence is {row['cadence_days']} days" + (f" and its owner is {row['owner']}" if row["owner"] else " and it has no owner") + ".", [row["record"]] if row["record"] else [], ends_on, 0.9)
        f["owner_row"] = {k: row[k] for k in ("section", "label", "owner", "cadence_days", "days_since", "records")}
        out.append(f)
    return out


def rule_redlines(brain: Brain, ends_on: str) -> list[dict]:
    reg = redlines.register(brain)
    n = reg["counts"]["without_reason"]
    if not n:
        return []
    ev = [_row("red_lines_without_reason", n, "n", ends_on, None, 0, "claims"), _row("red_lines", reg["counts"]["total"], "n", ends_on, None, None, "claims")]
    names = "; ".join(str(x["text"])[:40] for x in reg["lines"] if not x["why"] and x["editable"])[:160]
    f = _finding("BRN-R34", "low", {"type": "brand", "id": "red_lines", "label": "red lines register"}, ev, f"{n} of {reg['counts']['total']} red lines have no reason on file: {names}.", [x["record"] for x in reg["lines"] if not x["why"]][:6], ends_on, 0.9)
    f["redlines"] = {"without_reason": [{"record": x["record"], "text": x["text"], "kind": x["kind"]} for x in reg["lines"] if not x["why"] and x["editable"]][:10]}
    return [f]


def rule_audiences(brain: Brain, ends_on: str) -> list[dict]:
    a = audiences.profiles(brain, ladderproof)
    if not a["profiles"]:
        return []
    gaps = []
    if not a["counts"]["approved"]:
        gaps.append(f"none of the {a['counts']['profiles']} profiles is approved")
    if "ads" not in a["defaults"]:
        gaps.append("no default profile for ads")
    if not gaps:
        return []
    ev = [_row("profiles_approved", a["counts"]["approved"], "n", ends_on, None, 1, "avatars"), _row("defaults_set", a["counts"]["defaults_set"], "n", ends_on, None, 1, "avatars")]
    f = _finding("BRN-R33", "low", {"type": "brand", "id": "audiences", "label": "audience profiles"}, ev, "Generators write for no one in particular: " + " and ".join(gaps) + ".", [p["id"] for p in a["profiles"][:3]], ends_on, 0.9)
    f["audiences"] = {"top": [{"id": p["id"], "name": p["name"], "share": p["share"]} for p in a["profiles"][:3]], "gaps": gaps}
    return [f]


def rule_drift(brain: Brain, ends_on: str) -> list[dict]:
    d = drift.analysis(brain)
    if not d.get("available") or not d.get("drift"):
        return []
    ev = [_row("praise_echo_share", d["echo_share"], "share", ends_on, None, d["echo_floor"], "language_bank"), _row("contradicted_words", len(d["contradicted"]), "n", ends_on, None, 0, "language_bank")]
    parts = []
    if d["echo_share"] is not None and d["echo_share"] < d["echo_floor"]:
        parts.append(f"only {round(d['echo_share'] * 100)} percent of {d['counts']['praise_quotes']} praise quotes echo the positioning's words")
    if d["contradicted"]:
        parts.append("complaints contradict " + ", ".join(d["contradicted"]))
    f = _finding("BRN-R32", "low", {"type": "brand", "id": "positioning_drift", "label": "positioning frame"}, ev, "Positioning drift: " + "; ".join(parts) + ".", [x["record"] for x in d["sources"]][:4], ends_on, 0.7)
    f["drift"] = {"brief": d["brief"], "missing": d["missing"], "contradicted": d["contradicted"], "echo_share": d["echo_share"]}
    return [f]


def rule_consents(brain: Brain, ends_on: str) -> list[dict]:
    out = []
    for c in ugc.register(brain)["consents"]:
        if c["state"] not in ("expired", "expiring"):
            continue
        ev = [_row("days_left", c["days_left"], "n", ends_on, None, ugc.WINDOW_DAYS, "content")]
        why = f"the consent expired on {c['expires_on']}" if c["state"] == "expired" else f"the consent ends on {c['expires_on']}, {c['days_left']} days away"
        f = _finding("BRN-R31", "medium" if c["state"] == "expired" else "low", {"type": "brand", "id": f"consent_{c['key']}", "label": f"consent from {c['name']}"}, ev,
                     f"{c['name']}'s consent to use \"{str(c['what'])[:60]}\"" + (f" on {', '.join(c['scope'])}" if c["scope"] else "") + f": {why}.", [c["record"]], ends_on, 0.95)
        f["consent"] = {k: c[k] for k in ("key", "name", "handle", "channel", "what", "scope", "state", "days_left", "expires_on")}
        out.append(f)
    return out


def rule_assets(brain: Brain, ends_on: str) -> list[dict]:
    out = []
    for a in assets.register(brain)["assets"]:
        if not a.get("action"):
            continue
        sev = {"expired_live": "high", "inside_window": "medium"}.get(a["state"], "low")
        ev = [_row("days_left", a["days_left"], "n", ends_on, None, a["window_days"], "content"), _row("live", 1 if a["live"] else 0, "flag", ends_on, None, None, "content")]
        why = {"expired_live": f"the right expired on {a['expires_on']} and it is still live", "inside_window": f"the right ends on {a['expires_on']}, {a['days_left']} days away", "no_date": "no expiry date is on file", "bad_date": "the expiry date is unreadable"}[a["state"]]
        f = _finding("BRN-R30", sev, {"type": "brand", "id": f"asset_{a['key']}", "label": a["name"]}, ev, f"{a['name']} ({a['kind']}, {', '.join(a['where']) or 'use not on file'}): {why}.", [a["record"]], ends_on, 0.95)
        f["asset"] = {k: a[k] for k in ("key", "name", "kind", "state", "days_left", "expires_on", "where", "rights_holder", "action")}
        out.append(f)
    return out


def rule_rejected_due(brain: Brain, ends_on: str) -> list[dict]:
    out = []
    for v in bottlenecks.rejected_ideas(brain).values():
        if not v["due"]:
            continue
        ev = [_row("days_past_review", -(v["days_to_review"] or 0), "n", ends_on, None, 0, "learnings")]
        f = _finding("BRN-R29", "low", {"type": "brand", "id": f"rejected_{v['idea_id'].lower().replace('-', '_')}", "label": f"rejected idea {v['idea_id']}"}, ev,
                     f"You rejected idea {v['idea_id']} ({str(v.get('title'))[:60]}) on {v.get('rejected_on') or 'an earlier date'}" + (f" because {v['reason']}" if v.get("reason") else "") + f"; the review date {v['review_on']} has passed.", [v["record"]], ends_on, 0.9)
        f["rejected"] = v
        out.append(f)
    return out


def rule_permissions(brain: Brain, ends_on: str) -> list[dict]:
    pm = health.permissions(brain)
    unset = [s for s in pm["sections"] if not s["explicit"] and s["records"]]
    if not unset:
        return []
    ev = [_row("sections_without_permission_entry", len(unset), "n", ends_on, None, 0, "team"),
          _row("permission_coverage_pct", pm["counts"]["coverage_pct"], "share", ends_on, None, 1, "team")]
    names = ", ".join(s["label"] for s in unset[:4]) + (" and more" if len(unset) > 4 else "")
    return [_finding("BRN-R20", "low", {"type": "brand", "id": "permissions_unset", "label": "permission map"}, ev,
                     f"{len(unset)} sections have no permission entry and default to restricted: {names}.", [], ends_on, 0.9)]


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
    out = rule_stale(brain, ends_on) + rule_claims(brain, ends_on) + rule_competitor_gaps(brain, ends_on) + rule_angle_gaps(brain, ends_on) + rule_signals(brain, ends_on) + rule_weak_sections(brain, ends_on) + rule_conflicts(brain, ends_on) + rule_untiered_claims(brain, ends_on) + rule_site_changes(brain, ends_on) + rule_parity(brain, ends_on) + rule_contracts(brain, ends_on) + rule_legal(brain, ends_on) + rule_picked_ideas(brain, ends_on) + rule_ladder_proof(brain, ends_on) + rule_self_audit(brain, ends_on) + rule_peaks(brain, ends_on) + rule_visual(brain, ends_on) + rule_visibility(brain, ends_on) + rule_rejected_due(brain, ends_on) + rule_assets(brain, ends_on) + rule_consents(brain, ends_on) + rule_drift(brain, ends_on) + rule_audiences(brain, ends_on) + rule_redlines(brain, ends_on) + rule_owners(brain, ends_on) + rule_expiring(brain, ends_on) + rule_number_dependents(brain, ends_on) + rule_permissions(brain, ends_on) + rule_snapshot_stale(brain, ends_on)
    if bank is None:
        for rid, sev in (("BRN-R02", "medium"), ("BRN-R03", "medium")):
            f = _finding(rid, sev, {"type": "brand", "id": "question_bank", "label": "question bank"},
                         [], "The question bank could not be read.", [], ends_on)
            f.update(status="unavailable", unavailable={"inputs": ["app/brain/questions.bank.json"],
                     "connector": "none, a repo file", "fix": "Restore questions.bank.json."})
            out.append(f)
    else:
        out += rule_empty(brain, bank, ends_on) + rule_questions(brain, bank, ends_on) + rule_assumptions(brain, bank, ends_on)
    out.sort(key=lambda f: (SEVERITY_ORDER[f["severity"]], f["id"]))
    return out


if __name__ == "__main__":
    b = sys.argv[1] if len(sys.argv) > 1 else "bombas"
    print(json.dumps(run(b), indent=1))
