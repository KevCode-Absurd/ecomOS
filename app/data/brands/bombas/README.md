# bombas: simulated data (generator v2)

Simulated data. Every row carries `simulated = 1`. Nothing here is a Bombas result. The shape follows the brain's
public profile (`app/brain/bombas/assumptions.json`); performance rates are placeholders listed in `manifest.json`.

Build: scale 1.0, seed 7, 2024-09-28 to 2026-09-27 (730 days, last full day in America/New_York).
Rebuild: `python3 app/data/generate.py --brand bombas --scale 1.0 --as-of 2026-09-27`.

`data.sqlite` is git-ignored (rebuilt from the seed). `aggregates/*.json`, `manifest.json`, `assumptions.json`, `tables.json` are committed.

## Calibration hit (last 12 months)

- Revenue: orders 366,638,931 plus wholesale fixture 54,995,840 plus marketplace fixture 36,663,893 = 458,298,664 USD against the point 457,000,000 (+0.28 percent); band x scale 450,000,000 to 550,000,000; in band: True
- Sales channel mix, percent of revenue (generated vs brain): dtc site 73.5 vs 74.0, wholesale 12.0 vs 12.0, owned retail 6.5 vs 6.0, marketplaces 8.0 vs 8.0; largest gap 0.5 points
- Paid split, percent of paid spend (generated vs brain): meta 60.0 vs 60.0, google 20.0 vs 20.0, youtube creator 8.0 vs 8.0, tiktok 6.0 vs 6.0, pinterest 3.0 vs 3.0, other 3.0 vs 3.0; largest gap 0.01 points
- AOV (net merchandise per order): 73.01 vs 73.0 target
- Repeat within 12 months: 0.3493 vs 0.35
- Seasonality (detrended month index): max gap 0.075
- Socks, slippers and footwear share of line revenue: 0.93 vs 0.93
- GA4 sessions per month: 14,999,350 vs 15,000,000 assumed; conversion on web orders 2.6 percent
- Finance join: 25 of 25 products carry a cogs_landed key

## Tables

