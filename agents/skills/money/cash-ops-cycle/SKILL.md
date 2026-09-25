---
name: money/cash-ops-cycle
owner: MONEY
version: 1
invoke_when: a vendor bill, B2B invoice, payroll cycle or expense statement needs processing
inputs: vendor bills and POs, B2B invoice terms, payroll roster, expense policy, card statement
outputs: AP queue, AR aging, payroll run, or expense reconciliation, by process
---
# Run accounts payable, receivable, payroll and expense

## Purpose
One engine for the recurring cash-movement processes, so approval chains, payment terms and policy checks are applied the same way every cycle.

## Steps
1. For payable: capture every bill, match it to its PO and receipt, and route it through the approval chain by amount and vendor.
2. For receivable: invoice B2B and wholesale buyers on their agreed terms and run a structured dunning sequence on overdue accounts.
3. For payroll: process the cycle from the roster through Gusto or ADP, then prepare federal/state withholding and W-2/1099-NEC filings (PF, ESI, professional tax, TDS and Form 16 for India-selling brands).
4. For expense: apply the travel-and-expense policy to every receipt and card charge, then reconcile the card statement to the ledger.

## Checks
- No bill is scheduled for payment without completing its approval step.
- Payroll always shows the gross-to-net calculation, not the net figure alone.
- Every expense line is marked compliant or flagged against the written policy.

## Output
The requested process's result: AP approval queue and aging, AR aging and dunning log, payroll run and filing pack, or expense and card reconciliation.

## Example
A vendor bill routed for approval sits 4 days past the brand's own 3-day SLA for its amount tier; the aging report flags it by name before the vendor calls asking about it.
