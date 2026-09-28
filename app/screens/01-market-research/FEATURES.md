# Products and research: features

Status: todo | doing | done | parked. One feature per commit. The first round is the skeleton; after that, features come in rounds of 10, stack-ranked by revenue impact, usefulness and how easy they are to build on dummy data.

## Round 0: skeleton (done 28 Sep 2026, Bombas simulated data)

| # | Feature | Status |
|---|---|---|
| 0.1 | Page shell in the shared UI kit: header, simulated banner, tiles, insight list, decision row | done |
| 0.2 | `api.py` (`overview`, `findings`) from `app/metrics.py` (`units`, `product_net_sales`, added for this screen) and the brand brain, unavailable states | done |
| 0.3 | 3 tiles: units last 3 whole months vs a year earlier, lines losing share, lowest rated line | done |
| 0.4 | Demand by line: units, growth vs last year, points vs the store, net sales, stars, reviews, 1 and 2 star share | done |
| 0.5 | Price band table: per-pair list price per line against the competitor median band from `brain.competitors` (socks only) | done |
| 0.6 | Review mining tiles per line: what works, what fails (`products.reviews_*`), ladder rungs built from the same reviews | done |
| 0.7 | Candidate pipeline, seeded empty, with the margin gate rule and the floor from `finance_inputs.target_contribution_margin` | done |
| 0.8 | 2 insights as rules: hero line with no next SKU (PROD-C06), sock price position against the band (PROD-C04) | done |
| 0.9 | 1 chart: units by line, 12 whole months, top 5 lines stacked plus the rest | done |
| 0.10 | Decision row: screen next-SKU ideas (PROD-C01, agent does) | done |
| 0.11 | `audit.py`: PROD-R01 declining line (units down, or 1 point or more behind store growth), PROD-R02 review issue (1 and 2 star share 10 percent or more and 1.5x the brand median), money at stake on both | done |

Notes from round 0:
- On the Bombas simulated set every line grows about 28 percent a year, so no line falls in units. PROD-R01 also reads share: Gift Box grew 1.4 points slower than the store in all 3 months and fires as losing share.
- List prices are the simulated catalog; review totals and competitor prices are public brain records. The page says which is which.
- A line is the SKU title without its pack size. Review records map to lines through `audit.REVIEW_LINE`; lines without a record show "no record".
- Screenshot: `round0.png`.

## Room jobs (agent PROD, room "Products and research")

| Job | Question | Capabilities |
|---|---|---|
| kill a bad product idea before spending research time on it | does this idea clear a fast demand and fit check | PROD-C01 |
| check if a viral video-commerce product has real demand | is this one clip or a real pattern | PROD-C02 |
| see which competitors run real sustained ad spend on a candidate | who is actually making money on this, not just posting it | PROD-C03 |
| keep candidate research inside a fixed time budget | has this candidate used up its research hours | PROD-C04 |
| read trend direction against competitive saturation for a category | is this category growing with room left, or growing and already full | PROD-C05 |
| plan the next SKU for a proven hero product and its differentiation angle | what do we launch next and why is it different | PROD-C06 |
| tag a candidate's demand pattern and cash timing | is this evergreen, seasonal or a one-time novelty, and when does cash move | PROD-C07 |
| check a candidate against the margin and compliance gate | does this candidate actually make money after real costs, and is it legal to sell | PROD-C08 |
| compare gate-estimated margin against a live SKU's actual margin | is this SKU making what we modelled it would | PROD-C08 |
| mine reviews on the candidate's category for price ceiling and unmet complaints | what would buyers actually pay, and what do they hate about what exists | PROD-C04, PROD-C31 |
| run the remaining go-live gates on a candidate | is this candidate ready to fund | PROD-C10 |
| see the ranked shortlist and go or no-go memo | which candidates does the founder decide on this week | PROD-C11 |
| hand a validated angle and avatar to the creative team | what does creative build on, and is it grounded in real field research | PROD-C12 |
| track tech pack and spec versions for every SKU in the pipeline | which candidates have a real, versioned spec ready for sourcing | PROD-C13 |

No JTBD table exists for this room yet (jtbd-writer is a BRAND skill, not a room table).

## Candidates from the room spec (pick 10 per round)

### Questions this screen should answer

- does this idea clear a fast demand and fit check  (PROD-C01)
- is this one clip or a real pattern  (PROD-C02)
- who is actually making money on this, not just posting it  (PROD-C03)
- has this candidate used up its research hours  (PROD-C04)
- is this category growing with room left, or growing and already full  (PROD-C05)
- what do we launch next and why is it different  (PROD-C06)
- is this evergreen, seasonal or a one-time novelty, and when does cash move  (PROD-C07)
- does this candidate actually make money after real costs, and is it legal to sell  (PROD-C08)
- is this SKU making what we modelled it would  (PROD-C08)
- what would buyers actually pay, and what do they hate about what exists  (PROD-C04, PROD-C31)
- is this candidate ready to fund  (PROD-C10)
- which candidates does the founder decide on this week  (PROD-C11)
- what does creative build on, and is it grounded in real field research  (PROD-C12)
- which candidates have a real, versioned spec ready for sourcing  (PROD-C13)

### Metrics specified

