# Testing — draft playbook

**Status:** source-linked draft; not owner-approved or outcome-tested.

Read [the operating contract](../OPERATING_CONTRACT.md) before using a workflow.

## Inputs
- Funnel counts
- dates
- traffic segments
- page evidence
- margins
- previous experiments

## Measures
- Contribution per visitor
- purchase conversion
- uncertainty

## Foundation candidates
Inferred principle labels do not establish universal applicability. Retain source conditions; empty means no matched labelled principle, not absence of foundational knowledge.

- **Combine quantitative and qualitative research into test hypotheses** (`25979af2691c4a3b80d31a69`): Use funnel and heatmap evidence to locate shopper friction, then surveys and interviews to explain it before choosing a page or offer change.
  Applies when: Creating a prioritized CRO backlog for a PDP, cart, checkout, or paid-traffic landing page instead of redesigning from preference.
  Condition: The source gives illustrative tools and examples but no sample-size or interview-protocol requirements.
  Condition: A below-the-fold guarantee issue is an example, not evidence that every store should move guarantee content upward.

- **Use exit and post-purchase surveys to separate purchase friction from purchase motivation** (`f89dbadb9131e6dc051f86c6`): Ask abandoning shoppers what stopped them buying and ask new buyers what motivated them or nearly prevented purchase, then use recurring themes to improve PDPs, carts, checkout, and landing pages.
  Applies when: You need voice-of-customer evidence to prioritize ecommerce conversion hypotheses rather than inferring objections solely from behavioral data.
  Condition: Exit surveys represent only visitors who see and elect to answer them; buyer surveys cannot explain non-buyer behavior.
  Condition: The source gives no response-rate, sample-size, or representativeness benchmark.
  Condition: Do not confuse post-purchase survey work intended for marketing attribution with CRO research; attribution setup belongs in the measurement workflow.

- **Reduce PDP and checkout friction with ease-of-use changes** (`8accb09355e613be3f2ee7db`): Make the path from product evaluation to checkout clear and low-effort by reducing unnecessary input, surfacing the primary action, and explaining what happens next.
  Applies when: Shoppers view products or begin checkout but abandon before adding to cart, completing a product quiz, or placing an order.
  Condition: The source does not establish an optimal number of checkout or quiz fields.
  Condition: Some required information is necessary for fraud prevention, tax, shipping, or customer service; do not remove it without assessing those trade-offs.

## Diagnose an ecommerce conversion bottleneck
Workflow ID: `testing.diagnose-funnel`

**Deliverable:** Bottleneck diagnosis with evidence and next actions

### Proposed decision sequence
1. Reconcile funnel definitions and isolate relevant traffic segments
2. Connect numerical drop-offs with page and customer evidence
3. Rank hypotheses by impact, evidence and implementation cost

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Use funnel analysis and heatmaps to locate purchase friction
Card: `9568c40e1d888b7224c2468a` · Source: Conversion Rate Optimization Framework Revealed - Step By Step Breakdown.docx · Section: 1

Map drop-off, clicks, scroll depth, and false clicks to identify where shoppers fail to reach or complete purchase.

Applies when: Beginning a CRO audit or diagnosing a drop in PDP-to-cart, cart-to-checkout, or checkout-to-purchase performance.

- Map the journey from paid ad or entry page through PDP, cart, checkout, thank-you page, and any upsell flow; identify the largest abandonment points.
- Use analytics to understand where people leave, even if a full GA4 audit is not practical at lower traffic volumes.
- Install a heatmap tool on key product pages and inspect click maps, scroll behavior, and scroll depth. The source names Microsoft Clarity as a free option and Heatmap.com as a revenue-oriented alternative; verify current tool capabilities and setup.
- Check whether important selling points are placed where shoppers actually see them. The source cites a case where a critical factor near the footer reached only about 6% of visitors.
- Identify false and rage clicks, especially on elements that resemble buttons, links, or controls but do not work, then remove that friction.
- Use findings to form test hypotheses or fix clear defects, and pair them with qualitative research to learn why behavior occurred.
- **Condition:** The source's 6% visibility example is a single case, not a target or benchmark.
- **Condition:** Heatmaps identify behavioral patterns but do not by themselves explain shopper intent.

#### Prioritize CRO in five levels: clarity, copy, offer, proof, friction
Card: `9e7d2fb74d831fb8a621e3f7` · Source: eCommerce CRO Masterclass 2026_ The Full System.docx · Section: 1

Use a five-part sequence to identify high-leverage store changes, beginning with immediate page comprehension and ending with purchase friction.

