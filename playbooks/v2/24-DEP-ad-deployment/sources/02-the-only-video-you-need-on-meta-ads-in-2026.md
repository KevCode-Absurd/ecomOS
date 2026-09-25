# The Only Video You Need On Meta Ads In 2026

source_id: 1hoq9QqGRfyOOCLm-TxAVaa_l8S1R9dFX  |  folder: /24-DEP-ad-deployment (moved from /11-ADC-ad-copy-deployment)  |  cards: 48  |  words: 22,222  |  type: transcript (1 long YouTube video, about 2 hours, auto-captioned, no timestamps, whiteboard drawings referred to but not shown)

credibility: One unnamed presenter from an Australian performance agency. The library header names it Blue Sense Digital; the transcript's hiring email domain reads "bluensdigital.com.au". The agency says it only works with 8 and 9 figure brands, that 60% of its client portfolio spends more than $250k a month on Meta, and that it has "over 150 million in ad spend" connected to its business manager. It sells account management and offers a free audit to brands doing more than $5M a year online; it also recruits media buyers. Evidence is the agency's aggregated spend report (CPM inflation), its own audits (furniture brand, 6 fashion brands, $10k AOV brand), 1 client account at $750k a month, and the presenter's opinion. Meta's own "breakdown effect" help page is cited. No controlled tests. The presenter says openly that he talks in "frameworks rather than actuals" and that some preferences (1 ad account, ABO or CBO) reflect agency labor or personal bias.

