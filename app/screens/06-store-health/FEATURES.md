# Store health: features

Status: todo | doing | done | parked. One feature per commit. The first round is the skeleton; after that, features come in rounds of 10, stack-ranked by revenue impact, usefulness and how easy they are to build on dummy data.

## Round 0: skeleton

| # | Feature | Status |
|---|---|---|
| 0.1 | Page shell in the shared UI kit: header, empty-state tiles, insight list, action buttons | todo |
| 0.2 | `api.py` serving this screen's metrics from `app/data/` with unavailable states | todo |
| 0.3 | 3 metric tiles, 2 insights, 1 chart from the sample brand | todo |

## Candidates from the room spec (pick 10 per round)

### Questions this screen should answer

- is the account, staff access and 2FA set up the way it should be  (SITE-C02)
- does every payment method actually complete a real order  (SITE-C09)
- which apps are we paying for and running that earn nothing back  (SITE-C13)
- is every launch step actually verified, not just checked off  (SITE-C14)
- what quietly broke since the last time someone looked  (SITE-C15)
- is checkout fast, safe and free of settings that cost sales  (SITE-C18)
- which of these findings are not actually a site problem  (ORCH-C03)
- can a keyboard or screen-reader shopper actually buy something here  (SITE-C59)
- can search and AI answer engines actually read our product pages  (ORG-C23)
- did the last change break browsing, cart or a discount code  (SITE-C64)
- is the store up and can someone actually complete an order right now  (SITE-C65)
- which orders are likely to fail delivery or come back as a chargeback before we ship or settle them  (SITE-C67)
- which COD orders are likely to bounce back before we ship them  (SITE-C67)
- is what we are testing on staging actually what is live  (SITE-C70)
- do our tracking scripts actually wait for consent, not just show a banner  (SITE-C78)

### Metrics specified

- `launch_checklist_completion_pct`: how much of the launch checklist is done and verified. items marked verified (not just checked) divided by total checklist items
- `uptime_pct_30d`: how often the store was reachable over the last 30 days. successful synthetic checks divided by total checks, rolling 30 days
- `checkout_transaction_success_rate`: how often a real end-to-end test order completes. successful synthetic checkout completions divided by attempts, across the store's active payment methods
- `payment_method_coverage`: how many of the planned payment methods actually work. payment methods that pass a live go-live test divided by payment methods the brand intended to offer
- `app_count_no_revenue_link`: how many installed apps have no sales tied back to them. count of active apps where revenue_attributed is null or zero over the last 90 days
- `script_count_key_pages`: how many third-party scripts load on the home, PDP, cart and checkout pages. count of distinct third-party script hosts across those 4 templates
- `residual_code_after_uninstall_count`: how many leftover snippets remain from apps that were removed. count of theme code blocks or script tags referencing an app no longer in the active app list
- `accessibility_critical_issue_count`: how many serious accessibility problems the automated scan found. count of WCAG 2.1 A and AA violations flagged critical or serious, across home, PDP, collection, cart and checkout templates
- `accessibility_manual_flag_count`: how many issues only a real keyboard or screen-reader test found. count of findings logged during a manual pass on dynamic elements (variant picker, cart drawer, filters)
- `structured_data_coverage_pct`: how many eligible pages carry valid structured data. pages with at least one valid schema block (Product, Offer, Review, BreadcrumbList or FAQPage) divided by pages eligible for that schema type
- `structured_data_error_count`: how many schema blocks exist but have errors. count of schema blocks failing validation
- `address_validation_coverage_pct`: how much of the brand's order footprint has a working USPS address validation check. orders validated against USPS before checkout divided by all orders in the window
- `cod_pincode_coverage_pct`: India market option, reads null for US: how much of the brand's order footprint has a working COD serviceability check. orders from pincodes with a serviceability rule configured divided by all orders in the window
- `order_confirmation_rate`: how many orders get an SMS or email confirmation before dispatch. orders with a recorded confirmation event divided by total orders
- `cod_confirmation_rate`: India market option, reads null for US: how many COD orders get an OTP or WhatsApp confirmation before dispatch. COD orders with a recorded confirmation event divided by total COD orders
- `payment_method_mix_pct`: what share of orders use each payment method (card, Shop Pay, PayPal, Apple Pay, a BNPL option such as Affirm, Klarna or Afterpay). orders per payment method divided by total orders, in the window; where the brand offers COD in India, cod_share_pct is the same breakdown's India-only line item
- `cod_share_pct`: India market option, reads null for US: what share of orders are placed cash on delivery. COD orders divided by total orders, in the window
- `chargeback_rate`: what share of paid orders get reversed through the card network. chargebacks divided by total paid orders, in the window
- `dispute_rate`: what share of paid orders get reversed through PayPal or a similar wallet dispute process. wallet disputes divided by total paid orders, in the window
- `return_to_sender_rate`: what share of orders come back as an undelivered carrier return (refused, unreachable, failed delivery). orders marked return-to-sender by the carrier divided by total orders, in the window
- `rto_rate_pct`: India market option, reads null for US: what share of COD orders come back undelivered. COD orders marked returned-to-origin divided by total COD orders, in the window
- `broken_link_count`: how many dead links or redirect loops the last sweep found. count of URLs returning a 404 or a redirect loop from an internal link or sitemap crawl
- `inventory_reconciliation_variance_pct`: how far the store's stock count drifts from the real count. absolute difference between store-recorded stock and a physical or warehouse count, divided by warehouse count, averaged across checked SKUs
- `staging_drift_days`: how long since staging last matched production. today minus the last successful staging sync date
- `consent_gate_pass_rate`: how often a tracking script actually waits for consent before firing. test page loads where the tagged scripts fired only after a recorded consent event, divided by total test loads, per region
- `regression_test_pass_rate`: how often the automated flow tests pass after a change. passed scripted flows (browse, cart, discount, checkout) divided by total flows run, for the latest change
- `release_notes_backlog_count`: how many platform updates or deprecations have not been reviewed yet. count of release-note items logged as unreviewed, across the platform, installed apps and API versions

