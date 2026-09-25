# Google Ads for Ecommerce: The Complete Architecture & Operations Manual (2026 Edition)

source_id: 1qHnlFZvZKsgM8ijL6P-HZpVPMRO4nrc0  |  folder: /12-GAD-google-ads  |  cards: 22  |  words: 7,065  |  type: article (unsigned compiled manual, .docx)

credibility: No author, agency or company is named. The document says it is "compiled from Google documentation, platform changelogs, and operator-grade ecommerce playbooks", and the closing note lists Google Ads Help Center, Google Ads Developer Blog, Search Engine Journal, Search Engine Land, PPC Land, Optmyzr benchmark reports, COREPPC benchmarks and "operator-level" analyses. It sells nothing. It shows no own account data, no screenshots and no named client. Evidence is second-hand: cited third-party benchmarks (Optmyzr, COREPPC, Web Tonic), 1 cited study (Optmyzr, 24,702 PMax campaigns), 3 unnamed case examples (outdoor gear retailer, a 49% to 57% Shopping coverage case, a $25 to $9 CPC cap case) and paraphrased Google guidance. No links are given, so none of the numbers can be traced from the document itself. Treat it as a secondary summary, not a primary practitioner source (see section 9).
date signals: "current as of September 2026" (file modified 21 Sep 2026). Names dated platform changes: late 2024 PMax prioritisation replaced by ad rank; Optmyzr study "2024"; April 2026 user-provided data accepted from tags, Data Manager and API at once; June 2026 enhanced conversions for web and leads merged into 1 on/off setting; July 2026 Standard Shopping supports Maximize Conversion Value without tROAS; 17 Aug 2026 Target ROAS/CPA behaviour change for budget-limited campaigns; August 2026 PMax account-level placement exclusions expanded; 28 Feb 2026 YouTube Video Action line items paused or archived; Q1 2026 Demand Gen feed adoption 35%; 2026 Google product data specification update; Content API "v2.1"; PMax "now Waze". All of these date the advice and should be re-checked. `[web check: each dated 2026 change in the appendix table]`
header note: The exported text starts with an ecomOS library routing block (scope of folder 12-GAD, "Not here" pointers to 10-MCR, 11-ADC and 06-MEA, tier 2, "Volume 15 to 20"). That block is library metadata, not source content. Its pointer "multi-platform channel structures ... -> 11-ADC" is out of date: since 24 Sep 2026 deployment content lives in 24-DEP-ad-deployment.
currency note: All money figures are USD. Convert to the brand's currency and cost base before using any CPC, spend or cap number. `[needs brand data: account currency and typical CPC range]`

## 1. What this source is for

It helps an operator design and run an ecommerce Google Ads account end to end: which campaign types to run and what job each has (Standard Shopping, Performance Max, Demand Gen, brand campaigns), how Shopping and PMax auctions read the product feed, how to engineer product titles and supplemental feeds in Merchant Center, how to set up purchase tracking (GTM, enhanced conversions, server-side), and how to bid and scale (intent-tiered keywords, brand vs non-brand split, tROAS guardrails, portfolio caps, a 5-gate scaling check). It is broad and well organised. It is a summary, so it is thin on exact clicks and on evidence.

## 2. Principles

