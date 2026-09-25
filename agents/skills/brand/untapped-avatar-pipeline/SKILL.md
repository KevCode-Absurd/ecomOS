---
name: untapped-avatar-pipeline
owner: BRAND
version: 1
invoke_when: the category is saturated with no real product difference left to claim
inputs: competitor packet, brand brain product capabilities
outputs: claimed-avatar map, adjacent job candidates, evidence-checked candidates
---
# Untapped avatar discovery pipeline

## Purpose
When every competitor claims the same avatar and the product has no new feature to differentiate on, the way out is often a different customer, not a different claim. This is a structured search for a real, unclaimed adjacent avatar.

## Steps
1. From the competitor packet's per-competitor avatar reads, map exactly who every visible rival is obviously serving.
2. List adjacent jobs this exact product, as it exists today, could also do: a gifting job, a professional-use job, a different life-stage job, drawn from the product's real capabilities, not a future roadmap.
3. Search reviews, forums, and both own and public search terms for any sign someone already uses or wants the product for that adjacent job.
4. Drop any candidate with zero found evidence; hope is not evidence.
5. Run a lightweight market-sizing pass on the strongest 1-2 remaining candidates.

## Checks
- Every candidate job must be something the product can do today.
- A candidate with no found evidence at all is dropped, not carried forward "just in case."

## Output
`{claimed_avatar_map, adjacent_job_candidates: [...], evidence_checked_candidates: [...]}`

## Example
Category: everyone targets the bride. Adjacent job found with evidence (3 reviews, 1 forum thread): jewellery bought by working women for daily office wear, a job no competitor's marketing speaks to.
