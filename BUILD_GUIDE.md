# Ecommerce intelligence layer: full-library build guide

Prepared 22 September 2026. Scope: build the reusable intelligence layer for the entire available library, with ongoing additions and refreshes. Business integrations, a visual reference library and agents that change live campaigns come later. This guide distinguishes the working local foundation from remaining production implementation.

## 1. The architecture we are building

The eventual system has four cooperating layers and one shared brand context:

| Component | Stores | Responsibility |
|---|---|---|
| Business data | Orders, margin, inventory, attribution, ad performance, experiments | Establish what is happening and what can be measured |
| Intelligence | Source evidence, conditional cards, conflicts, playbooks | Explain which actions might work, under which conditions, and why |
| References | Creatives, landing-page sections, offers and annotated examples | Supply relevant examples without treating appearance as proof of performance |
| Execution | Versioned skills, tools, workflows, approvals and action logs | Diagnose, plan, draft, execute authorized actions and measure outcomes |
| Brand context | Products, audience evidence, geography, claims constraints, positioning, resources and goals | Make every recommendation specific to the business |

The intelligence layer should be a queryable service, not a giant system prompt. Agents request knowledge for a specific decision; the service returns a bounded evidence packet, unresolved conditions and citations. A future orchestrator delegates by task and permissions. The 23 categories are a taxonomy; they do not require 23 always-running agents.

For example: a CRO workflow asks for product-page interventions given mobile traffic, measurement readiness and product characteristics. The service returns applicable actions and prerequisites. If the data cannot support a diagnosis, the workflow requests the missing information instead of inventing a strategy. The same principle applies to a new store and a $100m store; revenue alone is an inadequate applicability filter.

## 2. Drive versus local versus GitHub

**Keep Drive. You do not need to download and reorganize the entire folder manually.** It remains your convenient source collection interface. The production connector copies immutable versions into private object storage and records original Drive IDs, URLs, timestamps and hashes. Parsing and indexing operate on those snapshots. Your originals remain unchanged.

Use GitHub for code, schemas, prompts, taxonomy versions, synthetic tests and deployment configuration. Use Postgres for metadata, source/version relationships, cards, review queues and retrieval indexes. Store documents and images privately in object storage. Do not commit books, transcripts, customer records or secrets to GitHub.

A local export is a fallback if unattended Drive access is unavailable. It must preserve a manifest mapping files to stable source IDs and Drive links; filenames alone are unreliable identities. The local foundation already accepts DOCX/TXT/Markdown. The existing ChatGPT Drive connection permits assisted inspection but does not automatically provide credentials for your deployed worker.

Recommended first hosted shape: one Python worker and API, Postgres with full-text search and pgvector, private object storage, a small review interface, and a durable jobs table. Supabase can supply Postgres, auth and storage initially. A separate graph database or vector service is unnecessary for this library size; relationships fit ordinary tables.

## 3. What the inspected library tells us

The available inventory contains **256 source DOCX files**, rather than 350 verified sources: 23 domain folders plus a multi-domain folder and supporting folders, 25 readmes, seven templates and five root control files. This is an inventory snapshot, not a claim that all documents have been read. Eight documents were sampled in the earlier review.

The sample contains useful original content mixed with generated analysis and metadata. Problems include missing original URLs/dates, conflicting headers, routing inconsistencies and an outdated ingestion count. Therefore, headers and folder names are classification hints, not trusted evidence. A source can belong to multiple categories. Longer documents need section-level processing; at least one sampled transcript is exceptionally long.

First reconcile the full manifest, including pagination, nested folders, unsupported types, duplicates, permission failures and deleted/moved files. If more sources exist outside this root, include their roots before calculating final coverage. Do not silently equate “293 total files” with “293 knowledge sources.”

## 4. Build sequence and responsibilities

These are stages of one full-library build. Evaluation uses selected passages, but the product scope remains the entire library.