1. **Run a hybrid stack with explicit roles, not 1 campaign type.** Standard Shopping gives control and data visibility on core, known-intent traffic. PMax gives reach and automated discovery across Search, YouTube, Display, Gmail, Discover and Maps. Condition: the account has enough conversion volume per campaign to learn; smaller accounts should master high-intent campaigns first. Evidence: Optmyzr 2024 study of 24,702 PMax campaigns (82% ran PMax alongside other types; PMax "consistently underperformed" other campaigns when they competed for the same traffic). `[web check: Optmyzr 2024 PMax study findings]` [07a456f35774] [013bd9d69456]
2. **Role separation matters more since late 2024.** Source says Google moved from automatic PMax prioritisation to an ad rank model, so the campaign with the highest ad rank wins regardless of type. Without role rules, PMax will take high-intent commercial traffic from Standard Shopping. `[web check: current Google rule for PMax vs Standard Shopping auction priority]` [07a456f35774] [013bd9d69456]
3. **Standard Shopping is the precision layer.** It is the only place with product-group bids and clear per-product query data. Use it for hero SKUs (defend top impression share), high-margin products (aggressive bids), clearance (move stock fast, lower ROAS target), and new arrivals (gather data before scaling). Its conversions are easier to read than PMax's blended number. Condition: it serves only the Shopping surface. [f2e339bd5505]
4. **Shopping and PMax bid against the same feed, so they cannibalise unless the feed is split by role.** Source's fix: duplicate the feed; the Shopping copy is tuned for branded and high-intent category terms, the PMax copy for discovery and scaling. [f2e339bd5505] [59d9f9d20e0c]
5. **Choose feed-only or full-asset PMax by creative quality, not by default.** Feed-only (no headlines, descriptions, images or videos added, auto-generation turned off) fits when: (a) you want to focus on high-intent Shopping placements, (b) the brand lacks strong video or lifestyle imagery, (c) you need isolation between Shopping spend and YouTube/Display spend, or (d) an existing PMax overspends in low-value networks and misses ROAS goals. Full-asset fits when you have strong lifestyle photos, UGC video and brand video. Caveat inside the source: accounts without conversion volume see budget drift into YouTube, Display and Gmail even without uploaded assets. Card 5858ab16c0d1 adds an editorial correction: feed-only does not guarantee Shopping-only delivery and audience signals are not strict targeting. [5858ab16c0d1]
6. **One theme per PMax asset group.** Segment by product category (example: "Men's Shoes", "Skincare") or performance tier (best sellers, mid-tier, low-margin, new arrivals). Do not put the whole catalog in 1 generic group. Condition: 2 to 5 groups is the practical range for small-to-mid accounts. [a8f7e2302cd3]
7. **PMax has 3 levers you control:** URL expansion (URL-contains rules or turn final URL expansion off), audience signals (first-party data, Customer Match, custom segments), and placement exclusions (account-level exclusions now span PMax). Source adds that feeding inputs matters more than trying to steer outputs. [5858ab16c0d1] [abc2dfeeea38]
8. **Demand Gen is the feed-powered mid-funnel layer and gives more creative control than PMax.** You can upload, preview and edit ad combinations before launch and make separate ads for in-feed, in-stream and Shorts. PMax builds ads from assets automatically. Use Demand Gen for creative precision, message testing and visual identity. Condition: layer it in only after core conversions are stable. Card 64749b0f187a adds: judge it on assisted demand and downstream PMax, not direct last-click ROAS alone (this is a card addition, not in the source text). [64749b0f187a] [013bd9d69456]
9. **YouTube is now a surface inside Demand Gen and PMax, not a standalone ecommerce destination.** Highest-leverage placements for ecommerce inside Demand Gen: in-stream for product demos, Shorts for UGC-style content. [70ca3006a799]
10. **PMax cannibalising brand and high-intent Shopping traffic is "the single most common structural failure".** PMax takes branded traffic because it converts well, looks efficient, and starves the brand campaign of data. [a2f5b3c20d44]
11. **Brand captures demand; non-brand creates it. Keep them apart.** Mixing them distorts data and makes scaling decisions expensive. Most budget and testing effort should go to non-brand. [bcbe49473936] [a2f5b3c20d44]
12. **In Shopping and PMax, the feed is the advertising.** There are no keywords. Google reads titles, descriptions, attributes, price and availability to decide which queries each product matches. The title is "the most important line of advertising copy you will ever write". [c7807eeedee7] [9983e71e8efc]
13. **Feed quality is the biggest Ad Rank lever in Shopping and PMax.** Quality inputs in Shopping: title relevance, image quality, price competitiveness (expected CTR); title, description and attribute match to the query (ad relevance); page load speed, mobile responsiveness, content relevance (landing page experience). Source claims PMax aggregates quality signals across the asset group, so 1 weak product drags the whole group (no evidence given). [c7807eeedee7]
14. **Higher quality lowers actual CPC for the same position.** Better titles and complete attributes can cut CPC without changing bids. [c7807eeedee7]
15. **Front-load searched attributes in product titles; keep 1 attribute order across the whole catalog.** Consistency lets the algorithm learn reliable patterns. Avoid keyword stuffing. [9983e71e8efc]
16. **Supplemental feeds are "the most overlooked lever" in Merchant Center.** They override titles, product types and custom labels without touching the website or primary feed. [59d9f9d20e0c]
17. **Custom labels are the bridge between feed data and campaign structure.** Segment by margin tier, bestseller status, seasonality and inventory priority. The most impactful split separates high-ticket SKUs from low-margin products so they can be bid differently. [59d9f9d20e0c] [9a7b30ebd79d]
18. **Prevent feed errors before Google sees them.** Pre-validation beats repair. [82e55ef4dd25]
19. **Conversion values must be real order revenue, ideally margin-adjusted.** Actual revenue including discounts and shipping, not a fixed value. A fixed value "actively" degrades tROAS. [24d517dd8fe0] [283cece14dca]
20. **Enhanced conversions matter most where purchase volume is low.** Better match rates give Smart Bidding more data; this can decide whether Smart Bidding has enough signal at all. [80d2cbcc7a96]
21. **Organise Search keyword research by buyer intent tier, not by feature or volume.** 4 tiers: transactional, comparison, problem-aware, competitor. Each gets its own bid level and landing page logic. [4c09826249af]
22. **Build long-tail clusters on purpose instead of chasing head terms.** Lower CPC, less auction pressure, cleaner conversion signal; it "compounds horizontally across products, markets, and variations". Source calls it "margin engineering, not volume chasing". [4c09826249af]
23. **Catalog breadth (surface area) limits what the algorithm can find.** Under 30 SKUs there is not enough surface area to find viable demand pockets at scale. Once feeds are right, campaign structure becomes more predictable. [9a7b30ebd79d]
24. **Target ROAS is the default ecommerce bid strategy when order values vary.** Example: a $200 order and a $20 order need different bid economics. Use Maximize Conversion Value in growth phases when you accept lower marginal ROAS for volume. [283cece14dca]
25. **Since 17 Aug 2026 the tROAS number you enter matters more.** Budget-limited tROAS and tCPA campaigns now track closer to the stated target. A loose legacy target that the budget cap used to hide may now be hit exactly. Targets are a commercial decision: margin, stock position, product mix, promotions. `[web check: 17 Aug 2026 Target ROAS change]` [283cece14dca]
26. **Portfolio bid strategies share learning and unlock caps and floors.** Use when campaigns share 1 goal; do not use when goals differ or volume is low. [b664dd686d10]
27. **Fix inputs before chasing outputs.** PMax performance is a function of input quality (feed data, conversion signals, audience signals, creative), not of controlling the algorithm's output. Scale amplifies feed problems; it does not solve them. [abc2dfeeea38]
28. **Set target ROAS from gross margin, not industry averages.** A brand with 60% margins can scale profitably at a lower ROAS than a brand with 25% margins. [37a75be509aa]

## 3. Procedures

Note: the source gives few click paths. Where it names a menu or setting, it is tagged `[verify UI]`. Where it gives only the idea, the steps below say so.

### 3.1 Build the 4-layer retail stack
1. Layer 1, Standard Shopping: cover top-revenue SKUs and high-intent product categories. Bid strategy tROAS plus manual product-group bid levers. `[needs brand data: SKU revenue ranking, margin by SKU]` [07a456f35774] [f2e339bd5505]
2. Layer 2, Performance Max: 1 campaign focused on new-customer acquisition. Audience signals built around "lookalike and in-market segments" (source wording). `[web check: whether lookalike segments are available as PMax audience signals]` `[verify UI]` [07a456f35774]
3. Layer 3, Demand Gen: feed-connected mid-funnel layer across YouTube (incl. Shorts), Discover, Gmail, Maps and Display. Add only once core conversions are stable. [64749b0f187a] [07a456f35774]
4. Layer 4, brand controls: dedicated branded Search and branded Shopping campaigns; brand exclusions and branded negatives in PMax; brand negatives in non-brand campaigns (procedure 3.2). [a2f5b3c20d44]
5. Add campaign-level negative keywords for low-intent queries such as "free", "cheap", and competitor brand names in the main campaigns (competitor terms go to their own isolated campaign if you run one; see 3.10). [07a456f35774] [4c09826249af]
6. Starting budget bands (source heuristic, not measured): PMax 50 to 70% (catalog and multi-surface acquisition, segmented by category or performance tier); Standard Shopping 30 to 50% (branded and high-intent category terms); Demand Gen 10 to 20% (upper-funnel discovery with product feed). The source gives no separate share for brand Search. `[needs brand data: total monthly Google budget, catalog size, margin]` [013bd9d69456] [9a7b30ebd79d]
7. Duplicate the feed so Shopping and PMax each get a role-matched version (procedure 3.6). [59d9f9d20e0c]

