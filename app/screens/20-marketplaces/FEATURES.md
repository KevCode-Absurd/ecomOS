# Marketplaces and quick commerce: features

Status: todo | doing | done | parked. One feature per commit. The first round is the skeleton; after that, features come in rounds of 10, stack-ranked by revenue impact, usefulness and how easy they are to build on dummy data.

## Round 0: skeleton

| # | Feature | Status |
|---|---|---|
| 0.1 | Page shell in the shared UI kit: header, empty-state tiles, insight list, action buttons | todo |
| 0.2 | `api.py` serving this screen's metrics from `app/data/` with unavailable states | todo |
| 0.3 | 3 metric tiles, 2 insights, 1 chart from the sample brand | todo |

## Candidates from the room spec (pick 10 per round)

### Questions this screen should answer

- which listings are broken, missing attributes or out of spec right now  (PROD-C63, PROD-C64)
- who holds the Buy Box, and is anyone underselling my price  (PROD-C46)
- is my account health at risk of a suspension  (PROD-C38)
- is the feed the ad teams pull from current and clean  (PROD-C47)
- what is this platform's ad spend really returning  (PROD-C49)
- did each platform actually pay me what my orders say I'm owed  (ORCH-C03)
- which dark stores are about to go out of stock and hurt my ranking  (PROD-C51)
- am I using platform ad credits before they expire, and what's the peak retail calendar asking for (india: the festive calendar)  (PROD-C50)
- where is this onboarding stuck, and what document is missing  (PROD-C48)
- is this listing legally clear to publish  (PROD-C45)
- is my listing structured so the target keywords actually rank  (PROD-C34)
- am I about to breach a storage limit or run out of FBA stock  (PROD-C39)
- did sales drop because of traffic or because of conversion  (PROD-C40)
- which of my other marketplace listings have gone stale  (PROD-C44)

### Metrics specified

- `listing_health_score`: Share of live listings passing the channel's own content rules. listings with no open image, attribute or content error ÷ total live listings, per channel
- `image_video_spec_pass_rate`: Share of product images and videos meeting each channel's size and crop rules. assets passing the channel's own spec check ÷ total assets checked, per channel
- `buy_box_win_rate`: Share of time this brand holds the Buy Box on its own listings. time-weighted share of Buy Box ownership by the brand's own seller account ÷ total tracked time, per SKU
- `reseller_price_variance`: How far an unauthorised reseller's price sits below MAP. (MAP price − lowest tracked reseller price) ÷ MAP price, per SKU
- `account_health_score`: How close the seller account is to a policy or performance suspension risk. channel's own account health metrics (order defect rate, policy strikes, late shipment rate) rolled into a single risk flag against the channel's stated suspension thresholds
- `review_rating_avg`: Average star rating per SKU per channel. mean of star ratings on live reviews, per SKU per channel
- `catalogue_feed_freshness_hours`: How long since the shared catalogue feed last synced. now − last successful feed sync timestamp
- `rapid_delivery_reported_roas`: The ROAS the rapid-delivery platform's own dashboard shows. platform-reported ad revenue ÷ platform-reported ad spend, as the platform calculates it (often on list/MRP price)
- `rapid_delivery_true_roas`: ROAS recalculated from actual transaction value, not list/MRP price. sum of actual transaction value on attributed orders ÷ ad spend, using the real selling price after platform discount
- `settlement_variance_amount`: Difference between what a marketplace should pay out and what it actually paid. sum of expected settlement value from order records − actual amount received, per platform per period
- `dark_store_fill_rate_pct`: Share of dark stores carrying this SKU in stock right now. dark stores with stock greater than zero for the SKU ÷ total dark stores expected to carry it
- `ad_credit_utilization_pct`: Share of a platform's ad credit used before it expires. ad credit spent ÷ ad credit granted, for the current credit cycle
- `amazon_ipi_score`: Amazon's Inventory Performance Index score. value as reported by Amazon Seller Central
- `amazon_replenishment_alert_count`: How many FBA SKUs are below their recommended replenishment level. count of SKUs where FBA sellable stock is below the recommended reorder trigger from cover targets
- `sales_change_attribution`: Whether an Amazon sales change is a traffic problem or a conversion problem. split of the sales change into the portion explained by session/impression change versus the portion explained by conversion rate change, holding the other constant
- `listing_staleness_days`: Days since a Walmart, Target Plus, eBay or TikTok Shop listing was last updated (india: Flipkart, Myntra or Nykaa). today − last_updated_at, per listing
- `us_labeling_compliance_status`: Whether a regulated SKU's FTC quality-mark, Care Labeling or Prop 65 documentation is on file and current (india: BIS, hallmarking or labelling). flag from the compliance docs table: required doc types present and not expired

### Insights specified (rules in code)

