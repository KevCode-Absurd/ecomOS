# How to Scale an eCommerce Brand Profitably in 2026: The Full System

**PART 2 OF 2.** This file covers only the second half of the source text (part2 of a 2-way split). It picks up mid-sentence on Meta account structure at $250k+/month spend and runs through: Meta account structure at scale, CBO vs ABO, ad set composition and naming, retargeting/DPA management, settings to disable, testing-budget math, the full Meta creative-strategy module (Andromeda, concept architecture, hooks, formats, testing framework, creative fatigue, creative production/team/AI), and the full Google Ads module (account structure, PMax, Standard Shopping, Search, bidding, GMC feed, a 90-day rollout, and a root-cause diagnostic framework). Part 1 (not written by this agent) should cover the source's opening: data integrity/commercial-alignment foundations, sub-$50k and $50k-$250k Meta account structures, and the start of concept-level testing - the two files are meant to be merged into one mini playbook by a later pass.

source_id: 1Ta2RSp1n8gCTsxoz38HIw1ZHjRtrCjTL | folder: 99-multi | cards: 198 total for the whole source (this part indexes 107 of them, ids listed in Section 10) | words: 123,649 total for the whole source, approx. 63,200 in this part | type: talk / transcript (long-form YouTube video, spoken and lightly edited)

**credibility**: the speaker runs a paid-media/creative agency serving e-commerce and retail clients on Meta and Google. Self-reported agency signals scattered through the text: hiring contact given inconsistently as "hiringblensedigital.com.au" / "hiringbluensedigital.com.au" / "hiring at bluedigital.com.au" (three different transcriptions of what is almost certainly one real domain), and a self-reference to "the BlueSense YouTube channel" - likely agency name "Blue Sense Digital" or similar [web check: confirm exact agency name and domain before citing it anywhere client-facing]. States 8-9 years running Meta ads (since 2018). Claims to have run PMax on 250+ of the agency's own managed accounts and consulted on ~400 more (7-to-10-figure e-commerce accounts) - self-reported, no methodology given. States 60% of the agency's own client portfolio spends over $250k/month on Meta. Sells two things throughout: (a) a "free audit" as a lead-gen offer, gated at "$5 million a year" in online revenue (stated once, inconsistently, as "$5 million a month" - likely a slip, but flagged), and (b) is actively hiring performance marketers. Every named case study in this part ($350k/month client with 15 ads, six fashion-brand DPA audits, the sunglasses wholesaler, the $25k/day worked example account) is self-reported client work with no independent verification, and several are explicitly recalled "off the top of my head." Treat all figures, percentages and named results in this file as **unverified, self-reported claims**, not proven benchmarks.

**date signals**: explicitly timestamped ("as of April 2026") for the trial-reels tactic, with the source itself flagging that tactic may not survive algorithm changes. Repeatedly frames advice as being "for 2026 and 2027." Treats Meta's Andromeda algorithm shift as a completed, mature change and treats interest-targeting as functionally dead. Treats PMax, Standard Shopping, AIMax, Demand Gen and DSA deprecation as the current Google product landscape. Several tactics are explicitly labeled by the source as time-sensitive (the second-ad-account strategy, the partnership-ads "arbitrage window," Meta's Gmail placement behavior in PMax). Anything platform-mechanical here should be re-verified live before being relied on operationally.

## 1. What this source is for

Helps a media buyer or founder (a) structure and operate a Meta ad account once spend passes roughly $250k/month, choosing between ABO and CBO and managing retargeting/DPA risk; (b) build and run a Meta creative-strategy system end to end - concept design, hooks, formats, testing, fatigue management, production team and budget, and AI's proper role in that pipeline - on the premise that creative, not media buying, is now the primary lever on Meta; and (c) structure, optimize and diagnose a Google Ads account for e-commerce in 2026 (PMax, Standard Shopping, Search, GMC feed, bidding), including a repeatable root-cause process for figuring out why an account's performance dropped before touching anything.

## 2. Principles

1. **Creative is the targeting, not just the message.** Post-Andromeda, Meta no longer needs a chosen audience to serve an ad against - it reads the creative itself (transcript, on-screen copy, imagery) and finds who resonates. Loading similar creative narrows reach; loading creative that speaks to genuinely different people is what expands reach. Condition: applies to Meta specifically, post-Andromeda (source says this has been true in practice for ~2 years before this recording, formalized by the Andromeda rollout). Evidence: source's own agency behavior (stopped using interest targeting ~2 years ago) plus a stated prior video making the same point pre-Andromeda [web check: verify]. `[4bddfe132ec2]` `[90fdf6692e74]` `[8868bab7b40d]`

2. **Data integrity and commercial alignment are non-negotiable at every spend level.** Whatever structural complexity gets added as an account scales, you must still be able to read the data to make decisions, and the structure must match the business's actual margin/product/persona reality - not complexity for its own sake. Condition: applies at any spend tier. Evidence: source's own stated account-structure "four questions" and "what stays fixed as spend scales" list. `[34509036c871]`

3. **Attribution reliability rises as you move up the account hierarchy.** Ad-level ROAS is the least trustworthy read (last-click attribution plus hidden multi-touch sequencing distort it); adset-level is more trustworthy; campaign-level ROAS on 7-day click, with existing customers excluded, is the most trustworthy and tends to track the real P&L. Condition: decisions about scaling/killing creative should be made at the adset or campaign level, not the ad level. Evidence: source's own explanation of Meta's sequencing mechanics; no external citation given. `[5b34bfe523b3]` `[a96c890428cb]`

4. **A concept is persona × angle × offer, tested in that priority order, with format as a distant fourth lever.** To create real audience diversity you must change one of persona/angle/offer; if an ad underperforms, fix the angle first (highest leverage, least constrained), then the offer (high leverage but limited room to iterate), then the persona (drives breadth/volume), and only then the format (mostly just reaches people who prefer that content type). Condition: this ordering is the source's own explicit ranking, stated as a common industry mistake to run it backwards (format first, angle last). Evidence: source's own framework, cross-referenced against Alex Hormozi's "offer is king" framing as a named point of disagreement. `[bc784b37d696]` `[0f6cdc6afa17]`

5. **Volume beats quality-picking, but only above a minimum quality bar.** No one - including expert creative strategists - can reliably guess which of several "good" ads will actually win; therefore the right strategy is to define a minimum quality bar, get every ad above it, then maximize volume, rather than trying to intellectually pick winners in advance. Condition: applies once ads already clear a basic quality bar (have a real concept, working hook, and awareness-appropriate format) - high volume of ads that don't clear that bar is "junk volume," not a strategy. Evidence: source's own claim, illustrated with a self-reported example of 2,000+ ads/month barely reaching $4M spend and being unprofitable. `[a9d4d1b724a5]`

6. **Google Ads account structure defaults to full consolidation; every extra campaign needs a specific commercial justification.** Segmented campaigns learn in isolation (smaller, less reliable datasets each), which structurally worsens bidding accuracy; the only valid reasons to split are brand vs non-brand, geography, margin/efficiency differences, and genuinely different product categories/audiences. Condition: applies to PMax, Standard Shopping and Search structure alike. Evidence: source's own worked example (50/20/10-conversion campaigns consolidating into 90) and the agency's own account-audit experience. `[d39e9023291d]` `[92200eb95b45]` `[5d8be0c613b5]`

7. **PMax and DPAs systematically over-attribute; Standard Shopping and top-of-funnel spend are structurally under-credited.** Both are driven by the same mechanism: a bottom-of-funnel/retargeting-heavy tool captures last-touch credit for demand that top-of-funnel spend actually generated. Practical effect: naive reliance on in-platform ROAS pushes budget toward PMax/DPAs and away from the genuinely incremental top-of-funnel spend that sustains them, which can spiral an account into decline. Condition: matters most as PMax or DPA spend share grows past a modest level; less relevant at very low spend. Evidence: source's own scaling tests (PMax 2x vs Standard Shopping 2x, incremental revenue compared) and repeated "DPA death spiral" client pattern - both self-reported. `[e800ec50f078]` `[fa103e10c7f6]` `[299de15a096a]` `[926e49f0a825]`

