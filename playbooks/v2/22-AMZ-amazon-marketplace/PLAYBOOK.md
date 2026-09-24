# 22-AMZ Amazon marketplace playbook

version: 2.0-draft  |  2026-09-24  |  sources: 4 (source 01 is split into 3 part files, so 6 mini playbook files)  |  cards: 284 (256 + 10 + 10 + 8)  |  built from: sources/*.md

## 0. How to use this playbook

**Who runs it.** The Amazon marketplace agent for a brand that owns its product (private label or original product). It covers whether to add Amazon as a channel, account setup, Brand Registry, product research screens, the fee stack and margin model, Amazon-specific sourcing steps, listing build, FBA inbound shipments, launch, PPC, reviews and policy, inventory, and failure patterns.

**What it is not for.** Retail arbitrage, online arbitrage and wholesale reselling of other brands' products are out of scope for ecomOS brands. Sources 01p1, 02 and 03 carry that content. It is walled off in section 7, conflict 1, and never turned into a rule here. Two of the sources' own curation headers say so: source 02's export header says to skip "Retail Arbitrage (RA), Online Arbitrage (OA)... library poison" and the "BSR < 100k and 30% ROI" formulas; source 03's header says "DO NOT CAPTURE... exclusively Retail and Online Arbitrage reselling, which violates the 22-AMZ skip rules... Source should be discarded." Cards for both exist anyway. This playbook keeps only the model-agnostic mechanics from them (account documents, box limits, UK VAT, inventory breakdown statuses, carrier pickup) and marks each one.

**Sections by task.**

| Task | Load |
|---|---|
| Should this brand add Amazon, and when | 1, 3A, 3E, 5.1, 9 (channel decision memo) |
| Open and verify the seller account | 3B, 4 P2, 11 |
| Trademark, Brand Registry, hijacker protection | 3C, 4 P3, 5.8 |
| Screen a product or SKU for Amazon | 3D, 4 P4, 5.2, 6 |
| Fee stack, margin model, budget | 3E, 4 P5, 5.3, 6, 7 conflict 5 |
| Amazon-specific sourcing steps | 3F, 4 P6 (general sourcing lives in 18-COG) |
| Build or audit a listing | 3G, 4 P7, P8, P9, 5.4 |
| Send stock into FBA | 3H, 4 P10, P11, P12, 5.5 |
| Plan a launch | 3I, 3K, 4 P13, 5.6, 7 conflict 3 |
| Set up or review PPC | 3J, 4 P14, P15, 5.7 |
| Reviews and policy | 3K, 5.8, 7 conflicts 3 and 4 |
| Inventory, replenishment, storage fees | 3L, 4 P16, P17, 7 conflict 2 |
| Monthly report | 3N, 4 P16, 9 |

**What the agent must fetch before acting.**

- From the brand record: product, price, landed cost per unit, dimensions and weight, category, target marketplace, entity and VAT status, trademark status, existing Amazon account (if any), cash available for inventory and ads. Everything in this playbook tagged `[needs brand data]` is listed in section 10.
- From the data layer: any existing Amazon sales, sessions, unit session percentage, PPC spend, stock levels, storage age. If the brand has no Amazon history, say so in every deliverable and use the source heuristics only as a starting range.
- From the web: current fee tables, plan prices, size and weight limits, long-term storage threshold, restricted category list, Brand Registry terms, USPTO or UK IPO fees, Helium 10 UI. Everything tagged `[web check]` is listed in section 10. Do not quote a fee from this playbook to a client without a live check.

**Source credibility, stated up front.** All 4 sources are creators selling courses, coaching or affiliate tools. Source 01 (a 12-hour YouTube course) sells a paid program and carries Helium 10, Jungle Scout, LegalZoom and credit card affiliate links. Source 02 sells mentorship. Source 03 sells mentorship and carries SellerAmp, Keepa, SellerBoard and VA-program affiliate codes. Source 04 sells consultation calls and carries a Helium 10 affiliate link. Every dollar figure is self-reported and unaudited. Several figures are internally inconsistent inside the same source (trademark fee $250 vs $275 vs $225-275; long-term storage 180 vs 365 days vs "6 months"; storage rate $0.70 vs $0.75; label fee $0.30 vs $0.50; small parcel example $26.62 vs $266; several case study P&Ls that do not add up). Section 7 conflict 5 lists them. Section 12 rates each source. This playbook marks inconsistencies and never averages them.

**ecomOS rules that override any source.**

1. No invented claims in listings, ads or reports. One true, specific claim beats a buzzword.
2. No review manipulation and no incentivised reviews. No reimbursed purchases, no friends and family reviews, no refund-for-removal offers, no review gating. Source 01 describes these tactics; its own card `[eec0cf391ebf]` rejects them and so does this playbook.
3. No policy-breaching tactics: no false ship-from address, no gray-market barcodes, no duplicate accounts, no selling in restricted categories without approval.
4. Brand data over course figures. Where the brand has real numbers, the source heuristic is only a sanity check.
5. Amazon account writes need a human. The agent drafts listings, shipment plans, campaign structures and reports. A named person clicks publish, confirms a shipment, changes a price or a budget.

**Writing rules for anything client-facing.** Short sentences. Digits. No em dashes. No hype. Concrete before-to-after benefits. Do not repeat the sources' unsourced market statistics ("40% of sellers make $100k", "4,000 new sellers a day", "56% of shoppers start on Amazon") in any deliverable `[web check: verify or drop]`.

## 1. Scope and outcomes

**Covers.** Amazon as a sales channel for a brand's own product: channel fit, seller account and verification, trademark and Brand Registry, Amazon product research and validation, the Amazon fee stack and margin model, the Amazon-specific parts of sourcing (MOQ and capacity, samples, pre-shipment QC, FNSKU on packaging, freight mode, customs), listing build (title, bullets, description, images, attributes, backend keywords, A+), FBA inbound shipments, launch, Sponsored Products PPC, reviews and policy compliance, inventory and storage fees, and the failure patterns the sources report.

**Does not cover.** Point to the neighbour folder:

- General supplier search, negotiation, factory audits, freight forwarding: `18-COG-sourcing`. This playbook keeps only the steps that change because the stock goes to FBA.
- Product idea generation, demand research outside Amazon, crowdfunding validation: `01-PRD-product-research`. Source 01's crowdfunding material (Kickstarter and Indiegogo to fund a first run) is noted in section 3F but belongs there.
- Meta, TikTok and other off-Amazon paid traffic: `24-DEP-ad-deployment` and `10-MCR-paid-social-creative`. Google Ads: `12-GAD-google-ads`.
- Entity, tax, VAT registration, sales tax nexus: `20-FIN-finance-and-accounting`. Source 01's entity and S-corp guidance is lay opinion and is summarised only.
- Brand name, logo, packaging design: `04-BRD-brand`. Source 01's 5-tier logo price test is an example, not a rule here.
- Listing copy craft beyond the Amazon-specific structure: `11-ADC-ad-copy-deployment`.
- Retail arbitrage, online arbitrage, wholesale reselling: no folder. Out of scope for ecomOS.

**Business measures it moves.** Amazon revenue and units; net margin per unit after referral, FBA, storage, PPC and returns; PPC spend as a share of Amazon revenue; organic share of sales; sessions and unit session percentage; review count and rating; stock cover in weeks and stockout days; storage age and long-term storage fees; account health (order defect rate, policy flags); Brand Registry status and hijacker incidents.

## 2. Inputs the agent needs

| Input | From where | Required or optional | Why |
|---|---|---|---|
| Product spec: dimensions, weight, packaging, consumable or not, shelf life, materials | Brand record | Required | Sets FBA size tier, storage cost, expiry attributes, prep category, hazmat questions |
| Landed cost per unit (product + freight + duty + inspection) | Brand record or 18-COG output | Required | Every margin gate in 3E depends on it |
| Target sell price and competitor price band | Brand record + web (Amazon search) | Required | 3x cost rule, price band screens, price disparity check |
| Category and any gating or compliance needs (COA, certificates) | Brand record + `[web check]` | Required | Restricted category screen; compliance flags delay launch |
| Target marketplace(s) and currency | User | Required | Fees, VAT, box limits, plan prices differ by marketplace |
| Entity, EIN or company number, VAT registration status, bank, ID documents | Brand record (never store or print document contents) | Required for account setup | Verification fails on mismatches |
| Trademark status (filed, application number, class, mark type) | Brand record | Required for Brand Registry | Application number is enough to enrol per source 01 |
| Existing Amazon seller account or past suspended account | User | Required | Duplicate accounts risk a ban |
| Cash available for first inventory and first 3 months of PPC | User | Required | Sizes the first order and the revenue band to target |
| Monthly unit forecast or, if live, trailing sales velocity | Data layer | Required | Plan choice, inventory cover, reorder timing |
| Existing Amazon data: sessions, unit session %, PPC search term reports, stock, storage age | Data layer | Optional (required once live) | Weekly PPC review, monthly report, replenishment |
| Brand voice and claims list (approved, banned) | Brand record | Required for listing | No invented claims |
| Real product photos | Brand record | Required for listing | Generated images can redraw products |
| Helium 10 or Jungle Scout access | User | Optional | Research recipes in P4 and P7 assume Helium 10; say so when it is missing |
| Current fee tables, size limits, storage thresholds, plan prices | Web | Required | Every number in section 6 is dated |
| Off-Amazon audience assets (email list, social, existing DTC customers) | Brand record | Optional | Launch plan and Brand Referral Bonus |

## 3. Decision rules

Each rule: the rule, the condition, supporting mini playbooks (01p1, 01p2, 01p3, 02, 03, 04), conflicts, card ids. Where only one source says it, the rule says so. Where sources disagree, the rule keeps the strictest condition and points to section 7.

### 3A. Channel fit: whether and when to add Amazon

**R1. Decide the fulfilment model and the business model before opening an account.** Condition: any brand adding Amazon. FBA (Amazon picks, packs, ships, handles service) or FBM (brand ships) changes every fee line. The model is "own brand, own product"; arbitrage and wholesale are out of scope (section 7, conflict 1). Sources: 02 (FBA vs FBM before signup), 01p2, 01p3. `[79cb4207ec95]` `[a4f91430f890]` `[a4c6fdf106db]`

**R2. Default to FBA for a product that fits standard size tiers; use FBM only for heavy, fragile, low-volume or made-to-order goods, or where actual economics say so.** Condition: applies once the brand sells on Amazon at all. Source 01 claims FBA lifted sales 4 to 5x on its own and students' products through Prime eligibility; source 02 gives the FBM exceptions; source 01's own card `[e94ff8c9c6e7]` says to test conversion and contribution rather than assume a fixed multiplier. Keep the strict form: model both, do not assume the multiplier. Sources: 01p2, 01p3, 02. `[a4c6fdf106db]` `[fa55e3951630]` `[e94ff8c9c6e7]` `[79cb4207ec95]`

**R3. Add Amazon only when the unit economics gate (3E) passes on the brand's own landed cost, not on course figures.** Condition: every brand, every SKU. Source 04 says sellers who "don't know their numbers" fail; source 01 makes fee modelling the go/no-go step. Sources: 01p1, 01p3, 04. `[1b7f1a279442]` `[78d7c95b1453]` `[5702731d73e5]` `[needs brand data: landed cost, price]`

**R4. Budget the launch from line items, not a headline number.** Condition: any new Amazon launch. Source 01p3 gives a floor of about $3,500 "if everything goes perfectly" and recommends about $5,000 plus about $1,000 for PPC; its 7 case studies spent $5,800 to $26,524. Source 02 says private label needs about £5,000 to £10,000. These are presenter figures. The agent builds the brand's own line-item budget (P5). Sources: 01p3, 02. `[8ba56c7195cf]` `[c380d6dca0c8]` `[61933f8f37]` `[45eacb809b]` `[db37f80efe]` `[a4f91430f890]`

**R5. Match the target revenue band to the cash available.** Condition: choosing which product or SKU to launch first. Source 04: a $30,000 a month product needs about 3 months of inventory plus heavy ad spend; $1,500 to $3,000 a month products can still be viable. Source 01 says a first run should cover 3 to 6 months of sales. Sources: 04, 01p2. `[b640794fea47]` `[1b37755b2ef8]` `[needs brand data: cash for inventory and ads]`

**R6. Do not delay a launch to keep researching once the screens pass.** Condition: product passes 3D and 3E and a supplier is acceptable. Source 01 frames analysis paralysis as its students' most repeated and costliest mistake (AJ estimated about $30,000 from a 3-month delay; Brent estimated $20,000 to $30,000 a month from a 2-year delay). One case (Jeremy) shows delay can be supply-chain-driven; the fix there is a different manufacturer, not more speed. This is one source's opinion, repeated across its cases. Sources: 01p1, 01p3. `[b35c0005507d]` `[22226777874a]` `[734c8c132f]`

**R7. Prefer a differentiated product over a generic private-label clone.** Condition: choosing what to sell on Amazon. Source 01 attributes its 2 failure cases (Cam's leash plateau, Cam's prong collar bankruptcy) partly to generic private label and says a first-to-market product "grows the pie" when competitors enter. Its card notes private label can still work in some categories. Source 04 says to solve a real customer problem. Sources: 01p1, 01p3, 04. `[56fc5dcf9ebc]` `[58de052ddcc1]` `[78d7c95b1453]` `[7327612c90dc]`

### 3B. Account setup and verification

**R8. Choose the Professional plan once expected volume is above about 40 units a month; stay on Individual below that, and do not pay the monthly fee during pre-launch research.** Condition: US marketplace. Source 01: Professional $39.99 a month, Individual $0.99 per item, breakeven about 40 units; do not pay Professional while still researching. Source 03: same prices, crossover about 41 units, and claims Individual cannot win the Buy Box and makes ungating harder (Buy Box matters little for a single-seller own-brand listing). Source 02 UK: Individual 75p + VAT per unit; Professional £25 + VAT a month (about £30). `[web check: current plan prices and Individual plan limits]` Sources: 01p1, 01p3, 03, 02. `[8009156d0211]` `[608f261d2998]` `[d1fc1d8f24]` `[721a8236e673]` `[d3afe0f2d0ab]` `[f543c38ae44d]`

**R9. Never open a second seller account without telling Amazon, and disclose any old or suspended account.** Condition: anyone with a prior Amazon seller account, even a forgotten one. Source 01 and source 02 both cite a prior suspended account as a rejection cause. Sources: 01p1, 02. `[62ee9d521629]` `[52b388ae9bf4]` `[f543c38ae44d]`

**R10. Gather the document set before starting signup, and register under a name that matches ID and proof of address exactly.** Condition: every new account. Set: government ID (passport or licence), bank statement as a downloaded PDF (not a photo), proof of address, bank account and routing details, tax ID (SSN or EIN; UK company number), phone, business email, payment card. Source 01 says use a credit card and claims a debit or prepaid card triggers suspension; source 03 says a debit card worked for her. Conflict, both unverified (section 7, conflict 6). Strictest: use a credit card. Sources: 01p1, 02, 03. `[52b388ae9bf4]` `[d400e1bd04f8]` `[f543c38ae44d]` `[web check: current Amazon identity and payment requirements]`

**R11. Expect a live video verification call; mismatches add delay.** Condition: US and UK signups as filmed. Source 01: agent checks ID against face and submitted data; a mismatch (wrong birthdate) adds up to 48 hours; calls cannot be recorded; Amazon may ask for a utility bill after submission. Source 02: hold ID next to face, upload proof of address; usually done within 72 hours, sometimes 1 to 2 hours. Sources: 01p1, 02. `[52b388ae9bf4]` `[f543c38ae44d]` `[verify UI]`

**R12. Do not change bank details or business address in the first 1 to 2 months after approval.** Condition: post-approval. Source 01 only, no card; presenter says Amazon reads it as a scam signal. Do these changes before signup. `[web check: current account verification red flags]`

**R13. Add payout bank details and pass verification before sourcing or shipping any stock.** Condition: every new account. Source 02 only. `[3f1b8c4c6147]`

**R14. Use a real EIN, seller's permit and a separate business bank account; never mix personal and business spend.** Condition: US brand. EIN is free at irs.gov; seller's permit is free from the state .gov site; anyone charging for either is flagged as a scam by source 01. Mixing spend is an IRS flag and can pierce an LLC shield. Entity choice (DBA, LLC, LLC with S-corp election) is lay opinion in source 01; route to 20-FIN. Sources: 01p1, 01p2, 01p3. `[5922aa6e05a8]` `[89eb3eba5f62]` `[56008befb8c7]` `[0cd745664a]` `[web check: sales tax nexus and marketplace facilitator rules; consult a tax professional]`

**R15. Buy UPCs from GS1, not gray-market resellers.** Condition: any new ASIN. Source 01 quotes about $30 for a single GS1 code (a 10-pack was about $250 historically) and warns reseller codes "sometimes work" but risk listing or account problems. Figures across cases range $20 to $250. Sources: 01p1, 01p2, 01p3. `[608f261d2998]` `[web check: current GS1 pricing]`

**R16. If the marketplace applies VAT to Amazon fees, add it to the fee lines before judging margin.** Condition: UK sellers, including those not VAT registered. Source 02: 20% VAT on Amazon's selling and fulfilment fees, not shown by the calculator by default; in its £40 example it added about £1.20 to fees and about 60p to fulfilment. Source 02 only. `[394a2f9025bb]` `[web check: current VAT treatment of Amazon fees by marketplace]` `[needs brand data: VAT status]`

### 3C. Brand Registry and brand protection

**R17. File a trademark before or at listing creation; the application number is enough to enrol in Brand Registry, approval is not required.** Condition: brand selling its own branded product. Source 01: approval takes 6 to 18 months; enrolment needs the application. DIY filing cost is quoted as $250, $275 and $225 to 275 in different places (section 7, conflict 5); Calvin paid $650 via LegalZoom. Sources: 01p1, 01p2, 01p3. `[9ea0db787b78]` `[c3d8bb5dbf28]` `[f0afeac35357]` `[62ee9d521629]` `[web check: current USPTO and UK IPO fees and Brand Registry trademark requirements]`

**R18. Prefer a design (logo) mark when the name is generic or crowded; file a word mark only when the name is distinctive.** Condition: choosing mark type before filing. Source 01: logo marks are easier to win; a rushed, denied word mark forced Juliana into a rebrand with an estimated $100,000+ opportunity cost. Source 01 only. `[bcaa11727f52]` `[9ea0db787b78]` `[847aa6549bbc]`

**R19. Create the product listing (even imperfect) before applying for Brand Registry.** Condition: enrolment requires an ASIN. Source 01 only. `[c3d8bb5dbf28]` `[62ee9d521629]` `[verify UI: brandservices.amazon.com flow]`

**R20. Enrol in Brand Registry as soon as eligible and use what it unlocks.** Condition: every own-brand seller. Source 01 lists: A+ content, Vine (free with Brand Registry, about $200 without), Transparency (about 2,000 free codes), Sponsored Brands, Storefront, Subscribe & Save, Customer Engagement email, Brand Analytics, Attribution, Brand Referral Bonus, listing-edit protection and hijacker case escalation, plus a new-seller incentive (5% of the first $1 million in branded sales). Source 01 only; program terms change. `[049d4d03504b]` `[4fd40bd784d0]` `[d650da94a314]` `[f0d7832422e1]` `[web check: current Brand Registry benefits and incentive terms]`

**R21. Model Brand Referral Bonus as a credit on qualifying external sales, not as "15% becomes 5%".** Condition: sending off-Amazon traffic (email, social, ads) to the listing. Source 01 gives 2 framings, 15% to 5% and "about 10% back"; its card `[0665136f41d7]` says do not assume the 15% becomes 5%. Use tracked Attribution links; reconcile credited amounts. Sources: 01p2, 01p3. `[b70faf4d0983]` `[0665136f41d7]` `[web check: current Brand Referral Bonus mechanics]`

**R22. Use a Chinese manufacturer NNN agreement, not a Western NDA, and consider a provisional patent for a novel product.** Condition: novel product sourced overseas. Source 01 opinion only: NDAs are "unenforceable" in China; provisional patent about $75; utility patent about $1,090 in DIY fees or about $10,000 with a lawyer, and Jeremy's DIY filing took years. Legal advice is required. `[web check: current USPTO fees; verify NNN claim with counsel]` `[needs brand data: counsel]`

### 3D. Product research and validation thresholds

**R23. Screen out disqualifying products before judging upside: cheap, head-on competitive, seasonal or trend, restricted, gated or patented.** Condition: every candidate. Source 04's 4 elimination groups; source 01 adds a restricted list (alcohol, adult, dangerous goods, lithium batteries, tobacco, medication, CBD) and says CBD sellers were banned; source 04 names Baby, CDs and Vinyl, and battery electronics as trouble categories; source 01 tells beginners to avoid electronics, most appliances, and CDs, vinyl and books. Sources: 01p1, 04. `[f51e4d6ea760]` `[680f24307e2a]` `[c38799c1757b]` `[web check: current restricted and gated category lists]`

**R24. Price floor: target $25 or more; treat $15 as the absolute minimum; discard under about $10.** Condition: new own-brand launch. Source 01: $15 to $85 band, sweet spot about $25 to $30, $15 the firmer floor; its own cases include successes outside the band. Source 04: about $25+, most profitable items over $30, discard $7 to $10 items because about $1 per click PPC erases profit in 2 to 3 clicks. Merged rule keeps the strictest: $25+ target. Section 7, conflict 8. Sources: 01p1, 01p3, 04. `[e3b79ddc217f]` `[69e72ae58a]` `[78d7c95b1453]` `[680f24307e2a]`

**R25. Demand and low competition must both hold; missing either kills the product.** Condition: every candidate. Source 01: high search volume with no purpose-built listing is the ideal; source 04: review count max 300 to exclude dominant listings. Sources: 01p1, 04. `[9592e17b4a23]` `[032cac3738fc]` `[c38799c1757b]`

**R26. Reject brand-dominated categories.** Condition: 1 or 2 legacy brands take most category sales (Nike, Adidas, Puma in soccer balls). No numeric threshold in either source. Sources: 01p1, 04. `[6b24a59a41c1]` `[78d7c95b1453]`

**R27. Reject tight page-1 price clusters; prefer wide legitimate spreads.** Condition: search the main keyword on Amazon and record page-1 prices. Tight (source 04: $7 to $13 for tongue scrapers; source 01: floss picks $2 to $16) means buyers pick on price and stars. Wide ($20 and $100 on the same page; $5 vs $95) means buyers pay for differences. Sources: 01p1, 04. `[6b24a59a41c1]` `[aabcbafc75f4]`

**R28. Prefer products with many distinct search phrasings.** Condition: keyword variability test. Source 04: dozens of variants (slim, wallet, waterproof, for men) give cheap long-tail entry; 1 or 2 monolithic terms mean one contested battle. Source 04 only. `[c7f835842a76]`

**R29. Require listing age of at least 8 months on the comparables you validate against.** Condition: using Helium 10 Black Box to judge evergreen demand. Source 04 only; filters fads. `[c38799c1757b]` `[verify UI]`

**R30. Mine 1-star to 3-star reviews of selling competitors and put the fixes into the product brief; treat a 4.1 to 4.3 star product doing $5,000+ a month as proof of demand with a spec sheet attached.** Condition: shortlisted product. Source 04 also uses the share of 1-star reviews (12% in its example) and weak images as opportunity signals. Source 01 does the same with New Releases and 1 to 3 star reviews. Sources: 01p1, 04. `[85e208c54bc9]` `[e3b79ddc217f]` `[d25b670164dc]`

**R31. Do not copy any presenter's filter recipe verbatim.** Condition: running Black Box or Magnet. Source 04 says so itself: everyone using the same filters surfaces the same products. Two recipes exist and differ (section 7, conflict 9): source 01 uses price $15 to $85, monthly revenue $5,000 to $80,000 and max average rating 3.5; source 04 uses price $25 to $60, revenue $5,000 to $20,000, review count max 300, listing age min 8 months, image count max 4. Sources: 01p1, 04. `[e3b79ddc217f]` `[c38799c1757b]`

**R32. Validate a keyword gap live on Amazon, not only in the tool.** Condition: any phrase with search volume and title density 0. Source 01: "bourberine tea" showed 1,200+ monthly searches in Magnet and zero matching listings on Amazon at the time. Cross-check Google Trends direction and Keyword Planner, but Google interest is not Amazon purchase intent. Source 01 only. `[032cac3738fc]` `[ce7276f8b3d0]` `[0d48e4ef7ef2]`

**R33. Cross-check tool revenue estimates with BSR and the Jungle Scout sales estimator; treat all of them as modelled numbers.** Condition: any revenue figure used in a screen. Sources: 01p1, 01p3, 04. `[ff8b02ff28]` `[0232a56aeb27]`

**R34. Giftability is a tie-breaker, not a gate.** Condition: two otherwise similar candidates. A product that works for several occasions plus self-purchase captures Q4 without being seasonal. Source 01's Q4 estimate is about 3x normal volume (presenter claim). Sources: 04, 01p1. `[8397ad752638]` `[f3b427a78dee]`

### 3E. Unit economics and the fee stack

**R35. Net margin gate: 30% or more after landed cost and all Amazon fees, or do not launch.** Condition: every SKU, computed on brand data. Source 04: 30%+ after product, shipping, duties, taxes and FBA fees. Source 01: thirds heuristic (about a third product, a third Amazon fees, a third profit), so 30 to 33% net. Source 02's 30% ROI is a reseller metric on cost, not a net margin; do not mix them. Sources: 01p1, 01p3, 04. `[1b7f1a279442]` `[f9ed217597]` `[32df6696fa]` `[78d7c95b1453]` `[needs brand data: landed cost, price]`

**R36. Price at 3x unit manufacturing cost or more, and position premium rather than cheapest for a differentiated product.** Condition: new product pricing. Source 01: referral plus pick and pack take about a third of price, closer to 20 to 25% for higher-priced light items; premium positioning is the presenter's strategy, not a universal law. Source 01 only. `[e55bba302c29]` `[de4c95b021]` `[d0428dbc14f4]`

**R37. Model the full fee stack, line by line, before committing stock.** Condition: every SKU. Lines from source 01 (all `[web check]`): referral fee (source simplifies to 15%; varies by category); FBA pick and pack (small standard about $2.16 to $2.70, large standard examples $4.25 and $4.95, apparel plus $0.30 to $0.40); monthly storage ($0.70 or $0.75 per cubic foot January to September, $2.40 October to December); long-term storage ($6 to $6.90 per cubic foot or $0.15 per item, whichever is greater, after 180 or 365 days, conflict 5); labelling if Amazon applies FNSKU ($0.30 or $0.50 per unit; 38p in the UK per source 02); prep services ($0.50 to $2.00 per unit); return processing fee (size and weight based) and disposal (about $0.50 per unit); Individual plan fixed closing fee ($0.88 in one example); plan fee; PPC; inbound freight; duty (10 to 20% from China per source 01); customs bond ($100 single, about $400 annual). Source 02 adds VAT on fees in the UK. Sources: 01p1, 01p2, 01p3, 02. `[5702731d73e5]` `[5a52954b5a]` `[cff0a2d5c5]` `[de97ba8ee8e6]` `[dd7da612975b]` `[996e5b8cd15d]` `[a5c9b2ba33c2]` `[0e36997070ce]` `[394a2f9025bb]` `[fa55e3951630]`

**R38. Compute storage cost from cubic feet, not from guesswork.** Condition: every SKU. Source 01: length x width x height in inches divided by 1,728, times the per-cubic-foot rate; a 3x4x5 inch unit is 60 cubic inches, about $0.026 per unit per month at $0.75. Multiply by expected months in the warehouse. Source 01 only. `[de97ba8ee8e6]`

**R39. Design packaging to the smallest size tier that protects the product.** Condition: packaging decisions before the first run. Source 01: 98% of products fall in small or large standard; a small-standard tier saved about $0.64 per unit in one example ($2.16 vs $2.70). Source 01 only. `[cff0a2d5c5]` `[web check: current size tier limits]`

**R40. Read the monthly P&L by fee line, never by revenue.** Condition: every month once live. Lines: revenue, product cost, referral, FBA pick and pack, storage, inbound, PPC, subscription, returns, other, net. A stockout month is not a demand signal. Sources: 01p1, 01p3. `[4e439ec1d0c9]` `[2f107a408cee]` `[e507ae86a8]` `[7e8e8bfd3833]` `[f9ed217597]`

**R41. Audit Amazon's fee charges and lost or damaged inventory claims regularly; late claims may not be paid.** Condition: monthly once live. Source 01 names Helium 10 Refund Genie; source 03 names SellerBoard's reimbursement template and a 2-week escalation threshold outside Q4. Sources: 01p2, 01p3, 03. `[c4af442b1b]` `[bf7de81b2309]` `[13ee6100527e]`

**R42. Set the PPC budget from cost per click, conversion rate and margin, and keep at least about $1,000 for launch PPC.** Condition: launch budget. The $1,000 is source 01's rule of thumb. Sources: 01p3. `[12b47e3bd2]` `[needs brand data: margin per unit]`

### 3F. Sourcing and samples (Amazon-specific only; the rest is 18-COG)

**R43. Ask for maximum monthly production capacity, not only MOQ, before the first order.** Condition: every manufacturer. Source 01: Calvin never asked, outgrew his manufacturer and estimated a $20,000+ loss. Source 01 only. `[458ab7dcf449]` `[05aad4186d69]` `[30cfab7b2654]`

**R44. Always get a sample, and pay for the printed or custom sample when one is offered.** Condition: before any production run. Source 01: Veno Cards skipped a $200 to $300 printed sample and shipped defects; off-the-shelf samples usually cost only shipping ($25 to $45 international). Source 01 only. `[6f30eee6c39c]` `[05c3449a22]`

**R45. A passed sample does not certify the bulk run; inspect before releasing the balance and before the stock reaches FBA.** Condition: every bulk order. Source 01: pay 30% upfront and 70% after a third-party inspection (about $100; Alibaba's service about $118 a day); inspectors must confirm barcodes scan; Calvin's uninspected run cost about $10,000 in returns and bad reviews. For a first shipment, ship to yourself first when feasible. Source 01 only. `[00605a61c7e0]` `[5001ae00f465]` `[1dada9a298]`

**R46. Use a reversible payment method (credit card, PayPal, Alipay) for early orders; move to wire only once trust exists.** Condition: new manufacturer relationship. Source 01 only; reversible methods carry about 3% fee. `[00605a61c7e0]`

**R47. Print the FNSKU on the packaging at the factory, or label yourself; never let Amazon label.** Condition: every FBA unit. Source 01 quotes $0.50 and $0.30 per unit for Amazon labelling; source 02 quotes 38p. For a private label product the FNSKU printed on the box avoids stickers and labour. Sources: 01p2, 01p3, 02, 03. `[a5c9b2ba33c2]` `[996e5b8cd15d]` `[d9137e094ae3]` `[03f3588ec184]`

**R48. Choose freight mode by urgency and weight; sea is about a third of air cost but 4 to 6 weeks plus customs.** Condition: every inbound from overseas. Source 01p2 recommends air for a first shipment (5 to 10 days, lower customs risk); source 01p1's AJ calls full air "throwing money down the drain" when not urgent and split half and half. Section 7, conflict 7. Landed cost example: about $11 per unit air vs about $7.50 sea for the same product. Use a freight forwarder for sea. Sources: 01p1, 01p2, 01p3. `[dd5ab39da4c6]` `[0e36997070ce]` `[982d07654f]` `[962618d3768f]` `[2e76599ac49d]`

**R49. Source consumables domestically unless the overseas regulatory path is confirmed.** Condition: food, supplements, anything ingested. Source 01's cases (electrolytes, caffeinated gum, caffeinated tea) used US manufacturers; the source does not explain the regulatory reasoning. Source 01 only. `[8e7b2048c3]` `[409cdd9f62e7]` `[web check: FDA and import labelling rules for the product]`

**R50. Route everything else to 18-COG.** Alibaba filters (Trade Assurance, Verified Supplier, transactions, export markets, factory video), ThomasNet, Europages, trade shows, Jungle Scout Supplier Database, sourcing agents, cold outreach, MOQ negotiation ("quote 50,000, start with 500"), factory audits, middleman detection, labour conditions. Sources: 01p1, 01p2, 01p3. `[516fc94151074]` `[2be091c6eb]` `[bfd58753bfa0]` `[088df087220a]` `[92fe3ae2bbcc]` `[00a90593aced]` `[8115f16806de]` `[904e60a14493]` `[3aa386e7b617]` `[34c87d59e1]` `[e3dd370433]` `[3f72af588c]`

**R51. Crowdfunding to fund a first run belongs in 01-PRD.** Source 01's Brent ($15,000), AJ (about $107,000 total) and Jeremy ($11,000) cases are examples, not a rule here. `[bd7b6cb00090]` `[5c218c90e46e]` `[cfd113d1ee3b]` `[482f30b7cac2]` `[555c1a9c93]` `[732b192e50]` `[58573c3182]`

### 3G. Listing build

**R52. Put the number 1 target phrase as the first 2 words of the title and of the first bullet; front-load the keyword, not the brand name, unless the brand is already famous.** Condition: every new listing. Sources: 01p2, 01p3. `[ce7276f8b3d0]` `[ea92d3208742]` `[3926ce74869f]` `[f55f316136]`

**R53. Sort keywords into 3 buckets and only use the first 2: exact core phrases, true supporting attributes, and generic buzzwords to cut.** Condition: keyword research for title, bullets, description and backend. Source 01 kept "organic", "blood sugar", "caffeine-free" and cut "wellness", "detox", "energy", "antioxidant-rich blend". Source 01 only. `[395420566b52]`

**R54. Write 5 bullets that lead with benefits, carry one true specific claim each, and never invent a claim.** Condition: every listing. Source 01 recommends a money-back guarantee bullet (true of Amazon's return policy) `[web check: current return policy]`. ecomOS rule: no invented claims. Sources: 01p2, 01p3. `[9c6378ecc053]` `[da17cf4d53]`

**R55. The main image must differentiate on the search grid: product as hero, clean, high contrast against white, minimal packaging or logo dominance.** Condition: every listing. Source 01: black packaging with red "HIGH CAFFEINE TEA" against pale competitors. Use the real product photo; generated images can redraw products. Sources: 01p2, 01p3. `[55551166fe42]` `[3926ce74869f]` `[64df5a657d]`

**R56. Use all secondary image slots (up to 8) including at least one comparison chart; do not launch with DIY or low-quality images.** Condition: every listing. Source 01: "Mina" reportedly lost over $10,000 from poor launch images; Daryl and Amanda estimated $5,000 lost to Canva photos. Source 04 uses 4 or fewer competitor images as a weakness signal. Sources: 01p2, 01p3, 04. `[55551166fe42]` `[a4c6fdf106db]` `[64df5a657d]` `[c38799c1757b]`

**R57. Fill every attribute field correctly, especially expireable, shelf life in days, units per sellable unit, and the category.** Condition: new listing. Shelf life controls how long Amazon holds stock. Check a comparable competitor's category at the bottom of its page if unsure. Source 01 only. `[f78efe258b21]` `[b50ed76429]` `[verify UI: fields vary by category]`

**R58. Fill backend search terms and set a future offer start date so launch traffic lands on a live, stocked listing.** Condition: new listing with a planned launch push. Source 01 only. `[29b5729fab42]` `[57a6c36160]`

**R59. Build a new listing for the brand's product; join an existing ASIN only when the brand's product already has one.** Condition: own-brand product. Source 02's "join the ASIN, price to the lowest FBA seller, choose Amazon's barcode" rule is a reseller rule; the only own-brand case is when resellers already listed the brand's product, in which case Brand Registry gives the brand control of the detail page. Sources: 01p2, 02. `[f78efe258b21]` `[cee7349150a1]` `[f0d7832422e1]`

**R60. Expect compliance flags; plan buffer time.** Condition: supplements, "diet", anything a keyword scanner can misread. Source 01's electrolyte product needed a Certificate of Analysis after a false "diet product" flag. Source 01 only. `[web check: current category compliance triggers]`

**R61. Use A+ content and Listing Analyzer or Index Checker once Brand Registered.** Condition: after enrolment. Source 01 names the tools but gives no step-by-step. `[049d4d03504b]` `[db44931641c9]` `[verify UI]`

### 3H. FBA inbound shipments

**R62. Build the shipment from measured case dimensions and weight; the limits are hard constraints.** Condition: every shipment. US per source 01: no case side over 25 inches, case under 50 lb (example: 45 units, 11x18x10 inches, 37.35 lb). UK per source 02: no side over 63.5 cm, box under 23 kg. Sources: 01p2, 02. `[b541f1c3cafd]` `[03f3588ec184]` `[web check: current limits by marketplace]`

**R63. Save a case-pack template so repeat shipments reuse the same counts and dimensions.** Condition: after the first shipment. Source 01 only. `[b541f1c3cafd]` `[verify UI]`

**R64. Check every box label before dispatch: weight, dimensions, ship-from and ship-to match the carrier label; Amazon may split a shipment across fulfilment centres.** Condition: every shipment. Source 01: a wrong ship-from address cost the presenter about $5,000 in lost sales. Source 01 only. `[ebc91c8e96fb]`

**R65. Use the true ship-from address. Never enter a false address to steer fulfilment-centre assignment.** Condition: every shipment. Source 01 describes setting a California address when importing from China as "technically against Amazon's rules... at your own risk". No card supports it. ecomOS rule: no. Section 7, conflict 4.

**R66. Small parcel through Amazon's partnered UPS rate for boxes; LTL pallets for large volumes.** Condition: shipment size. Source 01: LTL can roughly halve freight versus repeated small parcel sends; LTL needs a trucking company, palletising, wrapping and a Bill of Lading; the small-parcel example (9 cases, 336 lb) is quoted as $26.62 in the part 2 mini playbook and about $266 in the card (conflict 5). Source 02: UPS partnered is cheaper than DPD in the UK; never drop off at a fulfilment centre. Sources: 01p2, 02. `[3232a9886a40]` `[962618d3768f]` `[03f3588ec184]` `[f2e93ddb9b51]`

**R67. Keep every carrier receipt and Bill of Lading; Amazon may not pay for lost inventory without your proof.** Condition: every shipment, especially pallets. Source 01: a misplaced BOL nearly cost $10,000. Source 01 only. `[bc218f44de6b]` `[77a1ff7d9047]`

**R68. A shipment is not done when a tracking number appears; book the carrier collection.** Condition: UK small parcel via UPS. Source 02 only. `[f2e93ddb9b51]`

**R69. Read the FBA Inventory Breakdown before assuming loss: FC transfer is normal; escalate only past the normal window.** Condition: every inbound. Source 03: transit 3 to 4 days, check-in 1 to 2 weeks outside Q4, escalate past 2 weeks, up to 1 month in Q4. Source 01: 3 to 6 weeks from ship to sellable, longer in Q4. Sources: 03, 01p2, 01p3. `[13ee6100527e]` `[24ca880132fb]` `[bc218f44de6b]`

**R70. Answer the dangerous-goods and prep questions accurately; set prep category for fragile, liquid, adult or baby items; for multipacks label the poly bag, not each unit.** Condition: every shipment. Sources: 01p1, 01p2, 02. `[175a95a101de]` `[b541f1c3cafd]` `[03f3588ec184]`

### 3I. Launch

**R71. Concentrate genuine sales into launch day and the first weeks, with the listing live, stocked and PPC on.** Condition: every new listing. Source 01's model: click-through, reviews and sales velocity drive rank; presenter's best result about 75 reviews in week 1. Its card marks launch velocity a hypothesis, not a confirmed ranking factor, and says use genuine demand only. Source 01 only. `[463691efbbbf]` `[aee1983890]` `[704c9fab96]` `[57a6c36160]` `[74e3240100]`

**R72. Build the audience before launch, not after: social content, an email waitlist, a pre-launch group, seeded small influencers.** Condition: differentiated product with a story. Source 01: at least 5 case studies; Leanne and Logan launched quietly and were copied within months; influencer sweet spot 5,000 to 10,000 followers for free-product collaborations; 85 boxes seeded in one launch. Source 01 only. `[f7ca6bfbed66]` `[e1bd5b72a974]` `[7f7fc935deaf]` `[8ff3fc81251d]` `[5b52f3c9f179]` `[355294051c5f]` `[c5fd5ed5d1d3]` `[ca1444b7a40f]`

**R73. Launch 1 SKU, not 4 colours or sizes, unless the category requires variants.** Condition: first launch. Source 01: Cam's colour variants cost about $2,500; Juliana's apparel sizing was required and not a mistake. Source 01 only. `[10a62cce57]` `[941d2d31ce]`

**R74. Use only compliant launch levers from source 01's list of 10: social media, email waitlist, Facebook group, influencers, Amazon Live, PPC automatic campaign, Cialdini's principles in assets, the 80/20 focus, and launch-week discounting through Amazon's own tools. Drop "manual review generation".** Condition: every launch. Source 01 describes the review tactic while flagging it as against ToS. Section 7, conflict 3. `[e21952afd0db]` `[63de606f452d]` `[ab5555cbca]` `[eec0cf391ebf]`

**R75. Use price as an inventory throttle when selling faster than you can restock.** Condition: stockout risk with weeks to the next delivery. Source 01: Carnivore Electrolytes went $24.99 to $29.99 to $34.99 and "sales stayed the same"; Juliana did the same. Two cases, one source. A price change is an account write and needs a human.

**R76. Recover a stalled launch with data and traffic, not a relaunch of the same listing.** Condition: launch that did not take. Source 01 only, thin on how. `[ff442ba83825]` `[2e469b7e6c]`

### 3J. PPC

**R77. Run an automatic Sponsored Products campaign first to discover converting search terms, then build manual campaigns from that data.** Condition: no keyword history. Source 01 only. `[77301bfbc801]` `[86640d985c9d]`

**R78. Split the automatic campaign into 4 ad groups by targeting group (close match, loose match, substitutes, complements) with separate bids; never one blended bid.** Condition: every automatic campaign. Source 01's live example bids: close $0.92, loose $0.72, substitutes $0.13, complements $0.71; not benchmarks. Dynamic bids up and down can raise a bid up to +100%. Source 01 only. `[b5ced20e1372]` `[77301bfbc801]`

**R79. Build manual keyword campaigns with broad, phrase and exact match, filtering Magnet output before adding terms.** Condition: after 2 to 4 weeks of automatic data (the source gives no exact wait). Source 01's demo filters: under 5,000 monthly searches, 2 words minimum, 100 competing products maximum, 2 keyword sales a month minimum. Source 01 only. `[c977be9f1949]` `[9b0fd6fbf0fb]`

**R80. Run product targeting on competitor ASINs, one ad group per competitor brand so profitability is readable.** Condition: competitors with weaker listings or higher prices. Source 01 only. `[32a766a06882]`

**R81. Add negative keywords to every campaign; mandatory with broad or phrase match.** Condition: every live campaign. Source 01 only. `[f14aac7c2e85]` `[3f4076bb096d]`

**R82. Judge PPC on net profit, not sales; test switching it down once organic momentum exists.** Condition: listing with organic sales. Source 01: Carnivore Electrolytes turned PPC off in month 6, sales dipped slightly, profit rose; Cynthia's overspend drove her loss. Source 01 only. `[abf98f0a62]` `[cbf54bbe6b]` `[4e2dab02af]` `[2dfb813269]`

**R83. If a listing cannot advertise, isolate the trigger: strip the description, then remove images one by one.** Condition: "controversial product" or ineligibility flag. Source 01's diagnostic, not guaranteed. `[web check: current ad policy for the category]`

### 3K. Reviews and policy compliance

**R84. Use only Amazon's permitted review-request path for eligible orders, without selecting satisfied buyers.** Condition: every order. Source 01's card; source 03 mentions an automated request about 5 days after delivery. Sources: 01p2, 03. `[eec0cf391ebf]` `[9360a21466]` `[69b0a58ad59d]`

**R85. Never reimburse purchases, offer money, discounts or gifts for reviews, recruit friends, family or associates, or link a refund to a review change.** Condition: always. Source 01 describes all of these as tactics "people use" and admits they breach ToS; source 01p1 describes "alluding to" a refund to get seller feedback pulled. ecomOS rule: none of it. Section 7, conflict 3. `[eec0cf391ebf]` `[8446fdb9deaa]`

**R86. Use Vine only under current terms and only when the product is ready; expect it can lower the rating.** Condition: Brand Registered, new ASIN. Source 01: Connor's Vine reviewers were outside the target audience and cost about $4,000+. `[eec0cf391ebf]` `[9360a21466]` `[web check: current Vine terms]`

**R87. Contest seller feedback that is really a product review within 30 days; never negotiate its removal with a benefit.** Condition: misplaced feedback. Source 01 only. `[8446fdb9deaa]` `[web check: current feedback removal rules]`

**R88. Watch Account Health weekly: order defect rate, negative feedback, A-to-z claims, chargebacks, policy notices.** Condition: live account. Source 01's healthy example: 0% defects over 743 orders. `[verify UI]`

**R89. Do not use gray-market UPCs, false ship-from addresses, duplicate accounts, or shared devices and networks with reviewer accounts.** Condition: always. Sources: 01p1, 01p2, 01p3. `[608f261d2998]` `[eec0cf391ebf]`

### 3L. Inventory and IPI

**R90. Send 3 to 6 months of cover per inbound and start the next order at 2 to 3 months remaining; for an unproven product send a smaller first batch and scale to sell-through.** Condition: replenishment. Source 01 gives the 3 to 6 month range in 3 places; its Cam prong collar case shipped 100% and paid long-term storage; its cards say the range is a heuristic. Section 7, conflict 2. Sources: 01p2, 01p3. `[1b37755b2ef8]` `[24ca880132fb]` `[390e894204]` `[dd7da612975b]` `[59201e11d9]` `[d573b8e605]` `[needs brand data: velocity, lead time, cash]`

**R91. Treat a stockout as the failure mode to avoid; reorder early, rush if needed.** Condition: velocity rising. Source 01: under-ordering is its most repeated mistake (AJ over $100,000; Calvin about $100,000 across 3 stockouts; Cam about $5,000); a stockout can drop rank and, per the presenter, get an account flagged. Source 01 only, presenter's characterisation. `[7b7a6cece1eb]` `[6804638a759c]` `[2cca0ae31a]` `[35387918cf]` `[e62d78f3c87e]` `[8f3cf8e89ad3]`

**R92. Watch inventory age; act before the long-term threshold.** Condition: any slow SKU. The threshold is stated as 365 days, 180 days and "beyond 6 months" inside source 01 (conflict 5) `[web check: current long-term storage window]`. Options: sell through faster, request removal, or accept the fee if removal costs more. `[de97ba8ee8e6]` `[e62d78f3c87e]` `[dd7da612975b]`

**R93. Plan Q4 stock early: about 3x normal volume (presenter claim), longer check-in, higher storage rate.** Condition: any product with Q4 demand. Sources: 01p1, 01p3, 03. `[f3b427a78dee]` `[13ee6100527e]` `[de97ba8ee8e6]`

**R94. IPI, storage limits and restock limits are not covered by any source; fetch them live.** Source 02's header names IPI but the transcript does not cover it. `[web check: current IPI thresholds and capacity limits]`

### 3M. Measurement

**R95. Read sessions and unit session percentage separately before diagnosing.** Condition: weekly. Source 01: traffic can rise while conversion falls and total sales still rise. `[73e0a4ad19dc]`

**R96. Track off-Amazon ad attribution before trusting it.** Condition: any external traffic. Source 01: Juliana's Facebook spend was mostly wasted until tracking existed. `[d650da94a314]`

**R97. Map revenue by month for a full year before calling a product failed.** Condition: apparent decline. Source 01: AJ's January dip was seasonal. `[2e76599ac49d]`

## 4. Procedures (implementation)

Each procedure: goal, preconditions, steps with settings, checks, rollback. Steps that touch the Amazon account are drafted by the agent and executed by a named human. All Seller Central and Helium 10 paths carry `[verify UI]`.

### P1. Channel decision

Goal: a yes, no, or not-yet on adding Amazon for one product.
Preconditions: brand record with product spec, landed cost, price, category, cash; access to Amazon search.
1. Run the channel fit checklist (5.1). Fail on any hard stop (restricted category without approval, no trademark plan, no cash for 3 months of stock plus about $1,000 PPC).
2. Run the product research screen (P4) on the brand's product against its Amazon category: price floor, price disparity, brand dominance, keyword variability, competitor review counts.
3. Run the fee and margin model (P5) on brand data. Gate: 30% net or more after all fees (R35).
4. Size the first order and the PPC budget against cash (R4, R5, R90).
5. Write the channel decision memo (9.1) with the numbers, the gates passed or failed, and the `[web check]` items still open.
Checks: every number traces to brand data or a live web check, none to a course figure alone.
Rollback: none; the memo is advisory.

### P2. Seller account signup and verification `[verify UI: entire flow]`

Goal: a verified Professional or Individual account able to receive payouts.
Preconditions: R9 cleared (no undisclosed prior account); document set from R10; entity and bank in place; decision on plan (R8).
US flow per source 01p1 and 03:
1. Go to sell.amazon.com, Sign up. Use a dedicated business email.
2. Choose plan. Professional ($39.99 a month per sources) if over about 40 units a month is expected at go-live; Individual otherwise. Source 03 says both plans were charged the first-month fee at signup `[web check]`.
3. Select business location and entity type. Non-US brands: source 01 suggests a US LLC first; route to 20-FIN.
4. Enter EIN as the company registration number; registered business address (registered agent if the home address is not the business address); verify the business phone by SMS PIN.
5. Enter personal details: citizenship, ID type and number, expiry; confirm sole owner or add co-owners.
6. Enter bank account for payouts (source 01: US Bank for US; Payoneer or WorldFirst for non-US `[web check: exact company names]`). If the bank cannot be verified instantly, a statement PDF upload follows.
7. Enter the payment card (credit card per source 01; source 03 says debit worked; conflict 6).
8. Choose the store name (need not match the entity; changeable later).
9. Answer: have a UPC (yes, GS1); own brand (yes); registered trademark (say no if only filed; add Brand Registry later).
10. Upload ID and bank statement PDF. Submit.
11. Attend the video verification call. Have the same ID in hand. Expect up to 48 hours added for any mismatch; be ready with a utility bill if asked.
UK flow per source 02:
1. Choose amazon.co.uk. Compare plans (Individual 75p + VAT per unit; Professional £25 + VAT a month per source) `[web check]`.
2. Register under the name that matches ID and proof of address. Complete the live video call: ID next to face, upload proof of address. Typical 72 hours.
3. Add bank and payment details before sourcing.
Checks: account shows verified; payout details saved; no pending document requests. Do not change bank or address for 1 to 2 months (R12).
Rollback: if rejected, appeal with the exact document mismatches fixed; source 02 mentions paid appeal specialists; do not open a second account.

### P3. Trademark filing and Brand Registry enrolment `[verify UI]` `[web check: current fees and requirements]`

Goal: Brand Registry active on the brand's ASINs.
Preconditions: brand name conflict screen done (04-BRD); mark type chosen (R18); listing exists (R19).
1. File at uspto.gov (Trademarks, Apply Online) or the UK IPO: goods and services class, mark image or literal text. Source 01 quotes DIY fees of $250, $275 and $225 to 275 (conflict 5). Lawyer add-on: "a couple hundred" is reasonable per source 01; $1,000 to $2,000 called overpriced.
2. Record the application serial number in the brand record.
3. Go to brandservices.amazon.com. Enrol with: trademark application or registration number, mark type, brand name exactly as filed, seller account, product ASIN, images of product and packaging showing the brand (source 01 mentions a mockup-photo shortcut when stock is not yet in hand; use real packaging where it exists).
4. Verify ownership when Amazon contacts the trademark correspondent.
5. After approval: turn on A+ content, enrol in Brand Referral Bonus (Brands dashboard), set up Transparency if hijack risk exists, review Brand Analytics.
Checks: Brand Registry shows the brand and ASINs; listing edits by others are blocked; Sponsored Brands available.
Rollback: a denied word mark may force a rebrand (Juliana); the design mark path (R18) is the hedge.

### P4. Product research screen (Helium 10 recipes and manual checks) `[verify UI: Helium 10 and Amazon]`

Goal: a pass or fail on a candidate product or SKU, with the evidence in the product screen sheet (9.2).
Preconditions: Helium 10 access (or say the recipe cannot run); category known.
A. Black Box first pass (two recipes; do not copy either verbatim, R31):
1. Tools, Black Box, Products tab.
2. Category: one ungated category the brand's product sits in. Source 04 names Home & Kitchen, Patio Lawn & Garden, Pet Supplies, Office Products, Industrial & Scientific, Kitchen & Dining, Sports & Outdoors, Tools & Home Improvement as open; avoid Baby, CDs and Vinyl, battery electronics. Source 01 also avoids electronics, appliances, books.
3. Source 04 recipe: Review Count Max 300; Price $25 to $60; Monthly Revenue $5,000 to $20,000; Listing Age Min 8 months; Image Count Max 4. His run returned 500+ products.
4. Source 01 recipe: Price $15 to $85; Monthly Revenue $5,000 to $80,000; Max average rating 3.5 to surface high-selling, badly reviewed listings.
5. Scroll results manually; there is no further automated filter in either source.
B. Magnet keyword gap (source 01):
1. Tools, Magnet. Seed with the product's core terms. Set title density filter to 0 to 0. Sort by Magnet IQ score. Scan all pages for a phrase with real volume and no matching product.
2. Validate live: search the exact phrase on Amazon; confirm no purpose-built listing.
3. Cross-check Google Trends direction and Keyword Planner related terms; confirm Amazon demand for the exact phrase back in Magnet.
C. Cerebro reverse ASIN (source 01): paste the closest competitor ASIN, Get Keywords, sort by Magnet IQ, look for a high-volume phrase the incumbent's title misses; filter title density 0.
D. Amazon autocomplete: type stems, note suggestions, cross-check with X-ray revenue.
E. New Releases and Best Sellers: note "first available" dates; read 1 to 3 star reviews of strong sellers.
F. Manual checks on page 1 of the main keyword: record prices (R27); count dominant brands (R26); list distinct search phrasings (R28); note review counts of the top 10 (R25).
G. Review mining (source 04): sort Black Box results by rating low to high; open 4.1 to 4.3 star products doing $5,000+ a month; read 1-star reviews; note the share of 1-star; note image quality; write each recurring fixable complaint as a line in the product brief. Repeat post-launch on your own and competitor listings.
H. Cross-check any revenue estimate with BSR in the Jungle Scout sales estimator (marketplace, category, BSR) and the FBA calculator (R33).
Checks: the screen sheet shows pass or fail per check with the evidence; every filter value is marked as a presenter heuristic.
Rollback: none.

### P5. Fee and margin model

Goal: net margin per unit and a line-item launch budget on brand data.
Preconditions: dimensions, weight, landed cost, price; live fee tables `[web check]`.
1. Find a comparable ASIN of the same size and weight. Open the Amazon FBA revenue calculator (Seller Central, Resources) `[verify UI]`. Enter price, dimensions, weight, cost of goods. Read referral, fulfilment, and monthly storage per unit.
2. Add lines the calculator does not show: VAT on fees where it applies (UK 20%, R16); inbound freight per unit; duty (source 01: 10 to 20% from China) and customs bond; inspection; FNSKU printing; prep; returns allowance (return fee plus disposal about $0.50 or refurbish); PPC per unit at launch (from CPC, conversion, margin, R42); plan fee spread over units; long-term storage risk.
3. Storage: cubic inches divided by 1,728 times the rate; months in warehouse; Q4 rate (R38).
4. Compute net margin = (price minus all lines) divided by price. Gate 30% (R35). Also check price is 3x or more unit cost (R36).
5. Build the launch budget: plan fee; research tool (source 01 cases: $40 to $595); design (Canva free to 99designs about $300 to $900); entity (DBA about $99; LLC $150 to $350 plus state fees); samples ($50 to $750); first run; freight; UPC ($30 GS1); trademark; photos ($50 to $100 render or real shoot); pre-launch marketing; PPC about $1,000 minimum; cushion. All figures are source 01's; replace with quotes.
6. Write the fee and margin model spec (9.3) and mark every line as brand data, quote, or `[web check]`.
Checks: sum of lines matches the calculator plus the added lines; no line is a course figure without a flag.
Rollback: none.

### P6. Amazon-specific sourcing steps (the rest is 18-COG)

Goal: a production run that arrives FBA-ready and inspected.
Preconditions: supplier shortlisted through 18-COG.
1. Ask each shortlisted supplier: MOQ, maximum monthly capacity, lead time, packaging options, whether they can print the FNSKU and any required warning labels on the packaging, whether they can palletise and accept a truck (R43, R47, R66).
2. Order the sample; pay for the printed or custom sample (R44). Approve against the brief from P4 step G.
3. Pay 30% upfront by a reversible method on early orders (R45, R46).
4. Before the balance: third-party inspection (about $100; Alibaba about $118 a day). Inspector checks unit quality against the approved sample and scans the FNSKU and UPC barcodes.
5. Choose freight by urgency and weight (R48): air 5 to 10 days; sea 4 to 6 weeks plus customs with a freight forwarder; budget the customs bond and duty. For a first shipment, ship to the brand first for a physical check when feasible, then forward to FBA.
6. Size the run against R90 and cash: a smaller first batch for an unproven SKU, 3 to 6 months of cover once velocity is known.
Checks: inspection report on file; barcodes scan; case pack matches the FBA limits in R62.
Rollback: hold the 70% balance until defects are fixed.

### P7. Keyword research for the listing `[verify UI]`

Goal: a keyword set in 3 buckets for title, bullets, description and backend.
1. Magnet: seed with the product terms; read monthly volumes; validate gaps live on Amazon (R32).
2. Cerebro on 2 to 3 competitor ASINs; note the phrases that drive their sales; note adjacent high-volume terms that are not targets (source 01's "card shuffler" at 26,000 a month for a card deck).
3. Mine adjacent listings outside the exact subcategory for attribute terms.
4. Bucket: core exact phrases; true supporting attributes; buzzwords to cut (R53).
5. Assign: bucket 1 to the first 2 words of the title and bullet 1; bucket 2 across title, bullets, description; leftovers to backend search terms.
Checks: every phrase in the listing is true of the product.

### P8. Build a new listing `[verify UI: Catalog, Add Products, Blank Form]`

Goal: a complete, compliant listing ready to go live on a set date.
Preconditions: P7 keyword set; real product photos; approved claims list; GS1 UPC; brand name as filed.
1. Catalog, Add Products, Blank Form, Start. (Source 01 notes a paste-your-Shopify-URL AI draft option `[web check: availability]`; treat any draft as a starting point and check every claim.)
2. Title: target phrase first, then true attributes, count and use case. Source 01's example: "Bourberine Tea, Supreme Herbal, Advanced Metabolic and Immune Support, Antioxidant Rich, All Natural Ingredients, 30 Tea Bags for Holistic Wellness" (note the buzzwords it kept; apply R53 harder than the example does).
3. Category: reject a too-generic auto-suggestion; browse to the specific node; copy a comparable competitor's node if unsure.
4. Variations: yes only if selling sizes, colours or flavours as one parent (R73).
5. Brand name: exactly as filed. Product ID: UPC from GS1.
6. Description: one benefit-led paragraph carrying bucket 1 and 2 keywords; no invented claims.
7. Bullets: 5, one at a time. Lead bullet 1 with the target phrase; benefits before features; one true specific claim each; optional guarantee bullet if it matches the current return policy.
8. Images: main image per R55 (real product, hero, high contrast, no clutter); up to 8 secondary including a comparison chart, use, scale, packaging, benefits text.
9. Attributes: manufacturer (brand is acceptable if a third party makes it); items per sellable unit; ingredients or materials; expireable (yes for consumables); shelf life in days; unit count and measure; form; a descriptive SKU (for example "brand-product-30ct").
10. Quantity (FBM only); condition New; price per R36; list price is a reference field, not the sell price.
11. Fulfilment: FBA; package level orderable: yes; cautionary statement if applicable.
12. All attributes: set the offer start date to the launch date; fill backend search terms with bucket 2 and 3 leftovers not already visible.
13. Save. Expect possible compliance flags (COA) and build buffer time (R60).
14. After Brand Registry: A+ content module set.
Checks: run the listing audit (5.4). A human presses publish.
Rollback: the future offer start date keeps the listing dark until ready.

### P9. Join an existing ASIN (only when the brand's product already has one) `[verify UI]`

Goal: the brand as the seller of its own product on an ASIN resellers created.
1. Catalog, Add Products, search the ASIN, condition New, Sell this product.
2. Set price, fulfilment FBA, and Amazon's barcode (FNSKU) so units are not commingled (source 02's rule, valid here too).
3. Enrol in Brand Registry (P3) to take control of the detail page and remove unauthorised edits.
Checks: offer appears in inventory within about 15 minutes (source 02).
Note: everything else in source 02's ASIN-joining procedure (price to the lowest FBA seller, ungating invoices) is reseller practice and does not apply.

### P10. FBA inbound shipment, US flow `[verify UI: Send to Amazon]`

Goal: stock checked in and sellable with no problems on the shipment.
Preconditions: units labelled with FNSKU at the factory or by the brand; measured case dimensions and weight; true ship-from address.
1. Inventory, Manage Inventory, Send/Replenish Inventory (switch the item to FBA first if the option is missing).
2. Ship-from: the true address of the origin (R65). Marketplace destination: the target marketplace. Fulfilment capability: standard FBA, or multi-channel if also shipping for the brand's own site.
3. Case-pack template: units per case, dimensions, weight; no side over 25 inches, case under 50 lb (R62). Prep category if fragile, liquid, adult, baby. Save the template (R63).
4. Labelling: "units already labelled" when the FNSKU is printed on packaging; otherwise print FNSKU labels from Seller Central; never "Amazon labels" (R47).
5. Enter case count. Answer dangerous-goods questions accurately (R70).
6. Shipping mode: small parcel through the partnered UPS rate for boxes; LTL for 1 or more pallets (get quotes at freightquote.com per source 01; confirm the manufacturer or warehouse can palletise and load a truck).
7. Print box labels (and pallet labels for LTL). Check each label: weight, dimensions, ship-from, ship-to; note that Amazon may split boxes across fulfilment centres (R64).
8. Hand over. Keep the carrier receipt and the Bill of Lading (R67).
9. Track: Manage FBA Shipments; statuses in transit, delivered, receiving, closed. Check the Contents tab for declared vs received and the Problems tab.
10. If received units are short past the normal window (R69), open a reimbursement case with the shipped-quantity proof.
Checks: run the inbound shipment check (5.5). A human confirms the shipment and accepts charges.
Rollback: source 02 says a confirmed shipment can be cancelled within about 24 hours without charge `[web check]`.

### P11. FBA inbound shipment, UK flow and UPS collection `[verify UI]`

Goal: same as P10 on amazon.co.uk.
1. Send to Amazon from the inventory offer. Ship-from address.
2. Prep: "No prep needed" default; bubble wrap for fragile. Labelling: by the brand (or Amazon at 38p per unit per source 02, avoid).
3. Units for this SKU; expiry date if applicable.
4. Print SKU labels on A4 self-adhesive sheets or thermal. For multipacks, poly bag and label the bag, not each unit.
5. Packing: boxes, each box's dimensions and weight; the tool rejects any side over 63.5 cm or weight over 23 kg.
6. Ship date; small parcel or pallet; carrier UPS (partnered; DPD also offered). Review the assigned fulfilment centre. Never drop off at a fulfilment centre.
7. Accept charges. Print box and carrier labels at the template size Seller Central specifies. Copy the tracking ID.
8. UPS schedule-a-pickup: prepaid label yes; tracking IDs comma separated; address; number of boxes; total weight; flag over 32 kg; choose a 4-hour window or a drop-off point. Confirm.
Checks: collection booked, not just a tracking number (R68).

### P12. Inventory breakdown and reimbursement check `[verify UI]`

Goal: know where every shipped unit is and claim what Amazon owes.
1. Manage All Inventory, SKU condition column, FBA Inventory Breakdown.
2. Read available; reserved split into FC transfer, FC processing, customer order. FC transfer is Amazon redistributing across centres; normal.
3. Timing (source 03, outside Q4): transit 3 to 4 days; check-in 1 to 2 weeks. Beyond 2 weeks, open a case. Q4: up to a month is normal.
4. Compare received to shipped on the shipment's Contents tab. File a claim with the BOL, receipt and packing list.
5. Monthly: audit fee lines and lost or damaged inventory (R41), with Refund Genie, SellerBoard or a manual check.

### P13. Launch plan

Goal: a dated launch that concentrates genuine demand into the first weeks without any policy risk.
Preconditions: listing built (P8) with a future offer start date; stock checked in; Brand Registry filed; PPC campaigns drafted (P14); audience assets known.
1. 6 to 8 weeks out: post the development story on the brand's channels; open an email waitlist; open a small pre-launch group for feedback (R72). Seed product to 5,000 to 10,000 follower creators for honest posts, with no review ask and no reimbursement (R85).
2. 2 weeks out: confirm stock is sellable; set launch price (introductory discount through Amazon's own coupon or promotion tools only); load A+ if available.
3. Launch day: flip the offer start date; send the waitlist email with the Attribution link (R21); post; start the automatic PPC campaign; consider Amazon Live if the brand has a presenter.
4. Days 1 to 14: request reviews through Amazon's button on eligible orders; do not gate or select; watch sessions, unit session percentage, PPC search terms daily.
5. Weeks 3 to 6: build manual campaigns from converting terms (P14 B); reorder if velocity beats forecast (R91); raise price as a throttle only if stock will run out before the next delivery (R75, human decision).
6. Month 3 onward: test lowering PPC where organic holds (R82); repeat review mining on the brand's own listing.
Checks: launch readiness checklist (5.6) passes; nothing in the plan pays for, gates or recruits reviews.

### P14. PPC setup `[verify UI: Advertising, Campaign Manager, Sponsored Products]`

Goal: an automatic campaign split by targeting group, then manual keyword and product targeting campaigns with negatives.
A. Automatic campaign (source 01):
1. Create campaign, Sponsored Products, automatic targeting, daily budget from the PPC budget (R42), dynamic bids down only at launch, or up and down if the margin allows up to +100% on a bid.
2. Create 4 ad groups, one per targeting group: close match, loose match, substitutes, complements. Set a separate bid per group from Amazon's suggested range (source 01's example: $0.92, $0.72, $0.13, $0.71; not benchmarks).
3. Add negative keywords from the start for wrong formats, sizes, uses (R81).
B. Manual keyword campaign (after automatic data):
1. Pull the search term report; keep terms with orders.
2. Add Magnet candidates filtered per source 01: under 5,000 monthly searches, 2 words minimum, 100 competing products maximum, 2 keyword sales a month minimum (presenter's demo filters).
3. Ad groups by match type: exact for proven converters; phrase and broad for discovery, each with negatives.
C. Product targeting: one campaign, one ad group per competitor brand, ASINs with weaker listings or higher prices (R80).
D. Negatives: on every campaign, weekly (P15).
Checks: the PPC structure (9.6) is documented with bids, budgets and negatives; a human creates the campaigns and sets the budgets.
Rollback: pause, do not delete, so history stays readable.

### P15. PPC weekly review

Goal: keep PPC on net profit.
1. Pull search term reports for all campaigns. Add negatives for terms with spend and no orders past a spend threshold the brand sets `[needs brand data: threshold]` (the sources give none).
2. Move converting automatic terms to exact match; lower or pause bids on terms with high spend and no orders.
3. Read ACOS per ad group against the margin from P5; the sources give no target ACOS; the gate is net profit after PPC.
4. Check budget pacing and bid changes from dynamic bidding.
5. Check that the listing is still advertising-eligible (R83).
6. Once organic share is meaningful, test a lower PPC budget for a period and compare net profit (R82).
Checks: PPC weekly review checklist (5.7). A human applies bid and budget changes.

### P16. Monthly P&L, fee audit and report

Goal: the monthly Amazon report (9.7).
1. Pull revenue, units, sessions, unit session percentage, PPC spend and orders, returns, storage age, stock cover.
2. Build the P&L by fee line (R40) from settlement data, not estimates.
3. Reconcile fees against expected (P5); claim errors (R41).
4. Flag: stockout days, inventory past 150 days (ahead of any long-term threshold), account health notices, hijackers, review rating drift.
5. State what needs a human: price, budget, removal orders, reorders.

### P17. Replenishment planning

Goal: no stockout and no long-term storage.
1. Weekly: units per week trailing 4 weeks; units on hand and inbound; days of supply (the Restock Inventory widget gives days of supply and a suggested quantity, source 01).
2. Reorder trigger: remaining cover at 2 to 3 months plus the full lead time (manufacture plus freight plus 3 to 6 weeks check-in; longer in Q4).
3. Order size: 3 to 6 months of cover for a proven SKU; a smaller batch for a new one (R90); drip larger runs into FBA in tranches (source 01's Cam case).
4. Watch inventory age against the live long-term threshold `[web check]`; remove or sell through before it.
5. Q4: order earlier, expect about 3x demand (presenter claim), and the higher storage rate.

## 5. Diagnostic checklists

Written so a worker can run them. Columns: what to check | how | good | bad | fix | source.

### 5.1 Channel fit check

| What | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Category restricted, gated or patent risk | Amazon restricted list `[web check]`; patent search | Open category, no patent | Restricted, gated, patented | Stop, or get approval first | 01p1, 04 |
| Trademark plan | Brand record | Filed or filing now | None | File before listing (P3) | 01p1, 01p3 |
| Price floor | Brand price | $25 or more | Under $15 | Reposition or do not launch | 01p1, 04 |
| Net margin after all fees | P5 model | 30% or more | Under 30% | Cut landed cost, raise price, change packaging tier, or stop | 01p3, 04 |
| Cash for 3 months of stock plus about $1,000 PPC | Brand cash | Yes | No | Smaller revenue band, smaller first batch, or wait | 01p3, 04 |
| Product differentiated | Review mining, price disparity | Clear fixable gap or unique product | Generic clone in a tight price cluster | Change product or positioning | 01p1, 04 |
| Prior seller accounts | Ask the user | None, or disclosed | Undisclosed old or suspended account | Disclose to Amazon before signup | 01p1, 02 |
| Marketplace VAT and tax | Brand record | Known and modelled | Unknown | Route to 20-FIN | 02 |
| Fulfilment fit | Product weight, fragility | Standard size tier, FBA | Oversize, fragile, made-to-order | Model FBM or a mix (R2) | 02, 01p3 |

### 5.2 Product research screen

| What | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Elimination groups | R23 list | None apply | Cheap, seasonal, restricted, head-on competitive | Discard | 04, 01p1 |
| Price band | Page-1 prices | $25 to $85 | Under $15 or cluster under $10 | Discard or reposition | 01p1, 04 |
| Page-1 price spread | Record 10 prices | Wide (for example $20 and $100) | Tight (for example $7 to $13) | Discard | 01p1, 04 |
| Brand dominance | Top sellers by brand | Sales spread across many sellers | 1 or 2 legacy brands own it | Discard | 01p1, 04 |
| Review counts of top 10 | Page 1 | Several under 300 | All in the thousands | Discard or find a sub-niche | 04 |
| Listing age of comparables | Black Box | 8+ months | Under 8 months | Treat as fad risk | 04 |
| Keyword variability | List phrasings | Dozens | 1 or 2 | Deprioritise | 04 |
| Keyword gap | Magnet title density 0, live search | Volume with no matching listing | Every phrase already served | Differentiate harder | 01p1 |
| Revenue band vs cash | Black Box revenue | $5,000 to $20,000 a month (or $1,500 to $3,000 on a small budget) | $30,000+ with no capital | Pick a smaller band | 04 |
| Review mining | 1-star reviews of 4.1 to 4.3 star sellers | Recurring fixable complaints | Complaints are misuse | Write fixes into the brief | 04, 01p1 |
| Giftability | Occasion list | Several occasions plus self-purchase | Single season only | Tie-breaker only | 04 |
| Q4 exposure | Seasonality | Evergreen with a Q4 lift | Pure seasonal | Avoid as a first product | 01p1 |

### 5.3 Unit economics gate

| What | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Referral fee | Live category rate `[web check]` | Modelled at the real rate | Assumed flat 15% | Use the category table | 01p1, 01p3 |
| FBA fee | Calculator on a comparable | Size tier confirmed | Guessed | Measure packed unit | 01p3 |
| Storage | Cubic feet x rate x months, Q4 rate | Included | Missing | Add (R38) | 01p3 |
| Long-term storage risk | Months of cover vs live threshold `[web check]` | Cover under the threshold | Cover over it | Smaller batches | 01p3 |
| VAT on fees | Marketplace rule | Added where it applies | Missing | Add (R16) | 02 |
| Inbound freight, duty, bond, inspection | Quotes | Per unit lines | Missing | Add | 01p2 |
| Labelling and prep | Factory prints FNSKU | $0 | Amazon labels at $0.30 to $0.50 (38p UK) | Print at factory | 01p2, 01p3, 02 |
| Returns and disposal | Category return rate `[needs brand data]` | Allowance included | Missing | Add | 01p3 |
| PPC per unit | CPC, conversion, margin | Included | Missing | Add (R42) | 01p3 |
| Price vs cost | Price / unit cost | 3x or more | Under 3x | Raise price or cut cost | 01p2 |
| Net margin | Full stack | 30% or more | Under 30% | Do not launch as is | 01p3, 04 |
| Launch budget | Line items | Every line a quote or brand figure | Headline number | Rebuild (P5 step 5) | 01p3 |

### 5.4 Listing audit

| What | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Title | First 2 words | Target phrase first | Brand or buzzword first | Rewrite | 01p2, 01p3 |
| Title buzzwords | Bucket test | Only bucket 1 and 2 terms | "wellness", "detox", "premium" filler | Cut | 01p2 |
| Bullet 1 | First words | Target phrase, then benefit | Feature list | Rewrite | 01p2 |
| Bullets 2 to 5 | Read each | Benefit, one true specific claim | Vague or invented claims | Rewrite; remove any claim not on the approved list | 01p2, ecomOS |
| Description | Read | Benefit paragraph with keywords | Keyword stuffing or empty | Rewrite | 01p2 |
| Main image | View on the search grid at thumbnail size | Product hero, high contrast, reads at small size | Packaging or logo dominates, low contrast, generated redraw | Reshoot with the real product | 01p2, 01p3 |
| Secondary images | Count and content | Up to 8, comparison chart, use, scale | 4 or fewer, DIY look | Add | 01p2, 01p3, 04 |
| Attributes | Field by field | Category node specific; expireable and shelf life correct; units per sellable unit correct | Generic node; blanks | Fix | 01p2 |
| Backend keywords | All attributes | Filled with unused true terms | Empty or duplicates | Fill | 01p2 |
| Offer start date | All attributes | Set to launch day | Live to zero demand | Set | 01p2 |
| Brand name and UPC | Compare to filing and GS1 | Exact match | Mismatch or reseller UPC | Fix | 01p2 |
| Compliance | Category triggers | Documents ready (COA and so on) | Flag pending | Build buffer | 01p3 |
| A+ content | Brand Registry | Present | Missing | Add after enrolment | 01p2 |
| Index and analysis | Helium 10 Index Checker, Listing Analyzer | Indexed for core phrases | Not indexed | Fix keywords | 01p2 |

### 5.5 Inbound shipment check

| What | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Ship-from address | Read | True origin | Any false address | Correct (R65) | 01p2 |
| Case size and weight | Measure | Under 25 in per side and 50 lb (US); under 63.5 cm and 23 kg (UK) `[web check]` | Over | Repack or split | 01p2, 02 |
| FNSKU | Scan a unit | Scans, applied at factory or by the brand | Missing, unscannable, "Amazon labels" chosen | Relabel; never Amazon | 01p2, 03, 02 |
| Prep | Category rules | Poly bag, bubble wrap, multipack bag labelled | Missing | Prep | 02, 01p2 |
| Dangerous goods answers | Questionnaire | Accurate | Guessed | Correct | 01p1 |
| Box labels | Compare to carrier label | Weight, dimensions, ship-from and ship-to match; split shipments noted | Mismatch | Reprint | 01p2 |
| Shipping mode | Volume | Small parcel for boxes; LTL for pallets | Repeated small parcel for pallet volume | Switch | 01p2 |
| Carrier booked | Tracking and pickup | Collection booked or drop-off done | Tracking number only | Book (R68) | 02 |
| Paperwork | File | Receipt and BOL kept | Missing | Keep before handover | 01p2 |
| Status | Manage FBA Shipments | In transit to closed with no Problems | Problems tab items; short receipt | Resolve; claim with proof | 01p2, 03 |
| Timing | Inventory breakdown | Check-in within 1 to 2 weeks (up to 1 month Q4) | Past 2 weeks outside Q4 | Open a case | 03 |
| Cover sent | Units vs velocity | 3 to 6 months (smaller for a new SKU) | 100% of a large run to FBA at once | Drip in tranches | 01p2, 01p3 |

### 5.6 Launch readiness

| What | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Stock sellable | Inventory | Available units at FBA | In transit or receiving | Hold the launch date | 01p2 |
| Listing audit | 5.4 | Passed | Open items | Fix first | 01p2 |
| Offer start date | Attributes | Launch day | Already live | Coordinate the push | 01p2 |
| Brand Registry | Status | Filed or active | Not filed | File; launch can proceed | 01p2 |
| Audience assets | Waitlist size, group, seeded creators | Ready with tracked links | None | Build (R72) or accept a slower ramp | 01p2, 01p3 |
| PPC drafted | P14 | Automatic campaign in 4 ad groups with negatives | Blended bid, no negatives | Fix | 01p2 |
| Review plan | Read it | Amazon request button only; Vine only if ready | Any incentive, gating, recruiting | Remove (R85) | 01p2, ecomOS |
| Reorder trigger set | P17 | Dates and quantities | None | Set | 01p2, 01p3 |
| Compliance | Flags | Cleared | Pending COA or ad ineligibility | Resolve or buffer | 01p3 |
| Human owners | Names | Publish, shipment, price, budget each have a named person | Agent-only | Assign | ecomOS |

### 5.7 PPC weekly review

| What | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Search terms with spend and no orders | Search term report | Negated past the brand's spend threshold | Still spending | Add negatives | 01p2 |
| Converting automatic terms | Report | Moved to exact match | Left in automatic only | Move | 01p2 |
| Targeting group bids | 4 ad groups | Separate bids, adjusted to results | One bid | Split | 01p2 |
| ACOS vs margin | Ad group level | Net profit after PPC positive | Negative for weeks | Lower bids or pause the group | 01p3 |
| Product targeting | Per competitor ad group | Profitable groups kept | Losing groups still live | Pause | 01p2 |
| Budget pacing | Campaign | Runs the day | Out by noon or unspent | Adjust (human) | 01p2 |
| Eligibility | Campaign status | Serving | Ineligible flag | Diagnose (R83) | 01p3 |
| Organic vs paid share | Business Reports vs ad orders | Organic growing | PPC-dependent | Test a lower budget (R82) | 01p3 |
| Off-Amazon attribution | Attribution links | Tracked | Untracked | Fix (R96) | 01p3 |

### 5.8 Policy compliance audit

| What | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Review practices | Read every launch and CRM step | Amazon request path only; no incentives, gating, recruiting, refund links | Any of these | Remove; document | 01p2, 01p3, ecomOS |
| Vine use | Terms | Current terms, product ready | Seeding non-target reviewers | Stop | 01p3 |
| Seller feedback handling | Feedback Manager | Misplaced product reviews contested within 30 days; no benefit offered | Refund alluded to | Stop | 01p1 |
| Ship-from address | Shipments | True | False | Correct | 01p2 |
| Accounts | Ask | 1 account, prior ones disclosed | Duplicate | Disclose | 01p1 |
| Barcodes | GS1 record | GS1 | Reseller codes | Replace | 01p1, 01p3 |
| Claims | Listing and A+ | Approved list only | Unapproved health or performance claims | Remove | ecomOS |
| Restricted categories | Live list `[web check]` | Approved or not applicable | Selling without approval | Stop | 01p1 |
| Account Health | Performance page | ODR, claims, chargebacks within Amazon's limits | Warnings | Act on each notice | 01p2 |
| Hijackers | Brand Registry, Alerts | None | Unknown sellers on the ASIN | Brand Registry case; Transparency | 01p2 |
| Human sign-off | Log | Every account write has a named person | Agent wrote to the account | Stop; fix the process | ecomOS |

## 6. Thresholds and benchmarks

One table for the folder. Confidence: how many sources agree. "Presenter heuristic" marks a number that is one creator's rule of thumb, not a published Amazon figure. Every fee and limit needs a `[web check]` before use.

| Item | Value | Condition | Source | Confidence |
|---|---|---|---|---|
| Professional plan (US) | $39.99 a month | Any volume | 01p1, 01p3, 03 | 3 sources agree; dated `[web check]` |
| Individual plan (US) | $0.99 per item | Low volume | 01p1, 03 | 2 agree; dated |
| Plan breakeven | About 40 to 41 units a month | Choosing plan | 01p1, 03 | 2 agree; presenter heuristic |
| Professional plan (UK) | £25 + VAT a month | UK | 02 | 1 source; dated |
| Individual plan (UK) | 75p + VAT per unit | UK | 02 | 1 source; dated |
| Verification turnaround | Up to 72 hours (UK); up to 48 hours added per mismatch (US) | Signup | 02, 01p1 | 1 each; presenter experience |
| Referral fee | 15% (source simplification; varies by category) | All sales | 01p1, 01p2, 01p3 | 1 source repeated; `[web check]` |
| FBA pick and pack, small standard | About $2.16 to $2.70 per unit | Small standard tier | 01p3 | 1 source; dated |
| FBA pick and pack, large standard | Examples $4.25 and $4.95 per unit | Large standard tier | 01p3 | 1 source; dated |
| Apparel surcharge | About $0.30 to $0.40 per unit | Apparel | 01p3 | 1 source; dated |
| Monthly storage | $0.70 or $0.75 per cubic foot Jan to Sep; $2.40 Oct to Dec | Standard size | 01p3 | 1 source, 2 figures; dated |
| Long-term storage fee | $6 to $6.90 per cubic foot or $0.15 per item, whichever is greater | Aged inventory | 01p3 | 1 source; dated |
| Long-term storage threshold | 365 days, 180 days, or "beyond 6 months" | Aged inventory | 01p3 presenter, 01p3 Cam, 01p2 | Conflict inside 1 source; `[web check]` critical |
| Amazon labelling fee | $0.50 per unit (01p2), $0.30 (01p3), 38p (02) | If Amazon applies FNSKU | 01p2, 01p3, 02 | Conflict; avoid the fee anyway |
| Prep services | About $0.50 to $2.00 per unit | If Amazon preps | 01p3 | 1 source; dated |
| Disposal fee | About $0.50 per unit | Returned unit disposed | 01p3 | 1 source; dated |
| Individual plan closing fee | $0.88 (example) | Individual plan only | 01p1 | 1 example |
| UK VAT on fees | 20% on selling and fulfilment fees | UK sellers | 02 | 1 source; `[web check]` |
| Duty from China to US | About 10 to 20% | By category | 01p2 | 1 source; `[web check: HS code]` |
| Customs bond | About $100 single; about $400 annual | Sea import | 01p2 | 1 source; dated |
| Sea freight | About $2 per kg; 4 to 6 weeks; about a third of air | Non-urgent | 01p1, 01p2, 01p3 | 1 source repeated |
| Air freight | 5 to 10 days; materially more | Urgent or first shipment | 01p1, 01p2 | 1 source |
| Inspection | About $100 third party; about $118 a day Alibaba | Before balance | 01p2 | 1 source; dated |
| Payment split | 30% upfront, 70% after inspection | Wire to a new supplier | 01p2 | 1 source; presenter practice |
| Sample cost | $25 to $45 shipping; $200 to $300 custom printed | Before a run | 01p2 | 1 source |
| GS1 UPC | About $30 single; 10-pack about $250 historically; $20 to $250 across cases | New ASIN | 01p1, 01p2, 01p3 | 1 source, inconsistent; `[web check]` |
| Trademark DIY fee | $250, $275, $225 to 275 | USPTO self filing | 01p1, 01p2, 01p3 | Conflict inside 1 source; `[web check]` |
| Trademark approval time | 6 to 18 months | After filing | 01p1 | 1 source |
| Provisional patent | About $75 | Novel product | 01p2, 01p3 | 1 source; `[web check]` |
| Utility patent | About $1,090 DIY fees; about $10,000 with a lawyer | Novel product | 01p2, 01p3 | 1 source; `[web check]` |
| Vine without Brand Registry | About $200 | Non-registered | 01p2 | 1 source; `[web check]` |
| Brand Registry new-seller incentive | 5% of the first $1 million | New brands | 01p2 | 1 source; `[web check]` |
| Brand Referral Bonus | "About 10% back" or "15% to 5%" | External traffic | 01p2, 01p3 | Conflict; `[web check]` |
| Price band | $15 to $85, sweet spot $25 to $30 | New launch | 01p1 | Presenter heuristic |
| Price floor | $25+; discard under about $10 | New launch | 04 | Presenter heuristic |
| Net margin gate | 30% or more after landed cost and fees | Go or no-go | 01p3, 04 | 2 agree; presenter heuristics |
| Price to cost | 3x or more | Pricing | 01p2 | Presenter heuristic |
| Fee share of price | About a third; 20 to 25% for pricier light items | Estimate | 01p2 | Presenter heuristic |
| Black Box (04) | Reviews max 300; price $25 to $60; revenue $5,000 to $20,000; age 8+ months; images max 4 | First pass | 04 | Presenter heuristic; do not copy verbatim |
| Black Box (01) | Price $15 to $85; revenue $5,000 to $80,000; max rating 3.5 | First pass | 01p1 | Presenter heuristic |
| Review-mining band | 4.1 to 4.3 stars and $5,000+ a month | Shortlist | 04 | Presenter heuristic |
| Small-budget revenue band | $1,500 to $3,000 a month still viable | Limited cash | 04 | Presenter opinion |
| $30,000 a month product | Needs about 3 months of inventory plus heavy ads | Capital check | 04 | Presenter heuristic |
| Cheap product PPC trap | About $1 per click erases profit in 2 to 3 clicks on an $8 item | Under $10 | 04 | Presenter reasoning |
| Magnet PPC keyword filter | Under 5,000 searches; 2+ words; 100 or fewer competing products; 2+ keyword sales a month | Manual campaign mining | 01p2 | Presenter demo settings |
| Automatic bids example | Close $0.92; loose $0.72; substitutes $0.13; complements $0.71 | One product | 01p2 | Example only |
| Dynamic bid range | Up to +100% | Up and down strategy | 01p2 | Amazon mechanic; `[verify UI]` |
| Launch PPC reserve | About $1,000 | Launch budget | 01p3 | Presenter heuristic |
| Startup budget | Floor about $3,500; recommended about $5,000 plus $1,000 PPC; cases $5,800 to $26,524 | Private label launch | 01p3 | Presenter figures |
| Private label capital (UK) | About £5,000 to £10,000 | UK | 02 | Presenter figure |
| First run cover | 3 to 6 months; reorder at 2 to 3 months left | Replenishment | 01p2, 01p3 | 1 source repeated; conflict 2 |
| Replenishment lead time | 3 to 6 weeks ship to sellable; longer in Q4 | FBA inbound | 01p2 | 1 source |
| Check-in timing | Transit 3 to 4 days; check-in 1 to 2 weeks; escalate past 2 weeks; up to 1 month in Q4 | FBA inbound | 03 | 1 source; presenter experience |
| Case limits (US) | No side over 25 in; under 50 lb | Case pack | 01p2 | 1 source; `[web check]` |
| Box limits (UK) | No side over 63.5 cm; under 23 kg | Shipping plan | 02 | 1 source; `[web check]` |
| UPS pickup weight flag (UK) | Over 32 kg | Pickup form | 02 | 1 source |
| Shipment cancel window | About 24 hours | After accepting charges | 02 | 1 source; `[web check]` |
| Q4 demand | About 3x normal | Q4 planning | 01p1 | Presenter claim |
| Influencer seeding size | 5,000 to 10,000 followers; 85 boxes in one launch | Free-product collaborations | 01p2 | Presenter practice |
| Launch reviews | About 75 in week 1 (presenter's best) | Example | 01p3 | Example only |
| Seller feedback contest window | 30 days | Misplaced product review | 01p1 | 1 source; `[web check]` |
| Trend lead time | About 2 months manufacture and ship | Why avoid fads | 01p1 | Presenter reasoning |
| Repricing tool threshold | About 25 listings | Reseller context; not a private label rule | 03 | Out of scope |
| BSR under 100,000; 4+ sellers; ROI 30% | Reseller screen | Wholesale or arbitrage only | 02 | Out of scope |

## 7. Where sources disagree

Each conflict: what each side says, when each is right, what the agent should do.

**Conflict 1. Private label and own product vs arbitrage and wholesale.**
- Source 01p1 teaches retail and online arbitrage as a low-capital start (Seller app scanning, 90-day median price, Buy Box on price about 90% of the time, min and max repricing). Source 02 teaches wholesale and arbitrage (BSR under 100,000, 4+ sellers, Amazon not on the Buy Box, 30% ROI, 10 to 50 unit test orders, ungating with invoices) and says beginners should start there before private label. Source 03 is entirely arbitrage (ungating per brand, SellerAmp and Keepa, removing price tags, prep centres in tax-free states, repricers past 25 listings). Source 01p3 and 04 argue for a differentiated own product; source 01 calls generic private label "outdated".
- When each is right: arbitrage and wholesale are a way for an individual to learn the platform with little capital. They do not apply to a brand that owns its product: no Buy Box contest, no ungating for the brand's own ASINs, no hiding of acquisition price, different economics and failure modes. Source 02's and 03's own curation headers say the content should be skipped or discarded.
- What the agent should do: treat arbitrage and wholesale as out of scope for ecomOS brands. Do not use BSR under 100,000, 4+ sellers, 30% ROI, test-order sizes, ungating invoices, repricer thresholds or price-tag removal in any rule or deliverable. Keep only the model-agnostic mechanics from 02 and 03 (document set, UK VAT on fees, box limits, carrier pickup, inventory breakdown statuses, escalation timing), each marked with its source. If a user asks about arbitrage, say it is out of scope and point to the wall-off here.

**Conflict 2. Under-ordering inventory vs cash risk (and how much to send to FBA).**
- Source 01 says under-ordering is its most expensive recurring mistake (Brent, Cam, AJ, Calvin, and the presenter himself), recommends 3 to 6 months of cover per run "closer to 6" for anything perishable or seasonal, and warns that a stockout can drop rank and, in the presenter's telling, flag the account. The same source's Cam prong collar case shipped 100% of a large order to FBA before validating sell-through and paid long-term storage plus $1,300 to remove stock (card dd7da61297). Source 02 (reseller) says test 10 to 50 units first. Source 04 says match the revenue band to cash and that a $30,000 a month product needs 3 months of stock plus heavy ads. Source 01's own cards say 3 to 6 months is a scenario, not a default order size.
- When each is right: 3 to 6 months of cover fits a product with a demand signal (existing comparable sales, a proven first batch, a waitlist that converted). A smaller first batch, dripped into FBA, fits a new, unvalidated product or a cash-constrained brand. MOQ can make a small first batch impossible.
- What the agent should do: for a new SKU, recommend the smallest run the MOQ allows that still covers the launch window plus one reorder lead time, sent to FBA in tranches; once velocity is known, move to 3 to 6 months of cover and reorder at 2 to 3 months remaining. Always show the stockout cost and the storage cost side by side on brand numbers. Never let a stockout fear push cash past what the brand has said it can lose.

**Conflict 3. Review-generation tactics vs policy.**
- Source 01 describes, while flagging them as against ToS and "gray hat": reimbursing friends, family and strangers by Venmo or PayPal for a purchase and a 5-star review; a "never share Wi-Fi" workaround; "alluding to" a refund to get seller feedback pulled; and says bans "almost never" follow. Source 01's own card `[eec0cf391ebf]` says the opposite: use only Amazon's permitted request path, never reimburse or gift for reviews, never recruit friends, family or associates, and using different accounts or networks does not make it acceptable. Source 03's SellerBoard sends automated review-request emails about 5 days after delivery.
- When each is right: never for the tactic. The card is right. Amazon's request-a-review button and Vine under current terms are the only paths in any source that are compliant.
- What the agent should do: follow the card and the ecomOS rule. Remove any incentive, gating, selection of happy buyers, recruiting of known people, or refund-for-removal from any plan. Use Vine only when the product is ready and the brand accepts the rating risk (Connor's case). Log the rejected tactic and why in the launch plan so nobody reintroduces it.

**Conflict 4. Gray-area ship-from address.**
- Source 01p2 describes entering a California ship-from address on an inbound plan when importing from China to bias fulfilment-centre assignment to the West Coast and cut inbound freight, calls it "technically against Amazon's rules", says most sellers he knows do it, and says "do this at your own risk". No card in the source supports it. The same source's presenter says a wrong ship-from address once cost him about $5,000 in lost sales.
- When each is right: never for the false address. Legitimate ways to reduce inbound distance exist (a real West Coast freight forwarder or 3PL as the true ship-from) and are 18-COG questions.
- What the agent should do: always use the true origin address. If inbound cost matters, model a real forwarder or prep centre on the coast as the ship-from and route the sourcing question to 18-COG.

**Conflict 5. Conflicting fee and cost figures between and inside sources.**
- Long-term storage threshold: 365 days (01p3 presenter; card de97ba8ee8), 180 days (01p3 Cam; cards dd7da61297 and e62d78f3c8), "beyond 6 months" (01p2; card 24ca880132). Materially different for planning.
- Monthly storage rate: $0.70 vs $0.75 per cubic foot January to September (01p3, same part).
- Amazon labelling fee: $0.50 per unit (01p2; card a5c9b2ba33), $0.30 (01p3; card 996e5b8cd1), 38p (02).
- Trademark DIY fee: $250 (01p1, 01p2), $275 (01p2 later), $225 to 275 (01p3); LegalZoom $650 (Calvin); Trademarkia used for US plus Canada (Daryl and Amanda).
- UPC: $30 single GS1; $70 for 7 from a reseller; $250 for a 10-pack; $20 to $250 across cases; one case used "UPCs.com".
- Brand Referral Bonus: "15% falls to 5%" vs "about 10% back" (01p2 and 01p3).
- Small parcel example: 9 cases, 336 lb, "$26.62" in the 01p2 mini playbook vs "about $266" in its card 3232a9886a40; the $336 figure is weight, not cost.
- Referral fee: flat 15% throughout source 01; Amazon's rate varies by category.
- Case study P&Ls: Cam leash month 1 ($173 revenue vs $186 profit); Brent year 1 ("almost three quarters of a million" vs a cost breakdown summing near $340,000); AJ's viral day ($37,000 vs $22,000); Cynthia's manufacturer mistake ($2,300 vs about $7,800); the presenter's keto product year 1 ($300,000 to $360,000).
- Helium 10 cost: $40 to $595 across cases.
- What the agent should do: never average. Quote the range with both figures and the source, then replace with a live figure `[web check]` before any deliverable. For the long-term storage window, plan to the shortest stated (180 days) until the live figure is confirmed, because that is the conservative side for inventory sizing. For case study P&Ls, use only the direction of the story, never the exact number, and mark it "example, self-reported, inconsistent".

**Conflict 6. Credit card vs debit card at signup.**
- Source 01p1 says use a credit card and claims a debit or prepaid card triggers suspension. Source 03 says a debit card worked even though the page implied credit only.
- What the agent should do: use a business credit card (strictest, and it separates spend). Do not repeat the suspension claim as fact `[web check]`.

**Conflict 7. Air vs sea for the first shipment.**
- Source 01p2 recommends air for a first shipment (5 to 10 days, lower customs risk for a first-time importer). Source 01p1's AJ calls full air "throwing money down the drain" when not urgent and split the order half air, half sea (air portion about $4,200; landed cost about $11 air vs $7.50 sea). Source 01p3 says choose by urgency and weight and that Daryl and Amanda lost about $1,700 on a rushed forwarder choice.
- When each is right: air when the launch date is fixed, the order is small and light, or the brand has never imported; sea when volume and weight are high and the launch can wait 6 to 8 weeks; a split when part of the order is urgent.
- What the agent should do: model both on the brand's weight and volume, show landed cost per unit and days, and let the launch date decide. Route forwarder selection to 18-COG.

**Conflict 8. Price floor: $15 vs $25.**
- Source 01 gives $15 to $85 with a sweet spot of $25 to $30 and calls $15 the firmer floor; its cases include a success under $15 (Troy, Small and Light) and one over $85 (Brent). Source 04 says about $25+ and discards under about $10.
- What the agent should do: target $25 or more for a new launch; treat $15 to $25 as needing a strong reason (very low FBA fee tier, high repeat rate) and a margin model that still clears 30%; discard under $10.

**Conflict 9. Two Black Box recipes.**
- Source 01: price $15 to $85, revenue $5,000 to $80,000, max average rating 3.5 (finds high sellers with bad reviews). Source 04: price $25 to $60, revenue $5,000 to $20,000, review count max 300, listing age 8+ months, image count max 4 (finds weak competitors). Both presenters call their values heuristics; source 04 says not to copy his.
- What the agent should do: run both as separate passes, label the recipe on each result, and pass a candidate only if the manual checks (price disparity, brand dominance, keyword variability, review mining) also pass.

**Conflict 10. FBA sales multiplier.**
- Source 01 claims 4 to 5x sales from FBA over FBM on its own and students' products. Its card `[e94ff8c9c6e7]` says compare actual costs and test conversion; Seller Fulfilled Prime may exist for qualifying merchants. Source 02 gives FBM exceptions.
- What the agent should do: default to FBA for standard-size goods but model both and never quote a multiplier.

**Conflict 11. When to form an LLC.**
- Source 01 recommends an LLC (with S-corp election) before selling; source 01p3 says skip it unless real lawsuit risk exists; source 03 formed hers in month 6 after $10,000 a month.
- What the agent should do: route to 20-FIN; none of the sources is legal or tax advice.

**Conflict 12. Individual plan and the Buy Box.**
- Source 03 says the Individual plan cannot win the Buy Box. No other source says this, and for a single-seller own-brand listing the Buy Box contest does not apply in the same way.
- What the agent should do: choose the plan on volume (R8) and check the live plan feature list `[web check]`.

**Conflict 13. Launch loud vs launch quiet.**
- Source 01 says launch with an audience and fast reviews (Leanne and Logan were copied after a quiet launch). Source 01's Cam collar case could not advertise at all and failed. The sources give no evidence that a loud launch prevents copying, only the presenter's opinion.
- What the agent should do: build the audience where the brand has assets; do not promise that velocity blocks copycats; protect with Brand Registry, Transparency and, where the product is novel, IP.

**Conflict 14. PPC always on vs turn it off.**
- Source 01's card `[4e2dab02af]` calls PPC the fuel for a new listing; its Carnivore Electrolytes case turned PPC off in month 6 and profit rose; Cynthia's overspend drove her loss.
- What the agent should do: PPC on at launch; from month 3, test budget reductions against net profit; never run untracked.

## 8. Common mistakes

Merged from all sources, deduplicated, with the fix.

| Mistake | Fix | Sources |
|---|---|---|
| Waiting months or years to launch once screens pass | Set a launch date at the go decision; a decent supplier now beats a perfect one later (R6) | 01p1, 01p3 |
| Choosing a generic private-label clone | Differentiate from review mining; solve a named problem (R7, R30) | 01p1, 01p3, 04 |
| Not knowing landed cost, fees and margin | Run P5 on brand data before any order (R35, R37) | 04, 01p1 |
| Selling cheap ($7 to $10) products | $25+ target; $15 minimum (R24) | 04, 01p1 |
| Seasonal, trend or restricted products as a first launch | Elimination screen (R23) | 01p1, 04 |
| Copying a presenter's filter recipe | Vary category and values; rely on manual checks (R31) | 04 |
| Chasing the biggest revenue number without the cash | Match band to cash (R5) | 04 |
| Duplicate seller account | Disclose (R9) | 01p1, 02 |
| Name on account not matching ID | Match exactly (R10) | 02 |
| Changing bank or address right after approval | Do it before signup (R12) | 01p1 |
| Gray-market UPCs | GS1 (R15) | 01p1, 01p3 |
| Rushed word mark denied, forcing a rebrand | Design mark or distinctive name; check odds first (R18) | 01p3 |
| Missing the 20% VAT on fees (UK) | Add it (R16) | 02 |
| Asking MOQ but not capacity | Ask both (R43) | 01p2 |
| Trusting the sample for the bulk run | Inspect before the balance (R45) | 01p2 |
| Skipping the paid printed sample | Pay for it (R44) | 01p2 |
| Wiring 100% upfront | 30/70 and reversible methods early (R45, R46) | 01p2 |
| Cheapest manufacturer, disorganised | Weigh reliability; 18-COG | 01p2 |
| Middleman posing as a factory; labour abuse | Audit or agent visit; 18-COG | 01p3 |
| Full air by default, or sea when the date is fixed | Model both (R48, conflict 7) | 01p1, 01p2, 01p3 |
| Too many SKUs or colours at launch | One SKU unless the category requires variants (R73) | 01p1, 01p3 |
| Under-ordering; stockouts | Reorder at 2 to 3 months of cover; rush when velocity rises (R90, R91) | 01p1, 01p2, 01p3 |
| Shipping 100% of a big run to FBA before validation | Drip in tranches (R90) | 01p3 |
| Letting Amazon apply FNSKU labels | Print at the factory (R47) | 01p2, 01p3, 02 |
| Wrong ship-from address, or a false one | True address, checked (R64, R65) | 01p2 |
| Losing the BOL or receipt | File before handover (R67) | 01p2 |
| Treating a tracking number as a finished shipment | Book the collection (R68) | 02 |
| Reading FC transfer as a lost shipment; panicking at Q4 delays | Read the breakdown; escalate past the window (R69) | 03 |
| Feature-led bullets | Benefits with one true claim each (R54) | 01p2 |
| Brand name or buzzwords first in the title | Target phrase first (R52, R53) | 01p2, 01p3 |
| DIY or generated images | Real product, professional shots (R55, R56) | 01p2, 01p3 |
| Empty backend keywords; listing live to zero demand | Fill; future start date (R58) | 01p2 |
| Ignoring compliance flags (COA) | Buffer time (R60) | 01p3 |
| Launching quietly with no audience | Build the waitlist first (R72) | 01p2, 01p3 |
| Reimbursed, recruited, gated or incentivised reviews | Amazon's request path only (R84, R85) | 01p2, 01p3 |
| Vine on a product that is not ready or for the wrong audience | Fix the product first (R86) | 01p3 |
| One blended automatic bid; no negatives | 4 ad groups; negatives everywhere (R78, R81) | 01p2 |
| Untracked PPC or Facebook spend | Attribution; net profit test (R82, R96) | 01p3 |
| Reading revenue as profit; reading a stockout month as demand | P&L by fee line (R40) | 01p1, 01p3 |
| Calling a product dead after a seasonal dip | Full-year map (R97) | 01p1 |
| Not claiming fee errors and lost units | Monthly audit (R41) | 01p2, 01p3, 03 |
| Coasting once a revenue goal is hit | Keep growing or plan the decline (presenter's "most expensive mistake") | 01p3 |
| Outsourcing before mastering the work | Master first, then delegate; but delegate non-revenue tasks sooner than AJ did | 03, 01p1 |
| Buying software before it has data to work on | Sequence spend to need | 03 |
| Quoting course figures to a client | Brand data and live checks only | ecomOS |
| Agent writes to the account | Human owner for every write | ecomOS |

## 9. Deliverables

**9.1 Channel decision memo.** 1 page. Recommendation (yes, no, not yet) and date. Product, marketplace, price, landed cost. Gate results: category, trademark, price floor, net margin, cash, differentiation, fulfilment fit. Revenue band targeted and why. First order size and PPC reserve. Open `[web check]` and `[needs brand data]` items. Risks in plain words. Owners for each human step. Format: Markdown, table of gates, numbers with their source (brand, quote, web).

**9.2 Product screen sheet.** One row per candidate or SKU; columns: category and gating; page-1 price band and spread; brand dominance; top-10 review counts; listing age of comparables; keyword variability count; keyword gap (phrase, volume, live check); revenue estimate (tool, BSR cross-check); review-mining findings (complaint, share of 1-star, fix in brief); giftability; verdict. Each filter value marked "presenter heuristic". Format: CSV or table.

**9.3 Fee and margin model spec.** Inputs: price, unit cost, freight, duty, bond, inspection, dimensions, weight, category, marketplace, VAT status, return rate, months in warehouse, Q4 share, CPC, conversion. Lines: referral, FBA, storage, long-term storage risk, labelling, prep, returns, disposal, plan fee, PPC per unit, VAT on fees. Outputs: net margin per unit, price to cost ratio, contribution after PPC, breakeven units, launch budget by line, cash needed for first order plus PPC. Every fee line carries its source and date of the web check. Format: spreadsheet spec (columns and formulas in words), then the model in the finance track.

**9.4 Listing brief.** Target phrase and the 3 keyword buckets; title; 5 bullets with the claim source for each; description; image list (main plus up to 8, each with content and the real photo asset); attributes table; backend keywords; offer start date; category node; compliance documents; A+ module plan. Marked for the human who publishes. Format: Markdown.

**9.5 Launch plan.** Dated timeline from 8 weeks out to month 3: audience build, seeding (no review ask), stock check-in, PPC start, launch email with Attribution links, review requests through Amazon only, reorder trigger, price throttle rule, PPC budget test date. A section "tactics rejected and why" listing anything from the sources that breaches policy. Owners per step. Format: Markdown table.

**9.6 PPC structure.** Campaigns, ad groups, targeting type, match type, bids, daily budgets, negatives, naming convention, weekly review rules and thresholds, what needs a human. Format: table.

**9.7 Monthly Amazon report.** Revenue, units, sessions, unit session percentage, organic vs paid orders, PPC spend and ACOS, P&L by fee line, net margin, returns, stock cover and stockout days, inventory age, storage fees, fee claims filed, account health, reviews and rating, Brand Registry and hijacker status, actions needing a human. Missing values shown as unavailable, never zero. Period ROAS as total value divided by total spend. Format: Markdown with tables; client version follows the writing rules and never mentions tools or credentials.

## 10. What needs live data or a web check

**`[needs brand data]`**
- Landed cost per unit, price, dimensions, weight, packaging, consumable status, shelf life (R3, R35, R37, R38).
- Category, gating or compliance documents, approved and banned claims (R23, R54, R60).
- Cash for first inventory and 3 months of PPC; acceptable loss (R4, R5, R90).
- Entity, tax IDs, VAT status, bank, ID documents (never stored in the playbook) (R10, R14, R16).
- Trademark status, mark type, class, application number (R17, R18).
- Prior Amazon accounts (R9).
- Sales velocity, sessions, unit session percentage, search term reports, stock and inventory age once live (R40, R90, R95).
- Return rate for the category (5.3).
- PPC negative-keyword spend threshold and target contribution (P15).
- Margin per unit for the PPC budget (R42).
- Audience assets: email list, social, existing customers (R72).
- Counsel for NNN, patents, entity (R22, conflict 11).
- Which coast or state a real forwarder or prep centre sits in, if used as ship-from (conflict 4).

**`[web check]`**
- Plan prices and Individual plan limits by marketplace (R8).
- Identity, payment card and verification requirements; account red flags (R10, R11, R12).
- GS1 pricing (R15).
- VAT treatment of Amazon fees by marketplace (R16).
- USPTO and UK IPO trademark fees; Brand Registry eligibility, benefits, incentives; Brand Referral Bonus mechanics (R17, R20, R21).
- Patent fees; NNN enforceability (R22).
- Restricted, gated and hazmat category lists; ad policy for the category (R23, R83).
- Referral fee by category; FBA fee tiers and size limits; storage rates; long-term storage threshold and rate; labelling, prep, return and disposal fees (R37, R38, R39, R92).
- Duty by HS code; customs bond costs (R37).
- FBA case and box limits by marketplace; partnered carrier options; cancellation window; UPS pickup terms (R62, R66, P10, P11).
- IPI, capacity and restock limits (R94).
- Vine terms; feedback removal rules; review policy (R84, R86, R87).
- Return policy wording for any guarantee bullet (R54).
- Helium 10 Black Box, Magnet, Cerebro UI and pricing; Jungle Scout estimator (P4, P7).
- Amazon Live current state; Alibaba "Trendy Hunter"; Shopify-URL listing draft (R74, P8).
- Sales tax nexus and marketplace facilitator rules (R14).
- Every market statistic the sources quote (section 0).

## 11. Freshness and stale-risk notes

| Area | Why it goes stale | Re-verify |
|---|---|---|
| Fee tables: referral, FBA, storage, long-term storage, labelling, prep, returns, disposal, inbound placement | Amazon changes fees at least yearly, often in Q1 and before Q4; the sources already disagree on several | Before every margin model and every quarterly report; always before a client deliverable |
| Long-term storage window | Stated as 180, 365 and "6 months" in one source | Before every replenishment plan |
| Plan prices and Individual plan limits | Change by marketplace and year | Before signup and yearly |
| Seller Central UI: Add Products, Send to Amazon, Manage FBA Shipments, Inventory Breakdown, Brands, Campaign Manager | Source 03 says the shipping workflow "changes often"; every path here is `[verify UI]` | Before each procedure run; update P8, P10, P11, P12, P14 when a step no longer matches |
| Helium 10 UI and filters; Jungle Scout tools | Source 04 is from April 2023; tool names and plan tiers move | Before P4 and P7; yearly at least |
| Policies: reviews, Vine, feedback removal, ship-from, restricted categories, hazmat, claims | Policy pages change; enforcement changes faster | Quarterly, and before any launch plan |
| Brand Registry benefits, incentives, Brand Referral Bonus | Program terms change | Before P3 and yearly |
| Size and weight limits for cases and boxes | Changed in the past; differ by marketplace | Before every shipment plan |
| Trademark, patent and GS1 fees | Set by agencies; the sources disagree already | Before P3 |
| Duty and tariffs | Trade policy moves | Before every sourcing quote |
| VAT and sales tax rules | Law changes; marketplace facilitator rules | Yearly and on any new marketplace |
| Case study figures | Self-reported, undated, inconsistent | Never use as benchmarks; keep as examples only |
| Amazon Live, AI listing drafts, Trendy Hunter | Features the sources call "new" are not; some may be gone | On first use |

## 12. Source index

| No. | Title | Type | Credibility and bias | Contributed most |
|---|---|---|---|---|
| 01 (01p1, 01p2, 01p3) | FREE Amazon FBA Course: 12 Hour Full Step by Step Tutorial 2025 (155,303 words, 256 cards, 3 part files) | YouTube course transcript | Presenter "Travis", about 10 years selling; sells the Passion Product Formula program and a $7 challenge; FBA Creatives design service; affiliate links to Helium 10, Jungle Scout, LegalZoom, WY Registered Agent, credit cards. All figures self-reported; case studies are student testimonials and course marketing; two failure cases are framed to sell the course. Several figures inconsistent inside the source (conflict 5). Unsourced market statistics. Describes policy-breaching review and ship-from tactics while flagging them. Rating: strong on procedure and mechanics; weak on numbers; promotional. Medium credibility for how, low for figures. | Account signup flow; trademark and Brand Registry; Magnet, Cerebro, Blackbox and autocomplete research; fee stack and storage maths; thirds and 3x rules; Amazon-specific sourcing (capacity, samples, 30/70, inspection, freight, customs); listing field walkthrough; case packs, labels, small parcel vs LTL, BOL, shipment statuses; 10 launch techniques; PPC structure (auto split, manual, product targeting, negatives); inventory cover rules; 13 case studies with budgets and P&Ls; failure patterns |
| 02 | Beginners Guide To Amazon FBA In 2025 (UK) (7,558 words, 10 cards) | YouTube tutorial | Unnamed UK presenter, about 5 years; sells mentorship; students by first name; free PDF lead magnet; "800% ROI" claim. Reseller focus; its own export header says to skip arbitrage and the BSR and ROI formulas. Dated 2025-06-28, mid-2025 UK account. Rating: low to medium; useful only for UK mechanics. | UK account and video verification; UK plan prices; 20% VAT on Amazon fees; Send to Amazon flow, prep and labelling choices, box limits (63.5 cm, 23 kg), carrier and pickup booking; FBM exceptions; capital by business model |
| 03 | How to Start Amazon FBA in 2026 (5,654 words, 10 cards) | YouTube talk, auto captions | "Jazz Hustles", 21, arbitrage seller since January 2023; sells mentorship; affiliate codes for SellerAmp, Keepa, SellerBoard, FastTrack VA. Its capture header says "DO NOT CAPTURE... Source should be discarded". Shot 16 January 2025. Transcript errors ("FDA", "$339.99"). Rating: low; arbitrage only; a few platform mechanics kept. | Document checklist; plan crossover about 41 units; FBA Inventory Breakdown statuses and check-in timing (3 to 4 days transit, 1 to 2 weeks, 2-week escalation, 1 month in Q4); FNSKU labels from Seller Central; sequencing spend to need; reimbursement claims |
| 04 | COMPLETE Amazon FBA Product Research Masterclass (5,019 words, 8 cards) | YouTube transcript | Sean Peterson, self-described 7-figure seller (about $102,000 in 30 days on screen, unverified); Helium 10 affiliate (20% off); sells consultation calls with a "guarantee". April 2023, Helium 10 UI of that time. States his numbers are heuristics and not to copy his filters. Rating: medium for the screening logic; low for numbers; promotional. | Elimination screen; $25 floor and 30% net margin; brand dominance; keyword variability; page-1 price disparity; Black Box recipe (300 reviews, $25 to $60, $5,000 to $20,000, 8 months, 4 images); review mining 4.1 to 4.3 stars into a supplier brief; revenue band matched to cash; giftability |

**Neighbour folders and what lives there.**
- `01-PRD-product-research`: demand research beyond Amazon, idea generation, crowdfunding validation, pre-sales.
- `18-COG-sourcing`: supplier search and vetting, Alibaba and ThomasNet, negotiation, factory audits, freight forwarders, sourcing agents.
- `20-FIN-finance-and-accounting`: entity, tax, VAT, sales tax nexus, cash planning.
- `04-BRD-brand`: brand name, logo, packaging design, trademark strategy beyond the Amazon steps.
- `24-DEP-ad-deployment` and `10-MCR-paid-social-creative`: off-Amazon paid traffic and creative that feed Amazon launches through Attribution links.
- `12-GAD-google-ads`: Google traffic to Amazon or DTC.
- `11-ADC-ad-copy-deployment`: copy craft for bullets, A+ and ads.
- `06-MEA-measurement`: attribution and reporting standards the monthly report follows.
- `17-CXP-post-purchase`: inserts, follow-up and support that must stay independent of review behaviour.
