# Ecommerce review: 16-AEO answer and generative engines playbook

Read PLAYBOOK.md in full (109 decision rules, 20 procedures, 6 checklists) plus TEMPLATE.md, and grepped the 9 mini playbooks in `sources/` for store topics. This review does not edit PLAYBOOK.md.

## 1. Ecommerce specificity score: 2 out of 5

The playbook is honest about its own weakness: section 0 states none of its 9 sources shows a measured ecommerce case, and most examples are B2B SaaS (Webflow, Gamma), a fictional EV installer, or unnamed illustrations. The mechanics (crawler access, answer-first writing, mentions, measurement) are correctly explained and often reworded for PDP and category pages, but most of the 109 rules stay at the level any SaaS or publisher would also follow, with no store-type conditions. Procedures (section 4) and the page-content checklist (5.2) are the strongest ecommerce work here; decision rules (section 3) are the weakest.

**Rule count by type (109 rules in section 3, counted by rule ID):**

- (a) Store-specific: 24 rules (about 22%). Examples: R2 (category pages, buying guides), R19 (catalog budget concentration), R24 to R30 (crawlability tied to checkout paths, SKU/collection pages, Shopify Dawn theme, Product/Offer schema), R36, R40, R42 to R44, R48, R49 (PDP, category, comparison, FAQ conditions), R69, R101 (reviews), R76 (mattress affiliate example), R85, R87 (shoppable cards, checkout survey).
- (b) Generic, correctly applied to a store (card adaptation noted): 4 rules. R33, R35, R50, R62.
- (c) Generic, no store framing: 77 rules (about 71%). Most of 3.1, 3.5, 3.7, 3.8, 3.9 and half of 3.10 sit here. Correct and usable, but say nothing a SaaS or publisher agent would not also say.
- (d) Out of scope, not reframed: 4 rules. R21 (Glassdoor hiring-review anecdote), R72 (BBB/Foursquare/Nextdoor local directories), R77 (MCP agent integration; text says "mostly outside ecommerce today"), R107 (hidden incentive text in JSON schemas, a developer-tooling risk).

## 2. Prioritisation check: no priority order exists

The playbook sequences work inside one engagement (R14: crawler check, then measurement, then gap analysis, then fix) and inside content production (R16, R19), but never ranks the levers against each other for a store, and never conditions that ranking on store type (single hero SKU vs catalog, AOV, subscription vs one-off, marketplace-heavy, luxury or considered, mobile-first India vs US). Section 7's conflicts (C2, C4, C5, C19) come closest, since they argue about sequencing by brand size and platform, but they are conflicts, not a ranked list. Draft block below.

### 3.0 Ecommerce priority order (draft)

1. Crawler access and indexing (robots.txt, Cloudflare AI-bot setting, JS rendering, GSC/Bing submission). Nothing downstream works if bots cannot fetch the store. R23, R14, R26, R27.
2. Measurement live before content work starts (GA4 AI channel, checkout survey, frozen prompt baseline). Day 1 is measured. R14, R85 to R89.
3. Brand gap analysis and prompt audit, including named competitors, to find the biggest lever first. R78, R80, R14.
4. Concentrate rewrites on the top 5 to 10 pages with traffic or links, not the whole catalog. A single-hero-SKU brand collapses this to 1 to 2 pages; a wide catalog gets the 80/20 slice. R19, R41.
5. Fix wrong or missing brand facts at the source (fact page, PDP specs, pricing, shipping, returns). R46, R47, R75.
6. Rewrite the concentrated page set answer-first, atomic, with a comparison table and a 5-item FAQ cap. R36, R37, R42, R48.
7. High-AOV or considered-purchase catalogs add buying guides and original data; low-AOV or impulse catalogs skip the guide and spend on category pages and reviews. `[general practice]`, using R2 and R44.
8. Tier-1 editorial mentions already cited for the category (listicles, comparison sites, gift guides). R63, R64.
9. Honest, unincentivised review collection on platforms buyers and engines already read. R69, R101.
10. Tier-2 community presence (Reddit, forums) in threads already cited, weighted toward ChatGPT until the brand's data says otherwise. R66, R67.
11. Comparison pages against 3 to 4 named competitors, softened for luxury or considered-purchase brands where naming a cheaper rival can cut against the position (`[general practice]`). R43.
12. Monthly share-of-voice and prompt-audit cadence, quarterly deep competitive audit. R84, R10.

Gaps this order cannot fill from the playbook: no rule distinguishes a subscription brand from a one-off purchase brand, a marketplace-heavy brand (most revenue via Amazon or a social shop, not the owned site) from a DTC-only brand, or an India mobile-first buyer base from a US one. See section 4 below.

## 3. Rule rewrites (15)

Condition, sources and card ids unchanged; wording only.

