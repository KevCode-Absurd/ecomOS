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

## Round 3 (manager, 28 Sep 2026): 10 features, one commit each

| # | Feature | Status | What a founder can do |
|---|---|---|---|
| 3.1 | What changed this week (`changes.py`, `GET changes`): every write through this screen (edit, answer, approve, forbid, file, proposal accepted or ignored, conflict, contract, permission, snippet, example, page id) and every site snapshot and site change lands as a `changes` record with the value before and after; the timeline for the week; version steps (brain hash before and after each write) in `review/versions.json` | done | Read one list after a week away and know what moved and who moved it |
| 3.2 | Where is it used (`GET dependents`): the fact-to-asset trace from records only: other records carrying the same number or code next to the same words, ladder rungs citing it as proof, questions it answered, snippets built on it, and the brand's own ads that carry the code; a site change logs its dependents; trace buttons on the profile | done | See that the first order code sits in 21 of 23 active ads before changing it |
| 3.3 | Which numbers are yours (`assumptions.py`, `GET assumptions`, `POST assumptions/<field>`): the 12 assumptions the simulation and the diagnosis run on, with status (yours, sourced, modelled, derived), unit, as of, the reasoning, the sources and the rooms that read them; confirm as is or correct writes an approved founder record on the source id; rule BRN-R21 modelled assumption read by rooms | done | Replace every benchmark that stood in for your number, one click each |
| 3.4 | What AI shopping agents should say about us (`facts.py`, `GET facts`, `POST facts/<key>`, `GET facts/export`): 12 question and answer pairs built from the records (returns, shipping options, free shipping, guarantee, giving, first order, pack sizes, materials, gift cards, B Corp, sizing, where we ship), approve a wording as an approved content record, stale when a number moves, export as FAQPage JSON-LD and plain text; an LOOP-C38 decision to probe what AI assistants say | done | Give the answer engines and shopping agents one approved set of facts, and know when one goes stale |
| 3.5 | Channel rule sets in the scanner (`POST scan` with `channel`): Amazon listing (no promotional wording, no links, guarantee terms, caps), Meta ad (no personal attributes, before and after, medical words, creator label), Google ad (no exclamation marks, caps, click here, superlatives), email (unsubscribe present, no fake replies, spam words), SMS (opt-out and brand name present); generic platform vocabulary, applied on top of the brain scan | done | Check a draft against the platform it goes to, not only against the brain |
| 3.6 | What an agent reads (`GET summaries`, `GET package?capability=`): the brand card's token count, one T1 summary per section with tokens, and the exact package a capability gets (T0, T1, T2 parts, tokens against its budget, public-facing exclusions) with copy; if an agent gets something wrong, this is what it saw | done | See exactly what any agent is told before it writes, and where the budget goes |
| 3.7 | Learned from your edits (`learn.py`, `GET learn`, `POST learn/apply`): every founder edit that replaced a value keeps the value before; the words cut in 2 or more edits (or once when hype) are proposed for words we avoid, the words added in 2 or more edits for words we use, each with the before and after as evidence; apply appends to the voice sheet and the scanner enforces it from then on | done | Teach the voice sheet by editing, without writing rules |
| 3.8 | The week in one page (`report.py`, `GET report?days=7`): changes by kind, decisions, questions answered and the top open, conflicts settled, site changes, files in, competitor snapshot age and gaps, one health line, the brain screen's top 5 moves; plain text to copy and a print view | done | Read the week in a minute and hand it to anyone without the screen |
| 3.9 | Proposed updates in a minute (`GET review`, `POST review/bulk`): proposals grouped by the file or agent they came from, each next to the record that wins the field today (new field, replaces, same value), with the evidence quote; Accept all that add something, Ignore the same-value ones, Ignore all, or one by one; accepts and ignores land in the changes log | done | Clear 30 proposals in a minute and never accept a duplicate |
| 3.10 | The founder round (`GET digest`): the top 5 questions with pull-first hints and the rooms they unblock, the proposed updates waiting, one health line, the top 3 moves to approve, in one message to copy; Slack and email delivery read unavailable until a connector exists | done | Get the weekly ask as one message that takes a minute to answer |

