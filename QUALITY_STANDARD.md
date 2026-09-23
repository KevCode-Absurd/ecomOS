# Ecommerce intelligence: quality before compression

Decision recorded 2026-09-22: choose models by measured usefulness, not by lowest reasoning effort. Working processing budget remains $160; absolute ceiling $200. Neither spending ceiling guarantees a complete production-quality library. If projected quality work exceeds the working budget, present the measured tradeoff before changing it.

## What creates differentiation

The library must change a business decision in a defensible way. Volume of sources and fluent summaries are not sufficient. Differentiation comes from preserved specialist knowledge, applicability to brand facts, traceable evidence, explicit disagreements, and measured outcomes. The library is maintainable infrastructure: platform instructions, stale tactics and failed experiments will still need updates after initial construction.

## Knowledge representation

Keep three linked representations rather than force every source into tiny cards:

1. Immutable original and normalized text, with document version, locator and character offsets. Preserve tables, examples and unprocessed media in a coverage ledger.
2. Atomic decision cards: one supported recommendation with mechanism, trigger, source-stated prerequisites and exclusions, execution steps, required inputs, expected artifact, measurement guidance, and unresolved questions. Missing fields remain unknown; never invent a complete playbook from a thin excerpt.
3. Playbooks connecting cards into ordered workflows, with alternative branches, dependencies, conflicts and evidence links. Synthesis and proposed safeguards must be identified separately from the author's advice.

Each consequential claim, threshold and step needs its own evidence link. Store AND/OR logic explicitly; do not flatten alternate audiences into simultaneous requirements. Distinguish an anecdote from a general recommendation. Preserve units, denominators, attribution windows, platform, market, date, and qualifications. Numerical or causal claims receive additional review. Preserve original wording separately from normalized operational wording.

Cards have stable IDs and versions. Origin, source authority and factual correctness are separate dimensions. A model cannot certify authorship from writing style. An exact quote proves text exists, not that the recommendation follows from it or is correct today.

## Extraction and model selection

Current candidates: DeepSeek Flash with disabled and high thinking; OpenAI Terra at low and high effort. Add a stronger OpenAI model for adjudication if difficult cases show a material benefit; do not assume vendor or effort level determines quality.

Run comparable prompts, passages and schemas across candidates. Give reasoning configurations enough output allowance to finish; the earlier 4,096-token cap confounded reasoning quality with truncation. The next high-effort diagnostic allows 16,384 completion tokens and retains a $5 stage ceiling. Its 24 candidate body passages remain unverified, and its three-card extraction cap measures diagnostics only, not comprehensive recall. Do not use that runner for bulk publication.

Before choosing the production route, run the no-thinking control on the SAME body passages with the SAME output allowance, then manually audit extraction against annotated evidence. Do not compare the earlier header-heavy set with the new body set as if it were a controlled experiment. A stronger-model critic can flag errors but cannot be the sole truth labeler. Blind model identities during scoring.

Use inexpensive deterministic code for parsing, hashes, exact offsets, duplication and budget checks. Select the best passing extraction route by domain and complexity; escalate ambiguous, conflicting, numerical and highly consequential recommendations. Compute cost per accepted, audited decision unit, including reasoning, rejected outputs, validation and retries—not cost per request.

## Coverage and release gates

For every source span record: processed, no actionable knowledge with reason, duplicate with canonical reference, unresolved, or awaiting media interpretation. A three-card cap must trigger explicit continuation or smaller semantic sections, not silent loss. Inspect neighboring sections before accepting extracted advice because central excerpts can omit qualifications.

Create reference annotations before tuning: all material recommendations in selected sections, their supporting spans, conditions, exceptions and relationships. Reserve an untouched document-level holdout; overlapping passages from one document must not cross tuning and holdout sets.

Initial acceptance targets (proposed gates, not achieved results):

- 100% exact and version-resolvable evidence references for published claims.
- Zero critical errors in audited examples: fabricated actions/lifts, reversed advice, omitted applicability that makes an action inappropriate, or private data disclosure.
- At least 95% supported claim precision and 90% material recommendation recall against independently reviewed annotations. Report numerator, denominator, domain breakdown and uncertainty; a small test is not proof of production reliability.
- No publication of unresolved source conflicts, unknown provenance as original proof, truncated outputs or unreviewed candidate cards.
- Final source coverage report accounts for every document, unresolved span and media item. Completion cannot mean merely that every file was downloaded.

## Test the benefit to the agent

Use identical executor model, brand brief, question, output budget and scoring rubric across three conditions: no library; ordinary raw-text retrieval; curated cards with evidence expansion. Randomize presentation to reviewers. Score correct next action, applicability, specialist detail, evidence support, sequencing, missing-data handling, and execution-ready output. Do not reward length or jargon.

For each case score 0 (wrong/missing), 1 (partial), or 2 (complete) on each dimension. Mark critical errors separately: a high average cannot cancel them. Record preference wins, ties, losses and failure explanations. Proposed utility gate: curated knowledge wins at least 70% of non-tied comparisons against the no-library baseline and improves over raw retrieval, without more critical errors. This is an engineering release target, not a promised business uplift.

Use paired brand scenarios where one relevant fact changes: contribution margin, inventory, platform, audience awareness, measurement reliability or purchase cycle. The recommended action should change when evidence warrants it, and remain stable when irrelevant details change. Include cases that should abstain. Include new brands, established brands and agencies; do not assume tactics transfer to $100M businesses automatically.

## Retrieval contract

Retrieve by business objective and constraints as well as semantic similarity. Return compact routing summaries first, then the selected cards and their dependencies, and fetch longer evidence on demand. Keep explicit conditions and exclusions intact under token limits. When context cannot fit, return a coverage warning and request another retrieval round; never silently trim away a prerequisite. Unknown brand facts become questions or conditional branches, not assumed facts.

## Immediate work sequence

1. Review proposed body excerpts with adjacent context; label origin uncertainty and evidence limitations.
2. Run the high-effort diagnostic after approval of the private excerpt transmission. No automatic card publication.
3. Build document-level annotations and matched controls; update the card schema and test conditions, conflicts and recall.
4. Test executor outputs with and without the library and compare against raw retrieval.
5. Project full-library costs from accepted-card yield, review rate and coverage. Then process resumable batches, preserving quality gates and budget reservations.

Official configuration references: https://developers.openai.com/api/docs/models/gpt-5.6-terra and https://api-docs.deepseek.com/guides/thinking_mode/ . API support does not establish task quality; local evaluation determines selection.
