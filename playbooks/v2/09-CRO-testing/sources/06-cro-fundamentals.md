# CRO fundamentals

source_id: 13xcmKLUtePPNdWOs5tNDQCnQJxcH3vGJ  |  folder: /09-CRO-testing  |  cards: 19  |  words: 7057  |  type: article (2 AI-style deep-research reports in one document)
credibility: No author. The text opens "Below is a detailed breakdown of the causal measurement concepts you asked about", so it reads as the output of a research assistant or LLM deep-research run, not a practitioner's own work. Part 1 is "Deep Dive: Holdouts, Incrementality, and Causal Inference in Ecommerce CRO". Part 2 is "Deep Research: Ecommerce Conversion Rate Optimization (CRO)". Evidence is mostly third-party figures named by source only loosely (Baymard, IAB, Shopify, Columbia Business School, vendor case studies) with no links, sample sizes or dates for most numbers. Several examples (retargeting 80/20, popup holdout, email holdout, CRO programme holdout) are illustrations, not real results. Named case results (Hourglass, Modibodi, Snow Peak, Kiehl's, BLACKROLL and others) are vendor or agency case studies without test detail. Some numbers conflict inside the document (section 9).
date signals: Titled "2025 to 2026 data". Hourglass geo test dated 5 May to 16 June 2025. Baymard "2025 benchmark". AI referral growth measured July 2024 to July 2025. Global ecommerce sales "projected to exceed $6.8 trillion in 2025". One programme "executed 54 experiments in 2025". Original Duckhead growth "in 2024". Speed metrics use INP, which dates it after 2024.
scope note: The document header labels it module 06-MEA, but it is filed in 09-CRO. The header says to skip advanced causal methods (BSTS, propensity score matching) and off-site incrementality set-ups, yet the text covers them at length; they are kept here for completeness and flagged as belonging to measurement (06-MEA) and ad-channel testing (11-ADC). Speed work belongs mainly in 08-SPD, cart recovery flows in retention, and page design in 07-LPG.

## 1. What this source is for

Two jobs. First, it helps an operator pick the right measurement design for a question: A/B test, feature holdout, CRO programme holdout, user or geo holdout for a channel, or a causal method when randomisation is impossible. Second, it gives a funnel-stage CRO checklist for ecommerce (homepage, category, product page, cart, checkout, mobile, speed, trust, personalisation, AI-referred traffic) with benchmark bands and a list of levers and case results. It is broad and benchmark-heavy, and thin on how-to detail.

## 2. Principles

### 2.1 Measurement design

1. **A/B tests measure local effects; holdouts measure business impact.** An A/B test answers "did B beat A for the people who saw it in this window". It does not answer 3 questions: would these conversions have happened anyway; what is the combined effect of shipping 20 winners; what happens to total revenue when a channel is switched off. Use holdouts, incrementality tests and causal methods for those. [0eca60fd9161]

2. **Winners do not add up.** Ship 20 winners and conversion will not be "20x better". Reasons: interaction effects (a CTA that won alone may not work with a new homepage layout that also won), cumulative drift (buyer mix, competition and seasons change, so a January winner may not hold in December), and attribution confusion (if conversion rose 8% after 20 changes, you cannot say which ones did it; some winners add nothing after earlier changes; some losers might work in combination). [f671352f5b6e]

3. **A holdout is a random group excluded from an intervention, and it can persist.** Unlike an A/B control, which lasts one test, a holdout can run weeks or months and be excluded from all improvements. The gap between groups is the true incremental effect. The source calls holdouts "the gold standard for causal measurement" and "the most honest proof of program value". [f671352f5b6e]

4. **Measure features by net revenue, not by their own engagement metric.** A popup or recommendation module can raise opt-ins or clicks while cutting purchases. Use a feature holdout and judge on revenue per visitor, with conversion rate, AOV and opt-in rate as support. [c076b110d253]

5. **Incrementality is the question that matters for channels.** The source cites IAB research that 71% of advertisers now see incrementality as their most important KPI, and says ROAS and last-click attribution systematically overstate channels that intercept existing demand. Core question: "If we turned this channel off for two weeks, what would actually happen to total revenue?" [ddbbe8061d10]

6. **Match the method to the question and the data.** Randomise when you can; use a causal method when you cannot; state its identifying assumption and challenge it before trusting the output (card caveat). [04a08881ac09] [0eca60fd9161]

7. **Traffic decides which designs are possible.** High-traffic stores (over 100,000 monthly visitors) can run user-level holdouts, geo holdouts and switchbacks. Lower-traffic stores may need BSTS, synthetic control or longer holdouts to reach power. The card flags 100,000 as rough guidance. [0eca60fd9161]

8. **The goal is better decisions, not more tests.** Judge the programme on incremental revenue, conversion or margin against the counterfactual, not on tests launched or winners shipped. "Would this have happened anyway? If you cannot answer that, you are optimizing in the dark." [0eca60fd9161]

9. **Keep a causal knowledge base.** Every holdout, incrementality test and causal analysis gets a record: question, method, result with confidence interval, decision. The source says this is "far more valuable than a collection of A/B test results". [2b951af15841]

### 2.2 A/B test validity

10. **A valid A/B test needs 5 things.** Enough sample for significance; one clear primary metric (usually conversion rate or revenue per session); proper randomisation; a fixed duration decided in advance (no peeking, no early stop); balanced traffic allocation. [300b03fc0354]

11. **Multivariate only above a traffic and variable-count threshold.** Below it, "sequential A/B tests" (one after another) are the safer choice. No threshold number is given. [300b03fc0354]

