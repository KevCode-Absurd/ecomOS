# High-reasoning body-excerpt comparison

Completed 2026-09-22. The approved 24-excerpt comparison finished successfully. DeepSeek Flash high is a promising extraction candidate, but neither model's raw output is ready for automatic publication or execution. This experiment does not establish that the curated library improves agent decisions yet.

## Measured results

Both providers received the same 24 selected excerpts, the same extraction prompt and a 16,384-token completion allowance, with reasoning set to high. Source text total: 232,980 characters. The excerpts cover 24 source groups but are not a statistically representative or independently provenance-verified sample. Each call allowed at most three cards.

| Measurement | DeepSeek Flash, high | OpenAI Terra, high |
|---|---:|---:|
| Completed requests | 24 | 24 |
| Nonempty responses | 23 | 23 |
| Candidate cards | 69 | 69 |
| Responses passing schema and exact-quote checks | 24 | 5 |
| Truncated outputs | 0 | 0 |
| Mean request time | 32.17 seconds | 12.50 seconds |
| Conservative booked cost, before ledger rounding | $0.249122 | $0.413205 |
| Responses requesting continuation | 23 | 23 |

The response-level pass count includes one valid empty response per provider. These are formatting/evidence-location checks, **not semantic accuracy scores**. There are 138 candidate card versions across two extractors, not 138 unique approved pieces of knowledge.

Stage ledger: **$0.662339 of the $5 ceiling**. All calibration to date: **$0.790639**. Zero pending reservations. Costs use conservative configured rates rather than an invoice and include reported completion usage; ledger values round each request upward. No bulk processing or publication occurred.

DeepSeek returned 321 exact quote anchors. Terra returned 43 exact anchors, 178 with added wrapping quotation marks, and six other unmatched anchors. Wrapper errors are diagnosed separately because they are not equivalent to fabricated advice. They were not silently repaired or accepted.

## Semantic spot review

Reviewed source and candidate outputs in subscription, CRO and finance in detail, plus selected product research, tracking, advertising, remarketing and security cases. This is a model-assisted spot review, not an independently scored evaluation of every candidate.

### Subscription

DeepSeek noticed contradictory platform eligibility statements and inconsistent percentage wording in the transcript. That is useful. However, it combined reminder design, platform migration, gifts, delay links and segmentation into one large action. Its conditions also made an optional gift/perk look like a prerequisite for the whole task.

Terra separated some decisions more clearly, but its stage-based message customization card also included an upcoming gift in the applicability list. Gift-specific messaging is an optional branch, not a universal requirement. Both need field-level evidence and explicit condition logic. Neither extraction validates current legal requirements or platform behavior.

### CRO

Both retained a research-backed hypothesis structure and attributed traffic/duration advice to the speaker. DeepSeek also extracted prioritization details; Terra retained the revenue-per-visitor/session distinction. Each omitted other useful points under the three-card cap. Continuation must become actual work, not a boolean that is ignored.

DeepSeek attached the high-volume comprehensive-test context to a broader testing card. This risks excluding other applicable uses. Numerical rules of thumb also need to stay distinguishable from a validated statistical design. More reasoning did not resolve these representation problems.

### Finance and measurement

Both retained the distinction between within-platform directional ROAS and cross-platform allocation, and between acquisition revenue and total revenue. Terra more clearly preserved the warning against casually turning a geographic-test illustration into a spending experiment. DeepSeek retained caveats but still wrote a procedural action from the simplified illustration, which needs a hold for complete test-design review.

Some exclusions in these and tracking cards describe the problem the action is intended to fix. If converted directly into retrieval predicates, they could prevent an agent from finding the repair instructions. Distinguish task triggers, prerequisites, exclusions and completion criteria.

### Preserve useful non-action knowledge

Both returned no action cards for the selected security lecture excerpt. Avoiding invented mitigation steps is appropriate, but explanatory principles should remain accessible to security agents. An action-only schema can lose useful knowledge. A separate selected passage was a compiled strategy table with citation markers; its references and provenance remain unresolved. Body length alone does not establish original authorship.

## Decisions and implemented changes

- Do not select a production model solely from these pass counts. DeepSeek high is the next extraction baseline to test; Terra high remains a comparison/review candidate. A stronger adjudicator can be tested on difficult cases if it improves measured quality.
- Do not compare this test's quality directly with the earlier low/no-thinking experiment: passages and completion allowances differed. A matched comparison must hold both constant.
- Implemented explicit ALL/ANY/NOT conditions, numerical ranges and three-state handling of missing facts in the local store/context path. Legacy equality conditions remain supported. All **35 code tests pass**. This does not automatically translate the current free-text candidate conditions into reviewed predicates.
- Added the next extraction contract in `prompts/extract-v2.md`: atomic units; separate action/principle/example/warning types; field-specific evidence; supplied provenance rather than model guesses; derived suggestions separated from source knowledge; explicit continuation.
- Prepared 23 source-anchored review criteria across three cases. Private anchors remain under ignored `data/`; these are draft annotations pending independent review, not certified ground truth.
- Added three synthetic brand-context pairs for six development scenarios. These are prepared cases; the no-library/raw-retrieval/curated-knowledge agent comparison has **not yet run**.

## Next quality gate

Implement and validate the revised extraction schema, then run matched settings on the approved excerpts. Review semantic support and coverage before scaling. After candidate review, compare the same executor on the same brand scenarios with no library, ordinary raw retrieval and curated evidence. Keep an untouched document-level holdout for the eventual release decision.

The remaining bottleneck is faithful, complete, usable representation—not the cost of this diagnostic. No promise of full-library processing cost or business uplift follows from a capped three-card sample.

## Reproduce and inspect locally

`scripts/summarize_calibration.py` produces read-only quote/format diagnostics from saved responses. `scripts/prepare_semantic_review.py` resolves private draft review anchors. Neither script calls a model or publishes cards. Original responses, usage, authorization record and spend ledger are in ignored `data/calibration-body-high/`.
