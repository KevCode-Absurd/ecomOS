---
name: post-launch-hygiene
owner: site-specialist
version: 1
invoke_when: the weekly recurring housekeeping pass after a store is live
inputs: connector: shopify admin, connector: support desk
outputs: hygiene report, fix list
---
# Post-launch hygiene sweep

## Purpose
Catch the small things quietly going wrong on a live store before they become a support flood or a lost sale, on a fixed weekly cadence.

## Steps
1. Reconcile platform inventory against real stock (weekly for month one, then as risk warrants).
2. Classify support tickets by root cause; anything outside Site's 4 folders gets routed with site/handoff-note, not dropped.
3. Re-run shipping and tax checks whenever a product, zone or app changed this week.
4. Confirm review-request automation and the payout bank account are both actually working, checked against a real order.
5. Sweep for broken links to images, CSS and JS, and collapse any redirect chain to one 301.

## Checks
- Every recurring ticket cluster maps to a named root cause or is routed to the right specialist.
- No item marked fixed without a live re-check.

## Output
A short weekly hygiene report and a fix list, each fix naming who does it.

## Example
"Ticket cluster (11 this week): 'where is my size chart' on the linen shirt PDP. Root cause: size chart missing after last theme update. Fix: re-add via SITE-W11, same day."