### Round 3 status for Kevin (28 Sep 2026)

1. What you can do now: read one list of everything that changed this week with the value before; see that the first order code sits in 21 of 23 active ads before touching it; replace every benchmark that stood in for your number, one click each; give shopping agents and answer engines one approved set of store facts and export it; check a draft against the platform it goes to (Amazon, Meta, Google, email, SMS); see exactly what any agent is told before it writes; let the voice sheet learn from the words you cut and add; read the week in one page or print it; clear 30 proposed updates in a minute with the record each would replace beside it; get the founder round as one message.
2. What changed: 10 features, 1 new rule (BRN-R21, now 21 rules), 21 new api routes, modules `changes.py`, `assumptions.py`, `facts.py`, `learn.py`, `report.py`; every write now logs a change and a version step; 84 screen tests green, `test_app_rank` green; the screen's api is 1,400 lines and screen.js 1,350, still one file each.
3. What the brain screen puts on the master list now: the 3 angle briefs, the Darn Tough answer, the modelled gross margin and return share to confirm, the 11 vendor contracts, the permission map.
4. Honest gaps: the trace reads records only until Meta and Klaviyo connect; the report and the digest copy but do not send; the review queue matches a proposal to the record it replaces by field name, so an oddly named line reads "new field"; the learned words need 2 edits before they show; the T2 records in a package are the overlay's choice, not this screen's.
5. Round 4 candidates: the onboarding intake that pre-fills itself for a second brand (proves plug and play), claim and angle test history once the experiments registry lands in the data layer, the visual check on generated creative against the brand's colours and logo rules, per-channel rule sets the founder edits, and the audit trail once the store logs reads. Web pass ideas 3, 12, 14, 17 and 24 remain.
6. Screenshot: `round3.png` (the founder round). Every feature is a pushed commit; the screen now has 21 rules and 63 routes.

### Round 2 status for Kevin (28 Sep 2026)

1. What you can do now: decide what we can say and check any draft before it ships (forbidden phrases and stale numbers block); see the day a price, policy or claim moved on the site and what to update; set your MAP and seller names and get the notice drafted for every Amazon listing that breaks them; put vendor contracts on file and get the renegotiation brief before the notice deadline; gate an email, ad or page for US disclosures; teach agents your voice with examples and lock the 6 lines that must never drift; hand CX and copy a battlecard per competitor; ask the brain a plain question and get a sourced answer; set who sees which section and export the whole brain.
2. What changed: 10 features, 8 new rules (BRN-R13 to R20, now 20 rules), 24 new api routes, modules `claims.py`, `sitediff.py`, `parity.py`, `contracts.py`, `legal.py`, `voice.py`, `battlecards.py`, `ask.py`; the first site snapshot is seeded and committed; 84 screen tests green, `test_app_rank` green.
3. What the brain screen puts on the master list now: the 3 angle briefs, the Darn Tough answer, the vendor contracts to put on file (11 known vendors, none on file), the permission map to set; MAP and seller checks wait on 2 founder inputs and say so.
4. Honest gaps: the site diff has one snapshot until the next crawl; the parity check is per pair against the single-pair floor with a 35 percent band because the site's pack prices are not in the ladder; the legal gate is rules, not counsel; permissions are a map until hosting and auth enforce them; the voice sheet is empty until you fill 4 fields and paste 3 liked examples.
5. Round 3 candidates: the founder-edit to voice-sheet learning loop, claim and angle test history from the experiments registry, the fact-to-asset trace across live ads and emails when Meta and Klaviyo connect, a weekly brain report, and the onboarding intake that pre-fills itself. Web pass ideas 3, 6, 12, 14, 17 and 24 remain.
6. Screenshot: `round2.png` (the draft scanner). Every feature is one commit on the branch.

