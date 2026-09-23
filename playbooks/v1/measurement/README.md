# Measurement — draft playbook

**Status:** source-linked draft; not owner-approved or outcome-tested.

Read [the operating contract](../OPERATING_CONTRACT.md) before using a workflow.

## Inputs
- Shopify/analytics/ad reports
- date range
- timezone
- currency
- attribution and event settings

## Measures
- Reconciliation gaps
- duplicate events
- purchase coverage

## Foundation candidates
Inferred principle labels do not establish universal applicability. Retain source conditions; empty means no matched labelled principle, not absence of foundational knowledge.

- **What the Meta Conversions API Gateway actually is** (`94681676110e5db4248c1ecd`): A hybrid setup where the client-side pixel fires as usual and also relays the same event to a first-party subdomain gateway that forwards it to Meta's Conversions API.
  Applies when: Deciding how to add server-side conversion tracking to an ecommerce store when you have no developer resources and are considering the Meta CAPI Gateway instead of a full server-side tag manager.
  Condition: The vendor claims (e.g. average cost-per-result improvements up to 13% and ~7% more conversions) are vendor-reported figures, not guarantees; the source argues real-world results are lower because of the architecture.
  Condition: This is one practitioner's opinion (Analytics Mania); treat the recommendation against the gateway as a situational judgment, not a universal rule.

- **Measure purchase conversion rate, not raw key event rate** (`d5605a4c54a85175d75c9743`): GA4's 'key events' bundle purchases with other actions, so you must manually filter to the purchase event before reading any conversion rate.
  Applies when: Judging whether your store's or a channel's conversion rate is healthy before making merchandising or media-spend decisions.
  Condition: The source's own store showed ~1.7% conversion rate after filtering to purchase; treat that as an example, not a benchmark.
  Condition: GA4's interface changes over time, so verify the current click path before relying on it.

- **Compounders vs Linear Metrics in Ecommerce** (`3a1918a526e2ca564e3733ce`): Conversion rate and referral coefficient compound revenue and customer growth, so prioritize them over one-off linear levers.
  Applies when: Deciding whether to invest next month's budget in CRO, referral program, or a linear traffic/spend increase.
  Condition: The arithmetic examples are illustrative of compounding logic, not measured outcomes.
  Condition: The source's position that CRO should come first is his opinion; it assumes you have enough traffic to measure conversion changes reliably.

## Reconcile ecommerce performance reports
Workflow ID: `measurement.reconcile-reports`

**Deliverable:** Reconciliation table and confidence notes

### Proposed decision sequence
1. Align dates, timezone, currency and metric definitions
2. Separate test orders, refunds and attribution differences
3. Explain remaining gaps without forcing platforms to match

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Read the Monetization reports for purchase revenue, items, and list/promotion breakdowns
Card: `2fa8beb663c84c75bab7e12f` · Source: Google Analytics Tutorial For Beginners (2026 Update).docx · Section: 0

Use GA4 ecommerce reports to see purchase revenue, purchasers, items bought, list membership, promotions and coupon revenue.

Applies when: You're reviewing store revenue performance in GA4 and want to break down purchases by product, list placement or promotion code.

- Open Monetization > Overview: Total Revenue is the value from all events; Purchase Revenue is transaction revenue only. They match unless you've assigned dollar values to non-purchase events.
- Note which metrics are user-based (purchasers, first-time purchasers) versus event-based (purchase revenue).
- Check the top items card for the products selling most.
- Scroll to the item list, promotion and coupon code cards to see which collections, promotions and discount codes are driving purchases — these depend on that data being sent to GA4.
- Open Ecommerce Purchases for a more granular item-level table; change the dimension dropdown to slice differently.
- Use the Purchase Journey and Checkout Journey reports for the funnel views, and transaction-ID reports for reconciliation with your platform.
- **Condition:** Coupon, promotion and list reporting only works if those parameters are implemented on your store's events.
- **Condition:** Revenue metrics depend on correct value/currency parameters being sent, not on GA4 inferring them.
- **Condition:** For attribution of purchased revenue across campaigns, use the Advertising reports rather than the Monetization reports.

