---
name: stats-design
owner: site-specialist
version: 1
invoke_when: a CRO hypothesis has cleared intake and needs a real, honest test design
inputs: intake note, traffic and order volume, minimum detectable effect target
outputs: test design spec (arms, sample, runtime, stopping rule)
---
# Design the statistics of a CRO test

## Purpose
Size and design a test so its result can actually be trusted, since a wrong sample-size formula is a silent, expensive mistake.

## Steps
1. Decide test-or-not from the traffic gate and real sample-size math; below the threshold, recommend a bigger change instead.
2. Size the test from the minimum detectable effect, stated as orders per variant, never a flat number pulled from habit.
3. Compute runtime as arms x sample / weekly traffic, running at least 2 full weeks and covering each weekday twice.
4. Pick a stopping rule before launch and commit to it; no peeking outside the planned looks.
5. Randomize by user with sticky bucketing so a visitor never sees both arms.
6. Remove or isolate returning-visitor traffic so it doesn't contaminate a new-visitor test.

## Checks
- Sample size is orders per variant, computed from a real MDE, not a round number.
- Stopping rule exists in writing before the test goes live.

## Output
A test design spec: arms, sample size, runtime, stats engine, stopping rule, randomization method.

## Example
"MDE: 8% relative lift on PDP-to-cart. Required: 2,400 orders per variant. At current 850 orders/week split across 2 arms, runtime: 3 weeks. Stopping rule: fixed horizon, no early peek."