### Round 1 status for Kevin (28 Sep 2026)

1. What you can do now: approve the top 10 across 28 screens, edit the profile so every screen reads your words, drop a file and see the records it proposes, settle a conflict in one click, answer the 5 questions that unblock the most screens, and see which angles, formats and hook forms competitors run that we never do, each with a drafted brief.
2. What changed: 10 features, 12 audit rules (BRN-R01 to R12), 14 new api routes, `market.py`, `health.py`, `ingest.py`, `ranking.py`; every founder write lands in the section file and the founder raw lane so a re-merge keeps it; 59 tests green on the screen, `test_app_rank` green.
3. What the brain screen puts on the master list today: brief the durability angle (3 competitor pages run it, we run 0, the brain names it as who we are), brief proof and authority, answer the Darn Tough comparison where buyers make it, fill policies and claims, settle the objection ladders (100 percent inferred).
4. Honest gaps: last read per section is unavailable until the store logs reads; a page id typed here joins the estimate, not yet the real pull config; the competitor angle cells are presence from 30 ads per page, not shares; no private connector is live, so the connectors table reads Connect one for 13 categories.
5. Not built yet from the room spec: claims tier bar, site diff between crawls, marketplace parity, contract renewals, permission matrix, legal disclosure gate. Round 2 starts with these plus the web pass picks (word scanner on drafts, voice sheet with liked and disliked examples, approved snippets, battlecards, ask the brain).
6. Screenshot: `round1.png` (top of the page at 1280 wide). Click-through: run the server and open `/screens/05-brand-brain/`.

Contract asks (for the lead): all three answered on 28 Sep 2026 (commit 029ff27). The flow proof now reads the store's read log (`profile`, `records` and `package` stamp it when the caller names itself with `?reader=`); founder page ids join the Ad Library pull; default rank titles use the rule name.

Web pass for round 2 ideas: `WEB-PASS.md` in this folder (25 features from the best brand-ops tools, 5 that none of them do).

## Round 2 (manager, 28 Sep 2026): 10 features, one commit each

Sources: the room spec (claims tier bar, site diff, marketplace parity, contract renewals, permission matrix, legal gate, export) and `WEB-PASS.md` (word scanner on drafts, voice sheet, approved snippets, battlecards, ask the brain, audit trail).

