---
name: test-program-governance
owner: LIFE
version: 1
invoke_when: prioritising the test backlog, specifying a new test, or checking test
  hygiene across flows, campaigns, channels or offers
inputs: backlog, registry of running tests, metric contract
outputs: test specification, pre-registered before launch
---
# Lifecycle test program governance

## Purpose
Keeps lifecycle experimentation trustworthy: no confounded tests, one variable at a
time, and a metric and read window fixed before anyone sees a result.

## Steps
1. Check the backlog against currently running tests for any segment-and-metric
   overlap that would confound a read.
2. Rank remaining candidates by expected impact and dependency order (a test whose
   prerequisite is unmet ranks below that prerequisite).
3. Write the hypothesis, control, variant, and minimum sample size for each test.
4. Pre-register the exact metric and read window before launch.
5. Set a holdout, sized in code, for any incrementality read.

## Checks
No two live tests confound each other. Metric and window are fixed before launch,
never chosen after seeing early results.

## Output
A test specification per prioritised test, ready to hand to the workflow that will
build the variant.

## Example
"Win-back discount-timing test queued behind the win-back trigger-timing test
(prerequisite): read discount timing only once trigger timing is settled."
