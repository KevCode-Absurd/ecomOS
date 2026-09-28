# Sessions: how ecomOS gets built without bloated context windows

Date: 28 Sep 2026. Machine copy: `sessions/sessions.json`. Card for any session: `python3 scripts/session.py <id>`.

## The rules

1. **One session, one deliverable, one folder.** A session reads at most 3 named files plus its own folder, writes the files on its card, commits, pushes, and ends. Nothing else is in scope.
2. **The card is the brief.** `python3 scripts/session.py S1.2a` prints the first line to type, the reads with token estimates, the writes and the done-when. The first line is fixed. Do not improvise a longer one.
3. **Budgets are real.** Build sessions start under about 25k tokens, bulk sessions under 12k, contract and review sessions under 40k. The card prints the estimate. If the reads exceed the budget, the session is too big: split it before starting.
4. **The big files are never opened.** `agents/catalogue.json` is about 300k tokens, `agents/rooms/rooms.json` about 180k, `agents/DATA-LAYER.md` 11k, `app/data/generate.py` 22k. Query them: `scripts/session.py --room "Paid social"`, `--capability MEDIA-C04`, `--capabilities MEDIA`, `--contract 3,5`, `--sample bombas offers`. A session that needs a slice gets the slice.
5. **Reading many things is a sub-agent's job.** When a session must survey files, docs or the web, it spawns an agent that returns at most 500 words, or records in the schema, never pages. The parent keeps its context for building.
6. **Memory is files and git, never the transcript.** Each stage folder keeps a `STATUS.md` under 30 lines: what is done, what is next, what was parked and why. The last act of every session is updating it. The next session reads `STATUS.md`, not the history. The commit message carries the reason for a decision.
7. **`/clear` after every commit.** One deliverable per conversation. Ask for the numbered item, never "improve X".
8. **Tests are the done check.** A session ends by running its tests and printing the counts. A session without a test writes one.
9. **Parallel groups run in worktrees.** Sessions in the same parallel group (S1.3, S2.1) run at the same time in separate worktrees. They share nothing but the contract. Contract changes are their own session and land first.
10. **Model by session type.** Contracts, schemas, reviews and ranking: Fable. Building: Opus. Bulk and parallel work (extractors, field census, overlays): Sonnet. Tagging inside pipelines at runtime: Haiku.
11. **Nothing paid without a card that says so.** Extractors use public pages and sub-agent web reads. No embedding calls, no benchmark reruns.

## Why this keeps context small

The heavy knowledge lives in files with a query script in front of it. A session is a card: 3 files, a folder, a first line. The brain contract is 7.7k tokens but a session reads 2 of its sections (1.8k). The product plan is 9k tokens and no build session reads it at all. `STATUS.md` replaces the history. Sub-agents do the reading. The result: a build session starts around 5k to 8k tokens and spends the rest of its window on the work.

## The whole build in numbers

| Stage | What | Sessions | Lead model | Runs in parallel |
|---|---|---|---|---|
| 1 | Brand brain: store, router, extractors, merge, keeper | 10 | Opus, Sonnet for extractors | the 5 extractors |
| 2 | Data layer: field census, contract v2, generator, finance inputs | 16 | Sonnet for census, Opus for the generator | the 12 census sessions |
| 3 | Interface: audit contract, setup, 28 screens round 0, then feature rounds | 33 plus feature rounds | Opus builds, Fable ranks | screens within a phase |
| 4 | Inspiration: contract, 4 pullers, the UI block | 6 | Sonnet pullers, Opus UI | the 4 pullers |
| 5 | The loop: findings, propose, dispatch, QA, registry, orchestrator, demo | 5 | Opus, Fable for the demo | none, it is a chain |
| 6 | Hosted product: database, auth, worker, live connectors, storage, deploy, security | 11 | Opus | the 5 live connectors |
| 7 | Subscription variant plan | 1 | Fable | none |
| | **Total** | **82 cards** | Opus 49, Sonnet 22, Fable 11 | |

