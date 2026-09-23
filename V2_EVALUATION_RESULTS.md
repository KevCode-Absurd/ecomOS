# Revised intelligence units and agent evaluation

Completed 2026-09-22. The revised representation is implemented and tested. It improves evidence handling and reduces the context needed for selected tasks, but the agent comparison has not demonstrated a differentiated, production-ready operating system. Some decisions remained generic, and one card-assisted recommendation became too eager to act.

## What is built

- Typed action, principle, example, warning and unresolved-claim units.
- Separate claims, actions, triggers, prerequisites, exclusions and completion criteria, each with exact evidence where supplied.
- Nested ALL/ANY condition groups; ungrounded and ambiguous quote anchors are held.
- Local evidence offsets bound to source ID, version hash and paragraph/table locator.
- Candidate staging checked against downloaded source snapshots. No automatic publishing or conversion into execution permission.
- Persistent follow-up tasks for missing coverage, unresolved context, quote repairs and semantic review.
- A source catalog for all 256 parsed documents, with Drive references and separate folder/header hints.
- A six-scenario development comparison using no library, raw text and model-reviewed cards.

Core tests: **46 passed**. V2 units remain separate from the older approved-card store; production retrieval and publishing integration are not complete.

## Extraction comparison on the three annotated cases

Same three excerpts and revised prompt. DeepSeek's first high-reasoning attempts ran out of completion allowance before returning JSON; they were confirmed truncated outcomes, not unknown network failures.

| Configuration | Completed outputs | Units passing field-evidence checks | Units held by those checks | Booked cost |
|---|---:|---:|---:|---:|
| DeepSeek, no thinking, 16,384 allowance | 3/3 | 36 | 10 | $0.0190 |
| DeepSeek, high, 16,384 allowance | 0/3 | 0 | No usable output | $0.0621 |
| DeepSeek, high, 32,768 allowance | 3/3 | 48 | 0 | $0.0894 |
| Terra, high, 16,384 allowance | 3/3 | 47 | 1 | $0.2871 |

These are source-location/structure checks, not semantic accuracy or recall scores. The larger-cap experiment changes the allowance, so it is not a strictly matched comparison on that parameter. The low/no-thinking outputs completed below their caps. Evidence-binding success does not mean every condition or relationship is correct.

**Working choice for further extraction:** DeepSeek high with enough completion capacity; use Terra for comparison, difficult reviews and fallback. Do not lock production routing yet. The experiment supports spending more reasoning on this richer contract, rather than defaulting to no thinking solely for cost.

## Wider 24-excerpt test and staging

DeepSeek high at the larger allowance completed 23 excerpts. Its security-excerpt connection failed before a usable response was received; its outcome remains unknown and it was not retried. A separate Terra-high call completed that excerpt. The resulting 24-source staging manifest is therefore mixed-provider, **not a claim of 24/24 DeepSeek success**.

The staging pass persisted **369 units** with verified local evidence offsets: **316 candidates** and **53 held units**. Held units include response-level dependency/relationship problems found during revalidation. Other units that failed evidence binding remain in their original response artifacts for repair rather than being silently discarded. All candidates still require semantic review; none are approved.

There are **84 pending follow-up tasks**, including further extraction where the output cap left more material, evidence repair, source-context checks and semantic/coverage review. No excerpt is marked independently complete. This is a calibration set, not processing of all 256 documents.

The contract also risks over-fragmentation: a meaningful task such as writing a research-backed hypothesis can become several tiny units. Before bulk ingestion, establish task-sized cards and linked substeps so an agent does not need to retrieve many fragments to perform one job.

## What changed for the agent

Eighteen decision runs completed: six synthetic scenarios times three context conditions. Expected answers were withheld. Relevant sources were preselected, so this tests representation, not search quality. Seventeen units were model-reviewed for the curated packets, with four logged corrections; this is not an independent human evaluation.

- Gift and cross-platform ROAS decisions were largely similar with and without the library.
- Supplied knowledge shifted CRO measurement toward revenue per visitor/session.
- Curated context produced a conditional factorial-testing path for the higher-volume brand, while other conditions initially rejected the proposed broad test.
- The curated within-platform ROAS answer recommended a budget shift before resolving important missing facts. This is a regression to fix.
- Compact subscription packets omitted helpful delay/skip guidance that remained available in the raw excerpt. Compactness must preserve relevant dependencies.

Reviewed packets used **37.27% fewer total prompt tokens** than raw excerpts, or approximately **41.77% fewer library-context tokens** after subtracting the no-library baseline. Their API cost was about **14.5% lower** in this small test. Three curated responses exceeded the requested 350 words, versus none in the other conditions. Lower input size does not automatically produce a shorter or better answer.

No decision-quality win rate, production accuracy, general cost ratio or business uplift is claimed. See `AGENT_EVALUATION_REVIEW.md` for the case-by-case findings and limitations.

## Source routing

The local catalog covers 256 documents. It detected **56 folder/header routing disagreements** and explicit plaintext header URL fields in **29 documents** within the opening text inspected. These are discovery hints, not proof of category errors or missing URLs elsewhere. Source authorship has not been independently verified. Use content-level classification and preserve Drive references rather than routing every card by folder name.

## Spend and remaining work

This phase: **$1.263518 recorded usage**, plus **$0.044807 retained reservation** for the interrupted DeepSeek call; **$1.308325 committed** against the shared $5 stage ceiling. All calibration to date: **$2.054157 recorded usage**, or **$2.098964 including that reservation**. These use configured conservative rates and are not provider invoices. There is one unresolved request outcome; no automatic resend or release of its reservation occurred.

Before full-library processing: repair evidence/relationship errors, implement actual continuation and deduplication, group inseparable substeps into useful task cards, preserve relevant warnings/dependencies during retrieval, and test an explicit missing-facts gate before consequential recommendations. Then evaluate harder, unseen brand cases. The current six cases must not become a claimed holdout after tuning against them.

No additional account or hosting setup was needed for this phase. Raw sources, credentials, API artifacts, staged units and private review anchors remain outside GitHub in ignored local storage.
