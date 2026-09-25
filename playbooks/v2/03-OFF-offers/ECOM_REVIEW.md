# Ecommerce specificity review: 03-OFF-offers

Reviewer read TEMPLATE.md and PLAYBOOK.md in full. No files edited except this one.

## 1. Score: 4 out of 5

This playbook is one of the most ecommerce-specific documents this format could produce. Almost every rule ties to a real store mechanism: COGS waterfall, contribution per order and per visitor, shipping cost by units in the box, cohort LTV by first-order type, cancel-flow save cost. It loses a point because it has no ranked priority section (item 2), a handful of rules import direct-mail or B2B evidence with light store translation, and Group Q (testing) reads as general CRO doctrine restated rather than offer-specific guidance.

**Section 3 rule count (R1 to R151; formulas F1 to F18 excluded, all store-specific):**

| Category | Count | Share |
|---|---|---|
| (a) Store-specific | 124 | 82% |
| (b) Generic, correctly applied to a store | 20 | 13% |
| (c) Generic, no store framing | 7 | 5% |
| (d) Out of scope for a store | 0 | 0% |

No rule is purely B2B, SaaS, publisher or enterprise content: section 1's scope note already routes that material out. The 7 in (c) are R25, R26, R30, R36, R38, R61 and R144: pricing psychology or direct-mail evidence (Kennedy's price quote, old premium-versus-discount mail tests, price-ending tests) kept mostly as-is. The 20 in (b) cluster in Group A (value equation, R1 to R3, R5, R6, R8, R10), Group P (naming, R138 to R140) and Group Q (testing, R142, R143, R145, R147), where a generic framework or CRO principle is mapped onto a product or page but is not itself store-native.

## 2. Prioritisation check: missing. Draft block below

The playbook has no ranked "what matters most" section. Section 0's table says which sections to load for a named task, and section 3 groups rules by sub-topic, but nothing ranks levers by store type. An agent with no task named cannot tell that costing the current offer beats naming it, or that a low-AOV single-SKU brand should fix structure before a pop-up. Draft:

**3.0 Ecommerce priority order**

1. Cost the current offer in full (waterfall, CP per order and per visitor, break-even ROAS); every later lever is judged against this baseline. R13, R14, P1.
2. For a single hero SKU at low AOV, fix basket structure before spending more on ads; a $14 to $25 CAC cannot sit on a $14 order. R21, R41, R44.
3. Decide the new-versus-one-time-versus-subscription split; the subscriber LTV gap is the largest lever the sources measured. R23, R75.
4. Build the subscription buy box (front-loaded discount, gated kit, pre-selected plan) for a consumable with proven repeat use. R76 to R82, P9.
5. Build the quantity ladder for shelf-stable, multi-unit catalogue products; it is funded by shipping, not margin. R41 to R49, P5.
6. Cost a gift or bonus before deepening a discount; a low-landed-cost item usually beats an equal percent off. R53, R54, P6.
7. Set cart thresholds from the order-value distribution, not the mean. R62 to R64, P7.
8. Fix the guarantee and risk reversal, especially for a considered or high-ticket purchase (jewellery is one). R101 to R104, P14. `[general practice]`: for luxury stores this should outrank rungs 2 and 5, since trust, not price, is the blocker.
9. For a fixed-offer brand, run the presentation audit; it is the entire lever available once price is fixed. R133 to R137, P19.
10. Fix the pop-up and first-order offer; cheap to change, often the weakest surface on the site. R125 to R130, P17.
11. Score and place upsells, cross-sells and post-purchase offers; smaller lift, near-free once the core offer works. R68 to R74, P8.
12. Add honest scarcity, urgency and cancel-flow save offers only once the above are in place; framing and retention, not a substitute for structure. R111, R94 to R98.

Store-type notes: a marketplace-heavy brand inserts marketplace coupon and listing-title mechanics between rungs 5 and 9, since the platform controls layout `[general practice, see item 4]`. A mobile-first India store weighs rung 8 higher, since COD trust friction is common there `[general practice]`. A catalogue brand runs rung 1 per SKU family, not per SKU.

## 3. Rule rewrites (15)

Condition, sources and card ids stay unchanged; only the rule sentence is reworded to name the store surface it acts on.

