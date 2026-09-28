"""Brand brain screen API: /api/05-brand-brain/...

Reads app/brain/<brand>/ through app/brain/store.py and keeper.py. The only
writes go through Brain.put and Brain.retire: a founder answer to an open
question, and accept or ignore on a proposed record. Nothing external.

  GET  agentfile?capability=    the brain file an agent reads for one capability: strict rules,
                                judgement rules, the package, where to check (markdown)
  GET  agentfile/endpoints      this route table as JSON, for an agent or an MCP wrapper
  GET  brainmd                  the router BRAIN.md text
  GET  trail?days=7             who read what: section reads by reader, facts handed to agents, private facts to public readers
  POST export/diff              {bundle | content_base64}: what changed since that export, record by record
  POST export/diff/start|part|finish  the same export in 24 KB base64 parts (the server takes 32 KB a request)
  POST review/draft             {text, channel, kind}: every check in one call and the route
  GET  overview                 T0 card, section table, tiles, insights, chart, ladders,
                                open questions, review queue, conflicts
  GET  master?window=28d        the orchestrator's master list: every screen's rank merged
                                (app/rank.py): top 10 to approve, connect strip, bottlenecks
  GET  profile                  the editable brand profile: one winning record per field in
                                identity, positioning, voice, visual, products, offers,
                                policies, claims, with tier, source, date and where it flows
  POST profile/<section>/<field> {text}: writes an approved founder record that wins the merge
  GET  documents                the documents manifest with what each file changed
  POST documents                {name, text | content_base64 | url, note}: stores the file
                                under documents/ and adds a manifest line; never blocked
  GET  competitors              the Ad Library pages against the brand: format and hook mix per page,
                                competitor medians, the gaps, proposed pages, and the cost of a re-pull
  GET  coverage                 angles by page: our ad count per angle against each competitor page, gaps with a
                                drafted concept brief, our own ground, contested angles
  GET  signals                  what buyers say elsewhere: recommended-instead per competitor with the doubt behind
                                it, our proof status and where to answer; category frames against our frame; the
                                competitor sets; proposed pages waiting on a page id
  POST competitors/page-id      {name, page_id}: writes an approved founder record competitors.page_id_<slug>;
                                the page joins the page list and the next pull estimate
  GET  health                   freshness by confidence: sections by tier with counts, freshness, the one action
                                per section (connect, ask the founder, re-crawl), and the connectors
  GET  health/cell?section=&tier=  the records in one heatmap cell, best first
  POST approve/<record id>      {choice: approve | forbid}: the founder settles a record; it becomes an approved
                                (or forbidden) founder record with the old tier in history
  GET  conflicts                open and settled conflicts with the default winner named and who reads the field
  POST conflicts/<id>           {record_id | index | text, reason}: the founder decides; writes an approved founder
                                record for the field, marks the conflict resolved, logs a decisions record
  GET  questions                every open question ranked by weight times rooms unblocked, with the pull-first
                                hint, the fields an answer fills and the screens it unblocks
  POST questions/bank/<qid>     {answer}: answers a bank question with an approved founder record on its first field
  GET  decisions                the decisions timeline: action decisions from every screen plus the brain's
                                decisions section, newest first
  POST documents/extract        {name}: re-read a stored text or markdown file into proposed records
  GET  rank                     this screen's ranked actions with real titles, steps, artefacts and drafts (ranking.py);
                                served by app/rank.py through the `rank(brand, window)` export below
  GET  flows                    which screens read each profile section (a scan of their code plus the store's read
                                log), when a founder last edited it and when it was last read; `profile`, `records`
                                and `package` stamp the read log when the caller names itself with ?reader=
  GET  claims                   the claims desk: every claim with tier, category, source, where the ladders use it,
                                the verdict, tier counts and the forbidden phrases
  POST claims                   {text, tier: approved | forbidden}: add a claim or forbid a phrase (founder record)
  POST scan                     {text, channel?}: check a draft against the brain (forbidden phrases, unproven
                                absolutes, stale numbers, unapproved claims, avoid list, reading grade) and, with a
                                channel (amazon, meta, google, email, sms), that channel's rule set
  GET  site/diff                changes between the two newest site snapshots, each with its action; one snapshot
                                reads unavailable with the reason
  POST site/snapshot            store the crawl on file as a snapshot (after each site crawl)
  POST site/reviewed            {ids}: mark changes reviewed for the current pair
  GET  parity                   marketplace listings against the site: price per pair, site floor, MAP, seller,
                                flags with actions; MAP and seller names unavailable until the founder sets them
  POST parity/map               {usd}: the minimum advertised price per pair, an approved founder record in offers
  POST parity/sellers           {names}: the seller names that are ours, an approved founder record in offers
  GET  contracts                the vendor contract register: on file, inside the window, no date, known vendors
                                without a contract; the renewal calendar
  POST contracts                {vendor, type, renewal_date, notice_days, rate_card, sla_terms}: a founder record
                                operations.contract_<vendor>
  GET  legal                    the US disclosure checks read from the brain: pass, fail, unavailable, n/a
  POST legal/gate               {kind: email | ad | pdp | policy | subscription, text}: gate a pasted draft
  GET  voice                    the voice sheet: fields, liked and disliked examples, lines from our own pages, the
                                copy-ready sheet text; and the approved snippets with a stale check
  POST voice/example            {kind: liked | disliked, text, why}: a founder example record
  POST voice/snippet/<key>      {text}: lock the exact wording of a snippet as an approved record
  GET  battlecards              one card per tracked competitor: their angles, where they beat us, the doubt they
                                exploit, our proof, how we win, CX and copy lines, plain text to copy
  GET  ask?q=                   answers from records with tier, source and date; "can we say" routes to the claims
  POST ask/open                 {q, why}: save an unanswered question as an open question
  GET  permissions              sections by role (founder, in-house, agency, specialist), restricted by default
  POST permissions/<section>    {roles: {role: full | read | none}}: a founder record team.permission_<section>
  GET  export                   the whole brain as one portable JSON (records, manifest, router, conflicts)
  GET  changes                  the changes log (every write through this screen and every site change), newest
                                first, with counts for the week and the version steps
  GET  dependents?record=<id>   what depends on one fact: records, ladder rungs, questions, snippets, ads
  GET  assumptions              the register: the numbers the simulation runs on, status, unit, as of, rooms
  POST assumptions/<field>      {choice: confirm} or {value}: an approved founder record on the source id
  GET  facts                    store facts for AI shopping agents: question and answer pairs built from records,
                                proposed, approved, stale or unavailable
  POST facts/<key>              {answer, question?}: approve the wording as content.faq_<key>
  GET  facts/export             FAQPage JSON-LD and plain text of the approved pairs
  GET  summaries                what an agent reads first: the T1 summary per section with its token count
  GET  package?capability=<id>  the package a capability gets (T0, T1, T2) with tokens against its budget
  GET  learn                    words the founder cut or added across their edits, proposed for the voice sheet
  POST learn/apply              {kind: avoided | used, words: [...]}: append to voice.words_avoided or words_used
  GET  report?days=7            the weekly brain report in plain words: changes, decisions, questions, conflicts,
                                site, files, competitors, health, top moves
  GET  digest                   the founder round: 5 questions with hints, proposed updates, one health line, the
                                top 3 moves; delivery unavailable until a Slack or email connector exists
  GET  review                   the review queue grouped by source, each proposal with the record it would replace
  POST review/bulk              {choice: accept | ignore, ids}: clear many proposals at once
  GET  bottlenecks              the diagnosis's bottlenecks with the master-list items that address each and the
                                idea bank's best unlocks for it, ranked in code; strengths and the test queue
  POST bottlenecks/pick         {idea_id, bottleneck, why}: pick an idea; it becomes a plans record and a test brief
                                on the master list
  GET  records?section=<name>   one section's records with tier, date, source and evidence
  GET  audit                    findings from audit.py (app/contracts/audit.md shape)
  POST questions/<field>        {answer}: writes a founder record, marks the question answered
  POST review/<record id>       {choice: accept | ignore}

Query `brand` (default bombas) and `today` (YYYY-MM-DD, default the real date)
work on every route. Set BRAIN_ROOT to point at a copy of app/brain (tests do).
"""
from __future__ import annotations

import base64
import datetime as dt
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parents[1]
if str(APP / "brain") not in sys.path:
    sys.path.insert(0, str(APP / "brain"))

import keeper  # noqa: E402
import package as package_mod  # noqa: E402
from package import t0_card  # noqa: E402
from store import SECTIONS, Brain  # noqa: E402

BRAIN_ROOT: Path | None = None
SAFE_BRAND = re.compile(r"^[a-z0-9_-]+$")
QUESTION_ROUND_AT = 4
CHART_DAYS = 30
SIMULATED_NOTE = ("Bombas is the sample brand. Brain records come from public sources. "
                  "Every sales and ad number in ecomOS is simulated.")
GENERIC_NOTE = "Brain records come from public sources and the founder. Every sales and ad number in ecomOS is simulated until a store connects."
META_SECTIONS = {"freshness", "open_questions", "changes"}

_spec = importlib.util.spec_from_file_location("brand_brain_audit", HERE / "audit.py")
audit = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(audit)
_hspec = importlib.util.spec_from_file_location("brand_brain_health", HERE / "health.py")
health = importlib.util.module_from_spec(_hspec)
_hspec.loader.exec_module(health)
_ospec = importlib.util.spec_from_file_location("brand_brain_bottlenecks", HERE / "bottlenecks.py")
bottlenecks = importlib.util.module_from_spec(_ospec)
_ospec.loader.exec_module(bottlenecks)
_rpspec = importlib.util.spec_from_file_location("brand_brain_report", HERE / "report.py")
report = importlib.util.module_from_spec(_rpspec)
_rpspec.loader.exec_module(report)
_nspec = importlib.util.spec_from_file_location("brand_brain_learn", HERE / "learn.py")
learn = importlib.util.module_from_spec(_nspec)
_nspec.loader.exec_module(learn)
_fspec = importlib.util.spec_from_file_location("brand_brain_facts", HERE / "facts.py")
facts = importlib.util.module_from_spec(_fspec)
_fspec.loader.exec_module(facts)
_uspec = importlib.util.spec_from_file_location("brand_brain_assumptions", HERE / "assumptions.py")
assumptions = importlib.util.module_from_spec(_uspec)
_uspec.loader.exec_module(assumptions)
_gspec = importlib.util.spec_from_file_location("brand_brain_changes", HERE / "changes.py")
changes = importlib.util.module_from_spec(_gspec)
_gspec.loader.exec_module(changes)
_bspec = importlib.util.spec_from_file_location("brand_brain_battlecards", HERE / "battlecards.py")
battlecards = importlib.util.module_from_spec(_bspec)
_bspec.loader.exec_module(battlecards)
_aspec = importlib.util.spec_from_file_location("brand_brain_ask", HERE / "ask.py")
ask = importlib.util.module_from_spec(_aspec)
_aspec.loader.exec_module(ask)
_vspec = importlib.util.spec_from_file_location("brand_brain_voice", HERE / "voice.py")
voice = importlib.util.module_from_spec(_vspec)
_vspec.loader.exec_module(voice)
_tspec = importlib.util.spec_from_file_location("brand_brain_contracts", HERE / "contracts.py")
contracts = importlib.util.module_from_spec(_tspec)
_tspec.loader.exec_module(contracts)
_lspec = importlib.util.spec_from_file_location("brand_brain_legal", HERE / "legal.py")
legal = importlib.util.module_from_spec(_lspec)
_lspec.loader.exec_module(legal)
_pspec = importlib.util.spec_from_file_location("brand_brain_parity", HERE / "parity.py")
parity = importlib.util.module_from_spec(_pspec)
_pspec.loader.exec_module(parity)
_sspec = importlib.util.spec_from_file_location("brand_brain_sitediff", HERE / "sitediff.py")
sitediff = importlib.util.module_from_spec(_sspec)
_sspec.loader.exec_module(sitediff)
_trspec = importlib.util.spec_from_file_location("brand_brain_trail", HERE / "trail.py")
trail = importlib.util.module_from_spec(_trspec)
_trspec.loader.exec_module(trail)
_bdspec = importlib.util.spec_from_file_location("brand_brain_braindiff", HERE / "braindiff.py")
braindiff = importlib.util.module_from_spec(_bdspec)
_bdspec.loader.exec_module(braindiff)
_afspec = importlib.util.spec_from_file_location("brand_brain_agentfile", HERE / "agentfile.py")
agentfile = importlib.util.module_from_spec(_afspec)
_afspec.loader.exec_module(agentfile)
_rvspec = importlib.util.spec_from_file_location("brand_brain_reviewer", HERE / "reviewer.py")
reviewer = importlib.util.module_from_spec(_rvspec)
_rvspec.loader.exec_module(reviewer)
_mvspec = importlib.util.spec_from_file_location("brand_brain_moves", HERE / "moves.py")
moves = importlib.util.module_from_spec(_mvspec)
_mvspec.loader.exec_module(moves)
_vbspec = importlib.util.spec_from_file_location("brand_brain_visibility", HERE / "visibility.py")
visibility = importlib.util.module_from_spec(_vbspec)
_vbspec.loader.exec_module(visibility)
_nbspec = importlib.util.spec_from_file_location("brand_brain_newbrand", HERE / "newbrand.py")
newbrand = importlib.util.module_from_spec(_nbspec)
_nbspec.loader.exec_module(newbrand)
_vispec = importlib.util.spec_from_file_location("brand_brain_visual", HERE / "visual.py")
visual = importlib.util.module_from_spec(_vispec)
_vispec.loader.exec_module(visual)
_yspec = importlib.util.spec_from_file_location("brand_brain_history", HERE / "history.py")
history = importlib.util.module_from_spec(_yspec)
_yspec.loader.exec_module(history)
_qspec = importlib.util.spec_from_file_location("brand_brain_peaks", HERE / "peaks.py")
peaks = importlib.util.module_from_spec(_qspec)
_qspec.loader.exec_module(peaks)
_xspec = importlib.util.spec_from_file_location("brand_brain_selfaudit", HERE / "selfaudit.py")
selfaudit = importlib.util.module_from_spec(_xspec)
_xspec.loader.exec_module(selfaudit)
_dspec = importlib.util.spec_from_file_location("brand_brain_ladderproof", HERE / "ladderproof.py")
ladderproof = importlib.util.module_from_spec(_dspec)
_dspec.loader.exec_module(ladderproof)
_cspec = importlib.util.spec_from_file_location("brand_brain_claims", HERE / "claims.py")
claims_mod = importlib.util.module_from_spec(_cspec)
_cspec.loader.exec_module(claims_mod)
_kspec = importlib.util.spec_from_file_location("brand_brain_ranking", HERE / "ranking.py")
ranking = importlib.util.module_from_spec(_kspec)
_kspec.loader.exec_module(ranking)
_ispec = importlib.util.spec_from_file_location("brand_brain_ingest", HERE / "ingest.py")
ingest = importlib.util.module_from_spec(_ispec)
_ispec.loader.exec_module(ingest)
_mspec = importlib.util.spec_from_file_location("brand_brain_market", HERE / "market.py")
market = importlib.util.module_from_spec(_mspec)
_mspec.loader.exec_module(market)
_rspec = importlib.util.spec_from_file_location("ecomos_rank_bb", APP / "rank.py")
rank_mod = importlib.util.module_from_spec(_rspec)
_rspec.loader.exec_module(rank_mod)

