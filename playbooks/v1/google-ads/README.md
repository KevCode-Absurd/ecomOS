# Google Ads — draft playbook

**Status:** source-linked draft; not owner-approved or outcome-tested.

Read [the operating contract](../OPERATING_CONTRACT.md) before using a workflow.

## Inputs
- Feed/catalog
- campaign/search-term reports
- conversion setup
- margins
- goals

## Measures
- Contribution
- purchase CPA
- ROAS
- qualified search demand

## Foundation candidates
Inferred principle labels do not establish universal applicability. Retain source conditions; empty means no matched labelled principle, not absence of foundational knowledge.

- **Treat the Product Feed as the Advertising Copy** (`7671c6e57a6e5965b133722a`): In Shopping and PMax there are no keywords — Google reads your feed title, description, attributes, price and availability to decide which queries each product matches.
  Applies when: You are optimising Google Shopping or Performance Max for ecommerce and deciding where to spend merchandising and copywriting effort.
  Condition: Source's claim that the title is 'the most important line of advertising copy you will ever write' is a strong practitioner opinion specific to feed-led campaigns.
  Condition: Feed classification errors can cause a well-written title to still match poorly.

- **Read the Shopping and PMax Auction Correctly** (`c7807eeedee7005d4d904acd`): In Shopping and PMax there are no keywords — quality signals come from feed data, so product titles and attributes drive Ad Rank.
  Applies when: Explaining why a product wins or loses Shopping auctions, or deciding where to invest to improve visibility and CPC.
  Condition: Source-cited 2026 averages (Search CPC ~$1.42, Shopping ~$0.68, PMax ~$0.82; blended ROAS 4.2×; Shopping ROAS 5.1×, Search 3.4×, PMax 4.8×) are benchmark aggregates that vary by vertical and margin — not targets.
  Condition: Google Shopping CPCs were cited as up 22% year over year, making feed efficiency more important but also making old CPC assumptions unreliable.

- **Standard Shopping for SKU-Level Bid Control** (`f2e339bd5505c24c503bf11d`): Use Standard Shopping when you need product-group bid control, clear per-product query data and read-clean conversions that PMax blurs.
  Applies when: Deciding which products belong in Standard Shopping versus PMax, or when PMax reporting is too blended to tell what is actually working.
  Condition: Standard Shopping only serves the Shopping surface — it does not reach YouTube, Display, Gmail or Discover.
  Condition: Running Shopping and PMax on the same feed without role separation causes direct cannibalisation.

## Audit an ecommerce Google Ads account
Workflow ID: `google-ads.audit-retail-search`

**Deliverable:** Account audit and ranked action plan

### Proposed decision sequence
1. Validate purchase tracking and margin context
2. Separate brand/nonbrand and product-level performance where supported
3. Prioritise feed, query and budget hypotheses with evidence

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Standard Shopping for SKU-Level Bid Control
Card: `f2e339bd5505c24c503bf11d` · Source: # Google Ads for Ecommerce_ The Complete Architecture & Operations Manual (2026 Edition).docx · Section: 0

Use Standard Shopping when you need product-group bid control, clear per-product query data and read-clean conversions that PMax blurs.

Applies when: Deciding which products belong in Standard Shopping versus PMax, or when PMax reporting is too blended to tell what is actually working.

- Route hero SKUs here when you need to defend top impression share on your most important products.
- Set aggressive product-group bids on high-margin products where the unit economics can absorb higher CPCs.
- Use Standard Shopping for clearance inventory you must move quickly, accepting a lower ROAS target on those product groups.
- Test new arrivals here first: Standard Shopping gives per-product query and conversion data you can read before deciding what to scale into PMax.
- Keep in mind both campaign types bid against the same feed; when running in parallel, duplicate the feed and give Shopping the branded/high-intent version and PMax the discovery version.
- Where attribution clarity matters across multiple sales channels, prefer reading Standard Shopping conversions over PMax's blended number that mixes Shopping, Display, YouTube and Search.
- **Condition:** Standard Shopping only serves the Shopping surface — it does not reach YouTube, Display, Gmail or Discover.
- **Condition:** Running Shopping and PMax on the same feed without role separation causes direct cannibalisation.

#### Match failure modes to campaign type: PMax and Shopping
Card: `4e3675b7a020bb07760c9416` · Source: How To Fix An Underperforming Google Ads Account.docx · Section: 0

