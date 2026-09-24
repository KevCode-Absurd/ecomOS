# ecomOS — complete project handoff to Claude

Prepared 24 September 2026, Asia/Kolkata. This is a technical and product handoff, not a claim that the complete operating system is deployed.

## 1. Start here

The owner is Kevin. The product is an ecommerce operating system for brands and agencies, spanning research, offers, creative, copy, landing pages, acquisition, retention, operations and measurement. Its differentiation should come from expert ecommerce knowledge combined with the brand's own data, approved voice, references and history of what has been tried.

The main completed foundation is a local intelligence library: **7,611 task-sized cards from 256 source documents**, covering **23 topic folders plus one mixed folder**. It has keyword and semantic retrieval, metadata labels, task-specific creative routing, draft playbooks for all 23 topics and several evaluated ad-copy playbook versions. A separate Meta gallery has subsequently been substantially expanded through Claude. The integrated multi-tenant product, general brand brain, general reference library and autonomous execution platform are not complete.

**Do not restart ingestion, regenerate the cards or assume all old READMEs describe the present state.** Read the current files, preserve outputs, and continue from the strongest tested components.

### Location and identity

```text
Project / Git root:
C:\Users\kevin\Documents\Codex\2026-09-22\https-drive-google-com-drive-u\outputs\ecom-intelligence

Canonical cards:
data/library-v3/cards.json

Repository:
https://github.com/KevCode-Absurd/ecomOS

Drive root:
https://drive.google.com/drive/folders/1wo7oScCia-h3XiwW_Ogjcvkr60_S11Ax
```

The owner says the repository is private; keep it private. This handoff did not make a live GitHub privacy or access check. The sanitized local origin points to that repository. At the start of preparation HEAD was `e47e9eb`; another session subsequently committed `c403d0d` (data folder) and `c3f8d77` (`CLAUDE.md`). The final snapshot observed HEAD `c3f8d77`, with `main` matching its cached `origin/main` ref. Do not equate a local tracking ref with a fresh remote check.

**Read [HANDOFF_PROJECT_SNAPSHOT.json](HANDOFF_PROJECT_SNAPSHOT.json) for timestamped local counts, hashes, Git state and budget balances.** Git staging changed while this document was being prepared; recheck it before any commit. Do not overwrite another session's work.

### Recommended reading order

1. Existing repository notes [CLAUDE.md](CLAUDE.md), this document and [CLAUDE_START_HERE.md](CLAUDE_START_HERE.md). The handoff complements the repository notes; it does not replace them.
2. [LIBRARY_WORKFLOW.md](LIBRARY_WORKFLOW.md), [KNOWLEDGE_RETRIEVAL.md](KNOWLEDGE_RETRIEVAL.md), [CREATIVE_RETRIEVAL.md](CREATIVE_RETRIEVAL.md).
3. [AD_COPY_ITERATION_DECISION.md](AD_COPY_ITERATION_DECISION.md) and [the final copy comparison](AD_COPY_TASK_FIRST_COMPARISON.html).
4. [playbooks/README.md](playbooks/README.md), [operating contract](playbooks/OPERATING_CONTRACT.md), [working ad-copy candidate](playbooks/ad-copy-v1.2/README.md).
5. [META_GALLERY_STATUS.md](META_GALLERY_STATUS.md), newest updates first. This includes later Claude work that older Codex-era notes do not contain.
6. Older experiment reports as needed, using the phase map below. They are evidence and history, not automatic current operating instructions.

## 2. Owner intent, priorities and decisions

Kevin has worked in ecommerce for roughly six to seven years and curated the sources based on industry taste. The source library is mostly YouTube transcripts, articles, copied text and books. Its purpose is better ecommerce decisions and usable deliverables, not an elaborate citation product.

Important decisions from the conversation:

- **Quality first, cost second, speed third.** The product motto is cheaper, faster, better, but do not claim all three have been demonstrated or sacrifice output quality merely to reduce context.
- Models can be economical or frontier. This is not a cheap-model-only project. Compare the same model with/without useful knowledge and compare models where appropriate.
- The owner explicitly simplified the initial over-engineered extraction approach: clean text, create actionable cards, tag them and retrieve only relevant guidance. An 80/20 internal knowledge base is acceptable. Do not reinstate mandatory exact-quote approval for every card as the default pipeline.
- Text-only ingestion was intentional. Images and embeds in source documents were ignored. This is not missing work that needs to be paid for again.
- All cards must support merchant tasks. General-book principles can transfer, but service-agency sales-call procedures should not become ecommerce guidance merely by changing a tag.
- Expert reputation does not mean every statement is current or applies to every brand. Retain important qualifications and distinguish source examples from brand facts.
- Source cards stay intact while playbooks evolve. Owner feedback may change a playbook, a brand-voice record or an applicability rule; these are different changes.
- Knowledge and external research can work together. Do not force an either/or design. Keep private business data out of public web searches.
- Do not stuff a context window just because space is available. Equally, do not make an arbitrary tiny context cap the goal when a complex task needs more guidance.
- The owner wants natural, simple, direct copy, roughly below tenth-grade reading level: avatar-specific, benefit-led, concrete and aspirational without vague hype. The product should credibly connect the unwanted before state to the desired after state.
- Judge usable outputs through an owner/agency lens. AI reviewer scores are advisory, and the latest experiments showed substantial score instability. Owner preference and editing effort are more useful next signals.
- The owner chose to work on brand-brain planning separately. Do not confuse the last recommendation to collect copy preferences with a requirement to pause every other possible implementation task.

Budget history: initial processing discussions ranged around $100–$170, with a $200 overall ceiling. The shared ledger retains a $160 working stop and $200 absolute ceiling. A $10 CRO limit and $20–$25 benchmark limits were used at particular stages; they are not interchangeable ongoing caps. The two latest copy rounds had separate $2 caps and together used about $0.1454 in estimated new API usage. Check existing ledger reservations before any paid continuation. Historical account credits are not current balances.

## 3. Architecture: what exists and what is still planned

```text
Business systems                 Curated source library          Reference assets
Shopify / Woo / Meta / email     transcripts, books, articles     ads / emails / pages
          |                              |                              |
    DATA LAYER                   INTELLIGENCE LAYER               INSPIRATION LAYER
          |                    cards + labels + retrieval         assets + searchable analysis
          v                              |
     BRAND BRAIN                 TASK PLAYBOOKS
facts, voice, audience,          procedures, inputs, outputs,
claims, objectives              decision rules and checks
          \______________________________|______________________________/
                                         |
                              FUTURE EXECUTION AGENTS
                      context assembly -> draft -> validate -> act
                                         |
                             EXPERIMENT / DECISION MEMORY
                      attempts, variants, results, caveats, feedback
```

