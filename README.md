# Ecommerce intelligence layer

## Current workflow — September 22

The active text-only card workflow is described in [LIBRARY_WORKFLOW.md](LIBRARY_WORKFLOW.md). It supersedes the older per-claim approval requirements below. CRO and product research have been converted into practical cards; private outputs and progress live in `data/library-v3/`. Use `scripts/build_library.py` to resume remaining folders, `scripts/library_embeddings.py` to refresh semantic search, and `scripts/search_library.py "your task" --brand-context "known facts"` to retrieve a bounded context packet. Runtime agents can use frontier or economical models with this same knowledge.

The remaining sections below document the earlier foundation and experiments; their old publication gates are not prerequisites for the active internal library.

A local, single-user foundation for converting a growing ecommerce source library into traceable, conditional knowledge. All 293 library files have been snapshotted; 256 source documents were parsed and 37 supporting files retained. Knowledge extraction and semantic quality review are still in calibration. This is not a deployed platform or a published knowledge library.

## Run

Python 3.11+. The core store uses the standard library; Drive/model scripts also require the locally installed dependencies in ignored `.runtime/` (requests, google-auth and cryptography), and token measurement uses tiktoken. Run from this directory:

```powershell
python -m unittest discover -s tests -v
python -m intelligence.cli estimate --sources 350 --raw-tokens 30000
python -m intelligence.cli estimate --sources 350 --raw-tokens 30000 --batch
python -m intelligence.cli ingest-local path/to/source.docx --source-id stable-drive-file-id --scope global
```

Local ingestion stores immutable raw bytes and paragraph/table passages under ignored `data/`. Newly imported material is unreviewed. It does not become approved knowledge automatically. Use `Store.review_source`, `Store.classify_origin`, `Store.add_card`, and `Store.approve_card` from an integration or review interface. Tests demonstrate these calls using synthetic text only.

## Implemented

- DOCX, TXT and Markdown parsing; DOCX table text and media inventory.
- Stable source/version identities and idempotent ingestion.
- Source snapshots, evidence locators, exact quote checks and source-origin labels.
- Explicit source-use review, card approval, expiry and source-change invalidation.
- Scope checks; condition and dependency checks during context packing.
- Lexical retrieval baseline with bounded complete-card packets.
- Read-only Drive inventory and immutable downloads, corpus audit and lossless evidence segmentation.
- Explicit opt-in model calibration, persistent spending reservations and diagnostic reports.
- AND/OR/NOT, numerical ranges, strict equality and unknown-fact handling in condition evaluation.
- V2 units with field-level evidence, action/principle/example/warning distinctions, and snapshot-checked local staging.
- Development comparison of an executor with no library, raw excerpts and reviewed knowledge packets.
- Reproducible model-cost scenarios, with independent output and verification volume controls.

## Not implemented yet

Continuous Drive change reconciliation, semantic entailment verification, independently verified origin classification, semantic search, compact card projections, production tokenizer integration, full extraction jobs/continuation, review UI, production tenant authentication/RLS, hosted deployment, and production monitoring. Paid calibration requires an explicit execution flag; it never publishes cards. The bulk inference environment flag remains disabled.

UTF-8 byte counting is a conservative development budget, **not measured tokens**. Production must inject the target model's tokenizer or count API and reserve room for system instructions, brand facts, tools and output. Source quote matching proves the quote exists, not that it supports the claim; independent evidence verification and human evaluation remain essential.

Reviewed conditions support equality dictionaries and explicit logical expressions. Missing facts remain unknown. Production still needs governed fact definitions, units/currencies and field-level source evidence. Never silently translate a complex source condition into a simpler one. The `op` key is reserved for expressions; a fact named `op` must use an explicit equality predicate.

## Repository policy

Keep code, schemas, prompts and synthetic evaluations in GitHub. Keep source documents, private cards, credentials and customer data in private storage. `data/`, `.env` and secrets are ignored. The user created the private repository `KevCode-Absurd/ecomOS`; a push from this workspace is not yet verified.

Read `BUILD_GUIDE.md` for the full-library implementation sequence, model choices, costs and required access.

Read `QUALITY_STANDARD.md` for current evaluation gates. `CALIBRATION_RESULTS.md` describes the initial eight-excerpt test; `BODY_CALIBRATION_RESULTS.md` records the completed 24-excerpt high-reasoning comparison. Neither diagnostic establishes production semantic accuracy.

`AGENT_EVALUATION_REVIEW.md` records the six-scenario development comparison, including regressions. V2 units are staged separately under ignored `data/units/`; they are not automatically imported into the legacy approved-card store or made available for business execution. Source-specific review edits and original model responses remain separate and traceable.

`V2_EVALUATION_RESULTS.md` consolidates the revised extraction results, mixed-provider fallback, staging counts, costs and limitations. The 24-source staging manifest includes one separate Terra fallback after an uncertain DeepSeek connection failure; the outstanding cost reservation is retained.

Offline inspection commands (after the associated experiments finish):

```powershell
python scripts/catalog_sources.py
python scripts/stage_units.py
python scripts/plan_continuations.py
python scripts/summarize_agent_eval.py
```

These commands read local artifacts only. Model runners require `--execute` and reserve spending before dispatch. The V2 extraction and agent-comparison requests share a $5 stage ceiling within the existing global budget.

## CRO folder checkpoint

See `CRO_PROCESSING_STATUS.md` for the current measured state, spend and limitations. The first pass covers all seven CRO documents; repair/review is incomplete and nothing is published. The approved folder cap remains $10. Private manifests, keys, API outputs and cards stay in ignored local storage.

Offline artifact order: `report_cro_quality.py`, `index_cro_revisions.py`, `audit_cro_origins.py`, then `compact_cro.py`. `prepare_cro_context.py` builds source-bound context windows without API calls. Context-aware repair/review requires explicit execution and sufficient authorized budget; no broader folder ingestion is enabled.

## Meta ad gallery

A separate, read-only local gallery of the top 30 ads by spend, across all formats or per format (image, video, carousel, catalog, flexible). It does not touch the intelligence library. See [META_GALLERY_STATUS.md](META_GALLERY_STATUS.md) for the connection status, run commands and reporting limits.

```powershell
python -m meta_gallery.server --prefetch-images
python -m meta_gallery.server   # http://127.0.0.1:8765
```
