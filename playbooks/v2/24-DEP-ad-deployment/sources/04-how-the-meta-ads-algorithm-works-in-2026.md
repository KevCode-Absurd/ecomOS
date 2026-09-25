# How The Meta Ads Algorithm Works in 2026

source_id: 1yEyKvUZcQKwo69HfAxOG4gAIAdgcxt4p  |  folder: /24-DEP-ad-deployment (moved from /11-ADC)  |  cards: 13  |  words: 7214  |  type: transcript (YouTube video, one presenter, whiteboard style)
credibility: Presenter runs the agency Blue Sense Digital (hiring email on a .com.au domain, so likely Australian). He sells free 1-hour Loom account audits to ecommerce brands doing at least $10M a year, and is recruiting performance marketers. He says his team helped ecommerce and retail brands make "close to half a billion dollars in attributed revenue" over 5 years. He claims every mechanic is "sourced to Meta's own engineering posts and help documentation", but the transcript gives no links or document names. Evidence types: Meta's own claims (200 ms, 3% conversion lift, 5% CTR lift), his agency's observations (CPM gap between funnels, budget increases over 20%), his own failed attempts to measure server-side tracking, and his opinion (economics beat tactics). No client case data with numbers is given.
date signals: Title says 2026. Says Meta "rebuilt its entire system between 2023 and 2026". Names Lattice (2023), sequence learning (November 2024), Andromeda (December 2024), GEM (no date), adaptive ranking model (seems to be the current year, "so far this year"). Says interests and lookalikes were deprecated July 2025 and Chrome kept cookies in April 2025. Refers to his own video "how to structure account in 2026 on Meta". Document modified 21 Sep 2026.
scope note: The document header marks it core for ad account structure, algorithm mechanics, auction, vector targeting, bidding, signal quality (EMQ/CAPI), consolidation, broad targeting, exclusions, entity ID grouping and unit economics. Creative formats, concepts and UGC belong in 10-MCR. GA and organic analytics belong in 06-MEA. The header says to skip the audit pitch and hiring call. Offer design and unit economics detail belong with the offer and finance folders; they are kept here only as they touch the auction.

## 1. What this source is for

It gives an operator a mental model of how Meta picks who sees an ad in 2026: retrieval, ranking, auction. It uses that model to justify 5 account rules: go broad with exclusions, feed diverse concepts, keep EMQ high, fix unit economics first, and consolidate structure. It also lists popular Meta advice the presenter calls wrong. It is strong on "why" and weak on "how": there are no setup steps, no budget numbers for a brand, and no test designs.

## 2. Principles

### 2.1 Targeting and delivery

1. **Your creative targets the buyer, not your audience settings.** Source says Meta rebuilt its system from 2023 to 2026 and took audience choice away from advertisers. The machine reads the ad and finds the buyer. If an agency still pushes interest or lookalike targeting, the presenter says it is out of date. [48728b3abcdf]

2. **Old model: labels. New model: vectors.** Old: any interaction with a post (even a negative comment or a "I hate this post" share) gave the user a label such as "pets". Labels are weak predictors: interest in pets does not mean owning a pet or liking your brand. Stacking interests (pets + has a cat + has a family + lives in a city) was more precise, but hard to measure unless the budget was large, and it caused audience fatigue as you ran through the whole interest. New: each interaction nudges the user in a space of "tens of thousands of dimensions". Users with similar behaviour cluster together. Source admits vectors existed before too; the contrast is to teach the idea. [48728b3abcdf]

3. **Broad targeting is a probe, not a spray.** With broad targeting, Meta spends "a little sprinkle" across the whole space, sees who engages and buys, then narrows delivery to those clusters. Source says this is why "broad targeting will always outperform interest targeting on large data sets over a long period of time". Condition: large data sets and long periods. The source does not say what happens at small spend. [48728b3abcdf]

