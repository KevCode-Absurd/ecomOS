## Build a Four-Layer Google Ads Retail Stack
Use when: Structuring or restructuring the whole Google Ads account for an ecommerce catalog: deciding which campaign types to run and what job each one does.
- Layer 1 — Standard Shopping: cover top-revenue SKUs and high-intent categories with tROAS targets and product-group-level manual bid levers, so you keep query-level visibility on core products.
- Layer 2 — Performance Max: run a campaign focused on new-customer acquisition with audience signals built from lookalike and in-market segments, taking multi-surface discovery workloads off Shopping.
- Layer 3 — Demand Gen: use as the feed-powered mid-funnel layer (YouTube, Shorts, Discover, Gmail, Maps, Display) to create demand before the user searches; layer it in only after core conversions are stable.
- Layer 4 — Brand controls: run dedicated branded Search and Shopping campaigns, and exclude brand from PMax and new-customer campaigns so brand efficiency is reported separately.
- Assign budget bands source suggests for ecommerce: PMax ~50-70% for catalog/multi-surface acquisition, Standard Shopping ~30-50% for brand and high-intent categories, Demand Gen ~10-20% for upper funnel; treat as a starting heuristic, not a benchmark.
- Since late 2024 Google uses ad rank rather than automatic PMax prioritisation, so the highest-ad-rank campaign wins the auction regardless of type — role separation is what prevents PMax from absorbing your best Shopping traffic.
Caveat: Budget split percentages are the source's suggested structure, not measured results; adjust to catalog size and margin.
Caveat: Hybrid stacks need enough conversion volume per campaign to learn; small accounts should master high-intent campaigns before adding Demand Gen.

Tags: google-ads, campaign-architecture, performance-max, standard-shopping, demand-gen, budget-allocation
Source: # Google Ads for Ecommerce_ The Complete Architecture & Operations Manual (2026 Edition).docx

---

## Standard Shopping for SKU-Level Bid Control
Use when: Deciding which products belong in Standard Shopping versus PMax, or when PMax reporting is too blended to tell what is actually working.
- Route hero SKUs here when you need to defend top impression share on your most important products.
- Set aggressive product-group bids on high-margin products where the unit economics can absorb higher CPCs.
- Use Standard Shopping for clearance inventory you must move quickly, accepting a lower ROAS target on those product groups.
- Test new arrivals here first: Standard Shopping gives per-product query and conversion data you can read before deciding what to scale into PMax.
- Keep in mind both campaign types bid against the same feed; when running in parallel, duplicate the feed and give Shopping the branded/high-intent version and PMax the discovery version.
- Where attribution clarity matters across multiple sales channels, prefer reading Standard Shopping conversions over PMax's blended number that mixes Shopping, Display, YouTube and Search.
Caveat: Standard Shopping only serves the Shopping surface — it does not reach YouTube, Display, Gmail or Discover.
Caveat: Running Shopping and PMax on the same feed without role separation causes direct cannibalisation.

Tags: google-ads, standard-shopping, product-group-bidding, sku-management, measurement, campaign-architecture
Source: # Google Ads for Ecommerce_ The Complete Architecture & Operations Manual (2026 Edition).docx

---

## Choose Feed-Only vs Full-Asset PMax for Retail
Use when: Evaluating a feed-led versus full-asset Performance Max campaign for an ecommerce product catalog.
- Confirm Merchant Center linkage, eligible products, accurate prices and stock, and tested purchase-value tracking.
- Treat the source feed-only approach as a test of reduced manually supplied creative. Review the actual asset-generation and URL-expansion settings in the current interface.
- Monitor channel delivery, product performance and new versus returning customer outcomes; compare contribution and acquisition cost with the existing Shopping or full-asset setup.
- Do not classify the campaign as remarketing-only or promise Shopping-only delivery. Use a campaign with appropriate audience controls when strict remarketing is required.
Caveat: Editorial correction: PMax audience signals do not impose strict targeting; omitting manual creative does not guarantee placement isolation. https://support.google.com/google-ads/answer/14530785
Caveat: Merchant Center data can generate assets automatically. Source examples of efficient feed-led campaigns are not delivery guarantees. https://support.google.com/google-ads/answer/15865151

Tags: google-ads, performance-max, feed-only, asset-strategy, campaign-architecture, product-feed
Source: # Google Ads for Ecommerce_ The Complete Architecture & Operations Manual (2026 Edition).docx

---