### Insights specified (rules in code)

- checklist item done but not verified: a launch checklist item is marked done but its own verification step (the action a real customer would take) has not been logged as passed → "{item} is marked done but was never actually tested the way a customer would use it" (action SITE-C14)
- app with no revenue link: app_count_no_revenue_link includes an app with a real monthly cost → "{app} costs {inr} a month and nothing in your sales data ties back to it" (action SITE-C13)
- leftover code after an uninstall: residual_code_after_uninstall_count is over 0 → "{app} was removed but its code is still loading on {n} pages" (action SITE-C13)
- uptime or checkout incident: a synthetic check fails 2 checks in a row on any monitored endpoint → "{endpoint} failed {n} checks in a row starting at {time}, likely {suspected_cause}" (action SITE-C65)
- repeated accessibility violation across templates: the same WCAG rule fails on 3 or more of the 5 checked templates → "{rule} fails on {n} of your 5 key templates, most often {example}" (action SITE-C59)
- missing alt text above threshold: over 10 percent of product images on a template have no alt text → "{pct}% of images on {template} have no alt text" (action SITE-C59)
- structured data errors block rich results: structured_data_error_count is over 0 on a PDP template → "{n} PDP pages have a broken {schema_type} block and cannot show rich results" (action ORG-C23)
- chargeback or return-to-sender rate above the brand's own baseline: chargeback_rate or return_to_sender_rate for the last 30 days is more than 20 percent above the brand's trailing 90-day average → "chargebacks or failed deliveries are running at {pct}%, up from your usual {baseline}%" (action SITE-C67)
- India market option, reads null for US: RTO rate above the brand's own baseline: rto_rate_pct for the last 30 days is more than 20 percent above the brand's trailing 90-day average → "COD returns are running at {pct}%, up from your usual {baseline}%" (action SITE-C67)
- India market option, reads null for US: unconfirmed COD with high RTO: a pincode cluster has cod_confirmation_rate under 50 percent and rto_rate_pct over double the brand average → "{cluster} has almost no COD confirmation and returns {x} times more often than average" (action SITE-C67)
- staging out of sync: staging_drift_days is over 30 → "staging has not matched production in {n} days; a change tested there is not safe to trust" (action SITE-C70)
- consent gate not actually blocking a script: consent_gate_pass_rate for a named script is under 100 percent → "{script} fires before consent is given on {pct}% of test loads" (action SITE-C78)
- broken link or redirect loop: broken_link_count is over 0 on a page linked from navigation or a sitemap → "{n} links are broken, including {example} linked from your main menu" (action SITE-C15)
- inventory mismatch: inventory_reconciliation_variance_pct is over 2 percent for a SKU → "{sku} shows {store_count} in the store but {warehouse_count} in the warehouse" (action SITE-C15)
- unreviewed platform update past its deadline: a release-note item's own sunset or deprecation date has passed and it is still marked unreviewed → "{item} was deprecated on {date} and has not been reviewed yet" (action SITE-C68)
- new regression after a change: regression_test_pass_rate is under 100 percent on the run right after a theme or app change → "{flow} broke after the latest {change_type} change" (action SITE-C64)