Feature rounds are not counted: each screen gets rounds of 10 as long as the founder keeps asking, one commit per feature, using the S3.R card. A realistic first pass is 2 rounds on the 6 screens that matter most (Today, brand brain, paid social, Google Ads, email, CRO), about 120 feature commits.

Sequence: stage 1 and the stage 2 census group start together. Stage 3 starts when the audit contract exists and the generator has Bombas data. Stage 4 runs alongside stage 3 feature rounds. Stage 5 needs Today, paid social and Google Ads at round 0. Stage 6 starts after the end to end demo. Stage 7 last.

## Where everything lives

| What | Now (demo) | Hosted | Committed |
|---|---|---|---|
| Brain records | `app/brain/<brand>/<section>.json`, one file per section | Postgres table `records` with `brand_id`, same JSON export | yes for public demo brands, no for real brands |
| `BRAIN.md` router | `app/brain/<brand>/BRAIN.md`, regenerated on publish | same, served at `/brain/<brand>/BRAIN.md` | yes for demo brands |
| Documents (uploads) | `app/brain/<brand>/documents/` plus `manifest.json` | object storage bucket, manifest in the database | never for real brands |
| Assets (product images, ad creative) | `app/brain/<brand>/assets/` with a manifest | bucket | never |
| Review queue, versions, changes, freshness | JSON files next to the sections | tables | demo only |
| Data layer, aggregates | `app/data/brands/<brand>/aggregates/*.json` | tables | yes |
| Data layer, row level | `app/data/brands/<brand>/data.sqlite`, regenerated by one command | Postgres | never |
| Finance inputs | `app/data/brands/<brand>/finance_inputs.json` | table with effective dates | demo only |
| Findings, decisions, registry | `app/data/brands/<brand>/{findings,decisions,registry}.json` | tables | demo only |
| Connector census | `app/contracts/connectors/<platform>.md` | same | yes |
| Contracts, schemas, sessions, code, tests | the repo | the repo | yes |
| Spec shelf | `agents/`, `ideas/`, read by id through `scripts/session.py` | same | yes, unchanged |
| Credentials | `.env`, `secrets/` | secrets manager | never |
| Session memory | `STATUS.md` in each stage folder, git log | same | yes |

One layout per brand, demo or real:

```
app/brain/<brand>/         BRAIN.md, <section>.json x28, sources.json, assumptions.json,
                           freshness.json, review.json, changes.json, documents/, assets/
app/data/brands/<brand>/   aggregates/, data.sqlite (not committed), finance_inputs.json,
                           findings.json, decisions.json, registry.json, README.md
```

The store module is the only thing that knows whether it is reading files or a database. S6.1 swaps it. Nothing above it changes.

## How we proceed

1. Read the card: `python3 scripts/session.py <id>`.
2. Open a fresh session (a new window, or a sibling session created from this one) and paste the first line.
3. The session works inside its budget, commits, pulls with rebase, pushes, updates `STATUS.md`, ends.
4. Parallel groups open one session per card at the same time, each in its own worktree or sibling session.
5. Kevin reviews at S1.4, S2.5, each S3.P publish, and S5.5.

## Stage 1: brand brain

