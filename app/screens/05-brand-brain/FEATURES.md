# Brand brain: features

Status: todo | doing | done | parked. One feature per commit. The first round is the skeleton; after that, features come in rounds of 10, stack-ranked by revenue impact, usefulness and how easy they are to build on dummy data.

## Round 0: skeleton

| # | Feature | Status |
|---|---|---|
| 0.1 | Page shell in the shared UI kit: simulated-data banner, T0 card, tiles, insights, decision rows | done |
| 0.2 | `api.py`: overview, records per section, audit, answer box, review queue; reads `app/brain/<brand>/` through store.py and keeper.py | done |
| 0.3 | 3 tiles (open questions, conflicts, sections a room is missing), 2 insights as rules (founder round due at 4+ open questions, BRN-C07; source conflict, BRN-C05), 1 chart (records added per day, by first known date) | done |
| 0.4 | Section table: records, days since update, stale, mean confidence (unavailable when no record has one) | done |
| 0.5 | Record browser per section: tier, date, confidence, source link, up to 3 evidence quotes | done |
| 0.6 | Objection ladders as rungs: doubt, one-star and five-star counts, quotes, uses, proof or "no proof" | done |
| 0.7 | Open questions with an answer box: writes a founder record (`source.type` founder, tier approved) through `Brain.put` and marks the question answered | done |
| 0.8 | Review queue: proposed records, accept (active) or ignore (retired, never deleted) | done |
| 0.9 | Conflicts list from `review/conflicts.json`: both values, sources, the kept value, BRN-C05 decision row | done |
| 0.10 | `audit.py` in the audit.md shape: BRN-R01 stale section, BRN-R02 empty section a room needs, BRN-R03 unanswered high-weight question, BRN-R04 unapproved claim used by copy. 18 findings on Bombas on 28 Sep 2026 | done |

## Candidates from the room spec (pick 10 per round)

### Questions this screen should answer

- can I trust what this page is telling me right now  (BRN-C12)
- what can and can't we say about this product  (BRN-C03)
- why did we decide that, and when  (BRN-C08)
- what does the system need from me to get unstuck  (BRN-C07)
- the document says one thing and the site says another, which wins  (BRN-C05)
- did a price, a policy or a claim change without me knowing  (BRN-C01)
- is any of our data actually stale right now  (BRN-C02, BRN-C14)
- what contract needs my attention before it auto-renews  (LOOP-C28)
- is this page legally compliant before it goes live  (LOOP-C27)
- does the agency staff see more of our brain than they should  (LOOP-C29)
- is someone undercutting our price on Amazon or Walmart  (PROD-C46)
- if we part ways with this agency, can we take everything with us  (LOOP-C22)

### Metrics specified

- `section_freshness`: Days since each brain section last collected or crawled. today - last successful collection date, per section
- `confidence_tier_counts`: How many claims sit in each tier: approved, site-backed, forbidden, untiered. count of claims by tier
- `open_questions_count`: How many gaps or conflicts are waiting on a founder answer. count of open question records with no founder answer
- `conflict_count`: Facts where a document and the site (or two connectors) disagree. count of unresolved conflict records
- `site_diff_count`: Products, prices, stock, policy or claim changes since the last crawl. count of diffs between the last two site snapshots
- `connector_health_pct`: Share of connected sources that reported successfully in their own cadence. successful pulls / expected pulls, per source, rolled up
- `contract_renewal_countdown`: Days left before each vendor or platform contract renews or its rate card expires. renewal_date - today, per contract
- `legal_disclosure_pass_rate`: Share of live pages, policies and invoice templates carrying the required US disclosures. pages passing all required checks / pages checked
- `marketplace_parity_flags`: Listings where price, content or stock diverge from the brand's own D2C data, by marketplace. count of listing fields differing from the brand's stated price, stock and approved claims
- `permission_coverage_pct`: Share of brain sections with an assigned permission table entry. sections with an explicit permission entry / total sections
- `competitor_snapshot_age`: Days since each tracked competitor's ads, site and price were last captured. today - last snapshot date, per competitor
- `voice_sheet_examples_count`: How many liked, disliked and site-backed examples back the current voice sheet. count of tagged voice examples

### Insights specified (rules in code)

