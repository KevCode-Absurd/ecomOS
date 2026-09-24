# 20-FIN Finance and accounting playbook

version: 2.0-draft  |  date: 24 Sep 2026  |  sources: 6 mini playbooks (5 independent presenters; 01 and 05 share a presenter and 01's T5 segment is the same case as 05)  |  cards: 203  |  built from: sources/*.md

## 0. How to use this playbook

**Who runs it.** The profit and marketing efficiency agent (finance agent). It owns the definitions every other agent uses for revenue, cost, margin, CAC and LTV; the P&L ladder and the 4-bucket view; the daily and weekly contribution readouts; the COGS and landed-cost table; break-even ROAS and CAC for any offer; cohort LTV and payback; the cash, inventory and PO checks; scenario answers; and the reconciliation of platform numbers to the books. A worker can run the section 5 checklists alone.

**All arithmetic is done in code, never by the model.** Every formula in section 3.0 is written so a developer can implement it: named variables, units, sign conventions and the source. The agent fetches inputs, calls the calculation, and reads the result. It never estimates a margin, a ratio or a cash balance in prose. If an input is missing, the output is "unavailable", not 0. Period ROAS and MER are total value divided by total spend for the period, never an average of daily ratios. Totals stay separate from breakdowns.

**Which sections to load for which task.**

| task | load |
|---|---|
| Define or check a metric (gross vs net, COGS scope, CM1 to CM3, MER, CAC, LTV, payback, CCC, FCF) | 3.0, 3.1, 3.2, 3.6, 3.7, 7 |
| Build or audit the COGS and landed-cost table | 3.2, P3, P4, P5, P6, checklist 5.3 |
| Build the P&L ladder and the 4-bucket view | 3.3, P1, P2, P15, checklist 5.1 |
| Daily contribution dashboard and weekly readout | 3.4, 3.5, P13, P14, checklist 5.2, deliverable 9.1 |
| Returns accrual | 3.5, P13 |
| CAC, first-order economics, LTV, LTGP:CAC, payback | 3.6, 3.7, P7 to P12, section 6 |
| Discount, promo, BOGO, discount vs CAC pool | 3.8, P16, 7 (C12) |
| Price a product | 3.9, P17 |
| Forecast revenue (new and returning), scenario answer | 3.10, 3.15, P18, P27, deliverable 9.3 |
| OPEX and payroll sizing | 3.11, P26, 7 (C4) |
| Cash vs profit, 3 statements, FCF | 3.12, P19, P20, checklist 5.5 |
| Inventory grades, days of inventory, PO, demand plan, liquidation | 3.13, P21 to P23, checklists 5.5, 5.6 |
| Cash conversion cycle, financing | 3.13, 3.14, P24 |
| Subscriptions and churn | 3.17, P12 |
| Reconcile Shopify, Meta, Amazon and Metabase numbers to the books | 3.16, P28, checklist 5.4 |
| Any point where sources disagree | section 7 |
| Alerts and what to hand back | section 9 |

**Fetch before acting.**

- From brand data: gross revenue, discounts, refunds, chargebacks and shipping collected by day; orders, units and new vs returning flag per order; landed cost per SKU; fulfillment cost per order (pick and pack, packing materials, outbound shipping, 3PL storage); payment and marketplace fee rates; ad spend by day and channel; other variable marketing (influencers, affiliates, variable agency fees); OPEX by month (payroll, software, rent, fixed agencies); return rate by month and category; cohort orders and revenue by first-purchase month; inventory units and cost by SKU with receive dates; supplier lead times, deposits and payment terms; opening cash, loan schedule, tax calendar; accounting policy on COGS scope. Full list in section 2 and section 10.
- From the data layer: Shopify (or the store platform) gross-to-net report, Metabase sales (for Gehna: dashboard 6), Meta and Google spend and attributed results (read only), the accounting system (Xero, QuickBooks, NetSuite or Tally), the inventory system, the cohort table.
- From the web: payment gateway fee rates, marketplace and FBA fee schedules, duty and tariff rates for the brand's import lanes, tax payment calendar, financing terms, accounting-standard treatment of shipping and handling. List in section 10, cadence in section 11.

**Source notes to keep in mind while reading.**

- Every number in the sources is a model input, a worked example, a vendor claim or a single anecdote. None of the 6 sources reports a study with sample size and method except the 1 cross-brand accounting study mini playbook 02 cites (Finaloop, industry gross margin about 42%). Treat every number in section 6 as a flag, never a target, unless the brand's own data confirms it.
- Mini playbook 01 is 16 videos by 1 presenter, 6 of them made or sponsored by a subscription-software vendor (Ordergroove). Its subscription, prepaid and default-to-subscription claims are vendor claims. Its accounting mechanics are standard.
- Mini playbook 02 is an agency founder (Common Thread Collective) on a podcast. Its rules of thumb (OPEX 10 to 12%, payroll 12% of the lowest month, cost of delivery 30 to 40%, 4 peaks a year) are portfolio opinions from US brands on Meta, 2025 to 2026.
- Mini playbook 03 is an Australian agency presenter. Its P&L ladder, CM1 to CM3, waterfall pricing and LTGP:CAC bands are the most complete framework in the folder, but several of its worked examples contain arithmetic slips, corrected in section 8.
- Mini playbooks 04 and 06 are accountants (UK integrator, US controller). They give statutory COGS rules and no numbers. They put outbound shipping and fees below gross profit; 01, 02 and 03 put them above contribution margin. Section 7 (C1) settles how the agent handles this.
- Mini playbook 05 is 1 made-up 6-month three-statement model. Its cash mechanics are standard accounting.
- US and Australian context throughout: merchant fees about 3%, 25% benefits load, quarterly estimated tax, DMAs for geo tests, June financial year end in Australia. Indian brands (Gehna) must swap in GST, TDS, Indian payment gateway rates, Indian payroll on-costs and the Indian tax calendar. `[needs brand data: country-specific rates]` is implied wherever a US rate appears.
- Tags: `[verify UI]` for platform steps that change, `[needs brand data: what]` for anything that depends on the brand's own numbers, `[web check: what]` for anything to confirm live.

## 1. Scope and outcomes

**This folder covers.**

- Definitions and formulas: gross vs net revenue, COGS scope, landed cost, cost of delivery, CM1, CM2, CM3, contribution after ads, MER and aMER, break-even ROAS and CAC, blended, paid, media-only and fully loaded CAC, LTV and LTGP, LTV:CAC and LTGP:CAC, CAC payback, churn and lifetime, cash conversion cycle, operating cash flow, free cash flow, net cash flow, runway.
- The P&L ladder (gross revenue to net profit) and the 4-bucket P&L (cost of delivery, CAC, OPEX, profit), with percent-of-revenue reads and the fault rule (a missed line is caused by a line above it).
- Daily contribution readouts, the weekly profit memo, returns accruals, and the metric hierarchy (cash, then contribution, then business metrics, then customer metrics, then channel metrics).
- Discounts and CAC as 1 cost pool, promo modelling (percent off vs BOGO), break-even for any offer, the bottom-up pricing waterfall.
- Cohort forecasts of returning revenue, spend-vs-aMER forecasts of new-customer revenue, the 3-model forecast built from the marketing calendar, and scenario analysis (the next $10,000, spend up 50%, CAC sensitivity).
- Inventory and cash planning: 3-statement reads, FCF reconciliation, mini cash flow and runway, inventory roll with lead time, PO sizing, the demand plan before a PO, inventory grades A to D, days of inventory, liquidation funnels, the cash conversion cycle, vendor terms and inventory financing.
- Reconciliation of platform numbers (Shopify, Meta, Amazon, Metabase) to the books.
- Subscription unit economics, churn and prepaid modelling, as far as they feed LTV and cash.

**This folder does not cover (neighbour folder).**

- Media buying, bid strategies, campaign structure and creative: 11-ADC, 24-DEP, 10-MCR. This playbook only sets the CAC ceiling and the break-even the buyer must respect.
- Attribution models, geo-lift test design, Meta attribution settings, incrementality vendors: 06-MEA. This playbook keeps only the incrementality factor formula and the rule that break-even ROAS is compared to calibrated, not raw, platform ROAS.
- Offer construction, bundle design, subscription cart mechanics, gift with purchase creative: 03-OFF and 07-LPG. This playbook keeps the margin arithmetic for each offer type.
- Supplier sourcing, freight negotiation, factory price negotiation: 18-COG. This playbook keeps landed-cost allocation and the CCC.
- Amazon launch tactics, reviews, ranking: 22-AMZ. This playbook keeps the FBA unit-economics and inventory-lag model.
- Email and SMS flows: 14-EML. This playbook keeps the rule that returning revenue is forecast from the send calendar and cohort curves.
- Product development and SKU strategy beyond the finance test (margin, volume or cash problem): 03-OFF and 18-COG.

**Business measures this folder moves.**

- Contribution after marketing (CM3) in dollars and as a percent of net revenue, daily and monthly.
- Net profit percent and EBITDA percent.
- Free cash flow, cash balance and runway in months; days of inventory by SKU; cash conversion cycle in days.
- CAC against first-order gross profit; LTGP:CAC at 30, 90 and 365 days; cohort payback in months or orders.
- Gross margin (CM2) accuracy: the gap between the margin the team quotes and the margin the books show.
- OPEX and payroll as a percent of revenue.
- Forecast error: actual vs daily expectation, and the returning-revenue forecast error.

## 2. Inputs the agent needs

| input | from where | required or optional | why |
|---|---|---|---|
| Gross revenue by day (product sales at list, before discounts, excluding sales tax collected) | data layer (Shopify, Metabase) | required | Top of the ladder; every percent-of-revenue line divides by net revenue derived from it [895584eaf5b7] [c9ccfa76430a] |
| Discounts, refunds, chargebacks, shipping collected by day | data layer | required | Gross-to-net bridge; refunds and discounts are profit levers on their own [c9ccfa76430a] |
| Orders, units per order, new vs returning flag per order | data layer | required | Per-order and per-basket unit economics; CAC denominator is new customers only [49110942deea] [9a77dac5a3ba] |
| Landed cost per SKU (purchase price + inbound freight share + duty share + product packaging) | brand record, inventory system | required | Product COGS; without it every margin is wrong [a0e16cf2802e] [427dd537598d] |
| Fulfillment cost per order (pick and pack, packing materials, outbound shipping, 3PL storage, warehouse staff per order) | brand record, 3PL invoices | required | Cost of delivery and CM2 [4e8e7fd6e6e4] [db1cf398804d] |
| Payment gateway and marketplace fee rates | brand record; `[web check: current rates]` | required | Variable fees in cost of delivery [2978d63684ea] |
| Ad spend by day and channel; other variable marketing (influencers, affiliates, variable agency and creative fees) | data layer (Meta, Google, Amazon read only), brand record | required | CAC, MER, aMER, CM3 [fc4fd43c986c] [8cc010473338] |
| OPEX by month: payroll and on-costs, software, rent, fixed agencies and retainers | accounting system | required | EBITDA, 4-bucket OPEX share, payroll rule [7c524289c2d3] [434847dcd5bb] |
| Interest, tax, depreciation and amortisation by month | accounting system | required for monthly close | Below-EBITDA lines; cash timing [ff3c54a4afb8] [416bbd9031ed] |
| Return rate by month and category; average discount by category | data layer | required | Returns accrual, refund and discount allowance in pricing [1d3d04198311] [db1cf398804d] |
| Cohort table: customers, orders and revenue by first-purchase month and month since acquisition | data layer or SQL | required | Retention, LTV, LTGP:CAC, payback, returning-revenue forecast [540b5bdda637] [c87f67f6310b] |
| Subscription counts: prior-period subscribers, new, cancellations | data layer | optional (subscription brands) | Churn, lifetime, subscription LTV [e587bb652cdc] |
| Inventory units and cost by SKU, receive date, expiry or season date | inventory system | required for cash and inventory checks | Days of inventory, grades A to D, aged stock, waste [f2fc5286cc97] [2d244e2a4df6] |
| Supplier lead time, MOQ, deposit and payment terms per supplier | brand record | required for PO and CCC | Inventory roll, PO timing, CCC [308a0d76128c] [beb1703b3d17] [377b3fd122bf] |
| Opening cash, loan balances and repayment schedule, tax payment calendar | accounting system, accountant | required for cash checks | Runway, net cash flow, tax lumps [9d2823e98694] [4f714af151a4] |
| Accounting policy: what sits in statutory COGS, how freight and duty are allocated, capitalisation rules | brand record, accountant | required | Statutory vs internal margin views; consistency [4b0ff6e78865] [7d9e989e15be] |
| Marketing calendar with dates: launches, promos, sends, influencer drops, PR | brand record | required for forecasts | Event-effect model; returning revenue rises on send days [15d4d04ea13a] |
| Targets: net profit target, OPEX plan, CAC or ROAS line | user (owner) | required | CM3 back-solve, the constraint line [4ca15f364bbb] [75cf518af8d3] |
| Incrementality factors per channel, if any tests were run | 06-MEA registry | optional | Calibrate platform ROAS before comparing to break-even [ccf3794cd11d] |
| Comparable-brand curves (spend vs efficiency, repurchase) | web or agency benchmarks | optional | Regress a short or outlier history to the mean [ac073be6ad16] |
| Competitor prices for a product being priced | `[web check]` | required for pricing | Waterfall price vs market check [9ee62d2b55d0] |

## 3. Decision rules

Every rule states the rule, when it applies, the mini playbooks that support it (by number), any conflict (by section 7 code), and card ids. Where only 1 source supports a rule, the rule says so. Where sources disagree, the strictest condition is kept here and the disagreement is written out in section 7. Section 3.0 is the formula register; rules cite formulas by F number.

### 3.0 Definitions and formula register

Conventions for the developer. All money in the brand's reporting currency, tax exclusive. All percentages as decimals in code (0.30, not 30). A period is a day, week or month; every ratio for a period uses period totals (sum of numerators over sum of denominators), never an average of daily ratios. "Order" is 1 checkout; "unit" is 1 item; "customer" is 1 unique buyer; state which count a metric uses [49110942deea] [9a77dac5a3ba]. Missing inputs return "unavailable", never 0. Every output carries its definition label (for example "CM2, internal COD scope, tax excluded").

**F1. Gross revenue.**
```
gross_revenue = sum(list_price_per_line x quantity) for all orders in the period
```
Excludes sales tax, VAT or GST collected (pass-through). Before discounts, refunds and shipping collected. Sources: 01 (T7 counts tax in gross; this playbook does not), 03, 04. [957cabf05b5f] [c9ccfa76430a] [db1cf398804d]

**F2. Net revenue.**
```
net_revenue = gross_revenue - discounts - refunds_accrued - chargebacks + shipping_collected
```
`discounts` = coupon and automatic price reductions (a coupon reduces revenue; it is not COGS and not ad spend) [4b0ff6e78865]. `refunds_accrued` = the returns accrual for the period (F31), not refunds processed in the period, for management reads; the books use processed refunds and the two are reconciled at month end (P28). `shipping_collected` = shipping charged at checkout. Sources: 01, 02, 03, 04. [895584eaf5b7] [c9ccfa76430a] [1d3d04198311]

**F3. AOV and units per transaction.**
```
aov_net = net_revenue / orders
aov_new = net_revenue_new_customers / orders_new_customers
upt = units / orders
```
Use `aov_new` for CAC comparisons, never blended AOV [9a77dac5a3ba]. `upt` is typically 1.1 to 1.7 in the sources; unit economics in DTC are per basket, not per unit [49110942deea] [9a77dac5a3ba].

**F4. Landed cost per unit (statutory product COGS per unit).**
```
landed_cost_unit[sku] = purchase_price_unit[sku]
                      + freight_share[sku] / units_received[sku]
                      + duty_share[sku] / units_received[sku]
                      + product_packaging_unit[sku]
freight_share[sku] = shipment_freight x allocation_weight[sku]
duty_share[sku]    = shipment_duty_paid x allocation_weight[sku]
allocation_weight[sku] = basis[sku] / sum(basis[all skus in shipment])
```
`basis` is 1 documented allocation basis for every shipment: weight, volume, value or units. The sources name no basis; pick 1 and keep it [427dd537598d] [a0e16cf2802e]. `purchase_price_unit` is net of supplier discounts and credits [61551ff00944]. `duty_paid` is the duty actually paid, not the tariff rate [a0e16cf2802e]. Product packaging (the retail box) is in; the shipping carton is out [df753e79eb2d]. For a manufacturer add direct labor and manufacturing overhead [1939dcb79b5d]. Sources: 04, 06, 01.

**F5. Product COGS for a period.**
```
product_cogs = sum(units_sold[sku] x landed_cost_unit[sku]) over skus
```
Recognised when the unit sells, not when the invoice arrives; inventory is an asset until then [a490586f1272] [b4b11ba26397]. No source gives the opening-plus-purchases-minus-closing formula or a cost-flow method (FIFO, weighted average); the brand's accounting policy sets it `[needs brand data: cost flow method]` [427dd537598d]. Sources: 01, 04, 05, 06.

**F6. Fulfillment cost per order (variable delivery cost).**
```
fulfillment_order = pick_pack + packing_materials + outbound_shipping + storage_per_order
                  + warehouse_staff_per_order + payment_fee + marketplace_fee
payment_fee    = payment_fee_rate x order_revenue_collected
marketplace_fee = marketplace_fee_rate x order_revenue (marketplace orders only)
warehouse_staff_per_order = daily_warehouse_staff_cost / packages_shipped_per_day
```
Sources: 01 (pick and pack, packing, 3PL, shipping, merchant fees), 03 (adds warehouse staff, fees in COD), 02 (shipping and variable expense). Conflict C1: 04 and 06 keep all of these below statutory gross profit. [4e8e7fd6e6e4] [957cabf05b5f] [db1cf398804d] [7c524289c2d3]

**F7. Cost of delivery (COD).**
```
cod = product_cogs + sum(fulfillment_order) over orders
```
02's bucket 1 and 03's first expense bucket. Sources: 02, 03. [9a74113cfe78] [7c524289c2d3]

**F8. CM1, product margin.**
```
cm1_dollars = net_revenue - product_cogs
cm1_pct     = cm1_dollars / net_revenue
```
01 calls this "ecom gross margin"; 03 calls it product margin (CM1) and uses manufacturer unit cost only, before freight. This playbook uses landed cost. Never quote CM1 as gross margin [db1cf398804d] [ca717cbf0593]. Sources: 01, 03.

**F9. CM2, gross margin (true gross margin, contribution before marketing).**
```
cm2_dollars = net_revenue - cod
cm2_pct     = cm2_dollars / net_revenue
cm2_order   = aov_net - product_cogs_order - fulfillment_order
```
Per basket: `cm2_basket = price_paid_ex_tax - landed_cost x upt - fulfillment_order - refund_discount_allowance` [db1cf398804d]. 01 calls this "contribution margin" (T7) or "gross profit" (T9, T10). 03 calls it gross margin (CM2). This is the margin that sets the CAC ceiling (F15). Sources: 01, 03, 02. Conflict C11 on naming. [68431c491a0c] [957cabf05b5f] [e8db824002f5]

**F10. CM3, contribution after marketing.**
```
cm3_media    = cm2_dollars - ad_spend                       (02's daily CM; "contribution after ads")
cm3_loaded   = cm2_dollars - variable_marketing             (03's CM3; 01's post-marketing CM)
variable_marketing = ad_spend + influencer_fees + affiliate_fees + variable_agency_fees + variable_creative
```
Report both and label them. Daily dashboards use `cm3_media` because only ad spend is known daily; the weekly memo and the monthly close use `cm3_loaded`. Conflict C2 on what counts as variable marketing. Sources: 01, 02, 03. [25d900c4c527] [bf82ba8e8bc2] [7ca062ce13b6] [8cc010473338]

**F11. EBITDA, operating income and net profit.**
```
ebitda      = cm3_loaded - opex
opex        = payroll + payroll_on_costs + software + rent + fixed_agencies + other_fixed
net_profit  = ebitda - interest - tax - depreciation - amortisation
ebit_margin = ebitda / net_revenue
```
Interest sits below EBITDA, never in OPEX [7c524289c2d3] [ff3c54a4afb8]. 01's "operating income" = CM minus all opex including advertising, which equals `ebitda` here [f39ad32b21d7]. Sources: 01, 03, 05.

**F12. 4-bucket P&L.**
```
bucket_cod_pct    = cod / net_revenue
bucket_cac_pct    = ad_spend / net_revenue          (02: pure variable media only)
bucket_opex_pct   = opex / net_revenue              (02: rent, labour, software, agencies, contractors, fixed creative)
bucket_profit_pct = 1 - bucket_cod_pct - bucket_cac_pct - bucket_opex_pct
check: bucket_profit_pct == ebitda / net_revenue when variable_marketing == ad_spend
```
If influencers or variable agency fees exist, put them in the CAC bucket and state it, so that the 4 buckets still sum to 100%. Source: 02 only for the framing; 03 uses the same 3 expense buckets. [9a74113cfe78] [4ca15f364bbb]

**F13. Percent of revenue and trailing average.**
```
line_pct[m]        = line[m] / net_revenue[m]
trailing_per_order = sum(line over last k months) / sum(orders over last k months)
```
Source: 01. [c160135c9bd3] [49110942deea]

**F14. MER, aMER and ROAS.**
```
mer   = net_revenue / ad_spend                    (period totals)
amer  = net_revenue_new_customers / ad_spend
roas_platform[channel] = attributed_revenue[channel] / spend[channel]   (platform's own attribution)
roas_calibrated[channel] = roas_platform[channel] x incrementality_factor[channel]
incrementality_factor[channel] = incremental_result_from_test / platform_reported_result
```
MER includes returning revenue that would have come anyway; manage acquisition to aMER [8aab49e8f65e] [fc4fd43c986c]. Platform ROAS is a within-platform read only; never compare ROAS across platforms [08a2587ba438]. Factor example: platform 1.0, geo test 1.2, factor 1.2 [ccf3794cd11d]. Sources: 02, 03.

**F15. Break-even ROAS, break-even CAC (CPA) and the operating CAC ceiling.**
```
breakeven_roas_new  = 1 / cm2_pct_new_orders   = aov_new / cm2_order_new
breakeven_cac       = cm2_order_new                                    (first-order gross profit per new order)
cac_ceiling         = cm2_order_new - required_contribution_per_new_order
required_contribution_per_new_order = (net_target_pct + opex_pct) x aov_new   (from F27)
```
Break-even excludes OPEX and profit, so the operating ceiling sits below it [c49b93d6bb68]. 01's version: "CAC should be less than or equal to CM per order" [ca717cbf0593]. Compare `breakeven_roas_new` with `roas_calibrated` (F14), or better with aMER, not with raw platform ROAS. Sources: 01, 03, 02.

**F16. CAC, 4 definitions. Always label which one.**
```
cac_blended  = variable_marketing / new_customers                (01: all marketing; 03: total ad spend)
cac_media    = ad_spend / new_customers                          (02, 03: pure media)
cac_paid     = paid_ad_spend / paid_attributed_new_customers     (01)
cac_loaded   = (ad_spend + influencers + affiliates + variable_agency + variable_creative + discount_cost_new_orders) / new_customers
discount_cost_new_orders = sum(discount on first orders)          (01: discount + CAC is 1 pool)
cac_from_funnel = cpc / conversion_rate                           (01 T15; per-channel estimate only)
```
`new_customers` = customers whose first order fell in the period, from the store, never from platform CPA and never per channel [9a77dac5a3ba] [6fe6a3b41072]. Conflict C2. Sources: 01, 02, 03.

**F17. Discount and CAC as 1 pool (true cost of acquisition).**
```
true_cost_of_acquisition = discount_per_new_order + cac_media
cm3_per_new_customer     = (list_price - discount) - cogs_order - cac_media
```
A discount and CAC are the same money: post-marketing CM is unchanged only when CAC falls by the same dollar amount as the discount. Source: 01 only. Conflict C12. [aa80d087ca61] [8723bc22dfe2] [1247e2cd031e]

**F18. Discount vs CAC scenario grid (equal ad spend).**
```
for each scenario s:
  sessions            = ad_spend / blended_cpc
  purchases[s]        = sessions x conversion_rate[s]
  cac[s]              = ad_spend / purchases[s]
  net_aov[s]          = list_price - discount[s]
  cm2_customer[s]     = net_aov[s] - cogs_order
  cm3_customer[s]     = cm2_customer[s] - cac[s]
  net_sales[s]        = purchases[s] x net_aov[s]
  total_cogs[s]       = purchases[s] x cogs_order
  cm2_total[s]        = net_sales[s] - total_cogs[s]
  cm3_total[s]        = cm2_total[s] - ad_spend
pick s with max(cm3_total[s]) within brand limits
```
`conversion_rate[s]` is an assumption until tested `[needs brand data: conversion by discount level]`. Source: 01 only. [1247e2cd031e] [993ecc7a19f0]

**F19. Percent off vs BOGO per order.**
```
percent_off: revenue = aov x (1 - d); product_cogs unchanged; fees = fee_rate x revenue; cm2 = revenue - product_cogs - fulfillment_adj
bogo:        revenue = aov; product_cogs = 2 x product_cogs_unit; shipping and pick_pack rise a little; fees unchanged; cm2 = revenue - 2 x product_cogs_unit - fulfillment_bogo
cm3_promo = cm2 - cac_promo
```
Percent off gives away revenue; BOGO gives away cost. Condition: unit product cost is low and the second unit ships in the same box. Source: 01 only. [5425adb4473f] [13df6c347b0e]

**F20. Bundle cost lift.**
```
fulfillment_bundle_of_2 = fulfillment_order x 1.20      (03's estimate; measure the real lift)
```
Source: 03 only. [c49b93d6bb68]

**F21. First-order test.**
```
first_order_cm      = cm2_order_new
cm_to_cac           = first_order_cm / cac
first_order_profit  = first_order_cm - cac
```
Sources: 01, 03. [a592b3f28c58] [9a77dac5a3ba]

**F22. Cohort retention, NRR and cumulative value.**
```
cohort[c] = customers whose first order month == c
retention[c][n]     = customers_of_cohort_c_ordering_in_month_n / cohort_size[c]     (n = months since first order; month 0 = 1.0)
nrr[c][n]           = cohort_revenue[c][n] / cohort_revenue[c][0]
cum_revenue_per_customer[c][n] = sum(cohort_revenue[c][0..n]) / cohort_size[c]
cum_gp_per_customer[c][n]      = sum(cohort_gross_profit[c][0..n]) / cohort_size[c]
orders_per_customer[c][n]      = sum(cohort_orders[c][0..n]) / cohort_size[c]
calendar_month_total[m] = sum over c of cohort_metric[c][m - c]    (the diagonal)
```
Always divide by the original cohort size, not last month's survivors [540b5bdda637] [90b11f77327e]. Leave future cells empty, not 0 [2650453af6e8]. NRR above 1.0 is expansion, not an error [20b50a304d0f]. Sources: 01, 02, 03.

**F23. LTV (lifetime contribution) and LTGP (time-boxed).**
```
ltv_cohort        = cum_gp_per_customer[c][n_max]               (use the cohort with the most history)
ltv_simple        = cm2_order x lifetime_orders
ltgp[W]           = sum(gross_profit from orders within W days of first order) / cohort_size     (W in {30, 90, 180, 365})
ltv_churn         = gp_per_order x orders_per_period / churn_rate         (subscriptions only; F26)
ltv_weighted_mix  = sum(segment_share[s] x ltv[s])
```
LTV is lifetime profit, never lifetime revenue [613635831aff] [285ed6bb4705]. Gross profit here means CM2 per order (state the scope). Sources: 01, 03.

**F24. LTV:CAC and LTGP:CAC.**
```
ltv_to_cac     = ltv_cohort / cac_blended
ltgp_to_cac[W] = ltgp[W] / cac_media           (03's bands apply to W = 30 and 90)
paid_ltv_to_cac = ltv_cohort / cac_paid
```
Conflict C3 on the bands. Sources: 01, 03. [e2eaed277a0d] [55599aea266f] [8cab64f326b9]

**F25. Cohort CAC payback.**
```
outlay        = cohort_size x cac
cum_gp[t]     = sum over periods 0..t of (survivors[t] x gp_per_order)
payback_period = min t such that cum_gp[t] >= outlay
tail_profit    = cum_gp[t_max] - outlay
naive_payback  = cac / gp_per_month        (wrong: assumes 0 churn; report only as the lower bound)
```
Measure in months for monthly billing, in orders when customers skip or order every 2 to 3 months [9a3cda2fe90f]. Source: 01 only for the method; 03 gives a 3 to 6 month agency window. [d78b5a172074] [285ed6bb4705]

**F26. Churn, lifetime and conversions.**
```
churn_rate[p]     = cancellations[p] / subscribers_at_end_of_prior_period
avg_lifetime      = 1 / churn_rate                                (in periods of the churn rate)
lifetime_orders   = avg_lifetime x orders_per_period
monthly_from_annual_survival = 1 - (1 - annual_churn) ^ (1 / 12)   (card's survival basis)
monthly_from_annual_simple   = annual_churn / 12                   (01's presenter: 40% annual = 2.5 years = 30 months)
subscribers[p]    = subscribers[p-1] + new[p] - churned[p];  churned[p] = subscribers[p-1] x churn_rate
```
Churn applies to subscriptions only; a one-off store uses cohort retention [d4b9ff187dc2] [e587bb652cdc] [fe4a0757982c]. The 2 annual-to-monthly conversions differ (40% annual: 24 months vs 30 months); state which one the brand uses (C13) [602ada5d7d4a]. Source: 01 only.

**F27. CM3 target back-solved from a net target.**
```
cm3_target_pct = net_target_pct + opex_pct
cm3_target_dollars = net_target_dollars + opex_dollars
```
Example: 20% net + 15% OPEX = 35% CM3. Source: 03 only. [4ca15f364bbb]

**F28. Waterfall price.**
```
price = fixed_costs_per_order / (1 - cm3_target_pct - pct_charges)
fixed_costs_per_order = cac_estimate + shipping_and_fulfillment_per_order + landed_cost x upt
pct_charges = return_allowance_pct + discount_allowance_pct + payment_fee_rate
require: (1 - cm3_target_pct - pct_charges) > 0
```
Example: (30 + 11 + 6) / (1 - 0.20 - 0.06) = 63.51. Source: 03 (card supplies the closed form; the transcript guessed "$70"). [9ee62d2b55d0]

**F29. Product-level contribution per sale and campaign split.**
```
contribution_per_sale[p] = cm2_order[p] - cac[p]          (cac[p] = CPA from that product's campaign, as an estimate)
rank products by contribution_per_sale, not by cpa
```
Source: 03 only. [3827dc99f5ed] [ac6ec12672a6]

**F30. Net shipping cost.**
```
net_shipping = shipping_collected - outbound_shipping_cost
shipping_pct = outbound_shipping_cost / net_revenue
```
Source: 02 only. [1e5dad6d98ce]

**F31. Returns accrual.**
```
return_rate = refunds_last_12_months / gross_revenue_last_12_months     (or by category and month)
refunds_accrued[day] = return_rate x gross_revenue[day]
month_end_true_up = refunds_processed_for_that_month_sales - refunds_accrued_for_that_month
```
Do not read Shopify "total sales" (today's revenue minus returns processed today) as the efficiency base [1d3d04198311]. Source: 02 only for the accrual; 03 uses an allowance in pricing. Conflict C15.

**F32. Existing-customer ad budget.**
```
existing_budget_month = existing_customers x monthly_frequency x cpm_existing / 1000
```
Example: 300,000 x 3 x 2.50 / 1000 = 2,250. Source: 03 only. [10c558b5c0d8]

**F33. Payroll baseline and on-costs.**
```
payroll_baseline_month = 0.12 x min(monthly_net_revenue over the year)      (02)
payroll_cost_month     = sum(annual_salary[role] / 12 x headcount[role])       (01)
on_costs               = payroll_cost_month x on_cost_rate                    (01: 0.25 in the US)
revenue_per_employee   = annual_net_revenue / fte
```
Sources: 02 (12% rule), 01 (payroll model). [798f1af7e866] [f39ad32b21d7] [66d5d76e9b71]

**F34. Cash conversion cycle and days of inventory.**
```
ccc = dio + dso - dpo
dio = inventory_value / (product_cogs_per_day)
dso = receivables / (net_revenue_per_day)            (near 0 for card-paid DTC; marketplace payouts add days)
dpo = payables / (product_cogs_per_day)
days_of_inventory[sku] = units_on_hand[sku] / avg_daily_units_sold[sku]
target: days_of_inventory[sku] ~= supplier_lead_time_days[sku]
```
Sources: 03 (CCC), 02 (days of inventory = lead time). [beb1703b3d17] [f2fc5286cc97]

**F35. Inventory roll, PO sizing and PO cost.**
```
inventory[t] = inventory[t-1] - units_sold[t] + arrivals[t]
arrivals[t]  = purchase_units[t - lead_time_periods]
constraint: inventory[t] >= 0 for all t (a negative month = stockout; move or enlarge the PO)
po_units     = sum(forecast_units_sold over lead_time + cycle_time) - inventory_on_hand - inventory_on_order
po_cost      = po_units x weighted_unit_cost
weighted_unit_cost = sum(mix_share[sku] x landed_cost_unit[sku])
```
Sources: 01 (lead time 3 to 4 months, cycle 4 months in its models), 02 (just in time). [308a0d76128c] [49138d1247d7]

**F36. Demand plan before a PO.**
```
po_units = units_existing_customers (email, SMS) + units_seeding (influencer) + units_paid
units_paid = media_dollars / cac_estimate x conversion_to_units
media_dollars_required = units_paid x cac_estimate / conversion_to_units
error_bars: new category -> wide range on cac_estimate (no history)
```
Source: 02 only. [20338553ad10]

**F37. Operating cash flow, free cash flow, net cash flow.**
```
operating_cash_flow = net_income + depreciation + amortisation
                    - delta_receivables + delta_payables - delta_inventory + delta_tax_liability + other_working_capital
free_cash_flow      = operating_cash_flow - capex_cash                      (capex_cash as a positive number)
net_cash_flow       = free_cash_flow + financing_cash_flow                   (loan draws in, principal and distributions out)
check: net_cash_flow == cash[t] - cash[t-1]
check: assets == liabilities + equity every month
```
Delta = this period minus last period. Inventory up = cash out. Do not subtract a negative investing figure (that would add it back) (C20). Sources: 05, 01. [652ee8dcf710] [059ee049c6fc] [4f714af151a4] [6fab761526bc]

**F38. Mini cash flow and runway (planning model).**
```
closing_cash[m] = opening_cash[m] + net_income[m] - inventory_purchases_paid[m] + product_cogs_of_units_sold[m] - other_capex[m] - principal_repaid[m] - tax_paid[m]
runway_months   = count of months until closing_cash < 0
lowest_cash     = min(closing_cash[m])
```
`product_cogs_of_units_sold` is added back because that inventory was paid for earlier; inventory purchases hit cash when paid (deposits and balances by supplier terms) [9d2823e98694] [6a8332853dd6]. Source: 01, 05.

**F39. Depreciation, capitalised cost and tax with loss carryforward.**
```
monthly_depreciation = capitalised_cost / useful_life_months      (05: 36 months "for most software"; 3 or 5 years for other assets)
cumulative_taxable   = max(0, cumulative_profit_since_start)
tax_expense[m]       = tax_rate x max(0, profit[m]) only once cumulative losses are used up
tax_paid[m]          = per the brand's payment calendar (US: quarterly estimates)
```
Sources: 01, 05. `[web check: tax calendar and loss carryforward rules]` [7d9e989e15be] [b8599dca5b33] [416bbd9031ed]

**F40. Forecast chain from ad spend (planning model).**
```
new_customers[m]        = round(ad_spend[m] / cac[m])
returning_transactional[m] = return_rate x sum(new_customers over the trailing 6 months)     (01: 3 to 5% a month)
subscriptions[m]        = subscriptions[m-1] + new_subs[m] - subscriptions[m-1] x churn
orders[m]               = new_customers[m] + returning_transactional[m] + subscriptions[m]
net_revenue[m]          = sum over segments of orders x net_aov[segment]
check: rolled-up cm2_pct per segment == unit-economics cm2_pct per segment
```
Source: 01 only. [563870c81120] [c1e5e9113ebe] [1903080a3a75] [f1bd2de486c0]

**F41. Returning-revenue forecast (cohort method).**
```
returning_revenue[m] = sum over cohorts c of cohort_size[c] x repeat_rate[m - c] x aov_returning
returning_revenue_adj[m] = returning_revenue[m] x seasonality[month_of_year] + planned_event_revenue[m]
seasonality[k] = mean over last 3 years of (returning_revenue[k] / annual_mean_returning_revenue)
```
Example: 100 x 0.001 x 100 = 10 (the source said 1; corrected). Sources: 03, 02. [c87f67f6310b] [fc4fd43c986c]

**F42. New-customer revenue forecast (spend vs aMER curve).**
```
fit amer = f(daily_ad_spend) on about 1 year of daily points, excluding sale days, BFCM and days under the minimum spend (03: under 1,000 a day)
new_customer_revenue[m] = sum over days of ad_spend[d] x f(ad_spend[d])
required_spend(target_revenue, target_amer) = solve f(spend) == target_amer; spend = target_revenue / target_amer
```
Fit log or linear, whichever fits best; add seasonality and an AOV term (02). Sources: 03, 02. [0d00eb5d6d39] [fc4fd43c986c]

**F43. 3-model daily expectation.**
```
expected_revenue[d] = new_customer_revenue[d] + returning_revenue[d] + event_effect[d]
variance[d]         = actual_revenue[d] - expected_revenue[d]
```
Source: 02 only. [4d4d40fe1138] [15d4d04ea13a]

**F44. Marginal return and the profit frontier.**
```
marginal_amer[channel] = delta_new_customer_revenue / delta_spend       (from a +delta test, an incrementality test or an MMM)
stop when marginal_amer[channel] <= breakeven_roas_new
move delta from the channel with the lowest marginal_amer to the one with the highest, while both stay above break-even
```
Sources: 03, 02. [c60eaf1ca845] [35efd9091446]

**F45. Reconciliation of platform numbers to the books.**
```
gap_revenue  = platform_net_sales - books_net_revenue
gap_refunds  = refunds_accrued - refunds_processed
gap_fees     = platform_fees_reported - fees_in_books
gap_spend    = sum(platform_spend by channel) - marketing_in_books
gap_attrib   = sum(platform_attributed_revenue) - net_revenue        (expected > 0; each platform claims overlapping orders)
```
Every gap is explained by a named cause (tax, timing, processed vs accrued returns, shipping income, fee coding, currency) or it is an error. Sources: 02, 03, 04. [1d3d04198311] [c9ccfa76430a] [4b0ff6e78865]

