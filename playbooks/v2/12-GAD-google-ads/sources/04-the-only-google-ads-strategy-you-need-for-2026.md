# The Only Google Ads Strategy You Need for 2026

source_id: 1cVFwWMuAQVnzljzddBcWvIjk-85_LU2W  |  folder: /12-GAD-google-ads  |  cards: 32  |  words: 16957  |  type: transcript (YouTube video, one presenter, whiteboard style)
credibility: Presenter runs the agency Blue Sense Digital (hiring email on a .com.au domain; he cites Australian accounts, so likely Australian). Same presenter as the Meta videos in 24-DEP. He sells free account audits to brands "doing over $5 million a month" (as transcribed; the Meta video says $10M a year, so the unit may be a transcription error) and recruits performance marketers. He says the agency works only with ecommerce and retail brands. Stated evidence: PMax run on "over 250 accounts", consulting on "another 400 ecom accounts from 7 8 9 10 figures", PMax scaled to $100k to $300k a month on large accounts, internal ramp tests (PMax vs standard shopping), private talks with owners of "some of the biggest Google ads agencies in the world", and one named client case (PMax drifting into YouTube and Gmail). No client names, no charts with numbers, no published data. Many numbers are illustrations he labels as such (70% vs 35% margin, $40 t-shirt vs $200 jumper, 30% testing budget). He says his old view "PMax campaigns are terrible" was biased, and flags his audience signal claim as "a little bit controversial".
date signals: Title says 2026. Says most agency playbooks are "2022 2023 strategies" and the platform shifted over the "last two to three years". Names AI Max and Demand Gen as newly introduced, DSAs as "being deprecated", PMax negative keywords as "recently" rolled out, and brand exclusion lists as "the only way" to exclude brand "for the last like year". Says PMax replaced Smart Shopping "3 years" ago (transcript says "20122"; likely 2022). Says SKAGs "stopped working in like 2020" and he ran them in 2019. Says smart bidding is unavailable to new accounts "at least the last time I checked". Document modified 21 Sep 2026. Transcript is cut off mid-sentence in the closing pitch; nothing of substance seems missing.
scope note: The document header marks it core for Google Ads account structure, PMax mechanics, standard shopping, search ad groups (STAGs vs SKAGs), bidding (expansive vs restrictive), GMC feed optimization and the target ROAS death spiral. It says to skip the audit pitch, the hiring call and the "new product every 3 to 4 months" claim. Paid social creative belongs in 10-MCR. GA reporting and MMM belong in 06-MEA. Landing page testing detail belongs in 07-LPG and 09-CRO; it is kept here only as the search lever the source names.

## 1. What this source is for

It gives an operator a full 2026 rebuild plan for an ecommerce Google Ads account: how many campaigns to run and why, how to set up PMax so it is not a retargeting campaign, when to add standard shopping, how to pick and move bidding strategies, how to fix the Merchant Center feed, and a 90-day order of work. Its core claim is that PMax over-credits itself on warm traffic, so cold growth needs standard shopping and a low target ROAS "feeder" campaign. It is strong on mechanics and audit checks. It is thin on exact settings paths, test sizes and how to measure backend incrementality.

## 2. Principles

### 2.1 Commercial frame

1. **Most accounts either overspend or underspend on Google.** Overspend: Google sits at the bottom of the funnel, captures demand made by Meta, TikTok and affiliates, reports a high ROAS, and gets more budget even though it is not incremental. Underspend: teams that believe Google is "only bottom funnel" cap it (example: under $10,000 a month while spending "a4 million a month" on Meta, as transcribed) even in categories with lots of cold search demand. The test is whether backend revenue moves when Google spend moves, not the in-platform ROAS. The $10k figure is an illustration. [fb0673e2ae6d] `[needs brand data: backend revenue vs Google spend over time; category search volume]`

2. **Five platform shifts date older playbooks.** (1) PMax hit its ceiling: early PMax results were very strong (he suspects Google gave auction discounts to push adoption), the arbitrage faded as everyone moved spend in, and visibility into where spend goes is poor. (2) Standard shopping is back, because PMax shows diminishing returns at scale and cold growth needs standard shopping layered in. (3) Match types changed: exact match now matches "the same meaning", phrase match got a little broader, broad match is as broad as ever. (4) Google introduced AI Max and Demand Gen. (5) DSAs are being deprecated. No card covers shifts 3 to 5; the source gives no detail on AI Max or Demand Gen. [8ac98b834d71] `[web check: current exact and phrase match definitions; AI Max for Search status; Demand Gen; DSA deprecation date]`

### 2.2 Account structure

3. **Consolidation beats segmentation.** Campaigns learn mostly in isolation (he admits some platform-level data sharing but ignores it to simplify). Example: 3 shopping campaigns with the same products at 50, 20 and 10 conversions per 30 days. The 10-conversion campaign bids from 10 users' data and performs worst. ROAS usually falls with conversion volume down the campaign list, and he calls that "usually causally related". Merging all into the top campaign gives 90 conversions a month and better bids. [379b1f714127]

4. **The default is 1 campaign. Every extra campaign needs heavy justification.** "The goal is always one campaign; that's never realistic but it's the default." The account's complexity should match the business's complexity. An agency that does not know the business "down to the grade C inventory level" will either split with no reason or merge when a split would serve the business. [379b1f714127] [a715afa0c38a]

5. **Only 4 reasons justify a campaign split.** (1) Brand vs non-brand: PMax should not run on brand searches; if you want brand placements and cold reach, run 2 campaigns ("I would always recommend this"). (2) Geography: multiple countries "should always" be split at campaign level. (3) Different margins or efficiency goals: a 70% gross margin collection cannot share a bid strategy with a 35% one; at a 300% target ROAS one is barely profitable and one is very profitable, and Google, blind to margin in most setups, sends spend to whichever makes more revenue. (4) Product categories that learn toward different personas (example: office chairs vs plants). Margin numbers are illustrations. [a715afa0c38a] `[needs brand data: gross margin by collection; countries sold; category list]`

6. **Business reasons can justify a split outside the 4.** The source's worked example has 3 campaigns that break the consolidation rule on purpose: grade C inventory that would otherwise need an 80% discount or be given away (gets a little spend to clear stock even though it converts poorly), new arrivals (to surface them at the top of Shopping and keep seasonal range relevant), and the core campaign. The source does not reconcile this with "only 4 justifications"; treat inventory clearance and new arrivals as commercial reasons the source accepts. [379b1f714127] `[needs brand data: aged or grade C stock; new arrival cadence]`

7. **Use single topic ad groups (STAGs), not single keyword ad groups (SKAGs).** SKAGs worked when ads had 3 fixed headlines and 1 or 2 descriptions you ordered yourself. Responsive search ads have 15 headlines, 4 descriptions and other assets, about 2,700 combinations, and need about a quarter million impressions to test. One exact keyword never gets there. Put 10 to 20 themed keywords under each topic and write the ad to the theme; the RSA adapts headlines per keyword. His agency still onboards SKAG accounts, moves them to STAGs, and "always" sees better results. He allows that SKAGs may still work in some accounts. His worked example is a service business (plumbing). [61f688e47745] `[web check: RSA asset limits]`

