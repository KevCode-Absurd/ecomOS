# Brand brain v2: review of the skill and the design for ecomOS

Date: 28 Sep 2026. Status: design for Kevin's review (session S1.1). Input: Kevin's `brand-brain` skill (9 markdown files, 7 phases, 2 gates, living-system rules). Companion files: `app/brain/schema.json`, `app/brain/validate.py`, `app/brain/example/`.

## 1. What the skill does well

Keep these. They are the reason it works in a chat session.

- **Scrape first, ask later.** The site answers most questions. The user only fills gaps.
- **Two gates.** The user confirms the basics and gets a chance to add assets. Cheap insurance against building on a wrong scrape.
- **Connected sources before manual asks.** Meta, Klaviyo and Shopify are read before the user is asked to paste anything.
- **Product images pulled without asking.** `products.json` on Shopify is the right shortcut.
- **Grounding review.** Every avatar carries verbatim quotes or is labelled inferred. No invented quotes. This is the best rule in the file.
- **One diagnosis line.** Market awareness, the highest-intensity persona, the gap between who ads target and who buys.
- **A living system.** Write-back rules at session end. `recent-changes.md` as the freshness signal. Decisions logged so they are not re-argued.
- **No em dashes.** Same rule as ecomOS.

## 2. Where it falls short for what we are building

The skill is a chat workflow that writes prose files for one use: ads and creative. ecomOS needs a brain that serves 28 rooms, runs without a person in the loop, and stays fresh. The gaps, in order of cost:

1. **Prose, not records.** Facts sit inside paragraphs. No fact has its own source, date, confidence or tier. Nothing can be validated, diffed, expired or sliced. An agent must load a whole file to get one fact.
2. **Context bloat by design.** `brain.md` is an append-only log that "must not be trimmed". Nine files are "always load". After 6 months of use a session starts at 30k tokens before the task. The opposite of what Kevin wants.
3. **Ads-shaped.** The 9 files serve paid social and creative. Nothing for offer economics, shipping and returns policy, fulfilment, suppliers, marketplaces, finance targets, tracking, SEO facts, content series, team and approval chain, security, or experiments. 20 of the 28 rooms would find nothing they need.
4. **Chat gates block automation.** Gate 1 and Gate 2 need a person typing. A cloud service cannot wait in a chat. Gates must become items in a review queue that the founder clears from a screen, on their own time.
5. **Tool names are hard-wired.** `mcp__claude_ai_Meta_MCP__...` only exists inside one Claude client. A product needs connector adapters with a stable interface and mock mode.
6. **Local folders.** Images go to `Products/` on the user's disk. A product needs object storage, a manifest with rights and product ids, and per-brand tenancy.
7. **No calibration numbers.** The skill never records the numbers that make simulation and diagnosis possible: revenue band, AOV, repeat rate, channel mix, margins, targets. It also mixes what it does record (top campaigns, open rates) into prose where they go stale without a date.
8. **Personas fixed at 2 to 3, competitors from web search only.** Real brands have 4 to 8 buying situations, and the Ad Library, reviews and tickets are better competitor and avatar evidence than a search results page.
9. **Public and private mixed.** Site copy and the brand's own Meta numbers land in the same file. ecomOS keeps public research and private data apart.
10. **Refresh every 6 to 12 months.** Products change weekly, offers daily. Freshness has to be per section with its own clock.
11. **Winning ads from memory.** "Describe an ad you are proud of" is a fallback. Winners should come from the data layer with the metric, window and freshness attached.
12. **Claude-Code specific output.** `.claude/CLAUDE.md` is useful for a folder on a laptop. The product needs a context builder that any agent calls.

Everything in section 1 survives. Everything in section 2 is fixed by the design below.

## 3. Brain v2: records, not prose

The brain is a set of **records**. A record is one fact about one brand, in one section, with its provenance.