12. **Hypothesis format: IF [change], THEN [expected result], BECAUSE [reasoning].** [300b03fc0354]

13. **Prioritise with PIE, ICE or CIE.** PIE = Potential, Importance, Ease. ICE = Impact, Confidence, Ease. CIE = Confidence, Importance, Ease. No scoring scales given. [300b03fc0354]

14. **CUPED is "essentially free sensitivity"** for any A/B test with pre-experiment data on users (for example past purchase frequency or browsing history). It reduces variance and required sample size. See section 9 for the conflict with source 05. [300b03fc0354]

15. **Measure revenue per session, not just conversion rate.** A lift in AOV from trust signals or personalisation is as valuable as a lift in conversion. [25f9d85cd8e3]

### 2.3 Funnel and page levers

16. **CRO is a revenue multiplier on traffic you already pay for.** Average ecommerce conversion is about 2.5 to 3%, so about 97% of visitors leave without buying. Revenue = traffic x conversion rate x AOV x repeat rate; CRO controls 3 of the 4. [93fdbe5da8f2]

17. **Conversion is a cascade of micro-decisions across page types.** Homepage, category, product page, cart and checkout each have their own friction, psychology and levers. Ecommerce must handle browsing, product evaluation, trust and transaction friction, often in one session. [25f9d85cd8e3]

18. **Find the leaking stage before choosing the fix.** Example from the card: strong add-to-cart with weak checkout completion points to checkout work, not another product page redesign. [25f9d85cd8e3]

19. **The homepage orients; it rarely converts.** Its job is to route visitors to the right products quickly and build credibility. Hero passes a "three-second test"; one clear conversion offer (newsletter with a concrete incentive such as early access or first-order discount); simple navigation with clear category entry points; high-quality visuals on clean backgrounds; strategic CTA placement. [5e578ca91bcc]

20. **Curate, do not overload, the homepage.** Promoting many items across many categories (full head-to-toe outfits) cut add to cart by 6.07% and CTR by 10.4% in one reported experiment. A focused selection wins. [5e578ca91bcc]

21. **Personalise with history; show bestsellers to new visitors.** Personalised homepage recommendations: +136% CTR to product pages vs static. Bestsellers for visitors with no history: +23.01% CTR to product pages vs static featured products. Secure trust signals and good page design for everyone first, then layer personalisation where cohorts value it (35 to 44 year olds rated personalisation highest in one study). Personalisation is shifting from browsing history to real-time intent signals (fit, shipping, returns, compatibility reassurance before a shopper bounces). [5e578ca91bcc]

22. **Define each category page's job before designing it: browsing, deciding or buying.** On browsing pages, "Add to Cart" buttons create decision conflict because the visitor is still asking "what options exist", not "am I ready to buy this". Visitors want clear subcategories, strong visual hierarchy for scanning, filters that narrow without overwhelming, and click-through to product pages. [1e03a58f6fe1]

23. **Category exit rate should sit near the site average.** A high exit rate means visitors leave the site instead of going to product pages. The card adds: check traffic intent before blaming design. [1e03a58f6fe1]

24. **Keep promo messaging consistent from category page to product page.** When the promo on the category page is reinforced on the product page, add to cart is more likely. [1e03a58f6fe1]

25. **The product page is "make-or-break".** "If the product page doesn't sell, nothing else in your funnel matters." Going from 2.0% to 2.5% conversion is a 25% revenue increase at the same traffic. [fc7c739888fc]

26. **Product page essentials.** Crisp multi-angle images, short videos, lifestyle photos; 360-degree views or demo clips raise engagement and time on page; clean light backgrounds show items accurately. Descriptions lead with value proposition, perceived value, benefits and use cases, not just features. Price, shipping cost, return policy and realistic delivery estimates easy to find. Add to Cart above the fold. Trust signals and social proof near the decision. [fc7c739888fc]

27. **Believable reviews beat perfect ones.** A mix of 4- and 5-star reviews feels more real than a wall of 5 stars; some negative reviews outweighed by positive ones increase trust. Influencer UGC adds aspirational context. [e18bae3af3dd]

28. **Most shoppers need proof from others.** Only 14% of consumers trust what a brand says about itself, so "86% require trust signals and social proof". [e18bae3af3dd]

29. **Place trust signals where the decision happens.** One DTC brand moved trust icons inline next to Add to Cart instead of a section below and saw +18% revenue per session after 3 weeks. Trust signals buried below the fold are listed as a pitfall. [e18bae3af3dd]

30. **Late costs are the biggest checkout leak.** 39% of abandoners leave because extra costs (shipping, tax, fees) appear too late. Pricing transparency is "the single largest lever". Show them before checkout begins. [d4104b13110f]

31. **Guest checkout is one of the most impactful interventions.** Forcing account creation adds friction at the worst moment. Collect email during guest checkout and build the account relationship after purchase. Baymard: 62% of sites do not make guest checkout prominent enough. [d4104b13110f]

32. **Cut checkout fields to the strictly necessary.** Each field is another chance to abandon. Use autofill. Use progress indicators to reduce anxiety. High-contrast buttons and minimal fields raise conversion (a machine-learning study where logistic regression modelled this best at 87% accuracy). [d4104b13110f]

33. **Offer the payment methods your market uses.** UPI in India; Apple Pay, Google Pay and Shop Pay in Western markets. Show recognisable payment brands and wallets. Avoid redirects or context switches during payment. [d4104b13110f]

34. **Surface security signals, return policies and payment logos in checkout.** Use smart authentication to reduce friction. [d4104b13110f] [e18bae3af3dd]

