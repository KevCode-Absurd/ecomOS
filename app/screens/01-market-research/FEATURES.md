# Products and research: features

Status: todo | doing | done | parked. One feature per commit. The first round is the skeleton; after that, features come in rounds of 10, stack-ranked by revenue impact, usefulness and how easy they are to build on dummy data.

## Round 0: skeleton

| # | Feature | Status |
|---|---|---|
| 0.1 | Page shell in the shared UI kit: header, empty-state tiles, insight list, action buttons | todo |
| 0.2 | `api.py` serving this screen's metrics from `app/data/` with unavailable states | todo |
| 0.3 | 3 metric tiles, 2 insights, 1 chart from the sample brand | todo |

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

## Rounds

| Round | Features picked | Date | Notes |
|---|---|---|---|
