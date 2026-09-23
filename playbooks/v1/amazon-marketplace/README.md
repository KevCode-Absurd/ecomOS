# Amazon Marketplace — draft playbook

**Status:** source-linked draft; not owner-approved or outcome-tested.

Read [the operating contract](../OPERATING_CONTRACT.md) before using a workflow.

## Inputs
- Marketplace/country
- SKU economics
- listing
- fees
- stock
- account/report access

## Measures
- Contribution
- conversion
- inventory availability
- return rate

## Foundation candidates
Inferred principle labels do not establish universal applicability. Retain source conditions; empty means no matched labelled principle, not absence of foundational knowledge.

- **Choose FBA or FBM before setting up a seller account** (`79cb4207ec9548d50a9d074a`): FBA hands pick/pack/ship to Amazon for per-order fees; FBM means you ship yourself, and the source's preference is FBA for a semi-passive operation.
  Applies when: Deciding your fulfilment model before registering an Amazon seller account or sourcing inventory.
  Condition: Source is a single practitioner's preference, not a benchmark; FBM is not inherently worse.

- **Compare FBA vs FBM Before Choosing Fulfillment** (`82518c27f0d1ee180403e4ac`): FBA is convenient and hands-off but costs per order; FBM keeps you responsible for shipping at a similar total cost.
  Applies when: Deciding how orders on your Amazon listings should be fulfilled.
  Condition: FBA fee schedules change; confirm current rates for your product dimensions in Seller Central.
  Condition: The source does not provide a universal rule for when FBM wins — it says costs are roughly comparable, so re-evaluate for your own SKU.

- **Compare FBA and merchant fulfillment for the actual product** (`e94ff8c9c6e704d5d42f4f86`): Evaluate delivery eligibility, total costs and operational capacity rather than assuming FBA guarantees higher sales.
  Applies when: Fulfillment model choice for a new listing, or deciding whether to migrate seller-fulfilled SKUs into FBA.
  Condition: Source sales uplifts are individual cases; check current program requirements in the selling marketplace.

## Improve an Amazon product listing
Workflow ID: `amazon-marketplace.listing-copy`

**Deliverable:** Listing copy and asset brief

### Proposed decision sequence
1. Verify product facts and marketplace-specific requirements
2. Map shopper questions to title, bullets and supporting assets
3. Draft accurate copy and identify unsubstantiated claims

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Apply Conversion Psychology to Packaging and Listings
Card: `d0428dbc14f4a6be51e9a3c3` · Source: FREE Amazon FBA Course _ 12 Hour FULL Step by Step Tutorial 2025.docx · Section: 1

Treat branding and listing content as premium presentation tools that justify higher prices and improve conversion.

Applies when: Product-page and merchandising decisions: writing your title, bullets, images and designing packaging to convert more visitors.

- Recognize that two identical products can sell at different prices if one appears more premium — the source's core argument for investing in branding and packaging, since cost to produce is the same.
- Use this to price higher: better presentation supports premium pricing rather than competing on lowest price.
- On the listing, use the assets Amazon gives you: title, images, bullet points, and (with Brand Registry) enhanced brand content images in the description.
- Frame content around buyer benefits so shoppers choose your product over competitors at the same search position.
- Apply before building the listing, not after: decide brand positioning and packaging first, since these are inputs to the listing and to your price.
- **Condition:** This is the presenter's stated approach; specific conversion lifts are not measured in the source.
- **Condition:** Brand-Registry-gated features require a trademark application.

#### Set up a seller account you can actually trade from
Card: `3f1b8c4c61475e58d0fd861c` · Source: Beginners Guide To Amazon FBA In 2025 (1).docx · Section: 0

The account needs verified identity, a linked bank account and the correct plan before any listing work begins.

Applies when: Preparing a newly approved seller account before adding your first ASIN.