### Visuals specified

- launch checklist tree (checklist with pass/fail per item): every launch item, whether it is done and whether it is verified
- uptime and incident timeline (timeline with incident markers): uptime and checkout success over the last 30 days with incidents marked and their duration
- app and script inventory table (sortable table, color-coded): every app with cost, weight and revenue link, red flagged when it has none
- accessibility issue heatmap (table heatmap, templates by rule): which WCAG rule fails on which template
- structured data coverage bar (stacked bar by page type): share of eligible pages with valid, invalid or missing structured data, per page type
- failed-delivery and chargeback funnel by ZIP code tier (funnel or stacked bar): orders placed, confirmed, delivered, and lost to a failed delivery or a chargeback, split by ZIP code tier
- India market option, reads null for US: RTO funnel by pincode tier (funnel or stacked bar): COD orders placed, confirmed, delivered and returned to origin, split by pincode tier
- staging drift indicator (single stat with a trend line): days since staging last matched production, over time

### Not in the usual tools

- checks a real transaction path end to end (add to cart through payment) from several regions, not just whether the homepage returns a 200
- ties every accessibility violation to the template it repeats on and routes it straight to a developer brief
- tracks structured data coverage as one rolling percentage across every eligible page type, not one URL at a time
- reads the failed-delivery and chargeback outcome back against the brand's own delivered-order history to say which checkout control actually reduced losses (India market option: which COD control actually reduced RTO)
- cross-references every installed app against the brand's own revenue attribution before calling it dead weight
- verifies each pre-launch checklist item with the action a real customer would take, not a box someone ticks from memory

### Data this screen needs

- `launch_checklist`: item, capability, status, verified_by_action, verified_at (SITE-C14 launch sequencing)
- `app_inventory`: app_id, name, monthly_cost, revenue_attributed, script_bytes, install_date, owner (SITE-C13 app audit (manual entry until a platform API is connected), shared with Site and speed)
- `uptime_checks`: endpoint, region, timestamp, status, latency_ms (SITE-C65 synthetic monitor)
- `checkout_synthetic_tests`: timestamp, gateway, region, result, error_detail (SITE-C65 synthetic transaction monitor)
- `accessibility_scan`: template, rule, wcag_criterion, severity, element, status, scanned_at (SITE-C59 automated plus manual scan)
- `structured_data_audit`: page_id, page_type, schema_type, valid, errors, crawled_at (SITE-C60 schema audit)
- `checkout_orders`: order_id, payment_method, zip_code, address_validated, fraud_flag, confirmed_channel, confirmed_at, delivered, chargeback, dispute (checkout payment and carrier data, SITE-C67)
- `cod_orders`: order_id, pincode, pincode_tier, confirmed_channel, confirmed_at, delivered, rto, order_date (order and logistics data, SITE-C67; India market option, reads null for US)
- `staging_sync_log`: last_synced_at, drift_days, diff_summary (SITE-C70 staging sync)
- `consent_test_log`: script_name, region, fired_before_consent, tested_at (SITE-C78 consent test)
- `regression_test_runs`: run_id, trigger, flow, pass, diff_pct, run_at (SITE-C64 regression suite)
- `release_notes_feed`: platform, item, date, sunset_date, reviewed, action_needed (SITE-C68 release tracking)

## Rounds

| Round | Features picked | Date | Notes |
|---|---|---|---|
