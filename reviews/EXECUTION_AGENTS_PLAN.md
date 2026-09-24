# Execution layer: agent catalogue, ranking and build plan

Date: 24 Sep 2026. Companion to `INTELLIGENCE_REVIEW.md`. Planning only; nothing built.

Kevin's ask: list every agent the execution layer could offer, rank them from most to least useful, and for each say what it draws from the data layer, brand brain, intelligence layer and inspiration layer, and which playbooks it needs. Then decide whether working backwards from agents to playbooks is the right approach.

## 1. Is this the right approach?

Yes, with 3 conditions.

1. **Rank by value to a paying user and by data reach, not by folder.** 24 folders do not mean 24 equal agents. An agent that reads real ad and sales data for a live brand is worth more today than one that needs a business that does not exist yet. So the ranking below puts "brand already running" agents first and "start a business" agents later, even though Kevin's 2-year vision starts at product research.
2. **Every agent starts in draft mode.** It reads, diagnoses, drafts and proposes. A human clicks before anything is published, paused, spent or sent. This is already the Meta rule in `CLAUDE.md`. Keep it for Shopify, Klaviyo and Google too. Autonomous writes come only after the experiment registry shows an agent's proposals were accepted often.
3. **One shared spine, many thin agents.** The agents differ in playbook, inputs and tools. They should share one orchestrator, one brand record, one experiment registry, one audit log and one review gate. Building 20 separate agents each with its own plumbing is how this fails.

Working backwards then gives a clean list: the top 8 agents define the first 12 playbooks, the first 6 data tables and the first inspiration fields. That is a better build order than "finish the data layer, then the intelligence layer, then agents".

## 2. Design rules for the execution layer

**Four agent shapes.** Every agent below is one of these. Build the shape once, reuse it.

| Shape | How it runs | Used by |
|---|---|---|
| A. Checklist fan-out | Deterministic tools check each item (a page, a script, a setting, a permission). Sub-workers run in parallel. One model call summarises, ranks and writes the fix list. | Speed, security, store launch, measurement audit, brand consistency |
| B. Diagnose, hypothesise, propose | Pull numbers from the data layer. Do arithmetic in code. One model call reads the numbers with a diagnostics playbook and writes ranked hypotheses and next actions. | Paid media, finance, Google Ads, retention, SEO |
| C. Research, draft, critique, variants | Load brand record and avatar. Retrieve inspiration matches. Draft with a playbook. A second pass (critic) checks facts, claims, offer rules and voice. Return 3 variants plus an audit of what was used. | Ad copy and creative, landing pages, email, offers, organic content |
| D. Experiment loop | Read the registry. Propose a test with a hypothesis, metric, sample size and stop rule. Human approves. Agent tracks results from the data layer and writes the decision back. | CRO, creative testing, offer testing, promotions |

**On agents that debate each other.** Do not start there. The repo's evidence shows AI judges move 10 points on unchanged text, so 3 models voting mostly averages noise at 3x the cost. Use a single critic pass with a fixed checklist (facts, claims, offer rules, voice, completeness) plus deterministic checks (prices, arithmetic, banned words). Reserve a 2-model "propose and challenge" round for high-stakes calls only: budget reallocation over a set amount, offer changes, pricing. Even there, the human decides.

**What every agent must produce.** A deliverable, a short "why" with the numbers used, the list of cards and playbook version used, the brand facts relied on, cost and time, and a line in the experiment registry when a test is proposed. No customer-facing output mentions the source library.

**Model routing.** Shape A and B run on a cheap model with a playbook; the tools do the hard work. Shape C uses a strong model for the draft and a cheap model for the critic. Shape D uses a cheap model except for the hypothesis step.

## 3. Shared infrastructure (build once, before any agent)

