# Offers and pricing: features

Status: todo | doing | done | parked. One feature per commit. The first round is the skeleton; after that, features come in rounds of 10, stack-ranked by revenue impact, usefulness and how easy they are to build on dummy data.

## Round 0: skeleton (done 28 Sep 2026, S3.9, Bombas simulated data)

| # | Feature | Status |
|---|---|---|
| 0.1 | Page shell in the shared UI kit: header, simulated-data banner, tiles, insights, decision row, findings | done |
| 0.2 | `api.py`: `overview` and `findings` under `/api/04-offers-pricing/`, unavailable states, sample brand degrades | done |
| 0.3 | 3 tiles (free shipping threshold vs AOV and break-even, discount share of gross, multi-pack share), 2 insights as rules (threshold pull and move rule; discount creep), 1 chart (AOV and discount share by month, 24 months) | done |
| 0.4 | Offer stack from the brain: threshold, shipping under it, first-order code (ad library, first and last seen), code share in live ads, pack ladder, guarantee, return window, gifting; each with source, link and date | done |
| 0.5 | Free shipping threshold economics: order value in $5 bins (paid vs free), share $10 just under and just over, break-even (AOV + label / margin), the move rule | done |
| 0.6 | Discount policy: discount share by month, BFCM depth against the 28 days before | done |
| 0.7 | Pack ladder: revenue and packs by pack size, paid and list price per pair, drop per rung and vs the single | done |
| 0.8 | Guarantee against objections: top rung of each ladder, proof or none, returns per 1,000 orders for the matching reason | done |
| 0.9 | `audit.py`: OFFER-R01 threshold under break-even (money), OFFER-R03 per-SKU margin unavailable, OFFER-R04 deal-breaker rung with no proof (money floor from returns when above own median) | done |

Metrics added in their own commits: `order_value_distribution`, `returns_by_reason` (`app/contracts/metrics.md`, Offers section).

Known gaps from round 0:
- Per-SKU margin is unavailable: `finance_inputs.json` keys cost by codes like `BMB-SK-M-ANK-1`; products use `BB-ANK-1`. Break-even uses the target gross margin until they join.
- Order-level numbers (bins, returns by reason) read `data.sqlite`; the page shows them as shares or per-order rates and takes volume from the daily totals, so a scale 0.1 build and the scale 1.0 aggregates agree.
- Simulated orders charge $5.99 under the line and use their own codes; the brain's public values ($7.95, COMFORT20) are shown beside them.
- The brain lists 7 and 12 packs; the simulated catalogue has 1, 3, 4, 6 and 8. The 6-pack ankle sock gives no per-pair drop over the 4-pack (a LIFE-C39 candidate).

## Round 1: the execution surface (from 28 Sep 2026, depth contract)

