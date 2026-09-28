# bombas: simulated data (generator v2)

Simulated data. Every row carries `simulated = 1`. Nothing here is a Bombas result. The shape follows the brain's
public profile (`app/brain/bombas/assumptions.json`); performance rates are placeholders listed in `manifest.json`.

Build: scale 1.0, seed 7, 2024-09-28 to 2026-09-27 (730 days, last full day in America/New_York).
Rebuild: `python3 app/data/generate.py --brand bombas --scale 1.0 --as-of 2026-09-27`.

`data.sqlite` is git-ignored (rebuilt from the seed). `aggregates/*.json`, `manifest.json`, `assumptions.json`, `tables.json` are committed.

## Calibration hit (last 12 months)

- Revenue: orders 455,301,492 plus wholesale fixture 45,029,818 = 500,331,310 USD; band x scale 450,000,000 to 550,000,000; in band: True
- AOV (net merchandise per order): 73.03 vs 73.0 target
- Repeat within 12 months: 0.3504 vs 0.35
- Seasonality (detrended month index): max gap 0.027
- Socks and slippers share of line revenue: 0.9299 vs 0.93

## Tables

| Table | Rows | Where | Source | Shaped like |
|---|---:|---|---|---|
| `orders` | 11,061,240 | data.sqlite | generator | Shopify Order + customerJourneySummary |
| `order_lines` | 15,712,074 | data.sqlite | generator | Shopify LineItem (nested in orders) |
| `customers` | 7,554,112 | data.sqlite | generator | Shopify Customer |
| `products` | 21 | data.sqlite | generator | Shopify ProductVariant + GA4 item report (28 days) |
| `inventory` | 30,660 | data.sqlite | generator | Shopify InventoryLevel, daily capture |
| `inbound_pos` | 249 | data.sqlite | fixture | fixture (not in the Shopify census) |
| `reversed_orders` | 716,202 | data.sqlite | generator | Shopify Return, Fulfillment, ShopifyPaymentsDispute |
| `payouts` | 730 | data.sqlite | generator | ShopifyPaymentsPayout |
| `abandoned_checkouts` | 8,242,547 | data.sqlite | generator | Shopify AbandonedCheckout |
| `sessions` | 285,214 | data.sqlite | generator | GA4 runReport |
| `ad_rows` | 22,791 | data.sqlite | generator | Meta Insights level=ad, time_increment=1 |
| `google_rows` | 14,600 | data.sqlite | generator | Google Ads GAQL campaign, search_term_view, asset_group |
| `flows` | 6,570 | data.sqlite | generator | Klaviyo Metric Aggregates by flow message |
| `campaign_sends` | 1,736 | data.sqlite | generator | Klaviyo Campaign + Metric Aggregates |
| `tickets` | 1,131,568 | data.sqlite | fixture | fixture (Gorgias shape) |
| `reviews` | 179,826 | data.sqlite | fixture | fixture (reviews app shape) |
| `speed_runs` | 18 | data.sqlite | fixture | fixture (speed lab) |
| `content_posts` | 120 | data.sqlite | fixture | fixture (platform exports) |
| `search_console` | 720 | data.sqlite | fixture | fixture (Search Console shape) |
| `marketplace_listings` | 0 | data.sqlite | fixture | fixture (Amazon Seller shape) |
| `wholesale_sell_in` | 124 | data.sqlite | fixture | fixture (no connector; brain wholesale share) |
| `aggregates/daily` | 730 | aggregates/daily.json | generator | rollup of the tables above |
| `aggregates/monthly` | 25 | aggregates/monthly.json | generator | rollup of the tables above |
| `aggregates/channels_monthly` | 200 | aggregates/channels_monthly.json | generator | rollup of the tables above |
| `aggregates/products_monthly` | 525 | aggregates/products_monthly.json | generator | rollup of the tables above |
| `aggregates/cohorts` | 25 | aggregates/cohorts.json | generator | rollup of the tables above |
| `aggregates/wholesale_monthly` | 124 | aggregates/wholesale_monthly.json | generator | rollup of the tables above |
| `aggregates/calibration` | 12 | aggregates/calibration.json | generator | rollup of the tables above |

## How the tables tie together

- Orders are the one truth. GA4 `sessions.transactions` = orders GA4 tracked (a fixed 93 percent of web orders); sessions are implied from them by placeholder conversion rates.
- Meta `ad_rows.purchases` = paid social orders credited on click (80 percent) plus 1d_view credit on 7 percent of direct, organic, email, SMS and other orders. Those view orders overlap Google and Klaviyo on purpose.
- Google `google_rows` campaign conversions = 88 percent of paid search orders plus brand search credit on 5 percent of organic and 4 percent of direct orders. Search term rows drop terms under 10 impressions, so they never sum to the campaign row.
- Klaviyo `flows` and `campaign_sends`: attributed orders = every email and SMS order plus overlap on direct, organic, paid social and paid search orders. `matched_order_ids` lists them and each id is in `orders`.
- `payouts`: Shopify Payments charges (PayPal excluded) paid 2 days later, less fees, refunds and dispute moves. `net = charges_gross - charges_fee + refunds_gross + adjustments_gross` (refunds and adjustments are signed).
- `reversed_orders`: each row is on an order. Returns refund one line with its tax; carrier returns refund the whole order and are excluded from return rate; chargebacks are Shopify Payments orders only. `rto` is null for a US brand and not written.
- `tickets`: most carry an order id; pre-sale tickets carry none. `reviews` are written from order lines, so every sku is in `products` and review counts follow units sold.
- `inventory` falls with units sold and rises with `inbound_pos` receipts. `wholesale_sell_in` is a fixture: the brain's wholesale share, split by the retail partners from their start year. It is not in `orders`.
- `marketplace_listings` has no rows: the brain's marketplace share is null, so the table reads unavailable. Amazon settlements are not written for the same reason.
- `finance_inputs` is not written here; it is S2.4 (`contracts/finance-inputs.md`).
- `orders.status` and `orders.payment_method` are filled by the generator; a live Shopify pull writes null until the census follow-up (data-sources.md).
- `orders.acquisition_channel` and `orders.units` are generator conveniences (not census fields); screens should derive channel from utm and units from lines for a real brand.