8. **Google's advice is right about 20% of the time; test it.** He says Google and Facebook "want you to spend a lot of money" and their advice is not what you should do 80% of the time, but consolidation of keywords is one of the 20% he has tested and confirmed. Opinion, not data. [61f688e47745]

### 2.3 Shopping vs search

9. **Ecommerce should put 80% to 90% of Google spend in Shopping, not Search.** Reason: pre-click information. A search ad gives a headline, a description "no one reads" and a few extensions; no price, look or options. A Shopping listing shows image, price, title, promos or reviews, brand and extensions, with about 5 competitors beside it, so the shopper compares 6 listings and arrives pre-sold. Search clicks cost "$1 to $2" in his example and bring more mismatched visitors, worst in visual categories like fashion. Move into Search only after Shopping is saturated. Elsewhere he says "90% of your focus" for "90% of ecommerce brands". [0faae8bbc52a] [30bbbd9532ea]

10. **Exception: ecommerce with a B2B component.** Business buyers skip Shopping listings because unit prices ($5, $10) do not match a bulk or supplier purchase, and click search ads instead. Example: bulk eyelashes to technicians and small businesses; tea for a cafe. Here Search can beat Shopping. [0faae8bbc52a] [30bbbd9532ea] `[needs brand data: share of orders that are bulk or trade]`

11. **Lead gen readers should swap "shopping" for "search".** The source says this once, about the PMax vs standard shopping allocation. [8ac98b834d71]

### 2.4 Performance Max

12. **PMax is not the enemy; PMax on default settings is.** It works with the right asset group structure, brand exclusions, audience signals treated as signals, and feed-only used where it fits. [903e91b5cc9d] [fd408fa56660]

13. **PMax over-credits itself because it retargets.** His agency's past ramp tests: PMax and standard shopping both at 5x; scale one or the other 2x over 30 days. Every time, the standard shopping ramp gave better incremental backend revenue, even though its in-platform ROAS fell (to about 4x and 3x) while PMax still showed 5x. Standard shopping drives cold traffic that PMax later retargets and takes the last click for. Note the card says the ramps were on different accounts; the transcript says "on another account", so the comparison is across accounts. [8ac98b834d71]

14. **PMax is good for small accounts and plateaus at scale.** Under about $15k to $20k a month, PMax "gets the account moving". Scaled to $100k to $300k a month on large accounts, doubling budget at a reported 5x ROAS did not move backend revenue. Raising budget further or raising target ROAS both push spend into warm and repeat traffic, and PMax becomes "a glorified retargeting campaign". [8ac98b834d71]

15. **Ask what share goes to PMax, not whether to run it.** For most mid to upper market ecommerce: "not a lot to PMax, 20 30 40% maybe", with much of the spend in standard shopping. [8ac98b834d71] `[needs brand data: current spend split PMax vs Shopping vs Search]`

16. **Industry view the source reports: 50% or more of PMax conversions are repeat or warm customers PMax did not acquire.** He says agency owners agree "behind closed doors". Standard shopping under-attributes when it sits beside PMax. Hearsay, not measured. [b390a3400b4f] `[needs brand data: new vs returning customer split by campaign]`

17. **Segment PMax at asset group level, and customise each listing group.** Asset group = images, headlines, descriptions used on Search, Display, YouTube, Discover, Gmail and other placements. Listing group = the products from the GMC feed, used for Shopping placements. Biggest mistake: 1 default asset group. Bigger mistake: several asset groups whose listing groups all hold every product. 4 reasons to segment even though consolidation wins: (1) creative relevance in retargeting and cold (jeans viewer sees jeans); (2) audience signals can be specific ("in market for jeans" vs "fashion"); (3) search themes can be specific; (4) you see performance by asset group (tops beating jeans due to seasonality, checked against Keyword Planner and demand forecasts, then move budget). [fd408fa56660]

18. **Simpler PMax structures beat hyper-segmented ones.** Early on his agency tested accounts with about 200 asset groups split by listing group, search theme and product type. Simpler structures "always performed better". "Don't go and throw 400 asset groups in the account." [fd408fa56660]

19. **Audience signals and search themes are directions, not targeting.** They help at launch when there is no conversion data. Google bypasses them once it has real conversion data. After 30 days of conversion data "the audience signal has done its job" and removing it "won't impact performance at all". For mature accounts spending $30k to $100k a month on PMax, they are "a 1% lever at best" (transcribed "1enter"). They matter on a new business, new product, new asset group or new category. Flagged by the source as controversial. [903e91b5cc9d]

20. **PMax priority order (ecommerce, PMax weighted to Shopping).** (1) GMC feed: titles, descriptions, images. (2) Brand exclusions ("if you don't have them, they are just retargeting campaigns"). (3) Asset and listing group structure plus the quality of the assets. (4) Bidding strategy. (5) Audience signals and search themes. Condition: the ranking assumes PMax puts most spend into Shopping. [903e91b5cc9d]

21. **Feed-only PMax forces spend toward Shopping.** Delete all asset groups so only the listing group remains. Source says PMax can then place only on Shopping and display retargeting with product tiles, which is what Smart Shopping used to be. Use it to stop PMax drifting into YouTube, Gmail or Search. Conflict: the card's editorial note (citing Google help pages) says omitting manual creative does not guarantee placement isolation and Merchant Center data can generate assets automatically. Treat feed-only as a test, and check actual channel delivery. [d4571d60eeee] `[web check: feed-only PMax placement behaviour and channel reporting]`

22. **You can mix PMax campaigns.** Some categories can have their own PMax, some feed-only, some full asset. [d4571d60eeee]

### 2.5 Bidding

23. **Max conversion value first, then target ROAS for stability.** Target ROAS does not raise average performance; over time it averages "somewhat similar" to max conversion value. It trades big swings for day-to-day reliability. Most teams want steady daily revenue, so moving to target ROAS once data exists is "generally what you should do". [29bf1d1ed526]

24. **Raising target ROAS narrows the audience toward warm users.** A higher target makes the campaign bid only on the people it can hit that return on, who are mostly site visitors, existing customers and people who saw your Meta ads. Worked example: set 400% under a trailing 420% to 430%; then 425%, 450%, 500%; spend pulls back until equilibrium. The account went from about 4x to about 6x ROAS at $1,000 a day, which looks like great media buying, but the earlier 4x position "was probably a better position" because it reached more cold traffic. [29bf1d1ed526]

25. **Expansive vs restrictive bidding.** Expansive: maximize conversions and maximize conversion value; can enter any auction; wins auctions it would not have won and loses some it would not have lost; higher risk. Restrictive: target CPA and target ROAS; only enter auctions that meet the efficiency goal. Concept (not a measurement): expansive puts about 30% of budget into testing new keywords, audiences, placement types, regions and adjacent bets, which unlocks scale; restrictive puts about 0%. How restrictive depends on the gap: hitting 4 with a 4.5 target means 0% testing; hitting 5 with a 2 target behaves more like max conversion value. [07bdd8638a6a]

26. **Do not stay on target ROAS permanently.** Being on it for a long time silos the account in one audience and demographic that does not evolve with the business or platform and can "negative feedback loop". He rotates between expansive and restrictive "over extended time periods". The source gives no rotation length. [07bdd8638a6a] [3001e5a56d5d]

