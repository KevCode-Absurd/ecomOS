# Affiliate, marketplace and retail media: features

Status: todo | doing | done | parked. One feature per commit. The first round is the skeleton; after that, features come in rounds of 10, stack-ranked by revenue impact, usefulness and how easy they are to build on dummy data.

## Round 0: skeleton

| # | Feature | Status |
|---|---|---|
| 0.1 | Page shell in the shared UI kit: header, empty-state tiles, insight list, action buttons | todo |
| 0.2 | `api.py` serving this screen's metrics from `app/data/` with unavailable states | todo |
| 0.3 | 3 metric tiles, 2 insights, 1 chart from the sample brand | todo |

## Candidates from the room spec (pick 10 per round)

### Questions this screen should answer

- who is asking to join and who should get in  (MEDIA-C49)
- are our active affiliates doing what they agreed to  (MEDIA-C49)
- is anyone gaming commission without earning it  (MEDIA-C50)
- are we paying the right rate to the right partner  (MEDIA-C51)
- does the payout the network wants match what actually sold and stayed sold  (MEDIA-C51)
- what should whoever runs our marketplace ads actually do this month  (MEDIA-C52)
- what should whoever runs our Flipkart ads actually do this month  (MEDIA-C52)
- is rapid-delivery retail media worth a self-serve ad budget and how much  (MEDIA-C53)
- is quick commerce worth a self-serve ad budget and how much  (MEDIA-C53)
- are Meta and Google retargeting pools saturated enough to justify a DSP  (MEDIA-C54)
- does what Meta, Google and TikTok actually billed match what they reported and what we budgeted  (MONEY-C15)
- is every new invoice matched automatically or sitting unresolved  (MONEY-C15)
- who is already talking about us for free, before we pay anyone  (ORG-C49)

### Metrics specified

- `affiliate_pipeline`: How many applicants are waiting, approved or rejected. count of applications by status (pending, approved, rejected)
- `active_partner_count`: How many affiliates and creators are actively earning. count of partners with at least 1 sale in trailing 30 days
- `commission_owed_vs_paid`: Gap between what the network says is owed and what was actually paid. network-reported commission owed minus verified paid amount
- `fraud_flag_count`: Number of open suspected-fraud flags. count of affiliates matching fast click-to-conversion, suspect ISP, brand-bidding or big-ticket-early-order patterns
- `commission_rate_coverage`: Share of partners with a set commission tier on file. partners with an assigned tier / total active partners
- `marketplace_brief_status`: Where the Amazon, Walmart Connect or Target Roundel ads brief stands. status flag: drafted, sent, acknowledged, live (manually updated)
- `marketplace_acos_reported`: Amazon's, Walmart's or Target's own ACOS, as last reported to us. ad spend / ad-attributed sales, taken from whoever runs the account
- `flipkart_brief_status`: Where the Flipkart ads brief stands. India only; reads null for US brands, which use marketplace_brief_status instead.. status flag: drafted, sent, acknowledged, live
- `rapid_delivery_plan_status`: Where the Instacart/DoorDash/Gopuff retail media plan stands, per platform. status flag per platform: drafted, sent, live
- `quick_commerce_plan_status`: Where the Blinkit/Zepto/Instamart plan stands, per platform. India only; reads null for US brands, which use rapid_delivery_plan_status instead.. status flag per platform: drafted, sent, live
- `rapid_delivery_roas_benchmark_gap`: How reported rapid-delivery/grocery marketplace ROAS compares to the category benchmark. reported ROAS (manually entered) minus benchmark (4-8x established SKUs, 1.5-3x new launches)
- `quick_commerce_roas_benchmark_gap`: How reported quick-commerce ROAS compares to the category benchmark. India only; reads null for US brands, which use rapid_delivery_roas_benchmark_gap instead.. reported ROAS (manually entered) minus benchmark (4-8x established SKUs, 1.5-3x new launches)
- `retargeting_saturation_signal`: Whether Meta and Google retargeting pools are maxed out. retargeting frequency at or above cap with flat reach, on both Meta and Google, for 14+ days
- `invoice_vs_reported_variance`: Gap between a platform's invoice and its own reported spend. invoiced amount minus platform-reported spend for the same period
- `invoice_vs_ledger_variance`: Gap between an invoice and the brand's own budget ledger. invoiced amount minus ledger-recorded spend for the same period
- `sales_tax_1099_reconciliation_status`: Whether US sales tax charged on ad invoices and 1099 filings tied to the ledger are reconciled. count of invoices with sales-tax and 1099 records matched to the accounting ledger / total invoices
- `gst_rcm_reconciliation_status`: Whether GST and reverse-charge credits on ad invoices are reconciled. India only; reads null for US brands, which use sales_tax_1099_reconciliation_status instead.. count of invoices with GST/RCM matched to the credit ledger / total invoices
- `billing_dispute_count`: Open disputes with a platform over billing. count of open disputes
- `organic_mentions_found`: Creators found organically using or reviewing the product. count of public posts matching the brand or close competitor, found this scan
- `whitelist_outreach_conversion`: Share of discovered creators who became paid partners. creators who signed on / creators contacted
- `affiliate_share_of_new_customers`: Share of new customers coming through the affiliate program. new customers with an affiliate attribution / total new customers
- `coupon_abuse_rate`: Share of coupon redemptions that look abusive. redemptions flagged (reused past limit, resold, or from a flagged affiliate) / total redemptions

### Insights specified (rules in code)

