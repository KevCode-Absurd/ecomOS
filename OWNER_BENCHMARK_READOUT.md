# Is the ecommerce intelligence layer worth it?

**Promising for Terra and Sol; not yet a universal improvement.** In this nine-workflow pilot, selected expert cards improved Terra's average owner-oriented score from 3.34 to 3.71/4, and Sol's from 3.78 to 3.90. Luna fell from 3.41 to 3.24. This is evidence to keep developing the layer selectively, not proof of commercial ROI or that more context always helps.

**Start here: [side-by-side comparison document](OWNER_BENCHMARK_COMPARISON.html).** Choose a task and any two model/context combinations. Expand the exact input, full card text, provider token usage, initial/final outputs, action checks and both reviewer perspectives. Everything is self-contained; there are no remote scripts or services.

[Full results and selected card lists](OWNER_BENCHMARK_RESULTS.md) · [Metrics CSV](data/ecommerce-owner-benchmark-v3/metrics.csv) · [Human owner rating sheet](data/ecommerce-owner-benchmark-v3/human-owner-review.csv)

## What we tested

One fictional Shopify brand, TrailFold, with product prices/costs, inventory, Meta Ads reporting, Klaviyo reporting, customer questions, constraints and team capacity. Every model received the same brand facts. There were no real customer records or live platform changes.

| Workflow | Requested deliverable |
|---|---|
| E1 | Inventory-aware acquisition decision, discount economics and campaign-change draft |
| E2 | Eligible customer IDs from event fixtures plus three actual abandonment emails |
| E3 | PDP copy, experiment configuration and build/QA schedule |
| E4 | Cross-channel reconciliation and a staffed audit plan |
| E5 | Three static-ad concepts, finished copy, visual briefs and testing plan |
| E6 | Paid-traffic landing-page wireframe, copy and developer handoff |
| E7 | Accessory bundle economics, offer copy and launch decision |
| E8 | Post-purchase onboarding, review request and accessory cross-sell flow |
| E9 | Client-facing update and an agency task board |

Nine tasks × three models × three methods = **81 completed comparisons**. The methods were no cards, broad retrieved cards, and applicability-selected cards. Exact models were `gpt-5.6-luna`, `gpt-5.6-terra` and `gpt-5.6-sol`, all at medium reasoning. No new Astra or DeepSeek calls were made.

E1–E4 included a draft, deterministic action-field checks and one revision. E1/E3 needed a corrected validation pass because the original checker confused equivalent field names/types with bad decisions. All 18 affected conditions received the same corrected pass from their initial draft. Original revisions, costs and feedback remain available. This tests drafting and limited execution readiness, not autonomous tool use or real deployment.

## Results from an owner perspective

Two anonymized reviews per task: Sol simulated a business owner; Terra simulated an agency owner. They judged usefulness, brand fit, correctness, clarity and handoff readiness. These are **model judgments, not real customer satisfaction scores**. Shared model-family bias and one generation per condition limit the conclusions.

| Model | No cards: score /4 | Broad cards: score /4 | Selected cards: score /4 | Selected versus no cards |
|---|---:|---:|---:|---|
| Luna | 3.41 | 3.15 | 3.24 | Improved 3 tasks; declined 6 |
| Terra | 3.34 | 3.73 | 3.71 | Improved 7 tasks; declined 2 |
| Sol | 3.78 | 3.75 | 3.90 | Improved 3; tied 5; declined 1 |

Both reviewers chose “use” for 8/9 Sol-selected outputs versus 6/9 Sol baseline outputs. Terra-selected scored close to Sol baseline on average, but both reviewers chose “use” for only 2/9 Terra-selected outputs. **Do not equate similar average scores with equal readiness.** There is no new matched Astra comparison, so this cannot establish that Terra beats Astra.

### Concrete value and failures

- **Checkout recovery:** Terra moved from 2.40 to 3.675/4 with selected cards. The baseline scheduled messages 18 hours apart while also requiring no email in the previous 24 hours, and used Daypack-specific details without product branching. Selected guidance improved the draft. Even with correct customer IDs, the full flow still needs operational review.
- **Agency update:** Terra moved from 2.55 to 4.00/4 with selected cards. The result combined the inventory constraint, reporting caveats and a capacity-compliant task board. The improvement is useful in this case, but a single generation does not establish a repeatable causal effect.
- **Luna agency update:** Selected context produced a worse answer. It confused a flat add-to-cart count with a flat rate: 2,000/20,000 is 10%, while 2,000/25,000 is 8%. Its hour allocations also disagreed. Context did not prevent basic execution errors.
- **Creative briefs:** Selected context did not beat baseline on any of the three models in the averaged review. Useful source guidance was present, but audience definitions, distinct concepts and controlled-test instructions still needed editing. Do not force a tiny packet when the task needs broader coverage.
- **Landing-page work:** Broad cards helped Terra more than the selected packet in this trial. This is a reason to select for required capabilities, not simply minimize the number of cards.

