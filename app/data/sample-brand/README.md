# Tallgrass Goods: the sample brand

Fictional US brand. Every file here except `brand.json` and this README is written by `app/data/generate.py` from `brand.json` and its seed. Do not edit the generated files by hand. Change `brand.json` or the generator, rerun, and commit.

```bash
python app/data/generate.py            # rewrite every table (about 4 seconds)
python app/data/generate.py --check    # rerun in memory and confirm the files on disk match, byte for byte
python app/data/tables.py orders       # load a table and print its shape
```

Window: 13 months, 2025-08-25 to 2026-09-24 (the `as_of` day in `brand.json`, 396 days). Every table carries `brand`, `source` and `captured_at` (2026-09-25T06:00:00Z). JSON files carry them in the header; CSV files carry them in `tables.json`, the manifest the server reads. The manifest is itself a table with one row per table. Load through `app/data/tables.py`, which returns typed rows for both formats.

## Tables

| Table | File | Rows | Shaped like | Real brand fills from |
|---|---|---|---|---|
| `products` | products.json | 40 | Shopify products plus a cost sheet: sku, title, type, price, cost, weight, stock, images | Shopify |
| `orders` | orders.json | 15,265 | Shopify orders: line items, subtotal, discount, shipping, tax lines by state, total, payment method, gateway, channel, utm, device, fulfilment, refund, return, chargeback, `rto` null | Shopify |
| `customers` | customers.csv | 10,499 | Shopify customers: first and last order, orders count, total spent, consents, state, segment | Shopify |
| `sessions` | sessions.csv | 41,683 | GA4 daily rows by source, medium, campaign, landing page, device with sessions, product views, add to carts, checkouts, purchases | GA4 |
| `inventory` | inventory.csv | 15,840 | stock by sku by day: on hand, sold, received, backordered, inbound | Shopify or 3PL |
| `purchase_orders` | purchase_orders.json | 196 | inbound POs: qty, ordered, expected, received, unit cost (companion to inventory) | 3PL |
| `ad_rows` | ad_rows.csv | 3,208 | Meta ad-level daily: campaign, ad set, ad, creative id, format, spend, impressions, reach, frequency, clicks, purchases, purchase value | Meta Ads (read) |
| `google_rows` | google_rows.csv | 8,712 | Google Ads daily by campaign and search term: impressions, clicks, cost, conversions, value | Google Ads (read) |
| `flows` | flows.json | 6,240 | Klaviyo flow messages by day: sends, delivered, opens, clicks, unsubscribes, matched order ids | Klaviyo |
| `campaign_sends` | campaign_sends.json | 108 | Klaviyo campaigns: segment, list size, sends, opens, clicks, unsubscribes, code, matched order ids | Klaviyo |
| `tickets` | tickets.json | 2,320 | Gorgias tickets: channel, reason, order id, first response, resolution, csat | Gorgias |
| `reviews` | reviews.json | 656 | site and Amazon reviews: sku, rating, title, text, author, verified, order id | Judge.me, Amazon |
| `reversed_orders` | reversed_orders.json | 1,007 | returns and chargebacks in one table with `legs` in the header: return 941, rto null, chargeback 66 | Shopify, gateway disputes |
| `payouts` | payouts.json | 200 | settlements: gross, fees, refunds, chargebacks, net, deposit date. Weekly for Shopify Payments, PayPal and Affirm, every 14 days for Amazon | Shopify Payments, PayPal, Affirm, Amazon |
| `content_posts` | content_posts.json | 170 | organic posts: platform, format, hook, views, saves, clicks, matched order ids | platform exports |
| `search_console` | search_console.csv | 1,260 | 90 queries by month (14 months): page, clicks, impressions, ctr, position. The contract asks for 200; the rest come as screens need them | Search Console |
| `marketplace_listings` | marketplace_listings.json | 15 | Amazon listing snapshot: asin, price, buy box share, stock, rating, reviews, units 30d, fees | Amazon Seller (read) |
| `speed_runs` | speed_runs.json | 237 | speed lab summaries: page, variant, run, fcp, lcp, load, cls, tbt, requests, bytes by party. A fixture, not measured | `speed_lab.measure` |
| `claims` | claims.json | 6 | claim text with tier: approved, site backed, forbidden | brand brain |
| `decisions` | decisions.json | 2 | seed examples only. The live log the server appends to is `app/data/decisions.json` | screens |
| `registry` | registry.json | 3 | experiments: hypothesis, metric, dates, status, result, learning | screens |
| `contract_status` | contract_status.json | 21 | table freshness plus a `metrics` list saying which contract metrics are available and which are not, with the reason | generate.py |