- claim untiered too long: a claim has sat untiered for more than 7 days → "{claim} has been untiered for {n} days and needs a founder call" (action BRN-C07)
- source conflict: a document fact and the live site disagree on the same field → "{document} says {value_a}, the site says {value_b}; the site wins by default until you say otherwise" (action BRN-C05)
- site changed unnoticed: a price, stock, policy or claim diff appears between two crawls → "{field} changed from {old} to {new} on {date}" (action BRN-C01)
- connector failing: connector_health_pct falls under 90% for a source over its own cadence → "{source} has missed {n} of its last {m} expected pulls; its fields show unavailable, not zero" (action BRN-C02)
- contract renewal approaching: contract_renewal_countdown falls inside the alert window sized for that vendor type → "{vendor} renews in {n} days; last terms were {rate} agreed on {date}" (action LOOP-C28)
- contract missing renewal date: a stored contract has no renewal date field → "{vendor}'s contract has no renewal date on file and is marked incomplete" (action LOOP-C28)
- disclosure missing: a live or about-to-ship page fails a required US disclosure check → "{page} is missing {disclosure}; this blocks going live" (action LOOP-C27)
- MAP violation: a marketplace listing price sits below the brand's stated minimum advertised price → "{marketplace} lists {product} at {price}, below your {map_price} minimum" (action PROD-C46)
- unauthorized reseller: a marketplace listing's seller name does not match the brand's own account → "An unrecognised seller is listing {product} on {marketplace}" (action PROD-C46)
- permission gap: a brain section has no assigned permission entry → "{section} has no permission set and defaults to restricted" (action LOOP-C29)
- competitor snapshot stale: competitor_snapshot_age exceeds 7 days → "{competitor} was last captured {n} days ago" (action BRN-C11)
- founder question round due: open_questions_count reaches 4 or more, or one open question blocks a running item → "{n} open questions are waiting; it is time for a founder round" (action BRN-C07)

### Visuals specified

- freshness x confidence heatmap (heatmap grid): each brain section on freshness (rows) against confidence tier (columns)
- claims tier bar (stacked bar): count of claims by tier: approved, site-backed, forbidden, untiered
- decisions log timeline (vertical timeline): founder decisions with reason and date, most recent first
- conflict table (two-column comparison table): each unresolved conflict, source A value versus source B value, with the site marked as current default
- contract renewal calendar (horizontal timeline / gantt strip): each vendor contract's renewal date with the alert window marked
- permission matrix (grid): brain sections (rows) against roles or people (columns) with view rights marked
- marketplace parity strip (small multiples per marketplace): brand's own price versus marketplace price versus MAP line, per SKU with a flag

### Not in the usual tools

- claims tiered approved, site-backed or forbidden, tied to red lines and forbidden-claim detection, not generic content staleness
- a conflict between a document and the live site resolved with a stated default (the site wins) rather than left for a person to notice
- marketplace listings diffed against the brand's own price, stock and claims the same way the D2C site is crawled
- vendor and platform contracts extracted into renewal alerts sized to how long a renegotiation takes, inside the same brain as everything else about the brand
- US legal disclosure gate (FTC, CAN-SPAM, CCPA privacy policy, sales tax on invoices, return policy, auto-renewal) checked before a page ships, as a blocking check, not a general CMS compliance plugin
- a permission map enforced the same way whether a person opens the brain directly or asks a question in chat

### Data this screen needs

- `brain_sections`: brand, section, last_collected, confidence, source, unavailable_flag (brain-keeper collectors)
- `claims`: brand, claim_text, tier, source, date, product_or_page (BRN-C03)
- `open_questions`: brand, question, raised_date, blocks, answered_date, answer (BRN-C07)
- `conflicts`: brand, field, source_a, value_a, source_b, value_b, default_winner, resolved (BRN-C05)
- `site_snapshots`: brand, page, snapshot_date, products, prices, stock, policies, claims, scripts (site crawler)
- `connector_log`: brand, source, expected_pulls, successful_pulls, last_success (BRN-C02)
- `vendor_contracts`: brand, vendor, type, renewal_date, rate_card, sla_terms, source_doc, last_diff (LOOP-C28 document reader)
- `disclosure_checks`: brand, page_or_template, check, pass_fail, checked_date (LOOP-C27)
- `marketplace_listings`: brand, marketplace, sku, price, map_price, seller_name, stock, content_diff, snapshot_date (LOOP-C30 marketplace snapshot)
- `permission_table`: brand, section, role_or_person, access_level (LOOP-C29)
- `competitor_snapshots`: brand, competitor, ads, site, prices, launches, snapshot_date (BRN-C11)
- `decisions_log`: brand, date, topic, decision, reason, person (BRN-C08)

