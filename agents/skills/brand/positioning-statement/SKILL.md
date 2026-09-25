---
name: positioning-statement
owner: BRAND
version: 1
invoke_when: a positioning statement needs drafting, auditing, testing, or no open slot exists head-on
inputs: category ladder, XY map, avatar record, claims tiers
outputs: positioning statement, 3-sentence promise, differentiation line, checklist result
---
# Positioning statement

## Purpose
This is the single procedure for turning a mapped competitive field into the one line a shopper reads and believes, including the fallback path when the map shows every direct slot already taken.

## Steps
1. Answer the 6 positioning questions in writing: for whom, for what category, against what alternative, what benefit, why believe it, why now. Every answer traces to the avatar record or a verified fact.
2. Draft the 3-sentence promise: the change, the mechanism, the proof.
3. Cut the promise to the one differentiation line a scrolling shopper would actually read.
4. Run the fixed positioning checklist (clear, ownable, provable, durable, no disputed statistic); a fail on any item blocks moving forward until fixed.
5. If the XY map shows every corner already occupied, search for an unclaimed dimension entirely (a creneau), take the deliberate against-position relative to the category leader, or reframe the whole category around a frustration the avatar record already documents.
6. Where two framings are both credible, design a small test (an ad message test, a landing headline split, or an AI-persona pretest) before committing to one.

## Checks
- Every claim passes `shared/claim-check` against the claims tiers.
- The differentiation line fails the strip test if a competitor's name could swap in and it would still read true: a fail means it is not ownable yet.
- A checklist fail blocks presentation to the founder until resolved.

## Output
`{positioning_statement, promise, differentiation_line, checklist_result: {pass|fail, notes}}`

## Example
Differentiation line: "Jewellery you can wear the Tuesday after the wedding, not just the wedding day." Strip test: fails if swapped for a costume-jewellery competitor (still true for them too): flagged to sharpen further before founder review.
