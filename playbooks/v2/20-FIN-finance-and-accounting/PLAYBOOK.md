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

