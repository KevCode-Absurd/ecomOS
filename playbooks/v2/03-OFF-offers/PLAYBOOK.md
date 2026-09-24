# 03-OFF-offers playbook

version: 2.0-draft  |  date: 24 Sep 2026  |  sources: 10 mini playbooks (8 independent voices: 01 and 10 are the same author, 05 and 07 are the same agency, and 06 and 07 are never counted as 2)  |  cards: 270  |  built from: sources/*.md

## 0. How to use this playbook

**Who runs it.** The offer and pricing agent. It designs and costs offers for physical products: bundles, buy-more-save-more ladders, gifts with purchase, thresholds, subscriptions, guarantees, bonuses, credit and discount framing, promotions and pop-up offers. It also audits how a fixed offer is presented across ad, page and checkout. It hands page layout to 07-LPG, test design and significance to 09-CRO, email and SMS flows to 14-EML, cancel-flow build and portal UX to 17-CXP, landed cost and P&L definitions to 20-FIN, ad copy to 11-ADC and ad account work to 24-DEP.

**Every offer is costed before it is proposed.** No bundle, discount, gift, guarantee, threshold or subscription rate leaves this agent without a contribution-per-order and contribution-per-visitor figure at the proposed structure, against the current structure. All arithmetic is done in code in ecomOS (`intelligence/` calculators, or a script the agent writes and runs), never in the model's prose. Missing inputs give "unavailable", not 0. Formulas are in section 3.0.

**ecomOS rules that override every source in this folder.**
1. No fake urgency, fake scarcity, fake restock notices or invented reference prices. A countdown, stock count, "X% claimed" bar, "was" price or stated bonus value is allowed only if it is true, enforced and provable from brand data. Sources 01, 02, 07, 09 and 10 each contain at least 1 line that permits or ignores this; those lines are marked "reject" below.
2. Guarantees and offers are costed before they are proposed (formulas F2, F3, F8, F10, F11).
3. Fixed-offer brands (Peach Bucket is one) get presentation fixes, not new discounts. For them the agent runs P19 and checklist 5.2 and does not propose a price change unless the brand owner asks for one in writing.
4. Consumer-law risks are flagged `[web check]` by country. Reference prices, "up to" savings claims, auto-renewal and pre-selected subscriptions, cancel-flow friction, drip pricing, health claims and countdown timers all carry a `[web check]` tag in this playbook. Gehna sells in India; India's 2023 dark-pattern guidelines list false urgency, basket sneaking, subscription traps and drip pricing. Peach Bucket and TrailFold markets must be confirmed from the brand record before any legal check is scoped `[needs brand data: selling countries per brand]`.
5. Brands stay apart. Numbers in this playbook are the sources' examples in USD (some GBP and EUR), never a brand's. Convert every threshold to the brand's currency and price points before using it.

**Which sections to load for which task.**

| Task | Load |
|---|---|
| Cost an offer idea, or check an existing offer's economics | 3.0 (F1 to F7), 3 group B, P1, P2, checklist 5.1 |
| Propose 3 costed offer options for a brand | 3 groups A to I, P1 to P9, 6, 9.1 |
| Decide whether to discount at all, and how deep | 3 group D, P3, P4, 7 (C3, C4), 6 |
| Build a bundle or buy-more-save-more ladder | 3 group E, P5, F10, checklist 5.6 |
| Design a gift with purchase or bonus | 3 group F, P6, F13 |
| Set a free-shipping or spend threshold | 3 group G, P7, F17, 7 (C1) |
| Score upsells, cross-sells and post-purchase offers | 3 group H, P8, F9 |
| Design or review a subscription offer and buy box | 3 groups I and J, P9 to P13, F11, F12, checklist 5.3, 7 (C5, C6, C9) |
| Design and cost a guarantee | 3 group K, P14, F8, checklist 5.7 |
| Use scarcity, urgency or a drop | 3 group L, P15, checklist 5.8, 7 (C10) |
| Plan a promotion or sale, with stop rules | 3 group M, P16, checklist 5.4, 9.3 |
| Pop-up or first-order offer | 3 group N, P17, P18, F16, checklist 5.5, 7 (C7) |
| Fixed-offer brand: presentation audit and fix list | 3 group O, P19, checklist 5.2, 9.2 |
| Name or reframe an offer | 3 group P, P23 |
| Value equation audit of a product offer | 3 group A, P20 |
| Reposition a hero SKU into several offers | 3 group A (R9), P22 |
| Refresh a tired offer | 3 group M (R123), P21 |
| Propose an offer test | 3 group Q, P24, 9.5 |
| Any point where sources disagree | 7 |
| What cannot be known without brand data or the web | 10, 11 |

**Fetch before acting.**
- From the brand record: price list, all-in COGS per SKU (product, inbound freight, packaging), shipping and 3PL cost by units per order, payment fees, return rate and reverse-logistics cost per return, current offers on site and in ads, subscription terms, guarantee text, selling countries and currency, whether the brand is a fixed-offer brand, owner's rules on discounting.
- From the data layer: order-level order values for 90 to 180 days (not the reported mean AOV), units per transaction by period, conversion rate by traffic type, sessions, CAC or blended CPA, cohort repeat rate and LTV at 90 days, 6 and 12 months, subscriber vs one-time cohorts, subscription take rate, churn by month, cancel reasons, save rate, past sale periods with ROAS and UPT, pop-up opt-in rate, email revenue per subscriber.
- From the web (`[web check]`): consumer-law rules in each selling country for reference prices, "up to" claims, countdowns, stock claims, auto-renewal and cancel flows, pre-selected options and drip pricing; current Shopify subscription and discount-combination behaviour; current app names and features named in section 11.

## 1. Scope and outcomes

**Covers.** What the buyer gets, at what price and terms, and why now, for physical products sold online. Specifically: the value equation as it applies to products; offer types (bundles and multi-packs, buy-more-save-more ladders, gifts with purchase, spend and unit thresholds, subscriptions and prepaid plans, guarantees and try-before-you-buy, bonuses, store credit versus discounts, loss leaders); costing every offer at contribution per order and per visitor; discount depth and framing (dollar versus percent, BOGO and "free" versus percent off, per-unit and per-day price display); subscription design (pre-selected default, save rates, front-loaded versus flat, subscription-only versus a one-time path, cadence, gift roadmaps, cancel-flow save offers, win-back offers, LTV windows); promotions and their cannibalisation (price-integrity, subscriber collision, frequency); pop-up and first-order offers; fixed-offer presentation across ad, page and checkout; when not to discount; and the rules that protect margin and price integrity.

**Does not cover (neighbour folders).** Page layout, section order, listicles, side-cart UI and progress-bar design: 07-LPG. Test sizing, significance and stopping rules: 09-CRO. Onboarding, billing reminder, order confirmation, subscriber campaign and win-back email builds: 14-EML. Cancel-flow build, portal UX, dunning and payment recovery: 17-CXP. Landed cost, P&L ladder, cash and inventory: 20-FIN. Ad copy for the offer: 11-ADC. Lead-generation offers, bait pieces and B2B invoice terms from source 02 are kept in section 3 group N and P18 only where they translate to email capture; the rest is out of scope for a DTC store.

**Business measures it moves.** Conversion rate, units per transaction, AOV, contribution per order, contribution per visitor (profit per session), break-even and required ROAS, allowable CAC, subscription take rate, cohort LTV at 90 days and 6 months, refund and return rate, discount share of revenue, and price integrity (share of revenue sold at full price).

## 2. Inputs the agent needs

| Input | From where | Required or optional | Why |
|---|---|---|---|
| Price per SKU and per variant, in selling currency | Brand record | Required | Every formula starts from price |
| All-in COGS per SKU (product, inbound freight, packaging, duties) | Brand record or 20-FIN landed-cost table | Required | Gross margin; sources 04 and 08 say most brands miss shipping and fees |
| Shipping and 3PL cost by units per order and weight band | Brand record | Required | Bundle savings come from shipping, not unit cost (04, 08) |
| Payment fees and app fees per order | Brand record | Required | Contribution per order |
| Return and refund rate, return cost per order, resale rate | Data layer | Required for guarantees and bundles | F8; unconditional guarantees on physical goods carry reverse-logistics cost (02) |
| Order-level order values, 90 to 180 days | Data layer | Required for thresholds | Thresholds are set on the distribution, not the mean (04) |
| Units per transaction, overall and in past sale periods | Data layer | Required for discount modelling | UPT lift is the only thing that can pay for a discount (04) |
| Sessions, conversion rate by traffic type, CAC or blended CPA | Data layer | Required | Contribution per visitor, required ROAS |
| Past sale periods: dates, depth, ROAS or CPA, UPT, refund rate | Data layer | Required before any promotion | Sale efficiency lift is brand-specific: 70% to 80% for rare discounters, about 5% for known discounters (04) |
| Discount share of revenue and repeat buyers who only buy on sale | Data layer | Required for price integrity | Detects a trained-to-wait customer base (04, 07) |
| Cohort repeat rate and LTV at 90 days, 6 and 12 months, split by first-order type | Data layer | Required for subscription and LTV plays | F11; 05, 06, 07 all size the offer from the subscriber gap |
| Subscription take rate, churn by month, cancel reasons, save rate, skip and delay use | Data layer | Required for subscription brands | Groups I and J |
| Current offers live on site, in ads, in pop-up, in email, at checkout | Brand record plus a live crawl | Required | Congruence audit (P19); conflicting offers are a top failure (07, 05) |
| Owner's discount policy and whether the brand is fixed-offer | Brand record or user | Required | Override rule 3 |
| Selling countries | Brand record | Required | Scopes every `[web check]` |
| Inventory by variant and production limits | Data layer or user | Required before any scarcity claim | Honest scarcity only (01, 02, 10) |
| Objection list from reviews, support, chat, cancel reasons | Brand record or data layer | Optional but strong | Offers are built on the biggest objection (04, 01, 08) |
| Competitor offers and price map | Inspiration or web | Optional | Layout and mood only; never copy claims (ecomOS rule) |
| Pop-up opt-in rate, email revenue per subscriber, ESP cost tiers | Data layer | Required for pop-up offers | F16 |
| Cash position and months to payback | User or 20-FIN | Required for first-order-loss plays | 06 gates subscription losses on cash |

## 3. Decision rules

Rules are numbered R1 to R151 and grouped by sub-topic. Each states the rule, its condition, the mini playbooks that support it (S01 to S10), conflicts (C numbers point to section 7) and card ids. "Voices" counts independent presenters (see section 12): S01 and S10 are 1 voice, S05 and S07 are 1 voice, S06 and S07 are never counted as 2.

### 3.0 Formulas

All arithmetic runs in code. Variables are per order unless stated. "GM" is gross margin after all variable costs, not product COGS alone.

```
F1  Gross margin per order (all-in)
    GM_order = price_paid − COGS_units − shipping_cost(n) − fulfilment_cost − payment_fees − gift_cost
      price_paid      = order value after discounts, excluding tax
      COGS_units      = sum of all-in unit COGS for every unit shipped (including "free" units)
      shipping_cost(n)= outbound shipping and 3PL cost for n units in the box (not per-unit flat)
      gift_cost       = landed cost of any gift with purchase or bonus that ships
    GM_pct = GM_order / price_paid
    Source: S04 [0b43c974ae3c] [8074b0c6c718], S08 [471fc0881800], S06 [e311b1e255a4]
```

```
F2  Contribution per order and per visitor
    CP_order   = GM_order − CAC_order
      CAC_order = ad spend attributed per order (blended CPA if no clean attribution)
    CP_visitor = CVR × GM_order − ad_spend_per_session
      CVR      = orders / sessions for the same traffic and period
    Profit per session (S08 definition): net_profit / sessions, where net_profit = sum(GM_order) − ad spend − returns cost.
    Use CP_visitor to compare offers on the same traffic; use CP_order to set CAC targets.
    Source: S04 [0b43c974ae3c], S08 [1cda5c627ada], S06 [e311b1e255a4]
```

```
F3  Break-even ROAS and target CPA
    BE_ROAS     = price_paid / GM_order            (= 1 / GM_pct)
    target_CPA  = AOV / target_ROAS
    CP_target   = GM_order − target_CPA            (contribution the brand wants to keep per order)
    Source: S04 [0b43c974ae3c] [9fe82ea9bb52]
```

```
F4  Allowable CAC and required ROAS after an offer change
    allowable_CAC_new = GM_order_new − CP_target
    required_ROAS_new = AOV_new / allowable_CAC_new
    efficiency_lift_needed = required_ROAS_new / current_target_ROAS − 1
    Reject the offer if efficiency_lift_needed exceeds the brand's measured sale-period lift.
    Source: S04 [0b43c974ae3c] [f8754813a6a1]
```

```
F5  Discount modelling on a unit price
    unit_price_d = unit_price × (1 − d)                  d = headline discount as a fraction
    AOV_new      = unit_price_d × UPT_new                 UPT_new from past sale periods, never assumed 1.0
    COGS_new     = COGS_pct_of_full_price × unit_price × UPT_new   (COGS is paid on units, so on full retail value)
    GM_new       = AOV_new − COGS_new − shipping_cost(UPT_new) − fees
    Then apply F4.
    Source: S04 [0b43c974ae3c] [9fe82ea9bb52]
```

```
F6  Break-even lift for any margin-costing offer
    Holding CP_visitor constant on the same traffic:
      CVR_needed = CVR_current × GM_order_current / GM_order_new
      lift_needed = CVR_needed / CVR_current − 1
    For a discount with no UPT change, GM_order_new = GM_order_current − d × price, so the CVR lift
    needed grows faster than d as margin thins (the S04 "steep curve").
    Break-even discount (deepest d at which CP_order_new = CP_order_current, given UPT_new and CAC unchanged):
      d_be = 1 − (GM_order_current + COGS_new + shipping_cost(UPT_new) + fees) / (unit_price × UPT_new)   (CAC cancels)
    Source: S04 [99f79f8d840d], S06 [52c6ca3043ae], S08 [1cda5c627ada]
```

```
F7  Bundle tier savings and per-unit display
    tier_total(n)      = price for n units in the tier
    per_unit(n)        = tier_total(n) / n
    dollars_saved(n)   = n × single_price − tier_total(n)
    pct_saved(n)       = dollars_saved(n) / (n × single_price)
    per_serving(n)     = tier_total(n) / (n × servings_per_unit)
    per_day(n)         = tier_total(n) / (n × days_of_use_per_unit)
    shipping_saving(n) = n × shipping_cost(1) − shipping_cost(n)
    Show the larger of dollars_saved and pct_saved (S08) and always per_unit or per_serving (S09).
    Source: S08 [9f02d954cf3b] [5f2ab9d96cc7], S09 [4dc9316eaaf5], S04 [6a0ef806927d], S03 [defb3074e4c1]
```

```
F8  Guarantee economics
    net_orders          = orders × (1 − refund_rate)
    cost_per_refund     = refund_amount + return_shipping_paid + handling − resale_value_recovered
    guarantee_cost/order= refund_rate × cost_per_refund
    Compare 2 versions on net contribution:
      NC = orders × GM_order − orders × refund_rate × cost_per_refund
    A stronger guarantee wins only if NC_new > NC_current after the change in orders and refund rate.
    S01 example: 100 orders, 5 refunds = 95 net; 130 orders, 13 refunds = 117 net; 117 / 95 = 1.23x (refund cost not included there; include it here).
    Source: S01 [4d72bb91baae] [264e18c4c7be], S02 [729e71de2194] [322b4dd8abd3]
```

```
F9  Upsell, cross-sell and add-on value
    incremental_CP_per_exposed_order = take_rate × added_order_value × GM_pct_of_added_item
    Rank candidates on this product only. Measure lift against a holdout, since takers self-select.
    S04 example: 10% × $50 × 50% = $2.50 per order.
    Source: S04 [52ef4486583d] [456ea796c7fe] [67ab77318d00]
```

```
F10 Tier contribution (bundle, ladder, gift tier, subscription plan)
    CP_tier(n) = tier_total(n) − n × COGS_unit − shipping_cost(n) − fees − gift_cost(n) − CAC
    Every tier must clear CP_target (F3). If the deepest tier does not, cut its savings or gifts, not the shallow tiers.
    Source: S09 [01902b9597c7] [e339ff439cf1], S04 [2105cc48bb5d], S08 [471fc0881800]
```

```
F11 Subscription LTV, LTGP and the CAC ceiling
    survival(k)   = share of first-order subscribers still active at order k (from cohorts, not assumed)
    LTGP(K)       = sum over k = 1..K of [ order_value(k) × GM_pct(k) × survival(k) ] − gift_cost(k) × survival(k)
      order_value(1) uses the front-loaded price; order_value(k>1) uses the recurring price
    LTV window K  = the horizon the brand can fund: 90 days for cash-tight brands, 6 months as the S05/S06/S07 comparison horizon, 12 months only with proven cohorts
    CAC_ceiling   = LTGP(K) / target_LTGP_to_CAC   (S06 uses 3:1 on revenue LTV; ecomOS uses gross profit, per 20-FIN)
    Payback check = smallest K at which cumulative LTGP(K) ≥ CAC
    Source: S06 [5ea541b8c8d2] [0e9661473b27], S05 [d99fcf6edcf0], S07 [02a3e80a55a4] [89fd70abc2ef], S01 [6f9b8a8a1348], S03 [9099002370eb]
```

```
F12 Subscriber cap
    cap = new_subscribers_per_month / monthly_churn_rate
    S03 example: 2,000 new a month at 10% churn caps the base at 20,000.
    Source: S03 [a84f21107a98]
```

```
F13 Gift or bonus payback
    gift_spend         = recipients × gift_landed_cost
    incremental_value  = (orders_with_gift − orders_without_gift) × GM_order      (holdout or before/after)
    Keep the gift only if incremental_value > gift_spend.
    S03 example: 1,000 cohort, 900 reach order 2, gifts at $2 to $5 = $1,800 to $4,500; a 5% lift = 45 extra orders.
    Source: S03 [d4bfd76ee183], S04 [0afa90fbaa08], S07 [db90a9c32f90]
```

```
F14 Stacked discounts
    additive   : d_total = d1 + d2 + ...
    compounded : d_total = 1 − (1 − d1) × (1 − d2) × ...
    Which one applies depends on the checkout platform [verify UI]. Advertise only what checkout gives.
    20% + 20% compounded = 36%, not 40%. 15% + 10% compounded = 23.5%, not 25%.
    Source: S03 [35bed5b98d94], S07 [9e01130cee63]
```

```
F15 Scale screen and revenue per session
    RPS          = AOV × CVR                     (revenue per session)
    S09 screen   = AOV × (CVR × 100) > 250      (same as RPS > 2.50 in the source's currency)
    This screen has no margin term. Use it only as a first sort, then run F2.
    Source: S09 [34682db50bb8]
```

```
F16 Pop-up offer economics
    new_subscribers     = sessions × (optin_rate_new − optin_rate_current)
    email_value         = new_subscribers × revenue_per_subscriber × GM_pct
    discount_cost       = redeemed_codes × discount_per_order
    esp_cost_delta      = ESP tier cost at the new list size − current
    net                 = email_value − discount_cost − esp_cost_delta
    Judge variants on placed-order rate, gross profit after gift or discount cost, then 90-day LTV (S07).
    Source: S06 [42cf8bc4ce3a], S07 [db90a9c32f90] [89fd70abc2ef]
```

```
F17 Free-shipping threshold check
    For threshold T:
      share_already_above = orders with value ≥ T before the threshold / all orders
      share_moved         = orders that rise from below T to ≥ T after launch (holdout or before/after)
      CP_at_T             = GM_order at basket T including the now-unpaid shipping − CAC
    Keep T only if share_moved × (CP_at_T − CP_typical_below_T) > share_already_above × shipping_cost_given_away.
    Source: S04 [a1a57841df7a] [c9081fedfb43], S06 [52c6ca3043ae] [d5d7d14f51e0]
```

```
F18 Cancel-flow save offer cost
    save_cost_per_saved  = discount × order_value (this order only) or × sum of discounted future orders
    value_of_save        = LTGP of a saved subscriber over the LTV window K (F11), from cohorts of saved subscribers, not of all subscribers
    Raise the save offer only while value_of_save > save_cost_per_saved / save_rate_lift.
    S03: moving from 20% to 30% costs 10 percentage points of price on that order.
    Source: S03 [a006e3aa6f9c], S05 [1ae7b0ed8e41]
```

### Group A. What an offer is, and the value equation for physical products

**R1. An offer is the whole package, not the discount.** It is what the buyer gets, what they pay, the terms, and why now. A discount only fills the price slot. Condition: always; before proposing any offer, write it out in S04's 5 variables (positioning, price architecture, value mechanic, risk reversal, urgency) and S02's "what they get plus what they must do". Voices: 6 (S01, S02, S04, S06, S07, S08). [78a797a2bcce] [abaef45f549d] [a3756b7bf5f1] [5a6c2fe3c283] [e311b1e255a4] [82ae4d2b081b] [0a570cacb952]

**R2. Every offer is a trade of unit margin for 1 of 3 things: conversion, basket size (AOV) or repeat (LTV).** Name which one before designing it, and model the downstream chain (CVR, AOV, CAC, ROAS, contribution, LTV) before launch. Condition: applies to free shipping, gifts and email discounts too. Voices: 3 (S06, S04, S08). [e311b1e255a4] [0090d4f61912] [9e3f61688b5b] [1cda5c627ada]

**R3. The value equation applies to physical products.** Value = (dream outcome × perceived likelihood) / (time delay × effort and sacrifice). Raise the top, lower the bottom. Source 01 wrote it for services; source 10 (the same author) maps each part to a product store, and sources 06 (header only) and 08 repeat the mapping. Condition: a design heuristic, not literal maths; score each driver 0 or 1 to compare 2 offers, do not compute "value". Voices: 3 (S01+S10, S06 header, S08). [110b031911f0] [0e0a8b7a8e72] [b314811091f7] [0f5c6cd39ab0] [bdf993c3765b] [7bd7a76b5ba7] [4cc6038f44bf]

**R4. For products, the 4 drivers map to fixed levers.** Dream outcome: name and message the end state per avatar (warm, look good, sleep, focus), not the category. Likelihood: readable reviews, a demo of the outcome in use (S10's Levi's example: 1 video, about 90 seconds, 3 ways to wear), unboxing content, ingredient breakdowns, a guarantee. Time delay: shorter order-to-delivery (2-day, 1-day; 2 weeks is a weakness in S08 and S10), a stated delivery date, and for made-to-order goods a shorter production window; plus early wins after purchase (S01). Effort: saved details, express wallets, guest checkout, BNPL, try-before-you-buy, and product how-to content. Condition: work the bottom of the equation (time, effort) before making a bigger claim (S01). Voices: 3 (S01+S10, S08, S06 header). [bdf993c3765b] [44778b53f7ea] [2e7527024ff5] [cd466b907220] [7653128fbf28] [4cc6038f44bf] [4d408bb8adbd]

**R5. Perceived value is what counts; make improvements visible.** A faster checkout or better ingredient only adds value if the page shows it. Condition: any product improvement. Voices: 1 (S01). [d3c0e5ca9001]

**R6. Do not sell a commodity on price; differentiate the offer instead.** If reviews, support and comparisons say "these are the same, I'll buy the cheaper one", rebuild the package (bundle, kit, guarantee, bonus, name) rather than cut price. Condition: a commoditised SKU; not a licence to overprice, see R14. Voices: 2 (S01, S04). [61f1c72af108] [7a8d7aa38df0] [45e7a80365bc]

**R7. The offer starts in the ad and must match the page and checkout.** The desire, proof, delivery promise, risk reversal and price shown in the ad are the offer; the page confirms them. Condition: all paid traffic. Voices: 3 (S08, S01 card, S04 curator baseline). [0a570cacb952] [f3e0c5293ed8] [511c3a0c4cf9] [5a6c2fe3c283]

**R8. Build the offer on the customer's biggest objection, not on your margin target.** Ask what held buyers back, what worried them, what they would like to see; put the fix for the biggest objection in the offer (S04's lifetime guarantee on the 2-towel tier; S01's eating-out guide). Condition: needs an objection list `[needs brand data: reviews, support, chat, cancel reasons]`. Voices: 3 (S04, S01, S08). [0afa90fbaa08] [42ec3370c194] [cd4c2dd6a329] [7d21455c5598]

**R9. One hero SKU can carry several offers by repositioning per persona or job.** List the jobs the SKU does, test them as ad angles, and build a dedicated page and offer around each winner; the SKU does not change and margin impact is nil or positive. Condition: single-SKU or hero-SKU brands; health angles need a claims check `[web check: health claim rules per country]`. Voices: 3 (S04, S03, S10). [ec3b35527187] [9f5f2138c2b5] [c03757c10672] [44778b53f7ea]

**R10. Solve every perceived problem or expect the unsolved one to block sales.** Map what the buyer must do before, during and after use; each step needs a component, a bonus or a piece of content. Condition: S01's method; use it to generate bundle and bonus ideas, not to bloat the offer (see R11). Voices: 2 (S01, S10). [d49905c44a5d] [c509fc4145c1] [a8421dadafb4]

**R11. Simple scales; subtract what buyers do not care about.** Layer meaningful value, then remove parts a post-launch survey shows nobody valued; too much stacking becomes "too much for the consumer" and a layered offer that confuses loses. Condition: after 90 to 120 days live (S04). Voices: 3 (S04, S09, S08). [2105cc48bb5d] [42ec3370c194] [01902b9597c7] [5f2ab9d96cc7]

**R12. Market and product come before the offer.** If the category is shrinking or the product does not repeat, no offer fixes it; if the product is a daily ritual it will retain better than an occasion product, and retention benchmarks from other niches do not transfer. Condition: check before spending on offer tests. Voices: 3 (S01, S05, S04). [c6f5c92f4d60] [3e5ddfe3f852] [9d7f6e7eec35] [45e7a80365bc]

### Group B. Cost every offer before proposing it

**R13. Know the full-price waterfall for every product before any offer.** Price, all-in COGS including shipping, fulfilment and payment fees, gross margin, break-even ROAS, target CPA, contribution per order (F1 to F3). Round costs up and revenue down. Condition: always; if the brand cannot supply all-in COGS, the offer output is "unavailable" and the agent requests it via 20-FIN. Voices: 4 (S04, S08, S06, S01 card). [0b43c974ae3c] [9fe82ea9bb52] [471fc0881800] [e311b1e255a4] [c8b36a7d028e]

**R14. Judge an offer on contribution per order and contribution per visitor, never on revenue, ROAS, AOV or take rate alone.** A higher ROAS can lose more money (S06's free-shipping case); a higher AOV can cut conversion and profit (S08's year-supply case); a higher take rate can raise CAC (S03). Condition: every comparison of 2 offers. Voices: 5 (S06, S08, S04, S03, S09). [52c6ca3043ae] [90e80c5c7974] [1cda5c627ada] [52ef4486583d] [9099002370eb] [34682db50bb8]

**R15. Reset target ROAS and break-even CPA for every new offer and hand them to the paid team.** A deeper bundle, a free unit or a gift changes the margin structure, so the old targets are wrong. Condition: any change to price, tier depth, gifts or free units. Voices: 2 (S08, S04). [471fc0881800] [9fe82ea9bb52]

**R16. Model the UPT lift and put COGS on retail units, not on the discounted AOV.** Ignoring the UPT lift understates AOV; applying COGS% to the discounted price overstates margin. Condition: any discount or bundle model (F5). Voices: 1 (S04); no other source models it, and none contradicts it. [0b43c974ae3c]

**R17. Required ROAS rises much faster than break-even ROAS as a discount deepens.** Margin hits the profit target long before it hits 0, so a 15% versus 25% discount can mean roughly 8x versus 20x required ROAS in S04's illustration. Condition: use F4 with the brand's numbers; the curve, not the 8x and 20x, is the rule. Voices: 1 (S04). [99f79f8d840d] [9fe82ea9bb52] [f8754813a6a1]

**R18. Sale efficiency lift is brand-specific; measure it before trusting a discount.** S04 has modelled 70% to 80% efficiency gains during sales for luxury brands that never discount and about 5% for saturated discounters. Condition: `[needs brand data: ROAS or CPA in past sale periods versus non-sale periods, and discount frequency]`; with no history, assume the low end. Voices: 1 (S04). [0b43c974ae3c]

**R19. Match offer boldness to cash.** Cash-tight: only offers profitable on order 1 (bundles at a profitable ROAS). Funded: a first-order loss on subscription is allowed if cohort LTGP and payback are proven. Aggressive: a bigger first-order loss to win customers, only with reserves to cover months of losses. Condition: `[needs brand data: cash on hand, monthly ad spend, months to payback]`. Voices: 2 (S06, S03). [0e9661473b27] [5ea541b8c8d2] [73cdef4101eb]

**R20. Fixed per-order costs fall per unit as units per order rise; that saving funds the ladder, not the unit price.** S08: $5 shipping on 1 unit is $5 a unit, on 4 units $1.25 a unit. S04: 1 unit ships for $12, 2 for $14, 3 for $17 against $36 baked into 3 single prices, so a 3-pack saves $19. Condition: `[needs brand data: shipping and 3PL cost by units per order and weight band]`; heavy or bulky goods may not get this saving. Voices: 2 (S08, S04). [471fc0881800] [6a0ef806927d] [2105cc48bb5d]

**R21. A low AOV single item cannot carry paid acquisition; fix AOV with structure before spending.** S06's $14 sock loses on every order at a $14 to $25 CAC; free shipping makes it worse; a 4-pack at about $50 (11% off 4 singles) moves it to profit. Condition: single hero SKU, low price, paid traffic. Voices: 3 (S06, S09, S04). [52c6ca3043ae] [0090d4f61912] [34682db50bb8] [9e7e3b4c4f44]

**R22. Use the AOV × CVR > 250 screen only as a first sort.** It has no margin term and is bound to the source's currency. Pass or fail, run F2 next. Condition: S09's heuristic; convert to the brand's currency `[needs brand data: AOV, CVR, currency, margin]`. Voices: 1 (S09). [34682db50bb8]

**R23. Judge offers on gross profit and a 90-day (or repeat-cycle) LTV window, not first-order results.** An offer can win the first order and lower repeat purchase (front-loaded discounts, disappointing bonuses). Condition: any offer test; set the window to the product's repeat cycle. Voices: 4 (S07, S03, S05, S04). [89fd70abc2ef] [db90a9c32f90] [7ff6a97aeea6] [d99fcf6edcf0] [42ec3370c194]

### Group C. Pricing and price integrity

**R24. Widen the value-to-price gap by adding value first; cutting price is "most of the time the wrong decision".** Price can only fall to 0; value can rise without limit. Condition: S01's frame, applied to products by S10 and S04; not a ban on modelled markdowns (R31). Voices: 3 (S01+S10, S04, S07). [d1d1f8ddde9a] [582ef3d59a15] [a3756b7bf5f1] [82ae4d2b081b]

**R25. Do not compete on price unless your costs are about 1/10th of competitors'.** Being second cheapest has no strategic benefit (S01 quoting Kennedy). Condition: S01 opinion; for marketplace and shopping-ad SKUs where price parity is enforced, route to 12-GAD. Voices: 1 (S01). [d1d1f8ddde9a]

**R26. Price signals positioning; the lower price often loses the test.** S02: a $79 software tool sold to neither consumers nor professionals; refocused on professionals at $129, sales rose. Condition: a repositioning result, not proof that raising price alone lifts sales; test price with positioning (P24). Voices: 2 (S02, S01). [608cbae96529] [60fcb07453d8] [50211f248483]

**R27. Flat, frequent discounting re-anchors the price and trains buyers to wait.** S04: launch at 60% gross profit, end at 45% because every repeat order needs a discount. S07: 50% or 90% off sells but "is not going to last you very long". Condition: any brand; measure discount share of revenue and repeat buyers who only buy on sale `[needs brand data]`. Voices: 4 (S04, S07, S01, S06). [a3756b7bf5f1] [0c2ae5495d35] [8074b0c6c718] [82ae4d2b081b] [39853dac5920] [d5d7d14f51e0]

**R28. No invented reference prices.** S07's "jack up your price and then discount down to your target price" and S04's "list the bag at $60 and show $160, now $100" are rejected unless the higher price is a real, recent selling price in that market and the rule for "was" prices is met. Stated bonus values (S01, S07) and cover prices (S02) must be prices the item is actually sold at (S02's own rule: list it for sale at that price). Condition: ecomOS override; `[web check: reference-price and strike-through rules per selling country]`. Voices: the practice appears in S07, S04, S01 and S02; the honesty condition is S02's and the repo's. [bbc8899c72f2] [0afa90fbaa08] [769c1d67e28c] [38a0eb6af210] [6c1eb9526af9] [e3d657e18bdc]

**R29. Show the full price; never hide the total behind a first instalment or per-day figure.** Per-day and per-serving maths are allowed next to the total (R48), not instead of it. S02's "buyers react to the first payment" is a 2009 direct-mail tactic that conflicts with total-price and drip-pricing rules. Condition: always; `[web check: drip pricing and instalment disclosure rules per country]`. Voices: cards of S02 and S08; S02's text conflicts (C15). [43f3ba786866] [acb243537e19] [5f2ab9d96cc7]

**R30. Tell the pipeline before a real price rise; never raise prices silently.** Condition: any price increase; the rise itself must be real and dated. Voices: 1 (S01). [676632fcde7f] [582ef3d59a15]

### Group D. Discounts: when, how deep, how framed

**R31. Discount only in exchange for something: a bigger order, a subscription, or clearing stuck stock.** "Bundle 3 and take 15% off" or "10% off over $120" trades margin for basket size; a flat 10% off the hero product alone buys a small conversion bump and leaves the brand where it started. Condition: default for every brand; fixed-offer brands do not get new discounts at all (override rule 3). Voices: 5 (S06, S04, S07, S01, S03). [b331e530dfcf] [d5d7d14f51e0] [2b9021591176] [82ae4d2b081b] [39853dac5920] [defb3074e4c1]

**R32. A flat discount is a last resort with 2 valid uses: a few very high-margin SKUs, or grade C stock that must turn into cash.** Never to rescue a revenue number. Run it rarely: S04 says 1 to 2 times a year. Condition: S04's guardrail; a brand's own sale history sets the exact count. Voices: 2 (S04, S01). [2b9021591176] [8074b0c6c718] [39853dac5920]

**R33. Token discounts of 5% to 10% can lose money: price falls and nobody adds to cart.** Contribution per order dips until the depth where buyers start adding units, peaks (20% in S04's illustration), then falls again; past 30% to 40% it is "not worth it for anyone". Condition: S04's curve from flat-discount history; a brand must plot its own (P4). Conflict C4: S06 and S07 run 10% to 15% welcome offers and S06 says a 10% off opt-in "substantially" moves email margin. Voices: 1 (S04) for the loss claim. [99f79f8d840d]

**R34. State a fixed saving in currency and a variable saving in percent; above about $100 AOV, currency off tends to beat percent off; below it, percent off.** S02: "$50 off" produced nearly 3x the revenue of an equal "15% off" in 1 email test. S07: at $50 AOV, "10%" reads bigger than "$5"; at $200 AOV, "$20 off" reads bigger than "10%". S08 generalises: show whichever number is larger. Condition: USD heuristics; convert to the brand's currency, and in INR or other high-nominal currencies the currency figure will almost always be larger `[needs brand data: currency and price points]`. Voices: 4 (S02, S07, S08, S06 header). [582638c44d2e] [febdce2ad8fb] [9f02d954cf3b] [0b8b7baee596]

**R35. Frame extra units as "free" rather than an equivalent percent, at the same total price.** "Buy 2, get 1 free" instead of "33% off 3"; S07 claims "free always works better" from its own tests (no numbers), S02 calls "free" the strongest word, S08 prefers it. Condition: the economics must be identical (a free unit is real COGS and freight); the correct equivalent of B2G1 is 33.3% off, not the "60%" S08 compares it with. Conflict C4b: S06's speaker calls BOGO "very hard to use unless it makes sense on your margin". Voices: 4 (S07, S08, S02, S06 header). [52bf7bcc54a4] [ae0a3d67b0b3] [9ee3a3ddedd2] [274578b3f2f5] [d5d7d14f51e0]

**R36. Free usage units or product can beat an equal cash discount, and a premium can beat a cash discount, but not for B2B buyers.** S02: "30 free minutes" pulled about 2x "$5 off" (MCI); Benson's rule is that a premium beats a cash discount if you choose only 1; a business-gift firm found 25% off plus a clock radio did worse than 25% off alone. Condition: consumer offers; direct-mail evidence from 1992 to 2008, so test. Voices: 1 (S02). [7a9d0f1bb6c4] [60fcb07453d8] [eb0b5c5a0052]

**R37. Never make the buyer do mental math.** Show currency saved, per-unit or per-serving cost and per-tier saving; "67% off the 3rd unit" (which is only 22.3% off 3 units) is the pattern to avoid. Condition: all offer copy and tier badges. Voices: 3 (S08, S09, S07). [5f2ab9d96cc7] [4dc9316eaaf5] [61cf8d39f4bb]

**R38. Odd percentages (17.5%, 18%) and price endings are framing tests, low priority.** S07 offers them as ideas with no result; S02's card on price endings is the card writer's, not Bly's. Condition: test only after structural offers are settled. Voices: 1 (S07). [51d44fdc7df5] [9ee3a3ddedd2]

**R39. Discount depth tests (10% vs 20% vs 30%) are not offer tests.** Change structure (gift vs credit vs bundle vs subscription terms) before changing depth. Condition: S07 and S06 header. Voices: 2 (S07, S06 header). [82ae4d2b081b] [e311b1e255a4]

**R40. New and returning customers get different offers.** New: first-purchase economics and entry. Returning: lock-in, subscription, larger packs. A retention discount shown to the whole site trains everyone. Condition: any brand with repeat purchase. Voices: 2 (S04, S03). [8290896c9a20] [8074b0c6c718] [35bed5b98d94]

### Group E. Bundles, multi-packs and buy-more-save-more ladders

**R41. Buy-more-save-more is the first mechanic to test for a consumable or multi-unit product.** A bigger upfront quantity adds real value, filters out pure discount hunters (they will not buy 3 bags at once), and uses anchoring so the middle tier feels "just right". Condition: shelf-stable product, inventory to support it, and a real reason to own more than 1 (R46). Voices: 5 (S03, S06, S07, S09, S02). [defb3074e4c1] [75c76ec85c29] [0090d4f61912] [61cf8d39f4bb] [01902b9597c7] [7367beea9d44]

**R42. Bundle the same product (more units, other flavours or colours), not a forced mixed assortment.** S07: mixed bundles "don't perform as well" because the buyer may only want 2 of the 3 items. S06's Grind Machine and S04's cross-category bundles are the exception: add-ons that relate to the product's use. Condition: default same-SKU; mixed only when the items form a routine (04's multi-SKU case) or the brand has 1 non-consumable hero and related gear. Conflict C12. Voices: 3 for same-product (S07, S03, S09); 2 for related add-ons (S04, S06). [a4348a9802d1] [6a0ef806927d] [0090d4f61912] [9e7e3b4c4f44]

**R43. Use 3 tiers with the middle tier pre-selected and treated as the standard; do not default to the largest.** S07 (True Classic 1, 3, 6; the 6-pack is the middle of what is shown), S09 (buy 1, 2, 3 with 3 as the middle option), S02 (good, better, best; most take the middle; supplement ladder 6, 3, 1 month with the average landing at 3 to 4 months), S05 (3 options, 2 of them subscriptions, for a subscription brand), S06 header (middle tier auto-selected). Condition: the pre-selected tier must be the one whose contribution and take rate the brand wants; in fit-sensitive categories a larger default can raise returns `[needs brand data: return rate by tier]`. Voices: 5 (S07, S09, S02, S05, S06 header). [61cf8d39f4bb] [58e1159fc052] [7367beea9d44] [abb86777aeb2] [d8cbf6d9333d] [274578b3f2f5]

**R44. Step the per-unit price down each tier and show it.** True Classic: $35 single, $23 per item in the 3-pack, $20 in the 6-pack ($120, about $90 saved on 6 singles). S03's protein ladder: $50 single, $45 subscribed, $80 for 2, $120 for 3 (the 3rd tier gets no deeper per-bag price in his example, which weakens it). Condition: per_unit(n) must fall with n (F7) or the top tier has no reason to exist. Voices: 4 (S07, S03, S09, S08). [61cf8d39f4bb] [defb3074e4c1] [4dc9316eaaf5] [9f02d954cf3b]

**R45. Do not sell only the biggest pack; keep a low-friction entry tier.** S08: if the only option is a year's supply at $360, AOV rises and conversion falls, and profit per customer drops. Condition: any ladder; the entry tier stays at full price so it anchors the savings (S07, S05). Voices: 3 (S08, S07, S05). [90e80c5c7974] [61cf8d39f4bb] [7860f83f10e6]

**R46. Give each tier a physical reason to exist.** Coverage (1 unit covers 700 sq ft, 2 cover 1,400), room size, number of kids, individual versus family, days of supply (30, 60, 90). "Save more" alone is not a reason. Condition: all ladders. Voices: 2 (S08, S04). [fc891407623e] [9e3f61688b5b]

**R47. Put the variant choice before the quantity choice.** Flavour, size or colour first, then the ladder; the same structure on every sibling product so shoppers learn it once. Condition: products with variants. Voices: 1 (S09). [01902b9597c7] [58e1159fc052]

**R48. Show the per-serving, per-unit or per-day price on every tier, next to the total.** Breaks a large total into a small number without hiding the total (R29). Condition: quantity breaks and high-AOV bundles; divide by units or days of use, never by an arbitrary figure. Voices: 3 (S09, S08, S02). [4dc9316eaaf5] [5f2ab9d96cc7] [d6f9d5596273]

**R49. Every tier, including the deepest, must clear the contribution target after discount, gifts and freight (F10).** If the top tier fails, cut its savings or gifts, not the shallow tiers. Condition: before launch and after every price or freight change. Voices: 4 (S09, S04, S08, S02). [01902b9597c7] [e339ff439cf1] [2105cc48bb5d] [471fc0881800] [abb86777aeb2]

**R50. Read take rate per tier after launch and retune quantities, prices and savings within unit economics.** Most buyers on tier 1 means the ladder is not working. Condition: at least 1 repeat cycle of data `[needs brand data: orders by tier]`. Voices: 2 (S09, S03). [58e1159fc052] [75c76ec85c29]

**R51. Bundles can be skipped when subscription plus a useful gift fits the product better.** S08's example brand runs no bundle, optimises subscription opt-in and uses a free gift. Condition: replenishment products; an alternative, not a better option. Voices: 1 (S08). [c2bff6b33753]

**R52. Bundles are the obvious offer; they protect contribution margin but "you could do a lot more".** Layering a bundle with a starter kit, a subscription unlock or a scaling gift makes a stronger offer than any one mechanic, provided the presentation stays clear (R11). Condition: after the ladder is costed. Voices: 2 (S04, S09). [6a0ef806927d] [01902b9597c7]

### Group F. Gifts with purchase, welcome kits and bonuses

**R53. A gift must help the buyer use the core product and cost the brand little.** Frother, spoon, creamer or bottle for a drink powder; a sample kit; a dosing tool; not stickers, tote bags or generic swag. Later gifts can shift to revenue expansion (samples of other SKUs, branded items). Condition: all gifts and welcome kits; S06's speaker praises a journal and a luxury getaway, which is his own inconsistency, not a rule. Voices: 5 (S05, S07, S03, S06 header, S04). [503d2fb72fc1] [494b95673d4f] [eaf22ff0c7f6] [a4608f159609] [0afa90fbaa08]

**R54. Prefer a low-landed-cost product or sample to a deeper discount.** 10% off a $100 product costs $10; if a SKU has landed cost under $5 to $10, giving it costs less and attracts value buyers rather than discount hunters. A mystery gift can cost $0 to $3 (samples, a co-marketing partner's sample, an item bought on a large PO that fits the box). Condition: needs more than 1 SKU or a sample format `[needs brand data: landed cost per SKU]`. Voices: 3 (S03, S04, S07). [a4608f159609] [defb3074e4c1] [2105cc48bb5d] [bbc8899c72f2]

**R55. Gifts scale with units and sit on the tier you want to sell.** More free mugs as you buy more bags (S09); the objection-fixing guarantee only on the 2-pack (S04); S09's "Jabi" ladder gives 1, 1, 3, 4 gifts for 1 to 4 bottles, so the jump to tier 3 is the big one. Condition: gift cost is inside CP_tier (F10). Voices: 2 (S09, S04). [e339ff439cf1] [01902b9597c7] [0afa90fbaa08]

**R56. Never gift more of the same product.** It devalues the unit price the customer just paid. Condition: gift roadmaps and welcome kits; a free unit inside a later 90-day order framed as "an extra 30 days" (S04) is a bundle tier, not a gift, and must be costed as one. Voices: 1 (S05); S04 uses the free-unit tier idea. [503d2fb72fc1] [ec3b35527187]

**R57. Tell people about a gift at every step or it buys nothing.** Show it on the PDP before purchase, in onboarding, in the billing reminder, and make the customer click to claim where possible; a hidden surprise gift sent to everyone retains the people who were staying anyway. Condition: any gift roadmap. Voices: 2 (S03, S05). [d4bfd76ee183] [503d2fb72fc1] [e9c9f0ad1a68]

**R58. Untargeted order-2 gifts usually fail the payback test; gifts belong in the acquisition promise or in a targeted save.** S03's maths: 1,000 subscribers, 900 reach order 2, gifts at $2 to $5 cost $1,800 to $4,500; a 5% lift is 45 orders. S05 places gifts at months 2, 4 and 6 (his "highest churn months") and says every-order gifting is more than needed. Condition: run F13 with the brand's churn by order number `[needs brand data]`. Conflict C11. Voices: 2 (S03, S05). [d4bfd76ee183] [503d2fb72fc1]

**R59. Bonuses for products are how-to content, tools and checklists, not more reading.** Styling videos, usage protocols, dosing and timing guides, recipe or pairing guides, a program with a stated length; S01's rule that tools and checklists beat more training holds. Condition: the bonus answers a specific reason the buyer thinks they will fail; near-zero incremental cost; must be delivered and used or it hurts retention (S04's chatbot meal plans). Voices: 4 (S10, S01, S06 header, S04). [a8421dadafb4] [7d21455c5598] [cadfc89e4c1d] [412980697148] [42ec3370c194]

**R60. Stated bonus and kit values must be real prices, and the stack anchors to the core price.** S01: total bonus value should exceed the core offer's value; S02 (Bell): total premium value above the main price, as a hypothesis; S05 and S07 show kits with a value on the page (IM8 $89 or $100; AG1 $43 and $72). Condition: each value is a price the item sells at (R28) `[web check: reference-value claims per country]`. Voices: 4 (S01, S02, S05, S07). [7d21455c5598] [6c1eb9526af9] [7860f83f10e6] [494b95673d4f]

**R61. Two premiums often beat one, but a choice of premiums seldom works.** Give each item a job; do not ask the buyer to pick (a decision deferred is a decision not made). Condition: S02's direct-mail evidence; test. Voices: 1 (S02). [6c1eb9526af9] [48c07a67fbf9]

### Group G. Thresholds and cart-level offers

**R62. Set spend and free-shipping thresholds on the order-value distribution, not on the mean AOV.** Export order-level values, plot the count by band, look for 2 peaks; aim 1 offer at each peak to move it up; with 1 peak, move the core group up 1 step (30-day to 90-day). A threshold near the mean gives free shipping to buyers already above it and moves only a thin band (about 10% in S04's example). Condition: `[needs brand data: order-level order values]`; re-plot after any price, bundle or threshold change. Voices: 1 (S04); S06 gives a threshold example ($120) without a method. [a1a57841df7a] [c9081fedfb43] [f0cd279bc44b] [9e3f61688b5b] [b331e530dfcf]

**R63. A free-shipping threshold is a weak lever on its own and can lose money on low-AOV orders.** S06 ranks it "cheaper but weak"; S06's $14 free-shipping case lifts ROAS and loses more than paid shipping. Condition: run F17; use a threshold only above a peak, and never on a single low-price item. Conflict C1. Voices: 2 (S06, S04). [d5d7d14f51e0] [52c6ca3043ae] [a1a57841df7a]

**R64. Unlock a product, sample or gift at the threshold, not only shipping.** A progress bar at the top of the drawer cart ("add 1 more and get X"), samples or a complementary item at the threshold, and optionally chained unlocks (free shipping first, then a gift). Condition: cart layout itself belongs to 07-LPG; the economics belong here (F10 for the unlocked item). Voices: 3 (S04, S09, S06). [fa0ea3889627] [3ddf9722dfa2] [3817d0f2245c] [b331e530dfcf]

**R65. Frame cart offers as "the more you add, the more you save" and check the bigger cart covers the discount.** "10% off over $120", "3 items, 15% off". Condition: contribution per order must rise, not just revenue. Voices: 1 (S06). [b331e530dfcf]

**R66. Cart offers that trigger only on adding a product (Dr. Squatch's free shipping for adding an item, in-cart upgrade to subscribe-and-save) beat unconditional ones.** Condition: the trigger item must clear F9. Voices: 2 (S06, S09). [0090d4f61912] [2b91c05f98d2]

**R67. In cart, keep 1 offer per slot, relevance over price, legible in 2 to 3 seconds.** Three offers cause decision fatigue; a good price on an irrelevant item does nothing; the copy is usually a flat discount on the added item. Condition: drawer cart cross-sells. Voices: 1 (S04). [0fc1f8211e17] [67ab77318d00]

### Group H. Upsells, cross-sells, checkout add-ons and post-purchase offers

**R68. Score every upsell and cross-sell by incremental contribution per exposed order: take rate × added value × gross margin of the added item (F9).** Rank on that product, not on take rate, AOV lift or margin alone. S04's own A versus B example is arithmetically wrong (A = $2.40 beats B = $1.80 on his inputs), so trust the formula, not his conclusion. Condition: every slot. Voices: 1 (S04). [52ef4486583d] [456ea796c7fe] [67ab77318d00]

**R69. Measure upsell lift against a holdout.** Takers self-select, so AOV among takers overstates lift. Condition: card addition to S04, consistent with 09-CRO. Voices: 1 (S04 card). [456ea796c7fe]

**R70. Place offers by friction: in-cart for threshold unlocks (5% to 15% take), checkout for a low-friction add-on only, post-purchase one-click for full products (35% to 40% take seen).** Do not sell another full product at checkout. Condition: S04's current view (he says it changed); the take rates are his experience `[needs brand data: take rate by placement]`; `[verify UI]` for one-click post-purchase support on the platform. Voices: 1 (S04); S06 lists one-click upsells and order bumps as "free money" without placement rules. [3ddf9722dfa2] [d2c3bb4a5a83] [caf68780fe4e] [d5d7d14f51e0]

**R71. Post-purchase: anchor high, then down-sell.** Show a $50 to $60 upsell first; if declined, $20 to $30; if taken, $30 to $40. Leading with the cheapest item anchors low and makes everything after look expensive. Expect declining take rates (about 25% then 10% in S04's example). Condition: S04's method; RPV target 10% to 15% of AOV is his benchmark. Time-limited post-purchase chains ("next 60 minutes") are allowed only if the timer is real (R111). Voices: 1 (S04). [6856ee4fdaf4] [caf68780fe4e]

**R72. Checkout add-ons such as shipping protection are high-margin but carry a consumer-law and trust check.** S04: $4.99, about 30% take, near 100% margin, $1 to $2 gross profit per order, because carriers pay most claims. Condition: pre-ticked add-ons are a dark-pattern risk in several markets `[web check: rules on pre-selected checkout add-ons per country]` `[needs brand data: claim rate and carrier terms]`. Voices: 1 (S04). [3ddf9722dfa2] [d2c3bb4a5a83]

**R73. Cross-sells work as samples in the next box, not as onboarding sales emails.** Put a sample of the second product in order 2 where it doubles as a gift; S03 sees little success with cross-sell emails in onboarding. Condition: subscription and replenishment brands; email execution in 14-EML. Voices: 2 (S03, S05). [a4608f159609] [df3fcc51281e] [503d2fb72fc1]

**R74. Feed upsell gains into the CAC ceiling.** If contribution per order is $20 and an upsell adds $2, allowable CAC rises by about $2. Condition: after a holdout-measured lift. Voices: 1 (S04). [52ef4486583d]

### Group I. Subscription offer design

**R75. Optimise for the first order being a subscription, because the gap is large and one-time buyers rarely convert later.** S05's client: 6-month LTV about $130 one-time versus about $195 subscription (+50%), about 2x at 12 months, 3x at 24. S07's dashboard: about $226 versus $138 at month 6, and only about 10% of one-time buyers later subscribe. S06: $165 versus $289 at month 6. Condition: consumable with repeat use; part of every gap is self-selection, so size the offer from the brand's own cohorts, not these numbers `[needs brand data: LTV by first-order type at 90 days, 6 and 12 months]`. Voices: 3 (S05+S07, S06, S03). [d99fcf6edcf0] [02a3e80a55a4] [971d6e5bf0ce] [5ea541b8c8d2] [a84f21107a98]

**R76. A flat 10% to 15% subscribe-and-save on 1 SKU only says "cheaper" and gives no reason to subscribe today.** On a $20 product 10% is $2. S07 ranks the basic recurring discount the weakest of 4 models. Condition: any subscription buy box; what replaces it is contested (C5). Voices: 3 (S03, S05+S07, S06). [defb3074e4c1] [75c76ec85c29] [5ff86e2e0a6f] [971d6e5bf0ce] [00081cdadc00]

**R77. Put the offer on the subscription option and keep one-time at full price, small and recessed.** Discount, welcome kit, guarantee and program access go on subscription only (IM8, H1, Everyday Dose, AG1). Condition: a take-rate strategy for consumables; the one-time option stays visible (C6), and the removal of every one-time discount must be tested against one-time demand `[needs brand data: one-time versus subscription conversion and LTV]`. Voices: 2 (S05+S07, S03). [7860f83f10e6] [bbc8899c72f2] [971d6e5bf0ce] [9099002370eb]

**R78. Pre-select subscription and show 3 options, 2 of them subscriptions.** Default bias decides take rate; with 2 options one-time is half the choices. Condition: `[verify UI: subscription widget default setting]`; pre-selection of a recurring charge is regulated in some markets, so the price, cadence and cancel terms must be stated next to the default `[web check: pre-selected subscription and auto-renewal disclosure rules per country]`. Voices: 2 (S05, S06 header); S09 shows a subscription-only page as 1 valid layout. [d8cbf6d9333d] [274578b3f2f5] [01902b9597c7]

**R79. Front-load the discount and lower the recurring rate, then validate on 90-day LTV.** S07's pick: 25% off the first order, 10% recurring; Armra about 30% first, about 5% recurring (S03's host, S07); S05's examples 30% off a 90-day supply, 55% (Everyday Dose), a saving of €40 (H1); S06 header 25% to 30% first, 5% to 10% recurring. Condition: the recurring rate must still beat any public sale rate (R92); the first-order margin at the net price must be modelled (F10, F11) and the churn after order 1 watched `[needs brand data: churn by month for front-loaded cohorts]`. Conflict C5 (S03 dislikes upfront discounts). Voices: 3 (S05+S07, S06 header, S03's host reports the Armra numbers). [971d6e5bf0ce] [5ff86e2e0a6f] [7860f83f10e6] [00081cdadc00] [9099002370eb]

**R80. Take rate is a trade between conversion and LTV, set by contribution margin, not a target in itself.** Pushing take rate to 80% to 90% usually raises CAC because people who do not want to subscribe are pushed away. While LTV supports it, keep subscription prominent and one-time as a small link; when CAC becomes untenable, test a one-time option, a gift with purchase or a quiz funnel. Condition: needs contribution margin per order and cohort retention `[needs brand data]`. Voices: 1 (S03), consistent with S05 and S07 on prominence. [9099002370eb] [73cdef4101eb]

**R81. Choose the profit shape by modelled total profit: front-loaded (first-order profit) or back-loaded (earn it over the LTV tail).** Some brands get about 80% of needed LTV on order 1; others take less upfront. Condition: F11 with the brand's cohorts; the card's mapping of fast-acting products to front-loaded profit is an inference, not stated by S03. Voices: 1 (S03). [73cdef4101eb]

**R82. Gate the best part of the offer on the behaviour you want.** S04: the 25% lifetime rate needs the 90-day supply and a ticked subscription box; no tick, no offer. S05 and S07: kit and program only on subscription. Condition: the gate must be stated plainly at the point of choice. Voices: 3 (S04, S05+S07, S09). [858ec2cdad96] [2105cc48bb5d] [7860f83f10e6] [01902b9597c7]

**R83. Match cadence and pack size to real use, and let the customer change frequency easily.** 30 servings on 30 days only for daily use; offer 3, 5 or 6 week cadences, not only 4; a beverage brand lets buyers pick can count. S03 cites an old Autoship Cloud study: subscribers who adjusted frequency 3 times had about 200% higher LTV (correlation). "Too much product" is usually the biggest cancel reason (S05). Condition: `[needs brand data: servings per pack, use rate, cancel reasons by plan]`. Voices: 2 (S05, S03). [167cf8e69e33] [34907451e7ef] [1ae7b0ed8e41]

**R84. Add a longer plan tier with more value, and consider prepaid plans to pull cash forward.** IM8: 90-day plan 30% off with a $100 kit, program and 90-day guarantee; 30-day plan 20% off with a smaller kit; AG1: 3-month plan $72 of gifts versus $43. S06: prepaid 90-day to annual plans at a "major discount"; S03: prepaid or 3-month commitment earns 2 extra months during a sale. Condition: the prepaid discount must be costed against churn saved, and no discount level is given by any source. Voices: 3 (S05+S07, S06, S03). [5ff86e2e0a6f] [90826afade8a] [35bed5b98d94]

**R85. Design gift roadmaps as an acquisition promise, shown before purchase, and place later gifts where churn peaks.** Everyday Dose gives gifts on orders 2 to 5; S05 says months 2, 4 and 6 are enough; Elevate unlocks 8 or 9 items across 1 to 4 month supplies (gamified tiers). Condition: R57 and R58 apply; `[needs brand data: churn by order number]`. Voices: 3 (S03, S05+S07). [d4bfd76ee183] [503d2fb72fc1] [defb3074e4c1]

**R86. Set a long results horizon for slow-acting products and promise nothing early.** Tell buyers 90 to 120 days (S05), "a 3-month game" (S03); brands that promise early results see cancels at the promised point. Condition: daily-use supplements and skincare; the timeline must be supported by evidence `[needs brand data: evidence for any result timeline]`. Voices: 2 (S05, S03), plus S04's hair-health example. [2762401ae2f2] [1493dc0bce84] [ec3b35527187]

**R87. Test multiple subscription offers and personas; never settle on 1.** The same product serves several jobs with different conversion, take rate and LTV; run separate hooks and funnels per job, tag self-selected persona data (popup quiz, post-purchase survey) and read cohorts by tag. Start by about $1M a year. Condition: consumables with several distinct reasons to buy. Voices: 2 (S03, S04). [c03757c10672] [9f5f2138c2b5] [7ff6a97aeea6] [33ff2c0b8e49] [ec3b35527187]

**R88. Subscription is an auction: higher LTV lets you outbid rivals, but only with cash to carry order-1 losses.** Done wrong it is "one of the quickest ways to bleed your business dry". Condition: R19; LTV ceiling from F11 on gross profit, not revenue. Voices: 2 (S06, S03). [5ea541b8c8d2] [0e9661473b27] [00081cdadc00] [a79ffdb8c9a0]

**R89. Growth is capped by acquisition when the base nears new-per-month divided by churn (F12).** Then test budget goes to offers, hooks and personas, with retention work kept running. Condition: S03's frame; do not read it as "retention work has no value". Voices: 1 (S03); S05 argues the opposite priority (C13). [a84f21107a98] [a79ffdb8c9a0] [9d7f6e7eec35]

**R90. Understand the customer's lived experience before offer testing.** Whole-team whiteboard of what customers like and hate; buy and live the full journey; call customers when small. Condition: before any subscription offer redesign. Voices: 2 (S03, S05). [cfdb1e2cd594] [1c5f9fce2bb2] [2762401ae2f2]

### Group J. Subscription mechanics that change the offer (portal, skip, cancel, win-back, sales)

Build steps for these live in 17-CXP and 14-EML. The rules here set the offer logic the agent must respect.

**R91. A sitewide sale must not equal or beat the subscriber rate.** If sitewide is 20% and subscribers get 20%, the sale gives subscribers nothing and they cancel to rebuy; decide first whether cancel-and-rebuy is acceptable. If not, you cannot run 50% sitewide. Condition: every promotion at a subscription brand. Voices: 2 (S03, S05). [35bed5b98d94] [1b7f42b5f9e3]

**R92. Build the subscriber offer first, then trickle down to the public.** S03: 40% sitewide but subscribers get 50% on items added during the sale, or 2 free months for prepaid; S05: exclude active subscribers from standard promos and give them their own add-on deal (30% off an add-on to the next order). Then brief ads and email that the public offer points to what subscribers get. Condition: subscription brands. Voices: 2 (S03, S05). [35bed5b98d94] [1b7f42b5f9e3]

**R93. Layer a subscription offer into every sitewide sale and state the stacked total the way checkout applies it.** S03's host: 20% sitewide plus 20% subscribe-and-save, led as "save up to 40%" then "20% off for life"; compounded it is 36% (F14) `[verify UI: discount stacking]`. Condition: only when R91 holds. Voices: 1 (S03 host). [35bed5b98d94]

**R94. Inside the cancel flow, a discount is the strongest save lever; use it there, not upfront (S03's position).** Match the action to the reason: expense gets a discount on this order (20% to 30%; 40% to 50% for a genuine budget change), too much product gets delay or a frequency change, wrong product gets a swap. Flat currency offers only for baskets over about $100. Condition: F18 must show the saved LTGP exceeds the cost; limit repeats so customers do not learn to cancel for the offer (S05 card). Voices: 2 (S03, S05). [a006e3aa6f9c] [1ae7b0ed8e41]

**R95. Founder video first, then reasons, then offers; the cancel page is where the last save happens but most effort belongs earlier.** S03: struggling brands moved from 5% to 6% save rate to about 15% with a 1-minute founder video; S05's bands: under 10% needs work, 15% good, 20% very good. Condition: `[verify UI: splash video support in the subscription platform]`; a flow that hides cancel is a legal risk (R96). Voices: 2 (S03, S05). [2555be53857a] [1ae7b0ed8e41]

**R96. Cancel must stay findable and completable; save offers may not become a trap.** S05's "delay on top, manage at the bottom" billing reminder and S03's "make one-time a hyperlink" are prominence choices; hiding the cancel path or adding steps is not allowed in ecomOS. Condition: `[web check: click-to-cancel, negative-option and dark-pattern rules per country; India 2023 guidelines list subscription traps]`. Conflict C9. Voices: ecomOS override; S05 raises the legal flag on billing reminders only. [32e1b81135d0] [1ae7b0ed8e41] [945cce30648f]

**R97. No open-ended pause; 1 skip; delay capped at about 30 days by default, tested longer for large packs.** Pause leaves subscribers in limbo with about 10% reactivation (S03's rough figure); a "pause" that auto-resumes is a delay and should be named one. A skip is delayed revenue, not a save; push chronic skippers to "get it now" with a bonus or out to win-back. Condition: S03 and its host's rule; S05 lists pause among portal perks (C14). Voices: 1 (S03). [34907451e7ef] [394bd4ca221e] [4f318efde260]

**R98. No big offer in the cancel confirmation; win-back offers can be aggressive and change the product relationship.** S03: rotate a new win-back offer to all cancelled subscribers every 1 to 2 weeks and judge click and reactivation rate; examples: 50% off A plus B together, free B for 3 months with 3 months of A. S05: 30 to 60 days after cancel, a bigger first-order-back offer (30%, 40% or 50%) stepping down to the standard 15%. Condition: broad first, reason-split only with bandwidth (C16). Voices: 2 (S03, S05). [42ece6bd5274] [552ee801d868]

**R99. Subscribers are their own segment: fewer sends, their own offers, and every send has a stated intention.** Do not skip billing reminders "because they cause cancels" while opting all subscribers into campaigns; S05's reminder rewrite cut cancel rate from 8.6% to 5.8% in 1 A/B test. Condition: email build in 14-EML; billing reminders are legally required in some places `[web check: auto-renewal notice rules per country]`. Voices: 2 (S03, S05). [525866e33d96] [32e1b81135d0] [1b7f42b5f9e3]

**R100. Failed payments leak 5% to 10% of subscription revenue at a few million a year; recovery is an offer-adjacent lever.** Condition: S03's estimate; route the build to 17-CXP. Voices: 1 (S03). [9644aea14d42]

### Group K. Guarantees and risk reversal

**R101. Cost the guarantee before proposing it (F8).** Compare net contribution, not net orders, across versions; include refund, return shipping, handling and lost resale value. S01's 95 versus 117 example omits the refund cost; do not. Condition: every guarantee change; `[needs brand data: refund and return rate, return cost per order, resale rate]`. Voices: 3 (S01, S02, S04). [4d72bb91baae] [264e18c4c7be] [729e71de2194] [322b4dd8abd3] [0afa90fbaa08]

**R102. Write the guarantee as "If you do not get X in Y time, we will Z"; without the "or what" it is weak.** Name the fear it removes (fit, durability, taste, results, damage). Condition: all guarantees; the "X result" must be a claim the brand can make `[web check: outcome claims per category]`. Voices: 2 (S01, S02). [eaf3e7847805] [4f18a85334fc]

**R103. Decide 4 things: length, conditionality, coverage, activation.** Length: S02 prefers 60 or 90 days over 30 (a 60-day trial beat 30 by 10%; 90 no better than 60 in 1 test); Space Goods shows 60 days (S09); IM8 90 days (S07). Conditionality: S02 says unconditional is best and conditions like "in saleable condition" depress sales; S01 says prefer conditional when fulfilment cost is high. Coverage: say "product refund" if shipping is not refunded. Activation: clock starts on receipt, and the claim method is spelled out (return the unused portion "or even the empty bottles"). Condition: physical goods carry reverse-logistics cost that e-books do not, so the S02 default needs a returns-cost model first. Conflict C17. Voices: 3 (S02, S01, S09). [729e71de2194] [4f18a85334fc] [da1973ba6fc3] [0a29207c3138] [d7f2ba51f82c]

**R104. A money-back guarantee is close to table stakes for physical products; the second layer is what differentiates.** Options: try-before-you-buy with delayed capture (Amazon's 7-day model in S10; S06 header), a keep-the-bonus refund (S02: keeper premiums; a keep-the-e-book refund lifted conversion 21% for digital goods only), an outsized refund (double your money back tripled attendance for a workshop in S02), a lifetime guarantee on the tier where durability is the objection (S04). Condition: each layer removes a different risk and the combined worst case is modelled (S01 card); delayed capture moves cash timing and return risk onto the merchant `[web check: processor support for delayed capture]` `[needs brand data: fraud rate]`. Voices: 4 (S10, S02, S04, S01). [d51c9104d84e] [88ee7e21b5aa] [e3d657e18bdc] [2de80b052adc] [5450fc48fb31] [0afa90fbaa08]

**R105. Make the guarantee visible near the price and at checkout, in plain type.** Not an 8-point footnote; S09 shows it under the buy box with the delivery date. Condition: the short version near add-to-cart, the full policy linked. Voices: 3 (S02, S09, S10). [7e4c3385639c] [d7f2ba51f82c] [f106bb47354d]

**R106. Guarantees are enhancers, not a cover for a weak product or checkout.** Refunds from a bad product make the guarantee a liability; tie conditions to actions that make customers succeed where results depend on use. Condition: S01; consumable outcomes (creatine, skincare) need a use period before judging (R86). Voices: 2 (S01, S02). [eaf3e7847805] [7a9d0f1bb6c4]

**R107. Name the guarantee for clarity and brand fit, not boilerplate and not shock.** "30 Day Money Back Satisfaction Guarantee" is weak (S01); S01's shock names are style, not required. Condition: on-brand, clear, no invented claims. Voices: 1 (S01). [1890fdd95d42]

**R108. "All sales final" only for genuinely non-returnable value, and never with an invented reason.** S01's "just make one up" is rejected. Condition: hygiene, customised or perishable items, with the true reason stated `[web check: statutory return rights per country, which may override any policy]`. Voices: 1 (S01), bounded by the repo rule. [9413eb3d3ddf]

**R109. Trials and samples fail through inertia, not only fear; add a decide-by incentive and reminders.** "Free use" beat "free trial" by 15% in S02's test; sample on the buyer's own need where possible. Condition: trial and sample offers; measure activation and return rate, not sign-ups. Voices: 1 (S02). [7a9d0f1bb6c4] [4e2954e81935]

**R110. Broad guarantees suit lower-ticket B2C; specific, conditional ones suit higher ticket.** Condition: S01 opinion; for jewellery-grade tickets the guarantee terms interact with statutory rights and resale, so the returns-cost model decides. Voices: 1 (S01). [da1973ba6fc3] [7b7abfbdcab4]

### Group L. Scarcity, urgency and drops (honest only)

**R111. Scarcity is quantity, urgency is time; use either only when it is real, enforced and provable.** Real stock per variant, a real drop size, a real end date and time with time zone, a real post-deadline price. Fake countdowns "lose credibility" (S01); S02's "an invented reason can work", S10's stock counts and 60-minute deals with no truth condition, S07's "79% claimed" bar he cannot verify, and S09's "reserving your order due to high demand" timer are all rejected unless true. Condition: ecomOS override; `[web check: false urgency and scarcity rules per country; India 2023 dark-pattern guidelines; UK DMCC; EU UCPD; US FTC]` `[needs brand data: live inventory by variant, production limits]`. Voices: the honesty condition is S01's and S02's own; S06 header, S07, S09 and S10 present the tactics. [9264ceff1dcd] [4fc1b785cdaa] [e456aab8c58a] [ea94a39e0ec6] [c5deb26d06e5] [275612802571] [bb89fca1e69e] [3817d0f2245c] [483d4914fae6]

**R112. Limited releases: fix the run, sell out, tell everyone, repeat about monthly, not more.** Limited flavours, colours, designs or sizes (S01's 100 boxes); S10's 100 printed shirts on a Friday. Better to sell out consistently than over-order; announce the sell-out; keep some demand unmet so the next drop compounds. Condition: a limited-release model, not core SKUs, which must stay in stock; `[needs brand data: inventory and production limits]`. Voices: 1 voice (S01+S10). [b83b87f23486] [47afc4b21d24] [e456aab8c58a] [275612802571]

**R113. Make the promotion or bonus expire, not the product.** Rolling seasonal wrappers with real dates ("ends 31 March"), a bonus that ends, a price rise announced before it happens. Condition: the date holds; never extend a stated deadline (S02); rename the wrapper about every 4 weeks at most (S01). Voices: 2 (S01, S02). [676632fcde7f] [9264ceff1dcd] [ea94a39e0ec6]

**R114. Deadline length: long enough not to rush, short enough to matter.** S02's direct-mail guidance: 7 to 21 days for mail, "this week only" or 48 hours for email with 1 or 2 reminders; S01: the last 4 hours of a week-long launch can carry 50% to 60% of sales (no data). Condition: S02's numbers are 2009 mail figures; treat as test ideas `[needs brand data: sales by hour in past launches]`. Voices: 2 (S01, S02). [ea94a39e0ec6] [c5deb26d06e5] [9264ceff1dcd]

**R115. A fixed print run or "only N left" is not credible for anything unlimited.** S02 on PDFs; the same holds for made-to-order goods without a real cap. Condition: any scarcity claim. Voices: 1 (S02). [ea94a39e0ec6]

**R116. Keep the core offer evergreen; put urgency on a separate, honest flash-deals surface or on the lifetime rate window.** True Classic runs bundles year-round and a flash page for overstock (S07); S04 puts urgency on the lifetime subscription rate window. Condition: the flash deals are really refreshed and the window really closes (S07 admits he does not know if True Classic refreshes daily). Voices: 2 (S07, S04). [bb89fca1e69e] [858ec2cdad96]

### Group M. Promotions, cannibalisation and offer lifecycle

**R117. An evergreen stacked offer beats a rotating promo calendar.** A 52-week calendar of percent-off rotations is "the complete wrong definition of offers" (S04); a well-built stacked offer lowers the efficiency the brand must hit all year (S04's example: required ROAS 6x to about 2.9x at the same contribution). Condition: consumables with repeat purchase for the subscription part; the stack itself for any brand. Voices: 3 (S04, S07, S01). [2105cc48bb5d] [8074b0c6c718] [bb89fca1e69e] [39853dac5920]

**R118. Before any sale, compute cannibalisation and require the sale to clear it.** Inputs: share of the last 30 days' revenue that would have come at full price anyway, subscriber rebuy leakage (R91), pull-forward from the next 30 days, refund rate in past sales, and required ROAS at the sale depth (F4). The sale is approved only if incremental contribution after these exceeds 0 and price integrity survives (R27). Condition: every promotion; `[needs brand data: past sale periods, subscriber base, refund rates]`. Voices: the components come from S04, S03, S05 and S07; no single source gives the full test. [0b43c974ae3c] [35bed5b98d94] [1b7f42b5f9e3] [2b9021591176] [82ae4d2b081b]

**R119. Set stop rules before launch: required ROAS or CPA not met for N days, discount share of revenue above a cap, subscriber cancels above baseline, refund rate above baseline, stock below the level the scarcity claim states.** Condition: written into the promotion plan (9.3); the exact N and caps come from the brand's history. Voices: derived from S04's required-ROAS gate, S05's subscription-cancelled tracking per campaign, S01's honest-scarcity rule. [f8754813a6a1] [1b7f42b5f9e3] [e456aab8c58a]

**R120. Q1 (or any seasonal dip) is an offer problem, and a good time to test offers.** Rotate in offers that fit the season rather than accept the dip. Condition: S04's opinion; conversion is suppressed so tests need more traffic (09-CRO). Voices: 1 (S04). [8074b0c6c718]

**R121. Hold a winning offer 6 to 12 months while testing challengers on side funnels; audit it after 90 to 120 days live.** Survey buyers on which part convinced them, remove parts nobody valued, check the bonus did not disappoint, and check repeat rate by offer. Condition: S04's observation of large CPG brands. Voices: 2 (S04, S01). [39335b89c471] [42ec3370c194] [b261bc411259]

**R122. About 100 offers are possible, about 10 are good, and nobody knows the winner until it is tested in market.** Condition: creative and the rest of the funnel must be stable or the test is confounded. Voices: 3 (S04, S08, S02). [9e3f61688b5b] [1cda5c627ada] [3ab744029b93]

**R123. Refresh a fatigued offer in this order: creative, body copy, headline or wrapper, duration, enhancer, then monetisation and price.** Each step down is more operationally heavy; do not call an offer fatigued because the audience saw it once; once an offer is monetised, rarely change it. Condition: `[needs brand data: reach, frequency, CTR and CVR trend by creative]`. Voices: 1 (S01). [b261bc411259] [1874fa3ba153]

**R124. A loss leader is allowed only with a planned attachment path and a capped loss.** Profit comes from later sales; plan the back end (bundle, replenishment, email) before traffic arrives and judge on cohort contribution. Condition: S02's direct-mail rule, translated by its cards. Voices: 1 (S02). [b1e72aa6f5b2] [ab07ca65bb72]

### Group N. Pop-up and first-order offers

**R125. Run a first-order offer in the pop-up; a bare "join our community" or a plain 10% off is not enough.** S06: no offer 1% to 5% opt-in, static 10% off about 7%, mystery framing of the same 10% about 15% (17.46% at 1 client). S07: "just throw up a 10% off" is the common mistake. Condition: brands that discount at all; fixed-offer brands present the fixed offer or a non-discount hook (R133). Voices: 2 (S06, S07; S05 adds that the pop-up must not undercut the subscription offer). [42cf8bc4ce3a] [1f0ee6e31e5c] [7860f83f10e6]

**R126. Only 4 first-order offer types are worth running: currency off, percent off, free gift (including B2G1), and cash back or credit.** No giveaways (low-quality leads) and no free guides (low intent) for a DTC store. Condition: S07's agency view; S02's bait-piece method is the opposite view for considered purchases (C18). Voices: 1 (S07). [1f0ee6e31e5c] [04eeb7082406]

**R127. Test structurally different pop-up offers on equal traffic and judge on placed-order rate, gross profit and 90-day LTV, not opt-ins.** S07's 8-variant test: the incumbent free gift (520 opt-ins, 3.3% placed-order rate) lost to "$25 in credit" (about 1,800 opt-ins, 10.7%), with mystery framing of the same $25 in between (7.6%). Condition: 1 client test at $250 to $300 AOV; credit must be a real, redeemable balance with known breakage `[needs brand data: redemption and breakage]`. Conflict C7. Voices: 1 (S07). [db90a9c32f90] [e54276a5821f] [89fd70abc2ef]

**R128. Mystery or "exclusive" framing lifts opt-in on the same discount, but the revealed value must feel worth it.** S06 and S07 both use it; S07's test shows an explicit credit figure beat the mystery version. Condition: full-width pop-up, value revealed in the first message (14-EML); `[verify UI: reveal formats in the pop-up tool]`. Voices: 2 (S06, S07). [42cf8bc4ce3a] [63e5c2109fe1] [e54276a5821f]

**R129. The pop-up offer must be the site's offer: no separate one-time discount that undercuts the subscription or bundle offer, and no conflicting codes.** S05: a 10% pop-up that only works on one-time purchase makes a 20% subscription offer look weak. S07: list every live discount, confirm which combine at checkout, and advertise the true combined value once ("you've got $X off"), or "up to $X" only if a further layer really stacks. Condition: R28 and F14; `[web check: "up to" savings-claim rules per country]`. Voices: 2 (S05+S07). [7860f83f10e6] [9e01130cee63]

**R130. Count the whole pop-up chain: opt-in, email revenue per subscriber, discount cost and ESP cost (F16).** S06's scenario (2 million visitors, $0.30 per subscriber a month) shows a 3x subscriber count is 3x email revenue, minus higher ESP tiers and discount cost. Condition: `[needs brand data: visitors, opt-in rate, revenue per subscriber, ESP pricing]`. Voices: 1 (S06). [42cf8bc4ce3a]

**R131. Give exit and abandonment offers by commitment stage: browsers generous with urgency, cart abandoners small, checkout abandoners no discount, only risk reversal or free shipping.** Checkout abandoners were stopped by friction and will likely buy in 2 to 3 days; S04 prefers abandoned-flow email to exit pop-ups. Condition: S04's logic; common practice discounts checkout abandoners (C2). Voices: 1 (S04). [ec51739ce59d]

**R132. Keep a low-commitment path beside the buy button for considered purchases.** A buying guide, fit quiz or "remind me" capture draws out buyers who are not ready (S02's soft offer); a "why not today" exit question routed by reason (price, fit, timing) tells the brand why. Condition: high-consideration or gifting categories (jewellery is one); the ecommerce translation is the cards', not Bly's. Voices: 1 (S02). [1944526d2b8a] [207cd91b5fae] [c2720146fa16] [b4af036c7d67]

### Group O. Fixed-offer presentation and congruence

**R133. Fixed-offer brands get presentation fixes, not new discounts.** When the owner has fixed the offer (Peach Bucket is one), the agent's whole scope is: state the offer in the 5 variables, make the value visible, remove friction, show proof, delivery and guarantee near the price, frame the existing price (per-unit, per-day, versus the alternative), and make every surface agree. Condition: ecomOS override; no new price point, code or gift unless the owner asks in writing. Voices: ecomOS rule; supported by S08 (offer as whole package), S10 (out-offer with the same product), S09 (presentation is as hard as structure). [0a570cacb952] [f106bb47354d] [01902b9597c7]

**R134. Ad, landing page, PDP, cart, checkout, confirmation email and support macros state the same offer, price, savings and terms, and no expired promotion is visible anywhere.** Condition: run P19 before any launch and after any change; the cards of S01 and S04 carry this as the curator's baseline. Voices: 4 (S01 card, S04 curator, S08, S07). [511c3a0c4cf9] [5a6c2fe3c283] [0a570cacb952] [9e01130cee63]

**R135. Reinforce the offer under the buy box with promises the brand can keep: free shipping if true, skip or cancel anytime if true, stock status, a delivery date, the guarantee.** An exact delivery date beats "ships within 24 hours"; both must match fulfilment data `[needs brand data: dispatch and delivery times by region]`. Condition: layout in 07-LPG; the truth check here. Voices: 2 (S09, S10). [d7f2ba51f82c] [bdf993c3765b]

**R136. Never copy another brand's claims, counts or discounts.** "Over 150,000 customers", "67% off", "safe and effective" are that brand's; each claim must be true for this brand. Condition: competitor pages are layout and mood inspiration only (ecomOS rule). Voices: 1 (S09) plus ecomOS. [b7975111e758] [d7f2ba51f82c]

**R137. Cut checkout effort as part of the offer: express wallets, guest checkout, saved details, BNPL where available, minimal fields.** Condition: `[verify UI]` `[web check: wallet and BNPL availability and fees per country]`; the S02 figure of about 20% abandonment per form field is 2008 data and stale. Voices: 4 (S10, S08, S06 header, S02). [bdf993c3765b] [4cc6038f44bf] [7bd7a76b5ba7] [7fdcaf1b88c1] [435dd5f2cbb1]

### Group P. Naming and framing the offer

**R138. Name the offer and its parts for the outcome and the buyer, using 3 to 5 of Magnet, Avatar, Goal, Interval, Container.** "Warm" words for warmth buyers, "light fashion jacket" for style buyers (S10); on marketplaces use the terms buyers search. Condition: an outcome plus a time interval implies a guarantee and may be refused by ad platforms `[web check: Meta and Google policy on outcome-plus-timeframe claims]`. Voices: 2 voices (S01+S10, S06 header). [f2d527d24cc0] [966feb3ae826] [a354c944e694] [44778b53f7ea] [b82349684f51]

**R139. Test 2 to 3 names in ads, keep the winner as control.** Nobody can predict which name wins. Condition: 24-DEP runs the ad test. Voices: 1 (S01). [f2d527d24cc0]

**R140. Build value before the price appears, with real comparisons.** Compare to a real alternative that solves the same problem (a consultation, a salon visit, replacing the item yearly), state higher-priced alternatives first, and divide by the period of use, never by an arbitrary unit. Condition: every comparison must be substantiated `[needs brand data: real alternative costs]`; S02's compounding-calculator tactic and false close are rejected. Voices: 2 (S02, S08). [51cc47d99259] [baa9c811749e] [d6f9d5596273] [4cc6038f44bf]

**R141. Match the claim to the buyer's awareness stage and carry it from ad to page.** Problem aware, solution aware, product aware get different headline claims for the same product (S08's humidifier). Condition: stage research in 02-AVT. Voices: 1 (S08). [f3e0c5293ed8]

### Group Q. Testing offers

**R142. Test structure before depth, on dedicated pages or funnels, one offer variable per cell, with equal traffic and message-matched landing pages.** Condition: 09-CRO sets sample size, duration and stopping rules; no source in this folder gives them. Voices: 4 (S07, S04, S02, S09). [82ae4d2b081b] [9e3f61688b5b] [3ab744029b93] [58e1159fc052]

**R143. Preselect the metric: contribution per visitor (profit per session) for purchase tests, gross profit after gift or discount cost, then LTV at the repeat-cycle window.** Condition: decide which costs count in "net profit" before the test and write it down. Voices: 4 (S08, S07, S02 card, S04). [1cda5c627ada] [89fd70abc2ef] [3ab744029b93] [52ef4486583d]

**R144. Isolate the offer when you need to credit it; test offers and creatives in parallel only when you want combinations.** S08's presenter says test both at once; its cards and 09-CRO say hold creative constant to attribute. Both are kept (C19). Voices: 1 (S08). [1cda5c627ada] [90e80c5c7974]

**R145. Start by testing 1 element (unit price display, variant order, a gift tier) unless a full offer overhaul is the hypothesis.** Condition: S09. Voices: 1 (S09). [58e1159fc052]

**R146. Expect losing tests and keep a backlog; do not judge a product on 1 promotion.** S02: if 1 test in 2 to 5 wins you can make a lot of money; offer testing has moved response by 10% to 900% in his experience (a claim, not a benchmark). Voices: 2 (S02, S04). [3ab744029b93] [c7ccc30477c8] [39335b89c471]

**R147. Re-test after a change in traffic source or creative; a new audience shifts AOV and conversion.** Voices: 1 (S08 card). [90e80c5c7974]

### Group R. Legal and platform guardrails (ecomOS)

**R148. Every reference price, "up to" claim, stated bonus value, countdown, stock count, pre-selected subscription, cancel-flow step, checkout add-on default and health or outcome claim carries a `[web check]` by selling country before it ships.** Condition: always; the agent lists them in the deliverable (9.1 to 9.5). Voices: ecomOS override; flagged in S01, S02, S04, S05, S07, S09, S10 caveats.

**R149. Meta and other ad platforms are read-only; offers are proposals for a human to apply.** Voices: ecomOS rule.

**R150. Currency: convert every USD threshold in this playbook before use, and note that none was tested outside USD.** Condition: Gehna prices in INR; the $100 dollar-versus-percent rule and the 250 screen do not carry over as written. Voices: S07, S09, S08 caveats. [febdce2ad8fb] [34682db50bb8] [9f02d954cf3b]

**R151. Do not read a card's ecommerce adaptation as the source's claim.** S01, S02 and S10 are services, direct-mail and framework sources; S06's header adds 9 cards the speaker never said. Where a rule above rests on a card adaptation or header only, section 12 says so, and the rule is a hypothesis to test. Voices: the mini playbooks' own caveats.

## 4. Procedures (implementation)

Procedures are numbered P1 to P25. Each has a goal, preconditions, steps with settings, checks, rollback and `[verify UI]` tags. Arithmetic steps call code (`intelligence/` calculators or a script the agent writes and runs); the model never computes in prose.

### P1. Build the offer economics baseline (waterfall) per SKU and per tier
Goal: the numbers every other procedure needs. Sources: S04 3.1, S08 3.1, S06 3.1. [0b43c974ae3c] [471fc0881800] [e311b1e255a4]
Preconditions: price list, all-in COGS, shipping and 3PL by units, fees, current target ROAS or CPA `[needs brand data]`.
1. For each SKU and each existing tier, pull price, all-in COGS per unit, shipping cost for 1, 2, 3, 4 and 6 units, fulfilment cost, payment fee rate, current gift cost.
2. Compute F1 (GM per order and GM%) and F3 (BE_ROAS, target CPA, CP_target) in code. Round costs up.
3. Pull the last 90 to 180 days: sessions, orders, CVR, order-level values, UPT, blended CAC. Compute F2 (CP_order, CP_visitor) for the current offer.
4. Pull past sale periods: dates, depth, UPT, ROAS or CPA, refund rate. Store the measured sale-period efficiency lift (R18).
5. Record the output as the "current offer" row of the options table (9.1). Any missing input makes the affected cell "unavailable" and generates a data request to 20-FIN.
Check: BE_ROAS below current target ROAS; if not, the brand is losing money at full price and no offer fixes it (route to 20-FIN before continuing).
Rollback: none; read-only.

### P2. Cost a proposed offer before proposing it
Goal: contribution per order and per visitor at the proposed structure versus the current one. Sources: S04, S06, S08, S09. [0b43c974ae3c] [52c6ca3043ae] [1cda5c627ada] [01902b9597c7]
Preconditions: P1 done; the proposal written in the 5 variables (R1).
1. Write the proposed offer: product and tiers, price per tier, discount or free units, gifts and their landed cost, shipping terms, guarantee, urgency element (if honest), who sees it (new, returning, subscribers).
2. For each tier compute CP_tier (F10) with the tier's real shipping cost and gift cost. For a discount, model UPT_new from past sales (F5). For a guarantee change, apply F8. For an upsell, F9.
3. Estimate the demand side conservatively: CVR lift and tier mix from the brand's own history or a holdout, never from a source's example. Compute CP_visitor for current and proposed (F2), and the break-even CVR lift (F6).
4. Compute allowable CAC and required ROAS (F4) and the efficiency lift needed; compare with the measured sale-period lift (P1 step 4).
5. For LTV plays compute LTGP(K) and the CAC ceiling (F11) with the brand's survival curve; state K.
6. Record 3 rows: current, proposed at conservative demand, proposed at break-even demand. Mark every assumption `[needs brand data]` where it is not measured.
Check: the proposed offer passes only if CP_visitor rises at the conservative demand case, or the brand has explicitly accepted a first-order loss with cash to fund it (R19) and a proven payback.
Rollback: none; the output is a table, not a change.

### P3. Model a flat discount before running it
Goal: know the required ROAS at the depth before anyone approves the sale. Source: S04 3.1. [0b43c974ae3c] [9fe82ea9bb52] [f8754813a6a1]
1. Take the full-price waterfall (P1).
2. Apply the discount to the unit price (25% off $100 is $75).
3. Set UPT_new from past sale periods of similar depth `[needs brand data]`; if none, use UPT_current (no lift) as the conservative case.
4. AOV_new = unit_price_d × UPT_new; COGS_new = COGS% × full unit price × UPT_new; shipping at UPT_new units.
5. GM_new, BE_ROAS_new, allowable CAC (GM_new − CP_target), required ROAS (F4).
6. Compare required ROAS to the current target and to the measured sale-period lift. S04's example: $100 AOV, $40 COGS, 6x target: 25% off with UPT 1.0 to 1.63 needs about 8.9x, roughly 50% more efficiency.
7. If the lift is not credible, pick a shallower depth or a non-discount mechanic (P5, P6, P7).
8. Hand the new target CPA and ROAS to 24-DEP in writing.
Check: COGS was applied to retail units, not to discounted AOV. Rollback: none.

### P4. Find the profit-maximising discount depth from the brand's own history
Goal: the depth where contribution per order peaks. Source: S04 3.2. [99f79f8d840d]
Preconditions: at least 3 past flat-discount periods at different depths with UPT, average unit retail and CP per order; consistent tracking.
1. Build a table: depth, UPT, average unit retail, CP per order, required ROAS at CP_target.
2. Plot CP per order against depth. Expect a dip at 5% to 10%, a rise once buyers add units, a fall past the point where margin loss outweighs UPT.
3. Headline the depth at the peak (S04's illustration: 20%); rule out any depth whose required ROAS the brand has never achieved.
4. If history is missing or messy, do not run the plot; state "unavailable" and propose a structural offer instead.
Check: the plot uses contribution per order, not revenue. Rollback: none.

### P5. Build a buy-more-save-more ladder
Goal: 3 tiers, each with a reason, a falling per-unit price, a clear saving, and contribution above target. Sources: S03 3.3, S07 3.4, S09 3.1, S08 3.3, S02 3.10. [defb3074e4c1] [61cf8d39f4bb] [01902b9597c7] [fc891407623e] [7367beea9d44]
1. Confirm fit: consumable or multi-unit product, shelf-stable, inventory for the top tier, a real reason to own more (days of supply, coverage, household size).
2. Choose quantities: 1, 2, 3 or 1, 3, 6 (S09: no one-size-fits-all). Same product, other flavours or colours allowed; no forced mixed assortment (R42).
3. Price the tiers so per_unit(n) falls with n (F7). Fund the fall from shipping and fulfilment savings first (R20), then from margin only within CP_target (F10).
4. Compute dollars_saved, pct_saved, per_unit, per_serving or per_day for each tier in code; label each tier with the larger of dollars or percent (R34) and always the per-unit figure (R48).
5. Where the mechanic is extra units at the same total price, frame it as "buy 2, get 1 free" (R35) after confirming the real percent equivalent (B2G1 = 33.3%).
6. Attach gifts that scale with units, on the tier you want to sell (R55); cost them inside F10.
7. Pre-select the middle tier; keep the single at full price as the anchor and entry (R43, R45).
8. Put the variant selector above the ladder; copy the structure to sibling products (R47).
9. Write the tier reasons ("for 1 month", "covers 1,400 sq ft", "for the family").
10. Set the new target ROAS and CPA per tier mix (R15) and hand to 24-DEP.
11. After 1 repeat cycle, read take rate by tier and retune (R50).
Check: every tier clears CP_target; the deepest tier's per-unit price is above all-in COGS plus its share of shipping and fees. `[verify UI: bundle or quantity-break app and its per-tier pricing rules]`.
Rollback: revert the widget to the previous ladder; keep the old tier prices archived with dates.

### P6. Design a gift with purchase or welcome kit
Goal: a gift that lifts take rate on the tier you want without wasting margin. Sources: S04 3.6, S05 3.3, S07 3.2, S03 3.6. [0afa90fbaa08] [503d2fb72fc1] [494b95673d4f] [d4bfd76ee183]
1. List what blocks or degrades use of the product (clumping, dosing, measuring, storage, styling) from reviews and support `[needs brand data]`.
2. Shortlist gifts that remove a block or make use feel special; exclude swag; exclude more of the same product (R53, R56).
3. Get landed cost, box fit and shipping impact per gift `[needs brand data]`; prefer items under the discount they replace (R54).
4. Decide placement: acquisition promise on the PDP (before purchase) or a targeted save; not an untargeted order-2 surprise (R58).
5. Model base versus offer tier with F10 and F13. S04's example: 1 towel CP $26.50 (BE 1.89); 2 towels plus a $4 bag CP $53.50 (BE 1.87).
6. State the gift's value only at a price it is sold at (R28, R60).
7. Show the gift on PDP, in onboarding, in the billing reminder, with a click-to-claim where the platform allows (R57) `[verify UI]`.
8. After 90 to 120 days, survey buyers on whether the gift mattered; drop it if take rate did not move (R11).
Check: gift cost is inside CP_tier; the objection it fixes is real. Rollback: remove the gift from the tier; honour gifts already promised on open subscriptions.

### P7. Set threshold offers from the order-value distribution
Goal: thresholds that move a real band of orders. Source: S04 3.7. [a1a57841df7a] [c9081fedfb43] [f0cd279bc44b]
1. Export order-level order values for 90 to 180 days `[needs brand data]`; do not use the reported mean AOV.
2. Plot the count of orders by value band in code. Identify peaks.
3. Two peaks: set 1 offer aimed just above each peak, possibly different mechanics per peak. One peak: aim to move the core group 1 step up (30-day to 90-day supply).
4. Never set a threshold between peaks or at the mean.
5. For a free-shipping threshold run F17; keep it only if moved orders' extra contribution beats the shipping given to orders already above it (R63).
6. Prefer a product, sample or gift unlock at the threshold to shipping alone (R64); cost the unlock with F10.
7. Re-plot after any price, bundle or threshold change.
Check: share of orders already above T is known and priced in. `[verify UI: cart progress bar and unlock app]`. Rollback: revert T; announce nothing publicly if the threshold was not advertised.

### P8. Score and place upsells, cross-sells and post-purchase offers
Goal: slots filled by incremental contribution, not take rate. Sources: S04 3.9 to 3.11. [52ef4486583d] [456ea796c7fe] [3ddf9722dfa2] [6856ee4fdaf4] [0fc1f8211e17]
1. For each candidate and placement get take rate, added order value and GM% of the added item `[needs brand data]`.
2. Compute F9 per candidate in code; rank.
3. In cart: 1 offer per slot, relevant to the cart, legible in 2 to 3 seconds, usually a flat discount on the added item.
4. Checkout: a low-friction add-on only (shipping protection, expedited delivery, a small warranty); never a full product; no pre-ticked box `[web check]`.
5. Post-purchase one-click: anchor at $50 to $60 (S04's example), down-sell to $20 to $30 if declined, next upsell $30 to $40 if taken `[verify UI: one-click post-purchase support]`.
6. Measure lift against a holdout by placement; track take rate and incremental CP separately.
7. Feed the measured gain into allowable CAC (R74).
Check: no more than 1 offer per cart slot; time-limited chains only with a real timer. Rollback: remove the slot content; the cart and checkout keep working without it.

### P9. Design a subscription offer and buy box
Goal: first-order subscription take rate at a modelled LTV, with a visible one-time path. Sources: S05 3.1 to 3.2, S07 3.1 to 3.3, S03 3.3, S04 3.8. [7860f83f10e6] [d8cbf6d9333d] [971d6e5bf0ce] [5ff86e2e0a6f] [2105cc48bb5d]
1. Classify the product's use: daily ritual or occasional; set the default cadence and pack from real use (R83) `[needs brand data]`.
2. Pull cohort LTV by first-order type at 90 days, 6 and 12 months; compute LTGP(K) and the CAC ceiling (F11) `[needs brand data]`.
3. Pick the model: (a) buy-more-save-more first (S03), (b) front-loaded discount with lower recurring rate (S07's 25% then 10%, or the brand's tested numbers), (c) welcome kit plus recurring discount (S07's strongest), (d) subscription only (S09's Space Goods; C6). Model each with F10 and F11.
4. Keep one-time at full price, visible but recessed (R77); do not remove it without a test (C6).
5. Lay out 3 options, 2 subscriptions (for example 90-day, 30-day, one-time), pre-select the plan you want, show price, saving, gifts and cadence on the subscription options `[verify UI: widget default selection]` `[web check: pre-selected subscription rules per country]`.
6. Gate kit, program, guarantee and best price on subscription (R82); state the gate plainly.
7. Add a longer plan or prepaid tier with more value (R84), costed.
8. Plan the gift roadmap (P6) and the results-horizon messaging (R86; execution 14-EML).
9. Set the pop-up and all site offers to the same subscription offer (R129).
10. Check the recurring rate beats any planned public sale rate (R91).
11. Test take rate and, later, retention by cohort; do not judge on take rate alone (R80).
Check: first-order margin at the net price is known; churn after order 1 for front-loaded cohorts is tracked. Rollback: restore the previous default and rates; existing subscribers keep their terms.

### P10. Model take rate and discount depth for a subscription
Goal: the discount pair (first order, recurring) that maximises modelled cohort profit. Source: S03 3.4. [9099002370eb] [73cdef4101eb]
1. Get contribution margin per order and the retention curve by month `[needs brand data]`.
2. Build scenarios in code: heavy first-order discount with small recurring (about 30% then 5%, the Armra description) versus lighter first-order with a longer tail; several depths (S03 guesses Armra tested 25% to 50%).
3. Compute LTGP(K) per scenario (F11) and CAC ceiling; pick by total profit per cohort, not by take rate.
4. Choose one-time prominence for the phase (R80).
5. Re-run when CAC moves or after each 90 days of cohort data.
Check: the model uses the brand's survival curve, not a source's LTV numbers. Rollback: none.

### P11. Plan a sale for a subscription brand
Goal: a sale that does not cannibalise subscribers. Sources: S03 3.8, S05 3.8. [35bed5b98d94] [1b7f42b5f9e3]
1. Decide: is subscriber cancel-and-rebuy acceptable? If no, the public depth must stay below the subscriber rate.
2. Design the subscriber offer first: deeper on add-ons, extra months for prepaid, a gift for trying a new product, or 30% off an add-on to the next order.
3. Set the public offer below it and add a subscription layer; compute the stacked total the way checkout applies it (F14) `[verify UI]`.
4. Exclude active subscribers from the public promo sends; send them their own offer by email, portal and add-to-next-order links `[verify UI]`.
5. Brief ads and email: the public offer points to what subscribers get.
6. Track "subscription cancelled" against each campaign (S05); stop rule: cancels above baseline (R119).
Check: R91 holds on every surface, including retargeting ads subscribers will see. Rollback: end the public offer early per the stop rule; honour subscriber offers already sent.

### P12. Set cancel-flow save offers (offer logic only)
Goal: save offers that pay back. Sources: S03 3.9, S05 3.9. [a006e3aa6f9c] [1ae7b0ed8e41] [2555be53857a]
1. Baseline the save rate `[needs brand data]`.
2. Order of build: founder or brand-voice video splash (about 1 minute), 6 or 7 reasons, matched actions, then offers.
3. Map reason to action: too expensive (value branch: education; budget branch: discount on this order), too much product (delay, skip 1, change frequency), wrong product or taste (swap), taking a break (change next date).
4. Cost each discount step with F18; raise from 20% to 30% only if saved LTGP covers it; flat currency offers only above about $100 basket.
5. Segment by month in subscription, product or basket where the platform allows `[verify UI]`.
6. Monthly: retire the 1 or 2 least-picked reasons, add specific ones; send each reason pattern to its upstream owner.
7. Keep cancel completable in the same number of steps as sign-up or fewer (R96) `[web check: click-to-cancel rules per country]`.
Check: save rate against S05's bands (under 10% rework, 15% good, 20% very good) as context, not a target. Rollback: revert to the previous flow; never remove the cancel button.

### P13. Win-back offers
Goal: reactivation without teaching customers to cancel for a deal. Sources: S03 3.10, S05 3.9. [42ece6bd5274] [552ee801d868]
1. Cancel confirmation: amicable, door open, education; no big offer.
2. Immediately after cancel: 1 or 2 short emails by reason with the standard offer and a "reactivate" link (14-EML builds them).
3. 30 to 60 days after cancel (S05) or on a 1 to 2 week rotation to all cancelled subscribers (S03): a bigger first-order-back offer (30%, 40% or 50%) stepping down to the standard rate; product-relationship offers (A plus B at 50%; free B for 3 months with 3 months of A).
4. Judge on click rate and reactivation rate; bigger groups give clearer reads than 7 reason-splits.
5. Cost the win-back discount with F11 on reactivated cohorts.
Check: the win-back rate is never visible to active subscribers. Rollback: pause the flow.

### P14. Design and cost a guarantee
Goal: a guarantee that raises net contribution. Sources: S01 3.7, S02 3.11, S10 3.3, S04 3.6. [eaf3e7847805] [729e71de2194] [d51c9104d84e] [4d72bb91baae]
1. Name the buyer's biggest fear from reviews and support (fit, durability, taste, results, damage in transit) `[needs brand data]`.
2. Write the promise as "If not X within Y, we will Z" (R102).
3. Decide length, conditionality, coverage and activation (R103). Default 30 days; test 60 or 90 where the returns-cost model allows; unconditional wording unless hygiene, customisation or safety needs a stated condition.
4. Decide the second layer if any: try-before-you-buy with delayed capture, keep-the-bonus refund, outsized refund, a tier-specific durability guarantee (R104) `[web check: delayed-capture support and rules]`.
5. Pull refund rate, return cost per order, resale value `[needs brand data]`; run F8 for current versus proposed on net contribution with a conservative order lift (S01's 30% lift is an anecdote).
6. Put the short version near the price and at checkout; link the full policy (R105).
7. Name it for clarity and brand fit (R107).
8. Flag statutory return rights by country `[web check]`; the guarantee adds to them, never replaces them.
Check: worst-case combined cost of stacked layers is modelled. Rollback: shorten or narrow the guarantee for new orders only; honour the terms shown at purchase.

### P15. Use scarcity or urgency honestly
Goal: real limits, enforced. Sources: S01 3.4 to 3.5, S02 3.13, S10 3.2, S07 3.5. [b83b87f23486] [4fc1b785cdaa] [ea94a39e0ec6] [275612802571] [bb89fca1e69e]
1. Pick the lever: a limited release (fixed run by flavour, colour, design or size), a dated promotion or bonus window, real stock per variant, a capacity limit with a true reason.
2. Verify the limit from inventory or production data `[needs brand data]`; write the true reason.
3. Set the date and time with time zone; write the post-deadline state (price returns to X, bonus ends, drop closes).
4. Sync counts and dates across store, ads, email and support.
5. Enforce: close on time, never extend, sell out and say so, restock only as a new announced drop.
6. `[web check: false-urgency and scarcity rules per country]` before launch.
Check: no timer resets, no evergreen "only 3 left", no "high demand" reservation timers without a real hold. Rollback: remove the element; if a deadline was stated it is not extended.

### P16. Plan a promotion with stop rules
Goal: a sale that clears cannibalisation and protects price integrity. Sources: S04 3.3, S03 3.8, S05 3.8, S01 3.5. [2b9021591176] [35bed5b98d94] [1b7f42b5f9e3] [676632fcde7f]
1. Purpose check: turning stuck stock into cash or a planned seasonal wrapper is valid; rescuing a revenue number is not (R32).
2. Frequency check: flat sitewide sales this year so far; S04's guardrail is 1 to 2 a year.
3. Depth: run P3 and P4; pick the depth whose required ROAS the brand has hit before.
4. Cannibalisation (R118): estimate full-price revenue displaced, subscriber leakage (P11), pull-forward, refund rate in past sales; compute incremental contribution in code.
5. Audience: new versus returning versus subscribers get different offers (R40, R92).
6. Wrapper: real dates, a real reason, a name (P23); the promotion expires, not the product (R113).
7. Stop rules (R119): required ROAS or CPA missed for N days; discount share of revenue above cap; subscriber cancels above baseline; refund rate above baseline; stock below the stated limit. Write the numbers.
8. Post-sale: measure price integrity for 30 days after (full-price share, repeat buyers who wait).
Check: every stop rule has a number and an owner. Rollback: end early per stop rules; honour orders placed.

### P17. Run a first-order pop-up offer test
Goal: the pop-up offer with the best gross profit and 90-day LTV. Sources: S07 3.6, S06 3.4. [db90a9c32f90] [42cf8bc4ce3a] [1f0ee6e31e5c]
1. Confirm the brand discounts at all; fixed-offer brands run P19 instead and test a non-discount hook (early access, a guide, the fixed offer itself).
2. Shortlist structurally different variants: currency off, percent off, free gift, credit, mystery framing of one of them; size currency versus percent by the AOV rule in the brand's currency (R34).
3. Equal traffic per variant; only the pop-up offer changes `[verify UI: split-test settings in the pop-up tool]`.
4. Read per variant: opt-ins, placed-order rate, revenue, gross profit after gift or discount cost; then 90-day LTV of each variant's buyers.
5. Cut to the leaders and keep running until 09-CRO's stopping rule is met.
6. Model the full chain with F16.
7. Roll the winner into the pop-up and the welcome flow (14-EML).
Check: the winner leads on gross profit and holds on LTV, not on opt-ins. Rollback: restore the incumbent.

### P18. Stack the site's existing offer into the first-order headline
Goal: 1 true combined number, no conflicting offers. Source: S07 3.7. [9e01130cee63]
1. List every live discount: sitewide, subscription saving, bundle saving, welcome code, evergreen promo.
2. Convert each to a currency value at the product's price or AOV in code.
3. Confirm which combine at checkout and whether they add or compound (F14) `[verify UI]`.
4. Advertise the total as 1 currency figure, or "up to $X" only if a further layer really stacks `[web check: "up to" claims]`.
5. Remove any offer that conflicts between site and pop-up.
6. Recheck first-order margin at the full stacked discount (F10).
Check: the advertised number equals what checkout gives. Rollback: revert the headline to the single true offer.

### P19. Fixed-offer presentation audit and fix list
Goal: raise conversion on a fixed offer without touching price. Sources: ecomOS override; S08, S10, S09, S01 card, S04 curator. [0a570cacb952] [f106bb47354d] [01902b9597c7] [511c3a0c4cf9] [d7f2ba51f82c]
1. Write the fixed offer in the 5 variables; note which are empty (positioning, value mechanic, risk reversal, honest urgency).
2. Crawl every surface: ad, landing page, PDP, cart, checkout, confirmation email, pop-up, support macros. Record the price, savings, terms, delivery promise and guarantee each one shows.
3. Mark every mismatch and every expired or conflicting promotion.
4. Value equation pass (P20): dream outcome named per avatar; proof (reviews, demo, unboxing); time (delivery date, ship-by); effort (wallets, guest checkout, how-to content).
5. Framing pass: per-unit or per-day price next to the total; the larger of dollars or percent where a saving exists; tier reasons; no mental math.
6. Buy-box pass: guarantee, delivery date, stock status and true promises under the price; variant before quantity.
7. Bonus pass: zero-cost how-to content presented as part of the offer.
8. Produce the fix list (9.2) ranked by cheapest, highest-leverage first; each fix names the surface, the current text, the proposed text, and the evidence needed.
Check: no fix changes price, adds a discount or code, or invents a claim. Rollback: each fix is reversible copy or layout.

### P20. Value equation audit of a product offer
Goal: find the weakest driver and fix it first. Sources: S01 5.3, S10 3.1, S08 3.4. [0e0a8b7a8e72] [bdf993c3765b] [4cc6038f44bf]
1. Pick 1 product and 1 avatar; write the dream outcome as the end state.
2. Likelihood: count readable reviews; check for a demo of the outcome in use and unboxing content `[needs brand data]`.
3. Time: record order-to-delivery by region and production lead time; check for a stated delivery date.
4. Effort: walk mobile checkout; note forced account creation, missing wallets, missing how-to content.
5. Score each driver 0 or 1 against the strongest competitor selling a similar product (S10's checklist in 5.9).
6. Fix the cheapest gaps first; add proof and a guarantee before making a bigger claim.
Check: no claim added without evidence. Rollback: copy and layout only.

### P21. Refresh a fatigued offer
Goal: restore response with the least operational change. Source: S01 3.9. [b261bc411259] [1874fa3ba153]
1. Confirm fatigue with reach and frequency data, not time running `[needs brand data]`.
2. Change in order: creative; body copy; headline or wrapper; duration; enhancer (bonus or discount component); monetisation and price. Stop at the first step that restores response.
3. Do not change a monetised, working offer out of boredom.
Check: each change is dated and tested against the control. Rollback: revert the last step.

### P22. Reposition a hero SKU into several offers
Goal: more offers from 1 SKU with nil or positive margin impact. Source: S04 3.4. [ec3b35527187]
1. List personas, problems and mechanisms the SKU serves.
2. Test them as ad angles (24-DEP); find the winners `[needs brand data: angle performance]`.
3. Build a dedicated page and offer per winning angle: title and positioning change, SKU does not.
4. Add partner value that costs nothing only with a compliance check `[web check: category and referral rules]`.
5. Use a supported result timeline as offer structure (for example a free extra 30 days inside the second 90-day order) only with evidence `[needs brand data]`.
Check: no health or outcome claim without substantiation. Rollback: unpublish the angle page.

### P23. Name the offer
Goal: a name that says who it is for and what it does. Sources: S01 3.8, S10 3.5. [f2d527d24cc0] [44778b53f7ea] [966feb3ae826]
1. Draft 3 to 5 names using 3 to 5 of Magnet, Avatar, Goal, Interval, Container; add the outcome word buyers search for.
2. Drop any name that states a quantified outcome with a timeframe unless the platform allows it `[web check]`.
3. Name the bundle components with the same formula; put a benefit in each title.
4. Run the best 2 to 3 in ads (24-DEP); keep the winner as control.
Check: no invented claims in names. Rollback: revert the name; keep the winner log.

### P24. Run and read an offer test
Goal: a clean read on contribution per visitor and LTV. Sources: S07 3.6, S08 3.2, S02 3.17, S09 2.14, S04 3.13. [89fd70abc2ef] [1cda5c627ada] [3ab744029b93] [58e1159fc052] [9e3f61688b5b]
1. Write the hypothesis and the single variable (structure first, depth later).
2. Preselect the metric: CP_visitor for purchase tests, gross profit after gift or discount cost, LTV at the repeat-cycle window; write which costs count.
3. Hand sample size, duration and stopping rule to 09-CRO.
4. Equal traffic per cell; message-matched landing page per cell; hold creative constant unless the test is about combinations (R144).
5. Read: CVR, AOV, UPT, CP per order, CP per visitor, refund rate, then the LTV window.
6. Log the result in the experiment record (9.5) with the offer written in the 5 variables.
7. Re-test after a traffic or creative change.
Check: no winner declared on opt-ins, revenue or AOV alone. Rollback: restore the control.

### P25. Build a stacked evergreen offer (trim and stack)
Goal: a category-of-one bundle that lowers required efficiency. Sources: S04 3.8, S01 3.3, S09 3.1. [2105cc48bb5d] [e141a5bda4f3] [de5a81dc7f90] [01902b9597c7]
1. Start from the product's natural larger pack (90-day supply, family pack) and a moderate headline discount at most at the P4 peak.
2. List the buyer's problems before, during and after use (S01 step 2); turn each into a component: a tool, a how-to asset, a sample, a program with a stated length.
3. Trim: estimate cost to the brand for each component; remove high-cost low-value first, then low-cost low-value; keep low-cost high-value and high-cost high-value.
4. Add the subscription unlock gated on the tick (R82) and a lifetime rate only if the churn model supports it.
5. Cost the stack with F10 and F4; S04's example moved required ROAS from 6x to about 2.9x at the same contribution, including a $19 shipping saving on 3 units.
6. Name the stack and each component (P23); state each component's value only at a real price (R28).
7. Run 90 to 120 days, survey, remove unvalued parts (R121).
Check: the stack is legible in the buy box (R11); the deepest tier clears CP_target. Rollback: revert to the ladder without the stack.

## 5. Diagnostic checklists

Written so a worker can run each one alone. "Source" gives the mini playbook and card.

### 5.1 Offer economics check (run before any offer is proposed)

| What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| All-in COGS per SKU exists | Ask for product, inbound freight, packaging, duties per unit | A number per SKU with a date | Product cost only, or a single blended % | Request from 20-FIN; output "unavailable" until then | S04 [8074b0c6c718], S08 [471fc0881800] |
| Shipping cost by units per order | Ask 3PL or carrier table for 1 to 6 units | Cost per units-in-box | One flat per-unit figure | Get the table; bundles depend on it | S04 [6a0ef806927d], S08 [471fc0881800] |
| Gross margin per order and GM% (F1) | Compute in code for current offer and each tier | GM% known per tier | GM computed on discounted AOV with COGS % | Recompute with COGS on retail units | S04 [0b43c974ae3c] |
| Break-even ROAS below current target ROAS (F3) | Compare | BE_ROAS < target | BE_ROAS ≥ target | Stop; the brand loses at full price; route to 20-FIN | S04 [9fe82ea9bb52] |
| Contribution per order and per visitor, current vs proposed (F2) | Compute at conservative demand | CP_visitor rises | CP_visitor falls, or only revenue or ROAS rises | Reject or restructure | S06 [52c6ca3043ae], S08 [1cda5c627ada] |
| UPT lift assumption comes from history | Check the source of UPT_new | Past sale periods or a holdout | Assumed or copied from a source example | Use UPT_current as the conservative case | S04 [0b43c974ae3c] |
| Required ROAS at the offer vs measured sale lift (F4) | Compare | Within the brand's achieved range | Needs a lift the brand has never hit | Shallower depth or non-discount mechanic | S04 [f8754813a6a1] |
| Every tier clears CP_target (F10) | Compute per tier including gifts and freight | All tiers pass | Deepest tier fails | Cut savings or gifts on that tier | S09 [01902b9597c7], S02 [abb86777aeb2] |
| Gift cost inside the tier margin | Check gift landed cost and box fit | Inside F10 | Left out ("it's only $3") | Include it | S04 [2105cc48bb5d], S06 [eaf22ff0c7f6] |
| Guarantee cost modelled (F8) | Refund rate × cost per refund | Known and included | Not modelled | Run P14 | S01 [4d72bb91baae], S02 [729e71de2194] |
| LTV window and survival curve are the brand's (F11) | Check inputs | Cohort data at 90 days and 6 months | A source's $195, $226 or $289 used | Replace with brand cohorts or mark unavailable | S05 [d99fcf6edcf0], S07 [02a3e80a55a4], S06 [5ea541b8c8d2] |
| Cash can carry any first-order loss | Ask months of runway and payback | Runway > payback | Loss funded by hope | Bundle-first plan | S06 [0e9661473b27] |
| Stacked discount computed the way checkout applies it (F14) | Check platform behaviour `[verify UI]` | Advertised = checkout | "Up to 40%" that is 36% | Fix the number | S03 [35bed5b98d94], S07 [9e01130cee63] |
| Currency converted | Check thresholds used | Brand currency | $100 rule or 250 screen used raw | Convert | S07 [febdce2ad8fb], S09 [34682db50bb8] |
| Arithmetic done in code | Check the calc log | Script or calculator output attached | Numbers typed in prose | Re-run in code | ecomOS rule |

### 5.2 Offer presentation audit across ad, page and checkout (fixed-offer brands run this first)

| What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Same offer on every surface | Screenshot ad, landing page, PDP, cart, checkout, confirmation email, pop-up, support macros | Identical price, saving, terms | Any mismatch or an expired promo | Fix every surface; remove expired promos | S01 [511c3a0c4cf9], S04 [5a6c2fe3c283], S07 [9e01130cee63] |
| Offer written in 5 variables | Fill positioning, price architecture, value mechanic, risk reversal, urgency | 3 or more filled honestly | Only "X% off" or only a price | Add value mechanic, risk reversal, proof | S04 [a3756b7bf5f1] |
| Ad promise matches page headline | Side by side | Same desire, proof, delivery, guarantee | Different promise or stage | Align | S08 [0a570cacb952] [f3e0c5293ed8] |
| Dream outcome named per avatar | Read PDP title and headline | Outcome and who it is for | Category name only | Rename (P23) | S10 [44778b53f7ea] |
| Proof present | Count reviews; look for demo and unboxing video | Readable reviews plus a demo of use | No demonstration | Add demo content | S10 [bdf993c3765b] |
| Delivery promise | Compare to fulfilment data | Exact date or ship-by that is met | "2 weeks" or none, or a promise not met | State a true date | S09 [d7f2ba51f82c], S10 |
| Guarantee visible near price and at checkout | Look | Short version near add-to-cart | Footnote or policy page only | Move it up | S02 [7e4c3385639c], S09 |
| Per-unit or per-day price next to total | Read each tier | Both shown | Total only, or per-day instead of total | Add per-unit; keep total | S09 [4dc9316eaaf5], S08 [5f2ab9d96cc7] |
| Saving shown as the larger number | Compute both | Larger shown | Smaller shown | Swap | S08 [9f02d954cf3b], S07 [febdce2ad8fb] |
| No mental math | Read tier labels | Dollars saved, per-kit cost | "67% off the 3rd unit" | Rewrite | S08 [5f2ab9d96cc7] |
| Tier reasons stated | Read tiers | Size, room, family, days | "Save more" only | Add reasons | S08 [fc891407623e] |
| Variant before quantity | Load PDP | Variant selector above ladder | Reversed or mixed | Reorder (07-LPG) | S09 [01902b9597c7] |
| Middle tier pre-selected, single at full price | Load PDP | Yes | Largest default, or single discounted | Re-default | S07 [61cf8d39f4bb], S05 [d8cbf6d9333d] |
| Pop-up offer equals the site offer | Open as new visitor | Same offer, one combined number | 10% one-time only, undercutting subscription | Align (P18) | S05 [7860f83f10e6], S07 [9e01130cee63] |
| Checkout effort | Walk mobile checkout | Wallets, guest checkout, few fields | Forced profile, many fields | Fix (07-LPG) | S10 [bdf993c3765b], S02 [7fdcaf1b88c1] |
| Claims are the brand's own | Check every count, %, "safe" claim | Substantiated | Copied from a competitor | Remove | S09 [b7975111e758] |
| Urgency and scarcity real | Check timers, stock counts, "claimed" bars | Real, enforced, dated | Resetting timer, evergreen "3 left", "high demand" hold | Remove | S01 [4fc1b785cdaa], S07 [bb89fca1e69e], S09 [3817d0f2245c] |
| Reference prices and stated values real | Check "was" prices and bonus values | Real recent prices | Inflated anchors | Remove `[web check]` | S07 [bbc8899c72f2], S02 [769c1d67e28c] |
| No new discount introduced (fixed-offer brand) | Diff the fix list against price and codes | Presentation only | A new code or price | Remove | ecomOS override |

### 5.3 Subscription design review

| What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Product suits subscription | Use frequency, repeat rate | Daily ritual or steady replenishment | Occasional use forced onto 30 days | Cadence by use, or no subscription | S05 [9d7f6e7eec35] [167cf8e69e33] |
| Reason to subscribe today | Read the buy box | Front-loaded value, kit, gated perks or bulk tiers | Flat 10% to 15% only | P9 | S03 [75c76ec85c29], S07 [971d6e5bf0ce] |
| Subscription pre-selected, 3 options, 2 subscriptions | Load PDP | Yes, with price, cadence and cancel terms next to it | One-time default, 2 options | Re-lay out `[verify UI]` `[web check]` | S05 [d8cbf6d9333d] |
| One-time path visible | Load PDP | Present, full price, recessed | Removed without a test | Restore and test (C6) | S05 [7860f83f10e6], S09 [58e1159fc052] |
| First-order margin at net price known | F10 with kit and gifts | Known | Not modelled | P10 | S07 [5ff86e2e0a6f] |
| LTGP and CAC ceiling from brand cohorts | F11 | Cohort survival curve used | Source numbers used | Replace | S06 [5ea541b8c8d2] |
| Recurring rate beats any public sale | Compare planned sales | Subscriber rate deeper | Sitewide equals or beats it | P11 | S03 [35bed5b98d94] |
| Take rate not pushed past margin support | CAC trend vs take rate | CAC stable | CAC rising as take rate rises | Test OTP, GWP, quiz | S03 [9099002370eb] |
| Gifts help use, told at every step | Read PDP, onboarding, reminders | Visible, useful, claim link | Hidden surprise swag | P6 | S03 [d4bfd76ee183], S05 [503d2fb72fc1] |
| Cadence and pack match use | Cancel reasons "too much product" | Low | High | Change defaults | S05 [167cf8e69e33] |
| Frequency change easy; no open-ended pause; skip and delay capped | Portal walk-through | Yes | Pause forever, hidden frequency | Fix (17-CXP) | S03 [34907451e7ef] |
| Results horizon stated, no early promise | Read onboarding copy | 90 to 120 days where evidence supports | Results promised in days | Rewrite (14-EML) | S05 [2762401ae2f2] |
| Cancel flow: video, reasons, matched saves, costed discounts | Walk the flow | Yes, costed with F18 | Generic screen or trap | P12 | S03 [a006e3aa6f9c], S05 [1ae7b0ed8e41] |
| Cancel findable and completable | Count steps | Same as sign-up or fewer | Buried, extra steps | Fix `[web check]` | ecomOS, S05 caveat |
| Billing reminders sent; subscribers out of public promos | Check flows and segments | Yes | No reminders, in all promos | Fix (14-EML) | S05 [32e1b81135d0] [1b7f42b5f9e3] |
| Win-back rates not visible to active subscribers | Check audiences | Separate | Leaks | Fix | S05 [552ee801d868] |
| Failed-payment recovery measured | Ask for failed and recovered revenue | Known | Unknown | 17-CXP | S03 [9644aea14d42] |

### 5.4 Promotion plan review

| What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Purpose | Ask why | Stock to cash, seasonal wrapper, tested offer | Rescue a revenue number | Decline (R32) | S04 [2b9021591176] |
| Frequency this year | Count flat sales | Within the brand's guardrail (S04: 1 to 2) | Monthly or weekly | Replace with evergreen stack | S04 [8074b0c6c718] |
| Depth modelled (P3, P4) | Required ROAS vs achieved | Achievable | Needs an unprecedented lift | Shallower or structural | S04 [99f79f8d840d] |
| Cannibalisation computed (R118) | Displaced full-price revenue, pull-forward, subscriber leakage, refunds | Incremental contribution > 0 | Not computed | Compute | S04, S03, S05 |
| Subscriber offer built first | Compare rates | Subscriber offer deeper | Sitewide equals or beats | P11 | S03 [35bed5b98d94] |
| Subscribers excluded from public sends | Check segments | Yes | No | Fix | S05 [1b7f42b5f9e3] |
| New vs returning offers differ | Read the plan | Different | Same | Split | S04 [8290896c9a20] |
| Dates and reason real; expires the promo not the product | Read copy | Real dates, true reason | Fake countdown, evergreen "ends soon" | P15 | S01 [676632fcde7f] [4fc1b785cdaa] |
| Stacked totals correct (F14) | Check checkout | Advertised = checkout | Wrong | Fix | S07 [9e01130cee63] |
| Stop rules with numbers and owners | Read the plan | N days, caps, baselines written | "We'll watch it" | Write them | R119 |
| Targets handed to paid team | Check the brief | New CPA and ROAS per offer | Old targets | Send | S08 [471fc0881800] |
| Price-integrity measurement after | Plan a 30-day read | Full-price share tracked | Not planned | Add | S04 [0c2ae5495d35] |
| Legal flags listed | Read the plan | `[web check]` per country | None | Add | R148 |

### 5.5 Pop-up offer review

| What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Pop-up has an offer | Open as new visitor | An offer | "Join our community" | Add (or a non-discount hook for fixed-offer brands) | S06 [42cf8bc4ce3a] |
| Offer type on the shortlist | Compare | Currency off, percent off, free gift, credit | Giveaway, free guide (DTC), bare 10% | Replace and test | S07 [1f0ee6e31e5c] |
| Framing fits AOV in brand currency | Convert AOV | Currency off above about $100 equivalent, percent below | Reverse | Test the other framing | S07 [febdce2ad8fb], S02 [582638c44d2e] |
| Pop-up equals the site offer | Compare | One combined true number | Undercuts subscription; conflicting codes | P18 | S05 [7860f83f10e6], S07 [9e01130cee63] |
| Mystery reveal delivers | Opt in and read message 1 | Clear, worthwhile value | Small or vague | Raise value or drop framing | S07 [e54276a5821f] |
| Credit is real and redeemable | Check the mechanism | Real balance, breakage known | A code called "credit" | Name it correctly | S07 [db90a9c32f90] |
| Test read on placed-order rate, gross profit, 90-day LTV | Read results | Winner on profit and LTV | Winner on opt-ins | Wait for data | S07 [89fd70abc2ef] |
| Full chain modelled (F16) | Check inputs | Opt-in, revenue per subscriber, discount cost, ESP cost | Opt-in only | Model | S06 [42cf8bc4ce3a] |
| Discount code cost tracked | Redemptions × discount | Known | Unknown | Track | S06 |
| Timing and reveal format `[verify UI]` | Check tool | Set | Unknown | 07-LPG and tool docs | S06 [63e5c2109fe1] |

### 5.6 Bundle ladder check

| What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Per-unit price falls each tier (F7) | Compute | Falls | Flat at the top (S03's $40, $40) | Reprice top tier or drop it | S03 [defb3074e4c1], S07 [61cf8d39f4bb] |
| Same product or related-use add-ons | Read contents | Same SKU or variants; related gear | Forced mixed assortment | Rebuild | S07 [a4348a9802d1] |
| Middle tier default; single full price | Load PDP | Yes | No | Fix | S07, S02, S05 |
| Tier reasons | Read | Present | Absent | Add | S08 [fc891407623e] |
| Free framing equivalence | Compute | B2G1 = 33.3% off 3 | "60% off" claimed | Correct | S08 [ae0a3d67b0b3] |
| Gifts scale with units, on the target tier | Read | Yes | Same gift on every tier | Restructure | S09 [e339ff439cf1] |
| Every tier clears CP_target | F10 | Yes | Top tier fails | Cut savings or gifts | S09 [01902b9597c7] |
| Take rate by tier read after 1 cycle | Data | Mid and top tiers taken | Most on tier 1 | Retune | S09 [58e1159fc052] |
| Returns by tier (fit categories) | Data | Stable | Larger default raises returns | Change default | S07 card [61cf8d39f4bb] |

### 5.7 Guarantee review

| What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Written as "If not X in Y, we will Z" | Read | Yes | "Satisfaction guaranteed" | Rewrite | S01 [eaf3e7847805] |
| Length, conditions, coverage, activation stated | Read | All 4 | Vague "full refund", clock from order date | Fix | S02 [729e71de2194] |
| Net contribution modelled (F8) | Compute | Yes | Only order lift assumed | Model | S01 [264e18c4c7be] |
| Returns cost and resale known | Data | Yes | Unknown | Get data | S02 [322b4dd8abd3] |
| Second layer removes a different risk | Compare layers | Yes, worst case modelled | Duplicate layers | Trim | S01 [5450fc48fb31] |
| Visible near price and checkout | Look | Yes | Footnote | Move | S02 [7e4c3385639c] |
| Statutory rights flagged | `[web check]` | Listed per country | Missing | Add | R148 |
| "All sales final" only with a true reason | Read | True reason, non-returnable value | Invented reason | Remove | S01 [9413eb3d3ddf] |

### 5.8 Scarcity and urgency honesty check

| What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Limit is real | Inventory or production data | Matches | No cap | Remove claim | S01 [e456aab8c58a] |
| Deadline real and enforced | Past promos | Closed on time, not extended | Extended, timer resets | Remove or enforce | S02 [ea94a39e0ec6] |
| Stock counts live per variant | Compare to system | Live | Static "3 left" | Connect or remove | S10 [275612802571] |
| "X% claimed" bar tied to real data | Check source | Real | Decorative | Remove | S07 [bb89fca1e69e] |
| Reservation timer holds stock | Check cart logic | Real hold | Copy only | Remove | S09 [3817d0f2245c] |
| Post-deadline state shown | Read copy | Price after, bonus ends | None | Add | S02 card [c5deb26d06e5] |
| Drop cadence | Calendar | About monthly at most | Weekly "limited" | Slow down | S01 [47afc4b21d24] |
| Legal check done | `[web check]` | Per country | None | Add | R148 |

### 5.9 Same-product competitor offer check (from S10)

| Check | Good | Bad (S10's weak profile) | Next step |
|---|---|---|---|
| Dream outcome stated | Outcome for a named avatar | Category only | P23 |
| Proof of outcome | Reviews plus a demo of use | No demonstration | P20 |
| Delivery speed | Short, stated window | 2 weeks | Shorten; state a date |
| Checkout effort | Saved details, wallets, guest | Forced profile | Remove friction |
| Guarantee | Money-back plus a second layer | None | P14 |
| Scarcity and urgency | Real and shown | None, so buyers defer | P15 |
| Bonuses | How-to per use | Nothing beyond the product | R59 |
| Name | Outcome word | "Jacket" | P23 |
Source: S10 [f106bb47354d]. Fix the cheapest, highest-leverage gaps first (card addition).

## 6. Thresholds and benchmarks

All values are the sources' examples or heuristics, in the source's currency. Confidence: "1 voice" means 1 independent presenter; S01 and S10 share an author; S05 and S07 share an agency; S06 and S07 are never counted as 2.

| Value | Condition | Source | Confidence |
|---|---|---|---|
| Break-even ROAS = 1 / GM% | GM after all variable costs | S04 | 1 voice, formula (no dispute) |
| Required ROAS about 8.9x at 25% off from a 6x target (UPT 1.0 to 1.63) | S04's illustration; ratio not benchmark | S04 | 1 voice |
| Efficiency lift in sales: 70% to 80% (rare discounters), about 5% (known discounters) | Modelled client experience | S04 | 1 voice |
| Token discounts 5% to 10% lose contribution | No UPT lift at that depth | S04 | 1 voice; contested by S06 and S07 welcome offers (C4) |
| Profit-maximising depth 20%; past 30% to 40% not worth it | S04's illustrated brand | S04 | 1 voice |
| Flat sitewide discounts 1 to 2 times a year | Protect price integrity | S04 | 1 voice; S01 and S07 agree in direction |
| Dollar off above about $100 AOV; percent off below | USD; rule of 100 | S07, S06 header, S02 ("$50 off" ~3x "15% off"), S08 (larger number) | 3 voices in direction (S05+S07, S02, S08) |
| "Free" beats an equal percent | Same total price | S07, S08, S02 | 3 voices; no numbers |
| B2G1 = 33.3% off; B2G2 = 50% off | Arithmetic | S08 (corrected) | Fact |
| 3 tiers, middle pre-selected | Ladders and buy boxes | S07, S09, S02, S05, S06 header | 4 voices |
| Ladder example: $50, $45 subscribed, $80 for 2, $120 for 3 | Protein, S03 | S03 | 1 voice, example |
| True Classic: $35, $23 per item (3), $20 per item (6), $120 | Apparel example | S07 | 1 voice, example |
| Shipping 1 unit $12, 2 units $14, 3 units $17 | S04 example; 3-pack saves $19 | S04 | 1 voice, example |
| Shipping $5 flat for 1 to 4 units ($1.25 a unit at 4) | Light skincare example | S08 | 1 voice, example |
| $14 single item cannot carry a $14 to $25 CAC; 4-pack about $50 (11% off) fixes it | Low-AOV hero SKU | S06 | 1 voice, scenario |
| AOV × CVR (no % sign) > 250 | Presenter heuristic; no margin term; currency-bound | S09 | 1 voice |
| Mystery gift $0 to $3 | Samples, partner samples, PO items | S04 | 1 voice |
| Gift roadmap at months 2, 4, 6 | "Highest churn months" | S05 | 1 voice; S03 warns untargeted gifts rarely pay back |
| Untargeted order-2 gift maths: 900 × $2 to $5 = $1,800 to $4,500 vs 45 extra orders at 5% lift | S03's tests | S03 | 1 voice |
| Kit values shown: $89 or $100 (IM8), $43 and $72 (AG1), $20 + $65 + $10 + $20 (Everyday Dose) | Page snapshots | S05, S07 | 1 voice (same agency), examples `[web check]` |
| In-cart take rate 5% to 15%; post-purchase 35% to 40%; shipping protection $4.99 at about 30% take | S04's experience | S04 | 1 voice |
| Post-purchase anchor $50 to $60, down-sell $20 to $30; take rates about 25% then 10%; RPV 10% to 15% of AOV | S04's method | S04 | 1 voice |
| Upsell value = take × added value × GM%; example $2.50 | Formula | S04 | 1 voice, formula |
| Threshold near the mean moves about 10% of buyers | S04 illustration | S04 | 1 voice |
| Subscriber vs one-time LTV: $195 vs $130 (6 months, +50%; 2x at 12, 3x at 24); $226 vs $138; $289 vs $165 | Single dashboards; selection bias | S05, S07, S06 | 2 voices (S05+S07, S06); single-client each |
| One-time buyers who later subscribe: about 10% | Claim | S07 | 1 voice, no data |
| Front-loaded subscription: 25% then 10% (S07 pick); 30% then 5% (Armra); 25% to 30% then 5% to 10% (S06 header) | Consumables | S07, S03 host, S06 header | 2 voices (S05+S07, S06 header); S03 dislikes upfront discounts (C5) |
| Basic recurring discount 10% to 20% (weakest model) | Subscription | S07, S06 ("10% not enough") | 2 voices |
| Subscription first-order discount examples: 30% on 90-day (IM8), 55% (Everyday Dose), €40 (H1), 34% (Symbiotica), 40% to 50% (Rise), 67% (Space Goods) | Page snapshots | S05, S06, S07, S09 | Examples only `[web check]` |
| Take rate pushed to 80% to 90% raises CAC | Forcing subscription | S03 | 1 voice |
| Front-loaded LTV: about 80% of needed LTV on order 1 for some brands | S03 | S03 | 1 voice |
| Subscriber cap = new per month / churn; 2,000 at 10% = 20,000 | Formula | S03 | 1 voice, formula |
| Start offer testing at about $1M a year | Subscription brands | S03 | 1 voice |
| Offer test cadence for win-back: new offer every 1 to 2 weeks; win-back flow at 30 to 60 days after cancel | S03; S05 | S03, S05 | 2 voices, different designs (C16) |
| Win-back offer 30%, 40% or 50% first order back, then 15% | S05 | S05 | 1 voice |
| Cancel-flow save: 20% to 30% on this order; 40% to 50% for a genuine budget change; flat currency only above about $100 basket | S03 | S03 | 1 voice |
| Save rate bands: under 10% rework, 15% good, 20% very good; founder video 5% to 6% to about 15% | S05 bands; S03 client observation | S05, S03 | 2 voices |
| Billing reminder rewrite: cancel rate 8.6% to 5.8% | 1 A/B test | S05 | 1 voice |
| Skip 1; delay 2 to 4 weeks (30 days), longer for large packs; no open-ended pause; pause reactivation about 10% | S03 host | S03 | 1 voice |
| Frequency adjusters (3 changes) about 200% higher LTV | 1 old study; correlation | S03 | 1 voice |
| Dunning leakage 5% to 10% of subscription revenue | A few million a year | S03 | 1 voice, estimate |
| Results horizon 90 to 120 days; "3-month game" | Slow-acting products | S05, S03 | 2 voices |
| Sitewide 20% vs subscriber 20% = no subscriber benefit; 40% sitewide with 50% subscriber add-ons | S03 | S03 | 1 voice |
| Stacked 20% + 20% = 36% compounded | F14 | S03 (corrected) | Fact |
| Guarantee length: 30 days common; 60 or 90 preferred (S02); 60-day trial +10% vs 30, 90 no better | Direct mail and software | S02; S09 shows 60 days; S07 shows 90 days | 3 voices show 60 to 90 in use |
| "Free use" beat "free trial" by 15% | Software trial wording | S02 | 1 voice |
| Keep-the-product refund +21% conversion | Digital goods only | S02 | 1 voice |
| Double money back tripled attendance | Workshop | S02 | 1 voice, not physical goods |
| Guarantee maths 95 vs 117 net orders = 1.23x | Refund cost omitted | S01 | 1 voice, illustration |
| Satisfaction refunds 2 in 4,000 sales over 3.5 years | Service offer | S01 | 1 voice, service |
| Guarantee lift 2x to 4x from a better guarantee | Second-hand anecdote | S01 | 1 voice, no data |
| Try-before-you-buy: charge after 7 days | Amazon feature | S10, S06 header | 1 voice plus header `[web check]` |
| Limited drop: 100 units, monthly at most, always sell out | Physical limited releases | S01, S10 | 1 voice (same author) |
| Deadline windows: 7 to 21 days mail; 48 hours or "this week" email with 1 to 2 reminders; last 4 hours = 50% to 60% of a week-long launch (no data) | 2009 mail and S01 claim | S02, S01 | 2 voices, stale |
| Lightning deal 60 minutes | Amazon | S10 | 1 voice |
| Pop-up opt-in: no offer 1% to 5%; static 10% about 7%; mystery 10% about 15% (17.46% at 1 client) | S06 scenario | S06 | 1 voice |
| Pop-up test: free gift 520 opt-ins at 3.3%; 10% off 476; mystery $25 at 7.6%; "$25 in credit" about 1,800 at 10.7% | 1 client, $250 to $300 AOV | S07 | 1 voice |
| Email revenue $0.30 per subscriber per month | Scenario input | S06 | 1 voice, assumption |
| Form fields: about 20% abandon per field; ochre button beat red by 27% | 2008 data | S02 | 1 voice, stale `[web check]` |
| Offer review at 90 to 120 days; hold a winner 6 to 12 months | S04 | S04 | 1 voice |
| About 10 good offers in 100 | S04 | S04 | 1 voice |
| Offer testing lift range 10% to 900% | Bly's claim | S02 | 1 voice, claim |
| Promo wrapper rotation every 4 weeks; refresh order creative > copy > wrapper > duration > enhancer > monetisation | S01 | S01 | 1 voice |
| Reach cost 1,000 people for about $20 (2021) | Local ads | S01 | 1 voice, stale |

## 7. Where sources disagree

Each conflict: what each side says, when each is right, what the agent should do.

**C1. Free-shipping thresholds: weak or standard?** S06's speaker ranks the free-shipping threshold "cheaper but weak" and shows free shipping losing money on a $14 order; S06's own card and common practice call a threshold a standard AOV lever; S04 uses thresholds but sets them on the distribution's peaks and prefers a product unlock; S09 shows a free-shipping bar in the cart as normal. When each is right: a threshold set just above a real peak with a product or sample unlock moves orders and pays; a threshold set at the mean, or free shipping on a low-AOV single item, gives shipping away. What the agent should do: never propose free shipping as the offer; propose a threshold only after P7 and F17 pass, prefer an unlock at the threshold, and treat "free shipping" as a promise row item (R135) when it is already true.

**C2. Checkout abandoners: discount or not?** S04: no discount; risk reversal, a reminder or free shipping, because friction stopped them and they buy in 2 to 3 days. Common practice (and many flows in 14-EML) sends a code. S07's stacking method assumes the welcome code applies to whoever has it. When each is right: S04 is right for high-intent abandoners on a brand with price integrity; a code is defensible where the brand already discounts and the abandoner never saw the first-order offer. What the agent should do: default to S04 (no new discount at checkout abandonment; reminder plus risk reversal plus delivery promise); allow the existing first-order offer to be restated, never a deeper one; test the discount version only with a holdout on contribution.

**C3. Discount on one-time orders, or none at all?** S05 (and S07): no discount, no gifts on one-time; everything on subscription. S03: use buy-more-save-more and value stacks, and keep a one-time path when CAC needs it; S09: Love Wellness sells one-time and subscribe-and-save side by side; S06 and S04 discount one-time bundles freely. When each is right: S05 for a consumable take-rate strategy with proven subscriber LTV; S03, S06 and S04 for brands that need first-order volume, non-consumables, or when CAC has risen. What the agent should do: for consumables with cohort data proving the gap, put the offer on subscription and keep one-time at full price; for non-consumables (jewellery, kits) the "no one-time discount" rule does not apply and the ladder or gift carries the offer; never discount one-time deeper than subscription.

**C4. Do 5% to 10% discounts lose money?** S04: yes, at that depth nobody adds units, so contribution per order falls. S06: a 10% to 15% welcome offer converting at 10% to 18% opt-in "substantially" moves email margin; S07 uses 10% off as a test arm and calls a bare 10% "not enough" rather than harmful; S02 treats small early-bird discounts ($5 to $10 on $100) as enough. When each is right: S04 is about sitewide flat discounts on the same traffic; S06 and S07 are about a first-order code that buys an email address and a first purchase. What the agent should do: no token sitewide discounts; a first-order code is allowed only where the brand discounts at all, sized by R34, and judged by F16 on gross profit and LTV, not opt-ins. Related: **C4b, BOGO.** S06 header and S07 say "buy 2 get 1 free" beats "33% off 3"; S06's speaker says BOGO is "very hard to use unless it makes sense on your margin". Both hold: framing wins at the same total price, and a free unit is real COGS. The agent frames as free only after F10 passes.

**C5. Upfront subscribe-and-save discounts: front-load or avoid?** S07 (and S05's examples): front-load 25% to 30% then 5% to 10% recurring; S06 header the same. S03: "I kind of hate discounting upfront on subscriptions"; lead with bulk tiers and value stacks, and use discounts in the cancel flow. S04: a lifetime 25% rate gated on a 90-day supply and the subscription tick. When each is right: front-loading wins take rate for consumables with proven LTGP and cash; S03's approach wins where discount hunters churn after order 1 or margin is thin. What the agent should do: model both with F11 on the brand's cohorts (P10); if churn after order 1 for front-loaded cohorts is unknown, start with S03's ladder and value stack, and front-load only as a test with a 90-day LTV read.

**C6. Subscription-only versus keeping a one-time option.** S09 (Space Goods) and S07's model 4 show subscription-only; S05 and S07 keep one-time but recess it; S03 makes one-time a small hyperlink while LTV supports it and restores it when CAC rises; common advice keeps one-time to reduce first-order friction. When each is right: subscription-only can work for a daily consumable with a strong kit and cash; it suppresses trial for high-consideration or high-price products. What the agent should do: keep a visible one-time path by default; test hiding it only with a holdout on contribution per visitor, and check pre-selected subscription and cancel rules first `[web check]`.

**C7. Credit versus free gift in pop-ups.** S07's test: "$25 in credit" beat the incumbent free gift by about 3.5x on opt-ins and about 3.2x on placed-order rate, and won on gross profit after gift COGS; S06 favours mystery framing of a discount; S02 (Benson) says a premium beats a cash discount if you pick only 1, and free units beat equal cash. When each is right: a credit or currency figure wins at high AOV where the gift's value looks small next to the price; a gift wins where it is useful to the product's use and cheap to the brand. What the agent should do: run P17 with both arms; "credit" must be a real redeemable balance; judge on gross profit and 90-day LTV.

**C8. Raise-then-discount.** S07: "jack up your prices and then discount down to your target price"; S04: list the gift at a price and show "$160, now $100". S02: put a price on the free item and actually sell it at that price so the claim is true. ecomOS: no invented reference prices. What the agent should do: reject raise-then-discount unless the higher price is a real, recent selling price in that market; state bonus values only at prices the item sells at; flag every strike-through `[web check: reference-price rules per country]`.

**C9. Bury cancel versus easy cancel.** S05: delay on top, manage at the bottom of the billing reminder, a founder video splash before cancel; S03: one-time purchase as a hyperlink, founder video, matched save offers; both want save flows. Consumer rules in several markets require cancel to be as easy as sign-up, and India's 2023 guidelines list subscription traps as a dark pattern. What the agent should do: keep the founder video and matched save offers (they are content, not obstacles), but cancel must be findable in the portal and completable in no more steps than sign-up; no extra steps, no hidden links; `[web check: click-to-cancel rules per country]`.

**C10. Scarcity and timers.** S10 presents per-size stock counts, 60-minute deals and Friday drops with no truth condition; S07 praises a flash page with a countdown to midnight and a "79% claimed" bar he cannot verify; S09 shows a "reserving your order due to high demand" timer as a tactic; S02 says an invented reason "can work"; S01 says fake countdowns lose credibility and S01's physical-product scarcity is real limited runs; S02 also says do not use fixed print runs for downloads and never extend a deadline. What the agent should do: only real, enforced limits and dates (R111, P15); no reservation timers without a real hold; no "claimed" bars without live data; `[web check]` per country.

**C11. Gifts on order 2.** Platforms and S05 place gifts on order 2 (months 2, 4, 6) to lift retention; S03's tests found untargeted second-order gifts did not pay back and gifts belong in the acquisition promise or a targeted save. What the agent should do: run F13 with the brand's churn by order number; if the gift is used, announce it before purchase and make it click-to-claim (R57).

**C12. Same-product bundles versus mixed bundles.** S07: mixed bundles perform worse because buyers only want 2 of 3; S04: multi-SKU brands should use native bundles and cross-category upsells; S06's Grind Machine bundles related gear with a single hero product. What the agent should do: default to same-SKU ladders; allow mixed bundles only when the items form 1 routine or the hero is a non-consumable with related accessories; test both on CP per visitor and return rate.

**C13. Acquisition first or retention first for subscription brands.** S03: growth is capped by acquisition; offer and persona testing come before retention tinkering. S05: retention is the bigger profit lever; optimise for the 3rd and 4th order. When each is right: S03 when the base is near its cap (F12) or take-rate and persona data are thin; S05 when cohorts show early churn from onboarding or cadence problems. What the agent should do: compute the cap and the churn-by-day chart; work on the constraint the data shows; keep both tracks running.

**C14. Pause as a save option.** S03 and its host: no open-ended pause; S05 lists pause among the perks a subscriber can use. What the agent should do: offer delay (capped, auto-resuming) and frequency change; rename any auto-resuming "pause" as delay; if the platform only has open-ended pause, cap it `[verify UI]`.

**C15. First-payment framing and instalments.** S02: buyers react to the first payment; "$19.95 a month" beats "$240 a year"; quarterly payments beat a cheaper annual price in 1 test. Modern drip-pricing and total-price rules, and the cards, require the full price to be visible. What the agent should do: show the total; BNPL and instalments may be offered as effort reducers (R4) with the total stated; `[web check: instalment and drip-pricing rules per country]`.

**C16. Win-back: broad and fast, or split by reason?** S03 now prefers 1 broad offer track rotated every 1 to 2 weeks; S05 segments win-back by cancel reason at 30 to 60 days. What the agent should do: broad first for small lists (bigger groups give clearer reads), reason-split only with bandwidth and volume; both step down from a bigger first-order-back offer to the standard rate.

**C17. Guarantee: unconditional and long, or conditional when fulfilment cost is high?** S02: unconditional 60 to 90 days is best; conditions depress sales; people are basically honest. S01: prefer conditional or anti-guarantees when fulfilment cost is high; tie conditions to success actions; broad for low-ticket B2C. S10: money-back is table stakes, add try-before-you-buy. What the agent should do: cost both with F8 using the brand's return cost; for low-ticket consumables an unconditional window near S02's is usually affordable; for high-ticket or high-return-cost goods (jewellery, bulky items) the conditions and the length come from the returns model; statutory rights come first.

**C18. Giveaways and free guides as first-order hooks.** S07: never (low intent); S02: a free buying guide "often doubles" lead response and soft leads convert as well as hard ones. When each is right: S07 for impulse and replenishment DTC; S02 for considered purchases with a research step. What the agent should do: for consumables and low-ticket goods, the 4-type shortlist (R126); for jewellery-grade or gifting purchases, test a guide or quiz beside the buy button (R132) and judge on downstream purchase, not email volume.

**C19. Test offers and creatives together, or isolate the offer?** S08's presenter: both at once; S08's cards and 09-CRO: hold creative constant to credit the offer. What the agent should do: isolate when the question is "did the offer cause it"; run parallel only when looking for combinations, and say so in the test record.

**C20. Middle tier default versus "make the largest tier visually heavier".** S07's transcript: default the middle because the largest feels scary; S07's card adds "make the largest tier visually heavier". What the agent should do: follow the transcript (middle default); visual weight on the largest tier is a 07-LPG test, not a rule.

**C21. Bonus format: tools and checklists, or education?** S01: tools and checklists beat more training; S10: bonuses are how-to videos and guides. Both agree the bonus helps the buyer use the product. What the agent should do: prefer the shortest asset that removes the effort (a dosing card, a 90-second styling clip); avoid long courses unless the product's result depends on a routine.

**C22. Offer as the biggest lever versus market and product first.** S07 and S06: the offer is what separates 7-figure from 9-figure brands and "the most sensitive lever"; S01: market beats offer beats persuasion; S04: product and brand outrank offer in his hierarchy. What the agent should do: check the market and product fit first (R12); then the offer is the highest-leverage change the agent controls.

**C23. The AOV × CVR > 250 screen.** S09 uses it as a scale gate; S04, S06 and S08 judge on contribution and profit per session; the screen has no margin term. What the agent should do: R22, a first sort only.

**C24. Hormozi's "never discount the core offer" versus his own "88% off" magnets.** Inside S01 discounts appear as time-limited promotional wrappers in lead generation, not as a concession to close. What the agent should do: no discounting to close or to rescue revenue; dated promotional wrappers are allowed under P16.

## 8. Common mistakes

Merged from all sources, deduplicated, with the fix.

1. Calling a percent off "the offer". Fix: write the 5 variables; fill 3 or more. (S04, S07, S06, S01)
2. Modelling a discount without the UPT lift, or with COGS on the discounted price, or without shipping and fees. Fix: P3 with F5. (S04, S08)
3. Reading a higher ROAS, revenue or AOV as a win. Fix: CP per order and per visitor (F2). (S06, S08, S09)
4. Running a bigger offer without resetting ROAS and CPA targets, so revenue grows and profit falls. Fix: R15. (S08, S04)
5. Token 5% to 10% sitewide discounts. Fix: R33; structural offers instead. (S04)
6. Discounting to rescue a revenue number or on a weekly promo calendar, training buyers to wait. Fix: R32, R27, P16. (S04, S07, S01)
7. Free shipping on a low-AOV single item. Fix: multi-pack or threshold above a peak (P5, P7). (S06)
8. Setting thresholds on the mean AOV. Fix: P7. (S04)
9. Only one pack size, or only the biggest pack. Fix: 3 tiers, entry at full price, middle default (P5). (S08, S07)
10. Forced mixed-product bundles. Fix: same-SKU ladders unless a routine (C12). (S07)
11. Tiers with no reason and no per-unit price; labels that need mental math; the smaller of dollars and percent shown; "buy 2 get 1 free" called "60% off". Fix: R37, R34, R35, R48. (S08, S09)
12. Gifts nobody cares about (tote bags, stickers), gifts of the same product, gifts never announced, untargeted order-2 gifts. Fix: P6, R53 to R58. (S05, S07, S03, S04)
13. Stacking so much that the buy box confuses; keeping a bonus that sells but disappoints. Fix: R11, R121. (S04, S09)
14. Judging upsells by take rate or AOV lift; 3 offers in 1 cart slot; a full product at checkout; leading post-purchase with the cheapest item. Fix: P8. (S04)
15. Flat "subscribe and save 15%" as the whole subscription offer; one-time pre-selected; a 2-option buy box; a pop-up that undercuts the subscription offer. Fix: P9. (S05, S07, S03)
16. Chasing 80% to 90% take rate without contribution and LTV data; front-loading with no churn read. Fix: P10, R80. (S03, S07)
17. Sizing an offer from a source's LTV numbers instead of the brand's cohorts. Fix: F11 with brand data. (S05, S06, S07 caveats)
18. First-order-loss subscription plays without the cash to carry them. Fix: R19. (S06)
19. A sitewide sale that equals or beats the subscriber rate; subscribers included in promo sends; no subscription layer in a sale. Fix: P11. (S03, S05)
20. Open-ended pauses; treating a skip as a save; chronic skippers left in limbo. Fix: R97. (S03)
21. No billing reminders "because they cause cancels" while all subscribers get campaigns. Fix: R99. (S03, S05)
22. Taking cancel reasons literally; a long cancel survey; the big offer in the cancel confirmation; win-back split 7 ways on a small list. Fix: P12, P13. (S03)
23. Guarantees with no "or what"; conditions like "saleable condition"; "full refund" that excludes shipping; clock from order date; buried in a footnote; used to cover a weak product. Fix: P14. (S01, S02)
24. Stacking guarantees without costing the combined worst case; try-before-you-buy without checking capture, returns and fraud. Fix: R104. (S10 vs S01 cards)
25. Fake countdowns, resetting timers, evergreen "only 3 left", "high demand" reservation timers, extended deadlines, print-run scarcity on unlimited goods. Fix: P15. (S01, S02, S09, S07)
26. Invented reference prices, raise-then-discount, stated bonus values with no real price. Fix: R28. (S07, S04 vs S02)
27. Copying another brand's claims, counts and discounts. Fix: R136. (S09)
28. Offer mismatch between ad, page, cart, checkout, email and support; expired promos left visible. Fix: P19. (S01 card, S04 curator, S08)
29. Skipping the pop-up, or a pop-up with no offer; giveaways and free guides as DTC hooks; a bare 10% left for years untested. Fix: P17. (S06, S07)
30. Testing only discount depth; declaring winners on opt-ins or revenue; changing everything at once; quitting after 1 losing test; changing a working offer out of boredom. Fix: P24, R146, R123. (S07, S09, S02, S01)
31. Making bigger claims instead of cutting time and effort; improving the product without showing it; naming the product after the category. Fix: P20, P23. (S01, S10)
32. Slow shipping (2 weeks), forced account creation, missing wallets. Fix: R137. (S08, S10)
33. Using USD thresholds unconverted; applying the 250 screen as a gate. Fix: R150, R22. (S07, S09)
34. Taking a card's ecommerce adaptation or a curator header as the source's evidence. Fix: R151; section 12. (S01, S02, S06, S10)

## 9. Deliverables

Every deliverable states its inputs, marks `[needs brand data]` and `[web check]` items, attaches the calculation log, and is written in plain English: short sentences, digits, no em dashes, no inflated words, no invented claims, no mention of GPT or .env on client-facing pages.

### 9.1 Three costed offer options
Format: 1 page plus an options table.
- Header: brand, product or SKU set, goal (conversion, AOV or LTV; R2), audience (new, returning, subscribers), date, currency.
- Current offer row: the 5 variables, price, GM per order, CP per order, CP per visitor, BE_ROAS, target CPA, take rate by tier if any.
- 3 option rows, each: the offer in the 5 variables; tier table with per-unit price, dollars and percent saved, per-serving or per-day; gifts and their landed cost; guarantee; honest urgency element if any; CP per tier (F10); CP per order and per visitor at conservative demand and at break-even demand (F2, F6); required ROAS and efficiency lift needed (F4); for LTV plays LTGP(K), K, CAC ceiling and payback (F11); cash needed if order 1 loses; risks; `[needs brand data]` gaps; `[web check]` flags by country.
- Recommendation: which option to test first and why, in 3 sentences.
- Appendix: calculation log (script name, inputs, outputs), source rules used (R numbers), and the mini playbooks behind them.

### 9.2 Fixed-offer presentation fix list
Format: a ranked table.
- Columns: surface (ad, landing page, PDP, cart, checkout, pop-up, email, support macro); what it shows now (quoted); what it should show; which rule (R numbers); evidence needed to make the claim; cost to fix (copy, layout, data); owner folder (03-OFF, 07-LPG, 11-ADC, 14-EML).
- Ordered cheapest and highest-leverage first (mismatches and expired promos, then value-equation gaps, then framing, then buy-box reinforcement, then bonuses).
- A line confirming no price, code or gift change is included.
- The value-equation scorecard (P20) and the competitor check (5.9) as an appendix.

### 9.3 Promotion plan with stop rules
Format: 1 page.
- Purpose and type (stock clearance, seasonal wrapper, tested offer); why not a flat discount if one is proposed.
- Audiences and the offer for each (new, returning, subscribers); the subscriber offer first (P11).
- Depth, modelled with P3 and P4; required ROAS and CPA; the measured sale-period lift it is compared against.
- Cannibalisation estimate (R118) and the incremental contribution result.
- Dates, time zone, the true reason, the post-deadline state, and the honesty check (5.8).
- Stop rules with numbers and owners: required ROAS or CPA missed for N days; discount share of revenue cap; subscriber cancels above baseline; refund rate above baseline; stock below the stated limit.
- Surfaces to update and the congruence check (5.2).
- Post-sale read: price-integrity metrics for 30 days.
- `[web check]` flags by country.

### 9.4 Subscription design
Format: a spec plus a model.
- Product use classification, cadence and pack options, and the evidence.
- Buy box: 3 options, which is pre-selected, price and saving per option, what is gated on subscription, one-time price and placement, the disclosure text next to the default.
- Discount structure: first-order, recurring, longer or prepaid tiers; modelled with P10 (scenario table, LTGP(K), CAC ceiling, payback).
- Gift roadmap: items, landed cost, when shown, click-to-claim; F13 result.
- Results-horizon messaging requirement (for 14-EML).
- Sale policy for subscribers (P11) and the rule that public offers never beat the subscriber rate.
- Cancel-flow save-offer logic (P12) with F18 costs; win-back offers (P13).
- Portal rules the offer depends on (skip, delay cap, frequency change) for 17-CXP.
- `[verify UI]` items for the subscription platform; `[web check]` items for auto-renewal, pre-selection and cancel rules by country.

### 9.5 Test proposal (for 09-CRO and the experiment registry)
Format: 1 page.
- Hypothesis, the single variable, control and variants written in the 5 variables.
- Preselected metric (CP per visitor; gross profit after gift or discount cost; LTV window K) and which costs count.
- Traffic plan: equal split, dedicated pages, creative held constant or not (C19).
- Sample size, duration and stopping rule: requested from 09-CRO.
- Read plan: CVR, AOV, UPT, CP per order and per visitor, refund rate, take rate by tier, then the LTV read at K.
- Rollback plan.
- Registry record fields: brand, date, offer before and after, result, decision.

## 10. What needs live data or a web check

### 10.1 `[needs brand data]`
- Price list per SKU and variant in the selling currency; all-in COGS per unit (product, inbound freight, packaging, duties); shipping and 3PL cost by units per order and weight band; payment and app fees per order.
- Order-level order values for 90 to 180 days; UPT overall and in past sale periods; sessions, CVR by traffic type, blended CAC or CPA; discount share of revenue; repeat buyers who only buy on sale.
- Past sale periods: dates, depth, ROAS or CPA, UPT, refund rate; the measured efficiency lift in sales versus non-sale periods.
- Cohort repeat rate and LTV at 90 days, 6 and 12 months, split by first-order type (one-time, subscription, bundle tier, pop-up variant); survival curve by order number; churn by month and by day since subscription start.
- Subscription take rate; cancel reasons by plan; save rate; skip, delay and pause use; failed-payment revenue and recovery; share of one-time buyers who later subscribe.
- Return and refund rate, return cost per order, resale rate, chargebacks, fraud rate (for delayed capture).
- Take rate and margin by upsell SKU and placement; cart attach rates.
- Pop-up: visitors, opt-in rate, placed-order rate by variant, email revenue per subscriber, ESP tier costs, code redemptions, credit redemption and breakage.
- Objection list from reviews, support, chat and cancel reasons; the usage questions buyers ask; evidence for any result timeline claimed.
- Live inventory by variant and production limits before any scarcity claim; sales by hour in past launches.
- Delivery and dispatch times by region; production lead time for made-to-order items.
- Current offers on every surface, support macros and refund policy text; owner's discount policy; whether the brand is fixed-offer; selling countries; cash runway and months to payback.
- Gift landed cost, box fit, shipping impact; kit unit economics (18-COG).
- Reach and frequency by creative before calling an offer fatigued.
- Real alternative costs used in any price comparison.
- Brand-specific: Gehna prices in INR (convert every USD threshold); Peach Bucket's fixed offer text and surfaces; TrailFold is fictional and gets no live data.

### 10.2 `[web check]` by selling country
- Reference prices and strike-through "was" prices; stated bonus and kit values; "up to X off" savings claims.
- False urgency and scarcity: countdowns, stock counts, "claimed" bars, reservation timers, limited drops (US FTC, UK CMA and DMCC, EU UCPD, India's 2023 dark-pattern guidelines).
- Auto-renewal and negative-option rules, pre-selected subscription options, billing reminder requirements, click-to-cancel rules, subscription traps.
- Pre-ticked checkout add-ons (shipping protection), drip pricing and total-price disclosure, instalment and BNPL disclosure.
- Statutory return and warranty rights that sit under any guarantee; "all sales final" limits.
- Health and outcome claims by category (supplements, skincare, GLP-1 adjacent); outcome-plus-timeframe claims in ad names (Meta and Google policy).
- Delayed-capture and try-before-you-buy support by payment processor and platform; current Amazon Try Before You Buy terms as the model.
- Current Shopify behaviour: discount combination (additive or compounded), subscription widget defaults, checkout customisation by plan, whether the native order confirmation can be disabled.
- App names and features named in the sources: Skio, Recharge, Stay AI, Loop, Prosper Stack, Rebuy ("Reby"), Alia, KnoCommerce, ChurnBuster, PostPilot, "Zamo", "Fly Code", "Redux"; the S04 discount-to-efficiency calculator; S03's Cancel Page resources; S01's Acquisition.com training pages.
- Brand offers used as examples (IM8, AG1, Armra, Everyday Dose, True Classic, Live Fresh, Space Goods, Love Wellness, Symbiotica, Rise, Dr. Squatch, Bloom, H1, Elevate, Gruns) are point-in-time snapshots and change often.
- Uncited studies: the wine price test, the London Underground map, Grandview and IHRSA market sizes, the 57% white-paper survey, Jonah Berger's rule of 100, the 2008 form-field abandonment figure.
- Current CPM figures (S01's $20 per 1,000 is 2021).

## 11. Freshness and stale-risk notes

| Rule area | Depends on | Re-verify | Notes |
|---|---|---|---|
| Buy-box defaults, 3-option layouts, gated perks (R78, R82) | Shopify subscription APIs and app widgets (Skio, Recharge, Stay AI, Loop) | Quarterly and before any build `[verify UI]` | S03 says platform features are the most time-sensitive part; founder-video splash and time-window portal popups were new in 2025 to 2026 |
| Discount stacking (F14, R93, R129) | Shopify discount-combination settings | Before every stacked claim `[verify UI]` | Additive versus compounded changes the advertised number |
| Cancel-flow saves, click-to-cancel (R94 to R96, C9) | Consumer law (US FTC negative option, state auto-renewal laws, EU and UK rules, India 2023 guidelines) | Before launch and every 6 months `[web check]` | S05 flags billing-reminder law only; the rest is the repo's flag |
| Reference prices, stated values, "up to" claims (R28, R60, R129) | Pricing law per country | Before every use `[web check]` | S07's raise-then-discount and S04's gift list price are the risk lines |
| Scarcity and urgency (group L) | Dark-pattern rules per country; live inventory | Before every use `[web check]` | S02's "invented reason", S10's untested stock counts, S09's reservation timer are 2009 to 2025 practice |
| Pre-ticked checkout add-ons (R72) | Consumer rules and platform policy | Before use `[web check]` | Shipping protection provider terms change |
| Try-before-you-buy and delayed capture (R104) | Processor support; Amazon's programme terms | Before use `[web check]` | S10's 7-day model is a 2021 to 2024 Amazon feature |
| App and tool names (section 10.2) | Vendor changes | Every 6 months `[web check]` | Several names are phonetic transcriptions |
| Brand example offers (IM8, AG1, True Classic and others) | Live pages | Before quoting `[web check]` | Snapshots from 2025 |
| USD thresholds ($100 rule, 250 screen, $25 credit) | Currency and price levels | Convert every time | None tested outside USD |
| Direct-mail numbers from S02 (deadlines, per-field abandonment, print costs) | 2008 to 2009 data | Treat as test ideas only | Stale by design |
| Ad platform policy on outcome-plus-timeframe names (R138) | Meta and Google policy | Before naming `[web check]` | S01's line is 2021 |
| CPM and reach cost (S01) | Ad markets | Do not use | 2021 figure |
| Take-rate and RPV ranges from S04 | His market and clients | Replace with brand data | Never benchmarks |

## 12. Source index

Confidence tallies in this playbook count independent voices, not files. S01 and S10 are the same author (Hormozi). S05 and S07 are the same agency (WellCopy: same community name, same "custom Claude skill", same IM8, AG1, Armra and Everyday Dose walk-throughs). The brief said S06 and S07 look like the same talk; on reading, S06 is a different presenter (a DTC agency owner with the $14 sock model, Garden Alchemy and Giggly examples), but S06 and S07 share brand examples and the front-loaded subscription formula, so they are never counted as 2 voices for the same claim. Net: 8 voices across 10 files.

| No. | Title | Type | Credibility and bias | What it contributed most |
|---|---|---|---|---|
| 01 | $100M Offers (Hormozi) | Book, 2021, services and info products; 70 cards | Author of the framework; sells nothing in the book but takes equity in businesses; own self-reported results, 1 voluntary survey, uncited studies; the book calls its numbers "theoretical". Applies to physical products only where the text names them (limited releases, sell-outs, supplements versus gyms, lotion margin, infomercial knives, Prestige Labs partner discount, auction goods); the rest is service advice adapted by cards. Bias: premium-price, never-discount stance; "make one up" for anti-guarantee reasons (rejected). | Value equation (R3, R4), trim and stack (P25), enhancer logic, honest scarcity for limited drops (R112), urgency that expires the promo not the product (R113), guarantee form and refund maths (R101, R102, F8), MAGIC naming (P23), refresh order (P21). Bounded by S10 (which parts transfer) and by S04, S06 and S08 (margin maths the book lacks). |
| 02 | How to Create Irresistible Offers (Bly) | Book, 2009, direct mail, B2B lead generation and info products; 57 cards | Freelance copywriter; published by AWAI, which sells training; own mailings, client stories, third-party tests quoted without sample sizes, Benson's 1992 rules. Ecommerce steps come from the cards, not the text. Bias: direct-response conventions; "invented reason can work" (rejected); first-payment framing (rejected for total-price rules). | Dollar versus percent by fixed or variable saving (R34), "free" as the strongest word (R35), premium versus cash discount evidence (R36), 6 traits of a premium, guarantee's 4 decisions and 60 to 90 day preference (R103), real deadlines and never extend (R113, R115), trials fail by inertia (R109), good-better-best middle (R43), sell the free item at its stated price (R28), soft and hard offers for considered purchases (R132), test expectations (R146). |
| 03 | The Most Valuable Subscription Video (Holman) | Podcast transcript, 2025 to 2026; 29 cards | Subscription agency owner and paid resource site; host runs an email agency; client anecdotes, 1 old Autoship Cloud study; several numbers are the host's. Bias: sells subscription services; calls his thesis "rage bait". | Subscriber cap (F12), buy-more-save-more as the first mechanic (R41), value stack cheaper than a discount (R54), take rate versus LTV by contribution margin (R80), untargeted gift maths (R58, F13), sale collision and subscriber-first offers (R91, R92), cancel-flow discount logic (R94), no open-ended pause (R97), broad win-back (R98), dislike of upfront subscription discounts (C5). |
| 04 | How 8 and 9 Figure Brands Build Offers Without Discounting | 90-minute talk, likely Australian agency, 2024 to 2026; 36 cards | Unnamed performance agency owner; opinion plus worked round-number examples; no test data; sells a calculator and audits; some arithmetic does not match his inputs. Bias: anti-discount, pro-stacked-offer. | The economics core: the waterfall, break-even and required ROAS, COGS on retail units (F1, F3 to F5), the discount curve (R33), sale lift by brand type (R18), 5 offer variables (R1), thresholds on the distribution (R62), gift-with-purchase maths (P6), stacked evergreen offer (P25), upsell scoring and placement (P8), exit-intent by stage (R131), 4 selection questions, 90 to 120 day review (R121). |
| 05 | The $100M Subscription Brand Playbook (WellCopy) | YouTube transcript, likely July 2025; 14 cards | Email, SMS and subscription agency; 3 sales pitches inside; screenshots and 4 single-client results, 1 A/B test. Bias: sells retention services; legal risks of buried cancel and pre-selection not addressed. Same agency as 07. | Subscription-first offer architecture (R77), 3-option buy box with subscription pre-selected (R78), pop-up equals the subscription offer (R129), consumption gifts and roadmap (R53, R85), cadence by use (R83), results horizon (R86), subscriber exclusion from sales (R92), save-rate bands, win-back timing (R98). |
| 06 | I Studied Every Ecommerce Offer | YouTube transcript, likely 2025; 19 cards, 8 to 9 of them header-only | Unnamed DTC agency owner; client screenshots and round-number scenarios; "works every time" with no data; a curator header adds rules the speaker never said (value equation mapping, dollar versus percent, 25% to 30% then 5% to 10%, middle default, BOGO framing, try-before-you-buy, scarcity, digital bonuses). Bias: sells agency work; pro mystery pop-ups; pro first-order-loss for cash-rich brands. Counted as 1 with 07 wherever they agree. | Offer as a trade of unit margin (R2), the $14 sock model and free-shipping loss (R21, R63), order of work (free money, weak, worth paying for, where brands die), pop-up opt-in scenario and mystery framing (R125, R128), subscription as an auction gated on cash (R88, R19), LTV ceiling logic (F11), prepaid plans (R84). |
| 07 | I Studied Every $100M Ecommerce Offer | YouTube transcript, 2025 or later; 17 cards | WellCopy agency (same as 05) and its analytics platform; 1 cohort chart, 1 repeat chart, 1 8-variant pop-up test with opt-in counts; brand page walk-throughs; agency, community and pop-up tool plugs. Bias: sells retention services; "jack up prices then discount" (rejected); flash page he cannot verify. Counted as 1 with 05, and never as 2 with 06. | Structure over depth (R39), front-loaded subscription formula (R79), 4 ranked subscription models (P9), welcome-kit gifts with stated values, same-product bundles (R42), middle-tier anchoring (R43), "free" framing (R35), dollar off above $100 AOV (R34), the 8-variant pop-up test and credit framing (R127), stacking site offers into 1 number (P18), 90-day LTV read (R23). |
| 08 | How To Create Winning Offers In Ecom (Evolve) | Auto-captioned video, 2024 or later; 11 cards | Sells a consulting community; secondhand store results, no margins or lifts; borrows Hormozi's value equation and Schwartz's stages. Bias: motivational framing; loose discount equivalence ("buy 2 get 1 free" versus "60%"). | Profit per session as the offer metric (F2, R143), reset ROAS and CPA per offer (R15), fixed costs fall per unit (R20), AOV versus conversion balance (R45), tier reasons (R46), rule of larger numbers (R34), no mental math (R37), value equation on the page and in the ad (R4, R7), awareness-stage claims (R141). |
| 09 | $10,000,000 per year on Shopify (Jordan Hayes) | YouTube teardown, May 2025; 10 cards | Agency owner teardown of Space Goods, "Jabi" and Love Wellness pages; no data, unsourced $10M claim; the 250 rule is his own; presents a reservation timer without caveat. Bias: sells agency calls. | Layered offers (R52), per-serving price on every tier (R48), gifts that scale with units (R55), starter kit, variant before quantity (R47), promise row with delivery date and guarantee (R135), subscription-only as 1 valid layout (C6), AOV × CVR > 250 as a screen (R22), test 1 element (R145). |
| 10 | Applying $100M Offers to E-Commerce: I'm Pissed (Hormozi) | YouTube transcript, about 2021 to 2024; 7 cards | The author of 01 arguing his framework applies to products, using Amazon as the model; no store data; no costs; presents stock counts and 60-minute deals with no truth condition. Bias: defending his own book. Counted as 1 with 01. | The bound on 01: which parts the author says transfer (all 4 value drivers and all 5 enhancers, with different "vehicles") and the product levers for each (R4), 2-layer time delay, money-back as table stakes plus try-before-you-buy (R104), how-to bonuses (R59), outcome and search-term naming (R138), the same-product competitor checklist (5.9). |

**Where source 01 applies to physical products by its own text, and how source 10 bounds it.** By text: the offer model names physical products, software and brick-and-mortar; lotion gross profit ($10 price, $2 cost); beauty vehicles; the golf-club status line; supplements versus gyms; the "Physical Products" scarcity subsection (limited flavours, colours, designs, sizes; 100 boxes; always sell out; about monthly; announce sell-outs); infomercial knives; Prestige Labs partner discount; auction goods. Not addressed for physical products by the text: the Value Equation examples, the 5-step build, pricing cases, service scarcity caps, the 4 urgency methods, bonus presentation, all guarantee types, naming examples. Source 10 says all 4 value drivers and all 5 enhancers transfer but with different vehicles (show the product in use, what arrives, delivery speed, one-click checkout, stock per size, lightning deals, easy returns plus try-before-you-buy, how-to content, outcome names); it gives no view on market choice, trim and stack, guarantee types beyond money-back, guarantee economics or MAGIC. This playbook uses 01's service-only parts (guarantee types, 5-step build, urgency methods) as idea sources marked by the mini playbook's "[text: service/info]" tag, always behind the economics gate of S04, S06 and S08 and the honesty rules of the repo.

**Arithmetic slips found in the sources and corrected here (do the maths in code; quote the corrected value).**
- S01: 2.5 × 2.5 × 4 = 25, not "22.4"; $112,000 / $10,000 = 11.2x; 200,000 people at $20 per 1,000 = $4,000, not $10,000; 1,960 hours is 49 weeks at 40 hours, not a year; profit $2,943 to $8,940 is 3.04x, not 3.1x; "Feb 30" is a typo; the 95 versus 117 guarantee example omits refund cost.
- S03: 20% + 20% compounded is 36%, not "up to 40%"; the 3-bag tier at $120 has the same $40 per bag as the 2-bag tier, so it carries no extra saving; "it jumps 10%" means 10 percentage points (5% to 15%).
- S04: break-even ROAS in the 25% sale is 2.14 from his inputs, not 2.22; the margin loss from $60 to $35 is about 42%, not "nearly 50%"; the upsell A versus B example gives A = $2.40 and B = $1.80, so A wins, not B (card 52ef4486583d's $1.60 for A is also wrong); break-even ROAS rises as 1 / remaining margin, a curve, not "linearly"; "binomial" means bimodal.
- S05: 8.6% to 5.8% is a 32.6% relative drop, so "33%" is right and the captioned "28%" is a fragment; community size is given as both 145 and 250+.
- S06: scenario A gives −$600 from its inputs, not −$617; the mystery pop-up gives exactly 3x, not "more than 3x"; $95 is 2.4x a $40 product, not "two times"; $289 / $95 = 3.04, so the "3:1" is the ratio the speaker used, but he also says "LTV times your margin", which is a different ceiling; in scenario C the CAC ($14.29) falls versus A but rises versus B.
- S07: if 15% equals $25 the price is about $167, so 25% is about $42, not "$35", and 35% is about $58, not "almost $50" or "$60"; 15% + 10% compounded is 23.5%, not 25%, and with a further 10% is 31.15%; store lift is stated as $200K and then $400K; agency size as 300+ and 100+ brands; the "$25 off" and mystery variants are not cleanly separated.
- S08: "buy 2, get 1 free" is 33.3% off, not "60%"; "67% off the 3rd unit" is 22.3% off 3 units; the 2-pack at $100 is $50 a unit and the 4-pack at $190 is $47.50 a unit; a low-effort product lowers effort (he misspeaks).
- S09: the per-bottle figures "15.95 each, $79.95 each" do not read as 2 unit prices; do not quote them; the "Jabi" gift ladder is 1, 1, 3, 4, not 1 per bottle.
- S02: the Copywriter's Toolkit is $79 in one place and $39 in two others; the Marlins at 23-14 lost about 38%, rounded to "4 in 10"; software premium value is $49 to $499 in one chapter and $49 to $300+ in another.

**Neighbour folders and what lives there.** 07-LPG: page layout, buy-box and cart UI, listicles, progress bars. 09-CRO: test sizing, significance, stopping rules, holdouts. 14-EML: onboarding, billing reminders, order confirmations, subscriber campaigns, win-back and welcome flows. 17-CXP: cancel-flow build, portal UX, dunning, unboxing and inserts. 20-FIN: landed cost, P&L ladder, cash, inventory grades, LTGP definitions. 18-COG: kit and gift sourcing and unit economics. 11-ADC: ad copy for the offer. 24-DEP: Meta and TikTok account work and name tests. 12-GAD: Google Ads and price parity on Shopping. 02-AVT: avatar and awareness-stage research. 06-MEA: attribution and analytics.
