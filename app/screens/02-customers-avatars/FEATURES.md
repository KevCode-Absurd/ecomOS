# Brand and customers: features

Status: todo | doing | done | parked. One feature per commit. The first round is the skeleton; after that, features come in rounds of 10, stack-ranked by revenue impact, usefulness and how easy they are to build on dummy data.

## Round 0: skeleton (done 28 Sep 2026, S3.7, Bombas)

| # | Feature | Status |
|---|---|---|
| 0.1 | Page shell in the shared UI kit: simulated badge, tiles, insights, chart, avatars, objection map, language bank, voice sheet, decision row, audit table | done |
| 0.2 | `api.py`: `overview`, `audit`, `POST voice/examples`. Brand facts through `app/brain/store.py`; cohorts through `app/data/tables.py` | done |
| 0.3 | 3 tiles (grounded avatars, objection coverage, repeat within 3 months), 2 insight rules, 1 chart (repeat within 3 months by first-order month) | done |
| 0.4 | Avatar cards: share estimate, intensity, job, up to 3 quotes with source links, top doubt with proof or no proof, badge grounded / one source / inferred | done |
| 0.5 | Objection map: objection, avatars (from ladder rungs), proof or open question, quotes, coverage in ads and on pages | done; ads and pages show unavailable (no angle field in `ad_rows`, no live page scan) |
| 0.6 | Language bank by theme: phrases with counts, mentions by source, one quote per phrase with link | done |
| 0.7 | Voice sheet: do, do not, tone by context from voice records; liked and disliked examples box writes founder records (`<brand>.voice.<kind>_example_<sha8>`) through `Brain.put`; marking the other way retires the old record | done |
| 0.8 | `audit.py`: CUST-R01 ungrounded avatar, CUST-R02 uncovered top objection, CUST-R03 objection coverage in ads (unavailable until ads name an angle) | done |

Round 0 notes:
- Repeat within 3 months is computed from `cohorts.json` `active_by_month` (months 1 to 3 summed, over cohort size). A buyer active in 2 of those months counts twice, so it is an upper bound. `repeat_rate_90d` in `metrics.py` needs order rows, which read as unreadable for Bombas, so the chart does not use it. A contract session could add a cohort-level repeat metric from the aggregates.
- The audit entity for an avatar is type `brand` with the avatar key as id: `audit.md` has no `avatar` type yet. Propose one in a contract session.
- Ad coverage needs an angle per ad. The simulated `ad_rows` has placeholder text and no angle; the generator or an ad naming rule would fill it.
- "Ungrounded" means no quotes, or quotes from fewer than 2 independent sources. On Bombas 7 of 11 avatars rest on 1 source.

## Round 1: the execution surface (from 28 Sep 2026)

Judged by `app/contracts/depth.md`. Each feature ends in an action with an owner, steps and an artefact.

| # | Feature | Status |
|---|---|---|
| 1.1 | Round 0 anti-patterns out: plan board first with ranked actions from `rank`, orientation beside it (new customers 28d, returning share, repeat in 3 months, avatars with proof, rungs without proof, oldest avatar check), what is wrong grouped by rule with evidence and a link to its action, action cards with steps, desk, audit and rule list at the bottom. Tiles, insights and the repeat bar chart removed. `rank(brand, window)` in `api.py` gives every action a real title | done |
| 1.2 | Avatar cards: job, moment, pain, top doubt with one-star and five-star counts, proof on file, where their voice shows (channel chips). Each ends in the next build from a rule in `builds.py` (offer when the top doubt has no proof and the rung lists offer, page block when it has no proof, research note when there are no quotes, else an ad brief), with owner, steps, a drafted artefact filled from the brain, Copy brief and the decision row. Reddit lines are never shown as testimonials | done |
| 1.3 | Where each avatar gets an answer: a coverage matrix of avatars by channel (ads and email, product page, Amazon listing, support replies, offer). Each cell is doubts answered with proof against doubts that channel must answer, from the ladder rungs and their `uses`. Red cells carry "Brief it", which opens a side panel with a drafted brief, owner, steps and the decision row. Beside it, Meta formats us against the category median from the Ad Library pulls in the brain, with a test brief for a format the category runs in 15 percent or more of live ads and we run at under half that | done |
| 1.4 | Doubts rung by rung, per avatar: pills filter the ladders by avatar with the count of rungs without proof. Each rung shows one-star against five-star as a split bar, the proof on file and a verdict from a rule: no proof (copy, or an offer when the rung lists offer), not landing (proof on file yet one-star is 2x five-star or more with 10 or more: move the proof to the first screen), lead with it (five-star above one-star: an ad brief), keep. Every move opens a drafted brief with owner and steps. The old objection table sits under a fold | done |
| 1.5 | Their words for each doubt: phrases from the language bank linked to each rung (through `derived_from`), split into how they say the doubt (complaint or 1 to 2 star) and how they say the win (praise, result or 4 to 5 star), up to 6 each, generic lines dropped, Reddit lines marked language only and unticked. Avatar pills. "Use in brief" builds a copy brief from the ticked lines with the proof, owner and steps. All phrases by theme sit under a fold | done |
| 1.6 | Cohort grid with the break named and the retention action | todo |
| 1.7 | New against returning mix and what drives it | todo |
| 1.8 | Avatars served and not served: positioning map | todo |
| 1.9 | Where reviews say the avatar is misread | todo |
| 1.10 | `rank` with real steps and artefacts for every rule | todo |

