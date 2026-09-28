# Finance and cash: features

Status: todo | doing | done | parked. One feature per commit. The first round is the skeleton; after that, features come in rounds of 10, stack-ranked by revenue impact, usefulness and how easy they are to build on dummy data.

## Round 0: skeleton

| # | Feature | Status |
|---|---|---|
| 0.1 | Page shell in the shared UI kit: header, empty-state tiles, insight list, action buttons | done |
| 0.2 | `api.py` serving this screen's metrics from `app/data/` with unavailable states | done |
| 0.3 | 3 metric tiles (gross margin, online store contribution after marketing, MER), 2 insights (margin basis, MER against target), 1 chart (margin ladder by month) on Bombas | done |
| 0.4 | `audit.py`: all 11 room rules (FIN-R01 to FIN-R11) in the contract shape; P&L ladder, sales lines, margin by SKU and cash facts | done |

## Room jobs

| Job | Question | Capabilities |
|---|---|---|
| know real profit per order, SKU and channel | what did we actually make on this, after every real cost | MONEY-C01, MONEY-C02, MONEY-C03 |
| price or re-price a product from a profit target | is this price actually profitable at our margin target | MONEY-C04 |
| gate a promo before it goes live | will this sale, BOGO or gift-with-purchase lose money | MONEY-C05 |
| see the cash runway before it is a crisis | when do we run low on cash if nothing changes | MONEY-C06 |
| plan inventory cash and the cash conversion cycle | how much cash is tied up in stock, and for how long | MONEY-C07 |
| compare financing, the data room and insurance | what does this loan, investor ask or coverage gap do to our cash | MONEY-C08, MONEY-C58, MONEY-C59 |
| know CAC, payback and LTV:CAC before scaling spend | can we afford to spend more on acquisition | MONEY-C09 |
| forecast revenue from cohorts and the calendar | what will next month's revenue look like, new vs returning | MONEY-C10 |
| build and defend the OPEX and payroll budget | what can we afford to spend, and what does the next dollar buy | MONEY-C11 |
| stay compliant on sales tax, liabilities and FX | are we exposed on nexus, gift-card liability or currency risk | MONEY-C12 |
| trust the daily and weekly numbers | do Shopify, Meta, GA4, the processor and the books agree | MONEY-C14, MONEY-C15 |
| know which SKUs and subscribers make money | which products or plans should we grow, fix or cut | MONEY-C17, MONEY-C18 |
| set the acquisition financial calendar | how much can we safely spend around BFCM and promos | LOOP-C05 |
| turn every payout, bill and payroll run into one ledger | where did this payout or bill actually land | MONEY-C51 to MONEY-C57, MONEY-C60 |

## JTBD rules (audit.py)

| Rule | Room insight | Inputs | Capability | Bombas, round 0 |
|---|---|---|---|---|
| FIN-R01 | margin leak by SKU | products_monthly, finance_inputs, orders, reversed_orders, paid_media_monthly | MONEY-C02 | fires: 6 single-pair SKUs lose $1 to $7 per unit after marketing while units rise |
| FIN-R02 | cash below floor | bank_ledger, cash floor in the brain | MONEY-C06 | unavailable |
| FIN-R03 | promo missed break-even | promo_models | MONEY-C05 | unavailable |
| FIN-R04 | CAC payback outruns cash cycle | accounts_payable | MONEY-C09 | unavailable |
| FIN-R05 | platform-books gap unexplained | finance_inputs.pnl_actual | MONEY-C15 | unavailable |
| FIN-R06 | payout deposit stuck | payouts, bank_ledger | MONEY-C52 | unavailable |
| FIN-R07 | COD remittance stuck | cod_remittance | MONEY-C52 | not run: markets IN only |
| FIN-R08 | inventory cash overhang | inventory, inbound_pos, order_lines | MONEY-C07 | runs, silent: every SKU sits under lead time + 30 days |
| FIN-R09 | subscription churn spike | subscription_cohorts | MONEY-C18 | not run: no subscriptions |
| FIN-R10 | budget overrun | budget_annual | MONEY-C11 | unavailable |
| FIN-R11 | sales tax nexus exposure | sales_tax_filings | MONEY-C12 | unavailable |

## Candidates from the room spec (pick 10 per round)

### Questions this screen should answer

- what did we actually make on this, after every real cost  (MONEY-C01, MONEY-C02, MONEY-C03)
- is this price actually profitable at our margin target, not just above cost  (MONEY-C04)
- will this sale, BOGO or gift-with-purchase lose money  (MONEY-C05)
- when do we run low on cash if nothing changes  (MONEY-C06)
- how much cash is tied up in stock, and for how long  (MONEY-C07)
- what does this loan, this investor ask or this coverage gap do to our cash  (MONEY-C08, MONEY-C58, MONEY-C59, MONEY-C08)
- can we afford to spend more on acquisition  (MONEY-C09)
- what will next month's revenue look like, split new vs returning  (MONEY-C10)
- what can we afford to spend, and what does the next dollar of spend buy  (MONEY-C11)
- are we exposed on sales-tax nexus, gift-card liability or currency risk  (MONEY-C12)
- do Shopify, Meta, GA4, the processor and the books agree  (MONEY-C14, MONEY-C15)
- which products or subscription plans should we grow, fix or cut  (MONEY-C17, MONEY-C18)
- how much can we safely spend around Q4 holiday (BFCM) and the rest of the promo calendar  (LOOP-C05)
- where did this payout, this bill, or (for an India-selling brand) this COD cash actually land  (MONEY-C51, MONEY-C52, MONEY-C53, MONEY-C54, MONEY-C55, MONEY-C56, MONEY-C57, MONEY-C60, MONEY-C52)