| Component | Current state | Important boundary |
|---|---|---|
| Raw source ingestion | Local inventory, snapshots, parsed text and completed card extraction | Continuous Drive change reconciliation is not a running service. |
| Intelligence cards | 7,611 cards; all 256 source IDs represented | Structural completeness is not exhaustive semantic coverage or correctness. |
| Retrieval | Working Python/CLI hybrid search; metadata; creative routes | Not hosted/MCP; applicability still partly heuristic; no exhaustive recall proof. |
| Playbooks | 23 domain drafts × 3 workflows; focused ad-copy editorial versions | Most domains are scaffolds with candidate evidence, not fully curated agent policies. |
| Brand brain | Architecture discussed; benchmark brand fact sheets exist | A general persistent, approved brand-brain service is not built. |
| Data layer | Peach Bucket exports; separate Claude-built Meta/Metabase gallery capture | Not a general production connector platform for every brand. |
| Inspiration | Design discussed; Meta gallery has competitor references and creative features | A general 2,000-asset static/email/landing-page library is not complete. |
| Execution | Draft/validation experiments; local gallery creative endpoints | No end-to-end autonomous ecommerce operator or authorization framework deployed. |
| Experiment memory | Many saved manifests, attempts, outputs and reviews; gallery notes/tests features documented | No unified cross-agent experiment registry preventing duplicate tests across the whole product. |
| Hosting/security | Local development; private repository intended | Production auth, tenant isolation, secret management, monitoring and hosting need explicit implementation/review. |

Experiment history should be a structured, brand-linked record: hypothesis, input/context versions, assets, dates, channel, budget, attribution, decision, result and limitations. The brand brain may contain a summary of learned preferences; detailed experiment history should remain queryable rather than becoming one giant prompt. This is a proposed design, not a completed database contract.

## 4. Work completed from the beginning

### Phase A — access, inventory and the first foundation

1. The user supplied the Drive folder and created `KevCode-Absurd/ecomOS`, later making it private.
2. API billing was set up for DeepSeek and OpenAI. No Anthropic API key was supplied in the conversation; an Anthropic subscription was mentioned. Do not assume subscriptions are general API billing credentials.
3. A Google Cloud project and Drive-reader service account were set up. Local scripts use `secrets/drive-reader.json` and read-only Drive scope. The account expected by `scripts/check_drive.py` is `ecomos-drive-reader@ecomos-509406.iam.gserviceaccount.com`.
4. The source inventory was measured, rather than relying on the original estimate of 300–400 sources: **293 files = 256 source documents + 37 supporting files**, across 24 content groups.
5. Immutable source snapshots, DOCX/TXT/Markdown parsing, paragraph/table locators, source/version IDs, segmentation, a SQLite store, condition evaluation and spending controls were implemented.

Relevant code: `intelligence/parsing.py`, `segmentation.py`, `store.py`, `conditions.py`, `context.py`, `budget.py`; `scripts/inventory_drive.py`, `snapshot_drive.py`, `audit_corpus.py`, `segment_corpus.py`, `catalog_sources.py`.

Historical reports: [BUILD_GUIDE.md](BUILD_GUIDE.md), [SETUP_NEXT.md](SETUP_NEXT.md), [QUALITY_STANDARD.md](QUALITY_STANDARD.md). Some contain old prerequisites superseded by the simpler practical-card workflow.

### Phase B — extraction calibration and why the design changed

The initial design spent considerable effort on exact quote anchoring, per-claim evidence, conditions, approvals and review. It created useful infrastructure but was too slow and fragmented for the owner's intended internal knowledge product.

| Test | What actually happened | Main lesson |
|---|---|---|
| Eight-excerpt initial calibration | 24 calls across DeepSeek low, Terra low and DeepSeek non-thinking; about $0.1283 | DeepSeek non-thinking completed cheaply; the sample overrepresented headers, so it did not establish full-corpus quality. |
| 24 body-excerpt comparison | Both providers completed 24 responses; 69 candidate cards each; about $0.662339 for this stage | Exact-quote formatting and structure are not semantic accuracy. Three-card output caps did not establish recall. |
| Revised typed units | Action/principle/example/warning units; ALL/ANY conditions; evidence offsets | Better representation, but risk of over-fragmentation and expensive review. |
| Wider V2 staging | 23 DeepSeek results + one separate Terra fallback; 369 staged units: 316 candidates, 53 held; 84 follow-ups | A connection failure remained uncertain; it was not represented as 24/24 DeepSeek success. |
| Six-scenario context comparison | 18 decision outputs comparing no library, raw excerpts and curated units | Curated packets reduced input size, but some useful guidance was omitted and one recommendation became too eager to act. |

The six-scenario test measured approximately 37.27% fewer total prompt tokens for curated packets versus raw excerpts, but did not establish a decision-quality win rate. High reasoning sometimes exhausted completion limits; this is a configuration issue, not a universal argument against reasoning.

Read: [CALIBRATION_RESULTS.md](CALIBRATION_RESULTS.md), [BODY_CALIBRATION_RESULTS.md](BODY_CALIBRATION_RESULTS.md), [V2_EVALUATION_RESULTS.md](V2_EVALUATION_RESULTS.md), [AGENT_EVALUATION_REVIEW.md](AGENT_EVALUATION_REVIEW.md).

**These V1/V2 stores and units are historical experiments, not the canonical current 7,611-card library.** Do not count them again as additional production cards.

### Phase C — practical card extraction, CRO first, then every folder

The owner explicitly redirected the work to a practical text transformation:

1. Clean the available text locally; ignore embedded images.
2. Keep related paragraphs in coherent sections.
3. Convert each section into useful task-sized cards: title, searchable summary, when to use, steps, caveats and tags.
4. Attach stable source/version metadata automatically.
5. Validate structure and cache results; use targeted repairs instead of another mandatory model review for every card.
6. Start with CRO; make it ecommerce-focused; then product research and numbered folders sequentially; finally mixed material.
7. Refresh keyword and semantic indexes as folders complete.

The active bulk transformation used `deepseek-flash` with thinking disabled after a lower-reasoning configuration wasted completion space or truncated outputs. Selective OpenAI adaptations/reviews were used for difficult broad-business material. This extraction setting does not constrain runtime-agent model choice.