## Room jobs (room "Brand and customers", agent BRAND)

| Job | Question | Capabilities |
|---|---|---|
| know who really buys and why, with evidence | who is my customer and what job did they hire us for | BRAND-C01, BRAND-C02, BRAND-C03, BRAND-C04, BRAND-C08, BRAND-C09, BRAND-C10, BRAND-C11 |
| reuse customers' own words in copy and creative instead of guessing | what exact words do our customers use for this | BRAND-C14, CREA-C03 |
| split one avatar into separate records when the job changes | is this really one customer or three | BRAND-C12 |
| pair every named objection with the real thing that removed it | what actually gets someone past this objection | BRAND-C13 |
| confirm what research found at wider scale | does this hold up outside the sample we already read | BRAND-C05, BRAND-C06 |
| find an untapped avatar when the category feels saturated | is there a customer nobody else is claiming | BRAND-C16 |
| keep the voice sheet current and check assets against it before they ship | does this sound like us, and is every claim in it safe | BRAND-C32, LOOP-C12, BRN-C03 |
| walk the live site, ads and email against the guidelines on a cadence | where has the brand drifted since last quarter | BRAND-C37 |
| track the brand's health line separate from any one campaign | is the brand getting stronger or weaker | BRAND-C48 |
| keep the founder-facing brand brain current | what does the brand stand for right now, in one place | BRAND-C15, LOOP-C11 |
| check what we say we are against what customers actually say | do customers describe us the way we describe ourselves | BRAND-C59 |
| run automated checks on the brand's own journey and messaging before spending | would a real shopper get stuck, and does this message land | BRAND-C67, BRAND-C66 |
| watch for trademark, domain and handle risk | is anyone about to take something that is ours | MONEY-C48 |
| keep every page and channel leading with the same one idea | what is the one message this page or email should lead with | BRAND-C33 |

The job to be done for each avatar is brand data: it lives in `app/brain/<brand>/avatars.json` (`value.job`) and shows on the avatar cards, not here.

## Candidates from the room spec (pick 10 per round)

### Questions this screen should answer

- who is my customer and what job did they hire us for  (BRAND-C01, BRAND-C02, BRAND-C03, BRAND-C04, BRAND-C08, BRAND-C09, BRAND-C10, BRAND-C11)
- what exact words do our customers use for this  (BRAND-C14, CREA-C03)
- is this really one customer or three  (BRAND-C12)
- what actually gets someone past this objection  (BRAND-C13)
- does this hold up outside the sample we already read  (BRAND-C05, BRAND-C06)
- is there a customer nobody else is claiming  (BRAND-C16)
- does this sound like us, and is every claim in it safe  (BRAND-C32, LOOP-C12, BRN-C03)
- where has the brand drifted since last quarter  (BRAND-C37)
- is the brand getting stronger or weaker  (BRAND-C48)
- what does the brand stand for right now, in one place  (BRAND-C15, LOOP-C11)
- do customers describe us the way we describe ourselves  (BRAND-C59)
- would a real shopper get stuck, and does this message land  (BRAND-C67, BRAND-C66)
- is anyone about to take something that is ours  (MONEY-C48)
- what is the one message this page or email should lead with  (BRAND-C33)

