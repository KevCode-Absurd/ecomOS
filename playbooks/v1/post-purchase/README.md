# Post Purchase — draft playbook

**Status:** source-linked draft; not owner-approved or outcome-tested.

Read [the operating contract](../OPERATING_CONTRACT.md) before using a workflow.

## Inputs
- Orders/delivery events
- support issues
- product lifecycle
- consent
- policies

## Measures
- Support resolution
- refunds
- repeat purchase
- contribution

## Foundation candidates
Inferred principle labels do not establish universal applicability. Retain source conditions; empty means no matched labelled principle, not absence of foundational knowledge.

- **Problem-solve with low effort and over-recover failures** (`df383902e95dcd522d58bace`): Never engineer failures, but make recovery exceptionally generous when they happen because the downside of a bad fix is far larger than the upside of a good one.
  Applies when: When writing support policy, refund authority limits, or handling a specific failure such as a lost parcel or damaged item.
  Condition: 5.4% is a banking-study figure; rates in e-commerce are not established.
  Condition: Generous over-recovery creates abuse risk; set caps by order value and monitor patterns.

- **Reconcile effort reduction and delight across the journey** (`36baf5a5a8ad38f21fc8a5a3`): Resolve the 'delight vs effort' debate by cutting friction in service moments and adding designed peaks only in discretionary ones.
  Applies when: When allocating post-purchase CX or retention budget and deciding whether to invest in support/returns fixes or unboxing/surprise moments.
  Condition: The 'delight pays' case is contested; treat big surprise programs as brand/word-of-mouth plays, not guaranteed retention math.
  Condition: The HBR/Effortless Experience study is the peer-reviewed anchor; most delight benchmarks are vendor-sourced.

- **Prioritize the Retention Hierarchy Before Touching Email and SMS** (`290bef9daa56a500ad07a194`): Fix product quality, product portfolio, acquisition quality and customer experience before expecting owned media to rescue retention.
  Applies when: Repeat purchase rate or 90-day LTV is flat and you're tempted to invest in more email flows, SMS or Klaviyo work as the first fix.
  Condition: This is the source's stated hierarchy and opinion; it is not a universal law, and brands with a strong product may still get quick wins from flows.
  Condition: Owned media can genuinely amplify retention once foundations are sound — the caution is about using it to mask a broken product or portfolio.

## Design product onboarding
Workflow ID: `post-purchase.onboarding`

**Deliverable:** Onboarding sequence and content brief

### Proposed decision sequence
1. Identify delivery and first-use friction from real evidence
2. Provide useful instructions at appropriate lifecycle moments
3. Measure support needs and customer outcomes before adding upsells

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Convert shipping and delivery emails into education touchpoints
Card: `6d6e184eb84866186d1e8f11` · Source: E-commerce Customer Delight Journey.docx · Section: 0

Replace bare tracking notifications with prep instructions and outcome timelines to reduce post-purchase dissonance and build anticipation for the peak.

Applies when: Designing the order-confirmation, shipping, and delivery-notification sequence for any product that requires setup or a routine.

- Assume the period between purchase and delivery creates anticipation plus subconscious anxiety (post-purchase dissonance) — silence breeds it.
- For each post-purchase email, add product-specific education instead of only a tracking link: how to prepare before the product arrives, what physical sensations to expect on first use, and a realistic timeline to visible results.
- Use the messages to reinforce the correctness of the buying decision, which is the stated purpose of combating dissonance.
- Sequence them so the last message before delivery sets up the unboxing moment as the peak.
- Keep expectations accurate here — an inflated timeline claim becomes negative disconfirmation later.
- **Condition:** The source presents this as a design principle for considered or routine-based products (its example is a personalized skincare regimen); for commodity reorders, the education payload may be thin.
- **Condition:** Don't overload transactional emails with content that delays the tracking information customers actually open the message for.
- **Condition:** Keep transactional messages focused on the order and necessary usage information; place promotional cross-sells in appropriately permitted marketing messages.

#### Exploit the 'Quiet Period' Between Order and Delivery
Card: `578e1e518ece0c8c289d84a1` · Source: E-commerce Customer Delight.docx · Section: 0

Treat the window after purchase but before delivery as a relationship-building period using education, onboarding and community content.

Applies when: Planning lifecycle messaging for stores where delivery takes days and customers are switching from a familiar product or brand.

