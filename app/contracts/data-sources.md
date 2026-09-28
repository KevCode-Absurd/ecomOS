# Data sources and tables (v2, 28 Sep 2026)

The data layer is `app/data/`. For the sample brand (Bombas, simulated) every table is written by the generator, calibrated per `calibration.md`. For a real brand the same tables fill from read-only connectors in `app/connectors/`. Nothing in a screen changes between the two.

Each table below names its connector, the census fields it maps to (`connectors/<file>.md`), its grain, its window rules and its unavailable rule. A table no census supports is marked **fixture** with the reason. Brand-supplied numbers live in `finance_inputs`, defined in `finance-inputs.md`.

## Rules for every table

- Columns every table carries: `brand`, `captured_at` (connector pull) or `computed_at` (derived), `source` (connector name, `generator` or `fixture`), and `simulated` (true for the sample brand, shown on every page).
- Windows end on the last full day in the brand's timezone (US default: America/New_York). Window lengths are set in `metrics.md`. Each table states its history cap from the census; a day past the cap is unavailable.
- Missing shows as unavailable, never 0. A value is null when the connector cannot return it: scope or permission missing, past the history cap, platform not in use, breakdown rejected, row hidden by a privacy threshold. A 0 is written only when the platform reported 0.
- US brand by default. Market-only fields (cash on delivery, return to origin) exist, read null and stay hidden unless `brand.json` sets a market that uses them.
- Platform-reported and order-matched numbers are kept in separate columns and named as such. Totals are kept separate from breakdowns. Ratios are computed in code from totals.
- Fixture tables keep a frozen shape, are written by the generator with `source: fixture`, and show a "no connector yet" badge on screens. Adding a connector for one is a contract session plus a census file.

## Shopify (`connectors/f-shopify.md`)

Pull: bulk operation for history, then incremental by updated time. Orders older than 60 days need `read_all_orders`; without it, days past 60 are unavailable, not 0.

### `orders`
Grain: one row per order, line items nested. Window: full history with `read_all_orders`, else 60 days.
| Column | Census fields |
|---|---|
| id, created_at, customer_id, channel | Order.id, createdAt, customer, sourceName |
| lines: sku, qty, qty_current, unit_price, unit_price_discounted, line_total, line_discount, cost | LineItem.sku, quantity, currentQuantity, originalUnitPriceSet, discountedUnitPriceSet, discountedTotalSet, totalDiscountSet; LineItem.variant.inventoryItem.unitCost |
| discount, discount_codes | Order.discountApplications, discountCodes (sub-object fields are a census follow-up) |
| shipping, tax_lines (title, rate, amount, jurisdiction liable) | Order.shippingLine; Order.taxLines and currentTaxLines (TaxLine.title, rate, ratePercentage, priceSet, channelLiable) |
| total, total_current, refunds | Order.totalPriceSet, currentTotalPriceSet, refunds (Refund fields are a census follow-up) |
| utm (source, medium, campaign, content, term), landing_page, referrer, first_visit_at, last_visit_at, days_to_conversion, order_index | Order.customerJourneySummary: firstVisit, lastVisit, daysToConversion, customerOrderIndex, ready; CustomerVisit.occurredAt, source, sourceType, referrerUrl, landingPage, utmParameters |
| status, payment_method | not in the census field list. Follow-up census of Order status and OrderTransaction fields before build. Until then the connector writes null and `paid order` in `metrics.md` cannot be computed from a live pull. |
Unavailable: utm columns when `ready` is false (sessions still attaching); `cost` without the "View product costs" permission; any order past the 60-day cap without `read_all_orders`.

### `customers`
Grain: one row per customer, snapshot at `captured_at`. Lifetime fields are lifetime, never windowed; cohort metrics come from `orders`.
| Column | Census fields |
|---|---|
| id, orders_count, total_spent | Customer.id, numberOfOrders, amountSpent |
| first_order_at | computed from Customer.orders (earliest createdAt); unavailable without `read_all_orders` |
| email_consent, email_opt_in_level, email_consent_at, sms_consent | emailMarketingConsent (marketingState, marketingOptInLevel, consentUpdatedAt), smsMarketingConsent |
| state | not censused (address); null until a follow-up pass |

### `products`
Grain: one row per variant (sku), snapshot. GA4 item fields join on `itemId` = sku.
| Column | Census fields |
|---|---|
| sku, price, compare_at_price, stock, tracked | ProductVariant.sku, price, compareAtPrice, inventoryQuantity; InventoryItem.tracked |
| cost | InventoryItem.unitCost; overridden by `finance_inputs.cogs_landed` when present |
| views, adds, checkouts, purchased, item_revenue, cart_to_view, purchase_to_view | GA4 (`e-ga4.md`): itemId, itemName, itemCategory..itemCategory5, itemBrand, itemsViewed, itemsAddedToCart, itemsCheckedOut, itemsPurchased, itemRevenue, cartToViewRate, purchaseToViewRate |
| title, type, weight, images | not censused (Product object); follow-up pass |
Unavailable: `cost` without the product-costs permission; GA4 item columns when `checkCompatibility` rejects the pair or the row is thresholded.