| Table | Rows | Where | Source | Shaped like |
|---|---:|---|---|---|
| `orders` | 8,801,664 | data.sqlite | generator | Shopify Order + customerJourneySummary |
| `order_lines` | 11,764,753 | data.sqlite | generator | Shopify LineItem (nested in orders) |
| `customers` | 5,819,036 | data.sqlite | generator | Shopify Customer |
| `products` | 25 | data.sqlite | generator | Shopify ProductVariant + GA4 item report (28 days) |
| `inventory` | 36,500 | data.sqlite | generator | Shopify InventoryLevel, daily capture |
| `inbound_pos` | 291 | data.sqlite | fixture | fixture (not in the Shopify census) |
| `reversed_orders` | 533,323 | data.sqlite | generator | Shopify Return, Fulfillment, ShopifyPaymentsDispute |
| `payouts` | 730 | data.sqlite | generator | ShopifyPaymentsPayout |
| `abandoned_checkouts` | 16,842,382 | data.sqlite | generator | Shopify AbandonedCheckout |
| `sessions` | 278,582 | data.sqlite | generator | GA4 runReport |
| `ad_rows` | 22,791 | data.sqlite | generator | Meta Insights level=ad, time_increment=1 |
| `google_rows` | 14,600 | data.sqlite | generator | Google Ads GAQL campaign, search_term_view, asset_group |
| `flows` | 6,570 | data.sqlite | generator | Klaviyo Metric Aggregates by flow message |
| `campaign_sends` | 1,736 | data.sqlite | generator | Klaviyo Campaign + Metric Aggregates |
| `tickets` | 472,982 | data.sqlite | fixture | fixture (Gorgias shape) |
| `reviews` | 135,163 | data.sqlite | fixture | fixture (reviews app shape) |
| `speed_runs` | 18 | data.sqlite | fixture | fixture (speed lab) |
| `content_posts` | 120 | data.sqlite | fixture | fixture (platform exports) |
| `search_console` | 720 | data.sqlite | fixture | fixture (Search Console shape) |
| `marketplace_listings` | 0 | data.sqlite | fixture | fixture (Amazon Seller shape) |
| `wholesale_sell_in` | 124 | data.sqlite | fixture | fixture (no connector; brain wholesale share) |
| `marketplace_sales` | 50 | data.sqlite | fixture | fixture (no connector; brain marketplace share, Amazon and TikTok Shop) |
| `paid_other_spend` | 2,920 | data.sqlite | fixture | fixture (no connector; YouTube creators, TikTok, Pinterest, other at the brain's paid split) |
| `aggregates/daily` | 730 | aggregates/daily.json | generator | rollup of the tables above |
| `aggregates/monthly` | 25 | aggregates/monthly.json | generator | rollup of the tables above |
| `aggregates/channels_monthly` | 186 | aggregates/channels_monthly.json | generator | rollup of the tables above |
| `aggregates/products_monthly` | 625 | aggregates/products_monthly.json | generator | rollup of the tables above |
| `aggregates/cohorts` | 25 | aggregates/cohorts.json | generator | rollup of the tables above |
| `aggregates/wholesale_monthly` | 124 | aggregates/wholesale_monthly.json | generator | rollup of the tables above |
| `aggregates/marketplace_monthly` | 50 | aggregates/marketplace_monthly.json | generator | rollup of the tables above |
| `aggregates/paid_media_monthly` | 150 | aggregates/paid_media_monthly.json | generator | rollup of the tables above |
| `aggregates/calibration` | 16 | aggregates/calibration.json | generator | rollup of the tables above |

## How the tables tie together

- Orders are the one truth. GA4 `sessions.transactions` = orders GA4 tracked (a daily share between 91 and 95 percent of web orders); sessions are implied from them by the placeholder conversion rates, scaled by one factor so sessions average the assumed `site_sessions_monthly`.
- Meta `ad_rows.purchases` = paid social orders credited on click (80 percent) plus 1d_view credit on 7 percent of direct, organic, email, SMS and other orders. Those view orders overlap Google and Klaviyo on purpose.
- Google `google_rows` campaign conversions = 88 percent of paid search orders plus brand search credit on 5 percent of organic and 4 percent of direct orders. Search term rows drop terms under 10 impressions, so they never sum to the campaign row.
- Klaviyo `flows` and `campaign_sends`: attributed orders = every email and SMS order plus overlap on direct, organic, paid social and paid search orders. `matched_order_ids` lists them and each id is in `orders`.
- `payouts`: Shopify Payments charges (PayPal excluded) paid 2 days later, less fees, refunds and dispute moves. `net = charges_gross - charges_fee + refunds_gross + adjustments_gross` (refunds and adjustments are signed).
- `reversed_orders`: each row is on an order. Returns refund one line with its tax; carrier returns refund the whole order and are excluded from return rate; chargebacks are Shopify Payments orders only. `rto` is null for a US brand and not written.
- `tickets`: most carry an order id; pre-sale tickets carry none. `reviews` are written from order lines, so every sku is in `products` and review counts follow units sold.
- `tickets` per order equal `ticket_rate` (5 percent, 8 percent for December orders): order tickets, the 30 percent of returns that open a ticket, and pre-sale questions together.
- `inventory` falls with units sold and rises with `inbound_pos` receipts. `wholesale_sell_in` is a fixture: the brain's wholesale share of revenue on its own month curve (high in Aug to Oct, low in Dec and Jan), split by the retail partners from their start year; new partners ramp 25, 50, then 100 percent by quarter and DSW is capped at 25 percent of wholesale in its first year. It is not in `orders`.
- `marketplace_sales` is a fixture: the brain's marketplace share of revenue by month, split Amazon 80 and TikTok Shop 20 (assumed). It is not in `orders`. `marketplace_listings` has no rows: there is no listing detail, so it reads unavailable.
- `paid_other_spend` is a fixture: daily spend for YouTube creators, TikTok, Pinterest and other at the brain's paid split. Meta and Google spend come from `ad_rows` and `google_rows`; Google CPAs carry one scale so Meta to Google lands on the split.
- `orders` and `channels_monthly` carry no POS before the first store opened (2025-11-01); `monthly.pos_orders` and `daily.pos_orders` read null there, not 0.
- `products.sku` and `order_lines.sku` use the finance keys (`BMB-...`), so `finance_inputs.cogs_landed` joins by sku. `finance_inputs` is not written here; it is S2.4 (`contracts/finance-inputs.md`). Its rows start 2025-01-01, so margin before then reads unavailable.
- `orders.status` and `orders.payment_method` are filled by the generator; a live Shopify pull writes null until the census follow-up (data-sources.md).
- `orders.acquisition_channel` and `orders.units` are generator conveniences (not census fields); screens should derive channel from utm and units from lines for a real brand.
