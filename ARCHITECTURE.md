# ecomOS agent architecture

Date: 25 Sep 2026. Status: proposal for Kevin's decision. Built on what exists: the card library (7,611 cards), the idea bank (4,650 ideas across 25 domains), the Gehna gallery and brand record, and the two blind tests that showed playbooks do not help when loaded as instructions.

## The answer in short

- 14 agents in 4 layers. 3 run the loop (Diagnose, Propose, Registrar). 3 keep the stores honest (Brand Brain Keeper, Reference Scout, QA Gate). 8 execute, one per output surface, not one per folder. Each specialist owns 2 to 4 of the 25 folders; the multi folder routes by bottleneck.
- The execution layer never starts from a web search. Order: the brand's own numbers first, then an audit of the brand's own surface, then the idea bank, then the web to verify and fill gaps, then scoring in code, then the founder, then execution, then the registry.
- Build 4 agents first and run the whole loop on one bottleneck (Gehna site speed): Diagnose, Propose, the Site specialist, Registrar, with a review page for approvals. Add specialists as approved ideas demand them.

## The four layers

### 1. Data layer: brand brain and warehouse

What it holds, per brand:
- Brand record: products with prices, weights and stock read from the site by script with the date; policies (shipping, returns, exchange, EMI, warranty) as quoted from the page; claims in 3 tiers (approved, site-backed, forbidden) each with evidence; voice with liked and disliked examples; audience; decisions log (every "confirm before launch" answer stored once).
- Warehouse: orders and sessions (Metabase, GA4), ad accounts (Meta cache today, Google later), email and SMS platform, reviews and support tickets, competitors (ad library, sites), speed measurements.
- Metric contract: a fixed list of computed numbers with freshness stamps (the vocabulary in `ideas/README.md`). Computed in code. Missing shows as unavailable, never 0. Windows end on the last full day.
- Experiment registry: idea id, brand, status (proposed, approved, rejected, parked, running, read, learned), owner, artefact, metric, read point, kill and scale rule, result, learning, founder reason.

What exists: `data/meta-gallery/` (Meta cache, brand.json, sales, competitors), the speed measurements from the first test, the site facts the copy-test arms pulled. Missing: the schema, the collectors as scheduled scripts, the metric contract, the registry.

Agent: Brand Brain Keeper. Runs the collectors, diffs the site against the last snapshot, tiers claims, flags stale facts, keeps the decisions log. Mostly scripts; the model only tiers claims and writes the voice notes.

### 2. Intelligence layer

What it holds: the idea bank (4,650 ideas, brand-agnostic, filtered by bottleneck and store type, scored in code), the card library (evidence behind each idea, keyword search is free), benchmarks and thresholds, and web research as a tool with rules (public web stays separate from private data, every fetched fact carries its URL and date).

Agents:
- Diagnose. Input: the metric contract and its history. Output: a ranked list of bottlenecks with the numbers that prove each one, the money at stake computed in code, and what data is missing. It does not propose fixes.
- Propose. Input: the top bottleneck, the audit of the brand's surface, the bank, the web. Output: a ranked proposal list (see the flow below). This is the agent that answers "what should we do next".

### 3. Inspiration layer

What it holds: references by angle, format and mood. Competitor ads (7 brands already in the gallery), the brand's own winners with ad-level results, landing page and email swipes, creator content. Rule: structure and mood only, never text, logos, products or faces. Generated images can redraw products, so real photos where accuracy matters.

Agent: Reference Scout. Given an approved idea and a surface, returns 3 to 8 references with why each one fits, tagged so the specialist can cite them. Extends `intelligence/creative_retrieval.py`.

### 4. Execution layer

The founder gate sits at the top of this layer. Nothing below runs on an idea the founder has not approved, and nothing writes to an external system (Meta stays read-only) until Kevin turns that on per surface.

Specialists, each owning folders and an output type:

| Specialist | Folders | Produces |
|---|---|---|
| Site | 05-SET, 07-LPG, 08-SPD, 09-CRO | developer briefs with thresholds and rollback, page specs and copy, CRO test specs, pull requests on a custom site |
| Paid creative and copy | 10-MCR, 11-ADC | ad concepts, static and video briefs, hook banks, copy sets with claim checks |
| Media buyer | 24-DEP, 12-GAD | account structure, budget and test plans, kill and scale rules, change lists for a human to apply |
| Lifecycle | 14-EML, 17-CXP, 03-OFF | flows, campaigns, offer designs, retention programs, post-purchase fixes |
| Organic and search | 13-ORG, 15-SEO, 16-AEO | content calendars, pages, technical SEO briefs, answer-engine fixes |
| Product and supply | 01-PRD, 18-COG, 22-AMZ | product briefs, supplier RFQs, landed cost models, marketplace listings |
| Money and ops | 20-FIN, 21-OPS, 06-MEA, 23-SEC | P&L and cash models, tracking fixes, hiring scorecards, security audits |
| Brand strategist | 02-AVT, 04-BRD, 19-WLD | positioning, avatars, naming, wild bets with stage gates |

