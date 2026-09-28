# ecomOS product plan: general purpose, brand brain first

Date: 28 Sep 2026. Status: agreed direction from Kevin, written by Claude. This file replaces the brand-specific framing in older notes. Read it before `app/BUILD-PLAN.md`.

## 1. What we are building

ecomOS is a general-purpose operating system for any e-commerce store. It is not built for one client. Gehna was an example we tweaked things on. Tallgrass Goods was a fictional stand-in. Neither defines the product.

The product does 5 things for a store, in this order:

1. **Brand brain.** Everything known about the brand, structured so agents can read the slice they need.
2. **Data layer.** Every number from every connected platform, plus the numbers the brand supplies itself (costs, margins, targets).
3. **Screens.** One screen per domain (28 today), each running a deep audit and showing the metrics, insights and actions for that domain.
4. **Inspiration.** Per domain, the outside references that matter for this brand: ads, emails, pages, creators, competitors.
5. **The loop.** Audit everything, rank the top 10 actions, let the founder click, then an agent does it or a person gets the brief.

Scope rules:

- **Non-subscription stores first.** When the non-subscription product is complete, we read the codebase and decide what a subscription variant needs (payback, churn, cohort revenue curves, dunning). That will be a sibling product with shared code, not a fork of the screens.
- **The model brand is Bombas.** A real US brand (socks, underwear, tees, slippers; buy one, give one). We use only public information: the website, the Meta Ad Library, founder interviews and podcasts, press, reviews, job postings. Performance data is simulated and every page says so. We never reuse Bombas logos, copy or product photos.
- **Data is simulated now, real later.** The simulated tables are shaped by what each platform's API actually exposes. When a real store connects, the same tables fill from connectors and no screen changes.
- **Agents come after the brain and the data.** Small, domain-specific agents with a strict context package, not one large agent with everything loaded.

Everything under `app/` stays. The screen structure, the contracts, the UI kit, the server and the metric contract are the foundation. What changes is the sample brand profile and what fills it.

## 2. The shape of the product

```
founder enters website, connects sources, uploads brand documents
        │
        ▼
┌─────────────────────┐     ┌──────────────────────────────┐
│  BRAND BRAIN        │     │  DATA LAYER                  │
│  identity, voice    │     │  connector tables (Meta,     │
│  products, offers   │◀───▶│  Google, GA4, Shopify,       │
│  avatars, claims    │     │  Klaviyo, Gorgias, GSC ...)  │
│  competitors        │     │  brand-supplied inputs       │
│  decisions, history │     │  metric contract in code     │
└─────────┬───────────┘     └──────────────┬───────────────┘
          │        context packages by id  │
          ▼                                ▼
┌───────────────────────────────────────────────────────────┐
│  28 SCREENS, each with: audit.py, metrics, insights,      │
│  inspiration feed, action buttons with capability ids     │
└──────────────────────────┬────────────────────────────────┘
                           ▼
┌───────────────────────────────────────────────────────────┐
│  THE LOOP: audit all → rank top 10 → founder decides →    │
│  agent does it / person gets brief → registry → reads     │
└───────────────────────────────────────────────────────────┘
```

Every arrow is a file contract in `app/contracts/`. No screen reads another screen. No agent reads the whole brain.

## 3. Stage 1: the brand brain

### 3.1 What it is

A structured store of facts about one brand, with a source and a date on every fact. It is the single thing every agent reads before it works. It is written by ingestion (public sources, connected sources, uploaded documents) and by the founder (decisions, corrections, red lines). Kevin will supply an existing brand-brain skill file; session S1.1 refines it into the schema below.

### 3.2 Schema (sections, each a JSON file under `app/brain/<brand>/`)

Update 28 Sep 2026, session S1.1: the full design is `app/contracts/brand-brain.md` (28 sections, record shape, context packaging tiers, ingestion, the freshness mechanism, cloud deployment steps). The record schema is `app/brain/schema.json` with `app/brain/validate.py`. The table below is the first cut and the contract file wins where they differ.

