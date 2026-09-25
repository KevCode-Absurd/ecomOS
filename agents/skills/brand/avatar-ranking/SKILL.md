---
name: avatar-ranking
owner: BRAND
version: 1
invoke_when: multiple avatar candidates exist and one must be picked as the cycle's primary
inputs: all candidates surfaced this quarter, metric contract fields
outputs: ranked list, recommended primary avatar
---
# Avatar ranking

## Purpose
Not every avatar candidate research surfaces deserves to become the primary. This skill applies a consistent, evidence-weighted score instead of picking whichever idea sounds newest or most exciting.

## Steps
1. List every avatar candidate surfaced this quarter, noting which run (reviews, social, untapped-avatar pipeline, etc.) found it.
2. Drop any candidate appearing in only one source type; a real avatar shows up more than once.
3. Score each remaining candidate on estimated reach (against the brand's own traffic and customer data) and product fit (does the current product actually serve this job well), computed in code using `shared/rank-candidates`.
4. Rank candidates by reach x fit x evidence strength.
5. Recommend a primary, and name the top 1-2 runner-ups with why they ranked below the pick.

## Checks
- Every scored candidate cites 2 or more independent source types.
- Reach and fit scores are computed in code from real fields, not estimated in prose.
- The current primary avatar is re-scored fresh each cycle, not kept by default.

## Output
`{ranked_list: [{candidate, reach_score, fit_score, evidence_score, total}], recommended_primary}`

## Example
3 candidates scored; the current primary re-scores highest (reach 0.8, fit 0.9) but a sub-avatar from social listening (reach 0.3, fit 0.95) is flagged as a strong runner-up worth a dedicated segment record.
