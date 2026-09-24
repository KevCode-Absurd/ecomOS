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
