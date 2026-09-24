# Asked Claude to Find Me a $1K/Day Product (It Worked)

source_id: 1TYodTXR6LLlNuTKucxPY5dDu3hFIw3Mu  |  folder: /01-PRD-product-research  |  cards: 10  |  words: 5358  |  type: video transcript (YouTube)

credibility: Presenter is "Mark" (Instagram: Mark Builds Brands), who runs a paid mentorship called Brand Builds Academy (BBA) and pitches it at the end of the video. His evidence is his own stated process and one on-screen example (a competitor brand found live during recording), not audited financials or a documented track record of his own product launches. Treat his numbers as one practitioner's rules of thumb, not tested benchmarks. He has a commercial incentive to make the method sound easy and fast ("should never take you more than like an hour"), which is a reason to discount claims about ease and speed specifically.

date signals: source_date 2026-06, verified_at 2026-09-19. url: youtube.com/watch?v=1KrsOagtWgM. Names a specific AI model, "Opus 4.8" (says Sonnet "would probably be fine" too) — model names and version numbers go stale fast `[web check: current Claude model names]`. Names a specific third-party tool, Get Hooked (get hooked.ai), and its MCP connector setup flow inside Claude's UI — both the tool's existence/pricing and Claude's connector UI can change `[web check: Get Hooked still exists/pricing]` `[verify UI: Claude custom connector flow]`. The source's own header flags this: "decay_risk: high (Claude MCP integrations and exact ad costs decay rapidly)."

## 1. What this source is for

A five-step workflow for sourcing a physical ecommerce product using Claude plus an ad-spy tool (Get Hooked) connected via MCP: pick a market, narrow to an emotional problem, find a candidate product from live competitor ad data, validate the competitor's scale with a traffic-based revenue estimate, and check the margin math before testing. It also gives a short troubleshooting framework for after a paid test fails, to tell whether the ads or the funnel is the constraint, so a failed test isn't automatically blamed on the product.

## 2. Principles

1. **Market first, product second.** The market and the emotional problem it contains drive sales more than the specific product does. The source's analogy: selling umbrellas in a thunderstorm vs. on a sunny day — same product, very different sales volume. Condition: applies before any product search starts. Evidence: presenter's stated framework/opinion, not measured. [c9b651f1b77d]
2. **Pick a broad emotional problem, not a narrow one.** A single well-chosen problem (e.g. migraines) can be solved by many different products (supplements, a headband, a massage gun, a neck traction device, a clinic visit), which gives more product options and more room to test. Condition: applied when narrowing from market to problem, before selecting a product. Evidence: presenter's reasoning, illustrated with one example (migraines), not data. [c9b651f1b77d]
3. **AI-assisted sourcing is a bounded discipline.** It ends at a validated, margin-checked product; it does not produce ad creative, does not manage bids/CPC/CPM, and does not build or optimize the funnel/checkout. Condition: use when scoping a sourcing sprint or briefing a team, so a creative or checkout problem doesn't get treated as "the product is wrong." Evidence: the source's own module-boundary framing (maps to separate creative, media-buying and storefront work). [33a09eb2fe9d]
4. **The product is rarely the reason a test fails.** Presenter's claim: top six-, seven- and eight-figure brands aren't selling anything especially remarkable — their ads and funnel are dialed in. A failed test should trigger a "why" diagnosis (ads vs. funnel) before the product is abandoned. Condition: after a paid test is unprofitable, and only after the process (market, problem, product, validation, game plan) was actually followed. Evidence: presenter's observation from working with clients, not a cited study. [2b0c86c591158]

## 3. Procedures

### A. Overall 5-step sequence
1. Find a market.
2. Identify an emotional problem within that market.
3. Select a candidate product that solves that problem.
4. Validate the product/competitor with real data.
5. Build a game plan to sell it (troubleshooting readiness), before spending ad money.
Source frames product selection as step 3 of 5, not the end point — validation and a game plan are treated as mandatory, not optional. [c9b651f1b77d]

### B. Choose a market
1. Pick from markets the source says are reliably passionate: pet, weight loss, hair growth, cosmetic/anything with a clear before-and-after (skincare included here), supplements, beauty, health and wellness.
2. Do not overthink this step — pick one and move on. The source frames this as the easiest, most "spoonfed" part of the process.
Caveat inside the source: supplements is called "a great never-ending market" but also "challenging." [c9b651f1b77d]

