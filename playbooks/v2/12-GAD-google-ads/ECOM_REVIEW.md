# Ecommerce review: 12-GAD-google-ads

Reviewed: PLAYBOOK.md (31,564 words, 143 decision rules R1 to R143). Method: full read against `playbooks/v2/TEMPLATE.md`, then grepped `sources/` for missing-lever material.

## 1. Score: 4 out of 5

This playbook runs on contribution margin, break-even ROAS and CPA, AOV, Merchant Center and feed mechanics, PMax and Shopping structure, and SKU-level stock and margin tiers, none of which a SaaS or lead-gen account would touch. It loses a point because a real minority of its rules, mostly search ad mechanics, generic bidding-stage mechanics and its diagnostic method, read like a general Google Ads course with no store framing, and because it has no single ranked "what matters most" entry point for a given store.

Rule count in section 3 (143 rules, by my read):

| Type | Count | Share |
|---|---|---|
| (a) Store-specific | 97 | 68% |
| (b) Generic, correctly applied | 22 | 15% |
| (c) Generic, no store framing | 24 | 17% |
| (d) Out of scope | 0 | 0% |

The (c) rules cluster in 3.H Search (R72, R73, R74, R76, R77, R81, R82), 3.K Bidding (R111, R112, R115 to R118), 3.M Negatives (R124, R125), and 3.O Diagnosis (R135, R138, R140, R141). None are wrong, just Google Ads 101 any account would follow.

## 2. Prioritisation check: missing, drafted below

Section 0 has a load-by-task table and R129 has a 5-gate scaling checklist, but nothing ranks the 12 sub-topics for a given store. 4.23 step 3 orders scaling levers only. Drafted from the playbook's own rules and section 7 conflicts:

### 3.0 Ecommerce priority order

1. Tracking is correct: 1 primary purchase action, real order value, reconciled with backend orders (R11 to R21, gate 1). Nothing below is measurable without it.
2. Break-even ROAS and CPA known from contribution margin, not gross margin or a benchmark (R3, R4, R68). Every bid, budget and brand call reads off this.
3. Merchant Center and feed are clean: no disapprovals, accurate titles, price and stock synced (R22 to R40, gate 1). Catalogue stores add margin and bestseller labels (R37, R66); a single hero SKU needs 1 clean listing and a correct GTIN (R36).
4. Brand and non-brand split, brand excluded from cold campaigns (R53, R54, gate 3). Skipping this inflates every ROAS number above.
5. Launch order fits store shape: bestsellers-only Shopping first for a catalogue (R47, R65), 1 PMax plus brand campaigns for a single hero SKU (R86, conflict 7.1).
6. Bid strategy matches conversion volume, not the calendar: manual or Maximize Clicks with no data, value bidding near 30 conversions a month, tROAS near 50 (R108 to R110, conflict 7.9). A subscription or fixed-price SKU can move to tCPA sooner (R109).
7. Budget sized from AOV and margin: about 3 to 4x AOV a day to start (R119), cold traffic 80% to 90% once brand is split (R120). Low-AOV stores (under about $100) fix AOV first (R6).
8. PMax runs on inputs, not trust: brand exclusion, themed asset groups, feed-only tested on purpose (R84, R90, R92).
9. Search and Demand Gen layer in after Shopping and brand work: non-brand Search from converting search terms (R70), YouTube only after an AOV fit check and proven Meta creative (R96, R97). A Meta-heavy DR brand can bring Demand Gen in earlier (R42 exception).
10. Retention data lowers how far below first-order break-even the store may buy (R5); without it, stay at or above break-even.
11. Scaling passes 5 gates before more budget: feed, tracking, brand split, creative supply, bid maturity (R129, R130).
12. Diagnosis on a dip checks the bigger channel and outside changes first, in fixed order (R135 to R141, procedure 4.25).

Marketplace-heavy, luxury or considered-purchase, and mobile-first India stores are not covered by any rule here; those gaps are marked `[general practice]` in item 4.

## 3. Rule rewrites (15)

Wording only; condition, sources and card ids unchanged.

- **R19.** Read the last 3 to 7 days on conversion-time columns, not click-date columns; Google still credits the click date, so a store's own MER read will look worse than backend orders show.
- **R20.** Put Google Ads, Merchant Center and GA4 under 1 master login so the store's Shopify feed, ratings and purchase data reconcile under 1 account.
- **R51.** Turn off auto-apply recommendations, AI keywords and auto-created assets so Google cannot quietly spend on non-bestseller SKUs or undo a brand exclusion the store set on purpose.
- **R72.** Group Search keywords into single-theme ad groups by product or collection, never 1 keyword per SKU, so each collection page gets enough volume to leave learning.
- **R73.** Use exact match on keywords the store's own search terms already proved converted; broad match only with smart bidding and proof, never to guess demand for a new SKU.
- **R74.** Write 7 to 9 headlines and 2 to 4 descriptions built from the store's own offer, price point and bestseller angle, not 15 near-duplicates chasing an ad-strength score.
- **R76.** Lead headlines with the product, price break or live offer; use descriptions to answer the shopper's real objection (shipping cost, fit, return window), not generic urgency copy.
- **R77.** Before raising a Search bid, fix the PDP or collection page it lands on: load speed, mobile checkout friction, and whether it matches the ad's promise.
- **R81.** Test AI Max only on a cold, brand-excluded campaign, so a bad match cannot burn spend on a competitor's line or a discontinued SKU.
- **R82.** Judge CPC against the store's break-even CPA and AOV, not alone; a CPC can be profitable at $150 AOV and unprofitable at $30 AOV.
- **R108.** Cap manual CPC or Maximize Clicks bids at break-even CPA divided by an assumed conversion rate, so a new account cannot buy clicks it cannot afford once a sale happens.
- **R111.** A tighter tROAS shrinks the campaign toward the store's own past buyers; watch new-customer share before tightening further.
- **R116.** Use a seasonality adjustment only for a short, store-caused spike (a flash sale, an influencer post), never a recurring calendar event like a holiday.
- **R124.** Build the account negative list from terms that never belong on this catalogue (jobs, free, wholesale, repair parts) without blocking real product searches.
- **R141.** Before changing anything, finish the sentence: this campaign's backend revenue dropped because this metric fell, driven by this sub-metric, caused by this trigger; a fix that cannot complete that sentence will not fix revenue.

