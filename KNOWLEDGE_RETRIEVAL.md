# Intelligence labels and retrieval

Working local implementation for all 7,611 cards. Original card text and IDs are unchanged.

## What agents use

Use `scripts/search_knowledge.py` or import `search_knowledge` from that module. Reuse the process/engine for low latency. The former `search_library.py` remains a legacy comparison interface.

```python
search_knowledge(
    task="Improve mobile product-page conversion",
    brand_context="Skincare; mostly paid social; low add-to-cart rate",
    complexity="focused",
    token_budget=8000
)
```

The response contains one context string, card IDs, token usage, current-verification flags and warnings. It does not repeat the complete card objects or send the metadata catalogue. `get_knowledge_card(card_id)` retrieves a selected card and source pointer for deeper inspection. This is a Python/CLI interface, not yet a hosted or MCP service.

## Labels

- Knowledge type: principle, diagnostic, procedure, tactic, case-study, unknown.
- Role: foundation, growth, operations, protection; multiple allowed.
- Durability: durable, periodically-changing, volatile, unknown. Durable is not universally applicable or permanently verified.
- Task labels: checkout-conversion, product-page, creative-testing, offer-design, customer-research, retention, email-sms, search-acquisition, organic-discovery, measurement, profitability, site-speed, security, inventory-sourcing, team-operations, marketplace.
- Existing domain and platform mentions; a mention is not proof of exclusive applicability.
- Applicability text and original caveats; source/evidence status and unknown date fields.

The model inferred the type, role, durability and task labels from title, summary, use conditions and tags. Topic/platform rules supply additional metadata. These labels are not independent fact verification. A spot check across all 24 folders corrected one obvious case-study misclassification. Three knowledge types and eight durability labels remain unknown. No invented expiry dates or verification dates.

## Retrieval behavior

Keyword FTS plus existing semantic vectors, vectorized similarity, task-fit ranking, seasonal-context penalty and conservative duplicate suppression. Unknown labels do not exclude cards unless an agent explicitly requests a metadata filter. Opt-in filters: domain, platform, role, knowledge_type, durability. Applicability is ranked from text; arbitrary brand constraints are not fully machine-verifiable yet. The execution agent must still assess fit.

Focused allowance: 8,000 knowledge tokens, up to 16 cards. Multi-part/broad: 16,000, up to 32. Both are overridable ceilings, not quotas. Low-scoring candidates are suppressed with a provisional relative-score floor; no-match and semantic-fallback states are explicit. These heuristics need broader relevance evaluation before production.

Conditions and complete step sequences are retained to avoid changing the meaning of advice. Per-sentence extraction is intentionally not claimed. Administrative metadata stays out of the context. The reported knowledge budget counts the context string; the complete JSON tool response has small additional overhead. Brand data, images, task instructions and output space need their own allocation.

## Updates

`python scripts/build_knowledge_metadata.py` preserves matching model/reviewed labels and generates conservative fallback labels for new or changed cards. `python scripts/classify_knowledge_labels.py` resumes cached label batches under its $4 stage ceiling. Reviewed edits live in `data/library-v3/metadata-overrides.json` keyed by card ID and content hash. Edited cards invalidate stale labels. The engine reloads when cards, metadata, vectors or index files change. Vector refresh remains the existing ingestion step.

## Validation and cost

- 13 targeted tests passed: conditions, duplicate handling, empty/zero budgets, unknown queries, filters, cached embeddings, fallback and stale metadata reload.
- All 7,611 metadata hashes match active cards; all vectors remain present.
- Eight real-library hybrid smoke queries reviewed; full report: `data/library-v3/retrieval-v4-evaluation.json`. These are developer-authored checks, not blinded task-quality evaluations.
- Cold engine load: 1371 ms. Median repeated-query search: 23.7 ms on this machine. First-time embedding requests add network/provider latency; the initial run observed roughly 0.6-3 seconds for four uncached queries.
- Aggregate complete tool-response tokens were 58.1% lower than the legacy interface in these checks. Returned selections differ; most savings come from eliminating duplicate card serialization. This is not an answer-quality or universal-cost guarantee.
- Label classification ledger estimate: $0.4752; no unresolved label reservations. Cumulative project estimate including existing unresolved reservations: $21.6606. Query embeddings are included in the project total. Provider invoices may differ.

Next evaluation: independently judge applicability and coverage across brand scenarios, including conflicts and missing facts. No data connectors, inspiration assets, hosting or GitHub publication were added in this step.
