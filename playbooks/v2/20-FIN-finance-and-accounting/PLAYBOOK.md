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