- Before you can sell, complete the tasks the dashboard flags, including adding the bank account Amazon will use to pay you and to charge fees.
- Do not begin sourcing or shipping until verification has passed and payment details are registered, otherwise you cannot receive funds.
- Keep your proof of ID and proof of address consistent with the name on the account so future reviews or reinstatements are simpler.
- Set your account to the correct marketplace and only enable the marketplaces you actually intend to sell in when creating listings, so you do not accidentally expose stock abroad.
- Treat the account as the asset: the source notes suspensions are a real risk, and appeals are harder once a prior suspension exists.
- **Condition:** The exact dashboard tasks and screens change; follow the current on-screen guidance.

#### Keyword variability test: count the ways a product is searched
Card: `c7f835842a7659d4160fd222` · Source: COMPLETE Amazon FBA Product Research Masterclass.docx · Section: 0

Prefer products describable by many distinct long-tail keywords so you can rank on multiple first-page terms instead of one contested head term.

Applies when: Deciding between two candidate products, or judging whether a niche offers cheap organic entry for a new Amazon listing.

- Take your candidate product and list the distinct ways a customer might search for it — the source's phone-case example: slim, green, wallet, waterproof, for men, for women.
- Prefer products with dozens or hundreds of descriptive variants; these give many low-hanging long-tail terms to target in listing copy and launch PPC.
- Discard or downgrade products with only one or two monolithic keywords — ranking becomes a single contested battle with no cheap entry points.
- For ecommerce merchandising, apply the same test when writing PDP titles and bullet copy: cover the distinct descriptive variants rather than repeating one head term.
- Validate the actual search demand for each variant in a keyword tool before building the listing around it.
- **Condition:** The source gives no numeric minimum for 'enough' keywords — 'dozens' and '10/20/30/100' are illustrative.
- **Condition:** Keyword counts and search volumes change over time; re-verify before committing.

### Retrieval and applicability
Search: `Amazon listing title benefit proof conversion`
Related domains: sourcing, finance-and-accounting, ad-copy-deployment
Mixed-folder candidate IDs: aefe14739fde12f907f36e98, 7421bd80f1529f7e897598b5, eff569999325c2cbb5571174

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

## Evaluate marketplace SKU economics
Workflow ID: `amazon-marketplace.sku-economics`

**Deliverable:** SKU economics and decision brief

### Proposed decision sequence
1. Compare fulfilment models with applicable fees and landed costs
2. Account for returns, advertising and inventory exposure
3. Show sensitivity and decide what evidence is missing

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Choose FBA or FBM before setting up a seller account
Card: `79cb4207ec9548d50a9d074a` · Source: Beginners Guide To Amazon FBA In 2025 (1).docx · Section: 0

FBA hands pick/pack/ship to Amazon for per-order fees; FBM means you ship yourself, and the source's preference is FBA for a semi-passive operation.

Applies when: Deciding your fulfilment model before registering an Amazon seller account or sourcing inventory.

- Understand the two models: FBA (Fulfilment by Amazon) means you send stock to Amazon's warehouse and they pick, pack and ship each order, charging fulfilment fees that reduce your margin. FBM (Fulfilment by Merchant) means you ship every order yourself.
- Source view: the presenter chooses FBA because he wants a lifestyle, semi-passive business rather than packing orders at home. Treat this as his personal preference, not a universal rule — FBM can suit heavy, fragile, low-volume or made-to-order items.
- Note that your choice changes the fee lines in every profitability calculation, so fix the model before you analyse products.
- If in doubt, run one small FBA test batch and compare actual per-unit fulfilment fees against your own shipping cost before committing your full range.
- Verify current fee schedules and programme terms in Seller Central, as Amazon changes them.
- **Condition:** Source is a single practitioner's preference, not a benchmark; FBM is not inherently worse.

#### Compare FBA vs FBM Before Choosing Fulfillment
Card: `82518c27f0d1ee180403e4ac` · Source: FREE Amazon FBA Course _ 12 Hour FULL Step by Step Tutorial 2025.docx · Section: 14

