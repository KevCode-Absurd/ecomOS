---
name: money/margin/customer-profitability
owner: MONEY
version: 1
invoke_when: a loyalty tier design or VIP segmentation needs true profit per customer
inputs: order-cost dataset, support ticket cost, return log, discount ledger, current tiers
outputs: true customer profitability table with tier-mismatch flags
---
# Compute true customer profitability

## Purpose
A customer who buys often but returns often, or costs a lot in support tickets, may be worth less than a quieter customer. This skill puts every real cost against revenue before anyone calls someone a VIP.

## Steps
1. Pull support-ticket cost per contact, return and refund cost, shipping cost and discount cost for each customer.
2. Subtract all four from revenue, in code, to get true profitability.
3. Compare true profitability to the customer's current loyalty tier.
4. Flag any customer whose tier does not match their true profitability rank.

## Checks
- No cost bucket is estimated; a missing one is marked unavailable, never zero.
- The comparison to loyalty tier uses true profit, never raw revenue.

## Output
A table per customer: revenue, each cost bucket, true profit, current tier, and a mismatch flag.

## Example
A customer with the highest revenue this year is flagged for a tier downgrade once true profit accounts for an 18 percent return rate and 6 support tickets.