### Metrics specified

- `cm1_per_order`: What is left after the product and payment fees. net revenue − COGS − payment processing fees, per order
- `cm2_per_order`: What is left after also paying to pack and ship it. CM1 − fulfillment, shipping and packaging cost, per order
- `cm3_per_channel`: What is left after also paying the marketing that brought the order in. CM2 − variable marketing spend attributed to that order's channel (spend allocated pro rata by attributed orders)
- `net_profit`: What the brand actually kept, bottom of the P&L ladder. gross revenue − COGS − delivery cost − marketing cost − OPEX
- `gross_margin_pct`: Percent kept after just product cost. (net revenue − COGS) ÷ net revenue
- `cash_low_point_13wk`: The lowest the bank balance is expected to go in the next 13 weeks, and when. rolling 13-week cash forecast from current balance plus modeled inflows and outflows, minimum point
- `days_inventory_outstanding`: How many days of stock sit in the warehouse on average. average inventory value ÷ (COGS ÷ days in period) × days in period
- `cash_conversion_cycle`: Days between paying for stock and collecting cash for it. days inventory outstanding + days sales outstanding − days payable outstanding
- `cac_blended`: Total cost to get one new customer, all channels included. total marketing spend ÷ new customers acquired, same period
- `cac_payback_months`: Months of gross profit it takes to earn back what it cost to get a customer. CAC ÷ average monthly gross profit per new customer, from real cohorts
- `ltgp_to_cac`: Lifetime gross profit for every dollar spent to acquire. lifetime gross profit per customer (fixed lookback window) ÷ CAC
- `mer_and_amer`: Total revenue for every dollar of ad spend, plain and adjusted. MER = total revenue ÷ total ad spend; aMER = (total revenue − discount-code and branded-search revenue) ÷ total ad spend
- `landed_cost_per_sku`: The full cost to get one unit into a box, ready to sell. product cost + freight + duty + packaging, per SKU
- `platform_books_variance`: How far Shopify, Meta, GA4, the processor and the books disagree. for each of the 5 recurring gaps: |platform figure − books figure| and named cause
- `payout_deposit_gap`: Payout cash a gateway or marketplace says it sent but that has not yet landed in the bank. sum reported paid by gateway/marketplace − sum landed in bank, aged by days since the payout was reported
- `cod_remittance_gap`: COD cash collected but not yet in the bank (India only; reads null for US brands). sum of COD collected by courier − sum remitted, aged by days since collection
- `sales_tax_liability_position`: What is owed or claimable in state sales tax this period (GST for India-selling brands). sales tax collected − sales tax remitted/credit available, by state (output GST − input GST credit, by state/GSTIN, for India)
- `opex_vs_budget`: Overspend or underspend against the annual plan, by category. (actual OPEX − budgeted OPEX) ÷ budgeted OPEX, per category, per month
- `subscription_churn_rate`: Share of subscribers who left this period, against the right base. customers who canceled in period ÷ active subscribers at the start of the period

### Insights specified (rules in code)

- margin leak by SKU: a SKU's unit volume rose over the trailing 3 months while its CM3 stayed negative → "{sku} sold more each month but still loses ${amount} per unit after marketing cost" (action MONEY-C02)
- cash below floor: the 13-week forecast's lowest point falls below the brand's stated minimum cash floor → "cash is projected to fall below ${floor} in week {n} if nothing changes" (action MONEY-C06)
- promo missed break-even: a completed promo's realized margin is below the break-even margin modeled before it launched → "{promo} needed a {x}% sales lift to break even and got {y}%" (action MONEY-C05)
- CAC payback outruns cash cycle: CAC payback period in months exceeds the cash conversion cycle expressed in months → "new customers take {x} months to pay back but cash is tied up for {y} months first" (action MONEY-C09)
- platform-books gap unexplained: platform_books_variance exceeds 2% for a source with no cause tagged → "{source} and the books differ by ${amount} this month with no named cause" (action MONEY-C15)
- payout deposit stuck: payout_deposit_gap for a source exceeds that source's stated payout SLA in days → "${amount} from {source} is {n} days past its payout SLA" (action MONEY-C52)
- COD remittance stuck: cod_remittance_gap for a courier exceeds that courier's stated SLA in days (India only; reads null for US brands) → "₹{amount} in COD cash from {courier} is {n} days past its remittance SLA" (action MONEY-C52)
- inventory cash overhang: days_inventory_outstanding exceeds the SKU's supplier lead time by more than 30 days → "${amount} of {sku} stock sits {n} days beyond what lead time needs" (action MONEY-C07)
- subscription churn spike: subscription_churn_rate this month exceeds the trailing 3-month average by 20% relative → "{x}% more subscribers churned this month than the 3-month average" (action MONEY-C18)
- budget overrun: opex_vs_budget for a category exceeds 10% over budget → "{category} spent {x}% over budget this month" (action MONEY-C11)
- sales tax nexus exposure: a state or marketplace's trailing 12-month sales crossed the economic-nexus threshold with no matching registration on file (the GST registration threshold, for India-selling brands) → "{market} sales crossed the sales-tax nexus threshold with no registration logged (the GST registration threshold, for India)" (action MONEY-C12)

