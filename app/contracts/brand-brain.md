# Brand brain v2: review of the skill and the design for ecomOS

Date: 28 Sep 2026. Status: design for Kevin's review (session S1.1). Input: Kevin's `brand-brain` skill (9 markdown files, 7 phases, 2 gates, living-system rules). Companion files: `app/brain/schema.json` (records), `app/brain/documents.schema.json` (upload manifest), `app/brain/sources.registry.json` (every source and what it fills), `app/brain/questions.bank.json` (what we ask and when), `app/brain/validate.py`, `app/brain/example/`.

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
5. **Three integrations, hard-wired.** Meta, Klaviyo and Shopify by tool name. A brand may run on WooCommerce, Mailchimp, Zendesk, Yotpo and QuickBooks. A product needs a source registry and connector adapters with a stable interface and mock mode, and its questions must be computed from what the connected sources could not answer.
6. **Local folders.** Images go to `Products/` on the user's disk. A product needs object storage, a manifest with rights and product ids, and per-brand tenancy.
7. **No calibration numbers.** The skill never records the numbers that make simulation and diagnosis possible: revenue band, AOV, repeat rate, channel mix, margins, targets. It also mixes what it does record (top campaigns, open rates) into prose where they go stale without a date.
8. **Personas fixed at 2 to 3, competitors from web search only.** Real brands have 4 to 8 buying situations, and the Ad Library, reviews and tickets are better competitor and avatar evidence than a search results page.
9. **Public and private mixed.** Site copy and the brand's own Meta numbers land in the same file. ecomOS keeps public research and private data apart.
10. **Refresh every 6 to 12 months.** Products change weekly, offers daily. Freshness has to be per section with its own clock.
11. **Winning ads from memory.** "Describe an ad you are proud of" is a fallback. Winners should come from the data layer with the metric, window and freshness attached.
12. **Claude-Code specific output.** `.claude/CLAUDE.md` is useful for a folder on a laptop. The product needs a context builder that any agent calls.

Everything in section 1 survives. Everything in section 2 is fixed by the design below.

## 3. Brain v2: records and documents

Kevin's rule (28 Sep 2026): provenance is welcome, never required. A founder must be able to drop in anything they think matters without filling a form. So the brain holds two kinds of content, and tells them apart.

### 3.1 Records: structured facts, provenance when it exists

A record is one fact about one brand in one section. Only `id`, `brand`, `section` and a `value` or `text` are required. Everything else is optional and used when present.

```json
{
  "id": "bombas.offers.free_shipping_threshold_usd",
  "brand": "bombas",
  "section": "offers",
  "field": "free_shipping_threshold_usd",
  "value": 50,
  "text": "Free shipping on orders over $50.",
  "source": {"type": "site", "ref": "https://bombas.com/pages/shipping", "captured_at": "2026-09-28"},
  "confidence": 0.95,
  "tier": "site_backed",
  "expires_at": "2026-10-05",
  "evidence": [{"quote": "Free shipping on orders over $50", "ref": "https://bombas.com/pages/shipping"}]
}
```

A founder's quick note is also a valid record:

```json
{"id": "bombas.learnings.note_2026_09_28_1", "brand": "bombas", "section": "learnings",
 "text": "Founder-face videos beat product-only statics for us in Q2. Do not know why yet."}
```

Rules:

