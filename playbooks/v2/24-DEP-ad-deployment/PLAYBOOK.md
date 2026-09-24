# 24-DEP-ad-deployment playbook

version: 2.0-draft  |  date: 24 Sep 2026  |  sources: 10  |  cards: 213  |  built from: sources/*.md

## 0. How to use this playbook

**Who runs it.** The paid social performance agent for Meta and TikTok. It owns account and campaign structure, launch settings, test sizing, kill and scale calls, budget pacing, attribution settings, new-customer measurement, retargeting and exclusions, account audits, and TikTok setup (pixel, in-feed, Spark, Search, Shop, GMV Max). Creative production, hooks and scripts belong to 10-MCR. Attribution modelling, MMM and analytics tooling belong to 06-MEA. Google Ads belongs to 12-GAD. Ad copy belongs to 11-ADC.

**Meta is read-only in ecomOS. Propose, do not execute.** Every Meta step in this playbook ends in a written recommendation for a human to apply. The Meta MCP has write tools; they are not allowed. TikTok has no connector yet; all TikTok steps are also proposals or instructions for a human operator.

**Which sections to load for which task.**

| Task | Load |
|---|---|
| Design or restructure a Meta account | 2, 3 groups A to E, 4 (P1, P2), 5.4, 6, 7.2, 7.3 |
| Launch a Meta creative test | 3 group F, 4 (P3), 6, 7.10 |
| Read a test, kill, keep or scale | 3 groups G and H, 4 (P4, P5), 5.1, 6, 7.1, 7.9 |
| Weekly account read | 5.1, 3 group G, 9 (diagnosis memo) |
| Attribution and new-customer measurement | 3 group I, 4 (P6, P8, P18), 5.3, 7.3 |
| Frequency and fatigue | 3 group K, 5.2, 7.6 |
| Retargeting, existing customers, DPA | 3 group L, 4 (P7), 7.4 |
| Full account audit | 3 group N, 4 (P9, P18), 5.3, 5.4, 9 |
| Understand why delivery behaves as it does | 3 group J, 7.5, 7.7, 7.8 |
| TikTok account, pixel and first campaign | 3 group O, 4 (P11, P12, P13), 5.5 |
| TikTok Spark, Search, Shop, GMV Max, retargeting | 3 group P, 4 (P14 to P17), 5.5, 5.6 |
| Any point where sources disagree | 7 |
| What to hand back | 9 |
| What cannot be known without brand data or the web | 10, 11 |

**Fetch before acting.**

- From brand data: monthly spend by platform and campaign, monthly orders split new vs returning, AOV, gross margin by category, break-even ROAS and allowable CPA, repeat purchase rate and repurchase cycle, customer count (for exclusion and retargeting sizing), new ads launched per month, current concept list, time from first visit to purchase, revenue by weekday. Full list in section 2 and section 10.
- From the data layer (Meta MCP read tools, TikTok exports, Metabase for Gehna): campaign, ad set and ad spend, ROAS, CPA, frequency, reach; audience segment breakdown (new, engaged, existing); attribution comparison columns (7-day click, 1-day view, incremental); EMQ per event; placement breakdown; ad set targeting and attribution settings.
- From the web: every `[web check]` in section 10 that touches the decision at hand. Most sources are late 2025 to mid 2026 snapshots of fast-changing platform features.
- From the user: spend tier, target countries, risk appetite (ABO vs CBO, cap vs double down), which brand (Gehna, Peach Bucket, TrailFold: keep them apart).

## 1. Scope and outcomes

**Covers.** How to structure a Meta ad account by spend tier and business complexity. How to build concept ad sets and name them. How to target (broad with hard controls). How to size a test, how long to run it, how many ads to load. When to kill, keep, fork or scale. How to pace budget increases and find a creative's spend ceiling. Which attribution setting to optimise and read on, and how to prove new-customer profitability. How Meta delivery works (retrieval, ranking, auction) and what that means for creative volume and diversity. Frequency and fatigue reads. Retargeting, existing-customer budgets and DPA share. How to audit an account from business numbers down to the ad. TikTok Ads Manager and Business Center setup, pixel, in-feed Sales campaigns, budget rules, Spark Ads, Search, TikTok Shop and GMV Max, retargeting audiences.

**Does not cover.** Creative production, hooks, scripts, awareness-stage writing, UGC sourcing, AI video tools (10-MCR; sources 01, 05, 06 and 09 carry creative material that is recorded in their mini playbooks, not here, except where it drives a deployment decision). Pixel and CAPI implementation detail, incrementality test design, MMM (06-MEA). Google Ads structure, brand vs non-brand, Merchant Center (12-GAD; source 03 touches these and they are pointed there). Landing page tests (09-CRO, 07-LPG). Offer and pricing design (offer folder), though rule A3 records the sources' view that economics set the bid ceiling.

**Business measures it moves.** New-customer count and CAC. First-purchase gross profit to CAC. Acquisition MER (new-customer revenue divided by ad spend). Contribution margin after ad spend. Share of spend reaching new people vs existing customers. Creative test throughput (concepts tested per month, winners found per month). Wasted spend from broken exclusions, wrong attribution, undefendable campaigns and over-frequency.

## 2. Inputs the agent needs

| Input | From where | Required or optional | Why |
|---|---|---|---|
| Monthly Meta and TikTok spend, last 24 to 30 months | Brand record, data layer | Required | Spend tier picks the structure template (B rules); cohort model needs history (source 03) |
| Orders per month split new vs returning, per platform if possible | Brand record (Shopify or Metabase) | Required | CAC, aMER, first-time P&L, new-customer ROAS (I rules) |
| AOV and gross margin by category, monthly, post-discount | Brand record | Required | GP to CAC, break-even ROAS, category segmentation (rules A3, B6) |
| Break-even ROAS and allowable CPA | Derived from margin; user confirms | Required | Every kill, keep and scale rule needs a target |
| Repeat purchase rate and repurchase cycle | Brand record | Required | Existing-customer exclusion window, whether a retargeting campaign is justified (L rules) |
| Customer file size and sync status (Klaviyo to Meta, CSV to TikTok) | Brand record, data layer | Required | Exclusions and retargeting budget formula (rule L3) |
| Conversions per month per campaign | Data layer | Required | Consolidation test (rule B2) |
| Current campaign, ad set and ad list with names, targeting, attribution setting, budget type | Data layer | Required | Structure audit (5.4) |
| Audience segment breakdown (new, engaged, existing) with spend, ROAS, frequency | Data layer | Required for Meta reads | New-customer profitability check (5.3), frequency check (5.2) |
| Attribution comparison columns (7-day click, 1-day view, incremental) | Data layer | Required for Meta reads | Rule I1 to I5 |
| Ad-level frequency, reach, CTR, CPM, hook and hold rate | Data layer | Optional | Fatigue and soft-metric reads (K rules, J rules) |
| EMQ per event, CAPI status | Data layer, 06-MEA | Optional | Signal check (rule J8) |
| New ads launched per month and concept tags (persona, angle, offer) | Brand record, creative team | Required | Creative velocity vs spend (rule N6), concept counts (rule N7) |
| Revenue by weekday and time from first visit to purchase | Brand record | Optional | Test duration (rule F4) |
| Target countries, languages, minimum age for category | User | Required | Hard controls (rule D2) |
| Risk appetite: efficiency vs de-risking | User | Required | ABO vs CBO (rule E1), cap vs double down (rule H6) |
| TikTok: Business Center, ad account, pixel status, Shop status | User, TikTok exports | Required for TikTok | Launch check (5.5) |
| Competitor ads | Inspiration layer (Creative Center, Foreplay) | Optional | Layout and mood only; never copy text, faces or products (ecomOS rule) |

## 3. Decision rules

Each rule states the rule, its condition, the mini playbooks that support it (S01 to S10), conflicts, and card ids. Where only 1 source says it, the rule says "Source Sxx says".

### Group A. Foundations

**R1. Fix in this order: data integrity, then account structure, then creative.** Condition: any audit or restructure. Data is first because everything else is judged on it and it is quickest to fix. Structure is second because it is fast. Creative is second by commercial impact but slowest to fix. Supports: S03 (explicit order), S02 (data integrity as non-negotiable), S08 (data integrity test). Conflict: card 2156baae2c7a says structure is number 2 by impact; the S03 transcript says creative is. Use the transcript. [7101da7d331d] [2156baae2c7a] [b8107473f4c3] [e336ef61445a]

**R2. Every structure must pass 2 tests: readable data and commercial alignment.** Condition: every account, every tier. Readable data: you can run a decision loop (read, decide, wait, decide again) and defend every layer to an outside auditor. Commercial alignment: budget can flex to the categories, ranges, regions and personas the business needs, and low-margin lines cannot soak up spend unseen. If either fails, restructure. Supports: S02, S08. [b8107473f4c3] [f623a968dbf2] [3da640845924] [e336ef61445a]

**R3. Economics set the ceiling; tactics cannot beat bad unit economics.** Condition: before any scaling plan. Your sustainable bid is your first-order gross profit plus what retention allows. Higher price, AOV, units per transaction, margin and retention win more auctions than any structure or setting. Review first-order AOV, gross margin and 365-day LTV payback before tactics. Supports: S04 ("cannot out-tactic bad economics"), S03 (GP to CAC bands), S07 (scale is a business problem), S09 (scale to break-even ROAS, net free cash flow). [bd4cb33200e9] [8ffd28b7fc7e] [021224f4073c] [1ff82eb90f46] [259da0427eb7]

**R4. Judge on business numbers, not platform ROAS alone.** Condition: any keep, kill, scale or budget decision. Platform ROAS must correlate with acquisition MER (new-customer revenue ÷ ad spend). Period ROAS = total value ÷ total spend from store data (ecomOS rule). If the platform number is far above aMER, suspect existing-customer spend or view-through credit before believing it. Supports: S03, S07 (ignores Meta CPA, uses outside attribution), S09 (blended ROAS and net free cash flow), S10 (SKU-level new-customer sales). [378c1eb72ff9] [40de3bd68e44] [259da0427eb7] [b410bffcb50f]

**R5. Do not act on Meta's in-platform suggestions, scores or projected uplifts without own-account evidence.** Condition: any Ads Manager recommendation, opportunity score, or "lower cost per result by 11%" prompt. Test it and log the result, or skip it. A profitable account can show opportunity score 0. Source S07 says this; S02 and S04 agree that platform-wide updates aim to raise Meta's take, not your ROAS. [d9cba85df27b] [94fa98ec33c1] [5b99bf6d671d] [e82a1ef3cf77]

**R6. Expect CPM inflation of about 20% to 30% a year and plan creative and page improvement to offset it.** Condition: annual planning. A creative or offer that broke even 12 months ago may lose money now. Source S02 says this from its own aggregated spend report. `[needs brand data: own CPM trend by year]` `[web check: current Meta CPM inflation]` [5b99bf6d671d]

### Group B. Account and campaign structure by spend tier

**R7. Start from 1 cold campaign; every extra campaign must be defendable in 1 written line.** Condition: any Meta account. Valid reasons: different unit economics (margin spread, grade A to D inventory), non-overlapping personas or ranges (men's vs women's), different regions with own stock, targets or URLs, a promo cadence that would disrupt learning, a funnel large enough to KPI on its own (S02 example: advertorials at about 30% of spend), a business unit with its own KPI (new arrivals vs core, protein vs pre-workout). Not valid: "spend feels big", a duplicate cold campaign doing the same test, an objective swap (add to cart) with no reason. Accounts at $1M to $5M a month often run only 4 or 5 campaigns. Supports: S02, S03, S04, S08. [5ce17b008587] [7230fc5fab8f] [568f98fcc9aa] [7350eaba553e] [0ed2f8dbde17] [52611fb24810] [74eaa65de2ef]

**R8. Consolidate by default because conversion data is siloed at campaign level; accounts improve past about 100 to 200 conversions a month per campaign.** Condition: low conversion volume. 100 conversions a month over 4 campaigns gives 25 each, and each optimises worse. Ad set splits cost less: about 5% to 10% efficiency swing. Source S02 gives the numbers; S04 and S08 agree on the mechanism. [7230fc5fab8f] [9b521e4ff188] [0ed2f8dbde17] [3ae3be9f8f79]

**R9. Full consolidation (1 campaign, 1 ad set, all ads, or 1 Advantage+ campaign with everything) is wrong for about 90% of brands.** Condition: segment when any of these hold: (a) margin spread across ranges, (b) non-overlapping audiences, (c) very high AOV with low conversion volume (S02 example: $10,000 AOV, about 5 orders a day). 1 Advantage+ campaign is acceptable only for 1 product, 1 persona, small spend. Supports: S02 (90% figure), S08 ("terrible idea" for any real complexity). Conflict with Meta's own consolidation push: see 7.2. [ebff07a9e6f2] [1589854e06d9] [52611fb24810] [7230fc5fab8f]

**R10. Under $50k a month: testing campaign (concept ad sets, 3 to 5 ads each), optional scaling campaign, optional small existing-customer campaign.** Condition: this tier, as a safe default, not a custom design. Exclude existing customers from testing and scaling. Attribution 7-day click. Read window never shorter than 5 days. Skip a website-visitor retargeting campaign in about 90% of accounts. Source S02 gives this template. [ba414cee7839] [fb9db4eb1b28] [0e642b4c3a8c] [b8a2663f518f] [ccf942b9f2c8] [568f98fcc9aa]

**R11. $50k to $250k a month: more concept ad sets, 2 or 3 cold campaigns each with a commercial reason, 100 to 300 new ads a month.** Condition: this tier. Split single-SKU CPG by funnel or persona when landing pages, creators and photos differ ("almost 2 businesses"). Split multi-SKU fashion by commercial lever (new arrivals, a category with better LTV run at a higher CPA). Example fit: 2 campaigns x 10 ad sets = 20 ad sets, 5 to 15 ads each. Source S02. `[needs brand data: LTV and repeat rate by first-purchase category]` [7350eaba553e] [65e0503d7bc4]

**R12. $250k plus a month: page strategy is mandatory, bidding diversity across campaigns, consider a second ad account on the same pixel, keep testing.** Condition: this tier. Meta caps live ads per page at about 300 to 500 `[web check]`. Second account: different bid logic (maximize value, cost caps) and a fallback if the main account is banned or billing fails; it might hold 10% of spend. Do not split ad accounts by country except for billing currency. Source S02, and it says this advice changes about every 6 months. [58966745d295] [8494f59ad41f] [63e75994772f] [b8c4642d637c]

**R13. Campaign-level splits follow business units; ad set splits follow the variable you want to learn.** Condition: designing any layer. Product categories with different margins, demographics or budgets can be campaigns (or ad sets if there are many; do not make 20 low-budget campaigns for 20 categories). The preferred ad set variable is the creative concept. Format splits (image, video, DPA in separate ad sets) only for new accounts under about $10,000 a month. Landing-page splits only when testing a new custom page. Launch-date splits never. Supports: S08 (explicit), S02 (segment at ad set before multiplying campaigns). [52611fb24810] [1ed05eaf4fa7] [a5c883d83f91] [acad4b08fee6] [66c735ceb8ff] [ebff07a9e6f2] [49146dda7d03]

**R14. Run promos in their own campaign when they recur.** Condition: promo cadence of about every 3 to 4 weeks or any promo that would disrupt testing and scaling learning. Promo audiences are more price-sensitive and turn over fast. Source S02 ($750k a month account). [74eaa65de2ef]

**R15. Pull a funnel out into its own campaign once it is large enough to KPI alone.** Condition: S02 example is advertorials at about 30% of total spend. Below that, keep it inside the testing structure. [74eaa65de2ef]

**R16. Do not add structure to make reporting look tidy.** Condition: any proposed split. Structure is a manual signal that some ads must learn separately. Reporting problems are solved with naming and filters. Supports: S04, S02 (international reporting by filters, not accounts). [0ed2f8dbde17] [b8c4642d637c]

### Group C. Ad set design

**R17. A concept = persona + angle + offer (+ ad type or format when it changes enough to be read as a different ad). 1 ad set holds 1 concept.** Condition: cold campaigns at every tier. Change any 1 of the 3 and it is a new concept. Ad type is flexible inside a concept. Supports: S02, S03, S04, S06 (1 stage per concept), S07 (1 net-new concept per ad set), S08. [b722b2c086bc] [65e0503d7bc4] [94c8e0f902f4] [917ee36d87e9] [45c43e3ff759] [6ee9db26f236] [faa05bf3cff8]

**R18. Minimum 3 ads per ad set; rule of thumb 3 to 15; 5 to 20 for reading spend share; up to 50 new per concept per month at high volume.** Condition: 3 is the floor so the ad set can sequence (people see an ad 2 to 6 times before buying). 200 ads in 1 ad set is possible but usually spans several concepts that should be split. Supports: S02 (3 to 15, min 3), S08 (5, 10, 20; 50 per concept per month), S07 (1 concept + 3 variations = 4). `[web check: current ads-per-ad-set limit]` [d6c0209e9d6b] [ab729ba34368] [3ae3be9f8f79] [6ee9db26f236]

**R19. Load a new concept with the concept ad plus 3 variations (different hooks) so a concept is not killed on 1 ad.** Condition: new-concept tests. Source S07 says a hook variation won while the original lost. Variations of the account's current top ad usually do "decent" but do not beat it. Conflict with "only net-new concepts after Andromeda": see 7.8. [6ee9db26f236]

**R20. Keep conflicting personas out of 1 ad set.** Condition: men's and women's ranges, or any 2 personas who do not overlap. Mixed ad sets have no group to optimise toward and go broad. Check with a gender breakdown per ad `[verify UI]`. Supports: S02, S08. [ebff07a9e6f2] [3e877cb4c991] [66c735ceb8ff]

**R21. Group all funnel stages for 1 persona in 1 ad set, or split by stage only if you blend the numbers when deciding.** Condition: same persona and product. S02: a consolidated persona ad set at 4x; the same ads split into 2x (top) and 6x (bottom) get the 2x cut by mistake. S06 agrees that awareness-grouped ads self-select their audience (unaware ads at low frequency, product-aware ads retargeting on their own). Conflict: see 7.2. [d6c0209e9d6b] [faa05bf3cff8]

**R22. Name ad sets: persona, angle, offer, content type (if grouped by type), launch date. Never batch names like "March 7 creatives".** Condition: every ad set, every campaign, same convention account-wide. Rename old ad sets retrospectively when taking over an account. TikTok: product + objective + date at campaign level, same convention downward. Supports: S02, S08, S03 (naming must match settings and creative), S05. [c910cbdcfaae] [66c735ceb8ff] [36f63e27c6d5] [0856c5eb5224]

**R23. Never touch an ad set that is hitting KPI. Fork it.** Condition: new creative for a winning concept goes into a new ad set beside it. New creative for a losing concept goes into the losing ad set to try to revive it. Expect sprawl: 6 of 10 ad sets may belong to 1 winning concept. Source S02 calls this the number 1 rule of Meta buying. Conflict with S08, which places new ads into the matching concept ad set regardless: see 7.11. [a95742238877] [ba414cee7839] [b722b2c086bc]

### Group D. Targeting

**R24. Go broad on Meta. Keep only hard controls: exclusions, minimum age, locations (never worldwide), languages.** Condition: cold prospecting, all tiers. Age bands, gender, interests and lookalikes are suggestions Meta may ignore. The creative does the targeting (see group J). Supports: S02, S03 (would not use interests or lookalikes in 99% of ecommerce purchase accounts), S04, S07, S09 (7-day broad vs stack test). Conflict on whether interests and lookalikes are fully dead: see 7.5. `[verify UI]` `[web check: which audience fields are hard controls vs Advantage+ audience suggestions]` [4c81bdf1685a] [b025c790c4ac] [48728b3abcdf] [071837c01e9b] [32581af3f424] [9869e4293b51]

**R25. If you test interests, lookalikes or custom audiences on Meta, cap them as a small sandbox.** Condition: S07's practice; no cap amount given. Spend the saved time on creative. [32581af3f424] [a55d9b19503c]

**R26. Put the audience in the creative and the copy, not in the targeting.** Condition: broad targeting. Casting (age and gender of people shown), hook, format, copy, thumbnail and landing page all steer delivery. S09 adds identity words in headlines ("for 25-year-old women") and long copy that says who the ad is for; both are 1 presenter's model and must not misstate the offer or break personal-attribute policy `[web check: Meta ad policy on personal attributes in copy]`. Supports: S04, S07, S09, S06. [48728b3abcdf] [32581af3f424] [ffc5c00e2e11] [0de9911b652b] [7443b5bb8016]

**R27. Exclude existing customers from every cold campaign (testing and scaling).** Condition: all tiers, all cold Meta campaigns; TikTok retargeting excludes buyers too. Reasons: repeat buyers make a concept look better than it is, Meta pushes spend to warm clusters that convert easily, and S10's example sent about half of a TOF budget to existing customers. Window: start at 2 years, treat older buyers as lapsed and consider a dedicated lapsed campaign; shorten to the brand's repurchase cycle in short-cycle categories. Supports: S02, S03, S04, S10, S01 (TikTok). Conflicts: S07 allows at most 1 purchaser exclusion on retargeting and none elsewhere; S06 says exclusions do not fix weak creative; Advantage+ offers a percentage cap instead. See 7.4. `[needs brand data: customer file, repurchase cycle]` `[verify UI]` `[web check: existing-customer controls in current Advantage+ sales campaigns]` [fb9db4eb1b28] [b025c790c4ac] [071837c01e9b] [cf3aa44a7de1] [1ee708d070fe]

**R28. Do not launch placement, age or gender campaigns from breakdown ROAS.** Condition: any breakdown (Stories 4x vs Feed 3x with Feed at 80% of spend). Breakdown data is blended and ignores incremental return; Meta has tested pushing spend to the "better" breakdown and found poor incremental return. Exceptions need 6 to 7 years of buying experience. Source S02, citing Meta's "breakdown effect" help page `[web check]`. [528465d5cc14]

**R29. Remove Audience Network "app rewards" placement from store-traffic or engaged-view campaigns.** Condition: local or store campaigns bleeding into it. Source S03 says it has never seen it drive a purchase. `[verify UI]` [b025c790c4ac]

### Group E. Budget type and bidding

**R30. ABO vs CBO is a risk choice, except at high AOV with low volume where you must use ABO.** Condition: CBO gives efficiency with concentrated risk (20% of ads take 80% of spend; new or expensive ads may get nothing). ABO forces spend through every test at slightly lower ROI (S02's hypothetical: about 10% lower). Inexperienced buyer: consolidated CBO. Experienced buyer weighing risk: ABO or in-between. At $10,000 AOV and about 5 orders a day, CBO falls back to CTR and CPC signals, so use ABO. Supports: S02, S08 (CBO or manual ad set moves, no pick), S01 (TikTok: CBO off for testing, on for scaling). Conflict: card 1589854e06d9 says "default to CBO when volume is healthy"; the S02 transcript says personal preference. [2f66cf4f65c6] [1589854e06d9] [479be1c347e0]

**R31. At large spend, S02's preferred structure is CBO with ad set minimum and maximum spend limits: about 60% directed, 40% free.** Condition: needs heavy oversight; overkill at about $10k a month. S08's 40% max cap on a winning ad set uses the same control. `[verify UI: ad set spend limits under campaign budget]` [2f66cf4f65c6] [99cd67e7cbac]

**R32. Seasonal rotation: CBO in Q4 peak, ABO in Q1 for clean testing.** Condition: S02's practice for some accounts. Q4 conversion rates inflate ad reads. [2f66cf4f65c6]

**R33. Ignore cost caps and bid caps under about $200k a month; pick a bid strategy by business constraint, not fashion.** Condition: lowest cost runs profitably at multiple 5 figures and 6 figures a day (S07). Cost cap for a CPA ceiling, bid cap for a bid ceiling, target ROAS or maximize value for return goals. Daily bid tweaks might squeeze about 5% for an hour a day; the same hour on creative pays more. Bidding diversity across campaigns matters over about $250k a month. Supports: S02, S07, S08 ("media buying died" for daily tweaks). [bfec753c654b] [9997eb5233ac] [1ff82eb90f46] [b0bdf29a1f32] [5e79782f9a1e] [58966745d295]

**R34. Cost caps and bidding live at ad set level, never ad level.** Condition: always. Ads inherit optimisation from the ad set, which is 1 reason ad-level ROAS misleads. Source S02. [9ede69b02ec7]

### Group F. Launching and testing

**R35. Size a creative test by 1 of 2 methods, and decide the end condition before launch.** Condition: every Meta test. Method 1 (kill rule): spend threshold = 3x target CPA at the concept ad set; at threshold 3 to 4 conversions keep, 2 yellow (run about 1 more CPA of spend), 0 to 1 cut. Preferred when the client allows: 5x target CPA, strict yes or no. Method 2 (formula): daily budget = (target conversions x expected CPA) ÷ test days; S02 example 20 x $100 ÷ 14 = about $143 a day. Meta's 50 conversions per 7 days learning rule gives about $714 a day per ad set at $100 CPA and is unrealistic for about 99% of advertisers. Source S02 gives both methods without reconciling them. Conflict: see 7.10. [87a85788a663] [1c683e007b76] [57a5a1e787d4] [b8a2663f518f]

**R36. Default test duration 1 week; 3 to 4 days for large stable brands with short purchase cycles; 10 to 14 days for tiny budgets, long cycles or heavy weekday seasonality. Never under 5 days below $50k a month. Never act on 1 day.** Condition: match the read window to volume (3 conversions in 3 days cannot support 3-day reads; 1,000 a day can support 2-day reads). S07: expect sine-wave daily results under about $1,000 a day; pull at least 7 days and the largest spend window. Supports: S02, S07, S09 (7-day broad test). `[needs brand data: revenue by weekday, time from first visit to purchase]` [f88304f4647b] [b8a2663f518f] [c8f9d9634c5f] [9869e4293b51]

**R37. Do not judge ads on $1 to $2 of spend, and do not set ad set budgets from the learning-phase rule.** Condition: any test. Ads never stop learning; do not obsess over exiting learning. Supports: S08, S02, S07. Conflict on learning phase: see 7.7. [3ae3be9f8f79] [1c683e007b76] [c8f9d9634c5f]

**R38. Test creatives that differ a lot, so winners and losers are clear.** Condition: any test batch. Near-identical ads collapse into 1 Entity ID and share the same audience pool (S04: 200 ads read as 20). Diversity means concepts (angle, offer, persona), not formats. Supports: S04, S03, S05, S08. [917ee36d87e9] [45c43e3ff759] [d3b3e82930e5]

**R39. Never test inside the scaling campaign.** Condition: any account with a scaling campaign. Source S02. [b8a2663f518f]

**R40. Launch about 1 new ad per $1,000 of monthly spend, with diminishing returns at very large spend.** Condition: creative volume check. $100k a month = about 100 ads; $1M to $3M does not need 3,000. S02 says 100 to 300 a month at $50k to $250k. At large spend replace the heuristic with a winner-churn or average-winner model `[needs brand data: winner churn, hit rate, average winner revenue]`. Supports: S03, S02, S09 (Andromeda is "a hungry panda"). [ea5e41f9a967] [65e0503d7bc4] [5a4c1bc7103b]

**R41. Concept count by spend band: under $100k a month test 1 to 3 concepts well; $100k to $500k about 2 winning and 2 to 6 in test; above $500k 3 or more winning and 4 to 5 core funnels.** Condition: S03 heuristic. 1 concept at $200k a month and 200 ads a month is a fatigue risk. [45c43e3ff759]

### Group G. Kill, keep and scale rules

**R42. Make the ad set the unit of decision. Do not kill or scale single ads on their ROAS.** Condition: every read. Campaign 7-day-click ROAS is relatively reliable, ad set less, ad very unreliable, because the UI is last click while Meta optimises across multi-ad sequences. 3 ads at $5,000 each with very different ROAS may all be doing their job. Ask 1 question: is this ad set, with this set of ads, at KPI? Supports: S02, S08, S06 (judge unaware ads account-wide), S10 (rankings untrustworthy under view-through). Conflict with S05 and S09, which rank ads: see 7.9. [9ede69b02ec7] [ab729ba34368] [b722b2c086bc] [7443b5bb8016] [34a82c492fd6]

**R43. Inside an ad set that is at KPI, use spend share as a rough creative read: the ads taking spend are the ones to make more of.** Condition: only inside an ad set at KPI, and only for creative briefs, never for budget moves. Of 20 ads maybe 4 spend. Source S08. [ab729ba34368] [94c8e0f902f4]

**R44. Keep-kill call at the threshold (Method 1): 3 to 4 conversions at 3x CPA keep; 2 yellow; 0 to 1 cut. At 5x CPA yes or no only.** Condition: applies to concept ad sets, not single ads. Source S02. [87a85788a663]

**R45. At KPI: raise the ad set budget about 20% a day (small tier) or by a larger step if you accept the lag. Missing KPI after enough spend: diagnose the creative, make more ads and concepts, then wind down.** Condition: read over the rolling window in R36. Conflict on the 20% step: see 7.1. Supports: S02 (20%), S04 (no documented cap), S08 (rotate out after statistical relevance, number not given). [b8a2663f518f] [eff64339b5de] [99cd67e7cbac]

**R46. Before briefing more of a "winner", confirm it wins on new customers under 7-day click.** Condition: any top-spend ad in a TOF or scaling campaign. S10 example: 12.84x blended, about 5x on new audiences, 1.71x on new audiences under incremental attribution. Briefing creative on a false winner spends operating money against bad data. Source S10; S03 and S02 agree on the mechanism. [8c6833a8cd30] [34a82c492fd6] [378c1eb72ff9]

**R47. Do not ride 1 winner. Clone it into variants, keep other concepts alive, and cap or plan for its fatigue.** Condition: 1 ad or concept carries most spend. S09: turning everything else off is "amateur hour". S08: overleverage builds business risk; cap at, say, 40% or double down on purpose. S02: the winner will fatigue with no backup under CBO. [c61bad8559ba] [99cd67e7cbac] [477d8f00df92] [1589854e06d9]

**R48. Rescue ads a CBO ignored only if you have high conviction, in a separate ad set with its own budget.** Condition: after the CBO has run; S09 says another 20% of such ads "typically" turn out to be winners. No budget, duration or conviction rule is given, so cap it and log it. This conflicts with trusting the algorithm's allocation (S02 R28 logic). Source S09 only. [841a1ded8706]

### Group H. Budget pacing and scaling mechanics

**R49. Find each winner's spend equilibrium before moving it to a scaling campaign.** Condition: an ad set well above target (S02 example: above a 5x target) with strong soft metrics. Raise daily spend in steps; when ROAS drops to unprofitable, pull back; repeat until you find the level where results hold (example $300 a day). Record it as that creative's capacity. Source S02. [0e642b4c3a8c] [a95742238877]

**R50. Move only equilibrium winners (same post IDs) into a scaling campaign, keep the original running, exclude existing customers, KPI the scaling campaign at campaign level, expect about +20% daily spend on a good day.** Condition: worth it from about $400 a day per asset (adds about $80); not at $60 a day (adds about $10). Refresh top post IDs every 1 to 2 weeks at large spend. Source S02. [0e642b4c3a8c] [a95742238877] [b8a2663f518f] [74eaa65de2ef]

**R51. Budget increases above 20% are fine; the dip after a raise is a lag, not a learning reset.** Condition: judge a raise on 7 days or longer, not same-day revenue. New audiences need several exposures before buying. Source S04 says the 20% rule has no Meta documentation and its agency raises more all the time. S02 still uses about 20% a day at the small tier. Conflict: see 7.1. [eff64339b5de] [b8a2663f518f] [c8f9d9634c5f]

**R52. Scale toward break-even ROAS only if repeat purchase or cash position supports it; otherwise scale to a contribution-margin target.** Condition: S09's stance is to "keep feeding the beast" to near break-even on the first order and judge by net cash in 30 days. S03's bands say first-purchase GP to CAC of 2 to 3 is where to scale and below 1 risks bankruptcy unless retention is strong. Keep both; the agent uses GP to CAC bands as the default and S09's stance as an option the owner must choose knowingly. `[needs brand data: break-even ROAS, GP to CAC, retention]` [259da0427eb7] [021224f4073c] [96ddc2d014f8]

**R53. When you double down on a winning concept, shift creative volume toward it (S08 example: 120 ads for the winner, 40 for the rest, from 50 each) and build the whole funnel around it (S02: custom landing page, named bundle, testimonials).** Condition: winner confirmed on new customers (R46) and LTV of that concept checked `[needs brand data: LTV by acquiring concept]`. Supports: S08, S02, S03 (analyse and replicate winners). [477d8f00df92] [65e0503d7bc4] [7a6be5942fff]

**R54. Judge a scale-up on store-side new-customer sales for the SKU being scaled, not platform ROAS.** Condition: the scaled ad concentrates on 1 SKU. Store-wide reads need a much longer test or a bigger budget change. Confirm the SKU was not promoted elsewhere in the window (card addition). Source S10. `[needs brand data: SKU sales split new vs returning, daily]` [b410bffcb50f]

### Group I. Attribution settings and new-customer measurement

**R55. Optimise and read on 7-day click. Turn 1-day view off for budget decisions.** Condition: Meta, all cold campaigns; S10 says all campaigns. View-through pulls spend to ads that win on views, not clicks, and over-credits existing-customer revenue. Supports: S02, S08, S10. S03's go-to is 7-day click plus 1-day engaged view. Conflict: see 7.3. `[verify UI]` [fb9db4eb1b28] [04f6f0b93295] [ab729ba34368] [de104cfb484c] [34a82c492fd6] [451238284cae]

**R56. Use the same attribution setting on every campaign.** Condition: mixed settings change ROAS between campaigns and break comparisons. Source S03. `[verify UI]` [451238284cae]

**R57. Use incremental attribution as a comparison column, not as the optimisation target or the measure of success.** Condition: it is a modelled factor from aggregated lift studies of other advertisers. S10 example factor: 0.2x for a retargeting segment, turning 10x into 2x. S02 reads DPA and retargeting on it as a check. Supports: S10, S02. `[verify UI]` `[web check: how Meta models incremental attribution and whether it is still an optimisation option]` [de104cfb484c] [cf36e5f30572]

**R58. When platform ROAS and aMER still disagree after tightening attribution, run a test, do not guess.** Condition: 8 and 9 figure brands: Conversion Lift Test (user-level holdout, Experiments) or causal geo-lift, about 25 days, parameters set in advance. Design detail lives in 06-MEA. Supports: S03, S10. `[verify UI]` [845571c9595b] [de104cfb484c]

**R59. Build the new-customer view: CAC = spend ÷ new customers, first-purchase GP, GP to CAC, new-customer count, monthly, 2 to 2.5 years back; plus a first-time-customer P&L and aMER.** Condition: any audit; any brand with meaningful repeat revenue, which hides weak acquisition. Read: CAC up with volume up a lot may be fine; CAC up with volume flat is the bottleneck. Never use a flat GP assumption. Source S03. `[needs brand data: orders with new vs returning flag, monthly gross margin]` [96ddc2d014f8] [04bd5299ca53] [3b7f250f224e] [9cb9b9fec95a]

**R60. GP to CAC bands (first purchase): below 1 losing money on first order, 1 to 2 hold, 2 to 3 scale, above 3 spend more.** Condition: S03 opinion; retention moves the bands (strong retention allows lower; weak retention needs higher). Assumes no acquisition channel is left out of CAC. [021224f4073c] [cb04728e9c8a]

**R61. Do not tighten Google attribution windows or copy Meta rules onto Google; that is 12-GAD.** Condition: any cross-platform audit. Source S03. [89ab42bd67bc] [ce1358ea9d05]

**R62. TikTok: 1-day view inflates ROAS a lot; read 7-day click, and reconcile TikTok-reported purchases with store orders.** Condition: any TikTok read. S01 leaves attribution windows at default and never reconciles; S03 says TikTok drops to about aMER or lower at 7-day click. `[verify UI]` `[needs brand data: store orders to reconcile]` [378c1eb72ff9] [e413ec2ddfd9]

### Group J. The algorithm: delivery, ranking, auction, creative as targeting

**R63. Every impression passes retrieval, ranking (S07: light and heavy), then auction, in about 200 ms. Retrieval decides which ads even enter a user's auction, and that is where creative does the targeting.** Condition: mental model, not a setting. Andromeda (Dec 2024) changed retrieval; GEM made it multimodal (reads video, audio, groups creatives by representation); sequence learning (Nov 2024) optimises across ad sequences; adaptive ranking spends compute per impression. Supports: S04, S07. All dates and roles are presenter claims `[web check: Meta engineering posts on Andromeda, GEM, sequence learning, adaptive ranking]`. [e82a1ef3cf77] [4844059375a6] [6ee9db26f236] [066b6cc383fe]

**R64. Auction score = bid x estimated action rate + ad quality (S07 calls the last term user value). Estimated action rate = expected CTR x expected conversion rate. Relevance beats bid.** Condition: a $0.50 bid can beat $1 with better action rate and quality. You have 2 levers in action rate (creative for CTR, funnel for conversion rate) and 1 in bid. Quality and action rate are rear-view diagnostics you cannot set directly; diversify creative instead. Misleading clickbait works against the quality term and loses delivery over time. Supports: S04, S07. `[web check: current Meta help wording of the auction formula]` [8ffd28b7fc7e] [3ad804612663] [71ab0ba03b8a] [a55d9b19503c]

**R65. Broad targeting is a probe: Meta sprinkles spend across the space, finds clusters that buy, then narrows. Narrow creative saturates its cluster, frequency rises, then delivery drifts to nearby colder clusters and ROAS tapers.** Condition: this is why ads fatigue when scaled. S04's illustration: a very specific callout saturates after maybe $10,000. S02: as you scale the targeted area widens into less convinced people. [48728b3abcdf] [4de396baf031] [4c81bdf1685a]

**R66. Near-identical ads collapse into 1 Entity ID and reach no new people; only concept diversity reaches net-new audiences. Iterations are still allowed.** Condition: creative planning. S04: 200 ads read as 20 unique in groups of 10 (illustration). Entity ID is not visible in the account. Conflict with S07 on variations: see 7.8. [917ee36d87e9] [4de396baf031] [6ee9db26f236]

**R67. Post Andromeda, Meta will keep a product-aware ad on warm people who might convert and will not push it to unaware people. Loading many bottom-funnel ads and raising budget sends frequency "through the roof".** Condition: S06's model; verify in own data. It means the creative mix by awareness stage, not audience settings, decides cold reach. [7443b5bb8016] [faa05bf3cff8]

**R68. Keep signal clean (pixel plus CAPI, purchase event EMQ), but treat EMQ as plumbing, not a profit lever.** Condition: if Meta sees 70 of 100 conversions it under-estimates your action rate and you lose auctions you should win (S04). S07: EMQ 9.8 to 9.9 with no visible link to profit. S04: paid server-side tools are a "very small" unmeasurable lever; get them if affordable. Conflict: see 7.6. Setup lives in 06-MEA. `[verify UI]` `[needs brand data: purchase EMQ, Meta purchases vs backend orders]` [74d3bc849c6b] [40de3bd68e44] [773fc35a99e9]

**R69. Meta updates aim at small platform-wide lifts so Meta can raise CPMs; expect your ROAS to stay flat while you adapt.** Condition: planning. Do not expect an update to raise your ROAS. Sources S04, S02. [e82a1ef3cf77] [5b99bf6d671d]

**R70. CPC and CTR barely predict return except at extremes; a new ad set or campaign over-weights soft metrics until it has conversion data.** Condition: allocating on CTR, CPC or hook rate. Very high CPC does mean very low ROI (S02). In a new account images and DPAs take spend early on soft metrics (S08). S07 still says Meta rewards high CTR with lower CPMs over time. `[needs brand data: CPC vs ROAS by ad]` [1589854e06d9] [a5c883d83f91] [3ad804612663]

### Group K. Frequency and fatigue

**R71. Read frequency by audience segment on a 30-day window, not as a percentage split.** Condition: any Meta account with audience segments defined. Existing customers: keep below 7 per 30 days (S02); 30 is over-spend, 50 clearly, 1 likely under-spend. Engaged about 14 (S03 example) means too much middle-funnel creative. New segment frequency normal for cold. Supports: S02, S03. S10 flags "a little bit high" on a top TOF ad with no number. `[verify UI]` [9d8a9963309a] [b8a436d33e2f] [3a48f7471999] [8c6833a8cd30]

**R72. Rising frequency with flat cold reach and stalled scaling is a creative-mix problem first, not an exclusion problem.** Condition: audit the live library by awareness stage; expect too many product-aware or feature-led ads. Shift production up the stages (S06 starting split 80% unaware and problem aware, 10% solution aware, 10% product and most aware). S04 agrees: add distinct concepts, not iterations. Conflict with S02 and S10, which fix exclusions first: see 7.4. `[needs brand data: frequency and reach by ad set, creative mix by stage]` [7443b5bb8016] [b81e94d98fa2] [4de396baf031]

**R73. Watch frequency and ROAS trend on persona-specific ads; when frequency rises and ROAS tapers, brief a new concept, do not iterate.** Condition: narrow-persona ads. Source S04 (with card inference on triggers). [4de396baf031]

**R74. Fatigue is the reason to keep a pipeline: the account's top ad will die, and a variation of it will usually not beat it.** Condition: any account with a dominant winner. Supports: S07, S09, S08. [6ee9db26f236] [c61bad8559ba] [99cd67e7cbac]

### Group L. Retargeting, existing customers and DPA

**R75. Retargeting is a capped support layer, not a growth driver. On cold ask "where can we spend more", on retargeting ask "where can we spend less".** Condition: all retargeting on Meta, TikTok, Pinterest. Audits find about 50% of spend on existing plus engaged, which is a mistake. Source S02; S03 agrees (frequency-based caps). [028483f1e7af] [9d8a9963309a] [b8a436d33e2f]

**R76. Skip a website-visitor retargeting campaign in about 90% of accounts.** Condition: the audience segment breakdown shows the engaged segment already gets meaningful spend at enough frequency from cold campaigns. Source S02. S07 runs retargeting broad with at most a purchaser exclusion. S01 (TikTok) builds a 30-day web-visitor retargeting campaign from about $3,000 budget. Keep both. [ccf942b9f2c8] [32581af3f424] [ab880cedcc94]

**R77. Size existing-customer spend in dollars and frequency, never as a percentage.** Condition: monthly budget = customers x (CPM ÷ 1,000) x desired monthly frequency; card example 50,000 x ($10 ÷ 1,000) x 2 = $1,000 a month. Keep frequency below 7 per 30 days. Ask whether the next $10 or $1,000 a day pays back. Re-derive when customer count or CPM changes. Only run it when repeat purchase is expected (supplements yes, furniture no). Source S02. `[needs brand data: customer count, retargeting CPM, repeat rate]` [3a48f7471999] [9d8a9963309a] [4b24c60d9321] [ccf942b9f2c8]

**R78. Hold existing-customer spend in 1 dedicated campaign so it cannot bleed into cold.** Condition: any account targeting existing customers. Source S03; S02 template agrees. [b8a436d33e2f] [ba414cee7839]

**R79. Do not hyper-segment retargeting by add to cart, checkout, page or category, or by warmth tier.** Condition: S02 says the CPM increase never pays back the conversion-rate gain. Fashion: new arrivals and DPA can be 2 ad sets in the existing-customer campaign so DPA does not take everything (S02 Brand B). [028483f1e7af] [49146dda7d03]

**R80. Retarget non-buyers with a different offer or product, an objection-handling ad, or proof, not the same ad louder.** Condition: more than 1 product or offer. Source S09 (lead-gen origin; swap phone research for surveys). S06: product-aware needs proof, risk reversal, offer clarity; most-aware needs a reason to act now and a DPA can be enough. [5dff147cb0c0] [04071060afad]

**R81. DPA ROAS mirrors top-of-funnel spend; read it on 7-day click or incremental, keep it out of the cold CBO, and never cut prospecting because DPAs "hold up performance".** Condition: any account with catalog ads. S02: furniture DPA 7x shown, 1.9x on 7-day click and incremental, holding 57% of cold budget; 6 fashion brands at about 80% DPA share declining for 6 months (death spiral). S03: 70% DPA share is too much. Supports: S02, S03. [cf36e5f30572] [805594665ccc] [1589854e06d9] [278c94b0c456]

### Group M. Settings hygiene

**R82. Flexible ads off, unless forced by page caps, and then only with near-identical assets.** Condition: you cannot read which asset drove results, cropping is uncontrolled, and Meta may build a carousel the client never approved. Source S02. `[verify UI: current name of flexible ads]` [e323039d800f]

**R83. Advantage+ creative optimisations off at 2 levels: per ad, and in advertiser settings where automated rules switch them back on.** Condition: every launch; recheck recently launched ads. Source S02. `[verify UI: advertiser settings path]` [04cf2865b996]

**R84. Define audience segments (new, engaged, existing) in advertiser settings and check the customer sync on a schedule.** Condition: the Klaviyo to Meta sync breaks periodically; then existing customers get served as new. Without the definitions the audience breakdown and frequency reads do not exist. Supports: S02, S03. `[verify UI]` [d74e033578c8] [ccf942b9f2c8] [b025c790c4ac]

**R85. Before drawing a creative conclusion from a number that looks too good, check the attribution window and the audience segment.** Condition: any standout ROAS. Supports: S02, S10, S03. [fb9db4eb1b28] [04f6f0b93295] [8c6833a8cd30] [378c1eb72ff9]

**R86. Plan pages before hitting the live-ad cap: duplicate brand pages, partnership ads and brand-owned third-party pages, regional pages.** Condition: high creative volume or multi-country. Cap about 300 to 500 live ads per page `[web check]`. S02 would run all 3 together (example: Gruns runs about 15 pages). Note S02's "whitelisting" means a brand-made third-party page, not a creator handle. [8494f59ad41f] [63e75994772f]

### Group N. Audits

**R87. An audit names the 1 constraint on profitable growth and ranks fixes by commercial impact into a 90-day roadmap. It is not 40 screenshots of settings errors.** Condition: every audit. Refuse to audit on platform data alone; get backend access first. Source S03. [ce4264077b22] [3b7f250f224e]

**R88. Audit top-down: business numbers, then platform, campaign, ad set, ad.** Condition: every audit. Start at Shopify revenue, new-customer revenue, CAC; name the problem type; find the platform; then drill. Review the whole account at once, not 1 campaign. Supports: S03, S02. [f547d41f4dd4] [092e8775c5e9]

**R89. Structure review: list every campaign, write its 1-line defendable purpose, error-check against that purpose, cut or merge what cannot be defended. Often half cannot.** Condition: every audit. Then 4 checks: 30-day frequency by segment; attribution consistency; a methodical testing structure exists; settings errors (segments not defined, app rewards, legacy targeting, missing exclusions, names that lie). Naming that does not match settings is the most common finding. Source S03; S02 and S08 agree. [5ce17b008587] [b8a436d33e2f] [451238284cae] [b025c790c4ac] [36f63e27c6d5] [e336ef61445a]

**R90. Creative review: exactly 1 bottleneck at a time, in order volume, diversity, quality.** Condition: volume = new ads per month vs spend ÷ $1,000 (R40); diversity = concepts total and winning vs band (R41); quality = read scripts and watch ads with direct-response judgment (no SOP given; hand to 10-MCR). Bonus checks: DPA share, winners analysed and replicated, a production system with a feedback loop. Source S03. [3ecc8cc48319] [ea5e41f9a967] [45c43e3ff759] [7a6be5942fff] [458dbfdbdf45]

**R91. Validate any structure with 4 questions: readable data, matches how the business makes money, right for spend tier and creative throughput, support layers sized to real retention.** Condition: any "no" means restructure. Source S02; S08's 2 tests overlap. [3da640845924] [e336ef61445a]

### Group O. TikTok: setup and in-feed structure

**R92. Complete the account before spending: business info, documents, card on file, automatic payments, backup payment method, audience controls, brand safety hub (standard inventory), account health good or excellent.** Condition: every new TikTok advertiser. Business Center for anyone with more than 1 user; 2-step auth and allowed email domain. Supports: S01, S05. S05's claim that business-domain emails get better approval is unverified `[web check]`. `[verify UI]` [bbb344647f7f] [fe05eddfed67] [4204465b105f]

**R93. No pixel, no spend. Install via the official TikTok for Shopify app (developer TikTok Inc.) or partner integration, then test every event (page view, view content, add to cart, initiate checkout, complete payment) with Pixel Helper or Test Events before launch.** Condition: if purchase or add to cart does not fire, stop. Supports: S01, S05. `[verify UI]` `[web check: consent rules before choosing "maximum" data sharing]` [837875464f88] [41b98e976611]

**R94. Objective Sales (web conversions), destination Website, manual campaign not Smart+ at first, advanced view, campaign catalog off, split test off, CBO off while testing.** Condition: first in-feed campaign for a store. Smart+ as a later parallel test ("mixed results", S01). S05: toggle off smart campaigns. `[verify UI]` `[web check: current Smart+ defaults and names]` [f6953a15849d] [097d6ce5e477] [479be1c347e0] [0856c5eb5224]

**R95. Ad group: optimise for Complete Payment on the pixel, placements TikTok only or automatic with a placement read later, targeting broad (country, language, 18+), continuous schedule, no target CPA on a new account, attribution windows default, conversions not value.** Condition: first launch. S01 uses automatic placements and says TikTok placement usually wins; S05 unticks everything but TikTok. Either way, read the placement breakdown and opt out of weak ones. `[verify UI]` [b9a9580d6fee] [e413ec2ddfd9] [e9592c1f1fb3]

**R96. Broad first on TikTok; interests only as a test ad group with 2 to 5 broad parent categories; never 15 to 20 stacked interests; behaviours sparingly.** Condition: S05 fashion case: 15+ interests gave CPA above 100, 1 broad category gave 34 to 41 (currency unclear). S01 adds 3 to 5 interests in a second ad group with the same ads. Supports: S01, S05. [b9a9580d6fee] [ce98eaba5aeb] [43139284c6a4]

**R97. TikTok daily budget floor: $20 a day is the platform minimum; sources want $50 a day per ad group (S05) or 2x current CPA per day, about $50 if CPA unknown (S01). TikTok's own advice is 10x CPA. Learning phase exits at 25 results or 7 days.** Condition: S01's 2x CPA buys about 14 results in 7 days, not 25; reaching 25 needs about 3.6x CPA. Agent default: max($50, 2x CPA) per ad group; raise toward 3.6x CPA if the learning read matters. Conflict: see 7.12. `[needs brand data: current TikTok CPA]` [e413ec2ddfd9] [153cd8af7351] [d3b3e82930e5]

**R98. Structure grows with budget: at about $20 a day, 1 Prospecting campaign, 1 broad ad group, 3 ads; above that add an interest ad group with the same 3 to 5 ads; no more than 4 ad groups per campaign; a winner moves to a CBO scaling campaign.** Condition: S01. S05: 1 campaign, up to 8 ad groups each testing 1 thing, never all budget in 1 ad group. Build all ads in the first ad group before duplicating. [b9a9580d6fee] [479be1c347e0] [43139284c6a4] [832a0215542d]

**R99. TikTok first test: 2 ad groups x 3 very different creatives x at least $50 a day x 3 to 4 days ($300 to $400). Do not touch anything before $50 spend or 1,000 impressions per ad.** Condition: S05. Read at 24 hours on soft metrics and at 3 days on cost metrics (section 6). $50 is a floor for CTR, CPM and watch-time reads, not for purchases. [d3b3e82930e5] [75aa9cb13f3d] [78428f27caf0]

**R100. TikTok lookalikes are still in use: seed from purchasers or 180-day visitors, size balanced for large countries and broad for small; do not target custom audiences directly in prospecting.** Condition: S05 practice; S01 builds a balanced lookalike from 30-day purchasers. This contrasts with the Meta rule (R24). Keep them platform-specific. `[verify UI]` [f10b4c010429] [1ee708d070fe]

**R101. Move a winning TikTok creative into a separate CBO scaling campaign; keep testing in the manual campaign.** Condition: S01. No step size or pacing given; borrow Meta pacing (R45, R51) with the TikTok learning threshold in mind. [b9a9580d6fee] [479be1c347e0]

### Group P. TikTok: Spark, Search, Shop, GMV Max, retargeting

**R102. Post organically first, wait 5 to 7 days, then Spark the winners.** Condition: any content you or creators can post. A post shows within 2 days if it is taking off and has about a 1-week life. At scale post 20, boost the top 10% to 30%. Ask creators for a 365-day authorization code. Spark Ads keep likes and comments and are said to have higher CTR and lower CPA (presenter claim). Source S01. `[verify UI]` [260e5915e605] [8e7a9a972f04] [15b3e91bb766] [cd344df6562d] [a388b241a299]

**R103. Search campaigns: 20 to 50 keywords from Keyword Planner, phrase match, automated keywords off at launch, review search terms after a couple of days and add negatives regularly; skip search if volume is negligible.** Condition: S01. `[verify UI]` [300e5d732f27] [3ae33f4363ac] [f5220429194f]

**R104. TikTok Shop: Seller Center with the same email as Shopify, official app sync, fill every red-starred field, seller shipping for most, fix listings below "good", check restricted categories, connect Shop to Business Center and to the TikTok profile.** Condition: markets where Shop is available `[web check: Shop and GMV Max availability]`. Source S01. `[verify UI]` [e65261264f64] [02f8e94e8978] [d7bbe2fbdade]

**R105. Affiliates: open collaboration with commission only on sales (example 20%), follower and GMV thresholds for free samples, target collaborations with custom rates, shop-ads commission about 5% (below standard because you also pay for the ads).** Condition: S01. Judge requesters on post rate and 30-day GMV. [f1578b0b61d9]

**R106. GMV Max: 1 campaign per product, start with the top 20% of SKUs by orders, ROI target = TikTok's suggestion + 1 (demo 1.2 to 2.2) and never below break-even, daily budget 2x target CPA, cut special promotion days to 50% and a 1x limit, auto-select creative on, boost winners at $10 a day minimum on top of budget.** Condition: S01. Lower the ROI target only if no impressions after a few days. TikTok's suggestion is often below break-even. Conflict: card 153cd8af7351 says set it low then raise; follow the transcript. `[needs brand data: break-even ROAS]` `[verify UI]` [3f9a7828109d] [c3654a90de4f] [153cd8af7351]

**R107. TikTok retargeting: web visitors 30 days excluding 30-day purchasers, auto refresh on, audience expansion off, reach-and-frequency off; audiences take about 24 hours to populate. Add at about $3,000 budget (period unstated), then 7-day non-buyers and 30-day add-to-cart as budget grows; at $10k+ add re-engagement and GMV Max.** Condition: S01. Audience expansion on "might as well be broad". `[verify UI]` [1ee708d070fe] [ab880cedcc94]

## 4. Procedures (implementation)

**Meta is read-only in ecomOS; propose, do not execute.** Every step below that changes a Meta or TikTok account is written as a proposal for a human operator. The agent reads, computes, drafts and hands over. Every platform step carries `[verify UI]` because menu names, defaults and limits in the sources are late 2025 to mid 2026 snapshots.

### P1. Design or restructure a Meta account (any tier)

Goal: a structure that passes R2 and R91, sized to spend tier and creative throughput.
Preconditions: inputs from section 2 (spend tier, categories, margins, personas, regions, new ads per month, conversions per campaign).
Steps:
1. Answer the 5 diagnostic questions: product categories and their goals; margin spread across categories `[needs brand data]`; non-overlapping personas; regions with own stock, targets or URLs `[needs brand data]`; creative throughput (10 a month vs 2,000) `[needs brand data]`. [b8107473f4c3]
2. Audit business complexity: core vs seasonal ranges, distinct demographics, concept winners you are overleveraged into `[needs brand data: spend share per concept]`. [52611fb24810]
3. Pick the tier template: under $50k (R10), $50k to $250k (R11), $250k plus (R12). Treat it as a starting point. [568f98fcc9aa] [7350eaba553e] [58966745d295]
4. Draft campaigns. For each, write the 1-line defendable purpose (R7). Merge any 2 that share a purpose. Check no campaign exists for tidiness (R16). [5ce17b008587]
5. Put segmentation at ad set level before adding campaigns, unless margin, persona or region force a campaign (R13). [ebff07a9e6f2]
6. Define concept ad sets (P2). Check each ad set's conversion volume can support a read in the window from R36. [7230fc5fab8f]
7. Decide ABO or CBO (R30 to R32) and record the reason. [2f66cf4f65c6]
8. Set attribution (7-day click, all campaigns) and existing-customer exclusion (2 years or repurchase cycle) on every cold campaign `[verify UI]` (P6). [fb9db4eb1b28] [cf3aa44a7de1]
9. Size retargeting and existing-customer spend (P7). Skip website-visitor retargeting unless 5.3 shows the engaged segment is starved. [ccf942b9f2c8]
10. Run the 4-question validation (R91). Any "no": go back to step 4. [3da640845924]
Checks after: every campaign has a purpose line; every ad set is 1 concept with 3+ ads; exclusions and attribution match on all cold campaigns; the audience segment breakdown will be readable (segments defined). [b025c790c4ac]
Rollback: keep the old structure live until the new one has 1 full read window; do not turn off winning ad sets to move them (R23, R50).

### P2. Build and name a concept ad set

Goal: 1 concept, 3 to 15 ads, readable name.
Preconditions: concept matrix (personas x angles x offers) from 10-MCR; the ads.
Steps:
1. Write the concept as persona + angle + offer (+ ad type). Example: coffee drinkers + whitening without sensitivity + product only + UGC. [65e0503d7bc4] [94c8e0f902f4]
2. Check no live ad set already holds this concept. If one does and it is hitting KPI, create a new ad set beside it (R23). If it is missing KPI, add the ads to it. [a95742238877]
3. Load 3 to 15 ads; for a new concept, the concept ad plus 3 hook variations (R19). All ads speak to the same persona. Top, middle and bottom funnel ads can share it (R21). [d6c0209e9d6b] [6ee9db26f236]
4. Targeting: broad; hard controls only (exclusions, minimum age, locations, languages) `[verify UI]`. [48728b3abcdf]
5. Name: persona, angle, offer, content type, launch date. Same convention across campaigns. [c910cbdcfaae]
6. Flexible ads off; Advantage+ creative optimisations off on each ad `[verify UI]`. [e323039d800f] [04cf2865b996]
Checks after 2 to 3 days: gender or age breakdown per ad `[verify UI]`; if ads serve to the wrong group the ad set is mixed, split it. [3e877cb4c991]
Rollback: pause the ad set; do not delete, so its history stays readable.

### P3. Launch a Meta creative test and size it

Goal: a test whose end condition is decided before launch.
Preconditions: target CPA or ROAS from margin `[needs brand data]`; concept ad sets built (P2); testing campaign excludes existing customers and runs 7-day click.
Steps:
1. Pick the sizing method. Method 1 (kill rule): threshold spend = 3x target CPA per concept ad set (5x if the owner accepts more spend for a cleaner read). Method 2 (formula): daily budget = (target conversions x expected CPA) ÷ test days; example 20 x $100 ÷ 14 = about $143 a day. Write the number down. [87a85788a663] [1c683e007b76]
2. Set duration from R36: default 7 days; 3 to 4 days only for large stable brands with short purchase cycles; 10 to 14 days for tiny budgets, long cycles or strong weekday swings `[needs brand data: revenue by weekday, time to purchase]`. Never under 5 days below $50k a month. [f88304f4647b] [b8a2663f518f]
3. Write the decision table before launch: keep, kill, extend, scale, and the numbers that trigger each (R44). [1c683e007b76]
4. Propose ad set budgets (ABO) or campaign budget with ad set minimums (CBO) `[verify UI]`. Do not derive budgets from the 50-conversions-in-7-days learning rule. [1c683e007b76]
5. Log the test in the test plan deliverable (section 9) with concept, ad ids, budget, start, planned read date. Note the launch weekday. [f88304f4647b]
Checks during: no edits before the read date except a broken link or policy rejection. Daily swings under about $1,000 a day are normal (R36). [c8f9d9634c5f]
Rollback: if a test must stop early (budget cut, stock out), mark it "inconclusive", not "lost".

### P4. Read a test and produce the kill, keep, scale list

Goal: an ad set level decision list with reasons.
Preconditions: the read date from P3 has arrived; audience segments and attribution columns available.
Steps:
1. Pull ad set spend, conversions, CPA or ROAS on 7-day click for the full window. Ignore 1-day view `[verify UI]`. [04f6f0b93295]
2. For each ad set apply the decision table. Method 1 at 3x CPA: 3 to 4 conversions keep, 2 yellow (extend about 1 CPA of spend), 0 to 1 kill. At 5x: yes or no. Method 2: at or better than target over the window keep, else kill unless a stated reason (seasonality, tracking outage) says extend. [87a85788a663]
3. For any ad set at KPI: propose a budget raise (about 20% a day at the small tier; larger steps allowed if the owner accepts the lag, R51). Do not add new creative to it (R23). [b8a2663f518f] [eff64339b5de]
4. For any ad set at KPI, sort ads by spend and list the 2 to 4 that take spend as the "make more like this" brief for 10-MCR. Do not move budget on ad-level ROAS (R42, R43). [ab729ba34368]
5. For any ad set missing KPI after enough spend: state what the creative got wrong (stage mismatch, weak hook, wrong persona), propose new ads into it or retire it. [b8a2663f518f] [8a649c8f4785]
6. Before calling any ad set a winner to scale, run P8 on its top ad (new-customer ROAS on 7-day click). [8c6833a8cd30]
7. Sanity checks: attribution window used, audience segment (existing near 0% in cold), frequency (R71), launch weekday effect. [fb9db4eb1b28]
8. Write the kill, keep, scale list (section 9 format) with the number that triggered each call.
Rollback: a "kill" is a pause proposal. Keep the ad set for history.

### P5. Scale a winner: equilibrium, fork, scaling campaign

Goal: more spend on a proven concept without breaking it.
Preconditions: an ad set well above target with strong soft metrics for at least 1 full read window; P8 passed.
Steps:
1. Raise the ad set budget in steps (about 20% a day at the small tier; more if accepted). Hold each step for the read window. [b8a2663f518f] [eff64339b5de]
2. When ROAS turns unprofitable, propose pulling back to the last good level. Repeat until the level where results hold is found. Record it as the creative's capacity (example $300 a day). [0e642b4c3a8c]
3. New creative for the concept: fork into a new ad set beside the winner (R23). [a95742238877]
4. If the winner's capacity is about $400 a day or more, propose a scaling campaign: CBO, 1 ad set, same post IDs, existing customers excluded, KPI at campaign level, no tests inside. Keep the original ad set running. Expect about +20% daily spend on a good day, not a promise. Refresh top post IDs every 1 to 2 weeks at large spend `[verify UI: use existing post IDs]`. [0e642b4c3a8c] [a95742238877] [b8a2663f518f]
5. Under about $60 a day capacity, skip the scaling campaign and fix ad, page, offer or concept instead. [0e642b4c3a8c]
6. Decide double down vs cap (R47, R53): shift creative volume toward the winner (S08 example 120 vs 40) or cap the winning ad set's share (S08 example 40%) and rotate new concepts in `[verify UI: ad set spend limits]`. Check the concept's LTV first `[needs brand data]`. [477d8f00df92] [99cd67e7cbac]
7. Measure the scale-up on store-side new-customer sales of the scaled SKU (R54) `[needs brand data]`. [b410bffcb50f]
Rollback: if ROAS and new-customer SKU sales both fall after a step, return to the recorded capacity.

### P6. Set attribution, exclusions and settings hygiene (proposal)

Goal: consistent 7-day click, existing customers out of cold, creative settings under control.
Preconditions: customer file synced (Klaviyo to Meta) `[needs brand data]`; audience segments defined.
Steps:
1. Attribution setting: 7-day click on every campaign; 1-day view off for optimisation and for budget decisions `[verify UI]`. [de104cfb484c] [04f6f0b93295]
2. Add "compare attribution settings" columns: 7-day click, 7-day click + 1-day view (and 1-day engaged view where offered), incremental attribution, as read-only comparison `[verify UI]`. [378c1eb72ff9] [de104cfb484c]
3. Audience segments: define new, engaged, existing in advertiser settings; confirm the existing-customer source and its last sync `[verify UI]`. [ccf942b9f2c8] [d74e033578c8]
4. Exclusions: existing customers excluded on every cold campaign (testing and scaling), window 2 years or the brand's repurchase cycle; optional lapsed-customer campaign for older buyers `[verify UI]` `[web check: Advantage+ existing-customer controls]`. [cf3aa44a7de1] [fb9db4eb1b28]
5. Flexible ads off `[verify UI]`. [e323039d800f]
6. Advantage+ creative optimisations off per ad and in advertiser settings, creative sub-dropdown, automated rules `[verify UI]`. [04cf2865b996]
7. Placements: remove Audience Network app rewards from any store or engaged-view campaign `[verify UI]`. [b025c790c4ac]
8. Legacy targeting: list ad sets with interests or lookalikes on purchase objectives; propose broad. [b025c790c4ac]
9. Naming: rename ad sets and campaigns so names match settings and creative. [36f63e27c6d5] [c910cbdcfaae]
Checks after: audience breakdown shows existing near 0% in cold; recently launched ads still have optimisations off after 2 weeks. [04cf2865b996]
Rollback: attribution changes alter which ads win spend; re-read rankings after 1 window before any kill (S10 card step). [9759cdb709fb]

### P7. Size retargeting and existing-customer budgets

Goal: dollar and frequency-based support layer.
Preconditions: customer count, retargeting CPM, repeat purchase rate `[needs brand data]`.
Steps:
1. Decide if an existing-customer campaign is justified: repeat purchase expected (consumables, low AOV subscription) yes; one-off (furniture) no. [ccf942b9f2c8]
2. Monthly budget = customers x (CPM ÷ 1,000) x desired monthly frequency (below 7). Example 50,000 x ($10 ÷ 1,000) x 2 = $1,000 a month. [3a48f7471999]
3. Hold it in 1 dedicated campaign. Judge it on incremental attribution as a check and on 30-day frequency `[verify UI]`. [b8a436d33e2f] [cf36e5f30572]
4. Website-visitor retargeting: only if the audience breakdown shows engaged starved of spend in cold. If run, consolidate audiences; no add-to-cart, checkout or page splits. [ccf942b9f2c8] [028483f1e7af]
5. DPA: keep out of the cold CBO; its own ad set inside the existing-customer campaign (with a new-arrivals ad set beside it in fashion); watch DPA share of total spend (70% to 80% is a death-spiral signal). [805594665ccc] [278c94b0c456] [49146dda7d03]
6. Re-derive monthly. Ask if the next $10 or $1,000 a day pays back. [9d8a9963309a]
Checks: existing frequency below 7 per 30 days; retargeting share of spend well below the about 50% audit red flag. [028483f1e7af]

### P8. Diagnose a top-spending TOF ad (new-customer profitability)

Goal: know whether a "winner" acquires new customers.
Preconditions: audience segments defined; comparison columns available; ad-level report `[needs brand data]`.
Steps:
1. Open the campaign at ad level, sort by spend, note the top ad's ROAS and frequency. Frequency that looks high for a cold ad is the first flag. [8c6833a8cd30]
2. Breakdown by audience segment (existing, engaged, new) `[verify UI]`. Read the share of spend on existing (S10 example: about half). [8c6833a8cd30]
3. Read new-segment ROAS (example 13x blended, about 5x new). A large gap means spend is pulled by existing-customer performance. [8c6833a8cd30]
4. Keep the split and open Columns > Compare attribution settings; add 7-day click and incremental `[verify UI]`. Read the new row under incremental (example 1.71x). [de104cfb484c]
5. Check the ad set's attribution setting. If 7-day click + 1-day view, mark all rankings in that ad set untrustworthy. [34a82c492fd6]
6. Decision: do not scale or brief more of this ad until P6 is applied and rankings re-read; if the new-customer 7-day-click ROAS clears target, it is a real winner. [34a82c492fd6]
7. Record blended, new-segment and incremental ROAS in the diagnosis memo. [8c6833a8cd30]
Rollback: none; read-only.

### P9. Run a full account audit

Goal: 1 named constraint, ranked 90-day roadmap.
Preconditions: backend access (Shopify or Metabase orders with new vs returning flag, P&L with gross margin) and platform read access. Without backend data, stop and request it. [3b7f250f224e]
Steps:
1. Cohort model, monthly, 2 to 2.5 years: CAC, first-purchase GP (AOV x monthly margin, or Shopify COGS), GP to CAC, new-customer count. Graph. Read the last 6 months. Score against R60 bands. [96ddc2d014f8] [021224f4073c]
2. Normalized P&L to contribution margin (gross revenue, minus refunds, discounts, plus shipping collected, minus COGS, fulfilment, fees, minus marketing). Check whether contribution margin fell when spend rose. [9cb9b9fec95a]
3. First-time-customer P&L and aMER = new-customer revenue ÷ ad spend. Compare to blended. [04bd5299ca53]
4. Reconcile each platform's ROAS with aMER (P18). Big gap: data integrity is the number 1 bottleneck. [378c1eb72ff9] [7101da7d331d]
5. Retention layer: GP cohort growth by day 90, 180, 365 vs category benchmarks `[needs brand data]` `[web check]`; adjust CAC tolerance. [cb04728e9c8a]
6. Structure review (R89): campaign purpose sheet, frequency by segment, attribution consistency, testing structure, settings errors, naming vs reality. Include the structure audit checklist 5.4. [5ce17b008587] [b025c790c4ac]
7. Creative review (R90): volume vs spend ÷ $1,000, concept counts vs band, quality read; pick 1 bottleneck. DPA share. Winner replication. Production system. [ea5e41f9a967] [45c43e3ff759] [3ecc8cc48319]
8. Drill from business number to platform to campaign to ad set to ad for the named problem. [f547d41f4dd4]
9. Sequence: data integrity fixes first (quickest), structure second, creative third (slowest, largest). [7101da7d331d]
10. Deliver the diagnosis memo (section 9): constraint, proof, ranked roadmap, what needs a human to apply, what needs a test. S03 delivers as a 1 to 1.5 hour narrated recording; ecomOS delivers a memo plus the JSON proposal. [ce4264077b22]

### P10. Zombie ad set for CBO-starved ads (optional, S09 only)

Goal: force delivery on ads the CBO ignored.
Preconditions: a CBO has run a full window; a list of 0-spend ads. This is 1 presenter's tactic and conflicts with trusting allocation (R28); use only with a hard budget cap and a log.
Steps:
1. List ads with 0 or near-0 spend after the window. [841a1ded8706]
2. Keep only those with a written reason for high conviction. [841a1ded8706]
3. Propose a separate ad set with its own small budget (no amount given by the source; set it from R35 Method 1 at 3x CPA) `[verify UI]`. [841a1ded8706]
4. Read after the R36 window. Move winners into the concept structure (card inference). Log the hit rate; S09 claims about 20%. [841a1ded8706]

### P11. TikTok account, Business Center and pixel

Goal: a launch-ready TikTok account with tested events.
Steps (all `[verify UI]`):
1. Create the ads account with a business email; region, currency, time zone correct; read any credit offer terms `[web check: current offer]`. [bbb344647f7f] [4204465b105f]
2. Tools > Account setup: address, documents (upload anything requested), payment type automatic, credit card, plus a backup method. [bbb344647f7f] [4204465b105f]
3. Audience controls: default location, minimum age 18. Brand safety hub: standard inventory, apply to all objectives; exclude categories as needed. [bbb344647f7f]
4. Business Center: users and roles, link the ad account, link the TikTok account by QR code with "show as ad only", link the Shop if any, 2-step auth, allowed email domain. Confirm Assets shows the TikTok account under the ad account. [fe05eddfed67] [cd344df6562d]
5. Pixel: Events Manager > Web > Shopify; install the official TikTok app (developer TikTok Inc.); "TikTok Ads setup"; match the Business Center and ad account in each dropdown; data sharing level after checking consent rules `[web check]`. [837875464f88] [41b98e976611]
6. Test events with Pixel Helper or Test Events: page view, view content, add to cart, initiate checkout, complete payment. If purchase or add to cart does not fire, stop. [837875464f88]
7. Account health: good or excellent; clear notifications. [bbb344647f7f]
Checks: run 5.5 before any spend.

### P12. TikTok in-feed Sales campaign to a website

Goal: first prospecting campaign with a clean test structure.
Preconditions: P11 done; 3 to 5 very different creatives (10-MCR).
Steps (all `[verify UI]`):
1. Campaigns > Create > advanced view. Objective Sales. Destination Website. Manual (not Smart+). Catalog off. Special categories only if housing, employment or credit. Split test off. CBO off. Name "Prospecting" or product + objective + date. [f6953a15849d] [097d6ce5e477] [0856c5eb5224]
2. Ad group 1: optimisation website conversion, pixel, event Complete Payment (if missing, fix pixel). Placements: TikTok only, or automatic with a placement read after 1 week. Targeting broad: country, language, 18+, all spending power, all income, all devices. No audiences. [b9a9580d6fee] [e9592c1f1fb3]
3. Budget: max($50, 2x current CPA) a day; $20 is the platform floor. Continuous schedule, all day. Target CPA blank. Attribution windows default. Optimisation conversions, not value. [e413ec2ddfd9] [e9592c1f1fb3]
4. Ads: upload 3 to 5 videos or pick TikTok posts (Spark). Music sharing off. Several CTA options. Product tagging off unless Shop. Destination URL (UTMs auto). Confirm music rights. Ad library checkbox per policy `[web check: opt-out rules by region]`. [40f4521921d6]
5. Build all ads in ad group 1, then duplicate the ad group into the same campaign changing only the audience: interest ad group with 2 to 5 broad parent-category interests (or a purchase lookalike). Name "Broad [country]" and "Interest [country]". Keep total ad groups at 4 or fewer. [43139284c6a4] [ce98eaba5aeb] [f10b4c010429]
6. Publish. Do not touch for 3 to 4 days except for disapprovals. [d3b3e82930e5]
Checks: 5.5 launch check; then 24-hour and 3-day reads (section 6). [75aa9cb13f3d]
Rollback: pause ad groups, never delete.

### P13. TikTok first test read (24 hours, 3 days)

Goal: separate creative problems from audience problems, then cut the bottom half.
Preconditions: each ad has at least $50 spend or 1,000 impressions. [75aa9cb13f3d]
Steps:
1. At 24 hours: CTR above 1% good, below 1% creative problem (new hook and transitions); watch time above 25% good, below 20% hook problem (vary first 3 seconds); CPM under $15 good, above $20 audience problem (adjust targeting) `[web check: current CPM by market]`. [78428f27caf0]
2. At 3 days: CPC under $2, cost per add to cart under $10, cost per purchase under $30 (S05 US heuristics; replace with the brand's allowable CPA `[needs brand data]`). [75aa9cb13f3d]
3. Kill the bottom 50% of ads by the brand's cost metric; keep the top half; brief new variations of winners. Source S05 does not define "double down"; use max($50, 2x CPA) budget steps and re-read after 3 to 4 days. [75aa9cb13f3d]
4. Compare broad vs interest ad groups on the same ads. No clear difference: keep broad. [b9a9580d6fee]
5. After 1 week, read the placement breakdown; opt out of weak placements. [b9a9580d6fee]
6. Check learning: 25 results in 7 days. If far off, raise toward 3.6x CPA a day or accept slow learning. [e413ec2ddfd9]
7. Reconcile TikTok-reported purchases with store orders before believing the CPA `[needs brand data]`. [378c1eb72ff9]

### P14. Spark Ads (own post and creator post)

Steps (all `[verify UI]`):
1. Post 3 or more videos (own account or creators). Wait 5 to 7 days. Pick winners by sales, follows or engagement. [260e5915e605] [8e7a9a972f04]
2. Own post: in the ad, Creative > TikTok post > pick account > select post. If posts do not show, the account is not linked (P11 step 4). [cd344df6562d]
3. Creator post: ask the creator for a code: video > three dots > ad settings > ad authorization on > duration 365 days > authorize > manage code > copy. Paste it under "add post". Set destination URL to your page. [15b3e91bb766]
4. Engagement flows both ways between ad and post. [a388b241a299]

### P15. TikTok Search campaign

Steps (all `[verify UI]`):
1. Tools > Keyword Planner: product term > Discover; set area; low competition first, then all; 20 to 50 keywords; save the plan. Skip search if total volume is negligible. [300e5d732f27]
2. Create > Sales > Search. Name "Prospecting search". Location, pixel, Complete Payment, target CPA blank. Import the saved plan. Select all > match type phrase. Automated keywords off. Budget at least $20 a day. [3ae33f4363ac]
3. Ad: URL; video, TikTok post or recommended posts. Product-specific terms in their own ad groups. [3ae33f4363ac]
4. After a couple of days: ad group > View data > Search terms; add negatives. Repeat regularly. [f5220429194f]

### P16. TikTok Shop, affiliates and GMV Max

Steps (all `[verify UI]`, market availability `[web check]`):
1. Seller Center with the same email as Shopify; business documents; pickup and return warehouses; returns and tax. [02f8e94e8978]
2. Products: "TikTok for Shopify" official app > Start selling on TikTok > connect; seller shipping for most; fill red-starred fields; check restricted categories; fix listing quality to "good"; confirm live via TikTok search > Shop tab; connect Shop to Business Center and profile. [02f8e94e8978] [d7bbe2fbdade] [e65261264f64]
3. Affiliates: open collaboration (commission example 20%, sample thresholds by followers and GMV); target collaboration (custom rates, shop-ads commission about 5%); review requesters by post rate and 30-day GMV. [f1578b0b61d9]
4. GMV Max: Campaigns > Sales > TikTok Shop > GMV Max; pick the Shop; Promote products; uncheck all products; add the top 20% by historical orders; ROI target = suggestion + 1 and not below break-even `[needs brand data]`; daily budget 2x target CPA; special promotion days 50% and 1x; creative auto-select on; publish. [3f9a7828109d]
5. Monitor: analytics > view creative (in queue, learning, delivering, not delivering); boost a strong video at $10 a day minimum (adds to budget); Creatives tab for revenue per video and top creators. If no impressions after a few days, lower the ROI target 1 step. [c3654a90de4f] [3f9a7828109d]

### P17. TikTok retargeting audiences and campaign

Steps (all `[verify UI]`):
1. Audience manager > Custom audience > Website traffic: page view (or view content), pixel, last 30 days; exclude purchasers last 30 days; name "web visitors 30 days exclude"; auto refresh on; expansion off; reach and frequency off. Wait about 24 hours. [1ee708d070fe]
2. Optional lookalike: source = purchasers last 30 days (or 180 days per S05); balanced for large countries, broad for small. [1ee708d070fe] [f10b4c010429]
3. Campaign: Sales > Website; settings as P12 except audience: manual targeting > include the custom audience. Budget at least $20 a day; S01 adds retargeting at about a $3,000 budget (period unstated). [ab880cedcc94]
4. As budget grows: 7-day non-buyers, 30-day add-to-cart, special offers; at $10k+ add re-engagement (content engagers) and GMV Max. [ab880cedcc94]
5. Apply R75: retargeting is capped; judge by frequency and store-side incrementality, not platform ROAS.

### P18. Reconcile platform ROAS with acquisition MER

Steps:
1. aMER = new-customer revenue ÷ ad spend, monthly, from store data `[needs brand data]`. [04bd5299ca53]
2. Put each platform's account ROAS beside aMER. S03 example: aMER 3x to 7x, Meta 17x. [378c1eb72ff9]
3. Meta: Columns > compare attribution settings: 7-day click, 7-day click + 1-day engaged view, incremental `[verify UI]`. In 95% of accounts (S03 claim) the tighter numbers track aMER. Suspect existing-customer spend and 1-day view first. [378c1eb72ff9]
4. Choose: switch all campaigns to the setting that matches, or keep settings and always judge on the comparison column. [378c1eb72ff9]
5. TikTok and Pinterest: 7-day click column `[verify UI]`. [378c1eb72ff9]
6. Google: do not tighten; check brand vs non-brand separation (12-GAD). [89ab42bd67bc]
7. Still unreconciled: propose a Conversion Lift Test or geo-lift (about 25 days) via 06-MEA. [845571c9595b] [de104cfb484c]

## 5. Diagnostic checklists

### 5.1 Weekly account read (Meta)

| What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Window length | Pull 7 days and the largest spend window; 7-day click only | Decisions on 7+ days | Decision on 1 day or about $100 spend | Wait; zoom out | S07 [c8f9d9634c5f], S02 [b8a2663f518f] |
| Ad set vs KPI | Ad set CPA or ROAS vs target over the window | At or better | Below, after threshold spend (3x or 5x CPA) | Apply P4 decision table | S02 [87a85788a663] |
| Ad-level urges | Are you about to kill or scale a single ad on ROAS? | No; ad set is the unit | Yes | Stop; read the ad set; use spend share only for briefs | S08 [ab729ba34368], S02 [9ede69b02ec7] |
| Spend concentration | Share of spend on top ad set or concept `[needs brand data]` | Within chosen cap (S08 example 40%) or a deliberate double down | 1 concept carries almost all spend with no backup | Cap and rotate, or fund a pipeline | S08 [99cd67e7cbac], S09 [c61bad8559ba] |
| Existing customers in cold | Audience segment breakdown | Existing near 0% | Meaningful existing spend | Check exclusion and sync (P6) | S02 [ccf942b9f2c8], S10 [8c6833a8cd30] |
| Attribution basis | Compare 7-day click vs default columns | ROAS holds on 7-day click | Collapses without view-through | Do not scale that ad set; propose 7-day click | S10 [34a82c492fd6] |
| Frequency by segment | 30-day frequency new, engaged, existing | Existing below 7; engaged moderate | Existing 30+; engaged about 14 | Cut existing budget (P7); more top-funnel creative | S02 [9d8a9963309a], S03 [b8a436d33e2f] |
| Learning obsession | Are budgets set to hit 50 conversions in 7 days? | Budgets from P3 | Budgets from the learning rule | Reset per P3 | S02 [1c683e007b76], S07 [c8f9d9634c5f] |
| Creative settings drift | Recently launched ads: Advantage+ creative optimisations, flexible ads | Off | Turned back on | Propose off at both levels | S02 [04cf2865b996] |
| Creative volume this month | New ads vs spend ÷ $1,000 | At or near | Far below | Volume is the bottleneck; brief 10-MCR | S03 [ea5e41f9a967] |
| Platform vs store | Platform ROAS vs aMER or store period ROAS | Close | Wide gap | P18 | S03 [378c1eb72ff9] |
| Meta suggestions applied | List changes made from Ads Manager prompts | None, or tested and logged | Applied on projected uplift | Revert or test with a log | S07 [d9cba85df27b] |

### 5.2 Fatigue check

| What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Frequency trend on top ads | Ad-level frequency over 4 weeks `[needs brand data]` | Flat | Rising while cold reach is flat | Run the library stage audit below | S06 [7443b5bb8016], S04 [4de396baf031] |
| ROAS trend with frequency | Same ads, ROAS by week | Stable | Tapering as frequency rises | Brief a new concept, not an iteration | S04 [4de396baf031] |
| Cold reach vs budget | Reach on the new segment as budget rose | Reach grows | Flat reach, higher frequency | Creative mix, then exclusions | S06 [7443b5bb8016] |
| Library mix by stage | Tag each live ad: unaware, problem, solution, product, most aware; count | Roughly 80/10/10 or a data-based flex | Mostly product-aware or feature-led | Shift production up the stages (10-MCR) | S06 [b81e94d98fa2] [59dbcd6956ee] |
| Near-duplicate count | Count ads by persona x angle x offer, not by file | Many distinct concepts | Many near-duplicates | Cut duplicates; brief concepts | S04 [917ee36d87e9] |
| Narrow-persona saturation | Persona-callout ads: frequency and spend since launch | Below saturation | Frequency climbing after a few thousand dollars | New concept for a new cluster | S04 [4de396baf031] |
| Single-winner dependence | Share of spend on the top ad | Diversified | 1 ad carries the account | Clone into variants; keep concepts alive | S09 [c61bad8559ba], S07 [6ee9db26f236] |
| Existing-customer over-frequency | 30-day frequency on existing | Below 7 | 30 or 50 | Re-derive dollar budget (P7) | S02 [3a48f7471999] |
| Retention curve drops (video) | Video retention per ad `[verify UI]` | Gradual decline | Drops at product intro or CTA | Smooth the bridge (10-MCR) | S06 [84685cc67b36] |

### 5.3 New-customer profitability check

| What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Backend access | Orders with new vs returning flag, margin `[needs brand data]` | Available | Platform data only | Stop; get access | S03 [3b7f250f224e] |
| CAC trend | Spend ÷ new customers, monthly, 2 years | Flat or down with volume up | Up while volume flat | CAC is the scale bottleneck; drill down | S03 [96ddc2d014f8] |
| GP to CAC | First-purchase GP ÷ CAC | 2 to 3 | Below 1, or falling 6 months | Hold or pull back; fix economics or creative | S03 [021224f4073c] |
| Blended vs first-time P&L | Rebuild P&L without returning orders | Same story | Blended fine, first-time poor | Acquisition is weak; repeat revenue masks it | S03 [04bd5299ca53] |
| Contribution margin vs spend | Normalized P&L | Rising or stable as spend rises | Falling while spend rises | Find where scaling broke | S03 [9cb9b9fec95a] |
| Platform ROAS vs aMER | Side by side | Close | 3x to 7x vs 17x type gap | P18 | S03 [378c1eb72ff9] |
| Top ad on new segment | Audience breakdown ROAS, new row, 7-day click | Clears target | 13x blended vs 5x new vs 1.71x incremental type gap | Do not scale or brief it; P6 then re-read | S10 [8c6833a8cd30] |
| Existing-customer spend in TOF | Audience breakdown spend share | Near 0% | About half | Exclusion (2 years or cycle) | S10 [cf3aa44a7de1] |
| Scale-up result | New-customer SKU sales before vs after budget change `[needs brand data]` | Rise | No rise despite platform ROAS | Platform overstated; revert | S10 [b410bffcb50f] |
| Retention tolerance | GP cohort growth day 90, 180, 365 `[needs brand data]` | Strong; allows lower first-order GP to CAC | Weak; first order must be very profitable | Adjust CAC target | S03 [cb04728e9c8a] |
| Scaling stance | Owner's chosen target: GP to CAC band or near break-even with cash check | Written and agreed | Undefined | Decide before scaling | S03 [021224f4073c], S09 [259da0427eb7] |

### 5.4 Structure audit

| What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Campaign count and purpose | Sheet: campaign, 1-line purpose | Every campaign defendable; goal is 1 cold | Duplicates; objective swaps; "spend feels big" | Merge or cut | S03 [5ce17b008587], S02 [7230fc5fab8f] |
| Conversions per campaign | Monthly conversions by campaign | Well above 100 to 200 each, or few campaigns | About 25 each across 4 campaigns | Consolidate; segment at ad set | S02 [7230fc5fab8f] |
| Over-consolidation | Categories, margins, personas vs 1 campaign | Complexity matches structure | Multi-category, multi-persona brand in 1 Advantage+ campaign; DPA inside cold CBO | Add business-unit campaigns and concept ad sets; pull DPA out | S08 [52611fb24810], S02 [1589854e06d9] |
| Ad set basis | Read ad set names and contents | 1 concept each; persona, angle, offer, date names | Date batches; formats at scale; landing-page splits | Rebuild by concept | S08 [66c735ceb8ff] [a5c883d83f91], S02 [c910cbdcfaae] |
| Mixed personas | Gender or age breakdown per ad `[verify UI]` | Each ad serves its group | Men's ads to women and reverse | Split ad sets | S08 [3e877cb4c991], S02 [ebff07a9e6f2] |
| Ads per ad set | Count | 3 to 15 (up to 20 for reads) | 1 or 2; or 200 spanning concepts | Add variations or split | S02 [d6c0209e9d6b], S07 [6ee9db26f236] |
| Targeting | Ad set audience settings | Broad; exclusions, min age, locations, languages | Interests, lookalikes, worldwide, age bands as controls | Propose broad with hard controls | S04 [48728b3abcdf], S03 [b025c790c4ac] |
| Exclusions | Cold campaign audiences | Existing excluded on all cold | Missing on any cold campaign | P6 step 4 | S02 [fb9db4eb1b28] |
| Attribution | Setting per campaign | 7-day click everywhere | Mixed; 1-day view on | P6 steps 1 to 2 | S03 [451238284cae], S10 [de104cfb484c] |
| Segments defined | Advertiser settings | New, engaged, existing set and synced | Not set; sync broken | Define; fix sync | S02 [d74e033578c8], S03 [b025c790c4ac] |
| Retargeting share | Spend on existing plus engaged | Small, frequency-led | About 50% | Cap (P7) | S02 [028483f1e7af] |
| Retargeting splits | Ad set list | Consolidated | Add-to-cart, checkout, page, warmth tiers | Merge | S02 [028483f1e7af] |
| DPA share | Spend by campaign type | Small | 57% to 80% and declining account | Rebuild prospecting; read DPA on 7-day click | S02 [805594665ccc], S03 [278c94b0c456] |
| Testing structure | Where do new assets and products enter? | Methodical, readable | None; tests inside scaling | Build testing campaign; no tests in scaling | S03 [5ce17b008587], S02 [b8a2663f518f] |
| Scaling campaign | Contents and entry rule | Equilibrium winners at $400+ a day; exclusions on | $60 a day winners; tests inside; no exclusions | P5 | S02 [0e642b4c3a8c] |
| Placements | Placement breakdown `[verify UI]` | No app rewards spend | Store or engaged-view campaigns in app rewards | Remove | S03 [b025c790c4ac] |
| Naming vs reality | Compare names to targeting, objective, ads | Match | "Cold TOF" targeting existing with bottom-funnel ads | Rename; do not scale on its ROAS | S03 [36f63e27c6d5] |
| ABO or CBO fit | AOV, orders per day | ABO at high AOV low volume; otherwise by risk | CBO at $10k AOV and 5 orders a day | ABO | S02 [1589854e06d9] |
| Page cap headroom | Live ads per page vs about 300 to 500 `[web check]` | Headroom or page plan | Near cap, no plan | Page strategy (R86) | S02 [63e75994772f] |
| 4-question validation | R91 | 4 yes | Any no | Restructure | S02 [3da640845924] |

### 5.5 TikTok launch check

| What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Account setup | Tools > Account setup `[verify UI]` | Address, documents, card, automatic payments, backup method | Anything missing | Complete before launch | S01 [bbb344647f7f], S05 [4204465b105f] |
| Account health | Health page and notifications | Good or excellent, no warnings | Errors | Fix immediately | S01 [bbb344647f7f] |
| Business Center links | BC > ad account > Assets | TikTok account and Shop linked; users added | Posts missing in picker; Shop missing in GMV Max | Link assets | S01 [fe05eddfed67] |
| Pixel events | Pixel Helper or Test Events walk-through | All 5 events fire | Purchase or ATC missing | Do not launch Sales; fix install | S01 [837875464f88], S05 [41b98e976611] |
| Purchase event in ad group | Optimisation event dropdown | Complete Payment listed | Empty | Back to pixel | S01 [f6953a15849d] |
| Campaign type | Campaign settings | Sales, Website, Manual, advanced view, catalog off, CBO off | Smart+ or simplified view at first launch | Rebuild | S01 [097d6ce5e477], S05 [0856c5eb5224] |
| Ad group settings | Ad group | Broad, continuous, target CPA blank, conversions | Narrow interests, dayparting, target CPA on a new account | Reset | S01 [b9a9580d6fee] [e413ec2ddfd9], S05 [e9592c1f1fb3] |
| Budget | Per ad group | max($50, 2x CPA); at least $20 | Under $20 rejected; under $50 slow learning | Raise or accept slow learning | S01 [e413ec2ddfd9], S05 [d3b3e82930e5] |
| Ad count and diversity | Ads per ad group | 3 to 5, very different | 1 or 2, or near-identical | Add | S01 [43139284c6a4], S05 [d3b3e82930e5] |
| Ad settings | Ad level | Music sharing off; rights confirmed; CTAs set; UTMs | Uncleared music; sharing on | Fix | S01 [40f4521921d6] |
| Video spec | File | 9:16, 1080 x 1920, MP4, H.264, under size limit `[web check]` | Wrong ratio | Re-export | S05 [78d35b770fae] |
| Ad library opt-out | Ad checkbox | Set per regional rules `[web check]` | Unchecked by default without a decision | Decide | S01 [40f4521921d6] |
| Data sharing and consent | Shopify app setting | Level matches privacy policy and market law `[web check]` | "Maximum" with no policy check | Review | S01 [837875464f88] |
| Naming | Campaign, ad group, ad | product + objective + date; "Broad [country]" | Random | Rename | S05 [0856c5eb5224] |

### 5.6 GMV Max and Shop monitor

| What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Delivery | Impressions over first days | Delivering | None | Lower ROI target 1 step | S01 [3f9a7828109d] |
| ROI target vs margin | Target vs break-even `[needs brand data]` | At or above break-even | At TikTok's suggestion (often below break-even) | Raise | S01 [3f9a7828109d] |
| Spend vs budget | Special promotion days settings | Capped at 50% and 1x | Defaults letting spend jump far above budget | Cut | S01 [3f9a7828109d] |
| Creative statuses | Analytics > view creative | Delivering; boosts on winners | All "not delivering" | Recruit more creators; check listings | S01 [c3654a90de4f] |
| Listing quality | Seller Center products | Good or better | Fair | Improve listing | S01 [d7bbe2fbdade] |
| Seller to-do | Seller Center home | Clear | Violations, low stock, negative reviews | Resolve | S01 [d7bbe2fbdade] |
| Reconciliation | GMV Max revenue vs Shop orders `[needs brand data]` | Match | Gap | Read Shop data as truth | ecomOS rule |

## 6. Thresholds and benchmarks

Confidence: high = 3 or more sources agree; medium = 2 sources; low = 1 source or a worked example. All money figures are USD from the sources unless stated. `[needs brand data: convert to the brand's currency and spend level]`

| Item | Value | Condition | Source | Confidence |
|---|---|---|---|---|
| Spend tiers (Meta) | Under $50k; $50k to $250k; $250k plus a month | Structure templates | S02 | Low (1 source's frame) |
| Campaigns | Goal 1 cold; $1M to $5M a month accounts often 4 or 5 | Add only for business complexity | S03, S02, S04, S08 | High |
| Conversions per campaign | Improves past about 100 to 200 a month | Consolidation test | S02 | Low |
| Ad set segmentation effect | About 5% to 10% efficiency swing | Ad set level only | S02 | Low |
| Brands that can fully consolidate | About 10% | 1 campaign, 1 ad set | S02, S08 agrees in kind | Medium |
| Ads per ad set | Min 3; 3 to 15; 5 to 20 for reads; 1 concept + 3 variations | Concept ad sets | S02, S08, S07 | High |
| Exposures before purchase | 2 to 6 | Why min 3 ads | S02 | Low |
| Concept definition | Persona + angle + offer (+ format) | All | S02, S03, S04, S08, S07 | High |
| Format ad sets stop at | About $10,000 a month | New accounts only | S08 | Low |
| New ads per month | About 1 per $1,000 spend; 100 to 300 at $50k to $250k; diminishing above $1M | Volume check | S03, S02 | Medium |
| Concepts by band | Under $100k: 1 to 3; $100k to $500k: about 2 winning, 2 to 6 testing; above $500k: 3+ winning, 4 to 5 funnels | Diversity check | S03 | Low |
| Test threshold (kill rule) | 3x target CPA: 3 to 4 conv keep, 2 yellow, 0 to 1 cut; 5x: yes or no | Concept ad set | S02 | Low |
| Test budget (formula) | (target conv x CPA) ÷ days; example $143 a day | Any test | S02 | Low |
| Meta learning rule | 50 conv per 7 days (about $714 a day at $100 CPA); rejected for test sizing | Test budgets | S02, S07 reject; Meta states it `[web check]` | Medium (rejection) |
| Test duration | 1 week default; 3 to 4 days large stable; 10 to 14 days small or slow | Per business | S02 | Low |
| Minimum read window | 5 days under $50k a month; 7 days per S07; never 1 day | Any decision | S02, S07, S09 | High |
| Minimum spend before any read | Not $1 to $2 | Any ad | S08 | Low |
| Daily volatility normal | Under about $1,000 a day | Meta | S07 | Low |
| Budget step on winners | About 20% a day (S02); more than 20% is fine, dip is lag (S04) | Scaling | S02, S04 (conflict 7.1) | Medium, contested |
| Scaling campaign entry | Equilibrium winner, about $400 a day and up; not $60 a day; example trigger above 5x target | Meta | S02 | Low |
| Scaling campaign gain | About +20% daily spend on a good day | Per asset | S02 | Low |
| Scaling refresh | Top post IDs every 1 to 2 weeks | $750k a month example | S02 | Low |
| Winner cap | 40% max spend share (example) | Cap and rotate | S08 | Low |
| Double down volume | 120 vs 40 creatives (example) | Winner confirmed | S08 | Low |
| Zombie rescue hit rate | About 20% (claim) | CBO-starved ads | S09 | Low |
| Pareto | 20% of ads take 80% of spend | CBO | S02, S08 | Medium |
| Attribution for optimisation | 7-day click | All cold; S10 all campaigns | S02, S08, S10 | High |
| Attribution variant | 7-day click + 1-day engaged view | S03's go-to | S03 | Low |
| 1-day view | Off for decisions | Meta | S02, S10, S03 | High |
| Incremental attribution | Comparison column only | Meta | S10, S02 | Medium |
| Tight settings match aMER | 95% of accounts (claim) | Meta | S03 | Low |
| Existing-customer frequency | Below 7 per 30 days; 30 or 50 over-spend; 1 under-spend | Retargeting | S02 (S03 examples agree) | Medium |
| Engaged frequency example | About 14 = too much middle-funnel | Audit | S03 | Low |
| Retargeting share red flag | About 50% of spend on existing plus engaged | Audit | S02 | Low |
| Website-visitor campaign | Skip in about 90% of accounts | Meta | S02 | Low |
| Existing-customer budget | Customers x (CPM ÷ 1,000) x frequency per month | Monthly | S02 | Low |
| Exclusion window | 2 years; or repurchase cycle | Cold campaigns | S10 | Low |
| DPA share red flag | 57% to 80% (S02); 70% (S03) | Any account | S02, S03 | Medium |
| DPA honest read | 7x shown vs 1.9x on 7-day click or incremental (example) | Furniture audit | S02 | Low |
| TOF winner example | 12.84x blended; about 5x new; 1.71x new incremental; about half of spend on existing | 1 account | S10 | Low |
| GP to CAC bands | Below 1 losing; 1 to 2 hold; 2 to 3 scale; above 3 spend more | First purchase; retention moves bands | S03 | Low |
| aMER seen | About 3x to 7x at large retailers (illustration) | Not a target | S03 | Low |
| Cohort lookback | 2 to 2.5 years monthly | Audit | S03 | Low |
| Geo-lift length | About 25 days | 8 and 9 figure brands | S03 | Low |
| Lift test arithmetic | 10% holdout; 2% vs 1% = 1 point lift; 5x reads about 2.5x (hypothetical) | Explanation | S10 | Low |
| Cost or bid caps | Ignore under about $200k a month; diversify bidding above $250k | Meta | S02 | Low |
| Daily bid tweaks | About 5% for an hour a day; not worth it | Meta | S02, S08 | Medium |
| Media buying lift | 10% to 20% at $100k to $300k; 3% to 4% at $1M (tension noted) | Meta | S02 | Low |
| CPM inflation | About 20% to 30% a year | Meta | S02 | Low |
| Interest misassignment | About 30% (report cited, unsourced) | Historical | S02 | Low |
| Delivery pipeline time | About 200 ms | Meta | S04, S07 | Medium (Meta's figure as quoted) |
| Entity ID illustration | 200 ads read as 20 | Near-duplicates | S04 | Low |
| Narrow persona saturation | Maybe $10,000 spend | Specific callout ad | S04 | Low |
| Adaptive ranking lift | +3% conversions, +5% CTR (Meta claim) | Platform-wide | S04 | Low |
| Page ad cap | About 300 to 500 live ads `[web check]` | Per page | S02 | Low |
| Second account share | Might hold 10% of spend | $250k plus | S02 | Low |
| Creative stage mix | 80% unaware and problem aware, 10% solution, 10% product and most aware | Starting split | S06 | Low |
| TikTok minimum budget | $20 a day (platform); $50 a day per ad group (S05); 2x CPA, about $50 if unknown (S01); TikTok says 10x CPA | Ad group | S01, S05 | Medium (conflict 7.12) |
| TikTok learning exit | 25 results or 7 days | Campaign | S01 (TikTok's definition) | Low `[web check]` |
| TikTok first test | 2 ad groups x 3 ads x $50 x 3 to 4 days = $300 to $400 | New account | S05 | Low |
| TikTok minimum data per ad | $50 spend or 1,000 impressions | Before any change | S05 | Low |
| TikTok 24-hour reads | CTR above 1% good; watch time above 25% good, below 20% weak hook; CPM under $15 good, above $20 audience problem | US, undated | S05 | Low `[web check]` |
| TikTok 3-day reads | CPC under $2; cost per ATC under $10; CPA under $30 | US heuristics; replace with brand CPA | S05 | Low |
| TikTok cut rule | Kill bottom 50% of ads after 3 days | First test | S05 | Low |
| TikTok typical costs | CPM $3 to $10; CPC $0.17 to $1.00; CPV $0.01 to $0.07 | Undated, no country | S01 | Low `[web check]` |
| TikTok ad groups per campaign | No more than 4 (S01); up to 8 in S05's case | Testing | S01, S05 | Low, differ |
| TikTok interests | 2 to 5 broad parent categories; never 15 to 20 | Interest ad group | S01, S05 | Medium |
| TikTok lookalike size | Balanced large countries; broad small | Lookalikes | S05, S01 | Medium |
| TikTok retargeting window | 30-day visitors excluding 30-day buyers; S05 seeds 180-day visitors | Custom audiences | S01, S05 | Medium |
| TikTok retargeting entry | About $3,000 budget (period unstated) | Structure tier | S01 | Low |
| TikTok audience populate time | About 24 hours | New audience | S01 | Low |
| Spark timing | Post first; wait 5 to 7 days; first 2 days show lift-off; boost top 10% to 30% of 20 | Organic-first loop | S01 | Low |
| Spark authorization | 365 days | Creator code | S01 | Low |
| Search keywords | 20 to 50; phrase match; negatives after a couple of days | Search campaign | S01 | Low |
| GMV Max | Top 20% SKUs; ROI = suggestion + 1; budget 2x CPA; promo days 50% and 1x; boost $10 a day min; 1 campaign per product | Shop ads | S01 | Low |
| GMV Max example | $4,000 spend, about $12,000 revenue, about 3 ROAS, "not awesome" | Early account | S01 | Low |
| Affiliate commissions | Open example 20%; target 24% to 25%; shop-ads about 5% | Shop | S01 | Low |

## 7. Where sources disagree

**7.1 The 20% budget rule.** S02 raises winning ad sets about 20% a day at the small tier and reads over a rolling window of at least 5 days. S04 says the 20% cap is in no Meta documentation, its agency raises by more "all the time", and the dip after a raise is a lag while new people see several ads, not a learning reset. S07 adds that daily results under about $1,000 a day are noise anyway. What the agent should do: propose steps sized to the read window, not to a fixed percentage. Under $50k a month use about 20% a day as the default because the read windows are long and the downside of a bad raise is slow to see. Above that, larger steps are allowed when the owner accepts a 7-day lag before judging. Never judge a raise on same-day revenue. Log every raise with its date so the lag can be read. [b8a2663f518f] [eff64339b5de] [c8f9d9634c5f]

**7.2 1 ad set for all funnel stages vs stage-split (and consolidation vs Meta's own push).** S02: put top, middle and bottom funnel ads for 1 persona in 1 ad set, because humans misread a 2x and 6x split that is really 4x; splitting is fine only if you blend the numbers. S06: keep each concept to 1 awareness stage and group by concept; awareness-grouped ads self-select their audience, so product-aware ad sets will show high frequency and unaware ad sets low frequency, and that is expected. S08: 1 concept per ad set, and mixed personas in 1 ad set go broad. Meta's own guidance and many operators push 1 Advantage+ campaign; S08 calls that a terrible idea for any brand with real complexity and S02 says it fits about 10% of brands. What the agent should do: the ad set unit is the concept (persona + angle + offer). Inside 1 persona, funnel stages may share the ad set (S02) or be split by stage as separate concepts (S06); either is allowed, but any stage-split read must be blended to the persona level before a kill or scale call. Never split by launch date. Never run 1 campaign for a multi-category, multi-persona brand. [d6c0209e9d6b] [faa05bf3cff8] [94c8e0f902f4] [52611fb24810]

**7.3 Attribution window: 7-day click vs default, and where engaged view fits.** S02, S08 and S10 optimise and read on 7-day click and turn 1-day view off; S10 says on all campaigns. S03's go-to is 7-day click plus 1-day engaged view (definition recalled from memory: like, comment, share or 5+ seconds watched `[web check]`). Meta's default is 7-day click plus 1-day view and many guides keep it. S07 ignores Meta CPA entirely and uses third-party attribution. What the agent should do: propose 7-day click as the optimisation setting on all cold campaigns and use the same setting everywhere. Read 7-day click plus 1-day engaged view and incremental as comparison columns only. Never move budget on a 1-day view number. Reconcile all of it with aMER or store period ROAS before any scale call. [de104cfb484c] [04f6f0b93295] [451238284cae] [40de3bd68e44]

**7.4 Excluding existing customers vs caps vs "exclusions won't fix it".** S02, S03, S04 and S10 exclude existing customers from every cold campaign (S10: 2-year window, lapsed carve-out). Advantage+ offers a percentage spend cap instead; S02 says percentages are the wrong frame because they move with pool size and cold budget. S07 runs retargeting broad with at most 1 purchaser exclusion and does not stress exclusions elsewhere. S06 says adding website-visitor exclusions to force cold delivery will not work when the ads are product-aware; fix the creative mix. What the agent should do: exclude existing customers (purchasers) from all cold campaigns as a data-integrity rule, sized in dollars and frequency, not a percentage cap. Do not add website-visitor or engaged exclusions to cold campaigns as a fatigue fix; run the creative-stage audit (5.2) instead. When the audience breakdown shows existing spend in cold, fix the exclusion or the sync first; when it shows high frequency on the new segment with flat reach, fix the creative mix. [fb9db4eb1b28] [cf3aa44a7de1] [3a48f7471999] [32581af3f424] [7443b5bb8016]

**7.5 Lookalikes and interests: dead or not.** S02 ("shouldn't be in your account"), S03 (not in 99% of ecommerce purchase accounts), S04 (deprecated July 2025 `[web check]`; suggestions only) and S09 (broad beats stacking, test it over 7 days) say dead on Meta. S07 keeps them as a capped sandbox. On TikTok, S05 uses lookalikes from day 1 and a 4-week ladder ending in stacked audiences, and S01 builds a balanced purchaser lookalike and a 3-to-5 interest ad group. What the agent should do: on Meta, broad with hard controls by default; if a client insists, run S09's 7-day same-creative broad vs stack test with a stated minimum spend and conversion count, and cap the sandbox. On TikTok, broad first, then 1 interest ad group (2 to 5 parent categories) or 1 purchaser lookalike with the same ads as a controlled test; keep broad if no clear difference. Check the live status of these features before proposing them. [4c81bdf1685a] [b025c790c4ac] [066b6cc383fe] [9869e4293b51] [32581af3f424] [f10b4c010429] [b9a9580d6fee]

**7.6 EMQ and signal quality: lever or plumbing.** S04 calls clean signal a hidden lever that lowers CPMs (70 of 100 conversions tracked under-states your action rate) but calls paid server-side tools a "very small" unmeasurable lever. S07 calls EMQ overrated (9.8 to 9.9 with no visible profit link) yet still says to send good data via CAPI. What the agent should do: treat pixel plus CAPI and a healthy purchase EMQ as required plumbing (06-MEA owns setup), check EMQ and Meta-vs-backend purchase counts in every audit, and never promise a performance gain from raising EMQ. Do not buy server-side tools expecting a measurable jump. [74d3bc849c6b] [40de3bd68e44] [773fc35a99e9]

**7.7 Learning phase.** Meta says about 50 conversions in 7 days exits learning; TikTok says 25 results in 7 days. S02 rejects sizing budgets from the Meta rule (about $714 a day per ad set at $100 CPA). S07 says ads never stop learning and not to obsess over exiting. S01 tries to hit 25 in 7 days but its 2x CPA budget buys about 14. What the agent should do: size tests from target CPA and read window (P3), not from learning thresholds; note learning status as context; on TikTok, accept slow learning at low budgets or propose about 3.6x CPA a day if the owner wants the 25-in-7 read. [1c683e007b76] [c8f9d9634c5f] [e413ec2ddfd9] [153cd8af7351]

**7.8 Variations vs new concepts after Andromeda.** S04: near-identical ads collapse into 1 Entity ID; only concept diversity reaches net-new people; iterations are allowed but do not count as diversity. S03: diversity means concepts, not formats. S07: the "only net-new concepts" narrative is too simple; variations are still highly effective; 1 concept + 3 hook variations per ad set so a concept is not killed on 1 ad; but a variation of the account's top ad usually will not beat it. S09: clone a winner into hundreds of copy variants. What the agent should do: test every new concept with 3 to 4 variations inside its ad set (S07) so the concept read is fair; count diversity by concepts, not by ad files (S03, S04); expect variations of the current top ad to extend its life, not beat it; brief new concepts for net-new reach and when frequency rises. Do not let variant counts substitute for concept counts in the volume check (R40, R41). [917ee36d87e9] [6ee9db26f236] [45c43e3ff759] [c61bad8559ba]

**7.9 Ad-level ROAS as a signal.** S02, S08, S06 and S10 say ad-level ROAS is unreliable (last click vs multi-touch optimisation; unaware ads earn credit for others; view-through and existing customers inflate rankings) and the ad set is the decision unit. S08 uses spend share inside a winning ad set as a rough creative read. S05 and S09 rank single ads (kill bottom 50% at 3 days; find the winning ad and clone it). What the agent should do: on Meta, keep, kill and scale at the ad set level; use spend share inside an at-KPI ad set only to brief creative; never turn off a top spender because its own ROAS is low. On TikTok, where sources only give ad-level rules, apply S05's cut rule but on the brand's cost metric with a 7-day-click and store reconciliation first. Where 1 ad clearly dominates, run P8 before treating it as the model to copy. [ab729ba34368] [9ede69b02ec7] [7443b5bb8016] [34a82c492fd6] [75aa9cb13f3d]

**7.10 Test budget sizing: Meta's 50 conversions vs the sources' formulas.** Meta: 50 conversions in 7 days. S02 method 1: 3x or 5x target CPA per concept ad set, judged on 3 to 5 conversions. S02 method 2: chosen conversions (5, 10, 20) x CPA ÷ days. S05 (TikTok): $50 a day per ad group for 3 to 4 days, judged on soft metrics at 24 hours. S07: no numbers, just 7+ days. What the agent should do: default to S02 method 2 with the conversion count set by the owner's risk (10 to 20 for a scale decision, 3 to 5 for a first screen), cross-check that the resulting daily budget is at least 3x target CPA over the window, and write the end condition before launch. Use method 1 as the quick screen for many small concepts. Never set budgets from the 50-in-7 rule. [87a85788a663] [1c683e007b76] [d3b3e82930e5]

**7.11 Where new creative for an existing concept goes.** S02: if the concept's ad set hits KPI, do not touch it; fork a new ad set. S08: place each new ad into its matching concept ad set; never make batch ad sets. What the agent should do: both agree on no date-batch ad sets. Use S02's fork rule for winning ad sets (protect what works) and S08's placement rule for ad sets that are not yet at KPI. Name forks with the same concept fields plus the launch date so concept performance can be filtered across ad sets. [a95742238877] [66c735ceb8ff]

**7.12 TikTok minimum budget.** Platform floor $20 a day. S01: 2x current CPA, about $50 if unknown, $20 with a long learning phase if tight; TikTok's 10x CPA "not loved". S05: at least $50 a day per ad group or you never get data. What the agent should do: default max($50, 2x CPA) per ad group; 2 ad groups at launch; raise toward 3.6x CPA only if the learning read matters and the brand's allowable CPA supports it. [e413ec2ddfd9] [e9592c1f1fb3]

**7.13 Statics vs video for cold.** S09 would pick statics "all day" (cheaper, more per session, beat a 2.5-month VSL) but still runs 17+ VSLs and proven organic video. S06 says statics can spend about $250,000 at unaware and problem-aware stages if the primary text carries a long story. S05 (TikTok) is video-only. S03 says diversity is concepts, not formats. What the agent should do: format is a 10-MCR decision; for deployment, do not build format ad sets past about $10,000 a month (S08) and do not assume statics are retargeting-only. Read format by spend share inside concept ad sets. [5a4c1bc7103b] [50555d28666c] [a5c883d83f91]

**7.14 Retargeting as a growth layer vs a capped support layer.** S01 (TikTok) grows a retargeting stack with budget (30-day visitors, 7-day non-buyers, 30-day ATC, re-engagement). S09 builds a 4-part retargeting funnel and promises $1 to $3 or $5. S02 and S03 cap retargeting by frequency and skip website-visitor campaigns in about 90% of Meta accounts; S07 runs retargeting broad with 1 exclusion. What the agent should do: on Meta, cap by frequency and dollars (P7) and run website-visitor retargeting only when the engaged segment is starved. On TikTok, follow S01's tiers but apply the same cap logic and exclude buyers. Judge all retargeting on incremental columns and store data, not platform ROAS. [028483f1e7af] [ab880cedcc94] [5dff147cb0c0] [ccf942b9f2c8]

**7.15 Spend-as-proxy and zombie rescues vs trusting allocation.** S02 (breakdown effect) says trust Meta's spend split unless you are an expert. S08 uses spend share inside a winning ad set as a creative read. S09 forces spend on ads the CBO ignored and claims 20% become winners. S02 also notes CBO may starve expensive or new creative, which is the ABO argument. What the agent should do: do not restructure on breakdown ROAS; use spend share for creative briefs only; if forcing spend on ignored ads, do it as a capped, logged test (P10) or by running ABO for the test campaign. [528465d5cc14] [ab729ba34368] [841a1ded8706] [2f66cf4f65c6]

**7.16 Scale ceiling: GP to CAC bands vs break-even ROAS.** S03: scale at 2 to 3 first-purchase GP to CAC; below 1 is a bankruptcy risk unless retention or capital covers it. S09: scale to near break-even ROAS and judge by net cash in 30 days. What the agent should do: present both to the owner with the brand's retention data; default to the GP to CAC band; allow S09's stance only with a written cash and loss limit. [021224f4073c] [259da0427eb7]

**7.17 Single ad per ad set after sequence learning.** S04's transcript most naturally says single-ad-per-ad-set structures died in November 2024; 2 of its cards read it the other way. All other sources want 3+ ads per ad set. What the agent should do: 3+ ads per ad set; treat the card reading as unconfirmed `[web check]`. [e82a1ef3cf77] [0ed2f8dbde17] [d6c0209e9d6b]

## 8. Common mistakes

1. Auditing or judging from platform data only; no backend access. Fix: get orders with new vs returning flag and margin first (P9). [3b7f250f224e]
2. Scaling on blended P&L that repeat revenue props up. Fix: first-time P&L and aMER. [04bd5299ca53]
3. Comparing CAC across years without first-purchase GP, or using a flat GP. Fix: monthly GP from AOV x margin or COGS. [96ddc2d014f8]
4. Killing or scaling single ads on last-click ROAS; turning off the top spender because its ROAS is low. Fix: ad set as the unit; spend share for briefs only. [ab729ba34368] [9ede69b02ec7]
5. Judging tests on 1 day, on $1 to $2, or on about $100 spend. Fix: read windows from R36. [3ae3be9f8f79] [c8f9d9634c5f]
6. Setting ad set budgets from the 50-in-7 learning rule. Fix: P3. [1c683e007b76]
7. Hyper-segmentation: many campaigns and ad sets, few ads, tiny spend, launch-date batches. Fix: consolidate to concept ad sets. [9b521e4ff188] [0ed2f8dbde17] [66c735ceb8ff]
8. Total consolidation: 1 Advantage+ campaign for a multi-category, multi-persona brand; DPA inside the cold CBO. Fix: business-unit campaigns, concept ad sets, DPA in its own place. [52611fb24810] [1589854e06d9]
9. Adding campaigns because spend feels big, or campaigns nobody can defend. Fix: purpose line per campaign. [7350eaba553e] [5ce17b008587]
10. Interest stacking and lookalikes on Meta purchase objectives; worldwide targeting; age bands as controls. Fix: broad with hard controls. [b025c790c4ac] [48728b3abcdf]
11. Existing customers not excluded from cold; sync broken; percentage caps instead of dollars and frequency. Fix: P6, P7. [fb9db4eb1b28] [3a48f7471999] [d74e033578c8]
12. Optimising on 7-day click + 1-day view so view-throughs steer spend; mixed attribution across campaigns. Fix: 7-day click everywhere. [34a82c492fd6] [451238284cae]
13. Optimising toward incremental attribution or treating it as measured lift. Fix: comparison column; lift test for real answers. [de104cfb484c]
14. Briefing more of a "winner" before checking its new-customer 7-day-click ROAS. Fix: P8. [8c6833a8cd30]
15. Retargeting at about 50% of spend; splits by add to cart, checkout, page, warmth; the same ad louder to non-buyers. Fix: cap, consolidate, change the offer. [028483f1e7af] [5dff147cb0c0]
16. DPA death spiral: cutting prospecting and creative because DPAs look strong. Fix: rebuild top of funnel; read DPA honestly. [805594665ccc]
17. Adding new creative to a working ad set; rolling a $60 a day winner into a scaling campaign; testing inside scaling; no exclusions on scaling. Fix: R23, R50. [a95742238877] [0e642b4c3a8c] [b8a2663f518f]
18. Riding 1 winner with everything else off. Fix: variants, pipeline, cap. [c61bad8559ba] [99cd67e7cbac]
19. Launching placement or demographic campaigns from breakdown ROAS. Fix: R28. [528465d5cc14]
20. Flexible ads on with mixed assets; Advantage+ creative optimisations creeping back on. Fix: R82, R83. [e323039d800f] [04cf2865b996]
21. Store or local campaigns bleeding into Audience Network app rewards. Fix: remove. [b025c790c4ac]
22. Names that lie about targeting, objective or stage. Fix: rename; do not scale on that ROAS. [36f63e27c6d5]
23. Treating diversity as formats; 1 concept at $200k a month. Fix: concept counts by band. [45c43e3ff759]
24. Accepting Meta suggestions on projected uplift; chasing quality score or opportunity score. Fix: test and log or skip. [d9cba85df27b] [71ab0ba03b8a]
25. Expecting server-side tracking or higher EMQ to raise results. Fix: plumbing, not lever. [74d3bc849c6b] [40de3bd68e44]
26. Splitting ad accounts by country without a billing reason; hitting page caps with no plan. Fix: filters, page strategy. [b8c4642d637c] [63e75994772f]
27. Daily bid and budget fiddling as "media buying". Fix: structure and creative. [9997eb5233ac] [5e79782f9a1e]
28. Trying to out-tactic bad unit economics. Fix: offer, AOV, margin first. [bd4cb33200e9]
29. TikTok: launching without a tested pixel, without documents or a card, in simplified view, with Smart+ first, catalog on, CBO on while testing, target CPA on a new account, 15+ interests, dayparting, all budget in 1 ad group, music without rights, ad library box left by default without a decision. Fix: P11, P12, 5.5. [bbb344647f7f] [837875464f88] [097d6ce5e477] [ce98eaba5aeb] [832a0215542d] [40f4521921d6]
30. TikTok: boosting a post before its organic run; short creator authorization; all SKUs in 1 GMV Max; ROI target at TikTok's suggestion or set so high nothing delivers; promotion days at default; forgetting boosts add to budget; retargeting without buyer exclusion or with audience expansion on. Fix: P14, P16, P17. [260e5915e605] [15b3e91bb766] [3f9a7828109d] [c3654a90de4f] [1ee708d070fe]
31. TikTok: trusting default-attribution platform ROAS without reconciling to store orders. Fix: R62. [e413ec2ddfd9] [378c1eb72ff9]

## 9. Deliverables

All deliverables carry the brand name, the date range, the attribution setting used, and the line "Meta is read-only in ecomOS; these are proposals for a human to apply." Writing rules: short sentences, digits, no em dashes, no invented claims, no GPT or .env mentions on client-facing pages.

**9.1 Diagnosis memo** (audit, weekly read, or new-customer check). Markdown, 1 to 3 pages.
- Constraint: the 1 bottleneck (data integrity, structure, creative volume, creative diversity, creative quality, economics), with the proof (numbers and the breakdown or model that shows it).
- Business view: CAC, first-purchase GP, GP to CAC, new-customer count trend (last 6 months and 2 years), aMER vs each platform's ROAS, contribution margin trend. Mark any figure that came from platform attribution only.
- Account view: campaign purpose table (campaign, purpose, defendable yes or no, action); frequency by segment; attribution settings; exclusions; testing structure; scaling structure; settings hygiene findings.
- Creative view: new ads per month vs spend ÷ $1,000; concepts total and winning vs band; stage mix count; DPA share.
- Ranked roadmap: fixes ordered by commercial impact with the order of work (data, structure, creative), owner, and what needs a test rather than a change.
- Open items: every `[needs brand data]` and `[web check]` that blocked a firmer call.

**9.2 Budget proposal JSON.** One object per proposed change, arrays for the whole proposal. Money in the account currency; note currency once.

```json
{
  "brand": "string",
  "platform": "meta | tiktok",
  "currency": "INR | USD | ...",
  "date_range_read": {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"},
  "attribution_read": "7d_click",
  "read_only_note": "Meta is read-only in ecomOS; propose, do not execute.",
  "targets": {"target_cpa": 0, "target_roas": 0, "break_even_roas": 0, "gp_to_cac_band": "2-3"},
  "changes": [
    {
      "level": "campaign | ad_set | ad_group",
      "id": "string",
      "name": "string",
      "concept": {"persona": "", "angle": "", "offer": "", "ad_type": ""},
      "action": "raise | lower | hold | pause | fork | move_to_scaling | new",
      "current_daily_budget": 0,
      "proposed_daily_budget": 0,
      "step_pct": 20,
      "reason": "rule id and the numbers that triggered it, e.g. R44: 4 conv at 3x CPA",
      "evidence": {"spend": 0, "conversions": 0, "cpa": 0, "roas_7d_click": 0, "roas_new_segment": 0, "frequency_30d": 0},
      "next_read_date": "YYYY-MM-DD",
      "rollback": "return to current_daily_budget if roas_7d_click below target at next read"
    }
  ],
  "settings_proposals": [
    {"setting": "attribution | exclusion | flexible_ads | advantage_creative | placement | audience_segments", "scope": "string", "from": "string", "to": "string", "reason": "rule id"}
  ],
  "totals": {"current_daily": 0, "proposed_daily": 0, "delta_pct": 0},
  "open_items": ["[needs brand data: ...]", "[web check: ...]"]
}
```

**9.3 Kill, keep, scale list.** Table per ad set (Meta) or ad group and ad (TikTok): name, concept, spend in window, conversions, CPA or ROAS on 7-day click, new-segment ROAS where available, frequency, call (kill, keep, extend, fork, scale), the rule and number that triggered it, the creative brief line for 10-MCR ("make more like ads X and Y: they take spend in an at-KPI ad set"). Ad-level entries on Meta are briefs, not budget moves.

**9.4 Test plan.** Per concept test: concept (persona, angle, offer, ad type), hypothesis, ad set name, ads (ids or files) with 3 to 4 variations, targeting (broad plus hard controls), attribution setting, exclusions, daily budget and the method that sized it (3x or 5x CPA, or formula with conversions and days), start date and weekday, read date, decision table (keep, kill, extend, scale with numbers), and the store-side measure (new-customer SKU sales) where relevant. Includes a "do not touch until" date.

**9.5 TikTok launch sheet** (when TikTok is in scope). The 5.5 checklist with pass or fail per row, the P12 settings as built, the first test plan (P13), and the 24-hour and 3-day read table filled in.

## 10. What needs live data or a web check

**Brand data `[needs brand data]`**
- Monthly spend by platform and campaign type, 24 to 30 months; monthly conversions by campaign.
- Orders with new vs returning flag; new-customer count by month; SKU-level daily sales split new vs returning.
- AOV, gross margin by category (monthly, post-discount), COGS, units per transaction; break-even ROAS and allowable CPA; first-order GP; 365-day LTV; GP cohort curves by day 90, 180, 365.
- Repeat purchase rate; repurchase cycle (sets the exclusion window); LTV and repeat rate by first-purchase category and by acquiring concept.
- Customer file size and sync status (Klaviyo to Meta; CSV to TikTok, with consent status); retargeting CPM; current 30-day frequency on existing, engaged and new.
- Own CPM trend by year; CPC vs ROAS scatter by ad; CPM and page conversion rate by landing page.
- New ads launched per month; concept tags per ad; stage tags per ad; spend share per concept; winner churn, hit rate, average winner revenue.
- Revenue by weekday; time from first visit to purchase; days from first view to purchase.
- Purchase EMQ; Meta-reported purchases vs backend orders; TikTok-reported purchases vs store orders; which attribution source the brand uses.
- Frequency and reach by ad set over time; per-video retention curves; ad-level CTR, CPM, hook rate, hold rate, click-to-purchase.
- Target countries, languages, minimum age for the category; where stock sits; regional targets; category and range budget targets.
- Current TikTok CPA by product; customer age mix; daily budget to cap any audience sandbox.
- Geo-level sales for any lift test.

**Web checks `[web check]`**
- Meta: current names and behaviour of Andromeda, GEM, sequence learning, adaptive ranking, and the 3% and 5% lift claims; the auction formula wording (ad quality vs user value); which audience fields are hard controls vs Advantage+ suggestions; status of interests and lookalikes (claimed deprecated July 2025); current learning phase definition; incremental attribution (still an optimisation option? how modelled?); engaged-view definition and attribution options; existing-customer controls in Advantage+ sales campaigns; "breakdown effect" help page; flexible ads name and settings; Advantage+ creative optimisations path in advertiser settings; ad set spend limits under campaign budget (percent or amount); ads-per-ad-set limit; live-ads-per-page and per-account caps; stance on multiple ad accounts sharing 1 pixel; relevance diagnostics; ad policy on personal attributes and health claims; Chrome third-party cookie status; current advertiser count; CPM inflation; consolidation guidance; ads per ad set after sequence learning.
- TikTok: Ads Manager and Seller Center current flows; Smart+ names and defaults; GMV Max and TikTok Shop availability by country; special promotion days controls and defaults; ad library opt-out rules by region; upload specs; Commercial Music Library rules; whether learning is per ad group; business-domain email approval claim; backup payment methods by country; current CPM, CPC and CPV benchmarks by market; TikTok user, time-spent and Shop GMV figures; new-advertiser credit offers; CapCut pricing and ownership; UGC package prices; AI model limits.
- Both: consent rules (GDPR, India DPDP) before choosing maximum data sharing; category retention benchmarks; source of the 30% interest misassignment figure; ad blocker install count.

## 11. Freshness and stale-risk notes

- **Andromeda, GEM, sequence learning, adaptive ranking (R63 to R67).** All 4 Meta-side sources describe these from memory with no links. Rules built on them (creative is targeting, Entity ID grouping, ad set learns in isolation, product-aware ads held on warm users) are presenter models. Re-verify against Meta engineering posts every quarter; re-read section 7.8 when Meta changes retrieval.
- **Interest and lookalike deprecation (R24, 7.5).** S04 dates it to July 2025; S07 still uses them as a sandbox; TikTok sources use them. Check the live UI before proposing removal or use. Re-verify each quarter.
- **Advantage+ changes (R9, R27, R83, 7.4).** Names (Advantage+ sales campaign, Advantage+ campaign budget, flexible ads, creative optimisations, existing-customer cap or exclusion) and defaults move often. S02 says its second-account advice changes about every 6 months. Every `[verify UI]` in P6 needs a fresh look before each proposal.
- **Attribution options (R55 to R57, 7.3).** Incremental attribution as a setting, engaged view definition, and comparison columns are 2025 to 2026 features. Re-verify monthly while in use.
- **Page and ad caps (R86).** About 300 to 500 is a presenter figure. Check before any page strategy proposal.
- **Learning phase thresholds (7.7).** Meta 50 in 7, TikTok 25 in 7: platform definitions that change. Check yearly; they do not drive budgets here.
- **TikTok Shop, GMV Max, Smart+, TikTok One, Search ads (group P).** S01 calls several "new" or "newer". Availability by country, UI flows, ROI target behaviour and promotion-day defaults are late 2025 snapshots. Re-verify before every TikTok Shop proposal and at least quarterly.
- **TikTok cost benchmarks (R99, section 6).** US, undated, 1 presenter each. Replace with the brand's own first 2 weeks of data.
- **Pricing named in sources (CapCut, UGC packages, server-side tools).** Point-in-time; do not quote without a check.
- **GP to CAC bands, frequency ceilings, retargeting share flags (R60, R71, R75).** Opinion-based and not UI-dependent, so they age slowly, but they assume the sources' 7 to 9 figure USD context. Re-fit to the brand's margin, currency and retention.
- **ecomOS constraint.** Meta is read-only and TikTok has no connector. Any move to production access (META_GALLERY_STATUS.md next steps) changes how P4 to P6 hand off, not the rules.

## 12. Source index

| No. | Title | Type | Credibility | Contributed most |
|---|---|---|---|---|
| S01 | The BEST TikTok Ads Course For Beginners in 2026 | Course transcript, about 10 modules, 43,104 words, 57 cards | Agency owner (Zoco Marketing) selling a "free" course with affiliate and partner links (TikTok credits, CapCut, Arc Ads, Foreplay, Kalodata, Shopify). 1 presenter's claims; blurred client screenshots; no test sizes or controls. Strong as a click-by-click setup guide, thin on kill and scale rules. | TikTok account, Business Center, pixel test, in-feed Sales build, budget rules (2x CPA, 25 in 7), broad first then interest test, Spark organic-first loop, Search campaigns, TikTok Shop, affiliates, GMV Max settings, retargeting audiences and budget tiers. |
| S02 | The Only Video You Need On Meta Ads In 2026 | 2-hour talk transcript, 22,222 words, 48 cards | Australian agency (Blue Sense Digital) selling management and free audits to $5M+ brands; recruiting. Evidence is its own audits, aggregated spend report and 1 $750k a month account; no controlled tests; presenter admits some preferences are agency labour or bias. The most complete structural source. | Spend-tier templates, 5 diagnostic questions, concept ad sets, fork rule, test sizing (3x or 5x CPA; formula), test duration, spend equilibrium and scaling campaign, ABO vs CBO, breakdown effect, retargeting as capped layer, existing-customer dollars and frequency, DPA death spiral, settings to turn off, page strategy, second account. |
| S03 | How We Audit 8 and 9 Figure Ad Accounts (Full Process) | Solo walkthrough transcript, 10,451 words, 25 cards | Unnamed agency lead ($400M a year claimed under management) selling free audits to $5M+ brands and recruiting. No data tables or before-and-after cases; key models (retention benchmarks, velocity models, geo-lift design) kept in-house. Document header describes a different CRO video; ignore it. | Audit method: cohort model (CAC, first-purchase GP, GP to CAC bands), normalized and first-time P&L, aMER reconciliation, 7-day click + 1-day engaged view, defend-every-campaign structure review, frequency by segment, settings errors, creative bottleneck order (volume, diversity, quality), 1 ad per $1,000, concept bands, fix order data then structure then creative. |
| S04 | How The Meta Ads Algorithm Works in 2026 | Whiteboard talk transcript, 7,214 words, 13 cards | Same agency as S02 (Blue Sense Digital); sells audits to $10M+ brands. Claims all mechanics come from Meta docs but cites none. Meta's own lift claims quoted; agency observations; opinion. Strong on why, weak on how. | Retrieval, ranking, auction model; auction formula; hard controls vs suggestions; broad as a probe; narrow-creative saturation; Entity ID and concept diversity; EMQ as accuracy of action rate; server-side tracking unmeasurable; 20% rule undocumented; economics beat tactics; consolidate by default. |
| S05 | The Only TikTok Ads Tutorial You Will Ever Need | Tutorial transcript, 5,518 words, 16 cards | Agency owner "Tim" ($5M+ TikTok spend claimed) selling done-for-you management. 1 fashion case, 1 SaaS viral ad, unsourced platform stats; several internal contradictions (CTA, music, age, interests). US-centric thresholds, undated. | Business Center and payment setup, Shopify pixel partner integration, 3-tier pyramid, $50 a day per ad group, 2 to 3 parent interests, custom audiences as lookalike seeds, 4-week targeting ladder, 3:2:1 first test, 24-hour and 3-day thresholds, kill bottom 50%, naming convention, smart campaigns off. |
| S06 | How To Make Your Meta Ads Scale | Talk transcript, 5,480 words, 11 cards | Unnamed creative-breakdown presenter, likely agency-side; nothing sold in the transcript. All rules are 1 practitioner's reading of other brands' ads; 1 observed result (a static running 4 to 5 months). Mostly creative strategy (10-MCR); the deployment part is frequency diagnosis and structure by awareness. | Post-Andromeda holding of product-aware ads on warm users; frequency as a creative-mix problem, not an exclusion problem; 80/10/10 stage split; judge unaware ads account-wide; structure follows concepts and 1 stage per concept; DPA can cover most-aware. |
| S07 | The entire Meta ads algorithm explained in 21 mins | Talk transcript, 5,262 words, 13 cards | Media buyer "Mark" selling a free AI-ads masterclass; runs accounts at 5 figures a day. 1 screenshot; a withdrawn Meta doc reconstructed from memory; peer hearsay; opinionated and profane. Ban-wave theory is unverified and excluded from rules. | 4-stage pipeline and Total Value equation; broad default with a capped sandbox; 1 concept + 3 variations per ad set; variations still work; bid strategy by constraint (lowest cost profitable at scale); ads always learning; 7-day minimum and noise under $1,000 a day; EMQ overrated; distrust Meta suggestions and scores; outside attribution. |
| S08 | How To Structure Meta For High Creative Volume | Talking-head transcript, 4,549 words, 13 cards | Unnamed paid social agency speaker selling services; all numbers are worked examples (3x, 70% and 55% margin, 50 and 120 creatives, 40% cap, $10,000 a month); no client data. Andromeda claims are the speaker's model. | Campaign splits by business unit, ad set splits by the variable you want to learn (concept preferred; format only for new accounts; never launch date); ROAS reliability falls by level; ad set as decision unit; spend share as creative read; Pareto; double down (120 vs 40) or cap (40%); 2 tests (data integrity, commercial alignment). |
| S09 | Learn 97% of Meta Ads in Under 19 Minutes | "8 hacks" transcript, 4,461 words, 10 cards | Agency owner selling his AI copy tool (Kong); likely lead-gen focused; "$300M spent" self-reported; anecdotes only; most examples are services, 1 ecommerce example. Aggressive stances (statics only, scale to break-even). | Do not ride 1 winner; clone into variants under CBO; zombie ad set for starved ads (capped use); identity words and long copy as targeting context; 7-day broad vs interest-stack test; headline-to-page match; retarget non-buyers with a different offer; blended ROAS and net free cash flow; scale toward break-even as an owner's choice. |
| S10 | How To Scale Meta TOF Campaigns | Short screen-share transcript, 2,121 words, 7 cards | Unnamed auditor ("90% of accounts I look at"); 1 real Advantage+ campaign on screen plus 2 hypotheticals; no after-fix result; incremental attribution explanation is the presenter's assumption. Card fe7d1d8bcc27 has no basis in the transcript. | The new-customer profitability diagnostic (audience breakdown, then attribution comparison); 12.84x vs 5x vs 1.71x example; about half of TOF spend on existing customers; 7-day click on all campaigns; incremental attribution as column only; 2-year exclusion with lapsed carve-out; Conversion Lift Test vs incremental attribution; measure scaling on new-customer SKU sales. |

**Neighbour folders and what lives there.**
- 10-MCR-paid-social-creative: hooks, scripts, awareness-stage writing, formats, UGC, AI video tools, creative production systems (S01 modules on psychology, CapCut, Arc Ads; S05 filming and editing; S06 stage scripting; S09 native content).
- 06-MEA-measurement: pixel and CAPI setup, EMQ improvement, incrementality test design (Conversion Lift, geo-lift), MMM, third-party attribution tools, GA reporting.
- 12-GAD-google-ads: Google structure, brand vs non-brand, attribution windows, Merchant Center feed and multi-currency (S03's Google section).
- 11-ADC-ad-copy-deployment: ad copy and the ad-copy v1.2 playbook (identity words and long copy from S09 belong there for writing; here only as a targeting model).
- 09-CRO-testing and 07-LPG: landing page split tests, headline-to-page match (S09 hack 6), page conversion reads.
- Offer and finance folders: pricing, AOV levers, unit economics detail (S04 R3, S03 cohort model as a finance model).