## Rounds

| Round | Features picked | Date | Notes |
|---|---|---|---|
| 0 | skeleton, 0.1 to 0.10 | 2026-09-28 | Bombas brain (public sources); tests in tests/test_screen_brand_brain.py. No decisions, changes or contracts data yet, so those jobs wait for a later round. |
| 1 (lead sample) | top section to the depth contract: master list (plan board of the top 10 across 28 audits, connect strip, bottlenecks table), editable profile (8 sections, winning record per field, founder edits write approved records), files in (drop or url into the documents manifest); tiles and the records chart removed; screenshot `round1-sample.png` | 2026-09-28 | Built by the lead session as the sample for every manager. Routes: `master`, `profile`, `profile/<section>/<field>`, `documents`. The manager continues round 1 with brief section 5 items 3 and 4 (competitors and market, health) and the rest of the list. |

| 1 (manager) | competitors and market, coverage matrix, market signals, health, connectors, conflicts, questions, decisions, files in deeper, flow proof and `rank()` | 2026-09-28 | Manager session, brief section 5 items 3 and 4 plus the rest of the list. Table below. |

## Round 1 (manager, 28 Sep 2026): 10 features, one commit each

| # | Feature | Status | What a founder can do |
|---|---|---|---|
| 1.1 | Competitors and market: the Ad Library pages against the brand (`GET competitors`, `market.py`): verdict table per page with format mix, hook-form mix, run lengths, offers and signals; page detail panel with mix against the competitor median; stacked mix charts; gaps to brief as actions (rules BRN-R05 format gap, BRN-R06 hook-form gap, BRN-R07 snapshot stale); re-pull strip with the Apify estimate against the per-run and weekly caps, by page id only, logged as a BRN-C11 decision, never run from the screen | done | See which formats and hook forms competitors run that we do not, open any page in the Ad Library, brief the gap, queue a re-pull with its cost known |
| 1.2 | Coverage matrix (`GET coverage`): angles by page, our ad count per angle against every competitor page that runs it; red cells are angles we never lead with and open a drafted concept brief (proof from approved or site-backed claims and the ladder rungs, format to start with, win and stop rule) with a CREA-C06 decision row; lines for own ground unused, only us, contested; rule BRN-R08 angle gap (high at 3 or more pages) carries the draft | done | See in one grid which angles competitors run that we never do, and brief the gap with proof the brain can back |
| 1.3 | What buyers say elsewhere (`GET signals`): recommended-instead per competitor with the doubt behind it (angle from that page's hooks), our ladder proof status, where the answer goes (from the rung's uses) and an "Answer it" panel with the action; category frames against our positioning frame; the mission-read cross check against the ads; competitor sets with tracked chips; proposed pages with a page-id input that writes an approved founder record and joins the page list and the re-pull estimate (`POST competitors/page-id`); rules BRN-R09 recommended instead (high at 3 threads), BRN-R10 frame not carried | done | See who buyers pick instead and why, what proof we lack, where to put the answer and who writes it; add a competitor page without touching a config file |
| 1.4 | Health (`GET health`, `health.py`): every section by tier with counts, freshness against the contract shelf life and one verdict with an action (connect a source, ask the founder, re-crawl, fresh) carrying capability, owner and steps; sections-and-actions verdict table plus the heatmap; a section panel with the action card; a cell panel listing the records with Approve as is and Forbid (`POST approve/<id>` writes a founder record with the old tier in history); rule BRN-R11 weak section | done | See at a glance which sections are stale, empty or mostly inferred, do the one thing that fixes each, and settle inferred records one click at a time |
| 1.5 | Connectors (in `GET health`): one row per source category with connected via, options, what it fills, rooms it unblocks, last pull; verdict Connect one first for the categories that unblock most rooms; a connect panel with the 4 steps (person picks and pastes a read-only key, agent pulls in mock then live, proposes records, person accepts) as a BRN-C02 action; all 87 sources with pulls, failed, health and last pull from the brain's source log; never pulled reads unavailable | done | See which one source per category to connect next and why, and what it will fill |
| 1.6 | Which source wins (`GET conflicts`, `POST conflicts/<id>`): open conflicts as a two-column comparison with the default winner named (founder, connector, site, document, ad library, and so on), who reads the field, Keep this and Use this instead per value, or a typed value with a reason; the decision writes an approved founder record (section file and the founder raw lane, so a re-merge keeps it), marks the conflict resolved and logs a decisions record; settled list; rule BRN-R12 open conflict (high when gated). Every founder write on this screen (profile edit, answer, approve, page id) now lands in the founder raw lane too | done | Settle a disagreement between the site and a document in one click, with the reason kept, and know it reaches every screen |
| 1.7 | What the system needs from you (`GET questions`, `POST questions/bank/<qid>`): the brain's open questions and the bank questions no connected source answers, in one list ranked by weight times rooms unblocked; each with the pull-first hint (connect which source, or answer in a line), the field it fills, the screens it unblocks as links, and an inline answer that writes an approved founder record; answered list kept | done | Answer the 5 questions that unblock the most screens, or see which connector answers them for you |
| 1.8 | Decisions log timeline; approved master-list items show their decision and move to in progress | todo | |
| 1.9 | Files in, deeper (`ingest.py`, `POST documents`, `POST documents/extract`): a text or markdown file is read by rules (headings set the section, key: value lines, bullets, tried-and-failed sentences to learnings, never-say sentences to claims as forbidden, decided sentences to decisions) into proposed records with the file as source, the date and the line as evidence; nothing reaches the brain until accepted in the review queue; the files table shows waiting, accepted, sections and what each file changed; binary files and urls are kept as they are; no model call | done | Drop call notes or a brand book and see exactly which records it would add, then accept them one by one |
| 1.10 | `rank(brand, window)` in `api.py` (`ranking.py`): real titles, steps, artefacts, sizes, stop rules and check dates for BRN-R01 to R12, drafts on the angle briefs, owners by what ships (briefs draft and you approve, refreshes run, conflicts and claims are yours), reputation overrides as documented in `audit.py`; picked up by `app/rank.py` for the rank route and the master list. Flow proof (`GET flows`): per profile section, which screens read it (code scan), which read the T0 card, approved count and last founder edit; last read is unavailable until reads are logged | done | The master list now reads as work: "Brief the durability angle: 3 competitor pages run it, we run 0" with the brief attached; an edit's reach is visible |

