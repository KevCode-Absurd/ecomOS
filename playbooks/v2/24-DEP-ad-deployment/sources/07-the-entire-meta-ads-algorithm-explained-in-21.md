# The entire Meta ads algorithm explained in 21 mins

source_id: 1LPa_LlZLtLsNdfeCslfnxz_FBPhWcZR4  |  folder: /24-DEP-ad-deployment (moved from /11-ADC)  |  cards: 13  |  words: 5262  |  type: transcript (YouTube talk, single presenter)
credibility: Presenter "Mark", an ecommerce media buyer who runs Meta ad accounts. He sells a free AI-ads masterclass (plugged mid-video) and says "damn near 100%" of his accounts run some form of AI ads. Evidence is his own accounts ("multiple five figures per day", has seen 6 figures per day), talks with "high skill advertisers", 1 on-screen screenshot (profitable account with a 0 opportunity score, EMQ 9.8 to 9.9) and a Meta document on the auction that he says Meta later withdrew. No controlled tests, no numbers on results. Tone is opinionated and profane. Treat most rules as "Source 07 says".
date signals: Names the Andromeda update and a flood of AI creative, so 2025 or later. Masterclass plug says "this Thursday, May 14th, 7:00 p.m. Eastern"; May 14 is a Thursday in 2026, so likely recorded May 2026 `[web check: video publish date]`. Refers to iOS 14 (launched 2020, in effect early 2021). Names Advantage+ campaigns, lowest cost, cost cap, bid cap, target ROAS, maximum value, EMQ, opportunity score, Conversions API, Triple Whale, Hyros. All platform names and settings can change.
scope note: The source header places the 4-step auction, the Total Value formula, broad vs manual targeting, Andromeda and creative diversity, and bidding choice in this folder. It routes creative hooks, formats and fatigue to 10-MCR, and pixel, CAPI, EMQ and incrementality to 06-MEA. It says to skip learning-phase venting, iOS and EMQ commentary, ban-wave earnings theories and webinar plugs. Those parts are still recorded below (sections 2.13 to 2.18) so nothing is lost, but the folder merge should route EMQ and CAPI detail to 06-MEA and treat the ban-wave theory as opinion only.

## 1. What this source is for

It gives an operator a mental model of how Meta picks which ad to show: 4 filter stages in about 200 ms, and a Total Value equation that decides the winner. From that model it derives a small set of operating rules: run broad and let creative do the targeting, keep testing variations inside each new concept, pick a bid strategy by business constraint, judge on 7-day or longer windows, trust outside attribution over Meta's reported conversions, and question Meta's own suggestions and scores. It is strong on "why" and weak on "how": few settings, no test sizes, no kill rules.

## 2. Principles

### 2.1 Meta serves ads through 4 stages in about 200 ms
Every time a user scrolls to an ad slot, Meta runs, in order: 1) retrieval, 2) light ranking, 3) heavy ranking, 4) auction. The presenter says tens of millions of ads compete for 1 impression and the whole process takes about 200 ms. Condition: this is the presenter's simplified version of Meta's process; the stage counts are his illustration, not a published benchmark (card caveat). [4844059375a6]

### 2.2 Retrieval is where "creative is targeting" happens
Retrieval is the most data-heavy stage. Meta checks whether the ad is "even remotely relevant" to the user ("in the right ballpark") and reads the creative to decide who to show it to. Signals the source names: hook, format, the demographic of people shown in the ad, copy, video script, thumbnail, and the landing page. Example: an ad featuring a 55-year-old woman skews delivery toward women and toward older women, "all taken into context with what the creative is actually saying". The presenter says the list is not complete and that he is simplifying. Card inference: if the creative's signals point to a small audience, retrieval can limit delivery regardless of budget. [4844059375a6] [32581af3f424]

