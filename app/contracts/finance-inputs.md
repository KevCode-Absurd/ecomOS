# Finance inputs (brand-supplied numbers)

The platforms do not know what a brand pays for goods, boxes, labels, fees or people. The brand supplies those through a form or a sheet into one table, `finance_inputs`. Every row has an effective date range, so gross profit, contribution margin and runway can be computed for any window. This is the contract for that table and for the metrics it unlocks. Source: `PRODUCT-PLAN.md` section 4.3.

## Shape of a row

| Column | Meaning |
|---|---|
| field | one of the field ids below |
| scope | what the value applies to: `sku`, `carrier_zone`, `channel`, `marketplace`, `vendor`, `global` |
| scope_key | the sku, the carrier plus zone band, the channel name, the marketplace, the vendor name; empty for global |
| value, unit | the number and its unit: `usd`, `usd_per_order`, `usd_per_unit`, `usd_per_return`, `usd_per_month`, `percent`, `weeks` |
| effective_from, effective_to | dates; `effective_to` empty means still in force. Ranges for the same field and scope key must not overlap. |
| entered_by, entered_at, note | who, when, and a plain note (invoice, contract, estimate) |
| confidence | `invoice` (from a bill), `estimate` (founder's number), `simulated` (sample brand) |

## Fields

| Field | Scope | Unit | What it is |
|---|---|---|---|
| cogs_landed | sku | usd_per_unit | cost of one unit delivered to the warehouse: goods, freight, duty. Overrides Shopify `InventoryItem.unitCost` when both exist. |
| packaging | global or sku | usd_per_order | box, mailer, inserts, tape per order |
| shipping_label | carrier_zone | usd_per_order | label cost by carrier and zone band, for example `usps_ground:zone_5`. A weight band can be added to the key. |
| threepl_pick_pack | global | usd_per_order | 3PL pick and pack fee per order; extra units per order as a second row with unit `usd_per_unit` |
| threepl_storage | global | usd_per_month | 3PL storage and account fees per month |
| returns_processing | global | usd_per_return | inspection, restock and return label per return |
| payment_fee_percent | channel | percent | gateway percent by channel (online store, marketplace, wholesale) |
| payment_fee_fixed | channel | usd_per_order | gateway fixed fee per transaction |
| marketplace_fee_percent | marketplace | percent | referral or commission percent |
| marketplace_fee_fixed | marketplace | usd_per_order | per-order or fulfillment fee |
| app_fees | vendor | usd_per_month | app subscriptions, one row per app |
| agency_fees | vendor | usd_per_month | agency and tool retainers, one row per vendor |
| fixed_costs | global | usd_per_month | rent, insurance, software not listed above, other overhead |
| headcount_cost | global | usd_per_month | fully loaded payroll and contractors |
| cash_balance | global | usd | cash on hand as of `effective_from`; the newest row wins |
| credit_line_available | global | usd | undrawn credit as of `effective_from` |
| target_cac | global or channel | usd | target cost to acquire a first-time customer |
| target_mer | global | percent | target marketing efficiency ratio, revenue over all marketing spend |
| target_gross_margin | global | percent | target gross margin |
| target_contribution_margin | global | percent | target contribution margin |
| target_inventory_cover | global or sku | weeks | weeks of stock the brand wants on hand |
| pnl_actual | global | usd_per_month | monthly P&L actuals by line (revenue, cogs, marketing, opex, net) for reconciliation; `scope_key` holds the line name |

## Rules

- Missing shows as unavailable, never 0. A metric that needs a field the brand has not supplied reads unavailable and names the field it is waiting for.
- No default fills a blank. Industry averages never stand in for a brand's own costs. The sample brand carries `confidence: simulated` rows only.
- Partial coverage is shown as partial. If COGS exists for 30 of 40 SKUs, per-SKU margins show for those 30, the total reads unavailable, and the tile says "COGS on 30 of 40 SKUs".
- Windows use the row in force on each order's date for per-order and per-unit fields. Monthly fields are spread evenly across the days of the month they cover, then summed over the window.
- Percent plus fixed fees are computed per order in code, never as an average rate.
- A change of value is a new row with a new `effective_from`, never an edit of the old row. History stays intact so past windows do not move.
- Marketplace fees apply only to orders whose `channel` is that marketplace. Channel comes from `orders.channel`.
- Actuals never overwrite computed numbers. The Money screen shows both and the gap.
- Sales tax is not a cost and is not in this table; it comes from `orders.tax_lines`.

## Metrics unlocked

Formulas in words. Exact definitions of the underlying terms (paid order, net revenue, cohort) are in `metrics.md`. Every metric here is unavailable until each field it lists exists for the window.

| Metric | Fields needed | How |
|---|---|---|
| gross_margin | cogs_landed | net revenue minus COGS of units sold, over net revenue |
| gross_profit_per_order | cogs_landed | net revenue minus COGS, over paid orders |
| fulfillment_cost_per_order | packaging, shipping_label, threepl_pick_pack | sum per order, label picked by the order's carrier and zone band |
| payment_fees | payment_fee_percent, payment_fee_fixed | per order: total times percent plus fixed, summed |
| marketplace_fees | marketplace_fee_percent, marketplace_fee_fixed | same, marketplace orders only |
| returns_cost | returns_processing | returns in the window times the fee, plus refunded revenue from `reversed_orders` |
| contribution_margin (per order, per channel, total) | all of the above plus paid spend from `ad_rows` and `google_rows` | net revenue minus COGS, fulfillment, payment and marketplace fees, returns cost and marketing spend |
| break_even_roas | cogs_landed, packaging, shipping_label, threepl_pick_pack, payment fees | 1 over contribution margin before marketing, as a share of revenue |
| first_order_payback | contribution margin fields, target_cac or actual CAC | contribution on the first order over cost to acquire; under 1 means the first order does not pay back |
| operating_margin | contribution fields plus app_fees, agency_fees, fixed_costs, headcount_cost | contribution margin minus monthly costs spread over the window |
| cash_runway_weeks | cash_balance, credit_line_available, operating margin fields | cash plus undrawn credit over average weekly net burn; unavailable when burn is not negative |
| inventory_cover_weeks | target_inventory_cover for the target; `inventory` and `orders` for the actual | weeks of stock at trailing sell-through, compared to target |
| target gaps | target_cac, target_mer, target_gross_margin, target_contribution_margin | actual minus target, shown next to the actual tile |
| pnl_reconciliation | pnl_actual | computed line minus actual line, by month |

## Where the numbers come from for a real brand

- COGS: the brand's cost sheet, the 3PL receiving report, or Shopify unit cost as a first fill marked `estimate`.
- Shipping labels: the carrier invoice or the 3PL rate card, one row per zone band.
- Fees: the gateway statement and the marketplace settlement report; `payouts` can confirm the blended rate but never replaces the rows.
- Monthly costs and cash: the bookkeeper's P&L and the bank balance, entered monthly.

## Sample brand

The generator writes a simulated set for Bombas: COGS for every SKU, one carrier with 3 zone bands, one gateway, no marketplace, 6 app rows, 1 agency row, monthly fixed costs, headcount, a cash balance and all 5 targets. Values are plausible for a US sock and apparel brand at the brain's revenue band and are labeled simulated on every page. Calibration rules are in `calibration.md`.
