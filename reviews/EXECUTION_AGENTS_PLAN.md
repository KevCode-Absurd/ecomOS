# Execution layer: the agent stack, designed for the full system

Date: 24 Sep 2026. Companion to `INTELLIGENCE_REVIEW.md`. Planning only; nothing built. This version replaces the earlier draft that ranked by what data exists today.

**Assumption, as Kevin set it:** the data warehouse is built and trusted (Meta, Google, GA4, Klaviyo, Shopify, support tickets, reviews, all reconciled daily, gross margin and marketing efficiency computed in code and passed through CAPI). The brand brain is built (facts, claims, offers, voice, competitors, past winners, assets, preferences). The inspiration library is built (own and competitor statics, videos, pages, emails, with structured descriptions and performance). The intelligence layer holds a distilled playbook per workflow plus cards for lookup. The question is only: what are the best possible agents on top, and in what order do they matter.

## 1. How the layer is organised

Three levels. Kevin's 24 subsections live at the middle level.

```
Level 3  PROGRAMS         long-running goals that chain many agents
         Weekly growth review, Launch program (new brand), Quarterly plan, Client report
                |
Level 2  DOMAIN AGENTS    one per use case (the 24 subsections, merged to 20)
         Paid media, Creative, CRO, Profit, Lifecycle, Offer, Landing, Voice of customer ...
                |
Level 1  WORKERS          small, single-purpose, mostly code
         metric puller, sample-size calculator, page fetcher, claim checker, image matcher,
         Lighthouse runner, cohort builder, critic, fact checker, registry writer
```

**The orchestrator** sits above all three. It takes a request or a schedule tick, picks the program or agent, loads the brand brain slice and the playbook, routes the model tier, runs the agent's shape, logs everything, and hands the result to the approval gate. There is one orchestrator, not one per agent.

**Five agent shapes.** Every domain agent is built from one. The shape is built once.

| Shape | What it does | Model use |
|---|---|---|
| A. Audit | Workers check each item against a checklist from the playbook. One model call ranks and explains. | Cheap model |
| B. Diagnose | Workers pull numbers and do the arithmetic. One model call reads them with a diagnostics playbook and writes ranked causes and next actions. | Cheap model; strong model when the numbers conflict |
| C. Create | Load brand brain and avatar, retrieve inspiration matches, draft with a playbook, critic pass, return ranked variants with an audit trail. | Strong model to draft, cheap model to critique |
| D. Experiment | Read the registry, design a test with hypothesis, metric, guardrails, sample size and stop rule, get approval, monitor, write the decision back. | Cheap model, strong model for the hypothesis |
| E. Deliberate | Proposer writes options, challenger attacks them with the brand brain and data, a judge with a fixed checklist scores, human decides. For high-stakes, low-frequency calls only. | Two strong models plus a cheap judge |

**Where debate earns its place.** Shape E costs about 3x a single pass and, per the repo's evidence, AI judges are noisy. So it is reserved for decisions that are rare, expensive and hard to reverse: pricing and offer changes, budget shifts above a threshold, positioning, killing a product, entering a channel. Everything else uses a single critic with a fixed checklist plus code-based checks (prices, arithmetic, banned claims, offer rules).

**Autonomy ladder.** Every agent is born at L1 and earns its way up per action type through the registry.

| Level | Meaning | Example |
|---|---|---|
| L0 | Read and report | Weekly diagnosis memo |
| L1 | Draft for approval | Proposed budget change, ad copy, flow email |
| L2 | Act inside guardrails, report after | Pause an ad above a CPA ceiling for 3 days, add a negative keyword, send a flow email already approved as a template |
| L3 | Act and only report exceptions | Bid and budget pacing inside a monthly cap |

Promotion rule: an action type moves up one level when at least 30 of its proposals were approved unchanged and none caused a logged loss. Anything touching money, customers or public claims never skips a level. Meta stays read-only until Kevin decides otherwise.

**What every agent returns.** The deliverable. The numbers used and the arithmetic. The brand facts relied on. The playbook version and cards used. Cost, tokens and time. A registry entry when a test or action is proposed. Nothing customer-facing mentions the source library.

## 2. Ranking method

Four scores, 1 to 5 each.

