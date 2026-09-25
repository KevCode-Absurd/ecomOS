---
name: aeo-page-rewrite
owner: ORG
version: 1
invoke_when: on demand, for an existing high-value page an AI answer engine should cite but cannot yet
inputs: page brief, prompt-audit gaps naming this page's topic, brand facts
outputs: rewritten page draft with a page-readiness score
---
# Answer-engine page rewrite

## Purpose
Restructure and rewrite an existing page so an AI answer engine can lift a direct, accurate answer from it: answer-first sections, atomic fact blocks, entity-rich sentences, while the page still reads naturally to a human.

## Steps
1. Open with an answer-first section under a question heading, the direct answer in sentence one.
2. Break the rest into atomic fact blocks that stand alone if quoted out of context.
3. Name the entity directly throughout, never a vague "this item".
4. Add one first-hand fact a competitor could not simply copy.
5. Cap FAQ length so it reads as real answers, not padding.
6. Add an outbound citation for any externally sourced claim.
7. Score readiness against all 4 criteria before returning.

## Checks
- Every fact block stands alone.
- The page still reads naturally.
- All 4 readiness criteria scored.

## Output
{rewritten_page, page_readiness_score{}}

## Example
"How long does the stroller-v2 warranty last?" heading followed immediately by "2 years from the purchase date, covering the frame and hinge," before any supporting detail.