- `demand_screen_result`: Whether a candidate passed the first fast check. pass/fail flag from the demand, competition and store-fit rule set applied to the candidate
- `video_commerce_demand_signal`: How strong the social/video demand signal is, and from how many sources. count of independent platforms and creators showing sustained views or sell-through above the category median, not a single clip
- `ad_library_spend_signal`: How many advertisers keep spending on this product idea, and for how long. count of distinct advertisers with an ad live for more than 90 days in public ad libraries for the candidate's category
- `research_time_used`: Hours spent researching this candidate against its budget. sum of logged research hours for the candidate ÷ the time box set for its research stage
- `trend_direction_score`: Whether the category is growing, flat or shrinking over several years. slope of a multi-year search or sales trend index, normalised to a -1 to 1 score
- `competitive_saturation_count`: How many sellers already compete in this category. count of distinct active sellers or listings found for the category across the channels checked
- `demand_pattern_tag`: Evergreen, seasonal or trending label for the candidate. rule-based tag from the trend series shape (flat, spiking, or one-off) plus review and search seasonality
- `review_price_signal`: The price buyers say in reviews they would actually pay. median of price mentions extracted from 1 to 5 star reviews on competing products in the category
- `review_complaint_rate`: How often the same unmet complaint shows up in competitor reviews. count of reviews mentioning the top recurring complaint ÷ total reviews mined for that competitor product
- `contribution_margin_pct_modelled`: The margin the gate model expects after price, cost, shipping and duty. (planned price − COGS − shipping − duty − payment fee) ÷ planned price
- `contribution_margin_pct_actual`: The margin a launched SKU is really making, from real sales. (actual revenue − actual COGS − allocated shipping − allocated ad spend − returns cost) ÷ actual revenue, from sales and cost records
- `compliance_gate_status`: Whether the candidate's regulatory checks are cleared. pass/fail flag from the compliance checklist attached to the margin gate (labelling, category-specific certification)
- `differentiation_angle_confidence`: How solid the stated point of difference is. rule score from whether the angle field is filled, is backed by a named source (review gap, teardown or field research), and is not a copy of a competitor's own claim
- `shortlist_score`: A candidate's rank on the fixed scorecard. weighted sum of the scorecard's fixed criteria (demand, margin, differentiation, compliance, cash timing), weights set once per brand
- `go_live_gate_pass_count`: How many of the 5 go-live gates a candidate has cleared. count of passed gates (provable claim, owned difference, brand threshold, contribution margin, ad-cost ceiling) ÷ 5
- `tech_pack_status`: Whether a SKU has a current, versioned spec ready for sourcing. flag from the tech pack table: current version has tolerances, BOM and packaging cost line filled
- `candidate_pipeline_age_days`: How long a candidate has sat in the pipeline without a decision. today minus the candidate's screen-in date
- `shortlist_review_date_status`: Whether a shortlisted candidate's scheduled review has come due. today compared against the review date set on the go/no-go memo
- `sku_revenue_share`: Share of category revenue this SKU brings in. SKU revenue ÷ total category revenue, trailing window
- `sku_return_rate`: Share of units sold that come back. returned units ÷ shipped units for the SKU, trailing window

### Insights specified (rules in code)

- demand screen failed: candidate fails 2 or more of the demand, competition or store-fit checks in the screen → "{candidate} failed {n} of the fast checks. Killing it now saves the research hours." (action PROD-C01)
- single-source video spike: video_commerce_demand_signal shows exactly 1 platform or creator source over the window → "{candidate}'s demand comes from one clip on one platform. Treat it as unverified until a second source confirms it." (action PROD-C02)
- real sustained ad spend found: ad_library_spend_signal counts 3 or more advertisers with an ad live past 90 days → "{n} advertisers have kept an ad live for {days}+ days on this idea. That is a real spend signal, not a trend." (action PROD-C03)
- trend up, category full: trend_direction_score is positive and competitive_saturation_count is above the brand's set ceiling → "{category} is growing, but {n} sellers already compete in it. Room left is smaller than the trend line suggests." (action PROD-C05)
- margin gate failed: contribution_margin_pct_modelled is below the brand's set minimum threshold → "{candidate}'s modelled margin is {pct}%, below the {threshold}% floor. It cannot move to sourcing spend without a price, cost or channel change." (action PROD-C08)
- actual margin trailing the model: contribution_margin_pct_actual is more than 5 points below contribution_margin_pct_modelled for the same SKU → "{sku} is making {actual}% margin against a {modelled}% model. Recheck landed cost and ad spend allocation." (action PROD-C08)
- review price gap: review_price_signal is more than 15% below the candidate's planned price → "Reviewers say they would pay around {price}, {pct}% below the planned price. Recheck positioning before funding." (action PROD-C04)
- unresolved category complaint: review_complaint_rate for the top complaint exceeds 15% of mined reviews → "{pct}% of reviews on the category leader mention the same complaint: {complaint}. That is the gap to build the angle on." (action PROD-C04)
- seasonal candidate with no cash plan: demand_pattern_tag is seasonal or gifting and no cash timing note is attached → "{candidate} is tagged seasonal, but no cash plan is attached for its spike window. It cannot reach the shortlist without one." (action PROD-C07)
- differentiation angle missing: differentiation_angle_confidence is unavailable (angle field empty) while the candidate is past the screening stage → "{candidate} has no stated point of difference. It should not reach a funding gate without one." (action PROD-C06)
- candidate stalled past its time box: candidate_pipeline_age_days exceeds the time box set for its current stage → "{candidate} has sat at this stage for {days} days, past its {budget}-day box. Decide or kill it." (action PROD-C04)
- shortlist review due: shortlist_review_date_status shows today at or past the set review date → "{candidate}'s review date has arrived. Bring it back to the founder for a fresh decision." (action PROD-C11)
- hero SKU with no line extension: a SKU's sku_revenue_share is in the top decile of its category and no next-SKU candidate is open in the pipeline → "{sku} drives {pct}% of category revenue with no next SKU in the pipeline. Consider planning an extension." (action PROD-C06)
- compliance gate incomplete: compliance_gate_status is unavailable while go_live_gate_pass_count shows other gates passed → "{candidate} has cleared {n} of 5 gates but the compliance check has not run. It is not fundable yet." (action PROD-C10)

### Visuals specified

