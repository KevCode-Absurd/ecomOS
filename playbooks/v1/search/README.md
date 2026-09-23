# Search — draft playbook

**Status:** source-linked draft; not owner-approved or outcome-tested.

Read [the operating contract](../OPERATING_CONTRACT.md) before using a workflow.

## Inputs
- Catalog/URLs
- Search Console data
- indexability
- query demand
- market

## Measures
- Qualified organic visits
- organic purchases
- contribution

## Foundation candidates
Inferred principle labels do not establish universal applicability. Retain source conditions; empty means no matched labelled principle, not absence of foundational knowledge.

- **Treat canonical URLs as the single version of each store page** (`8b18558928513b8f38dee6c8`): Canonical URLs identify the single preferred version of a page's content, preventing duplicate versions from splitting ranking signals.
  Applies when: Reviewing a store with filter, pagination or parameter variants that create near-duplicate product URLs.
  Condition: The source covers canonicals only briefly; it does not prescribe implementation for complex ecommerce parameter setups.
  Condition: Canonical tags are hints, not guarantees, and should be paired with consistent internal linking.

- **Build and submit an XML sitemap to help Google discover sellable URLs** (`3af48b4346f424d7d7513585`): Create an XML sitemap listing your pages, confirm it exposes product/category/blog URLs, and submit it so search engines can crawl and index them.
  Applies when: Launching a new store, adding a large batch of SKUs or categories, or diagnosing why pages aren't indexed.
  Condition: The source presents sitemap XML as the important variant for indexing; an HTML sitemap still helps users but is not the crawl-submission mechanism.
  Condition: Sitemaps inform Google rather than force indexing — pages still have to be crawlable and non-duplicate.
  Condition: Sitemaps support discovery; submission does not guarantee crawling, indexing or rankings.

- **Use sitemaps to help crawlers discover store URLs** (`425291fc77917caff8e8395a`): Submit a sitemap so search engines know which pages exist and can crawl them, rather than waiting passively.
  Applies when: You have new collections or product pages that are not appearing in organic search, or your catalogue is large enough that manual discovery is impractical.
  Condition: The source describes sitemaps as informing engines of your pages and prompting crawling; it does not promise indexing or ranking of every submitted URL.
  Condition: Sitemaps support discovery; submission does not guarantee crawling, indexing or rankings.

## Prioritise ecommerce search pages
Workflow ID: `search.money-pages`

**Deliverable:** Page-to-query map and backlog

### Proposed decision sequence
1. Map relevant shopping queries to product and collection pages
2. Find missing or overlapping intent coverage
3. Prioritise changes by demand, business value and feasibility

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Keep keyword research simple: two buckets only
Card: `b2ab9292f6baea94828d8182` · Source: Complete SEO Course (3 Hours)_ Rank #1 AI Search _ Prompts Included.docx · Section: 1

Find only transactional (buying-intent) and informational (topical-authority) keywords and stop overcomplicating.

Applies when: Starting keyword research for a store's category and product pages or planning a blog/content engine.

- Set up one SEO data source. The tutorial uses DataForSEO via a Google Sheets add-on (pay-as-you-go credits), but Ahrefs or Semrush work too — pick one and stick with it.
- Define transactional keywords: terms with buying intent where the searcher is ready to purchase or submit a lead — put these on your money/category/product pages.
- Define informational keywords: terms where people want to learn or compare — use these to build topical authority and capture upper-funnel traffic.
- Pull both 'similar keywords' and 'keyword suggestions' for your seed terms (the source requests up to 80 per run and notes similar keywords are stricter, suggestions looser).
- Ignore extra keyword-type definitions; the source argues simplicity performs better, especially when starting.
- Feed the raw keyword data into an LLM with a segmentation prompt (business type, location, goal = leads/topical authority) to sort keywords into money-page targets vs blog targets.
- Use the output to assign each keyword to a page: main service/category page gets the head transactional term; subpages get supporting terms; articles handle informational clusters.
- Remember zero-volume keywords can still matter — if you know your niche and shoppers search that phrase, optimize for it anyway.
- **Condition:** SEO tool volumes are estimates and not an absolute source of truth; use them as a guide alongside your own niche knowledge.
- **Condition:** Transactional vs informational is a simplification — the source says more granular definitions exist but don't matter for getting started.

#### Build a keyword strategy combining money pages and backlinks
Card: `527f947f429c29f7c3740324` · Source: $40,000,000 Worth of Ecommerce SEO Advice in 11 Minutes.docx · Section: 0

Combine transactional keyword targeting on collection pages with a small set of quality backlinks to drive organic revenue.

Applies when: Planning a quarter of SEO work for a store: which pages to create/optimize and which links to acquire.

