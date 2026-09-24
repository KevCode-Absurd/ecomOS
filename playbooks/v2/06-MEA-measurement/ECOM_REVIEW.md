# Ecommerce specificity review: 06-MEA-measurement

Reviewer read `TEMPLATE.md` and the full `PLAYBOOK.md` (about 24,256 words). No paid or web calls used. `PLAYBOOK.md` was not edited.

## 1. Score: 3 out of 5

Reasoning: sections 0, 1, 2 and 9 are built for a store from line 1 (checkout domain, top metric, order reconciliation, revenue definitions), and groups E, J and M turn generic tools into store rules (ecommerce events, Shopify constraints, net sales plus shipping). But close to half the 95 rules are GA4, GTM and Meta admin mechanics with no store framing, the kind any SaaS or publisher property would also need, and the top-metric and qualitative-research groups read as general business strategy.

Rule count by type, out of 95 rules in section 3 (R1 to R95):

- (a) Store-specific: 32. Example: R25, R26, R51, R60-65, R73-78, R86-90.
- (b) Generic principle applied correctly to a store: 17. Example: R1, R2, R4, R44-46, R55-57.
- (c) Generic with no store framing: 46. Example: R7, R9, R15-19, R33, R48-50, R58, R66-69, R79-81, R84, R85.
- (d) Out of scope (B2B, SaaS, publisher, enterprise): 0.

No rule here targets a non-store business. The gap is generic tutorial mechanics (mostly S01, S03, the 2 GA4 beginner tutorials) carried over without a store lens.

## 2. Prioritisation check: no priority block exists

The playbook groups rules by sub-topic (GA4 admin, Meta pixel, Shopify, UTM, attribution, reconciliation, top metric, funnel, trust) and by task in section 0's load table. Neither ranks levers by value to a store, and neither carries conditions by store type (hero SKU vs catalogue, low vs high AOV, subscription vs one-off, marketplace-heavy, luxury or considered purchase, mobile-first India vs US). Section 7 never resolves into a ranking either. Draft block below.

### 3.0 Ecommerce priority order (draft)

1. Confirm ecommerce events arrive (view_item, add_to_cart, begin_checkout, purchase with value, items, transaction_id) before trusting any other number; nothing below works without it. R25, R26, P6.
2. Purchase is the only sales key event, counted once per transaction, never a thank-you page view. R26 to R28, C1.
3. Reconcile GA4, Meta and Shopify purchase counts and revenue to store orders, same dates and channel; the trust layer every other read sits on. R73, P21.
4. Meta pixel plus CAPI redundancy and dedup, checked per event type, not just PageView; ad-driven stores mis-state spend efficiency without it. R44 to R47, P9, P11.
5. Revenue definition fixed: net sales plus shipping, tax out, returns on refund date; every triage and reconciliation number depends on this first. R74, R75.
6. Sessions x conversion rate x AOV triage, on 1 basis, before anyone names a cause for a sales move. R76, R77, P19.
7. Shopify constraints: GTM does not run in checkout, Shopify sessions include bots, AOV excludes shipping; skipping this misreads the store's own dashboard. R60, R61, R65.
8. UTM and channel tagging discipline for the store's paid mix (Meta, Google, affiliate, email); bad tags break every read below this line. R66 to R68.
9. Daily trust check published before any other agent reads yesterday's numbers. R92, P22.
10. Set the top metric (customers, revenue or profit) by store stage and offer: hero-SKU or early-stage runs on customers, catalogue or repeat-heavy can run on revenue or profit, subscription stores need a repeat or renewal view alongside it (subscription not sourced, `[general practice]`). R79 to R81.
11. Funnel benchmark by store type: use the brand's own history first; S06's 2:1:1 fits low-ticket or FMCG, not luxury or considered-purchase stores with longer paths (R69 windows matter more there). R87, R38.
12. Platform vs self-reported attribution rule, written once, more urgent for marketplace-heavy or mobile-first stores where platform tracking is weakest (`[general practice]` for the geography point). R69 to R71.

Store-type conditions the sources do state: FMCG or low-ticket funnel target (R87), fashion return timing (R75), consent by selling country (R22, R52). Conditions marked `[general practice]` (subscription framing, luxury path length, marketplace and mobile-market tracking) are reviewer inference.

## 3. Rule rewrites (15)

Condition, sources and card ids unchanged; wording only, naming a store decision.

1. **R3.** Add: close with a store action (restock a SKU, pause or scale a channel, change an offer, fix a funnel step), never "keep monitoring".
2. **R6.** Replace the $1M/$100M illustration: match analytics effort to the store's own ad spend tier; a $5K/month Meta spender needs no $10M brand's data team.
3. **R7.** Add: an agency running several brands never merges 2 brands into 1 GA4 account to save setup time.
4. **R9.** Add: a subscription portal or wholesale storefront still shares 1 web stream with the main site if a shopper crosses both.
5. **R19.** Add: 14-month retention is what lets a store compare this BFCM week to last year's; do not find this out the week after peak season.
6. **R33.** Add: Traffic acquisition tells a store whether yesterday's Meta or Google spend earned its sessions; User acquisition is a brand or LTV read, not a spend decision.
7. **R34.** Add: read channel then medium then campaign whenever the question is "did this ad set or email send work", which is most of a store's marketing questions.
8. **R41.** Add: never let an AI summary decide a store's ROAS, reorder or channel-kill call; check it in the underlying report first.
9. **R66.** Add: cover every paid and owned link a store sends (Meta, Google, affiliate, influencer, email, SMS), not only the ad platforms.
10. **R69.** Add: expect the Last Click vs Data Driven gap to be largest on stores running Meta and Google Ads together; report it per channel before either loses budget.
11. **R79.** Add: a hero-SKU or pre-launch store usually runs on customers; a catalogue store with margin runs on revenue or profit; name which case the brand is in.
12. **R80.** Add: a store still finding product-market fit chases customers even at a CAC loss; a store past that point chases revenue then profit.
13. **R84.** Add: when a HiPPO wants a PDP or offer change on opinion alone, propose the test the store can run (a hero image swap, a shipping threshold change), not an abstract "test it".
14. **R91.** Add: for a paid channel, check the ad's promise (price, offer, product) against the landing page before adding spend; for organic, check the page against the search term.
15. **R95.** Add: pair a cart or checkout drop with a session recording, a post-purchase survey verbatim, or a support ticket, not a generic interview.