Why identifying the campaign type first matters, and the specific failure modes to check for PMax and Shopping.

Applies when: When a Google Ads decline has been traced to a specific campaign and you need to know what to inspect.

- Understand that PMax, Shopping and Search decline for different reasons, so establish campaign type before troubleshooting.
- PMax / Shopping check 1 — warm/cold drift: check the search term report for brand terms and the audience report for skew toward existing customers. If brand terms are appearing despite exclusions, or the audience skews warm, the exclusion is broken or target ROAS is pushed too high.
- PMax / Shopping check 2 — feed health: feed quality drives most Shopping performance (the speaker says 80–90% of PMax performance comes from Shopping). Check products in the campaign for out-of-stock, turned-off or disapproved items, and verify the GMC feed for errors and warnings, including changed titles or descriptions.
- PMax / Shopping check 3 — target ROAS: raising tROAS narrows targeting toward warmer, higher-conversion-probability buyers, likely pulling spend back and hurting new-customer acquisition. Cross-check new-customer ROAS in a third-party tool or natively in Google Ads; a higher tROAS typically shows worse NC ROAS.
- PMax / Shopping check 4 — product bloat and stock churn: a rapidly growing SKU count flooding one campaign can hurt learning, and high-spend products going in and out of stock reset that product's learning and can affect the whole campaign.
- Also check whether spend is being distributed into search partners with poor performance.
- **Condition:** The 80–90% figure is the speaker's stated observation, not a measured benchmark.
- **Condition:** Brand exclusion should already be in place — the check is a double-check, not a fix in itself.

#### Stop PMax and Shopping Cannibalising Brand Demand
Card: `4eceae623d26c2b80f95343f` · Source: # The Complete Google Ads Architecture & Operations Manual (2026 Edition).docx · Section: 0

Three parallel fixes — brand negatives on PMax, negatives on new-customer campaigns, and dedicated branded campaigns — keep PMax from eating the highest-intent commercial traffic.

Applies when: PMax and Shopping run against the same feed and you suspect PMax is absorbing branded and high-intent queries, destroying cost transparency on your most valuable searches.

- Add branded negative keywords and brand exclusions to PMax campaigns so PMax cannot bid on branded queries.
- Add negative keywords to new-customer-acquisition Search and Shopping campaigns so they do not absorb branded demand and get falsely credited.
- Create dedicated branded Search and Shopping campaigns to collect only branded traffic, with uncapped budget relative to search volume — losing brand impression share to a competitor is one of the most avoidable ways to lose pipeline.
- Optimise branded campaigns on efficiency metrics (ROAS, CPC, impression share), not growth metrics.
- Use feed duplication with strict role rules: the Shopping feed optimised for branded and high-intent category terms, the PMax feed optimised for discovery and scaling, so both can surface products across eligible auctions without sacrificing efficiency.
- Confirm the current location of brand exclusion settings (account vs campaign level) in the live interface.
- **Condition:** Splitting traffic will initially make your account-level ROAS look worse because brand efficiency no longer flatters non-brand; that is the intended transparency gain.
- **Condition:** Source presents this as the single most common structural failure; treat it as a frequent pattern, not a claim about every account.

### Retrieval and applicability
Search: `Google Shopping PMax brand conversion feed margin`
Related domains: measurement, finance-and-accounting, landing-pages
Mixed-folder candidate IDs: 0d34948521a961485602c895, ed7c1f01178816b95a5b2d32, 6e67e3c7c4432dabff6f7ff2

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

## Improve a product feed
Workflow ID: `google-ads.improve-feed`

**Deliverable:** Feed correction specification

### Proposed decision sequence
1. Check product identity, required attributes and landing-page consistency
2. Improve titles and attributes using actual product facts
3. Validate disapprovals and measure changes at a comparable grain

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Feed product titles with informative keywords
Card: `0d729814ee3064f7b6486305` · Source: Full Ecom Google Ads Course 2026 (100% FREE).docx · Section: 1

Write Merchant Center product titles that include the full product name, key attributes, and brand so Google matches them to the right searches.

Applies when: Optimizing Merchant Center product data before running Shopping campaigns.