```json
{
  "id": "bombas.offers.free_shipping_threshold",
  "brand": "bombas",
  "section": "offers",
  "field": "free_shipping_threshold_usd",
  "value": 50,
  "text": "Free shipping on orders over $50.",
  "source": {"type": "site", "ref": "https://bombas.com/pages/shipping", "captured_at": "2026-09-28"},
  "confidence": 0.95,
  "tier": "site_backed",
  "status": "active",
  "visibility": "public",
  "valid_from": "2026-09-28",
  "expires_at": "2026-10-05",
  "evidence": [{"quote": "Free shipping on orders over $50", "ref": "https://bombas.com/pages/shipping"}],
  "history": []
}
```

Rules that hold for every record:

- `source.type` is one of `site`, `ad_library`, `connector`, `document`, `interview`, `press`, `review`, `ticket`, `founder`, `agent`, `inferred`. A summary is not a fact; `agent` and `inferred` records carry the record ids they were derived from.
- `tier` is one of `approved` (founder confirmed), `site_backed` (quoted from a live page), `reported` (press, interview, filing), `evidence` (reviews, tickets), `inferred` (a model's read, labelled), `forbidden` (founder said never, or unprovable). Claims copy can use only `approved` and `site_backed`.
- `visibility` is `public` or `private`. Private records come only from connected sources, uploads and the founder. A context package for public-facing work can exclude private records.
- `expires_at` comes from the section's TTL (section 4). An expired record is `stale`, still readable, flagged in every package that carries it.
- `history` keeps prior values with the date they changed. Nothing is deleted; `status` moves to `retired`.
- No em dash in any string. The validator rejects it.

Prose still exists, but as **derived summaries** (section 5), regenerated from records, never hand-edited.

## 4. Sections: what the brain holds across the 25 domains

One section per topic. Fields are typed. The rooms column comes from `agents/rooms/rooms.json` data needs. TTL is how long a record is trusted before the keeper re-checks it. Kevin's 9 files map onto these: brand-guidelines into `identity`, `voice`, `visual`, `claims`; products-and-positioning into `products`, `offers`, `positioning`; customer-avatars into `avatars`, `objections`, `language_bank`; competitors into `competitors`; brain.md into `decisions`, `learnings`, `open_questions`, `diagnosis`; recent-changes into `changes`; winning-ads into `learnings` with data-layer pointers.

| Section | Fields (examples) | Sources | Rooms that read it | TTL |
|---|---|---|---|---|
| `identity` | name, legal name, founded, founders, HQ, mission, one-line pitch, brand promise, category, certifications (B Corp), giving model, red lines | site, press, founder | all (in the card) | 180 d |
| `diagnosis` | awareness level, highest-intensity avatar, biggest gap, bottleneck stage, one-line diagnosis, dated | keeper from data and reviews | today, creative, copy, paid | 90 d |
| `story_bank` | origin beats, founder quotes with source, mission proof points (units given), press lines, milestones by year | interviews, podcasts, press | creative, copy, organic, PR | 90 d |
| `voice` | personality adjectives, writes-like analogy, do list, do-not list, tone by context, reading level, words used, words avoided, liked and disliked examples marked by founder | site copy, emails, ads, founder | copy, creative, email, CX, organic | 60 d |
| `visual` | palette with roles, type, photo style, people style, mood, do and do-not, logo rules, asset manifest pointer | site CSS, assets | creative, landing pages, organic | 90 d |
| `products` | lines, SKUs with price, cost tier, materials, sizes, packs, hero flag, launch date, status, PDP url, images manifest, restrictions | site crawl, feed, connector | offers, creative, copy, Google, marketplaces, supply, SEO | 7 d |
| `offers` | free shipping threshold, guarantee, discount policy, current promos with dates, bundles and pack ladder, loyalty, referral, gifting, BNPL, price integrity rules | site, emails, ad library, founder | offers, paid, email, CRO, copy, finance | 1 d |
| `policies` | shipping speed and carriers, returns window and cost, exchanges, warranty, privacy, consent, accessibility statement | site legal pages | CX, store health, copy, security | 30 d |
| `claims` | claim text, tier, evidence ref, category (material, benefit, comparison, guarantee), regions allowed, expiry | site, founder, legal | copy, creative, QA gate, marketplaces, answer engines | 30 d |
| `avatars` | name, share estimate, intensity, jobs, triggers, pains, emotional driver, channels, evidence quotes with refs, inferred flag | reviews, tickets, interviews, founder | creative, copy, paid, email, CX, research | 30 d |
| `objections` | objection text, avatar ids, proof that removes it, proof asset ref, coverage in ads and pages | reviews, tickets, founder | copy, CRO, creative, email | 30 d |
| `language_bank` | verbatim phrases by theme (problem, result, surprise, complaint), source, count | reviews, tickets, social | copy, creative, SEO, CRO | 30 d |
| `competitors` | competitor set, positioning, price band, what they do well, gap, ad library snapshot ref, price capture ref, launches | ad library, sites, search | competitors, creative, offers, research, Google | 14 d |
| `positioning` | category ladder, positioning statement, differentiators ranked, whitespace, messaging hierarchy, battlecards | keeper, founder | brand, copy, creative, competitors | 60 d |
| `channels` | channel, role (primary, second, test), what is public about it, owner, agency, platform account ids (private), status | interviews, connectors, founder | paid, Google, email, organic, affiliates, marketplaces | 30 d |
| `calendar` | seasonality peaks, promo calendar, launch dates, gifting windows, market holidays, blackout dates | site, emails, founder | today, offers, email, paid, supply, finance | 30 d |
| `economics` | pointer fields only: which finance inputs exist, targets (CAC, MER, margins, cover), public revenue band and its source | founder, press | finance, offers, paid, Google, today | 30 d |
| `operations` | fulfilment model, 3PL, warehouses, carriers, ship-in days, suppliers and countries, MOQ, lead times, peak plan | founder, site, documents | supply, CX, store health, finance | 30 d |
| `marketplaces` | which marketplaces, listing ids, buy box policy, MAP, retail partners, wholesale | site, connectors, press | marketplaces, Google, offers, affiliates | 14 d |
| `stack` | platform, theme, apps and scripts, ESP, support desk, reviews app, analytics, tag manager, connectors with access level and owner | crawl, connectors, founder | store health, speed, measurement, security, team | 14 d |
| `site_map` | page registry: url, type (home, collection, PDP, lander, legal, facts), owner, last change, speed run ref | crawl | CRO, speed, SEO, answer engines, copy | 7 d |
| `content` | series, formats, creators seeded, UGC rights, community spaces, posting floor | site, social, founder | organic, creative, PR | 30 d |
| `seo_facts` | target queries, question map, facts page contents, corrections issued, directories | GSC, crawl, keeper | SEO, answer engines, copy | 30 d |
| `team` | roles, people, agencies, who approves what, escalation, working hours, tools per role | founder | orchestrator, team ops, reports | 90 d |
| `decisions` | date, decision, reason, who, scope, parked items with reason and revisit date | founder, app | orchestrator, today, all rooms | none |
| `learnings` | what works, what to avoid, priors per idea (with registry pointer), winning ads with metric and window pointer | registry, data layer, founder | creative, paid, copy, email, experiments | 90 d |
| `open_questions` | question, section it would fill, why it matters, who can answer, asked on, answered on | keeper | today, brand brain screen, setup | none |
| `changes` | date, type, what changed, section and record ids, source | keeper diff | all (read first) | none |
| `freshness` | per section: last updated, record count, stale count, conflict count, confidence | keeper | brand brain screen, orchestrator | daily |

28 sections. The three that did not exist in the skill and matter most to the other rooms: `policies`, `operations` and `stack`. The three that keep the brain honest: `changes`, `open_questions`, `freshness`.

Subscription brands later add `plans` (plan ladder, skip and pause rules, dunning) as one more section, not a fork.

## 5. Context packaging: how we keep any agent's context small

The agent never opens the brain. A **package builder** in code assembles what one capability needs, inside a budget.

Four tiers, cheapest first:

| Tier | What | Size | When |
|---|---|---|---|
| T0 card | identity one-liner, diagnosis line, red lines, top 5 claims, current promos, freshness warnings | about 300 tokens | every agent, always |
| T1 summaries | one derived paragraph per section, regenerated when the section changes, with record count and freshness | about 120 tokens per section | the sections the capability names |
| T2 records | the records of a section, highest confidence first, active before stale | as budget allows | when the capability needs facts, not a gist |
| T3 evidence | quotes, source excerpts, asset refs | only on request | grounding, QA, claims checks |

How a package is built:

1. The capability record in `agents/catalogue.json` names `brain_sections` (with tier per section) and a `brain_budget` (default 4,000 tokens).
2. The builder adds T0, then T1 for each named section, then T2 records until the budget is spent, then stops. Private records are excluded when the capability is `public_facing`.
3. Every record in the package carries its date and tier, so the agent can quote "site-backed, 3 days old".
4. The package is cached by (brand, capability, brain version). The stable part (T0 plus T1) goes first in the prompt so prompt caching works.

Example: capability "write a paid social creative brief" gets T0, T1 for `products`, `offers`, `avatars`, `objections`, `voice`, `learnings`, `competitors`, and T2 records for `avatars` and `claims`. About 3,500 tokens. A 6-month-old brain costs the same as a 1-day-old one.

Summaries are written by a task agent (Haiku or Sonnet) on change, never by hand, and each cites the record ids it summarises so a wrong summary can be traced.

## 6. Ingestion: from sources to records

```
sources ──▶ extractors (one per source type, fixed output schema)
        ──▶ merge (dedupe by field, keep history, detect conflicts)
        ──▶ tiering (claims, confidence)
        ──▶ review queue (founder clears from the setup or brain screen)
        ──▶ publish version N (summaries regenerated, freshness updated, changes logged)
```

Extractors, each a small task agent or a script with the same output shape:

| Extractor | Reads | Writes to |
|---|---|---|
| site crawl and diff | sitemap, `products.json`, legal pages, CSS | products, offers, policies, claims, voice, visual, site_map, stack, changes |
| ad library | brand's own page and competitor pages | competitors, offers, learnings (public), story_bank |
| reviews and tickets | reviews app, marketplace reviews, support desk | avatars, objections, language_bank, products (issues) |
| connectors | Shopify, Meta, Google, GA4, Klaviyo, Gorgias, GSC, Amazon | channels, stack, products (hero flags, status), marketplaces, learnings (winners with metric pointers). Numbers themselves stay in the data layer. |
| documents | uploads, Drive folder, Notion, brand book, decks, research PDFs | any section, `source.type` document, page ref |
| interviews and press | transcripts, podcasts, articles, filings | story_bank, identity, channels, economics (public band) |
| founder answers | question rounds, chat, Slack channel | decisions, claims (approved), voice (liked and disliked), any section as `approved` |
| agent write-back | every agent run | proposed records into the review queue, never direct |

Merge rules: one active record per (section, field) unless the field is a list. The site wins over a document when they disagree, and a conflict record is raised. Founder wins over everything. Confidence is set by source type and agreement between sources.

Review queue rules: `identity`, `claims`, `red lines`, `decisions` and any `forbidden` change need the founder (gate). Everything else auto-publishes with a low-risk flag and shows in `changes` for 7 days so it can be reverted from the brain screen. This replaces Gate 1 and Gate 2 with something that works without a chat.

## 7. Keeping it fresh: the mechanism Kevin asked for

The founder enters the website, connects what they have, and the brain keeps improving from four clocks:

1. **Continuous.** Connectors sync daily. Facts that come from data (hero product, best flow, top ad) are recomputed from the data layer and the brain stores the pointer plus the date. The site is crawled daily and diffed; a changed price, a new product, a new promo, a removed page lands in `changes` and updates its section.
2. **Event driven.** A new document in the linked Drive folder or Slack channel triggers the document extractor. A new ad in the Ad Library triggers the ad extractor. A spike in one ticket reason triggers the objections extractor.
3. **Scheduled ask.** Every week (configurable to every 2 days), the keeper computes gaps: expired records, sections with low confidence, open conflicts, open questions, and the rooms that are blocked by them. It sends a short digest with 3 to 5 targeted questions and a place to attach files. Delivered to the app inbox and, where connected, Slack or email. Answers become `approved` records; attachments run through the document extractor. Never more than 5 questions; the rest wait.
4. **Session write-back.** Every agent run can call `propose_brain_update` with records it believes are new (a hook that worked, an objection that came up, a product that is out of stock). They go to the review queue, not to the brain. The founder sees "3 proposed updates" on the brain screen and clears them in a minute.

Health is visible: the brand brain screen shows per section freshness, confidence, stale count, conflicts, and what a connect or an answer would unlock. The weekly digest includes one line on brain health.

Versioning: each publish is a version with a diff. Any package names the version it was built from. Rollback is a version pointer.

## 8. Making it deployable in the cloud

The skill runs in one chat. The product runs as a service. Steps, in order:

1. **Split the skill into a package.** `app/brain/` with `schema.json`, `validate.py`, `store.py` (read and write records, versions), `extract/` (one module per extractor), `merge.py`, `package.py` (the context builder), `keeper.py` (the scheduler entry). No chat in any of them. Inputs are a brand id and a source; outputs are records.
2. **Replace gates with a review queue.** A `review` table with proposed records, risk level, and who cleared them. The setup screen and the brand brain screen read it. Nothing waits on a chat.
3. **Store.** SQLite per brand for the demo. Postgres with a `brand_id` on every row when hosted. Records, versions, summaries, review queue, changes. Assets in object storage (S3 or R2) with a manifest table: product id, role (packshot, lifestyle, UGC, ad), rights, source, hash.
4. **Connectors as adapters.** One class per platform with `pull(table, window)` and `status()`, a `mock` mode that returns the generated tables, a `live` mode that calls the API. OAuth apps for Shopify, Meta, Google, Klaviyo. Tokens in a secrets manager, read-only scopes, never in the repo.
5. **Jobs and schedules.** A worker process that runs crawls, extractors, syncs and the weekly ask. Cron or a queue (Cloud Run Jobs, Render cron, or a Python worker with Redis). Every job writes a run record with duration, rows and errors.
6. **Model calls server side.** Extractors call the Claude API with structured outputs for their fixed schema. Bulk runs (tagging thousands of reviews) go through the Batch API at half price. The T0 card and T1 summaries sit first in every prompt for prompt caching. Budget ledger enforced per brand per day.
7. **The brain API.** `GET /brain/<brand>/card`, `GET /brain/<brand>/sections/<name>`, `GET /brain/<brand>/package?capability=<id>`, `POST /brain/<brand>/records` (proposed), `POST /brain/<brand>/review/<id>`, `GET /brain/<brand>/health`, `GET /brain/<brand>/versions`. Agents and screens use only these.
8. **Auth and tenancy.** Login (magic link or an auth provider), brands per account, roles (founder, team, agency), every query scoped by brand id. Rate limits on crawling, respect robots.txt, per-brand data export and deletion.
9. **Hosting.** One app service (the existing `app/server.py` grown up, behind auth), one worker, one database, one bucket. Fly, Render or Cloud Run all fit. Logs and a health page.
10. **Migration path from the demo.** The Bombas brain is built as JSON files under `app/brain/bombas/` with this exact schema. The store module reads files now and a database later. Nothing above it changes.

## 9. What we build now for Bombas

Session S1.2 runs the extractors that need no private access: site crawl, Ad Library, reviews, interviews and press, job postings. Output: `app/brain/bombas/<section>.json`, `sources.json`, `assumptions.json`. Every record public. Kevin reviews from the files and, once the screen exists, from the brand brain screen.

Calibration fields that S1.2 must fill or mark open, because the generator needs them: revenue band and source, AOV estimate from the price ladder and pack sizes, repeat rate if stated anywhere, channel mix from interviews, seasonality from the promo history in emails and ads, giving units by year, retail partners.

## 10. Decisions for Kevin

1. The 28 sections in section 4: cut or add any before S1.2 runs.
2. Auto-publish low-risk changes with a 7-day revert window, versus gating everything. Recommendation: auto-publish.
3. The weekly ask: default weekly, 5 questions max, delivered in-app and to Slack when connected. Or every 2 days.
4. Whether agent write-back is on from day one (recommended, always through the review queue).