| Component | What it does | Exists today? |
|---|---|---|
| Orchestrator | Takes a request, picks the agent, loads brand record and playbook, routes the model, runs the shape, logs the run | No. Task 7 in the review memo is the seed |
| Brand record (brand brain v1) | Facts, prices, costs, approved claims, offer rules, proof, voice examples, competitors, exclusions, learned preferences | Partial: `data/meta-gallery/brand.json` for Gehna, ad hoc sheets for Peach Bucket and TrailFold |
| Experiment registry | Hypothesis, brand, channel, assets, dates, budget, metric, result, decision. Read by every agent before it proposes a test | No. The gallery's action plan lists tests but does not store results |
| Data access layer | Typed readers for daily metrics, funnel, customers, catalog, support text, site audit | Partial: `meta_gallery/metrics.py` and the Metabase pull, for 1 brand |
| Audit log | One row per run: inputs, playbook version, cards, model, tokens, cost, output hash, human decision | Partial: `intelligence/budget.py` tracks cost only |
| Review gate | Blind side-by-side sheet and a ship / edit / rewrite label. Feeds learned preferences back to the brand record | No. Task 8 in the review memo |
| Critic and fact checker | Deterministic price, claim and arithmetic checks plus one cheap-model checklist pass | Partial: `scripts/owner_validation.py` and benchmark validators, not reusable yet |

## 4. Agent catalogue

Scores are 1 to 5. **Value** is how often a running brand needs it times how much money it touches. **Data** is how much of the input exists today for Gehna or Peach Bucket. **Knowledge** is the card-sample quality of the folders it draws on (from the review). **Risk** is how badly a wrong output hurts (5 is worst). Rank score = Value + Data + Knowledge minus Risk, then adjusted by my judgement where noted.

Inputs use these codes. D = data layer, B = brand record, I = intelligence layer (playbooks plus lookup cards), N = inspiration layer, R = experiment registry.

### Tier 1: build first (weeks 1 to 8). Serve brands that already sell.

**1. Paid media performance agent** (Shape B, then D). Folders 10-MCR, 11-ADC, 06-MEA, 20-FIN. Value 5, Data 5, Knowledge 4, Risk 2.
- Job: weekly and on-demand read of Meta results. Answers "ROAS dropped, what do I check", finds fatigue, spend concentration, creative winners and losers, audience overlap, attribution gaps. Ranks the next 5 tests. Drafts budget and pause proposals for approval.
- Sub-agents: metrics puller (code), fatigue and frequency checker (code), creative ranker (code plus vision model on thumbnails), hypothesis writer (model), test ranker (model, reads R).
- Inputs: D daily spend, revenue, orders by campaign, ad set and ad, plus impressions, frequency, CTR, CPM; D brand sales by day from Metabase; B margin and target contribution; I diagnostics playbook; R past tests.
- Outputs: diagnosis memo, ranked test list, proposed changes as a draft JSON. No writes to Meta.
- Playbooks needed: `paid-media.diagnose-performance-drop`, `paid-media.rank-creative-tests`, `paid-media.scale-or-cut`.
- Exists today: most of the data path, in the gallery's overview, insights and action plan tabs. This agent is the gallery made general and given a playbook.

**2. Creative and ad copy agent** (Shape C). Folders 11-ADC, 10-MCR, 02-AVT, 04-BRD. Value 5, Data 4, Knowledge 3, Risk 2.
- Job: from a brief, produce static ad concepts and copy variants that fit the brand, the avatar and the offer. Match winners in the account against the inspiration library to propose formats. Build variants of a reference image with the real product locked.
- Sub-agents: brief checker (code, against B), inspiration matcher (embedding over N), concept writer (strong model, playbook), copy writer (strong model, ad-copy v2 playbook), critic (cheap model plus deterministic claim check), image variant builder (existing studio path).
- Inputs: B facts, claims, offer rules, voice; D ad-level winners and losers with metrics; N statics with structured descriptions and performance; I ad-copy v2 and creative-concept playbooks; R what was already tested.
- Outputs: 3 concepts, each with copy variants, format, reference match, and a claim audit. Draft only.
- Playbooks: `ad-copy.write-static-copy` (v1.2 is the base), `creative.concept-from-winners`, `creative.variant-plan`.
- Exists today: creative studio in the gallery, ad-copy v1.2, `creative_retrieval.py`. Missing: brand record, inspiration descriptions, critic.