27. **Ecommerce should bid for value about 90% of the time.** Max conversions and target CPA chase the lowest CPA and most orders, so spend flows to the cheapest product. Example: $40 t-shirt at about $20 CPA and 2x ROAS vs $200 jumper at about $60 CPA and 3.5x ROAS; conversion bidding funds the t-shirt, value bidding would fund the jumper. Target CPA is a sub-type of max conversions; target ROAS is a sub-type of max conversion value. Note: the card 07bdd8638a6a says value bidding "reflects product margin differences"; the source says value bidding reflects order value, and elsewhere says Google usually cannot see margin. [ed1a69221ddc] [07bdd8638a6a] `[needs brand data: price and margin by product]`

28. **The target ROAS death spiral.** Pattern: spend steady, ROAS dips, the campaign misses its target, spend trails off, campaigns "just die". Mechanism: to hit the target it shrinks the audience; fewer conversions mean less of the last 30 to 90 days of data it models from; small samples make targeting worse; volume falls further. Triggers can be seasonality, a strong product going out of stock, anything that cuts conversions (example: 100 conversions a month falling to 80). If you leave the target, the campaign dies. If you lower it, lower it aggressively; timid cuts fail. [3001e5a56d5d]

29. **Feeder strategy for cold acquisition.** Run a broad campaign at a very low target ROAS (example 50%, a 0.5 ROAS) that reaches the whole pool of relevant searchers, plus a high target ROAS campaign (example 600%) that only reaches warm, in-market, likely buyers. The first drives cheap traffic; the second converts it on the 2nd or 3rd click. Most advertisers only bid on the high-intent half of searchers, so auctions for low-intent-looking first-time searchers are cheap. Usual setup: standard shopping as the cold leg, PMax as the high target ROAS leg. Source says it "works on a lot of accounts". ROAS levels are examples. [b390a3400b4f] `[needs brand data: margin and cash to fund a deliberately low-ROAS cold campaign]`

30. **Portfolio bid strategies merge learning across split campaigns.** Set the bid strategy at account level and apply it to several campaigns so they learn together; useful when you need segmentation but want pooled learning. It also lets you add a max and min CPC to target ROAS or max value (example: high-end furniture where clicks can cost $10 to $30; cap at $10). He says the merged-learning feature is also in "SA3" (likely Search Ads 360) for enterprise. [8d6cc6ef07b8] `[verify UI]` `[web check: portfolio bid limits by campaign type]`

31. **Smart bidding exploration (Search only).** Lets a target ROAS campaign go outside its target in 10%, 20%, 30% bands to test auctions. A middle ground between restrictive and expansive. Not available on PMax or Shopping in his experience. He recommends "looking into" it; he gives no results. [97caffb37450] `[verify UI]` `[web check: smart bidding exploration name and availability]`

32. **Manual CPC and maximize clicks are for new accounts only.** New accounts with no conversion data may be forced into manual bidding ("at least the last time I checked"). Established accounts should not use them unless a skilled agency runs a deliberate arbitrage test, which his agency does rarely ("won't see it in 90% of accounts"). On Search, "generally" use a smart strategy such as target ROAS or max conversions. [9b1a4ac01c87] `[web check: smart bidding eligibility for new accounts]`

### 2.6 Search campaigns

33. **Search is a minor lever for most ecommerce.** "Transparently, search campaigns is not something that we focus on that much." [0faae8bbc52a]

34. **Negative keywords matter most in the first 30 days.** New search campaigns go broad and pick up irrelevant terms. Review negatives weekly in month 1, daily if budgets are very high. After month 1 drop to "weekly-nightly" (as transcribed; possibly weekly to fortnightly). Do not over-edit: each change "does reset learnings" a little. Keep a universal negative list at account level so every new campaign inherits it (jobs, careers, interns, hiring, salary). He says you can find one online or ask an LLM to build one. [12e5a4881580]

35. **RSAs are in learning most of the time.** 2,700 combinations x an assumed 100 impressions each = 270,000 impressions to exit learning (he says 100 is too few to trust). So minimise segmentation; in most accounts RSAs stay in learning "indefinitely". [fd776d0fc197]

36. **CPC is a vanity metric in the middle range.** Across large datasets, CPC has "very little relationship" with ROAS or ROI, at account, campaign and product level. Only the extremes signal: about $100 CPC is never profitable; about 10 cents is probably junk traffic. Click quality comes from how well automated bidding picks likely buyers. [087445947ca9]

37. **Conversion rate and AOV decide who can afford to win the auction.** Whoever can pay most wins. Converting 2x better than competitors lets you pay 2x per click for the same profit. Higher AOV does the same. All in-platform work (structure, asset groups, signals, feed) aims to enter better auctions and raise quality score so your effective bid is lower. But a competitor with better conversion rate and AOV can outbid you "with worse ads, with a worse campaign structure, with worse everything". [78d712129ebc]

38. **Landing page testing is one of the biggest Search levers.** "Very little people" split test landing pages from search ads. Opinion from agency experience. [bd9b251ac5b1]

39. **Exclude brand on Search campaigns** (cold search). [9b1a4ac01c87]

### 2.7 Merchant Center feed

40. **The feed is one of the most important Shopping levers.** Shopping uses the feed to decide which terms to show on, and quality score depends on it. The most important element is the product title. "Most GMC titles are not optimized." [a1c3cff78bf2] [903e91b5cc9d]

41. **Titles lead with converting search terms, brand last or gone.** Default titles look like "[Brand] Nathan Dress Size 12 [colour]". Brand means nothing when brand is excluded and already shows at the bottom of the listing. An internal name like "Nathan" means nothing unless shoppers know the product. Rebuild: keep the unique name if needed, add keywords at the front or right after name and type (example: "formal dress"), add as many attributes as fit the title length (colour, so "blue dress" searches match), push brand to the end (keep it if you are a big retail brand; drop it if nobody knows you). Keywords come from search term reports of what converted, never invented. CPG allows more freedom: "creatine powder" becomes "dissolvable creatine powder, clear, flavored, portable" then brand. "There isn't a golden rule." [a1c3cff78bf2] `[needs brand data: search term report with conversions]` `[web check: current GMC title length limit]`

42. **Each variant can target its own keyword pool.** If 50 g, 100 g and 500 g variants each create their own Shopping listing (depends on feed setup), give each its own title, image and description aimed at different keywords, even though all land on the same product page. [a1c3cff78bf2]

43. **Images take about 70% of the listing and drive the click.** Price and title matter too, but the image mostly decides. Aim to hook the right buyer, not everyone (he cites Eugene Schwartz on headlines). In practice, within brand rules, build contrast with competing listings: if competitors shoot on white, keep a shoot but change the background colour. [829c77305316]

44. **Use 4:5 images.** Fashion images often come as "9 by 6" (as transcribed) and get auto-cropped badly. Override with a supplementary feed of 4:5 images, which he says "is now the default image ratio that Google wants". [829c77305316] `[web check: Merchant Center recommended image aspect ratio]`

