# ENTIRE google ads algorithm explained in 24 mins

source_id: 1ChjXTPfoKbbQc3OYX-w0ryLOLqGcn1r1  |  folder: /12-GAD-google-ads (moved from /11-ADC-ad-copy-deployment)  |  cards: 16  |  words: 6617  |  type: transcript (YouTube talk, single presenter, auto-captioned, no timestamps)
credibility: Unnamed presenter, an ecommerce store operator who says he started Google Ads with $200 "out of a college dorm room", has "made millions of dollars through Google" and has "lost hundreds of thousands" on mistakes. He runs several stores ("the reason why [I] keep on building more stores") and says he has outcompeted IKEA, AliExpress, Amazon and Home Depot. He sells hands-on coaching ("hold your hand throughout this entire process of starting Google Ads from A to Z", link below). Evidence: his own accounts, 1 store's revenue and profit timeline, a click-share-by-position chart shown on screen (he labels it organic search), and an ad score formula he says was "given out by the DOJ because they legally had to". No controlled tests, no client data set, no screenshots of the formula source. Tone is confident and profane. Treat every rule as "Source 07 says".
date signals: No year stated. He says the deep-versus-wide trade-off vanished "in the past couple months" thanks to AI tools and that he uses Claude to write titles, so 2024 or later `[web check: video publish date]`. The DOJ formula reference points to the US v. Google search trial (2023 to 2024) `[web check: what the trial exhibits actually disclosed]`. Names Performance Max with text, image and video "enhancement" toggles, Google Merchant Center (GMC), My Ad Center (myadcenter.google.com, "manage privacy"), Keyword Planner, standard Shopping, branded Search, target ROAS entered as a percentage, location "presence" versus "presence or interest", and the TV screens device option. All UI steps can change. The Drive file date (21 Sep 2026) is not the recording date.
scope note: The source header files it under ad copy and deployment, but the content is Google Ads mechanics, Shopping feed optimization, PMax setup and scaling, so it belongs in 12-GAD. The header says to skip dorm-room background and the coaching plug. Feed title and description writing overlaps with 15-SEO-search and product data; post-click experience (page speed, delivery) overlaps with 08-SPD-speed and 09-CRO-testing.

## 1. What this source is for

It gives an operator a mental model of how Google picks and prices ads: 4 stages (retrieval, elimination, ranking, auction) driven by an ad score of bid times predicted CTR minus an experience penalty. From that model it derives 1 claim: relevance is the lever at every stage. It then gives a growth tactic ("surface area scaling": duplicate a winning product across price tiers, avatar images and keyword-rich titles to hold several slots), a lean PMax setup limited to Search and Shopping, rules on when to add tROAS and when to layer standard Shopping, a learning-phase view, a weekly review habit, and a branded Search add-on. It is strong on why and on the PMax setup clicks. It is weak on proof, on Merchant Center policy, and on how to measure whether the tactics work.

## 2. Principles

