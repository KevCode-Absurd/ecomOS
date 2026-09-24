# 01-PRD product research playbook

version: 2.0-draft  |  date: 2026-09-24  |  sources: 10  |  cards: 170  |  built from: sources/*.md

## 0. How to use this playbook

**Ecommerce first.** This playbook is for stores: DTC, marketplace or hybrid, not general business ideation. Section 3.0 is the ranking: load it before the numbered groups in section 3. Store-type conditions (hero SKU vs catalogue, low vs high AOV, subscription vs one-off, marketplace-heavy, luxury or considered purchase, mobile-first India vs US) decide which rules apply to the candidate in front of you.

**Who runs it.** The product research agent. Its job ends at a go or no-go decision on a specific product, with a validation memo, a supplier brief and a launch sequence plan attached. Creative production, media buying, storefront build and fulfillment setup are other folders (see section 1).

**Which sections to load for which task.**

| Task | Load | Run |
|---|---|---|
| Find new product ideas for a brand | 0, 1, 2, 3.1 to 3.5, 5.1 | Procedures P1 to P8, then P17 |
| Screen a candidate someone else found | 3.6 to 3.13, 5.1 to 5.4 | P9 to P14 |
| Full validation memo before sourcing spend | 3.6 to 3.13, 3.16, 6 | P13, P14, P19 |
| Supplier brief and sample order | 3.14, 5.5 | P15, P16 |
| Launch order and market expansion | 3.15, 7, 5.6 | P18 |
| A paid test failed, is the product wrong? | 3.16 | P20 |
| Reconcile conflicting advice | 7 | none |

**What the agent fetches before acting.**

1. From the brand record: business model (dropshipping, private label, owned manufacturing), margin floor, target countries, ad budget per test, current catalog, existing suppliers, first-order budget and acceptable MOQ, audience age skew, which ad platform the brand actually runs. Section 10 lists every `[needs brand data]` item.
2. From the data layer: real landed cost, shipping cost per order, refund and chargeback rates, payment processing rate, past test results with CPA and ROAS. These numbers override any figure a source gives about its own store.
3. From the web: current state of every tool named here (many are subscription products pushed on affiliate links), Meta Ad Library and TikTok Shop data for the candidate, regulations per target country. Section 10 lists every `[web check]`. Section 11 says how often to re-check.

**What the sources are.** 10 mini playbooks. 7 of them (02, 04, 05, 06, 08, 10 and much of 03) are dropshipping or DTC creators who sell a course, mentorship or tool, and several push tools on affiliate links: 02 (Spy Crew bundle, own paid community), 04 (Team Drop referral bonuses, own paid community), 05 (Winning Hunter discount code, own mentorship), 06 (own mentorship, prompts only via Instagram DM), 08 (ShopHunter 25% off, ZenDrop 50% off plus $200 credit), 10 (Luxury Extras tool bundle), 03 (own tool Trend Rocket, own coaching). 09 is Shopify's own channel and pitches a Shopify trial. 07 is a software podcaster demoing Alibaba's Axio with no affiliation to Alibaba, but promoting his own paid idea newsletter. Only 01 (a serial consumer-brand founder turned VC) sells nothing in-video, and his evidence is his own recollection. No source cites a dataset, a study or audited numbers. Every threshold in this playbook is a practitioner heuristic unless section 6 says otherwise. Section 12 rates each source.

**Sources 02 and 10.** The brief for this pass said 02 and 10 look like two cuts of the same talk with different headline numbers ($2.3M and $670k). Mini playbook 10 raised that guess. The cards and snapshots do not support it: 02 is a June 2025 video (youtube v=sCUEN4htx-0) on Kalodata and TikTok Shop screening with Meta as the sales channel; 10 is a February 2026 video (v=QwWO3EUYW2E) on Get Hooked filters, native news widgets and Facebook-first offers for 60+ buyers. Different tools, dates, methods and claims. This playbook keeps them as 2 sources. What they share: both are single anonymous or near-anonymous dropshippers with unverified revenue claims and a tool to sell. Neither headline number is used anywhere in this playbook as evidence. `[web check: whether the 2 presenters are the same person; it does not change any rule]`

**Dropshipping assumption tag.** Rules marked `[dropshipping assumption]` depend on the arbitrage model: find a product already selling on someone else's store, source the same generic item, resell it at a markup on Meta, discard fast if it fails. Each such rule says how it changes for a branded brand that owns its product, holds inventory and has a reputation to protect. Short version: the branded brand keeps the graph-reading, demand, competition and economics checks, drops the "flip someone else's winner" mechanic, and raises the bar on differentiation, samples and regulatory checks because a failed SKU costs inventory, not just ad spend.

**ecomOS rules that override any source** (repeated in 3.17):
- No invented claims. A product angle cannot promise an outcome the brand cannot prove.
- No copying competitor products, text, logos or faces. Competitor ads are signals, not proven winners. Use them for demand proof, layout and mood only.
- Numbers from the brand record and warehouse win over any source's self-reported figures.
- Meta is read-only. Research uses the Ad Library and read tools only.
- Keep brands apart. Keep public web research separate from private business data.

## 1. Scope and outcomes

**Covers.** Where product ideas come from (boring-category thesis, TikTok Shop screening, ad library and spy tool scouting, native widget scouting, organic feed training, AI-assisted research, Alibaba's agent, supplier-first sourcing). Demand and competition validation (view and revenue thresholds, 30-day vs 180-day trend read, saturation reads, evergreen vs trending, competitor proof, positioning gaps and unserved avatars). The 16-question validation framework. Unit economics gates (price band, margin, shipping, durability, perishability, regulatory). Sourcing and supplier vetting (Alibaba, AliExpress reverse image, private branded-dropshipping suppliers, sample orders). Launch sequencing and international expansion order. The go or no-go decision and what to do when a first test fails.

**Does not cover.** Building ad creative from a validated hook (03-CRE; source 02's mix-match splicing lives there). Running and reading the Meta test itself (04-MED; source 06's CPC, CTR and CPM diagnostics are a handoff, not this folder's core). Storefront, advertorial and checkout build (05-WEB). Fulfillment app setup, 3PL wallets, shipping-line configuration (06-OPS and 18-COG; source 04's Team Drop setup steps are summarized only as far as they affect sourcing decisions). Testing one product across several buyer avatars in ad creative (02-AVT; source 03 routes it there). Exit valuation multiples (20-FIN; source 03). Naming and brand identity (source 01's naming method is noted in 3.8 only where it affects positioning). Founder psychology, hiring and mental health (sources 01 and 03; not extracted).

**Business measures this domain moves.** Hit rate of tested products (source 05 claims about 1 in 2 after angle pivoting, unverified). Gross margin per unit and margin after ad cost. Capital at risk per test (ad spend for dropshipping; ad spend plus inventory and MOQ for an owned product). Time from idea to first test. Refund and chargeback rate driven by product quality, durability and delivery time. Share of revenue from a single hero product (source 03's warning: the Udie hero declined faster than secondary lines grew).

## 2. Inputs the agent needs

| Input | From where | Required or optional | Why |
|---|---|---|---|
| Business model: dropship, private label, owned manufacturing | brand record | required | Decides which `[dropshipping assumption]` rules apply and how strict the sample and regulatory gates are |
| Margin floor and target contribution margin after ads | brand record | required | Replaces the $30 and 3x heuristics with the brand's own bar (R76) |
| Landed cost, shipping per order, processing rate, refund rate | data layer (warehouse, payments) | required for any go decision | The source margin rules ignore these costs (06, 07); the gate must include them |
| Target countries and current ship-to cost and speed per country | brand record, 3PL | required | Expansion order (R99), shipping window (R85), duty and VAT (R100) |
| Ad budget per test and number of angles affordable at once | brand record | required | Sets how many candidates per week and whether multi-angle tests are possible (R65, R97) |
| Which ad platform the brand runs (Meta, TikTok, Google) | brand record | required | TikTok saturation reads and the Facebook-first assumption change by platform (R24, R33) |
| Audience age skew | brand record, data layer | optional | Native widget method assumes 60+ buyers (R33) |
| Existing catalog and hero product | brand record | required | Secondary-product rule (R59), 1 SKU rule (R87) |
| Existing supplier relationships, MOQ tolerance, first-order budget | brand record | required for supplier brief | P15, P16, R89, R92 |
| Past test results (CPA, ROAS, CTR, ATC rate) | data layer | optional | Recalibrates revenue band and margin floor (R15, R76), post-test diagnosis (R107) |
| Candidate list from a human or another agent | user | optional | Runs through P9 to P14 regardless of origin (R105) |
| Reference ads and competitor stores | inspiration, web | optional | Angle audit (R60), offer audit (R63), never for copying |
| Tool access: Kalodata or Shop Plus, an ad-spy tool, SimilarWeb, Google Trends, Keyword Planner | web, brand subscriptions | optional per method | Each method in section 4 lists which tools it needs and a free fallback |
| Regulations per category and country | web | required for cosmetics, food, supplements, baby, medical claims | R84, question 16 of P13 |

## 3. Decision rules

Format: rule, condition (when it applies and when it does not), sources by mini playbook number, conflicts, card ids. "Strict" means the merged rule keeps the tightest version any source gave.

### 3.0 Ecommerce priority order

Load this ranked list before the numbered groups below. Each lever points to the rule ids it draws on. Conditions by store type decide which side applies.

1. **Margin and contribution gate (R76, P14, O4).** Nothing else matters if the product cannot pay for its own acquisition cost; the hard stop every source implies.
2. **Regulatory and IP clearance (R84, R86).** A miss voids the SKU after money is spent on samples or ads; the other no-override stop.
3. **Owned difference named (O2, R60).** Proven demand with no angle is a cash test (R56), not a bet for a brand holding inventory and reputation.
4. **Demand read matched to the brand's own ad platform (R24, R44 to R49).** TikTok-Shop-heavy brands read video and live data directly (R15 to R21); Meta-only brands treat TikTok data as a lead, not proof.
5. **Competition ladder, exact-product and niche level (R53, R54).** Amber or red with no angle routes to P12 first; green goes straight to economics.
6. **Price band and margin floor from the store's own AOV (R75, R76, O4).** Impulse-price stores live or die on the dollar floor; a luxury or considered-purchase store should raise it and lean less on the 3x multiple. `[general practice]`
7. **SKU strategy by store type (R59, R87, C5).** A hero-SKU launch opens at 1 SKU with a secondary-product plan; a catalogue brand checks gaps in its existing range instead, since R87 assumes no catalogue yet. `[general practice]`
8. **Subscription or repeat fit from real usage (R72, R9).** Subscription stores gate on replenishment cadence; one-off or considered-purchase stores check LTV against AOV instead (R113; card 3b6e3ec9a71b).
9. **Sourcing model by channel (R93, R50).** A no-inventory store compares agent vs marketplace-direct cost (R93); a store also on a third-party marketplace reads that marketplace's own density and fees separately (R110). `[general practice]`
10. **Logistics and durability priced before sourcing (R81 to R83, R85).** A shippability gate, not a differentiator, but it still kills candidates that passed 1 to 9.
11. **Supplier vetting and sample order (R89 to R92).** Only after the SKU clears 1 to 10, so cash and goodwill are not spent early.
12. **Launch sequencing and expansion order (R99, R100).** A mobile-first India-vs-US move must re-price duty, payment friction (R115) and delivery days per market first. `[general practice]`

Load this block first; the groups below are the detail.

### 3.1 Where product ideas come from

**R1. Enter a large, existing, high-frequency category rather than inventing one.** You skip educating buyers on what the product is and only have to win on differentiation. Condition: choosing a category for a brand that will own its product for years. Does not apply to a short-window cash test on a trending item (R69). Sources: 01 (Method, Olly, Wellie were all decades-old categories). Conflict: 03 says chase a trending product, not a market, for speed to $10M; see section 7, conflict C2. Cards: [04109fbada87] [43675a4ef223].

**R2. Look for a "sea of sameness".** Within a category, near-identical packaging, color and voice across every incumbent is the opening. Over-complication or self-seriousness in a category is a second signal. Condition: category scan for an owned brand; walk the physical aisle or the search results page, not just a spy tool. Source: 01 only. Cards: [04109fbada87] [82c3c64bf61f].

**R3. White space is a category where buyers cannot name a favorite brand.** Ask people to name their top 3 brands; if they cannot, or the label is just the generic name, there is a gap. 03 states the same idea as "problem-aware, product-aware, not brand-aware" buyers, who convert without warm-up. Condition: an opening hypothesis, not proof of demand. 01's own jewelry venture had strong consumer love and still failed on economics (R80). Sources: 01, 03. Cards: [1dbc0386d821] [fff4fa23ccb9].

**R4. Watch for a shift in how people shop, pay or get delivery (buy-now-pay-later, TikTok Shop checkout, same-day delivery) that incumbents have not built for; it only counts once it changes what a buyer expects on a PDP or at checkout.** Condition: idea generation. Neither source gives a checklist beyond this. Sources: 01, 03. Cards: [82c3c64bf61f] [d8999078063c] [225664d8dac9].

**R5. The product must solve a felt problem or serve a passionate community; daily pain ranks highest.** Merged from 6 sources. 10 requires a problem felt every day (foot pain on every step). 06 requires an emotional problem inside a market. 05 and 02 require a real problem or insecurity, and 02 warns beginners pick problems that are too small. 09 accepts pain or passion, or both. 08 accepts either a problem or a passionate community (its anime katana example passes on passion alone). Strict merge: require at least 1 of the 2, rank daily pain above occasional pain above passion, and reject "nice to have". Condition: every candidate from every method. Sources: 02, 05, 06, 08, 09, 10. Conflict: 10 would reject a passion-only product; 08 accepts it. Section 7, C9. Cards: [cccca902b389] [c9b651f1b77d] [9651e08d5907] [6be819f254f6] [ec2cf7075718] [178c6277a818].

**R6. Pick a broad emotional problem, not a narrow one.** One problem (migraines) maps to many products (supplement, headband, massage gun, traction device), so you have more to test. Condition: narrowing from market to problem before product search. Source: 06 only. Cards: [c9b651f1b77d].

**R7. Pair demand with a quality gap.** High search or sales volume alone is not an opportunity if buyers are already satisfied. Look for volume plus a low average rating; 07's heuristic is about 3.8 or below on Amazon for the specific sub-niche. Condition: owned or private-label product where you can fix what reviews complain about. Does not help a dropshipper reselling the same item. Source: 07 only, from one demo. Cards: [d814f1dad676].

**R8. Ground a pain point in a review naming the product and a real complaint (a PDP review, a return reason, a support ticket), not a category-level post; confirm it is about the product, not the topic.** Condition: any AI-mined pain point list. Source: 07. Cards: [385b53666fdd].

**R9. Choose the category to fit the business model you want.** 02: health products suit renewables and subscription revenue; beauty, apparel and underwear, home improvement and jewelry skew to one-off high-volume sales with fewer sellers hunting there. 09: consumable and disposable formats support repeat purchase. Condition: preference, not a gate; 02's own $1.5M store had 0 subscribers. Sources: 02, 09. Cards: [aa365bb09a4b] [b4379b7a96e8] [480136acffdb].

**R10. Prefer products that are scarce offline and absent from big-box retail.** Easy local availability removes the reason to buy online and weakens margin protection. Condition: general screen; neither source gives a fallback if you proceed anyway. Sources: 09, 10. Cards: [5101fbb610a7] [cccca902b389].

**R11. A founder's own taste is not a demand signal; run the demand check (P9) or the store's conversion and repeat-purchase data before funding a candidate on preference.** Condition: beginner or new-brand selection. Conflict: 01 uses the founder's own excitement (the "energy test") as a selection signal between finished concepts. Section 7, C4. Sources: 03, 05. Cards: [4255b2303ee8] [0a9bbf43cada].

**R12. Random, un-niched products are an optional beginner path.** `[dropshipping assumption]` They dodge the high CPMs of brand-heavy verticals (women's beauty, dog products) where an unbranded seller cannot compete on ad cost. 05 calls this "by no means a must-do". For a branded brand: not applicable; the brand's category is fixed, so use R60 (unserved avatar) instead. Source: 05. Cards: [c97ea08c9bfc].

**R13. Customization is a demand signal with a fulfillment cost.** Personalized items (photo phone case, custom crystal frame) advertise well on TikTok per 08, but the source ignores the added handling, lead time and returns. Condition: treat as a plus in scoring only if the brand can fulfil custom orders. `[needs brand data: can the 3PL or supplier handle per-order customization]` Source: 08. Cards: [6cb10ef0ecb5].

**R14. Trend tools are a source of SKU ideas only; every idea clears the same PDP-ready checks (platform demand, Ad Library count, landed-cost margin) as a product scouted from Meta or TikTok Shop before it reaches the shortlist.** Condition: always. Sources: 08, 09, 03 (Exploding Topics named as a tool). Cards: [bdee2e77e91b] [2c09edad5b25] [b08de7f842b3].

**R110. A marketplace listing (Amazon, Flipkart, Meesho, Myntra, Etsy) is a separate channel with its own fees, search ranking and competitor set; a marketplace-heavy brand screens a candidate against that marketplace's own listing density and take rate, not only Meta or TikTok Shop data.** `[general practice]` No library source; verify against brand data before use.

### 3.2 Screening TikTok Shop data (Kalodata or Shop Plus) `[dropshipping assumption]`

All rules here come from source 02 alone, one operator's live screen-share. A branded brand can use them to read demand for a category or format it already sells or plans to make; it must not use them to pick someone else's product to resell.

**R15. Filter to $33,000 to $97,000 revenue in the last 30 days, and avoid products above $300,000 a month.** The top of the band is a heuristic to avoid the most contested products; $300K to $1M+ means many competitors. Recalibrate from your own test results: if a $20K product tested unprofitably, raise the floor to about $40K next hunt; pushing to $200K to $300K trades that for maximum competition. Condition: Kalodata Products tab, last 30 days, one category at a time. Source: 02. Cards: [f950357be56c] [5c7c5df4a96e] [d646f7ac02d3] [55e052fdbfd1].

**R16. Count video revenue only, exclude live-stream revenue, and reject a product where live revenue is about $25,000 or more.** Live-stream success does not transfer to a replicable video ad. Condition: any TikTok Shop screen. Source: 02. Cards: [d8128fe11921] [f950357be56c].

**R17. Sort lowest to highest revenue inside the band and screen by graph shape before looking at the product image.** Lowest first surfaces the least-discovered breakouts; ignoring the image on the first pass avoids bias. Use the image only as a second check for products you already recognize (R22). Source: 02. Cards: [47c4014d910a].

**R18. Read the 30-day graph, then always open the 180-day graph before deciding anything.** Keep 30-day graphs that are flat or tilting up at the end; discard straight downtrends. On 180 days, reject a product that peaked months ago and now flatlines or declines, reject a flat line, and treat up-down-up with an overall rise as healthy. Skipping the 180-day view is the mistake 02 warns about most. Condition: every candidate. Source: 02. Cards: [a560155647d3] [aed42c07b4e8] [558f5e822852].

**R19. A steep, uninterrupted new curve with no prior history is a gamble, not a validated winner.** It has no downside data. A product with an established up-and-down history that trends up overall is the healthier signal even when smaller. Condition: brand-new listings. Conflict inside 02: it also says speed into a spike buys ad-account history on that product (a belief, not a documented platform rule). Section 7, C6. Source: 02. Cards: [ae35f8af0cb0] [160628e26bfe].

**R20. The top video must be from the last 7 to 14 days, revenue must spread across 3 to 5 recent videos, and a single old video carrying 90 to 95% of revenue is a reject.** Check the last-7-days video view, not only lifetime, because the top lifetime ad and the top recent ad differ. Stated exception: if the top video alone did tens of thousands in the last 7 days (02's example: $58K vs $600 on the runner-up), 02 still tests it. Condition: TikTok Shop candidates; log the exception when you use it (R106). Source: 02. Cards: [d428c3748db2] [cc4b1af32e18] [56a8113dfb7e].

**R21. Require winning creative in the target market's language.** A Spanish top video for a US test means the product sells to Latin American buyers, not US English speakers. Skip for that market; it says nothing about the product elsewhere. Source: 02. Cards: [9130c566dbb1].

**R22. If you recognize the product or brand, treat that as saturation and skip it.** Familiarity from repeated exposure is a saturation read regardless of graph shape (02's example: moringa). Condition: your own recall while scanning. Conflict: 05 and 08 say saturation is demand if an angle is open (R55). Source: 02. Cards: [eb853be1825b] [47c4014d910a].

**R23. The tool's category bucket is not the product's true niche; widen filters before abandoning a niche.** A supplement can sit under beauty. Adjust the category filter first; switch niche only if that still returns nothing. Source: 02. Cards: [ba18dae7b09a] [83c660eb50cb].

**R24. TikTok Shop validation does not guarantee a Meta win, and TikTok saturation alone does not disqualify a Meta test.** 02: you test with your own ad, offer and platform, so treat the product as a candidate for a short test. 05: weight the density on the platform you actually advertise on; note in the log when a product is TikTok-heavy but Meta-light as an untapped signal. Condition: brand advertises on Meta. If the brand advertises on TikTok itself, weight TikTok density directly. `[needs brand data: primary ad platform]` Sources: 02, 05. Cards: [1d273c71ce53] [cf56089fcd7c].

### 3.3 Ad library and spy tool scouting

**R25. Use ad run length as the profitability proxy; the strict bar is 14 days currently running.** 10: minimum runtime 14 days in Get Hooked, and more than about 1 week for an Ad Library match. 08: sort PP Ads by days running, longest first. 02: an ad running only hours has no spend history and validates nothing; bookmark and watch. Condition: any tool that exposes run length. Runtime is not proof of ROAS; no source shows that link. Sources: 02, 08, 10. Cards: [67d480044198] [1586541150e9] [c37e17bb2b06] [4be18218219d].

**R26. Read many concurrent active ads from one page as budget and confidence, not as profit.** 10 filters to brands with more than 50 active ads; 06 qualifies a brand on "enough active ads" (no number) and 08 on a high concurrent count. All three then require a separate revenue check (R49). Condition: tools that report active ads per page. Sources: 06, 08, 10. Cards: [67d480044198] [b09a0ce63306] [3d818b03cb3b].

**R27. Search the Meta Ad Library with generic direct-response phrases to surface dropshipping-style advertisers.** "free shipping", "50% off", "shop now", or a problem keyword like "pain relief". Filter to active ads; optionally restrict to the last 1 to 2 weeks to bias toward new tests. `[verify UI]` Condition: free scouting. For a branded brand these results show the low end of the market; also search the category term itself to see branded competitors. Sources: 05, 08. Cards: [0cdc9e5914ee] [3d818b03cb3b].

**R28. Category filters under-include; fall back to manual keywords.** 10's health category returned junk until he searched symptoms. 02's gut-cleanse example returned little on obvious terms even though competitors existed, and 02 gives no fix beyond "decide anyway". Condition: any spy tool or Ad Library search. Sources: 02, 10. Cards: [67d480044198] [4be18218219d].

**R29. In spy-tool scans, skip established mega-brands and look for generic, adaptable products.** `[dropshipping assumption]` 08: heavily branded advertisers leave little room to adapt. For a branded brand: reverse it. The mega-brands define what is already served; use them for R60 (unserved avatar) and R7 (quality gap), and do not skip them. Source: 08. Cards: [c37e17bb2b06].

**R30. Cap ads per brand at 4 in the spy tool and set 500 results per page.** Prevents one advertiser flooding the list; broad pages speed the scan. `[verify UI]` Sources: 10 (cap of 4), 08 (500 per page). Cards: [67d480044198] [c37e17bb2b06].

**R31. Judge each competitor's store and offer, not just their ad.** A generic template store, no subscription and a weak offer is a beatable competitor; a polished branded store with a strong bundle is a real one. A store that has stopped running the product does not count toward saturation. Condition: after the competitor count (R53). Sources: 02, 05. Cards: [4be18218219d] [555bf9237f92] [2ee82e58c7a1].

**R32. Mine a validated competitor's longest-running or highest-impression ad for the avatar and the angle, never for the asset.** 10: find the avatar (a mother worn down by a 4-year-old's bedtime) and message frame, then build your own native ad against the same avatar, executed better. 08: sort an advertiser's ads by impressions to study audience, copy and variant count. 02: a ripped ad makes your store indistinguishable. ecomOS override: text, logos, faces and video are never reused; see 3.17. Sources: 02, 08, 10. Cards: [1c7e14118dbb] [c37e17bb2b06] [3662a6024399].

**R33. Native ad widgets on news and weather sites are a shortcut to older-buyer offers.** 10 asserts these placements skew to 60+ visitors and refreshes the "paid content" block to log recurring problem categories (neuropathy, tinnitus, incontinence, hearing, snoring, joint pain). Condition: brand targets older buyers on Facebook; the demographic claim is unsourced. `[web check: whether weather.com and CNN still carry native widgets and which vendor]` `[needs brand data: audience age skew]` Source: 10. Cards: [484b2d31c673].

**R34. Do not scrape saturated aggregator feeds or copy a competitor's store as a beginner.** 10: thousands work the same AliExpress-style feed, CPMs and CPCs rise, and a win cannot be repeated because no skill was learned. 05: copying a competitor's product or store "a bit better" simply does not work for beginners. Condition: always. Both sources still run methods that start from a competitor's product; the difference they imply is that something in your execution (avatar, geography, offer, research depth) must differ. Sources: 05, 10. Cards: [d3641c6bc6a8] [4255b2303ee8].

### 3.4 Organic feed scouting

**R35. Train a fresh social account to surface product ads, and expect it to drift.** 08 (TikTok): new account, watch and like every dropshipper-style pitch, keep scrolling. 05 (Instagram): new account, search #winningproduct, like 5 to 10 product videos, switch to Reels, keep liking to hold the feed on topic; works better on mobile; run in short frequent sessions. Condition: free discovery. Conflict: 10 calls TikTok and Instagram burner scouting outdated for 2026, says it needs a trained eye that takes 3 to 6 months, and that Instagram burners mostly show reposts from TikTok and AliExpress; 10 allows a Facebook burner as a middle option. Section 7, C10. Sources: 05, 08 for; 10 against. Cards: [ef25d34ce2bb] [ab2f47bf79d4] [1bd4e5736ad6] [d3641c6bc6a8].

**R36. One viral video is not a candidate until the creator's profile shows at least 3 videos over 1,000,000 views.** Below that, treat it as a fluke and keep scrolling. High views can reflect the creator's personality, not the product. Condition: organic finds. Source: 08, personal heuristic. Cards: [056889323762].

**R37. The moment a scouted post shows a sellable product with a visible price and offer, stop scrolling and log it; more scrolling delays validating it, it does not improve the shortlist.** Source: 08. Cards: [ef25d34ce2bb].

**R38. Existing content must exist for the product, or skip it.** `[dropshipping assumption]` 05: with no TikTok or social footage you have nothing to build ads and pages from. Condition: before ad spend, for a seller who does not shoot its own content. For a branded brand: the gate becomes "can we demo the product on camera in under 15 seconds"; existing UGC is a plus, not a gate. Source: 05. Cards: [9651e08d5907] [cf56089fcd7c].

**R111. Influencer or creator product seeding is a demand and content method distinct from burner-account scouting (R35, P6); track whether a seeded creator's post drives sales before treating the product as validated.** `[general practice]` No library source; verify against brand data before use.

### 3.5 AI-assisted research

**R39. Let the agent do the research-heavy stages; keep humans on the decisions.** Trend scanning, review mining, pain-point clustering, sub-niche lists and first-pass concepts can be delegated. Deciding to build, calling suppliers and choosing order size stay human. AI sourcing ends at a validated, margin-checked product; it does not write ads, manage bids or fix checkout. Sources: 06, 07. Cards: [80a6973eb5c9] [33a09eb2fe9d].

**R40. Generate a long list of emotional sub-niches, then pick 5.** 06 asked Claude for sub-niches inside one market and got 30 (lower back stiffness, neck tension, plantar fasciitis), then chose 5 as the search scope for an ad-data query. The exact prompt is not in the source; build it from the inputs and outputs in P7. Source: 06. Cards: [1918017689b2].

**R41. AI concepts and mockups are stimulus, not a spec.** Combine the generated concept with ranked, cited pain points to write the real specification; never send the mockup to a factory. Source: 07. Cards: [040c099795ea] [385b53666fdd].

**R42. Search reviews for a buyer naming a price they would pay, a competitor price they found too high, or a pre-order pledge; the closest proxy to price-band fit (R75) before a live listing exists.** Source: 07. Cards: [385b53666fdd].

**R43. A brand that qualifies on active-ad volume is a candidate, not proof.** Run the revenue estimate (R49) before treating it as validation; ad volume can be budget or testing, not profit. Source: 06. Cards: [b09a0ce63306] [b37123cc93c7].

### 3.6 Demand validation

**R44. Keyword volume and social mentions size interest; they do not confirm anyone will check out at your price.** Cross-check Google Trends and the Ad Library before shortlisting. Source: 09. Cards: [3b155508fd8a].

**R45. Run Google Trends on the exact sub-niche term, on 12 months for direction and on several years for fad vs growth and seasonality.** 02: search "GLP-1 patches", not "GLP-1"; a parent term at all-time high can hide a format still on a fresh rise; 02 calls this optional and skips it when conviction is high. 09: classify growing, flat, fad or declining and plot multiple years for recurring spikes; 09 treats it as required. Strict merge: required. Sources: 02, 09. Cards: [c243c92a3b36] [989940333480] [2c09edad5b25] [52858475e05d].

**R46. Read trend and competition together.** Crowded ad library plus rising trend line is the best combination. Crowded library plus fading trend is a late entry. Empty library plus rising trend is either early or unproven; use R61. Source: 02. Cards: [989940333480].

**R47. A rising trend can reverse before inventory sells through; do not commit an MOQ order to a hero SKU on trend data alone, plan a secondary evergreen SKU (R59) before ad spend starts.** Condition: any trend-led pick; plan secondary products before the hero fades (R59). Sources: 03, 09. Cards: [2c09edad5b25] [a2e55b83f2ac].

**R48. A stable read, where search volume and unit sales hold together, supports a permanent catalog SKU; a spike with no matching sales is a signal for one limited batch, not an MOQ order or a built-out PDP.** Source: 07, from Axio's chart. Cards: [d814f1dad676].

**R49. Estimate competitor revenue before treating a competitor as proof, and apply a floor of roughly $200,000 to $300,000 a month.** 06's formula: monthly visits (SimilarWeb extension, about 3 free lookups a day) x conversion rate (baseline 2%, range 1.5 to 3.5%, lower for higher tickets) x conservative AOV from the visible offer stack. 06 states the floor 2 ways ($300K and "$200 to 300K"); use the range. 08 uses ShopHunter's estimate as directional confirmation only (example: about $90,000 in a month for a katana store), which would fail 06's floor. Condition: a single competitor used as validation. A lower estimate does not kill a product if 2 or more sellers confirm demand (R53). Sources: 06, 08. Conflict on the floor: section 7, C11. Cards: [b37123cc93c7] [c4db64af21f5].

**R50. At least 1 other seller must be moving the product and making money.** 08 makes this the primary viability filter, above "solves a problem" or "is in demand". Condition: `[dropshipping assumption]` in its strong form. For a branded brand entering a category with an owned difference, this becomes "the category has proven buyers" (R1, R3); 01 and 03 both launched where no direct competitor sold the same thing and treat 0 to 1 identical competitors as the best case (R53). Section 7, C1. Source: 08. Cards: [f966191090da].

**R51. A traffic tool showing no data for a store is ambiguous, not negative.** It usually means a new or under-5,000-visit store. Do not drop the candidate on that alone. Source: 10. Cards: [484b2d31c673].

**R52. Confirm the buyer is reachable: country, whether they buy online, shipping feasibility.** Use audience tools on a market leader's site if one exists (09 named Alexa, now discontinued; see section 11), otherwise sample social profiles and Google Trends region data. Source: 09. Cards: [adc4fca0bb7f].

### 3.7 Competition and saturation

**R53. Count advertisers on the exact product in the target market and grade with this ladder.** Green: 0 to 1 advertiser running the identical product (03: a second or third identical-product bidder "grossly" raises CPMs). Amber: 2 to 4 distinct stores active in the last 7 days (05's pass bar is under 5, stronger under 3). Red: 5 or more without a differentiation angle in hand; use R60 or drop. In a paid spy tool, 05's bar is under about 10 total stores selling it and no more than 3 "serious" (well-built, branded) ones. Stores that stopped running the product do not count. Condition: Meta Ad Library or spy tool, exact product name, one market. Sources: 03, 05. Cards: [0d441a9b8171] [b08de7f842b3] [0cdc9e5914ee] [2ee82e58c7a1].

**R54. Count competitors at the niche level as well as the exact-product level, and include substitutes.** 02: patches compete with pills, gummies and powders of the same ingredient for the same buyer. 09: include DIY, homemade and generic-commodity alternatives, searched per target country. Sources: 02, 09. Cards: [83bd19d0e69c] [989940333480] [5101fbb610a7].

**R55. Saturation proves demand; it is only actionable with a concrete unserved angle.** 05: many sellers means the market is already taught. 08: no seller reaches everyone; teeth-whitening pens kept producing new profitable entrants. 10: in a contested angle (neuropathy), go deeper on research than the field instead of leaving. Condition: you can name the avatar, geography or offer competitors are not serving (R60 to R63). Conflicts: 02 skips anything it recognizes (R22); 03 says a second identical competitor changes the economics (R58); 10 warns that crowded feeds raise CPMs (R34). Section 7, C1. Sources: 05, 08, 10. Cards: [2ad4276c7787] [f966191090da] [1c7e14118dbb].

**R56. 10 or more accounts selling the identical item is both a saturation warning and a validation signal; treat it as a short cash test, not a brand.** 08's ice-cube air cooler: seasonal, copied everywhere, still a workable summer test, judged honestly as not a long-term product. Source: 08. Cards: [f0dd2055cfb2].

**R57. A fragmented market with no leader is a possible opportunity, not proof of a gap.** 09 hedges this in its own example. Source: 09. Cards: [5101fbb610a7].

**R58. Watch competitor density as a leading indicator that a product's economics are about to change.** Meta is an auction; scarcity of bidders is what produces outsized early results. No multiplier is given. Source: 03. Cards: [0d441a9b8171].

**R59. A winning product is not a moat; build a brand around the function and add evergreen secondary products before the hero fades.** 03: the Udie secondary line (sleep tee, gown, bath hoodie) grew about 20% a year while the hero declined faster. 04: add branded packaging only after the product is proven, to defend against exact-offer undercutting. Condition: after a product is proven, not before. Sources: 03, 04. Cards: [f26d1bd56c46] [a2e55b83f2ac] [e0ad963873bc].

### 3.8 Positioning gaps and unserved avatars

**R60. List every angle competitors already run, then name the avatar none of them serve.** 03: a TENS device sold for period pain has an unserved muscle-recovery angle for ultramarathon runners. 05: a shoe dryer sold generically could target parents of muddy kids, campers or athletes with smelly shoes; a home-fitness set sold to young women could target older adults with stiff joints. 08: a clothing brand for "girlfriends of boyfriends 5 ft 8 and under". Condition: after R53 shows amber or red, or for any owned product entering a served category. The avatar must genuinely fit the product; forcing one wastes budget. Sources: 03, 05, 08. Cards: [b08de7f842b3] [c4dc84a5fa7e] [c840da78d857] [f966191090da].

**R61. The chosen angle should hold a small but nonzero share of current ad volume.** 05's example: about 10% of ads used the weight-loss framing. Literal 0% is more opportunity and more unproven-demand risk; 05 does not resolve the trade-off. Condition: angle audit. Source: 05. Cards: [c4dc84a5fa7e].

**R62. An angle pivot keeps the product and offer fixed; only the avatar and message change, and the hook, page, imagery and proof are rebuilt entirely around the new avatar.** Do not bolt the new avatar on as a secondary message. Source: 05. Cards: [c4dc84a5fa7e] [2ad4276c7787].

**R63. The offer structure is a differentiation lever you can build without copying the product.** 02: a "youth reset kit" with a bundle name, BOGO, free ebook and a named active ingredient beat a bare listing of the same commodity. 06: AOV should sit 20 to 40% above base price via upsells, up to about 50% for a one-product store. ecomOS override: no invented claims about the ingredient. Sources: 02, 06. Cards: [555bf9237f92] [3b6e3ec9a71b].

**R64. A branded or technical-sounding format or ingredient name raises perceived sophistication, independent of clinical merit.** 02: "liposomal", "NAD", patches inside a saturated pill niche. Condition: a persuasion read only. ecomOS override: any claim must be provable; do not invent efficacy. Source: 02. Cards: [4dfda20ee4eb].

**R65. Testing several avatars on one product in ad creative is 02-AVT work.** 03 launches one generic store and runs one creative per candidate avatar (muscle cramps, period pain, runners), then builds the brand around whichever wins. This folder only delivers the list of candidate avatars and the gap evidence. `[needs brand data: budget to run several angles at once]` Source: 03. Cards: [b08de7f842b3].

**R66. Change exactly 1 major variable from the category's core expectation.** 01: 2 or 3 changes at once make the product too novel; a 10x-concentrated detergent failed because it looked too small to work. Pick the single sharp contrast (everyone round, so go square) and keep everything else familiar. Condition: differentiation design for an owned product. Source: 01. Cards: [5decfc6860a7] [43675a4ef223] [9f7db76f5eee] [4bc5544141c3].

**R67. Take design and mechanics from the most distant industry, not from competitors.** 01: vase shapes became bottles, a Tokyo facade became a handwash bottle. "The further apart the dots, the more powerful the idea"; failure rises with distance. This is the sourced alternative to copying a competitor's look. Source: 01. Cards: [49e93f41ae1c] [dee369fd9467].

**R68. Name benefits, not features, and give the buyer both a self-interested and a feel-good reason.** 01: Olly relabeled melatonin as "sleep"; Method paired looks and scent (narcissism) with planet-friendly (altruism) for repeat purchase. `[web check: supplement and cosmetic claim rules per market before benefit naming]` Source: 01. Cards: [6cabb003162c] [82e20b234c02].

### 3.9 Evergreen vs trending, and seasonality

**R69. Classify every candidate as evergreen or trending before spending, and match budget and patience to the class.** 08: evergreen sells year-round and can carry a brand for years but starts slower and needs more ad iteration; trending (seasonal or a pop-culture moment) gives fast cash and is gone in about 2 to 4 weeks. 09: classify the market as growing, flat, fad or declining. Condition: always. A brand that owns inventory should default to evergreen; a trending pick is only for a seller who can exit fast. Conflict on which to prefer: section 7, C7. Sources: 08, 09. Cards: [4ff7704274e2] [2c09edad5b25].

**R70. Map seasonality across several years and plan cash and inventory around it.** Recurring monthly spikes (Christmas trees in Nov and Dec) concentrate revenue and risk; subtle spikes (January "hair rescue") are fine. 03 made about 80% of profit across 2 Black Friday months, one operator's number. Sources: 09, 08 (seasonal AC unit), 03. Cards: [52858475e05d] [f0dd2055cfb2] [7ed3cdb6425f].

**R71. Speed into a spike is an advantage in the arbitrage model and a gamble in every model.** `[dropshipping assumption]` 02 believes early entry builds ad-account history on a product (unverified) and also calls a no-history spike a gamble that can collapse and take early advertisers with it. For a branded brand: never buy MOQ inventory against a spike with no 180-day history. Source: 02. Cards: [ae35f8af0cb0] [160628e26bfe].

**R112. Map gifting and occasion demand (festivals, wedding season, Mother's Day) the same way as Christmas and Black Friday (R70); a product that spikes only on a gifting occasion needs the same cash and inventory plan as any other seasonal spike.** `[general practice]` No library source; verify against brand data before use.

### 3.10 Product attributes

**R72. Prefer consumable or renewable products, but check the real replenishment rate before assuming a subscription.** 02: renewables support subscription revenue (one store: 33% subscribed, over $5,000 a month recurring) but a $1.5M store had 0 subscribers, so this is optional. 09: a hair mask used a couple of times a year cannot carry a monthly subscription. Sources: 02, 09. Cards: [0a701d80d125] [aa365bb09a4b] [494c8db9f8ce] [480136acffdb].

**R73. Reject viral junk that rides novelty with no real value.** 05's junk: music projector, wall-mount gym bag. Winners relieve pain, hygiene, fitness or convenience problems. Source: 05. Cards: [9ffdbd6051d3].

**R74. Ask whether the novelty creates a repeat-purchase annuity or a one-time purchase.** 01: a cheese-shape stamper is a durable toy, not a consumable. Condition: format innovation on a commodity. Source: 01. Cards: [978d4e988945].

**R113. Weight lifetime value, not just AOV, when a product's repeat-purchase potential is unclear; a low-AOV item with strong repeat usage can clear the margin gate (R76) on LTV even where a single order would not.** `[general practice]` No library source; verify against brand data before use.

### 3.11 Price and unit economics

**R75. Price band ladder.** Reject at about $9.99 or below on the source platform (02: impulse price, no room for Meta acquisition cost; 05's $30 margin floor implies the same). Caution between $10 and $50 (09 flags $9 to $20 as a red flag but proceeds). Target $50 to $150 (09: "generally accepted by many top ecommerce entrepreneurs", unsourced). 02 repositions a $15 TikTok Shop item to about $29.99 with BOGO plus $4 to $5 shipping on its own store, which sits below 09's band and above 02's reject line. Condition: paid-acquisition-led launch. A low-ticket lead product is a deliberate strategy in some acquisition playbooks (02's own caveat), so treat the band as a default, not a law. `[needs brand data: current AOV and the brand's price architecture]` Sources: 02, 05, 09. Cards: [d8128fe11921] [5d466fe60646] [0a701d80d125] [cbda8eff6638] [9651e08d5907].

**R76. Margin gate: gross margin of at least $30 a unit and retail price of at least 3x landed cost, both together; $40 preferred.** 06: both rules must pass ($15 landed, $50 retail passes; a $10 item at exactly 3x fails the $30 floor, so the floor binds at low cost); 06 raised his floor from $20 to $30 as Meta costs rose. 05: $30 to $40 above supplier cost. 07: a tool's margin percentage is on product cost only. 04: net margin after ads and COGS, protected by refund control, is the real KPI. None of these include shipping, processing fees, refunds or duties, so the gate in P14 adds them. `[dropshipping assumption]` For a branded brand, replace the dollar floor with the brand record's contribution-margin target after all landed and fulfillment costs; the 3x multiple stays as a sanity check. `[needs brand data: landed cost, processing rate, refund rate, shipping per order, target contribution margin]` Sources: 04, 05, 06, 07. Cards: [cd8817fc79ec] [9651e08d5907] [a20e53fb1d99] [cac61838f02d].

**R77. Model markup at both the low and high end of the realistic price range, and separately at future bulk cost.** 09: $583 per 100 units was a concern at $9 and healthy at $20. 04: a wallet quoted at $7 new fell to $5.50 with volume; ask for re-quotes rather than assuming they come. Sources: 04, 09. Cards: [952aae634b40] [2edf05052ea4].

**R78. Do not assume you can match an established competitor's cost base.** They have negotiated better rates than a new seller. Source: 06. Cards: [cd8817fc79ec].

**R79. Set price from about 2 dozen comparable products, not from 1 competitor.** Source: 09. Cards: [cbda8eff6638].

**R80. Before scaling ad spend on strong early signal, separate a fixable operational problem (weak copy, a mispriced offer) from a structural cost problem ad spend cannot beat; scale the first, stop the category on the second.** Condition: strong qualitative signals but a hard business. If the cost inputs are outside your control, stop rather than fund harder. Sources: 01, 03. Cards: [b86bba793279] [fff4fa23ccb9].

**R114. Treat payment-gateway friction as a margin input: COD collection fees, failed-payment retry cost and prepaid-discount cost all reduce the contribution margin the margin gate (R76) checks.** `[general practice]` No library source; verify against brand data before use.

### 3.12 Logistics, durability, perishability, regulatory

**R81. Reject heavy or oversized items unless the brand's shipping economics have been priced on the carrier's site.** 05: a hard skip for dropshipping. 09: estimate packed size and weight and price a real shipment before sourcing. Strict merge: price it; reject if shipping eats a large share of the cost-to-price spread. Sources: 05, 09. Cards: [9651e08d5907] [837eb78db394].

**R82. Choose materials and packaging that survive parcel handling.** Plastic over glass; 03's glass vials broke in shipping and killed a seasoning venture. Durability is a margin and returns decision. Sources: 09, 03. Cards: [c7268fae6d38] [fff4fa23ccb9].

**R83. Shelf life must exceed the realistic time to build marketing and sell through, plus the customer's time to use a unit.** 09 judged about 3 years "more than enough" for coconut oil. Condition: perishable or degradable products. Source: 09. Cards: [646fd0db3481].

**R84. Research regulations and restrictions in every target country before any spend, especially food, cosmetics, supplements and baby products.** Covers claims, labeling, packaging copy and testing or documentation. 01's benefit-naming (melatonin as "sleep") depends on claim rules per market. 03: check registration, sizing standards, returns and payments before treating a new country as a cheap test. `[web check: current rules per category and country]` Sources: 01, 03, 09. Cards: [5f471d64cfd2] [6cabb003162c] [4643fb9dd291].

**R85. Delivery window target of 6 to 10 days; 8 to 15 acceptable early; 10 to 15 (marketplace direct) raises chargebacks.** `[dropshipping assumption]` 04: a faster 5 to 8 day line added about $3 a unit on a $13 item and is overkill unless AOV absorbs it; refunds and chargebacks can escalate to withheld payouts. For a branded brand shipping from its own 3PL, use the brand's measured delivery times and refund rate instead. `[needs brand data: delivery days and refund rate per ship-to country]` Source: 04. Cards: [c9130a31f6bd] [cac61838f02d].

**R86. Before listing a fandom-adjacent or licensed-look product, check trademark exposure with the same rigor as the country regulatory check (R84); a takedown after launch costs the ad spend and the SKU.** `[web check: trademark and licensing status of any character, brand or design element]` Source gap flagged from 08. Cards: [5be11a6e0db5].

**R115. For a mobile-first, cash-on-delivery market, price the RTO (return to origin) rate and COD collection cost into the margin gate (R76) before launch; a product with a high RTO rate can fail on delivery economics even after it clears every other check.** `[general practice]` No library source; verify against brand data before use.

**R116. Some categories need a specific certification beyond the general regulatory check (R84): jewelry needs hallmarking, electronics and toys need BIS or the destination country's safety mark, cosmetics need per-country ingredient clearance.** One example exists: 07 cites GreenGuard Gold certification on a crib product, but gives no general method. `[general practice]` No library source for a general method; verify against brand data and per-country rules before use. Source: 07. Cards: [48b21947926b].

### 3.13 SKU count and range

**R87. Launch with exactly 1 SKU; treat variants as complexity debt to add later.** 09: fewer sizes, colors and formulations mean less inventory capital, storage and shipping mix-ups. Conflict: 03 adds evergreen secondary products once the hero is proven, and 06 pushes AOV with upsells that need something to upsell. Reconcile by stage: 1 SKU to validate, range after proof. Section 7, C5. Sources: 09; 03 and 06 for the later stage. Cards: [190344a3ce52] [a2e55b83f2ac] [3b6e3ec9a71b].

### 3.14 Sourcing and suppliers

**R88. Reverse-image search the competitor's product photo to find the supplier listing and the raw cost floor.** 08: right-click, Google "Search by Image", scroll to an AliExpress or similar listing (katana at about $75 retail found at about $40; travel bag at $98 found at $16). 05: check AliExpress cost for every Reels or Ad Library find. Condition: cost check only. The listing may differ in quality and spec from the competitor's unit; shipping time and reliability need separate checks. ecomOS override: this finds the cost of a category item; the deliverable must still name an owned difference (3.17). Sources: 05, 08. Cards: [39e6f64e0acb] [ab2f47bf79d4].

**R89. Write one structured sourcing request naming OEM service, private label, an MOQ ceiling you can fund, certifications and review strength.** 07's example: "MOQ under 500". Review each profile on wholesale cost, target retail, MOQ range, margin, reorder rate and the stated match reason; separate suppliers who match the product requirement from ones who only match the category. Source: 07. Cards: [48b21947926b].

**R90. Translate consumer language into manufacturing specification before contacting suppliers.** "Quiet keyboard" becomes "5-layer internal dampening structure"; "matte paint" becomes "e-coating". 07 says vague specs invite inflated quotes; his opinion on supplier psychology, not tested. Source: 07. Cards: [2f326a2e0a04].

**R91. Vet a shortlisted supplier with 2 to 3 specific capability questions tied to the product's differentiation, by phone, regardless of platform rating.** A 4.7 rating is not proof of a good experience. Vague answers to a specific technical question mean do not scale. Source: 07. Cards: [7ce6e9e93939].

**R92. Receive a sample through the store's own fulfillment chain, not only the factory, before committing to MOQ inventory or PDP photography; a sample that fails unboxing or shelf-life kills the SKU first.** Strict merge: always. For an owned product the sample also feeds R82 (durability) and the content check (R38). Sources: 04, 07. Cards: [7ce6e9e93939] [d528b5e6c32f].

**R93. A private supplier or agent model beats marketplace-direct ordering for a no-inventory store; both are promoted by an interested party.** `[dropshipping assumption]` 04: an agent sources from 1688 and factories, stages 2 to 3 days in their warehouse, quotes from a photo or link on WhatsApp, bills per order from a pre-funded wallet, and offers branded packaging; 04 rejects AliExpress, Alibaba, CJ, AutoDS and Zendrop on cost, speed, branding and support, while earning referral bonuses from the platform he demos. 08 promotes ZenDrop on a 50% off affiliate link. Condition: no-inventory Shopify store. For a branded brand that holds stock this model does not apply; use R89 to R92 with Alibaba or a domestic manufacturer. `[web check: Team Drop, ZenDrop, AutoDS pricing and status]` Sources: 04, 08. Cards: [38cefaf4b56b] [5af9496ab626] [d528b5e6c32f] [a7e2993419b5].

**R94. Add logo, custom mailer and inserts only after the product is proven to sell.** 04's rationale: cost and complexity before proof, and a defense against exact-offer copycats after. For a branded brand where packaging is part of the product (01's Olly jar), stage it: sample-run packaging for the test, full custom packaging after the first reorder. Sources: 04, 01. Cards: [e0ad963873bc] [4bc5544141c3].

**R95. Set a reminder to re-quote every supplier once a SKU's order volume crosses a threshold (500 or 1,000 units); do not assume the landed cost in the margin gate (R76) still holds as it scales.** Source: 04. Cards: [2edf05052ea4].

**R96. Confirm a supplier surfaced by an AI agent is actually reachable on the platform it names.** 07's first shortlist was not on Alibaba until a follow-up prompt verified it. Source: 07. Cards: [48b21947926b].

**R117. For a considered-purchase category (electronics, jewelry, appliances), price warranty and after-sales support cost into the supplier brief (D3) before sourcing; a low landed cost can still fail once return and repair handling are added.** `[general practice]` No library source; verify against brand data before use.

### 3.15 Research cadence, launch sequencing and expansion order

**R97. Keep a research log and run a 3 to 3 to 1 daily funnel.** 05: log about 3 qualifying candidates a day (name, buy price, sell price, competitor pages, notes such as "heavy on TikTok, light on Meta"), narrow to the 3 strongest overall, pick 1 to test that day. Condition: a seller testing daily with cheap switching cost. `[dropshipping assumption]` A branded brand with MOQ inventory tests far fewer products; keep the log, drop the daily cadence. Source: 05. Cards: [9b3d44f6bf5b].

**R98. Product research ends at a validated product with evidence attached; creative, media and store are separate workstreams with separate owners.** Sources: 02, 06. Cards: [88ceb078bd65] [33a09eb2fe9d].

**R99. Expansion order is a choice between 3 sourced options; validate each market on its own.** Inverse order (03): Australia, then UK, then Europe, then Canada, then the US last, to be first-mover in each smaller market before the US auction saturates; Udie ended with the UK largest and the US smallest. Preconditions 03 states: product already proven in 1 market, capital for several sequential launches, a product that travels across English-speaking markets. Geo-arbitrage (05): take a product with proven US or UK ad volume into an untapped European country with localized creative. Home market first: the default 03's interviewer calls the conventional method. No source gives a metric for when a market is "proven enough" to move on. Condition: only after product-market fit in 1 market. Section 7, C3. `[needs brand data: home market, logistics and payment coverage per country]` Sources: 03, 05. Cards: [baffe12832b0] [4643fb9dd291] [687fc8ceb72a] [533302cea515].

**R100. Before entering any new country, localize creative and check duty, VAT, shipping time, sizing and compliance; they can erase the margin advantage.** Sources: 03, 05. Cards: [4643fb9dd291] [533302cea515].

**R101. Choose between 2 or 3 fully built concept directions with qualitative checks, used to guide, not to vote.** 01's sequence: build each direction with a designer, ask which one you are most excited about, show friends and family, run "consumer auditions" (qualitative groups for feedback, not A vs B votes), show retail buyers framed as "help me improve". Condition: an owned brand concept; 01 has no quantitative method at all. Conflict with data-led validation (02, 06, 08, 09): section 7, C8. Source: 01. Cards: [72f41e3a8257] [3b1fb5de42bc].

**R102. Before concluding demand is absent, try a change of presentation.** 01: milk in a bottle cap; Babybel's peelable wax with about a 3-second "time to fun". Do not over-engineer the fix. Condition: low trial or flat engagement on a product the checks said had demand. Source: 01. Cards: [1b2101d23187] [eedf2639799e].

### 3.16 Test, go or no-go, and post-test diagnosis

**R103. Run the market-level questions before the product-level questions.** Demand size, competitors, trend direction, offline availability and target customer can kill an idea before you model unit economics. Source: 09. Cards: [6d1e8d68fa75].

**R104. Score each of the 16 questions pass, caution or red flag; expect some flags; close with a written highlights and concerns list and judge each concern fixable or market-dependent.** 09 proceeded with 2 red flags (low price, fragmented competition) because both were fixable by branding and a better formula. No source gives a weighting or a count of flags that kills a product; P19 supplies ecomOS's own gate. Source: 09. Cards: [6d1e8d68fa75] [090e016603b6].

**R105. Every candidate goes through the full stack regardless of where it came from.** Competitors making money, problem or passion, demand proof, sourcing and margin, open angle, then build. 08's checklist is pass or fail with no ranking; section 9 adds a score. Source: 08. Cards: [178c6277a818] [bdee2e77e91b].

**R106. The agent may override one amber-level ecom check per product if it names the overriding number in the log; it may never override a red on the margin gate, the regulatory check, or the owned-difference requirement (O2).** Condition: the agent may override a single amber check on a named signal; it may not override a red on R76 (margin), R84 (regulatory) or 3.17. Section 7, C12. Source: 02. Cards: [5c7c5df4a96e] [cc4b1af32e18] [c243c92a3b36].

**R107. After a short paid test fails, diagnose ads and funnel before blaming the product, and only after the process was actually followed.** 02: run a Meta test about 2 to 3 days, then move on if it underperforms. 06: the product is rarely the reason; check link CPC (about $1.50 target, $2 to $4+ elevated), then CTR (3% floor, about 4% ideal, below 3% is creative), then CPM (no fixed bar, above about $80 US is high); on the funnel, landing-to-ATC of 10% or more (8 to 9% for pricier items), ATC-to-purchase of 30% or more, AOV 20 to 40% above base. These are 06's targets for US Meta traffic and belong to 04-MED and 05-WEB for the fix. Condition: a validated product with one unprofitable test. `[needs brand data: the brand's own CPA and ROAS bar]` Sources: 02, 06. Cards: [1d273c71ce53] [2b0c86c59115] [f5d6e64a0e54] [3b6e3ec9a71b].

Moved to Appendix A: R108, "if it is hard, it is probably wrong" (founder-psychology aphorism, source 01, no store framing).

Moved to Appendix A: R109, one early win is not a repeatable formula (founder-psychology aphorism, source 03, no store framing).

### 3.17 ecomOS overrides (apply above every rule in this section)

**O1. No invented claims.** Any benefit, ingredient or outcome in a proposed angle must be provable from the brand's own evidence. R63, R64 and R68 are persuasion reads, not permission to claim.

**O2. No copying competitor products, text, logos or faces.** A competitor selling item X is a demand signal for the category of X. The shortlist entry must name at least 1 owned difference (avatar, offer structure, formulation, spec, packaging, geography) before it can reach "go". Competitor video is never downloaded, remixed or reposted (overrides 05's "download and remix" step and 02's "borrow the hook" step; the hook idea can be described in words and rebuilt by 03-CRE from scratch).

**O3. Competitor ads are signals, not proven winners.** Ad count, run length and impressions show spend, not profit. Use them for layout, mood, angle and demand direction only. A competitor is "proven" only after R49 or a second independent seller.

**O4. Brand record and warehouse numbers win.** The margin floor, delivery times, refund rate, conversion rate and AOV assumptions in this playbook are placeholders until the brand's own data replaces them. Where a source's self-reported number and the brand's number disagree, the brand's number is used and the source's is noted as context.

**O5. Meta is read-only.** Research uses the Ads Library and read tools. No test is launched from this folder; the launch handoff goes to 04-MED with a written brief.

**O6. Keep brands apart, and keep public research separate from private data.** A shortlist built for one brand is not reused for another. Competitor and public tool data live in the research memo; brand economics live in the brand record.

## 4. Procedures (implementation)

Each procedure: goal, preconditions, steps, checks, rollback. "Rollback" means what to do when a check fails so no spend or reputation is lost. Platform steps carry `[verify UI]`.

### P1. Category thesis scan (boring-product method)

Goal: find a large, stagnant, high-frequency category with an open emotional or aesthetic gap, for an owned brand. Source: 01, with 03 for the trend-spotting habit.
Preconditions: the brand is willing to own a product for years; a designer or creative partner is available for P1 step 8.
1. List categories the brand could enter that are decades old, bought weekly or monthly, and need no consumer education (R1).
2. For each, walk the shelf or the top 20 search results and score the sea of sameness: same colors, same shapes, same voice, same claims (R2). Note shopper confusion signals (01 watched vitamin shoppers ask strangers what magnesium does).
3. Run the brand-recall test: ask 5 to 10 target buyers to name their top 3 brands in the category (R3). Record answers.
4. Name the cultural shift visible elsewhere that this category has missed, and write the bridging question: "what would the [reference brand] of [category] look like?" (R4).
5. Check offline availability and big-box presence (R10). Easy local availability lowers the score.
6. Decide the single variable to change: shape, color, format, benefit framing or ritual (R66). List every other deviation and park it for later line extensions.
7. Write the 2-sided reason to buy: the self-interested reason and the feel-good reason (R68).
8. Build 2 or 3 concept directions with the creative partner and run P19's qualitative pass (R101) before any spend.
Checks: at least 1 category with strong sameness and no named favorite brand; exactly 1 major variable changed; both halves of R68 present.
Rollback: if the economics check in P14 fails (input costs you cannot control, capital-intensive retail), stop the category rather than the concept (R80).

### P2. TikTok Shop screen in Kalodata or Shop Plus `[dropshipping assumption]` `[verify UI]`

Goal: a list of products trending up on TikTok Shop that are not yet saturated, with evidence attached. Source: 02.
Preconditions: Kalodata (about $80 a month) or Spy Crew Pro (about $49 a month with a Shop Plus clone) `[web check: current pricing and bundle]`; a target market language; the brand's ad platform known.
1. Open the Products tab only. Set date range to Last 30 Days. Pick 1 category (Health, Beauty and Personal Care, Women's or Men's Wear and Underwear, Home Improvement, or the brand's own category).
2. Set revenue range to $33,000 to $97,000 (R15). Set revenue source to Video only (R16). Leave the "growing" trend toggle off (02 says it hides good products). Sort revenue lowest to highest (R17).
3. First pass: look only at each row's small revenue graph. Keep flat-or-rising tails, drop straight downtrends (R18).
4. Second pass: glance at the image and drop anything you recognize as long-running (R22).
5. Open each survivor. Switch to the 180-day graph. Reject peaked-months-ago, reject flat, keep up-down-up rising, and mark a steep no-history climb as "gamble" (R18, R19).
6. Open the video list. Confirm the top video by revenue is 7 to 14 days old. Switch to last-7-days videos and confirm revenue spreads across 3 to 5 videos. Reject 90 to 95% on one old video unless the exception in R20 applies, and log the exception if used (R106).
7. Watch the top video. Reject non-target-language creative (R21).
8. Check the listing price. Reject at about $9.99 or below (R75). Check live revenue; reject at about $25,000 or more from live (R16).
9. If a category yields nothing after several pages, widen or switch the category filter before leaving the niche (R23).
10. Hand survivors to P9 (demand), P10 (competition) and P14 (economics). Record the 30-day and 180-day screenshots or figures in the log (P17).
Checks after step 6: at least 3 recent videos with revenue; top video age in days written down.
Rollback: a product that passes here and fails a 2 to 3 day Meta test is normal (R24); return to step 2 and, if the product was near the band floor, raise the floor to about $40,000 (R15).
For a branded brand: use steps 1 to 5 on the brand's own category to read format and trend, then stop; do not source the listed product.

### P3. Meta Ad Library scouting and competitor count (free) `[verify UI]`

Goal: surface direct-response advertisers and count competitors on an exact product in one market. Sources: 05, 08, 10, 02, 03.
Preconditions: target country; a keyword list (generic offers and problem terms).
1. Open the Meta Ad Library. Set country to the target market. Set to active ads.
2. Search generic offer phrases ("free shipping", "50% off", "shop now") and problem phrases ("pain relief", a symptom) (R27). Optionally limit dates to the last 1 to 2 weeks.
3. For 10's older-buyer method, switch media to Images to surface native-style static ads and read ad age (R25, R33).
4. For each interesting advertiser, open the page's About, then Page Transparency, to confirm ads are running and for how long (R25) `[verify UI]`.
5. For each candidate product, search the exact product name and count distinct stores active in the last 7 days. Grade with R53's ladder. Then search the niche term and count adjacent formats and substitutes (R54).
6. Open each competitor's store from the ad. Rate it beatable or serious (R31). Note the offer structure (R63).
7. List every angle the ads use, and write the avatars none of them serve (R60).
8. Record: advertiser, run length, active-ad count, store rating, angles, count by ladder color. Save to the log (P17).
Checks: run length and count are for the target country, not global; ads running only hours are marked "no signal".
Rollback: red count with no angle means drop or route to P12; do not proceed to P14.

### P4. Paid ad-spy scouting (Get Hooked, PP Ads, Winning Hunter) `[verify UI]`

Goal: a shortlist of proven, currently running products from a paid tool, faster than the free library. Sources: 10 (Get Hooked), 08 (PP Ads), 05 (Winning Hunter). All three tools are promoted with commercial interest; see section 12.
Preconditions: one tool subscription `[web check: current tool names, filters and pricing]`.
Get Hooked (10): set Location to the target country; Top performing on; ads per brand 4; Format Video; Status Currently running; Minimum runtime 14 days; Channel Facebook; Brand active ads more than 50 (R25, R26, R30). Try a niche category first; if results are junk, switch to manual symptom keywords (R28). Scroll for hours; this is the work.
PP Ads (08): base filter by niche or keyword; sort by Days running, longest first; 500 per page (R25, R30); skip mega-brands (R29, reversed for a branded brand); open the advertiser's site; sort their ads by impressions to study audience and copy (R32).
Winning Hunter (05): select the drop-ship ads filter; skip irrelevant categories; save qualifying ads to a list over 10 to 20 minutes a day; use the AI competitor search (called "Magic AI" in 05) on the product name to list every store running it; apply the under-10-total, at-most-3-serious bar (R53).
Common steps for every tool:
1. For each candidate, open the seller's site and check whether a near-identical item is sourceable (P15). `[dropshipping assumption]`
2. Run P3 step 5 in the free library to confirm the count in the target country.
3. Run P11 to estimate the competitor's revenue before treating it as proof (R43, R49).
4. Log the product, the ad's run length, active-ad count, the avatar and angle in words, and the store rating. Never save the ad asset for reuse (O2).
Checks: run length 14 days or more; at least 1 competitor with an estimated revenue above the floor or 2 independent sellers.
Rollback: if the tool's category filter returns repeats, switch to keywords; if nothing passes, change niche, not the thresholds.

### P5. Native widget scouting (older-buyer offers) `[web check]`

Goal: log recurring problem categories being sold to older buyers through native placements. Source: 10 only.
Preconditions: the brand serves or wants to serve 60+ buyers on Facebook `[needs brand data: audience age skew]`.
1. Open a general-interest news or weather site that carries a "paid content" block (10 named weather.com and CNN) `[web check: still true and which vendor]`.
2. Refresh the block repeatedly and log every product and problem that recurs (10's list: neuropathy, tinnitus, bladder incontinence, hearing aids, snoring and sleep apnea, neck, hip and knee pain).
3. Rate each problem on severity and privacy sensitivity separately from how good the product looks (R5).
4. Run a traffic estimate on the advertiser's store; treat "no data" as new or small, not dead (R51).
5. Validate in the Ad Library with the Images filter and a 1-week-plus run length (P3 step 3).
6. Mine the longest-running ad for avatar and angle in words (R32).
Checks: problem is felt daily; product is not in big-box retail (R10).
Rollback: if the Ad Library shows many long-running advertisers on the same angle, either go deeper on research than the field (10) or drop; record the choice.

### P6. Organic feed training (TikTok, Instagram Reels) `[verify UI]`

Goal: cheap discovery of products being pushed to consumers right now. Sources: 08, 05. Counter-view from 10 (R35).
Preconditions: a fresh account per platform used only for research.
1. TikTok (08): watch fully and like every product-pitch video; keep scrolling until the feed is mostly pitches.
2. Instagram (05): search #winningproduct, like 5 to 10 physical-product videos, switch to Reels, keep liking qualifying videos; use mobile; run short sessions often.
3. When a product catches the eye and meets R5, stop scrolling (R37).
4. Open the creator's profile and count videos over 1,000,000 views; require at least 3 (R36).
5. Search the product term on the platform to find other sellers; note likes and view counts.
6. Check AliExpress or the supplier cost (P15) and log the candidate (P17).
7. Route to P9, P10 and P11.
Checks: the feed has not drifted (05 warns it does); the candidate passed R36.
Rollback: if 2 weeks of sessions produce only reposts (10's complaint), switch to P3 or P4.

### P7. AI-assisted market to problem to product (Claude plus an ad-data connector) `[verify UI]`

Goal: a validated candidate from a market and an emotional problem, using Claude with an ad-library aggregator connected over MCP. Source: 06.
Preconditions: Claude access; an ad-data tool with an MCP endpoint (06 used Get Hooked on a free trial) `[web check: tool exists, pricing, MCP still offered]`; SimilarWeb extension for P11.
1. Pick a market from 06's list without overthinking: pet, weight loss, hair growth, cosmetic or any clear before-and-after, supplements, beauty, health and wellness (06 calls supplements "great" and "challenging" in the same breath).
2. Ask Claude for a list of emotional sub-niches for a DTC beginner brand in that market. 06's prompt is not in the source; write your own that asks for about 30 sub-niches, each stated as a felt problem with who feels it and when. Pick 5 (R40).
3. Connect the ad-data tool: in the tool, open the account menu, AI and MCP, copy the MCP server URL and OAuth Client ID; in Claude, Customize, Connectors, add custom connector, paste both (06's steps, high decay) `[verify UI]`.
4. Run one sourcing prompt that gives Claude: how to use the connector, the research process (find brands with enough active ads in each sub-niche; for each, return product, pain point, ad pattern, funnel type such as PDP vs advertorial, and the top ad), and the 5 sub-niches (R43). Expect a few minutes.
5. For each qualifying brand, run P11 (revenue estimate) and P14 (margin).
6. Treat funnel architecture in the output as intelligence about where competitors send traffic; hand it to 05-WEB.
Checks: every candidate has a revenue estimate and a margin check, not just an ad count.
Rollback: if the connector fails or the tool is gone, run P3 and P4 manually with the 5 sub-niches as keywords.

### P8. Alibaba Axio agent workflow (trend to supplier shortlist) `[verify UI]`

Goal: from a category trend to a spec, a supplier shortlist and an RFQ draft, for an owned or private-label product. Source: 07, a single first-time demo; free at recording `[web check: Axio availability, pricing, country access]`.
Preconditions: a category; a first-order budget and MOQ ceiling `[needs brand data]`.
1. Trend prompt: "analyze current market trends in [category] and identify what is gaining traction". Read the chart of search volume vs sales count; keep pairs that move together (R48).
2. Drill into named sub-variations, not the category. Read the average Amazon rating; flag about 3.8 or below as a quality gap (R7). Open the positive and negative tag breakdown.
3. Pain-point prompt: "Analyze [category] and list the top 10 unmet customer pain points with proof from reviews, forums and Amazon Q&A. Cluster by theme and rank by urgency and willingness to pay." Name the relevant forums (07: Reddit and Geekhack for keyboards) (R42).
4. Open the cited sources and confirm each is specific and real (R8, R41).
5. Concept prompt: category plus narrow audience plus trend (07: "mechanical keyboard company for Gen Z women, cozy gaming"). Ask for brand identity, product concept and roadmap together. Treat visuals as stimulus (R41).
6. Sourcing prompt: "Find manufacturers offering high quality [product] with OEM service, private label, MOQ under [N], official certifications and strong reviews" (R89). Ask the agent to verify each supplier is reachable on Alibaba (R96).
7. Translate the ranked pain points into manufacturing terms and ask the agent to draft the RFQ (R90). Do not send from inside the tool without human review.
8. Continue in P16.
Checks: cited pain points opened and confirmed; suppliers verified on platform; margin from the tool re-computed with freight, fees, returns and ad cost (R76).
Rollback: if the tool's trend claims do not match live Amazon listings `[web check]`, discard that run.

### P9. Demand check

Goal: confirm demand is real, rising and durable for the exact product term. Sources: 09, 02, 07.
Preconditions: a specific product idea and its exact sub-niche term.
1. Google Keyword Planner: monthly search volume for the core keywords. BuzzSumo or a current equivalent: daily social mentions (09's example: about 73,000 searches and about 150 tweets a day, example only) (R44) `[verify UI]`.
2. Google Trends, exact sub-niche term, 12 months: require an active current uptrend (R45).
3. Google Trends, same term, 5 years: classify growing, flat, fad or declining; mark recurring monthly spikes as seasonality (R45, R70).
4. Where available, compare search volume and sales count over time (R48).
5. Check offline availability by searching local retailers per target country (R10).
6. Profile the buyer: country (Trends region data), gender and age (sample social profiles), buys online or not (R52).
7. Write the demand verdict: pass, caution or red flag, with the numbers.
Checks: the term is the sub-niche, not the parent; the multi-year read was done, not just 12 months.
Rollback: a declining or fad read stops the candidate unless it is explicitly a trending cash test (R69).

### P10. Competition and saturation check

Goal: a graded read of how contested the product is and whether an open angle exists. Sources: 03, 05, 02, 08, 09, 10.
1. Run P3 steps 5 to 7 for the exact product and the niche (R53, R54).
2. Include substitutes and DIY alternatives per target country (R54).
3. Apply the familiarity test: if the researcher recognizes the product as long-running, note "saturated by recall" (R22).
4. Count distinct accounts selling the identical item on the discovery platform; 10 or more is heavy saturation and cash-test-only (R56).
5. Read trend and competition together (R46): crowded plus rising, crowded plus fading, empty plus rising.
6. If amber or red, run P12 for an angle. If a fragmented market with no leader, mark "possible opportunity, unproven" (R57).
7. Write the competition verdict with the ladder color and the angle status.
Checks: counts are per target country; stopped ads excluded.
Rollback: red with no angle is a no-go for an owned product; for a dropshipping cash test it may still run under R56 with a fixed budget and no brand build.

### P11. Competitor revenue estimate

Goal: decide whether a competitor is proof of a viable product. Sources: 06, 08.
1. Install the SimilarWeb extension (about 3 free lookups a day at the time of 06) `[web check: current free tier]`. Read the competitor's estimated monthly visits; take the conservative figure.
2. Choose a conversion rate: 2% baseline, 1.5 to 3.5% range, lower for higher tickets (R49).
3. Estimate AOV from the visible offer stack conservatively.
4. Compute orders = visits x rate; revenue = orders x AOV. 06's example: 1.5M x 2% = 30,000 orders x $90 = about $2.7M a month.
5. Optionally run the store URL through a spy estimator such as ShopHunter (08, affiliate-promoted) for a second directional figure, and search the same tool for other stores on the product.
6. Apply the floor: roughly $200,000 to $300,000 a month for a single competitor to count as proof (R49). Below the floor, require a second independent seller.
Checks: the traffic figure is monthly, not daily; the AOV is not the single-item price.
Rollback: no traffic data is ambiguous (R51), not a fail; find a second seller.

### P12. Positioning gap and angle audit

Goal: name an avatar or angle competitors do not serve, with evidence. Sources: 03, 05, 08, 10.
Preconditions: P10 returned amber or red, or the brand owns a product entering a served category.
1. Confirm the product passes the baseline screen first (R5, R75, R76, R81); pivot after screening, not instead of it.
2. Catalogue the audiences and outcomes in every competitor ad and page (P3 step 7).
3. Write what none or few of the ads say: which customer type, life stage or outcome is absent.
4. List 3 to 5 alternative avatars the product genuinely fits (R60). Reject forced fits.
5. Estimate each avatar's share of current ad volume; prefer a small nonzero share, about 10% (R61); flag 0% as "unproven".
6. For each avatar, mine the longest-running competitor ad for the message frame in words only (R32, O2).
7. Write the angle brief: avatar, situation, before-to-after benefit the brand can prove (O1), the offer structure (R63), and what changes on page and creative (R62). Hand candidate avatars to 02-AVT for testing (R65).
Checks: each avatar has a stated reason the product fits; no claim without brand evidence.
Rollback: if no avatar fits, the product is a no-go for this brand regardless of demand.

### P13. The 16-question validation pass

Goal: a scored, written go or no-go memo on one specific product before sourcing spend. Source: 09, ordering from R103.
Preconditions: one product, not a category; results of P9 to P12 at hand.
Market level:
1. Market size and demand (Keyword Planner volume, social mentions). Score pass, caution or red.
2. Competitors, including DIY and commodity substitutes, per target country.
3. Market direction: growing, flat, fad, declining.
4. Local and offline availability.
5. Target customer: who, where, buys online?
Product level:
6. Selling price from about 2 dozen comparables vs the $50 to $150 band (R75, R79).
7. Markup at low and high price, all-in cost for a small first run, and future bulk cost (R77).
8. SKU count: default 1 (R87).
9. Subscription fit from real usage frequency (R72).
10. Size and weight priced on the carrier site (R81).
11. Durability of product and packaging (R82).
12. Seasonality across years (R70).
13. Pain, passion, both, or nice-to-have (R5).
14. Consumable or disposable (R72).
15. Shelf life vs ramp time (R83).
16. Regulations and restrictions per country and category (R84).
Close-out:
17. Write highlights and concerns. For each concern, state fixable (branding, positioning, formulation, packaging) or market-dependent (R104).
18. Apply the ecomOS gate in P19.
Checks: every question has a score and a number or a source; no question skipped as "obvious".
Rollback: any red on 16 (regulatory) or on P14's gate stops the product until resolved.

### P14. Unit economics gate

Goal: confirm the product can pay for acquisition and fulfillment at the planned price. Sources: 06, 05, 09, 07, 04, plus O4.
1. Landed cost: product cost plus freight to you plus duty; for dropshipping, the supplier's quote plus the shipping line to the customer (R76, R85).
2. Fulfillment costs: pick and pack, packaging, outbound shipping per order (from the warehouse or the brand's 3PL) `[needs brand data]`.
3. Payment processing rate and refund rate from the brand's own history `[needs brand data]`.
4. Retail price from P13 step 6.
5. Gross margin = price minus landed cost. Gate 1: at least $30 ($40 preferred). Gate 2: price at least 3x landed cost. Both must pass (R76).
6. Contribution margin = price minus landed, fulfillment, processing and expected refunds. Gate 3: at or above the brand record's contribution target `[needs brand data]`. Where the brand has no target yet, state the assumption and mark the memo "provisional".
7. Ad cost headroom: contribution margin minus the brand's historical CPA for similar products; must be positive `[needs brand data: CPA history]`.
8. Repeat step 5 to 7 at the low and high end of the price range and at bulk cost (R77).
9. Record 07's caveat that any tool's margin percentage excludes freight, fees, returns, ads and licensing.
Checks: no source's example margin ($25 to $80, $40 to $120, $15 to $50) is used as the brand's number.
Rollback: if only the top of the price range passes, verify buyers pay that price (09) before sourcing; if nothing passes, drop the product or change the offer (bundle, AOV) and re-run.

### P15. Reverse-image sourcing and supplier quote

Goal: find the supplier cost floor and 2 or 3 candidate suppliers for a category item. Sources: 08, 04, 05, 07.
1. Right-click the product image from a competitor's ad or page, run Google "Search by Image", scroll to an AliExpress, Alibaba or 1688 listing (R88) `[verify UI]`.
2. Record the listing price, MOQ, variants and shipping options; note where the listing's spec may differ from the competitor's unit.
3. For a dropshipping store with an agent (04): send the photo or link to the agent on WhatsApp, receive a quote and shipping-line options per country; compare cost and delivery days (R85, R93) `[dropshipping assumption]`.
4. For an owned or private-label product: run P8 step 6 or search Alibaba directly with the structured request (R89); shortlist 2 or 3 verified manufacturers.
5. Ask for the quote at the first-order quantity and at a volume tier (R77, R95).
6. Write the supplier brief (section 9) with the cost floor, MOQ, lead time, shipping options and the owned difference the brand will add (O2).
Checks: the cost is at the quantity you will actually order, not a 10,000-unit tier (R78).
Rollback: if no listing matches, treat the product as custom-made and route to P8.

### P16. Supplier vetting and sample order

Goal: confirm a supplier can make the differentiated spec before any volume commitment. Sources: 07, 04.
1. Translate the 2 to 3 defining features into manufacturing terms (R90).
2. Send the RFQ with spec, customization, delivery terms and target quantity.
3. Call each shortlisted supplier and ask the 2 to 3 capability questions; rate answers specific or vague (R91).
4. Order a sample; for a first production run, about 50 units, never thousands (R92).
5. Test the sample for durability, packaging survival, and on-camera demo (R82, R38).
6. For a dropshipping agent: confirm which warehouse produces the better-quality version and which shipping line hits 6 to 10 days to each target country (R85).
7. Only after sales are proven, add branded packaging and link it to the product in the platform (R94) `[verify UI]`.
Checks: sample matches spec; delivery days measured on the sample shipment.
Rollback: vague answers or a failed sample drop the supplier, not the product; return to P15 step 4.

### P17. Research log and selection funnel

Goal: a single artifact that records every candidate and decision. Source: 05, adapted.
1. One sheet with columns: date, product, source method (P1 to P8), buy price, sell price, gross margin, 30-day and 180-day read, top video age, competitor count and color, revenue estimate, angle status, evergreen or trending, notes.
2. Add about 3 qualifying candidates a day when in active hunting mode (R97) `[dropshipping assumption]`; a branded brand logs whatever P1 to P8 produce.
3. Weekly: narrow to the 3 strongest overall by margin, clarity of problem and weakest competition; pick 1 for the validation memo (P13).
4. Record every rule override with the overriding signal (R106).
Checks: every row has a source method and a next step.
Rollback: none; the log is the audit trail.

### P18. Launch sequence and international expansion plan

Goal: the order in which markets are entered, with the checks per market. Sources: 03, 05.
Preconditions: the product has proven demand and economics in at least 1 market (03's stated precondition); capital for sequential launches `[needs brand data]`.
1. Pick the sequence option and write why: inverse (AU, UK, EU, CA, US), geo-arbitrage into an untapped market, or home market first (R99). See section 7, C3 for how to choose.
2. For each market in order: validate demand independently (P9 with region data), count competitors in that country (P10), price a shipment and delivery days (R81, R85), check duty, VAT, sizing, returns and regulatory registration (R100, R84), localize creative and copy (R100).
3. Define the "proven enough to move on" metric yourself; no source gives one. Suggested placeholder until the brand sets its own: the brand's CPA bar met for 4 consecutive weeks at planned spend `[needs brand data]`.
4. Plan secondary evergreen products before the hero product's trend fades (R59).
5. Write the plan (section 9) with dates, markets, gates and the go or no-go owner.
Checks: no market is entered on spillover assumptions from the last one.
Rollback: if a market fails its own validation, pause that market, do not reorder the whole plan.

### P19. Go or no-go decision

Goal: a single, defensible decision with the evidence attached. Sources: 09 (memo), 08 (stack), 01 (qualitative pass), plus ecomOS gates.
1. Confirm the full stack ran: P9, P10, P11 (or 2 independent sellers), P12 if needed, P13, P14, P15 (R105).
2. Hard stops (no override): red on P14 gate 1 or 2; red on regulatory (R84); no owned difference named (O2); any claim the brand cannot prove (O1).
3. Amber checks may be overridden once each, with the signal named and logged (R106).
4. For an owned brand concept, run 01's qualitative pass: which direction the team is most excited by, friends and family reaction, consumer auditions for feedback, retail buyer reaction framed as "help me improve" (R101). Record it as input, not as the decision.
5. Write the validation memo (section 9) with the score, the highlights and concerns, the fixable vs market-dependent judgment, the decision and the next owner (04-MED for a test brief, 06-OPS for a purchase order).
6. Set the post-test review: 2 to 3 days after launch for a dropshipping Meta test (R107), or the brand's own review window.
Checks: every number in the memo has a source or a brand-record reference.
Rollback: a "go" that fails its first test goes to P20, not straight to "no".

### P20. Post-test diagnosis

Goal: decide whether a failed test means a bad product or a bad ad or funnel. Sources: 06, 02.
Preconditions: P19 was actually followed; 1 unprofitable test of 2 to 3 days (dropshipping) or the brand's window.
1. Ads first: link CPC near $1.50 is fine, $2 to $4+ is elevated (US, 06). CTR below 3% means creative. If CTR is 4 to 5% and CPC still high, read CPM; above about $80 US is high with no firm line (R107). Route creative to 03-CRE and bidding to 04-MED.
2. Funnel second: landing-to-ATC under 10% (8 to 9% for pricier items) means offer, page or traffic; ATC-to-purchase under 30% means checkout or payment approval, fix by removing steps; AOV under 20 to 40% over base means missing upsells. Route to 05-WEB.
3. Only if ads and funnel are within range does the product go back to P13 and P12 for a re-read (a new avatar, a changed presentation per R102, or a no-go).
4. Log the outcome and recalibrate thresholds (R15) in the log.
Checks: the brand's own CPA and ROAS bar is used, not 06's numbers `[needs brand data]`.
Rollback: none; this is the rollback for P19.

## 5. Diagnostic checklists

Each row: what to check | how | good | bad | fix | source. A worker runs the rows in order and stops at the first hard fail unless the row says "caution".

### 5.1 Idea screen (run on every candidate from any method, before any tool time)

| What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Solves a felt problem or serves a passionate community | Write the problem in 1 sentence and who feels it, how often | Daily or chronic pain, or a clearly passionate community | Nice-to-have, novelty, occasional use | Drop, or find the daily-pain avatar (P12) | 10, 06, 05, 02, 09, 08 |
| Real value vs viral junk | Would the buyer use it a month later? | Relieves pain, hygiene, fitness, convenience | Music projector class of product | Drop | 05 |
| Business model fit | Consumable or renewable? Real usage frequency? | Repeat purchase possible, or a one-off with volume | Consumable but used twice a year and pitched as monthly subscription | Keep as one-off, no subscription claim | 02, 09 |
| Offline scarcity | Search local retail and big-box per target country | Scarce offline | On the grocery or big-box shelf | Caution; needs a strong owned difference | 09, 10 |
| Not personally chosen | Was it picked because the founder likes it? | Picked from demand evidence | "I'd buy it" is the only reason | Run P9 before spending more time | 05, 03 |
| Weight and size | Packed dimensions; price on carrier site | Small parcel | Heavy or oversized | Drop for dropshipping; price the shipping and re-run P14 for owned | 05, 09 |
| Content exists or can be made | Search TikTok for the product; can it be demoed in 15 seconds? | Plenty of footage, or easy demo | No footage and no demo | Drop for dropshipping; plan a shoot for owned | 05 |
| Customization | Does the buyer personalize it? | Plus for TikTok appeal, only if fulfillment can handle it | Custom item with no fulfillment plan | Caution; confirm with 3PL | 08 |
| Fandom or licensed elements | Any character, brand or design owned by someone? | None | Present | `[web check: trademark]` before shortlisting | gap flagged in 08 |
| Log it | Row in the research sheet with source method | Logged | Not logged | Log before further work | 05 |

### 5.2 Demand check

| What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| 30-day trend on TikTok Shop (if used) | Kalodata product graph | Flat or rising tail | Straight down | Skip | 02 |
| 180-day trend | Kalodata product detail `[verify UI]` | Up overall, or up-down-up rising | Peaked months ago, flat, or steep no-history spike | Skip; mark spike as gamble | 02 |
| Revenue band | Last 30 days, video only | $33K to $97K | Above $300K, or live 25K+ | Skip; recalibrate band from tests | 02 |
| Video recency and spread | Last-7-days video list | Top video 7 to 14 days old, 3 to 5 videos with revenue | 90 to 95% on one old video | Skip unless the exception is logged | 02 |
| Creative language | Watch top video | Target market language | Other language | Skip for this market | 02 |
| Creator not a fluke (organic finds) | Count videos over 1M views on profile | 3 or more | Fewer than 3 | Keep scrolling | 08 |
| Search volume and mentions | Keyword Planner, mention tool | Volume plus steady chatter | Low volume or no purchase intent | Caution; cross-check Trends | 09 |
| Exact sub-niche trend, 12 months | Google Trends, exact term | Active uptrend | Flat, falling, stale peak | Deprioritize | 02, 09 |
| Multi-year direction | Google Trends, 5 years | Growing, or stable | Fad spike, decline | Drop unless cash test | 09 |
| Seasonality | Multi-year monthly spikes | Mild or plannable | Extreme concentration | Plan cash and inventory, or drop | 09, 08 |
| Volume vs sales | Axio or equivalent chart | Move together and hold | Volume without sales | Look at sub-variations | 07 |
| Quality gap (owned product) | Average Amazon rating of sub-niche | About 3.8 or below with demand | Already high | Gap argument does not apply | 07 |
| Buyer reachable | Trends region, social sampling | Country, online buying and shipping confirmed | Unknown or unshippable | Fix logistics first | 09 |

### 5.3 Competition check

| What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Exact-product advertisers, target country | Ad Library, last 7 days active | 0 to 1 (green), 2 to 4 (amber) | 5 or more with no angle | P12 or drop | 03, 05 |
| Spy-tool store count | Winning Hunter or similar | Under 10 total, at most 3 serious | 10+ or 4+ serious | P12 or drop | 05 |
| Niche-level competitors and substitutes | Search the niche term; include DIY and commodity | Few adjacent formats | Every format crowded | Position against the format, or drop | 02, 09 |
| Competitor run length | Page Transparency, spy tool | 14 days or more running | Hours old | Mark "no signal", watch | 10, 08, 02 |
| Competitor active-ad count | Tool or Ad Library | 50+ shows budget and confidence | Handful | Neither proves profit; run 5.3 revenue row | 10, 06, 08 |
| Competitor revenue | SimilarWeb formula, ShopHunter | Roughly $200K to $300K a month or 2 independent sellers | Below floor and only 1 seller | Find a second seller or drop | 06, 08 |
| Competitor store quality | Open the store | Generic template, weak offer | Polished, branded, strong bundle | Count as serious | 05, 02 |
| Trend plus competition | Combine 5.2 and this table | Crowded and rising, or open and rising | Crowded and fading | Late entry; drop | 02 |
| Familiarity | Researcher's recall | Unfamiliar | Recognized as long-running | Saturated by recall; needs an angle | 02 |
| Identical sellers on discovery platform | Count accounts | Under 10 | 10 or more | Cash test only, no brand | 08 |
| Open angle | List every angle in competitor ads | An avatar with about 10% share or a describable gap | All avatars served | Drop for this brand | 05, 03, 08 |
| Offer gap | Compare bundles, BOGO, named ingredients | Competitors run bare listings | Strong bundles everywhere | Build the offer from the brand's provable benefits | 02, 06 |

### 5.4 Unit economics gate

| What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Source platform price | Listing price | Above $10 | About $9.99 or below | Reject | 02, 05 |
| Retail price band | About 2 dozen comparables | $50 to $150 | $10 to $50 | Caution; needs branding or AOV plan | 09 |
| Gross margin per unit | Price minus landed cost | $30 or more, $40 preferred | Under $30 | Raise price, bundle, or drop | 06, 05 |
| Price to landed cost | Ratio | 3x or more | Under 3x | Re-source or drop | 06 |
| Both margin gates together | Check both | Both pass | One passes | Fail (the $30 floor binds at low cost) | 06 |
| Contribution after fulfillment, processing, refunds | Brand record numbers | At or above brand target | Below | Fix offer or drop; memo "provisional" if no target | O4, 04, 07 |
| CPA headroom | Contribution minus historical CPA | Positive | Negative | Not launchable at planned price | O4 |
| Markup at low and high price and at bulk | 3 calculations | Healthy at the low end | Only works at the top | Verify buyers pay the top price | 09, 04 |
| Competitor cost assumption | Compare quotes | Own quote used | Competitor's assumed cost used | Re-quote at own volume | 06 |
| Shipping share of spread | Carrier price | Small share | Large share | Raise price, shrink format, drop | 09 |
| Delivery window (dropshipping) | Supplier line | 6 to 10 days | 10 to 15 or more | Faster line if AOV absorbs about $3 a unit | 04 |
| Durability | Sample drop and transit test | Survives | Breaks (glass) | Change material | 09, 03 |
| Shelf life vs ramp | Compare months | Comfortably longer | Shorter than ramp | Drop or shorten ramp | 09 |
| Regulatory per country and category | `[web check]` | Cleared | Claims, labeling or testing blockers | Hard stop until resolved | 09, 01, 03 |
| Structural economics | Inputs you cannot control (commodity prices, leases, capital) | Manageable | Business can't reach profit under normal volatility | Stop the category | 01 |

### 5.5 Supplier check

| What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Cost floor found | Reverse image to AliExpress, Alibaba, 1688 | Listing found, price and MOQ read | Nothing matches | Treat as custom; P8 | 08, 05 |
| Quote at real order size | Ask at first-order quantity and a volume tier | Both quotes in hand | Only a large-tier quote | Re-ask | 04, 06 |
| Supplier reachable on platform | Verify listing exists | Confirmed | AI shortlist not on the platform | Ask for alternates | 07 |
| Spec in manufacturing terms | RFQ text | Named structures, coatings, materials | Consumer adjectives | Rewrite RFQ | 07 |
| Capability questions | Phone call, 2 to 3 questions | Specific answers | Vague | Drop supplier | 07 |
| Platform rating | Read but do not rely on | Rating plus a good call | Rating alone | Call anyway | 07 |
| Sample | Order 1 sample, then about 50 units | Matches spec, survives transit, demoable | Fails any | Drop supplier, keep product | 07, 04 |
| Warehouse quality (agent model) | Ask which warehouse makes the better version | Named | Unknown | Ask before scaling | 04 |
| Shipping line per country | Compare cost and days | 6 to 10 days at acceptable cost | Only slow or only costly | Re-price or change agent | 04 |
| Branding timing | Custom packaging only after sales | Staged | Custom mailers before proof | Defer | 04 |
| Re-quote cadence | Calendar reminder | Asked as volume grows | Assumed automatic | Ask | 04 |
| Commercial interest of the recommender | Who promoted this supplier or platform? | Independent | Affiliate or referral | Compare 2 alternatives `[web check]` | 04, 08 |

### 5.6 Launch readiness

| What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Full stack ran | P9 to P15 recorded in the log | All present | Any missing | Run it | 08 |
| Hard stops clear | P14 gates 1 and 2, regulatory, owned difference, provable claims | All clear | Any red | No-go until fixed | O1, O2, 06, 09 |
| Overrides logged | Each override names its signal | Logged | Silent overrides | Log or revert | 02 |
| Evergreen or trending decided | Written class with budget and patience | Matched | Trending pick with brand build plan | Cut the brand build; cash test | 08 |
| SKU count | Launch list | 1 | Several variants | Defer variants | 09 |
| First market chosen and validated alone | P18 step 2 done for that market | Done | Assumed from another market | Validate | 03 |
| Localization, duty, VAT, shipping days for that market | Checked | Done | Missing | Do before spend | 05, 03 |
| Offer and AOV plan | Bundle or upsell defined from provable benefits | AOV 20 to 40% over base planned | Bare single item | Build the offer | 06, 02 |
| Angle brief handed to 02-AVT and 03-CRE | Avatar, situation, benefit, offer, in words | Delivered | Competitor asset attached | Remove asset; describe in words | O2, 10 |
| Test window and review set | Date and metric owner | Set (2 to 3 days dropshipping, or brand window) | None | Set | 02, 06 |
| Secondary product plan (owned brand) | Named evergreen follow-ons | Listed | None | Draft before hero fades | 03 |
| Post-test diagnosis owner | P20 assigned | Assigned | Unassigned | Assign | 06 |

## 6. Thresholds and benchmarks

Confidence: "3 sources" means 3 mini playbooks state it independently; "1 operator" means one presenter's personal heuristic; "unsourced" means the source attributes it to no one; "example" means a worked figure, not a target. Every number is a placeholder until the brand's own data replaces it (O4).

| Threshold | Value | Condition | Source | Confidence |
|---|---|---|---|---|
| TikTok Shop revenue band | $33K to $97K per 30 days | Kalodata screen, video revenue only | 02 | 1 operator, self-adjusted live to $36K to $70K |
| Revenue ceiling to avoid | $300K to $1M+ a month | Hyper-competitive | 02 | 1 operator |
| Band recalibration | Raise floor to about $40K after an unprofitable low-band test | Retest | 02 | 1 operator |
| Live revenue reject | About $25K or more from live | TikTok Shop | 02 | 1 operator |
| Top video age | 7 to 14 days | TikTok Shop video list | 02 | 1 operator |
| Video spread | 3 to 5 recent videos with revenue | TikTok Shop | 02 | 1 operator |
| Concentration reject | 90 to 95% on one old video | TikTok Shop | 02 | 1 operator, with a stated exception |
| Source-platform price reject | About $9.99 or below | Dropshipping to Meta | 02, 05 (implied) | 1 operator plus 1 implied |
| Retail price band | $50 to $150 | Paid-acquisition launch | 09 | unsourced industry claim |
| Below-band caution | $9 to $20 flagged, not rejected | 09's example | 09 | example |
| Reposition example | $15 TikTok item to $29.99 plus BOGO plus $4 to $5 shipping | Meta store | 02 | example |
| Gross margin floor | $30 a unit; $40 preferred | Every candidate | 06, 05 | 2 sources (06 raised from $20) |
| Price to landed cost | 3x or more | With the $30 floor | 06 | 1 operator |
| Comparable products to price against | About 2 dozen | Price setting | 09 | 1 operator |
| Competitor revenue floor | Roughly $200K to $300K a month | Single competitor as proof | 06 | 1 operator, stated 2 ways |
| Conversion rate assumption | 2% baseline, 1.5 to 3.5% | SimilarWeb formula | 06 | 1 operator |
| SimilarWeb free tier | About 3 lookups a day | Free extension | 06 | 1 operator `[web check]` |
| Ad Library competitor ladder | 0 to 1 green; 2 to 4 amber; 5+ red | Exact product, last 7 days, one country | 03, 05 | 2 sources merged (03: 2+ raises CPMs; 05: under 5 pass, under 3 strong) |
| Spy-tool store count | Under 10 total, at most 3 serious | Winning Hunter | 05 | 1 operator |
| Heavy saturation | 10+ accounts selling the identical item | Discovery platform | 08 | 1 operator |
| Minimum ad runtime | 14 days (spy tool); more than 1 week (Ad Library) | Profitability proxy | 10, 08 | 2 sources on direction, 1 on the number |
| Brand active ads filter | More than 50 | Get Hooked | 10 | 1 operator |
| Ads per brand cap | 4 | Get Hooked | 10 | 1 operator |
| Results per page | 500 | PP Ads | 08 | 1 operator |
| Creator not a fluke | 3+ videos over 1,000,000 views | Organic finds | 08 | 1 operator |
| Reels seed likes | 5 to 10 | Instagram feed training | 05 | 1 operator |
| Angle share | About 10% of current ad volume | Angle pivot | 05 | 1 example |
| Sub-niche list | About 30 generated, 5 chosen | Claude workflow | 06 | 1 operator |
| Amazon rating gap | About 3.8 or below | Owned-product gap | 07 | 1 demo |
| MOQ ceiling example | Under 500 | Sourcing prompt | 07 | example |
| Trial order | About 50 units, not 5,000 | New supplier | 07 | 1 demo |
| Delivery window | 6 to 10 days target; 8 to 15 acceptable; 10 to 15 marketplace-direct | Dropshipping to US | 04 | 1 operator, affiliate-promoted |
| Faster-line surcharge | About $3 a unit on a $13 item | 5 to 8 days vs 8 to 15 | 04 | example |
| Volume quote drop | $7 to $5.50 a unit | With order history | 04 | example |
| Warehouse staging | 2 to 3 days | Agent model | 04 | 1 operator |
| Trending lifespan | 2 to 4 weeks | Trending class | 08 | 1 operator, "a few weeks" in transcript |
| Daily research funnel | 3 logged, 3 favorites, 1 tested | Daily dropshipping cadence | 05 | 1 operator |
| Claimed hit rate | 3 to 5 winners a week; about 1 in 2 tests | After angle pivoting | 05 | unverified self-report; not a target |
| Meta test window | 2 to 3 days | Dropshipping test | 02 | 1 operator; 04-MED owns it |
| Ad variants prepared | 5 to 8 | Per test | 02 | 1 operator; 03-CRE owns it |
| Link CPC (US) | About $1.50 target; $2 to $4+ elevated | Post-test diagnosis | 06 | 1 operator; 04-MED |
| CTR | 3% floor, about 4% ideal | Post-test | 06 | 1 operator |
| CPM (US) | Above about $80 high, no firm line | Post-test | 06 | 1 operator, self-described non-KPI |
| Landing to ATC | 10%+, 8 to 9% for pricier | Post-test funnel | 06 | 1 operator; 05-WEB |
| ATC to purchase | 30%+ | Post-test funnel | 06 | 1 operator |
| AOV over base price | 20 to 40%; about 50% one-product store | Offer design | 06 | 1 operator |
| SKU count at launch | 1 | Owned product | 09 | 1 source |
| Shelf life example | About 3 years judged enough | Coconut oil | 09 | example |
| One-iteration rule | Change exactly 1 variable | Owned product design | 01 | 1 founder |
| Brand recall test | Top 3 brands named | Category white space | 01 | 1 founder |
| Expansion order | AU, UK, EU, CA, US | Proven product, capital for sequence | 03 | 1 operator; result was UK largest, US smallest |
| Trained eye for burner scouting | 3 to 6 months | Burner methods | 10 | 1 operator opinion |
| Black Friday share of profit | About 80% across 2 months | 03's brand | 03 | 1 operator; 18-COG |
| Net margin range | 20 to 30% | 03's brands | 03 | 1 operator, self-contradicted in the same breath |
| Subscription attach example | 33%, over $5,000 a month recurring | One product | 02 | example |
| Tool prices | Kalodata about $80 a month; Spy Crew Pro about $49; Team Drop $0; Axio free | At recording | 02, 04, 07 | `[web check]` all |

One threshold row, "uphill phase before breakthrough" (about 6 months, source 01), moved to Appendix A with R108.

## 7. Where sources disagree

Each conflict: what each side says, when each is right, what the agent should do.

**C1. Saturation: disqualifier or opportunity.**
Disqualifier: 02 skips anything it recognizes, caps revenue to avoid contested products, and rejects late entries where the library is crowded and the trend fades. 03 says a second or third identical-product bidder grossly raises CPMs and that outsized results come from scarcity of bidders. 10 says thousands work the same aggregator feeds and CPMs rise.
Opportunity: 05 says many sellers prove demand and removes the "teach the market" risk, and builds its whole angle-pivot method on saturated products. 08 says no seller reaches everyone and cites teeth-whitening pens. 10 itself says to go deeper on research in a contested angle (neuropathy).
When each is right: the disqualifier view is right when you would run the same product, same angle, same market as the incumbents, with no cost or brand advantage, on an auction platform. The opportunity view is right when you can name an unserved avatar, geography or offer, and can afford higher CPMs while you prove it.
What the agent does: grade with R53's ladder and never read saturation alone. Green means proceed. Amber or red means run P12; if an angle with a small nonzero share exists and P14 still passes at a CPM 25% higher than the brand's history `[needs brand data]`, proceed as a differentiated entry; if not, drop. A 10+ identical-seller product is a cash test only (R56), never a brand build.

**C2. Arbitrage or copy-a-proven-product vs owning a differentiated product.**
Arbitrage: 02 (find someone else's TikTok Shop winner, resell on Meta), 08 (find competitors making money, reverse-image the item, adapt what works), 05 (copy demand, change the avatar or geography), 04 (source the same generic item privately, brand after proof), 10 (mine the winning angle, execute better). 03 says chase the trending product for speed and admits he could not define "brand" at $10M a year.
Owning: 01 (change 1 variable in a stagnant category, steal design from distant industries, never from competitors), 07 (pair demand with a quality gap and build the spec from cited pain points), 03 later (a winning product is not a moat; build brand and secondary products), 09 (fixable concerns via branding and a better formula).
When each is right: arbitrage is right for a seller with no inventory, cheap switching cost, and a goal of cash flow in weeks; it dies when copies arrive (03's "power law", 04's undercutting). Owning is right for a brand that will hold inventory and reputation and wants durability; it is slower and needs capital for samples, tooling and regulatory work.
What the agent does: ecomOS forbids copying products, text, logos and faces (O2), so pure arbitrage is out of scope for every ecomOS brand. The agent uses the arbitrage sources for demand reading and cost floors only, and every shortlist entry must name an owned difference. For a dropshipping-model brand, the difference can be avatar, offer and packaging; for an owned brand it should include spec or formulation.

**C3. Home market first vs inverse expansion (AU, UK, EU, CA, then US).**
Inverse: 03, one operator, one product (Udie), with the stated result that the UK became the largest market and the US the smallest. Geo-arbitrage: 05, take a US or UK-proven product into an untapped European country. Home market first: the conventional method 03's interviewer cites; no source in this folder argues it in detail.
When each is right: inverse is right for an English-language product that travels without localization, with capital for 4 to 5 sequential launches, when the goal is first-mover position before the US auction saturates. Geo-arbitrage is right for a single untapped market with a proven product elsewhere and a localization budget. Home first is right when the brand's logistics, payments, compliance and reputation exist only at home, which is the case for most ecomOS brands.
What the agent does: default to the brand's home market for the first proof (R99 precondition: fit in 1 market before any sequence). Then score candidate next markets on: exact-product competitor count there (P10), delivery days and cost (R85), duty, VAT and compliance (R100), and localization cost. Enter the cheapest-to-win market next, whichever it is; the inverse order is one sourced answer to that scoring, not a rule. Set the "proven enough" gate yourself (P18 step 3) because no source gives one.

**C4. Passion vs cash flow.**
Cash flow: 03 (become passionate about success first, pursue passion when financially free), 05 (selling what you like is not research). Passion: 01's energy test (which direction excites you), "if it is hard it is probably wrong" (R108, moved to Appendix A), and his warning that work should give energy back. 08 accepts a "passionate community" as a substitute for a problem.
When each is right: cash flow is right for selection (what to sell). 01's energy test is right for choosing between concepts that already passed the market checks, and as a founder-persistence signal, not a demand signal. 08's passionate-community rule is about the buyer's passion, not the founder's.
What the agent does: never score a candidate on founder preference. Record founder excitement as a tiebreaker between candidates that pass P13 and P14 equally. Treat a buyer community's passion as a valid R5 input.

**C5. 1 SKU vs a range.**
1 SKU: 09 (inventory capital, storage, shipping mix-ups). Range: 03 (evergreen secondary products before the hero fades), 06 (AOV 20 to 40% over base needs upsells), 02 (subscription and bundles).
When each is right: 1 SKU for validation and the first inventory buy. A range once the hero is proven, to defend against trend fade and to lift AOV.
What the agent does: launch plan carries 1 SKU. The validation memo lists the 2 to 3 evergreen follow-ons and the upsell that will lift AOV, with a trigger (first reorder, or the brand's CPA bar met for 4 weeks) for adding them.

**C6. Trending vs evergreen.**
Trending: 02 (speed into a spike builds ad-account history), 08 (fast cash, gone in 2 to 4 weeks), 03 (chase the trending product; $10M in year 1). Evergreen: 08 (brandable for years, slower start), 09 (avoid fads), 01 (high-frequency stagnant categories), 03 later (secondary evergreen lines outlasted the hero).
When each is right: trending is right when switching cost is near zero and no inventory is bought. Evergreen is right for any brand that buys MOQ inventory or builds a brand.
What the agent does: classify every candidate (R69). For an ecomOS brand holding stock, trending picks are capped at sample-quantity buys and a fixed test budget, no custom packaging and no brand build. Evergreen picks go through the full P13 and P18. A steep no-history spike is a gamble in every model (R19).

**C7. Breaking your own filters on conviction.**
For: 02 (the criteria are a blueprint, not a bible; breaks the concentration rule on a $58K-in-7-days video; skips Google Trends when sure). 01 (rules as heuristics, with counter-examples given against his own rules). Against: 09 (a written pass, caution, red-flag score with explicit reasons), 08 (the full stack on every product), 06 (validate and margin-check before spending, do not blame the method after one bad day).
When each is right: overrides are right on amber checks where the overriding signal is stronger than the rule's purpose (a very large recent revenue figure outweighs concentration risk). They are wrong on hard economics, regulatory and claims checks, and wrong when they are not written down, because 2 operators then reach different picks from the same data.
What the agent does: R106. One override per amber check, with the signal named and logged in P17. No override on P14 gates, R84 or section 3.17. A memo with more than 2 overrides is marked "conviction pick" and needs a human sign-off.

**C8. Qualitative concept validation vs data-led validation.**
Qualitative: 01 (build the concept, energy test, friends and family, consumer auditions for feedback not votes, retail buyer reactions). Data-led: 02 (graphs and video data), 06 (traffic-based revenue estimate and margin math), 08 (competitor profit), 09 (keyword and trend data plus a scored memo).
When each is right: 01's method is for a new format in an old category where no competitor data exists to read. The data-led methods are for products with observable demand.
What the agent does: run the data-led stack always (R105). Add 01's qualitative pass for owned-brand concepts as input to P19 step 4. Never let the qualitative pass replace P14.

**C9. Problem-solving required vs passion-community enough.**
10 requires a daily problem; 05, 06 and 02 require a real problem or insecurity; 09 and 08 accept passion. What the agent does: R5's ranked merge. A passion-only product must show stronger demand evidence (R36 plus R49) to compensate.

**C10. Organic burner-account scouting: useful or outdated.**
Useful: 05 (Instagram Reels), 08 (TikTok, found a candidate in 40 seconds). Outdated: 10 (2026 methods; needs a trained eye that takes 3 to 6 months; Instagram burners are reposts). What the agent does: use P6 as a free supplement with a 2-week time box; rely on P3 and P4 for the primary list. If the brand's platform is TikTok, P6 stays primary.

**C11. Competitor revenue floor: $200K to $300K a month vs any proof of profit.**
06's floor is high and stated 2 ways; 08 accepts a single ShopHunter estimate of about $90K a month. What the agent does: apply 06's floor for a single competitor used as proof; below it, require 2 independent sellers with run length of 14 days or more (R25). Record both numbers as estimates, not facts.

**C12. Margin as absolute dollars vs percentage vs price band.**
05 and 06 use dollar floors; 06 adds a 3x multiple; 09 uses a price band; 07 reports a percentage on product cost only; 04 says net margin after ads is the only real KPI. What the agent does: P14 runs all of them and lets the brand record's contribution target decide (O4). The dollar floor binds at low cost; the multiple binds at high cost; the band is a caution, not a gate.

**C13. "The product is rarely the reason a test fails" vs "the product is everything".**
06 says failures are usually ads or funnel (about 90% ads-related in his experience, anecdotal). 03 attributes his first hits mainly to "perfect product timing". 02 says validated products still fail your test and you move on. What the agent does: P20 order (ads, funnel, then product) after 1 failed test; after 2 failed tests with ads and funnel in range, the product goes back to P12 or to no-go.

**C14. Private supplier or agent vs marketplace vs subscription platform.**
04 rejects AliExpress, Alibaba, CJ, AutoDS and Zendrop in favor of a free agent platform it earns referral bonuses from; 08 promotes ZenDrop on an affiliate link; 07 uses Alibaba directly; 05 and 08 use AliExpress for the cost floor. What the agent does: no source is neutral. Use AliExpress and Alibaba for the cost floor, get 2 quotes from 2 different channel types, and judge on measured delivery days, sample quality and total landed cost `[web check: current pricing and terms of each platform]`.

## 8. Common mistakes

Merged from all 10 sources, deduplicated, each with the fix.

1. Picking on total revenue without checking the videos that drive it, or their age (02). Fix: R20, P2 step 6.
2. Reading only the 30-day graph (02). Fix: R18; the 180-day view is mandatory.
3. Treating a viral video, a trend headline or a spy-tool hit as validation (08, 09, 06, 14 sources in spirit). Fix: R105, full stack every time.
4. Trusting a single viral creator without the 3-videos-over-1M audit (08). Fix: R36.
5. Reading active-ad count or run length as profit (06, 08, 10). Fix: R26, R49, O3.
6. Treating an ad running only hours as either proof or a non-threat (02). Fix: bookmark and watch.
7. Selling what you like (05, 03). Fix: R11; founder preference is a tiebreaker only.
8. Copying a competitor's product or store "a bit better", or scraping aggregator feeds (05, 10). Fix: R34, O2, name an owned difference.
9. Ripping a competitor's ad wholesale or reposting their video (02, 05). Fix: O2; describe the angle in words for 03-CRE.
10. Testing a $9.99 product and expecting Meta economics to work (02). Fix: R75.
11. Checking one margin rule and not the other, or using a competitor's assumed cost (06). Fix: R76, R78, P14 both gates.
12. Ignoring shipping, processing, refunds and duty in the margin (06, 07, 04). Fix: P14 steps 2 to 3 from brand data.
13. Choosing heavy, oversized or fragile products without pricing the carrier or testing transit (05, 09, 03). Fix: R81, R82.
14. Not checking seasonality and getting caught on cash flow (09). Fix: R70.
15. Choosing a perishable product with shelf life shorter than the ramp (09). Fix: R83.
16. Entering a regulated category before checking claims and labeling rules (09, 01). Fix: R84, hard stop.
17. Assuming any consumable supports a monthly subscription (09). Fix: R72.
18. Launching many SKUs at once (09). Fix: R87.
19. Adding custom packaging before the product sells (04). Fix: R94.
20. Trusting a supplier rating without a call, or placing a large first order (07). Fix: R91, R92.
21. Sending suppliers consumer-language specs (07). Fix: R90.
22. Assuming an AI-listed supplier is on the platform named, or that AI mockups are a spec (07). Fix: R96, R41.
23. Skipping willingness-to-pay in pain-point prompts (07). Fix: R42.
24. Asking an AI to "find me a $1k a day product" with no market or problem first (06). Fix: P7 steps 1 to 2.
25. Forcing an ill-fitting avatar onto a product to escape saturation (05). Fix: R60 fit test.
26. Overbuilding a brand around a 2 to 4 week trending product (08). Fix: R56, R69.
27. Buying MOQ inventory against a no-history spike (02, applied to owned brands). Fix: R71.
28. Changing 2 or 3 product variables at once (01). Fix: R66.
29. Over-complicating the pitch to signal sophistication (01). Fix: 1 concrete scenario and 1 difference.
30. Funding a structurally capital-intensive business on consumer love alone (01). Fix: R80.
31. Treating one early win as a repeatable formula and launching many follow-ons (03). Fix: R109, moved to Appendix A.
32. Assuming spillover from one country to the next (03). Fix: R99, validate each market alone.
33. Skipping duty, VAT and localization when moving a product across markets (05, 03). Fix: R100.
34. Not verifying a logistics partner's regional paperwork before peak (03; 18-COG owns the fix).
35. Giving up on a niche after a few pages instead of widening filters (02). Fix: R23.
36. Leaving the "growing" toggle on in Kalodata, hiding good products (02). Fix: P2 step 2.
37. Judging a native-scouted store dead because a traffic tool shows no data (10). Fix: R51.
38. Blaming the product, or the method, after one bad day (06, 02). Fix: P20.
39. Over-optimizing CTR for curiosity ads that do not sell (06). Fix: 04-MED; P20 step 1.
40. Silent rule overrides (02). Fix: R106, log every override.
41. Treating the 16 questions as strict pass or fail (09). Fix: R104, pass, caution, red flag.
42. Letting a fresh research feed drift (05). Fix: keep curating or switch method.
43. Assuming an operator's self-reported revenue proves the method (all 10). Fix: section 12; use only the mechanics.
44. Reusing a source's example numbers as the brand's targets (09, 06, 04). Fix: O4.

## 9. Deliverables

Every deliverable is plain text or a table, short sentences, digits, no em dashes, no inflated words, and cites card ids where a rule was applied. Nothing in a deliverable claims a benefit the brand cannot prove (O1).

**D1. Shortlist with scores.** One row per candidate from P17, top 10, sorted by score.
Columns: rank; product (generic name, no competitor brand); source method (P1 to P8) and date; problem or passion (R5 class: daily pain, occasional pain, passion, nice-to-have); evergreen or trending; demand read (30-day and 180-day shape, Trends 12-month and 5-year class, seasonality note); competition color (R53) and identical-seller count; competitor proof (revenue estimate or 2 sellers with 14-day runtime); open angle (avatar in 1 line, share estimate); price band and gross margin at own quote; logistics flags (weight, durability, shelf life, regulatory); owned difference (O2); score; next step.
Score (ecomOS scale, not from any source): 0 to 3 points each on demand, competition, angle, economics, logistics; 15 max. A red on P14 gates 1 or 2 or on regulatory sets the score to 0 regardless of the rest. Overrides are listed under the row.

**D2. Validation memo per product.** 1 to 2 pages.
Header: product, brand, date, business model, target market, author.
1. Summary: decision (go, conditional go, no-go) and the 3 reasons.
2. The 16 questions with score and evidence (P13), market questions first.
3. Demand evidence: numbers, dates, tool names, screenshots referenced by file name.
4. Competition evidence: ladder color, counts by country, competitor revenue estimate with the formula inputs, store quality notes.
5. Angle brief (P12 step 7) or "not needed, green".
6. Unit economics (P14): landed cost, fulfillment, processing, refunds, price, gross margin, 3x check, contribution vs brand target, CPA headroom, at low and high price and at bulk. Marked "provisional" where brand data is missing.
7. Logistics and regulatory: weight, durability, shelf life, rules per country, IP check.
8. Highlights and concerns; each concern fixable or market-dependent (R104).
9. Overrides used, each with its signal (R106).
10. Handoffs: 02-AVT (avatars), 03-CRE (angle in words), 04-MED (test brief and window), 05-WEB (funnel type seen in competitors), 06-OPS (supplier brief).
11. Post-test review date and the metric that decides (P20).

**D3. Supplier brief.** 1 page.
Product spec in manufacturing terms (R90); the 2 to 3 defining features and the capability question for each (R91); cost floor found and where (R88); 2 or 3 candidate suppliers with platform, verified listing, quote at first-order quantity and at a volume tier, MOQ, lead time, certifications, reorder rate if shown; sample plan (1 sample, then about 50 units) and the tests the sample must pass (R82, R38); shipping options per target country with days and cost (R85); packaging plan staged after proof (R94); the recommender's commercial interest for any platform named (section 12); re-quote cadence (R95).

**D4. Launch sequence plan.** 1 page plus a table.
Chosen sequence option and why (C3); first market and its independent validation summary; per-market table: market, competitor count, delivery days and cost, duty and VAT, compliance items, localization needed, entry gate metric, planned date, owner; SKU at launch (1) and the follow-on products with their trigger (C5); evergreen or trending class with the matching budget and patience (R69); test window and review owner.

**D5. Offer ladder.** 1 page.
Base price and the offer structure that lifts AOV without inventing claims (R63): bundle name, BOGO or multi-buy, free-gift threshold, a named ingredient or format only where provable (O1); the price-to-margin math from the margin gate (R76) at the offer's effective price, not the sticker price; the stage at which each rung is added (test, proven, scaled). Handed to 05-WEB as a page-ready pricing structure instead of extracted from the validation memo's prose.

## 10. What needs live data or a web check

### 10.1 `[needs brand data]` (from the brand record or data layer)

- Business model: dropshipping, private label or owned manufacturing (section 0, every `[dropshipping assumption]` rule).
- Margin floor and contribution target after all costs (R76, P14 gate 3).
- Landed cost, shipping per order, payment processing rate, refund and chargeback rate (R76, R85, P14 steps 1 to 3).
- Historical CPA and ROAS for similar products; the brand's own test bar (R107, P14 step 7, P19 step 6, P20).
- Delivery days and refund rate per ship-to country (R85).
- Primary ad platform (R24, R33).
- Audience age skew (R33, P5).
- Current AOV and price architecture (R75).
- Ad budget per test and number of angles affordable at once (R65, R97).
- Home market, logistics and payment coverage per country, capital for sequential launches (R99, P18).
- Per-market regulatory, sizing and returns requirements (R84, R100).
- Current catalog, hero product, existing supplier relationships, MOQ tolerance, first-order budget (R59, R87, R89, P8, P15).
- Whether the 3PL or supplier can handle per-order customization (R13).
- Which SKUs or claims can legally be named by benefit per market (R68).
- CPM tolerance for a differentiated entry into a contested angle (C1: placeholder of 25% above history).
- The "proven enough to expand" metric (P18 step 3: placeholder of CPA bar met 4 weeks).

### 10.2 `[web check]` (live on the web before acting)

Tools and pricing: Kalodata, Shop Plus and Spy Crew bundle contents and prices (R15, P2); Get Hooked existence, pricing and MCP endpoint (P4, P7); PP Ads filters (P4); Winning Hunter pricing and whether "Magic AI" is still the feature name (P4); ShopHunter (P11); SimilarWeb free-tier limit (R49); Team Drop status and fees, Uni Express and "Yune" shipping-line names, AutoDS and ZenDrop pricing (R93, C14); Axio availability, pricing and country access (P8); Trend Rocket, Exploding Topics, Mania, Trend Hunter current features (R14); BuzzSumo or a current mention-count tool (P9); a replacement for Alexa for competitor audience data (R52, section 11); current Claude model names and connector UI (P7).
Platform data: Meta Ad Library counts and run lengths per country for each candidate (P3); TikTok Shop graphs and video lists (P2); Google Trends and Keyword Planner reads (P9); live Amazon ratings and listings to confirm any AI-summarized trend or rating claim (P8, R48).
Regulatory and IP: claim, labeling and testing rules per category and country (R84, R68); trademark and licensing status of any character or design element (R86); import duty, VAT and shipping-time rules per target country (R100).
Source verification (does not change any rule): whether the 02 and 10 presenters are the same person; publish date of 03's interview; whether 05's revenue claims and 06's method have any corroboration; whether Target's "Made to Matter" program still exists (01); whether RFID livestock verification products exist (01); whether native widgets still run on weather.com and CNN and which vendor (R33); whether Meta delivery rewards advertiser tenure on a product (R71, 02's belief); current Facebook age-demographic data (R33).

## 11. Freshness and stale-risk notes

| Area | What can go stale | Rules affected | Re-verify |
|---|---|---|---|
| Discontinued tools | Alexa's traffic and demographics service was shut down in 2022; 09 still names it. No replacement is sourced. | R52, P9 step 6 | Before first use; pick a current audience tool and record it in an overlay |
| TikTok Shop tools | Kalodata filter names, the "growing" toggle, revenue-source filter, 30-day and 180-day views, Shop Plus clone inside Spy Crew, prices ($80, $49). 02's own metadata marks decay risk high. | R15 to R23, P2 | Every 3 months, and before any hunt after a UI change |
| TikTok Shop itself | Category names, revenue reporting, live vs video split, market availability; the GLP-1 patch example is a 2025 moment | R15, R16, examples | Every 3 months |
| Ad Library UI | Active filter, date filter, media type filter, Page Transparency location, country selector | R25, R27, P3 | Every 3 months; `[verify UI]` on every step |
| Spy tools | Get Hooked filters (Top performing, ads per brand, runtime, brand active ads), PP Ads sort names and page size, Winning Hunter "Magic AI", ShopHunter estimates; all promoted with affiliate links | R25, R26, R30, P4, P11 | Every 3 months; treat filter names as illustrative |
| AI tooling | Claude model names ("Opus 4.8" in 06), custom connector steps, Get Hooked MCP endpoint, Axio's features, pricing and access; 06 and 07 both mark decay risk high | P7, P8, R39 to R43 | Monthly while in use |
| Platform saturation | Every threshold in 3.2, 3.3 and 3.7 reflects the competition level at recording (2024 to 2026). CPM levels, the $33K to $97K band, the 14-day runtime and the competitor ladder drift as more sellers use the same tools | R15, R25, R53, section 6 | Recalibrate from the brand's own test results every quarter (R15's method) |
| Ad cost benchmarks | 06's CPC, CTR, CPM, ATC and checkout numbers are US Meta figures at recording; 06 already raised his margin floor from $20 to $30 because costs rose | R76, R107, P20 | Replace with brand data as soon as 1 test exists |
| Sourcing platforms | Team Drop, ZenDrop, AutoDS pricing and "free" status, shipping-line names and the 6 to 10 day window, AliExpress delivery times, Alibaba verified-supplier features, 1688 access | R85, R93, P15, P16 | Every 6 months, and before any supplier brief |
| Regulatory | Claim and labeling rules for supplements, cosmetics, food, baby products; duty and VAT thresholds per country | R84, R100 | Before every launch and every new market |
| Native placements | Which sites carry paid-content widgets, which vendor, and whether the older-buyer skew holds | R33, P5 | Every 6 months |
| Social feed methods | 10 already calls TikTok and Instagram burner scouting outdated for 2026; feed algorithms change without notice | R35, P6 | Every 6 months; time-box to 2 weeks per attempt |
| Source claims | All revenue figures and case results are self-reported at recording (2021 to 2026) and never verified; they do not go stale so much as they were never fresh | section 12 | Never used as targets |
| Expansion order | 03's inverse sequence reflects 2019 to 2022 auction conditions and COVID growth; the US-last logic may not hold | R99, C3 | Score markets live each time (P18) |

24 Sep 2026: ecommerce specificity pass applied from ECOM_REVIEW.md; priority block added, 14 rules reworded, 8 levers added, about 175 words moved to Appendix A.

## 12. Source index

Credibility scale: A = operator with named, checkable brands and no tool to sell; B = operator with named results but a commercial pitch; C = anonymous or near-anonymous creator with self-reported results and a tool or course to sell; D = demo or teaching content with no results at all. Bias notes name what the source gains from you believing it.

| No. | Title | Type | Credibility and bias | What it contributed most |
|---|---|---|---|---|
| 01 | How I Start $1 Billion Companies from Boring Products | Podcast interview, late 2025 | A minus. Eric Ryan (Method, Olly, Wellie; Cast failed). Own recollection only, valuations self-stated, half the transcript is hosts brainstorming pitches. Now a VC, so an incentive to make founding sound systematic. No tool sold. | Boring-category thesis, sea of sameness, brand-recall white-space test, one-iteration rule, cross-industry design theft, benefits over features, structural-economics stop rule, qualitative concept selection (R1 to R4, R66 to R68, R80, R101, R102) |
| 02 | This Product Research Method Made Me $2.3M Dropshipping | Live screen-share, June 2025 | C. "Ben", 20, self-reported store results, promotes Spy Crew (affiliate) and his paid community; states his rules are a blueprint he breaks on conviction. Most thresholds in section 6 are his alone. | Kalodata filter settings, 30 vs 180-day read, video recency and spread, live-revenue and $9.99 rejects, niche-level competition, offer as differentiator, TikTok Shop does not equal Meta (R15 to R24, R46, R54, R63, R64, R106) |
| 03 | How to Build a Billion Dollar E-Commerce Empire | Podcast interview, about mid-2025 | B. Dave Fogerty (Calming Blankets, Udie, Pupnaps; 10 to 12 failures). Self-reported, hedged ("I'd have to check"), sells Trend Rocket and coaching. Half the content is founder psychology, not extracted. | Inverse expansion order, positioning-gap method from the Ad Library, CPM effect of identical competitors, product over brand for speed, brand and secondary products as the moat, passion vs cash flow (R3, R4, R53, R58, R59, R60, R99, R109) |
| 04 | The Best Supplier for Branded Dropshipping in 2026 | Talk, Nov 2025 | C. Anonymous creator, income screenshots, referral bonuses from Team Drop, sells his own community. Every competitor comparison is his opinion. | Private-agent sourcing model, shipping-line cost vs speed, volume re-quotes, branding after proof, net margin and refunds as the KPI (R76, R77, R85, R93 to R95) |
| 05 | Full Product Research Course for Dropshipping | Course-style video, Mar 2026 | C. Creator with a $10M revenue claim and a mentorship, Winning Hunter discount code. Rules are personal heuristics; "1 in 2 winners" is unverified. | 4-point baseline screen, Ad Library generic-keyword method, competitor count thresholds, Reels feed training, Winning Hunter workflow, Blue Ocean angle pivot with the 10% share rule, geo-arbitrage, research log funnel (R5, R27, R35, R38, R53, R55, R60 to R62, R97) |
| 06 | Asked Claude to Find Me a $1K a Day Product | Video, June 2026 | C. "Mark", Brand Builds Academy mentorship; one live example, prompts withheld behind an Instagram DM funnel; claims the method takes under an hour. Mechanics are separable from the pitch. | Market, problem, product hierarchy; Claude sub-niche generation; MCP ad-data connector; SimilarWeb revenue formula and floor; $30 and 3x margin rules; post-test ads vs funnel diagnosis (R5, R6, R39, R40, R43, R49, R76, R107) |
| 07 | Making Money with Alibaba's New AI Agent | Podcast demo, about Jan 2026 | D. Software podcaster, not an ecommerce operator, no affiliation with Alibaba, promotes his own paid idea newsletter. Single first-time demo; every number is an on-screen example. | Demand plus quality gap (3.8 rating), cited pain-point mining with willingness to pay, consumer-to-manufacturing language, structured sourcing prompt, 2 to 3 capability questions, 50-unit trial order, human in the loop (R7, R8, R41, R42, R48, R89 to R92, R96) |
| 08 | The Only Product Research Video You Need to Start Dropshipping | Talk, June 2024 | C. Anonymous creator, ShopHunter 25% and ZenDrop 50% affiliate links, PP Ads stated unpaid. Oldest dropshipping source; its trending example was stale at publication. | Competitor profit as the first filter, saturation reframed, evergreen vs trending, 3-videos-over-1M audit, PP Ads longest-running sort, reverse-image sourcing, 10-account saturation rule, master checklist (R25, R36, R50, R55, R56, R69, R88, R105) |
| 09 | How to Find and Validate Winning Products: 16 Steps | Shopify channel video, July 2021 | D plus. Shopify's Michelle Bally; teaching framework on a hypothetical coconut-oil hair mask, pitches a Shopify trial. The $50 to $150 band is unsourced. Names Alexa, discontinued 2022. Least biased toward any single tool. | The 16-question pass, market before product, pass/caution/red scoring, price band, markup at 2 price points and at bulk, 1 SKU, subscription by real usage, size and weight, durability, seasonality, shelf life, regulatory, the written memo (R44, R45, R47, R52, R57, R70, R72, R75, R77, R79, R81 to R84, R87, R103, R104) |
| 10 | The Product Research Method That Made Me $670k | Talk, Feb 2026 | C. Anonymous, no screenshots, promotes the Luxury Extras tool bundle. Not the same video as 02 despite the earlier guess (section 0). Asserts Facebook skews older with no data. | Get Hooked filter settings (14 days, 50 active ads, 4 per brand), native widget scouting, daily-problem plus retail-absence criteria, Ad Library image filter and 1-week read, angle mining from the longest-running ad, the case against burner scouting and aggregator ripping (R5, R10, R25, R26, R28, R30, R32 to R35) |

**Neighbour folders and what lives there.**
- 02-AVT (buyer avatars): testing one product across several avatars in creative (03's method); consumes this folder's candidate avatar list.
- 03-CRE (creative): hook and body construction, 02's mix-match splicing, 05's remix step (which ecomOS replaces with original production); consumes the angle brief in words.
- 04-MED (media): the 2 to 3 day Meta test, CPC, CTR and CPM reads (06), bidding; consumes the test brief; Meta stays read-only from this folder.
- 05-WEB (storefront): PDP vs advertorial, checkout simplification, AOV upsells (06); consumes competitor funnel notes.
- 06-OPS and 18-COG (operations, logistics): fulfillment app setup, 3PL wallets and fulfillment locations (04), shipping lines, peak-season paperwork (03); consumes the supplier brief.
- 20-FIN (finance): exit multiples and valuation (03).
- 24-DEP (ad deployment) and 12-GAD (Google Ads): account audits and Google search demand tactics; Keyword Planner reads from P9 may inform 12-GAD.
- Brand folders (`brands/<brand>/overlays/01-PRD-product-research.md`): the brand's margin target, markets, platform, supplier list and every `[needs brand data]` value above.

## Appendix A. General background

Demoted during the 24 Sep 2026 ecommerce specificity pass (ECOM_REVIEW.md section 5): founder-psychology aphorisms with no store framing, moved out of section 3.16 and section 6. Kept for reference only; not decision rules an agent runs.

**R108 (moved from section 3.16).** Use "if it is hard, it is probably wrong" as a prompt to re-examine, not as a stop signal. 01 states the rule and then describes 6 months of pushing uphill before a concept broke through. Effort does not equal value. Source: 01. Cards: [9f2a41b455b9].

**R109 (moved from section 3.16).** Do not treat one early win as a repeatable formula for launching many more products. 03 launched 10 to 12 follow-on businesses after 2 hits and says all failed on unbuilt skills (team, systems, brand, secondary products). Source: 03. Cards: [7820f678f67d] [ddbe3cee6657].

**Uphill phase before breakthrough (moved from section 6, thresholds table).** About 6 months. Counter-example to "if hard, wrong". Source: 01, 1 founder.