| Stage | Implementation and output | Needed from you | Completion condition |
|---|---|---|---|
| 1. Access and inventory | Read-only Drive connector; complete manifest; source registry and exception ledger | Root folders; confirm which content can be used in a commercial client product; GitHub sign-in | Every discovered item has an identity and disposition |
| 2. Snapshot and parse | Immutable source versions; headings, paragraphs, tables, links and media references; parser diagnostics | Resolve inaccessible or corrupt files; supply originals where available | Every source is parsed or explicitly held with a reason |
| 3. Normalize and classify | Separate original text from annotations; repair metadata in derived records; multi-label taxonomy | Confirm business vocabulary and any source trust exceptions | No generated commentary silently treated as original evidence |
| 4. Extract candidates | Section-level principles, procedures, diagnostics and examples; evidence spans and conditions | A few examples of what you consider excellent actionable advice | Each candidate has provenance or an explicit unsupported status |
| 5. Verify and reconcile | Independent evidence review, deterministic checks, duplicate families, conflict records | Review uncertain/high-impact examples and source rights questions | Unsupported claims cannot enter the approved retrieval index |
| 6. Publish and compose | Versioned approved cards; compact projections; dependency-aware playbooks | Choose initial policy for automatic versus human publication | Every published record satisfies policy and has a review date |
| 7. Retrieve and evaluate | Hybrid search, metadata filters, reranking, conditional context packets, citation expansion | Representative questions and correct/incorrect outcomes | Held-out retrieval/actionability targets pass |
| 8. Operate continuously | Changes feed, retries, spending controls, review dashboard, backups, freshness and drift tests | Hosting/project access and operating budget | A source update can propagate safely without rebuilding everything |

Do not wait for perfect metadata to parse a source. Keep uncertain fields null, process the usable material, and hold claims whose provenance is insufficient. Likewise, a failed source should not stop other sources; coverage reports must expose the gap.

## 5. The ingestion pipeline in detail

1. **Discover.** Crawl all folders; persist parent relationships, MIME type, file ID, modified time, size, permission disposition and intended scope. Capture a Drive change token before the crawl and reconcile changes after it to avoid a moving snapshot gap.
2. **Version.** Download/export supported content; hash bytes and normalized content separately. Store raw snapshots immutably. Reuse unchanged parsing results. Record parser/model/prompt/schema versions so a code change can invalidate derivatives without pretending the source changed.
3. **Parse.** Preserve document order, headings, table structure, link destinations and media anchors. DOCX normally needs no paid OCR. OCR only image-based pages; transcribe only actual audio/video. Never quietly omit failed tables or images: flag them for a separate parser/review path.
4. **Separate origin.** Identify original transcript/article passages, generated summaries, editorial notes and metadata. Keep all of them, but do not let a summary verify itself. Source trust, evidence strength and freshness are separate fields.
5. **Segment.** Begin with coherent sections of roughly 1,500–3,000 tokens, with small contextual overlap and heading ancestry. Bound individual calls; retrieve adjacent passages or related sections when necessary. Track which spans were processed so no middle section disappears. Chunking is an evidence-processing strategy, not the final knowledge unit.
6. **Classify.** Assign multiple domains, task types, channels, objective, maturity prerequisites and evidence type. Folder labels contribute a prior only. Unknown or proposed tags go to a controlled taxonomy queue instead of creating unlimited near-duplicate categories.
7. **Extract.** Produce the smallest complete knowledge unit: one decision/action with its conditions. Do not enforce a card quota per document. Distinguish principle, diagnostic, procedure, example and measurable claim. A book may support many cards; a repetitive transcript may support very few.
8. **Verify.** Check schema, exact evidence spans, attribution and numerical fidelity programmatically. A second model checks entailment, qualifications and unsupported generalization against original passages. A current-platform check is a separate job using official documentation when needed; expert reputation does not establish present-day validity.
9. **Reconcile.** Use hashes and normalized text first, embeddings for duplicate candidates second, model adjudication only for uncertain pairs. Group semantically related cards without destroying distinct conditions or independent citations. Retain conflicting advice as alternatives with applicability and evidence, not a fabricated consensus.
10. **Publish.** Save validated versions and compact views atomically. Human-review uncertain/high-impact cases. Initially audit a stratified sample from every domain, source type and extraction model. Automation can expand after measured performance; do not require you to manually approve thousands of easy records forever.
11. **Refresh.** Process source changes and removal events, retire affected evidence/cards, rebuild only dependent playbooks and indexes, and run targeted regression tests. Periodic full reconciliation catches missed events and folder moves. A metadata-only rename should not trigger a paid full re-extraction. Do not advance the sync checkpoint until its jobs are durably recorded.