- Do keyword research to identify transactional keywords (category/product intent) rather than informational ones.
- Map top keywords to new or existing collection pages, creating pages where gaps exist (source case: ~40 new collection pages).
- Build 10-20 quality backlinks to those money pages via link insertions and relevant outreach.
- Deprioritize informational blog keywords unless they support a transactional page.
- Review organic search revenue after 3-6 months and reallocate toward pages/keywords showing traction.
- Keep the plan lean: the source argues success comes from focusing on money pages plus backlinks, not from doing everything.
- **Condition:** The ~40-page example is a single case; the number of pages needed depends on catalog and niche.
- **Condition:** Timelines in the source's examples (3-11 months) are illustrative, not promises.
- **Condition:** Editorial qualification: paid placements must use rel="sponsored" or rel="nofollow"; do not buy unqualified links to manipulate rankings. Assess sponsored placements by relevant referral traffic and commercial value, not promised ranking credit.

#### Match the SERP's format, then differentiate on substance not word count
Card: `bd25b3cabfdf796ff18707bb` · Source: How to Rank #1 in Google in 2026_ The 3-Step SEO Playbook.docx · Section: 0

Build each money page in the format Google already rewards for that keyword, and compete by covering the topic more completely instead of writing longer.

Applies when: Building or rewriting a PDP, category page or landing page after the SERP intent check.

