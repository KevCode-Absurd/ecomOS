# Sourcing — draft playbook

**Status:** source-linked draft; not owner-approved or outcome-tested.

Read [the operating contract](../OPERATING_CONTRACT.md) before using a workflow.

## Inputs
- Specifications/BOM
- supplier quotes
- lead times
- quality evidence
- inventory and cash

## Measures
- Landed cost
- defects
- stockouts
- cash tied in inventory

## Foundation candidates
Inferred principle labels do not establish universal applicability. Retain source conditions; empty means no matched labelled principle, not absence of foundational knowledge.

- **Structure Bulk Purchases Around Cash Flow, Not Just Unit Price** (`b2b02a1e47e6cd8453c5ab28`): Unused volume and freight discounts can be leveraged through payment or inventory structures rather than taken as straight price cuts.
  Applies when: Replenishment and cash-flow planning: you are ordering a recurring SKU several times a year and weighing a larger order tier against working capital.
  Condition: This is one commenter's model, not a proven universal method.
  Condition: Splitting inventory ownership introduces legal and accounting complexity that the source does not address.

- **Enter Supplier Negotiations From a Position of Redundancy** (`89a60c40d39ffec4165fabcd`): Before asking a supplier to cut cost, do your homework so you already know the benchmark cost and have alternate suppliers mapped — leverage comes from preparation.
  Applies when: Preparing for a cost-down negotiation with a factory or new supplier, or onboarding a supplier for a new product line.
  Condition: The source's rule: if the factory won't budge, find another factory — but this only works if you actually built the redundancy first. If you entered the relationship giving the factory too much power, leverage is hard to recover.

- **Compare supplier credit with other working-capital options** (`63dcc0f46e05d9490aa88dfb`): The goal across BOM, price breaks and terms is a supplier relationship where they finance your inventory and dividends.
  Applies when: Designing your overall sourcing/finance strategy and deciding what to prioritize as you scale purchasing.
  Condition: This is Roman Khan's stated approach; results are his own and reflect a specific business mix and scale, not a guarantee. Long terms and consignment still require a supplier willing to extend them.

## Compare suppliers for an ecommerce product
Workflow ID: `sourcing.supplier-shortlist`

**Deliverable:** Supplier comparison and sample plan

### Proposed decision sequence
1. Define specifications and required quality evidence
2. Compare quotes on landed cost, lead time, terms and risk
3. Plan samples and acceptance checks before committing volume

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Enter Supplier Negotiations From a Position of Redundancy
Card: `89a60c40d39ffec4165fabcd` · Source: He Went From $3M In Debt To $13M In Cash Using This Playbook.docx · Section: 1

Before asking a supplier to cut cost, do your homework so you already know the benchmark cost and have alternate suppliers mapped — leverage comes from preparation.

Applies when: Preparing for a cost-down negotiation with a factory or new supplier, or onboarding a supplier for a new product line.

- Before negotiating, buy and reverse-engineer competitor samples and map alternative suppliers for every key component.
- Talk to heads of procurement at larger incumbent brands in your category to learn the industry-standard factory margin band (e.g. the source cites jewelry factories at ~5–9% EBITDA).
- Come in with the BOM already drafted from other suppliers so the conversation starts from knowledge, not hope.
- Ask each supplier to build their own BOM to your template rather than sending your current supplier's BOM — you want their independently sourced component costs.
- Always maintain at least one viable alternate factory so you can act if the incumbent won't move.
- **Condition:** The source's rule: if the factory won't budge, find another factory — but this only works if you actually built the redundancy first. If you entered the relationship giving the factory too much power, leverage is hard to recover.

#### Run the Sample Progression: Strike-Off to Pre-Production to Production
Card: `8254bc7180c2c3902fcea3f4` · Source: The Ultimate Guide To Product Sourcing In 2026.docx · Section: 0

Advance through three sample stages and hold a factory sample as the gold standard reference so bulk orders can be checked against it.