1. **R3.** The gate is whether the specific PDP or category page ranks top 10, not the domain in general.
2. **R5.** Pick platforms by where buyers do pre-purchase research relative to the catalog's AOV and consideration level, not a universal 1-to-3 rule.
3. **R9.** Track add-to-cart rate, order conversion rate and revenue per session from AI-referred sessions, not sign-ups; a store's north star is orders and AOV.
4. **R13.** The SEO foundation this protects is PDP, category and collection page ranking, not blog ranking.
5. **R17.** Niche the query down using the catalog's own attributes (size, material, use case, fit), the way "best hiking backpack" narrows to "best hiking backpack under 40 liters for thru-hiking."
6. **R21.** The same mechanism applies to a product review page: a 2-star rating on the platform an engine cites can be why the engine describes the product badly.
7. **R37.** Make PDP fact blocks (materials, sizing, care, shipping, returns) the atomic unit; each must stand alone.
8. **R38.** Name the actual product, material, model number and named competitor SKU instead of "this item" or "many users."
9. **R55.** Draw buyer questions from the catalog first: fit, sizing, compatibility with other owned products, use case, before general keyword mining.
10. **R63.** Tier-1 targets are product review sites and seasonal gift-guide listicles, which carry more weight for physical goods than the generic examples given.
11. **R72.** For an online-only store, the NAP equivalent is identical facts and price across the site, the Shopping feed and any marketplace listing, not BBB or Foursquare.
12. **R78.** The competitor set must include marketplace listings (Amazon, a marketplace's own search) alongside DTC competitor sites.
13. **R93.** Compare AI-referred order conversion rate, AOV and revenue per session against organic, not an undefined "revenue."
14. **R8.** The mentions that matter are product-specific ("the XYZ backpack"), not only brand-name mentions.
15. **R6.** An AI answer naming "brands like ours" with no PDP link is still a top-of-funnel impression, the "named but unlinked" state this rule defines.

## 4. Missing store levers (8)

1. **Merchant feed and AI shopping surfaces** (Shopping in AI Overviews/AI Mode, ChatGPT or Perplexity shopping actions, shoppable carousels). Goes in 3.3. Source 04 names shoppable carousels as a format signal [7a7c5e12d8bc] [536f2c6edb07] but states it has "no mention of Amazon, other marketplaces, paid LLM placements/ads, or platform-specific shopping-agent APIs" (`04-...md:137`). `[general practice]`
2. **Marketplace citation surface** (Amazon and other marketplace listings as a source engines cite). Goes in 3.6. Same source-04 gap note is the only material here. `[general practice]`
3. **SKU-level catalog structure**: variants, collection pagination, faceted-navigation SEO, canonical URLs. Goes in 3.3 near R35. Source 01 flags this itself: "the source itself never discusses SKU-level catalogs, product variants, collection pagination, faceted-navigation SEO, or canonical handling for filtered URLs" (`01-...md:222`). `[general practice]`
4. **Inventory and stock status** effect on citation. Goes in 3.4 near R40 and checklist 5.2. No source mentions inventory, stock or backorder. `[general practice]`
5. **Seasonal and peak-season planning** (Black Friday, gift guides). Goes in 3.2 or 3.6. No source mentions seasonal, holiday or peak season. `[general practice]`
6. **Subscription vs one-off framing** (plan/pricing facts, cancellation policy as trust signal). Goes in 3.4 near R46/R47. The only "subscription" hits are source 01's own paid community and source 02's SEO-tool subscription, both unrelated to the brand. `[general practice]`
7. **AOV and price-tier segmentation** shaping tactic choice (used in the priority draft above). Goes in 3.0/3.2. No source uses AOV or price point as a variable. `[general practice]`
8. **Regional and mobile-first platform mix** (India vs US assistant use, regional review platforms). Goes in 3.2 near R15. No source mentions India, mobile-first or a non-US market. `[general practice]`

## 5. Demotions to an appendix "General background"

- **R107**, hidden incentive text in JSON schemas or install packages aimed at autonomous agents. A developer-tooling and API-security topic, not a store lever. About 80 words.
- **R77**, MCP or agent integration as a retention play. The rule's own text calls it "mostly outside ecommerce today." About 90 words.
- **R72** plus its procedure step (P14 step 3) and diagnostic row, free local-business directory listings (BBB, Foursquare, Nextdoor Business). Only relevant to a brand with a physical retail location. About 180 words combined.
- **R21**, the Glassdoor hiring-review anecdote. A hiring-review example with no store review-platform translation (section 3 above supplies one). About 90 words.
- The B2B/SaaS-only rows in section 6's threshold table: Webflow's 6x conversion and 8% sign-ups, Gamma's referral growth from under 1% of traffic, Vercel's ~10% AI conversion, and Tally's "+$1M ARR." Sign-up and ARR metrics with no order, AOV or revenue-per-session translation; the table already marks them "Example." About 120 words.

## 6. Deliverables check (section 9)

Seven of the 9 deliverables (D1, D3, D4, D5, D6, D7, D9) are generic operational spreadsheets any AEO program would produce; usable by a store team but with no store-specific fields. D8 (vendor vetting sheet) is a fine general business document. D2, the page rewrite brief, is the standout: its fields (page type PDP/category/guide/comparison, TL;DR fact list of materials/sizing/use case/price range, FAQ cap, schema facts) are exactly what a store team would hand a writer.

Proposed changes:
- Rename D1 to "Catalog crawlability fix list" and add a page-type column (PDP, collection, guide) so fixes are prioritised by which pages drive revenue, not just by layer.
- Add a new deliverable, a **catalog citation priority list**: top revenue-driving SKUs and collections cross-referenced against citation and gap status from P3, so page-level work (D2) is ordered by what the business sells. This gives the R19 catalog-concentration rule a deliverable of its own.
- Rename D4 and D5 to "AI answer visibility test set" and "AI visibility and citation report" to match how a store team talks about traffic and citation; the fields inside are already sound.

## 7. The single highest-value change

Add the store-type-conditioned priority order (section 2 above) as a real section 3.0, and require every future rule addition to state which store type it applies to (single SKU, catalog, subscription, marketplace-heavy, considered purchase, region). The playbook's 109 rules are correct and well-organised but interchangeable with a generic AEO consultant's deck: only 24 of 109 carry a real store condition, and none carries a store-type condition. A ranked, conditioned front section would turn a competent generic AEO reference into a tool that tells a store operator what to do first for their specific business, the one thing a general model cannot already produce as well as this folder's raw material could support.