Total 24.6 MB. `orders.json` is 14.5 MB and `sessions.csv` 3.3 MB.

## What the numbers say

Whole window unless stated. All computed from the files, not typed in.

| Measure | Value |
|---|---|
| Sessions a day | about 1,575, 69 percent mobile |
| Paid orders a day | 38, so 15,265 in 13 months |
| Conversion (orders over sessions) | 2.4 percent |
| Net AOV | $94. `brand.json` targets $85; the $98 skillet leads sales, so it lands higher |
| Repeat share of orders | 30 percent |
| Revenue including tax and shipping | $1.53M |
| Meta spend and reported ROAS | $339k, 2.8. Meta reports 1.9 purchases for every order that carries a paid social utm, on purpose |
| MER (revenue over Meta plus Google spend) | 3.8 |
| Return rate on delivered orders | 6.4 percent |
| Chargeback rate on paid orders | 0.44 percent |
| Sales tax | collected in 15 nexus states. Orders to other states carry 0 tax by policy, not by a gap |

Seasonality: a month curve with a November and December peak, Black Friday at 3 times a normal day, Cyber Monday at 2.6, a drop after the 20 December shipping cutoff, Mother's Day and Father's Day weeks, a January dip. Weekdays are stronger than Saturdays. Volume grows 25 percent across the window and organic search grows 35 percent.

Money flows in one direction: Meta and Google clicks become paid sessions, flow and campaign clicks become email sessions, the funnel produces orders, and orders produce customers, stock movements, returns, chargebacks, tickets, reviews, payouts and the matched ids in flows, campaigns and posts.

## Planted stories

These are on purpose, so the first screens have something to find. Nothing else is staged.

1. **Mobile checkout broke on 2026-08-21.** Mobile checkout rate (checkouts over add to carts) fell from 0.47 to 0.39 while desktop held at 0.54. Orders a day fell with it. `speed_runs` shows why: from the week of 2026-08-17 the product page on mobile went from LCP 2.3 s to 3.9 s, 88 to 112 requests and 22 to 41 percent third-party bytes, with a fix chain measured on 2026-09-22 that brings it back. Screens: 00-today, 07, 08.
2. **The oldest Meta ad is tired.** Ad 120210000001001 ("Seasoned once, cooks for decades") has CTR down from 1.08 to 0.80 percent and CPA up from $54 to $81 at frequency 1.7. Ad 120210000001007 ("Skillet vs nonstick", launched 2026-07-27) runs at 1.9 percent CTR and $30 CPA. Two ads share creative `cr-9001`; two are dynamic and flagged. Screens: 09, 11.
3. **The 12-inch Skillet is short for Q4.** 266 on hand, 167 sold in the last 28 days, and the open PO is 21 days late with arrival on 2026-11-03. It already hit zero for 2 days in August. Gift sets stocked out for up to 14 days in Black Friday week last year. On Amazon the same skillet has lost the buy box to a reseller (share 0.42). Screens: 19, 20, 21.
4. **The Bread Board warps.** Since 2026-05-15 orders of `TG-WB-005` return at about 3 times the base rate with reason "warped or cracked", and its reviews since mid June average 3.4 stars against 4.3 sitewide, with quotable complaints. Screens: 15, 05, 01.

Smaller signals: USPS deliveries run 3 days late since 2026-09-11 and "where is my order" tickets doubled per day; one TikTok post on 2026-03-11 reached 1.24M views and organic social sessions spiked for 10 days.

## Rules the generator keeps

- Market-only fields exist and read null: `rto`, `cod_confirmed`, the `rto` leg. There is no cash on delivery.
- Missing is null, never 0: SMS opens, unreceived POs, open returns, csat not given.
- Meta-reported purchases are kept separate from order-matched ones. `flows`, `campaign_sends` and `content_posts` carry matched order ids from `orders`, not platform attribution.
- Every text a screen may quote (reviews, hooks, subjects, ticket reasons) is plain and fictional. Emails end in example.com. The site is tallgrassgoods.example.
- Determinism: one `random.Random` per table, seeded from `brand.json` seed plus the table name, so adding a table does not change the others. No sets are iterated, no clocks are read. `app/data/.gitattributes` pins LF so `--check` stays exact on Windows checkouts.