35. **Checkout is where most stores are weakest.** Baymard: large sites have about 32 checkout-specific improvements available and can gain about 35% checkout conversion from UX fixes alone. "Fix checkout first" is strategic priority 1. [d4104b13110f]

36. **Speed is a multiplier.** It affects search visibility, paid traffic cost, conversion and repeat purchase at once. Mobile target: LCP under 2 seconds. [9461d45dfbe7]

37. **Mobile is the largest gap.** Mobile drives about 60% of traffic and sales but converts at about half the desktop rate. Mobile cart abandonment is about 85%. Priorities: one-page or wallet checkout; tap-friendly CTAs and clickable phone and email fields; guest checkout and wallets; resized tap targets, floating key CTAs and critical actions in the thumb zone; social proof visible where decisions happen. Desktop grids squeezed onto mobile and filters hidden in hamburger menus cause exits. [1e03a58f6fe1] [d4104b13110f]

38. **AI-referred visitors arrive pre-sold and want confirmation.** They ask detailed natural-language questions and get 1 to 3 recommendations before clicking. They expect the page to confirm immediately why it matches their brief; a generic page that makes them redo the research lowers conversion. More than half of AI-referred sessions start on product pages (vs 20% for organic search). Shopify data: AI shoppers convert at nearly 50% higher rates and spend 14% more. [86c233f0eb39]

39. **Recover abandoned carts fast, then escalate.** Contact within the first hour; escalate through objection handling and urgency over 72 hours; incentives (time-limited discount, free shipping) are one tactic among several. The card adds: do not make discounts the only answer; compare against a holdout. [e46b405d55df]

## 3. Procedures

### 3.1 Pick a measurement design (source's framework)
Step 1. Decide the question.
- "Did this specific test win?" → standard A/B test.
- "Does our retargeting drive incremental revenue?" → user-level holdout.
- "Does Meta advertising drive incremental sales?" → geo holdout.
- "Has our whole CRO programme created value?" → CRO programme holdout.
- "What was the impact of this change during peak season?" → BSTS or difference-in-differences.
- "We cannot randomise; how do we estimate causality?" → synthetic control, propensity score matching, or regression discontinuity.

Step 2. Match the method to data infrastructure and traffic (over 100,000 monthly visitors for user holdouts, geo holdouts and switchbacks; otherwise BSTS, synthetic control or longer holdouts). `[needs brand data: monthly visitors, logged-in share, geo split]`

Step 3. Document: question, method, result with confidence interval, business decision. [0eca60fd9161] [2b951af15841]

### 3.2 Run a CRO programme holdout
1. Randomly assign a small share of all traffic to a permanent holdout that sees the site as it was before the programme. Example: 5%.
2. Everyone else gets every shipped winner.
3. Keep the assignment stable for the period. Example: 90 days.
4. Compare conversion rate (and revenue per visitor) at the end.
5. Report net lift, not the sum of individual test lifts.
6. Record which experiences each group could receive, the CI, and the decision.
Card caveats: 5% and 90 days are illustrative; calculate whether your traffic can detect a meaningful effect. Withholding major usability, accessibility or policy fixes from a permanent holdout may raise operational or ethical concerns. [f671352f5b6e]

### 3.3 Run a feature holdout (popup, recommendations, personalisation)
1. Randomly hold out a group that never sees the feature. Examples: popup 90% exposed / 10% holdout; recommendations 5% holdout.
2. Tag and track both groups through the whole journey, to purchase and, where relevant, repeat purchase.
3. Measure RPV (decision metric), AOV, conversion rate, and email or SMS opt-in rate.
4. Look for trade-offs: more opt-ins but fewer purchases; more clicks but no bigger baskets.
5. Segment (new vs returning, mobile vs desktop) only when sample supports it; decide on the pre-declared overall metric.
6. Keep the holdout long enough to capture delayed and repeat purchases if the feature targets them. [c076b110d253]

### 3.4 Measure retargeting incrementality (user-level holdout)
1. Define the audience: visitors in the last 30 days who did not buy.
2. Split 80/20 at random.
3. Show retargeting ads to the 80%; suppress all retargeting to the 20%.
4. Run 14 days.
5. Compare conversion rates. The holdout rate divided by the exposed rate is the share that would have bought anyway; 1 minus that is the incremental share.
Note: ad-platform set-up belongs in 11-ADC. `[verify UI]` for any platform suppression step. [ddbbe8061d10]

### 3.5 Measure email campaign incrementality
1. Hold back part of the eligible list (example: 10%).
2. Send the campaign to the rest.
3. Incremental lift = promoted group purchase rate minus holdout purchase rate (example: 3.8% minus 2.1% = 1.7 points), not the promoted rate alone. [ddbbe8061d10]

### 3.6 Run a geo holdout
1. Pick candidate regions (DMAs, cities, countries).
2. Compare their past conversion and revenue patterns with possible control markets; pick sets with strong pre-period similarity (example: correlations 0.96 to 0.99).
3. Pause all campaigns of the tested channel in holdout markets for a pre-declared window (example: 6 weeks); leave control markets unchanged.
4. Report incremental CPA, incremental ROAS, new-customer CPA, new-customer ROAS, lift % and confidence level.
5. Use incremental, not platform-attributed, ROAS for budget decisions.
6. Check for spill-over (national campaigns, influencers, direct traffic, retail availability) before reading the result (card addition). [e353aade03ae]