Targeted cleanup included removing service-only sales-call and agency procedures from CRO, adapting transferable book guidance to merchant tasks, distinguishing source recommendations from universal thresholds, and handling broad-source/English cleanup where needed. Inspect individual `*_STATUS.md` files and `data/library-v3/*review*.json` / `*cleanup*.json` for exact corrections. Original model results and pre-adaptation material were retained separately.

The completion audit on 22 September recorded **630/630 sections with results**, including **55 intentionally empty sections**. Most were headers/routing material; five body sections were excluded as service-only, biography/testimonials, speculative closing discussion or promotion. Every source contributed cards. The live Drive inventory at that audit matched its snapshot. **This handoff did not recheck Drive on 24 September.**

Canonical counts, rechecked locally for this handoff:

| Folder / domain | Cards |
|---|---:|
| 01 Product research | 170 |
| 02 Avatars | 216 |
| 03 Offers | 270 |
| 04 Brand | 524 |
| 05 Store setup | 432 |
| 06 Measurement | 117 |
| 07 Landing pages | 400 |
| 08 Speed | 226 |
| 09 CRO / testing | 177 |
| 10 Paid social creative | 319 |
| 11 Ad copy / deployment | 756 |
| 12 Google Ads | 221 |
| 13 Organic / content | 149 |
| 14 Email / lifecycle | 578 |
| 15 Search / SEO | 420 |
| 16 Answer / generative engines | 173 |
| 17 Post-purchase | 112 |
| 18 Sourcing | 82 |
| 19 Wild bets | 96 |
| 20 Finance / accounting | 203 |
| 21 Team / management | 258 |
| 22 Amazon marketplace | 284 |
| 23 Bot / agent security | 412 |
| 99 Mixed | 1,016 |
| **Total** | **7,611** |

Read: [LIBRARY_WORKFLOW.md](LIBRARY_WORKFLOW.md), [LIBRARY_PROGRESS.md](LIBRARY_PROGRESS.md), [FINAL_COMPLETENESS_CHECK.md](FINAL_COMPLETENESS_CHECK.md). The older progress report's cumulative cost is historical; use the snapshot ledgers for the current local estimate.

## 5. Where the intelligence lives

| Path | Purpose |
|---|---|
| `data/library-v3/cards.json` | Canonical consolidated active cards; top-level `cards` list. |
| `data/library-v3/markdown/` | Human-readable per-folder exports. |
| `data/library-v3/manifest.json` | Current extraction jobs/source-section associations. |
| `data/library-v3/progress.json` | Completion report. |
| `data/library-v3/search.sqlite` | SQLite full-text keyword index. |
| `data/library-v3/vectors.json` | Semantic vectors keyed by card ID. |
| `data/library-v3/metadata.json` | Labels keyed by card ID/content hash. |
| `data/library-v3/metadata-overrides.json` | Reviewed metadata overrides, bound to content hashes. |
| `data/library-v3/embeddings/` | Cached embedding responses. |
| `data/snapshots/` | Raw/downloaded source snapshots and ingestion artifacts. |
| `data/inventory/`, `data/source-catalog.json` | Drive/source discovery records. |
| `data/units/`, `data/cro-folder-v1/`, `data/calibration-*` | Earlier experiments; not the active card source of truth. |

Each current card contains:

```json
{
  "id": "stable card identifier",
  "title": "task or principle title",
  "summary": "searchable short description",
  "use_when": "applicability text",
  "steps": ["coherent actionable guidance"],
  "caveats": ["important conditions and limits"],
  "tags": ["specific search tags"],
  "source_id": "source identifier",
  "source_sha256": "source version hash",
  "source_name": "source name",
  "folder": "source folder",
  "domain": "normalized topic domain",
  "section": "source section locator"
}
```

This is an illustrative schema, not a fabricated source card. The actual cards include all of those fields. Source pointers remain useful internally even though client-facing exact citations are not the main product requirement.

Current card-file SHA-256:

```text
0287a2e2df3a54711125de9d2927b1efd3d7add875be994c4af6f326cfa84074
```

The handoff audit found 7,611 unique IDs, 256 distinct source IDs, 7,611 metadata records, 7,611 vectors and 7,611 keyword-index rows. The playbook experiments did not alter the canonical cards.

**One folder should not become one giant card.** A topic can contain many independent decisions, conditions and substeps. The corpus is already consolidated into one JSON file for storage. Retrieval granularity remains the individual useful card. Putting all CRO knowledge into one model input would usually add irrelevant tokens rather than improve search.

## 6. Exactly how retrieval works now

Primary entry point: `scripts/search_knowledge.py`. Engine: `intelligence/knowledge_search.py`. The older `scripts/search_library.py` is retained for comparison and should not be mistaken for the preferred compact interface.

1. A reusable engine loads the consolidated cards, metadata, keyword-index connection data and vectors. It does not ask a language model to read each source file for each request.
2. It checks file timestamps/sizes and reloads changed library artifacts. Stale/missing metadata hashes fall back to conservative classification.
3. It tokenizes the task into search terms and derives task-intent labels. Optional explicit filters restrict domain, platform, knowledge type, role or durability. Programmatic allowed/excluded IDs support creative routing.
4. SQLite FTS ranks keyword matches using BM25. It keeps up to 150 eligible keyword candidates. The actual weighting expression is `bm25(search,0,5,3,4,1)`; inspect the index schema before interpreting each column weight.
5. If semantic search is enabled, the query includes the task and supplied brand context. `text-embedding-3-small`, 512 dimensions, supplies a vector. Existing card vectors are normalized and compared with a NumPy matrix operation. Up to 150 eligible semantic candidates join the pool.
6. Each ranking contributes reciprocal-rank score `1 / (60 + rank)`, with rank starting at 1. Then the engine adds `0.025 × query-term coverage` and `0.008 × inferred task-label overlap`.
7. Seasonal titles get a 0.65 multiplier when the task/brand context lacks corresponding seasonal intent.
8. Candidates below 55% of the top combined score are suppressed. A card without query-term overlap must have cosine similarity at least 0.30. These thresholds are heuristics, not calibrated probabilities.
9. Duplicates with matching normalized titles and caveats are suppressed. Near-duplicate titles with matching caveats and title-term Jaccard overlap at least 0.78 are also suppressed. This is conservative lexical suppression, not complete semantic deduplication.
10. Whole rendered cards are packed while they fit the token budget. Oversized cards are skipped, not cut mid-step. The engine does not claim validated sentence-by-sentence extraction.
11. Only the compact context is intended for the writing model: card ID/title, applicability, steps and essential caveats. Administrative metadata and full card objects are not duplicated in that text.
12. The response also provides IDs, token count, elapsed time, warnings, no-match state and `needs_current_check` IDs for volatile/periodically changing advice. The application must actually use those signals.

