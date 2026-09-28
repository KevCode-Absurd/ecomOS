# Answer engines: features

Status: todo | doing | done | parked. One feature per commit. The first round is the skeleton; after that, features come in rounds of 10, stack-ranked by revenue impact, usefulness and how easy they are to build on dummy data.

## Round 0: skeleton

| # | Feature | Status |
|---|---|---|
| 0.1 | Page shell in the shared UI kit: header, empty-state tiles, insight list, action buttons | done |
| 0.2 | `api.py` serving this screen's metrics from `app/data/` with unavailable states | done |
| 0.3 | 3 metric tiles, 2 insights, 1 chart from the sample brand | done |
| 0.4 | `audit.py`: 14 rules (AEO-R01 to R14) in the contract shape; readiness rules fire on Bombas | done |

## Jobs to be done (room spec) and the audit rules behind them

| Job | Question | Capability | Rules |
|---|---|---|---|
| Run a fixed prompt set, see how each engine describes and recommends us | what does each engine say about us today | ORG-C37 | AEO-R07, AEO-R09, AEO-R14 |
| Know whether an answer is a real gap and how bad | which of the 6 gap types are we in per engine | ORG-C37 | AEO-R09 (gap types need the prompt log) |
| Publish one facts page that closes every gap | what facts are missing that a buyer prompt needs | ORG-C35 | AEO-R11, AEO-R12 |
| Keep facts identical everywhere an engine reads | do price, returns, warranty, payment match on site, schema, feed, directories | ORG-C35 | AEO-R03 |
| Make a high-value page easy to lift an answer from | which pages are citable, which bury the answer | ORG-C34 | AEO-R02, AEO-R05, AEO-R10, AEO-R13 |
| Fix a wrong AI-stated fact at the source | what is an engine getting wrong, where did it learn it | ORG-C36 | AEO-R01 |
| Know if a correction landed | did the answer change after the fix, how long did it take | ORG-C36 | AEO-R04 |
| Check what a shopping agent tells a buyer | would an agent get price, stock and delivery right | PROD-C47 | AEO-R06 |
| Short weekly read on us and named competitors | did an engine change how it describes a competitor | BRN-C11 | AEO-R08 |

Rules R01 to R11 are the room spec's insights in order. R12 to R14 are round 0 readiness reads from the brain and sessions.

## Candidates from the room spec (pick 10 per round)

### Questions this screen should answer

- what does ChatGPT, Gemini, Perplexity and Google AI say about us today  (ORG-C37)
- which of the 6 gap types are we in for each named engine  (ORG-C37)
- what facts are missing that a buyer prompt keeps needing  (ORG-C35)
- does the price, return window, warranty and payment method answer match on the site, schema, feed and directories  (ORG-C35)
- which pages are citable and which still bury the answer  (ORG-C34)
- what is an engine getting wrong about us right now, and where did it likely learn it  (ORG-C36)
- did the engine's answer change after we fixed it, and how long did that take  (ORG-C36)
- would an AI shopping agent get our price, stock and delivery estimate right  (PROD-C47)
- did an engine change how it describes a named competitor, or did they make a new claim  (BRN-C11)

### Metrics specified

- `ai_mention_rate`: Share of the frozen prompt set where the brand is mentioned at all, per engine. prompts_mentioning_brand / prompts_in_set, grouped by engine
- `ai_recommend_rate`: Share of prompts where the brand is named as a recommended option, not just mentioned. prompts_recommending_brand / prompts_in_set, grouped by engine
- `ai_share_of_voice`: Brand mentions as a share of all named-brand mentions (brand plus named competitors) in the same prompt set. brand_mentions / (brand_mentions + competitor_mentions)
- `ai_sentiment_score`: Share of brand mentions classified positive under a fixed rubric. positive_mentions / total_mentions
- `fact_gap_count`: Gaps found in the last prompt audit, by category (price, materials, returns, shipping, payment method, warranty). count(gaps) from the last audit, grouped by category
- `fact_gap_closed_rate`: Share of the last audit's gaps that now have a published fix. gaps_with_published_fix / gaps_found
- `fact_consistency_score`: Share of core facts that read identically across site, schema, feed and tracked directories. facts_matching_everywhere / facts_checked
- `citation_source_share`: Of the sources an engine cites when it answers about the brand, the share that are brand-owned. brand_owned_citations / total_citations
- `wrong_fact_count_open`: Confirmed wrong AI-stated facts not yet corrected at any level. count(corrections) where status = open
- `correction_landed_rate`: Share of corrections confirmed fixed on re-check after the set cadence. corrections_confirmed_on_recheck / corrections_rechecked
- `correction_lag_days`: Typical days from a wrong fact confirmed to the site-level fix published. median(site_fix_date - confirmed_date)
- `citable_page_count`: Pages rewritten to the answer-first, atomic-fact format, out of the priority list. pages_rewritten / pages_on_priority_list
- `agentic_listing_accuracy`: Share of checked fields (price, stock, variant, delivery estimate) a shopping-agent-style query returns correctly. fields_matching_live_feed / fields_checked
- `competitor_ai_narrative_change_count`: Detected changes this week in how an engine describes a named competitor. count(narrative_changes) from the weekly competitor prompt slice
- `engine_coverage`: Which engines are currently in the monitored set. list of engines with a successful run in the last 35 days

### Insights specified (rules in code)