8. **Root-cause analysis must run top-down (business → channel → campaign type → campaign → submetric), never bottom-up.** Most people jump straight to a flagged submetric (e.g. "this ad's CPC is down") without first checking whether it matters at the business level at all, which wastes time and produces wrong fixes. Condition: applies to any ad-account diagnostic process, described here specifically for Google. Evidence: source's own stated framework and explicit claim that "most accounts that appear broken aren't actually broken at all." `[74d14b3daff2]` `[41fe6e957f15]`

## 3. Procedures

Grouped by domain, as this source is multi-topic within the paid-media/creative space. Domains with no content in this part of the source (offers, landing pages, email/retention as their own procedures, standalone finance procedures) are not listed here - check part 1 and the neighbor folders (offers, email/retention) for those.

### Paid media - Meta account structure and testing

**Structuring an account above ~$250k/month spend** (source gives strategies, not one fixed structure, because complexity varies too much at this range):
1. Consider a second ad account running the same pixel but different bid logic (e.g. maximize-conversions in the primary account, maximize-conversion-value or cost/bid caps in the second) to win auctions the first account isn't entering, and to de-risk against a ban or billing failure in the primary account. `[159829ec73747f9033f8e0b6]` - note: source explicitly flags this tactic as time-sensitive and likely to change. `[web check: confirm this is still valid Meta behavior]`
2. Solve the page-limit problem you will hit at this spend level (source references 3 options given earlier in the full source - likely covered in part 1; not restated here).
3. Introduce bidding-strategy complexity (bid caps, cost caps, target ROAS run alongside standard campaigns) only once spend clears roughly $250k/month - below that, bidding-strategy tinkering is not the highest-leverage lever. `[159829ec73747f9033f8e0b6]`
4. For international expansion, do not default to a separate ad account per country/region - this multiplies management labor. Segment by ad account only when you need to bill in a specific local currency; solve reporting-by-country with filter rules instead. `[0dd3aee5c557]`

