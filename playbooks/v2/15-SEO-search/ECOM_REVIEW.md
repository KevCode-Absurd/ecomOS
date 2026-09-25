# SEO and search (15-SEO-search): ecommerce specificity review

## 1. Score

**Score: 3 out of 5.**

The architecture and template layers (groups D, E, F: site structure, collection pages, product pages) are genuinely store-native, with Shopify duplication fixes, variant handling, and collection-versus-product copy rules that a SaaS or blog would never need. But close to half the decision rules are general SEO doctrine (query intent, technical floor, link building, AI-content hygiene, reporting cadence) restated with a store label rather than reasoned differently for one. The playbook reads as strong on "how a store's pages are built" and average on "why an ecommerce agent should prioritize differently than a generic SEO agent."

**Section 3 rule count by class (146 decision rules, R1 to R146, including the 8 unsourced house overrides R139 to R146):**

| Class | Count | Share |
|---|---|---|
| (a) Store-specific in substance | 52 | 36% |
| (b) Generic principle, correctly tied to a store example or condition | 23 | 16% |
| (c) Generic, no store framing at all | 70 | 48% |
| (d) Out of scope for a store | 1 | 1% |

Note: this required judgment calls (a rule with one store example but a fully general principle scored (b), not (a)). The single (d) is R20 (a SaaS "electronic signature software" example). R26 (plumbing sweep example) and R116/R138 (physical-location local SEO) use out-of-scope examples but the rule itself is correctly scoped, so they are not counted as (d).

## 2. Prioritization check: fails

No section ranks levers by order of value, and none conditions the plan on store type (hero SKU vs full catalog, low vs high AOV, subscription vs one-off, marketplace-heavy, luxury/considered, mobile-first India vs US). Section 0's table routes by *task*, not *lever priority*. Existing conditioning is scattered: R18 (authority level), R58/R59 (SKU count), R116/R138 (physical location only). Draft block below.

### 3.0 Ecommerce priority order

1. **Money pages before anything else.** Collections and products convert; blogs do not. Every other lever waits. -> R4, R5, R67, conflict 7.1.
2. **Technical floor, once, sitewide.** Crawlable, indexed, no broken links, usable mobile UX. A blocked money page beats every content or link gain. -> R86, R87, R88.
3. **Protect branded search.** Any store running paid ads must hold position 1 for its own name and product names, or ad spend leaks to a competitor. -> R10.
4. **Catalog shape decides the template weight.** 50+ SKUs: collections likely carry most organic revenue, invest there first. Hero SKU or thin catalog: the product page and its cluster is the money page; do not force an empty collection layer. -> R58, R59, R37.
5. **Set the volume floor from AOV and catalog size, never a guru's number.** A niche or high-AOV, low-frequency ("considered purchase") store needs a lower floor and more patience than a low-AOV impulse category. -> R23. `[general practice]` on the considered-purchase half; the playbook gives only the catalog-size half.
6. **Marketplace-heavy categories change the target.** Where Amazon or another marketplace owns first-page or AI-citation slots, list there instead of fighting for a standalone page. -> R11.
7. **Concentrate on 1 category or cluster at a time, sized to the catalog.** A multi-category retailer picks 1 category per quarter; a hero-SKU or subscription store applies the same discipline to its 1 money page and cluster. -> R6, R68.
8. **Subscription and considered-purchase stores need the comparison and trust layer earlier.** These buyers read alternatives and reviews before converting; build that content sooner than a low-AOV, one-off store would. -> R65, R69, conflict 7.1. `[general practice]`.
9. **Local-only levers apply only with a physical location.** Google Business Profile, citations, NAP: skip for a pure online store. -> R138, R116.
10. **Mobile-first stores (most India-market and mobile-heavy US catalogs) should treat mobile UX as the primary check, not an equal-weight item.** `[general practice]`: a card for this exists in `sources/01` but was dropped; see missing lever 2.
11. **AI answer-engine visibility rises for comparison-heavy, considered or subscription categories; matters less for one commodity SKU.** -> R118, R119, R120.
12. **Link building is last, sized to the catalog's link gap, not a fixed quota.** No source conditions it by store type beyond authority level. -> R104, R105, R111.

## 3. Rule rewrites (generic wording, store-specific rewording, condition/sources/cards unchanged)