### Round 1 status for Kevin (28 Sep 2026)

1. What you can do now: approve the top 10 across 28 screens, edit the profile so every screen reads your words, drop a file and see the records it proposes, settle a conflict in one click, answer the 5 questions that unblock the most screens, and see which angles, formats and hook forms competitors run that we never do, each with a drafted brief.
2. What changed: 10 features, 12 audit rules (BRN-R01 to R12), 14 new api routes, `market.py`, `health.py`, `ingest.py`, `ranking.py`; every founder write lands in the section file and the founder raw lane so a re-merge keeps it; 59 tests green on the screen, `test_app_rank` green.
3. What the brain screen puts on the master list today: brief the durability angle (3 competitor pages run it, we run 0, the brain names it as who we are), brief proof and authority, answer the Darn Tough comparison where buyers make it, fill policies and claims, settle the objection ladders (100 percent inferred).
4. Honest gaps: last read per section is unavailable until the store logs reads; a page id typed here joins the estimate, not yet the real pull config; the competitor angle cells are presence from 30 ads per page, not shares; no private connector is live, so the connectors table reads Connect one for 13 categories.
5. Not built yet from the room spec: claims tier bar, site diff between crawls, marketplace parity, contract renewals, permission matrix, legal disclosure gate. Round 2 starts with these plus the web pass picks (word scanner on drafts, voice sheet with liked and disliked examples, approved snippets, battlecards, ask the brain).
6. Screenshot: `round1.png` (top of the page at 1280 wide). Click-through: run the server and open `/screens/05-brand-brain/`.