Applies when: You are selecting between final candidate factories or preparing to green-light bulk production.

- Order samples from every potential supplier you are considering — this tests communication and reliability as much as quality. Watch who follows instructions, sends updates unprompted, and matches your tech pack precisely.
- Start with a strike-off or small test sample to approve materials and prints.
- Move to a pre-production sample that should match your tech pack perfectly. Treat this as the gold standard you will compare bulk against.
- For apparel, confirm grading here: get multiple pre-production samples to verify sizes scale correctly (S, M, L proportions).
- Keep one approved sample in-house and one at the factory for reference.
- After choosing the final supplier, order a production sample built right before mass production. If it does not match the pre-production standard, do not proceed.
- Protect your IP as you scale: keep original tech packs, artwork and source files on your side, sign a manufacturing agreement at volume, and register trademarks.
- **Condition:** The source presents the production sample mismatch as a hard stop; it does not discuss scenarios where minor deviation might be acceptable.
- **Condition:** Grading guidance is specific to apparel sizing.

#### Approve a new factory sample before committing to a store launch
Card: `101cb1f841d99d0a183bfd2a` · Source: How He Makes Millions Sourcing Products From China.docx · Section: 0

Never pitch factory-sourced product to a buyer without first obtaining and inspecting a physical sample from that factory.

Applies when: Selecting a new supplier or product variation before placing a bulk purchase order for an ecommerce store.

- Collect samples from each candidate factory for any new product or new supplier.
- Inspect the sample for the quality attributes your client or store depends on before making any pricing or listing commitments.
- Use approved sample quality and a complete cost quote to decide whether to commit to production and customer-facing promises.
- Keep the sample as the reference for the bulk run, so your quality check has a fixed benchmark.
- Combine sampling with your external vetting: the source builds client trust on saving time and reducing risk, not just lowering cost.
- **Condition:** A good sample does not guarantee a good bulk run — production quality can drift, so build in pre-shipment checks.
- **Condition:** Sampling adds cost and lead time, which matters most for fast-moving ecommerce launches.

### Retrieval and applicability
Search: `supplier BOM specification quality sample redundancy`
Related domains: finance-and-accounting, product-research, team-and-management
Mixed-folder candidate IDs: de43bdcfd16a9df9d3110573, 38c80ae68029672e69cd13ce, d147d0be41fbb21e1e42ba77

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

## Prepare a supplier negotiation
Workflow ID: `sourcing.cost-negotiation`

**Deliverable:** Negotiation brief

### Proposed decision sequence
1. Break landed cost into components and identify negotiable items
2. Compare alternatives and volume commitments against cash exposure
3. Prepare requests and acceptable trade-offs

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Ask for Volume Price Breaks on Every BOM Line
Card: `2cb8e11885e1afc5f86d9ef9` · Source: He Went From $3M In Debt To $13M In Cash Using This Playbook.docx · Section: 1

Negotiate component-level price breaks tied to unit volumes, understanding that factory economics rest on machine and labor utilization.

Applies when: Setting up volume tiers with a factory, planning a purchase order schedule, or forecasting COGS at higher volumes.

- For each BOM line (cotton, labor, zippers, polishing/QC, etc.), ask: at what volume does this price drop?
- Frame it around the supplier's utilization — how much of their dedicated line is used, where is idle machine or fixed-labor capacity you can fill?
- Reconcile invoices with the supplier line-by-line (the source has production leads sit with suppliers to do this), so credits for hitting thresholds are actually applied.
- Track price breaks on sub-components too, since suppliers pass through their own sub-vendor economies of scale (e.g. a big zipper maker gives the factory a discount that should flow to you).
- Consider internalizing procurement of key components (buying gold/diamonds/chips directly and supplying your assembler) to capture the sub-vendor margin, but only once you can manage the inventory price risk.
- **Condition:** The source frames these as credits applied after you hit overage volumes, not blanket discounts — build the mechanism into the agreement. Internalizing components also exposes you to commodity price swings.