### `inventory`
Grain: sku x location x day. Shopify has no stock history endpoint, so history accrues from daily captures.
Census: InventoryLevel.quantities (available, on_hand, incoming, committed), InventoryLevel.location, InventoryItem.tracked. Window: from the first capture forward; earlier days unavailable. Inbound purchase orders are not in the census: the `inbound_pos` part is **fixture**.

### `reversed_orders`
Three legs, kept as `type`: `return` (received and sent back), `rto` (never received, cash on delivery only, null for US), `chargeback` (disputes). Columns: order_id, type, reason, amount, opened_at, closed_at, outcome. Grain: one row per return, RTO parcel or dispute.
| Leg | Census fields |
|---|---|
| return | Return.status, returnLineItems, totalQuantity, refunds (amount), returnShippingFees, decline (outcome). Opened and closed timestamps are not in the census field list: follow-up. |
| return, reason `carrier_returned` | Fulfillment.displayStatus, events, trackingInfo. Feeds `return_to_sender_rate` only; excluded from `return_rate`. |
| rto | no source for a US brand; null. A market connector defines it later. |
| chargeback | ShopifyPaymentsDispute.amount, status (outcome), type (inquiry or chargeback), evidenceDueBy, evidenceSentOn, finalizedOn (closed_at), order. |
Window: follows `orders`. Unavailable: the chargeback leg for stores not on Shopify Payments; `rto` for US.

### `payouts`
Grain: one row per payout. Census: ShopifyPaymentsPayout.net, status, issuedAt, summary (fees and gross by transaction type), transactionType. Window: full history via bulk pull. Unavailable: stores not on Shopify Payments (other gateways have no data here). Amazon settlements are **fixture** until a marketplace census exists.

### `abandoned_checkouts`
Grain: one row per checkout not completed. Census: AbandonedCheckout.abandonedCheckoutUrl, lineItems, discountCodes, taxLines, totalPriceSet, customer. Window: follows `orders`. Unavailable: whole table when the merchant user lacks `manage_abandoned_checkouts`; `customer` null for app-created checkouts.

## GA4 (`connectors/e-ga4.md`)

### `sessions`
Grain: one row per date x source x medium x campaign x channel group x landing page x device x new-or-returning, from `runReport`. Rows are aggregates, not single sessions.
| Column | Census fields |
|---|---|
| date, source, medium, campaign, channel_group, landing_page, device, new_vs_returning | date, sessionSource, sessionMedium, sessionCampaignName, sessionDefaultChannelGroup, landingPage, deviceCategory, newVsReturning |
| sessions, engaged_sessions, users, new_users | sessions, engagedSessions, totalUsers, newUsers |
| product_view, add_to_cart, checkout, purchase, transactions, revenue | itemViewEvents, addToCarts, checkouts, ecommercePurchases, transactions, purchaseRevenue |
| sampled, thresholded, other_row_loss | ResponseMetaData: samplingMetadatas, subjectToThresholding, dataLossFromOtherRow |
Window: daily, no platform lookback cap for `runReport`; first pull 13 months, then daily. Data retention (2 or 14 months) bounds only funnel and exploration reports, which this table does not use.
Unavailable: a thresholded row; the `(other)` row at breakdown level (totals kept); a column whose pair `checkCompatibility` marks incompatible. A sampled response is kept and flagged; screens show the flag.
Note for `metrics.md`: GA4 returns event counts, not sessions with the event. Rates written as "sessions with X / sessions" read unavailable until the metric contract restates them as event-per-session rates or `sessionKeyEventRate`.

## Meta (`connectors/a-meta-marketing.md`)

### `ad_rows`
Grain: ad x day (`level=ad`, `time_increment=1`), with campaign and ad set ids. Ad-level rows are kept when ads share an image.
| Column | Census fields |
|---|---|
| date, campaign_id, adset_id, ad_id | date_start, campaign_id, adset_id, ad_id |
| spend, impressions, reach, clicks, link_clicks | spend, impressions, reach, clicks, inline_link_clicks |
| purchases, purchase_value, add_to_cart, initiate_checkout (each as default window, 7d_click, 1d_view) | actions and action_values by action_type `omni_purchase` (confirmed), `omni_add_to_cart`, `omni_initiate_checkout` (partially verified, re-check live); AdsActionStats value, 7d_click, 1d_view |
| video_p25 .. video_p100 | video_p25_watched_actions .. video_p100_watched_actions |
| creative_id, body, title, cta, image_hash, video_id, thumbnail_url, is_dynamic | Ad Creative: body, title, call_to_action_type, image_hash, video_id, thumbnail_url; `is_dynamic` true when asset_feed_spec is present (flag, never split into variations) |
Window: attribution default `7d_click` plus `1d_view`; `7d_view` and `28d_view` are not returned since 12 Jan 2026. History 37 months for totals; reach with breakdowns 13 months; frequency breakdowns 6 months. `frequency`, `cpm`, `cpc`, `ctr`, `purchase_roas` are not stored; `metrics.md` computes them from totals.
Unavailable: an ad-day with no row at all; reach past 13 months when a breakdown is on; a window Meta no longer returns. An action type absent from `actions` on a row that has spend and impressions is a platform zero and is written as 0.

