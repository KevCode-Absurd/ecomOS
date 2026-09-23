# Ecommerce intelligence owner-value evaluation

Nine workflows, three models, three retrieval methods. Complete side-by-side inputs, cards and outputs: [comparison document](OWNER_BENCHMARK_COMPARISON.html).

| Model | Context | Owner score /4 | Both reviewers: use /9 | Mean input tokens | Mean completion tokens | Mean cold cost | Median cold seconds |
|---|---|---:|---:|---:|---:|---:|---:|
| gpt-5.6-luna | none | 3.41 | 1 | 2920 | 2578 | $0.0038 | 18.5 |
| gpt-5.6-luna | raw | 3.15 | 0 | 12855 | 3001 | $0.0068 | 25.2 |
| gpt-5.6-luna | selected | 3.24 | 0 | 5741 | 3112 | $0.0090 | 34.6 |
| gpt-5.6-terra | none | 3.34 | 1 | 2972 | 2501 | $0.0374 | 32.2 |
| gpt-5.6-terra | raw | 3.73 | 3 | 12877 | 3092 | $0.0693 | 33.6 |
| gpt-5.6-terra | selected | 3.71 | 2 | 5752 | 2853 | $0.0525 | 46.4 |
| gpt-5.6-sol | none | 3.78 | 6 | 2970 | 3058 | $0.0760 | 47.8 |
| gpt-5.6-sol | raw | 3.75 | 5 | 12873 | 3632 | $0.1370 | 64.6 |
| gpt-5.6-sol | selected | 3.90 | 8 | 5693 | 3790 | $0.1081 | 73.2 |

Scores are advisory model judgments. Completion tokens include reasoning. First four tasks include draft + revision; remaining five have one draft. Cold cost and latency include an unamortized selector for selected context. The selector was actually run once per task and reused.

Current evaluation ledger including interrupted V2: $8.5618, excluding tiny separately logged query embeddings.

## Process

1. Freeze the same fictional Shopify/Meta/Klaviyo brand and task for every condition.
2. Run two task-specific hybrid searches, merge duplicate IDs, and record all candidate cards.
3. Compare no cards, all broad candidates, and Luna-selected applicable cards. Selected text is copied intact with conditions; selection explanations never enter the answer prompt.
4. Generate each deliverable with Luna, Terra and Sol at medium reasoning. Save exact input, output, usage and timing.
5. For inventory, audience, experiment and reconciliation tasks, run deterministic field checks and allow exactly one revision for every condition. No platform writes occur.
6. Randomize candidate labels for two simulated owner reviews. Evaluate practical usefulness, brand fit, correctness, clarity and handoff readiness.
7. Audit keyword versus hybrid candidates, coverage, applicability and freshness gaps. These are judgments about retrieved candidates, not complete-library recall.

## Task-by-task retrieval trace

### E1: Inventory-aware acquisition and offer decision

Use Shopify product economics, stock and Meta evidence to produce a 14-day acquisition decision and a usable campaign-change draft. Evaluate the proposed 20% Daypack discount at $30 CAC. Owner has not approved discounts. Reserve 30 Daypacks as an inventory buffer. Replenishment is 35 days away. Explain the distinction between ad CPA and total demand. Submit a proposed daily_total_daypack_units_cap, discount_percent and launch_status. Include actual ad copy, budget decision, dependencies and missing evidence.

Broad: 24 cards / 6552 tokens. Selected: 7 cards / 1752 tokens.

Selected cards:

- Calculate pre-marketing contribution using explicit delivery costs (`013834b51f3c09687d62b861`)
- Recalculate contribution and break-even acquisition cost before discounting (`c49b93d6bb680198b6d98962`)
- Choose the discount/CAC mix that maximises total contribution margin (`993ecc7a19f08496eb4203ec`)
- Zero-to-One Paid Test Campaign Framework (`92354a4e70a243a65fa1780a`)
- Size test budgets from target conversions, CPA, and duration (`1c683e007b76790275ae9f51`)
- Rotating Hooks and Angles Before Adding Media Budget (`df475f552102d5f042b874f4`)
- Judge creative at the adset level, not the ad level (`ab729ba34368891859d923c9`)

