---
name: prod/sourcing-audit
owner: PROD
version: 1
invoke_when: a brand is onboarded or a new client taken on, or a billing cycle or SLA period needs its standing
  check
inputs: the full supplier and SKU list, contracted rates for suppliers/couriers/3PLs, current billing statements,
  SLA terms
outputs: an onboarding audit report, ongoing billing-anomaly flags, and a daily SLA tracking log
---
# Audit the sourcing base and watch billing/SLA

## Purpose
Two different jobs share one owner: a one-time full audit when a brand comes on board or a client is taken over,
and a standing, ongoing watch on every bill and SLA so a quiet rate increase or missed service level is never
discovered by accident.

## Steps
1. On onboarding, audit the entire sourcing base in one pass: every active supplier, their current term, their
   current price, cross-checked against what the brand's own records say should be true.
2. At a high SKU count, move purchase orders from a weekly to a daily cadence so no reorder waits an unnecessary
   week.
3. Watch every recurring supplier, courier and 3PL bill against its contracted rate, computed in code, every
   billing cycle.
4. Flag a quiet rate increase, a duplicate charge, or a new surcharge the same cycle it appears: never let it run
   for months unnoticed.
5. Track 3PL and warehouse SLA performance daily against the written SLA: pick-and-pack speed, mis-ship rate,
   damage rate, backorder rate.

## Checks
- The onboarding audit covers every active supplier, none skipped.
- Every billing check compares against the actual contracted rate, not simply against last month's bill.
- An SLA breach is flagged the day it happens, not discovered at a monthly review.

## Output
{onboarding_audit[], po_cadence, billing_flags[], sla_log[]}

## Example
Onboarding audit of 22 suppliers found one still billing an old, since-superseded rate. Billing watch flagged a
new "fuel surcharge" line from a courier this cycle, absent from the signed contract. SLA log shows the 3PL's
mis-ship rate at 0.4%, within the written 0.5% SLA.