- candidate funnel (funnel chart): count of candidates at each stage: screened, researched, gated, shortlisted, go
- trend vs saturation map (scatter plot): trend_direction_score on one axis, competitive_saturation_count on the other, one point per category
- SKU margin waterfall (waterfall chart): price stepping down through COGS, shipping, duty, ad spend and returns to net contribution margin
- review complaint bars (horizontal bar chart): top recurring complaints from mined reviews, ranked by share of reviews mentioning them
- ad spend timeline (step chart): count of advertisers with a live ad on this product idea over the trailing 6 months
- shortlist scorecard grid (ranked table with score bars): each shortlisted candidate's score on every scorecard criterion, ranked

### Not in the usual tools

- combines video-commerce demand, ad library spend and DTC review mining in one screen before any paid research tool is used
- computes true contribution margin per SKU including allocated ad spend and returns, and checks it against the original gate model
- enforces a visible, fixed research time box per candidate so research cannot sprawl
- ties a mined review price signal directly into the margin gate's pricing input
- reads trend direction and competitor count together as one go/no-go signal

### Data this screen needs

- `candidate_pipeline`: candidate_id, name, category, stage, screen_result, time_box_days, hours_logged, angle_text, angle_source, screen_in_date (manual entry plus agent screen output)
- `trend_series`: category, period, index_value, source (web research pull (public trend tools))
- `competitor_scan`: category, seller_count, scanned_at, source (web research pull)
- `ad_library_captures`: candidate_id, advertiser, platform, first_seen, last_seen, days_active (ad library and spy-tool search)
- `video_commerce_signals`: candidate_id, platform, creator_or_shop, views_or_units, captured_at (video-commerce platform pull)
- `review_mining`: source_product, channel, rating, review_text, price_mention, mined_at (review mining script (reads public listing reviews))
- `margin_gate_calc`: candidate_id, planned_price, cogs, shipping_cost, duty, payment_fee_pct, contribution_margin_pct, compliance_checklist_status, run_at (margin gate script (code, not model judgment))
- `sku_sales_cost`: sku, channel, period, revenue, cogs_actual, ad_spend_allocated, returns_units, returns_cost (brand sales data joined to sourcing cost records)
- `shortlist_scorecard`: candidate_id, criterion, weight, score, rank, review_date, decision (scorecard script plus founder decision log)
- `tech_pack_versions`: sku, version, tolerances, bom, packaging_cost, status, updated_at (manual entry plus sourcing agent output)

## Round 1: the execution surface (from 28 Sep 2026, depth contract)

The screen is rebuilt to `app/contracts/depth.md`: the plan first, then what is wrong, the actions with their implementation, the desk, the audit. Every element ends in an action with an owner, steps and an artefact. `rank(brand, window)` in `api.py` maps every audit finding to a real action.