- Copy the winning format, not the winning content: identify whether the top results are product pages, category pages, long-form posts, listicles or videos, and make your page that format. The source explicitly includes video when how-to SERPs show videos.
- Ignore word count as a target — the presenter states Google does not reward a particular length. Replace 'how long should this be?' with 'what does someone searching this need to know, and have I covered it completely?'
- Study competitor outlines to ensure you cover the topic at least as thoroughly, and mine the SERP's People Also Ask / questions data to answer every question in the content.
- After drafting in your own words, review for semantic coverage — the entities and subtopics the top pages treat — because this supports both traditional search and AI answer surfaces. (The source uses Surfer's content editor workflow for outlines, questions and entity checks; verify current features if you use the tool.)
- Differentiate on substance you can add that competitors can't: original photography, real screenshots, tested specifics, opinions and data.
- Keep the page's commercial job clear — the format may be informational, but the page should still route buyers toward the product or category it supports.
- **Condition:** The source is a Surfer-sponsored video; tool-specific workflow steps describe one interface and may change.
- **Condition:** Quality coverage does not guarantee rankings — the presenter stresses that a great page alone is not enough for newer or low-authority sites.

### Retrieval and applicability
Search: `money pages category product search intent keywords`
Related domains: landing-pages, speed, measurement
Mixed-folder candidate IDs: 6e67e3c7c4432dabff6f7ff2, 28532c9e9701c5d4f375a954, 50d06003decdf6ab69fa15b3

- Does this advice fit the product lifecycle, market, audience and requested deliverable?
- Does it require proof, access, budget or assets the brand does not have?
- Does it change a fixed price, offer, policy or other explicit constraint?
- Are platform details or numerical claims current and substantiated?

### Output checks
- Deliver the specified artifact, not general advice about creating it.
- Use supplied brand facts; label hypotheses and missing inputs separately.
- Preserve relevant source conditions; do not copy another business’s proof or results.
- Include an owner, measurement and decision rule when proposing a test.
- Check the output against the requested constraints and owner feedback.

Stop after the requested artifact passes factual and brief checks; allow at most two revision passes, then report the unresolved issue.

## Audit technical ecommerce SEO
Workflow ID: `search.technical-search`

**Deliverable:** Technical search audit

### Proposed decision sequence
1. Inspect crawling, indexing and canonical signals on key templates
2. Separate confirmed faults from inferred ranking explanations
3. Specify fixes and a monitoring plan

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Treat canonical URLs as the single version of each store page
Card: `8b18558928513b8f38dee6c8` · Source: SEO Full Course 2026 _ SEO Tutorial For Beginners _ Search Engine Optimization Course _ Simplilearn.docx · Section: 5

Canonical URLs identify the single preferred version of a page's content, preventing duplicate versions from splitting ranking signals.

Applies when: Reviewing a store with filter, pagination or parameter variants that create near-duplicate product URLs.

- Understand the source's definition: canonical URLs are the URLs that show a unique page or unique content — the version a page intends to be indexed under.
- Check a live page's source code for the canonical tag. The source shows a page whose canonical version points to itself, meaning it isn't treated as duplicated elsewhere.
- Expect the XML sitemap to list these canonical versions of your pages, so the sitemap and canonical tags reinforce the same preferred URLs.
- Where a store generates variant URLs (filters, tracking parameters, sort orders), plan to consolidate them to the canonical product or category URL.
- Verify the implementation after changing it, since incorrect canonical tags can deindex the wrong page.
- **Condition:** The source covers canonicals only briefly; it does not prescribe implementation for complex ecommerce parameter setups.
- **Condition:** Canonical tags are hints, not guarantees, and should be paired with consistent internal linking.

#### Check initial and rendered HTML on ecommerce money pages
Card: `df678a626742279fa1b1ca43` · Source: Claude Code + SEO Masterclass.docx · Section: 1

Use server-rendered or static product content where practical, and verify crawler rendering before choosing an architecture.

Applies when: Technical SEO setup at site build time, when deciding how pages are rendered and whether crawlers can index them at all.

- Inspect initial HTML and rendered HTML on the homepage, collections and product pages.
- Prefer accessible product facts and links in initial HTML where practical; Shopify Liquid templates can provide this without rebuilding the storefront.
- For Google, use URL Inspection to check rendered content and blocked resources; Google can execute JavaScript.
- Correct missing product facts, broken links or blocked rendering resources, then retest affected templates.
- **Condition:** Static generation is not a Google indexing requirement. Rendering support differs across crawlers; assess the actual store and target engine.

#### Technical SEO on Shopify: Audit Order and Purpose
Card: `6b922910be5636aa4d47cbf5` · Source: Beginners Guide to Shopify SEO - Full Course (4+ Hour Masterclass).docx · Section: 0

Run a three-step Shopify technical SEO audit (manual, crawl, Search Console) as the foundation before content or link work.

Applies when: Before investing in content marketing or link building for your store; when organic rankings are stagnant and you don't know if the technical foundation is broken.

- Understand the mechanism: Google spends a limited crawl budget per site, so cleaning up duplicates and low-value pages lowers the 'cost of retrieval' and improves your odds of ranking.
- Step 1 - Manually review the store for the known Shopify issue classes: product URL duplication from collection paths, auto-generated tag/vendor/type pages, unredirected deleted products, variant duplication, missing structured data.
- Step 2 - Crawl the whole site with a crawler such as Sitebulb, using the Chrome (JS-rendering) crawler and a mobile user agent since Google uses mobile-first indexing. Enable structured data checks in crawl settings.
- Step 3 - Open Google Search Console and review Page Indexing for 404s, 'crawled - currently not indexed,' robots.txt blocks, and the Shopping/Enhancements structured data reports.
- Prioritize critical and high-severity crawl issues first, then work down the list. Fix redirects on unintended 404s (301 to the relevant live page) to recover traffic and preserve link equity.
- **Condition:** Presenter's opinion: technical SEO is the mandatory first step; skipping it undermines even excellent content and backlinks.
- **Condition:** Sitebulb and GSC interfaces change - verify current menu names.
- **Condition:** Large stores with thousands of pages are most affected, but small stores still benefit.

### Retrieval and applicability
Search: `indexability canonical crawl technical ecommerce SEO`
Related domains: landing-pages, speed, measurement
Mixed-folder candidate IDs: a4641f67247fff88193f0230, cfc0bb5b70ee282ce477cd1f, 7880f75d131f0e367e88b78c

- Does this advice fit the product lifecycle, market, audience and requested deliverable?
- Does it require proof, access, budget or assets the brand does not have?
- Does it change a fixed price, offer, policy or other explicit constraint?
- Are platform details or numerical claims current and substantiated?

### Output checks
- Deliver the specified artifact, not general advice about creating it.
- Use supplied brand facts; label hypotheses and missing inputs separately.
- Preserve relevant source conditions; do not copy another business’s proof or results.
- Include an owner, measurement and decision rule when proposing a test.
- Check the output against the requested constraints and owner feedback.

Stop after the requested artifact passes factual and brief checks; allow at most two revision passes, then report the unresolved issue.

## Create an ecommerce search content brief
Workflow ID: `search.search-content`

**Deliverable:** Search content brief

### Proposed decision sequence
1. Choose a query where the store has useful product expertise
2. Specify evidence, customer questions and appropriate product connections
3. Define a complete brief without keyword stuffing or invented authority

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### The four blog formats that still drive ecommerce revenue
Card: `9dcbebf25933a70c1185352d` · Source: Steal These Shopify SEO Hacks To Rank #1 Overnight.docx · Section: 0

Replace lifestyle and seasonal blog content with four bottom- and mid-funnel formats built for buyer intent.

Applies when: Planning a content calendar or auditing existing blog posts that get traffic but no sales.

- Stop producing the formats the source calls dead in ecommerce: seasonal lifestyle posts, generic listicles, trend pieces, and tips that apply to everyone and sell to no one.
- Format 1 - You vs competitors: target 'brand A vs brand B' searches by decision-stage buyers. Mentioning a competitor's name can help you rank for their branded search and introduce yourself as the stronger option.
- Format 2 - Alternatives to competitors: target 'alternatives to X' and 'best X alternatives' searches, list options and position yourself first to convert people outside your funnel.
- Format 3 - Best [product type] for [use case]: target clear buying intent like 'best eye serums for women over 50'; match product to need and target low-difficulty longtail terms.
- Format 4 - Buying guides: long-form evergreen content that educates hesitant buyers and naturally earns backlinks that lift domain authority.
- Before writing any post, check the SERP: if blogs rank, write the blog; if it's all collection pages, build that page instead.
- The source claims 10-15 well-targeted posts can build this system, and cites a client (Simbotanica) ranking #3 for a competitor's brand name within a week of implementing two competitor-focused formats.
- **Condition:** The Simbotanica ranking-in-a-week result is an anecdote, not a benchmark.
- **Condition:** Only works for products with existing search demand.

#### Run the 30-Second Intent Test Before Targeting Any Keyword
Card: `f32610667b5ffdda8a1d905f` · Source: Learn Everything About SEO & AI SEO in 50 Minutes!.docx · Section: 0

Search your target keyword and read the top 10 results; the format that ranks is Google's definition of the intent you must match.

Applies when: Validating keyword targets for a product page, category page, comparison page or blog post before committing content budget.

- Search the exact keyword in Google and inspect the top 10 organic results.
- Classify the dominant format: informational (how-to articles), commercial (comparison posts and buying guides), transactional (product or pricing pages), or navigational/branded. If the top 10 are all comparison blogs, intent is commercial; if they are product pages, intent is transactional.
- Match your page type to that intent rather than fighting it — you generally cannot rank a straight product page for a keyword whose SERP is all educational guides, and vice versa.
- Check the modern SERP features: AI overview at the top, sponsored ads, people-also-ask boxes, video carousels, local map packs, knowledge panels. If videos dominate, you need a video to compete.
- Note that even commercial and transactional queries now get AI overviews, meaning Google may answer comparison or buying questions before any click. Your page must go deeper than the summary to earn the click.
- **Condition:** Shorter keywords are usually higher volume, more competitive and less useful — 'coffee' (~650k US searches/month in the source's example) has a messy, undefined SERP, while 'best dark roast coffee beans for espresso' is low volume but has crystal-clear comparison intent and a fraction of the competition.
- **Condition:** SERPs vary by location, personalization and time; re-check intent when you refresh a page.
- **Condition:** Editorial qualification: paid placements must use sponsored or nofollow link attributes; do not buy unqualified links to manipulate rankings.

#### Attack Competitor Comparison, Review and Alternatives Queries
Card: `5346127695b99a2b80e07037` · Source: Ecommerce SEO_ The Definitive Guide for 2026.docx · Section: 1

Build pages for competitor reviews, alternatives, head-to-head and '[competitor] vs [you]' queries to capture high-intent category demand.

Applies when: Creating content that intercepts shoppers comparing brands before purchase in your category.

- Identify the five to ten competitors that appear most often across intents in your category (filter the competitor export); start from the ones showing up across many query types.
- Build these query variants: '[competitor] review', '[competitor] alternatives', '[competitor A] vs [competitor B]', and '[competitor A] vs [competitor B] vs [your brand]'.
- In alternatives lists, place your brand first and include seven to ten competitors, but only if you believe and can support the claim.
- Keep reviews factual: highlight objectively different formulations, sourcing or serving, and avoid disparaging competitors — the source explicitly advises against hostile comparisons.
- For head-to-head pages, use a category-seed word so the relevant keyword repeats once (e.g., 'creatine battle: Legion vs Thorne vs First Form') rather than repeating the seed for each brand.
- Expect volume: the source's small example produced 71 pages across 19 unique intents from these variants alone.
- Rebuild the list from Search Console as new variant queries surface; this is a self-reinforcing loop.
- **Condition:** Comparison content requires willingness to name competitors; some brands resist this, but the source argues silence cedes the decision to consumers and rivals.
- **Condition:** The source demonstrated fast indexing on one brand-owned example; treat speed as an anecdote, not a guaranteed timeline.

### Retrieval and applicability
Search: `search intent content product comparison helpful`
Related domains: landing-pages, speed, measurement
Mixed-folder candidate IDs: 2065c258255c0c4d8f220d81, 115d61471e7a4f9a711dd6fe, 45c33c914848981f80c71139

- Does this advice fit the product lifecycle, market, audience and requested deliverable?
- Does it require proof, access, budget or assets the brand does not have?
- Does it change a fixed price, offer, policy or other explicit constraint?
- Are platform details or numerical claims current and substantiated?

### Output checks
- Deliver the specified artifact, not general advice about creating it.
- Use supplied brand facts; label hypotheses and missing inputs separately.
- Preserve relevant source conditions; do not copy another business’s proof or results.
- Include an owner, measurement and decision rule when proposing a test.
- Check the output against the requested constraints and owner feedback.

Stop after the requested artifact passes factual and brief checks; allow at most two revision passes, then report the unresolved issue.
