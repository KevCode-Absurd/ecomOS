---
name: money/attribution-model-reconcile
owner: MONEY
version: 1
invoke_when: attribution models disagree or platform order counts need cross-checking against store orders
inputs: order counts by source, attribution reports by model, blended MER history
outputs: order-count cross-check, bot spike flags, or a per-channel attribution gap report
---
# Reconcile attribution models and order counts

## Purpose
Catch a bot-inflated session spike and a platform-versus-GA4 attribution disagreement before either one drives a budget decision.

## Steps
1. Cross-check GA4, Meta, Shopify and marketplace order counts against actual store orders for the period.
2. Flag any spike in one source's count that does not match store orders as a possible bot signal, and hand it to the security scan.
3. Report the gap between last-click and data-driven models, and between platform-reported and GA4-reported numbers, per channel.
4. Before a large reallocation, run or schedule a holdout test rather than trust the attribution gap alone.

## Checks
- Every order-count gap over 2 percent carries a named cause.
- The model gap is reported per channel, never collapsed into one number.

## Output
Order-count cross-check table, bot spike flag list, and the per-channel attribution gap report.

## Example
Meta reports 30 percent more sessions than GA4 for one campaign in a single week; the spike is flagged as a likely bot pattern and handed to the weekly security scan instead of being read as real interest.