FBA is convenient and hands-off but costs per order; FBM keeps you responsible for shipping at a similar total cost.

Applies when: Deciding how orders on your Amazon listings should be fulfilled.

- Understand FBA (Fulfilled by Amazon): Amazon picks, packs, and ships each order for a per-unit fee. In the case studies this ran $38 to $4,400 in a month depending on volume.
- Understand FBM (Fulfilled by Merchant): you ship orders yourself, and per the source the total cost often ends up similar, so the deciding factor is your time and capacity, not solely cost.
- For a solo operator who wants to avoid daily post-office trips, FBA removes the packing and outbound logistics work at the cost of per-order fees.
- Remember FBA does not eliminate storage risk: unsold FBA inventory accrues long-term storage fees after 180 days, so fulfillment choice does not solve the overstocking problem.
- Model your category's actual FBA fee per unit against your margin before committing, since the fee scales with size and weight and was one seller's second-largest cost line.
- **Condition:** FBA fee schedules change; confirm current rates for your product dimensions in Seller Central.
- **Condition:** The source does not provide a universal rule for when FBM wins — it says costs are roughly comparable, so re-evaluate for your own SKU.

#### Anti-portfolio: products to avoid when selecting an FBA item
Card: `680f24307e2ab558d2196eb2` · Source: COMPLETE Amazon FBA Product Research Masterclass.docx · Section: 0

Reject cheap, seasonal, trendy, gated, and patented products before spending on inventory to avoid dead stock and price wars.

Applies when: Screening candidate products for a new Amazon FBA listing before committing capital to inventory.

- Rule out cheap products (roughly under $10 retail): the source argues a $7–8 flimsy item generates bad reviews, invites low-barrier competitors, and lets PPC clicks of about $1 consume all profit within two or three clicks.
- Reject seasonal and trend-driven items, which leave you holding unsellable inventory and paying long-term storage fees once demand passes.
- Reject restricted/gated categories and patented products — the source reports having ordered inventory he then could not sell because Amazon blocked the category or the item was patented.
- Treat these as elimination criteria first, before evaluating upside: the speaker claims applying them saves tens of thousands of dollars, and that getting product selection wrong means failure.
- Note this is one seller's opinion and heuristic, not a platform rule; verify current category gating and IP status per item before ordering.
- **Condition:** The $10 price floor and '$1/click' figure are illustrative from the source, not measured benchmarks.
- **Condition:** Some sellers profitably run cheap or seasonal products; the source's guidance assumes a paid-PPC-led launch model.

### Retrieval and applicability
Search: `Amazon FBA FBM fees contribution inventory ROI`
Related domains: sourcing, finance-and-accounting, ad-copy-deployment
Mixed-folder candidate IDs: 2e790ab86c57db643416435b, 1035e4c1ce18c3c7e36835c2, cb72f5171b60d51280f77753

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

## Audit marketplace readiness
Workflow ID: `amazon-marketplace.marketplace-audit`

**Deliverable:** Marketplace readiness audit

### Proposed decision sequence
1. Check buyability, listing consistency and stock readiness
2. Review available account and conversion issues
3. Prioritise corrections and verify current marketplace rules

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Compare FBA and merchant fulfillment for the actual product
Card: `e94ff8c9c6e704d5d42f4f86` · Source: FREE Amazon FBA Course _ 12 Hour FULL Step by Step Tutorial 2025.docx · Section: 11

Evaluate delivery eligibility, total costs and operational capacity rather than assuming FBA guarantees higher sales.

Applies when: Fulfillment model choice for a new listing, or deciding whether to migrate seller-fulfilled SKUs into FBA.

