# Product Research — draft playbook

**Status:** source-linked draft; not owner-approved or outcome-tested.

Read [the operating contract](../OPERATING_CONTRACT.md) before using a workflow.

## Inputs
- Market
- product candidates
- customer evidence
- target price
- landed costs
- constraints

## Measures
- Contribution per order
- validation purchases
- return reasons

## Foundation candidates
Inferred principle labels do not establish universal applicability. Retain source conditions; empty means no matched labelled principle, not absence of foundational knowledge.

- **Product Criteria: Daily Problem Plus Retail Absence** (`cccca902b3896ea85b116184`): Two baseline criteria — a problem that recurs daily and no big-box retail availability — for screening product ideas.
  Applies when: Screening candidate products before spending on creative, site build or inventory, especially in health and wellness.
  Condition: Applies to physical problem-solution goods aimed at older buyers; not a universal test for all ecommerce categories.
  Condition: Retail absence is a margin/protection heuristic, not proof of demand — validate separately with ad intelligence.
  Condition: The source presents these as his screen, not an empirically benchmarked rule.

- **Competitor profit as the primary product-viability filter** (`f966191090dae0ac21ec0fa3`): Treat active, profitable competitors as proof of concept rather than a disqualifying sign of saturation.
  Applies when: Choosing whether to pursue a product or brushing off one because 'everyone is selling it'.
  Condition: This is the presenter's opinion and it runs against the common 'pick an unsaturated niche' advice; treat both as situational.
  Condition: Saturation can still make paid acquisition more expensive; the angle trick is not a guarantee, only a way to differentiate.

- **Keep AI Sourcing and Ad Execution in Separate Ownership** (`33a09eb2fe9d840b800f4141`): AI-assisted sourcing ends at a validated, margin-checked product; creative, media buying and storefront work are separate disciplines that determine whether the product actually succeeds.
  Applies when: Scoping a product-research sprint, or setting expectations that finding the product is only one part of a profitable launch.
  Condition: The source maps these boundaries as a module taxonomy; it does not argue paid media or creative are unimportant — the reverse.

## Validate an ecommerce product opportunity
Workflow ID: `product-research.validate-product`

**Deliverable:** Candidate comparison and validation brief

### Proposed decision sequence
1. Separate customer-problem evidence from popularity proxies
2. Check unit economics and fulfilment constraints before prioritising candidates
3. Define a bounded validation with explicit reject and proceed criteria

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Score opportunities on wholesale-to-retail margin before designing
Card: `a20e53fb1d991a39e79282c3` · Source: Making $$ with Alibaba's NEW AI Agent (Full Demo).docx · Section: 0

The sourcing tool reports wholesale cost, target retail price and gross margin percentage so you can compare product ideas on economics, not just demand.

Applies when: Choosing between several validated product ideas, or sanity-checking that a category can support the ad and fulfilment costs of ecommerce.

- For each candidate product, record wholesale cost, target retail price, MOQ range and the reported gross margin percentage.
- Compare across products on margin as well as demand. The source's example showed hoodies at roughly 200-300% margin while phone cases were cited at 300-400%, with a $6.71 wholesale hoodie as a concrete figure.
- Where margins depend on licensing, treat the licence cost as a separate line before deciding; the source flags licensing as a requirement for the branded example.
- Treat margin percentage as covering product cost only. It does not include freight, platform fees, returns or paid acquisition, so model those separately before committing.
- **Condition:** Margin and wholesale figures from the tool are estimates and vary by supplier and order size; confirm with actual quotes.
- **Condition:** A high margin category may still be unviable once acquisition cost and returns are included.

#### Product Criteria: Daily Problem Plus Retail Absence
Card: `cccca902b3896ea85b116184` · Source: Transcript of the product research method that made me $670k.docx · Section: 0

Two baseline criteria — a problem that recurs daily and no big-box retail availability — for screening product ideas.

Applies when: Screening candidate products before spending on creative, site build or inventory, especially in health and wellness.