#### Negotiate Down Per-Unit Cost Before You Commit Volume
Card: `c7f05c514633358e224d0650` · Source: What I learnt from sourcing e-commerce products from China.docx · Section: 0

Ask suppliers for a lower unit price rather than accepting the initial quote; small per-unit reductions compound across a large order.

Applies when: Supplier negotiation: you have a quote in hand for a replenishment or new-product bulk order and are deciding whether to push back on price.

- Treat the first quote as an opening position, not a final price. The source got a per-product cost from $6 down to $4.80 through direct negotiation.
- Quantify the saving before you decide how hard to push: the author notes that $1.20 reduction saved roughly $3,500 per order at his volume, which is why the effort was worth it.
- Negotiate alongside volume, payment and shipping terms rather than price alone — suppliers may offer freight consolidation or other concessions instead of a price cut if cash flow constrains your order size.
- A commenter with sourcing expertise suggests unused discounts (volume, consolidated freight) can be repurposed creatively — for example, funding a larger order to unlock a lower tier and structuring payments around it — so ask what other levers exist beyond the sticker price.
- Do not present a source's negotiated outcome as your expected result; your leverage depends on volume, category and supplier.
- **Condition:** The $6→$4.80 and $3,500 figures are from the author's own order and are examples, not benchmarks.
- **Condition:** Aggressive negotiation can damage a relationship, so weigh it against long-term supply reliability.

#### Request a Structured Quote Before Sampling
Card: `e929a7dceb465eaed4e4e8b3` · Source: The Ultimate Guide To Product Sourcing In 2026.docx · Section: 0

A complete quote request forces suppliers to commit on unit cost, MOQ, lead time, packaging and payment terms so factories are comparable side by side.

Applies when: You have a shortlist of vetted factories and need comparable commercial terms to choose between them or use as negotiation leverage.

- Send your tech pack to each shortlisted factory with a request for a quote covering all of the following, not just unit price.
- Ask for unit cost broken out per SKU or variation.
- Ask for minimum order quantity per SKU.
- Ask for lead time to manufacture, in days.
- Ask for packaging details and specifications.
- Ask for payment terms.
- Compare qualified suppliers using the same specifications, quantities and delivery terms; real alternatives can support negotiation, but are not the only reason a factory improves terms.
- **Condition:** The source does not specify a standard payment-term structure, so negotiate based on what protects your cash flow.
- **Condition:** Getting a competing quote is described as leverage, but the source also warns against hostile squeezing of suppliers.

### Retrieval and applicability
Search: `BOM cost negotiation volume price payment terms`
Related domains: finance-and-accounting, product-research, team-and-management
Mixed-folder candidate IDs: a3a00f7b96c8576e44fafa39, 765be2933ced903dd9234f7d, 561de6374d65f734aa8ce0d1

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

## Plan replenishment under uncertainty
Workflow ID: `sourcing.inventory-plan`

**Deliverable:** Replenishment recommendation with scenarios

### Proposed decision sequence
1. Reconcile stock, open orders and demand assumptions
2. Model lead-time and demand scenarios with cash constraints
3. Propose purchase quantities and review triggers

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Calculate Reorder Point with Velocity, Lead Time and Safety Stock
Card: `8bf409e6c3d5d2bfff0a8ecd` · Source: The Ultimate Guide To Product Sourcing In 2026.docx · Section: 0

Reorder Point = (Daily Sales Velocity x Total Lead Time) + Safety Stock, so you reorder before running dry rather than chasing demand.

Applies when: You are setting reorder triggers and planning replenishment shipments for any SKU.