- Identify the anxiety or uncertainty a new customer feels while waiting — the source's example is Bobbie, an infant formula brand, whose customers are parents switching formulas.
- Send education and onboarding content during the wait so the customer is confident and knows what to do when the product arrives; Bobbie uses milestone-based communications tied to a baby's development.
- Combine this with predictive refill models and a flexible subscription so needs are met as the customer's situation evolves.
- Apply the same logic in ecommerce categories with a learning curve (e.g., a new coffee setup, complex skincare routine) by sending setup guidance before the parcel lands.
- **Condition:** Bobbie's milestone approach depends on predictable, developmental triggers specific to infant formula; adapt the mechanism, not the exact content, to your category.

#### Reconcile effort reduction and delight across the journey
Card: `36baf5a5a8ad38f21fc8a5a3` · Source: Customer delight across the e-commerce journey_ a retention playbook.docx · Section: 0

Resolve the 'delight vs effort' debate by cutting friction in service moments and adding designed peaks only in discretionary ones.

Applies when: When allocating post-purchase CX or retention budget and deciding whether to invest in support/returns fixes or unboxing/surprise moments.

- Separate the journey into service/problem moments (returns, WISMO, complaints, checkout) and discretionary moments (unboxing, onboarding, milestones, payment perk).
- In service moments, reduce effort: one-touch resolution, fast refunds, proactive updates, no dark patterns. The 2010 HBR study of 75,000+ service interactions (Dixon, Freeman, Toman) found 96% of high-effort customers became more disloyal vs 9% of low-effort ones.
- In discretionary moments, engineer a limited number of peaks using Heath's four elements (elevation, insight, pride, connection) rather than spreading budget across the forgettable middle.
- Sequence spend: fix effort and broken promises first, then add peaks, because evidence that effort drives defection is much stronger than evidence that delight drives loyalty.
- Track both: WISMO rate and return-to-refund time for the effort side; repeat rate, review rate and UGC for the peak side.
- **Condition:** The 'delight pays' case is contested; treat big surprise programs as brand/word-of-mouth plays, not guaranteed retention math.
- **Condition:** The HBR/Effortless Experience study is the peer-reviewed anchor; most delight benchmarks are vendor-sourced.

### Retrieval and applicability
Search: `post purchase onboarding product use support expectations`
Related domains: email-lifecycle, avatars, wild-bets
Mixed-folder candidate IDs: 7a84d0a050408eaaf77b3e84, b29e7060f44b7ad53174d9e0, c34cee3e77b8134b84fb5623

- Does this advice fit the product lifecycle, market, audience and requested deliverable?
- Does it require proof, access, budget or assets the brand does not have?
- Does it change a fixed price, offer, policy or other explicit constraint?
- Are platform details or numerical claims current and substantiated?

### Output checks
- Deliver the specified artifact, not general advice about creating it.
- Use supplied brand facts; label hypotheses and missing inputs separately.
- Preserve relevant source conditions; do not copy another business’s proof or results.
- Include an owner, measurement and decision rule when proposing a test.
- Check the output against the requested constraints and owner feedback.

Stop after the requested artifact passes factual and brief checks; allow at most two revision passes, then report the unresolved issue.

## Design a service recovery response
Workflow ID: `post-purchase.service-recovery`

**Deliverable:** Customer response and internal recovery action

### Proposed decision sequence
1. Establish the actual issue and approved remedies
2. Resolve the failure clearly before suggesting additional purchases
3. Record root cause and follow-up ownership

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Problem-solve with low effort and over-recover failures
Card: `df383902e95dcd522d58bace` · Source: Customer delight across the e-commerce journey_ a retention playbook.docx · Section: 0

Never engineer failures, but make recovery exceptionally generous when they happen because the downside of a bad fix is far larger than the upside of a good one.

Applies when: When writing support policy, refund authority limits, or handling a specific failure such as a lost parcel or damaged item.

- Recognize the service recovery paradox is real but rare: Michel and Meuter's study of 11,000+ banking interviews found only 63 of 1,189 customers with a problem perceived recovery as 'much better than expected' (5.4%).
- It appears when the failure is not severe, the customer had no prior failure, and the recovery is exceptional and better than expected.
- When a failure happens, over-recover deliberately: empower reps to refund without escalation, tell a customer to keep or donate the product rather than ship it back, and send a human gesture.
- Reach out proactively when something breaks, before the customer complains. Organizational-learning research shows the paradox appears most when the customer sees the firm took action.
- Do not engineer failures to create recovery opportunities: Michel and Meuter concluded error-free service still beats recovery on overall satisfaction.
- Track first-contact resolution, CSAT and repeat rate among customers who experienced a failure.
- **Condition:** 5.4% is a banking-study figure; rates in e-commerce are not established.
- **Condition:** Generous over-recovery creates abuse risk; set caps by order value and monitor patterns.