- Put the highly necessary product details first in the title, then attributes, then the brand name at the end.
- Example structure: 'Black Non-Stick Frying Pan 38cm Diameter, Peter's Pans'.
- Include keywords that reflect what shoppers actually search, so Google can target the product ad to the right queries.
- Fill every available field (title, description, product type, category, price, sale price, GTIN, etc.) with high-quality information.
- If you have a GTIN, include it; if not, do not worry and still complete the rest.
- Do not agonize over perfection at this stage — get a correct, informative setup live first; deep optimization is a separate, longer effort.
- **Condition:** Title keyword strategy must not include terms your product is not (see incorrect-attribute warning card).

#### Focus Feed Optimization on Price, Title and Image
Card: `1f2977dd9a2ce295d93ee901` · Source: Ecommerce Google Ads 2026 Free Course.docx · Section: 3

In Shopping you cannot choose the queries you serve, so direct roughly 95% of feed effort into price, product title and product image.

Applies when: Deciding where to spend merchandising effort when Shopping performance is weak and you cannot manipulate query targeting.

- Accept the constraint: with Shopping ads you don't pick search queries the way you do in Search campaigns; Google matches your feed to queries.
- Concentrate effort on the three attributes the source says drive roughly 95% of Shopping performance: price, product title and product image.
- Set price competitively relative to the listings you appear beside, since price is visible in the Shopping unit and feeds directly into perceived value.
- Rewrite titles using the core type → features/benefits → specifics → brand structure.
- Upgrade images per the resolution, focus and lifestyle-test guidance.
- Treat remaining feed attributes (descriptions, GTINs, custom labels) as secondary but keep them accurate; ensure every variant has its own unique GTIN and correct identifier codes, which sync reliably when Shopify is connected to Merchant Center.
- **Condition:** The '95%' figure is the presenter's heuristic emphasis, not a measured attribution model.
- **Condition:** Verify current Merchant Center attribute requirements and sync behaviour before relying on automatic Shopify population.

#### Treat the Product Feed as the Advertising Copy
Card: `7671c6e57a6e5965b133722a` · Source: # The Complete Google Ads Architecture & Operations Manual (2026 Edition).docx · Section: 0

In Shopping and PMax there are no keywords — Google reads your feed title, description, attributes, price and availability to decide which queries each product matches.

Applies when: You are optimising Google Shopping or Performance Max for ecommerce and deciding where to spend merchandising and copywriting effort.

- Accept that your feed is not a data source but the advertising itself: Google scans titles, descriptions, attributes, pricing and availability and decides on its own which search queries each product matches.
- Therefore treat the product title as the most important line of advertising copy you will write, because it determines what Google thinks you sell and who to show it to.
- Front-load the attributes buyers actually search with (structure below) rather than leading with brand and model name.
- Maintain accuracy of price and availability so Google's matching and any automatic item updates stay aligned with your landing pages.
- Re-audit the feed whenever you add categories or price tiers, since matching is driven by feed content, not keyword bids.
- Confirm current matching behaviour in Google Merchant Center documentation, as the algorithm evolves.
- **Condition:** Source's claim that the title is 'the most important line of advertising copy you will ever write' is a strong practitioner opinion specific to feed-led campaigns.
- **Condition:** Feed classification errors can cause a well-written title to still match poorly.

### Retrieval and applicability
Search: `feed title attribute product shopping merchant`
Related domains: measurement, finance-and-accounting, landing-pages
Mixed-folder candidate IDs: 6e67e3c7c4432dabff6f7ff2, ac4bf9ad64fd12e1ce92b00e, 7421bd80f1529f7e897598b5

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

## Plan a retail search campaign structure
Workflow ID: `google-ads.plan-retail-campaign`

**Deliverable:** Campaign plan with verification requirements

### Proposed decision sequence
1. Group products by business economics and shopper intent
2. Choose a structure fitting available data and creative assets
3. Define budget, tracking and evaluation before execution

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Standard Shopping for SKU-Level Bid Control
Card: `f2e339bd5505c24c503bf11d` · Source: # Google Ads for Ecommerce_ The Complete Architecture & Operations Manual (2026 Edition).docx · Section: 0

Use Standard Shopping when you need product-group bid control, clear per-product query data and read-clean conversions that PMax blurs.

Applies when: Deciding which products belong in Standard Shopping versus PMax, or when PMax reporting is too blended to tell what is actually working.