### 3.7 Three incrementality tests any store can run
1. **Platform-native lift study:** Meta or Google randomly assigns users to exposed and holdout groups and measures the conversion difference. `[verify UI]`
2. **DIY geo holdout:** pause ads in matched test regions, compare with control regions.
3. **On/off experiment:** turn a channel or campaign on and off in alternating periods; measures overall revenue impact. [ddbbe8061d10]

### 3.8 Use causal methods when you cannot randomise
- **Difference-in-differences:** Effect = (Treatment_after − Treatment_before) − (Control_after − Control_before). Use when you cannot randomise users (site-wide changes) but have a comparable control group. Example: email redesign.
- **CUPED:** use a pre-period covariate (past purchase frequency, browsing history) to cut variance. Use for any A/B test with user-level pre-period data. Example: smaller samples for checkout tests.
- **Switchback:** randomise whole environments (regions, time periods), alternating treatment and control. Use for marketplace tests where user-level randomisation causes interference (search ranking, ad spend allocation). Source claims 40 to 60% lower standard errors vs simple item randomisation.
- **Synthetic control:** build a weighted composite control from imperfect candidates. Use when no single control market matches, especially in geo tests.
- **BSTS:** Kalman filtering for trend and seasonality, spike-and-slab regression for predictor selection, Bayesian model averaging against overfitting. Use for strong seasonality with no clean control (example: Black Friday and Christmas).
- **Propensity score matching:** match each treated customer to a similar untreated one on observed covariates. Use with rich customer data when you cannot randomise.
- **Instrumental variables:** a variable correlated with treatment but affecting the outcome only through treatment. Use for selection bias or endogeneity.
- **Regression discontinuity:** compare people just above and below a cutoff. Use for threshold rules (loyalty tiers, free shipping thresholds, discount minimums). Example: discount above $100; compare $99 and $101 spenders.
Card rule for all: state the identifying assumption (parallel trends, valid threshold, no unobserved confounding) and test or challenge it; these methods need specialist implementation. [04a08881ac09]

### 3.9 Run a valid A/B test (source's checklist)
1. Write IF/THEN/BECAUSE.
2. Prioritise with PIE, ICE or CIE.
3. Pick one primary metric tied to purchase value (conversion rate or revenue per session); add guardrails (AOV, refund rate, margin, checkout completion) per the card.
4. Calculate sample size; set allocation and duration before launch; randomise properly; keep groups balanced.
5. Do not peek and stop on a good-looking result.
6. Use multivariate only when traffic supports it.
7. Use CUPED where pre-experiment data exists.
The source gives no formula, scoring scale or sample numbers. [300b03fc0354]

### 3.10 Diagnose the funnel
1. Instrument: sessions → product page view → add to cart → checkout start → checkout completion → purchase, plus AOV and revenue per session.
2. Compare each stage with the bands in section 4.
3. Compare product page conversion with the vertical band.
4. Use category dynamics to form hypotheses (fit uncertainty in apparel, research intensity in electronics, repeat intent in beauty).
5. Pick the stage with the biggest leak and work there.
6. Use revenue per session as a primary metric when AOV can move (bundles, recommendations, delivery thresholds, trust messaging). [25f9d85cd8e3] `[needs brand data: stage conversion rates by device and channel]`

### 3.11 Checkout audit
1. Check the 3 main abandonment causes: late extra costs; long or complex flow; forced account creation.
2. Show shipping, tax and fees before checkout.
3. Make guest checkout prominent; collect email during it.
4. Remove every field not strictly needed; enable autofill; add progress indicators on multi-step flows.
5. Use high-contrast primary buttons; avoid payment redirects.
6. Offer the market's payment methods.
7. Show security indicators, return policy and payment logos.
8. On mobile: large, well-spaced tap targets; one-page or wallet checkout.
9. Track add to cart, cart to checkout, checkout completion, payment errors and mobile completion separately before and after (card). [d4104b13110f]

### 3.12 Cart abandonment recovery
Tactics listed: brand reviews on checkout page; optimise checkout; show fees before checkout; exit-intent popups; automatic email and SMS reminders; multi-step flows with objection handling and urgency over 72 hours; incentives (time-limited discounts, free shipping); real-time intent personalisation (fit, shipping, returns, compatibility).
Timing: first contact within the first hour; escalate over 72 hours.
Card additions: lead with the likely objection (total cost, delivery, returns, fit, compatibility); use discounts only when incremental order value beats margin loss; compare with a holdout; frequent discounts can train shoppers to abandon on purpose. Flow build belongs to the retention folder. [e46b405d55df]

### 3.13 Mobile category page
- Key actions in the lower half of the screen (thumb zone); quick win: sticky filter bar at bottom.
- Tap targets at least 44px with generous whitespace.
- Filter access: sticky bottom sheet or floating "Filter" pill (source claims 75% of mobile users abandon if they cannot refine quickly).
- First 2 rows get most taps; limit hero banners to 30 to 40% of the first view.
- Swipeable carousels for subcategories and variants.
- Responsive WebP images; lazy-load below the fold. [1e03a58f6fe1]

### 3.14 Mobile speed
1. Measure real-user LCP and INP (Chrome UX Report, Shopify Web Performance, PageSpeed Insights). `[verify UI]`
2. Target mobile LCP under 2 seconds.
3. Compress images: hero under 100KB, grid images under 60KB.
4. Preconnect key domains; defer non-critical JavaScript; responsive WebP; lazy-load below the fold.
5. Measure before and after; use a test or holdout to isolate revenue impact (card).
Detailed speed work: 08-SPD. [9461d45dfbe7]

