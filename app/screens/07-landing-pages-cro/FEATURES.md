# Landing pages and CRO: features

Status: todo | doing | done | parked. One feature per commit. The first round is the skeleton; after that, features come in rounds of 10, stack-ranked by revenue impact, usefulness and how easy they are to build on dummy data.

## Round 0: skeleton

| # | Feature | Status |
|---|---|---|
| 0.1 | Page shell in the shared UI kit: header, empty-state tiles, insight list, action buttons | done |
| 0.2 | `api.py` serving this screen's metrics from `app/data/` with unavailable states | done |
| 0.3 | 3 metric tiles, 2 insights, 1 chart from the sample brand | done |
| 0.4 | Funnel by device with the break per device, money at stake by device, funnel by source | done |
| 0.5 | Page registry (site_map plus landing pages, funnel rates, speed where speed_runs has one) | done |
| 0.6 | Message match: Ad Library promises from the brain against captured page records | done |
| 0.7 | PDP objection-proof map from the objection ladders | done |
| 0.8 | Test registry seeded empty (hypothesis, metric, sample size rule, read date) | done |
| 0.9 | `audit.py`: CRO-R07 device break, CRO-R02 lander message mismatch, contract shape | done |

Round 0 notes (28 Sep 2026, Bombas simulated, scale 0.1):
- New metric `session_funnel` in `app/metrics.py` (see `contracts/metrics.md`), because orders by device are not in the daily aggregate. Purchase is GA4 ecommercePurchases.
- In this data the mobile break is at add to cart (4.99 percent against a median of 5.23 percent), not checkout to purchase, which sits at its median on every device. CRO-R07 checks every step, so it names whichever step breaks.
- Message match reads the brain: the ad side is the Ad Library records (COMFORT20 offer, comfort hook, giving line); the page side is site-captured records for that path. Only the home page is captured, so the other paid landers read unavailable, not mismatch. The ad table has no copy or landing URL; the lander comes from GA4 paid social sessions.
- Speed shows unavailable: the `speed_runs` fixture has no `device` or `measured_at` column, so `lcp_ms` cannot read it. A fix belongs in the generator or the speed metric, not here.
- Stake on a mismatch is the lander's drop against its own median; the mismatch is the named cause, not a proven one (confidence minus 0.2).

## Room jobs (Landing pages and CRO)

| Job | Question | Capability | Status |
|---|---|---|---|
| decide where an ad or search click should land | should this click go to a PDP, an advertorial, a quiz or a sales page | SITE-C35 | todo |
| check the ad's promise survives to the page and the cart | does the price, guarantee and offer on the ad still match at checkout | SITE-C36 | round 0: page side from the brain |
| build and score the hero section | is the hero specific enough to stop the scroll | SITE-C37 | todo |
| fix the PDP first screen | does the buy box have everything a phone shopper needs without scrolling | SITE-C38 | todo |
| write on-page copy in the customer's own words | does the copy sound like our reviews and tickets, or like a template | SITE-C39 | todo |
| place proof next to the objection it answers | is our proof actually next to the doubt it is meant to remove | SITE-C40 | round 0: proof map |
| build bundle and offer pricing with real anchors | does the bundle show a real saving in dollars, not just a percent | LIFE-C39 | todo |
| write urgency and scarcity that is true | is our low-stock message wired to real inventory or just typed in | SITE-C42 | todo |
| strip friction off a single-offer page | what on this page distracts from the one thing we want the shopper to do | SITE-C43 | todo |
| build and QA a page mobile-first | does this page actually work on our own customers' phones | SITE-C44 | round 0: device break |
| score and rank the test backlog | which test is worth running next, and why | LOOP-C09 | round 0: registry seeded |
| QA a test before it goes live | will this test track correctly and not flicker on a slow connection | SITE-C51 | todo |
| read a finished test's results | did this test actually win, and is it safe to trust | SITE-C52 | todo |
| decide whether to scale a winner | does this winner still look good once returns and repeat orders are in | SITE-C53 | todo |

## Candidates from the room spec (pick 10 per round)

### Questions this screen should answer

