# Google Ads: features

Status: todo | doing | done | parked. One feature per commit. The first round is the skeleton; after that, features come in rounds of 10, stack-ranked by revenue impact, usefulness and how easy they are to build on dummy data.

## Round 0: skeleton

| # | Feature | Status |
|---|---|---|
| 0.1 | Page shell in the shared UI kit: simulated banner, founder note, tiles, decision row, insights, tables | done |
| 0.2 | `api.py` serving this screen's numbers from `app/data/brands/bombas/` through `app/metrics.py`, with unavailable states | done |
| 0.3 | 4 tiles (Google spend, Google ROAS, non-brand ROAS, brand share of spend), 1 chart (daily spend or conversions, 90 days, brand vs non-brand) | done |
| 0.4 | Brand vs non-brand split (spend, conversions, value, ROAS, cost per conversion, share of spend) with the brand incrementality flag | done |
| 0.5 | Search terms table, 30 days, with the negatives-to-add and new-keywords rules in `api.term_rule` | done |
| 0.6 | Impression share lost to budget vs rank per Search campaign (clipped days counted, never read as a number) | done |
| 0.7 | Performance Max asset group table (ad strength only; spend by asset group is not in the data, shown unavailable) | done |
| 0.8 | Conversion tracking check: Google conversions and value vs store paid search orders and net sales, last full month, gap stated | done |
| 0.9 | `audit.py` in the audit.md shape: GADS-R01 brand cannibalisation, R02 budget capped, R03 search term waste, R04 tracking gap, R05 lost to rank | done |

Round 0 notes (28 Sep 2026, Bombas simulated, scale 0.1): R01, R02, R04 and R05 fire. R03 fires on nothing: every simulated term converts near its campaign's cost per conversion, so the negatives rule has no rows. R04 fires on value, not count: Google's value per conversion is about 11 percent over the store's net order value (Google's value includes tax and shipping). Brand impression share reads low because days over 90 percent are stored empty. Break-even ROAS is unavailable for Bombas (no cost inputs), so R02 compares against the account's own Google ROAS.

## Jobs to be done (PRODUCT-PLAN.md 5.3), candidates for round 1

| Job | Who does it today | Data needed | How ecomOS helps | Status |
|---|---|---|---|---|
| Split brand and non-brand | search manager | campaign and keyword rows, search terms | brand versus non-brand efficiency, share of spend, incrementality flag on brand | round 0 done; next: brand holdout plan, PMax brand share |
| Mine search terms | search manager | search term report with conversions | negatives to add, new keywords to add, themes rising | round 0 rules done; next: themes rising, n-gram waste |
| Keep the shopping feed healthy | feed manager | Merchant Center statuses and issues | disapprovals and title quality with fixes | todo (no Merchant Center table yet) |
| Read PMax | search manager | asset groups, channel split, asset labels | asset group leaderboard, cannibalisation check against brand search | round 0 ad strength only; leaderboard needs spend by asset group |
| Win the auction where it matters | search manager | impression share, lost share by budget and rank, quality score | where budget is capping, where rank is losing, quality score fixes | round 0 done; next: quality score by keyword |
| Bid to the right target | search manager | conversion values, margins from finance inputs | tROAS and tCPA suggestions from contribution margin, not platform ROAS | todo (needs Bombas cost inputs) |
| Keep tracking right | technical marketer | conversion actions, GA4 reconciliation | conversion audit, value mismatch alerts | round 0 check done; next: GA4 reconciliation |
| Match query to page | search and CRO | landing pages by query, GA4 funnel | landing page fit, speed by page | todo |
| Report | account manager | everything above | weekly summary | todo |

## Candidates from the room spec (pick 10 per round)

### Questions this screen should answer