- **Money.** How much profit the agent can move per year for a typical brand.
- **Frequency.** How often a brand needs it: 5 daily, 4 weekly, 3 monthly, 2 quarterly, 1 once.
- **AI leverage.** How much of the work an agent can do end to end with full data, versus how much still needs human taste or hands.
- **Compounding.** How much this agent improves the other agents through the brand brain and the registry.

Rank score is the sum. Ties are broken by Money, then Compounding.

## 3. The stack, ranked

### Rank 1. Paid media performance and budget agent

Shape B, then D, with E for large reallocations. Score 19: Money 5, Frequency 5, AI leverage 5, Compounding 4.

- **Mission.** Run the paid engine day to day across Meta, Google and any other channel: find what is wasting money, what is winning, what is fatiguing, where to move budget, and what to test next. Report in contribution terms, not ROAS alone.
- **Runs.** Daily pacing check, weekly deep read, on demand for "what happened".
- **Sub-agents.** Channel readers (Meta, Google Search and Shopping, PMax, TikTok) as workers. Fatigue and frequency worker. Audience overlap worker. Search-term waste worker. Feed health worker. Creative ranker (code plus vision model over own statics and videos). Incrementality reader (holdout and geo tests from the registry). Budget allocator (code: marginal contribution per channel and campaign). Hypothesis writer (model). Test ranker (model, reads registry).
- **Inputs.** Data: ad metrics at ad level with attribution, blended MER and contribution by day, incrementality results, funnel by source. Brand brain: margin targets, cash limits, seasonality, launch calendar, excluded audiences. Intelligence: diagnostics playbooks per channel, scaling gates, fatigue rules. Inspiration: own winners for the creative ranker. Registry: past tests and decisions.
- **Outputs.** Daily exception list. Weekly diagnosis memo with ranked causes. Budget proposal by campaign with expected contribution. Kill, keep, scale list for ads. Top 5 tests. Creative briefs handed to Rank 2. Landing issues handed to Rank 7.
- **Playbooks.** `paid.diagnose-drop`, `paid.pace-budget`, `paid.scale-or-cut`, `paid.rank-tests`, `paid.google-search-hygiene`, `paid.shopping-vs-pmax`, `paid.feed-health`, `paid.incrementality-plan`.
- **Autonomy target.** L2 for pausing above a CPA ceiling and negative keywords; L3 for pacing inside a cap; L1 forever for new campaigns and reallocations above a threshold.
- **Quality gate.** Every number in the memo traces to a query. No recommendation without the contribution effect stated. Guardrail: never propose more than a set percent shift in one day.

### Rank 2. Creative and ad production agent

Shape C. Score 18: Money 5, Frequency 5, AI leverage 4, Compounding 4.

- **Mission.** Keep the account fed with concepts, statics, video scripts and copy that fit the brand, the avatar and the offer, and that learn from what won. Kevin's "match our winners against good formats" idea lives here.
- **Runs.** Weekly batch from Rank 1's briefs, on demand for launches.
- **Sub-agents.** Winner analyst (vision model describes own top and bottom ads, code finds what the winners share). Inspiration matcher (embedding and field match over the library, own and competitor, competitor as layout and mood only). Concept writer (strong model, playbook). Copy writer (strong model, ad-copy playbook from v1.2). Script writer for video and UGC briefs. Static builder (image model with the real product locked as a layer). Claim and offer checker (code). Critic (cheap model, checklist: avatar fit, credible before and after, one clear benefit, no invented claims, voice). Variant planner (one variable per variant).
- **Inputs.** Data: ad-level results, hook and hold rates for video, comment text. Brand brain: facts, claims and proof, offer rules, voice examples, liked and disliked outputs, product photos. Intelligence: copy, concept, hook, UGC and static-format playbooks. Inspiration: everything, with performance. Registry: which angles and formats were already tested.
- **Outputs.** Concept board: 5 concepts, each with the winner pattern it draws on, 3 copy variants, format, reference match, static mockups, video script or UGC brief, and a claim audit. Test plan handed to Rank 3 or Rank 1.
- **Playbooks.** `creative.analyse-winners`, `creative.concept-board`, `creative.static-copy`, `creative.video-script`, `creative.ugc-brief`, `creative.variant-plan`, `creative.hook-library`.
- **Autonomy target.** L1 always for anything public. L2 for internal mockup generation.
- **Quality gate.** Blind pairwise review by Kevin or the client for a rolling sample. Ship, edit or rewrite label feeds learned preferences back to the brand brain.

