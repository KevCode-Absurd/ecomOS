# How To Scale Meta TOF Campaigns

source_id: 1ylnZFnlwBEhctSQ1WnU-xTiIJ_8I2V5t  |  folder: /24-DEP-ad-deployment (moved from /11-ADC-ad-copy-deployment)  |  cards: 7  |  words: 2121  |  type: transcript (short screen-share video, spoken)
credibility: An unnamed presenter who audits Meta ad accounts ("90% of ad accounts I look at"). Likely an agency or consultant; the transcript does not say what they sell. Evidence is 1 real Advantage+ scaling campaign shown on screen (1 ad, its audience and attribution breakdowns) plus 2 worked hypothetical examples (a lift-test calculation and an incremental-attribution factor). No test results, sample sizes or before-and-after numbers after the fix. The "90%" figure is the presenter's own observation, not a measured statistic. The description of how Meta's incremental attribution works is the presenter's belief ("I assume", "they don't obviously specify").
date signals: No year stated. Names Advantage+ scaling campaigns, the "compare attribution settings" column view, an "incremental attribution" setting that can be used for optimization, and Conversion Lift Tests under Experiments. The incremental attribution option dates it to Meta's recent attribution changes, so roughly 2025 or later. File last modified 21 Sep 2026. All menu names and setting options are time-sensitive. `[web check: current Meta attribution settings, including whether incremental attribution is still offered as an optimization setting and a comparison column]`
scope note: The header (written for old folder 11-ADC) puts account structure, budget distribution, scaling rules, attribution, ROAS targets, incrementality testing, CAC tolerance and first vs returning customer unit economics in scope. It routes creative formats, concepts and creative quality to 10-MCR, and Google Analytics reporting and MMM tools to 06-MEA. It says to skip general complaints about other agencies misreading data.

## 1. What this source is for

It helps an operator check whether a Meta Advantage+ top-of-funnel (TOF) scaling campaign is really acquiring new customers, or only looks good because of existing customers and view-through conversions. It gives a 2-step diagnostic (audience breakdown, then attribution breakdown), a 3-part fix (7-day click, exclude existing customers, measure top-line new-customer sales at SKU level), and an explanation of why Meta's incremental attribution setting is not the same as a Conversion Lift Test. Use it when CAC rises every time a brand scales while new-customer count stays flat.

## 2. Principles

1. **The top-spending ad with the best platform ROAS can be losing money on new customers.** In the example, the highest-spend ad showed 13x ROAS (12.84) but only about 5x on new audiences, and 1.71x on new audiences under incremental attribution. Condition: a TOF Advantage+ scaling campaign with no existing-customer restriction and 7-day click plus 1-day view optimization. Evidence: 1 account shown on screen. [8c6833a8cd30] [9759cdb709fb]

2. **High frequency on a TOF scaling ad is a red flag.** The presenter treats a "a little bit high" frequency as the first sign the ad is reaching people it has already reached (retargeting-style delivery). No frequency number is given. Card caveat: it is a flag to investigate with the audience breakdown, not proof. [8c6833a8cd30]

3. **Meta over-distributes spend to ads that do well on existing customers.** With no restriction, "about half the budget" in the example went to existing customers. The presenter's reading: Meta pushes spend there because ROAS on existing customers is good, not because the ad acquires new ones. [8c6833a8cd30] [cf3aa44a7de1]

4. **Optimizing on 7-day click plus 1-day view lets view-throughs pull spend.** The ad set in the example optimized on 7-day click, 1-day view. The presenter says this is "what is causing all of the spend to pull here": the ad wins on view-throughs, not on clicks or incrementality. So spend priorities follow "an inflated fake number", not commercial outcomes. [34a82c492fd6]

5. **Ad rankings in such an account cannot be trusted.** Because spend is not distributed by new-customer performance, a low-spend ad "might be the best performing ad on new audiences. We don't know." Condition: the ad set optimizes with view-through and has no existing-customer exclusion. [34a82c492fd6] [8c6833a8cd30]

6. **Bad rankings create a costly loop into creative.** Teams see the top ad, brief the creative team, strategist or external agency to "double down" on its concept or format, and spend operating money on a concept that was never validated on new customers. Do not brief more of a "winner" until the breakdowns confirm new-customer performance. [34a82c492fd6] [8c6833a8cd30]