- where does this account actually break: business, channel, campaign or metric  (MEDIA-C02)
- is real order value passing through cleanly to Google  (MEDIA-C04)
- is Merchant Center compliant and are the free add-ons enrolled  (MEDIA-C30)
- do our titles lead with what people actually search  (MEDIA-C31)
- does every campaign have one funnel job and a written reason  (MEDIA-C32)
- is brand spend inflating the numbers we use to judge non-brand  (MEDIA-C33)
- is our Shopping structure right for our catalogue and margin spread  (MEDIA-C34)
- which keywords are wasting spend and which are ready for more  (MEDIA-C35)
- which PMax defaults are hiding control from us right now  (MEDIA-C36)
- are Search and Shopping dialled in enough to add YouTube  (MEDIA-C37)
- are our lists big enough to use and are customers excluded from cold  (MEDIA-C38)
- should we still be on Maximize Conversion Value or move to Target ROAS  (MEDIA-C39)
- is our daily budget too small or too big for our AOV and stage  (MEDIA-C40)
- have we actually earned the right to add budget or a new campaign type  (MEDIA-C41)

### Metrics specified

- `conversion_tracking_coverage`: Share of purchases where Google gets the real order value. purchases with enhanced conversion value populated / total tracked purchases
- `merchant_center_health`: Whether Merchant Center is approved and add-ons are on. count of open disapprovals + count of the 4 add-ons not enrolled
- `feed_title_quality`: Share of titles that lead with the actual converting search term. titles starting with a top-20 converting search term / total live titles
- `brand_nonbrand_split`: Spend and ROAS split between brand and non-brand. spend and value summed separately for campaigns tagged brand vs non-brand
- `nonbrand_cpa_vs_breakeven`: Is non-brand Search costing more than it can afford to. non-brand CPA / break-even CPA (from margin)
- `pmax_control_flags`: How many control-hiding defaults are still switched on in PMax. count of: URL expansion on, auto assets on, final URL expansion on, across active PMax campaigns
- `pmax_search_terms_coverage`: Share of PMax spend with a visible search term behind it. spend on search terms shown in the PMax insights report / total PMax search spend
- `search_term_waste`: Spend on search terms with no conversions over the waste threshold. sum of spend on terms with 0 conversions and spend over 2x average CPA
- `bid_strategy_stage`: Where the account sits on the bidding ladder. current strategy (Maximize Conversion Value, or Target ROAS with X% of conversions from that strategy)
- `remarketing_list_size`: How big each remarketing list actually is. member count per list
- `cart_abandoner_list_size`: Size of the add-to-cart-minus-purchase list. add-to-cart audience minus purchaser audience, member count
- `budget_vs_sizing_formula`: Is today's budget in the recommended range for our stage. daily budget / (3 to 4x AOV for Search and Shopping, or $50-100 and 3x non-brand CPA for PMax)
- `scaling_gates_passed`: How many of the 5 scaling gates the account currently passes. count of gates passed out of 5 (fixed gate list from MEDIA-C41)
- `youtube_demand_gen_readiness`: Whether Search and Shopping are dialled in enough to add video. checklist score: Search/Shopping hitting target ROAS + proven Meta creative available + AOV fits video funnel
- `google_blended_mer_gap`: Gap between Google's own ROAS and the brand's blended MER. Google-reported ROAS minus blended MER, as a percentage of Google's ROAS
- `disapproval_resolution_days`: How long a disapproved ad or product stays down. days between disapproval flagged and resolved
- `spend_pace_vs_budget_google`: Month-to-date spend against plan, Google only. (spend to date / days elapsed) x days in month vs planned monthly budget
- `new_customer_cac_google`: Cost to win one new customer through Google. Google spend / new customers attributed to Google
- `addon_enrollment_status`: Which of the 4 Merchant Center add-ons are live. count enrolled out of 4
- `campaign_purpose_coverage`: Share of live campaigns with a written one-line purpose. campaigns with a purpose note on file / total live campaigns

### Insights specified (rules in code)