| # | Feature | Status | What a founder can do |
|---|---|---|---|
| 2.1 | Claims desk and draft scanner (`claims.py`, `GET claims`, `POST claims`, `POST scan`): every claim by tier, kind, source, age and the ladder rungs and surfaces that use it, with Approve, Forbid and Allow again; add a claim or forbid a phrase; tier bar; a scanner that checks any pasted draft against the brain (forbidden phrases block, numbers the brain contradicts block, unproven absolutes, unapproved claims and a reading grade above 10 warn), every hit naming the record and the fix; rule BRN-R13 claim untiered over 7 days | done | Decide what we can say in one click, and check any ad, email or page before it ships |
| 2.2 | Did the site change (`sitediff.py`, `GET site/diff`, `POST site/snapshot`, `POST site/reviewed`): the crawl on file is snapshotted (first one seeded), the two newest snapshots are diffed record by record (added, removed, changed, before and now), severity by section, each change carrying its action (carry a new offer or policy into copy, ads, email and CX; re-tier a changed claim; check listings after a product change) and a Mark reviewed button; one snapshot reads unavailable with the reason; rule BRN-R14 open site change; re-crawl as a BRN-C01 decision | done | Know the day a price, a policy or a claim moved on the site, and what to update because of it |
| 2.3 | Is anyone undercutting us on Amazon (`parity.py`, `GET parity`, `POST parity/map`, `POST parity/sellers`): every marketplace listing with pack count from the title, price per pair, the site's single-pair floor per line, gap, seller, stars and reviews; MAP and your seller names typed once as approved founder records turn on the checks; flags end in a MAP notice or an unauthorised seller report; rules BRN-R15 below MAP and BRN-R16 unrecognised seller fire only with their inputs, else one unavailable finding names what fills them | done | Set your MAP and seller names once, then see every listing that breaks them with the notice drafted |
| 2.4 | What renews before we notice (`contracts.py`, `GET contracts`, `POST contracts`): the register of vendor contracts as founder records in operations (vendor, type, renewal date, notice days, rate card, SLA), alert windows by vendor type (platform and 3PL 90 days, agency and payments 60, apps and SaaS 30), verdicts (renews in N days, passed, no date, no contract on file), the 12-month calendar; vendors the brain knows from the stack and partner mentions are listed until their contract is on file; rules BRN-R17 renewal approaching and BRN-R18 missing date or missing contract, with rank actions | done | Add each vendor's renewal date once and get the renegotiation brief before the notice deadline |
| 2.5 | Is it legal to ship (`legal.py`, `GET legal`, `POST legal/gate`): 11 US disclosure checks read from the brain (privacy policy with an effective date, state privacy notice, terms, returns posted, cookie consent, accessibility, creator ads labelled; CAN-SPAM, pricing and sales tax unavailable until their source connects; auto-renewal n/a without plans), each pass, fail, unavailable or n/a with evidence and a fix; a gate for a pasted email, ad, product page, policy or subscription terms that lists what is missing, with the claims scanner run on the same text; rule BRN-R19 disclosure missing blocks going live | done | Know the disclosures the site carries and gate any draft before it ships |
| 2.6 | How we write, the voice sheet (`voice.py`, `GET voice`, `POST voice/example`): the contract's 8 voice fields editable in place (they also appear in the profile), liked and disliked examples with a why, lines the crawl quoted from our own pages, a copy-ready sheet in plain text for any writing agent, ready when 4 fields and 3 liked examples exist; the scanner now warns on words from the avoid list | done | Teach every writing agent your voice with examples, and see the avoid list enforced on drafts |
| 2.7 | Approved snippets (`POST voice/snippet/<key>`): the 6 fixed lines (free shipping, standard shipping, returns, guarantee, giving, first order) built in code from the records they depend on, lockable to your exact wording; a locked line whose number the brain no longer holds reads stale, is not pasted, and ends in a re-approve action that also finds the live assets carrying the old line; copy all for an agent | done | Fix the exact wording of the lines that must never drift, and know the day a record makes one stale |
| 2.8 | How we win against each competitor (`battlecards.py`, `GET battlecards`): one card per tracked page rebuilt from the brain on every load: what they say, their price band, what they push, their angles, where they run and we do not, threads recommending them (counted, never quoted), the doubt they exploit and our proof on its rung, how we win from approved or site-backed claims, CX macro and copy first line, verdict (losing, proof gap, angle gap, covered), plain text to copy and a BRAND-C57 decision | done | Hand any competitor's card to CX and copy, and see which proof gap loses the comparison |
| 2.9 | Ask the brain (`ask.py`, `GET ask`, `POST ask/open`): a plain question answered from records ranked by keyword coverage, tier and date, each with its source link; "can we say" routes to the claims tiers (yes with the claim as written, never for a forbidden phrase, needs proof for a superlative, not as written with the closest claim, not on file); an unanswered question saves as an open question that shows under what the system needs; the box sits above the plan | done | Get a sourced answer in seconds, or leave the question where the system will chase it |
| 2.10 | Who sees what, and can we take it all with us (`GET permissions`, `POST permissions/<section>`, `GET export`): sections by role (founder, in-house, agency, specialist) as a heatmap, restricted by default (founder full, in-house read, outsiders none; private sections tighter) until a founder record sets a section; rule BRN-R20 permission gap; the whole brain exported as one JSON (records with sources and history, the documents manifest and file list, the router, conflicts) with an LOOP-C22 offboarding decision. Enforcement lands with hosting and auth; this is the map | done | Set the map once and know the brain leaves with you the day a relationship ends |

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