**Worked 5-campaign structure at ~$750k/month spend** (source's own client example - treat as an illustrative pattern, not a template to copy) `[d00fe7fd4c3b]`:
1. Testing campaign (ABO), tests run at the adset level even at very high spend.
2. Scaling campaign (CBO, one adset, cost caps) - top-performing post IDs are pulled in every 1-2 weeks without being turned off in the testing campaign.
3. Promo campaign, kept separate because promos rotate every 3-4 weeks and would otherwise disrupt testing/scaling learning phases; also skews toward price-sensitive buyers.
4. Advertorial campaign, pulled out once it organically grew to ~30% of spend inside testing, so it can be KPI'd as its own funnel.
5. DPA campaign for existing customers/website visitors, run on incremental attribution, kept low and in line with frequency targets.

**Choosing ABO vs CBO** (source frames this as risk tolerance, not a right answer) `[9190a63c0c09]` `[345054044d8c]`:
- Use CBO for higher risk / likely higher blended ROAS (concentrates spend into top performers, per Pareto's principle - source's own account-audit pattern claims ~4% of ads hold ~64% of total spend/revenue, self-reported).
- Use ABO (or CBO with min/max spend caps on ~60% of budget, ~40% left free) for lower risk / more even portfolio distribution - only worth the added management overhead at large scale; "overkill" below roughly $10k/month.
- Do not use CBO if the brand has high AOV and low conversion volume - CBO will chase soft signals (CTR/CPC) instead of true conversions when conversion data is too sparse.
- Consider seasonal switching: CBO during high-spend push periods (e.g. Black Friday/Q4), ABO during dedicated testing periods (e.g. Q1).

**Ad set composition rules** `[d45d9720ad61]` `[b3d6e61e0a7a]` `[afc96213f022]`:
1. Minimum 3 ads per adset (needed for Meta to sequence ads to a user); practical range 3-15 ads for most accounts, no hard ceiling at very high spend.
2. Keep all ads in one adset targeting the same persona, but consolidate different funnel-awareness stages (top/mid/bottom) into the SAME adset rather than splitting by awareness stage - splitting invites human bias (each adset's own last-click ROAS looks misleadingly different even though they work together).
3. Name adsets by persona, angle, offer, content type and launch date - never by batch/date alone (e.g. not "March 7 creatives") - so concepts can be filtered and KPI'd later.
4. Do not add new ads to an adset that is currently hitting KPI - it resets the learning/sequencing phase and can hurt a working result. If you want to add more creative to a working concept, launch a new adset for that same concept instead. Freely add/remove ads in an underperforming adset - there's no working sequence to protect.
5. Never turn off a winning ad or adset to "move it" into a scaling campaign - increase its budget in place, or duplicate the post ID into a separate campaign without disabling the original.

**Retargeting and DPA management** `[34161704728554cedff6859f]` `[e800ec50f078340338ff16dc]` `[421e7aee0498049003e18790]`:
1. Treat retargeting as a capped support layer, never a growth driver - actively look for ways to cut retargeting spend, the opposite mindset from cold acquisition.
2. Do not hyper-segment retargeting by product/page/funnel-step - consolidate into fewer audiences; the CPM increase from segmentation is never worth the marginal conversion-rate gain.
3. Track frequency as the core retargeting KPI alongside incremental revenue.
4. For DPAs: measure ROAS on 7-day click or incremental attribution, not last-click/view-heavy models (Columns → Compare attribution settings → Incremental attribution → Apply `[verify UI]`). Remember DPA performance is a direct reflection of top-of-funnel investment - don't cut TOF spend because DPA "looks like it's carrying the account."
5. Budget existing-customer spend in DOLLARS, not as a percentage of total spend. Formula: existing-customer monthly budget ≈ (number of existing/target customers) × (CPM) × (desired monthly frequency). Judge success only on (a) profitability of the incremental spend and (b) frequency, not on a % target.

**Settings to turn off / check on Meta** `[4101599d2222430e164ae8a6]` `[00054444d5a7fd9f66324855]`:
1. Flexible/dynamic-creative ads - you lose the ability to tell which asset drove performance; if you must use them (e.g. to dodge the ad limit), only load very similar creative variants.
2. Cost caps/bid caps as a primary lever below ~$200k/month spend - not the highest-leverage lever at that scale, though usable if you know what you're doing.
3. One-day view attribution in adset-level budget decisions - it over-attributes to existing customers.
4. Advantage+ automated creative-optimization rules at the advertiser-settings level, in addition to the per-ad toggle (Meta can silently re-enable them). `[verify UI]`
5. Audit the CRM-to-Meta audience sync (e.g. Klaviyo) periodically - it breaks periodically, and when it does, existing customers get mistargeted as new, wasting acquisition budget.

**Calculating a test's daily budget** `[2dbc68e5e82e]`: pick (a) the conversion count that counts as statistically significant for you, and (b) how many days you want to spend to reach it. Daily test budget = (target conversions × expected CPA) ÷ test duration in days. Example: 20 conversions × $100 CPA ÷ 14 days ≈ $143/day. Source explicitly rejects Meta's own "50 conversions in 7 days" guidance as unworkable once back-calculated into a daily budget (same CPA → $714/day per single test, unaffordable for 5-10 concurrent tests).

### Creative - concept architecture, hooks, formats, testing

**Building concepts** `[dac13325f1bc]` `[e218c186102a]` `[010fe64918f4]` `[c9cab64dcc73]`:
1. Define persona first: an archetype defined by problem/desire/buying-trigger, never a plain demographic ("busy professional" is bad; "a consultant who flies twice a week and needs a carry-on wardrobe for boardrooms and bars" is good). Manually build 30-40 real personas before asking an LLM for more; feeding an LLM only 3-4 shallow personas produces generic, "average" output.
2. Choose an angle: assemble from a menu (problem agitation, contrarian truth, social proof/domain authority, curiosity gap, comparison/objection handling, before-after transformation - the last one is high-performing but Meta actively disfavors it, so it must be worked in carefully) tailored to the chosen persona.
3. Only then choose format (video/static/carousel/VSL/etc.) - never start with format. `[a7eee2af51378d570b51c2d5]`

**Testing priority order when something isn't working** `[bc784b37d696]`: fix the angle first → then the offer (limited room once you've exhausted product/value-prop variations) → then the persona (for breadth/volume, not for fixing underperformance) → then format last.

**Structuring adsets by concept** `[a290245745d6356061056b51]`: one concept (one persona/angle/offer) per adset, so targeting doesn't get confused and learnings stay attributable. Build at least 10+ ads per new concept test (rule of thumb: required ads ≈ 1 ÷ account hit rate; e.g. a 5% hit rate needs ~20 ads to expect one winner).

**Hooks and bridges** `[9c15aae468c216642d523cd1]` `[b86b75e9bce9d133f6fb0bee]` `[312400b7ccabfa09a8d8ea3a]` `[19ad3f95102c20c8fa77f85b]` `[5e663b2acdc67893d08eb72c]`:
1. Grade a hook on clarity, relevance (agitate the problem, not a persona callout), novelty, specificity and credibility - you don't need all five, just a couple done well.
2. Never abruptly introduce the product right after the hook ("bridge" failure) - blend the awareness transition gradually (unaware → problem aware → solution aware → product aware) and introduce the product as LATE as the format allows, even though fewer total viewers reach it - the ones who do convert at a much higher rate.
3. Hook testing still works post-Andromeda (a new hook gets its own creative ID and reaches a distinct audience) and is extremely cheap - rotate hooks onto fatiguing hero ads to extend life.

**Choosing a format** `[a7eee2af51378d570b51c2d5]` `[bc1fb281f2e320597effcf3c]`: ask, in order - what's the concept? does it need education? can the value prop fit in one frame (favor cheap statics)? does it need a demo? what awareness stage is this for? Then check cost-of-production against contribution margin per ad (per format) before committing budget to a format at scale - a format that "performs better" in absolute ROAS can still be the worse investment if it costs much more to produce per unit of contribution margin.

**Testing cycle** `[61ad59932aa7]`: build hypothesis (which concept variable is being tested) → build 10+ ads → launch → analyze against the original hypothesis (expected spend/conversions/ROI vs actual) → if it worked, scale → iterate (this loop speeds up as spend grows).

**Managing creative fatigue** `[02326c43f14a]` `[3ebec38bdf56]` `[e6675d2d6fbe]`:
1. Understand every ad has a finite total spend capacity (area under a spend-vs-time curve) and will eventually fatigue - decide deliberately whether to squeeze it hard (faster, shorter life - right choice only if you need to sell through excess inventory) or run it lean (slower, longer life - right choice if inventory/cash-cycle is constrained). Share inventory/cash-cycle context with your media buyer proactively; they won't know to ask.
2. When a creative fatigues, the 4 tactics available are (in the source's stated order of preference, most to least recommended): iterate new hooks onto the proven body; move it to a cost-cap campaign to squeeze more (short-term only); rotate it into a different format; or duplicate the post ID into another campaign. Adset-duplication is explicitly NOT recommended by the source.
3. Match persona breadth to spend capacity - narrow personas resonate better but cap daily spend lower; broad personas can absorb more spend but require much higher creative skill. Start narrow, broaden only once you're at meaningful scale.

**Creative production planning by spend tier** `[ec0c882e1e06]` `[3ed85b1ffd80]` `[e530277843071991748dd73e]`:
- $4k-$30k/month: founder-led content (time, not money, is the cost); 3 core concepts; 60-80% of budget on testing; validate cheaply with cut-down "trial reels" posted organically before spending ad dollars. `[bd9a8085893c]`
- $30k-$100k/month: 25% of media budget to production; 2-3 UGC creators; 5-6 concepts; introduce a scaling campaign and partnership ads; target creative volume via the formula below.
- $100k+/month: production budget asymptotes to ~10% of media spend (≈2.5% of revenue at a 25% marketing-efficiency ratio); full production team (scripter, editor, 4-6 creators, designer); 8-10 active concepts; at least 100 new assets/month; track cost-per-asset and profit-contribution-per-ad by creator/source.
- Simple creative-volume rule of thumb: 1 new ad per $1,000 of monthly spend. Better method: required creatives/month = target new-customer-revenue ÷ (average spend per ad × average ROAS) - flex this with the revenue forecast, and separately model win/loss distribution and time-to-revenue rather than relying on a single average.

**Building the creative team** `[0b902cecf95bd0bd40abf928]` `[e530277843071991748dd73e]` `[3412220fa6466ce136241e08]`:
1. Hire a video editor (ideally AI-native) and a static designer as volume grows - both can be remote/part-time.
2. Fill the "creative strategist" role (fundamentally a copywriting function) either by hiring one directly, or by promoting/training up an existing designer or editor into the role - the latter can create faster feedback loops. Some businesses pay this role a variable ~3% of ad spend on top of base salary, though this breaks down (gets "outrageous") at large scale.
3. When sourcing any creator, review past output AND the brief that produced it, to calibrate how detailed your own briefs need to be.
4. Apply AI in the middle of the pipeline (briefing/scriptwriting, production) where it adds real leverage; avoid leaning on it for ideation or analysis, where it tends to default to generic output and can mislead core decisions if trusted uncritically.

### Paid media - Google Ads

**Account structure** `[92200eb95b45]` `[5d8be0c613b5]` `[0103a8c9bea3]`:
1. Default to one consolidated campaign per product line; add a campaign only for brand vs non-brand, geography, margin-tier differences, or genuinely distinct product categories/audiences.
2. Route 80-90% of e-commerce Google spend to Shopping, not Search - Shopping's pre-click information (image/price/title) produces far higher-intent clicks. Exception: e-commerce businesses with a real B2B buying motion perform better on Search (B2B buyers distrust Shopping's retail pricing display).
3. Replace SKAGs with topic ad groups (10-20 themed keywords per group) - SKAGs stopped working once Responsive Search Ads needed high impression volume (~2,700 possible combinations) to properly learn. `[50d06003decd]`
4. Run a universal, account-level negative-keyword list on every new campaign; review negative keywords daily-to-weekly in a new search campaign's first 30 days, then ease off.

**PMax setup** `[8c4e6e2d406b]` `[2b7d05cb2e3f]` `[0d34948521a9]`:
1. Segment asset groups by product type (never leave the single default asset group), with a correspondingly customized listing group per asset group - 15+ products per asset group as a rough floor, 3-20 asset groups as a rough range for most accounts.
2. Set audience signals and search themes from real historical converting search terms, not guesses - but note they only matter meaningfully on brand-new campaigns/products with no conversion history; on a mature account (source's threshold: roughly $30k-$100k+/month on PMax) tweaking them makes almost no difference.
3. Set brand exclusions BOTH ways (brand-list exclusion AND direct negative keywords) as redundant fail-safes - without brand exclusion, PMax functions largely as a retargeting campaign. `[verify UI]`
4. Launch on Max Conversion Value to accumulate data, then transition to Target ROAS for stability once there's enough data. Watch for the tROAS "trap": raising target ROAS narrows the eligible audience toward warm users rather than genuinely improving efficiency.
5. Use feed-only PMax (delete all asset groups, leaving only the listing group; disable URL Expansion and Automatically Created Assets) to force spend into Shopping only, if PMax starts placing unpredictably on YouTube/Gmail/Display. `[verify UI]`
6. Priority order for PMax variables: GMC feed quality > brand exclusions > asset/listing-group structure and creative > bidding strategy > audience signals/search themes.

**Feeder strategy** `[926e49f0a825]`: run Standard Shopping as the cold/top-of-funnel campaign (genuinely reaches cold users) at a low target ROAS to capture cheap, low-competition traffic; run PMax as a high-target-ROAS converter layer on top of it. Addresses the claim (source's own industry-anecdote, unverified) that PMax over-attributes ~50%+ of its conversions to repeat/warm customers.

**Standard Shopping structures** `[cfc0bb5b70ee]`: top-sellers-vs-everything-else split (large non-fashion SKU counts only); the feeder strategy above; or a tiered performance labelizer (over/near/under/no-index) - only worth the complexity at thousands of SKUs.

**Bidding strategy selection** `[7881306718d9]` `[791e1a8f256b]` `[f6bbad74d2b1]`:
1. New accounts with no conversion data are forced onto manual CPC/Maximize Clicks; move off these as soon as possible once established.
2. Choose expansive (Max Conversions/Max Conversion Value) to keep exploring new auctions/audiences, or restrictive (Target CPA/Target ROAS) to protect a set efficiency - rotate between the two over time rather than sitting permanently on one.
3. For e-commerce, optimize for VALUE (Max Conversion Value / Target ROAS) roughly 90% of the time, not for raw conversions/Target CPA, which biases spend toward your cheapest product regardless of its actual margin/ROAS.
4. Use portfolio bidding strategies to merge learnings across otherwise-segmented campaigns, and to layer a max/min CPC cap on top of a value-based bid strategy. `[verify UI]` Example: a high-end furniture account sets a $10-$30 max CPC ceiling on top of a target-ROAS or maximize-value strategy, so the campaign never pays for a click above that ceiling, no matter how high-intent the user looks, because that click can never be profitable in that niche. The same portfolio-bidding capability also exists in what the source calls "SA3" (almost certainly Search Ads 360), but it is enterprise-only there. `[web check: confirm the tool's real name and which account tiers get access]`
5. On Search only, consider Smart Bidding Exploration to let a Target ROAS campaign explore ~10-30% outside its band. `[verify UI]`
6. Change Google budgets in ~20% increments upward (Google punishes abrupt jumps); budget cuts can be made quickly without the same instability.
7. Treat a campaign's "Limited by budget" flag as an indicator, not proof of real unspent opportunity. Source reports seeing it on almost every account regardless of spend level, including a client spending $5,000-$10,000/day on PMax inside a small total-addressable market (Australia). Confirm with other evidence (profitability at the margin, competitive saturation) before raising the budget on the strength of the flag alone.

**GMC feed optimization** `[6e67e3c7c443]` `[7421bd80f152]` `[f8b37ea10202]` `[ac4bf9ad64fd]`:
1. Rebuild product titles around actual historically-converting search terms (from Search Term Reports), pushing the brand name to the back (or dropping it if it has no recognition value) and front-loading descriptive/converting keywords instead of the bare product name.
2. For multi-variant SKUs, give each variant its own title/image/description targeting a different keyword cluster, even though they route to the same page.
3. Fix image aspect ratio to the platform's current default (source states 4:5 as of this recording - `[web check]`) via a supplementary feed if source images are natively a different ratio; build visual contrast against competitor listings rather than just maximizing raw CTR. Basis: the product image occupies roughly 70% of a shopping listing's visual real estate (source's own estimate), so after price it is the biggest driver of the click. Source frames the image like an ad hook, citing Eugene Schwartz's point that a headline's job is to get the right reader to read, not everyone - the goal is to attract the right shopper, not to maximize raw CTR from the wrong one.
4. Run separate feeds per currency for every region sold into - a single shared-currency feed causes a visible live-conversion display that suppresses CTR and conversion rate.
5. Roll any bulk title/feed changes out SLOWLY, in stages, monitoring CTR/CPC/ROAS after each batch - changing everything at once resets learning phases account-wide.

**90-day Google Ads rollout** `[fb780cdc68a6]`: (1) verify tracking (no GA4-as-primary-conversion, enhanced conversions + auto-tagging on); (2) build a structure map justifying every campaign beyond one; (3) run a PMax-specific check (asset groups, brand exclusions, signals, tROAS sanity, bidding strategy); (4) audit for wasted spend (orphan campaigns, unprofitable search terms, Display leakage); (5) health-check all ad assets/extensions; (6) run the feed check above, rolled out slowly.

**Root-cause diagnostic process** (the source's full "why did my Google account drop" framework) `[74d14b3daff2]` `[41fe6e957f15]` `[39809745fc54]`:
1. Before touching anything: check change history; extend the analysis window (avoid small-sample bias from very short periods); pull "Conversions (by conversion time)" instead of default conversions to avoid the false recent-days dip caused by Google's click-date attribution lag. `[verify UI]`
2. Level 1 (≈5 minutes): cross-channel check weighted by spend share (don't blame Google if it's a small % of total spend); decompose Revenue = Conversion Rate × AOV × Sessions and identify which moved; distinguish a true business KPI drop from an attribution-metric artifact; check whether the dip is just expected seasonality against forecast. Default rule of thumb: for most of the source's own clients, 80-90% of spend skews to Meta, so check Meta first as the default before Google, then confirm the actual order for this account with the spend-share math rather than assuming.
3. Levels 2-3: if it is a Google issue, start at the account level sorted by campaign cost descending, focus on the top 5 spenders, run a 90-180-day weekly-view scan of cost/conversions/conversion value/cost-per-conversion/ROAS/CTR, find the inflection date, then drill into the implicated campaign(s) and ad groups/asset groups. Materiality check: a campaign holding 10% of the Google budget that doubles its performance only moves the whole account by roughly 5% - this is the source's own reasoning for always starting at the top 5 spenders rather than wherever a stakeholder happens to point.
4. Identify campaign TYPE (PMax/Shopping/Search) because each has different failure modes: `[5bfbaaa5f311]` `[9fcbc9897f69]` `[ed7c1f01178a]`
   - PMax: warm/cold drift (check Search Term Report + Audience Report for brand/warm contamination), feed disapprovals, tROAS over-narrowing (verify via NC ROAS, not blended ROAS), product bloat / in-and-out-of-stock churn on high-spend products. Worked example: a product holding about 15% of a PMax campaign's spend goes out of stock for 4 days; this resets that one product's learning phase and drags down the whole campaign around it, which is why the source's agency asks clients up front to flag chronic stock volatility so the account can be structured around it.
   - Search: search-term drift before/after the inflection point, new competitors in Auction Insights, tROAS narrowing, Display accidentally re-enabled.
   - Shopping: feed health first (stock status, recent title/description changes, GMC errors), then search-partner placement leakage.
5. Levels 4-5: decompose the affected top-line metric into its formula components. Three core formulas: CPA = CPC ÷ Conversion Rate; Clicks = Impressions × CTR; attributed revenue = Clicks × Conversion Rate × Average Order Value. `[fee71c6e7a9f]` `[aaa2978ee3ef]`
   - CPC issue → treat CPC itself as a vanity metric on Google, Meta and TikTok - it only matters at the extremes. Check CPA first: a CPC rise matched by a proportional conversion-rate rise keeps CPA flat and is not a problem. Only if CPA actually moved, check Quality Score/Expected CTR/Ad Relevance/Landing Page Experience columns, new-competitor entry via Auction Insights, or a shift into premium auctions (ask whether the pricier clicks are actually converting better - if conversion rate hasn't risen to match, the premium auction isn't paying off). `[7748b51c5778]`
   - Conversion-rate issue → check tracking/latency, landing-page changes, audience-quality shift, a learning-phase reset, or an offer change. `[19d3b54fbeeb]`
   - AOV issue → decompose into new-customer AOV versus returning-customer AOV first and identify which one moved, then drill into units-per-transaction and average-unit-retail within that segment, before assuming an offer change is the cause. `[fee71c6e7a9f]`
   - Volume issue → check impression-share lost to budget vs. to rank/bid (if impressions AND clicks are both down together, it is almost never a budget problem - it is the bid, driven by quality score, new competitors or your own auction aggressiveness); check CTR decay from ad fatigue (source calls this rare on Google generally, more plausible on Search than on Shopping), audience mismatch, stale seasonal copy, or competitor price cuts (build a real-time competitor-price monitor to pull/deprioritize a product the moment a competitor undercuts it, rather than matching the discount). `[6ad389eace76]` `[1067951c3e42]`
6. Level 8 (apply the fix): default to a targeted fix, not a rebuild (a rebuild resets the learning phase and risks a compounding decline). Change one or a few things at a time when you need to know what actually worked; only "throw the kitchen sink" in a genuine emergency where the cause doesn't matter, only the fix. Size the fix to the size of the problem before applying it. `[d0bb3b7973363c0303bf38ae]` `[859209042dcd]`
7. Discipline check before touching the account: you must be able to state "this campaign is underperforming because [metric] dropped, driven by [submetric], caused by [root-cause trigger]" - if you cannot complete that sentence, don't make a change yet. `[34e9220c4fce]`

## 4. Rules, thresholds and numbers

| Rule / number | Threshold | Condition | Source's basis | Card id |
|---|---|---|---|---|
| Minimum ads per adset | 3 | Any spend level | Needed for Meta to sequence ads | `d45d9720ad61` |
| Typical ads per adset | 3-15 (up to 200 at very high spend) | Most accounts vs. very large accounts | Self-reported agency practice | `d45d9720ad61` |
| New ads/month to sustain growth | 100-300 | ~$250k+/month Meta spend | Self-reported | `f7d41ac1c4b7` |
| Ads-to-adset ratio example | 5-15 ads per adset across 2 campaigns × 10 adsets | ~$250k+/month | Self-reported illustrative structure | `f7d41ac1c4b7` |
| Test daily budget formula | (target conversions × expected CPA) ÷ duration in days | Any Meta test | Source's own formula | `2dbc68e5e82e` |
| Existing-customer budget formula | (# existing customers) × CPM × desired monthly frequency | Meta retargeting | Source's own formula, explicit rejection of % framing | `421e7aee0498` |
| Cold-adset frequency red flag | above ~2 on a cold ad (30-60 day lookback) | Meta, cold campaigns | Cites a Meta article ~4-5 years old (unverified) | `8868bab7b40d` |
| Mean spend per ad unit | ~$700-$1,500 | Meta, varies by account | Self-reported | `0f6cdc6afa17` |
| Simple creative-volume rule | 1 new ad per $1,000/month spend | Meta, AUD (roughly translates to USD) | Self-reported rule of thumb | `3ed85b1ffd80` |
| Production budget by spend tier | time/founder-led ($4-30k/mo); 25% of media ($30-100k/mo); ~10% of media / ~2.5% of revenue (>$100k/mo) | Meta creative production | Self-reported tiered guidance | `ec0c882e1e06` |
| Creative-strategist variable pay | ~3% of ad spend | Mid-size brands; breaks down at large scale | Self-reported | `e530277843071991748dd73e` |
| PMax good range without full customization | ≤ ~$15k-$20k/month | Small accounts | Self-reported | `299de15a096a` |
| Recommended PMax share of Google spend | ~20-40% | Mid-to-upper e-commerce | Self-reported | `299de15a096a` |
| Shopping vs Search split | 80-90% Shopping / 10-20% Search | E-commerce, non-B2B | Self-reported | `0103a8c9bea3` |
| Asset group product floor | ~15 products minimum, 1 product = red flag | PMax asset groups | Self-reported | `8c4e6e2d406b` |
| Asset group count | 3-20 typical range | PMax | Self-reported, based on internal testing | `8c4e6e2d406b` |
| RSA combination scale | ~2,700 possible combinations; ~250,000+ impressions to learn | Google Search RSAs | Source's own rough math (assumes ~100 impressions/combo, called "too low" a bar by the source itself) | `50d06003decd` |
| Google budget increase pacing | ~20% increments | Google Ads (contrast: more flexible on Meta/TikTok) | Self-reported | `50032f16a8cf` |
| GA4-as-primary-conversion attribution gap | ~10-15%+ missed conversions | Google Ads tracking | Self-reported `[web check]` | `37eb427df717` |
| Smart Bidding Exploration band | ~10-30% outside target ROAS | Google Search only | Self-reported `[verify UI]` | `f6bbad74d2b1` |
| Furniture max-CPC ceiling example | $10-$30 max CPC | High-end/high-bid niches, on top of portfolio bidding | Self-reported | `f6bbad74d2b1` |
| Image share of shopping-listing real estate | ~70% | Google Shopping/PMax listings | Self-reported | `f8b37ea10202` |
| "Limited by budget" false-positive example | flagged even at $5,000-$10,000/day PMax spend in a small TAM (Australia) | Any Google spend level | Self-reported | `50032f16a8cf` |
| Campaign materiality example | 10% of Google budget doubling in performance moves the whole account ~5% | Prioritizing which campaign to investigate first | Source's own worked example | `74d14b3daff2` |
| PMax stock-churn example | ~15% of campaign spend on one product, out of stock 4 days | PMax product bloat / learning reset | Self-reported | `5bfbaaa5f311` |

## 5. Diagnostics and checks

- **Cold-ad frequency check (Meta)**: pull last 30-60 days, ad level, cold campaigns only. Good: frequency ≤ ~2. Bad: frequency > 2 → creative fatigue / insufficient diversification. Fix: add volume and diversify concepts. `[8868bab7b40d]`
- **DPA ROAS sanity check (Meta)**: compare default ROAS to (a) ROAS with existing customers excluded and (b) incremental-attribution ROAS. Good: incremental ROAS still supports the spend level. Bad: a large gap between attributed and incremental ROAS → you are likely overspending on DPAs; do not scale DPAs past roughly $1,000/day on cold audiences (source's own ceiling claim). `[fa103e10c7f6]`
- **Hook/hold-rate check (Meta creative)**: compare an ad's hook rate (past 3 seconds) and hold rate (past 15 seconds, definitions vary) against the account average. Bad hook rate → try swapping only the hook. Bad hold rate → investigate the bridge specifically. `[9d81ae41459e]`
- **Metrics-reliability check order (Meta creative)**: read amount spent first (best proxy - Meta is voting with budget even when last-click ROAS looks unimpressive), then ROAS/CPA on 7-day-click or incremental attribution, then CTR/CPC as a fringe-only leading indicator, then hook/hold rate as diagnostic only. `[9d81ae41459e]`
- **Google - conversion-latency check**: always view "Conversions (by conversion time)," not default conversions, before judging the last 3-4 days of performance - default view will always look artificially bad in that window. `[verify UI]`
- **Google - cross-channel weight check**: before troubleshooting Google, weight the likely cause by each channel's share of total ad spend; check the dominant channel first.
- **Google - PMax warm/cold drift check**: review Search Term Report (brand leakage) and Audience Report (skew toward existing customers). Bad → brand exclusion has broken, or target ROAS is set too high.
- **Google - impression-share diagnosis**: if hitting daily budget cap → "lost to budget" (raise budget if profitable). If click volume AND impressions both fall while spend is flat → almost certainly "lost to rank/bid" → check Quality Score, new competitors, and your own bid aggressiveness.
- **Google - CPC quality check**: add Quality Score, Expected CTR, Ad Relevance, Landing Page Experience columns; whichever moved right after the drop date is the thing to fix. Landing Page Experience is the slowest to fix (depends on Google's own re-crawl cadence, can take weeks to months).
- **Google - competitor price check (Shopping)**: if a specific product's CTR/ROAS drops in a pattern matching a known competitor's promotions, monitor that competitor's pricing and deprioritize/pull the product rather than matching the discount.
- **Google/Meta/TikTok - CPC vanity-metric check**: don't react to a rising CPC on its own. Good: CPC up but conversion rate rose to match, so CPA is flat - not a problem. Bad: CPC up with conversion rate flat - now check Quality Score components, Auction Insights for new entrants, or a shift into premium auctions.
- **Google - "Limited by budget" sanity check**: don't treat the flag as proof of unspent opportunity by itself - the source sees it on nearly every account. Confirm with margin/profitability evidence before raising a budget on the strength of the flag alone.

## 6. Tools, settings and named features

- **Meta**: Creative Similarity Score (ask a Meta rep for access; most advertisers can't see it natively) `[verify UI]`; Advantage+ creative auto-optimization settings (advertiser-level, separate from per-ad toggle) `[verify UI]`; Columns → Compare attribution settings → Incremental attribution `[verify UI]`; portfolio-model / concept-per-adset structuring (source's own framework, not a platform feature).
- **Google Ads**: Performance Max (asset groups, listing groups, feed-only mode, URL Expansion / Automatically Created Assets settings) `[verify UI]`; brand-exclusion lists and PMax negative keywords (two separate mechanisms, use both) `[verify UI]`; Portfolio Bidding Strategies (cross-campaign learning-merge + min/max CPC caps) `[verify UI]`; the same portfolio-bidding capability also exists in what the source calls "SA3" (almost certainly Search Ads 360), enterprise-only there `[web check: confirm real tool name and access tier]`; Smart Bidding Exploration (Search only) `[verify UI]`; Auction Insights; "Search impression share lost (rank)" column `[verify UI]`; "Limited by budget" campaign status flag (treat as an indicator, not proof of unspent opportunity); Google Merchant Center (GMC) feed, multi-currency feeds; "Conversions (by conversion time)" custom column `[verify UI]`.
- **Third-party**: Triple Whale, named once as an example tool for reading new-customer (NC) ROAS on PMax - not the source's own tool, no endorsement detail given.
- **Named source's own offers** (commercial, unverified): a free creative-volume/financial-model calculator and a free account audit, both lead-gen offers gated at "$5 million a year" (stated once as "$5 million a month," likely a slip) in e-commerce/retail revenue.
- **AI usage**: source recommends a custom "Claude skill" (or equivalent LLM tool) built specifically for briefing/scriptwriting (a ~20-question intake producing a near-final script/brief), and for persona ideation refinement - but explicitly not for primary ideation or primary performance-analysis decisions.

## 7. Examples and case results

All of the following are self-reported by the source, with no independent verification, and several are explicitly recalled from memory rather than checked against records - treat as illustrative, not proof.

- **$25k/day (~$750k/month) account, 5-campaign structure** (testing/scaling/promo/advertorial/DPA) - presented as a real, currently-successful client account. `[d00fe7fd4c3b]`
- **$350k/month client with only 15 live ads**: agency reworked old assets up to ~60 ads with no new production, reportedly adding ~$40k/month in spend while cutting CAC 20-30% and lifting new-customer revenue by "about 28%" (recalled loosely). Reverted when the founder refused further creative investment (treated creative as a cost center) and the reworked assets eventually fatigued. Illustrates the source's core "creative as cost center vs revenue driver" thesis. `[1deded070dbd]`
- **"DPA death spiral" pattern**: six fashion-brand account audits within ~2 weeks, each spending ~80% of budget on DPAs with declining performance over the prior 6 months, traced to cutting top-of-funnel/creative spend because DPA ROAS looked strong. `[e800ec50f078]`
- **Sunglasses wholesaler**: product-level performance dips traced one-for-one to the biggest competitor discounting the same product on Google Shopping; agency built a real-time competitor-price-monitoring script to pull/deprioritize the product rather than match the discount. `[1067951c3e42]`
- **PMax Gmail/YouTube runaway spend**: a "couple hundred thousand"/month PMax client saw clicks spike and ROAS drop ~20% when PMax silently shifted spend into YouTube (2%→10%) and Gmail cold placements (~10%); Gmail placements count an email OPEN as a "click" without the user ever reaching the site. Fixed by switching to feed-only PMax. `[0d34948521a9]`
- **25 million-view VSL example** (IM8-adjacent gut-health ad, name inferred from product mentioned) running 3-4 years, used to illustrate awareness-stage sequencing and objection-handling structure - a durability claim, not a controlled-performance claim. `[4930a1df56a6]`
- **2,000+ ads/month, ~$4M spend, unprofitable** - used as the source's central "activity vs strategy" cautionary example. `[a9d4d1b724a5]`
- **Furniture max-CPC example**: a high-end furniture account layers a $10-$30 max-CPC ceiling on top of a target-ROAS/max-value bid strategy via portfolio bidding, since a $30 click can never be profitable in that niche no matter how high-intent the user looks. `[f6bbad74d2b1]`
- **"Limited by budget" false positive**: a PMax campaign spending $5,000-$10,000/day inside a small total-addressable market (Australia) is still flagged "Limited by budget," illustrating why the source treats the flag as an indicator, not proof of real unspent opportunity. `[50032f16a8cf]`
- **Campaign materiality math**: a campaign holding 10% of Google budget that doubles its own performance only moves the whole account by roughly 5% - the source's own reasoning for always starting a diagnostic at the top 5 spenders rather than wherever a metric was flagged. `[74d14b3daff2]`
- **PMax stock-churn example**: a product holding about 15% of a PMax campaign's spend goes out of stock for 4 days, resetting that product's learning phase and dragging the whole campaign; the source's agency now asks clients at onboarding to flag chronic stock volatility for this reason. `[5bfbaaa5f311]`

## 8. Mistakes the source warns about

- Confusing activity (raw ad volume) with strategy; launching high volume without a defined concept/persona/angle/offer standard.
- Misdiagnosing the actual creative bottleneck (assuming "more volume" fixes a problem that is actually format diversity, funnel-stage coverage, or partnership-ad absence).
- Treating creative production as a cost center instead of a revenue driver.
- Splitting one adset's funnel-stage creative into separate adsets and then reading the resulting (misleadingly different) ROAS numbers at face value, rather than blending them.
- Turning off a low-ROAS ad/adset that is actually hitting overall KPI, because of last-click attribution and hidden sequencing.
- Adding new ads to a currently-winning adset (resets the learning phase).
- Overspending on DPAs because their attributed ROAS looks inflated, while starving the top-of-funnel spend DPA performance actually depends on.
- Using existing-customer spend as a % of total spend as a KPI, instead of a dollar figure tied to frequency and profitability.
- Running SKAGs / hyper-segmented ad groups under modern Responsive Search Ads, starving them of the impression volume needed to learn.
- Leaving Display enabled inside Search campaigns; leaving Auto-Apply Recommendations on; skipping negative-keyword hygiene; using GA4 events as the primary conversion source.
- Raising Target ROAS repeatedly to "improve efficiency," not realizing it is narrowing the eligible audience toward warm users rather than improving genuine performance (the tROAS trap and its escalated form, the tROAS death spiral).
- Rebuilding/restructuring a Google account reactively instead of applying a targeted fix - a rebuild resets the learning phase and risks compounding the original decline.
- Jumping straight to a flagged submetric (bottom-up troubleshooting) instead of confirming top-down whether it matters at the business level at all.
- Duplicating adsets as a fatigue-recovery tactic (explicitly not recommended by the source, though acknowledged as still used by some practitioners).
- Reacting to a rising CPC by itself, on Google, Meta or TikTok, without first checking whether CPA actually moved - source treats CPC as a vanity metric that only matters at the extremes.
- Assuming a falling Search CTR means ad fatigue when audience mismatch is the more likely cause - source calls fatigue rare on Google generally, and even rarer on Shopping than on Search.
- Treating a "Limited by budget" flag as proof there is real unspent opportunity, instead of one signal to weigh against margin and competitive-saturation evidence.
- Maximizing raw click-through rate on a shopping-listing image instead of attracting the right shopper - a higher CTR from the wrong audience just buys worse-converting clicks.

## 9. Caveats, conflicts and what is missing

- **Everything client-specific in this source is self-reported**, often explicitly recalled "off the top of my head" (e.g. the $350k/month case's exact CAC/revenue figures). No underlying data, screenshots, or third-party verification is shown in the transcript itself.
- **The agency's own commercial incentive runs through the whole source**: both the free-audit lead-gen offer and the hiring CTA repeat multiple times, and the "$5 million a year" (once stated as "a month," an apparent inconsistency) revenue gate for the free audit should be read as a sales funnel, not a neutral benchmark.
- **Explicit named disagreement**: the source directly pushes back on Alex Hormozi's "offer is king" framing, ranking offer below angle in testing priority - flagged in the source text itself as a deliberate contrarian point, not a settled industry consensus.
- **Explicit self-correction**: the source states its own earlier "PMax campaigns are terrible" video was "a bit of a biased view... contextual to the moment," now walked back to "PMax isn't the enemy" if configured well - a useful signal that the source revises stated positions over time and this file's Google Ads section could similarly age.
- **Time-sensitive tactics flagged by the source itself**: the second-ad-account bidding-diversification strategy ("what I'd say 6 months ago is different from today"), the trial-reels tactic (explicitly dated "as of April 2026"), and the partnership-ads "arbitrage window" (source suspects it's closing as more advertisers catch on) should all be re-verified before relying on them.
- **Platform mechanics tagged `[verify UI]` throughout this file** (PMax settings, brand exclusion methods, Smart Bidding Exploration, portfolio bidding strategies, GMC image ratio, Google's Gmail click-counting behavior, DSA deprecation, current match-type semantics) should be checked live before operational use - Google and Meta both ship product changes frequently, and the source itself notes this repeatedly.
- **The source gives no primary sourcing for several cited "facts"**: the ~4-5-year-old Meta article on identical-creative frequency decay, the informal "other agency owners" claim about PMax over-attributing 50%+ of conversions, and the "270,000 impressions to learn an RSA" math (the source's own rough estimate, explicitly caveated as using a bar it calls "too low"). `[web check: the Meta frequency-decay article specifically, if this claim is used in a client-facing deliverable]`
- **What this part does not cover** (likely in part 1 or the neighbor folders): sub-$50k and $50k-$250k Meta account structures, the start of concept-level testing discussion, offer mechanics/discount economics, unit-economics/finance formulas, and any landing-page or email/retention content - this source is overwhelmingly a paid-media and creative-production playbook, with only glancing references to inventory/balance-sheet ops and none to email/retention as a topic in its own right within this part.
- **Numbering/spelling inconsistencies in the transcript itself** are noted inline above (the agency's hiring-email domain spelled three different ways; the audit revenue gate stated once as "a month" instead of "a year") - these are transcription artifacts, not deliberate claims, but are preserved here rather than silently corrected.
- **Tail slice verified**: source lines 1301 to 1594 (portfolio bidding and SA360/"SA3", Google budget pacing and the "Limited by budget" flag, GMC title/image mechanics including the real-estate and Eugene Schwartz points, the close of the 90-day rollout, and the full root-cause diagnostic walkthrough through to the closing sign-off) have been read in full and cross-checked against this file. Most of the content was already covered; the additions above are the specific numbers, worked examples and finer mechanics (SA360, the furniture max-CPC example, the 70% image-real-estate figure, the 80-90% Meta-first default, the CPC-as-vanity-metric and AOV-decomposition nuances, the campaign-materiality math, and the PMax stock-churn example) that were missing.

## 10. Card index

All 107 card ids from `data/library-v3/cards.json` that this part's content maps to (in source order; the remaining ~91 cards for this source's part 1 are not listed here):

- `dac13325f1bc4a2422d0461d` - Concept Matrix: Persona × Angle × Offer × Ad Type
- `f7d41ac1c4b7b2a3d0ab9640` - Ad Volume Targets and Ad-to-Ad-Set Ratio at Scale
- `159829ec73747f9033f8e0b6` - Plan advertising continuity and test bid strategies within permitted account use
- `0dd3aee5c557d07ab7335b23` - International Expansion Without Ad-Account Sprawl
- `d00fe7fd4c3bc3d4d6b859aa` - Five-Campaign Account Structure for ~$750K/Month Spend
- `34509036c871a9d0e70bbca1` - What Stays Fixed as Spend Scales
- `9190a63c0c09abd211a44489` - ABO vs CBO: Choose Your Risk/Efficiency Profile
- `d45d9720ad61425e535c8b39` - Ad Set Composition: 3 to 15 Ads, Same Audience
- `b3d6e61e0a7acbce5390415c` - Consolidate Funnel Stages in One Ad Set to Avoid Biased Readouts
- `afc96213f0220b2b40d73e66` - Name Ad Sets by Persona, Angle, Offer, Content Type, Date
- `34161704728554cedff6859f` - Retargeting Is a Capped Support Layer, Not a Growth Driver
- `e800ec50f078340338ff16dc` - DPAs Only Look Great Because They Sit at the Point of Purchase
- `421e7aee0498049003e18790` - Budget Existing-Customer Spend in Dollars, Not as a Percentage
- `4101599d2222430e164ae8a6` - Settings to Turn Off: Flexible Ads, One-Day View, Auto Creative Optimisations
- `00054444d5a7fd9f66324855` - Maintain Audience Segment Sync Audit (CRM → Meta)
- `2dbc68e5e82e9bcccd55f251` - Calculate Test Budget from Conversions, CPA and Duration
- `01aea02748b6b0f0f82d4650` - Creative as the Growth Lever, Portfolio Model Over Hero Ads
- `1f2c53df551efc1f54dcca03` - Diagnose Creative Bottlenecks Before Adding Volume
- `4bddfe132ec20c19e34cd489` - How Andromeda Reversed Targeting: Ads Go In, Meta Finds the Audience
- `90fdf6692e74842c84d0d701` - Post-Andromeda account structure: creative as targeting
- `8868bab7b40d1a9ad318dc90` - Creative similarity, frequency and reach decay
- `a96c890428cb603dfc91c938` - Creative sequencing and why not to kill low-ROAS ads
- `5b34bfe523b3646727007194` - Metric reliability by account level
- `0f6cdc6afa17199ccb38606f` - Four components of concept diversity
- `e218c186102ad2fcaa178649` - Persona construction: archetypes not demographics
- `010fe64918f47b6230e2899e` - Building an angle: assemble the components that fit the persona
- `bc784b37d696d5dab915a039` - Testing priority order: angle before offer, persona or format
- `a290245745d6356061056b51` - Structuring ad sets by concept for a usable learning loop
- `c9cab64dcc732a73997df6a1` - Worked concept build: persona, angle, offer, format
- `9c15aae468c216642d523cd1` - Hooks as relevance promises, not bait
- `b86b75e9bce9d133f6fb0bee` - Hook grading criteria and reusable hook types
- `312400b7ccabfa09a8d8ea3a` - Scroll-stopping hook mechanisms and when each works
- `19ad3f95102c20c8fa77f85b` - Bridge scripting: never jump from hook to product
- `5e663b2acdc67893d08eb72c` - Hook testing still works post-Andromeda - and it's cheap
- `a7eee2af51378d570b51c2d5` - Five questions to choose the right ad format
- `bc1fb281f2e320597effcf3c` - Cost of production versus contribution margin per ad - the image vs video decision
- `8004c3204936fdf92a1fc4e1` - Advertorial statics: make the ad look like an organic post
- `9b60e827e51de46d55770f27` - Review/round-up advertorial funnel with a dermatologist framing
- `ba82a65b35b4274277febfee` - Long-form copy statics for 50+ demographics
- `4930a1df56a64e44337df968` - VSSL script structure: persona call-out, objection handling, problem agitation, then late product reveal
- `6b0a6f82bca68f979f4671a6` - Objection-handling UGC spliced onto the front of a VSSL
- `fa103e10c7f6d2eea8f1a37f` - Incremental attribution: read DPA ROAS correctly before scaling bottom of funnel
- `3ae202bfc21a073af1b7972d` - Allocate creative effort by funnel need with a normalized budget
- `c9a888b1f02eaed5a2316c4a` - Partnership ads: using creator audience data for cold targeting
- `61ad59932aa7f6f212be0c8f` - Testing cycle: hypothesis, volume, launch, analyze, scale, iterate
- `69a7c7195336347e3c893a05` - When to add ads to an adset vs launch a new adset
- `9d81ae41459e6d2a8b40704a` - Metrics ranked by reliability for judging creative
- `345054044d8c9ea791effb5f` - ABO vs CBO: risk tolerance trade-off via Pareto's principle
- `22138a212ab57a3dfb575f6f` - Fix the 90/10 desire vs pain-point creative imbalance
- `140b0e63185d2bf301ecb169` - Bottom-of-funnel retargeting as objection handling
- `ee7169c0fb38e9f344f34b13` - Diagnose bottom-of-funnel objections before writing BOF creative
- `a9d4d1b724a51e7ae9343b1c` - Creative volume hierarchy: volume beats concept, hook and editing
- `3ed85b1ffd807d8c9f7e13b9` - Calculate creative volume from spend or from hit-rate back-propagation
- `ec0c882e1e06fd62cfa30df2` - Set the creative production budget as a share of media spend by scale
- `1deded070dbd1fb935ac9171` - Treat creative as a revenue driver, not a cost centre: the redistribution math
- `bd9a8085893c6f070f6c664f` - Test creative volume cheaply with trial reels before ad manager
- `02326c43f14a507969210765` - Understand creative fatigue as spend capacity plus audience size
- `3ebec38bdf567ce40b0cc022` - Match persona breadth to spend capacity; go specific first, broad later
- `e6675d2d6fbe70089a115818` - Recover spend from fatiguing ads with four tactics
- `d3fd934664cb45da84305530` - Run portfolio management across ads, products and the balance sheet
- `ec070bd2a240ca32e8395bcf` - Budget creative effort across replication, iteration and net-new
- `0b902cecf95bd0bd40abf928` - Brief creators with their past work plus the brief behind it
- `e530277843071991748dd73e` - Build the creative production team by spend tier
- `3412220fa6466ce136241e08` - Automate the middle of the creative process with AI, not the ends
- `748e28ee574a0b2a3c3c62bf` - Match persona callouts and creative to audience warmth and account scale
- `92200eb95b453fb8750b9043` - Google Ads structure: consolidation beats segmentation, unless commercial reality forces segmentation
- `c1d0d2b869b83eb8fbdb0400` - Recognise Google spend as either over-spending or under-spending
- `46006b8261d1aa639ab58921` - Apply the five major Google Ads shifts when restructuring in 2026
- `5d8be0c613b5b6078c3af519` - Justify every campaign beyond one (justification-based account structure)
- `0103a8c9bea0ea38194f4916` - Route 80-90% of ecommerce spend to Shopping, not Search
- `50d06003decdf6ab69fa15b3` - Use single-topic ad groups (STAG) instead of SKAGs
- `8c4e6e2d406bfb52a74c2d3c` - Structure PMax asset groups by product type with matched listing groups
- `299de15a096ab2575b0aec6a` - Diagnose why PMax segmentation is worth breaking consolidation
- `2b7d05cb2e3f65ccef03542e` - Set brand exclusions (two ways) on PMax to stop pure retargeting
- `0d34948521a961485602c895` - Run feed-only PMax to force Shopping placement and fix runaway spend
- `e1258c1c01bdaa3abfbe0519` - Move to tROAS for stability, then avoid the over-tightening trap
- `926e49f0a825e63e28788e7d` - Build a feeder strategy: cold funnel campaign feeding a high-tROAS retargeter
- `cfc0bb5b70ee282ce477cd1f` - Standard Shopping structures: top-sellers split, feeder, and labelizer
- `28532c9e9701c5d4f375a954` - Run Search campaigns only for the right cases; use STAGs and front-load negatives
- `bb73c455dd9a774b720b284f` - Treat landing-page testing as the biggest Search lever
- `37eb427df7175562e588b898` - Fix seven common Google Ads account hygiene mistakes
- `7881306718d910374f4372f3` - Google Ads bidding: expansive vs restrictive strategies
- `791e1a8f256b8d933848c321` - Prefer value-based bidding for ecommerce over lowest-CPA bidding
- `508646f782d913537fcb3f22` - Detect and stop the tROAS death spiral
- `f6bbad74d2b1fc09c322efa9` - Merge campaign learnings with portfolio bidding strategies
- `50032f16a8cf75faea1b48cd` - Change Google Ads budgets and strategies slowly, downward faster than upward
- `6e67e3c7c4432dabff6f7ff2` - Optimise Google Merchant Center titles from search term data
- `7421bd80f1529f7e897598b5` - Spin variant listings to cover multiple keyword pools
- `f8b37ea10202cfe7e5130d49` - Fix feed image aspect ratios and build contrast for click-through
- `ac4bf9ad64fd12e1ce92b00e` - Set up separate feeds per currency for international Shopping
- `fb780cdc68aaf637eac0cfb9` - Sequence the 90-day Google Ads improvement rollout
- `74278f16f035e15ba11dd134` - Run a 5-minute business-level diagnostic before touching Google Ads
- `41fe6e957f15627198531c6f` - Complete three pre-checks before any Google Ads diagnosis
- `39809745fc544314447fbb64` - Drill from account to campaign to ad group to find the inflection point
- `5bfbaaa5f311822c84555d8f` - Diagnose PMax failures: warm/cold drift, disapprovals, tROAS narrowing, product bloat
- `9fcbc9897f69f7101d921ad9` - Diagnose Search campaign failures: search terms, auctions, tROAS, display leakage
- `ed7c1f01178816b95a5b2d32` - Diagnose Shopping campaign failures through the feed first
- `fee71c6e7a9f469d10e6ee47` - Decompose campaign KPIs via submetric formulas for root cause analysis
- `aaa2978ee3ef8d8bb27dda44` - Use revenue equation to route ecommerce diagnosis
- `74d14b3daff2e02b9f07dd6c` - Google Ads Diagnostic Tree: Top-Down Root Cause Analysis
- `7748b51c57788bb830d64086` - Diagnosing Rising CPC: Three Causes and When It Actually Matters
- `19d3b54fbeeb31f3bbd23c2d` - Diagnosing Falling Conversion Rate: Tracking, Landing Page, Audience, Learning, Offer
- `6ad389eace765c8bd514357a` - Diagnosing Volume Declines: Impressions, Impression Share and CTR
- `1067951c3e42f2b344ca8de5` - Competitor Price Monitoring to Pull Products Before Margin Erosion
- `d0bb3b7973363c0303bf38ae` - Fix Before Rebuild: Avoiding the Learning-Phase Death Spiral
- `859209042dcd562e2d7dcd47` - Bundling Versus Isolating Fixes: Choosing Based on Severity
- `34e9220c4fce7dd644bd07aa` - Pre-Investigation Checks Before Touching Any Ad Account
