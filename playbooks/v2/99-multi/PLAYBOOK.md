# 99-multi playbook: the operating system layer

version: 2.0-draft  |  24 Sep 2026  |  sources: 22 (23 mini playbook files; source 01 is in 2 parts)  |  cards: 1,016  |  built from: sources/*.md

## 0. How to use this playbook

**Which agent runs it.** The brand operator agent. This is the cross-domain layer that no single domain folder owns. It decides which lever to pull, in what order, at what stage, and with what money. It does not execute inside a domain: it routes to 01-PRD through 24-DEP for that. Every domain-specific finding in these 22 sources is mapped in the routing table in section 1.3 so the domain folders can absorb it in a later overlay pass.

**Two jobs.**
1. Operating system: unit economics and the growth model, bottleneck diagnosis, stage plans, channel mix and sequencing, persuasion as constraints, seasonal peaks, founder and capital decisions, the brand teardown method.
2. Routing layer: section 1.3 maps every domain finding to its owner folder with source numbers. Detail stays here only where no domain folder owns it.

**Which sections to load for which task.**

| Task | Load |
|---|---|
| "Are we healthy, can we scale?" | 3.A, 4.1, 4.2, 5.1, 6 |
| "Growth stalled, what is broken?" | 3.B, 4.3, 5.2, 7 |
| "What should we be doing at our size?" | 3.C, 4.4, 5.3 |
| "Where should the next dollar go?" | 3.D, 4.5, 5.4 |
| "Is this offer or copy honest and grounded?" | 3.E, 8 |
| "Black Friday or peak plan" | 3.F, 4.6, 5.5 |
| "Raise, sell, hire a CEO, take PE money?" | 3.G, 4.8, 5.7 |
| "Tear down a competitor" | 3.H, 4.7, 5.6 |
| "Which folder owns this?" | 1.3 |

**What the agent must fetch before acting.**
- From the brand record: category, price points, SKU count, hero SKU share, stage (revenue and monthly spend), channel mix, ownership and capital position, peak-season calendar.
- From the data layer: net revenue split new vs returning, per-SKU COGS and cost of delivery, ad spend by channel, new-customer counts, cohort repeat curves, inventory on hand and on order, opex by line, cash balance. Do all arithmetic in code, never in the model.
- From the web, when a rule carries `[web check]`: current platform attribution defaults, current Meta and Google features named here, current macro figures for the target market. Section 10 lists them.
- From the user: the objective for the period (profit, cash, growth, exit) and the risk appetite. Several rules in section 7 cannot be resolved without it.

**Source warning, read first.** Nearly every source here is a founder self-report on a promotional podcast, an agency pitch, or a course. Six sources come from one agency (Blue Sense Digital: 01, 14, 15, 17, 19, 20 is a likely sibling), two are the same founder twice (03 and 13, Bloom), two are the same brand from inside and outside (09 and 16, IM8). Several sources contradict themselves on numbers: spend shares (05), valuations (05), CAC arithmetic (16, 22), fee and cost figures (16), audit claims (14 title vs body), deal years (03), creator CPM anchors (03 vs 13). Section 12 rates each source. Where a source contradicts itself, this playbook marks both figures and does not average them. Only 02 (Cialdini) and 22 (a hypothetical spreadsheet) have no commercial pitch, and 22 has no real data at all.

**ecomOS rules that override any source.**
- No invented claims, no invented scarcity, no fake proof. Cialdini's mechanisms (3.E) are constraints, not tactics to fake.
- Competitor ads are signals, not proven winners. Never copy competitor text, products, faces or landing copy (3.H).
- Brand and warehouse data beat any founder figure. Every threshold in section 6 is a hypothesis until the brand's own data confirms it.
- All arithmetic in code. Metrics that are missing show as unavailable, not zero. Period ROAS = total value divided by total spend. Keep totals separate from breakdowns.
- Meta is read-only. Nothing here authorizes an ad-account write. Recommendations go to a human.
- Keep brands apart. Case numbers from Ridge, True Classic, Bloom, IM8, Comfrt, Salt and Stone, David Protein, Gruns and Alo are examples, never promises.

## 1. Scope and outcomes

### 1.1 What this folder covers

The operating layer that sits above the 24 domain folders:

1. **Unit economics and the growth model**: net revenue, true gross margin, contribution margin, MER and AMER, CAC paired with first-purchase gross profit, LTGP:CAC bands, payback, the 6 cash-conversion levers, the death spiral and its early warnings, the 60 to 180 day lag between a lever change and cash.
2. **Bottleneck diagnosis**: data integrity first, one bottleneck at a time, traffic vs conversion vs backend, product-led vs media-led brand archetypes, top-down root cause.
3. **Stage plans**: $0 to $100k, $100k to $1M, $1M to $10M, $10M plus, expressed in both annual revenue and monthly spend, with what changes at each stage.
4. **Channel mix and sequencing**: Meta share, Google, influencers and affiliates, retail, Amazon, organic, tertiary channels, and the "next best dollar" rule.
5. **Persuasion principles as constraints**: Cialdini's 6 principles plus contrast, each with its operating condition, its failure mode, and the ecomOS ban on the manufactured version.
6. **Seasonal peaks**: Black Friday spend front-loading, creative volume, offer ladders, pacing, attribution lag, cohort quality.
7. **Founder and capital decisions**: bootstrapping vs raising, supplier terms, debt tools, PE and LBO mechanics, secondaries, exits, key-person risk, CEO replacement.
8. **Brand teardown method**: how to read a competitor's ads, P&L and landers as signals.

### 1.2 What it does not cover, and the measures it moves

Not here: any execution detail inside a domain. Meta account structure lives in 24-DEP. Creative production in 10-MCR. Ad copy in 11-ADC. Offers and pricing in 03-OFF. Landing pages in 07-LPG. Measurement mechanics (CAPI, geo-lift design, attribution windows) in 06-MEA. Finance mechanics (P&L build, forecasting, working capital instruments) in 20-FIN. Retail, suppliers and 3PLs in 18-COG. Team and hiring in 21-OPS. Creators and organic in 13-ORG. Amazon in 22-AMZ. Email in 14-EML. Post-purchase in 17-CXP. Product selection in 01-PRD. Avatars in 02-AVT. Brand in 04-BRD. Wild bets in 19-WLD.

Measures this layer moves: net-customer profit contribution, LTGP:CAC in the chosen window, CAC payback months, cash conversion cycle days, ending cash, contribution margin after marketing, share of revenue from new vs returning customers, and the share of spend that survives an incrementality read.

### 1.3 Routing table: domain findings in these 22 sources and the folder that owns them

Use this table when a source finding is not cross-domain. Source numbers use 01p1 and 01p2 for the two parts of source 01. Card ids are the first 12 characters. The owning folder should absorb these in its overlay pass; this playbook keeps only the cross-domain rule that references them.

| Owner folder | Finding (short) | Sources | Card ids |
|---|---|---|---|
| 01-PRD | CAC product vs LTV product test; $50+ price floor; $10 to 50M net-new bar | 04 | 7088bf5dd924, 6359013f537c |
| 01-PRD | Mass-market checklist: consumable, low SKU, 75%+ GM, Target/Walmart/Costco viable | 04 | afb28cb1dcdf |
| 01-PRD | Launch cost cap (under $500k), parallel launches, never rescue a flop | 04 | db8e8f54f571, 121ab6f08f3f |
| 01-PRD | Small-brand 3-gate validation: email threshold, organic, small paid | 04 | c2268e45aa25 |
| 01-PRD | Trend surface area vs single-ingredient trend | 04 | 4279fceac4b9 |
| 01-PRD | Saturated category, white space inside it; TAM ladder gated by community demand | 03, 13 | 255fc78a445c, b2f5debc1f20, e068edbb24fa, 2ad217557e32, d7b0efd4b69c, 66cddfb2c547 |
| 01-PRD | Live sampling 150 tasters, 90% like; loud minority (50 comments, 100k units, 50 sold); team as incubator | 03 | 178efe60f98d, 4718620ea527, 1c4d387e42fb |
| 01-PRD | Digital lead product before physical ($9.99 PDF); community picks next category | 03, 13 | cb1e0f63e55e, 491bb6180c60, b3ef8af35c4c |
| 01-PRD | Amazon BSR and Google Trends as daily demand barometers | 03 | 62d605c6e4da, 197b32fb0f0f, f55c76bb188a |
| 01-PRD | Review mining 1 to 3 stars; wash test 10 times; kill a line 3 times on a panel | 05 | a36ca55acd6d, cc5525cdafc8, 956c62284f86 |
| 01-PRD | Trend tools (Trend Rocket, Exploding Topics, ad library); product-aware-not-brand-aware selection | 13 | 8b75ede22872, 48725fd2f914 |
| 01-PRD | Narrow ICP first (2M CrossFit and paleo), broader later; TAM pivot; contrarian ingredients; c-store observation | 07 | c37b669dd0a2, 8737923d6563, 65e6ba412a1e, d552995a5c78, 9e80874ceb00, 2044b40abf90, 84cee8bfb56d, 2984886c35ed |
| 01-PRD | Clinical validation before claims; capability-fit scan; launch on owned infrastructure | 09 | 903a160a459, 775b6e6ff8df, 384fcc700d97, da1c4ad0b07f, b4498bb660aa, 65823626690b |
| 01-PRD | 4-pillar brief (formula, fragrance, design, price); taste-maker panel; scent system; aisle walk; hero decided by sales | 12 | 37667c1a6d0e, 9130d21f0b19, 6ed958dca6ff, 1c99bc387faa, f5a23c680c87, 965a3d1500b7 |
| 01-PRD | Product selection: repeat purchase, emotional effect, efficient packaging; compete on format | 08 | 038fe4f3d870, 1982b3e1dece |
| 01-PRD | Second brand funded and seeded from the first | 18 | 931bf2d42178 |
| 01-PRD | Repositioning vs launch; SKU rotation for large assortments | 21 | 8edaaa4485cc, 7a75df0c27c6 |
| 02-AVT | Empathy avatar feed; data-derived personas (1 in 8 customers an influencer) | 06 | e66dd38f, e16ab1ce |
| 02-AVT | Layered demographic (fat burners, women, over 40); pivot only after multi-demographic test | 11 | ff32df14c8b0, 8bbceb08f413 |
| 02-AVT | Multi-avatar generic-store test | 13 | 3e91d8f9ae2c |
| 02-AVT | Unexpected personas; LLM angle generation 10 to 15; benefit pillars | 21 | 2ed7b60540d7, cd1f18839b86, e92050bf8727 |
| 02-AVT | Purple ocean, mass desire, stage of sophistication, contrast | 10 | 0a484f196d18, 99f786ee77e3, 5655eccf94a7, 3e457e257de6, 6fc58bfd3165 |
| 02-AVT | AI persona simulation from own research docs | 10 | 5cc2f2f1185c |
| 03-OFF | 5 offer mechanics; discount curves; contribution-max discount depth; full waterfall before a sale | 01p1 | 31e28984af3d, c92a82747e36, d7809c576fb8, 9ea687d35127, a7870bd441df |
| 03-OFF | Repositioning as zero-COGS offer; bundles; GWP at true gift cost; threshold from AOV distribution | 01p1 | f2929b62a6cb, fbf5c852d1d2, e345aac91cf4, 2b882f09e94b, afe614ed1856, be026fe672a8, 1a706c3de836 |
| 03-OFF | Flat discount 1 to 2 times a year, only for high-GM or C/D stock; new vs returning offers | 01p1 | 36326f28b88c, 2d88760c5b13, a1fd76b8d908 |
| 03-OFF | Upsell placement by friction; anchor high then downsell; 5 in-cart rules; RPV 10 to 15%; exit intent by stage; 4 offer questions; evergreen offer; offer beats account | 01p1 | af664909cd4e, 3d3e2b815f9b, 835b52ea1691, 1902fe9818ae, 26de2145522c, 03b1898ead39, 54348c1adb1f, 8aec1db231ba, f5e39801f58b, 3aa3584b7dc0 |
| 03-OFF | Pricing ladder and anchors from contrast; rejection-then-retreat as a real tier ladder; GWP as reciprocity | 02 | dce513894389, c7ac01349bb9, 45c33c914848, 739e469e9802, e9fddef96d88, 4c4ed8151f87, d690f71a75b1, d1fe88bdcd7d, 8d852dc8c90f |
| 03-OFF | Household decision-maker; exclusivity used rarely | 03 | fcb4ec9b69e0, 7880f75d131f |
| 03-OFF | GWP ladder $100/$150/$200; packs and pack builder; bulk pricing; staffed post-purchase upsell (5 to 15% of net profit) | 05 | 56b7435b66de, cc391f8fe191, c33859641d7d, f7efc2743826, 166329ced091, 19ecf70e4555, 6a750f82159d |
| 03-OFF | Consumer-surplus pricing ($10 to 15 WTP vs $3.25) | 07 | 744f2d6fbe49, 992289e5aab9 |
| 03-OFF | Offers in a high-CPM world; GWP arbitrage (MSRP $500, COGS $100); 15 offers a quarter by traffic source | 08 | 916278acd788, a3aae8bbd129, d6b5067b58b0 |
| 03-OFF | 3-tier ladder ($112 / $89 / $235 prepaid); term matched to clinical timeline; expert-access value stack | 09 | 1698727f88bc, 05f9ce1db6a4, 3c14ab66c8d1, 55be58bb0c65, fc2bdc9b74e2 |
| 03-OFF | Hero-SKU gating 30 to 40% above AOV; stockpile offers kill reorder | 11 | fd5777d14d59, 7555f8b740ac, 9bf05e0dda65 |
| 03-OFF | GWP that appears on camera; restock as validity marketing | 13 | 9d911f4de73e, b7d4878acc8a |
| 03-OFF | Profit play vs inventory play; offer ladder with triggers; discount-adjusted break-even ROAS | 15 | 9b4e9226481, e2262e74c26f, d6b1b339b607, 61f3aa873861 |
| 03-OFF | Middle-tier ladder; quarterly plan tested in isolation; bonus stack; restate guarantee at checkout | 16 | 30f3591e0db6, ba1c6ce5fe6a, 928d2ddfc162, f55f1e9b4827 |
| 03-OFF | No discount in premium ads, baseline risk reversal off-ad; cheapest SKU out of paid; scarcity only when real; free-shipping threshold over % off | 17 | 7999f7f71668, 375d99aa7abb, 3a1292e93ad7 |
| 03-OFF | Reprice down fast after a failed premium launch ($69) | 18 | 11347fa2b0f9 |
| 03-OFF | AOV without discounting or added fixed cost | 22 | 871d9318f |
| 04-BRD | Budget a brand line; $8M vs $300M account comparison | 01p1 | e08bf0b419e3 |
| 04-BRD | White space "overcharging and under-doing"; side-by-side visuals; giving as CAC arbitrage; founder content for recruiting | 05 | d728417ae4e8, b6b98fd3405d, 24bfd66860ae, 8e02c9fff8a5 |
| 04-BRD | Enterprise campaign design; funnel-tied big campaigns; viral-moment infrastructure; niche domination; judge sponsorships by deal size | 06 | 6c969802, aafa13e6, 480804bd, 4993433a, 054d2570, 316da3a1 |
| 04-BRD | Packaging in a saturated-claim category; brand-first color hierarchy; fix name with packaging; agency brief; gender tension; stigma positioning; non-obvious-but-true; credibility partners; crisis response | 07 | 4ff6b854477a, d4cb8111e899, a7781092cdd0, e9305d64f3f0, 1cd22fa872f7, 4d31ac1012b1, 533d4b53ef2d, 77feb6c7b006, d14808598a83, 7037655ae574, 93ad7e463793, 5dfd00a65b06, cf48c9f65acd, 14dca5a82dc8, 10689aea9077, 46802c2318be |
| 04-BRD | Break category color code (red vs green) | 09 | e1d2a371e2e0 |
| 04-BRD | Display-worthy packaging; founder-obsession moat; collabs for noise; brand spend once liquid | 12 | 41cc3a2cbaf5, d92731f1e097, 209d27872f4b, bb0b357e60fb, 522c1edf8b71, dedcbb054c21 |
| 04-BRD | Harvest vs create demand; judge in ecosystem; outside-account levers; retail content as authority | 17 | ec5bd4781c52, 00fc76514ab2, e2748fcc89c4, ea0fb51b4d36, eaa8aaeb8087 |
| 04-BRD | Emotional problem in a commodity category | 18 | 18c16e8562ed |
| 04-BRD | Narrow consumer, distribution moat, narrow niche premium | 03, 13 | 3fd749ca919f, 9bde353a7e8b, db5a21935060 |
| 05-SET | Localized stores vs one global checkout (UK 0.5% vs US 2.5% vs 5 to 7%) | 04 | c780e415d44d |
| 05-SET | Translate site and creative before opening a market; cross-border integration that breaks | 05 | 1bf2b0cb1bac, 9b738ddc9a70 |
| 06-MEA | 7-day click, 1-day view inflation 30 to 50%, existing-customer bleed, halo; subtraction not addition; metric pyramid; MER vs AMER; CAPI; GA4 fallback; Shopify reports unreliable | 01p1, 14 | 21ae950f3d4b, d18061f1791b, 7500786dbfd9, c2b721c34563, 4c923bbba4d6, 1dfa80844f46, 2326f545f479, e2b6cdb21e10, d63cd6fefbdc, 2d775e75662d, 5de99742a3a0, 3c73946c2bb4, 2c720c61a375, 7a6b5c93b855, 38c80ae68029, 256e8f1a95e7, d233cdfd3b00, a14d468f90cf |
| 06-MEA | Geo-lift design; lift tests by tier; CausalImpact; seasonal launch confound; 9-mistake audit; revenue-banded rollout | 01p1, 14 | 75660c5c38e6, ebddd1328afa, c357a526bf80, f78b03e4db0e, 926a75d6e756, d912bfa27ecc, 96e6e856fd7b, c049a4fab120, 33775b73749d, c3b26441e2aa, 23010ab3b691, 99402b442662, 28067949e768, 17393d9c2d71, 2b34d63c3b0e |
| 06-MEA | Metric reliability by account level; breakdown distrust; conversions by conversion time | 01p1, 01p2 | 5b34bfe523b3, a96c890428cb, b3d6e61e0a7a, 41fe6e957f15 |
| 06-MEA | Holdouts at $15 to 50M; 1% on tools; naming convention; pause-one-channel test | 04 | 0329cf172907, 89eb781b3bd2, cd334cfab060, 4fef2f81efe1, 7efbf56effb8 |
| 06-MEA | Post-purchase survey as attribution truth; survey share vs spend share; KPI window weekly | 05 | b22aead0c4cf, fcf99d9abd1d, 0e47a816e696, 0e1860afecb6 |
| 06-MEA | Chaos theory above $100k/month; ROAS model breaks at $20 to 50M | 06 | ed223dde, fd46c05f |
| 06-MEA | Multi-KPI ad judgement; daily burn and discount % | 08 | 222d8f7291df, 72a946cbac3c, 207581e0e4f1 |
| 06-MEA | Platform attribution off 5 to 10% or 30 to 50% | 10 | 64c447f737c2 |
| 06-MEA | Attribution multiplier; post-treatment window; marginal CAC; elasticity to cut only; November cohort | 15 | a0478e430dad, c310f482ec53, 1d313c3eb80b, a74069ce7855, 675de05124cc, 7473b6195d7f, ebb016b64886 |
| 06-MEA | 5-rung reliability ladder | 19 | 217c8dc47244 |
| 06-MEA | ROAS 3 flaws; metrics that hold in every context; healthy ROAS with flat topline | 20 | 53cff4b8747, c2f447b2849, 9497f75a4f1 |
| 07-LPG | Homepage by SKU count; PDP hero lifestyle; frequently-bought-together; CRO stack; mobile first | 08 | 96733f0bc647, 622c857be244, f792955c5fb6, 0098da2a7acb, 0ee96bf492bf, b9c6647eebf7, 48f063960d40, e98be365e095 |
| 07-LPG | Angle test before landing page (12% vs 1% CTR) | 11 | 6b9ad04ab9c3, a335ae58c3ad |
| 07-LPG | 3-tier landing routing; persona pages; hard-to-copy trust | 16 | e4fe53bab69e, a420b37128144, 27b9f5d576b0, a72c28e35ff9 |
| 07-LPG | Collab lander; category grid with daily owner (fashion only); unused pages; CRO fundamentals then 5 to 10% split tests | 17 | b60bbbefb2a7, c59f7a0191bc, 59a49f7f9d40, 7c106a91e81a, f7b19b16475e |
| 07-LPG | Congruent page per repositioning angle | 21 | 00e148e02113 |
| 07-LPG | Single CTA per step (bystander research) | 02 | ab6cbc054bf3, e23f6027a769 |
| 09-CRO | One variable per test; fold check; simplify PDP | 05 | 2fbed3721ea5, bf63ed67f8b3, e6cea5c9afd4 |
| 09-CRO | Funnel "hose" instrumentation; break the funnel before launch | 10 | 4fc18ca8c1c4, 5d4f23b0fe19 |
| 09-CRO | Verifiable social proof; scarcity tied to real constraint; lowball as checkout audit | 02 | 2610a89b3503, b00c278eaa05, d147d0be41fb, 743b6f53913c, fdc00c6aa447, cb31b8de451f, e0ab1f148d59 |
| 10-MCR | Concept matrix; persona, angle, offer, format order; hooks and bridges; format choice; VSL and advertorial; testing cycle; creative metrics; volume and hit rate; fatigue tactics; team by tier; AI in the middle | 01p2 | dac13325f1bc, 0f6cdc6afa17, e218c186102a, 010fe64918f4, c9cab64dcc73, bc784b37d696, a290245745d6, 3b07bb97fef4, 9c15aae468c2, b86b75e9bce9, 312400b7ccab, 19ad3f95102c, 5e663b2acdc6, a7eee2af5137, bc1fb281f2e3, 8004c3204936, 9b60e827e51d, ba82a65b35b4, 4930a1df56a6, 6b0a6f82bca6, 61ad59932aa7, 9d81ae41459e, a9d4d1b724a5, 3ed85b1ffd80, ec0c882e1e06, 1deded070dbd, bd9a8085893c, 02326c43f14a, 3ebec38bdf56, e6675d2d6fbe, 8868bab7b40d, 0b902cecf95b, e530277843071, 3412220fa646, 3ae202bfc21a, 22138a212ab5, 140b0e63185d, ee7169c0fb38, ec070bd2a240, 748e28ee574a, 01aea02748b6, 1f2c53df551e, f7d41ac1c4b7 |
| 10-MCR | True creative contrast; 1 to 3 seconds; UGC gifting 2 per 100; mine the archive; whitelisting fame irrelevant | 04 | 5be5fed1c72d, 954f15424bc2, 93bc573f154d, fc7c16b38b65, 8fa3a6c48b7b |
| 10-MCR | 4 to 6 openers; 3 creative buckets; 8 of 10 quality bar; company-wide idea channel | 05 | 9bb7e2b3f539, 431a46633c1b, f48f5e60e38a, 62f6d773086a, 6610acb913ba |
| 10-MCR | Staged AI adoption; systems not trends; idea reuse line | 06 | 03f7a0ba, 470629aa, 17193941 |
| 10-MCR | Smoke test angles with statics; native placements; creative as targeting; briefing editors; media buyer as creative strategist; clipping marketplaces | 08 | fc880a4db350, afd9b4efb691, d78d15b92404, d2899427c971, a71d44047464, 8aea6aee665f, b19555ac55d8 |
| 10-MCR | 1,500 active ads; 75/25 statics to video; AI ad timed to event; creative diversity as constraint | 09 | 603ebe25e9d5, 2aa5d495130, 7d23a954f5e, 3c104e877904, d7225a2807fc |
| 10-MCR | AI competitor-scrape and UGC workflow | 11 | e5199936326a, a984fdf4f581 |
| 10-MCR | Format mix by spend share; statics legibility; 4-phase creative; overlay evergreen; judge on CTR/CPC at ad-set level during BF only; creative as CPM lever; competitor scrape | 15 | 0fd306b87cfb, 088ef4385388, d6a9aa0c6869, 7c0dc6951b2c, 88407c078150, f9f39dcd376e, 9f9579f3d2c0, 7dc76b3e9b9f |
| 10-MCR | Clock script; persona clone; mechanism first; awareness-stage mix; consistency audit | 16 | f8de417026bc, 49962212b27a, 59b0f846c0c8, bd778e96d24f, 095521571e86, 2e205c8f91d2 |
| 10-MCR | 8-beat script; one named mechanism; need-first for expensive; silent multi-product video; six-format map | 17 | dc5261d74f44, 131fc4f2bcc0, ac993ebaf7d1, 82172d90ee14, d3b243c83ed2 |
| 10-MCR | 200 creatives a month floor; inflection with paid and creative supply | 18 | bbac1e69e635, 1c0184cbc727 |
| 11-ADC | Hook 80/15/5; PIG hook; one awareness stage; research 80%; customer language; swipe philosophy; copy vs content; emotional delta; clarity over polish; disguise; assume nothing | 10 | 7c32ef7f2d80, 7d460350a380, f24960c6f7b6, 62247a5dc49e, 4d3bc6c7e698, 12f592a7e391, 5c6cc037d679, eb0b904a4894, 91eeaf1e059b, 42a366d5ecc7, c311dc8298cd, 6e85c6d4738c |
| 11-ADC | "Because" clause; similarity proof; authority relevance in copy | 02 | a3af94f07c08, 2afb006d52b4, 00b1280a3b63, eff569999325 |
| 12-GAD | All Google Ads structure, PMax, Shopping, bidding, GMC feed, 90-day rollout, root-cause diagnostic | 01p2 | 92200eb95b45, 5d8be0c613b5, 0103a8c9bea0, 50d06003decd, 8c4e6e2d406b, 299de15a096a, 2b7d05cb2e3f, 0d34948521a9, e1258c1c01bd, 926e49f0a825, cfc0bb5b70ee, 28532c9e9701, bb73c455dd9a, 37eb427df717, 7881306718d9, 791e1a8f256b, f6bbad74d2b1, 50032f16a8cf, 6e67e3c7c443, 7421bd80f152, f8b37ea10202, ac4bf9ad64fd, fb780cdc68a6, 46006b8261d1, c1d0d2b869b8, 74d14b3daff2, 39809745fc54, 5bfbaaa5f311, 9fcbc9897f69, ed7c1f01178a, fee71c6e7a9f, aaa2978ee3ef, 7748b51c5778, 19d3b54fbeeb, 6ad389eace76, 1067951c3e42, d0bb3b797336, 859209042dcd, 34e9220c4fce |
| 12-GAD | Branded search cap ~1% (Ridge holdouts) | 04 | 1f911edec6bb |
| 12-GAD | Google halo; brand-term waste | 14 | 71083548afed, 606c03936b6f |
| 12-GAD | Google as prep platform at BF, not scaling | 15 | 16f43795044b |
| 13-ORG | In-house creator team 15 to 25; VPN scouting; creator CPM at half Meta CPM; loose briefs; no-code program; follower bands; TikTok Shop affiliate separate; events as content; founder brand | 03, 13 | 2218553363b7, e93a4a1fe046, 14e767cc9e9b, 063f442d74a8, f0c35189d69e, 56a6106683a4, a67c4bbfd5c3, a5e7b7863c43, 7196b283bc16, 2ad095563d0a, e4aa7b7065d9, ac7a5c24d798, 9440e57d0b39, 6a3c3dd9f14f, 299cb75107f7, faded9a8b79e, a536655a1684, e8563c906f7a, 5df5a9e8c019, 226149210a30, 096660c8b6a2, 2cd965d92f02, 38e857b80873, 66600c6c3ffe, a60bd45558c3, 607dda5aa8c8, c1c1f0f794c4, 92c2d1e93cf4 |
| 13-ORG | Sponsorship: broad and cheap then deep; non-endemic; code plus URL; creator equity partner; X for founders | 04 | e6cb05526e60, 47d290ff4340, 7e12fa08f9b3, 175066c0600e, 793682953546, 1d505dda7fcc, a05b57ecb16d, 3c74b42925fa |
| 13-ORG | Organic-to-paid; tribal pillars; formats; trend SLAs; creator volume; two-tier briefs; targeted creator metrics; repurpose; separate accounts; customer flywheel; wheelhouse setting | 06 | f763727b, 45b7cff3, cc68c239, deb34829, 563c88af, fb1fc2c1, 296fd9cf, 4a1d62b4, fbd2c3f2, 1035e4c1, 4c92b8fc, d221ebb3, a3921462, dcdda7a9, 6f1fb6f6, f75f881a, b9b02e8b, 115d6147, d4a06472, 95cf0951, 139e192f, c5b670d4, 86a0620c, 570496970, 9084311, 56b30c64 |
| 13-ORG | Sampling 10% of marketing; pre-launch 6 months, 5,000 giveaway, 40k list | 07 | 587671f8263f, c8c89832c5b3, 654aeb3e25b4 |
| 13-ORG | Founder content system; building in public vs key-man risk | 08 | 35d275e5755e, fcb510de5279 |
| 13-ORG | Celebrity equity 3-year minimum; seed inner circle; golden ticket | 09 | 561de6374d6, 724b21f679d0, c15d3fb275ab, 98763258984c, e466b46bcbdf |
| 13-ORG | Founder brand as distribution | 11 | a901d93b0685 |
| 13-ORG | Equity or royalty ambassador cost declines as % | 16 | 3b0c2850367a, 1eb397831f80 |
| 13-ORG | Affiliate floor $1,000 or 15 to 20%; micro-creators under 10k; treat creators like staff; promote to recruiter; 5 to 7 posts a day; repurpose; AI hooks; whitelisting subset | 18 | abdbf1926c47, caf5937eab0a, 3f688d13c219, 09073df9ee81, 80bd8aab351e, 17f9e8e7500f, d6035cb037ec, baa638798686, ae37b5d39c3e, cf2f42e698fe, a84d20a1386a |
| 14-EML | Welcome flow as retention asset; discount 10 to 20 to 30 test; hail mary at 120 days; retention before discount | 05 | d7082f8c3c81, ee6015291fc4, 5e6576835e07 |
| 14-EML | RPR by segment; plain-text founder email; response campaigns | 08 | 3f130bc491dd, d68ba58bd922, 1e164e5e7ed1 |
| 14-EML | Flows as precondition for paid (15% lift); 90-day habit sequence; incentivized surveys; owned list not a cold test bed; identity-resolution legal check | 11 | 36f24e817a8e, bf5f23012c88, 414f3d559f4e, 2a60e95ff096, e17963c7293b |
| 14-EML | Reciprocity in email; bad-news sender split; "you promised" trap | 02 | f312371dc69f, 09edbcf0efa2, 38c98207d034, 5d3184b62ffe |
| 14-EML | Owned vs rented channels | 19 | 9f8e357bd0b2 |
| 14-EML | Klaviyo 50% myth; 5-day open is view-through; flows cannot create retention | 20 | 0c79d63f1e16, 0005f05fcb3 |
| 17-CXP | Retention phase after acquisition; 3-month tier as first retention move | 09 | 7d3b5a19ab1e |
| 17-CXP | Ritual products retain with routine-havers; portfolio migration; community as retention | 03 | d788451e257a, f9b199b5a8d3, 2ad217557e32 |
| 17-CXP | Wow budget; AI routing only; all-hands customer calls; membership club; advisory group; personalized video | 05 | a2ffc00dede1, 2c4a21f43820, feb29848807a, c34cee3e77b8, 60728fbd9631, 32991ec33169, a0ff95163c90, b6356b81e142, 1667a4459343 |
| 17-CXP | Churn map day 1, 28, 31 to 45; cancellation branches; surprise budget; one-person referral ask; surveys | 08 | 9edfe64030cb, 35f9701b3753, f029acb2b668, 409f2d205b7d, f9aac0151b5e, fa9fee3e4288 |
| 17-CXP | Founder reads every review; CS as diagnostic | 12 | 09624658c7f6, c769c358508d, 91bd091d5123 |
| 17-CXP | Post-purchase goals and commitment; onboarding questions | 02 | 7a84d0a05040, cf409d4e384d, de1dbe05496e, 3f1108aa246a |
| 17-CXP | Retention backend from day one; replenish 30/60/90 | 10 | 3d5541e52ed0 |
| 17-CXP | Cohort analysis not tiles; category bands (fashion 55%, CPG 110%, furniture 0%) | 19 | 676a17d4a712, 376c8c477e8f |
| 17-CXP | Returning rate lever (80 to 90% of net profit claim) | 22 | 5613ddc47 |
| 18-COG | Supplier terms 15 to 90 days; safety stock; $25M revolver; over-betting inventory | 05 | 765be2933ced, 5529a92593b3, 88dae8d1f315, 1dcdad671ee9 |
| 18-COG | Retail: prove one chain, overproduce for POs, buyer changes every 2 years; retail exclusivity; demand before pitching; POs | 03 | aae76c2599ce, c4aaa2c825af, b8824848deef, 1bc6acca39d7, ae001e348577, 2e93f1412716 |
| 18-COG | Mall foot traffic not standalone; Leap; digital proof before big box; Target via integration | 05 | 4bdfa7fa6c39, 5115e27797b5, 664e2cb90e53, 57085d0ee6ad, fb46fba302bf |
| 18-COG | Single-source supplier; MFN; vertical integration; regional then mass retail; distributors; trade shows; ingredient upgrade | 07 | a7c30506fe46, c4432820ebd9, 248161a47836, 05f735247a96, b2b445ceda24, 0508e490d885, 30db6707bf15, 22da9c339149 |
| 18-COG | Contract manufacturers via big-brand supply chains; vet capacity and certs; ~10 manufacturers; retail cash-on-shipment | 12 | de43bdcfd16a, 6eaf0acca2a5, f6567143a45c, 2590378c1767, 4e93962abaeb |
| 18-COG | 3PL and 4PL sourcing; international shipping cost | 04 | 36fa738a669c, 406f95cc2038 |
| 18-COG | 3PL/4PL paperwork before peak (inventory seizure) | 13 | ac76fdafcc3e |
| 18-COG | Sellout capacity crunch; 3-month restock; support scaling | 18 | ccdffe1f5d76, ea32886fb87f |
| 18-COG | Sell-through and MMU as cash levers | 22 | 7fe3a7782, a3a00f7b9 |
| 18-COG | Vendor "free" offer defence | 02 | a2d0ba8b9063 |
| 18-COG | Retail-entry decision on leverage; Grade C stock into other markets | 09, 01p1 | e3a6e7b106c2, 8669aea558c2 |
| 19-WLD | Golden ticket experiences; TikTok Shop fit; stunts; AI ladder | 09, 04, 05, 10 | aa53fdd80c81, 3127f1396d5d, cb6b3e45c875, 1702c2fc493d, 80dc4498105e |
| 20-FIN | P&L waterfall; staff classification; waterfall pricing; forecasting; CCC; inventory grading; balance sheet; contribution margin back-solve; brand line | 01p1 | f82391a766c6, 29f6666ae310, 2ddbe78b9877, 312d5fc90827, 2f48255ebfdf, a3b5f20b67e2, 7e066cd286cd, eecd54f14ae1, 8669aea558c2, 731ac683ccf3, 002934fe70f3, c8cb8294b3f6, 9840c923e170, 2ba72747cc86, 7d67a42b0d81, 82a77847f675, 812745ee3d05, d3fd934664cb, 6b261e1e25a5, 50ee11fa1685, e3e82328c6eb, 53c86fa371bb, a39261c57a5e, 975ff246ddd2 |
| 20-FIN | GM as delivered cost; working capital tools; LBO mechanics; PE expectations; sale timeline; deal terms; exit timing; equity instruments | 04 | f78f584be878, e9d130295214, edf06536c8b7, 6713ec746162, 796cf06f23d1, 20817201b1bb, 78f51f3e7f41, 1d505dda7fcc, d30839f7b7a0, 31c8109a299f, a9c862b663ce, 12509c82d440, f2ee818aa879 |
| 20-FIN | CFO early; raise as last resort; supplier finance | 05 | a9156795ce70, 88dae8d1f315 |
| 20-FIN | Bootstrap deliberately; partnership 1+1=3; EV test; spike cash to inventory; diversify channels | 03, 13 | 74016741fdbc, 91a2ee5c0b52, f90e66edbcd2, 64892ed4faa6, 9994f24661, 492ad9d02ac5, 414454f50f31, c11ca588fe21 |
| 20-FIN | Exit multiples; value drivers; cash flow before exit | 13 | dc145902632, 0355e66068, 9c1c2bba079a |
| 20-FIN | DTC GM 40 to 50% at launch; exit buyer type; competitive process; capital efficiency; founder, CEO, shareholder roles; 3 inventory numbers | 07 | cb72f5171b60, 3a6d05bf8a2a, 399d57d8b870, fca479f57f8f, bd022d81f786, acf4c08a857a, 4269b434597c, 4410f4acddbe, cb3fb2fcbada, ec589900e2d1, 58e0fc375c4c |
| 20-FIN | CAC:LTV and payback gates; upfront revenue recognition; treasury; investor numbers; hard pivot; no-diligence investing | 09 | d222f5b460d3, aac81fd83b5b, 9d090dbadbb0, 5bfb3732fb33, fd68d33918f8, ff64a574212a, 383edf00490e, 6671e33e746c, a15322158e85 |
| 20-FIN | 3-layer economics; LTV:CAC 3:1; bid headroom | 10 | cd2ec58854db, a90f86deab35, 81635c2e6b25 |
| 20-FIN | 300 screen; 12-month LTGP vs Day-1 CAC; make CAC work | 11 | 9e6eb4c8669a, e5cd6f1465bb, 8914117448ec, 0ac75b0ea6cb, 5baa55c8c61a |
| 20-FIN | Secondary PE; partner selection; founder presence; sale-ready | 12 | 93d8ebb61724, c3cde0fb2643, 8b03a5eaa976, 9421982e1ec7, 629185c92369, b0c7c3317789, afb8409d019a |
| 20-FIN | MER vs AMER; profit contribution formulas; LTGP:CAC bands; COGS tagging | 14 | 3c73946c2bb4, 6f250e030e8c, 777732c1773f, b1834ecfb2a1 |
| 20-FIN | CAC vs GP; LTV horizon; ARR; cash vs profit; CM definition; payback window; cohort maturity | 16 | c52a5730e858, 070e0c60e2f7, 70936c5570f6, 9cb4c7dc31a1, a75628e1fb76, 179c5947001a, 3ca0714a9b6d |
| 20-FIN | Death spiral; bands; CAC decomposition; 2-P&L split; funding a sub-1 ratio; opex creep; first-purchase norm; timestamp changes | 19 | 6da370548f56, 176c49fbae67, e0b1085f47a3, 2ee0c2788115, a6b527c71dec, ceffceaa4132, 7b24b5654a81, 577a55dfd0ec, f0fd9a23a268 |
| 20-FIN | Scaling vs profit; 20% net bar | 20 | 7ea79f0c239 |
| 20-FIN | 6 cash levers; 1:1 opex rule; 60 to 180 day lag; compounding levers; cash vs net income | 22 | 7054802f6, 71b3d1891, 32440a917, 5007ba2e3, 8105508e9 |
| 21-OPS | Opex as profit leak; creative team by tier | 01p1, 01p2 | 9840c923e170, e530277843071 |
| 21-OPS | Metric ladder (buyer, paid lead, CMO, CEO); make-money vs save-money roles; daily standup rhythm | 04 | dd91a3f96554, 071715bc72c9 |
| 21-OPS | Hiring homework, 1 to 1.5 months, under 5% evolve; EOS after stability; kudos; elite generalists | 05 | d281ce11c9df, c622b95664bc, dae1bdd430e3, d84592054461 |
| 21-OPS | Media pod; kill committee reviews; creative strategist role; meeting cost; edge as org grows; build vs buy; underpriced creatives | 06 | 30aac5b8, 03f5ace4c, 4995b579, 717a1b23, 232a3d43, 8c3677c3, cfdf31a0, 9317da28, cb291f7d, 21ed4b4d |
| 21-OPS | Servant leadership bottleneck; team before the bet; humility | 07 | d52e908d7529, 896e2a297f55, c840c7b9163f, 09ddb10b541b |
| 21-OPS | Founder runs ads to $10 to 30k/month; rollup one-CMO failure; routines | 08 | af4b9f233f1a, e3318059ec3e, b909a511bc14 |
| 21-OPS | 5 to 8 person decision loop; always-on culture; AI native | 09 | b5802ce3e875, 9d66422ea27f, a4a2ced6122b, a4641f67247f |
| 21-OPS | Entropy; no clean hands; money loves speed; compare to own data; intuition as test data; break rules after learning them | 10 | 25d1aef326ee, 11e43df4c9d2, 899c0cfa0cb1, 391c879b2d86, 455d2f7749e9, c5c9a8f05d83 |
| 21-OPS | Pods with P&L; districts; AI intake funnel; SOP as promotion gate; manager buy-in; entrepreneurial hires; hand off first; plateau rebuild | 11 | 3bb0382ee1c9, 2176a7a0631f, 725bc1a75caf, cc06d2a56717, 9b674f4dc81a, a7c4f87a603d, e507fc4479e3, 99d2957b0b33, 38ec5dd1be44, 4fe972618132, ba53cc416810, 90ab58908635, a56c19b082b4 |
| 21-OPS | Remote understaffed; LinkedIn sourcing; hire weakest function first; trust leadership; AI for retrieval; discipline; doer over planner | 12 | f1602f3ade20, 1cd6bcabe32b, b6ad829d22ec, 281ef6e02753, 0d5cadae700b, 75db67df1097, c6c172c7233c, 5efa62a4a8bd |
| 21-OPS | Hiring by stage; taste question; pain-point hires; in-person by function; founder as environment builder; EA; emotion control | 03 | 2d7a3ee723c7, 635bd0289e24, 3dee9502ba57, 946ef10a2730, 343ad0cbf415, a69727c31c29, 8f7e058f72a8, 2a23256062f6, 9bb47013cb56, d4d6af3eb796, 2065c258255c, 816304aac815, b2f690710bcc, e309e0b2cd3f, 2f351c65c24e, 3b9dee739e33, 2d121e3f9ded, 9b90e19c9efe |
| 21-OPS | CEO replacement archetype; founder mindset (anxiety, associates, presenting, truth, passion, billionaire trait) | 13 | 116713e4f02a, a0f3b2b3fa6b, 3ae237242a99, b7325aad598c, 0bccc8b217ae, f42f58122d64, dd33fa2d9cdb, e68d1fc98494, 720de20ad84e, b11aa79f3613, 0de14be93710, d0dea192a922 |
| 21-OPS | Peer network for growth-stage problems | 18 | 4bb5f94ab4b7 |
| 21-OPS | Fixed opex cut hits cash 1:1 | 22 | 71b3d1891 |
| 21-OPS | Record independent judgements; praise contests as selected material; time-travel question | 02 | 2f71ca0f90fc, 089b4cae5fa1, 239a4c7c7019, 95e9000831b0 |
| 22-AMZ | Sell direct to Amazon; counterfeit; spread SKUs; external traffic to Amazon; Amazon rank before retail | 03, 13 | e9c97672d49d, 5003bce29ee7, 9f5bae6b1128, aefe14739fde, 5630f92d6cff |
| 22-AMZ | One price across Amazon and prestige retail; organic rank before ads | 12 | 1f023eb429f7, 2e790ab86c57, 65240921911c |
| 22-AMZ | 2% Amazon while 98% DTC | 09 | dfb0138526ec |
| 24-DEP | Consolidation; cost caps at ad set; Andromeda; no daily tweaks; 2 non-negotiables; 5 diagnostic questions; campaign justification; retargeting capped; scaling campaign $400/day; test budget CPA x3 or x5; test duration; page cap 300 to 500; sub-$50k, $50 to 250k and $250k+ structures; ABO vs CBO; ad-set composition; settings to turn off; DPA; existing-customer budget in dollars; 4 low-spend mistakes; second ad account | 01p1, 01p2 | d39e9023291d, f72ca32e9529, e93ca591561c, f7b8e05cda3d, 7b669e91a2f0, d9ebea42b405, 4bddfe132ec2, 90fdf6692e74, 6d6ffaa950ec, 34509036c871, 1fe205b60578, 235886e51a03, 88cbc55b3268, 341617047285, 69a7c7195336, 81e15385dc8b, 1e8b0ae41022, 2dbc68e5e82e, c9a888b1f02e, 0dd3aee5c557, 5de48d3e386a, 6c9368a6f500, 3b07bb97fef4, 159829ec7374, d00fe7fd4c3b, 9190a63c0c09, 345054044d8c, d45d9720ad61, afc96213f022, 4101599d2222, 00054444d5a7, e800ec50f078, fa103e10c7f6, 421e7aee0498, f7563f8a98f0, df7a0134cc56, 587d3d72e000 |
| 24-DEP | Channel diversification with a Facebook core; test new channels; live-event deals | 05 | 0cfb7300187c, 4c2d5d5eae2d, b2a4cf038faf |
| 24-DEP | Zero-to-one test campaign $10 to 50/day; doubling framework; 2-signal creative read | 06 | 92354a4e, 13f04667, 69f4ae6b |
| 24-DEP | Story folders not funnel stages; 70/30 winners to tests; weekly creative cadence; 30-day bench; tranches of cash | 08 | 2c6edc3dae30, 1dcea062829e, 5e5bc3b4063a, bb0e6110d983, 9d6086554618 |
| 24-DEP | 85/15 Meta to Google held; scale Meta before diversifying | 09 | 09fbaaa5df5f, 0805d0da06ef |
| 24-DEP | Over-segmentation; existing-customer exclusions; DPA; tertiary channels; traffic objectives need measurement | 14 | e7a390a10174, b2092d04659e, 79b6665ba35d, 94dc95d044bc, 703558b83184, a7b82c68d543 |
| 24-DEP | 3-day rolling CM3 rule; pacing sheet; cost caps diagnostic; hourly multipliers; base and stretch gates; never turn off evergreen | 15 | 3b63d06d5486, 5afc0c5d082f, 4afe3a4577de, 6f476966cae3, 71ba87612a01, 7c0dc6951b2c |
| 24-DEP | Rotation vs holding winners | 17 | 31cd05ed427e, cdc15b2f036c |
| 24-DEP | Existing-customer frequency 20 to 100 found, ~10 gut check; repurchase cycle; organic-follower hammering | 20 | 722e2752eec7, ca90d7c1ca85, c1b04bc58a5a, 706b85f45d0 |
| 24-DEP | Angle saturation as TAM ceiling | 21 | b2da5bc185dd |
| 02 (keep here) | The 6 principles, contrast, defences and their operating conditions | 02 | see section 3.E |

Cards not listed above but present in the sources are cross-domain and are cited in sections 3 to 8 of this playbook.

## 2. Inputs the agent needs

| Input | From where | Required or optional | Why |
|---|---|---|---|
| Net revenue by month, split new vs returning customer, with order counts | Data layer | Required | AMER, CAC, new-customer profit contribution, the 2-P&L split (3.A, 4.1) |
| Ad spend by channel by month, including influencer and affiliate spend | Data layer | Required | CAC, MER, AMER, channel mix review (3.D) |
| Per-SKU COGS, freight in, shipping out, pick and pack, transaction fee, refund allowance | Data layer, brand record | Required | True gross margin, break-even ROAS, discount modelling (3.A.4) |
| Cohort repeat curves: revenue and gross profit by acquisition month at day 30, 90, 180, 365 | Data layer | Required for LTGP:CAC; optional for a first health check | LTGP window, category band, November cohort check (3.A.8, 3.F) |
| Inventory on hand, on order, sell-through per SKU over 30 days, supplier terms, lead times | Data layer, brand record | Required for cash model | CCC, 6 levers, peak readiness (3.A.11, 4.9) |
| Opex by line, fixed vs variable; cash balance; debt and terms | Data layer, user | Required for cash model and founder decisions | Opex creep check, funding decisions (3.A.12, 3.G) |
| Stage: trailing 12-month revenue and current monthly ad spend | Brand record | Required | Stage plan selection (3.C) |
| Category, price points, SKU count, hero SKU share, subscription share | Brand record | Required | Archetype and lever choice (3.B), offer routing |
| Channel mix today and channels available (retail doors, Amazon, TikTok Shop) | Brand record | Required | Channel review (3.D) |
| Ownership, capital position, investor or lender covenants, exit intent | User | Required for 3.G, else optional | Founder decision memo |
| Peak-season calendar: prior-year hourly revenue and spend curves, attribution window comparison | Data layer | Required for 3.F | Pacing sheet, attribution multiplier |
| Existing-customer ad frequency, share of spend on existing customers | Data layer (Meta read-only) | Required for bottleneck check | Existing-customer bleed, non-incremental spend |
| Competitor ad library scrape, public pages, any public filings | Web, inspiration layer | Optional, for teardowns | Section 3.H, 4.7. Signals only |
| Current platform attribution defaults and feature names | Web | Required before any `[verify UI]` rule is acted on | Section 10 and 11 |
| Objective for the period (profit, cash, growth, exit) and risk appetite | User | Required | Resolves several section 7 conflicts |

## 3. Decision rules

Numbering: letter for the group, number within it. Each rule gives the rule, the condition, the mini playbooks that support it (01p1 and 01p2 for the parts of source 01), conflicts, and card ids. Where several sources say the same thing, the merged rule keeps the strictest condition. Where one source says it alone, the rule says so. Sources 01, 14, 15, 17, 19 (and likely 20) are one agency; when only they support a rule, that is one voice restated, not independent confirmation.

### 3.A Unit economics and the growth model

**A1. Data integrity gates every other decision.** Treat the business as 3 stacked pillars: data integrity and measurement at the base, creative velocity and diversity in the middle, technical account structure on top. Fix the base before touching the other two, because creative and budget decisions optimized against false signals compound the wrong way. Condition: always; but a single-channel brand with no tracking at all needs basic tracking first, not a measurement hierarchy. Sources: 01p1, 14 (same agency, one voice). [4f911dc82a03] [4f1e89e8a798]

**A2. Compute every ratio on net revenue after refunds and discounts, and split it into new-customer and returning-customer lines with order counts.** Gross revenue compresses once returns process (fashion 10 to 80% refund rates per 01p1). Returning-customer revenue is mostly a function of product and category, not of this month's ad spend, so it must not be credited to paid. Condition: always. Sources: 01p1, 14, 19, 20. [1dfa80844f46] [6b261e1e25a5] [6f250e030e8c] [975ff246ddd2] [a6b527c71dec] [722e2752eec7]

**A3. MER is the CFO's control metric; AMER is the paid-media metric.** MER = net revenue divided by ad spend. AMER = new-customer net revenue divided by ad spend. MER can rise (4x to 5x) while AMER falls (2.0x to 1.8x to 1.6x) because returning revenue grew; scaling on MER in that case starves acquisition. Hold the CMO or media buyer to AMER and profit contribution. Condition: any brand with meaningful returning revenue. AMER targets are not comparable across brands; a 60% gross margin brand can run a worse AMER than a 40% one and be equally profitable. Sources: 01p1, 14, 04 (Ridge's metric ladder: buyer owns ad ROAS, paid lead owns channel MER, CMO owns digital MER, CEO owns holistic MER). [1dfa80844f46] [2326f545f479] [3c73946c2bb4] [dd91a3f96554]

**A4. Use true gross margin (fully delivered cost), never product margin, for any marketing budget decision.** Product margin = price minus unit cost. True gross margin subtracts shipping out, pick and pack, transaction fees, flow-through sales tax, landed freight and a refund and discount allowance. A $100 t-shirt with 70% product margin had 24% true gross margin in 01p1's example. Yeti's public gross margin is about 51% (04). Rahal's launch gate is 40 to 50% gross margin after every fulfillment cost for CPG DTC (07). Ridge's new-category bar is about 75% fully delivered (04, one operator's bar). Condition: always; recompute per SKU and per discount scenario. Sources: 01p1, 04, 07, 14. [7d67a42b0d81] [2ddbe78b9877] [f78f584be878] [cb72f5171b60] [3a6d05bf8a2a]

**A5. Tag COGS per SKU so gross margin is live, or every metric is wrong during any discount.** A 20% storewide discount on a 50% gross margin product drops gross margin to 37.5% (a 30% relative drop) while a flat "our margin is 50%" assumption shows no change. Condition: always; mandatory before any promotion is modelled. Sources: 01p1, 14, 19 (cohort GP from actual COGS, not assumed %). [53c86fa371bb] [b1834ecfb2a1] [676a17d4a712]

**A6. Never judge CAC alone. Pair it with first-purchase gross profit on new customers only, then with cohort gross profit over time.** CAC = total ad spend across all platforms divided by new customers in the period, from order data, never platform CPA. First-purchase GP:CAC below 1.0 means the brand depends on repeat purchase to break even on that customer. IM8's disclosed figures gave 0.51 in July 2026 (AOV $212 x 58% margin = $123 GP, CAC $239) and a 6-month cohort GP:CAC that fell from about 2x to 1.03x over 6 quarters as volume scaled (16). Condition: always. Sources: 01p1, 14, 16, 19. [82a77847f675] [6f250e030e8c] [c52a5730e858] [3ca0714a9b6d] [176c49fbae67]

**A7. Break-even ROAS = 1 divided by true gross margin %. Break-even CAC = gross margin dollars per order.** Recompute both at any discounted price with all cost lines. Break-even ROAS rises linearly with discount depth; the ROAS needed to hold a fixed contribution-profit target rises faster than linearly, so some discount depths are unreachable. Condition: any product, any promotion. Sources: 01p1, 15. Caveat: 15's worked example (2x break-even moving to 4.5x at 40% off) does not reconcile with its own formula; use the formula, not the example. [c92a82747e36] [b539f0c8f5a4] [a74069ce7855] [61f3aa873861]

**A8. LTGP:CAC in a fixed window is the one comparable metric across time and across brands.** LTGP = gross profit (revenue minus COGS minus cost of delivery) over a constrained window: 30, 90, 180 or 365 days by category repurchase frequency; never an unbounded "lifetime". Bands, all one agency's heuristic restated in 01p1, 14 and 19: below 1.0 = death spiral unless retention is exceptional (called about 0.1% of brands); 1 to 2 = workable but tight, needs lean opex or high volume; 2 to 3 = scale here; above 3 = leaving money on the table, unless cash-constrained (the exception 14 states and 19 omits). Other sources' targets: 3:1 baseline, 7 to 10:1 for high ticket (10, one presenter's heuristic); 3.0 to 3.5x CAC:LTV on a 24-month horizon (09, IM8 founder claim); IM8's disclosed "3:1" is a 36-month projection from a 20-month-old oldest cohort (16). Condition: the band is bounded by category; furniture and homewares show near 0% day-365 GP lift, fashion about 55%, CPG and supplements about 110% (19, unsourced vertical figures). Sources: 01p1, 09, 10, 14, 16, 19. [50ee11fa1685] [e3e82328c6eb] [777732c1773f] [e0b1085f47a3] [a90f86deab35] [d222f5b460d3] [070e0c60e2f7] [376c8c477e8f]

**A9. Set CAC targets from your own LTV and repeat data, and target near-breakeven on first purchase unless retention is proven.** Ecommerce is not a service business: consumers are "lucky" to make a second purchase, so first-purchase profitability is the norm (19). One-off products aim for first-order profit; strong repeat justifies break-even or a small first-order loss (08, Breeze $85 to 90 target, $120 to 130 ceiling). The 12-month lifetime gross profit method: pull customers who bought 12 or more months ago, sum their gross profit over the next 12 months, and size the allowable Day-1 loss from that ($60 CAC, $40 first-order profit, about $400 backend in 11's example). Condition: needs 12 months of purchase history; recent buyers have incomplete data. Sources: 08, 11, 19. [207581e0e4f1] [8914117448ec] [0ac75b0ea6cb] [577a55dfd0ec]

**A10. Payback period is the second gate on spend, and short payback is the norm for an ordinary operator.** IM8 states under 4 months blended as its gate and calls under 4 excellent, 6 good, 12 weak; its host calls 6 to 12 months "world class" for a competitor in the same breath (09, unresolved). IM8's actual 6 to 8 month payback window was funded by a $1B non-dilutive facility that pays 70% of each cohort's upfront marketing; the teardown calls copying that window "ridiculously risky" (16). Condition: recheck payback after any planned spend increase, since rising CPMs lengthen it even if trailing CAC:LTV looks fine. Sources: 09, 16, 19. See 7.8 for the funded-long-payback conflict. [d222f5b460d3] [aac81fd83b5b] [179c5947001a] [9cb4c7dc31a1]

**A11. Contribution margin = true gross margin minus all marketing. Diagnose a missed target upward through the waterfall.** Waterfall: net revenue, cost of delivery, gross margin, marketing, contribution margin, opex, EBITDA, interest, net profit (worked example 100, 40, 60, 20, 40, 20, 20, 10, 10). Interest sits below EBITDA. Fulfilment staff sit in cost of delivery. A missed EBITDA points to opex, marketing or cost of delivery; a missed contribution margin to marketing or cost of delivery; a missed gross margin to cost of delivery or revenue. Condition: always. Watch for non-standard definitions: IM8's shareholder letter puts advertising below "contribution margin" (16). Sources: 01p1, 16. [f82391a766c6] [29f6666ae310] [2ba72747cc86] [a75628e1fb76]

**A12. Profit is not cash. Model ending cash separately from net income, and model the cash the next inventory buy needs before setting a growth target.** $2M of P&L profit with $3M of unsold inventory is about $1M cash negative (01p1). A brand can be net-income positive while its bank balance falls in the same month because of a purchase order (22). Cash conversion cycle = DIO + DSO minus DPO; each PO is only as big as the gross profit the last one produced, absent financing. Inventory financing to chase a revenue target compresses net profit toward zero ($2M to $7M revenue, profit to zero, seen "five times" per 01p1). Condition: every inventory-holding brand, every growth target. Sources: 01p1, 22, 05 (over-betting inventory was True Classic's closest brush with failure). [731ac683ccf3] [7e066cd286cd] [eecd54f14ae1] [8105508e9] [1dcdad671ee9]

**A13. The 6 cash-conversion levers are CAC, AOV, maintained markup, returning-customer rate, 30-day sell-through and opex. Find the one that binds, or move 2 to 3 together.** Fixed opex cuts hit net cash 1:1; marketing cuts do not, because they also cut revenue and COGS. Sell-through and markup release cash trapped in inventory without changing the P&L. AOV gains only count if they do not come from discounting. The source's example moves opex, markup and sell-through together and roughly doubles ending cash without touching CAC, AOV or return rate. Condition: bootstrapped or cash-constrained brands; all figures are one hypothetical spreadsheet (22). Source: 22 only. [7054802f6] [71b3d1891] [871d9318f] [a3a00f7b9] [7fe3a7782] [5007ba2e3]

**A14. A lever change takes 60 to 180 days to show in cash. Judge it against that window, not month one.** The model stays roughly flat at day 30 and compounds through day 180. Condition: any of the 6 levers; if nothing has moved by day 90 to 180, the model or the change is wrong (the source gives no next step). Source: 22 only. [32440a917]

**A15. Grade inventory A to D and route paid spend deliberately into C and D stock to convert it to cash, even though it looks bad on ROAS.** Isolate it in its own funnel at breakeven or a small loss; coordinate finance and media because a team KPI'd on ROAS will starve dead stock of spend. Do not reflexively cut marketing when cash is tight from unsold inventory; the fix may be a short-term MER increase aimed at the backlog. Condition: brands with a C/D backlog; single-SKU supplement brands are misleading templates because they can reposition one SKU across many claims. Sources: 01p1, 15 (inventory play at Black Friday), 22 (sell-through lever). [8669aea558c2] [2ba72747cc86] [36326f28b88c] [9b4e9226481] [7fe3a7782]

**A16. Rising CPMs are structural. Offset them through CTR or conversion rate, not by treating each year's rise as a crisis.** CAC = CPC divided by conversion rate; CPC = CTR x CPM. Platforms must grow revenue every year, so CPMs will very likely be higher next year (19). Observed: $10 to 15 CPMs pre-2020 vs $35 to 45 now (08); about 20 to 30% year on year in one agency's book (01p1, no card). A continuous small gain in CTR (creative, offer framing) or conversion rate (PDP, landing page, checkout) outpaces the annual CPM lift. Condition: diagnose which surface is weak before defaulting to "creative problem". Sources: 19, 08, 01p1. [2ee0c2788115] [916278acd788]

**A17. AOV and LTV are bid headroom: the brand that can afford to spend the most to acquire a customer wins the auction.** Raising first-order AOV (bundles, prepaid tiers, a subscription default) funds a higher allowable CPA, but only if CAC does not rise at the same rate; IM8's quarterly plan raised first-purchase AOV from $142 to $212 (quarterly buyers $321) at a 40% take rate (16). Test a longer default billing cycle in an isolated funnel, never by switching the whole store. Condition: stockpile offers on consumables can raise AOV and kill reorder (11). Sources: 10, 16, 11, 09. [81635c2e6b25] [f55f1e9b4827] [ba1c6ce5fe6a] [9bf05e0dda65] [1698727f88bc]

**A18. Once CAC-cutting plateaus on a well-run account, stop asking "how do I lower CAC" and ask "how do I make this CAC work" through retention and backend value.** Moving CAC from about $70 to $60 on an already-optimized account is very hard (11, citing a third party). Retention is the durable driver because CAC rises with scale; when repeat rate is zero, LTV equals AOV by definition (10). But retention is downstream of product, portfolio, repeatability and experience; email amplifies those, it does not create them (20). For the roughly 80% of brands with weak day-365 GP lift, CAC discipline, not more retention tactics, is the primary lever (19). Condition: which side of the ratio to work depends on category band (A8). Sources: 11, 10, 20, 19. [5baa55c8c61a] [3d5541e52ed0] [0005f05fcb3] [376c8c477e8f]

**A19. The death spiral: CAC creeps up, a fixed budget buys fewer customers, revenue falls, spend is raised to hold revenue, CAC rises again, and the loop rarely self-corrects until CAC has roughly doubled.** Early warnings: CAC breaking upward while new-customer volume and revenue fall; a blended P&L that looks fine while the first-time-customer P&L goes from plus $20k to minus $70k a month; reported ROAS improving while profit and revenue are flat ("on the treadmill"). Capital does not fix a bad ratio; it buys time. Condition: weak repeat purchasing makes the loop faster. Sources: 19, 14, 01p1. [6da370548f56] [a6b527c71dec] [f0fd9a23a268] [4f1e89e8a798]

**A20. Run the 2-P&L split (first-time vs returning orders, every line tagged) whenever acquisition might be quietly loss-making, and timestamp every structural change against the CAC and LTGP series.** A verified returning-customer subsidy (minus $50k first-time, plus $300k returning in the illustration) is one legitimate way to fund a sub-1 ratio; investor capital and debt are the other two, and none fixes the ratio. The presenter would not work with a $6 to 7M brand carrying investors or creditors (19, stated policy, not a law). Condition: use unit-level LTGP:CAC as the everyday proxy when the split is too heavy to run monthly. Source: 19 only. [a6b527c71dec] [f0fd9a23a268] [ceffceaa4132]

**A21. Opex creep is a separate cash-failure mode from the death spiral, mostly at $50k to $300k a month.** Revenue growth does not guarantee profit growth; founders scale into a bigger business at the same absolute profit because opex grows faster than gross margin. Marketing spend, not headcount, software or office, is the main DTC growth lever. Cut fixed cost sized for a past revenue peak (COVID-era hiring). Tension kept from 01p1: people are also the highest-leverage line once a brand can hire well. Condition: before adding any fixed cost, confirm the current LTGP:CAC can carry it. Sources: 01p1, 19, 22, 04 (Ridge: payroll about 7% of revenue, "10 or less to win"), 05 (60 people at $200M+). [9840c923e170] [7b24b5654a81] [71b3d1891] [dd91a3f96554] [d84592054461]

**A22. Read any headline growth number skeptically: ARR is one month times 12; "cash-flow positive" can be a financing effect; a stated LTV:CAC has a horizon and a share that is modelled, not observed.** Ask what month an ARR was annualized from and compare to a rolling 3 to 6 month average. Ask what is funding a cash-flow-positive claim. Ask whether any cohort has reached the stated LTV horizon. Condition: applies to founder self-reports in this folder as much as to competitors. Source: 16. [70936c5570f6] [9cb4c7dc31a1] [070e0c60e2f7]

**A23. Metrics that hold up in every context are incrementality, net profit, customer lifetime value and new-customer CAC. ROAS and email-attributed revenue are context, not north stars.** ROAS is skewed by existing customers, credits last click, and moves with attribution settings; it makes branded search, retargeting and email look like the best channels and makes awareness spend look worthless. Aim for the lowest ROAS you can acquire profitably at, not the highest. A healthy ROAS with flat topline usually means new and existing spend is not separated. Condition: always. Sources: 20, 14, 01p1, 05 (blended ROAS, new-customer ROAS, new-customer CAC, CPMs as the health set). [53cff4b8747] [c2f447b2849] [9497f75a4f1] [7c355072e26e] [0e1860afecb6]

**A24. Match the measurement tier to the size of the decision: platform metrics for small daily calls, finance-grade metrics (AMER, profit contribution, CAC) for budget and channel calls, causal lift for large strategy calls.** The reliability ladder from least to most: expert opinion and anecdote, platform-attributed ROAS, marketing mix models, quasi-experiments, geo holdouts (19). Adding tools, dashboards and conversion events to fix confusing metrics compounds it; subtract to a small agreed hierarchy. Recommended executive dashboard: profit contribution (or new-customer profit contribution) as headline, then AMER and new-customer revenue and orders, then CAC. Condition: incrementality testing is relevant mainly to the top 20% of brands by scale (01p1). Sources: 01p1, 14, 19, 04 (about 1% of marketing spend on measurement tooling, justified if it buys a 5% lift). [c2b721c34563] [4c923bbba4d6] [7500786dbfd9] [2d775e75662d] [217c8dc47244] [6f250e030e8c] [cd334cfab060]

**A25. Ecommerce is a plant, not software: slow years are not death.** Dude Wipes did $100k in 2012, about $1M by 2018, then headed toward $300M+; Stanley ran about $75M a year for about 30 years before spiking to $750M and settling near $300M; Baseball Lifestyle plateaued at $1 to 2M until about 2020 then reached about $150M (04, all unverified). Condition: this is a caution against panic and against copying a fast case as a formula, not a promise. Sources: 04, 13 (fast-launch skill is not brand-building skill: 3 wins then 10 to 12 failures). [a9c862b663ce] [12509c82d440] [3ae237242a99] [b7325aad598c]

### 3.B Bottleneck diagnosis

**B1. Growth is solving one bottleneck at a time. Find the current constraint fast, resource it, and expect the next one to appear.** Do not work every lever at once. Condition: always; the compounding-lever exception (A13) is a deliberate 2 to 3 lever move with a baseline kept, not "everything at once". Sources: 14, 22, 10 (entropy: add hours, people or systems where the next bottleneck appears). [4f1e89e8a798] [7054802f6] [25d1aef326ee]

**B2. Before any diagnosis, confirm the data has integrity: 7-day click reporting, existing customers excluded from cold campaigns, COGS tagged, new vs returning split, CAPI firing.** Symptoms of a metrics problem, not a strategy problem: ROAS improving quarter on quarter while profit and revenue are flat; the team "constantly iterating but doing nothing". The 9 measurement mistakes to check: 1-day view on, Google halo, brand-term waste, over-segmentation, fake-high tertiary channels, existing-customer overspend, unmeasured traffic or reach campaigns, DPA overspend, no testing structure. Condition: always first. Sources: 14, 01p1. Note the title of 14 says data integrity is the bottleneck in "80%" of audits; the transcript says "about 30%". Carry 30%. [c3b26441e2aa] [4f1e89e8a798] [2b34d63c3b0e]

**B3. When profitability degrades, reject the 3 default diagnoses (traffic, creative, seasonality) until the CAC and LTGP series have been read.** Pull CAC month over month with new-customer volume and revenue; if CAC is breaking upward while volume falls and spend was raised to hold revenue, the death spiral is running (A19). Condition: always before trying a new platform, a new agency or a new creative push. Source: 19 (seen in "about 100" of "over a thousand" audits, self-reported). [6da370548f56]

**B4. Then run the 3-layer read: ads, funnel, backend.** Ads layer: is the traffic cheap and qualified (CPM, CPC, CTR, hook rate)? Funnel layer: conversion rate times AOV. Backend: repeat rate, subscription, LTV. A weak metric in one layer is an indicator, not the constraint; instrument every step (ad, landing page view, add to cart, checkout, purchase) and drill to the actual break (a missing payment processor in 10's example). Condition: always. Sources: 10, 06. [cd2ec58854db] [4fc18ca8c1c4] [69f4ae6b]

**B5. Traffic vs conversion: the 2-signal creative read, then the price read.** If the platform will not give an ad spend, it is a creative or hook problem. If it spends but does not return money, it is a funnel, offer or landing-page problem. If clicks and impressions are cost-effective for the niche but carts are abandoned, it is a price or offer problem, not the ad (08). If CTR is fine and conversion is weak, the fix belongs to the PDP, landing page, pricing presentation or checkout (19). Condition: baseline CPM and CPC for the niche are needed to call "cost-effective". Sources: 06, 08, 19, 11 (test 4 to 5 angles against the same page before rebuilding the page; a 12% vs 1% CTR spread names the angle). [69f4ae6b] [a9b568d2aeff] [2ee0c2788115] [6b9ad04ab9c3]

**B6. The paid-traffic scalability screen: conversion rate % times AOV around 300 or above, at a roughly $3 CPC ceiling.** 3% x $100 = 300; 5% x $60, 1% x $300 also qualify. Well under 300 means fix conversion rate or AOV (whichever is cheaper to move) before adding spend; micro-CRO wins come after. Condition: recompute the threshold from the brand's own CPC and margin rather than copying 300; one agency owner's heuristic. Source: 11 only. [9e6eb4c8669a] [e5cd6f1465bb]

**B7. Diagnose the brand archetype before choosing the lever: product-led or media-led, creating demand or harvesting it.** Product-led signs: reorders with "average" ads (05), customers making unprompted content before outbound scaling (03), a product that sells organically without paid (01p1's "would it sell anyway"). Media-led signs: growth tracks creative volume and spend (09, 18). Harvest-only signs: 96% of ads in the bottom 2 awareness stages, celebrity names carrying prospecting, no cold-prospecting creative (17, Alo). A harvest-only account with no outside demand engine has no fallback and fits about 5% of brands. Condition: the lever differs: product-led brands should fix the offer or launch the next product; media-led brands should add creative volume; harvest-only brands should build problem-first creative before spending more. Sources: 05, 03, 17, 09, 18, 01p1. [59a96c63099e] [e8563c906f7a] [ec5bd4781c52] [00fc76514ab2] [812745ee3d05] [3c104e877904]

**B8. Product-market fit outranks marketing skill. Do not pivot a product or audience before real effort has gone in; then test several demographics with several angles before calling it a product problem.** Real effort means ads, UGC, an email backend and site work over a meaningful window (11's illustrative horizon is about 2 years). If friction persists across every demographic and angle, it is product-market fit, not messaging. Condition: also check price before product (Comfrt's premium launch did $10k against a $100k target, then $150k in 2 weeks at $69, 18). Sources: 11, 18, 05. [8bbceb08f413] [ff32df14c8b0] [11347fa2b0f9] [59a96c63099e]

**B9. Creative volume, not budget, is the ceiling on spend for a media-led brand. Check volume before blaming optimization.** Reference points, all self-reported: 1 new ad per $1,000 of monthly spend (01p2); each creative unit sustains about $2,500 of spend, so doubling spend needs double the creatives (16); 200 new creatives a month as a floor to scale, and 3 brands at $500k in month 3 each had about 200 creatives (18); 50 to 1,500 active ads in 13 months at $150 to 300k a day (09); 100 to 300 new ads a month at $250k+ a month (01p2). Volume only counts above a minimum quality bar; 2,000 ads a month at $4M spend was unprofitable (01p2). Condition: media-led brands; check the account hit rate (ads needed = 1 divided by hit rate). Sources: 01p2, 16, 18, 09. [3ed85b1ffd80] [49962212b27a] [bbac1e69e635] [603ebe25e9d5] [a9d4d1b724a5]

**B10. When an angle stops absorbing spend and frequency climbs, diagnose an angle-TAM ceiling, not a broken ad or bid, and open a new persona.** Each angle has a finite audience that actually has that problem; stacking angle TAMs is what lets one SKU absorb more spend. Condition: needs the brand's own frequency and spend-by-angle history; no numeric ceiling in the source. Sources: 21, 15 (at Black Friday, saturation is usually offer or creative fatigue, frequency barely moves: 1.75 baseline, 1.96 peak). [b2da5bc185dd] [ce65e92b40c4]

**B11. Root cause top-down, never bottom-up: business, then channel (weighted by spend share), then campaign type, then campaign, then submetric.** Check the dominant channel first (80 to 90% Meta for most of 01p2's clients). Decompose revenue = sessions x conversion rate x AOV and name which moved. Extend the window to avoid small-sample bias; use conversions by conversion time to avoid the false recent-days dip. A campaign holding 10% of budget that doubles moves the account about 5%. Discipline sentence before any change: "underperforming because [metric] dropped, driven by [submetric], caused by [trigger]". Targeted fix, not a rebuild; change one or a few things unless it is an emergency. Condition: any account-level diagnostic. Source: 01p2 (Google-specific framing, applies to any channel). [74d14b3daff2] [41fe6e957f15] [34e9220c4fce] [d0bb3b797336]

**B12. Before crediting an inside-account change for a recovery, size its realistic ceiling against the size of the swing, and check whether outside-account levers moved.** At $100 to 200M, a bid or budget tweak adds about 1% to a campaign; influencer deals, retail openings and PR move far more, and a "recovery" may be natural fluctuation (17). A new channel launched into a seasonal peak cannot be credited with the lift without a causal design (14). Condition: any post-hoc attribution of a revenue move. Sources: 17, 14. [ea0fb51b4d36] [33775b73749d]

**B13. Separate "the business looks fine today" from "the strategy is working". Judge on a weekly to monthly window, not daily or intraday.** A mid-day retention send can flip blended ROAS without saying anything about acquisition. During a deliberate spend-mix change, commit in advance to judging weekly on unit economics. Condition: a brand-new store may need daily monitoring; the source calls its own past intraday panic an unhealthy founder pattern. Source: 05. [0e1860afecb6]

**B14. When healthy-looking ROAS coincides with flat topline, check segmentation first: spend concentrated on existing customers or an unconverted organic following produces a short-term ROAS that dries up as that pool is exhausted.** Existing-customer ad frequency found in audits: 20 to 100 exposures a month; about 10 is the presenter's gut-check, not a benchmark. Paid to existing customers tested non-incremental even for a multi-nine-figure CPG brand. Match existing-customer spend to the repurchase cycle: near zero for furniture, a small narrow-segment allowance for FMCG. Condition: a frequency cut is a hypothesis to confirm with a lift test. Sources: 20, 01p1 (existing-customer budget = customers x target frequency x CPM; frequency under 7 to 8, stated with 2 different windows), 14. [9497f75a4f1] [722e2752eec7] [ca90d7c1ca85] [c1b04bc58a5a] [587d3d72e000] [df7a0134cc56] [b2092d04659e]

**B15. Intuition is accumulated test history, not a launch signal. Compare results against the brand's own data and runway, not other operators' public wins.** An operator with 10,000 to 20,000 hours of tests may read patterns others cannot and is still often wrong; a beginner's strong feeling is a hypothesis. At scale, the Rahal position ("you don't need attribution, it's intuition") is a mature, well-capitalized, second-time founder's preference and fits worst for an early or resource-constrained brand (07). Condition: see 7.6 for attribution vs intuition. Sources: 10, 07, 04 (most absolute-sounding rules are situational). [455d2f7749e9] [391c879b2d86] [5a9b4680ac1d] [12509c82d440]

### 3.C Stage-by-stage operating plans

The sources band stages 3 different ways: by monthly marketing spend (06: $0 to 10k, $10 to 100k, $100k to 1M, $1M+, "unlimited"), by annual revenue (14: $1 to 5M, $5 to 20M, $20M+; 04: $15M, $20M, $50M international triggers; 07: about $200M for the brand-vs-performance flip), and by monthly Meta spend (01: under $50k, $50 to 250k, $250k+). The 4 stages below use annual revenue as the primary key and list the source bands that fall inside each. The mapping between spend and revenue bands is approximate; use the brand's own marketing-to-revenue ratio (sources cite 8 to 20% in 06, up to 50% in high-margin periods in 04) to place a brand `[needs brand data: trailing 12-month revenue and current monthly spend]`.

**C1. $0 to $100k revenue (roughly $0 to $10k a month of marketing). Job: prove demand and one channel with the founder's own hands.** Rules: pick one specific customer, not an "overarching perspective" (06). Prefer a product with proven demand in a saturated category and carve a slice inside it; do not stack an unproven product on unproven creative and unproven media buying (10, 03, 13). Validate cheaply in stages: email the design to any list with a sales threshold, post about 50 organic short-form pieces and watch for an outlier above baseline (about 800 views baseline, 4,000+ outlier in 06's example), then a small fixed paid test (04, 06). A dedicated Meta test campaign at $10 to 50 a day, 1 to 3 new creatives every few days, read on the 2 signals; about $300 validates a low-priced product and about 2 weeks reads a $150 product at $10 a day; about $2,000 takes a store from nothing to validated (06, one presenter's figures). The founder writes the first ads and runs the account (10, 08: do it yourself under $3 to 10k a month; learn it before delegating up to $10 to 30k a month). Stand up welcome and abandoned-cart flows before scaling paid (11). Price for a brand with no track record: a premium launch price with no reviews fails; reprice fast and refund early buyers the difference (18). Do not aim for near-perfect margin on day one at the expense of demand, but confirm 40 to 50% true gross margin for CPG DTC before scaling, not "later" (07). Sources: 06, 10, 04, 08, 11, 18, 07, 03, 13. [92354a4e] [f763727b] [69f4ae6b] [c2268e45aa25] [11e43df4c9d2] [af4b9f233f1a] [36f24e817a8e] [11347fa2b0f9] [cb72f5171b60] [1d7f15eafafc] [0a484f196d18]

**C2. $100k to $1M revenue (roughly $10k to $100k a month). Job: get the unit economics right before the volume, and build the creative engine.** Rules: build the P&L waterfall and true gross margin per SKU (A4, A11); compute CAC against first-purchase GP and start a monthly CAC and LTGP table (A6, A8); tag COGS (A5). Meta reporting on 7-day click, existing customers excluded from cold campaigns, a daily dashboard of new-customer profit contribution, new-customer revenue and orders and blended CAC, brand search minimized (14's $1 to 5M list, which starts at the top of this stage). Ad account: one testing campaign, ad sets by concept (persona x angle x offer), 3 to 5 creatives per ad set, budget from target CPA x 3 to x 5, minimum test window about 1 week (01p1). Budget increases in steps of about 20% a day when an ad set hits KPI (01p1), or the doubling framework $50 to $100 to $200 a day which its own source says breaks at 6 figures (06; see 7.3). Creative: 3 core concepts, 60 to 80% of budget on testing, founder-led content, trial reels before ad dollars (01p2's $4 to 30k tier); a media pod of 1 analytical person plus 1 creative person (06). Hire a strong finance capability or fractional CFO early, not "a year before the sale" (05). Watch opex creep: this is the $50 to 300k a month band where it kills brands (19). Sources: 14, 01p1, 01p2, 06, 05, 19. [23010ab3b691] [5de48d3e386a] [1e8b0ae41022] [2dbc68e5e82e] [ec0c882e1e06] [30aac5b8] [a9156795ce70] [7b24b5654a81]

**C3. $1M to $10M revenue (roughly $100k to $1M a month). Job: scale the winning channel to its frontier, add measurement, and start the second channel and the team.** Rules: attribution starts to break above about $100k a month ("chaos theory", 06); add in-platform lift tests and incremental attribution as a second validation layer at $5 to 20M (14). Meta structure moves to 2 to 3 cold campaigns only when justified by distinct funnels, personas or regions; concept-level testing is the core skill; find the roughly 20% of concepts that can absorb hundreds of thousands a month (01p1's $50 to 250k tier). Production budget about 25% of media spend, 2 to 3 UGC creators, 5 to 6 concepts (01p2's $30 to 100k tier). Scale the primary channel before diversifying; name the remaining headroom before adding a channel and fund new channels as separate experiments (09, 04). Founder hiring order: first the founder's weakest function (an ops generalist about 3 years in for Salt and Stone), then a paid-media owner, then a CMO (12); COO and CFO before the founder becomes the bottleneck (18). Rebuild the operating foundation at the plateau around $100k a month rather than piling more on the founder (11). Pure performance marketing works from about $1M to about $20M (01p1). Sources: 06, 14, 01p1, 01p2, 09, 04, 12, 18, 11. [ed223dde] [99402b442662] [1fe205b60578] [3b07bb97fef4] [0805d0da06ef] [281ef6e02753] [a56c19b082b4] [e08bf0b419e3]

**C4. $10M plus (roughly $1M+ a month, and the $20 to 50M revenue band where the ROAS model stops scaling). Job: geo-lift measurement, brand and outside-account levers, retail and international by operational fit, and a leadership team that runs without the founder.** Rules: at $20M+ run geo-lift outside the platform at high frequency, build an omnichannel dashboard with every revenue source, and apply incrementality factors to platform ROAS before reallocating (14; 04 adopts holdouts at about $15 to 50M). Diminishing returns on brute-force performance appear past about $30 to 40k a day; budget a brand line even where ROI is unmeasurable (01p1). The brand-vs-performance split moves from about 90/10 performance pre-fit to about 60/40 brand at "teenage" scale to mostly brand at maturity, with about $200M as the unsourced point where a company stops needing to be "a marketing company" (07); Salt and Stone approved billboards only once liquidity allowed (12). Pick one awareness initiative and dominate it rather than 3 or 4 half-efforts (06). Meta at $250k+ a month: strategies not one structure, a second ad account with different bid logic (time-sensitive), bid complexity only now, 100 to 300 new ads a month, production budget asymptotes to about 10% of media (01p2). Inside-account tweaks add about 1%; influencer deals, retail and PR move more (17). International by operational fit, not demand: UK at about $15M, Canada at about $20M, EU warehouses at about $50M for a small-item brand; never "flip the switch" without localizing site and creative (04, 05); after US scale for a food brand (07). Retail: prove one chain, overproduce for the PO, buyer changes every 2 years (03); regional and specialty before mass (07); mall foot traffic over standalone stores (05). Team: the founder shifts from decision-maker to environment-builder once every direct report is better at their vertical (03, 12); keep decision loops under 5 to 8 people (09); expect director-level burnout and plan hiring around it (06). Sources: 14, 04, 01p1, 01p2, 07, 12, 06, 17, 05, 03, 09. [28067949e768] [0329cf172907] [e08bf0b419e3] [5a9b4680ac1d] [dedcbb054c21] [fd46c05f] [159829ec7374] [f7d41ac1c4b7] [ea0fb51b4d36] [406f95cc2038] [1bf2b0cb1bac] [f640724d4b4c] [aae76c2599ce] [05f735247a96] [5115e27797b5] [2a23256062f6] [b5802ce3e875] [21ed4b4d]

**C5. What changes at each stage boundary, in one line each.** Measurement: 7-day click and COGS tagging, then in-platform lift, then geo-lift (14). Creative: founder-led and 3 concepts, then 25% of media and 5 to 6 concepts, then 10% of media and 8 to 10 concepts with 100+ assets a month (01p2). Account structure: one testing campaign, then 2 to 3 justified campaigns, then strategies with a second account (01p1, 01p2). Budget pacing: doubling is tolerable early and breaks at 6 figures; 20% steps after (06, 01p1). Spend split: 90/10 performance, 60/40 brand, mostly brand (07). Team: founder does it, then a pod, then a P&L-owning structure and a leadership layer (06, 11, 12). Measurement tooling: none, then about 1% of spend (04). Sources as cited.

**C6. Sequence acquisition before retention in year one, then dedicate a retention phase and start with the biggest lever (the offer and subscription structure), not small loyalty assets.** IM8 spent its first 9 to 12 months on acquisition only and made the 3-month prepaid tier its first retention move (09). Retention programs cannot escape the category band (19). Condition: category dependent; do not defer retention indefinitely. Sources: 09, 19, 10 (retention in the backend from day one for consumables, replenish at 30, 60 or 90 days). Conflict kept: 09 sequences retention after year one; 10 builds it in from day one. See 7.12. [7d3b5a19ab1e] [376c8c477e8f] [3d5541e52ed0]

**C7. Set an internal "sustainable pace" before pushing to the next tier, and plan support and inventory for the spike before running the promotion that causes it.** Comfrt's target was to sustain $40 to 60M a month before pushing to $100M; its sellout forced the ad account into a new learning phase, withheld Black Friday sends, took 3 months to restock and needed 40 support reps in a month (18). Condition: any brand approaching a step change in volume. Sources: 18, 03 (overproduce around major retail launches), 13 (3PL and 4PL paperwork signed before peak). [ccdffe1f5d76] [ea32886fb87f] [1bc6acca39d7] [ac76fdafcc3e]

### 3.D Channel mix and sequencing

**D1. Build the mix bottom-up from each channel's "perfect level of spend" and move the next dollar to the channel furthest from its frontier, not from a fixed percentage template.** Push each channel to the point where its incremental AMER hits break-even, reallocating from lower-incremental to higher-incremental channels. True measurement needs per-channel incrementality; at lower revenue an experienced buyer's judgment or MMM approximates it. Condition: any brand on more than one channel. Sources: 01p1, 04. [3d5f23fdd11d] [c7c32c187bce] [ad362a18f501]

**D2. Meta is the dominant paid channel in every source that gives a mix; the share ranges from about 50% to 85%.** Ridge about 50% Meta (50 to 75% across years), 20% Google and YouTube (search 5, YouTube 15), 10% influencer, 20% tertiary (04). True Classic about 50% Meta, Google and YouTube stated as both 15 to 20% and 20 to 25% in the same interview, AppLovin notable, TikTok held at 5 figures a day (05). IM8 85% Meta, 15% Google, held from day one (09). One agency's clients 60 to 70% Meta (14), 80 to 90% Meta (01p2). Exception: Bloom claims 85% of spend on influencers and under 5% on Meta (03). Condition: concentration is a platform risk the sources themselves flag (09's host called his own 95% Meta "super dangerous"). All figures founder-reported. Sources: 04, 05, 09, 14, 01p2, 03. [ad362a18f501] [0cfb7300187c] [09fbaaa5df5f] [d912bfa27ecc] [2218553363b7]

**D3. Scale the primary channel to its named headroom before adding a channel, then fund new channels as separate experiments with their own creative and success criteria, not as reallocation.** Prove one channel small before expanding (05's origin; explicitly pre-iOS 14). Tertiary channels (Snapchat, TikTok, Reddit, X, Pinterest, AppLovin, linear TV) stay lightly funded (about $1 to 10k a day combined at Ridge) with flexing spend and no dedicated buyer, only once core channels are near their ceiling (04). A very high ROAS on a low-spend tertiary channel is a red flag for warm-only delivery; validate with a lift read before crediting it (14). Sources: 09, 04, 05, 14. [0805d0da06ef] [ad362a18f501] [4c2d5d5eae2d] [94dc95d044bc]

**D4. Google: route 80 to 90% of ecommerce Google spend to Shopping; treat PMax and branded search as demand harvesters that over-attribute; verify with holdouts before scaling.** PMax at 20 to 40% of Google spend for mid to upper ecommerce (01p2); Ridge caps branded search near 1% of marketing spend after its own holdouts (04, high-awareness brand). At Black Friday Google is a preparation platform, not a scaling platform (15). Condition: the branded-search cut generalizes only to brands with strong awareness; see 7.2. Sources: 01p2, 04, 14, 15. [0103a8c9bea0] [299de15a096a] [1f911edec6bb] [71083548afed] [16f43795044b]

**D5. Influencers and affiliates: start broad and cheap, learn who moves product, then narrow to a few deep long-term deals; pay micro-creators with a floor-or-commission structure and move winners to commission only.** Ridge went 50 to 500 to about 5,000 YouTubers then narrowed to about 300; small-channel CPMs about $5 to 10 (04). Comfrt: creators under 10k followers, $1,000 a month floor or 15 to 20% commission, 30 videos in 30 days, commission-only at scale, 250k+ ambassadors of whom more than half are customers (18). Bloom: creator flat fee at about half the brand's own Meta CPM (03 says $10 from a $20 Meta CPM; 13 says about $2; same method, inconsistent anchors), with a 15 to 25 person in-house team and no codes or links (03, 13). Prefer non-endemic sponsorships (04). Celebrity or top-tier partners on equity with a 3-year minimum, seeded through the inner circle first (09, 16, 04's MKBHD deal). Condition: measurement of a zero-code program only works omnichannel with DTC under 5% of revenue (03); see 7.1. Sources: 04, 18, 03, 13, 09, 16. [e6cb05526e60] [47d290ff4340] [7e12fa08f9b3] [abdbf1926c47] [caf5937eab0a] [f0c35189d69e] [a5e7b7863c43] [561de6374d6] [793682953546] [ac7a5c24d798]

**D6. Organic and creators are the cheapest proving ground and the best paid creative, but new-customer acquisition itself stays rented.** 70% of Ridge's best paid ads are organic winners (04); stopping organic posting weakened paid performance at Breeze (08, correlation); Purely White grew to 300M+ views a month on organic with paid "never working", while Comfrt's paid worked at 4 to 5x early (18, unresolved). Even a 50k-follower account rarely reaches 50k views, so reaching an "owned" audience still rents distribution (19). Condition: see 7.4 for organic-first vs paid-from-day-one. Sources: 04, 08, 18, 19, 06. [954f15424bc2] [b19555ac55d8] [a84d20a1386a] [9f8e357bd0b2] [f763727b]

**D7. Retail and Amazon are later-stage demand sources sequenced after digital proof, and a store footprint lifts online revenue in its region.** Prove sell-through with one national chain (Target) before more doors (03); build digital sell-through and brand recognition before pitching big box (05); regional and specialty before mass, or lose the account for good (07); a client's online revenue rose about 20% after opening stores in Canada (17, one anecdote). Amazon: send external traffic to win rank, then use rank as retail evidence (13); earn the bestseller badge organically before Amazon ads; hold one price across Amazon and prestige retail (12); sell direct to Amazon to cut counterfeit and diversion risk (03). IM8 stays 98% own site and declines retail while DTC headroom exists, using rejections as leverage (09). Condition: retail needs inventory buffers and fill-rate discipline; a missed PO is worse than a stockout on your own site (03). Sources: 03, 05, 07, 17, 13, 12, 09. [aae76c2599ce] [664e2cb90e53] [05f735247a96] [eaa8aaeb8087] [aefe14739fde] [2e790ab86c57] [1f023eb429f7] [e9c97672d49d] [dfb0138526ec]

**D8. TikTok Shop and creator-commission channels are a current arbitrage that shifts monthly; fit is impulse price (under about $29 to 39), female-first purchase, and spillover distribution, since TikTok Shop itself captures about 5% of the value it creates.** Run TikTok Shop affiliate as a separate track from the organic creator program; a TikTok Shop win correlated with about a 30% lift on Amazon, Target and Walmart in Bloom's account (03, correlation). Condition: `[web check: current TikTok Shop affiliate economics and policies]`. Sources: 04, 11, 03. [cb6b3e45c875] [a984fdf4f581] [faded9a8b79e] [1d781f4b15e7]

**D9. Diversify channels to remove key-channel and key-person risk, deliberately and before a crisis.** Bloom was about a week from a 50% layoff after losing its largest channel (03). Building in public and naming a brand after one person concentrate the same risk (03, 08). Condition: continuous audit of revenue share by channel, retailer and creator. Sources: 03, 08, 04. [492ad9d02ac5] [414454f50f31] [fcb510de5279]

**D10. Confirm channel cannibalization by pausing one of two overlapping channels and watching total revenue, not the paused channel's reported conversions.** A brand paused one of Amazon or TikTok Shop and saw no change in total revenue (04, secondhand). A TikTok launch at 25% of Meta's budget lifted a Meta mid-funnel campaign from 4x to 12x; crediting Meta and cutting TikTok would be wrong (01p1, 14). Condition: any pair of channels that may share demand. Sources: 04, 01p1, 14. [89eb781b3bd2] [4ba4c1567d4d] [7c355072e26e]

**D11. Coordinate paid spend with the owned calendar: pull paid back ahead of a known email drop, launch or discount push, because those customers convert without paid pressure.** Track daily burn, discount as a percent of sales and $1,000+ orders together; rising revenue with rising discount rate can still lose to burn. Condition: brands with a working email list. Source: 08 only. [222d8f7291df] [72a946cbac3c]

**D12. Run each new major product category as its own business unit for acquisition (own ad account, own buyer, own targets) while email and storewide offers cross-sell across units.** Ridge's structure across wallets, rings, phone cases and luggage (04). Condition: multi-category brands; a rollup that centralizes one CMO across brands with different customers is named as a failure cause (08). Sources: 04, 08. [7a83a06a1f8d] [e3318059ec3e]

### 3.E Persuasion principles as constraints on offers and copy

These rules come from source 02 (Cialdini), the only academic source in the folder. It has no ecommerce content; every ecommerce mapping below is the mini playbook author's adaptation, marked as such. The mechanisms are real; the ecomOS rule is that the agent may use each one only in its honest form. The manufactured form of each is banned regardless of what any founder source in this folder did.

**E1. All 6 principles run on one mechanism: a rushed, uncertain or distracted buyer reaches for a single cue instead of analysing the situation.** The cue works when it is true and becomes a vulnerability only when faked. Adding "because" to a small request raised compliance from 60% to 93 to 94% even with an empty reason. Constraint: give the reason for every small request on a page (why the email, why the size question); never fake the cue. Apply persuasion levers only after baseline mechanics work and sequence them so they do not cancel each other. Source: 02. [6437ff16f5bb] [a3af94f07c08] [2afb006d52b4] [d771afe27917] [95287da743ad]

**E2. Reciprocation: an unrequested gift creates an obligation that overrides liking; a real concession invites a concession.** Regan's unsolicited Coke roughly doubled ticket sales; an unsolicited gift lifted a mail response from 18% to 35%; rejection-then-retreat moved compliance from 17% to 50% and raised follow-through (85% vs 50% show-up). Conditions: the gift must come before the ask; the opening request in a retreat must be plausible, or the retreat is not reciprocated. Honest forms: a genuine free sample or guide before any ask (07's sampling line at about 10% of marketing; 03 and 13's on-camera gift with purchase); a real premium tier above the tier you want most buyers to land on (16's middle-tier ladder). Banned: a "free" item engineered as a lowball (02's own checkout-audit repurposing of the lowball), a fictional premium anchor, a "we'll take less profit for you" concession that was never a cost. Defence the buyer uses, so the agent must expect it: redefine a device as a tactic, not a favor, and owe nothing. Source: 02; honest applications in 07, 03, 13, 16. [eba045f9fe03] [09edbcf0efa2] [e020fb4b6275] [3866a7fb25f7] [e0ab1f148d59] [a2d0ba8b9063] [587671f8263f] [30f3591e0db6]

**E3. Commitment and consistency: an active, public, effortful, freely chosen commitment changes self-image; a large external inducement does not.** Foot-in-the-door roughly doubled later compliance; a barely sufficient reason produced durable behavior where a strong threat produced compliance only while present (77% vs 33% chose the forbidden toy after the strong threat was lifted); Pallak's households kept saving energy after the promised publicity was withdrawn (12.2% to 15.5%). Honest forms: a small real first purchase or trial that earns follow-on interest; voluntary written goals in onboarding; a subscription whose discount is disclosed and whose value holds after the introductory incentive ends (02's retention-test repurposing). Constraint on offers: the welcome discount that converts (05's 10% to 20% step, no gain at 30%) is a first-purchase incentive, not a recurring reflex; a large incentive trains the customer to attribute the purchase to the deal. Banned: a foot-in-the-door that hides the true cost; unescapable subscription terms (08 calls these no longer legally viable). Sources: 02; 05, 08 for the offer constraint. [1dc5c87f6b56] [47ad577a71af] [39d3229ff1f7] [b3eea5415ee8] [3f1108aa246a] [7a84d0a05040] [ee6015291fc4] [9edfe64030cb]

**E4. Social proof works under uncertainty and similarity, and fails or misleads when falsified or when it is a cascade with no independent information.** A lone bystander helped 85% of the time vs 31% with 5 present; a wallet with a note from a similar finder was returned 70% vs 33%. Constraint: concentrate proof on the ambiguous steps of the funnel and on cold traffic; use similar-customer proof (same body type, same use case) rather than "everyone loves this"; every count must trace to real order or platform data. A "bestseller" or "trending" signal can be shoppers copying shoppers, so read repeat rate and direct search alongside rank. Banned: seller-typed counts, static "X people viewing", fabricated reviews, astroturfed community content. Real forms in this folder: IM8's ambassador wall and science stack as hard-to-copy trust (16); Bloom's "restocked 3 times" only when true (03, 13). Sources: 02; 16, 03, 13, 05 (post-purchase survey as truth), 06. [af86be5a3012] [c0a38656da11] [00b1280a3b63] [2610a89b3503] [b00c278eaa05] [d147d0be41fb] [83427f562f2c] [a72c28e35ff9] [561a44bba1b4]

**E5. Liking: attractiveness, similarity, compliments, familiarity and cooperation all raise compliance and all operate below awareness (73% of voters denied any appearance bias while attractive candidates got more than 2.5x the votes).** Constraint: real customers and creators who resemble the buyer are a legitimate lever (18's micro-creators who are also customers; 06's on-camera faces carried from organic into paid); the "we're on the same side against the carrier" frame is honest only when the constraint is real. Banned: fabricated personas, actors presented as customers, staged adversaries. Rivalry breeds hostility, not liking, so competitive framing against the customer backfires. Sources: 02; 18, 06. [b633a77c719e] [6e0f593353ac] [0ac6098b64d7] [313c00948117] [caf5937eab0a]

**E6. Authority: symbols of authority work almost as well as expertise, which is exactly why the two-question test applies to every credential on a page: is this person an expert on this specific claim, and how truthful can we expect them to be here?** A guard uniform moved compliance from 42% to 92%; 95% of nurses began an unauthorized dose on an unverified phone "doctor". Trust rises when the authority concedes a minor point against its own interest before the main claim. Constraint: named, checkable, relevant credentials only (07's Huberman and Layne Norton for nutrition, 09's advisory board, 06's dermatologist or nurse for a wellness product); a real store footprint as an authority signal (17). Banned: an actor, an unrelated celebrity, an empty title, or a funnel that asks the customer to act before the claim can be verified (02's bank-examiner template as a diagnostic). Sources: 02; 07, 09, 06, 17. [6ef2415cede8] [eff569999325] [efb0633227f5] [72d23ea7ddf2] [57c69c609f38] [cf48c9f65acd] [eaa8aaeb8087]

**E7. Scarcity raises desire to own, not perceived quality, and is strongest when newly scarce and when caused by other people's demand.** Cookies from a jar of 2 were rated more desirable, not better tasting; scarce and "exclusive" supply news raised beef orders about 6x. Constraint: state true remaining stock, a real fixed deadline, or a genuine one-time batch; tie every scarcity claim to a checkable constraint (03's and 13's restock language, 17's rule that only brands that actually sell out can use scarcity honestly, 15's final 24 to 48 hour deadline creative for a sale with a real end). Never use scarcity to imply better performance. Banned: countdowns that reset, "3 left" not backed by inventory, staged rival buyers (02's simultaneous-appointment scheme), constant scarcity (13 notes it loses effect and is a consumer-law risk in some markets). Sources: 02; 03, 13, 17, 15. [743b6f53913c] [11bcf453bac4] [3128fdab039e] [28f3d6876a8c] [1ba0b515409e] [b7d4878acc8a] [3a1292e93ad7] [d6a9aa0c6869]

**E8. Contrast: show the expensive item first; a cheap item shown first makes everything after it look expensive.** Brunswick's average sale rose from $550 to over $1,000 when buyers saw the $3,000 table first. Constraint: a real premium anchor tier or a premium item before accessories is honest sequencing (16's three-tier ladder; 01p1's anchor-high-then-downsell in post-purchase upsells; 17's rule to keep the cheapest SKU out of paid); a fake "was" price is not. Sources: 02; 16, 01p1, 17. [dce513894389] [c7ac01349bb9] [739e469e9802] [835b52ea1691] [375d99aa7abb]

**E9. The team is subject to the same mechanisms: pre-commit a ceiling before any competitive bid (ad auctions, inventory, sponsorship), and run the time-travel question on launches and channel bets before funding them further.** ABC's $3.3M Poseidon bid was an expected $1M loss made under auction fever; the losing CBS bidder called losing a relief. Ask "knowing what we now know, would we make this call again?" and trust the first reaction before rationalization. Public, costly commitments make survivors manufacture confirming evidence (the doomsday-cult pattern), so vocal post-launch enthusiasm from people who already spent money or reputation is not proof the product delivered. Sources: 02; 04 (never rescue a flop with better marketing), 10 (assume nothing). [80d1a965dcd8] [239a4c7c7019] [95e9000831b0] [2f71ca0f90fc] [913bb06d2be3] [db8e8f54f571]

**E10. Sophisticated buyers neutralize each tactic, and the defence describes when the tactic stops working.** The Hare Krishna flower gift lost effectiveness once recognized; stacked, conflicting cues (an aggressive countdown beside heavy unrelated proof) reduce credibility instead of adding force. Constraint on CRO and copy: do not treat "always add urgency" or "more proof is always better" as universal; see 7.9. Source: 02. [ecc4097514cf] [d4cb90c749c7]

### 3.F Seasonal peaks (Black Friday and Q4)

Source 15 is the only dedicated peak source and comes from one agency's client portfolio ($50 to 100M of spend), a third-party incrementality report (House), an attribution vendor's report (Triple Whale) and a creative-analytics vendor (Motion), all cited secondhand. Every number is a 2025 to 2026 snapshot `[web check before reuse in a later year]`. Sources 13, 18, 01p2, 14 and 19 add peak-relevant rules.

**F1. Pre-sale spend is a lagging indicator, not a weak signal. Do not cut spend in October and early November because short-window ROAS looks weak.** A sale collapses the whole top-of-funnel audience into one revenue spike; underspending before it shrinks the funnel when it needs to be biggest. The 1-day vs 30-day click gap was about 40% in a normal period and about 80% in November in the agency's accounts; one large brand's ROAS on November 12 to 13 backdated from about 1x to about 4x. Condition: needs at least one prior peak of the brand's own data for both windows `[needs brand data]`. Source: 15. [d243f038601b] [a0478e430dad] [c310f482ec53]

**F2. Front-load about 31 to 43% of the September-to-December budget into September and October, and treat November as a harvesting month for reach, not a buying month.** CPMs rose about 25 to 30% above October from about November 12 and further through the weekend; Triple Whale's weekend report said +50% Meta and +10% Google, measured differently from the agency's own 7.8% figure; do not average these. Clients spending over $2M a month underspent relative to returns; the $500k to 2M bracket spent about 1.76 to 1.8x October in November. Post-treatment lift from pre-season tests was 105% for tests ending 3 or more weeks before the sale, and 41% of incremental value showed up after the test window (House; fashion 93% vs CPG 30%). Condition: portfolio ranges to calibrate from, not targets. Source: 15. [62e69271e95c] [a464d35942c4] [9bbe6d4b46a1] [1d313c3eb80b]

**F3. Decide the sale's objective (contribution profit vs clearing C-grade stock) before setting any CAC tolerance, because they pull in opposite directions.** A profit play spends to the marginal frontier and stops when incremental returns turn negative; an inventory play explicitly authorizes negative marginal contribution late in the weekend to clear stock; a tiered GWP serves both partially and underperforms either pure play. Condition: communicate the objective to the media team before the weekend. Sources: 15, 01p1 (C/D stock routing). [9b4e9226481] [8669aea558c2]

**F4. Apply 3 corrections before any peak forecast: attribution (a multiplier from prior-year short vs long window), cohort value (November cohorts repeated at 38.5% at 6 months vs 63% for February in a 10-brand sample, but 2 of 10 showed no gap), and margin (discount-adjusted break-even ROAS).** Skipping any one leaves the plan on a distorted base; the default November CAC allowance is "wrong twice" without the cohort and margin fixes. Condition: `[needs brand data: 6-month repeat by acquisition month for 2 prior years; gross margin by SKU; planned discount depth]`. Sources: 15, 19 (a discount-heavy cohort's first-purchase GP fell from about $70 to $40). [ebb016b64886] [7473b6195d7f] [d661eb7e3ac0] [61f3aa873861] [676a17d4a712]

**F5. Scale on marginal contribution margin, not blended averages, with a written rule set: 3-day rolling marginal CM3 improving means increase; flat means hold; 2 consecutive poor reads mean decrease.** Average CAC can sit under tolerance ($392 vs a $400 limit in the example) while marginal CAC is about $1,000. Never judge the day against a fixed 8am target: spend peaks 5 to 7am and revenue 7 to 11am, so build per-hour delayed-attribution multipliers and read conversion rate by hour as the less-lagged signal. Use revenue-to-spend elasticity only to justify a cut, never to scale, because it is observational. Condition: intra-hour pacing only at very high spend with rotating offers. Source: 15. [a74069ce7855] [294df46a0b6e] [3b63d06d5486] [6f476966cae3] [675de05124cc] [5afc0c5d082f]

**F6. Enter with base and stretch budgets and pre-agreed numeric gates so the team can move between them and pull back without a live approval call. The budget is a ceiling to deploy against incremental returns, never a target to spend.** Condition: gates are a CM3 floor, a marginal CAC ceiling or a ROAS band, agreed before the window. Source: 15. [71ba87612a01]

**F7. Forecast creative volume from peak daily spend divided by a realistic per-ad spend ceiling, and plan for the tail, because the 80/20 rule does not hold at Black Friday.** A $150k peak day at $10 to 12k per ad needs 12 to 18 ads that can each hold that spend, not 12 to 18 ads that exist. In the portfolio the top 1 ad held about 7% of spend, top 10 about 33%, and the bottom 80% of ads about 54%; accounts under $250k of November spend were more concentrated (top 20% of ads at 53%) than larger ones (44%, then 33%). Per-ad ceilings in the agency's AUD accounts: most evergreen $4 to 8.5k a day, realistic ceiling $8 to 13k a day. Condition: if required volume exceeds production capacity, lower the target or raise production and page capacity before locking the plan. See 7.10. Source: 15. [075f80613bc3] [b5d2b85f4f87] [291583358578]

**F8. Never turn off evergreen campaigns for the sale; duplicate the best performers (including fatigued ones) and badge them with the offer. Judge creative during the window on CTR and CPC at the ad-set level, not ROAS at the ad level, because the discount corrupts the feedback loop exactly when the most data is generated.** Turning off evergreen is called "the single biggest mistake" of the period; evergreen carried 50 to 60% of Black Friday spend. Plan the format mix by spend share (offer statics about 19%, offer-overlaid evergreen about 18%, creator or founder content the largest share) rather than by whichever format shows the highest raw ROAS. Add sale messaging to catalog copy (74% of scraped brands had none). Condition: the CTR/CPC rule is a Black Friday exception; the same source says those metrics have no useful correlation with ROAS the rest of the year. Sources: 15, 01p2 (never turn off a winning ad to move it). [7c0dc6951b2c] [88407c078150] [f9f39dcd376e] [0fd306b87cfb] [69a7c7195336]

**F9. Pre-build the full offer ladder (GWP, referral, free shipping, bundle, deepest site-wide discount) with landing pages and creative loaded before the sale, with trade-number triggers for each fallback, and phase creative in 4 stages: teaser or early access, launch, mid-sale refresh, final 24 to 48 hour deadline.** Lock the offer before producing launch and deadline assets. Rolling offers prevent offer fatigue; pivoting an offer across hundreds of live ads in real time is very hard. Condition: any trade-reactive brand. Sources: 15, 08 (15 unique offers a quarter once a team exists). [e2262e74c26f] [d6b1b339b607] [d6a9aa0c6869] [d6b5067b58b0]

**F10. Google is a preparation platform for the peak: update titles, assets, promotion feeds and Merchant Center pricing well in advance, and do not raise Google budget on the weekend because its ROAS looks strong; that strength is mostly captured demand from Meta and brand search.** Cost caps, avoided year-round by this agency, become a diagnostic during the peak to map the marginal frontier, not the main scaling lever. Condition: `[verify UI]` for Merchant Center and PMax promotion setup. Sources: 15, 01p2. [16f43795044b] [4afe3a4577de] [926e49f0a825]

**F11. Protect the operation before the peak: 3PL and 4PL paperwork signed in every region, inventory buffer and support capacity sized to the spike, page-limit headroom for the creative ramp.** One missing 4PL document caused a full inventory seizure on Black Friday two years running and killed a $130M acquisition offer (13); Black Friday and the 2 months around it were about 80% of that brand's annual profit. A sellout during the peak forced Comfrt to withhold email and SMS and reset its ad account (18). Condition: run the checklist on a fixed pre-peak date, not during the event. Sources: 13, 18, 15, 03 (overproduce around major retail launches). [ac76fdafcc3e] [ccdffe1f5d76] [ea32886fb87f] [9f9579f3d2c0] [1bc6acca39d7]

**F12. Q5 (about December 16 to 31) is the cheapest media of the cycle and suits a deliberately prepared offer, not a leftover budget dump. Do not carry last year's CPMs into this year's forecast.** The agency expected Black Friday 2026 to run at higher CPMs into a weaker consumer than 2025 based on Australian rates and inflation and slowing Meta inventory growth; re-check the macro for the target market `[web check]`. Source: 15. [5eab80b6afef] [3561b527a1f8] [6a2ae399039b]

**F13. Do not credit a channel launched into a seasonal peak with the peak's lift without a causal design (lift test, geo-lift or CausalImpact).** "Revenue went up after we launched" in October to November is not evidence. Sources: 14, 15. [33775b73749d] [c049a4fab120]

### 3.G Founder and capital decisions

**G1. Default to capital efficiency: fund growth from profit and supplier terms first, debt second, equity last, and raise only for a specific opportunity that cash flow cannot buy fast enough.** Bootstrapping forces faster-killed product bets because no outside money props up a loser (04, Ridge's only outside money a $200k Kickstarter). True Classic never raised primary capital; it progressed supplier terms from none to 15, 30, 45 and 60 to 90+ days, then a $1M, $5M and $25M supplier revolver, and treats board seats and observer scrutiny as a real cost (05). Bloom bootstrapped to a claimed $180M and declined a nine-figure acquisition, but its founder credits the choice partly to not understanding enterprise value early (03). Rahal raised only to finance an ingredient-supplier acquisition, and asks any investor whose money it is, what return they need and over what time (07). Comfrt started with about $50k from the first brand's cash flow (18). Condition: an inventory-heavy or truly capital-constrained model may need outside capital regardless (04's own caveat); see 7.8. Sources: 04, 05, 03, 07, 18, 09 (5 numbers for any investor: unit economics, TAM with named competitors, differentiation, runway, path to profit). [31c8109a299f] [765be2933ced] [5529a92593b3] [a9156795ce70] [74016741fdbc] [4269b434597c] [4410f4acddbe] [931bf2d42178] [ff64a574212a]

**G2. Match the working-capital tool to the timing gap: a revolver for smoothing, a debt recap to take enterprise value off the table, PO or receivables factoring when a retailer PO needs upfront cash (cheaper with stronger retailers), supplier safety stock and terms before any of them.** Debt taken without genuine confidence the business works is a short-term patch (05). A brand funding first-purchase losses with debt needs a "dialed-in" operator; the presenter would not work with a $6 to 7M brand carrying investors or creditors (19, stated policy). Model the debt load a lender or buyer would place on the business and whether it survives a downturn before accepting it: 2 to 3x EBITDA is conservative, 6 to 7x was seen pre-2022 (04). Condition: always before signing. Sources: 04, 05, 19. [e9d130295214] [edf06536c8b7] [ceffceaa4132] [88dae8d1f315]

**G3. Bring in senior finance capability (a CFO or president who can build rolling forecasts and has been through a transaction) early, not a year before a sale.** True Classic had no financial models until about a year before its interview and calls that a gap (05); Salt and Stone's sale-ready checklist starts with finance leadership who have been through an acquisition and a banker (12); Rahal's "restaurant bathroom" test: books that close fast and pass audit (07). Condition: any brand above about $1M. Sources: 05, 12, 07. [a9156795ce70] [afb8409d019a] [bd022d81f786]

**G4. Sell inventory-and-people risk down before it kills you: single-source suppliers get MFN clauses, backup capacity and, where the input is the moat, vertical integration; contract manufacturers are vetted on capacity and certifications and split across facilities at volume.** RXBAR nearly died when a larger customer bought out its sole manufacturer's capacity (07); Salt and Stone's costliest mistake was an unvetted manufacturer, and it now runs about 10 facilities (12). Treat vendor relations as mutualism, not leverage extraction. Condition: any physical-goods brand. Sources: 07, 12. [a7c30506fe46] [c4432820ebd9] [248161a47836] [f6567143a45c] [2590378c1767]

**G5. A strategic partnership or minority equity sale is right only when it closes a capability gap you cannot build (the "1+1=3" test) and visibly raises enterprise value; otherwise you might as well sell the whole business.** Bloom sold about 30% to Nutrabolt for beverage logistics and distribution, kept about 70%, and reports enterprise value tripling and a Target shelf in about 6 months (03, 13; the deal year is given as both 2022 and 2023). Expect the partner to influence product and channel decisions even as a minority holder; set exclusivity and exit terms first. Sources: 03, 13. [91a2ee5c0b52] [f90e66edbcd2] [64892ed4faa6] [c11ca588fe21]

**G6. Understand PE mechanics before entering a process: a leveraged buyout can make the buyer money even if the brand later fails, because the return comes from debt recapitalizations on the company's own balance sheet.** $100M business bought with $50M equity plus $50M bank debt secured by the company (04). PE buyers want sustainable EBITDA of about 15 to 20% with multi-year 20% growth and a visible moat; a 30 to 40% margin invites add-backs for what was underspent; leave named "meat on the bone" (an unentered channel or unlaunched line) rather than a fully optimized business (04). Strategics underwrite on EPS accretion and synergy; PE on IRR (about 2x in 2 years in Rahal's illustration) (07). Sources: 04, 07. [edf06536c8b7] [6713ec746162] [399d57d8b870]

**G7. A secondary sale lets a founder take chips off the table while keeping control; it dilutes but adds no cash to the company; budget about 45 days of diligence and expect the stated timeline to slip to the outer bound.** Salt and Stone ran a process with about 15 PE bidders, chose a lower bid for fit (operator-founded firm that "lets me do my thing"), and did a second transaction within about 18 to 24 months; PE secondaries typically buy 50 to 70% (12, founder's generalization). Interview the buyer back in unstructured time; the highest bid is not the criterion. Condition: most available to a founder who started near 100% ownership. Source: 12. [93d8ebb61724] [c3cde0fb2643] [8b03a5eaa976] [9421982e1ec7]

**G8. Run a competitive sell-side process with a banker and a real timeline, 8 to 10 buyers mixing strategics and PE, full transparency (buyers find everything), and the CEO personally closing.** Expect a real brand sale to take about 10 months; sub-$5M deals through searcher funds move faster at about 1 to 3x EBITDA (04). Expect a vulnerable window between signing and close (RXBAR signed October 6, closed October 28, 2017) (07). Read terms, not headline price: "participation" and a "second bite of the apple" rarely pay; get your own defensible EBITDA before add-backs erode it (04). Sources: 07, 04. [fca479f57f8f] [796cf06f23d1] [20817201b1bb] [58e0fc375c4c]

**G9. Exit multiples are founder heuristics that shift with the market; verify current conditions and never assume the outlier band.** Fogerty's bands: dropshipping about 1 to 2x EBITDA; non-subscription ecommerce about 3 to 6x EBITDA; replenishable and subscription categories higher; a brand with retail distribution, a flywheel and a following up to about 3 to 5x revenue or about 30x EBITDA, explicitly an outlier; agencies about 3 to 5x profit, his own 11x in 2021 (13). Value drivers: recurring or contracted revenue, hard-to-win customers, scale, growth trajectory, a buyer whose network lifts the earnout. Normal ecommerce exit timelines 5 to 7 years, up to about 9. Build cash flow and skill before designing for an exit. Condition: `[web check: current consumer-brand multiples]`. Sources: 13, 04. [dc145902632] [0355e66068] [9c1c2bba079a] [796cf06f23d1]

**G10. Take an offer that is genuinely life-changing money rather than holding out, and prefer to sell in the first year growth plateaus rather than after it turns down; treat this as a personal risk decision, not a formula.** Ridge was reportedly offered $300M at about $100M revenue and the deal fell through in a cooling market; the founder wishes he had taken it (04). A founder's personal net worth of $1 to 5M is the de-risking threshold the same founder names before big decisions. Condition: opinion, explicitly not financial advice; taxes, earnouts and rollover specifics are ignored. Source: 04. [78f51f3e7f41] [d30839f7b7a0]

**G11. Decide the founder's role in buyer meetings from the exit goal before the first meeting: staying means showing the passion; a clean exit means limiting founder presence so the buyer does not price "the magic" into a retained stake.** This runs against standard M&A guidance that founder engagement builds buyer confidence; the source frames it as tactical and specific `[needs legal or deal advisory review]`. Separate the founder, CEO and shareholder roles through a sale and act in each appropriately on close day; a 5-year non-compete (2 to 6 called standard) followed (07). Sources: 12, 07. [629185c92369] [b0c7c3317789] [acf4c08a857a]

**G12. Key-person risk: remove it deliberately on both the founder side (a leadership team that runs the business, a CEO archetype defined before hiring a replacement, not the founder's mirror opposite, 6-month trial) and the partner side (no brand named after one person, no single dominant creator, celebrity deals on equity with 3-year minimums and a plan for a partner's public profile changing).** Fogerty "lucked out" on a CEO hire he nearly got wrong (13); Bloom avoids naming the brand after a founder or one influencer (03); IM8's source gives no downside case for a celebrity partner's profile changing (09). Building in public reverses its CAC benefit when the founder stops (08). Condition: any brand where one person's absence would stop sales. Sources: 13, 03, 09, 08, 12. [116713e4f02a] [492ad9d02ac5] [561de6374d6] [fcb510de5279] [0d5cadae700b]

**G13. Cut a structurally ending revenue line early and decisively to protect cash, but do not confuse a temporarily soft category with a dead one.** Prenetics wound down COVID testing and laid off about 2,000; companies that kept scaling that revenue are described as bankrupt or delisted (09). The same decisiveness on a viable but slow category destroys it (A25). Condition: hindsight validated the specific call. Source: 09. [6671e33e746c]

**G14. Treasury allocation into a volatile asset is a separate, capped decision with a stop condition tied to the core business, kept smaller than operating cash.** Prenetics held about $70M cash against about $40M in Bitcoin and stopped adding when it distracted from IM8 (09). Condition: public or investor-facing entities confirm accounting and disclosure first. Source: 09 only. [5bfb3732fb33] [fd68d33918f8]

**G15. Grant equity, options or profits-interest units to creators, advisors or hires only after specifying what they contribute and what upside they get, with legal and tax advice on the instrument, because the wrong instrument triggers a taxable event at grant.** Source: 04. [1d505dda7fcc]

**G16. Peer and mentor network before the crisis, and outside review of the business, because growth-stage problems become rarer and harder to find advice for.** Comfrt called on named founders during its sellout crisis (18); 10 argues no operator sees every problem alone. Sources: 18, 10, 13. [4bb5f94ab4b7] [25d1aef326ee] [f42f58122d64]

### 3.H The brand teardown method

Rule zero, from ecomOS: a competitor's ads, pages and public P&L are signals for structure, mechanism, format mix and funnel logic. They are never proven winners and never templates. No copying of text, products, photography, faces or landing copy, whatever the performance. Ad-library composition is not spend distribution, so every percentage below is a composition read, not a performance read (17, 16).

**H1. Start with the P&L or the public filings if any exist, and read them the way section A22 says: check the contribution-margin definition, the ARR annualization, the LTV horizon vs the oldest cohort, and what is funding any cash-flow claim.** IM8's public letters gave a 65% P&L gross margin and a 58% "contractual" margin, opex falling from 32% to 15% of revenue, MER swinging 78% to 54% in a month, and a 6-month cohort GP:CAC falling from about 2x to 1.03x; the same transcript gives the ambassador cost as both "11% to 3.3%" and "14% to 6.2%" and the Q2 net margin as both minus 41% and minus 401% (16, unreconciled). Condition: a private competitor has no P&L; the presenter of 17 says "every financial figure here is an estimate" for Alo. Source: 16, 17. [a75628e1fb76] [70936c5570f6] [070e0c60e2f7] [9cb4c7dc31a1] [c52a5730e858]

**H2. Classify the ad account as creating demand or harvesting it: tag a sample by awareness stage, count the share carrying a celebrity or influencer name, and ask whether any cold-prospecting creative would survive if the outside engine stopped.** Alo: 96% of ads product-aware or most-aware, about 15% with a celebrity name, no cold fallback, a legitimate strategy only with fame, retail scale and press that about 95% of brands lack (17). IM8's 40-ad sample: mostly problem and solution aware, a small unaware share, 1 most-aware and 3 product-aware (16). Condition: the read tells you what the account depends on, not what it earns. Sources: 17, 16. [ec5bd4781c52] [00fc76514ab2] [095521571e86]

**H3. Map creative against a fixed format taxonomy and transcribe the dominant script; score scripts on the 8 beats (hook, problem, mechanism, proof, objection, offer, risk reversal, CTA); count voiceover vs silent; measure live-ad lifespan.** Alo's six formats (editorial panel, celebrity portrait, product grid, colorway launch, dynamic carousel, creator UGC), 21% catalog ads, 99.6% "shop now", 3 of 4 videos silent, median live-ad age 5 days and oldest 24 (17). IM8's "clock" script cloned across joint pain, menopause and alcohol personas with only the persona and destination changed (16). Condition: note what the taxonomy misses (store content, founder content in Alo's case). Sources: 17, 16. [d3b243c83ed2] [dc5261d74f44] [f8de417026bc] [49962212b27a] [31cd05ed427e]

**H4. Audit destination routing: what share of ads land on a homepage, a category grid, a persona page, an advertorial or quiz, or the PDP, and which built pages receive zero traffic.** IM8: about 150 of about 700 ads to persona pages, about 88 to the homepage, a retired quiz funnel (16). Alo: about three quarters of paid traffic to collection grids (220 ads to new arrivals, 79 to best sellers), a built cold-audience page with no ads (17). Condition: a category grid as a paid destination is defensible only in fast-merchandised fashion with a daily owner of the top slots and variant stock. Sources: 16, 17. [e4fe53bab69e] [a420b37128144] [7c106a91e81a] [c59f7a0191bc] [59a49f7f9d40]

**H5. Read the offer and price discipline: median price, cheapest entry price and whether it appears in ads, discount language in ads vs off-ad risk reversal, tier ladder and default selection, monthly-equivalent display of a longer commitment.** Alo: median $118, a $48 entry bra never advertised, 0% of ads mention price, discount or risk reversal while a 10% email capture, a member GWP, Afterpay and instant refunds run off-ad (17). IM8: a $112 / $89 / $235 ladder with the middle tier as target, a 30% subscription discount default-selected, a monthly-equivalent price at add-to-cart that the presenter says is non-compliant in a couple of US states (16, a knowing risk trade, `[web check]` before adopting anything like it). Sources: 17, 16. [7999f7f71668] [375d99aa7abb] [30f3591e0db6] [928d2ddfc162]

**H6. Audit the competitor's internal consistency, then your own: customer counts, ingredient counts and other proof numbers across same-day ads vs disclosed totals.** IM8's same-day ads claimed about 390k, 516k and 700k customers against a disclosed about 414k; the presenter reads it as an admin and compliance gap, not fraud (16). Condition: do the same audit on the brand's own library before a platform or regulator does. Source: 16. [2e205c8f91d2]

**H7. Separate transferable from non-transferable before writing recommendations, and judge the creative in its ecosystem.** IM8 transferable: persona-cloned scripts, persona pages, offer stacking, mechanism-first copy; not transferable: the $1B facility, the Beckham equity deal, the 6 to 8 month payback (16). Alo transferable: need-first scripts on a lower-risk segment, retail content as authority, collab landers; not transferable: the harvest-only account (17). The same assets relaunched under an unknown brand would perform far worse (17's 0.4 ROAS is illustrative). Repositioning a competitor's product into many angles (Gruns' 5 "products" from 1 SKU, 660 live ads) is a pattern to learn, not angles to copy, and the GLP-1 angle carries compliance risk the source ignores (21). Sources: 16, 17, 21. [179c5947001a] [1eb397831f80] [e2748fcc89c4] [b59db770ce4e] [c38bcfd6b16e]

**H8. Scrape competitors' peak-season pages and ads for next year's planning, and count concept diversity, not asset count.** True Classic about 11 core concepts, Ridge about 10, Alo about 7; Skims shipped 429 unique assets from 3 concepts, which the source flags as not advisable at smaller scale; November creative volume ran 12.6x October at Represent, 4x at Skims, flat at Alo (15, observational scrape). Condition: signals only. Source: 15. [7dc76b3e9b9f]

**H9. Use free public demand barometers (Amazon BSR daily, Google Trends for category terms and for any creator you plan to sponsor) as directional filters before committing to a category or a 6 to 12 month contract.** Look for a consistent upward line, not a spike; neither shows margin. Source: 03. [62d605c6e4da] [197b32fb0f0f] [f55c76bb188a]

### 3.I Cross-cutting operating discipline

**I1. Do all arithmetic in code and keep totals separate from breakdowns.** Breakdown numbers (Meta's age, placement and audience-segment splits) are blended reads that do not show the incremental return at the margin; do not restructure on them (01p1). Period ROAS is total value divided by total spend. Source: 01p1 and ecomOS rule. [b3d6e61e0a7a]

**I2. Every threshold in this playbook is a hypothesis until the brand's own data confirms it.** Founder figures, agency portfolio averages and hypothetical spreadsheets are marked as such in section 6. Sources: all; 04 (most conventions are situational), 10 (compare against your own data). [12509c82d440] [391c879b2d86]

**I3. Bias toward action on directional evidence for internal bets; slow down and test incrementally on anything customer-facing (a new market, a new checkout, a full-store billing-cycle switch).** True Classic's "flip the switch" international launch and its broken cross-border integration are the failure cases (05); IM8's teardown warns a wholesale switch to quarterly billing is "unbelievably dangerous" (16). Sources: 05, 16, 12 (doer over planner, explicitly time-bound to the founder's circumstances), 06 (a 90-day planning cycle is too late), 10 (money loves speed, only with significant data). [6d5f7cb9ab97] [9b738ddc9a70] [ba1c6ce5fe6a] [5efa62a4a8bd] [296fd9cf] [899c0cfa0cb1]

**I4. Timestamp every structural change and keep a pre-change baseline so the CAC and LTGP series can be compared before and after.** Sources: 19, 22. [f0fd9a23a268] [5007ba2e3]

**I5. Product leads; marketing amplifies.** A strong product with mediocre marketing can win; the reverse cannot (11, 05). Improve the hero ingredient even when it raises COGS if it drives stickiness (07). Follow the hero product the data picks, not the launch plan (12). Sources: 11, 05, 07, 12. [8bbceb08f413] [59a96c63099e] [22da9c339149] [965a3d1500b7]

## 4. Procedures (implementation)

Each procedure: goal, preconditions, steps, checks, rollback. All arithmetic runs in code from brand data. Nothing here writes to an ad platform; outputs are recommendations for a human.

### 4.1 Build the growth model sheet

Goal: one monthly model that ties the P&L waterfall, the cash model and the acquisition ratios together so every other procedure reads from it.
Preconditions: 12 months of order data with new vs returning tags, per-SKU COGS and cost of delivery, ad spend by channel, opex by line, inventory on hand and on order, cash balance. If new vs returning tags are missing, build them from customer first-order dates before anything else.

1. P&L waterfall by month, each line also as a percent of net revenue: gross revenue; minus refunds, discounts, shipping allowances = net revenue; minus cost of delivery (COGS, freight in, shipping out, pick and pack, transaction fees, fulfilment labour allocated per order) = true gross margin; minus all marketing (paid, creator fees, affiliate commission, sampling, agency fees, measurement tooling) = contribution margin; minus opex = EBITDA; minus interest = net profit (01p1, 14). Check: interest is not in opex; fulfilment staff are not in opex; transaction fees are not in opex. [f82391a766c6] [29f6666ae310]
2. Split net revenue and order counts into new-customer and returning-customer columns. Compute MER = net revenue / ad spend and AMER = new-customer net revenue / ad spend, both monthly (14). Check: AMER is the paid-media accountability line; MER is the CFO line. [3c73946c2bb4]
3. CAC = total ad spend (all platforms, including creator and affiliate cost) / new customers, from order data (19, 14). First-purchase GP per new customer = new-customer AOV x true gross margin % on the new-customer product mix. First-purchase GP:CAC (16). [176c49fbae67] [c52a5730e858]
4. Cohort table: for each acquisition month, cumulative gross profit per customer at day 30, 90, 180, 365, using actual COGS, never an assumed margin (19). LTGP:CAC at the window chosen by category: first-purchase only for furniture and homewares, 180 to 365 days for consumables, supplements, subscription and fashion (19, A8). Flag any window that extends past the oldest real cohort as modelled (16). [676a17d4a712] [376c8c477e8f] [070e0c60e2f7]
5. New-customer profit contribution = new-customer revenue minus its cost of delivery minus its marketing (14); the 2-P&L split when acquisition may be loss-making (19). [6f250e030e8c] [a6b527c71dec]
6. Cash lines (22): starting inventory, inventory purchases (cash out when paid, by supplier terms), marketing, revenue, COGS, gross profit, opex, net income, starting cash plus net cash flow = ending cash. CCC = DIO + DSO minus DPO (01p1). The 6 levers as inputs: CAC, AOV, maintained markup, returning-customer rate, 30-day sell-through, opex. [8105508e9] [7054802f6] [7e066cd286cd]
7. Payback months: months until cumulative cohort gross profit per customer exceeds CAC (09). [aac81fd83b5b]
8. Forecast lines: returning revenue bottom-up from cohort curves x cohort size x returning AOV, with seasonality; new-customer revenue from a regression of daily AMER on daily spend over about a year with peak outliers and sub-floor days removed (01p1). Mark both forecasts with their own error, not the source's claimed 1 to 10% accuracy. [2f48255ebfdf] [a3b5f20b67e2]
9. Dashboard order: new-customer profit contribution as headline; AMER and new-customer revenue and orders; CAC; LTGP:CAC; payback; ending cash and CCC (14). [6f250e030e8c]

Checks: the recomputed true gross margin vs the margin the brand quotes internally (01p1's 70% vs 24% gap); net income vs ending cash moving apart in months with a purchase order (22); AMER trend vs MER trend diverging (14). Rollback: none; this is a read model. Where an input is missing, show it as unavailable and list it under section 10, never as zero.

### 4.2 Unit economics health check (monthly)

Goal: a pass or fail on whether the brand can scale spend this month, with the reason.
Preconditions: 4.1 built for at least the trailing 3 months.

1. Read first-purchase GP:CAC for the last month and the trailing 3. Below 1.0 means the brand depends on repeat purchase to break even; note it, do not fail yet (16). [c52a5730e858]
2. Read LTGP:CAC in the category window against the bands: below 1 = stop scaling and go to 4.10; 1 to 2 = hold spend, work AOV, margin or retention; 2 to 3 = scale in 20% steps; above 3 = scale harder unless cash-constrained (14, 19). [777732c1773f] [e0b1085f47a3]
3. Read payback months against the brand's own gate; recompute what payback would be after the planned spend increase at the current CPM trend (09). [aac81fd83b5b]
4. Read the 6-month cohort GP:CAC trend over the last 4 to 6 cohorts; a falling trend at rising volume is a marginal-quality warning even when the blended number passes (16). [3ca0714a9b6d]
5. Read AMER vs MER: if MER rose and AMER fell, block the spend increase and flag the returning-revenue trap (14). [3c73946c2bb4]
6. Read ending cash and CCC: if the planned growth implies an inventory buy the cash cannot cover without new financing, route to 4.8 before approving spend (01p1). [eecd54f14ae1]
7. Read opex as a percent of revenue vs 6 months ago; if it rose while LTGP:CAC did not, flag opex creep (19, 22). [7b24b5654a81]
8. Output: pass, hold, or stop, with the binding line and the next procedure to run.

Checks: every ratio uses net revenue (A2); the CAC denominator is new customers from order data, not platform conversions (A6). Rollback: none.

### 4.3 Bottleneck diagnosis

Goal: name the one constraint and the lever that moves it, before any spend, creative or structural change.
Preconditions: 4.1; access to platform reports (Meta read-only) with 7-day-click and attribution comparison; frequency by audience segment.

1. Data integrity pass (14's 9 mistakes): 1-day view still in headline reporting; existing customers excluded from cold campaigns; brand and non-brand split; campaign count vs spend; tertiary channels with fake-high ROAS; existing-customer spend and frequency; traffic or reach campaigns with no measurement plan; DPA share; any testing structure. Fix what is broken here first and re-read the month. `[verify UI: Meta Columns, Compare Attribution Settings]` [c3b26441e2aa] [d233cdfd3b00]
2. Read the CAC and LTGP series month over month with new-customer volume and revenue. If CAC is rising while volume and revenue fall and spend was raised to hold revenue, the death spiral is running: go to 4.10 (19). [6da370548f56]
3. Run the 2-P&L split if the blended P&L looks fine but step 2 is ambiguous (19). [a6b527c71dec]
4. Archetype read (B7): product-led (reorders with average ads), media-led (growth tracks creative volume), harvest-only (bottom-2 awareness stages dominate, celebrity names carry prospecting). Record it; it changes the lever. [ec5bd4781c52] [59a96c63099e]
5. Three-layer read (10): ads (CPM, CPC, CTR, hook rate vs the brand's own baseline), funnel (conversion rate x AOV, and the 300 screen at the brand's own CPC), backend (repeat rate, LTV). Instrument every step: ad, landing view, add to cart, checkout, purchase. [cd2ec58854db] [4fc18ca8c1c4] [9e6eb4c8669a]
6. Traffic vs conversion (B5): no spend = creative; spend without return = funnel, offer or page; cheap clicks with cart abandonment = price. If page is suspected, run 4 to 5 ad angles against the existing page for 1 to 2 days before touching the page (11). [69f4ae6b] [a9b568d2aeff] [6b9ad04ab9c3]
7. Creative supply check for media-led brands: new creatives per month vs the brand's own historical ratio of spend per creative unit (references: about $2,500 per unit, 1 per $1,000 of monthly spend, 200 a month floor, all self-reported); frequency climbing on an angle = angle-TAM ceiling, open a new persona (16, 01p2, 18, 21). [49962212b27a] [3ed85b1ffd80] [bbac1e69e635] [b2da5bc185dd]
8. Existing-customer and warm-audience check: frequency on existing customers over 30 days (audits find 20 to 100; about 10 is a gut check), share of spend on existing customers, share of "cold" conversions from returning customers; a healthy ROAS with flat topline is usually this (20). Recommend a lift test before a cut. `[verify UI: Meta experiments, conversion lift]` [ca90d7c1ca85] [9497f75a4f1]
9. Channel-level top-down (01p2): weight by spend share, decompose revenue = sessions x conversion rate x AOV, extend the window, use conversions by conversion time, find the inflection date, then drill to the campaign and submetric. Write the discipline sentence before recommending any change. [74d14b3daff2] [34e9220c4fce]
10. Outside-account check (17, 14): list influencer deals, retail openings, PR, seasonality and channel launches in the window; size the plausible inside-account effect (about 1% at scale) against the swing. [ea0fb51b4d36] [33775b73749d]
11. Output: the bottleneck diagnosis memo (9.2): constraint, evidence, lever, owner folder, expected lag (60 to 180 days for cash levers), the test that would confirm it, rollback.

Checks: the memo names exactly one primary constraint; every number cites the data-layer query that produced it. Rollback: recommendations only; if a recommended change is made by a human and the CAC/LTGP series worsens over the confirmation window, the memo's rollback step applies.

### 4.4 Stage review (quarterly)

Goal: confirm the brand is running the plan for its stage and name what must change before the next boundary.
Preconditions: trailing 12-month revenue, current monthly spend, team list, measurement stack, ad-account structure summary (read-only).

1. Place the brand: revenue band (C1 to C4) and monthly spend band; note if the two disagree and why (marketing ratio outside 8 to 20% of revenue). [fd46c05f]
2. Measurement layer vs stage (14): $1 to 5M has 7-day click, COGS tagging, the new-customer dashboard, exclusions and minimized brand search; $5 to 20M adds in-platform lift and incremental attribution; $20M+ runs geo-lift, an omnichannel dashboard and applied incrementality factors. Mark each as present or missing. [23010ab3b691] [99402b442662] [28067949e768]
3. Creative and production vs stage (01p2): concept count, production budget share, creator count, assets per month, against the tier table in C5. [ec0c882e1e06] [e530277843071]
4. Account structure vs stage (01p1, 01p2): campaign count justified by distinct funnels, personas, regions or KPIs; conversions per campaign against the 100 to 200 a month inflection; a scaling campaign only above about $400 a day plateaued spend. [d39e9023291d] [1fe205b60578] [81e15385dc8b]
5. Channel sequencing vs stage (3.D): primary channel headroom named; tertiary channels lightly funded; retail and Amazon only after digital proof; international only at the operational-fit triggers. [0805d0da06ef] [406f95cc2038]
6. Team vs stage (3.C): founder still running ads above $30k a month (08); no finance capability above $1M (05); no ops generalist by the time the founder's weakest function binds (12); decision loop above 5 to 8 people (09); opex sized for a past peak (22). [af4b9f233f1a] [a9156795ce70] [281ef6e02753] [b5802ce3e875] [71b3d1891]
7. Brand vs performance split vs stage (07): record the current split and whether a brand line exists at all past about $20M (01p1). [5a9b4680ac1d] [e08bf0b419e3]
8. Retention phase check (C6): has a deliberate retention phase started after the first year, starting with the offer structure? [7d3b5a19ab1e]
9. Output: the stage plan (9.3): what is in place, what is missing for this stage, what the next boundary requires, in priority order with owner folders.

Checks: each "missing" item is tied to a rule in 3.C. Rollback: none.

### 4.5 Next best dollar (channel mix review)

Goal: decide where the next increment of spend goes and which channel, if any, to cut.
Preconditions: spend and new-customer revenue by channel by month; any lift or holdout reads; existing-customer share of spend by channel.

1. For each channel compute AMER and, where available, incremental AMER from holdouts or lift tests; where none exists, mark the read as attributed and apply the reliability tier (A24). [3d5f23fdd11d] [217c8dc47244]
2. Strip the 3 inflators from each channel's read: view-through, existing-customer conversions, and any halo event in the window (14). Mark branded search, retargeting, DPA and email-attributed revenue as harvest, not growth. [d63cd6fefbdc] [53cff4b8747]
3. Check for overlap: any pair of channels that may share demand (Amazon and TikTok Shop, Meta and Google brand) gets a pause-one test or a geo holdout recommendation before either is scaled (04). [89eb781b3bd2]
4. Rank channels by incremental AMER relative to break-even; the next dollar goes to the channel with the most headroom below its frontier, not to the channel with the highest attributed ROAS (01p1, 04). [c7c32c187bce]
5. Before adding a new channel: name the primary channel's remaining headroom, confirm creative capacity to feed a second channel, and fund it as a separate experiment with its own creative and success criteria (09). [0805d0da06ef]
6. Concentration check: share of spend and revenue on the top platform, top retailer, top creator; flag above the level the brand has stress-tested (03, 09). [492ad9d02ac5]
7. Existing-customer spend: recompute as customers x target frequency x CPM in dollars, not a percent, and compare to actual (01p1, 01p2). [df7a0134cc56] [421e7aee0498]
8. Calendar: list upcoming email drops, launches and promotions and reduce paid pressure around them (08). [222d8f7291df]
9. Output: the channel mix plan (9.4): current mix, incremental read per channel with its tier, the next-dollar allocation, the cut candidates with the test that confirms each, and the concentration risks.

Checks: no allocation moves on a platform-reported ROAS alone. Rollback: each reallocation carries a confirmation window (weekly AMER read for 4 weeks) and a revert condition.

### 4.6 Peak season plan (Black Friday)

Goal: a written plan 70 or more days out with budget, creative volume, offer ladder, pacing and the 3 corrections applied.
Preconditions: prior-year hourly revenue and spend curves; prior-year data in both 1-day and 7-day or 30-day click windows; 6-month repeat by acquisition month for 2 prior years; gross margin by SKU; planned discounts; inventory by grade; production capacity; page-limit headroom. All `[needs brand data]`.

1. Objective: profit play or inventory play, decided with the user and written down with the CAC tolerance it implies (15). [9b4e9226481]
2. Corrections (15): attribution multiplier from prior-year short vs long window; November cohort repeat vs a normal month; discount-adjusted break-even ROAS per offer tier. Output a corrected CAC allowance for November. [ebb016b64886] [7473b6195d7f] [61f3aa873861]
3. Budget: base and stretch models with numeric gates; front-load 31 to 43% of the September-to-December total into September and October as the calibration range; expect CPMs 25 to 30% above October from about November 12 and do not carry last year's CPMs (15). [71ba87612a01] [62e69271e95c] [6a2ae399039b]
4. Creative volume: peak-day spend target / realistic per-ad ceiling from the brand's own history = ads that must hold volume; add tail buffer (bottom 80% of ads held about 54% of spend); check production capacity and page limits; if short, lower the target or raise capacity now (15). `[verify UI: Meta page and ad limits]` [075f80613bc3] [291583358578] [9f9579f3d2c0]
5. Format mix by planned spend share: offer statics, offer-overlaid evergreen, creator or founder content, product or VSL, early access; 4 creative phases with the offer locked first (15). [0fd306b87cfb] [d6a9aa0c6869]
6. Offer ladder: fallback offers with landing pages and creative pre-loaded and trade-number triggers (15); every scarcity or deadline claim tied to a real end date (E7). [e2262e74c26f] [3a1292e93ad7]
7. Pacing sheet from prior-year hourly curves with the attribution multiplier baked in; per-hour multipliers for the 5 to 7am spend peak vs 7 to 11am revenue peak; the 3-day rolling CM3 scaling rule written down (15). [5afc0c5d082f] [6f476966cae3] [3b63d06d5486]
8. Google prep: titles, assets, promotion feeds and Merchant Center pricing updated in advance; no weekend budget raises on Google ROAS alone (15). `[verify UI]` [16f43795044b]
9. Evergreen: list the campaigns that must not be turned off and the winners to duplicate with the offer badge (15). [7c0dc6951b2c]
10. Operations: 3PL and 4PL paperwork per region, inventory buffer vs expected spike, support capacity, restock lead time; decide in advance whether to protect stock into December (13, 18). [ac76fdafcc3e] [ccdffe1f5d76]
11. Q5 offer prepared for about December 16 to 31 (15). [5eab80b6afef]
12. Post-peak: extend the measurement window for pre-season tests; do not credit any channel launched in October with the lift without a causal read (14, 15). [1d313c3eb80b] [33775b73749d]

Checks: the plan names the objective, the corrected CAC allowance, the creative count that can hold spend, the gates, and the owner of each. Rollback: the base-to-stretch and pullback gates are the rollback.

### 4.7 Brand teardown intake

Goal: a teardown report (9.6) that reads a competitor as a set of signals and states what is transferable.
Preconditions: a scrape of the competitor's public ad library and public pages (inspiration layer), any public filings, the brand's own data for comparison. Public research stays separate from private business data.

1. Context and finances: what is public, what is estimated; apply A22 to any P&L or letter (16, 17). [a75628e1fb76] [70936c5570f6]
2. Awareness-stage tag on a sample of 40 or more ads; share carrying a celebrity or influencer name; creating vs harvesting verdict (17, 16). [00fc76514ab2] [095521571e86]
3. Format map against a fixed taxonomy; transcribe a sample of scripts and score the 8 beats; voiceover vs silent; median and maximum live-ad age; new-asset cadence (17). [d3b243c83ed2] [dc5261d74f44] [31cd05ed427e]
4. Destination audit: share of ads to homepage, grid, persona page, advertorial or quiz, PDP; built pages with no traffic (16, 17). [a420b37128144] [7c106a91e81a]
5. Offer and price audit: median price, entry price and whether advertised, discount and risk-reversal language in ads vs off-ad, tier ladder and default, subscription display (17, 16). [7999f7f71668] [30f3591e0db6]
6. Consistency audit: proof numbers across same-day ads vs disclosed figures (16). [2e205c8f91d2]
7. Dependency audit: what outside engine the account relies on (fame, retail, PR, financing, celebrity equity) and whether the brand under review has it (17, 16). [ec5bd4781c52] [179c5947001a]
8. Transferable vs not, with the ecomOS line: patterns of structure, mechanism, format mix and routing may inform original work; text, products, faces and page copy may not be copied; competitor ads are signals, not proven winners (16, 17, 21). [e2748fcc89c4]
9. Route each transferable pattern to its owner folder (10-MCR, 07-LPG, 03-OFF, 04-BRD) as a hypothesis to test on the brand's own traffic.

Checks: every percentage is labelled a composition read; no line in the report reproduces competitor copy. Rollback: none.

### 4.8 Founder decision memo (raise, sell, partner, hire a CEO, take debt)

Goal: a memo the founder can decide from, with the mechanics, the numbers and the risks named.
Preconditions: 4.1, cap table and ownership, current debt and terms, personal and company objectives from the user, exit intent.

1. State the decision and the objective it serves (growth, cash, control, personal liquidity, succession).
2. Options in order of dilution and cost: profit and supplier terms; a revolver, recap or factoring; a strategic minority partner (1+1=3 test and EV test); investor capital (whose money, what return, what horizon, low-touch or not); a secondary; a full sale (04, 05, 03, 07, 12). [e9d130295214] [f90e66edbcd2] [4410f4acddbe] [93d8ebb61724]
3. For any debt or PE option: the implied leverage multiple against 2 to 3x conservative vs 6 to 7x, and whether the business services it in a downturn (04). [edf06536c8b7]
4. For any sale: buyer type and what it underwrites on; competitive process size (8 to 10); timeline (about 10 months); term traps (participation, second bite, add-backs); founder-meeting strategy set by exit intent; non-compete length (07, 04, 12). [399d57d8b870] [fca479f57f8f] [20817201b1bb] [629185c92369]
5. For any multiple cited: the band, its source, and the note that it is a founder heuristic `[web check: current multiples]` (13). [dc145902632]
6. For a CEO or GM replacement: the archetype the stage needs, the "not my mirror opposite" check, a trial of about 6 months (13). [116713e4f02a]
7. Key-person and key-channel risk after the decision (G12). [492ad9d02ac5]
8. The time-travel question and a pre-committed ceiling for any competitive bid (E9). [239a4c7c7019] [80d1a965dcd8]
9. Output: the memo (9.7) with a recommendation, the numbers behind it, the things the agent cannot know (section 10), and a note that legal, tax and deal advice is required before signing.

Checks: no option is presented without its downside case. Rollback: not applicable; the memo recommends, the founder decides.

### 4.9 Cash conversion model and lever plan

Goal: find which of the 6 levers binds and plan a 2 to 3 lever move with a baseline kept.
Preconditions: 4.1 step 6 built.

1. Run the base model 6 months forward at current inputs (22). [7054802f6]
2. Re-run once per lever with a plausible change (the source's illustrative moves: CAC down about 15 to 20%, AOV up about 20% without discounting, markup 4.0 to 4.5, returning share 25% to 35% with the cost of the retention hire included, sell-through 30% to 40% by cutting weak SKUs, fixed opex cut to current revenue). Read ending cash at day 30, 60, 90 and 180, not day 30 alone (22). [32440a917]
3. Rank levers by ending-cash effect and by feasibility; note that opex cuts hit cash 1:1 and marketing cuts do not (22). [71b3d1891]
4. Pick 2 to 3 to move together; keep the base run as the comparison (22). [5007ba2e3]
5. Route each lever to its owner: CAC to 24-DEP and 10-MCR; AOV to 03-OFF and 07-LPG; markup to 18-COG and 03-OFF; returning rate to 14-EML and 17-CXP; sell-through to 18-COG; opex to 21-OPS.
6. Reinvest freed cash deliberately (default: marketing at the channel with headroom from 4.5).

Checks: every input is the brand's own; the source's dollar outputs are never quoted as expectations. Rollback: the base run.

### 4.10 Death spiral response

Goal: stop the loop without starving revenue or the balance sheet.
Preconditions: 4.3 step 2 found CAC rising with falling volume and revenue, or LTGP:CAC below 1.

1. Freeze spend increases; do not raise budget to hold revenue (19). [6da370548f56]
2. Confirm the read is real: strip view-through and existing-customer conversions, check for a halo, re-read AMER (14, 19). [d63cd6fefbdc] [217c8dc47244]
3. Run the 2-P&L split; if returning profit subsidizes a first-time loss, document it as the funding route and set its limit (19). [a6b527c71dec] [ceffceaa4132]
4. Decompose CAC into CPC / conversion rate and CPC into CTR x CPM; assign the fix to the weak surface: creative and offer framing for CTR, page, price presentation and checkout for conversion rate (19). [2ee0c2788115]
5. Work the ratio, not the funding: raise first-order gross profit (offer structure, bundles without discounting, prepaid tier tested in isolation), raise margin (markup, cost of delivery), or lower CAC; retention tactics cannot move a category-bound LTGP (19, 16, 22). [376c8c477e8f] [f55f1e9b4827] [871d9318f]
6. Check opex creep separately and cut fixed cost sized for a past peak (19, 22). [7b24b5654a81] [71b3d1891]
7. If the brand is cash-constrained by unsold inventory, route spend into C and D stock deliberately rather than cutting marketing across the board (01p1). [2ba72747cc86] [8669aea558c2]
8. Set the confirmation window at 60 to 180 days on the cash lines and weekly on AMER and CAC (22, 05). [32440a917] [0e1860afecb6]

Checks: every step names the number it expects to move. Rollback: if AMER falls further after a change, revert that change first and re-read before the next.

## 5. Diagnostic checklists

Written so a worker can run each one from the data layer and the brand record. Every "good" or "bad" threshold is the source's, marked in section 6 with its confidence.

### 5.1 Unit economics health check

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Ratios on net revenue | Confirm refunds and discounts are subtracted before any ratio | All ratios net | Gross revenue anywhere in a ratio | Rebuild 4.1 step 1 | 01p1, 14 |
| True gross margin vs quoted margin | Recompute per SKU with all delivery costs | Recomputed margin within a few points of the quoted one | Large gap (source example 70% vs 24%) | Reset every break-even and budget from the true figure | 01p1, 04 |
| COGS tagged per SKU | Product-level cost fields present | All active SKUs tagged | Flat "average margin" used | Tag before any promotion | 14, 19 |
| New vs returning split | Order tags, revenue and orders by type | Both lines present monthly | Blended only | Build tags from first-order dates | 14, 20 |
| AMER vs MER | Trailing 3 months | Both flat or rising | MER up, AMER down | Block spend increase; A3 | 14 |
| First-purchase GP:CAC | New-customer AOV x true GM % / CAC | At or above 1.0, or below 1.0 with a verified cohort subsidy | Below 1.0 with no cohort data | Read cohorts; if none, treat as death-spiral risk | 16, 19 |
| LTGP:CAC in category window | Cohort GP / CAC at 30, 90, 180 or 365 days | 2 to 3 | Below 1; or 1 to 2 with rising opex | 4.10, or hold and work AOV, margin, retention | 14, 19 |
| Above 3 | Same | Scale harder | Cash-constrained: hold | 4.5 next best dollar | 14 |
| Payback months | Months to cumulative cohort GP > CAC | Within the brand's own gate (IM8 uses under 4 blended) | Payback lengthens after the planned spend step | Recheck at current CPM trend before scaling | 09, 16 |
| 6-month cohort GP:CAC trend | Last 4 to 6 cohorts | Flat or rising | Falling at rising volume (IM8 2x to 1.03x) | Marginal-quality warning; slow the ramp | 16 |
| Profit vs cash | Net income vs ending cash by month | Move together, or gap reconciles to a PO | Profit up, cash flat or down, no PO explains it | Model CCC; 4.9 | 01p1, 22 |
| Opex share | Opex % of revenue vs 6 months ago | Flat or falling | Rising while LTGP:CAC did not | Cut fixed cost sized for a past peak | 19, 22 |
| Discount rate vs burn | Daily discount % of sales with daily spend | Discount % stable | Revenue up with discount % up | Re-run margin; A5 | 08 |

### 5.2 Bottleneck diagnosis

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| 1-day view in headline reporting | Compare attribution settings `[verify UI]` | 7-day click within a few % of blended | Large gap (30 to 50% claimed) | Report on 7-day click; deliver on 7-day click / 1-day engaged | 14, 01p1 |
| Existing customers in cold campaigns | Exclusion lists applied and fresh; audience segment breakdown | Cold conversions mostly new | Returning share high in "cold" | Refresh exclusions; audit CRM sync | 14, 01p2 |
| Existing-customer frequency | Frequency on that segment, trailing 30 days | Around 10 or below | 20 to 100 | Cut as a hypothesis; confirm with a lift test | 20 |
| Campaign count vs conversions | Monthly conversions / active campaigns | Comfortably above 100 to 200 per campaign | Well below | Consolidate | 01p1, 14 |
| Tertiary channel with high ROAS at low spend | Spend share vs reported ROAS | ROAS consistent with spend level | Very high ROAS at tiny spend | Lift read before crediting | 14 |
| Any traffic, reach or DPA campaign without a measurement plan | Ask "how would we know if this worked" | A test design exists | Before-and-after only | Define lift test or CausalImpact, or stop funding | 14 |
| CAC and LTGP series | Monthly table with volume and revenue | CAC stable or falling, volume holding | CAC up, volume and revenue down, spend raised | 4.10 | 19 |
| First-time P&L | 2-P&L split | Near breakeven or a verified subsidy | Deeply negative while blended looks fine | Fix first-time loss first | 19 |
| Archetype | Reorders with average ads; growth vs creative volume; awareness-stage mix | Archetype named | Unknown | Read B7 before picking a lever | 05, 17, 09 |
| Ads layer | CPM, CPC, CTR, hook rate vs own baseline | Cheap and qualified | Cheap but unqualified, or no spend delivered | Creative or hook | 10, 06 |
| Funnel layer | CR x AOV vs own CPC | At or above the brand's own 300-equivalent | Well under | Fix CR or AOV before spend | 11 |
| Price vs creative | Clicks cheap, carts abandoned | Conversion holds | Abandonment high | Test price or offer, not the ad | 08 |
| Angle vs page | 4 to 5 angles on one page, 1 to 2 days | One angle separates clearly | None separates | Product-market fit or persona problem, not messaging | 11 |
| Creative supply | New creatives per month vs spend per unit history | Supply matches spend | Below the brand's own ratio | Volume before optimization | 16, 18, 01p2 |
| Angle saturation | Frequency and spend by angle | Frequency stable | Frequency climbing, spend stalls | New persona, not new bid | 21 |
| Outside-account events | Calendar of influencer, retail, PR, launches | Accounted for | A swing credited to a tweak | Size the inside-account ceiling (about 1%) | 17 |
| Discipline sentence | "Underperforming because X dropped, driven by Y, caused by Z" | Sentence complete | Cannot complete it | No change yet | 01p2 |

### 5.3 Stage review

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Stage placement | Trailing 12-month revenue and monthly spend | Both bands agree | Spend band above revenue band | Check marketing ratio; C rules | 06, 14 |
| Measurement layer | Items present vs the revenue band list | All items for the band | Missing items | Add in the order of 14's bands | 14 |
| Creative tier | Concepts, production share, creators, assets per month | Matches C5 tier | Below tier | Production plan; 10-MCR | 01p2 |
| Account structure | Campaigns justified; conversions per campaign | Justified and above inflection | Campaigns added "because spend grew" | Consolidate; 24-DEP | 01p1 |
| Budget pacing method | Step size on winners | 20% steps (doubling only at very small scale) | Doubling at 6 figures | Switch to steps | 06, 01p1 |
| Primary channel headroom | Named estimate | Named | Not named, yet new channels added | Name it first | 09 |
| Founder still running ads | Monthly spend | Under $10 to 30k a month | Above, with no owner | Hire or fractional buyer | 08 |
| Finance capability | CFO, fractional CFO or models | Present above about $1M | Absent | Hire early | 05, 12 |
| Founder's weakest function | Task audit | Hired first | Founder still does it | Ops generalist, then paid owner, then CMO | 12 |
| Decision loop size | People in any given decision | 5 to 8 or fewer | More | Cut | 09 |
| Opex sized for past peak | Fixed costs added at a high period | Resized | Still there | Cut, 1:1 to cash | 22 |
| Brand line | Any spend not held to ROI, above about $20M | Present | None | A brand line | 01p1, 07 |
| Retention phase | Deliberate phase after year one, offer first | Started | Not started, or flows only | C6 | 09, 20 |
| Sustainable pace | Internal pace target before the next tier | Set | Not set | Set with support and inventory plan | 18 |

### 5.4 Channel mix review

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Incremental read per channel | Holdout, lift or CausalImpact | Exists for large channels | Attributed only | Tier the read; recommend a test | 14, 19 |
| Inflators stripped | View-through, existing customers, halo | Stripped | Not | Strip before ranking | 14 |
| Harvest vs growth | Branded search, retargeting, DPA, email marked | Marked as harvest | Counted as growth | Reclassify | 20, 14 |
| Branded search share | % of marketing spend | Near 1% for a high-awareness brand; protected for a low-awareness one | Uncapped and justified by its ROAS | Holdout; see 7.2 | 04, 14 |
| Overlap | Pairs sharing demand | Tested | Untested | Pause-one or geo test | 04 |
| Next dollar | Channel furthest below its frontier | Named | Sent to highest attributed ROAS | Reallocate | 01p1, 04 |
| New channel funding | Separate experiment with own creative and criteria | Yes | Reallocation from core | Ring-fence | 09 |
| Tertiary channels | Combined spend and staffing | Light, flexing, no dedicated buyer | Dedicated buyer per tiny channel | Consolidate | 04 |
| Concentration | Top platform, retailer, creator share | Below stress-tested level | Above | Diversify deliberately | 03, 09 |
| Existing-customer budget | Customers x frequency x CPM in dollars | Matches actual | Set as a % of spend | Recompute | 01p1, 01p2 |
| Paid vs owned calendar | Upcoming drops and launches | Paid pulled back around them | Not coordinated | Coordinate | 08 |
| Organic engine | Posting cadence and organic winners feeding paid | Active | Stopped | Restart; 13-ORG | 08, 04 |
| Retail and Amazon sequence | Digital proof before pitch; buffer for POs | Sequenced | Early mass retail, no buffer | 3.D7 | 03, 05, 07 |

### 5.5 Black Friday readiness

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Objective set | Profit play or inventory play written | Set with CAC tolerance | Unset | Decide with user | 15 |
| Attribution multiplier | Prior-year 1-day vs 30-day click | Multiplier derived | Not derived | Derive; expect about 40% normal, about 80% November as the source's range | 15 |
| Cohort correction | November vs normal-month 6-month repeat, 2 years | Checked | Assumed | Check the brand's own | 15 |
| Margin correction | Break-even ROAS per tier from actual margin | Modelled | Assumed multiplier | Model | 15 |
| Front-load | Sep and Oct share of Sep to Dec budget | In or near 31 to 43% | Under, with a pre-sale ROAS dip read as weakness | Do not cut pre-sale | 15 |
| Base and stretch gates | Numeric gates written | Written | Verbal | Write | 15 |
| Creative count that can hold spend | Peak spend / per-ad ceiling | Enough plus tail | "12 to 18 ads exist" | Production or lower target | 15 |
| Format mix | Planned shares | Planned | Chasing the highest raw ROAS format | Plan | 15 |
| Offer ladder | Fallbacks, pages, creative, triggers | Pre-built | One fixed offer | Pre-build | 15 |
| Scarcity claims | Real end dates and stock | All real | Any resetting or invented | Remove | 02, 17 |
| Pacing sheet | Prior-year hourly curves with multiplier | Built | Flat daily caps | Build | 15 |
| Scaling rule | 3-day rolling CM3 rule written | Written | Ad hoc, 8am target | Write | 15 |
| Evergreen | List of campaigns not to pause | Listed | Plan to pause | Overlay instead | 15 |
| Google prep | Titles, assets, promotion feeds, pricing `[verify UI]` | Done in advance | Weekend budget raises | Prep | 15 |
| Page limits | Headroom for the ramp `[verify UI]` | Enough | None | Add pages in advance | 15 |
| 3PL and 4PL paperwork | Signed per region | All signed | Any missing | Sign before the date | 13 |
| Inventory buffer and support | Buffer vs spike; support capacity | Sized | Not | Size; decide stock protection | 18, 03 |
| Q5 offer | Prepared for about Dec 16 to 31 | Prepared | Leftover dump | Prepare | 15 |
| Macro and CPM assumption | This year's rates and inventory `[web check]` | Updated | Last year's CPMs | Update | 15 |

### 5.6 Teardown intake

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Public data sources listed | Filings, letters, scrape, pages | Each labelled by reliability | Mixed together | Label | 16, 17 |
| P&L read | CM definition, ARR month, LTV horizon, financing | Each questioned | Taken at face value | A22 | 16 |
| Awareness tag | Sample of 40+ ads | Done | Not | Do | 16, 17 |
| Celebrity share | Ads with a named person | Counted | Not | Count | 17 |
| Creating vs harvesting verdict | From the two above | Stated | Not | State | 17 |
| Format map and script scoring | Taxonomy, 8 beats, voiceover share, ad age | Done | Not | Do | 17 |
| Destination audit | Share by page type; unused pages | Done | Not | Do | 16, 17 |
| Offer and price audit | Median, entry, ad language vs off-ad, ladder, display compliance | Done | Not | Do | 17, 16 |
| Consistency audit | Proof numbers across same-day ads | Done | Not | Do | 16 |
| Dependency audit | Outside engine the brand under review lacks | Named | Not | Name | 17, 16 |
| Transferable vs not | Two lists | Present | Missing | Write | 16 |
| ecomOS line | No copied text, product, face or page copy; signals only | Confirmed | Any copied element | Remove | rule |

### 5.7 Founder decision memo check

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Objective stated | Growth, cash, control, liquidity, succession | Stated | Implicit | State | 03, 07 |
| Cheapest options first | Profit, terms, revolver, factoring before equity | Considered | Skipped to equity | Add | 04, 05 |
| Leverage modelled | Implied EBITDA multiple; downturn service | 2 to 3x or the business survives worse | 6 to 7x, growth-dependent | Flag | 04 |
| Investor questions | Whose money, return, horizon, touch | Answered | Unasked | Ask | 07 |
| Strategic partner tests | 1+1=3 and EV increase | Both pass | Either fails | Do not sign | 03, 13 |
| Buyer type and underwriting | Strategic vs PE | Pitch matched | Generic | Match | 07 |
| Process design | Banker, timeline, 8 to 10 buyers, transparency | Designed | Single buyer or "everyone" | Design | 07 |
| Term traps | Participation, second bite, add-backs, earnout | Reviewed with counsel | Headline only | Review | 04 |
| Multiples | Band, source, currency of check | Labelled heuristic, `[web check]` | Assumed outlier | Label | 13 |
| Founder-meeting strategy | Set by exit intent | Set | Default | Set; legal review | 12 |
| CEO replacement | Archetype, not mirror opposite, 6-month trial | Defined | Reactive | Define | 13 |
| Key-person and key-channel risk after | Named with mitigations | Named | Ignored | Name | 03, 09, 08 |
| Downside case | For every option | Present | Missing | Add | rule |
| Advice line | Legal, tax and deal advice required before signing | Present | Missing | Add | 04, 12 |

## 6. Thresholds and benchmarks

Confidence key: **Multi** = 2 or more independent sources agree (same-agency restatements count once). **Single** = 1 source. **Founder** = founder self-report on a promotional interview. **Agency** = agency portfolio average or heuristic with a service to sell. **Hypo** = explicitly hypothetical or spreadsheet illustration. **Disclosed** = from public filings, still narrative. **Study** = academic study (02), dated and in a non-ecommerce context. Every value is a hypothesis until the brand's own data confirms it.

| Value | Condition | Source | Confidence |
|---|---|---|---|
| Break-even ROAS = 1 / true gross margin %; break-even CAC = gross margin $ | Any product or discount | 01p1, 15 | Multi (arithmetic) |
| LTGP:CAC bands: <1 spiral, 1 to 2 tight, 2 to 3 scale, >3 underinvesting (cash exception) | 180-day or category window | 01p1, 14, 19 | Agency (one voice, stated 3 times) |
| LTV:CAC 3:1 baseline; 7 to 10:1 high ticket | Most DTC vs high ticket | 10 | Single, course seller |
| CAC:LTV 3.0 to 3.5x on 24 months; payback under 4 months blended | IM8 gate | 09 | Founder |
| Payback bands: <4 excellent, 6 good, 12 weak; host calls 6 to 12 "world class" | Same interview, unresolved | 09 | Founder, inconsistent |
| IM8 disclosed 3:1 is a 36-month projection; oldest cohort 20 months | Reading any LTV claim | 16 | Disclosed |
| First-purchase GP:CAC 0.51 (Jul 2026), 0.4 (Q2); 6-month cohort GP:CAC 2x to 1.03x | IM8 | 16 | Disclosed |
| Day-365 GP lift: fashion ~55%, CPG and supplements ~110%, furniture ~0%; ~80% of brands weak | Category bands | 19 | Agency, unsourced |
| DTC gross margin 40 to 50% after all fulfillment at launch | CPG DTC | 07 | Founder |
| New-category gross margin ~75% fully delivered | Ridge's bar | 04 | Founder |
| Yeti gross margin ~51% | Public comparator | 04 | Single, public figure cited |
| True gross margin example: 70% product margin to 24% | $100 t-shirt | 01p1 | Hypo |
| 20% storewide discount: 50% GM to 37.5% | COGS tagging | 01p1, 14 | Agency (arithmetic) |
| 1-day view share of reported ROAS 30 to 50% | Meta default attribution | 01p1, 14 | Agency |
| Platform attribution error 5 to 10% low, 30 to 50% high | Post-tracking changes | 10 | Single |
| Reported 20x to 7x after stripping view-through | One Australian retailer | 19 | Agency |
| MER 4x to 5x while AMER 2.0 to 1.8 to 1.6 | Returning-revenue trap | 01p1, 14 | Hypo |
| Conversion inflection ~100 to 200 a month per campaign | Meta consolidation | 01p1 | Agency |
| Existing-customer frequency: audits find 20 to 100 a month; ~10 gut check | Paid to existing customers | 20 | Single |
| Existing-customer frequency cap under 8 (7-day) or under 7 (30-day) | Same source, 2 windows | 01p1 | Agency, inconsistent |
| Cold-ad frequency red flag above ~2 (30 to 60 days) | Meta cold campaigns | 01p2 | Agency |
| Incrementality testing relevant to top ~20% of brands | Measurement tier | 01p1 | Agency |
| Measurement rollout: 7-day click and COGS at $1 to 5M; lift tests at $5 to 20M; geo-lift at $20M+ | Revenue bands | 14 | Agency |
| Holdout adoption ~$15 to 50M revenue | Ridge estimate | 04 | Founder |
| Measurement tooling ~1% of marketing spend, justified by ~5% lift | Ridge | 04 | Founder |
| Chaos theory above ~$100k a month; ROAS model breaks ~$20 to 50M revenue at 8 to 20% of revenue on marketing | Attribution breakdown | 06 | Single, course seller |
| TikTok and Google lift-test minimum ~$200k | In-platform lift | 01p1, 14 | Agency `[web check]` |
| Pure performance ceiling ~$1M to 20M; diminishing returns past $30 to 40k a day | Brand line | 01p1 | Agency |
| Brand vs performance: 90/10 pre-fit, 60/40 brand teenage, mostly brand mature; ~$200M flip | Stage | 07 | Founder, unsourced |
| Sampling ~10% of marketing as a fixed line | Cheap shelf-stable products | 07 | Founder |
| Meta share: 50% (04, 05), 60 to 70% (14), 80 to 90% (01p2), 85% (09); <5% (03) | Channel mix | see | Founder or agency, wide range |
| Google and YouTube 15 to 20% or 20 to 25% | True Classic, same interview | 05 | Founder, inconsistent |
| Ridge mix 50/20/10/20; tertiary $1 to 10k a day | Ridge | 04 | Founder |
| Bloom: 85% influencers, <5% Meta; DTC <5% of revenue | Bloom | 03 | Founder |
| Branded search cap ~1% of marketing spend | High-awareness brand, own holdouts | 04 | Founder; conflicts with 7.2 |
| Shopping 80 to 90% of Google spend; PMax 20 to 40% of Google | Ecommerce | 01p2 | Agency |
| Creator fee: half the brand's Meta CPM; anchors $10 (03) vs ~$2 (13) | Bloom method | 03, 13 | Founder, inconsistent anchors |
| Small-channel sponsorship CPM ~$5 to 10 | YouTube mid-rolls | 04 | Founder |
| Affiliate floor $1,000 a month or 15 to 20% commission; 30 videos in 30 days | Comfrt | 18 | Founder |
| Micro-creators under 10k followers; 5,000 to 50,000 band on limited budget | Comfrt; Bloom | 18, 03 | Founder |
| Creative unit sustains ~$2,500 of spend | IM8 scrape | 16 | Single, analyst read |
| 1 new ad per $1,000 monthly spend; mean spend per ad $700 to 1,500 | Meta | 01p2 | Agency |
| 200 new creatives a month floor | Comfrt | 18 | Founder |
| 50 to 1,500 active ads in 13 months at $150 to 300k a day; 75/25 statics to video | IM8 | 09 | Founder |
| 100 to 300 new ads a month at $250k+ | Meta | 01p2 | Agency |
| Production budget: founder-led, then 25% of media, then ~10% of media (~2.5% of revenue) | Spend tiers | 01p2 | Agency |
| Test campaign $10 to 50 a day; 1 to 3 creatives every few days; ~$300 to validate; ~2 weeks for a $150 product; ~$2,000 to a validated store | Zero to one | 06 | Single, course seller |
| Doubling $50 to $100 to $200 a day; breaks at 6 figures | Small scale | 06 | Single; conflicts with 20% steps |
| Budget steps ~20% a day (Meta), ~20% increments (Google) | Winners | 01p1, 01p2 | Agency |
| Test budget CPA x 3 (0 to 1 conversions cut, 2 extend, 3 to 4+ keep) or x 5 | New concept | 01p1 | Agency |
| Test window ~1 week; 3 to 4 days large and fast; 10 to 14 days small and slow | New concept | 01p1 | Agency |
| 70/30 winners to tests; 90/10 or 100/0 when struggling | Meta budget | 08 | Single, agency seller |
| Scaling campaign worth it from ~$400 a day plateaued; not at ~$60 | Meta | 01p1 | Agency |
| Meta page ad cap ~300 to 500 | Volume advertisers | 01p1 | Agency `[verify UI]` |
| CPM $10 to 15 pre-2020 vs $35 to 45 now | Meta | 08 | Single |
| Meta CPM inflation ~20 to 30% a year | One agency's book | 01p1 | Agency, no card |
| 300 screen: CR% x AOV at ~$3 CPC | Paid scalability | 11 | Single, agency seller |
| Welcome discount 10 to 20% big lift; 20 to 30% none | True Classic | 05 | Founder |
| GWP ladder $100 / $150 / $200; AOV $36 to $112 | True Classic | 05 | Founder |
| Hero gating threshold 30 to 40% above AOV; $65 to $100 | One apparel client | 11 | Single, agency seller |
| IM8 ladder $112 / $89 / $235; AOV to $280; 50%+ take (09); quarterly 40% take, AOV $142 to $212, quarterly $321 (16) | IM8 | 09, 16 | Founder and Disclosed, differ |
| Post-purchase upsell 5 to 15% of net profit when staffed; RPV 10 to 15% | Upsells | 05, 01p1 | Founder; Agency |
| Subscription churn 24% to 17%, goal under 5%; peaks day 1, ~28, ~31 to 45 | Breeze | 08 | Founder |
| November cohort 6-month repeat 38.5% vs 63% Feb; 2 of 10 no gap | 10-brand sample | 15 | Agency |
| 1-day vs 30-day click gap ~40% normal, ~80% November | One agency's accounts | 15 | Agency |
| Post-treatment lift 105% (3+ weeks pre-BF); 41% of value after window; fashion 93% vs CPG 30% | House report | 15 | Single, secondhand |
| Preseason share 31 to 43% of Sep to Dec budget | Portfolio | 15 | Agency |
| CPM +25 to 30% from ~Nov 12; Triple Whale +50% Meta, +10% Google; agency 7.8% Meta | Different methods | 15 | Agency and secondhand, not comparable |
| Frequency 1.75 baseline, 1.96 peak, 1.82 Q5 | Large brands | 15 | Agency |
| Marginal CAC example: avg $337 to $392 (under $400), marginal ~$1,000 | Illustration | 15 | Hypo |
| 3-day rolling CM3 rule; spend peaks 5 to 7am, revenue 7 to 11am | Peak pacing | 15 | Agency |
| Per-ad ceiling: evergreen $4 to 8.5k a day, realistic $8 to 13k (AUD) | Agency accounts | 15 | Agency |
| Pareto at BF: top 1 ad ~7%, top 10 ~33%, bottom 80% ~54%; under $250k top 20% hold 53% | Portfolio | 15 | Agency |
| Format mix: offer statics ~19%, offer-overlaid evergreen ~18%; evergreen 50 to 60% of BF spend | Portfolio | 15 | Agency |
| Q5 ~Dec 16 to 31 cheapest media | Calendar | 15 | Agency |
| BF plus 2 months ~80% of annual profit | Oodie | 13 | Founder |
| Lever lag 60 to 180 days | Cash levers | 22 | Hypo |
| Fixed opex cut hits cash 1:1 | Fixed cost | 22 | Hypo (accounting logic) |
| Returning customers 80 to 90% of net profit | Assertion | 22 | Hypo, unsupported |
| CCC = DIO + DSO minus DPO | Any inventory brand | 01p1 | Standard formula |
| Inventory financing spiral $2M to $7M revenue, profit to zero, "5 times" | Anecdote | 01p1 | Agency |
| Opex creep failure band ~$50 to 300k a month | SMB clients | 19 | Agency |
| Payroll ~7% of revenue; "10 or less" to win | Ridge | 04 | Founder |
| ~60 employees at $200M+ (~$3M per employee) | True Classic | 05 | Founder |
| Supplier terms 15 to 30 to 45 to 60 to 90+ days; $1M to $5M to $25M revolver; $40M inventory buy year 2 | True Classic | 05 | Founder |
| LBO leverage 2 to 3x conservative, 6 to 7x pre-2022; $100M = $50M equity + $50M debt | PE | 04 | Founder |
| PE wants 15 to 20% EBITDA, ~20% growth; 30 to 40% margins invite add-backs | Sale prep | 04 | Founder |
| Sale ~10 months; sub-$5M at 1 to 3x EBITDA; 8 to 10 buyers; 45-day secondary diligence; ~15 PE bidders; PE buys 50 to 70% | Deals | 04, 07, 12 | Founder |
| Exit multiples: dropship 1 to 2x EBITDA; non-sub 3 to 6x; subscription higher; outlier 3 to 5x revenue or ~30x EBITDA; agency 3 to 5x, his 11x | Heuristics | 13 | Founder `[web check]` |
| Ecommerce exit timeline 5 to 7 years, up to ~9 | General | 13 | Founder |
| Non-compete 5 years (2 to 6 standard) | RXBAR | 07 | Founder |
| International triggers: UK ~$15M, Canada ~$20M, EU warehouses ~$50M | Small items | 04 | Founder |
| $5M international revenue with $3M shipping; UK 0.5% vs US 2.5% vs 5 to 7% global checkout | Ridge | 04 | Founder `[web check]` |
| Retail leases $20 to 40k a month; 1,000 to 1,500 sq ft; break even in 4 walls | True Classic | 05 | Founder |
| Buyer changes ~every 2 years | Large retailers | 03 | Founder |
| Restock ~3 months; 40 support reps in a month; sustain $40 to 60M a month before $100M | Comfrt | 18 | Founder |
| First-order contribution margin ~$9 (2013) to ~-$29 (2022) | Unnamed "2022 report" | 19 | Agency, unsourced |
| Casper $423M ad spend, -$300 per mattress; SDC $8.9B IPO, liquidated in ~4 years | Named examples | 19 | Agency `[web check]` |
| "Because" 60% to 93 to 94%; unsolicited gift ~2x; mail 18% to 35%; retreat 17% to 50%; bystander 85% vs 31%; similar finder 70% vs 33%; uniform 42% to 92%; scarce cookies more desirable not tastier; exclusive supply news ~6x orders | Compliance psychology | 02 | Study, dated, non-ecommerce |
| Data integrity is the bottleneck in "80%" (title) vs "about 30%" (body) of audits | Same source | 14 | Agency, inconsistent; carry 30% |
| Free audit gate $5M+ (01, 14, 17) vs $10M+ (16, 19) | Agency offers | see | Agency, time-specific |

## 7. Where sources disagree

Each conflict: what each side says, when each is right, what the agent should do. None is averaged into a rule neither side stated.

**7.1 Zero-attribution influencer programs vs tracked codes and URLs.** Bloom runs a claimed 85%-of-spend creator program with no affiliate links or codes, judged on views, content volume, cost per thousand views and blended signals (branded search, new customers, Amazon and retail sell-through), and its founder admits the attribution is poor (03, 13). Ridge tracks every sponsorship with a unique code and a unique URL and judges on cumulative long-tail revenue, accepting code leakage to aggregator sites (04). Comfrt pays commission on whichever channel a creator's content converts on, which requires tracking (18). When each is right: zero attribution only works omnichannel with DTC under 5% of revenue and a huge creator bench, where a 7-day window would miss purchases at a retailer 2 weeks later (03's own condition). Tracked codes are right for any DTC-heavy or code-dependent store, which is most ecomOS brands. What the agent should do: default to codes plus URLs plus a post-purchase survey (05); treat blended signals as a supplement; only recommend a zero-attribution program when DTC share is small and the brand can defend the spend from retail sell-through data `[needs brand data: DTC share of revenue]`. [ac7a5c24d798] [6a3c3dd9f14f] [175066c0600e] [b22aead0c4cf]

**7.2 Branded search cut to about 1% vs protected.** Ridge's own geo holdouts showed branded search and Google Shopping barely moved total revenue, so it caps branded search near 1% of marketing spend (04). The same-agency sources say to minimize brand spend where it is not incremental and to separate brand from non-brand reporting (14), and PMax without brand exclusions is largely retargeting (01p2). The common practice, and the situation of a low-awareness brand, is to protect branded search because it captures real demand a competitor could otherwise buy. When each is right: the cut is right for a brand with strong organic awareness whose holdout confirms it; protection is right when branded volume is small, competitors bid on the name, or no holdout exists. What the agent should do: never cut on the attributed ROAS argument alone; recommend a holdout on branded search first; until then, exclude brand from PMax and report brand separately (12-GAD). [1f911edec6bb] [606c03936b6f] [2b7d05cb2e3f]

**7.3 Double the budget vs step it up.** The zero-to-one framework doubles daily budget $50 to $100 to $200 while returns hold, and its own source says this breaks at 6-figure spend (06). The agency sources raise budgets in about 20% steps on Meta and about 20% increments on Google to avoid resetting learning (01p1, 01p2). The coaching-era "just bump your budget" advice worked for timid small brands in 2020 to 2022 and is called unreliable now (20). When each is right: doubling is tolerable at $10 to 200 a day where the absolute dollars are small and the read is a demand test; stepping is right at any scale where learning phases and profit matter. What the agent should do: recommend 20% steps by default; allow doubling only inside a small validation test and only while the return ratio holds at each step; `[verify UI: Meta's current learning-phase and budget-change guidance]`. [13f04667] [5de48d3e386a] [7ea79f0c239]

**7.4 Organic first vs paid from day 1 (the Comfrt contradiction).** Paid ads "never worked" for Purely White, which grew for years on organic Snapchat and TikTok creators to 300M+ views a month; paid worked at a claimed 4 to 5x early for Comfrt once organic proof and creator supply existed; the founder does not resolve why beyond category and messaging (18). Ridge would build an audience before a product if starting over and gets 70% of its best paid ads from organic winners (04). The zero-to-one framework posts about 50 organic pieces before a $10 to 50 a day paid test (06). IM8 and Breeze scaled paid from the start with creative volume (09, 08), and Fogerty's early wins were "the best possible at Facebook ads" (13). Bloom avoids Meta dependence altogether (03, 13). When each is right: organic first when the product is inherently shareable, the founder has time not money, and the category needs education; paid from day 1 when demand is proven, creative can be produced at volume, and unit economics are known. What the agent should do: run the cheap gates in order (list, organic outlier, small paid test, C1) and let the brand's own signals pick the sequence; do not present either as a law. [a84d20a1386a] [1c0184cbc727] [954f15424bc2] [f763727b] [09fbaaa5df5f] [5630f92d6cff]

**7.5 Few elite generalists vs redundancy.** True Classic runs about 60 people at $200M+ and credits elite generalists for never raising primary capital; the source does not address succession or key-person risk (05). Salt and Stone stays deliberately understaffed and remote (12). Ridge cut headcount from about 75 while growing (04). Against this: Comfrt's founder was told the business would fail without a COO and CFO (18); IM8 caps decision loops at 5 to 8 (09); the Blue Sense sources call people the highest-leverage line once a brand can hire well (01p1); 06 expects director-level burnout and plans hiring around it. When each is right: lean generalists are right while the founder can still see every function and the brand is below the point where one absence stops sales; redundancy is right once any single person's absence would stop orders shipping, ads running or cash being collected. What the agent should do: keep headcount growth below revenue growth (04), but require a named backup for each of ads, fulfilment, finance and customer service, and treat "elite hires push back when surrounded by weaker colleagues" (05) as a retention risk to manage. [d84592054461] [1cd6bcabe32b] [071715bc72c9] [b5802ce3e875] [9840c923e170]

**7.6 Attribution vs intuition at scale.** Rahal: "you don't need attribution, it's an intuition-type thing," with about 60% of spend on brand at "teenage" scale and mostly brand at maturity (07). Salt and Stone approves billboards on team conviction once liquidity allows (12). Bloom accepts correlational measurement (03). Against this: the agency sources build a measurement layer that gets more rigorous with scale, up to geo-lift at $20M+ (14, 01p1); Ridge spends about 1% of marketing on measurement and runs holdouts (04); 10 reframes intuition as 10,000 to 20,000 hours of test history. When each is right: intuition is a mature, well-capitalized, second-time founder's preference and fits worst for an early or resource-constrained brand (07's own caveat); rigorous measurement is right whenever the decision is large, the channels are many, or the operator lacks the test history. What the agent should do: match the measurement tier to the decision size (A24); allow an unmeasured brand line only once the brand is past the performance ceiling (about $1M to 20M per 01p1) and has cash to lose; never fund an unmeasurable channel on intuition alone at an early stage. [5a9b4680ac1d] [dedcbb054c21] [9440e57d0b39] [455d2f7749e9] [c2b721c34563]

**7.7 Hero SKU gating vs bundles.** One agency owner pulled a hero hat (about 40% of revenue) from direct sale and made it a free gift above a threshold 30 to 40% over AOV, reporting AOV from about $65 to $100 "overnight" (11, one case, no downside data). The Blue Sense offer module prefers bundles, GWP at true gift cost, thresholds set from the AOV distribution, and product repositioning, all of which keep the hero on sale (01p1). True Classic uses a GWP ladder and packs (05). Alo keeps its cheapest SKU out of paid entirely (17). When each is right: gating is a high-risk move for a brand whose hero is genuinely coveted and whose economics survive giving it away; bundles and thresholds are right for everyone else and for any consumable where a stockpile offer kills reorder (11's own warning). What the agent should do: default to bundles and thresholds from the AOV distribution (03-OFF); treat hero gating as a test with a written revert condition, never a default. [fd5777d14d59] [7555f8b740ac] [1a706c3de836] [fbf5c852d1d2] [9bf05e0dda65]

**7.8 Subscriptions with long payback funded by capital vs short payback.** IM8 tolerated a 6 to 8 month payback and a quarter with a heavily negative net margin, funded by a $1B facility that pays 70% of each cohort's marketing, and its founder states a sub-4-month gate at the same time (09, 16). Bloom's ritual products retain with routine-havers (03). Against this: ecommerce should target near-breakeven on the first purchase because consumers rarely buy twice (19); a $6 to 7M brand with investors or creditors is a risk profile the same presenter refuses (19); the teardown itself says "do not copy IM8's payback window" (16). When each is right: a long payback is defensible only with non-dilutive or patient capital, a proven cohort curve that reaches the horizon, and a public or investor-facing structure that can carry the loss; short payback is right for everyone else. What the agent should do: gate spend on the brand's own payback and LTGP:CAC (A9, A10); if the founder wants to fund a longer payback, route to 4.8 and require the funding source, the cohort evidence and the stop condition in writing. [179c5947001a] [9cb4c7dc31a1] [577a55dfd0ec] [ceffceaa4132] [d222f5b460d3]

**7.9 Always-urgency CRO reflex vs Cialdini's conditions.** Common CRO advice adds urgency and proof to every page. Cialdini: scarcity works when newly scarce and demand-caused, raises desire not quality, and the arousal it produces degrades decision quality; social proof helps under uncertainty and similarity and can read as desperate on a confident buyer; stacked conflicting cues reduce credibility; recognized tactics stop working (02). Alo runs zero discount, price or risk-reversal language in ads and still sells out, and can use scarcity because it actually sells out (17). Black Friday deadline creative is a real deadline (15). When each is right: urgency and proof are right on the ambiguous steps for cold, uncertain traffic when the claim is true; they are wrong on high-intent branded traffic, on a premium position, and whenever the claim is not backed by a real constraint. What the agent should do: apply E4 and E7 as gates before 09-CRO tests any urgency or proof element; ban resetting countdowns, seller-typed counts and staged rivals outright; test the honest version against no urgency, since the source predicts it can lose on confident buyers. [743b6f53913c] [c0a38656da11] [ecc4097514cf] [7999f7f71668] [3a1292e93ad7]

**7.10 80/20 creative concentration vs spread at Black Friday.** The Blue Sense Meta module says CBO concentrates spend by Pareto, with about 4% of ads holding about 64% of spend and revenue (01p2). The same agency's Black Friday data says Pareto does not hold in the peak: the top 20% of ads held 53% of spend in accounts under $250k of November spend and progressively less in larger ones, and the bottom 80% held about 54% overall (15). When each is right: concentration describes an evergreen scaling campaign in a normal period; spread describes the peak window, when offer and discount drive most of the variance and volume across the tail carries the account. What the agent should do: plan creative volume for the tail at the peak (F7) and let winners concentrate the rest of the year; use ABO or CBO with caps to control concentration by period (01p2's seasonal switching). [345054044d8c] [291583358578] [9190a63c0c09]

**7.11 The "80%" vs "30%" audit claim.** Source 14's title says data integrity is the bottleneck in 80% of audits; its transcript says "about 30%". Neither has a shown method. What the agent should do: carry 30% as what the presenter states on camera, flag 80% as an unsupported headline, and treat the true share as unknown `[web check: any published methodology]`. [4f1e89e8a798]

**7.12 Retention from day one vs a retention phase after year one.** 10 builds the backend from day one with 30, 60 or 90 day replenishment for consumables; 11 requires welcome and abandoned-cart flows before any paid scale; 09 spent 9 to 12 months on acquisition only and then made the offer structure the first retention move; 19 says retention tactics cannot move a category-bound LTGP for the roughly 80% of brands with weak repeat; 20 says retention is downstream of product and flows cannot create it. When each is right: flows and a subscription option from day one cost little and are right for any consumable; a dedicated retention program is right once acquisition is proven and the category band supports it. What the agent should do: require the cheap infrastructure (flows, a subscription option, cohort tracking) from C1; schedule the deliberate retention phase for C3; set expectations by category band. [3d5541e52ed0] [36f24e817a8e] [7d3b5a19ab1e] [376c8c477e8f] [0005f05fcb3]

**7.13 Founder on camera vs an expert or hired face.** 03, 05, 08 and 11 build founder content as distribution and recruiting; 06 calls "it must be the founder" a fallacy, prefers a niche expert or a credible hired face, and warns founder-led content becomes a liability as a brand grows; 08 notes stopping public building reverses the CAC benefit. What the agent should do: test the founder against an expert on the brand's own traffic; never make the brand depend on one face (G12). [9084311] [56b30c64] [a901d93b0685] [fcb510de5279]

**7.14 Standalone flagship stores vs mall foot traffic.** Common retail advice favors a controlled flagship; True Classic's standalone stores lost money even in prime locations while high-traffic malls broke even or profited (05). What the agent should do: treat it as this brand's result; require a foot-traffic model and a break-even-in-four-walls test before any store, and prefer a retail-as-a-service test first (18-COG). [4bdfa7fa6c39] [5115e27797b5]

**7.15 Founder presence in buyer meetings.** Salt and Stone's founder would avoid buyer meetings when the goal is a clean exit, so the buyer does not price "the magic" into a retained stake; standard M&A guidance says founder engagement builds confidence (12). What the agent should do: set the strategy from the stated exit intent, and require deal advisory review (G11). [629185c92369] [b0c7c3317789]

**7.16 Angle before offer vs offer is king.** The Blue Sense creative module ranks the fix order as angle, then offer, then persona, then format, and names its disagreement with the "offer is king" framing (01p2); 08 and 01p1's offer module treat the offer as the primary lever as CPMs rise. What the agent should do: for an underperforming ad, work the angle first (10-MCR); for an underperforming business, work the offer first (03-OFF); these are different diagnoses, not one rule. [bc784b37d696] [916278acd788] [f5e39801f58b]

**7.17 LTGP:CAC above 3 is "bad" vs the cash-flow exception.** 14 states the cash-constrained exception; 19 omits it and says "ramp harder". What the agent should do: keep the exception; a brand that cannot fund the inventory a faster ramp needs is right to sit above 3 (A8, A12). [777732c1773f] [e0b1085f47a3]

**7.18 Rotate creative fast vs hold winners.** Alo turns its account over about every 3 weeks with a 24-day maximum ad age; the teardown's agency lets winners run with quick replenishment and concentrates on a hero SKU for market entry, and calls the two situational (17). What the agent should do: the account's job decides: a harvest-only distribution account can rotate; an account that must find new customers holds winners (24-DEP). [31cd05ed427e] [cdc15b2f036c] [c38bcfd6b16e]

**7.19 Retail exclusivity: mostly wide vs deliberate use.** Bloom defaults to wide availability and admits using exclusivity and FOMO deliberately at times (03); Salt and Stone refused a Sephora exclusive (12); Bloom's beverage launched as a Target exclusive (03). What the agent should do: default wide; use an exclusive only as a launch tactic with a planned end and a plan for other retailers' reaction. [7880f75d131f] [65240921911c]

**7.20 Bloom avoids Meta dependence vs Fogerty's Meta-first wins.** Two founders in one file (13) with opposite channel strategies for different eras and products. What the agent should do: two conditional approaches (D2, D6); pick by creator supply, product shareability and measurement needs, not by which founder is louder. [5630f92d6cff] [8b75ede22872]

## 8. Common mistakes

Merged from all sources, deduplicated, with the fix. Domain-specific mistakes (ad-set settings, feed hygiene, email cadence) stay in the owner folders.

1. Comparing ROAS across campaigns, platforms or funnel stages as if equal numbers meant equal value. Fix: compare profit contribution; strip view-through, existing customers and halo; never move budget up the funnel on a retargeting ROAS (01p1, 14, 20). [4ba4c1567d4d] [7c355072e26e] [53cff4b8747]
2. Reporting product margin as gross margin, or a flat "average margin" during a discount. Fix: A4, A5 (01p1, 04, 07, 14). [7d67a42b0d81] [b1834ecfb2a1]
3. Judging CAC alone, or with blended AOV inflated by returning customers. Fix: A6 (01p1, 16). [82a77847f675] [c52a5730e858]
4. Scaling on blended MER or a healthy ROAS while AMER or topline is flat. Fix: A3, B14 (14, 20). [3c73946c2bb4] [9497f75a4f1]
5. Diagnosing a profit decline as traffic, creative or seasonality before reading CAC and LTGP. Fix: B3 (19). [6da370548f56]
6. Raising spend to hold revenue when CAC is rising. Fix: 4.10 (19). [6da370548f56]
7. Raising capital or debt against a structurally bad ratio, or treating "cash-flow positive" as profit. Fix: A19, A22, G2 (19, 16). [ceffceaa4132] [9cb4c7dc31a1]
8. Reading net income as cash, and promising a growth rate without modelling the inventory cash it needs. Fix: A12 (01p1, 22, 05). [731ac683ccf3] [8105508e9] [1dcdad671ee9]
9. Reflexively cutting marketing when cash is tight from unsold inventory. Fix: A15 (01p1). [2ba72747cc86]
10. Judging a lever change inside 30 days. Fix: A14 (22). [32440a917]
11. Treating a marketing cut as equivalent to a fixed opex cut for cash. Fix: A13 (22). [71b3d1891]
12. Letting opex grow under a "reinvest" narrative, or leaving fixed cost sized for a past peak. Fix: A21 (01p1, 19, 22). [9840c923e170] [7b24b5654a81]
13. Adding attribution tools, dashboards and conversion events to fix confusing metrics. Fix: subtract to a hierarchy, A24 (01p1, 14). [7500786dbfd9] [2d775e75662d]
14. Trusting first-click or multi-touch tools to redirect budget into brand search. Fix: A24, 7.2 (14). [5de99742a3a0]
15. Crediting a channel launched into a seasonal peak with the peak's lift. Fix: F13 (14, 15). [33775b73749d]
16. Crediting an inside-account tweak for a recovery that was fluctuation or an outside lever. Fix: B12 (17). [ea0fb51b4d36]
17. Copying a large brand's harvest-only ad strategy without its outside demand engine. Fix: B7, H2 (17). [ec5bd4781c52]
18. Copying a financed brand's payback window or negative margin. Fix: 7.8 (16). [179c5947001a]
19. Copying a fast case (a trending product, an uncrowded auction, a celebrity network) as a formula. Fix: A25, H7 (13, 09, 04). [b7325aad598c] [3ae237242a99]
20. Stacking an unproven product on unproven creative and unproven media buying. Fix: C1 (10). [1d7f15eafafc]
21. Launching at a premium price with no reviews or track record, then defending the number. Fix: B8 (18). [11347fa2b0f9]
22. Trying to rescue a flopped launch with better marketing. Fix: E9 (04). [db8e8f54f571]
23. Pivoting a product or audience before real effort and a multi-demographic test. Fix: B8 (11). [8bbceb08f413]
24. Rebuilding a landing page before testing which angle wins. Fix: B5 (11). [6b9ad04ab9c3]
25. Treating creative volume as the fix when the underlying creative is not good, or reading a large ad count as quality. Fix: B9 (01p2, 09, 06). [a9d4d1b724a5] [3c104e877904] [396a23d8]
26. Diagnosing an angle's plateau as a bid or creative failure instead of a TAM ceiling. Fix: B10 (21). [b2da5bc185dd]
27. Not separating new and existing customer spend, and hammering existing customers or an unconverted organic following. Fix: B14 (20, 14). [722e2752eec7] [b2092d04659e]
28. Setting existing-customer spend as a percent of budget. Fix: D5 procedure step 7 (01p2). [421e7aee0498]
29. Adding a channel before naming the primary channel's headroom, or funding it by reallocation. Fix: D3 (09). [0805d0da06ef]
30. Ignoring channel overlap and platform concentration risk. Fix: D9, D10 (04, 09, 03). [89eb781b3bd2] [492ad9d02ac5]
31. Judging sponsorships by raw audience size, or paying a premium for fame that tested irrelevant. Fix: D5 (06, 04). [054d2570] [8fa3a6c48b7b]
32. Cutting pre-sale spend on a lagged ROAS read; turning off evergreen for the sale; judging peak creative on ROAS; reading the day at 8am. Fix: F1, F8, F5 (15). [a0478e430dad] [7c0dc6951b2c] [88407c078150] [3b63d06d5486]
33. Assuming a few winners will carry a Black Friday account, or that 12 to 18 ads that exist can hold spend. Fix: F7 (15). [291583358578] [075f80613bc3]
34. Ignoring November cohort quality and discount compression when setting the November CAC allowance. Fix: F4 (15). [d661eb7e3ac0]
35. Running a peak with unsigned 3PL or 4PL paperwork, no inventory buffer and no support plan. Fix: F11 (13, 18). [ac76fdafcc3e] [ccdffe1f5d76]
36. Manufacturing scarcity, proof, authority or concessions. Fix: 3.E; banned under ecomOS rules (02, 13, 17). [743b6f53913c] [b7d4878acc8a] [3a1292e93ad7]
37. Stacking conflicting persuasion cues on one step, or applying them before baseline mechanics work. Fix: E1, E10 (02). [95287da743ad] [d771afe27917]
38. Bidding past a pre-committed ceiling in a competitive auction (ads, inventory, sponsorship). Fix: E9 (02). [80d1a965dcd8]
39. Assuming "own your list" replaces paid acquisition, or that "50% of revenue from email" is a benchmark. Fix: D6, 7.12 (19, 20). [9f8e357bd0b2] [0c79d63f1e16]
40. Redoing email flows to fix a retention problem rooted in product, pricing or experience. Fix: A18 (20). [0005f05fcb3]
41. Reading Klaviyo attributed revenue, daily returning revenue or a "% new customers" tile as retention. Fix: cohort analysis (19, 20). [676a17d4a712]
42. Entering mass retail before proving sell-through, or missing a retailer PO. Fix: D7 (07, 03). [05f735247a96] [1bc6acca39d7]
43. Flipping international shipping on with no localization or landed-cost check. Fix: C4 (05, 04). [1bf2b0cb1bac] [406f95cc2038]
44. Trusting an unvetted single-source manufacturer or supplier. Fix: G4 (12, 07). [f6567143a45c] [248161a47836]
45. Taking on leverage without modelling the downturn, assuming a "second bite" will pay, or hiding weaknesses from a buyer. Fix: G2, G8 (04, 07). [edf06536c8b7] [20817201b1bb] [58e0fc375c4c]
46. Hiring a CEO who is the founder's mirror opposite; hiring for 12 to 24 month potential in hyper-growth; hiring on a prestigious employer's name. Fix: G12, 21-OPS (13, 05, 03). [116713e4f02a] [d281ce11c9df] [3dee9502ba57]
47. Letting a treasury bet or a personal-brand program distract from the core, or concentrate key-person risk. Fix: G14, G12 (09, 08). [fd68d33918f8] [fcb510de5279]
48. Treating any founder's public number, a title's headline, or an agency's portfolio average as a benchmark for this brand. Fix: I2, section 12 (all). [12509c82d440] [391c879b2d86]

## 9. Deliverables

**9.1 Growth model sheet spec.** A monthly workbook (or data-layer view) with these tabs, all computed in code: (a) P&L waterfall with each line in dollars and % of net revenue, new and returning columns; (b) acquisition: spend by channel, new customers, CAC, first-purchase GP, GP:CAC, AMER, MER; (c) cohorts: cumulative GP per customer by acquisition month at day 30, 90, 180, 365, LTGP:CAC in the category window, payback months, with modelled horizons flagged; (d) cash: the 22 line order, CCC, ending cash, the 6 levers as named inputs; (e) forecast: returning revenue from cohort curves, new revenue from the AMER regression, each with its own error band; (f) dashboard: new-customer profit contribution, AMER, new-customer revenue and orders, CAC, LTGP:CAC, payback, ending cash. Every cell that depends on a missing input shows "unavailable". Source of each formula cited by card id in a notes tab (4.1).

**9.2 Bottleneck diagnosis memo.** One page: data-integrity findings and fixes made first; the CAC and LTGP series read; archetype; the 3-layer read with numbers; the single binding constraint and its evidence; the lever and its owner folder; the expected lag; the test that confirms it; the rollback; the discipline sentence. Appendix: the queries used (4.3).

**9.3 Stage plan.** The brand's stage with both bands; a table of stage requirements (measurement, creative, structure, pacing, channels, team, brand line, retention phase) marked present or missing; the priority list to close the gaps with owner folders; the next boundary and what it will require; dated for the next quarterly review (4.4).

**9.4 Channel mix plan.** Current spend and new-customer revenue by channel; incremental read per channel with its reliability tier; inflators stripped; harvest vs growth classification; overlap tests recommended; the next-dollar allocation with a confirmation window and revert condition; cut candidates with their confirming test; concentration risks; existing-customer budget in dollars; the owned-calendar coordination (4.5).

**9.5 Peak season plan.** Objective and CAC tolerance; the 3 corrections with the corrected November allowance; base and stretch budgets with numeric gates; front-load schedule; creative volume that can hold spend, tail buffer, format mix and 4 phases; offer ladder with triggers and pre-built pages; pacing sheet spec with hourly multipliers and the written scaling rule; Google prep list; evergreen do-not-pause list; operations checklist (paperwork, buffer, support, page limits); Q5 offer; post-peak measurement plan (4.6).

**9.6 Teardown report format.** Header: brand, date of scrape, data sources by reliability, the ecomOS signals-only line. Sections: business context and P&L read (with every estimate labelled); demand verdict (awareness mix, celebrity share, creating vs harvesting); creative (format map, script scores, voiceover share, ad age); destinations; offer and price discipline; consistency audit; dependency audit; transferable vs not; hypotheses routed to owner folders. No competitor copy, product shots, faces or page text reproduced (4.7).

**9.7 Founder decision memo.** Decision and objective; options in order of dilution with the mechanics; the numbers (leverage, EBITDA before add-backs, multiples with source and check status, timelines); the process design; term traps; founder-meeting strategy; key-person and key-channel risk after; the downside case per option; the time-travel question; what the agent cannot know; the legal, tax and deal advice line (4.8).

**9.8 Routing list to domain folders.** For each finding the agent used from this folder that belongs to a domain, a line: finding, source number, card ids, owner folder, the overlay it should land in. Section 1.3 is the master list; each deliverable above appends the lines it touched.

## 10. What needs live data or a web check

### 10.1 `[needs brand data]`, grouped

**Unit economics and cash (4.1, 4.2, 4.9, 4.10)**
- Net revenue, refunds, discounts and shipping allowances by month; new vs returning order tags with counts.
- Per-SKU COGS, freight in, shipping out, pick and pack, transaction fee %, refund allowance; landed cost per international order by destination.
- Ad spend by channel including creator fees, affiliate commission, sampling and agency fees; measurement tooling spend.
- New customers per month from order data; cohort gross profit at day 30, 90, 180, 365 by acquisition month; oldest cohort age.
- Inventory on hand and on order by SKU and grade; 30-day sell-through per SKU; supplier terms and lead times; maintained markup.
- Opex by line, fixed vs variable, with hire dates; cash balance; debt, covenants and interest.
- The brand's own marketing-to-revenue ratio, CPC and CPM history by niche (to recompute the 300 screen and the payback gate).
- Trailing 12-month revenue and current monthly spend (stage placement).

**Bottleneck and channel (4.3, 4.5)**
- Existing-customer ad frequency over 30 days and share of spend on existing customers; returning share of "cold" conversions.
- Conversions per active campaign; active campaign count; brand vs non-brand spend split.
- New creatives per month and the brand's own spend-per-creative history; frequency and spend by angle.
- Funnel step-through rates (landing view, add to cart, checkout, purchase) and category-typical rates.
- Any lift, holdout or CausalImpact reads; channel share of spend, revenue, retailers and creators for concentration.
- Post-purchase survey channel shares vs spend shares.
- Upcoming email drops, launches and promotions.
- DTC share of revenue (decides 7.1).

**Peak season (4.6)**
- Prior-year hourly revenue and spend curves; prior-year data in 1-day and 7-day or 30-day click windows; 6-month repeat by acquisition month for 2 prior years; gross margin by SKU and planned discount depth; production capacity and page headroom; 3PL and 4PL paperwork status; support capacity; restock lead time.

**Founder decisions (4.8)**
- Cap table and ownership; current debt terms; personal and company objectives; exit intent; operator experience; current leadership and named backups.

**Teardown (4.7)**
- The brand's own numbers for comparison only; the competitor's public scrape and pages stay in the inspiration layer, separate from private data.

**Persuasion constraints (3.E)**
- Real stock levels and end dates behind any scarcity claim; real order and platform data behind any proof count; the actual expert or credential behind any authority cue.

### 10.2 `[web check]` and `[verify UI]`, grouped

**Platform mechanics (Meta, Google, TikTok, Klaviyo)**
- Meta's current default attribution windows and the 7-day-click definition change dated by 14 and 01p1 to about March or April 2026; the "1-day engaged" bucket.
- How Meta's "incremental attribution" column is computed (industry factor vs live holdout), dated to about November 2025.
- Meta's per-Page active-ad cap (about 300 to 500 per 01p1); partnership ads and whitelisting rules and disclosure; "flexible ads" name; Advantage+ creative settings; experiments and conversion-lift tooling; Creative Similarity Score access.
- The "Andromeda" name for Meta's ranking engine (01p1, 01p2, 04, 10) and whether visually similar creative is treated as duplicate.
- TikTok and Google in-platform lift-test minimum spend (about $200k per 14).
- Google: PMax feed-only mode, brand exclusion methods, portfolio bidding and "SA3" (likely Search Ads 360), Smart Bidding Exploration, GMC image ratio (4:5 per 01p2), Merchant Center promotion feeds, Gmail click counting, DSA deprecation.
- Klaviyo default attribution (5-day open, 5-day click per 20).
- TikTok Shop affiliate tooling, payout rules and current economics (03, 11, 18); Instagram Shop creator posting.
- Current geo-lift feasibility and region granularity for Australia (14).

**Case figures 2025 to 2026, all self-reported unless noted**
- IM8 and Prenetics: run rate, market cap, the $44M raise, the $1B facility terms, FY26 guidance, the Lemonade comparison (09, 16; some checkable in filings).
- Bloom: $180M bootstrapped, $500M pace, the Nutrabolt deal year (2022 vs 2023) and terms, 50,000 doors, 15B views (03, 13).
- Ridge: revenue, the $300M offer, the MKBHD deal terms, Dude Wipes, Stanley and Baseball Lifestyle trajectories (04).
- True Classic: $200M+ ARR, $850M vs $950M valuation, 60 employees, $40M inventory buy (05).
- David Protein: $725M Series A, RXBAR $600M sale, week-one sales (07).
- Salt and Stone: $165M+, Humble Growth and Advent terms, the $500M+ exit rumor (12).
- Comfrt: the "$500M in 3 years" title claim, $43M month, $100M in 2 months (18).
- Oodie and Calming Blankets revenue, the $130M failed deal, the 11x agency sale (13).
- Gruns: "$0 to $500M in 2 years", 660 live ads (21).
- Alo: revenue and valuation estimates, store count, the January 2026 CEO hire (17).
- Casper's ad spend and unit loss; Smile Direct Club's IPO and liquidation; the unnamed "2022 report" on first-order contribution margin (19).
- The Triple Whale 2025 Black Friday report, the House incrementality figures, the Motion finding (15).
- Australian cash rate and inflation figures; the target market's equivalents (15).

**Tool and vendor names (many possibly mis-transcribed)**
- Northbeam, Triple Whale, Haus (also "House"), Iris, Measured, Foreplay, Motion, Refunnel, Social Snowball, Superfiliate, pics.io, Shopify Markets Pro (renamed), ShipMonk, ShipBob, SeKO, Flexport, Brand Access and Passport (04); KnoCommerce ("No Commerce"), Intelligems, Gorgias, Zowie, Kudos, Maverick, Fondue, Wayflyer, Leap, AfterSell, FedEx Crossborder (05); Outer Signal, One Sec, an internal video tool (06); Nostra, customers.ai, heatmap.com, Replo, Stored, clipping marketplaces (08); Higgsfield, "Nano Banana", OpenSend, ClickUp, Remotely X (11); Trend Rocket, Exploding Topics, "Mania" (13); Hyros ("High roast"), Wicked Reports, "We track" (10); CausalImpact's current name and maintainer (01p1, 14); Reshop, Alo Access, Alo Wellness Club (17); Day Job agency, UNFI, KeHE (07); Raymond James, Humble Growth, Advent (12).

**People and sources named**
- Blue Sense Digital's identity, presenters and domain (01, 14, 15, 17, 19); Eddie's full name and the "$1B" claim (11); "Mark" and Brand Builder Academy (10); "Orin" and cut 30, and the "Claude" or "Cloud" enterprise case (06); "Chris Haddad" and "Peter Kell" (10); "Paul Wy" (20); "Jordan Manard" (11); Nick Shackelford's current roles (08); the podcast hosts of 07, 09, 12.

**Legal and compliance**
- Identity-resolution and email-append legality by jurisdiction (11); subscription commitment and cancellation rules (08); monthly-equivalent display of a longer commitment (16); sweepstakes rules for golden-ticket promotions (09); calorie and nutrition claim substantiation (07); GLP-1 adjacent claims for supplements (21, 01p1); AI-content and sponsored-content disclosure (06, 09, 03); MFN clause enforceability (07); paid insider introductions to manufacturers (12); trademark class checks (07).

## 11. Freshness and stale-risk notes

| Area | Why it goes stale | Re-verify |
|---|---|---|
| Meta attribution defaults, 7-day-click definition, incremental attribution, page caps, partnership ads, Advantage+ settings, learning-phase budget rules | 01p1 and 14 pin changes to March, April and November 2025 to 2026; 01p2 flags the second-ad-account tactic, trial reels ("as of April 2026") and the partnership-ads window as time-sensitive | Before every use; at least monthly |
| Google PMax, Shopping, bidding, GMC feed specs | Product renames and deprecations named in 01p2 | Before every use |
| TikTok Shop and creator-commission economics | 11 says the arbitrage shifts "every single month" | Monthly |
| CPM levels and macro (rates, inflation, ad inventory growth) | 15 is a 2025 to 2026 snapshot and expects each year to differ; 19 says CPMs rise every year | Each quarter and before any peak plan |
| All 2025 to 2026 case figures (IM8, Bloom, Ridge, True Classic, David, Salt and Stone, Comfrt, Oodie, Gruns, Alo) | Founder claims at a moment; several already restated within their own interviews | Before quoting any externally; treat as examples only |
| Exit multiples and PE leverage norms | 04 dates 6 to 7x to pre-2022; 13 says multiples move with timing | Before any founder memo |
| Tool and vendor names | Many are mis-transcribed and products rename or get acquired (Shopify's international product, Brand Access) | Before recommending any |
| Cialdini's study figures | 1990s edition; some studies debated since; no unity principle | The mechanisms hold; do not quote the figures as current ecommerce evidence |
| Source 19's era | Likely recorded around 2022; prefer 14 and 01p1 where they overlap | Already applied |
| The spend, revenue and stage bands in 3.C | Round numbers chosen by interviewers or agencies, not researched inflection points | Recalibrate to the brand's own ratio each stage review |
| Legal and compliance items in 10.2 | Rules differ by market and change | Before any deliverable that touches them |

## 12. Source index

Credibility scale: A = academic or disclosed data with stated method; B = operator's own data with a named vendor or public comparator, no pitch; C = founder self-report on a promotional interview; D = agency or course seller pitching the service being recommended; E = hypothetical or observational only. Bias notes name what each source sells.

| # | Title (short) | Type | Credibility and bias | Contributed most to |
|---|---|---|---|---|
| 01p1 | Scale an ecommerce brand profitably, part 1 (Blue Sense masterclass, May 2026) | Course transcript | D. Agency selling a free audit ($5M+; once "a month") and hiring. Self-reported 1,000+ audits, $150M spend. Internal: LTGP:CAC bands stated twice with different windows; frequency cap 8/7-day vs 7/30-day; a 25%-off example that does not reconcile; hiring domain spelled 3 ways. 2XU disclosed as a client. Several examples explicitly hypothetical. | A1 to A24 finance and measurement core; offers module (routed); Meta structure tiers (routed); C2, C3 |
| 01p2 | Same, part 2 | Course transcript | D, same voice. Flags its own time-sensitive tactics; walks back its own earlier PMax position. | Creative tiers and volume (B9, C5); Google root-cause method (B11); channel mix (D2); rotation rules |
| 02 | Influence (Cialdini) | Book, 1990s revised edition | A for mechanism, with selection bias and dated, sometimes debated studies; no commercial pitch; no ecommerce content, all mappings are the mini playbook author's. | 3.E in full; E9 team-side defences; 7.9 |
| 03 | How Bloom built the playbook (Greg Lavecchia, 2026) | Podcast | C. Founder promo; sponsor reads (Chargeflow, Whisper Flow, Ketone IQ) are not Bloom; no unit economics at all; deal year given as 2022 and 2023. Family with 13. | D2 exception, D5, D7, D9, G1, G5, retail rules (routed), 7.1, 7.19 |
| 04 | Ecommerce masterclass (Sean Frank, Ridge) | Podcast | B minus. Bootstrapped operator with Northbeam and Haus data; no course; sponsor reads not Ridge; every threshold is his own rule of thumb; internal tension "we're a marketing company" vs a celebrity equity brand play. | D1 to D3, D5, D10, D12, G1, G2, G6, G8, G10, G15, A24 tooling, A25, 7.2, 7.5 |
| 05 | True Classic (Ryan Bartlett) | Podcast | C. Founder promo; Google share 15 to 20% vs 20 to 25%, valuation $850M vs $950M in the same interview; the "wow budget" is the interviewer's program; no test methodology behind "tested" claims. | A12, A21, B13, C2 finance hire, C4 retail and international, D2, G1, G3, 7.5, 7.14 |
| 06 | Every level of marketing (Orin) | Podcast | D. Sells the cut 30 program; PE creative director; no data shown; levels are interviewer's round numbers; "Claude" vs "Cloud" case ambiguity. | 3.C level structure, C1, C4 awareness initiative, A24 chaos theory, 7.3, 7.13 |
| 07 | $725M in 255 days (Peter Rahal) | Podcast | C. Founder promo; sponsor reads; $600M sale and $725M valuation unverified in text; one card (f640724d4b4c) contains an ingredient error. Explicitly finds performance marketing "not interesting". | A4 launch margin, C4 brand vs performance, D7 regional retail, G1, G3, G4, G6, G8, G11, G13, 7.6 |
| 08 | The new way to run Meta ads 2025 (Nick Shackelford) | Podcast | D. Sells agency and ad-production services that supply the role he recommends; all figures are one brand's (Breeze). | A9 CAC from LTV, A16 CPM levels, B5 price read, C1 founder runs ads, D6, D11, D12, G12 building in public |
| 09 | $100M in under a year (Danny Young, IM8) | Podcast | C. Founder promo; public parent so some figures checkable; payback bands contradicted by the host; the host calls 95% Meta dangerous while praising 85%; prior exits, a public balance sheet and a Beckham introduction are not replicable. Family with 16. | A8, A10, B9, C6, D2, D3, D5 equity partners, D7 DTC-only, G1 investor numbers, G12, G13, G14, 7.8 |
| 10 | 8 years of marketing advice (Mark) | Video | D. Sells Brand Builder Academy; self-reported spend and revenue; named attributions possibly mis-transcribed; file contains unrelated classification scaffolding. | A16, A17, A18, B4, B15, C1, 7.12, 7.16 context; copy rules routed |
| 11 | $1B marketer (Eddie, BAD) | Podcast | D. Sells agency, course and a staffing firm he owns; "$1B" is the host's framing; duplicate card pairs; single-case numbers. | A9 12-month LTGP, A18, B5 angle test, B6 300 screen, B8, C1 flows, C3 plateau, 7.7 |
| 12 | 9-figure founder (Nema, Salt and Stone) | Podcast | C. Founder promo; $165M+ and two PE deals unverified; narrative not method; AI and copycat claims are opinion. | C3 hiring order, C4 brand spend, D7 one price and organic Amazon, G3, G4, G7, G11, G12, 7.15 |
| 13 | How Bloom built an empire (curator notes) + Oodie founder podcast (Dave Fogerty) | Bundled | C. Part 1 is paraphrase, not quotes; part 2 sells a course and Trend Rocket; two different brands under one id; creator CPM anchor ($2) differs from 03 ($10); "Udie" is Oodie. | A25, F11, G5, G9, G12, 7.20; international sequencing and product selection routed |
| 14 | The #1 bottleneck in 80% of audits (Blue Sense, May 2026) | Video | D, same agency as 01. Title 80% vs body 30%; audit gate $5M+; all examples hypothetical; strongest formula set in the folder. | A1 to A8, A11, A23, A24, B1, B2, C2 to C4 measurement bands, D10, 7.11, 7.17 |
| 15 | Black Friday 2026 strategy (Nathan, Blue Sense, Sep 2026) | Client briefing | D, same agency. Sells the pacing, attribution and creative services described; portfolio averages plus secondhand Triple Whale, House and Motion figures that disagree on magnitude; a break-even example that does not reconcile; Australian macro. | 3.F in full, 4.6, 5.5, H8, 7.10 |
| 16 | I scraped 700 IM8 ads and read their P&L | Teardown video | B for the disclosed figures (with narrative caveats), D for the audit pitch ($10M+), E for the scrape; ambassador cost, CAC arithmetic, net margin and one ad count internally inconsistent. Family with 09. | A6, A10, A11 CM definition, A17, A22, B9, 3.H method, 7.8 |
| 17 | Alo Yoga teardown (Blue Sense) | Teardown video | D and E. Same agency (audit $5M+); a one-time scrape; "every financial figure here is an estimate"; composition is not spend; machine-transcription errors in proper nouns. | B7, B12, D7 retail lift, 3.H method, E7 scarcity, 7.9, 7.18 |
| 18 | How Comfrt made $500M in 3 years (Hudson) | Podcast | C. Host is his mentor and sells a course; "$500M" never stated in the body; ROAS undefined; two brands with opposite paid outcomes. | B8 repricing, B9 creative floor, C7 pace and sellout, D5 affiliate structure, F11, G1, G16, 7.4 |
| 19 | The death spiral (Blue Sense, about 2022) | Video | D, same agency, older; audit gate $10M+; unnamed "2022 report"; Casper and SDC figures unsourced; omits the cash exception 14 states. | A8 bands, A9, A16, A18, A19, A20, A21, B3, 4.10, 7.17 |
| 20 | 5 ecommerce myths (host and Angus) | Podcast | D minus. Cross-promotion, no named product; anonymized audits; "Paul Wy" attribution unverified. Likely same agency family. | A23, B14, D6, 7.3, 7.9 support, 7.12 |
| 21 | How Gruns went from $0 to $500M (narrator) | Video | E. Outside reading of a public ad library plus an LLM demo; headline revenue unverified; GLP-1 compliance ignored. | B10, H7; repositioning routed to 02-AVT, 10-MCR, 07-LPG |
| 22 | The six bottlenecks in ecommerce growth | Video | E. One hypothetical spreadsheet; no pitch; defers fixes to a next video; CAC example internally inconsistent ($65 vs $55; "7x" does not reconcile). | A12, A13, A14, 4.9; the only source with the 6-lever cash frame |

**Families to read as one voice.** Blue Sense Digital: 01p1, 01p2, 14, 15, 17, 19, and likely 20. Bloom: 03 and 13 part 1. IM8: 09 (inside) and 16 (outside). The same podcast series hosts 07, 09 and 12.

**Neighbour folders and what lives there.**
- 01-PRD product research: category selection, validation gates, launch caps, sampling, review mining, clinical validation.
- 02-AVT avatars: personas, layered demographics, angle generation, empathy feeds.
- 03-OFF offers: every pricing, discount, bundle, GWP, upsell, subscription-tier and offer-ladder mechanic.
- 04-BRD brand: positioning, packaging, naming, collabs, brand lines, harvest-vs-create, enterprise campaigns.
- 05-SET store setup: localized stores, international checkout, cross-border integrations.
- 06-MEA measurement: attribution windows, CAPI, GA4, lift and geo-lift design, surveys, tooling, reliability ladder.
- 07-LPG landing pages: routing by awareness stage, persona pages, grids, collab landers, PDP structure.
- 09-CRO testing: one-variable tests, funnel instrumentation, proof and urgency elements under the 3.E gates.
- 10-MCR paid social creative: concepts, hooks, formats, volume, fatigue, production tiers, scripts.
- 11-ADC ad copy: hook writing, awareness stages, research, copy vs content.
- 12-GAD Google Ads: structure, PMax, Shopping, bidding, feeds, branded search, root-cause diagnostics.
- 13-ORG organic and content: creator programs, sponsorships, affiliates, founder content, sampling, events.
- 14-EML email lifecycle: flows, welcome offers, attribution, surveys, identity resolution, owned channels.
- 17-CXP post-purchase: retention phases, cohorts by category, churn maps, service recovery, reviews.
- 18-COG sourcing: suppliers, manufacturers, retail entry, 3PL and 4PL, inventory buffers, sell-through.
- 19-WLD wild bets: golden tickets, stunts, TikTok Shop plays, AI ladders.
- 20-FIN finance: P&L build, forecasting, working capital, exits, PE, secondaries, treasury, the formulas behind section 3.A.
- 21-OPS team: hiring, org design, decision loops, SOPs, founder role, leadership.
- 22-AMZ Amazon: direct selling, rank sequencing, one-price policy, counterfeit.
- 24-DEP ad deployment: Meta account structure, testing budgets, pacing rules, existing-customer spend, peak pacing mechanics.