7. **Rising CAC with flat new-customer acquisition on every scale-up points to setup, not creative.** The example brand had tried to scale many times over the last 2 years; each time CAC went up and new-customer acquisition stayed flat. The presenter's cause: the ad is "probably just retargeting, overattributing, or cannibalizing spend from ads that should be good top-of-funnel ads". The presenter calls this "pretty basic to fix". [9759cdb709fb]

8. **Use 7-day click optimization on all campaigns.** Reason: ad-level spend then follows conversions caused by a click. The presenter says "on all campaigns", not only cold ones. [de104cfb484c]

9. **Incremental attribution is an estimate. Use it as a breakout column, not for optimization or measurement.** Source says: Meta's incremental attribution applies a factor built from aggregated lift studies (the presenter assumes across all advertisers in a similar category) to your numbers. It is not a measurement of your own customers. "Our competitors might be very very different from us." Presenter's own position: "I don't really love optimizing a campaign towards an estimate." This is one presenter's opinion with a stated reason. [de104cfb484c]

10. **A Conversion Lift Test is the real incrementality measure.** Meta holds out a share of the target audience, compares purchase rates between held-out and served groups, and the gap is the true lift. The presenter calls this difference-in-difference design. Found under Experiments. Use it when you need to know real incremental impact. [de104cfb484c]

11. **Exclude existing customers from cold campaigns, but treat lapsed buyers as a separate case.** Someone who has not bought in 2 years is "kind of a lapsed customer", not an active one. "Maybe just a 2-year exclusion is good enough." Optionally give lapsed buyers their own campaign with its own strategy. [cf3aa44a7de1]

12. **Judge scaling on top-line revenue, ideally new-customer sales for the SKU being scaled.** In-platform ROAS is the number that misled you. A single-SKU readout is easier than store-wide totals, because store-wide needs a much longer test or a much bigger budget change to reach statistical relevance. The objective of an Advantage+ TOF scaling campaign is new customers, so narrow further to new-customer sales on that SKU. [b410bffcb50f]

## 3. Procedures

### 3.1 Diagnose a top-spending TOF ad (audience, then attribution)
Precondition: an Advantage+ TOF scaling campaign where the top-spend ad shows high platform ROAS. `[needs brand data: ad-level spend, frequency, ROAS, audience segment breakdown, attribution comparison columns]`
1. Open the campaign at ad level and find the highest-spend ad. Note its ROAS and frequency. Frequency that looks high is the first flag. [8c6833a8cd30]
2. Apply the audience breakdown that splits spend into existing customers, engaged, and new. `[verify UI]` Read the share of spend going to existing customers (example: about half). [8c6833a8cd30]
3. Read ROAS for the new-audience row only (example: dropped from 13x blended to about 5x). A large gap between blended and new-customer ROAS means spend is being pulled by existing-customer performance. [8c6833a8cd30]
4. Keep the same audience split and open Columns > Compare attribution settings. Add 7-day click and incremental attribution as columns. `[verify UI]` [8c6833a8cd30] [de104cfb484c]
5. Read the new-audience row under incremental attribution (example: 1.71x, against the 12.84x shown at the top line). [8c6833a8cd30]
6. Check the ad set's attribution setting. If it is 7-day click, 1-day view, treat all ad rankings in that ad set as untrustworthy. [34a82c492fd6]
7. Do not scale the ad or brief more creative like it until the fix in 3.2 is in place and rankings are re-read. [34a82c492fd6]

### 3.2 Fix the setup (the presenter's 3 basics)
1. Set 7-day click as the attribution setting for optimization on all campaigns, so view-throughs do not drive spend. `[verify UI]` [de104cfb484c]
2. Add incremental attribution only as a comparison column. Do not set it as the optimization target or use it as the measure of success. `[verify UI]` [de104cfb484c]
3. Exclude existing customers from every cold TOF scaling campaign. `[verify UI]` `[web check: how existing-customer exclusion or caps work in current Advantage+ sales campaigns]` [cf3aa44a7de1]
4. Set the "existing customer" window. Source's starting point: buyers in the last 2 years are excluded; buyers older than 2 years count as lapsed and may receive spend. `[needs brand data: repurchase cycle]` [cf3aa44a7de1]
5. Optional: put lapsed customers (for example, last bought over 2 years ago) in a dedicated campaign with its own strategy. [cf3aa44a7de1]
6. After the change, re-read ad rankings. Correcting attribution and exclusions changes which ads win spend (card step). [9759cdb709fb]

