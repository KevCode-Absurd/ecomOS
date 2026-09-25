# How To Fix An Underperforming Google Ads Account

source_id: 1FHkxdCv4zRv4MOZ_iQ5uVQ-lqJFakJVB  |  folder: /12-GAD-google-ads  |  cards: 15  |  words: 8,996  |  type: talk (1-hour solo training video, auto-transcribed)

credibility: Presenter works at Blue Sense Digital, a paid media agency (hiring address ends in .com.au, so Australian). Not named in the transcript. Evidence is the agency's own audit and client work: says 80 to 90% of the businesses it works with and audits skew spend to Meta. Gives 1 client example (a sunglasses wholesaler) with no before and after numbers, and 1 personal account of a slow landing page experience fix. No data tables, no tests. The video sells a free audit to brands doing over $5 million a year and recruits performance marketers. Possibly the same agency as 24-DEP source 03 (same audit offer and $5 million floor, same "top-down" method), but the transcript does not confirm it.
date signals: Refers to its own 2.5-hour video "creative strategy in 2026", so recorded late 2025 or 2026. Refers to an earlier "other Google video" on target ROAS (not in this source). Says new-customer ROAS can "these days" be seen natively in Google Ads. Names PMax, Shopping, Search, Display, YouTube, GMC, search partners, auction insights, Quality Score columns.
transcript note: Auto-transcription errors. "high tea ROAS" = high tROAS (target ROAS). "big expanders" = big spenders. "NC ROAS" = new-customer ROAS. "better spend" (brand search) is unclear; likely "Meta spend". "grow multiple fixes" = throw multiple fixes. "search impression share lost {bracket} rank" = Search lost IS (rank).
header warning: The document text starts with a routing note for 06-MEA (measurement) and says ad-platform diagnostics belong in 11-ADC. The file now sits in 12-GAD. The content is a Google Ads diagnostic method with a measurement front end, so it fits both. Nothing in the header adds numbers that the transcript lacks.

## 1. What this source is for

It gives an operator a fixed order to investigate a Google Ads account that looks like it is underperforming, so they do not change the wrong thing. It runs top-down: business KPIs, channel check, campaign type, specific campaign, metric, sub-metric, trigger, root cause. It lists failure modes per campaign type (PMax, Shopping, Search), the formulas that split each metric, and the checks for CPC, conversion rate, impressions and CTR. It ends with how to apply a fix: default to a fix over a rebuild, isolate fixes when severity allows, and do not touch the account until you can state the root-cause sentence. It is strong on order and logic, thin on the actual fixes (source says there are about 20 sub-metrics and about 100 fixes each, and does not list them).

## 2. Principles