### C. Generate emotional sub-niches with Claude
1. Open Claude directly (presenter used Opus; says Sonnet "would probably be fine"). No other AI tool needed for this step. `[web check: current Claude model names]`
2. Paste a large, structured prompt asking for a list of emotional sub-niches for a DTC beginner brand in the chosen market. (Exact prompt text is not reproduced in the source — the presenter says to get it via Instagram DM, not in the transcript itself. Do not reconstruct wording the source didn't give; note the gap.)
3. Submit. In the example, Claude returned 30 emotional sub-niches (examples shown: lower back stiffness, neck and shoulder tension, plantar fasciitis).
4. Review the list and pick 5 sub-niches you like most. These 5 become the search scope for the next step. [1918017689b2]

### D. Connect Get Hooked to Claude via MCP `[verify UI]`
1. Create an account at get hooked.ai (presenter used a free trial). `[web check: Get Hooked still exists/pricing]`
2. In Get Hooked, open the account menu (bottom-left corner), select "AI and MCP."
3. Scroll past the API section to the "Connect to AI agent" / MCP section.
4. Copy the MCP server URL and the OAuth Client ID shown there.
5. In Claude, go to the left sidebar, select "Customize," then "Connectors," then the plus icon, then "Add custom connector."
6. Name the connector (e.g. "Get Hooked"), paste the MCP server URL, paste the OAuth Client ID into its field, click Add.
Result: Claude now has access to a large aggregator of Facebook/Meta ads on top of its normal capability. [2e6da11c04cc]
Caveat: exact menu labels and steps are explicitly called high-decay by the source; confirm current UI in both tools before relying on this sequence.

### E. Run the MCP sourcing prompt
1. Write one prompt that bundles: (a) information about the MCP and how to use it, (b) the research process Claude should follow, (c) the 5 sub-niches chosen in step C. (Again, exact prompt text is not given in the transcript.)
2. Submit and wait — the source says this takes "a few minutes."
3. Read the output: for each qualifying brand (enough active ads, fits an input sub-niche), the output includes product, pain point, typical ad pattern, funnel architecture (driving to a PDP vs. an advertorial), and a top-performing ad.
4. Treat funnel architecture as competitive intelligence — it shows where competitors send traffic, not just what they sell.
5. Example output from the video: a Facebook page called "Fall Prevention Tips," 232 active ads across a few subdomains, selling wide-toe-box barefoot shoes on a foot-pain angle. [b09a0ce63306]
Caveat: qualifying on active-ad-volume can reflect ad budget or ongoing testing, not proven profitability — validate separately (step F).
Caveat: presenter's claim that this makes product selection take "never... more than like an hour" is his personal experience, not a benchmark to plan around.

### F. Validate competitor scale with the SimilarWeb revenue formula
1. Install the SimilarWeb browser extension (source notes roughly 3 free searches/day on the free tier).
2. Open the competitor's store page with the extension enabled to read estimated monthly visits.
3. Estimate a conversion rate: baseline 2%, typical range 1.5%–3.5% in the source's own usage; higher-priced products get a lower estimated rate (e.g. ~1.5% for high-ticket) — note the source states this baseline two slightly different ways across the raw transcript and its own card notes (see section 9).
4. Estimate AOV conservatively from the visible offer stack (bundles, upsells) rather than the single-item price.
5. Multiply: monthly visits x conversion rate = estimated monthly orders; orders x AOV = estimated monthly revenue.
6. Apply a floor: only treat a competitor as validating a product if estimated revenue is above roughly $200k–$300k/month (source states both $300k in one place and "$200 to 300k" in another — read as "roughly $200k–$300k+" rather than one exact number).
Worked example from the video: store selling shoes at $70/pair; ~1.5M visits/month used (actual traffic looked closer to ~2M, presenter chose the conservative figure); 2% conversion; AOV estimated at $90 (conservative, off a $70 item plus offer stack) → 1.5M x 0.02 = 30,000 orders/month; 30,000 x $90 = ~$2.7M/month estimated revenue. [b37123cc93c7]
Caveat: these are rough estimates from public traffic tools, not financials — the presenter states outright he cannot calculate an exact number.

### G. Margin check
1. Compute landed cost of goods sold (COGS): product cost plus shipping to you.
2. Check rule 1: retail price must be at least 3x landed COGS.
3. Check rule 2: gross margin per unit (price minus COGS) must be at least $30.
4. Both rules must pass together, not just one. Worked example: $15 landed cost, $50 retail price → $35 gross margin, satisfies 3x (3.33x) and the $30 floor. [cd8817fc79ec]
Caveat: do not assume you can source at the same cost as an established competitor — they've likely negotiated better supplier rates than a new, possibly drop-shipping, brand.

### H. Post-test troubleshooting ("the why")
Use only after steps A–G were actually followed and a paid test underperforms — not as a way to skip validation.
1. Ask whether the failure is ad-related or funnel-related before concluding the product is bad. [2b0c86c591158]
2. Check ad KPIs in this order: CPC → CTR → CPM (see section 4 for numbers). [f5d6e64a0e54]
3. Check funnel KPIs: landing-page-to-ATC ratio, ATC-to-purchase ratio, AOV (and LTV for subscription/retention models). [3b6e3ec9a71b]
4. If a funnel KPI check points to a checkout/payment problem, fix that before touching the product or the ads.
5. Route the actual fix to the right discipline: creative/ad-copy issues to a creative process, bid/CPC/CPM management to paid-media execution, checkout/landing-page layout to storefront work — this sourcing method does not itself fix any of those. [33a09eb2fe9d]

## 4. Rules, thresholds and numbers

| Rule | Number / threshold | Condition | Source's basis | Card id |
|---|---|---|---|---|
| Competitor revenue floor | ~$200k–$300k+/month estimated | Treating a competitor as proof of a viable product | Presenter's stated minimum bar, stated inconsistently as both "$300k" and "$200 to 300k" | b37123cc93c7 |
| Conversion rate assumption | baseline 2%, range 1.5%–3.5% | Used inside the SimilarWeb revenue formula; lower rate for higher-ticket items | Presenter's own estimation habit, not measured | b37123cc93c7 |
| SimilarWeb free-tier limit | ~3 searches/day | Using the free SimilarWeb extension | Presenter's stated experience with the tool `[web check: current SimilarWeb free-tier limit]` | b37123cc93c7 |
| Margin rule 1 | retail price >= 3x landed COGS | Before committing to test a sourced product | Presenter's rule of thumb | cd8817fc79ec |
| Margin rule 2 | gross margin >= $30/unit | Same as above; raised from a prior personal rule of $20 because Meta ad costs kept rising | Presenter's rule of thumb, explicitly says he changed it over time | cd8817fc79ec |
| Ad CPC (US) | target ~$1.50 link CPC; elevated = $2–$4+ | Diagnosing a failed US ad test | Presenter's target number, "check-engine light," not diagnostic on its own | f5d6e64a0e54 |
| Ad CTR | target >=3%, ideally ~4%; below 3% = creative problem | Same | Presenter's target | f5d6e64a0e54 |
| Ad CPM (US) | no fixed KPI; ~>$80 called high | Same; presenter explicitly says this has no strict KPI and is niche/location dependent | Presenter's rough guide, stated as non-authoritative | f5d6e64a0e54 |
| Funnel ATC ratio | >=10% (8–9% acceptable for pricier products) | Diagnosing a failed test's funnel side | Presenter's benchmark | 3b6e3ec9a71b |
| Funnel ATC-to-purchase ratio | >=30% completion | Same | Presenter's benchmark | 3b6e3ec9a71b |
| AOV vs. base price | 20–40% above base selling price (presenter suggests pushing to ~50% for a one-product store) | Same | Presenter's benchmark | 3b6e3ec9a71b |
| LTV (subscription/retention models) | "substantially higher" than AOV, no number given | Same | Presenter's benchmark, undefined threshold | 3b6e3ec9a71b |

## 5. Diagnostics and checks

**Ad-side check (run when a US test is unprofitable):**
1. Check link CPC first. If near $1.50, ads are not the obvious constraint; if $2–$4+, something is wrong (but this alone doesn't say what).
2. Check CTR next. Below 3% = creative is the problem (weak hooks/copy) — this is where the presenter says ~90% of failures land, in his experience, because sellers overrate their own ads.
3. If CTR is healthy (4–5%) but CPC is still high, check CPM. Above roughly $80 (US) is called high, but the source gives no firm line — it explicitly varies by niche and location.
4. Watch the feedback loop: weak creative lowers CTR and raises CPM simultaneously, compounding into a high CPC.
5. Do not over-optimize CTR alone — a high-CTR, low-conversion ad usually means the ad generated curiosity/engagement but didn't sell. [f5d6e64a0e54] [2b0c86c591158]

**Funnel-side check (run when ad metrics look fine but the product still isn't converting):**
1. Landing-page-to-ATC ratio below 10% (or 8–9% for pricier items): offer or page is failing, or traffic is unqualified.
2. ATC-to-purchase below 30%: check payment-processor approval rates and simplify checkout — the source explicitly favors removing steps over adding conversion "bumpers."
3. AOV below a 20–40% markup over base price: usually missing upsells/downsells on the first purchase.
4. For subscription/retention models, check LTV instead of relying on AOV alone. [3b6e3ec9a71b]

**Product-selection qualifying check (before validation):** a candidate found via Get Hooked must be running "enough active ads" (no fixed number given) and fit one of the chosen sub-niches — but active-ad volume is a qualifying filter, not proof of profitability; that requires the SimilarWeb revenue check. [b09a0ce63306] [b37123cc93c7]

## 6. Tools, settings and named features

- **Claude** (chat interface): used to generate emotional sub-niche lists and to run the MCP-connected sourcing prompt. Presenter used a model named "Opus 4.8"; says Sonnet would likely work too. `[web check: current Claude model names]`
- **Get Hooked** (get hooked.ai): a Facebook/Meta ad-library aggregator used as an MCP data source for Claude. Free trial available per the source. `[web check: Get Hooked still exists/pricing]`
- **Claude custom connectors / MCP**: Customize -> Connectors -> "+" -> Add custom connector; requires the Get Hooked MCP server URL and OAuth Client ID. `[verify UI]`
- **SimilarWeb browser extension**: used to read a competitor's estimated monthly visits; free tier gives roughly 3 searches/day per the source. `[web check: current SimilarWeb free-tier limit]`
- Presenter's own promo mechanic (not part of the workflow itself): DM "Carl" to his Instagram (Mark Builds Brands) to get his prompts, and an application funnel into his mentorship, Brand Builds Academy (BBA). Not a sourcing step — noted for completeness and because the source's own metadata says to skip capturing this kind of promotional content as workflow content.

## 7. Examples and case results

- **Fall Prevention Tips (example find):** Facebook page with 232 active ads across a few subdomains, selling wide-toe-box barefoot shoes marketed on eliminating foot pain. Presented as a live example of step E's output, not a verified success story. [b09a0ce63306]
- **Revenue estimate walkthrough (example calculation):** shoes sold at $70/pair; ~1.5M monthly visits used conservatively (actual traffic estimated closer to ~2M); 2% conversion; AOV estimated at $90 → 30,000 orders/month x $90 = ~$2.7M/month estimated revenue. Presenter notes this is unusually high — "not every single store... is going to be a number this high" — and that the real bar is ~$200k–$300k/month. [b37123cc93c7]
- **Margin example:** source a product for $15 landed, sell for $50 → $35 gross margin, which clears both the 3x-COGS rule and the $30-margin floor at once. [cd8817fc79ec]
- **Personal history note:** presenter says he used to require only $20 of margin and raised it to $30 because Meta ad costs kept increasing — presented as his own rule change over time, not a study. [cd8817fc79ec]

## 8. Mistakes the source warns about

- Jumping into Claude with "find me a $1k/day product" without doing market and problem research first.
- Overthinking market selection instead of just picking one from the list and moving on.
- Treating high active-ad-count or a single big competitor find as proof of profitability without running the SimilarWeb revenue check.
- Assuming you can match an established competitor's cost base — they've had time to negotiate better supplier rates than a new (often drop-shipping) brand.
- Testing a product with no game plan, hitting one unprofitable day, and quitting while blaming "the method" or calling it a scam.
- Assuming a failed test means the product is bad, when the source says it's rarely the product and usually ads or funnel.
- Over-optimizing CTR for vanity (high-curiosity, low-sell creative) instead of balancing engagement with actually selling.
- Not checking the payment processor's approval rates, or over-complicating checkout, when ATC-to-purchase is low — the source says simplification beats adding more conversion elements.
- Treating margin rules 1 and 2 as independent instead of checking both together (see section 9 for where they can conflict). [2b0c86c591158] [f5d6e64a0e54] [3b6e3ec9a71b] [cd8817fc79ec]

## 9. Caveats, conflicts and what is missing

- **Commercial bias:** the presenter monetizes a mentorship program (BBA) pitched at the end of the video and frames the described method as easy and fast ("should never take you more than like an hour"). Weigh ease/speed claims accordingly; the mechanical steps (formulas, thresholds) are separable from that framing.
- **Internal inconsistency on the revenue floor:** the structured metadata block states the benchmark as ">$300k/mo" in one place and "$200 to 300k" in another ("Look for" section vs. "Scope definition" section) inside the same source. Treat the floor as "roughly $200k–$300k+" rather than a single precise number.
- **Internal inconsistency on conversion-rate assumption:** stated as "2% as a baseline conservative average" in one part of the structured notes and as "2 to 3% on average" / "1.5 to 3.5%" in the raw transcript. Use 2% as the stated baseline and 1.5%–3.5% as the working range, per the card's own reconciliation. [b37123cc93c7]
- **Margin rules can conflict at low price points:** the card for the margin rules itself flags that 3x COGS and a $30 floor don't always agree — e.g. a $12-cost product at 3x gives $36 (passes both), but a $10-cost product at exactly 3x gives only $20 margin (fails the $30 floor). At low COGS, the $30 floor is the binding constraint, not the 3x multiplier. [cd8817fc79ec]
- **Margins don't cover everything:** the 3x-COGS/$30-margin rules are framed by the source as sized to "absorb Meta ad costs" specifically — they say nothing about shipping cost, payment processing fees, or refunds, which also eat gross margin. `[needs brand data: landed cost, payment processing rate, refund rate, shipping cost per order]`
- **No fixed CPM threshold given** — the presenter explicitly says he has no KPI for CPM and calls $80 a rough, relative guide, not a rule. Do not treat it with the same confidence as the CPC/CTR numbers.
- **Exact prompts not reproduced:** the source transcript references "pasting in this massive prompt" twice (sub-niche generation, and the MCP sourcing prompt) but the wording isn't given in the video content itself — only available via the presenter's separate Instagram DM funnel, which is a promotional mechanism, not part of the citable source text. Any prompt used to run this workflow will need to be built from the stated inputs/outputs in section 3, not copied from this source.
- **No stated sample size or track record:** the video shows one example brand and one example revenue calculation; there's no claim of how many products the presenter has sourced this way or their success rate.
- **90% figure is anecdotal:** "roughly 90% of the issues I see are ads-related" is explicitly presented as personal observation, not a measured statistic across a client base.
- **High decay risk flagged by the source itself** for the Claude model name, the Get Hooked MCP integration steps, and "exact ad costs" (CPC/CPM targets) — all should be re-verified before relying on them operationally. `[web check]` `[verify UI]`

## 10. Card index

- c9b651f1b77d — Market-First Product Research Hierarchy
- 1918017689b2 — Use Claude to Generate Winning Emotional Sub-Niches
- 2e6da11c04cc — Connect Get Hooked to Claude via MCP for Ad-Library Sourcing
- b09a0ce63306 — Run the MCP Product-Sourcing Prompt Over Your Five Sub-Niches
- b37123cc93c7 — Estimate Competitor Revenue with the SimilarWeb Formula
- cd8817fc79ec — The Two Golden Margin Rules: 3x COGS and $30 Gross Margin
- 2b0c86c59115 — Diagnose a Failed Product Test: Ads Problem or Funnel Problem
- f5d6e64a0e54 — Ad Failure KPIs: CPC, CTR and CPM Thresholds
- 3b6e3ec9a71b — Funnel Failure KPIs: ATC Ratio, Checkout Completion and AOV
- 33a09eb2fe9d — Keep AI Sourcing and Ad Execution in Separate Ownership