**3. Profit and finance agent** (Shape B). Folders 20-FIN, 06-MEA. Value 5, Data 4, Knowledge 5, Risk 3.
- Job: turn orders, spend, COGS and fees into contribution margin, MER, contribution after ads, cash tied in stock, by day, week and product. Reconcile platform numbers to the P&L. Flag missing days and duplicates. This is the base for Kevin's plan to send gross profit through CAPI: the numbers must be right in a table before they go anywhere.
- Sub-agents: data integrity checker (code), margin calculator (code), reconciler (code), narrator (cheap model, playbook).
- Inputs: D orders, refunds, spend by channel, COGS per SKU, shipping and payment fees; B cost assumptions and tax rules; I finance playbook.
- Outputs: a weekly profit memo, a per-SKU contribution table, alerts. All arithmetic in code.
- Playbooks: `finance.weekly-contribution-readout`, `finance.reconcile-platform-to-pnl`, `finance.unit-economics-by-sku`.
- Exists today: Metabase sales pull, Peach Bucket unit economics in the handoff. Missing: COGS table, reconciliation.

**4. Measurement and tracking agent** (Shape A). Folders 06-MEA, 12-GAD, 23-SEC (store security cards only). Value 4, Data 3, Knowledge 4 with stale risk, Risk 3.
- Job: audit pixel, CAPI, GA4 and Google Ads conversion setup. Check event coverage, duplicates, deduplication keys, attribution windows, consent. Later: draft the CAPI enrichment (gross profit, COGS) as a spec for a developer.
- Sub-agents: event fetcher (Meta dataset stats via MCP, GA4 export), checklist runner (code), gap explainer (cheap model, playbook).
- Inputs: D event counts by source, purchase counts by platform vs Shopify; B attribution settings; I measurement playbook with a "verify the current UI" rule.
- Outputs: audit table with pass, fail and unknown; fix list; CAPI spec draft.
- Playbooks: `measurement.audit-tracking`, `measurement.capi-enrichment-spec`.
- Caution: the folder's cards name menu paths that go stale. The playbook must state checks, not clicks.

**5. CRO and experiment agent** (Shape D). Folders 09-CRO, 07-LPG, 03-OFF. Value 4, Data 3, Knowledge 5, Risk 2.
- Job: read the funnel, find the biggest drop, propose 3 tests with hypothesis, metric, guardrails, sample size and stop rule. Register them. Track results and write the decision. Kevin's "suggest experiments, run them, keep results" agent.
- Sub-agents: funnel reader (code), test designer (model, playbook), sample size calculator (code), result reader (code), decision writer (model).
- Inputs: D sessions, ATC, checkout, purchase by device and source; page inventory; B margins, offer rules; I CRO playbook; R everything tried before.
- Outputs: test proposals, registry entries, readouts. Implementation stays human or a later landing-page agent.
- Playbooks: `cro.find-biggest-drop`, `cro.design-test`, `cro.read-result`.
- Exists today: 09-CRO is the strongest folder. Missing: funnel data feed and registry.

**6. Email and SMS lifecycle agent** (Shape C). Folders 14-EML, 17-CXP, 03-OFF. Value 4, Data 3, Knowledge 4, Risk 2.
- Job: audit existing flows, draft missing ones (welcome, abandoned checkout, post-purchase, win-back), write the emails in brand voice, propose send logic and tests.
- Sub-agents: flow auditor (Klaviyo export reader, code), gap finder (model), copy writer (strong model, playbook), critic.
- Inputs: D flow performance, list size, segments; B voice, claims, offers, product facts; I lifecycle playbook; N email references; R.
- Outputs: flow map, email drafts, test plan.
- Playbooks: `email.audit-flows`, `email.write-flow-emails`, `email.plan-campaign-calendar`.
- Missing: Klaviyo or equivalent read access.