Applies when: Creating a CRO roadmap, auditing a PDP, or deciding which conversion issue to address before running lower-impact tests.

- Audit in this order: clarity and hierarchy, copy, offer, proof, then friction. Ask whether a shopper can immediately understand the product and page structure before refining persuasion.
- Fix clarity and hierarchy first when the defect is obvious. The source considers these relatively fast, high-leverage improvements that generally do not require split testing.
- Improve copy by connecting the product to the shopper’s desired outcome and removing doubt; then assess whether the offer itself is sufficiently compelling.
- Add proof that validates claims and the product mechanism, then remove practical barriers that obstruct checkout or product selection.
- Use the same order as a PDP structure: clear value proposition first, then persuasive explanation of the unique mechanism, then offer, proof, and friction reduction.
- Recognize the tension in the framework: the source says offer quality may have the largest impact, but ranks it after early page fixes because building a strong offer is much harder.
- **Condition:** This is the presenter’s ICE-informed prioritization judgment, not a statistically derived universal order.
- **Condition:** Do not interpret the sequence as a rule that offer problems can wait indefinitely; a poor offer can suppress conversion despite polished copy and design.

#### Audit a product or landing page with the six-part CRO framework
Card: `bdded17187e0c768ff62f21e` · Source: COMPLETE Revenue-increasing Conversion Rate Optimisation (CRO) Course.docx · Section: 0

Review a shopper journey through Credibility, Lure, Objection Handling, Social Proof, Ease of Use, and Result to identify the specific gaps suppressing purchase.

Applies when: You are prioritising improvements to a PDP, collection landing page, cart, checkout, or product-quiz page before commissioning a redesign or launching tests.

- Audit the page in six focused passes rather than judging it as a whole. Credibility asks whether shoppers can believe the brand, product claims, and merchant. Lure asks whether the next action has a clear benefit, such as finding the right variant or seeing delivery eligibility. Objection Handling asks whether doubts about buying or proceeding are answered.
- Assess Social Proof: can shoppers see that comparable people bought, used, or rated the product? Assess Ease of Use: is the route to select a variant, add to cart, and check out obvious and low effort? Assess Result: after the conversion action, does the process deliver the promised outcome, such as a valid recommendation, order confirmation, or stated promotion?
- Record gaps as concrete hypotheses, such as “no delivery reassurance beside Add to Cart,” “reviews are below the decision area,” or “the product quiz promises a recommendation but does not explain what the shopper receives.”
- Rank gaps by likely effect on purchase or margin and implementation cost, then test or implement the highest-priority changes. Re-audit after changes because strengthening one element can expose another weakness.
- **Condition:** This framework diagnoses likely friction; it does not itself establish which change will produce the largest revenue lift.
- **Condition:** Treat assessments of proof strength or clarity as hypotheses to validate with shopper research and experiment data.

### Retrieval and applicability
Search: `CRO audit funnel checkout product page friction`
Related domains: measurement, landing-pages, offers
Mixed-folder candidate IDs: d771afe27917bb503cc77039, c33859641d7d1e37f0ac59dc, 3d3e2b815f9bad06fb978df4

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

## Design a conversion experiment
Workflow ID: `testing.design-experiment`

**Deliverable:** Experiment specification

### Proposed decision sequence
1. Specify one causal hypothesis and a clear control
2. Define primary metric, guardrails, duration and sample rationale
3. Record allocation and decision rules before launch

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Use valid A/B tests for product and checkout decisions
Card: `300b03fc03541fde01ea5ed4` · Source: CRO fundamentals.docx · Section: 0

Reliable ecommerce A/B testing requires a causal hypothesis, one primary business metric, adequate sample size, randomization, and a fixed stopping plan.

Applies when: Testing a PDP layout, trust message, category-page interaction, checkout field change, or merchandising treatment.

- Write a hypothesis in the source’s IF/THEN/BECAUSE format: IF the change is made, THEN a specified shopper outcome will improve, BECAUSE of a stated behavioral reason.
- Prioritize the backlog with PIE, ICE, or CIE so high-potential, important, feasible ideas are tested before cosmetic preferences.
- Choose one primary metric tied to purchase value—typically conversion rate or revenue per session—and define guardrails such as AOV, refund rate, margin, or checkout completion where relevant.
- Calculate the necessary sample size and set traffic allocation and duration before launch. Randomize properly and keep groups balanced.
- Do not peek and stop when a result looks favorable. Run through the planned duration unless a pre-specified safety or business rule requires intervention.
- Use multivariate tests only when traffic can support the number of combinations; sequential A/B tests are safer at lower volume.
- Where appropriate, use CUPED with pre-experiment variables such as prior purchase frequency or browsing history to reduce variance and improve sensitivity.
- **Condition:** The source names prioritization frameworks but provides no scoring scales or sample-size formula.
- **Condition:** A cited 61.1% win rate and 1.879 ROI describe one programme, not a target for another store.