- engine invents a fact: an engine's answer states a specific number or claim that does not match the facts registry → "{engine} told a buyer {claim}, which is not on our facts page" (action ORG-C36)
- recommend gap versus a competitor: an engine mentions the brand but recommends a named competitor for the same prompt → "{engine} named {competitor} instead of us for '{prompt}'" (action ORG-C34)
- fact drift across surfaces: the same fact reads with a different value on two tracked surfaces → "{fact} says {value_a} on the site and {value_b} on the feed" (action ORG-C35)
- correction did not land: a correction shipped N days ago and the re-check still returns the old fact → "{n} days after we fixed it, {engine} still says the old {fact}" (action ORG-C36)
- no brand-owned citation: an engine's answers about the brand cite zero brand-owned sources across the last audit → "{engine} never cites our own site when it answers about us" (action ORG-C34)
- shopping agent gets it wrong: an agentic listing spot-check returns a price or stock value that does not match the live feed → "{n} products show the wrong {field} to a shopping agent" (action PROD-C47)
- sentiment slide: ai_sentiment_score for an engine falls versus the prior month → "{engine}'s positive mentions fell {pct} points this month" (action ORG-C37)
- competitor narrative shift: a named competitor's described strengths changed between this week's and last week's prompt slice → "{engine} now says {competitor} is {new_claim}, it did not say that last week" (action BRN-C11)
- stale prompt set: the prompt set has not run for an engine in more than 35 days → "the AI-visibility check has not run on {engine} in {d} days" (action ORG-C37)
- citable rewrite backlog stalling: a page on the priority rewrite list has sat unrewritten for more than 4 weeks → "{n} priority pages are still not rewritten for citation after {weeks} weeks" (action ORG-C34)
- known but not recommended: ai_mention_rate is high (over 60%) while ai_recommend_rate is low (under 20%) for the same engine → "{engine} knows us in {pct}% of prompts but recommends us in only {rec_pct}%" (action ORG-C35)

### Visuals specified

- share of voice by engine (stacked bar chart): brand vs named competitor mentions, one bar per engine
- fact consistency matrix (grid, facts by surface): each core fact against each tracked surface, matched or mismatched
- correction lifecycle timeline (step timeline): confirmed wrong fact, site fix, publisher fix, re-check pass or fail
- agentic listing spot-check table (table): field, expected value, what the agent returned, match or mismatch
- weekly change ticker (diff list): what changed this week for the brand and named competitors
- sentiment trend by engine (line chart): monthly sentiment score per engine

### Not in the usual tools

- ties the facts page to a fixed re-check cadence that confirms a correction actually landed in the engine's answer
- checks what a shopping agent would tell a buyer about price, stock and delivery against the brand's own live feed
- scores fact consistency across site, schema, feed and directories side by side, before an engine ever asks
- sequences page rewrites by the gaps a real, frozen prompt audit found for this brand
- bundles a named competitor's changing AI narrative with their social and PR activity in one short weekly brief

### Data this screen needs

- `ai_prompt_runs`: engine, prompt, run_date, response_text, mentions_brand, recommends_brand, sentiment, cited_sources (frozen prompt set run against each engine (API or manual capture))
- `competitor_prompt_runs`: engine, competitor, prompt, run_date, response_text, narrative_tags (same prompt-run script, competitor slice, weekly subset)
- `facts_registry`: fact_id, category, value, surface, last_checked (ORG-C35 output, one row per fact per surface)
- `corrections_log`: fact_id, wrong_claim, confirmed_date, site_fix_date, publisher_fix_date, recheck_dates, recheck_result, status (ORG-C36 workflow output)
- `product_feed_snapshot`: sku, price, stock, variant, delivery_estimate, last_updated (merchant feed export)
- `agentic_listing_checks`: sku, field, expected_value, agent_returned_value, match, checked_at (agentic spot-check script against product_feed_snapshot)
- `page_rewrite_backlog`: page, priority, gap_category, status, flagged_at, rewritten_at (ORG-C34 priority list)
- `directories_tracked`: directory, region, last_checked, facts_match (manual or scraped check of Yelp, the Better Business Bureau, Google Business Profile and named marketplaces (JustDial and IndiaMart added for an India listing, market option, reads null for a US-only brand))

## Rounds

| Round | Features picked | Date | Notes |
|---|---|---|---|
| 0 | Shell, api, 3 tiles, 2 insights, 1 chart, audit | 2026-09-28 | S3.20 |

## Round 0 status

1. Built: index.html, screen.js, api.py (overview, findings), audit.py (14 rules), fixtures/prompts.json (14 sample buyer prompts), round0.png.
2. Tiles: buyer prompts the brain can answer (8 of 14), core facts on a facts page (0 of 6), AI referral sessions (unavailable: no AI engine source in sessions).
3. Insights: 6 sample prompts need a fact the brain lacks (ORG-C35); agent shopping endpoint published but never checked (PROD-C47). Chart: one-star mentions by buyer doubt, answered or not.
4. Firing on Bombas: R03 ankle sock price on verified Amazon listings 33 percent below the catalog, R09 prompt set never run, R12 four missing facts, R13 refund and shipping facts only on /policies/ pages.
5. Unavailable with connector named: R01, R02, R04 to R08, R10, R11 (prompt log, corrections, feed, agentic checks), R14 (AI referrers). No finding has money yet; R14 carries the formula for when GA4 has AI sources.
6. Next: propose `ai_referral_sessions` for the metric contract, a prompt-run log table in data-sources, and a facts registry so R03 covers schema, feed and directories.