### Visuals specified

- P&L ladder (waterfall chart): gross revenue stepping down through COGS, delivery cost, marketing cost and OPEX to net profit
- 13-week cash forecast (line chart with a marked floor): projected daily cash balance with the lowest point and its date flagged
- contribution margin by SKU and channel (ranked bar table): CM1, CM2, CM3 per SKU and per channel, sorted worst to best
- CAC and payback trend (line chart with a shaded LTGP:CAC band): blended CAC and payback months over time against the brand's own target band
- platform-to-books bridge (bridge/waterfall chart): the 5 recurring gaps (Shopify, Meta, GA4, processor, accounting) and their named causes
- payout deposit aging (bar chart by source (gateway, marketplace; courier for India COD), bucketed by days late): how much payout cash is owed by each source and how overdue it is
- budget vs actual (bar chart by OPEX category): budgeted vs actual spend per category, this month and trailing

### Not in the usual tools

- one P&L ladder from gross revenue to net profit with CM1, CM2 and CM3 labeled by scope, computed automatically from the brand's own order and cost data
- a rolling 13-week cash forecast tied to the same order, cost and payroll data as the P&L
- a promo break-even gate that blocks or clears a promo before it goes public, using the brand's real CM3
- financing options stress-tested live against the brand's actual rolling cash forecast, not a one-time spreadsheet comparison
- payout cash tracked to the bank and escalated to the source automatically once a remittance passes that source's own SLA (COD cash and the courier, for India-selling brands)
- all 5 recurring platform-to-books gaps reconciled in one place with a named cause each month

### Data this screen needs

- `orders`: order_id, sku_lines, gross_revenue, discounts, refunds, payment_method, channel, placed_at, first_time_customer (Shopify Admin API export)
- `landed_cost`: sku, product_cost, freight, duty, packaging, effective_date, backup_doc_url (manual finance upload)
- `ad_spend`: brand, channel, campaign, date, spend, attributed_revenue (Meta MCP (read-only) + Google Ads export)
- `bank_ledger`: date, amount, counterparty, category, account (accounting export (QuickBooks/Xero; Zoho Books/Tally for India) or bank feed)
- `settlements`: platform, payout_id, gross, commission, fees, tax_on_fees, refunds, net, payout_date (marketplace/gateway payout reports)
- `cod_remittance`: courier, order_id, cod_collected, remitted_amount, remitted_date, sla_days (courier portal/API (Shiprocket, Delhivery); reads null for US brands)
- `payroll_statutory`: employee_id, cycle, gross, federal_withholding, state_withholding, fica, suta, net (Gusto or ADP export)
- `payroll_statutory_india`: employee_id, cycle, gross, pf, esi, pt, tds, net (payroll processor export; reads null for US brands)
- `fixed_assets`: asset_id, purchase_date, cost, useful_life, depreciation_method, book_value (manual register)
- `expenses_cards`: employee_id, date, amount, category, receipt_url, policy_flag (expense/card feed)
- `budget_annual`: category, month, budgeted, actual (manual budget document)
- `subscription_cohorts`: customer_id, plan, start_date, churn_date, mrr (subscription platform export (e.g. Recharge))
- `sales_tax_filings`: state, period, tax_collected, tax_remitted, filed_at (Avalara or TaxJar export)
- `gst_filings`: gstin, state, period, output_gst, input_credit, filed_at (GST invoicing app export; reads null for US brands)

## Rounds

| Round | Features picked | Date | Notes |
|---|---|---|---|
| 0 | shell, api, tiles, insights, chart, audit | 28 Sep 2026 | S3.23 |

## Round 0 status

1. Built: index.html, screen.js, api.py, audit.py (11 rules), tests/test_screen_finance_cash.py (9 pass), round0.png at 1280 wide.
2. Dollars come from the scale 1.0 aggregates. The 0.1 data.sqlite gives only rates (fees, fulfillment, returns per dollar; days of stock).
3. Bombas, Aug 2026: gross margin 72.4 percent, online store CM3 30.5 percent, MER 4.06x. All simulated.
4. Months before Jan 2025 have no cost rows and read None. Retail (POS) has no card fee rows, so its CM2 reads unavailable.
5. Donated pairs carry no cost row, so gross margin reads about 9 points over the brain's 63 percent model (insight 1).
6. Next: cost donated items, CM3 by acquisition channel, 13-week cash forecast, payout aging. app/metrics.py margin metrics read unavailable for brand folders.
