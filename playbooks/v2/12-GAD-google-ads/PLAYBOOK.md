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
