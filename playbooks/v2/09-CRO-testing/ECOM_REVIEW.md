# Ecommerce specificity review: 09-CRO-testing

## 1. Score and rule count

Score: 4 out of 5.

The playbook earns this because its 2 richest sections, page-level rules (3.10, 33 rules) and the diagnostic checklists (5.2 to 5.6), are built entirely around a Shopify store's own pages: home, collection, PDP, cart, checkout and mobile, with real thresholds (44px tap targets, under 10% of AOV in checkout extras, 4 hero questions on a phone) and Shopify-specific limits (checkout extensibility, plan tiers). It loses a point because much of the middle, sample size, peeking, SRM, novelty and win rate benchmarks, reads like a general A/B testing manual that would say the same thing to a SaaS or publisher team. The store edge sits at the 2 ends, what to test and page-level fixes, while the statistical core stays generic.

Rule count, 137 decision rules in section 3:

- (a) store-specific: 71 rules (52%)
- (b) generic but correctly applied to a store: 13 rules (9%)
- (c) generic with no store framing: 53 rules (39%)
- (d) out of scope for a store: 0 rules (0%)

By subsection, (a) concentrates in 3.1 metrics (10 of 11), 3.10 page-level (28 of 33), 3.11 price and offer (3 of 3) and 3.12 Shopify platform (3 of 3). (c) concentrates in 3.6 sample size (7 of 8), 3.7 validity (11 of 13) and 3.3 research (11 of 22), where rules like "don't peek," "check SRM," "use PXL not ICE," or "interview customers" would sit unchanged in a SaaS playbook.

## 2. Prioritisation check

No, not as written. Section 0's task-routing table and section 3.5's traffic gates (R53) rank by orders per month, but nothing ranks levers by AOV, catalogue size, subscription vs one-off, marketplace exposure, luxury vs impulse, or India vs US. Draft block:

**3.0 Ecommerce priority order**

1. Repair defects and checkout blockers first. R50, R16, R123. Costs every store type; matters most on considered-purchase or luxury sites where one lost sale is expensive.
2. Read the funnel for the biggest weighted leak. R12, R13. For a single-hero-SKU store the "page" is usually the PDP; for a catalogue store it can be collection or search.
3. Diagnose traffic-mix effects before touching a page. R15. Matters most for ad-driven, cold-traffic stores; less for repeat or organic-heavy stores.
4. Mobile-first audit and fixes. R124. Highest for mobile-first markets (India, Southeast Asia) at 80 to 95% mobile share; lower for a desktop-researched, high-ticket purchase. `[general practice]` for the desktop case.
5. PDP: 4 hero questions, proof and CTA above the fold. R101, R102. Top for single-hero-SKU brands, where the PDP does the homepage's job; shares priority with collection UX on a catalogue store.
6. Checkout friction removal: guest checkout, express pay, fewer fields, upfront costs. R116 to R119. Highest for low-AOV, impulse, cold-traffic stores; lower once a luxury buyer has already committed.
7. Cart economics: free-shipping threshold and bundle upsell tuned to AOV. R114, R131. High for low-to-mid AOV catalogue stores; does not apply to a single-SKU subscription store, which has no "add more items" lever. `[general practice]`.
8. Proof and review strategy matched to store maturity. R104. Very high under 100 reviews (build volume); drops toward relevance once mature.
9. Message match from ad to landing page. R108. High for paid-social acquisition; low for repeat, email or retail-driven stores.
10. Price and offer construction: no same-SKU price tests, prefer bundles and tiers. R129 to R131. High for promo-heavy, multi-SKU catalogues. No offer content here for subscription plan tiers. `[general practice]`.
11. Traffic-gated test aggressiveness by order volume. R53, R59. Governs how hard every lever above can be tested; binds tightest for low-order, single-SKU or marketplace-heavy stores.
12. LTV and guardrail check before scaling a winning angle. R84. Last gate before spending against a win; most critical for claims-driven categories (health, beauty).

## 3. Rule rewrites (up to 15)

Condition, sources and card ids stay unchanged; only the rule wording changes.

1. **R14**: A funnel drop on the PDP, cart or checkout step shows where shoppers leave, not why. Watch recordings, read heatmaps, or survey that exact step before writing a hypothesis.
2. **R20**: Every PDP, cart or checkout hypothesis needs 2 points of store evidence: one quantitative (a funnel rate, a heatmap, an add-to-cart rate) and one qualitative (a survey answer, a review theme, a recording).
3. **R38**: Pick Clarity, Hotjar or Okendo by the store's daily session volume and Shopify plan tier. A single-SKU store under a few hundred daily sessions should default to Clarity's free tier before paying for an all-in-one platform.
4. **R45**: Score PDP, cart and checkout hypotheses with PXL-style evidence gating, not ICE, because the merchandiser or founder who pitched the idea will otherwise score their own PDP change 9 out of 9.
5. **R46**: Put above-the-fold PDP and homepage changes (hero, price, CTA) ahead of below-the-fold collection filters, because most shoppers decide to buy before they scroll on a phone.
6. **R55**: Treat any "we changed the PDP and revenue went up" comparison as biased. Promos, restocks and seasonal demand move orders exactly like a real page change would.
7. **R58**: Never run 2 tests on the same PDP at once. A homepage test and a cart test can run together because they touch different steps in the funnel.
8. **R60**: State every sample size as orders per variant, not sessions or clicks, because orders are what a store's finance team and P&L track.
9. **R70**: A checkout tool that reports "significant" is not enough. Size the checkout or cart test yourself from the page's weekly order volume first.
10. **R75**: Pre-register mobile vs desktop and cold-paid vs returning before reading any PDP or checkout result, because a mobile checkout fix can lose on desktop and still look like a blended win.
11. **R83**: Read the mobile PDP or checkout number before shipping. On a mobile-first India or Southeast Asia store, a desktop-only lift is not worth shipping.
12. **R86**: Do not promise a founder more than 1 in 5 to 1 in 10 PDP, cart or checkout tests will beat control. Set the expectation against ecommerce agency figures (DRIP, ConversionTeam), not tech-platform case studies.
13. **R10**: Judge a CRO retainer by incremental revenue or margin against a holdout of the store's own traffic, not by how many PDP or checkout tests were shipped that month.
14. **R37**: Call recent buyers of the flagship SKU, or a random sample across the catalogue, and ask why they bought, whether checkout was easy, and what words they used for the product.
15. **R136**: Run only as many PDP, cart or checkout tests a month as the store's weekly order volume can power, with no 2 tests overlapping one page. A single-hero-SKU store under 300 orders a month should run 1 bold test at a time, not a weekly cadence.