**7. Landing page and PDP agent** (Shape C, uses A for audit). Folders 07-LPG, 09-CRO, 03-OFF, 08-SPD. Value 4, Data 3, Knowledge 4, Risk 2.
- Job: audit a page against the offer, avatar and traffic source. Draft a new section order and copy. Later, produce a page draft in the store's section format.
- Sub-agents: page fetcher and structure reader (code), audit checklist (model with playbook), copy drafter (strong model), critic, speed check (calls agent 11).
- Inputs: D page funnel by source; B facts, proof, offer; I landing-page playbook; N landing page references (later).
- Outputs: audit, wireframe as text, section copy, test proposal to agent 5.
- Playbooks: `landing.audit-page`, `landing.draft-cold-traffic-page`, `landing.pdp-rebuild`.

**8. Offer and pricing agent** (Shape C, D for tests). Folders 03-OFF, 20-FIN, 02-AVT. Value 4, Data 3, Knowledge 4, Risk 4.
- Job: design or improve the offer: bundles, guarantees, tiers, promotions. Every option costed before it is proposed. Respect fixed-offer rules.
- Sub-agents: economics calculator (code), option writer (strong model), critic against B offer rules, test designer (agent 5).
- Inputs: D price, COGS, AOV, conversion, refunds by SKU; B offer rules, policies; I offers playbook; R.
- Outputs: 3 costed options with contribution per order, a presentation fix list for fixed offers, a test proposal.
- Playbooks: `offers.design-offer`, `offers.audit-fixed-offer`, `offers.plan-promotion`.

### Tier 2: build next (weeks 8 to 16). High value, but needs data or knowledge work first.

**9. Google Ads agent** (Shape B). Folder 12-GAD, 06-MEA. Value 4, Data 2 (no Google connector yet), Knowledge 4 with stale risk, Risk 3. Same shape as agent 1 for Search, Shopping and PMax: search-term waste, feed issues, brand exclusions, scaling gates. Playbooks: `google.diagnose-account`, `google.shopping-vs-pmax`, `google.search-term-cleanup`. Blocked on read access to Google Ads.

**10. Avatar and customer research agent** (Shape C). Folders 02-AVT, 01-PRD. Value 4, Data 3, Knowledge 2 (weak folder), Risk 2. Mines reviews, support tickets and comments into an evidence-led avatar with verbatim language and objections. Feeds agents 2, 6, 7, 8. The folder is weak, so the playbook should come mostly from the review-mining and jobs-to-be-done cards, and the strength comes from the brand's own text. Playbooks: `avatar.build-from-evidence`, `avatar.mine-objections`. Missing: review and support text feed.

**11. Site speed agent** (Shape A). Folder 08-SPD. Value 3, Data 4 (public URLs suffice), Knowledge 4, Risk 1. Kevin's example. Sub-agents: Lighthouse and CrUX runner per template (code), script and app inventory (code), image audit (code), fix ranker (cheap model, playbook). Mostly deterministic. Playbook: `speed.audit-and-prioritise`. Cheap to build and a good first Shape A.

**12. Retention and post-purchase agent** (Shape B plus C). Folders 17-CXP, 14-EML, 19-WLD. Value 3, Data 3, Knowledge 3, Risk 2. Cohort repeat rate, LTV window, delivery and support issue patterns, replenishment timing, a bounded "wild bet" test. Playbooks: `retention.cohort-readout`, `retention.post-purchase-flow`. Fold 19-WLD into this agent.

**13. Brand brain keeper** (Shape C, but its main job is upkeep). Folder 04-BRD. Value 4 as infrastructure, Data 3, Knowledge 2, Risk 2. Onboards a brand through the sequence Kevin described (site, ads, tone, competitors), drafts the brand record and voice guide, and updates learned preferences from the review gate. 04-BRD is the weakest folder, so the playbook should lean on Kevin's taste and the brand's approved copy. Playbooks: `brand.onboard-brand-record`, `brand.voice-guide`, `brand.consistency-audit`.