| Section | Holds | Filled from | Read by |
|---|---|---|---|
| `identity` | name, founded, founders, HQ, mission, story, legal claims (B Corp etc), red lines | site, interviews, press | every agent, first 300 tokens |
| `products` | catalog: lines, SKUs, price ladder, materials, sizes, bundles, hero products, launch history | site crawl, feed | offers, creative, copy, Google, marketplaces |
| `offers` | shipping threshold, guarantee, discount policy, loyalty, gifting, bundles, current promos | site, emails, ad library | offers, paid, email, CRO |
| `voice` | tone rules, words used and avoided, reading level, example sentences, do and do not | site copy, emails, ads | copy, creative, email, CX |
| `avatars` | customer segments with evidence quotes, jobs, objections, triggers, channels | reviews, interviews, support themes | creative, copy, paid, email |
| `claims` | tiered: approved, site-backed, needs evidence, forbidden | site, legal pages, founder | copy, creative, QA gate |
| `competitors` | set of named competitors, what each is running, positioning map | ad library, sites | competitors, creative, offers |
| `channels` | which channels exist, their role, what is known about their performance publicly | interviews, press | paid, email, organic |
| `story_bank` | founder quotes, origin story beats, mission proof points, press lines | interviews, podcasts, press | creative, copy, PR |
| `market` | category, US defaults, marketplaces, seasonality, gifting calendar | public | every planner |
| `decisions` | founder decisions with reasons and dates, parked items | the app | orchestrator, propose |
| `open_questions` | what the brain does not know and who can answer | ingestion gaps | today screen, onboarding |
| `freshness` | per section: last updated, source count, confidence | ingestion | brand brain screen |

Rules: one fact per record, `source`, `captured_at`, `confidence`, `tier`. Public facts and private data never mix in one record. Nothing in the brain is a number computed from the data layer; the brain points at the metric name instead.

### 3.3 How agents access it

A **context package** is built in code, not by the agent: the sections the capability declares, filtered to the records with the highest confidence, capped at a token budget (default 4,000 tokens). `agents/catalogue.json` already names capabilities; S1.1 adds a `brain_sections` list to each capability record. The package also carries the metric contract answers the capability needs and a slice of the data layer. The agent never opens the brain folder itself.

### 3.4 Ingestion for Bombas (public only)

| Source | Method | Fills |
|---|---|---|
| bombas.com | crawl the sitemap: collections, PDPs, about, mission, FAQ, shipping, returns, size guides | products, offers, claims, voice, identity |
| Meta Ad Library | search by page name, pull running ads, dates, formats, copy | competitors (for Bombas itself as a reference), offers, voice, creative angles |
| Founder interviews and podcasts | transcripts where public, press features | story_bank, identity, channels, decisions history |
| Press and filings | funding, revenue reports, B Corp report, giving milestones | identity, market, calibration targets for the generator |
| Reviews | site reviews, retailer reviews, Reddit threads | avatars, objections, language bank |
| Job postings | roles hiring, tools named | channels, team shape, tool stack |
| Emails | public archives of brand emails | offers, voice, cadence |
| Kevin's documents | anything he uploads | any section, marked `founder_supplied` |

Each source is one sub-agent with one output file and a fixed schema. A merge step de-duplicates and tiers claims. Kevin reviews the brain before anything is built on it.

## 4. Stage 2: the data layer

### 4.1 Principle

Simulate what the platform can actually give us. Every table is shaped by the platform's API: its fields, its breakdowns, its limits, its retention. The generator writes rows a connector could have written. That is what makes the switch to live data a configuration change.

### 4.2 Connectors and what each exposes

This is the starter list. Session S2.1 reads each platform's official documentation and writes `app/contracts/connectors/<platform>.md` with the exact field names, breakdown rules, attribution options, rate limits and retention. The list below is from memory and is a guide to that work, not the result of it.