| Id | Session | Model | Budget | Needs |
|---|---|---|---|---|
| S1.2a | Brain store, package builder and BRAIN.md router | opus | 22,000 | none |
| S1.2b | brain_sections overlay for every capability | sonnet | 12,000 | S1.2a |
| S1.3a | Bombas extractor: site crawl (parallel S1.3) | sonnet | 15,000 | S1.2a |
| S1.3b | Bombas extractor: Meta Ad Library (parallel S1.3) | opus | 15,000 | S1.2a |
| S1.3c | Bombas extractor: press, interviews and podcasts (parallel S1.3) | sonnet | 15,000 | S1.2a |
| S1.3d | Bombas extractor: public reviews and forums (parallel S1.3) | sonnet | 15,000 | S1.2a |
| S1.3e | Bombas extractor: job postings and stack (parallel S1.3) | sonnet | 15,000 | S1.2a |
| S1.3f | Bombas extractor: own-site, Amazon and retailer reviews, 5-star and 1-star | opus | 20,000 | S1.2a |
| S1.3h | Bombas extractor: Reddit mentions and category threads | sonnet | 18,000 | S1.2a |
| S1.3g | Objection ladders and re-merge | opus | 30,000 | S1.3f, S1.3m, S1.3h |
| S1.3m | Bombas merge and first publish | opus | 30,000 | S1.3a, S1.3b, S1.3c, S1.3d, S1.3e |
| S1.4 | Brain review with Kevin | fable | 20,000 | S1.3m |
| S1.5 | Keeper: gaps, the ask, the weekly audit | opus | 25,000 | S1.2a |
| S1.6 | Apify connector: Amazon reviews, Meta Ad Library, Reddit adapters | opus | 25,000 | S1.2a |

Order: S1.2a first (everything reads the store). Then S1.2b and S1.5 in parallel with the S1.3 group. S1.3m after the group. S1.3f and S1.3g add the review lanes and the objection ladders (default for every new brand from now on). S1.4 with Kevin.

## Stage 2: data layer

| Id | Session | Model | Budget | Needs |
|---|---|---|---|---|
| S2.1a | Field census: Meta Marketing API insights and creatives (parallel S2.1) | sonnet | 10,000 | none |
| S2.1b | Field census: Meta Ad Library, datasets and catalog (parallel S2.1) | sonnet | 10,000 | none |
| S2.1c | Field census: Google Ads API (parallel S2.1) | sonnet | 10,000 | none |
| S2.1d | Field census: Google Merchant Center (parallel S2.1) | sonnet | 10,000 | none |
| S2.1e | Field census: GA4 Data API (parallel S2.1) | sonnet | 10,000 | none |
| S2.1f | Field census: Shopify Admin API (parallel S2.1) | sonnet | 10,000 | none |
| S2.1g | Field census: Klaviyo API (parallel S2.1) | sonnet | 10,000 | none |
| S2.1h | Field census: Gorgias API (parallel S2.1) | sonnet | 10,000 | none |
| S2.1i | Field census: Google Search Console (parallel S2.1) | sonnet | 10,000 | none |
| S2.1j | Field census: Amazon SP-API and Ads API (parallel S2.1) | sonnet | 10,000 | none |
| S2.1k | Field census: WooCommerce REST API (parallel S2.1) | sonnet | 10,000 | none |
| S2.1l | Field census: Mailchimp API (parallel S2.1) | sonnet | 10,000 | none |
| S2.2 | Data sources v2 contract | fable | 40,000 | S2.1a, S2.1c, S2.1e, S2.1f, S2.1g |
| S2.3 | Generator v2 for Bombas | opus | 50,000 | S2.2, S1.3m |
| S2.4 | Brand-supplied numbers and margin metrics | opus | 25,000 | S2.2 |
| S2.5 | Data review with Kevin | fable | 20,000 | S2.3, S2.4 |

Order: the S2.1 group can start today, in parallel, nothing depends on the brain. S2.2 once the 5 core census files exist. S2.3 needs the Bombas brain for calibration.

## Stage 3: interface