### E2: Build and test an abandonment audience

Build a three-email checkout recovery draft and select exactly the eligible customer IDs from the event fixtures. Today is 2026-09-23T12:00:00Z. Eligibility: consent true; checkout at least 2 hours but no more than 48 hours ago; no subsequent purchase; not in welcome flow; no email in last 24h. No discount approved. Provide subjects, actual body copy, delays, purchase suppression, collision handling, and selected_customer_ids. Explain how Shopify events and Klaviyo eligibility interact. Draft only.

Broad: 21 cards / 6228 tokens. Selected: 5 cards / 1558 tokens.

Selected cards:

- Trigger Abandoned Checkout on checkout started With Order Filtering (`85117c7d09108698841362fb`)
- Flow structure and profile filters in Klaviyo (`dfc548f661d230535e9993aa`)
- Abandoned cart/checkout email content: 3-stage objection sequence (`bdbde349add0546ce9c3f6f8`)
- Write plain, item-first recovery copy that overcomes objections (`abb2fb64e79c352922b4d261`)
- Link Abandonment Emails Directly Back to Checkout (`79cdac8bb86eba4c7cf16b77`)

### E3: Mobile PDP experiment with resource scheduling

Produce implementation-ready mobile PDP copy, FAQ, section order, and an experiment configuration. Only 1200 eligible PDP sessions per week exist; baseline purchase rate 2%, minimum detectable absolute improvement 0.4 percentage points. Analyst supplied required sample 21000 sessions TOTAL; use it, do not recalculate a different test. Propose test_days, designer_hours, developer_hours, claimed_statistical_significance and launch_status. Build needs 6 designer and 3 developer hours; QA needs another 2 developer hours. Only 4 developer hours are available in week one, 4 in week two. Include schedule/dependencies and how you avoid false proof after a 14-day test. No verified 15-inch fit or speed data.

Broad: 24 cards / 6732 tokens. Selected: 7 cards / 1984 tokens.

Selected cards:

- Resolve pre-purchase objections beside product, cart and checkout actions (`f62861431f319d58c0f7e055`)
- Answer four purchase questions above the fold (`bb761687ad68b66f17ed0215`)
- Configure Shopify product page section settings (`2efef89fb3bf8bc56b2dccd0`)
- Make PDPs sales-ready before scaling traffic (`fc7c739888fcdf8372969363`)
- Require statistical power before acting on a test (`c546525713365ccb5fffcdb4`)
- Plan A/B tests around calculated sample size, duration, randomization, and QA (`4d0785cdcf2b3e6fa3ffcb41`)
- Only run A/B tests that can reach valid decisions (`699a7cd5ac4c6774df818a33`)

### E4: Cross-channel reconciliation and executable audit

Create an order-level reconciliation table and a concrete next-week resource plan. Shopify net revenue 45000 includes a $1000 refund already deducted. Meta exported 400 orders totaling 48000; 80 Meta orders totaling 9600 are outside the Shopify reporting period. Klaviyo exported 120 orders totaling 14000, all in-period. Of in-period orders, 50 orders worth 6000 overlap Meta and Klaviyo. Compute in_period_meta_value, union_attributed_value and unassigned_shopify_value. These are attribution matches, not incremental sales. Build an audit task list with owner, acceptance test, dependency, hours and decision gates. Max analyst hours 6, developer 4, owner 2; do not double-subtract the refund or scale based on the blended attribution union.

Broad: 24 cards / 6619 tokens. Selected: 6 cards / 1695 tokens.

Selected cards:

- Revenue Attribution: Separating Platform-Driven Sales from Total Store Revenue (`f836216a37bb843c5f2b8b40`)
- Configure smart sending and attribution windows (`1ce671434e00d36d94a1ea0c`)
- Balance Attribution and Profitability Metrics in Your Owned Media KPIs (`2df157249026bbe0fbaa206c`)
- Shift from ROAS to financial-based KPIs for scaling decisions (`17393d9c2d71e4abeecfdd45`)
- Measurement pyramid: platform metrics, finance-grade KPIs, incrementality (`d5c2a3d880d97c51367259dd`)
- Using Incrementality to Find the Marketing That Doesn't Work (`89eb781b3bd2677e0b167f91`)