- Route hero SKUs here when you need to defend top impression share on your most important products.
- Set aggressive product-group bids on high-margin products where the unit economics can absorb higher CPCs.
- Use Standard Shopping for clearance inventory you must move quickly, accepting a lower ROAS target on those product groups.
- Test new arrivals here first: Standard Shopping gives per-product query and conversion data you can read before deciding what to scale into PMax.
- Keep in mind both campaign types bid against the same feed; when running in parallel, duplicate the feed and give Shopping the branded/high-intent version and PMax the discovery version.
- Where attribution clarity matters across multiple sales channels, prefer reading Standard Shopping conversions over PMax's blended number that mixes Shopping, Display, YouTube and Search.
- **Condition:** Standard Shopping only serves the Shopping surface — it does not reach YouTube, Display, Gmail or Discover.
- **Condition:** Running Shopping and PMax on the same feed without role separation causes direct cannibalisation.

#### Use Brand Exclusions and Weigh What Actually Matters in PMax
Card: `903e91b5cc9db4d2b7bb7093` · Source: The Only Google Ads Strategy You Need for 2026.docx · Section: 1

Without brand exclusions a PMax campaign is effectively a retargeting campaign; the source ranks the variables that move PMax performance.

Applies when: Configuring or prioritising fixes inside an ecommerce PMax campaign.

- Exclude your brand from PMax. Two methods exist: (1) campaign settings → brand exclusions → add new brand, let Google index your branded terms and apply the brand list; (2) the newer capability to add negative keywords directly to PMax. The source recommends doing both as fail-safes so a missed variation is still caught by the list and vice versa.
- After running PMax across ~250 accounts and consulting on ~400 more, the source ranks variables in this order: (1) the GMC feed — titles, descriptions, imagery (assuming PMax is prioritising Shopping); (2) brand exclusions; (3) asset and listing group structure plus the assets themselves; (4) bidding strategy; (5) audience signals and search themes.
- Search themes and audience signals are signals, not targeting — they do not guarantee bids on those terms. Prioritise keywords that historically converted in your account rather than inventing them.
- For mature accounts spending tens of thousands per month, the source reports audience signals and search themes are roughly a 1% lever at best; they matter mainly on new business, new product, new category or new asset group launches, where there is no conversion history.
- Once a campaign has ~30 days of conversion data, Google bypasses the audience signal — the source states you could remove it with no performance impact.
- Verify current interface locations for brand exclusion and negative keyword settings before acting, as Google changes these.
- **Condition:** The ranking and agency-tested figures are the source's own observations, not published benchmarks.
- **Condition:** The claim that audience signals stop mattering is explicitly flagged as potentially controversial.

#### Set Up a Standard Shopping Campaign (Not PMax)
Card: `43c52017c399aea1ab05ee6b` · Source: Ecommerce Google Ads 2026 Free Course.docx · Section: 3

Configure a standard Shopping campaign with sales objective, purchases-only conversion goal and presence-only location targeting.

Applies when: Launching a DTC store's first Shopping campaign in Google Ads.

- Confirm prerequisites first: conversion tracking installed, Merchant Center account created and linked to Google Ads.
- In ads.google.com go to Campaigns → the blue plus → objective Sales; set the conversion goal to purchases.
- When Google pushes Performance Max, decline and choose Standard Shopping instead (the source's recommendation for this setup).
- Select the linked Merchant Center account from the product drop-down and name the campaign to encode scope: channel, product count, and jurisdiction (e.g. 'Shopping | All Products | UK').
- Set an average daily budget; choose a bid strategy guided by account maturity — manual CPC or Maximise Clicks for new accounts, Target ROAS once conversion data exists.
- In campaign settings, set the location, then open Location options and switch from 'Presence or interest' to 'Presence' so you only pay for people actually in your target market.
- Turn off Search Partners — the source reports consistently weak performance there for these campaigns.
- In ad group settings name the group, set a max CPC if on manual bidding, and choose products by all products, product type/category, item ID, or custom labels (e.g. seasonality, bestsellers) before saving.
- Publish; ads typically start serving within a couple of hours.
- **Condition:** Bid strategy choice depends on account history — the source points to a separate bid strategy lesson rather than one universal rule.
- **Condition:** Custom labels for seasonality/bestsellers must first be built in Merchant Center.
- **Condition:** Ad interface element names and PMax defaults change frequently; verify the current UI.

### Retrieval and applicability
Search: `Shopping PMax asset groups campaign structure bidding`
Related domains: measurement, finance-and-accounting, landing-pages
Mixed-folder candidate IDs: 2b7d05cb2e3f65ccef03542e, 8c4e6e2d406bfb52a74c2d3c, fb780cdc68aaf637eac0cfb9

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