## 4. Missing store levers (8)

1. **Peak-season readiness** (budget pre-raise, feed and promo updates, creative refresh on a sale calendar). Would go near 4.24. `03` has BFCM headline examples only (`[4b1f9877b48b]`); `09` warns against seasonality bid adjustments for holidays (`[44615a608690]`); no checklist exists. `[general practice]`
2. **Marketplace-heavy stores** (Amazon or Flipkart alongside the site, and its effect on Shopping bids or brand defence). Would go in 3.A. `06` states outright "No marketplace or multi-country guidance despite the subtitle." No source in this folder. `[general practice]`
3. **Subscription value tracking** (first order vs subscription LTV in enhanced conversions). Would go in 3.B and 4.4. `02` allows tCPA for "a subscription where order values are equal" (`[ed1a69221ddc]`) but gives no tracking build. Partial source; the build itself is `[general practice]`.
4. **Luxury or considered-purchase funnel** (longer research cycle, view-through weighting, an informational YouTube stage before Search). Would go in 3.A and 3.J. `08` covers luxury only for discount policy (`[38b728817a44]`). `[general practice]`
5. **Mobile-first, non-US market setup** (Merchant Center payment methods, language and currency defaults, data-cost-aware creative). Would go in section 2 and 3.D. No mention of India, INR, or any non-US, non-UK market in `sources/`. `[general practice]`
6. **Proactive inventory-to-ad coordination** (throttle spend ahead of a predicted stockout, not just react after). Would go in 3.N and 4.24. `05` and `08` cover reacting to a stockout already happening (`[4e3675b7a020]`, `[f08cac856543]`); nothing acts ahead of one. `[general practice]`
7. **New-SKU launch playbook**, distinct from bestseller cold-start, for adding 1 product to a live account. Would go near 4.11. `06/09` names "new-arrival SKUs" as a label (`[59d9f9d20e0c]`) with no launch procedure. `[general practice]`
8. **Cross-border shipping cost and duty display** in feed and ads. Would go in 3.D near R39. Same `06` gap as item 2; no source in this folder. `[general practice]`

## 5. Demotions to "General background"

- R125, negative match type mechanics (about 45 words): pure syntax, same for any advertiser.
- R76, generic RSA copywriting tactics ("imperative verbs, numbers, you, title case") (about 40 words): ad-copy 101, no store content.
- R82's opening line "CPC is a vanity metric except at the extremes" (about 25 words): true for any paid channel on its own; the store-tied rewrite above should replace it.
- R135 and R141, the top-down investigation order and root-cause sentence (about 90 words): a general diagnostic method, reusable outside Google Ads; keep a pointer in 4.25, move the method itself.
- The platform-mechanic half of R111, R112, R115, R117 (about 180 words): plain description of how tROAS, portfolio bidding and smart bidding exploration work as features, separate from the store-specific numbers, which stay in section 3.

Total: roughly 380 words of 31,564, under 2%. Not a bloat problem, just a small tail of platform mechanics that reads the same for any advertiser.

## 6. Deliverables check (section 9)

All 6 are things a store team would use: a diagnosis tied to backend revenue, ready-to-load exclusion lists, a campaign map with a reason per split, a per-SKU feed fix list, an AOV-and-margin budget proposal, and a test plan tied to the playbook's own conflicts. None are generic report templates. Two changes: rename 9.1 "Account diagnosis" to "Google Ads root-cause report" so it reads as a decision, not a data pull; and add a "Peak-season readiness" deliverable once item 4.1 gets a sourced procedure, since nothing today would catch a store unprepared into a sale period.

## 7. The single highest-value change

Add section 3.0, the priority order drafted above, and keep it current. This playbook holds 143 well-sourced rules and 7 explicit conflicts, more Google Ads knowledge than most operators carry, but it asks the reader to already know which of 12 sub-topics matters first for their store. A single-hero-SKU brand, a discount catalogue brand and a subscription brand should not start in the same place, and nothing today says where each one starts. A ranked, conditioned entry point turns a very good reference into a usable operating sequence, which is the difference between a playbook and a search engine over 143 rules.