- Check that the product solves a real problem, either a deep emotional problem/desire or a physical problem the buyer feels every single day.
- Use the source's example: foot pain — felt every time the person walks — so they will buy almost anything if the copy is good.
- Confirm the product is not available in big-box retail stores; retail absence protects margin and ad-driven demand.
- Prefer problems with high daily frequency and strong aversion (chronic pain, child sleep disruption, incontinence) because urgency shortens the buying decision.
- Assess 'deeply annoying daily problem' as a better signal than 'cool product' — the source explicitly rates a boring problem like tinnitus higher than a gimmicky pillow because of the ongoing irritation.
- **Condition:** Applies to physical problem-solution goods aimed at older buyers; not a universal test for all ecommerce categories.
- **Condition:** Retail absence is a margin/protection heuristic, not proof of demand — validate separately with ad intelligence.
- **Condition:** The source presents these as his screen, not an empirically benchmarked rule.

#### The validation checklist applied to every product before selling
Card: `178c6277a818e77ecad08171` · Source: The Only Product Research Video You Need to Start Dropshipping.docx · Section: 0

A repeatable gate: proof of competitors making money, demand signals, sourcing price and fulfillment readiness.

Applies when: Right before committing money or building a store around a product.

- Confirm competitors exist and are making money with the product — the core criterion from the start of the workflow.
- Confirm the product either solves a problem or serves a passionate community.
- Confirm demand through repeated viral evidence, multiple competitors, or high active ad volume in the Facebook Ad Library.
- Confirm sourcing: reverse-image search the product to find supplier cost and a margin floor, and check shipping speed.
- Confirm the marketing angle you would use is not already fully occupied — look for a specific sub-demographic or creative angle competitors have not tapped.
- Only then move to store build, creative production and testing; the presenter says once you see what works for competitors there is no need to reinvent the wheel, just adapt it.
- **Condition:** This is a screening framework from a practitioner, not a statistical model; each signal can be wrong in isolation.
- **Condition:** Fulfillment tooling (e.g. sourcing/3PL apps) is out of scope for this workflow and should be verified separately as interfaces change.

### Retrieval and applicability
Search: `product research demand selection validation margin`
Related domains: avatars, offers, sourcing, finance-and-accounting
Mixed-folder candidate IDs: da1c4ad0b07f73d74e11b23c, cc5525cdafc8c55c5b697173, cb1e0f63e55e5b76dea610b0

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

## Research competing product offers
Workflow ID: `product-research.research-competition`

**Deliverable:** Competitor comparison and positioning hypotheses

### Proposed decision sequence
1. Compare products serving the same customer circumstance
2. Record verifiable features, prices and proof without assuming competitor profitability
3. Identify a substantiated differentiation hypothesis and evidence needed

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Competitor profit as the primary product-viability filter
Card: `f966191090dae0ac21ec0fa3` · Source: The Only Product Research Video You Need to Start Dropshipping.docx · Section: 0

Treat active, profitable competitors as proof of concept rather than a disqualifying sign of saturation.

Applies when: Choosing whether to pursue a product or brushing off one because 'everyone is selling it'.

- Before anything else, require evidence that at least one other seller is moving this product and making money. The presenter argues this matters more than abstract criteria like 'solves a problem' or 'is in demand'.
- Reframe saturation: there are too many people online to reach everyone with one product, so big competitors do not mean no room; the presenter points to continual new entrants in heavily-marketed categories like teeth-whitening pens.
- When a niche looks saturated, look for an untapped angle rather than abandoning the niche — e.g. a clothing brand targeting only girlfriends of boyfriends 5'8" and under, which hooks attention and speaks to a very narrow demographic.
- Confirm the product is either problem-solving or serves a passionate community, then validate there are multiple competitors doing well before committing.
- **Condition:** This is the presenter's opinion and it runs against the common 'pick an unsaturated niche' advice; treat both as situational.
- **Condition:** Saturation can still make paid acquisition more expensive; the angle trick is not a guarantee, only a way to differentiate.