- fast click-to-conversion fraud pattern: a new affiliate's clicks convert in under the platform's normal minimum browse time, repeatedly → "{affiliate} converts clicks in under {seconds}s, {n} times this week. Check for cookie stuffing." (action MEDIA-C50)
- big-ticket order right after signup: a new affiliate generates an order for a top-price-band item within 48 hours of joining → "{affiliate} placed a {amount} order {hours}h after joining. Hold this payout for review." (action MEDIA-C50)
- unusual orders-to-clicks ratio: an affiliate's orders-to-clicks ratio is 3x or more the program average → "{affiliate}'s conversion rate is {x} the program average." (action MEDIA-C50)
- commission mismatch: commission_owed_vs_paid variance exceeds 2% of the payout cycle total → "The network wants {amount} more than verified sales support. Reconcile before paying." (action MEDIA-C51)
- brand-bidding affiliate: an affiliate is found bidding on the brand's own name in paid search → "{affiliate} is bidding on '{brand_term}' in search. This usually breaks program terms." (action MEDIA-C50)
- invoice does not match platform report: invoice_vs_reported_variance exceeds 1% → "{platform}'s invoice is {pct}% off its own reported spend for {period}." (action MONEY-C15)
- invoice does not match ledger: invoice_vs_ledger_variance is non-zero → "{platform}'s invoice is {amount} off the budget ledger for {period}." (action MONEY-C15)
- sales tax or 1099 credit unreconciled: an invoice's sales-tax charge or 1099 record has not been matched to the accounting ledger → "{n} invoices have sales-tax or 1099 records not yet matched." (action MONEY-C15)
- GST credit unreconciled: an invoice's GST/RCM has not been matched to the accounting credit ledger. India only; does not fire for US brands. → "{n} invoices have GST credits not yet matched." (action MONEY-C15)
- retargeting pool saturated: retargeting_saturation_signal is true on both Meta and Google → "Both Meta and Google retargeting are capped with flat reach. Worth a DSP pilot." (action MEDIA-C54)
- rapid-delivery retail media underperforming benchmark: rapid_delivery_roas_benchmark_gap is negative by more than 20% → "{platform} ROAS is {pct}% below the category benchmark." (action MEDIA-C53)
- quick commerce underperforming benchmark: quick_commerce_roas_benchmark_gap is negative by more than 20%. India only; does not fire for US brands. → "{platform} ROAS is {pct}% below the category benchmark." (action MEDIA-C53)
- organic mention worth whitelisting: a discovered organic mention has engagement above the brand's set threshold and is not already a paid partner → "{creator} is already showing your product organically with {engagement} engagement. Reach out before offering payment." (action ORG-C49)
- coupon abuse rising: coupon_abuse_rate rose 1 point or more week over week → "Coupon abuse rose to {pct}% this week." (action MEDIA-C50)

### Visuals specified

- affiliate funnel (funnel chart): applied, approved, active, flagged counts
- commission reconciliation table (table): owed vs paid vs variance, per payout cycle, per affiliate above a threshold
- billing reconciliation waterfall (waterfall): platform-reported spend, invoiced amount and ledger amount for the period, with the gaps labelled
- marketplace brief status board (kanban-style status board): Amazon, Walmart, Target, Instacart, DoorDash and Gopuff briefs by status (drafted, sent, live), plus Flipkart, Blinkit, Zepto and Instamart briefs for the India option
- creator mention feed (card feed): discovered organic mentions with engagement and whitelist status
- DSP readiness gauge (gauge): days of sustained retargeting saturation against the threshold that triggers a DSP evaluation

### Not in the usual tools

- flags affiliate fraud using fast click-to-conversion, suspect ISP, big-ticket-early-order and brand-bidding rules together, tied back to the exact commission owed
- reconciles what an affiliate network says is owed against verified sales and refunds before a payout is approved
- turns Amazon, Walmart, Target and rapid-delivery plans (Flipkart and quick-commerce plans for the India option) into a handoff brief with targeting, budget and a category ROAS benchmark, and says plainly that live performance stays unavailable until those accounts are connected
- matches each platform's invoice, including applicable US sales tax and 1099 records (GST and reverse-charge credits for the India option), against both its own reported spend and the brand's budget ledger in one reconciliation
- surfaces creators already wearing or reviewing the product organically as whitelist candidates before any outreach cost is paid
- keeps founder-gate calls (fraud holds, payout disputes, DSP spend, commission tier changes) in one queue instead of split across the affiliate network's UI, each platform's billing page, and email

### Data this screen needs

- `affiliate_applications`: applicant_id, status, applied_at, reviewed_at, reviewer_note (affiliate network API or brand record)
- `affiliate_clicks_orders`: affiliate_id, click_at, order_at, order_id, amount, ip_or_isp (affiliate network API)
- `commission_tiers`: affiliate_id, partner_type, category, customer_status, rate (brand record)
- `affiliate_payout_cycles`: cycle_id, network_owed, verified_owed, paid, variance (affiliate network payout report + brand order data)
- `marketplace_briefs`: platform, brief_id, status, sent_at, acknowledged_at (brand record (no connector to Amazon/Walmart/Target/Instacart yet; Flipkart/quick-commerce for the India option))
- `platform_invoices`: platform, invoice_id, period, invoiced_amount, sales_tax_1099, gst_rcm_india, reported_spend, ledger_spend (platform billing portals (manual pull) + intelligence/budget.py)
- `organic_mentions`: creator_handle, platform, post_url, found_at, engagement, whitelist_status (public social scan (not yet built))
- `coupon_redemptions`: code, affiliate_id, redeemed_at, flagged (coupon system (not yet connected))

## Rounds

| Round | Features picked | Date | Notes |
|---|---|---|---|
