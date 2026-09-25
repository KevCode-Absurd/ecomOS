# Execution layer: the agent stack, designed for the full system

Date: 24 Sep 2026. Companion to `INTELLIGENCE_REVIEW.md`. Planning only; nothing built. This version replaces the earlier draft that ranked by what data exists today.

**Assumption, as Kevin set it:** the data warehouse is built and trusted (Meta, Google, GA4, Klaviyo, Shopify, support tickets, reviews, all reconciled daily, gross margin and marketing efficiency computed in code and passed through CAPI). The brand brain is built (facts, claims, offers, voice, competitors, past winners, assets, preferences). The inspiration library is built (own and competitor statics, videos, pages, emails, with structured descriptions and performance). The intelligence layer holds a distilled playbook per workflow plus cards for lookup. The question is only: what are the best possible agents on top, and in what order do they matter.

## 1. How the layer is organised

Three levels. Kevin's 24 folders each become one agent at the middle level; the full map is in section 3.

```
Level 3  PROGRAMS         long-running goals that chain many agents
         Weekly growth review, Launch program (new brand), Quarterly plan, Client report
                |
Level 2  DOMAIN AGENTS    one per folder (24 agents)
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

The 24 agents follow in rank order. The folder-to-agent map at the end of this section is the summary table.

### Rank 1. Paid media performance and budget agent, social channels (folder 10-MCR)

Shape B, then D, with E for large reallocations. Score 19: Money 5, Frequency 5, AI leverage 5, Compounding 4.

- **Mission.** Run the paid social engine day to day across Meta, TikTok and other social channels; Google has its own agent at rank 5 and shares the budget allocator: find what is wasting money, what is winning, what is fatiguing, where to move budget, and what to test next. Report in contribution terms, not ROAS alone.
- **Runs.** Daily pacing check, weekly deep read, on demand for "what happened".
- **Sub-agents.** Channel readers (Meta, TikTok, Pinterest, Snap) as workers. Fatigue and frequency worker. Audience overlap worker. Creative ranker (code plus vision model over own statics and videos). Incrementality reader (holdout and geo tests from the registry). Budget allocator (code: marginal contribution per channel and campaign). Hypothesis writer (model). Test ranker (model, reads registry).
- **Inputs.** Data: ad metrics at ad level with attribution, blended MER and contribution by day, incrementality results, funnel by source. Brand brain: margin targets, cash limits, seasonality, launch calendar, excluded audiences. Intelligence: diagnostics playbooks per channel, scaling gates, fatigue rules. Inspiration: own winners for the creative ranker. Registry: past tests and decisions.
- **Outputs.** Daily exception list. Weekly diagnosis memo with ranked causes. Budget proposal by campaign with expected contribution. Kill, keep, scale list for ads. Top 5 tests. Creative briefs handed to Rank 2. Landing issues handed to Rank 8.
- **Sources across folders.** 24-DEP (213 deployment cards, moved from 11 on 24 Sep), creative-testing cards from 10-MCR, measurement cards from 06-MEA, contribution rules from 20-FIN.
- **Playbooks.** `paid.diagnose-drop`, `paid.pace-budget`, `paid.scale-or-cut`, `paid.rank-tests`, `paid.incrementality-plan`.
- **Autonomy target.** L2 for pausing above a CPA ceiling and negative keywords; L3 for pacing inside a cap; L1 forever for new campaigns and reallocations above a threshold.
- **Quality gate.** Every number in the memo traces to a query. No recommendation without the contribution effect stated. Guardrail: never propose more than a set percent shift in one day.

### Rank 2. Ad copy and creative production agent (folder 11-ADC)

Shape C. Score 18: Money 5, Frequency 5, AI leverage 4, Compounding 4.

- **Mission.** Keep the account fed with concepts, statics, video scripts and copy that fit the brand, the avatar and the offer, and that learn from what won. Kevin's "match our winners against good formats" idea lives here.
- **Runs.** Weekly batch from Rank 1's briefs, on demand for launches.
- **Sub-agents.** Winner analyst (vision model describes own top and bottom ads, code finds what the winners share). Inspiration matcher (embedding and field match over the library, own and competitor, competitor as layout and mood only). Concept writer (strong model, playbook). Copy writer (strong model, ad-copy playbook from v1.2). Script writer for video and UGC briefs. Static builder (image model with the real product locked as a layer). Claim and offer checker (code). Critic (cheap model, checklist: avatar fit, credible before and after, one clear benefit, no invented claims, voice). Variant planner (one variable per variant).
- **Inputs.** Data: ad-level results, hook and hold rates for video, comment text. Brand brain: facts, claims and proof, offer rules, voice examples, liked and disliked outputs, product photos. Intelligence: copy, concept, hook, UGC and static-format playbooks. Inspiration: everything, with performance. Registry: which angles and formats were already tested.
- **Outputs.** Concept board: 5 concepts, each with the winner pattern it draws on, 3 copy variants, format, reference match, static mockups, video script or UGC brief, and a claim audit. Test plan handed to Rank 3 or Rank 1.
- **Sources across folders.** 11-ADC (402 copywriting cards after the split), 10-MCR creative concept and format cards, avatar cards from 02-AVT, voice from 04-BRD.
- **Playbooks.** `creative.analyse-winners`, `creative.concept-board`, `creative.static-copy`, `creative.video-script`, `creative.ugc-brief`, `creative.variant-plan`, `creative.hook-library`.
- **Autonomy target.** L1 always for anything public. L2 for internal mockup generation.
- **Quality gate.** Blind pairwise review by Kevin or the client for a rolling sample. Ship, edit or rewrite label feeds learned preferences back to the brand brain.

### Rank 3. Growth experimentation agent (CRO and beyond) (folder 09-CRO)

Shape D. Score 17: Money 4, Frequency 4, AI leverage 4, Compounding 5.

- **Mission.** Own the test programme across site, offer, creative and lifecycle. Find the biggest drop, propose tests that are worth running, size them properly, watch them, call them honestly and write the decision back so nothing is tested twice by accident.
- **Runs.** Weekly review, event-driven when a test reaches its sample size.
- **Sub-agents.** Funnel reader (code, by device, source, page template). Opportunity sizer (code: visitors times drop times margin). Test designer (strong model, playbook). Sample size and duration worker (code). Guardrail monitor (code: revenue per visitor, refunds, speed). Result reader (code, with uncertainty). Decision writer (model). Registry keeper.
- **Inputs.** Data: funnel, page performance, experiment platform results, margins. Brand brain: offer rules, constraints, traffic level. Intelligence: CRO playbooks (test selection by traffic, pre-registration, holdouts, reading results). Registry.
- **Outputs.** Ranked test backlog with expected value. Test specs ready for a developer or the landing agent. Readouts with a decision: ship, kill, rerun. A living map of what is known about the funnel.
- **Playbooks.** `exp.find-biggest-drop`, `exp.design-test`, `exp.size-and-guardrails`, `exp.read-result`, `exp.holdout-plan`, `exp.low-traffic-alternatives`.
- **Autonomy target.** L2 for stopping a test that breaches a guardrail. L1 for launching.
- **Quality gate.** No test without a pre-registered metric and stop rule. No "winner" without the uncertainty stated.

### Rank 4. Profit and marketing efficiency agent (folder 20-FIN)

Shape B, with E for pricing and cash calls. Score 17: Money 5, Frequency 4, AI leverage 5, Compounding 3.

- **Mission.** Be the CFO view. Contribution by SKU, channel and cohort. MER and contribution after ads by week. Cash tied in stock. Forecasts. Reconcile platform claims to the P&L. Tell the owner where profit is leaking and what it would take to fix.
- **Runs.** Weekly readout, monthly close, on demand.
- **Sub-agents.** Contribution calculator (code). Reconciler (code: platform-reported purchases versus store orders). Cohort LTV worker (code). Forecast worker (code, simple models with error bands). Cash and inventory worker (code). Scenario worker (code: what if price, CAC or return rate changes). Narrator (cheap model, playbook). Anomaly flagger.
- **Inputs.** Data: orders, refunds, COGS, fees, spend, inventory, cash. Brand brain: targets, tax, payment terms. Intelligence: finance playbooks. Registry: which tests changed margin.
- **Outputs.** Weekly profit memo. SKU contribution table. Efficiency dashboard numbers. Scenario answers. Alerts with the arithmetic shown.
- **Playbooks.** `profit.weekly-readout`, `profit.reconcile`, `profit.sku-economics`, `profit.forecast`, `profit.cash-and-inventory`, `profit.scenario`.
- **Autonomy target.** L0 and L1. It never acts; it informs everyone else's guardrails.
- **Quality gate.** Every figure computed in code and traceable. Missing data shown as unavailable, never zero.

### Rank 5. Google Ads performance agent (folder 12-GAD)

Shape and scores are in the map below.

Shape B, then D.
- Mission: run Search, Shopping, PMax and YouTube for profit. Search-term waste, feed health, brand and competitor exclusions, bidding strategy by stage, scaling gates, PMax versus Shopping choice, attribution alignment with the warehouse.
- Sub-agents: search-term worker, feed and Merchant Center worker, structure and bidding worker, brand-exclusion worker, PMax asset reader, budget allocator (shared with rank 1), hypothesis writer, test ranker.
- Inputs: Google Ads and Merchant Center data at keyword, product and asset-group level; blended contribution from rank 4; brand brain margins, catalog and exclusions; Google playbooks; registry.
- Outputs: weekly account diagnosis, negative and exclusion lists, structure and bidding proposals, feed fixes, budget proposal, tests.
- Sources across folders: 12-GAD, now including the 4 Google Ads documents moved from 11 on 24 Sep (141 cards), plus conversion setup cards from 06-MEA.
- Playbooks: `google.diagnose-account`, `google.search-term-hygiene`, `google.feed-health`, `google.shopping-vs-pmax`, `google.bidding-by-stage`, `google.scaling-gates`, `google.brand-and-competitor-exclusions`.
- Autonomy target: L2 for negatives and exclusions; L3 for pacing inside a cap; L1 for structure changes.

### Rank 6. Lifecycle agent (email, SMS, push) (folder 14-EML)

Shape C with D for send tests. Score 16: Money 4, Frequency 4, AI leverage 4, Compounding 4.

- **Mission.** Own the owned channels. Right flows, right segments, right message, in the brand's voice, tested and measured in contribution, with deliverability protected.
- **Runs.** Weekly flow health, monthly calendar, on demand for campaigns.
- **Sub-agents.** Flow auditor (code over the email platform's data: coverage, gaps, timing, revenue per recipient). Segment builder (code over customer table: RFM, replenishment timing, at-risk). Copy writer (strong model, playbook). Critic. Deliverability monitor (code). Calendar planner (model). Send-time and content test designer (hands to Rank 3).
- **Inputs.** Data: customer events, flow and campaign performance, consent, complaints, product replenishment cycles. Brand brain: voice, offers, product facts, launch calendar. Intelligence: lifecycle playbooks. Inspiration: email references. Registry.
- **Outputs.** Flow map with gaps and fixes. Full email drafts with subject lines and preview text. Segment definitions. Monthly calendar. Test proposals.
- **Playbooks.** `life.audit-flows`, `life.welcome-and-nurture`, `life.abandoned-checkout`, `life.post-purchase`, `life.winback`, `life.campaign-calendar`, `life.sms-rules`, `life.deliverability`.
- **Autonomy target.** L2 for sending emails from approved templates to approved segments; L1 for new copy.

### Rank 7. Offer and pricing agent (folder 03-OFF)

Shape C and E. Score 15: Money 5, Frequency 2, AI leverage 4, Compounding 4.

- **Mission.** Design and improve the offer: price points, bundles, tiers, guarantees, subscriptions, promotions. Every option costed at contribution per order and per visitor before it is proposed. Respect fixed-offer rules.
- **Runs.** Quarterly review, on demand before launches and promotions.
- **Sub-agents.** Economics worker (code). Elasticity reader (code, from past price tests in the registry). Option writer (strong model, playbook). Challenger (second strong model, attacks with data and brand constraints). Judge (cheap model, checklist). Presentation auditor (code plus model: is the offer explained the same across ad, page and checkout). Promotion planner with cannibalisation model (code).
- **Inputs.** Data: price, COGS, AOV, conversion, refunds, repeat rate by SKU and bundle. Brand brain: offer rules, policies, positioning. Intelligence: offer playbooks. Registry.
- **Outputs.** 3 costed options with contribution, risk and a test design. Fixed-offer presentation fixes. Promotion plan with stop rules.
- **Playbooks.** `offer.design`, `offer.bundle-economics`, `offer.guarantee-and-risk-reversal`, `offer.audit-fixed-offer`, `offer.promotion-plan`, `offer.subscription-design`.
- **Autonomy target.** L1 forever.

### Rank 8. Landing page and PDP agent (folder 07-LPG)

Shape C plus A. Score 15: Money 4, Frequency 4, AI leverage 3, Compounding 4.

- **Mission.** Make every page match its traffic and its avatar. Audit, rewrite, and produce page drafts in the store's section format, with the test handed to Rank 3.
- **Runs.** On demand, and triggered by Rank 1 when a campaign's landing conversion falls.
- **Sub-agents.** Page fetcher and structure reader (code). Message-match checker (model: does the page answer the ad's promise). Audit checklist (model with playbook). Section-order planner. Copy drafter (strong model). Proof and claim checker (code). Speed and mobile check (calls Rank 21). Layout matcher (inspiration library of pages). Draft builder in theme sections.
- **Inputs.** Data: page funnel by source and device, scroll and click data where available. Brand brain: facts, proof, offer, voice, avatar. Intelligence: landing playbooks (cold traffic pages, PDP rebuild, advertorials, quiz funnels). Inspiration: page references. Registry.
- **Outputs.** Audit with ranked fixes. Wireframe as an ordered section list with copy. Theme-ready draft. Test spec.
- **Playbooks.** `page.audit`, `page.cold-traffic-landing`, `page.pdp-rebuild`, `page.advertorial`, `page.message-match`, `page.mobile-first`.
- **Autonomy target.** L1. L2 later for publishing an approved draft to a hidden preview.

### Rank 9. Voice of customer and avatar agent (folder 02-AVT)

Shape C (research). Score 15: Money 3, Frequency 3, AI leverage 4, Compounding 5.

- **Mission.** Turn the brand's own words from customers into a living avatar: situations, desired outcomes, objections, verbatim language, buying triggers, by segment. Feed every creating agent. Refresh as new text arrives.
- **Runs.** Monthly refresh, event-driven when a review or ticket theme spikes.
- **Sub-agents.** Text collector (code over reviews, tickets, ad comments, survey answers, chat logs). Theme clusterer (embedding plus model). Objection ranker (code: frequency times buying relevance). Verbatim picker. Avatar writer (strong model, playbook). Evidence auditor (code: every claim in the avatar links to quotes). Interview planner for gaps.
- **Inputs.** Data: all customer text with dates and order links, cohort behaviour. Brand brain: current avatar, positioning. Intelligence: research playbooks (review mining, jobs and circumstances, interview design).
- **Outputs.** Avatar record in the brand brain with quotes. Objection map. Language bank for copy. Alerts when a new theme appears. Interview plan when evidence is thin.
- **Playbooks.** `voc.mine-text`, `voc.build-avatar`, `voc.objection-map`, `voc.interview-plan`, `voc.theme-alerts`.
- **Autonomy target.** L2 for updating the brand brain's avatar section with evidence attached; human approves the summary.

### Rank 10. Growth strategist agent (folder 99-multi)

Shape and scores are in the map below.

Shape B with E.
- Mission: read the whole brand like an outside operator would. Find the current bottleneck (traffic, conversion, AOV, retention, margin, cash), tear down a competitor's creative, offers and landers, plan seasonal pushes (Black Friday, launches), and set the quarter's priorities for the other agents.
- Sub-agents: bottleneck finder (code over the warehouse, using the six-bottlenecks frame), competitor teardown worker (public pages and the inspiration library), seasonal planner, priority writer, challenger and judge.
- Inputs: everything rank 4 produces, funnel, cohorts, competitor assets, brand brain targets, the cross-domain playbooks distilled from 99-multi, registry.
- Outputs: quarterly priority memo, bottleneck diagnosis, competitor teardown, seasonal plan with budget, creative and offer themes handed to ranks 1, 2, 5, 6, 7.
- Playbooks: `strategy.find-bottleneck`, `strategy.competitor-teardown`, `strategy.seasonal-plan`, `strategy.quarterly-priorities`, `strategy.myths-and-traps`.
- Autonomy target: L0 and L1.

### Rank 11. Retention and customer experience agent (folder 17-CXP)

Shape B plus C. Score 14: Money 4, Frequency 4, AI leverage 3, Compounding 3.

- **Mission.** Grow repeat contribution. Read cohorts, replenishment timing, support patterns, delivery issues and refund reasons. Fix the experience causes, then design retention plays and bounded loyalty or surprise tests.
- **Runs.** Weekly cohort and support read, monthly plays.
- **Sub-agents.** Cohort worker (code). Support theme worker (shares with Rank 9). Delivery and refund analyst (code). Play designer (model, playbook). Test designer (hands to Rank 3). Support macro drafter (model, voice).
- **Inputs.** Data: orders, cohorts, tickets, delivery events, refunds, NPS. Brand brain: policies, product lifecycle. Intelligence: post-purchase, retention and wild-bet playbooks. Registry.
- **Outputs.** Cohort readout. Top 3 experience fixes with expected effect. Retention play with test design. Support reply templates in voice.
- **Playbooks.** `retain.cohort-readout`, `retain.experience-fixes`, `retain.replenishment-timing`, `retain.loyalty-or-surprise-test`, `retain.support-macros`.
- **Autonomy target.** L1; L2 for support macros once approved.

### Rank 12. Measurement and data trust agent (folder 06-MEA)

Shape A. Score 14: Money 3, Frequency 4, AI leverage 5, Compounding 2 (with the warehouse assumed built, its job is to keep it trusted).

- **Mission.** Watch that the numbers stay right. Event coverage, duplicate purchases, attribution drift, consent changes, CAPI match quality, margin fields flowing, platform versus store gaps. Raise the flag before Ranks 1 and 4 act on bad data.
- **Runs.** Daily checks, weekly report.
- **Sub-agents.** Coverage checker, dedup checker, reconciliation worker, drift detector (all code). Explainer (cheap model, playbook, states checks not clicks).
- **Outputs.** Trust score per source per day. Fix list with owner. Block signal to other agents when trust drops.
- **Playbooks.** `measure.daily-trust-checks`, `measure.attribution-drift`, `measure.capi-quality`, `measure.new-source-onboarding`.
- **Autonomy target.** L2: it can put a source into "untrusted" and stop other agents using it.

### Rank 13. Organic search agent (SEO) (folder 15-SEO)

Shape A plus B plus C. Score 13: Money 3, Frequency 3, AI leverage 4, Compounding 3.

- **Mission.** Grow qualified organic visits and purchases. Technical health, collection and PDP content, query demand, internal links, content briefs written for buying intent.
- **Sub-agents.** Crawler and index checker (code). Query demand worker (Search Console). Content gap worker. Brief and copy writer (strong model). Link planner. Speed check via Rank 21.
- **Outputs.** Technical fix list. Prioritised page and content plan. Drafts.
- **Playbooks.** `seo.technical-audit`, `seo.collection-content`, `seo.pdp-copy`, `seo.query-demand-map`, `seo.internal-links`.
- **Autonomy target.** L1; L2 for metadata fixes.

### Rank 14. Wild bets agent (folder 19-WLD)

Shape and scores are in the map below.

Shape C and D.
- Mission: propose and test unconventional plays that the main agents would not: outcome guarantees, surprise gifts, a no-ads week, direct mail to top cohorts, handwritten notes, community offers. Always bounded: a budget, a cohort, a metric, a stop rule.
- Sub-agents: idea generator (strong model over the wild-bets playbook and the brand's context), fit filter (brand brain rules), economics worker, test designer (through rank 3), result reader.
- Inputs: cohorts and LTV from rank 11, margins from rank 4, brand brain voice and policies, registry.
- Outputs: 3 bounded bets per quarter with costed tests. Registry entries.
- Playbooks: `wild.bet-ideas`, `wild.bound-and-measure`, `wild.retention-bets`, `wild.offer-bets`.
- Autonomy target: L1 always.

### Rank 15. Organic content and social agent (folder 13-ORG)

Shape C. Score 12: Money 3, Frequency 5, AI leverage 2, Compounding 2.

- **Mission.** Plan and draft organic content that answers the avatar's questions in the brand's voice, repurpose winners across formats, and learn from engagement. Human filming and taste stay human.
- **Sub-agents.** Question miner (from Rank 9). Winner analyst (own posts). Hook and script writer. Repurposer (one asset into many). Calendar planner. Engagement reader.
- **Outputs.** Monthly calendar, hooks, scripts, captions, repurposing plan.
- **Playbooks.** `organic.question-bank`, `organic.hooks-and-scripts`, `organic.repurpose`, `organic.calendar`.
- **Autonomy target.** L1.

### Rank 16. Product research and expansion agent (folder 01-PRD)

Shape C plus E. Score 12: Money 5, Frequency 1, AI leverage 3, Compounding 3.

- **Mission.** For a new brand: validate an opportunity with evidence, not popularity. For a running brand: prioritise expansions and kill weak SKUs. First stage of Kevin's start-a-business path.
- **Sub-agents.** Demand reader (search and marketplace signals). Competitor offer mapper (public pages). Unit economics worker (code, with sourcing quotes as inputs). Customer evidence worker (from Rank 9). Validation designer (small paid test through Rank 1 and 2). Challenger and judge for the go or no-go.
- **Outputs.** Opportunity memo with a go, no-go or test decision. Expansion ranking. Validation test plan.
- **Playbooks.** `product.validate-opportunity`, `product.competitor-offer-map`, `product.expansion-ranking`, `product.kill-or-keep`.
- **Autonomy target.** L1.

### Rank 17. Brand positioning and voice agent (folder 04-BRD)

Shape C plus E. Score 12: Money 3, Frequency 2, AI leverage 2, Compounding 5.

- **Mission.** Keep the brand brain's positioning and voice sharp and consistent. Onboard a new brand through the question sequence, draft positioning options, build the voice guide from approved examples, audit consistency across ads, pages and emails.
- **Sub-agents.** Onboarding interviewer (model, structured questions). Positioning writer and challenger. Voice guide builder (from liked and disliked examples). Consistency auditor (code plus model across touchpoints). Preference learner (from the review gate).
- **Outputs.** Brand brain sections: positioning, voice guide with good and bad examples, claim register, consistency report.
- **Playbooks.** `brand.onboard`, `brand.positioning-options`, `brand.voice-guide`, `brand.consistency-audit`, `brand.claim-register`.
- **Autonomy target.** L2 for writing to the brand brain with a diff the owner approves.

### Rank 18. Store build and launch agent (folder 05-SET)

Shape A plus C. Score 11: Money 3, Frequency 1, AI leverage 4, Compounding 3.

- **Mission.** Take a brand from nothing to a buyable store: domain, theme, catalog, payments, shipping, taxes, policies, tracking, test purchase, launch blockers. Then keep the store healthy.
- **Sub-agents.** Launch checklist runner (code against the platform API). Catalog builder (from product facts). Policy drafter. Test-purchase walker (browser automation in a test environment). Blocker ranker.
- **Outputs.** Launch readiness report. Configured store draft. Policies. Blocker list.
- **Playbooks.** `store.launch-checklist`, `store.catalog-setup`, `store.shipping-and-tax`, `store.policies`, `store.health-check`. Every step says "verify the current UI".
- **Autonomy target.** L2 inside a development store; L1 on a live store.

### Rank 19. Sourcing and supply agent (folder 18-COG)

Shape and scores are in the map below.

Shape C and A.
- Mission: turn a product decision into a buyable spec and a costed plan. Write the specification and bill of materials, compare supplier quotes, plan the 3 sample stages, compute landed cost with duties, freight and defects, plan reorder timing against cash, and hand the purchase order to a human or a partner API.
- Sub-agents: spec and BOM writer, quote comparer (code), sample-stage planner, landed-cost calculator (code), reorder and cash planner (with rank 4), supplier risk checklist.
- Inputs: product decision from rank 16, sales velocity and cash from rank 4, brand brain product facts, sourcing playbooks, supplier quotes as uploads.
- Outputs: spec sheet, quote comparison, sample plan, landed cost per unit, reorder calendar, purchase order draft.
- Playbooks: `source.spec-and-bom`, `source.compare-quotes`, `source.sample-stages`, `source.landed-cost`, `source.reorder-and-cash`, `source.supplier-risk`.
- Autonomy target: L1. The purchase itself stays human or partner.

### Rank 20. Answer engine visibility agent (AEO) (folder 16-AEO)

Shape A. Score 10: Money 2, Frequency 3, AI leverage 4, Compounding 1.

- **Mission.** Watch how AI answer engines describe the brand and category, find mention and accuracy gaps, propose page and schema fixes, track change over time. Treated as an observation tool until it shows sales effect.
- **Playbooks.** `aeo.visibility-audit`, `aeo.accuracy-fixes`, `aeo.tracking`.
- **Autonomy target.** L0 and L1.

### Rank 21. Site speed and reliability agent (folder 08-SPD)

Shape A. Score 10: Money 2, Frequency 3, AI leverage 5, Compounding 2. Kevin's example agent.

- **Mission.** Keep every template fast on real devices. Lab and field scores per template, script and app inventory, image weight, third-party impact, regression after changes. Rank fixes by revenue at risk.
- **Sub-agents.** Lighthouse and CrUX runner per template. Script inventory. App audit. Image audit. Regression watcher. Fix ranker (cheap model, playbook).
- **Outputs.** Speed report with fixes ranked by pages times revenue. Regression alerts.
- **Playbooks.** `speed.audit`, `speed.third-party-triage`, `speed.image-policy`, `speed.regression-watch`.
- **Autonomy target.** L2 for image compression and lazy loading rules; L1 for removing apps.

### Rank 22. Marketplace agent (Amazon and others) (folder 22-AMZ)

Shape B plus C. Score 9: Money 4 where used, Frequency 4, AI leverage 3, Compounding 1. Only when a brand sells there.

- **Mission.** Listing quality, advertising, inventory placement, fees, reviews, and the store-to-marketplace pricing relationship.
- **Playbooks.** `market.listing-optimise`, `market.ads`, `market.inventory-and-fees`, `market.reviews`.
- **Autonomy target.** L1.

### Rank 23. Security, fraud and bot agent (folder 23-SEC)

Shape A. Score 9: Money 2, Frequency 3, AI leverage 4, Compounding 1.

- **Mission.** Admin access and permissions, app scopes, payment fraud settings, checkout skimming signs, bot and scraper traffic in analytics, incident checklist. Operator-level, not developer-level.
- **Playbooks.** `sec.access-and-permissions`, `sec.payment-fraud-settings`, `sec.bot-traffic-check`, `sec.incident-checklist`.
- **Autonomy target.** L1; L2 for flagging suspicious sessions to the measurement agent.

### Rank 24. Operations and team agent (folder 21-OPS)

Shape C. Score 9: Money 2, Frequency 4, AI leverage 3, Compounding 1.

- **Mission.** For the agency or the in-house team: weekly task board from all agents' proposals, owner assignment, client update, process checklists, recurring error log.
- **Playbooks.** `ops.weekly-board`, `ops.client-update`, `ops.process-checklist`.
- **Autonomy target.** L2 for drafting the update; human sends.

**Nothing excluded.** Every folder has an agent in the map below. Sourcing keeps the buying step human or partner-run, per Kevin, but the spec, quote, sample and landed-cost work is an agent.

### Folder-to-agent map: all 24 folders, ranked

Every source folder gets its own agent. Nothing is merged away. This table summarises the cards above. On 24 Sep 2026 folder 11 was split: 10 Meta, TikTok and account-audit documents (213 cards) moved to a new Drive folder `24-DEP-ad-deployment`, and 4 Google Ads documents (141 cards) moved to `12-GAD`. Folder 11 now holds copywriting only (9 documents, 402 cards). The repo records this in `data/library-v3/folder-overrides.json` without changing cards.json; card ids do not depend on folder. Where two folders share a shape and data, the agents are siblings that hand work to each other, not one agent. Scores use the method in section 2.

| Rank | Folder | Agent | Shape | Money | Freq | AI lev. | Comp. | Score |
|---|---|---|---|---|---|---|---|---|
| 1 | 24-DEP ad deployment (new, split from 11 on 24 Sep) | Paid media performance and budget (Meta, TikTok, other social) | B, D, E | 5 | 5 | 5 | 4 | 19 |
| 2 | 11-ADC ad copy (copy only after the split) and 10-MCR paid social creative | Ad copy and creative production, 2 sibling agents: copy (11) and creative concepts and formats (10) | C | 5 | 5 | 4 | 4 | 18 |
| 3 | 09-CRO testing | Growth experimentation (CRO) | D | 4 | 4 | 4 | 5 | 17 |
| 4 | 20-FIN finance and accounting | Profit and marketing efficiency | B, E | 5 | 4 | 5 | 3 | 17 |
| 5 | 12-GAD google ads | Google Ads performance (Search, Shopping, PMax, YouTube) | B, D | 5 | 5 | 4 | 3 | 17 |
| 6 | 14-EML email lifecycle | Lifecycle (email, SMS, push) | C, D | 4 | 4 | 4 | 4 | 16 |
| 7 | 03-OFF offers | Offer and pricing | C, E | 5 | 2 | 4 | 4 | 15 |
| 8 | 07-LPG landing pages | Landing page and PDP | C, A | 4 | 4 | 3 | 4 | 15 |
| 9 | 02-AVT avatars | Voice of customer and avatar | C | 3 | 3 | 4 | 5 | 15 |
| 10 | 99-multi cross-domain | Growth strategist (teardowns, bottleneck finder, seasonal plans) | B, E | 4 | 2 | 3 | 5 | 14 |
| 11 | 17-CXP post-purchase | Retention and customer experience | B, C | 4 | 4 | 3 | 3 | 14 |
| 12 | 06-MEA measurement | Measurement and data trust | A | 3 | 4 | 5 | 2 | 14 |
| 13 | 15-SEO search | Organic search (SEO) | A, B, C | 3 | 3 | 4 | 3 | 13 |
| 14 | 19-WLD wild bets | Unconventional offers and retention bets | C, D | 3 | 2 | 3 | 4 | 12 |
| 15 | 13-ORG organic and content | Organic content and social | C | 3 | 5 | 2 | 2 | 12 |
| 16 | 01-PRD product research | Product research and expansion | C, E | 5 | 1 | 3 | 3 | 12 |
| 17 | 04-BRD brand | Brand positioning and voice | C, E | 3 | 2 | 2 | 5 | 12 |
| 18 | 05-SET store setup | Store build and launch | A, C | 3 | 1 | 4 | 3 | 11 |
| 19 | 18-COG sourcing | Sourcing and supply (specs, quotes, samples, landed cost) | C, A | 4 | 2 | 2 | 3 | 11 |
| 20 | 16-AEO answer engines | Answer engine visibility | A | 2 | 3 | 4 | 1 | 10 |
| 21 | 08-SPD speed | Site speed and reliability | A | 2 | 3 | 5 | 2 | 10 (moved up from 9 by hand: cheapest to build well) |
| 22 | 22-AMZ amazon marketplace | Marketplace | B, C | 4 | 4 | 3 | 1 | 9 (conditional on selling there) |
| 23 | 23-SEC bot and agent security | Security, fraud and bots | A | 2 | 3 | 4 | 1 | 9 |
| 24 | 21-OPS team and management | Operations and team | C | 2 | 4 | 3 | 1 | 9 |

Notes on the order. Ranks 1 to 6 are the weekly operating loop of any brand that spends on ads. Google Ads is its own agent (rank 5) because its data, levers and playbooks differ from social; it shares the budget allocator worker with rank 1. Ad copy (rank 2) is split from paid social creative (rank 1): rank 1 reads results and briefs, rank 2 makes the ads. Offers move a lot of money but rarely. Voice of customer scores low on money but feeds ranks 2, 6, 7, 8, 15 and 16. The growth strategist from 99-multi is the cross-domain reader: teardowns, the six bottlenecks, Black Friday plans; it points the other agents at the right problem. Product research starts the "start a business" story but happens once, so it sits mid-table. Sourcing is an agent even though Kevin plans to outsource the buying: it writes the spec, compares quotes, plans samples and computes landed cost, and hands the purchase to a human or a partner API. Site speed is the easiest to build well but protects revenue more than it creates it.

## 4. Programs: chaining agents for goals

Programs are where the "operating system" feeling comes from. Each is an orchestrator script over the agents above.

| Program | Cadence | Agents in order | Output |
|---|---|---|---|
| **Weekly growth review** | Weekly | 12 (trust) then 4 (profit) then 1 and 5 (paid) then 3 (tests) then 6 (lifecycle) then 11 (retention); 24 compiles | One memo: what happened, why, what we do this week, what we test, with every proposal linked to approval |
| **Launch a new brand** | Once, 8 to 12 weeks | 16 then 9 then 7 then 17 then 19 then 18 then 8 then 2 then 1 and 5 then 6 then 12 | A buyable, tracked, advertised store with flows live and the first tests registered. The purchase order in step 19 is a human checkpoint. |
| **Launch a product or collection** | Per launch | 9, 7, 19, 8, 2, 6, 1, 5, 3 | Offer, stock, page, creative, emails, budget and tests, all from one brief |
| **Fix a profit problem** | On demand | 4 diagnoses, 10 finds the bottleneck, then routes to 1, 5, 7, 11 or 18 as the cause dictates; 7 with Shape E if pricing | A diagnosis and a costed plan |
| **Quarterly plan** | Quarterly | 4, 9, 3 (what we learned), 10 sets priorities, 7, 16, 14, then 1, 2, 5, 6 set targets | Targets, budget by channel, test roadmap, content and creative themes, 3 wild bets |
| **Client report** | Monthly | 4, 1, 5, 3, 6, 11; 24 writes | Plain-language report with numbers computed in code, no source library mentioned |

## 5. What each lower layer must expose to the agents

With the layers assumed built, this is the interface the agents need from them. It is what to check the data and brand-brain work against.

**Data layer.** Typed, versioned readers with a trust flag: `ad_metrics` (ad level, all channels, attribution window stated), `blended_daily` (spend, revenue, orders, MER, contribution after ads), `sales_by_sku`, `costs_by_sku`, `funnel_by_source_device_template`, `customers_and_cohorts`, `email_events`, `support_and_review_text`, `site_audit`, `events_and_capi_quality`, `inventory_and_cash`. Every reader returns unavailable for missing values and never silently fills zeros.

**Brand brain.** Read slices per agent, write with diffs and approval: facts and products, prices and costs, claim register with proof, offer rules, positioning, voice guide with liked and disliked examples, avatar with quotes, competitors, launch calendar, targets and guardrails, learned preferences (from the review gate), asset locations.

**Intelligence layer.** `get_playbook(agent, workflow, version)` returns 2,000 to 4,000 tokens with rule-to-card links. `lookup(question, filters)` returns up to 4 cards. Playbooks carry a "verify current UI" flag where platforms change.

**Inspiration layer.** `match(asset_or_brief, filters)` over own and competitor assets with structured fields and performance; competitor assets marked signal only and never returned for text or product copying. `describe(asset)` for new assets.

**Experiment registry.** `propose`, `approve`, `start`, `read`, `decide`, `search_similar`. Every agent calls `search_similar` before proposing.

**Approval gate.** `submit(action, level, evidence)`; returns approved, edited or rejected, and records the human's edit so the brand brain and playbooks can learn.

## 6. Playbooks: two kinds per agent, decision and implementation

**The finding that forced this section.** Folder 11-ADC is named "ad copy and deployment" and holds 756 cards. About 400 are copywriting (8 Hour Copywriting Course, Cashvertising, Scientific Advertising, Copy Hackers, Harry Dry). About 350 are deployment and tactics: the Google Ads Free Course (100 cards), 2 TikTok Ads courses (73), 7 Meta Ads documents on the algorithm, structure for creative volume, scaling and top-of-funnel campaigns (115), an 8 and 9 figure account audit process (25), and Google Ads strategy documents (41). By keyword, 323 cards are deployment only, 214 are both, 144 are copy only. The 3 existing v1 workflows for this domain (`write-static-copy`, `revise-copy`, `objection-copy`) are all copy. The deployment half has no playbook.

The same gap exists in most folders: the cards say how to set things up, and the plan so far only listed playbooks that decide what to do. So every agent gets two kinds.

**Decision playbooks** say what to do and why: diagnose, choose, design, rank. 2,000 to 4,000 tokens. Model reads them with the numbers and the brand brain.

**Implementation playbooks** say how to do it in the platform, step by step, with the settings, the order, the checks and the traps. Each step carries a "verify the current UI" flag where the platform changes, a rollback note, and the guardrail that applies. They are what an L2 or L3 action executes against, and what a human follows when the agent stays at L1. 1,500 to 3,000 tokens each, tighter than decision playbooks because they are procedures.

**Folder contributions are many to many.** The map in section 3 is one agent per folder for ownership and ranking. But the cards in 11-ADC feed 3 agents: rank 2 takes the copy cards, rank 1 takes the Meta and TikTok deployment cards, rank 5 takes the Google deployment cards. Likewise 06-MEA feeds ranks 12, 1 and 5, and 03-OFF feeds ranks 7, 8 and 2. Distillation should pull by topic across folders, not by folder alone. Done on 24 Sep 2026 at the document level: the deployment documents moved to `24-DEP-ad-deployment` (Meta, TikTok, account audit) and `12-GAD` (Google Ads) in Drive, recorded in `data/library-v3/folder-overrides.json`. Readers should apply the overrides on load; cards.json is unchanged. The 214 cards that are both copy and deployment sit with their document, which is the right home for distillation.

### Implementation playbooks for the top 8 agents

**Rank 1, paid social.** `impl.meta.account-structure` (campaign, ad set and ad naming, CBO vs ABO, consolidation rules), `impl.meta.launch-campaign` (objective, optimisation event, attribution setting, placements, budget, creative slots, checks before publish), `impl.meta.structure-for-creative-volume`, `impl.meta.scale-tof` (budget step rules, duplication vs raise, when to reset learning), `impl.meta.audit-account` (the 8 and 9 figure audit process as a checklist), `impl.meta.retargeting-setup`, `impl.tiktok.launch-and-scale`, `impl.meta.pause-and-kill-rules`.

**Rank 2, ad copy and creative.** `impl.copy.static-ad-formats` (primary text, headline, description lengths and rules per placement), `impl.copy.hook-writing-process` (the 8 Hour and Sandcastles methods as steps), `impl.copy.claim-check-and-compliance`, `impl.copy.variant-naming-and-handoff` (so rank 1 can read results by variable), `impl.creative.static-production-spec` (sizes, safe zones, product lock, text density), `impl.creative.video-script-format`.

**Rank 3, experimentation.** `impl.exp.pre-register-test`, `impl.exp.set-up-ab-in-platform` (theme, app or server side), `impl.exp.qa-checklist`, `impl.exp.read-and-close`.

**Rank 4, profit.** `impl.profit.cogs-table-build`, `impl.profit.weekly-close-steps`, `impl.profit.reconcile-platform-to-store`, `impl.profit.cash-and-inventory-sheet`.

**Rank 5, Google Ads.** From the 100-card Google Ads course and the 12-GAD folder: `impl.google.account-and-conversion-setup`, `impl.google.merchant-center-and-feed`, `impl.google.shopping-campaign-build`, `impl.google.pmax-build-and-asset-groups`, `impl.google.search-campaign-build` (match types, RSAs, negatives), `impl.google.bidding-changes-by-stage`, `impl.google.brand-and-competitor-exclusions`, `impl.google.fix-underperforming-account` (the audit procedure).

**Rank 6, lifecycle.** `impl.email.flow-build` (trigger, filters, timing, splits, exit rules), `impl.email.segment-build`, `impl.sms.compliance-and-quiet-hours`, `impl.email.deliverability-setup` (domains, warm-up, list hygiene), `impl.email.campaign-send-checklist`.

**Rank 7, offers.** `impl.offer.bundle-setup-in-store`, `impl.offer.discount-and-guardrail-setup`, `impl.offer.subscription-setup`, `impl.offer.promotion-launch-checklist`.

**Rank 8, landing pages.** `impl.page.build-in-theme-sections`, `impl.page.quiz-funnel-build`, `impl.page.advertorial-build`, `impl.page.qa-before-traffic` (speed, mobile, tracking, links, claims).

Ranks 9 to 24 get the same treatment as they are built: at least 2 implementation playbooks each (store launch, tracking setup, SEO technical fixes, security settings, marketplace listing build, sample stages and purchase order, and so on). The 05-SET, 06-MEA, 12-GAD, 15-SEO and 22-AMZ folders are almost all implementation content already, so their decision playbooks will be short and their implementation playbooks long.

### Backlog totals

About 115 decision playbooks and about 90 implementation playbooks across the 24 agents. Build order for the first 40: the decision and implementation playbooks of ranks 1, 2, 4 and 5 (the weekly loop), then rank 3 and 6. Each is distilled from cards across folders by topic tag, edited once by Kevin, linked to card ids, versioned, and under its token cap.

## 7. Build order, given the full stack

Build the shapes, not the agents, first. Then fill agents in rank order.

1. Orchestrator, approval gate, registry client, audit log, model router. Shape B and Shape C as reusable runners.
2. Rank 1, 2 and 5 on Shape B and C. Rank 4 on Shape B. These four prove the weekly loop.
3. Shape D and Shape A. Rank 3 and Rank 12.
4. Rank 6, 8, 9, 7 (Shape E arrives with Rank 7).
5. The Weekly growth review program.
6. Ranks 10 to 17 in order, then the Launch program.
7. Ranks 18 to 24 as clients need them.

Promotion up the autonomy ladder happens per action type from the registry record, never by a decision to "turn on autonomy".

## 8. Questions for Kevin

1. Which channels does the paid media agent own on day one: Meta and Google only, or also TikTok, Pinterest and affiliates? It changes the channel workers.
2. For Shape E, who is the final judge on pricing and offer changes: always the owner, or can the agency approve inside a band?
3. Video creative: does the creative agent produce finished videos, or scripts and briefs for humans and tools? The full pipeline is a large build.
4. Should the Launch program include sourcing as a human checkpoint with an API later, or leave it fully outside?
5. Client-facing: do clients see all 20 agents, or a smaller set with the rest behind the agency?