#### Competition assessment via Facebook Ad Library and Page Transparency
Card: `4be18218219d4e40995262b4` · Source: This Product Research Method Made Me $2.3M Dropshipping (LIVE HUNTING).docx · Section: 1

Assess how many direct competitors are running the product, how long they've been running, and whether their stores and offers look beatable.

Applies when: Validating saturation and competitive positioning right before you decide to buy or build the store.

- Search the product term in Facebook Ad Library. Assess the whole niche first (e.g. all GLP products: gummies, liquids, pills, powders), then narrow to your exact variation (e.g. GLP patches).
- Open the page for each competitor, go to About → Page Transparency, confirm whether the page is currently running ads, then open their ad library to see every active ad.
- Note how long they have been running. A competitor running ads for only nine hours has no spend history, so their ads validate nothing yet — the source says to bookmark them and watch rather than infer a winner.
- Check whether they run video or image ads and what language they target. A competitor running Spanish-only image ads, for example, is not a direct competitor in the US English market.
- Evaluate their store and offer. The source rejects a competitor's store as 'completely trash' — minimal template, wrong product imagery — and notes a stronger brand presentation plus subscription option as a differentiator he could use.
- Expect more competitors to appear over time; finding three already means the product is moving. Speed matters — a competitor found the same product 24 hours earlier, which the source treats as a meaningful head start.
- **Condition:** Ad Library shows ads, not spend, so you cannot tell if a competitor's campaign is profitable.
- **Condition:** Page Transparency and Ad Library interfaces change; verify current navigation in the tool.
- **Condition:** New competitors with hours of runtime provide no validation either way.

#### Verify blue oceans by auditing what competitors are not doing
Card: `c840da78d85770f3573102a8` · Source: Full Product Research Course for Dropshipping (Find Winning Products FAST).docx · Section: 0

A two-step routine: find a problem-solving product, then audit competitor ads to locate the audience or angle none of them occupy.

Applies when: Systematically generating differentiated angles for any saturated product you are considering.

- Step one: confirm the product solves a real problem and clears the baseline margin, content and shipping criteria.
- Step two: research the product's competitors — collect their ads, landing pages and targeting signals, then write down explicitly what they are not doing: which customer type, life circumstance or outcome they never mention.
- Look for angles that are visibly rare in the ad set rather than completely absent, since a small amount of validation reduces the risk of an angle nobody wants.
- Position your whole campaign on the gap — avatar, hook, imagery, proof — rather than adding it as a secondary message.
- Repeat the audit whenever entering a new category; the source frames this as thinking rather than automating, and argues most dropshippers do not do it.
- **Condition:** 'Do something nobody's doing' is the source's maxim and a direction of travel, not evidence that any untaken angle will convert.
- **Condition:** Competitor ad libraries only show what is currently running, so recently paused tests can be invisible.

### Retrieval and applicability
Search: `competitor research differentiation market product`
Related domains: avatars, offers, sourcing, finance-and-accounting
Mixed-folder candidate IDs: 66cddfb2c547b0890c143e59, 255fc78a445c27602f657909, 383edf04900eb58ad32f4e3b

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

## Prioritise a product expansion
Workflow ID: `product-research.prioritise-expansion`

**Deliverable:** Ranked expansion backlog and validation plan

### Proposed decision sequence
1. Group requests by customer problem and repeat frequency
2. Assess complementarity, margin and inventory exposure
3. Choose a small validation before committing stock

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Inverse international expansion sequence to dodge US ad auction saturation
Card: `baffe12832b0f6c59b71b3c9` · Source: How to Build an Billion Dollar E-Commerce Empire.docx · Section: 0

Enter secondary English-speaking markets in the order Australia, UK, Europe, Canada, then US to build dominant share before competitors saturate Meta auctions.

Applies when: Planning geographic expansion for an established ecommerce brand that has product-market fit in one market and is deciding which country to enter next.