Defaults are **8,000 knowledge tokens/up to 16 cards** for focused tasks, **16,000/up to 32** for multi-part or broad tasks. These are ceilings, not quotas, and can be overridden. Token counting uses `o200k_base`; complete request overhead, brand context, reference images, instructions, tools and output require separate accounting.

Query embeddings are cached in memory for up to 128 queries and on disk by request hash. Warm search can be very fast; a new embedding requires a provider call. Supplied brand context goes to that embedding provider when semantic search is enabled; do not put secrets or unnecessary sensitive records into it. Keyword-only mode avoids the embedding API. If semantic search fails, the engine falls back with a warning and does not automatically retry.

Historical measurements: roughly 1.37 seconds cold load and 23.7 ms median repeated-query search in the initial local checks. First-time embeddings added roughly 0.6–3 seconds in a small sample. Those are not production latency promises. Reuse an engine rather than launching a fresh Python process for each request.

### Labels already implemented

- Knowledge type: principle, diagnostic, procedure, tactic, case-study, unknown.
- Roles: foundation, growth, operations, protection; multiple permitted.
- Durability: durable, periodically-changing, volatile, unknown.
- Task labels: checkout conversion, product page, creative testing, offer design, customer research, retention, email/SMS, search acquisition, organic discovery, measurement, profitability, site speed, security, inventory/sourcing, team operations, marketplace.
- Domain, platform mentions, applicability, caveats, source/evidence status and date fields where known.

Labels are inferred/classified, not independent factual verification. Durable does not mean universal. Growth does not mean a known expiry date. Unknown dates remain unknown. Source creators' reputation is not a substitute for checking changing platform instructions.

### Creative retrieval specialization

`intelligence.creative_retrieval.retrieve_campaign(engine, queries)` runs routes for avatar research, landing-page guidance, static ads and writing principles. Writing principles are restricted to ad-copy material. It uses domain plus title/tag eligibility, up to four cards per route, and excludes already-selected IDs across routes.

This stopped plainly unrelated staff-permission and security cards from entering creative packets. It still does not fully enforce brand constraints: a fixed-offer brief can retrieve offer-tier advice. Pass only each route's `context` and `purpose` to the generator, retaining full audit objects server-side. Do not send the compact context and full cards again.

## 7. Benchmark history and what it really established

All scores below are experiment-specific. Different rubrics, prompts, models, task sets and reviewer batches mean they must not be plotted as one continuous accuracy metric. None establishes conversion lift or universal superiority.

### 7.1 Fictional ecommerce pilot

`BENCHMARK_RESULTS.md`, `BENCHMARK_COMPARISON.html`, `data/ecommerce-benchmark-v1/`.

- Ten fictional-brand tasks: six diagnostic questions and four artifact tasks.
- DeepSeek Flash high and GPT-6 Astra medium, each with and without retrieved cards: 40 eventual usable outputs.
- DeepSeek needed 15 recoveries after truncation/malformed outputs; recovery raised the completion allowance from 8,192 to 32,768. Therefore this is not a clean equal-limit model comparison.
- Mean advisory scores: DeepSeek 87.4 without vs 86.2 with; Astra 98.9 vs 99.6. Astra had a ceiling effect. Retrieval was not a consistent win.
- Large packets contained 14–32 cards and 3,837–9,620 tokens. Some recommendations misapplied source thresholds or exceeded contribution/inventory constraints.
- Experiment cost including recoveries/reviews: approximately $5.1194, historical estimate.

The interrupted V2 successor and the later owner-oriented V3 must not be merged into a pretend complete clean trial. Read `data/ecommerce-benchmark-v2/` and the later report's notes about retained reservations.

### 7.2 Owner/agency workflow benchmark

`OWNER_BENCHMARK_READOUT.md`, `OWNER_BENCHMARK_RESULTS.md`, `OWNER_BENCHMARK_COMPARISON.html`, `data/ecommerce-owner-benchmark-v3/`.

- Fictional Shopify brand TrailFold, with prices, costs, inventory, Meta, Klaviyo, customer questions and team capacity.
- Nine tasks: acquisition economics, abandonment flow, PDP, attribution audit, static creative, landing-page handoff, bundle offer, post-purchase flow, agency update/task board.
- Models: **GPT-5.6 Luna, Terra and Sol**, medium reasoning. Three conditions: no cards, broad cards, selected cards. **81 comparisons**.
- E1–E4 included draft/action-field checks/revision. A validator initially rejected equivalent field names/types, so affected conditions were corrected consistently; original artifacts remain.

| Model | No cards /4 | Broad /4 | Selected /4 |
|---|---:|---:|---:|
| Luna | 3.41 | 3.15 | 3.24 |
| Terra | 3.34 | 3.73 | 3.71 |
| Sol | 3.78 | 3.75 | 3.90 |

Selected packets reduced knowledge tokens by 72.3% versus broad packets: 5–7 cards / 1,551–2,279 tokens instead of 20–24 / 5,714–7,327. But model-based selection added around 13.58 seconds and its own cost. Selection could omit needed coverage. A smaller packet was not always better; broad guidance helped one landing-page workflow more.

Average selected-context costs exceeded no-card costs: Luna approximately $0.0090 vs $0.0038; Terra $0.0525 vs $0.0374; Sol $0.1081 vs $0.0760. The experiment did not prove retrieval was cheaper than an unassisted model doing no research. It showed that potential savings need to come from better model/task routing, avoiding unnecessary research/retries, caching and less operator editing—not from pretending context tokens are free.

Full evaluation committed about $8.56 including selection/reviews/corrections and uncertain predecessor reservations. Do not add this to overlapping global cumulative totals. No new matched Astra comparison here proved that Terra beats Astra.

### 7.3 Real brand: Peach Bucket with public research

`PEACH_BUCKET_WEB_BENCHMARK_PLAN.md`, `PEACH_BUCKET_WEB_RESULTS.md`, `PEACH_BUCKET_FINDINGS.md`, `PEACH_BUCKET_WEB_COMPARISON.html`, `data/peach-web-benchmark/`.

The owner supplied the child-safety-kit website, Shopify and Meta CSVs, screenshots and economics. Public research was separated from private analysis after the first combined design was rejected by automatic approval review for possible private-data leakage into web queries. The replacement gives both arms identical public research per model/task and introduces private facts only in the analysis stage.