| # | Feature | Status |
|---|---|---|
| 1.1 | Plan board first from `rank`, orientation numbers beside it (units, lines losing share, product lines in the brain, public revenue band, open findings, stake, brain freshness); what is wrong grouped by rule with evidence numbers; action cards with owner, steps, artefact, win and stop rules; the desk restyled as verdict tables with a gap line and an action under each block; the audit with findings and rules at the bottom; exports. Round 0 tiles, insight cards and the units chart removed. New rule PROD-R03 (hero line with no next SKU in the pipeline). `rank` v1 with real titles and steps for R01 to R03. | done |
| 1.2 | Industry and sub-industry trends: `fixtures/market_trends.json` from a public web pass (12 markets, 8 preferences, 18 launches, a url and a date on every number), trend strips of the public markets beside our 12-month category mix with verdicts against market growth and the public share records in the brain, a lanes table (sold, advertised, or neither), new rules PROD-R04 (category behind its market, money = growth gap x net sales) and PROD-R05 (growing lane sold and not named in any active ad, or the gift window inside 90 days), ad-brief recipes in `rank` | done |
| 1.3 | Emerging sub-categories and new products: 10 lanes (compression, merino, run and hike, guarantee proof, style drops, gifting, underwear, footwear, apparel, creator proof) read from the competitor pages in the brain (who pushes it, active ads, longest run) and the launches in the web pass (brand, what, date, price, url), against whether we sell and advertise it; verdict follow, watch or ignore by rule (2 pages and a 30-day runner; under 14 days and no launch); rule PROD-R06 (competitor-pushed lane we do not advertise) with a Brief it action, merged with the PROD-R05 market finding on the same lane | done |
| 1.4 | What people are talking about: one row per theme (durability, price and worth, fit, comfort, delivery, marketplace trust, mission) with complaint against praise quotes from the objection ladders by source, Reddit mentions and upvotes, the Instagram hashtag pull (`social_pull.py` through the Apify connector under the brand caps, whitelist of fields, no usernames; mock run on file because the live run could not be authorised from the build session), the top doubt, and whether the site and the active ads answer it; verdict unanswered, answered, strength, watch; rule PROD-R07 (complaint-led theme with no ad answer) with an ad brief plus page section recipe | done |
| 1.5 | Shifting preferences: 8 public survey preferences from the web pass (sustainability, natural fibres, durability, giving, made in USA, resale, compression, gifting) against our own claims, our active ads, the competitors' pitches and the category conversation; verdict leading, prove it, gap, watch; rule PROD-R08 (a preference competitors claim and no record of ours carries) with a claim, counter or leave recipe that writes an approved positioning record; prove-it rows link to the ad briefs from 1.2 to 1.4 | done |
| 1.6 | Positioning map: `Charts.positioningMap` of price per pair (competitor medians from the brain, ours from the catalog or the public entry price) against the share of proof-led hook types, points sized by active ads, quadrants named (value with proof, premium with proof, value on feel, premium on feel), members and empty quadrants listed, pages without a price band listed apart; the Reddit frames and recommended-instead counts beside it; rule PROD-R09 (category framed on proof, brand never named, competitor recommended instead, our proof share below the competitor median) with a proof-next-to-the-price recipe | done |
| 1.7 | Personas served and not served: `UI.coverageMatrix` of the brain's avatars by the lines the brand sells (our evidence quotes and records against competitor pages whose pitch carries the avatar's words), a click on any cell opens the avatar and its action, a verdict table beside it (share, intensity, theme and its complaint share, competitors pitching to them, in our ads); rules PROD-R10 (avatar with no line evidence while a competitor pitches to them) and PROD-R11 (big segment on a complaint-led theme no ad answers, money = share x 28-day net revenue x complaint share x repeat rate, capped at high) with screen and win-back recipes | done |
| 1.8 | Search terms: brand, category, competitor and problem term groups built from the brain (identity, lines, materials, competitor set, Reddit recommended-instead, ladder rung doubts, the brand's own research searches), Search Console and Google search-term demand per group over 28 days when the tables exist and unavailable otherwise, the pages in the site map that answer each group, the questions people ask the category (seo_facts); rules PROD-R12 (Search Console not connected, a connect action) and PROD-R13 (a group with impressions and no page, a page action) | done |
| 1.9 | Where the brand is falling behind: every positioning and avatar gap the audit found (PROD-R06 to R11), ranked by money at stake where a formula exists, then reach (share of buyers, competitor pages, Reddit upvotes, complaint quotes), then severity; owner, capability and the action on each row; orientation numbers (gaps, stake, share of 28-day net revenue, the quadrant we sit in) and the proof we hold and never say in an ad; the same rows feed `rank` | done |
| 1.10 | `rank(brand, window)` in `api.py` for all 13 rules: real titles, steps with who does each, artefact kinds (research_note, page_section, ad_brief, offer, landing_page, connector_setup), size, win and stop rules, check dates; rubric overrides declared in the audit docstring (R07 reputation 4, R09 reputation 5, R11 satisfaction 4) applied in code with the total recomputed; one action per lane when a market and a competitor finding overlap; tests that every finding maps to a valid action, every rule has a recipe, the order is deterministic and the rubric totals add up. Screenshots `round1.png` and `round1b.png` (the page is 19,140 px tall; each file under 1 MB). | done |

## Round 2: the rest of the room spec (from 28 Sep 2026)

The candidate side of the desk: the pipeline with its gates, boxes and scorecard, and the research-tool jobs (trend against saturation, sustained ad spend, review price and complaint mining) rebuilt as rules on our own data. Ideas taken from the bank by id: PRD-052 (competitor count ladder), PRD-079 (dollar floor and multiple), PRD-023 (run length as a live test), PRD-044 and PRD-045 (12-month and multi-year trend checks), PRD-005 (felt problem).

| # | Feature | Status |
|---|---|---|
| 2.1 | Candidate pipeline that works: `POST candidates` and `POST candidates/<id>` write `fixtures/pipeline.json` (screen in, advance, log hours, set checks, kill; every change in the row's log), seeded with 4 candidates from the round 1 findings; funnel by stage reached; a screen-in form and the actions on every card; rules PROD-R14 (candidate past its time box) and PROD-R15 (2 of 3 fast checks failed) with decide-or-kill recipes | done |
| 2.2 | Margin gate per candidate: contribution margin modelled = (price - landed cost - donated item - fulfilment - payment fee) / price, every term from the candidate, the finance inputs (landed cost entered or the median of single-unit SKUs in the category times the pack, label, packaging, pick and pack over units an order, payment fees) or the brain (the donated item share); a waterfall per candidate with pills, the gate table against the brand floor and the bank's PRD-079 reference; rule PROD-R16 (modelled margin below the floor) with a price, cost or channel recipe; PROD-R17 actual margin by SKU unavailable until the store connects | done |
| 2.3 | Demand pattern tag: evergreen, seasonal or trending per category and per candidate from our own 12-month unit series (top 2 months share against an even year), the web pass (market growth, launches) and the name (gift); the cash timing each implies; a cash plan attached to a candidate from the card; rule PROD-R18 (seasonal candidate with no cash plan) with a drafted cash plan that says what is unavailable (lead time) | done |
| 2.4 | Trend against saturation map: one point per lane, trend score from the web pass growth and launches against sellers (competitor pages pushing it plus launches by others), the bank's PRD-052 ladder (green 0 to 1, amber 2 to 4, red 5 or more) as the grid, quadrants named (growing with room left, growing but full, flat and open, flat and crowded); rule PROD-R19 (growing but full, product lanes) with a find-the-room recipe | done |
| 2.5 | Sustained ad spend per lane: competitor pages by the longest run of their active ads (under 14, 14 to 29, 30 to 89, 90 days or more) as a stacked bar per lane, the advertisers at 90 days or more, verdict funded test, live test or noise (bank ideas PRD-023 and PRD-024), and the open candidates on each lane; rule PROD-R20 (funded product lane with no candidate) with a screen recipe, merged with the lane brief when both fire | done |
| 2.6 | Review price signal: per-pair price mentions mined from review quotes (Amazon, the brand site, Trustpilot, retailers; Reddit left out; packs left out) as a median with the range, by source and star, the quotes in their words, against the competitor band, our own pair and each candidate's planned price per unit; rule PROD-R21 (a sock candidate planned more than 15 percent above the review median) with a price-or-proof recipe | done |
| 2.7 | Complaint bars per listing: the brand's Amazon listings with complaint themes as a share of the reviews mined (stacked bars with the 15 percent rule line), praise share, the listing's public stars, ratings and price; rule PROD-R22 (one complaint over 15 percent of 20 or more mined reviews) with a build-the-angle recipe that proposes a brain record | done |
| 2.8 | Differentiation angle and the 5 go-live gates: angle confidence 0 to 3 (filled, names a source, not a competitor's claim by shared words against every competitor pitch in the brain), the gates per candidate as a heatmap (provable claim, owned difference, brand threshold, contribution margin, ad-cost ceiling against target CAC) with the reason on every cell, plus the compliance check; rules PROD-R23 (angle missing past screening) and PROD-R24 (2 or more gates passed, compliance not run) with write-the-angle and compliance-checklist recipes | done |
| 2.9 | Shortlist scorecard: demand, margin, differentiation, compliance and cash timing scored 0 to 5 in code from the checks, the spend signal, the margin gate, the angle, the compliance check and the demand pattern, weighted once per brand (learnings.shortlist_weights, else 30, 30, 20, 10, 10), ranked as a heatmap and a table with go, hold or no-go; the go or no-go memo drafted from the numbers with shortlist, go and kill from the panel; rule PROD-R25 (review date arrived) with the memo as the artefact draft | done |
| 2.10 | `rank` recipes for PROD-R14 to R25 (every rule has a recipe or a connect action), one card per candidate (the highest-scored finding hosts the others, every finding still mapped), tests for the merge and the recipes, `round2.png`, `round2b.png` and `round2c.png` (the page is 31,822 px tall; each under 1 MB), the round 2 founder note | done |

## Round 3: the rest of the room spec and the research-tool jobs (from 28 Sep 2026)

| # | Feature | Status |
|---|---|---|
| 3.1 | Readability: what is wrong shows 2 findings per rule with show-more and a severity filter (pills), the actions beyond the top 10 fold into a table with an Open button, and the desk opens with a jump strip to its blocks; the page drops from 31,822 to about 27,300 px with nothing hidden | done |
| 3.2 | Video-commerce demand signals per lane: the Instagram hashtag pull (mock, said so), Reddit mentions and upvotes on the lane's words, competitor creator-style ads and our own creator ads; platforms above a floor counted, verdict real pattern, single source or no signal, with the candidates resting on each lane; rule PROD-R26 (a candidate lane on exactly one platform) with a confirm-on-a-second-platform recipe (bank ideas PRD-018, PRD-022) | done |
| 3.3 | Tech pack and spec versions per candidate: tolerances, the bill of materials and the packaging cost line saved from the card as versioned packs (the new one supersedes the last), status ready to quote, partial, spec missing or not yet needed; rule PROD-R27 (candidate at gated or later with no current spec) with a write-the-spec recipe; one card per candidate keeps it merged in the plan | done |
| 3.4 | Research hours budget: hours logged per candidate against the hours allowed through its stage (per-stage budgets summed, a brand sets its own in learnings.research_hours_budget), as bars and a table with in budget, near the cap, over budget; rule PROD-R28 (hours past the budget) with a stop-the-clock recipe, merged into the candidate's card | done |
| 3.5 | Trend history check per lane: the web pass series split into history and forecast, the last-year rate against the multi-year rate, verdict steady, spike, falling, forecast only or no series (bank ideas PRD-044 and PRD-045); rule PROD-R29 (a candidate lane with no 3-year history, or a spike) with a run-the-multi-year-check recipe that writes the series back into the web pass | done |
| 3.6 | Audience surfaces (SparkToro-style): every subreddit in the Reddit pull, every review source in the ladders and every social surface the brand names, with reach on file, tone, the loudest theme and whether any brand record shows us there; configured surfaces with no pull read not pulled, never 0; rule PROD-R30 (reach over the floor, no presence) with a listening-post recipe for forums (one card across the subreddits), a claim-the-profile recipe for review sources and an open-the-account recipe for social | done |
| 3.7 | Marketplace seller read (Jungle Scout-style): the brain's Amazon presence record (brand store, A+ content, brand as seller, resellers seen, lines not found) and every listing with pairs parsed from the title, price per pair against the site per-pair price, stars, ratings and seller (not read, never assumed); rules PROD-R31 (brand not the seller of record, no brand store; Brand Registry and stance recipe, PROD-C29) and PROD-R32 (listing 25 percent or more off the site price on 20 or more ratings; price integrity check, PROD-C46), merged into one Amazon stance card | done |
| 3.8 | Competitor launch cadence (Particl-style): the web pass launches by brand (12 and 24 months, last launch, lanes, channels, median price) as bars and a table, our cadence against the competitor median, and per lane the competitor launches, the newest one, our last one and whether we sell it; rule PROD-R33 (a lane we sell with 2 or more competitor launches in 12 months or 2 brands in 24 and none of ours in 24; proof lanes never) with a next-SKU brief recipe merged into the lane card | done |
| 3.9 | Second brand test (Tallgrass Goods, the sample brand: kitchen goods, no brain, no web pass): the web pass and social pull fixtures now carry a brand field and another brand reads none of them (`web_pass`, `lanes_for`, `social_pull_for`), the lanes moved from a code constant into the web pass fixture, the rank route serves the sample brand through the server's data reader, the window never runs past the data's last full day, the empty funnel no longer draws NaN bars; every block on the sample renders its honest empty state and every action is a connect action; tests `SecondBrandTest` | done |
| 3.10 | Recipes for PROD-R26 to R33 (every rule has a recipe or a connect action; totals recomputed after every merge), tests for each feature (74 in the file), `round3.png`, `round3b.png`, `round3c.png` (the Bombas page, 35,117 px tall, each part under 1 MB) and `round3s.png` (the sample brand, every block in its empty state), the round 3 founder note | done |

## Round 4: decision memory, the pulls, and a brand with no brain (from 28 Sep 2026)

| # | Feature | Status |
|---|---|---|
| 4.1 | Decision memory: the founder's choices from the shared decisions log ride on the plan. A "not now" parks the action for 14 days (it leaves the plan, a "Decided" strip under the plan lists it with the note, the date it comes back and its card so it can be decided again); agent and person choices stay on their cards as "Saved"; an expired park returns on its own; route `parked` | done |
| 4.2 | Category mix from orders when a brand has no monthly product table (the sample brand): units and net sales by product type per month from order line items (discount shared by line value, cancelled orders out), labelled as such on the page; growth on last year reads unavailable until the whole prior year is on file; the demand pattern tags now fill for the sample brand | done |
| 4.3 | Return rate by line (room metric `sku_return_rate`): units from order line items and returns from the return leg of reversed orders over 12 whole months, per line against the store median with the top reasons; lines under 20 returns read too thin to judge; rule PROD-R34 line at 1.5 times the median with a returns-read recipe keyed to the top reason; unavailable with the reason when orders or returns are not connected (Bombas: orders are an 8.8 million row table, read through an aggregate) | done |
| 4.4 | Open questions for the founder: the brain's open_questions, each a doubt from the objection ladders with the complaint quotes behind it, tied to its theme, with who can answer, whether it was asked or answered and whether any record answers the theme yet; rule PROD-R35 (5 or more complaint quotes, never asked or unanswered 14 days) with an ask-the-founder recipe whose artefact is the answer as a brain record; the question rides on its theme's PROD-R07 card as an extra step | done |
| 4.5 | Pulls and their freshness: every pull the desk reads (Reddit, Amazon reviews, Ad Library by page id, listings, the seller of record, Instagram, the web pass) with its last capture from the brain's source refs, age against its window (Ad Library 7 days while a candidate is open), the blocks it feeds and the estimate for a run at the configured size from the connector's price table against the brand's caps; rule PROD-R36 pull due, never run, mock, or no actor set, with a person-approves-the-run recipe that names the command and the caps; nothing runs from the page | done |
| 4.6 | Amazon listing seller pull: `listing_pull.py` runs the listing actor (junglee~amazon-crawler per ASIN, or `amazon_reviews.listing_actor`) through the connector under the caps and writes `fixtures/amazon_listings.json` (seller of record, third party or not, price, stars, ratings; no reviewer fields); the marketplace read takes sellers only from a live run and says when a mock is on file; the pulls block reads its date and mode; live run not authorised from the build session, mock on file | done |
| 4.7 | Web pass runner: `web_pass.py --brand X --init` writes `fixtures/web_pass/<brand>.json` as a template (lanes, markets, preferences, launches, a url and a date per number) and `--check` lists what is missing and refuses a number without a source; the desk reads the brand's own file first, then the legacy fixture when its brand matches; the connect action for a brand with no web pass names the two commands; the checker found 3 gaps in the Bombas fixture | done |
| 4.8 | Candidate brief: `candidates/<id>/brief` assembles one page per candidate from every block (angle and its source, fast checks, lane signals, trend check, demand pattern and cash plan, price and margin waterfall, review price signal, the 5 gates and compliance, the scorecard, tech pack and hours, the open actions, the log); a Brief button on every pipeline row opens it with a copy button; the artefact that goes to creative and sourcing, read only | done |
| 4.9 | The first run and its MOQ (bank idea BRD-249): from gated on, each candidate's first production run on file (units wanted, format, its MOQ, cash out, the lower-MOQ alternative considered), the cash as a share of 28-day net revenue; rule PROD-R37 no first run on file, or a full-MOQ run at 25 percent of revenue or more (or revenue unknown, or MOQ over the units wanted) with no lower-MOQ option noted, money = the first run cash; recipes to size the run or cost a lower-MOQ format; entered from the block, written on the candidate, read by the brief; merged into the candidate card | done |
| 4.10 | Recipes for PROD-R34 to R37 (every rule has a recipe or a connect action), tests for each feature (88 in the file), `round4.png`, `round4b.png`, `round4c.png` (the Bombas page, 37,719 px tall, each part under 1 MB) and `round4s.png` (the sample brand with the mix, the demand pattern and the return rates now filled from orders), the round 4 founder note | done |

## Round 5: hand-offs, memory and the calendar (from 28 Sep 2026)

| # | Feature | Status |
|---|---|---|
| 5.1 | The hand-off (events contract): `fixtures/product_candidates.json` rewritten on every candidate write (stage and decision, planned price, landed cost estimate, pack units, first run, tech pack version, angle, review date; a gross margin from the estimates, labelled as such), served at `product_candidates`; a go writes a proposed test in the registry shape to `fixtures/proposed_tests.json` (hypothesis from the angle, metric contribution margin, read point the review date), served at `tests`; the pipeline block shows both | done |
| 5.2 | What each card covers: every finding behind a card (rule id, severity, sentence, stake) as a checklist in the card panel, and under each top card that merges 2 or more findings, so a merged card reads as a list that closes item by item | done |
| 5.3 | The research calendar (route `calendar`, above the desk): every dated thing in the next 45 days on one timeline and a table, overdue first: time-box ends, review dates, the check dates of the top 10 actions, parked actions coming back, pulls due, the gift window; each row opens its card | done |
| 5.4 | Creative hand-off per buyer or theme card: the angle brief for creative (the doubt, the avatar, the proof on file, review quotes never from Reddit, the words buyers use, the do-not list), copyable from the card panel | todo |
| 5.5 | The desk report: one markdown page with every block's gap line, the top 10, the connect list and the parked list, copy or download from Exports | todo |
| 5.6 | Ledger week-to-date in the pulls block: this ISO week's Apify spend and reservations for the brand from the spend ledger, read only, against the weekly cap | todo |
| 5.7 | Our launches from the brain calendar join the web pass launches in the cadence read, so our last launch per lane is not only what the press covered | todo |
| 5.8 | Idea bank pass: PRD-113 (a stage advanced while a check or gate failed and the log names no reason) and PRD-047 (a trending candidate at gated or later with no evergreen companion named) as rules | todo |
| 5.9 | Since you last looked: a snapshot of the findings taken on demand, and a strip of what is new, gone or changed since it | todo |
| 5.10 | Recipes, tests, round5.png, founder note | todo |

## Round 4 note for the founder (28 Sep 2026)

1. The plan now remembers you. A "not now" parks an action for 14 days and it leaves the plan; a strip under the plan lists what is parked with your note and the date it comes back, and its card so you can decide again; agent and person choices stay on their cards. The founder's 5 open questions from the brain (each a doubt with the complaint quotes behind it and no proof that covers it) sit on their theme cards as the step only you can take.
2. The desk now knows what it is standing on: every pull it reads (Reddit, Amazon reviews, Ad Library by page id, listings, the seller of record, Instagram, the web pass) with its last capture, its window, the blocks it feeds and what a run costs under the caps. Today two are not live: the Instagram pull (mock) and the seller of record (mock, sellers withheld); the cards name the command and the estimate, and a person approves each paid call.
3. The candidate side gained two more checks and its hand-off: return rate by line with the reasons (room metric, from orders and the return leg), the first run and its MOQ (bank idea BRD-249: no first run on file yet for the gift box; a full-MOQ run with no lower-MOQ option is a risk priced at its cash), and a one-page brief per candidate that pulls every block together for creative and sourcing, with a copy button.
4. A new brand no longer needs a hand-written fixture: `web_pass.py --init` writes the template (lanes, markets, preferences, launches, a url and a date per number) and `--check` refuses a number without a source; the connect action names both commands. The checker found 3 gaps in the Bombas file, since fixed. A brand with orders but no monthly product table now gets its category mix, demand pattern and return rates from order line items; on Tallgrass Goods those three blocks fill and the rest say why they cannot.
5. Numbers on Bombas: 78 findings across 37 rules read as 46 cards, 2 of them connect actions; the top 10 is still buyers, positioning and unanswered doubts, with the Amazon stance third. Still unavailable, said so on the page: the live Instagram and listing pulls, actual margin by SKU and Search Console (need the store and the console), and return rates on Bombas (orders are an 8.8 million row table, read through an aggregate; a returns aggregate is a contract ask below).
6. Next, round 5: the plan board's decision row feeding the experiment registry (a go on a candidate opens a test with its win rule and read point); a candidate's brief handed to the creative and landing page desks through the events contract; the pulls block driving a weekly refresh checklist with the ledger's week-to-date; a proposal to move `orders_monthly` and `return_rates` into the metric contract so every screen shares them; and the merged cards showing their sub-findings as a checklist.

## Round 3 note for the founder (28 Sep 2026)

1. The desk now reads the outside as well as the inside: who launches and how often (a lane we sell where competitors keep launching and we have not is in play), who sells us on Amazon and at what price a pair (every offer read is a reseller, no brand store, 11 listings priced 25 percent or more off the site), where buyers talk and where no record shows us (r/BuyItForLife with 22,968 upvotes, Trustpilot with 31 quotes), whether a candidate's demand is one clip or a pattern, and whether a lane's trend rests on history or a forecast (today every lane is forecast only, so the check is open).
2. On Bombas the plan reads 70 findings across 33 rules as 42 cards, 2 of them connect actions; the top 10 stays buyers, positioning and unanswered doubts, with the Amazon stance decision third. The forums collapse into one listening post, the price spreads into the Amazon card, the launch cadence into the lane brief, so a merged card still carries every finding it covers.
3. The candidate side gained the operations checks: a versioned tech pack per candidate (tolerances, BOM, packaging cost), the research hours budget per stage (sprawl fires when hours pass it), and the demand pattern tag with its cash timing; each still lands on the candidate's single card.
4. The desk is no longer Bombas-shaped. The web pass and social pull fixtures now say whose they are and any other brand reads none of them; the lanes moved out of the code into the web pass. On Tallgrass Goods (kitchen goods, no brain, no web pass) every block shows its honest empty state and every action is a connect action; `round3s.png` shows it. The rank route serves the sample brand too.
5. Still unavailable, said so on the page: the seller of record per listing (the listing actor has not run), the live Instagram pull (refused by the build session's permission check; the mock file is used), 10 configured subreddits and 4 social surfaces with no pull yet (each a paid call a person approves), actual margin by SKU and Search Console demand (need the store and the console connected), and multi-year history on any lane (the web pass holds one point and a forecast per market).
6. Next, round 4: refresh the Reddit and review pulls through the connector on a schedule with the ledger; a per-brand web pass runner so a new brand gets its lanes, markets and launches without a hand-written fixture; the listing actor run for the seller of record under the caps; category mix from orders when a brand has no monthly product table; and the plan board's decision row wired to the decisions log so a founder's go, hold or kill is remembered across sessions.

## Round 2 note for the founder (28 Sep 2026)

1. A founder can now run the candidate side of the desk end to end: screen an idea in (or take one from a gap above), watch it move through the fast checks, the margin gate, the demand pattern and cash plan, the angle and the 5 go-live gates, the compliance check and the scorecard, and decide go, hold or kill from the memo. Every write lands in the pipeline log; nothing is bought or listed.
2. On the seeded Bombas candidates the desk says: the holiday gift box scores 86 and passes every gate (go, once a cash plan is attached); the easy pull-on compression sock scores 81 and waits on compliance; the merino sock has no angle yet; the made-in-USA line fails the screen, the margin gate (16 percent against a 22 percent floor) and the price signal (no go).
3. What changed: 9 new desk blocks, 12 new rules (PROD-R14 to R25), the one thing this screen writes (candidates), and the research-tool jobs rebuilt as rules on our own data: trend against saturation with the bank's seller ladder, sustained ad spend by run length, the review price signal, complaint mining per listing. Bank ideas taken by id: PRD-052, PRD-079, PRD-023, PRD-024, PRD-044, PRD-045, PRD-005.
4. The plan at the top now carries one card per candidate (the biggest open item hosts the rest), so 42 findings read as 31 actions and the top 10 stays about buyers and positioning, with the candidates underneath.
5. Still unavailable, said so on the page: actual margin by SKU (needs the store connected), Search Console demand, the live Instagram pull, and the lead time for cash plans (no operations record holds one).
6. Next, round 3: the web pass on what Particl, Jungle Scout, Exploding Topics, Glimpse, SparkToro and Similarweb show that this desk does not, rebuilt as rules; a second brand folder so the tests prove the desk is not Bombas-shaped; tech pack versions per candidate (PROD-C13); and the Reddit and review pulls refreshed through the connector on a schedule.

## Round 1 note for the founder (28 Sep 2026)

1. A founder can now open the research desk and see, first, the 10 moves ranked by the rubric: win back the 5 big buyer segments whose main doubt no ad answers (repeat revenue at risk computed per segment), take the "buy it for life" position with proof next to the price, answer the 4 unanswered review themes, decide the made-in-USA position, and brief the lanes competitors push that we never advertise (guarantee, merino, style, gifting before the holiday window, underwear, t-shirts, sustainability).
2. Every move has an owner (agent drafts and you approve, or the agent does it), the numbered steps with who does each, the artefact (ad brief, page section, offer spec, research note, lander), a win rule, a stop rule and a check date. "Copy brief" and the decision row sit on every item.
3. What changed: the round 0 report (tiles, insight cards, a units chart) is gone. The desk now has 9 blocks, each ending in a gap line and an action: trends against our mix, competitor lanes and launches, the conversation by theme and source with an Instagram pull, shifting preferences, the positioning map, the avatar by line matrix, search term groups, the falling-behind list, plus demand, prices, reviews and the pipeline.
4. The audit grew from 2 rules to 13. Every number is computed in code from the brain, the aggregates and two fixtures (a public web pass with a url and a date on every number, and the social pull). Unavailable is shown as unavailable: the catalog, Search Console and the live Instagram run are not connected in the build container.
5. Two things need Kevin: the Instagram live pull was refused by the build session's permission classifier (estimate $0.56, under the caps), so the block reads the mock file and says so; and the connector price for the hashtag actor is a contract ask below.
6. Next: round 2 takes the rest of the room spec (candidate pipeline with the margin gate, time boxes, the shortlist scorecard, video-commerce demand signals) and what the best research tools do (Particl, Jungle Scout, Exploding Topics, Glimpse, SparkToro, Similarweb style jobs) rebuilt as rules on our own data, plus the idea bank.

## Contract asks

- `product_candidates` (events.md names it, data-sources.md does not define it): the table shape this screen writes is in `fixtures/product_candidates.json` (candidate_id, brand, name, category, stage, decision, planned_price_usd, landed_cost_estimate_usd, pack_units, gross_margin_pct_from_estimates, first_run, tech_pack_version, tech_pack_status, angle_text, angle_source, review_date, source_finding, updated_at, simulated). Ask: define it in `data-sources.md` and give it a home in the data layer so 04-offers-pricing and 19-supply-inventory read one path. Likewise the proposed tests in `fixtures/proposed_tests.json` want a route on the shared registry (25-experiments) that accepts a `proposed` row.
- A returns aggregate per brand (`returns_monthly`: month, line or SKU, returns, reasons) next to `products_monthly`, so the return rate by line reads on a brand whose orders are too big to scan; and `orders_monthly` (category mix from order line items) and `return_rates` in `app/metrics.py` so every screen shares them. Until then this screen computes both from the sample brand's order rows and says so.
- `app/connectors/apify.py` PRICES_PER_1000: add `apify~instagram-hashtag-scraper` at about $2.30 per 1,000 results (Apify Store, 28 Sep 2026). Until then `social_pull.py` sets the price at run time for its own estimate and stays under the brand's caps through the connector.
- The live Instagram pull (estimate $0.56 for 125 posts) was refused by the build session's permission classifier as a real-world transaction. Kevin or the lead can run `python3 app/screens/01-market-research/social_pull.py --brand bombas --mode live --per-tag 25` from a session that allows it; the page then reads the live file.

## Rounds

| Round | Features picked | Date | Notes |
|---|---|---|---|
| 0 | skeleton, 0.1 to 0.11 | 28 Sep 2026 | S3.6, Bombas simulated set at scale 0.1 |
| 1 | 1.1 to 1.10 | 28 Sep 2026 | plan first, 13 rules (PROD-R01 to R13), rank with a recipe per rule, web pass and social pull fixtures, round1.png and round1b.png |
| 2 | 2.1 to 2.10 | 28 Sep 2026 | the candidate side of the desk: pipeline writes, margin gate, demand pattern, lane map, spend signal, price signal, complaint bars, angle and gates, scorecard; 25 rules (PROD-R01 to R25), one card per candidate; round2.png, round2b.png and round2c.png |
| 3 | 3.1 to 3.10 | 28 Sep 2026 | the outside read and the operations checks: readability pass, video signals, tech packs, hours budget, trend checks, audience surfaces, marketplace seller read, launch cadence, second brand test; 33 rules (PROD-R01 to R33), fixtures bound to a brand; round3.png, round3b.png, round3c.png and round3s.png |
| 4 | 4.1 to 4.10 | 28 Sep 2026 | decision memory, mix and return rates from orders, open questions, the pulls and their freshness, the listing seller pull, the web pass runner, the candidate brief, the first run and its MOQ; 37 rules (PROD-R01 to R37); round4.png, round4b.png, round4c.png and round4s.png |