### Metrics specified

- `avatar_coverage`: Share of last 90 days' revenue tied to a gated, complete avatar record. revenue from orders matched to a primary or segmented avatar / total revenue
- `avatar_evidence_count`: How many independent quotes back each avatar's job statement. count of distinct sourced quotes per avatar record
- `avatar_freshness_days`: Days since this avatar was last re-checked against real orders and reviews. today minus last audit date
- `language_bank_size`: Exact customer phrases on file per avatar. count of tracked phrases per avatar, deduplicated
- `language_bank_reuse_rate`: Share of live ad, page and email lines that trace back to a banked customer phrase. lines matched to a bank phrase / total scored lines
- `voice_compliance_score`: Share of live assets that pass the voice sheet check. assets passing / assets scanned, across site, ads and email
- `voice_drift_flags`: New drift issues found this audit that were not flagged last time. count of new rule violations this run
- `claims_risk_count`: Claims waiting on evidence or legal review before they can ship. count of claims in the registry without a passed evidence tier
- `branded_search_index`: How often people search for the brand by name, indexed to a base month. branded query volume / volume in the base month, times 100
- `mention_volume`: Public mentions of the brand across tracked sources. count of mentions per period
- `mention_sentiment_net`: Share of mentions reading positive minus share reading negative. (positive mentions minus negative mentions) / total mentions
- `repeat_purchase_rate`: Share of customers in the window who bought again. customers with 2 or more orders / customers with 1 or more orders
- `review_rating_trend`: Average star rating over time. mean rating per period, all verified reviews
- `objection_coverage`: Share of named objections that have a proven remover attached. objections with a paired remover / total named objections
- `mystery_shopper_pass_rate`: Share of journey checkpoints that passed on the last run. checkpoints passed / checkpoints tested
- `trademark_watch_alerts`: Open alerts on the brand's own marks, domains or handles. count of open alerts (renewal due, lookalike registration)
- `messaging_hierarchy_adoption`: Share of live page and channel types that lead with the current top message. page or channel instances matching the current hierarchy top line / total scanned
- `perception_gap_score`: How closely customer language matches the positioning statement. share of top review and mention terms that also appear in the positioning statement and voice sheet

### Insights specified (rules in code)

- avatar gone stale: avatar_freshness_days over 90 for the primary avatar → "The primary avatar has not been re-checked in {n} days. Confirm it still holds before the next brief." (action BRAND-C15)
- new objection not yet mapped: a phrase cluster appears in 5 or more reviews or tickets in a period and matches no entry in the objection map → "{n} customers raised '{phrase}' this month. It has no listed remover yet." (action BRAND-C13)
- voice drift on a live asset: an asset scanned this audit fails a voice rule it passed last audit → "{asset} now breaks the voice sheet on {rule}. It passed last time." (action BRAND-C37)
- unverified claim about to ship: a claim tagged for a live page or ad has no passed evidence tier → "'{claim}' is scheduled to go live with no evidence on file." (action BRN-C03)
- branded search falling at flat spend: branded_search_index drops more than 15 percent over 8 weeks while paid spend is flat or up → "Branded search fell {pct} percent over 8 weeks while spend held steady." (action BRAND-C48)
- sentiment turned amid a mention spike: mention_volume rises more than 2x the trailing average and mention_sentiment_net turns negative in the same week → "Mentions jumped {x}x this week and sentiment went negative. This may need a holding statement." (action BRAND-C54)
- repeat rate falling for the primary avatar: repeat_purchase_rate for the primary avatar's segment drops more than 5 points quarter over quarter → "Repeat purchase among {avatar} fell {pts} points this quarter." (action BRAND-C48)
- banked phrase never used: a phrase logged 10 or more times in the language bank appears in zero live assets → "Customers say '{phrase}' often, but it is in none of our live copy." (action BRAND-C14)
- trademark or handle risk: a renewal falls due within 60 days, or a new registration matches the brand name closely → "{item} needs attention: {reason}." (action MONEY-C48)
- mystery shopper found a broken step: a journey checkpoint fails on the latest run that passed on the prior run → "The {step} step of the buying journey failed on the latest check." (action BRAND-C67)
- AI persona pretest flagged a miss: a persona pretest scores a message or name below the pass threshold set for that test → "'{concept}' scored low with the {persona} persona before any real spend." (action BRAND-C66)
- perception gap widening: perception_gap_score drops more than 10 points quarter over quarter → "What customers say about us now matches our positioning statement {pct} percent less than last quarter." (action BRAND-C59)