### 3.15 AI-referred traffic
1. Segment AI referral traffic where analytics allows and compare landing mix, product page engagement, conversion, AOV and refunds (card). `[needs brand data: AI referral sessions]`
2. Make product pages confirm the visitor's likely constraints at once: product type, size, price ceiling, delivery need, use case.
3. Do not push these visitors back into broad browsing.
4. Test AI pre-sale search or chat only if it answers product questions reliably.
5. Measure revenue per session and purchases, not referral growth. [86c233f0eb39]

## 4. Rules, thresholds and numbers

**Overall conversion bands** (source table 2.1). [25f9d85cd8e3]

| level | conversion rate |
|---|---|
| Underperforming | under 1% |
| Average | 1 to 2% |
| Above average | 2 to 3% ("industry standard") |
| Strong | 3 to 4.5% |
| Top 10% | 4.5%+ |
| Best-in-class | 5 to 8%+ |

**Funnel-stage bands** (source table 2.3). [25f9d85cd8e3]

| stage | poor | average | good | excellent |
|---|---|---|---|---|
| Overall CR | under 1% | 2 to 3% | 3 to 5% | over 5% |
| Add to cart | under 5% | 8 to 12% | 12 to 18% | over 18% |
| Cart to checkout | under 30% | 50 to 60% | 60 to 70% | over 70% |
| Checkout completion | under 50% | 60 to 70% | 70 to 80% | over 80% |

**Product page conversion by vertical** (source table 2.2). [25f9d85cd8e3]

| category | PDP conversion |
|---|---|
| Beauty and skincare | 2.5 to 4% |
| Apparel and fashion | 1.8 to 3% |
| Consumer electronics | 1.2 to 2% |
| Home goods and furniture | 1.5 to 2.5% |
| SaaS and subscriptions | 3 to 7% |

| rule | number or threshold | condition | source's basis | card id |
|---|---|---|---|---|
| Global ecommerce conversion | about 2.5 to 3%; about 97% leave without buying | Average | Unnamed | [93fdbe5da8f2] |
| Cart abandonment | 70.22% | Average of 50 studies | Baymard | [d4104b13110f] |
| Mobile cart abandonment | about 85% | Mobile | Unnamed | [d4104b13110f] |
| Abandon for late extra costs | 39% of abandoners | Shipping, tax, fees shown late | Baymard | [d4104b13110f] |
| Abandon for long or complex checkout | 18% | | Baymard | [d4104b13110f] |
| Abandon for forced account | about 16 to 24% | | Baymard | [d4104b13110f] |
| Sites not making guest checkout prominent | 62% | | Baymard | [d4104b13110f] |
| Checkout UX mediocre or worse | 65% of sites (also given as 64% desktop, 63% mobile); only 2% good; none perfect; 15% poor or very poor | 2025 benchmark | Baymard | [d4104b13110f] |
| Checkout improvements available | about 32 per large site | Large sites | Baymard | [d4104b13110f] |
| Checkout conversion gain from UX fixes | about 35% | Large sites | Baymard usability testing | [d4104b13110f] |
| Checkout ML model | high-contrast buttons and minimal fields raise conversion; logistic regression 87% accuracy | One ML study | Unnamed | none (text only) |
| Trust gap | 14% trust brand claims; 86% need trust signals and social proof | Consumers | Unnamed | [e18bae3af3dd] |
| Test win rates by category | benefit communication 54.5%; shipping and return communication 41.8%; payment trust signals 40.5% | A/B test categories | Unnamed | [e18bae3af3dd] |
| Inline trust icons | +18% revenue per session after 3 weeks | One DTC brand | Case | [e18bae3af3dd] |
| Homepage personalised recs | +136% CTR to PDPs | vs static recs | One retail experiment | [5e578ca91bcc] |
| Bestsellers for new visitors | +23.01% CTR to PDPs | vs static featured | One experiment | [5e578ca91bcc] |
| Broad homepage assortment | −6.07% add to cart, −10.4% CTR | Full-outfit, many categories | One experiment | [5e578ca91bcc] |
| Hero test | 3 seconds | Homepage hero | Principle | [5e578ca91bcc] |
| Mobile share | about 60% of sales and traffic, about half desktop CR | Global | Unnamed | [1e03a58f6fe1] |
| Mobile tap targets | at least 44px | Mobile | Guideline | [1e03a58f6fe1] |
| Mobile filter abandonment | 75% abandon if they cannot refine quickly | Mobile category pages | Unnamed | [1e03a58f6fe1] |
| Hero banner share of first view | 30 to 40% maximum | Mobile category | Guideline | [1e03a58f6fe1] |
| Mobile LCP target | under 2 seconds | Mobile | Guideline | [9461d45dfbe7] |
| Image weights | hero under 100KB, grid under 60KB | Mobile | Guideline | [9461d45dfbe7] |
| LCP vs conversion | every 100ms slower → 3.5% lower conversion | Directional | Unnamed | [9461d45dfbe7] |
| LCP 2.5s vs 1.5s | about 30% lower conversion | Stores | Unnamed | [9461d45dfbe7] |
| INP vs conversion | every 32ms slower → about 1.5% drop | | Unnamed | [9461d45dfbe7] |
| Mobile speed gain | 0.1s faster → 8.4% higher retail conversion | | Unnamed | [9461d45dfbe7] |
| Load time vs CR | 2.4s → 1.9% CR; 4.2s → under 1%; 5.7s+ → 0.6% | One report | Unnamed | [9461d45dfbe7] |
| Delay vs conversion | 1 second → up to 7% fewer conversions; also "100ms → 7% drop" in "one large analysis" | Conflicting (section 9) | Unnamed | [9461d45dfbe7] |
| PDP conversion gain | 2.0% → 2.5% = 25% more revenue | Same traffic | Arithmetic | [fc7c739888fc] |
| Incrementality as top KPI | 71% of advertisers | Survey | IAB | [ddbbe8061d10] |
| AI referral traffic growth | +4,700% year over year | US shopping sites, Jul 2024 to Jul 2025 | Unnamed | [86c233f0eb39] |
| AI sessions starting on PDPs | more than half (vs 20% for organic search) | | Shopify data | [86c233f0eb39] |
| AI shopper conversion and spend | nearly 50% higher CR; 14% more spend | | Shopify data | [86c233f0eb39] |
| GenAI workflows | sales up to +16.3%; pre-sale chatbot +16.3% sales, +21.7% CR; CR up to 22%; smaller and newer sellers gained more | 7 workflows on a major platform | Columbia Business School study | [86c233f0eb39] |
| Personalisation by age | 35 to 44 rated it highest | Survey | Unnamed | [5e578ca91bcc] |
| Holdout traffic gate | over 100,000 monthly visitors for user holdouts, geo holdouts, switchbacks | Rough | Source | [0eca60fd9161] |
| CRO programme holdout (example) | 5% of traffic, 90 days | Illustrative | Source | [f671352f5b6e] |
| Popup holdout (example) | 90% exposed, 10% holdout | Illustrative | Source | [c076b110d253] |
| Recommendation holdout (example) | 5% | Illustrative | Source | [c076b110d253] |
| Email holdout (example) | 10% of list | Illustrative | Source | [ddbbe8061d10] |
| Retargeting holdout (example) | 80/20 split, 14 days, 30-day non-buyer audience | Illustrative | Source | [ddbbe8061d10] |
| Geo holdout match | correlation 0.96 to 0.99 with controls | Hourglass example | Case | [e353aade03ae] |
| Switchback precision | 40 to 60% lower standard errors vs item randomisation | Marketplaces | Unnamed | [04a08881ac09] |
| Cart recovery timing | first contact within 1 hour; sequence over 72 hours | Framework to test | Source | [e46b405d55df] |