- Compare current FBA fees, storage and inbound costs with the merchant's own shipping and service costs.
- Assess delivery promises, stock availability, returns and operating capacity for the product.
- FBA can provide Prime eligibility; qualifying merchants may also use Seller Fulfilled Prime where available.
- Test conversion and contribution where practical rather than assuming a fixed sales multiplier or direct ranking boost.
- Choose FBA, merchant fulfillment or a mix using actual economics and service requirements.
- **Condition:** Source sales uplifts are individual cases; check current program requirements in the selling marketplace.

#### Reading FBA Inventory Breakdown: FC Transfer, FC Processing, Reserved
Card: `13ee6100527e366a3205edf9` · Source: How to Start Amazon FBA in 2026.docx · Section: 0

Use Seller Central's FBA inventory breakdown to diagnose where units are between shipment and sellable, and interpret FC transfer vs FC processing vs reserved states.

Applies when: When units you shipped to Amazon are not yet sellable and you need to know where they are, whether they're lost, or when to escalate for reimbursement.

- Go to Seller Central → Manage All Inventory, and under the SKU condition scroll to the FBA Inventory Breakdown section.
- Read the statuses: 'FC transfer' means Amazon is dispersing units among different fulfillment centers; 'FC processing' means units are at their final warehouse being opened, scanned in, and shelved — this phase takes a while.
- Expect transit to Amazon to be fast (source cites ~3–4 days) but check-in/processing to be the long part.
- Benchmark timing: the source considers 1–2 weeks for check-in normal; beyond 2 weeks she begins investigating reimbursement, though Q4 (Oct–Dec) check-in can legitimately take a month due to demand.
- If units are not received in full, use the reimbursement process (SellerBoard provides a template to paste into Seller Support) to recover lost units.
- Confirm Amazon sometimes splits one shipment across multiple fulfillment centers — seeing units in FC transfer is expected, not an error.
- **Condition:** Timing figures are the source's experience and vary — Seller Central layout and terminology change, so verify the current interface.
- **Condition:** Q4 delays are seasonally normal, not necessarily a lost-inventory situation.

#### Add an existing ASIN to your inventory instead of creating a listing
Card: `cee7349150a1e7c21d4aebc3` · Source: Beginners Guide To Amazon FBA In 2025 (1).docx · Section: 0

Match existing listings by ASIN, sell at the lowest FBA price and select Amazon's barcode to avoid commingled stock.

Applies when: Listing a validated wholesale or arbitrage product you are ready to sell on Amazon.

- In Seller Central go to Catalog > Add Product, paste the product's ASIN (found under 'see all information') and search rather than building a brand-new listing.
- If the result says condition new 'apply to sell' you are gated. To get ungated the source's method is to buy 10 units — sometimes 100 — of the exact product from a wholesale supplier and upload an invoice matching your Amazon account or company name.
- Once eligible, set condition as New and click 'Sell this product'; you are joining the existing listing, not creating one.
- Price to match or sit close to the lowest FBA seller on the listing. Filter the other-sellers view by Prime to isolate FBA sellers.
- Set fulfilment channel to Amazon (FBA) and disable any other marketplaces you do not want to sell in, then save and finish.
- At the barcode field choose 'Amazon's barcode only' even if the product already has a manufacturer barcode, so Amazon can attribute commingled shipments to you rather than confusing your stock with another seller's on the same ASIN.
- Allow around 15 minutes for the offer to appear in your inventory.
- **Condition:** Gating thresholds and invoice requirements vary by category and brand; verify with Seller Central.
- **Condition:** Sticking your own Amazon barcode over the manufacturer barcode is the source's commingling safeguard — this alters the physical unit, so confirm it does not conflict with the brand's requirements.

### Retrieval and applicability
Search: `Amazon inventory listing fulfilment account conversion`
Related domains: sourcing, finance-and-accounting, ad-copy-deployment
Mixed-folder candidate IDs: 88cbc55b3268bd48710d9c64, e9c97672d49d54978252e4ce, 9f5bae6b1128098902b51bbc

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