## Google Ads (`connectors/c-google-ads.md`)

### `google_rows`
Two row kinds, never summed together: `campaign` (campaign x day) and `search_term` (search term x ad group x day). Performance Max campaigns have campaign rows only, plus `asset_group` rows for ad strength.
| Column | Census fields |
|---|---|
| date, campaign_id, campaign_name, campaign_status, channel_type, bidding | segments.date, campaign.id, name, status, advertising_channel_type, bidding_strategy_type |
| spend, impressions, clicks, conversions, conversion_value, all_conversions, all_conversion_value | metrics.cost_micros (divided by 1,000,000 in code), impressions, clicks, conversions, conversions_value, all_conversions, all_conversions_value |
| impression_share, top_is, abs_top_is, lost_is_budget, lost_is_rank | metrics.search_impression_share, search_top_impression_share, search_absolute_top_impression_share, search_budget_lost_impression_share, search_rank_lost_impression_share |
| search_term, term_status, ad_group_id, quality_score | search_term_view.search_term, status; ad_group id; ad_group_criterion.quality_info.quality_score |
| asset_group_id, ad_strength (PMax) | asset_group.id, name, ad_strength |
Window: daily segments 37 months back; older months by `segments.month` only. Conversions are by interaction date; the by-conversion-date variants are not stored in round 0. Removed entities are filtered out to match the UI.
Unavailable: search term rows hidden by the privacy threshold, so term rows never reconcile to the campaign row; impression share reported at the 0.0999 floor or the 0.9001 ceiling is stored null with a `clipped` flag; quality score when Google has too little data. A campaign-day absent because all metrics were zero is a platform zero only when the campaign was enabled that day; otherwise no row.

## Klaviyo (`connectors/g-klaviyo.md`)

Metric ids differ per account. At connect time the connector resolves the account's Placed Order, Received, Opened, Clicked, Unsubscribed and Bounced metrics by name from Get Metrics and stores the mapping. Attribution is the account's setting (default cooperative last touch, 5-day email click, 24-hour SMS) and is not readable through the API; rows carry `attribution: account_setting`.

### `flows`
Grain: flow message x day (Metric Aggregates, `interval: day`).
| Column | Census fields |
|---|---|
| flow_id, flow_name, flow_status, trigger_type, message_id, channel, subject | Flow id, name, status, trigger_type; Flow Message channel, definition.name, subject_line |
| sends, opens, clicks, unsubscribes, bounces | Metric Aggregate count by `$message` for the mapped metrics |
| attributed_revenue, attributed_orders (platform reported) | sum_value and count of Placed Order by `$attributed_flow` and `$attributed_message` |
| matched_order_ids | Placed Order Event event_properties filtered by `$attributed_message`; joined to `orders` for `revenue_by_flow_order_matched` |
Window: 1 year per query, paged by year; 1 extra filter per query. Unavailable: a channel the account does not use (no SMS metric); a `by` dimension the metric rejects, tested per metric at connect time.

### `campaign_sends`
Grain: campaign message x day from `send_time`. Census: Campaign id, name, status, send_time, send_strategy.type, audiences, send_options.use_smart_sending; Campaign Message definition (subject, body per channel). Metrics, windows and unavailable rules as `flows`, grouped by `$attributed_message` and `$attributed_channel`.

## Fixture tables (no census)

| Table | Shape kept | Reason it is fixture |
|---|---|---|
| `tickets` | id, created_at, channel, reason, order_id, first_response_min, resolved_min, csat | Gorgias census not scheduled |
| `reviews` | sku, rating, text, date, source | Judge.me and Amazon reviews census not scheduled |
| `speed_runs` | page, variant, run, load_ms, lcp_ms, fcp_ms, bytes, requests | internal lab (`speed_lab.measure`), not a connector; a real run replaces the fixture |
| `content_posts` | platform, date, format, hook, views, saves, clicks, matched_orders | platform exports, no API census |
| `search_console` | query, page, clicks, impressions, position | Search Console census not scheduled |
| `marketplace_listings` | marketplace, listing id, price, buy_box, stock, rating, reviews | Amazon Seller census not scheduled |
| `inbound_pos`, Amazon settlements | see `inventory` and `payouts` | not in the Shopify census |

## Written by the product, not a connector

- `finance_inputs`: brand-supplied costs, fees and targets with effective dates. Contract in `finance-inputs.md`.
- `claims`, `decisions`, `registry`, `contract_status`: brand brain and memory tables, written by screens, seeded with a few examples.
- Generation manifest for the sample brand: which brain fields calibrated each table and which fallbacks ran. Contract in `calibration.md`.

A screen that needs a table not here proposes it in a contract session. Census follow-ups named above (Order status, OrderTransaction, Refund, ShippingLine, Product fields, Return timestamps) are the next census pass.