- Sequence entry as Australia, then UK, then Europe, then Canada, and only then the US. The point of going in reverse order of market size is to accumulate revenue, data and brand proof in less contested channels before the largest, most expensive auction.
- Treat the US last because its Meta ad auctions are the most competitive and expensive; a brand entering cold faces established incumbents bidding up the same audiences.
- Use the earlier markets as proving grounds: each launch should produce conversion data, creative learnings and social proof that makes the eventual US entry stronger.
- Confirm the strategy is viable for your situation before committing: this sequence assumes sufficient capital to run several launches and a product that travels across English-speaking markets with minimal localisation.
- Validate demand independently in each new market rather than assuming spillover from the previous one; auction dynamics, competitors and buyer behaviour differ by country.
- **Condition:** This is one operator's stated sequence from a podcast interview, not a universal rule; the source qualifies it as conditional on brand state and available capital.
- **Condition:** Deferring the US can mean leaving the largest revenue pool to competitors who arrive first; the trade-off is market share versus total addressable revenue.
- **Condition:** The source's broader context was a founder interview including dropshipping anecdotes and mental-health discussion; only the geographic expansion model is transferable.
- **Condition:** Do not score markets on ad demand alone via ad-library scrapers; that approach has different economics and failure modes from a brand expansion.

#### Map seasonality to protect cash flow
Card: `52858475e05d069ee8ce4496` · Source: Transcript of How To Find And Validate WINNING PRODUCTS_ The 16 Step Product Research Guide.docx · Section: 0

Identifying seasonal demand swings with Google Trends lets you plan inventory buys and marketing calendar around cash flow.

Applies when: You are validating a product whose demand may cluster in specific months, or planning inventory and ad budgets.

- Plot the core keywords in Google Trends across multiple years, looking for recurring monthly spikes.
- Label the pattern: extreme seasonality (the source uses Christmas trees, almost all bought in November and December), mild seasonality, or year-round demand.
- If seasonality exists, plan cash flow around it: inventory must be paid for before the spike, and off-season months still carry storage and overhead.
- Use the seasonal pattern in marketing too. In the source example subtle January search spikes were interpreted as cold-weather hair rescue demand and noted for winter marketing.
- Do not confuse mild seasonal variation with a fad; check whether the spikes repeat each year before treating them as predictable.
- **Condition:** A mildly seasonal product can still be a strong business; the source keeps the data for campaign timing rather than rejecting the product.
- **Condition:** Strong seasonality concentrates both revenue and risk, and complicates launching a new brand from zero.

#### Geo-arbitrage: move proven US/UK products into untapped markets
Card: `533302cea5159a2297eb0eb7` · Source: Full Product Research Course for Dropshipping (Find Winning Products FAST).docx · Section: 0

Take a product already validated by US or UK advertising volume and run it in a market where it has not yet been shown.

Applies when: You have a proven product with strong English-language ad evidence and want lower competition than the source market.

- Identify products with heavy existing US/UK ad volume as proof of demand, not as a place to compete.
- Choose a market where the same product has not been advertised (the source cites untapped European countries as his example).
- Assume consumer preferences transfer reasonably across similar markets — the source argues people 'like the same products' but simply have not been shown them.
- Localise creative and copy to the target market's language and context before launching.
- Verify local shipping costs, delivery times and import duties, since these can erase the margin advantage of lower competition.
- **Condition:** The source's confidence in cross-market preference transfer is an opinion; the 'pretty much 100% success rate' phrasing is a claim, not a benchmark.
- **Condition:** Logistics, VAT/import rules and payment availability vary by country and must be checked before committing.

### Retrieval and applicability
Search: `product expansion survey demand customer inventory`
Related domains: avatars, offers, sourcing, finance-and-accounting
Mixed-folder candidate IDs: 414f3d559f4e716ff8ec26ab, b3ef8af35c4c8dc666239594, c38bcfd6b16e39728f3a1e81

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