### E5: Agency creative production brief

Create three distinct static Meta ad briefs for Daypack: one iteration of desk-to-trail, one laptop-fit objection concept and one fresh positioning hypothesis. Give actual headline/body/CTA, image composition, production instructions and a single-variable test plan. Allocate no more than 8 designer hours total. No competitor performance or testimonial is verified. These are production drafts; inventory is constrained. Return actions.concepts as a list and actions.designer_hours. Write for a designer and media buyer to use today.

Broad: 24 cards / 7327 tokens. Selected: 7 cards / 2279 tokens.

Selected cards:

- Write creative briefs with six mandatory fields before producing ads (`377393f355c6053df5e1edc3`)
- Design Static Ads Around the Eye's Reading Path (`08f49b8491b0ead3b3cc138b`)
- Run single-variable creative tests within the same angle (`1c4808b43997d5b85feb4b1c`)
- Concept = Persona × Angle × Offer × Format (`ab5dac71c1dc0cd369d1d52c`)
- Testing Priority Order: Angle First, Then Offer, Persona, Format (`4a3ce680ae23e5eb6e943fd6`)
- The One-Element Ad — Strip To The Essential Component (`7272fafc80c75a09a6cd3508`)
- Common hook types and when to use each (`9197d49f4af43881e5fb28e4`)

### E6: Paid-traffic landing page build brief

Build a landing-page wireframe and final copy for a Meta ad promising clarity about the Daypack laptop sleeve. Give hero, benefits, fit guidance, objection blocks, shipping/returns, CTA destinations and mobile acceptance checks. Unknown: actual internal sleeve dimensions and whether a 15-inch laptop fits. Give clearly marked placeholders for missing facts rather than inventing them. Preserve ad-to-page message match, prioritize what can ship, and provide a developer handoff within 4 developer hours. Return actions.section_order and actions.developer_hours.

Broad: 24 cards / 6590 tokens. Selected: 7 cards / 1902 tokens.

Selected cards:

- Match each campaign promise to the product landing page hero (`3cefd472f3802645bf11d970`)
- Match the Product-Page Hero to Traffic Awareness (`af3eaeba1a44d8149e6d521d`)
- Put purchase-critical PDP information in a scannable first screen (`3ff3c8b062b05b89cb32bf0f`)
- Resolve pre-purchase objections beside product, cart and checkout actions (`f62861431f319d58c0f7e055`)
- Match authentic product reviews to purchase objections (`cca2df9310c11fcf077b964c`)
- Direct response design rules for the page (`28056fad0269d1716f8e3659`)
- Answer four purchase questions above the fold (`bb761687ad68b66f17ed0215`)

### E7: Accessory bundle profitability and offer copy

Owner asks: should we offer a Daypack plus Cable pouch bundle for $90? For this scenario only, combined landed COGS $33, pick-pack $2.50, merchant shipping $8.50, payment fee 3%, expected new-order CAC $30. Single Daypack economics remain as in brand facts. Calculate bundle pre_ad_contribution and after_ad_contribution, compare with full-price Daypack, and draft offer copy. No additional discount or launch approved. Address cannibalization and limited Daypack stock; do not use unmeasured LTV to rescue the offer. Return actions.bundle_pre_ad_contribution, actions.bundle_after_ad_contribution and actions.launch_status.

Broad: 20 cards / 5714 tokens. Selected: 6 cards / 1551 tokens.

Selected cards:

- Fund bundle value from fulfillment economics (`d5a74f7edaddf9e1113337fb`)
- Build offers with bundles, gifts, and relevant one-click upsells (`0ca0ef2a3d5d5b8d8411ac56`)
- Evaluate Offers by Profit Per Session (`1cda5c627ada2689fcdd4b93`)
- Model Fixed Costs Across Bundle Tiers Before Discounting (`471fc0881800ba3b8799ea5e`)
- Use bundles to give value without eroding gross margin percentage (`e345aac91cf443d84d08c371`)
- Strategic bundling and making savings obvious (`fa82d767b9520ad3c9e9c974`)

### E8: Post-purchase retention flow

