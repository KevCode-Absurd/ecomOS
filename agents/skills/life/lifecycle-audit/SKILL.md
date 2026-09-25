---
name: lifecycle-audit
owner: LIFE
version: 1
invoke_when: sequencing the lifecycle build, or running the monthly program audit
inputs: metric contract, ESP flow/trigger config, order data, registry
outputs: ranked backlog or monthly health scorecard
---
# Lifecycle program audit

## Purpose
Scores flow and segmentation health against the standard set of 8 flow types and
produces a ranked backlog, so build sequencing is a read of real gaps, not a guess
at what "should" exist.

## Steps
1. List the 8 standard flow types and check each one's existence and health in the
   ESP: trigger fires, filters set, no stage overlap with another flow.
2. Pull flow-vs-campaign revenue split from the metric contract for context.
3. Flag every missing flow and every broken filter or overlap by name.
4. Rank the resulting gaps, plus any segmentation or deliverability flag, by
   expected revenue impact using order volume and AOV as the size input, computed
   in code.

## Checks
Every flow type in the standard set gets a row, even "missing." Every score traces
to a metric-contract field or an ESP read. No arithmetic done in the model.

## Output
A ranked backlog (for W01) or a monthly scorecard (for W11), both with the score
parts visible.

## Example
"Win-back flow: exists but no re-entry rule - claims same customer as sunset flow.
Ranked #2 behind 'no post-purchase flow exists' (#1, larger revenue gap)."