## 5. Diagnostics and checks

| check | how | good | bad | next step |
|---|---|---|---|---|
| Question type | Write the decision question | Method matches question (3.1) | A/B test asked to prove channel value or programme ROI | Switch to holdout or causal method [0eca60fd9161] |
| Programme value | Compare holdout vs optimised group | Net lift with CI | Only the sum of individual test lifts | Set up a programme holdout [f671352f5b6e] |
| Feature value | Feature holdout on RPV | RPV up or flat with more opt-ins | Opt-ins up, purchases down | Rework or remove feature [c076b110d253] |
| Channel value | User or geo holdout | Meaningful incremental lift | Holdout converts near exposed rate (example: 70%) | Cut or redirect spend [ddbbe8061d10] |
| Geo test set-up | Pre-period correlation of markets | Very high similarity | Weak match or spill-over | Re-pick markets or use synthetic control [e353aade03ae] |
| Causal method | Identifying assumption stated and challenged | Assumption checked | Output trusted blind | Challenge or drop the method [04a08881ac09] |
| Overall CR | Stage band table | 3 to 5% good | under 1% | Look for friction or traffic-quality issues [25f9d85cd8e3] |
| Add to cart rate | Band table | 12 to 18% | under 5% | Product page work [25f9d85cd8e3] [fc7c739888fc] |
| Cart to checkout | Band table | 60 to 70% | under 30% | Cart work: cost transparency, trust [25f9d85cd8e3] |
| Checkout completion | Band table | 70 to 80% | under 50% | Checkout audit (3.11) [d4104b13110f] |
| Category exit rate | Analytics vs site average | Near average | Well above | Check traffic intent, then design [1e03a58f6fe1] |
| Category CTAs | Page review | Browsing pages route to product pages | Add to Cart on browsing pages | Remove or test removal [1e03a58f6fe1] |
| Mobile filters | Page review on phone | Sticky bottom filter or pill | Filters hidden in a menu | Add sticky filter [1e03a58f6fe1] |
| Product page info | Page review | Price, shipping cost, returns, delivery estimate easy to find; Add to Cart above fold | Hidden costs, "add to cart to see shipping" | Surface the info [fc7c739888fc] [e18bae3af3dd] |
| Review mix | Review widget | Mix of 4 and 5 stars | Wall of perfect scores | Show real distribution [e18bae3af3dd] |
| Trust placement | Page review | Icons beside Add to Cart | Trust block far below | Test inline placement [e18bae3af3dd] |
| Hidden costs | Walk through checkout | Costs shown before checkout | Costs appear at last step | Show early [d4104b13110f] |
| Guest checkout | Walk through | Prominent guest option | Forced or hidden account step | Make guest prominent [d4104b13110f] |
| Payment options | Walk through | Market's wallets and local methods | Missing wallet or UPI; redirects | Add methods [d4104b13110f] |
| Mobile speed | Real-user LCP, INP | LCP under 2s | LCP 2.5s+ | Image, JS, preconnect work (08-SPD) [9461d45dfbe7] |
| AI referral landing | Landing page mix of AI traffic | Product page confirms the brief | Generic page, forces re-browsing | Tailor product page facts [86c233f0eb39] |
| Win claims | Sample, duration, baseline stated? | Stated | Not stated | Treat as hypothesis only (see source 05) |

## 6. Tools, settings and named features

All `[verify UI]` and `[web check: current capabilities and pricing]`.