#### Test faster refunds with clear customer choice and eligibility
Card: `0f70a58b8a2ba8b2eb762030` · Source: E-commerce Customer Delight.docx · Section: 0

Collapse the refund timeline from 10–14 days to seconds or minutes to recapture purchase intent at its peak.

Applies when: Selecting a refund method or negotiating refund timelines with your returns platform and finance team.

- Consider faster eligible refunds and optional store credit; the source's Reebok case reports higher repurchase among customers choosing instant refunds, which does not establish causation.
- Present original-payment refunds and optional credit clearly according to the store's applicable policy. Do not silently replace a refund with wallet credit to retain revenue.
- Measure refund-related tickets and subsequent purchases in comparable cohorts; vendor case results are hypotheses for testing.
- Use the speed benchmarks available in-market: Auchan averages 10-minute refunds (Fintecture, €22 million refunded in 2022); Bayse Brand refunds in under 30 seconds (Refundid); Riverford refunds within 30 minutes (Worldpay Faster Refunds).
- Track request-to-initiation and initiation-to-receipt times separately, refund method, abuse losses and 60-day repurchase. Model eligibility and cash needs before scaling.
- **Condition:** The 11x and 85% figures are vendor case studies from specific brands, not transferable benchmarks; instant refunds carry fraud and cash-flow considerations the source does not address.
- **Condition:** Store credit is a distinct option, not an equivalent cash refund; availability and processing speed depend on payment method and provider.

#### Build brand agents with a distinctive voice instead of generic AI bots
Card: `7de1741d65327cafe5154f55` · Source: 9 Customer Experience Trends for 2026 by Steven Van Belleghem.docx · Section: 0

Generic AI bots will sound identical and forgettable, so the source urges companies to build 'brand agents' that embody the company's unique voice and tone.

Applies when: You are deploying a customer-service chatbot or shopping assistant and need to decide how much investment goes into voice and brand personality versus pure functionality.

- Before writing dialogue flows, define the brand's voice in concrete terms (tone, vocabulary, pacing, what the brand would never say) and use it as the spec for the agent.
- Draft sample conversations and have people familiar with the brand judge whether the agent is recognizably your brand, testing the source's bar: users should know they're talking to your brand, like Apple, Disney or Lego agents.
- Match personality to the use case: a pragmatic, calm voice for a logistics brand versus an energetic one for a fitness brand, rather than one generic helpful-assistant tone.
- Protect voice through every update so it doesn't flatten back to generic chatbot phrasing as the system scales.
- Warn stakeholders that defaulting to off-the-shelf technology, as the source puts it, flattens your differentiating brand aspect.
- Monitor voice consistency alongside resolution and conversion metrics, and review transcripts regularly for drift.
- **Condition:** This is the source's forward-looking argument, not a benchmarked outcome; brand voice has no standard metric.
- **Condition:** A strongly voiced agent still requires accurate information and reliable resolution to be useful.

### Retrieval and applicability
Search: `support failure resolution refund policy customer experience`
Related domains: email-lifecycle, avatars, wild-bets
Mixed-folder candidate IDs: 2c4a21f438205d730e0564cc, e2d412db7e876186ef0cc882, e17963c7293b1575bb8d9667

- Does this advice fit the product lifecycle, market, audience and requested deliverable?
- Does it require proof, access, budget or assets the brand does not have?
- Does it change a fixed price, offer, policy or other explicit constraint?
- Are platform details or numerical claims current and substantiated?

### Output checks
- Deliver the specified artifact, not general advice about creating it.
- Use supplied brand facts; label hypotheses and missing inputs separately.
- Preserve relevant source conditions; do not copy another business’s proof or results.
- Include an owner, measurement and decision rule when proposing a test.
- Check the output against the requested constraints and owner feedback.

Stop after the requested artifact passes factual and brief checks; allow at most two revision passes, then report the unresolved issue.

## Plan a relevant repeat-purchase intervention
Workflow ID: `post-purchase.repeat-purchase`

**Deliverable:** Retention intervention brief

### Proposed decision sequence
1. Determine whether replenishment or complementary purchase is plausible
2. Select an eligible segment and useful timing from product lifecycle
3. Check contribution and compare outcomes without assuming causation

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Segment Post-Purchase Flows by First-Time, Repeat and VIP Buyers
Card: `e13b48c6a15a1a2a3b47a509` · Source: E-commerce Customer Delight.docx · Section: 0

Build distinct post-purchase email flows per customer segment, using education for new buyers and early access for VIPs.

Applies when: Restructuring lifecycle email and on-site experience so loyal customers do not receive the same treatment as first-time shoppers.