- Measure daily sales velocity: how fast the product actually sells, measured over time. Use Shopify order history to spot velocity, slow movers and seasonal spikes, and review weekly.
- Measure replenishment lead time from releasing a reorder until usable stock is received, including production, freight, customs and receiving; payment date alone may not start the operational clock.
- Set a safety stock buffer to cover sales spikes or freight delays so you keep selling.
- Compute: Reorder Point = (Daily Sales Velocity x Total Lead Time in days) + Safety Stock.
- Example: 50 units/day x 60 days + 500 safety units = 3,500 units. Compare against inventory position: usable on-hand plus confirmed inbound minus committed or backordered demand, avoiding double-counting allocations.
- Feed weekly performance and stock-level reviews into the reorder plan, and communicate them to suppliers before problems appear.
- **Condition:** The example numbers are illustrative inputs, not benchmarks; your velocity, lead time and safety stock must come from your own data.
- **Condition:** The source attributes a major stockout and lost sales to having no forecasting system in place — treat the formula as a discipline, not a one-time calculation.

#### Structure Bulk Purchases Around Cash Flow, Not Just Unit Price
Card: `b2b02a1e47e6cd8453c5ab28` · Source: What I learnt from sourcing e-commerce products from China.docx · Section: 0

Unused volume and freight discounts can be leveraged through payment or inventory structures rather than taken as straight price cuts.

Applies when: Replenishment and cash-flow planning: you are ordering a recurring SKU several times a year and weighing a larger order tier against working capital.

- The source describes a 30% deposit and 70% pre-shipment balance as one structure; confirm actual milestones and contractual terms for your order.
- Note the commenter's scenario: a client re-ordering the same product multiple times a year at roughly $10 landed cost. An outside party adds capital to increase the order to a full year's supply, unlocking a volume discount while keeping the client's per-unit cost unchanged at $10.
- The client receives the full year of stock, and only pays the outside party as they consume inventory — removing lead time and MOQ on the portion already warehoused, and improving cash flow.
- For an ecommerce operator, this suggests a decision: if a volume tier would strain cash flow, look for investors or distributors willing to fund the gap and be repaid as you sell through, rather than declining the discount entirely.
- This is a commenter's specific client arrangement, not a standard market practice; structure any such deal with clear inventory ownership and repayment terms.
- **Condition:** This is one commenter's model, not a proven universal method.
- **Condition:** Splitting inventory ownership introduces legal and accounting complexity that the source does not address.

#### Use Payment Terms to Widen Your Float, Not to Chase Sales
Card: `520876950b5089b2fb3244db` · Source: He Went From $3M In Debt To $13M In Cash Using This Playbook.docx · Section: 1

Your real float is payment terms minus production lead time, so extending net terms buys you error tolerance and free cash flow.

Applies when: Deciding what payment terms to request from suppliers and how much working capital to hold before scaling ad spend or order volume.

- Map the actual deposit, invoice, shipping, receipt, sale and processor-payout dates. If net 90 begins when production starts and stock arrives in 30 days, 60 days remain before payment; a different contractual start changes this calculation.
- Push for longer net terms as you mature — the source went from net 7 to net 90, citing net 180 as an extreme others use.
- Recognize the most valuable outcome is margin of error: marketing is a daily variable cost you can switch off, a purchase order is not.
- Factor in inventory mistakes (e.g. wrong size mix on rings) that eat your float in the real world.
- Target consignment if you can get it: the factory owns goods until you sell, converting a made-to-order business to near-dropship cash dynamics.
- **Condition:** Consignment is easiest with categories where the supplier can reclaim/resell inventory (the source notes gold's melt value and Hong Kong fulfillment made it feasible for one business); it isn't universally available.
- **Condition:** Time from warehouse arrival to sale and payout consumes the remaining headroom; payment terms alone do not establish cash conversion.

### Retrieval and applicability
Search: `inventory lead time stockout purchase order demand`
Related domains: finance-and-accounting, product-research, team-and-management
Mixed-folder candidate IDs: c8c9e0285d1c94bb1ceec0f0, 88dae8d1f315c0489467aafa, 384fcc700d977347a4dc58f6

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
