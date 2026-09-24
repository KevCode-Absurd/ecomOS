# Ecommerce review: 07-LPG landing pages playbook

Reviewed against `TEMPLATE.md` and the full `PLAYBOOK.md` (1,142 lines, 133 decision rules in section 3).

## 1. Ecommerce specificity score: 4 out of 5

The playbook does what a general prompt cannot: it names 5 store page types (PDP, cold LP, advertorial, quiz, sales page) with different rules for each, ties every metric to purchase conversion, RPV and contribution instead of leads or calls, and flags rules borrowed from lead-gen sources as "card adaptation" so the agent knows they were never tested on a store. Its weak spot is volume: most of the 133 rules are direct-response copywriting or CRO craft from lead-gen or info-product courses that keep that generic shape even where a store detail was available. It earns the 4th point for this self-honesty and 5 fully store-native sections (PDP, homepage and collection, offers, cart, nav); it misses the 5th because a reader still has to translate close to half the rules into "so what for a store" themselves.

**Rule share, section 3 (133 rules, counted by rule id):**

| Class | Count | Share |
|---|---|---|
| (a) store-specific | 30 | 23% |
| (b) generic, correctly applied to a store | 44 | 33% |
| (c) generic, no store framing | 56 | 42% |
| (d) out of scope for a store | 3 | 2% |

(a) clusters in 3G offers (6 of 8), 3H.2 to 3H.3 nav and cart, 3D.3 to 3D.5 campaign, PDP and homepage, and 3L quiz-to-SKU routing (5 of 12). (c) clusters in 3E copy craft (8 of 11), 3I mobile UX (5 of 7), 3J page length (all 3), 3K advertorial craft (9 of 12) and 3O test methodology (4 of 6). The 3 (d) rules: 3A.9 and 3K.12 (publisher content, kept separate) and 3F.9 (case studies, whose condition names B2B first).

## 2. Prioritisation check: no ranked block exists

Section 0's task table says which sections to load per job; section 7 ranks conditions inside single conflicts. Nothing ranks levers against each other for a given store. Draft below, built only from this playbook's rules and section 7, ranked by how much purchase rate or RPV a lever can move and how early it must be decided. `[general practice]` marks a ranking judgment, not an unsourced rule.

**3.0 Ecommerce priority order**
1. Route traffic to the right page type first (3A.1 to 3A.9): PDP direct for a single hero SKU (3A.1, 3A.3); advertorial or quiz for a considered, high-AOV, cold offer (3A.2, 3A.7, 3A.8); catalogue brands decide per SKU. Wrong routing wastes the whole build.
2. Match the page to the ad's exact promise, persona and offer (3B.1 to 3B.3), the single most agreed rule in the folder; cheap to fix and the first check for every store type.
3. Build the PDP first screen to spec (3C.9, 3D.4, 4.4) before anything else on a catalogue store, where most traffic lands; rank lower for a single-SKU brand.
4. Fix the weakest GA4 funnel stage first, not the whole funnel (3N.2). `[general practice: triage order]`
5. Put real FUD reducers under the CTA and add to cart, word for word to policy (3C.8, 3G.6); higher for new brands and COD or low-trust markets.
6. Show bundle savings in money, cap tiers at 3 (3G.1, 3G.2); high for multi-pack or subscription brands, irrelevant for single-unit ones.
7. Build and QA mobile first (3I.1, 4.17); highest for a mobile-first market like India.
8. Cart drawer with no reload and real upsells (3H.3), a low-cost, store-wide lever once traffic and PDPs are fixed.
9. Build an advertorial or quiz only after a winning ad or research base exists (3A.4, 4.6). `[general practice: sequencing]` Skipping this is the most named mistake for this page type.
10. Scatter proof and objection-matched reviews at the buy box and drop-off points (3F.2, 3F.3); higher where trust is the blocker.
11. Score and queue tests by traffic, above the fold first, hand to 09-CRO with the prior's gaps stated (3O.2, 3O.3, 4.16); low-traffic pages use before-and-after.
12. Run the compliance check (5.7) before launch on any advertorial, quiz or claims page: a gate, not a lever, so it sits last.

## 3. Rule rewrites (condition, sources and card ids unchanged)