### 3.2 Stop PMax brand cannibalisation (3 parallel actions)
1. Add branded negative keywords and brand exclusions to every PMax campaign. Brand exclusions in PMax apply to Search, Shopping and YouTube search inventory. There is an option to still let Shopping ads appear on searches for excluded brands; decide on purpose. `[verify UI]` [a2f5b3c20d44]
2. Add brand negative keywords to new-customer-acquisition Search and Shopping campaigns. [a2f5b3c20d44] [bcbe49473936]
3. Create dedicated branded Search and branded Shopping campaigns that collect only branded traffic. Brand keywords in exact match only; exclude non-branded terms. [a2f5b3c20d44] [bcbe49473936]
4. Give brand campaigns budget "uncapped relative to search volume" so no brand impression share is lost to competitors. [bcbe49473936]
5. Report brand and non-brand separately (procedure 5.4). [bcbe49473936]

### 3.3 Decide feed-only vs full-asset PMax
1. Check preconditions for feed-only: Merchant Center fully optimised and linked to Google Ads; purchase conversion tracking verified active; at least 15 products; optimised titles, competitive prices, complete attributes. `[needs brand data: active product count, feed diagnostics, purchase tag status]` [5858ab16c0d1]
2. Check whether any of the 4 feed-only conditions apply (section 2, principle 5). [5858ab16c0d1]
3. If feed-only: build the campaign with zero manual assets (no headlines, descriptions, lifestyle images, uploaded videos) and explicitly turn off Google's auto-generation, otherwise Google scrapes the site and creates assets. `[verify UI: auto-generated asset settings and final URL expansion]` [5858ab16c0d1]
4. If strong creative exists (lifestyle photos, UGC video, brand video): use full-asset PMax. [5858ab16c0d1]
5. After launch, watch channel delivery. Card 5858ab16c0d1 (editorial) adds: compare product performance, new vs returning outcomes, contribution and acquisition cost against the existing Shopping or full-asset setup; do not call it remarketing-only or promise Shopping-only delivery. `[needs brand data: channel breakdown of PMax spend, new vs returning split]` [5858ab16c0d1]

