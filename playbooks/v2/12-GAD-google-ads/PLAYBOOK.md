# 12-GAD Google Ads playbook

version: 2.0-draft  |  date: 24 Sep 2026  |  sources: 10 mini playbooks (9 independent; 06 and 09 count as 1 weak source)  |  cards: 362  |  built from: sources/*.md

## 0. How to use this playbook

Who runs it: the Google Ads performance agent. It recommends; a human applies every write to Google Ads, Merchant Center, GTM or the site. Meta rules in CLAUDE.md apply here too: no ad-account writes without a human, no credentials in output, arithmetic in code.

Load by task:

| Task | Load |
|---|---|
| New account or audit of an existing one | 1, 2, 3 (all), 5.3 structure audit, 9 |
| Conversion tracking setup or check | 3.B, 4.1 to 4.4, 5.1 |
| Merchant Center, feed, suspension risk | 3.C, 3.D, 4.5 to 4.8, 5.2 |
| Campaign build (brand, Shopping, Search, PMax, Demand Gen) | 3.E to 3.J, 4.9 to 4.20 |
| Bidding and budgets | 3.K, 3.L, 4.21, 4.22, 6 |
| Scaling decision | 3.N, 4.23, 5.6 |
| Account is underperforming | 3.O, 4.25, 5.7 |
| Daily, weekly, monthly care | 4.24, 5.4 |
| Any decision where sources disagree | 7 |

Before acting, the agent fetches: brand record (AOV, contribution margin per order and per SKU, break-even ROAS and CPA, repeat rate, brand name variants, countries, shipping and returns terms, offers); data layer (Google Ads spend, conversions and value by campaign for 90 to 180 days, search terms, product-level spend, Merchant Center diagnostics, backend orders by day, new vs returning split); web (current Google Ads and Merchant Center UI, PMax vs Standard Shopping serving rule, PMax channel report, Demand Gen placements). Section 10 lists every item.

Every platform step below carries `[verify UI]`. The 10 sources were recorded between late 2024 and September 2026. Menus, bid strategy names and PMax controls change often.

## 1. Scope and outcomes

Covers: Google Ads for ecommerce stores. Conversion tracking and Merchant Center setup, feed and title rules, account architecture (Shopping, Search brand and non-brand, Performance Max, Demand Gen, YouTube, Display remarketing), bidding by stage, budgets, negatives and exclusions, PMax mechanics, scaling gates, the diagnostic order for an underperforming account, operating routines, and suspension avoidance.

Does not cover: ad creative craft for video and static (10-MCR); Meta, TikTok and multi-platform deployment (24-DEP); site CRO, landing page testing detail and MMM or incrementality design (06-MEA, 07-LPG, 09-CRO); SEO and product data outside the feed (15-SEO); offer design in depth (offer folder). Where a source gives a Google-specific version of those topics (cold-search landing pages, YouTube hook structure), it stays here as the lever the source names.

Business measures it moves: new-customer revenue and new-customer CPA; blended MER; non-brand ROAS on its own; brand impression share; share of budget going to cold traffic; Merchant Center approval rate and suspension risk; Google share of total revenue (source 01 gives 20% to 30% as a healthy range, opinion).

## 2. Inputs the agent needs

| Input | From where | Required or optional | Why |
|---|---|---|---|
| AOV, contribution margin per order (after COGS, shipping, fees, returns), margin by SKU or collection | Brand record | Required | Break-even ROAS and CPA; margin-tier structure; budget sizing (3 to 4x AOV) |
| Repeat rate and cohort revenue at 30, 60, 90, 180, 365 days | Brand record or data layer | Optional, required for LTV-based targets | Sets how far below first-order break-even the brand may buy |
| Brand name, misspellings, brand plus product phrases | Brand record, search terms | Required | Brand campaigns, brand negatives, brand exclusion lists |
| Countries sold to, currencies, languages | Brand record | Required | 1 campaign per country; 1 feed per currency; Presence targeting |
| Current offers, shipping threshold, returns window, couriers | Brand record | Required | Ads, promotions, Merchant Center policies must match the site |
| Approved claims and proof | Brand record | Required | Feed descriptions and ads; misrepresentation risk |
| Google Ads: spend, conversions, value by campaign, 90 to 180 days weekly | Data layer | Required | Structure audit, diagnosis, thresholds |
| Search terms (Search, Shopping, PMax) with cost and conversions | Data layer | Required | Negatives, brand leakage, title keywords, new Search campaigns |
| Product-level spend, clicks, conversions, value | Data layer | Required | Hero products, zombies, tiers, exclusions |
| PMax channel or placement split, asset group results | Data layer | Required when PMax runs | Drift, feed-only check |
| New vs returning customer split by campaign | Data layer (Google native new-customer metrics, Triple Whale, Northbeam or similar) | Optional, strongly preferred | PMax warm-share check, tROAS narrowing check |
| Backend orders and revenue by day | Data layer (Shopify, Metabase) | Required | Tracking reconciliation; MER; latency check |
| Merchant Center diagnostics, product status, store quality score | Data layer or user screenshot | Required | Feed health, suspension risk |
| Spend by platform (Meta, Google, others) and MER | Data layer | Required for diagnosis | Level 1 of the diagnostic order |
| Change history (Google Ads, Meta, site, promo calendar) | User | Required for diagnosis | Rule 1 of pre-diagnosis |
| Winning Meta creatives, reviews export, founder story | Inspiration, brand record | Optional | YouTube creative; ad copy angles |
| Competitor bidding on the brand name; competitor prices on shared SKUs | Web | Optional | Brand campaign decision; Shopping CTR drops |
| Current Google UI, PMax serving rules, Demand Gen placements, Merchant Center limits | Web | Required before any build | Every `[verify UI]` and `[web check]` |

## 3. Decision rules

Format: rule, condition, sources by mini playbook number, cards. "Conflict" points to section 7. Where only 1 source says it, the rule says so. 06 and 09 are cited as "06/09" and count as 1 weak source.

### 3.A Readiness and unit economics

**R1. Do not scale Google until the offer, the page and the message are proven.** Condition: no product-market fit, no converting page, or no proven angle. Then set up only tracking, Merchant Center, brand campaigns and 1 Shopping campaign; test the offer elsewhere (source 01 says on Meta). Google captures demand; it does not create it (except YouTube). Sources: 01, 08 (a campaign that fails at low budget fails on offer or ads, not budget). Cards: [447589198c09] [f4ea91fcade1] [af051bd7984a]

**R2. Work in this order: offer, landing page, unit economics, goals and KPIs, tracking, structure, targeting, creative, bids and budget last.** Condition: any new build or rebuild. Source 01 says most owners start with bids and budget. Sources: 01, 04 (90-day order: tracking, structure, PMax check, bidding, waste, assets, feed), 06/09 (fix inputs before outputs). Cards: [fa9689ea4d16] [4c549b970082] [2792071d2d2e] [abc2dfeeea38] [daa2070d28bf]

**R3. Know break-even ROAS and break-even CPA before any bid or budget decision, and compute them from contribution margin, not gross margin.** Formulas: break-even ROAS = 1 / contribution margin (40% margin gives 2.5); break-even CPA = AOV x contribution margin ($100 x 40% = $40). Condition: every account. Sources 01, 08 and 06/09 use gross margin; ecomOS uses contribution margin after COGS, shipping, payment fees, fulfilment and returns (card 7f0f4a47add4 already rewrites it that way). Conflict 7.8. Sources: 01, 08, 06/09, 04 (Google is blind to margin), 10 (PMax does not know margins). Cards: [7f0f4a47add4] [efe781ef33f1] [37a75be509aa] [a715afa0c38a] [3fec1d2be46d] `[needs brand data: contribution margin per order and per SKU]`

**R4. Set ROAS targets from margin, never from industry benchmarks.** Condition: always. A 60% margin brand can scale at a lower ROAS than a 25% margin brand. Sources: 06/09, 01, 10. Cards: [37a75be509aa] [7f0f4a47add4] [3fec1d2be46d]

**R5. Buy new customers at or slightly under first-order break-even, and let the back end make the profit, only when the brand has real retention data.** Condition: repeat-purchase product, measured cohort LTV, email and SMS flows in place. Source 01: with strong LTV go to about 0.8x first-order ROAS and recover within 12 months. Source 08: if LTV doubles, a 1.5x or even 1.2x ROAS floor can become acceptable; scale CPA allowance by LTV but check margin on repeat orders. Without retention data, stay at or above first-order break-even. Sources: 01, 08. Cards: [e97aeff823a5] [3335ab579d2a] [4478e71195a6] [ef1555c15a96] [af051bd7984a] `[needs brand data: cohort revenue and margin at 30/60/90/180/365 days]`

**R6. Raise AOV before cutting COGS or chasing a small CPA cut.** Condition: AOV under about $100. Bundles, buy 1 gift 1, add-ons, spend thresholds framed as "shipping's on us" (source 01), dollar-off offers above about $100 AOV. Source 08: an AOV over $100 makes profitable ads "much easier"; $120 AOV at 10% margin leaves $12 per order. Sources: 01, 08. Cards: [3335ab579d2a] [f4ea91fcade1] [efe781ef33f1] [ef1555c15a96]

**R7. Judge the channel on MER and backend revenue, not on in-platform ROAS.** Condition: always, and most of all when PMax or brand campaigns run. Overspend pattern: Google sits at the bottom of the funnel, reports high ROAS, and gets more budget without moving backend revenue. Underspend pattern: Google capped as "bottom funnel only" in a category with real cold search demand. Sources: 01, 04, 05, 08. Cards: [e97aeff823a5] [7f0f4a47add4] [fb0673e2ae6d] [7fe2bb1f5bff] [d7752a494148] `[needs brand data: total revenue and total marketing spend by week; Google spend vs backend revenue over time]`

**R8. Conversion rate and AOV decide who can afford to win the auction.** Condition: any Search or Shopping auction. A 2x conversion rate lets you pay 2x per click for the same profit. In-platform work lowers your effective bid; a competitor with better conversion rate and AOV can still outbid you. So landing page and offer tests are Google levers. Sources: 04, 07 (relevance and beta), 06/09. Cards: [78d712129ebc] [bd9b251ac5b1] [bf7fb09f077f] [1267e0489b18]

**R9. Discount with a plan.** Condition: mid-market brands. Discount only high-margin products, gate discounts behind a spend threshold, or give an inexpensive free item with a high-margin purchase. Lowest-price brands lean into discounts. Premium brands give extras, not price cuts. Check gross profit during the sale, not volume. Source: 08 only. Cards: [38b728817a44] [5632d9d930a2]

**R10. Mine reviews for ad copy and feed copy angles.** Condition: any brand with reviews; with none, read competitor reviews and use only claims true for your product. Sources: 08, 01 (AI research workflow). Cards: [082b2980e92f] [a9aae4ff1aef] [52816ff36204]

### 3.B Conversion tracking

**R11. Fix conversion tracking before anything else.** Condition: always. Without it the advertiser and Smart Bidding "fly blind". Sources: 01, 02, 03, 04, 06/09, 08. Cards: [fff2f5c0c47c] [2b368492270c] [d9dc799b0bcb] [2792071d2d2e] [535e56dd51f1] [d7752a494148]

**R12. Exactly 1 primary purchase action per account; purchases only as primary; everything else secondary (observe only).** Condition: always. 2 primary purchase actions double revenue and ROAS on paper (source 02 calls it the worst of 3 cardinal sins). Add to cart, begin checkout, page view, view item and search stay secondary and out of account default goals. Sources: 01, 02, 03. Cards: [30fdf39203d6] [a3831e8b2c64] [fff2f5c0c47c] [634ed94f1328] [d9dc799b0bcb] [535fcd04bd8b]

**R13. Optimise every ecommerce campaign to purchase, not add to cart or clicks.** Condition: 99% of cases (sources 01, 02, 03). Exception in source 02: product at $10k to $15k with 8 to 20 conversions a month may optimise to add to cart and remarket. Sources: 01, 02, 03. Cards: [3335ab579d2a] [30fdf39203d6] [d9dc799b0bcb]

**R14. Do not use the GA4 import as the primary purchase action.** Condition: always. GA4 under-counts Google Ads conversions by about 20% (source 02) or 10% to 15%, sometimes more (source 04) versus the Google Ads tag with enhanced conversions and auto-tagging. Keep GA4 as a secondary backup. Sources: 02, 04. Cards: [30fdf39203d6] [a3831e8b2c64] [18f7a08a224c] [2792071d2d2e]

**R15. Turn on enhanced conversions and pass real order revenue (discounts and shipping included), never a fixed value.** Condition: always; matters most where purchase volume is low. A fixed value degrades tROAS. Sources: 01, 02, 04, 06/09. Cards: [fff2f5c0c47c] [30fdf39203d6] [2792071d2d2e] [80d2cbcc7a96] [24d517dd8fe0] [f866b580a9ae]

**R16. Use the Shopify Google and YouTube app as the fast route, GTM as the robust route, server-side above about $50k a month.** Condition: Shopify store. Source 02: the app gets you 80% to 90% of the way. Source 01 gives the GTM plus Shopify custom pixel build. Source 06/09 says server-side GTM is "increasingly the default" above $50k a month (heuristic). If both app and GTM purchase actions exist, keep only 1 primary. Sources: 01, 02, 06/09. Cards: [93f8e8d57251] [2b368492270c] [fff2f5c0c47c] [535e56dd51f1] [966cf63d89ec] [56853873c2c8]

**R17. Set conversion windows to match the purchase cycle and check against Shopify, do not just take the maximum.** Condition: always. Source 01 sets click 90 days, engaged view 30, view-through 30, data-driven attribution. Longer windows raise reported conversions. Source: 01 only, with the ecomOS caveat. Cards: [fff2f5c0c47c] `[needs brand data: time from first click to purchase]`

**R18. Track new customers separately: a first-order conversion event, or a third-party new-customer CPA, not Google's customer acquisition bid setting.** Condition: any account that reports new-customer growth. Source 01 keeps the all-purchase action, adds a first-order event as primary (or keeps it secondary and reads new-customer CPA in Triple Whale or Northbeam), and leaves the "customer acquisition" setting off. Source 05 reads new-customer ROAS natively or in Triple Whale. Sources 02 and 03 leave the customer acquisition setting at default or off. Sources: 01, 05, 02, 03. Cards: [a336449b068e] [69caeee85e5f] [4e3675b7a020] [8e83ab723ce9] [4b15db679fc4] `[web check: native new-customer metrics and how to detect first orders in Shopify customer events]`

**R19. Read recent days on "conversions by conversion time", not default columns.** Condition: any read of the last 3 to 7 days. Google credits a conversion to the click date, so the last 3 to 4 days (often 7) always look bad on default columns. Add the ROAS-by-time custom column (conversion value by conversion time / cost). Sources: 02, 05. Cards: [d2bb52998ad7] [0cdf0df9c538] [62403f6f3b48] `[verify UI]`

**R20. Use 1 master Google account that owns Google Ads, Merchant Center and Analytics.** Condition: new setup. Source: 02 only. Cards: [52efc5146531]

**R21. Reconcile Google-reported purchases with backend orders.** Condition: after setup and monthly. No source gives a numeric match threshold. Sources: 01, 06/09, 08. Cards: [fff2f5c0c47c] [56853873c2c8] [d7752a494148] `[needs brand data: Shopify orders vs Google Ads purchases for the same days]`

### 3.C Merchant Center setup and suspension avoidance

**R22. Merchant Center is required for Shopping, PMax with products, Demand Gen with feed and dynamic remarketing. Skip it only for gray-hat, non-compliant or heavy dropshipping stores that would get banned.** Condition: the store has real policies and a brand experience. Sources: 01, 02, 03. Cards: [78000b7f5684] [911db04602d6] [a0825cabc944]

**R23. Business info, shipping, returns and contact details in Merchant Center must match the website exactly.** Condition: always. Mismatches are the top suspension trigger (source 01: "Google are ruthless with this"; a client who changed courier and did not update Merchant Center was down about a week). Set the Shopify shipping sync to manual so Shopify changes do not silently create mismatches. Name couriers. Link directly to the returns policy page. Sources: 01, 02. Cards: [bb3574f9e67a] [7255257382d0] [9de75b008814] [911db04602d6]

**R24. Enrol the 4 add-ons: dynamic remarketing, Google customer reviews, product ratings, promotions.** Condition: new Merchant Center. Product ratings need 50 reviews in total and at least 3 per product to show; expect 2 to 4 weeks. Judge.me syncs through Shopify; Trustpilot and Stamped are official aggregators. Sources: 01, 02. Cards: [5fa36e157a58] [69bd2ba35622] `[web check: current product ratings thresholds]`

**R25. Never edit price, availability or sale price in Merchant Center; change them in Shopify so the feed matches the site. Never change the product ID.** Condition: always. Price on page = price at checkout = price in feed. Sources: 01, 06/09 (price mismatch is a top disapproval cause; refresh the feed at least every 6 hours when prices change often and turn on automatic item updates). Cards: [c32fb2d0de63] [61f93049590a] [82e55ef4dd25] [9972bf6ca8cf]

**R26. Fix disapprovals first, then warnings and limited performance.** Condition: weekly, and after any drop in eligible products. Disapproved items cannot serve anywhere. 5 common causes: missing or wrong GTIN, price mismatch, missing shipping info, policy violation, formatting or missing required attributes. Autofix only formatting and optional attributes; fix policy and price by hand. Sources: 01, 02, 06/09. Cards: [5157f5f5a687] [911db04602d6] [82e55ef4dd25] [9972bf6ca8cf]

**R27. Run the anti-suspension checklist (34 items in source 01) on a schedule: payment methods work, prices and tax shown before payment, discount codes work, no exaggerated claims, real reviews, out of stock shown as sold out, no broken links, policies in the footer, branded email, phone line, SSL sitewide, no default theme, no dead apps.** Condition: always; misrepresentation is "the biggest thing that hits brands", most of all in health. Source: 01 only for the list; 02 adds promotions must match the site exactly or get rejected. Cards: [95550c2e178c] [eea0c9ae49af] [a9d854c2d98d] [173c252bafd5] [f7f63ab97480] [8ff6407379e3] [c9b580a81edf] `[web check: Google misrepresentation and healthcare policies for the category]`

**R28. Work toward the Top Quality Store badge.** Condition: Merchant Center account. Categories: browsing (high-res main image plus 8 to 10 more, load under 2 seconds), purchase (promotions match site, several e-wallets), shipping, returns (30 days or more), store rating. Source 02 reports at least a 20% lift when the badge lands (agency observation). Source 01 aims for "exceptional" on the scorecard. Sources: 01, 02. Cards: [8a99ccae1285] [c9b580a81edf]

**R29. Do not claim the "small business" identity attribute or any other attribute unless it is true by Google's definition.** Condition: US business info. Source 01 recommends claiming it for any company under $40M; ecomOS rejects that without a check. Cards: [bb3574f9e67a] `[web check: Merchant Center small business attribute definition]`

### 3.D Feed, titles, images, descriptions

**R30. In Shopping and PMax the feed is the targeting. Price, title and image drive about 95% of Shopping performance.** Condition: any feed-led campaign. Source 02: spend 95% of feed time on these 3; price matters most because Shopping is a comparison surface. Source 04: image takes about 70% of the listing and drives the click. Source 07: titles and descriptions matter most. Sources: 01, 02, 04, 06/09, 07. Cards: [21229935ad81] [1f2977dd9a2c] [3cce923d11c9] [a1c3cff78bf2] [829c77305316] [c7807eeedee7] [7671c6e57a6e] [f3d645adbbbe]

**R31. Titles lead with the converting search term and product type, then attributes; brand goes last for small brands and first only for a known brand.** Condition: default for most DTC brands. Attribute order from the sources: highest-volume converting keyword plus product type, variant details (colour, size, capacity, material, dosage, use case), second keyword or USP, brand last (source 01: brand first if you are a big brand; source 06/09: fashion, electronics and seasonal alternatives put brand first). Keep 1 attribute order across the catalog. Keywords come from the search term report of what converted, never invented. Conflict 7.3. Sources: 01, 02, 03, 04, 06/09, 07. Cards: [3cce923d11c9] [b5af5e150e67] [6126c42680a9] [35ccb3d32bf5] [0d729814ee30] [a1c3cff78bf2] [9983e71e8efc] [76f0f732dbe5] [afd1fd903f18] `[needs brand data: search terms with conversions by product type]`

**R32. Title length: keep every title between 60 and 150 characters; put the searched attributes in the first 70.** Condition: all SKUs. Source 01 says 130 to 150; source 02 says up to 150 with the first 70 visible; source 06/09 says 60 to 150, aim about 120, first 25 to 30 most important. Merged rule keeps the strictest window (first 70) and the widest allowed range. Sources: 01, 02, 06/09. Cards: [3cce923d11c9] [b5af5e150e67] [9983e71e8efc] [76f0f732dbe5] `[web check: current Merchant Center title character limit]`

**R33. No keyword stuffing, no promotional text, no wrong attributes in titles or descriptions.** Condition: always. Source 07 says to "stuff" keywords; its own cards and every other source say keep titles readable and attributes true. Source 03: an "aluminum pan" description on a non-aluminium pan sends the wrong searches. Source 01: descriptions about 1,000 characters, keywords front-loaded, features, USPs, a CTA, no promotional text (policy). Source 02: up to 5,000 characters, answer buyer objections, brief. Sources: 01, 02, 03, 06/09, 07 (cards). Cards: [f74643a53f4d] [e58f1b803e0f] [27a887849ed2] [9983e71e8efc] [f3d645adbbbe] `[web check: Merchant Center description limit and keyword stuffing policy]`

**R34. Roll title changes out in batches, highest-opportunity products first, with a recorded baseline; never switch all titles at once.** Condition: any title rewrite on a live account. A bulk switch resets learning on every campaign (source 04). Watch CTR, CPC and returns per batch. Use a supplemental feed to override titles without touching the site (source 06/09). Sources: 04, 06/09. Cards: [18d6b809b70b] [2792071d2d2e] [59d9f9d20e0c] [76f0f732dbe5]

**R35. Images: high resolution, product as the main subject, no text overlays, and test lifestyle or elevated backgrounds against plain white.** Condition: all SKUs. Text overlays (sale stickers) are a policy violation. Source 02 reports lifestyle wins about 90% of its CTR tests; source 01 found the plain product shot worked for its brand; source 04 says build contrast with the listings you appear beside. Source 04: supply 4:5 images by supplementary feed if auto-cropping hurts. Source 07: vary avatar images across duplicates (see R38). Sources: 01, 02, 04, 07. Cards: [eeaaed11a13b] [d633238d5060] [24a69e143936] [829c77305316] [2dd030a32711] `[web check: Merchant Center image policy and recommended aspect ratio]`

**R36. Every variant needs its own GTIN; each variant listing can target its own keyword pool.** Condition: variants create separate listings. Sources: 02, 04, 01. Cards: [21229935ad81] [a1c3cff78bf2] [61f93049590a]

**R37. Use custom labels to carry margin tier, bestseller status, seasonality and inventory priority into campaign structure.** Condition: catalog with mixed margins or performance. The most useful split separates high-ticket or high-margin SKUs from low-margin ones. Sources: 01, 06/09, 10, 04 (labelizer tiers for thousands of SKUs). Cards: [61f93049590a] [59d9f9d20e0c] [9a7b30ebd79d] [3fec1d2be46d] [e2e3fde986ec]

**R38. Do not duplicate the same product at several prices to hold more slots.** Condition: source 07's "surface area scaling". It risks duplicate-product, price-accuracy and misrepresentation problems, and needs a brand-level pricing decision. Real tiered variants with different images and titles are fine. Source: 07 only for the tactic; its own cards warn against it. Cards: [fe7e30671299] [2dd030a32711] `[web check: Merchant Center duplicate product and misrepresentation policies]`

**R39. 1 feed per currency.** Condition: selling in more than 1 currency. A converted-price label kills CTR and conversion rate. Source: 04 only. Cards: [d68cec537fb6] `[web check: current multi-country feed setup]`

**R40. Negatives are a plaster; the feed is the cure.** Condition: a product shows for poor queries. Add the negative, then fix the title and description that caused the match. Sources: 02, 01. Cards: [25c967c6e637] [a223f5b65ca8]

### 3.E Account architecture and launch order

**R41. Google is 4 ad surfaces: Search, Shopping, YouTube (Demand Gen), Display. Shopping is the core for ecommerce and gets the largest share.** Condition: consumer ecommerce. Source 01: Shopping is 60% to 80% of ecommerce Google ads; source 04: 80% to 90% of spend in Shopping, Search only after Shopping saturates; source 02: Shopping is "the bread winner"; source 03: Shopping is the core and non-brand Search is secondary; source 10: Shopping gets "the lion's share"; source 07: Search plus Shopping make 99% of revenue, most from Shopping. Exception (source 04): ecommerce with a B2B or bulk component, where Search can beat Shopping. Sources: 01, 02, 03, 04, 07, 10. Cards: [c38dea49205d] [911db04602d6] [bca4ccb4fceb] [0faae8bbc52a] [30bbbd9532ea] [08b3d9f85868] [cc19e5a055f2]

**R42. Launch bottom of funnel first: branded Search, branded Shopping and 1 non-brand Shopping campaign, then remarketing and PMax, then Demand Gen or YouTube.** Condition: new account or new brand on Google. Source 01: phase 1 (30 to 60 days) brand Search, brand Shopping, 1 prospecting Shopping on manual bidding; phase 2 (months 2 to 6) smart bidding, PMax, YouTube; phase 3 (after 6 months) scale. Source 03: step 1 Search and Shopping, step 2 remarketing (Video, Display or PMax) after about 4 to 6 weeks of data, step 3 Demand Gen once bottom and mid funnel are saturated. Source 02: Search and Shopping first, mostly Shopping; PMax and Demand Gen after they work; YouTube last. Source 08: Search and Shopping, PMax after about 100 purchases. Exception (source 03): a large account with proven Meta creatives may bring Demand Gen in at step 2. Exception (source 01): Meta-heavy direct response brands with no category search demand put about 80% into Demand Gen from the start. Conflict 7.1. Sources: 01, 02, 03, 08. Cards: [4aee86b1351f] [a2427f18e5fe] [9f22aab00a78] [224802f88324] [b6530a0cdc65] [b7bf73d92363] [575bdc0721ef] [78000b7f5684]

**R43. Every campaign has 1 funnel job; check each campaign against the role map.** Roles: non-brand Shopping and PMax (with brand excluded) acquire new customers; brand Search and brand Shopping capture branded demand and block competitors; non-brand Search takes high-intent and problem queries; Demand Gen or YouTube creates demand; Display or Demand Gen remarketing converts visitors; dynamic remarketing ties it together. 2 campaigns chasing the same traffic is a structure fault. Sources: 01, 03, 06/09, 10. Cards: [188ae31b3990] [3aeb15c6850e] [0cc26b9c7f70] [07a456f35774] [013bd9d69456] [61d89a7caa36] [10c2368513b5]

**R44. Default to 1 campaign per job; every extra campaign needs a written reason.** Reasons that justify a split: brand vs non-brand; country; different margins or efficiency goals; product categories that learn toward different personas; a stated commercial need (clearance stock, new arrivals, an underfunded bestseller). Campaigns learn mostly in isolation, so 3 campaigns with the same products at 50, 20 and 10 conversions a month bid worse than 1 at 90. Source 02: brands at $50k to $500k a month rarely have the traffic for heavy segmentation. Source 07: aim as close to 1 campaign as possible. Sources: 01, 02, 04, 07. Cards: [329599511dc8] [96fdc15f1d9a] [4995c5440e92] [4692423b2426] [379b1f714127] [a715afa0c38a] [e5ab20feaa14] [568c59a75126] `[needs brand data: margin by collection, countries, category list, aged stock]`

**R45. 1 campaign per country. Never 2 locations in 1 PMax.** Condition: multi-country. Sources: 01, 04. Cards: [329599511dc8] [a715afa0c38a]

**R46. Split by margin or efficiency goal when margins differ a lot.** Condition: product margins spread widely (source 10 example 30% vs 70%; source 04 example 70% vs 35% at a 300% target). High-margin tiers get a lower ROAS target; low-margin tiers a higher one. Source 10: if margins are within about 10% of each other, tier by past ROAS and spend instead (high ROAS, low ROAS, low spend, zombies). Sources: 04, 10, 06/09. Cards: [a715afa0c38a] [3fec1d2be46d] [a06b74f587c9] [f2e339bd5505] [59d9f9d20e0c]

**R47. Start cold campaigns on bestsellers, not the whole catalog.** Condition: new Shopping, PMax or Demand Gen campaign, or a takeover. 5 to 10 bestsellers (source 03, usually under 10); 1 or a handful of products (source 08); 20% of SKUs for 80% of revenue (source 01). Open the full catalog to warm audiences only (source 08). Add an all-products campaign later to find new bestsellers (source 03) or a "testing" PMax on test products (source 01). Sources: 01, 02, 03, 08. Cards: [7a8f73110a88] [e248a09cecef] [4995c5440e92] [11a3baaf5810] [dbf8b8785311] [f08cac856543] [422b680d3617]

**R48. Standard Shopping is the precision layer; PMax is the reach layer; at scale, layer Standard Shopping next to PMax for cold growth.** Condition: PMax has plateaued (raising budget or target no longer moves backend revenue) or spend is high. Source 04: PMax gets the account moving under about $15k to $20k a month, plateaus at $100k to $300k a month, and should hold 20% to 40% of spend at scale with Standard Shopping doing cold acquisition. Source 07: 1 lean PMax until about $5k to $10k a day, layer Standard Shopping above about $20k to $25k a day. Source 06/09: Shopping for hero, high-margin, clearance and new-arrival SKUs. Source 10: rebuild PMax's parts (Shopping, Search, Demand Gen) and keep PMax as a catch-all. Conflict 7.1 and 7.4. Sources: 04, 06/09, 07, 10, 01 (composite approach). Cards: [8ac98b834d71] [e2e3fde986ec] [f2e339bd5505] [568c59a75126] [d4494776c11a] [10c2368513b5] [798fd2575bf2]

**R49. Name every campaign with 1 pattern: type, geo, focus, optional bid strategy or audience.** Examples: "Search | USA | Branded", "Shopping | USA | Bestsellers | Max Clicks", "PMAX | USA | Feed only | Remarketing focus". Sources: 03, 04, 02. Cards: [d9dc799b0bcb] [18f7a08a224c] [43c52017c399]

**R50. Kill tiny orphan campaigns and roll spend up.** Condition: campaigns with no role and little spend (source 04 example $400 a month). Only the top 5 campaigns by spend can move the account (source 05). Sources: 04, 05. Cards: [2792071d2d2e] [26676d575992]

**R51. Turn off Google's auto-apply recommendations, AI-generated keywords and assets, auto-created assets, video enhancements and (in remarketing) optimised targeting.** Condition: every campaign, unless testing on purpose. Sources: 01, 03, 04, 07. Cards: [b8508808a53a] [bdfbb0a5fb12] [f06749b19e9b] [18f7a08a224c] [08b3d9f85868]

**R52. Default campaign settings for ecommerce: Sales objective, purchase goal only, Search Partners off, Display Network off on Search, location option Presence (not Presence or interest), tablets and TV screens off unless device data says otherwise.** Condition: every Search, Shopping, PMax and Demand Gen build. Presence is not available on Video or PMax in some UIs (source 03). Tablets off is source 01's preference; check your own device data. Sources: 01, 02, 03, 04, 07. Cards: [b62174aad487] [535fcd04bd8b] [43c52017c399] [7640dc7d9a25] [35e595666320] [fbfe5ace84d4] [18f7a08a224c] [08b3d9f85868] [4184750845e0] `[verify UI]`

### 3.F Brand vs non-brand

**R53. Always separate brand from non-brand in Search, Shopping and PMax.** Condition: any account with brand search volume. Brand ROAS is structurally high and inflates blended results. Source 06/09 pattern: brand about 11% of search spend, 34% of conversions. Source 01 case: 50% overlap before segmenting, 87% of Google purchases from brand-unaware people after. Sources: 01, 02, 03, 04, 06/09, 10. Cards: [f6230028c4ce] [a56ce106bb55] [c4b8343d0510] [f52ecc6c8839] [cd05d756f069] [a715afa0c38a] [a2f5b3c20d44] [bcbe49473936] [9c25700ad918] [51226e3b8539]

**R54. Exclude brand from every cold campaign with both a brand exclusion list and exact-match brand negatives (all spellings, misspellings, brand plus product phrases).** Condition: PMax, non-brand Shopping, non-brand Search, DSA, Demand Gen prospecting. Neither control alone is foolproof. Sources: 01, 02, 03, 04, 06/09. Cards: [a2427f18e5fe] [69caeee85e5f] [8e83ab723ce9] [c769e50b230c] [23298f395683] [3280f3210b89] [ae212dfcabdd] [903e91b5cc9d] [9b1a4ac01c87] [a2f5b3c20d44] [4eceae623d26] `[verify UI]`

**R55. Run a branded Search campaign when competitors or resellers bid on the brand, when the account is new (cheap conversions feed learning), or when an offer turns brand researchers into buyers. Consider skipping or pausing it when no one bids on the brand and the organic listing always ranks first, and test the pause.** Sources 01, 03 and 06/09 say every brand needs it; source 02 would "almost always" skip it with zero competition; source 07 says it brings about 1% of revenue and is defensive; source 01 admits most brand conversions "would happen anyway" and tells Meta-heavy brands to experiment with turning brand off. Conflict 7.2. Cards: [b62174aad487] [6319ccc026d9] [4b15db679fc4] [fe8bd2cdf490] [a1bbee7012e8] [a56ce106bb55] [bcbe49473936] `[web check: who bids on the brand name, via a live search and Auction insights]` `[needs brand data: brand search volume, organic brand click share, a brand-off holdout if possible]`

**R56. Brand campaigns run on manual CPC or Target Impression Share (absolute top), never on conversion-based smart bidding, and never with the customer acquisition setting on.** Condition: brand Search and brand Shopping. Source 01: Target Impression Share, absolute top, 95%, max CPC about $3 for brand Search; Manual CPC, $1 default bid for brand Shopping. Source 02: manual CPC "I will never use automated bidding in branded campaigns", sometimes Target Impression Share, aim over 90% impression share. Source 03: Max Clicks in a new account, conversion bidding after 10 to 15 conversions (the outlier). Sources: 01, 02, 03. Cards: [b62174aad487] [1e8b3f869526] [c769e50b230c] [a3bf86a930b0]

**R57. Brand keywords in exact match; add phrase match later only to find new brand terms and promote converters to exact.** Condition: brand Search. Keywords: brand, misspellings, brand without space, brand plus product word, brand reviews, brand discount code. Do not go "super overboard" (source 03). Sources: 01, 02, 03, 06/09. Cards: [b62174aad487] [fe8bd2cdf490] [cd05d756f069] [bcbe49473936]

**R58. Cap brand spend for growth accounts; keep brand uncapped relative to search volume only when the goal is defence.** Source 01: brand at 3% to 8% of monthly Google spend, 10% at most, and 1% to 5% or 0 for Meta-heavy brands; cold traffic should hold 80% to 90% of budget. Source 03: $10 to $20 a day small brand, up to $50 a day large brand; branded Shopping about $20 a day. Source 06/09: uncapped relative to search volume and judged on ROAS, CPC and impression share, not growth. These agree in practice: brand budgets are small in dollars because brand volume is small, and the campaign should not be budget-limited when brand-intent terms hit the cap. Conflict 7.2. Cards: [e248a09cecef] [a56ce106bb55] [78000b7f5684] [d28083dc2834] [b69974ff92ac] [bcbe49473936] [4eceae623d26]

**R59. If a brand campaign runs, it must actually cover brand: under about 90% to 95% impression share at absolute top, it gives none of the protection benefit.** Condition: brand Search. Source 01: an account with 30 cent brand clicks at 14% or under 10% impression share gets nothing. Sources: 01, 02. Cards: [a56ce106bb55] [b62174aad487] [c769e50b230c]

**R60. Brand gets a much higher ROAS target than non-brand where targets are used; judge growth on non-brand alone.** Condition: separated reporting. Source 10: brand conversions are less incremental; if the account is over-indexed on brand, move budget to non-brand. Source 06/09 example: moving 30% of brand spend to non-brand lifted new customers 22% (uncontrolled). Sources: 10, 06/09, 02. Cards: [51226e3b8539] [72c8c5c5e72f] [bcbe49473936] [9c25700ad918] [c4b8343d0510]

**R61. Run a branded Shopping campaign when brand product searches are heavy (from Meta, TikTok, organic) or when you want products on brand searches; keep brand Shopping identical to non-brand Shopping in products, audiences and locations, differing only in priority and bidding.** Condition: brand Shopping split. Source 02 priority routing: non-brand campaign High priority with a brand negative list; brand campaign Low priority; a brand query is blocked in the High campaign and falls to the brand campaign. Guard 2 failures: non-brand limited by budget (brand queries spill), or a product missing from non-brand. Source 01 and 03 use a script that auto-excludes non-brand terms from the brand Shopping campaign. Sources: 01, 02, 03. Cards: [2983e818cf87] [1e8b3f869526] [f52ecc6c8839] [b69974ff92ac] `[web check: current negative keyword script for brand-only Shopping]`

**R62. Exclude existing customers from prospecting campaigns, and often from brand campaigns too.** Condition: customer list uploaded (Shopify or Klaviyo export, refreshed monthly). On YouTube, without the exclusion Google retargets buyers and takes credit. Use the list also as a PMax signal and a Demand Gen lookalike seed. Sources: 01, 02. Cards: [a2427f18e5fe] [2983e818cf87] [67af52d7623d] [ce4012235cdc] [5d0be265e08e]

**R63. Competitor campaigns: run them only in their own campaign with their own budget cap, judged on their own conversion rate; otherwise exclude competitor names.** Source 01 calls them a waste when brand protection works, but also lists "competitive search if it works well"; source 06/09 makes competitor terms tier 4 with a separate campaign. Sources: 01, 06/09. Cards: [f6230028c4ce] [a2427f18e5fe] [4c09826249af] [e8f1dbe974c5]

### 3.G Standard Shopping structure and optimisation

**R64. New account: Standard Shopping, not PMax, as the first product campaign. Decline the PMax preselection.** Condition: no conversion data. Sources: 02, 03, 08, 01. Cards: [43c52017c399] [11a3baaf5810] [575bdc0721ef] [4aee86b1351f]

**R65. First Shopping campaign: bestsellers only, 1 ad group, everything else excluded; add an all-products campaign once bestsellers show consistent sales and ROAS.** Condition: new account. Sources: 03, 02, 08. Cards: [11a3baaf5810] [4b04bc3b1c75] [dbf8b8785311] [4995c5440e92] [f08cac856543]

**R66. Choose the Shopping structure by catalog and margin: (a) 1 consolidated campaign for most DTC brands; (b) top sellers vs everything else (about 80% of spend on the top 20% of products) for large SKU counts outside fashion, not for 5 to 10 product stores; (c) margin tiers (3 to 5) when margins vary a lot; (d) ROAS tiers (high ROAS, low ROAS, low spend, zombies) when margins are within about 10%; (e) labelizer tiers on 30-day rolling performance only for thousands of SKUs; (f) feeder (cold Shopping at a very low tROAS beside a high-tROAS PMax) when PMax has plateaued.** Sources: 02, 04, 10, 06/09. Cards: [4995c5440e92] [e2e3fde986ec] [3fec1d2be46d] [a06b74f587c9] [b390a3400b4f] [f2e339bd5505]

**R67. Shopping optimisation loop: structure, bidding, negatives, monitor, poor products, good products.** Monitor CTR, CPC, conversion rate, ROAS or CPA, then search impression share, lost IS (budget), lost IS (rank), click share. Poor products: read their search terms, add negatives, fix title and description. Good products: lost IS (budget) high and at KPI, raise budget; lost IS (rank) high, decide whether to accept lower efficiency for scale, then raise CPC (manual) or lower tROAS (automated). High impression share with low click share means titles or images are not clickworthy. Source: 02, with 01 and 05 on impression share. Cards: [4995c5440e92] [5d9dd44f8d9a] [25c967c6e637] [c6256b30ff46] [ffbb287b9903] [36a8c46cb661] [2795573cf2d6]

**R68. Prune products that got real spend and clicks but drag ROAS; isolate zero-spend "zombies" in their own campaign or asset group with a small budget.** Condition: after enough data; no source gives a numeric threshold. Sources: 03, 01, 10. Cards: [258be064768c] [7a8f73110a88] [a06b74f587c9] [5ebe76f05300] `[needs brand data: break-even ROAS per product]`

**R69. When a competitor discounts a shared product 20% to 30%, pull or de-prioritise the product rather than match into near-zero margin; reintroduce when the gap closes.** Condition: resellers or shared SKUs. Source 05 client used a price-monitoring script. For own-brand products this is less clear. Source: 05 only. Cards: [caf9cb9b298e] `[web check: Merchant Center price competitiveness report]`

### 3.H Search campaigns

**R70. Let converting data pick keywords: run Shopping and PMax broad, read search terms daily, move converting queries into Search as exact match, then into titles, assets and landing pages.** Condition: any account with Shopping or PMax data. Traditional research (Keyword Planner, Semrush, Ahrefs, SpyFu) supplies the first rung and extra terms but has no purchase data. Sources: 01, 02, 10, 06/09. Cards: [a223f5b65ca8] [287eff9e6167] [8c0b85636322] [6bfe7d97b858] [4a2c02a70a66] [4c09826249af]

**R71. Classify keywords by intent before bidding: transactional (highest bids, product page), commercial or comparison (own ad groups, comparison pages), problem-aware (lowest bids, tightest negatives, advertorial or category page, not product page), navigational or brand (brand campaign), competitor (own capped campaign).** Condition: non-brand Search build. Sources: 02, 06/09, 01. Cards: [4691ad952431] [4c09826249af] [e8f1dbe974c5] [68c39167796f]

**R72. Build single-theme ad groups (STAGs), never SKAGs.** Condition: every Search campaign. Keywords per group: 2 to 3, up to 5 to 8 (source 02); 10 to 20 (source 04); 3 to 5, max 10 (source 03). Merged: 3 to 10 per theme; a keyword that does not fit starts a new group. RSAs have about 2,700 combinations and need about 250,000 impressions to learn, so 1 keyword per group never exits learning. Sources: 02, 03, 04, 10. Cards: [1b793cd8bbb3] [de648eb98d87] [76be15912789] [61f688e47745] [fd776d0fc197] [bca4ccb4fceb] [4a2c02a70a66]

**R73. Match types: exact for proven converters; broad only with smart bidding and lots of data, or as a deliberate test; phrase rarely (it has become broader).** Condition: new account or efficiency focus, exact on known converters (about 80% exact plus core broad terms is source 02's middle ground). Source 01 cold-search case ran exact plus broad with AI Max and "never phrase"; source 03 uses 3 to 5 phrase-match keywords for a category test; source 04 says never broad match with Maximize Clicks. Sources: 01, 02, 03, 04. Cards: [a223f5b65ca8] [c37ad85535b2] [68c39167796f] [c45d399b63a9] [18f7a08a224c] `[web check: current exact and phrase match definitions]`

**R74. Search ads: 7 to 9 headlines and 2 to 4 descriptions with distinct angles, not 15 near-duplicates; pin only with a reason (brand authority in headline 1 on brand ads, a promotion that must show, dynamic keyword insertion on problem-aware terms).** Source 02: 7 to 9; source 10: 8 headlines and 2 descriptions; source 03: 3 to 5 headlines, pin brand to position 1; source 01: fill all 15 in PMax and pin DKI in cold search. Ad strength is not ad rank. Conflict 7.6. Sources: 01, 02, 03, 10. Cards: [bfa79d563469] [533ef4069e40] [b14c89dd124a] [966d6939f047] [4b1f9877b48b] [68c39167796f] `[web check: RSA asset limits]`

**R75. Fill the assets: sitelinks (collections, best sellers, reviews, promotions), callouts (25 characters, up to 10), structured snippets, promotion asset, price assets (rarely), business name and logo (needs advertiser verification), images. Skip calls and messages for ecommerce.** Condition: Search and PMax. Per asset group, not account-wide ("account-wide is lazy", source 01). Sources: 01, 02, 03, 04. Cards: [850683161175] [19cb14a20c03] [8e3ee156ad91] [2792071d2d2e]

**R76. Headlines grab, match intent and drive action; descriptions handle objections, add trust and urgency; use the searcher's words.** Condition: all RSAs. Tactics: imperative verbs, numbers, "you", the offer in 1 or 2 headlines, title case headlines, sentence case descriptions. Sources: 02, 03. Cards: [089beecb4466] [195e55ecd55d] [4b1f9877b48b]

**R77. Fix quality before paying more: expected CTR (ad copy, assets, match), ad relevance (tighter themes, keyword-to-copy match), landing page experience (speed, mobile, message match). Raise bids only when quality is maxed.** Condition: Search keywords. Source 02 case: one keyword's CPC fell from $5.84 to $2.38 after ad and page fixes. Landing page experience recovers slowly (weeks to months, source 05). Sources: 02, 05, 06/09, 07, 10. Cards: [be07dfd74db8] [4d0a3e281799] [76be15912789] [6ff74a04932d] [1267e0489b18] [2d82081ef51f] [11dd9a205267] [8beaa7445948]

**R78. Cold problem-aware Search: only when the product solves a searched problem; send to an advertorial or educational page, not a bare buy box; Maximize Conversions (or Maximize Clicks while testing fit); brand excluded; exact plus broad; DKI pinned.** Condition: real category or problem demand (blood pressure, methylene blue). Skip Search for unique low-volume products. Source 01 case: £3,500 spend, 2.18 Google ROAS, 8.32% CTR, 3.82% conversion rate over about 3 weeks (example). Source: 01, with 06/09 on problem-aware routing. Cards: [68c39167796f] [30a52da78077] [deb514cc9507] [e0e3cef53d9f] [4c09826249af]

**R79. Test landing pages from Search continuously: duplicate the ad, point ad 2 at page 2, compare conversion rate over 30 to 60 days, keep the winner, add a challenger.** Condition: Search ad groups with volume. Source: 04, with 01 on ad and page testing. Cards: [bd9b251ac5b1] [e5912712faf6] `[needs brand data: conversion rate and AOV per landing page]`

**R80. DSA: only with a large content site across many categories, after RSAs run, to mine keywords and preview how PMax search may behave; negative ad targets on policy, blog and returns pages.** Condition: not a 1-page funnel. Source 04 notes DSA is being deprecated. Sources: 02, 01, 04. Cards: [aa122d012f28] [be76f13238a4] [2977af57de2c] [e0e3cef53d9f] [8ac98b834d71] `[web check: DSA status]`

**R81. AI Max for Search: source 01 turns it on for cold search (opinion, "new features tend to do well"); source 02 skips it to keep control; source 06/09 assigns it long-tail and conversational queries in large accounts.** Condition: treat as a test in 1 campaign with brand excluded. Sources: 01, 02, 06/09. Cards: [68c39167796f] [535fcd04bd8b] [61d89a7caa36] `[web check: AI Max for Search behaviour and controls]`

**R82. CPC is a vanity metric except at the extremes (about $100 never profitable; about 10 cents probably junk). CPC up with conversion rate up is fine; CPC up with conversion rate flat is the problem.** Condition: any read of CPC. Sources: 04, 05. Cards: [087445947ca9] [6ff74a04932d]

### 3.I Performance Max mechanics

**R83. Qualify before launching PMax: clean feed, 1 primary purchase action, at least $50 to $100 a day (source 01) or $100 a day and at least 3x non-brand CPA (source 02), and enough conversions (30 to 50 a month, source 01; about 100 purchases in the account, source 08). If not, run manual Search and Shopping.** Condition: accounts that plan PMax as a conversion campaign. Sources 07 and 10 treat PMax as a fine start for beginners. Conflict 7.1. Sources: 01, 02, 08, 03. Cards: [634ed94f1328] [c178b83767e8] [575bdc0721ef] [be2fa7635a24] `[needs brand data: non-brand CPA, monthly purchases]`

**R84. PMax on default settings is the enemy, not PMax.** Requirements: brand exclusions plus brand negatives; asset groups by product type or performance tier with listing groups customised to match; final URL expansion off (or URL-contains rules) and text customisation off; auto-created assets and enhancements off; tablets and TV off; Presence targeting; 1 country per campaign. Sources: 01, 02, 03, 04, 06/09, 07. Cards: [903e91b5cc9d] [fd408fa56660] [69caeee85e5f] [8e3ee156ad91] [64c009e7bc50] [f06749b19e9b] [5858ab16c0d1] [2fcfa24a9f1f] [08b3d9f85868]

**R85. Asset groups: 1 theme per group (product type or tier), 3 to 20 groups per campaign (source 04), 2 to 5 practical for small to mid accounts (source 06/09), at least about 15 products per group and never 1 product alone (source 04); every listing group filtered to its theme. Simpler beats hyper-segmented (200 to 400 asset groups underperformed).** Condition: full-asset PMax. Sources: 01, 02, 04, 06/09. Cards: [8e3ee156ad91] [329599511dc8] [8e83ab723ce9] [fd408fa56660] [a8f7e2302cd3] `[needs brand data: SKU count per product type]`

**R86. Split PMax campaigns only for a different audience or product line, a different country, or a different efficiency goal (efficiency PMax for categories 2 to 4 vs scaling PMax for bestsellers).** Condition: otherwise 1 campaign with asset groups. 1 hero SKU: 1 PMax plus brand Search plus brand Shopping is enough (source 01 case). Sources: 01, 02, 04. Cards: [329599511dc8] [d5f436322917] [4692423b2426] [a715afa0c38a]

**R87. Assets in a full PMax: fill headlines (source 01: 15; source 02: 6 to 7), 5 long headlines, descriptions (source 01: 5; source 02: 3 to 4), 15 to 20 images in horizontal, square and vertical crops, sitelinks and promotions per asset group; videos only if you have good ones (source 01 adds none and puts video budget in Demand Gen; source 06/09 asks for 5 videos per group). Refresh every 4 to 6 weeks; replace assets rated low or with no spend.** Sources: 01, 02, 06/09. Cards: [8e3ee156ad91] [8e83ab723ce9] [64c009e7bc50] [2bf868bfb28d] [a8f7e2302cd3] [abc2dfeeea38]

**R88. Audience signals and search themes are directions, not targeting. Use first-party lists (all-time customers, top customers) and converting search terms at launch; do not invent search themes; expect them to matter little after about 30 days of conversion data.** Source 04: after 30 days signals have done their job and are a 1% lever on mature accounts. Source 02: first-party lists learn faster than custom segments or in-market; search themes can cannibalise Search and DSA, add them only if you want PMax search aggressive. Source 03: leave signals blank. Source 01: up to 50 search themes from converting terms plus customer list and custom segments. Conflict 7.10. Sources: 01, 02, 03, 04, 06/09. Cards: [25eaf30834e2] [8e3ee156ad91] [c178b83767e8] [70544247c36d] [903e91b5cc9d] [5858ab16c0d1]

**R89. PMax over-credits itself on warm and brand traffic. Raising its target ROAS narrows it toward warm users; scaling a plateaued PMax by budget or target does not move backend revenue.** Source 04 ramp tests: Standard Shopping and PMax both at 5x; the Shopping ramp fell to 4x then 3x in platform but gave better backend revenue; PMax held 5x and backend lagged (across accounts, no holdout). Source 04 hearsay: 50% or more of PMax conversions are repeat or warm. Source 10: PMax spends about 60% to 70% on Shopping, 20% to 30% on Search, 5% to 10% on image and video that is "likely 100% retargeting". Source 05: higher tROAS shows worse new-customer ROAS. Sources: 04, 05, 10, 01, 03. Cards: [8ac98b834d71] [b390a3400b4f] [29bf1d1ed526] [4e3675b7a020] [be7ffdbb4c17] [72c8c5c5e72f] [5beebcb72872] [be2fa7635a24] `[needs brand data: new vs returning split by campaign]`

**R90. Feed-only PMax (listing group only, no assets, auto-generation and URL expansion off) is a test of pushing spend toward Shopping and stopping drift into YouTube, Gmail and Display, not a guaranteed Shopping-only or remarketing-only campaign.** Conditions where sources use it: PMax drifting into unwanted placements (source 04 case: YouTube 2% to 10% of spend, Gmail about 10%, ROAS down about 20%, fixed by feed-only); no strong video or lifestyle creative; need to isolate Shopping spend (source 06/09); a "remarketing layer" beside non-brand Shopping (source 03); the main ecommerce campaign, limited to Search and Shopping (source 07). Cards in 02, 03, 04, 06 and 09 carry Google Help corrections: no placement isolation is guaranteed and Merchant Center data can generate assets. Always check channel delivery and new vs returning after launch. Conflict 7.5. Sources: 03, 04, 06/09, 07, 02 (header only). Cards: [70544247c36d] [0ac64f9f98bb] [aa3a6d301e62] [d4571d60eeee] [5858ab16c0d1] [2fcfa24a9f1f] [08b3d9f85868] [eb5d63ad4917] `[web check: Google Help 14530785 and 15865151; PMax channel performance report]`

**R91. PMax product hygiene: keep high-spend products in stock; products going in and out of stock reset that product's learning and hurt the campaign; exclude SKUs that spend without converting via listing groups; put underperformers in a "zombie" asset group if they must stay.** Condition: weekly. Source 05: a product with 15% of PMax spend out of stock 4 days hurts the whole campaign; source 05 says 80% to 90% of PMax performance in ecommerce comes from Shopping, so feed quality is the PMax lever. Sources: 01, 05. Cards: [5ebe76f05300] [7a8f73110a88] [4e3675b7a020]

**R92. PMax priority order (ecommerce, PMax weighted to Shopping): feed titles, descriptions and images; brand exclusions; asset and listing group structure and asset quality; bidding strategy; audience signals and search themes.** Source: 04 only for the order; 06/09 agree that inputs (feed, conversion data, signals, creative) beat output control. Cards: [903e91b5cc9d] [abc2dfeeea38] [daa2070d28bf]

**R93. Mine PMax search terms to launch dedicated Search campaigns on proven terms; PMax takes a lot of search spend.** Condition: PMax with search term insights. Sources: 01, 06/09, 10. Cards: [798fd2575bf2] [4c09826249af] [4a2c02a70a66]

**R94. PMax safety net: after Shopping, Search and Demand Gen are rebuilt, keep PMax on at a much higher ROAS target (source 10 example: manual campaigns at 300% to 400%, PMax at 600% to 700%) so manual campaigns win most auctions and PMax catches stragglers; watch PMax spend share and widen the gap if it still dominates.** Condition: advanced account with time to manage. Same mechanism as the feeder strategy in R114. Source: 10 only (04 gives the feeder). Cards: [56795ebc9766] [b390a3400b4f] `[web check: current PMax vs Standard Shopping and Search serving rule]`

**R95. Do not trust "Shopping High priority beats PMax" as a serving rule.** Source 03 says High priority on Standard Shopping makes it serve before PMax; sources 06/09 say since late 2024 the higher ad rank wins regardless of type; source 02 uses priority only between Shopping campaigns. Conflict 7.4. Cards: [70544247c36d] [07a456f35774] [013bd9d69456] [f52ecc6c8839] `[web check: Google's current rule for Standard Shopping vs PMax serving]`

### 3.J Demand Gen, YouTube, Display and remarketing

**R96. YouTube (via Demand Gen) is the lever that breaks the search-volume cap; add it only when Search and Shopping are dialled in, unless the brand is Meta-heavy with proven creative and little category search.** Sources: 01, 02, 03, 06/09. Cards: [5f52247ede2b] [6be29457f355] [44689f14e053] [a5cf27b657fa] [b6530a0cdc65] [64749b0f187a] [78000b7f5684]

**R97. YouTube fit check before spending: AOV ideally $75 to $100 (over $50 workable, $25 to $30 poor); visually demonstrable product; winning Meta creative and a validated offer; budget for 4 to 6 choppy weeks; no budget stolen from a working channel.** Source 02 for the numbers; source 01 says test creative on Meta and move winners to YouTube. Sources: 01, 02. Cards: [1abd0e7f1e7c] [a5cf27b657fa] [a2427f18e5fe] `[needs brand data: AOV, Meta winners]`

**R98. Demand Gen prospecting setup: Sales objective, purchase goal only, Maximize Conversions with no target CPA at first, YouTube in-stream and Shorts only (in-feed, Discover, Gmail, Display off), tablets off, TV off until scaling, mobile only when starting with Meta creative, optimised targeting off while testing, no sitelinks, final URL never the homepage.** Condition: cold YouTube. Product feed: sources 01 and 02 turn it off ("never worth running"); source 03 and 06/09 turn it on. Conflict 7.11. Sources: 01, 02, 03. Cards: [87c6c1776dbe] [a1e9a7459f53] [dc729c544305] [15e16ca20a02] [4184750845e0]

**R99. Demand Gen audiences: source 01 runs fully broad (creative is the targeting; $8,000 a day broad and profitable); source 02 starts narrow (custom segments of search terms, competitor sites, lookalikes of converters, demographic refinement) and expands sideways, never in-market or affinity; source 03 runs open with at most 3 to 5 search themes and 1 to 2 in-market segments, and never feeds Demand Gen your own customer or remarketing lists. All exclude the all-time customer list. Conflict 7.11.** Cards: [87c6c1776dbe] [5d0be265e08e] [12168d012cf1] [ce4012235cdc]

**R100. Demand Gen budget: at least $100 a day (source 01), about 3x AOV per day (source 02, $60 AOV means $180 a day), $50 a day at $10 to $20 AOV and $100 or more at about $50 AOV (source 03), about 30% to 40% of account budget when new customers are the focus (source 03), about 80% for Meta-heavy DR brands (source 01). A $50 a day test totalling $500 is not a test (source 01).** Cards: [87c6c1776dbe] [dc729c544305] [2380ca9a554b] [78000b7f5684] [e0e3cef53d9f] `[needs brand data: AOV, total daily budget]`

**R101. YouTube creative: Shorts 20 to 60 seconds, never over 60 (Shorts eligibility ends about 60 seconds); 9:16 with subtitles; hook in the first 1 to 5 seconds; problem then demo then social proof at 60% to 70% then a strong direct CTA with offer; call out the situation, not the demographic; no lazy AI voice ads; never hire an actor as "the founder"; up to 5 videos per ad group; make 16:9 versions of winners for in-stream and TV (source 01: Shorts CPM about $17 vs about $8 horizontal).** Sources: 01, 02, 03. Cards: [6803e3b2bebe] [d2116e31fe30] [417de6079aa3] [a1e9a7459f53] [9bfa186f1531] [2d25e7734ec7] [40f24b9ec7e3]

**R102. YouTube KPIs and traffic lights: view rate about 20% in-stream and 10% Shorts is good; CTR above 1% in-stream (1.3% to 1.4% typical) and 0.6% to 1% Shorts; dashboard conversion rate 0.05% or more (below means fix the page); new-customer CPA at or under break-even. Poor on all: pause. Soft: keep and hunt a stronger ad. Strong: raise budget fast. Judge campaign-level new-customer CPA, not each ad, because ads sequence.** Source: 01 only for the ranges; 02 gives lead indicators (view rate, played to 25/50/75/100%, CTR, CPM, CPV, frequency) since purchases lag 1 to 2 weeks. Cards: [b934c312198e] [9bfa186f1531] [c93a353df47a] `[needs brand data: break-even new-customer CPA]`

**R103. Switch Demand Gen to target CPA or ROAS only after 2 to 4 weeks with a steady CPA over 3 to 5 days (source 02) or about 50 conversions (source 06/09), set at or slightly below current CPA; then raise bids 5% to 10% (never over 15%) every 5 to 7 days (source 06/09). Let it run 30 days before big changes.** Sources: 02, 06/09, 03 (no target CPA until Google finds a realistic CPA). Cards: [dc729c544305] [1990ef8e4d09] [2380ca9a554b]

**R104. Remarketing: build lists first (website visitors 3 to 7 days normally, 30-day default; cart abandoners from GA4 add_to_cart minus purchase, 30 days or 60 for low traffic; product viewers; YouTube ad viewers; past purchasers), wait for size (source 02: about 1,000 to 1,500 people to serve, not a universal rule), then run Demand Gen remarketing (YouTube, Discover, Gmail, no Display) with optimised targeting off, images and videos in 1 campaign, audiences as separate segments, and 1 objection per ad (complacency, price, trust, efficacy, logistics).** Sources: 02, 03, 10. Cards: [4bba31df42c6] [8573a3074cc2] [7b6b3c03be03] [061764977d03] [bff4fce7c8df] [4cbf20c9e261] [06762ec1db15] [1010d231578b] [74a36fd11057] [3f75b0b24b85] [cd21a20937c4] [146aa74746f4] `[web check: current list-size minimums per network]`

**R105. Display: remarketing only, at $10 to $15 a day, Maximize Conversion Value, optimised targeting off; cold Display only at tens of thousands a day. Video remarketing before Display remarketing. Display Network off on every Search campaign.** Sources: 01, 02, 03, 04, 05. Cards: [c38dea49205d] [e69a94e940ad] [0997a8f355eb] [7640dc7d9a25] [18f7a08a224c] [141c23b0306c]

**R106. Read Demand Gen by audience and by network; make more creative for the winning placement and cut or exclude the weak one.** Condition: segmented audiences set up. Source 10 example: Shorts winning, Display losing. Sources: 10, 01 (audience insights feed Demand Gen). Cards: [ffb75a5b8076] [146aa74746f4] [a5827fbc8126] `[web check: whether Demand Gen allows turning off single placements]`

**R107. Conversion mechanism order for cold YouTube traffic: decked-out sales page, advertorial (story preferred), quiz funnel, listicle, VSL only at scale. Capture email on the page (source 01 case: 14.7% pop-up rate) and run welcome and post-purchase flows; count that retention revenue in the first-order math.** Source: 01 only. Cards: [7d3bf600db06] [4b1cf3a51f8d] [322026f452d6] [e2980a3a4e74]

### 3.K Bidding by stage

**R108. Stage 1, no conversion history: manual CPC (with a cap, source 02 example $2 per keyword) or Maximize Clicks (with an optional max CPC) on Search and Shopping. Trim by hand until conversions build.** Condition: new account, or an account with no recent conversions (paused 2 years counts as new). Source 02 uses manual CPC 70% to 80% of the time; source 03 uses Maximize Clicks; source 01 uses manual bidding in phase 1; source 04 says manual or Maximize Clicks belong only in new accounts (and never broad match with Maximize Clicks); source 07 launches PMax on Maximize Conversion Value with no target from day 1 and never uses a manual stage. Conflict 7.7. Sources: 01, 02, 03, 04. Cards: [4aee86b1351f] [805871e8952b] [5d9dd44f8d9a] [a3bf86a930b0] [56cda9478c6f] [9b1a4ac01c87]

**R109. Stage 2, conversions arriving: move to Maximize Conversion Value (Maximize Conversions or tCPA only when order values are fixed, single SKU or subscription, or when you know break-even CPA and want volume, not value).** Switch points by source: 10 to 15 conversions (source 03, Search), 15 to 20 (source 03, Shopping), about 30 a month (source 02), 1 a day for 30 days (source 01), 15 to 30 (source 02 header only). Ecommerce bids for value about 90% of the time (source 04): conversion bidding funds the cheapest product. Conflict 7.9. Sources: 01, 02, 03, 04, 06/09. Cards: [805871e8952b] [a3bf86a930b0] [56cda9478c6f] [4aee86b1351f] [ed1a69221ddc] [07bdd8638a6a] [283cece14dca] [4b56cb53eee4]

**R110. Stage 3, enough volume: add a Target ROAS set at or slightly below the trailing 30-day actual, and hold it at least 2 to 3 weeks.** Switch points: 30 to 50 conversions a month per Shopping campaign (source 02); over 50 (source 02 mind map); 50 a month in 1 PMax campaign (source 02); 30 or more a month with a steady ROAS (source 03); about 50 a month, more in competitive auctions (source 06/09); about 3 months and only at a plateau for PMax (source 07). First target: at or 10% to 15% below actual (sources 02, 04, 06/09; source 04 example trailing 420% to 430%, set 400%). Never set the target far above actual (a 700% target on a 200% campaign stops spend). Conflict 7.9. Sources: 01, 02, 03, 04, 06/09, 07. Cards: [5da4b51eabe6] [5d9dd44f8d9a] [9edd4e9d7860] [56cda9478c6f] [29bf1d1ed526] [283cece14dca] [4b56cb53eee4] [d4494776c11a] [7f0f4a47add4]

**R111. Target ROAS trades swings for stability; it does not raise average performance, and raising it narrows the audience toward warm users.** Condition: any tROAS campaign. Source 04 illustration: target raised 400% to 500% moved a campaign from about 4x to about 6x at $1,000 a day, and the earlier position reached more cold traffic. Source 05: tROAS shows "how hard the campaign will go on retargeting warm people". Sources: 04, 05, 01. Cards: [29bf1d1ed526] [4e3675b7a020] [141c23b0306c] [4175eb319be4]

**R112. Step the target gently: source 06/09 says 15% to 20% per step, 2 to 3 weeks apart, watching impression share and conversion volume; source 02 says raise gently or hold it and scale budget; source 01 says wait 2 to 4 weeks after any bid strategy change. Do not halve a target CPA or double a budget overnight (source 04).** Cards: [283cece14dca] [5da4b51eabe6] [4175eb319be4] [7003ff9f69ce]

**R113. Break the target ROAS death spiral by cutting the target aggressively, not timidly.** Pattern: ROAS dips (seasonality, a hero product out of stock, 100 conversions falling to 80), the campaign misses target, shrinks its audience, models from a smaller 30 to 90 day sample, and spend trails off. Timid cuts fail. Also check stock-outs and seasonality first. Source: 04 only. Cards: [3001e5a56d5d] [29bf1d1ed526]

**R114. Do not stay on a restrictive strategy forever; rotate expansive (Maximize Conversion Value) and restrictive (tROAS) periods, or run a feeder: cold Standard Shopping at a very low tROAS (source example 50%) beside a high-tROAS PMax (example 600%), judged together on backend revenue and new customers.** Condition: PMax plateaued or suspected of warm-traffic over-crediting; margin and cash can fund a deliberately low-ROAS cold leg. Source 04 gives no rotation length, budget split or stop rule. Source: 04 only (10 uses the same mechanism as the safety net, R94). Cards: [07bdd8638a6a] [b390a3400b4f] [56795ebc9766] `[needs brand data: margin and cash to fund the cold leg]`

**R115. Portfolio bid strategies: pool campaigns that share 1 goal to merge learning, and use them to add a Max CPC cap or bid floor (source 06/09 case: spikes to $25, cap $9). Do not pool different goals (clearance vs new arrivals), campaigns needing manual bids, or tiny campaigns.** Sources: 04, 06/09. Cards: [8d6cc6ef07b8] [b664dd686d10] [e5678cb19768] `[web check: which strategies support portfolio bid limits]`

**R116. Seasonality adjustments only for 1 to 7 day conversion rate jumps from unusual causes (a flash promotion), not for holidays or anything over 7 days.** Source: 06/09 only. Cards: [44615a608690]

**R117. Smart bidding exploration (Search only) lets a tROAS campaign test auctions outside its target in 10%, 20% or 30% bands; consider it instead of loosening the target.** Source: 04 only, no results given. Cards: [97caffb37450] `[web check: name and availability]`

**R118. After 17 Aug 2026 (source 06/09 claim), budget-limited tROAS and tCPA campaigns track closer to the stated target, so re-audit loose legacy targets that the budget cap used to hide.** Source: 06/09 only. Cards: [283cece14dca] `[web check: 17 Aug 2026 Target ROAS change]`

### 3.L Budgets

**R119. Size daily budgets from AOV and CPA: a new Maximize Conversion Value campaign at about 3 to 4x AOV per day (source 02); PMax at $100 a day and at least 3x non-brand CPA (source 02) or $50 to $100 a day (source 01); YouTube at about 3x AOV (source 02); a $1,000 product at $200 per conversion on $50 a day gives 1 conversion every 4 days (source 03 illustration). Start only with a budget you can lose.** Sources: 01, 02, 03. Cards: [805871e8952b] [c178b83767e8] [8e3ee156ad91] [dc729c544305] [56cda9478c6f] [d28083dc2834] [96b95d8a8ec0] `[needs brand data: AOV, non-brand CPA]`

**R120. Budget shares are rules of thumb by stage, not 1 plan.** Cold traffic 80% to 90% of budget and brand 3% to 8% (source 01). Non-brand Shopping 50% or more; video remarketing 10% to 15%; Demand Gen about 30% to 40% when new customers are the focus (source 03). Shopping 80% to 90% (source 04). PMax 20% to 40% at scale (source 04) vs PMax 50% to 70% with Shopping 30% to 50% and Demand Gen 10% to 20% (source 06) vs PMax 70% to 80% with Shopping 20% to 30% (source 09). Meta-heavy DR brands: about 80% Demand Gen, 10% to 15% mid-funnel (up to 20% to 30% in big categories), 1% to 5% brand (source 01). Conflict 7.1. Cards: [f6230028c4ce] [e248a09cecef] [56cda9478c6f] [0997a8f355eb] [2380ca9a554b] [0faae8bbc52a] [8ac98b834d71] [013bd9d69456] [6a480c2ffb47] [78000b7f5684]

**R121. Raise budgets in steps of about 10% to 20% per week when ROAS holds above break-even; cut faster.** Source 01: 10% to 20% weekly; spending 100% at KPI, raise 10% to 15%; spending under 80% and underperforming, loosen the target instead. Source 04: about 20% steps, cutting from high budgets fast is fine. Source 02 allows $50 to $60 to $70 to $100 or doubling "at any time" (the loosest). Exception (source 01): a real demand spike (a podcast) with a converting mechanism justifies a hard raise ($1,000 to $20,000 a day in its case) while results hold. Sources: 01, 02, 04. Cards: [4175eb319be4] [7003ff9f69ce] [96b95d8a8ec0] [d40cdd66a2bc]

**R122. "Limited by budget" is a hint, not proof: test extra spend in steps and watch backend revenue.** Condition: any campaign; source 04 sees the flag at $5k to $10k a day in a small market. Raise budget only when lost IS (budget) is high and the campaign hits KPI. Sources: 04, 02, 05. Cards: [a36358d5ff15] [ffbb287b9903] [2795573cf2d6]

**R123. Ignore Google's budget forecasts and "spend more" recommendations.** Sources: 02, 01, 04. Cards: [96b95d8a8ec0] [b8508808a53a] [18f7a08a224c]

### 3.M Negatives and exclusions

**R124. Keep an account-level universal negative list (jobs, careers, interns, hiring, salary, free, cheap where they signal no intent) so every new campaign inherits it; put terms irrelevant to the whole business at account level, terms irrelevant to some products at list, campaign or ad group level.** Sources: 04, 02, 06/09. Cards: [12e5a4881580] [25c967c6e637] [423e6a50781c] [07a456f35774]

**R125. Negative match types mirror keywords: broad negatives block any order of all words (not singular or plural variants), phrase negatives block the words in order with extras allowed, exact negatives block only the exact query.** Source: 02 only. Cards: [2cd86d3bc065]

**R126. Search term review cadence: daily in new campaigns, new products and high budgets, or every 48 to 72 hours for new PMax (source 02); weekly in month 1 for new Search at normal budgets (source 04); at least a couple of times a week once stable (source 02); less after month 1 and avoid over-editing because each change resets learning a little (source 04). Sources: 01, 02, 04, 07 (Sunday review).** Cards: [a5827fbc8126] [423e6a50781c] [2bf868bfb28d] [12e5a4881580] [031ec7c8b2d2]

**R127. In cold Search, remove terms with clicks and no conversions and promote converting broad terms to exact; no source gives a minimum click count.** Sources: 01, 02. Cards: [68c39167796f] [deb514cc9507] [423e6a50781c]

**R128. PMax exclusions: brand list plus brand negatives (R54); URL exclusions for blog, about, size charts, shipping, contact, high-bounce and out-of-stock pages when final URL expansion is on; SKU exclusions via listing groups; account-level placement exclusions; age exclusions where the product is age-bound; customer list exclusions on cold campaigns.** Sources: 01, 04, 06/09. Cards: [64c009e7bc50] [69caeee85e5f] [5ebe76f05300] [5858ab16c0d1] [2fcfa24a9f1f] [a2427f18e5fe] `[verify UI]`

### 3.N Scaling gates

**R129. Pass 5 gates before adding budget or campaign types: feed health (no disapprovals, warnings worked down); tracking validated end to end (enhanced conversions on, values equal real order revenue, reconciled with backend); brand and non-brand in separate campaigns, budgets and reports; creative supply (15 or more images and 5 or more videos per full PMax asset group refreshed every 4 to 6 weeks, continuous Demand Gen refresh); bid maturity (about 50 conversions a month before tROAS). A failed gate means invest in inputs, not budget.** Source: 06/09 for the gate list; the same conditions appear across 01, 02 and 04. Gate 2's "server-side tags firing" is stricter than the same source's $50k a month server-side heuristic; treat server-side as required only above that spend. Cards: [abc2dfeeea38] [daa2070d28bf] [634ed94f1328] [f6230028c4ce] [2792071d2d2e]

**R130. Scale from strength: only a campaign that hits target ROAS at the current budget gets more budget; expect ROAS to fall as spend rises and judge on total profit and customer count (4x at $100k a month beats 6x at $10k).** Sources: 08, 01, 04. Cards: [af051bd7984a] [4175eb319be4] [8ac98b834d71]

**R131. "Cut fast, scale slow" in steady state; scale a clear winner or a real demand spike fast.** Source 01 says both; the condition decides. Cards: [4175eb319be4] [9bfa186f1531] [d40cdd66a2bc]

**R132. Scale order for YouTube: more (budget until the ceiling, more creatives), better (hook tests, 16:9 versions, new offers and CTAs, new mechanisms), new (in-feed long-form with a thumbnail).** Source: 01 only. Cards: [9bfa186f1531] [b934c312198e]

**R133. When a product scales, plan stock and supply; stock churn on a high-spend product resets its learning.** Sources: 08, 05. Cards: [f08cac856543] [4e3675b7a020]

**R134. Catalog breadth: under about 30 SKUs limits what Shopping and PMax can find at scale (source 06/09); a 1-hero-SKU account still works with 1 PMax plus brand campaigns (source 01). Do not add thin listings just to add breadth.** Cards: [9a7b30ebd79d] [6a480c2ffb47] [d5f436322917]

### 3.O Diagnosis and operating cadence

**R135. Investigate top-down: business KPIs, channel, campaign type, campaign, metric, sub-metric, trigger, root cause. Never start at the metric a client names.** Source: 05, with 01 on the health read order (impression share, CPC, CTR, conversion rate, conversions, session duration). Cards: [7c50191f8854] [7fe2bb1f5bff] [ae67680618f3] [b27fb4f22fa1]

**R136. Before any change, apply 3 rules: read change history (yours, teammates, client, site); extend the window (90 to 180 days weekly for the account scan, never a 1-day read); read recent days on conversion time.** Source: 05, with 02 on latency. Cards: [62403f6f3b48] [31ee29611482] [d2bb52998ad7]

**R137. Google is rarely the cause of a business dip when it is 20% to 30% of spend; diagnose the larger channel first, ask what changed outside Google (sale ended, Meta creative refresh, offer change, site change), split revenue into conversion rate x AOV x sessions, and rule out seasonality against a forecast.** Source: 05 only. Cards: [7fe2bb1f5bff] [e2a87175fcd5]

**R138. Only the top 5 campaigns by spend can move the account; find the inflection date on the overview graph, then the 1 or 2 campaigns and ad or asset groups that changed after it.** Source: 05. Cards: [26676d575992] [31ee29611482]

**R139. Failure modes by campaign type. PMax: warm and cold drift (brand terms in search terms, audience skew), feed disapprovals or stock-outs on top products, tROAS pushed too high, product bloat. Shopping: tROAS, Merchant Center (stock, changed titles, errors), too many products, search partners. Search: search term reallocation under broad match and smart bidding, a new competitor in auction insights, tROAS, Display left on.** Source: 05. Cards: [4e3675b7a020] [141c23b0306c]

**R140. Split every KPI with 2 formulas: CPA = CPC / conversion rate; clicks = impressions x CTR. CPC up: quality score components, new competitor, premium auctions. Conversion rate down: tracking, landing page (the number 1 cause), audience shift, learning reset, offer change. Impressions down: lost IS (budget) if the budget is hit, lost IS (rank) if clicks and impressions both fall on steady spend. CTR down: stale seasonal copy, audience shift, competitor price cut on Shopping.** Source: 05, with 02 on impression share reading. Cards: [2069300bf455] [6ff74a04932d] [86ca17cab286] [2795573cf2d6] [caf9cb9b298e] [ffbb287b9903]

**R141. Default to a fix, not a rebuild; isolate 1 fix when the dip is mild, allow the kitchen sink only when dire; do not touch the account until you can finish the root-cause sentence ("this campaign is underperforming because this metric dropped, driven by this sub-metric, caused by this trigger, which was the root cause").** Source: 05. Cards: [5df8489778d1] [817f1a421116] [7c50191f8854]

**R142. Be in the account daily for search terms, auction insights and spend anomalies; do product, asset and landing page work weekly; refresh search themes, customer lists and bid strategy review monthly; check site vs Merchant Center policies monthly.** Sources: 01, 02, 07 (Sunday: tROAS, budget, remove keywords, remove products; judge week over week). Cards: [a5827fbc8126] [5ebe76f05300] [64c009e7bc50] [67af52d7623d] [b9ecdf07948a] [d40cdd66a2bc] [031ec7c8b2d2] [36a8c46cb661]

**R143. Nothing is set and forget: test search ads and feeds weekly against a control, keep several ads per ad group, replace low-rated PMax assets, refresh remarketing creative per objection.** Sources: 01, 02, 04. Cards: [e5912712faf6] [533ef4069e40] [2bf868bfb28d] [74a36fd11057]

## 4. Procedures (implementation)

Every step that names a menu, button, field or setting is `[verify UI]`. The recordings span late 2024 to September 2026. Where a source gives no step, the procedure says so. Rollback for every campaign build: pause the campaign; do not delete it, because history is lost.

### 4.1 Connect Shopify to Google Ads with the Google and YouTube app (fast route)

Goal: purchase, add to cart, begin checkout, page view, view item and search actions in Google Ads with enhanced conversions, plus product sync. Preconditions: 1 master Google account owns Google Ads, Merchant Center and GA4 (R20). Source: 02, 03. Cards: [93f8e8d57251] [52efc5146531] [a0825cabc944]

1. Shopify admin > Sales channels > Google and YouTube. Install. Sign in with the master Google account. `[verify UI]`
2. In app settings, pick the Google Ads account from the dropdown (name or number). Connect Google Ads first, then Merchant Center (existing or create). Choose to link products. `[verify UI]`
3. Check: the app imports conversion actions; purchase ("Google Shopping App Purchase") is primary. Enhanced conversions on. `[verify UI]`
4. Wait: the first purchase can take a couple of hours to fire; actions show in a day or 2. No sales means nothing fires.
5. Check: Google Ads > Tools > Data manager > Connected products shows Merchant Center linked; Merchant Center > Products shows the catalog (source 03 example 131 products). `[verify UI]`
6. If a GTM or GA4 purchase action already exists, go to 4.3 at once and leave 1 primary.
7. Rollback: disconnect the app's Google Ads link; set its purchase action to secondary.

### 4.2 Enhanced purchase tracking through GTM and a Shopify custom pixel (robust route)

Goal: purchase (with real value), add to cart, begin checkout, product view tags, dynamic remarketing parameters, GA4. Preconditions: GTM container; Shopify Customer events access. Source 01 gives the click path (its container and pixel code sit behind its opt-in); source 06/09 gives the tag list. Cards: [fff2f5c0c47c] [535e56dd51f1] [80d2cbcc7a96] [24d517dd8fe0] [56853873c2c8] [f866b580a9ae]

1. Google Ads > Goals > Settings: turn on enhanced conversions, method Google tag. (Source 06/09 says since June 2026 this is a single on/off switch.) `[verify UI]` `[web check: current enhanced conversions setting]`
2. Goals > Conversions > Summary > Create > Website > enter domain > Scan > "Add a conversion action manually". `[verify UI]`
3. Purchase action: category Purchase; in account default goals; primary; name "<brand> purchase"; value "use different values for each conversion"; count Every; click-through window 90 days, engaged view 30, view-through 30 (source 01's choice; R17 says match the purchase cycle); attribution data-driven; managed through the Google tag. `[verify UI]`
4. Add to cart and begin checkout: same settings, removed from account default goals. Product view: category Page view. Save. Copy the conversion ID and the 4 labels into the brand's setup doc (never into chat output).
5. GTM: Admin > Import container (source 01's container) or build by hand: Conversion Linker tag on All Pages; GA4 event tag for `purchase` on the thank-you page; Google Ads Conversion Tracking tag with ID and label, triggered by the purchase dataLayer event from Shopify's checkout thank_you page or Customer Events; pass product ID, category and value for dynamic remarketing; turn on "Include user-provided data" and map email, phone and address variables. `[verify UI]`
6. Value = actual order revenue including discounts and shipping, never a fixed value (R15). Margin-adjusted values are ideal; no source says how to compute them.
7. Submit > Publish. Copy the GTM container ID into the setup doc.
8. Shopify > Settings > Customer events > Custom pixels > Add custom pixel > name "Google conversion pixel" > delete default code > paste the GTM customer-event code > set country code > paste the GTM ID > Save > Connect. `[verify UI]`
9. Back in Google Ads: set add to cart, begin checkout and page view to Secondary (observe only). Purchase stays the only primary.
10. Check: place a test order; the purchase fires once with the right value; Tag Assistant shows the tags; enhanced conversions diagnostics report is clean (source 06/09). Reconcile Google purchases with Shopify orders over the next 7 days on conversion-time columns. No source gives a match threshold. `[needs brand data: Shopify orders vs Google purchases]`
11. Server-side (above about $50k a month, source 06/09): server container on Google Cloud or Stape, GA4 client, Ads Conversion Tracking tag and Conversion Linker in the server container; reconcile browser and server paths with backend orders; monitor the container. No source gives deduplication or consent steps. `[web check: consent mode requirements]`
12. Rollback: pause the GTM tags; set the GTM purchase action to secondary; the app action becomes primary again.

### 4.3 Set primary and secondary actions and link GA4

Goal: exactly 1 primary purchase action; GA4 as backup. Source: 02. Cards: [30fdf39203d6] [a3831e8b2c64]

1. GA4 > Admin > Property settings > Product links > Google Ads links > search the Google Ads ID > Link; enable personalised advertising and auto-tagging > Submit. `[verify UI]`
2. Google Ads > Conversion actions > Purchase category: list every purchase action (app, GTM, GA4). Open each > Settings > Action optimization. Exactly 1 purchase action Primary; all others Secondary. `[verify UI]`
3. Set add to cart, begin checkout, page view, view item, search to Secondary. Remove non-purchase actions from account default goals.
4. Check: conversions and ROAS did not double after linking GA4 (source 02: a sudden doubling means 2 primaries).
5. Every couple of weeks read 4 GA4 reports: user attributes, monetisation ecommerce purchases, landing pages (engagement time, bounce), first-user channel with UTMs on all paid traffic. [324a945cc6a5]

### 4.4 New-customer conversion tag

Goal: read new-customer CPA and ROAS without Google's customer acquisition setting. Source: 01 (no build steps given). Cards: [a336449b068e] [69caeee85e5f]

1. Keep the all-purchase action.
2. Add a second purchase event that fires only on a customer's first order (custom pixel logic or a tool such as Blotout). `[web check: how to detect first orders in Shopify customer events today]`
3. Option A (source 01's 2025 method): first-order event primary, all-purchase secondary. Option B: keep all-purchase primary and read new-customer CPA in Triple Whale, Northbeam or Google's native new-customer columns. `[web check: native new-customer metrics]`
4. Leave "customer acquisition" off in campaign settings (sources 01, 02, 03).
5. Check: new-customer count in Google matches Shopify first orders within reason.

### 4.5 Merchant Center setup

Goal: an approved, policy-safe Merchant Center linked to Google Ads with the 4 add-ons. Source: 01 (phases), 02, 03. Cards: [5fa36e157a58] [bb3574f9e67a] [7255257382d0] [5157f5f5a687] [8a99ccae1285] [911db04602d6] [69bd2ba35622] [c9b580a81edf] [a0825cabc944]

1. Create or select the Merchant Center in the Shopify app (4.1) or at merchants.google.com. Complete: business information, claim and verify the website, shipping and returns, tax, add products. `[verify UI]`
2. Settings > Add-ons > Discover: enrol dynamic remarketing, Google customer reviews, product ratings, promotions. Check each is active, not only available. `[verify UI]`
3. Business info: accurate name, address, phone, checkout link, payment methods; square and rectangular logo, main and accent colour; social profiles. Do not claim identity attributes that are not true (R29).
4. Shopify app > product feed settings > shipping = Manual (set up in Merchant Center). `[verify UI]`
5. Merchant Center > Shipping and returns: a shipping policy for every country by speed and method, named couriers, accurate ship-from; a returns policy that matches the site, linked to the returns page. Tax settings per country. `[web check: current Merchant Center tax settings]`
6. Settings > Data sources: confirm the primary feed (Shopify Content API or a feed app such as Simprosys, DataFeedWatch, Channable) updates; note supplemental feeds and promotion sources. `[verify UI]`
7. Link: Merchant Center settings cog > Apps and services > Add a service > Google Ads > pick the account > Confirm. Confirm in Google Ads Data manager. `[verify UI]`
8. Product ratings: submit the interest form; choose Google Customer Reviews, an official aggregator (Trustpilot, Stamped) or Judge.me via Shopify; needs 50 reviews total and 3 per product; allow 2 to 4 weeks. `[verify UI]` `[web check: thresholds]`
9. Promotions: add real promotions with exact details, dates and codes; test the code at checkout first.
10. Shopping experience scorecard: fix shipping, returns, purchase, browsing and promotion items; aim for "exceptional". `[verify UI]`
11. Check: Products status mostly approved (pending at first); Diagnostics has no red items; store quality shows a score. Setup takes about 20 minutes (source 02) plus approval time.
12. Rollback: none needed; fix issues in place. Never delete and recreate the account (history and trust reset).

### 4.6 Rewrite feed titles and roll them out

Goal: titles that match converting queries without resetting learning. Sources: 04, 01, 02, 06/09, 07. Cards: [a1c3cff78bf2] [18d6b809b70b] [3cce923d11c9] [b5af5e150e67] [6126c42680a9] [9983e71e8efc] [76f0f732dbe5] [afd1fd903f18] [59d9f9d20e0c]

1. Pull the search term report (Shopping and PMax) and list converting terms per product type. Add Keyword Planner terms for the core product. `[needs brand data: search terms with conversions]`
2. Audit 20 or more current titles: brand or internal name first, attributes past 70 characters, mixed order, under 60 or over 150 characters, raw manufacturer titles.
3. Draft per SKU: converting keyword plus product type (or unique name then keyword), variant attributes (colour, size, material, capacity, dosage, use case), second keyword or USP, brand last (brand first only for a known brand; conflict 7.3). First 70 characters carry the match; 60 to 150 total; 1 order across the catalog. An AI draft from the formula is fine; a human picks the 2 keywords and checks every attribute is true.
4. Descriptions: front-load keywords, features, USPs, buyer objections, a plain CTA, no promotional text, no false attributes, no stuffing.
5. Push through a supplemental feed (or the feed app) rather than editing the site or the primary feed; or edit in Merchant Center > Products > SKU > Edit for small catalogs. Never touch price, availability or ID. `[verify UI]`
6. Record a baseline (impressions, CTR, CPC, conversions, value per changed SKU, 30 days).
7. Roll out in batches, highest-opportunity products first. Never all titles at once.
8. Check after 2 to 4 weeks per batch: CTR, CPC, conversion value on changed listings. No material change: test different keywords. Re-audit after adding categories or price tiers.
9. Rollback: revert the supplemental feed row for the batch.

### 4.7 Feed health triage

Goal: zero disapprovals; warnings shrinking. Sources: 06/09, 01, 02. Cards: [82e55ef4dd25] [9972bf6ca8cf] [5157f5f5a687] [911db04602d6]

1. Merchant Center > Products > Diagnostics (or Needs attention). Filter Disapproved first. `[verify UI]`
2. For each disapproval find the cause: missing or wrong GTIN; price mismatch feed vs page; missing shipping; policy (restricted product, misrepresentation); formatting or missing required attribute (age group, gender, colour for apparel).
3. Autofix only formatting and optional attributes ("Fix type" filter, select all, Autofix). Fix policy, price and required attributes by hand in Shopify or the feed tool. `[verify UI]`
4. Then Warnings and Limited performance.
5. If prices change often: feed refresh at least every 6 hours; automatic item updates on. `[verify UI]`
6. Check weekly: no new red or yellow items; eligible product count stable. After a sudden drop in eligible products, run this at once.
7. Rollback: revert the last feed change (Merchant Center UI changes are reversible within 30 days per source 06/09, unverified). `[web check: 30-day reversal claim]`

### 4.8 Monthly policy and suspension check

Goal: catch mismatches before Google does. Source: 01. Cards: [95550c2e178c] [eea0c9ae49af] [a9d854c2d98d] [173c252bafd5] [9de75b008814] [f7f63ab97480] [8ff6407379e3] [b9ecdf07948a]

1. Shipping: site policy, couriers, cost and delivery time equal Merchant Center; update Merchant Center the same day a courier or cost changes.
2. Returns: window, refund processing time, return address and instructions current on site and in Merchant Center; test the return links.
3. Checkout: every listed payment method works; tax and shipping shown before payment; discount codes and live promotions work; SSL on checkout and sitewide.
4. Listings: out of stock shows as sold out and syncs; page price = checkout price = feed price; no broken links from product page to listing; no exaggerated or unsupported claims; only real reviews.
5. Contact and legal: physical address current; support phone works; branded email; same contact details across Merchant Center, Google Ads and all Google accounts; returns, shipping, terms, privacy, about, contact and subscription management in the footer.
6. Store: no default theme, no dead apps, no broken navigation, load speed tested, images and copy congruent with the feed.
7. Record each item as pass or fix in the brand's ops log. If suspended, assume 1 of these items; Google usually will not say which.

### 4.9 Branded Search campaign

Goal: own the brand SERP cheaply. Preconditions: decision per R55 (competitors bid, new account, or an offer worth showing); brand variants list. Sources: 01, 02, 03. Cards: [b62174aad487] [6319ccc026d9] [fe8bd2cdf490] [c769e50b230c] [4b1f9877b48b] [d28083dc2834] [19cb14a20c03]

1. New campaign > Sales > conversion goal Purchase only > Search > website visits. Name "Search | <country> | Brand". Skip "ways to reach your goal" and AI keyword or asset suggestions. `[verify UI]`
2. Bidding: Target impression share, absolute top, 95%, max CPC limit about $3 (source 01); or manual CPC (source 02). Never conversion-based smart bidding. Customer acquisition: off.
3. Networks: Search Partners off, Display off. Location: country, Presence. Language: the market's. Audiences: customer lists, site visitors, GA audiences as Observation only. No ad schedule. No brand exclusion. `[verify UI]`
4. Ad group "Brand": exact match [brand], [brand misspelling], [brandnospace], [brand reviews], [brand discount code], [brand + product word]. 4 to 6 keywords; do not go overboard.
5. Ad: final URL homepage (or the matching page per variant: reviews query to reviews page). Headline 1 pinned: "<Brand> Official Site"; test headline 2 as the offer; trust headline. 3 to 9 headlines (conflict 7.6). Descriptions from the best landing page copy. Business name and logo (needs advertiser verification). Sitelinks: collections, best sellers, reviews, live promotions. Callouts, structured snippets.
6. Budget: $25 a day (source 01) or $10 to $20 small brand, up to $50 large brand (source 03). Spending $5 to $10 of a $20 budget is normal.
7. Publish. Check after 7 days: impression share at absolute top 90% to 95%; CPC 1 to 50 cents; no non-brand terms in search terms (add negatives); no "limited by budget" on brand-intent terms.
8. Optimise: raise max CPC only if impression share is low; add phrase match of the brand to find new terms and promote converters to exact. Never move off impression-share or manual bidding.
9. Rollback: pause. If testing incrementality, pause for a fixed window and compare branded organic clicks plus total brand conversions before and after. `[needs brand data: brand-off holdout]`

### 4.10 Branded Shopping campaign

Goal: product listings on brand searches at manual cost. Preconditions: Merchant Center linked; brand volume worth it. Sources: 01, 03. Cards: [2983e818cf87] [1e8b3f869526] [b69974ff92ac]

1. New campaign > Sales > Purchases > Shopping > select Merchant Center > Standard Shopping (decline PMax). Name "Shopping | <country> | Brand". `[verify UI]`
2. Bidding: Manual CPC. Budget: $50 a day (source 01) or about $20 a day (source 03). Priority: High (source 01) or Low with the split in 4.12 (source 02). Search Partners off. All devices. Location Presence.
3. Ad group per product group; default bid $1. All products in 1 group unless products differ a lot and you want separate average CPCs.
4. Tools > Bulk actions > Scripts: add a script that auto-excludes non-brand search terms (source 01 and 03 scripts are not in the text). `[verify UI]` `[web check: current brand-only Shopping script]`
5. Audiences > Exclusions: upload the Shopify customer list and exclude it (source 01; optional, see R62).
6. Check weekly: search terms are brand only; impression share; raise max CPC a little if share is low. Never move to automated bidding here.
7. Rollback: pause.

### 4.11 Non-brand Standard Shopping (bestsellers first)

Goal: the main new-customer campaign in a new account. Preconditions: tracking works; Merchant Center linked; bestseller list. Sources: 02, 03, 01. Cards: [43c52017c399] [11a3baaf5810] [4b04bc3b1c75] [56cda9478c6f] [fbfe5ace84d4] [3280f3210b89] [dbf8b8785311] [258be064768c]

1. New campaign > Sales > Purchases > Shopping > Merchant Center (pick the right feed) > Standard Shopping. Name "Shopping | <country> | Bestsellers | <bid strategy>". `[verify UI]`
2. Bidding: Maximize Clicks (source 03) or manual CPC with a cap (source 02) while there are no conversions; Target ROAS only in a seasoned account (4.21). Bid equally for new and existing customers.
3. Budget: the largest share of the account (source 03: 50% or more). Priority: Low while it is the only Shopping campaign; change per 4.12 later. Search Partners off. Devices all. Location country, Presence. `[verify UI]`
4. Ad group "Bestsellers", default max CPC (example $1). Create.
5. Product groups: All products > plus > Add subdivision > Item ID (or category if the feed is cleanly categorised) > select 5 to 10 bestsellers (usually under 10; no sales yet, pick about 5 predicted winners) > Save without changing bids > set "Everything else in All products" to Exclude. `[verify UI]`
6. Negative keywords: add every brand variant in exact match (Campaigns > Audiences, keywords and content > Search keywords > Negative search keywords), ideally as a shared "Branded" list. `[verify UI]`
7. Check: ads serve within a couple of hours; search terms daily for the first weeks; product-level spend concentrates on the bestsellers.
8. After consistent sales and ROAS: switch bestsellers to Maximize Conversion Value (4.21), and add a second all-products campaign (same settings, no subdivision) to find new bestsellers; feed discovered winners back into the bestseller campaign; exclude products with real spend and clicks but weak ROAS.
9. Rollback: pause the new campaign; keep the bestseller campaign.

### 4.12 Brand and non-brand Shopping split by priority

Goal: read true non-brand Shopping performance. Preconditions: 2 Shopping campaigns with identical products, audiences and locations. Source: 02. Cards: [f52ecc6c8839]

1. Non-brand campaign: all (or bestseller) products; priority High; a moderate Target ROAS (source example 200% to 300%, set from KPIs) or the stage-appropriate strategy; attach the "Branded" negative keyword list. `[verify UI]`
2. Brand campaign: same products; priority Low; a higher Target ROAS or manual CPC (the source's number is garbled; use brand economics). `[verify UI]`
3. Routing: a query goes to the High campaign first; a brand query is blocked there by the brand negative and falls to the Low brand campaign.
4. Guard weekly: non-brand is not "limited by budget" (otherwise brand-campaign search terms fill with non-brand queries); no product is missing from non-brand.
5. This does not control PMax (R95, conflict 7.4).
6. Rollback: remove the priority difference and the negative list; the 2 campaigns return to sharing queries.

### 4.13 Non-brand Search campaign (STAGs)

Goal: capture category and product intent with control. Preconditions: keyword research (R70, R71); category with real demand. Sources: 02, 03, 04, 10. Cards: [535fcd04bd8b] [b14c89dd124a] [96b95d8a8ec0] [8c0b85636322] [6bfe7d97b858] [c37ad85535b2] [1b793cd8bbb3] [de648eb98d87] [76be15912789] [61f688e47745] [c45d399b63a9] [23298f395683] [4a2c02a70a66]

1. Research: 20 to 30 seed terms naming the core offer; expand each into long-tail; validate in Keyword Planner (volume, 3-month and year-on-year change, competition, top-of-page bid range); pull the PMax and Shopping search terms that already convert; filter by economics (expected CPC vs expected conversion rate vs target CPA or ROAS); cut to about 20 to 25 keywords to start. `[needs brand data: conversion rate, target CAC or ROAS]`
2. Classify by intent (R71) and route: transactional to product pages, category to collection pages, problem-aware to advertorial or category pages, competitor to its own capped campaign or excluded.
3. New campaign > Sales > Purchase only > Search > website visits. Name "Search | <country> | Non-brand | <theme>". Bidding: Maximize Clicks or manual CPC with no conversions; Maximize Conversion Value once conversions exist (4.21). Search Partners off, Display off, Presence, market language, audiences Observation only, AI Max skipped unless testing (R81), broad match setting off. Enter keywords by hand, not Google's URL suggestions. `[verify UI]`
4. Ad groups: 1 theme each, 3 to 10 keywords; exact for known converters, about 80% exact plus a few core broad terms with smart bidding; 1 collection per ad group, never 2. Attach the "Branded" negative list and the universal list.
5. Ads per ad group: at least 2. 7 to 9 headlines with distinct angles (conflict 7.6), 2 to 4 descriptions; keyword in a headline; offer in 1 or 2 headlines; pin only with a reason; DKI where the query language should echo. Final URL: the matching page; display path set. Business name, logo, images, sitelinks, callouts, structured snippets, promotion asset.
6. Budget: $20 to $30 a day for a category test (source 03); about 3 to 4x AOV for a Maximize Conversion Value launch (source 02). Ignore Google's forecast.
7. Publish. Check: serving within a day (if not after 1 to 2 days, check bidding, keyword volume, keyword choice); first clicks can be expensive; search terms daily in week 1 to 4; quality score components per keyword.
8. Optimise: negatives per R126; promote converting broad terms to exact; fix quality components before raising bids; landing page rotation test (4.14 step 6); keep winners, cut losers, add 1 or 2 new angles monthly.
9. Rollback: pause; if the category test is not profitable after enough data, drop it.

### 4.14 Cold problem-aware Search

Goal: capture problem searches before product awareness. Preconditions: the product solves a searched problem; an advertorial or educational page exists. Source: 01. Cards: [68c39167796f] [30a52da78077] [deb514cc9507]

1. Settings as 4.13 step 3. Bidding: Maximize Conversions (Maximize Clicks while testing fit on broad investigative terms). AI Max: source 01 turns it on; treat as a test. Brand exclusion on. Countries you ship to, Presence.
2. Keywords: many problem phrasings; exact plus broad; no phrase (source 01's choice).
3. Ads: DKI in a pinned headline; price extensions, structured snippets, callouts, sitelinks, logo.
4. Landing page: advertorial or educational sales letter, not a bare buy box.
5. Budget: source 01 case ran £125 a day. `[needs brand data: break-even CPA to size the test]`
6. Review search terms: remove clicks with no conversions; promote converters to exact; for the top term, point the keyword's final URL at a page written for that query. Ad group landing page rotation: duplicate the ad, ad 2 to page 2, read conversion rate over 30 to 60 days, keep the winner, add a challenger (source 04).
7. Next phase: articles for the 4 or 5 winning terms.
8. Rollback: pause.

### 4.15 Full-asset Performance Max build

Goal: a controlled PMax that acquires cold customers. Preconditions: R83 qualification (clean feed, 1 primary purchase action, $50 to $100 a day or $100 a day and 3x non-brand CPA, 30 to 50 conversions a month); brand list; product themes; creative for 15 to 20 images per group. Sources: 01, 02, 04, 06/09. Cards: [634ed94f1328] [69caeee85e5f] [8e3ee156ad91] [329599511dc8] [7a8f73110a88] [25eaf30834e2] [8e83ab723ce9] [c178b83767e8] [fd408fa56660] [903e91b5cc9d] [a8f7e2302cd3] [5858ab16c0d1]

1. Decide campaign count: 1 per truly different audience or product line, 1 per country, optional efficiency vs scaling split (R86). 1 hero SKU: 1 PMax.
2. New campaign > Sales > Purchases > Performance Max > add Merchant Center. Name "PMax | <country> | <line>". `[verify UI]`
3. Bidding: Maximize Conversion Value, no target for the first 2 to 4 weeks (source 02) or until 50 conversions a month in the campaign; source 01 has seen tROAS at break-even ROAS work best once data exists. Customer acquisition: off. `[verify UI]` `[needs brand data: break-even ROAS]`
4. Location: 1 country, Presence. Language. Ad schedule all day. Campaign URL options: UTMs for the attribution tool. Devices: tablets off, TV off; keep computers only if their data is good. `[verify UI]`
5. Brand exclusions: add the brand list (every spelling); also add brand negatives on the campaign (4.17). Age exclusions if age-bound. Skip Google's asset generation. Auto-created assets and enhancements: off. Final URL expansion: off (or URL-contains rules plus exclusions for blog, about, size charts, shipping, contact, out-of-stock pages). Text customisation: off. Image enhancements and landing page images: source 01 leaves on. `[verify UI]`
6. Asset groups: 1 per product type or tier (3 to 20; 2 to 5 for small to mid accounts); listing group filtered to that theme (item ID or category); at least about 15 products per group; never 1 product alone; underperformers in a "zombie" group with a small share. `[verify UI]`
7. Per asset group: brand guidelines (name, logos, colours, fonts); headlines (6 to 15, conflict 7.6), 5 long headlines, 3 to 5 descriptions; 15 to 20 images in horizontal, square and vertical; videos only if strong (source 01 adds none; source 06/09 wants 5); final URL = the collection page for the group (or homepage to test routing); sitelinks, promotions, prices, callouts, structured snippets specific to the group; CTA "Shop now".
8. Signals per group: customer list and top customers; converting search terms as search themes (source 02 says skip themes unless you want aggressive PMax search; source 04 says they matter only for the first 30 days); in-market or custom segments as specific as the group. Never invent themes.
9. Budget: at least $50 a day, ideally $100 (source 01); 3x non-brand CPA floor (source 02). Publish.
10. Check day 1 to 7: brand terms absent from search term insights; channel report shows most spend on Shopping for ecommerce; no unwanted landing pages in the placement report; product spend on the intended SKUs. Expect 4 to 6 weeks of learning; avoid changes that extend it.
11. Rollback: pause the campaign; move budget back to Standard Shopping.

### 4.16 Feed-only PMax (test, not a guarantee)

Goal: push PMax spend toward Shopping and stop drift into YouTube, Gmail and Display. Preconditions: Merchant Center link, eligible products, correct prices and stock, tested purchase value tracking; 15 or more products (source 06/09). Sources: 03, 04, 07, 06/09. Cards: [70544247c36d] [0ac64f9f98bb] [d4571d60eeee] [08b3d9f85868] [5858ab16c0d1] [2fcfa24a9f1f]

1. Use when: PMax drifts into placements you do not want; no strong video or lifestyle creative; you need to separate Shopping spend from video and display spend; an existing PMax overspends on low-value networks; or (source 03) as a layer beside non-brand Shopping.
2. New campaign (source 07: "Create a campaign without guidance") > Performance Max > goal Purchases > select Merchant Center. Name "PMax | <country> | Feed only". `[verify UI]`
3. Bidding: Maximize Conversion Value, no target at launch (source 03 generally does not add one; source 07 adds one only at a plateau after about 3 months). Customer acquisition off. Location Presence where offered. TV screens off. `[verify UI]`
4. Auto-created assets, text, image and video enhancements: off. Asset generation screen: skip; ignore red warnings. Final URL expansion: off. `[verify UI]`
5. 1 asset group "All products feed only" (or per theme) with the listing group set and every asset field empty: no final URL, headlines, descriptions, logos, images or videos. If a prefilled logo or URL remains, delete it; if any single asset remains Google asks for all. Source 07 workaround if the empty group will not publish: publish a filled group, duplicate it, empty the duplicate, publish, pause the original. `[verify UI]`
6. Signals: blank (sources 03, 07). Brand exclusions and brand negatives on (4.17).
7. Publish. Check weekly: channel delivery split (Shopping vs YouTube, Display, Gmail, Search), product results, new vs returning share, contribution and acquisition cost against the existing Shopping or full-asset campaign. Google Help (cited in the cards) says omitting assets does not guarantee Shopping-only delivery and Merchant Center data can generate assets, and low-conversion accounts drift anyway.
8. Do not label it "remarketing only" in any report. Do not set the Standard Shopping priority to High expecting it to outrank PMax (R95).
9. Rollback: pause; or add assets and convert it to a full-asset PMax.

### 4.17 PMax and cold-campaign brand exclusion

Goal: no brand queries in cold campaigns. Sources: 02, 03, 04, 06/09, 01. Cards: [8e83ab723ce9] [ae212dfcabdd] [903e91b5cc9d] [a2f5b3c20d44] [4eceae623d26] [a5827fbc8126]

1. Build the brand list: brand, misspellings, no-space version, brand plus category, brand plus product phrases, from search term reports. `[needs brand data: brand variants]`
2. PMax: campaign settings > Brand exclusions > add the brand list (Google indexes branded terms). Decide on purpose whether Shopping ads may still show on excluded-brand searches (source 06/09 names this option). `[verify UI]`
3. PMax: also add the same terms as exact-match negative keywords on the campaign (a shared "Branded" list where the UI allows; source 03 recorded a support form workaround when it did not). `[verify UI]` `[web check: PMax negative keyword lists]`
4. Non-brand Shopping, non-brand Search, DSA, Demand Gen prospecting: attach the "Branded" negative list; add the brand exclusion where the campaign type offers it.
5. Check daily (new) then weekly: PMax search term insights (7 and 28 days) show no brand terms and no branded conversions; audience report does not skew to existing customers; PMax ROAS is not "unusually strong while the brand campaign starves".
6. Re-check search terms monthly for new brand variants and add them.
7. Rollback: none; removing exclusions re-creates the leak.

### 4.18 Feeder strategy and PMax safety net

Goal: cold reach at scale when PMax has plateaued. Preconditions: PMax plateau confirmed (budget or target changes no longer move backend revenue) or a warm-share finding; margin and cash to fund a low-ROAS cold leg; backend and new-customer reporting. Sources: 04, 10. Cards: [b390a3400b4f] [8ac98b834d71] [29bf1d1ed526] [56795ebc9766] [e2e3fde986ec]

1. Confirm the plateau: 2 budget steps of about 20% with reported ROAS holding and backend revenue flat; or new vs returning shows most PMax conversions are returning. `[needs brand data: backend revenue, new vs returning by campaign]`
2. Feeder (source 04): build a Standard Shopping campaign with broad product coverage and a very low target ROAS (example 50%); run PMax (brand excluded) at a high target ROAS (example 600%) as the warm converter. Or safety net (source 10): manual Shopping, Search and Demand Gen at about 300% to 400% targets, PMax at 600% to 700%.
3. Set the budget split from margin and cash; the sources give none. Set a test length (60 to 90 days is not in the sources; pick one and write it down) and a stop rule (backend new-customer CPA above break-even for 4 weeks).
4. Judge the pair together on backend revenue and new customers, not each campaign's ROAS; Shopping under-attributes beside PMax.
5. Check monthly: PMax share of spend fell as intended; widen the target gap if PMax still dominates. `[web check: current serving rule between PMax and Standard Shopping]`
6. Rollback: raise the feeder's target or pause it; restore PMax's earlier target.

### 4.19 Remarketing lists, customer lists and Demand Gen remarketing

Goal: warm-audience campaigns that answer objections and exclude buyers from prospecting. Sources: 02, 03, 10. Cards: [4bba31df42c6] [8573a3074cc2] [7b6b3c03be03] [061764977d03] [ce4012235cdc] [f2925b7ac7a4] [3f75b0b24b85] [bff4fce7c8df] [4cbf20c9e261] [06762ec1db15] [1010d231578b] [74a36fd11057] [cd21a20937c4] [146aa74746f4] [ffb75a5b8076] [e69a94e940ad] [0997a8f355eb]

1. Sources first: Google Ads tag, the Shopify link, GA4 link through Data manager. Tools > Audience manager: check existing lists and sizes. `[verify UI]`
2. Website visitors: Audience manager > Data segments > plus > Website visitors > "visited a web page" past 30 days (default; the agency normally uses 3 to 7 days), optional URL contains for product or collection; prefill 30 days; wait up to a day; check eligibility per network. `[verify UI]`
3. Cart abandoners: GA4 Admin > Audiences > New: include add_to_cart, exclude purchase; 30 days (60 for low traffic); mark as key audience so it imports; needs GA4 linked. Source 02 example: 4.2K to 3.6K after excluding buyers. About 1,000 to 1,500 people to serve (not universal). `[verify UI]` `[web check: list-size minimums]`
4. Customer list: Audience manager > Customer list; CSV with email, phone, first and last name, zip, country from Shopify or Klaviyo; name with definition and dates; types: all customers, top 5% by revenue or 3 or more purchases; allow a day. Refresh monthly. Consent and Customer Match policy apply. `[verify UI]` `[web check: Customer Match eligibility]`
5. Custom segments: searched terms only (source 02's best-performing type in 2025), competitor sites, or in-market as a PMax or Demand Gen signal.
6. Demand Gen remarketing: New campaign > Sales > Purchases > Demand Gen; product feed off (source 02) or on (source 03; conflict 7.11); Maximize Conversions, no target CPA at first; budget example £50 or $50 a day; country and language at ad group level; TV off; channels YouTube (in-stream, in-feed, Shorts), Discover, Gmail, Display off; audience = the segment as a custom audience, no other signals; optimised targeting off. `[verify UI]`
7. Ad groups by audience: product viewers, add-to-cart non-buyers, checkout abandoners, category viewers, all visitors, past purchasers (upsell). Images and videos in the same campaign (source 10). No lookback windows or exclusions between segments are given.
8. Ads: single image for a strong offer, carousel for range, video for story; up to 20 images, a couple of offer-led headlines, descriptions that close on trust or logistics; 1 objection per ad (complacency: offer plus urgency; price: unit price or comparison; trust: PR and third-party reviews; efficacy: customer photo and review; logistics: shipping, returns, warranty). No brand introduction. Frequency cap 3 a day on video remarketing (source 03).
9. Check after 2 to 4 weeks: ROAS, spend and clicks by audience; segment by network; keep winners, cut losers; push the winning objection answer up-funnel and share with the Meta team.
10. Display remarketing (optional, after video): Display campaign, $10 to $15 a day, Maximize Conversion Value (tROAS only later and low), audience = your data segments > website visitors > all users, optimised targeting off, 1 landscape and 1 square image, 1 to 2 headlines and descriptions, an offer code. `[verify UI]`
11. Rollback: pause; lists stay.

### 4.20 Demand Gen and YouTube prospecting

Goal: create demand beyond search volume. Preconditions: R97 fit check passed; 3 to 5 videos per concept; a conversion mechanism (sales page, advertorial, quiz); customer list for exclusion. Sources: 01, 02, 03. Cards: [87c6c1776dbe] [a1e9a7459f53] [0a48fe8e9e6d] [6803e3b2bebe] [d2116e31fe30] [7d3bf600db06] [dc729c544305] [5d0be265e08e] [417de6079aa3] [2380ca9a554b] [15e16ca20a02] [2d25e7734ec7] [41602f39be64] [12168d012cf1] [9bfa186f1531] [b934c312198e]

1. New campaign > Sales > Purchases only (1 primary action) > Demand Gen. Name "Demand Gen | <country> | <bestsellers or concept> | Conversions". `[verify UI]`
2. Product feed: off (sources 01, 02) or on with bestsellers by item ID (source 03). Conflict 7.11: start off when the ad is a story and the landing page is a sales page; test on when the ad is a product demo.
3. Bidding: Maximize Conversions, goal purchase, no target CPA. Budget: at least $100 a day (source 01) or about 3x AOV (source 02) or by AOV band (source 03). `[needs brand data: AOV]`
4. Location: country. Language: set the market language explicitly (source 01: avoids Spanish-language traffic in the US). Devices: tablets off; TV off until scaling; mobile only when starting with Meta vertical creative; add computers and TV with 16:9 winners later. Ad schedule all day. Google video partners off. `[verify UI]`
5. Ad group channels "Let me choose": YouTube in-stream and Shorts only (in-feed, Discover, Gmail, Display off). Shorts only for a 9:16-only test (source 02). Google requires at least 1 video that fits each chosen format. `[verify UI]`
6. Audience: source 01 fully broad; source 02 three ad groups (search-term custom segment; competitor-site segment; lookalike of converters, reach narrow or balanced) with demographic refinement; source 03 open with at most 3 to 5 search themes and 1 to 2 in-market. Never in-market or affinity alone (source 02), never your own customer or remarketing lists in prospecting (source 03). Exclude the all-time customer list in every ad group. Optimised targeting off while testing; on when scaling (source 01).
7. Ads: video URL from an unlisted YouTube upload; final URL a sales page, advertorial, listicle, quiz or VSL, never the homepage; up to 5 videos per ad group, 3 to 5 per concept; headlines up to 40 characters, long headlines and descriptions up to 90 (use the full length per source 01; 1 to 3 per field per source 03); CTA "Shop now"; business name; sitelinks off; asset optimisation and video enhancements off. Videos under about 60 seconds keep Shorts on; over 60, in-stream only. Change 1 variable between ads when testing.
8. Structure: 1 campaign with a testing ad group and a winners ad group; move the winner to its own group and hook-test against it.
9. Check from day 3: view rate (about 20% in-stream, 10% Shorts), played to 25/50/75/100%, CTR (over 1% in-stream, 0.6% to 1% Shorts), CPM, CPV, frequency; conversions lag 1 to 2 weeks; expect 4 to 6 choppy weeks. Traffic lights per ad (R102). New-customer CPA at campaign level in the attribution tool.
10. After 2 to 4 weeks with a steady CPA over 3 to 5 days: optional target CPA at or slightly below current CPA (source 02), or stay on Maximize Conversions and raise budget to the natural ceiling (source 01). Then raise bids 5% to 10% every 5 to 7 days (source 06/09).
11. Rollback: pause the ad group; keep the winners group.

### 4.21 Bid strategy progression

Goal: move each campaign through stages without starving delivery. Sources: 01, 02, 03, 04, 06/09, 07. Cards: [805871e8952b] [5da4b51eabe6] [5d9dd44f8d9a] [9edd4e9d7860] [a3bf86a930b0] [56cda9478c6f] [29bf1d1ed526] [283cece14dca] [4b56cb53eee4] [d4494776c11a] [3001e5a56d5d]

1. Classify the campaign: new (no recent conversions), building, or mature. Count purchase conversions per campaign over the last 30 days and per account. `[needs brand data: conversions by campaign]`
2. New Search or Shopping: manual CPC with a cap, or Maximize Clicks. Brand campaigns stay on manual or impression share for good.
3. When conversions arrive (10 to 15 Search, 15 to 20 Shopping per source 03; about 30 a month per sources 01 and 02; conflict 7.9): Maximize Conversion Value (Maximize Conversions or tCPA only for fixed order values). New campaigns in an existing account start here, with budget about 3 to 4x AOV. `[verify UI]`
4. At 30 to 50 conversions a month in the campaign (50 for PMax; source 06/09 about 50; source 07 about 3 months for PMax): read actual ROAS and CPA over 30 days; set Target ROAS at or 10% to 15% below actual; hold 2 to 3 weeks; check spend does not collapse. `[verify UI]`
5. Stuck under 50 a month: expand budget or targeting instead of adding a target; consider a portfolio strategy across low-volume campaigns.
6. Later: raise the target in steps of 15% to 20% no more than every 2 to 3 weeks (source 06/09), or hold it and scale budget (source 02). Watch impression share, conversion volume and new-customer share at each step. Add a Max CPC cap through a portfolio strategy if CPCs spike.
7. If spend trails off after a ROAS dip: check stock-outs and seasonality; cut the target aggressively (source 04); consider a period back on Maximize Conversion Value.
8. Rollback: return to the previous strategy; expect 2 to 4 weeks of relearning.

### 4.22 Budget changes

Goal: raise and cut budgets without resetting learning. Sources: 01, 04, 02. Cards: [4175eb319be4] [7003ff9f69ce] [96b95d8a8ec0] [a36358d5ff15] [d40cdd66a2bc]

1. Weekly, per campaign: ROAS vs break-even (conversion-time columns, 7 and 28 days), spend vs budget, lost IS (budget), new-customer CPA.
2. Spending 100% of budget and at or above KPI: raise 10% to 15% (source 01) or about 20% (source 04). ROAS consistently above break-even: raise 10% to 20% a week.
3. Spending under 80% and underperforming: do not raise; loosen the target (lower tROAS, raise tCPA) or fix inputs.
4. Below break-even: pause, adjust or optimise; cut budgets faster than you raise them.
5. "Limited by budget" alone is not a reason (R122).
6. Daily spend far above the daily budget: look for an outside cause (press, podcast); if it is real demand and the mechanism converts, raise hard and keep it while results hold (source 01 case: $1,000 to $20,000 a day).
7. After any bid strategy change, no big budget moves for 2 to 4 weeks.
8. Rollback: return to the last budget; cuts are safe at any speed.

### 4.23 Scaling readiness and scale steps

Goal: add budget or campaign types only when the account can use them. Sources: 06/09, 01, 04, 08. Cards: [abc2dfeeea38] [daa2070d28bf] [af051bd7984a] [8ac98b834d71] [4175eb319be4]

1. Run checklist 5.6 (the 5 gates). Any fail: fix inputs, not budget.
2. Confirm the campaign hits target ROAS at the current budget (source 08).
3. Pick the lever in order: budget step (4.22); bestseller focus and SKU exclusions; new asset groups or creative; layer Standard Shopping beside a plateaued PMax (4.18); add non-brand Search on proven PMax terms; add Demand Gen or YouTube (4.20); cold Search and Display last.
4. After each step wait 2 to 4 weeks; judge on backend revenue, new customers and MER, expecting ROAS to fall as spend rises.
5. Rollback: step the budget back; pause the newest layer first.

### 4.24 Daily, weekly and monthly routines

Sources: 01, 02, 07, 04. Cards: [a5827fbc8126] [5ebe76f05300] [64c009e7bc50] [67af52d7623d] [b9ecdf07948a] [d40cdd66a2bc] [031ec7c8b2d2] [2bf868bfb28d] [12e5a4881580] [423e6a50781c]

Daily (10 to 20 minutes):
1. Spend vs budget per campaign; any spend anomaly gets an outside-cause check.
2. PMax search term insights (7 and 28 days) and Shopping or Search search terms: exclude irrelevant terms; brand terms in cold campaigns mean a broken exclusion; note new keyword ideas. New campaigns daily; stable ones at least twice a week.
3. Auction insights: impression share vs named competitors on Search and Shopping.
4. Merchant Center: new disapprovals.

Weekly (Sunday per source 07):
1. Campaign read on conversion-time columns: cost, conversions, value, CPA, ROAS, CTR, impression share, lost IS (budget and rank), week over week, not day to day.
2. PMax: Campaign > Products for SKU spend; exclude non-converting SKUs via listing groups; asset details per group, replace low or no-spend assets; landing page and placement reports, exclude bad URLs.
3. Budget and target decisions per 4.22 and 4.21 (the only weekly levers: tROAS, budget, remove keywords, remove products).
4. Merchant Center: fix new red and yellow items; feed updates for stock and price.
5. Search ads: read asset performance; keep winners, cut losers, add 1 new angle.
6. YouTube or Demand Gen: traffic lights per ad; move winners; refresh creative.

Monthly:
1. Replace non-converting PMax search themes with converting queries.
2. Refresh the customer list upload; check exclusions still apply.
3. Review Maximize Conversion Value vs Target ROAS per campaign; check for the death spiral pattern.
4. Site vs Merchant Center policy check (4.8); promotions with correct end dates.
5. Reconcile Google purchases with backend orders; MER by channel; brand vs non-brand split; new vs returning by campaign.
6. Structure audit (5.3) every quarter or after any major change.

### 4.25 Diagnose an underperforming account (fixed order)

Goal: find the root cause before touching anything. Source: 05, with 01 and 02. Cards: [7c50191f8854] [62403f6f3b48] [7fe2bb1f5bff] [e2a87175fcd5] [26676d575992] [31ee29611482] [4e3675b7a020] [141c23b0306c] [2069300bf455] [6ff74a04932d] [86ca17cab286] [2795573cf2d6] [caf9cb9b298e] [5df8489778d1] [817f1a421116]

Step 0, before anything: change history in Google Ads, Meta, TikTok and the site; ask the client what changed; extend the window (never 1 day); switch to conversion-time columns for the last 7 days. If a batch of your own changes just went in, wait. `[verify UI: change history; conversions by conversion time]`

Level 1, business (about 5 minutes):
1. Media mix by spend share. Google at 10% of spend (about half of it brand) is almost never the cause; at 65/35 check the bigger channel first; at 65% Google, Google first. `[needs brand data: spend by platform]`
2. What changed outside Google: end of a sale, Meta creative refresh, offer change, site change, price change, stock.
3. Revenue = conversion rate x AOV x sessions. Conversion rate down: the website. Sessions down: which source lost clicks. AOV down: product mix in ads or a site merchandising change; split new vs returning AOV, then units per order and average unit price.
4. True KPI (revenue, profit, MER, aMER) vs attributed number. Platform down but business flat: suspect tracking or attribution.
5. Seasonality vs forecast. Inside the forecast: stop.

Level 2 and 3, account and campaign (about 5 minutes):
6. Date range 90 to 180 days, weekly view, Overview tab; rotate cost, conversions, value, CPA, ROAS, CTR; find the inflection date.
7. Campaigns sorted by cost; top 5 only; which changed after the date; then ad groups or asset groups.
8. Record campaign type and the specific campaigns.

Level 4, campaign-type checks:
9. PMax: brand terms in search terms; audience report skew to existing customers; top-spend products out of stock, off or disapproved; Merchant Center errors; tROAS raised (new-customer ROAS by target level); product bloat and stock churn.
10. Shopping: tROAS; Merchant Center (stock, changed titles or descriptions, errors, warnings); too many products; search partners spend.
11. Search: search terms before vs after by spend; auction insights before vs after (new entrant); tROAS; Display Network on.

Level 5, metric and sub-metric:
12. Efficiency down, volume flat: CPA = CPC / conversion rate. CPC up: Quality Score columns (expected CTR, ad relevance, landing page experience) before vs after; new competitor; premium auctions from a bidding change (only a problem if conversion rate did not rise). Conversion rate down, in order: tracking; landing page (URL switch, page change, price, redirect, upsell, merchandising); audience (search terms, bidding change); learning reset from a structural change; offer (promo ended, shipping threshold).
13. Volume down, efficiency flat: clicks = impressions x CTR. Impressions down: lost IS (budget) if the budget is hit; lost IS (rank) if clicks and impressions both fell on steady spend (fix quality, competition, aggressiveness). CTR down: stale seasonal copy; audience shift; competitor price cut on Shopping (check competitor prices; ad fatigue is rare on Google).

Level 8, root cause and fix:
14. Write the root-cause sentence. If you cannot, do not touch the account.
15. Severity: dire allows many fixes at once; mild means 1 isolated fix.
16. Estimate the fix's size honestly; a headline change does not fix a business decline.
17. Apply a fix, not a rebuild; wait long enough for the conversion volume to show a read; rebuild only if fixes cannot close the gap.
18. Deliverable: the diagnosis document in 9.1.

### 4.26 Restructure an account toward consolidation

Goal: fewer, fuller campaigns with a reason for each. Source: 04, with 01 and 02. Cards: [379b1f714127] [a715afa0c38a] [8d6cc6ef07b8] [329599511dc8] [4692423b2426] [2792071d2d2e]

1. List every campaign with 30-day conversions, ROAS, spend and role. `[needs brand data: campaign-level data]`
2. Flag same-product campaigns where ROAS falls with conversion volume; flag campaigns with no role; flag tiny campaigns.
3. For each campaign write the reason it exists: brand vs non-brand, country, margin or efficiency tier, category or persona, clearance or new arrivals, hero SKU. No reason: merge into the highest-volume campaign of the same role.
4. Where a split must stay but learning is thin, apply a portfolio bid strategy across the group.
5. Fix the 7 common setup faults while there: GA4 as primary, 1 PMax asset group, broad match with Maximize Clicks, Display on Search, no negatives, auto-apply recommendations on, no naming convention.
6. Change in stages: 1 merge at a time, 2 to 4 weeks apart; judge on backend revenue, not only in-platform ROAS.
7. Rollback: re-enable the paused campaigns; history is intact if nothing was deleted.