| Id | Session | Model | Budget | Needs |
|---|---|---|---|---|
| S3.0 | Setup screen round 0 | opus | 20,000 | S1.5, S2.4 |
| S3.1 | Audit contract | fable | 25,000 | none |
| S3.x | Any screen, round 0 then rounds of 10 | opus builds, fable ranks | 20,000 | S3.1 |
| S3.2 | Screen 00-today round 0 (parallel S3-phase-A) | opus | 20,000 | S3.1, S2.3 |
| S3.3 | Screen 05-brand-brain round 0 (parallel S3-phase-B) | opus | 20,000 | S3.1, S2.3 |
| S3.4 | Screen 11-paid-social round 0 (parallel S3-phase-D) | opus | 20,000 | S3.1, S2.3 |
| S3.5 | Screen 12-google-ads round 0 (parallel S3-phase-D) | opus | 20,000 | S3.1, S2.3 |
| S3.6 | Screen 01-market-research round 0 (parallel S3-phase-B) | opus | 20,000 | S3.1, S2.3 |
| S3.7 | Screen 02-customers-avatars round 0 (parallel S3-phase-B) | opus | 20,000 | S3.1, S2.3 |
| S3.8 | Screen 03-competitors round 0 (parallel S3-phase-B) | opus | 20,000 | S3.1, S2.3 |
| S3.9 | Screen 04-offers-pricing round 0 (parallel S3-phase-B) | opus | 20,000 | S3.1, S2.3 |
| S3.10 | Screen 06-store-health round 0 (parallel S3-phase-C) | opus | 20,000 | S3.1, S2.3 |
| S3.11 | Screen 07-landing-pages-cro round 0 (parallel S3-phase-C) | opus | 20,000 | S3.1, S2.3 |
| S3.12 | Screen 08-site-speed round 0 (parallel S3-phase-C) | opus | 20,000 | S3.1, S2.3 |
| S3.13 | Screen 09-creative round 0 (parallel S3-phase-D) | opus | 20,000 | S3.1, S2.3 |
| S3.14 | Screen 10-copy round 0 (parallel S3-phase-D) | opus | 20,000 | S3.1, S2.3 |
| S3.15 | Screen 13-affiliate-marketplace-ads round 0 (parallel S3-phase-D) | opus | 20,000 | S3.1, S2.3 |
| S3.16 | Screen 14-email-messaging round 0 (parallel S3-phase-E) | opus | 20,000 | S3.1, S2.3 |
| S3.17 | Screen 15-customers-cx round 0 (parallel S3-phase-E) | opus | 20,000 | S3.1, S2.3 |
| S3.18 | Screen 16-organic-content round 0 (parallel S3-phase-F) | opus | 20,000 | S3.1, S2.3 |
| S3.19 | Screen 17-seo round 0 (parallel S3-phase-F) | opus | 20,000 | S3.1, S2.3 |
| S3.20 | Screen 18-answer-engines round 0 (parallel S3-phase-F) | opus | 20,000 | S3.1, S2.3 |
| S3.21 | Screen 19-supply-inventory round 0 (parallel S3-phase-G) | opus | 20,000 | S3.1, S2.3 |
| S3.22 | Screen 20-marketplaces round 0 (parallel S3-phase-G) | opus | 20,000 | S3.1, S2.3 |
| S3.23 | Screen 21-finance-cash round 0 (parallel S3-phase-G) | opus | 20,000 | S3.1, S2.3 |
| S3.24 | Screen 22-measurement round 0 (parallel S3-phase-G) | opus | 20,000 | S3.1, S2.3 |
| S3.25 | Screen 23-team-ops round 0 (parallel S3-phase-G) | opus | 20,000 | S3.1, S2.3 |
| S3.26 | Screen 24-security round 0 (parallel S3-phase-G) | opus | 20,000 | S3.1, S2.3 |
| S3.27 | Screen 25-experiments round 0 (parallel S3-phase-H) | opus | 20,000 | S3.1, S2.3 |
| S3.28 | Screen 26-reports round 0 (parallel S3-phase-H) | opus | 20,000 | S3.1, S2.3 |
| S3.29 | Screen 27-wild-bets-pr round 0 (parallel S3-phase-H) | opus | 20,000 | S3.1, S2.3 |
| S3.R | Feature rounds: any screen, 10 candidates then one feature per commit | fable ranks, opus builds | 20,000 | S3.2 |
| S3.P | Publish and consistency review after each round | fable | 25,000 | S3.R |