### Rank 3. Growth experimentation agent (CRO and beyond)

Shape D. Score 17: Money 4, Frequency 4, AI leverage 4, Compounding 5.

- **Mission.** Own the test programme across site, offer, creative and lifecycle. Find the biggest drop, propose tests that are worth running, size them properly, watch them, call them honestly and write the decision back so nothing is tested twice by accident.
- **Runs.** Weekly review, event-driven when a test reaches its sample size.
- **Sub-agents.** Funnel reader (code, by device, source, page template). Opportunity sizer (code: visitors times drop times margin). Test designer (strong model, playbook). Sample size and duration worker (code). Guardrail monitor (code: revenue per visitor, refunds, speed). Result reader (code, with uncertainty). Decision writer (model). Registry keeper.
- **Inputs.** Data: funnel, page performance, experiment platform results, margins. Brand brain: offer rules, constraints, traffic level. Intelligence: CRO playbooks (test selection by traffic, pre-registration, holdouts, reading results). Registry.
- **Outputs.** Ranked test backlog with expected value. Test specs ready for a developer or the landing agent. Readouts with a decision: ship, kill, rerun. A living map of what is known about the funnel.
- **Playbooks.** `exp.find-biggest-drop`, `exp.design-test`, `exp.size-and-guardrails`, `exp.read-result`, `exp.holdout-plan`, `exp.low-traffic-alternatives`.
- **Autonomy target.** L2 for stopping a test that breaches a guardrail. L1 for launching.
- **Quality gate.** No test without a pre-registered metric and stop rule. No "winner" without the uncertainty stated.

### Rank 4. Profit and marketing efficiency agent

Shape B, with E for pricing and cash calls. Score 17: Money 5, Frequency 4, AI leverage 5, Compounding 3.

- **Mission.** Be the CFO view. Contribution by SKU, channel and cohort. MER and contribution after ads by week. Cash tied in stock. Forecasts. Reconcile platform claims to the P&L. Tell the owner where profit is leaking and what it would take to fix.
- **Runs.** Weekly readout, monthly close, on demand.
- **Sub-agents.** Contribution calculator (code). Reconciler (code: platform-reported purchases versus store orders). Cohort LTV worker (code). Forecast worker (code, simple models with error bands). Cash and inventory worker (code). Scenario worker (code: what if price, CAC or return rate changes). Narrator (cheap model, playbook). Anomaly flagger.
- **Inputs.** Data: orders, refunds, COGS, fees, spend, inventory, cash. Brand brain: targets, tax, payment terms. Intelligence: finance playbooks. Registry: which tests changed margin.
- **Outputs.** Weekly profit memo. SKU contribution table. Efficiency dashboard numbers. Scenario answers. Alerts with the arithmetic shown.
- **Playbooks.** `profit.weekly-readout`, `profit.reconcile`, `profit.sku-economics`, `profit.forecast`, `profit.cash-and-inventory`, `profit.scenario`.
- **Autonomy target.** L0 and L1. It never acts; it informs everyone else's guardrails.
- **Quality gate.** Every figure computed in code and traceable. Missing data shown as unavailable, never zero.

### Rank 5. Lifecycle agent (email, SMS, push)

Shape C with D for send tests. Score 16: Money 4, Frequency 4, AI leverage 4, Compounding 4.