### Visuals specified

- avatar evidence board (card grid, one card per avatar): job statement, 5W profile, quote count, freshness, provisional flag
- language bank frequency chart (horizontal bar list): top phrases by mention count, tagged used or unused in live copy
- voice compliance heatmap (heatmap, channel by period): pass or fail per audit for site, ads and email over time
- brand health trend lines (4 small line charts): branded search, mention volume, net sentiment and repeat rate over time
- objection to remover table (paired table): each named objection next to its proven remover and coverage flag
- mystery shopper journey funnel (step funnel with pass or fail marks): browse, cart, checkout, confirmation, support reply, each marked pass or fail on the latest run

### Not in the usual tools

- the avatar record gates every field against a completeness checklist and marks itself provisional until a pattern shows across independent sources
- the language bank tracks reuse rate of real customer phrases in live copy, not just a tone score on a draft
- the consistency audit walks the live site, live ads and live email together on one cadence with one rule set
- brand health here joins branded search, mentions, sentiment and repeat purchase from the brand's own store data into one line
- the perception gap check compares the positioning statement word for word against the brand's own reviews and support tickets
- the mystery shopper audit runs the brand's own live journey end to end, including a real support query, on demand and repeatably
- objection pairing here is the real thing that removed the objection for a real customer, tied to a support macro

### Data this screen needs

- `avatar_records`: brand, avatar_id, tier, job_statement, 5w_profile, quote_ids, status, primary_flag, last_audit_date (BRAND-C09 through BRAND-C11, BRAND-C15)
- `language_bank`: brand, avatar_id, phrase, source_type, source_id, first_seen, repeat_count, used_in_live_copy (BRAND-C14)
- `reviews_raw`: brand, review_id, star_rating, text, date, product_id (store review export, BRAND-C01)
- `support_tickets_raw`: brand, ticket_id, channel (email, sms, call; whatsapp where used, markets: IN, EU, LATAM), reason_code, return_or_failed_delivery_flag (return_to_sender_rate for US, rto_flag for India orders markets: IN), text, date (helpdesk export, BRAND-C02)
- `onsite_search_and_behavior`: brand, query, result_count, converted_flag, session_id, date (site search log, BRAND-C04)
- `objection_map`: brand, objection, remover, source_id, coverage_flag (BRAND-C13)
- `voice_sheet`: brand, version, liked_examples, disliked_examples, rules, approved_date (BRAND-C32)
- `claims_registry`: brand, claim_id, claim_text, evidence_tier, status, target_asset (BRAND-C22, BRAND-C38)
- `brand_consistency_audits`: brand, audit_id, channel, asset_id, rule, pass_fail, date (BRAND-C37)
- `brand_health`: brand, period, branded_search_index, mention_volume, mention_sentiment_net, repeat_purchase_rate, review_rating_avg (search console or SEO tool, mention listening feed, store order history, BRAND-C48)
- `mystery_shopper_runs`: brand, run_id, step, pass_fail, note, date (BRAND-C67)
- `ai_persona_pretests`: brand, test_id, concept, persona, score, date (BRAND-C66)
- `trademark_domain_watch`: brand, item, type (mark, domain, handle), renewal_date, alert_reason (BRAND-C69)
- `messaging_hierarchy`: brand, page_or_channel_type, top_message, supporting_points, approved_date (BRAND-C33)

## Rounds

| Round | Features picked | Date | Notes |
|---|---|---|---|
| 0 | skeleton, 0.1 to 0.8 | 28 Sep 2026 | Bombas brain plus simulated cohorts; screenshot `round0.png` |
| 1 | 1.1 to 1.10, no picks (depth brief) | 28 Sep 2026 | in progress |