#### Write a pre-registered test brief with a real decision rule
Card: `1b7725e0ff57f1b5fc24d1c1` · Source: CRO as testing and experimentation for DTC ecommerce.docx · Section: 0

A test brief should connect evidence to a change, segment, MDE, primary metric, guardrails, validity checks, and actions for win, loss, or inconclusive outcomes.

Applies when: Approving a PDP, cart, checkout, product-quiz, or retention-flow experiment before design and development begin.

- Use the structure: because we observed specific evidence, we believe a stated change will cause a defined effect for a stated shopper segment, measured by a named primary metric.
- Set the MDE and sample requirement in advance, then state the action for a win, loss, or inconclusive result.
- Choose conversion rate for faster power, or revenue/gross-profit metrics where order value is central and traffic supports them.
- Define guardrails such as AOV, margin, refunds, returns, page speed, and downstream purchase conversion.
- Pre-register important segments, including device, paid versus organic, and new versus returning shoppers, rather than searching them after the result.
- Specify runtime as at least a full week—usually two—plus time to reach the planned sample.
- Include an SRM check, tracking QA, and the method or stopping rule that makes monitoring valid.
- **Condition:** A micro-conversion can be primary for a low-traffic diagnostic test, but purchase and revenue should remain guardrails.
- **Condition:** A post-hoc segment result can seed a follow-up test but should not be presented as the registered result.

#### Turn Clarity evidence into a testable ecommerce hypothesis
Card: `6d2e6fafa7df9f658707accc` · Source: Microsoft Clarity COMPLETE Tutorial in 2026 to Skyrocket Conversions.docx · Section: 0

Move from maps and recordings to a single observable change hypothesis tied to shopper reach, interaction, and purchase-path progression.

Applies when: Converting Clarity findings into a prioritized experiment or implementation brief for a PDP, collection, cart, checkout, or landing page.

- Define the page's single intended progression: view a product, select a variant, add to cart, begin checkout, or complete checkout.
- Use click and scroll maps to establish whether shoppers reach the relevant section and interact with the intended element. Locate the most specific apparent barrier, such as a long block before add to cart, a hidden filter, a misleading static banner, or missing delivery information.
- Open recordings for the same page, device, and behaviour to validate that the map pattern reflects actual shopper friction and to understand the likely intent.
- Write a focused hypothesis in change-and-reason form: for example, 'Because shoppers repeatedly return to the top to change the collection filter, test a persistent filter trigger so refinements remain available while browsing products.'
- Specify the behaviour to evaluate after release: reach to add-to-cart, CTA click share, filter use without scroll-back, PDP views from collection, cart starts, checkout progression, or purchase conversion. Choose the metric appropriate to the page's role.
- Use this qualitative evidence to prioritize the test, then apply the store's normal experiment design and sample-size calculation before making causal claims about conversion or revenue.
- **Condition:** Clarity demonstrates behaviour and supports hypotheses; it does not by itself establish causality or statistical significance.
- **Condition:** The source demonstrates the diagnostic loop but does not provide experiment outcomes or a statistical testing design.

### Retrieval and applicability
Search: `experiment hypothesis testing sample conversion`
Related domains: measurement, landing-pages, offers
Mixed-folder candidate IDs: 61ad59932aa7f6f212be0c8f, 899c0cfa0cb1d30d6fad78be, c5c9a8f05d83cc6e43f0f40d

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

## Interpret experiment results
Workflow ID: `testing.interpret-test`

**Deliverable:** Experiment readout and next decision

### Proposed decision sequence
1. Check data integrity and whether the planned exposure was achieved
2. Compare business impact with uncertainty and guardrails
3. Choose adopt, reject or inconclusive with a justified follow-up

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Only run A/B tests that can reach valid decisions
Card: `699a7cd5ac4c6774df818a33` · Source: eCommerce CRO Masterclass 2026_ The Full System.docx · Section: 2

Assess sample needs, contamination, multi-click exposure, and time-to-purchase before treating an A/B result as evidence.