date signals: Title says 2026. Names Andromeda and a second Meta update the transcript spells "Gemmin" (a card reads it as Gemini) [web check: likely Meta's GEM ads model]. Says Advantage+ campaigns launched "like 2 years ago" with an "existing customer spend cap" percentage field. Uses the current name "flexible ads" and warns the name changes. Refers to iOS 14 (once "iOS 14.2") as a past turning point and to 2018, 2019 and 2020 practice as dated. References 2 of the agency's own videos ("Meta Ads creative strategy in 2026", and an attribution video posted "18th of May" called "If your ad account looks good but profit isn't"). The presenter says his second-ad-account advice changes about every 6 months. File modified 2026-09-21.

## 1. What this source is for

It helps an operator design, audit or restructure a Meta ad account for an ecommerce brand at any spend tier: under $50k a month, $50k to $250k, and $250k plus. It covers how Meta allocates spend (last-click display versus multi-touch optimization, the breakdown effect, broad targeting as a vector space), when to consolidate and when to segment, ABO versus CBO, concept-based ad sets (persona, angle, offer, ad type), test budgets, durations and kill rules, scaling campaigns, retargeting, DPA and existing-customer budgets, page caps, extra ad accounts, and settings to turn off. It is about structure and budget flow. Creative production and ad quality belong to folder 10-MCR; attribution models and MMM belong to 06-MEA.

## 2. Principles

1. **Meta optimizes for revenue per user per minute, so costs keep rising.** Condition: always. Meta grows revenue by adding ad inventory (more ads per feed, more surfaces; the presenter recalls 1 ad per 5 to 6 posts 6 years ago versus 3 ads in a row now) and by raising CPMs. Meta cannot make all advertisers unprofitable, so each update (Andromeda, "Gemmin" and smaller ones) aims to raise ad-serving efficiency and conversion rates so it can charge more. Evidence: the agency's aggregated report over 3 years shows about 20% to 30% CPM inflation a year, cyclical around Black Friday, above general dollar inflation. Implication: a creative or offer that broke even 12 months ago may now lose money; keep improving creative and landing pages. [5b99bf6d671d] [needs brand data: own CPM trend by year] [web check: current Meta CPM inflation]

2. **What the platform shows is not what Meta optimizes.** Condition: whenever you judge ads. The UI shows last-click: full credit to the final ad clicked. Meta optimizes across multi-touch sequences; with 3 ads in a click path it likely gives about 1/3 credit to each in the back end (presenter's inference). Ad-level ROAS is what you see; Meta actually optimizes toward the CPA target at the ad set level, because bidding and optimization are inherited from the ad set. That is why cost caps are set at ad set level, never ad level. So judge creative and move budget at the ad set level. When 3 ads under 1 ad set each spend $5,000 at very different returns, do not simply turn off the 2 weaker ones; they may be doing earlier work in the sequence. [9ede69b02ec7] [b722b2c086bc]

3. **The breakdown effect: trust Meta's spend split across breakdowns most of the time.** Condition: when a breakdown (age, gender, placement, region) or ad list shows a higher-ROAS segment getting less spend. Breakdown data is blended and ignores incremental return. Example: Stories at 4x ROAS, Feed at 3x, but Feed holds 80% of spend. Meta has tried pushing more into Stories and found poor incremental return. Ad example: an ad at $300 a day earns nothing more at $320 (0x incremental), while an ad at $200 a day earns more when pushed to $250 (say 2x incremental), so budget goes to the second. Meta documents this publicly [web check: Meta help page "breakdown effect"]. Rule: unless you are an expert buyer of 6 to 7 years, do not make changes based on complex breakdowns or ad-level ROAS; do not launch a Stories-only campaign because Stories look better. There are real cases where the split is wrong, but spotting them needs expertise. This still applies at $250k plus. [528465d5cc14]

4. **The creative is the targeting (Andromeda).** Condition: cold prospecting. Old model: choose interests and audiences, then load creative. Current model: load creative, leave targeting broad, and Meta reads the creative and serves it to relevant people (the retrieval system). Interests record interaction, not intent (posting "I hate dogs" gets you tagged as interested in dogs). A report cited by the presenter (he is unsure whether from Meta) says about 30% of people in an interest group were wrongly assigned [web check: source of the 30% misassignment figure]. Broad targeting works like a vector space of about 10,000 dimensions; users move in real time with what they engage with, cluster naturally, and Meta finds the hotspots where people buy. As you scale, the targeted area widens into colder people who are less convinced, which is why ads fatigue and campaigns die when scaled. [4c81bdf1685a]

5. **Interest targeting and lookalike audiences are dead; test pages instead.** Condition: source's strong opinion for all spend tiers. "Very strongly of the belief this shouldn't be in your account." Spend that test effort on landing page split tests and CRO, which can make an inflection in conversion rate. [4c81bdf1685a] [9997eb5233ac]

6. **Consolidation beats segmentation, because conversion data is siloed at the campaign level.** Condition: general default, strongest at low conversion volume. All major platforms (Meta, Google, TikTok, Pinterest) use campaign, ad set (ad group), ad. Some signal is shared between campaigns, but not all. 100 conversions a month split over 4 campaigns gives each 25, so small sample bias makes each optimize worse. Accounts often improve once they pass about 100 to 200 conversions a month. At the ad set level more data is shared and campaign data inherits down, so segmenting or consolidating ad sets swings efficiency only about 5% to 10% (noticeable at scale). [7230fc5fab8f] [9b521e4ff188]

7. **Campaign segmentation exists for commercial reasons, not for its own sake.** Condition: when you add a campaign. Valid reasons the source gives: budgets that must flow through different campaigns over time (a promotion that rolls into something else), separate KPI and reporting, and different business units or personas (a pets category and a children category). [7230fc5fab8f] [568f98fcc9aa]

8. **Total consolidation (1 campaign, 1 ad set, all ads) is wrong for about 90% of brands.** Condition: segment when any of these 3 hold. (a) Different unit economics: 70% gross margin on one range and 60% on another, or grade A to D inventory where slow stock must be discounted hard; in 1 campaign, spend drifts to heavy-sale items with compressed margin, worse contribution margin, and sale messaging pushed to the whole funnel. (b) Non-overlapping audiences: a men's and women's activewear range in 1 ad set confuses targeting, which lives at ad set level; women's ads serve to men. Men's ads to women is less bad (women buy for partners) but the reverse rarely pays. (c) High AOV or low conversion volume: a client at $10,000 AOV doing about $50k a day gets about 5 orders a day, so CBO cannot optimize on purchases and falls back to upstream signals (CTR, CPC, hold rate). About 10% of brands can run full consolidation. [ebff07a9e6f2] [1589854e06d9]

9. **CPC and CTR barely predict return except at the extremes.** Condition: when an algorithm or a buyer allocates on soft metrics. Source's claim from large data sets: very high CPC does mean very low ROI, but otherwise CPC shows almost no correlation with return. The transcript garbles the second half of this claim. [1589854e06d9] [needs brand data: CPC versus ROAS scatter by ad]

10. **Letting the machine distribute spend is efficient but concentrates risk.** Condition: consolidated CBO. Meta usually allocates better than you, but on an 80/20 Pareto split: 20% of ads get 80% of spend. Downsides: 100 new ads a month may get no spend and no test; paid influencer partnership ads may get nothing; 1 winner that will fatigue leaves no backup. Forced (segmented) spend de-risks and supports testing, but a novice doing it carelessly burns money. For a $10M a year in-house business, a first-year buyer should run consolidated CBO; an experienced buyer who weighs risk against profit should run segmented or in-between. [1589854e06d9] [2f66cf4f65c6]

11. **Media buying still matters, but only for a narrow set of levers and mostly at high spend.** Condition: spend tier. At $100 a day it is not a big lever. At $100k to $300k a month good buying may give a 10% to 20% efficiency lift. At about $1M a month even 3% to 4% is worth a dedicated person. Dead: daily bid tweaks with cost or bid caps (might squeeze about 5% for an hour a day; the same hour on creative could double or triple the account), daily budget pacing on smaller accounts (decisions on tiny samples), interest targeting, lookalikes. Still matters: account structure and architecture aligned to commercial goals, concept-level segmentation at the ad set level, and control of dollar or percent allocation to existing customers. Note the internal tension: 10% to 20% lift at $100k to $300k versus 3% to 4% at $1M. [9997eb5233ac]

12. **2 non-negotiables for any structure: data integrity and commercial alignment.** Condition: every structure at every tier. Data integrity: the structure must produce readable, actionable data so you can run decision loops (read, decide, wait, decide again); unreadable structures force restructures. Commercial alignment: the structure must reflect products, margins and goals; it must not hide a product or category that needs spend or will become sale inventory; low-margin lines that cannot support paid acquisition, and categories with their own priority or KPI, must show in the structure. [b8107473f4c3] [f623a968dbf2] [3da640845924]

13. **There is no universal structure.** Condition: always. Structure depends on product categories, margin spread, personas, regions and creative throughput. Two brands at the same revenue can need very different structures (see Section 7). [b8107473f4c3]

14. **Never touch something that is working; fork it.** Condition: an ad set hitting KPI. The source calls this the number 1 rule of Meta media buying. Put new creative for that concept in a new ad set beside it. If the ad set is not hitting KPI, add new creative into it to try to make it perform. Expect sprawl: 6 of 10 ad sets may belong to 1 winning concept. [a95742238877] [ba414cee7839] [b722b2c086bc]

15. **A concept is persona + angle + offer (+ ad type), and each ad set holds one concept.** Condition: cold campaigns at every tier, including $300k a day. Ad type is flexible under a concept. Ad sets learn somewhat in isolation, so unrelated creative in 1 ad set confuses targeting. Concept-level KPI gives directional creative feedback: losing concepts get more attention, winning concepts get more volume. [b722b2c086bc] [65e0503d7bc4]

16. **Concept testing tells you who your customer is.** Condition: $50k plus, with enough volume per concept. It shows which personas you acquire and in what share (for example 40% smokers, 40% brides). Use it to steer landing pages, offers, product expansion and retention flows. If concepts stay very broad, you get no accurate persona insight and inefficiency bleeds into the rest of the business. [ac6d263bd22b]

17. **Retargeting is a capped support layer, not a growth driver.** Condition: all retargeting (website visitors, DPA, existing customers). On cold, ask "where can we spend more?" (abundance). On retargeting, ask "where can we spend less?" (scarcity), on every platform (Meta, TikTok, Pinterest), because the top end of retargeting spend is often not incremental and brands almost always overspend. [028483f1e7af] [9d8a9963309a]

18. **DPA performance mirrors top-of-funnel investment.** Condition: any account running DPAs. DPAs place just before purchase, so they take more credit than they earn and look better than they are. Raise top-of-funnel spend and DPA ROAS rises; cut it and DPA ROAS falls. Cutting creative or prospecting because DPAs "hold up performance" causes the DPA death spiral. [cf36e5f30572] [805594665ccc]

19. **Existing-customer spend is a dollar and frequency decision, not a percentage.** Condition: any existing-customer targeting. The percentage cap field in Advantage+ framed everyone wrongly. A percentage moves with the size of the customer pool and with new-customer budget, so it is useless. Judge on 2 things: is the extra spend profitable (another $10 or $1,000 a day returns enough revenue to pay for itself and profit), and what is the frequency. 20% of spend at a frequency of 50 per 30 days is over-spend; 20% at a frequency of 1 is likely under-spend. [3a48f7471999]

20. **Add structure as spend and complexity grow; keep the fundamentals.** Condition: moving between tiers. What never changes: the 2 non-negotiables, the breakdown effect, the concept framework, and KPI at ad set and campaign level. [568f98fcc9aa] [7350eaba553e]

21. **ABO versus CBO is a risk choice and largely personal preference.** Condition: every account except high AOV with low volume. CBO: more risk, better efficiency, spend flows to top ads and ad sets, but new or expensive creative (a $20,000 shoot, a $20,000 60-day influencer partnership ad) may get no spend. ABO: forces spend through every new ad set, lower risk, slightly lower ROI (presenter's hypothetical: about 10% lower). Both have run most of the spend on very large accounts (the transcript garbles the figures as "a4 million a day" for ABO and "quart million a day" for CBO). It comes down to how much you trust the algorithm; forcing a minimum spend on an ad Meta ignored and seeing it win erodes that trust. Exception: with very high AOV and low conversion volume, do not use CBO, because it allocates on soft metrics (CTR, CPC). [2f66cf4f65c6] [1589854e06d9]

22. **Group all funnel stages for one persona in one ad set.** Condition: ads that target the same persona and product. Minimum 3 ads so the ad set can sequence (people need to see an ad 2 to 6 times before buying). Top, middle and bottom of funnel ads can share an ad set. The source leans toward consolidation partly for machine learning, but mainly because humans misread split ad sets (see Section 5). [d6c0209e9d6b]

## 3. Procedures

### 3.1 Design a custom structure (any tier)
1. Confirm the 2 non-negotiables are goals: readable data, commercial alignment. [b8107473f4c3]
2. Answer the 5 diagnostic questions [b8107473f4c3]:
   1. How many product categories? More categories with different goals usually need more segmentation.
   2. How wide is the margin spread across categories? Wide spread needs structure that stops low-margin items soaking up spend. [needs brand data: gross margin by category, post-discount]
   3. Are there multiple personas that do not overlap? Non-overlapping personas go into the structure; slight tweaks of the same person do not.
   4. How many regions? Multiple regions usually need campaign segmentation to control spend and sell-through, especially where inventory is held in-country or regions have their own revenue targets. [needs brand data: where stock sits, regional targets]
   5. What is the creative throughput? 10 ads a month allows little segmentation; 2,000 a month needs a methodical path from testing into scaling. [needs brand data: new ads per month]
3. Pick the spend-tier template (3.2, 3.5 or 3.6) as a starting point, then adapt it.
4. Put segmentation at the ad set level before multiplying campaigns, where you can. [ebff07a9e6f2] [49146dda7d03]
5. Run the 4-question validation (3.14). If any answer is no, restructure. [3da640845924]

### 3.2 Generic structure under $50k a month
The source says this is not ideal or custom, only a safe default. [ba414cee7839] [568f98fcc9aa]
1. **Testing campaign** (may be all you need at this tier). ABO or CBO (see 3.10). Ad sets by concept. 3 to 5 creatives per ad set; more if you have the volume. [ba414cee7839]
2. Exclude existing customers from the testing campaign, so a few repeat buyers do not make a concept look better than it is. The source says this matters less at this scale but should still be done. [fb9db4eb1b28] [verify UI]
3. Set attribution to 7-day click for data integrity. [fb9db4eb1b28] [verify UI]
4. New creative for a concept: ad set not hitting KPI, add it in; ad set hitting KPI, launch a new ad set for the same concept (3.8). [a95742238877]
5. **Scaling campaign** only when an ad set clearly beats target (the example is above a 5x target return) with strong soft metrics and has reached its spend equilibrium (3.9). KPI it at campaign level; no ad set segmentation in it. Exclude existing customers in it too. [0e642b4c3a8c] [b8a2663f518f]
6. **Retargeting campaign**: optional. Skip a website-visitor campaign in about 90% of accounts (check 5.3). Add a small existing-customer campaign only if repeat purchase is expected (supplements, low AOV subscription: yes; furniture: no). Keep it low, controlled, and judged by frequency. At this tier most businesses are new with few existing customers. [ccf942b9f2c8] [needs brand data: repeat purchase rate]
7. KPIs: testing at ad set level against target CPA or ROAS over a reasonable rolling window, never shorter than 5 days at this tier. Hitting KPI: raise budget about 20% a day. Missing KPI: diagnose what was wrong in the creative, make more ads and concepts, then wind the ad set down or off. Retargeting: incremental ROAS via an attribution breakdown, and frequency not above 7 on a 30-day window. [b8a2663f518f]
8. Why it works here: consolidated for low conversion volume, structured testing because there is likely no big winner yet, and little product or business complexity. [568f98fcc9aa]

### 3.3 Size a creative test: kill-rule method (3x or 5x CPA)
[87a85788a663]
1. Take target CPA (example $50 per customer).
2. Spend threshold = 3 x target CPA ($150) at the ad set (concept) level.
3. At the threshold: 3 or 4 conversions, keep running; 2, yellow light, run about another $50 then decide; 0 or 1, cut.
4. Source's preference when the client allows: wait to 5 x target CPA ($250). No yellow light at 5x; the call is strictly yes or no. Reason: early spend is Meta learning who to target, and efficiency usually improves after that.
5. Apply to ad sets, not single ads.

### 3.4 Size a test: formula method (daily budget)
[1c683e007b76] [57a5a1e787d4]
1. Set the stat threshold: how many conversions will you call significant (5, 10, 20?).
2. Set learning speed: over how many days (3, 7, 14, 30?).
3. Daily test budget = (target conversions x expected CPA) ÷ test duration in days.
4. Source example: 20 conversions x $100 CPA ÷ 14 days = about $143 a day.
5. Compare with Meta's advice of 50 conversions per 7 days to exit learning: 50 x $100 ÷ 7 = about $714 a day for 1 concept ad set; 10 such tests = about $7,000 a day. The source calls this unrealistic for about 99% of advertisers and says it is a common mistake to set ad set budgets this way. [web check: current Meta learning phase threshold]
6. Decide before launch what result ends the test and what follows (scale, kill, extend). [1c683e007b76]
Note: card 57a5a1e787d4 gives a 20 x $30 = $600, about $86 a day over 7 days example that is not in the source text; the source's own example is the $143 one.

### 3.5 Set test duration
[f88304f4647b]
1. Check daily seasonality: tests launched on a strong day look better regardless of creative. [needs brand data: revenue by weekday]
2. Check time to purchase: buyers typically need 2, 3 or 4 impressions and maybe a couple of clicks over 3 to 4 days. A 1-day test warms people, then other ads convert them in retargeting and you kill the ad that did the work. This applies on Google and other platforms too. [needs brand data: time from first visit to purchase]
3. Default to 1 week.
4. Large, stable business with short time to purchase: 3 to 4 days.
5. Tiny budget, long time to purchase, heavy daily seasonality: 10 to 14 days.
6. Match the read window to volume: 3 conversions in 3 days cannot support 3-day reads; 1,000 conversions a day can support 2-day reads. Under $50k a month, no reads shorter than 5 days. [b8a2663f518f]
Goal: fastest feedback loop that still covers weekly seasonality and time to purchase; growth speed is a function of feedback cycle speed.

### 3.6 Structure at $50k to $250k a month
[7350eaba553e] [65e0503d7bc4]
1. Keep the retargeting campaign, likely still existing customers only; adding website visitors is rarely needed.
2. Cold: more ad sets (more concept tests, more creative), and possibly 2 or 3 cold campaigns, each with a specific commercial reason.
3. Single-SKU CPG: split campaigns by funnel or persona. Example: fish oil for people 65 plus with arthritis (VSSLs, native statics, testimonials from older people, TV-style ads cut into UGC format) versus the same product for 25 to 35 year olds for brain health or work performance. Different landing pages and photos, different creators and profiles (one may lean on whitelisting, the other on the native page). They are "almost 2 different businesses", so 2 campaigns.
4. Multi-SKU fashion: split by commercial lever, for example a new-arrivals campaign to raise sell-through, or a category campaign (pants) where LTV analysis shows higher first-order AOV and better repeat rates, run at a higher CPA KPI. [needs brand data: LTV and repeat rate by first-purchase category]
5. Do not add campaigns because spend "feels big" (for example, "we spend $100k, one campaign seems weird"). That breaks data integrity and decision loops.
6. Launch about 100 to 300 new ads a month if you want to grow (fewer if not). Example fit: 2 campaigns x 10 ad sets = 20 ad sets, so 5 to 15 ads per ad set. Fewer campaigns and ad sets also work.
7. The skill at this tier is continuous concept testing to find the 20% of concepts that can hold hundreds of thousands a month.

### 3.7 Build and scale a concept matrix
[65e0503d7bc4] [ac6d263bd22b]
1. List personas, angles, offers and ad types; build the matrix; make each ad set one concept.
2. Example concept 1: persona coffee drinkers, angle whitening without sensitivity, offer just the product, ad type UGC (rotate many ad types under this ad set).
3. Example concept 2: persona brides, angle get ready for your wedding in 14 days, offer a bundle curated for a 14-day turnaround, ad type testimonial from a real bride with before and after and the process documented.
4. Example concept 3: persona smokers, angle remove stains, offer a subscription (the problem keeps coming back), ad type founder talking to camera (the founder is a smoker).
5. When a concept wins: make much more creative for it, build a custom landing page with continuity (name the bundle, for example "wedding in 14 days bundle"), add testimonials, build the whole funnel around the angle. The source says this can scale to 2x to 3x volume while you keep working other angles and personas.
6. Read results at concept level; feed them into the next creative batch.
7. Push insights upstream: offer changes, new product categories for that audience, and retention flows (example: a post-wedding win-back that sends a free gift, "congrats on getting married", and an offer that pulls the customer into another product line suited to their stage of life).
Depth on concept building is in the agency's separate 30-minute video, not in this source.

### 3.8 Add new creative to a concept (fork rule)
[a95742238877] [b722b2c086bc]
1. Check the concept's ad set against KPI (target CPA or ROAS).
2. Not hitting KPI: add the new creatives to that ad set to try to revive it.
3. Hitting KPI: do not touch it. Launch the new creatives as a new ad set for the same concept.
4. Name the new ad set per 3.12.

### 3.9 Find spend equilibrium, then decide on a scaling campaign
[0e642b4c3a8c] [a95742238877]
1. Take an ad set well above target (example: above a 5x target return) with strong soft metrics.
2. Raise daily spend over time (about 20% a day at the small tier). [b8a2663f518f]
3. When ROAS drops to unprofitable, pull spend back. Repeat until you find the daily level where results hold and any push drops them (example: $300 a day). Record it as that creative's capacity.
4. Only then consider moving those creatives (same post IDs) into a scaling campaign. Keep the original running; do not turn it off.
5. Expected gain on a good day: about 20% more daily spend on that asset (example: $300 a day becomes $400 a day across the account). This is a hope, not a promise; often it cannot.
6. Skip it at low spend: at $60 a day it adds about $10 a day. Fix the ad, landing page, offer or concept instead.
7. Worth it at about $400 a day (adds about $80 a day), and across 10 top ads at once it might add about $1,000 a day.
8. Never test inside the scaling campaign; exclude existing customers from it. [b8a2663f518f]

### 3.10 Choose ABO or CBO
[2f66cf4f65c6] [1589854e06d9]
1. High AOV and low conversion volume (example: $10,000 AOV, about 5 orders a day): use ABO; avoid CBO.
2. Otherwise choose by risk appetite and trust in the algorithm: CBO for efficiency with concentrated risk; ABO to force spend through every test.
3. Inexperienced buyer: prefer consolidated CBO. Experienced buyer: ABO or in-between.
4. At large spend, the source's preferred structure is CBO with minimum and maximum ad set spend limits: about 60% of budget tightly directed, about 40% free to flow. Most of the agency's accounts run this. It needs heavy oversight; at about $10k a month it is overkill, so just pick ABO or CBO. [verify UI: ad set spend limits under campaign budget]
5. Seasonal rotation used for some accounts: CBO in Q4 peak (Black Friday, November, December) to maximize spend and efficiency in a short window; back to ABO in Q1 (January, February) for clean creative testing, because Q4 conversion rates are inflated and make ads look better than they are.

### 3.11 Build an ad set
[d6c0209e9d6b]
1. 1 concept per ad set; all ads speak to the same audience (same persona, same product).
2. Minimum 3 ads; rule of thumb 3 to 15. Maximum is effectively unlimited up to the ad set ad limit (the agency runs some with 200 creatives), but most brands lack the volume, and 200 ads usually span several concepts that should be split. [web check: current ads-per-ad-set limit]
3. Put top, middle and bottom of funnel ads for that persona in the same ad set (option 2). Splitting by awareness stage (option 1) also works, but only if you blend the numbers when deciding.

### 3.12 Name ad sets
[c910cbdcfaae]
1. Format: persona, angle, offer, content type (if the ad set groups one content type), launch date.
2. Do not use batch names like "March 7 creatives"; they hide the concept and suggest concepts were batched together.
3. When taking over a messy account, rename old ad sets retrospectively so past concept performance can be read.
4. Use the same convention across campaigns so you can filter and KPI concepts account-wide.

### 3.13 Size retargeting and existing-customer budgets
[3a48f7471999] [9d8a9963309a] [4b24c60d9321]
1. Monthly budget = number of people in the audience x CPM x desired frequency per month. Because CPM is the cost per 1,000 impressions, divide CPM by 1,000 in the arithmetic (the source states the formula without the division). Card 3a48f7471999 gives its own example, not from the source: 50,000 customers x ($10 ÷ 1,000) x 2 = $1,000 a month. [needs brand data: customer count, retargeting CPM]
2. Frequency ceiling: keep existing-customer frequency below 7 on a 30-day rolling window. [needs brand data: current 30-day frequency on existing customers]
3. At small scale this can be tiny (the CPG example spends about $20 a day).
4. Re-derive when customer count or CPM changes. Review profit and frequency every period.
5. Ask whether more spend is profitable; if adding $10 or $1,000 a day does not pay back with profit, do not add it.

### 3.14 Validate a structure (4 questions)
[3da640845924] [092e8775c5e9]
1. Does the structure produce data I can read to make decisions?
2. Does it match how the business actually makes money (commercial alignment)?
3. Is it right for the spend tier and creative throughput?
4. Are the support layers (DPA, retargeting, website visitors, existing customers) sized to the real retention of the business?
If any answer is no, the structure is wrong; restructure.

### 3.15 Settings to turn off or check
The intro promises "3 settings"; the section itself lists 5 items. Card f623a968dbf2 says the settings are not named; they are named, below. [f623a968dbf2]
1. **Flexible ads: off.** You cannot tell which asset drove results, which breaks data integrity. Also: no control of cropping (1:1 and story assets get cropped into other placements), and Meta may string flexible ads into a carousel the client never approved. Only fallback use: forced by page limits after trying page tactics (3.16); then load only very similar creative so a win still says "this type works". Never mix very different asset types. [e323039d800f] [verify UI: current name of flexible ads]
2. **Cost caps and bid caps: ignore under about $200k a month.** Ask "would the business double if we focused only on bidding?" Usually no. Experienced buyers can still run cost caps at any spend. [bfec753c654b]
3. **1-day view attribution: off,** or at least not used when flowing budget between ad sets or judging what works. It over-attributes, especially existing-customer revenue. [04f6f0b93295] [verify UI]
4. **Advantage+ creative optimizations: off at 2 levels.** On every ad you launch, and in advertiser settings under the creative sub-dropdown, where automated rules otherwise switch creative optimizations back on over time. [04cf2865b996] [verify UI: advertiser settings path]
5. **Audience segments: set up and synced.** Define existing customers (commonly synced from Klaviyo to Meta). The sync breaks periodically; then existing customers get served as new, eroding data integrity and wasting spend. Check it on a schedule. [d74e033578c8] [fb9db4eb1b28] [verify UI]

### 3.16 Page strategy for ad caps
[8494f59ad41f] [63e75994772f]
1. Know the cap: Meta caps live ads per page at about 300 to 500 (the transcript also says "you can't have more than 500 active ads in the account"). High-volume brands hit it fast; at $250k plus it is a guarantee. [web check: current active-ad limit per page and per ad account]
2. Without a plan you must turn ads off. Instead use all 3 options the source recommends (it would run them together):
   1. Duplicate brand pages. Example: Gruns runs about 15 pages that differ only in logo color. The presenter is not concerned about consolidating on 1 page; some are.
   2. Partnership ads (a real creator's page; often paid if they have leverage) and "whitelisting" in the source's sense: a brand-created third-party page (example: "Fiber Health Magazine") running the same ads, ideally reworked to be more advertorial. Third-party framing feels less like selling.
   3. Regional pages (Brand UK, Brand Australia, Brand USA). Country campaigns with 100 ads each hit the cap even when the ads are identical; per-country pages give each its own cap.
3. Plan pages before you hit the cap, and account for them in creative planning (some funnels lean on whitelisting, others on the native page). [63e75994772f]

### 3.17 Structure at $250k plus a month
Range is $250k to $20M a month, so the source gives tactics, not a template. [58966745d295] [b8c4642d637c]
1. Consider a second ad account: same pixel, different bid logic (for example maximize conversions in the main account; maximize conversion value, cost caps or bid caps in the second), same or different page. It can win auctions the main account does not enter. Risk: it may raise your own CPMs through cross-bidding; with the same page and pixel the source thinks this is minor, and says nobody has proven it either way. Main benefit: if the main account is banned or billing fails, crank up the second (it might hold only 10% of spend normally) and avoid a week with no new-customer revenue. The source says this advice changes about every 6 months. [web check: current Meta stance on multiple ad accounts with one pixel]
2. Page strategy is mandatory (3.16).
3. Diversify bidding across campaigns (bid caps, cost caps, maximize conversion value, target ROAS next to maximize conversions); each enters auctions differently and you generally win more. A dedicated buyer is worth it here.
4. International: do not split ad accounts by country, except to be billed in local currency (for example USD for a US bank, GBP for a UK entity). Solve reporting with filters on country or campaign name. Plan pages and store backend (for example Shopify) per region. The source admits its preference partly reflects agency labor (some clients run 7 accounts for 7 regions).
5. Keep testing campaigns even at huge spend (the source has seen testing at $300k a day).

## 4. Rules, thresholds and numbers

| Rule | Number or threshold | Condition | Source's basis | Card |
|---|---|---|---|---|
| CPM inflation | about 20% to 30% a year | agency data, cyclical with Black Friday | aggregated report on 150M+ spend | 5b99bf6d671d |
| Signal lost at iOS 14 | about 30% | historical | presenter's recollection of Meta statement | 9b521e4ff188 |
| Interest group misassignment | about 30% of people | historical claim | "a report" | 4c81bdf1685a |
| Old ad set learning sample | about 1,000 random people | pre-iOS 14 Meta | presenter's account | 9b521e4ff188 |
| Account improves past | about 100 to 200 conversions a month | per consolidated signal | presenter's observation | 7230fc5fab8f |
| Ad set segmentation effect | about 5% to 10% efficiency swing | ad set level only | presenter's estimate | 7230fc5fab8f |
| Brands that can fully consolidate | about 10% (90% should not) | 1 campaign, 1 ad set | opinion | 7230fc5fab8f |
| Media buying lift | 10% to 20% | $100k to $300k a month | estimate | 9997eb5233ac |
| Media buying worth | 3% to 4% | about $1M a month | estimate | 58966745d295 |
| Daily bid tweaks | about 5% gain, 1 hour a day | any tier | estimate; not worth it | 9997eb5233ac |
| Pareto split under CBO | 20% of ads get 80% of spend | consolidated CBO | opinion | 1589854e06d9 |
| Creatives per ad set | 3 to 5 | under $50k a month | template | ba414cee7839 |
| Ads per ad set | minimum 3, rule of thumb 3 to 15, up to 200 | any | sequencing; agency accounts | d6c0209e9d6b |
| Exposures before purchase | 2 to 6 | general | opinion | d6c0209e9d6b |
| Test kill threshold | 3x target CPA; 3-4 conv keep, 2 run about $50 more, 0-1 cut | concept ad set | rule of thumb | 87a85788a663 |
| Preferred kill threshold | 5x target CPA, yes or no only | if client allows | preference | 87a85788a663 |
| Daily test budget | (target conv x expected CPA) ÷ days | any test | formula | 1c683e007b76 |
| Worked test budget | 20 x $100 ÷ 14 = about $143 a day | example | source example | 1c683e007b76 |
| Meta learning rule (rejected for tests) | 50 conv per 7 days = about $714 a day at $100 CPA | 1 ad set | source critique | 1c683e007b76 |
| Test duration | 1 week default; 3-4 days large stable; 10-14 days tiny, slow, seasonal | per business | framework | f88304f4647b |
| Minimum read window | 5 days | under $50k a month | presenter | b8a2663f518f |
| Short read window allowed | 2 days at 1,000 conv a day; not 3 days at 3 conv | volume-based | presenter | f88304f4647b |
| Budget increase on winners | about 20% a day | under $50k a month tier | presenter | b8a2663f518f |
| Scaling campaign trigger example | above 5x target return plus good soft metrics | winner at equilibrium | example | 0e642b4c3a8c |
| Scaling campaign gain | about +20% daily spend on a good day | per asset | presenter | a95742238877 |
| Not worth scaling campaign | $60 a day base (+ about $10) | low spend | presenter | 0e642b4c3a8c |
| Worth it | $400 a day base (+ about $80); 10 ads + about $1,000 a day | higher spend | presenter | a95742238877 |
| Scaling campaign refresh | top post IDs moved every 1 to 2 weeks | $750k a month example | client account | a95742238877 |
| Existing-customer frequency ceiling | below 7 per 30 days rolling | retargeting existing customers | presenter | 9d8a9963309a, b8a2663f518f |
| Over-frequency signal | 30 a month probably too high; 50 per 30 days clearly too high; 1 likely too low | existing customers | illustrations | 028483f1e7af, 3a48f7471999 |
| Existing-customer budget | customers x CPM (÷1,000) x frequency per month | monthly dollars | formula | 3a48f7471999, 9d8a9963309a |
| Small CPG retargeting spend | about $20 a day | $5M a year CPG | example | 4b24c60d9321 |
| Website-visitor campaign not needed | about 90% of accounts | cold campaigns already reach engaged | presenter | ccf942b9f2c8 |
| Retargeting share in audits | about 50% of spend to existing plus engaged | audit finding, a mistake | audits | 028483f1e7af |
| DPA death spiral pattern | about 80% of spend on DPAs, decline over 6 months | 6 fashion brands in 2 weeks | audits | 805594665ccc |
| Furniture DPA | 57% of budget; 7x shown, 1.9x on 7-day click or incremental | 1 audit, $20M-$30M brand | audit | 1589854e06d9 |
| NZ paired with AU | caps itself at about 7% to 10% of total spend | AU+NZ campaign | presenter | 49146dda7d03 |
| Page ad cap | about 300 to 500 live ads | per page | presenter [web check] | 8494f59ad41f |
| Cost or bid caps not a priority | under about $200k a month | any | opinion | bfec753c654b |
| Bidding strategy mix matters | over $250k a month (99.9% of advertisers are below) | high spend | presenter | 58966745d295 |
| CBO controlled share | about 60% directed by min/max limits, about 40% free | large accounts | agency default | 2f66cf4f65c6 |
| New ads per month for growth | 100 to 300 | $50k to $250k a month | presenter | 65e0503d7bc4 |
| Advertorial pulled out | at about 30% of total spend | $750k a month example | client account | 74eaa65de2ef |
| Promo cadence in example | every 3 to 4 weeks | $750k a month example | client account | 74eaa65de2ef |
| Free audit threshold | $5M a year online revenue | sales pitch | n/a | none |

## 5. Diagnostics and checks

### 5.1 Is conversion data too split?
- Check: conversions per month per campaign. [needs brand data: monthly conversions by campaign]
- Bad: a small account with 4 campaigns sharing about 100 conversions a month (about 25 each).
- Good: few campaigns, and each has a stated commercial reason.
- Fix: consolidate campaigns; move category or persona splits down to ad sets. [7230fc5fab8f]

### 5.2 Are men's and women's (or other non-overlapping) ads mixed?
- Check: open the ad set, use the gender breakdown on each ad. [verify UI]
- Bad: women's ads serving heavily to men.
- Fix: separate ad sets or campaigns by persona or range. [ebff07a9e6f2]

### 5.3 How is spend split across new, engaged and existing audiences?
- Setup: audience segments must be defined in advertiser settings. [verify UI]
- Check: Breakdown, then audience segments (the source also says the total row at the bottom of the account shows total distribution). Read spend, ROAS and frequency for new, engaged and existing. [verify UI]
- Good: existing near 0% in cold campaigns (they are excluded); engaged already gets meaningful spend at a high enough frequency, so no website-visitor campaign is needed.
- Bad: about 50% of spend on existing plus engaged; any meaningful existing spend in cold campaigns (exclusion or sync is broken).
- Fix: tighten exclusions, check the Klaviyo to Meta sync, cap retargeting. [ccf942b9f2c8] [fb9db4eb1b28] [d74e033578c8] [028483f1e7af]

### 5.4 Is a DPA or retargeting ad set over-credited?
- Check: compare its ROAS on the default view with 7-day click and with incremental attribution. [verify UI]
- Bad: example furniture DPA at 7x shown and 1.9x on 7-day click or incremental, while holding 57% of cold CBO budget; other ad sets did better on honest attribution.
- Fix: pull DPAs out of cold CBO, cap them, judge on incremental. [1589854e06d9] [cf36e5f30572]

### 5.5 DPA death spiral check
- Check: DPA share of spend over the past several months, alongside prospecting spend and creative output. [needs brand data: monthly spend by campaign type, new ads per month]
- Bad: DPA share climbing toward about 80%, creative production cut, account in decline.
- Fix: rebuild top-of-funnel spend and creative throughput; when DPA softens, look upstream first. Audit the whole account at once, not one campaign. [805594665ccc] [092e8775c5e9]

### 5.6 Existing-customer frequency
- Check: 30-day frequency on existing customers.
- Good: below 7. Bad: 30 or 50 a month. Too low: about 1 (likely under-spending).
- Fix: re-derive the dollar budget (3.13). [3a48f7471999] [9d8a9963309a]

### 5.7 Retargeting hyper-segmentation
- Check: separate retargeting ad sets by landing page, product category, add to cart, initiate checkout, website visitors.
- Bad: several warmth tiers split out ("very 2019"); the source says the CPM increase is never outweighed by the conversion-rate gain.
- Fix: consolidate retargeting audiences. [028483f1e7af]

### 5.8 Does a number look too good?
- Check the attribution window (1-day view on?) and the audience segment breakdown before drawing a creative conclusion. [fb9db4eb1b28] [04f6f0b93295]

### 5.9 Are creative settings reverting?
- Check recently launched ads for Advantage+ creative optimizations switched back on; check advertiser settings rules. [04cf2865b996] [verify UI]

### 5.10 Is the ad set naming readable?
- Bad: "March 7 creatives". Good: persona, angle, offer, content type, date. [c910cbdcfaae]

### 5.11 CBO allocating on soft metrics?
- Check: in a high AOV, low volume account, is CBO spend following CTR or CPC rather than purchases? [needs brand data: purchases per day, AOV]
- Fix: move to ABO. [1589854e06d9]

### 5.12 Scaling campaign sanity
- Bad: winners moved to scaling at about $60 a day; tests run inside the scaling campaign; no exclusions in it.
- Fix: keep scaling for winners at equilibrium with meaningful spend (about $400 a day and up). [0e642b4c3a8c] [b8a2663f518f]

### 5.13 Structure validation
Run the 4 questions (3.14). Any "no" means restructure. [3da640845924]

## 6. Tools, settings and named features

- **Ads Manager breakdowns** (age, gender, placement, region, audience segments): used for gender mismatch and audience spend checks; do not restructure on breakdown ROAS. [verify UI] [528465d5cc14]
- **Audience segments** (advertiser settings; new, engaged, existing): required for the audience segment breakdown and existing-customer control. [verify UI] [ccf942b9f2c8]
- **Klaviyo to Meta audience sync**: feeds existing-customer segments; breaks periodically. [verify UI] [d74e033578c8]
- **Attribution settings**: 7-day click for reading and budgeting; 1-day view off; "incremental attribution" named as an option for DPA and retargeting reads. [verify UI] [web check: current Meta incremental attribution setting] [fb9db4eb1b28] [cf36e5f30572]
- **Advantage+ campaigns** ("Advantage+ cold campaign" used in the CPG example) and their old "existing customer spend cap" percentage field, which the source says framed spend wrongly. [verify UI] [4b24c60d9321] [3a48f7471999]
- **Advantage+ creative optimizations**: turn off per ad and in advertiser settings, creative sub-dropdown, automated rules. [verify UI] [04cf2865b996]
- **Flexible ads**: avoid. [verify UI] [e323039d800f]
- **ABO and CBO** (CBO also called Advantage campaign budget in a card), with ad set minimum and maximum spend limits. [verify UI] [2f66cf4f65c6]
- **Bid strategies**: maximize conversions, maximize conversion value, target ROAS, cost caps, bid caps. Set at ad set level, not ad level. [9ede69b02ec7] [58966745d295]
- **Dynamic product ads (DPA)**: catalog ads that reprioritize products a user viewed, if the pixel fires correct product data. [cf36e5f30572]
- **Partnership ads** and **whitelisting** (source's meaning: a brand-made third-party page). [8494f59ad41f]
- **Post IDs**: the source moves the same post IDs of top performers into the scaling campaign. [a95742238877]
- **Pixel**: shared across a second ad account. [58966745d295]
- **Shopify**: backend handling of regions named, no steps given. [b8c4642d637c]
- **Meta "breakdown effect" help page**: cited as public documentation. [web check] [528465d5cc14]

## 7. Examples and case results

All are examples, not promises.

- **Brand A, CPG** [4b24c60d9321]: 1 consumable product, $5M a year, 70% gross margin, 1 persona (busy moms), sells in AU and US (source thinks AU only is right at this size). Structure: 1 Advantage+ cold campaign per country; concept ad sets with most spend on the 1 working concept; existing customers excluded from both (in CPG, returning revenue would over-attribute to cold and push frequency up); 1 existing-customer retargeting campaign at about $20 a day, frequency below 7 per 30 days.
- **Brand B, fashion** [49146dda7d03]: 50 SKUs, $5M a year, lower gross margin (sign of constant discounting), 4 personas (3 to 4 is typical in fashion), sells AU, NZ, UK, 3 categories (pants, tops, dresses) with separate purchase orders and revenue goals. AU and NZ in 1 campaign. UK options: (1) 1 AU campaign and 1 UK campaign with category ad sets on ABO for budget control, or (2) consolidate regions into category campaigns if UK orders ship from AU stock. Complication: hemispheres have opposite seasons, so UK-season purchase orders mean UK stock must move. Source picks option 1, also because UK sits on a different subdomain and needs different URLs. Plus a DPA retargeting campaign to engaged audiences (90-day website visitors) and an existing-customer campaign with 2 ad sets, new arrivals and DPA (together, DPA would take all spend). Fashion existing-customer targeting is described as more incremental than any other category the agency has seen.
- **Furniture brand, $20M to $30M** [1589854e06d9]: 1 consolidated cold CBO; 57% of Meta budget in the top ad set, a DPA, at 7x shown ROAS but 1.9x on both 7-day click and incremental; everything else did better on those views.
- **High AOV brand** [ebff07a9e6f2]: $10,000 AOV, about $50k a day, about 5 orders a day; CBO would optimize on soft metrics.
- **6 fashion brands in 2 weeks of audits** [805594665ccc]: about 80% of spend on DPAs, accounts declining for 6 months; agency kept raising DPA budgets and told the brand it did not need as much creative.
- **$750k a month account ($25k a day)** [74eaa65de2ef] [a95742238877] [cf36e5f30572]: (1) testing campaign on ABO, tests at ad set level, some test ad sets spend several thousand a day and scaling also happens there; (2) scaling campaign, CBO, 1 ad set, cost caps, top post IDs added every 1 to 2 weeks without turning them off in testing; (3) promo campaign, because promos run every 3 to 4 weeks, turn over fast and would disrupt testing and scaling learning, and they reach more price-sensitive buyers; (4) advertorial campaign, pulled out once advertorials took about 30% of total spend so it can be KPI'd as its own funnel; (5) DPA campaign for existing customers and a few website visitors, on incremental attribution, low spend in line with frequency.
- **Awareness-stage split** [d6c0209e9d6b]: consolidated persona ad set at 4x; the same ads split into a top-of-funnel ad set at 2x and a bottom-of-funnel ad set at 6x. The right call is to blend and treat the concept as 4x, but buyers and clients cut the 2x.
- **Sequencing** [9ede69b02ec7]: 3 ads in 1 ad set each at $5,000 spend with very different returns.
- **Stories versus Feed** [528465d5cc14]: 4x versus 3x, Feed holds 80% of spend.
- **Gruns** [8494f59ad41f]: about 15 duplicate pages with different logo colors.
- **Teeth whitening concepts** and **fish oil funnels**: see 3.7 and 3.6.

## 8. Mistakes the source warns about

1. Hyper-segmented legacy structures, common with cheap agencies serving $10k to $20k a month brands. [9b521e4ff188]
2. Consolidating everything into 1 campaign and 1 ad set regardless of margins, personas or AOV. [7230fc5fab8f]
3. Putting DPAs in the same cold CBO as everything else. [1589854e06d9]
4. Killing or scaling on ad-level ROAS; ignoring sequencing. [9ede69b02ec7]
5. Launching placement or demographic campaigns from breakdown ROAS. [528465d5cc14]
6. Interest and lookalike testing. [4c81bdf1685a]
7. Daily bid tweaks and daily budget pacing on small accounts. [9997eb5233ac]
8. Testing inside the scaling campaign. [b8a2663f518f]
9. No exclusions on the scaling campaign. [b8a2663f518f]
10. Killing tests too fast (read window too short). [b8a2663f518f]
11. Setting ad set budgets from the 50 conversions per 7 days rule. [b8a2663f518f] [1c683e007b76]
12. Adding new creative to an ad set that is working. [a95742238877]
13. Rolling a $60 a day winner into a scaling campaign. [0e642b4c3a8c]
14. Adding campaigns because spend feels big, not for a commercial reason. [7350eaba553e]
15. Splitting funnel stages and then reacting to the split ROAS instead of blending. [d6c0209e9d6b]
16. Batch ad set names like "March 7 creatives". [c910cbdcfaae]
17. Letting retargeting reach about 50% of spend; treating it as growth. [028483f1e7af]
18. Splitting retargeting by add to cart, checkout, page or category. [028483f1e7af]
19. Cutting creative and prospecting because DPAs look strong (DPA death spiral). [805594665ccc]
20. Setting existing-customer spend as a percentage. [3a48f7471999]
21. Flexible ads with mixed asset types. [e323039d800f]
22. Leaving 1-day view on for budget decisions. [04f6f0b93295]
23. Turning off Advantage+ creative per ad but not in advertiser settings. [04cf2865b996]
24. Not checking the audience segment sync. [d74e033578c8]
25. Splitting ad accounts by country without a billing-currency reason. [b8c4642d637c]
26. Running promos inside testing or scaling campaigns. [74eaa65de2ef]
27. Hitting the page ad cap with no page plan. [63e75994772f]

## 9. Caveats, conflicts and what is missing

- **Single agency, sales video.** Numbers are the agency's estimates, audits and 1 client account. Ends with a free audit pitch for $5M plus brands and a hiring call.
- **Transcript noise.** "ABO" often transcribes as "an" or "an so"; "ROAS" as "rorowaz"; "Andromeda" as "Andromedor"; ABO and CBO figures at very large spend are garbled; the CPC versus ROI sentence contradicts itself. Read those passages with care.
- **"3 settings" versus 5.** The intro promises 3 settings to turn off; the section lists 5 (flexible ads, cost or bid caps, 1-day view, Advantage+ creative optimizations, audience segment setup). Card f623a968dbf2 wrongly says they are not named.
- **Card additions not in the source.** Card 57a5a1e787d4 adds a 20 x $30 example; card 3a48f7471999 adds a 50,000 x $10 x 2 example. The library topic header says CBO gives spend to "the top 4% of ads"; the source says 80/20. Card 1589854e06d9 says "default to CBO when conversion volume is healthy"; the source calls the choice personal preference. Card ac6d263bd22b's "broad targeting yields no persona data" refers in the source to broad concepts, not broad audience targeting (which the source recommends).
- **CPM in the formula.** The source's "customers x CPM x frequency" needs CPM ÷ 1,000 to give dollars.
- **Two test-sizing methods.** The 3x or 5x CPA kill rule judges on about 3 to 5 conversions; the formula method uses a chosen threshold like 20. The source gives both without reconciling them.
- **Country segmentation tension.** The page section says "generally you should segment your campaigns based on country", while Brand B's option 2 and the consolidation principle allow merging regions when stock and targets allow. Rule the source implies: segment by country when inventory, targets or URLs differ.
- **Media buying lift tension.** 10% to 20% at $100k to $300k a month versus 3% to 4% being "quite mature" at $1M.
- **"Whitelisting" term.** The source uses it for a brand-created third-party page; common industry use means running ads through a creator's handle (what the source calls partnership ads). Keep the meanings apart.
- **Conflicts with common advice.** Meta's own 50 conversions per 7 days learning guidance is rejected for test budgets. Meta's default 7-day click plus 1-day view is rejected for decisions. Funnel-stage and add-to-cart or checkout retargeting splits, common in older playbooks, are rejected. Percentage caps on existing-customer spend (a Meta feature) are rejected. Lookalikes are called dead, which many practitioners still dispute [web check: current Meta guidance on lookalikes and interests as signals].
- **Missing how.** No steps for running incremental attribution or the "attribution breakdown"; no LTV analysis method; no definition of "soft metrics" thresholds; no steps for second-account setup, min and max spend limits, or Klaviyo sync checks; no guidance on where the "reasonable rolling window" ends above 5 days; exact page and ad limits not confirmed; no data behind the 100 to 200 conversions or 5% to 10% claims.
- **Date risk.** Andromeda, flexible ads, Advantage+ settings, page caps and second-account tactics are named as fast-changing by the source itself. Re-verify at use. [web check: all Meta UI names and limits above]

## 10. Card index

- `5b99bf6d671d` Meta CPM inflation and the efficiency trade-off
- `9ede69b02ec7` Last-click reality vs. Meta's multi-touch optimization
- `528465d5cc14` Trust the algorithm's breakdown spend distribution
- `4c81bdf1685a` Creative-as-targeting and why broad targeting works
- `7230fc5fab8f` Consolidation beats segmentation: the campaign-level data silo
- `b8107473f4c3` Five diagnostic questions for account structure
- `ba414cee7839` Generic sub-$50k/month Meta structure
- `9d8a9963309a` Budgeting the retargeting support layer
- `57a5a1e787d4` Calculating daily testing budgets by back-propagation
- `1589854e06d9` Choosing ABO vs CBO by conversion volume and signal
- `ebff07a9e6f2` Segment accounts by unit economics and audience
- `4b24c60d9321` Worked example: CPG brand structure with one persona and two markets
- `49146dda7d03` Worked example: fashion brand with SKUs, personas and regions
- `8494f59ad41f` Page caps, whitelisting and regional pages
- `9997eb5233ac` What media buying still controls (and what's dead)
- `b722b2c086bc` Concept definition and adset grouping rule
- `9b521e4ff188` Why 2018-style interest segmentation stopped working
- `f623a968dbf2` Three settings-style cleanups to audit before restructuring
- `a95742238877` Never Touch a Performing Ad Set, Fork It Instead
- `fb9db4eb1b28` Exclude Existing Customers and Set 7-Day Click Attribution
- `87a85788a663` Set Test Budgets by Back-Propagating from CPA
- `f88304f4647b` Run Tests One Week to Capture Seasonality and Time-to-Purchase
- `b8a2663f518f` KPI at Ad Set Level and Scale Budgets in 20% Daily Steps
- `568f98fcc9aa` Keep Account Structure Consolidated at Low Spend
- `7350eaba553e` Layer Campaigns at $50k to $250k with a Commercial Reason
- `65e0503d7bc4` Build Creative Concepts as Persona x Angle x Offer x Ad Type
- `ac6d263bd22b` Use Concept Testing to Shape Retention and Product Strategy
- `74eaa65de2ef` Run a Dedicated Promo Campaign to Protect Learning
- `ccf942b9f2c8` Consolidate Website-Visitor Retargeting into Cold Campaigns
- `028483f1e7af` Treat Retargeting as a Capped Support Layer
- `cf36e5f30572` Read DPA ROAS with 7-Day Click or Incremental Attribution
- `2f66cf4f65c6` Choose ABO vs CBO by Risk Versus Efficiency Profile
- `d6c0209e9d6b` Keep Three to Fifteen Ads per Ad Set, Aligned to One Audience
- `c910cbdcfaae` Name Ad Sets by Persona, Angle, Offer and Date
- `58966745d295` Add a Second Ad Account with Different Bid Logic to Derisk and Expand Auction Entry
- `b8c4642d637c` Avoid Splitting Ad Accounts by Country
- `63e75994772f` Add a Page Strategy Before You Hit Ad Limits
- `0e642b4c3a8c` Find the Spend Equilibrium Where Efficiency Breaks
- `3a48f7471999` Budget existing-customer retargeting by dollar and frequency, not percent
- `805594665ccc` Avoiding the DPA death spiral: protect top-of-funnel investment
- `e323039d800f` Turn off Meta flexible ads to preserve creative read-outs
- `bfec753c654b` Deprioritize cost caps and bid caps below ~$200k/month
- `04f6f0b93295` Disable 1-day view attribution for budget and scaling decisions
- `04cf2865b996` Turn off Advantage+ creative optimizations at account and ad level
- `d74e033578c8` Audit audience segment syncs to prevent existing customers being served as new
- `1c683e007b76` Size test budgets from target conversions, CPA, and duration
- `3da640845924` Four-question checklist to validate any ad account structure
- `092e8775c5e9` Review the whole ad account at once when auditing spend allocation
