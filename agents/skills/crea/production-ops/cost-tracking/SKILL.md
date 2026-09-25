---
name: production-ops/cost-tracking
owner: crea-paid-creative-copy
version: 1
invoke_when: real production costs need logging against the monthly budget,
  or a likely overrun needs an early flag
inputs: billing records, invoices, AI generation-credit usage
outputs: cost-per-asset table, spend-versus-plan status, overrun flag
---
Purpose: tie real production cost, AI credits, freelancer and agency
invoices, stock license fees, to the specific finished asset it paid for, so
the monthly plan is checked against real spend, not a guess.

Steps
1. Log every real cost as it is incurred against the named asset id it
   produced; a lump-sum monthly invoice with no per-asset breakdown gets
   split before it is logged, not entered whole.
2. Compute cost per finished asset by format in code, never estimated in
   prose.
3. Compare running month-to-date spend against the monthly budget line set
   in the pipeline plan.
4. When the trend line projects crossing the budget before month end, flag it
   with the exact date it will cross, not a vague warning.
5. Log the weekly snapshot to the registry so next month's pipeline plan
   starts from real history.

Checks: every cost tied to a named asset; a cost not yet logged shows as
unavailable, never as zero.

Output: the cost-per-asset table, the spend-versus-plan status, and an
overrun flag when the trend calls for one.

Example: this month's AI generation credits, one freelancer invoice and a
stock-music fee total to a cost per finished asset 18% above the trailing
3-month average, flagged with the date it will cross budget if it continues.