- **Mission.** Own the owned channels. Right flows, right segments, right message, in the brand's voice, tested and measured in contribution, with deliverability protected.
- **Runs.** Weekly flow health, monthly calendar, on demand for campaigns.
- **Sub-agents.** Flow auditor (code over the email platform's data: coverage, gaps, timing, revenue per recipient). Segment builder (code over customer table: RFM, replenishment timing, at-risk). Copy writer (strong model, playbook). Critic. Deliverability monitor (code). Calendar planner (model). Send-time and content test designer (hands to Rank 3).
- **Inputs.** Data: customer events, flow and campaign performance, consent, complaints, product replenishment cycles. Brand brain: voice, offers, product facts, launch calendar. Intelligence: lifecycle playbooks. Inspiration: email references. Registry.
- **Outputs.** Flow map with gaps and fixes. Full email drafts with subject lines and preview text. Segment definitions. Monthly calendar. Test proposals.
- **Playbooks.** `life.audit-flows`, `life.welcome-and-nurture`, `life.abandoned-checkout`, `life.post-purchase`, `life.winback`, `life.campaign-calendar`, `life.sms-rules`, `life.deliverability`.
- **Autonomy target.** L2 for sending emails from approved templates to approved segments; L1 for new copy.

### Rank 6. Offer and pricing agent

Shape C and E. Score 15: Money 5, Frequency 2, AI leverage 4, Compounding 4.

- **Mission.** Design and improve the offer: price points, bundles, tiers, guarantees, subscriptions, promotions. Every option costed at contribution per order and per visitor before it is proposed. Respect fixed-offer rules.
- **Runs.** Quarterly review, on demand before launches and promotions.
- **Sub-agents.** Economics worker (code). Elasticity reader (code, from past price tests in the registry). Option writer (strong model, playbook). Challenger (second strong model, attacks with data and brand constraints). Judge (cheap model, checklist). Presentation auditor (code plus model: is the offer explained the same across ad, page and checkout). Promotion planner with cannibalisation model (code).
- **Inputs.** Data: price, COGS, AOV, conversion, refunds, repeat rate by SKU and bundle. Brand brain: offer rules, policies, positioning. Intelligence: offer playbooks. Registry.
- **Outputs.** 3 costed options with contribution, risk and a test design. Fixed-offer presentation fixes. Promotion plan with stop rules.
- **Playbooks.** `offer.design`, `offer.bundle-economics`, `offer.guarantee-and-risk-reversal`, `offer.audit-fixed-offer`, `offer.promotion-plan`, `offer.subscription-design`.
- **Autonomy target.** L1 forever.

### Rank 7. Landing page and PDP agent

Shape C plus A. Score 15: Money 4, Frequency 4, AI leverage 3, Compounding 4.

- **Mission.** Make every page match its traffic and its avatar. Audit, rewrite, and produce page drafts in the store's section format, with the test handed to Rank 3.
- **Runs.** On demand, and triggered by Rank 1 when a campaign's landing conversion falls.
- **Sub-agents.** Page fetcher and structure reader (code). Message-match checker (model: does the page answer the ad's promise). Audit checklist (model with playbook). Section-order planner. Copy drafter (strong model). Proof and claim checker (code). Speed and mobile check (calls Rank 17). Layout matcher (inspiration library of pages). Draft builder in theme sections.
- **Inputs.** Data: page funnel by source and device, scroll and click data where available. Brand brain: facts, proof, offer, voice, avatar. Intelligence: landing playbooks (cold traffic pages, PDP rebuild, advertorials, quiz funnels). Inspiration: page references. Registry.
- **Outputs.** Audit with ranked fixes. Wireframe as an ordered section list with copy. Theme-ready draft. Test spec.
- **Playbooks.** `page.audit`, `page.cold-traffic-landing`, `page.pdp-rebuild`, `page.advertorial`, `page.message-match`, `page.mobile-first`.
- **Autonomy target.** L1. L2 later for publishing an approved draft to a hidden preview.

### Rank 8. Voice of customer and avatar agent

Shape C (research). Score 15: Money 3, Frequency 3, AI leverage 4, Compounding 5.

- **Mission.** Turn the brand's own words from customers into a living avatar: situations, desired outcomes, objections, verbatim language, buying triggers, by segment. Feed every creating agent. Refresh as new text arrives.
- **Runs.** Monthly refresh, event-driven when a review or ticket theme spikes.
- **Sub-agents.** Text collector (code over reviews, tickets, ad comments, survey answers, chat logs). Theme clusterer (embedding plus model). Objection ranker (code: frequency times buying relevance). Verbatim picker. Avatar writer (strong model, playbook). Evidence auditor (code: every claim in the avatar links to quotes). Interview planner for gaps.
- **Inputs.** Data: all customer text with dates and order links, cohort behaviour. Brand brain: current avatar, positioning. Intelligence: research playbooks (review mining, jobs and circumstances, interview design).
- **Outputs.** Avatar record in the brand brain with quotes. Objection map. Language bank for copy. Alerts when a new theme appears. Interview plan when evidence is thin.
- **Playbooks.** `voc.mine-text`, `voc.build-avatar`, `voc.objection-map`, `voc.interview-plan`, `voc.theme-alerts`.
- **Autonomy target.** L2 for updating the brand brain's avatar section with evidence attached; human approves the summary.

### Rank 9. Retention and customer experience agent

Shape B plus C. Score 14: Money 4, Frequency 4, AI leverage 3, Compounding 3.

- **Mission.** Grow repeat contribution. Read cohorts, replenishment timing, support patterns, delivery issues and refund reasons. Fix the experience causes, then design retention plays and bounded loyalty or surprise tests.
- **Runs.** Weekly cohort and support read, monthly plays.
- **Sub-agents.** Cohort worker (code). Support theme worker (shares with Rank 8). Delivery and refund analyst (code). Play designer (model, playbook). Test designer (hands to Rank 3). Support macro drafter (model, voice).
- **Inputs.** Data: orders, cohorts, tickets, delivery events, refunds, NPS. Brand brain: policies, product lifecycle. Intelligence: post-purchase, retention and wild-bet playbooks. Registry.
- **Outputs.** Cohort readout. Top 3 experience fixes with expected effect. Retention play with test design. Support reply templates in voice.
- **Playbooks.** `retain.cohort-readout`, `retain.experience-fixes`, `retain.replenishment-timing`, `retain.loyalty-or-surprise-test`, `retain.support-macros`.
- **Autonomy target.** L1; L2 for support macros once approved.

### Rank 10. Measurement and data trust agent

Shape A. Score 14: Money 3, Frequency 4, AI leverage 5, Compounding 2 (with the warehouse assumed built, its job is to keep it trusted).

- **Mission.** Watch that the numbers stay right. Event coverage, duplicate purchases, attribution drift, consent changes, CAPI match quality, margin fields flowing, platform versus store gaps. Raise the flag before Ranks 1 and 4 act on bad data.
- **Runs.** Daily checks, weekly report.
- **Sub-agents.** Coverage checker, dedup checker, reconciliation worker, drift detector (all code). Explainer (cheap model, playbook, states checks not clicks).
- **Outputs.** Trust score per source per day. Fix list with owner. Block signal to other agents when trust drops.
- **Playbooks.** `measure.daily-trust-checks`, `measure.attribution-drift`, `measure.capi-quality`, `measure.new-source-onboarding`.
- **Autonomy target.** L2: it can put a source into "untrusted" and stop other agents using it.

### Rank 11. Organic search agent (SEO)

Shape A plus B plus C. Score 13: Money 3, Frequency 3, AI leverage 4, Compounding 3.

- **Mission.** Grow qualified organic visits and purchases. Technical health, collection and PDP content, query demand, internal links, content briefs written for buying intent.
- **Sub-agents.** Crawler and index checker (code). Query demand worker (Search Console). Content gap worker. Brief and copy writer (strong model). Link planner. Speed check via Rank 17.
- **Outputs.** Technical fix list. Prioritised page and content plan. Drafts.
- **Playbooks.** `seo.technical-audit`, `seo.collection-content`, `seo.pdp-copy`, `seo.query-demand-map`, `seo.internal-links`.
- **Autonomy target.** L1; L2 for metadata fixes.

### Rank 12. Organic content and social agent

Shape C. Score 12: Money 3, Frequency 5, AI leverage 2, Compounding 2.

- **Mission.** Plan and draft organic content that answers the avatar's questions in the brand's voice, repurpose winners across formats, and learn from engagement. Human filming and taste stay human.
- **Sub-agents.** Question miner (from Rank 8). Winner analyst (own posts). Hook and script writer. Repurposer (one asset into many). Calendar planner. Engagement reader.
- **Outputs.** Monthly calendar, hooks, scripts, captions, repurposing plan.
- **Playbooks.** `organic.question-bank`, `organic.hooks-and-scripts`, `organic.repurpose`, `organic.calendar`.
- **Autonomy target.** L1.

### Rank 13. Product research and expansion agent

Shape C plus E. Score 12: Money 5, Frequency 1, AI leverage 3, Compounding 3.

- **Mission.** For a new brand: validate an opportunity with evidence, not popularity. For a running brand: prioritise expansions and kill weak SKUs. First stage of Kevin's start-a-business path.
- **Sub-agents.** Demand reader (search and marketplace signals). Competitor offer mapper (public pages). Unit economics worker (code, with sourcing quotes as inputs). Customer evidence worker (from Rank 8). Validation designer (small paid test through Rank 1 and 2). Challenger and judge for the go or no-go.
- **Outputs.** Opportunity memo with a go, no-go or test decision. Expansion ranking. Validation test plan.
- **Playbooks.** `product.validate-opportunity`, `product.competitor-offer-map`, `product.expansion-ranking`, `product.kill-or-keep`.
- **Autonomy target.** L1.

### Rank 14. Brand positioning and voice agent

Shape C plus E. Score 12: Money 3, Frequency 2, AI leverage 2, Compounding 5.

- **Mission.** Keep the brand brain's positioning and voice sharp and consistent. Onboard a new brand through the question sequence, draft positioning options, build the voice guide from approved examples, audit consistency across ads, pages and emails.
- **Sub-agents.** Onboarding interviewer (model, structured questions). Positioning writer and challenger. Voice guide builder (from liked and disliked examples). Consistency auditor (code plus model across touchpoints). Preference learner (from the review gate).
- **Outputs.** Brand brain sections: positioning, voice guide with good and bad examples, claim register, consistency report.
- **Playbooks.** `brand.onboard`, `brand.positioning-options`, `brand.voice-guide`, `brand.consistency-audit`, `brand.claim-register`.
- **Autonomy target.** L2 for writing to the brand brain with a diff the owner approves.

### Rank 15. Store build and launch agent

Shape A plus C. Score 11: Money 3, Frequency 1, AI leverage 4, Compounding 3.

- **Mission.** Take a brand from nothing to a buyable store: domain, theme, catalog, payments, shipping, taxes, policies, tracking, test purchase, launch blockers. Then keep the store healthy.
- **Sub-agents.** Launch checklist runner (code against the platform API). Catalog builder (from product facts). Policy drafter. Test-purchase walker (browser automation in a test environment). Blocker ranker.
- **Outputs.** Launch readiness report. Configured store draft. Policies. Blocker list.
- **Playbooks.** `store.launch-checklist`, `store.catalog-setup`, `store.shipping-and-tax`, `store.policies`, `store.health-check`. Every step says "verify the current UI".
- **Autonomy target.** L2 inside a development store; L1 on a live store.

### Rank 16. Answer engine visibility agent (AEO)

Shape A. Score 10: Money 2, Frequency 3, AI leverage 4, Compounding 1.

- **Mission.** Watch how AI answer engines describe the brand and category, find mention and accuracy gaps, propose page and schema fixes, track change over time. Treated as an observation tool until it shows sales effect.
- **Playbooks.** `aeo.visibility-audit`, `aeo.accuracy-fixes`, `aeo.tracking`.
- **Autonomy target.** L0 and L1.

### Rank 17. Site speed and reliability agent

Shape A. Score 10: Money 2, Frequency 3, AI leverage 5, Compounding 2. Kevin's example agent.

- **Mission.** Keep every template fast on real devices. Lab and field scores per template, script and app inventory, image weight, third-party impact, regression after changes. Rank fixes by revenue at risk.
- **Sub-agents.** Lighthouse and CrUX runner per template. Script inventory. App audit. Image audit. Regression watcher. Fix ranker (cheap model, playbook).
- **Outputs.** Speed report with fixes ranked by pages times revenue. Regression alerts.
- **Playbooks.** `speed.audit`, `speed.third-party-triage`, `speed.image-policy`, `speed.regression-watch`.
- **Autonomy target.** L2 for image compression and lazy loading rules; L1 for removing apps.

### Rank 18. Marketplace agent (Amazon and others)

Shape B plus C. Score 9: Money 4 where used, Frequency 4, AI leverage 3, Compounding 1. Only when a brand sells there.

- **Mission.** Listing quality, advertising, inventory placement, fees, reviews, and the store-to-marketplace pricing relationship.
- **Playbooks.** `market.listing-optimise`, `market.ads`, `market.inventory-and-fees`, `market.reviews`.
- **Autonomy target.** L1.

### Rank 19. Security, fraud and bot agent

Shape A. Score 9: Money 2, Frequency 3, AI leverage 4, Compounding 1.

- **Mission.** Admin access and permissions, app scopes, payment fraud settings, checkout skimming signs, bot and scraper traffic in analytics, incident checklist. Operator-level, not developer-level.
- **Playbooks.** `sec.access-and-permissions`, `sec.payment-fraud-settings`, `sec.bot-traffic-check`, `sec.incident-checklist`.
- **Autonomy target.** L1; L2 for flagging suspicious sessions to the measurement agent.

### Rank 20. Operations and team agent

Shape C. Score 9: Money 2, Frequency 4, AI leverage 3, Compounding 1.

- **Mission.** For the agency or the in-house team: weekly task board from all agents' proposals, owner assignment, client update, process checklists, recurring error log.
- **Playbooks.** `ops.weekly-board`, `ops.client-update`, `ops.process-checklist`.
- **Autonomy target.** L2 for drafting the update; human sends.

**Excluded.** Sourcing, per Kevin (only the COGS and lead-time inputs to Ranks 4 and 13 remain). Wild bets are folded into Rank 9.

### Ranking table

| Rank | Agent | Shape | Money | Freq | AI lev. | Comp. | Score |
|---|---|---|---|---|---|---|---|
| 1 | Paid media performance and budget | B, D, E | 5 | 5 | 5 | 4 | 19 |
| 2 | Creative and ad production | C | 5 | 5 | 4 | 4 | 18 |
| 3 | Growth experimentation (CRO) | D | 4 | 4 | 4 | 5 | 17 |
| 4 | Profit and marketing efficiency | B, E | 5 | 4 | 5 | 3 | 17 |
| 5 | Lifecycle (email, SMS) | C, D | 4 | 4 | 4 | 4 | 16 |
| 6 | Offer and pricing | C, E | 5 | 2 | 4 | 4 | 15 |
| 7 | Landing page and PDP | C, A | 4 | 4 | 3 | 4 | 15 |
| 8 | Voice of customer and avatar | C | 3 | 3 | 4 | 5 | 15 |
| 9 | Retention and customer experience | B, C | 4 | 4 | 3 | 3 | 14 |
| 10 | Measurement and data trust | A | 3 | 4 | 5 | 2 | 14 |
| 11 | Organic search (SEO) | A, B, C | 3 | 3 | 4 | 3 | 13 |
| 12 | Organic content and social | C | 3 | 5 | 2 | 2 | 12 |
| 13 | Product research and expansion | C, E | 5 | 1 | 3 | 3 | 12 |
| 14 | Brand positioning and voice | C, E | 3 | 2 | 2 | 5 | 12 |
| 15 | Store build and launch | A, C | 3 | 1 | 4 | 3 | 11 |
| 16 | Answer engine visibility | A | 2 | 3 | 4 | 1 | 10 |
| 17 | Site speed and reliability | A | 2 | 3 | 5 | 2 | 10 |
| 18 | Marketplace | B, C | 4 | 4 | 3 | 1 | 9 (conditional) |
| 19 | Security, fraud and bots | A | 2 | 3 | 4 | 1 | 9 |
| 20 | Operations and team | C | 2 | 4 | 3 | 1 | 9 |

Notes on the order. Ranks 1 to 5 are the weekly operating loop of any brand that spends on ads; they move the most money most often, and with the warehouse assumed, AI can carry most of the work. Rank 6 moves a lot of money rarely, so it sits below the weekly loop. Rank 8 scores lower on money but has the highest compounding; it feeds 2, 5, 6, 7, 12 and 13. Rank 13 is the first step in the "start a business" story but happens once, so it ranks mid-table. Rank 17 is the easiest to build well, but it protects revenue more than it creates it.

## 4. Programs: chaining agents for goals

Programs are where the "operating system" feeling comes from. Each is an orchestrator script over the agents above.

| Program | Cadence | Agents in order | Output |
|---|---|---|---|
| **Weekly growth review** | Weekly | 10 (trust) then 4 (profit) then 1 (paid) then 3 (tests) then 5 (lifecycle) then 9 (retention); 20 compiles | One memo: what happened, why, what we do this week, what we test, with every proposal linked to approval |
| **Launch a new brand** | Once, 8 to 12 weeks | 13 then 8 then 6 then 14 then 15 then 7 then 2 then 1 then 5 then 10 | A buyable, tracked, advertised store with flows live and the first tests registered. Sourcing is a human step between 13 and 15. |
| **Launch a product or collection** | Per launch | 8, 6, 7, 2, 5, 1, 3 | Offer, page, creative, emails, budget and tests, all from one brief |
| **Fix a profit problem** | On demand | 4 diagnoses, then routes to 1, 6, 9 or 15 as the cause dictates; 6 with Shape E if pricing | A diagnosis and a costed plan |
| **Quarterly plan** | Quarterly | 4, 8, 3 (what we learned), 6, 13, then 1, 2, 5 set targets | Targets, budget by channel, test roadmap, content and creative themes |
| **Client report** | Monthly | 4, 1, 3, 5, 9; 20 writes | Plain-language report with numbers computed in code, no source library mentioned |

## 5. What each lower layer must expose to the agents

With the layers assumed built, this is the interface the agents need from them. It is what to check the data and brand-brain work against.

**Data layer.** Typed, versioned readers with a trust flag: `ad_metrics` (ad level, all channels, attribution window stated), `blended_daily` (spend, revenue, orders, MER, contribution after ads), `sales_by_sku`, `costs_by_sku`, `funnel_by_source_device_template`, `customers_and_cohorts`, `email_events`, `support_and_review_text`, `site_audit`, `events_and_capi_quality`, `inventory_and_cash`. Every reader returns unavailable for missing values and never silently fills zeros.

**Brand brain.** Read slices per agent, write with diffs and approval: facts and products, prices and costs, claim register with proof, offer rules, positioning, voice guide with liked and disliked examples, avatar with quotes, competitors, launch calendar, targets and guardrails, learned preferences (from the review gate), asset locations.

**Intelligence layer.** `get_playbook(agent, workflow, version)` returns 2,000 to 4,000 tokens with rule-to-card links. `lookup(question, filters)` returns up to 4 cards. Playbooks carry a "verify current UI" flag where platforms change.

**Inspiration layer.** `match(asset_or_brief, filters)` over own and competitor assets with structured fields and performance; competitor assets marked signal only and never returned for text or product copying. `describe(asset)` for new assets.

**Experiment registry.** `propose`, `approve`, `start`, `read`, `decide`, `search_similar`. Every agent calls `search_similar` before proposing.

**Approval gate.** `submit(action, level, evidence)`; returns approved, edited or rejected, and records the human's edit so the brand brain and playbooks can learn.

## 6. Playbook backlog by rank

About 95 playbooks across the 20 agents, listed under each agent above. The first 30, in the order the weekly loop needs them: the 8 paid playbooks, the 7 creative playbooks, the 6 experimentation playbooks, the 6 profit playbooks, and the first 3 lifecycle playbooks. Each is distilled from its folder, edited once by Kevin, linked to cards, versioned, and under 4,000 tokens.

## 7. Build order, given the full stack

Build the shapes, not the agents, first. Then fill agents in rank order.

1. Orchestrator, approval gate, registry client, audit log, model router. Shape B and Shape C as reusable runners.
2. Rank 1 and Rank 2 on Shape B and C. Rank 4 on Shape B. These three prove the weekly loop.
3. Shape D and Shape A. Rank 3 and Rank 10.
4. Rank 5, 7, 8, 6 (Shape E arrives with Rank 6).
5. The Weekly growth review program.
6. Ranks 9 to 14 in order, then the Launch program.
7. Ranks 15 to 20 as clients need them.

Promotion up the autonomy ladder happens per action type from the registry record, never by a decision to "turn on autonomy".

## 8. Questions for Kevin

1. Which channels does the paid media agent own on day one: Meta and Google only, or also TikTok, Pinterest and affiliates? It changes the channel workers.
2. For Shape E, who is the final judge on pricing and offer changes: always the owner, or can the agency approve inside a band?
3. Video creative: does the creative agent produce finished videos, or scripts and briefs for humans and tools? The full pipeline is a large build.
4. Should the Launch program include sourcing as a human checkpoint with an API later, or leave it fully outside?
5. Client-facing: do clients see all 20 agents, or a smaller set with the rest behind the agency?