- Segment your base into first-time buyers, repeat buyers and VIPs.
- For first-time buyers, focus the flow on education and brand story.
- For repeat buyers, focus on cross-selling into adjacent categories.
- For VIPs, focus on early access, exclusive experiences and recognition.
- Consider adding non-discount rewards — early access, exclusive content or experiential benefits — to differentiate from points-only competitors.
- Apply the same logic on-site: Princess Polly identified that multi-purchase customers received the identical on-site experience as one-time buyers and used personalization to make loyal customers feel valued.
- For lapsed customers, send valuable content instead of generic discounts: Matas, the Danish beauty retailer, ran a personalized re-engagement sequence that achieved a 29-point retention lift within 30 days while driving 20% more orders.
- **Condition:** The Matas and Princess Polly results are single-brand examples; the source does not specify the exact segmentation criteria or cadence beyond first-time/repeat/VIP.

#### Use CAC Payback Period for Subscription-first Brands
Card: `d1160b9862c5da7244221db7` · Source: The Complete E-Commerce Retention Masterclass.docx · Section: 1

When first-purchase gross profit is below CAC, track the point at which cumulative subscription or replenishment profit repays the deficit.

Applies when: Running a supplements, CPG or subscription store that knowingly loses money on the first order.

- Accept the Day 0 loss explicitly. Example: $50 CAC vs $45 first-order gross profit = negative $5 contribution.
- Track the CAC payback period: the date at which cumulative gross profit from the cohort crosses the initial deficit and the brand starts earning profit.
- Drive it with retention levers — subscription depth, replenishment cadence, second/third purchase rates — because every additional repeat inside the payback window shortens the period.
- Use the payback period as a standing KPI on the finance dashboard alongside contribution margin, since it directly ties retention tactics to how fast cash returns.
- Before scaling, model how much capital you can afford to have tied up while cohorts are in the red — payback is a working capital constraint as much as a profit one.
- **Condition:** The specific $50/$45 figures are an illustrative example, not a benchmark.
- **Condition:** Requires a category with high repeat rate and natural replenishment; this framework does not fit one-off or durable-goods purchases.

#### Educate customers across the journey to drive repeat purchase
Card: `55f0042df14c6c6ba61d7ef8` · Source: Customer delight across the e-commerce journey_ a retention playbook.docx · Section: 0

Match content to stage: teach the problem at awareness, trade-offs at consideration, first use in the delivery gap and advanced use in retention.

Applies when: When planning content, email or video assets against specific stage outcomes to reduce returns and increase repeat rate.

- Awareness: teach the problem and the desired outcome, not the spec. Beardbrand built 1,000+ YouTube grooming videos (1.6M+ subscribers) that fed its move from online-only to Target; Glossier built Into the Gloss community before product.
- Consideration: teach trade-offs and fit through quizzes, comparison pages, AR and UGC; tell customers when a product is not right for them to cut returns and earn trust.
- Delivery gap: teach first use and build anticipation with drip emails and SMS while the customer waits; boAt sends usage instructions plus a next-order discount.
- Onboarding: send a personalized day-by-day usage plan tied to the purchased item and outcome; measure activation rate and 60-day repeat rate.
- Retention: teach advanced use and adjacent needs via newsletters and replenishment tips to set up cross-sell.
- Measure content-attributed signups and assisted conversions; content with no link to the product problem is just cost.
- **Condition:** Beardbrand and Glossier are illustrative examples, not controlled studies of content ROI.
- **Condition:** Long-form content is personality- and resource-intensive; Dollar Shave Club-style viral content is hard to repeat.

### Retrieval and applicability
Search: `repeat purchase retention lifecycle replenishment cross sell`
Related domains: email-lifecycle, avatars, wild-bets
Mixed-folder candidate IDs: 3d5541e52ed085fe57e0c37d, 9bf05e0dda65b0f199a4bc03, 81635c2e6b2563fbcf652d88

- Does this advice fit the product lifecycle, market, audience and requested deliverable?
- Does it require proof, access, budget or assets the brand does not have?
- Does it change a fixed price, offer, policy or other explicit constraint?
- Are platform details or numerical claims current and substantiated?

### Output checks
- Deliver the specified artifact, not general advice about creating it.
- Use supplied brand facts; label hypotheses and missing inputs separately.
- Preserve relevant source conditions; do not copy another business’s proof or results.
- Include an owner, measurement and decision rule when proposing a test.
- Check the output against the requested constraints and owner feedback.

Stop after the requested artifact passes factual and brief checks; allow at most two revision passes, then report the unresolved issue.