- should this click go to a PDP, an advertorial, a quiz or a sales page  (SITE-C35)
- does the price, guarantee and offer on the ad still match at checkout  (SITE-C36)
- is the hero specific enough to stop the scroll  (SITE-C37)
- does the buy box have everything a phone shopper needs without scrolling  (SITE-C38)
- does the copy sound like our reviews and tickets, or like a template  (SITE-C39)
- is our proof actually next to the doubt it is meant to remove  (SITE-C40)
- does the bundle show a real saving in dollars, not just a percent  (LIFE-C39)
- is our low-stock message wired to real inventory or just typed in  (SITE-C42)
- what on this page distracts from the one thing we want the shopper to do  (SITE-C43)
- does this page actually work on our own customers' phones  (SITE-C44)
- which test is worth running next, and why  (LOOP-C09)
- will this test track correctly and not flicker on a slow connection  (SITE-C51)
- did this test actually win, and is it safe to trust  (SITE-C52)
- does this winner still look good once returns and repeat orders are in  (SITE-C53)

### Metrics specified

- `message_match_score`: how much of the ad's promise still shows on the page and at checkout. matched elements (price, persona, guarantee, CTA wording) divided by total tracked elements from the ad, for the ad's own landing path
- `hero_headline_specificity`: how concrete the hero headline is about the outcome. rule-based check: contains a number, a timeframe or a named result versus a vague claim, scored 0 to 3
- `pdp_first_screen_completeness`: how many of the 5 required buy-box elements show without scrolling on the brand's own phone. count of (price, proof, CTA, variant picker, delivery info) visible above the fold on the brand's stated device, divided by 5
- `mobile_form_field_count`: how many fields a shopper fills before they can act, on mobile. count of required input fields on the page's primary form (checkout, quiz start, or capture)
- `funnel_step_conversion`: what share of visitors move from one step to the next. sessions reaching step N+1 divided by sessions reaching step N, for landing page to PDP to cart to checkout to purchase
- `test_expected_profit_ceiling`: the most this test could realistically be worth if it wins. estimated lift range x affected traffic x average order value x margin, capped at a stated ceiling assumption
- `test_sample_size_required`: how many visitors this test needs before its result can be trusted. computed from the chosen minimum detectable effect, baseline conversion rate and the test's statistical engine
- `days_to_significance_at_current_traffic`: how many more days this test needs at today's traffic. (sample_size_required minus visitors so far) divided by average daily visitors to the test
- `sample_ratio_mismatch_flag`: whether traffic split evenly between the test arms the way it was set up to. chi-square check of visitor counts per arm against the configured split
- `device_split_of_test_traffic`: how the test's visitors split between mobile and desktop. count of test sessions grouped by device type
- `novelty_decay_pct`: how much of the lift was just people noticing something new. lift in week 1 of the test minus lift in the weeks after, divided by week 1 lift
- `winner_ltv_return_check`: whether a scaled winner still looks good after returns and repeat orders are counted. compare 30 and 60 day return rate and repeat-purchase rate of the winner cohort against the control cohort
- `landing_page_load_status`: whether the page this room is scoring is also fast enough to run traffic to. pulled from the Site and speed room's fully_loaded_mobile and page_weight_budget_status for the same page
- `urgency_claim_truth_status`: whether a displayed stock count or countdown is wired to a real number. compare the displayed value against the live inventory or promo end-date feed at the same timestamp
- `proof_placement_coverage`: how many of the page's objections have proof placed next to them. count of objections with a mapped proof element within the same page section, divided by total objections on the brand's objection list

### Insights specified (rules in code)

