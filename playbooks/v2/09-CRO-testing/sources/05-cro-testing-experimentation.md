# CRO as testing and experimentation for DTC ecommerce

source_id: 1-erJBJ6iVbCFgrxQ0SjuTi9kbLRL2jmF  |  folder: /09-CRO-testing  |  cards: 19  |  words: 7065  |  type: article (synthesised research document with a source list)
credibility: An unnamed, synthesised research brief in 3 parts: Part A (research), Part B (a stage-gated guide by monthly orders), Part C (a tiered source list with rejected sources). It checks 4 claims from an earlier "internal doc". It is not first-hand practice. Its strength is that almost every statistical claim is tied to a named primary source: Kohavi, Tang and Xu (Trustworthy Online Controlled Experiments, 2020), Evan Miller (2010, 2015), Johari et al. (always-valid inference), Spotify, Etsy and LinkedIn engineering, the CUPED paper (Microsoft 2013), Baymard, plus vendor docs (Optimizely, VWO, GrowthBook, AB Tasty, DebugBear). Win-rate figures from agencies (DRIP, ConversionTeam) are labelled tier 3. It sells nothing. The order-volume bands in Part B are the author's own synthesis, not from a study.
date signals: Written 2025 to 2026. Cites Molas (30 Oct 2025), Baymard (updated 22 Sep 2025), DebugBear (updated Dec 2025), Atticus Li (Mar 2026), Shopify checkout extensibility rollout (Aug 2024), Google Optimize sunset (30 Sep 2023). The author flags the Shopify checkout position "as of late 2025" and says to re-verify it yearly. Vendor free tiers (VWO 50,000 tested users per month, Statsig 1M events per month) are time-sensitive.
scope note: The document header labels it module 06-MEA, but it is filed in 09-CRO. The author defines CRO here as "is the difference real" (statistics, experiment design, discipline). Page design belongs to 07-LPG (in this document's own words, "LPG"), tracking accuracy to 06-MEA except where broken tracking invalidates a test. Ad metrics go to 11-ADC, finance to 20-FIN. The header says to skip "magic conversion number" claims that ignore MDE math.

## 1. What this source is for

It is the statistics and discipline manual for running A/B tests on a DTC store. Use it to decide whether something should be fixed or tested, to size a test, to set runtime and stopping rules, to pick the primary metric and guardrails, to check whether a result is valid, to read the result honestly, and to decide which testing methods a store can use at its order volume. It also covers Shopify-specific limits (checkout, Rollouts), price-testing ethics and the tool landscape.

## 2. Principles

1. **Repair broken things; test only real uncertainty.** If the current state is objectively defective (loses money with no upside, breaks a known standard, or is literally broken), fix it and move on. Examples: page errors, a form field that rejects valid input, add to cart failing on Safari, tracking firing twice. Do not run a test to decide whether to fix a bug. Test when both versions are plausibly viable and you do not know which is better. Basis: Kohavi's framing that experiments are for hypotheses with genuinely uncertain outcomes. Also log repairs so they are not re-proposed as hypotheses. [3eca46fe9ba3]

2. **Sample size is driven by the minimum detectable effect (MDE), not by a magic conversion count.** Evan Miller's rule: n = 16 x sigma^2 / delta^2 per variant, where delta is the absolute effect and, for a conversion rate, sigma^2 = p(1-p). The 16 bakes in alpha 0.05 two-sided and 80% power. Halving the effect you want to detect quadruples the sample. Set MDE to the smallest lift worth shipping, not the smallest possible. [00c82f0de25d]

3. **Most DTC micro-tweaks cannot be detected.** At a 2% baseline, a 10% relative lift needs about 80,000 visitors per variant (160,000 total). A 20% lift needs about 21,000 per variant. A 5% lift needs 315,000 per variant, which "most brands will never reach in a reasonable window". The author calls this "the central fact of the whole module". [00c82f0de25d] [0bda3b4d7e04]

4. **Think in conversions per variant.** At fixed power, the conversions needed per variant depend mainly on the relative MDE, not the baseline: about 3,830 for 5%, about 1,000 for 10%, about 260 for 20%, about 120 for 30% (80% power, 95% confidence). [00c82f0de25d]

5. **Two-tailed is the default.** One-tailed reaches significance faster but only tests one direction. Use it only when a negative result would trigger the same action as a null (keep control either way). Document this before launch and recompute sample size, since standard tables assume two-sided. It is not a shortcut to hide downside. Most store changes can plausibly hurt conversion, AOV, margin or experience, so two-tailed is more defensible. [517a8bce6324]

6. **A p-value is valid only under its planned stopping rule. Do not peek.** Fixed-horizon testing means: fix sample size in advance, look once at the end. Stopping at the first p < 0.05 while checking continuously inflates false positives badly. Either analyse once at the planned sample, or use a validated sequential method. [e3ee87a025c5]

7. **Sequential methods make early looks legitimate, at a cost.** mSPRT always-valid p-values (Johari et al.; used by Optimizely, Uber, Netflix, Amplitude), GAVI confidence sequences (Howard et al. 2021; Eppo), group sequential design with alpha spending (Lan-DeMets 1983; Spotify), corrected-alpha (Statsig). Always-valid methods let you stop any time but cost power (wider intervals) compared with a correctly sized fixed test. Spotify's guidance: if you can estimate expected sample size well, group sequential is more powerful; if not, always-valid is safer. [e3ee87a025c5]

8. **Bayesian is not immune to peeking.** A fixed posterior threshold does not control error under optional stopping. And most commercial "Bayesian" tools use flat priors, which makes them close to frequentist but less transparent. If you cannot state the prior, you cannot fully interpret or reproduce the result. [e3ee87a025c5]

9. **Run at least 1 full week, in practice 2, and also reach the planned sample.** Weekends convert differently from weekdays and buyers differ by day. 2 weeks captures one full cycle of returning visitors (Kohavi). Hitting significance early is not a reason to stop. Two weeks is a minimum, not a replacement for sample-size math. [5fae1beab1ba]

10. **Check novelty and primacy with daily plots, but be sceptical.** Novelty: a temporary bump because the change is new, which decays. Primacy: returning users are used to the old design, so the new one dips then recovers. Diagnose by plotting daily effect and comparing first-exposure vs repeat-exposure conversion. Kohavi found most suspected novelty or primacy effects are statistical artifacts of noisy early cumulative deltas. [5fae1beab1ba]

11. **Below the A/B threshold, the job changes from proving to learning. "Test bigger, not more."** Bold changes aimed at 10 to 20%+ effects; test on the highest-traffic pages; lean on qualitative research; re-test surprising big winners with a holdout. One bold homepage test teaches more than 10 micro-tests on low-traffic category pages (SplitBase). [67f74e89d43e]

12. **Before/after tests are biased, not just noisy.** Pre-post uses all traffic on one version at a time, but confounds the change with time: seasonality, promotions, weekday mix, traffic-source shifts, news. The author corrects the internal claim that it "works if you accept wider error bars": the real problem is bias. Use only for big structural changes where the effect dwarfs noise, with equal comparable periods and conditions held constant. Treat a clear, stable, explainable shift as weak evidence and confirm later with a randomised test. [062507c94ee4]

13. **Micro-conversions power faster but may not carry to purchase.** Add to cart or begin checkout as primary metric is fine as a leading indicator only if purchase and revenue stay as guardrails. [67f74e89d43e] [1b7725e0ff57]

14. **Frequentist and Bayesian each have a place.** Frequentist: explicit error-rate contract, forces upfront MDE and sample discipline, reproducible (a z-test is a z-test); but p-values are misread, the 0.05 cliff is artificial, fixed samples are rigid and peeking silently breaks it. Bayesian: gives "probability B beats A" and expected loss, intuitive, credible intervals mean what people think; but priors are subjective and usually hidden, and "probability to be best" can mislead without a loss function. [e3ee87a025c5]

15. **Check validity before trusting any lift.** Sample ratio mismatch, flicker, bots, tracking breakage, overlapping promotions, multiple comparisons, segment fishing, early stopping and novelty can all fake a result. [370ed8c02e34] [1f26cd618e2d]

16. **Twyman's law: a surprising number is usually wrong.** A 364% lift is more likely an instrumentation bug, SRM or contamination than a discovery (Kohavi). The author calls this "the anchor rule for auditing case studies". Vendor case studies without sample, duration and baseline are hypothesis material only. [370ed8c02e34]

17. **CUPED helps less on anonymous DTC traffic.** CUPED uses pre-experiment data for the same user as a covariate, keeping the estimate unbiased but lowering variance. Vendors claim 30 to 50% lower sample needs for metrics strongly tied to past behaviour. But it needs logged-in users or stable device IDs. For DTC brands with mostly new, anonymous checkout traffic, the covariate is missing or weak. LinkedIn found only 15.91% variance reduction on n = 400,000 for volatile revenue. Verdict: turn it on if your platform offers it and you have returning identified users; it is not a magic fix. Simpler aids: use a proportion metric instead of a raw revenue mean, and winsorize outlier orders. [0bda3b4d7e04] [7eeb62d20124]

18. **A/B tests for durable decisions; bandits for short tactical ones.** A/B: explore then exploit; best for a clean causal read before a lasting change (redesign, pricing, navigation, checkout). Bandit (Thompson sampling, UCB): shifts traffic to the better arm in real time; best when showing the loser is costly and the window is short (headlines, seasonal promos, banner creative, recommendations). Bandits minimise regret, not estimate effects, and give less certainty on losing arms and a narrower KPI focus. Hybrid is the common ecommerce pattern. Bandits need sticky bucketing so returning users stay on one arm. [3b20905bfc58]

19. **A/B/n needs the full per-variant sample for every arm.** Total traffic scales with the number of arms. A brand under a few thousand orders per month cannot power 3 to 4 variants at a useful MDE. Do not add arms just to test more ideas at once. [3b20905bfc58]

20. **Prioritise by expected profit, not expected lift.** Expected value = P(win) x expected lift x value per conversion x traffic exposed, minus build cost. A 20% lift on a low-margin, low-traffic page can be worth less than a 5% lift on the checkout of the hero product. Weight by gross profit per conversion, not revenue, because a lift that shifts mix toward low-margin SKUs can raise revenue and cut profit. Require at least 2 points of evidence before a test enters the backlog (PXL-style gating). [aad25dea9ed9]

21. **Research produces hypotheses, not tests.** Each method answers a different question (section 3.3). DRIP reports a 36.3% win rate because it pre-qualifies every hypothesis with analytics, recordings and heatmaps; teams that test without research see lower win rates. [f856d689f3d8]

22. **Pick the primary metric by the decision and the traffic.** Conversion rate is binary, low variance and fastest, but ignores order value. Revenue per visitor captures both but is highly skewed and needs about 6x the traffic. Gross profit per visitor is "the honest objective for a DTC brand" but has the same variance problem plus needs margin data. [7eeb62d20124]

23. **Guardrails must not get worse even when the primary improves.** AOV, return rate, refund rate, page load, add to cart, margin. "A conversion win that tanks AOV or margin is not a win." [1f26cd618e2d] [7eeb62d20124]

24. **Pre-register segments; do not fish.** Mobile and desktop can move in opposite directions, so a blended win can hide a mobile loss. Pre-register device, paid vs organic, new vs returning. Slicing after the fact until a winner appears is p-hacking. Post-hoc slices only seed new tests. [1f26cd618e2d]

25. **Confidence intervals over p-values; practical over statistical significance.** Report the interval. Decide against the MDE and business value. "Significant" does not mean 95% likely real: if only 10% of ideas truly work and you test at 80% power, roughly 1 in 5 significant wins is a false positive. [70db51ffb976]

26. **A fully powered inconclusive test is a result.** It is evidence the effect is smaller than your MDE. Do not extend it to chase significance (that is peeking). Ship neither or the cheaper, simpler version, and move on. Kohavi: little value in extending a test that is significantly negative after 2 weeks; fail fast. [70db51ffb976]

27. **Keep an experiment log.** Institutional memory stops re-running losers and flags surprising winners for replication. At Booking.com scale (1,000+ concurrent experiments) "the bottleneck is not running tests but not fooling yourself with them". [70db51ffb976]

28. **Expect most tests to fail.** The best-sourced anchor: about 10 to 20% of well-run tests produce a significant winner. Always carry the definition and sample with any win rate. [8dc46d4893e1]

29. **Shopify checkout cannot be A/B tested client-side on standard plans.** Since checkout extensibility replaced checkout.liquid (general rollout August 2024), JavaScript injection into checkout is gone, and Shopify's developer forum confirms there is no built-in way to show a checkout customisation to one group and hide it from another. About 80% of high-impact ecommerce tests happen before checkout anyway. `[verify UI]` `[web check: current Shopify checkout extensibility and A/B testing options, yearly]` [7c932a3b4986]

30. **Client-side for front-end visuals; server-side for checkout, pricing logic and speed-sensitive paths.** Client-side: marketer-owned, visual editor, fast; but flicker, extra JS, slower pages, easier to break, logic is public. AB Tasty says flicker comes from how client-side tools work and there is "no miracle fix". Server-side: no flicker, faster, robust, can test backend logic (pricing, search, recommendations, checkout), works with feature flags; but needs engineers, a deploy cycle, higher cost, slower to ship. [7c932a3b4986]

31. **Do not test different prices for the same SKU at the same time.** Legal in the US and EU if not based on protected characteristics (nationality, gender, race), which is illegal negative price discrimination. The EU requires disclosure when a price is personalised. Even where legal it is "an ethics and brand landmine". Test price presentation, framing, tiers and bundles, or different offerings at different prices, instead. [34fa165a64fe]

## 3. Procedures

### 3.1 Decide: repair or test
1. Ask: is the current state objectively defective (errors, rejects valid input, browser-specific failure, double-firing tracking, violates a known standard, loses money with no upside)?
2. If yes: repair it, log the repair, move on. Do not randomise shoppers onto a broken experience to prove it hurts.
3. If both versions are plausible and the better one is unknown: go to test design.
4. If tracking breaks during a test, invalidate the read. [3eca46fe9ba3]

### 3.2 Size a test
1. Get the baseline conversion rate of the page and metric. `[needs brand data: baseline conversion rate per page and device]`
2. Set the MDE to the smallest lift worth shipping (think in gross profit).
3. Check whether the calculator wants relative or absolute MDE. Example: 2% to 2.4% is +0.4 points absolute, +20% relative.
4. Use alpha 0.05, power 0.80, two-sided unless the one-tailed condition in principle 5 holds.
5. Compute n per variant (Miller: 16 x p(1-p) / delta^2), or use the table in section 4, or a calculator such as Evan Miller's.
6. Multiply by the number of arms for total traffic.
7. Divide by weekly eligible traffic to get runtime. `[needs brand data: weekly sessions on the tested page]`
8. Round runtime up to whole weeks, at least 1 and in practice 2.
9. If the runtime is unreasonable, raise the MDE (bolder change), move to a higher-traffic page, switch to a faster primary metric with purchase as guardrail, or drop to research-only. [00c82f0de25d] [5fae1beab1ba] [67f74e89d43e]

### 3.3 Generate hypotheses with research (method only; page design output belongs in 07-LPG)
1. **Analytics funnel (GA4, Shopify):** find the step with the biggest drop and the most traffic. Tells you where to test.
2. **Session replay:** rage clicks, dead clicks, loops, form abandonment. Tells you what is confusing.
3. **Heatmaps and scroll maps:** what gets attention and what is missed. Feeds placement and reach hypotheses. Weight by revenue per click, not raw clicks.
4. **On-site surveys (exit intent, post-purchase):** why people did not buy or almost did not. Feeds objections.
5. **User testing:** watch 5 to 8 people attempt a task and narrate. Feeds usability problems.
6. **Customer interviews:** motivation, anxiety, and the words customers use. Feeds messaging hypotheses.
7. Output: a prioritised, evidence-backed hypothesis with at least 2 points of evidence. [f856d689f3d8] [aad25dea9ed9]

### 3.4 Write the test brief (pre-registration)
1. Hypothesis: "Because we observed [evidence], we believe [change] will cause [effect] for [segment], measured by [primary metric]. We will know it worked if [metric moves by MDE]."
2. One primary decision metric (conversion rate, RPV, or gross profit per visitor).
3. MDE, planned sample, planned dates.
4. Guardrails with thresholds: AOV, margin, return rate, refund rate, page load, add to cart, downstream purchase.
5. Pre-registered segments: device, paid vs organic, new vs returning.
6. Tails (two-sided default) and the stopping method (fixed horizon, or which sequential method).
7. Runtime: at least 1 full week, usually 2, plus time to reach sample.
8. Validity plan: SRM check, tracking QA, flicker check.
9. Action for win, loss and inconclusive. [1b7725e0ff57] [1f26cd618e2d]

### 3.5 Run and monitor
1. Launch with the planned split.
2. Check SRM early and often (chi-square on users, not page views). Flag at p < 0.001 (Kameleoon's threshold). If present, stop trusting the result until the cause is found.
3. Check tracking fires correctly in both arms.
4. Filter bots.
5. Watch for promotions, holidays or traffic-mix shifts overlapping the test.
6. If using a fixed-horizon test, do not act on interim significance.
7. If using a sequential engine, follow its stopping rule only. [370ed8c02e34] [e3ee87a025c5]

### 3.6 Audit a result or a case study
1. SRM: chi-square goodness-of-fit on the randomisation unit.
2. Flicker: in client-side tests, did the original render before the variant? Flicker can both hurt UX and inflate the effect by drawing the eye.
3. Tracking: did any pixel or event break mid-test?
4. Bots filtered?
5. Seasonality or promos overlapping?
6. Metric count: how many metrics and segments were read? Apply Bonferroni or FDR.
7. Twyman's law: is the lift implausibly large? If 50%+ or hundreds of percent, hunt for bugs, SRM, contamination, bot skew, tracking failure, overlapping promotions before celebrating.
8. For a case study: does it state baseline, sample, runtime and validity checks? If not, it is hypothesis material only. [370ed8c02e34] [8dc46d4893e1]

### 3.7 Read and decide
1. Report the effect with its confidence interval.
2. Compare to the MDE and to incremental gross profit, build cost, and guardrails.
3. Plot the daily effect; compare first vs repeat exposure if novelty is suspected.
4. Win: ship, and if the lift is surprising and large, replicate or hold out before banking the revenue.
5. Inconclusive at full power: ship neither or the simpler, cheaper option. Do not extend.
6. Clearly negative: stop; do not wait for reversal.
7. Log: hypothesis, evidence, primary and guardrail metrics, MDE, planned sample and dates, actual result with CI, SRM check, decision, learning. [70db51ffb976] [5fae1beab1ba]

### 3.8 Plan Shopify tests `[verify UI]`
1. Check the plan. Basic, Shopify, Advanced: test everything before checkout (product, collection, cart, homepage, add to cart, trust badges, pricing display). Tools like Varify run via a head snippet on all plans.
2. Shopify Plus: checkout extensibility (Checkout Blocks, UI extensions, Shopify Functions, Branding API) plus native theme A/B testing. Some apps (Personizely, Checkout Boost) run limited checkout-element tests via Checkout Blocks.
3. For theme tests, consider Shopify **Rollouts**: server-side split before the page ships, so no flicker and no speed penalty. It reports numbers but no significance verdict; you do the stats. Needs a paid plan tier.
4. Use client-side tools for visual front-end tests; server-side or Rollouts for checkout, pricing logic and performance-sensitive paths.
5. Re-verify plan eligibility and features before committing. `[web check: Shopify Rollouts availability, plan tier, checkout A/B options]` [7c932a3b4986]

### 3.9 Price tests
1. Get legal and ethics review. `[web check: jurisdiction rules on personalised pricing and disclosure]`
2. Never base price differences on protected characteristics.
3. Avoid showing different prices for the same SKU to different users at the same time.
4. Test instead: price presentation, savings framing, payment framing, tiers, bundles, or offers that add or remove real features at different prices.
5. Document refund, support and price-match handling before exposing traffic.
6. If using a Shopify price-test app (TestSignal named), check how it assigns prices, handles disclosure, and records revenue and margin. [34fa165a64fe]

### 3.10 Choose methods by monthly orders (Part B)
Assumes DTC, about 2 to 3% conversion, mostly new or anonymous traffic. Orders per month is the binding constraint. Always compute real sample size first. `[needs brand data: orders per month, conversion rate, traffic per page]` [0bda3b4d7e04]

1. **Under 30 orders/month.** Valid: qualitative research only (replay, surveys, user testing, interviews, funnel review), best-practice fixes, repairs. Not valid: any A/B, A/B/n, bandit, or before/after with statistical claims; even a 30% lift needs about 120+ conversions per variant. Do: fix what is broken, apply proven LPG and checkout practice without testing, build the research habit and the experiment log, interview customers.
2. **30 to 300.** Valid: bold A/B tests on the highest-traffic page (home, hero product, cart) aimed at 20%+ relative lift, 2 to 4 weeks, fixed sample computed in advance; micro-conversion primary with purchase as guardrail; before/after only for large structural changes with conditions held constant. Not valid: tweak tests (button colour, minor copy); A/B/n; RPV as primary; same-SKU price tests. Do: one big test at a time, research-heavy, sample-size calculator before every test; accept that most months you learn from research.
3. **300 to 3,000.** Valid: regular A/B tests aimed at 10 to 20% lifts on high-traffic pages; conversion rate primary; guardrails on AOV, margin, return rate; 2-week minimum; SRM checks; sequential engines (Statsig, GrowthBook, Eppo, Optimizely) to monitor without peeking penalties. Borderline: RPV primary (under-powered unless near the top of the band); A/B/n with only 2 to 3 arms; CUPED if returning identified users exist. Not valid: sub-5% lifts; many variants at once; same-SKU price tests. Do: prioritised backlog (PXL or profit-weighted), 1 to a few tests live, disciplined log.
4. **3,000 to 20,000.** Valid: A/B/n, bandits for short campaigns and tactical high-volume decisions, winsorized RPV, CUPED, pre-registered segments, device and source splits; 5 to 10% lifts on hero pages. Not valid: sub-2 to 3% lifts without long runtimes; same-SKU price discrimination. Do: a proper programme, server-side for checkout and pricing logic (Plus), hybrid A/B plus bandit, formal guardrails and stopping rules.
5. **20,000+.** Valid: full programme; small-MDE tests (2 to 5%); revenue and gross-profit-per-visitor primaries; CUPED and variance reduction; always-valid sequential monitoring; many concurrent tests with FDR control; bandits for personalisation; holdouts for surprising winners; long-term novelty and primacy analysis. Not valid: naive same-SKU price discrimination, unplanned peeking, uncorrected multiple comparisons. Do: operate "like Booking/Microsoft in miniature": log, replication of surprising results, A/A tests to validate the platform, a culture that expects most tests to fail.

### 3.11 Prioritise the backlog
1. Gate entry: no idea enters without at least 2 points of evidence (analytics plus replay, survey, user test or interview).
2. Pick a scoring frame to organise ideas:
   - **ICE** (Sean Ellis / GrowthHackers): Impact, Confidence, Ease, each 1 to 10, averaged. Fast and subjective. Weakness: whoever pitches the idea scores it, so everything scores 9/9/9 and nothing is deprioritised. Best for small teams building the habit.
   - **PIE** (Chris Goward / WiderFunnel): Potential, Importance (traffic and value of the page), Ease, 1 to 10 each. Forces a look at traffic data. Middle ground.
   - **PXL** (Peep Laja / CXL): about 10 to 14 binary or scaled criteria tied to evidence: is the change above the fold, is it noticeable within 5 seconds, is it on a high-traffic page, is it backed by heatmaps, user testing, surveys or analytics, how hard is it to build. Weighted, mostly yes or no, less subjective. Best for mature programmes. Slowest.
   - **RICE** (Intercom): Reach, Impact, Confidence, Effort. Use when audience size varies a lot.
3. Then rank by expected value: P(win) x expected lift x gross profit per conversion x traffic exposed, minus build cost. `[needs brand data: SKU margin, page traffic]`
4. Keep P(win) honest and evidence-based, or the formula gives false precision.
5. Add a profit-weighted ceiling estimate: the most the change could be worth if it wins. [aad25dea9ed9]

### 3.12 Pick a stats engine and stopping method
1. If you can estimate expected sample size well: fixed horizon, or group sequential design (more powerful; Spotify's view).
2. If you cannot, or stakeholders will watch daily: an always-valid method (mSPRT, GAVI, corrected-alpha).
3. If the tool is Bayesian: find out its prior and whether its stopping threshold is protected against optional stopping. If you cannot state the prior, you cannot fully interpret or reproduce the result.
4. Confirm the tool's current engine in vendor docs before writing the plan. `[web check: vendor stats engine docs]` [e3ee87a025c5]

## 4. Rules, thresholds and numbers

**Sample size table** (visitors per variant, 95% confidence, 80% power, two-sided; statsunlock.com, consistent with Evan Miller). [00c82f0de25d]

| baseline | 5% rel | 10% rel | 20% rel | 30% rel | 50% rel |
|---|---|---|---|---|---|
| 1% | 637,010 | 163,095 | 42,693 | 19,827 | 7,750 |
| 2% | 315,206 | 80,682 | 21,109 | 9,798 | 3,826 |
| 3% | 207,938 | 53,211 | 13,914 | 6,455 | 2,518 |
| 5% | 122,124 | 31,234 | 8,158 | 3,780 | 1,471 |

| rule | number or threshold | condition | source's basis | card id |
|---|---|---|---|---|
| Sample size formula | n = 16 x p(1-p) / delta^2 per variant | alpha 0.05 two-sided, power 0.80; delta absolute | Evan Miller 2010 | [00c82f0de25d] |
| Effect of halving MDE | 4x sample | Always | Formula | [00c82f0de25d] |
| Alpha / power defaults | 0.05 / 0.80 | Standard | Convention | [00c82f0de25d] |
| Conversions per variant | about 3,830 (5%), 1,000 (10%), 260 (20%), 120 (30%) | 80% power, 95% confidence | Derived from tables x baseline | [00c82f0de25d] |
| "400 conversions per month" claim | Only powers about 30 to 40% lift in a month (card: 25%+); 10% needs about 1,000 per variant | Rejected as a general rule | CXL | [00c82f0de25d] |
| "200 conversions per variant for 20% lift" | True-ish; 250 to 260 is safer at 80% power | 95% confidence | improvado.io, HubSpot "20,000 rule" (20,000 per group at 2% = about 400 control conversions) | [00c82f0de25d] |
| Peeking, worst case | nominal 5% false positive becomes 26.1% | Checking after every observation, stopping at first p < 0.05 | Evan Miller | [e3ee87a025c5] |
| Reported significance needed for true 5% | 2.9% (1 peek), 2.2% (2), 1.8% (3), 1.4% (5), 1.0% (10) | Fixed number of interim looks | Evan Miller peeking table | none (text only) |
| Etsy peeking simulation | over 50% chance of false difference after 500 observations | True null, 50% baseline, alpha 0.10, checking every observation | Etsy Code as Craft, 3 Oct 2018 | none (text only) |
| Kohavi and Sonnet peeking | 5% error becomes about 17% | Run 2 weeks, then check daily for 2 more weeks | Kohavi/Sonnet | none (text only) |
| Bayesian peeking | about 80% false positive rate | Peek every 100 observations, stop at P(A>B) > 0.95 | Alex Molas simulation, 30 Oct 2025 | [e3ee87a025c5] |
| Minimum runtime | 1 full week, in practice 2 | Plus reaching planned sample | Kohavi "Five Puzzling Outcomes" | [5fae1beab1ba] |
| Low-traffic gate for bold changes | under about 100,000 visitors/month: aim at 10 to 20%+ effects | Heuristic | aiformarketing.news; VWO | [67f74e89d43e] |
| User test size | 5 to 8 people | Task-based testing | Source cites without origin | [f856d689f3d8] |
| SRM frequency | about 6% of Microsoft experiments | Large platform | Kohavi | [370ed8c02e34] |
| SRM flag | p < 0.001 | Chi-square on users | Kameleoon | [370ed8c02e34] |
| SRM example | designed 50/50 returning 50.3/49.7 | Illustration of a mismatch | Source | [370ed8c02e34] |
| Anti-flicker cost | hides page up to 3 to 4 seconds by default | Anti-flicker snippets | DebugBear; Andy Davies | [370ed8c02e34] |
| Multiple metrics error | 1 metric 5%, 2 about 10%, 3 about 14% | alpha 0.05 each | Kohavi/Sonnet | [1f26cd618e2d] |
| CUPED sample reduction | 30 to 50% | Metrics strongly correlated with past behaviour | Optimizely glossary | none (text only; card [0bda3b4d7e04] names CUPED only) |
| CUPED ceiling on revenue | 15.91% variance reduction | n = 400,000 LinkedIn feed members, volatile revenue | Jin, Ba et al., arXiv 2110.13406 | none (text only) |
| RPV skew | 97% of visitors spend $0; coefficient of variation about 750% (sd $18 on mean $2.40) | Typical ecommerce case | Atticus Li, Mar 2026 | [7eeb62d20124] |
| RPV sample penalty | about 6x traffic; about 175,000 vs 28,000 per variant | 3% baseline, same relative MDE | Atticus Li | [7eeb62d20124] |
| A/B power at scale | most tests reach power within 2 weeks | $100M/year retailer | leadgen-economy.com | none (text only) |
| A/B/n and routine bandits | 3,000+ orders/month (band 3,000 to 20,000 is "a fair floor") | Lower only for short regret-minimising campaigns | Author synthesis | [3b20905bfc58] [0bda3b4d7e04] |
| Backlog entry gate | at least 2 points of evidence | Every test idea | PXL-style, author | [aad25dea9ed9] |
| False wins among significant results | about 1 in 5 | If 10% of ideas truly work and power is 80% | nishbhana.com | [70db51ffb976] |
| Share of high-impact tests before checkout | about 80% | Ecommerce | Source (vendor-derived) | none (text only) |
| Order-volume bands | under 30; 30 to 300; 300 to 3,000; 3,000 to 20,000; 20,000+ | DTC, 2 to 3% CR, anonymous traffic | Author synthesis | [0bda3b4d7e04] |
| Target lift by band | 30 to 300: 20%+; 300 to 3,000: 10 to 20%; 3,000 to 20,000: 5 to 10%; 20,000+: 2 to 5% | Heuristic | Author synthesis | [0bda3b4d7e04] |
| Band 2 runtime | 2 to 4 weeks | Bold tests | Author synthesis | [0bda3b4d7e04] |
| Realistic lift sizes | 1 to 5% on mature pages; 10 to 20%+ on early or unoptimised pages; 50%+ is suspect | Planning expectation | discoveredlabs.com; Twyman's law | [8dc46d4893e1] |
| Winner's curse sample | 200 conversions instead of 2,000 inflates lift and false positives | Small-sample early-stopped winners | Source | [8dc46d4893e1] |
| VWO free tier | up to 50,000 tested users/month | Time-sensitive | Source | none `[web check: current VWO free tier]` |
| Statsig free tier | up to 1M events/month | Time-sensitive | Source | none `[web check: current Statsig free tier]` |

**Win-rate benchmarks** (each with its sample and definition). [8dc46d4893e1]

| source | win rate | definition and sample |
|---|---|---|
| Microsoft | about 33% (one-third improved key metric) | Kohavi, Crook, Longbotham 2009 |
| Bing | about 15% (10 to 20% in well-optimised domains) | Kohavi, Deng, Longbotham 2014 |
| Google Ads, Booking.com, Netflix | about 10% | Manzi 2012; Thomke 2020 |
| Airbnb Search | about 8% | Kohavi |
| Thomke and Ghosh | 10% had a significant uplift on primary metric | Meta-analysis of about 20,000 Optimizely experiments, 1,000+ customers |
| Optimizely | 12% win on primary metric; clients average about 20% across all metrics, 10% for revenue-tied tests; 35 to 40% conclusive | 127,000 experiments, 1,100 companies |
| VWO | about 14% | Platform-published |
| CXL / Convert | about 20% | Platform-published |
| DRIP | 36.3% win, 22.1% loss, 41.6% inconclusive; decisive win rate 62.1%; median winner RPV +2.77%, top quartile +5.21% or more | DRIP ecommerce database; research-prequalified; looser win definition |
| ConversionTeam | 19.1% significant winners per test; 50.5% raw winners; 61.1% decisive | 2,288 audited tests |

## 5. Diagnostics and checks

| check | how | good | bad | next step |
|---|---|---|---|---|
| Repair or test? | Is current state objectively broken? | Both versions viable, outcome unknown | Bug, broken tracking, known violation | Repair; do not test [3eca46fe9ba3] |
| Is the test powered? | Sample table or calculator vs weekly traffic | Planned sample reached in 2 to 4 weeks | Needs months, or MDE under 10% at low volume | Bolder change, higher-traffic page, micro-conversion primary, or research only [00c82f0de25d] [67f74e89d43e] |
| Relative vs absolute MDE | Read calculator input | Matches plan | Mixed up (+0.4 pts vs +20%) | Recompute [00c82f0de25d] |
| Tails | Brief says two-sided unless justified | Two-sided, or one-sided with documented reason | One-sided chosen to hit significance | Revert to two-sided, recompute [517a8bce6324] |
| Peeking | Compare stop date with planned sample, and the method | Stopped at planned sample, or by a sequential rule | Stopped at first p < 0.05 | Treat result as unreliable; re-run correctly [e3ee87a025c5] |
| Runtime | Dates cover full weeks | 2 full weeks or more, sample met | Under 1 week, or split weeks | Extend to full weeks only if pre-planned [5fae1beab1ba] |
| SRM | Chi-square on users | p above 0.001 | p < 0.001 or visible skew | Do not trust; find the cause (bots, redirects, tracking) [370ed8c02e34] |
| Flicker | Load variant on slow mobile; watch first paint | No original flash | Original flashes, then swaps | Server-side, synchronous high-head script, or careful anti-flicker (costs up to 3 to 4 s) [370ed8c02e34] |
| Tracking | Event counts per arm vs orders in store backend | Match | Pixel broke mid-test | Invalidate [3eca46fe9ba3] |
| Promo overlap | Marketing calendar vs test dates | Clean window | Sale or holiday inside window | Note the confound; consider re-run [062507c94ee4] |
| Multiple comparisons | Count metrics and segments read | 1 primary, pre-registered segments | Many metrics or post-hoc slices | Bonferroni or FDR; post-hoc slices seed new tests [1f26cd618e2d] |
| Device split | Pre-registered mobile vs desktop read | Same direction | Blended win hides mobile loss | Do not ship blind; investigate [1f26cd618e2d] |
| Guardrails | AOV, margin, returns, refunds, page load, add to cart | Flat or better | Any worse | Not a win even if primary improved [7eeb62d20124] |
| Plausibility | Lift size vs page maturity | 1 to 5% mature, 10 to 20% unoptimised | 50%+ or hundreds of % | Twyman's law audit; replicate or hold out [370ed8c02e34] [8dc46d4893e1] |
| Novelty | Daily effect plot; first vs repeat exposure | Stable | Early spike that fades | Be sceptical of early cumulative noise; judge on stable period [5fae1beab1ba] |
| Bayesian tool | Can you state the prior and stopping rule? | Yes | Flat hidden prior; stopped at P > 0.95 on a peek | Treat like a peeked frequentist test [e3ee87a025c5] |
| Platform check | Run an A/A test | No difference | Significant A/A difference | Fix platform before trusting tests [0bda3b4d7e04] |

## 6. Tools, settings and named features

All vendor features `[verify UI]` and `[web check: current engine, pricing, free tier]`.

- **Evan Miller sample size calculator** and "Simple Sequential A/B Testing" (2015), a hand-computable sequential stop rule for low-conversion settings that ignores failure counts.
- **Client-side visual editors:** VWO (SmartStats: Bayesian, Beta-Binomial with Monte Carlo, reports probability to beat baseline and expected loss; free up to 50,000 tested users/month), AB Tasty (Bayesian by preference), Convert.com, Kameleoon (flags SRM at p < 0.001), Optimizely Web (Stats Engine: frequentist mSPRT always-valid p-values plus False Discovery Rate control; CUPED default-on).
- **Engineering-led, server-side, feature flags:** GrowthBook (open source, free self-host; frequentist and Bayesian, sequential, CUPED), Statsig (corrected-alpha sequential; free up to 1M events/month; powers OpenAI, Notion, Atlassian), Eppo (warehouse-native; Bayesian with shrinkage plus GAVI), Split, LaunchDarkly.
- **Datadog:** CUPED default-on.
- **Shopify-native:** Shopify Rollouts (server-side theme A/B; no flicker; numbers without significance verdict; paid plan tier), Shopify app-store tools; Varify (head snippet, all plans); Personizely and Checkout Boost (limited checkout-element tests via Checkout Blocks on Plus); TestSignal (price tests).
- **Shopify Plus checkout extensibility:** Checkout Blocks, UI extensions, Shopify Functions, Branding API.
- **Google Optimize:** sunset 30 September 2023; Google points to partners AB Tasty, Optimizely, VWO.
- **Research tools by type:** GA4 and Shopify funnels, session replay, heatmaps and scroll maps, exit-intent and post-purchase surveys, user testing, interviews (no vendors named for these).
- **Must-capture references named in Part C:** Kohavi, Tang, Xu, *Trustworthy Online Controlled Experiments* (Cambridge, 2020); Evan Miller, "How Not To Run an A/B Test" (2010); Johari et al., "Always Valid Inference" (2015/2022) and "Peeking at A/B Tests" (KDD 2017); Spotify Engineering, "Choosing a Sequential Testing Framework" (Mar 2023); Deng et al., CUPED (WSDM 2013); Kohavi et al., "Seven Rules of Thumb" (KDD 2014) and "Five Puzzling Outcomes" (KDD 2012); Etsy Code as Craft on peeking (2018); Molas on Bayesian peeking (2025); CXL on PXL, bandits and "how many conversions"; Gupta, Kohavi et al. on automated SRM detection (ACM 2022); Baymard cart and checkout research; Varify and Convert on Shopify testing; Shopify developer forum on checkout A/B (Nov to Dec 2024); GrowthBook on Kohavi's win-rate table.
- **Rejected by the author:** listicles quoting round win rates with no sample; vendor case studies with big lifts and no sample, duration or baseline; auto-generated calculator pages (cite Miller instead); HubSpot "20,000 rule" as a general rule (email-oriented); opinion posts without data.
- **Statistical methods named:** chi-square goodness-of-fit (SRM), Bonferroni and FDR (multiple comparisons), mSPRT, GAVI, group sequential with Lan-DeMets alpha spending, corrected-alpha, CUPED, winsorization, threshold-proportion metrics, Thompson sampling and UCB (bandits), A/A tests, holdouts.

## 7. Examples and case results

All are examples, not promises.

- **Amazon DVD price test (September 2000):** discounts of 20% to 40% on 68 DVD titles over 5 days. Customers compared notes, backlash followed. Amazon refunded 6,896 customers an average of $3.10 each (about $21,377 total; ABC News, 29 Sep 2000). Bezos: "we've never tested and we never will test prices based on customer demographics... even that was a mistake because it created uncertainty for customers." Amazon still refuses personalised pricing. The lesson is reputational uncertainty, not a forecast of loss. [34fa165a64fe]
- **"+364% lift" case studies:** rejected under Twyman's law as "the single most common source of bad knowledge in this field". [370ed8c02e34]
- **LinkedIn CUPED:** 15.91% variance reduction on 400,000 members for volatile revenue. (text only)
- **RPV skew case:** 97% spend $0, sd $18 on mean $2.40. [7eeb62d20124]
- **Baymard checkout data:** 70.22% global average cart abandonment from 50 studies (updated 22 Sep 2025; held 69 to 71% since 2014); 11.3 average checkout form fields; up to 35.26% achievable checkout uplift; about $260B recoverable orders across US and EU. Cited as evidence for big-swing checkout hypotheses. (text only)
- **GrowthBook** variance-reduction guide uses a $5,000-order example for outliers. (text only; the example itself is not given)
- **Conversionista** gives a worked example where higher conversion yields lower revenue. (text only; numbers not given)

## 8. Mistakes the source warns about

- Testing whether to fix a bug. [3eca46fe9ba3]
- Using "400 conversions a month" or any magic number instead of MDE math. [00c82f0de25d]
- Confusing relative and absolute lift. [00c82f0de25d]
- One-tailed tests used to reach significance faster. [517a8bce6324]
- Peeking and stopping at first significance; believing Bayesian tools are immune. [e3ee87a025c5]
- Stopping before a full week, or before planned sample, because it looks significant. [5fae1beab1ba]
- Reading early cumulative noise as novelty or primacy. [5fae1beab1ba]
- Tweak tests (button colour, minor copy) at low volume. [67f74e89d43e]
- Testing low-traffic category pages. [67f74e89d43e]
- Treating before/after as proof, or calling its problem "wider error bars". [062507c94ee4]
- Banking a micro-conversion lift without purchase guardrail. [67f74e89d43e]
- Ignoring SRM, flicker, bots, tracking breakage, promo overlap. [370ed8c02e34]
- Reading many metrics or slicing segments after the fact. [1f26cd618e2d]
- RPV as primary at low volume. [7eeb62d20124]
- Adding arms to "test more ideas at once". [3b20905bfc58]
- Using bandits where a clean causal read is needed. [3b20905bfc58]
- Letting the idea's owner score it 9/9/9 in ICE. [aad25dea9ed9]
- Ranking by lift instead of profit; weighting by revenue instead of gross profit. [aad25dea9ed9]
- Testing without research. [f856d689f3d8]
- Reading p < 0.05 as "95% likely real". [70db51ffb976]
- Extending an inconclusive test hoping for significance. [70db51ffb976]
- Comparing win rates without their definitions. [8dc46d4893e1]
- Planning client-side checkout tests on standard Shopify. [7c932a3b4986]
- Same-SKU price tests. [34fa165a64fe]
- Trusting vendor case studies with no sample, duration or baseline. [370ed8c02e34]

## 9. Caveats, conflicts and what is missing

- **Order-volume bands are the author's heuristics**, built on 2 to 3% conversion and anonymous traffic. They are not eligibility gates. Always compute sample size. [0bda3b4d7e04]
- **Two traffic gates.** One is visitors (under about 100,000 per month: bold changes only). The other is orders (the 5 bands). They are not reconciled in the source.
- **Bonferroni vs FDR:** the source does not say when to prefer which. [1f26cd618e2d]
- **Winsorization cap and threshold metric:** no value given; choose and pre-register one per catalogue. [7eeb62d20124]
- **Bandit algorithm:** Thompson sampling and UCB named; none prescribed. [3b20905bfc58]
- **Novelty:** no threshold that proves a real novelty effect. [5fae1beab1ba]
- **Win rates range 8% to 36%** because they measure different things. The author's anchor is 10 to 20%. DRIP's 36.3% is not in conflict once research pre-qualification and a looser win definition are noted. [8dc46d4893e1]
- **Calculator differences:** small, from Miller's constant (slightly below 16) and pooled vs unpooled variance.
- **Several sources are 2026 SEO or agency posts,** used only for cross-checked facts (tooling, Shopify limits). Statistics anchor to tier 1 to 2 sources.
- **Shopify checkout is evolving.** Re-verify yearly. `[web check: Shopify checkout extensibility A/B options]`
- **Conflicts with source 06 (CRO fundamentals):** 06 calls CUPED "essentially free sensitivity" for any test with pre-experiment data; 05 says it helps little for anonymous DTC traffic (15.91% ceiling on revenue). 06 cites a 61.1% win rate and "60%+ win rate" as a target; 05 anchors at 10 to 20% and treats high rates as definition-dependent. 06 prioritises with PIE, ICE, CIE; 05 prefers PXL-style evidence gating plus profit-weighted expected value. 06 says "test relentlessly" and weekly; 05 says "test bigger, not more" at low volume. 06 calls sequential A/B tests safer than multivariate at low traffic; 05 warns that sequential before/after is biased (different meaning of "sequential"; keep both).
- **Consistent with source 06:** Baymard 70.22% abandonment; about 35% checkout uplift available; holdouts for surprising winners; experiment log.
- **Consistent with source 04 and 07:** research first (replay, heatmaps, surveys, user testing) before scarce tests.
- **Missing:** no worked SRM calculation; no guidance on test overlap or interaction between concurrent tests beyond FDR; no guardrail threshold values; no A/A test procedure; no detail on how to build a holdout.
- **Neighbours:** tracking setup and GA4 funnels: 06-MEA; page design output: 07-LPG; ad metrics: 11-ADC; finance: 20-FIN.

## 10. Card index

- 3eca46fe9ba38ace3185d459: Repair defects; test only genuine uncertainty
- 00c82f0de25d3386ad4f37ac: Calculate sample size from MDE, not a conversion-count rule
- 517a8bce632406dcb72b85db: Use two-tailed testing unless null and negative outcomes mean the same action
- e3ee87a025c5b42db58b8cd0: Prevent peeking with a fixed horizon or a valid sequential engine
- 5fae1beab1baca2b9443a544: Set runtime for weekly cycles and investigate novelty correctly
- 67f74e89d43e515491135713: Low-traffic stores should test bold changes and lean on research
- 062507c94ee4c6be8e065f41: Use before/after only as weak evidence for large structural changes
- 370ed8c02e34b8db1a17c453: Audit experiment validity: SRM, flicker, and implausible results
- 1f26cd618e2d059fc9eba5a7: Pre-register decision metrics, segments, and guardrails
- 7eeb62d20124e0e045cd54b7: Choose a metric that matches the store decision and available traffic
- 3b20905bfc58802f066c21cc: Use A/B/n and bandits for different ecommerce decisions
- aad25dea9ed9ef55a2eba83e: Prioritize experiments by evidence and expected gross profit
- f856d689f3d85f8204d660c1: Turn research into evidence-backed ecommerce hypotheses
- 1b7725e0ff57f1b5fc24d1c1: Write a pre-registered test brief with a real decision rule
- 7c932a3b4986ebab47d4abad: Plan Shopify testing around checkout-extensibility limits
- 34fa165a64fe9a5db85bab2f: Avoid same-SKU personalized price experiments; test the offer instead
- 70db51ffb976aae155019e38: Read results through intervals, business value, and an experiment log
- 8dc46d4893e1ff71d673eb5e: Use win-rate benchmarks only with their definitions
- 0bda3b4d7e04da1a8e111c17: Choose an experimentation approach by order volume, then verify with math