# the editable profile: sections in reading order, the fields a founder edits first, and where each section flows
PROFILE_SECTIONS = [
    ("identity", "Identity", ["category", "one_line_pitch", "giving_model", "founded", "headquarters", "certification_bcorp"]),
    ("positioning", "Positioning", ["frame", "category_frame", "price_frame", "competitive_frame", "proof_points"]),
    ("voice", "Voice", ["adjectives", "writes_like", "do_list", "do_not_list", "tone_by_context", "reading_level", "words_used", "words_avoided"]),
    ("visual", "Visual", []),
    ("products", "Products", ["lines", "price_ladder_socks", "pack_sizes", "materials"]),
    ("offers", "Offers", ["free_shipping_threshold_usd", "standard_shipping_cost", "guarantee", "first_order_code", "bundles_pack_ladder"]),
    ("policies", "Policies", ["returns_window_days", "refund_method", "happiness_guarantee", "exchanges", "shipping_options"]),
    ("claims", "Claims", []),
]
FLOWS_TO = {"identity": "every screen", "positioning": "market research, customers, competitors, offers, creative, copy, landing pages, SEO, answer engines",
            "voice": "copy, creative, email, organic, CX", "visual": "creative, landing pages, organic",
            "products": "offers, creative, copy, Google Ads, marketplaces, supply, SEO", "offers": "paid social, Google Ads, email, landing pages, finance",
            "policies": "CX, store health, landing pages, security", "claims": "copy, creative, landing pages, answer engines, marketplaces"}
TIER_RANK = {"approved": 0, "site_backed": 1, "reported": 2, "evidence": 3, "inferred": 4, "unverified": 5, "forbidden": 6}
DOC_MAX_BYTES = 5 * 1024 * 1024
SAFE_FILE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 ._()-]{0,120}$")


def _brain(req) -> Brain:
    brand = req.arg("brand", "bombas")
    if not SAFE_BRAND.match(brand):
        raise ValueError("bad brand")
    t = req.arg("today")
    today = dt.date.fromisoformat(t) if t else dt.date.today()
    return Brain(brand, BRAIN_ROOT, today)


def _source(r: dict) -> dict:
    s = r.get("source") or {}
    ref = s.get("ref") or ""
    return {"type": s.get("type") or "none", "ref": ref, "link": ref if ref.startswith("http") else None}


def record_view(r: dict) -> dict:
    return {"id": r["id"], "field": r.get("field"), "text": r.get("text") or (
                r["value"] if isinstance(r.get("value"), str) else json.dumps(r.get("value"))[:300]),
            "tier": r["tier"], "status": r["status"], "date": r["date"], "age_days": r["age_days"],
            "confidence": r["confidence"], "visibility": r["visibility"], "source": _source(r),
            "evidence": [{"quote": e.get("quote"), "ref": e.get("ref")} for e in (r.get("evidence") or [])]}


def section_table(brain: Brain) -> list[dict]:
    stats = brain.section_stats()
    out = []
    for sec in SECTIONS:
        st = stats[sec]
        confs = [r["confidence"] for r in brain.records(sec) if isinstance(r["confidence"], (int, float))]
        age = (brain.today - dt.date.fromisoformat(st["last_update"])).days if st["last_update"] else None
        out.append({"section": sec, "records": st["count"], "last_update": st["last_update"],
                    "freshness_days": age, "stale": st["stale"],
                    "confidence": round(sum(confs) / len(confs), 2) if confs else None,
                    "meta": sec in META_SECTIONS})
    return out


def open_questions(brain: Brain, bank: list[dict]) -> list[dict]:
    out = []
    for oq in brain.records("open_questions"):
        v = oq.get("value") or {}
        out.append({"id": oq["id"], "field": oq["field"], "question": v.get("question") or oq.get("text"),
                    "section": v.get("section"), "why": v.get("why"), "who_can_answer": v.get("who_can_answer"),
                    "answered_on": v.get("answered_on"), "answer_record": v.get("answer_record"),
                    "weight": audit.question_weight(oq, bank)})
    out.sort(key=lambda q: (bool(q["answered_on"]), -q["weight"], q["field"]))
    return out


def _conflict_rows(brain: Brain) -> list[dict]:
    path = brain.dir / "review" / "conflicts.json"
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    except (OSError, ValueError):
        return []


def conflicts(brain: Brain) -> list[dict]:
    return [c for c in _conflict_rows(brain) if c.get("status", "open") == "open"]


ROOM_SCREEN = {"today": "00-today", "research": "01-market-research", "avatars": "02-customers-avatars", "competitors": "03-competitors",
               "offers": "04-offers-pricing", "brand": "05-brand-brain", "store_health": "06-store-health", "cro": "07-landing-pages-cro",
               "speed": "08-site-speed", "creative": "09-creative", "copy": "10-copy", "paid_social": "11-paid-social", "google_ads": "12-google-ads",
               "affiliates": "13-affiliate-marketplace-ads", "email": "14-email-messaging", "cx": "15-customers-cx", "organic": "16-organic-content",
               "seo": "17-seo", "answer_engines": "18-answer-engines", "supply": "19-supply-inventory", "marketplaces": "20-marketplaces",
               "finance": "21-finance-cash", "measurement": "22-measurement", "team_ops": "23-team-ops", "security": "24-security",
               "experiments": "25-experiments", "reports": "26-reports", "wild_bets": "27-wild-bets-pr", "orchestrator": "05-brand-brain"}


DECISIONS_PATH = APP / "data" / "decisions.json"


def _decisions_path(req) -> Path:
    """Tests point the log at a temp file with ?decisions=<path> under the temp brain root; the app never does."""
    p = req.arg("decisions")
    if p and BRAIN_ROOT is not None and str(Path(p).resolve()).startswith(str(Path(BRAIN_ROOT).resolve())):
        return Path(p)
    return DECISIONS_PATH


def decisions_log(brain: Brain, path: Path | None = None) -> dict:
    """The decisions timeline: action decisions from data/decisions.json (any screen) plus the brain's decisions section.

    Each action decision carries whether it is the current one for its finding (a later row supersedes it), and a
    snooze carries its expiry (time plus rank's SNOOZE_DAYS), the days left, and whether it has expired and the action
    is back on the list. An `undo` row (this screen's fallback, see decisions_undo) clears the decision before it."""
    path = path or DECISIONS_PATH
    try:
        rows = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    except (OSError, ValueError):
        rows = []
    snooze_days = getattr(rank_mod, "SNOOZE_DAYS", 14)
    rows = [r for r in (rows if isinstance(rows, list) else []) if isinstance(r, dict)]
    latest: dict = {}
    for i, r in enumerate(rows):
        latest[r.get("finding_id") or (r.get("screen"), r.get("capability"))] = i
    items = []
    for i, r in enumerate(rows):
        key = r.get("finding_id") or (r.get("screen"), r.get("capability"))
        day = str(r.get("time") or "")[:10]
        it = {"kind": "action", "time": r.get("time"), "date": day, "screen": r.get("screen"), "capability": r.get("capability"),
              "choice": r.get("choice"), "reason": r.get("reason") or "", "finding_id": r.get("finding_id"), "autonomy": r.get("autonomy"),
              "current": latest.get(key) == i, "superseded": latest.get(key) != i, "expires_on": None, "days_left": None, "expired": False}
        if r.get("choice") == "not_now":
            try:
                exp = dt.date.fromisoformat(day) + dt.timedelta(days=snooze_days)
                it["expires_on"] = exp.isoformat()
                it["days_left"] = (exp - brain.today).days
                it["expired"] = it["days_left"] <= 0
            except ValueError:
                pass
        items.append(it)
    for r in brain.records("decisions"):
        src = r.get("source") or {}
        items.append({"kind": "brain", "id": r["id"], "date": None if r["date"] == "undated" else r["date"], "time": None,
                      "title": (r.get("field") or "").replace("_", " "), "text": r.get("text") or "", "who": src.get("ref") or src.get("type") or "founder", "tier": r["tier"]})
    items.sort(key=lambda it: (it.get("time") or it.get("date") or ""), reverse=True)
    cur = [it for it in items if it["kind"] == "action" and it["current"]]
    active_snoozes = [it for it in cur if it["choice"] == "not_now" and not it["expired"]]
    counts = {"action": sum(1 for it in cur if it["choice"] in ("agent", "person")),
              "snoozed": len(active_snoozes),
              "expiring": sum(1 for it in active_snoozes if it["days_left"] is not None and it["days_left"] <= 3),
              "expired": sum(1 for it in cur if it["choice"] == "not_now" and it["expired"]),
              "undone": sum(1 for it in cur if it["choice"] == "undo"),
              "superseded": sum(1 for it in items if it["kind"] == "action" and it["superseded"]),
              "brain": sum(1 for it in items if it["kind"] == "brain")}
    return {"items": items, "counts": counts, "snooze_days": snooze_days, "last": items[0].get("time") or items[0].get("date") if items else None,
            "note": f"A snooze hides an action for {snooze_days} days, then it is back on the list. A later decision on the same action supersedes the earlier one; the log keeps both. Undo appends a clearing row, it never deletes."}


def decisions_undo(brain: Brain, body: dict, path: Path | None = None):
    """Local fallback for an undo: append a row with choice `undo` to data/decisions.json for the finding, so rank's
    latest-row-wins reading no longer snoozes or marks it decided. The server's POST /api/decisions refuses the choice
    (CHOICES has no undo yet; contract ask in FEATURES.md), so this screen writes the same file the same way."""
    path = path or DECISIONS_PATH
    fid = str((body or {}).get("finding_id") or "")
    if not fid or len(fid) > 200 or not re.fullmatch(r"[A-Za-z0-9_.:\- /]+", fid):
        return 400, {"error": "finding_id must be an action id"}
    try:
        rows = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    except (OSError, ValueError):
        rows = []
    rows = rows if isinstance(rows, list) else []
    last = next((r for r in reversed(rows) if isinstance(r, dict) and r.get("finding_id") == fid), None)
    if last is None:
        return 404, {"error": "no decision on that action", "finding_id": fid}
    if last.get("choice") == "undo":
        return 400, {"error": "already undone", "finding_id": fid}
    row = {"screen": "05-brand-brain", "capability": str(last.get("capability") or "")[:80], "choice": "undo", "reason": str((body or {}).get("reason") or "")[:300],
           "time": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "finding_id": fid, "undoes": {"choice": last.get("choice"), "time": last.get("time")}}
    rows.append(row)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(rows, indent=1), encoding="utf-8")
        tmp.replace(path)
    except OSError as e:
        return 500, {"error": f"could not write the decisions log: {e}"}
    changes.log(brain, "decision", None, None, f"undid the {str(last.get('choice')).replace('_', ' ')} decision on {fid}")
    return 201, {"ok": True, "finding_id": fid, "undid": row["undoes"], "next": "The action is back on the list with no decision. The log keeps both rows."}


def questions_ranked(brain: Brain) -> dict:
    """Every open question in one list: the brain's own open_questions plus the bank questions no connected source answers.
    Ranked by weight times rooms unblocked. Each carries the pull-first hint and the fields an answer fills."""
    bank = keeper.load_bank()
    try:
        registry = keeper.load_registry()
    except (OSError, ValueError, KeyError):
        registry = {}
    rooms_by_sec = {}
    for q in bank:
        for f in q["fills"]:
            rooms_by_sec.setdefault(f.split(".")[0], set()).update(q["unblocks_rooms"])
    out = []
    for q in open_questions(brain, bank):
        rooms = sorted(rooms_by_sec.get(q["section"], set()))
        out.append({"id": q["id"], "kind": "brain", "field": q["field"], "question": q["question"], "why": q["why"], "section": q["section"],
                    "fills": [f"{q['section']}.{q['field']}"], "rooms": rooms, "screens": sorted({ROOM_SCREEN.get(r, r) for r in rooms}),
                    "weight": q["weight"], "importance": q["weight"] * max(1, len(rooms)), "connect": [],
                    "hint": f"Only {q['who_can_answer'] or 'the founder'} can answer this. One line is enough; a proof link is better.",
                    "who": q["who_can_answer"], "answered_on": q["answered_on"], "answer_record": q["answer_record"]})
    for a in keeper.ask(brain, n=50, bank=bank, registry=registry):
        rooms = a["rooms"]
        connect = [{"id": s, "name": registry.get(s, {}).get("name", s), "category": registry.get(s, {}).get("category")} for s in a["connect"]]
        first = a["fills"][0]
        sec = first.split(".")[0]
        out.append({"id": a["id"], "kind": "bank", "field": first.split(".", 1)[1] if "." in first else f"founder_{a['id'].split('.')[-1]}",
                    "question": a["asks"], "why": a["why"], "section": sec, "fills": a["fills"], "rooms": rooms,
                    "screens": sorted({ROOM_SCREEN.get(r, r) for r in rooms}), "weight": a["weight"], "importance": a["importance"],
                    "connect": connect, "hint": (f"Pull first: connect {' or '.join(c['name'] for c in connect[:3])} in Setup and this answers itself. Or answer in a line." if connect else "No source answers this. Answer in a line."),
                    "who": "the founder", "answered_on": None, "answer_record": None})
    out.sort(key=lambda q: (bool(q["answered_on"]), -q["importance"], -q["weight"], q["id"]))
    open_n = sum(1 for q in out if not q["answered_on"])
    return {"questions": out, "counts": {"open": open_n, "answered": len(out) - open_n, "round_due": open_n >= QUESTION_ROUND_AT,
                                          "rooms_blocked": len({r for q in out if not q["answered_on"] for r in q["rooms"]}),
                                          "connect_first": sum(1 for q in out if not q["answered_on"] and q["connect"])},
            "top": [q for q in out if not q["answered_on"]][:5], "round_at": QUESTION_ROUND_AT}