45. **1 feed per currency.** Running all regions through 1 feed in 1 currency makes Shopping show a live conversion ("converted from AUD", "USD plus tax"), which "immediately kills click-through rates and conversion rates" because shoppers think the store is foreign. [d68cec537fb6] `[web check: current Merchant Center multi-country and currency setup]`

46. **Descriptions and other attributes are a one-time clean-up.** "That should honestly already be in place. If it's not, do it." The source gives no detail on which attributes. [d68cec537fb6] [829c77305316]

### 2.8 Budgets and tracking

47. **Raise Google budgets in about 20% steps; cut faster.** The 20% rule "is real" on Google. Google is a stable platform that drives conversions consistently and wants slow, methodical changes. Do not double budgets overnight and do not change target CPA overnight (transcribed "having a target CPA", likely "halving"). Cutting from high budgets fast is "generally okay". Meta and TikTok tolerate much faster increases. [7003ff9f69ce]

48. **"Limited by budget" is a hint, not proof.** He sees it on nearly every account at any spend, including PMax campaigns at $5,000 to $10,000 a day in a very small Australian market. [a36358d5ff15]

49. **Do not use GA4 events as the primary conversion.** He reports a 10% to 15% attribution gap, "sometimes even higher", versus the Google Ads tag installed directly on the site. Use enhanced conversions and auto-tagging. [18f7a08a224c] [2792071d2d2e] `[needs brand data: Google Ads tag vs GA4 conversion counts]`

## 3. Procedures

### 3.1 Restructure an account toward consolidation

1. List every campaign with its 30-day conversions and ROAS. [379b1f714127] `[needs brand data: campaign-level conversions]`
2. Look for ROAS falling with conversion volume across campaigns that hold the same products.
3. Start from a target of 1 campaign. For each extra campaign, write which reason it serves: brand vs non-brand, geography, margin or efficiency goal, product category, or a stated commercial need (clearance stock, new arrivals). [a715afa0c38a] [379b1f714127]
4. Merge campaigns with no reason: move products and budget into the highest-volume campaign.
5. Where splits must stay but learning is thin, apply a portfolio bid strategy across them. [8d6cc6ef07b8] `[verify UI]`
6. Judge the change on backend revenue, not only in-platform ROAS. [379b1f714127]

### 3.2 Build a PMax campaign

1. Keep brand out: add a brand exclusion list (campaign settings > brand exclusions > add new brand; Google indexes branded terms; select the list) and also add brand negative keywords on the PMax campaign. Use both as fail-safes. [903e91b5cc9d] `[verify UI]`
2. Create 1 asset group per product type (examples: chairs, tables, lighting, decor; hand tools, power tools, fasteners, hardware accessories). Minimum 3, maximum 20 asset groups. [fd408fa56660]
3. In each asset group, customise the listing group so it holds only that product type. [fd408fa56660] `[verify UI]`
4. Aim for at least 15 products per asset group (flexible with SKU count). Never 1 product alone; it will get little spend, even a hero product. [fd408fa56660] `[needs brand data: SKU count per product type]`
5. Fill assets well: headlines, images, descriptions. Weak assets make weak ads. [903e91b5cc9d]
6. Add an audience signal per asset group, as specific as the group (example: in market for denim, age, interests). [fd408fa56660]
7. Add search themes from keywords that converted in past search campaigns. Do not make them up. [903e91b5cc9d] `[needs brand data: converting search terms]`
8. Launch on maximize conversion value. [29bf1d1ed526]
9. After 30 days of conversion data, signals have done their job; the source says they can be removed with no impact. [903e91b5cc9d]
10. Once data exists, move to target ROAS set a little under trailing ROAS (example: trailing 420% to 430%, set 400%). Move slowly. [29bf1d1ed526] [7003ff9f69ce]
11. Do not keep raising the target to squeeze more ROAS. Watch spend and new-customer share. [29bf1d1ed526]

### 3.3 Switch a PMax campaign to feed-only