- 39/48 answers completed; 19 complete A/B pairs; only 7/16 simulated owner/agency reviews valid.
- Reviewed subset: Luna improved 3.09→3.26/4; Terra declined 3.73→3.63; Sol declined 3.64→3.54.
- The stage stopped after transport failures and budget reservations, not because every test completed.
- Historical stage estimate: $6.074523 settled + $14.582655 reserved, under the $25 stage ceiling when embedding accounting is included. Reservations are not confirmed charges; check current ledger before resuming.
- This compared cards after equal public research. It did not prove the library replaced browsing or lowered total research cost.

Known brand facts and cautions for any continuation:

- New store; reported sales reversals were test orders. Do not reinterpret them as customer refunds/RTO without evidence.
- User supplied product cost ₹650, shipping ₹350, payment fee 2% of selling price and RTO 3–4%.
- At ₹3,299 list price: `3299 - 650 - 350 - 0.02*3299 = ₹2,233.02` before ads, RTO and other unconfirmed costs. This is not net profit.
- Attribution: 7-day click, 1-day view, 1-day engaged view, as supplied. Do not sum Meta-attributed purchases with Shopify orders as independent sales.
- Screenshot showed 4,452 sessions, 112 added-to-cart sessions, 101 checkout sessions and 34 completed-checkout sessions. Session counts are not unique customer records; 101−34 does not prove 67 exportable abandoned checkouts.
- Export/screenshot date boundaries differ. Preserve original periods; do not treat them as a clean previous-month comparison.
- Genuine customer-order count remains uncertain after test-order exclusions. Audience motivations inferred from product/Reddit are hypotheses, not verified purchaser demographics.

