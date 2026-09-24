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
| Refresh a tired offer | 3 group M (R99), P21 |
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

Rules are numbered R1 to R128 and grouped by sub-topic. Each states the rule, its condition, the mini playbooks that support it (S01 to S10), conflicts (C numbers point to section 7) and card ids. "Voices" counts independent presenters (see section 12): S01 and S10 are 1 voice, S05 and S07 are 1 voice, S06 and S07 are never counted as 2.

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
      d_be = 1 − (GM_order_current + COGS_new + shipping_cost(UPT_new) + fees + CAC) / (unit_price × UPT_new)
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
