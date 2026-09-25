# 17-CXP post-purchase playbook

version: 2.0-draft  |  date: 2026-09-24  |  sources: 7 (5 independent, see 0.2)  |  cards: 112  |  built from: sources/*.md

## 0. How to use this playbook

**Ecommerce first.** This playbook is for ecommerce stores, not a general customer-experience guide. Section 3.0 is the ranking: work its 12 levers top to bottom before opening any other rule. Store-type conditions (hero SKU vs catalogue, low vs high AOV, subscription vs one-off, marketplace-heavy, luxury or considered purchase, mobile-first India vs US) decide which rules in the sections below actually apply to the brand in front of the agent.

### 0.1 Who runs it

This is the base layer for the retention and customer experience agent. It covers the money side of retention (LTGP, CAC, ratio bands, payback, floor and ceiling), how to read cohorts, how to structure the first, second and third purchase, the segments that retention runs on, and every touchpoint after "Buy": confirmation, tracking, the wait, delivery, unboxing, returns, refunds, reviews, support and recovery. It also holds the CX strategy layer (maturity, ownership, measurement method) and the trend forecasts, with a clear line where a forecast stops being a rule.

Every rule cites the mini playbook numbers (01 to 07) and card ids. Cards are in `data/library-v3/cards.json`. Rules that start with "ecomOS" override any source. They are in 3.24.

### 0.2 How the 7 sources are counted

| Number | Source | Counted as |
|---|---|---|
| 01 | The Complete E-Commerce Retention Masterclass (Nathan, Angus Cowan) | 1 |
| 02 | Introduction to Customer Experience (Luxembourg, CQX) | 1 |
| 03 | Customer Digital Experience is Key to Successful Ecommerce (Coveo interview) | 1 |
| 04 | E-commerce Customer Delight (compiled report) | 1 together: "the delight cluster" |
| 05 | Customer delight across the e-commerce journey: a retention view (research memo) | (same) |
| 06 | E-commerce Customer Delight Journey (research report) | (same) |
| 07 | 9 Customer Experience Trends for 2026 (Van Belleghem) | 1 |

Sources 04, 05 and 06 are variant drafts of the same research brief. They share the topic, the theory base (peak-end, Kano, effort), the same case examples (branded tracking, instant refunds, handwritten notes, quizzes) and often the same vendor numbers. Each mini playbook flagged this on its own. This playbook counts them as 1 source in every confidence tally and writes "04/05/06" or "the delight cluster" when they agree. Where they differ from each other, the playbook says which one says what. So the maximum confidence in section 6 is 5 sources, not 7.

About 70% of source 01 is Klaviyo flow, segmentation, campaign and RFM content that belongs to 14-EML. This playbook keeps the formulas and the retention structure from 01 (LTGP, CAC, bands, F1/F2/F3, engaged audience, RFM, VIP, existing-customer ads, discount cohorts) and summarises the build parts briefly with pointers to `playbooks/v2/14-EML-email-lifecycle/PLAYBOOK.md`. Source 03 is mostly pre-purchase search and merchandising; only its margin and buy-vs-build rules are kept here.

### 0.3 Which sections to load for which task

| Task | Load |
|---|---|
| Cohort readout, LTGP, CAC target, payback | 3.0, 3.1, 3.2, 4.P1 to 4.P4, 5.1, 6, 9.1 |
| Find the retention constraint (product, portfolio, acquisition, CX, owned media) | 3.3, 3.4, 4.P5, 4.P6, 5.5 |
| Segments: engaged, RFM, VIP, lifecycle | 3.5, 3.6, 4.P7, 4.P8, then 14-EML |
| Existing-customer ads budget | 3.7, 4.P9, 6 |
| Discount-cohort and acquisition-quality audit | 3.8, 4.P10, 4.P11, 5.1 |
| Post-purchase journey audit (confirmation to review) | 3.9 to 3.14, 4.P12 to 4.P19, 5.2, 9.2 |
| Returns, refunds, support, recovery | 3.14 to 3.16, 4.P20 to 4.P23, 5.3, 9.4 |
| Loyalty, VIP experience, win-back | 3.17, 3.18, 4.P24, 4.P25 |
| Prioritise experience fixes and delight spend | 3.0, 3.9, 4.P12, 4.P26, 4.P27, 5.4, 9.2, 9.7 |
| Retention play with test design | 3.4, 3.19, 4.P30, 5.5, 9.3 |
| CX strategy, maturity, ownership, voice of customer | 4.P29, 7.C1, Appendix A (general theory, moved from 3.21 and P28) |
| Search tech, buy vs build, margin per visitor | 3.22, 4.P31, 7.C4 |
| AI, trends, brand agents, AI visibility | 3.16, 3.23, 4.P32, 11 |
| Any conflict between sources | 7 |

### 0.4 What the agent must fetch before acting

1. From the brand record: category and repeat cycle (consumable, durable, fashion), AOV for new customers, gross margin, COGS per SKU, delivery cost per order, transaction fee rate, refund rate, discount policy, ship-to countries, returns policy and law per market, carrier lanes and handling time, brand promise in one line, voice guide, approved claims, product usage cadence per SKU, packaging spec and 3PL capabilities, and the share of orders that are marketplace-fulfilled and so out of scope for this playbook (R158).
2. From the data layer (Shopify, Klaviyo, helpdesk, returns app, Metabase): order-level revenue and refunds by customer with first-order date, media spend by period, new customers by period, discount code per order, ticket log tagged by type (WISMO, returns, product, other), delivery promise and delivered timestamps per order, return request and refund timestamps, review request and review counts, list size and engaged segment size, RFM output.
3. From the web, tagged `[web check]`: tracking-page and returns vendors and prices, refund and returns law per ship-to market, AI support tool capabilities, the statistics quoted by sources before any client use. Section 10 lists all of them.

Tags: `[verify UI]` marks platform steps that can change. `[needs brand data: x]` marks a value the agent must pull before acting. `[web check: x]` marks something to check live.

All arithmetic runs in code in ecomOS, never in the model. Every formula in 3.0 has its variables defined. A missing input returns "unavailable", never 0. A vendor or brand case number is a claim, not a benchmark; the agent says "claim" when it quotes one.

## 1. Scope and outcomes

Covers: retention economics (LTGP by window, CAC, LTGP to CAC bands, CAC payback, CAC floor and ceiling); cohort reading (period returning rate vs cohort repeat rate, RPR bands, top-20% share); the first, second and third purchase structure (F1, F2, F3); engaged-audience, RFM, VIP and lifecycle segments; the existing-customer ad budget; discount-cohort and acquisition-quality audits; the post-purchase journey (order confirmation, the wait, delivery promise, branded tracking, WISMO, delivery and unboxing, education, review request, replenishment and second-purchase nudges, returns and refunds); effort reduction in service moments and engineered peaks in discretionary moments (peak-end, Kano, delight decay, expectancy disconfirmation); service recovery; support as a profit centre; loyalty tiers and experiential rewards; win-back; CX strategy, ownership, maturity and voice of customer; where the AI and CX trend forecasts stop being rules.

**R158.** This playbook covers the brand's own site and app checkout only. Marketplace-fulfilled orders (Amazon or Flipkart-fulfilled, where the brand does not control tracking, packaging or support) sit outside this scope; do not apply the branded-tracking, unboxing or support rules here to an order the brand cannot touch after the sale. `[general practice]`. No source in this folder found this lever (only an unrelated SAP Store mention in 03); verify against brand data before use.

Does not cover (go to the neighbour folder):

- Flow builds, email counts, timing, subject lines, deliverability, SMS mechanics: 14-EML. This playbook says what the retention structure is; 14-EML says how to build it in Klaviyo.
- Paid acquisition, CAC measurement in the ad platforms, attribution: 06-MEA and 24-DEP. This playbook only holds the CAC arithmetic needed to set a target and the narrow existing-customer budget rule.
- Contribution margin, COGS, fulfillment cost definitions: 20-FIN. Where 20-FIN defines CM2, use it as the gross profit per order in the LTGP formulas here.
- Offer and bundle design: 03-OFF. This playbook only says that offers move the LTGP ceiling.
- Checkout and site conversion testing: 09-CRO and 07-LPG. Checkout appears here only as a "pit to smooth" in the peak-end map.
- Search, recommendations and merchandising build: 05-SET. Only source 03's margin and buy-vs-build rules stay here.
- AI visibility in LLM answers: 16-AEO. Source 07's audit is summarised and pointed there.
- Warehouse, picking and packing: 21-OPS.

Business measures this domain moves:

- Cohort repeat purchase rate and first-to-second order conversion within 90 days (01, 04/05/06). [42e1ab9189e1] [3c84840ee4fe] [6dcc8b256a6b]
- 90-day and 365-day LTGP per new customer, and the CAC ceiling that follows from it (01). [2d30561e1938] [3861489d8286]
- Revenue and profit share from the top 20% of customers (01). [b4ff45d77f83] [3de8a595a9bb]
- CAC payback date for subscription and CPG brands (01, 06 worked example). [d1160b9862c5] [8db0ffa97875]
- WISMO contacts per order, delivery estimate accuracy, return-to-refund time, returners' repeat rate (04/05/06). [6390a69c8430] [6177983af652] [33d6b517ecb9]
- Cost per contact and return per contact (07). [298b23ff39c4]
- Engaged share of the list, as the leading retention KPI on the owned-media side (01). [c5da5743237]

## 2. Inputs the agent needs

| Input | From where | Required or optional | Why |
|---|---|---|---|
| Order-level revenue, refunds, discount code, customer id, first-order date | data layer (Shopify or Metabase) | required | Every cohort metric, LTGP, F2 rate, discount-cohort audit (3.1, 3.2, 3.8) |
| COGS per SKU, delivery cost per order, transaction fee rate | brand record or 20-FIN | required | Day-0 and cohort gross profit (F1, F2) |
| Refund rate and whether revenue is gross or net of refunds | brand record | required | Avoids double-counting refunds (R4) |
| Media spend by period, all channels; new customers by period | data layer (ad platforms, Shopify) | required | CAC (F3), ratio (F4) |
| CPC and new-customer conversion rate, current and best realistic | data layer | required | CAC floor and realistic case (F6) |
| Category repeat cycle; subscription attach; usage cadence per SKU | brand record | required | LTGP window choice (R7), payback (R11), replenishment timing (F23) |
| Annual revenue and capital position (bootstrapped, funded, loan) | user | required | Window choice and VIP-program leverage (R7, R43) |
| Existing-customer count, planned send frequency, CPM | data layer, ad platform | optional | Existing-customer budget (F13); only in the fashion or frequent-drop case |
| List size, engaged segment size, RFM output | data layer (Klaviyo) | required for segment tasks | Engaged share (F12), RFM segments (R40, R41) |
| Ticket log tagged WISMO, returns, product, other; contact cost | helpdesk | required for journey and support audits | WISMO rate (F17), cost per contact (F19) |
| Delivery promise, ship, deliver timestamps per order; carrier lane data | data layer, carrier or tracking app | required for journey audit | DEA (F16), delivery promise build (P14) |
| Return request, approval, refund timestamps; refund method | returns app or payments | required for returns audit | Refund cycle time (F18) |
| Review request send and review counts | reviews app | optional | Review request rules (R91) |
| Brand promise in one line; voice guide; approved claims | brand record | required | Coherence check (R84), support templates (P22), education emails (R72) |
| Packaging spec, 3PL insert and note capability, per-order packaging cost | brand record, 3PL | required for unboxing work | Unboxing protocol on a budget (P16), F22 |
| Post-purchase survey and support verbatims, NPS if collected | data layer | optional | Product-quality audit (R24), objection map (R79), conflict C1 |
| Returns and refund law per ship-to market | web | required before any returns policy change | `[web check]` (section 10) |
| Tracking, returns, helpdesk and AI support vendors and prices | web | optional | P15, P20, P23 `[web check]` |

## 3. Decision rules

Every rule states the rule, when it applies, the mini playbooks that support it, any conflict (by section 7 code), and card ids. Where only 1 source supports a rule, the rule says so. Where sources disagree, the strictest condition is kept here and the disagreement is written out in section 7. Section 3.0 is the formula register; rules cite formulas by F number.

### 3.0 Ecommerce priority order

Work this list top to bottom on any post-purchase job. It is the triage order, not a replacement for the detail below.

1. Fix product and portfolio before any CX spend. A broken reason to return outranks every touchpoint fix. R23, R24, R25.
2. Get delivery date accuracy and proactive tracking above 90%. Cheapest, most universal WISMO and trust fix. R69, R70, R126 step 1.
3. Fix returns and refunds friction. Weight highest for catalogue and apparel brands with high return rates, lower for single-SKU low-return consumables. R96, R97, R102.
4. Build the 3-message post-purchase sequence and cut WISMO under 5%. Universal, low cost, high leverage. R67, R68, R71.
5. Design the unboxing peak. Weight highest for single-hero-SKU DTC brands with a strong physical identity, lower for commodity or marketplace-heavy catalogues. `[general practice]` on the marketplace weighting; R80, R83.
6. Time replenishment and the second-purchase nudge to the usage cycle. High priority for consumable and subscription brands, low for durable one-off categories. R34, R92.
7. Track CAC payback day for subscription or CPG brands only; one-off and durable brands skip to first-order profitability. R7, R11.
8. Set the LTGP window and CAC ceiling by capital and category. Bootstrapped or sub-15 to 20 million brands default 30-day; funded or high-repeat brands go 90-day or further. R7, R8.
9. Build engaged-audience and RFM segmentation, only after steps 1 to 4 are healthy. R23, R37, R40, R41.
10. Choose the update channel by audience and geography: SMS for older or US bases, WhatsApp for opted-in Indian D2C. The clearest store-by-geography rule the playbook already has. R75.
11. Build loyalty and VIP tiers only once delivery, returns and support are reliable, and only where VIP revenue is the constraint, roughly above 10 to 20 million a year. R43, R115.
12. Spend on existing-customer ads only in the fashion or frequent-drop exception. Every other store type skips this lever. R49.

Load this block first; the groups below are the detail.

### 3.0b Definitions and formula register

Conventions for the developer. All money in the brand's reporting currency, tax excluded. All rates as decimals in code (0.30, not 30). A cohort is the set of customers whose first order falls in one acquisition period (week or month). A window W is measured in days from each customer's first order, not from a calendar date. Every ratio over a period uses period totals (sum over sum), never an average of daily ratios. Missing inputs return "unavailable", never 0. Every output carries its definition label (for example "90-day LTGP, refunds included, cohort June 2026").

**F1. Day-0 gross profit per new customer.**
```
gp_day0 = nc_aov - cogs_order - delivery_cost_order - transaction_fees_order - refund_allowance_order
refund_allowance_order = refund_rate x nc_aov        (only if nc_aov is gross of refunds; else 0)
```
`nc_aov` = average first-order revenue of new customers in the cohort. `cogs_order` = landed product cost of the first order. `delivery_cost_order` = shipping plus fulfillment plus 3PL, handling, pick and pack. `transaction_fees_order` = payment fees. Never compute this as `nc_aov x assumed_margin`; AOV and margin move per cohort, most of all in discount periods. Where 20-FIN's CM2 per order is available, `gp_day0 = cm2_order` for new customers. Source 01. [2d30561e1938]

**F2. Cohort LTGP at window W.**
```
ltgp_W[cohort] = sum_over_customers_in_cohort( revenue_within_W - cogs_within_W - delivery_within_W - fees_within_W - refunds_within_W ) / customers_in_cohort
W in {0, 30, 60, 90, 180, 365}
```
Built from real order and refund line items per customer, refreshed at least monthly. `customers_in_cohort` is the pre-refund acquired count. Refunds enter here and only here (see F3). The 30 to 365 day series is the cohort LTGP curve. Sources 01; 05 agrees on cohort reporting. [2d30561e1938] [b4ff45d77f83] [3e09caf827f4]

**F3. CAC.**
```
cac_period = media_spend_period / new_customers_period
```
`media_spend_period` = total paid media across all channels in the period. `new_customers_period` = first-time buyers in the same period, counted before refunds. Do not remove refunded customers from the denominator; that would blame the ad platform for a product problem. Period: daily or hourly for 9 to 10 figure retailers, weekly or monthly for 6 to 8 figure brands. Source 01. [2d30561e1938]

**F4. LTGP to CAC ratio and bands.**
```
ratio_W = ltgp_W / cac_period
band: ratio_W < 1.0        -> losing money (only under a deliberate capital-funded growth plan)
      1.0 <= ratio_W < 2.0 -> inefficient, scalable only with strong working capital or an exit plan
      2.0 <= ratio_W <= 3.0 -> target scaling band
      ratio_W > 3.0        -> leaving money on the table (arbitrage, unlikely to last)
```
State W with every ratio. Source 01, agency heuristic. Conflict C9 with 20-FIN on the above-3 reading. [3861489d8286]

**F5. CAC target from LTGP.**
```
cac_target = ltgp_W / target_ratio
```
Worked examples from 01: 80 (30-day LTGP) / 2 = 40; 100 (90-day LTGP) / 2 = 50. Moving from the 30-day to the 90-day window raised the ceiling by 25% in that example. Source 01. [3861489d8286]

**F6. CAC floor and realistic case from CPC and conversion.**
```
cac_floor     = cpc_low  / cvr_new_high
cac_realistic = cpc_now  / cvr_new_now
paid_headroom = cac_realistic - cac_floor
cvr_new = new_customers / clicks              (new customers only, not all purchases)
```
Worked examples from 01: 0.70 / 0.03 = 23.33; 1.00 / 0.02 = 50. A small `paid_headroom` means paid is near its floor and the lever is LTGP. Source 01. [f1d832540bbc] [2e9e88a22775]

**F7. CAC payback for a Day-0 loss.**
```
deficit_day0   = cac_period - gp_day0
cum_gp(t)      = sum of gross profit from all cohort orders through day t / customers_in_cohort
payback_day    = smallest t where cum_gp(t) >= cac_period
```
Worked example from 01: 50 CAC, 45 Day-0 gross profit, deficit 5. Only for categories with real replenishment or subscription depth. Source 01; 06 gives a parallel worked example (20 CAC, 10 first-order margin, 3 delight cost). [d1160b9862c5] [8db0ffa97875]

**F8. Period returning-customer rate vs cohort repeat purchase rate.**
```
returning_rate_period = orders_from_returning_customers_period / total_orders_period     (Shopify "% returning customers")
repeat_rate_W[cohort] = customers_in_cohort_with_2_or_more_orders_within_W / customers_in_cohort
```
`returning_rate_period` rises with store age and with weaker acquisition; it is not a retention KPI. Use it only to slice a sale period (new vs existing resonance). `repeat_rate_W` is the retention KPI. Sources 01; 05 agrees on cohort reporting. [9444eb58b437] [3e09caf827f4]

**F9. Repeat purchase rate bands (04, uncited heuristic).**
```
rpr = repeat_rate_W with W stated (04 does not state W; treat as 12 months)
rpr < 0.20        -> problem
0.20 <= rpr < 0.30 -> average
0.30 <= rpr < 0.40 -> good
rpr >= 0.40       -> excellent
```
Reference points, not targets: 05 cites a DTC 12-month average near 0.282 (range 0.099 luxury to 0.652 grocery, one 156,110-customer dataset at 0.188), 06 cites "30% to 40%" average retention, 01 says only about 20% buy twice from 80% of brands. Conflict C5. [7f71ff76f9b1] [3e09caf827f4] [8db0ffa97875] [42e1ab9189e1]

**F10. First-to-second order conversion (the F2 metric).**
```
f2_rate_W[cohort] = customers_in_cohort_with_second_order_within_W / customers_in_cohort
```
Read against 90-day LTGP. 05 says 25% to 30% is achievable "when done well" for non-consumables (source estimate). Sources 01, 05. [3c84840ee4fe] [6dcc8b256a6b]

**F11. Top-20% revenue share (the F3 metric).**
```
top20_share = revenue_from_top_20pct_customers_by_revenue_period / total_revenue_period
top20_profit_share = gross_profit_from_same_customers / total_gross_profit_period
```
Read against 365-day LTGP. 01's stated VIP pattern: about 0.50 or more of revenue and about 0.80 of profit; validate on brand data. Source 01. [b4ff45d77f83] [3de8a595a9bb]

**F12. Engaged share of list.**
```
engaged = profiles with (open or click within L_email) or (add_to_cart, checkout_started or order within L_site)
engaged_share = engaged / total_list
```
01's example lookbacks: L_email about 180 days, L_site about 220 days for site actions and about 280 days for orders. Target: engaged_share >= 0.50 and rising. Source 01. Build details in 14-EML. [83592aa3301a] [c5da5743237]

**F13. Existing-customer paid budget (dollar-based, not a share of spend).**
```
existing_budget_month = send_frequency_month x existing_customers x cpm / 1000
send_frequency_month in [4, 7]
```
Only in the fashion or frequent-drop exception (R44). Source 01. [675be3b57a10]

**F14. Marginal CAC of an existing-customer spend step.**
```
marginal_cac = (spend_high - spend_low) / (conversions_high - conversions_low)
```
Worked example from 01: (1000 - 700) / (50 - 47) = 100 per extra conversion. Pull back when marginal_cac exceeds the existing-customer CPA target. Source 01. [675be3b57a10]

**F15. Customer retention rate for a fixed population (06).**
```
crr = (customers_end - customers_new_in_period) / customers_start
```
Define the population and window the same way at both ends. Source 06. [bc11d5300f1f]

**F16. Delivery estimate accuracy.**
```
dea = orders_delivered_within_promise / orders_whose_promise_window_has_closed
```
Overdue and undelivered orders count as misses, not pending. Target above 0.90 (05 heuristic; one vendor case above 0.95). Source 05. [6177983af652] [3e09caf827f4]

**F17. WISMO rates.**
```
wismo_order_rate   = orders_with_at_least_1_wismo_contact / orders_shipped
wismo_tickets_per_order = wismo_tickets / orders_shipped
wismo_ticket_share = wismo_tickets / all_tickets
```
Track the first two separately; they diverge when customers file repeat tickets. Bands (05, vendor guide): under 0.03 healthy; 0.03 to 0.08 normal but expensive; above 0.08 structural. Source 05; 04 gives the ticket-cut claim. [6390a69c8430] [d17748ab5f3a]

**F18. Refund cycle time and returners' repeat rate.**
```
refund_cycle_days = median(refund_received_at - return_requested_at)     (from the customer's request, not the warehouse scan)
refund_initiation_days = median(refund_initiated_at - return_requested_at)
returner_repeat_rate_W = returners_with_next_order_within_W / returners
gap = returner_repeat_rate_W - non_returner_repeat_rate_W
```
Good: `gap >= 0`. Sources 04, 05. [0f70a58b8a2b] [33d6b517ecb9]

**F19. Support cost and return per contact.**
```
cost_per_contact   = support_cost_period / contacts_period
return_per_contact = gross_profit_from_orders_linked_to_contacts_period / contacts_period
profit_centre_ratio = return_per_contact / cost_per_contact
```
Two separate lines; the ratio is the profit-centre signal. Source 07 gives the direction and no numbers. [298b23ff39c4]

**F20. Delight payback test.**
```
incremental_contribution = (repeat_gp_per_customer_treated - repeat_gp_per_customer_control)
                          - (remarketing + incentive + service cost per customer on repeat orders)
passes if incremental_contribution > delight_cost_per_customer over a mature window
```
Treated and control are matched or randomised cohorts, same window, refunds included. Source 06. [8db0ffa97875]

**F21. Margin per visitor (03, the guest's own term).**
```
mpv = sum(basket_margin_period) / unique_visitors_period          (visitors who did not buy stay in the denominator)
```
State which costs are inside "margin". Not an industry-standard metric. Source 03. [0272f48ebf68]

**F22. Packaging budget and insert scaling.**
```
packaging_budget_order = k x product_cost_order,  k in [0.02, 0.05]
insert_cost_month = insert_cost_order x orders_month
```
05's cost bands: branded moment under 0.50 per order; full premium 2.80 to 4.50; a 0.60 to 0.80 insert stack "becomes material" at 2,000 orders a month. Source 05. [bc838a699da9]

**F23. Replenishment trigger.**
```
usage_cycle_days[sku] = pack_size / daily_usage   or   median observed reorder interval
replenish_trigger_day = 0.75 x usage_cycle_days[sku]
max_replenish_messages_per_cycle = 2
```
Source 05; 04 agrees on "sized to usage and pack size, not a fixed day count". [6dcc8b256a6b] [491dd6d4221a]

**F24. Discount-cohort comparison.**
```
for each group in {no_code, code_A, code_B, ...}:
    repeat_rate_W[group], ltgp_W[group]
penalty[group] = ltgp_W[no_code] - ltgp_W[group]
```
Source 01. [34373cddcf01]

**F25. Dormant rebuild sample arithmetic.**
```
sample_size        = unengaged / n_samples            (01 used n_samples = 10)
newly_engaged_rate = newly_engaged_from_sample / sample_size
send_size_next     = engaged + sample_size
```
01's spoken case: 375,000 + 37,500 = 412,500 (the presenter said "about 410,000"); 7,000 / 37,500 = 0.187 (the presenter said "20 or 30%"). Use the computed values. Conflict C5. [83592aa3301a] [eacd1adfeb8d]

### 3.1 Retention economics: LTGP, CAC, bands, windows, payback, floor and ceiling

**R1. Measure lifetime value as lifetime gross profit (LTGP), never as revenue.** Applies to every LTV figure in ecommerce. Revenue is "almost meaningless" across brands because unit economics differ; software can use revenue LTV because overhead is low, ecommerce cannot. Source 01 (1 source). 03 agrees that customers should be valued by margin contribution, not revenue. [2d30561e1938] [31f92baa2ab2]

**R2. Every LTGP figure carries a time window.** Say "30-day LTGP", "90-day LTGP", never "lifetime". Build the cohort curve at 0, 30, 60, 90, 180 and 365 days (F2). An unconstrained lifetime number is unmeasurable and does not match cash needs. Source 01. 05 agrees on cohort windows. [2d30561e1938] [b4ff45d77f83] [3e09caf827f4]

**R3. Compute LTGP from order-level revenue and refund lines, never from AOV times an assumed margin.** Applies always; the AOV-times-margin shortcut breaks most in discount periods, when both AOV and margin compress. Refresh at least monthly. Source 01. [2d30561e1938]

**R4. Refunds go into LTGP and never into CAC.** The CAC denominator is the pre-refund new-customer count (F3). Correcting CAC for refunds blames the ad platform for a product-quality problem. If the revenue feed is already net of refunds, set the refund allowance to 0 so refunds are not subtracted twice. Source 01. [2d30561e1938]

**R5. CAC is total media spend across all channels divided by new customers in the same period; pick the period by scale.** Daily or hourly for 9 to 10 figure retailers; weekly or monthly trends for 6 to 8 figure brands. Source 01. 20-FIN holds the full CAC definition set. [2d30561e1938]

**R6. Set the CAC target as LTGP at the chosen window divided by a target ratio, and manage inside the 2 to 3 band (F4, F5).** Below 1 only under a deliberate capital-funded growth plan; 1 to 2 only with strong working capital or an exit plan; above 3 means spend is being left on the table. Source 01 (agency heuristic, 1 source). Conflict C9: 20-FIN's sources disagree on the reading of above 3. [3861489d8286]

**R7. Choose the LTGP window by growth appetite and capital, not habit.** Default 30-day for most stores, especially bootstrapped or profit-first stores and stores under about 15 to 20 million a year. 90-day or further for CPG, supplements and other high-repeat categories, or for funded brands willing to run a short-term loss. A loan-funded long-payback model needs interest-cost modelling and is "incredibly risky" under about 15 to 20 million a year. Source 01. `[needs brand data: annual revenue, capital position, category repeat cycle]` [5a300a3bc804]

**R8. Before extending the window or raising the CAC ceiling, forecast the incremental new-customer volume it buys.** Plot new customers against CAC ceiling. If a 10 unit rise in the ceiling buys meaningfully more customers (01's example: 30% to 40% more), fund it when cash allows. If volume barely moves, stay conservative and profitable on the first order. Diminishing returns are still returns as long as the volume is real. Source 01. [5a300a3bc804] [3861489d8286]

**R9. Bound CAC with CPC divided by new-customer conversion rate, as a scenario range, never a promise (F6).** Use click-to-new-customer conversion, not all-purchase conversion (that gives cost per purchase, not CAC). CPC on its own is a vanity metric that only matters at the extremes: very high is bad, very low usually means bad traffic. Source 01. [f1d832540bbc]

**R10. Decide which half of the ratio has real headroom before investing, and re-run the comparison at least quarterly.** CAC has a hard floor (traffic quality decays past a point); LTGP has a movable ceiling (offer, bundle, subscription, retention). Inexperienced operators underestimate both how low CAC can go and how high LTGP can be pushed. If `paid_headroom` in F6 is small, work the LTGP side. Source 01. [2e9e88a22775]

**R11. For subscription or CPG brands taking a Day-0 loss, track the CAC payback day as a standing finance KPI (F7).** Accept the deficit explicitly, track cumulative cohort gross profit, mark the crossing date, and model how much working capital sits in the red before scaling spend. Pull the date earlier with subscription depth, replenishment cadence and second and third purchase rate. Does not apply to one-off or durable-goods purchases. Source 01; 06 gives the same logic as a delight-spend justification. [d1160b9862c5] [8db0ffa97875]

**R12. Raise the LTGP ceiling through offer and subscription design, and judge each change by cohort LTGP, not first-order AOV.** Map the current 90 and 365 day ceiling including subscription attach; test bundles, starter kits, multi-month packs, one-time vs subscribe-and-save, trial vs full size; treat subscription cancellation as a leading LTV indicator; re-run the ratio after each change. Source 01. Offer mechanics live in 03-OFF. [9f7c64c08aab]

**R13. Justify any delight or packaging spend against CAC payback and cohort contribution, not first-order margin or aesthetics (F20).** Applies when the first order runs at a loss, which 06 calls common in saturated D2C niches. 06's worked example (20 CAC, 10 first-order margin, 3 delight cost, an assumed 50% retention lift) is illustrative only; the 50% and the "23% more spend from engaged customers" figure are cited claims. Source 06 (delight cluster). [8db0ffa97875]

**R14. Value customers and visitors by margin, not revenue or order count, and track the margin trajectory over time.** 03's example: a buyer of ten 5,000 laptops at thin margin with heavy support cost can be worth less than a buyer of many 80%-margin staplers. 03 also proposes margin per visitor (F21) as a north star for on-site decisions; it is the guest's own term, not an industry metric, and needs clean per-SKU COGS first. Source 03 (vendor GM, 1 source). [0272f48ebf68] [31f92baa2ab2]

### 3.2 Measuring retention: cohorts, repeat rate, attribution

**R15. Never use Shopify's "% returning customers" as a retention or LTV KPI (F8).** It is returning-customer orders over total orders in a period. It rises with store age and with weaker acquisition, so it can reward acquiring less. Its only legitimate use is slicing a sale period into new vs existing resonance. Source 01. [9444eb58b437]

**R16. Report every retention metric by acquisition cohort, never as a blended average.** WISMO rate, repeat rate, NPS or CSAT, LTGP: blended numbers are distorted by acquisition timing and category mix. Sources 01, 05 (2 sources). [b4ff45d77f83] [3e09caf827f4]

**R17. Use platform attribution as a north star only, and profitability metrics to find the constraint.** Klaviyo account, campaign and flow attributed revenue is "a grain of salt" number; 01 cites unnamed studies that 70% to 80% of campaign revenue may be incremental for some accounts, and says it depends on the brand. Chasing attribution optimises for looking good in-platform; ignoring incremental repeat work in favour of only long-term LTV thinking means today's numbers never move. Source 01. [2df157249026]

**R18. The core retention dashboard holds: 90 and 365 day LTGP mapped across the 30 to 365 day cohorts with refunds included, first-to-second conversion (F10), and revenue from the top 20% of customers (F11).** Attribution submetrics sit under it: campaign revenue, pop-up conversion (not opt-in rate), flow revenue used to find gaps, and year-on-year owned-media growth relative to business growth. 01's soft indicator of 30% to 50% of revenue from email is "not a hard science". Source 01. [2df157249026] [b4ff45d77f83]

**R19. Do not stop at CSAT and NPS: track CLV by delight-touchpoint cohort, WISMO volume, unboxing UGC count, return-to-repurchase rate, tracking-page engagement and loyalty-redeemer repeat rate too, since CSAT and NPS only catch dissatisfaction, not a customer quietly drifting.** 04's list: CLV by delight-touchpoint cohort, WISMO volume, unboxing UGC count, return-to-repurchase rate, tracking-page engagement, loyalty-redeemer repeat rate. 06 adds a customer retention rate (F15) and cites NPS benchmarks of about 50 average and 70 plus "world class" (cited industry figures, unverified). 05 gates roadmap steps on WISMO under 5% of orders and stable post-purchase NPS. Delight cluster (1 source). Conflict C1 on whether to survey at all. [7f71ff76f9b1] [bc11d5300f1f] [d6e5e929396b]

**R20. Every vendor or brand case number in this playbook is a claim to size an opportunity, not a target.** 05 treats only Kahneman's peak-end research and the 2010 HBR effort study as strong anchors; everything else (WISMO ranges, repeat-rate ranges, conversion lifts, loyalty ROI, Indian D2C figures) is vendor or self-reported. 04 says the same of its 40 brand cases. 03's 72% margin claim and 06's Bare Anatomy 35% CAC claim are single cases. Sources 03, delight cluster (2 sources agree on the caution). [4530efe6348a] [7f71ff76f9b1] [0272f48ebf68] [6bda120ef375]

**R21. Judge a pop-up by the conversion, AOV and gross profit of the customers it signs up, not its opt-in rate.** A 5% or 10% opt-in target "because someone told me" says nothing about audience value; compare against other acquisition sources. Source 01. Build rules in 14-EML. [4789763c9e99]

### 3.3 The retention hierarchy: diagnose before touching owned media

**R22. Expect that only about 20% of customers buy a second time from about 80% of brands, and treat weak second-purchase conversion as the default suspect.** This is 01's framing stat from its client base, not a benchmark; repeat rates differ by category. Source 01. [42e1ab9189e1]

**R23. Work the retention hierarchy top down: 1 product quality, 2 product portfolio, 3 acquisition quality, 4 customer experience, 5 owned media.** Owned media is "the amplifier"; it cannot outmarket a flawed retention system. Do not fund email, SMS, loyalty or delight work until the first 4 are checked. Source 01; the delight cluster's "fix effort before delight" and "loyalty only after foundations" rules are the same order applied to CX (R58, R115). 2 sources agree on the sequencing. [290bef9daa56] [b233a6d834e6] [d6e5e929396b]

**R24. Audit product quality with real customer evidence: surveys, NPS, verbatim feedback, support tickets, review text; never founder opinion.** Source 01. 02 disagrees on surveys as the instrument (C1); use the evidence the brand already holds first (P29). [290bef9daa56] [b24643e22b8c]

**R25. Check that the portfolio gives a reason to return: cross-sell, upsell or replenishment.** If none exists, the fix is a new product, collection or subscription, not more messaging. Source 01. [290bef9daa56]

**R26. First-order behaviour predicts repeat behaviour; treat acquisition quality as a retention lever.** Low-AOV TikTok Shop buyers and customers acquired in 40% to 50% flash sales repeat far less than a customer who spent 200 on the first order. Source 01. Audit method in R53 to R55. [290bef9daa56]

**R27. Customer experience includes how problems are handled, not only whether they happen.** Shipping updates, communication and support quality count; a problem handled well can predict a return visit. Source 01; the delight cluster's recovery rules agree (R104). 2 sources. [290bef9daa56] [284b8c726776] [df383902e95d]

**R28. Diagnose weak second-purchase conversion as a foundations problem before blaming email copy, and check for vanity signals first.** Common vanity signals: attribution dashboards and the Shopify returning-customer metric read as proof retention is fine. Source 01. [42e1ab9189e1] [9444eb58b437]

### 3.4 Purchase structure: first, second and third purchase (F1, F2, F3)

**R29. Map the whole account into 3 functions: F1 acquisition, F2 first-to-second order conversion, F3 revenue from the top 20% of customers, gross-profit adjusted.** F2 correlates with 90-day LTGP; F3 with 365-day LTGP; F1 is the gate. "F stands for function." Source 01. [3c84840ee4fe]

**R30. Split every flow's first branch by journey stage (new, returning, loyal or subscriber), never by product.** New: more aggressive, tackle trust and price, introduce the brand. Returning: skip the introduction, go straight to what they need. Loyal or subscriber: least aggressive, protect the relationship, ideally no incentive. Product or cart-value splits come second and are tests. Source 01; 04 agrees that first-time, repeat and VIP must get different treatment on site and in flows. 2 sources. [3c84840ee4fe] [e13b48c6a15a]

**R31. Reject the 2 common structure failures: one linear sequence for every entrant, and a first split by product attribute.** The second can be tested later as a secondary split; done first it hides where the constraint sits. Source 01. [3c84840ee4fe]

**R32. When the constraint is known (for example F2), go straight to that branch across every flow and diagnose there.** Do not react with a generic new win-back flow or more discount campaigns. Source 01. [3c84840ee4fe]

**R33. Flows carry the customer journey; campaigns carry reach and moments.** Flows run 24/7 on real behaviour and are more incremental than blasts, which often reach already-engaged people. The flow-to-campaign revenue split is business and month dependent and not a ratio to optimise. Source 01. Build in 14-EML. [3c84840ee4fe]

**R34. The second purchase: for non-consumables, nudge about 10 days after the first order arrives with a modest 10% to 15% incentive aimed at relevant discovery; for consumables, trigger at about 75% of the usage cycle (F23), framed as usefulness, capped at 2 messages a cycle.** 05's estimate is that a well-run second-purchase nudge converts 25% to 30% of first buyers; 05 cites replenishment conversion of 8% to 15% vs 1% to 3% for general promos (vendor benchmark). Source 05 (delight cluster). Conflict C7: 01 says loyal customers get no incentive and 06 says gifts, not codes; the 10% to 15% here applies to the first-to-second step for new customers only. [6dcc8b256a6b] [491dd6d4221a]

**R35. Give first-time, repeat and VIP buyers different post-purchase tracks: first-time gets education and brand story, repeat gets cross-sell into adjacent categories, VIP gets early access, exclusive experiences and recognition.** Princess Polly found one-time and repeat buyers got an identical on-site experience and treated that as the gap (case). Matas' segmented, non-discount re-engagement sequence reported a 29-point retention lift in 30 days (vendor case). Source 04; 01's journey-stage split is the same rule. 2 sources. [e13b48c6a15a] [3c84840ee4fe]

**R36. The third purchase and beyond: build loyalty tiers around milestones and status, message the loyal tier least, and only once delivery, returns and support are reliable.** Source 05 (tiers by milestone), 01 (least aggressive messaging for loyal, no incentive). 2 sources. [e6f325f479fd] [3c84840ee4fe]

### 3.5 Segments: engaged audience, lifecycle cohorts, RFM, VIP

These rules define the segments retention runs on. Klaviyo build steps, sunset and suppression logic, and window choices per market are in 14-EML (its R79, R82, R93 cover unengaged and suppression definitions).

**R37. Define an engaged audience (F12) as the primary sendable base, target at least 50% of the list inside it, and track its growth as the core owned-media retention KPI.** Engaged = opened or clicked within the email lookback, or added to cart, started checkout or ordered within the site lookback. 01's example lookbacks (about 180, 220 and 280 days) are heuristics to adapt to the brand's purchase cycle. Source 01. [83592aa3301a] [c5da5743237]

**R38. Rebuild reach into dormant subscribers gradually with random samples, not with one full-list blast.** Split the unengaged remainder into equal random samples (01 used 10), add 1 sample per send with the best content, fold the newly engaged into the permanent segment, repeat over 6 to 9 months, and save the biggest reactivation push for a calendar peak. Case: a 9-figure activewear retailer went from sends capped at 50,000 to 200,000 on a 750,000 list to a full-list Black Friday send and reported a 40% year-on-year lift (single case). Source 01. Arithmetic in F25; conflict C5. [83592aa3301a] [eacd1adfeb8d]

**R39. For subscription brands, run 4 lifecycle cohorts with 1 goal each: never purchased (get the first sale, ideally onto subscription), purchased not subscribed (upsell to subscription or next order), active subscriber (protect, no incentive), cancelled (reactivate).** Non-subscription brands substitute RFM or spend tiers (01's example: 500, 1,000, 3,000). Source 01. [4d8506a387fd]

**R40. Score RFM relative to the brand's own base, not an external benchmark, and use the segments Champions, Loyal, Recent, At Risk, Needs Attention.** At Risk means slowing against the customer's own cadence (usually every 3 months, now 3.5). Treat Needs Attention like At Risk, especially for former Champions. RFM sits in Klaviyo's marketing analytics tab `[verify UI]`. Source 01. [98fc8eced08a]

**R41. Trigger win-back, replenishment, post-purchase and abandonment branches off RFM, not a fixed day count.** A 120-day trigger hits a 200-day-cycle customer far too early with an unneeded discount. Source 01. Conflict C6: 05's 30 to 45 day win-back timing. [98fc8eced08a]

**R42. Define VIPs by revenue and profit concentration (01's pattern: about 50% plus of revenue, about 80% of profit), and validate on brand data before building anything.** VIPs return more, buy more often and rely less on discounts. Source 01. `[needs brand data: top-20% revenue and profit share]` [3de8a595a9bb]

**R43. Invest in VIP-specific programming only when VIP revenue is the actual constraint.** Under about 10 to 20 million a year the constraint is usually first-to-second order conversion; above that, VIP programs gain leverage. Source 01; 05's roadmap puts loyalty and VIP tiers at step 6, after delivery, returns, unboxing, nudges and quiz. 2 sources agree on "later, not first". [3de8a595a9bb] [d6e5e929396b]

**R44. Reward VIPs with exclusivity, not broad discounts: exclusive products, private sales, early access, events, community, and reminders of perks they have earned.** Build dedicated VIP branches in flows and use the specific-goal campaign slot for VIP sends. Source 01; 04 agrees (experiential rewards, R116). 2 sources. [39c55eb82e67] [3de8a595a9bb] [8b6b2a3dbcb5]

### 3.6 Campaign reach vs personalisation

**R45. Spend about 80% of campaign effort on reach (elite broad content to the engaged base) and about 20% on narrow specific-goal sends with 1 clear business reason.** Specific goals: excess stock, a supplier-led sale, a product push, a VIP push. Source 01 (heuristic, 1 source). "Elite content" is never defined beyond education, entertainment, social proof and reviews. [097d09066f7a] [3121e4d083d4]

**R46. Reject hyperpersonalisation as the default campaign strategy.** 01's reasons: the labour of one-to-one campaigns rarely pays back, fragmentation stops you learning what elite content is, and repeat revenue arrives in waves that only cash in if a large engaged audience was built first. Source 01, stated as a contrarian position. Conflict C2 with 07's hyperpersonalisation as a coaching assistant and 03's personalised discovery. [097d09066f7a]

**R47. Route personalisation to flows, not campaigns.** Flows have behaviour to act on; split by journey stage first, then by product or collection. Only about 3% of a list is ready to buy today (01's estimate); campaigns aimed at that 3% ignore the 97% who may still engage with broad content. Source 01. [3121e4d083d4]

**R48. Plan the calendar in 2 layers: always-on engagement content for baseline and event-based campaigns for peaks, and judge the channel by year-on-year growth relative to the business, not by any single send.** Repeat revenue peaks with sales, launches and restocks; new-customer revenue should scale closer to linear. Source 01. [f6f96b40442]

### 3.7 Existing-customer paid spend

**R49. Paid ads are an acquisition tool; the default is little or no spend on existing customers.** The single exception 01 now accepts: fashion or frequent-drop brands, where email and SMS cannot reliably surface every new arrival to the whole base. 01 states it held a harder line 2 to 3 years earlier and was wrong in that case; treat the exception as its current view. Source 01. Conflict C8 notes the reversal. [675be3b57a10]

**R50. Set the existing-customer CPA target at half or less of the new-customer CPA target.** 01's example: 40 new, 20 or lower existing. Equal CPAs mean overspend on existing customers or poor ads. Source 01. [675be3b57a10]

**R51. Measure the marginal CAC of existing-customer spend (F14) and pull back while conversions hold.** 01's example: 1,000 a day gives 50 conversions, 700 a day gives 47; the extra 300 bought 3 conversions at 100 each. Reallocate the saving to acquisition. Source 01. [675be3b57a10]

**R52. Budget existing-customer spend as a dollar amount from frequency, audience size and CPM (F13), never as a share of total spend.** Frequency 4 to 7 a month. Source 01. [675be3b57a10]

### 3.8 Acquisition quality: discount cohorts and zero-party data

**R53. Treat discount-driven acquisition as a hypothesis to test per brand, never as a default.** Front-end metrics improve in a sale (ROAS, volume) because the funnel opens to price-motivated buyers who often do not repeat at full price. 01 says about 60% of its client brands see substantially worse LTV and repeat from discount-acquired cohorts, and some 9-figure retailers see no penalty. Run F24 by discount code before scaling a promotion. Source 01. [34373cddcf01]

**R54. Collect zero-party data (what the customer says about themselves) separately from first-party data (email, phone, name), and use it to fix paid targeting, not only email personalisation.** Analyse the top 20% of customers for shared persona, resonant angle and purchased offer, overallocate spend toward that pattern; analyse the bottom 20% for mismatched angles. Source 01; 06 agrees zero-party data via a quiz is the safe personalisation source (R130). 2 sources. [e74d0b65f2db] [6bda120ef375]

**R55. Never trust a strong front-end ROAS without checking refunds, returns and repeat for that angle.** 01's case: a skin-health supplement sold on an "energy" angle showed "a five ROAS", then returns, refunds and no repeat, visible only in support feedback. Exclude angles that attract mismatched customers even when the ad dashboard looks good. Source 01. [e74d0b65f2db]

### 3.9 Effort vs delight: where to reduce friction and where to build a peak

**R56. Before writing a confirmation email, a tracking page or a return flow, decide the feeling you want the shopper to have there (reassured after checkout, informed during the wait, delighted at unboxing) and design copy and timing around it, not around urgency tactics like "only 1 left."** Applies to every post-purchase touchpoint. Consider rational and emotional needs together. Business-metric tactics (urgency, "only 1 left") that override the felt experience are a trust risk. Source 02 (general CX theory, no ecommerce data); 06 agrees that purchase and loyalty run on emotion first. 2 sources. [30663f02bf6d] [66a49b885b12]

**R57. A delivery that lands exactly on the quoted date, or a refund that takes exactly as long as policy says, both leave the customer neutral and free to try a competitor next time. Beat the quoted date or refund window on cheap, visible steps to earn a small positive surprise instead.** Expectancy disconfirmation (Oliver): expectation set by copy, price, brand and competitors vs perceived performance gives confirmation (neutral), negative disconfirmation (regret, churn) or positive disconfirmation (delight, advocacy). Source 06 (delight cluster). [9eb0da75866c]

**R58. Fix effort and broken promises before adding any delight.** A note or gift on top of a late delivery, a hard return or a slow refund creates "cognitive dissonance", not loyalty, and "makes the failure more memorable". Evidence 05 rates as strong: the 2010 HBR study of 75,000 plus service interactions found 96% of customers with a high-effort interaction became more disloyal vs 9% of low-effort ones. 04 cites 87% of brands believing they deliver exceptional CX vs 11% of shoppers agreeing (unattributed). Delight cluster (04, 05, 06 all state it); 01's hierarchy is the same order. 2 sources. Conflict C3. [b233a6d834e6] [36baf5a5a8ad] [ff986b275489] [290bef9daa56]

**R59. Split the journey into service moments and discretionary moments, and treat them differently.** Service moments (returns, WISMO, complaints, checkout): reduce effort, one-touch resolution, fast refunds, proactive updates, no dark patterns. Discretionary moments (unboxing, onboarding, milestones, a payment-time perk): engineer a limited number of peaks using elevation, insight, pride and connection. Source 05 (delight cluster). [36baf5a5a8ad] [df383902e95d]

**R60. Budget for 1 deliberate peak and 1 strong ending, not an even spread across the journey.** Peak-end rule (Kahneman, replicated; 05 cites a 2022 meta-analysis of 174 effect sizes): memory is set by the most intense moment and the last moment, not the average. For most DTC brands the peak is the physical unboxing (the only touchpoint with a 100% open rate) and the end is delivery confirmation, follow-up or issue resolution. Sources 05, 06 (delight cluster). [00097342f6ce] [0372f28739d1]

**R61. A negative peak overrides a good average; find and fix it before funding new delight.** Candidate negative peaks: checkout friction, confusing navigation, opaque billing, surprise fees, broken delivery, a slow refund. Source 06 (delight cluster). [0372f28739d1]

**R62. Classify every touchpoint with the Kano model before budgeting: must-be (fund as non-negotiable fixes), one-dimensional (hold at market standard), attractive (the only place delight budget goes).** Must-be examples: secure checkout, correct item, working navigation, accurate sizing. A classification is not fixed across audiences or eras. Source 06 (delight cluster). [ff986b275489]

**R63. Plan for delight decay: every repeatable delighter becomes a one-dimensional attribute and then a must-be.** 06's example: free 2-day shipping. When a funded delighter's metric goes flat while spend continues, treat it as decayed and plan its replacement on a rolling cycle. Source 06 (delight cluster). [a4e3c81ce639]

**R64. Under-promise slightly and over-deliver where it is cheap and visible; over-promising is the most frequent source of negative disconfirmation and churn.** 06's example: quote 5 days, arrive in 3. The under-promise must still be competitive. Source 06 (delight cluster); 05's delivery-promise rule (R69) is the operational form. [9eb0da75866c] [6177983af652]

**R65. Never manufacture a stockout, a slow refund or a shipping delay to trigger a recovery moment. When a real failure happens (wrong item, late parcel, damaged box), over-recover it; do not treat failures as a marketing tactic.** 05 cites Michel and Meuter's banking study (11,000 plus interviews): 5.4% of customers with a problem rated the recovery "much better than expected", and error-free service still beat recovery on satisfaction. When a failure happens anyway, over-recover (R104). Source 05; 04's Bloom & Wild quote ("over-fix turns them into a stronger advocate") is one CEO's observation, not a law. Delight cluster. Conflict C12. [df383902e95d] [284b8c726776]

**R66. Treat surprise gifts, handwritten notes at scale and community as brand and word-of-mouth plays until F20 proves them on brand data.** 05 says the evidence that delight alone drives loyalty is weaker and contested; 06 says to set the per-order delight budget from payback math, not packaging taste. Delight cluster. [4530efe6348a] [8db0ffa97875]

### 3.10 Order confirmation, the wait and WISMO

**R67. The order confirmation is an anxiety-reduction instrument, not a receipt.** Include a clear delivery estimate, the branded tracking link, what happens next, and 1 small piece of value (care guide, styling tip, founder note). 04 cites two-thirds of online shoppers feeling anxious right after clicking buy (unattributed). Sources 04, 06 (delight cluster). [d17748ab5f3a] [6d6e184eb848]

**R68. Send at least 3 proactive automated updates between order and delivery: confirmation with delivery estimate, shipping confirmation with a working tracking link, out-for-delivery with a window.** Fewer than 3 is the trigger to add more. 04 claims the 3-step flow "can eliminate up to 80%" of WISMO tickets (operational claim, no study). Add "delivered" and "delayed" messages (05). Delight cluster. [d17748ab5f3a] [6390a69c8430]

**R69. Build the delivery estimate from real lane and carrier performance plus handling time, pad it slightly, and show a specific date rather than a range.** Delivery speed fell from the number 1 consumer delivery priority in 2022 to number 5 by 2024 (McKinsey via a vendor), behind cost, transparency and reliability; a specific date is reported to lift conversion 13% to 25% over a vague range (Forrester via Narvar, vendor-reported). 74% of consumers in a 2025 Narvar survey (3,461 people) received a package later than the estimate. Source 05 (delight cluster). [6177983af652]

**R70. Hold delivery estimate accuracy (F16) above 90%, and count overdue undelivered orders as misses.** Source 05 heuristic; 1 vendor case above 95%. Delight cluster. [6177983af652] [3e09caf827f4]

**R71. WISMO is the first post-purchase fix: it is the largest support-cost driver and the easiest to remove.** Vendor-consistent ranges: 30% to 50% of tickets in normal periods, 50% to 80% at peak. Bands per order (F17): under 3% healthy, 3% to 8% normal but expensive, above 8% structural. 05's roadmap gate: move on when WISMO is under 5% of orders. Measure the brand's own number rather than trusting the range. Source 05; 04 agrees on priority. Delight cluster. `[needs brand data: WISMO tickets per order]` [6390a69c8430] [d17748ab5f3a]

**R72. For considered or routine-based products, put product-specific education in the shipping-window messages: prep steps, what to expect on first use, a realistic timeline to results.** Silence between confirmation and delivery breeds post-purchase dissonance. Keep every claim as accurate as the PDP; an inflated timeline here becomes negative disconfirmation later. Sequence the last message before delivery to set up the unboxing as the peak. May be thin for simple commodity reorders. Sources 06, 04 (the Bobbie infant-formula example uses developmental milestones; adapt the mechanism, not the content). Delight cluster. [6d6e184eb848] [578e1e518ece]

**R73. Keep transactional emails focused on the order; do not delay the tracking information the customer opened the email for, and route promotional cross-sell to permitted marketing sends.** Source 06 (delight cluster). Conflict C13 with 04's tracking-page recommendations: recommendations sit on the page, below status, not in the transactional email body above the tracking link. [6d6e184eb848] [af9547313e6f]

**R74. Reach out before the customer asks when a parcel stalls or a shipment issue is detected.** Herschel (via Malomo) and Bloom & Wild are the named examples. Sources 04, 05 (delight cluster). [73abfaadbe4c] [6390a69c8430] [284b8c726776]

**R75. Choose the update channel by audience: SMS for older or less digital bases (Crystal Classics' senior-skewed luxury customers), WhatsApp journeys for Indian D2C where opt-in is in place.** 05 cites a GoKwik dataset (26 billion messages, 1,800 plus brands, vendor-reported): automated WhatsApp journeys 11.12% CTR vs 2.6% for broadcasts. `[web check: WhatsApp Business opt-in rules for transactional vs marketing messages in India]`. Sources 04, 05 (delight cluster). [73abfaadbe4c] [ce139d4913b8]

**R151. For a multi-item order, tell the customer up front when items will ship separately, and send a tracking update per parcel, not one status for the whole order.** `[general practice]`. No source in this folder; verify against brand data before use.

**R152. Give the customer a self-service way to edit the delivery address or cancel the order in the short window before it ships, and state that window in the confirmation message.** `[general practice]`. No source in this folder; verify against brand data before use.

### 3.11 Branded tracking page

**R76. Point the tracking link to a page on the brand's own domain, never the carrier's page.** The carrier page is generic, may show competitor ads, and hands the highest-frequency post-purchase visit (04 cites 4.6 tracking visits per order, unattributed) to someone else. 04's aggregate claims for branded tracking: 23% to 31% higher repeat purchase, 9 to 12x ROI, 40% to 60% WISMO reduction (vendor frameworks, claims). Sources 04, 05 (delight cluster). [73abfaadbe4c] [6177983af652]

**R77. Page content: order status, estimated delivery window, carrier, logo and colours, 1 complementary product recommendation, loyalty link, a clear returns path; optionally order lookup, education, rewards detail, social feed.** Configure through a vendor (04 names SyncTrack, AfterShip, parcelLab, Malomo, Narvar; 05 adds Wonderment, ParcelWILL, Route) "without engineering resources". `[web check: vendor features, Shopify compatibility and pricing]` `[verify UI]`. Source 04; 05 lists vendors. Delight cluster. [73abfaadbe4c] [af9547313e6f]

**R78. Instrument recommendation clicks and linked purchases separately from raw page visits; visits are not revenue.** True Classic's plus 29% revenue per email, Crystal Classics' 50% to 60% call drop and Bokksu's 90% plus open rate are single vendor cases. Source 04 (delight cluster). [af9547313e6f] [73abfaadbe4c]

**R79. Map the top 10 pre-purchase objections and answer them on the product page, then route unanswered chat and support questions back into PDP content as a standing loop.** 04's examples: skincare (irritation, results timeline, price vs drugstore), furniture (fits through the door, assembly, colour accuracy). This is pre-purchase work that cuts post-purchase tickets and returns. Source 04 (delight cluster). `[needs brand data: top objections from tickets, reviews and chat]` [d2d7139dff02]

**R153. For cross-border orders, show landed cost (duties, taxes, customs fees) before checkout, not as a surprise on delivery, and put the customs status on the tracking page.** `[general practice]`. No source in this folder; verify against brand data before use.

### 3.12 Delivery and unboxing

**R80. Design the unboxing on purpose: it is the only physical touchpoint a digital brand controls and the natural peak in the peak-end map.** Sources 04, 05, 06 (delight cluster, all 3 drafts). [83291c925c2b] [bc838a699da9] [0372f28739d1]

**R81. Every order gets a standard insert (thank you, QR to a how-to video or loyalty signup); handwritten notes are reserved for high-value or VIP orders; an unexpected small gift goes in where the order type allows.** 04 cites about 80% of brands adding at least 1 customisation (ShipBob report, year not given) and 55% of shoppers more likely to rebuy after branded packaging (survey claim). Source 04 (delight cluster). Conflict C11: 04's insert carries a next-purchase discount code, 06 says no code. [83291c925c2b] [26ca8fa814e1]

**R82. Cap packaging spend at 2% to 5% of product cost (F22) and model insert cost per order at volume before adding layers.** Box cost is roughly fixed; insert cost multiplies per order. 05's bands: a branded moment under 0.50 per order, full premium 2.80 to 4.50, tissue 0.05 to 0.15 a sheet, sticker 0.04 to 0.05, card about 0.10. Source 05 (delight cluster). `[needs brand data: per-order packaging cost and monthly orders]` [bc838a699da9]

**R83. Layer the reveal (outer box, tissue, wrap, insert, product), add 1 script-breaking surprise, and include a first-use guide with a QR to a 60-second setup video.** 05 claims a 95% insert open rate vs about 20% for email (unsourced). Source 05 (delight cluster). [bc838a699da9]

**R84. Packaging weight, rigidity and texture are read as value within milliseconds; choose materials that match the one-line brand promise and walk a live order to catch any conflicting signal.** Premium: weighted glass, rigid setup boxes, matte or soft-touch laminates. Natural or authentic: raw board, linen-effect finishes. Premium tactile packaging on a "natural" brand reads as dissonance. The cited firm-vs-flimsy cup study is a perception effect, not proof of repeat purchase. Source 06 (delight cluster). [dfab0b08f391] [029011fd7e9d]

**R85. Put an unconditional gift in the box, not a conditional discount code.** The gift must be unadvertised, with no code, minimum spend, review or referral condition; budget it inside COGS against retention. A code creates transactional obligation and trains customers to wait for markdowns. Source 06 (delight cluster). Conflict C11. [f60a2e0fa1a5]

**R86. Notes must reference the exact item, carry a real signature or an item-specific merge field, be timed to arrival, and never be represented as personally handwritten when a machine wrote them.** Follow with a short "did it fit, did it work" check-in a few days later. Robotic handwriting vendors (06 names Handwrytten, triggered from Klaviyo or Gorgias events at milestones: high-value first purchase, subscription anniversary, VIP) are a claim to verify `[web check: Handwrytten pricing, pen quality, integrations]` `[verify UI]`. 06's cited note figures (99% open, up to 37% higher retention, about 100.5% higher spend) are vendor claims. Sources 05, 06, 04 (delight cluster). Conflict C10 on scale. [b056689936fe] [5f53155ff467] [83291c925c2b]

**R87. A cheap, irrelevant or clearance gift reads as landfill and cheapens the brand.** Match perceived value and relevance to the order. Even Chewy's surprise pet portraits were sometimes returned as confusing (05). Sources 05, 06 (delight cluster). [bc838a699da9] [f60a2e0fa1a5]

**R88. Treat packaging as a creative asset designed to be filmed, capture and repost the UGC, and count unboxing UGC volume as the metric for this spend.** Source 04 (delight cluster). [26ca8fa814e1] [7f71ff76f9b1]

**R154. Offer gift wrap and a gift receipt with the price hidden on packing slip and box, at checkout for any order marked as a gift.** `[general practice]`. No source in this folder; verify against brand data before use.

### 3.13 After delivery: education, reassurance, reviews, replenishment

**R89. Trigger a product education sequence about 48 hours after delivery confirmation (sooner for complex products): quick-start guide, video tutorial, common mistakes.** Include a tip not on the PDP. Build for the top 3 product categories first. 04 cites post-purchase emails opening "almost 17% higher" than average automations and a Freshly Cosmetics educational flow at 44.5% open, 2.81% click and over 10,000 euro (vendor cases). Source 04; 05 agrees education across the journey drives repeat (Beardbrand, Patagonia examples). Delight cluster. `[needs brand data: genuine post-purchase tips per product]` [862c6466d9cf] [491dd6d4221a] [55f0042df14c]

**R90. Send a reassurance message about 2 days after purchase ("you made the right choice") with a reassurance-toned subject.** 04 cites 47.4% open for one subscription brand (Klaviyo case). Source 04 (delight cluster). [491dd6d4221a]

**R91. Ask for honest reviews through the post-purchase flow, thank-you page and insert; never filter requests to satisfied buyers only, and ask for specific use cases and outcomes.** 07 adds that third-party customer content may influence LLM recommendations; treat that as a hypothesis, and never fabricate or gate reviews. 04's Knickey feedback-request note is the physical form. Sources 07, 04 (2 sources). Timing and copy in 14-EML. [291fd5b847c5] [83291c925c2b]

**R92. Time every post-purchase message to the order's real events (delivery confirmed, first use, usage cycle), not to the send date.** Replenishment prompts are sized to usage and pack size (F23). Sources 04, 05 (delight cluster). [491dd6d4221a] [6dcc8b256a6b]

**R93. Give subscriptions real flexibility: change cadence, skip, pause.** Rigid subscriptions drive cancellations and chargebacks. Source 05 (delight cluster). [6dcc8b256a6b]

**R94. A post-checkout upsell (larger size or adjacent item) is a separate, low-friction AOV lever; frame it as completing the purchase, not new selling.** No lift is quantified in the source (Yotpo guidance). Source 04 (delight cluster). [bd18309bf03e]

**R95. Where the brand holds genuine repeat-need expertise, education can extend into an always-on assistant tied to setup, usage, troubleshooting and replenishment; measure it by retention and repeat, not chat volume.** Source 07 (forecast, 1 source, no performance data on the L'Oreal example). Conflict C2. [52869049dbd3]

**R155. At the subscription cancel step, show a pause, skip or discount offer before the cancellation completes, alongside the flexibility R93 already requires; never make cancellation itself hard to find or complete.** Applies with R39's "cancelled" cohort as the retarget list if the save offer is declined. Sources warn only against a hard-to-cancel flow (05); no material on a proactive save offer. `[general practice]`. No source in this folder for the save-offer step; verify against brand data before use.

### 3.14 Returns and refunds

**R96. Treat returns as a retention fork, not a cost line.** 05 cites NRF and Happy Returns 2025 (2,006 consumers): 71% less likely to shop again after a poor return (67% in 2024), 80% tell friends and family, 76% more likely to choose a retailer offering instant refund or exchange. 04 cites 76% who will not rebuy after a poor return and 67% who check the policy before buying (unattributed). Delight cluster. [33d6b517ecb9] [0f70a58b8a2b]

**R97. Collapse the refund timeline from the traditional 10 to 14 days toward hours or minutes, and measure request-to-initiation and initiation-to-receipt separately by method (F18).** 04's cases (Reebok 11x repurchase and 63% faster repeat via Reshop; Razorpay wallet refunds 85% retention vs 40% to 50%; Origin minus 61% refund tickets via Loop; Auchan about 10 minutes; Bayse under 30 seconds; Riverford within 30 minutes) are vendor claims with no methodology; 04 itself notes the Reebok case does not establish causation. Source 04 (delight cluster). [0f70a58b8a2b]

**R98. Offer a clear choice between original-payment refund and store credit; never silently substitute credit to protect revenue.** Source 04 (delight cluster). [0f70a58b8a2b]

**R99. Before scaling faster refunds, measure return-fraud losses and cash-flow impact, and compare 60-day repurchase between instant-refund and standard-refund cohorts in a real test.** Source 04 (delight cluster). `[needs brand data: return fraud rate and cash position]` [0f70a58b8a2b]

**R100. Give returners a self-service portal, keep-it or donate-it refunds for low-value items, and clear exchange, credit and refund options.** Sources 05 (delight cluster); Zappos and Chewy examples. [33d6b517ecb9] [df383902e95d]

**R101. Publish the returns policy where shoppers look before buying, and check returns and refund law per ship-to market before any policy change.** `[web check: returns and refund law per market]`. Sources 04 (67% check the policy) and this playbook's compliance rule. [0f70a58b8a2b]

**R102. Gate returns work on returners' repeat rate: move on when it matches or beats non-returners (F18).** Source 05 (delight cluster). [33d6b517ecb9] [d6e5e929396b]

**R156. For cash-on-delivery orders, track return-to-origin (RTO) rate as its own cost line next to refund cycle time (F18); confirm the order by call or WhatsApp before dispatch on high-RTO lanes or first-time COD customers.** Central to India D2C economics. `[general practice]`. No source in this folder; verify against brand data before use.

**R157. Track chargebacks and payment disputes as a cost line separate from returns and refunds, with their own count and dollar total, and report both alongside F19.** Source 05 lists cancellations and chargebacks as a mistake, with no card id and no procedure; `[general practice]` for the rest. No source in this folder beyond that one line; verify against brand data before use.

### 3.15 Service recovery and support

**R103. In service moments, reduce effort: one-touch resolution, no repeat explanations, no dark patterns, refunds without escalation.** Evidence: the HBR 96% vs 9% effort finding (R58). Source 05 (delight cluster); 06 cites the same 96% figure. [df383902e95d] [bc11d5300f1f]

**R104. When a genuine failure happens, over-recover: a bad recovery costs more than a good one gains.** Refund without escalation, tell the customer to keep or donate the product where sensible, add a human gesture, replace same day where feasible. Keep it scoped to real failures; do not routinise "extra" fixes as a standing cost. Sources 05, 04 (delight cluster); 01 agrees a problem handled well can bring the customer back. 2 sources. [df383902e95d] [284b8c726776] [290bef9daa56]

**R105. Give frontline agents authority for one-time exceptions beyond policy for sympathetic cases (Flipkart's smartwatch exception, Chewy's 2,500 plus empowered reps).** Sources 04, 05 (delight cluster). [284b8c726776] [df383902e95d]

**R106. Build a staff checklist for the store's own edge cases before they happen: an order stuck in customs, a mis-shipped item, a stockout after the order confirms, a subscription payment failure. Do this during journey mapping, not live on a ticket.** Source 02 (1 source). [feb07cfa31b9] [41d67b919c4c]

**R107. Track first-contact resolution, CSAT and repeat rate among customers who had a failure, as a separate cohort.** Source 05 (delight cluster). [df383902e95d]

**R108. Shoppers rank "helped me when something went wrong" above generic friendliness and close to ease of checkout; treat a bad return or refund experience as a bigger trust hit than slow live chat.** In 02's live poll it ranked third, behind corporate attitude and ease of doing business, and ahead of product (sixth). This is one webinar audience, not a study; 02 says the order varies by category. Source 02. [fe0fd05d0bc2]

### 3.16 Support as a profit centre, AI agents and brand voice

**R109. Before any "profit centre" claim, establish 2 separate baselines: cost per contact and return per contact (F19).** Source 07 (direction only, no numbers, 1 source). [298b23ff39c4]

**R110. Resolve the issue first, then surface 1 relevant recommendation, non-intrusively, based on individual fit rather than best-sellers; monitor acceptance and complaint rates.** Requires complete and accurate customer, order and history context in the support tool. Source 07. [298b23ff39c4]

**R111. Automate high-volume, low-complexity contacts (order status first) and keep humans for emotional or complex cases.** 05 notes Gorgias as Shopify-native with brands reporting 64% to 95% AI resolution on order-status queries (vendor-reported). Sources 07, 05 (2 sources). `[web check: current AI support tool capabilities and pricing]` [298b23ff39c4] [6390a69c8430]

**R112. Before turning on an order-status bot, a return-authorization flow or a WISMO auto-reply, write down the brand's tone, the words it never uses, and how it should sound different from a generic support bot.** Have people who know the brand judge transcripts blind, and review for drift after every update. Generic bots flatten differentiation. Source 07 (opinion, 1 source). [7de1741d6532]

**R113. On handwritten notes, recovery emails and VIP messages, write in a human voice on purpose; do not let AI polish flatten the one moment meant to feel personal.** Test it. 07's claim that audiences lose attention when they notice AI polish has no test data. Source 07 (1 source). [a06a3fc0aa46]

**R114. Give AI budget to genuine post-purchase help (setup, troubleshooting, replenishment advice), not just ticket deflection, only in categories where the brand has real expertise to hand to the bot.** 07 cites an unnamed study; treat as a forecast. Source 07 (1 source). `[web check: locate the study 07 cites on why people use generative AI]` [27961d818a69]

### 3.17 Loyalty and VIP experience

**R115. Wait: build loyalty tiers and big surprise programs only once delivery, returns and support are reliable.** Source 05 roadmap step 6; 01's "VIP only if it is the constraint" (R43). 2 sources. [e6f325f479fd] [d6e5e929396b] [3de8a595a9bb]

**R116. Prefer experiential and status rewards (early access, events, line passes, recognition, exclusive content) over points-only discounts, most of all for Gen Z and fashion-driven bases.** 04's cases: Princess Polly 66% repeat among redeemers and 15.4x loyalty ROI; Sephora challenges tripling expected participation; Moroccanoil 5x ROI and 2.2x LTV; LeMieux app users 8x revenue per user (all vendor or brand claims). 04 does not claim this beats discounts in every category. Source 04; 01's exclusivity rule (R44) agrees. 2 sources. [8b6b2a3dbcb5] [90c580a2402c] [39c55eb82e67]

**R117. Integrate reward redemption into checkout and judge the program by redeemer vs non-redeemer repeat rate and LTV.** 04's Colorescience example: 30% vs 10% repeat (claim). Source 04 (delight cluster). [90c580a2402c]

**R118. Structure tiers around milestones and status, and message the top tier least (R36).** 05's Sephora example: 3 tiers (free, 350, 1,000), about 46 million members, about 80% of sales, Rouge retention "near 90%" (vendor write-up, flagged). Source 05 (delight cluster). [e6f325f479fd]

**R119. Re-engage lapsed customers with valuable content and segmented offers before generic discounts.** Matas case (04): 29-point retention lift in 30 days, plus 20% orders (vendor claim). Source 04 (delight cluster). [e13b48c6a15a]

**R120. Where the brand has a real shared activity (a run club, a restock alert group, a top-spender chat), build community around it as a retention channel AI cannot copy; do not launch a generic "community" tab with no activity behind it.** Examples: Lululemon, Nike Run Club in 07; Glossier's Slack for top shoppers in 05; LeMieux's app in 04. No measured outcome attached in any source. Sources 07 (forecast), 05 and 04 (examples). 2 sources, both thin. [6893cdd6a985] [90c580a2402c]

### 3.18 Win-back

**R121. Audit the lapsed list before any win-back send: if more than 20% has a support ticket, a return or a 1-star review, fix the experience first.** Source 05 (delight cluster). [5195356ba962]

**R122. Time the win-back off the customer's own cadence (RFM At Risk, R41) where the data exists; where it does not, send 30 to 45 days after the last purchase rather than 90 plus.** 05 cites a Klaviyo benchmark of 2.3x better conversion at 30 to 45 days vs 90 plus (vendor). Sources 01 and 05 disagree on the trigger: conflict C6. [98fc8eced08a] [5195356ba962]

**R123. Escalate the incentive across the sequence (no discount, then 10%, then 15%, then free shipping) rather than leading with a flat discount.** 05 cites Omnisend: escalation beats a flat discount by 34% (vendor). Source 05 (delight cluster). Copy and timing in 14-EML. [5195356ba962]

**R124. Segment win-back by reason for lapse (price, experience, product gap) and measure reactivation rate, revenue recovered and the subsequent 90-day repeat rate.** 05's benchmarks: 12% to 20% reactivation average, 20% to 35% top quartile; reactivation "5 to 10x cheaper" than acquisition (both unattributed). Source 05 (delight cluster). [5195356ba962]

### 3.19 Testing, prioritisation and roadmap

**R125. Prioritise retention tests by the identified constraint, in this order: 1 structure and timing (flow architecture, split order, cadence, segmentation, delays), 2 offers (size, structure, conditions, timing by stage), 3 messaging (copy, angles, creative).** Subject-line and delay tests are executor work, not the top-level agenda. Keep 1 person on retention strategy and profitability alongside executors. Source 01. [ebe1e2f78000]

**R126. Build the post-purchase roadmap in payoff order with an exit gate per step: 1 accurate delivery dates plus proactive tracking on a branded page (gate: WISMO under 5% of orders, post-purchase NPS stable); 2 easy, fast, kind returns (gate: short refund cycle, returners' repeat at or above non-returners); 3 unboxing peak plus first-use insert (gate: repeat and review rate rise); 4 replenishment and the 10-day second-purchase nudge (gate: 90-day repeat improves); 5 quiz personalisation (gate: quiz buyers show lower returns, higher AOV); 6 loyalty and VIP tiers; 7 gifts, notes at scale, community; 8 win-back automation after the list audit.** Source 05 (delight cluster); consistent with 01's hierarchy. [d6e5e929396b] [290bef9daa56]

**R127. Run the delight payback test (F20) with matched or randomised cohorts before scaling any packaging, note or gift program.** Source 06 (delight cluster). [8db0ffa97875]

**R128. A journey map of the post-purchase funnel (confirmation, tracking, wait, delivery, unboxing, support, return, repeat) only earns its keep if it changes one of those touchpoints; if nothing ships, it was a workshop exercise, not CX work.** Keep it as a living management tool, not a workshop deliverable. Sources 02, 06 (2 sources). [feb07cfa31b9] [0fe858c0c51f]

### 3.20 Personalisation, quizzes and zero-party data

**R129. Real personalisation changes what the customer sees or gets (quiz-driven fit, usage-timed replenishment); first-name tokens are not personalisation.** Source 05 (delight cluster); 03 agrees personalisation should shorten time to satisfaction. 04 adds on-site discovery cases: Kurt Geiger's adaptive homepage carousel (23.28% uplift) and GetGlowing's recommendations (about 22% of revenue), both vendor claims. 2 sources. [89e75eb0f016] [84c660fc619e] [9a5e68d31eee]

**R130. Earn personalisation data through a value-adding quiz the customer knowingly answers, not through opaque inference or third-party data; "creepy" personalisation risks immediate abandonment, a costlier failure than no personalisation.** Source 06; 01's zero-party rule (R54) agrees. 2 sources. [a40ceca4da16] [6bda120ef375] [e74d0b65f2db]

**R131. Keep the quiz short (05: about 5 questions), never funnel every answer to the same product, and measure completion, quiz-buyer AOV and quiz-buyer return rate against non-quiz buyers.** 06's Bare Anatomy example collects 75 plus data points and reports 35% lower CAC (third-party write-up, claim); 06 itself warns that long quizzes add friction. Test length against category consideration. Sources 05, 06 (delight cluster, with a length difference noted). [89e75eb0f016] [6bda120ef375]

**R132. Balance history-based personalisation against discovery, seasonality and testing; monitor whether recommendations narrow what shoppers see.** Source 03 (1 source). [84c660fc619e]

**R133. Pair personalisation with risk reversal and virtual try-on where the category supports it (apparel returns 30% to 50%; AR try-on reported to cut returns 25% to 45%, mixed vendor sources).** Source 05 (delight cluster). [89e75eb0f016]

### 3.21 CX strategy, ownership, maturity and voice of customer

Moved to Appendix A: general CX strategy theory (R134 to R143, source 02, plus B2B rule R141). R137, R138, R139 and R141 are still cited by id elsewhere in this playbook (P12, 5.4, section 8); look them up in Appendix A.

### 3.22 Search, discovery and buy vs build (from 03, a vendor interview)

**R144. Buy or use a Shopify-ecosystem app for search, ranking and merchandising unless the brand's edge genuinely is that engine; keep assortment, layout, supplier choice and merchandising judgment in-house.** 03's argument: retailers cannot out-hire big tech for engineering, and a gifting-company executive found self-built infrastructure ate the P&L and attention ("are we in the data centre business or the business of selling gifts?"). This is also Coveo's commercial position. Source 03 (1 source). Conflict C4. [ee1d80f4de9d]

**R145. Write the business objective and the allowed signals before any AI deployment, and pick the outcome metric in advance (margin per visitor, conversion, AOV).** No "AI for AI's sake". Treat any ranking model as probabilistic and monitor and correct it. Source 03. [800f306a36a5] [86cba9e8253e]

**R146. Rank by intent and business goal, not popularity alone; combine typed queries with browsing context and history.** Source 03 (examples: "BO" meaning boating, hunting or footwear by section; a footwear client lifting order value "substantially" by showing men's and kids' shoes next to women's). [86cba9e8253e]

**R147. Remove repeated logins and long page-throughs in cart, checkout and account flows; design for an interrupted user.** 03 cites about 1,400 digital interactions a day rising to 5,000 by 2025 (a 2022 research claim, unverified). Source 03; 05 and 06 give the checkout detail (R150). [668dd6245995]

**R148. Free merchandisers from manual monitoring (dead search terms, layout policing) so they work on assortment, supplier and persona strategy.** Source 03. [ee1d80f4de9d] [800f306a36a5]

**R149. Treat any markdown or clearance pricing used to defend share as a costed decision against the discount-cohort penalty (F24), not a default reflex in a slow week.** Source 03. [31f92baa2ab2]

**R150. Checkout is a pit to smooth, not a peak to build: show total cost including shipping and tax before the final step, offer guest checkout, add express pay for returning buyers, cut form fields toward the 7 to 8 strictly necessary (06 cites Baymard's roughly 15 average), and remove dark patterns (hidden subscriptions, pre-checked add-ons, fake urgency, hard-to-cancel flows).** 05 cites Baymard's 70.22% average abandonment (September 2025) with extra costs cited by 39% and forced account creation by 24% to 26% of abandoners. Watch failed orders and support contacts after cutting fields, not only abandonment. Sources 05, 06 (delight cluster); 02 agrees fake urgency erodes trust. Testing method in 09-CRO. [c7561c93445f] [1d8f5cd1000c] [30663f02bf6d]

### 3.23 Trends: where 07's predictions stop being rules

Source 07 is one presenter's annual forecast with no client data, no numbers with a method and 1 uncited study. Nothing in it is a rule on its own. The table says what each prediction is, what would make it a rule, and what the agent does now.

| Prediction (07) | Status | Becomes a rule when | What the agent does now | Card |
|---|---|---|---|---|
| Consumer search effort moves toward zero as AI agents shop and compare; a hypothetical agent rebuys a ticket on a roughly 10% price drop | Forecast, illustrative number | Brand data shows AI-referred sessions or agent traffic at a measurable share | Log referrer and agent traffic; do not build a pricing rule on the 10% | [257592d57c21] |
| The funnel collapses into 1 AI platform (inspiration, comparison, checkout) | Forecast; 07's own trigger is 10% to 20% of customers using that flow "12 months from now" | That share is observed on brand data | Map which funnel steps a customer could complete inside an AI platform; check platform commerce requirements quarterly `[web check]` | [7c1202336d90] |
| Algorithmic invisibility in LLM answers is a new discoverability risk | Forecast; 07 calls LLM ranking "a black box" with inconsistent results across runs | A meaningful minority of the audience starts category searches on AI platforms | Run the unbranded prompt audit (16-AEO) as a tracker; treat single runs as noise | [9d2f6feec1cd] |
| Third-party customer content is the strongest influence on LLM recommendations | Hypothesis, no method | Repeated prompt audits move after review or PR work | Collect honest reviews (R91); never fabricate or gate | [291fd5b847c5] |
| Support shifts from cost centre to profit centre | Direction, no numbers | F19 baselines exist and the ratio moves | Establish the 2 baselines (R109) | [298b23ff39c4] |
| Hyperpersonalisation as a 24/7 coaching assistant | Forecast, 1 named example without data | Retention and repeat rise for assistant users vs matched non-users | Only where genuine repeat-need expertise exists (R95); conflict C2 | [52869049dbd3] |
| Emotional value is AI's biggest untapped use | Opinion, unnamed study | The study is located and the brand tests an emotional-value use | Keep it on the roadmap watchlist | [27961d818a69] |
| Belonging as a service: human community as the differentiator | Forecast with examples only | Community members show higher repeat than matched non-members | Run community only where a real shared activity exists (R120) | [6893cdd6a985] |
| Un-AI-fication: imperfect human writing earns more trust | Observation, no data | An A/B on a trust-sensitive touchpoint shows it | Test it (R113) | [a06a3fc0aa46] |
| Brand agents with distinct voice, not generic bots | Recommendation | Any customer-facing bot is deployed | Apply the voice spec (R112) | [7de1741d6532] |

### 3.24 ecomOS rules that override any source

**E1.** All arithmetic runs in code in ecomOS. The model never computes a cohort figure, a ratio or a budget by hand. Every number the agent reports carries its formula label from 3.0 and its data window.

**E2.** A missing or unsupported input returns "unavailable", never 0. Period metrics are sums over sums.

**E3.** Vendor and brand case numbers are claims. When quoted they carry the word "claim" and the source, never "benchmark". Section 6's confidence column is the only place a number is graded.

**E4.** Customer-facing copy (support templates, confirmation and tracking messages, notes) uses short sentences, simple words, digits, no em dashes, no inflated words, reading level below tenth grade, concrete benefits, and no claim that is not in the brand record. Do not mention GPT or .env on client pages.

**E5.** Brands stay apart: Gehna, Peach Bucket and TrailFold data never mix in a cohort readout.

**E6.** Meta is read-only. The existing-customer budget in F13 is a recommendation to the user, never an ad-account write.

**E7.** Sources 04, 05 and 06 count as 1 source in every tally. A rule supported only by the delight cluster is "1 source" even when all 3 drafts state it.

**E8.** Where this playbook and 14-EML, 20-FIN or 06-MEA overlap, the definition in the owning folder wins (CM2 in 20-FIN, flow build in 14-EML, attribution in 06-MEA). This playbook owns LTGP windows, ratio bands, cohort repeat rate and the post-purchase journey.

## 4. Procedures (implementation)

Each procedure states its goal, preconditions, steps, the check after each step, and rollback. Platform steps carry `[verify UI]`. Arithmetic steps name the formula from 3.0 and run in code.

### P1. Build the cohort LTGP curve (Day 0 to 365)

Goal: a per-cohort LTGP series at 0, 30, 60, 90, 180 and 365 days, refunds included, from order-level data. Source 01. [2d30561e1938] [b4ff45d77f83]

Preconditions: order-level export with customer id, order date, revenue, refund lines; COGS per SKU; delivery cost per order; fee rate `[needs brand data: all 4]`.

1. Assign each customer to the cohort of their first order (week or month). Check: cohort sizes are pre-refund counts.
2. For each order compute gross profit per F1's components (revenue, COGS, delivery, fees, refund lines). Check: if revenue is already net of refunds, refund allowance is 0 (R4).
3. For each cohort and each W, sum gross profit from orders within W days of each customer's first order, divide by cohort size (F2). Check: Day-0 value equals the mean first-order gross profit.
4. Plot the curve per cohort; note the plateau month as the practical ceiling. Check: the curve is non-decreasing except where refunds land.
5. Refresh monthly; flag discount-period cohorts (R3).

Rollback: if COGS per SKU is missing for more than a set share of units, report LTGP as "unavailable" for that cohort rather than substituting an average margin.

### P2. Compute CAC, set the target and bound it

Goal: a CAC target that traces to a window and a ratio, plus a floor and realistic case. Source 01. [2d30561e1938] [3861489d8286] [f1d832540bbc] [2e9e88a22775]

1. Sum media spend across channels for the period; count new customers in the same period, pre-refund; compute F3. Check: the period matches the brand's scale (R5).
2. Choose the LTGP window by R7 (30-day default; 90-day for high-repeat or funded). Record the reason. `[needs brand data: revenue, capital, category]`
3. Pick the target ratio inside the 2 to 3 band unless the user states a funded-growth plan (F4). Compute F5. Check: the target is written as "LTGP_W / ratio = target".
4. Compute the floor and realistic case (F6) with new-customer conversion, not all-purchase conversion. Check: `paid_headroom` is reported with both inputs shown.
5. If considering a higher ceiling, forecast incremental customers per unit of ceiling (R8); fund only if the volume is meaningful.
6. Decide which side to work (R10): small paid headroom means LTGP levers (P3, R12); large means paid efficiency (06-MEA, 24-DEP).
7. Re-run quarterly.

Rollback: if new-customer conversion cannot be separated from returning, do not produce F6; report "unavailable" and say why.

### P3. Track CAC payback for a subscription or CPG brand

Goal: a payback day on the finance dashboard. Source 01; 06 for the delight variant. [d1160b9862c5] [8db0ffa97875]

1. Confirm the category has replenishment or subscription depth; stop if it is one-off or durable.
2. Compute `deficit_day0` (F7). Check: gp_day0 comes from P1, not an assumed margin.
3. Track cumulative cohort gross profit through time and mark `payback_day`.
4. Model working capital tied up while cohorts are in the red, per month of spend, before scaling.
5. List the levers that pull the date earlier: subscription attach, replenishment cadence, second and third purchase rate; assign 1 test each (P30).

Rollback: if the payback day exceeds the cash horizon the user states, recommend the 30-day window and first-order profitability instead.

### P4. Cohort readout

Goal: the standard readout in 9.1: repeat rate, F2 rate, LTGP curve, top-20% share, discount-code split, by cohort. Sources 01, 05. [9444eb58b437] [b4ff45d77f83] [3e09caf827f4] [34373cddcf01]

1. Pull the order-level export and build cohorts (P1 step 1).
2. Compute `repeat_rate_W` (F8) at 90 and 365 days per cohort. Check: never report Shopify's returning-customer percentage as this number (R15).
3. Compute `f2_rate_90` (F10) per cohort.
4. Compute LTGP at each W (P1).
5. Compute top-20% revenue and profit share for the trailing 12 months (F11).
6. Split each cohort by discount code (F24) and compute the penalty per code.
7. Grade repeat rate against F9 bands with the window stated and the caution that the bands are uncited.
8. Write 3 findings: the weakest of F1, F2, F3; the discount penalty if any; the cohort trend (improving, flat, worse).
9. Every figure carries its label, window and data date.

Rollback: if fewer than 3 mature cohorts exist at the window, report the trend as "not yet readable".

### P5. Diagnose the retention hierarchy before funding owned media

Goal: find which of product, portfolio, acquisition, CX or owned media is the constraint. Source 01. [290bef9daa56] [42e1ab9189e1]

1. Product quality: pull review text, support ticket themes, refund reasons, NPS if collected (P29 for method). Check: evidence is customer data, not founder opinion.
2. Portfolio: list cross-sell, upsell and replenishment paths per bestseller. Check: a reason to return exists for the top 3 SKUs; if not, the fix is product, not messaging (R25).
3. Acquisition quality: from P4, compare repeat and LTGP by channel, AOV band and discount code (R26, P10).
4. CX: run the post-purchase journey audit (5.2) and the support and returns audit (5.3).
5. Owned media: only now review engaged share (F12), flow coverage and cadence (14-EML).
6. Name the constraint and the evidence; route the next work to the matching section.

### P6. Find the F1, F2, F3 constraint and set the journey-stage structure

Goal: a constraint statement and the first-branch structure for every flow. Source 01. Build steps in 14-EML P9, P10, P12. [3c84840ee4fe] [ebe1e2f78000]

1. From P4, read acquisition volume (F1), `f2_rate_90` (F2) and `top20_share` (F3) against history and goals.
2. Name the weakest function. Check: under about 10 to 20 million a year expect F2 (R43).
3. Open every flow `[verify UI]` and check that the first split is new, returning, loyal or subscriber (R30). Log any linear or product-first flow (R31).
4. For the constrained function, go to its branch in every flow and list the gaps (R32).
5. Hand the build list to 14-EML with the constraint named.

Rollback: do not add a generic win-back flow or a blanket discount campaign as the response (R32).

### P7. Define the engaged audience and rebuild dormant reach

Goal: an engaged segment at or above 50% of the list and a monthly rebuild plan. Source 01. Klaviyo segment build in 14-EML P12. [83592aa3301a] [c5da5743237] [eacd1adfeb8d]

1. Set lookbacks by the brand's purchase cycle (01's examples: about 180 days email, 220 site actions, 280 orders). `[needs brand data: median days between orders]`
2. Build the segment `[verify UI]`; record `engaged_share` (F12).
3. Split the unengaged remainder into n equal random samples (01 used 10) (F25).
4. Each send, add 1 sample with the best content; after the send compute `newly_engaged_rate` and fold the newly engaged into the permanent segment. Check: the computed rate, not the presenter's rounded figure, is what gets reported (C5).
5. Repeat for 6 to 9 months; track `engaged_share` monthly as the KPI.
6. Schedule the full-list send for the next calendar peak once the base is rebuilt.

Rollback: if bounce or spam rate rises after a sample is added, halve the sample size and continue (deliverability rules in 14-EML).

### P8. RFM segmentation, lifecycle cohorts and VIP definition

Goal: RFM segments, lifecycle cohorts and a validated VIP definition. Source 01. [98fc8eced08a] [4d8506a387fd] [3de8a595a9bb]

1. Run RFM in the ESP's analytics tab `[verify UI]` relative to the brand's own base; export Champions, Loyal, Recent, At Risk, Needs Attention.
2. For subscription brands, build the 4 lifecycle cohorts (R39); for others, RFM or spend tiers.
3. Compute top-20% revenue and profit share (F11); compare with 01's pattern (about 50% and 80%). Record the brand's own numbers as the VIP definition.
4. Check the VIP-program leverage rule (R43): if F2 is the constraint, log VIP work as later.
5. Build the "Recent but not yet Loyal" segment as the first-to-second target, and "former Champion now At Risk" as the win-back target.
6. Replace fixed-day win-back triggers with RFM triggers (R41); hand to 14-EML.

### P9. Size an existing-customer paid budget (exception case only)

Goal: a dollar budget and a CPA target for existing-customer ads. Source 01. [675be3b57a10]

1. Confirm the exception: fashion or frequent-drop brand where email and SMS do not reach the whole base for new arrivals (R49). If not, recommend no spend.
2. Set the existing CPA target at half or less of the new-customer CPA (R50).
3. Compute F13 with frequency 4 to 7, existing-customer count and current CPM. `[needs brand data: existing customers, CPM]`
4. After 2 weeks, compute marginal CAC between spend levels (F14). Check: if marginal CAC exceeds the existing CPA target, cut spend to the lower level and reallocate to acquisition.
5. Report as a recommendation; Meta stays read-only (E6).

### P10. Discount-cohort audit

Goal: the LTGP and repeat penalty per discount code. Source 01. [34373cddcf01]

1. From P4, split cohorts by discount code taken on the first order (F24).
2. Compute `repeat_rate_90`, `repeat_rate_365` and `ltgp_90`, `ltgp_365` per group.
3. Compute `penalty` per code against the no-code group.
4. Weigh the front-end lift (ROAS, volume, from 06-MEA) against the penalty before scaling the promotion. Check: the recommendation states both sides in numbers.
5. Note 01's caution: some 9-figure retailers show no penalty; the brand's numbers decide.

### P11. Zero-party persona audit (top and bottom 20%)

Goal: the angle, persona and offer to overallocate toward, and the angles to exclude. Source 01. [e74d0b65f2db]

1. Collect zero-party data through the post-purchase survey or quiz (P29 rules on surveys; 06's quiz form in P12 step 6). `[needs brand data: survey or quiz responses joined to orders]`
2. Rank customers by 12-month revenue (or gross profit); take the top and bottom 20%.
3. For each group, tabulate persona, acquisition angle, first offer, refund and repeat rate.
4. Name the top-20% pattern to overallocate paid spend toward; name bottom-20% mismatches (01's "energy" angle on a skin supplement) to reduce or exclude, even where front-end ROAS looks strong (R55).
5. Hand angle changes to 10-MCR and 24-DEP.

### P12. Persona journey map with Kano classification and peak-end map

Goal: a single map that says, per touchpoint, whether to fix, hold or delight. Sources 02, 06, 05. [feb07cfa31b9] [0fe858c0c51f] [ff986b275489] [0372f28739d1] [36baf5a5a8ad]

1. Pick 1 persona: the highest-value cohort or the segment with the sharpest pain (R137).
2. Decide the intended experience in 1 sentence and check current processes can deliver it (02 step 1 and 2).
3. Plot actions, motivations and emotional states across consideration, purchase, wait, delivery, use, support, return, repeat. Convert each descriptive line to an emotional one.
4. Classify each touchpoint by Kano: must-be, one-dimensional, attractive (R62). Check: any must-be gap is logged as a fix, not as delight.
5. Tag each touchpoint as a service moment or a discretionary moment (R59).
6. Mark the current peak and end; mark any negative peak (R61).
7. Run "what if" scenarios per service moment and draft the staff checklist (R106).
8. Output: the fix list (must-be gaps and negative peaks), the 1 peak and 1 end to fund, and the touchpoint each change will alter (R128).
9. Re-audit on a cycle for delight decay (R63).

### P13. Post-purchase communication flow (confirmation to delivered)

Goal: at least 3 automated proactive updates plus education in the window. Sources 04, 05, 06. Klaviyo mechanics in 14-EML P9. [d17748ab5f3a] [6390a69c8430] [6d6e184eb848]

1. Count current automated touchpoints between order and delivery. Check: fewer than 3 triggers this build (R68).
2. Order confirmation: delivery estimate (P14), branded tracking link (P15), what happens next, 1 piece of value (R67). Use concrete words ("today", "update", "delivery").
3. Shipping confirmation: working branded tracking link.
4. Out for delivery: delivery window.
5. Add delivered and delayed messages (05).
6. For considered products, add education in the shipping window: prep, first-use sensations, realistic results timeline; last message sets up the unboxing (R72). Keep claims equal to the PDP.
7. Keep transactional messages focused; no promo cross-sell above the tracking info (R73).
8. Choose channel per audience: SMS for older bases, WhatsApp in India with opt-in `[web check]` (R75).
9. Check after launch: WISMO per order (F17) monthly; target under 3%, roadmap gate under 5%.

Rollback: if delivered-message timing misfires (carrier scan lag), remove the delivered message before removing any of the 3 core updates.

### P14. Delivery promise and DEA

Goal: a specific delivery date the brand usually beats, measured by F16. Source 05; 06 for the under-promise rule. [6177983af652] [3e09caf827f4] [9eb0da75866c]

1. Pull delivered-minus-shipped days by lane and carrier for the last 90 days plus handling time. `[needs brand data: carrier lane performance, handling time]`
2. Set the promise at a percentile that beats the estimate most of the time (05: "pad slightly"; 06: must still be competitive).
3. Show a specific date on PDP, cart and confirmation `[verify UI]`.
4. Compute DEA weekly (F16), counting overdue undelivered as misses. Check: above 0.90.
5. If DEA falls below 0.90 for 2 weeks, widen the pad for the failing lane, not all lanes.

### P15. Branded tracking page

Goal: tracking on the brand's domain with instrumented recommendations. Sources 04, 05. [73abfaadbe4c] [af9547313e6f]

1. Shortlist vendors `[web check: SyncTrack, AfterShip, parcelLab, Malomo, Narvar, Wonderment, ParcelWILL, Route: features, Shopify compatibility, pricing]`.
2. Point all tracking links in P13 messages to the branded page `[verify UI]`.
3. Populate: status, window, carrier, brand, 1 complementary recommendation, loyalty link, returns path (R77).
4. Turn on proactive delay alerts (R74).
5. Instrument recommendation clicks and linked orders separately from visits (R78).
6. Report monthly: visits per order, recommendation click rate, linked orders, WISMO per order before and after.

Rollback: keep the carrier link as a fallback line in the message for 30 days in case the page fails.

### P16. Unboxing protocol on a budget

Goal: a layered unboxing with a fixed per-order cost. Sources 04, 05, 06. [83291c925c2b] [bc838a699da9] [dfab0b08f391] [029011fd7e9d]

1. Write the brand's one-line promise; choose materials that match it (R84). `[needs brand data: brand promise, positioning]`
2. Set the packaging budget with F22 (2% to 5% of product cost) and model insert cost at current monthly orders. `[needs brand data: product cost per order, orders per month, 3PL insert capability]`
3. Standard for every order: layered reveal, 1 insert (thank you, QR to a 60-second first-use video or loyalty signup) (R81, R83).
4. Reserve handwritten notes for VIP and high-value orders (R81, P17).
5. Add 1 unconditional gift where the order type allows, relevant and unadvertised (R85, R87).
6. Walk a live order end to end and remove any conflicting signal (R84).
7. Measure: unboxing UGC count, review rate, repeat rate by cohort; run the delight payback test (P26) before scaling.

Rollback: if the insert stack exceeds the F22 band at volume, drop the lowest-value insert first, never the first-use guide.

### P17. Handwritten notes and gifts

Goal: notes and gifts that read as genuine and are costed. Sources 05, 06, 04. [b056689936fe] [5f53155ff467] [f60a2e0fa1a5]

1. Define triggers: high-value first purchase, subscription anniversary, VIP appreciation, a resolved failure (R86).
2. Write the note to reference the exact item; use a real signature or an item-specific merge field at scale; never a form letter and never claim "handwritten by staff" for a machine note.
3. If using a robotic vendor, evaluate pen and paper quality and integrations first `[web check: Handwrytten]` `[verify UI: Klaviyo and Gorgias triggers]`.
4. Pair with a sample matched to the purchase; time to arrival; follow with a "did it work" check-in a few days later.
5. Gifts: unconditional, no code, budgeted in COGS (R85).
6. Cost per send goes into P26.

### P18. Post-delivery education and review request sequence

Goal: education that cuts misuse returns and a review request that collects honest reviews. Sources 04, 05, 07. Email build in 14-EML P9. [862c6466d9cf] [491dd6d4221a] [291fd5b847c5]

1. Pick the top 3 categories by order share.
2. Trigger at delivery confirmation plus about 48 hours (sooner for complex products): quick-start, video, common mistakes (R89). Include a tip not on the PDP. `[needs brand data: product tips]`
3. Send the reassurance message about 2 days after purchase (R90).
4. Review request after the product has been used (timing by category, set in 14-EML); ask for specific use cases; no filtering to happy customers; also on the thank-you page and insert (R91).
5. Measure: open and click per message, return rate for misuse reasons before and after, review count and rating distribution.

### P19. Replenishment and second-purchase nudges

Goal: nudges timed to use, capped, with a stated incentive rule. Source 05; 04 for the timing principle. [6dcc8b256a6b] [491dd6d4221a]

1. Consumables: compute `usage_cycle_days` per SKU from pack size and usage or the observed median reorder interval (F23). `[needs brand data: usage cadence per SKU]`
2. Trigger at 0.75 of the cycle; cap at 2 messages a cycle; frame as usefulness.
3. Non-consumables: about 10 days after the first order arrives, 10% to 15% incentive aimed at relevant discovery (R34). Apply the conflict C7 rule: incentive only for the first-to-second step, none for loyal.
4. Subscriptions: offer change, skip, pause (R93).
5. Measure `f2_rate_90` by cohort before and after.

### P20. Faster-refund and returns test

Goal: a measured refund-speed change with fraud and cash controls. Sources 04, 05. [0f70a58b8a2b] [33d6b517ecb9]

1. Measure the baseline: `refund_cycle_days`, `refund_initiation_days`, return rate, `returner_repeat_rate_90` vs non-returners (F18). `[needs brand data: return and refund timestamps]`
2. Check returns law per ship-to market `[web check]` (R101).
3. Shortlist a returns or payments vendor for instant or fast refunds `[web check: Loop, AfterShip Returns, Narvar, Reshop, Refundid, Worldpay Faster Refunds, Razorpay: availability and pricing per market]`.
4. Offer the choice: original payment or store credit; never silent substitution (R98).
5. Add a self-service portal and keep-it refunds for low-value items (R100).
6. Run the test: instant-refund cohort vs standard cohort, 60-day repurchase, fraud losses, cash impact (R99).
7. Scale only if `gap` in F18 is at or above 0 and fraud stays inside the brand's tolerance.

Rollback: revert to standard refund timing for the affected market if fraud losses exceed the tolerance the user set.

### P21. Service failure recovery

Goal: a recovery that costs less than it gains and is measured. Sources 05, 04, 02. [df383902e95d] [284b8c726776] [feb07cfa31b9]

1. Detect: use tracking and order data to flag likely failures before the complaint (R74).
2. Reach out first with the fact, the fix and the timing.
3. Fix with the least customer effort: refund without escalation, replacement same day where feasible, keep or donate for low-value items (R104, R105).
4. Add a human gesture scoped to the failure; never routinise it.
5. Log the case in the failure cohort; track first-contact resolution, CSAT and 90-day repeat for that cohort (R107).
6. Feed the failure type back into the journey map's "what if" list (R106).

### P22. Support reply templates in voice

Goal: the deliverable in 9.4: templates for WISMO, late delivery, damaged or wrong item, return request, refund status, cancellation, product question, complaint escalation. Sources 07 (voice), 05 and 04 (recovery content), E4 (writing rules). [7de1741d6532] [a06a3fc0aa46] [df383902e95d] [284b8c726776]

1. Pull the brand voice guide and 3 examples of on-voice copy. `[needs brand data: voice guide, approved claims, policy limits]`
2. For each template write: 1 line that names the problem, 1 line with the fix and the date, 1 line with what the customer needs to do (or "nothing"), 1 human line in voice. Short sentences, digits, no em dashes, no inflated words (E4).
3. State only policy the brand record confirms (refund timing, exchange rules).
4. Mark variables in brackets: [order number], [date], [item].
5. Have someone who knows the brand read 3 templates blind and confirm the voice (R112). Check: no template reads as a generic bot.
6. Version the set; review after every policy or tool change.

### P23. Support as a profit centre: baselines

Goal: F19 baselines and a resolve-then-offer rule in the helpdesk. Source 07; 05 for the automation claim. [298b23ff39c4] [6390a69c8430]

1. Compute `cost_per_contact` and `return_per_contact` for the last 90 days. `[needs brand data: support cost, contact count, orders linked to contacts]`
2. Give agents and bots full order and history context `[verify UI: helpdesk integration]`.
3. Automate order-status contacts first (R111) `[web check: AI support tool capabilities]`.
4. Add a resolve-first, then 1 relevant recommendation rule; monitor acceptance and complaints (R110).
5. Report the ratio monthly; a rising ratio with flat complaints is the signal.

### P24. Loyalty tiers and experiential rewards

Goal: a tiered program that is measured by redeemer vs non-redeemer repeat. Sources 04, 05, 01. [8b6b2a3dbcb5] [90c580a2402c] [e6f325f479fd] [39c55eb82e67]

1. Confirm foundations: DEA above 0.90, WISMO under 5%, returner repeat gap at or above 0, support baselines exist (R115). If not, stop.
2. Confirm VIP revenue is the constraint or the brand is above the scale where VIP work has leverage (R43).
3. Define tiers by milestone and status from P8's VIP definition.
4. Choose rewards: early access, exclusive products, events, community, recognition; discounts last (R44, R116).
5. Integrate redemption into checkout `[verify UI]` (R117).
6. Measure redemption rate, redeemer vs non-redeemer repeat and LTV (F8 by segment).

### P25. Win-back campaign

Goal: a win-back that does not fire into unresolved service problems. Sources 05, 01. Copy in 14-EML P10. [5195356ba962] [98fc8eced08a]

1. Audit the lapsed list: share with an open ticket, a return or a 1-star review. If above 20%, fix the experience first (R121).
2. Trigger: RFM At Risk where available; otherwise 30 to 45 days after the last purchase (R122, C6).
3. Sequence: no discount, then 10%, then 15%, then free shipping (R123).
4. Segment by reason for lapse (R124).
5. Measure reactivation rate, revenue recovered, 90-day repeat among reactivated.

### P26. Delight payback test

Goal: a pass or fail on any delight program using F20. Source 06. [8db0ffa97875]

1. Establish CAC (P2) and first-order gross profit (P1). Compute the payback gap.
2. Estimate program cost per customer (packaging, gift, note).
3. Split matched or randomised cohorts: treated vs control, same acquisition period.
4. Observe over a mature window (at least the brand's median second-order interval, ideally 90 days); include refunds and the cost of remarketing, incentives and service on repeat orders.
5. Compute `incremental_contribution` and compare with program cost. Pass: contribution exceeds cost.
6. On fail: cut the per-order budget or change the program; do not change the accounting.

### P27. Retention roadmap in payoff order

Goal: the ordered build plan with exit gates. Source 05; consistent with 01. [d6e5e929396b] [290bef9daa56]

1. Run P5 to confirm the constraint is CX, not product or portfolio.
2. Order the work per R126 (delivery promise and tracking, returns, unboxing, nudges, quiz, loyalty, gifts and community, win-back).
3. Attach the exit gate metric and current value to each step. `[needs brand data: WISMO rate, DEA, refund cycle, repeat rates]`
4. Do not start a later step while an earlier gate is unmet, unless the user overrides in writing.
5. Review the gates monthly.

### P28. Moved to Appendix A: CX maturity assessment and ownership.

### P29. Voice of customer without annoying customers (reconciled C1)

Goal: product and experience evidence with surveys used only where they will be acted on. Sources 02, 01, 04, 06. [b24643e22b8c] [290bef9daa56] [7f71ff76f9b1] [bc11d5300f1f]

1. Own homework first: ticket themes, refund reasons, review text, returns reasons, WISMO and DEA data.
2. Ask the support and fulfilment team what customers think; only after a plan to act exists.
3. Talk to 5 to 10 customers directly, including returners and lapsed buyers.
4. If a gap remains that only customers can answer (the reason behind a purchase, zero-party persona data), run 1 short post-purchase survey with a named owner and budget to act. Keep it to the questions that will change a decision. Do not ask customers to check what the business should check itself (02's hotel-room example).
5. Report NPS or CSAT only alongside cohort repeat and contribution (R19).

### P30. Design a retention test

Goal: the deliverable in 9.3. Sources 01, 05, 06. [ebe1e2f78000] [8db0ffa97875] [d6e5e929396b]

1. Name the constraint from P4 to P6 (F1, F2 or F3) and the touchpoint from P12.
2. Pick the test class in order: structure and timing, then offer, then messaging (R125).
3. Write the hypothesis with the metric from 3.0 (for example `f2_rate_90`), the current value, the minimum change worth acting on, and the window.
4. Choose the split: randomised by customer where the ESP allows, else matched cohorts by acquisition week.
5. Set the readout date at the metric's window plus 2 weeks for refunds.
6. Pre-register the decision rule: ship, iterate or stop.
7. Log the test in the experiment registry (not built yet; keep a dated file under the brand folder until it exists).

### P31. Buy vs build for search, recommendation and data technology

Goal: a costed decision. Source 03 (vendor view; see C4). [ee1d80f4de9d] [800f306a36a5] [0272f48ebf68]

1. List what differentiates the brand (assortment, layout, supplier choices, persona) and keep it in-house.
2. List commodity capability (ranking, query understanding, catalog normalisation) as buy or partner candidates.
3. Estimate the ongoing cost of owning infrastructure (headcount, opportunity cost) against vendor track record.
4. Require any vendor to state the objectives the tool optimises for and which signals it uses.
5. Check per-SKU COGS quality before adopting margin per visitor (F21); if dirty, use MPV as directional only.
6. Record what the brand keeps as its own data moat (zero-party data, reviews, first-party behaviour) regardless of the vendor choice.

### P32. AI visibility, brand agent and trend watchlist

Goal: quarterly checks that turn 07's forecasts into observed data. Source 07. Full audit in 16-AEO. [9d2f6feec1cd] [7c1202336d90] [7de1741d6532]

1. Build a list of unbranded prompts an ideal customer would ask; run them across ChatGPT, Perplexity and Gemini on 3 separate days; record mentions and cited sources. Treat single runs as noise.
2. Log AI-referred and agent traffic share monthly. If it reaches a share the user sets (07's own heuristic is 10% to 20%), open a funnel review.
3. For any bot the brand runs, apply the voice spec and blind transcript review (P22 step 5).
4. Re-check platform commerce requirements quarterly `[web check]`.

## 5. Diagnostic checklists

Written so a worker can run each one. Each row: what to check, how, good, bad, fix, source.

### 5.1 Cohort readout

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| LTV is stated with a window | Read the retention dashboard labels | "30-day LTGP", "90-day LTGP" | Bare "LTV" or "lifetime value" | Rebuild per P1 | 01 [2d30561e1938] |
| LTGP comes from order lines | Ask how 90-day LTGP is built | Order and refund lines, refreshed monthly | AOV times assumed margin | P1 | 01 [2d30561e1938] |
| Refunds counted once | Trace refunds through CAC and LTGP | In LTGP only | In CAC, or in neither, or twice | R4 | 01 [2d30561e1938] |
| Repeat rate is cohort-based | Check the metric's formula | `repeat_rate_W` by cohort (F8) | Shopify "% returning customers" | R15, P4 | 01 [9444eb58b437] |
| Metrics are by cohort, not blended | Look for cohort columns | Every rate has a cohort and window | One blended number | R16 | 01, 05 [3e09caf827f4] |
| CAC target traces to a window and ratio | Ask for the calculation | "LTGP_W / ratio = target" written down | Target from habit or a competitor | P2 | 01 [3861489d8286] |
| Paid headroom known | Compute F6 | Floor well below realistic CAC | Floor near current CAC | Work the LTGP side (R10, R12) | 01 [f1d832540bbc] |
| Constraint named (F1, F2, F3) | Compare volume, `f2_rate_90`, `top20_share` to history | A clear, data-backed answer | "We don't know" | P6 | 01 [3c84840ee4fe] |
| Discount cohorts checked | F24 by code | Penalty known and accepted, or none | Never run | P10 | 01 [34373cddcf01] |
| Front-end ROAS cross-checked | Refund and repeat by angle | Downstream quality confirmed | High ROAS, support says mismatch | P11 | 01 [e74d0b65f2db] |
| Payback tracked (subscription, CPG) | F7 on the finance dashboard | Payback day and working capital modelled | Day-0 loss accepted without a date | P3 | 01 [d1160b9862c5] |
| Engaged share tracked | F12 monthly | At or above 0.50 and rising | Undefined or shrinking | P7 | 01 [c5da5743237] |
| Case numbers labelled | Read the readout | Every vendor or case figure says "claim" | Presented as benchmarks | E3 | 05 [4530efe6348a] |

### 5.2 Post-purchase journey audit

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Automated updates between order and delivery | Count them | 3 or more, plus delivered and delayed | Fewer than 3 | P13 | 04 [d17748ab5f3a] |
| Confirmation content | Read the email | Delivery estimate, branded tracking link, what next, 1 piece of value | Receipt only | R67 | 04 [d17748ab5f3a] |
| Delivery promise | Look at PDP, cart, confirmation | Specific date, built from lane data, padded | Vague range or carrier ideal SLA | P14 | 05 [6177983af652] |
| DEA | F16 weekly | Above 0.90 | Below, or overdue orders counted as pending | P14 | 05 [3e09caf827f4] |
| WISMO per order | F17 monthly | Under 0.03 | Above 0.08 (structural), or above 0.05 blocks the roadmap | P13, P15 | 05 [6390a69c8430] |
| Tracking destination | Click the link in the shipping email | Brand domain page with recommendations and returns path | Carrier page | P15 | 04 [73abfaadbe4c] |
| Tracking page instrumented | Look at reporting | Recommendation clicks and linked orders separate from visits | Visits only | R78 | 04 [af9547313e6f] |
| Education in the wait (considered products) | Read the shipping emails | Prep, first-use, realistic timeline, claims match PDP | Bare tracking link or inflated claims | R72 | 06 [6d6e184eb848] |
| Transactional emails focused | Read them | Tracking info first, no promo cross-sell | Cross-sell above the tracking info | R73 | 06 [6d6e184eb848] |
| Peak and end identified | P12 map | Positive peak (unboxing) and reassuring end | Negative peak live, or abrupt end | R60, R61 | 06 [0372f28739d1] |
| Must-be gaps | Kano pass in P12 | None open | Delight spend while a must-be is broken | R62 | 06 [ff986b275489] |
| Unboxing protocol | Open a live order | Layered reveal, insert with QR, coherent materials | Bare box, or materials contradicting the promise | P16 | 05, 06 [bc838a699da9] [029011fd7e9d] |
| Packaging cost in band | F22 | 2% to 5% of product cost | Above, or insert stack unmodelled at volume | P16 | 05 [bc838a699da9] |
| Gift type | Check the box | Unconditional, relevant | Conditional code as the "gift", or clearance item | R85, R87 | 06 [f60a2e0fa1a5] |
| Notes | Read one | References the item, real signature, honest about how it was made | Form letter, or machine note claimed as staff-written | R86 | 05, 06 [b056689936fe] [5f53155ff467] |
| Education after delivery | Check the flow | Trigger at delivery plus 48 hours, 3 messages, top 3 categories | None, or send-date based | P18 | 04 [862c6466d9cf] |
| Review request | Check the flow, page, insert | Honest, unfiltered, asks for use cases | Filtered to happy buyers, or absent | R91 | 07 [291fd5b847c5] |
| Replenishment timing | F23 per SKU | 0.75 of cycle, max 2 a cycle | Fixed day count, or more than 2 | P19 | 05 [6dcc8b256a6b] |
| Second-purchase nudge | Check the flow | About 10 days after arrival for non-consumables | Absent, or the same discount for everyone | P19, C7 | 05 [6dcc8b256a6b] |
| Journey stage split | Open each flow | First branch new, returning, loyal | Linear or product-first | P6 | 01 [3c84840ee4fe] |
| First-time, repeat, VIP tracks | Compare flows and on-site experience | Different content per tier | Identical | R35 | 04 [e13b48c6a15a] |
| Delight decay | Metric trend per funded delighter | Still moving | Flat while spend continues | R63 | 06 [a4e3c81ce639] |
| Delight spend justified | P26 | Payback test run and passed | Budget from taste | R127 | 06 [8db0ffa97875] |

### 5.3 Support and returns audit

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Ticket mix | Tag tickets by type | WISMO share known and falling | Untagged, or WISMO above 50% outside peak | P13, P23 | 05 [6390a69c8430] |
| Effort in service moments | Walk a return and a WISMO contact as a customer | One touch, no repeat explanations | Escalations, repeated logins, forms | R103 | 05 [df383902e95d] |
| Agent authority | Ask what an agent can do without approval | Refund, replace, one-time exception, keep-it | Everything escalates | R105 | 04, 05 [284b8c726776] |
| Proactive outreach | Look for stalled-parcel alerts | Brand reaches out first | Customer finds out first | R74 | 04, 05 [73abfaadbe4c] |
| Recovery is over-recovery, not engineered | Read recovery cases | Fix plus a scoped gesture on real failures | "Extra" fixes routinised, or failures tolerated for recovery moments | R65, R104 | 05 [df383902e95d] |
| Failure cohort measured | Look for the cohort | FCR, CSAT, 90-day repeat for customers who had a failure | Not tracked | R107 | 05 [df383902e95d] |
| Returns policy visible | Check PDP and footer | Findable before purchase, lawful per market | Hidden, or unchecked against law | R101 | 04 [0f70a58b8a2b] |
| Refund cycle | F18 | Hours or minutes from request | Days; measured from warehouse scan | P20 | 04, 05 [0f70a58b8a2b] |
| Refund choice | Read the returns flow | Cash or credit offered clearly | Credit substituted silently | R98 | 04 [0f70a58b8a2b] |
| Returner repeat gap | F18 `gap` | At or above 0 | Returners repeat less | P20 | 05 [33d6b517ecb9] |
| Fraud and cash controls | Ask | Fraud rate and cash impact tracked before scaling fast refunds | Not tracked | R99 | 04 [0f70a58b8a2b] |
| Support baselines | F19 | Cost per contact and return per contact both tracked | Neither | P23 | 07 [298b23ff39c4] |
| Offer timing in support | Read transcripts | Resolve first, 1 relevant offer, non-intrusive | Upsell before resolution | R110 | 07 [298b23ff39c4] |
| Automation scope | Check the bot's routing | Order status automated; emotional and complex to humans | Everything or nothing automated | R111 | 07, 05 [298b23ff39c4] |
| Voice | Blind transcript read | Recognisably the brand | Generic bot phrasing | P22 | 07 [7de1741d6532] |
| Templates | Read 3 | Short sentences, digits, policy matches record | Inflated words, invented policy | E4 | ecomOS |
| Lapsed list health | Share with ticket, return or 1-star | Under 20% | Over 20% | R121 | 05 [5195356ba962] |
| Staff checklists for "what if" cases | Ask for them | Exist per service moment | None, or over-scripted | R106 | 02 [feb07cfa31b9] |

### 5.4 Experience-fix prioritisation

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Foundations before delight | Compare DEA, WISMO, refund cycle with any delight project in flight | Foundations healthy, then delight | Delight shipping while a foundation is broken | R58, R126 | 04, 05, 06 [b233a6d834e6] |
| Kano class per candidate fix | P12 step 4 | Must-be gaps ranked first | Attractive items funded first | R62 | 06 [ff986b275489] |
| Negative peak found | P12 step 6 | Identified and scheduled first | Unknown | R61 | 06 [0372f28739d1] |
| Service vs discretionary tagged | P12 step 5 | Effort fixes in service moments, peaks in discretionary | Delight attempted in a service moment | R59 | 05 [36baf5a5a8ad] |
| Expected effect stated | Each fix has a metric from 3.0, current value and expected direction | Yes, with the claim labelled | "Should help" | 9.2 | ecomOS |
| Roadmap order respected | Compare with R126 | Steps in payoff order with gates | Loyalty before delivery and returns | P27 | 05 [d6e5e929396b] |
| Cost modelled at volume | F22 | Insert and gift cost per order at current and 2x orders | Per-unit only | P16 | 05 [bc838a699da9] |
| Coherence with brand promise | P16 step 6 | All signals match | A mismatch | R84 | 06 [029011fd7e9d] |
| Persona named | P12 step 1 | 1 persona per map | All customers at once | R137 | 06 [0fe858c0c51f] |
| Fix changes a touchpoint | Read the plan | Each item names the touchpoint it alters | Map without changes | R128 | 02, 06 [feb07cfa31b9] |

### 5.5 Retention play review

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Constraint named | P4 to P6 | F1, F2 or F3 with evidence | Not named | P6 | 01 [3c84840ee4fe] |
| Hierarchy checked first | P5 | Product, portfolio, acquisition, CX cleared | Jumped to email or loyalty | R23 | 01 [290bef9daa56] |
| Test class in order | R125 | Structure, then offer, then messaging | Subject-line test as the play | P30 | 01 [ebe1e2f78000] |
| Metric and window pre-set | Read the plan | Formula from 3.0, current value, minimum change, readout date | Vague success | P30 | ecomOS |
| Split valid | Read the plan | Randomised or matched by acquisition week | Before vs after only | P30 | 06 [8db0ffa97875] |
| Incentive rule stated | Read the plan | Who gets an incentive and who does not (C7) | Blanket discount | R34, R36 | 01, 05, 06 |
| VIP work justified | R43 | VIP is the constraint or scale supports it | VIP program while F2 is weak | R43 | 01 [3de8a595a9bb] |
| Existing-customer spend justified | R49 | Exception case confirmed, CPA at half | Same CPA as new, or no marginal check | P9 | 01 [675be3b57a10] |
| Win-back list audited | R121 | Under 20% unresolved | Not checked | P25 | 05 [5195356ba962] |
| Claims labelled | Read the plan | Vendor figures say "claim" | Presented as expected results | E3 | 05 [4530efe6348a] |
| Decision rule pre-registered | Read the plan | Ship, iterate, stop conditions | Decide after seeing data | P30 | ecomOS |
| Logged | Experiment file | Dated entry | None | P30 | ecomOS |

## 6. Thresholds and benchmarks

All values are flags, not targets, unless brand data confirms them. Confidence counts independent sources (04, 05 and 06 count as 1, labelled D). Basis says whether the number is a stated formula, an operator heuristic, a cited study, or a vendor claim.

| Metric | Value | Condition | Source | Confidence |
|---|---|---|---|---|
| LTV base | Gross profit, never revenue | Always | 01; 03 agrees on margin | 2 sources, definition |
| LTGP windows | 0, 30, 60, 90, 180, 365 days | Cohort curve | 01; D (05) agrees on cohorts | 2 sources |
| Default LTGP window | 30-day; 90-day for CPG, supplements, funded | By capital and category | 01 | 1 source, heuristic |
| LTGP:CAC below 1 | Losing money | Any window | 01 | 1 source, heuristic; 20-FIN agrees |
| LTGP:CAC 1 to 2 | Inefficient, needs working capital | Any window | 01 | 1 source, heuristic |
| LTGP:CAC 2 to 3 | Target scaling band | Any window | 01 | 1 source, heuristic; 20-FIN agrees |
| LTGP:CAC above 3 | Leaving money on the table | Any window | 01 | 1 source; conflict C9 with 20-FIN sources |
| Window change effect | 30-day to 90-day raised the ceiling 25% | Worked example only | 01 | Example |
| Volume test for a higher ceiling | Worth it at about 30% to 40% more customers per 10 unit rise | Example | 01 | Example |
| Loan-funded long payback | "Incredibly risky" under about 15 to 20 million a year | Aggressive model | 01 | 1 source, opinion |
| CAC period | Daily or hourly (9 to 10 figures); weekly or monthly (6 to 8 figures) | By scale | 01 | 1 source, heuristic |
| CAC floor example | 0.70 CPC / 0.03 = 23.33 | Best case | 01 | Example |
| CAC realistic example | 1.00 CPC / 0.02 = 50 | Actual | 01 | Example |
| Payback deficit example | 50 CAC, 45 Day-0 GP, deficit 5 | CPG | 01 | Example |
| Delight payback example | 20 CAC, 10 first-order margin, 3 delight cost, assumed 50% retention lift | Illustration | D (06) | Example, assumed lift |
| Second purchase | Only about 20% buy twice from about 80% of brands | Framing stat | 01 | 1 source, observation |
| RPR bands | Under 20% problem; 20 to 30 average; 30 to 40 good; above 40 excellent | Window unstated | D (04) | 1 source, uncited heuristic |
| DTC 12-month repeat | About 28.2% average; 9.9% luxury to 65.2% grocery; 18.8% in one 156,110-customer set | 12 months | D (05) | Vendor datasets, claim |
| Average retention rate | 30% to 40% | "Baseline industry figure" | D (06) | Cited, unverified |
| Indian D2C 12-month repeat | About 23% to 25% | Directional | D (05) | Second-hand, unverified |
| First-to-second conversion "done well" | 25% to 30% | Non-consumables with nudge | D (05) | 1 source, estimate |
| Top-20% share (VIP pattern) | About 50% plus of revenue, about 80% of profit | Validate on brand data | 01 | 1 source, heuristic |
| VIP program leverage | Above about 10 to 20 million a year | Below: F2 is the constraint | 01 | 1 source, heuristic |
| Engaged share | At least 50% of list | Default target | 01 | 1 source, heuristic |
| Engaged lookbacks | About 180 (email), 220 (site), 280 (orders) days | Example | 01 | Example, adapt |
| Dormant rebuild | 10 random samples, 6 to 9 months | Method | 01 | 1 source, method |
| Ready-to-buy share of list | About 3% | Illustration | 01 | Opinion |
| Campaign split | 80% reach, 20% specific goal | Heuristic | 01 | 1 source; conflict C2 |
| Email share of revenue | 30% to 50% | Soft indicator, attributed | 01 | 1 source, "not hard science" |
| Campaign incrementality | 70% to 80% of campaign revenue, some accounts | Unnamed studies | 01 | 1 source, unverified |
| Existing-customer CPA | Half or less of new-customer CPA | Exception case only | 01 | 1 source, heuristic |
| Existing-customer frequency | 4 to 7 a month | F13 | 01 | 1 source, heuristic |
| Existing-customer marginal CAC example | 1,000 vs 700 a day: 3 conversions at 100 each | Example | 01 | Example |
| Discount-cohort penalty | About 60% of 01's clients see substantially worse LTV; some 9-figure retailers none | Check own data | 01 | 1 source, generalisation |
| Spend tiers (non-subscription) | 500, 1,000, 3,000 | Example | 01 | Example |
| Effort and disloyalty | 96% of high-effort customers more disloyal vs 9% low-effort | Service interactions | D (05, 06 both cite) | 1 source citing HBR 2010, 75,000 plus interactions; strong basis |
| Service recovery paradox rate | 5.4% (63 of 1,189) | Banking, exceptional recovery only | D (05) | 1 source citing academic study |
| Peak-end | Memory = peak plus end | Replicated psychology; 2022 meta-analysis of 174 effects | D (05, 06) | 1 source, strong basis |
| Delight belief gap | 87% of brands vs 11% of shoppers | General | D (04) | Unattributed claim |
| Post-purchase anxiety | Two-thirds of shoppers | Right after buying | D (04) | Unattributed claim |
| Minimum proactive updates | 3 | Order to delivery | D (04) | 1 source |
| 3-step flow WISMO cut | "Up to 80%" | Claim | D (04) | Vendor-style claim |
| WISMO share of tickets | 30% to 50% normal; 50% to 80% peak | Vendor-consistent | D (05) | 1 source, vendor range |
| WISMO per order bands | Under 3% healthy; 3 to 8% normal but expensive; above 8% structural | F17 | D (05) | Vendor guide |
| WISMO roadmap gate | Under 5% of orders | Move to step 2 | D (05) | 1 source, heuristic |
| DEA target | Above 90%; vendor case above 95% | F16 | D (05) | 1 source, heuristic |
| Late delivery | 74% got a package later than estimated in the past year | US, 2025 | D (05) | Narvar survey, 3,461 people, vendor |
| Delivery priority | Speed fell from number 1 (2022) to number 5 (2024) | Consumer ranking | D (05) | McKinsey via vendor |
| Specific date conversion lift | 13% to 25% over a vague range | Claim | D (05) | Forrester via Narvar, vendor |
| Tracking visits per order | 4.6 | General | D (04) | Unattributed claim |
| Branded tracking effects | 23% to 31% repeat lift; 9 to 12x ROI; 40% to 60% WISMO cut | Claims | D (04) | Vendor frameworks |
| Branded tracking cases | True Classic plus 29% revenue per email; Crystal Classics 50% to 60% call drop, plus 78% CTR; Bokksu 90% plus open, 45.7% CTR; IWA minus 47% WISMO | Single cases | D (04) | Vendor case studies |
| Packaging budget | 2% to 5% of product cost | Unboxing | D (05) | 1 source, heuristic |
| Packaging cost bands | Under 0.50 branded; 2.80 to 4.50 premium; tissue 0.05 to 0.15; sticker 0.04 to 0.05; card about 0.10 | Per order | D (05) | Source compilation |
| Insert scaling | 0.60 to 0.80 stack material at 2,000 orders a month | Volume | D (05) | Source arithmetic |
| Insert open rate | 95% vs about 20% email | Claim | D (05) | Unsourced |
| Branded packaging | 55% more likely to rebuy; about 80% of brands customise | Survey claims | D (04) | Survey and ShipBob report, year unknown |
| Handwritten note effects | 99% open; up to 37% higher retention; about 100.5% higher spend | Claims | D (06) | Vendor data |
| Post-purchase email opens | About 17% higher than average automations | Claim | D (04) | Unattributed |
| Reassurance email | 47.4% open at 2 days | 1 brand | D (04) | Klaviyo case |
| Education flow | 44.5% open, 2.81% click, over 10,000 euro | Freshly Cosmetics | D (04) | Vendor case |
| Education trigger | Delivery plus 48 hours | Sequence start | D (04) | 1 source |
| Replenishment trigger | 75% of usage cycle; max 2 per cycle | Consumables | D (05) | 1 source, recommendation |
| Replenishment conversion | 8% to 15% vs 1% to 3% general promos | Claim | D (05) | Vendor benchmark |
| Second-purchase nudge | About 10 days after arrival; 10% to 15% incentive | Non-consumables | D (05) | 1 source; conflict C7 |
| Bad return churn | 71% less likely to shop again (67% in 2024); 80% tell others; 76% prefer instant refund or exchange | Consumers | D (05) | NRF and Happy Returns 2025, 2,006 people; credible body |
| Poor returns | 76% will not rebuy; 84% less likely; 67% check policy first | Claims | D (04) | Unattributed |
| Instant refund cases | Reebok 11x repurchase, 63% faster; Razorpay 85% vs 40% to 50%; Origin minus 61% tickets; Auchan about 10 minutes; Bayse under 30 seconds; Riverford within 30 minutes | Single cases | D (04) | Vendor claims, no causation |
| Instant refund general | 23% higher repurchase in 30 days; smooth first return 3x more likely to rebuy in 60 days | Claims | D (04) | Unattributed |
| Repeat customer spend | 67% more than first-time | Claim | D (04) | Unattributed |
| Retention to profit | 5-point retention gain gives 25% to 95% profit gain | Financial services, 1990 | D (04, 05) | Reichheld and Bain, old, other industry |
| Acquisition vs retention cost | 5x to 25x | Directional, old | D (05) | Repeated derivation |
| Cart abandonment | 70.22% average | 50-study meta-analysis, Sept 2025 | D (05) | Baymard, credible |
| Abandonment causes | Extra costs 39%; forced account 24% to 26% | 2024 survey, n = 4,329 | D (05) | Baymard-cited |
| Checkout fields | About 15 average vs 7 to 8 necessary | Checkout | D (06) | Baymard-cited |
| Payment option display | Up to 30% faster checkout, up to 12% less abandonment | Claim | D (06) | Unnamed |
| Shop Pay | Up to 50% lift vs guest; 5% from presence | Claim | D (05) | Shopify-commissioned |
| Quiz length | About 5 questions | Guided selling | D (05) | 1 source; 06 case uses 75 plus data points |
| Quiz case | 80% completion, plus 16.4%; supports 80% of the business | Function of Beauty | D (05) | Vendor case |
| Quiz case | 35% lower CAC; 150 crore INR in 5 years | Bare Anatomy | D (06) | Third-party write-up |
| Apparel returns | 30% to 50%; AR try-on cuts 25% to 45% | Category | D (05) | Mixed vendor |
| Win-back list audit | Fix experience if over 20% have a ticket, return or 1-star | Prep | D (05) | 1 source, recommendation |
| Win-back timing | 30 to 45 days after last purchase; 2.3x vs 90 plus | Claim | D (05) | Klaviyo benchmark; conflict C6 |
| Win-back reactivation | 12% to 20% average; 20% to 35% top quartile | Claim | D (05) | Industry benchmark |
| Incentive escalation | Beats flat discount by 34% | Claim | D (05) | Omnisend |
| Reactivation cost | 5 to 10x cheaper than acquisition | Claim | D (05) | Unattributed |
| Loyalty cases | Princess Polly 66% repeat, 15.4x ROI; Moroccanoil 5x ROI, 2.2x LTV; LeMieux 8x revenue per app user; Colorescience 30% vs 10%; Matas 29 points in 30 days | Single cases | D (04) | Vendor claims |
| Sephora Beauty Insider | About 46 million members, about 80% of sales, Rouge retention near 90% | 1 brand | D (05) | Press and vendor, flagged |
| NPS benchmarks | About 50 average, 70 plus world class | Ecommerce | D (06) | Cited industry, unverified |
| NPS and repeat | NPS above 50 gives repeat 15 to 20 points higher than NPS below 30 | Directional | D (05) | Vendor |
| WhatsApp journeys (India) | 11.12% CTR, opens up to 73.9%; broadcasts 2.6%; 83% of festive orders from first-time buyers | India | D (05) | GoKwik, 26 billion messages, vendor |
| AI support resolution | 64% to 95% on order status | Some brands | D (05) | Vendor-reported (Gorgias) |
| CX maturity split, Consumer stats, Favourite-brand drivers | Moved to Appendix A (general CX theory, source 02) | | | |
| Digital interactions | About 1,400 a day, 5,000 by 2025 | 2022 research | 03 | 1 source, unlinked |
| Retail margin | About 6% falling toward about 2% by 2024 to 2025 | Forecast | 03 | 1 source, forecast |
| B2B order profile | About 70 lines, about 500,000; 5 to 10 plus touchpoints | Guest's clients | 03 | 1 source, anecdote |
| Margin case | 72% margin boost | 1 Coveo customer | 03 | Vendor claim |
| AI funnel trigger | 10% to 20% of customers using an AI-platform funnel | Heuristic | 07 | 1 source, forecast |
| Agent repricing trigger | About 10% price drop | Hypothetical | 07 | Illustration only |

## 7. Where sources disagree

Each conflict: what each side says, when each is right, what the agent should do.

**C1. Post-purchase surveys: yes or no.** 02 says do not measure customers with things that annoy them; surveys mostly serve ego or staff pressure; do your own homework, ask employees, talk to customers. 01 says audit product quality with surveys, NPS and verbatims, and collect zero-party data via post-purchase surveys. 04 wants delight metrics alongside CSAT and NPS; 05 gates roadmap steps on post-purchase NPS; 06 tracks NPS, CSAT and CRR. When each is right: 02 is right that a survey with no budget to act on it is worse than none, and that the business should check its own quality; 01 and the delight cluster are right that zero-party persona data and objection text only come from the customer. What the agent does: run P29. Exhaust owned data and employee input first; survey only for questions that will change a decision, with an owner and budget; never ask the customer to check what the business should check; report survey scores only next to cohort repeat and contribution. [b24643e22b8c] [290bef9daa56] [e74d0b65f2db] [7f71ff76f9b1] [bc11d5300f1f]

**C2. Hyperpersonalisation vs reach-first 80/20.** 01 rejects hyperpersonalisation as the default campaign strategy: 80% reach, 20% specific goal, personalise only in flows. 07 says hyperpersonalisation is under-scoped and should become a 24/7 coaching assistant. 03 says personalised discovery shortens time to satisfaction and defends against Amazon. 05 and 06 say real personalisation changes what the customer gets (quiz, replenishment timing) and first-name tokens are weak. When each is right: 01 is talking about campaign sends to a list, where labour cost and fragmentation are real and where a large engaged base cashes in at peaks; 07, 03, 05 and 06 are talking about behaviour-triggered flows, on-site discovery and product fit, which 01 itself says is where personalisation belongs. What the agent does: campaigns run 80/20 reach-first (R45); personalisation lives in flows, on-site recommendations and quiz-driven fit (R47, R129, R131); a coaching assistant is a forecast to test only where the brand has repeat-need expertise (R95). Do not present 07's assistant as a proven retention lever. [097d09066f7a] [3121e4d083d4] [52869049dbd3] [84c660fc619e] [89e75eb0f016]

**C3. Delight vs effort.** 02 says emotion drives behaviour and CX is where a brand competes. 07 says emotional value is AI's biggest untapped use. 04, 05 and 06 say delight must sit on top of effortlessness; 05 calls the "delight pays" case contested and the effort evidence strong (96% vs 9%). 06 says delight decays into baseline. When each is right: 02 and 07 describe the intended outcome (a feeling); the delight cluster describes the order of operations (remove effort in service moments, then build 1 peak in a discretionary moment). What the agent does: R58, R59, R60 in that order; fund delight only through P26; label delight programs as brand and word-of-mouth plays until brand data proves them (R66). [30663f02bf6d] [27961d818a69] [b233a6d834e6] [36baf5a5a8ad] [a4e3c81ce639]

**C4. Buy vs build for search and data technology.** 03 (a Coveo GM) says buy or partner for search, recommendations and personalisation and keep only brand-differentiating decisions in-house. 06 and 01 say zero-party data earned through a quiz or survey is the safe personalisation source and 07 says brand agents need a distinct voice, which implies owning the data and the voice layer even when the engine is bought. No source in this folder argues for building search in-house; the counter-position is the general "own your data and core tech" view that 03's own mini playbook flags. When each is right: 03 is right for the engine (ranking, query understanding, catalog normalisation) at most brand scales; the own-your-data view is right for the inputs (zero-party data, reviews, first-party behaviour) and the voice. What the agent does: P31: buy the engine, own the data and the voice, require the vendor to state objectives and signals, and mark the decision as 03's commercial position when presenting it. [ee1d80f4de9d] [6bda120ef375] [e74d0b65f2db] [7de1741d6532]

**C5. Arithmetic slips and repeat-rate figures.** (a) 01's spoken case: 375,000 engaged plus a 37,500 sample is 412,500, the presenter said "about 410,000"; 7,000 newly engaged of 37,500 is 18.7%, the presenter said "20 or 30%". (b) 06's worked example assumes a 50% retention lift with no basis. (c) Repeat rates: 04's bands (20% to 40%), 05's 28.2% DTC average vs an 18.8% dataset vs 23% to 25% India, 06's "30% to 40% average retention", 01's "only 20% buy twice". These are different populations, windows and definitions, and no source reconciles them. What the agent does: recompute every case figure in code from the stated inputs and report the computed value with the source's spoken value in brackets (F25); never present the 50% lift as anything but an assumption; never average the repeat-rate figures; report the brand's own `repeat_rate_W` with its window and cite the bands as uncited reference points only. [83592aa3301a] [eacd1adfeb8d] [8db0ffa97875] [7f71ff76f9b1] [3e09caf827f4]

**C6. Win-back timing.** 01: trigger off RFM and the customer's own cadence; a fixed 120-day trigger hits a 200-day-cycle customer too early. 05: send 30 to 45 days after the last purchase, not 90 plus, citing a Klaviyo benchmark of 2.3x better conversion. When each is right: 01 where the brand has enough order history for RFM and varied cycles; 05 where history is thin or cycles are short and uniform. What the agent does: RFM At Risk where it exists; else 30 to 45 days after the expected reorder point for consumables and after the last purchase for non-consumables; never a fixed day count across all customers (R122). [98fc8eced08a] [5195356ba962]

**C7. Incentives on the second purchase and in the box.** 05: 10% to 15% incentive about 10 days after the first order arrives, and "running low? save 10%" for replenishment. 04: the standard insert carries a next-purchase discount code. 06: an unconditional gift, no code, because codes train customers to wait for markdowns. 01: loyal and subscriber customers get the least aggressive messaging and ideally no incentive. When each is right: a modest first-to-second incentive is a test for new customers; a code in every box trains the whole base; no incentive is right for loyal customers. What the agent does: incentive only at the first-to-second step and only as a test measured by `f2_rate_90` and 365-day LTGP; a gift, not a code, in the box; no incentive to the loyal tier; run the discount-cohort audit (P10) on any code used. [6dcc8b256a6b] [83291c925c2b] [f60a2e0fa1a5] [3c84840ee4fe]

**C8. Existing-customer paid spend.** 01 disagrees with its own earlier position ("spend nothing on existing customers") and now allows spend for fashion and frequent-drop brands. No other source covers this. What the agent does: treat the exception as 01's current view; require the exception condition and the half-CPA rule before recommending any spend (P9). [675be3b57a10]

**C9. LTGP:CAC above 3.** 01: leaving money on the table, arbitrage that will not last. 20-FIN's sources disagree among themselves (one calls above 3 a mistake, one calls 5 plus healthy at late stage, common advice calls 3:1 healthy). What the agent does: use 01's 2 to 3 band as the scaling target here; when a brand sits above 3, present it as a choice between faster growth and higher margin, not as an error, and cite 20-FIN C3. [3861489d8286]

**C10. Handwritten notes at scale.** 04: reserve handwritten notes for VIP and high-value orders. 05: at scale use pre-printed cards with a real signature or an item-specific merge field. 06: robotic handwriting at retention milestones, never represented as personally handwritten. When each is right: 04 for volume brands with limited fulfilment capacity; 05 and 06 for brands that want the touch at every milestone. What the agent does: VIP and milestone notes only; real signature or merge field; disclose machine writing if asked and never claim staff wrote it; cost each send into P26. [83291c925c2b] [b056689936fe] [5f53155ff467]

**C11. Discount code in the insert.** 04's insert protocol includes a next-purchase code; 06 says no code. Covered by C7; the agent follows 06 for the box and tests any code through P10.

**C12. Service recovery paradox.** 04 generalises Bloom & Wild's CEO: over-fixing a problem turns the customer into a stronger advocate than one who never had a problem. 05: the paradox is real but rare (5.4%) and conditional, and error-free service still wins; never engineer it. Both say to over-recover when a failure happens. What the agent does: never accept failures for the sake of recovery; over-recover genuine failures; measure the failure cohort (R107) rather than assume advocacy. [284b8c726776] [df383902e95d]

**C13. Recommendations in post-purchase messages.** 04 puts a complementary recommendation on the tracking page and a post-checkout upsell after payment. 06 says transactional emails stay focused on the order and promotional cross-sell goes to marketing sends. What the agent does: recommendations on the tracking page below status and on the post-checkout page; none in the body of the transactional email above the tracking information. [af9547313e6f] [bd18309bf03e] [6d6e184eb848]

**C14. Quiz length.** 05: about 5 questions. 06's Bare Anatomy example: 75 plus data points, with 06's own caution that long quizzes add friction. What the agent does: start near 5 questions; extend only when the category's consideration level and a completion-rate test justify it (R131). [89e75eb0f016] [6bda120ef375]

## 8. Common mistakes

Merged and deduplicated from all sources, with the fix.

1. Reporting Shopify's "% returning customers" as retention. Fix: cohort `repeat_rate_W` (R15). [9444eb58b437]
2. LTGP from AOV times an assumed margin. Fix: order-level cohort build (P1). [2d30561e1938]
3. Refunds in CAC, or in neither CAC nor LTGP, or counted twice. Fix: R4. [2d30561e1938]
4. Optimising only attribution dashboards, or ignoring incremental repeat work for long-term LTV thinking. Fix: R17, R18. [2df157249026]
5. Chasing pop-up opt-in rate. Fix: R21. [4789763c9e99]
6. One linear flow for everyone, or a product-first split. Fix: R30, R31. [3c84840ee4fe]
7. Hyperpersonalising campaigns into micro-segments and starving reach. Fix: R45 to R47. [097d09066f7a] [eacd1adfeb8d]
8. Testing subject lines and delays before structure and offers. Fix: R125. [ebe1e2f78000]
9. Fixed-day win-back triggers. Fix: R41, C6. [98fc8eced08a]
10. Treating VIPs like the general list, or building VIP programs while F2 is the constraint. Fix: R43, R44. [39c55eb82e67] [3de8a595a9bb]
11. Same CPA for existing and new customers; scaling existing-customer spend past diminishing returns. Fix: P9. [675be3b57a10]
12. Trusting front-end ROAS without checking refunds and repeat. Fix: P11. [e74d0b65f2db]
13. Scaling a discount promotion without a cohort check by code. Fix: P10. [34373cddcf01]
14. Jumping to email or loyalty when product, portfolio, acquisition or CX is the constraint. Fix: P5. [290bef9daa56]
15. A loan-funded long-payback model without interest modelling under about 15 to 20 million a year. Fix: R7. [5a300a3bc804]
16. Treating the confirmation email as a receipt. Fix: R67. [d17748ab5f3a]
17. Fewer than 3 proactive updates; a bare tracking-link email in a considered category. Fix: P13. [d17748ab5f3a] [6d6e184eb848]
18. Sending customers to the carrier's tracking page. Fix: P15. [73abfaadbe4c]
19. Over-promising delivery dates or product results. Fix: R64, P14. [9eb0da75866c]
20. A note or gift on top of a late delivery or slow refund. Fix: R58. [b233a6d834e6]
21. Trying to delight during a service failure instead of cutting effort. Fix: R59, R103. [36baf5a5a8ad]
22. Engineering failures to create recovery moments. Fix: R65. [df383902e95d]
23. Spreading CX budget evenly instead of 1 peak and 1 end; adding delight while a negative peak is live. Fix: R60, R61. [0372f28739d1]
24. Funding "delight" that is really a must-be gap, or funding attractive items while a must-be is broken. Fix: R62. [ff986b275489]
25. Assuming a delighter stays a delighter. Fix: R63. [a4e3c81ce639]
26. A conditional discount code as the "gift"; a cheap or off-brand gift; a form letter dressed as handwritten; a machine note claimed as staff-written. Fix: R85 to R87. [f60a2e0fa1a5] [b056689936fe] [5f53155ff467]
27. Packaging texture that contradicts the brand promise. Fix: R84. [029011fd7e9d]
28. Overloading transactional emails or adding promo cross-sell above the tracking info. Fix: R73. [6d6e184eb848]
29. Returns run as a cost centre; slow refunds; credit substituted silently. Fix: R96 to R98. [0f70a58b8a2b] [33d6b517ecb9]
30. Identical experience for first-time, repeat and VIP buyers. Fix: R35. [e13b48c6a15a]
31. Only CSAT and NPS on the dashboard. Fix: R19. [7f71ff76f9b1]
32. Survey scores standing in for financial impact. Fix: P26. [8db0ffa97875]
33. Surveys run to flatter or to pressure staff, or asking employees without a plan to act. Fix: P29. [b24643e22b8c]
34. Over-messaging replenishment; rigid subscriptions. Fix: R92, R93. [6dcc8b256a6b]
35. Leading win-back with a flat discount, or sending it into unresolved service problems. Fix: R121, R123. [5195356ba962]
36. Loyalty tiers before delivery, returns and support are reliable. Fix: R115. [e6f325f479fd]
37. First-name tokens as "personalisation"; creepy inference or third-party data; a quiz that funnels everyone to 1 product; too many quiz questions. Fix: R129 to R131. [89e75eb0f016] [a40ceca4da16]
38. Dark patterns, forced account creation, hidden fees at the last step; cutting fields so far that failed orders rise. Fix: R150. [c7561c93445f] [1d8f5cd1000c]
39. Mapping all personas at once; a journey map that changes nothing. Fix: R137, R128. [0fe858c0c51f] [feb07cfa31b9]
40. CX as a slogan; CX owned by marketing alone; employee experience run apart from CX; silo thinking. Fix: R138, R139. [8c2c0d954819] [41d67b919c4c]
41. "We're B2B, CX does not apply." Fix: R141. [e984e2fe9282]
42. Upsell before the issue is resolved; generic bots that flatten the voice; AI budget only on efficiency. Fix: R110, R112, R114. [298b23ff39c4] [7de1741d6532]
43. Building search and ranking in-house without the talent; popularity-only ranking; AI with no objective; merchandisers stuck on manual monitoring. Fix: P31. [ee1d80f4de9d] [86cba9e8253e] [800f306a36a5]
44. Treating a single vendor benchmark, a forecast percentage or a case result as a portable target. Fix: E3, R20. [4530efe6348a]
45. Fabricating or filtering reviews to game AI visibility. Fix: R91. [291fd5b847c5]

## 9. Deliverables

What the agent produces for each task, and the format. Every number carries its formula label, window, cohort and data date. Every vendor or case figure says "claim".

### 9.1 Cohort readout

Format: 1 page plus a table file. Built by P4.

1. Header: brand, data date, cohorts covered, windows.
2. Table: per cohort, customers acquired (pre-refund), Day-0 GP (F1), LTGP at 30, 60, 90, 180, 365 (F2), `repeat_rate_90` and `repeat_rate_365` (F8), `f2_rate_90` (F10).
3. Trailing-12-month `top20_share` revenue and profit (F11).
4. CAC by period (F3), ratio at the chosen window (F4) with the band, CAC target (F5), floor and realistic case (F6), payback day where it applies (F7).
5. Discount-code split with penalty per code (F24).
6. Three findings: the weakest function (F1, F2, F3), the discount penalty, the cohort trend.
7. Caveats: cohorts too young to read, missing COGS share, any "unavailable".

### 9.2 Top 3 experience fixes with expected effect

Format: 3 entries, each 6 lines. Built by P12, 5.2, 5.3, 5.4.

Per fix: the touchpoint; the moment type (service or discretionary) and Kano class; the current value of the governing metric (F16 DEA, F17 WISMO, F18 refund cycle and gap, F8 repeat, review rate, UGC count); the change; the expected direction and the source's figure labelled as claim or example (for example "04 claims a 3-step flow cuts WISMO up to 80%; expect a fall, size unknown until measured"); the cost at current and 2x volume (F22 where packaging); the gate that says it worked. Order the 3 by R126's payoff order, must-be gaps and negative peaks first.

### 9.3 Retention play with test design

Format: 1 page. Built by P30.

1. Constraint (F1, F2 or F3) and the evidence from the readout.
2. Hierarchy check: product, portfolio, acquisition and CX cleared, with the evidence line each.
3. The play: what changes, for which segment (journey stage, RFM, tier), with the incentive rule from C7.
4. Test class (structure and timing, offer, messaging) and why this class now.
5. Hypothesis: metric (3.0 label), current value, minimum change worth acting on, window, readout date.
6. Split: randomised or matched cohorts; sample per arm.
7. Decision rule: ship, iterate, stop.
8. Dependencies: 14-EML build items, data needed, `[verify UI]` steps.
9. Log entry for the experiment file.

### 9.4 Support reply templates in voice

Format: a set of 8 templates, each under 120 words, in the brand's voice, with bracketed variables. Built by P22.

Templates: where is my order; late delivery; damaged or wrong item; return request; refund status; cancellation; product question after delivery; complaint escalation. Each has 4 parts: the problem named, the fix with a date, what the customer needs to do, 1 human line. Policy lines match the brand record. Each set ships with the blind-read result (who read, whether they recognised the voice) and a version date.

### 9.5 Post-purchase journey audit report

Format: the 5.2 and 5.3 tables filled in, with the current value per row, a red or green flag, and the fix reference. Plus the P12 map for the chosen persona: peak, end, negative peaks, Kano classes, service vs discretionary tags.

### 9.6 Delight payback model

Format: the F20 inputs and result for 1 program, with treated and control cohort sizes, window, program cost per customer, incremental contribution, pass or fail, and the decision.

### 9.7 Post-purchase roadmap with exit gates

Format: 1 page for leadership. Built by P27.

1. The 8 steps in payoff order (R126): delivery promise and tracking, returns, unboxing, replenishment and nudges, quiz personalisation, loyalty and VIP, gifts and community, win-back.
2. Per step: the exit gate metric, its current value, and whether the gate is met.
3. The step in progress and the next step blocked behind it.
4. Dates: when each completed step passed its gate, and the target date for the next one.
5. A 1-line ask per step still blocked: what the brand needs to unblock it (data, budget, a decision).

## 10. What needs live data or a web check

### 10.1 `[needs brand data]`

Retention economics: order-level revenue and refund lines with customer id and first-order date; COGS per SKU; delivery cost per order; transaction fee rate; refund rate and whether revenue is net; media spend by period and channel; new customers by period; CPC and new-customer conversion; annual revenue, capital position and category repeat cycle (R7); subscription attach and cancellation; days between orders; top-20% revenue and profit share (R42).

Segments and owned media: list size; engaged segment size and lookbacks; RFM output; existing-customer count and CPM (P9); survey or quiz responses joined to orders (P11).

Journey: WISMO tickets per order; ticket log by type; carrier lane performance and handling time (P14); delivery promise and delivered timestamps; return request, approval and refund timestamps and method; return fraud rate and cash position (R99); review request and review counts; per-order packaging cost, orders per month, 3PL insert and note capability (P16); product cost per order; usage cadence per SKU (F23); genuine post-purchase tips per product (R89); top objections from tickets, reviews and chat (R79); brand promise, positioning and voice guide (P16, P22); approved claims and policy limits.

Support: support cost, contact count, orders linked to contacts (F19); helpdesk context integration status.

Strategy: leadership meeting agenda (P28); current storefront search and recommendation platform and contract (P31); catalog size and COGS data quality (F21).

### 10.2 `[web check]`

Vendors and prices: branded tracking (SyncTrack, AfterShip, parcelLab, Malomo, Narvar, Wonderment, ParcelWILL, Route); returns and refunds (Loop, AfterShip Returns, Narvar, Reshop, Refundid, Worldpay Faster Refunds, Razorpay Engage, Fintecture); handwriting (Handwrytten) and its Klaviyo and Gorgias triggers; helpdesk and AI support (Gorgias, Zendesk, Intercom) capabilities and pricing; quiz tools (Visual Quiz Builder, Octane AI); loyalty tools; search and recommendation vendors (Coveo lineup and pricing, SAP Store listing).

Law and platform rules: returns and refund law per ship-to market (R101); WhatsApp Business opt-in rules for transactional vs marketing messages in India (R75); in-platform commerce requirements on ChatGPT, Perplexity and Gemini (P32); Klaviyo's current post-purchase email guide and RFM location `[verify UI]`.

Statistics quoted by sources, before any client use: 02's 78%, 85%, 92% and 80/15/5 and 8-year figures; 03's 1,400 to 5,000 interactions and 6% to 2% margin forecast; 04's unnamed "2023 analysis" that delight is a losing strategy; 05's vendor benchmarks (WISMO ranges, win-back, replenishment, tracking); 06's cited figures (35% CAC, 37% retention, 100.5% spend, 30% and 12% checkout effects, 96% disloyalty, NPS 50 and 70, "95% subconscious"); 07's unnamed study on why people use generative AI; the current Baymard checkout field count.

People and claims: 01's presenters and the "biggest email agency in Australia" claim; 01's referenced channel for the full flow breakdown; 02's presenter name and company; 07's presenter background; Bare Anatomy and Sweet Karam Coffee details; whether 07's named products (L'Oreal assistant, Talk to Ralph, Meta glasses subtitles, Comet) still exist as described.

## 11. Freshness and stale-risk notes

| Area | What can go stale | Re-verify |
|---|---|---|
| Tracking-page vendors | Names, mergers (Wonderment into Loop, ParcelPanel renamed ParcelWILL per 05), pricing tiers (05 quotes about 99 a month for 2,500 shipments), Shopify app compatibility, feature names | Before every P15 recommendation; at least every 6 months |
| Returns and refund vendors | Instant-refund availability per market and card network (Riverford's case was Mastercard and Visa only), fees, fraud tooling | Before every P20; every 6 months |
| Returns law | Statutory return windows, refund timing rules and consumer protection per ship-to market; India, EU, UK, US states differ | Before any policy change; annually at minimum |
| AI support tools | Resolution-rate claims (05's 64% to 95%), model capabilities, pricing, data-handling terms | Before P23 step 3; every quarter |
| AI platforms and commerce | In-platform checkout and app integrations on ChatGPT, Perplexity, Gemini; 07 expects material change within about a year | Quarterly (P32) |
| Klaviyo and Shopify UI | RFM tab location, attribution report names, the returning-customer metric wording, post-purchase guide content | Every `[verify UI]` step, each build |
| WhatsApp Business rules (India) | Opt-in and template categories for transactional vs marketing | Before any WhatsApp journey |
| Consumer statistics | NRF and Happy Returns, Narvar, Baymard and McKinsey figures are dated 2024 to 2025 and move yearly | Annually; quote the year |
| Vendor case studies | All of 04's 40 brand cases and 05's Indian D2C figures are undated or 2022 to 2026 marketing content | Never quote without "claim" and a date; refresh if used externally |
| 01's economics heuristics | Ratio bands, the 15 to 20 million window rule, the 10 to 20 million VIP rule are agency rules of thumb as of late 2025 or 2026 | Re-test against brand cohorts yearly; do not update from the web |
| 03's margin forecast | 6% to 2% retail margin by 2024 to 2025 is a 2022 forecast, now past its date | Replace with the brand's own margin trajectory; do not quote |
| 07's forecasts | All are "for 2026 and beyond" | Re-read section 3.23 each quarter; move a row to a rule only when the trigger is observed |

24 Sep 2026: ecommerce specificity pass applied from ECOM_REVIEW.md; priority block added, 13 rules reworded, 8 levers added, about 720 words moved to Appendix A.

## 12. Source index

| Number | Title | Type | Credibility and bias | Contributed most |
|---|---|---|---|---|
| 01 | The Complete E-Commerce Retention Masterclass | Transcript, 2 agency presenters, auto captions | Agency marketing content ending in a paid-audit pitch for brands over 5 million a year and a hiring link. Evidence is client-base heuristics ("60% of the brands we work with"), 2 named cases (a 9-figure activewear retailer, a 9-figure supplements retailer), unnamed studies; no controlled tests. Nathan's finance rules are one operator's numbers and thresholds (2 to 3 band, 15 to 20 million, 10 to 20 million); Angus's email content is about 70% of the runtime and belongs to 14-EML. Spoken arithmetic has slips (C5). Credibility: medium for operating heuristics, low as benchmarks. | Every formula in 3.0 from F1 to F14 and F24, F25; the retention hierarchy; F1, F2, F3 structure; engaged audience; RFM; VIP; existing-customer ads; discount cohorts; zero-party targeting |
| 02 | Introduction to Customer Experience (CX) | Talk, webinar with live polls | A promotional taster for a paid workshop; the presenter defers the "how" to it. General CX theory with no ecommerce content of her own; all ecommerce framing in its cards is the card-writer's translation. Statistics (78%, 85%, 92%, 80/15/5, 8 years) are unsourced. Holds a self-declared contrarian position against surveys (C1). Credibility: low for numbers, useful for vocabulary and the ownership and maturity model. | Maturity phases, 3-part framework, journey not process, ownership and leadership agenda, employee-experience link, voice-of-customer method, B2B parity |
| 03 | Customer Digital Experience is Key to Successful Ecommerce | Transcript, analyst interview with a Coveo GM | A vendor selling the category he recommends buying; build-vs-buy and MPV are his commercial position. Client anecdotes (chemical distributor, footwear, fleet parts, gifting), 1 unnamed customer's 72% margin claim, a 2022 research figure not linked, a margin forecast now past its date. Mostly pre-purchase search content. Credibility: low as evidence, medium as a framing of margin-first measurement. | Margin per visitor (F21), margin-based customer value, buy vs build (C4), objective-before-AI, friction and distraction rules |
| 04 | E-commerce Customer Delight | Article, compiled research report (delight cluster) | Unsigned synthesis with about 40 brand cases sourced from vendor case-study pages (parcelLab, Narvar, Malomo, Reshop, Loop, Klaviyo, Yotpo and others). Sells nothing itself but every number is a vendor's or brand's self-report; the source's own cards say "not benchmarks". RPR bands are uncited. Credibility: low for numbers, high for the checklist of levers. Counted as 1 with 05 and 06. | 3-step WISMO flow, branded tracking page, unboxing protocol, education sequence, faster refunds with choice, recovery playbook, experiential loyalty, first-time, repeat, VIP tracks, delight metrics, fix effortlessness first |
| 05 | Customer delight across the e-commerce journey: a retention view | Research memo, literature review (delight cluster) | Unsigned, sells nothing, and flags its own evidence quality line by line: peak-end (Kahneman, 2022 meta-analysis) and the 2010 HBR effort study (75,000 plus interactions) as strong; Michel and Meuter, Reichheld and Bain, Baymard, NRF and Happy Returns as credible; everything else vendor or self-reported (Narvar, Klaviyo, Omnisend, GoKwik, Mamaearth, Licious, Nykaa). Pre-processed for the card pipeline. Credibility: the strongest in the folder on the effort-vs-delight question; still vendor-heavy on operational ranges. Counted as 1 with 04 and 06. | Service vs discretionary moments, peak-end, recovery paradox, WISMO bands, DEA, delivery precision, packaging cost bands, replenishment and second-purchase timing, win-back method, roadmap in payoff order, cohort measurement discipline, benchmark caution |
| 06 | E-commerce Customer Delight Journey | Article, footnoted research report (delight cluster) | Unsigned, about 50 works cited: established theory (Oliver's expectancy disconfirmation, Kano, Kahneman, reciprocity) with applied percentages from vendor blogs (Handwrytten, Gorgias), Baymard, Slideshare decks and agency posts. Two brand cases (Bare Anatomy, Sweet Karam Coffee) are third-party write-ups. Its "95% subconscious" framing is persuasion-industry talk. Credibility: strong on the why, thin on the how; numbers are claims. Counted as 1 with 04 and 05. | Kano classification, delight decay, positive disconfirmation and under-promise, negative peak rule, haptics and brand coherence, unconditional gift vs code, robotic notes with disclosure, checkout cognitive load, CRR, delight payback test, persona journey map, privacy paradox |
| 07 | 9 Customer Experience Trends for 2026 | Talk, annual forecast | One presenter's predictions with no credentials stated in the transcript, no client data, 1 uncited study, named examples with no metrics. Explicitly forward-looking; its 2 percentages (10% price trigger, 10% to 20% adoption) are illustrations. Credibility: low as evidence; useful as a watchlist. | Support as profit centre (F19), brand agent voice, human-textured writing, honest review collection, AI visibility audit pointer, the trend watchlist in 3.23 |

Neighbour folders and what lives there:

- 14-EML-email-lifecycle: flow builds (welcome, post-purchase, replenishment, win-back, sunset), segment builds, campaign cadence, deliverability, SMS. The Klaviyo build parts of 01 belong there; this playbook keeps 01's structure and formulas.
- 20-FIN-finance-and-accounting: CM1, CM2, COGS, fulfillment cost, payback windows, the LTGP:CAC band discussion (its C3 vs this playbook's C9).
- 06-MEA-measurement and 24-DEP-ad-deployment: CAC measurement in platforms, attribution, incrementality, existing-customer campaign setup.
- 03-OFF-offers: bundles, subscribe-and-save, starter kits that move the LTGP ceiling (R12).
- 09-CRO-testing and 07-LPG-landing-pages: checkout and PDP testing method; R150 and R79 are the only checkout and PDP rules kept here.
- 05-SET-store-setup: search, recommendations and merchandising build; 03's engine rules are summarised in 3.22 only.
- 16-AEO-answer-and-generative-engines: the unbranded LLM prompt audit and AI visibility work pointed to from 3.23 and P32.
- 21-OPS-team-and-management: warehouse, picking, packing and 3PL operations behind P16.
- 10-MCR-paid-social-creative: angle and creative changes from the zero-party audit (P11).

## Appendix A. General background

General corporate CX strategy theory, moved out of the main body on the 24 Sep 2026 ecommerce specificity pass. Source 02 has almost no ecommerce mechanics of its own; the playbook's own credibility note calls it "general CX theory with no ecommerce content of her own." Kept here for reference and because R137, R138, R139 and R141 are still cited by id elsewhere in this playbook (P12, section 5.4, section 8).

### A.1 CX strategy, ownership, maturity and voice of customer (moved from section 3.21)

**R134. Write a CX strategy as an umbrella over the store: the feeling you want customers to have, the customer principles, what each means in practice, and who does what.** Three completeness questions: do you know who your customers are emotionally, do you know what experience you want them to have, does everyone know their part. Source 02 (1 source, general theory). [0eea90f3c62d] [fa4cf546d38a] [bdadd07890fc]

**R135. Place the brand on the maturity line (random, intentional, differentiated) and set milestones in years, not quarters.** Random: outcomes depend on who handles the contact. Intentional: shared vision and cross-functional commitment; 02 says profitability starts here. Differentiated: everyone acts in the customer's interest all the time. 02's 80/15/5 split and 8-year timeline are unsourced assertions. Source 02. [2d05c23909e5]

**R136. Run the 3-part framework (strategy, measurement, people) as linked pieces; silo thinking is the single biggest thing that breaks a CX strategy.** Source 02 (framework credited to an unnamed partner). [fa4cf546d38a]

**R137. Map the journey from the outside in, 1 high-value persona at a time, and push every insight from descriptive ("wants fast shipping") to emotional ("anxiety from no order acknowledgement").** "If they cannot feel it, hear it, see it, touch it, it is not a journey, it is a process." Mapping all customers at once creates noise. Sources 02, 06 (2 sources). [feb07cfa31b9] [0fe858c0c51f]

**R138. Give CX a dedicated cross-functional owner, with the CEO accountable, and put customer impact on the leadership agenda ahead of revenue items.** Marketing covers only part of CX. 02's check: ask for the last leadership meeting protocol and look for the customer on it. Source 02. [8c2c0d954819] [6edd7693ad4a]

**R139. Link employee experience to CX delivery in 1 shared strategy; how staff are treated shows in how customers are treated, down to packing.** Source 02 (ABB anecdote: shift from "helping the product" to "helping the customer with the product"). [41d67b919c4c]

**R140. Voice of customer: do your own homework first (data you already hold, ticket text, reviews), ask employees what customers think (only with a plan to act), and talk to customers directly; run a satisfaction survey only when there is budget and commitment to act on it.** 02 holds the contrarian position that surveys annoy customers and mostly serve ego or staff pressure; 01, 04, 05 and 06 use surveys, NPS and CSAT as inputs. Conflict C1 gives the reconciled procedure (P29). Sources 02 vs 01 and the delight cluster. [b24643e22b8c] [290bef9daa56] [7f71ff76f9b1] [bc11d5300f1f]

**R141. Apply the same CX rules to B2B and wholesale storefronts; buyers expect consumer-grade search and checkout even on 70-line, 500,000 orders.** Sources 02, 03 (2 sources agree). Out of scope for a store: this playbook covers consumer ecommerce; B2B and wholesale storefronts are a different domain. [e984e2fe9282] [6d5eea41344a]

**R142. Experience is a design choice; experience leaders in any category (02 names Amazon, Airbnb, Uber) set the bar for what the customer expects next, so judge every new tool against the intended experience before adopting it.** Source 02. [b4c441cd3922]

**R143. Differentiate on experience and word of mouth where product, price and quality are copied fast; word of mouth spreads only when the experience is good enough on its own.** 02's 92% trust and 78% "doing good" figures are unsourced. Source 02. `[web check: sources for 02's 78%, 85%, 92% and 80/15/5 figures]` [ff0c754a9777]

### A.2 CX maturity assessment and ownership (moved from procedure P28)

Goal: a maturity placement and an ownership decision. Source 02. [2d05c23909e5] [8c2c0d954819] [6edd7693ad4a] [fa4cf546d38a]

1. Look for signs of "random": reply times, packaging and service quality that vary by who handles the contact.
2. Ask for the last leadership meeting agenda; check whether the customer appears.
3. Run the 3-part question sequence: strategy (who, what feeling, who does what), measurement (journey mapped, measured from the customer's side, priorities known), people (know the strategy, ambassadors, enabled).
4. Name the phase and 1 milestone per year toward the next.
5. Recommend a cross-functional CX owner reporting to leadership; not marketing alone.

### A.3 General CX benchmarks (moved from section 6)

| Metric | Value | Condition | Source | Confidence |
|---|---|---|---|---|
| CX maturity split | 80% random, 15% intentional, 5% differentiated; 8 years to move | General | 02 | 1 source, unsourced |
| Consumer stats | 78% advocacy for "doing good"; 85% employee obligation; 92% trust friends over marketing | General | 02 | 1 source, unsourced |
| Favourite-brand drivers | Attitude, ease, helpful with problems, people, personalisation, product, consistency | 1 webinar poll | 02 | 1 source, informal |