#### Landing page vs pages and screens report
Card: `5c2c65569229cb75e24a9bc8` · Source: Google Analytics 4 tutorial for beginners (2026) __ GA4 tutorial for beginners __ GA4 course.docx · Section: 1

Use the landing-page report for session entry pages and pages-and-screens for total page views, and understand why revenue in the pages report can mislead.

Applies when: Evaluating which entry pages (homepage, collections, checkout URL) start sessions and drive revenue, versus measuring overall page popularity.

- Use the Landing page report to see the FIRST page of each session and revenue attributed to those entry sessions — useful for judging which entry points (homepage, new arrivals, clearance) actually produce revenue.
- Use Pages and screens for total page views regardless of position in the session, plus users and active users per page.
- Sort Pages and screens by views or users to find the most-visited pages; be aware revenue in this report is attributed to the page where the conversion occurred, so almost all revenue lands on checkout — the presenter considers revenue unhelpful here.
- Interpret 'active users': a user who spent at least 10 seconds, converted (a key event), viewed 2+ pages in a session, or is a new user.
- Expect checkout URLs to appear as landing pages when a session expires mid-purchase — a visitor who leaves after adding to cart and returns later can start a new session with checkout as the landing page.
- To reduce that false signal, consider raising the default session timeout (see the session-timeout card).
- **Condition:** Revenue in the pages-and-screens report is attributed to the conversion page, making it near-useless for judging page value.

#### Reconcile platform attribution with self-reported attribution
Card: `7f3bed7f5dd10de0d154589f` · Source: eCommerce Marketing Data 101_ Derric Haynie's Crash Course on Understanding Data Analytics.docx · Section: 0

Expect and plan for the gap between what ad platforms claim and what customers say drove the purchase.

Applies when: When Google Ads or a social platform reports conversions that zero-party survey data does not corroborate, and you must decide budget.

- Pull platform-attributed conversions for a channel for a defined window.
- Pull post-purchase survey answers naming that channel for the same window.
- Compute the gap and treat the platform number as directional, not exact — consent loss and tracking prevention cause platform numbers to miss or over-claim.
- If a platform over-claims relative to self-reported attribution, avoid cutting it solely on the platform number until you test incrementality.
- If self-reported attribution names channels the platform cannot see (word of mouth, podcasts, offline), preserve budget there even without a tracked conversion.
- **Condition:** Neither number is ground truth; they measure different things (tracked touchpoints vs stated memory).
- **Condition:** The source treats self-reported attribution as often the more honest signal, which is a stance, not a proven rule.

### Retrieval and applicability
Search: `attribution revenue reconciliation purchase conversion`
Related domains: finance-and-accounting, testing, google-ads
Mixed-folder candidate IDs: 2b34d63c3b0e9a1a1a46a7c2, 0c79d63f1e16217a8de39c51, b07800dfb7024d82679b03e0

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

## Audit purchase tracking
Workflow ID: `measurement.audit-events`

**Deliverable:** Tracking audit and verification steps

### Proposed decision sequence
1. Map browser/server events to actual purchase actions
2. Check identifiers, values and duplicate-event handling
3. Specify a controlled validation and document missing permissions

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Deduplicating pixel and Conversions API events with matching IDs
Card: `90f2da80bf6715aa1b7c163c` · Source: Facebook Conversions API gateway tutorial (FB CAPI Gateway a.k.a. Meta CAPI gateway).docx · Section: 0

The gateway auto-attaches the same event ID to both the browser pixel event and the server-side event so Meta can deduplicate the pair.

Applies when: Verifying your conversion tracking after installing the CAPI Gateway, or diagnosing double-counted purchases and inflated conversion counts.