- listing failing channel spec: listing_health_score for a channel drops below 95%, or any single listing has an open image or attribute error → "{n} listings on {channel} fail a content or image rule right now. Fix before the next sync." (action PROD-C63)
- Buy Box lost on an advertised SKU: buy_box_win_rate falls below 80% for a SKU that is currently running ads → "{sku} is only winning the Buy Box {pct}% of the time while ads are live. Ad spend is funding someone else's sale." (action PROD-C46)
- MAP violation detected: reseller_price_variance shows a tracked reseller price more than 10% below MAP → "A reseller is selling {sku} {pct}% below MAP. Flag it before it drags down price perception everywhere." (action PROD-C46)
- account health approaching suspension risk: account_health_score crosses the channel's own stated warning threshold → "{channel} account health has crossed its warning line. Address it before it becomes a suspension." (action PROD-C38)
- true ROAS far below what the dashboard shows: rapid_delivery_reported_roas exceeds rapid_delivery_true_roas by more than 20% → "{platform} shows {reported}x ROAS, but the real number on transaction value is {true}x. Do not scale spend on the reported figure." (action PROD-C49)
- settlement shortfall: settlement_variance_amount is nonzero and beyond a small rounding tolerance for a closed cycle → "{platform} paid {amount} less than the order records show for {period}. Send to Finance to dispute." (action ORCH-C03)
- dark store stockout risk: dark_store_fill_rate_pct for a hero SKU falls below 70% for 2 consecutive days → "{sku} is out of stock in {pct}% of its dark stores for {n} days running. Expect a ranking penalty." (action PROD-C51)
- ad credit going unused: ad_credit_utilization_pct is below 50% with fewer than 10 days left in the credit cycle → "{platform} ad credit is {pct}% used with {days} days left in the cycle. Spend it or lose it." (action PROD-C50)
- IPI score risking storage limits: amazon_ipi_score falls below Amazon's published storage-limit threshold → "Amazon IPI score is {score}, below the storage-limit line. Storage capacity may be restricted." (action PROD-C39)
- sales drop is a conversion problem, not traffic: sales_change_attribution shows over 70% of a sales drop explained by conversion rate, with traffic flat or up → "Sales fell {pct}%, but traffic held steady. The problem is on the listing or price, not visibility." (action PROD-C40)
- stale marketplace listing: listing_staleness_days exceeds 90 for a listing on Walmart, Target Plus, eBay or TikTok Shop (india: Flipkart, Myntra or Nykaa) → "{sku} on {channel} has not been updated in {days} days. Review it against current competitor listings." (action PROD-C44)
- compliance document missing before go-live: us_labeling_compliance_status is unavailable or expired for a SKU category that requires it, and the listing is live or scheduled → "{sku} needs a current FTC quality-mark or Care Labeling document before it can stay live (india: a BIS or hallmarking document). It is missing or expired." (action PROD-C45)
- catalogue feed gone stale: catalogue_feed_freshness_hours exceeds 24 while ads or listings depend on it → "The shared catalogue feed has not synced in {hours} hours. Ads and listings may be running on old data." (action PROD-C47)

### Visuals specified

- Buy Box ownership timeline (stacked area chart): share of time the Buy Box is held by the brand versus each tracked reseller, over the trailing 30 days
- true versus reported ROAS bars (grouped bar chart): rapid_delivery_reported_roas next to rapid_delivery_true_roas, per platform per period
- listing health scorecard grid (matrix grid): each channel down the side, each check (image, attribute, price match) across the top, colour-coded pass or fail
- dark store fill rate map (heat map): fill rate by store or region for each hero SKU
- account health gauge (gauge chart): each channel's account health score against its own warning and suspension thresholds
- settlement reconciliation waterfall (waterfall chart): expected settlement value stepping down through platform commission, fees and deductions to the amount actually received

### Not in the usual tools

- recomputes rapid-delivery ROAS from real transaction value instead of list/MRP price, and shows the gap against the platform's own reported number
- watches Buy Box, reviews, listing health and account risk together across Amazon, Walmart, Target Plus, eBay and TikTok Shop in one room (india: Flipkart, Myntra, Nykaa, Blinkit and Zepto)
- reconciles marketplace settlement payouts against order records automatically and routes a shortfall to Finance
- keeps one clean catalogue feed that Media buyer and Organic both pull from, with a staleness check
- splits an Amazon sales change into traffic versus conversion before anyone calls a product a failure

### Data this screen needs

- `marketplace_listings`: channel, sku, listing_id, status, image_pass, attribute_pass, last_updated_at (per-channel seller portal export or API)
- `buybox_snapshots`: channel, sku, seller, price, is_buybox_winner, captured_at (Buy Box tracking script or connector)
- `reviews`: channel, sku, rating, review_text, review_date (per-channel review export)
- `account_health_metrics`: channel, metric_name, value, threshold, as_of_date (per-channel account health export)
- `catalogue_feed`: sku, title, price, image_url, availability, gtin, synced_at (catalogue feed build script)
- `rapid_delivery_orders`: platform, sku, list_price, transaction_value, ad_spend_attributed, order_date (platform order and ad export)
- `settlement_reports`: platform, period, expected_amount, paid_amount, deduction_breakdown (platform settlement file reconciliation script)
- `dark_store_inventory`: platform, store_id, sku, stock_level, fill_rate, as_of (platform dark-store inventory feed)
- `ad_credit_ledger`: platform, cycle_start, cycle_end, credit_granted, credit_used (platform ad account export)
- `amazon_inventory`: sku, ipi_score, sellable_units, storage_limit_flag, as_of_date (Amazon Seller Central inventory export)
- `amazon_traffic_sales`: sku, sessions, conversion_rate, units_ordered, date (Amazon Business Reports export)
- `compliance_docs`: sku, doc_type, status, issued_date, expiry_date (manual entry plus compliance tracking script)

## Rounds

| Round | Features picked | Date | Notes |
|---|---|---|---|