- **Analytics:** Shopify Analytics, Google Analytics 4, Mixpanel.
- **Heatmaps and session recording:** VWO Insights, Hotjar, Microsoft Clarity.
- **A/B testing:** VWO, Optimizely, AB Tasty, Convert.
- **Personalisation:** Optimizely, Monetate, Rebuy, Dynamic Yield.
- **Surveys and feedback:** VWO On-Page Surveys, Qualtrics, Hotjar Surveys.
- **Speed monitoring:** Chrome UX Report, Shopify Web Performance, PageSpeed Insights.
- **Cart recovery:** Klaviyo, Yotpo, WooCommerce plugins.
- **Incrementality:** Meta and Google platform-native lift studies; DIY geo holdouts; on/off tests.
- **Payment:** Apple Pay, Google Pay, Shop Pay, UPI.
- **Causal methods:** DiD, CUPED, switchback, synthetic control, BSTS, PSM, IV, RDD.
The card adds: pick tools by measurement job, not by feature list; check privacy, data quality and integrations. [373e2f9d659a]

## 7. Examples and case results

All examples. Most lack sample size, duration or baseline.

- **CRO programme holdout (illustration):** 5% holdout for 90 days converts at 2.5%; optimised users at 2.9%; +0.4 points, 16% relative. [f671352f5b6e]
- **Email holdout (illustration):** 10% held back buy at 2.1%; promoted group 3.8%; true lift 1.7 points. Attributing the full 3.8% to email over-invests in email. [ddbbe8061d10]
- **Retargeting (illustration):** 80/20 split, 14 days; holdout converted at 70% of exposed rate, so true incrementality 30%. The brand stopped standard retargeting offers and kept the channel only for specific deal announcements. [ddbbe8061d10]
- **Hourglass Cosmetics geo holdout (real, 2025):** luxury beauty brand with Sephora retail. Paused all Meta campaigns in 10 DMAs for 6 weeks (5 May to 16 June 2025); DMA correlations with controls 0.96 to 0.99. Incremental CPA $130 (10.4% lift, 99% confidence); incremental ROAS 0.51 (7.9% lift, 90% confidence); new-customer CPA $190 (10.6% lift, 95% confidence); new-customer ROAS 0.35 (8.6% lift, 90% confidence). Conclusion: Meta drove real incremental value; omni-channel lift likely several times higher. [e353aade03ae]
- **Switchback checkout test:** a marketplace ran 12 days, rotating 1-page and 3-page checkout every hour. AOV +2.1% (98% significance) and RPV improved, "flipping" the "fewer steps = higher conversion" advice. Card: context-specific, not proof longer checkouts win. [04a08881ac09]
- **Wildberries:** synthetic control for 2 quasi-experiments. [04a08881ac09]
- **BSTS:** a brand isolated a CRO change during Black Friday and Christmas. [04a08881ac09]
- **PSM:** product sampling responders matched to non-responders. **IV:** marketplace used sellers' buybox behaviour on other products as an instrument. **RDD:** $100 discount threshold. [04a08881ac09]
- **GoodwillFinds:** product page A/B test, +5.16% clicks on "Add-to-Bag" after 8 days. [fc7c739888fc]
- **Optimizely retail experiment:** "Highly Rated" badges and size filters drew attention to popular products and raised add-to-cart likelihood (no numbers). [fc7c739888fc]
- **Kutts:** variation lifted conversion about 6% and revenue 9%. [fc7c739888fc]
- **Simba Sleep:** 9% revenue lift with real-time personalisation and automated A/B and dynamic testing. [5e578ca91bcc]
- **One programme in 2025:** 54 experiments, 61.1% win rate, "ROI of 1.879%" excluding platform costs (the card reads it as 1.879; unit unclear). [300b03fc0354]
- **ShopClues:** at least 1 effective A/B test per week; 26% more checkout page visits; 50% higher CTR on the new top navigation bar. [300b03fc0354]
- **Case table:** Modibodi cart icon optimisation, $400,000 annualised uplift, 9.7x ROI. Snow Peak focused changes, +35% conversion, $600,000 extra revenue in 6 months. Kiehl's with SplitBase, about $1.6M extra revenue. BLACKROLL 27 winning tests, €343,240 during test periods, 15x ROI before rollouts. Urban Botanica 1.2% to 4.8% conversion. ReplaceDirect, 25% less cart abandonment. Original Duckhead full audit, 100% YoY growth in 2024. Dorko AI-generated lifestyle images per SKU, +6.35% conversion. Delugs Strap Finder tool, +58% YoY checkout conversion. (text only, no card beyond those cited)
- **Revenue equation:** a $1M store at 2% conversion reaches $1.5M at 3% at the same traffic, AOV and repeat rate; +15% AOV adds another $225K. [93fdbe5da8f2]

## 8. Mistakes the source warns about

The source's own pitfall list (based on Baymard 2025 and field research):
1. Mediocre checkout experience (64% of sites mediocre or worse; 2% good). [d4104b13110f]
2. Hidden costs revealed late (39% abandon). [d4104b13110f]
3. Forced account creation (62% do not make guest checkout prominent). [d4104b13110f]
4. Slow mobile pages (every 100ms costs 3.5%). [9461d45dfbe7]
5. Desktop-first design on mobile: tiny thumbnails, unreadable text, hidden filters. [1e03a58f6fe1]
6. Trust signals buried below the fold. [e18bae3af3dd]
7. Overloaded homepage. [5e578ca91bcc]
8. Add to Cart on browsing-focused category pages. [1e03a58f6fe1]
9. No testing programme; relying on opinion. [300b03fc0354]
10. Generic landing pages for AI and LLM traffic. [86c233f0eb39]

