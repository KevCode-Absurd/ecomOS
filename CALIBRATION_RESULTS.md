# First extraction calibration — 22 September 2026

The approved comparison completed: eight identical excerpts, two providers, plus a DeepSeek non-thinking variation. Total 24 requests. The ledger booked **$0.128300** with zero pending requests. This is a conservative token-price estimate, not a provider invoice: it uses DeepSeek peak/cache-miss rates and OpenAI input cache-write upper rates. No cards were published.

| Variant | Complete outputs | Outputs passing schema and exact-quote checks | Average observed latency | Booked cost for eight calls |
|---|---:|---:|---:|---:|
| DeepSeek Flash, low thinking, 4,096 output-token limit | 5/8 | 5/8 | 15.24 seconds | $0.036696 |
| GPT-5.6 Terra, low thinking, same output-token limit | 8/8 | 5/8 | 9.82 seconds | $0.082234 |
| DeepSeek Flash, non-thinking, same output-token limit | 8/8 | 7/8 | 4.01 seconds | $0.009361 |

These counts are **not semantic accuracy scores**. This is a small, deliberately bounded diagnostic, not a statistically representative model ranking. Seven excerpts are editorial guidance/summary passages; the SEO excerpt is transcript-like text. The sampling method overrepresented document headers. The results therefore test contamination and output mechanics much more than full-transcript extraction quality. The three-card limit also prevents recall measurement and must not silently limit full ingestion.

## Findings from inspecting the source and output

1. **DeepSeek non-thinking is the stronger next extraction candidate on cost and completion.** Low thinking exhausted its output allowance on three cases. This does not prove it cannot work at another cap or prompt; it means the tested setting was unreliable.
2. **Exact evidence must be validated by code.** Terra added wrapping quotation marks/escaping on several cases; DeepSeek non-thinking introduced a typo in one quoted span. Both fail literal matching. Preserve raw output; repair only through a checked source-span selection, never approximate fabricated evidence into approval.
3. **Do not let the extractor decide source provenance.** Both models labeled a transcript-like SEO passage generated analysis. Editorial headers should be separately identified from document structure, with uncertain boundaries reviewed. Until confirmed, origin remains unverified.
4. **Conditions need stronger structure.** DeepSeek put missing-information statements into exclusion fields. Both models introduced reasonable but uncited implementation safeguards. Keep source-supported conditions separate from derived operator safeguards and missing facts. Use explicit ALL/ANY logic: two alternative traffic audiences must not become simultaneous requirements.
5. **Faithful quotation is not factual correctness.** Both providers reproduced a questionable numerical example in an editorial offer summary instead of resolving its arithmetic. Such material requires original-evidence retrieval and a calculation check. A source threshold must also remain attributed advice, not an automatically universal execution rule.
6. **Publication stays blocked for this batch.** Candidates are illustrative outputs; none has a verified original-evidence chain, human-labeled evaluation score or production-ready applicability representation.

## Required changes before broad paid processing

- Separate metadata, routing notes, editorial summaries and transcript/article body. Store original locators and do not silently promote body guesses to verified provenance.
- Replace flat condition lists with typed predicates and explicit alternative branches; keep derived safeguards and unknowns in separate fields.
- Require source offsets for evidence and validate reconstructed quotes. Store source text unchanged.
- Add numeric-consistency checks and a reviewer path for stale platform instructions or conflicting evidence.
- Build a new evaluation selection from actual source bodies across all categories, with adjacent context and labeled expected behavior. The current eight-excerpt result cannot justify full-corpus model selection.
- Route uncomplicated extraction to DeepSeek non-thinking as a candidate default; evaluate Terra as a verifier rather than assuming its higher price guarantees correctness.
- Re-estimate cost using accepted-card yield, prompt overhead and verification volume. Do not multiply this header-heavy sample's cheap cost across the full library.

Detailed source excerpts and model outputs remain under ignored `data/calibration-v1/`. The approved payload manifest is `data/calibration-transmission-review.json`. No raw source material or credentials were pushed to GitHub.