Suggested states: discovered → snapshotted → parsed → extracted → verified → approved → indexed, with explicit held, failed, stale and retired branches. Jobs have deterministic idempotency keys, attempt limits, retry backoff and a dead-letter queue. Keep the last approved knowledge version available only if policy permits and clearly marks its freshness; never present retired evidence as current.

## 6. Knowledge records and compact context

Maintain separate records: Source, SourceVersion, Passage, Claim/CardVersion, EvidenceLink, ConflictSet, PlaybookVersion, ProcessingRun, ReviewDecision and RetrievalTrace. A card is not the raw chunk, and a playbook is not a new uncited source.

Production card fields should include:

- Stable family ID and version ID; title, type, scope and category tags.
- Claim and concrete action; expected output; required inputs.
- Applies-when predicates, exclusions, missing-input behavior and dependencies.
- Measurement/stop criteria where supported; clearly labeled proposed implementation details otherwise.
- Evidence references to source version and exact locators; independent support/counterevidence links.
- Evidence type, limitations, uncertainty, source date, verified date and next review date.
- Publication status, extraction/verification provenance and supersession relationships.

Use typed applicability fields such as channel, market, business model, product restrictions, measurement readiness, inventory constraints, available resources and validated sample size. Do not ask a language model to infer that absent brand data is true. The local scaffold currently implements simpler equality predicates; complex ranges/AND/OR logic remain a production task.

Build three views from the same approved record:

| View | Starting size target | Purpose |
|---|---:|---|
| Discovery | 40–60 tokens | Title, action category, main applicability and ID for ranking |
| Execution core | 150–250 tokens | Action, essential conditions/exclusions, required inputs, evidence IDs and uncertainty |
| Expanded evidence | 400–800 tokens, or explicit longer allowance | Detailed procedure, supporting passages, qualifications and conflict resolution |

These are targets, not reasons to delete meaning. If a safe core cannot fit, split a multi-action record or retrieve a larger complete packet. Never truncate exclusions, qualifications or dependencies to meet an arbitrary card size.

Retrieval flow: authenticate tenant → determine task and missing facts → filter authorized/fresh/approved records → keyword plus vector candidate search → merge candidates → rerank for applicability and evidence → resolve conflicts and dependency closure → pack within the task's budget → return evidence IDs, omitted reasons and missing questions. Fetch expanded evidence on demand.

Start with 3–6 execution cards and roughly 2,000–3,000 knowledge tokens per narrowly scoped task, then measure. A large strategy should be decomposed into decisions, each with a focused packet. Reserve separate budgets for system instructions, brand facts, tools and model output. Log actual provider tokens and cost. Never retrieve “all Meta Ads cards” simply because an agent has that role.

The future skills registry stores each skill's objective, accepted input schema, required knowledge queries, tools, permissions, output schema, evaluation suite and version. Skills consume the same retrieval API. Adding a skill should not require rebuilding the corpus; adding a source should not require rewriting agent prompts.

## 7. Models by task and why

These are **starting candidates**, not claims of a benchmark-proven best model for your documents. Prices were checked on official pages on 22 September 2026; confirm availability, API identifiers and pricing in your account before paid execution. Numbers below are USD per million input/output tokens, standard uncached text rates.