| Connector | Level and grain | Key fields (to confirm in S2.1) | Breakdowns | Notes |
|---|---|---|---|---|
| Meta Marketing API, insights | account, campaign, ad set, ad; daily | spend, impressions, reach, frequency, clicks, inline_link_clicks, cpm, cpc, ctr, actions and action_values (purchase, add_to_cart, initiate_checkout, view_content, landing_page_view), cost_per_action_type, purchase_roas, video_p25 to p100, thruplay | age, gender, country, region, publisher_platform, platform_position, device_platform | attribution windows 1d click, 7d click, 1d view. Some breakdown pairs not allowed. About 37 months of history. Read only. |
| Meta Marketing API, creatives | ad creative | body, title, call_to_action_type, image_hash, video_id, thumbnail_url, object_story_spec, asset_feed_spec (dynamic) | | flag dynamic and mixed creatives |
| Meta Ad Library | ad | page, start date, platforms, creative bodies, snapshot url | | competitor signals only. EU adds reach ranges. |
| Meta datasets and catalog | pixel, catalog | event counts, match quality, dataset stats, catalog diagnostics, product set counts | | setup health |
| Google Ads API | campaign, ad group, ad, keyword, search term, asset group; daily | impressions, clicks, cost, conversions, conversions_value, all_conversions, search_impression_share, top and absolute top share, budget_lost_impression_share, rank_lost_impression_share, quality score, ad strength | device, network, click type, geo, hour | PMax exposes asset groups and channel split with limited transparency. Search terms report has thresholds. |
| Google Merchant Center | product | approval status, disapproval reasons, item issues, price and availability | | feed quality |
| GA4 Data API | session and event; daily | sessions, totalUsers, newUsers, engagedSessions, engagementRate, addToCarts, checkouts, ecommercePurchases, purchaseRevenue, itemsViewed, itemsAddedToCart, transactions, cartToViewRate, purchaseToViewRate | date, sessionSource, sessionMedium, sessionCampaignName, sessionDefaultChannelGroup, landingPage, deviceCategory, country, region, newVsReturning, itemName | sampling and thresholding on small rows. Event retention 2 or 14 months. |
| Shopify Admin API (GraphQL) | order, line, customer, product, variant, inventory, fulfilment, return, dispute, payout | orders with line items, discounts, shipping, tax lines, refunds, source name, customer journey (utm, first and last visit), customers (orders count, amount spent, marketing consent), variants with unit cost, inventory levels, fulfilments and tracking, returns, disputes, payouts, abandoned checkouts | | unit cost per variant exists. Payments payouts and disputes need the payments scope. |
| Klaviyo API | profile, list, segment, flow, flow message, campaign, message, metric, event | sends, opens, clicks, unsubscribes, bounces, placed order attributed, metric aggregates by flow or message, revenue per recipient | by message, by day | Klaviyo's own attribution window (default 5 days). SMS in the same objects. |
| Gorgias API | ticket, message, customer, satisfaction | created, channel, via, status, tags, assignee, first response and resolution times from stats, CSAT | | tags are the reason taxonomy |
| Google Search Console | query, page; daily | clicks, impressions, ctr, position | country, device, search type | 16 months. Row limits per request. |
| Amazon SP-API and Ads API | order, ASIN, settlement, campaign, keyword | sales and traffic report (sessions, page views, buy box share, units, ordered product sales), FBA inventory, settlements, sponsored products spend, sales, ACoS | by ASIN, by day | no review API. Reviews stay a fixture. |
| Reviews (Judge.me, Yotpo, Okendo) | review | rating, body, product, created, verified | | quotable language for avatars |
| Page speed (own lab) | page, run | load, LCP, FCP, bytes, requests, filmstrip | device, variant | already built in `speed_lab` |
| Slack, email, Drive (founder inputs) | document, message | brand documents, decisions, plans | | writes to the brain, not the data layer |
| Later: TikTok Ads, Pinterest, Recharge or Skio (subscriptions), Walmart, Target Plus | | | | out of scope for the demo |

### 4.3 Brand-supplied numbers (the platforms do not have these)

A table `finance_inputs` that a brand fills in through a form or a sheet, with effective dates, so gross profit and contribution margin can be computed for any window:

- COGS per SKU (landed), packaging per order, shipping label cost per order by carrier and zone band, 3PL pick and pack fee, returns processing cost per return
- payment fees as a percent plus fixed, marketplace fees, app subscriptions, agency and tool fees monthly
- fixed costs monthly, headcount cost, cash balance, credit lines
- targets: target CAC, target MER, gross margin target, contribution margin target, inventory cover target
- monthly P&L actuals when available, to reconcile the computed numbers against

Metrics that become available once the brand supplies these: gross margin, gross profit per order, contribution margin per order and per channel, break-even ROAS, payback on first order, cash runway. The metric contract already marks `contribution_margin` and `cash_runway_weeks` as unavailable for this reason.

### 4.4 The simulation

- **Profile.** `app/brain/bombas/` gives the calibration targets: annual revenue band from public reports, average order value from the price ladder and pack sizes, repeat rate from what the brand says publicly, channel mix from interviews, seasonality (Q4 gifting, back to school, Prime-style events), giving milestones for the story. Where a number is not public, the generator states its assumption in `assumptions.json`.
- **Window.** 24 months of daily data ending on the last full day. Daily rows for every connector table. Order-level rows for cohorts, returns and CX.
- **Realism rules.** Weekly seasonality, holiday peaks, launch bumps, ad fatigue curves, creative rotation, brand versus non-brand search behaviour, email flows tied to actual orders, tickets tied to orders and shipments, returns in three legs (return, return to sender, chargeback) with cash on delivery legs null for a US brand, reviews with quotable language, stockouts that show up in sessions and search.
- **Scale.** A `scale` field in the profile. 1.0 means the public revenue band. 0.1 for fast local development. Order-level rows at full scale go into SQLite under `app/data/brands/bombas/`, regenerated by one command and not committed. Aggregates used by published pages are committed as JSON.
- **Consistency.** One truth: orders. Every other table derives from it (GA4 sessions imply orders, Meta purchases are a subset with attribution noise, Klaviyo attributed orders overlap, Shopify payouts sum the orders less fees). Attribution overlap is deliberate so the measurement screen has something to reconcile.
- **Review.** Session S2.5 produces a sanity report: ratios by month, channel shares, funnel rates, repeat curves, margin by channel, and Kevin reviews it before screens are built on it.

## 5. Stage 3: the interface

### 5.1 Onboarding flow (new screen `setup`)

1. Enter the website. The crawler fills the brain and shows what it found.
2. Upload brand documents (brand book, past decks, research). Each becomes brain records marked founder supplied.
3. Connect sources: Shopify, Meta, Google Ads, GA4, Klaviyo, Gorgias, Search Console, Amazon, reviews, Slack. In the demo each connector is in mock mode and shows what it would pull and what fields it exposes.
4. Fill brand-supplied numbers, or skip and see which metrics stay unavailable.
5. First audit runs. The Today screen shows the pipeline break and the top 10.

### 5.2 The 28 screens stay

The screen list in `app/screens/INDEX.md` stands. Each screen keeps its folder, its `CLAUDE.md`, its `FEATURES.md`, and its round structure. Two additions per screen:

- `audit.py`: a deep audit for that domain. It returns findings with severity, evidence rows, the metric or rule that fired, the capability id that fixes it, and the money at stake where computable. Findings feed the loop.
- an `inspiration` block that reads from the inspiration layer for that screen's domain.

### 5.3 Jobs to be done per channel

The screens are built around what a store wants from each channel, the jobs that get it there, who does them, the data each job needs, and how we help. Paid social and Google Ads first, since Kevin chose them. TikTok Ads comes later.

**Paid social (Meta). Goal: profitable new-customer acquisition at target CAC and MER, with retention spend kept efficient.**