| Rule | Generic wording now | Store-specific rewording |
|---|---|---|
| 3C.2 | Headline states the dream outcome | State the outcome this SKU delivers, not the category, with only numbers that SKU's own PDP and reviews back |
| 3E.1 | Every heading states the benefit | Name the shopper's payoff for this line, not the department label ("Our Ingredients" becomes "What's in your jar and why it works") |
| 3E.3 | Benefits before features | Lead with the benefit a shopper uses to pick between 2 open comparison tabs; the spec backs it up, not headlines it |
| 3D.6 | Pain section: problem, agitate, solve | Open on the exact shopping or product friction this SKU creates (a stain, a leak, a return trip), not a generic opener |
| 3D.9 | Comparison block vs the usual alternatives | Compare against the 2 or 3 SKUs or brands the shopper is actually price-checking in the same search or listing |
| 3F.1 | Proof must be verifiable: name, photo, date | Show the platform badge (Shopify verified buyer, Amazon verified purchase) the shopper trusts for the channel it buys on |
| 3F.4 | Prefer short video testimonials | Prioritise phone-shot UGC of the product unboxed or worn, styled like the brand's own ad, matching cold traffic's feed |
| 3I.2 | One pinned CTA on mobile | The pinned PDP CTA shows live price and saving, updates on variant tap, never covers the size or shade selector |
| 3J.1 | Length follows warmth, not word count | Scale page length by SKU tier (hero, core, tail) for a catalogue brand, not one house style for every product |
| 3K.4 | Mechanism maps to the root cause | Name the mechanism with the pack's own ingredient words, so the story never outpaces the label and unboxed product |
| 3N.1 | Analyse data before any design change | Pull that SKU's own GA4 and Clarity numbers, not a site average, since 1 slow SKU can hide behind a healthy brand rate |
| 3O.2 | A/B test only with enough traffic | Set the floor per page: a homepage may clear it while long-tail PDPs never do, so most PDPs default to before-and-after |
| 3H.1 | Dedicated pages have no navigation | Strip nav only on 1-campaign pages; keep Shop reachable elsewhere, since a lost visitor is a lost repeat purchase, not a lost lead |
| 3E.7 | Images match the paragraph, look real | Every image traces to the SKU's current photo set (color, size, packaging shipping today); a mismatch drives a return |
| 3D.11 | FAQ built from real objections | Build the PDP FAQ from that SKU's own tickets and negative reviews (runs small, scent fades), not the site-wide FAQ |

## 4. Missing store levers (up to 8)

1. **Subscribe-and-save or one-time selector on the PDP.** Goes in 3C.9, 4.4 step 3. No source here; `[general practice]`.
2. **On-site search and its results page as a lever.** Goes in 3D.5. Source 01 mentions search only as a place to mine objections `[3f57d3484974]`; the feature itself is `[general practice]`.
3. **Delivery ETA or pincode serviceability check.** Goes in 3C.8, 4.4 step 6. No source here; `[general practice]`, and most useful for a mobile-first India store.
4. **Local payment trust signals (COD, UPI, EMI, buy-now-pay-later) matched to the market.** Goes in 3C.8, inputs row 16. Source 15 names this gap directly; card `[716414ea8582]` is a card addition; beyond returns and shipping it is `[general practice]`.
5. **A distinct page for repeat or loyalty customers** (skip persuasion, direct reorder). 3A.1 routes repeat buyers to the PDP but does not design what changes for them; `[general practice]`.
6. **A frequently-bought-together module on the PDP**, separate from the cart-drawer upsell `[af92a8953b92]`; `[general practice]`.
7. **A dedicated size or fit guide module.** Source 15 names sizing as a missing FUD item, card `[716414ea8582]`; format is `[general practice]`.
8. **A real-time low-stock display on live inventory.** 3G.5 `[ba6079d8e9e9]` bans fake scarcity but does not design the UI itself; `[general practice]`.

## 5. Demotions to an appendix "General background"

- **3K.12 and its mention in 3A.9** (publisher sponsored content, source 26 only, about 90 words): publisher-media practice, not a brand's own page; already kept separate, so moving it out removes about 150 words of non-store content from section 3.
- **3F.9 case studies** (about 60 words): its condition names B2B and high-ticket first, reading as carried from an agency source, not written for a store.
- **The unverified web-psychology statistics in section 6** ("50 ms first impression", "20% read, 80% scan", "60,000x faster than text", "90% visual", "4.7 to 4.9 beats 5.0"): about 6 rows, 120 words, none store facts, already flagged unsourced there and again in 10.2.
- **3M.4's order-bump price and 3M.5's OTO "10x front end" heuristics** (about 185 words): a single presenter's info-product numbers, hedged as a poor fit for durable goods; keep the store instruction (contribution per buyer, real add-on service) and demote the numbers.

## 6. Deliverables check (section 9)

The 5 deliverables are things a store team would use: a PDP or LP audit with checklist evidence (9.1), a wireframe with real copy and image direction (9.2), a full advertorial draft in a fixed block order (9.3), a quiz spec a builder can implement (9.4), and a test proposal for 09-CRO (9.5).

Two changes would sharpen them. Split 9.2: a PDP rebuild follows the fixed template in 3C.9 and needs a short "PDP brief" (gallery plan, buy-box order, FUD list, bundle block), not the long-form wireframe built for a cold landing page. Turn 9.5 into a small ranked backlog, not 1 proposal: 4.16 already scores every candidate test with a PXL-style sheet and runs the highest first, but the deliverable writes up only 1 hypothesis at a time.

## 7. The single highest-value change

Add the "3.0 Ecommerce priority order" block. The most consequential decision for a store, which page type to build and what to fix first, is buried across 9 conditions in 3A plus scattered hints in section 7, so an agent must read most of section 3 before knowing where to start. A short block keyed to store type (SKU count, AOV, subscription vs one-off, market) lets the agent read 1 page and know whether this brand's biggest lever is routing, the PDP, mobile QA or proof, before it reaches the generic direct-response rules that make up most of the rule count.
