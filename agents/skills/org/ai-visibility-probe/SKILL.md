---
name: ai-visibility-probe
owner: ORG
version: 1
invoke_when: monthly
inputs: frozen prompt set, entity list, competitor list, prior month's citation log
outputs: per-prompt classified results, a persistence check, classified gaps
---
# AI-visibility probe and gap classification

## Purpose
Run the recurring, repeatable check of how ChatGPT, Gemini, Perplexity and Google AI describe the brand on a frozen prompt set, since there is no shared monitoring API today, and never collapse the result into a single deterministic rank.

## Steps
1. Run every frozen prompt on each prioritized platform, by hand.
2. Classify each result: named, cited with link, cited without link, or absent, and whether a competitor was named instead or alongside.
3. Check whether the answer came from live retrieval (a shown citation) or model memory with no citation.
4. Recheck last month's citations to confirm they persisted.
5. Classify each gap: missing fact, wrong fact, outdated fact, no coverage.
6. Return the raw results for the reporting skill to turn into the monthly report.

## Checks
- No single rank number reported.
- Every citation opened and verified directly.
- Persistence actually re-run, not assumed.

## Output
{per_prompt_results[], persistence_check[], gaps[]}

## Example
Prompt "best foldable stroller for small US apartments" on Perplexity cites a competitor's blog by link, and does not mention this brand at all: classified as "no coverage".