| Task | Starting choice | Input / output | Routing rule |
|---|---|---:|---|
| Manifest, hashing, DOCX parsing, exact quotes and schema checks | Deterministic code | No model charge | Never use an LLM for work code can verify exactly |
| Domain classification, header repair suggestions, duplicate-pair screening | GPT-5.6 Luna | $0.20 / $1.20 | Escalate ambiguous or conflicting cases |
| Evidence-grounded extraction | Claude Sonnet 5 | $2 / $10 | Compare with Terra and Gemini on the actual corpus before locking in |
| Independent evidence verification | GPT-5.6 Terra | $2 / $12 | Use original evidence; disagreement goes to adjudication |
| Hard conflicts and playbook synthesis | GPT-5.6 Sol | $4 / $20 | Only a minority of records need this stage |
| Rare unresolved complex adjudication | GPT-6 Astra | $10 / $50 | Optional; manual review may be more valuable |
| Search embeddings | text-embedding-3-small | $0.02 / — | Embed approved views and useful evidence once per content version |
| Lower-cost extraction challenger | Gemini 3.8 Flash | $0.75 / $3.75 | Promotional rates through 31 December 2026; quality must pass the same gates |

Sources: [OpenAI pricing](https://developers.openai.com/api/docs/pricing), [embedding model](https://developers.openai.com/api/docs/models/text-embedding-3-small), [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing), [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing). Sol pricing is promotional with availability stated at least through 21 November 2026. Gemini 3.8 Flash rises to $1.50/$7.50 on 1 January 2027 under the listed schedule. Batch discounts may halve eligible text processing charges, at the cost of asynchronous completion and provider constraints.

If you want one vendor initially, use Terra for extraction and verification and Sol only for escalation; operational simplicity may outweigh a small API-price difference. Independent models reduce some shared mistakes but do not guarantee correctness. Do not pay for two models to verify every trivial classification: spend verification on published claims.

Evaluate candidates on a stratified set of passages across all domains, long documents, tables, mixed-origin text and conflicting recommendations. Score quote fidelity, claim support, preserved conditions, actionable completeness, duplicate behavior, abstention and cost per accepted card. Keep a held-out set. Choose the cheapest model that passes these gates; low cost per raw token is not the same as low cost per useful card.

## 8. Approximate initial cost

Planning workload: **350 sources × 30,000 raw tokens = 10.5 million raw tokens**. This is not a measured token count of your Drive. Extraction includes 25% repeated context; output estimates include billable reasoning where applicable. Different vendors tokenize the same text differently, so the following is a budgeting approximation.

| Stage | Aggregate input / output assumption | Standard model cost |
|---|---|---:|
| Classification | 2.10m / 0.175m | $0.63 |
| Extraction | 13.125m / 2.80m | $54.25 |
| Evidence verification | 8.40m / 1.40m | $33.60 |
| Difficult cases: 20% of sources | 0.84m / 0.14m | $6.16 |
| Duplicate screening | 2.80m / 0.175m | $0.77 |
| 100 playbook compositions | 0.80m / 0.20m | $7.20 |
| 200 evaluation cases | 1.20m / 0.20m | $4.80 |
| Embeddings | 13.30m input | $0.27 |
| **Total** | | **$107.68** |
| **With 30% contingency** | | **$139.98** |

If all modeled text stages qualify for 50% batch pricing, the same scenario is about **$70.16 including contingency**. Single-provider Terra extraction is about **$147.26 including contingency**. Gemini extraction at the listed promotional rate is about **$95.90 including contingency**, assuming equal output volume and acceptance rate—which must be tested.

Output volume is a major sensitivity. These assumptions allow 8,000 billed extraction output tokens per source, not unlimited cards. Dense books, many supporting quotes, retries and poor verification acceptance can substantially increase cost. Run the estimator with measured tokens, output yield and verification scales after parsing; impose a hard run budget before inference. A reserve is not a spending limit.

Formula: cost = sum(input_tokens × input_rate + billed_output_tokens × output_rate) / 1,000,000, plus external tools. For 20 new sources at the baseline density, proportional source stages are about $5.47 before contingency and before additional playbooks/evaluation; do not rerun the whole library. Changed shared rules may legitimately trigger a broader evaluation run.

These estimates exclude engineering, human review, taxes, paid search, OCR, transcription and production agent usage. Initial manual review hours should be estimated from measured throughput: review_count × minutes_per_record / 60. For example, 500 records at two minutes each is about 17 hours, not a model bill.

For hosting, budget approximately $40–$100/month for a small initial deployment; this is a planning allowance, not a vendor quote. [Supabase Pro starts at $25/month](https://supabase.com/pricing); workers, backups, logs and overages need separate allowance. Local development can start without hosted infrastructure. No API calls have been paid for by this scaffold.

## 9. Quality gates and “finished” criteria

Full ingestion is finished when every discovered source has a recorded outcome, not when every source has produced cards. The first production release should have:

- A reconciled manifest and visible failures/holds; zero silently skipped sources.
- All published cards linked to source versions and resolvable evidence spans.
- Zero known unsupported numerical promises in the held-out release set; a documented human audit of entailment and conditions.
- Measured retrieval performance on representative questions; initial targets of at least 90% recall@10 for expert-labeled relevant cards and at least 95% supported claims in audited responses, adjusted after baseline measurement.
- Reliable abstention when prerequisites are missing or competing evidence cannot be resolved.
- No cross-tenant disclosure in access-control tests. User-supplied scope strings are not production authorization.
- Source update, deletion, revocation, retry, interrupted-job and budget-exhaustion tests.
- A successful backup restore and a reproducible knowledge release with model/prompt/schema versions.

These are proposed acceptance targets, not achieved measurements. A high aggregate score cannot excuse a serious source attribution or access failure. Store test failures and affected domains, not only a single overall percentage.

## 10. What exists now and the next handoff

The accompanying code implements an offline staging store, basic parsers, immutable versioning, evidence and publication checks, scope filtering, conditional dependency-aware packet assembly and cost estimation. Twelve automated tests pass. It has not downloaded/converted all 256 sources, run provider extraction, built semantic retrieval, deployed a service or published a GitHub repository.

The next production work is: connect Drive → finish parser coverage → measure the entire corpus → implement queued model extraction/verification and spending limits → add review/publication UI → implement hybrid retrieval and evaluation → run the full corpus → deploy refresh and monitoring.

Needed from you now:

1. **GitHub:** sign in so the authorized private `ecom-intelligence` repository can be created; specify an organization only if you prefer it to your personal account.
2. **Model access and budget:** identify available providers and the maximum first-run spend. Do not paste keys into chat; place them in local environment variables or the deployment secret manager. ChatGPT/Claude subscriptions are separate from API billing.
3. **Drive runtime access:** choose an owned Google Cloud project and authorized OAuth flow, or a service account with explicit read access to the intended folder. Configure access deliberately; the connected chat session is not unattended runtime authentication.
4. **Content scope:** confirm this is the complete root and identify material restricted from commercial/client use. Public availability and your ability to read a book do not automatically establish redistribution rights; keep source access and client-visible quotation policy separate.
5. **Quality direction:** supply 15–30 representative business questions and, where possible, what a useful answer would contain. This is an evaluation set for the full build, not a restriction to those sources.

No manual folder cleanup is required before proceeding. Most normalization belongs in derived metadata, preserving your original files and making future additions easy.

Implementation references: [Drive changes](https://developers.google.com/workspace/drive/api/guides/manage-changes), [Drive authorization](https://developers.google.com/workspace/drive/api/guides/api-specific-auth), [structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs). Structured output validation controls shape; it does not establish factual accuracy.