Shared by all specialists:
- QA Gate. Runs before anything is delivered: every claim traced to the brand record, every number recomputed in code, windows end on a full day, reading level, no competitor text, no placeholders, Meta read-only. This is the checklist that would have caught every miss in the copy test.
- Registrar. Writes the registry entry when an idea is approved, checks read points on schedule, records results, updates the brand's effect prior for that idea, and turns founder reasons into ranking weights.

Why 8 specialists and not 25: agents are grouped by what they produce, because a developer brief, an ad set and an email flow need different tools, references and QA. The 25 folders are how the knowledge is filed, not how the work is done. The multi folder has no owner; its ideas reach the right specialist through the bottleneck tag.

## How Propose pulls ideas

This is the order, and the reasons for it.

1. Diagnose from the brand's numbers. No web, no bank. The bottleneck must come from the metric contract, or the system chases what is fashionable instead of what is broken. Output: 1 to 3 bottlenecks with money at stake.
2. Audit the brand's own surface for that bottleneck. For speed: the Chromium runs on 3 pages. For retention: the flows that exist, the past-customer campaigns that do not, the frequency data. For copy: what the account runs and what the site promises. This produces observed conditions with evidence, the way the Gehna speed audit did. It is the most valuable step, because idea applicability is decided here.
3. Pull candidates from the idea bank. Filter in code by bottleneck and store tags (Gehna: high AOV, luxury or considered, catalogue, custom platform, India mobile, paid social led). Then the model matches each idea's `signal.check` against the observed conditions and keeps only the ideas whose signal fires, quoting the evidence. Expect 30 to 80 candidates from a few hundred.
4. Web research, scoped and last. Two jobs only: verify anything time-sensitive in the candidates (platform UI, current benchmarks, a policy), and search for tactics the bank lacks for this bottleneck and category. Web-sourced candidates carry their URL and date, get a lower prior, and are written to a candidates file for curation into the bank. The web is last because the bank is curated and the web is noisy. It is not skipped because the bank is 2026 material and platforms move.
5. Score in code. Reach: orders, sessions or revenue the idea touches, computed from the contract. Effect: the bank's basis and size, adjusted by any brand prior from the registry. Effort, cost, risk, reversibility, confidence from the record. Founder weights from past reasons. Dependencies from prerequisites. The model fills the evidence fields; the arithmetic and the sort are code.
6. Write the proposal cards. Each: the idea, why now (the observed condition and the numbers), what it could move and the basis, what it costs, how we will know (metric, read point, kill and scale rule), what it depends on, and the owner specialist.
7. Founder gate. Approve, reject or park, with a reason. Reasons become weights.
8. Execute. The owning specialist takes the idea record, the brand brain, references from the Scout, and its domain checklist, and produces the artefact. QA Gate checks it. Registrar logs it with its read point.
9. Learn. At the read point the Registrar pulls the metric, records the result, and updates the brand's prior for that idea. The bank itself does not change; brand results live in the registry and a brand overlay.

## Model routing

- Collectors, extraction, signal matching, QA checks, registry work: Haiku or Sonnet. These are structured tasks with clear inputs.
- Diagnose narrative, Propose ranking rationale, specialist creative work and briefs: Fable.
- All arithmetic in code, whichever model.
- A run for one bottleneck should cost a fraction of the copy test, because most tokens go to structured steps on cheap models and the bank replaces open-ended research.

## What exists and what to build

| Piece | State |
|---|---|
| Card library and search | Built |
| Idea bank, loader, scoring v0 | Built |
| Meta cache, brand.json, sales, competitors | Built for Gehna, manual refresh |
| Speed measurement instrument | Built (Chromium, throttled profile) |
| Brand brain schema and collectors | To build |
| Metric contract | To build |
| Experiment registry | To build |
| Diagnose, Propose, Registrar | To build |
| Review page for the founder gate | To build (the gallery's action plan tab is the seed) |
| Site specialist and QA Gate | To build |
| Other 7 specialists, Reference Scout | Build on demand from approved ideas |

## Build order

1. Brand brain schema, metric contract for Gehna, registry schema. Fill from what exists.
2. Diagnose and Propose on Gehna site speed, end to end, with the review page. Kevin approves or rejects with reasons.
3. Site specialist executes 1 or 2 approved ideas as developer briefs. QA Gate on the output. Registrar logs read points.
4. Second bottleneck through a second specialist (likely Lifecycle or Paid copy, since the copy test already produced the audit) to prove the loop is general.
5. Then the remaining specialists, each built when a ranked idea needs it.

## Decisions for Kevin

- Where the founder gate lives: the gallery page (already published) or a new page.
- When Meta write access is switched on, and for which surfaces. Until then every execution is a brief, a draft, a change list or a pull request.
- Whether specialists are shared across brands (one Site specialist with a brand parameter) or copied per brand. Shared is the default here.
- How much web research per run. The default above caps it at verification plus one gap search per bottleneck.