## 4. Missing store levers (up to 8)

1. **On-site search** (autocomplete, no-results handling, search-to-purchase rate). New 3.10 "Search" subsection. No source in this folder. `[general practice]`
2. **Marketplace-lite stores** (a DTC brand also on Amazon, Flipkart, Meesho or Instagram/WhatsApp). Goes in section 1 and 3.0. No source; "marketplace" in `06-cro-fundamentals.md` line 159 means a platform like Uber, not this. `[general practice]`
3. **Subscription mechanics** (pause, skip, swap, cancel-flow saves), distinct from one-off CRO. New 3.10 subsection. Thin source: `02-cro-masterclass-2026.md` line 160 names a "subscription funnel" once; `06-cro-fundamentals.md` gives a SaaS/subscription conversion band with no ecommerce framing. Mostly `[general practice]`.
4. **Size guides and fit tools** for apparel, to cut size-driven returns. Goes in 3.10 PDP. No source in this folder.
5. **Buy-now-pay-later badges** as a PDP and cart AOV lever. Goes in 3.10 PDP or Cart. Buried source: `02-cro-masterclass-2026.md` section 6 names "Afterpay-style instalments: 'why now' lever" with no card id and no rule built on it.
6. **Loyalty and rewards programmes** and their effect on repeat purchase. Near 3.9 or 3.13. Only mention: `06-cro-fundamentals.md` line 164, loyalty tiers as a statistics example, not ecommerce content. `[general practice]`
7. **Legitimate scarcity and back-in-stock testing**, distinct from the warning against fake scarcity. Goes in 3.10 PDP or Collection. Partial source: `03-cro-framework-conversion-wise.md` line 109, card `6f635b9d003d`, "low in stock" as one label example, no dedicated procedure.
8. **Localisation beyond payment method**: currency display, cash on delivery, GST-inclusive pricing, language. Goes in 3.10 Checkout, next to R118. No source beyond the UPI line.

## 5. Demotions to a "General background" appendix

1. Causal-method definitions in R94 and P23 (difference-in-differences, regression discontinuity, propensity matching, synthetic control, switchback), about 350 words. Generic statistics, already routed to 06-MEA; keep the routing line, move the definitions.
2. The peeking-simulation narrative in R67 and R68 (Evan Miller, Kohavi, Etsy, Molas percentages), about 300 words. Keep the operating rule (do not peek, use a named engine); move the study history.
3. The ICE/PIE/PXL/RICE debate in R45, about 150 words. Used in every industry. Keep the chosen method (PXL plus profit ranking, R44); move the comparison.
4. The tech-platform win-rate roll call in R86 (Microsoft, Bing, Booking, Netflix, Airbnb, Optimizely, VWO, CXL), about 150 words. Most are not DTC stores. Keep the ecommerce-agency figures (DRIP, ConversionTeam) and the 10 to 20% anchor; move the rest.
5. The full stats-engine vendor roster in R134 (VWO, AB Tasty, Convert, Kameleoon, Optimizely, GrowthBook, Statsig, Eppo), about 150 words. Keep "confirm the vendor's engine and SRM alert before committing"; move the vendor detail.

## 6. Deliverables check

Mostly yes. Of 13 deliverables in section 9, most are things a store team would open and use: a funnel memo built on corrected Shopify and GA4 numbers, PDP, cart and checkout audit reports using the section 5 checklists, a test brief with real sample size, a live-winner register, and a holdout readout in RPV. These are tied to Shopify data and store pages, not generic CRO reports.

Two are weaker. "Hypothesis backlog (leaderboard)" is a generic project-management label even though its content is store-specific; rename it "PDP, cart and checkout test backlog." "Measurement design recommendation" is really an internal routing note, not something to hand a store owner; rename it "test vs holdout routing note."

## 7. The single highest-value change

Add the missing "3.0 Ecommerce priority order" and condition every major lever by store archetype: single hero SKU vs catalogue, low vs high AOV, subscription vs one-off, marketplace-heavy, luxury or considered purchase, and mobile-first India vs US. The playbook is comprehensive and well sourced but store-neutral in structure: it tells the agent how to run CRO for any Shopify store, and leaves it to work out, task by task, which lever matters most for this store. A short block that says "for a single-SKU mobile-first India store, do X before Y; for a multi-category US catalogue store with subscription SKUs, do Y before X" would turn 137 well-evidenced but flatly ranked rules into an actual decision aid, and it is the one change a generic-model user would notice in the first 5 minutes of use.