| Job | Who does it today | Data needed | How ecomOS helps |
|---|---|---|---|
| Know where money goes and what it returns | media buyer | insights at ad level, daily, actions and values, MER from orders | pacing tile, spend vs plan, ROAS and CPA by campaign, ad set and ad, MER next to platform ROAS |
| Kill and scale | media buyer | 7d and 28d rows, frequency, CTR trend, purchases | ranked kill and scale list with the rule that fired and the dollars at stake |
| Find winning and losing creative | creative strategist | creatives joined to insights, tagged by angle, hook, format, avatar | creative leaderboard, fatigue alerts, winners by angle and avatar |
| Cover the creative map | creative strategist | brain avatars and angles, current ads tagged | coverage grid of avatars by angles by formats, gaps turned into briefs |
| Produce new creative | creative team, agency, UGC creators | brain voice, claims, winners, competitor signals, references | brief generator, script generator, static concepts, variant sets from a winner, claim check |
| Know which audiences and placements work | media buyer | breakdowns by age, gender, placement, geo, device | breakdown tables with significance flags, structure audit (consolidation, Advantage+ versus manual, exclusions) |
| Watch competitors | strategist | Ad Library by page, run length, formats | competitor board, long-running ads as signals, never copied |
| Keep setup healthy | technical marketer | pixel and dataset stats, event match quality, catalog diagnostics | setup audit with fixes |
| Match ad to page | media buyer and CRO | ad promise, landing page content, page speed | message-match audit, ad to page to checkout trace |
| Plan tests | strategist | registry of past tests, current spend | test plan with sample size and read dates, conflicts flagged |
| Report | account manager | everything above | weekly founder summary in plain words |

**Google Ads. Goal: capture existing demand profitably, protect the brand term, grow non-brand and shopping.**

| Job | Who does it today | Data needed | How ecomOS helps |
|---|---|---|---|
| Split brand and non-brand | search manager | campaign and keyword rows, search terms | brand versus non-brand efficiency, share of spend, incrementality flag on brand |
| Mine search terms | search manager | search term report with conversions | negatives to add, new keywords to add, themes rising |
| Keep the shopping feed healthy | feed manager | Merchant Center statuses and issues | disapprovals and title quality with fixes |
| Read PMax | search manager | asset groups, channel split, asset labels | asset group leaderboard, cannibalisation check against brand search |
| Win the auction where it matters | search manager | impression share, lost share by budget and rank, quality score | where budget is capping, where rank is losing, quality score fixes |
| Bid to the right target | search manager | conversion values, margins from finance inputs | tROAS and tCPA suggestions from contribution margin, not platform ROAS |
| Keep tracking right | technical marketer | conversion actions, GA4 reconciliation | conversion audit, value mismatch alerts |
| Match query to page | search and CRO | landing pages by query, GA4 funnel | landing page fit, speed by page |
| Report | account manager | everything above | weekly summary |

Shorter versions of the same table exist for the other channels and will live in each screen's `FEATURES.md`, seeded in round 0:

- **Email and SMS:** grow the list, keep deliverability, make flows earn revenue from orders, plan campaigns to the calendar, segment by avatar and lifecycle, test subject lines and offers.
- **Landing pages and CRO:** find the break in the funnel by device and source, run tests with a read date, keep message match, fix speed.
- **SEO and answer engines:** rank for the queries that convert, keep the crawl clean, refresh content that decays, make AI assistants describe the brand correctly.
- **Customers and CX:** know repeat, LTV and cohorts, know why tickets happen, cut returns and chargebacks, turn reviews into language.
- **Offers and pricing:** set the free shipping threshold, discount policy, bundles and guarantees from margin, not habit.
- **Supply, marketplaces, finance, measurement, security, team:** the operations screens keep their room specs.

### 5.4 Build order for screens

Phase order stays as in `app/BUILD-PLAN.md`. Setup runs first. Then Today, then the brand brain screen, then paid social and Google Ads, since those are the chosen focus, then the rest in phase order. Round 0 for a screen adds the audit stub. Screens in different phases run in parallel sessions.

## 6. Stage 4: the inspiration layer

Per domain, a registry of outside sources, a puller with a fixture mode, and a relevance scorer that reads the brain.