1. **3 failure modes cause most harm on an underperforming account.** (1) You make a change you should not have, and things get worse. (2) You do not make a change when you should have. (3) You make many changes, but the dip had nothing to do with the platform. The method exists to prevent all 3. [7c50191f8854]
2. **Investigate top-down, never bottom-up.** Start at business KPIs, then channel, campaign type, campaign, metric, sub-metric, cause, root cause. Ask "why" at each layer. Source says starting at the bottom is "the whole reason why most people are not good at root cause analysis". [7c50191f8854] [7fe2bb1f5bff]
3. **Before touching anything, run 3 rules: change history, longer time horizon, conversion latency.** Skipping them risks changing a healthy account. [62403f6f3b48]
4. **Most accounts that look broken are not broken.** Source says you are "probably just misreading them or looking at the data wrong". This is the presenter's view. [62403f6f3b48] [7c50191f8854]
5. **Google is rarely the cause of a business revenue dip when it is a minority of spend.** Source says on most businesses where Google is 20 to 30% of spend, Google "usually isn't the reason". Source calls Google "one of the most consistent platforms" and Meta "all over the place" (creative winners scale spend fast, then fatigue). This is the presenter's opinion from its client base. [7fe2bb1f5bff]
6. **Check platforms in order of spend share.** If Meta is the bigger spender, diagnose Meta first. If Google is the bigger spender, diagnose Google first. [7fe2bb1f5bff]
7. **Separate true business KPIs from attributed numbers.** True KPIs: revenue, profit contribution, MER, aMER (any efficiency number indexed on actual business revenue). Attributed numbers can carry conversion lag or a tracking error. Source says it diagnoses from true business KPIs and "rarely" from attributed numbers. [7fe2bb1f5bff]
8. **Rule out seasonality with a forecast before diagnosing.** If the dip matches the forecast, no diagnostic is needed. Without a forecast, seasonal dips waste hours of diagnosis. [e2a87175fcd5]
9. **Only the top 5 campaigns by spend can move the account.** Source says the cause is "somewhere in the top five by spend". A small campaign can be the cause, but it is unlikely, so check it last. [26676d575992]
10. **Campaign type decides the failure mode.** PMax, Shopping and Search decline for different reasons, so find the type before troubleshooting. [4e3675b7a020] [31ee29611482]
11. **Raising target ROAS does not raise efficiency; it narrows the audience.** Google enters fewer auctions, the ones it expects to win with high-intent buyers. This skews warmer, likely pulls spend back and likely worsens new-customer acquisition. Source says tROAS shows "how hard the campaign will go on just retargeting warm people", not cold performance. Applies to PMax, Shopping and Search. [4e3675b7a020] [141c23b0306c]
12. **Every campaign KPI is the product of 2 or 3 underlying metrics.** Knowing the formulas lets you reach the real root cause, not the first symptom. [2069300bf455]
13. **CPC is close to a vanity metric.** It matters only at the extremes (very high or very low). CPC up with conversion rate up keeps CPA flat and is fine. CPC up with conversion rate flat is the problem signal. Source says the same holds on Meta and TikTok. [6ff74a04932d]
14. **Audience change links many sub-metrics.** A change in audience (search terms, bidding strategy, auctions entered) can lower both conversion rate and CTR. [2795573cf2d6] [86ca17cab286]
15. **Default to a fix, not a rebuild.** A rebuild triggers a learning reset. Source warns of a feedback loop: decline, big change, more decline, another big change. Rebuild only if fixes fail or cannot close the gap to historical performance. [5df8489778d1]
16. **Isolate fixes when severity allows.** Applying many fixes at once (the "kitchen sink") hides which one worked, so you cannot repeat the fix next time. If the situation is dire, the kitchen sink is acceptable. [817f1a421116]
17. **Be honest about how big a fix's impact will be.** A headline change will not fix a business decline unless a headline change caused it. Keep rethinking the fix until it is big enough to close the gap. [5df8489778d1]
18. **Do not touch the account until you can finish the root-cause sentence.** "This campaign is underperforming because this metric dropped, driven by this sub-metric, which was caused by this trigger, which itself was the root cause." [7c50191f8854]

## 3. Procedures

### 3.1 Pre-diagnosis rules (before any audit or change) [62403f6f3b48]

1. Check change history. Look for changes by you, teammates, the client or anyone else with access. Do not audit or change anything right after a batch of your own changes. [verify UI: Change history location in Google Ads] [needs brand data: who else edits the account and the site]
2. Extend the time horizon. Do not diagnose a 1-day read. Zoom out as far as possible, scaled to the account's conversion volume, to avoid small-sample bias. Source gives no number here; the account scan in 3.3 uses 90 to 180 days. [needs brand data: daily and weekly conversion volume]
3. Check conversion latency. Google credits a conversion to the click date, not the purchase date. Source's timeline: click on the 1st, click again on the 3rd, buy on the 7th. Most platforms show the purchase on the 7th; Google shows it back on the click date. So the last 3 to 4 days (and often the last 7) always look bad on ROAS and conversions.
4. Add the custom column "conversions by conversion time" (credits the purchase day). Use it to read the last 3 to 4 days. The keyword to look for is "conversion time". [verify UI: column name and whether it is a custom column or a standard "by conv. time" column] [web check: current Google Ads "conversions (by conv. time)" columns]

### 3.2 Level 1: business signal (source says about 5 minutes for a skilled operator)

Goal: decide whether Google Ads is broken at all. Often you stop here. [7fe2bb1f5bff] [e2a87175fcd5]

1. Cross-channel check. Get the media mix by spend share. [needs brand data: spend by platform for the period]
   - Example: 90% Meta, 10% Google. A revenue dip is probably Meta. Source adds that "probably half" of that Google 10% is brand, so only about 5% is new-customer acquisition through Google. Do not troubleshoot Google.
   - Example: 65% Meta, 35% Google. Probably Meta, but not certain. Troubleshoot both; Meta first.
   - Example: 65% Google, 35% Meta. Google first.
2. Ask what changed outside Google. This "shouldn't be a two-second process". Questions the source gives:
   - Did anything materially change on Meta, Pinterest, TikTok or in the business?
   - Did we come off the back of a sale?
   - Did we do a full creative refresh on Meta and performance fell after it?
   - Did we change the offer on Meta?
   - Agency side: ask the client "did anything happen within the business that we're not across?"
   - Do your own checks: open Meta and TikTok change history, check the website is not broken. [needs brand data: promo calendar, site changes, other-platform change logs]
3. Split the revenue equation: Revenue = Conversion Rate x Average Order Value x Sessions. Find which of the 3 fell. [needs brand data: store analytics for sessions, conversion rate, AOV]
   - Conversion rate down: look at the website.
   - Sessions down: find which traffic source lost click volume.
   - AOV down: check product prioritisation (possibly inside Google Ads, where some products may suddenly be pushed more) or a website change to structured upsell or cross-sell.