Some reviewer flags are debatable. For example, an agency reviewer treated `launch_status: draft` as a critical problem in one offer answer although the generation prompt explicitly allowed draft or blocked. We preserved the review rather than silently changing scores. Read the evidence and use the human rating sheet before treating small score differences as meaningful.

## Retrieval, context size and time

Broad retrieval provided **20–24 cards and 5,714–7,327 knowledge tokens** per task. Selection retained **5–7 cards and 1,551–2,279 tokens**, a **72.3% reduction** across the nine packets. This was a result of selecting applicable cards, not a hard 2,000-token cap.

Median timing for two task-specific queries:

- New hybrid retrieval: **1.26 seconds**.
- Cached-query hybrid retrieval: approximately **75 milliseconds**.
- Keyword-only retrieval: approximately **53 milliseconds**.
- Additional Luna applicability selection: **13.58 seconds**.

Keyword-only retrieval was audited for candidate relevance, not tested as a separate answer-generation condition. “Cached hybrid” measures cached query retrieval, not an independently tested whole-response cache. Selection adds latency on new requests; storing a versioned selected packet can avoid that repeated work, but its suitability must be invalidated when brand facts or source content change.

The relevance audit found real improvements in the selected candidate mix, and also omissions. The email selection omitted available Shopify-event validation guidance; attribution candidates lacked a full export-join procedure. We examined the retrieved candidate union, not every card in the 7,611-card library. **We cannot claim exhaustive recall.**

## Token and cost trade-offs

The figures below average the active workflow: initial draft plus revision for E1–E4, one draft for E5–E9. Input includes instructions, brand, task, cards and previous draft/feedback where applicable. Completion tokens include reasoning. Selection cost is included as if paid anew for each selected workflow; in the experiment, packets were created once and reused. Superseded diagnostic revisions are separately logged and included in the evaluation budget.

| Model / method | Mean input tokens | Mean completion tokens | Mean estimated cost | Median total seconds |
|---|---:|---:|---:|---:|
| Luna / none | 2,920 | 2,578 | $0.0038 | 18.5 |
| Luna / broad | 12,855 | 3,001 | $0.0068 | 25.2 |
| Luna / selected | 5,741 | 3,112 | $0.0090 | 34.6 |
| Terra / none | 2,972 | 2,501 | $0.0374 | 32.2 |
| Terra / broad | 12,877 | 3,092 | $0.0693 | 33.6 |
| Terra / selected | 5,752 | 2,853 | $0.0525 | 46.4 |
| Sol / none | 2,970 | 3,058 | $0.0760 | 47.8 |
| Sol / broad | 12,873 | 3,632 | $0.1370 | 64.6 |
| Sol / selected | 5,693 | 3,790 | $0.1081 | 73.2 |

These are conservative token-cost estimates, not provider invoices. Concurrent calls affect latency. The full current evaluation committed **$8.56**, including reviews, retrieval audits, selection, corrections, query embeddings and the interrupted predecessor's reservations. The completed new stage has no pending requests; six uncertain predecessor requests retain conservative reservations rather than being assumed free.

## How to extract more value next

1. **Organize retrieval around the deliverable.** A creative brief needs audience, angle, copy, visual hierarchy and test design. An email flow needs event eligibility, suppression, product branching, timing, copy and measurement. Fetch enough guidance to cover the required parts; allow broader packets when they add useful coverage.
2. **Keep brand facts and computation separate from guidance.** Calculate margins, stock runway, funnel rates, eligibility and resource totals with deterministic tools. Cards guide the decision; they should not replace arithmetic or current account data.
3. **Turn strong guidance into reusable task procedures.** Define required inputs, steps, output fields and acceptance checks. Preserve expert caveats and source links. Mark missing evidence instead of filling it with generic advice. Cache stable procedures using task family, brand-fact version and library version.
4. **Use stronger models where this trial supports them.** Sol with selected context is the strongest quality candidate here. Terra with context is a promising lower-cost option for reviewed workflows. Luna is a candidate for routing, tagging and extraction; this test does not support it as the default autonomous operator. Validate those smaller jobs separately before relying on that routing.
5. **Make freshness explicit.** Record verified date, scope and review trigger separately from “foundational” or “tactical.” Check changing platform instructions against official documentation and the actual account before execution. Do not label the whole library current because its creators are reputable.
6. **Measure actual owner effort.** Have an operator rate blinded drafts, count required edits and record time to an acceptable deliverable. Then run a limited draft-only agent workflow with real brand data. Revenue impact requires a separate controlled business test; these ratings cannot establish it.

The product value to pursue is a useful, personalized deliverable that needs less operator correction. The card count, retrieved-token count and a polished explanation are not substitutes for that outcome.