## Structure PMax Asset Groups by Theme for Retail
Use when: Building PMax asset groups for a product catalog, or when a single generic asset group is producing weak or inconsistent results.
- Apply the rule of one theme per asset group — never dump the whole catalog into one generic group.
- Segment by product category (e.g. ‘Men's Shoes’, ‘Skincare’) or by performance tier (best sellers, mid-tier, low-margin, new arrivals) so spend and creative can be reasoned about per segment.
- Use two to five well-fed asset groups per campaign as the practical range for most small-to-mid ecommerce accounts; campaigns allow up to 100 groups but assets cannot be shared between campaigns.
- Populate each group per Google's creative guidance: at least 15 high-quality image assets and 5 video variations, refreshed every 4-6 weeks.
- Remember quality signals in PMax are aggregated across the whole asset group, so a single weak product or asset can drag down the group's performance.
Caveat: The 15-image/5-video guidance and 4-6 week refresh cadence come from Google's creative playbook as cited by the source and may change; validate in the current interface.

Tags: google-ads, performance-max, asset-groups, creative-strategy, catalog-segmentation, merchandising
Source: # Google Ads for Ecommerce_ The Complete Architecture & Operations Manual (2026 Edition).docx

---

## Use Demand Gen for Feed-Powered Mid-Funnel Retail
Use when: Planning mid-funnel or upper-funnel YouTube/Discover coverage for an ecommerce catalog, or when you need distinct creative per placement rather than AI-combined assets.
- Enable product feed integration so Demand Gen ads act as a virtual storefront, letting viewers shop the catalog on YouTube across supported formats and verticals.
- Exploit the control advantage: upload, preview and edit specific ad combinations before launch, and tailor separate YouTube ads for in-feed, in-stream and Shorts — something PMax does not permit because it auto-builds ads from uploaded assets.
- Position Demand Gen as the awareness and interest layer that engages users before they search; let PMax capture those users later with Shopping and Search placements once purchase intent appears.
- For a fitness catalogue example, reach prospects with lifestyle video showcasing new activewear, then let PMax serve tailored Shopping/Search once intent signals fire.
- Choose Demand Gen when creative precision, message testing and visual identity matter; choose PMax when automated asset combination and reach matter more.
- For smaller accounts, master high-intent campaigns first and layer Demand Gen in only once core conversions are stable.
- Note YouTube Video Action line items were paused/archived from 28 February 2026 — migrate ecommerce video to Demand Gen line items and verify current options in the interface.
Caveat: Demand Gen is upper/mid-funnel, so judge it on assisted demand and downstream PMax performance, not on direct last-click ROAS alone.

Tags: google-ads, demand-gen, youtube, product-feed, mid-funnel, creative-strategy
Source: # Google Ads for Ecommerce_ The Complete Architecture & Operations Manual (2026 Edition).docx

---

## Match YouTube Ad Formats to Ecommerce Jobs
Use when: Selecting video ad formats and lengths for a Demand Gen or PMax campaign in an ecommerce account.
- Skippable In-Stream (no length limit, ≤3 min recommended) — product demos, unboxing and testimonials where viewers can choose to keep watching.
- In-Feed (YouTube Home, Search, Watch Next; no length limit) — discovery-stage browsing and catalog browsing.
- Non-Skippable In-Stream (15-60 sec, varies) — full product story or promotional offers where you need the whole message seen.
- Bumper (6 sec, 5 sec min) — brand recall and sale announcements.
- YouTube Shorts (≤60 sec recommended) — UGC-style content and quick product reveals.
- YouTube Masthead (YouTube homepage, ≥10 sec recommended) — seasonal launches and major sales events.
- For ecommerce specifically, prioritise in-stream for product demos and Shorts for UGC-style content as the highest-leverage placements within Demand Gen.
- Note YouTube is now a surface inside Demand Gen and PMax rather than a standalone ecommerce destination, so format choice happens inside those campaign types.
Caveat: Length caps vary by format and change over time; verify current specs in Google Ads before producing assets.

Tags: google-ads, youtube, demand-gen, video-formats, creative-strategy, awareness
Source: # Google Ads for Ecommerce_ The Complete Architecture & Operations Manual (2026 Edition).docx

---

## Stop PMax Brand Cannibalisation in Retail Accounts
Use when: Diagnosing suspiciously strong PMax ROAS, or setting up a new ecommerce account where branded search must stay separately measured.
- Add branded negative keywords and brand exclusions to PMax campaigns so PMax cannot bid on branded queries; for PMax, brand exclusions apply to Search, Shopping and YouTube search inventory, with an option to still allow Shopping ads on excluded-brand searches.
- Add negative keywords to new-customer-acquisition Search and Shopping campaigns to stop them absorbing branded demand.
- Create dedicated branded Search and Shopping campaigns whose only job is collecting branded traffic, using exact match and excluding non-branded terms.
- Define roles explicitly: Shopping handles brand and high-intent categories with precision and cost control; PMax handles scale and new-demand discovery.
- Watch for the distortion pattern: in many ecommerce accounts, brand terms take roughly 11% of search spend but carry about 34% of conversions, which flatters account ROAS and hides weak non-brand prospecting performance.
- Separate reporting so you can judge whether non-brand is genuinely profitable rather than subsidised by brand efficiency — an outdoor gear retailer cited in the source shifted 30% of its brand-heavy budget to non-brand search and saw a 22% lift in new customer acquisition (a case example, not a promise).
Caveat: The 11%/34% split and the outdoor-gear result are source-cited examples from specific accounts, not universal figures.

Tags: google-ads, performance-max, brand-exclusions, cannibalisation, measurement, campaign-architecture
Source: # Google Ads for Ecommerce_ The Complete Architecture & Operations Manual (2026 Edition).docx

---

## Read the Shopping and PMax Auction Correctly
Use when: Explaining why a product wins or loses Shopping auctions, or deciding where to invest to improve visibility and CPC.
- Recognise that Google scans your feed (titles, descriptions, attributes, pricing, availability) and decides which queries each product matches — the feed is the advertising, not just a data source.
- Treat the product title as your most important line of ad copy, because that is what Google reads to determine what you sell and who sees it.
- Understand Ad Rank = Max CPC Bid × Quality Score × Expected Impact of Extensions/Formats + Contextual Adjustments; the simplified form is Bid × Quality Score.
- Improve the Shopping quality inputs: title relevance to query, image quality and price competitiveness (expected CTR); closeness of title/description/attributes to the query (ad relevance); and product page load speed, mobile responsiveness and content relevance (landing page experience).
- For PMax, remember quality signals aggregate across the whole asset group, so one weak product drags the group — feed quality is the single biggest Ad Rank lever.
- Work the CPC formula: Actual CPC = (Ad Rank of advertiser below you ÷ Your Quality Score) + $0.01. Because Ad Rank appears in both numerator and denominator, a higher Quality Score lowers your actual CPC for the same position.
- Practical ecommerce consequence: accurate titles and complete attributes can cut CPC on the same products without changing bids.
Caveat: Source-cited 2026 averages (Search CPC ~$1.42, Shopping ~$0.68, PMax ~$0.82; blended ROAS 4.2×; Shopping ROAS 5.1×, Search 3.4×, PMax 4.8×) are benchmark aggregates that vary by vertical and margin — not targets.
Caveat: Google Shopping CPCs were cited as up 22% year over year, making feed efficiency more important but also making old CPC assumptions unreliable.

Tags: google-ads, auction-mechanics, ad-rank, quality-score, product-feed, cpc
Source: # Google Ads for Ecommerce_ The Complete Architecture & Operations Manual (2026 Edition).docx

---

## Rewrite Product Titles with Attribute Front-Loading
Use when: Optimising product titles in Google Merchant Center for Shopping, PMax or Demand Gen visibility on a retail catalog.
- Use the source's 2026 default structure: Product Type → Material → Colour → Fit/Size → Key Feature → Brand (last).
- Replace the manufacturer pattern (Brand + Product Name), which buries matching attributes past the point where Google weights them. Example: ‘Aurora Lamp’ tells Google almost nothing; ‘Brass Bedside Table Lamp, Dimmable, Touch Control – Aurora’ conveys product type, material, key feature and brand.
- Keep the attributes buyers type inside the first ~70 characters, since Google's matching weights that section most heavily; the first 25-30 characters matter most and optimised titles run around 120 characters.
- Keep total title length between 60 and 150 characters as the working range.
- Use vertical-specific alternatives where they fit: Fashion/Apparel — Brand + Product Type + Key Feature + Model + Colour/Size; Electronics — Brand + Model Number + Product Type + Colour; Seasonal — Brand + Attributes (size, description) + Type.
- Apply the same attribute order across the entire catalog so the algorithm can learn reliable patterns.
- Avoid keyword stuffing — unnatural attribute density is penalised. Over 80% of ecommerce brands audited in 2026 used raw Shopify manufacturer titles, missing this lever.
Caveat: The 60-150 character range and 25-30/70-character weightings are source guidance; test titles in your own auction data before rolling out catalog-wide.

Tags: google-ads, product-feed, title-optimization, merchant-center, catalog-management, seo
Source: # Google Ads for Ecommerce_ The Complete Architecture & Operations Manual (2026 Edition).docx

---

## Use Supplemental Feeds and Feed Duplication by Campaign Role
Use when: Testing title variants, applying promotional labels, or running Shopping and PMax in parallel on the same catalog.
- Create a supplemental feed in the Merchant Center UI and link it to a primary feed; use it to override titles, product types and custom labels without editing your website or primary feed.
- Use supplemental feeds to test title variants, apply promotional labels, and isolate product sets for different campaign roles; tools like Channable can sync optimised titles to Merchant Center this way.
- Note Content API v2.1 allows partial product data updates via supplemental feeds, modifying specific fields without affecting other data, and supplemental feed updates do not reset product expiration dates.
- For parallel Shopping + PMax, duplicate the feed with distinct rules: the Shopping version optimised for branded and high-intent category terms, the PMax version optimised for discovery and scaling.
- Accept that duplicate feeds let both campaigns surface products in eligible auctions more often without sacrificing efficiency; a documented case study showed Shopping coverage rising from 49% to 57% in one month after feed duplication with strict role separation (a case example, not a guarantee).
- Build custom-label architecture as the bridge between feed data and campaign structure — especially separating high-ticket SKUs from low-margin products so bids can differ by segment.
Caveat: Supplemental feeds can only be created in the Merchant Center UI, not via the API, and must be linked to a primary feed.

Tags: google-ads, merchant-center, supplemental-feeds, feed-duplication, custom-labels, catalog-segmentation
Source: # Google Ads for Ecommerce_ The Complete Architecture & Operations Manual (2026 Edition).docx

---

## Run a Feed Health Diagnostic and Disapproval Triage
Use when: Weekly or monthly catalog hygiene for an ecommerce store running Shopping, PMax or free listings, or after a sudden drop in eligible products.
- Go to Google Merchant Center → Products → Diagnostics and filter by ‘Disapproved’ first — disapproved products are ineligible for all Shopping ads and free listings, so each one is immediate lost revenue.
- Then filter ‘Warnings’ and ‘Limited performance’ — these are approved but underperforming and represent optimisation opportunities rather than blockers.
- Know the five most common ecommerce disapproval causes: missing or incorrect GTINs; price mismatch between feed and landing page; missing shipping information; policy violations (restricted products, misrepresentation); and incorrect feed formatting or missing required attributes.
- Treat price mismatch as a top offender: if the feed says $49.99, the landing page must also show $49.99.
- Use the ‘Fix type’ filter to isolate auto-fixable items (formatting errors, missing optional attributes), select all, and run Autofix; handle policy violations, price mismatches and missing required attributes manually.
- Prevent rather than repair: pre-validate the whole catalog against current Google specs with tools like SmartFeed or Feedonomics before Google sees it.
- For dynamic pricing, update the feed at least every 6 hours and enable automatic item updates in Merchant Center so Google can use crawled prices when feed prices lag.
- Note Google's 2026 product data specification update tightened image and availability requirements, pushing more borderline listings into the ignored column.
Caveat: Diagnostics labels, Autofix scope and the 2026 spec requirements change — verify the current Merchant Center interface and Help Center before large-scale fixes.

Tags: google-ads, merchant-center, feed-health, disapprovals, product-feed, operations
Source: # Google Ads for Ecommerce_ The Complete Architecture & Operations Manual (2026 Edition).docx

---

## Build Ecommerce Conversion Tracking via GTM
Use when: Setting up or auditing conversion tracking for a Shopify or WooCommerce store before scaling Google Ads spend.
- Add the Conversion Linker tag and fire it on All Pages in most cases; this enables Google Ads to send data to Tag Manager.
- Add a GA4 Event tag defining the key event — for ecommerce, the `purchase` event triggered on the order confirmation/thank-you page.
- Add the Google Ads Conversion Tracking tag, firing on the purchase event and using the Conversion ID and label from the Google Ads account; trigger it from a purchase dataLayer event pushed from Shopify's checkout/thank_you page or via Customer Events.
- Pass dynamic remarketing parameters — product ID, product category and conversion value — so remarketing audiences carry product-level signals and Smart Bidding optimises toward the right values.
- Move to server-side GTM when spend exceeds roughly $50K/month per the source: host a server container on Google Cloud, Stape or similar, configure a GA4 client to receive incoming events, and forward conversions to Google Ads from the server.
- Expect three server-side benefits: less page code and faster load, more durable tracking under browser restrictions, and richer data because server-side values can be enriched with CRM and backend signals.
Caveat: The $50K/month threshold is the source's rule of thumb, not a universal trigger; weigh it against technical cost and team capability.

Tags: google-ads, conversion-tracking, gtm, server-side-tracking, shopify, measurement
Source: # Google Ads for Ecommerce_ The Complete Architecture & Operations Manual (2026 Edition).docx

---

## Turn On Enhanced Conversions to Feed Smart Bidding
Use when: Ecommerce accounts with low purchase volume relative to lead-gen accounts, or any store where Smart Bidding appears starved of conversion signal.
- Understand the mechanic: enhanced conversions supplement standard tags by sending hashed email, phone and name data from your site; Google compares it to hashed data from signed-in accounts and attributes ad events. Data is hashed before transmission — Google never receives raw PII.
- In GTM, open the Google Ads Conversion tag and enable ‘Include user-provided data’.
- Map dataLayer variables for email, phone and address fields collected during checkout so the tag can include them in the conversion ping.
- For Shopify and WooCommerce, use the native Google channel or a custom GTM-based setup to forward purchase events with hashed data.
- Expect the payoff to be better match rates — more usable conversion data, which matters most for ecommerce where purchase volume is low and the algorithm can otherwise be starved of signal.
- Track the 2026 interface changes: from April 2026 Google Ads accepts user-provided data from website tags, Data Manager and API connections simultaneously; from June 2026 enhanced conversions for web and for leads merge into a single on/off setting and method selection disappears from the interface.
Caveat: Setup labels and settings changed in 2026 — verify the live GTM and Google Ads interfaces rather than following old step lists.

Tags: google-ads, enhanced-conversions, gtm, first-party-data, smart-bidding, measurement
Source: # Google Ads for Ecommerce_ The Complete Architecture & Operations Manual (2026 Edition).docx

---

## Pass Real Order Revenue to Target ROAS Bidding
Use when: Configuring conversion values for an ecommerce store running Target ROAS or Maximize Conversion Value bidding.
- Use server-side tracking to pass the actual revenue of each order — including discounts and shipping — rather than a fixed value for every purchase.
- Recognise the consequence of getting this wrong: reporting a fixed value actively degrades the algorithm's ability to optimise, because the bidder has no way to distinguish a $200 order from a $20 order.
- Align with the value-based bidding principle behind Target ROAS: it is appropriate precisely when conversion values vary significantly, which is normal in ecommerce.
- Consider passing margin-adjusted values where the business can calculate them, so the bidder optimises toward profit rather than raw revenue.
- Before scaling, verify conversion values reflect real order revenue as one of the scaling gates — inaccurate conversion data teaches the algorithm to optimise for the wrong outcome.
Caveat: The source frames margin-adjusted values as ideal but does not prescribe a calculation; align the method with your finance data before changing live values.

Tags: google-ads, target-roas, conversion-value, server-side-tracking, bidding, measurement
Source: # Google Ads for Ecommerce_ The Complete Architecture & Operations Manual (2026 Edition).docx

---

## Tier Ecommerce Keyword Research by Buyer Intent
Use when: Building or restructuring Search campaigns for an ecommerce store, or deciding which queries deserve their own ad groups and budgets.
- Tier 1 — Transactional: queries like ‘[product type] buy’, ‘[product type] online’, ‘[product type] for [use case]’. Bid highest and send traffic to the exact product page, not the category page; this is the profit centre of the account.
- Tier 2 — Comparison: ‘[brand] vs [brand]’, ‘[product type] review’, ‘[product type] alternatives’. Pair with comparison-focused ad copy and landing pages, and keep them in separate ad groups or campaigns so they can be measured and bid independently.
- Tier 3 — Problem-Aware: broad need or pain-point terms. Expect lower conversion rates and the highest risk of irrelevant traffic — apply the tightest negative keyword coverage and lowest starting bids, and route to content or category pages rather than product pages.
- Tier 4 — Competitor: rival product names. Isolate with their own budget cap and judge them on conversion-to-pipeline rate rather than blending them into account performance; they usually show lower CTR and higher CPC than brand campaigns.
- Mine PMax Search Terms for high-quality, high-converting queries Google found for you, and build dedicated Search campaigns targeting those terms for tighter control.
- Build long-tail clusters intentionally instead of chasing head terms: lower CPC, less auction pressure, cleaner conversion signal — it compounds horizontally across products, markets and variations rather than exploding vertically.
Caveat: Intent tiers are the source's organising heuristic; conversion rates and CPC expectations vary by vertical and should be validated against your own account data.

Tags: google-ads, keyword-research, search-campaigns, intent-tiering, long-tail, campaign-architecture
Source: # Google Ads for Ecommerce_ The Complete Architecture & Operations Manual (2026 Edition).docx

---

## Separate Brand and Non-Brand Budgets for Honest ROAS
Use when: Reviewing account-level ROAS for an ecommerce store, or planning how much budget to shift from brand defence into category and problem-aware prospecting.
- Start from the principle: brand traffic captures demand, non-brand traffic creates it; mixing the two distorts data and makes scaling decisions expensive.
- Build brand campaigns to protect your product name and close variants — they are typically cheap and convert well. Split into Brand Search (text ads) and Brand Shopping (product listings), use exact match, exclude non-branded terms, and keep budget uncapped relative to search volume because losing brand impression share to a competitor is highly avoidable lost revenue.
- Put most budget and testing effort into non-brand campaigns targeting category and problem-aware terms where the prospect has not chosen a vendor yet.
- Segment non-brand by awareness depth — problem-aware, solution-aware, product-aware, competitor-aware — because each cluster carries different ROAS expectations, bid aggression and creative angles.
- Apply the three-part separation mechanic: brand exclusions and branded negatives in PMax; negatives in new-customer campaigns; dedicated branded campaigns collecting branded traffic.
- Use the distortion check: where brand is ~11% of search spend but ~34% of conversions, account ROAS is flattered and non-brand performance is hidden. Separating the two reveals whether non-brand is profitable or merely subsidised (source case: an outdoor gear retailer shifted 30% of brand-heavy spend to non-brand and reported a 22% lift in new customer acquisition — an example, not a benchmark).
Caveat: Keep the distinction clear: brand campaigns capture existing demand and should not be credited with new-customer growth; the 11%/34% split and the retailer result are account-specific examples.

Tags: google-ads, brand-vs-non-brand, budget-allocation, measurement, acquisition, campaign-architecture
Source: # Google Ads for Ecommerce_ The Complete Architecture & Operations Manual (2026 Edition).docx

---

## Scale with Surface-Area Catalog Logic
Use when: Planning growth for a Google Ads ecommerce account, especially when deciding whether catalog size or campaign structure is the bottleneck.
- Assess surface area first: below roughly 30 SKUs you likely do not have enough breadth for the algorithm to find viable demand pockets at scale.
- Once feeds are structured correctly, campaign structure becomes far more predictable — fix the feed before restructuring campaigns.
- Segment PMax by product group and intent rather than running one campaign for everything, and match asset groups to specific product segments (e.g. kids vs adults, top categories).
- Use custom labels in the feed — margin tier, bestseller status, seasonality — so campaign structure reflects the commercial reality of your catalog rather than the platform's default groupings.
- Expect the payoff in coverage: duplicated, role-separated feeds let both campaigns surface products more frequently across eligible auctions (source case: Shopping coverage rose from 49% to 57% in one month).
- Treat catalog expansion carefully — more SKUs adds surface area only if each product has a complete, well-titled feed entry; thin listings just add disapproval risk.
Caveat: The 30-SKU threshold is the source's heuristic, not a hard rule; a well-structured small catalog can still work while a poorly structured large one will not.

Tags: google-ads, catalog-scaling, surface-area, custom-labels, performance-max, product-feed
Source: # Google Ads for Ecommerce_ The Complete Architecture & Operations Manual (2026 Edition).docx

---

## Set Target ROAS and Maximize Conversion Value Guardrails
Use when: Choosing or tuning bid strategies for ecommerce Shopping and PMax campaigns, or revalidating legacy targets after the August 2026 behaviour change.
- Use Target ROAS when conversion values vary significantly — the standard ecommerce case where a $200 order and a $20 order need different bid economics — and feed it accurate, ideally margin-adjusted values.
- Start tROAS 10-15% below your current actual ROAS to give the algorithm room to learn and expand; a target set too high on a cold campaign starves delivery and blocks conversion learning.
- Step the target up incrementally in 15-20% increments with two to three weeks between changes, monitoring impression share and conversion volume each time.
- Use Maximize Conversion Value when the goal is maximum conversion value within a set budget with no fixed ROAS constraint — appropriate in growth phases where you accept lower marginal ROAS for extra volume. In Standard Shopping it is now available without a Target ROAS requirement, extending flexibility to controlled setups.
- Re-audit targets against the August 17 2026 change: budget-limited campaigns using Target ROAS or Target CPA now work more consistently toward the stated target even when budgets are adjusted. A campaign with a 500% tROAS that previously delivered 800% may now deliver closer to 500% unless you change the target.
- Set targets as commercial decisions reflecting margin, stock position, product mix and promotional activity — not by copying industry ROAS averages.
Caveat: The 10-15% starting discount and 15-20% step-up cadence are source heuristics; step sizes depend on conversion volume.
Caveat: The August 2026 behaviour change means legacy loose targets may need revision — verify current behaviour in the live interface.

Tags: google-ads, target-roas, maximize-conversion-value, bidding, smart-bidding, budget-management
Source: # Google Ads for Ecommerce_ The Complete Architecture & Operations Manual (2026 Edition).docx

---

## Use Portfolio Bid Strategies for Caps and Floors
Use when: Running multiple ecommerce campaigns toward the same performance goal, or when Smart Bidding causes CPC spikes that threaten budget control.
- Understand what portfolio bidding does: it groups campaigns, ad groups or keywords under one automated strategy, shares performance data across them to speed learning, and reallocates budget toward better-performing campaigns.
- Use it when several campaigns share one goal (e.g. a 700% ROAS across all non-brand campaigns), when you want automatic budget reallocation on real-time signals, or when you need bid caps and floors.
- Apply the Max CPC cap guardrail: an ecommerce advertiser on tROAS seeing CPC spikes to $25 on low-demand days switched to portfolio bidding with a Max CPC of $9, preventing budget blowouts while still letting Smart Bidding chase the ROAS goal.
- Use bid floors to compete more aggressively where that is the goal; caps and floors are only available through portfolio bidding, even for a single campaign.
- Do not use portfolio bidding when campaigns have fundamentally different goals (clearance inventory vs new arrivals), when you need manual control over individual campaign bids, or when campaigns are too low-volume to benefit from pooled machine learning.
Caveat: The $25 spike and $9 cap are one advertiser's example; set caps from your own margin and CPC distribution.

Tags: google-ads, portfolio-bidding, bid-caps, smart-bidding, budget-management, cpc
Source: # Google Ads for Ecommerce_ The Complete Architecture & Operations Manual (2026 Edition).docx

---

## Pass Five Gates Before Scaling Ecommerce Spend
Use when: Deciding whether to increase budget or add campaign types in an ecommerce Google Ads account.
- Gate 1 — Feed health: do not scale until disapprovals are cleared and warnings addressed; disapproved products are ineligible and scale amplifies feed problems rather than solving them.
- Gate 2 — Conversion tracking integrity: validate end to end before scaling — enhanced conversions active, server-side tags firing, conversion values reflecting actual order revenue. Scaling on inaccurate data teaches the algorithm the wrong outcomes.
- Gate 3 — Brand/non-brand separation: keep brand and non-brand in separate campaigns with separate budgets and reporting, because blended ROAS distorts scaling decisions.
- Gate 4 — Asset and creative velocity: PMax needs 15+ images and 5+ videos per asset group refreshed every 4-6 weeks, and Demand Gen needs continuous refresh; lifestyle imagery, UGC video and product demos are the highest-leverage types for ecommerce.
- Gate 5 — Bid strategy maturity: wait for roughly 50 conversions per month for basic stability (more in competitive auctions) before moving from Maximize Conversions to Target ROAS.
- Apply the operating principle: PMax performance is a function of input quality — feed data, conversion signals, audience signals and creative assets — not of trying to control the algorithm's output distribution.
- If a gate fails, invest in better product titles, clearer attribute mapping and intent-based custom-label segmentation rather than increasing budget.
Caveat: The ~50 conversions/month threshold is a source heuristic for Smart Bidding stability; highly competitive auctions may need more.

Tags: google-ads, scaling, readiness-checklist, performance-max, smart-bidding, operations
Source: # Google Ads for Ecommerce_ The Complete Architecture & Operations Manual (2026 Edition).docx

---

## Choose Between PMax, Shopping and Demand Gen by Job
Use when: Assigning budget and roles across Google Ads campaign types for an ecommerce catalog as the account grows.
- For catalog and multi-surface acquisition, run PMax at roughly 50-70% of budget, segmented by product category or performance tier; the algorithm allocates across Search, Shopping, YouTube, Discover, Display, Gmail and Maps.
- For branded and high-intent category terms, run Standard Shopping at roughly 30-50% of budget with tROAS targets and manual product-group bid levers; it serves only the Shopping surface but gives control and transparency.
- For upper-funnel discovery, run Demand Gen at roughly 10-20% of budget with product feed integration to create a virtual storefront.
- Use the distinction that PMax automates asset combination while Demand Gen lets you upload, preview and edit specific combinations per placement.
- Watch the overlap: PMax and Standard Shopping bid against the same feed, and since campaign type no longer confers auction priority, they will cannibalise without role rules.
- Layer Demand Gen in only after high-intent campaigns are stable — for smaller accounts the source recommends mastering conversion campaigns first.
Caveat: Budget percentages are the source's suggested structure and vary with catalog size, margin and seasonality.

Tags: google-ads, campaign-architecture, budget-allocation, performance-max, standard-shopping, demand-gen
Source: # Google Ads for Ecommerce_ The Complete Architecture & Operations Manual (2026 Edition).docx

---

## Anchor ROAS Targets to Margin, Not Benchmarks
Use when: Setting or defending a target ROAS for an ecommerce account, or benchmarking account performance against market figures.
- Use the source's 2026 figures as context only: median ecommerce Google Ads ROAS 557% (5.57×, Optmyzr Q2 2026), average ROAS 3.4× (COREPPC 2026), Shopping 5.1×, PMax 4.8×, non-brand Search 3.4×; average CPCs $1.42 Search, $0.68 Shopping, $0.82 PMax; ecommerce conversion rate 2.8%.
- Treat the gradient as directional rather than a mandate: Shopping and PMax benchmarks read higher than non-brand Search in these sources, but that reflects surface and traffic mix, not a guarantee for your account.
- Adjust every benchmark for vertical, order value and margin structure before using it as a target.
- Apply the margin rule directly: a brand with 60% margins can profitably scale at a lower ROAS than a brand with 25% margins — set target ROAS relative to gross margin, not industry averages.
- Note the trend context: median ecommerce Google Ads ROAS was 3.68 in 2025, down 10.03% year over year, reflecting more competition and rising CPCs, and Shopping CPCs are up 22% year over year — so targets set on older data may be too aggressive.
- Combine with AOV and LTV when judging whether a given ROAS is acceptable; a low-ROAS first order can still be profitable when repeat purchase is strong.
Caveat: These are third-party benchmark aggregates from specific reports (Optmyzr, COREPPC, Web Tonic) cited by the source; they are not targets and vary widely by vertical.

Tags: google-ads, roas-benchmarks, target-roas, margin-management, measurement, aov
Source: # Google Ads for Ecommerce_ The Complete Architecture & Operations Manual (2026 Edition).docx

---

## Four-Layer Google Ads Account Model for Ecommerce
Use when: You are architecting or restructuring a full Google Ads account (typically $50K–$500K/month spend) and deciding which campaign types to run and how they relate.
- Assign each layer a distinct job: AI Max for Search captures net-new long-tail and conversational queries with low competition and cheap clicks; Performance Max handles full cross-channel conversion; Demand Gen fills the top of funnel with awareness; branded/non-brand Search harvests conversion-ready demand.
- Treat the layers as interdependent: Demand Gen warms audiences that PMax and Search later convert, so when the assist layer is removed, expect branded performance to drop weeks later rather than immediately — track it across a long enough window to see the causal lag.
- Budget the discovery and assist layers even though their direct ROAS looks weaker, because their contribution shows up downstream in branded and PMax conversion volume.
- Keep role separation explicit so PMax does not absorb branded and high-intent Shopping traffic (see cannibalisation control).
- Validate current campaign-type availability and behaviour against the live Google Ads interface before restructuring, since platform mechanics change.
Caveat: Source describes this as the pattern of high-spend ecommerce advertisers; it is an operating heuristic, not a guaranteed result at any spend level.
Caveat: Layer names and behaviours are dated to the 2026 edition and should be re-checked.

Tags: google-ads, account-structure, performance-max, demand-gen, search-campaigns, full-funnel, budget-allocation
Source: # The Complete Google Ads Architecture & Operations Manual (2026 Edition).docx

---

## Feed-Only Performance Max for a Feed-Led Retail Test
Use when: Evaluating a feed-led versus full-asset Performance Max campaign for an ecommerce product catalog.
- Confirm Merchant Center linkage, eligible products, accurate prices and stock, and tested purchase-value tracking.
- Treat the source feed-only approach as a test of reduced manually supplied creative. Review the actual asset-generation and URL-expansion settings in the current interface.
- Monitor channel delivery, product performance and new versus returning customer outcomes; compare contribution and acquisition cost with the existing Shopping or full-asset setup.
- Do not classify the campaign as remarketing-only or promise Shopping-only delivery. Use a campaign with appropriate audience controls when strict remarketing is required.
Caveat: Editorial correction: PMax audience signals do not impose strict targeting; omitting manual creative does not guarantee placement isolation. https://support.google.com/google-ads/answer/14530785
Caveat: Merchant Center data can generate assets automatically. Source examples of efficient feed-led campaigns are not delivery guarantees. https://support.google.com/google-ads/answer/15865151

Tags: google-ads, performance-max, feed-engineering, placement-exclusions, shopping, budget-control
Source: # The Complete Google Ads Architecture & Operations Manual (2026 Edition).docx

---

## Stop PMax and Shopping Cannibalising Brand Demand
Use when: PMax and Shopping run against the same feed and you suspect PMax is absorbing branded and high-intent queries, destroying cost transparency on your most valuable searches.
- Add branded negative keywords and brand exclusions to PMax campaigns so PMax cannot bid on branded queries.
- Add negative keywords to new-customer-acquisition Search and Shopping campaigns so they do not absorb branded demand and get falsely credited.
- Create dedicated branded Search and Shopping campaigns to collect only branded traffic, with uncapped budget relative to search volume — losing brand impression share to a competitor is one of the most avoidable ways to lose pipeline.
- Optimise branded campaigns on efficiency metrics (ROAS, CPC, impression share), not growth metrics.
- Use feed duplication with strict role rules: the Shopping feed optimised for branded and high-intent category terms, the PMax feed optimised for discovery and scaling, so both can surface products across eligible auctions without sacrificing efficiency.
- Confirm the current location of brand exclusion settings (account vs campaign level) in the live interface.
Caveat: Splitting traffic will initially make your account-level ROAS look worse because brand efficiency no longer flatters non-brand; that is the intended transparency gain.
Caveat: Source presents this as the single most common structural failure; treat it as a frequent pattern, not a claim about every account.

Tags: google-ads, performance-max, brand-segmentation, cannibalisation, shopping, feed-engineering, negative-keywords
Source: # The Complete Google Ads Architecture & Operations Manual (2026 Edition).docx

---

## Configure Demand Gen as the Assist Layer
Use when: You need a top-of-funnel demand-creation layer in Google Ads and are setting up Demand Gen campaigns, structure, bidding and pacing for ecommerce.
- Start with separate campaigns for remarketing and prospecting — they have different goals and need different creative and bid strategies. Optionally split again by placement type (Shorts-only, in-stream-only, image surfaces) to isolate performance.
- Choose a bidding approach from the six supported (Target CPA, Target ROAS, Target CPC, Maximize conversions, Maximize conversion value, Maximize clicks). The source recommends starting on Maximize Conversions to accumulate data, then moving to Target CPA or Target ROAS after roughly 50 conversions.
- Let campaigns run at least 30 days before iterating.
- Plan for creative velocity as the operational bottleneck: Demand Gen is a 'content monster,' and if creative refresh stops, the whole stack starves.
- Optimise using Reach Planner or Performance Planner for bid and budget recommendations, and use the in-UI tCPA Scaling Simulator to forecast traffic impact before scaling.
- On always-on campaigns, increase bids 5–10% (never more than 15%) every 5–7 days rather than making one large change.
- Verify current Demand Gen placements and bidding options; placements such as Google Maps were added mid-2026.
Caveat: The ~50-conversion switch point is a source heuristic for when data is sufficient, not a hard platform rule.
Caveat: Demand Gen inventory and formats change frequently; confirm available surfaces before planning creative.

Tags: google-ads, demand-gen, full-funnel, campaign-setup, bidding-strategy, creative-velocity, scaling
Source: # The Complete Google Ads Architecture & Operations Manual (2026 Edition).docx

---

## Match YouTube Ad Formats to Funnel Stage
Use when: You are planning video assets for a Google Ads stack and must decide which format to produce and which campaign type to run it in.
- Use Skippable In-Stream (YouTube videos, GVP interstitials; no length limit, ≤3 min recommended) for consideration and TrueView views.
- Use In-Feed (YouTube Home, Search, Watch Next; no length limit) for discovery-stage engagement.
- Use Non-Skippable In-Stream (15–60 sec, varies) when you need full message delivery.
- Use Bumper (6 sec, 5 sec min) for frequency and awareness.
- Use YouTube Shorts (≤60 sec recommended) for mobile-optimised engagement.
- Use Masthead (YouTube Homepage; no length limit, ≥10 sec recommended; CPM/CPH) for mass awareness.
- Note compatibility when allocating: Skippable In-Stream, In-Feed and Shorts work with Demand Gen, Video View campaigns, Video Reach campaigns and Performance Max; Bumper and Masthead are restricted to Video Reach and Reservation campaigns respectively.
- Migrate any legacy YouTube Video Action line items to Demand Gen, since those were paused and archived on February 28, 2026; YouTube audio ads were restricted to Pandora/SiriusXM in the US as of September 1, 2026.
Caveat: Format availability, length caps and campaign-type compatibility are platform facts subject to change; validate against the live interface.
Caveat: YouTube is positioned as a surface within Demand Gen and PMax rather than a standalone campaign destination.

Tags: google-ads, youtube, demand-gen, creative-strategy, video-ads, campaign-setup
Source: # The Complete Google Ads Architecture & Operations Manual (2026 Edition).docx

---

## How the Google Ads Auction Actually Works
Use when: You are diagnosing why a higher bid is not winning position, or explaining to a stakeholder why budget alone cannot buy placement.
- Recognise that Google weighs several factors simultaneously: your maximum bid (or Smart Bidding target); auction-time quality signals (expected CTR, ad relevance, landing page experience); the expected impact of ad assets (sitelinks, callouts, structured snippets, image extensions); auction competitiveness for that exact query; and user context such as location, device, time, language and query characteristics.
- Stop treating the auction as a simple bidding war. A well-built ad with a strong, relevant landing page can win a higher position at lower cost than a competitor bidding more.
- Respond to lost impressions by improving auction-time quality (ad relevance, expected CTR, landing page experience) rather than only raising bids.
- Add and maintain ad assets/extensions, since their expected impact is part of the ranking calculation.
- Remember the auction repeats for each search; there is no persistent position you own from a previous auction.
Caveat: Google does not publish the exact live weighting; the description here synthesises official documentation and operator analyses current as of September 2026.
Caveat: Contextual factors mean the same bid and ad can rank differently by device, location and time.

Tags: google-ads, auction-mechanics, ad-rank, quality-score, bidding-strategy, diagnostics
Source: # The Complete Google Ads Architecture & Operations Manual (2026 Edition).docx

---

## Ad Rank Formula and Position Threshold Heuristics
Use when: You are estimating how much bid headroom you need for top-of-page or top-3 placement, or modelling whether raising Quality Score beats raising bids.
- Use the operator-grade formula: Ad Rank = Max CPC Bid × Quality Score × Expected Impact of Extensions/Formats + Contextual Adjustments. In simplified teaching form, Ad Rank = Bid × Quality Score.
- Note that Ad Rank is calculated twice per auction — first to establish eligibility (whether your ad can show at all), then again to order the eligible ads.
- Apply the practical implication: a $3 bid with Quality Score 10 (Ad Rank = 30) beats a $5 bid with Quality Score 5 (Ad Rank = 25). Higher Quality Score directly reduces the CPC needed to hold a given position.
- Account for the minimum Ad Rank threshold below which no ad shows; two ads with the same bid can show in different positions based on Quality Score.
- Use the source's 2026 threshold heuristics for planning: brand-new accounts typically need top-of-page Ad Rank around 6–10; top-3 in mid-competitive markets requires approximately 30; the #1 position usually requires Ad Rank of 50 or higher. Brand-keyword Ad Rank for owners is typically dominant due to Quality Score of 9+.
- Treat these numbers as orientation only — they vary by market and account and are not published platform thresholds.
Caveat: The stated Ad Rank thresholds (6–10 top-of-page, ~30 top-3, 50+ for #1) are source-specific heuristics, not official Google figures.
Caveat: Contextual adjustments make strict arithmetic predictions unreliable.

Tags: google-ads, ad-rank, quality-score, auction-mechanics, bidding-strategy, measurement
Source: # The Complete Google Ads Architecture & Operations Manual (2026 Edition).docx

---

## Use Quality Score as a Diagnostic, Not a Currency
Use when: You are prioritising between ad copy testing and landing page work to improve Quality Score and reduce CPC.
- Understand that the auction reads expected CTR, ad relevance and landing page experience in real time; the visible Quality Score is only a summary diagnostic of those signals, not an input the auction consumes.
- Work with the 2026 component weighting: 1 base point + up to 3.5 points for expected CTR + up to 3.5 points for landing page experience + up to 2.0 points for ad relevance — approximately 39% expected CTR, 39% landing page experience, 22% ad relevance.
- Act on the operational implication: landing page experience is as important as ad copy for Quality Score, so if you are over-investing in ad copy tests and under-investing in landing page relevance, speed and mobile experience, rebalance that effort — landing page experience evaluates load speed, mobile responsiveness, content relevance to the query, and ease of finding the conversion action.
- Improve expected CTR (a forward-looking per-auction prediction, not your historical CTR) through ad copy testing, extension use, match type refinement and query-to-ad alignment.
- Improve ad relevance through tight ad group theming, keyword-to-ad-copy alignment, and landing page content matching the query's specific intent.
- Confirm current weighting presentation in the live interface, as Google does not guarantee a stable formula.
Caveat: Component weights are approximate for 2026 and not published as a contractual formula.
Caveat: Quality Score is not used to calculate your cost directly; actual CPC depends on competitors' Ad Rank and your own quality signals.

Tags: google-ads, quality-score, landing-page, ad-relevance, conversion-optimization, diagnostics, product-page
Source: # The Complete Google Ads Architecture & Operations Manual (2026 Edition).docx

---

## Second-Price Logic: Why Higher Quality Lowers Actual CPC
Use when: You are justifying investment in ad relevance and landing page quality to reduce cost per click, or explaining why a competitor with a bigger bid pays more for a worse position.
- Stop planning around your maximum bid. You pay the minimum amount required to beat the Ad Rank of the advertiser immediately below you.
- Apply the simplified formula: Actual CPC = (Ad Rank of the advertiser below you ÷ Your Quality Score) + $0.01.
- Recognise the double effect: Ad Rank appears in the numerator (competitor's Ad Rank) and your Quality Score in the denominator, so a higher Quality Score directly reduces your actual CPC for the same auction position.
- Use this as the economic argument for quality work: a competitor with a higher bid but lower Quality Score may pay more than you for a lower position.
- When you want to reduce CPC on a profitable keyword without reducing position, prioritise quality improvements (expected CTR, landing page experience) over bid reductions.
- Re-verify the formula's current public documentation before using it in budgeting models.
Caveat: Google does not publish the exact live CPC formula; this is an operator-grade simplification.
Caveat: The formula assumes a competitor exists below you in the auction; edge cases differ.

Tags: google-ads, auction-mechanics, cpc, quality-score, bidding-strategy, measurement
Source: # The Complete Google Ads Architecture & Operations Manual (2026 Edition).docx

---

## Smart Bidding Basics, Relabelling and Seasonality Adjustments
Use when: You are choosing a bid strategy, interpreting the 2026 strategy labels, or deciding whether to apply a seasonality adjustment around a promotion.
- Understand auction-time bidding: instead of one static keyword bid, Smart Bidding adjusts the bid for each specific auction based on device, location, time of day, query characteristics, audience membership and many other contextual factors.
- Read the 2026 relabelling correctly: from June 2026, 'Maximize conversions with a Target CPA' became 'Target CPA' and 'Maximize conversion value with a Target ROAS' became 'Target ROAS,' now standalone options separated from the un-targeted Maximize conversions and Maximize conversion value strategies. Underlying behaviour is unchanged — only labels were clarified.
- Apply seasonality adjustments only for predictable, short-term conversion-rate changes of 1–7 days caused by unprecedented reasons such as a promotion.
- Do not use seasonality adjustments for predictable seasonal mix shifts (back-to-school, holidays) or for periods longer than 7 days — Smart Bidding accounts for those naturally.
- Check the current strategy names and adjustment options in the live interface, since labels changed mid-2026.
Caveat: Strategy naming and available options are subject to change; validate before configuring.
Caveat: Relabelling does not change bidding behaviour, so do not expect performance differences from the rename alone.

Tags: google-ads, smart-bidding, target-cpa, target-roas, seasonality, bidding-strategy
Source: # The Complete Google Ads Architecture & Operations Manual (2026 Edition).docx

---

## Treat the Product Feed as the Advertising Copy
Use when: You are optimising Google Shopping or Performance Max for ecommerce and deciding where to spend merchandising and copywriting effort.
- Accept that your feed is not a data source but the advertising itself: Google scans titles, descriptions, attributes, pricing and availability and decides on its own which search queries each product matches.
- Therefore treat the product title as the most important line of advertising copy you will write, because it determines what Google thinks you sell and who to show it to.
- Front-load the attributes buyers actually search with (structure below) rather than leading with brand and model name.
- Maintain accuracy of price and availability so Google's matching and any automatic item updates stay aligned with your landing pages.
- Re-audit the feed whenever you add categories or price tiers, since matching is driven by feed content, not keyword bids.
- Confirm current matching behaviour in Google Merchant Center documentation, as the algorithm evolves.
Caveat: Source's claim that the title is 'the most important line of advertising copy you will ever write' is a strong practitioner opinion specific to feed-led campaigns.
Caveat: Feed classification errors can cause a well-written title to still match poorly.

Tags: google-ads, google-merchant-center, feed-engineering, product-titles, performance-max, shopping, product-page
Source: # The Complete Google Ads Architecture & Operations Manual (2026 Edition).docx

---

## Product Title Architecture for Feed Matching
Use when: You are writing or rewriting product titles for a Google Merchant Center feed to improve query matching in Shopping and PMax.
- Apply the proven 2026 structure: Product Type → Material → Colour → Fit/Size → Key Feature → Brand (last).
- Recognise why this inverts the common manufacturer-title pattern (Brand + Product Name): brand-led titles often bury the matching attributes beyond the first 70 characters, and Google's matching algorithm weights the first 70 characters most heavily.
- Put the attributes buyers type into that first 70-character window so they carry the match.
- Keep titles between 60 and 150 characters; everything after the first ~70 characters is supplementary.
- Avoid keyword stuffing — Google's algorithm penalises unnatural attribute density.
- Consider the alternative structure [Brand] + [Product Type] + [Key Feature] + [Model] + [Colour/Size] where it performs better in your vertical, but keep the attribute order identical across the entire catalog so the algorithm can learn reliable patterns.
- Use supplemental feeds — an often-overlooked lever in GMC — to override titles, product types and custom labels without touching your website or primary feed; test title variants, apply promotional labels and isolate product sets for different campaign roles. Tools like Channable can sync optimised titles to GMC via supplemental feeds.
Caveat: Google does not publish an exact 70-character weighting rule; treat this as an operator heuristic from the source.
Caveat: Consistency matters as much as any single structure — mixed attribute orders across the catalog degrade pattern learning.

Tags: google-ads, feed-engineering, product-titles, google-merchant-center, shopping, supplemental-feed, seo
Source: # The Complete Google Ads Architecture & Operations Manual (2026 Edition).docx

---

## Feed Health Diagnostics and Disapproval Remediation
Use when: You are doing routine Google Merchant Center maintenance or fixing disapprovals that are costing you Shopping and free-listing eligibility.
- Start in Google Merchant Center → Products → Diagnostics, which shows all products with issues categorised by severity.
- Filter Disapproved first — disapproved products are ineligible for all Shopping ads and free listings, so they represent immediate revenue loss.
- Then filter Warnings and Limited performance — these products are approved but underperforming, representing optimisation opportunities rather than lost eligibility.
- Know the five most common 2026 disapproval causes: missing or incorrect GTINs; price mismatch between feed and landing page; missing shipping information; policy violations (restricted products, misrepresentation); incorrect feed formatting or missing required attributes. Each appears in the Item Issues tab with specific affected SKUs and a View & edit option.
- Use the Fix type filter to isolate auto-fixable items (low-risk issues such as formatting errors and missing optional attributes), select all and run Autofix. Do manual fixes for policy violations, pricing mismatches and missing required attributes.
- Note that every change made through GMC's interface is reversible within 30 days — useful when trialling fixes.
- Prevent rather than repair: pre-validate the whole catalog before Google sees the feed using tools like SmartFeed or Feedonomics. For dynamic pricing, raise feed update frequency to at least every 6 hours and enable automatic item updates in GMC settings so Google can use crawled prices when feed prices lag.
- Verify current Diagnostics navigation and Autofix availability in the live Merchant Center interface.
Caveat: Autofix does not cover policy or pricing issues and should not be relied on as a complete remediation strategy.
Caveat: Third-party validation tool names are suggestions, not requirements; evaluate them against your catalog size.

Tags: google-ads, google-merchant-center, feed-engineering, disapprovals, diagnostics, operations, pricing
Source: # The Complete Google Ads Architecture & Operations Manual (2026 Edition).docx

---

## Conversion Tracking Tag Architecture via GTM
Use when: You are setting up or auditing Google Ads conversion tracking for an ecommerce store, including checkout purchase events.
- Build the layered tag structure: (1) Conversion Linker tag to enable Google Ads to send data to Tag Manager, set to fire on All Pages in most cases; (2) a GA4 Event tag defining the key event in the web container — a recommended event name (purchase, generate_lead, sign_up) or a custom event; (3) a Google Ads Conversion Tracking tag that fires when the key event occurs, using the Conversion ID and label from your Google Ads account.
- Move to server-side GTM where volume justifies it: this places conversion tags on your server, reduces page code, improves page load speed, and provides more resilient tracking under browser restrictions. The server container requires a Conversion Linker tag, a GA4 client and the Ads Conversion Tracking tag configured with the correct conversion ID and label.
- For product feed clicks, use the tracking template in Google Ads rather than hard-coding parameters in Google Merchant Center, keeping tracking centralised and easier to update across campaigns.
- Host the server container on a cloud provider (Google Cloud, Stape or similar).
- Validate the full path end-to-end before scaling spend — a misfiring purchase tag teaches bidding algorithms the wrong outcome.
- Confirm current GTM tag names and setup steps in the live Tag Manager interface.
Caveat: Source notes server-side GTM is increasingly the default for accounts spending above $50K/month — a spend-based heuristic, not a hard requirement.
Caveat: Server container hosting introduces infrastructure you must maintain; outages stop conversion recording.

Tags: google-ads, conversion-tracking, google-tag-manager, server-side-tracking, checkout, measurement, gtm
Source: # The Complete Google Ads Architecture & Operations Manual (2026 Edition).docx

---

## Enhanced Conversions Setup and Diagnostics
Use when: You are improving ecommerce conversion measurement accuracy or diagnosing why conversion counts look undercounted versus backend orders.
- Understand what enhanced conversions do: they supplement standard conversion tags by sending hashed first-party customer data — email addresses, phone numbers, names — in a privacy-safe way. The hashed data is compared to hashed data from signed-in Google Accounts and attributed to ad events, improving measurement accuracy and bidding performance. Data is hashed client-side or server-side before transmission; Google never receives raw PII.
- Note the 2026 setup changes: from April 2026 Google Ads accepts user-provided data from website tags, Data Manager and API connections simultaneously, so you no longer choose between implementation methods. From June 2026, enhanced conversions for web and for leads are combined into a single on/off setting and method selections disappear from the account interface.
- In GTM, open the Google Ads Conversion tag and enable 'Include user-provided data,' then map data-layer variables for the email, phone and address fields collected during checkout or form submission. The tag hashes the data and includes it in the conversion ping to Google Ads.
- Use it especially where conversions are valuable and long-cycle: it helps match conversion events back to signed-in Google Accounts.
- Check the enhanced conversions diagnostics report in Google Ads to identify and self-diagnose implementation issues. Common problems are missing or incorrectly formatted user-provided data, incorrect in-page code, and data-layer variable mismatches. Work through the implementation checklist before launch.
- Verify the current unified setting location and diagnostics report in the live interface, since UI changed mid-2026.
Caveat: Requires valid, consented first-party data collection — do not assume you can send PII without a lawful basis and hashing.
Caveat: Setup nuances changed in 2026; older tutorials may reference removed method-selection screens.

Tags: google-ads, enhanced-conversions, conversion-tracking, google-tag-manager, measurement, privacy, checkout
Source: # The Complete Google Ads Architecture & Operations Manual (2026 Edition).docx

---

## Server-Side Tracking for Page Speed and Data Durability
Use when: You are evaluating whether to move conversion tracking server-side, or troubleshooting declining measured conversions in ecommerce.
- Weigh the three benefits: improved page speed because conversion tags run on the server rather than in the user's browser; more durable tracking because server-side tags are less affected by browser privacy restrictions; and better data quality because server-side data can be enriched with CRM and backend signals before transmission.
- Set up a server container hosted on a cloud provider (Google Cloud, Stape or similar).
- Configure a GA4 client to receive incoming events.
- Configure the Ads Conversion Tracking tag in the server container to forward conversions to Google Ads.
- Configure the Conversion Linker tag in the server container as well, so Google Ads can send data to Tag Manager.
- Consider this especially for accounts above roughly $50K/month spend, which the source identifies as increasingly the default tier for server-side setups.
- Validate conversions in both the browser and server path after migration and reconcile against backend order counts.
- Verify current vendor options and GTM server-container configuration steps before building.
Caveat: The $50K/month threshold is a source heuristic, not a platform requirement.
Caveat: Server-side tracking adds infrastructure you must host and monitor; if the container fails you lose conversion recording.

Tags: google-ads, server-side-tracking, google-tag-manager, conversion-tracking, measurement, page-speed, privacy
Source: # The Complete Google Ads Architecture & Operations Manual (2026 Edition).docx

---

## Intent-Tiered Keyword Research Workflow
Use when: You are planning or restructuring a Search campaign's keyword strategy for an ecommerce store.
- Replace feature- or volume-led keyword research with organisation by buyer intent tier and build a four-tier structure.
- Tier 1 — Transactional: queries like '[category] software,' '[category] pricing,' '[category] for [industry].' These searchers are close to a decision; give them the highest bids and the most specific landing pages. This is the profit centre of the account.
- Tier 2 — Comparison: queries like '[competitor] alternative,' '[your category] vs [competitor].' These searchers are evaluating; use comparison-focused ad copy and landing pages, kept in separate ad groups or campaigns so they can be measured and bid independently.
- Tier 3 — Problem-Aware: broader, higher-volume terms describing a pain point rather than a solution category. These convert at a lower rate, attract irrelevant traffic most easily, and need the tightest negative keyword coverage and the lowest starting bids.
- Tier 4 — Competitor: queries bidding on rival product names. Isolate these with their own budget cap — they almost always have lower CTR and higher CPC than brand campaigns — and evaluate them on their own conversion-to-pipeline rate rather than blended into account performance.
- Build long-tail clusters intentionally rather than chasing head terms: long-tail has lower CPC, less auction pressure, cleaner conversion signal, and compounds horizontally across markets, angles and variations rather than exploding vertically. Treat it as margin engineering, not volume chasing.
Caveat: Tier examples are framed around software and services; adapt the query patterns to physical-goods ecommerce language.
Caveat: The claim that head-term chasing is an 'ego' pursuit is the source's opinion.

Tags: google-ads, keyword-research, intent-tiering, search-campaigns, long-tail, negative-keywords, acquisition
Source: # The Complete Google Ads Architecture & Operations Manual (2026 Edition).docx

---

## Brand vs Non-Brand Segmentation and ROAS Distortion
Use when: You are deciding how to split budget and reporting between brand and non-brand Search/Shopping, or diagnosing suspiciously stable account-level ROAS.
- Apply the core principle: brand traffic captures demand, non-brand traffic creates it. Mixing them distorts your data, and when your data lies, your scaling decisions get expensive.
- Run brand campaigns to protect searches for your product name and close variants: typically cheap, converting well, and defending against competitors bidding on your name. Give them uncapped budget relative to search volume and optimise on efficiency metrics (ROAS, CPC, impression share) rather than growth metrics.
- Direct most budget and testing effort to non-brand campaigns targeting category and problem-aware terms where the prospect has not chosen a vendor. Segment non-brand by awareness depth — problem-aware, solution-aware, product-aware and competitor-aware — because each cluster has different ROAS expectations, bid aggression levels and creative angles. Intent is not equal, so bidding should not be either.
- Implement the three-part separation mechanic: branded negatives and brand exclusions on PMax; negatives on new-customer-acquisition Search and Shopping campaigns; dedicated branded Search and Shopping campaigns collecting only branded traffic.
- Diagnose the ROAS distortion problem: in many accounts brand terms take only about 11% of search spend but carry 34% of conversions, which flatters total reported ROAS and masks true non-brand prospecting performance.
- After separation, evaluate whether non-brand is genuinely profitable or merely subsidised by brand efficiency.
- Re-check the source's illustrative percentage split against your own data rather than assuming the same ratio.
Caveat: The 11% spend / 34% conversion split is a source observation from many accounts, not a benchmark you should target.
Caveat: Separating brand will initially reduce reported blended ROAS — that is the point, not a failure.

Tags: google-ads, brand-segmentation, roas, measurement, search-campaigns, acquisition, budget-allocation
Source: # The Complete Google Ads Architecture & Operations Manual (2026 Edition).docx

---

## Surface-Area Catalog Scaling with Feed Duplication
Use when: You are deciding whether you have enough catalog to scale Shopping/PMax, or looking for a way to increase impressions without raising bids.
- Internalise the concept: surface area is the link between catalog size and algorithmic opportunity. PMax and Standard Shopping both bid against your product feed but need enough catalog breadth to find pockets of profitable demand. Under 30 SKUs you do not have enough surface area for the algorithm to find viable pockets at scale.
- Apply the planning thresholds: for Demand Gen with product feeds, aim for at least 50 approved products as a minimum, with larger catalogs benefiting from up to 10,000 products. Campaigns with as few as one product are technically supported, but at least four products are recommended to maximise eligibility across all ad placements.
- Use feed duplication as a scaling lever: when you duplicate the feed with distinct rules for Shopping and PMax, both campaigns can surface products more frequently across eligible auctions without sacrificing efficiency.
- Structure as PMax for scale (multi-surface acquisition, 70–80% of budget) and Standard Shopping for precision (branded and high-intent category terms, 20–30% of budget).
- Consider segmenting PMax by intent layer — a prospecting PMax with broad signals and a high-priority feed, plus a separate PMax for remarketing or brand defence with different asset groups and audience signals — so each gets a cleaner learning environment and prospecting is not starved of data by brand-driven conversions.
- Treat the documented case result (Shopping coverage rising from 49% to 57% in one month after feed duplication with strict role separation) as an illustration, not a guaranteed outcome.
Caveat: The 30-SKU and 50-product figures are source guidance for scale, not platform minimums (except where Google technically requires four products for full eligibility — verify current requirements).
Caveat: The 70/20 budget split is a suggested hybrid structure, not a universal rule.

Tags: google-ads, surface-area-scaling, feed-engineering, performance-max, shopping, product-selection, budget-allocation
Source: # The Complete Google Ads Architecture & Operations Manual (2026 Edition).docx

---

## Target ROAS vs Maximize Conversion Value
Use when: You are selecting a bid strategy for a Shopping or PMax campaign and setting the initial tROAS value.
- Read the 2026 labels correctly: as of June 2026, 'Maximize conversion value with a Target ROAS' is labelled simply 'Target ROAS' and is a standalone strategy; 'Maximize conversion value' without a target remains separate for driving as much conversion value as possible within a fixed budget.
- Choose Target ROAS when your goal is a desired return on ad spend across a campaign or portfolio, and especially when conversion values vary significantly — ecommerce where a $200 order and a $20 order require different bid economics.
- Report revenue or values associated with conversions before switching to Target ROAS, otherwise the algorithm has no value signal to optimise against.
- Choose Maximize Conversion Value when the goal is maximum conversion value within a set budget with no fixed ROAS constraint — appropriate during growth phases when you accept a lower marginal ROAS to capture additional volume.
- Apply the guardrail when setting Target ROAS: start 10–15% below your current actual ROAS to give the algorithm room to learn and expand. A tROAS set too high on a cold campaign starves delivery and prevents the algorithm from gathering optimisation data.
- Once the campaign is stable at the lower target, step it up incrementally and monitor impression share and conversion volume.
- Note that in Standard Shopping, Maximize Conversion Value is now available without a Target ROAS requirement (July 2026), adding flexibility to controlled Shopping setups.
Caveat: The 10–15% below-current-ROAS starting rule is a source heuristic; the source says a tROAS 'set too high' starves delivery, which is a directional claim, not a proven threshold for every account.
Caveat: Strategy labels changed in June 2026; older documentation may use the previous names.

Tags: google-ads, target-roas, bidding-strategy, performance-max, shopping, scaling, measurement
Source: # The Complete Google Ads Architecture & Operations Manual (2026 Edition).docx

---

## Portfolio Bid Strategies for Stabilised Scale and Bid Guardrails
Use when: You have multiple campaigns chasing the same ROAS or CPA goal, or you need a Max CPC cap to stop Smart Bidding budget blowouts.
- Understand what portfolio bidding does: it groups multiple campaigns, ad groups or keywords under a single automated strategy (Target ROAS, Target CPA, Maximize conversions, Maximize conversion value, Maximize clicks or Target impression share), then adjusts bids across the portfolio to hit the shared goal. It shares performance data across campaigns, speeding up learning, and reallocates budget to better-performing campaigns automatically.
- Use portfolio bidding when multiple campaigns share the same performance goal (e.g. a 700% ROAS or $50 CPA); when you want the platform to shift budget and adjust bids across campaigns automatically; when you need bid caps and bid floors, which are only available through portfolio bidding even for a single campaign; or when you need more Smart Bidding control, such as a Max CPC cap to prevent spikes or a bid floor to compete more aggressively.
- Consider the Max CPC cap use case: a B2B advertiser on tCPA saw CPC spikes up to $25 on low-demand days. Switching to portfolio bidding with a Max CPC of $9 created a guardrail against budget blowouts while keeping enough flexibility to optimise toward the $30 CPA goal.
- Avoid portfolio bidding when campaigns have fundamentally different goals (e.g. brand awareness vs conversion-driven), when you need manual control over individual campaign bids, or when campaigns are low-volume and cannot generate enough conversions to benefit from pooled machine learning.
- For multi-account work: when every account in an MCC shares the same currency, you can include campaigns from multiple countries in an MCC-level portfolio bid strategy — particularly valuable for smaller markets that individually lack conversion volume to train Smart Bidding, since pooling with larger markets accelerates learning and stabilises performance.
- Verify current portfolio bidding UI and MCC-level support in the live interface.
Caveat: The B2B $25 spike / $9 cap / $30 CPA example is a source case illustration, not a benchmark for your account.
Caveat: Pooling low-volume campaigns can drag down a portfolio if goals or economics genuinely differ.

Tags: google-ads, portfolio-bidding, bidding-strategy, budget-control, scaling, mcc, target-cpa
Source: # The Complete Google Ads Architecture & Operations Manual (2026 Edition).docx

---

## Five Gates Before Scaling Google Ads Spend
Use when: You are deciding whether to increase budget or scale campaigns, or diagnosing why a scaled campaign underperformed.
- Gate 1 — Feed health: do not scale until feed health is clean. Disapproved products are ineligible for auctions, and warnings and limited-performance items are suppressed in discovery surfaces. Scale amplifies feed problems; it does not solve them.
- Gate 2 — Conversion tracking integrity: do not scale until tracking is validated end-to-end. Enhanced conversions must be active, server-side tags must be firing, and conversion values must be accurate. Scaling on inaccurate conversion data teaches the algorithm to optimise for the wrong outcomes.
- Gate 3 — Brand/non-brand separation: do not scale until brand and non-brand traffic are in separate campaigns with separate budgets and separate reporting. If they are blended, your scaling decisions rest on distorted ROAS data.
- Gate 4 — Asset and creative velocity: scale requires creative throughput. PMax needs 15+ images and 5+ videos per asset group, refreshed every 4–6 weeks; Demand Gen needs continuous creative refresh because it is the fuel layer for the entire stack.
- Gate 5 — Bid strategy maturity: scale only after the campaign has enough conversion data for Smart Bidding to be effective — approximately 50 conversions per month for basic stability, and more in competitive auctions. Move from Maximize Conversions to Target CPA or Target ROAS only after this threshold.
- Apply the operating principle: fix inputs before chasing outputs. PMax performance is a function of input quality — feed data, conversion signals, audience signals and creative assets — not of trying to control the algorithm's output distribution.
- Treat the ~50 conversions/month figure as a source heuristic for basic stability, and validate against your own auction competitiveness.
Caveat: The five gates are the source's framework; it does not prove that passing all five guarantees profitable scale.
Caveat: The 50-conversion-per-month threshold is an approximation, not a platform rule.

Tags: google-ads, scaling, experiment-design, feed-engineering, conversion-tracking, brand-segmentation, performance-max
Source: # The Complete Google Ads Architecture & Operations Manual (2026 Edition).docx

---

## Map Google Ads campaign types to funnel stage before allocating budget
Use when: Deciding which Google Ads campaign types to launch first when moving budget over from Meta or building a new Google account for a DTC store.
- Recognise the six types: Search (keyword text ads, top/bottom of SERP), Shopping (product feed cards with image, price, ratings, delivery), Display (image banners across ~3M sites/apps, strongest for remarketing), Demand Gen (image+video across YouTube Shorts, Discover, Gmail; targets interests/life events/in-market rather than active search), Video/YouTube (Shorts, 6-second bumpers, skippable in-stream after 5s, non-skippable in-stream, in-feed), and Performance Max (all of the above in one campaign).
- Launch in the source's recommended chronological order: Search and Shopping first (bottom/mid funnel), then remarketing and PMax (mid funnel), then Demand Gen last to scale top-funnel demand.
- Treat Search and Shopping as the non-negotiable core — the source argues you will not succeed on Google Ads without nailing these two, and everything else is a bonus.
- Do not spread budget thin across all six types before Search and Shopping are working; layer on the rest once you see success.
- For each type you run, decide whether it is branded or non-branded (Search and Shopping are both split this way) since the economics and purposes differ.
Caveat: PMax is easy to set up but hard to diagnose because it blends all placements — the source does not recommend it for most beginners for exactly that reason.
Caveat: The timing of 'then add PMax and Demand Gen' is not quantified; success of Search/Shopping is the gate, not a fixed date.

Tags: google-ads, campaign-structure, performance-max, shopping-ads, search-ads, demand-gen, channel-expansion
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Split branded and non-branded Search/Shopping to protect and grow
Use when: Structuring Search and Shopping campaigns for a store, particularly when deciding how much budget to put behind the brand name versus generic product queries.
- Run branded Search/Shopping campaigns bidding on your own brand name (e.g. 'Nike' or 'Nike running shoes') to defend against competitors bidding on your brand and capturing traffic already looking for you.
- Run non-branded Search/Shopping campaigns on generic product queries (e.g. 'women's running shoes') as the main new-customer growth lever — this is where a Nike-style brand still shows up to convert shoppers comparing Brooks, Lululemon and Adidas.
- Use low-budget, high-ROAS branded campaigns deliberately as a cheap conversion-data feed for the algorithm, improving the machine learning that then powers the more expensive non-branded, new-customer campaigns.
- Explicitly add your branded terms as exact-match negative keywords inside non-branded campaigns, so brand searches do not get absorbed into non-branded reporting and distort attribution and ROAS.
- Review branded vs non-branded reporting separately — mixing them hides the true cost of acquiring new customers.
Caveat: Branded ROAS is structurally high and should not be used as evidence that your non-branded acquisition is profitable.
Caveat: The source notes the non-branded side is 'much more lucrative' for growth but does not supply cost or ROAS benchmarks for it.

Tags: google-ads, search-ads, shopping-ads, branded-keywords, negative-keywords, attribution, acquisition
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Use a feed-only Performance Max campaign as a feed-led retail test
Use when: Evaluating a feed-led versus full-asset Performance Max campaign for an ecommerce product catalog.
- Confirm Merchant Center linkage, eligible products, accurate prices and stock, and tested purchase-value tracking.
- Treat the source feed-only approach as a test of reduced manually supplied creative. Review the actual asset-generation and URL-expansion settings in the current interface.
- Monitor channel delivery, product performance and new versus returning customer outcomes; compare contribution and acquisition cost with the existing Shopping or full-asset setup.
- Do not classify the campaign as remarketing-only or promise Shopping-only delivery. Use a campaign with appropriate audience controls when strict remarketing is required.
Caveat: Editorial correction: PMax audience signals do not impose strict targeting; omitting manual creative does not guarantee placement isolation. https://support.google.com/google-ads/answer/14530785
Caveat: Merchant Center data can generate assets automatically. Source examples of efficient feed-led campaigns are not delivery guarantees. https://support.google.com/google-ads/answer/15865151

Tags: google-ads, performance-max, merchant-center, retargeting, remarketing, feed-management
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Run Display remarketing against exact previously-viewed products
Use when: Setting up retargeting for a store where shoppers browse product pages or add to cart but do not purchase.
- Install the tagging that records which products a user viewed and which they added to cart.
- Configure Display campaigns so the creative serves the specific product the shopper interacted with, not a generic brand banner.
- Keep the CTA explicit (e.g. a 'Shop Now' style button) pointing at that product or collection.
- Accept that Display is less popular than it once was but can still work when the creative is genuinely product-specific rather than generic branding.
- Expect Display focus on the mid-funnel: it re-engages people who already know the brand rather than creating new demand.
Caveat: Display reach spans roughly 3 million sites and apps, so placement quality varies; generic banners without product specificity are the setup the source warns against relying on.
Caveat: The source gives no Display performance benchmarks here beyond noting Display CTRs run lower than Search and Shopping.

Tags: google-ads, display-ads, retargeting, remarketing, product-feeds, creative-strategy
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Use Demand Gen to create demand on YouTube Shorts, Discover and Gmail
Use when: Planning top-funnel paid acquisition to reach cold or in-market audiences on Google's non-search surfaces, or looking for a cheaper video placement than Instagram Reels.
- Set up Demand Gen campaigns to serve image and video ads across YouTube (including Shorts), the Discover feed on mobile Chrome below the search box, and the promotions tab in Gmail.
- Target either cold audiences based on interests, life events, or in-market signals, or remarket to people who previously interacted with your store.
- Consider YouTube Shorts specifically for ecommerce — the source observes competition there is less fierce than on Instagram Reels and the cost to serve tends to be lower.
- Treat Demand Gen as demand creation rather than demand capture; it reaches people who are not yet searching for your products.
- Keep it last in the launch sequence — after Search and Shopping are proven — since the source positions it as top-funnel scaling.
Caveat: Placement cost observations are the source's current experience, not a guaranteed or stable benchmark; verify actual CPMs in your account.
Caveat: No conversion-rate or ROAS benchmarks for Demand Gen are given in this material.

Tags: google-ads, demand-gen, youtube-shorts, discover-feed, gmail-ads, creative-strategy, top-of-funnel
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Match YouTube ad format to the job the video needs to do
Use when: Choosing which YouTube video ad format to produce and buy for a store's awareness, consideration or retargeting objective.
- Shorts — vertical, mobile-first content similar to Reels; useful for cheaper reach given lighter competition.
- Bumper ads — roughly 6 seconds long and usually served at the start of a video; use for a single sharp message.
- Skippable in-stream — viewer can skip after 5 seconds; served before, during or after videos.
- Non-skippable in-stream — the viewer must watch the full (typically 30-second) ad; higher friction, so use sparingly.
- In-feed ads — served inside YouTube's feed, including the Discover page or the suggested 'watch next' list on the right-hand side.
- Pick format based on whether you need cheap reach, forced message delivery, or click-driven traffic, then produce creative to the length and aspect ratio that format requires.
Caveat: The source notes YouTube ads are 'really, really effective when done right' but does not provide performance benchmarks by format.
Caveat: Skips, length limits and available formats are platform-controlled and change — verify current specifications in Google Ads.

Tags: google-ads, youtube-ads, video-ads, creative-strategy, acquisition, brand-awareness
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Set the core Google Ads columns and read them in the right order
Use when: Configuring the Google Ads campaign view so you can judge performance daily without digging through reports.
- Include at minimum: impressions (how many times the ad was seen), clicks, CTR (clicks ÷ impressions), cost, conversion value ÷ cost (ROAS), cost per conversion/CPA, total conversions and conversion value, average CPC, and conversion rate.
- Arrange columns in the same logical order every time so you can scan any account the same way.
- Read conversion value ÷ cost as the ROAS figure — dollars returned in purchase value per dollar spent.
- Read conversion rate as the share of clickers who completed your chosen action (usually purchase for ecommerce).
- Set a date filter deliberately — 1 day, 1 week, 30 or 60 days — and remember the numbers shift with the window.
Caveat: The source's sample account shows conversion rates ranging from 14% down to 0.73% across campaigns, illustrating how misleading a single blended rate can be.
Caveat: Google Ads columns are customisable and the interface changes — verify current column names.

Tags: google-ads, measurement, reporting, roas, column-setup, kpi
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Judge CTR only against its campaign type, not one universal benchmark
Use when: Reviewing Search or Shopping ad copy and targeting, or diagnosing whether a campaign's click-through is genuinely weak.
- The source's directional expectations: non-branded Search should aim for at least 7–8% CTR; Shopping around 1%; Display typically lower still; branded Search is naturally very high.
- Do not judge a campaign on CTR in isolation — treat it as a trend metric, especially for Search campaigns, and look at movement over time rather than a single snapshot.
- If non-branded Search CTR sits well below the range, the likely levers are keyword-to-ad relevance, ad copy strength, offer clarity or urgency, and query match.
- For Shopping, remember the click competes with rich product cards (image, price, ratings, delivery) rather than a text ad, which is why 1%-style CTRs are normal.
- Avoid applying the Search target to Shopping or Display — a ~1% shopping CTR is not automatically a failure.
Caveat: The source explicitly says there is no set benchmark and these are general figures, not contractual targets.
Caveat: CTR is one diagnostic among many; a low CTR with strong conversion rate and ROAS may still be fine.

Tags: google-ads, click-through-rate, search-ads, shopping-ads, measurement, benchmarks
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Understand conversion lag with conversions vs conversions-by-conversion-time
Use when: Reading weekly or recent Google Ads performance for any store with a non-impulsive consideration phase, before deciding a campaign is failing.
- Know the two column pairs: conversions / conversion value (credited by ad-interaction date) versus conversions by conversion time / conversion value by conversion time (credited by purchase date).
- Worked example: a shopper clicks a Search ad on 1 July but buys on 4 July for $40 — the 1 July row shows 1 conversion and $40, while the 4 July row shows 0 conversions/$0 for those same columns.
- In that same example, the by-conversion-time row shows 0 on 1 July and 1 conversion with $40 value on 4 July.
- If your sales cycle runs long — say a 14–21 day consideration phase — the discrepancy becomes far more pronounced than in a one-week view where both dates fall inside the window.
- Do not judge recent campaigns on click-dated conversions alone; revisit the same period two to three weeks later when the purchases have populated.
Caveat: Attribution questions (organic/Facebook influence on the later purchase) are deliberately set aside in the source and are not resolved by these columns.
Caveat: During any partial look-back window, recency-biased numbers will always look worse than the settled data.

Tags: google-ads, measurement, conversion-lag, attribution, reporting, sales-cycle
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Read impression share to find out whether budget or ad rank is capping you
Use when: Deciding whether to raise budget or improve ad quality when a Search campaign is not serving as often as it could.
- Read search impression share as the percentage of eligible auctions where your ad actually served (e.g. 88.75% served means 11.25% lost).
- Read search absolute top impression share as the share of time you were the very first ad (position 1 only); search top impression share as positions 1–4, above organic results.
- Use the delta between the two: 88.75% serving, 87.3% in positions 1–4 and 81.57% in position 1 means roughly 6% of impressions were served in positions 2–4.
- Check search lost IS (rank) and search lost IS (budget) — the two must sum to your total missed impression share (e.g. 10% rank + ~1% budget = 11.25%).
- If you are losing on both, fix ad rank first: it is the more efficient route because improving relevance makes the same budget go further, whereas simply raising budget leaves the inefficiency in place.
- Only after maximising quality score should you bid more — raise manual CPC bids directly, or for automated strategies loosen the constraint, e.g. move a 400% tROAS target down to 350% or 300% to let Google bid more aggressively.
Caveat: Loosening a tROAS target increases CPC and ad rank but directly reduces the return target — this affects margin, so treat it as a deliberate trade.
Caveat: Impression-share metrics apply to Search-type campaigns; the source does not present them as universal.

Tags: google-ads, impression-share, ad-rank, bidding, budget-management, search-ads
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Diagnose ad rank through quality score's three components
Use when: Improving an underperforming Search campaign that is losing impression share to rank, rather than simply increasing bids.
- Look at quality score at keyword level and its three components — expected CTR, landing page experience and ad relevance — each rated above average, average or below average.
- Expected CTR: how likely Google thinks your ad is to be clicked relative to competing ads in the auction — influenced by offer, positioning and urgency in the copy.
- Landing page experience: speed, general UX, relevance of the page to both the keyword and the ad, and low bounce / high on-site engagement.
- Ad relevance: how tightly the keyword and ad copy match each other and the user's query.
- Work all three dimensions before touching bids; if they are maxed out, the only remaining lever for ad rank is paying a higher CPC.
- Treat the ad rank formula as having exactly two inputs — relevance (which Google rewards) and bid (which Google also rewards) — and prioritise the rewarded relevance route to protect margins.
Caveat: Quality score is Google's own representation and diagnostic aid, not a perfect measure; the source treats it as guidance for where to look.
Caveat: Component ratings are relative (above/average/below), not absolute numbers.

Tags: google-ads, quality-score, ad-rank, landing-page, ad-copy, search-ads
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Use video metrics: impressions vs views, view rate, CPV and frequency
Use when: Evaluating YouTube or video campaign creative performance and deciding whether the hook or the targeting is at fault.
- Distinguish an impression (the ad was seen) from a view (a higher-engagement threshold that varies by campaign type) — for some formats a view needs 30 seconds of watch time, and for videos shorter than 30 seconds it requires watching to completion.
- Read the standard metrics per format: in-stream view rate of 28% versus in-feed 19% in the source's example means in-stream viewers engaged at a higher rate.
- Use video-played-to-time (25%, 50%, 75%, 100%) to see where in the video viewers drop off — a steep fall before 25% points at the hook, a fall later points at the body or CTA.
- Check total watch time and average watch time per impression (in seconds) for how long people actually stayed.
- Check average CPV, average CPM, average CPC, cost, CTR, conversions, conversion value, ROAS and conversion rate at ad group or ad level.
- Check average impression frequency per user (e.g. 1.5×) over your time window to avoid over-serving the same people.
Caveat: There is no single umbrella definition of a 'view' — it depends entirely on campaign type, so do not compare view rates across formats naively.
Caveat: The source notes video metrics are less critical for people just starting out on Google Ads.

Tags: google-ads, youtube-ads, video-ads, view-rate, creative-strategy, measurement
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Build custom columns for ROAS-by-time, device splits and average daily spend
Use when: Reporting on Google Ads for a store with a long consideration phase, or comparing mobile vs desktop performance at a glance.
- Open Modify Columns and choose '+ Custom Column'; give it a name, description and a formula.
- For ROAS by time, use conversion value by conversion time ÷ cost — the same formula as ordinary ROAS but on the conversion-time value, so recent weeks fill in correctly as purchases land.
- For device splits, add custom columns for mobile conversion rate vs desktop conversion rate, and mobile ROAS vs desktop ROAS, using the corresponding device-segmented metrics.
- For convenience, add an average spend-per-day column so a 7-day total doesn't require mental division and you can read spend trend at a glance.
- Apply these especially when you are deliberately targeting one device more aggressively than another, so the skew is visible on entry to the account.
- Treat custom columns as decision-support: the goal is to have the KPIs you care about visible the moment you log in, rather than buried in reports.
Caveat: The source flags custom columns as probably a step too far for complete beginners — start with the standard column set first.
Caveat: Formula syntax and available metrics shift with the Google Ads interface; verify the current metric names.

Tags: google-ads, custom-columns, reporting, roas, device-targeting, measurement
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Link GA4 to Google Ads via Admin → Product links, then demote the imported purchase action
Use when: Setting up GA4-to-Google-Ads reporting and audience imports for a Shopify store, or auditing an account whose ROAS suddenly doubled after linking analytics.
- In GA4, go to Admin → Property settings → Product links → Google Ads links.
- Enter your Google Ads account ID (the purely numeric ID in the Google Ads top toolbar) into the search field and click Link.
- On the Link screen, decide on settings such as personalised advertising and auto-tagging, confirm the ad account number and name, and click Submit.
- After linking, go to Conversion actions in Google Ads and check what has been imported — typically a GA4 purchase action appears.
- If you already have a purchase conversion action (from Google Tag Manager, a third-party tool, or the Google and YouTube app connecting Shopify to Google Ads), the imported GA4 purchase action will by default be primary and will affect bidding and reporting alongside the existing one.
- The consequence of running two primary purchase actions is double counting: ROAS and purchases can appear to double almost overnight. Change the GA4-imported purchase action to secondary so it still fires for observation and as a fallback if the primary breaks, but does not double count.
- Never use the GA4-imported action as your primary — the source's agency always uses an alternative method as primary.
Caveat: This is a Shopify/ecommerce-oriented setup; the linking path and option names may change in the GA4 and Google Ads interfaces.
Caveat: The double-count spike can look like a performance win — treat a sudden ROAS doubling after a GA4 link as a red flag, not a victory.

Tags: google-ads, ga4, conversion-tracking, shopify, measurement, attribution
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Use four GA4 reports to sanity-check paid traffic quality
Use when: Reviewing store traffic quality every couple of weeks, especially to see how paid landing pages and channels are performing beyond Google Ads' own numbers.
- User attributes: break users down by country, city, gender, age, language and Google-tagged interests to sanity-check who the typical customer is.
- Monetization → e-commerce purchases: see how often each product was viewed, added to cart and purchased, plus the revenue per product — all in one place.
- Landing pages report: review sessions, active users, new users and average engagement time per session, then dig into bounce rates — this is where the source says GA4 is genuinely powerful for spotting weak paid-traffic landing pages.
- Channels report: view first-user and primary channel groupings (direct, organic search, cross-network, paid search, organic shopping, etc.) and drill into source and medium.
- Make sure UTM parameters are flowing through from all paid media so channel and source/medium attribution is actually usable.
- Understand that most of this is also available in your CMS (e.g. Shopify) — use GA4 for the consolidated view rather than as the only source.
Caveat: The source notes many ecommerce brand owners dislike GA4 and use alternate platforms — using it is optional, not mandatory.
Caveat: GA4 is free and useful but requires familiarisation with its navigation; the four reports here are a starting shortlist, not the full surface.

Tags: ga4, google-ads, reporting, landing-page, utm-tracking, measurement
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Build a 30-day cart-abandoner audience in GA4 and import it to Google Ads
Use when: Setting up cart-abandonment retargeting for a store, or creating a high-intent audience for Google Ads remarketing campaigns.
- In GA4 go to Admin → Data display → Audiences and create a new audience.
- Set the include condition to 'add to cart' (a pre-built GA4 event) with a 30-day membership duration.
- Add an exclusion condition: exclude users who have purchased — otherwise you will re-target people who already converted and waste spend.
- The source's example: 4.2K add-to-cart users over 30 days (15% of total users); excluding 603 purchasers left ~3.6K genuine cart abandoners — a sizeable audience.
- Mark the audience as a key audience so it can be imported into Google Ads.
- In Google Ads remarketing, use the specificity this audience allows — e.g. 'saw you weren't ready to make a purchase, here's a discount code or free shipping' — rather than generic site-visitor messaging.
- Optionally create a separate post-purchase audience to serve upsell messaging in the immediate post-purchase window, rather than mixing them into the cart-abandoner set.
Caveat: Audience sizes like 4.2K/3.6K are from the source's account and will differ entirely for your store.
Caveat: The audience quality depends on add-to-cart events being correctly tracked in GA4; bad event data makes the exclusion logic meaningless.

Tags: ga4, google-ads, retargeting, cart-abandonment, audience-building, retention
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Fix conversion tracking before anything else — it feeds you and the algorithm
Use when: Starting Google Ads for a store, or auditing an account that is running automated bid strategies on unreliable conversion data.
- Accept the source's framing: conversion tracking tells you whether a click led to a purchase, and it gives Google's automated bid strategies the positive and negative feedback they learn from — without it you may as well be lighting ad spend on fire.
- For a Shopify store, install the Google and YouTube app in Sales channels and connect it using a single master Google account linked to all your Google properties (Ads, Merchant Center, Analytics).
- Select your Google Ads account in the app's dropdown — this automatically imports Shopify's API conversion actions, turns conversion measurement on, and is the 80–90%-of-the-way-there quick route.
- Check that enhanced conversions are enabled and the Google tag is firing.
- If you are serious about Google Ads, go further and implement fully in Google Tag Manager, because more conversion data fed to the algorithm means better performance — the source's agency uses a dedicated pixel (Feed Army) for enhanced tracking and remarketing.
- Audit regularly for the common tracking failures the source calls cardinal sins — missing or duplicated conversion actions are the ones that quietly wreck automated bidding.
Caveat: The simple Shopify app route is presented as reaching 80–90% of a full implementation, not as a complete solution.
Caveat: Tool names, app flow and toggle labels (enhanced conversions, Google tag) change over time — verify the current setup in the relevant interfaces.

Tags: google-ads, conversion-tracking, shopify, google-tag-manager, measurement, automated-bidding
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Consolidate everything under one master Google account
Use when: Setting up or cleaning up a store's Google ecosystem before connecting Shopify, Merchant Center feeds or GA4.
- Create or choose one master Google account that owns or manages your Google Ads account.
- Sign in to the Google and YouTube app (or equivalent connection tool) with that master account so the Google Ads account appears in the dropdown by name or number.
- Link the same master account to Google Merchant Center (the product feed that powers Shopping and PMax) and to GA4.
- Select the correct Google Ads account in each connection so conversion actions import to the right place.
- Avoid splitting ownership across multiple Google logins — it is the root of connection failures and duplicated conversion actions.
Caveat: The source presents this as ideal setup hygiene rather than a strictly enforced requirement; the important outcome is that Ads, Merchant Center and Analytics all talk to each other.
Caveat: Google account and linking interfaces change — verify current steps.

Tags: google-ads, merchant-center, ga4, account-setup, shopify, conversion-tracking
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Adopt Google Ads as the stability layer under Meta-led acquisition
Use when: Deciding whether and why to diversify a Meta-dependent store into Google, and how to frame the channel's role internally.
- Diagnose Meta dependency risk: when Meta works it works, but CPM spikes, conversion drops, ad-account bans and revenue stalls all concentrate your growth in one place.
- Position Google Ads as the stability layer underneath Meta — high-intent Search and Shopping capture demand, full-funnel activity runs from education through to conversion.
- Prioritise fixing leaky campaign structures and wasted spend over adding more channels.
- Build reliable flows of new-customer acquisition through high-intent Search rather than chasing top-funnel volume first.
- Sequence channel expansion deliberately: Search and Shopping as the backbone, then remarketing/PMax, then Demand Gen last.
Caveat: This is the source's strategic opinion, framed from an agency that has worked with 80+ DTC brands and $50M+ in new-customer revenue — it is a thesis, not a benchmarked guarantee.
Caveat: Google Ads being 'more reliable' than Meta is a claim about volatility, not about absolute performance ceilings.

Tags: google-ads, channel-expansion, acquisition, risk-management, search-ads, shopping-ads
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Threshold the switch from Maximize Clicks to value-based bidding
Use when: Choosing a bid strategy for a new or low-volume Google Ads campaign, and deciding when to graduate to automated value bidding.
- Start new campaigns on Maximize Clicks while gathering initial data — the goal at this stage is volume of signal, not efficiency.
- Once the campaign reaches roughly 15–30 conversions per month, switch to Maximize Conversion Value or Target ROAS so the algorithm optimises toward value rather than clicks.
- Before switching, make sure conversion tracking is accurate — value bidding on broken or duplicated conversion data will optimise in the wrong direction.
- After switching, monitor impression share lost to rank and budget, and adjust the tROAS target (e.g. loosening 400% to 350% or 300%) if you need Google to bid more aggressively.
- Treat the 15–30 figure as the source's starting threshold for having enough conversions for value-based learning, not a hard calculation.
Caveat: Below the threshold, value-based bidding typically lacks enough signal to be effective — the source's band is a heuristic.
Caveat: Changing bid strategy resets learning, so make the transition deliberately rather than flipping back and forth.

Tags: google-ads, bidding, target-roas, maximize-conversions, budget-management, measurement
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Connect Shopify to Google Ads via the Google & YouTube App
Use when: Initial Google Ads setup or account audit for a Shopify store that has no working conversion tracking.
- Set up a single master Google account that owns your Google Ads, Merchant Center, and Analytics accounts, and use it to sign in to the Google & YouTube app in Shopify under Sales Channels; a fragmented account structure makes linking far harder.
- Open the app settings and select your existing Google Ads account from the drop-down (it may appear as a name or an ID number).
- Accept that this connection automatically imports Shopify's API conversion actions — including purchase, add to cart, begin checkout, page view, item view, and on-site search — along with conversion value and conversion count.
- If you already have conversions set up manually via Google Tag Manager or imported from GA4, audit your actions immediately: the only change the Shopify connection should make is adding actions as secondary, not creating a second primary purchase action.
- Turn on enhanced conversions and confirm your Google tag is firing.
- Expect a delay: allow a couple of hours for the first purchase to fire, and up to a day or two for actions to populate. If no existing Google Ads conversions exist, you will not see anything fire until real purchases occur.
- Identify the imported purchase action by its label, which appears as the Google shopping app purchase.
Caveat: Recommendation for beginners is to connect everything via the Shopify app; more seasoned advertisers wanting more robust tracking are advised to use FeedArmy's pixel instead.
Caveat: The app interface and menu labels may change over time — verify the current layout in Shopify before following exact click paths.

Tags: google-ads, shopify, conversion-tracking, measurement, merchant-center, setup
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Set Exactly One Primary Purchase Action
Use when: Auditing or setting up conversion tracking, or when your reported ROAS and revenue look implausibly strong.
- Recognize that primary conversion actions are used for bidding optimization and shown in reports, while secondary actions are observation-only and do not influence bidding.
- For an ecommerce store, set purchases as the sole primary action; set everything else (add to cart, begin checkout, page views, view item, search) to secondary.
- To change a setting, click into the conversion action, then open Settings, and locate action optimization; set it to primary or secondary as appropriate.
- Check for the first cardinal mistake: two purchase actions both marked primary. This typically happens when a Shopify-imported purchase, a Google Tag Manager purchase, and a GA4-imported purchase all exist — normally one is primary and the rest secondary, but if two are primary, revenue and ROAS are counted twice and look roughly double the truth. If an agency runs this while two primaries are live, the source advises firing them immediately.
- Check the second mistake: GA4 set as your primary purchase action. GA4 under-reports Google Ads conversions by around 20% versus Google Tag Manager or the Shopify action, giving the algorithm less data to optimize on. Prefer the Shopify action or a direct Google Tag Manager setup.
- Check the third mistake: non-purchase actions such as add to cart or begin checkout set as primary, or set as account default goals across campaigns. Set them to secondary.
Caveat: The source's ~20% GA4 under-report figure is their working estimate, not a guaranteed benchmark.
Caveat: Micro-conversion bidding is an exception the source attributes to very select high-ticket cases: a $10–15k product with only 8–20 conversions a month may not generate enough volume for smart bidding, so bidding could target add to cart with heavy remarketing. The source considers this appropriate for roughly 1% of advertisers, not the default.

Tags: google-ads, conversion-tracking, measurement, bidding, account-audit, ga4
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Use Cart Abandoners as a Remarketing Audience
Use when: Setting up remarketing for potential buyers who added to cart but did not purchase, especially for retention and checkout-stage recovery.
- In GA4, go to Admin, then Audiences, and create a new audience named for cart abandoners.
- Include users when they complete the add-to-cart action.
- Exclude users when a purchase has been made — without this you will serve ads to people who already bought.
- Set the membership window based on traffic volume: the source's example brand used 60 days because a 30-day window would not yield enough reach. Confirm Google Ads and GA4 are connected, then import the audience into Google Ads.
- Check current list eligibility for the intended campaign type in the account before launch. The source 1,000-1,500 figure is not a universal remarketing minimum.
- Target the imported list in remarketing campaigns focused on completing the purchase.
Caveat: A 60-day window is broad; the source used it solely because of low site traffic, so set windows from your own list-size data, not as a rule.
Caveat: Cart-abandoner audiences require GA4-to-Google Ads connectivity to import.

Tags: google-ads, remarketing, retention, cart-abandonment, ga4, audience-targeting
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Create Website Visitor Remarketing Lists by Page Depth
Use when: Creating remarketing audiences for abandoned-browse recovery, dynamic remarketing, or any retargeting by page intent.
- In Google Ads, go to Tools, then Audience Manager, then Data Segments, and click the plus button. Choose website visitors.
- Name the segment clearly, e.g. '30-day website visitors, all pages'.
- Set segment members by default to 'visited a web page in the past 30 days'.
- Optional: refine by URL. Use 'URL contains' for a specific product or collection to build page-level intent lists.
- Choose depth by traffic: the source suggests six- and seven-figure stores may not have enough traffic to filter by individual products, so keep it open to all visitors; eight- and nine-figure brands generally have enough traffic to build specific product and PDP lists that support more relevant dynamic remarketing.
- On duration, the source normally lowers lists to 3-day to 7-day visitors, treating longer windows as broad and less recommended — but again, this depends on traffic level.
- Wait up to a day for the list to populate, then check list size and eligibility for Search, Display, and YouTube under the data source.
Caveat: The 6/7-figure versus 8/9-figure traffic bands are the source's rule-of-thumb, not a calculated threshold.
Caveat: The 3–7 day preference is an opinion, contingent on volume; low-traffic stores may need broader windows to reach remarketing eligibility.

Tags: google-ads, remarketing, audience-targeting, product-page, merchandising, setup
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Build YouTube Interactor Lists to Sequence Education into Direct Response
Use when: Designing acquisition creative strategy that sequences YouTube awareness content into purchase-driven retargeting.
- In Google Ads Audience Manager, click the plus for a new data segment and choose YouTube users.
- Name the segment, set customer type, and select your brand's YouTube channel.
- Pick an interaction level from the available options: viewed any video on the channel, viewed certain videos, viewed certain video ads, subscribed, visited the channel page, or liked any video.
- The source's preferred approach is to select 'viewed certain videos as ads' for top-of-funnel educational content, then remarket those viewers with more direct-response creatives.
- This builds a funnel: paid top-of-funnel YouTube education creates the audience, and later direct-response ads convert that warmed audience.
Caveat: Applies when you actually run YouTube content or video ads; with no channel activity there is no audience.
Caveat: The option set in Audience Manager should be verified, as Google updates the interface.

Tags: google-ads, youtube, remarketing, acquisition, creative-strategy, funnel-sequencing
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Upload Customer Lists for Signals, Lookalikes and Exclusion
Use when: Acquisition expansion, lookalike targeting, or excluding existing customers from non-branded and general campaigns.
- In Audience Manager, Data Segments, click plus and choose customer list.
- Name the segment with the definition and upload date, e.g. all customers up to a certain date plus the date it was uploaded, if you upload manually.
- Choose customer type: all customers, or a segment of most valuable customers — the source suggests customers with three or more purchases, or the top 5% of revenue spent in your store.
- Upload a CSV including email, phone, first name, last name, zip, and country wherever available.
- Allow roughly a day for the list to fully populate.
- Use it in three ways: as an audience signal telling Google what your customers look like demographically and behaviorally so it can find similar cohorts; as the base for lookalike audiences inside Demand Gen; and as an exclusion list applied to non-branded campaigns and often to all campaigns.
- The source does not typically use uploaded customer lists to remarket directly to the customers themselves — the primary value is signal, lookalike and exclusion.
Caveat: Three-plus purchases and top 5% of revenue are the source's example definitions of valuable customers, adaptable to your data.
Caveat: Exclusions depend on matching emails, phones or addresses, so list completeness affects coverage.

Tags: google-ads, customer-list, audience-targeting, lookalike, acquisition, retention
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Build Custom Segments from Search Terms to Find New Demand Pockets
Use when: Opening new prospecting pockets, tuning acquisition targeting, or reaching problem-aware shoppers before they search your category terms.
- In Audience Manager, go to custom segments (not data segments) and create a new one; you can name it at the end.
- Choose what to include: people with specific interests or purchase intentions, people who searched any of your listed terms on Google, and/or people who browse websites similar to listed sites.
- For search-term segments, enter queries that describe the customer's problem and solution language. The source's collagen example lists 'why is my hair thinning', 'perimenopausal joint problems', 'best collagens', 'should I take liquid collagen or powder collagen' — treating the first as problem-aware and the last as solution-aware. The source cautions against spanning that broad a range in one segment, but it illustrates the query types available.
- For website segments, use 'similar to our own website' or 'similar to competitor websites' to concentrate Google's attention on an audience pocket matching your customer's browsing behavior.
- What works best for the source in 2025 is a custom segment using only searched terms, with no websites and no apps included.
- Rename and save; combine custom segments with campaign targeting to scale into markets your remarketing lists cannot reach.
Caveat: The example terms are illustrative, not validated performers — derive terms from your own customer language.
Caveat: The 'searched terms only' preference is the source's current working finding, not a universal rule.

Tags: google-ads, custom-segments, audience-targeting, acquisition, keyword-research, competitor-research
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Set Up Google Merchant Center and Sync Products for Shopping Ads
Use when: Before launching Shopping campaigns, or when your Shopify products are not feeding into Google Ads.
- Install the Google & YouTube app from Shopify's sales channel list and sign in with the same master Google account that owns your Google Ads and Analytics accounts.
- In app settings, connect your Google Ads account first, then connect Merchant Center: select an existing Merchant Center account from the drop-down, or follow the prompted setup.
- If creating a new account, provide business information, claim and verify your website, supply shipping and returns details, tax info, and add your products.
- For product upload, the source recommends the Shopify-to-Merchant-Center sync for the majority of ecommerce brand owners spending roughly 10–30k a month who are relatively new to Google Ads; manual Google Sheets or file uploads and third-party tools such as Simprosys or Feedonomics are alternatives. Feedonomics is described as good but optional.
- Once syncing, monitor the product statuses — approved, pending, not approved — expecting most products to sit pending until approved, and use diagnostics to investigate disapprovals.
- Link Merchant Center to Google Ads: in Merchant Center settings, go to Apps and services (under the settings cog), choose Add a service, select Google Ads, pick your ad account, and confirm. Having everything under one Google account makes this far simpler.
- After linking, products feed through and you can build Shopping campaigns using the product card format — image, title, price, and store and delivery information.
Caveat: The source calls Shopping ads the highest-performing campaign type for ecommerce and says skipping Merchant Center means leaving money on the table; other campaign types may fit differently depending on your store, and free listings and local inventory ads are additional benefits, the latter being relevant for brick-and-mortar stores.
Caveat: Setup time is quoted as around 20 minutes, but approval and feed processing add delay.
Caveat: Skipping Merchant Center also forfeits free listings; product approval status must be monitored for disapprovals.

Tags: google-ads, merchant-center, shopping-ads, product-feed, shopify, setup
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Map Product Feed Attributes to Search Intent in Shopping Campaigns
Use when: Feed optimization for Shopping campaigns, especially when products serve on irrelevant queries or conversions lag.
- Understand the mechanism: Shopping ads trigger on how closely your product data matches user search intent, not keywords. A search such as 'men's running shoes, size 10' serves listings whose data reflects men's, running shoe, and size 10.
- Prioritize five attributes that move the needle: price, product title, product images, product description, and GTINs. Titles, price and images are visible in listings; description and GTINs are not but help Google match the most relevant products.
- Treat price as the most important attribute because Google Shopping is fundamentally a comparison surface where shoppers compare price first. Accurate, fair and competitive pricing wins click share; a visible sale reduction (e.g. $30 to $15) is likely to capture more click share from deal-seeking shoppers.
- Work around price if you cannot compete on it: lead with a single-unit pack that shows the lowest headline price then upsell on the landing page, or promote a high-volume pack using unit pricing, or justify a premium price through quality and luxury positioning. Remember you only pay for clicks that actually occur, so a filtered-out shopper costs nothing.
- Install the remaining attributes by rewriting titles (see the dedicated title card), using sharp high-resolution images, writing useful descriptions, and populating accurate GTINs.
Caveat: The source notes price is often difficult for a brand owner to change, since they have usually already chosen an offer — treat the workarounds as mitigations, not fixes.
Caveat: The 'lowest price tends to win' observation is the source's characterization of Shopping as a comparison site, not a guaranteed outcome.

Tags: google-ads, product-feed, shopping-ads, pricing, product-page, merchandising
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Rewrite Product Titles for the First 70 Characters
Use when: Feed title optimization for any Shopping campaign, especially for cold-traffic acquisition where brand recognition is low.
- Work within the 150-character maximum but optimize for the first 70 characters, which are what shoppers actually see before Google truncates the title with an ellipsis.
- Decide brand placement by asking whether you are a market leader. If you are, leading with the brand (the Nike example) earns recognition and clicks. If you are not a market leader or have low brand awareness, lead with brand is wasted space for cold traffic; leave the brand at the end, or omit it if no space remains.
- Use this general structure: core product type first, then key features or benefits, then specifics such as quantity, size, material or use case, and finally the brand if space allows.
- Apparel example: replace a repetitive 'Zavari denim jacket for men, blue, Zavari clothing' with 'men's classic denim jacket, stretch fit, sharp, aligned blue, Zavari' — product type leads, features follow, specifics then brand.
- Consumer electronics example: replace 'Technova wireless earbuds, Technova Bluetooth headphones' with 'wireless earbuds with charging case, noise cancelling, Bluetooth 5.3, Technova' — front-load the details that matter to information-hungry shoppers in a longer consideration cycle.
- Do not let organic titles flow straight into the feed unchanged, since they often lead with the brand.
- Adapt the structure to your niche; the source notes it varies and that brand stuffing at the front is a common beauty and skincare problem.
Caveat: The 70-character visible limit and 150-character cap are Google's feed constraints as described by the source; verify current limits before bulk rewriting.
Caveat: The structure is a source heuristic — test titles against your own query data and conversion rates.

Tags: google-ads, product-feed, shopping-ads, product-page, conversion-optimization, copywriting
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Enable Product Ratings to Lift Shopping CTR
Use when: Shopping ads appear alongside competitors and you want higher click-through rate without extra spend.
- Submit the product ratings interest form to signal to Google you want product ratings in Merchant Center, and answer the qualification questions, including whether you work with a third-party review aggregator (common Shopify brands use Trustpilot or Judge.me).
- Choose an implementation route: Google's own customer reviews program, where Google collects the reviews; an official aggregator integration (the source says there are around 33 official aggregator platforms, including Trustpilot and Stamped); or a non-official aggregator.
- For Judge.me — used by roughly 70–80% of the brands the source partners with, low-cost and user-friendly — note there is no direct Merchant Center integration, so product ratings are uploaded manually via Shopify. Follow Judge.me's own guide: set up Judge.me, connect it to Shopify, ensure Shopify is connected to Merchant Center, and sync the ratings.
- Meet the eligibility thresholds: a total of at least 50 reviews to be eligible for the program, and at least three reviews on any single product to serve ratings for that product.
- Allow two to four weeks from submitting the interest form before product ratings actually serve on ads.
- Once live, ratings appear as a star score plus review count on your Shopping listings, drawing attention, raising CTR and building trust before the click.
Caveat: The source describes only positive effects on CTR, clicks and sales in their experience, and says it costs nothing — but results are their observation, not a guaranteed uplift.
Caveat: Trustpilot and Stamped are named official integrators; Judge.me is non-official and requires manual upload, which adds maintenance work.
Caveat: Threshold counts and aggregator integration status should be verified with Google, as programs change.

Tags: google-ads, merchant-center, shopping-ads, social-proof, conversion-optimization, reviews
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Chase the Top Quality Store Badge by Fixing Five Experience Categories
Use when: Merchant Center store-level optimization to raise Shopping ad ranking and CTR without increasing ad spend.
- Understand what the badge signals: Google indicates you rank highly across user-experience categories (browsing, purchase, shipping, returns, store rating), benchmarked against other stores in your country, and says badged stores rank higher in Shopping results. The badge can display on listings and on your website.
- Browsing experience: use only high-resolution images, never blurry ones; show many images per listing — the source recommends a high-quality primary image plus 8 to 10 additional images showing angles, lifestyle and product uses; and keep landing page load speed under 2 seconds on both desktop and mobile.
- Purchase experience: keep Merchant Center promotions consistent with site promotions in detail, dates and coupon codes, since mismatched promotions are disliked by Google and can be rejected; and offer multiple payment options such as Apple Pay, Google Wallet, PayPal and Amazon Pay, as more options are read as a better purchase experience.
- Shipping experience: keep delivery time to a minimum and shipping cost as low as possible, recognizing you are often constrained by regulations and carrier costs.
- Returns experience: give a fair and broad return window — at least 30 days, if not more — and reduce the customer's return cost.
- Store rating: collect post-purchase reviews at product and store level. Store ratings differ from product ratings and can serve in text/search ads as well as Shopping ads, helping CTR and trust. The source adds that collecting post-purchase reviews is good practice regardless of the badge.
Caveat: The ~20% performance lift is the source's claim from their own client experience, not a Google-published benchmark, and it takes time along with product ratings.
Caveat: Shipping and returns constraints may limit how far a brand can move these categories in practice.
Caveat: Benchmarks are relative to other stores in your country, so the bar shifts.

Tags: google-ads, merchant-center, shopping-ads, conversion-optimization, product-page, trust-signals
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Write Shopping Product Titles: Core Type → Features/Benefits → Specifics → Brand
Use when: Optimizing the product feed titles that power Shopping/PMax product listings, especially when your brand is not a market leader.
- Open with the core product type in plain search language (e.g. 'wireless earbuds', 'vitamin D3 supplement') so Google can index it against relevant queries.
- Frontload key features and benefits the buyer needs to evaluate: 'noise cancelling, Bluetooth 5.3', 'brightening serum with hyaluronic acid and aloe vera'. For higher-consideration categories like consumer electronics and skincare, buyers want more information and often know what actives or specs they need.
- Add specifics that the image alone cannot convey: quantity, size, dosage, serving count, use case (e.g. '5,000 IU', 'charging case', 'ergonomic neck support').
- Place the brand name at the end rather than the start — unless you are a market leader, where brand-first has merit per the source.
- Avoid repeating the brand name multiple times across title variants; that space is better spent on differentiating information.
- Check whether the title answers the questions a first-time buyer would have; if not, replace repeated brand mentions with missing attributes.
Caveat: The brand-first exception applies to established market leaders; most stores are competing for share and benefit from information-first titles.
Caveat: The source presents this as a framework, not a guarantee — even its best examples were described as improvable.

Tags: google-ads, product-titles, feed-optimization, shopping-ads, product-page, merchandising
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Recognize Bad Title Patterns: Brand-First Repetition
Use when: Auditing an existing product feed before a Shopping campaign launch or when CTR is low on well-funded listings.
- Pull titles that start with the brand and repeat it (e.g. 'Globy vitamin C serum, Globy skincare') and mark them for rewrite.
- Ask 'why buy this rather than any of the thousands of alternatives?' — if the title doesn't answer it, it isn't doing commercial work.
- Check category by category: supplements often omit dosage, tablet count and benefits; electronics omit what's in the box; bedding omits cooling/gel or ergonomic claims; beauty omits active ingredients.
- Quantify the gap by comparing a rewritten title's CTR against the original in the same ad group, holding image and price constant.
- Roll out the winning structure across the catalogue rather than fixing one SKU at a time.
Caveat: The source repeats patterns observed across niches; it does not provide benchmark CTR figures for any rewrite.

Tags: google-ads, product-titles, feed-optimization, shopping-ads, audit, ctr
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Product Image Standards: Resolution, Focus, No Overlays
Use when: Preparing or refreshing Merchant Center imagery for apparel, home goods or any feed flagged for disapprovals.
- Upload high-resolution images — blurry or low-quality shots will not perform and can hurt listing quality.
- Keep the product as the main subject; if you use lifestyle imagery, the item being sold must remain front and centre.
- Remove all text overlays (sale stickers, 'Black Friday', price badges) — the source states these trigger policy violations and prevent the item serving as a Shopping ad.
- For apparel, put the garment on a model and iron it before shooting; the source contrasts a crisp, modelled tee with a crinkled one on a white background where the garment disappears.
- For multi-item sets (e.g. utensil kits) a plain white background is acceptable because the volume of items is the selling point; for premium single items, invest in an elevated, minimal but luxe presentation.
- Watch composition on home goods: in a rug shot, check that props like an ottoman are not competing with the product as the visual focus.
Caveat: Source opinion: text overlays 'always get pinged' unless you are very lucky — treat as strong guidance, not a documented policy statement; verify current Merchant Center image policy in Google's help centre.
Caveat: No specific pixel or file-size threshold is given in the source.

Tags: google-ads, product-images, feed-optimization, merchant-center, creative-strategy, apparel, policy-compliance
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Test Lifestyle and AI Backgrounds Against Plain Product Shots
Use when: Improving Shopping listing creative when click-through rate is the bottleneck and price/title are already competitive.
- Set up a test alternating a plain white-background image with a lifestyle or elevated-background version of the same product, keeping title and price constant.
- Include an AI-generated or stylised background as a valid 'lifestyle' variant — a sleeker scene behind the product counts, it doesn't have to show the product in use.
- Use in-use shots where visualisation matters most (apparel on models; furniture in a room), but keep the sold product clearly identifiable.
- For premium products, prioritise the elevated look: the source argues a lower-priced competitor with a better image can appear to have higher perceived value, and shoppers comparing on price will click the better-looking listing.
- Use Google's Product Studio inside Merchant Center to generate elevated backgrounds from plain shots; you can describe the scene you want. It is free, and improving over time — confirm the current interface in Merchant Center.
- Scale winners across the catalogue rather than running one-off image swaps.
Caveat: The source's 'about 90% of the time lifestyle wins on CTR' is the presenter's observed experience, not a published benchmark; results will vary by category.
Caveat: Apparel has edge cases: a modelled shot usually wins, but testing non-model imagery is still worthwhile.

Tags: google-ads, product-images, creative-testing, shopping-ads, product-studio, ctr, experiment-design
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Write Product Descriptions That Answer Buyer Objections
Use when: Building or cleaning the description attribute in your Merchant Center feed before scaling Shopping spend.
- Take the copy from your PDP only if you first make it readable and scannable — reformat walls of text into short blocks covering key features and benefits.
- Work in relevant keywords naturally so Google can match products to queries; descriptions remain a useful matching signal even if less weighted than in the past.
- Never keyword-stuff: descriptions must flow naturally and add value. Don't add text purely to fill the field.
- List the questions a prospective buyer asks before purchase — the source argues brand owners already know these from their website objection handling — and answer them here.
- Check the copy answers specification gaps the title couldn't fit: dosage, materials, dimensions, what's in the box.
- Refresh descriptions when search term reports show irrelevant queries being triggered, since description content shapes how Google indexes the product.
Caveat: The 5,000-character limit and the weighting of descriptions are described from the presenter's knowledge and may change; verify current Merchant Center field limits.
Caveat: The source's own best examples were described as improvable, so treat the format as a floor not a ceiling.

Tags: google-ads, product-descriptions, feed-optimization, merchant-center, product-page, seo
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Focus Feed Optimization on Price, Title and Image
Use when: Deciding where to spend merchandising effort when Shopping performance is weak and you cannot manipulate query targeting.
- Accept the constraint: with Shopping ads you don't pick search queries the way you do in Search campaigns; Google matches your feed to queries.
- Concentrate effort on the three attributes the source says drive roughly 95% of Shopping performance: price, product title and product image.
- Set price competitively relative to the listings you appear beside, since price is visible in the Shopping unit and feeds directly into perceived value.
- Rewrite titles using the core type → features/benefits → specifics → brand structure.
- Upgrade images per the resolution, focus and lifestyle-test guidance.
- Treat remaining feed attributes (descriptions, GTINs, custom labels) as secondary but keep them accurate; ensure every variant has its own unique GTIN and correct identifier codes, which sync reliably when Shopify is connected to Merchant Center.
Caveat: The '95%' figure is the presenter's heuristic emphasis, not a measured attribution model.
Caveat: Verify current Merchant Center attribute requirements and sync behaviour before relying on automatic Shopify population.

Tags: google-ads, feed-optimization, shopping-ads, pricing, product-titles, product-images, merchant-center
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Set Up a Standard Shopping Campaign (Not PMax)
Use when: Launching a DTC store's first Shopping campaign in Google Ads.
- Confirm prerequisites first: conversion tracking installed, Merchant Center account created and linked to Google Ads.
- In ads.google.com go to Campaigns → the blue plus → objective Sales; set the conversion goal to purchases.
- When Google pushes Performance Max, decline and choose Standard Shopping instead (the source's recommendation for this setup).
- Select the linked Merchant Center account from the product drop-down and name the campaign to encode scope: channel, product count, and jurisdiction (e.g. 'Shopping | All Products | UK').
- Set an average daily budget; choose a bid strategy guided by account maturity — manual CPC or Maximise Clicks for new accounts, Target ROAS once conversion data exists.
- In campaign settings, set the location, then open Location options and switch from 'Presence or interest' to 'Presence' so you only pay for people actually in your target market.
- Turn off Search Partners — the source reports consistently weak performance there for these campaigns.
- In ad group settings name the group, set a max CPC if on manual bidding, and choose products by all products, product type/category, item ID, or custom labels (e.g. seasonality, bestsellers) before saving.
- Publish; ads typically start serving within a couple of hours.
Caveat: Bid strategy choice depends on account history — the source points to a separate bid strategy lesson rather than one universal rule.
Caveat: Custom labels for seasonality/bestsellers must first be built in Merchant Center.
Caveat: Ad interface element names and PMax defaults change frequently; verify the current UI.

Tags: google-ads, shopping-ads, campaign-setup, location-targeting, budgeting, bid-strategy, merchant-center
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Segment Branded and Non-Branded Shopping Campaigns with Priority Rules
Use when: Structuring Shopping campaigns so branded and non-branded performance can be measured separately and competitors can't intercept your brand traffic.
- Build the non-branded campaign: select all products, set campaign priority HIGH so all queries route here first, use a moderate Target ROAS, and add a branded negative keyword list so brand queries can't trigger these ads.
- Build the branded campaign: same products, priority LOW, with a higher Target ROAS because branded traffic converts better and at lower CPCs.
- Keep the two campaigns congruent: identical products, audiences and geos. Any difference breaks the hierarchy — a product missing from the non-branded campaign (or a geo mismatch) will let a non-branded query fall into the branded campaign.
- Reason through routing: query 'Nike shoes' routes first to high-priority non-branded, is blocked by the Nike negative, then serves in branded. Query 'running shoes' serves in non-branded as intended.
- Avoid the two failure modes: running out of budget in the non-branded campaign (overflow queries drop into branded) and excluding products from one campaign only.
- Use this split to see true non-branded ROAS and to stop resellers/competitors appearing above your own listing on your brand terms.
Caveat: Described by the source as an advanced technique; priority rules and shared negatives must be set up correctly the first time or results become misleading.
Caveat: The moderate/high ROAS values depend on your own KPIs — the source gives 200–300% as an illustrative non-branded range, not a benchmark.

Tags: google-ads, shopping-ads, branded-campaigns, campaign-structure, negative-keywords, roas, measurement
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Use Shopping Competitive Metrics to Diagnose Why Ads Didn't Serve
Use when: Weekly Shopping optimization reviews where a campaign hits its ROAS or CPA target but you suspect missed volume.
- Start with performance metrics: CTR, CPC, conversion rate and ROAS/CPA against your KPI.
- Then read search impression share — the share of eligible queries where your ad actually served. If it is 15%, you served 15 of every 100 relevant opportunities.
- Split the missing 85% into the two loss metrics: search lost to budget (you ran out of daily budget) and search lost to rank (your ad rank/bids weren't competitive enough).
- If budget loss dominates and you are hitting KPI: increase budget, don't touch bids — you shouldn't be capped when performance is on target.
- If rank loss dominates: decide whether you can afford slightly lower efficiency in exchange for scale. If yes, raise CPCs (manual bidding) or lower Target ROAS (automated bidding) to let the algorithm bid more aggressively.
- Check click share alongside impression share: high impression share with low click share means your products index well and serve for many terms but the titles/images aren't clickworthy — that is a creative/feed problem, not a bidding problem.
Caveat: For Shopping, ad rank largely reflects bid aggressiveness plus product quality, so 'rank' losses aren't purely a CPC question.
Caveat: Any CPC increase at stable conversion metrics reduces efficiency; the trade-off is a business decision, not a default.

Tags: google-ads, shopping-ads, measurement, impression-share, bid-strategy, budgeting, optimization
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Mine Search Terms and Split Negative Keyword Levels
Use when: Weekly optimization of Shopping campaigns, especially in the first weeks after launch or after adding new SKUs.
- Review search terms very frequently on a new account — the source suggests as often as daily — because new products surface for unknown queries and you don't select Shopping keywords yourself.
- Identify irrelevant terms and add negatives: account level if the term is irrelevant to the entire business, or campaign/ad group/list level if it is only irrelevant for particular products.
- Go beyond negation: ask why the query triggered at all. The root cause is usually the product title and description, so treat negatives as a plaster and fix the feed.
- Example mechanism: if you sell men's running shoes but the title/description doesn't clearly state size or shoe type, Google may match your product to the wrong queries. Making titles and descriptions specific channels indexing in the right direction.
- Recheck the search term report after feed changes to confirm the mix of queries has shifted.
Caveat: Negative keywords suppress future serving but do not correct Google's product indexing on their own.
Caveat: Account-level negatives should stay reserved for genuinely business-wide irrelevant terms.

Tags: google-ads, shopping-ads, negative-keywords, search-terms, feed-optimization, optimization
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Consolidate Shopping Campaigns Around Best Sellers for Small Accounts
Use when: Deciding account structure and budget allocation for a DTC store spending roughly 50k–500k per month, or launching a new Shopping account.
- Launch focused on best sellers — spreading an initial budget across the whole catalogue gives each product so little spend that learning is slow and growth is prolonged.
- Accept a consolidated structure if traffic volume is limited: the source argues stores in the ~50k–500k/month range rarely have enough traffic to benefit from heavy segmentation.
- In existing accounts, identify top performers and review the distribution of spend to confirm they receive adequate daily and weekly budget.
- If a best seller is underfunded inside a shared campaign, break it out into its own campaign so it can be controlled and scaled.
- Only expand budget to new or underfunded products once top performers are adequately funded and performance is proven.
Caveat: The 50k–500k per month range is the source's working heuristic, not a derived threshold.
Caveat: Segmentation becomes more viable as ad account scale and traffic grow.

Tags: google-ads, shopping-ads, campaign-structure, budgeting, best-sellers, scaling
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Choose Manual Bidding for New Shopping Accounts, Target ROAS After ~30–50 Monthly Conversions
Use when: Choosing or changing bid strategy for a Shopping campaign based on how much conversion data the account has.
- For a new account with no historical conversion data, apply a manual approach — Manual CPC with a set maximum you're willing to pay per click, or Maximise Clicks.
- Once the Shopping campaign has roughly 30–50 monthly conversions, transition to Target ROAS.
- Before setting a tROAS, look at the actual ROAS over the first four to six weeks of the campaign. If actual ROAS was around 250%, do not set a 400% target.
- Set the target at or slightly below the observed actual ROAS so the algorithm has room to breathe and spend; an over-aggressive target chokes delivery and the campaign stops spending.
- If you later need more aggression for scale, lower the Target ROAS rather than reverting to manual bidding.
- Recheck conversion volume and observed ROAS before each strategy change.
Caveat: The 30–50 monthly conversions figure and the 250% vs 400% example are source heuristics illustrating the principle, not universal thresholds.
Caveat: Bid strategy suitability is explicitly stated to depend on where the account is currently positioned.

Tags: google-ads, shopping-ads, bid-strategy, target-roas, manual-cpc, scaling, measurement
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Set Up a Sales-Objective Search Campaign
Use when: Launching or rebuilding text search campaigns for a DTC store in Google Ads.
- Create the campaign at ads.google.com → Campaigns → plus button. Choose objective Sales for DTC (Leads only if B2B).
- Set conversion goals to purchases only. The source calls out the common mistake of leaving page views or add-to-carts in the goal set — Google then optimizes for outcomes that aren't purchases. For an ecommerce store, purchases should be the sole goal in ~99% of cases per the source.
- Select campaign type Search, enter your URL, choose website visits as the destination, and name the campaign to encode channel, geography and brand/non-brand scope.
- Choose bidding focus. For multi-price catalogues, focus on conversion value so Google optimizes toward higher-value orders; single-SKU or subscription businesses may reasonably differ.
- In settings, turn off Search Partners and Display Network — the source reports search partners rarely outperforming core search.
- Set location, then open Location options and change from 'Presence or interest' to 'Presence' to avoid paying for worldwide users merely 'interested' in your market (e.g. during a US election cycle).
- Set language to your target market unless you intend to serve additional languages; leave audience segments on observation or blank; skip AI Max if you want to retain control.
- Enter keywords manually if you've done proper research, using punctuation to set match type: none = broad, quotes = phrase, brackets = exact.
- Set average daily budget — this is a daily average, not a total cap. Google's forecasts are described as often inaccurate; start with a budget you're comfortable losing and raise it conservatively.
Caveat: Ad interface labels, conversion goal names and AI Max availability change; verify the current UI.
Caveat: The source flags forecasts as unreliable and advises not expecting overnight results.

Tags: google-ads, search-ads, campaign-setup, conversion-tracking, location-targeting, match-types, budgeting
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Build RSA Assets with Variety, Not Padding
Use when: Writing search ad copy for a new or existing search campaign.
- Enter the final URL pointing to the landing page you want traffic on — homepage, collection page, product page or a listicle — not necessarily the homepage.
- Use display paths to signal relevance after the domain (e.g. /running-shoes) so users see they'll land on a page matching their intent.
- Write up to 15 headlines; include keywords where natural, and ensure each headline is unique and adds value rather than filling space.
- Mix asset types across headlines and descriptions: features, benefits, offers, urgency and calls to action, giving Google variance to test.
- Write up to four descriptions of 90 characters each in sentence case (headlines in title case), with at least two required; two descriptions can serve at once.
- Add images where available — no text or overlays — favouring clear product-centric or lifestyle shots.
- Include the business name for advertiser transparency and the business logo/favicon.
- Add site links that route to different destinations than the primary landing page (men's, women's, kids' categories; delivery and returns pages) and callouts as 25-character business facts such as free shipping thresholds, returns windows or review counts.
Caveat: Character limits and asset-type availability (images, structured snippets, phone, address) vary by market and change over time; verify in the current UI.
Caveat: The source focuses on callouts, site links and images as the most common extensions rather than covering all asset types.

Tags: google-ads, search-ads, ad-copy, responsive-search-ads, extensions, landing-page, creative-strategy
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Set and scale Google Ads campaign budgets safely
Use when: Launching a new Google Ads search campaign or increasing budget on an existing one.
- Enter an average daily budget — the amount Google can spend per day on average, not a lifetime cap that stops the campaign once exhausted.
- Treat Google's conversion, conversion value and cost-per-conversion forecasts as unreliable, especially when starting out; do not build spend decisions on them.
- Start only with a budget you are comfortable losing entirely, since early performance is volatile.
- Scale gradually rather than doubling or tripling overnight: the source suggests moving from $50/day to $60, then $70, then $100.
- Remember every setting (budget, bidding, keywords) can be changed at any point during the campaign's life.
- Expect delayed serving and volatile, sometimes very expensive initial clicks while Google learns; wait up to a day before troubleshooting.
- If no serving occurs beyond one to two days, check bidding setup and whether keywords have enough search volume.
Caveat: The $50→$100 example is the source's illustrative path, not a benchmark; choose increments based on your own margins.
Caveat: Google's budget forecasts are described as 'vastly inaccurate' — verify performance with your own data.

Tags: google-ads, budget-management, campaign-setup, scaling, bidding
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Choose keyword match types by account maturity and goal
Use when: Deciding whether to add exact, phrase or broad keywords to a search campaign.
- Understand the three types: broad match (no notation) casts the widest net; phrase match (quotation marks) is moderate; exact match (square brackets) is tightest, requiring near-identical meaning or intent.
- If your account is new, has little conversion data, or you prioritize efficiency, lead with exact match keywords you know convert (e.g. from Amazon or previous tests) to avoid wasted spend.
- If you are growth-focused and have substantial conversion data, lean into broad match, which pairs well with automated bid strategies like Maximize Conversion Value or Target ROAS.
- For a middle-ground approach the source suggests roughly 80% exact match plus core broad-match keywords, using broad to surface new converting search terms that you later promote to exact.
- Note that the source's team is using phrase match less because it has become broader in behavior.
Caveat: The '80% exact' split is the source's heuristic, not a calculated rule.
Caveat: All match types are trending broader as Google shifts away from manual keyword control; re-verify current behavior in the interface.

Tags: google-ads, keyword-research, match-types, campaign-setup, bidding
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Classify keywords into four funnel types before targeting
Use when: Planning keyword lists and choosing where each keyword's traffic should land.
- Informational (top of funnel, e.g. 'how to take collagen for best results'): users want education, not purchase — send to an advertorial-style landing page or blog, not a PDP.
- Commercial (mid funnel, e.g. 'best collagen powder for women over 50' or competitor comparisons): users are comparing; bucket with transactional keywords under 'performance search'.
- Transactional (mid-to-bottom funnel, e.g. 'buy collagen powder for women over 50'): imperative verbs signal near-purchase; route to purchase-ready pages.
- Navigational (bottom funnel, mostly branded, e.g. '[brand] collagen reviews' or promo-code searches): send to a reviews page, promo page, or the specific product page.
- Concentrate keyword research effort on commercial and transactional terms, since that is where most advertisers compete and where better research has the biggest impact.
Caveat: Sending informational traffic straight to a product page is ineffective because intent does not match, per the source.

Tags: google-ads, keyword-research, intent, landing-page, campaign-setup
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Run the seed-expand-segment keyword research method
Use when: Building or rebuilding a search campaign keyword list for a DTC product.
- Find 20-30 seed keywords: two-to-three-word phrases identifying your core product (e.g. 'collagen', "women's collagen", 'marine collagen').
- Expand each seed into long-tail keywords mirroring how users now search (e.g. from 'women's collagen': 'best collagen for women', "women's collagen for joint support", 'best collagen for women over 50', 'tasty collagen for women').
- Validate candidates in Google Keyword Planner for search volume, 3-month and year-on-year change, competition, and low/high top-of-page bid ranges.
- Estimate likely conversion rate from historical paid traffic and store data; if the CPC, conversion rate and target CAC/ROAS numbers don't work, exclude the keyword initially.
- Segment surviving keywords into themed ad groups (e.g. women over 50, joint support, flavor, flavorless, peptides, hair growth, collagen with vitamin C) so ad copy and landing pages stay tightly aligned.
- Expect to reduce hundreds of long-tail candidates down to roughly 20-25 to target initially.
Caveat: Keyword Planner bids and volumes are directional, not exact.
Caveat: The 20-30 seeds and 20-25 final keywords are the source's working ranges, not fixed thresholds.

Tags: google-ads, keyword-research, keyword-planner, campaign-structure, customer-research
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Use Keyword Planner, Semrush and ChatGPT for keyword ideation
Use when: Generating more long-tail keyword ideas after you've defined your seed keywords.
- Use Google Keyword Planner for volume, 3-month and year-on-year trend, competition level, and low/high top-of-page bid estimates.
- Use Semrush (paid) for keyword ideation and research — the source recommends it as a long-standing tool but notes it isn't required.
- Give ChatGPT your seed keywords and ask it to generate additional long-tail variations once Planner and Semrush ideas run out; it's good at exhaustive long-tail lists.
- Identify and define the core seed keywords yourself rather than relying on ChatGPT for that step.
- Combine all sources, then filter against CPC, competition, expected conversion rate and target CAC/ROAS before loading anything into campaigns.
Caveat: Semrush is optional; Google Ads plus ChatGPT can work for low-budget accounts.
Caveat: ChatGPT output duplicates and inaccuracies are common — validate against Keyword Planner.

Tags: google-ads, keyword-research, keyword-planner, semrush, chatgpt
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Apply negative keyword match types correctly
Use when: Filtering irrelevant search terms out of a search or shopping campaign to cut wasted spend.
- Broad negative (plain term, e.g. running shoes): blocks searches containing all terms in any order; e.g. 'blue running shoes' and 'shoes running' blocked, but 'blue tennis shoes' (missing 'running') and 'running shoe' (singular) may still show.
- Phrase negative (quotation marks): blocks searches containing the exact terms in the same order with other words allowed around them; 'blue running shoes' blocked, but 'shoes running' (wrong order) may show.
- Exact negative (square brackets): the tightest — blocks only searches matching the exact terms in the same order with no extra words; almost everything else may still show.
- Use broad negatives where a single variant represents a clear category you never want (e.g. a competitor or a different product type); use exact when you only want to exclude a specific query.
- Note that all three negative types apply, and match-type logic mirrors positive keywords.
Caveat: Singular/plural differences (shoe vs shoes) affect blocking — spell out variants you need to exclude.
Caveat: Broad negatives can accidentally block valuable long-tail queries if not chosen carefully.

Tags: google-ads, negative-keywords, match-types, ad-spend, campaign-setup
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Choose negative keyword level and review cadence
Use when: Setting up a negative keyword structure or deciding how often to review search term reports.
- Add negatives individually (when you spot a bad search term in the report) or as a negative keyword list you can apply in bulk.
- Apply at ad group level for tightest control; at campaign level to affect all ad groups in one campaign; at account level to affect all existing and future campaigns.
- Note the hierarchy: account negatives affect everything, campaign negatives affect that campaign's ad groups, ad group negatives affect only that ad group.
- Review search term reports daily in new accounts or while testing new keywords/products, adding negatives immediately to save money from day one.
- Reduce to a couple of times per week once performance is stable and search terms are cleaner — sometimes no additions will be needed.
Caveat: Account-level negatives persist into new campaigns, so use them sparingly or they will apply invisible constraints across everything.
Caveat: Daily review is most valuable early; frequency should flex with search volume and account maturity.

Tags: google-ads, negative-keywords, search-terms, ad-spend, campaign-management
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Use quality score to understand ad rank and CPC
Use when: Diagnosing why the same keyword costs far more than competitors or planning account improvements.
- Understand ad rank: on each search, Google rates eligible ads and serves higher-ranked ones in better positions.
- Recognize the bid is only one ad-rank input; improving ad quality is usually cheaper than raising bids to climb positions.
- Assess quality score's three components: expected click-through rate (vs competitors), ad relevance (does the ad match query and intent), and landing page experience (load speed, responsiveness, relevance, conversion).
- Check components in the keyword view — a keyword scoring 3 can have below-average expected CTR while ad relevance and landing page experience are average; fix the weakest first.
- Note that a single keyword's average CPC was reduced from $5.84 to $2.38 (per the source) through ad and landing page tweaks, illustrating that quality score directly affects unit economics and scalability.
Caveat: The $5.84→$2.38 example is a source example, not a guaranteed outcome; results depend on the keyword and account.
Caveat: Quality score components are relative to other advertisers, so they change even when you aren't making edits.

Tags: google-ads, quality-score, ad-rank, cpc, measurement
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Improve quality score via three levers
Use when: Working on a low quality score keyword or preparing a new search campaign for competitive terms.
- For expected CTR: strengthen headlines; match user intent — don't serve a 'best collagen' ad to someone researching 'benefits of collagen powder' at the top of the funnel.
- Add relevant ad extensions (sitelinks, callouts) to give users more information and more reasons to click.
- Continuously test headline angles — expected CTR is relative and non-static, so standing still while competitors test means your score declines.
- For ad relevance: segment ad groups by intent/theme so ad copy can address one user need; use dynamic keyword insertion so the actual search query appears in the headline or description.
- Match the user's language — use problem-aware phrasing for problem-aware queries, not technical jargon the searcher may not know.
- For landing page experience: improve load times (use PageSpeed Insights), match landing page headlines to ad headlines and search queries, provide clear CTAs and a frictionless conversion path, and optimize for mobile.
Caveat: Landing page experience includes whether the page converts well (per the source), not just speed and match.
Caveat: Dynamic keyword insertion requires careful capitalization/fallback setup to avoid awkward renderings.

Tags: google-ads, quality-score, ad-copy, landing-page, conversion-optimization
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Build single theme asset groups (STAGs) instead of mixed ad groups
Use when: Restructuring an existing search campaign or building a new one where keywords have divergent intents.
- Replace messy ad groups containing mixed intents (e.g. 'buy running shoes', 'cheap gym trainers', 'shoes for plantar fasciitis', 'running shoes for women') with single-theme groups like general running shoes, bargain hunters, plantar fasciitis, ladies trainers.
- Within each theme, align keywords, ad copy and landing page so a user searching a plantar-fasciitis term sees plantar-fasciitis language in the ad and lands on a page addressing that need.
- Expect STAGs to lift all three quality score components: higher CTR from tighter matching, higher ad relevance, and better landing page experience (longer dwell, fewer bounces, more conversions).
- Segment further where intents diverge — the source says not all keywords in a suggested theme must sit in one ad group if intent differs.
- This replaces the older SCAG (single keyword ad group) approach the source used in 2018-2019.
Caveat: More granular ad groups mean more management overhead; the source accepts this tradeoff for the relevance gain.
Caveat: The lift described is the source's observed mechanism, not a guaranteed outcome for every account.

Tags: google-ads, campaign-structure, quality-score, ad-copy, landing-page
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Size ad groups with 2-8 keywords to preserve relevance
Use when: Segmenting keyword lists into ad groups for a search campaign.
- Place two to three keywords per ad group, and up to about five to eight.
- When adding a keyword that doesn't fit the ad group's theme, create a new ad group instead of forcing it in.
- Er on the side of breaking things out rather than bundling — the source repeatedly prefers more granular segmentation to protect keyword/ad/landing page alignment.
- Recheck segmentation whenever you add a new keyword found via search term reports or broad-match expansion.
Caveat: The 2-3 to 5-8 range is the source's working heuristic, not a fixed rule.
Caveat: Very granular structures require more ad copy and landing page variation to maintain the benefit.

Tags: google-ads, campaign-structure, keyword-research, ad-copy, relevance
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Write headlines that grab, match intent and drive action
Use when: Writing or testing RSA headlines for a search campaign.
- Ensure each headline does one of three jobs: grab attention with an emotional hook or benefit, match user intent by including target keywords where possible, or guide action with a clear imperative verb (Shop, Buy, Explore, Learn).
- Use title case for readability (e.g. 'Shop The Collection').
- Use numbers and symbols to stand out on a noisy SERP — e.g. inseam lengths like 5", 7.5", 9", or a '#' symbol for 'number one'.
- Use 'you' and 'your' to speak directly to the searcher (e.g. 'Your New Favorite Shorts').
- Reflect positive outcomes that matter to your customer (e.g. 'Burn Fat And Glow').
- Show off your offer in a headline when it is strong — e.g. a free trial or a limited-time bundle discount — since offers increase clickability.
Caveat: Headlines match user intent by including target keywords, but don't force irrelevance — a 'best collagen' headline wastes money for a searcher researching benefits.
Caveat: Offer headlines assume a genuinely strong offer; weak offers won't rescue click-through.

Tags: google-ads, ad-copy, creative-strategy, conversion-optimization, search-campaigns
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Write descriptions to close, handle objections and build trust
Use when: Drafting RSA descriptions for a search campaign.
- Treat descriptions as the closer — their job is handling objections, reinforcing value, adding urgency and providing trust signals before the click.
- Use a problem-solution format, optionally drawn from a customer review to add credibility (e.g. 'Our dog had the worst breath and this is the only product that has worked').
- Use an offer-deadline format to create urgency (e.g. 'Hurry before they're gone. Get yours with monthly toys and treats').
- Use a benefit + trust signal format (e.g. 'Skin-loving ultra gentle close shave, dermatologist approved for sensitive skin').
- Remember two descriptions can serve at once and each is up to 90 characters, so pair formats that don't duplicate each other.
Caveat: The example formats are observed from competitor accounts; test which format your audience responds to rather than assuming one wins.

Tags: google-ads, ad-copy, creative-strategy, conversion-optimization, trust-signals
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Avoid maxing out and pinning RSA assets
Use when: Building or revising a responsive search ad.
- Don't max out 15 headlines for the sake of it — the source typically uses seven to eight or nine so that individual asset performance is not diluted across traffic.
- Ensure headlines vary meaningfully because two or three serve together; do not use near-identical headline variants.
- Test headline angles continuously; once you have seven to nine headlines, click-through feedback on what works arrives relatively quickly.
- Pin headlines or descriptions only when you have a specific reason: a promotion that must always show, or an angle with proven high CTR. Otherwise let Google rotate assets.
- Treat Google's 'ad strength' indicator as separate from ad rank; don't fill every slot just to satisfy ad strength.
- Add more headlines only if you have genuinely distinct viable angles that need testing.
Caveat: Google's own interface recommends filling more assets; the source disagrees in the interest of clean test read-outs.
Caveat: Pinning a promotion ensures delivery but reduces the rotation freedom of other assets.

Tags: google-ads, ad-copy, experiment-design, creative-strategy, responsive-search-ads
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Test RSAs with 7–9 Headlines, Not Always 15
Use when: Building or refreshing responsive search ads for a search campaign and deciding how many headline and description variants to write.
- Write 7–9 headline variants covering distinct angles you believe are viable for the product or category, rather than padding to Google's 15-headline maximum.
- Add more variants if you genuinely have more viable angles, but do not treat Google's ad strength meter as a reason to fill every slot; ad strength is a separate signal from ad rank.
- Let Google rotate them unpinned in most cases; only pin when you have a promotion that must be shown, or a proven high-CTR angle that must always serve.
- After a short run, pull headline and description performance, keep the winners, remove the losers, and add a few new angle variants to keep testing.
- Review performance on a regular cadence rather than setting copy and revisiting 12 months later, because new competitors enter the auction with new angles.
Caveat: The 7–9 figure is the presenter's working heuristic, not a performance benchmark.
Caveat: Pinning limits Google's testing flexibility, so pin only with a stated reason.

Tags: google-ads, creative-strategy, responsive-search-ads, ad-copy-testing, conversion-optimization, search-campaigns
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Five Ad Assets That Expand Search Real Estate
Use when: Finalizing search ad assets for a campaign and choosing which extensions to add for a product category or store.
- Add sitelinks pointing to useful non-homepage destinations: bestsellers, collection pages, new arrivals, promotions/clearance, and a reviews page for social proof.
- Add up to 10 callouts of 25 characters each that highlight concrete differentiators (for example battery life or included services) that could tip a click.
- Add a promotion asset for live sales or evergreen offers, and optionally repeat the offer in the headline.
- Use price assets mainly when you want to show value on low-cost ranges ('starting from') or to disqualify clicks on high-priced or luxury items.
- Add structured snippets — styles/categories for most stores, or brands stocked if you are a reseller — to add another scannable line of relevance.
- Treat these as a repeated test area: refresh assets as offers and ranges change so the larger ad footprint stays relevant.
Caveat: Extension types, character limits and the ad-assets interface change; verify current formats in the account before building.
Caveat: The source notes price assets are used only occasionally and suit specific cases.

Tags: google-ads, search-campaigns, ad-extensions, clickthrough-rate, merchandising, conversion-optimization
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Bid Strategy Progression for New vs Existing Accounts
Use when: Choosing a bid strategy for a new or recently relaunched account, or planning when to switch a store's search campaigns to automated bidding.
- In a new account or one without recent conversion history, avoid automated bidding first — machine learning has little data and tends to bid erratically and inflate CPCs.
- Choose manual CPC (set a max cost per click per keyword, preferring this roughly 70–80% of the time per the source) or maximize clicks (give a daily budget and let Google buy the most clicks, optionally with a CPC ceiling) to generate conversion data quickly.
- Manually review and trim keywords and search terms using that data; the goal is enough conversions to justify automated bidding.
- Treat an account as 'existing' only if it has recent conversion history; a paused account returning after a long gap should be treated as new.
- For existing accounts, pick maximize conversion value over maximize conversions, because e-commerce orders have different values and the algorithm should weight high-value purchases.
- Start new campaigns on maximize conversion value with a daily budget around 3–4x average order value, let it learn, then move to target ROAS at roughly 30–50 conversions per month.
Caveat: Conversion thresholds (30/50 per month) are the source's stage heuristics, not calculated rules.
Caveat: Lead-gen-style fixed-value models suit target CPA; variable-basket stores generally suit target ROAS.

Tags: google-ads, bid-strategy, search-campaigns, measurement, scaling, conversion-optimization
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Set Target ROAS At or Below Historical Actuals
Use when: Moving a store's campaign from maximize conversion value to target ROAS bidding, or when a target-ROAS campaign has stopped spending.
- Review actual ROAS over roughly the last 30 days under the current bid pattern before setting any target.
- Set the first target ROAS at that actual level or slightly below it (for example ~250% actual, set 220–250%) and hold it for at least 2–3 weeks.
- Let the campaign spend and generate data; too-low a target risks blowing through efficiency KPIs, so align it to what the business genuinely needs.
- Raise the target gently as you observe improved efficiency, or hold the target and scale through budget if growth is the goal.
- If a target-ROAS campaign stops spending or performance collapses, suspect the target is set too far above what the account has actually achieved.
Caveat: A very high target does not create efficiency; it usually just stops spend entirely, so this is a constriction risk not a stretch goal.
Caveat: Target ROAS and target CPA behave relative to the target you set — the ranking or auction does not change to meet it.

Tags: google-ads, bid-strategy, target-roas, scaling, measurement, ecommerce
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Check Google Can Read Your Site Before Running DSA
Use when: Deciding whether dynamic search ads are viable for a store, or diagnosing poor DSA relevance.
- In an existing account, open Keyword Planner and use the option to get keyword ideas from your site or specific URLs.
- Enter the landing pages you plan to target with DSA and review whether returned keywords match the product category intent you actually want.
- If Google surfaces branded and category-relevant terms (as in the source's example of a supplement brand returning category terms), DSA can likely work.
- If the output is irrelevant or generic, fix page clarity and crawlability before launching DSA, because DSA headlines, keywords and landing page selection all run off Google's interpretation of the site.
Caveat: DSA gives Google autonomy over headlines, keywords and landing page choice — you only supply descriptions, assets and ad targets.
Caveat: Keyword Planner interface options change; confirm the current interface before following these steps.

Tags: google-ads, dynamic-search-ads, keyword-research, product-page, measurement, search-campaigns
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Configure DSA Targets and Negatives by Category
Use when: Setting up or cleaning up dynamic search ads for a multi-category store.
- Choose your ad targets: all landing pages from standard ad groups, URL-based rules (URL contains a category term), category equals, or specific URLs.
- Segment at the ad group level by theme — one DSA ad group per category such as men's shoes, women's shoes, children's shoes — rather than mixing everything in one group.
- Add negative ad targets for pages you don't want crawled or served against, such as privacy policy, blog pages and return policy, especially in the initial phase.
- Once running, review your search term report frequently and continue adding irrelevant terms as negatives.
- Apply the same bidding discipline as RSAs: manual bidding in a new account, then automated once conversions reach roughly 30+ per month per the source's heuristic.
Caveat: DSA is best used to expand reach and mine new keywords alongside existing RSAs, not usually as the sole campaign type.
Caveat: Google's autonomy means the landing page a visitor sees may differ from the one you'd pick.

Tags: google-ads, dynamic-search-ads, search-campaigns, keyword-research, negative-keywords, ecommerce
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Use DSA as a Test Proxy for Performance Max Search
Use when: Planning a move into Performance Max or deciding whether to run DSA first for a store.
- If already running shopping or video campaigns, add DSA campaigns to generate readouts on how search within Performance Max is likely to perform.
- Compare DSA search performance against your existing RSA performance to gauge whether adding Performance Max makes sense.
- Use DSA for keyword mining at the same time: it can surface new converting search terms that RSA keyword research misses given the volume of new queries daily.
- Feed any strong DSA search terms back as keywords in more tightly controlled campaigns.
Caveat: This is the source's analogy, not a guaranteed equivalence — treat DSA results as directional evidence.
Caveat: Performance Max behavior and interface change often; confirm current capabilities.

Tags: google-ads, dynamic-search-ads, performance-max, keyword-research, search-campaigns, testing
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Decide Whether to Run Branded Search
Use when: Deciding whether to allocate budget to a branded search campaign for a store.
- Run branded search if competitors are bidding on your brand name, or if the account is new and needs easy conversion volume to feed machine learning.
- Skip it (per the source, almost always) if there is no competitor bidding and your organic listing reliably shows first for brand queries, since you would just pay for traffic you already get.
- If you run it, target exact match brand variations (brand, brand + shoes, brand reviews, brand men's) and map each to a relevant page — reviews page for review queries, collection page for category queries.
- Add your brand as phrase match to capture untargeted long-tail brand terms, then promote converting search terms from the search term report into exact match keywords.
- Exclude branded terms from all other search campaigns via negative keyword lists or brand exclusions, so non-brand campaigns are measured on genuinely incremental traffic.
Caveat: The 'almost always skip' stance is the presenter's opinion and depends on your organic ranking and competitive reality.
Caveat: Excluding brand from other campaigns matters for interpreting incrementality; not doing so inflates non-brand performance.

Tags: google-ads, branded-search, search-campaigns, measurement, negative-keywords, retention
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Branded Search Ad Copy, Bidding and 90% Impression Share
Use when: Setting up copy, bids and targets for a branded search campaign.
- Pin headline one to your brand name with an authority framing (for example 'brand official store'), since searchers are already looking for you.
- Test multiple headline-two angles — offer, shipping, feature/benefit — but generally pair the brand headline with some form of offer.
- Add multiple sitelinks to expand the ad and send users to collection pages, active promotions, bestsellers and a dedicated reviews page for trust.
- Bid with manual CPC and aim for over 90% impression share, or use target impression share as an alternative; the source avoids automated bidding on branded campaigns.
- Track the cost per conversion — the source expects branded conversions to cost only a couple of dollars — and investigate if it is materially higher.
Caveat: The 'over 90% impression share' and 'couple of dollars' figures are the source's targets, not universal benchmarks; they will vary by market and competition.
Caveat: The advice to never use automated bidding on branded campaigns is a strong presenter preference and should be treated as opinion.

Tags: google-ads, branded-search, bid-strategy, ad-copy-testing, search-campaigns, conversion-optimization
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Performance Max Basic Setup for Ecommerce
Use when: Launching a Performance Max campaign for an ecommerce store.
- Create a new campaign, choose Sales, optimize for purchases, select Performance Max and link your Merchant Center account so products are available.
- Choose conversion-value focus rather than conversion-count focus, since order values differ across the catalogue.
- Leave the target ROAS field blank initially and let the campaign run on maximize conversions for the first 2–4 weeks so the algorithm can learn.
- Set location and language, then add a brand exclusion (all brand spellings and misspellings) or a negative keyword list so the campaign does not serve on your own brand where dedicated branded campaigns exist.
- Skip Google's AI asset generation and supply your own assets: roughly 6–7 headlines (30 characters each), long headlines (90 characters), and 3–4 descriptions (90 characters), plus images, videos, sitelinks and extensions.
- Name each asset group by product theme and segment by theme rather than selecting all products, because centralizing copy, landing pages and creative around one theme is more coherent than letting Google bundle everything.
Caveat: Interface layout for campaign creation changes; verify current steps in the account.
Caveat: The source says more than 15 headlines is unnecessary but that filling slots is optional.

Tags: google-ads, performance-max, campaign-setup, ecommerce, creative-strategy, merchandising
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Performance Max Budget, Search Themes and Audience Signals
Use when: Sizing budget and configuring signals at Performance Max launch for a store.
- Set the average daily budget at least at 3x your non-branded average CPA — for example, a $40 CPA implies a floor of about $120/day.
- If the store cannot commit roughly $100/day to Performance Max, prefer running shopping and search campaigns instead of funneling a small budget into PMax.
- Add search themes only if you deliberately want to push search hard inside PMax, using proven converting keywords or search terms from the account; otherwise omit them because they can cannibalize traffic from your search campaigns.
- Add audience signals using first-party lists — all-time customers, top-value customers, or last-12-months customers — which the source has seen shorten the learning phase compared with leaving it blank or using custom/in-market segments.
Caveat: The 3x average CPA budget rule and roughly $100/day minimum are the source's heuristics, not calculated requirements.
Caveat: The source reports poorer performance when search themes are added throughout their accounts and mixed outside feedback on audience signals — treat both as directional.

Tags: google-ads, performance-max, budgeting, audience-signals, customer-research, ecommerce
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Performance Max Learning Phase and Bid Progression
Use when: Managing an early-stage Performance Max campaign and deciding when to change bid strategy.
- Expect a long learning phase for Performance Max — sometimes 4–6 weeks — and avoid frequent structural changes that prolong it.
- Start on maximize conversion value and review whether the campaign reaches roughly 50 conversions per month inside a single campaign.
- At that point transition to target ROAS and set the target at or slightly below the campaign's actual ROAS so the algorithm keeps room to spend.
- Then either scale by raising spend while holding the target, or gently raise the target ROAS as efficiency improves.
- Review campaign structure changes only after the learning phase has settled.
Caveat: The 50-conversions-per-month threshold is the source's heuristic and should be tested against your own campaign volume.
Caveat: Setting target ROAS far above actual performance typically strangles spend rather than improving efficiency.

Tags: google-ads, performance-max, bid-strategy, target-roas, scaling, measurement
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Ongoing Performance Max Optimization Checklist
Use when: Running weekly or monthly optimization on a Performance Max campaign for a store.
- Review search term reports (and search categories) for irrelevant terms and add negatives; in new accounts or new campaigns check every 48–72 hours.
- Check brand exclusions are in place for both your own brand and, if desired, competitor brands, keeping brand and non-brand traffic cleanly separated for honest performance measurement.
- Review channel/new PMax reporting to see impressions, interactions, spend and purchase value by network — search vs shopping vs video — and use a script like the one credited to Mike Rose for asset-group level cost and top-product detail if in-platform reporting is incomplete.
- Inspect audience segments for demographic and in-market skew (the source cites an example of 5x more clicks from one age band) and use those findings to build custom segments for this or other campaigns.
- Review asset performance (headlines, descriptions), remove persistently poor performers and add fresh angles to test on a recurring basis.
Caveat: Micro-script and channel reporting availability varies by account and UI state; verify current reporting before relying on it.
Caveat: Asset performance labels are Google's representations, not ground-truth conversion measures.

Tags: google-ads, performance-max, measurement, negative-keywords, creative-strategy, audience-signals
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Choose One or Two Performance Max Campaigns Over Sprawl
Use when: Structuring a store's Performance Max campaigns when deciding between consolidation and segmentation.
- When running significant shopping and manual search alongside PMax, consolidate into one PMax campaign with asset groups separated by theme (bestsellers, category two, category three).
- If a theme — for example bestsellers — is not getting adequate budget, extract it into a second, scaling-focused PMax campaign with a more aggressive target aimed at known bestsellers and top converters.
- Keep the remaining adjunctive categories in the efficiency-focused campaign.
- Reach for consolidation first; the source notes most brands in the roughly $100k–500k/month Google Ads range still benefit most from consolidated structure, with segmentation becoming more worthwhile above that level and only in certain cases.
Caveat: The $100k–500k per month range is the source's observation of its client base, not a formula.
Caveat: Even above that level, the source says there are cases where segmentation is better — do not treat consolidation as an absolute rule.

Tags: google-ads, performance-max, scaling, campaign-setup, budgeting, ecommerce
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Demand Gen for Remarketing to Cart Abandoners
Use when: Setting up a remarketing campaign to recover abandoned carts for an ecommerce store.
- Go to ads.google.com, open campaigns, create a new campaign, choose sales as the objective and purchases as the conversion focus.
- Select Demand Gen as the campaign type, which serves image and video ads across YouTube, Discover, Gmail and the display network, so you can reach returning visitors without relying on display alone.
- For the starter campaign in the source's example, target cart abandoners so the ads speak directly to people who reached the cart but did not complete a purchase.
- Serve dynamic remarketing creative so the ads reference the products the visitor viewed.
- Use Demand Gen for remarketing before display; the source reports Demand Gen far outperforming display for remarketing across its accounts.
Caveat: The source's remarketing example is described as a setup demonstration — no specific conversion lift figures are given, so avoid assuming results.
Caveat: Demand Gen placement and campaign creation options change frequently; verify the current interface.

Tags: google-ads, demand-gen, remarketing, cart-abandonment, retention, conversion-optimization
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Demand Gen remarketing setup for cart abandoners
Use when: Setting up a Google Ads retargeting campaign aimed at shoppers who added to cart but did not buy.
- Go to ads.google.com, click Campaigns, then the blue plus button and New campaign.
- Choose Demand Gen as the campaign type; set objective to Sales and conversion focus to Purchases.
- For a cart-abandoner campaign the source generally excludes the product feed and reports stronger performance without it.
- Leave target cost per action unset initially; give the campaign a daily budget (the walkthrough used a £50/day example).
- Set location and language at ad group level, and typically turn off TV screens under device targeting.
- In the ad group, add your imported cart-abandoner audience as a custom audience and add no other audience signals.
- Turn OFF optimized targeting — for remarketing you want only people who performed the desired action, not lookalike expansion.
- Choose channels: the source excludes the Google Display Network and runs YouTube (in-stream, in-feed, Shorts, Discover) plus Gmail, which they report gives higher-quality traffic.
- Pick an ad type based on the offer: single image for a strong simple offer, carousel image for high product variety, video when storytelling or offer nuance is needed.
Caveat: The channel mix that works for one account may differ; the presenter explicitly says others will have different opinions on excluding Display.
Caveat: Requires a large enough cart-abandoner list to be worth targeting.

Tags: google-ads, demand-gen, retargeting, cart-abandonment, campaign-setup, audience-targeting
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Five objections that explain cart abandonment and how to answer them in ads
Use when: Writing retargeting ad creative or offer copy for cart abandoners, and choosing which objection to lead with.
- Bucket each abandonment reason into one of five objections; the source notes more than one can apply.
- Complacency/distraction — the shopper was browsing casually and forgot. Answer with urgency so they feel the offer may expire; the source shows a high-urgency static creative as the example.
- Price/value — 'too expensive.' Answer by justifying price, comparing to competitors, or using price-per-unit for CPG-style products; the source cites Harry's comparing a $16 refill against a market leader at $40, and positioning the product as an investment rather than a purchase.
- Trust/credibility — 'is this company legit?' Answer with PR callouts, third-party review platforms (e.g. Trustpilot) and as much social proof as possible throughout the funnel.
- Product efficacy — 'will this even work?' Answer with real customer photos and inset reviews so prospects see someone like themselves for whom it worked.
- Logistic friction — shipping, delivery time, cost, returns. State your shipping/returns/warranty terms as attractively as your margins allow; the source's example shows free worldwide shipping and returns plus a 24-month warranty.
- Once you see which objection audience responds to on remarketing, push that same signal (trust/social proof, etc.) up into higher-funnel creative to prevent abandonment earlier.
Caveat: Not every brand can offer free worldwide shipping and returns; the source says to offer the most attractive options within your means.
Caveat: Example competitor pricing and review screenshots are illustrative, not benchmarks.

Tags: google-ads, retargeting, creative-strategy, cart-abandonment, objection-handling, offer-design
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Is YouTube a fit for your store? Four prerequisites
Use when: Deciding whether to add or launch a YouTube/Demand Gen channel for a DTC store.
- Check AOV: the source says a $25–$30 AOV makes success very unlikely; $75–$100 is ideal and anything above $50 is usually a workable starting point.
- Check demonstrability: can you clearly show the product's value in video? If not, YouTube is likely the wrong channel.
- Check patience and budget: expect choppy performance for an initial four-to-six-week period before deciding.
- Check your Meta creative: you should already have winning ad creative on Meta before moving to YouTube — do not use YouTube as a creative testing ground.
- Validate your offer on Meta first (faster feedback) and know your customer avatar in detail; the source says if you don't know your avatar inside out, do not touch YouTube ads.
- If budget is already spread thin across acquisition channels, don't cannibalise a working channel to fund YouTube — consolidate on what works.
Caveat: AOV thresholds are the presenter's working heuristics, not calculated benchmarks.
Caveat: If AOV, demonstrability or patience are missing, the source recommends waiting rather than forcing the channel.

Tags: google-ads, youtube-ads, channel-strategy, average-order-value, creative-strategy, qualification
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## YouTube campaign configuration: Demand Gen, Shorts only, maximise conversions
Use when: Launching a YouTube prospecting campaign and choosing channels, devices, bidding and budget.
- Use Demand Gen as the campaign type (Google deprecated Video Action campaigns in March 2025); objective Sales, goal Conversions.
- In channels, select only YouTube Shorts — exclude in-stream, in-feed, Discover, Gmail and Display when running a Shorts-only play.
- Exclude TVs, and generally exclude tablets; the source often (not always) excludes desktop to keep Shorts on mobile.
- Turn OFF optimized targeting for a new campaign with a new audience; start narrow then expand. Test turning optimized targeting on later if you want the algorithm to expand.
- Bid strategy: start on Maximize Conversions with a daily budget so Google can spend and learn; the source warns a Target CPA set with no data can suffocate spend and the campaign never takes off.
- Expect choppy performance in the learning period (roughly pronounced for about two weeks) even if the setup is correct.
- After about two weeks, wait for a consistent CPA pattern across a three-to-five-day window, then switch to Target CPA set at or slightly below current CPA (the source gives a $40 CPA → $35–$36 TCPA example when pushing efficiency early).
- Budget rule of thumb: aim for about three times AOV as daily budget (e.g. $60 AOV → $180/day).
Caveat: The source says allowing a higher TCPA lets more learning happen and optimises faster, but efficiency suffers short-term.
Caveat: The Video Action deprecation and Demand Gen interface details are the source's account and may change — verify the current Google Ads interface.

Tags: google-ads, youtube-ads, demand-gen, campaign-setup, bidding, budgeting, shorts
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Start narrow and expand horizontally on YouTube targeting
Use when: Building audience targeting for a new YouTube or Demand Gen prospecting campaign.
- Treat YouTube differently from Meta: on Meta the creative is the targeting and the algorithm widens delivery itself; the source has not seen that behaviour on YouTube — on YouTube your targeting is actually the targeting.
- Start with a narrow audience for your ICP, because most brands want efficiency early and niche products need their specific audience; you can always expand horizontally later.
- Do not start broad and narrow later — the source says this constricts the algorithm and your success.
- For each product vertical or customer avatar, apply the same top two-to-three proven Meta creatives across three separate ad groups.
- Build three audiences: (1) a custom segment from search-intent keywords (e.g. 'no lace trainers for women', 'hands-free shoes'), (2) a custom segment from website/competitor sites your ICP visits pre-purchase, and (3) a lookalike audience seeded from first-party data.
- Exclude your all-time customer list in every ad group so Google cannot harvest existing buyers and take credit for repeat purchases.
- Add demographic refinement (e.g. females 25–44) to each audience when you know the avatar; the source sees this outperform broad demographics unless your product has truly broad appeal.
Caveat: The presenter's own experience: in-market and affinity segments have never worked — 'they don't work in our experience' — but acknowledges this may change if YouTube follows Meta toward broad targeting.
Caveat: Seed lookalikes from converters rather than all website visitors; most visitors won't convert.

Tags: google-ads, youtube-ads, audience-targeting, custom-segments, lookalike-audiences, customer-research, exclusions
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## YouTube Shorts creative specs and storytelling structure
Use when: Producing video creative for a YouTube Shorts or Demand Gen prospecting campaign.
- Use 20–60 second videos; longer is trending, with storytelling, social proof and expert endorsements outperforming sub-20-second content — but do not exceed 60 seconds.
- Shoot 9:16 vertical for mobile-first; include subtitles because a large share watch without sound.
- Confirm proof of concept on Meta (or TikTok) first — you should be moving winning creative across, not testing creative on YouTube.
- Open with movement or curiosity: the source's Kizik example opens with someone rushing and falling while stepping into a shoe within the first one or two seconds — a scroll-stopping hook that also frames problem→solution.
- Demonstrate the product visually — your USP must be showable; the source says if the product isn't visually demonstrable, YouTube isn't for you.
- Around 60–70% in, consider stitching quick cuts of additional UGC creators' social proof alongside the main creator's narrative.
- Close with a strong CTA backed by a real offer and urgency whenever possible.
- In Google, you can add up to 20 images, a logo, up to five headlines and five descriptions; the source generally writes only a couple of offer-centric headlines and uses descriptions for objection handling and trust signals.
- Test adaptive layouts with caution: results have been mixed and you may see unusual placements and asset deliveries when on.
Caveat: The source has no strong opinion on adaptive layouts — mixed results only.
Caveat: Headline/description counts and layout options are from the source's session; verify current Google Ads limits.

Tags: google-ads, youtube-ads, creative-strategy, shorts, video-ads, product-demonstration, user-content
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## YouTube retargeting campaign with low-level spend
Use when: Adding a retargeting layer to a YouTube prospecting campaign for website visitors or cart abandoners.
- Create a campaign without guidance, select Video as the campaign type and Video views as the subtype — there is no fixed objective in this build.
- Pick your retargeting audience: e.g. website visitors from the last 3 or 7 days, product viewers, or add-to-cart users.
- Choose the format based on what works on Meta: skippable in-stream for longer horizontal storytelling full of social proof and offer urgency; Shorts for UGC retargeting.
- Note that many Meta advertisers retarget with static creative because it's cheaper — this is an acceptable area for small YouTube tests.
- For skippable in-stream, set keywords, topics and placements, but exclude the YouTube homepage, anything beyond YouTube (display network placements) and mobile apps/gaming apps to avoid low-quality placements.
- Bid target cost per view, generally in the £/$0.10–$0.30 region — but expect a narrower audience (e.g. add-to-cart) to be more expensive per view than a broad website-visitor list, so let CPV breathe.
- Err on the higher side initially and refine down once it has learned.
Caveat: The $0.10–$0.30 CPV range varies widely by niche and by how much cold traffic costs you; it's a starting region, not a target.
Caveat: Some advertisers do not run any YouTube retargeting and let Meta handle it — the source allows for this but recommends a small layer if cold YouTube spend is large.

Tags: google-ads, youtube-ads, retargeting, campaign-setup, bidding, placements, exclusions
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Three things YouTube-winning brands do
Use when: Auditing whether your store is ready for YouTube ads and reviewing your playbook priorities.
- Prove creative on Meta first: everything is tested there and moved to YouTube only once it's known to work — never test creative on YouTube.
- Layer YouTube on top of an already functional Shopping and Search bedrock; brand search, Shopping and prospecting campaigns should all be dialled in first.
- Know your target audience deeply — what they search for, what sites they visit, what their pre-purchase behaviour is — because that determines how effective your custom segments are and how quickly the algorithm learns.
- Track lead indicators during early launch when purchases may take a week or two to appear: view rate and placement watched, video played-to quartiles (25/50/75/100%), CTR, CPM, cost per view, impression frequency per user and average watch time per user.
- Also fix lag indicators — landing page arrivals, add-to-carts and purchases — because the source warns many accounts have broken conversion tracking and are reporting fabricated success.
Caveat: The $50m revenue and $2.4m-per-quarter figures are the agency's own reported results, not guarantees.
Caveat: Referencing the presenter's stated four-year experience and agency work; treat as practitioner opinion.

Tags: google-ads, youtube-ads, measurement, analytics, campaign-strategy, creative-strategy, conversion-tracking
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Demand Gen image ad anatomy for remarketing
Use when: Building or reviewing the asset group for a Demand Gen remarketing campaign.
- Name the ad and provide the final URL that clicks should land on.
- Upload up to 20 images and add your logo; adaptive layouts from Google lets it fit more layout styles and aspect ratios by manipulating your assets.
- Expect placements across YouTube, the Discover feed and Gmail when using Demand Gen.
- Use up to five headlines and five descriptions, but the source usually writes only a couple of headlines when they are very offer-centric — you know what message you want served.
- Write the headline around the offer (e.g. urgency) and use the description to close the deal with objection handling or trust signals.
- Remember the audience already failed to buy once — the ad's job is to address the specific reason they did not convert.
- Take care with adaptive layouts: the source reports mixed results and unusual placements/deliveries when enabled — be prepared if you turn it on.
Caveat: Field limits (20 images, 5 headlines, 5 descriptions) and layout behaviour are as described in the source's session; verify against the current Google Ads interface.

Tags: google-ads, demand-gen, retargeting, ad-assets, creative-strategy, product-page
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Turn remarketing objection-learning into funnel-wide improvements
Use when: Iterating on creative across a Google Ads account and trying to raise on-site conversion rate and ROAS.
- Build a large-enough cart-abandoner list so you can test multiple objection angles quickly against one performance measure.
- Run single-image and other simple ad variants, each hammering one objection (urgency for complacency, price justification, trust/social proof, efficacy proof, logistics clarity).
- Read the results: if trust/social proof wins with abandoners, you now know that group is holding back on credibility.
- Push the winning signal up-funnel: add more social proof or trust signals to prospecting and higher-funnel ad creative so people don't reach the cart unconvinced.
- Expect the payoff to show up as a higher site conversion rate and more positive feedback, which the source argues makes things more economically sensible and the account easier to scale.
- Keep the remarketing creative specific to the abandonment stage rather than copying cold prospecting creative — the source criticises treating remarketing as a one-and-done with the same cold static assets.
Caveat: This is the presenter's reasoning and observed pattern, not a measured causal result they document.
Caveat: Requires a large enough remarketing list to test multiple objections effectively.

Tags: google-ads, retargeting, creative-strategy, conversion-optimization, objection-handling, funnel-optimization
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Reconcile Google remarketing with your Meta team
Use when: Coordinating paid social and paid search teams on retargeting creative and messaging.
- Share what creative is working on Meta with whoever runs Google remarketing, and vice versa, so the same winning angles are used on both platforms.
- If your Meta team already has strong retargeting creative (often static for cost reasons), consider reusing those assets on YouTube Shorts or in-stream rather than building from scratch.
- Run a full-funnel remarketing view across Google and Meta so prospects see consistent objection-handling wherever they re-encounter the brand.
- Align on which objection each platform's retargeting is handling (e.g. Meta leans on cheap static social proof, Google leans on Shorts UGC) so the two layers complement rather than duplicate.
- The source argues this coordination is the route to higher conversion rates across paid channels and more profitable scaling; the source explicitly frames it as their own observation.
Caveat: No quantified benchmark is provided for the lift from coordination; treat as a qualitative recommendation.
Caveat: Assumes you have both a Meta and Google presence with enough creative volume to share.

Tags: google-ads, meta-ads, retargeting, cross-channel, creative-strategy, scaling
Source: Ecommerce Google Ads 2026 Free Course.docx

---

## Launch order for an ecommerce Google Ads account
Use when: Planning which campaign types to launch first for a new or restructured ecommerce Google Ads account.
- Start with Search and Shopping (bottom/mid funnel) so the account begins driving new customers and branded data immediately.
- After the account has roughly 4–6 weeks of data (source's guideline, not strict — depends on budget, product, and sale volume; can be sooner at high spend), add step two: direct remarketing via video and display campaigns to users who visited, added to cart, or began checkout without purchasing.
- Only introduce Demand Gen (step three) once bottom and mid-funnel are largely saturated, because top-of-funnel conversions cost more and bottom-funnel traffic converts cheaper and higher quality.
- Exception the source allows: if you already run proven creatives on Meta and are a large account, you may port them into Demand Gen earlier for profitable cold acquisition.
- For video cold traffic, use Demand Gen with video-only assets, since the older video campaign type is being sunset by Google (verify current interface).
Caveat: The 4–6 week figure is a general guideline, explicitly variable by budget and sales volume.

Tags: google-ads, account-structure, acquisition, full-funnel, campaign-launch, demand-gen, remarketing
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Separate branded vs non-branded campaigns
Use when: Structuring new Search or Shopping campaigns, or diagnosing muddled attribution and inflated metrics in an ecommerce account.
- Define branded search as any query containing your brand name with inherent brand intent (e.g., 'Peter's Pans'); non-branded as generic product terms (e.g., 'non-stick fry pan').
- Split every campaign into a branded stream and a non-branded stream rather than combining them.
- Add your brand terms as exact-match negative keywords in every non-branded campaign so branded searches cannot leak in and distort attribution.
- Expect your scaling to come from non-branded campaigns; branded campaigns exist mainly to capture existing demand cheaply and feed the algorithm data.
- In the account, keep budget allocated so branded campaigns do not accidentally absorb spend meant for non-branded growth.
Caveat: Source holds the opinion that branded campaigns are 'absolutely necessary' and high-performing accounts always have one; he concedes some accounts benefit less. Treat this as his view; nothing in Google Ads is black-and-white.

Tags: google-ads, account-structure, branded-search, negative-keywords, attribution, measurement
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Bid strategy progression: clicks first, then conversions
Use when: Setting or reviewing bid strategy on a new ecommerce Google Ads account or one with too few conversions for smart bidding.
- Launch with Maximize Clicks so Google can win cheap clicks while the account has no conversion history.
- Keep click-focused bidding until you have accumulated conversions; the source cites roughly 15–30 conversions per month as the threshold to consider moving to Maximize Conversion Value or Target ROAS, and mentions 10–15 conversions as an earlier consideration point.
- Rationale: asking a conversion-based strategy to find conversions in an account that has never recorded one is like blindfolding an archer — Google does not know what to aim at.
- Once conversions exist, switch the campaign to Maximize Conversion Value or Target ROAS to let smart bidding optimize toward revenue.
- Aggregate conversion volume across the account when judging readiness, since the threshold is about signal volume, not any single campaign.
Caveat: The 10–15 and 15–30 conversion figures are source-specific heuristics, not a documented calculation; treat as rough guides.

Tags: google-ads, bidding, measurement, account-structure, conversion-data
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Use branded campaigns as cheap algorithm training data
Use when: Deciding whether to bid on your own brand terms in ecommerce Google Ads.
- Accept that branded bidders would have converted anyway, and value the campaign for data instead: branded conversions are the cheapest source of high-quality traffic and signal.
- Let branded conversion data flow into the account so machine learning improves on more expensive new-customer non-branded efforts.
- Cap spend realistically — for smaller brands the source suggests roughly $10–$20/day, larger brands up to about $50/day, rare to exceed $50/day in the US.
- If you fully spend the daily budget, check search terms under insights and reports; if traffic matches your brand intent, raise the budget until captured.
- Set customer acquisition (new-customer) targeting off in branded campaigns; returning existing customers are fine there.
Caveat: Google will not spend your full branded budget if there is not enough branded search volume — a low delivery is normal for small brands.

Tags: google-ads, branded-search, bidding, budgeting, account-structure, machine-learning
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Turn off Search Partners and Display Network for Search campaigns
Use when: Configuring settings for a new ecommerce Search campaign, before launch.
- Leave the Google Search Partners Network unchecked: it adds reach but typically brings lower-quality traffic, fewer conversions, and higher cost per conversion.
- Leave the Google Display Network unchecked too: if you want display placements, create a separate Display campaign.
- Note both boxes are checked by default, so actively untick them each time you build a Search campaign.
- Only reconsider search partners if you have absolutely exhausted everything available on Google proper — the source calls this a very rare scenario.
Caveat: This is the source's default practice; he allows exceptions for saturated accounts but treats them as unusual.

Tags: google-ads, search-campaigns, campaign-settings, traffic-quality, conversion-optimization
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Set location targeting to presence, not presence-or-interest
Use when: Configuring geographic targeting on any ecommerce Google Ads campaign, especially when selling only to specific countries.
- In campaign settings, enter the target location and narrow it as far as needed (country, state, city, postcode).
- Open the location options dropdown and select 'presence' rather than 'presence or interest'.
- Reason: presence-or-interest can serve ads to people outside your target country who are merely interested in it (e.g., someone abroad searching about it), wasting spend.
- Optionally exclude regions you do not want to serve.
- Combine with a language setting that matches your store, typically English unless you sell in other languages.
- Leave audience segments off unless you have a specific demographic to target, and keep broad match keywords off for these campaigns.

Tags: google-ads, campaign-setup, location-targeting, ecommerce
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Ignore Google's AI keyword and asset generation
Use when: Building new Search campaigns and facing Google's prompted tools or recommendations.
- On the keyword and asset generation screen, do not use the suggested AI keywords or headlines.
- Apply the same skepticism throughout setup to any automated creation or automated change suggestions.
- Rationale: Google will try to make as much money as they can, not necessarily as much for you, and knows your brand and customers less well than you do.
- Add your own keywords manually with the intended match types instead.
- Same logic applies to ad copy: the source says Google will tell you not to pin headlines; he disagrees and says pin when it improves relevance.
Caveat: This is the source's strong opinion; other practitioners do use automated suggestions. Treat as a default stance, not a universal rule.

Tags: google-ads, campaign-settings, automation, keyword-research, search-campaigns
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Step 2: add remarketing to re-engage non-converting visitors
Use when: After initial Search/Shopping campaigns are running and you want to recover near-converting traffic in an ecommerce store.
- Build audience lists from site behavior: visited, added to cart, began checkout, and prior purchasers for repeat purchase.
- Run video remarketing campaigns for these audiences; the source finds video most effective when creatives are high quality because they are more engaging.
- Alternatively or additionally run display remarketing campaigns to re-approach non-purchasers and past buyers.
- Add these campaigns only after roughly 4–6 weeks of account data (source's guideline, variable by budget and sales volume).
- Expect these to lift both conversion rate and customer LTV by adding repeated touchpoints.
- Keep the goal to push users over the edge toward purchase and to re-trigger past customers, not to retarget broadly.
Caveat: The 4–6 week timing is a general guideline, not strict.

Tags: google-ads, remarketing, retention, video-ads, display-ads, ltv, audiences
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Use Performance Max correctly, or use feed-only PMax as a feed-led alternative
Use when: Evaluating a feed-led versus full-asset Performance Max campaign for an ecommerce product catalog.
- Confirm Merchant Center linkage, eligible products, accurate prices and stock, and tested purchase-value tracking.
- Treat the source feed-only approach as a test of reduced manually supplied creative. Review the actual asset-generation and URL-expansion settings in the current interface.
- Monitor channel delivery, product performance and new versus returning customer outcomes; compare contribution and acquisition cost with the existing Shopping or full-asset setup.
- Do not classify the campaign as remarketing-only or promise Shopping-only delivery. Use a campaign with appropriate audience controls when strict remarketing is required.
Caveat: Editorial correction: PMax audience signals do not impose strict targeting; omitting manual creative does not guarantee placement isolation. https://support.google.com/google-ads/answer/14530785
Caveat: Merchant Center data can generate assets automatically. Source examples of efficient feed-led campaigns are not delivery guarantees. https://support.google.com/google-ads/answer/15865151

Tags: google-ads, performance-max, remarketing, feed-management, merchant-center, account-structure
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Introduce Demand Gen last, for top-of-funnel cold traffic
Use when: Deciding when and how to run cold top-of-funnel Google Ads for an ecommerce brand.
- Target people who may not know the product, the problem, or your brand — e.g., a kitchen-cookware ad asking 'Are you sick of food sticking to your pans?' then showing a high-quality creative.
- Choose between video-only Demand Gen (YouTube ads via video assets, kept in the preferred/future-proof campaign type since old video campaigns are being sunset) and all-assets Demand Gen (serves across YouTube, display, search, and more).
- Start with video-focused setups: the source notes all-assets campaigns typically yield lower efficiency on video.
- Delay launch until bottom-of-funnel and mid-funnel campaigns are largely saturated, because top-of-funnel conversions cost more.
- Run it as a standalone full-funnel layer independent of other channels once proven; if you already have proven Meta creatives and a large account, port them here earlier for profitable acquisition.
Caveat: Efficiency/cost expectations are the source's guidance, not measured benchmarks; the video campaign sunset timing is forecast and should be verified.

Tags: google-ads, demand-gen, acquisition, creative-strategy, full-funnel, video-ads
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Link Shopify and Merchant Center, then Merchant Center to Google Ads
Use when: Preparing an ecommerce store to run Shopping or feed-based Google Ads for the first time.
- In Shopify, go to Sales channels → Google and YouTube and link your Google account and Merchant Center to Shopify, then link products.
- If you have no Merchant Center, create one (merchants.google.com) and connect it to Shopify via that tab; allow a couple of hours for the link and product import.
- In Google Ads, go to Tools → Data manager → connected products and connect Google Merchant Center if not already shown.
- Verify your imported products appear on the Merchant Center products page before building campaigns.
- If you are not on Shopify, use an equivalent linking solution for your platform (source notes most stores are Shopify but other tools exist).
Caveat: Interface paths are as described at the time of recording; Google changes navigation, so verify current menus.

Tags: google-ads, merchant-center, shopify, feed-management, shopping-campaigns, integration
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Feed product titles with informative keywords
Use when: Optimizing Merchant Center product data before running Shopping campaigns.
- Put the highly necessary product details first in the title, then attributes, then the brand name at the end.
- Example structure: 'Black Non-Stick Frying Pan 38cm Diameter, Peter's Pans'.
- Include keywords that reflect what shoppers actually search, so Google can target the product ad to the right queries.
- Fill every available field (title, description, product type, category, price, sale price, GTIN, etc.) with high-quality information.
- If you have a GTIN, include it; if not, do not worry and still complete the rest.
- Do not agonize over perfection at this stage — get a correct, informative setup live first; deep optimization is a separate, longer effort.
Caveat: Title keyword strategy must not include terms your product is not (see incorrect-attribute warning card).

Tags: google-ads, merchant-center, feed-optimization, product-page, shopping-campaigns
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Product descriptions: use AI for keyword-rich copy, but never wrong attributes
Use when: Filling Merchant Center product description fields across a catalog without hand-writing every one.
- Use a detailed prompt, e.g., 'Write a 2,000-character product description for a black 38cm non-stick frying pan, including keywords a shopper might Google to trigger a Shopping ad.'
- Treat the description as a keyword surface for Google's matching, not as marketing copy that must be hand-written.
- Only include keywords for products and searches you actually want to appear for.
- Exclude incorrect attributes: if a pan is not aluminum, do not write 'aluminum pan', or Google may serve it to aluminum or stainless steel pan searches and waste clicks.
- Review generated descriptions before saving to catch any fabricated attributes.
- Save your changes or the work is lost.
Caveat: Wrong attribute terms cause Google to show the product to irrelevant searches, so cheap AI generation must still be checked.

Tags: google-ads, merchant-center, feed-optimization, product-page, ai-tools, shopping-campaigns
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Use feed management tools for large catalogs
Use when: Working with a large SKU count and standard Shopify–Merchant Center sync is too slow or limited.
- Recognize that manually filling every field does not scale for large catalogs.
- Use a Shopify feed management plugin (the source names Srois, a Shopify plugin) to manage feeds more thoroughly than the automatic Google–Shopify integration.
- Apply it to bulk-edit titles, descriptions, and attributes across many products.
- If you have only a few products, skip this and hand-fill the fields — simpler and faster.
- After any bulk changes, verify in Merchant Center that products imported and are eligible to serve.
Caveat: The source explicitly does not go deep into optimization and promises a future guide; treat this as a starting point. Tool names and plugins change — verify availability.

Tags: google-ads, merchant-center, feed-management, shopify, scaling, shopping-campaigns
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Configure Shopping campaign objective and conversions
Use when: Creating a Shopping campaign for an ecommerce store and choosing conversion goals.
- In Campaigns, create a new campaign and choose the Sales objective (the source says this is the case ~99% of the time for ecommerce).
- Set the account goal to purchases only; remove add to cart and begin checkout as conversion goals for this campaign.
- Rationale: if Google can optimize to 'easy' micro-conversions, it may chase add-to-carts and never deliver purchases.
- Ensure purchase conversion tracking is correctly installed before launch — bad tracking feeds poor data and undermines results.
- Use a consistent campaign naming structure (campaign type → geography → focus, e.g., 'Shopping / USA / Non-Brand') so accounts are easy to review and audit.
Caveat: Source treats purchases-only as the right default for ecommerce; it does not deny that add-to-cart and begin-checkout can be useful elsewhere in the account.

Tags: google-ads, shopping-campaigns, conversion-tracking, campaign-settings, measurement
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Use Search for category/collection intent, Shopping for specific products
Use when: Deciding whether a keyword should be covered by a Search campaign or left to Shopping listings in an ecommerce account.
- For non-branded Search, target category/collection intent (e.g., 'non-stick pans') where the shopper wants to compare a range rather than one exact product.
- Send those clicks to the matching collection page (e.g., /nonstickpans), not a single product page.
- Use phrase match for these category keywords; phrase match can get broad, so monitor and add negatives.
- Keep ad groups to one collection/category each — never mix two collections in one ad group, or Google may show a crockpot searcher a non-stick pan ad.
- Use Shopping for the 'sniper' approach — when someone searches a specific product spec, the exact product listing shows with image, price, and shipping.
- Only run category Search campaigns when a category is genuinely popular and data supports testing it; they are not essential in most ecommerce accounts.
Caveat: Source states Search campaigns are not a big priority in ecommerce and he uses them infrequently; Shopping is the main driver.

Tags: google-ads, search-campaigns, shopping-campaigns, keyword-research, product-page, merchandising
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Write branded vs non-branded Search ad copy
Use when: Writing RSA headlines and assets for branded or non-branded ecommerce Search campaigns.
- Branded ads: always include the brand name in a headline and pin it to position 1 so searchers instantly recognize your brand and click through.
- Add a trust/social-proof headline (e.g., 'Ultimate Quality and Reliability') and an offer/CTA headline (e.g., a specific sale).
- Non-branded category ads: the brand name is optional; instead lead with selection and reassurance, e.g., 'Huge Range of Non-Stick Pans' or a guarantee like '100% Guaranteed Not to Stick'.
- For branded campaigns, set customer acquisition (new-customer) targeting off — returning customers are acceptable and desirable there.
- Use only 3–5 headlines rather than filling all 15 so you can actually split test; too many headlines make testing impossible.
- Pin headlines when it improves relevance, even though Google advises against pinning.
Caveat: Source's anti-pinning position is a strong opinion that contradicts Google's recommendation; treat as a situational choice.

Tags: google-ads, search-campaigns, ad-copy, creative-strategy, branded-search, testing
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Fill out ad extensions to expand ad real estate
Use when: Building Search ad assets for an ecommerce campaign and trying to maximize click-through rate.
- Add sitelinks to relevant but not immediately-matching pages (bestselling product, a why-non-stick blog post, etc.) so interested users can self-route.
- Add callouts and structured snippets for trust and to build out the ad's footprint on the search page.
- Test promotions and price assets; the source says they are useful but not strictly necessary.
- Skip calls and messages — not relevant for ecommerce brands.
- Complete advertiser verification to enable business name and logo on ads; source calls this worth the hassle because it raises trust, especially against competitors in non-branded auctions.
- Write these once with care — they can be reused across nearly every campaign, so quality copy pays off long-term.
Caveat: Bigger ads correlate with higher click chance per the source; asset types and availability change, so verify what your account supports.

Tags: google-ads, ad-extensions, click-through-rate, search-campaigns, trust-signals
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Set branded and category Search budgets
Use when: Allocating daily budget to branded vs category Search campaigns for an ecommerce store.
- For branded campaigns, budget roughly $10–$20/day for smaller brands, up to about $50/day for larger brands; it is rare to exceed $50/day in the US.
- Expect Google not to spend the full budget if branded search volume is low — a partial spend is normal.
- For category Search campaigns, start around $20–$30/day to test, adjusting for AOV (higher AOV needs more budget to generate purchase volume) and total account budget.
- If branded campaigns fully spend their budget, check search terms under insights and reports; if terms are aligned, increase budget until you capture the traffic.
- Scale non-branded/category spend only when the data tells you it is warranted.
Caveat: Figures are the source's rules of thumb, not benchmarks; actual spend depends on AOV, volume, and account size.

Tags: google-ads, budgeting, branded-search, search-campaigns, scaling
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Use negative keywords to protect non-branded campaigns
Use when: Building or auditing non-branded Search or Shopping campaigns in an ecommerce account.
- Go to the ad group or campaign keywords area and open the negative keywords section.
- Add every branded term you target in your branded campaign — brand name, misspellings, no-space variants — as negatives in the non-branded campaign.
- Example: if a shopper searches 'Peter's Pans non-stick frying pan', without the negative they could land in the non-branded ad group and distort attribution.
- Use a shared negative keyword list so the same brand terms can be applied across all non-branded campaigns.
- Beyond brand terms, monitor phrase-match traffic and add negatives for irrelevant queries as they appear.
- Re-check search terms regularly since broad phrase match drifts over time.

Tags: google-ads, campaign-setup, negative-keywords, ecommerce
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Test category Search campaigns cautiously
Use when: Evaluating whether to add non-branded category Search campaigns alongside Shopping.
- Default to letting Shopping carry non-branded product demand; only test category Search when one category gets heavy traffic and users likely to buy.
- Keep ad groups tightly themed to a single category or collection.
- Use 3–5 phrase-match keywords per category ad group, maximum 10 — three well-chosen phrases often capture the traffic.
- Point ads to the matching collection page for a seamless journey from query to page.
- Start at roughly $20–$30/day for the test and scale only if data supports a profitable ROI.
- Drop or pause the campaign if data does not show profitable demand.
Caveat: Source is candid that he does not use category Search campaigns frequently and considers them non-essential in most ecommerce accounts.

Tags: google-ads, search-campaigns, keyword-research, testing, budgeting, product-page
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Set up a first Standard Shopping campaign for bestsellers only
Use when: You are creating your first Google Shopping campaign and deciding which products to advertise.
- In Google Ads go to Campaigns > plus > Create, choose the Sales objective, and set conversion goals to purchases only (remove add-to-cart and begin-checkout as primary goals so Google doesn't chase the cheaper action). Verify the current interface before relying on exact menu paths.
- Choose Shopping as the campaign type and select your linked Merchant Center account/feed; if multiple feeds exist, pick the correct one.
- When Google pre-selects Performance Max, switch to Standard Shopping. The source advises avoiding PMAX when the account has no conversion data because it is likely to lose money without data.
- Name the campaign consistently (e.g. 'Shopping | USA | Bestsellers | Max Clicks') so the products, geo and bid strategy are obvious.
- Pick 5-10 known or predicted bestsellers (under 10 is the source's recommendation). Small catalogs in one campaign get attention spread thin if the budget is limited, and Google may latch onto weak products at mediocre ROAS.
Caveat: Source-specific heuristic: 5-10 products, under 10. Not a benchmark.
Caveat: Menu labels and defaults change; verify in the current UI.

Tags: google-ads, shopping-campaigns, product-selection, campaign-setup, bestsellers, performance-max
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Restrict a Shopping ad group to specific products by item ID
Use when: Your new Shopping ad group is showing all products and you want it to contain only bestsellers.
- Open Campaigns > Ad groups, select the campaign and ad group, then open the Product groups tab.
- All products is enabled by default; click the plus to Add subdivision. Prefer subdividing by Item ID when the feed is not cleanly categorized.
- Search each bestseller by name, select it, and repeat until all chosen products are listed, then Continue to edit bids and Save (do not change bid values on that screen).
- The group now shows your selected products separately plus an 'everything else / all products' row.
- Click the green status dot on the all-products row and change it to Exclude, leaving only the selected bestsellers enabled.
Caveat: Excluding everything else means only the listed products can serve; re-check the list when you add or retire products.
Caveat: Category subdivision only works if the Merchant Center feed is consistently categorized.

Tags: google-ads, shopping-campaigns, product-feed, merchandising, campaign-structure
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Choose a Shopping bid strategy based on account conversion data
Use when: You are setting the bidding strategy for a Shopping campaign and need to decide between clicks and conversion-based bidding.
- With no conversion data in the account, select Maximize Clicks. The source states conversion-based bidding on a data-less account tends to perform poorly.
- Once roughly 15+ conversions exist, consider switching to Maximize Conversion Value.
- At roughly 30+ conversions per month with a consistent ROAS (source example: hovering around 2.5), consider adding a Target ROAS so Google holds performance near the level you were already achieving.
- Optional: set a Maximum CPC bid limit only after you know your average CPC from performance columns, to clip outlier bids far above normal (source example: seeing $5 bids when average CPC is $1.20).
Caveat: 15 and 30 conversions plus the 2.5 ROAS figure are source-specific heuristics, not established thresholds.
Caveat: A Max CPC cap set too tight can suppress delivery.

Tags: google-ads, bidding-strategy, shopping-campaigns, measurement, roas, maximize-conversion-value
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Configure Shopping targeting: presence only, no search partners
Use when: You are finalizing locations, networks and devices on a Shopping campaign.
- Uncheck the automatically-enabled Search Network option unless you have already fully saturated the Google network (source says leave it off by default).
- Set devices to All Devices for most scenarios.
- Select the target location (e.g. United States), then open Location options and choose Presence, not Presence or interest. Presence-or-interest can show ads to people outside the country who merely show interest in it.
- Leave start and end dates as the creation date unless you have a specific flight.
Caveat: Google may still optimize device delivery toward the best-performing devices.
Caveat: Presence-vs-interest option is absent on some campaign types.

Tags: google-ads, shopping-campaigns, geo-targeting, campaign-settings, audience-targeting
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Exclude branded searches from a non-branded Shopping campaign
Use when: You run a Shopping campaign intended for new-customer, non-brand acquisition and want branded traffic excluded.
- Go to Campaigns > Audiences, keywords and content > Search keywords, and select the Shopping campaign.
- Under Negative search keywords, click plus to add negatives.
- Enter all brand-name variations (e.g. 'Peter's Pans', 'Peter's Pans frying pans') as exact match using square brackets so you exclude only those queries and not adjacent traffic.
- Keep the campaign's targeting non-branded; branded traffic should be handled in a separate branded campaign.
Caveat: Overly broad negatives can strip useful non-brand queries; exact match limits the blast radius.
Caveat: Source attributes the branded/non-branded separation rationale to its overview module; the concept is that branded and prospecting traffic perform differently and should be measured separately.

Tags: google-ads, shopping-campaigns, negative-keywords, branded-traffic, acquisition, campaign-structure
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Sequence a second all-products Shopping campaign after bestsellers prove out
Use when: Your bestsellers Shopping campaign is producing consistent sales and you want to prospect for additional high-performing products.
- Confirm the bestsellers campaign has steady, consistent sales and a stable, profitable ROAS first.
- Create a second Shopping campaign using the same setup but skip the product-group subdivision so all products remain enabled.
- Run this all-products campaign as a discovery channel to identify more potential bestsellers.
- Feed any discovered winners back into the bestsellers campaign structure and remove losers.
Caveat: Source says to only do this after bestsellers are working, not at launch.
Caveat: An all-products campaign can also be run as PMAX, but the source sticks to Shopping for this step.

Tags: google-ads, shopping-campaigns, product-selection, scaling, campaign-structure
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Prune underperforming products from a bestsellers campaign
Use when: A bestsellers Shopping campaign is live and some products are dragging down overall ROAS.
- Review product-level performance to find items with substantial ad spend and clicks but weak or unprofitable returns.
- Exclude those products from the bestsellers ad group using the product group exclusion flow.
- Keep the bestsellers campaign reserved only for products that justify inclusion.
Caveat: The source does not give a numeric spend or click threshold; use judgement and enough data before cutting.
Caveat: Removing a product entirely stops it serving; it can be re-added or moved to the all-products campaign.

Tags: google-ads, shopping-campaigns, optimization, roas, product-selection
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Add a low-budget branded Shopping campaign to capture branded product searches
Use when: You have meaningful branded search volume (from ads, organic or other channels) and are not fully capturing it with search campaigns.
- Set up a Shopping campaign with the same process as your standard campaign but leave all products enabled and exclude nothing.
- Use a small budget sized to cover branded traffic only (source example: around $20/day).
- Implement a branded Shopping script (source credits 'PBC masterminds' and provides a link) via Tools > Bulk actions > Scripts, copy the script and make the required modifications.
- Verify the current script and its instructions before use, since third-party scripts and the interface change.
Caveat: Only needed if you have substantial branded traffic; branded shopping campaigns are optional.
Caveat: Source says you can also do this even if you simply want your products to appear on brand searches.

Tags: google-ads, shopping-campaigns, branded-traffic, scripts, budgeting, campaign-setup
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Check audience lists and tagging before any remarketing campaign
Use when: You plan to run any display, video or PMAX remarketing campaign and need working audience data first.
- Open Tools > Shared library > Audience manager to see which audiences the account is tracking (some auto-created, some from other sources).
- Prioritize the automatic setup: the Google Ads tag, GA4 linked through the data manager, and the Shopify link, which the source calls the easiest and most reliable for most stores.
- Consider a customer match import plugin (source names 'Simprosys Custom Match list') to upload Shopify customers into Google Ads and feed purchase-converter data; the source describes it as cheap and optional, not required.
- Wait until lists have accumulated enough users before launching remarketing; too-small lists make targeting ineffective.
Caveat: Source does not specify a minimum list size, only that small lists won't allow effective targeting.
Caveat: Plugin names and setup flows change; verify before implementing.

Tags: google-ads, audience-targeting, remarketing, tagging, customer-match, shopify
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Set up a Display remarketing campaign for returning visitors
Use when: You have re-engagement audiences populated and want to retarget past site visitors with Display image ads.
- Create a new campaign with Sales objective and purchases-only conversion goals, choose Display, and enter the landing page. Send users to a page designed for prior visitors (offer or deal page) if you have one; otherwise the base or relevant collection page.
- Set geo with Presence only, leave most settings at defaults, and start budget low, around $10-15/day. The source warns that high Display budgets can push low-quality placements.
- Use conversion-value bidding (Maximize Conversion Value), since remarketing is introduced when the account already has data. Target ROAS can be added later; if enabled early, set a very low target so it doesn't restrict delivery.
- In targeting, choose audience segments from your data: Browse > How they've interacted with your business > website visitors, e.g. all users.
- Uncheck Optimized Targeting, which is on by default. It expands delivery beyond your remarketing list, which defeats the purpose. The source says it has not performed well for this use.
- Build the ad with at least the required landscape and square images; the source considers images more important than headlines/descriptions here. Creative should assume the viewer already knows the brand, e.g. a code offer like 'PETER30 for 30% off' rather than an introduction.
Caveat: Source opinion: avoid optimized targeting on remarketing; stated as the presenter's experience, not a universal rule.
Caveat: Budget figures are source examples, not benchmarks.

Tags: google-ads, remarketing, display-campaigns, audience-targeting, conversion-optimization, creative-strategy, budgeting
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Run Video remarketing for site visitors with a product feed attached
Use when: You want a more efficient remarketing channel than Display and are ready to retarget site visitors via YouTube.
- Create a campaign with Sales objective, purchases goal, and Video type. Note the source says Video campaigns were being upgraded to Demand Gen in early 2025; verify the current campaign types.
- Use Maximize Conversions (source says Maximize Conversion Value is not available on video). Budget around $10-20/day; the source recommends roughly 10-15% of total account budget for remarketing.
- Attach a Merchant Center product feed so relevant products show clickable below the ad (e.g. a non-stick pan ad paired with a non-stick pan feed), improving relevance and clickthrough.
- Device: if running vertical YouTube Shorts only, target mobile phones; if running landscape and portrait, keep all devices and let Google optimize toward the best performers.
- Set frequency capping to about 3 impressions per day. The source argues views beyond that rarely change opinion and waste spend.
- Turn off video enhancements so Google doesn't auto-edit or crop your videos; you should know exactly what creative is running.
- In the ad group, target all users (or specific segments like product viewers/abandoners), uncheck optimized targeting, and upload your video to YouTube (public or unlisted) and paste its URL. Add a CTA, headline and description, using the preview panels to see how each asset appears.
Caveat: Source opinion: video remarketing is typically more efficient than image display remarketing; invest there first, but this is the presenter's observation.
Caveat: Frequency cap of 3/day is a source recommendation, not a proven threshold.
Caveat: Video campaign type may no longer exist; verify in the current interface.

Tags: google-ads, remarketing, video-campaigns, youtube, product-feed, audience-targeting, frequency-capping, demand-gen
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Use 2-3 high-quality ad copy assets rather than filling every field
Use when: You are building a Display or Video remarketing ad and Google offers many headline/description slots.
- Provide at least one or two headlines and descriptions, which is enough to launch and run a little testing.
- Stop there rather than filling every available slot; the source argues you end up populating the later ones with low-quality copy.
- Tailor all copy and creative to the specific remarketing segment (all visitors, cart abandoners, product viewers) so it reads as re-engagement, not a first introduction.
- If you test asset performance, use separate ads with different assets so you can compare cleanly.
Caveat: Source opinion about asset quality versus quantity; not a tested rule.
Caveat: Minimum required assets still must be supplied for the ad to run.

Tags: google-ads, remarketing, creative-strategy, ad-copy, experiment-design
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Position PMAX as a remarketing weapon alongside new-customer Shopping
Use when: You already have Shopping campaigns acquiring new customers and want a retargeting layer using PMAX.
- Keep the Shopping campaign as the new-customer funnel targeting non-branded searches (branded traffic excluded via negatives).
- Set up a PMAX campaign whose strategic purpose is to retarget those shopping customers with shopping listings and high-intent ads.
- Get the important PMAX settings right before launching; the source stresses that PMAX is very data- and algorithm-dependent and can waste money when not contained by the correct strategy.
- Treat PMAX as reliant on existing account data, consistent with the source's advice to avoid using it at the outset when there is no data.
Caveat: Source describes this PMAX-as-remarketing approach as a fairly new, specific strategy; the full PMAX settings walkthrough is in a later module, not this section.
Caveat: Source states PMAX set up wrongly wastes money, and without data is likely to lose money.

Tags: google-ads, performance-max, remarketing, shopping-campaigns, campaign-structure, acquisition
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Feed-Only Performance Max Alongside Standard Shopping
Use when: Evaluating a feed-led versus full-asset Performance Max campaign for an ecommerce product catalog.
- Confirm Merchant Center linkage, eligible products, accurate prices and stock, and tested purchase-value tracking.
- Treat the source feed-only approach as a test of reduced manually supplied creative. Review the actual asset-generation and URL-expansion settings in the current interface.
- Monitor channel delivery, product performance and new versus returning customer outcomes; compare contribution and acquisition cost with the existing Shopping or full-asset setup.
- Do not classify the campaign as remarketing-only or promise Shopping-only delivery. Use a campaign with appropriate audience controls when strict remarketing is required.
Caveat: Editorial correction: PMax audience signals do not impose strict targeting; omitting manual creative does not guarantee placement isolation. https://support.google.com/google-ads/answer/14530785
Caveat: Merchant Center data can generate assets automatically. Source examples of efficient feed-led campaigns are not delivery guarantees. https://support.google.com/google-ads/answer/15865151

Tags: google-ads, performance-max, retargeting, campaign-structure, shopping-campaigns, merchant-center, audience-signals
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Excluding Branded Traffic from PMAX to Protect Attribution
Use when: Merchandising/measurement decision when PMAX is absorbing branded searches and inflating its apparent results while muddying which campaign actually drives new customers.
- Confirm you already run a separate branded Shopping campaign (and branded Search) that captures brand demand; this is the precondition for excluding brand from PMAX.
- In the PMAX campaign, go to Audiences, keywords and content, then Search keywords, then Negative search keywords.
- Add every brand variant customers might search, in exact match: brand name, brand plus product category, common misspellings and product-specific brand phrases.
- Save them into a new shared negative keyword list named for brand exclusion so the same list can be reused across campaigns.
- Because PMAX does not allow you to attach the list directly in the UI (as described in this course), use the Google support form to request the negative keyword list be applied to the PMAX campaign. Verify the current application method before relying on it.
- Assign roles in reporting: branded Shopping and branded Search collect branded traffic only; non-branded Shopping drives new customers; PMAX catches past visitors and non-converting traffic.
- Re-audit search terms periodically to identify new brand variants to add.
Caveat: Requires an existing branded campaign structure; excluding brand without one loses brand traffic entirely.
Caveat: The support-form route for applying negatives to PMAX is the presenter's workaround at time of recording and may be outdated.

Tags: google-ads, performance-max, branded-search, attribution, negative-keywords, shopping-campaigns
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Deciding Between Feed-Only PMAX and Asset-Filled PMAX
Use when: Evaluating a feed-led versus full-asset Performance Max campaign for an ecommerce product catalog.
- Confirm Merchant Center linkage, eligible products, accurate prices and stock, and tested purchase-value tracking.
- Treat the source feed-only approach as a test of reduced manually supplied creative. Review the actual asset-generation and URL-expansion settings in the current interface.
- Monitor channel delivery, product performance and new versus returning customer outcomes; compare contribution and acquisition cost with the existing Shopping or full-asset setup.
- Do not classify the campaign as remarketing-only or promise Shopping-only delivery. Use a campaign with appropriate audience controls when strict remarketing is required.
Caveat: Editorial correction: PMax audience signals do not impose strict targeting; omitting manual creative does not guarantee placement isolation. https://support.google.com/google-ads/answer/14530785
Caveat: Merchant Center data can generate assets automatically. Source examples of efficient feed-led campaigns are not delivery guarantees. https://support.google.com/google-ads/answer/15865151

Tags: google-ads, performance-max, campaign-structure, shopping-campaigns, roas, budget-allocation
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Budgeting and Sequencing Demand Gen Campaigns
Use when: Budget and rollout planning for a store deciding when to add Demand Gen and how much daily spend to commit relative to its existing Shopping/PMAX setup.
- Decide timing by budget: with a smaller budget and no proof on other platforms, implement Demand Gen after PMAX remarketing. With a high budget, existing proof on other platforms, and rapid scaling goals, implement it alongside PMAX (source treats this as step two versus step three).
- Set the campaign as Sales objective, purchases conversion goal, Demand Gen campaign type.
- Use best-seller products as the starting product set so the campaign accumulates data quickly and can be tested and iterated fast.
- Enable the product feed with your Merchant Center account so catalog items appear alongside the video/image ads and shorten the path to purchase.
- Start with conversion-based bidding and leave target CPA unchecked; the source argues you cannot know a realistic CPA before the campaign has data, and a misaligned target slows learning. Switch to conversion value bidding only if the account already has results to support it.
- Set daily budget relative to AOV: the source's illustration is roughly $50/day at $10–20 AOV and $100+/day at around $50 AOV, and it recommends allocating about 30% of the full account budget to Demand Gen when focused on new customers (e.g. ~$150/day out of a $500/day account). Treat these as starting heuristics, not benchmarks.
- Expect to invest meaningfully: the source states these campaigns need real budget to generate conversions.
Caveat: Budget figures are the presenter's rough guidance tied to AOV and total budget, not tested benchmarks.
Caveat: Converting new customers at '2+ ROAS' on cold traffic is presented as an observed example, not a promise.

Tags: google-ads, demand-gen, budget-allocation, campaign-structure, new-customer-acquisition, merchant-center
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Demand Gen Setup: Settings, Placements and Device Controls
Use when: Technical setup of a Demand Gen campaign for a store that wants control over placement quality and format, especially when repurposing short-form social creatives.
- Set location and language at campaign level (or ad group level if you need variation). The source's example targets the US with English.
- Disable Google video partners. The source compares them to low-quality display/search network placements and says results are worse than standard Google placements.
- If you want to bias toward YouTube Shorts, narrow devices to mobile only. The source notes this increases the chance of Shorts placement but cannot guarantee it.
- Understand the format selection caveat: if you assign a video only to Shorts, Google requires at least one video showing in each format for that choice to fully apply, and the source's observation is that it may still serve the video in other formats (in-stream, in-feed).
- Turn off video enhancements so Google does not auto-edit your creatives into formats that may crop content or wording.
- Note that device narrowing plus Shorts targeting together is the best available control for Shorts-specific delivery in the source's experience.
Caveat: Format selection behavior is described as unclear in Google's documentation and the source's read is an assumption based on observed data.
Caveat: Verify current placement and enhancement settings in the live interface, as these change frequently.

Tags: google-ads, demand-gen, video-ads, youtube-shorts, placement-targeting, campaign-settings
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Structuring Demand Gen Ad Groups by Creative Theme
Use when: Creative and ad-group planning when launching Demand Gen for a store that has multiple creative concepts or formats to test against a product set.
- Group creatives by theme, not by randomness: for example, one ad group containing three to five iterations of a UGC-style product review video for a specific product.
- Pair each theme ad group with the matching product selection, e.g. select the specific item IDs for the stainless steel pans being reviewed, so creatives and catalog items stay relevant to each other.
- Run video ads first. The source states video is the most effective and highest-return Demand Gen format it has seen, especially when you have proven Meta/TikTok/Snapchat creatives to port over.
- Separate image ads (image + products format) into their own ad group, and consider a separate campaign; do not mix them into the video ad group.
- Treat product ads as separate again, at minimum a distinct ad group. The source notes these are very new and it has limited data, so treat as experimental.
- Point each ad to the most relevant URL: the specific product page when the ad promotes one product, or a relevant category/landing page when it covers a range.
- Do not reuse another creator's YouTube video as your own ad creative; the source's example of pulling a random Short is illustrative only.
Caveat: The claim that video is the highest-return format is the presenter's observation, not a benchmark.
Caveat: Product ads are new with thin data in the source; results may differ.

Tags: google-ads, demand-gen, creative-strategy, video-ads, ad-groups, product-feed, ugc
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Keeping Demand Gen Assets Few and Varied Enough to Test
Use when: Creative testing decision for a store setting up Demand Gen (or similar) ads that wants to know which messaging actually drives conversions.
- Fill only the fields that apply to the chosen format and keep optional asset counts low: the source recommends roughly one to three headlines, descriptions and long headlines for Demand Gen assets.
- Recognize the combinatorial problem: five of each field multiplies into combinations you cannot attribute, making it impossible to know which headline performed.
- Run identical ad content with only a single variable changed between ads so you can compare cleanly, rather than changing several fields at once.
- Keep the copy extremely relevant to the specific product or theme of the ad group, and high quality over quantity.
- Note that this low-count guidance is specific to Demand Gen-style assets; the source separately notes Search ads require at least three headlines, so do not apply the 'one to three' rule to Search.
Caveat: Minimum asset counts differ by campaign type; check current platform requirements.
Caveat: Single-variable testing assumes sufficient volume for significance; the source does not address low-volume cases.

Tags: google-ads, demand-gen, experiment-design, creative-strategy, ad-copy, split-testing
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Audience Signals in Demand Gen: Bias Toward Cold Reach
Use when: Targeting setup for a Demand Gen campaign when the goal is new-customer acquisition and you must avoid duplicating remarketing already handled by PMAX.
- Default to fully open targeting: the source reports this performs best for its Demand Gen campaigns.
- If you do add signals, use external interest indicators only: roughly three to five search themes, one to two in-market segments, and a couple of demographic adjustments, kept conservative so testing stays interpretable.
- Never include your own data: no customer lists, remarketing audiences, or converter audiences, since these direct Google toward people who already know the brand, which defeats the new-customer purpose.
- Avoid affinity segments; the source considers them too broad and low-meaning.
- Turn off optimized targeting. The source says it makes targeting go wide in ways that produce lower-quality traffic; testing it later is optional once you have results.
- Test with and without signals to see which your account responds to, rather than assuming signals help.
Caveat: The 'open targeting performs best' finding is the presenter's campaign experience, not a controlled benchmark.
Caveat: Audience options and naming may change in Google's interface.

Tags: google-ads, demand-gen, audience-targeting, new-customer-acquisition, remarketing, experiment-design
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Assigning Funnel Roles Across the Google Ads Account
Use when: Whole-account architecture review for a store unsure whether campaigns are duplicating work, cannibalizing each other, or leaving a funnel stage uncovered.
- Assign non-branded Shopping as the new-customer acquisition driver; exclude past visitors and branded traffic there so it targets genuinely new buyers.
- Assign branded Shopping and branded Search purely to collecting branded demand, nothing else.
- Assign Display and YouTube remarketing to re-engage site visitors.
- Assign Performance Max to product remarketing and follow-up: catching past visitors, branded-adjacent and non-converting traffic the Shopping campaign does not target.
- Assign Demand Gen to the top of funnel: capturing new users and traffic on YouTube, Discover and Gmail, the closest Google surfaces to Meta/TikTok-style cold acquisition.
- Sequence implementation: Shopping and branded campaigns first, then PMAX remarketing once conversions are consistent, then Demand Gen (or alongside PMAX if you have budget and scaling ambition).
- Check each new campaign against this map before launch to confirm it does not duplicate another campaign's traffic.
Caveat: The exact role boundaries depend on having separate branded and non-branded campaigns; without them, roles blur.
Caveat: The source presents this as its recommended structure for ecommerce, not the only valid one.

Tags: google-ads, campaign-structure, retargeting, new-customer-acquisition, funnel, shopping-campaigns, demand-gen
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Pre-Launch Checklist for Google Ads Campaign Settings
Use when: Final QA before launching or editing a PMAX or Demand Gen campaign in a store's account, to avoid giving Google uncontrolled creative and placement decisions.
- Turn off automatically created assets in every campaign where the option appears; the source's rationale is that auto-created assets mean you don't know what is shown or what you are paying for, and it explicitly skips the asset-generation screens.
- Turn off video enhancements in Demand Gen so Google does not reformat your creative.
- Disable Google video partners in Demand Gen to avoid lower-quality placements.
- Turn off optimized targeting in Demand Gen unless testing it deliberately after results exist.
- Keep the source's underlying principle: maximize control over what is shown and where, and only delegate control when you can observe the results.
- Resolve launch-blocking validation errors and inspect asset automation settings; do not assume every missing-asset warning can be ignored.
Caveat: These are the presenter's control-first preferences, presented as opinion; some accounts may benefit from automation, which the source acknowledges only for targeting in specific cases.
Caveat: Option locations and names in Google Ads change; verify in the current interface.

Tags: google-ads, campaign-settings, performance-max, demand-gen, creative-strategy, quality-control
Source: Full Ecom Google Ads Course 2026 (100% FREE).docx

---

## Pre-diagnosis rules: change history, time horizon, conversion latency
Use when: Before diagnosing or editing Google Ads when a store's revenue or ROAS appears to have dropped.
- Check change history first. If anyone (you, a teammate, the client, another agency) recently tweaked settings, bids, budgets, campaign structure or the website, assume that change is the cause before running any audit. Never make new changes on top of unexplained recent changes.
- Extend the time horizon. Avoid diagnosing on a 1-day read; zoom out as far as the account's conversion volume allows so you are not making decisions off small-sample noise.
- Check conversion latency. In Google Ads, conversions are attributed back to the click date, not the purchase date. So the last 3–4 days always look terrible on default conversion and ROAS columns, in every account.
- Build a custom column using 'conversions by conversion time' (conversions credited to the day of purchase) to get a real-time read on the last few days.
- Only after those three checks should you start level-one diagnosis; otherwise you risk changing a healthy account and pushing it into a worse position.
Caveat: The speaker states last 3–4 days always look bad in every account — this is their framing of default attribution behavior, not a benchmark.
Caveat: Redesigning the account (or multiple changes at once) risks a learning-phase reset that deepens the decline.

Tags: google-ads, measurement, attribution, conversion-latency, diagnostics, change-management
Source: How To Fix An Underperforming Google Ads Account.docx

---

## Level-one business check: cross-channel spend weighting and the revenue equation
Use when: When a store reports a revenue or efficiency drop and you must decide whether to investigate Google Ads, Meta/other channels, or the website first.
- Establish the media mix by spend share. If Google is only ~10% of spend (e.g., 90% Meta), a top-line revenue dip is very unlikely to be a Google issue — start elsewhere.
- If spend is more evenly split (e.g., 65% Meta / 35% Google), still do due diligence on both, but start with the higher-spend platform.
- Ask what else changed outside Google: did a promotion end, was there a creative refresh on Meta, did the offer change, did the business change something material? Get the client to confirm anything you're not across.
- Decompose the revenue equation: Revenue = Conversion Rate × Average Order Value × Sessions. Identify which of the three fell.
- Interpret the lever: AOV down points to product mix / upsell-cross-sell changes; conversion rate down points to landing page, offer or audience; sessions down points to a traffic source losing click volume.
- Reconcile platform attribution against true business KPIs (revenue, profit contribution, MER/AMER) to distinguish a real business decline from a tracking or attribution error.
Caveat: The speaker notes the majority of accounts they see skew to Meta — this is their client-base observation, not a universal rule.
Caveat: If Google holds majority spend, run the Google drill first even though the general sequence favours the biggest spender.

Tags: google-ads, measurement, cross-channel, revenue-equation, diagnostics, attribution, mer
Source: How To Fix An Underperforming Google Ads Account.docx

---

## Check seasonality against a forecast before diagnosing
Use when: When a store's revenue dips and you need to decide whether the decline is a real anomaly or expected seasonality before investing time in root-cause work.
- Maintain a forecast for the business so each period has an expected revenue range rather than a single number.
- When a dip appears, compare actual against the forecast for that period. If the dip is in line with expected seasonality, stop — do not run a diagnostic process to 'fix' something that was predicted.
- If the dip is outside forecast, proceed to the cross-channel and revenue-equation checks.
- Where forecasting is absent, treat any seasonal dip as a real problem and expect to burn hours diagnosing a fluctuation that will recur.
- Keep the forecast updated so the comparison is meaningful over time.
Caveat: The speaker's process treats an expected seasonal dip as requiring no action — this depends on the forecast being accurate; a bad forecast mislabels real declines as seasonality.

Tags: google-ads, measurement, seasonality, forecasting, diagnostics
Source: How To Fix An Underperforming Google Ads Account.docx

---

## Prioritise diagnosis by spend: top-5 campaigns only
Use when: When drilling into a Google Ads account to find the cause of a material business decline.
- In the campaign tab, sort by cost descending so the highest-spend campaigns sit at the top.
- Do not spend diagnostic time below the top five campaigns by spend. Example: a campaign at 10% of budget doubling performance moves the business ~5%, and if Google is only 40% of your media mix, that is single-digit impact.
- Theoretically a small campaign could be the cause, but the speaker argues it is unlikely; start where the impact is and work down only after the likely causes are cleared.
- Ask the client's specific complaint against this lens: if it's a 10% ROAS decline on the fifth-biggest spender while business-level KPIs are up, it probably does not need investigating at all.
Caveat: The 10%-budget and 40%-media-mix numbers are illustrative examples, not thresholds to apply as hard rules.
Caveat: This is the speaker's prioritisation heuristic; a small campaign can occasionally be the root cause.

Tags: google-ads, measurement, diagnostics, campaign-structure, prioritisation
Source: How To Fix An Underperforming Google Ads Account.docx

---

## 90–180 day weekly overview scan before drilling into campaigns
Use when: When starting the Google Ads portion of a diagnosis, before looking at individual campaigns.
- Set date range to the last 90–180 days and switch to a weekly view.
- Stay in the Overview tab and rotate through each metric: cost, conversions, conversion value, cost per conversion, ROAS (conversion value ÷ cost), and CTR.
- For each metric, note whether it went up, down or sideways and, critically, when the inflection point occurred (e.g., '3 March').
- Move to the Campaign tab and work down from the top five spenders, asking which campaign contributed most to the metric change after that date.
- Then drop to ad group level (or asset groups in PMax) and repeat the same exercise to see whether all groups moved or one specific group did.
- Output two facts: which campaign type fell off, and which specific campaigns and ad groups within it.
Caveat: The benefit of a weekly view is trend visibility; a shorter daily view reintroduces the small-sample and latency problems.
Caveat: The five-minute figure is the speaker's expectation for an experienced operator, not a guarantee.

Tags: google-ads, measurement, diagnostics, reporting, campaign-structure
Source: How To Fix An Underperforming Google Ads Account.docx

---

## Match failure modes to campaign type: PMax and Shopping
Use when: When a Google Ads decline has been traced to a specific campaign and you need to know what to inspect.
- Understand that PMax, Shopping and Search decline for different reasons, so establish campaign type before troubleshooting.
- PMax / Shopping check 1 — warm/cold drift: check the search term report for brand terms and the audience report for skew toward existing customers. If brand terms are appearing despite exclusions, or the audience skews warm, the exclusion is broken or target ROAS is pushed too high.
- PMax / Shopping check 2 — feed health: feed quality drives most Shopping performance (the speaker says 80–90% of PMax performance comes from Shopping). Check products in the campaign for out-of-stock, turned-off or disapproved items, and verify the GMC feed for errors and warnings, including changed titles or descriptions.
- PMax / Shopping check 3 — target ROAS: raising tROAS narrows targeting toward warmer, higher-conversion-probability buyers, likely pulling spend back and hurting new-customer acquisition. Cross-check new-customer ROAS in a third-party tool or natively in Google Ads; a higher tROAS typically shows worse NC ROAS.
- PMax / Shopping check 4 — product bloat and stock churn: a rapidly growing SKU count flooding one campaign can hurt learning, and high-spend products going in and out of stock reset that product's learning and can affect the whole campaign.
- Also check whether spend is being distributed into search partners with poor performance.
Caveat: The 80–90% figure is the speaker's stated observation, not a measured benchmark.
Caveat: Brand exclusion should already be in place — the check is a double-check, not a fix in itself.

Tags: google-ads, pmax, shopping-campaigns, feed-management, target-roas, diagnostics
Source: How To Fix An Underperforming Google Ads Account.docx

---

## Search campaign failure modes: search terms, auction insights, display leakage
Use when: When diagnosis points to a Search campaign as the source of a performance decline.
- Search terms: split the report either side of the inflection point, sort by spend, and compare the top-spending terms and their efficiency. With broad match and smart bidding, a wild reallocation of spend across terms can be the cause even when overall volume looks similar.
- Auction insights: compare before and after the inflection point. A new competitor entering the auction can raise CPCs or reduce your ability to enter auctions at all.
- Target ROAS: the same failure mode as PMax — raising tROAS narrows targeting toward warmer buyers rather than magically improving efficiency.
- Display leakage: confirm display is turned off for the campaign, or spend may be silently allocated to display, which correlates with the performance drop.
Caveat: If search terms and efficiency look materially unchanged either side of the inflection point, move on rather than forcing a conclusion.
Caveat: The display-leakage check is a specific Google Ads configuration risk; verify the current interface for where display settings live.

Tags: google-ads, search-campaigns, search-terms, auction-insights, target-roas, diagnostics
Source: How To Fix An Underperforming Google Ads Account.docx

---

## Metric decomposition: build the formulas before you touch anything
Use when: When you've isolated a declining campaign metric and need to trace it down to the trigger that actually moved.
- Keep the two core formulas in mind: CPA = CPC ÷ conversion rate, and Clicks = Impressions × CTR. The speaker says these cover roughly 90% of troubleshooting.
- At campaign level: attributed revenue is driven by CPC, conversion rate and AOV. Declining conversions come from fewer clicks, lower conversion rate, or broken tracking.
- Understand AOV itself decomposes further: it's a blend of new-customer AOV and returning-customer AOV, each sitting on a distribution curve, and each order is mechanically driven by units per transaction and average unit retail.
- Use this decomposition to get past superficial answers. Trying to fix AOV by asking 'what offer changed?' is not root cause; drilling into NC AOV, then the distribution curve, then whether UPT or AUR moved, is.
- Write out which sub-metric moved and what triggered it before proposing any fix.
Caveat: The 90% figure is the speaker's own estimate of coverage from those two formulas.
Caveat: The speaker says infinite decomposition is possible; the value is choosing the next useful level, not expanding until the trail goes cold.

Tags: ecommerce, measurement, metrics-decomposition, aov, diagnostics
Source: How To Fix An Underperforming Google Ads Account.docx

---

## CPC troubleshooting: quality score, competition and premium auctions
Use when: When diagnosing a Google Ads efficiency decline where cost per click has risen.
- Add columns for Quality Score, Expected CTR, Ad Relevance and Landing Page Experience at keyword level. Compare before and after the inflection point.
- Ad relevance is often the easiest to fix: make the ad copy more relevant to the search terms actually being served.
- Expected CTR extrapolates current CTR into the future, so it improves only by making the ads materially better.
- Landing page experience is the hardest to change: it requires dev work, and Google's re-crawl/rescoring cadence is unclear — the speaker reports it can take weeks to months even after the site is fixed.
- Check auction insights before and after the dip to see if a new competitor entered the auction and is pushing up CPCs.
- Consider whether you're now entering premium (more expensive) auctions as a result of a tROAS or bidding change — this is only a problem if those clicks aren't higher quality.
- Treat CPC as a near-vanity metric: CPC up with conversion rate up keeps CPA flat and is fine; CPC up with conversion rate flat is the problem signal.
Caveat: Landing page experience is presented as occasionally being the bottleneck despite the long, uncertain resync cycle.
Caveat: Premium auction entry is not automatically bad — judge it on whether conversion rate compensates.

Tags: google-ads, cpc, quality-score, auction-insights, diagnostics
Source: How To Fix An Underperforming Google Ads Account.docx

---

## Conversion-rate troubleshooting: tracking, landing page, audience, learning, offer
Use when: When the conversion-rate leg of the revenue equation has fallen and you need to find which factor is responsible.
- Check tracking first: confirm conversion tracking still fires and that you aren't reading the last few days using default conversion columns instead of conversions by conversion time.
- Check landing page changes: did the URL change, were prices changed, is a redirect pushing traffic elsewhere, were upsells/cross-sells added, did merchandising shift? The speaker treats this as the number one likely cause of a conversion rate decrease.
- Check audience change: same page and site but lower-quality traffic from premium auctions converts worse, and vice versa. Inspect search terms for relevancy to the landing page and whether a bidding-strategy change is pushing toward a different audience.
- Check learning phase: a large structural change to the account resets the learning phase, which reliably lowers conversion rates because the system enters the wrong auctions and sends poor traffic.
- Check the offer: a promo ended, a discount was removed, or the free shipping threshold changed — all directly affect conversion rate.
Caveat: A learning-phase reset from structural change can push you into a feedback loop of decline; avoid causing it unnecessarily.
Caveat: The ordering reflects the speaker's experience, not a published causal test.

Tags: google-ads, conversion-rate, landing-page, tracking, learning-phase, diagnostics
Source: How To Fix An Underperforming Google Ads Account.docx

---

## Volume troubleshooting: clicks = impressions × CTR, budget vs bid share loss
Use when: When Google Ads efficiency is stable but volume (spend or revenue) has fallen and you need to find why clicks dropped.
- Split the click loss into impressions and CTR. Impressions falling means you're entering fewer auctions or your listings show less often.
- Distinguish impression share lost to budget from impression share lost to bid. If you're hitting your daily budget cap, more impressions require more spend.
- If click volume and impressions are both down while spend has been steady, the speaker says it's almost certainly a bid issue rather than a budget one.
- Fix impression share lost to bid by working on its inputs: quality score, new competitors in the auction, and how aggressively you're entering auctions.
- If CTR is the falling leg, look at ad fatigue (rare on Google, more plausible on search than Shopping) and audience mismatch — the ad may no longer fit the people and search terms it now serves.
- Check ad copy for time mismatch (e.g., a summer sale still running after summer) and, on Shopping, check competitive pricing on the same products.
Caveat: Ad fatigue is described as rare on Google, but the speaker allows for it in search ads.
Caveat: The budget-vs-bid inference relies on spend being stable over the comparison period.

Tags: google-ads, ctr, impression-share, budget, diagnostics
Source: How To Fix An Underperforming Google Ads Account.docx

---

## Competitive pricing scripts: pull products rather than match discounts
Use when: When Google Shopping CTR and ROAS fall on specific products and you suspect a competitor has discounted the same items.
- Track competitor pricing on your key products in real time — the source describes a script monitoring a major competitor's website for price changes.
- When a competitor cuts price materially (the example is 20–30% off), pull or de-prioritise the affected product in the campaign structure rather than continuing to force spend to it.
- Rationale: continuing to run the product would mean ROAS falls off a cliff, and matching the discount would erode gross margin to almost nothing.
- Use Impression Share lost to rank (search impression share lost {rank}) as the native Google Ads column for this signal.
- Reintroduce the product when the competitive discount ends and the price gap closes.
Caveat: This is one client example (a sunglasses wholesaler), not a guaranteed result.
Caveat: Script availability and metric naming may change — verify the current Google Ads interface before building the workflow.

Tags: google-ads, shopping-campaigns, pricing, competitive-analysis, automation
Source: How To Fix An Underperforming Google Ads Account.docx

---

## Default to fixes, not rebuilds — and protect the learning phase
Use when: When you've reached the root cause and are choosing between a targeted change and restructuring the account.
- Start with a fix, not a rebuild. Any rebuild triggers a learning reset, which the speaker says will likely put you in a worse position.
- Evidence the danger: performance declines, so you make a big change, which causes further decline, which prompts another big change — a feedback loop until the account is in a bad state.
- After applying a fix, allow enough time to determine whether it worked before layering another change.
- Only if fixes don't work, or clearly won't bridge the gap to historical performance, consider a rebuild.
- Before applying, ask honestly how much impact this specific change will make. Changing a headline is unlikely to fix an entire business decline unless a headline change was the original cause. Keep re-thinking the fix until you believe it's strong enough to move the problem area.
Caveat: The speaker acknowledges situations dire enough that a 'kitchen sink' response is justified — in that case speed beats clean attribution of the fix.
Caveat: The threshold for 'enough time' depends on the account's conversion volume, not a fixed window.

Tags: google-ads, learning-phase, change-management, diagnostics, experiment-design
Source: How To Fix An Underperforming Google Ads Account.docx

---

## Isolate one fix at a time to preserve causal learning
Use when: When deciding how many changes to apply to a landing page, offer or campaign after diagnosing a decline.
- Recognise the 'kitchen sink' problem: if you change the offer, redesign the landing page, and adjust traffic continuity all at once and performance recovers, you cannot identify which change mattered.
- If the problem recurs later, you'll be unable to solve it without repeating the kitchen sink — you've learned nothing transferable.
- Strip back to a smaller set of changes so the outcome is interpretable; this is where the speaker says the strategic judgement lies.
- Assess severity first: a dire, urgent decline may justify a kitchen sink because fixing it matters more than knowing why; a mild dip rewards a clean, attributable test.
Caveat: Isolating variables slows recovery — the trade-off must be weighed against severity.
Caveat: This is a principle for interpretability, not a controlled-experiment protocol; the source doesn't specify sample-size or duration requirements.

Tags: ecommerce, conversion-optimization, experiment-design, measurement, landing-page
Source: How To Fix An Underperforming Google Ads Account.docx

---

## Root-cause sentence test: don't touch the account until you can complete it
Use when: Before applying any fix to a Google Ads account following a diagnostic process.
- Assemble the full chain from the top down: business KPIs → channel checks → campaign types → specific campaign → metric → sub-metric → trigger → root cause.
- Check whether you can finish the sentence: 'this campaign is underperforming because this metric dropped, driven by this sub-metric, which was caused by this trigger, which itself was the root cause.'
- If you cannot complete that sentence after the process, do not change the account.
- Where the client points at a bottom-level metric (e.g., 'CPC is down on this ad'), zoom out first: check business-level KPIs and whether the issue matters to growth. Often it doesn't, and the hour is better spent elsewhere.
Caveat: The speaker describes this order of investigation as the skill that separates strong performance marketers from habitual tweakers — it's their opinion, not a formal standard.
Caveat: The gate can be overridden when a fix is clearly necessary for business continuity.

Tags: google-ads, diagnostics, decision-making, change-management
Source: How To Fix An Underperforming Google Ads Account.docx

---

## Diagnose Whether You Are Overspending or Underspending on Google Ads
Use when: Setting annual or quarterly budget allocation across Google, Meta, TikTok and affiliates, or deciding whether to increase Google spend when the platform reports high ROAS.
- Recognise the two failure modes: (1) overspend — Google looks efficient because it captures bottom-intent demand generated by Meta, TikTok and affiliates, so you push budget into spend that isn't incremental; (2) underspend — you believe Google is only bottom-funnel so you cap it at e.g. $10k/month while spending millions on Meta, even though your category has large cold search volume your product could serve.
- To test which camp you're in, look at whether backend revenue moves when you increase Google spend, not just the in-platform ROAS figure.
- If backend revenue does not track budget increases, you are likely overspending and should hold or redistribute, not scale further.
- If backend revenue is constrained only because you never funded Google beyond a token amount, investigate cold search demand for your category terms before dismissing the platform.
- Treat the source's >$10k/month anecdote as an illustration of the pattern, not a threshold for your store.
Caveat: The two-camp framing is the source's heuristic; real accounts sit on a spectrum.
Caveat: Attribution overlap between Google and upper-funnel channels makes either error easy to misdiagnose from platform numbers alone.

Tags: google-ads, budget-allocation, incrementality, measurement, acquisition, media-mix
Source: The Only Google Ads Strategy You Need for 2026.docx

---

## Consolidate Campaigns Before Segmenting Them
Use when: Auditing or restructuring campaign architecture (shopping, PMax, search) or when you see ROAS fall as you go down the campaign list.
- Map each campaign's 30-day conversion volume. If you run three shopping campaigns with 50, 20 and 10 conversions respectively, ignore the small amount of cross-campaign platform data sharing and model them as fully siloed.
- The campaign with 10 conversions is modelling bids off 10 users' psychographic data — it cannot bid accurately and will underperform. This is why account structures typically show ROAS declining in line with conversion volume.
- Merge products and budget into the highest-volume campaign to pool conversions (e.g. 90/month) so smart bidding has a larger dataset and produces more accurate auction bids.
- Only re-segment once you can justify the split commercially — the default should be one campaign; each additional campaign must earn its place.
- Validate any restructuring with backend revenue, since consolidated campaigns may look better in-platform for reasons unrelated to true incrementality.
Caveat: Consolidation assumes products share margin profile, market and creative logic; merging different-margin or different-country products distorts bidding.
Caveat: Platform-level data sharing exists to a degree; the silo model is a simplification for planning.

Tags: google-ads, account-structure, campaign-consolidation, measurement, shopping-campaigns
Source: The Only Google Ads Strategy You Need for 2026.docx

---

## The Four Justifications for Segmenting a Google Ads Account
Use when: Deciding whether to create an additional campaign for a product line, market or margin tier.
- Start from the default of one campaign; require heavy justification for every extra campaign.
- 1) Brand vs non-brand: never let a single PMax or shopping campaign cover both, because you want branded placements and cold acquisition managed separately.
- 2) Geography: selling in multiple countries always warrants campaign-level separation.
- 3) Margin or efficiency goals: a 70% gross-margin collection must not share a bidding strategy with a 35% margin collection. At a 300% target ROAS the 35% line is barely profitable while the 70% line is very profitable, and because Google usually can't see margin it will push all spend to whichever drives more revenue.
- 4) Product category: products that attract different personas (e.g. office chairs vs plants) should learn separately so each models its own audience.
- When proposing a split, name which of the four variables it addresses — if none apply, consolidate.
Caveat: The 70%/35% margin and 300% ROAS figures are illustrative.
Caveat: Margin-based segmentation depends on having margin data available to feed the platform; otherwise you're relying on separate campaigns and bids.

Tags: google-ads, account-structure, segmentation, margin-management, positioning, bidding
Source: The Only Google Ads Strategy You Need for 2026.docx

---

## Convert SKAGs into Single-Topic Ad Groups
Use when: Restructuring search campaign ad groups, or inheriting an account still running Single Keyword Ad Groups.
- Understand why SKAGs died: an RSA contains up to 15 headlines, 4 descriptions and other assets, producing roughly 2,700 combinations. Google split-tests these against each other, and testing realistically needs about a quarter-million impressions to resolve.
- A single exact-match keyword will never deliver that volume, so the ad stays stuck in learning and cannot optimise.
- Restructure into single-topic ad groups: e.g. 'general plumbing', 'emergency plumbing', 'affordable plumbing'. Under each theme, place 10–20 themed keywords rather than one.
- Write ads tuned to the theme so they are contextually relevant to every keyword in the group; the dynamic RSA then adjusts which headlines serve based on which keyword in the theme triggered.
- When auditing an existing SKAG account, transition to single-topic groups and compare performance — the source reports better results consistently across audited accounts, while acknowledging rare accounts where SKAGs still work.
Caveat: The quarter-million-impression figure is the source's testing heuristic, not a platform-published threshold.
Caveat: The source's demonstrated example is a service business; the same logic is applied by the source to ecommerce search campaigns.

Tags: google-ads, search-campaigns, ad-groups, responsive-search-ads, account-structure
Source: The Only Google Ads Strategy You Need for 2026.docx

---

## Fix the Seven Most Common Google Ads Setup Mistakes
Use when: Running an account audit or onboarding a store's existing Google Ads account.
- 1) Don't use GA4 events as the primary conversion: the source reports a 10–15% (sometimes higher) attribution gap versus direct snippet code on the site.
- 2) Don't run a single asset group in a PMax campaign — build segmentation at asset-group level.
- 3) Don't pair broad match with Maximize Clicks: broad match needs a smart bidding strategy to work well.
- 4) Turn off display in search campaigns; the source rates display as one of the worst networks, especially for cold traffic.
- 5) Add negative keywords — both branded negatives on cold campaigns and general negatives in search campaigns.
- 6) Turn off auto-applied recommendations so Google stops making changes you didn't approve.
- 7) Set a naming convention: agency tag, region, campaign type (PMax/shopping/search), audience (cold/brand/theta), and optionally goal, so anyone can read the account.
Caveat: The 10–15% GA4 gap is the source's observed figure and should be verified in your own setup.
Caveat: Naming convention fields are the presenter's preference; adapt to your team.

Tags: google-ads, account-audit, measurement, conversion-tracking, naming-convention, search-campaigns, negative-keywords
Source: The Only Google Ads Strategy You Need for 2026.docx

---

## Set Up PMax Asset Groups with Matching Listing Groups
Use when: Building or auditing a Performance Max campaign for an ecommerce store.
- Know the mechanics: an asset group holds images, headlines and descriptions used for search, display, YouTube, Discover and Gmail placements; its listing group holds the products from the Merchant Center feed that serve on Shopping.
- If you accept the default single asset group, everything is bundled and creative can't be matched to intent.
- If you build multiple asset groups but forget to customise each listing group, every asset group still contains all products — the segmentation does nothing.
- Four reasons to segment: (1) creative relevance — a shopper who viewed jeans should be retargeted with jeans imagery and copy, not random catalogue items; (2) audience signals work better when granular, since you can signal 'in market for jeans' instead of vague 'fashion'; (3) search themes become specific; (4) you gain visibility into performance by asset group, e.g. seeing that tops are outperforming jeans due to seasonality and reallocating budget.
- Apply the rules of thumb: one asset group per product type (chairs/tables/lighting/decor, or hand tools/power tools/fasteners/accessories), at least 15 products per asset group, never one product alone (it will get little spend).
Caveat: The 15-product minimum is a flexible heuristic that depends on SKU count.
Caveat: The source advises a minimum of three and maximum of about 20 asset groups; beyond 20 most businesses lack the complexity to justify it.

Tags: google-ads, performance-max, asset-groups, listing-groups, product-feed, segmentation
Source: The Only Google Ads Strategy You Need for 2026.docx

---

## Use Brand Exclusions and Weigh What Actually Matters in PMax
Use when: Configuring or prioritising fixes inside an ecommerce PMax campaign.
- Exclude your brand from PMax. Two methods exist: (1) campaign settings → brand exclusions → add new brand, let Google index your branded terms and apply the brand list; (2) the newer capability to add negative keywords directly to PMax. The source recommends doing both as fail-safes so a missed variation is still caught by the list and vice versa.
- After running PMax across ~250 accounts and consulting on ~400 more, the source ranks variables in this order: (1) the GMC feed — titles, descriptions, imagery (assuming PMax is prioritising Shopping); (2) brand exclusions; (3) asset and listing group structure plus the assets themselves; (4) bidding strategy; (5) audience signals and search themes.
- Search themes and audience signals are signals, not targeting — they do not guarantee bids on those terms. Prioritise keywords that historically converted in your account rather than inventing them.
- For mature accounts spending tens of thousands per month, the source reports audience signals and search themes are roughly a 1% lever at best; they matter mainly on new business, new product, new category or new asset group launches, where there is no conversion history.
- Once a campaign has ~30 days of conversion data, Google bypasses the audience signal — the source states you could remove it with no performance impact.
- Verify current interface locations for brand exclusion and negative keyword settings before acting, as Google changes these.
Caveat: The ranking and agency-tested figures are the source's own observations, not published benchmarks.
Caveat: The claim that audience signals stop mattering is explicitly flagged as potentially controversial.

Tags: google-ads, performance-max, brand-exclusions, search-themes, audience-signals, product-feed
Source: The Only Google Ads Strategy You Need for 2026.docx

---

## Run a Feed-Only PMax and Check Actual Channel Delivery
Use when: Evaluating a feed-led versus full-asset Performance Max campaign for an ecommerce product catalog.
- Confirm Merchant Center linkage, eligible products, accurate prices and stock, and tested purchase-value tracking.
- Treat the source feed-only approach as a test of reduced manually supplied creative. Review the actual asset-generation and URL-expansion settings in the current interface.
- Monitor channel delivery, product performance and new versus returning customer outcomes; compare contribution and acquisition cost with the existing Shopping or full-asset setup.
- Do not classify the campaign as remarketing-only or promise Shopping-only delivery. Use a campaign with appropriate audience controls when strict remarketing is required.
Caveat: Editorial correction: PMax audience signals do not impose strict targeting; omitting manual creative does not guarantee placement isolation. https://support.google.com/google-ads/answer/14530785
Caveat: Merchant Center data can generate assets automatically. Source examples of efficient feed-led campaigns are not delivery guarantees. https://support.google.com/google-ads/answer/15865151

Tags: google-ads, performance-max, feed-only, placement-targeting, budget-control, shopping-campaigns
Source: The Only Google Ads Strategy You Need for 2026.docx

---

## Use Max Conversion Value to Gather Data, Then Move to Target ROAS for Stability
Use when: Choosing or changing the bidding strategy on a PMax or shopping campaign.
- Launch on Maximize Conversion Value to accumulate conversion data, then roll into Target ROAS once data exists — this matches how the platform is designed to be used.
- Expect the trade-off: Max Conversion Value produces large up-and-down swings as the algorithm makes bigger bets; Target ROAS smooths the distribution. The source notes total performance over the same period is roughly comparable — the difference is day-to-day reliability.
- When setting the initial Target ROAS, look at trailing ROAS and set slightly below it (e.g. trailing 420–430% → set 400%).
- Then watch for the trap: repeatedly nudging Target ROAS upward (400% → 425% → 450% → 500%) squeezes spend down until a new equilibrium. It looks like improved media buying, but the campaign is restricting who it bids on — the pool narrows toward warm audiences and existing customers rather than new ones.
- If you need reliable daily revenue and don't need to chase incremental cold acquisition on that campaign, the higher target is a reasonable trade — but if you're already tight on volume, prefer a lower target and more spend.
Caveat: Figures like 400–500% target ROAS are illustrative examples of the trap, not benchmarks.
Caveat: The source frames the choice as reliability versus reach, not strictly better versus worse.

Tags: google-ads, bidding-strategies, target-roas, max-conversion-value, scaling, measurement
Source: The Only Google Ads Strategy You Need for 2026.docx

---

## Build a Feeder Strategy: Cold Shopping Plus Warm PMax
Use when: Scaling cold new-customer acquisition on Google when PMax alone has plateaued and you suspect warm-traffic over-attribution.
- Set up two campaigns: (1) a broad, low-Target-ROAS campaign (source example as low as 50%, i.e. 0.5 ROAS) that will bid across the entire pool of users searching relevant terms; (2) a high-Target-ROAS campaign (source example 600%) that only targets warm, in-market, likely-to-buy users, often previous site visitors.
- The logic: most advertisers only bid on the high-intent half of the user pool (people who have visited many sites and used purchase-relevant terms). Google sees the other half as low intent — first-time searchers with no site history — and almost nobody competes for those auctions, so clicks are cheap.
- The cold campaign drives traffic cheaply; the warm campaign captures and converts it on second or third click. The source reports this works well across many accounts.
- Practically, run standard shopping as the cold campaign (it is better at reaching cold audiences) and PMax as the high-target-ROAS retargeting leg.
- Why this is needed: the source reports that in private discussions, major agency owners agree PMax substantially over-attributes — 50%+ of PMax conversions are repeat or warm customers it didn't acquire — while standard shopping under-attributes because PMax takes credit for the final click. Verified against ~250 accounts running PMax plus ~400 consulted ecommerce accounts.
Caveat: The 0.5 and 6.0 ROAS levels are source examples; set your own bands against your margin and data.
Caveat: The 50%+ over-attribution figure is an industry observation reported by the source, not a measured benchmark you can rely on for your account.
Caveat: Feeder strategies require enough spend to fund a deliberately unprofitable cold campaign without hurting overall economics.

Tags: google-ads, performance-max, shopping-campaigns, incrementality, retargeting, acquisition, bidding
Source: The Only Google Ads Strategy You Need for 2026.docx

---

## Recognise PMax's Ceiling and Reframe the Allocation Question
Use when: Deciding whether to keep scaling PMax or redistribute budget into standard shopping.
- If you are spending roughly $15–20k/month or less, PMax is useful to get the account moving and scaling.
- As you scale PMax further, expect it to plateau. In the source's testing on large accounts scaled to $100k–$300k/month, doubling PMax budget while in-platform ROAS stayed at 5x did not move backend revenue.
- Two common reactions both fail: raising budgets further, or raising the target ROAS. Both push more spend into warm and repeat traffic, so the in-platform ROAS may rise while the campaign becomes a 'glorified retargeting campaign'.
- Accept that once PMax plateaus, further cold growth requires layering in standard shopping.
- Measure the right thing: run a controlled ramp — scale one campaign type by 2x over 30 days and compare with another account ramping the other — and check backend revenue, not the in-platform ROAS. The source reports standard shopping consistently produced better incremental backend revenue despite its in-platform ROAS dropping (e.g. 5x → 4x → 3x) while PMax's stayed at 5x.
- Reframe the planning question from 'should I run PMax?' to 'what percentage allocation should PMax versus standard shopping get?' — the source suggests roughly 20–40% to PMax for mid-to-upper-market ecommerce, with the majority in standard shopping.
Caveat: The 20–40% allocation and $15–20k/month threshold are the source's heuristics, not universal rules.
Caveat: The ramp test is illustrative and confounded by account differences; treat results as directional.
Caveat: Lead-gen businesses should read 'shopping' as 'search'.

Tags: google-ads, performance-max, shopping-campaigns, incrementality, budget-allocation, scaling, measurement
Source: The Only Google Ads Strategy You Need for 2026.docx

---

## Choose Between the Three Standard Shopping Structures
Use when: Choosing a standard shopping campaign structure for an ecommerce catalogue.
- Structure 1 — top sellers split: put all top sellers in one standard shopping campaign and everything else in a second. This forces Pareto (aim for ~80% of spend on the top 20% of products) while keeping a testing budget on the long tail to promote new winners. Suitable for a large SKU count in a non-fashion category; not suitable for fashion or a 5–10 product business.
- Structure 2 — feeder strategy: run standard shopping as the cold traffic engine feeding a high-target-ROAS campaign (see separate card).
- Structure 3 — labelizer/flo boost tiers: split products into over-index, index, near-index, under-index and no-index based on 30-day rolling performance, with bidding strategy and budget tuned per tier. You can label manually for small catalogues or run an automated labelizer script that re-tiers products in real time.
- The source only recommends the labelizer for catalogues with thousands of SKUs — for most businesses it adds segmentation complexity without enough upside.
- Apply the same four segmentation justifications as everywhere else (brand, geography, margin, category) if you split further.
Caveat: The source explicitly warns against the top-seller split for fashion and small catalogues.
Caveat: 80% of spend on the top 20% of products is a stated aim for that one structure, not a general rule.

Tags: google-ads, shopping-campaigns, account-structure, product-selection, automation, merchandising, sku-management
Source: The Only Google Ads Strategy You Need for 2026.docx

---

## Keep 80–90% of Ecommerce Google Spend in Shopping, Not Search
Use when: Deciding how to split budget between shopping and search campaigns for an ecommerce store.
- For ecommerce and retail, target roughly 80–90% of Google spend in shopping rather than search — the source's core recommendation for the category.
- Reason: search ads give the user a headline, a description nobody reads and a couple of extensions. Shopping shows the product image, price, title, active promos or reviews, brand name and extensions, with about five competitors beside you so the shopper pre-selects the most relevant listing before clicking.
- For visual categories like fashion this matters most: search ads for 'red dress' attract clicks from people who then bounce because the style isn't theirs; shopping ads filter that mismatch pre-click.
- Exception to reverse the split: ecommerce businesses with a B2B component. The source reports search outperforms shopping there — e.g. selling bulk eyelashes to technicians and small businesses — because a business buyer often won't click a shopping listing whose price doesn't match the mental model of a business purchase.
- Only push into search after you've saturated shopping and need additional volume.
Caveat: The 80–90% allocation is the source's recommendation for ecommerce, not a measured optimum for every store.
Caveat: The B2B exception is the source's observation and depends on your buyer type.

Tags: google-ads, shopping-campaigns, search-campaigns, budget-allocation, product-page, b2b, conversion-optimization
Source: The Only Google Ads Strategy You Need for 2026.docx

---

## Choose Shopping vs Search by Buyer Type
Use when: Deciding how to split Google Ads budget between Shopping and Search when your store sells both to consumers and to businesses (bulk, wholesale, trade customers).
- Ask whether a meaningful share of your buyers purchase for a business reason: bulk quantities, trade/technician use, repeat supply, or known-supplier relationships.
- Default to putting about 90% of ecommerce focus into Shopping, since that is where most consumer product discovery and greatest leverage sits.
- Break that default when the store has a B2B component: B2B buyers tend to skip Shopping listings because shown unit prices feel wrong for the bulk deal they want, so they click Search ads instead. Example given: bulk eyelashes sold to technicians and small salons perform better on Search than Shopping.
- If B2B applies, build Search campaigns around supplier-intent and bulk-intent language, and keep consumer Shopping running separately.
- Segment B2B traffic and creative onto different landing pages so bulk pricing and trade terms aren't shown to consumer shoppers.
- Judge by comparing cost per acquisition and revenue per click between the two channels in your own account rather than assuming the general rule applies.
Caveat: The 90% Shopping figure is the source's rule of thumb for consumer ecommerce, not a benchmark for B2B-heavy stores.

Tags: google-ads, shopping-ads, search-ads, b2b, channel-mix, budget-allocation
Source: The Only Google Ads Strategy You Need for 2026.docx

---

## Rebuild Google Shopping Product Titles for Keyword Reach
Use when: Optimizing the Google Merchant Center feed so your product listings appear for more relevant search queries and earn more clicks.
- Pull the search term report and identify the query variants that already convert for that product type (for example 'formal dress', 'dissolvable creatine powder', 'clear', 'flavored', 'portable').
- Move the brand name to the end of the title, or remove it entirely if nobody searches for your brand; the brand already appears lower in the Shopping listing.
- Move the decorative or internal product name (for example 'Nathan dress') out of the prime position unless it is a recognised product name.
- Lead with the highest-value relevant keyword plus product type so intent is clear to both the user and the algorithm.
- Append as many relevant attributes as fit within the title character limit so you can be matched on more specific queries (for example colour or size attributes).
- Continue adding researched keyword variants until the title is full.
- If a product has variants (for example 50g, 100g, 500g packs) that each generate a separate Shopping listing, give each variant its own title, image and description aimed at a different keyword pool, even though they land on the same product page.
Caveat: There is no golden title formula; base every change on your own historical search term data.
Caveat: Roll title changes out gradually, not all at once; a bulk switch resets learning phases across campaigns.
Caveat: This is a source-specific approach that should be validated against your own CTR and conversion results.

Tags: google-ads, product-feed, google-merchant-center, shopping-ads, product-titles, keyword-research
Source: The Only Google Ads Strategy You Need for 2026.docx

---

## Diagnose and Break the Target ROAS Death Spiral
Use when: Auditing a Google Ads account where spend has been gradually trailing off, or where target ROAS campaigns have stopped delivering volume.
- Look for the pattern over time: flat or rising spend, a dip in actual ROAS, then a steady decline in spend and conversions.
- Understand the mechanism: the campaign stops hitting target ROAS, so it narrows the audience it bids on, which cuts conversions, which reduces the last 30-90 days of conversion data, which degrades the bidding model, causing a worse audience and further decline.
- Recognise that seasonal dips, a strong product going out of stock, or any conversion drop can start the spiral through small sample sizes and worse targeting.
- If you decide to lower the target ROAS, do it aggressively rather than in small steps; timid reductions commonly fail to arrest the decline.
- Watch new accounts and recently onboarded campaigns for early signs so you can fix it before volume reaches zero.
- Once volume recovers, avoid leaving target ROAS fixed permanently; rotate between restrictive and expansive strategies over longer periods to prevent over-siloing.
Caveat: This is a mechanical failure pattern described by the source, not a universal rule; some campaigns with sufficient volume and stable history may hold a fixed target ROAS.

Tags: google-ads, bidding-strategies, target-roas, measurement, account-audit
Source: The Only Google Ads Strategy You Need for 2026.docx

---

## Pick Expansive vs Restrictive Bidding by Testing Appetite
Use when: Choosing or reviewing the bidding strategy for a Google Ads account and deciding whether you need scale discovery or tighter efficiency.
- Classify the strategy: maximize conversions and maximize conversion value are expansive because they can enter any auction; target CPA and target ROAS are restrictive because they only enter auctions that fit an efficiency target.
- Use the rough concept that an expansive strategy allocates something like 30% of budget to testing new keywords, audiences, placements, regions and similar adjacent bets, which is what can unlock scale.
- Assume a restrictive strategy has roughly 0% testing budget; how strict it really is depends on the gap between your achieved ROAS and the target. If you're hitting 4 and target is 4.5, testing is effectively zero; if you're hitting 5 and target is 2, it behaves more like max conversion value.
- Weigh the trade-offs: expansive bidding wins auctions it otherwise wouldn't but also loses some it otherwise wouldn't, so it is higher risk; restrictive bidding is more efficient but silos you into one audience and demographic over time.
- Rotate between the two over extended periods rather than staying on target ROAS permanently, to avoid a siloed negative feedback loop.
- As a default for ecommerce, the source recommends going for value most of the time, because value bidding reflects product margin differences that pure conversion bidding ignores.
Caveat: The 30% testing figure is an illustrative concept from the source, not a measured benchmark.
Caveat: Bidding behaviour and available settings change; verify current strategy options in the Google Ads interface.

Tags: google-ads, bidding-strategies, target-roas, max-conversion-value, budget-allocation, experiment-design
Source: The Only Google Ads Strategy You Need for 2026.docx

---

## Maximize Conversion Value Instead of Conversions for Mixed-Margin Catalogs
Use when: Choosing between maximize conversions/target CPA and maximize conversion value/target ROAS when your catalog spans very different price points and margins.
- Model the failure case: a $40 t-shirt can acquire customers at, say, $20 CPA while a $200 jumper may cost $60 CPA, so a conversion-optimized campaign funnels nearly all budget into the t-shirt.
- Check the ROAS of each: in the source example the t-shirt returns around 2x while the jumper returns around 3.5x, which is the outcome you'd prefer to fund.
- Recognize that maximize conversions cannot distinguish these, because it optimizes for the lowest CPA and highest order count, not for value.
- Switch ecommerce campaigns to value-based bidding (maximize conversion value or target ROAS) so the system weights higher-value orders.
- Confirm your conversion tracking passes order value accurately before relying on value bidding, otherwise the model learns the wrong signal.
- Review product-level spend after switching to verify budget is moving toward the higher-ROAS items you intended to fund.
Caveat: The dollar figures are illustrative examples from the source, not ecommerce benchmarks.
Caveat: Value bidding depends on accurate transaction value data; bad data will reinforce bad allocation.

Tags: google-ads, bidding-strategies, max-conversion-value, pricing, profitability, product-mix
Source: The Only Google Ads Strategy You Need for 2026.docx

---

## Use Portfolio Bidding to Merge Learnings and Cap CPC
Use when: You have deliberately split campaigns into segments (brand, category, margin tiers) and want them to learn together, or you need to cap expensive clicks.
- Confirm you need the segmentation for a commercial reason, since the primary goal is still to have as few campaigns as possible.
- Set up a portfolio bid strategy at the account level and apply it to the chosen campaigns so their conversion learnings are housed and modelled together rather than in isolation.
- Use the portfolio to layer a maximum and minimum CPC on a target ROAS or maximize value strategy. Example: in high-end furniture where individual clicks can reach $10-$30, set a max CPC so the algorithm never buys a click above your profitable ceiling.
- Treat this as the fix when too much segmentation has isolated campaigns from each other, since it recovers shared learning without rebuilding your structure.
- Check whether the equivalent feature is available in your campaign types before designing a strategy around it; the source notes this capability differs by account tier and campaign type.
Caveat: Portfolio bid strategies and CPC caps sit outside Pmax and Shopping in the source's account, so verify current availability in the Google Ads interface.
Caveat: A max CPC cap restricts auctions, so set it from your own profitable spend ceiling rather than guessing low.

Tags: google-ads, bidding-strategies, portfolio-bid-strategy, campaign-structure, cpc, account-audit
Source: The Only Google Ads Strategy You Need for 2026.docx

---

## Exploit Search Campaign Smart Bidding Exploration
Use when: You run Search campaigns on target ROAS and want some of the scale benefits of expansive bidding without abandoning efficiency targets.
- Set the Search campaign to a restrictive strategy such as target ROAS as your efficiency baseline.
- Enable the smart bidding exploration setting on the Search campaign so the algorithm can go outside the ROAS target in roughly 10-30% bands to test auctions it would otherwise skip.
- Treat this as a middle ground between restrictive and expansive strategies, giving efficiency plus some discovery of new audiences.
- Monitor whether the exploration produces incremental converting traffic or just erodes efficiency, and adjust the target accordingly.
- Note that this option is not available on Pmax or Shopping in the source's experience, so it applies to Search only.
- Verify the setting's current name and availability in the Google Ads interface, since platform settings change.
Caveat: Source-specific recommendation; the setting may have moved, been renamed or changed scope.
Caveat: Search campaigns are the source's secondary channel for most consumer ecommerce, so this tactic matters most where Search is already a focus.

Tags: google-ads, search-ads, bidding-strategies, target-roas, experiment-design
Source: The Only Google Ads Strategy You Need for 2026.docx

---

## Build Negative Keyword Discipline in the First 30 Days
Use when: Launching or taking over Search campaigns and controlling wasted spend on irrelevant queries.
- Expect the first 30 days to be the highest-leverage period for negative keywords, since campaigns go broad and pick up irrelevant terms.
- Review negative keywords weekly in the first 30 days. If budgets are high, review daily to prevent keyword bleed and wasted spend.
- From month one onward, drop the cadence to roughly weekly or nightly rather than constantly editing.
- Avoid over-tweaking negatives, because every edit resets learnings and impacts performance.
- Build a universal negative keyword list applied at account level so every new campaign inherits it automatically; search for an existing list, ask an LLM to draft one, or build your own.
- Seed the list with clearly irrelevant themes such as jobs, careers, interns, hiring and salary, which should never receive your ads.
- Use topic ad groups rather than keyword ad groups on the negative keyword side where you have thousands of SKUs; below that scale, this usually just overcomplicates the account.
Caveat: The weekly/daily cadence depends on your budget level and search volume.
Caveat: Exact negative keyword lists are not universal; audit yours against your catalog and business model.

Tags: google-ads, search-ads, negative-keywords, waste-reduction, account-audit
Source: The Only Google Ads Strategy You Need for 2026.docx

---

## Explain the Low Leverage of Average CPC
Use when: Reviewing Google Ads reporting or evaluating an agency's proposed CPC-focused optimization for your store.
- Write out the acquisition equation: cost per click drives traffic, and revenue equals conversion rate times average order value, so total return depends on all three.
- Stop optimizing solely for the lowest CPC, since cheap clicks can be junk traffic that never converts and expensive clicks can be high-intent buyers.
- Recognize that CPC and ROAS show very little relationship across large datasets, both at account and product level, in the source's analysis.
- Keep only the peripheral extremes in mind: CPCs around $100 are almost certainly unprofitable, and CPCs around 10 cents are probably junk traffic.
- Instead of chasing CPC, improve bidding quality by feeding the algorithm better conversion signals, quality score inputs and feed data so it bids on users likely to convert.
- Measure success with ROAS and revenue per visitor rather than CPC movement.
Caveat: The source presents this as a pattern observed across many accounts, not a formal benchmark; verify against your own account data.
Caveat: This does not mean CPC is irrelevant in the extreme; extreme CPC levels still indicate a problem.

Tags: google-ads, measurement, cost-per-click, acquisition, reporting
Source: The Only Google Ads Strategy You Need for 2026.docx

---

## Win More Google Auctions by Raising Your Website's Conversion Rate
Use when: Deciding where to invest to improve Google Ads performance when campaign settings have already been refined.
- Frame the auction logic: you and competitors bid on the same term, and whoever can pay the most wins the listing, the click and the conversion.
- Accept that higher conversion rate is your lever to afford higher bids: if you convert twice as well as competitors, you can pay double per click and make the same money.
- Apply the same logic to average order value: higher AOV extracts more revenue per click, so you can outbid competitors on the same traffic.
- Use campaign structure, asset groups, audience signals and feed optimization to improve quality score so your bid effectively enters the auction lower than competitors'.
- Recognize the counter-risk: a competitor with better conversion rate and AOV can outbid you even with worse ads and structure, so on-site performance ultimately caps what campaign work can achieve.
Caveat: The doubled-conversion-rate example is an illustration of the auction mechanic, not a promise of results.
Caveat: Without products and site improvements this advantage cannot be sustained.

Tags: google-ads, conversion-optimization, auction, acquisition, landing-page
Source: The Only Google Ads Strategy You Need for 2026.docx

---

## Run Continuous Landing Page Split Tests on Search Ads
Use when: Running Search campaigns and looking for the biggest lever beyond in-platform settings: improving the landing page conversion rate.
- Duplicate the ad in each ad group so ad one points to landing page one and ad two points to landing page two.
- Keep the ads otherwise identical so the landing page is the variable under test.
- Measure conversion rate over a 30-60 day period to give each page enough data.
- Select the landing page with the higher conversion rate and make it the default.
- Immediately start a new test: bring in landing page three as the challenger and compare it against the current winner.
- Repeat the cycle so the campaign's average conversion rate rises over time, which raises the amount you can afford to bid.
- Where possible, also test AOV improvements so revenue per visitor from the campaign rises alongside conversion rate.
Caveat: The 30-60 day window is the source's guidance; lower-traffic ad groups may need longer or may not reach significance.
Caveat: The source calls landing page testing one of the biggest levers in Search, but this is their opinion based on agency experience, not a measured benchmark.

Tags: google-ads, search-ads, landing-page, conversion-optimization, experiment-design
Source: The Only Google Ads Strategy You Need for 2026.docx

---

## Change Google Ads Budgets Slowly, Downward Faster
Use when: Scaling or pulling back spend on Google Ads campaigns after a winning period, or planning a promotion push.
- Increase Google Ads budgets in roughly 20% increments rather than doubling overnight; the source reports Google is a stable platform that responds badly to heavy budget changes.
- Apply the same caution to bidding target changes: do not move target CPA or target ROAS overnight.
- When reducing budgets from a high level, you can generally move faster with little instability or performance drop-off observed.
- Treat other platforms differently: on Meta and TikTok you can increase budgets considerably faster than the Google 20% guideline.
- Plan around the general principle that Google drives conversions consistently and wants slower, methodical changes, while other channels tolerate aggression.
Caveat: The 20% increment is a widely repeated heuristic that the source confirms holds on Google specifically; it is not a calculated optimum.
Caveat: Observed behaviour can change as the platform updates; validate on your own account.

Tags: google-ads, budget-allocation, scaling, bidding-strategies, acquisition
Source: The Only Google Ads Strategy You Need for 2026.docx

---

## Interpret 'Limited by Budget' as a Signal, Not a Rule
Use when: Deciding whether to raise campaign budgets when Google Ads reports campaigns are limited by budget.
- Read the flag as an indicator that the campaign could have entered more auctions if budget were available.
- Do not treat it as proof that additional spend will be profitable; the source reports seeing it on nearly every account, even campaigns spending $5,000-$10,000 a day in a small total addressable market.
- Investigate incremental spend by checking whether adding budget actually improves revenue and ROAS over a test period rather than accepting the flag at face value.
- Combine the signal with other diagnostics: conversion volume trends, auction insights and marginal ROAS.
- If incremental budget does not improve returns, leave the budget as is despite the flag.
Caveat: Google's flag behaviour is the platform's own reporting and may change over time; verify current semantics.
Caveat: Small total addressable markets can still show the flag even at very high spend, per the source's example.

Tags: google-ads, budget-allocation, scaling, measurement, account-audit
Source: The Only Google Ads Strategy You Need for 2026.docx

---

## Stagger Feed Title Rollouts to Protect Learning
Use when: Applying Google Merchant Center title, image or attribute changes across a catalog with active Shopping and Pmax campaigns.
- Prioritize the highest-opportunity products or categories rather than the whole catalog at once.
- Change a batch of titles, then watch campaign response before moving to the next batch.
- Monitor click-through rate, CPC and return on spend for the changed listings in real time to see if the changes made a material difference.
- Stop and redesign the keyword approach if results do not improve; test different researched keywords in titles instead.
- Keep the baseline recorded so you can compare before and after the change.
- Remember that a bulk switch resets learning phases on every campaign, which can put the account in a bad position.
Caveat: There is no fixed batch size; pace depends on catalog size and campaign volume.
Caveat: Feed changes can take time to propagate, so allow time before judging results.

Tags: google-ads, google-merchant-center, product-feed, product-titles, experiment-design
Source: The Only Google Ads Strategy You Need for 2026.docx

---

## Optimize Shopping Images for Contrast, Not Just CTR
Use when: Improving Google Shopping listing creative to lift click quality, not just click volume.
- Recognize the image dominates the listing, with price and title as secondary click drivers, so image work is high leverage.
- Aim for the right clicks rather than maximum CTR: if you attract the wrong people, higher CTR does not help, mirroring the idea that a headline should hook the right reader, not everyone.
- Study the listings you appear beside and build contrast, for example keeping a photo shoot but changing the background colour if competitors all use white backgrounds.
- Supply images in the ratio Google expects, about 4x5, and override feed images via a supplementary feed if your defaults, such as fashion's 9x6, get autocropped badly.
- Where brand recognition is limited, focus on visual differentiation rather than brand-led creative.
- Review click-through and conversion quality together after image changes to confirm you attracted buyers rather than browsers.
Caveat: The 70% real estate figure and 4x5 ratio are stated by the source and platform defaults may change; verify current Merchant Center image requirements.
Caveat: Higher CTR alone is not the goal; validate with conversion and return data.

Tags: google-ads, shopping-ads, product-feed, creative-strategy, google-merchant-center, product-images
Source: The Only Google Ads Strategy You Need for 2026.docx

---

## Set Up Separate Merchant Center Feeds per Currency
Use when: Selling to international customers through Google Shopping and reviewing your Merchant Center feed setup.
- Audit whether multiple countries or currencies are running through a single feed with one currency.
- Create a separate feed for each different currency so listings display prices in the local currency.
- Check how your current listings appear in each market; a live conversion label such as converted from AUD or USD plus tax signals a buyer that they are purchasing from an international store.
- Fix the feed rather than relying on the platform's automatic conversion display, since that label suppresses clicks and conversions.
- Review other basic feed attributes and descriptions at the same time, as this cleanup is largely a one-time setup.
Caveat: The source frames this as a common audit finding, not a measured CTR benchmark.
Caveat: Currency and localization requirements in Merchant Center change; verify current documentation before restructuring feeds.

Tags: google-ads, google-merchant-center, product-feed, international, localization, conversion-optimization
Source: The Only Google Ads Strategy You Need for 2026.docx

---

## Audit Responsive Search Ads for Learning Starvation
Use when: Structuring Search campaigns and RSAs for an account with limited impression volume.
- Note the arithmetic: a responsive search ad has roughly 2,700 possible asset combinations at setup.
- Assume a very low 100 impressions to judge one combination, which still implies about 270,000 impressions to exit learning and know which combinations work.
- Reduce segmentation accordingly, since every extra campaign and ad group fragments impressions and prolongs learning.
- Work toward one campaign unless there is a genuine commercial reason, such as splitting brand from non-brand, for each added campaign.
- Accept that in most accounts RSAs stay in learning indefinitely, and plan structure and expectations around that reality.
Caveat: The 2,700 combinations and 100-impression assumption are the source's illustrative arithmetic; the source itself says 100 impressions is too little data to judge.
Caveat: Low-volume accounts may never exit learning regardless of structure.

Tags: google-ads, search-ads, responsive-search-ads, campaign-structure, experiment-design
Source: The Only Google Ads Strategy You Need for 2026.docx

---

## Follow a 90-Day Google Ads Implementation Sequence
Use when: Onboarding a new Google Ads account or planning a quarter of work on an existing ecommerce account.
- Fix tracking first: ensure conversion events are firing correctly with no duplicate or stale tags, enhanced conversions and auto-tagging are on, and everything is up to standard.
- Build a structure map: decide how many campaigns you need, starting from one and requiring a commercial reason for each addition, such as brand versus non-brand, and apply consistent naming.
- Run a Pmax-specific check: asset groups split by product type, listing groups split out, brand exclusions on, audience signals present, and a target ROAS that is not so high the campaign functions only as retargeting.
- Confirm the bidding strategy matches your intent using the expansive versus restrictive framework.
- Audit for wasted spend: kill tiny campaigns that can be rolled up, add negatives for unprofitable search terms, and turn off display on Search campaigns if enabled.
- Health-check ad assets: sitelinks, call ads, current promos, and maximise assets in every campaign to increase ad real estate.
- Finish with a feed check on titles, images and remaining attributes, rolling changes out slowly rather than all at once.
Caveat: The 90-day framing is the source's suggested rollout, not a fixed requirement; pace depends on account size and budget.
Caveat: Specific settings and feature locations in Google Ads change frequently; verify each step in the current interface.

Tags: google-ads, account-audit, implementation, tracking, campaign-structure, product-feed
Source: The Only Google Ads Strategy You Need for 2026.docx

---

## Exclude Brand Traffic and Use Smart Bidding on Search
Use when: Setting up or auditing Search campaigns in an ecommerce account.
- Set brand exclusions on Search campaigns so branded spend does not inflate Search performance.
- Choose a smart bidding strategy such as target ROAS or max conversions rather than manual CPC or maximize clicks for established accounts.
- Reserve manual CPC or maximize clicks for new accounts without conversion data, where smart bidding may not be available, and move off them as soon as possible.
- Recognize that an agency may occasionally run maximize clicks as a deliberate arbitrage test, but this is rare and should not be the default for most accounts.
- Review whether any Search campaign is entering branded auctions you did not intend, and correct the exclusion settings.
Caveat: Smart bidding availability for new accounts depends on accumulated conversion data and may change over time.
Caveat: Portfolio bid strategies can also carry brand exclusions and other settings; check where exclusions are applied.
Caveat: The source works mainly with established businesses, so their default advice may not fit brand-new accounts.

Tags: google-ads, search-ads, brand-exclusions, bidding-strategies, account-audit
Source: The Only Google Ads Strategy You Need for 2026.docx