| Domain | Sources | What we keep | Relevance signal |
|---|---|---|---|
| Creative and paid social | Meta Ad Library (competitors and category leaders), public swipe files, creator content | layout, format, hook type, run length | same category, same avatar, same offer type |
| Email | public email archives, competitor sign-ups | cadence, structure, offer pattern, subject patterns | same price band, same gifting calendar |
| Landing pages | competitor PDPs and landers, page galleries | section order, proof types, offer placement | same product type |
| Organic and content | creator and brand posts with public metrics | format, hook, series | same audience |
| Offers | competitor promos over time | thresholds, bundle math, guarantee wording | same margin band |
| Product and research | reviews, Reddit, search demand | unmet needs, language | same category |

Rules: references are signals, not proven winners. Layout and mood only. Never copy text, logos, products or faces. Each reference carries the reason it is relevant to this brand, produced in code from brain fields. Video and image generation ("make me a version of this in our brand") plugs in here later as one-click workflows.

## 7. Stage 5: the loop

1. **Audit.** Every screen's `audit.py` runs on a schedule. Findings land in `data/<brand>/findings.json` with severity, evidence, money at stake, capability id, autonomy.
2. **Propose.** A ranker (code first, model second) turns findings into the top 10 for the Today screen: highest money at stake, highest confidence, lowest effort, no conflict with a running test.
3. **Decide.** The founder presses one of 3 buttons: let the agent do it, send to a person, not now. Every press is logged with a reason.
4. **Dispatch.** "Agent" builds a context package and runs the owning domain agent, which may spawn task agents. "Person" generates a brief and queues it. Output goes through a QA gate (claims, voice, numbers) before delivery.
5. **Register and read.** The experiment registry records what was done, the metric to watch, and the read date. The result flows back into the brain (decisions, learnings) and into the next audit.

Until connectors are live and Kevin approves execution, "agent does it" produces the artefact (the copy, the change list, the brief, the creative set) and stops. No external writes. Meta stays read only.

## 8. Agents: small, domain specific, recursive

### 8.1 Three tiers

| Tier | Count | Job | Context | Model |
|---|---|---|---|---|
| Orchestrator | 1 per brand | routes, schedules, keeps queues, talks to the founder. Owns nothing a specialist can do. | brain identity, registry, metric headlines. Under 8k tokens. | top model for founder chat and routing judgement |
| Domain agents | 1 per screen (28) | plan work inside one domain, pick task agents, assemble the result | context package for the domain: brain sections by id, metric answers, data slice, inspiration refs, idea records. 15 to 40k tokens. | Opus by default, Fable when the task is judgement heavy (strategy, ranking, review) |
| Task agents | many, tiny | one job with a strict input and output schema: tag an ad by angle, write 5 hooks, extract claims from a page, score a landing page, classify a ticket reason | only its inputs. Under 5k tokens. | Sonnet for writing and extraction at volume, Haiku for classification and tagging |

Recursion is allowed: a task agent may spawn task agents. Depth limit 3, a token budget per dispatch, and every spawn is logged. Nothing recursive runs without a parent that owns the result.

### 8.2 What every agent gets and never gets

Gets: its context package, the metric contract answers it asked for (values, windows, freshness, formulas), the tools it declared. Tools are read brain, read metrics, query tables, search ideas, search knowledge cards, ad library search, write draft, write registry.

Never gets: the whole brain, another domain's data, raw credentials, a connector write, arithmetic to do in its head (numbers are computed in code and quoted with their window).

### 8.3 Where the shelf comes in

`agents/catalogue.json` (560 capabilities), `agents/workflows/` (235 workflows), `agents/skills/` (the skill tree) and `ideas/v1/` (4,650 ideas) are the spec shelf. A domain agent's prompt is assembled from the slice of the shelf its capability ids name. No agent loads a playbook. The two blind tests in `reviews/` showed loaded playbooks did not help.

### 8.4 Runtime models (for the product itself, not for build sessions)

Cached pricing from the Claude API skill, June 2026, per million tokens:

| Model | Input | Output | Use in ecomOS |
|---|---|---|---|
| Claude Opus 5 (`claude-opus-5`) | $5 | $25 | default for domain agents and QA gate |
| Claude Sonnet 5 (`claude-sonnet-5`) | $2 | $10 | task agents that write or extract at volume |
| Claude Haiku 4.5 (`claude-haiku-4-5`) | $1 | $5 | tagging, classification, routing inside pipelines |
| Claude Fable 5.1 (`claude-fable-5-1`) | $10 | $50 | founder chat and strategy ranking where judgement matters most |

Prompt caching on the stable prefix (brain identity, tool list, contract) cuts repeated cost. Batch API for nightly audits and tagging runs at half price. Budget ledger in `intelligence/budget.py` stays the spend control.

## 9. Sessions: how we build this without burning tokens

Update 28 Sep 2026: the session cards, budgets and rules now live in `sessions/SESSIONS.md` and `sessions/sessions.json`, printed by `scripts/session.py <id>`. The tables below are the first cut; the sessions folder wins where they differ.

One session per numbered item. Each session starts fresh, reads only what its line names, commits after each deliverable, and pushes. `/clear` between items. Memory is the file it writes and the git log, never the transcript.

### Session models

| Work | Model | Why |
|---|---|---|
| Schema, contracts, plans, reviews | Fable | everything downstream depends on getting these right |
| Building a feature, a generator, an audit | Opus | strong build quality, lower cost than Fable |
| Bulk mechanical work: field census from docs, fixtures, tagging, per-platform tables | Sonnet | many similar small sessions, run in parallel |
| Ranking 10 candidates in a feature round | Fable | judgement, reads the spec, argues the order |

### Stage 1 sessions: brand brain

| # | Session | Model | Reads | Writes | Done when |
|---|---|---|---|---|---|
| S1.1 | Brain schema | Fable | Kevin's brain skill file, `agents/loop/BRAIN-KEEPER.md`, `app/screens/05-brand-brain/`, section 3 here | `app/contracts/brand-brain.md`, `app/brain/schema.json`, `brain_sections` on each capability | done 28 Sep 2026 except `brain_sections` on capabilities, which moves to S1.2. A validator passes an example brain and rejects a record without source or date |
| S1.2 | Bombas public ingestion | Opus, with web, one sub-agent per source | section 3.4, the schema | `app/brain/bombas/*.json`, `sources.json`, `assumptions.json` | every record has a source url and a date; the merge report lists conflicts |
| S1.3 | Brain review | Fable, then Kevin | the brain | `open_questions.json`, corrections | Kevin signs off the identity, products, offers, avatars and claims sections |

### Stage 2 sessions: data layer

| # | Session | Model | Reads | Writes | Done when |
|---|---|---|---|---|---|
| S2.1a to S2.1j | Field census, one per platform (Meta insights and creatives, Meta Ad Library and datasets, Google Ads, Merchant Center, GA4, Shopify, Klaviyo, Gorgias, Search Console, Amazon) | Sonnet, web, in parallel | the platform's official API docs | `app/contracts/connectors/<platform>.md` | fields, grain, breakdowns, attribution, limits, retention, and a sample row are all present |
| S2.2 | Data sources v2 | Fable | the 10 census files, `contracts/data-sources.md`, `agents/DATA-LAYER.md` | `contracts/data-sources.md` v2, `finance_inputs` table spec, calibration target list | every table names the census field it maps to |
| S2.3 | Generator v2 | Opus | v2 contract, `app/brain/bombas/`, `app/data/generate.py` | `app/data/generate.py` v2, `app/data/brands/bombas/`, `assumptions.json` | 24 months daily, deterministic, SQLite at scale 1.0, JSON aggregates, orders are the one truth |
| S2.4 | Brand-supplied inputs | Opus | `finance_inputs` spec, `app/metrics.py` | the table, the entry form in `setup`, margin metrics in `metrics.py` | contribution margin answers once inputs exist and reads unavailable before |
| S2.5 | Data review | Fable, then Kevin | the generated data | `app/data/brands/bombas/REVIEW.md` with charts | Kevin agrees the numbers look like a brand of this size |

### Stage 3 sessions: interface

