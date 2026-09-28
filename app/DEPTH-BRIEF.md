# ecomOS depth brief: from round 0 skeletons to an analytics platform (Kevin, 28 Sep 2026)

This is the founder's direction after reviewing round 0 of all 28 screens. It replaces the "10 candidates, founder picks" loop in `sessions/SESSIONS.md` for feature rounds. Read it first, then `app/CLAUDE.md`, then `app/contracts/`. It is written for the lead session that studies the Meta gallery and launches one manager session per screen.

## 1. What Kevin said, in order

1. **No more picking.** Do not ask the founder to choose 10 features. Build 10 features per screen per round, then keep looping: next 10, next 10. The founder reviews finished screens and gives step by step instructions; the managers build.
2. **Not a report. An analytics platform.** Round 0 reads like a report. Every screen must read like the Meta gallery built for Gehna (`meta_gallery/web/`, published at https://claude.ai/artifact/PYtCXf5norsr9vhSw4ZFVT): dense, visual, actionable, the most important thing at the top, then what is wrong, then the actions, then how each action gets implemented. Sections and subsections, not long text. Charts, matrices, maps, interactive diagrams, 3D where it helps the reader. Premium e-commerce look. The accent may move to green or blue; the lead decides the design system.
3. **Each screen is the best person in the world at that job, replaced by a screen plus agents.** Ask: if a world-class market researcher, Google Ads buyer, CRO lead or CX head had to hand their judgement to someone as a tool, what would the screen show, and what would its agents do? The screen shows the strategy, what is going right and wrong, what to do, what to prioritise, the top 10 things. The agents below it do the work. Deep analysis, not surface metrics. Surface metrics are allowed at the top as orientation only.
4. **Audit on every screen.** Each screen audits its whole domain end to end, ranks findings by a rubric, and pushes its top items up.
5. **Generalisable, plug and play, specific.** Any brand connects its sources and gets the same depth personalised from its own brain and data. Structure is fixed; content is the brand's.
6. **Order of operations.** Brand brain first, then market and product research, then customers and avatars, then competitors, then offers and pricing. Five screens, then Kevin reviews the brand brain, then the other four. Then the next five in screen order.
7. **Brand brain scope.** Founders add files any time and they are ingested (documents manifest exists). The brain holds everything about the brand: identity, positioning, products, competitors, the whole Ad Library pull, reviews, claims, policies. Positioning and brand facts are editable by the founder in the screen, and once edited they flow to every other screen from market research to site speed, security and Amazon. One consistent profile. No email data yet (not connected), so leave email out of the brain screen for now.
8. **Orchestrator on top of the brain.** With the data layer, the brain finds the bottleneck, ranks bottlenecks, picks the unlocks for each, and stack ranks the top 10 ideas the founder must approve. Rubric: revenue impact, profit impact, brand reputation impact, customer satisfaction (or a better rubric the lead proposes and writes down). Each screen's agent produces its ranked list on refresh; the orchestrator merges them into one master list, same rubric, and shows the 5 to 10 things the founder can approve today. Approval routes to an agent (does the work, hands to a human for verification and final approval) or to a human who implements from the screen.
9. **Ideas flow.** Ideas come from the web first (what the best operators and tools do), then from our own idea bank `ideas/v1/` (4,650 ideas, `python3 scripts/ideas.py`), then from the inspiration layer later. Add what the web pass finds that the bank lacks.
10. **Sessions.** Kevin wants to talk to each screen separately. One manager session per screen, long lived and named by screen, that builds the dashboard and spins its own sub-agents for the work. The lead session spins the managers. Go five at a time.
11. **Money.** Apify can go up to 100 dollars of tokens for this build; ask when a lane needs more. The Bombas weekly cap is 30 dollars (`app/brain/bombas/config/apify.json`), per run 4. Never pull by keyword on the Ad Library; page ids only.

## 2. The reference: what the Meta gallery does that round 0 does not

Study `meta_gallery/web/` (about 630 KB of JS: app, engine, overview, insights, lab, studio, sales, testlab, prodads, report, brandx, buyer, catalog, moves, health, festive) and `META_GALLERY_STATUS.md` updates 1 to 9. Things Kevin points at:

- The creative coverage matrix (`buyer.js`, section 6): where we spend by angle and format against where competitors spend, so a strategist sees the gaps and the next ads to make. Build this kind of matrix wherever a domain has a coverage question.
- Verdicts and fatigue on every ad, an action plan with ranked tests, a client report, competitor pills, a creative studio that makes variants from a reference, buyer cuts by audience and placement, a festive plan. Depth per element, not more elements.
- The page structure: tabs for jobs, a summary before detail, tables with tabular numbers, charts with a point, notes and CSV export, a date picker, exclusions.
- The reading level: a marketer reads it and knows what to do next.

The lead session writes down, in `app/contracts/depth.md`, the depth standard every screen must meet (sections, what a strategist sees at the top, what an action looks like, how implementation is shown, how the audit ranks, how the top 10 flows up) and, in `app/contracts/ui-kit.md` and `app/web/`, the design system (tokens, components, chart styles) that gives the platform one premium look. Screens then follow both.

## 3. What exists (do not rebuild)

- 28 screens plus setup at round 0 in `app/screens/<nn>-<slug>/` (api.py, audit.py, index.html, screen.js, FEATURES.md with room jobs, JTBD table and, for 5 screens, 10 ranked candidates). Audits return the contract shape (`app/contracts/audit.md`). 353 screen tests pass.
- Data layer: `app/data/generate.py` v2, Bombas at scale 1.0 (24 months daily, 23 tables, 9.5 GB SQLite git-ignored, aggregates committed), calibrated to founder numbers (457M, AOV 73, repeat 35 percent, channel mix 74/12/6/8, paid split 60/20/8/6/3/3). Metric contract `app/metrics.py`. Finance inputs and margin metrics. Rebuild: `python3 app/data/generate.py --brand bombas --scale 1.0 --as-of 2026-09-27` (never run tests while it writes).
- Brand brain: `app/brain/` (schema, store, package, router, merge, ladders, keeper, audit), Bombas brain of about 640 records across 22 sections, 7 objection ladders, diagnosis and positioning records, founder records, `BRAIN.md` router. Extractors in `app/brain/extract/` for any brand: site crawler, stack detector, Ad Library by page id, Amazon discovery, Reddit plan, press, jobs. Onboarding runner `app/brain/onboard.py`. Apify connector `app/connectors/apify.py` with ledger caps.
- Inspiration: contract `app/contracts/inspiration.md`, registry, puller A with media and rights (`app/inspiration/`). Pullers B, C, D and the UI block are not built; Kevin says the inspiration layer comes later.
- Idea bank `ideas/v1/` and the capability catalogue `agents/catalogue.json` (560 capabilities with autonomy).
- Sessions framework `sessions/SESSIONS.md`, `scripts/session.py`. Screens link to specs by id; `python3 scripts/session.py --room "<name>"` prints a room spec.

## 4. How the managers work

- One manager session per screen, titled `Manager: <nn>-<slug>`, model Opus (Fable for brand brain and market research, which set the pattern). Long lived: it keeps building rounds of 10 and Kevin can open it and give instructions. It reads this brief, `app/contracts/depth.md`, `app/contracts/ui-kit.md`, `app/CLAUDE.md`, `app/contracts/audit.md`, `app/contracts/metrics.md`, its own folder and its room spec. It never edits `app/data/generate.py`, other screens, or the ledger. Contract changes go through a short lead session.
- Each round: 10 features, one commit each, FEATURES.md rounds table updated per commit, a screenshot per round as `round<N>.png` under 1 MB, tests per feature, `git pull --rebase` before push. Sub-agents (the Agent tool) for research, web passes, chart work and tests; the manager integrates.
- Every feature is judged by: does a world-class operator learn something they could not see before, and can they act on it from the screen. Numbers computed in code, unavailable never zero, simulated labelled, no em dashes, short sentences.
- The audit and the top 10: every screen exposes `audit.run(brand, window)` findings with the rubric scores (revenue, profit, reputation, satisfaction) and a `rank` route; the brain screen's orchestrator merges all screens' lists into the master list.
- Reporting: when a round lands, the manager posts a 6-line note in FEATURES.md and the lead republishes the click-through page for Kevin.

## 5. Brand brain screen: what round 1 must contain

Kevin reviews this first. Sections, top to bottom:
1. **Brand profile, editable.** Identity, positioning (frame, category, price, competitive frame, proof points), voice, visual, products, offers, policies, claims by tier. Founder edits write approved records that win the merge and flow to every screen (the package builder already reads records; screens must read positioning from the brain, not their own fixtures).
2. **Files in.** Drop any file or paste a url; it lands in the documents manifest, gets read into records with source and date, and shows what it changed. Unstructured uploads are kept as documents and never blocked.
3. **Competitors and market.** The 12 competitor pages from the Ad Library with format and hook mixes against Bombas, the Reddit recommended-instead signal, the competitor frame; a coverage matrix (angles by format, us against them).
4. **Health.** Freshness by confidence heatmap, connectors, open conflicts with the site-wins default and a founder-decides button, the 5 open questions with inline answers, decisions log.
5. **The master list.** Bottlenecks ranked across all screens by the rubric, the unlocks under each, the top 10 for approval with the decision row (agent does it, send to a person, not now). This is the orchestrator's face; round 1 builds it on the 28 audits that exist.

## 6. Market and product research screen: what round 1 must contain

Kevin's example. Industry trend and sub-industry trends; emerging sub-categories; what people are talking about across platforms (Instagram post scraper by keyword through Apify, Reddit, reviews); new products in the category; shifting preferences (sustainability and others); the brand's position in the competitive landscape with an interactive map of the personas and markets served and not served; search terms for the brand and the industry; where the brand is falling behind on positioning and avatars. All actionable, ranked, with the actions and how to run them. Apify actors for Instagram and TikTok keyword pulls are allowed within the caps; page-id and keyword rules from the connector contract apply; usernames never stored.

## 7. What the lead session does first

1. Study the Meta gallery and this brief. Write `app/contracts/depth.md` and the design system in `app/contracts/ui-kit.md` plus `app/web/` (tokens, components, chart styles), with one sample screen section rebuilt to the standard as proof (brand brain is the natural choice).
2. Launch the first five managers in order (05-brand-brain, 01-market-research, 02-customers-avatars, 03-competitors, 04-offers-pricing), five at a time, each with a brief that carries sections 4 to 6 and its screen's room spec. Brand brain first so Kevin can review it while the others build.
3. Keep a check-in loop every 40 minutes: verify pushes, run tests, republish the click-through page https://claude.ai/artifact/HJscnVFPLxqbfCcysnmKmN (its source is the scratchpad builder; rebuild from the screens), report to Kevin in one message when brand brain round 1 is ready to review.
4. After Kevin's review, launch the next five in screen order and keep the loop going.