Original CSVs were supplied from `C:\Users\kevin\Downloads\` with names `Total sales over time - 2026-08-24 - 2026-09-23.csv` and `GTM-and-GA-test-Campaigns-24-Aug-2026-22-Sep-2026.csv`. Do not assume those external paths transfer to another machine; inspect saved benchmark inputs.

### 7.4 Landing-page, hero-section and static-ad comparison

`PEACH_BUCKET_VISUAL_READOUT.md`, `PEACH_BUCKET_VISUAL_COMPARISON.html`, `data/peach-visual-benchmark/`.

- GPT-6 Luna, Sol and Astra × with/without cards = six full landing-page drafts, six hero-section designs, six square ads and matching ad-copy sets.
- The hero deliverable was the **complete top section of the landing page**, not just a product hero photograph.
- Original product references came from the website. Language models received descriptions; the image generator received images. Do not claim every text model inspected image pixels.
- Planning/research was reused within each model pair. Up to six cards per avatar/page/ad query were used in the original route.
- One blinded copy review scored Luna 2→2, Sol 4→3, Astra 3→4 out of 4. It was not an image-performance test.
- Text total including review: about $1.43. Built-in image-tool billing was not exposed; image cost is **unknown, not zero**.
- A corrupt reference image required a valid rendition for later renders; that is a visual confound.
- Product components were sometimes redrawn/rearranged by generation. Production creative should preserve the actual product photo as a locked composited layer.

### 7.5 Creative routing and writing V2

`CREATIVE_RETRIEVAL.md`, `PEACH_BUCKET_WRITING_V2_READOUT.md`, `PEACH_BUCKET_WRITING_V2.html`, `data/peach-visual-benchmark/writing-v2/`.

Added category/topic routes and cross-route deduplication; specifically drew writing principles from ad-copy material such as Cashvertising, Copy Hackers and the copywriting course. Compared no cards, old retrieval and routed retrieval on the same revised prompt and fixed per-model plan.

Knowledge context dropped 7.5–15.1%, but improved copy quality was not established. Broad category correctness did not solve fixed-offer/product/proof applicability. Repeated safety qualifications and “the brand advertises” produced evaluator-style copy. Additional text/review cost was about $1.93; no new images were generated. The proposed wider 80/20 launch gate was not passed.

## 8. Playbooks: what was built, tested and retained

### All-domain scaffold

`playbooks/v1/INDEX.md`, `playbooks/domain_specs.py`, `scripts/build_playbooks.py`.

- 23 topic domains × three task workflows = **69 draft workflows**.
- Each has inputs, procedure, deliverable, related domains, checks and candidate supporting cards.
- The builder uses local keyword ranking, not an LLM reconciliation of every book and transcript.
- All 7,611 **card IDs** are accounted for across domain inventories and the mixed inventory. The original validation note says “source IDs”; interpret that as card inventory coverage, not 7,611 distinct source documents.
- Of 1,016 mixed cards, 179 have candidate workflow links and 837 remain explicitly unassigned to workflows, while still searchable.
- Adjacent-topic support remains in some scaffolds. Do not turn candidate matches into unconditional agent instructions.
- `scripts/read_playbook.py` loads a chosen workflow. It is a loader, not an executing agent. Default remains `playbooks/v1`; select editorial versions explicitly.

### Ad-copy editorial versions

| Version | What changed | Status |
|---|---|---|
| v1.1 | Synthesis of ten read cards; conditional principles; writing/revision/objection workflows | Historical editorial baseline. |
| v1.2 | Added concrete imagery, credible feature-to-benefit translation, clear headlines and variant planning; thirteen supporting cards | Strongest current tested candidate, still subject to owner review. |
| v1.3 | Added plain-language target, avatar and credible before/product/after connection | Experimental; simpler but did not improve overall score. |
| v1.4 | Prioritized buying question over scenes/formulas | Experimental; repeated inventory/price and did not replace v1.2. |

Supporting card files live under each version's `ad-copy-deployment/source-evidence.json`; runtime prompts and JSON playbooks are separate. The review criteria are operational choices informed by source principles and owner feedback, not scientifically proven copy-performance weights.

Example reviewed sources/IDs:

- `20fa6900506ffc06314306b2`: short messaging strategy.
- `40638b840ce1e28ea89b4b19`: WIIFM/benefits.
- `d5db0dddac4ab42c3d5640c1`: situational feature-versus-benefit lead.
- `8e6c32baa35ff2f2aa1ef544`: abstract-to-concrete writing.
- `17183d94160ce2f95770a9d7`: simplicity.
- `3f95809c1b82aca30df46509`: actual brand voice.
- `a9db8de6d903f43da80e956e`: verifiable evidence.
- `4fb56bc1019fff1c2b939750`: real objections; research-method transfer, not copying an entire VSL formula.
- `8998cd84ed0c5d71e3f42fc3`: visual words/mental pictures.
- `dc660f4f168c51e69db52095`: feature-to-benefit connection.
- `db040c273327393ad271a94d`: clear rather than merely clever headlines.

Read actual card bodies before adapting them. Do not adopt unsupported example statistics, demographic stereotypes, medical promises or universal performance claims from source examples.

### Ad-copy tests, in order

1. **Initial v1.1:** three briefs (installation, value, reassurance) × generic/playbook/playbook-plus-two-cards; Luna writer; nine outputs/27 variants. Full cards were manually selected, not dynamically retrieved. Cost about $0.006984 for usable generation; malformed-request attempts remain separately logged.
2. **v1.2 refinement:** same original briefs plus a new kit-versus-separate-products brief; Sol/Luna blinded reviews. On the original matched tasks: generic 62.0, v1.1 playbook 67.67, v1.1+cards 63.17, v1.2 playbook 77.67, v1.2+cards 79.67/100. Reviewers disagreed on the extra-card advantage. New brief gains were smaller: 68→70→73.5. New generation/review spend about $0.10547.
3. **v1.3 plain-language round:** five briefs, adding cupboard exploration and grandparent visits; six old outputs reused and nine new outputs; 15 sets reviewed. New rubric: natural language 20%, avatar fit 15%, credible bridge 20%, benefit 15%, visual specificity 10%, crispness 10%, distinctiveness 10%. Generic 55.7, v1.2 76.0, v1.3 74.7. New spend $0.075136.
4. **v1.4 task-first follow-up:** six briefs, including one fresh support-retargeting brief; ten old sets reused, eight new sets; 18 sets re-reviewed under the same rubric. Generic 70.3, v1.2 80.1, v1.4 77.4. New spend $0.070244.

**Critical review limitation:** unchanged generic copy from five briefs scored 55.7 in one reviewer batch and 69.4 in the next. Unchanged v1.2 sets moved 76.0→80.9. The sole fresh follow-up brief was essentially tied: generic 75, v1.2 76, v1.4 77. Do not present small score gains as robust performance improvement, and do not keep rerolling prompts until a preferred version wins.

Final six-brief per-request averages (three variants per request):

| Method | Input tokens | Output incl. reasoning | Seconds | Estimated USD | Approx. reading grade |
|---|---:|---:|---:|---:|---:|
| Generic | 428 | 1,246 | 16.1 | 0.000677 | 9.6 |
| v1.2 | 1,274 | 1,846 | 25.9 | 0.001082 | 8.4 |
| v1.4 | 1,373 | 1,540 | 23.6 | 0.000942 | 8.1 |

Grade is a spelling-based Flesch-Kincaid approximation on primary text only; short copy makes it noisy. Reused runs were not simultaneous, so latency is descriptive. The newer copy became simpler but not better overall. A v1.4 “six childproofing items” headline ambiguously implied a verified piece count; the source fact is a six-part/category kit.

Current decision: **retain v1.2 as the next working candidate; do not silently change the default loader or rewrite all cards.** The new style/bridge checklists are useful editorial guidance, but their expanded prompts have not earned replacement status. The generation tests covered writing static ads, not validation of every revised workflow or every brand.

Exact comparison/report locations:

- `AD_COPY_PLAYBOOK_COMPARISON.html`, `AD_COPY_PLAYBOOK_RESULTS.md`, `AD_COPY_PLAYBOOK_REVIEW.md`.
- `AD_COPY_OPTIMISATION_COMPARISON.html`, `AD_COPY_OPTIMISATION_RESULTS.md`.
- `AD_COPY_BRIDGE_COMPARISON.html`, `AD_COPY_BRIDGE_RESULTS.md`.
- `AD_COPY_TASK_FIRST_COMPARISON.html`, `AD_COPY_TASK_FIRST_RESULTS.md`.
- `AD_COPY_ITERATION_DECISION.md` gives the latest selection and limitations.
- Raw attempts/prompts/reviews: `data/ad-copy-playbook-test-v1/`, `data/ad-copy-optimisation-v1/`, `data/ad-copy-bridge-v1/`, `data/ad-copy-bridge-v2/`.

## 9. Meta gallery and later Claude work

This is a separate branch of product work that now lives in the same repository. **Do not report it as still just an unconnected top-30 prototype.** Conversely, the handoff has inspected its status/code inventory, not independently revalidated every live number or UI feature.

Initial request: read-only Meta connection; top 30–40 static ads; periods of one/three/six months; spend/ROAS filtering; visual cards and a side panel with campaign, ad set, ad, landing page, spend and demographic/placement breakdowns. The owner initially deferred video/general reference-library work. Later Claude work expanded the gallery beyond that initial scope.

According to the latest `META_GALLERY_STATUS.md` updates, Claude added:

- A working Meta Ads MCP route in Claude at `https://mcp.facebook.com/ads`, for the Gehna account. This is **not the Peach Bucket test brand**.
- A one-year capture with 472 spending ads and 9,294 ad-day rows; creative/ad-set details and monthly age/gender/platform breakdowns.
- All-format gallery, campaign/ad-set views, dates, exclusions, comparison, target-based verdicts, fatigue, CSV export, team notes and client reports.
- Daily/monthly brand sales from a Metabase dashboard, product/category/payment views and comparisons with Meta.
- Competitor snapshots and reference images, with new brands added in the latest update.
- Creative studio/reference-image workflows, AI concept/variant endpoints, and a “tests to run” action plan.

The latest documented test count there was 49; the complete repository's current suite has 148 tests. Historical sections in that file describe earlier smaller versions and sometimes conflict with the current feature set. Read newest updates first, then verify in `meta_gallery/`.

The newly added `CLAUDE.md` further clarifies that Metabase daily data was collected from a signed-in browser because the connector could not read the cards; production access is still pending. It records an existing shared claude.ai gallery artifact and a pending backup-to-Drive task. This handoff did not inspect the live artifact or perform that backup. A shared gallery artifact does not establish production hosting of the complete ecomOS stack.

Main code paths: `meta_gallery/server.py`, `snapshot.py`, `graph_client.py`, `metrics.py`, `view.py`, `themes.py`, `settings.py`, `ai.py`, `share.py`, `web/` and older `static/`. Private captures/cache/media/settings/notes are under `data/meta-gallery/`. `Claude outputs/` contains additional image artifacts; they were not rewritten by the copy work.

Connection status as recorded, not freshly rechecked here:

- Claude MCP authorization worked; Codex's registration flow failed on dynamic-client/CIMD support. Do not assume one client's OAuth grant transfers to another.
- Direct Marketing API had returned API-access-deactivated error 200; later network restrictions also prevented verification. `graph_client check`/`capture` exist, but fresh success must be established before calling automated refresh working.
- The MCP itself offers mutation tools. Prior gallery captures used reads; connector availability does not authorize publishing, pausing or changing spend.
- “Read-only gallery” historically referred to no Meta mutations. The newer local app has settings/notes writes and AI generation endpoints. Inspect current routes, authentication and secrets before hosting it; do not assume the whole server is inert or public-safe.
- Demographic/platform data may be monthly while main date ranges are daily. Preserve aggregation notes and do not add breakdown totals to top-line totals.
- Competitor longevity/version counts are proxy signals; they do not reveal actual spend, ROAS or why an ad worked.
- Recorded media URLs can expire. Check whether images were cached before trying to fetch old signed URLs.

The status file records a previous credential exposure in a tool log and requests key rotation. **No credential values are reproduced here, and rotation completion was not verified.** Confirm that maintenance item privately if continuing the connection work; never ask the owner to paste keys into chat.

## 10. Runtime, credentials and safe operating commands

### Environment

Windows/PowerShell. `pyproject.toml` requires Python 3.11+. The bundled Python used for the latest checks:

```text
C:\Users\kevin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe
```

Optional retrieval dependencies include NumPy and tiktoken. Existing `.runtime/` and `.retrieval-runtime/` contain local dependencies; they are not portable installation instructions. On another machine create a normal Python environment from the declared/actually used dependencies. Drive/provider scripts also use requests, google-auth and cryptography. Do not copy executable runtime folders blindly between machines.

Credentials are in local `.env` and `secrets/`; do not read their values into chat, include them in a bundle, or commit them. `OPENAI_API_KEY` and `DEEPSEEK_API_KEY` are used by benchmark/embedding scripts. Drive uses `secrets/drive-reader.json`. The example env also mentions database and object-storage settings; the active library does not require a provisioned cloud object bucket to be read locally. Confirm code before asking the owner to create services.

Existing ChatGPT/Codex/Claude subscriptions can support work in their own products. They are not substituted for API keys in these standalone Python provider calls. Model IDs and pricing in old reports are historical configurations; verify availability/pricing before a new paid experiment.

### Offline first inspection

Run from the project root:

```powershell
python -m unittest discover -s tests
python scripts/read_playbook.py --directory playbooks/ad-copy-v1.2 --list
python scripts/read_playbook.py --directory playbooks/ad-copy-v1.2 --workflow ad-copy-deployment.write-static-copy
python scripts/search_knowledge.py "Write static ad copy explaining installation support" --domain ad-copy-deployment --keyword-only --token-budget 3000 --max-cards 5
```

The search example intentionally uses keyword-only mode to avoid a new embedding call. It tests the interface, not exhaustive relevance. Do not paste the full 7,611-card file into a chat context.

Current test verification: **148 tests passed on 24 September**. Initial sandbox execution had 12 import errors because it could not read the already-installed local tiktoken file; an outside-sandbox rerun passed without a code change. Do not misreport that as twelve confirmed logic defects. These tests do not validate live connectors, current platform facts, semantic accuracy or conversion performance.

### Commands with side effects: inspect before using

| Command / module | Effect |
|---|---|
| `scripts/build_library.py` | Prepares/rebuilds local extraction manifests/exports; without `--execute` it is not a paid bulk run, but it still writes local artifacts. |
| `scripts/build_library.py --execute --folder NN` | Paid processing of incomplete/current-version sections in that folder; do not rerun everything for handoff. |
| `scripts/library_embeddings.py` | May call OpenAI for missing vectors and update caches/index artifacts. |
| `scripts/build_knowledge_metadata.py` | Rebuilds metadata with matching labels preserved/fallbacks for changed content. |
| `scripts/classify_knowledge_labels.py` | Paid resumable label classification; inspect existing stage cap/cache first. |
| `scripts/build_playbooks.py` | Builds a new scaffold; does not preserve all manual editorial changes from another version. |
| Benchmark generation/review scripts | Paid API calls, stage/global reservations, saved payloads and responses. |
| `python -m meta_gallery.snapshot` | Rebuilds local gallery cache from raw captures. |
| `python -m meta_gallery.server` | Runs local gallery at 127.0.0.1:8765; inspect current AI/write routes before exposing it. |
| `python -m meta_gallery.server --prefetch-images` | Downloads media to local cache. |
| `python -m meta_gallery.graph_client check` / `capture` | External Meta API reads; credentials/access/network must work. |

Do not run these merely because they appear in a handoff. The current request was documentation, not permission to restart paid processing, publish the app or mutate business accounts.

## 11. Spending, transport and Git boundaries

`intelligence/budget.py` stores integer micro-dollar reservations in SQLite. Requests reserve an upper bound before dispatch, settle from returned usage and retain reservations for uncertain outcomes. Reopening a ledger cannot raise its persisted cap. A bound overrun halts dispatch by lowering the working limit. These controls cover cooperating scripts, not all tools or an entire provider account.

Latest local global snapshot during handoff:

- Settled estimate: **$42.168606** across 1,847 entries.
- Reserved/uncertain: **$17.466431** across 37 entries.
- Combined ledger commitment: **$59.635037**.
- Working/absolute caps: **$160 / $200**.

Use the timestamped JSON snapshot if files change. These are not invoices or account balances. Stage ledgers often record the same calls as the global ledger; **do not sum them all**. Built-in image generation had unexposed cost, and later external/Claude gallery calls may use different accounting. The two latest copy cycles together cost about $0.1454, not an additional $0.1454 to add again to the global total.

Important implementation files: `scripts/calibration_client.py`, `http_worker.py`, `bounded_process.py`, `run_peach_web.py`, `optimise_ad_copy.py`, `intelligence/budget.py`. Calls use bounded transport, cached identities, saved raw outputs and conservative reservations. Never clear a reservation just to unblock a run. Reconcile it with provider usage or confirmed request outcome. Do not replay a timed-out request assuming it was free.

Historical malformed JSON-format requests occurred because the user input needed the word JSON; corrected manifests were saved separately. Do not overwrite those failed-attempt logs or count a locally repaired JSON bracket as an untouched provider output.

### Git/storage warning discovered during handoff

The old repository policy kept `data/`, raw sources, credentials and private cards outside Git. During handoff preparation the working `.gitignore` no longer contained `data/` and explicitly unignored `data/**/*.sqlite`. Another session first staged and then committed the data in `c403d0d`. The final local snapshot found **6,838 data files in HEAD and no staged files**. The handoff process did not stage or commit them. Therefore older statements that the data is excluded from Git no longer describe this checkout.