Also from the text:
- Adding up individual test wins to claim programme value. [f671352f5b6e]
- Crediting a channel with all attributed conversions (ROAS, last click). [ddbbe8061d10]
- Judging popups on opt-ins alone. [c076b110d253]
- Peeking and stopping early. [300b03fc0354]
- Multivariate tests below the traffic threshold. [300b03fc0354]
- Wall of perfect reviews. [e18bae3af3dd]
- Promo messaging that changes between category and product page. [1e03a58f6fe1]
- Judging only conversion rate when AOV can move. [25f9d85cd8e3]

## 9. Caveats, conflicts and what is missing

- **Weak sourcing.** Most numbers name no study, sample or date. Treat every benchmark as directional. The cards repeat this on every topic.
- **Internal speed conflict.** The source says 100ms slower = 3.5% lower conversion, then says a 100ms increase led to a 7% drop "in one large analysis", then says a 1-second delay cuts conversions by "up to 7%". These cannot all be true as elasticities. The header summarises this as "3.5% to 7%". The card says to use them to justify investigation, not to forecast. [9461d45dfbe7]
- **Internal Baymard conflict.** "65% mediocre or poor" in 3.5 vs "64% desktop, 63% mobile" in 3.5.7. Likely the same benchmark rounded differently.
- **Unit unclear:** "ROI of 1.879%" for one programme. [300b03fc0354]
- **Win-rate target conflict with source 05.** This source says a "disciplined testing program with 60%+ win rate generates compounding returns" and cites 61.1%. Source 05 anchors at 10 to 20% significant winners and says high rates depend on definition and research pre-qualification (DRIP 36.3%; ConversionTeam 61.1% is a "decisive" rate, not a significant-per-test rate). The number 61.1% also appears in source 05 as ConversionTeam's decisive rate (wins over wins plus losses); this source does not say whether its 61.1% uses that definition. Do not set 60% as a target.
- **CUPED conflict with source 05.** Here CUPED is "essentially free sensitivity" for any test with pre-period data. Source 05 says it helps little on mostly anonymous DTC traffic (LinkedIn 15.91% variance reduction on revenue). Rule: CUPED helps only where returning identified users give a strong covariate.
- **Prioritisation conflict with source 05.** This source lists PIE, ICE, CIE as equals. Source 05 says ICE lets idea owners inflate scores and prefers PXL-style evidence gating plus profit-weighted expected value.
- **Testing cadence conflict with source 05.** This source praises weekly testing ("test relentlessly"). Source 05 says low-volume stores should "test bigger, not more".
- **"Sequential" means different things.** Here "sequential A/B tests" means running tests one after another instead of multivariate. In source 05 "sequential" means sequential statistics or before/after comparisons.
- **Switchback example** contradicts common "fewer steps" advice but is from one marketplace. [04a08881ac09]
- **Traffic gate overlap.** This source's 100,000 monthly visitors gate is for holdout designs. Source 05's 100,000 visitors gate is for bold-change-only A/B testing. Same number, different use.
- **Holdout ethics.** A permanent holdout withholds fixes; the card flags accessibility and policy concerns. [f671352f5b6e]
- **Omnichannel brands:** online lift may understate offline and long-term effects. [ddbbe8061d10]
- **No how-to** for sample size, holdout power, geo matching method, BSTS tooling, or CUPED set-up.
- **Scope spill.** Geo and platform lift tests belong with 11-ADC and 06-MEA; speed with 08-SPD; recovery flows with retention; page design with 07-LPG. The header said to skip BSTS and PSM; kept here only as reference.
- **Fast-moving:** AI referral figures and Shopify data. `[web check: current AI referral share and behaviour]`
- **Legal risk:** false scarcity and inflated social proof ("X in carts", "only Y left") must reflect real data (card). [e18bae3af3dd]

## 10. Card index

- 0eca60fd91617a84cdf061ac: Choose the measurement design that matches the ecommerce decision
- f671352f5b6e382b99d3b277: Prove the net value of a CRO programme with a persistent holdout
- ddbbe8061d1090a09f9918cc: Measure channel incrementality with user-level and geo holdouts
- e353aade03aefafea77661e7: Design geo holdouts with pre-test market matching
- 300b03fc03541fde01ea5ed4: Use valid A/B tests for product and checkout decisions
- c076b110d253f505c1dbae09: Use feature holdouts to measure net revenue, not proxy engagement
- 04a08881ac09768ad3349860: Use causal methods carefully when user randomization is impossible
- 2b951af15841bd9ebd9449d7: Build a causal-learning log for ecommerce decisions
- 9461d45dfbe7bead0e0c54d8: Improve mobile speed with real-user performance measurement
- d4104b13110fbb1430f4f279: Prioritize checkout clarity, guest purchase, and local payment access
- e46b405d55df11eae11a8889: Recover cart abandonment without making discounts the only answer
- e18bae3af3dd771f091c46a8: Put credible trust information beside the buying decision
- 1e03a58f6fe1be8b07032a3b: Design category pages for browsing and mobile refinement
- 5e578ca91bcc244dd046c555: Route homepage visitors with selective personalization and constrained choice
- 86c233f0eb395b308de762a8: Confirm the brief for AI-referred product-page visitors
- 25f9d85cd8e363cdb4527de6: Diagnose funnel constraints with stage metrics and revenue per session
- fc7c739888fcdf8372969363: Make PDPs sales-ready before scaling traffic
- 93fdbe5da8f2a9a7fee7f0d2: Use the revenue equation to prioritize CRO investments
- 373e2f9d659ae5968c9e0950: Select a CRO tool stack by the measurement job