| # | Feature | Status |
|---|---|---|
| 1.1 | Plan first: round 0 tiles, insight cards and the AOV chart removed; plan board from `rank` with 6 orientation numbers (AOV, threshold, orders under it, refunds share, ads with the code, contribution margin); what is wrong ranked; action cards with owner, steps and artefact; desk; audit at the bottom. `actions.py` (rank override), `model.py` (offer economics), `screen.css`. OFFER-R01 now fires from the aggregates and finance inputs when order rows are absent (money null with its reason) | done |
| 1.2 | Objection ladder to offer map: the top rung of every ladder with the offer or proof that answers it (`playbook.py`, brand-agnostic), what in the brain already covers it, cost per claim from finance inputs (item or returns processing, label, pick and pack, box), cost per 1,000 orders at the brain's planned claim rate, returns behind it (labelled fixture while `returns_by_reason` is unavailable). Each open rung is an action with the drafted spec, win and stop rules. OFFER-R04 severity high at 20 one-star mentions; rubric override reputation 4, satisfaction 4 | done |
| 1.3 | Free shipping line: order value bins with the $10 under the line shaded (labelled fixture while order rows are absent), break-even by month against the line (step chart), the gap, and a table of nearby lines with what each must achieve to pay: a higher line pays while fewer than N percent of orders between the lines walk away, a lower one only if orders in the band rise N percent (contribution before media from finance inputs, listed shipping rate from the brain). The test brief carries the walk-away limit. New rules OFFER-R05 (break-even moved more than 5 percent in a year, line did not) and OFFER-R06 (line not pulling, unavailable without order rows) | done |
| 1.4 | Pack ladder: per line, singles' share of packs, the pack saving per item, margin per pack from cogs_landed, and the deeper price test's arithmetic (money given to current pack buyers against margin per trade-up, so the share of single buyers who must trade up). Verdicts push (keep price, preselect the pack, show price per item), deepen (a price test pays back under 25 percent trade-up), add (a basics line sold only as a single gets a pack). New rules OFFER-R07 and OFFER-R09, one merged action per verdict with the drafted page spec, test brief or pack offer; thresholds in `playbook.py`. Ladder math moved to `model.py` | done |
| 1.5 | First-order offer: the code against 4 alternatives (free item, free shipping, dollars off at the line, first-order pack price) at the average list-price order: price paid, cost against full price, contribution before media, payback on paid media per new customer, and how much first-order conversion each can lose against the code. Flags that the code takes the average basket under the free shipping line (the line counts after discount). New rule OFFER-R08 (code in more than half the active ads and a price-keeping offer keeps more), with the test brief and paired ad variants. Money is labelled "at equal conversion" | done |
| 1.6 | Margin waterfall per offer (`Charts.waterfall`, pills to switch): the average order, the first order with the code, the first order with a free item, an order at the free shipping line, the average order with the wear promise; list price, discount, landed cost, pick pack and box, shipping net, payment fee, returns at the brain model rates, before media, paid media, contribution. Each step names its source; a missing input breaks the step and every total after it. Red line: a first order must pay its own media, other orders keep the target contribution margin; proposed offers under it cannot clear approval. New rule OFFER-R10 (live offer under the red line), merged into the first-order test when it is the code | done |
| 1.7 | Promo calendar: 8 US retail windows by date rule (`playbook.PROMO_WINDOWS`, a brand in another market swaps the list), next dates, the approval date (start minus the window's lead), last year's net sales per day against the 28 days before and the discount depth, and whether a brain `plans` record covers it. Timeline plus a verdict table. New rule OFFER-R11: a window due in 30 days with no plan becomes a dated offer spec (approve, briefs, site loaded, report dates), a margin check at last year's depth and a depth cap; money is last year's sales above baseline | done |

## Room jobs

| Job | Question | Capability | Status |
|---|---|---|---|
| Design the offer's full value proposition | does this offer beat the buyer's biggest objection, priced and proven | LIFE-C36 | round 0: guarantee table, OFFER-R04 |
| Model offer and discount economics before launch | what does this discount cost in margin, and does it cross my red line | MONEY-C05 | round 0: threshold break-even, OFFER-R01; margin waits on COGS join |
| Govern discount policy and price integrity | are we training buyers to wait for a discount | LIFE-C38 | round 0: discount share, BFCM depth, creep rule |
| Design bundles and quantity-ladder pricing | does every tier have a reason to exist, is the middle one winning | LIFE-C39 | round 0: pack ladder table |
| Design gift-with-purchase offers | is the gift lifting the tier we want | LIFE-C40 | todo |
| Place upsell and cross-sell offers | which placements convert, and do they hurt margin | LIFE-C41 | todo |
| Design the guarantee and risk-reversal offer | does the guarantee remove risk without breaking margin | LIFE-C42 | todo (claims not tagged) |
| Design the subscription offer and cancel flow | is the reason to subscribe stronger than a flat discount | LIFE-C43 | parked (non-subscription first) |
| Design and model the pop-up first-order offer | does the pop-up offer pay for itself | LIFE-C02 | todo |
| Design referral and partner offers | is referral cheaper than paid media | LIFE-C45 | todo |
| Design payment terms, BNPL and trial pricing | is trial-to-full matching the model | LIFE-C46 | todo |
| Run the offer testing framework | what to test next, is any test untrustworthy | LIFE-C47 | todo |
| Track competitor and MAP pricing | did a competitor or reseller move price | BRN-C11, PROD-C46 | todo |
| Run the gift card program | outstanding gift card liability and redemption | LIFE-C58 | todo |

## Candidates from the room spec (pick 10 per round)

### Questions this screen should answer

- does this offer actually beat the buyer's single biggest objection, priced and proven  (LIFE-C36)
- what does this discount actually cost in margin, and does it cross my red line  (MONEY-C05)
- are we training buyers to wait for a discount  (LIFE-C38)
- does every tier in this ladder have a real reason to exist, and is the middle one winning  (LIFE-C39)
- is this gift lifting the tier we want, or just costing margin for no shift in behavior  (LIFE-C40)
- which placements are actually converting, and are they hurting margin anywhere  (LIFE-C41)
- does the guarantee remove real buyer risk without breaking margin if claims run high  (LIFE-C42)
- is the reason to subscribe stronger than a flat discount, and is the cancel-save offer working  (LIFE-C43)
- does the pop-up offer pay for itself once opt-ins, discount cost and ESP cost are counted  (LIFE-C02)
- is referral acquiring customers cheaper than paid media  (LIFE-C45)
- is the trial-to-full conversion rate matching what we modeled when we priced it  (LIFE-C46)
- what should be tested next, and is any test running so it can't be trusted  (LIFE-C47)
- did a named competitor or reseller just move price on us  (BRN-C11, PROD-C46, BRN-C11)
- how much outstanding gift card liability are we carrying, and is it being redeemed  (LIFE-C58)

### Metrics specified

- `margin_after_discount`: What is actually left after the discount, in dollars, not just percent off. order revenue − COGS − payment fee − discount amount, per order and rolled up per offer
- `free_shipping_threshold_breakeven`: The order value at which free shipping stops costing margin. AOV + (average shipping cost ÷ gross margin rate), recomputed from the brand's live numbers
- `discount_dependency_rate`: Share of revenue that only came in at a discount. revenue from orders with a discount code or automatic discount ÷ total revenue
- `discount_frequency_per_customer`: How often the same customer buys only when there is a discount. count of discounted orders ÷ total orders, per repeat customer
- `bundle_attach_rate`: Share of orders that take the bundle instead of a single item. bundle orders ÷ (bundle orders + single-item orders for the same product line)
- `average_selling_price_trend`: Whether the real price paid, after discounts, is rising or falling over time. total revenue ÷ total units, monthly
- `gwp_cost_share`: What the free gift costs as a share of the order it is attached to. gift COGS ÷ order revenue, for orders that received the gift
- `upsell_take_rate`: Share of eligible customers who accept an upsell or cross-sell offer. orders that included the upsell ÷ orders shown the upsell, by placement (cart, checkout, post-purchase)
- `guarantee_claim_rate`: Share of orders covered by the guarantee that actually file a claim. guarantee claims ÷ orders covered by that guarantee, in the guarantee's window
- `subscription_perk_redemption_rate`: Share of subscribers who actually use a given perk. perk redemptions ÷ active subscribers eligible for that perk
- `cancel_flow_save_rate`: Share of subscribers who accept the save offer instead of cancelling. saves ÷ (saves + completed cancellations)
- `popup_offer_net_economics`: Whether the pop-up offer pays for itself once every cost is counted. incremental revenue from pop-up-sourced first orders − (discount cost + ESP cost allocated to those contacts)
- `referral_program_cac`: Cost to acquire a customer through referral, versus paid CAC. total referral reward cost ÷ number of referred customers who placed an order
- `bnpl_trial_conversion_rate`: Share of trial or BNPL starts that convert to the full-price plan. trials converted to full price ÷ trials started
- `map_violation_count`: Number of listings selling below the agreed minimum advertised price. count of marketplace_listings rows where listed_price < map_price
- `competitor_price_index`: The brand's price versus named competitors, indexed. brand price ÷ average of named competitors' price for the matched product, per SKU family
- `gift_card_liability_outstanding`: Total value of gift cards sold but not yet redeemed. sum of issued_value − sum of redeemed_value, across active cards
- `gift_card_redemption_rate`: Share of issued gift card value that gets redeemed. redeemed value ÷ issued value, for cards past their typical redemption window
- `offer_test_backlog_status`: What is queued, running or done in the offer test backlog, and the win rate. count and status of entries in the offer test registry; win rate = tests won ÷ tests completed

### Insights specified (rules in code)

- discount creep: discount_dependency_rate rises more than 5 percentage points over the trailing 3 months → "discounted revenue went from {a}% to {b}% of sales over the last 3 months" (action LIFE-C38)
- margin red line breach: margin_after_discount for a live offer falls below the founder's stated red-line margin → "{offer} is running at {margin}% margin, below your {redline}% red line" (action MONEY-C05)
- MAP violation detected: map_violation_count > 0 for a listing in the current check → "{n} listings on {marketplace} are priced below the agreed MAP of {map_price}" (action PROD-C46)
- free shipping threshold stale: free_shipping_threshold_breakeven has not been recomputed since AOV or shipping cost moved more than 5 percent → "your free shipping threshold was set when AOV was {old}, it is now {new}" (action MONEY-C05)
- bundle cannibalizing full price: bundle_attach_rate is high (over 40 percent) while average_selling_price_trend for the product line is falling faster than the bundle's per-unit discount would explain → "the bundle is winning {pct}% of orders but per-unit price is falling faster than the bundle discount accounts for" (action LIFE-C39)
- gift cost creep with no lift: gwp_cost_share rises without a matching rise in average_selling_price_trend or bundle_attach_rate for the tier the gift was meant to lift → "the gift now costs {pct}% of order value with no lift in the tier it was meant to push" (action LIFE-C40)
- guarantee cost above plan: guarantee_claim_rate exceeds the claim-rate assumption used to price the guarantee by more than 50 percent relative → "claims are running at {actual}%, against a planned {planned}%" (action LIFE-C42)
- trial conversion miss: bnpl_trial_conversion_rate falls more than 20 percent relative below the modeled conversion used to price the trial → "trial-to-full conversion is {actual}%, against a modeled {planned}%" (action LIFE-C46)
- competitor price move: competitor_price_index moves more than 5 percent in either direction for a named competitor's matched SKU family within a week → "{competitor} moved price {pct}% on {product} this week" (action BRN-C11)
- referral beats paid CAC: referral_program_cac is less than half of blended paid CAC for the same period → "referral CAC is {referral}, less than half of paid CAC at {paid}" (action LIFE-C45)
- overlapping offer tests: two entries in the offer test_registry target the same product or segment with overlapping date ranges → "{test_a} and {test_b} are both running on {segment} at the same time, results cannot be trusted" (action LIFE-C47)
- gift card liability outpacing redemption: gift_card_liability_outstanding grows faster than gift_card_redemption_rate over 3 consecutive months → "outstanding gift card liability has grown {pct}% while redemption has not kept pace" (action LIFE-C58)
- subscription perk mismatch: subscription_perk_redemption_rate for a perk stays under 10 percent for 2 consecutive months → "only {pct}% of subscribers use the '{perk}' perk 2 months running" (action LIFE-C43)
- cancel save rate falling: cancel_flow_save_rate drops more than 10 percentage points versus its trailing 90-day average → "the cancel-flow save offer worked {old}% of the time, now {new}%" (action LIFE-C43)
- competitor policy change: a named competitor's public returns, loyalty or subscription-terms page changes materially since the last check → "{competitor} changed its {policy_type} page: {change}" (action BRN-C11)

### Visuals specified

- margin waterfall (waterfall chart): revenue down to net margin for a chosen offer or discount, step by step
- discount dependency trend (line chart): share of revenue at a discount, monthly, over the trailing 12 months
- free shipping threshold sensitivity (small interactive chart or table): break-even threshold recalculated as AOV, margin or shipping cost inputs change
- competitor price index (line chart): brand price index versus each named competitor over time
- bundle ladder funnel (funnel or bar chart): share of orders choosing each tier in the ladder, single item to largest bundle
- offer test backlog board (kanban-style list with win rate): offer tests planned, running, done, with hygiene flags
- gift card liability vs redemption (dual bar/line chart): outstanding liability and redemption rate over time

### Not in the usual tools

- The free shipping threshold is computed straight from this brand's own live AOV, margin and shipping cost, and flagged stale automatically when those inputs move
- A margin waterfall runs before an offer launches, and a founder-set red line blocks approval if it is crossed
- Discount dependency and price integrity are tracked as one running score across every offer and channel, not just a discount-usage count
- Competitor and MAP price tracking is tied directly into the brand's own offer test backlog and margin data
- Offer tests are checked for overlap (same segment, same window, two variables at once) automatically before a founder is asked to read results
- Gift card liability and redemption are shown together as a cash-flow signal, not just a balance

### Data this screen needs

- `orders`: order_id, sku, unit_count, price, discount_code, discount_amount, cogs, shipping_cost, placed_at (store order export, not yet connected)
- `product_costs`: sku, cogs, shipping_cost_avg (manual or ERP export, not yet connected)
- `discount_codes`: code, type, value, start_at, end_at, terms, conditionality (store discount export, not yet connected)
- `competitor_prices`: competitor, sku_family, price, url, captured_at (LIFE-C56 competitor price watch (agent, public web only))
- `marketplace_listings`: marketplace, sku, listed_price, map_price, checked_at (marketplace price pull, not yet connected)
- `gift_card_ledger`: card_id, issued_value, redeemed_value, issued_at, expiry_at (store gift card export, not yet connected)
- `subscription_plans`: plan_id, perks, price, cadence, redemption_log (subscription platform export (Recharge or equivalent), not yet connected)
- `guarantee_terms`: guarantee_id, coverage, length_days, cost_per_claim_estimate, planned_claim_rate (manual entry from LIFE-C42 design doc)
- `referral_program`: referrer_id, referred_id, reward_cost, order_id, referred_at (referral platform export, not yet connected)
- `bnpl_trials`: trial_id, customer_id, start_price, full_price, started_at, converted_flag, converted_at (BNPL/trial billing export, not yet connected)
- `offer_test_registry`: test_id, offer_type, hypothesis, segment, sku_scope, start, end, metric, result (LIFE-C47 offer testing framework log)

## Rounds

| Round | Features picked | Date | Notes |
|---|---|---|---|
| 0 | skeleton, 0.1 to 0.9 | 2026-09-28 | S3.9; screenshot round0.png |
| 1 | 1.1 plan first, 1.2 objection to offer map, 1.3 free shipping line, 1.4 pack ladder, 1.5 first-order offer, 1.6 margin waterfall, 1.7 promo calendar | 2026-09-28 | manager session; screenshot round1.png (updated as the round lands) |


## Round 1 candidates (ranked 28 Sep 2026 by the lead session)

Ranked by revenue impact, usefulness to a founder deciding alone, and buildable on the simulated data. Kevin picked the 5 screens; the top 5 here are recommended for round 1. One feature per commit, this table updated in the same commit.

| # | Feature | Capability | Why buildable now | Impact |
|---|---|---|---|---|
| 1.1 * | Margin waterfall per offer, revenue down to net, with a founder red line that blocks approval | MONEY-C05 | orders, discount codes and finance inputs exist | high |
| 1.2 * | Free shipping threshold sensitivity: break-even recomputed live from AOV, margin and shipping cost, with the stale flag | MONEY-C05 | already a finding; make the inputs adjustable | high |
| 1.3 * | Discount dependency trend over 12 months with the discount-creep rule | LIFE-C38 | discounted revenue share by month from orders | high |
| 1.4 * | Bundle ladder funnel: share of orders per pack size with the cannibalization rule | LIFE-C39 | pack sizes in products and order_lines | high |
| 1.5 * | Competitor price index from Amazon listings and Ad Library offers, plus MAP violation count | BRN-C11 | marketplaces records and learnings; signals only | medium |
| 1.6 | Offer test backlog board wired to the experiment registry with the overlap check | LIFE-C47 | registry from screen 25 | medium |
| 1.7 | Guarantee claim rate against the modelled 2 percent replacement rate | LIFE-C42 | reversed_orders replacements versus the brain's return_share_model | medium |
| 1.8 | Gift card liability against redemption, on a fixture until the ledger connects | LIFE-C58 | gift cards exist in products; the ledger does not | low |
| 1.9 | Upsell take rate by placement | LIFE-C41 | unavailable until the upsell app connects (Rebuy is in the stack) | low |
| 1.10 | Referral CAC against paid CAC | LIFE-C45 | unavailable until a referral platform connects | low |

\* recommended for round 1