### 3.3 Measure whether scaling worked
1. Identify whether the scaled campaign or ad concentrates on 1 SKU (in the example, the top ad was a single SKU no other ad was selling). [b410bffcb50f]
2. When you raise budget or add that product to the campaign, check whether that SKU's sales rose. `[needs brand data: SKU-level daily sales from the store, before and after]` [b410bffcb50f]
3. Narrow to new-customer sales on that SKU, since the campaign's job is acquiring new customers. `[needs brand data: SKU sales split by new vs returning customer]` [b410bffcb50f]
4. If you can only read store-wide sales, expect to need a much longer test or a much larger budget change for the result to be meaningful. The source gives no duration or lift size. [b410bffcb50f]
5. Compare platform ROAS with the store-side movement. Divergence means the platform is overstating acquisition (card step). [b410bffcb50f]
6. Card addition, not in the source: confirm the SKU was not promoted elsewhere (email, other channels, sales) during the window. [b410bffcb50f]

### 3.4 Worked arithmetic: how a Conversion Lift Test reads (source's hypothetical)
1. Target 10,000 people a day. Meta holds out 10% of them. [de104cfb484c]
2. Held-out group purchase rate: 1%. Served group purchase rate: 2%. [de104cfb484c]
3. Lift = 2% minus 1% = 1 percentage point. [de104cfb484c]
4. Presenter's reading: if platform ROAS is 5x, true ROAS is "probably" about 2.5x once conversions that would have happened anyway are removed (half the served conversions were going to happen). [de104cfb484c]

### 3.5 First-pass audit when CAC rises and new customers stay flat (card's framing of the source)
1. Retargeting check: audience breakdown on the scaling campaign; how much spend goes to existing and engaged users. [9759cdb709fb]
2. Over-attribution check: compare 7-day click against 1-day view and incremental attribution on the same ads. [9759cdb709fb]
3. Cannibalization check: are cold campaigns absorbing audiences retargeting should serve? The source names cannibalization but does not say how to check it. [9759cdb709fb]
4. Fix structure first (3.2), then measure on SKU-level new-customer sales (3.3), then re-audit. [9759cdb709fb]

## 4. Rules, thresholds and numbers

| rule | number or threshold | condition | source's basis | card id |
|---|---|---|---|---|
| Optimization attribution setting | 7-day click (no view-through) | All campaigns, per presenter | Spend should follow click-caused conversions | de104cfb484c |
| Setting to avoid for optimization | 7-day click, 1-day view | TOF scaling ad sets | View-throughs pulled spend in the example | 34a82c492fd6 |
| Incremental attribution use | Breakout column only | Any campaign | It is a modelled estimate from other advertisers' studies | de104cfb484c |
| Existing-customer exclusion window | 2 years ("maybe just a 2-year exclusion is good enough") | Cold TOF scaling campaigns | Presenter heuristic; buyers older than 2 years treated as lapsed | cf3aa44a7de1 |
| Frequency flag | "A little bit high"; no number | Top-spend ad in a TOF scaling campaign | Presenter's red flag | 8c6833a8cd30 |
| Example: share of budget on existing customers | About 50% | 1 Advantage+ scaling campaign, no restriction | On-screen example | 8c6833a8cd30 |
| Example: blended ROAS vs new-audience ROAS | 13x (12.84) vs about 5x | Same ad | On-screen example | 8c6833a8cd30 |
| Example: new audience, incremental attribution | 1.71x | Same ad | On-screen example | 8c6833a8cd30 |
| Example lift test holdout | 10% of 10,000 people a day | Hypothetical | Explanation of Conversion Lift Test | de104cfb484c |
| Example lift | 2% served vs 1% holdout = 1 point lift; 5x ROAS becomes about 2.5x | Hypothetical | Explanation | de104cfb484c |
| Example incremental factor | 0.2x for retargeting, fashion for men 40 to 50; 10x ROAS becomes 2x | Hypothetical, presenter's assumption | Explanation of incremental attribution | de104cfb484c |
| Scaling readout scope | Single SKU, new-customer sales | When 1 SKU is being scaled, especially with a large SKU count | Store-wide needs longer test or bigger lift delta | b410bffcb50f |
| Accounts missing these basics | "90%" | Presenter's own audits | Opinion, not measured | 9759cdb709fb |