1. Use when PMax drifts into placements you do not want (YouTube, Gmail, Search) or you want spend forced toward Shopping. [d4571d60eeee]
2. Before switching, confirm Merchant Center link, eligible products, correct prices and stock, and tested purchase value tracking (card addition). [d4571d60eeee]
3. Delete all asset groups so only the listing group remains. [d4571d60eeee] `[verify UI]`
4. Turn URL expansion off. If on, it adds URLs, scrapes information and builds asset groups by itself. [d4571d60eeee] `[verify UI]`
5. Turn automatically created assets off. [d4571d60eeee] `[verify UI]`
6. Check actual channel delivery after the switch, plus product results and new vs returning customers. Do not assume Shopping-only delivery (card's correction). [d4571d60eeee] `[web check: PMax channel performance report]`

### 3.4 Set up a feeder strategy

1. Confirm PMax has plateaued or you suspect warm-traffic over-crediting. [b390a3400b4f] [8ac98b834d71]
2. Build a standard shopping campaign with a broad reach and a very low target ROAS (source example 50%). [b390a3400b4f] `[verify UI]`
3. Run PMax (with brand exclusions) at a high target ROAS (source example 600%) as the warm converter. [b390a3400b4f]
4. Judge the pair together on backend revenue and new customers, not each campaign's reported ROAS, since shopping under-attributes beside PMax. [b390a3400b4f] `[needs brand data: backend revenue, new customer count]`
5. The source does not give budget split, test length or kill rules for the feeder. Set them from margin and cash. [b390a3400b4f]

### 3.5 Choose a standard shopping structure

1. Top sellers split: 1 campaign with top sellers, 1 with everything else. Aim for about 80% of spend on the top 20% of products while the second campaign keeps testing budget to find new winners. Only for large SKU counts outside fashion. Not for fashion ("a lot of reasons", not given) and not for 5 to 10 product stores. [e2e3fde986ec]
2. Feeder: standard shopping as cold leg (3.4). [e2e3fde986ec]
3. Flow boost labelizer: tier products into over-index (above expected), index (hitting target), near-index (just below), under-index (below), no-index (zero performance) on 30-day rolling results; give each tier its own bid strategy and budget. Label by hand with custom labels for small catalogues, or run an automated labelizer script that re-tiers in real time. Only for thousands of SKUs. [e2e3fde986ec] `[web check: labelizer script options]`
4. Any further split still needs 1 of the 4 reasons. [e2e3fde986ec]

### 3.6 Build or fix a search campaign

1. Group keywords into topics: 10 to 20 themed keywords per ad group; write the RSA to the theme. [61f688e47745]
2. Turn display network off. [18f7a08a224c] `[verify UI]`
3. Exclude brand. [9b1a4ac01c87]
4. Use smart bidding (target ROAS or max conversions) in established accounts; never broad match with maximize clicks. [9b1a4ac01c87] [18f7a08a224c]
5. Apply the account-level universal negative list. [12e5a4881580]
6. Month 1: review search terms and add negatives weekly, daily at high budgets. After month 1: less often, and avoid over-editing. [12e5a4881580]
7. Consider smart bidding exploration if on target ROAS. [97caffb37450] `[verify UI]`
8. Run landing page tests (3.7). [bd9b251ac5b1]

### 3.7 Landing page rotation on search

1. In each ad group, duplicate the ad: ad 1 to landing page 1, ad 2 to landing page 2. [bd9b251ac5b1]
2. Keep the ads otherwise the same (card addition; the source only says "duplicate it").
3. Compare conversion rate over 30 to 60 days. [bd9b251ac5b1]
4. Keep the winner. Turn off the loser. Add ad 3 with landing page 3 against the winner. Repeat. [bd9b251ac5b1]
5. Where possible also test AOV changes, so revenue per visitor rises and you can bid more. [bd9b251ac5b1] `[needs brand data: conversion rate and AOV per landing page]`

### 3.8 Rewrite GMC titles

1. Pull the search term report; find converting terms per product type. [a1c3cff78bf2] `[needs brand data: search terms with conversions]`
2. Draft titles: converting keyword plus product type first (or unique name then keyword), then attributes (colour, size and similar), brand last or removed. [a1c3cff78bf2]
3. For variants with separate listings, write each title, image and description for a different keyword pool. [a1c3cff78bf2]
4. Roll out in batches, highest-opportunity products first; never switch all titles at once, since a bulk switch "resets learning phases on every campaign". [18d6b809b70b] [2792071d2d2e]
5. After each batch, watch CTR, CPC and returns on the changed listings. If no material change, test different keywords. [18d6b809b70b]
6. Record a baseline before each batch (card addition). [18d6b809b70b]

### 3.9 Fix feed images and currency

1. Check image ratio; if auto-cropped, supply 4:5 images through a supplementary feed. [829c77305316] `[verify UI]`
2. Look at the listings you appear beside; change background or styling so yours stands out, within brand rules. [829c77305316]
3. Check each market's listings for a converted-price label. If present, set up a separate feed per currency. [d68cec537fb6] `[verify UI]`

### 3.10 The 90-day rollout (source's order)

1. Tracking: no GA4 events as primary conversions ("J4" in transcript); fire conversion events with enhanced conversions and auto-tagging on. [2792071d2d2e] `[verify UI]`
2. Structure map: how many campaigns (goal is 1), commercial reason for each extra one, brand vs non-brand split, consistent naming. [2792071d2d2e]
3. PMax check: asset groups by product type, listing groups split, brand exclusions on, audience signals present (not urgent), target ROAS not so high it turns PMax into retargeting. [2792071d2d2e]
4. Bidding check: expansive vs restrictive, conversions vs value. [2792071d2d2e]
5. Waste audit: kill tiny campaigns (example: $400 a month) and roll spend up; add negatives for unprofitable search terms; turn off display on search. [2792071d2d2e]
6. Asset health check: sitelinks, call ads (as transcribed; possibly "callouts"), promos that are not stale, all asset types filled in every campaign to take more space on the results page. [2792071d2d2e] `[verify UI]`
7. Feed check: titles, images, other attributes, rolled out slowly (3.8). [2792071d2d2e]

The source numbers these steps 1 to 6 plus "lastly", and does not assign weeks to them.

## 4. Rules, thresholds and numbers

| rule | number or threshold | condition | source's basis | card id |
|---|---|---|---|---|
| Underspend illustration | Google capped near $10k/month while Meta spends millions | category has cold search demand | illustration | fb0673e2ae6d |
| Default campaign count | 1; each extra needs a reason | all accounts | agency practice | 379b1f714127 |
| Siloed learning example | 50 / 20 / 10 conversions per 30 days; merged = 90 | same products in 3 campaigns | illustration | 379b1f714127 |
| Split reasons | 4: brand, geography, margin/efficiency, category | any split | agency practice | a715afa0c38a |
| Margin split example | 70% vs 35% gross margin at 300% target ROAS | different margins, 1 bid strategy | illustration | a715afa0c38a |
| Clearance stock example | grade C stock needing 80% discount | own campaign with a little spend | illustration | 379b1f714127 |
| Shopping share of ecommerce spend | 80% to 90% (also "90% of focus") | consumer ecommerce; not B2B | agency view | 0faae8bbc52a, 30bbbd9532ea |
| Search CPC example | $1 to $2 per click | fashion search example | illustration | 0faae8bbc52a |
| Competitors beside a Shopping listing | about 5 (6 listings compared) | Shopping results | observation | 0faae8bbc52a |
| STAG size | 10 to 20 themed keywords per ad group | search | agency practice | 61f688e47745 |
| RSA combinations | about 2,700 (15 headlines, 4 descriptions) | RSA | source's arithmetic | 61f688e47745, fd776d0fc197 |
| RSA test volume | about 250,000 impressions; 270,000 at 100 per combination | exit learning | source's arithmetic; 100 is too low | 61f688e47745, fd776d0fc197 |
| GA4 vs Ads tag gap | 10% to 15%, sometimes higher, missed | GA4 as primary conversion | observation | 18f7a08a224c |
| PMax good for small accounts | under about $15k to $20k/month | account scale | agency view | 8ac98b834d71 |
| PMax plateau | $100k to $300k/month; 2x budget at 5x ROAS, no backend change | large accounts | agency tests | 8ac98b834d71 |
| Ramp test | 2x budget over 30 days; shopping ROAS 5x to 4x to 3x, PMax stays 5x | test design | agency tests, across accounts | 8ac98b834d71 |
| PMax share of spend | 20% to 40% | mid to upper market ecommerce | agency view | 8ac98b834d71 |
| PMax over-attribution | 50%+ of PMax conversions are repeat or warm | PMax beside Shopping | hearsay from agency owners | b390a3400b4f |
| Asset groups per PMax | min 3, max 20 | most businesses | agency practice | fd408fa56660 |
| Products per asset group | at least 15; never 1 | depends on SKU count | heuristic | fd408fa56660 |
| Over-segmented PMax tested | about 200 asset groups; do not go to 400 | early PMax testing | agency tests | fd408fa56660 |
| Audience signal life | not needed after 30 days of conversion data | any PMax | agency view (controversial) | 903e91b5cc9d |
| Signals for mature accounts | about 1% lever at best | $30k to $100k/month on PMax | agency view | 903e91b5cc9d |
| PMax drift case | YouTube 2% to 10% of spend, Gmail about 10%, ROAS down about 20% | one client, a couple hundred thousand/month | case | d4571d60eeee |
| Gmail click cost appearance | about 10 cents; counts email open as click | PMax on Gmail | observation | d4571d60eeee |
| First target ROAS | a little under trailing (trailing 420% to 430%, set 400%) | moving from max value | example | 29bf1d1ed526 |
| Target ROAS trap | 400% to 425% to 450% to 500%; 4x to 6x at $1,000/day | raising target repeatedly | illustration | 29bf1d1ed526 |
| Expansive testing share | about 30% of budget | max conversions / max value | concept, not measured | 07bdd8638a6a |
| Restrictive testing share | about 0% | target near achieved (4 vs 4.5) | concept | 07bdd8638a6a |
| Loose target | hitting 5 with target 2 acts like max value | restrictive with big gap | concept | 07bdd8638a6a |
| Value vs conversions | value bidding about 90% of the time | ecommerce | agency view | ed1a69221ddc |
| T-shirt vs jumper | $40 at $20 CPA, 2x vs $200 at $60 CPA, 3.5x | mixed price catalogue | illustration | ed1a69221ddc |
| Target ROAS data window | last 30 to 90 days of conversions | how target ROAS models | source's claim | 3001e5a56d5d |
| Spiral trigger example | 100 to 80 conversions in 30 days | seasonality, stock-out | illustration | 3001e5a56d5d |
| Feeder cold leg | target ROAS as low as 50% (0.5) | feeder strategy | example | b390a3400b4f |
| Feeder warm leg | target ROAS about 600% | feeder strategy | example | b390a3400b4f |
| Top seller split | 80% of spend on top 20% of products | large SKU count, not fashion, not 5 to 10 products | agency practice | e2e3fde986ec |
| Labelizer tiers | 5 tiers on 30-day rolling performance | thousands of SKUs | agency practice | e2e3fde986ec |
| Max CPC cap example | $10 cap where clicks run $10 to $30 | high-end furniture, portfolio strategy | example | 8d6cc6ef07b8 |
| Smart bidding exploration | 10%, 20%, 30% bands outside target | Search only | source's description | 97caffb37450 |
| Negative review cadence | weekly in first 30 days; daily at high budgets; less after | new search campaigns | agency practice | 12e5a4881580 |
| CPC extremes | about $100 never profitable; about 10 cents junk | outer range only | observation | 087445947ca9 |
| Conversion rate edge | 2x conversion rate lets you pay 2x per click | auction logic | illustration | 78d712129ebc |
| Landing page test window | 30 to 60 days | search ad groups | agency practice | bd9b251ac5b1 |
| Budget increase step | about 20% | Google; Meta and TikTok can go faster | agency view | 7003ff9f69ce |
| Limited by budget example | $5k to $10k/day PMax still flagged | small Australian market | observation | a36358d5ff15 |
| Shopping image share of listing | about 70% | Shopping listing | source's claim | 829c77305316 |
| Image ratio | 4:5 | Shopping images | source's claim | 829c77305316 |
| Tiny campaign to kill | example $400/month | waste audit | example | 2792071d2d2e |

## 5. Diagnostics and checks

| check | how | good | bad | next step | card |
|---|---|---|---|---|---|
| Over- or underspend | Compare Google spend changes with backend revenue over time `[needs brand data: backend revenue]` | Revenue moves with spend | Spend up, revenue flat (overspend); tiny budget in a big search category (underspend) | Hold or redistribute; or test more spend on cold terms | fb0673e2ae6d |
| Siloed campaigns | Campaign list: 30-day conversions vs ROAS | Few campaigns, each with a split reason | ROAS falls with volume; same products in several campaigns | Merge, or apply a portfolio strategy | 379b1f714127, 8d6cc6ef07b8 |
| Split reasons | For each campaign, name the reason | Each maps to brand, geo, margin, category or a stated commercial need | No reason given | Consolidate | a715afa0c38a |
| Margin mixing | Compare gross margin of collections sharing a bid strategy `[needs brand data: margin by collection]` | Similar margins | 70% and 35% lines under 1 target | Split by margin tier | a715afa0c38a |
| Conversion source | Google Ads conversion settings: primary action source `[verify UI]` | Google Ads tag with enhanced conversions, auto-tagging on | GA4 event as primary | Switch primary; compare counts | 18f7a08a224c, 2792071d2d2e |
| PMax asset groups | Count asset groups; open each listing group | 3 to 20 groups by product type, each listing group filtered | 1 group; or many groups all holding every product; 1-product groups | Rebuild per 3.2 | fd408fa56660 |
| PMax brand exclusion | Campaign settings and negative keywords `[verify UI]` | Brand list plus brand negatives | Neither | Add both | 903e91b5cc9d |
| PMax warm share | New vs returning split by campaign `[needs brand data: customer type by campaign]` | Healthy new-customer share | Mostly repeat or warm (source says 50%+ is common) | Lower target, move budget to standard shopping, consider feeder | b390a3400b4f, 8ac98b834d71 |
| PMax plateau | Budget steps vs backend revenue | Revenue follows budget | ROAS holds, revenue flat | Shift share to standard shopping (20% to 40% PMax) | 8ac98b834d71 |
| PMax channel drift | Channel or placement breakdown `[verify UI]` | Most spend in Shopping for ecommerce | Sudden click spike, ROAS drop, spend moving to YouTube or Gmail | Feed-only PMax (3.3) | d4571d60eeee |
| Feed-only setup | Settings: URL expansion, auto-created assets `[verify UI]` | Both off | Either on | Turn off | d4571d60eeee |
| Target ROAS trap | History of target changes vs spend | Target a bit under trailing ROAS, spend stable | Target raised step by step, spend shrinking, ROAS rising | Lower target; accept lower ROAS for more cold reach | 29bf1d1ed526 |
| Death spiral | Spend, ROAS and conversions over months | Stable volume | ROAS dip then steady fall in spend and conversions | Cut target aggressively; check stock-outs and seasonality | 3001e5a56d5d |
| Restrictive too long | Time on target ROAS / CPA | Rotated with expansive periods | Months on 1 tight target, audience not growing | Plan an expansive period | 07bdd8638a6a |
| Conversions vs value | Bid strategy type; product-level spend | Value bidding; spend follows higher-ROAS products | Max conversions or target CPA pushing cheapest product | Switch to value; confirm order values pass | ed1a69221ddc |
| Manual bidding | Bid strategy on each campaign | Smart bidding in established accounts | Manual CPC or max clicks; broad match with max clicks | Move to smart bidding | 9b1a4ac01c87, 18f7a08a224c |
| Search network settings | Search campaign networks `[verify UI]` | Display off | Display on | Turn off | 18f7a08a224c |
| Negatives | Search terms report; negative lists | Account-level universal list; brand negatives on cold | No negatives | Build list; weekly review in month 1 | 12e5a4881580, 18f7a08a224c |
| Ad group structure | Keywords per ad group | 10 to 20 themed | 1 keyword per ad group | Move to STAGs | 61f688e47745 |
| Auto-apply recommendations | Recommendations settings `[verify UI]` | Off | On | Turn off | 18f7a08a224c |
| Naming | Campaign names | Agency tag, region, type, audience, optional goal | No pattern | Rename | 18f7a08a224c |
| Limited by budget | Status column | Read as hint; test extra spend and watch backend revenue | Budget raised only because of the flag | Test in 20% steps | a36358d5ff15, 7003ff9f69ce |
| CPC focus | Reports and agency goals | Judged on ROAS, conversion rate, AOV, revenue per visitor | Optimising for lowest CPC | Change the success metric | 087445947ca9 |
| Titles | Sample 20+ feed titles | Converting keyword first, attributes, brand last | Brand or internal name first; no attributes | Rewrite in batches (3.8) | a1c3cff78bf2 |
| Images | View Shopping listings vs competitors | 4:5, no bad crops, contrast with neighbours | Cropped, looks like every competitor | Supplementary feed; new backgrounds | 829c77305316 |
| Currency | Listings per country | Local currency | "Converted from" label | Feed per currency | d68cec537fb6 |
| Assets | Sitelinks, promos, other assets per campaign `[verify UI]` | All filled, promos current | Missing or stale promos | Fill and update | 2792071d2d2e |
| Waste | Spend by campaign and search term | No tiny orphan campaigns; no unprofitable terms | $400/month campaigns with no role; bleeding terms | Kill and roll up; add negatives | 2792071d2d2e |

## 6. Tools, settings and named features

- **Performance Max (PMax):** asset groups, listing groups, audience signals, search themes, brand exclusions, negative keywords (recently added). `[verify UI]` [fd408fa56660] [903e91b5cc9d]
- **Brand exclusion list:** campaign settings > brand exclusions > add new brand; Google indexes branded terms and you apply the list. `[verify UI]` [903e91b5cc9d]
- **Feed-only PMax settings:** URL expansion (turn off), automatically created assets (turn off). `[verify UI]` [d4571d60eeee]
- **Standard shopping:** cold acquisition leg; top seller split; labelizer tiers. [e2e3fde986ec] [b390a3400b4f]
- **Custom labels and labelizer script:** tier products by 30-day rolling performance (over-index, index, near-index, under-index, no-index). Source calls it "flow boost labelizer" (transcribed "flo boost"). `[web check: current labelizer tools]` [e2e3fde986ec]
- **Bid strategies:** manual CPC, maximize clicks, maximize conversions, maximize conversion value, target CPA, target ROAS. [07bdd8638a6a] [9b1a4ac01c87]
- **Portfolio bid strategies:** account-level, shared learning, max and min CPC limits. `[verify UI]` [8d6cc6ef07b8]
- **Search Ads 360:** named as "SA3" (likely SA360) for enterprise shared learning; no detail. `[web check: SA360 feature]` [8d6cc6ef07b8]
- **Smart bidding exploration:** Search only in source's experience. `[verify UI]` [97caffb37450]
- **Responsive search ads:** 15 headlines, 4 descriptions, "the only thing that you can run these days". [61f688e47745] [fd776d0fc197]
- **Match types:** exact (same meaning), phrase (a bit broader), broad. `[web check: current match type rules]` [61f688e47745]
- **Negative keyword lists:** account-level universal list. `[verify UI]` [12e5a4881580]
- **Auto-apply recommendations:** turn off. `[verify UI]` [18f7a08a224c]
- **Display network on search campaigns:** turn off. `[verify UI]` [18f7a08a224c]
- **Limited by budget status.** [a36358d5ff15]
- **Google Merchant Center:** titles, descriptions, images, supplementary feeds, 1 feed per currency. `[verify UI]` [a1c3cff78bf2] [829c77305316] [d68cec537fb6]
- **Keyword Planner and search term reports:** for seasonality checks and title keywords. [fd408fa56660] [a1c3cff78bf2]
- **Enhanced conversions, auto-tagging, Google Ads site tag vs GA4 events.** `[verify UI]` [2792071d2d2e] [18f7a08a224c]
- **Ad assets:** sitelinks, call assets (or callouts), promotions. `[verify UI]` [2792071d2d2e]
- **AI Max, Demand Gen, DSAs:** named as shifts only. `[web check: status and fit for ecommerce]`
- **Smart Shopping:** the old campaign type PMax replaced; feed-only PMax mimics it.

Naming convention the source uses: agency tag | region | campaign type (PMax, shopping, search) | audience (cold, brand, "theta" as transcribed; meaning unclear) | goal (usually dropped because it is almost always sales). [18f7a08a224c]

## 7. Examples and case results

All are the source's own reports, not promises.

- **PMax vs standard shopping ramps:** both at 5x; PMax scaled 2x over 30 days kept a reported 5x but backend revenue lagged; standard shopping ramp on another account fell to about 4x and 3x in platform but gave better backend revenue. "Every single time." [8ac98b834d71]
- **Large accounts:** PMax scaled to $100k to $300k a month; doubling budget at 5x reported ROAS did not move backend revenue. [8ac98b834d71]
- **PMax drift case:** client spending "a couple hundred thousand" a month on PMax. Clicks spiked, ROAS fell about 20%. PMax had moved YouTube spend from 2% to about 10% and put about 10% into cold Gmail. Gmail "clicks" were email opens, not site visits, at what looked like 10-cent clicks, and customers complained about emails they thought they had unsubscribed from. Fix: switched to feed-only PMax; the account "continued to scale". [d4571d60eeee]
- **Hyper-segmented PMax:** accounts with about 200 asset groups underperformed simpler builds. [fd408fa56660]
- **SKAG to STAG migrations:** "we always see better performance" after moving onboarded SKAG accounts to STAGs. [61f688e47745]
- **Target ROAS trap:** a campaign at about 4x and $1,000 a day moved to about 6x at $1,000 a day by raising the target from 400% to 500%+; the source argues the earlier position was better for cold acquisition. [29bf1d1ed526]
- **Limited by budget:** PMax at $5k to $10k a day in a small Australian market still flagged. [a36358d5ff15]
- **B2B search:** bulk eyelash seller did better on Search than Shopping. [0faae8bbc52a] [30bbbd9532ea]
- **Title rewrites (illustrations, no results given):** "Nathan dress size 12" to a title led by "formal dress"; "creatine powder" to "dissolvable creatine powder clear flavored portable [brand]". [a1c3cff78bf2]

## 8. Mistakes the source warns about

1. GA4 events as the primary conversion (10% to 15% or more missed). [18f7a08a224c]
2. 1 asset group in PMax. [18f7a08a224c] [fd408fa56660]
3. Multiple asset groups with un-customised listing groups (every product in every group). [fd408fa56660]
4. 1 product in an asset group; too many asset groups (200 to 400). [fd408fa56660]
5. Broad match with maximize clicks. [18f7a08a224c]
6. Display network on in search campaigns ("one of the worst advertising networks", especially for cold). [18f7a08a224c]
7. No negative keywords, including no brand negatives on cold campaigns. [18f7a08a224c]
8. Auto-apply recommendations left on ("almost always is not in your best interest"). [18f7a08a224c]
9. No naming convention. [18f7a08a224c]
10. No brand exclusions on PMax, which turns it into a retargeting campaign. [903e91b5cc9d]
11. Scaling a plateaued PMax by adding budget or raising target ROAS. [8ac98b834d71]
12. Raising target ROAS step by step and calling it good media buying. [29bf1d1ed526]
13. Lowering target ROAS too timidly once a death spiral starts. [3001e5a56d5d]
14. Staying on a restrictive strategy for a long time. [07bdd8638a6a]
15. Max conversions or target CPA in an ecommerce catalogue with mixed prices. [ed1a69221ddc]
16. Manual CPC or maximize clicks in an established account. [9b1a4ac01c87]
17. SKAGs and hyper-segmented search. [61f688e47745] [fd776d0fc197]
18. Over-editing negatives after month 1 (each edit resets learning a little). [12e5a4881580]
19. Chasing the lowest CPC. [087445947ca9]
20. Segmenting with no business reason, or consolidating when the business needs a split. [379b1f714127]
21. Paying for audits that tweak audience signals or search themes on mature accounts ("literally no impact"). [903e91b5cc9d]
22. Treating "limited by budget" as proof you can spend more. [a36358d5ff15]
23. Doubling budgets or halving target CPA overnight. [7003ff9f69ce]
24. Changing all feed titles at once. [18d6b809b70b] [2792071d2d2e]
25. Default titles with brand and internal names first. [a1c3cff78bf2]
26. Auto-cropped images in the wrong ratio. [829c77305316]
27. 1 feed for all currencies. [d68cec537fb6]
28. Top seller split in fashion or in a 5 to 10 product store. [e2e3fde986ec]
29. Labelizer structures below thousands of SKUs. [e2e3fde986ec]
30. Running fashion search ads that say "we sell dresses" with no visual filter. [0faae8bbc52a]

## 9. Caveats, conflicts and what is missing

- **Incrementality method is thin.** The core claim (PMax over-credits, standard shopping drives cold growth) rests on internal ramps compared across accounts and on hearsay about 50%+ warm conversions. No holdout, geo test or MMM design is given. Use 06-MEA for measurement design. `[needs brand data: new vs returning by campaign; backend revenue]`
- **Feed-only PMax conflict.** The source says feed-only PMax can place only on Shopping and display retargeting. The card d4571d60eeee carries an editorial correction citing Google help pages: no guaranteed placement isolation, and Merchant Center data can generate assets. Treat as a test and check channel reports. `[web check: Google help 14530785 and 15865151]`
- **Audience signal claim is contested by the source itself.** "Might be a little bit controversial." The claim that removing signals after 30 days has no effect is not backed by a shown test.
- **"Only 4 split reasons" vs worked example.** The example structure uses clearance stock and new arrivals, which are not in the 4. The source accepts both as commercial reality.
- **Shopping share numbers vary:** 80% to 90% of spend in one place, "90% of focus" in another.
- **PMax share:** "20 30 40% maybe" is loose.
- **Rotation between expansive and restrictive:** no cadence, trigger or length given.
- **Death spiral fix:** "aggressively" is not quantified. No number for how far to cut the target.
- **Feeder strategy:** no budget split, test length, success metric or stop rule. Needs margin and cash to fund a 0.5 ROAS campaign.
- **Budget changes:** 20% steps given, but no wait time between steps.
- **Negative cadence after month 1:** transcript "weekly-nightly" is unclear.
- **Card drift from the source (check before using the card alone):**
  - 12e5a4881580 says "use topic ad groups ... on the negative keyword side where you have thousands of SKUs". The source says to use topic ad groups (full stop), then starts the negatives topic; "thousands of SKUs" belongs to the labelizer. Ignore that bullet.
  - 07bdd8638a6a says value bidding "reflects product margin differences". The source says it reflects order value; margin is not visible to Google in most setups (a715afa0c38a).
  - 8d6cc6ef07b8 caveat says portfolio strategies and CPC caps "sit outside PMax and Shopping". The source says that only about smart bidding exploration.
  - 30bbbd9532ea adds B2B steps (supplier-intent keywords, separate B2B landing pages, CPA and revenue per click comparison) that the source does not give.
  - a36358d5ff15 adds auction insights and marginal ROAS; not in the source.
  - 9b1a4ac01c87 caveat about portfolio strategies carrying brand exclusions is not in the source.
  - 2792071d2d2e says "no duplicate or stale tags"; the source says no GA4 events.
  - 18d6b809b70b and bd9b251ac5b1 add a recorded baseline and identical ads; sensible but not in the source.
- **Transcription doubts:** "J4" and "G4" = GA4; "SA3" likely SA360; "theta" audience label unclear; "having a target CPA" likely "halving"; "call ads" possibly callouts; "9 by 6" image ratio; "$5 million a month" pitch figure.
- **Platform freshness:** PMax negative keywords, brand exclusions, smart bidding exploration, AI Max, Demand Gen, DSA deprecation, match type definitions, 4:5 image ratio, currency feeds and new-account smart bidding all change. `[web check: each before acting]`
- **Service example for search:** STAG example is plumbing; the source applies it to ecommerce without an ecommerce example.
- **Conflict with common ecommerce advice:** Common advice (and Google's own) often pushes PMax as the main or only ecommerce campaign. This source says PMax should get only 20% to 40% at scale, with standard shopping doing cold acquisition. It also says audience signals barely matter for mature accounts, and that CPC is a vanity metric. Common advice treats "limited by budget" as a scale signal; the source does not. The 20% budget-step rule matches common advice.
- **Missing:** no guidance on tROAS numbers from margin (break-even ROAS), no new-customer acquisition goal settings, no YouTube or Demand Gen detail, no attribution model settings, no seasonality adjustments, no conversion value rules, no specifics on which feed attributes to fix.

## 10. Card index

- fb0673e2ae6d  Diagnose Whether You Are Overspending or Underspending on Google Ads
- 379b1f714127  Consolidate Campaigns Before Segmenting Them
- a715afa0c38a  The Four Justifications for Segmenting a Google Ads Account
- 61f688e47745  Convert SKAGs into Single-Topic Ad Groups
- 18f7a08a224c  Fix the Seven Most Common Google Ads Setup Mistakes
- fd408fa56660  Set Up PMax Asset Groups with Matching Listing Groups
- 903e91b5cc9d  Use Brand Exclusions and Weigh What Actually Matters in PMax
- d4571d60eeee  Run a Feed-Only PMax and Check Actual Channel Delivery
- 29bf1d1ed526  Use Max Conversion Value to Gather Data, Then Move to Target ROAS for Stability
- b390a3400b4f  Build a Feeder Strategy: Cold Shopping Plus Warm PMax
- 8ac98b834d71  Recognise PMax's Ceiling and Reframe the Allocation Question
- e2e3fde986ec  Choose Between the Three Standard Shopping Structures
- 0faae8bbc52a  Keep 80-90% of Ecommerce Google Spend in Shopping, Not Search
- 30bbbd9532ea  Choose Shopping vs Search by Buyer Type
- a1c3cff78bf2  Rebuild Google Shopping Product Titles for Keyword Reach
- 3001e5a56d5d  Diagnose and Break the Target ROAS Death Spiral
- 07bdd8638a6a  Pick Expansive vs Restrictive Bidding by Testing Appetite
- ed1a69221ddc  Maximize Conversion Value Instead of Conversions for Mixed-Margin Catalogs
- 8d6cc6ef07b8  Use Portfolio Bidding to Merge Learnings and Cap CPC
- 97caffb37450  Exploit Search Campaign Smart Bidding Exploration
- 12e5a4881580  Build Negative Keyword Discipline in the First 30 Days
- 087445947ca9  Explain the Low Leverage of Average CPC
- 78d712129ebc  Win More Google Auctions by Raising Your Website's Conversion Rate
- bd9b251ac5b1  Run Continuous Landing Page Split Tests on Search Ads
- 7003ff9f69ce  Change Google Ads Budgets Slowly, Downward Faster
- a36358d5ff15  Interpret 'Limited by Budget' as a Signal, Not a Rule
- 18d6b809b70b  Stagger Feed Title Rollouts to Protect Learning
- 829c77305316  Optimize Shopping Images for Contrast, Not Just CTR
- d68cec537fb6  Set Up Separate Merchant Center Feeds per Currency
- fd776d0fc197  Audit Responsive Search Ads for Learning Starvation
- 2792071d2d2e  Follow a 90-Day Google Ads Implementation Sequence
- 9b1a4ac01c87  Exclude Brand Traffic and Use Smart Bidding on Search