**14. SEO agent** (Shape A plus B). Folder 15-SEO, 08-SPD. Value 3, Data 2 (needs Search Console), Knowledge 4, Risk 1. Indexability, page titles, collection content, query demand, rewrite manufacturer copy. Playbooks: `seo.technical-audit`, `seo.collection-and-pdp-content`.

### Tier 3: build later (after 16 weeks). For new businesses, or thin evidence.

**15. Product research agent** (Shape C). Folder 01-PRD. Value 3 for new businesses, 1 for running brands. Data 2 (needs external market data). Knowledge 3. Risk 3. Validation checklist, competitor offer research, expansion prioritisation. Playbooks: `product.validate-opportunity`, `product.research-competition`. First step of the 2-year vision, but not the first agent to build.

**16. Store setup and launch agent** (Shape A). Folder 05-SET. Value 3 new, 1 running. Data 3. Knowledge 4 but the highest stale risk. Risk 2. Launch checklist, test purchase walk, payments, shipping, policies, domain. Playbook: `store.launch-checklist` with "verify the current UI" on every step.

**17. Organic content agent** (Shape C). Folder 13-ORG. Value 3. Data 2. Knowledge 2 (creator philosophy, thin). Risk 1. Hooks, content calendar, repurposing. Playbook: `organic.content-plan`. Low priority until the folder improves or the brand supplies its own winning posts.

**18. Answer engine (AEO) agent** (Shape A). Folder 16-AEO. Value 2 today. Data 2. Knowledge 3 with high stale risk. Risk 2. Observe how AI answers mention the brand, find mention gaps, propose page fixes. Playbook: `aeo.visibility-audit`. Keep as an observation tool until there is evidence it moves sales.

**19. Amazon marketplace agent** (Shape B). Folder 22-AMZ. Value 2 unless a client sells on Amazon. Data 1. Knowledge 4 but reseller-shaped (90% one FBA course). Risk 3. Build only when a brand needs it.

**20. Security and bot agent** (Shape A). Folder 23-SEC. Value 2. Data 3. Knowledge 2 for operators (79% developer course). Risk 2. Admin access, permissions, app scopes, payment fraud settings, bot signs in analytics. Playbook: `security.store-hygiene-checklist` from the roughly 90 store-security and agent cards only.

**21. Team and operations agent** (Shape C). Folder 21-OPS. Value 2. Data 2. Knowledge 3. Risk 1. Weekly task board, agency update, process checklists. Useful for the agency side of Kevin's business, not for the brand. Playbook: `ops.weekly-update-and-board`.

**Excluded for now:** sourcing (Kevin will outsource it; the agent 3 COGS table is the only hook), wild bets (folded into 12), and fully autonomous execution (any writes to ad accounts, stores or email tools).

### Ranking table