- After connecting your pixel to the gateway, open the Meta Pixel Helper on a live page and confirm an event ID is now present on the pixel event.
- Open DevTools Network, filter for 'facebook', and locate the request going to your gateway subdomain.
- Inspect that request's payload and confirm the same event ID appears that you saw in the Pixel Helper.
- Confirm the event IDs match for each event type (page view, AddToCart, Purchase, etc.); mismatched or missing IDs mean deduplication will fail and conversions may be double counted.
- Monitor Events Manager after a few days for duplicate-event warnings or unexpected conversion volume jumps from dedup failures.
- **Condition:** Deduplication ID handling is automatic with the gateway; if you build custom server-side tagging you must manage event IDs yourself.
- **Condition:** Meta's interface and deduplication diagnostics change over time — verify current behavior in Events Manager.

#### Redundant Meta Ads tracking: browser pixel plus server Conversions API
Card: `0b762a5084497ce6d49600c1` · Source: Install Facebook (Meta Ads) Conversion API with server-side GTM.docx · Section: 0

Meta's recommended setup fires the same event twice — once from the browser pixel and once from the server-side Conversions API — then merges them with deduplication.

Applies when: Planning or auditing the tracking architecture that feeds Meta Ads purchase and lead optimization for your store, e.g. after iOS/ad-blocker signal loss hurts reported ROAS.

- Keep the standard Facebook/Meta pixel firing client-side from your normal GTM container, and add server-side tags that send the same events to the Conversions API from a server-side GTM container.
- Treat the result as two streams for the same event: the presenter shows this as the setup Meta recommends, framed as a redundant setup where the same event is tracked twice.
- Verify in Meta Events Manager that each event appears once from the browser and once from the server (the presenter demos a PageView and a Contact event showing both sources).
- Do not stop at 'both are firing' — without deduplication Meta would count the event twice, so pair this with matching Event IDs on both streams.
- Note the server event often arrives later than the browser event, so check again a moment after the browser event appears before concluding the server tag failed.
- In the server container's preview mode confirm each Meta tag reports 'succeeded'; a failed/succeeded=false result usually points to a wrong or malformed API access token.
- **Condition:** Redundancy without deduplication means double counting; the two parts must ship together.
- **Condition:** Setup depends on an existing server-side GTM container and consent mode configuration; the presenter treats this as a follow-on to those tutorials.

#### Measure purchase conversion rate, not raw key event rate
Card: `d5605a4c54a85175d75c9743` · Source: Google Analytics 4 For eCommerce 2025 ( Perfect for beginners).docx · Section: 0

GA4's 'key events' bundle purchases with other actions, so you must manually filter to the purchase event before reading any conversion rate.

Applies when: Judging whether your store's or a channel's conversion rate is healthy before making merchandising or media-spend decisions.

- Understand the trap: in GA4, key events are not only purchase events; page views, add-to-carts and other actions can be marked as key events.
- When you add the 'session key event rate' metric to any report, drill into the metric and set the event filter explicitly to 'purchase'.
- Only then read the percentage as your conversion rate.
- Sanity-check the result against total revenue in the same table so you are not reading a rate built on the wrong event set.
- Re-check this filter after any GA4 configuration change, since the key-event set can drift over time.
- **Condition:** The source's own store showed ~1.7% conversion rate after filtering to purchase; treat that as an example, not a benchmark.
- **Condition:** GA4's interface changes over time, so verify the current click path before relying on it.

### Retrieval and applicability
Search: `pixel conversions API deduplication event purchase`
Related domains: finance-and-accounting, testing, google-ads
Mixed-folder candidate IDs: 2c720c61a3755f9ab26ca915, e2b6cdb21e10af8714dad979, 256e8f1a95e79889b2523bb7

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

## Define the business metric contract
Workflow ID: `measurement.metric-contract`

**Deliverable:** Metric dictionary and reporting contract

### Proposed decision sequence
1. Define numerators, denominators and data sources
2. Specify aggregation grain and attribution limits
3. Attach freshness and missing-data handling to each metric

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Product Sell-Through Rate for Inventory Planning
Card: `37f16297a48eca6d9aba563d` · Source: What Metrics Matter In The Shopify Analytics Dashboard.docx · Section: 0

Track sell-through rate at product and category levels to optimize inventory, cash flow, and sustainable growth.

Applies when: When planning inventory purchases, managing cash conversion cycle, or deciding which products to reorder or discontinue.

