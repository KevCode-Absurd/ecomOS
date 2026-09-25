---
name: brand-story-and-promise
owner: BRAND
version: 1
invoke_when: the founder/brand story needs writing, or a brand promise and tagline need drafting and testing
inputs: founder's own account, avatar record, positioning statement if one exists
outputs: brand story, 3-sentence promise, tagline candidates
---
# Brand story and promise

## Purpose
The story and the promise are both meant to stay stable for years, so they get written once, carefully, from real material, not regenerated per campaign. This skill covers both since they are written and tested together.

## Steps
1. Write the founder or brand story in a self, us, now structure: who the founder is (self), the shared struggle with the customer (us), why this matters right now (now). Every biographical detail must be confirmed by the founder, never invented for narrative effect.
2. Draft the 3-sentence promise from the positioning statement if one exists: the change the customer gets, the mechanism that delivers it, the proof it is real.
3. Draft 3-5 tagline candidates from the promise.
4. Run the strip test on every candidate: if a competitor's name could swap in and it would still read true, it fails and is cut or sharpened.
5. For a candidate meant to become a signature line (used repeatedly across ads or packaging), design a small recall-based test: does a shopper remember it after seeing it once, measured with a stated read point.

## Checks
- No invented biographical fact; the founder confirms every detail in the story.
- Every claim in the promise passes `shared/claim-check`.
- Tagline candidates that fail the strip test are cut before presentation.

## Output
`{brand_story, promise, tagline_candidates: [...]}`

## Example
Tagline candidate "Jewellery that keeps its shine after the wedding" passes the strip test (specific to this brand's durability claim, backed by a site-approved claim tier) while "Beautiful jewellery for every occasion" fails (any competitor's name reads equally true).
