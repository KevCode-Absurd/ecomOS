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

### 3.1 Revenue and margin definitions

**R1. Read gross to net every month, not net alone.** Net revenue moves for 4 reasons: gross demand, refunds, discounts, shipping collected. Accounting software usually shows only net or cash; the store platform shows the bridge. 03's example: net 100K then 110K with gross 120K both months; the growth was refunds falling from 20K to 10K, not demand. Condition: every monthly close and every "revenue is up" claim. Sources: 03, 01. Cards: [c9ccfa76430a] [895584eaf5b7].

**R2. Exclude pass-through sales tax, VAT or GST from revenue before any margin.** 01 (T7) counts taxes collected in gross revenue; 03 removes them. Keep them out. The 24% vs 26.4% gap in 03's t-shirt example is exactly this convention (C14). Condition: always. Sources: 03; 01 conflicts. Cards: [db1cf398804d] [957cabf05b5f].

**R3. Treat refunds, discounts and shipping collected as profit levers, and test them as offers.** Lower refunds, fewer discounts and more shipping collected raise net revenue with no extra traffic; 03 says most brands under-collect shipping. Raising a shipping charge is an offer change: test conversion first (03-OFF). Condition: any brand where refunds or discounts exceed 5% of gross. Sources: 03, 02 (net shipping). Cards: [c9ccfa76430a] [1e5dad6d98ce].

**R4. Keep 3 margins apart and name them on every number: CM1 (product margin), CM2 (gross margin after cost of delivery), CM3 (contribution after marketing).** 01 and 03 both warn that people say "gross margin" or "contribution margin" and mean different things; 01 itself uses the words 3 ways (C11). A number without its scope label is unusable. Condition: every report, dashboard and formula output. Sources: 01, 03. Cards: [68431c491a0c] [7ca062ce13b6] [ca717cbf0593].

**R5. Never quote product margin as gross margin, and never set a marketing budget off product margin.** 03's t-shirt: 70% product margin became 24% gross margin once shipping, pick and pack, fees, freight and a refund and discount allowance were subtracted. A budget set off 70% is unprofitable at 24%. Condition: always; check with checklist 5.3 before any CAC target is set. Sources: 03, 01, 06. Cards: [db1cf398804d] [e8db824002f5] [aacabc94746b].

**R6. CM2 per new order is the ceiling on CAC (F15).** "Your CAC should be $83 or less" when CM per order is $83 (01). Break-even CAC = gross margin dollars per new order (03). The operating ceiling sits below break-even by the contribution the business needs for OPEX and profit. Condition: always for first-order acquisition; the lifetime exception is R57. Sources: 01, 03. Cards: [ca717cbf0593] [c49b93d6bb68] [68431c491a0c].

**R7. Post-marketing contribution (CM3) is the core profitability gauge.** If CM3 is not positive, no OPEX cut can make the business profitable; nothing is left for payroll (01). CM3 minus OPEX is profit (02, 03). Condition: every month; every daily dashboard (as cm3_media). Sources: 01, 02, 03. Cards: [bf82ba8e8bc2] [25d900c4c527] [4ca15f364bbb].

**R8. Compute unit economics per basket, not per unit, and say which count a metric uses.** Baskets carry 1.1 to 1.3 units (01) or 1.5 to 1.7 (03). A per-unit margin overstates fulfillment cost per item sold and understates CAC per order. Condition: any per-order or per-customer metric. Sources: 01, 03. Cards: [49110942deea] [9a77dac5a3ba].

**R9. Small per-order savings decide profit at volume.** A couple of dollars off freight, pick and pack or fees across thousands of orders is "the difference between tens of thousands of dollars of losses or profit" (01). Divide each fulfillment line by revenue monthly to see which one moved. Condition: only matters at volume; at 50 orders a month the lever is elsewhere. Source: 01 only. Cards: [2978d63684ea] [4e8e7fd6e6e4].

**R10. Watch gross margin percent, not gross profit dollars, in and after a promo month.** In 05's model, orders nearly doubled in the sale month, margin percent fell because of the discount, then recovered. A dip explained by discount is fine; a dip from cost lines (air freight, higher pick and pack) is not. Condition: every month with a promo. Sources: 05, 01. Cards: [02bbff7623e0] [183999c47203].

### 3.2 COGS scope and landed cost

**R11. Statutory COGS is "all in until it's in": every cost to get the product from the supplier's door onto your shelf ready to sell.** Purchase price net of supplier discounts, inbound freight including the container, duty actually paid, product packaging, and for a manufacturer direct labor and manufacturing overhead. Costs after that point are expenses in the statutory view. Backup test: would you have paid this cost if you had not bought these goods? Rent, yes (expense); the container, no (COGS). Condition: statutory and compliance accounts; confirm with the accountant. Sources: 04, 06. Cards: [a0e16cf2802e] [4b0ff6e78865] [1939dcb79b5d].

**R12. Keep 2 cost views and label every margin with its view: statutory COGS (04, 06) and internal cost of delivery (01, 02, 03).** Internal COD adds outbound shipping, pick and pack, packing materials, 3PL storage, warehouse staff per order, payment fees and marketplace fees. The marketing decision uses COD (CM2). The statutory P&L uses the accounting policy. Never mix them in one table. Condition: always. Conflict C1. Sources: 01, 02, 03, 04, 06. Cards: [4b0ff6e78865] [db1cf398804d] [0f57ba17ebb2] [4e8e7fd6e6e4].

**R13. Split product cost from fulfillment on the internal P&L so each line can be tracked and cut.** Product cost = manufacturing, import freight, duties, packaging, inbound freight. Fulfillment = pick and pack, packing materials, 3PL, storage, shipping to customer, merchant fees. A single COGS line hides which cost moved. Condition: internal P&L; per-order and percent-of-revenue reads. Sources: 01, 03. Cards: [4e8e7fd6e6e4] [1a6c983c0c2f] [7c524289c2d3].

**R14. Land freight and duty per unit, per SKU, at the time the invoice arrives, with 1 documented allocation basis.** Freight and duty come as lump-sum invoices from different parties; attach each to its PO when it arrives, weight it across the SKUs in the shipment (weight, volume, value or units; the sources name none), and recompute landed cost when supplier price, exchange rate or freight changes. Never file freight invoices "to sort out later". Condition: every inbound shipment. Sources: 04, 06. `[needs brand data: allocation basis in the accounting policy]`. Cards: [427dd537598d] [366fbbf40de6] [a490586f1272].