def answer_bank(brain: Brain, qid: str, body: dict):
    text = str((body or {}).get("answer") or "").strip()
    if not text:
        return 400, {"error": "answer is empty"}
    bank = keeper.load_bank()
    q = next((x for x in bank if x["id"] == qid), None)
    if q is None:
        return 404, {"error": "no such bank question", "id": qid}
    first = q["fills"][0]
    section = first.split(".")[0]
    field = first.split(".", 1)[1] if "." in first else f"founder_{qid.split('.')[-1]}"
    if section not in SECTIONS or not re.fullmatch(r"[a-z0-9_]{1,60}", field):
        return 400, {"error": "question fills no writable field", "fills": q["fills"]}
    rid = f"{brain.brand}.{section}.{field}"
    rec = {"id": rid, "brand": brain.brand, "section": section, "field": field, "value": _coerce(text), "text": text,
           "tier": "approved", "confidence": 1.0, "visibility": "private",
           "source": {"type": "founder", "ref": f"05-brand-brain answer to {qid}", "captured_at": brain.today.isoformat()}}
    errs = founder_put(brain, rec, kind="answer", what=f"answered {qid}: {text[:100]}")
    if errs:
        return 400, {"error": "record not valid", "details": errs}
    return 201, {"ok": True, "record": rid, "question": qid, "also_fills": q["fills"][1:], "unblocks": sorted(q["unblocks_rooms"]), "version": brain.version()}


DEFAULT_WINNER = ("founder", "connector", "site", "document", "ad_library", "interview", "press", "review", "ticket", "agent", "inferred")


def conflicts_view(brain: Brain) -> dict:
    """Open and settled conflicts with the default winner named (site wins over documents and everything below it)."""
    rows = _conflict_rows(brain)
    out = {"open": [], "settled": []}
    for c in rows:
        vals = c.get("values") or []
        ranked = sorted(vals, key=lambda v: (DEFAULT_WINNER.index(v.get("source_type")) if v.get("source_type") in DEFAULT_WINNER else 99, -(v.get("confidence") or 0)))
        default = ranked[0] if ranked else None
        item = dict(c, default_record=default.get("record_id") if default else None, default_source=default.get("source_type") if default else None,
                    kept_value=next((v for v in vals if v.get("record_id") == c.get("kept")), default),
                    reads_by=sorted(FLOWS_TO.get(c.get("section"), "").split(", ")) if FLOWS_TO.get(c.get("section")) else [])
        (out["open"] if c.get("status", "open") == "open" else out["settled"]).append(item)
    out["open"].sort(key=lambda c: (not c.get("needs_founder"), c.get("raised_at") or ""))
    out["settled"].sort(key=lambda c: -(int((c.get("resolved_at") or c.get("raised_at") or "0").replace("-", "")) if (c.get("resolved_at") or c.get("raised_at")) else 0))
    out["counts"] = {"open": len(out["open"]), "settled": len(out["settled"]), "needs_founder": sum(1 for c in out["open"] if c.get("needs_founder"))}
    out["rule"] = "Default: founder, then connector, then the live site, then documents, the ad library, interviews, press, reviews, tickets, agents, inferred. The kept value stands until you decide."
    return out


def conflict_resolve(brain: Brain, cid: str, body: dict):
    body = body or {}
    rows = _conflict_rows(brain)
    c = next((x for x in rows if x.get("id") == cid), None)
    if c is None:
        return 404, {"error": "no such conflict", "id": cid}
    vals = c.get("values") or []
    chosen = None
    if body.get("record_id"):
        chosen = next((v for v in vals if v.get("record_id") == body["record_id"] and ("index" not in body or vals.index(v) == body["index"])), None)
        if chosen is None and isinstance(body.get("index"), int) and 0 <= body["index"] < len(vals):
            chosen = vals[body["index"]]
    elif isinstance(body.get("index"), int) and 0 <= body["index"] < len(vals):
        chosen = vals[body["index"]]
    text = str(body.get("text") or "").strip()
    if chosen is None and not text:
        return 400, {"error": "send record_id, index or text"}
    section, field = c.get("section"), c.get("field")
    if section not in SECTIONS or not field:
        return 400, {"error": "conflict has no section or field"}
    rid = f"{brain.brand}.{section}.{field}"
    value = chosen.get("value") if chosen else _coerce(text)
    rec_text = (chosen.get("text") or str(chosen.get("value"))) if chosen else text
    reason = str(body.get("reason") or "").strip()[:300]
    rec = {"id": rid, "brand": brain.brand, "section": section, "field": field, "value": value, "text": rec_text,
           "tier": "approved", "confidence": 1.0, "visibility": "private",
           "source": {"type": "founder", "ref": f"05-brand-brain conflict decision on {cid}", "captured_at": brain.today.isoformat()}}
    errs = founder_put(brain, rec, kind="conflict", what=f"{section} {field}: kept {str(rec_text)[:80]}")
    if errs:
        return 400, {"error": "record not valid", "details": errs}
    c.update(status="resolved_by_founder", kept=rid, needs_founder=False, resolved_at=brain.today.isoformat(),
             rule="founder decided" + (f": {reason}" if reason else ""),
             chosen={"record_id": chosen.get("record_id") if chosen else None, "source_type": chosen.get("source_type") if chosen else "founder", "value": value})
    (brain.dir / "review").mkdir(parents=True, exist_ok=True)
    (brain.dir / "review" / "conflicts.json").write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    losers = [v for v in vals if v is not chosen]
    drec = {"id": f"{brain.brand}.decisions.conflict_{section}_{field}", "brand": brain.brand, "section": "decisions", "field": f"conflict_{section}_{field}",
            "value": {"conflict": cid, "kept": rid, "chosen_source": chosen.get("source_type") if chosen else "founder", "over": [v.get("source_type") for v in losers], "reason": reason or None},
            "text": f"Conflict on {section.replace('_', ' ')} {field.replace('_', ' ')}: kept \"{str(rec_text)[:80]}\" ({chosen.get('source_type') if chosen else 'typed by the founder'}) over " + (", ".join(f"\"{str(v.get('value'))[:40]}\" ({v.get('source_type')})" for v in losers) or "the other values") + (f". Reason: {reason}" if reason else "."),
            "tier": "approved", "confidence": 1.0, "visibility": "private",
            "source": {"type": "founder", "ref": f"05-brand-brain conflict decision on {cid}", "captured_at": brain.today.isoformat()}}
    founder_put(brain, drec)
    return 201, {"ok": True, "conflict": cid, "record": rid, "decision": drec["id"], "flows_to": FLOWS_TO.get(section, ""), "version": brain.version()}


def review_queue(brain: Brain) -> list[dict]:
    return [dict(record_view(r), section=r["section"])
            for r in brain.records(include_retired=True) if r["status"] == "proposed"]


def _same_value(a, b) -> bool:
    if isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool) and not isinstance(b, bool):
        return abs(float(a) - float(b)) < 1e-9
    if isinstance(a, str) and isinstance(b, str):
        return a.strip().lower() == b.strip().lower()
    return json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


def review_view(brain: Brain) -> dict:
    """Proposed records grouped by where they came from, each with the current winning record for the same field as the before."""
    active = {}
    for r in brain.records():
        key = (r["section"], r.get("field") or "value")
        cur = active.get(key)
        rank = (TIER_RANK.get(r["tier"], 9), "" if r["date"] == "undated" else "-" + r["date"])
        if cur is None or rank < cur[0]:
            active[key] = (rank, r)
    groups: dict[str, dict] = {}
    for r in brain.records(include_retired=True):
        if r["status"] != "proposed":
            continue
        src = r.get("source") or {}
        ref = src.get("ref") or src.get("type") or "unknown"
        key = Path(ref).name if ref.startswith("documents/") else ref
        g = groups.setdefault(key, {"source": key, "type": src.get("type") or "unknown", "date": None if r["date"] == "undated" else r["date"], "records": []})
        field = r.get("field") or "value"
        base_field = field
        if src.get("type") == "document":
            doc_slug = ingest.slug(Path(key).stem, 30)
            if doc_slug and field.startswith(doc_slug + "_"):
                base_field = field[len(doc_slug) + 1:]
        before = None
        hit = active.get((r["section"], field)) or active.get((r["section"], base_field))
        if hit:
            before = hit[1]
        elif src.get("type") == "document":
            # the file's key names the fact loosely: match an active field that starts with it, or that it starts with
            for (sec, f), (_, rec) in active.items():
                if sec == r["section"] and f != "value" and len(base_field) >= 8 and (f.startswith(base_field) or base_field.startswith(f)):
                    before = rec
                    break
        item = dict(record_view(r), section=r["section"])
        item["before"] = None if before is None else {"id": before["id"], "text": before.get("text") or (before["value"] if isinstance(before.get("value"), str) else json.dumps(before.get("value"))[:200]), "tier": before["tier"], "date": None if before["date"] == "undated" else before["date"]}
        item["change"] = "new field" if before is None else ("same value" if _same_value(before.get("value"), r.get("value")) else "replaces")
        g["records"].append(item)
    out = sorted(groups.values(), key=lambda g: (-(len(g["records"])), g["source"]))
    total = sum(len(g["records"]) for g in out)
    return {"groups": out, "counts": {"proposed": total, "groups": len(out), "new_fields": sum(1 for g in out for r in g["records"] if r["change"] == "new field"),
                                       "replacing": sum(1 for g in out for r in g["records"] if r["change"] == "replaces"), "duplicates": sum(1 for g in out for r in g["records"] if r["change"] == "same value")},
            "note": "Accept makes a record active; ignore retires it (never deleted). Before is the record that wins the field today. Same value means the proposal adds nothing: ignore it."}


def review_bulk(brain: Brain, body: dict):
    choice = (body or {}).get("choice")
    ids = [str(i) for i in ((body or {}).get("ids") or []) if isinstance(i, str)]
    if choice not in ("accept", "ignore"):
        return 400, {"error": "choice must be accept or ignore"}
    if not ids:
        return 400, {"error": "ids is empty"}
    done, failed = [], []
    for rid in ids[:200]:
        res = review(brain, rid, {"choice": choice})
        if isinstance(res, tuple):
            failed.append({"id": rid, "error": res[1].get("error")})
        else:
            done.append(rid)
    return 201, {"ok": not failed, "choice": choice, "done": done, "failed": failed, "version": brain.version()}


def ladders(brain: Brain) -> list[dict]:
    out = []
    for lad in brain.records("objection_ladders"):
        v = lad.get("value") or {}
        rungs = [{"level": r.get("level"), "doubt": r.get("doubt"), "one_star": (r.get("one_star") or [])[:2],
                  "five_star": (r.get("five_star") or [])[:1], "counts": r.get("counts") or {},
                  "proof": r.get("proof"), "proof_ids": r.get("proof_ids") or [], "uses": r.get("uses") or []}
                 for r in v.get("rungs") or []]
        out.append({"id": lad["id"], "theme": v.get("theme") or lad.get("field"), "rungs": rungs,
                    "date": lad["date"], "tier": lad["tier"]})
    return out


def chart(brain: Brain) -> dict:
    """Records added per day: each record counts once, on its earliest known date."""
    first: dict[str, int] = {}
    undated = 0
    for r in brain.records(include_retired=True):
        dates = [h.get("changed_at")[:10] for h in (r.get("history") or []) if h.get("changed_at")]
        if r["date"] != "undated":
            dates.append(r["date"])
        if not dates:
            undated += 1
            continue
        d = min(dates)
        first[d] = first.get(d, 0) + 1
    days = [(brain.today - dt.timedelta(days=i)).isoformat() for i in range(CHART_DAYS - 1, -1, -1)]
    earlier = sum(n for d, n in first.items() if d < days[0])
    return {"labels": days, "values": [first.get(d, 0) for d in days], "earlier": earlier, "undated": undated}


def tiles(sections, questions, conflict_rows, bank_gaps) -> list[dict]:
    waiting = sum(1 for q in questions if not q["answered_on"])
    empty = sorted({g["section"] for g in bank_gaps if g["kind"] == "empty"})
    return [
        {"name": "Open questions", "plain": "Questions waiting on a founder answer", "value": waiting,
         "unit": "n", "window": "as of now", "tone": "bad" if waiting >= QUESTION_ROUND_AT else None},
        {"name": "Conflicts", "plain": "Facts where two sources disagree", "value": len(conflict_rows),
         "unit": "n", "window": "as of now", "tone": "bad" if conflict_rows else "good"},
        {"name": "Sections a room is missing", "plain": "Sections with a field a room needs and no record",
         "value": len(empty), "unit": "n", "window": "as of now", "tone": "bad" if empty else "good"},
    ]


def _short(ref: str) -> str:
    return re.sub(r"^https?://", "", ref or "a source").rstrip("/")


def insights(questions, conflict_rows) -> list[dict]:
    """Two rules from the room spec: founder question round due, and source conflict."""
    out = []
    waiting = [q for q in questions if not q["answered_on"]]
    if len(waiting) >= QUESTION_ROUND_AT:
        out.append({"rule": f"open_questions_count >= {QUESTION_ROUND_AT}", "severity": "high",
                    "sentence": f"{len(waiting)} open questions are waiting. It is time for a founder round.",
                    "capability": "BRN-C07", "autonomy": "founder_gate",
                    "evidence": f"highest weight: {waiting[0]['question']}"})
    for c in conflict_rows:
        vals = c.get("values") or []
        if len(vals) < 2:
            continue
        a, b = vals[0], vals[1]
        kept = next((v for v in vals if v.get("record_id") == c.get("kept")), a)
        out.append({"rule": "two sources disagree on the same field", "severity": "high",
                    "sentence": (f"{_short(a['source_ref'])} says \"{a['value']}\". "
                                 f"{_short(b['source_ref'])} says \"{b['value']}\". "
                                 f"\"{kept['value']}\" is kept until you say otherwise."),
                    "capability": "BRN-C05", "autonomy": "agent",
                    "evidence": f"{c['section']}.{c['field']}, rule: {c.get('rule')}"})
    return out