- **What is required:** `id`, `brand`, `section`, and `value` or `text`. Nothing else.
- **What is used when present:** `source` (type, ref, captured_at), `confidence`, `tier`, `evidence`, `expires_at`, `visibility`, `history`. A record without a source gets `tier: unverified` and `confidence: null`. It is still read; the package shows it as "unverified, added by founder on <date>".
- **Where the line matters:** claims used in customer-facing copy must be `approved` or `site_backed`. Everything else can be unverified. The QA gate enforces this in one place, so the rest of the brain stays free.
- **Tiers:** `approved` (founder confirmed), `site_backed` (quoted from a live page), `reported` (press, interview, filing), `evidence` (reviews, tickets), `inferred` (a model's read, labelled), `unverified` (no source given), `forbidden` (founder said never).
- **Visibility:** `public` or `private`. Defaults to `private` for anything the founder adds and `public` for anything from a public source. Public-facing packages can exclude private records.
- **History:** a changed value keeps its prior values. Nothing is deleted; `status` moves to `retired`.
- **No em dash** in any string. The validator rejects it.

### 3.2 Documents: unstructured uploads, kept as they are

Anything the founder or team drops in: a brand book, a deck, a research PDF, a Loom transcript, a spreadsheet of past tests, a screenshot, a Slack export, a note. Stored as the file it is under `app/brain/<brand>/documents/` with one manifest line:

```json
{"file": "documents/2026-09-28-brand-book-v3.pdf", "added_at": "2026-09-28", "added_by": "kevin",
 "note": "current brand book, supersedes v2", "sections": ["voice", "visual"], "extracted": false}
```

Only `file` and `added_at` are required. `note`, `sections`, `tags`, `added_by`, `supersedes` are optional. Documents are not validated for content. They are indexed for search (keyword now, embeddings later through `intelligence/knowledge_search.py`) so an agent can pull the right page as T3 evidence. Extraction into records is optional, asynchronous, and proposed through the review queue; a document never has to be extracted to be useful.

Prose summaries still exist, but as **derived summaries** (section 5), regenerated from records and documents, never hand-edited.

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
| `objection_ladders` | one ladder per theme: rungs from mild doubt to deal-breaker, 1-star complaint language and 5-star praise language per rung, counts by star and source, proof that resolves each rung, avatar ids, uses (offer, copy, PDP, Amazon listing, CX) | derived from own-site, Amazon and retailer reviews, tickets | copy, offers, creative, marketplaces, CX, brand | 30 d |
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

### 5.1 The brand context file: `BRAIN.md`, a router not a store

Each brand gets one small markdown file, `app/brain/<brand>/BRAIN.md`, the way a `CLAUDE.md` works for a repo. It is what a person or an agent reads first. It holds under about 1,500 tokens and links out for everything else:

1. The T0 card: who the brand is, the diagnosis line, red lines, current promos, freshness warnings.
2. A section index: each of the 28 sections with record count, last update and one line, linking to its file.
3. A routing table: for this kind of work, read this. Example rows: "writing ad copy: `claims`, `voice`, `avatars`, then skill `agents/skills/CREA/ad-copy/SKILL.md`"; "pricing a promo: `offers`, `economics`, then `finance_inputs` in the data layer and capability MONEY-C04"; "anything numeric: the metric contract at `/api/metrics`, never this file".
4. A founder notes block: free text the founder edits by hand. Regeneration preserves it word for word.
5. Links to the documents manifest and the open questions.

It is regenerated from the records on every publish. It copies nothing from skills, agent files or the data layer; it names them by path or id. An agent that needs to execute something follows the link and loads only that skill. This is how one file gives full brand context without holding everything.

Adding context is one action from anywhere: paste a note, upload a file, answer a question, forward an email, drop a file in the linked Drive folder or Slack channel. Each becomes a record or a document, and `BRAIN.md` updates on the next publish.

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
| own-site reviews | the brand's review widget pages or JSON | avatars, objections, language_bank, products (issues). Default for every brand. |
| Amazon listings and reviews | listing pages for the brand's ASINs (public, small sample), the brand's Seller Central reviews export (document), a licensed provider (paid, optional) | marketplaces (listing content, rating split, review count), products, objections, language_bank. Default for every brand on Amazon. No review API exists and bulk scraping is against Amazon's terms, so the public lane stays a sample. |
| retailer reviews and tickets | retailer product pages, Reddit, Trustpilot, support desk | avatars, objections, language_bank, products (issues) |
| objection ladders | every review and ticket record in the brain | `objection_ladders`, derived; rebuilt when reviews change |
| connectors | Shopify, Meta, Google, GA4, Klaviyo, Gorgias, GSC, Amazon | channels, stack, products (hero flags, status), marketplaces, learnings (winners with metric pointers). Numbers themselves stay in the data layer. |
| documents | uploads, Drive folder, Notion, brand book, decks, research PDFs | any section, `source.type` document, page ref |
| interviews and press | transcripts, podcasts, articles, filings | story_bank, identity, channels, economics (public band) |
| founder answers | question rounds, chat, Slack channel | decisions, claims (approved), voice (liked and disliked), any section as `approved` |
| agent write-back | every agent run | proposed records into the review queue, never direct |

Merge rules: one active record per (section, field) unless the field is a list. The site wins over a document when they disagree, and a conflict record is raised. Founder wins over everything. Confidence is set by source type and agreement between sources.

Review queue rules: `identity`, `claims`, `red lines`, `decisions` and any `forbidden` change need the founder (gate). Everything else auto-publishes with a low-risk flag and shows in `changes` for 7 days so it can be reverted from the brain screen. This replaces Gate 1 and Gate 2 with something that works without a chat.

### 6.1 Sources: a registry, not three integrations

The skill knows 3 integrations. A brand may run on any of 60. `app/brain/sources.registry.json` lists every source the brain and the data layer can pull from, grouped by category, with the sections and tables each one fills, its access type and whether a mock exists. Categories today: public (site crawl, Ad Library, press, public reviews, job postings), store (Shopify, WooCommerce on WordPress, BigCommerce, Adobe Commerce, custom export), ads (Meta, Google, Merchant Center, TikTok, Pinterest, Amazon Ads), analytics (GA4, Search Console, Bing, Tag Manager, Clarity or Hotjar), email and SMS (Klaviyo, Mailchimp, Omnisend, Brevo, Attentive, Postscript, Customer.io), support (Gorgias, Zendesk, Freshdesk, Intercom, Help Scout), reviews (Judge.me, Yotpo, Okendo, Stamped, Trustpilot, Loox), SEO tools (Ahrefs, Semrush, Screaming Frog), marketplaces (Amazon, Walmart, TikTok Shop), payments (Stripe, PayPal, Shopify Payments), finance (QuickBooks, Xero, brand-supplied numbers), fulfilment (ShipStation, ShipBob, ShipHero, EasyPost, supplier sheet), subscriptions (Recharge, Skio, Loop; later), affiliates and creators (Impact, ShareASale, Refersion, GRIN), social organic (Instagram, TikTok, YouTube, Pinterest), documents (Drive, Notion, Dropbox, Slack, email forwarding, upload), WordPress content, and our own probes (speed lab, answer engine probe).

Rules:

- A source is never required. A brand connects at most one per category, or none. Declining a source is a recorded choice, not an error.
- Adding a source is one registry entry plus one adapter with `pull(table, window)` and `status()` and a mock. Nothing else changes: the sections and tables it fills already exist.
- Public sources run for every brand on day one. Private sources run only after the founder connects them.
- The setup screen shows the categories, what each would unlock (sections and rooms), and lets the founder connect, skip, or mark "not comfortable connecting".

### 6.2 Objection ladders: what 5-star and 1-star reviews become

Reviews are read at both ends first. 5-star reviews say what the product does well in the buyer's words. 1-star reviews say what breaks, what disappointed, and what the buyer expected. The ladder builder groups both by theme and writes one record per theme into `objection_ladders`:

```json
{"id": "bombas.objection_ladders.durability", "brand": "bombas", "section": "objection_ladders", "field": "ladder",
 "value": {"theme": "durability",
   "rungs": [
     {"level": 1, "doubt": "will they pill or thin out", "one_star": ["worn out after 3 months"], "five_star": ["two years and still no holes"],
      "counts": {"one_star": 14, "five_star": 22, "sources": {"amazon": 20, "own_site": 9, "trustpilot": 7}},
      "proof": "Happiness Guarantee replaces any pair that fails; state it next to the price", "avatars": ["durability_disappointed_repeat"],
      "uses": ["pdp", "amazon_listing", "copy", "cx_macro"]},
     {"level": 3, "doubt": "hole in the heel within weeks", "one_star": ["hole in the heel after 2 wears"], "five_star": [],
      "counts": {"one_star": 31, "five_star": 0}, "proof": "no public proof; open question for the founder", "uses": ["offer", "product"]}
   ],
   "what_works": ["cushioning", "stay-up", "gift reaction"], "what_fails": ["heel holes", "no-show slipping", "size chart"]},
 "text": "Durability is the top objection: 31 one-star reviews name heel holes; the guarantee answers the mild rung but not the deal-breaker.",
 "source": {"type": "agent", "ref": "ladder builder", "captured_at": "2026-09-28", "derived_from": ["bombas.objections.hole_recourse", "..."]},
 "tier": "inferred", "confidence": 0.7, "visibility": "public"}
```

Rules: rungs run from mild doubt to deal-breaker; every rung cites the record ids its quotes come from; counts are by star and by source so a Trustpilot skew is visible; a rung with no proof becomes an open question; every ladder names its uses so the offers, copy, marketplaces and CX rooms pick it up by section, not by reading reviews again. Ladders feed three rooms directly: avatars (each rung names its avatar), offers (a deal-breaker with no proof is an offer or guarantee problem), and copy and the Amazon listing (5-star language is the copy bank, 1-star language is what the listing must answer in the first 3 bullets). They are rebuilt whenever a review source changes.

## 7. Keeping it fresh: the mechanism Kevin asked for

The founder enters the website, connects what they have, and the brain keeps improving from five clocks:

1. **Continuous.** Connectors sync daily. Facts that come from data (hero product, best flow, top ad) are recomputed from the data layer and the brain stores the pointer plus the date. The site is crawled daily and diffed; a changed price, a new product, a new promo, a removed page lands in `changes` and updates its section.
2. **Event driven.** A new document in the linked Drive folder or Slack channel triggers the document extractor. A new ad in the Ad Library triggers the ad extractor. A spike in one ticket reason triggers the objections extractor.
3. **Scheduled ask: pull first, then ask only what matters.** Every week (configurable to every 2 days) the keeper runs in this order:
   1. Pull every connected source and run every public source. Fill what can be filled. Nothing is asked that a connected source already answered.
   2. Compute what is still missing: expired records, empty fields a room needs, open conflicts, low-confidence records.
   3. For each gap, look up `app/brain/questions.bank.json`. Each question names the fields it fills, the sources that could answer it instead, the rooms it unblocks and a weight. Importance is weight times the number of blocked rooms, times money at stake where the metric contract can compute it.
   4. Drop any question a connected source can answer. For a question a not-yet-connected source could answer, the ask becomes "connect X, or answer this in a line" with the reason. For a source the founder marked as not comfortable connecting, the question is asked plainly and never nags about the source again.
   5. Send the top 5 by importance, with a place to attach files. Never more. The rest wait for the next round or drop when a source fills them.
   
   Answers become records (founder-added, so `approved` where it is a claim or decision). Attachments run through the document extractor. The digest is delivered to the app inbox and, where connected, Slack or email. The bank starts with 18 questions and grows: a room that finds a gap it cannot fill adds a question with its fields and its weight, in a contract session.

4. **Session write-back.** Every agent run can call `propose_brain_update` with records it believes are new (a hook that worked, an objection that came up, a product that is out of stock). They go to the review queue, not to the brain. The founder sees "3 proposed updates" on the brain screen and clears them in a minute.

5. **Weekly audit of the brain and what it links to.** Alongside the questions, a job reviews the brain itself and proposes improvements into the review queue: stale or contradicting records, sections with nothing in them that a room needs, documents added but never read or extracted, summaries that drifted from their records, routing rows that point at a missing file, skills and agent files the routing table links to that overlap, are never used, or reference facts the brain now contradicts, and records that could be merged. Each proposal shows the before and after. The founder accepts or ignores them from the brain screen. Accepted skill changes become a commit in `agents/skills/`. The audit is how the brain, and the skills around it, get better without a person rereading everything.

Health is visible: the brand brain screen shows per section freshness, confidence, stale count, conflicts, and what a connect or an answer would unlock. The weekly digest includes one line on brain health.

Versioning: each publish is a version with a diff. Any package names the version it was built from. Rollback is a version pointer.

## 8. Making it deployable in the cloud

The skill runs in one chat. The product runs as a service. Steps, in order:

1. **Split the skill into a package.** `app/brain/` with `schema.json`, `validate.py`, `store.py` (read and write records, versions), `extract/` (one module per extractor), `merge.py`, `package.py` (the context builder), `router.py` (writes `BRAIN.md`), `audit.py` (the weekly audit), `keeper.py` (the scheduler entry). No chat in any of them. Inputs are a brand id and a source; outputs are records.
2. **Replace gates with a review queue.** A `review` table with proposed records, risk level, and who cleared them. The setup screen and the brand brain screen read it. Nothing waits on a chat.
3. **Store.** SQLite per brand for the demo. Postgres with a `brand_id` on every row when hosted. Records, versions, summaries, review queue, changes. Assets in object storage (S3 or R2) with a manifest table: product id, role (packshot, lifestyle, UGC, ad), rights, source, hash.
4. **Connectors as adapters.** One class per platform with `pull(table, window)` and `status()`, a `mock` mode that returns the generated tables, a `live` mode that calls the API. OAuth apps for Shopify, Meta, Google, Klaviyo. Tokens in a secrets manager, read-only scopes, never in the repo.
5. **Jobs and schedules.** A worker process that runs crawls, extractors, syncs and the weekly ask. Cron or a queue (Cloud Run Jobs, Render cron, or a Python worker with Redis). Every job writes a run record with duration, rows and errors.
6. **Model calls server side.** Extractors call the Claude API with structured outputs for their fixed schema. Bulk runs (tagging thousands of reviews) go through the Batch API at half price. The T0 card and T1 summaries sit first in every prompt for prompt caching. Budget ledger enforced per brand per day.
7. **The brain API.** `GET /brain/<brand>/card`, `GET /brain/<brand>/sections/<name>`, `GET /brain/<brand>/package?capability=<id>`, `POST /brain/<brand>/records` (proposed), `POST /brain/<brand>/review/<id>`, `GET /brain/<brand>/BRAIN.md`, `POST /brain/<brand>/documents` (any file plus an optional note), `GET /brain/<brand>/health`, `GET /brain/<brand>/versions`. Agents and screens use only these.
8. **Auth and tenancy.** Login (magic link or an auth provider), brands per account, roles (founder, team, agency), every query scoped by brand id. Rate limits on crawling, respect robots.txt, per-brand data export and deletion.
9. **Hosting.** One app service (the existing `app/server.py` grown up, behind auth), one worker, one database, one bucket. Fly, Render or Cloud Run all fit. Logs and a health page.
10. **Migration path from the demo.** The Bombas brain is built as JSON files under `app/brain/bombas/` with this exact schema. The store module reads files now and a database later. Nothing above it changes.

## 9. What we build now for Bombas

Session S1.2 runs the extractors that need no private access: site crawl, Ad Library, reviews, interviews and press, job postings. Output: `app/brain/bombas/<section>.json`, `sources.json`, `assumptions.json`. Every record public. Kevin reviews from the files and, once the screen exists, from the brand brain screen.

Calibration fields that S1.2 must fill or mark open, because the generator needs them: revenue band and source, AOV estimate from the price ladder and pack sizes, repeat rate if stated anywhere, channel mix from interviews, seasonality from the promo history in emails and ads, giving units by year, retail partners.

## 10. Decisions

Made by Kevin on 28 Sep 2026:

- Provenance is optional. Records need only id, brand, section and a value or text. Source, date, confidence and tier are used when present. Raw uploads are kept as documents with a one-line manifest entry and are never blocked.
- The brain is structured for the whole product, not for ads.
- One small `BRAIN.md` per brand routes to sections, skills, agent files and the data layer. It does not hold everything.
- Founders and teams can add context at any time, from anywhere, and it refines the brain.
- A weekly job audits the brain and the skills it links to, and proposes improvements, alongside at most 5 questions.
- Reviews are read from the brand's own site, Amazon and retailers on day one for every new brand, 5-star and 1-star first, and turned into objection ladders that feed avatars, offers, copy and the Amazon listing. Amazon is a public sample plus the brand's export, never bulk scraping.
- Sources are a registry of many, not 3 integrations. Pull everything connected first, then ask only what no connected source can answer, ranked by how much it helps the customer.

Still open:

1. The 28 sections in section 4: cut or add any before S1.2 runs.
2. Auto-publish low-risk changes with a 7-day revert window, versus gating everything. Recommendation: auto-publish.
3. Ask cadence: weekly, or every 2 days.