Round 0 is the same for every screen: shell, api, 3 tiles, 2 insights as rules, 1 chart, and the audit stub. Kevin's order comes first (Today, brand brain, paid social, Google Ads), then phase order. Screens in one phase run in parallel. Feature rounds use S3.R and publish with S3.P.

## Stage 4: inspiration

| Id | Session | Model | Budget | Needs |
|---|---|---|---|---|
| S4.1 | Inspiration contract and registry | fable | 25,000 | S1.3m |
| S4.2a | Inspiration puller: Meta Ad Library puller and tagger (parallel S4.2) | sonnet | 15,000 | S4.1 |
| S4.2b | Inspiration puller: email archive puller (parallel S4.2) | sonnet | 15,000 | S4.1 |
| S4.2c | Inspiration puller: landing page capture and section tagger (parallel S4.2) | sonnet | 15,000 | S4.1 |
| S4.2d | Inspiration puller: creator and organic content puller (parallel S4.2) | sonnet | 15,000 | S4.1 |
| S4.3 | Inspiration block in the UI kit and 4 screens | opus | 25,000 | S4.2a |

## Stage 5: the loop

| Id | Session | Model | Budget | Needs |
|---|---|---|---|---|
| S5.1 | Findings aggregator and Propose ranker | opus | 25,000 | S3.2, S3.4, S3.5 |
| S5.2 | Context packages and the first domain agent (paid social) | fable for the package builder, opus for the agent | 30,000 | S5.1, S1.2b |
| S5.3 | QA gate, registry and read dates | opus | 25,000 | S5.2 |
| S5.4 | Orchestrator: daily run, queues, decision row wiring | opus | 30,000 | S5.3 |
| S5.5 | End to end demo on Bombas, published | fable | 30,000 | S5.4, S4.3 |

## Stage 6: hosted product

| Id | Session | Model | Budget | Needs |
|---|---|---|---|---|
| S6.1 | Store: files to a database behind the same API | opus | 30,000 | S5.5 |
| S6.2 | Auth and tenancy | opus | 30,000 | S6.1 |
| S6.3 | Worker, schedules and run log | opus | 25,000 | S6.1 |
| S6.4a | Connector live mode: Shopify (parallel S6.4) | opus | 20,000 | S6.2 |
| S6.4b | Connector live mode: Meta Marketing API (parallel S6.4) | opus | 20,000 | S6.2 |
| S6.4c | Connector live mode: Google Ads and GA4 (parallel S6.4) | opus | 20,000 | S6.2 |
| S6.4d | Connector live mode: Klaviyo (parallel S6.4) | opus | 20,000 | S6.2 |
| S6.4e | Connector live mode: Gorgias and reviews (parallel S6.4) | opus | 20,000 | S6.2 |
| S6.5 | Object storage for documents and assets | sonnet | 15,000 | S6.1 |
| S6.6 | Deploy: app, worker, database, bucket, logs | opus | 25,000 | S6.2, S6.3, S6.5 |
| S6.7 | Security review before the first real brand | fable | 40,000 | S6.6 |

## Stage 7: subscription variant

| Id | Session | Model | Budget | Needs |
|---|---|---|---|---|
| S7.1 | Subscription variant: what changes | fable | 40,000 | S5.5 |

## What a session looks like, start to end

```
python3 scripts/session.py S1.3a        # read the card
<paste the first line into a fresh session>
... the session reads its files, spawns a sub-agent for the web pass,
    writes records, runs python3 app/brain/validate.py on its folder ...
git add <its files> && git commit -m "<what and why>"
git pull --rebase origin claude/ecommerce-brand-website-dmq45j && git push
<update STATUS.md in the same commit>
/clear
```
