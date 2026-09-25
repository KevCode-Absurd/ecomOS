---
name: offer-testing-framework
owner: LIFE
version: 1
invoke_when: sequencing or pre-registering a test on an offer, bundle, GWP,
  upsell or guarantee
inputs: offer test backlog, registry of past offer tests, metric contract
outputs: sequenced, dependency-checked offer test backlog
---
# Offer test sequencing

## Purpose
Keeps offer testing honest: structure tested before depth, one variable at a time,
with the metric and read window fixed before launch and no duplicate tests
running for the same underlying question.

## Steps
1. Pull every proposed offer/bundle/GWP/upsell/guarantee test not yet run.
2. Sequence so a structural question (does a bundle beat a single SKU) is tested
   before a depth question (which bundle size wins).
3. Check dependency order: a test needing a working discount-policy rule ranks
   below getting that rule settled.
4. Pre-register the exact metric and read window for each test before launch.
5. Remove duplicate or already-run tests from the backlog.

## Checks
No test changes two variables at once. No dependent test runs ahead of its
prerequisite. No duplicate test for the same offer question.

## Output
A sequenced, dependency-checked backlog, each entry pre-registered.

## Example
"Bundle-vs-single-SKU (structure) sequenced ahead of 3-pack-vs-5-pack (depth) for
the same product, since depth only matters if structure already won."