def overview(brain: Brain) -> dict:
    bank = keeper.load_bank()
    sections = section_table(brain)
    questions = open_questions(brain, bank)
    conf = conflicts(brain)
    g = keeper.gaps(brain, bank)
    return {"brand": brain.brand, "today": brain.today.isoformat(), "version": brain.version(),
            "simulated_note": SIMULATED_NOTE if brain.brand == "bombas" else f"{brain.brand} is a brain folder. " + GENERIC_NOTE, "t0": t0_card(brain, False),
            "tiles": tiles(sections, questions, conf, g), "insights": insights(questions, conf),
            "chart": chart(brain), "sections": sections, "ladders": ladders(brain),
            "questions": questions, "review": review_queue(brain), "conflicts": conf}


FOUNDER_LANE = "z-founder"


def founder_put(brain: Brain, rec: dict, kind: str = "founder_edit", what: str | None = None) -> list[str]:
    """Write a founder record to its section file and to raw/z-founder/<section>.json, so merge.py keeps it on a re-merge.
    Logs one changes record (with the value before, when the record existed) and a version step."""
    before_v = brain.version()
    old = next((r for r in brain.raw(rec["section"]) if r.get("id") == rec["id"]), None)
    errs = brain.put(rec)
    if errs:
        return errs
    changes.log(brain, kind, rec["section"], rec["id"], what or f"{rec['section'].replace('_', ' ')} {(rec.get('field') or '').replace('_', ' ')}: {str(rec.get('text') or rec.get('value'))[:120]}",
                before=(old.get("value") if old else None), after=rec.get("value"))
    changes.version_step(brain, before_v, what or f"{kind} {rec['id']}")
    lane = brain.dir / "raw" / FOUNDER_LANE
    try:
        lane.mkdir(parents=True, exist_ok=True)
        path = lane / f"{rec['section']}.json"
        rows = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
        rows = [r for r in rows if r.get("id") != rec["id"]] + [rec]
        path.write_text(json.dumps(rows, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    except (OSError, ValueError):
        pass  # the section file is the record of truth; the raw lane is a convenience for re-merges
    return []


def _coerce(text: str):
    t = text.strip().replace(",", "")
    try:
        return float(t.rstrip("%")) if t.rstrip("%").replace(".", "", 1).lstrip("-").isdigit() else text.strip()
    except ValueError:
        return text.strip()


def answer(brain: Brain, field: str, body: dict):
    text = str((body or {}).get("answer") or "").strip()
    if not text:
        return 400, {"error": "answer is empty"}
    oq = next((r for r in brain.raw("open_questions") if r.get("field") == field), None)
    if oq is None:
        return 404, {"error": "no open question", "field": field}
    v = dict(oq.get("value") or {})
    section = v.get("section") if v.get("section") in SECTIONS else "open_questions"
    rid = f"{brain.brand}.{section}.{field}"
    rec = {"id": rid, "brand": brain.brand, "section": section, "field": field, "value": _coerce(text),
           "text": text, "tier": "approved", "confidence": 1.0, "visibility": "private",
           "source": {"type": "founder", "ref": f"05-brand-brain answer to {oq['id']}",
                      "captured_at": brain.today.isoformat()}}
    errs = founder_put(brain, rec, kind="answer", what=f"answered {oq['id']}: {text[:100]}")
    if errs:
        return 400, {"error": "record not valid", "details": errs}
    v.update(answered_on=brain.today.isoformat(), answer_record=rid)
    errs = brain.put(dict(oq, value=v))
    if errs:
        return 400, {"error": "question not updated", "details": errs}
    return 201, {"ok": True, "record": rid, "question": oq["id"]}


def review(brain: Brain, rid: str, body: dict):
    choice = (body or {}).get("choice")
    if choice not in ("accept", "ignore"):
        return 400, {"error": "choice must be accept or ignore"}
    parts = rid.split(".")
    if len(parts) < 3 or parts[1] not in SECTIONS:
        return 404, {"error": "no such record", "id": rid}
    rec = next((r for r in brain.raw(parts[1]) if r.get("id") == rid), None)
    if rec is None or rec.get("status") != "proposed":
        return 404, {"error": "no proposed record", "id": rid}
    if choice == "ignore":
        brain.retire(rid)
        changes.log(brain, "ignored", parts[1], rid, f"ignored {rid}")
        return {"ok": True, "id": rid, "status": "retired"}
    errs = brain.put(dict(rec, status="active"))
    if errs:
        return 400, {"error": "record not valid", "details": errs}
    changes.log(brain, "accepted", parts[1], rid, f"accepted {rid}: {str(rec.get('text') or rec.get('value'))[:100]}", after=rec.get("value"))
    return {"ok": True, "id": rid, "status": "active"}


def _window(req, brain: Brain) -> dict:
    w = req.arg("window", "28d") or "28d"
    days = int(w[:-1]) if re.fullmatch(r"\d+d", w) else 28
    return {"ends_on": (brain.today - dt.timedelta(days=1)).isoformat(), "days": days, "trailing": 4}


def master(brain: Brain, window: dict) -> dict:
    root = (BRAIN_ROOT or (APP / "brain"))
    out = rank_mod.master(brain.brand, window)
    out["brain_version"] = brain.version()
    out["brain_root"] = str(root.name)
    return out


def profile(brain: Brain) -> dict:
    """One winning record per field: the best tier, then the newest. Founder edits are tier approved and win."""
    sections = []
    for sec, label, first in PROFILE_SECTIONS:
        by_field: dict[str, dict] = {}
        for r in brain.records(sec):
            f = r.get("field") or "value"
            key = (TIER_RANK.get(r["tier"], 9), "" if r["date"] == "undated" else "-" + r["date"])
            cur = by_field.get(f)
            if cur is None or key < cur[0]:
                by_field[f] = (key, r)
        order = list(first) + sorted(k for k in by_field if k not in first)
        fields = []
        for f in order:
            if f not in by_field:
                fields.append({"key": f, "text": None, "tier": None, "source": None, "date": None, "confidence": None, "record_id": None, "editable": True})
                continue
            r = by_field[f][1]
            src = _source(r)
            fields.append({"key": f, "text": r.get("text") or (r["value"] if isinstance(r.get("value"), str) else json.dumps(r.get("value"))[:300]),
                           "tier": r["tier"], "source": (src["type"] + (": " + re.sub(r"^https?://", "", src["ref"])[:60] if src["ref"] else "")),
                           "date": None if r["date"] == "undated" else r["date"], "confidence": r["confidence"], "record_id": r["id"],
                           "variants": sum(1 for x in brain.records(sec) if (x.get("field") or "value") == f), "editable": True})
        approved = sum(1 for x in fields if x["tier"] == "approved")
        sections.append({"section": sec, "label": label, "flows_to": FLOWS_TO.get(sec, ""), "fields": fields,
                         "records": len(brain.records(sec)), "approved": approved})
    total = sum(len(x["fields"]) for x in sections)
    appr = sum(x["approved"] for x in sections)
    return {"brand": brain.brand, "today": brain.today.isoformat(), "version": brain.version(), "sections": sections,
            "fields": total, "approved": appr, "approved_share": (appr / total) if total else None}


def profile_edit(brain: Brain, section: str, field: str, body: dict):
    text = str((body or {}).get("text") or "").strip()
    if not text:
        return 400, {"error": "text is empty"}
    if section not in {s for s, _, _ in PROFILE_SECTIONS} or not re.fullmatch(r"[a-z0-9_]{1,60}", field):
        return 404, {"error": "no such profile field", "section": section, "field": field}
    rid = f"{brain.brand}.{section}.{field}"
    rec = {"id": rid, "brand": brain.brand, "section": section, "field": field, "value": _coerce(text), "text": text,
           "tier": "approved", "confidence": 1.0, "visibility": "private",
           "source": {"type": "founder", "ref": "05-brand-brain profile edit", "captured_at": brain.today.isoformat()}}
    errs = founder_put(brain, rec)
    if errs:
        return 400, {"error": "record not valid", "details": errs}
    return 201, {"ok": True, "record": rid, "tier": "approved", "flows_to": FLOWS_TO.get(section, ""), "version": brain.version()}


def documents(brain: Brain) -> dict:
    docs = brain.documents()
    recs = brain.records(include_retired=True)
    out = []
    for d in docs:
        name = Path(d.get("file", "")).name
        mine = [r for r in recs if name and name in str((r.get("source") or {}).get("ref") or "")]
        proposed = [r for r in mine if r["status"] == "proposed"]
        accepted = [r for r in mine if r["status"] == "active"]
        ignored = [r for r in mine if r["status"] == "retired"]
        out.append(dict(d, name=name, records_changed=[r["id"] for r in mine][:20], records_changed_count=len(mine),
                        proposed=len(proposed), accepted=len(accepted), ignored=len(ignored),
                        sections_changed=sorted({r["section"] for r in mine}), readable=ingest.is_text_file(name),
                        what_changed=(f"{len(accepted)} accepted, {len(proposed)} waiting in the review queue, {len(ignored)} ignored" if mine
                                      else ("read, nothing to propose" if d.get("extracted") else ("kept as a file; not a text file" if not ingest.is_text_file(name) else "not read yet")))))
    out.sort(key=lambda d: d.get("added_at", ""), reverse=True)
    return {"documents": out, "count": len(out), "proposed_total": sum(d["proposed"] for d in out), "accepted_total": sum(d["accepted"] for d in out)}


def extract_document(brain: Brain, line: dict, data: bytes) -> dict:
    """Propose records from a text file into the review queue and mark the manifest line. Never blocks the upload."""
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        text = data.decode("latin-1", errors="replace")
    recs = ingest.extract(text, brain.brand, line["file"], brain.today.isoformat())
    written, errors = [], []
    for r in recs:
        errs = brain.put(r)
        (errors if errs else written).append(r["id"] if not errs else {"id": r["id"], "errors": errs})
    sm = ingest.summary([r for r in recs if r["id"] in set(written)])
    line.update(extracted=True, sections=sm["sections"], records_proposed=len(written))
    return dict(sm, written=written, errors=errors)


def document_add(brain: Brain, body: dict):
    body = body or {}
    url = str(body.get("url") or "").strip()
    name = str(body.get("name") or "").strip()
    note = str(body.get("note") or "").strip()[:300]
    if url:
        if not re.match(r"^https?://[^\s]{4,500}$", url):
            return 400, {"error": "url must start with http or https"}
        name = name or re.sub(r"[^A-Za-z0-9._-]+", "-", re.sub(r"^https?://", "", url))[:80].strip("-") + ".url"
        data = ("[InternetShortcut]\nURL=" + url + "\n").encode("utf-8")
    else:
        if not SAFE_FILE.match(name) or ".." in name:
            return 400, {"error": "name must be a plain file name"}
        if body.get("content_base64") is not None:
            try:
                data = base64.b64decode(str(body["content_base64"]), validate=True)
            except (ValueError, TypeError):
                return 400, {"error": "content_base64 is not valid base64"}
        elif body.get("text") is not None:
            data = str(body["text"]).encode("utf-8")
        else:
            return 400, {"error": "send text, content_base64 or url"}
    if len(data) > DOC_MAX_BYTES:
        return 413, {"error": "file is over 5 MB"}
    ddir = brain.dir / "documents"
    ddir.mkdir(parents=True, exist_ok=True)
    stamp = brain.today.isoformat()
    fname = f"{stamp}-{name}"
    target = ddir / fname
    i = 2
    while target.exists():
        target = ddir / f"{stamp}-{i}-{name}"
        i += 1
    target.write_bytes(data)
    manifest = brain.documents()
    line = {"file": f"documents/{target.name}", "added_at": stamp, "added_by": "founder", "extracted": False}
    if note:
        line["note"] = note
    if url:
        line["tags"] = ["url"]
    result = None
    if not url and ingest.is_text_file(target.name):
        result = extract_document(brain, line, data)
    manifest.append(line)
    (ddir / "manifest.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")
    changes.log(brain, "document", None, None, f"{target.name} ({len(data)} bytes)" + (f", {result['proposed']} records proposed" if result else ""))
    if result:
        nxt = (f"Read it: {result['proposed']} records proposed into the review queue ({', '.join(result['sections']) or 'none'}). "
               f"{result['forbidden']} marked forbidden. Nothing reaches the brain until you accept it.") if result["proposed"] else "Read it: nothing to propose. Kept as a file."
    else:
        nxt = "Kept as it is. A text or markdown file is read into proposed records; this one is not, so it stays a document."
    return 201, {"ok": True, "document": dict(line, name=target.name, bytes=len(data)), "records_changed_count": (result or {}).get("proposed", 0),
                 "extraction": result, "next": nxt, "version": brain.version()}


def document_extract(brain: Brain, body: dict):
    """Re-read one stored text file into the review queue (for files added before extraction existed)."""
    name = str((body or {}).get("name") or "").strip()
    manifest = brain.documents()
    line = next((d for d in manifest if Path(d.get("file", "")).name == name), None)
    if line is None:
        return 404, {"error": "no such document", "name": name}
    path = brain.dir / line["file"]
    if not path.is_file() or not ingest.is_text_file(name):
        return 400, {"error": "not a readable text file", "name": name}
    result = extract_document(brain, line, path.read_bytes())
    (brain.dir / "documents" / "manifest.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")
    return 201, {"ok": True, "name": name, "extraction": result, "version": brain.version()}


def competitors(brain: Brain) -> dict:
    d = market.pages(brain)
    d["gaps"] = market.gaps(brain)
    d["repull"] = market.repull(brain)
    d["formats"] = [{"key": k, "label": market.FORMAT_LABEL[k]} for k in market.FORMATS]
    d["hooks"] = [{"key": k, "label": market.HOOK_LABEL[k]} for k in market.HOOKS]
    d["stale_after_days"] = market.SNAPSHOT_STALE_DAYS
    d["brand"], d["today"], d["version"] = brain.brand, brain.today.isoformat(), brain.version()
    return d


def page_id_add(brain: Brain, body: dict):
    name = str((body or {}).get("name") or "").strip()
    pid = str((body or {}).get("page_id") or "").strip()
    if not name or not re.fullmatch(r"[A-Za-z0-9 .&'-]{2,60}", name):
        return 400, {"error": "name must be a plain page name"}
    if not re.fullmatch(r"\d{5,20}", pid):
        return 400, {"error": "page_id must be the numeric Meta page id"}
    slug = market._slug(name)
    rid = f"{brain.brand}.competitors.page_id_{slug}"
    rec = {"id": rid, "brand": brain.brand, "section": "competitors", "field": f"page_id_{slug}", "value": pid,
           "text": f"{name} Meta page id {pid}, added by the founder for the Ad Library pull.",
           "tier": "approved", "confidence": 1.0, "visibility": "private",
           "source": {"type": "founder", "ref": "05-brand-brain competitors page id", "captured_at": brain.today.isoformat()}}
    errs = founder_put(brain, rec)
    if errs:
        return 400, {"error": "record not valid", "details": errs}
    return 201, {"ok": True, "record": rid, "flows_to": "the page list and the next Ad Library pull estimate", "version": brain.version()}


def approve(brain: Brain, rid: str, body: dict):
    choice = (body or {}).get("choice")
    if choice not in ("approve", "forbid"):
        return 400, {"error": "choice must be approve or forbid"}
    parts = rid.split(".")
    if len(parts) < 3 or parts[1] not in SECTIONS:
        return 404, {"error": "no such record", "id": rid}
    rec = next((r for r in brain.raw(parts[1]) if r.get("id") == rid), None)
    if rec is None:
        return 404, {"error": "no such record", "id": rid}
    was = {"type": (rec.get("source") or {}).get("type"), "ref": (rec.get("source") or {}).get("ref"), "tier": rec.get("tier")}
    hist = list(rec.get("history") or []) + [{"value": rec.get("value"), "changed_at": brain.today.isoformat(),
                                             "source_ref": was["ref"] or "", "tier": was["tier"], "reason": f"founder {choice}"}]
    new = dict(rec, tier="approved" if choice == "approve" else "forbidden", confidence=1.0, status="active", history=hist,
               source={"type": "founder", "ref": f"05-brand-brain {choice} of {rid}", "captured_at": brain.today.isoformat(), "was": was})
    new.pop("expires_at", None)
    errs = founder_put(brain, new, kind=choice, what=f"{rid} {choice}d: {rec.get('tier')} to {new['tier']}")
    if errs:
        return 400, {"error": "record not valid", "details": errs}
    return 201, {"ok": True, "record": rid, "tier": new["tier"], "was": rec.get("tier"), "version": brain.version()}


def claim_add(brain: Brain, body: dict):
    """The founder adds a claim (approved) or forbids a phrase (forbidden)."""
    text = str((body or {}).get("text") or "").strip()
    tier = (body or {}).get("tier") or "approved"
    if not text or len(text) < 4:
        return 400, {"error": "text is empty"}
    if tier not in ("approved", "forbidden"):
        return 400, {"error": "tier must be approved or forbidden"}
    key = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")[:40]
    field = ("never_" if tier == "forbidden" else "founder_") + key
    rid = f"{brain.brand}.claims.{field}"
    rec = {"id": rid, "brand": brain.brand, "section": "claims", "field": field, "value": ("never say: " if tier == "forbidden" else "founder claim: ") + text,
           "text": ("Never say " + text.rstrip(".") + ".") if tier == "forbidden" else text, "tier": tier, "confidence": 1.0, "visibility": "private",
           "source": {"type": "founder", "ref": "05-brand-brain claims desk", "captured_at": brain.today.isoformat()}}
    errs = founder_put(brain, rec)
    if errs:
        return 400, {"error": "record not valid", "details": errs}
    return 201, {"ok": True, "record": rid, "tier": tier, "flows_to": FLOWS_TO.get("claims", ""), "version": brain.version()}


def bottlenecks_view(brain: Brain, window: dict) -> dict:
    try:
        actions = rank_mod.master(brain.brand, window)["actions"]
    except Exception:  # noqa: BLE001
        actions = rank(brain.brand, window)["actions"]
    out = bottlenecks.unlocks(brain, actions)
    out.update(brand=brain.brand, today=brain.today.isoformat(), version=brain.version())
    return out


def idea_pick(brain: Brain, body: dict):
    body = body or {}
    idea_id = str(body.get("idea_id") or "").strip().upper()
    if not re.fullmatch(r"[A-Z]{2,6}-\d{3,4}", idea_id):
        return 400, {"error": "idea_id must be a bank id like OFF-103"}
    res = bottlenecks.pick(brain, idea_id, str(body.get("bottleneck") or "").strip() or None, str(body.get("why") or "").strip())
    if not res["ok"]:
        return 404, res
    errs = founder_put(brain, res["record"], kind="founder_edit", what=f"picked idea {idea_id}: {res['record']['value']['title'][:100]}")
    if errs:
        return 400, {"error": "record not valid", "details": errs}
    return 201, {"ok": True, "record": res["record"]["id"], "idea_id": idea_id, "next": "It is a plans record now. The audit turns it into a test brief on the master list on the next load.", "version": brain.version()}


def report_view(brain: Brain, days: int) -> dict:
    try:
        actions = rank(brain.brand, _window_dict(brain))["actions"]
    except Exception:  # noqa: BLE001
        actions = []
    out = report.weekly(brain, days, changes.recent(brain, days), decisions_log(brain), questions_ranked(brain), conflicts_view(brain), sitediff.diff(brain), documents(brain),
                        health.heatmap(brain), actions, market.pages(brain) | {"gaps": market.gaps(brain)})
    out.update(brand=brain.brand, today=brain.today.isoformat(), version=brain.version())
    return out


def digest_view(brain: Brain) -> dict:
    try:
        actions = rank(brain.brand, _window_dict(brain))["actions"]
    except Exception:  # noqa: BLE001
        actions = []
    out = report.digest(brain, questions_ranked(brain), review_queue(brain), health.heatmap(brain), actions, health.connectors(brain))
    out.update(brand=brain.brand, today=brain.today.isoformat(), version=brain.version())
    return out


def _window_dict(brain: Brain) -> dict:
    return {"ends_on": (brain.today - dt.timedelta(days=1)).isoformat(), "days": 28, "trailing": 4}


def learn_view(brain: Brain) -> dict:
    return learn.proposals(brain, voice.words_avoided(brain), [w.strip().lower() for w in re.split(r"[,;\n]+", voice._text(voice._rec(brain, "voice", "words_used")) or "") if w.strip()])


def learn_apply(brain: Brain, body: dict):
    body = body or {}
    kind = body.get("kind")
    words = [str(w).strip().lower() for w in (body.get("words") or []) if str(w).strip()]
    if kind not in ("avoided", "used"):
        return 400, {"error": "kind must be avoided or used"}
    if not words:
        return 400, {"error": "words is empty"}
    field = "words_avoided" if kind == "avoided" else "words_used"
    cur = voice._rec(brain, "voice", field)
    have = [w.strip() for w in re.split(r"[,;\n]+", voice._text(cur) or "") if w.strip()]
    merged = have + [w for w in words if w not in {h.lower() for h in have}]
    text = ", ".join(merged)
    rec = {"id": f"{brain.brand}.voice.{field}", "brand": brain.brand, "section": "voice", "field": field, "value": merged, "text": text,
           "tier": "approved", "confidence": 1.0, "visibility": "private",
           "source": {"type": "founder", "ref": "05-brand-brain learned from edits", "captured_at": brain.today.isoformat()}}
    errs = founder_put(brain, rec, what=f"{field.replace('_', ' ')} learned from edits: {', '.join(words)[:100]}")
    if errs:
        return 400, {"error": "record not valid", "details": errs}
    return 201, {"ok": True, "record": rec["id"], "words": merged, "version": brain.version()}


def summaries(brain: Brain) -> dict:
    rows = []
    for sec in SECTIONS:
        if sec in health.META_SECTIONS:
            continue
        text = package_mod.t1_summary(brain, sec)
        rows.append({"section": sec, "label": sec.replace("_", " "), "records": len(brain.records(sec)), "tokens": package_mod.tokens(text), "text": text})
    t0 = t0_card(brain, False)
    return {"t0_tokens": package_mod.tokens(t0), "sections": rows, "total_tokens": sum(r["tokens"] for r in rows) + package_mod.tokens(t0),
            "note": "T0 is the brand card every agent reads. T1 is one derived paragraph per section, built in code from the strongest records until 480 characters. T2 is the records themselves, only for the sections a capability names."}


def package_view(brain: Brain, cap_id: str):
    if not re.fullmatch(r"[A-Z]{2,6}-C\d{2,3}", cap_id or ""):
        return 400, {"error": "capability must be an id like CREA-C06"}
    try:
        pkg = package_mod.package(brain.brand, cap_id, root=BRAIN_ROOT, today=brain.today, use_cache=False)
    except KeyError as exc:
        return 404, {"error": str(exc), "capability": cap_id}
    cat = rank_mod.catalogue().get(cap_id, {})
    return {"capability": cap_id, "name": cat.get("name"), "autonomy": cat.get("autonomy"), "budget": pkg["budget"], "tokens": pkg["tokens"], "public_facing": pkg["public_facing"],
            "share": round(pkg["tokens"] / pkg["budget"], 2) if pkg["budget"] else None,
            "parts": [{"tier": p["tier"], "section": p.get("section"), "tokens": package_mod.tokens(p["text"]), "text": p["text"]} for p in pkg["parts"]],
            "records": len(pkg["records"]), "record_ids": [r["id"] for r in pkg["records"]], "version": pkg["version"], "text": pkg["text"]}


def fact_approve(brain: Brain, key: str, body: dict):
    if key not in facts.KEYS:
        return 404, {"error": "no such fact", "key": key}
    answer = str((body or {}).get("answer") or "").strip()
    if len(answer) < 4:
        return 400, {"error": "answer is empty"}
    question = str((body or {}).get("question") or "").strip() or facts.QUESTIONS[key]
    field = f"faq_{key}"
    rec = {"id": f"{brain.brand}.content.{field}", "brand": brain.brand, "section": "content", "field": field, "value": {"question": question, "answer": answer},
           "text": f"Q: {question} A: {answer}", "tier": "approved", "confidence": 1.0, "visibility": "public",
           "source": {"type": "founder", "ref": "05-brand-brain store facts", "captured_at": brain.today.isoformat()}}
    errs = founder_put(brain, rec, what=f"store fact {key} approved: {answer[:100]}")
    if errs:
        return 400, {"error": "record not valid", "details": errs}
    row = next((r for r in facts.pairs(brain)["pairs"] if r["key"] == key), None)
    return 201, {"ok": True, "record": rec["id"], "status": row["status"] if row else None, "version": brain.version()}


def assumption_set(brain: Brain, field: str, body: dict):
    body = body or {}
    row = next((a for a in assumptions.load(brain) if a.get("field") == field), None)
    if row is None:
        return 404, {"error": "no such assumption", "field": field}
    target = (row.get("source_ids") or [None])[0]
    if not target or target.count(".") < 2 or target.split(".")[1] not in SECTIONS:
        return 400, {"error": "assumption has no brain record to write to", "field": field}
    section, rfield = target.split(".")[1], target.split(".", 2)[2]
    if body.get("choice") == "confirm":
        value = row.get("value")
        text = f"{field.replace('_', ' ')} confirmed by the founder: {assumptions._summary(value)}"
    else:
        raw = str(body.get("value") or "").strip()
        if not raw:
            return 400, {"error": "send choice confirm or a value"}
        value = _coerce(raw)
        text = f"{field.replace('_', ' ')} set by the founder: {raw[:160]}"
    rec = {"id": target, "brand": brain.brand, "section": section, "field": rfield, "value": value, "text": text,
           "tier": "approved", "confidence": 1.0, "visibility": "private",
           "source": {"type": "founder", "ref": "05-brand-brain assumptions register", "captured_at": brain.today.isoformat()}}
    errs = founder_put(brain, rec, what=f"assumption {field}: {text[:100]}")
    if errs:
        return 400, {"error": "record not valid", "details": errs}
    return 201, {"ok": True, "record": target, "status": "founder", "rooms": next((a["rooms"] for a in assumptions.register(brain, health.rooms_by_section(keeper.load_bank()))["assumptions"] if a["field"] == field), []), "version": brain.version()}


def permission_set(brain: Brain, section: str, body: dict):
    if section not in SECTIONS or section in health.META_SECTIONS:
        return 404, {"error": "no such section", "section": section}
    roles = (body or {}).get("roles") or {}
    if not isinstance(roles, dict) or not roles:
        return 400, {"error": "roles must map role to full, read or none"}
    clean = {}
    for role, lv in roles.items():
        if role not in health.ROLES or lv not in health.LEVELS:
            return 400, {"error": f"bad role or level: {role}={lv}"}
        clean[role] = lv
    clean["founder"] = "full"
    field = f"permission_{section}"
    rec = {"id": f"{brain.brand}.team.{field}", "brand": brain.brand, "section": "team", "field": field, "value": {"section": section, "roles": clean},
           "text": f"{section.replace('_', ' ')}: " + ", ".join(f"{health.ROLE_LABEL[r].lower()} {lv}" for r, lv in clean.items()) + ".",
           "tier": "approved", "confidence": 1.0, "visibility": "private",
           "source": {"type": "founder", "ref": "05-brand-brain permissions", "captured_at": brain.today.isoformat()}}
    errs = founder_put(brain, rec)
    if errs:
        return 400, {"error": "record not valid", "details": errs}
    return 201, {"ok": True, "record": rec["id"], "roles": clean, "version": brain.version()}


def voice_example(brain: Brain, body: dict):
    body = body or {}
    kind = body.get("kind")
    text = str(body.get("text") or "").strip()
    why = str(body.get("why") or "").strip()[:200]
    if kind not in ("liked", "disliked"):
        return 400, {"error": "kind must be liked or disliked"}
    if len(text) < 4:
        return 400, {"error": "text is empty"}
    n = sum(1 for r in brain.records("voice", include_retired=True) if (r.get("field") or "").startswith(f"{kind}_example")) + 1
    field = f"{kind}_example_{n}"
    rec = {"id": f"{brain.brand}.voice.{field}", "brand": brain.brand, "section": "voice", "field": field, "value": {"text": text, "why": why or None},
           "text": text, "tier": "approved", "confidence": 1.0, "visibility": "private",
           "source": {"type": "founder", "ref": "05-brand-brain voice sheet", "captured_at": brain.today.isoformat()}}
    errs = founder_put(brain, rec)
    if errs:
        return 400, {"error": "record not valid", "details": errs}
    return 201, {"ok": True, "record": rec["id"], "kind": kind, "count": n, "version": brain.version()}


def snippet_lock(brain: Brain, key: str, body: dict):
    text = str((body or {}).get("text") or "").strip()
    if key not in voice.SNIPPET_KEYS:
        return 404, {"error": "no such snippet", "key": key}
    if len(text) < 4:
        return 400, {"error": "text is empty"}
    field = f"snippet_{key}"
    rec = {"id": f"{brain.brand}.voice.{field}", "brand": brain.brand, "section": "voice", "field": field, "value": text, "text": text,
           "tier": "approved", "confidence": 1.0, "visibility": "private",
           "source": {"type": "founder", "ref": "05-brand-brain snippets", "captured_at": brain.today.isoformat()}}
    errs = founder_put(brain, rec)
    if errs:
        return 400, {"error": "record not valid", "details": errs}
    row = next((r for r in voice.snippets(brain)["snippets"] if r["key"] == key), None)
    return 201, {"ok": True, "record": rec["id"], "status": row["status"] if row else None, "version": brain.version()}


def contract_add(brain: Brain, body: dict):
    body = body or {}
    vendor = str(body.get("vendor") or "").strip()
    if not vendor or len(vendor) > 60:
        return 400, {"error": "vendor is empty"}
    ctype = body.get("type") if body.get("type") in contracts.WINDOW_DAYS else "other"
    rd = str(body.get("renewal_date") or "").strip() or None
    if rd:
        try:
            dt.date.fromisoformat(rd)
        except ValueError:
            return 400, {"error": "renewal_date must be YYYY-MM-DD"}
    notice = body.get("notice_days")
    try:
        notice = int(notice) if notice not in (None, "") else None
    except (TypeError, ValueError):
        return 400, {"error": "notice_days must be a number"}
    value = {"vendor": vendor, "type": ctype, "renewal_date": rd, "notice_days": notice,
             "rate_card": str(body.get("rate_card") or "").strip()[:200] or None, "sla_terms": str(body.get("sla_terms") or "").strip()[:200] or None,
             "source_doc": str(body.get("source_doc") or "").strip()[:120] or None}
    field = "contract_" + contracts.slug(vendor)
    rec = {"id": f"{brain.brand}.operations.{field}", "brand": brain.brand, "section": "operations", "field": field, "value": value,
           "text": f"{vendor} ({ctype}) " + (f"renews on {rd}" if rd else "has no renewal date on file") + (f", {notice} days notice" if notice else "") + ".",
           "tier": "approved", "confidence": 1.0, "visibility": "private",
           "source": {"type": "founder", "ref": "05-brand-brain contracts", "captured_at": brain.today.isoformat()}}
    errs = founder_put(brain, rec)
    if errs:
        return 400, {"error": "record not valid", "details": errs}
    return 201, {"ok": True, "record": rec["id"], "window_days": contracts.WINDOW_DAYS[ctype], "version": brain.version()}


def parity_set(brain: Brain, what: str, body: dict):
    body = body or {}
    if what == "map":
        try:
            usd = float(str(body.get("usd") or "").replace("$", "").replace(",", ""))
        except ValueError:
            return 400, {"error": "usd must be a number"}
        if usd <= 0 or usd > 10000:
            return 400, {"error": "usd out of range"}
        rec = {"id": f"{brain.brand}.offers.map_usd_per_pair", "brand": brain.brand, "section": "offers", "field": "map_usd_per_pair", "value": usd,
               "text": f"Minimum advertised price is ${usd:,.2f} a pair on every marketplace.", "tier": "approved", "confidence": 1.0, "visibility": "private",
               "source": {"type": "founder", "ref": "05-brand-brain marketplace parity", "captured_at": brain.today.isoformat()}}
    elif what == "sellers":
        names = [str(n).strip() for n in (body.get("names") if isinstance(body.get("names"), list) else str(body.get("names") or "").split(",")) if str(n).strip()]
        if not names:
            return 400, {"error": "names is empty"}
        rec = {"id": f"{brain.brand}.offers.marketplace_seller_names", "brand": brain.brand, "section": "offers", "field": "marketplace_seller_names", "value": names,
               "text": "Our marketplace seller names: " + ", ".join(names) + ".", "tier": "approved", "confidence": 1.0, "visibility": "private",
               "source": {"type": "founder", "ref": "05-brand-brain marketplace parity", "captured_at": brain.today.isoformat()}}
    else:
        return 404, {"error": "set map or sellers"}
    errs = founder_put(brain, rec)
    if errs:
        return 400, {"error": "record not valid", "details": errs}
    return 201, {"ok": True, "record": rec["id"], "version": brain.version()}


def rank(brand: str = "bombas", window: dict | None = None) -> dict:
    """The screen's own ranked actions (depth.md section 5): real titles, steps, artefacts and drafts for BRN-R01 to R12.
    app/rank.py picks this up for GET /api/05-brand-brain/rank and for the master list."""
    return ranking.rank(brand, window, lambda b, w: audit.run(b, w, BRAIN_ROOT))


# which screens read each profile section: a static scan of the screens' api code, plus the T0 card readers
READ_PATTERNS = (re.compile(r"""records\(\s*["']([a-z_]+)["']"""), re.compile(r"""for sec in \(([^)]*)\)"""))


def _log_read(brain: Brain, sections, reader: str | None) -> None:
    """Stamp a read in the store's read log when the caller names itself (?reader=<screen or agent>)."""
    if not reader or not hasattr(brain, "log_read"):
        return
    reader = re.sub(r"[^A-Za-z0-9_.:-]+", "", str(reader))[:80]
    if not reader:
        return
    for sec in ([sections] if isinstance(sections, str) else sections):
        brain.log_read(sec, reader)


def flows(brain: Brain) -> dict:
    """Which screens read each profile section and when they last read it. Readers come from a code scan of app/screens/*/api.py
    and from the store's read log (reads.log.jsonl, written when a caller names itself with ?reader=); last_read is the log's newest line."""
    readers: dict[str, set] = {}
    t0_readers: set = set()
    root = APP / "screens"
    for d in sorted(p for p in root.iterdir() if p.is_dir() and p.name != "05-brand-brain"):
        api_py = d / "api.py"
        if not api_py.is_file():
            continue
        try:
            t = api_py.read_text(encoding="utf-8")
        except OSError:
            continue
        secs = set(READ_PATTERNS[0].findall(t))
        for g in READ_PATTERNS[1].findall(t):
            secs |= set(re.findall(r"""["']([a-z_]+)["']""", g))
        for sec in secs:
            readers.setdefault(sec, set()).add(d.name)
        if "t0_card" in t or "package" in t:
            t0_readers.add(d.name)
    out = []
    for sec, label, first in PROFILE_SECTIONS:
        recs = brain.records(sec)
        approved = [r for r in recs if r["tier"] == "approved"]
        newest_founder = max((r["date"] for r in approved if r["date"] != "undated"), default=None)
        direct = sorted(readers.get(sec, set()))
        logged = brain.reads(sec) if hasattr(brain, "reads") else []
        last = logged[-1] if logged else None
        logged_readers = sorted({r.get("reader") for r in logged if r.get("reader")})
        out.append({"section": sec, "label": label, "records": len(recs), "approved": len(approved), "last_founder_edit": newest_founder,
                    "read_by": direct, "read_by_t0": sorted(t0_readers), "read_by_log": logged_readers, "reads_logged": len(logged), "flows_to": FLOWS_TO.get(sec, ""),
                    "last_read": last.get("at") if last else None, "last_reader": last.get("reader") if last else None,
                    "last_read_reason": None if last else "no read logged yet; a screen or agent stamps one by naming itself (?reader=) when it reads this section",
                    "reach": len(set(direct) | t0_readers | set(logged_readers))})
    return {"sections": out, "screens_scanned": sum(1 for p in root.iterdir() if p.is_dir() and (p / "api.py").is_file()) - 1,
            "note": "Read by: screens whose api reads the section from the brain store, from a scan of their code. T0: screens that read the compact brand card, which carries every profile section. An edit here reaches them on their next load."}


def handle(req):
    try:
        brain = _brain(req)
    except (ValueError, FileNotFoundError) as exc:
        return 404, {"error": str(exc)}
    parts = req.path
    if req.method == "GET" and parts == ["overview"]:
        return overview(brain)
    if req.method == "GET" and parts == ["master"]:
        return master(brain, _window(req, brain))
    if req.method == "GET" and parts == ["profile"]:
        _log_read(brain, [sec for sec, _, _ in PROFILE_SECTIONS], req.arg("reader"))
        return profile(brain)
    if req.method == "POST" and len(parts) == 3 and parts[0] == "profile":
        return profile_edit(brain, parts[1], parts[2], req.body)
    if req.method == "GET" and parts == ["documents"]:
        return documents(brain)
    if req.method == "POST" and parts == ["documents"]:
        return document_add(brain, req.body)
    if req.method == "POST" and parts == ["documents", "extract"]:
        return document_extract(brain, req.body)
    if req.method == "GET" and parts == ["competitors"]:
        return competitors(brain)
    if req.method == "GET" and parts == ["conflicts"]:
        cv = conflicts_view(brain)
        cv.update(brand=brain.brand, today=brain.today.isoformat(), version=brain.version())
        return cv
    if req.method == "POST" and len(parts) == 2 and parts[0] == "conflicts":
        return conflict_resolve(brain, parts[1], req.body)
    if req.method == "GET" and parts == ["health"]:
        h = health.heatmap(brain)
        h["connectors"] = health.connectors(brain)
        h.update(brand=brain.brand, today=brain.today.isoformat(), version=brain.version())
        return h
    if req.method == "GET" and parts == ["health", "cell"]:
        sec, tier = req.arg("section", ""), req.arg("tier", "")
        return {"section": sec, "tier": tier, "records": health.records_in_cell(brain, sec, tier)}
    if req.method == "POST" and len(parts) == 2 and parts[0] == "approve":
        return approve(brain, parts[1], req.body)
    if req.method == "GET" and parts == ["signals"]:
        sg = market.signals(brain)
        sg.update(brand=brain.brand, today=brain.today.isoformat(), version=brain.version())
        return sg
    if req.method == "POST" and parts == ["competitors", "page-id"]:
        return page_id_add(brain, req.body)
    if req.method == "GET" and parts == ["coverage"]:
        c = market.coverage(brain)
        c.update(brand=brain.brand, today=brain.today.isoformat(), version=brain.version())
        return c
    if req.method == "GET" and parts == ["records"]:
        sec = req.arg("section", "")
        if sec not in SECTIONS:
            return 404, {"error": "no such section", "section": sec}
        _log_read(brain, sec, req.arg("reader"))
        return {"section": sec, "records": [record_view(r) for r in brain.records(sec)]}
    if req.method == "GET" and parts == ["audit"]:
        ends = (brain.today - dt.timedelta(days=1)).isoformat()
        findings = audit.run(brain.brand, {"ends_on": ends, "days": 1, "trailing": 0}, BRAIN_ROOT)
        return {"findings": findings, "rules": audit.RULES, "brain_version": brain.version()}
    if req.method == "GET" and parts == ["visibility"]:
        v = visibility.audit(brain)
        v["capability"] = {"id": "LOOP-C22", "autonomy": "founder_gate"}
        return v
    if req.method == "POST" and parts == ["visibility"]:
        body = req.body or {}
        ids = body.get("ids") if isinstance(body.get("ids"), list) else ([body.get("id")] if body.get("id") else [])
        vis = str(body.get("visibility") or "")
        if not ids:
            return 400, {"error": "send id or ids"}
        before_v = brain.version()
        done, failed = [], []
        for rid in [str(x) for x in ids][:200]:
            res = visibility.set_visibility(brain, rid, vis)
            if isinstance(res, tuple):
                failed.append({"id": rid, "error": res[1].get("error")})
            else:
                done.append(res)
                if res["changed"]:
                    changes.log(brain, "visibility", rid.split(".")[1], rid, f"{rid}: visibility {res['before']} to {vis}", before=res["before"], after=vis)
        changes.version_step(brain, before_v, f"visibility set on {len(done)} records")
        return 201, {"ok": not failed, "done": done, "failed": failed, "changed": sum(1 for d in done if d["changed"]), "version": brain.version()}
    if req.method == "POST" and parts == ["visibility", "fix"]:
        v = visibility.audit(brain)
        which = str((req.body or {}).get("which") or "all")
        todo = (v["leaks"] if which in ("all", "leaks") else []) + (v["restricted"] if which in ("all", "restricted") else [])
        before_v = brain.version()
        done, failed = [], []
        for x in todo[:200]:
            res = visibility.set_visibility(brain, x["id"], x["fix"])
            if isinstance(res, tuple):
                failed.append({"id": x["id"], "error": res[1].get("error")})
            else:
                done.append(x["id"])
                changes.log(brain, "visibility", x["section"], x["id"], f"{x['id']}: visibility to {x['fix']} ({x['why']})", before=("public" if x["fix"] == "private" else "private"), after=x["fix"])
        changes.version_step(brain, before_v, f"visibility fixed on {len(done)} records")
        left = visibility.audit(brain)
        return 201, {"ok": not failed, "fixed": len(done), "failed": failed, "left": {"leaks": len(left["leaks"]), "restricted": len(left["restricted"])}, "version": brain.version()}
    if req.method == "GET" and parts == ["newbrand"]:
        root = BRAIN_ROOT or (APP / "brain")
        return {"brains": newbrand.brains(root), "lanes": newbrand.lanes(), "markets": list(newbrand.MARKETS), "capability": {"id": "BRN-C13", "autonomy": "founder_gate"},
                "note": "The intake writes a brain folder from your words only: name, store url, category, market, the Apify config with nothing confirmed, an empty documents manifest, the 5 opening questions and BRAIN.md. Nothing is crawled or paid. The dry run replays saved fixtures offline."}
    if req.method == "POST" and parts == ["newbrand"]:
        root = BRAIN_ROOT or (APP / "brain")
        res = newbrand.skeleton(Path(root), req.body or {}, brain.today)
        if isinstance(res, tuple):
            return res
        changes.log(brain, "brand", None, None, f"new brain started: {res['slug']} ({res['name']}, {res['url']})")
        return 201, res
    if req.method == "POST" and parts == ["newbrand", "dryrun"]:
        out_root = (Path(BRAIN_ROOT) / ".mock-onboard") if BRAIN_ROOT else newbrand.onboard.MOCK_ROOT
        res = newbrand.dryrun(req.body or {}, out_root, brain.today)
        if isinstance(res, tuple):
            return res
        return 201, res
    if req.method == "GET" and parts == ["visual"]:
        pal = visual.palette(brain)
        pal["capability"] = {"id": "CREA-C12", "autonomy": "agent_does"}
        return pal
    if req.method == "POST" and parts == ["visual", "check"]:
        body = req.body or {}
        if body.get("content_base64"):
            res = visual.check_png(brain, body["content_base64"])
            if isinstance(res, tuple):
                return res
            return dict(res, kind="png", name=str(body.get("name") or "")[:80])
        text = str(body.get("text") or "")
        if not text.strip():
            return 400, {"error": "send text (CSS, HTML or hex codes) or a PNG as content_base64"}
        return dict(visual.check_text(brain, text), kind="text")
    if req.method == "POST" and parts == ["visual", "logo"]:
        body = req.body or {}
        if not any(body.get(k) for k in ("min_size_px", "clear_space", "never", "backgrounds")):
            return 400, {"error": "set at least one of min_size_px, clear_space, never, backgrounds"}
        rec = visual.logo_record(brain, body)
        errs = founder_put(brain, rec, "logo", rec["text"][:160])
        if errs:
            return 400, {"error": "; ".join(errs)}
        return 201, {"ok": True, "record": rec["id"], "text": rec["text"], "version": brain.version()}
    if req.method == "GET" and parts == ["history"]:
        rid = req.arg("record", "") or ""
        if not re.fullmatch(r"[a-z0-9_-]+\.[a-z_]+\.[A-Za-z0-9_.-]{1,120}", rid):
            return 400, {"error": "record must be a record id"}
        t = history.timeline(brain, rid)
        if t is None:
            return 404, {"error": "no such record", "id": rid}
        return t
    if req.method == "POST" and parts == ["history", "restore"]:
        body = req.body or {}
        rid = str(body.get("record") or "")
        if not re.fullmatch(r"[a-z0-9_-]+\.[a-z_]+\.[A-Za-z0-9_.-]{1,120}", rid):
            return 400, {"error": "record must be a record id"}
        res = history.restore(brain, rid, body.get("index"))
        if isinstance(res, tuple):
            return res
        errs = founder_put(brain, res["record"], "restore", f"{rid}: restored the value from {res['record']['source']['restored_from'].get('changed_at') or 'an earlier version'}")
        if errs:
            return 400, {"error": "; ".join(errs)}
        return 201, {"ok": True, "record": rid, "before": res["before"], "after": res["after"], "version": brain.version(), "next": "Restored as your approved record. The value it replaced is in the history; every screen reads the restored one."}
    if req.method == "GET" and parts == ["peaks"]:
        r = peaks.readiness(brain, market.angles_of, legal, assumptions)
        r["capability"] = {"id": "BRN-C07", "autonomy": "founder_gate"}
        r["simulated_note"] = None
        return r
    if req.method == "POST" and parts == ["peaks", "plan"]:
        body = req.body or {}
        key = re.sub(r"[^a-z0-9_]+", "_", str(body.get("peak") or "").lower()).strip("_")
        offer = str(body.get("offer") or "").strip()
        if not key or not offer:
            return 400, {"error": "peak and offer are required"}
        known = {p["key"]: p for p in peaks.calendar(brain, market.angles_of)}
        pk = known.get(key)
        label = (pk or {}).get("label") or str(body.get("label") or key.replace("_", " "))
        date = (pk["date"].isoformat() if pk and pk.get("date") else None) or (str(body.get("date")) if body.get("date") else None)
        scan_res = claims_mod.scan(brain, offer)
        if scan_res["verdict"] == "fail":
            return 400, {"error": "the offer wording fails the claims scan", "hits": scan_res["hits"][:5]}
        errs = []
        for rec in peaks.plan(brain, key, label, date, offer, str(body.get("note") or ""), body.get("cutoff")):
            errs += founder_put(brain, rec, "peak", f"{label}: {rec['section'].replace('_', ' ')} {rec['field'].replace('_', ' ')} set")
        if errs:
            return 400, {"error": "; ".join(errs)}
        return 201, {"ok": True, "peak": key, "records": [f"{brain.brand}.offers.peak_{key}", f"{brain.brand}.calendar.peak_{key}"] + ([f"{brain.brand}.policies.holiday_shipping_cutoff"] if body.get("cutoff") else []),
                     "warns": [h["match"] for h in scan_res["hits"] if h["severity"] == "warn"][:5], "version": brain.version(), "next": f"{label} has an offer on file; every screen reads it. The creative brief and the send plan stay on the master list until done."}
    if req.method == "GET" and parts == ["selfaudit"]:
        sa = selfaudit.run(brain)
        sa["capability"] = {"id": "BRN-C12", "autonomy": "agent_does"}
        return sa
    if req.method == "POST" and parts == ["selfaudit", "regenerate"]:
        before_v = brain.version()
        drift_before = len(selfaudit.brain_audit.drift(brain))
        changes.log(brain, "router", None, None, f"BRAIN.md regenerated from the records: {drift_before} drifted rows before")  # logged first, so the version line in the new file is final
        try:
            res = selfaudit.regenerate(brain)
        except (ValueError, OSError) as e:
            return 400, {"error": str(e)}
        changes.version_step(brain, before_v, "BRAIN.md regenerated")
        return 201, dict(res, drift_before=drift_before, version=brain.version())
    if req.method == "POST" and parts == ["selfaudit", "retire"]:
        body = req.body or {}
        rid, keep = str(body.get("retire") or ""), str(body.get("keep") or "")
        dups = selfaudit.duplicates(brain)
        pair = next((d for d in dups if d["retire"] == rid and (not keep or d["keep"] == keep)), None)
        if pair is None:
            return 404, {"error": "no duplicate pair with that record to retire", "retire": rid, "keep": keep or None}
        before_v = brain.version()
        if not brain.retire(rid):
            return 404, {"error": "no such record", "id": rid}
        changes.log(brain, "retired", pair["section"], rid, f"retired {rid}, a duplicate of {pair['keep']} ({pair['match']})", before=rid, after=pair["keep"])
        changes.version_step(brain, before_v, f"retired duplicate {rid}")
        return 201, {"ok": True, "retired": rid, "kept": pair["keep"], "left": len(selfaudit.duplicates(brain)), "version": brain.version()}
    if req.method == "GET" and parts == ["ladders", "proof"]:
        m = ladderproof.matrix(brain, claims_mod)
        m["capability"] = {"id": "BRN-C03", "autonomy": "agent_does"}
        return m
    if req.method == "POST" and parts == ["ladders", "proof"]:
        body = req.body or {}
        res = ladderproof.attach(brain, str(body.get("theme") or ""), body.get("level"), str(body.get("record_id") or ""))
        if isinstance(res, tuple):
            return res
        errs = founder_put(brain, res["record"], "proof", f"{res['record']['value'].get('theme', '').replace('_', ' ')} rung {res['rung'].get('level')}: proof set to {body.get('record_id')}")
        if errs:
            return 400, {"error": "; ".join(errs)}
        return 201, {"ok": True, "record": res["record"]["id"], "proof_id": body.get("record_id"), "proof_tier": res["proof_tier"], "usable": res["usable"], "version": brain.version(),
                     "next": ("The rung is proved; its surfaces read it on the next brief." if res["usable"] else f"Attached, but the record is {res['proof_tier'].replace('_', ' ')}: approve it in the claims desk before a surface uses it.")}
    if req.method == "GET" and parts == ["bottlenecks"]:
        return bottlenecks_view(brain, _window(req, brain))
    if req.method == "POST" and parts == ["bottlenecks", "pick"]:
        return idea_pick(brain, req.body)
    if req.method == "GET" and parts == ["channels"]:
        cs = claims_mod.channel_sets(brain)
        cs["capability"] = {"id": "BRN-C03", "autonomy": "founder_gate"}
        return cs
    if req.method == "POST" and len(parts) == 2 and parts[0] == "channels" and parts[1] in claims_mod.CHANNELS:
        ch = parts[1]
        body = req.body or {}
        pattern = str(body.get("pattern") or "").strip()[:200]
        kind = str(body.get("kind") or "warn")
        if not pattern:
            return 400, {"error": "pattern is required: a phrase, or a regex when regex is true"}
        if kind not in claims_mod.RULE_KINDS:
            return 400, {"error": "kind must be fail, warn or must"}
        if body.get("regex"):
            try:
                re.compile(pattern)
            except re.error as e:
                return 400, {"error": f"regex does not compile: {e}"}
        n = 1 + sum(1 for r in brain.records("claims", include_retired=True) if (r.get("field") or "").startswith(f"channel_rule_{ch}_"))
        rec = {"id": f"{brain.brand}.claims.channel_rule_{ch}_{n}", "brand": brain.brand, "section": "claims", "field": f"channel_rule_{ch}_{n}",
               "value": {"channel": ch, "pattern": pattern, "regex": bool(body.get("regex")), "kind": kind, "why": str(body.get("why") or "")[:160] or None, "fix": str(body.get("fix") or "")[:160] or None},
               "text": f"{claims_mod.CHANNELS[ch]['label']} rule ({kind}): " + (f"the draft must contain '{pattern}'" if kind == "must" else f"'{pattern}' {'blocks' if kind == 'fail' else 'flags'} the draft") + (f". {body.get('why')}" if body.get("why") else "."),
               "tier": "approved", "confidence": 1.0, "visibility": "private", "source": {"type": "founder", "ref": "05-brand-brain channel rules", "captured_at": brain.today.isoformat()}}
        errs = founder_put(brain, rec, "rule", rec["text"][:160])
        if errs:
            return 400, {"error": "; ".join(errs)}
        return 201, {"ok": True, "record": rec["id"], "channel": ch, "version": brain.version(), "next": "The scanner applies it on every draft for this channel from now on."}
    if req.method == "POST" and len(parts) == 3 and parts[0] == "channels" and parts[1] in claims_mod.CHANNELS and parts[2] in ("mute", "remove"):
        ch = parts[1]
        body = req.body or {}
        before_v = brain.version()
        if parts[2] == "mute":
            idx = body.get("index")
            if not isinstance(idx, int) or not (0 <= idx < len(claims_mod.CHANNELS[ch]["rules"])):
                return 400, {"error": "index must name a built-in rule"}
            existing = next((r for r in brain.raw("claims") if (r.get("field") or "") == f"channel_mute_{ch}_{idx}" and r.get("status", "active") != "retired"), None)
            if existing:
                brain.retire(existing["id"])
                changes.log(brain, "rule", "claims", existing["id"], f"{claims_mod.CHANNELS[ch]['label']}: built-in rule {idx} unmuted")
                changes.version_step(brain, before_v, f"unmuted {ch} rule {idx}")
                return 201, {"ok": True, "muted": False, "index": idx, "version": brain.version()}
            why = claims_mod.CHANNELS[ch]["rules"][idx][2]
            rec = {"id": f"{brain.brand}.claims.channel_mute_{ch}_{idx}", "brand": brain.brand, "section": "claims", "field": f"channel_mute_{ch}_{idx}", "value": {"channel": ch, "index": idx, "why": why},
                   "text": f"{claims_mod.CHANNELS[ch]['label']} built-in rule muted by the founder: {why}.", "tier": "approved", "confidence": 1.0, "visibility": "private", "source": {"type": "founder", "ref": "05-brand-brain channel rules", "captured_at": brain.today.isoformat()}}
            errs = founder_put(brain, rec, "rule", rec["text"][:160])
            if errs:
                return 400, {"error": "; ".join(errs)}
            return 201, {"ok": True, "muted": True, "index": idx, "version": brain.version()}
        rid = str(body.get("record") or "")
        raw = next((r for r in brain.raw("claims") if r.get("id") == rid and (r.get("field") or "").startswith(f"channel_rule_{ch}_")), None)
        if raw is None:
            return 404, {"error": "no founder rule with that id on this channel", "record": rid}
        brain.retire(rid)
        changes.log(brain, "rule", "claims", rid, f"{claims_mod.CHANNELS[ch]['label']} rule removed (retired): {str(raw.get('text'))[:100]}")
        changes.version_step(brain, before_v, f"removed {rid}")
        return 201, {"ok": True, "removed": rid, "version": brain.version()}
    if req.method == "GET" and parts == ["moves"]:
        window = _window(req, brain)
        try:
            actions = rank_mod.master(brain.brand, window)["actions"]
        except Exception:  # noqa: BLE001
            actions = rank(brain.brand, window)["actions"]
        d = bottlenecks.diagnosis(brain)
        try:
            cov = market.coverage(brain)
        except Exception:  # noqa: BLE001
            cov = {"gaps": [], "contested": []}
        try:
            gp = market.gaps(brain)
        except Exception:  # noqa: BLE001
            gp = []
        try:
            sg = market.signals(brain)
        except Exception:  # noqa: BLE001
            sg = {}
        out = moves.counter_proposals(brain, d["bottlenecks"], cov, gp if isinstance(gp, list) else (gp.get("gaps") or []), sg, actions)
        out.update(brand=brain.brand, today=brain.today.isoformat(), bottlenecks=[{"key": b["key"], "theme": b["theme"], "rank": b["rank"]} for b in d["bottlenecks"]], capability={"id": "BRN-C11", "autonomy": "agent_does"})
        return out
    if req.method == "POST" and parts == ["bottlenecks", "reject"]:
        body = req.body or {}
        idea_id = str(body.get("idea_id") or "").strip().upper()
        if not re.fullmatch(r"[A-Z]{2,6}-\d{3,4}", idea_id):
            return 400, {"error": "idea_id must be a bank id like OFF-103"}
        res = bottlenecks.reject(brain, idea_id, str(body.get("bottleneck") or "").strip() or None, str(body.get("reason") or "").strip(), str(body.get("review_on") or "").strip() or None)
        if not res["ok"]:
            return (404 if res.get("error") == "no such idea" else 400), res
        errs = founder_put(brain, res["record"], kind="founder_edit", what=f"rejected idea {idea_id}: {res['record']['value']['title'][:80]}")
        if errs:
            return 400, {"error": "record not valid", "details": errs}
        return 201, {"ok": True, "record": res["record"]["id"], "idea_id": idea_id, "review_on": res["record"]["value"]["review_on"], "next": f"Out until {res['record']['value']['review_on']}. Agents read the learnings before proposing; the rule brings it back for review on that date.", "version": brain.version()}
    if req.method == "POST" and parts == ["bottlenecks", "unreject"]:
        body = req.body or {}
        idea_id = str(body.get("idea_id") or "").strip().upper()
        rej = bottlenecks.rejected_ideas(brain).get(idea_id)
        if rej is None:
            return 404, {"error": "no rejected idea with that id", "idea_id": idea_id}
        before_v = brain.version()
        brain.retire(rej["record"])
        changes.log(brain, "retired", "learnings", rej["record"], f"brought back idea {idea_id}: the rejection is retired, never deleted")
        changes.version_step(brain, before_v, f"unrejected {idea_id}")
        return 201, {"ok": True, "idea_id": idea_id, "retired": rej["record"], "next": "Back in the unlocks. The rejection stays in history.", "version": brain.version()}
    if req.method == "GET" and parts == ["report"]:
        try:
            days = max(1, min(90, int(req.arg("days", "7") or 7)))
        except ValueError:
            days = 7
        return report_view(brain, days)
    if req.method == "GET" and parts == ["digest"]:
        return digest_view(brain)
    if req.method == "GET" and parts == ["learn"]:
        lv = learn_view(brain)
        lv.update(brand=brain.brand, today=brain.today.isoformat(), version=brain.version())
        return lv
    if req.method == "POST" and parts == ["learn", "apply"]:
        return learn_apply(brain, req.body)
    if req.method == "GET" and parts == ["summaries"]:
        sm = summaries(brain)
        sm.update(brand=brain.brand, today=brain.today.isoformat(), version=brain.version())
        return sm
    if req.method == "GET" and parts == ["package"]:
        res = package_view(brain, req.arg("capability", "") or "")
        if not isinstance(res, tuple):
            _log_read(brain, [p["section"] for p in res["parts"] if p.get("section")], req.arg("reader") or res["capability"])
            if res.get("record_ids"):
                trail.log_records(brain, req.arg("reader") or res["capability"], res["record_ids"], res.get("public_facing"))
        return res
    if req.method == "GET" and parts == ["facts"]:
        fp = facts.pairs(brain)
        fp.update(brand=brain.brand, today=brain.today.isoformat(), version=brain.version())
        return fp
    if req.method == "GET" and parts == ["facts", "export"]:
        return facts.export(brain)
    if req.method == "POST" and len(parts) == 2 and parts[0] == "facts":
        return fact_approve(brain, parts[1], req.body)
    if req.method == "GET" and parts == ["assumptions"]:
        try:
            rooms = health.rooms_by_section(keeper.load_bank())
        except (OSError, ValueError, KeyError):
            rooms = {}
        ar = assumptions.register(brain, rooms)
        ar.update(brand=brain.brand, today=brain.today.isoformat(), version=brain.version())
        return ar
    if req.method == "POST" and len(parts) == 2 and parts[0] == "assumptions":
        return assumption_set(brain, parts[1], req.body)
    if req.method == "GET" and parts == ["changes"]:
        ch = changes.recent(brain)
        ch.update(brand=brain.brand, today=brain.today.isoformat(), version=brain.version())
        return ch
    if req.method == "GET" and parts == ["dependents"]:
        rid = req.arg("record", "") or ""
        if not re.fullmatch(r"[a-z0-9_-]+\.[a-z_]+\.[A-Za-z0-9_.-]{1,120}", rid):
            return 400, {"error": "record must be a record id"}
        return changes.dependents(brain, rid)
    if req.method == "GET" and parts == ["permissions"]:
        pm = health.permissions(brain)
        pm.update(brand=brain.brand, today=brain.today.isoformat(), version=brain.version())
        return pm
    if req.method == "POST" and len(parts) == 2 and parts[0] == "permissions":
        return permission_set(brain, parts[1], req.body)
    if req.method == "GET" and parts == ["export"]:
        return health.export_bundle(brain)
    if req.method == "POST" and parts == ["export", "diff", "start"]:
        up = brain.dir / "review" / "uploads"
        up.mkdir(parents=True, exist_ok=True)
        token = base64.urlsafe_b64encode(hashlib.sha256(f"{brain.brand}{dt.datetime.now(dt.timezone.utc).isoformat()}{len(list(up.iterdir()))}".encode()).digest()[:12]).decode().rstrip("=")
        (up / f"{token}.b64").write_text("", encoding="utf-8")
        return 201, {"token": token, "part_max_bytes": 24000, "note": "the server takes 32 KB per request; send the export as base64 parts in order, then finish"}
    if req.method == "POST" and parts == ["export", "diff", "part"]:
        body = req.body or {}
        token, data = str(body.get("token") or ""), str(body.get("data") or "")
        if not re.fullmatch(r"[A-Za-z0-9_-]{8,24}", token) or not data:
            return 400, {"error": "token and data are required"}
        f = brain.dir / "review" / "uploads" / f"{token}.b64"
        if not f.is_file():
            return 404, {"error": "no upload with that token; start again"}
        if f.stat().st_size + len(data) > 8_000_000:
            f.unlink(missing_ok=True)
            return 413, {"error": "the upload is over 8 MB; export a smaller brain"}
        with f.open("a", encoding="utf-8") as fh:
            fh.write(data)
        return 201, {"ok": True, "bytes": f.stat().st_size}
    if req.method == "POST" and parts == ["export", "diff", "finish"]:
        token = str((req.body or {}).get("token") or "")
        f = brain.dir / "review" / "uploads" / f"{token}.b64"
        if not re.fullmatch(r"[A-Za-z0-9_-]{8,24}", token) or not f.is_file():
            return 404, {"error": "no upload with that token; start again"}
        try:
            bundle = json.loads(base64.b64decode(f.read_text(encoding="utf-8"), validate=True).decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            f.unlink(missing_ok=True)
            return 400, {"error": "the upload is not a JSON export"}
        f.unlink(missing_ok=True)
        return braindiff.diff(brain, bundle, SECTIONS)
    if req.method == "POST" and parts == ["export", "diff"]:
        body = req.body or {}
        bundle = body.get("bundle")
        if bundle is None and body.get("content_base64"):
            try:
                bundle = json.loads(base64.b64decode(str(body["content_base64"]), validate=True).decode("utf-8"))
            except (ValueError, UnicodeDecodeError):
                return 400, {"error": "the file is not JSON"}
        if not isinstance(bundle, dict):
            return 400, {"error": "send bundle (the export JSON) or content_base64"}
        return braindiff.diff(brain, bundle, SECTIONS)
    if req.method == "GET" and parts == ["battlecards"]:
        bc = battlecards.cards(brain)
        bc.update(brand=brain.brand, today=brain.today.isoformat(), version=brain.version())
        return bc
    if req.method == "GET" and parts == ["ask"]:
        q = (req.arg("q", "") or "")[:300]
        return ask.search(brain, q)
    if req.method == "POST" and parts == ["ask", "open"]:
        q = str((req.body or {}).get("q") or "").strip()
        if len(q) < 4:
            return 400, {"error": "q is empty"}
        res = ask.to_open_question(brain, q[:300], str((req.body or {}).get("why") or ""))
        return (201, dict(res, version=brain.version())) if res["ok"] else (400, {"error": "record not valid", "details": res["errors"]})
    if req.method == "GET" and parts == ["voice"]:
        vs = voice.sheet(brain)
        vs["snippets"] = voice.snippets(brain)
        vs.update(brand=brain.brand, today=brain.today.isoformat(), version=brain.version())
        return vs
    if req.method == "POST" and parts == ["voice", "example"]:
        return voice_example(brain, req.body)
    if req.method == "POST" and len(parts) == 3 and parts[:2] == ["voice", "snippet"]:
        return snippet_lock(brain, parts[2], req.body)
    if req.method == "GET" and parts == ["contracts"]:
        cr = contracts.register(brain)
        cr.update(brand=brain.brand, today=brain.today.isoformat(), version=brain.version())
        return cr
    if req.method == "POST" and parts == ["contracts"]:
        return contract_add(brain, req.body)
    if req.method == "GET" and parts == ["legal"]:
        lg = legal.checks(brain)
        lg.update(brand=brain.brand, today=brain.today.isoformat(), version=brain.version(), kinds=legal.KINDS)
        return lg
    if req.method == "POST" and parts == ["legal", "gate"]:
        text = str((req.body or {}).get("text") or "")
        if not text.strip():
            return 400, {"error": "text is empty"}
        return legal.gate(brain, str((req.body or {}).get("kind") or "pdp"), text[:20000], claims_mod)
    if req.method == "GET" and parts == ["parity"]:
        pv = parity.strip(brain)
        pv.update(brand=brain.brand, today=brain.today.isoformat(), version=brain.version())
        return pv
    if req.method == "POST" and len(parts) == 2 and parts[0] == "parity":
        return parity_set(brain, parts[1], req.body)
    if req.method == "GET" and parts == ["site", "diff"]:
        sd = sitediff.diff(brain)
        sd.update(brand=brain.brand, today=brain.today.isoformat(), version=brain.version())
        return sd
    if req.method == "POST" and parts == ["site", "snapshot"]:
        res = sitediff.take(brain, (req.body or {}).get("date") or None)
        if res.get("ok"):
            sd = sitediff.diff(brain)
            changes.log(brain, "snapshot", "site_map", None, f"snapshot {res['date']}, {res['records']} records" + (f", {sd['counts']['changes']} changes since {sd['old']}" if sd.get("pair") else ""))
            for c in (sd.get("changes") or []):
                if not c.get("reviewed"):
                    dep = changes.dependents(brain, c["id"])
                    changes.log(brain, "site", c["section"], c["id"], f"{c['section']} {c.get('field') or ''} {c['change']}: {c['old_text']} to {c['new_text']}. Depends on it: {dep['summary']}", source="site crawl", before=c["old"], after=c["new"])
        return (201, res) if res.get("ok") else (400, res)
    if req.method == "POST" and parts == ["site", "reviewed"]:
        ids = [str(i) for i in ((req.body or {}).get("ids") or []) if isinstance(i, str)]
        sd = sitediff.diff(brain)
        if not sd.get("pair"):
            return 400, {"error": "no diff to review", "reason": sd.get("unavailable_reason")}
        if not ids:
            return 400, {"error": "ids is empty"}
        return 201, dict(sitediff.mark_reviewed(brain, sd["pair"], ids), ok=True)
    if req.method == "GET" and parts == ["claims"]:
        cd = claims_mod.desk(brain)
        cd.update(brand=brain.brand, today=brain.today.isoformat(), version=brain.version())
        return cd
    if req.method == "POST" and parts == ["claims"]:
        return claim_add(brain, req.body)
    if req.method == "GET" and parts == ["trail"]:
        try:
            days = max(1, min(90, int(req.arg("days", "7") or 7)))
        except ValueError:
            days = 7
        t = trail.weekly(brain, days)
        t.update(brand=brain.brand, today=brain.today.isoformat(), capability={"id": "LOOP-C29", "autonomy": "founder_gate"})
        return t
    if req.method == "GET" and parts == ["agentfile", "endpoints"]:
        rows = agentfile.endpoints(__doc__ or "")
        return {"screen": "05-brand-brain", "brand": brain.brand, "endpoints": rows, "counts": {"routes": len(rows), "read_only": sum(1 for r in rows if r["read_only"])},
                "note": "This screen's routes, parsed from its own route table. GET routes are read-only. Name yourself with ?reader=<capability id> on a read so the read is logged. There is no write to any external system."}
    if req.method == "GET" and parts == ["agentfile"]:
        cap = (req.arg("capability", "") or "").upper()
        pv = package_view(brain, cap)
        if isinstance(pv, tuple):
            return pv
        res = agentfile.build(brain, cap, pv, {"claims": claims_mod, "voice": voice, "visibility": visibility, "ladderproof": ladderproof, "market": market, "package": package_mod})
        _log_read(brain, [p["section"] for p in pv["parts"] if p.get("section")], req.arg("reader") or cap)
        if pv.get("record_ids"):
            trail.log_records(brain, req.arg("reader") or cap, pv["record_ids"], pv.get("public_facing"))
        res["name"] = pv.get("name")
        return res
    if req.method == "GET" and parts == ["brainmd"]:
        p = brain.dir / "BRAIN.md"
        try:
            text = p.read_text(encoding="utf-8") if p.is_file() else None
        except OSError:
            text = None
        if text is None:
            return 404, {"error": "no BRAIN.md for this brand; regenerate it from the self audit"}
        return {"file": "BRAIN.md", "text": text, "tokens": package_mod.tokens(text), "version": brain.version()}
    if req.method == "POST" and parts == ["review", "draft"]:
        text = str((req.body or {}).get("text") or "")
        if not text.strip():
            return 400, {"error": "text is empty"}
        if len(text) > 20000:
            return 413, {"error": "text is over 20,000 characters"}
        channel = (req.body or {}).get("channel") or None
        kind = (req.body or {}).get("kind") or None
        return reviewer.review(brain, text, channel, kind, claims_mod, legal, voice, visual)
    if req.method == "POST" and parts == ["scan"]:
        text = str((req.body or {}).get("text") or "")
        if not text.strip():
            return 400, {"error": "text is empty"}
        if len(text) > 20000:
            return 413, {"error": "text is over 20,000 characters"}
        channel = (req.body or {}).get("channel")
        return claims_mod.channel_scan(brain, text, channel) if channel else dict(claims_mod.scan(brain, text), channel=None, channel_hits=[], channels=sorted(claims_mod.CHANNELS))
    if req.method == "GET" and parts == ["flows"]:
        fl = flows(brain)
        fl.update(brand=brain.brand, today=brain.today.isoformat(), version=brain.version())
        return fl
    if req.method == "GET" and parts == ["decisions"]:
        dl = decisions_log(brain, _decisions_path(req))
        dl.update(brand=brain.brand, today=brain.today.isoformat(), version=brain.version())
        return dl
    if req.method == "POST" and parts == ["decisions", "undo"]:
        return decisions_undo(brain, req.body, _decisions_path(req))
    if req.method == "GET" and parts == ["questions"]:
        qv = questions_ranked(brain)
        qv.update(brand=brain.brand, today=brain.today.isoformat(), version=brain.version())
        return qv
    if req.method == "POST" and len(parts) == 3 and parts[:2] == ["questions", "bank"]:
        return answer_bank(brain, parts[2], req.body)
    if req.method == "POST" and len(parts) == 2 and parts[0] == "questions":
        return answer(brain, parts[1], req.body)
    if req.method == "GET" and parts == ["review"]:
        rv = review_view(brain)
        rv.update(brand=brain.brand, today=brain.today.isoformat(), version=brain.version())
        return rv
    if req.method == "POST" and parts == ["review", "bulk"]:
        return review_bulk(brain, req.body)
    if req.method == "POST" and len(parts) == 2 and parts[0] == "review":
        return review(brain, parts[1], req.body)
    return 404, {"error": "not found", "path": parts}