- Access Shopify Analytics > Reports > Products by sell-through rate (or similar report at the bottom of the dashboard).
- Calculate sell-through rate as units sold divided by units received over a period.
- Monitor sell-through by product and category to identify fast vs. slow movers. High sell-through means you can reorder more frequently and reduce stockouts; low sell-through ties up cash.
- Use sell-through insights to adjust purchasing quantities and timing, aiming to reduce excess inventory and improve cash flow.
- Link sell-through to your net profit margin and cash conversion cycle: higher sell-through allows faster reinvestment and growth.
- **Condition:** Sell-through alone doesn't account for profitability; combine with margin analysis.
- **Condition:** The source notes this is often overlooked by new brands but is critical for scaling.

#### Prevent fragmented sessions by extending GA4 session timeout
Card: `c91c77718ecd716817eb6e32` · Source: Google Analytics 4 tutorial for beginners (2026) __ GA4 tutorial for beginners __ GA4 course.docx · Section: 0

GA4's default 30-minute session timeout can split a single shopping journey into multiple sessions, distorting engagement and conversion metrics.

Applies when: Configuring a new GA4 property or investigating why session counts and conversion rates look inflated or fragmented for a store with long browse-to-purchase lag.

- Open GA4 Admin > Data Streams > select the stream > Configure Tag Settings (or the data stream's session settings depending on current UI).
- Locate the session timeout setting, which defaults to 30 minutes.
- Increase it toward the allowed maximum (the source cites up to 7 hours and 55 minutes) when customers commonly leave and return within a browsing session on the same device.
- Weigh the tradeoff: a longer timeout keeps a single journey intact but can merge genuinely separate visits into one session, lowering apparent per-session conversion rate.
- Re-check the resulting session and conversion-rate reports after the change to confirm the shift matches the store's real buying behavior.
- **Condition:** Choosing the maximum is not automatically correct; the source presents extending the timeout as a fix for fragmented sessions, not a universal requirement. Test against the store's actual purchase lag.

#### Predictive Analytics and AI Execution in Ecommerce
Card: `0f952763382f7a926c89c414` · Source: eCommerce Marketing Data 101_ Derric Haynie's Crash Course on Understanding Data Analytics.docx · Section: 1

Analytics has moved from humans explaining charts to AI recommending actions — and increasingly executing them — so stores that adopt predictive tools and AI-run tests are positioned to outcompete slower adopters.

Applies when: Deciding where to apply AI in merchandising, ad creative, attribution, on-site conversion or customer service, or fending off 'AI will hurt our brand' objections.

- Understand the shift: previously all analysis meant organizing data, choosing comparative metrics, and having a human explain the graph; now predictive tools use past data and regression-style machine learning to estimate, e.g., that a 5% ad-spend increase will move new customers and revenue while cost of acquisition stays roughly steady.
- The next step the source predicts is AI not just predicting but executing: generating and running landing-page or creative variants, reading conversion rate as the objective, and feeding results back to improve the next generation.
- Set human boundaries rather than hands-on involvement: guardrails like 'no misspelled words, no profanity' while letting the system test broadly — adding humans slows the loop and makes it less data-driven.
- Expected near-term displacements named by the source: media agencies need fewer people for running tools (strategy remains), creative and content-writing teams shrink toward one editor, customer service largely automates with escalation, and merchandising can be AI-selected, including testing demand before placing a purchase order.
- Adapt rather than resist: the source notes brands blocked by antiquated practices or a HiPPO veto on AI in customer service risk cost structures that competitors beat.
- **Condition:** These are the source's predictions for the next three to five years, not observed results — treat timelines as speculative.
- **Condition:** The 'one in a thousand' customer-service problem rate is the speaker's estimate, not a benchmark; test escalation paths before fully automating.

### Retrieval and applicability
Search: `conversion rate attribution analytics profitability`
Related domains: finance-and-accounting, testing, google-ads
Mixed-folder candidate IDs: e2b6cdb21e10af8714dad979, 38c80ae68029672e69cd13ce, 64c447f737c2d49c9136cc12

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