Applies when: Planning a landing-page, PDP, checkout, or offer test—or evaluating a claimed CRO winner from an agency or internal team.

- Calculate required sample size for the baseline conversion rate, minimum effect worth detecting, confidence level, and statistical power. The source illustrates that detecting a 10–20% lift at a 2.5% conversion rate can require about 1,000 conversions and roughly 40,000 sessions per variant, but calculate the actual requirement for the store.
- Check whether the relevant page can get that traffic within a sensible period and before seasonality, inventory changes, or campaign shifts invalidate the comparison.
- Do not inspect results daily and stop as soon as significance appears. The source warns that this practice greatly increases false positives.
- Prevent contamination: campaign blasts, retention traffic, and other high-intent sources can distort landing-page tests. Where appropriate, route a controlled cold-traffic source to dedicated test pages.
- Account for repeat clicks and cross-exposure. A shopper who sees more than one variant may dilute or bias a simple split-test comparison.
- Use primary business metrics such as revenue or contribution per visitor alongside purchase conversion, and document exclusions and test dates.
- **Condition:** The source's traffic figures are illustrative estimates, not a universal sample-size rule.
- **Condition:** A/B tests are most feasible where purchase cycles are short and relevant traffic volume is high; lower-volume stores may need stronger qualitative evidence and larger, less frequent changes.

#### Use win-rate benchmarks only with their definitions
Card: `8dc46d4893e1ff71d673eb5e` · Source: CRO as testing and experimentation for DTC ecommerce.docx · Section: 0

Ecommerce testing win rates vary from roughly 8% to 36% because samples and definitions differ, so use benchmarks to calibrate expectations rather than promise outcomes.

Applies when: Setting expectations for a merchant’s experimentation program or evaluating a vendor’s testing-performance claim.

- Use approximately 10–20% statistically significant winners as the conservative general expectation for well-run experiments cited in the source.
- Keep the denominator and definition attached to every number: significant wins per test, raw directional winners, decisive results, and revenue-tied wins are different measures.
- The source cites large-program results around 8–15% in optimized contexts such as Airbnb Search, Bing, Google Ads, Booking.com, and Netflix; an Optimizely meta-analysis of about 20,000 experiments found 10% statistically significant uplift on the primary metric.
- Interpret higher results in context. DRIP’s 36.3% ecommerce figure reflects research-prequalified hypotheses and a looser win definition; it should not be compared directly with significant-per-test rates.
- Calibrate expected effect sizes by maturity: the source characterizes 1–5% lifts as realistic on mature pages and 10–20%+ as possible on early or unoptimized experiences.
- Treat 50%+ claims as audit and replication candidates, particularly when based on small samples or early stopping.
- **Condition:** Benchmarks do not establish that a specific store test will win or determine its sample size.
- **Condition:** Small-sample winners are especially exposed to false positives and exaggerated effect estimates.

#### Plan A/B tests around calculated sample size, duration, randomization, and QA
Card: `4d0785cdcf2b3e6fa3ffcb41` · Source: Conversion Rate Optimization Framework Revealed - Step By Step Breakdown.docx · Section: 1

Use randomized traffic, adequate duration and calculated sample requirements before acting on an A/B-test result.

Applies when: Launching a purchase-conversion experiment on a product page, landing page, cart, checkout, or navigation flow.

- Define the primary purchase metric and calculate the sample size needed from the baseline rate, minimum meaningful effect, confidence requirement, and desired power before launch.
- The source commonly runs roughly 50,000–100,000 sessions depending on test location and recommends at least two weeks, preferably two to four, so weekday effects repeat.
- Randomize visitors between control and variation. Use multiple variations or multivariate designs only when traffic is high enough to support them.
- Distinguish statistical significance from statistical power: a result may look unlikely to be random without having enough data to be reliably repeatable or commercially meaningful.
- Do not run conflicting tests on the same page area. Separate tests can run on, for example, a homepage and cart, or clearly distinct page regions.
- QA each experience two or three times before launch; broken tracking, layouts, or CTAs can turn a viable variation into an apparent loser.
- **Condition:** The source's traffic and duration ranges are operating conventions, not replacements for an actual sample-size calculation.
- **Condition:** Its preference for above-the-fold, larger changes reflects the source's testing bias rather than a rule for every experiment.

### Retrieval and applicability
Search: `experiment significance sample uncertainty conversion results`
Related domains: measurement, landing-pages, offers
Mixed-folder candidate IDs: c0a38656da11fd84c8789595, 859209042dcd562e2d7dcd47, 6ef2415cede852f58bb7944e

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