1. **Rank is what matters most, because top slots take most clicks.** Condition: Search and Shopping, any query. Source 07 says "the only thing that matters with Google is just your ranking". Evidence: an on-screen chart he reads as position 1 = 40%, position 2 = 20%, position 3 = 10%, position 4 = 7.2% of clicks; he says the chart is for "organic search" and then applies it to ads. Examples: searching "Asana" shows monday.com first; searching "outdoor lighting", most shoppers click the first Shopping result "because it is the first immediate choice". He says many shoppers do not know what "sponsored" means. The card caveats that these shares vary by query, device and SERP layout, and that position 1 does not guarantee conversions. [a792fb2f1bc7] [bf7fb09f077f]
2. **You compete with a handful of listings, not the whole market.** Condition: any single query. After elimination only a few ads remain, so you are "just up against a couple other people that you're listed next to". [a792fb2f1bc7]
3. **Google runs 4 stages on every search: retrieval, elimination, ranking, auction.** Condition: every search. Source 07 says Google takes "hundreds of millions, if not billions" of ads, condenses them to a couple of thousand, then to "a few, maybe like 10", then ranks them and sets the price. This is his description, not Google documentation. [bf7fb09f077f]
4. **Retrieval reads everything you give Google, so "your feed is your target".** Condition: retrieval stage. Google scans "including but not limiting to" landing page, titles, descriptions, images, price point "if it's relevant to that user", ad assets such as keywords, and demographics. Example: if your images show college students, Google will show the ad to more college students. Example: a search for "orthopedic shoes" retrieves work boots, construction boots, indoor shoes and socks, but a yoga mat seller is thrown out. He calls retrieval "the most intensive part". The image-to-demographic claim is his interpretation, not documented. [bf7fb09f077f] [2dd030a32711] [4657c93cde0f]
5. **Elimination uses an ad score; a negative score removes you.** Condition: elimination stage. Source 07's formula: ad score = bid x predicted click-through rate (pCTR) minus beta, scored from -100 to 100 against the user's search. Elimination cuts 99.99% of retrieved ads. Any ad with a negative score is removed. He attributes the formula to a DOJ disclosure; the card caveats that the exact structure is his interpretation. [bf7fb09f077f] [web check: whether the DOJ trial exhibits show this formula, and the -100 to 100 scale]
6. **Bid is usually automated, so pCTR is the main lever you control.** Condition: automated bidding (anything except standard Shopping, per the source) and a store that is "not a scammer" with "a good-looking store", so beta is near zero. Then "the only thing left to focus on is how can you increase your predicted clickthrough rate". [bf7fb09f077f] [a792fb2f1bc7]
7. **pCTR depends on the searcher as much as on your ad.** Condition: ranking stage. Google uses its data on the person (gender, age, language, relationships, income, education, industry, employer size, home ownership, drawn from Google activity, YouTube history, locations and Google Pay payments) and their buying history. Example: if you bought running shoes a few months ago, Google predicts when you will buy again and times ads to that. So pCTR = the customer's intent plus how relevant you are to their buying history and current search. You can see your own profile at myadcenter.google.com > manage privacy [verify UI]. [bf7fb09f077f]
8. **Ranking orders surviving ads by the same ad score.** Condition: ranking stage. The closer to 100, the higher you rank. [bf7fb09f077f]
9. **Beta is an experience penalty you earn down over time.** Condition: always. Beta rises with slow landing pages, a poor experience, or not shipping ("if you're just flat out a scammer"). It falls as you gather conversions and give customers a good experience "every single day". Lower beta means cheaper clicks and higher rank. He says this is why Google rewards the long term and why "the longer you run a store, the more Google's going to trust you". The card treats beta as the source's framing, not Google-published mechanics. [8beaa7445948] [4657c93cde0f]
10. **Google charges per click, not per impression.** Condition: Search and Shopping. Source 07 contrasts Google (PPC) with Facebook, which he calls pay per impression ("if I watch [an] ad for 5 seconds and I don't end up buying, that advertiser is still going to get charged"). The card draws the implication that an irrelevant click is money spent with no purchase. [bf7fb09f077f] [a0c5917208b0]
11. **CPC = customer intent x your relevance multiplier, and relevance works inversely.** Condition: the auction stage. Source 07 says old-style CPC was set by keyword bids ("literally just meant your relevance"), but "in recent years" Google defines CPC as intent x relevance. His illustration: 3 searchers for "orthopedic shoes" graded by likelihood to buy from ads at 3x, 2x, 1x. 3 ads (socks, running shoes, orthopedic shoes) graded by relevance, where the most relevant gets a 1x multiplier, the next 2x, the least 5x. Most relevant ad + most likely buyer = $3 CPC. Least relevant ad + same buyer = $15 CPC "on something that should have charged you $3". These numbers are illustrative, not a published formula. [a0c5917208b0] [web check: how Google currently documents actual CPC and Ad Rank]
12. **High-intent buyers also bring higher conversion rate and AOV, and they go to the most relevant seller.** Condition: the source extends the auction model downstream. A person who "buys every single thing she sees" is more likely to buy from you and may "spend hundreds if not thousands of dollars per order". You only win her if you are the most relevant click. [a0c5917208b0]
13. **Relevance drives every stage.** Condition: whole pipeline. Relevance gets you retrieved, keeps you from elimination, lifts your rank, and gets you the highest-intent customer at a lower CPC with higher conversion rate and AOV. This is the source's central thesis. [bf7fb09f077f] [a0c5917208b0] [4657c93cde0f]
14. **AI tools remove the deep-versus-wide trade-off.** Condition: catalogs you can expand with AI-written titles and images. Before, you chose deep (1 landing page, 1 product, 1 avatar) or wide (many products and pages, no ideal customer). Source 07 says that "in the past couple months" AI tools let you run hundreds or thousands of products and landing pages, each relevant to 1 customer. He calls this "surface area scaling". [fe7e30671299]
15. **Surface area scaling: when a product works, duplicate it instead of only raising budget.** Condition: 1 product already working. Duplicate it "five or six more times", changing the customer avatar, price point, images, angles and demographics each time, so you hold slots 1 through 6. In Search you then collect 40% + 20% + 10% + 7% instead of only the top share. Example (anecdote): for some products "you have a six out of seven chance of clicking on one of my stores". [fe7e30671299] [a792fb2f1bc7]
16. **Price tier is the most important axis to vary.** Condition: surface area duplicates. Example: a $30 t-shirt duplicated as standard, budget, discount, premium and luxury versions. Reason: shoppers type prices ("best shirts under $30"); without a cheaper listing you are "completely thrown out of the auction", and for "under $100" the higher-priced listings are more likely to appear. The source does not say whether the duplicates are different products or the same product at different prices. See section 9. [fe7e30671299]
17. **People buy from people who look like them, so vary images by avatar.** Condition: product images in Shopping. Competitors show "a piece of clothing on a white background" (example: "black jacket"). Source 07 duplicates the image across avatars (leisure wear, active wear, corporate) so each shopper can see themselves using it. [2dd030a32711]
18. **Titles and descriptions matter most, and are written for the algorithm first.** Condition: Shopping feed titles and descriptions. Source 07 says titles and descriptions are "by far the most important" of the 3 axes (price, images, titles), act "as like SEO towards your brand", and are scanned "within 200 milliseconds", so "you have to make sure you have all the keywords stuffed in there". Each extra word enters a new "keyword pool" (he claims about 100 keywords versus 2). The card rewrites this into a readable-title rule and says more words do not guarantee more eligibility. This is a conflict; see section 9. [f3d645adbbbe] [afd1fd903f18]
19. **Consolidation beats segmentation.** Condition: account structure. Source 07 rejects running "like 10 different campaigns" split by niche or product line. Aim for as close to 1 campaign as possible. Exceptions he allows: brand Search, PMax and standard Shopping "layered" together. Cards flag this as his opinion; margin or region differences can need segments, and SKU-level reporting should be kept anyway. [e5ab20feaa14] [568c59a75126]
20. **For ecommerce, the main campaign is PMax restricted to Search and Shopping.** Condition: ecommerce with a Merchant Center feed. Default PMax also serves on YouTube, Gmail, Display, Maps and Discover; he says those "burn you money". Search and Shopping make "99% of all your revenue", "most of it" from Shopping. [08b3d9f85868]
21. **Do not set a target too early.** Condition: new PMax. He sets no tROAS for about the first 3 months and adds one only at a plateau or efficiency drop. Highly profitable campaigns may never need one; he scaled one to about $500K ad spend without a tROAS "because I didn't want to limit it". [d4494776c11a]
22. **Relevance shortens the learning phase.** Condition: new campaign or new account. Source 07 says Google defines the learning phase as 30 conversions in 30 days (about 1 a day). If titles, descriptions, images, price and products are aligned, you can exit "within like the first like week"; if not, "you're basically going to be in this learning phase forever". [f7a7231a09f3] [web check: Google's current learning-period definition for Smart Bidding and PMax]
23. **Google is a long-term, steadily rising channel; social is a sine wave.** Condition: "if every single thing is in alignment". Expect daily peaks and dips but an upward weekly trend line, and "longevity for two, three, even up to 5 years" of return. Anecdotal. [8beaa7445948] [031ec7c8b2d2]
24. **Go deep on 1 avatar, 1 pain point, 1 use case, then multiply.** Condition: store strategy. He credits his best store to being "super deep on one customer avatar, one major pain point, one major use case" and multiplying that "like 10,000 times across the entire store". [fe7e30671299]

## 3. Procedures

### 3.1 Lean PMax limited to Search and Shopping (source's main ecommerce campaign)
Goal: use PMax's automated bidding while serving only on Search and Shopping. All steps [verify UI]. [08b3d9f85868]
1. Click Create > Campaign.
2. Choose "Create a campaign without guidance".
3. Select Performance Max.
4. Set the goal to Purchases (source: "your account goal").
5. Select your Google Merchant Center (GMC) account.
6. On the bidding page, leave the target fields blank (no target ROAS). Click Next. [d4494776c11a]
7. Locations: choose "Presence". Source 07 believes the default is "presence or interest" and says that "is going to waste you a bunch of money".
8. Devices: turn off TV screens. He has never had a purchase from a TV screen.
9. Asset page: leave every headline, description, image, video and other asset field blank, so only products (the feed) are selected at the top right.
10. Scroll down and turn off text, image and video enhancement (automatic asset generation), so the campaign is not shown on YouTube, Gmail or other placements.
11. Click Next and set the budget. The source gives no budget figure for launch. [needs brand data: daily budget the brand can afford during learning]
12. If Google shows an error for the empty asset group: fill in the asset group fully and publish it, then duplicate it, leave the duplicate entirely blank, publish the duplicate, and pause the original.
13. Ignore ad strength. His ad strength is "poor" in every campaign he runs this way.
Check after: the source gives no check that serving really stayed on Search and Shopping. Add one: review the channel or placement report after launch [verify UI] [web check: whether a feed-only PMax with enhancements off can still serve on YouTube, Display or Gmail, and whether PMax now offers direct channel controls].
Alternative: a standard Shopping campaign "is not going to be AI" but gives more control over CPC. It is the only case where the source says bids are not automated. [08b3d9f85868] [bf7fb09f077f]

### 3.2 Surface area scaling (duplicate a working product)
Goal: hold several slots for the same demand. Preconditions: 1 product already converting [fe7e30671299]. [needs brand data: product-level conversions and margin by SKU]
1. Pick 1 product that is working.
2. Instead of only raising budget, create 5 to 6 duplicate listings.
3. For each duplicate, change the price tier: standard, budget, discount, premium, luxury (source example: a $30 t-shirt). [fe7e30671299]
4. For each duplicate, change the image to a distinct avatar and use case (source example: leisure wear, active wear, corporate for a black jacket). [2dd030a32711]
5. For each duplicate, write a title and description aimed at that tier's and avatar's searches (3.3). [f3d645adbbbe] [afd1fd903f18]
6. Source 07 says each duplicate should change "the price point, the images, the angles, and the demographics" so you "hit for every single type of relevant keyword".
Card additions not in the transcript: track blended CPC and conversion by variant before adding more; rebalance budget by CPA or ROAS per tier; give each variant an internal avatar name; plan for feed, price and stock sync workload. [fe7e30671299] [2dd030a32711]
The source gives no check for Merchant Center policy, no rule for how different the duplicates must be, and no measure of success beyond slot share. [web check: Merchant Center policies on duplicate products, price accuracy and misrepresentation]

### 3.3 Keyword Planner to titles and descriptions
All tool steps [verify UI]. [afd1fd903f18] [f3d645adbbbe]
1. Open Keyword Planner inside Google Ads (free).
2. Enter the core product term (example: "heated jacket").
3. Set your target country. Click Get results.
4. Read the related terms (examples he shows: electric jacket, self-heating jacket, heated coat, heated hunting clothes).
5. Download the keyword list.
6. Give the list plus your title format to an AI writing tool (he uses Claude). He says titles are built "in like less than a minute".
7. Title format, in order: main adjective, product, who it is for, USPs (what the product does), use cases, specifics. Example: "heated jacket for men, USB rechargeable, temperature control for hiking, skiing, and outdoor work, water resistant black".
8. Descriptions: about 2 paragraphs, with "every single keyword" possible, including use cases and needs (examples: winter, hunting, construction, working, bad circulation).
9. Card additions: check each title still reads as coherent customer-facing copy; repeat per surface-area variant so each tier and avatar has its own keyword pool; keep aggressive keyword copy to ad and feed fields, not the storefront. [afd1fd903f18]
[web check: current Merchant Center title and description length limits and rules against keyword stuffing and promotional text] [needs brand data: product attributes that are true for each SKU]

### 3.4 Scaling ladder for the PMax campaign
1. Run 1 lean PMax (3.1) for new brands "until I'm spending like maybe 5 to 10K a day". [568c59a75126]
2. When it "could be more optimized": add asset groups, tweak the tROAS, or layer a standard Shopping campaign beneath it. [568c59a75126]
3. Add a tROAS only after about 3 months and only at a plateau or efficiency drop (3.5). [d4494776c11a]
4. At about $20K to $30K a day, each budget increase returns less. From about $20K to $25K a day, he layers a standard Shopping campaign under the PMax, because "the early signs of this campaign will always be better than just increasing" the existing one. [d4494776c11a] [568c59a75126]
5. Add a branded Search campaign as a small defensive layer (3.6). [a1bbee7012e8]
The source gives 3 different spend triggers (5K to 10K, 20K to 25K, 20K to 30K a day); see section 9. [needs brand data: daily spend and marginal ROAS as budget rises]

### 3.5 Adding a tROAS
1. Leave it blank at launch and for about the first 3 months. [d4494776c11a]
2. Watch for a plateau or a drop in efficiency. [d4494776c11a]
3. When you add it, enter it as a percentage: 300% = $3 revenue per $1 of ad spend. [d4494776c11a]
4. If the campaign is already very profitable, you may never add one. [d4494776c11a]
The source gives no rule for which value to start at or how far to move it per change. [needs brand data: break-even ROAS from margins] [web check: whether PMax now requires or defaults a target]

### 3.6 Branded Search campaign
The source says it is "pretty easy to set up" and does not give the steps. Its only job: when someone types your brand name, you show first instead of a competitor or review site. It brings about 1% of his revenue, and he "rarely" sees it cannibalize PMax. Card additions: confirm brand search volume first; monitor it separately for real incremental value, since you may be paying for clicks you would win organically. [a1bbee7012e8] [needs brand data: brand search volume and organic rank for the brand name]

### 3.7 Weekly review (Sundays)
1. From about $100 total spend, you can already see which products and keywords get the most clicks, which products are not selling, and which keywords waste money. [031ec7c8b2d2]
2. Each Sunday, the only changes he makes: tweak the tROAS, raise the budget, remove keywords, or remove products. [031ec7c8b2d2]
3. Judge on the week-over-week trend, not daily swings. [031ec7c8b2d2]
The card adds "change 1 lever at a time"; the transcript does not say that. The card also warns that pruning too early can remove terms that lack data. The source gives no thresholds for removing a keyword or product.

## 4. Rules, thresholds and numbers

| rule | number or threshold | condition | source's basis | card id |
|---|---|---|---|---|
| Click share by position | 1st 40%, 2nd 20%, 3rd 10%, 4th 7.2% | chart he labels "organic search", applied to ads | on-screen chart, source not named | a792fb2f1bc7 |
| Retrieval to elimination funnel | billions > couple of thousand > about 10 | every search | his description | bf7fb09f077f |
| Elimination cut | 99.99% of retrieved ads | every search | his description | bf7fb09f077f |
| Ad score | bid x pCTR minus beta, range -100 to 100; negative = removed | elimination and ranking | attributed to DOJ disclosure, unverified | bf7fb09f077f |
| Bid examples | 50 cents or $3 per click | illustration | his example | bf7fb09f077f |
| CPC model | intent (3x, 2x, 1x) x relevance multiplier (1x, 2x, 5x); best match $3, worst $15 | auction | illustration only | a0c5917208b0 |
| Title scan time | 200 milliseconds | feed titles and descriptions | his claim | f3d645adbbbe |
| Keyword reach of a long title | about 100 keywords vs 2 | long attribute title | his claim | f3d645adbbbe |
| Duplicates per working product | 5 to 6 | 1 product already working | his accounts | fe7e30671299 |
| Price tiers | standard, budget, discount, premium, luxury | surface area duplicates | his method | fe7e30671299 |
| Slot capture example | 6 of 7 results his stores | some products | anecdote | fe7e30671299 |
| Revenue share from Search and Shopping | 99%, most from Shopping | ecommerce PMax | his accounts | 08b3d9f85868 |
| Revenue from the lean PMax | about 99%; branded Search about 1% | his account structure | his accounts | 568c59a75126, a1bbee7012e8 |
| Learning phase exit | 30 conversions in 30 days (about 1 a day) | new campaign or account | he says this is Google's definition | f7a7231a09f3 |
| Faster exit when aligned | within about the first week | titles, images, price, products aligned | his stores | f7a7231a09f3 |
| Typical launch curve | shaky first days, first order about day 3 (his first store day 2), 2 to 3 orders the next day (his first store 5) | new store | his stores | f7a7231a09f3 |
| No tROAS at start | first about 3 months | new PMax | his habit | d4494776c11a |
| tROAS meaning | 300% = $3 revenue per $1 | when set | definition | d4494776c11a |
| Campaign scaled without tROAS | about $500K ad spend | very profitable campaign | anecdote | d4494776c11a |
| Single PMax until | about $5K to $10K a day | new brands | his habit | 568c59a75126 |
| Plateau point | about $20K to $30K a day | PMax budget increases | his accounts | d4494776c11a |
| Layer standard Shopping | above about $20K to $25K a day | marginal return falling | his accounts | 568c59a75126 |
| Early read of products and keywords | about $100 total spend | new campaign | his habit | 031ec7c8b2d2 |
| Review day | weekly, Sunday | ongoing | his habit | 031ec7c8b2d2 |
| Longevity | 2 to 5 years of steady return | "everything in alignment" | his opinion | 8beaa7445948 |
| Description length | about 2 paragraphs | Shopping feed | his method | afd1fd903f18 |

## 5. Diagnostics and checks

| what to check | how | good | bad | next step | card |
|---|---|---|---|---|---|
| Ads not showing for a relevant query | Compare the query with titles, descriptions, images, price and landing page | Listing clearly matches the query words and price band | Vague title, missing attributes, price outside the query ("under $30") | Rewrite title and description (3.3); add a price-tier listing if the product truly exists at that price | bf7fb09f077f, fe7e30671299 |
| Rank and click share | Impression share and position metrics over time [verify UI] | Share and top positions rise after relevance changes | Flat after changes | Keep working titles and images; the source offers no further fix | a792fb2f1bc7 |
| High CPC | Compare CPC by product and query | Most relevant products get the cheaper clicks | Broad or loosely matched queries at high CPC | Per the CPC model, you are the low-relevance advertiser; tighten relevance or stop bidding there | a0c5917208b0 |
| Experience penalty (beta) risk | Landing page speed, shipping reliability, store look | Fast pages, orders shipped, clean store | Slow pages, late or missing orders | Fix speed and fulfilment; the source says beta falls with good experience over time | 8beaa7445948, 4657c93cde0f [needs brand data: page speed on ad landing pages, on-time delivery rate] |
| Feed and landing page match per variant | For each duplicate, check price, images and copy match its target buyer | Budget variant shows budget price clearly; imagery fits the avatar | Ad promises one thing, page shows another | Align PDP copy with feed copy; fix top-traffic listings first (card addition) | 4657c93cde0f |
| Stuck in learning | Conversions per day since launch | 1 or more a day; exit in about a week | Weeks with few conversions | Audit alignment of titles, images, price, products before raising budget | f7a7231a09f3 |
| Wrong placements | Channel or placement report [verify UI] | Spend on Search and Shopping only | Spend on YouTube, Gmail, Display, Maps, Discover | Re-check 3.1 steps 9 and 10 | 08b3d9f85868 |
| Location setting | Campaign location options [verify UI] | Presence | Presence or interest | Switch to presence | 08b3d9f85868 |
| Device setting | Device settings [verify UI] | TV screens off | TV screens on | Turn off | 08b3d9f85868 |
| Plateau | Marginal return as budget rises | Return holds as budget rises | Each increase returns less | Add tROAS, asset groups, or layer standard Shopping (3.4) | d4494776c11a, 568c59a75126 |
| Wasted keywords and dead products | Weekly report of clicks by product and search term [verify UI] | Clicks convert | Clicks with no sales | Remove the keyword or product on Sunday review | 031ec7c8b2d2 |
| Brand term leakage | Search your brand name | You show first | Competitor or review site first | Add branded Search campaign | a1bbee7012e8 |

The source gives no numeric kill thresholds for keywords or products, no CPC or CTR benchmarks, and no way to test whether duplicates cannibalize each other.

## 6. Tools, settings and named features

- **Google Ads campaign creation: "Create a campaign without guidance"** [verify UI]. Starting point for the lean PMax. [08b3d9f85868]
- **Performance Max (PMax).** Google's AI campaign type. Default channels named: Search, Shopping, YouTube, Gmail, Display, Google Maps, Discover. Goal set to Purchases. [08b3d9f85868] [web check: current PMax channel list and naming, since Discover has been renamed in some Google products]
- **Text, image and video enhancement toggles** in the PMax asset step. He turns all off to stop expansion to non-Shopping placements [verify UI]. [08b3d9f85868]
- **Ad strength.** Ignore it; "poor" in all his campaigns. [08b3d9f85868]
- **Location options: presence vs presence or interest** [verify UI]. Use presence. [08b3d9f85868]
- **Devices: TV screens** [verify UI]. Turn off. [08b3d9f85868]
- **Google Merchant Center (GMC).** The product feed; source of titles, descriptions, images, prices. [08b3d9f85868] [f3d645adbbbe]
- **Standard Shopping campaign.** Manual CPC control, "not going to be AI". Layered under PMax at scale. [568c59a75126] [d4494776c11a]
- **Branded Search campaign.** Defends the brand name. [a1bbee7012e8]
- **Target ROAS (tROAS).** Entered as a percentage; 300% = 3x. He notes Meta and TikTok do not have an equivalent "target" of this kind; that claim is his `[web check: Meta has a ROAS goal bid strategy]`. [d4494776c11a]
- **Asset groups.** Added later to optimize a scaled PMax; no detail given. [568c59a75126]
- **Keyword Planner.** Free, inside Google Ads; enter term, set country, get results, download [verify UI]. [afd1fd903f18]
- **Claude (or any AI writing tool).** Bulk titles from keyword list plus format. [afd1fd903f18]
- **My Ad Center (myadcenter.google.com > manage privacy).** Shows what Google infers about a user; he uses it to explain pCTR [verify UI]. [bf7fb09f077f]
- **Impression share and position reports.** Card addition for tracking rank [verify UI]. [a792fb2f1bc7]

## 7. Examples and case results

All are the presenter's own anecdotes, not promises.
- First store, started about mid-April: first month about $3.5K revenue at about 40% margin, about $1.5K profit. 3 months later: a $50K month with $20K profit. Q4 (3 months after that): $270K revenue with $56K profit. He says the store stayed above 3x ROAS its whole life. He credits depth on 1 avatar, 1 pain point, 1 use case, multiplied across the store. (Arithmetic note: 40% of $3.5K is $1.4K, not $1.5K; $56K on $270K is about 21% margin, lower than the earlier 40%.) [not carded directly; related: 8beaa7445948]
- First store: first order 2 days in, 5 orders the next day. [f7a7231a09f3]
- 1 campaign scaled to about $500K ad spend with no tROAS. [d4494776c11a]
- Some products where his stores hold 6 of 7 results. [fe7e30671299]
- Started with $200 of Google spend. Claims to outcompete IKEA, AliExpress, Amazon and Home Depot on relevance.
- Illustrations (not results): Asana search shows monday.com first; "outdoor lighting" Shopping; "orthopedic shoes" retrieval and CPC grid; $30 t-shirt price tiers with "best shirts under $30" and "under $100"; "black jacket" white-background images vs leisure, active and corporate avatar images; heated jacket title. [a792fb2f1bc7] [a0c5917208b0] [fe7e30671299] [2dd030a32711] [f3d645adbbbe]

## 8. Mistakes the source warns about

1. Believing Google is random, needs "a million different campaign types", a big bank balance or a known brand. [bf7fb09f077f]
2. Focusing on "quality score" instead of the ad score formula. [bf7fb09f077f]
3. Running many segmented campaigns by niche or product line. [e5ab20feaa14]
4. Launching PMax with default channels (Gmail, Display, YouTube, Maps, Discover) and filled-in assets. [08b3d9f85868]
5. Leaving location on presence or interest. [08b3d9f85868]
6. Leaving TV screens on. [08b3d9f85868]
7. Chasing ad strength. [08b3d9f85868]
8. Setting a tROAS too early; he says this "just kills their entire campaign". [d4494776c11a]
9. Only raising budget on a winner instead of duplicating it across tiers and avatars. [fe7e30671299]
10. White-background-only product images like every competitor. [2dd030a32711]
11. Short titles such as "heated jacket" that compete for about 2 keywords. [f3d645adbbbe]
12. Writing titles and descriptions for the customer and not the algorithm (his view; the card disagrees). [f3d645adbbbe]
13. Misaligned titles, images, price and products, which keep you in learning "forever". [f7a7231a09f3]
14. Scaling budget on the same PMax past the plateau instead of layering standard Shopping. [d4494776c11a] [568c59a75126]
15. A slow landing page or unreliable shipping, which raises beta. [8beaa7445948]
16. Judging Google like social platforms' up-and-down swings rather than week-over-week trend. [031ec7c8b2d2]

## 9. Caveats, conflicts and what is missing

- **Keyword stuffing conflicts with Google's feed rules and with the card.** Source 07 says to "stuff" keywords into titles and descriptions and write "for the algorithm". Card f3d645adbbbe rewrites this as "keep the result readable rather than stuffing every keyword" and "more words do not guarantee eligibility for more searches"; card afd1fd903f18 says stuffed copy can look spammy. Common ecommerce advice and Merchant Center guidance favour accurate, readable titles with key attributes first. Follow the card version; do not follow the stuffing instruction as written. [web check: current Merchant Center title limit and keyword stuffing policy]
- **Duplicating the same product at different prices is a policy and trust risk.** The source never says whether the budget, discount, premium and luxury versions are different products or the same item relisted. If they are the same item, this risks Merchant Center duplicate-product, price-accuracy or misrepresentation problems, and shoppers comparing prices. Card f3d645adbbbe says "do not create duplicate listings merely to repeat keywords". The tactic reads like a multi-store dropshipping play; it may not suit a brand with fixed pricing. [web check: Merchant Center duplicate and misrepresentation policies] [needs brand data: whether real tiered variants exist, pricing policy]
- **Card errors to watch.** Card fe7e30671299 says "the source reports seeing little cannibalization between variants"; the transcript says little cannibalization between PMax and branded Search, not between variants. Card 031ec7c8b2d2 says the source changes "only one" lever per week; the transcript lists 4 levers and does not say 1 at a time. Card 2dd030a32711 says "2 to 4 variant images"; the source shows 3.
- **The click-share chart is for organic search.** He reads it as "40% of all the clicks to an organic search" and then says position 1 gets "40% of all the money". Paid click shares differ. The 4 values sum to 77.2%. [web check: current paid Search and Shopping click share by position]
- **The ad score formula is unverified.** He attributes it to the DOJ but shows no document. The -100 to 100 scale and the "negative = eliminated" rule are his. He says it is "not quality score", which conflicts with Google's public Ad Rank docs that name quality factors. [web check: DOJ trial exhibits and Google Ad Rank documentation]
- **The CPC model is an illustration.** Google's public docs describe actual CPC in terms of Ad Rank and the next competitor, not intent x relevance multipliers. The 1x to 5x numbers are made up for teaching. [web check: Google actual CPC documentation]
- **The learning-phase number is his.** "30 conversions in 30 days" is presented as Google's definition. Other practitioners and Google describe learning differently (by time or conversion cycles). Do not plan launch budgets from this number alone. [web check: current Google learning period definition]
- **Spend triggers are inconsistent.** He says 1 PMax until about $5K to $10K a day, then says the plateau comes at $20K to $30K a day, then says he layers standard Shopping above $20K to $25K. Most brands never reach these levels; the source gives no trigger for small accounts other than "plateau or efficiency drop". [needs brand data: daily spend, marginal ROAS curve]
- **Feed-only PMax placement control is not proven.** He says leaving assets blank and turning off enhancements keeps PMax off YouTube, Gmail and Display. He offers no placement report. [web check: whether feed-only PMax still serves dynamic remarketing on Display or YouTube, and whether channel exclusions now exist]
- **Consolidation vs segmentation.** The card calls single-campaign consolidation his opinion and says margin or region differences can need segments. Many practitioners segment Shopping by margin or product performance. Keep SKU-level reporting either way. [e5ab20feaa14] [568c59a75126]
- **Branded Search incrementality.** He sees "rarely" any cannibalization; the card warns you may pay for conversions you would get organically. The source gives no test. [a1bbee7012e8]
- **Image-to-audience claim.** "If your images have college students in them, Google's going to ... show them to more college students" is his interpretation, not documented. [2dd030a32711]
- **Beta and trust over time.** Store-age trust and "keep building more stores" are his framing. The card turns it into "keep the same store running rather than starting fresh accounts"; the transcript says both that trust grows with store age and that he builds more stores. [8beaa7445948]
- **Missing how:** no budget at launch, no tROAS starting value, no keyword or product removal thresholds, no branded Search setup, no asset group guidance, no conversion tracking setup, no measurement of incrementality, no Merchant Center policy guidance, no advice for non-US markets beyond "set your target country".
- **Brand fit.** This is a single-operator, multi-store, US-dollar playbook. Price-tier duplicates, avatar image sets and aggressive titles need a brand-level decision before use. [needs brand data: brand pricing rules, product photo rules, market and currency]

## 10. Card index

- bf7fb09f077f: The four-step Google Ads pipeline: retrieval, elimination, ranking, auction
- fe7e30671299: Surface area scaling: duplicate products across pricing tiers to own the search page
- 2dd030a32711: Differentiate duplicate listings with image angles matched to customer avatars
- f3d645adbbbe: Write relevant, readable Shopping feed titles from product attributes
- 08b3d9f85868: Set up a lean Performance Max campaign limited to Search and Shopping
- d4494776c11a: Don't set a tROAS target before the account has conversion history
- e5ab20feaa14: Consolidate campaigns instead of segmenting by product line
- f7a7231a09f3: Work the learning phase: 30 conversions in 30 days is the baseline, not a cap
- 031ec7c8b2d2: Weekly optimisation cadence: tROAS, budget, negative keywords, product pruning
- a0c5917208b0: Use Google's intent-by-relevance CPC model to gauge paid search economics
- a1bbee7012e8: Add a branded search campaign to defend your brand term cheaply
- 8beaa7445948: Treat beta (experience penalty) as the long-term ranking lever
- afd1fd903f18: Build a broad keyword pool with Keyword Planner before writing feed copy
- 568c59a75126: Prefer PVMs consolidations before adding new campaign types (title typo for PMax)
- 4657c93cde0f: Interview alignment: relevance across feed, landing page and price point
- a792fb2f1bc7: Aim for high page position and read the clicks-per-position trade-off