### 2.3 Andromeda changed retrieval sorting and shifted targeting weight to creative
Andromeda was an update to the sorting process in the retrieval step. The presenter believes a main driver was the flood of AI-generated creative, which made the old sorting model less effective; he says it was "not the only reason". Result per the source: Meta now "mostly" looks at creative to decide targeting, not at ad set settings. He links this to a decline in audiences (interest, lookalike, custom) that can hold high budgets profitably. Condition: Andromeda's internals are not public; this is his inference. `[web check: Meta's own description of Andromeda]` [6ee9db26f236] [32581af3f424]

### 2.4 Run broad by default; manual audiences are a small sandbox
The presenter "rarely" uses interest audiences, and when he does he caps their budget. The same goes for lookalikes and custom audiences. For retargeting he sets no custom audiences and runs "completely broad", at most with 1 exclusion of purchasers. He says most high-skill advertisers he talks to do "something relatively similar". The "new way" is broad targeting and Advantage+ campaigns, "within reason". Condition: his own pattern plus hearsay from peers, not a test. Manual audiences can remain "a little experimentation sandbox". [32581af3f424] [a55d9b19503c]

### 2.5 Give Meta control "within reason", and do not blindly accept its suggestions
The algorithm is good, but many of Meta's in-platform suggestions are "horrible pieces of advice" that drain budget. Reason given: Meta is a for-profit company and the advertiser is its paying customer. Named example: ad-level suggestions that promise to lower cost per result by 11%, after which the presenter says accounts "went to [bad]". Card addition: require evidence from your own account before applying a suggestion, and do not refuse everything, test instead. [d9cba85df27b] [32581af3f424] [94fa98ec33c1]

### 2.6 Light ranking only cuts volume; heavy ranking is where your real competitors are
Light ranking cuts millions of ads to thousands (roughly 5,000 in his visual). He says it "barely deserves a description". Heavy ranking cuts thousands to "a couple hundred", "sometimes even less". Only at heavy ranking are competitors worth thinking about: you have "a handful" of real rivals, not tens of millions. His framing numbers: about 10 million advertisers on Facebook in total, and far fewer once you narrow to ecommerce. Note: card 4844059375a6 says "Meta says roughly 10 million"; the transcript states it as the presenter's own figure, not as a Meta quote. `[web check: current Meta advertiser count]` [4844059375a6]

### 2.7 The Total Value equation decides who wins
At heavy ranking, Meta gives every ad a value for the impression. Higher value wins. The lower-value ad loses that impression and is "served a lower quality impression" instead. The formula the presenter shows:

Total Value = (Advertiser Bid x Estimated Action Rate) + User Value (consumer value and experience)

For a conversion-optimized ad: Estimated Action Rate = Estimated Click-Through Rate x Estimated Click-to-Conversion Rate.

He says the formula came from Meta documentation that Meta later withdrew from Facebook, though a copy is "still on their website". Condition: treat the exact form as his reconstruction; estimated action rate is Meta's internal prediction, not a number you can read. `[web check: Meta Business Help Center "ad auction" page for the current published formula and whether the third term is called ad quality or user value]` [3ad804612663] [4844059375a6]

### 2.8 Read "estimated CTR" as all soft metrics, and "click-to-conversion" as funnel monetization
The presenter's reading, not Meta's: estimated CTR is "a culmination of all your soft metrics": CTR, CPC, CPM, hook rate, hold rate, cost per 3-second video view, and anything else tied to getting someone engaged and clicking. Click-to-conversion is "your conversion rate": of all clicks, how many purchased (ecommerce) or booked a call or applied (info or lead-gen). Meta treats these conversion types "largely the same" in this equation. Why CTR matters: Meta "historically loves" high CTR ads because CTR is "the most pure indication" of relevance. Over time and with more spend, Meta rewards high CTR with lower cost to advertise, lower CPMs and "ideally higher quality traffic". Card inference: bid is 1 lever; action rate is 2 levers (CTR and conversion rate) in the same product, so creative and funnel work raise your effective bid without raising the bid. [3ad804612663] [a55d9b19503c]

### 2.9 The user-value term protects Meta from aggressive advertisers
The last term exists so aggressive advertisers cannot ruin the user experience. Without it, the presenter says, scammers would flood the platform and it would be "like 50/50 instead of 80/20, which is roughly what it is right now" (his rough estimate, not data). Rule: "don't [mess] up the user experience". Card inference: creative that wins clicks by misleading people works against this term and can cost delivery over time. [3ad804612663] [a55d9b19503c]

### 2.10 The auction: highest total value wins, and bid strategy should fit your constraint
The auction is all remaining advertisers competing for 1 impression; the highest bid "with all the context of that equation" wins. Bid options named: lowest cost (auto bidding, Meta bids to get conversions at the lowest cost), manual bidding via cost caps (cap on the maximum you will pay to acquire a customer) and bid caps (the maximum you will bid to acquire a customer), plus other options Meta keeps releasing such as maximum value and target ROAS. He has run accounts spending "multiple five figures per day" and seen accounts at 6 figures per day, all on lowest cost and profitable; other advertisers run only bid caps. Rule: "choose what is actually going to solve the constraint in your business". [1ff82eb90f46] [b0bdf29a1f32]

### 2.11 Think like an entrepreneur, not a media buyer, about scale
People ask how to go from $1K per day to $10K per day by media buying alone. The presenter says "there's a little bit you can do" and media buying is not dead, but scaling is a business problem, not a bidding trick. He gives no specific non-media levers in this source. [1ff82eb90f46] [b0bdf29a1f32]

### 2.12 Creative diversity after Andromeda: keep testing variations
A post-Andromeda narrative says you should launch more net-new concepts and fewer variations. The presenter says that is too simple and that variations are "still highly, highly effective". His structure: 1 ad set = 1 net-new concept; ad 1 is the concept and ads 2, 3 and 4 are variations of it (example: 1 concept with 3 different hooks). Reason: more "at-bats" at the concept level. His case: a variation turned out to be the winner and the original concept the loser; if you skip variations you would wrongly call the concept a loser. Separate point: a variation of your account's current top ad "will do decent" but "typically" will not beat the top ad (his experience). Variations here are of a new concept, not of the winner. [6ee9db26f236]

### 2.13 Ads never stop learning
Meta describes a learning phase that ads, ad sets and campaigns (especially ads) go through to gather conversions before results become more stable. The presenter says: "Your ads are always learning." There is no point where they are "good forever"; "everything dies at some point". Early results are more volatile; sometimes they settle, sometimes not. "Sometimes the solution is literally just to make better ads." Do not obsess over exiting learning. `[web check: Meta's current learning phase definition and exit criteria]` [c8f9d9634c5f]

### 2.14 Daily volatility is normal, especially under about $1,000 per day
At $50 per day, a few hundred per day, "even up to like $1,000 per day", results that look "like a sine wave" are "100% normal". He also sees inconsistency well above $1K per day. Example he mocks: someone at 3x ROAS then unprofitable, spending $100. Rule: "when in doubt, zoom out": look at 7 days and at the largest spend window you have before deciding. If you want consistent results, he says, Google is more stable (his opinion). [c8f9d9634c5f]

### 2.15 Send Meta good data, but do not expect EMQ to predict profit (route detail to 06-MEA)
Meta performance often depends on the data you send back so it can learn your customers and, hopefully, lower cost over time. Use the Conversions API (server side, not only browser) to improve data and EMQ. EMQ sits on the purchase event in Events Manager on a 1 to 10 scale. The presenter calls EMQ "overrated": he has had EMQ of 9.8 to 9.9 without seeing a direct link to results. Summary rule: "send Facebook good data, and also take all the conversion data with a grain of salt". [40de3bd68e44] [773fc35a99e9]

### 2.16 Do not steer on Meta-reported CPA (route detail to 06-MEA)
Since iOS 14 (launched 2020, in effect about early 2021) users can opt out of tracking, so Meta's post-click conversion data is "really inaccurate". The presenter does not look at CPA inside Facebook "at all". He uses third-party attribution tools such as Triple Whale or Hyros, and says you could build ("vibe code") your own in a few hours. [40de3bd68e44] [94fa98ec33c1]

### 2.17 Meta's scores and guidance are not neutral: question everything
Meta is a for-profit, public company that serves its largest advertisers best and treats small advertisers, who cause "99% of their headaches", less well. Evidence shown: a profitable account with an opportunity score of 0. Rule: do not act on something because Meta's docs, CEO, CMO or head of advertising say so; "think for yourself". [94fa98ec33c1] [d9cba85df27b]

### 2.18 Rejections and ban waves (presenter's theory, not verified)
He says Meta tightens or relaxes enforcement around its earnings reports, which produces ban waves (ad accounts, business managers, pages, profiles) that ease "a month later". He uses this to explain why identical creative is approved for one advertiser and rejected for another. He says he cannot go into specifics. Card addition, not in the source: plan redundancy across ad accounts, pages and business managers. The card itself says this is not a compliance or evasion strategy. The source header says to skip this theory. Treat it as opinion only. [6dbefe2b17df] [94fa98ec33c1]

## 3. Procedures

The source gives few step-by-step procedures. These are the sequences it states or that its cards spell out. Card-only steps are marked.

### 3.1 Diagnose a new ad or ad set that will not spend, using the 4 stages
1. Map the ad to the 4 stages: retrieval, light ranking, heavy ranking, auction. [4844059375a6]
2. Retrieval check: list what the creative signals about its audience (people shown and their age and gender, hook, format, copy, script, thumbnail, landing page). If the signals point to a narrow audience, delivery can be limited regardless of budget (card inference). [4844059375a6] [32581af3f424]
3. Heavy ranking check: estimate the 2 halves of estimated action rate from your data. First half: CTR and soft metrics (CPC, CPM, hook rate, hold rate, cost per 3-second view). Second half: click-to-purchase rate. `[needs brand data: ad-level CTR, CPM, hook rate, hold rate, click-to-purchase rate]` [3ad804612663]
4. Decide the lever: raise bid (1 input) or fix creative and funnel (2 inputs in the same equation). Card suggests fixing action rate first. [3ad804612663]
5. User value check: is the ad winning clicks by misleading people? If so, expect it to lose delivery over time. [3ad804612663] [a55d9b19503c]
6. Note that a losing ad tends to show up first as weaker, costlier impressions, not zero delivery (card reading of the source's "lower quality impression"). [4844059375a6]

### 3.2 Set up targeting for an ecommerce account (source's default)
1. Use broad targeting and Advantage+ campaigns as the default. `[verify UI]` [32581af3f424]
2. Retargeting: no custom audiences; broad, with at most 1 exclusion of purchasers. `[verify UI]` [32581af3f424]
3. If you test interest, lookalike or custom audiences, keep them as a small sandbox with capped budgets. The source gives no cap amount. `[needs brand data: daily budget to set the cap]` [32581af3f424] [a55d9b19503c]
4. Put the time saved into creative volume and variety (card addition). [32581af3f424]

### 3.3 Build a test ad set for a new concept
1. 1 ad set = 1 net-new concept. [6ee9db26f236]
2. Ad 1 = the concept. Ads 2, 3 and 4 = variations of that concept (example: same concept, 3 different hooks). [6ee9db26f236]
3. Do not judge the concept on ad 1 alone. If ad 1 loses but a variation wins, the concept is alive. [6ee9db26f236]
4. When iterating on the account's top ad, expect variations to do "decent" but usually not beat it. [6ee9db26f236]
The source gives no budget, run time, or win and kill thresholds for these tests.

### 3.4 Choose a bid strategy
1. Name the business constraint first. Card framing: volume (need more spend), CPA protection (need a ceiling), or return at scale (need a ROAS goal). [b0bdf29a1f32]
2. Match the method (the mapping is a card addition; the source only says "solve the constraint"): lowest cost for volume at efficiency; cost cap for a ceiling on cost to acquire a customer; bid cap for a ceiling on the bid; target ROAS or maximum value where the goal is return-based. `[verify UI]` [1ff82eb90f46] [b0bdf29a1f32]
3. Do not switch to caps because they are trendy or because other accounts use them. Lowest cost can run profitably at 5 to 6 figures per day per the source. [1ff82eb90f46]
4. Revisit when the constraint changes, for example moving a proven campaign from test budget to growth budget (card addition). [b0bdf29a1f32]

### 3.5 Decide whether to act on volatile results
1. Check daily spend level. Under about $1,000 per day, expect sine-wave daily results. `[needs brand data: daily Meta spend]` [c8f9d9634c5f]
2. Do not act on 1 good or bad day. Pull at least 7 days, and the largest spend window you have. [c8f9d9634c5f]
3. Judge on outside attribution, not Meta CPA (3.7). [40de3bd68e44]
4. If results are still poor over that window, make better ads rather than chasing learning-phase fixes. [c8f9d9634c5f]
The source gives no ROAS or CPA threshold for "poor".

### 3.6 Review a Meta suggestion before applying it
1. Read the claimed benefit (example: "lower your cost per result by 11%"). `[verify UI]` [d9cba85df27b]
2. Do not accept the projection as evidence. Ask what your own account data says. [d9cba85df27b]
3. Card addition: if you test it, log the suggestion type and what happened after, so you build your own record of which ones help. [d9cba85df27b]

### 3.7 Tracking hygiene check (belongs to 06-MEA; kept here for completeness)
1. Confirm a Conversions API (server-side) setup runs alongside the browser pixel. `[verify UI]` [773fc35a99e9]
2. In Events Manager, open the purchase event and read EMQ (1 to 10). Use it as a plumbing check, not a profit forecast. `[verify UI]` `[needs brand data: current purchase EMQ]` [40de3bd68e44] [773fc35a99e9]
3. Judge performance with a third-party attribution tool (Triple Whale, Hyros, or a custom build). `[needs brand data: which attribution source the brand uses]` [40de3bd68e44]

### 3.8 Pre-launch 3-point check (the source's 3 takeaways; checklist use is a card addition)
1. Targeting: is the ad set broad, with creative defining the audience? [a55d9b19503c]
2. Creative: will it stop the scroll and earn high CTR and soft metrics? The presenter calls this "half the battle". [a55d9b19503c]
3. User experience: does it avoid misleading or annoying users? [a55d9b19503c]

## 4. Rules, thresholds and numbers

| rule | number or threshold | condition | source's basis | card id |
|---|---|---|---|---|
| Time Meta takes to pick an ad | about 200 ms | every impression | presenter's simplification | 4844059375a6 |
| Ads competing at retrieval | tens of millions | per impression | presenter's illustration | 4844059375a6 |
| After light ranking | thousands (roughly 5,000 in his visual) | illustration | presenter's visual | 4844059375a6 |
| After heavy ranking | a couple hundred, sometimes fewer | illustration | presenter | 4844059375a6 |
| Advertisers on Facebook | about 10 million total | framing only; far fewer in ecommerce | presenter's figure `[web check: current count]` | 4844059375a6 |
| Total Value | (bid x estimated action rate) + user value | heavy ranking and auction | withdrawn Meta doc as reconstructed by presenter `[web check]` | 3ad804612663 |
| Estimated action rate | estimated CTR x estimated click-to-conversion rate | conversion-optimized ads | same | 3ad804612663 |
| Share of conversion campaigns | "99%" of viewers | rhetorical | presenter | none |
| Scammer ratio | "80/20" now, would be "50/50" without user-value term | rhetorical | presenter's guess | 3ad804612663 |
| Retargeting exclusions | at most 1 (purchasers) | retargeting run broad | presenter's practice | 32581af3f424 |
| Interest audiences | rarely; budget capped if used | sandbox only | presenter's practice; no cap amount given | 32581af3f424 |
| Ads per concept ad set | 1 concept + 3 variations (ads 1 to 4) | new-concept testing | presenter's structure | 6ee9db26f236 |
| Lowest cost at scale | profitable at multiple 5 figures per day; seen at 6 figures per day | examples, not promises | presenter's accounts | 1ff82eb90f46 |
| Scale question he rejects as pure media buying | $1K to $10K per day | framing | presenter | 1ff82eb90f46 |
| Daily volatility is normal | up to about $1,000 per day (examples: $50, a few hundred) | also happens above $1K | presenter's rule of thumb | c8f9d9634c5f |
| Minimum decision window | 7 days, and the largest spend window available | before acting on results | presenter | c8f9d9634c5f |
| Low-spend example | 3x ROAS then unprofitable at $100 spend | example of noise | presenter | c8f9d9634c5f |
| EMQ scale | 1 to 10, on the purchase event | Events Manager | presenter `[verify UI]` | 40de3bd68e44 |
| High EMQ without profit link | 9.8 to 9.9 | presenter's own account | presenter's counterexample | 40de3bd68e44 |
| Opportunity score on a profitable account | 0 | presenter's screenshot | 1 account | 94fa98ec33c1 |
| Meta suggestion example | "lower cost per result by 11%" | ad-level suggestions | presenter's warning | d9cba85df27b |
| iOS 14 | launched 2020, in effect about early 2021 | tracking opt-out | presenter | 40de3bd68e44 |
| Ban waves easing | about "a month later" | presenter's earnings theory | unverified opinion | 6dbefe2b17df |

## 5. Diagnostics and checks

| check | how | good | bad | next step | card |
|---|---|---|---|---|---|
| Is creative defining the audience? | Review who appears in the ad, hook, copy, script, thumbnail, landing page | Signals match the buyer you want | Signals point to a different or tiny audience | Change casting, script or page to match the buyer; do not fix with ad set targeting | 32581af3f424 |
| Is the ad set over-constrained? | Look at targeting: interests, lookalikes, custom audiences | Broad or Advantage+, 1 purchaser exclusion at most on retargeting | Stacked interests or lookalikes carrying main budget | Move main budget to broad; keep audiences as capped sandbox `[verify UI]` | 32581af3f424 |
| First half of estimated action rate | CTR, CPC, CPM, hook rate, hold rate, cost per 3-second view | Improving over time with lower CPMs | Weak soft metrics | Improve creative (hooks are in 10-MCR) `[needs brand data: account baselines]` | 3ad804612663 |
| Second half of estimated action rate | Click-to-purchase rate | Holds or rises | Clicks but few purchases | Fix page, offer or checkout (card suggestion) | 3ad804612663 |
| User value | Does the ad mislead or annoy? | Clear, honest ad | Clickbait that wins clicks | Rewrite; expect delivery loss otherwise | 3ad804612663 |
| Concept wrongly killed? | Did the concept get 3 variations? | 4 ads per concept | 1 ad per concept, judged as loser | Relaunch with variations | 6ee9db26f236 |
| Reacting to noise? | Check spend level and window length | 7+ day window, largest spend window | Decision on 1 day, or on about $100 spend | Zoom out; wait for more data | c8f9d9634c5f |
| Which numbers are you steering on? | Identify source of CPA or ROAS | Third-party attribution | Meta-reported CPA only | Use outside attribution; read Meta numbers with caution | 40de3bd68e44 |
| Is data flowing to Meta? | CAPI present; purchase EMQ in Events Manager | Server-side events present | Browser-only | Set up CAPI (06-MEA) `[verify UI]` | 773fc35a99e9 |
| Is a Meta suggestion proven? | Compare claim with own data | Own evidence supports it | Only Meta's projected uplift | Do not apply, or test and log result | d9cba85df27b |
| Is the bid strategy chosen for a reason? | Write the constraint next to each campaign | Method matches constraint | Cap chosen because it is popular | Re-pick by constraint | b0bdf29a1f32 |

## 6. Tools, settings and named features

| tool or feature | use in the source | tag |
|---|---|---|
| Retrieval, light ranking, heavy ranking, auction | Meta's 4 ad-serving stages | `[web check: Meta's current description]` |
| Andromeda | Update to retrieval sorting; more weight on creative for targeting | `[web check]` |
| Advantage+ campaigns | The "new way": broad, Meta-controlled, "within reason" | `[verify UI]` |
| Broad targeting | Default for prospecting and retargeting | `[verify UI]` |
| Interest, lookalike, custom audiences | Rarely used; capped sandbox | `[verify UI]` |
| Purchaser exclusion | The 1 exclusion he allows on retargeting | `[verify UI]` |
| Lowest cost (auto bidding) | Default for many accounts, profitable at high spend | `[verify UI]` |
| Cost cap | Cap on max cost to acquire a customer | `[verify UI]` |
| Bid cap | Cap on max bid to acquire a customer | `[verify UI]` |
| Target ROAS, maximum value | Other options Meta releases | `[verify UI]` |
| Learning phase | Meta's concept; presenter says ads always learn | `[web check: current exit criteria]` |
| Events Manager, purchase event, EMQ (1 to 10) | Data quality check, "overrated" | `[verify UI]` |
| Conversions API | Server-side event sending | `[verify UI]` (setup in 06-MEA) |
| Opportunity score | Meta score; 0 on a profitable account | `[verify UI]` |
| Meta ad-level suggestions | Often harmful per presenter | `[verify UI]` |
| Triple Whale, Hyros, custom tool | Third-party attribution | `[web check: current tools and pricing]` |

## 7. Examples and case results

All are the presenter's anecdotes, not promises.
- An ad featuring a 55-year-old woman skews delivery toward older women. [32581af3f424]
- Accounts at multiple 5 figures per day, and some at 6 figures per day, run profitably on lowest cost only; others run only bid caps. [1ff82eb90f46]
- A concept ad set where a hook variation won and the original concept lost. No numbers given. [6ee9db26f236]
- Someone at 3x ROAS who became unprofitable, spending $100: used as an example of low-spend noise. [c8f9d9634c5f]
- EMQ of 9.8 to 9.9 with no visible link to profit. [40de3bd68e44]
- An "incredibly profitable" account showing an opportunity score of 0. [94fa98ec33c1]
- Meta suggestions promising 11% lower cost per result, followed by poor results. [d9cba85df27b]
- Identical creative approved for one advertiser and rejected for another. [6dbefe2b17df]

## 8. Mistakes the source warns about

1. Believing Meta ads are random, or that good creative alone makes everything else work. The science (the equation) matters too.
2. Spending effort on interest, lookalike and custom audience structures instead of creative. [32581af3f424]
3. Giving Meta full control and accepting its suggestions blindly. [d9cba85df27b]
4. Believing "variations are dead after Andromeda; only launch net-new concepts". [6ee9db26f236]
5. Calling a concept a loser after testing it without variations. [6ee9db26f236]
6. Expecting a variation of your top ad to beat it. [6ee9db26f236]
7. Obsessing over cost caps, bid caps or "the hot manual bidding method". [1ff82eb90f46]
8. Trying to "media buy" from $1K to $10K per day without fixing the business. [1ff82eb90f46]
9. Obsessing over the learning phase, or thinking an ad is good forever once it exits. [c8f9d9634c5f]
10. Making emotional decisions on daily swings, especially at low spend. [c8f9d9634c5f]
11. Steering on Meta-reported CPA after iOS 14. [40de3bd68e44]
12. Treating a high EMQ or opportunity score as a sign of profit. [40de3bd68e44] [94fa98ec33c1]
13. Winning clicks by harming user experience. [a55d9b19503c]
14. Taking Meta documentation or executive statements as binding. [94fa98ec33c1]

## 9. Caveats, conflicts and what is missing

- Single presenter, opinion-led, no controlled tests. He sells an AI-ads masterclass, which may bias his views on creative volume.
- The Total Value formula: he says Meta withdrew it and calls the third term "user value". Meta has published an auction description with a similar form (bid x estimated action rates + ad quality). `[web check: current Meta Help Center wording]` Card treats his version as a reconstruction. [3ad804612663]
- Reading estimated CTR as "all soft metrics" is his interpretation, not Meta's.
- Card 4844059375a6 attributes the 10 million advertiser figure to Meta; the transcript gives it as the presenter's own number.
- Several card steps are additions not in the transcript: bid-method-to-constraint mapping, logging suggestion outcomes, "pre-launch checklist" use, redundancy across ad accounts, pages and business managers, "redirect saved time to creative". They are marked "card addition" above.
- Internal tension: he says send Meta good data (CAPI, EMQ) yet calls EMQ overrated and ignores Meta's conversion data. His resolution: do it as cheap hygiene, but do not trust Meta's numbers.
- Conflicts with common advice: many guides stress improving EMQ as a performance lever; he calls it overrated. Many guides treat Meta's learning phase exit (a set number of conversions per week) as a key rule; he dismisses it. Common post-Andromeda advice favours many net-new concepts over variations; he disagrees. Many operators still read Meta-reported ROAS daily; he ignores Meta CPA entirely.
- Missing how: no budget per concept test, no test duration, no win or kill thresholds, no cost cap or bid cap values, no interest-audience cap amount, no audience size guidance, no detail on Advantage+ settings, no numbers for hook or hold rate.
- The ban-wave and earnings-report theory is unverified; the presenter says he cannot give specifics, and the source header says to skip it. It must not be used as policy or evasion advice.
- Scope: EMQ, CAPI, iOS and attribution belong to 06-MEA; hooks and creative fatigue belong to 10-MCR.
- For Gehna use: all Meta work is read-only in ecomOS. This source's setup steps are for planning and recommendations only.

## 10. Card index

- 4844059375a6: Meta's four-step ad serving pipeline
- 3ad804612663: The Total Value equation behind every winning impression
- 32581af3f424: Creative is the targeting: broad targeting after Andromeda
- 6ee9db26f236: Andromeda changed retrieval, not the value of variations
- 1ff82eb90f46: Choosing auto-bidding versus cost caps and bid caps
- c8f9d9634c5f: Stop optimizing to leave the learning phase
- b0bdf29a1f32: Set bidding strategy to your business constraint, not a trend
- d9cba85df27b: Push broad control to its limit, but audit Meta's suggestions
- 40de3bd68e44: Attribute conversions outside Facebook and read conversion data sceptically
- 773fc35a99e9: Send first-party signal via the Conversions API even when attribution is uncertain
- a55d9b19503c: Model every ad against the three takeaways of the auction
- 6dbefe2b17df: Treat ad rejections and ban waves as timing and account scale, not pure fault
- 94fa98ec33c1: Treat facebook internally reported numbers as untrusted until externally verified