4. Classify the drop: true business KPI (revenue, profit contribution, MER, aMER) or attributed number. If revenue fell, check which attributed figures correlate. Is Meta suddenly attributing much lower (source's example: ROAS from 4 to 3)? Did Google drop? Read Google on conversion time, not default conversions. [needs brand data: MER, aMER, platform-attributed revenue by day]
5. Check seasonality against the forecast. If the dip is in line with expected seasonality, stop. If it is outside the forecast, continue. Card adds: keep the forecast as an expected range and keep it updated. [needs brand data: revenue forecast by period]
6. Move to Google only if nothing happened elsewhere and it "seems to me definitely a Google issue".

### 3.3 Levels 2 and 3: account and campaign drill (the "5-minute check") [31ee29611482] [26676d575992]

1. Set the date range to the last 90 to 180 days. Switch to a weekly view. [verify UI]
2. Stay on the Overview tab (top left). Rotate the graph through each metric: cost, conversions, conversion value, cost per conversion, ROAS (conversion value / cost), CTR. For each, note up, down or sideways. [verify UI]
3. Find the inflection point: the date a metric started to trail off (source's example: 3 March).
4. Go to the Campaigns tab. Sort by cost descending. Work down the top 5 spenders only. Ask which campaign contributed most to the change after the inflection date. If this is a Google issue, expect 1 or 2 campaigns where conversions, ROAS or CTR declined after that date. [verify UI]
5. Drop to ad group level (asset group level in PMax). Repeat. Ask: did all groups decline, or 1 specific group?
6. Record 2 facts: (a) which campaign type fell off (PMax, Shopping, Search, Display, YouTube, other), (b) which specific campaigns and ad groups.

### 3.4 Campaign-type failure checks

**PMax** (4 failure modes) [4e3675b7a020]

1. Warm and cold drift. PMax can retarget and place across all channels, so a campaign labelled cold can drift to serving mostly existing customers.
   - Check the search term report for brand terms. Brand should already be excluded; this is a double-check. [verify UI: PMax search terms or search term insights] [web check: current PMax search term and brand exclusion features]
   - Check the audience report for skew toward existing customers. [verify UI]
   - If brand terms appear or the audience skews warm: the brand exclusion is broken, or target ROAS is pushed too high.
2. Feed disapprovals. Source says in ecommerce 80 to 90% of PMax performance comes from Shopping, and Shopping performance comes from feed quality.
   - Check products within the campaign: have any top-spending products gone out of stock, been turned off or been disapproved? [verify UI]
   - Check GMC (Google Merchant Center) and "double-check everything there". [verify UI] [needs brand data: stock status of top-spend products over the period]
3. High target ROAS narrowing targeting. See principle 11. Check new-customer ROAS in a third-party attribution tool (source names Triple Whale "or any tool that you use") or natively in Google Ads. A higher tROAS on the same PMax campaign typically shows much worse NC ROAS than a lower tROAS. [needs brand data: NC ROAS by campaign] [web check: native new-customer reporting in Google Ads]
4. Product bloat. Source says this does not apply to most accounts. If SKU count grows fast and new products flood the campaign, the number of products can hurt learning. Sub-point: products going in and out of stock reset that product's learning and affect the whole campaign, worst for high-spend products. Example: a product holding 15% of PMax spend goes out of stock for 4 days and comes back. [needs brand data: SKU growth rate, stock-out history]

**Search** (4 checks) [141c23b0306c]

1. Search terms. Open the search term report. Set the period before the inflection point, sort by spend, note top-spending terms and their efficiency. Repeat for the period after. Has it materially changed? If not, move on. With broad match and smart bidding there can be "a wild change in search term spend allocation" that caused the drop. [verify UI]
2. Auction insights. Compare before and after the inflection point. A new competitor launching search campaigns can drown you out: CPCs rise, or you enter fewer auctions. [verify UI]
3. Target ROAS. Same as PMax: raising it narrows audience targeting.
4. Display. Make sure display is turned off, or spend may have flowed into display and caused the drop. [verify UI: Display Network setting on Search campaigns]

**Shopping** (same as PMax except warm and cold drift) [4e3675b7a020]

1. Target ROAS.
2. GMC. Source calls this "likely the biggest and most important thing to check". Have products gone out of stock? Did we change titles or descriptions recently? Are there errors or warnings in the GMC feed? [verify UI]
3. Too many products flooding the campaign.
4. Search partners. "Probably not causing anything, but it's worth checking": is a lot of spend going to search partners and performing poorly? Card lists this under PMax and Shopping. [verify UI: search partners segment]

### 3.5 Levels 4 and 5: metric and sub-metric [2069300bf455]

1. Take the declining campaign KPI and split it.
   - Attributed revenue down: driven by CPC, conversion rate and AOV (the revenue equation, with clicks and CPC in place of sessions).
   - Conversions down: clicks dropped, conversion rate dropped, or tracking broke.
2. Use the 2 core formulas. Source says they get you "90% of the way most of the time":
   - CPA = CPC / conversion rate.
   - Clicks = Impressions x CTR.
3. Decide which branch: efficiency down with click volume about the same means CPC and conversion rate (3.6, 3.7). Efficiency the same but volume (spend or revenue) down means clicks (3.8, 3.9).
4. For AOV, go deeper. AOV is a blend of new-customer AOV and returning-customer AOV, each on a distribution curve. Each order is driven by units per transaction (UPT) and average unit retail (AUR). Order: find which of NC or returning AOV dipped, look at how its distribution curve changed, find which part changed, then whether UPT or AUR moved, then what mechanically moved it. Source says asking "what offer changed?" is not root cause. [needs brand data: order-level data split by new and returning customer]
5. Write down which sub-metric moved and what triggered it before proposing a fix.

### 3.6 CPC up: 3 causes [6ff74a04932d]

1. Quality Score. Open Keywords. Add columns: Quality Score, Expected CTR, Ad relevance, Landing page experience. Compare before and after the inflection point. If any changed materially, troubleshoot that one. [verify UI: column names under Quality Score]
   - Ad relevance: often easy. Make the ad more relevant to the search terms it actually serves on.
   - Expected CTR: extrapolated from current CTR. The ads need to get better.
   - Landing page experience: hardest. Needs dev work. Google's rescan and rescoring cycle is "pretty unknown". Source's own case: weeks, if not months, after the site was fixed. [web check: current guidance on landing page experience scoring]
2. New competitor. Open auction insights for before and after the dip. Look for a new entrant. [verify UI]
3. Premium auctions. A change to target ROAS or any bidding strategy can push you into more expensive auctions. Not bad if clicks are higher quality. It is a problem when you enter premium auctions and conversion rate does not rise.

### 3.7 Conversion rate down: 5 checks in this order [86ca17cab286]

1. Tracking. Has tracking stopped working? Are you reading a short recent period without conversions by conversion time? Both make conversion rate look bad with no real change. [needs brand data: backend orders vs Google-reported conversions by day]
2. Landing page. Source says this is probably the number 1 reason when conversion rate drops. Check:
   - Did you switch to a different URL?
   - Did you make material changes to the page?
   - Did the price change?
   - Is a redirect now pushing to a different website?
   - Were upsells or cross-sells added?
   - Did site merchandising change? [needs brand data: site change log, price history]
3. Audience. Same page and site can convert better with higher-quality users from premium auctions, or worse with lower-quality users. Check the search term report: have the terms driving traffic changed? Are they from keywords with no congruency with the landing page? Did a bidding strategy change push toward a different audience?
4. Learning phase. Did a large structural change push the account back into learning? Source says this "will always decrease conversion rates" because the system enters the wrong auctions and sends poor traffic. [web check: current Google Ads learning or "bid strategy status" behaviour]
5. Offer. Did a promo end? Was a discount removed? Did the free shipping threshold change? [needs brand data: promo and shipping threshold history]

### 3.8 Clicks down (volume): impressions branch [2795573cf2d6]

1. Split lost clicks into impressions and CTR.
2. Impressions down means you enter fewer auctions or show less. Find which of 2 causes:
   - Impression share lost to budget: you hit the budget. Example: a $100 a day budget that is being hit. More impressions need more spend.
   - Impression share lost to bid (rank): your bid is not high enough to enter enough auctions.
3. Tell them apart. If you are hitting the budget, it is budget. If click volume and impressions are both down (with spend steady), source says "I can almost guarantee" it is the bid, not the budget. [verify UI: Search lost IS (budget) and Search lost IS (rank) columns]
4. Note a false alarm: impressions can change on a flat budget because higher-quality users raise CTR, which offsets click volume.
5. Fix impression share lost to bid by working its 3 inputs: Quality Score (3.6 step 1), new competitors (3.6 step 2), and how aggressively you enter auctions (3.6 step 3).

### 3.9 Clicks down (volume): CTR branch [2795573cf2d6] [caf9cb9b298e]

1. Ad fatigue. Source says rare on Google; "super unlikely" on Shopping, possible on Search.
2. Audience mismatch. The ad that used to fit specific search terms and people no longer fits because the audience changed. Check search terms and bidding changes as in 3.7 step 3.
3. Seasonal copy. Read the ad copy for anything that no longer fits the moment (example: a summer sale message after summer).
4. Competitive pricing (Shopping). Source says this "will normally tell you one-for-one" why CTR fell: a competitor put the same product on sale (example: 20% off), and searchers click the cheaper listing. Check competitor prices on the affected products. [needs brand data: own price vs competitor price by product] [web check: Merchant Center price competitiveness reports]
5. Add the column "search impression share lost (rank)". Source recommends it here as a side note. [verify UI]

### 3.10 Level 8: root cause and fix [5df8489778d1] [817f1a421116] [7c50191f8854]

Source jumps from level 5 to level 8; levels 6 and 7 are not named.

1. Complete the root-cause sentence (principle 18). If you cannot, do not touch the account.
2. Assess severity. Dire: a kitchen-sink response is acceptable because fixing matters more than knowing why. Mild dip: isolate fixes so you learn what worked.
3. Estimate the impact of each candidate fix honestly. Drop fixes too small to close the gap.
4. Apply a fix, not a rebuild. Example from source: conversion rate on the landing page caused the upstream issues, so apply a material change to the landing page.
5. Wait long enough to see if the fix worked before layering another. Source gives no window; card says it depends on conversion volume. [needs brand data: conversion volume to size the read window]
6. If fixes fail, or cannot bridge the gap to historical performance, then consider a rebuild.

### 3.11 Client call-out at the bottom (e.g. "CPC is down on this ad") [7c50191f8854] [26676d575992]

1. Do not start at the ad. Go to the top: has anything changed materially at the business level?
2. If business KPIs are up, a 10% ROAS decline on the 5th-biggest spender "probably doesn't matter at all". You may still troubleshoot it, after you know the severity.
3. Check channels: could something on another channel have hit this campaign? Example: a brand search campaign depends on demand created elsewhere.
4. Then campaign type, then campaign, then the sub-metric the client named. Decide whether it connects to the top. Source says 5 to 10 minutes of top-down work tells you if it is worth an hour.

## 4. Rules, thresholds and numbers

| Rule | Number or threshold | Condition | Source's basis | Card |
|---|---|---|---|---|
| Recent days look bad on default columns | Last 3 to 4 days (sometimes last 7) | Default Google conversion columns (credited to click date) | Presenter: happens "in every single account" | [62403f6f3b48] |
| Level 1 duration | About 5 minutes | Skilled operator | Presenter's expectation | [7fe2bb1f5bff] |
| Google unlikely cause | Google at 10% of spend (90% Meta) | Top-line revenue dip | Presenter example | [7fe2bb1f5bff] |
| Brand share of small Google spend | "Probably half" of Google spend is brand | Example with Google at 10% | Presenter guess | [7fe2bb1f5bff] |
| Check both platforms, larger first | 65/35 split | Either direction | Presenter example | [7fe2bb1f5bff] |
| Most accounts are Meta-heavy | 80 to 90% of businesses the agency sees | Agency client and audit base | Presenter observation | [7fe2bb1f5bff] |
| Google usually not the cause | Google at 20 to 30% of spend | Most businesses | Presenter opinion | [7fe2bb1f5bff] |
| Revenue equation | Revenue = CVR x AOV x Sessions | Business level | Formula | [7fe2bb1f5bff] |
| Diagnose only top campaigns | Top 5 by spend | Material business decline | Presenter heuristic | [26676d575992] |
| Small campaign impact | 10% of budget doubling = about 5% account impact; single digits if Google is 40% of mix | Illustrative | Presenter arithmetic example | [26676d575992] |
| Account scan window | 90 to 180 days, weekly view | Start of Google drill | Presenter method | [31ee29611482] |
| Account scan duration | About 5 minutes | Experienced operator | Presenter expectation | [31ee29611482] |
| ROAS | Conversion value / cost | Google Ads | Definition | [31ee29611482] |
| PMax share from Shopping | 80 to 90% of PMax performance | Ecommerce | Presenter claim, no data | [4e3675b7a020] |
| Stock-out example | Product with 15% of PMax spend out of stock 4 days | Resets that product's learning and hurts campaign | Presenter example | [4e3675b7a020] |
| Core formulas coverage | 2 formulas cover about 90% of cases | CPA = CPC / CVR; Clicks = Impr x CTR | Presenter estimate | [2069300bf455] |
| Sub-metrics and fixes | About 20 sub-metrics, about 100 fixes each | Why the source gives no fix list | Presenter estimate | [5df8489778d1] |
| CPC judgement | CPC up + CVR up = fine; CPC up + CVR flat = problem | Any platform | Presenter reasoning | [6ff74a04932d] |
| Landing page experience recovery | Weeks to months after site fix | Google rescan cadence unknown | Presenter's own case | [6ff74a04932d] |
| Budget-limited impressions | Example $100 a day budget being hit | Hitting budget | Presenter example | [2795573cf2d6] |
| Bid-limited impressions | Clicks and impressions both down | Spend steady | Presenter: "almost guarantee" | [2795573cf2d6] |
| Competitor discount that triggers pulling a product | 20 to 30% off (CTR example uses 20%) | Same products on Shopping | 1 client example | [caf9cb9b298e] |
| Client call-out worth time | 5 to 10 minutes top-down before spending an hour | Bottom-level metric flagged | Presenter practice | [7c50191f8854] |

## 5. Diagnostics and checks

| Check | How | Good | Bad | Next |
|---|---|---|---|---|
| Recent changes | Change history in Google, Meta, TikTok; ask client | No unexplained changes | Recent tweaks by anyone | Treat the change as the likely cause; do not stack new changes [62403f6f3b48] |
| Sample size | Date range vs conversion volume | Range long enough to show a trend | 1-day read | Zoom out [62403f6f3b48] |
| Latency | Conversions by conversion time vs default columns | Recent days match on conversion time | Recent dip only on default columns | No action; it is lag [62403f6f3b48] |
| Is it Google? | Spend share by platform; other-channel changes | Google is the larger spender and nothing else changed | Google is a small share, or Meta, offer, sale or site changed | Diagnose the other cause first [7fe2bb1f5bff] |
| Which lever | Revenue = CVR x AOV x Sessions | One lever clearly moved | Unclear | CVR: website. Sessions: traffic source. AOV: product mix, upsell [7fe2bb1f5bff] |
| Real or attributed | Business revenue, MER, aMER vs platform numbers | Business KPI and platform move together | Platform down, business flat (or reverse) | Suspect tracking or attribution [7fe2bb1f5bff] |
| Seasonality | Actual vs forecast | Dip inside forecast | Dip outside forecast | Inside: stop. Outside: continue [e2a87175fcd5] |
| Where in Google | 90 to 180 days weekly; top 5 campaigns; ad or asset groups | 1 or 2 campaigns show a clear inflection date | All flat | Record campaign type and groups [31ee29611482] |
| PMax drift | Search terms (brand), audience report | No brand terms, cold skew | Brand terms or existing-customer skew | Fix brand exclusion or lower tROAS [4e3675b7a020] |
| Feed | Products in campaign, GMC | Top products in stock, approved | Out of stock, off, disapproved, errors, changed titles | Fix feed items [4e3675b7a020] |
| tROAS effect | NC ROAS vs tROAS level | NC ROAS holds | NC ROAS weak with high tROAS, spend pulled back | Consider lower tROAS [4e3675b7a020] |
| Search term shift | Before vs after, sorted by spend | Same top terms, same efficiency | Spend moved to new terms | Address the reallocation [141c23b0306c] |
| Competition | Auction insights before vs after | Same competitors | New entrant | Feeds CPC and IS lost to rank work [6ff74a04932d] |
| Display leakage | Search campaign network setting | Display off | Display on and taking spend | Turn off display [141c23b0306c] |
| Search partners | Segment by network | Small or efficient | Large and poor | Review (source rates this low priority) [4e3675b7a020] |
| Quality Score | QS, Expected CTR, Ad relevance, LP experience columns | Unchanged | One dropped after inflection | Fix that component [6ff74a04932d] |
| CPC vs CVR | Both trends | Move together | CPC up, CVR flat | QS, competition or premium auctions [6ff74a04932d] |
| CVR drop | Tracking, landing page, audience, learning, offer | None changed | One changed | Fix that one [86ca17cab286] |
| Impressions | IS lost to budget vs rank | Not limited | Hitting budget, or both clicks and impressions down | Budget: raise spend. Rank: QS, competition, aggressiveness [2795573cf2d6] |
| CTR | Copy timing, audience, competitor prices | Stable | Stale seasonal copy, audience shift, competitor sale | Update copy, check audience, pull or de-prioritise product [2795573cf2d6] [caf9cb9b298e] |
| Action gate | Root-cause sentence | Can finish it | Cannot | Do not touch the account [7c50191f8854] |

## 6. Tools, settings and named features

- **Change history** (Google Ads, Meta, TikTok): see who changed what before diagnosing. [verify UI] [62403f6f3b48]
- **Conversions by conversion time** (custom column): credits the purchase date for a real read on recent days. [verify UI] [62403f6f3b48]
- **Overview tab, weekly view, 90 to 180 days**: fast trend scan across cost, conversions, conversion value, cost per conversion, ROAS, CTR. [verify UI] [31ee29611482]
- **Campaigns tab sorted by cost descending**, then ad groups or PMax asset groups. [verify UI] [31ee29611482]
- **Search term report** (Search, PMax): spend shifts and brand leakage. [verify UI] [141c23b0306c] [4e3675b7a020]
- **Audience report** (PMax): skew toward existing customers. [verify UI] [4e3675b7a020]
- **Brand exclusion** (PMax): should already be in place; double-check it is working. [verify UI] [web check: current PMax brand exclusion options] [4e3675b7a020]
- **Google Merchant Center (GMC)**: feed errors, warnings, disapprovals, stock, title and description changes. [verify UI] [4e3675b7a020]
- **Target ROAS (tROAS)**: bidding target; higher values narrow targeting. [4e3675b7a020]
- **Auction insights**: new competitors before vs after the dip. [verify UI] [141c23b0306c] [6ff74a04932d]
- **Display Network setting** on Search campaigns: should be off. [verify UI] [141c23b0306c]
- **Search partners**: check spend and performance. [verify UI] [4e3675b7a020]
- **Keyword columns**: Quality Score, Expected CTR, Ad relevance, Landing page experience. [verify UI] [6ff74a04932d]
- **Search impression share lost to budget and to rank** columns. [verify UI] [2795573cf2d6] [caf9cb9b298e]
- **New-customer ROAS**: via Triple Whale or other third-party tool, or natively in Google Ads. [web check: native new-customer metrics in Google Ads] [4e3675b7a020]
- **Competitor price-monitoring script**: real-time watch of a competitor's website prices, used to pull or de-prioritise products. Source does not share the script or say how it was built. [caf9cb9b298e]
- **Forecast**: expected revenue by period to rule out seasonality. Source does not say how to build it. [e2a87175fcd5]

## 7. Examples and case results

- **Example, media mix:** 90% Meta and 10% Google (about half brand, so about 5% new-customer acquisition via Google). A revenue dip is probably Meta. [7fe2bb1f5bff]
- **Example, small campaign arithmetic:** a campaign with 10% of budget that doubles performance moves the account about 5%; if Google is 40% of media mix, the business impact is single digits. [26676d575992]
- **Example, stock churn:** a product holding 15% of PMax spend out of stock for 4 days resets its own learning and affects the campaign. The agency's client onboarding video asks clients to say if products go in and out of stock often, because it may change account structure. [4e3675b7a020]
- **Case, landing page experience (presenter's own):** landing page experience was the bottleneck and caused a dip; after fixing the site, Google took weeks, if not months, to rescan and rescore. No numbers given. [6ff74a04932d]
- **Case, sunglasses wholesaler (1 client):** product-level performance dropped each time its biggest competitor put that product on sale on Google Shopping (20 to 30% price cuts). The agency set up a real-time script to track the competitor's prices and pulled or de-prioritised the product as soon as the competitor discounted, rather than match and erode gross margin "to almost nothing". No before and after numbers. Card adds: reintroduce the product when the price gap closes (the transcript does not say this). [caf9cb9b298e]
- **Example, CTR:** a competitor puts the same shoes on 20% off; searchers for "Nike shoes" click the cheaper listing. [2795573cf2d6]
- **Example, client call-out:** 10% ROAS decline on the 5th-biggest spending campaign while business KPIs are up probably does not matter. [7c50191f8854]
- **Example, Meta ROAS:** Meta attributed ROAS going from 4 to 3 as a correlation check against a revenue dip. [7fe2bb1f5bff]

## 8. Mistakes the source warns about

1. Making a change that makes things worse; not changing when you should; changing Google when the dip came from elsewhere. [7c50191f8854]
2. Auditing or changing right after a batch of changes, or without knowing what the client or teammates changed. [62403f6f3b48]
3. Diagnosing from a 1-day window (small-sample bias). [62403f6f3b48]
4. Panicking over the last 3 days on default conversion columns. [62403f6f3b48]
5. Troubleshooting Google when it is a small share of spend. [7fe2bb1f5bff]
6. Treating the diagnosis of other channels as a 2-second step. [7fe2bb1f5bff]
7. Running a 5-hour diagnostic on a seasonal dip because there is no forecast. [e2a87175fcd5]
8. Spending time on campaigns below the top 5 by spend. [26676d575992]
9. Raising tROAS expecting better efficiency; it narrows to warm buyers and hurts new-customer acquisition. [4e3675b7a020]
10. Letting high-spend products go in and out of stock in a shared campaign. [4e3675b7a020]
11. Leaving display on in a Search campaign. [141c23b0306c]
12. Stopping at a surface answer ("what offer changed?") instead of drilling into NC AOV, the distribution curve, then UPT or AUR. [2069300bf455]
13. Treating a CPC rise as a problem when conversion rate rose too. [6ff74a04932d]
14. Matching competitor discounts into near-zero margin. [caf9cb9b298e]
15. Rebuilding or making big structural changes, which resets learning and can start a decline loop. [5df8489778d1] [86ca17cab286]
16. Throwing the kitchen sink at a mild dip, so you never learn what worked. [817f1a421116]
17. Overrating a small fix (such as a headline change). [5df8489778d1]
18. Starting at the bottom metric a client names instead of the business top. [7c50191f8854]
19. Tweaking constantly: "they see a number drop and they reach for a setting". [7c50191f8854]

## 9. Caveats, conflicts and what is missing

- **Single presenter, agency sales video.** All thresholds (top 5, 80 to 90% from Shopping, 90% coverage, 5 minutes) are opinion or illustration, not tested benchmarks. [26676d575992] [4e3675b7a020] [2069300bf455]
- **Fixes are not given.** Source says about 20 sub-metrics with about 100 fixes each depend on the business. The method finds the cause; it does not say how to fix most causes. [5df8489778d1]
- **No wait window.** "Allow enough time" to read a fix has no number. Card says it depends on conversion volume. [5df8489778d1] [817f1a421116]
- **No time-horizon number** in the pre-diagnosis rule beyond "zoom out" scaled to conversion volume; the account scan uses 90 to 180 days. [62403f6f3b48] [31ee29611482]
- **"Search impression share lost (rank)" as a pricing signal is doubtful.** The source places it as a side note after the competitor pricing case; the card maps it to competitor pricing. IS lost to rank reflects bid and ad rank, not price. Common practice checks price with Merchant Center price competitiveness data. Treat IS lost to rank as a general auction signal. [caf9cb9b298e] [web check: Merchant Center price competitiveness report]
- **Card adds a step the transcript does not give:** "reintroduce the product when the competitive discount ends". Reasonable, but not stated. [caf9cb9b298e]
- **Card lists search partners under PMax and Shopping**; the transcript raises it only under Shopping. [4e3675b7a020]
- **Pulling products vs matching price.** Common ecommerce advice often says to stay price-competitive or match. Source chooses to exit the auction to protect margin. Right for a reseller whose competitor sells the same product; less clear for own-brand products. [needs brand data: gross margin by product, whether products are sold by others]
- **"80 to 90% of PMax performance from Shopping"** is a claim with no data; PMax channel reporting may now let you check it. [web check: PMax channel performance report] [4e3675b7a020]
- **Ad fatigue "rare on Google"** is the presenter's view; he allows it on Search. [2795573cf2d6]
- **Learning phase "always" lowers conversion rate**: strong wording, no evidence given. [86ca17cab286]
- **Level numbering skips 6 and 7.** The transcript goes from levels 4 and 5 to level 8.
- **Seasonality rule depends on forecast quality.** A bad forecast can label a real decline as seasonal. Source does not say how to build the forecast (it is sold as an agency service). [e2a87175fcd5]
- **Budget vs bid inference assumes steady spend.** [2795573cf2d6]
- **Root-cause gate can be overridden** in a dire case (kitchen sink). The transcript says this for fixes; the card extends it to "business continuity". [7c50191f8854] [817f1a421116]
- **Fits with other sources:** matches 24-DEP source 03 on top-down diagnosis from business KPIs and on MER or aMER over platform ROAS. Source 03 also says do not tighten Google's attribution windows; this source does not discuss windows.

## 10. Card index

- [62403f6f3b48] Pre-diagnosis rules: change history, time horizon, conversion latency
- [7fe2bb1f5bff] Level-one business check: cross-channel spend weighting and the revenue equation
- [e2a87175fcd5] Check seasonality against a forecast before diagnosing
- [26676d575992] Prioritise diagnosis by spend: top-5 campaigns only
- [31ee29611482] 90–180 day weekly overview scan before drilling into campaigns
- [4e3675b7a020] Match failure modes to campaign type: PMax and Shopping
- [141c23b0306c] Search campaign failure modes: search terms, auction insights, display leakage
- [2069300bf455] Metric decomposition: build the formulas before you touch anything
- [6ff74a04932d] CPC troubleshooting: quality score, competition and premium auctions
- [86ca17cab286] Conversion-rate troubleshooting: tracking, landing page, audience, learning, offer
- [2795573cf2d6] Volume troubleshooting: clicks = impressions × CTR, budget vs bid share loss
- [caf9cb9b298e] Competitive pricing scripts: pull products rather than match discounts
- [5df8489778d1] Default to fixes, not rebuilds, and protect the learning phase
- [817f1a421116] Isolate one fix at a time to preserve causal learning
- [7c50191f8854] Root-cause sentence test: don't touch the account until you can complete it