| Rank | Agent | Shape | Value | Data | Knowledge | Risk | Score | Tier |
|---|---|---|---|---|---|---|---|---|
| 1 | Paid media performance | B, D | 5 | 5 | 4 | 2 | 12 | 1 |
| 2 | Creative and ad copy | C | 5 | 4 | 3 | 2 | 10 | 1 |
| 3 | Profit and finance | B | 5 | 4 | 5 | 3 | 11 | 1 |
| 4 | Measurement and tracking | A | 4 | 3 | 4 | 3 | 8 | 1 |
| 5 | CRO and experiments | D | 4 | 3 | 5 | 2 | 10 | 1 |
| 6 | Email and SMS lifecycle | C | 4 | 3 | 4 | 2 | 9 | 1 |
| 7 | Landing page and PDP | C, A | 4 | 3 | 4 | 2 | 9 | 1 |
| 8 | Offer and pricing | C, D | 4 | 3 | 4 | 4 | 7 | 1 |
| 9 | Google Ads | B | 4 | 2 | 4 | 3 | 7 | 2 |
| 10 | Avatar and research | C | 4 | 3 | 2 | 2 | 7 | 2 |
| 11 | Site speed | A | 3 | 4 | 4 | 1 | 10 | 2 |
| 12 | Retention and post-purchase | B, C | 3 | 3 | 3 | 2 | 7 | 2 |
| 13 | Brand brain keeper | C | 4 | 3 | 2 | 2 | 7 | 2 |
| 14 | SEO | A, B | 3 | 2 | 4 | 1 | 8 | 2 |
| 15 | Product research | C | 3 | 2 | 3 | 3 | 5 | 3 |
| 16 | Store setup and launch | A | 3 | 3 | 4 | 2 | 8 | 3 |
| 17 | Organic content | C | 3 | 2 | 2 | 1 | 6 | 3 |
| 18 | Answer engines | A | 2 | 2 | 3 | 2 | 5 | 3 |
| 19 | Amazon | B | 2 | 1 | 4 | 3 | 4 | 3 |
| 20 | Security and bots | A | 2 | 3 | 2 | 2 | 5 | 3 |
| 21 | Team and operations | C | 2 | 2 | 3 | 1 | 6 | 3 |

Where the score and the rank disagree, I moved the agent by hand. Site speed scores 10 but sits at 11 because it touches little money. Measurement scores 8 but sits at 4 because agents 1, 3 and 5 all depend on clean tracking. Brand brain keeper is infrastructure and belongs in the shared spine; it is ranked here only for its onboarding job.

## 5. What each layer must provide

This is the contract the top 8 agents need. Build these tables and fields first.

**Data layer (per brand, daily grain, one currency, one timezone, with a missingness flag on every row)**
1. `ad_metrics`: date, platform, campaign, ad set, ad, spend, impressions, clicks, frequency, purchases, value, attribution window. Agents 1, 2, 9.
2. `sales`: date, orders, gross, discounts, refunds, net, new vs returning, by product. Agents 1, 3, 5, 12.
3. `costs`: SKU, COGS, shipping, payment fee rate, platform fees, RTO rate. Agent 3, 8.
4. `funnel`: date, source, device, sessions, product views, ATC, checkout, purchase. Agents 5, 7.
5. `customers`: customer id, first order date, orders, LTV, last order, consent. Agents 6, 12.
6. `catalog`: SKU, title, price, inventory, URL, images. Agents 2, 7, 8.
7. `text`: reviews, support tickets, ad comments, with dates. Agent 10.
8. `site_audit`: URL, template, Lighthouse and CrUX scores, scripts, apps. Agents 7, 11.
9. `events`: pixel and CAPI counts by event and source. Agent 4.
Integrity checks run before any agent reads: missing days, duplicates, currency, negative values, platform totals versus store totals.

**Brand record (brand brain v1)**
Facts and products, prices and costs, approved claims and proof, offer rules (fixed offers, allowed discounts, guarantees), voice examples (liked and disliked), avatar summaries, competitors, attribution settings, exclusions, learned preferences from the review gate, version and date.

**Intelligence layer**
One distilled playbook per agent workflow (about 40 playbooks for the top 14 agents; 24 for Tier 1). Each 2,000 to 4,000 tokens, with rule-to-card links for lookup, a "verify the current UI" line where platforms change, and a version. Cards stay as the lookup store with the fixes from the review memo.

**Inspiration layer**
Statics first: image, brand, date, format, hook type, product placement, text density, colour, offer shown, people or not, performance if known, source (own account or competitor). Own-account assets carry ad-level metrics. Competitor assets are marked signal only. Later: emails and landing pages with the same idea. Video after statics show use.

**Experiment registry**
id, brand, agent, hypothesis, channel, assets, start, end, budget, metric, guardrails, sample size, result, decision, notes. Written by agents 1, 2, 5, 8, 12. Read by all.