Contract asks (for the lead):
- A read log in `app/brain/store.py` (stamp `section`, `reader`, `at` when a screen reads a section) so "last read" in the flow proof stops reading unavailable.
- `app/connectors/apify.py` (or the onboarding runner) to read `competitors.page_id_<slug>` founder records as extra Ad Library pages, so a page id typed on this screen joins the real pull as well as the estimate.
- `app/rank.py` `_title` falls back to the capability name; screens without an override read as capability names in the master list. Not mine to change; noted for the lead.

Web pass for round 2 ideas: `WEB-PASS.md` in this folder (25 features from the best brand-ops tools, 5 that none of them do).

## Round 2 (manager, 28 Sep 2026): 10 features, one commit each

Sources: the room spec (claims tier bar, site diff, marketplace parity, contract renewals, permission matrix, legal gate, export) and `WEB-PASS.md` (word scanner on drafts, voice sheet, approved snippets, battlecards, ask the brain, audit trail).

| # | Feature | Status | What a founder can do |
|---|---|---|---|
| 2.1 | Claims desk and draft scanner (`claims.py`, `GET claims`, `POST claims`, `POST scan`): every claim by tier, kind, source, age and the ladder rungs and surfaces that use it, with Approve, Forbid and Allow again; add a claim or forbid a phrase; tier bar; a scanner that checks any pasted draft against the brain (forbidden phrases block, numbers the brain contradicts block, unproven absolutes, unapproved claims and a reading grade above 10 warn), every hit naming the record and the fix; rule BRN-R13 claim untiered over 7 days | done | Decide what we can say in one click, and check any ad, email or page before it ships |
| 2.2 | Site diff between crawls: products, prices, offers, policies and claims changed since the last snapshot, each change ending in an action | todo | |
| 2.3 | Marketplace parity: Amazon price per pair against the site, MAP as a founder record, seller check | todo | |
| 2.4 | Contract renewals: vendors from the stack and operations with renewal dates, alert windows by vendor type | todo | |
| 2.5 | Legal disclosure gate: US checks across the brain and on a pasted page or email | todo | |
| 2.6 | Voice sheet: liked and disliked examples, do and do not lists, a copy-ready sheet for agents | todo | |
| 2.7 | Approved snippets: fixed lines agents paste word for word, with a stale check | todo | |
| 2.8 | Battlecards per competitor from the coverage matrix and the ladders | todo | |
| 2.9 | Ask the brain: keyword search with tier and source links, unanswered becomes an open question | todo | |
| 2.10 | Permission matrix stub and brain export | todo | |

## Round 1 candidates (ranked 28 Sep 2026 by the lead session)

Ranked by revenue impact, usefulness to a founder deciding alone, and buildable on the simulated data. Kevin picked the 5 screens; the top 5 here are recommended for round 1. One feature per commit, this table updated in the same commit.

| # | Feature | Capability | Why buildable now | Impact |
|---|---|---|---|---|
| 1.1 * | Freshness by confidence heatmap, one cell per section | BRN-C12 | freshness.json and confidence per record exist | high |
| 1.2 * | Claims tier bar with approve and forbid buttons that write founder records | BRN-C03 | claims records and the founder-answer route exist; the QA gate reads tiers | high |
| 1.3 * | Conflict table with the site-wins default and a founder-decides button | BRN-C05 | review/conflicts.json and founder resolution already work in merge | high |
| 1.4 * | Decisions log timeline, most recent first, with reason and date | BRN-C08 | decisions section plus data/decisions.json | medium |
| 1.5 * | Site diff: a second crawl compared to the first for products, prices, policies and claims | BRN-C01 | the site extractor exists; diff two runs | high |
| 1.6 | Connector health from the onboarding log and sources, unavailable never zero | BRN-C02 | onboard.log.jsonl and sources.json | medium |
| 1.7 | Marketplace parity strip: brand price against Amazon listing price and MAP per SKU | PROD-C46 | 34 Amazon listings in the brain; MAP is a founder record | medium |
| 1.8 | Founder question round: 5 questions with pull-first hints and inline answers | BRN-C07 | keeper.ask exists; the answer route exists | medium |
| 1.9 | Competitor snapshot age with a re-pull button that shows the Apify cost first | BRN-C11 | Ad Library by page id and the connector estimate | low |
| 1.10 | Permission matrix: sections by role, restricted by default | LOOP-C29 | needs tenancy from stage 6; stub only | low |

\* recommended for round 1