Before committing/pushing, inspect both the working tree and staged index, distinguish `git ls-files` from files actually present in HEAD, and preserve the owner's intended private-data transfer policy. A private repository is not the same as a secret store or authorization to expose customer/source data publicly. Do not silently revert another session's changes or issue `git add .`. No Git push, remote privacy change or credential rotation was performed by the handoff process. A credential audit of all 6,838 newly committed data files was outside this documentation task; the documentation bundle received its own allowlist and credential-pattern checks.

## 12. Known gaps and mistakes to avoid

1. **Source coverage is structural.** Every source has cards, but no exhaustive human recall audit proves every valuable idea was captured.
2. **Currentness is not guaranteed.** No automatic freshness verifier checks all platform claims; labels are not validation dates.
3. **Applicability remains incomplete.** Correct category does not mean correct product, offer, audience, evidence or budget.
4. **Do arithmetic deterministically.** Cards do not prevent margin, funnel-rate or resource-allocation mistakes.
5. **No universal retrieval win.** Some tasks/models improved; others regressed. Added context can increase input cost, reasoning cost and latency.
6. **AI scores are unstable.** Keep exact outputs and use owner preference; do not optimize only to the judge.
7. **Do not overcompress.** Removing conditions/substeps can remove the actual useful guidance. Whole-card context is intentional until selective extraction is validated.
8. **Do not overexpand.** Huge master prompts and all-topic context do not replace good task selection.
9. **No verified autonomous execution.** Drafting a campaign-change JSON is not evidence that live tool execution is safe or complete.
10. **Do not conflate brands.** Peach Bucket copy/economics, fictional TrailFold tests and Gehna gallery data are separate.
11. **Do not call competitor ads proven winners.** Without actual performance data, visual analysis and longevity are hypotheses/signals.
12. **Do not assume product image fidelity.** Generated mockups can redraw the actual product; use locked originals where accuracy matters.
13. **Do not rebuild all playbooks from the scaffold generator over manual versions.** Versioned editorial changes need deliberate migration.
14. **Do not treat older 'not implemented' lists as current.** Semantic retrieval, labels, playbooks, commits and the Meta gallery were added after some old READMEs.
15. **Do not treat later gallery status as independently audited here.** Verify its live connections, current code and security before production use.

## 13. Recommended next work, subject to the owner's chosen direction

The last recommendation to Kevin was to use human preference to improve one real workflow, rather than conduct another broad AI-scored tournament.

### Immediate continuation for the intelligence/copy track

1. Read the final copy comparison and v1.2. Confirm the actual copy, not just its score.
2. Ask for two or three liked and disliked outputs with brief reasons, or accept existing feedback/examples if available. Do not request new credentials for this step.
3. Build a compact, versioned Peach Bucket writing brief: product facts, approved claims, actual offer, customer hypothesis/evidence, voice examples, desired outcome and exclusions. Keep uncertainty outside customer-facing copy unless material to the claim.
4. Load one task playbook. Retrieve extra cards only when a concrete writing decision needs them, including conditions. Record what was selected and why in a concise audit record, not private reasoning.
5. Produce three new realistic requests as finished ad copy. Let Kevin judge whether he would use them and how much editing is needed. Keep the same facts across any comparison.
6. Route feedback correctly: wrong product fact → brand record; voice preference → brand overlay; irrelevant guidance → selection; repeated general process issue → proposed playbook revision.
7. Build a simple internal draft interface after that loop works: request + brand context → playbook → relevant cards → output → edit/feedback log. This interface is not yet completed for the general intelligence workflow.

Suggested acceptance criteria: no unsupported claim or fixed-offer violation; complete requested artifact; natural audience-specific language; a credible feature/benefit connection; distinct useful variants; owner can use it with little editing. Track time-to-acceptable-output as well as model cost/tokens. Numeric AI score alone is not the acceptance gate.

### Other tracks already discussed

- Brand brain: persistent fact/voice/evidence records, approval/versioning and integration with business systems.
- Data layer: normalized reporting definitions, dates, currency, attribution, missingness and deterministic calculations.
- Reference library: initially statics, emails and landing pages; retain assets plus structured searchable descriptions; deep analysis can be on demand. General video ingestion was deferred, even though the separate gallery later gained video views.
- Experiment memory: preserve hypothesis, context, asset versions, prior attempts, result and interpretation; distinguish “never tried” from “tried under a different condition.”
- Agent layer: task-specific procedures with input/output contracts, permission boundaries and observable tool results. Draft mode before consequential actions.

Do not present these as already integrated. Confirm which track Kevin wants Claude to take next and then work on that concrete scope without repeating setup that is already done.

## 14. How to transfer this project to Claude

### If Claude has local filesystem access

Give Claude the project root and paste `CLAUDE_START_HERE.md`. It should read this handoff, the snapshot and the referenced current reports, then inspect relevant code. It should use paths/search tools to retrieve cards; it should not try to fit the full card corpus into its own chat context.

### If Claude only has file uploads/chat access

Upload `CLAUDE_HANDOFF_BUNDLE.zip` if supported, or upload this Markdown document and `HANDOFF_PROJECT_SNAPSHOT.json` individually and paste the start prompt. The bundle contains handoff documents and historical report evidence. **It is not the full repository or card database, and it contains no API keys.** Tell Claude it must distinguish reading the handoff from having executable access to the project.

For actual retrieval/implementation, separately provide the private repository plus the required local data through an appropriate private filesystem/storage channel. Minimum retrieval data: `cards.json`, `metadata.json`, `vectors.json`, `search.sqlite`, corresponding code and dependencies. Full ingestion provenance additionally needs snapshots/manifests. Audit whether staged data actually reached Git; do not assume a repository clone contains ignored or uncommitted artifacts.

On another machine, local Windows paths and signed media URLs may not work. Preserve relative project structure, install dependencies and use secrets locally through a credential manager or `.env`; never upload credential files as context.

## 15. Handoff verification and provenance

This document was prepared from the conversation and inspected local code, manifests, reports, canonical card files, Git metadata and read-only budget queries. The canonical library hash/counts were checked, and the 148-test suite passed outside the sandbox. No paid model calls, Drive refresh, Meta mutations, deployment or Git push were performed for this handoff.

The snapshot lists hashes/sizes of the report evidence available at preparation time. Historical reports retain their own dates, models, configurations, limitations and measured costs; they have not been rewritten to make the experiments appear uniformly successful. Later Claude gallery work is explicitly attributed to its existing local status record.

The useful foundation to preserve is: **expert cards + compact retrieval + versioned task procedures + real brand facts + owner feedback**. The next implementation should turn that into a usable deliverable, while measuring what helps rather than assuming that more context, more rules or more AI reviewing must improve it.