## 6. Playbook backlog derived from Tier 1

In build order. The first 6 come straight from the agents that can run on Gehna data today.

1. `paid-media.diagnose-performance-drop` (agent 1)
2. `ad-copy.write-static-copy` v2 from v1.2 (agent 2)
3. `finance.weekly-contribution-readout` (agent 3)
4. `paid-media.rank-creative-tests` (agent 1)
5. `creative.concept-from-winners` (agent 2)
6. `measurement.audit-tracking` (agent 4)
7. `cro.design-test` and `cro.read-result` (agent 5)
8. `email.write-flow-emails` (agent 6)
9. `landing.audit-page` (agent 7)
10. `offers.design-offer` and `offers.audit-fixed-offer` (agent 8)
11. `finance.unit-economics-by-sku` (agent 3)
12. `paid-media.scale-or-cut` (agent 1)

Each playbook: distil from the folder through search and the markdown exports, Kevin edits once, link rules to card ids, keep under 4,000 tokens, version it. That is the task shape from the review memo.

## 7. Build plan

**Wave 0 (weeks 1 to 3): the spine.** Brand record schema and 2 records. Orchestrator with routing and audit log. Experiment registry table. Review gate sheet. Retrieval fixes and corpus exclusions from the review memo. Data readers for `ad_metrics` and `sales` lifted from the gallery. Acceptance: one end-to-end run of a stub agent on Gehna data, logged, reviewed by Kevin.

**Wave 1 (weeks 3 to 8): agents 1, 2, 3.** Paid media performance on Gehna. Creative and ad copy on Gehna or Peach Bucket. Finance readout on Gehna once a COGS table exists. Six playbooks. The experiment from the review memo runs inside this wave. Acceptance: Kevin ships or lightly edits at least half the outputs in the blind review.

**Wave 2 (weeks 8 to 12): agents 4, 5, 11.** Measurement audit, CRO experiment loop and site speed. These are the checklist and registry shapes, so they prove the shared spine handles Shape A and D. Needs the funnel feed.

**Wave 3 (weeks 12 to 16): agents 6, 7, 8, 10.** Email, landing page, offers, avatar. Needs Klaviyo read access, page fetcher and the review or support text feed.

**Wave 4 (after 16 weeks): Tier 2 and 3** in rank order, as data access arrives. Google Ads waits on a connector. Product research and store launch wait for a new-business client. Inspiration layer descriptions for the 3,000 to 4,000 statics can start any time as a background job, since agent 2 gets better as it fills.

**Client interface.** After Wave 1 works for 1 brand, wrap the orchestrator in the gallery's server so the owner asks in plain words and the orchestrator picks the agent. Hosting, auth and tenant separation are their own project before a second client sees it.

## 8. Are we on the right path?

Yes, if the next thing built is the spine plus agents 1 to 3 on one brand, and not a full data warehouse or 21 agents in parallel. The vision of one person starting and running a store from this system is reachable, but it is reached by making a live brand's weekly work better first. That earns the data, the brand records and the learned preferences that the new-business agents will need later.

Three things would put it on the wrong path: building agents before the brand record and registry exist, letting any agent write to a platform before its proposals have a track record in the review gate, and judging agents by AI scores instead of by whether Kevin or the client ships the output.

## 9. Questions for Kevin

1. Which brand runs Wave 1: Gehna (most data) or Peach Bucket (copy work already started)?
2. Can we get read access to Klaviyo (or the email tool) and Shopify analytics for that brand by week 8? That decides whether Wave 3 is on time.
3. For the profit agent: does a COGS per SKU table exist for that brand, or must it be built by hand first?
4. Is the client interface a chat box, a dashboard with buttons per agent, or both? It changes how the orchestrator exposes agents.
5. Agency use: do you want the team and operations agent early because your agency runs the accounts, even though it scored low for the brand itself?