1. **R2** (never promise a timeline): "Never promise a launch, restock or seasonal-campaign date off an SEO timeline; a Q4 promotion planned around an unranked page is the most common way this rule gets broken."
2. **R7** (stay inside the topical map): "Do not build content for a product category the store does not sell just because it clusters near a covered one; every page in the map must map to a real collection or product."
3. **R8** (fixed monthly cycle): "Run the cycle against the catalog: validate keywords for the categories on sale or in season this month, update those pages first, then publish and get links."
4. **R14** (crawl, index, rank): "On a store, the most common break is a money page (a collection or product) sitting behind noindex, a robots block, or a Shopify duplicate-URL path; check those before anything else."
5. **R18** (long-tail before head terms): "A new or thin-catalog store should target its specific product and attribute combinations before its category head term; a full-catalog store can spread across both once its top categories rank."
6. **R70** (match or beat the SERP): "Read what ranks for a collection or product term and add what a shopper needs to decide (specs, comparisons, real photos) that the top results skip; do not just lengthen the page."
7. **R71** (add what AI cannot): "The store's own moat is its product testing notes, real customer photos, sizing and fit data, and return-rate-informed advice, not generic expert quotes."
8. **R77** (AI text is not penalized, low quality is): "Product and collection copy generated from a spec sheet with no added detail reads as thin to Google the same way a scraped manufacturer description does; add what the manufacturer sheet does not have."
9. **R78** (ground prompts in brand facts): "Ground every product or collection draft in the actual catalog feed, real specs, and existing reviews for that SKU, not a generic brand voice document alone."
10. **R86** (technical floor): "For a store, the floor is: every collection and product meant to sell is crawlable and indexed, no broken links to product pages, mobile checkout and PDP usable, and category hierarchy clear from home to product."
11. **R92** (redirect dead URLs): "Redirect a discontinued or deleted product to the nearest relevant *product or collection* the shopper can still buy, never to an unrelated category or the homepage as a first resort."
12. **R97** (Search Console property type): "Use a Domain property so shop., checkout. and blog. subdomains and both http/https variants of the storefront are covered in one property."
13. **R110** (screen a link prospect): "Screen out prospects with no readership that would ever buy this category of product; a site with traffic but the wrong audience is as useless as a low-traffic one."
14. **R125** (report branded vs non-branded): "Report branded clicks (brand and product-name searches) separately from non-branded category and product-type searches; branded volume often moves with ad spend, not SEO work."
15. **R136** (agency red flags): "A red flag specific to a store: an audit or retainer that only proposes blog content and never touches collection or product page structure."

## 4. Missing store levers

1. **Google's free product listings (Shopping tab / Merchant Center feed).** Would go in section 1 and group A. No source in this folder; `[general practice]`.
2. **Mobile-first storefront design as an explicit priority, not a speed footnote.** Near R86/R100. Source dropped from the merge: `sources/01`, card `684253d7bab8` ("mobile is the primary storefront design target," 70 to 80% of sales from mobile).
3. **Regional localization: near-me phrasing, multilingual pages, region-specific promotions (India vs US).** Near R99's international gap. Source dropped: `sources/01`, card `9f38dfbf4f52`.
4. **Subscription pages as a distinct money-page template.** Group E/F, a third template beside collection and product. Source exists but unused as a rule: `sources/09`, card `28f51e6a77cb` (Counterculture coffee-subscription example, only used as a generic "money page" illustration).
5. **A seasonal SEO calendar tied to inventory** (build and refresh category pages ahead of a peak). Group A or 5.7. Partial source: `sources/01`, card `5437c6f5b94e`; `sources/03`, principle 7 (no card id).
6. **Luxury or considered-purchase framing** (low-frequency, high-AOV buying behavior). R23 and group G. No source in this folder; `[general practice]`.
7. **Bundle and kit product pages.** Group F. No source in this folder; `[general practice]`.
8. **Bulk seasonal SKU turnover** at catalog scale, beyond the single-product handling in R50. Near R50/P2 step 7. No source beyond R50's own cards; `[general practice]`.

## 5. Demotions to an appendix "General background"

- **Group B, R14, R17, R18** (crawl/index/rank, SERP features, long-tail-to-head-term theory): universal mechanics, roughly 500 words, not store-specific until R15/R16/R19.
- **Group L, R104-R107, R109-R115, R117** (link-building doctrine): applies identically to any website, roughly 1,400 words. Keep R108, R116 and the override R106 in place.
- **Group H, R77, R79-R82, R84, R85** (AI-content hygiene, human gates, automation caution): generic content-ops practice, roughly 700 words. Keep R78 and R83 in place.
- **Section 6 tool-price rows** (Semrush/Ahrefs tiers, Screaming Frog pricing, journalist-platform tiers): vendor trivia already flagged `[web check]`, roughly 250 words.

## 6. Deliverables check (section 9)

Mostly pass. 9.1 (keyword map), 9.2 (architecture spec with the Shopify fix list) and 9.3 (page briefs) are things a store team would actually use; 9.3 is effectively the PDP and collection brief the domain needs. 9.6 (report led by organic revenue, not raw traffic) has the right KPI order. 9.4 and 9.5 are generic SEO-ops documents, which is fine, they need no store-specific format. Only change: split 9.3 into named "PDP brief," "collection brief" and "guide brief" so an agent or a client can ask for one by name.

## 7. The single highest-value change

Add the ecommerce priority-order block (item 2) as the entry point of section 0, ahead of the task-routing table, conditioned on store type: catalog size, AOV, subscription vs one-off, marketplace exposure and physical location. Right now the playbook treats every store as one undifferentiated "ecommerce site" and lets generic SEO material (roughly half of section 3) carry that weight instead. A hero-SKU subscription brand, a 2,000-SKU marketplace-heavy retailer and a luxury considered-purchase brand should not run the same 30-day plan (P24) or volume floor (R23); today they would, because nothing routes them differently before they reach the rules. This addition would separate the playbook from a generic SEO prompt more than any single rule rewrite, because it forces every downstream rule through "which kind of store is this" instead of "a store" as one category.