| # | Session | Model | Notes |
|---|---|---|---|
| S3.0 | `setup` screen round 0 | Opus | website, documents, connectors in mock mode, finance inputs, first audit |
| S3.1 | Audit contract | Fable | `contracts/audit.md`: finding schema, severity scale, money at stake rule, `audit.py` interface |
| S3.2 | Today round 0 on Bombas data | Opus | pipeline break, top 10 from findings, decision row |
| S3.3 | Brand brain screen round 0 | Opus | the brain browsable, freshness, open questions, corrections |
| S3.4, S3.5 | Paid social and Google Ads round 0, then rounds of 10 | Opus builds, Fable ranks | the JTBD tables in 5.3 seed `FEATURES.md` |
| S3.6 on | Remaining screens in phase order, parallel worktrees | Opus builds, Fable ranks | contract changes are their own short Fable session first |

### Stage 4 and 5 sessions

| # | Session | Model | Notes |
|---|---|---|---|
| S4.1 | Inspiration contract and registry | Fable | sources, fixture mode, relevance rule per domain |
| S4.2 to S4.x | One puller per source with fixtures | Sonnet | Ad Library first, then emails, then pages |
| S5.1 | Findings aggregator and Propose ranker | Opus | code ranking first, model tie-break second |
| S5.2 | Dispatch: context packages and the first domain agent (paid social) | Fable for the package builder, Opus for the agent | outputs an artefact, no external writes |
| S5.3 | QA gate and registry | Opus | claims, voice, numbers; read dates |
| S5.4 | End to end demo on Bombas | Fable | audit to top 10 to click to artefact, published as a page |

### Stage 6, later: subscription variant

After stage 5 is demoed, one Fable session reads the codebase and writes `SUBSCRIPTION-VARIANT.md`: which metrics change (payback, churn, cohort revenue curves, dunning, skip and pause rates), which connectors join (Recharge, Skio), which screens change, and what shares. A second profile in the generator, not a fork.

## 10. Repo layout after this plan

```
app/
  brain/               the brand brain: schema.json, <brand>/ sections, validator
  contracts/           metrics, data-sources v2, connectors/<platform>.md, brand-brain, audit, events, ui-kit
  connectors/          read-only adapters, mock and live
  data/                generate.py, brands/<brand>/ (SQLite not committed, aggregates committed), tables.py
  inspiration/         registry, pullers, fixtures, relevance
  loop/                findings aggregator, propose, dispatch, qa gate, registry
  screens/             setup + the 28 screens, each with audit.py
  server.py, metrics.py, web/
agents/                the spec shelf, read by id
ideas/                 the idea bank, read by filter
intelligence/          knowledge search, creative retrieval, budget ledger
```

## 11. Decisions Kevin has made and decisions still open

Made:

- General purpose for any e-commerce store. Non-subscription first.
- Bombas as the model brand, public information only, simulated performance data.
- Brand brain first, then data layer, then interface, then inspiration, then the loop.
- Meta and Google Ads are the first channels. TikTok later.
- Simulated data shaped by each platform's API documentation, 1 to 2 years daily (this plan says 24 months).
- Small domain-specific agents with an orchestrator, recursion allowed.
- Multiple short sessions, model chosen per task.

Open (with the recommendation in this plan):

1. Full-scale simulation in SQLite, not committed, versus a scaled-down JSON set. Recommendation: full scale in SQLite with a `scale` switch.
2. Where the founder-facing app will be hosted and how auth works. Not needed for the demo. Decide before any real brand connects.
3. Which of Kevin's existing skills become the brain schema. Kevin will supply the file in S1.1.
4. Whether the `setup` screen is numbered `00` and Today moves to `01`, or `setup` stays unnumbered as the entry point. Recommendation: unnumbered.

## 12. Next step

S1.1, brand schema, as soon as Kevin shares the brain skill file. First line for that session:

`Work in app/. Session S1.1 per PRODUCT-PLAN.md section 3 and 9: turn the supplied brain skill into app/contracts/brand-brain.md and app/brain/schema.json with a validator.`

While waiting, S2.1 (field census, 10 parallel Sonnet sessions) can start today, because it depends on nothing but the platforms' public documentation.