- title missing the converting term: a live product title does not start with a top-20 converting search term for that product type → "{n} titles do not lead with the term that actually converts." (action MEDIA-C31)
- PMax hiding control: URL expansion, auto assets or final URL expansion is still on for an active PMax campaign → "{campaign} still has {setting} on. Turn it off to see and control what runs." (action MEDIA-C36)
- brand not excluded from cold: a non-brand or PMax campaign has no brand negative list or exclusion applied → "{campaign} has no brand exclusion. Brand searches may be inflating its ROAS." (action MEDIA-C33)
- search term wasting spend: a search term has spent over 2x average CPA with 0 conversions in 30 days → "'{term}' spent {amount} with 0 conversions. Add it as a negative." (action MEDIA-C35)
- remarketing list too small: a remarketing or cart-abandoner list is below the platform's minimum serving size → "{list} has {n} members, below the size Google needs to serve it. Wait before launching." (action MEDIA-C38)
- ready to progress bid strategy: conversion volume has held above the platform's Target ROAS threshold for 4 straight weeks on Maximize Conversion Value → "Volume has supported Target ROAS for 4 weeks. Consider moving up a stage." (action MEDIA-C39)
- budget outside the sizing formula: daily budget falls outside the AOV or CPA-based sizing range for the campaign's stage → "{campaign}'s budget is {pct}% outside the recommended range for its stage." (action MEDIA-C40)
- scaling gate failed: fewer than 5 of 5 scaling gates pass → "Only {n} of 5 scaling gates pass. Hold budget until the rest clear." (action MEDIA-C41)
- Merchant Center disapproval spike: open disapprovals rose 25% or more week over week → "Disapprovals rose to {n} this week, up from {prev}." (action MEDIA-C30)
- YouTube added too early: a YouTube or Demand Gen campaign is live while youtube_demand_gen_readiness has an unmet checklist item → "YouTube is spending before {unmet_item} is in place." (action MEDIA-C37)
- conversion value gap: conversion_tracking_coverage is under 95% → "{pct}% of purchases are passing real order value. The rest look like $0 conversions to Google." (action MEDIA-C04)
- Google vs blended MER gap: google_blended_mer_gap is 20% or more → "Google reports {google_roas}x but the brand's own numbers say {mer}x." (action MONEY-C23)
- non-brand above break-even: nonbrand_cpa_vs_breakeven is over 1.0 → "Non-brand CPA is {pct}% over break-even. Cut before adding budget." (action MONEY-C09)
- campaign with no purpose on file: a live campaign has no one-line purpose note → "{campaign} has no written purpose. Reporting confusion usually starts here." (action MEDIA-C32)

### Visuals specified

- channel-type funnel (grouped bar): spend and ROAS for Search, Shopping, PMax and YouTube side by side
- scaling gate checklist (5-light checklist): each of the 5 scaling gates as pass or fail
- feed quality scorecard (scorecard tiles): title quality %, open disapprovals, add-ons enrolled
- bid strategy ladder (step progress bar): current stage on the Maximize Conversion Value to Target ROAS ladder, with the volume needed for the next step
- search terms waste table (sortable table): search terms ranked by wasted spend, with a one-click negative-keyword action
- budget sizing gauge (gauge): today's budget against the formula's recommended range
- brand vs non-brand split (stacked bar): spend and ROAS for brand vs non-brand over time

### Not in the usual tools

- shows the 5 scaling gates as one pass/fail checklist before a scale recommendation is allowed through
- sizes budgets to the brand's own AOV and non-brand break-even CPA, not a generic recommended-budget number
- flags every Performance Max default that hides control (URL expansion, auto assets, final URL expansion) in one view
- reconciles Google's own reported ROAS against the brand's blended MER before any scale call, using the brand's own margin data
- checks feed titles against the brand's own converting search terms, not a generic title-length or keyword-stuffing checklist
- reads the PMax search terms report next to a bid-strategy-stage gate, so a brand does not move to Target ROAS before it has volume

### Data this screen needs

- `google_ads_campaign_daily`: campaign_id, campaign_type, date, spend, conversions, conversion_value, impressions, clicks (Google Ads API (not yet connected))
- `google_search_terms`: campaign_id, term, spend, conversions, conversion_value, date (Google Ads Search terms report)
- `merchant_center_feed`: product_id, title, status, disapproval_reason, addon_enrolled (Merchant Center API)
- `google_audience_lists`: list_id, type, member_count, created_at (Google Ads Audience Manager API)
- `brand_revenue_ledger`: date, order_id, channel, new_or_existing_customer, revenue, gross_profit (brand brain (not yet built))
- `campaign_purpose_notes`: campaign_id, purpose, written_by, written_at (brand record, manual entry today)

## Rounds

| Round | Features picked | Date | Notes |
|---|---|---|---|
| 0 | 0.1 to 0.9 | 2026-09-28 | S3.5 on Bombas simulated data |