Create a practical post-purchase email flow for first-time Daypack buyers with three actual emails: useful onboarding, review request and optional accessory cross-sell. Include event/timing, eligibility, suppression, returns/refunds, delivery uncertainty and a small holdout measurement. Bags are durable goods, not replenishable subscriptions. Do not request a review before confirmed delivery or imply known repeat-purchase lift. Return actions.emails with subject/body/timing and actions.primary_metric. Make it ready for an agency CRM specialist to configure after verifying event fields.

Broad: 24 cards / 6787 tokens. Selected: 6 cards / 1818 tokens.

Selected cards:

- Sequence the Post-Purchase Flow Around Shipping, Usage, Loyalty, Reviews and Cross-Sell (`0a935c9bd0919223a8ba4c36`)
- Design Post-Purchase Flows Around First-Time vs. Returning Customers (`55898f20e16116a726da3dca`)
- Capture reviews with a specific, low-friction post-purchase ask (`cf03cf0f0e81168879f6a1dd`)
- Convert shipping and delivery emails into education touchpoints (`6d6e184eb84866186d1e8f11`)
- Use feature holdouts to measure net revenue, not proxy engagement (`c076b110d253f505c1dbae09`)
- Build buyer, non-buyer and repeat-buyer segments for tailored messaging (`7ccc6c565f867390e76167f0`)

### E9: Weekly client update and agency task handoff

Write a client-facing weekly update using the supplied 30-day comparisons, explicitly saying these are 30-day data rather than inventing a weekly trend. Explain the conversion and Meta/Shopify discrepancy plainly. Give three priorities only, decisions needed from the owner, and an internal task board with owners, dependencies, acceptance checks and hours. Weekly limits: designer 8, developer 4, owner 4. Include an inventory-aware go/no-go rule. Do not claim a completed audit or promise revenue uplift. Return actions.priorities, actions.designer_hours, actions.developer_hours and actions.owner_hours.

Broad: 24 cards / 6663 tokens. Selected: 6 cards / 1851 tokens.

Selected cards:

- Reconcile Platform Data Against the P&L (`2b34d63c3b0e9a1a1a46a7c2`)
- Diagnose Growth Bottlenecks Through a Data-Integrity First Lens (`4f1e89e8a7983a564e1122a0`)
- Five core finance practices to run an ecommerce brand (`8d570963a07c01bd206aac7f`)
- Build a Weekly Forecasting Rhythm Even as a Solo Operator (`94c5d797f80b138ba47d3111`)
- The Daily 3: Cut to Three Needle-Movers (`bcee1e69de7698ae45475b5d`)
- Balance Attribution and Profitability Metrics in Your Owned Media KPIs (`2df157249026bbe0fbaa206c`)

## Limits

- Single fictional brand and one sample per cell; no statistical or revenue proof.
- Reviewers are models simulating owner perspectives, not actual owners. Reviewer models share family with candidates; rankings can be biased.
- First four tasks have an extra revision, applied equally to every condition. Structured checks cover only limited fields, not the entire artifact.
- E1/E3 original checks confused equivalent field names/types with decision errors. All 18 affected conditions were revised again from their INITIAL draft using corrected semantic checks. Original revisions are preserved. Per-workflow metrics show the active draft+corrected-revision path; discarded diagnostic revision costs/timing are separate and included in the budget ledger.
- Queries were authored for the experiment and frozen across models. Autonomous query planning and live platform tool execution are not tested.
- No exhaustive relevance labels over all 7611 cards: cannot claim full recall. Metadata and freshness labels are inferred, not independently verified.
- Costs are conservative estimates, not invoices; every input token charged at cache-write allowance.
- Concurrency influences observed latency. Cold workflow sums serial stages; cached packets can remove selection latency.
- No new Astra comparison; earlier easier tasks cannot establish Terra beats Astra.
- Different prompts from V1/V2 prevent direct historical score comparisons.

Pricing references: [Luna](https://developers.openai.com/api/docs/models/gpt-5.6-luna), [Terra](https://developers.openai.com/api/docs/models/gpt-5.6-terra), [Sol](https://developers.openai.com/api/docs/models/gpt-5.6-sol). Exact billed cost must be reconciled with the provider invoice.