## 4. Missing store levers (8)

Grep run against `sources/*.md` per topic.

1. **Cart and checkout abandonment tracking and recovery.** Grep for "abandon" hits nothing in the 7 sources. Goes in group E, near P6. `[general practice]`.
2. **A working repeat purchase or new-vs-returning revenue framework.** R64 only warns Shopify's returning customer rate misleads; no replacement is given (cohort reading sits in 20-FIN). S02's file admits "missing: formulas for CAC, LTV, ROAS" (line 201). Goes in group M, pointing to 20-FIN. Partial source, otherwise `[general practice]`.
3. **Subscription or recurring-revenue event modelling** (renewal event, MRR, churn date). S02's beauty box mention (line 162) is a homepage-test anecdote, not a method. Goes in group E, new sub-group. `[general practice]`.
4. **Marketplace and omnichannel purchase measurement** (Amazon, TikTok Shop, Instagram Shop, Shopping feed). R63 only filters Shopify's own channels out of paid-media reads; no source covers a marketplace feed. Goes in group M, near R73. `[general practice]`.
5. **Inventory or stockout-aware conversion reading.** A sold-out SKU causing a false conversion drop is not covered; only sell-through appears, routed to 20-FIN (S06, `[37f16297a48e]`). Goes in group O, near R86 to R91. Partial source, routed elsewhere.
6. **SMS as a measured channel.** Grep for "SMS" and "text message" hits nothing; email gets a neighbour folder, SMS is not even named as out of scope. Goes in section 1's "does not cover" list. `[general practice]`.
7. **Seasonal or peak-period measurement adjustments** (BFCM day-over-day reads, flash-sale timeout behaviour, holiday attribution windows). Black Friday appears only as a flavour example in R34, never a rule. Goes in group F. `[general practice]`.
8. **Post-purchase upsell and cross-sell revenue attribution.** S02 names it only as 1 AOV lever (line 53, `[5869b757b0e7]`), no event or reporting method. Goes in group E, near R32. Partial source, no method.

## 5. Demotions to an appendix "General background"

- **R6** ($1M/$100M decision-sizing illustration), about 60 words: business-sizing opinion, not a store rule.
- **R72** (zero, first and third-party data tiers), about 90 words: general data-governance framing; keep the CRM instruction, move the taxonomy.
- **R84** (HiPPO, "data reveals its position"), about 40 words: decision-culture advice with no store mechanic.
- **R85** (compounding vs incremental vs one-off, with the flawed arithmetic), about 70 words: generic classification, already flagged as wrong arithmetic in R1 and C13.
- **R95**'s general heuristics (founders call 1 customer a week; top 3% loyal, bottom 3% haters), about 100 words: startup customer-development wisdom, not a measurement rule; keep the pairing instruction.
- The "predictive analytics replaces hand analysis" aside in R41's notes (S02's AI forecast, no tool named), about 50 words: speculation, nothing to act on.

Total: roughly 400-450 words of section 3 is general business philosophy, not a store rule.

## 6. Deliverables check (section 9)

This domain's job is trust, not creative output, so audit tables, fix lists, trust scores and a settings log are the right deliverable, closer to an ops runbook than a campaign brief, and that fits the job. 9.4 (CAPI enrichment spec for gross profit and COGS) is genuinely store-specific, tied to margin-based bidding. 9.5 (report reads) is decision-oriented and correctly ecommerce-framed.

Gap: every deliverable in 9.1 to 9.6 is written for a technical operator (developer, GTM editor, Meta admin), none for the brand owner in plain terms. Add "9.7 Measurement health snapshot for the brand owner": 1 page, plain English, the trust score per source, the reconciliation gap in dollars, and the 1 thing to fix this week, no jargon. This turns the daily trust check (P22) into something a non-technical owner will read.

## 7. The single highest-value change

Add section 3.0 (the priority order above) and require every "which sections to load" row in section 0 to name which priority lever it serves, and under what store-type condition it changes. Right now the playbook is comprehensive but flat: a single-SKU launch brand and a multi-SKU catalogue brand with a subscription line get the same 95 rules in the same grouping, with no signal that reconciliation and event coverage matter before UTM discipline, or that R87's funnel benchmark should not be quoted at a luxury brand at all. A ranked, conditioned priority block turns a correct but generic-in-places GA4 and Meta reference into something that tells a store agent what to fix first, which is the point of an ecomOS playbook over a general prompt.