### 3.4 Structure PMax asset groups
1. Pick 1 theme per asset group: product category or performance tier. [a8f7e2302cd3]
2. Use 2 to 5 well-fed groups for small-to-mid accounts. Max 100 per campaign; asset groups cannot be shared between campaigns. [a8f7e2302cd3]
3. Match asset groups to product segments (example: kids vs adults, top categories). [9a7b30ebd79d]
4. Load each group with at least 15 high-quality images and 5 video variations (source attributes this to Google's creative playbook). [a8f7e2302cd3]
5. Refresh creative every 4 to 6 weeks. [a8f7e2302cd3] [abc2dfeeea38]
6. Set the 3 levers: URL expansion rules (URL-contains or off), audience signals (first-party data, Customer Match, custom segments), account-level placement exclusions. `[verify UI]` [5858ab16c0d1]

### 3.5 Rewrite product titles
1. Default order: Product Type, Material, Colour, Fit/Size, Key Feature, Brand (last). [9983e71e8efc]
2. Put the attributes buyers type inside the first about 70 characters. The first 25 to 30 characters matter most (source attributes this to Google). [9983e71e8efc]
3. Aim for about 120 characters; keep every title between 60 and 150 characters. [9983e71e8efc]
4. For some verticals use the alternative orders (these put brand first): Fashion/Apparel: Brand + Product Type + Key Feature + Model + Colour/Size. Electronics: Brand + Model Number + Product Type + Colour. Seasonal: Brand + Attributes (size, description) + Type. [9983e71e8efc]
5. Apply 1 order across the whole catalog. [9983e71e8efc]
6. Do not keyword-stuff. [9983e71e8efc]
7. Push the new titles through a supplemental feed (3.6), not by editing the site or primary feed. Channable and similar tools can sync titles this way. [59d9f9d20e0c]
8. Card 9983e71e8efc adds: test titles on your own auction data before a catalog-wide rollout. The source gives no test method. [9983e71e8efc]

### 3.6 Supplemental feeds, feed duplication and custom labels
1. Create a supplemental feed in the Merchant Center UI and link it to a primary feed. `[verify UI]` [59d9f9d20e0c]
2. Use it to override titles, product types and custom labels; to test title variants; to apply promotional labels; to isolate product sets for campaign roles. [59d9f9d20e0c]
3. For API work: source says Content API v2.1 allows partial product updates through supplemental feeds, changing only named fields. Supplemental updates do not reset product expiration dates. `[web check: Content API v2.1 status vs Merchant API]` [59d9f9d20e0c]
4. When running Shopping and PMax in parallel, duplicate the feed with distinct rules: Shopping version tuned for branded and high-intent category terms; PMax version tuned for discovery and scaling. The source does not say what the rules are or how the 2 versions should differ in practice. [59d9f9d20e0c]
5. Add custom labels for margin tier, bestseller status, seasonality and inventory priority. At minimum, separate high-ticket SKUs from low-margin products. `[needs brand data: margin per SKU, bestseller list, seasonality, stock priority]` [59d9f9d20e0c] [9a7b30ebd79d]
6. Build campaign and asset-group splits on those labels. [9a7b30ebd79d]

### 3.7 Feed health diagnostic and disapproval triage
1. Open Merchant Center > Products > Diagnostics. Issues are grouped by severity. `[verify UI]` [82e55ef4dd25]
2. Filter "Disapproved" first. These products are ineligible for all Shopping ads and free listings: immediate revenue loss. `[verify UI]` [82e55ef4dd25]
3. Then filter "Warnings" and "Limited performance": approved but underperforming; optimisation opportunities. `[verify UI]` [82e55ef4dd25]
4. Check the 5 common disapproval causes: (1) missing or wrong GTINs; (2) price mismatch between feed and landing page; (3) missing shipping info; (4) policy violations (restricted products, misrepresentation); (5) wrong feed formatting or missing required attributes. [82e55ef4dd25]
5. Use the "Fix type" filter to isolate auto-fixable items (formatting errors, missing optional attributes), select all, run Autofix. `[verify UI]` [82e55ef4dd25]
6. Fix manually: policy violations, price mismatches, missing required attributes. [82e55ef4dd25]
7. Prevention: pre-validate the catalog against current Google specs with a tool such as SmartFeed or Feedonomics. [82e55ef4dd25]
8. If prices change often: update the feed at least every 6 hours and turn on automatic item updates in Merchant Center settings so Google can use crawled prices when feed prices lag. `[verify UI]` [82e55ef4dd25]
9. Cadence: card 82e55ef4dd25 says weekly or monthly, or after a sudden drop in eligible products. The source text gives no cadence.

### 3.8 Purchase tracking through GTM (web container)
1. Add the Conversion Linker tag; fire on All Pages in most cases. [535e56dd51f1]
2. Add a GA4 Event tag for the `purchase` key event, triggered on the order confirmation or thank-you page. [535e56dd51f1]
3. Add the Google Ads Conversion Tracking tag with the Conversion ID and label from the Google Ads account. Trigger: a purchase dataLayer event pushed from Shopify's checkout/thank_you page or via Customer Events. `[verify UI: Shopify Customer Events and checkout page names]` [535e56dd51f1]
4. Pass dynamic remarketing parameters on the conversion tag: product ID, product category, conversion value. This fills remarketing audiences with product-level signals and helps Smart Bidding. [535e56dd51f1]
5. Make the conversion value the actual order revenue, including discounts and shipping. Ideally margin-adjusted; the source does not say how to compute that. `[needs brand data: order-level revenue definition, margin per order]` [24d517dd8fe0]

### 3.9 Enhanced conversions
1. In GTM, open the Google Ads Conversion tag and turn on "Include user-provided data". `[verify UI]` [80d2cbcc7a96]
2. Map dataLayer variables for email, phone and address collected at checkout. The tag hashes them and sends them with the conversion ping. [80d2cbcc7a96]
3. Shopify and WooCommerce: use the native Google channel or a custom GTM setup to forward purchase events with hashed data. `[verify UI]` [80d2cbcc7a96]
4. Account side: since June 2026 enhanced conversions for web and leads are 1 on/off setting with no method choice; since April 2026 user-provided data is accepted from tags, Data Manager and API at the same time. `[web check: current enhanced conversions setting and Data Manager]` `[verify UI]` [80d2cbcc7a96]
5. The source gives no step to confirm the match rate or diagnose it after setup. `[needs brand data: enhanced conversions diagnostics in the account]`

### 3.10 Server-side GTM
1. Trigger: source says server-side is "increasingly the default" above $50K/month spend. [535e56dd51f1]
2. Host a server container on Google Cloud, Stape or similar. [535e56dd51f1]
3. Set up a GA4 client to receive incoming events. [535e56dd51f1]
4. Configure the Ads Conversion Tracking tag in the server container to forward conversions to Google Ads. [535e56dd51f1]
5. Use the server to enrich values with CRM and backend data and to send real order revenue (discounts and shipping included). [24d517dd8fe0]
6. The source gives no testing, deduplication or consent steps.

### 3.11 Intent-tiered Search keyword build
1. Tier 1, transactional ("[product type] buy", "[product type] online", "[product type] for [use case]"): highest bids; land on the exact product page, not the category page. "The profit centre." [4c09826249af]
2. Tier 2, comparison ("[brand] vs [brand]", "[product type] review", "[product type] alternatives"): comparison-focused copy and landing pages; separate ad groups or campaigns so they are measured and bid on their own. [4c09826249af]
3. Tier 3, problem-aware (broad need or pain terms): lowest starting bids, tightest negative keyword coverage; route to content or category pages, not product pages. [4c09826249af]
4. Tier 4, competitor (rival product names): own campaign with its own budget cap; judge on its own conversion rate, not blended with the account. Expect lower CTR and higher CPC than brand. [4c09826249af]
5. Mine PMax search terms: find high-quality, high-converting terms Google found, then build dedicated Search campaigns on them for tighter control. `[verify UI: PMax search terms report]` [4c09826249af]
6. Build long-tail clusters across products, markets and variations. [4c09826249af]
7. Source also segments non-brand by awareness depth (problem-aware, solution-aware, product-aware, competitor-aware), each with its own ROAS expectation, bid aggression and creative angle. This is a second scheme next to the 4 tiers; the source does not reconcile them. [bcbe49473936]

### 3.12 Set and step Target ROAS
1. Pick the strategy: tROAS when order values vary a lot; Maximize Conversion Value when you want the most value within a budget with no ROAS floor (growth phase). Standard Shopping now allows Maximize Conversion Value without a tROAS (July 2026). `[web check: Standard Shopping Maximize Conversion Value without tROAS]` [283cece14dca]
2. Wait for bid strategy maturity: about 50 conversions a month for basic stability, more in competitive auctions, before moving to tROAS. `[needs brand data: monthly purchase conversions per campaign]` [abc2dfeeea38]
3. Set the first tROAS 10 to 15% below current actual ROAS. `[needs brand data: current actual ROAS per campaign, last 30 days or more]` [283cece14dca]
4. Once stable, step up in 15 to 20% increments, 2 to 3 weeks apart. [283cece14dca]
5. At each step watch impression share and conversion volume. [283cece14dca]
6. Re-audit every budget-limited tROAS or tCPA campaign against the 17 Aug 2026 change; rewrite legacy or loose targets to what the business can afford (margin, stock, product mix, promotions). `[needs brand data: gross margin %, stock position, promo calendar]` [283cece14dca]

### 3.13 Portfolio bid strategy with a Max CPC cap
1. Group campaigns that share 1 goal (example: 700% ROAS across all non-brand campaigns) under 1 portfolio strategy. `[verify UI]` [b664dd686d10]
2. Add a Max CPC cap to stop spikes, or a bid floor to compete harder. Source says caps and floors are only available through portfolio bidding, even for 1 campaign. `[web check: which Smart Bidding strategies support portfolio bid limits]` [b664dd686d10]
3. Set the cap from your own margin and CPC distribution (card caveat). `[needs brand data: CPC distribution by day, break-even CPC]` [b664dd686d10]
4. Do not group campaigns with different goals (example: clearance vs new arrivals), campaigns needing manual per-campaign bids, or low-volume campaigns. [b664dd686d10]

### 3.14 Five scaling gates (run before adding budget or campaign types)
1. Gate 1, feed health: disapprovals cleared, warnings and limited-performance items addressed. [abc2dfeeea38]
2. Gate 2, tracking integrity: validated end to end; enhanced conversions active; server-side tags firing; values equal actual order revenue. [abc2dfeeea38]
3. Gate 3, brand and non-brand in separate campaigns, budgets and reports. [abc2dfeeea38]
4. Gate 4, creative velocity: 15+ images and 5+ videos per PMax asset group, refreshed every 4 to 6 weeks; continuous Demand Gen refresh. Best types: lifestyle imagery, UGC video, product demos. [abc2dfeeea38]
5. Gate 5, bid maturity: about 50 conversions a month before moving to tROAS. [abc2dfeeea38]
6. If a gate fails, invest in inputs (titles, attribute mapping, custom-label segmentation), not budget. [abc2dfeeea38]

## 4. Rules, thresholds and numbers

| Rule | Number or threshold | Condition | Source's basis | Card id |
|---|---|---|---|---|
| Feed-only PMax minimum catalog | 15 products minimum | Feed-only PMax | Stated, no citation | [5858ab16c0d1] |
| Surface area floor | Under 30 SKUs = not enough to find viable demand pockets at scale | Shopping and PMax scaling | Heuristic, no evidence | [9a7b30ebd79d] |
| Asset groups per campaign | 1 min, 100 max; 2 to 5 practical | Small-to-mid ecommerce | Platform limit plus opinion | [a8f7e2302cd3] |
| Assets per asset group | 15+ images, 5+ videos | PMax | Attributed to Google's creative playbook | [a8f7e2302cd3] [abc2dfeeea38] |
| Creative refresh | Every 4 to 6 weeks | PMax asset groups | Attributed to Google | [a8f7e2302cd3] |
| Budget split | PMax 50 to 70%, Shopping 30 to 50%, Demand Gen 10 to 20% | Hybrid stack starting point | Source's suggested structure, not measured | [013bd9d69456] [07a456f35774] |
| Title length | 60 to 150 characters; target about 120 | Merchant Center titles | Stated as Google guidance | [9983e71e8efc] |
| Title match zone | First about 70 characters carry the match; first 25 to 30 most important | Merchant Center titles | Stated as Google guidance | [9983e71e8efc] |
| Feed refresh with dynamic pricing | At least every 6 hours, plus automatic item updates on | Prices change often | Stated | [82e55ef4dd25] |
| Price match | Feed price must equal landing page price (example $49.99 = $49.99) | Always | Top disapproval cause | [82e55ef4dd25] |
| Server-side GTM | Default above $50K/month spend | Tracking setup | "Increasingly the default"; rule of thumb | [535e56dd51f1] |
| Smart Bidding maturity | About 50 conversions/month; more in competitive auctions | Before moving to tROAS | Heuristic | [abc2dfeeea38] |
| Starting tROAS | 10 to 15% below current actual ROAS | Cold or newly switched campaign | Heuristic | [283cece14dca] |
| tROAS step-up | 15 to 20% per step, 2 to 3 weeks apart | After stable at lower target | Heuristic | [283cece14dca] |
| Portfolio Max CPC cap | Example: cap $9 after spikes up to $25 | tROAS with CPC spikes on low-demand days | 1 unnamed advertiser | [b664dd686d10] |
| Portfolio goal example | 700% ROAS across all non-brand campaigns | Shared goal | Example | [b664dd686d10] |
| Brand keyword match type | Exact match always; exclude non-brand terms | Brand campaigns | Stated | [bcbe49473936] |
| Brand budget | Uncapped relative to search volume | Brand campaigns | Opinion | [bcbe49473936] |
| Brand distortion pattern | Brand about 11% of search spend, 34% of conversions | "Many ecommerce accounts" | Unsourced pattern | [a2f5b3c20d44] [bcbe49473936] |
| Ad Rank formula | Max CPC x Quality Score x expected impact of extensions/formats + contextual adjustments | Source's model | Not Google's published formula; see section 9 | [c7807eeedee7] |
| Actual CPC formula | (Ad Rank of advertiser below / your Quality Score) + $0.01 | Source's model | Classic textbook formula; see section 9 | [c7807eeedee7] |
| CPC benchmarks 2026 | Search $1.42, Shopping $0.68, PMax $0.82 | Context only | COREPPC (Search), Web Tonic (Shopping, PMax) | [c7807eeedee7] [37a75be509aa] |
| ROAS benchmarks 2026 | Median all Google Ads 5.57x (Optmyzr Q2 2026); average 3.4x (COREPPC); Shopping 5.1x; PMax 4.8x; non-brand Search 3.4x; blended 4.2x (section 2.3) | Context only, not targets | Third-party reports | [37a75be509aa] [c7807eeedee7] |
| ROAS trend | Median 3.68 in 2025, down 10.03% YoY | Context | Unnamed report | [37a75be509aa] |
| Shopping CPC trend | Up 22% YoY | 2026 | Unnamed | [c7807eeedee7] [37a75be509aa] |
| Ecommerce conversion rate | 2.8% | Context | COREPPC 2026 | [37a75be509aa] |
| Demand Gen feed adoption | 35% of campaigns in 2026 (Q1), more than doubled in 2 years | Context | Unnamed | [64749b0f187a] |
| Title audit finding | Over 80% of brands audited in 2026 used raw Shopify manufacturer titles | Context | Unnamed audits | [9983e71e8efc] |
| Margin rule | 60% margin brand can scale at lower ROAS than 25% margin brand | Setting tROAS | Arithmetic logic | [37a75be509aa] |

## 5. Diagnostics and checks

### 5.1 Is PMax eating brand or Shopping traffic?
- Check: PMax search terms for brand queries; whether PMax has brand exclusions and branded negatives; whether brand Search and brand Shopping campaigns exist; whether non-brand Search/Shopping carry brand negatives. `[verify UI]` [a2f5b3c20d44]
- Bad: PMax ROAS looks unusually strong while the brand campaign is starved of data; no brand exclusion list on PMax. [a2f5b3c20d44]
- Fix: procedure 3.2.

### 5.2 Is Standard Shopping losing auctions to PMax?
- Check: both campaigns on the same feed with no role split; since late 2024 the higher ad rank wins, not the campaign type. [07a456f35774] [013bd9d69456]
- Fix: feed duplication with role rules (3.6); product-group bids on hero SKUs in Shopping. The source gives no metric to confirm overlap beyond coverage (next check).
- Coverage signal: the source's case went from 49% to 57% Shopping coverage in 1 month after feed duplication. It does not define "coverage" or say where to read it. `[web check: which Google Ads metric "Shopping coverage" refers to]` [59d9f9d20e0c]

### 5.3 Is feed-only PMax leaking into other networks?
- Check: channel delivery breakdown of spend (YouTube, Display, Gmail vs Shopping). Source warns low-conversion accounts see drift into those even without assets. `[verify UI: PMax channel performance report]` [5858ab16c0d1]
- Bad: spend in low-value networks while missing ROAS goals.
- Fix per source: feed-only config with auto-generation off; tighten URL expansion and placement exclusions. Card 5858ab16c0d1 warns this still does not guarantee isolation.

### 5.4 Is account ROAS flattered by brand?
- How: split spend and conversions by brand vs non-brand. `[needs brand data: brand vs non-brand spend, conversions, value]` [bcbe49473936]
- Bad: brand share of conversions far above its share of spend (source's pattern: 11% of spend, 34% of conversions), and blended ROAS used for scaling decisions.
- Next: judge non-brand on its own ROAS; consider moving brand-heavy budget into non-brand (source example: 30% shift, 22% new-customer lift). [bcbe49473936]

### 5.5 Feed health
- How: Merchant Center > Products > Diagnostics; Disapproved, then Warnings and Limited performance. `[verify UI]` [82e55ef4dd25]
- Good: no disapprovals; warnings handled.
- Bad: GTIN errors, price mismatch, missing shipping, policy flags, missing required attributes. Also borderline listings pushed to "ignored" by the 2026 spec (tighter image and availability rules). `[web check: 2026 product data specification changes]` [82e55ef4dd25]
- Next: Autofix low-risk items; fix the rest manually; pre-validate going forward.

### 5.6 Title quality
- Check: does the title start with brand or model name ("Aurora Lamp") or with searched attributes ("Brass Bedside Table Lamp, Dimmable, Touch Control - Aurora")? Are titles 60 to 150 characters? Is the attribute order the same across the catalog? [9983e71e8efc]
- Bad: raw Shopify manufacturer titles (source says over 80% of audited brands). [9983e71e8efc]

### 5.7 Tracking integrity
- Check: Conversion Linker on all pages; purchase event fires on thank-you page; Google Ads tag uses correct ID and label; dynamic remarketing parameters present (ID, category, value); value equals actual order revenue with discounts and shipping; enhanced conversions on with email, phone, address mapped. [535e56dd51f1] [80d2cbcc7a96] [24d517dd8fe0]
- Bad: fixed value per purchase (source: "actively degrading" tROAS). [24d517dd8fe0]
- The source gives no test method (for example Tag Assistant or comparing to backend orders). `[needs brand data: backend order count and revenue vs Google Ads reported purchases]`

### 5.8 Is the tROAS target a real business number?
- Check: budget-limited tROAS/tCPA campaigns whose actual ROAS runs far above target (source example: target 500%, delivering 800%). After 17 Aug 2026 these may fall toward 500%. [283cece14dca]
- Check: target vs break-even ROAS from gross margin. `[needs brand data: gross margin % after COGS, shipping, fees]` [37a75be509aa]
- Bad: target copied from benchmarks or left loose while the budget cap controlled spend.
- Next: reset the target to what the business can afford; step changes per 3.12.

### 5.9 CPC spikes on tROAS
- Check: daily CPC distribution; spikes on low-demand days (example up to $25). [b664dd686d10]
- Next: portfolio strategy with a Max CPC cap (example $9). [b664dd686d10]

### 5.10 Ready to scale?
- Run the 5 gates (3.14). Any fail = fix inputs first. [abc2dfeeea38]

## 6. Tools, settings and named features

- **Standard Shopping**: product-group bids, per-product query data; Shopping surface only. Maximize Conversion Value without tROAS since July 2026 (source claim). `[verify UI]` [f2e339bd5505] [283cece14dca]
- **Performance Max**: Search, Shopping, YouTube, Display, Discover, Gmail, Maps, and "now Waze" (source). 1 to 100 asset groups. Levers: URL expansion (URL-contains rules, final URL expansion off), audience signals (first-party data, Customer Match, custom segments), account-level placement exclusions (expanded August 2026). Auto-generated assets can be turned off. Brand exclusions apply to Search, Shopping and YouTube search inventory, with an option to still show Shopping ads on excluded-brand searches. PMax search terms can be mined. `[verify UI]` `[web check: PMax surfaces incl. Waze]` [5858ab16c0d1] [a2f5b3c20d44] [4c09826249af]
- **Demand Gen**: YouTube (incl. Shorts), Discover, Gmail, Maps, Display. Product feed integration ("virtual storefront"). Per-placement ad variants (in-feed, in-stream, Shorts), preview and edit before launch. YouTube Video Action line items paused or archived 28 Feb 2026; migrate to Demand Gen line items. `[verify UI]` `[web check: Video Action campaign status]` [64749b0f187a]
- **YouTube formats** (source table; card says verify specs):
  - Skippable in-stream: YouTube videos, GVP interstitials; no length limit (3 min or less recommended); product demos, unboxing, testimonials.
  - In-feed: YouTube Home, Search, Watch Next; no limit; discovery and catalog browsing.
  - Non-skippable in-stream: 15 to 60 sec (varies); full product story, promotional offers.
  - Bumper: 6 sec (5 sec min); brand recall, sale announcements.
  - Shorts: 60 sec or less recommended; UGC-style content, quick product reveals.
  - Masthead: YouTube homepage; no limit (10 sec or more recommended); seasonal launches, major sales.
  `[web check: current YouTube format length specs]` [70ca3006a799]
- **Google Merchant Center**: Products > Diagnostics; filters Disapproved, Warnings, Limited performance; "Fix type" filter; Autofix; automatic item updates; supplemental feeds (UI-created, linked to a primary feed); custom labels. `[verify UI]` [82e55ef4dd25] [59d9f9d20e0c]
- **Content API v2.1**: partial product updates via supplemental feeds. `[web check: Content API deprecation and Merchant API replacement]` [59d9f9d20e0c]
- **Feed tools**: Channable (sync titles through supplemental feeds), SmartFeed and Feedonomics (pre-validation). [59d9f9d20e0c] [82e55ef4dd25]
- **Google Tag Manager (web)**: Conversion Linker tag, GA4 Event tag (`purchase`), Google Ads Conversion Tracking tag, "Include user-provided data" option. [535e56dd51f1] [80d2cbcc7a96]
- **Server-side GTM**: server container on Google Cloud, Stape or similar; GA4 client; Ads Conversion Tracking tag. [535e56dd51f1]
- **Shopify**: checkout/thank_you page dataLayer push, Customer Events, native Google channel. **WooCommerce**: native Google channel or custom GTM. `[verify UI]` [535e56dd51f1] [80d2cbcc7a96]
- **Google Ads Data Manager**: accepts user-provided data alongside tags and API since April 2026. `[web check]` [80d2cbcc7a96]
- **Enhanced conversions**: single on/off setting since June 2026. `[verify UI]` [80d2cbcc7a96]
- **Bid strategies**: Target ROAS, Maximize Conversion Value, Maximize Conversions, Target CPA (named in the Aug 2026 change), portfolio strategies with Max CPC cap and bid floor. `[verify UI]` [283cece14dca] [b664dd686d10]
- **Benchmark publishers named**: Optmyzr, COREPPC, Web Tonic. [37a75be509aa]

## 7. Examples and case results

All are examples, not promises. None names a brand, date range or spend level.

- Optmyzr 2024 study: 24,702 PMax campaigns; 82% of advertisers ran PMax with other campaign types; PMax underperformed other campaigns competing for the same traffic. [07a456f35774]
- Brand distortion: brand terms about 11% of search spend, 34% of conversions, "in many ecommerce accounts". [a2f5b3c20d44] [bcbe49473936]
- Outdoor gear retailer: spent 80% of budget on brand; moved 30% of that spend to non-brand Search; "unlocked a 22% lift in new customer acquisition". [bcbe49473936] [a2f5b3c20d44]
- Feed duplication case: Shopping coverage 49% to 57% in 1 month after feed duplication with strict role separation. [59d9f9d20e0c] [9a7b30ebd79d]
- Portfolio cap: tROAS advertiser with CPC spikes up to $25 on low-demand days; portfolio strategy with Max CPC $9 stopped budget blowouts. [b664dd686d10]
- tROAS change illustration: target 500% delivering 800% while budget-limited; after 17 Aug 2026 may deliver closer to 500%. [283cece14dca]
- Title rewrite: "Aurora Lamp" vs "Brass Bedside Table Lamp, Dimmable, Touch Control - Aurora". [9983e71e8efc]
- Demand Gen plus PMax flow: fitness retailer uses Demand Gen lifestyle video for new activewear; PMax serves Shopping and Search once intent shows. [64749b0f187a]
- Asset group themes: "Men's Shoes", "Skincare"; kids vs adults. [a8f7e2302cd3] [9a7b30ebd79d]

## 8. Mistakes the source warns about

1. Running 1 campaign type for everything instead of a role-based stack. [07a456f35774]
2. Running Shopping and PMax on the same feed without role separation (direct cannibalisation). [f2e339bd5505] [59d9f9d20e0c]
3. Letting PMax bid on brand; no brand exclusions or branded negatives; no dedicated brand campaigns. "The single most common structural failure." [a2f5b3c20d44]
4. Judging the account on blended brand plus non-brand ROAS. [bcbe49473936]
5. Capping brand budgets and losing brand impression share to competitors. [bcbe49473936]
6. Dumping the whole catalog into 1 generic asset group. [a8f7e2302cd3]
7. Leaving auto-generation on in a "feed-only" PMax, so Google scrapes the site for assets. [5858ab16c0d1]
8. Choosing full-asset PMax by default instead of by creative quality. [5858ab16c0d1]
9. Adding Demand Gen before core conversions are stable (smaller accounts). [64749b0f187a]
10. Manufacturer titles (Brand + Product Name) that bury searched attributes past 70 characters; raw Shopify titles. [9983e71e8efc]
11. Inconsistent attribute order across the catalog. [9983e71e8efc]
12. Keyword stuffing titles. [9983e71e8efc]
13. Feed price different from landing page price. [82e55ef4dd25]
14. Slow feed updates when prices change often. [82e55ef4dd25]
15. Sending a fixed conversion value for every purchase. [24d517dd8fe0]
16. Not passing dynamic remarketing parameters. [535e56dd51f1]
17. Setting tROAS too high on a cold campaign (starves delivery). [283cece14dca]
18. Leaving legacy or loose tROAS targets after the 17 Aug 2026 change. [283cece14dca]
19. Copying industry ROAS averages as targets instead of using margin. [37a75be509aa]
20. Chasing head terms instead of building long-tail clusters. [4c09826249af]
21. Blending competitor campaigns into overall account performance. [4c09826249af]
22. Sending problem-aware traffic to product pages. [4c09826249af]
23. Putting campaigns with different goals (clearance vs new arrivals) or low volume into 1 portfolio. [b664dd686d10]
24. Scaling before the 5 gates pass; trying to control PMax outputs instead of fixing inputs. [abc2dfeeea38]

## 9. Caveats, conflicts and what is missing

**Generated or derivative document.** This looks like an AI-assisted compilation (a "deep research" style summary), not a primary source. Signs: no author, no own data; "compiled from" a list of publications with no links; whole passages repeated almost word for word (the 3-part brand separation and the 11%/34% line appear in both 1.6 and 4.2; "Google Shopping has no keywords... decides for itself" appears 3 times; the $50K/month server-side line and the 35% Demand Gen adoption line each appear twice); lead-gen wording in an ecommerce section ("conversion-to-pipeline rate" for competitor campaigns); and technical slips listed below. Its title matches the similar source 09 in this folder ("The Complete Google Ads Architecture & Operations Manual (2026 Edition)"); the exported filename of this document also carries "(2026 Edition)". Pass 2 should treat both as secondary and check for shared text rather than counting them as 2 independent confirmations.

**Internal contradictions**
- ROAS benchmarks do not agree: blended 4.2x (section 2.3) vs "average ecommerce ROAS 3.4x" (table) vs median 5.57x (Optmyzr Q2 2026) vs median 3.68 in 2025. Search ROAS is 3.4x in 2.3 and "non-brand Search" 3.4x in the table, the same number as the account average. Treat none as a target. [37a75be509aa] [c7807eeedee7]
- The Optmyzr study says PMax underperformed other campaign types on shared traffic, yet the cited benchmarks put PMax ROAS (4.8x) above Search (3.4x) and near Shopping (5.1x). Different populations; do not combine.
- Title order: the default puts brand last, but the fashion, electronics and seasonal alternatives put brand first. The source does not say when to choose which. [9983e71e8efc]
- Title zone: "first 25 to 30 characters most important" and "first about 70 characters carry the match" are both given as Google guidance.
- Feed-only PMax is offered for "strict isolation between Shopping spend and YouTube or Display spend", but the same section says low-volume accounts drift into YouTube, Display and Gmail even without assets. Card 5858ab16c0d1 adds a correction that feed-only does not guarantee placement isolation (Google Help links in the card).
- Gate 2 requires "server-side tags must be firing" before scaling, but section 3.5 frames server-side as the default only above $50K/month. For smaller accounts the gate is stricter than the setup advice. [abc2dfeeea38] [535e56dd51f1]
- Gate 5 says move "from Maximize Conversions to Target ROAS", while section 4.4 presents Maximize Conversion Value as the value-based growth option. The source does not explain the Maximize Conversions step for a value-bidding ecommerce account. [abc2dfeeea38] [283cece14dca]
- Shopping's role shifts: "top-revenue SKUs and high-intent categories" (1.1, 1.2), "branded and high-intent category terms" (1.6, 4.3), while 1.6 also asks for a separate dedicated brand Shopping campaign. The source does not say whether brand Shopping is the same campaign as the Standard Shopping layer.
- 2 non-brand schemes: 4 intent tiers (transactional, comparison, problem-aware, competitor) in 4.1 and 4 awareness levels (problem, solution, product, competitor aware) in 4.2. Not reconciled.
- 1.1 lists competitor brand names as negatives to filter; 4.1 runs competitor terms as their own tier. Compatible only if competitor terms are excluded from main campaigns and isolated in a competitor campaign; the source does not say this.
- Budget bands (PMax 50 to 70, Shopping 30 to 50, Demand Gen 10 to 20) can sum to 90% or up to 140%, and leave no line for brand Search. [013bd9d69456]

**Likely technical errors (check before using)**
- The Ad Rank formula as a product of bid, Quality Score and extension impact, and the "(Ad Rank below / your QS) + $0.01" CPC formula, are older textbook models. Google describes Quality Score as a diagnostic tool, not an auction input, and does not publish an exact Ad Rank formula. The source's own sentence explaining why Ad Rank appears "in both numerator and denominator" does not make sense. Keep the direction (better quality, lower CPC), not the formula. `[web check: Google's current Ad Rank and Quality Score documentation]` [c7807eeedee7]
- "Quality Score" as a named metric exists for Search keywords, not for Shopping or PMax products; the source applies the 3 QS components to Shopping without a source. [c7807eeedee7]
- The claim that PMax aggregates quality across the asset group so 1 weak product drags the group has no evidence. [c7807eeedee7] [a8f7e2302cd3]
- The Conversion Linker is described as "enables Google Ads to send data to Tag Manager". Commonly it stores ad click information (for example gclid) in first-party cookies so conversion tags can attribute. `[web check: Conversion Linker function]` [535e56dd51f1]
- The Google Ads Conversion Tracking tag in the web container is called "the server-side tag". It is a web tag in that setup; server-side is a separate container (3.7).
- The GA4 event tag is listed as a required part of Google Ads conversion tracking. Google Ads tags can work without it; the source does not say whether it means importing GA4 conversions or tagging directly. Risk of double counting if both are used as primary conversions. `[web check: Google Ads vs GA4 imported purchase conversions, primary vs secondary]`
- "Lookalike and in-market segments" as PMax audience signals: lookalike segments are a Demand Gen feature. `[web check]` [07a456f35774]
- Supplemental feeds "can only be created in the Merchant Center UI", yet the next sentence says Content API v2.1 updates them. Card 59d9f9d20e0c reads it as "not via the API". Content API v2.1 is being replaced by Merchant API. `[web check: Merchant API supplemental data sources]` [59d9f9d20e0c]
- Portfolio "caps and floors are only available through portfolio bidding, even for a single campaign": true for some strategies; check which. `[web check]` [b664dd686d10]

**What the cards add that the source text does not say** (do not cite the source for these): card 5858ab16c0d1's editorial correction and new vs returning measurement; card 64749b0f187a's "judge Demand Gen on assisted demand, not last-click"; card 9a7b30ebd79d's "thin listings just add disapproval risk"; card 37a75be509aa's "combine with AOV and LTV; a low-ROAS first order can be profitable when repeat purchase is strong" (the source header mentions LTV but the body does not); card 82e55ef4dd25's weekly or monthly cadence; card 9983e71e8efc's "test titles before catalog-wide rollout".

**What is missing**
- No how-to for feed duplication rules (what differs between the Shopping and PMax copies, and how to stop the same product serving twice).
- No method for margin-adjusted conversion values, break-even ROAS or profit on ad spend. `[needs brand data: gross margin %, COGS by SKU]`
- No new-customer acquisition goal settings for PMax (new customer value or new-customer-only), despite calling PMax the new-customer layer. `[web check: PMax customer acquisition goal options]`
- No incrementality or brand holdout test; the 22% lift case is not shown as a controlled test.
- No attribution model or conversion window guidance, no consent mode, no deduplication of browser and server events.
- No negative keyword list-building process beyond "free", "cheap", competitor names; no search term review cadence.
- No budget-change rules (how much to raise daily budgets at once) beyond the tROAS step cadence.
- No marketplace or multi-country guidance despite the subtitle ("Marketplace, and Multi-Channel").
- No free listings, Merchant Center promotions, product ratings or local inventory guidance.
- No Search ad copy (RSA) guidance.
- No evidence for the 15-product, 30-SKU, 50-conversion, 10 to 15% and 15 to 20% numbers.

**Conflicts with common ecommerce advice (for pass 2)**
- Many practitioners recommend brand first in titles for known brands; this source's default puts brand last (but its vertical alternatives put it first).
- Common advice is to change tROAS in small steps (often around 10 to 20%) and to start near current ROAS; this source starts 10 to 15% below and steps up 15 to 20%, which is in line on step size but assumes an upward path.
- "Uncapped" brand budgets and "always exact match" for brand differ from advice that brand spend should be tested for incrementality first (see 24-DEP source 03, which proposes brand holdout tests).
- The 50 to 70% PMax share differs from sources that prefer Shopping-led or Search-led structures for small catalogs; the source's own under-30-SKU warning points the same way.

**ecomOS note.** Every fix here (exclusions, negatives, bid targets, feed edits, tag changes) is a write to Google Ads, Merchant Center or the site. The agent recommends; a human acts. Keep Google Ads data separate from other brands' data.

## 10. Card index

- [07a456f35774] Build a Four-Layer Google Ads Retail Stack
- [f2e339bd5505] Standard Shopping for SKU-Level Bid Control
- [5858ab16c0d1] Choose Feed-Only vs Full-Asset PMax for Retail
- [a8f7e2302cd3] Structure PMax Asset Groups by Theme for Retail
- [64749b0f187a] Use Demand Gen for Feed-Powered Mid-Funnel Retail
- [70ca3006a799] Match YouTube Ad Formats to Ecommerce Jobs
- [a2f5b3c20d44] Stop PMax Brand Cannibalisation in Retail Accounts
- [c7807eeedee7] Read the Shopping and PMax Auction Correctly
- [9983e71e8efc] Rewrite Product Titles with Attribute Front-Loading
- [59d9f9d20e0c] Use Supplemental Feeds and Feed Duplication by Campaign Role
- [82e55ef4dd25] Run a Feed Health Diagnostic and Disapproval Triage
- [535e56dd51f1] Build Ecommerce Conversion Tracking via GTM
- [80d2cbcc7a96] Turn On Enhanced Conversions to Feed Smart Bidding
- [24d517dd8fe0] Pass Real Order Revenue to Target ROAS Bidding
- [4c09826249af] Tier Ecommerce Keyword Research by Buyer Intent
- [bcbe49473936] Separate Brand and Non-Brand Budgets for Honest ROAS
- [9a7b30ebd79d] Scale with Surface-Area Catalog Logic
- [283cece14dca] Set Target ROAS and Maximize Conversion Value Guardrails
- [b664dd686d10] Use Portfolio Bid Strategies for Caps and Floors
- [abc2dfeeea38] Pass Five Gates Before Scaling Ecommerce Spend
- [013bd9d69456] Choose Between PMax, Shopping and Demand Gen by Job
- [37a75be509aa] Anchor ROAS Targets to Margin, Not Benchmarks