- message-match break: message_match_score for an ad's landing path is under 100 percent → "the ad promises {promise} but the page says {page_text}, a mismatch on {element}" (action SITE-C36)
- hero missing a FUD reducer: no risk-reversal element (guarantee, free returns, security badge) sits within the hero's first viewport → "the hero on {page} has no reassurance next to the button" (action SITE-C37)
- PDP first screen incomplete: pdp_first_screen_completeness is under 5 of 5 on the brand's stated device → "{missing_element} does not show without scrolling on {device}" (action SITE-C38)
- mobile form too long: mobile_form_field_count is over 4 → "{page}'s form asks for {n} fields on a phone; the guideline is 4" (action SITE-C44)
- popup fires on load not on intent: a popup's trigger event fires on page load or a fixed timer instead of exit intent or scroll depth → "the popup on {page} interrupts before the shopper has shown any intent to leave" (action SITE-C43)
- fake urgency detected: urgency_claim_truth_status is mismatch → "{page} shows '{displayed_text}' but the real number is {actual_value}" (action SITE-C42)
- sample ratio mismatch on a live test: sample_ratio_mismatch_flag fails → "test {test_name} is splitting traffic unevenly; its result cannot be trusted yet" (action SITE-C51)
- win driven by novelty: novelty_decay_pct over 40 percent → "{test_name}'s lift fell {pct}% after week 1; the early win may not hold" (action SITE-C52)
- winner scaled without an LTV check: a test's status is shipped_to_100 and winner_ltv_return_check is unavailable more than 60 days after rollout → "{test_name} shipped {days} days ago with no return or repeat check run yet" (action SITE-C53)
- high-value backlog item stalled: a backlog hypothesis in the top quartile of test_expected_profit_ceiling has been sitting untested for over 45 days → "{hypothesis} could be worth {ceiling} and has waited {days} days untested" (action LOOP-C09)
- broken interactive control: a button, tab or accordion on a QA pass returns no visible change on click → "{control} on {page} does nothing when tapped" (action SITE-C43)
- bundle savings shown only as a percent: a bundle or offer block shows a percent-off with no dollar amount saved → "{offer} shows {pct}% off with no dollar saving stated" (action LIFE-C39)
- proof stacked once instead of scattered: over 70 percent of a page's proof elements sit in a single section instead of distributed to their matched objection → "{page} has most of its proof in one place; {n} objections have none nearby" (action SITE-C40)
- traffic routed to the wrong page type: a SKU's assigned awareness stage does not match the page type its ads currently point to (for example a cold, unaware audience sent straight to a bare PDP) → "{sku}'s ads target a cold audience but land on a bare PDP with no story" (action SITE-C35)
- test flicker on a slow connection: the QA pass on a throttled connection shows the original page for over 300 ms before the variant renders → "{test_name} flashes the original page for {ms} ms before the variant loads, on a slow connection" (action SITE-C51)

### Visuals specified

- funnel by page (step or sankey chart): sessions moving from landing page to PDP to cart to checkout to purchase, for the current page set
- test backlog ranked list (horizontal bar list): each hypothesis with its expected profit ceiling and evidence count
- message-match trace (flow diagram): the ad's promise elements carried across to the page and checkout, with breaks marked in red
- hero score card (scorecard with sub-scores): the hero's proof, headline, subhead, CTA and FUD scored against the fixed 6-part order
- test result chart (bar chart with confidence interval): conversion rate per arm with its confidence interval and sample ratio check
- winner LTV check (line chart, two cohorts): return rate and repeat-purchase rate for the winner cohort versus control, day 0 to day 60
- PDP first-screen map (annotated screenshot): the brand's real PDP screenshot on its own device with the 5 required elements marked present or missing

### Not in the usual tools

- audits whether the ad's exact promise, price, guarantee and CTA wording survives unbroken from the ad to the page to checkout
- ranks the test backlog by an expected-profit ceiling built from at least 2 pieces of evidence per hypothesis, before anything launches
- checks a scaled winner's return rate and repeat-purchase rate before calling it a lasting win
- flags an urgency or scarcity claim as false the moment its displayed number stops matching real inventory or a real promo end date
- ties funnel drop-off to the page-routing decision (PDP versus advertorial versus quiz versus sales page) for that SKU's awareness stage

### Data this screen needs

- `page_registry`: page_id, page_type, sku, awareness_stage, url, device_screenshot_ref (manual entry plus SITE-C35 routing rules)
- `ad_page_checkout_trace`: ad_id, page_id, promise_elements, match_status, checked_at (SITE-C36 audit script)
- `funnel_events`: session_id, step, page_id, device, timestamp (GA4 or the brand's own pixel export)
- `cro_test_registry`: test_id, hypothesis, evidence_count, expected_profit_ceiling, mde, sample_size_required, stopping_rule, status, launched_at (SITE-C49 and SITE-C50 design output)
- `cro_test_results`: test_id, arm, visitors, conversions, revenue, device, week (test platform export (VWO, Convert or native))
- `winner_ltv_followup`: test_id, cohort, day30_return_rate, day60_return_rate, day30_repeat_rate, day60_repeat_rate (sales data joined to the test's order list)
- `inventory_feed`: sku, stock_count, updated_at (platform inventory API)
- `objection_proof_map`: sku, objection, proof_element, page_section (SITE-C40 proof map, built from reviews and tickets)

## Rounds

| Round | Features picked | Date | Notes |
|---|---|---|---|
| 0 | 0.1 to 0.9 | 28 Sep 2026 | skeleton on Bombas simulated data; screenshot in round0.png |