No ROAS target, CAC tolerance, budget increase size, test duration or frequency number is given. `[needs brand data: break-even new-customer ROAS and CAC target]`

## 5. Diagnostics and checks

| check | how | good | bad | next |
|---|---|---|---|---|
| Frequency on top-spend TOF ad | Ad-level report sorted by spend | Frequency normal for a cold campaign (no number given) | "A little bit high" | Run the audience breakdown |
| Spend to existing customers | Audience breakdown: existing, engaged, new `[verify UI]` | Little or no spend on existing (cold campaign) | Large share (example: about half) | Add existing-customer exclusion (3.2) |
| Blended vs new-audience ROAS | Same breakdown, ROAS column | Small gap | Large gap (example: 13x to 5x) | Do not scale or brief more of this ad yet |
| Attribution basis of ROAS | Compare attribution settings: 7-day click, 1-day view, incremental `[verify UI]` | ROAS holds on 7-day click for new audience | ROAS depends on view-through or collapses under incremental (example: 1.71x) | Switch optimization to 7-day click |
| Ad set optimization setting | Ad set attribution setting | 7-day click | 7-day click, 1-day view | Change it, then re-read rankings |
| Scaling pattern over time | CAC and new-customer count across past scale-ups `[needs brand data: CAC and new-customer count by period]` | New customers rise with spend | CAC rises, new customers flat | Run 3.1 and 3.2 before any creative conclusion |
| Scaling result | SKU sales, then new-customer SKU sales, before vs after the budget change `[needs brand data]` | SKU new-customer sales rise | No rise despite platform ROAS | Treat platform ROAS as overstated |
| Real incrementality | Conversion Lift Test in Experiments `[verify UI]` | Measured lift | Only incremental attribution column available | Run a lift test if the decision needs true incrementality |

Card addition (fe7d1d8bcc27), not in the source text: before applying these checks, confirm the campaign optimizes for purchases, not leads. The source only discusses purchase-based scaling campaigns and never mentions leads.

## 6. Tools, settings and named features

- **Advantage+ scaling campaign (TOF)**: the campaign type in the example. `[verify UI]` `[web check: current Advantage+ sales campaign name and existing-customer controls]` [8c6833a8cd30]
- **Audience breakdown (existing customers / engaged / new)**: breakdown that splits spend and results by customer segment. `[verify UI]` [8c6833a8cd30]
- **Columns > Compare attribution settings**: shows 7-day click, view-through and incremental attribution side by side. `[verify UI]` [8c6833a8cd30] [de104cfb484c]
- **Attribution setting "7-day click, 1-day view"**: the setting the example ad set optimized on. Source: avoid it for optimization. `[verify UI]` [34a82c492fd6]
- **Incremental attribution**: available both as an optimization option and a column, per the source. Use as column only. Method not disclosed by Meta. `[verify UI]` `[web check: how Meta says incremental attribution is modelled]` [de104cfb484c]
- **Conversion Lift Test (Experiments)**: holdout test that measures true lift. The presenter briefly calls it a "geo lift test" then corrects to "conversion lift test"; the described method is a user-level holdout, not a geo test. `[verify UI]` [de104cfb484c]
- **Customer exclusion audience**: existing customers excluded from cold campaigns, with a 2-year window. How to build it is not given. `[verify UI]` [cf3aa44a7de1]
- **Shopify** (named only on the card, not in the transcript): store-side SKU and new-customer sales. `[verify UI]` [b410bffcb50f]

## 7. Examples and case results

Examples only, from 1 account. Not benchmarks, not promises.
- Top-spend ad in an Advantage+ TOF scaling campaign: 12.84x (about 13x) ROAS, highest spender, frequency "a little bit high". About half its budget went to existing customers. New-audience ROAS about 5x. New-audience ROAS under incremental attribution 1.71x. [8c6833a8cd30]
- The same brand had scaled several times over the last 2 years; each time CAC rose and new-customer acquisition stayed flat. [9759cdb709fb]
- The top ad was a single SKU that no other ad in the campaign was selling, which made a SKU-level readout possible. The presenter says sales "might have gone up"; no confirmed lift or number is given. [b410bffcb50f]
- Hypothetical lift test: 10,000 people a day, 10% held out, 1% vs 2% purchase rate, 1 point lift, 5x ROAS read as about 2.5x. [de104cfb484c]
- Hypothetical incremental factor: fashion brand for men 40 to 50, retargeting factor 0.2x, 10x ROAS read as 2x. [de104cfb484c]