4. **Narrow creative saturates its cluster, and that is creative fatigue.** A very specific ad (example: a callout to "business owners doing over $10 million a year") makes Meta find that small cluster and saturate it. After maybe $10,000 of spend (illustration, not a benchmark) there is no one new to reach. Meta then either re-serves the same people (frequency rises) or drifts to nearby clusters outside the ideal customer profile, so ROAS tapers. Source says Meta prefers to keep hitting the middle, so frequency goes up. [4de396baf031]

5. **Warm clusters can soak up acquisition spend.** A cluster the ad finds may be warm, existing customers. Meta pushes ads there because they are likely to convert. Exclusions of existing customers are "more important than ever" so budget is not wasted on them. [071837c01e9b]

6. **What you still control, and what is only a suggestion.** Controls: exclusions ("by far one of the most important"), minimum age, locations ("definitely don't go and just set to worldwide"), languages. Suggestions only (Meta may ignore them): age bands, gender, interests, lookalike audiences ("died a very long time ago"). Age minimums are a control; age bands are not. [48728b3abcdf] [071837c01e9b] `[verify UI]` `[web check: which audience fields are hard controls vs Advantage+ audience suggestions]`

### 2.2 The 3-stage delivery pipeline

7. **Every impression goes through retrieval, ranking, then auction, in about 200 ms (Meta's figure).** Retrieval: scan "tens of millions" of ads and shortlist "a few thousand" relevant to the user. Ranking: pick the most relevant and personal ads, most likely to convert, using the user's past ad interactions and organic interactions. Auction: "hundreds of ads" bid at once for the placement. [e82a1ef3cf77]

8. **Retrieval is the stage most videos skip, and it changed most.** Andromeda sits in retrieval. Source says most content focuses only on the final auction. When everyone goes broad, everyone can technically target everyone, so retrieval decides which ads even enter a user's auction. [e82a1ef3cf77]

9. **Map each Meta update to its stage.** An update changes retrieval, ranking or auction dynamics. Use this to decide which part of the account to adapt. [e82a1ef3cf77] [066b6cc383fe]

10. **Update history as the source gives it** [e82a1ef3cf77]:
    - Lattice (2023): ranking consolidation; faster, more consolidated ranking.
    - Sequence learning (November 2024): Meta optimises across sequences of ads (ad 1, then 2, then 3) and learns whether a conversion followed, so it optimises across the purchase journey. See section 9 on what this means for "single ad per ad set".
    - Andromeda (December 2024): change to retrieval. It reads or scans all ads and retrieves relevant ones based on its understanding of the creative.
    - GEM (no date): source says GEM, not Andromeda, is "the reason why you need heavy creative diversity". GEM made Andromeda multimodal: it can watch video, listen to audio, and group creatives by format and creative representation. Source says Andromeda "probably played a part" by spotting duplicates.
    - Adaptive ranking model (recent): decides how much compute to spend per impression, to speed "time to relevancy". Result: ads follow new interactions very fast. Example: after watching an organic reel from a page, the viewer gets that page's ad almost at once. Meta claims a 3% conversion lift and 5% CTR lift across the platform from it; the presenter says to be careful with platform number claims. `[web check: Meta engineering posts on Andromeda, GEM, adaptive ranking and the 3% / 5% lift claims]`

11. **Meta updates are not against you, but they will not raise your ROAS.** Meta wants small platform-wide conversion lifts so it can raise CPMs and earnings. Source expects your ROAS to stay flat ("sideline") as you adapt, while CPMs rise and Meta keeps the gain. Presenter calls this "kind of fair enough". Opinion, not data. [e82a1ef3cf77]

### 2.3 The auction

12. **Auction formula: Bid x Estimated Action Rate + Ad Quality.** Estimated action rate (EAR) = expected CTR x expected conversion rate. So 2 advertisers showing the same product to the same person can win at very different bids. Example: a $0.50 bid can beat a $1 bid if its EAR and ad quality are better. "The fastest way to go and lower your cost isn't to go and bid more, but it's to be more relevant." [8ffd28b7fc7e] `[web check: Meta help doc wording of the auction formula]`

13. **EAR and ad quality are rear-view diagnostics, not levers.** Source says Meta has been clear they describe what already happened. Meta uses historical ad quality, CTR and conversion rate to adjust your bid per user. You cannot change them in real time. [8ffd28b7fc7e] [71ab0ba03b8a]

14. **Quality score cannot be seen or measured.** It changes in every auction. Presenter compares chasing it to "star signs": do the basic fundamentals, skip advanced tricks, because you cannot measure the outcome. He draws the same point for Google (not just highest CPC). The source does not list the "fundamentals". [8ffd28b7fc7e] [71ab0ba03b8a]

15. **You cannot optimise relevance directly; diversify instead.** Relevance differs per person and per auction. The practical move is more diverse assets, so the library is relevant to a wider pool. [71ab0ba03b8a]

16. **EAR seems to drive CPM (presenter's observation and hypothesis).** He sees EAR as "very causal to CPMs", linked to ad quality. Illustration from outside ecommerce: a lead-magnet funnel with 30 to 70% landing page conversion had CPMs "like $25"; a book-a-call funnel (for example via Calendly) with 3 to 6% conversion had CPMs "like $100", a 4x gap, on the same lead event. He is not sure why: either Meta reads landing pages and infers value, or it prices on expected action rate. If it is EAR, you can set up funnels that maximise on-page action rate to cut CPM ("arbitrage"). He says the value part is "harder to prove". [c7223bce696a]

17. **Your bid is your economics.** Higher sustainable bid means more auctions won, which means more scale. "All business strategy is pricing strategy": price as high as possible, cost of goods as low as possible, open up margin, and give as much margin as possible to acquisition. Competitors with higher prices, gross profit, AOV, LTV and better retention win. First-order levers named: units per transaction, average unit retail. "Person with better unit economics can have way worse creatives ... campaign structure ... measurement, and they can actually still outperform you." "You cannot out tactic bad economics." Opinion from the presenter; his audits start at economics and his team is trained in finance. Same claim made for Google. [bd4cb33200e9] [8ffd28b7fc7e]

### 2.4 Signal quality

18. **Clean signal gives Meta an accurate EAR, which gives cheaper, better delivery.** Conversions through pixel or CAPI raise EMQ (Event Match Quality). Example arithmetic: ads drive 100 conversions, Meta tracks 70; true conversion rate 3% (maybe industry leading), Meta sees 2%. Meta's EAR is too low, "the entire bidding equation falls apart", and you lose auctions you should win. Source calls signal quality "a hidden lever that will decrease your CPMs". [74d3bc849c6b]

19. **Server-side tracking is a nice-to-have with unmeasurable impact.** It is pushed hard by vendors. If you can afford it (tools "might be costing you a couple thousand dollars a month") and assume it probably helps, get it. Do not expect results to rise or the account to change much; it is "a very small lever". Presenter tried to measure it "multiple times" and could not: week-to-week noise hides it, window choice is unclear, other changes overlap, and even a causal impact model lacks enough variance for statistical confidence. "Get it if you can afford it, but don't expect it to be measurable." [74d3bc849c6b]

20. **Economics beat EMQ.** In the takeaways he says a better EMQ wins more auctions, but raising first-order AOV (post-purchase upsells, a better offer) gives "way more leverage than any kind of EMQ change". [bd4cb33200e9] [74d3bc849c6b]

### 2.5 Creative diversity and the Entity ID trap

21. **Similar ads collapse into 1 Entity ID and lose unique reach.** Andromeda scans ads; near-identical ones are grouped under the same Entity ID. Example: 200 ads register as 20 unique ads, in groups of 10 (illustration). All ads in a group serve the same audience pool, with no unique reach. Repeating similar ads to the same people does not raise purchase odds. The point of more concepts is to reach more unique people or convert existing ones; near-duplicates do neither. [917ee36d87e9]

22. **A concept = angle x offer x persona, arguably plus format.** Plan creative by concept. Changing format "enough" can make Meta register a different ad even with the same angle, offer and persona. [917ee36d87e9] [4de396baf031]

23. **Iterations are allowed, but only concept diversity reaches net-new audiences.** "You can still have iterations within the account, but ultimately to reach net new audiences, you are going to require diversity within the concepting." [4de396baf031] [917ee36d87e9]

### 2.6 Account structure

24. **Structure exists to silo data on purpose.** Campaign > ad set > ad exists on Meta, Google, TikTok, Pinterest and Snapchat. It is your manual signal to the algorithm that some ads are different enough to learn separately. Campaigns do not share data; each has its own machine learning model. It is not there to make reporting look tidy. [0ed2f8dbde17]

25. **Consolidate by default; segment only for genuinely different audiences.** Example of valid segmentation: ice baths and saunas sold on one site resonate with very different people, so separate learning may make sense. Over-splitting (many campaigns, many ad sets, very few ads each, low spend) splits conversion data and gives worse performance on Meta, Google and TikTok. "Anytime you can consolidate ... you will see better performance." The source does not give spend or conversion thresholds for when to split. [0ed2f8dbde17]

### 2.7 Scaling

26. **The "20% budget increase" rule is not in Meta documentation.** Presenter's agency raises budgets by more than 20% "all the time and it's fine". The dip people see is a lag: new audiences need time to see several ads before buying. "If you just triple budgets today, revenue doesn't triple." He calls it a business effect, not an algorithm reset. No safe percentage and no evaluation window are given. [eff64339b5de] [066b6cc383fe]

## 3. Procedures

The source gives no click-level setup steps. It gives 1 ordered action list (its 5 takeaways) and 1 review habit. Steps below stay at that level.

### 3.1 The source's 5 next steps (its own order)
1. Go broad with exclusions. Exclude existing customers from acquisition. Keep minimum age, locations (not worldwide) and languages set. Do not rely on age bands, gender, interests or lookalikes. [48728b3abcdf] [071837c01e9b] `[verify UI]` `[needs brand data: customer list or purchaser audience to exclude; target countries and languages; minimum age for the category]`
2. Feed the algorithm diverse concepts (angle x offer x persona, plus format). Iterations are fine but do not count as diversity. [917ee36d87e9] [4de396baf031]
3. Make sure EMQ is high, since EMQ feeds EAR and EAR feeds the auction. Send conversions through pixel and CAPI. [74d3bc849c6b] `[needs brand data: current EMQ score per event]` `[verify UI]`
4. Review unit economics on first purchase and 365-day LTV payback ("365-day LTV pay" in the transcript). Ask whether they are as good as they could be. Raise first-order AOV and gross profit with post-purchase upsells and a better offer. Source says this beats any EMQ change. It points to its own 1-hour video "how to make offers in e-commerce". [bd4cb33200e9] `[needs brand data: first-order AOV, gross margin, COGS, units per transaction, 365-day LTV]`
5. Consolidate where possible. Split campaigns or ad sets only when audiences truly differ. Source points to its own 1.5-hour video "how to structure account in 2026 on Meta" for detail not given here. [0ed2f8dbde17]

### 3.2 Split-or-consolidate test (from the source's framing)
1. For each campaign or ad set split, ask: are these ads different enough that they must not share data? [0ed2f8dbde17]
2. If the products resonate with very different people (ice baths vs saunas), a separate campaign can be kept. [0ed2f8dbde17]
3. If not, merge them so conversion data pools. [0ed2f8dbde17]

### 3.3 Review habit for Meta advice (card framing, built on source content)
1. For any tactic, ask which stage it claims to affect: retrieval, ranking or auction. [066b6cc383fe] [e82a1ef3cf77]
2. Ask whether Meta documents it. The source rejects the 20% rule because no Meta doc supports it. [066b6cc383fe]
3. Drop tactics built on items the source calls stale: interests and lookalikes, "new" Lattice, cookie deprecation, direct quality score or relevance optimisation. [066b6cc383fe] `[web check: current status of each]`

### 3.4 Budget increase (what the source implies)
1. Raise budget by whatever step is needed; the 20% cap is not a documented limit per the source. [eff64339b5de]
2. Do not judge the increase on same-day revenue; allow for the lag while new audiences see several ads. Source gives no window length. [eff64339b5de] `[needs brand data: typical days from first ad view to purchase]`

## 4. Rules, thresholds and numbers

| rule | number or threshold | condition | source's basis | card id |
|---|---|---|---|---|
| Delivery pipeline time | about 200 ms for retrieval + ranking + auction | every impression | Meta's statement, as quoted | e82a1ef3cf77 |
| Retrieval shortlist | tens of millions of ads down to a few thousand | per impression | Meta docs, as quoted (transcript also says "tens of thousands" once) | e82a1ef3cf77 |
| Ads in the auction | hundreds | per impression | as quoted | e82a1ef3cf77 |
| Vector space size | tens of thousands of dimensions | user modelling | presenter's explanation | 48728b3abcdf |
| Broad beats interests | "always", on large data sets over long periods | large data, long time | presenter's claim | 48728b3abcdf |
| Narrow persona saturation | maybe $10,000 of spend | very specific callout ad (example: owners of $10M+ businesses) | illustration | 4de396baf031 |
| Auction score | Bid x EAR + Ad Quality | every auction | Meta docs, as quoted | 8ffd28b7fc7e |
| EAR | expected CTR x expected CVR | every auction | as quoted | 8ffd28b7fc7e |
| Relevance beats bid | $0.50 bid can beat $1 bid | same product, same person, better EAR and quality | illustration | 8ffd28b7fc7e |
| Lead-magnet funnel | 30 to 70% page conversion, CPM about $25 | non-ecommerce, lead event | presenter's observation | c7223bce696a |
| Book-a-call funnel | 3 to 6% page conversion, CPM about $100 (4x) | non-ecommerce, same lead event | presenter's observation | c7223bce696a |
| Signal loss example | 100 real conversions, 70 tracked; 3% true vs 2% seen CVR | poor tracking | worked example | 74d3bc849c6b |
| Server-side tracking cost | "a couple thousand dollars a month" | third-party tools | presenter's estimate | 74d3bc849c6b |
| Entity ID grouping | 200 ads seen as 20 unique, groups of 10 | many near-identical ads | illustration, not a fixed ratio | 917ee36d87e9 |
| Budget increase cap | 20% rule has no Meta documentation; >20% is routinely fine | scaling | agency experience | eff64339b5de |
| Adaptive ranking lift | +3% conversions, +5% CTR platform-wide | Meta claim | presenter says treat with care | e82a1ef3cf77 |
| Interests and lookalikes | deprecated July 2025 | Meta targeting | presenter's claim `[web check: Meta targeting changes July 2025]` | 066b6cc383fe |
| Chrome cookies | kept; decision April 2025 | tracking planning | presenter's claim `[web check: Chrome third-party cookie status]` | 066b6cc383fe |
| Lattice | 2023; "really doesn't matter anymore" | education and SOPs | presenter's claim | 066b6cc383fe |
| LTV window | 365-day LTV payback | bid ceiling review | presenter's recommendation | bd4cb33200e9 |
| Audit offer threshold | brands doing at least $10M a year | promo only | not a rule | none |

## 5. Diagnostics and checks

| check | how | good | bad | next step | card |
|---|---|---|---|---|---|
| Is targeting broad with real controls only? | Review ad set audience settings `[verify UI]` | Broad; exclusions, min age, locations, languages set | Stacked interests or lookalikes; worldwide location | Move to broad with exclusions | 48728b3abcdf |
| Are existing customers excluded from acquisition? | Check exclusion audiences on prospecting ad sets `[verify UI]` | Customer list excluded | No exclusions | Build and apply customer exclusion `[needs brand data: customer file]` | 071837c01e9b |
| Is spend drifting to warm people? | Source gives no method. Card suggests splitting new vs returning conversions (card inference, not in transcript) `[needs brand data: new vs returning customer sales]` | Mostly new buyers | Mostly returning buyers | Tighten exclusions | 071837c01e9b |
| Is a narrow concept saturated? | Watch frequency and ROAS trend on persona-specific ads `[needs brand data: frequency, ROAS by ad]` | Stable frequency and ROAS | Frequency rising, ROAS tapering | Add new distinct concepts, not more iterations | 4de396baf031 |
| How many distinct concepts are live? | Count ads by angle x offer x persona (and format), not by file count | Many distinct concepts | Many near-duplicates | Cut duplicates, brief new concepts | 917ee36d87e9 |
| Is the account over-segmented? | Count campaigns and ad sets vs spend and ads per ad set | Few campaigns, splits only for truly different audiences | Many campaigns and ad sets, few ads each, low spend | Consolidate | 0ed2f8dbde17 |
| Is Meta seeing all conversions? | Compare Meta-reported purchases with backend orders; check EMQ `[needs brand data: backend orders, EMQ]` `[verify UI]` | Meta count close to real count; high EMQ | Large gap (example 70 of 100) | Fix pixel and CAPI | 74d3bc849c6b |
| Did server-side tracking help? | Source says you mostly cannot tell: noise, window choice, overlapping changes, low variance even with causal impact | n/a | Expecting a clean before/after | Treat as a cost with hoped-for upside | 74d3bc849c6b |
| Are weak EAR or quality signals a settings issue? | Source: they are rear-view diagnostics | n/a | Tweaking settings to lift a score | Look at concept diversity, offer or landing page action rate | 71ab0ba03b8a |
| Do CPMs differ by landing page action rate? | Compare CPMs across pages or offers firing the same event `[needs brand data: CPM and page CVR by landing page]` | Higher action rate, lower CPM (hypothesis holds) | No link | Treat as hypothesis only | c7223bce696a |
| Are unit economics limiting scale? | Review first-order AOV, gross profit, COGS, units per transaction, 365-day LTV `[needs brand data: these figures]` | Room to bid above competitors | Thin margin, low AOV | Work on price, offer, upsells before tactics | bd4cb33200e9 |
| Did a budget rise "break" the campaign? | Look past same-day revenue; allow for lag | Revenue catches up later | Judging on day 1 | Wait out the lag (source gives no window) | eff64339b5de |

## 6. Tools, settings and named features

- **Broad targeting** (Meta ad set audience): default per source. `[verify UI]`
- **Exclusions** (custom audience of existing customers): most important control left. `[verify UI]`
- **Minimum age, locations, languages**: real controls. **Age bands, gender, interests, lookalikes**: suggestions only. `[verify UI]` `[web check: Advantage+ audience control vs suggestion fields]`
- **Meta Pixel and Conversions API (CAPI)**: send conversions back to Meta. `[verify UI]`
- **EMQ (Event Match Quality)** score: signal quality measure; the transcript also writes it "AMQ" and "Ven Match Quality" (transcription errors). `[verify UI]`
- **Server-side tracking software**: third-party, around a couple thousand dollars a month; nice-to-have. No vendor named.
- **Causal impact model**: named as the kind of method needed to test server-side tracking; source says even that lacked power.
- **Andromeda** (retrieval), **Lattice** (ranking, 2023), **sequence learning** (Nov 2024), **GEM** (multimodal grouping), **adaptive ranking model** (compute per impression): Meta systems, context only. `[web check: current names and roles]`
- **Entity ID**: Meta's grouping of similar ads. The card notes it is not visible in the ad account, so it must be reasoned about through concept planning. [917ee36d87e9]
- **Quality score / ad quality, estimated action rate**: not visible, change per auction (source's claim). `[web check: whether Ads Manager relevance diagnostics expose any of this]`
- **Google Ads quality score**: named as a parallel.
- **Calendly**: example booking tool in the non-ecommerce funnel illustration only.

## 7. Examples and case results

All are examples or illustrations, not promises.
- Pets post: interacting (even negatively) used to tag you with a "pets" label; now it nudges your vector. [48728b3abcdf]
- Persona callout to business owners doing $10M+ a year saturates after maybe $10,000 of spend. [4de396baf031]
- Presenter's own account: small retargeting-only spend. People who watch one of his reels get his ad almost at once, which he credits to the adaptive ranking update. [e82a1ef3cf77]
- Meta's claimed lift from the adaptive ranking update: +3% conversions, +5% CTR. [e82a1ef3cf77]
- $1 bid losing to a $0.50 bid on better EAR and ad quality. [8ffd28b7fc7e]
- Lead magnet (30 to 70% CVR, about $25 CPM) vs book-a-call (3 to 6% CVR, about $100 CPM), same lead event. Not ecommerce. [c7223bce696a]
- 100 conversions, 70 tracked; 3% real vs 2% seen conversion rate. [74d3bc849c6b]
- 200 ads read as 20 unique entities, groups of 10. [917ee36d87e9]
- Ice baths vs saunas on one site as a valid reason to segment. [0ed2f8dbde17]
- Tripling budget today does not triple revenue today. [eff64339b5de]

## 8. Mistakes the source warns about

1. Running interest or lookalike targeting, or believing it is better. [48728b3abcdf] [066b6cc383fe]
2. Setting location to worldwide. [48728b3abcdf]
3. Treating age bands or gender as controls. [48728b3abcdf]
4. Not excluding existing customers, so spend goes to warm buyers. [071837c01e9b]
5. Making one very narrow persona ad and scaling it until frequency climbs and ROAS tapers. [4de396baf031]
6. Uploading many near-identical ads and counting them as variety (Entity ID trap). [917ee36d87e9]
7. Raising bids to cut costs instead of being more relevant. [8ffd28b7fc7e]
8. Chasing quality score or relevance as if it were a setting. [8ffd28b7fc7e] [71ab0ba03b8a]
9. Buying server-side tracking and expecting a visible jump in results. [74d3bc849c6b]
10. Trying to out-tactic bad unit economics. [bd4cb33200e9]
11. Hyper-segmenting: many campaigns and ad sets, few ads each, low spend. [0ed2f8dbde17]
12. Thinking account structure exists only for your own reporting. [0ed2f8dbde17]
13. Capping budget rises at 20% because it "resets learning", and reading the lag as an algorithm problem. [eff64339b5de]
14. Teaching Lattice as new, planning around cookie deprecation. [066b6cc383fe]
15. Mixing up Andromeda and GEM as the cause of the need for diversity (source says GEM). [e82a1ef3cf77]
16. Focusing only on the final auction and ignoring retrieval. [e82a1ef3cf77]

## 9. Caveats, conflicts and what is missing

- **Sales source.** The video ends with an audit pitch and a hiring call. Its "half a billion in attributed revenue" is attributed (platform-reported), not audited, revenue.
- **No citations shown.** It claims to use Meta engineering posts and help docs but names none. Dates and system roles need a check. `[web check: Meta engineering blog posts on Lattice, Andromeda, GEM, sequence learning, adaptive ranking]`
- **Single ad per ad set is ambiguous.** The transcript says after sequence learning "your ad account should have been updated and structured accordingly, aka single ad per ad set, and kind of died back in November 2024". The most natural reading is that the single-ad-per-ad-set structure died in November 2024. Card [0ed2f8dbde17] reads it the other way ("requires ... one ad per ad set") and card [e82a1ef3cf77] says the update "supports" one ad per ad set. Treat the card reading as unconfirmed. `[web check: Meta guidance on ads per ad set after sequence learning]`
- **Andromeda vs GEM on grouping.** The source says GEM is why diversity matters, but in the Entity ID section it says Andromeda scans and groups ads. Both stated; it frames GEM as giving Andromeda multimodal reading.
- **Small internal slip.** Retrieval is described as "tens of millions" of ads and once as "tens of thousands".
- **"Broad always beats interests"** is conditioned on large data sets over long periods. The source gives no guidance for small budgets or new accounts.
- **Quality score "not visible".** Common advice points to Ads Manager relevance diagnostics (quality, engagement and conversion rate rankings). The source does not mention them. `[web check: current Ads Manager relevance diagnostics]`
- **CPM arbitrage is a hypothesis from non-ecommerce funnels.** The presenter says the value part is hard to prove. No ecommerce test is given. [c7223bce696a]
- **Economics dominate** is opinion ("cannot out-tactic bad economics"), not shown with data. [bd4cb33200e9]
- **EMQ tension.** It calls signal quality a lever that lowers CPMs, then calls server-side tracking a very small, unmeasurable lever. These fit if pixel plus CAPI basics are the lever and paid server-side tools are the extra. The source does not draw that line itself.
- **Card additions not in the transcript:** prioritising purchase, lead and add-to-cart events [74d3bc849c6b]; splitting new vs returning conversions and separating retargeting from acquisition [071837c01e9b]; using frequency and cluster-level spend as refresh triggers [4de396baf031]; bundles as an AOV lever [bd4cb33200e9]; "default to consolidation especially at low spend" [0ed2f8dbde17]. Use as card inferences, not source claims.
- **Missing how-to:** no exclusion setup steps, no EMQ targets, no CAPI setup, no budget numbers, no evaluation window after a budget rise, no minimum spend or conversions per campaign before splitting, no way to see Entity ID grouping, no creative volume per week, no bid strategy choice (cost cap, bid cap, etc.) despite the auction focus.
- **Conflicts with common ecommerce advice:** (1) the 20% budget rule, widely taught, is called undocumented; (2) CAPI and server-side tracking are often sold as big wins, the source calls the paid tools unmeasurable; (3) lookalikes and interests are still offered in many guides, the source says deprecated July 2025; (4) relevance or quality optimisation is often taught as a lever, the source calls it a diagnostic. `[web check: each of these 4]`

## 10. Card index

- 48728b3abcdf  Why your ad creative, not your targeting, selects the buyer
- e82a1ef3cf77  The three-stage Meta delivery pipeline: retrieval, ranking, auction
- 4de396baf031  Trigger creative fatigue deliberately, then refresh before ROAS tapers
- 071837c01e9b  Use exclusions to stop budget leaking to your warm customer cluster
- 8ffd28b7fc7e  Bid equation: relevance multipliers beat raising bids
- c7223bce696a  Turn estimated action rate into a CPM arbitrage through landing-page action design
- 74d3bc849c6b  Improve Event Match Quality to feed an accurate action rate
- 917ee36d87e9  Avoid the Entity ID trap by engineering true concept diversity
- eff64339b5de  Use the 20% budget-increase rule correction: it's a lag effect, not a learning reset
- 0ed2f8dbde17  Consolidate account structure to unify conversion data, but keep justified segmentation
- bd4cb33200e9  Treat unit economics as the scaling constraint, not platform tactics
- 71ab0ba03b8a  Stop optimizing for relevance and quality directly, diversify instead
- 066b6cc383fe  Prune deprecated targeting advice from your Meta playbook
