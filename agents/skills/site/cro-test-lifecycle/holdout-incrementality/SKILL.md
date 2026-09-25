---
name: holdout-incrementality
owner: site-specialist
version: 1
invoke_when: measuring a feature, popup, recommendation module, or the whole CRO programme's real causal value
inputs: metric contract, connector: metabase
outputs: holdout design, programme value report
---
# Design holdout and incrementality measurement

## Purpose
Prove a feature or a whole programme is adding real value with a holdout, since a feature's own engagement metric and the sum of individual test lifts both overstate value.

## Steps
1. Design a feature holdout (a popup, a recommendation module, a cart-recovery flow) instead of trusting its own engagement metric.
2. Run a persistent programme-level holdout to prove the CRO programme's net value, never reported as the sum of test lifts.
3. State the identifying assumption behind any causal method in writing, and actively try to challenge it.
4. Check the traffic gate before choosing a holdout design; a traffic-starved brand may not support a clean holdout.
5. Turn on CUPED variance reduction only for returning, identified users.
6. Winsorize outlier orders or switch to a proportion metric to steady a noisy revenue test.

## Checks
- Programme value is never reported as the sum of individual test lifts.
- The identifying assumption is written down, not left implicit.

## Output
A holdout design and a programme value report.

## Example
"Cart-recovery discount flow: holdout group with no discount converts at 62% of the discounted group's recovery rate; net incremental revenue after the discount cost is still positive but smaller than the raw recovery-rate lift suggested."