**R15. Product packaging is COGS; shipping packaging is a fulfillment expense.** The retail box the customer sees is part of the product (04's "Apple box"); the brown carton is delivery. Split mixed packaging invoices by line. Condition: always. Sources: 04, 06. Cards: [df753e79eb2d] [1939dcb79b5d].

**R16. Inbound freight is COGS; outbound shipping to the customer is not statutory COGS by default.** 06 sees freight-out booked to COGS "often". 04 allows 2 exceptions (free shipping built into the price, and dropship freight charged by the supplier) but hedges with "could". Whatever the statutory treatment, outbound shipping is always in internal COD and always counted before a CAC ceiling is set. Condition: statutory books follow the written policy; internal view always includes it. Conflict C1 and C17. Sources: 04, 06, 01, 02, 03. Cards: [79cf39d0f59a] [0f57ba17ebb2] [957cabf05b5f].

**R17. Payment fees and marketplace fees are variable delivery costs in the internal view; in the statutory view they are expenses below gross profit.** 03 calls putting transaction fees in OPEX "a mistake" because they vary with revenue; 04 keeps Amazon and Shopify fees out of COGS. Both are right in their own view. Condition: internal COD includes them; statutory follows policy. Sources: 03, 04, 01. Cards: [db1cf398804d] [4b0ff6e78865] [2978d63684ea].

**R18. Warehouse staff who pick, pack and ship belong in cost of delivery, at daily cost divided by packages per day.** 03's example: $400 a day / 100 packages = $4 an order. Leaving them in OPEX overstates gross margin. Condition: internal view; the bookkeeper tags the staff and builds a custom P&L `[verify UI: Xero or QuickBooks tracking categories]`. Source: 03 only. Cards: [7c524289c2d3].

**R19. Coupons reduce revenue; they are not COGS and not ad spend.** Supplier discounts reduce product cost; supplier credits generally sit against product cost but may carry a stock movement, so check. Condition: always. Source: 04 only. Cards: [4b0ff6e78865] [61551ff00944].

**R20. Advertising, Amazon PPC and marketing-only partner revenue share are never COGS.** A partner involved in delivering the product can be COGS; a partner that only markets it is marketing OPEX or variable marketing. Condition: always. Sources: 04, 06. Cards: [4b0ff6e78865] [0dad09bf5876].

**R21. Returns costs are split by type.** Return shipping back to you: overhead expense. Repackaging or a new box to make the item sellable again: can go into COGS. Bringing it back without making it sellable: not COGS. Apparel and other high-return categories track a returns-cost KPI and contribution margin next to gross margin. Condition: any brand with returns above a few percent. Source: 04 only. Cards: [bb8589d09789].

**R22. Inventory is an asset until it sells; COGS is booked when the unit sells, not when the invoice arrives.** Purchase invoices dumped into the accounting system as expense with no stock adjustment is the most common failure 04 sees. Condition: always. Sources: 04, 05, 06. Cards: [a0e16cf2802e] [a490586f1272] [b4b11ba26397].

### 3.3 The P&L ladder and the 4-bucket view

**R23. Use 1 ladder for the whole company: gross revenue, discounts, refunds, chargebacks, shipping collected, net revenue, product COGS, CM1, fulfillment and variable delivery, CM2, variable marketing, CM3, OPEX, EBITDA, interest, tax and D&A, net profit.** Every line in dollars and as a percent of net revenue, month by month, with a target per line `[needs brand data: targets]`. Sources: 03, 01, 02. Cards: [4ca15f364bbb] [c160135c9bd3] [957cabf05b5f].

**R24. The 4-bucket view: cost of delivery, CAC (variable media), OPEX, profit. Find the bucket that eats profit and fix that one.** 02's teaching picture is 25% each; its reference mix for a strong brand is COD 30 to 40%, CAC 25 to 30%, OPEX 10 to 12% (or 10 to 15%), profit 15 to 20%. 02 also cites an industry average gross margin of 42% (COGS 58%), so 30 to 40% COD is not typical (C5). Condition: monthly, next to the ladder; buckets are flags, not targets. Source: 02 only for the framing; 03 uses the same 3 expense buckets. Cards: [9a74113cfe78] [1e5dad6d98ce] [434847dcd5bb].

**R25. A missed target is caused by a line above it (the fault rule).** Missed EBITDA: OPEX, marketing or COD. Missed CM3: marketing or COD. Missed CM2: COD or revenue (refunds, discounts, shipping collected). Trace before reacting; 01's T2 case traced a loss month to marketing going from 29% to 39% of revenue. Condition: every monthly review. Sources: 03, 01. Cards: [4ca15f364bbb] [7ca062ce13b6] [c160135c9bd3].

**R26. Interest sits below EBITDA, never in OPEX.** EBITDA is the earning power with no loans; a buyer zeroes the loans. Net profit is what is left after interest, tax, depreciation and amortisation. Condition: always. Sources: 03, 05. Cards: [7c524289c2d3] [ff3c54a4afb8] [4f714af151a4].

**R27. Split marketing into variable (paid ads, influencers, events, agency and creative help that flexes with demand) and fixed (a permanent in-house creative team, retainers).** Variable goes above CM3; fixed goes in OPEX. Some brands put all creative above CM3 because it drives revenue; that is allowed if the convention is written down and never changed mid-year. Condition: always; the choice changes the CAC bucket (C2). Sources: 03, 02. Cards: [8cc010473338] [9a74113cfe78].

**R28. OPEX is everything not in COD or marketing: people, software, office.** In ecommerce, the way to reinvest is marketing, not headcount, software or office, which "generally" do not drive revenue (03). What happens at most 7-figure brands: OPEX rises faster than marketing and COD, and profit stays flat in dollars for 3 to 4 years. Condition: any brand where OPEX percent is flat or rising while revenue grows. Sources: 03, 02. Cards: [7c524289c2d3] [434847dcd5bb].

**R29. Put a percent-of-revenue column next to every line to read trajectory: revenue growing, margins predictable, efficiency improving.** Marketing percent will bounce while scaling; COD and OPEX percent should not. Condition: monthly. Sources: 01, 03. Cards: [c160135c9bd3] [4ca15f364bbb].

**R30. Track net shipping cost (shipping collected minus shipping cost) every month.** Shipping should be about 10% of revenue or less; 20 to 30% is a red flag; product cost 10 to 20% of revenue for "most brands" (02). Parcels over 39.5 inches on a side cost more (host). Condition: monthly; price-test shipping charges (03-OFF). Source: 02 only. Cards: [1e5dad6d98ce].

**R31. Revenue is not profit, and profit is not cash.** 03: a $10M business at 5% net makes $500K; a $5M business at 20% net makes $1M. Chasing revenue while expecting margin to expand later fails for many early-stage founders. Condition: any growth plan. Sources: 03, 05, 01, 02. Cards: [4ca15f364bbb] [ff3c54a4afb8] [652ee8dcf710].

**R32. Reconcile the model to itself: rolled-up gross profit percent per segment must equal the unit-economics percent, and the roll-up tab must equal the monthly tab.** If they differ, a formula is wrong. Condition: every model build and every close. Source: 01 only. Cards: [f1bd2de486c0] [def705c265c2].

### 3.4 Daily and weekly contribution readouts and the metric hierarchy

**R33. Daily contribution margin (cm3_media) is the scoreboard for the whole team; cash flow is the CEO's.** Report CM daily against a monthly CM goal sized to cover fixed costs (profit = CM minus OPEX). Everyone manages daily CM; the CEO or CFO keeps a separate rolling 13-week cash flow forecast because cash has human timing choices in it. Condition: every brand with daily ad spend. Source: 02 only. Cards: [25d900c4c527].

**R34. Keep fixed costs out of the daily view.** Spreading rent and payroll per day creates a false "cut spend" signal on ordinary days. Fixed costs fall as a percent of revenue as volume rises, so if media makes positive incremental CM the fix may be to spend more. Condition: daily dashboards; the monthly view carries OPEX. Source: 02 only. Cards: [25d900c4c527].

**R35. Metric hierarchy: cash flow (CEO) above contribution margin (team) above business metrics (revenue, spend, MER, AOV) above customer metrics (new-customer revenue, aMER, new-customer CM, ad spend) above channel metrics (Meta ROAS, MTA ROAS).** Read the dashboard top down. No single metric shows health: you can win CM in a month while the new-customer file shrinks. Condition: every dashboard layout and every alert. Sources: 02, 03 (measurement pyramid). Conflict C8. Cards: [25d900c4c527] [5297f747603f] [d5c2a3d880d9].

**R36. Daily or weekly ROAS reports are not the core decision tool.** Keep live dashboards of aMER, profit contribution and, ideally, LTGP:CAC in a fixed window; use platform ROAS only for directional campaign reads inside 1 platform. Condition: always. Sources: 03, 02. Cards: [8d570963a07c] [d5c2a3d880d9] [25d900c4c527].

**R37. Always split finance-grade metrics into new-customer versions: new-customer revenue, aMER, new-customer CM, new-customer cohort size, first-order GP.** MER is contaminated by returning revenue that would have returned anyway; 03's example is MER 2 with aMER "might be" 1.4. Condition: every readout. Sources: 03, 02, 01. Cards: [8aab49e8f65e] [30261689958c] [fc4fd43c986c].

**R38. Track the active customer file, not the cumulative one.** About 80% of customers who will ever come back do so within 6 to 8 months (02's portfolio heuristic); after that treat them as lapsed. Growth of the active file is the best predictor of future returning revenue; set new-customer goals so you are not "squeezing the sponge". Condition: monthly; check the brand's own repurchase curve first `[needs brand data: repurchase curve]`. Source: 02 only. Cards: [5297f747603f].

**R39. Show the numbers to everyone.** "You can't ask people to affect things they aren't looking at" (02). Align dashboards with pay and ownership. Condition: opinion from 1 source; apply where the owner agrees. Source: 02 only. Cards: [25d900c4c527] [83186e2addd5].

**R40. Track actuals to a daily expectation so a miss is seen on day 5, not day 22.** The expectation is the 3-model forecast (F43). Condition: every month with a target. Source: 02 only. Cards: [4d4d40fe1138].

### 3.5 Returns accrual

**R41. Apply a returns accrual to daily and monthly revenue, not processed returns.** Set the rate from history (02's example 10%); subtract rate times the day's revenue; true up to actual returns at month end. 02's example: a $1M December accrues $100,000, about $3,333 a day. Condition: every brand with a return rate above a few percent; category rates where they differ `[needs brand data: return rate by month and category]`. Source: 02 only. Cards: [1d3d04198311].

**R42. Never read Shopify's default "total sales" (today's revenue minus returns processed today) as the efficiency base.** A $500,000 January that processes $100,000 of December returns looks like a 20% return rate when the rate is still 10%, and the team pulls back spend. Condition: any January or post-peak read `[verify UI: Shopify default sales metric]`. Source: 02 only. Cards: [1d3d04198311].

**R43. Put a refund and discount allowance into every per-basket margin and into the waterfall price.** 03's allowance in its t-shirt example: about 5% discounts plus about 10% refunds; fashion refund rates run 10% up to 80%. Condition: pricing, break-even and CAC ceilings. Source: 03 only; 01 uses 5 to 10% returns and 4 to 5% refunds as model inputs. Conflict C15 (accrual vs restatement). Cards: [db1cf398804d] [c9ccfa76430a] [1a6c983c0c2f].

### 3.6 CAC

**R44. CAC = marketing spent in the period / customers whose first order fell in the period, from the store's own data.** Returning customers are excluded; including them "gives you a CAC that makes no sense" (01). Platform CPA runs on attributed numbers and shows a better number than reality (03). Condition: always. Sources: 01, 03, 02. Cards: [6fe6a3b41072] [9a77dac5a3ba] [8cab64f326b9].

**R45. Report 4 CACs and label them: blended, media-only, paid, fully loaded (F16).** 02 and 03 use media-only for the CAC bucket and put agencies, contractors and fixed creative in OPEX. 01 adds influencers, agencies and the first-order discount. Use media CAC for daily platform steering and the aMER curve; use fully loaded CAC for payback, LTV:CAC and the pricing waterfall. Condition: every CAC in a report carries its label. Conflict C2. Sources: 01, 02, 03. Cards: [9a74113cfe78] [6fe6a3b41072] [1247e2cd031e] [8cc010473338].

**R46. Channel-level CAC is an attribution estimate, not a finance number.** 03 calls it "impossible" without attribution; 01 says map the funnel by stage and channel but gives no method. Use `cac_from_funnel = cpc / conversion_rate` as a planning estimate only, and calibrate with incrementality factors (06-MEA). Condition: planning and channel comparisons; never in the P&L. Sources: 01, 03, 02. Cards: [6fe6a3b41072] [9a77dac5a3ba] [e9dcc756a117] [ccf3794cd11d].

**R47. Paid CAC is what constrains growth; blended CAC is directional.** Paid channels can scale 20x in a month; organic may be friends and family and cannot. 01's live-stream case: blended LTV:CAC 1.4 but paid LTV:CAC 1.08. Condition: any scaling decision. Source: 01 only. Cards: [8cab64f326b9] [79a98ff8e618].

**R48. "What is a good CAC?" is the wrong question; pair CAC with first-order gross profit of new customers.** $100 CAC against $10,000 first-order GP (furniture) is excellent; against $20 GP (sweets) it loses $80. Use new-customer AOV and first-order GP, never blended AOV times blended margin, because returning customers raise blended AOV and new customers buy on discounted front-end offers. 03's example: blended $100 x 70% = $70 GP and a $35 CAC target, when new-customer AOV was $90 and first-order GP about $50. Condition: every CAC target. Sources: 03, 01. Cards: [9a77dac5a3ba] [a592b3f28c58].

**R49. CAC is a function of conversion rate; a discount that lifts conversion lowers CAC, and the discount cost must be added back (R67).** Condition: any promo or landing page change. Sources: 01, 03. Cards: [5425adb4473f] [1247e2cd031e] [9a77dac5a3ba].

**R50. CAC is unknowable before launch; put in a placeholder, replace with observed CAC, and re-forecast.** New categories get wide error bars. Condition: pre-launch models and new-category demand plans. Sources: 01, 02. Cards: [563870c81120] [1b23d41ee499] [20338553ad10].

**R51. Set the CAC or ROAS line from unit economics and payback, then do not move it.** A 2021 partner analysis 02 cites found 60% of media dollars "never paid back over any period". The most common failure is "capitulation to efficiency of acquisition": lowering the line each quarter. The team solves with story, peaks, creative, product and channels. Condition: the line must come from real marginal economics (F15, F44), not a wish. Source: 02 only. Cards: [75cf518af8d3] [09e7f0d32ea7] [35efd9091446].

**R52. Each new customer should be at least as profitable as the last; do not scale spend to fix bad unit economics.** 01's sub-optimal path: CAC 68 to 79 to 123 to 149 with flat CM and 1.2 to 1.8 lifetime orders, CM:CAC 0.58 to 0.6, funded by a $20M raise. "Should not be scaling until it can fix its unit economics." Condition: CAC rising with flat CM2 and flat repeat. Sources: 01, 03 (financing spiral). Cards: [e2eaed277a0d] [cd36c8b5eacc] [beb1703b3d17].

### 3.7 First order vs lifetime: LTV, LTGP:CAC and payback

**R53. Gate acquisition on the first order: CM2 per new order divided by CAC should be 1 or above, unless cohorts prove repeat.** 01 prefers break-even or better on order 1 because many ecommerce customers buy once, and later orders then carry no marketing. 03 says first-order GP under about $70 "is probably a problem" for paid acquisition at scale. Buy-once categories (much apparel, Black Friday buyers) must pass this gate. Condition: default for every brand; the exception is R57. Sources: 01, 03. Conflict C9. Cards: [a004a45541ef] [c160135c9bd3] [55599aea266f] [957cabf05b5f].

**R54. LTV is lifetime profit (CM2 per order times orders), never lifetime revenue.** Many tools report LTV as revenue; in ecommerce revenue and gross profit are far apart. Condition: always. Sources: 01, 03. Cards: [613635831aff] [285ed6bb4705] [c1e5e9113ebe].

**R55. Time-box LTV: LTGP at 30 and 90 days for efficiency targets, 90 or 180 days for customer value, 365 days only when acquisition is aggressive.** Open-ended LTV keeps rising as the window extends (03: $100 at 6 months, $110 at 12, $120 at 18) and leads to overspending on cash you may not see for years. 01's plateau rule: find where cumulative cohort revenue stops rising (about 12 months at 25% monthly churn) and do not use 60 to 90 days for products bought again months later. Condition: every LTV figure carries its window. Sources: 03, 01. Conflict C10. Cards: [55599aea266f] [285ed6bb4705] [8fcbcb2cd9ba].

**R56. Cohorts are the only valid way to see retention and LTV.** Group by first-purchase month; divide by the original cohort size; read a calendar month diagonally; leave future cells empty. Aggregate totals and churn rates miss the shape of the curve (Dollar Shave Club lost about 25% in month 1 and about 10 points across all of year 2). Condition: any retention, LTV or payback claim. Sources: 01, 02, 03. Cards: [540b5bdda637] [9e1b24779308] [136827bb25c7] [5297f747603f] [c87f67f6310b].

**R57. Spend above first-order profit only when a cohort with enough history proves the tail, and use the lifetime-orders figure from the cohort with the most history, not an extrapolation.** 01's T12 accepts $115 CAC against $33 first-order GP because cumulative GP passes CAC at purchase 4; T16 accepts $50 CAC on $15 first GP with a 4.5-month life. 03 hedges: most brands that lose on acquisition lack the retention to support it, and "if you think your retention is good, it's usually mediocre". Condition: a cohort of at least 6 months (01 uses 6-month and 12-month cohorts) with cumulative GP per customer above CAC, and cash to carry the payback (R104). Sources: 01, 03. Conflict C9. Cards: [8b747d69f620] [e564ae6200ef] [b6fb728dba04] [30261689958c].

**R58. Read LTGP:CAC in a fixed window against the bands, and read "above 3" as a prompt to test marginal spend, not as proof of underspending.** 03: below 1 is losing money on acquisition (only a tiny share can run it); 1 to 2 generally not good (only CPG with excellent retention or funded growth); 2 to 3 optimal, scale; above 3 a mistake, under-using paid media. 01: 1.0 is not acceptable, 2 to 3 or above to grow a subscription box profitably, 5+ at late stage, 3 to 5x first-order CM:CAC for exceptional stores. Common advice: 3:1 healthy. Condition: 30-day and 90-day windows for the bands; a ratio above 3 triggers the marginal test in F44 before spend is raised. Conflict C3. Sources: 03, 01. Cards: [55599aea266f] [79a98ff8e618] [7eeee3aaceae] [e2eaed277a0d].

**R59. Below 1 is usually poor acquisition efficiency or thin first-order GP, not a strategy.** Fix the first-order economics (price, offer, COD) before calling it a lifetime play. Condition: any LTGP:CAC below 1 in the 90-day window. Source: 03 only; 01 agrees that CM:CAC below 1 needs cohort proof. Cards: [55599aea266f] [613635831aff].

**R60. Compute CAC payback from a cohort, never as CAC divided by monthly gross profit.** The naive figure assumes 0 churn; real payback is 20 to 100%, sometimes 200%, longer (01). 01's example: naive 3.2 months, cohort 8 months. Measure in months for monthly billing and in orders when customers skip or ship every 2 to 3 months. Condition: always. Source: 01 only. Cards: [9a3cda2fe90f].

**R61. After payback, read the tail: how much profit accrues after break-even.** A cohort that barely pays back with no tail means pricing or fundamentals are wrong. Test CAC sensitivity ($125 breaks even month 5; $225 month 11 in 01's model). Condition: every payback read. Source: 01 only. Cards: [d78b5a172074] [9a3cda2fe90f].

**R62. Agency and category practice runs a 3 to 6 month payback window; use it as the outer limit unless cash reserves justify longer.** 03 says agencies, CPG, fashion and retail run 3 to 6 months. 02 says match the payback horizon to the cash reserve. Condition: set the window with the owner `[needs brand data: cash reserve and owner's payback tolerance]`. Sources: 03, 02. Cards: [285ed6bb4705] [8d574ab5e9da].

**R63. Most profit usually comes from returning customers, so report new and returning profit contribution separately.** 03's example: $140K new revenue at 50% GM minus $50K ad spend = $20K; $60K returning at 50% minus $2.5K retention tools = $27.5K. Condition: monthly. Sources: 03, 01, 02. Cards: [30261689958c] [db6a44e073b2] [ea7eb29c3679].

**R64. Marketing as a percent of revenue depends on LTV and stage.** High-LTV brands that hold new-customer acquisition flat see marketing percent fall as repeat revenue builds; low-LTV hard goods stay near 40 to 50% because every month needs new buyers (02's Ridge example about 50%; legacy retailers about 10%). Condition: judge a brand's marketing percent against its own repeat curve, not a universal number. Source: 02 only. Cards: [ea7eb29c3679].

**R65. Hold CAC flat for repeat orders only when nothing was spent to get them.** If repeat orders come through email or subscription, divide lifetime CM by the same CAC; if paid retargeting drove them, add that spend. Condition: any LTV:CAC. Source: 01 only. Cards: [a592b3f28c58].

**R66. Retention is the biggest LTV lever; then AOV; then COGS renegotiation.** Cutting churn from 27% to 20% raised churn-based LTV 35% (01); renegotiated COGS lifted LTV from $69 to about $80 in the same case. Compete on value, not price: price-led buyers stay price sensitive. Condition: subscription and repeat businesses. Source: 01 only. Cards: [86fcb4012931] [ed010f896be7] [482dba787e59].

### 3.8 Discounts, promos and the discount vs CAC pool

**R67. A discount and CAC are the same money: add them together as the true cost of acquisition.** $100 to Facebook or $100 to the customer gives the same post-marketing CM if the discount cuts CAC by the same dollars. Condition: holds only when CAC falls by the same dollar amount as the discount; test the conversion lift, do not assume it. Source: 01 only. Conflict C12. Cards: [aa80d087ca61] [8723bc22dfe2] [1247e2cd031e].

**R68. Set 1 pool for discounts and marketing, owned by whoever runs marketing, and pick the split that maximises total post-marketing CM at the same spend, not per-customer margin.** 01's grid: $100,000 spend, 0 discount gives $25,000 post-marketing CM; $60 off with a 3.8% conversion gives $63,000, with $25 per customer in every scenario. "It can go both ways": some brands win on volume with worse unit economics, others on a smaller, richer base. Condition: conversion lifts are assumptions until tested `[needs brand data: conversion rate by discount level]`. Source: 01 only. Cards: [1247e2cd031e] [993ecc7a19f0] [8acd81a0345e].

**R69. Recalculate break-even ROAS and break-even CAC at the discounted price before any public discount.** 03's example: $100 price, $40 GM: break-even ROAS 2.5, break-even CAC $40. At 30% off with costs unchanged: GM $10, break-even CAC $10, break-even ROAS 7 (2.8x the original; the transcript's 10 is a slip). If the required efficiency has never been seen on paid, the discount "shouldn't go out publicly". Condition: every blanket discount. Sources: 03, 01. Cards: [c49b93d6bb68] [5425adb4473f].

**R70. Percent off gives away revenue; BOGO, bundles and gift with purchase give away cost.** With 50% off, product and fulfillment cost do not fall, so CM after CAC can go negative (01's Black Friday model: CM $84 to $29, a $4 loss per customer at 20,000 orders; a brand 01 knew lost $500,000). BOGO: customer pays full AOV, product cost doubles, shipping rises a little, CM $69 and CM minus CAC $36. 03: a bundle of 2 raises fulfillment about 20%, not 100%; a $4 gift "valued" at $50 to $60 can double AOV. Condition: unit product cost low and the second unit ships in the same box; measure incremental conversion, a gift does not guarantee the sale. Sources: 01, 03. Cards: [5425adb4473f] [13df6c347b0e] [c49b93d6bb68].

**R71. Make money on Black Friday customers on the first order.** They "are notorious for having really bad retention"; expect sale-period cohorts (November, BFCM) to be worth less over time. Condition: BFCM and any sitewide sale. Sources: 01, 02. Cards: [5425adb4473f] [fc4fd43c986c].

**R72. Attach the best discounts to a loyalty or subscription on-ramp, not a flash sale; flat discounting is for grade C stock.** Flash-sale converters often will not buy again without a big discount; on-ramp joiners self-select into higher LTV. 03: a flat discount is for slow inventory, even at break-even, because it was not going to sell anyway. Condition: any discount plan. Sources: 01, 03. Cards: [8acd81a0345e] [c49b93d6bb68].

**R73. Model a promo on the full stack: baseline conversion, CAC, gross AOV, net AOV after refunds, product COGS, fulfillment COGS, CM, CM minus CAC, monthly orders; then the promo variant; then multiply by expected promo volume.** Condition: every promo above a few percent of monthly revenue. Source: 01 only. Cards: [5425adb4473f] [1a6c983c0c2f].

**R74. "No refunds or returns during a promo" is not a rule the agent may apply.** 01 calls it best practice; it ignores consumer law `[web check: statutory return rights in the brand's country]`. Condition: never. Source: 01 (rejected). Cards: [5425adb4473f].

**R75. Do not model pre-orders, BNPL or try-before-you-buy without a cancellation and return rate; revenue cannot be recognised until fulfilled.** Condition: any such offer. Source: 02 only. Cards: [135d3773766f].

**R76. A discount that lifts conversion enough is the cheaper way to buy customers; a discount that does not is pure margin loss. Test as a split before committing.** 01 names the test but does not design it; 09-CRO holds the design. Condition: always. Source: 01 only. Cards: [1247e2cd031e].

### 3.9 Pricing waterfall

**R77. Price bottom-up from the net target, never by keystone or an arbitrary markup.** Keystone (cost x 2) ignores fulfillment and marketing; IMU (cost x 3, 4, 5) has no link to elasticity, competitors or the real cost stack. 03 guesses 40% of startups price by keystone and calls it "probably the worst way". Condition: every new product and every price review. Source: 03 only. Conflict C16. Cards: [9ee62d2b55d0].

**R78. The waterfall: net target + OPEX = CM3 target; add CAC estimate, return and discount allowance, shipping and fulfillment, landed cost; solve for price (F28); then check the market.** Example inputs: 10% net + 10% OPEX = 20% CM3; CAC $30; 3% returns + 3% discounts; shipping and fulfillment $11; COGS $6; price $63.51. Condition: `[needs brand data: CAC for comparable products, courier quote, landed cost]` `[web check: competitor prices]`. Source: 03 only. Cards: [9ee62d2b55d0].

**R79. If the required price is far above market, position as premium where nobody sells a premium version, or do not sell the product.** 03's example: everyone at $30 to $40, required price above that. Condition: after the waterfall. Source: 03 only. Cards: [9ee62d2b55d0].

**R80. After launch, stress-test the price with observed CAC, return rate and fulfillment cost; reprice or discontinue when the margin no longer covers CAC and an overhead share.** 06's closing test: get elements, timing and waste right, then decide make more, reprice, or discontinue. Pricing execution goes to 03-OFF. Condition: 60 to 90 days after launch and at every COGS change. Sources: 03, 06. Cards: [9ee62d2b55d0] [aacabc94746b] [e65733468333].

**R81. Price SKUs, colours and sizes differently; 1 flat price leaves margin on the table.** 02's host found he could charge more with no velocity drop using a price-testing tool. Condition: multi-variant catalogues; test design in 09-CRO. Source: 02 only. Cards: [224e4db9b5c9].

### 3.10 Forecasting

**R82. Forecast new-customer revenue and returning revenue separately, from their own inputs.** New revenue is driven by ad spend and other acquisition actions; returning revenue by launches, promo periods, email and SMS sends and product, with ads adding only a little. 03 calls this the "number one rule" of DTC forecasting. Condition: every forecast. Sources: 03, 02. Cards: [db6a44e073b2] [4870955af64e] [fc4fd43c986c].

**R83. The revenue forecast comes out of the marketing calendar, not a finance extrapolation.** Revenue comes from actions (an ad, a send, a launch, a promo, a PR hit). If last January had a launch and this January does not, do not copy last January. A plan with spend up 50% and CAC flat "is not real". When anyone asks for a higher number, ask which action will be added and what effect it will have. Condition: every plan and every re-forecast. Sources: 02, 03. Cards: [4d4d40fe1138] [15d4d04ea13a] [0d00eb5d6d39].

**R84. Returning revenue: cohort size times repeat rate by age times returning AOV, summed across cohorts (F41); then a 3-year seasonality factor and planned events.** 03 claims about 10% accuracy from the cohort sum and 1 to 2% with seasonality and events (presenter's claim, no data). Condition: needs monthly new-customer counts back to the first data `[needs brand data: cohort repeat curve]`. Sources: 03, 02. Cards: [c87f67f6310b] [fc4fd43c986c].

**R85. New-customer revenue: fit aMER against daily spend on about 1 year of data, excluding sale days, BFCM and days under a realistic minimum spend; read expected aMER at the planned spend; back-solve required spend from the target (F42).** Model what happens to efficiency at 2x spend instead of holding it flat. Condition: `[needs brand data: daily spend and new-customer revenue]`. Sources: 03, 02. Cards: [0d00eb5d6d39] [fc4fd43c986c].

**R86. Regress outliers to the mean and give a range, not a point.** One brand's history is a weak base; 2020 to 2021 misleads; cut data before known structural breaks (iOS 14, tariffs); use comparable brands' curves where possible. Condition: short or broken history. Source: 02 only. Cards: [ac073be6ad16].

**R87. Forecasting is about the gap between the realistic number and the target; name the inputs that close it.** Board wants $50M, model says $40M: list the event, product, channel or creative volume that adds $10M, or accept $40M. Condition: every plan review. Sources: 03, 02. Cards: [0d00eb5d6d39] [15d4d04ea13a].

**R88. Category profits get competed away; do not expect past efficiency back.** With no barriers to entry, competitor supply grows faster than demand (02's supplement brand: alone on its term in 2022, 50 listings now). Growth must come from new products, channels or stories, not a lower CAC line. Condition: any plan that assumes efficiency returns to an earlier year. Source: 02 only. Cards: [15d4d04ea13a] [5e8fb784d881].

**R89. In a planning model, everything flows from ad spend: new customers = spend / CAC; ad spend is the lever for burn, runway and revenue.** Keep inputs in 1 place (blue), formulas separate, a 48-month monthly horizon for an investor model, a catch-all opex line at 10% of revenue, and conservative churn and lifetime orders (upside is a bonus). Condition: any startup or raise model. Source: 01 only. Cards: [563870c81120] [939b20dbac4b] [7b2e56bcad5a] [50708132adc1] [b6fb728dba04].

**R90. Past a scale point (03: about $30K to $40K a day of ad spend, or $20M to $30M revenue) performance returns diminish and brand needs its own P&L line; brand activations will not show direct ROI.** Condition: opinion and anecdote from 1 source; budget size never quantified. Source: 03 only. Cards: [e4043b0af395] [090525149bfe].

### 3.11 OPEX and payroll

**R91. Ecommerce is a low-OPEX game; 02's standard for a great brand is 10 to 12% (elsewhere "closer to 15%"), and the host says over 20% "can't win".** 03 uses 15 to 20% in examples and says the fix is to freeze non-revenue hires, software and office spend. No source gives evidence beyond portfolio opinion. Condition: use as a flag; back-solve the brand's own OPEX line from its net target (F27). Conflict C4. Sources: 02, 03. Cards: [434847dcd5bb] [7c524289c2d3] [4ca15f364bbb].

**R92. Fixed OPEX dollars per day should fall every year, even while scaling, because AI raises output per person; track revenue per employee ($1M to $5M for lean brands, 02).** Condition: opinion from 1 source; a planning lens, not a rule. Source: 02 only. Cards: [434847dcd5bb].

**R93. Size full-time payroll at 12% of the lowest revenue month and cover the rest with flex labour (agencies, freelancers, seasonal hires, offshore, AI).** Examples: lowest month $600,000 gives $72,000 a month. Skips legal, notice, quality and culture costs. Condition: seasonal brands; a planning lens `[needs brand data: monthly revenue and payroll]`. Source: 02 only. Cards: [798f1af7e866].

**R94. Keep payroll models simple: salary / 12 x headcount by 3 to 4 buckets, plus on-costs (25% in the US; swap in the brand's country).** No 700-row payroll tabs. Condition: planning models. Source: 01 only. Cards: [f39ad32b21d7] [66d5d76e9b71].

**R95. Delay heavy people spend until the business can attract and identify great hires; reinvest through marketing first.** 03 also says people are the biggest lever and set the revenue ceiling; the advice is to delay, not to never hire. Condition: 7-figure brands. Source: 03 only. Cards: [7c524289c2d3].

**R96. Run 2 rhythms with 2 owners: 1 person plans the big moment months out, another manages tomorrow.** Daily CM tracking without a long-horizon owner drives short-term over-optimising. Condition: any team above a founder alone. Source: 02 only. Cards: [da68923c4cc5] [709862670eb2].

### 3.12 Cash vs profit: the 3 statements and free cash flow

**R97. Net income is often misleading; free cash flow shows what is really happening.** FCF answers 1 question: once the business has funded 100% of operations and needed investments, is any cash left. 05's model: net income positive all 6 months, FCF positive in only 2. Condition: every monthly close and before any big inventory buy, build or loan. Sources: 05, 01. Cards: [652ee8dcf710] [7404abfd63fa] [8187da83315e].

**R98. The P&L hides 4 cash movements: inventory bought in chunks but expensed when sold; capitalised build cost (depreciated over 36 months for most software, 3 or 5 years for other assets); loan principal (only interest hits the P&L); tax accrued monthly but paid in lumps.** A profitable store losing cash is usually doing 1 of these 4. Condition: any month where profit and cash point different ways. Sources: 05, 01. Cards: [2ff9cc0805c2] [7d9e989e15be] [4f714af151a4] [416bbd9031ed] [cc661026f56a].

**R99. Read the 3 statements together, in order: high-level metrics, income statement, balance sheet (assets = liabilities + equity or the model is wrong), cash flow (operating, investing, financing).** Start operating cash flow from net income and adjust for balance sheet movements (F37). Condition: monthly. Source: 05 only; 01 T5 is the same case. Cards: [6fab761526bc] [059ee049c6fc] [8c56490f81a2].

**R100. Judge operations on free cash flow and solvency on net cash flow.** Whether the business has a loan is a financing choice unrelated to operations; net cash flow tells you whether it can pay its debts and run at the same time. Net cash flow is below FCF only when repaying principal; in a borrowing month it is above. Condition: every cash review. Source: 05 only. Cards: [4f714af151a4].

**R101. Cash can be cut fast only on lines where cash equals expense (payroll, marketing, rent); cutting depreciation releases nothing.** Condition: any cash squeeze. Source: 05 only (card addition, standard accounting). Cards: [b4b11ba26397].

**R102. Inventory on the balance sheet can make a profitable brand cash-negative; assets in ecommerce are mostly unsold stock and cash.** 03's example: $2M profit, $3M of unsold inventory bought, $1M down in cash. Even at $1M to $2M profit the founder may take nothing because it is all in stock. Condition: every close reports inventory value next to profit. Sources: 03, 05, 01. Cards: [69c220a278fc] [beb1703b3d17] [6a8332853dd6].

**R103. Many ecommerce businesses die of liquidity, not unit economics.** "They run out of liquidity and have bad working capital dynamics" (01). Know runway early because raising takes a long time. Condition: any growth plan must carry a cash line and a lowest-cash month. Sources: 01, 03. Cards: [8187da83315e] [def705c265c2] [beb1703b3d17].

**R104. P&L and cash are different games; trade margin for cash on purpose when cash is the priority.** Liquidation, discounts and paying more for longer terms all hurt the P&L and help cash. Growing the bank account is the top priority when funding and M&A are hard (02). Condition: the owner has said cash is the constraint; each trade is written down with its P&L cost. Sources: 02, 03. Cards: [20d195846808] [f2fc5286cc97] [c73b11cb714e] [4d29da5108ca].

### 3.13 Inventory, cash conversion cycle, purchase orders, demand plans and liquidation

**R105. Forecast inventory with lead time and cycle time before you model cash; never let projected inventory go negative.** Roll inventory = prior minus sold plus arrivals, with arrivals lagged by lead time (F35). A negative month is a stockout; move or enlarge the PO. 01's models use 3 to 4 months lead time and a 4-month order cycle. Condition: every PO and every cash plan. Source: 01 only. Cards: [308a0d76128c] [49138d1247d7].

**R106. Use the inventory investment line (units times unit cost, when paid) for cash planning, never per-unit COGS.** COGS matches cost to the sale; cash leaves at deposit and balance dates. Condition: every cash forecast `[needs brand data: supplier deposit and balance terms]`. Sources: 01, 05. Cards: [49138d1247d7] [939b20dbac4b] [6a8332853dd6].

**R107. Target days of inventory equal to production lead time, so a PO placed today lands as you run out.** Grade stock A to D by sell-through or days outstanding; neither source gives day cut-offs `[needs brand data: grade cut-offs]`. Stock far above lead time (02's example 1,000 days; 03's 400 days after a failed launch) is a cash problem. Condition: every SKU, weekly. Sources: 02, 03. Cards: [f2fc5286cc97] [69c220a278fc].

**R108. Hold a weekly inventory and media meeting: days of stock vs lead time vs spend by SKU.** If a top SKU will sell out before restock (02: 30 days of stock, 80-day reorder), raise its ROAS target sharply or pause its ads, and move spend to SKUs with stock, including aged stock. Selling out a hero size or colour mid-flight makes Meta mark the ad a loser and it will not come back on restock. Condition: every week `[needs brand data: days of inventory by SKU, SKU-level spend]`. Source: 02 only; 03 agrees marketing needs the inventory position. Cards: [61a1eefb7db0] [224e4db9b5c9] [4d29da5108ca].

**R109. Every PO should maximise the marginal value of that batch: do not pay high CAC to sell stock that is about to run out, and do not sit on stock with no plan to sell it.** Condition: every PO and every budget move. Source: 02 only. Cards: [61a1eefb7db0] [c73b11cb714e].

**R110. Write a demand plan before any PO: units by channel (existing customers via email and SMS, influencer seeding, paid at a stated efficiency), the media dollars needed for the paid share, wide error bars for a new category, PO timing and cash cycle.** 02's failure: a brand expected $20M from a new SKU with "no idea" of the media needed. Condition: every PO above a routine reorder. Source: 02 only. Cards: [20338553ad10].

**R111. Test demand before a large PO: about 100 units, list, run ads, read efficiency, then order; run 2 supply chains (a fast low-MOQ chain to learn demand, a large-PO chain for proven items); use pre-orders when suppliers will not give terms and demand is already strong.** Condition: new products and new categories. Source: 02 only. Cards: [135d3773766f] [032c38a487a4].

**R112. Liquidate non-moving aged stock and make a new bet, even if you do not need the cash.** Funnel: an unlisted PDP or whitelisted creator page, ads excluding existing customers, deep discount on that page only or full price at lower efficiency (02: core at 2.0 ROAS, liquidation at 1.0 or 0.8; 03: break-even or a slight loss). Other outlets: a narrative discount email, a bulk liquidator, a new country where discounts will not hurt the main market. Judge by cash recovered, not ROAS; keep it separate from profitable acquisition. Condition: grade C and D stock. Sources: 02, 03. Cards: [f2fc5286cc97] [c73b11cb714e] [69c220a278fc] [4d29da5108ca].

**R113. Rotate dated goods nearest-expiry first; log stock in and out; count periodically; fire-sale stock very close to expiry as a last resort.** Recurring count gaps are shrink or process error and feed back into COGS assumptions. Condition: perishable, dated or seasonal goods; the obsolescence part applies to everything. Source: 06 only. Cards: [2d244e2a4df6].

**R114. Rationalise SKU count as new products launch.** Many launches sell 30 to 40% of stock on the initial organic pop and then stall; each failed launch parks cash on the balance sheet. Condition: every launch review. Source: 03 only. Cards: [69c220a278fc].

**R115. The cash conversion cycle, not ad efficiency, often caps growth.** CCC = DIO + DSO minus DPO. Sell 10 units, make $50 GP, buy 11 next; with a 90-day lead time and full payment up front you stock out for 90 days waiting for cash. "You can't triple an ecom business in a year" without multi-million self-funding, outside funding or financing (03's view, no data). Condition: any plan to grow faster than the CCC allows. Sources: 03, 02. Cards: [beb1703b3d17] [377b3fd122bf].

**R116. Fix a CCC squeeze in this order: smaller deposit (03: 20% up front, rest on shipment), shorter lead time (90 to 30 days), longer terms than production plus sell-through (02: 90 days to make, 120-day terms, a negative CCC), consignment, then financing.** Learn each counterpart's cost of capital and trade what they value (a slightly higher unit cost, a longer contract, a bigger commitment) for terms. Condition: every supplier review `[needs brand data: supplier terms and lead times]`. Sources: 03, 02. Cards: [beb1703b3d17] [377b3fd122bf].

**R117. Each new product must solve 1 of 3 problems: margin, volume or cash.** A cash problem with bimodal revenue (winter PO placed in the summer valley) wants a valley product or better terms; a margin problem wants a product that breaks even at 1.4 ROAS instead of 2.0; a volume problem wants a category with rising velocity. Condition: every product idea is scored against the named problem. Source: 02 only. Cards: [9d3c956f2cd5].

**R118. Classify SKUs monthly by volume, revenue, media spent and SKU-level efficiency: champion, hidden gem (high volume, low spend), growth driver (spend and revenue both rising), underperformer (high inventory, low velocity).** Scale hidden gems and growth drivers; turn underperformers to cash. No numeric cut-offs given `[needs brand data: SKU-level spend, units, revenue, stock]`. Condition: monthly. Source: 02 only. Cards: [ca6522622ee6] [8e1550070943].

### 3.14 Financing

**R119. Financing is expensive and risky; slower growth at better efficiency can earn more.** Lenders usually want the founder as collateral; debt bets on selling future units at an efficiency that repays the loan. 03 has seen about 5 times: spend $20K to $200K a month, revenue $2M to $7M, millions in inventory financing, net margin to near 0. Condition: any financing decision; stress-test slower sales before borrowing. Source: 03 only. Cards: [beb1703b3d17].

**R120. Do not sell permanent equity to fund 3 months of inventory.** 01 calls it "absurd" and points to revenue-based financing (Clearco for ecommerce, Pipe for SaaS); note the affiliate link and that terms are historical `[web check: current financing products and terms]`. Condition: short-term working capital needs. Source: 01 only. Cards: [a20812fa24c9].

**R121. Cost-of-capital reference points: credit cards about 30%, merchant cash advance about 70%; Chinese suppliers often have cheaper, subsidised capital.** Use these to decide who should carry the float. Condition: 02's estimates, US context. Source: 02 only. Cards: [377b3fd122bf].

**R122. Keep inventory payments in the cash schedule when modelling financing; treat the financing as a cash inflow and repayments as outflows, never as revenue or as a deleted inventory row.** 01's own model deletes the inventory row and replaces it with a revenue-share repayment; the card's version is the correct accounting. Condition: any financing model. Source: 01 (card correction). Cards: [a20812fa24c9] [59714f58fac1].

**R123. Assume a 7-figure client is using financing; interest alone does not change MER, so model sales and spend separately from debt cost.** Condition: agency or advisor context. Source: 03 (card addition). Cards: [8d570963a07c] [beb1703b3d17].

### 3.15 Scenario analysis and the profit frontier

**R124. Every founder must be able to answer: if we spend an extra $10,000 next month, where does it return the most incremental new-customer revenue, and can $10,000 moved from one channel return more in another.** Push each channel until the marginal dollar makes no more profit (incremental aMER hits break-even), then stop; add tertiary channels only after the 3 primaries hit the frontier. Condition: every budget change; incrementality tests are the only reliable measure, MMM or a +delta test stands in at 7-figure scale. Sources: 03, 02. Cards: [c60eaf1ca845] [35efd9091446].

**R125. A plan with spend up 50% and CAC flat is not real; model efficiency falling with spend (F42).** Condition: every plan. Sources: 02, 03. Cards: [4d4d40fe1138] [0d00eb5d6d39].

**R126. Test CAC and churn sensitivity on every model: what CAC breaks even in month 5 vs month 11, what churn halves LTV.** Condition: every model. Source: 01 only. Cards: [9a3cda2fe90f] [86fcb4012931].

**R127. Compare scenarios on total post-marketing CM at equal spend and on lowest cash month, never on per-customer margin or revenue alone.** Condition: every scenario answer (deliverable 9.3). Sources: 01, 05. Cards: [993ecc7a19f0] [9d2823e98694].

**R128. Put spend where contribution per sale is highest, not where CPA is lowest.** Maximize conversions favours the cheapest-to-acquire product; 03's hoodie made $24 contribution at $45 CPA vs the t-shirt's $12 at $15 CPA. Split campaigns by product economics; if a low-CPA product sells without ads, cut its spend (validate with a holdout). Condition: multi-product accounts; execution in 24-DEP. Source: 03 only. Cards: [3827dc99f5ed] [ac6ec12672a6].

### 3.16 Reconciliation of platform numbers to the books

**R129. The ad account is not the business; paid media must reconcile to the P&L.** If the ad account looks good and the business does not improve, the problem is measurement, margin or cash flow, not ads. Condition: every month. Sources: 03, 02. Cards: [4ca15f364bbb] [d5c2a3d880d9] [25d900c4c527].

**R130. Reconcile 5 gaps every month with a named cause for each (F45): platform net sales vs books revenue; accrued vs processed refunds; platform fees vs fees in the books; platform spend vs marketing in the books; sum of attributed revenue vs actual revenue.** Attribution overlap is expected and is not an error; an unexplained revenue gap is. Condition: monthly close. Sources: 02, 03, 04. Cards: [1d3d04198311] [c9ccfa76430a] [4b0ff6e78865].

**R131. Never compare ROAS across platforms, and never move budget on a raw ROAS gap.** Different attribution windows, funnel positions and incrementality. 03's pattern: TikTok drives impressions, Meta retargets, Google captures the brand search; cutting TikTok on its ROAS kills the top of the funnel. Condition: always; test design in 06-MEA. Sources: 03, 02. Cards: [08a2587ba438] [bc14184eea60] [3929ca774887].

**R132. Calibrate platform numbers with an incrementality factor before comparing them to break-even, and optimise on the platform setting with the tightest link to new-customer revenue (both sources prefer 7-day click without view-through).** Check the link with a daily correlation of 7-day-click ROAS and aMER (02 hopes for about 0.78). Condition: single-channel brands can trust the correlation; multi-channel brands need tests (06-MEA). Sources: 02, 03. Cards: [ccf3794cd11d] [3929ca774887] [de7656f52701].

**R133. When distribution widens (Amazon, retail), widen measurement: 1 engine, 1 blended contribution, not rival .com and Amazon P&Ls.** Measured on .com only, Meta looks worse as Amazon grows and the team cuts spend. Condition: any brand with more than 1 sales channel. Source: 02 only. Cards: [e840728f10ad] [ab546c35c94e].

### 3.17 Subscriptions and churn

**R134. Churn applies only to subscriptions; a one-off store uses cohort retention.** Always state the period (11% monthly and 11% annual are very different). Condition: always. Source: 01 only. Cards: [d4b9ff187dc2].

**R135. Churn denominator is the prior period's subscribers, never this period's total or new signups.** 01's example: 100 prior + 50 new minus 9 cancelled; churn 9%, not 6%. Condition: always. Source: 01 only. Cards: [e587bb652cdc] [1903080a3a75].

**R136. Average lifetime = 1 / churn; use it as a fast fallback, not the real answer, and be conservative (01 uses 25% monthly churn for a subscription box model).** Bands: 25% = 4 months, 20% = 5, 15% = 6.7, 10% = 10, 5% = 20. Annual to monthly conversion has 2 versions (C13). Condition: subscriptions with little cohort data. Source: 01 only. Cards: [fe4a0757982c] [136827bb25c7] [602ada5d7d4a].

**R137. Build separate unit economics for transactional and subscription customers, and expect blended CM percent to fall as the subscription mix rises.** Subscribers have lower AOV and lower margin per order but 3 to 5x revenue per customer (01's opinion). Condition: any subscribe-and-save brand. Source: 01 only. Cards: [17cd13e806d9] [69e7ae8e0048].

**R138. Forecast transactional repeats with a rolling 6-month return rate (3 to 5% of trailing-6-month customers per month in 01's experience).** Condition: non-subscription repeat. Source: 01 only. Cards: [c1e5e9113ebe].

**R139. Treat vendor subscription claims as hypotheses to test: increasing discounts over the lifetime beat flat subscribe-and-save; prepaid lifts LTV "100% or more" and creates negative working capital; defaulting the cart to subscription lifts signups 60 to 70%; about 50% roll off at the end of each prepaid term.** All from Ordergroove with no sample. Default-to-subscription carts carry consent and negative-option billing risk `[web check: auto-renewal consent rules in the brand's market]`. Condition: never cite as fact; 03-OFF holds the offer mechanics. Source: 01 only. Cards: [d8e1973bffac] [013b592e17af] [17cd13e806d9].

**R140. Prepaid is judged on lifetime GP and cash timing, not per-order margin.** 01's example: one-time $54 LTV, 3-order prepaid at 25% off $146, 6-order at 30% off $198; a 10% and 5% mix shift lifts weighted LTV 30%. Condition: model with the brand's own retention `[needs brand data: prepaid retention]`. Source: 01 only (vendor context). Cards: [d8e1973bffac].

**R141. Subscription LTV is checked 2 ways: churn method (GP per order times orders per period / churn) and cohort method (sum of survivors times GP per order / starting customers); they must agree.** 01's coffee case: $92 both ways. Condition: every subscription LTV. Source: 01 only. Cards: [0b060b80b16f] [8b747d69f620].

**R142. Post-advertising CM in a subscription launch may not cover payroll for a year or more; size the raise to the lowest cash month, not to the P&L.** 01's T10: CM covers nothing until month 11, payroll from month 14 to 15; $500,000 raised, about $1.5M needed to reach profitability. Condition: any subscription launch model. Source: 01 only. Cards: [9d2823e98694] [f39ad32b21d7].

## 4. Procedures (implementation)

Each procedure: goal, preconditions, numbered steps, checks, rollback. All calculations call the F formulas; the agent never does arithmetic in prose. Mini playbook numbers in the heading show where the steps come from.

### P1. Build the monthly P&L ladder (03, 01)

Goal: 1 ladder in dollars and percent of net revenue for each month, with the scope of every margin labelled.
Preconditions: gross-to-net data by day, landed cost table (P4), fulfillment cost per order (P5), marketing by type, OPEX by account, accounting policy on variable vs fixed marketing (R27).
Steps:
1. Pull gross revenue (F1), discounts, refunds accrued (F31), chargebacks, shipping collected. Compute net revenue (F2). Exclude sales tax (R2).
2. Compute product COGS (F5) from units sold by SKU times landed cost. Compute CM1 (F8).
3. Compute fulfillment and variable delivery (F6 summed), COD (F7), CM2 (F9).
4. Compute variable marketing per the written convention; CM3 media-only and CM3 loaded (F10).
5. Compute OPEX, EBITDA, interest, tax, D&A, net profit (F11).
6. Add a percent-of-revenue column for every line (F13) and the 4-bucket shares (F12).
7. Add a per-order column (line / orders) and a trailing-3-month per-order column (F13).
8. Set a target per line from the owner's net target and OPEX plan (F27) `[needs brand data: targets]`.
Checks: 4 buckets sum to 100%; rolled-up CM2 percent per segment equals the unit-economics CM2 percent (R32); net revenue ties to the reconciliation (P28); every margin carries its scope label.
Rollback: if landed costs are missing for any SKU, publish the ladder with CM1 marked "unavailable" for that SKU share rather than a guess.

### P2. Build the 4-bucket view and pick the bucket to work on (02)

Goal: 4 totals per month: cost of delivery, CAC (variable media), OPEX, profit.
Preconditions: P1.
Steps:
1. COD = product COGS + fulfillment and variable delivery. CAC bucket = pure variable media; creative only if truly variable; agencies and contractors on retainer go to OPEX (R27).
2. Compute shares (F12). Compare to the reference mix (COD 30 to 40%, CAC 25 to 30%, OPEX 10 to 15%, profit 15 to 20%) and to the 25/25/25/25 picture, remembering that industry average COGS is about 58% (C5).
3. Name the 1 bucket most out of line. Apply the fault rule (R25) to that bucket's lines only.
4. Track net shipping cost (F30) and shipping percent monthly inside the COD bucket.
Checks: the profit share equals EBITDA / net revenue when variable marketing is media only.
Rollback: none; this is a read.

### P3. Classify any cost: statutory COGS, internal COD, variable marketing or OPEX (04, 06, 03)

Goal: every account in the chart of accounts mapped to 1 statutory bucket and 1 internal bucket.
Preconditions: chart of accounts, accounting policy, the accountant's treatment of outbound shipping, packaging and returns `[needs brand data]`.
Steps:
1. Is the cost part of buying the product or getting it onto the shelf ready to sell? Yes: statutory COGS (R11).
2. If unsure: would you have paid it if you had not bought these goods? Yes: expense. No: COGS.
3. Incurred after the sale (delivery, shipping carton, return shipping)? Statutory expense, unless the written policy elects free-shipping or dropship freight into cost of sales (R16, C17). Internal view: COD.
4. Varies with revenue (payment fees, marketplace fees, pick and pack, warehouse staff per order)? Internal COD (R17, R18). Statutory: follow policy.
5. Reduces the price the customer pays (coupon)? Reduces revenue (R19).
6. Marketing, PPC, marketing-only partner revenue share? Variable marketing if it flexes with demand, OPEX if fixed (R20, R27).
7. Return costs: return shipping to overhead; repackaging to make sellable can be COGS; other return handling to expense (R21).
8. Interest: below EBITDA (R26).
9. Write the mapping in the brand record. Do not change it mid-year.
Checks: run checklist 5.3 after mapping.
Rollback: keep the previous mapping version; restate only when the accountant agrees.

### P4. Build the landed cost and COGS table (04, 06)

Goal: landed cost per unit for every SKU, tied to invoices.
Preconditions: POs, supplier invoices, freight and duty invoices, packaging invoices, allocation basis in the policy.
Steps:
1. At PO time record the agreed unit price per SKU.
2. When the supplier invoice arrives, compare it to the PO price. Resolve differences (commodity, currency) before posting.
3. When each freight or duty invoice arrives, link it to its PO(s) the same day. Never file to sort later.
4. Allocate shipment freight and duty across the SKUs in it by the 1 documented basis (F4). Record duty as the amount paid.
5. Split mixed packaging invoices: retail box to product packaging (COGS), shipping carton to fulfillment.
6. Apply supplier discounts to product cost; check credits for a matching stock return.
7. Post purchases to inventory (asset), not to expense; move cost to COGS when units sell (R22) `[web check: inventory and COGS journal steps in Xero, QuickBooks, NetSuite or Tally]` `[verify UI]`.
8. Recalculate landed cost when supplier price, exchange rate or freight changes; version the table with an effective date.
9. Above a few dozen SKUs or several shipments a month, move from a spreadsheet to inventory software and check its totals tie back to invoices.
Checks: sum of allocated freight and duty equals invoice totals; every SKU has purchase price + freight share + duty share + product packaging; the basis is the same across the last 3 shipments.
Rollback: if an allocation basis changes, restate the affected shipments and note it in the close.

### P5. Compute true gross margin (CM2) per basket, SKU and channel (03, 01)

Goal: the margin that sets the CAC ceiling.
Preconditions: P4, fulfillment quotes, fee rates, refund and discount rates by category.
Steps:
1. Price paid by the customer, excluding sales tax.
2. Subtract landed cost per unit times units in the basket (F4, F3).
3. Subtract outbound shipping per order, pick and pack per order, packing materials, storage per order, warehouse staff per order (F6).
4. Subtract payment fee (rate times revenue collected) and, for marketplace orders, the marketplace fee.
5. Subtract a refund and discount allowance per order `[needs brand data: refund rate and average discount by category]`.
6. CM2 basket dollars and percent (F9). Repeat per SKU and per channel (Shopify, Amazon, marketplace).
7. Repeat for new-customer baskets only (F3 aov_new) to get first-order GP for CAC work (R48).
8. Document the definition next to the number.
Checks: compare with the margin the team quotes; if the team's number is CM1, reset marketing budgets and CAC targets off CM2 (R5).
Rollback: none.

### P6. Reclassify warehouse staff into cost of delivery (03)

Goal: gross margin includes the people who fulfill orders.
Steps: 1. Daily cost of each fulfilment staff member. 2. Divide by packages shipped per day (03: $400 / 100 = $4 an order). 3. Bookkeeper tags the staff in the accounting system and builds a custom P&L moving them into COD `[verify UI: Xero or QuickBooks tracking categories]`. 4. Add the per-order figure to F6.
Checks: OPEX falls and COD rises by the same amount; CM2 percent falls.
Rollback: keep the statutory P&L unchanged if the accountant rejects the reclass; apply it in the internal view only.

### P7. Per-order unit economics and the SKU contribution table (01, 03)

Goal: CM2 per order overall, per SKU and per product category, with contribution per sale after CAC.
Preconditions: P1, P5, CAC by product from the scaling campaign (estimate).
Steps:
1. AOV, product COGS per order, fulfillment per order, CM2 per order (F9); trailing 3-month versions (F13).
2. Divide each fulfillment line by revenue to see which charge moved (R9).
3. Per SKU: revenue, units, landed cost, CM1, CM2 per unit and per basket; rank by dollars and by percent (01's SKU A: $92 CM at 40%; SKU B: $74 at 61%).
4. Per product or category: CM2 per order, CAC estimate (campaign CPA), contribution per sale = CM2 minus CAC (F29). Rank by contribution per sale.
5. Flag products whose low CPA hides low contribution, and products that would sell without ads (R128).
6. Add units on hand and days of inventory (F34) so the table also serves P21.
Checks: sum of SKU revenue ties to net revenue; per-order CM2 ties to the ladder.
Deliverable 9.2.

### P8. Compute CAC, 4 ways, and first-order GP (01, 03, 02)

Goal: labelled CAC figures for the period.
Preconditions: new vs returning flag per order `[needs brand data]`, spend by channel, other variable marketing, first-order discounts.
Steps:
1. Count customers whose first order fell in the period (store data, never platform).
2. cac_media = ad spend / new customers. cac_blended = all variable marketing / new customers. cac_loaded adds first-order discount cost. cac_paid = paid spend / paid-attributed new customers (F16).
3. First-order GP = CM2 per new order (P5 step 7).
4. First-order test (F21): CM:CAC and first-order profit for each CAC definition.
5. Break-even ROAS and CAC, and the operating CAC ceiling (F15) using the owner's net target and OPEX (F27).
6. Compare cac_media with the ceiling monthly; a month where CAC exceeds CM2 per new order is a loss month on acquisition (01's July).
Checks: no platform CPA anywhere in the output; every figure labelled.
Rollback: none.

### P9. Build the cohort table: retention, NRR, cumulative GP and LTV (01, 02, 03)

Goal: the source table for LTV, LTGP:CAC, payback and the returning-revenue forecast.
Preconditions: order history with customer id, first-order date, order date, net revenue and CM2 per order.
Steps:
1. Assign each customer to the cohort of their first order month. They never move.
2. Build 3 grids by cohort and month since first order: customers ordering, orders, net revenue. Divide every cell by the original cohort size (F22). Lock the denominator.
3. Retention percent grid; NRR grid; cumulative revenue per customer; cumulative GP per customer (revenue times CM2 percent or summed order-level CM2); orders per customer.
4. Leave future cells empty. The table is a triangle.
5. Read a calendar month diagonally and check the diagonal ties to reported returning orders (01: 122 in June).
6. Compare cohorts at the same age; a cohort far below others (01: January 74% vs July 91%) prompts a question about acquisition source or promo.
7. Take lifetime orders from the cohort with the most history, not an extrapolation.
8. Find the plateau month where cumulative revenue stops rising; that is the brand's LTV window ceiling (R55).
Source: SQL by an analyst, a cohort app, or the analytics tool's cohort report `[verify UI]`.
Checks: month 0 retention is 1.0 everywhere; sum of cohort revenue across a diagonal equals that month's revenue.

### P10. LTGP:CAC in fixed windows (03, 01)

Goal: 30-day, 90-day (and 365-day when acquisition is aggressive) LTGP:CAC for new customers.
Steps: 1. From P9, cumulative GP per customer at 30, 90 and 365 days (F23). 2. Divide by cac_media (03's bands) and by cac_loaded (report both) (F24). 3. Read against the bands (R58). 4. If above 3, run the marginal test (P27) before recommending more spend. 5. If below 1, check first-order GP and COD before calling it a lifetime play (R59).
Checks: the window is printed with every ratio.

### P11. Cohort CAC payback (01)

Goal: months (or orders) to recover the cohort's CAC outlay and the profit tail after.
Steps: 1. Pick 1 cohort of N customers; outlay = N x CAC (F25). 2. Survivors per period from P9; GP per period = survivors x GP per order. 3. Cumulative GP; payback = first period at or above outlay. 4. Report the tail profit to the plateau month. 5. Re-run at CAC plus and minus 25% and at churn plus 5 points (R126). 6. Report the naive figure only as the lower bound (R60).
Checks: payback in orders when customers skip or ship every 2 to 3 months.

### P12. Churn, lifetime and subscription LTV (01)

Goal: churn stated with its period, lifetime, and LTV checked 2 ways.
Steps: 1. Per period: subscribers at end of prior period, new, cancellations. 2. Churn = cancellations / prior-period base (F26). 3. Lifetime = 1 / churn; convert annual to monthly with the stated method (C13). 4. Churn LTV = GP per order x orders per period / churn. 5. Cohort LTV: start 1,000, apply survivorship each period, sum GP, divide by 1,000. 6. The 2 must agree within rounding (01: $92 both ways). 7. Transactional customers: rolling 6-month return rate (F40), not churn.
Checks: the period is printed; no churn figure for a non-subscription store.

### P13. Daily contribution dashboard with returns accrual (02)

Goal: cm3_media by day against a monthly goal, with the hierarchy below it.
Preconditions: daily gross revenue, discounts, shipping collected, orders with new flag, daily ad spend, product cost per order, fulfillment per order, return rate.
Steps:
1. Daily net revenue with refunds accrued at the historical rate (F31), not processed refunds (R41, R42).
2. Daily cm3_media = net revenue minus product COGS minus fulfillment minus ad spend (F10).
3. Monthly CM goal = OPEX plus the profit target (F27); daily pacing line = goal x (day of month / days in month) or the 3-model expectation (F43).
4. Rows below CM: revenue, spend, MER, AOV; then new-customer revenue, aMER, new-customer CM, ad spend; then channel ROAS last (R35).
5. No fixed costs in the daily view (R34).
6. Month end: true up accrued refunds to processed refunds; post the difference to the month.
7. The CEO or CFO keeps a separate rolling 13-week cash forecast (P20); the source gives no template.
Checks: month-to-date cm3_media ties to the monthly ladder within the accrual difference; MER and aMER are period totals, not averaged days.
`[verify UI: Shopify default sales metric]`

### P14. Weekly contribution readout (02, 03, 01)

Goal: the weekly profit memo (deliverable 9.1).
Steps:
1. Week and month-to-date: net revenue, CM2, cm3_media, cm3_loaded, each in dollars, percent of revenue and vs goal.
2. New vs returning split: new-customer revenue, aMER, cac_media, first-order GP, CM:CAC, new-customer count vs goal; returning revenue vs cohort forecast (F41).
3. Variance vs the daily expectation (F43) and the named cause (action added or missed, efficiency, AOV, returns).
4. Fault-rule read (R25): which line above the missed line moved.
5. Inventory line: days of stock on the top 10 SKUs vs lead time; any SKU that will sell out before restock; any C or D stock funnel and its cash recovered.
6. Cash line: cash balance, lowest projected point in the next 13 weeks, tax and PO payments due.
7. Alerts fired (9.4) and the recommended action for each, with the CAC line unchanged unless the owner changes it (R51).
Checks: every number carries its definition label and period.

### P15. Monthly P&L review and constraint diagnosis (03, 01, 02)

Goal: name the 1 constraint the business should work on this month.
Preconditions: P1, P2, targets per line.
Steps:
1. Compare each line's percent to last month, to the trailing 3 months and to target.
2. For any missed line, look only above it (R25): missed EBITDA means OPEX, marketing or COD; missed CM3 means marketing or COD; missed CM2 means COD or revenue (refunds, discounts, shipping collected).
3. Within the failing bucket, find the lever: refund causes by product and cohort, discount code use, shipping pricing, landed cost, pick and pack, fees, media efficiency (aMER), OPEX creep.
4. Check the promo month margin dip is explained by discount, not by cost lines (R10).
5. Read new vs returning profit contribution (R63) and the active customer file (R38).
6. Write the constraint, the lever and the owner in the close pack. Do not cut budgets by reflex.
Checks: 1 constraint named; the recommendation traces to a line above the miss.

### P16. Break-even for any offer: percent off, BOGO, bundle, gift, discount vs CAC grid (03, 01)

Goal: a go or no-go for a discount before it is public.
Preconditions: CM2 percent at the offer price (P5), conversion assumptions by discount level, CPC, ad spend.
Steps:
1. Break-even ROAS and CAC at full price (F15).
2. Repeat at the discounted price with costs unchanged. If break-even ROAS jumps to a level never seen on paid (03: 2.5 to 7), or break-even CAC falls below any observed CAC (03: $10), do not run it publicly (R69).
3. Model the alternative shapes (F19, F20): BOGO or bundle (cost doubles, fulfillment rises about 20%, revenue held), gift with purchase (gift cost vs AOV lift). Compare CM2 and CM3 per order, then multiply by expected promo volume (R70).
4. Run the discount vs CAC grid (F18) at equal spend across 3 discount levels; pick the highest total CM3 within brand limits (R68). Mark the conversion lifts as assumptions and hand the test to 09-CRO (R76).
5. For sitewide sales, add expected cannibalisation of full-price buyers and the lower retention of sale cohorts (R71) `[needs brand data: sale cohort retention]`.
6. Prefer attaching the deepest discount to a loyalty or subscription on-ramp; reserve flat discounts for grade C stock (R72).
7. Never plan "no returns during the promo" (R74).
Checks: every scenario shows CM3 per order and total CM3; the rejected scenarios are kept in the answer.

### P17. Waterfall price for a product (03)

Goal: a price that hits the CM3 target, checked against the market.
Steps: 1. CM3 target percent = net target + OPEX percent (F27). 2. CAC estimate from comparable products `[needs brand data]`. 3. Return and discount allowance percent. 4. Shipping and fulfillment per order from the courier or 3PL quote. 5. Landed cost per unit times expected units per basket. 6. Payment fee rate. 7. Solve price (F28); the denominator must be positive. 8. Check competitor prices `[web check]`. 9. If far above market: premium positioning or do not sell (R79). 10. After launch, re-run with observed CAC, returns and fulfillment (R80).
Checks: contribution at the solved price equals the target within rounding (03's inputs give $63.51 and 20%).

### P18. Forecast: returning revenue, new-customer revenue, daily expectation (03, 02)

Goal: a daily expected revenue line for the month and a monthly plan the team can execute.
Preconditions: P9 cohort curve, 1 year of daily spend and new-customer revenue, dated marketing calendar (launches, promos, sends, seeding, PR).
Steps:
1. Returning revenue by month (F41): cohort size x repeat rate by age x returning AOV, summed; apply the 3-year seasonality factor; add planned events that differ from last year.
2. New-customer revenue (F42): plot aMER vs daily spend, drop sale days, BFCM and days under the minimum spend; fit log or linear; read expected aMER at planned spend; back-solve the spend needed for the target; if that spend is not possible at that efficiency, name the input that beats last year's average (R87).
3. Event effects: overlay every past action on revenue (annotations); measure each event type's effect on efficiency, returning revenue and organic demand; add planned events (02, no maths given).
4. Add the email and SMS send calendar explicitly; returning revenue rises on send days.
5. Sum into a daily expectation (F43). Track actuals daily; act by day 5 (R40).
6. For short or broken history: regress to comparable brands, cut before structural breaks, give a range (R86).
7. Re-forecast when observed CAC or aMER replaces a placeholder (R50).
Checks: new plus returning plus events ties to the monthly plan; every uplift has a named action.
`[needs brand data: 24+ months of monthly spend, new-customer revenue, AOV, cohort revenue by month, dated calendar]`

### P19. Read the 3 statements and reconcile profit to free cash flow (05, 01)

Goal: explain every month where profit and cash point different ways.
Preconditions: monthly P&L, balance sheet and cash flow for at least 6 months.
Steps:
1. Side by side: revenue, net income, FCF, cash balance. Mark months where net income and FCF diverge.
2. Income statement: mark cash-equal lines (payroll, ads, rent, software) and non-cash or mistimed lines (depreciation, product cost, tax accrual). Rising depreciation means asset purchases; an interest line means debt.
3. Balance sheet: assets = liabilities + equity; movements in cash, inventory, receivables, payables, capitalised assets, tax liability, loans.
4. Operating cash flow from net income with the working-capital adjustments (F37); investing (capex, build); FCF; financing; net cash flow equals the change in cash.
5. For each divergent month, rank the drivers by size: inventory build, capitalised development, tax payment, principal repayment. Confirm a planned inventory build has a sell-through timeline; an unplanned one is fixed before the spend repeats. Look at several months, not 1.
6. Confirm FCF definition and capitalisation policy with the accountant `[web check: capitalisation rules and useful-life norms]`.
Checks: net cash flow ties to the bank; FCF sign convention stated (C20).

### P20. Mini cash flow, inventory roll and runway; the 13-week cash forecast (01, 05, 02)

Goal: the lowest cash month and runway, monthly for planning and weekly for the next 13 weeks.
Preconditions: opening cash, forecast orders (P18), landed costs, supplier deposit and balance terms, lead times, OPEX, loan schedule, tax calendar.
Steps:
1. Inventory roll (F35): starting units, forecast units sold, arrivals lagged by lead time; PO sized to cover lead time plus cycle; no negative month.
2. PO cash = units x weighted landed cost, placed on deposit and balance dates.
3. Mini cash flow (F38): opening cash + net income minus inventory paid + product COGS of units sold minus other capex minus principal minus tax paid = closing cash.
4. Find the lowest cash point and runway; test raise or facility timing (01: a $500,000 raise at month 6 was not enough; about $1.5M needed).
5. 13-week version by week: receipts by channel (card payouts, marketplace payout lags), payroll dates, ad platform billing, PO deposits and balances, tax dates, loan dates, rent. Owner: CEO or CFO. The sources give no template; build it from F38 by week.
6. Reserve cash for upcoming tax payments out of spending decisions.
Checks: closing cash of month m equals opening cash of month m+1; inventory never negative; the 13-week and monthly views agree in the overlap.
Rollback: if a PO would push the lowest cash below the buffer, move or split it, or seek terms (P24) before financing.

### P21. Inventory grading, days of inventory and the weekly inventory-media meeting (02, 03)

Goal: spend follows stock.
Steps: 1. Days of inventory per SKU (F34); grade A to D by sell-through or days outstanding `[needs brand data: cut-offs]`; Shopify's inventory ranking can help `[verify UI: Shopify ABC inventory report]`. 2. Compare days of stock with lead time per SKU. 3. Top SKU selling out before restock (30 days of stock, 80-day reorder): raise its ROAS target or pause its ads; move spend to SKUs with stock (R108). 4. C and D stock: open a liquidation funnel (P23). 5. Check whether a winning ad died when a size or colour sold out; relaunch on restock. 6. Update the SKU matrix (R118) monthly. 7. Rationalise SKUs after each launch review (R114).
Checks: no SKU with spend and under lead-time days of stock without a decision; every C or D SKU has a plan.

### P22. Demand plan before a PO (02, 01)

Goal: a PO backed by named demand and the media dollars to create it.
Steps: 1. Units by channel: existing customers (email and SMS), influencer seeding, paid at a stated efficiency (F36). 2. Media dollars for the paid share = units x CAC estimate / conversion to units; wide error bars for a new category. 3. Model PO timing against the cash cycle (P20). 4. Start with a small bet that scales; test demand first where possible (R111). 5. Score the product against the named business problem (R117). 6. Sign-off: owner confirms the media budget exists before the PO is placed.
Checks: the plan states units, dollars, efficiency and error bars; the PO does not exceed inventory the cash plan can carry.

### P23. Liquidation funnel for C and D stock (02, 03)

Goal: turn aged stock into cash without harming core acquisition.
Steps: 1. List SKUs with days outstanding far above lead time. 2. Build an unlisted PDP or whitelisted creator page, not in site navigation. 3. Run ads to it excluding existing customers. 4. Choose: deep discount on that page only, or full price at a lower efficiency target (02: 1.0 or 0.8 ROAS vs 2.0 core; 03: break-even or a slight loss). 5. Other outlets in parallel: a discount email with a narrative if brand-safe; a bulk liquidator; a new country. 6. Report cash recovered, not ROAS; keep the spend in its own line so core aMER is not polluted. 7. Put the cash into a better bet.
Checks: no liquidation spend counted in the acquisition CAC; the SKU's days of inventory falls week over week.

### P24. Fix a cash conversion cycle squeeze and evaluate financing (03, 02, 01)

Goal: shorten the CCC before borrowing; borrow only with a stress test.
Steps: 1. Map lead time, MOQ, deposit and payment terms per supplier; compute CCC (F34). 2. Negotiate a smaller deposit (03: 20% up front, balance on shipment). 3. Find a shorter lead time (90 to 30 days). 4. Ask for terms longer than production plus sell-through (02: 90-day make, 120-day terms), trading a slightly higher unit cost, a longer contract or a bigger commitment; aim at consignment over time. 5. Pre-orders where demand is strong and suppliers will not move. 6. If financing is still needed: compare real quotes, collateral (usually personal), fees; model repayments as cash outflows with inventory payments kept in the schedule (R122); stress-test slower sales and lower efficiency (R119); never fund 3 months of stock with permanent equity (R120) `[web check: current inventory financing terms]`.
Checks: CCC in days before and after; net margin at the stressed case stays above the owner's floor.

### P25. Existing-customer ad budget (03)

Goal: a retargeting budget from customer count, not a percent of spend.
Steps: 1. Count existing customers. 2. Frequency 3 to 6 a month. 3. Existing-customer CPM from the platform's audience segment breakdown `[verify UI: Meta audience segments]`. 4. Budget = customers x frequency x CPM / 1000 (F32). 5. Sanity: 03 says even brands with millions of customers are usually fine at about $10K, up to $30K to $40K a month. 6. Check 7-day frequency on Meta; above 8 means overspending. 7. Report on 7-day click without view-through (R132).
Checks: existing-customer spend is separated from acquisition spend in CAC (R44).

### P26. Payroll sizing by the 12% rule (02, 01)

Goal: a full-time payroll baseline the low month can carry.
Steps: 1. Lowest revenue month of the year. 2. Baseline = 12% of it (F33). 3. Compare to current payroll and on-costs. 4. Move the excess to flex labour (agencies, freelancers, seasonal, offshore, AI). 5. Model payroll as salary / 12 x headcount by 3 to 4 buckets plus on-costs (01). 6. Note the costs the rule skips: legal, notice, quality, culture.
Checks: OPEX percent after the move against the 10 to 15% flag (C4).

### P27. Scenario answer: the next $10,000, spend up 50%, CAC sensitivity, the marginal test (03, 02, 01)

Goal: a written scenario answer (deliverable 9.3) with totals, not per-customer margins.
Steps:
1. State the question and the scenarios (for example: +$10,000 to Meta, to Google, to TikTok; spend +50%; CAC +25%).
2. For each scenario compute: expected aMER from the curve (F42), new customers, new-customer revenue, CM2, cm3_media and cm3_loaded totals, lowest cash month (F38), LTGP:CAC 90-day, payback.
3. Marginal read (F44): incremental new-customer revenue / incremental spend per channel; stop where it hits break-even ROAS; move dollars from the lowest marginal aMER to the highest while both stay above break-even.
4. Where the curve is thin, say so and recommend a +delta test or incrementality test (06-MEA).
5. Compare on total CM3 at equal spend and on lowest cash month (R127); never on revenue alone.
6. Keep the CAC line fixed in the answer unless the owner changes it (R51).
Checks: every scenario carries the same definitions; the rejected scenarios are shown.

### P28. Reconcile platform numbers to the books (02, 03, 04)

Goal: every gap between Shopify, Meta, Google, Amazon, Metabase and the accounting system named and sized.
Preconditions: month closed in the accounting system; platform exports for the same dates and timezone.
Steps:
1. Revenue: platform gross, discounts, refunds processed, shipping collected, tax; books net revenue. Gap causes: tax included, timezone, processed vs accrued refunds, shipping income coded elsewhere, currency, gift cards.
2. Refunds: accrued (F31) vs processed; post the true-up; recompute the return rate.
3. Fees: payment gateway and marketplace fees reported by the platform vs fees in the books; fees must sit in COD internally and follow policy in the statutory view.
4. Marketing: platform spend by channel vs marketing in the books; billing lag and credits are named.
5. Attribution: sum of platform-attributed revenue vs actual revenue; overlap is expected and is reported as a ratio, never as an error.
6. COGS: units sold x landed cost vs COGS posted; inventory movement vs stock adjustments.
7. Write each gap with its cause and whether it recurs; unexplained gaps go to the alert list (9.4).
Checks: net revenue in the ladder equals books net revenue after named adjustments; the daily dashboard month-to-date ties to the close within the accrual difference.
`[verify UI: Shopify reports, Meta Ads Manager export, Amazon settlement reports, Metabase card definitions]`

## 5. Diagnostic checklists

Written so a worker can run them. Each row: what to check | how | good | bad | fix | source.

### 5.1 Monthly close

| what to check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| Gross-to-net bridge complete | Gross, discounts, refunds, chargebacks, shipping collected, tax all present by day | Net revenue derived, tax excluded | Only net from the accounting system | Pull the platform bridge; P1 step 1 | 03, 01 |
| Refunds trued up | Accrued vs processed for the month's sales | Difference posted and explained | Processed refunds used as the month's returns | Post the true-up; recompute rate | 02 |
| COGS booked when sold | Inventory movement vs COGS posted | Units sold x landed cost equals COGS | Purchases posted straight to expense | Stock adjustment; P4 step 7 | 04, 06, 05 |
| Margin labels | Every margin in the pack | CM1, CM2, CM3 named with scope | "Gross margin" with no scope | Relabel; R4 | 01, 03 |
| Variable vs fixed marketing | Marketing accounts vs the written convention | Same as last month | Creative or agency moved buckets | Restore the convention; note any change | 03, 02 |
| Interest placement | Where loan interest sits | Below EBITDA | Inside OPEX | Move it | 03, 05 |
| Warehouse staff | Where fulfilment staff sit | In COD (internal view) | In OPEX | P6 | 03 |
| Fault rule applied | For each missed line, the line above named | 1 constraint, 1 lever, 1 owner | Budget cut with no trace | P15 | 03, 01 |
| 4 buckets | Shares sum to 100% | Yes | No | Fix mapping | 02 |
| Model integrity | Rolled-up CM2 percent vs unit economics; roll-up vs monthly | Equal | Differ | Find the formula error | 01 |
| 3 statements | Assets = liabilities + equity; net cash flow = change in cash | Balances | Does not | Fix before any conclusion | 05 |
| Profit vs cash | Net income, FCF, cash balance side by side | Gaps explained by inventory, capex, tax, principal | Unexplained gap | P19 | 05, 01 |
| Inventory value | Inventory on hand at cost next to profit | Sell-through plan exists | Profit up, cash down, stock up | P20, P23 | 03, 05 |
| New vs returning profit | Contribution by segment | Both positive | New losing with no cohort proof | R53, R57 | 03, 01 |
| Active file | Customers active in the last 6 to 8 months | Growing | Revenue up, new customers down | New-customer goals | 02 |
| Reconciliation | 5 gaps sized and named | All explained | Unexplained revenue gap | P28; alert | 02, 03, 04 |

### 5.2 Weekly contribution readout

| what to check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| Daily CM vs goal | cm3_media month to date vs pacing line | On or above | Behind by day 5 | Adjust spend, sends, promos; P18 step 5 | 02 |
| Returns base | Daily revenue uses accrued returns | Yes | Processed returns (January crash) | F31 | 02 |
| Fixed costs in daily view | Look for daily rent or payroll allocation | None | Negative daily "profit" from spread fixed costs | Remove; monthly view carries OPEX | 02 |
| New vs returning | aMER, new-customer CM, first-order GP, new-customer count | Reported and vs goal | Only MER and ROAS | R37 | 03, 02 |
| CAC vs ceiling | cac_media vs cm2 per new order and the operating ceiling | Below ceiling | Above CM2 per new order | Loss month on acquisition; hold the line, fix creative, offer or COD | 01, 03 |
| MER vs aMER | Same period | aMER above break-even ROAS | MER fine, aMER below break-even | Manage to aMER | 03 |
| Marginal spend | Last spend step's incremental aMER | Above break-even | Below | Cut that step | 03, 02 |
| Frequency on existing customers | Meta 7-day frequency, audience segment spend `[verify UI]` | Under 8; spend near F32 | Over 8; tens of thousands on a small base | P25 | 03 |
| Stock vs spend | Days of stock on top SKUs vs lead time | Spend follows stock | Hero SKU at 30 days stock, 80-day lead, full spend | Raise ROAS target or pause; shift spend | 02 |
| Liquidation line | C and D funnel cash recovered | Rising, separate from core | Mixed into acquisition CAC | Separate line | 02, 03 |
| Cash next 13 weeks | Lowest point, tax and PO dates | Above buffer | Below buffer | P20, P24 | 02, 01 |
| CAC line stability | Was the CAC or ROAS target lowered this week | No | Yes, again | Owner decision only; R51 | 02 |

### 5.3 COGS table audit

| what to check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| Is "gross margin" really product margin | Ask how it was computed | Landed cost, shipping, pick and pack, fees, allowance, tax removed | PO cost only | Rebuild with P5; reset CAC targets | 03, 06 |
| Landed cost per SKU exists | Pick a SKU, ask for the breakdown | Purchase price + freight share + duty share + product packaging | Supplier price only, or a blended guess | P4 | 04 |
| Freight and duty attached | Each freight and duty invoice linked to a PO | All linked | A pile of unmatched invoices | Match now; capture at arrival | 04 |
| Allocation basis consistent | Compare last 3 shipments | Same documented basis | Changes | Fix 1 basis; restate if material | 04 |
| Software ties to invoices | Sum allocated freight and duty vs invoice totals | Match | Gap | Find unallocated or doubled invoices | 04 |
| Packaging split | Packaging invoices | Retail box in COGS, carton in fulfillment | 1 account | Split lines | 04, 06 |
| Fees, ads, outbound shipping, 3PL storage in statutory COGS | Review accounts above gross profit | Only product, freight-in, duty, packaging (plus policy exceptions) | Fees or PPC in COGS | Reclassify per policy | 04, 06 |
| Outbound shipping counted in internal COD | Check F6 | Yes | Missing | Add | 01, 02, 03 |
| Coupons coded as ad spend | Where coupon value lands | Reduces revenue | In advertising or COGS | Reclassify | 04 |
| Returns costs split | Return shipping vs repackaging | Overhead vs COGS by policy | 1 bucket | Split | 04 |
| PO vs invoice price | Compare before posting | Match or explained | Unchecked | Resolve with supplier | 04 |
| Supplier discounts and credits | Where they land | Against product cost; credits checked for stock returns | In other income | Reclassify | 04 |
| Waste and shrink | Expiry list; counts vs logs | Nearest date ships first; counts match | Long-dated ships first; gaps | Rotate; count; investigate | 06 |
| Margin band sanity | CM1 and CM2 vs the bands in section 6 | Inside or explained | Far outside | Look for misclassification or a low price; not a target | 06, 02 |
| Recalculated on change | Last landed cost effective date vs last price, FX or freight change | Current | Stale | Recalculate; version | 04 |

### 5.4 Platform-to-P&L reconciliation

| what to check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| Revenue basis | Platform "total sales" vs order revenue vs books | Order revenue, tax excluded, accrued returns for management | Total sales with processed returns as the efficiency base | F31; P28 step 1 `[verify UI]` | 02 |
| Same dates and timezone | Export settings | Match | Off by a day at month end | Align; re-export | 02, 03 |
| Refund timing | Accrued vs processed | True-up posted | December returns in January's rate | F31 | 02 |
| Shipping income | Where shipping collected sits | In the gross-to-net bridge | Missing or in other income | Reclassify | 03, 04 |
| Fees | Platform fee report vs books | Equal, in COD internally | Fees missing or in OPEX | Reclassify; C1 | 03, 04 |
| Spend | Platform spend vs marketing in books | Equal after billing lag | Unexplained gap | Trace invoices and credits | 02 |
| Attribution overlap | Sum of attributed revenue / actual revenue | Reported as a ratio | Treated as revenue | Never sum platform revenue into the P&L | 02, 03 |
| CAC source | New customers from the store | Yes | Platform CPA | R44 | 03, 01 |
| Attribution setting | Meta setting used for reporting | 7-day click, no view-through | 7-day click 1-day view or wider | R132 `[verify UI]` | 02, 03 |
| Cross-channel effects | Trend of .com efficiency vs Amazon or retail growth | Both measured | .com falls while Amazon grows, spend cut | Holdout on .com plus Amazon before cutting; R133 | 02 |
| COGS tie | Units sold x landed cost vs COGS posted | Equal | Differ | Stock adjustment or cost table error | 04, 06 |

### 5.5 Cash and inventory check

| what to check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| FCF vs net income | 6+ months side by side | Move together or gaps explained | Profit positive, cash falling, unexplained | P19 | 05, 01 |
| Inventory swing | Month-on-month inventory balance | Build matches a sell-through plan | Repeated builds, no plan | P20, P22 | 05, 03 |
| Hidden investment | Capitalised assets vs depreciation | Spend budgeted as cash | Cash far above depreciation, unbudgeted | Budget on cash | 05 |
| Tax lumps | Tax liability build and payment dates | Cash reserved | Payment month surprises | Reserve monthly `[web check: calendar]` | 05, 01 |
| Debt | Interest line, loan balance, financing section | Repayments fit inside FCF | Net cash flow negative because principal exceeds FCF | Model principal before drawing more | 05 |
| Runway | Cash by month | Lowest point above buffer | Negative before next raise or facility | Raise earlier, finance inventory, or slow the PO | 01 |
| Inventory cover | Projected inventory by month | Never negative | A negative month | Move or enlarge the PO | 01 |
| Days of inventory | Per SKU vs lead time | Near lead time | Hundreds or 1,000 days | Grade; liquidate C and D | 02, 03 |
| CCC | DIO + DSO minus DPO; supplier terms | Shrinking or negative | 90-day up-front payment and stockouts | P24 | 03, 02 |
| Cash play or P&L play | Owner's stated constraint; inventory vs profit; debt trend | Named and consistent | Profit on paper, cash falling, interest rising while MER falls | Slow growth to a better MER; P24 | 03 |
| Cutting media in a squeeze | Does media drive revenue; share of C and D stock | Ring-fenced clearance spend at break-even, judged on cash | Reflex 40% cut, revenue falls, more cuts | C6 rule in section 7 | 03, 02 |
| Financing stress test | Slower sales and lower efficiency case | Net margin above floor | Near 0 | Do not borrow; P24 | 03 |

### 5.6 Pre-PO demand check

| what to check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| Demand plan written | Units by channel with efficiency and error bars | Yes | Revenue target only | P22 | 02 |
| Media dollars for the paid share | Units x CAC / conversion to units | Budget exists and is approved | "No idea" of media needed | Size or shrink the PO | 02 |
| New category error bars | Range on CAC estimate | Wide, stated | Point estimate | Widen; small first bet | 02 |
| Demand tested | Small batch or pre-order result | Sell-through signal set and met | None | Test first; R111 | 02 |
| Inventory roll | Arrivals lagged by lead time; no negative month | Yes | Stockout or overbuild | F35 | 01 |
| Days of inventory after arrival | Units on hand plus PO / daily sales | Near lead time | Far above | Cut the PO | 02 |
| Cash at deposit and balance dates | 13-week and monthly cash | Above buffer | Below | Terms, split PO, or delay; P24 | 01, 03 |
| CCC effect | DIO after the PO; supplier terms | Terms longer than production plus sell-through | Full payment up front | Negotiate deposit and terms | 02, 03 |
| Problem solved | Margin, volume or cash named | Yes | "Cool product" | Score against the problem; R117 | 02 |
| SKU rationalisation | Which SKU leaves when this one lands | Named | None | R114 | 03 |
| Landed cost known | P4 for the new SKU including freight, duty, packaging | Yes | Supplier price only | P4; P17 | 04, 03 |
| Price passes the waterfall | F28 vs market | Yes | Required price far above market and no premium story | Do not sell; R79 | 03 |

### 5.7 CAC honesty check

| what to check | how | good | bad | fix | source |
|---|---|---|---|---|---|
| Denominator | New customers from the store | Yes | All orders, or platform CPA | R44 | 01, 03 |
| Label | Which of the 4 CACs | Stated | "CAC" alone | R45 | 01, 02, 03 |
| Paired with | First-order GP of new customers | Yes | Blended AOV x blended margin | R48 | 03 |
| Paid vs blended | Both reported | Yes | Blended only while organic is friends and family | R47 | 01 |
| Discount cost | First-order discounts in the loaded CAC | Yes | Ignored | F16, R67 | 01 |
| Channel CAC in the P&L | Search for per-channel CAC lines | None | Present | Move to planning estimates | 03 |
| LTV window | Every LTV or LTGP carries its window | Yes | Open-ended | R55 | 03, 01 |
| Payback method | Cohort | Yes | CAC / monthly GP | R60 | 01 |

## 6. Thresholds and benchmarks

All values are flags, not targets, unless the brand's own data confirms them. Confidence: how many independent sources agree and on what basis. US and Australian context unless noted.

| metric | value | condition | source | confidence |
|---|---|---|---|---|
| CAC denominator | New customers only, from the store | Always | 01, 02, 03 | 3 sources agree, definition |
| LTV base | Lifetime gross profit or CM2, never revenue | Always | 01, 03 | 2 sources agree |
| First-order CM:CAC | At or above 1 | Default gate; buy-once categories must | 01, 03 | 2 sources, opinion; exception with cohort proof |
| First-order CM:CAC, exceptional stores | 3 to 5x | Late stage, high margin | 01 | 1 source, opinion |
| First-order GP | Under about $70 "probably a problem" | Paid acquisition at scale | 03 | 1 source, opinion |
| LTGP:CAC below 1 | Losing on acquisition | 30 or 90 day | 03; 01 agrees below 1 is "upside down" | 2 sources agree |
| LTGP:CAC 1 to 2 | Generally not good | Only CPG with excellent retention or funded growth | 03 | 1 source; 01 accepted 1.09 as a start with a path to 2 |
| LTGP:CAC or LTV:CAC 2 to 3 | Optimal, scale | 30 or 90 day (03); subscription box (01) | 03, 01 | 2 sources agree on the band |
| LTGP:CAC above 3 | 03: mistake, underspending; 01: 5+ late stage is healthy; common advice: 3:1 healthy | See C3 | 03 vs 01 | Conflict; 1 source each |
| CAC for the bottom of the optimal band | First-order GP / 2 | Example | 03 | 1 source, arithmetic |
| LTV and LTGP windows | 30 and 90 days for efficiency; 90 or 180 for value; 365 when aggressive; plateau month as the ceiling | Every LTV figure | 03, 01 | 2 sources, compatible (C10) |
| Short LTV window | 60 to 90 days understates long-cycle products | Gifting, long repurchase cycles | 01 | 1 source |
| CAC payback window | 3 to 6 months (agency, CPG, fashion, retail) | Outer limit unless cash allows | 03; 02 says match the cash reserve | 2 sources, opinion |
| Payback error | Naive payback understates by 20 to 100%, sometimes 200% | Not cohortised | 01 | 1 source, experience |
| Lapse window | 80% of returners come back within 6 to 8 months | Most brands | 02 | 1 source, portfolio |
| Returns and refunds | 5 to 10% of gross revenue | Many verticals | 01 | 1 source, opinion |
| Refund model inputs | 4 to 5% of order revenue | Model inputs | 01 | 1 source |
| Fashion refund rate | About 10% standard; 10% up to 80% seen | Fashion | 03 | 1 source, agency experience |
| Returns accrual example | 10% | Example only | 02 | 1 source |
| Payment fees | About 3% (US); 2.75% in models | US card processing | 01, 03 (3% in example) | 2 sources, US |
| Product cost | 10 to 20% of revenue | "Most brands" | 02 | 1 source, observation |
| Shipping | About 10% of revenue or less; 10 to 20% seen; 20 to 30% red flag | Any | 02 | 1 source |
| Cost of delivery | 30 to 40% of revenue | "Then it is not the biggest problem" | 02 | 1 source, opinion; conflicts with its own 58% average (C5) |
| Industry gross margin | About 42% (COGS about 58%) | Industry average | 02 (Finaloop study) | 1 study cited, no method given |
| CPG gross margin | 20 to 40% "typically"; baby food about 30% | Physical product makers | 06 | 1 source, rule of thumb; DTC often higher |
| SaaS gross margin | 70 to 90% | Software | 06 | 1 source; not ecommerce |
| Supplements gross margin | 50 to 70% | Supplements | 01 | 1 source, opinion |
| Fulfillment share | 30 to 32% of revenue (T2 case); about 50% CM2 (T7 case) | Case examples | 01 | Examples only |
| CAC bucket | 25 to 30% of revenue | Strong ecommerce business | 02 | 1 source |
| Marketing % of revenue | 40 to 50% low-LTV hard goods; about 50% Ridge; about 10% legacy retailers | Depends on LTV and stage | 02 | 1 source, portfolio |
| Marketing % at a true 70% CM2 | 20 to 25% | Only if 70% is real gross margin | 03 | 1 source, opinion |
| Median new-customer Meta ROAS | About 1.7 (acquisition cost about 55 to 60% of new-customer revenue) | CTC portfolio, US, 2025 to 2026 | 02 | 1 source, portfolio |
| OPEX | 10 to 12% (also "closer to 15%"); host: over 20% "can't win" | Great ecommerce business | 02 | 1 source, opinion (C4) |
| OPEX in examples | 10 to 20% | Worked examples | 03 | Examples |
| Profit | 15 to 20% "killing it"; 20% net "healthy" | Ecommerce | 02, 03 | 2 sources, opinion |
| Payroll baseline | 12% of the lowest revenue month | Seasonal brands | 02 | 1 source, heuristic |
| Payroll on-costs | 25% of salary | US: healthcare, payroll tax, 401k | 01 | 1 source, US |
| Revenue per employee | $1M to $5M | Lean AI-enabled brands | 02 | 1 source |
| Unknown opex bucket | 10% of revenue | Planning model | 01 | 1 source |
| Units per transaction | 1.1 to 1.3 (01); 1.5 to 1.7 (03) | DTC baskets | 01, 03 | 2 sources, different ranges |
| Existing-customer frequency | 3 to 6 a month target; over 8 in 7 days is overspending | Meta | 03 | 1 source (unit slip noted) |
| Existing-customer spend | About $10K, up to $30K to $40K a month | Brands with millions of customers | 03 | 1 source |
| Meta attribution for reporting | 7-day click, no view-through | Optimisation and reporting | 02, 03 | 2 sources agree |
| ROAS to aMER correlation | About 0.78 hoped | Single-channel Meta brand | 02 | 1 source (transcript "7.8") |
| Break-even ROAS | 1 / CM2 percent | Excludes OPEX and profit | 03; 01 equivalent | 2 sources, arithmetic |
| Discount example | 30% off took break-even ROAS 2.5 to 7 | Costs unchanged | 03 (corrected) | Arithmetic |
| Bundle of 2 fulfillment lift | About 20% | General | 03 | 1 source, opinion |
| Black Friday conversion | 4 to 5% from 1.75% | Big list, promo | 01 | 1 source, "normal" |
| Days of inventory target | Equal to production lead time | Just in time | 02 | 1 source |
| Aged stock flags | 400 days (failed launch), 1,000 days | Examples | 03, 02 | Examples |
| Liquidation efficiency | 1.0 or 0.8 ROAS vs 2.0 core; break-even or slight loss | Grade C and D stock | 02, 03 | 2 sources agree on direction |
| Failed launch pattern | 30 to 40% sell-through then stall | Typical failed launch | 03 | 1 source, opinion |
| Stock-out rule | 30 days of stock vs 80-day reorder: raise ROAS target or pause | Best SKUs | 02 | 1 source, example |
| Small batch test | About 100 units; live in 72 hours | Test chain | 02 (ColourPop) | 1 source, example |
| Supplier deposit | 20% up front, rest on shipment | Negotiation example | 03 | 1 source, example |
| Terms target | Terms longer than production plus sell-through (90-day make, 120-day terms) | Negative CCC | 02 | 1 source, example |
| Cost of capital | Credit cards about 30%; MCA about 70% | Small brands, US | 02 | 1 source, estimate |
| Software useful life | 36 months "for most software"; other assets 3 or 5 years | Depends on policy | 05, 01 (same presenter) | 1 presenter |
| Tax rate in models | 25%, paid quarterly | Illustrative, US | 05, 01 | Illustrative only `[web check]` |
| Subscription churn | 25% monthly "common"; use it to be conservative | Subscription box models | 01 | 1 source, opinion |
| Churn lifetime bands | 25% = 4 months; 20% = 5; 15% = 6.7; 10% = 10; 5% = 20; 40% annual = 30 months (or 24 by survival) | Constant churn | 01 | Arithmetic; C13 |
| Transactional return rate | 3 to 5% of trailing-6-month customers per month | Non-subscription repeat | 01 | 1 source, experience |
| One-time buyer retention | About 10% reach order 2, 5% order 3, 3% order 4; 1.2 orders in year 1 | Vendor example | 01 (Ordergroove) | Vendor claim |
| Subscriptions vs one-time | 3 to 5x revenue per customer | Usual | 01 | 1 source, opinion |
| Default cart to subscription | +60 to 70% signups | Vendor data, no sample | 01 | Vendor claim |
| Prepaid vs flat 20% subscribe and save | About 2.5x lifetime spend; 50% roll off per term | Vendor data | 01 | Vendor claim |
| Amazon FBA fees | About 20 to 25% of revenue (referral fee omitted) | Depends on size and weight | 01 | 1 source `[web check]` |
| Regression data | About 1 year of daily points, minus sale days, BFCM, days under $1,000 spend | New-customer forecast | 03 | 1 source (unit slip noted) |
| Returning forecast accuracy | About 10%; 1 to 2% with seasonality and events | Cohort method | 03 | 1 source, claim |
| Forecast accuracy (agency) | $3B within 4% of target | CTC portfolio | 02 | Own claim |
| Detect a miss | By day 5, not day 22 | Monthly targets | 02 | 1 source, opinion |
| Performance-only growth range | About $1M to $20M revenue; plateau at $30K to $40K a day | Opinion | 03 | 1 source |
| Incrementality testing needed | Top 20% of brands, "over $10M a month" (may mean a year), multi-market or omnichannel | Heuristic | 03 | 1 source; unit unclear |
| Wasted spend 2021 | 60% of media dollars never paid back | One partner analysis | 02 | 1 analysis, no method |
| Cash forecast | Rolling 13 weeks, owned by CEO or CFO | Always | 02 | 1 source, practice |
| VC model horizon | 48 months, monthly | Investor model | 01 | 1 source |

## 7. Where sources disagree

Each conflict: what each side says, when each is right, what the agent should do.

**C1. What belongs in COGS: outbound shipping, payment and marketplace fees, pick and pack, 3PL storage.**
- 04 and 06 (accountants): statutory COGS is only the cost to get goods onto the shelf. Outbound shipping, the shipping carton, Amazon and Shopify fees, PPC, 3PL storage and shipping charges are expenses below gross profit. 04 allows 2 hedged exceptions: free shipping built into the price, and dropship freight charged by the supplier. 06 sees freight-out in COGS "often" and calls it a mistake.
- 01, 02 and 03 (operators and agencies): cost of delivery includes outbound shipping, pick and pack, packing materials, 3PL, storage, payment fees (03 calls fees in OPEX "a mistake"), and 03 adds warehouse staff per order. The margin after all of these is the one that sets the CAC ceiling.
- When each is right: 04 and 06 for statutory and compliance accounts and for period-to-period comparability of gross profit. 01 to 03 for every marketing, pricing and CAC decision, because those costs vary with every order.
- What the agent does: keep 2 views (R12). Statutory COGS follows the written policy (P3). Internal COD always includes every variable delivery cost (F6, F7). Every margin carries its scope label. The CAC ceiling uses CM2 on the internal view, never statutory gross profit. `[web check: US GAAP ASC 606 shipping and handling election; IAS 2; Ind AS 2 for Indian brands]`

**C2. CAC: media-only or fully loaded.**
- 02: the CAC bucket is pure variable media; agencies, contractors and fixed creative go to OPEX. 03: CAC = total ad spend / new customers; variable creative and agency help sit in variable marketing but its CAC formula uses ad spend.
- 01: blended CAC = total marketing (paid ads, influencers, agencies, other marketing) / new customer orders, and the first-order discount is the same money as CAC.
- When each is right: media-only for daily steering and the spend-vs-aMER curve, because only media moves daily and its efficiency is what the curve models. Fully loaded for payback, LTGP:CAC, the pricing waterfall and any "did this customer pay back" question, because the customer had to cover all of it.
- What the agent does: compute and label 4 CACs (F16, R45). Reports show cac_media and cac_loaded side by side. The 4-bucket CAC share uses whatever the written convention says and states it (F12).

**C3. LTV:CAC bands: 3:1, first-order GP:CAC, or "above 3 means underspending".**
- 01: first-order CM:CAC at or above 1 is the main gate; LTV:CAC 1.0 is not acceptable; 2 to 3 or above to grow profitably (subscription box); 5+ (6.7) at late stage on the optimal path; exceptional stores 3 to 5x on the first order.
- 03: LTGP:CAC in a fixed 30 or 90 day window; below 1 losing; 1 to 2 generally not good; 2 to 3 optimal; above 3 a mistake, under-using paid media; the bottom of the optimal band is first-order GP / 2.
- Common advice (named by both): 3:1 healthy, with an open-ended LTV.
- When each is right: 03's "above 3 is a mistake" holds when the marginal dollar still returns above break-even and the brand has cash to carry payback; 01's 5+ holds when growth is limited by supply, brand or category saturation (02's R88) and forcing spend would buy negative marginal customers. The 3:1 rule of thumb is only meaningful with a stated window.
- What the agent does: gate on first-order CM2:CAC (R53); scale on windowed LTGP:CAC in the 2 to 3 band; when the ratio is above 3, run the marginal test (F44, P27) and raise spend only if incremental aMER stays above break-even and the 13-week cash forecast carries the payback; never report an open-ended ratio (R58).

**C4. OPEX targets.**
- 02: 10 to 12% now (was 25, 20, 15), "closer to 15%" in another passage; host: over 20% "can't win", heading to 3%.
- 03: examples at 10 to 20%; no universal target; reinvest through marketing, not headcount; people are also the biggest lever, so delay rather than never hire.
- 01: no target; OPEX is a plan (payroll buckets, software, a 10% unknown bucket) and the P&L must clear it.
- When each is right: 02's band describes lean US Meta-first brands in 2025 to 2026; a brand with owned fulfilment, retail or a large creative team will sit higher and may be right to.
- What the agent does: back-solve the brand's OPEX line from its net target (F27); flag OPEX above 15% and rising as a percent while revenue grows (R28, R91); never call 10 to 12% a target without the owner's agreement.

**C5. Cost of delivery percentages.**
- 02: 30 to 40% of revenue for a strong brand; product cost 10 to 20%; shipping about 10% or less. The same speaker cites an industry average gross margin of about 42% (COGS 58%) and says "COGS are probably 60% or 40%".
- 01 cases: T2 product 18% plus fulfillment 30 to 32% = about 50%; T7 CM2 a little under 50%. 06: CPG gross margin 20 to 40% (COD 60 to 80%). 03 examples: COD 30 to 40%.
- When each is right: category decides. Jewellery, supplements and perfume have low value-to-weight cost; coolers and art have high shipping share.
- What the agent does: report the brand's COD share against its own history and category `[web check: gross margin ranges by category]`; use 30 to 40% as a flag that COD "is not the biggest problem", never as a target (R24).

**C6. Raise ad spend in a cash squeeze.**
- 03: when November stock is unsold in February and the CFO proposes a 40% media cut, raise marketing from 30% to 35% of revenue short term, with the extra 5% only for clearing C and D stock; cutting media drops revenue and starts a spiral.
- 02: liquidate aged stock through its own funnel at 1.0 or 0.8 ROAS, cut spend on SKUs about to run out, hold the CAC line, and prioritise the bank account. 01: do not scale spend to fix bad unit economics; know runway. 05: judge on free cash flow.
- When each is right: 03's move works only when media demonstrably drives revenue and the extra spend converts C and D stock into cash faster than it burns cash. 01 and 02 are right when the problem is unit economics or when the cash forecast cannot fund the spend before the cash comes back.
- What the agent does: allow a spend increase in a squeeze only if all 5 hold: media drives revenue (aMER above break-even on the clearance funnel), the stock is grade C or D, the spend is ring-fenced in its own funnel line at break-even or a stated slight loss, success is judged on cash recovered per week, and the 13-week cash forecast shows the brand can fund the spend until the cash returns. Otherwise, hold or cut. Write the P&L cost of the trade down (R104).

**C7. "Never turn off an ad."**
- 02: a one-line quick answer with no reasoning.
- 02 itself: pause ads on a hero SKU about to stock out; cut spend past the marginal frontier. 03: stop paying to advertise a product that sells without ads (validate with a holdout); pull spend from products with low contribution per sale.
- What the agent does: ignore the one-liner. Pause or cut when the SKU will stock out before restock, when the marginal dollar is below break-even, or when a holdout shows the sales were not incremental. Creative-level pausing rules live in 24-DEP.

**C8. Judge health by free cash flow, profit or ROAS.**
- 05 and 01: net income misleads; free cash flow is the check; a profitable store can run out of cash.
- 02: cash flow at the top for the CEO, daily contribution margin for the team, channel ROAS at the bottom. 03: contribution margin (CM3) is the best index over time; ROAS is a within-platform read only; know whether you are in a cash play or a P&L play.
- No source says ROAS measures health; all 3 that mention it warn against it.
- What the agent does: 1 hierarchy (R35): cash (13-week forecast, FCF, lowest cash month) for the owner; cm3 daily for the team; net profit and the ladder monthly; aMER and LTGP:CAC for acquisition; platform ROAS only as a directional within-platform read, calibrated by an incrementality factor where one exists. Alerts fire on divergence (9.4): profit up and cash down, or CM up and new-customer file down.

**C9. Break even on the first order, or lose early and earn later.**
- 01 (T3, T4, T7): break even or better on order 1; Black Friday buyers especially. 01 (T12, T14, T16): accepts CAC well above first-order GP when the cohort tail repays it. 03: first-order GP is the anchor; most brands that lose on acquisition lack the retention to support it; CPG can run a 3 to 6 month payback.
- When each is right: the repeat rate decides. Buy-once categories must pass the first-order gate; consumables with a proven cohort tail may not.
- What the agent does: R53 as the default; R57 as the exception, only with a cohort of at least 6 months showing cumulative GP above CAC and cash to carry the payback window.

**C10. LTV window.**
- 03: 90 or 180 days for customer value; 30 and 90 days for LTGP:CAC; 365 only when aggressive. 01: find the plateau in cumulative cohort revenue (about 12 months at 25% monthly churn); 60 to 90 days understates long-cycle and gifting products.
- Not a method conflict. What the agent does: every LTV figure carries its window; efficiency targets use 30 and 90 days; the brand's plateau month sets the longest window used; long-cycle products extend the window and say so (R55).

**C11. Margin names.**
- 01 T7: gross margin = revenue minus product cost; contribution margin = minus fulfillment too. 01 T8 to T10: gross profit, gross margin and contribution margin "all mean the same thing" and already include fulfillment. 03: CM1 product margin, CM2 gross margin (after all COD), CM3 contribution after marketing. 02: CM = net sales minus product cost minus variable expense minus ad spend (03's CM3 with media only).
- What the agent does: the ecomOS names are CM1, CM2, CM3 media-only, CM3 loaded (F8 to F10). When reading any source number, check which costs it subtracts before using it.

**C12. Discounts are CAC vs discounts erode margin and brand.**
- 01: a discount and CAC are the same money; the biggest discount can produce the most total profit (grid: $25,000 to $63,000 post-marketing CM at equal spend); the brand caveat is stated.
- 03: recalculate break-even before any public discount; a 30% discount can make the required ROAS impossible; prefer bundles and gifts; flat discounts are for grade C stock. 01 (T3) agrees on the promo shapes. 02: liquidation discounts hurt the P&L and help cash, on purpose.
- Not a real conflict once the condition is stated. What the agent does: model every discount through both lenses: the pool (F18) for total CM3 at equal spend, and break-even (F15) at the discounted price. A discount passes only if total CM3 rises and the required efficiency has been observed on paid before. Conversion lift is a test, not an assumption (R76).

**C13. Annual to monthly churn.**
- 01's presenter: 40% annual = 2.5 years = 30 months (lifetime = 1 / annual churn, in years). Card [602ada5d7d4a]: monthly = 1 minus (1 minus annual) ^ (1/12) = 4.17%, lifetime about 24 months.
- What the agent does: use the survival conversion (F26) in code, state it, and show the simple version only for comparison with the source.

**C14. Tax in the gross margin example.**
- 03's transcript: $100 price, $76 of costs including $9 tax, margin 24%. Card: tax removed from revenue, $91 revenue, $24 contribution, 26.4%.
- What the agent does: remove pass-through tax from revenue (R2), so 26.4% is the ecomOS answer; never count tax as a cost.

**C15. Returns: accrue monthly or restate later.**
- 02's guest: a daily accrual at the historical rate with a month-end true-up. 02's host: restate December about 6 weeks later when the return window closes.
- What the agent does: accrue daily (F31) for management reads and true up at month end; restate the prior month in the close pack when the return window is longer than a month `[needs brand data: return window by category]`.

**C16. Keystone pricing.**
- 03: keystone is "probably the worst way you could ever price". Many retail guides teach keystone as a floor.
- What the agent does: price with the waterfall (P17); keystone may appear only as a sanity floor for wholesale, never as the DTC method.

**C17. Free shipping as COGS.**
- 04: outbound shipping "could be considered" COGS when shipping is built into the price, or under dropship. Its own card and 06 say classification follows policy, not whether the customer paid a shipping line.
- What the agent does: statutory treatment follows the written policy and the accountant `[web check: standard]`; the internal view includes outbound shipping in every case.

**C18. Who owns the forecast.**
- 02: marketing should own the consumer forecast because revenue comes from marketing actions; a finance extrapolation "is not real". 03: forecasting is finance-grade work from cohort curves and spend regressions.
- Not a real conflict: both build from inputs, not from last year's line. What the agent does: build the forecast from the cohort curve, the spend curve and the dated calendar (P18); the owner names the accountable person.

**C19. Statutory vs internal COGS for KPIs.**
- 04: statutory COGS and internal KPIs (contribution margin, returns cost) can differ, especially in apparel; do not force every internal view into 1 COGS number. 01 to 03 run the business on the internal view.
- What the agent does: as C1; the close pack shows both and the bridge between them.

**C20. Free cash flow sign convention.**
- 05's transcript: "operating cash flow minus investing cash flow". Investing cash flow is usually negative, so the literal arithmetic adds it back.
- What the agent does: FCF = operating cash flow minus capex as a positive number (F37), definition stated in every report.

**C21. Payback windows.**
- 03: agencies and CPG, fashion and retail run 3 to 6 months. 01: cohort payback took 8 months in its box example and 9 months in the SaaS example, and real payback runs far longer than the naive figure. 02: match the payback horizon to the cash reserve.
- What the agent does: compute cohort payback (P11); set the acceptable window with the owner from the cash reserve, with 3 to 6 months as the default outer limit (R62).

## 8. Common mistakes

Merged from all 6 sources, deduplicated, with the fix.

**Definitions and margins**
1. Quoting product margin (CM1) as gross margin and setting marketing budgets off it. Fix: P5, R5. (03, 06)
2. Using "gross margin" and "contribution margin" without saying which costs are subtracted. Fix: R4, F8 to F10. (01, 03)
3. Counting pass-through sales tax in revenue or as a cost. Fix: R2. (03)
4. Reading only net revenue and missing refund, discount and shipping-collected levers. Fix: R1, R3. (03)
5. Computing unit economics per unit when baskets carry more than 1 unit. Fix: R8. (01, 03)
6. Lumping product and fulfillment into 1 COGS line so nobody sees which cost moved. Fix: R13. (01)

**COGS and classification**
7. Purchase invoices posted as expense with no stock adjustment; no COGS at all. Fix: R22, P4 step 7. (04)
8. Freight and duty never allocated to units; a pile of unmatched invoices. Fix: R14, P4. (04, 06)
9. Inbound freight expensed separately while outbound shipping sits in statutory COGS. Fix: R16, P3. (04, 06)
10. Amazon fees, Shopify fees, PPC or marketing-only revenue share in statutory COGS. Fix: R17, R20. (04, 06)
11. Payment fees in OPEX (they vary with revenue). Fix: R17. (03)
12. Warehouse staff left in OPEX, overstating gross margin. Fix: P6. (03)
13. Mixed packaging invoices coded to 1 account. Fix: R15. (04)
14. Coupons coded as ad spend or COGS. Fix: R19. (04)
15. All returns costs treated the same way. Fix: R21. (04)
16. Supplier invoice price never checked against the PO price. Fix: P4 step 2. (04)
17. Accepting "close enough" COGS; treating margin bands as targets. Fix: checklist 5.3. (04, 06)
18. Expired or stolen stock with no rotation, logs or counts. Fix: R113. (06)

**P&L structure**
19. Interest inside OPEX. Fix: R26. (03, 05)
20. Fixed creative or retainers moved in and out of variable marketing mid-year. Fix: R27. (03, 02)
21. Growing OPEX (people, software, office) faster than revenue as "reinvestment"; profit flat for years. Fix: R28, R91. (03, 02)
22. Chasing revenue while expecting margin to expand later. Fix: R31. (03)
23. Reacting to a missed line before tracing the line above it. Fix: R25, P15. (03, 01)
24. Spreading fixed costs into the daily view and then cutting spend that makes positive incremental CM. Fix: R34. (02)
25. Running the company on channel ROAS (Meta, MTA tools) and then asking why there is no cash. Fix: R35, R36. (02, 03)

**Revenue, returns and reconciliation**
26. Reading January efficiency on Shopify total sales that include December's processed returns, then pulling back spend. Fix: R41, R42. (02)
27. Summing platform-attributed revenue into the P&L; comparing ROAS across platforms; moving money to the highest-ROAS bottom-of-funnel line and then wondering why growth stops. Fix: R130, R131. (03, 02)
28. Measuring media only on .com after adding Amazon or retail, and cutting spend; separate .com and Amazon P&Ls. Fix: R133. (02)
29. Measuring in one tool while Meta optimises on another signal. Fix: R132. (02)

**CAC and LTV**
30. Dividing marketing by all orders, or using platform CPA as CAC, or computing CAC per channel in the P&L. Fix: R44, R46. (01, 03)
31. Setting CAC targets from blended AOV and a wrong margin. Fix: R48. (03)
32. Using blended CAC alone when organic buyers are friends and family. Fix: R47. (01)
33. Ignoring the first-order discount as part of acquisition cost. Fix: R67. (01)
34. Open-ended or revenue-based LTV. Fix: R54, R55. (03, 01)
35. Accepting LTGP:CAC below 1 as "a strategy"; also sitting far above 3 without testing marginal spend. Fix: R58, R59. (03)
36. Running CM:CAC below 1 in a buy-once category; or judging a repeat business on the first order alone. Fix: C9. (01)
37. Payback as CAC / monthly GP (assumes 0 churn); payback in months when customers skip. Fix: R60. (01)
38. Reading retention from aggregate totals or a churn rate instead of cohorts; reading a calendar month across a row instead of diagonally; treating NRR above 100% as an error. Fix: R56, F22. (01)
39. Churn without a period; churn divided by the current total or applied to new signups; asking for churn in a non-subscription store. Fix: R134, R135. (01)
40. Lowering the CAC or ROAS line whenever the team says it cannot be hit. Fix: R51. (02)
41. Scaling spend (often with raised money) while CAC rises and CM and repeat stay flat. Fix: R52. (01)
42. Letting maximize conversions pour spend into the cheapest-CPA product; paying to advertise products that sell anyway. Fix: R128. (03)

**Discounts and pricing**
43. 50% off sitewide: volume soars while CM after CAC goes negative. Fix: R70, P16. (01)
44. Public discounts without recomputing break-even ROAS and CAC. Fix: R69. (03)
45. Treating discounts and marketing as separate budgets; assuming the biggest discount always wins; putting the deepest discounts on flash sales instead of on-ramps. Fix: R68, R72. (01)
46. Planning "no returns during the promo". Fix: R74. (01)
47. Keystone or arbitrary markup pricing; 1 flat price across variants. Fix: R77, R81. (03, 02)
48. Pre-orders or BNPL modelled without cancellation or return rates. Fix: R75. (02)

**Forecasting**
49. Forecasting total revenue in 1 line; copying last year's month that had a launch; spend up 50% with CAC flat. Fix: R82, R83, R125. (03, 02)
50. Forecasting from an outlier year with no regression to the mean. Fix: R86. (02)
51. Leaving sale periods and BFCM in the spend-efficiency regression. Fix: R85. (03)
52. Assuming the customer file compounds forever. Fix: R38. (02)
53. Expecting a saturated category's old efficiency to return. Fix: R88. (02)

**Cash and inventory**
54. Judging health on net income alone; treating profit as cash; ignoring inventory on the balance sheet. Fix: R97, R102. (05, 03, 01)
55. Treating depreciation as cash spent, or per-unit COGS as the month's cash spent on stock. Fix: R98, R106. (05, 01)
56. Treating borrowing as improved cash health; treating debt as an operating issue. Fix: R100. (05)
57. Planning tax without the payment calendar or accumulated losses. Fix: F39. (05, 01)
58. Letting projected inventory go negative; placing a PO with no media plan (the $20M SKU). Fix: R105, R110. (01, 02)
59. A media buyer on a ROAS target with no inventory view, selling out hero SKUs at high CAC; a stock-out killing a winning ad. Fix: R108. (02)
60. Holding aged stock to prop up the balance sheet; paying storage on stock with no ads or emails planned; agencies KPI'd only on profit starving B, C and D stock. Fix: R112. (02, 03)
61. Launching products without rationalising SKUs. Fix: R114. (03)
62. Cutting media by reflex when stock is stuck, or raising it without the 5 conditions in C6. Fix: C6. (03, 02)
63. Scaling ad spend with no view of the CCC and financing; lowering efficiency to grow faster while debt rises; trying to triple in a year on borrowed money. Fix: R115, R119. (03)
64. Selling permanent equity to fund 3 months of inventory. Fix: R120. (01)
65. Full-time payroll sized to peak months; long-payback investments when cash is tight. Fix: R93, R62. (02)
66. Over-formatted models and 700-row payroll tabs. Fix: R94. (01)

**Arithmetic slips in the sources (use the corrected numbers).**
67. 03 discount example: break-even ROAS at 30% off is 7 (10 / 70 = 14.3% margin; 1 / 0.143), not 10; the rise is 2.8x, not 5x. Break-even CAC $10 is right.
68. 03 LTGP:CAC example: 100 / 33 = 3.03, not 3.33.
69. 03 cohort forecast example: 100 x 0.1% x $100 = $10, not $1.
70. 03 waterfall example: the exact price for its inputs is $63.51, not "about $70"; at $70 the contribution is $18.80 (26.9%), above the 20% target.
71. 03 existing-customer budget: the formula needs "/ 1,000" for CPM; the $2,250 result is right.
72. 03 brand example: $300M vs $8M is about 37.5x, not 20x.
73. 03 t-shirt margin: 24% counts tax as a cost; 26.4% on $91 is the tax-excluded answer (C14).
74. 03 frequency: "under 8" is over 7 days (the Meta column), not per month; regression cut-off is likely $1,000 a day, not a month; "over $10 million a month" for incrementality may mean a year.
75. 01 T2 first-order AOV is $238, not $138 (card [a592b3f28c58] repeats 138).
76. 01 T4 fulfillment in the $175 example is $45, not $40 (card [ca717cbf0593]).
77. 01 T9 subscription fulfillment is about $15.50, not $5.50, to give the stated 59% and $33.40 (card [17cd13e806d9]).
78. 01 T14 shipping is $7.25, not $0.30 (8.64 + 4.50 + 7.25 = 20.39) (cards [31dce846c93c] [482dba787e59]).
79. 01 T10 first inventory purchase is about $17,700 (2,400 x $7.20), not $177,000.
80. 01 T5 and 05: "net income only 140" is $140,000 (card [8c56490f81a2]).
81. 01 T3: CM after CAC at baseline is $45,000 (5,000 x $9), not $50,000; BOGO at 20,000 orders is $720,000 (20,000 x $36).
82. 01 T8 grid: 66,667 x 2.2% = 1,467 and x 3.8% = 2,533; the source's 1,433 and 2,500 buyers are rounded assumptions.
83. 01 T2: product cost 17.7 to 19% of revenue does not fit "73% to product gross profit"; use the line values.
84. 01 T14: paid LTV:CAC is $69 / $64 = 1.08, far thinner than the blended 1.4 (card [79a98ff8e618] garbles it).
85. 01 churn conversion: 40% annual is 30 months by the presenter's simple method and about 24 months by survival (C13).
86. 02: the hoped correlation is 0.78, not "7.8".
87. 05: FCF is operating cash flow minus capex as a positive number; "net cash flow slightly lower than FCF" holds only in a month that repays principal (C20).
88. 03 card [8aab49e8f65e]: the 1.4 aMER is hypothetical; $100 / $50 is the blended MER of 2. Card [ac6ec12672a6]: "$15 to $27" means +$15, from $12 to $27.