## 8. Mistakes the source warns about

1. Trusting the top-spend ad's platform ROAS without an audience and attribution breakdown. [8c6833a8cd30]
2. Briefing the creative team or agency to double down on the "winning" concept or format based on those numbers, which adds operating cost against bad data. [34a82c492fd6]
3. Optimizing on 7-day click, 1-day view, so view-throughs decide where spend goes. [34a82c492fd6]
4. Leaving existing customers unrestricted in cold scaling campaigns, so spend flows to whichever ads do best on existing customers, "inclusive of viewers". [cf3aa44a7de1]
5. Optimizing toward, or measuring success with, incremental attribution, which is an estimate built on other advertisers' data. [de104cfb484c]
6. Confusing incremental attribution with a Conversion Lift Test. [de104cfb484c]
7. Judging scaling on in-platform ROAS instead of top-line revenue and new-customer SKU sales. [b410bffcb50f]
8. Reading scaling on store-wide sales with too short a test or too small a budget change to see a real effect. [b410bffcb50f]

## 9. Caveats, conflicts and what is missing

- **Single account, no after-fix result.** The source never shows what happened after switching to 7-day click and excluding customers. The fix is reasoning, not a tested remedy. [9759cdb709fb]
- **Incremental attribution explanation is the presenter's guess.** "I assume", "they don't obviously specify". `[web check: Meta's documentation on incremental attribution]` [de104cfb484c]
- **Lift test terms are loose.** The transcript first says "geo lift test", then corrects to "conversion lift test", and calls a simple holdout comparison "difference-in-difference". The card header calls it a "geo-holdout". The described method is a user-level holdout. Treat the arithmetic as illustrative. [de104cfb484c]
- **"7-day click on all campaigns"** is stated as universal, including non-cold campaigns. The source gives no condition where 1-day view is acceptable. The card notes view-throughs are not worthless; the argument is that they should not drive optimization in cold acquisition. [34a82c492fd6]
- **2-year exclusion is a heuristic.** The presenter hedges ("maybe"). Cards add: set the window to the brand's repurchase cycle; short-cycle categories may need a shorter window. `[needs brand data: repurchase cycle]` [cf3aa44a7de1]
- **Missing how-to:** no steps to build the exclusion audience, no mention of Advantage+ controls for existing customers, no frequency threshold, no budget step size for scaling, no test duration, no significance method, no way to check cannibalization, no ROAS or CAC target.
- **Card additions beyond the transcript:** the lead vs purchase card (fe7d1d8bcc27) is not in the source at all, including its claim that changing the conversion event resets learning. The "check no other promotion ran on the SKU" step (b410bffcb50f), the "cold outbidding retargeting" framing of cannibalization (9759cdb709fb) and the Shopify name are card inferences. Use them as sensible checks, not as this source's claims.
- **Conflict with common advice:** much common Meta guidance keeps the default 7-day click, 1-day view setting and lets Advantage+ include existing customers under a cap. This source rejects both for TOF scaling. It also runs against advice to use incremental attribution for optimization. Keep this as one presenter's position. `[web check: current Meta defaults and recommendations for attribution and existing customers in Advantage+]`
- **Neighbour folders:** creative quality and concepts belong in 10-MCR; GA and MMM tools belong in 06-MEA.

## 10. Card index

- 8c6833a8cd30: Diagnose inflated ROAS in Advantage+ scaling campaigns with audience breakdowns
- de104cfb484c: Use 7-day click for optimization and treat incremental attribution as a breakout only
- cf3aa44a7de1: Exclude existing customers from cold TOF campaigns, with a lapsed-customer carve-out
- b410bffcb50f: Measure scaling lift on top-line new-customer sales at the SKU level
- 34a82c492fd6: Why optimizing on 1-day view-through inflates rankings and misallocates spend
- fe7d1d8bcc27: Read purchase conversion separately from lead conversion when auditing a scaling campaign (card content not found in source text)
- 9759cdb709fb: Diagnostic path when CAC rises on every scaling attempt and new customers stay flat