- **R25.** Match a competitor's price only if your landed cost per unit (F1) is close to 1/10th of theirs; check before matching a shopping-feed or marketplace price.
- **R26.** A low headline price can read as low quality on a PDP; test a higher price with a positioning change (audience, hero image, bundle) on the product page, not the price line alone.
- **R30.** Before a real price rise on a live SKU, notify active subscribers and cart abandoners, and update the price in every running ad and PDP so no channel shows a stale price at launch.
- **R36.** A free sample, extra unit or usage credit tied to the product can beat an equal cash discount at the same cost; test this in the pop-up or win-back flow (P17, P13), not the old mail-test result.
- **R38.** Treat odd-numbered discounts and price-ending changes ($X.99 versus a round figure, or the nearest round number in INR) as low-priority copy tests, run only after tier, gift and guarantee structure is settled.
- **R61.** When a tier or welcome kit carries 2 gift items, give each a distinct job instead of making the buyer choose one on the PDP or at checkout.
- **R90.** Before redesigning a subscription buy box, walk the brand's own PDP, cart, checkout, confirmation email and first unboxing as a customer would, and call real subscribers or people who cancelled.
- **R106.** A guarantee does not fix a PDP that overclaims or a checkout that loses orders to friction; if refund rate is high, check the product page and reviews first.
- **R110.** A short, broad guarantee suits a low-ticket, one-off purchase; for jewellery-grade or high-ticket items, size length and conditions from the store's own return-cost model (F8) and statutory rights.
- **R124.** A loss-leader SKU is allowed only when the store already has the next purchase built (a bundle upsell, subscription offer or 14-EML flow) to route the buyer into, with the loss capped against cohort contribution.
- **R138.** Name the offer using the buyer's outcome and, on a marketplace listing, the exact terms buyers search for; test names in the PDP title, ad headline and pop-up, not only in ads.
- **R139.** Run a candidate name as the PDP title at the same time as the ad-headline test; a name buyers never see on the page will not be helped by an ad test alone.
- **R140.** Build the value comparison on the PDP itself (per-unit or per-day cost against a real alternative the buyer already spends on) before the price appears, not only in ad copy.
- **R144.** Hold ad creative and landing page fixed while testing an offer change on the same SKU so any lift can be credited to the offer; test both together only when hunting a new combination.
- **R146.** Expect most offer tests on a store's own traffic to lose or tie; keep a backlog of untested ideas per SKU so the team is not stalled on one.

## 4. Missing store levers (6)

- **Cash-on-delivery or payment-linked offers** (prepaid discount, or a COD fee waiver above a basket size). Goes in Group D near R31 to R40. No source here, `[general practice]`; relevant to Gehna's India, mobile-first checkout.
- **Customer referral offers** (give X, get X, distinct from the affiliate/partner idea in P22 step 4). Would go near Group N. No source here, `[general practice]`.
- **Marketplace deal mechanics** (Amazon or Flipkart coupons, Lightning Deals, Subscribe and Save, fee-adjusted margin). Only R9's routing note and R138's search-term line touch marketplaces; `10-applying-100m-offers-to-e-commerce-i-m-pissed.md` [44778b53f7ea] covers naming only. Mostly `[general practice]`; route to 12-GAD/24-DEP with a stub here.
- **Loyalty points shown at risk in the cancel flow.** In the sources but not its own rule: `05-the-100m-subscription-brand-playbook.md` [1ae7b0ed8e41] ("show the points they would lose") and `06-i-studied-every-ecommerce-offer-so-you-don-t.md` [d5d7d14f51e0] list it among "cheaper but weak" levers, flagged "named only". Belongs in P12 beside the founder-video and matched saves.
- **Festival and peak-calendar offer planning** (BFCM, Diwali, EOSS, Republic Day). Partial source: `03-the-most-valuable-subscription-video-you-ll.md` [35bed5b98d94] covers BFCM and subscriber collision, but no India festival calendar exists here. Extend P16 with a calendar table; the India half is `[general practice]`.
- **A store-credit bonus for exchange over refund.** Store credit appears only as pop-up framing (`07-i-studied-every-100m-ecommerce-offer-so-you-don.md` [db90a9c32f90] [e54276a5821f]), not a returns lever. Extend Group K near R108. No source here, `[general practice]`.

## 5. Demotions to an appendix "General background"

- **R36** (about 80 words): the MCI "30 free minutes" and business-gift-firm examples are old B2B and consumer direct-mail results, no ecommerce translation beyond "test it". Keep the rewritten rule; move the raw evidence.
- **R61** (about 40 words): the "two premiums" direct-mail evidence (Bly) has no store example. Move the citation; keep the rewritten rule.
- **R25's Kennedy quote** (about 50 words): "no strategic benefit to being second cheapest" is general positioning advice, no store mechanism beyond the rewritten rule.
- **R26's software-tool example** (about 40 words): the $79 to $129 software case is not a physical product. Keep the rewritten PDP rule; move the example.
- **R137's 2008 web-design stats** (about 30 words, form-field abandonment, button-colour test): already flagged stale in section 10.2; drop from the 5.2 checklist row, keep the rewritten rule.

Total: about 240 words moved, none load-bearing.

## 6. Deliverables check (section 9)

All 5 deliverables are store-usable, not generic documents: 9.1 is a costed offer-options table (an offer ladder), 9.2 a ranked PDP-to-checkout fix list, 9.3 a promotion plan with stop rules, 9.4 a subscription buy-box spec, 9.5 a test proposal for 09-CRO. No renames needed. One gap: none hands 07-LPG a ready-to-paste PDP copy block (price, tier labels, guarantee, delivery promise); P19 and P20 audit but do not produce it. A 9.6 "PDP offer block" would close that.

## 7. The single highest-value change

Add the ranked "3.0 Ecommerce priority order" drafted in item 2. The playbook is an excellent reference library keyed by task name, but gives an agent no way to decide what to work on first with no task named, or to weigh a luxury store's guarantee problem against a low-AOV store's structure problem. Without that ranking, an agent under time pressure could spend equal effort on a low-leverage item (naming, P23) and a high-leverage one (the COGS waterfall, P1), the exact generic-prompt failure this playbook otherwise avoids. A ranked, store-type-conditioned order turns the library into a decision procedure, the one thing a generic prompt for a store could not produce on its own.
