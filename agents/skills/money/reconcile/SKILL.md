---
name: money/reconcile
owner: MONEY
version: 1
invoke_when: a payout, remittance or invoice from outside the brand needs matching to the books
inputs: source statement, bank statement or spend dashboard, chart of accounts
outputs: reconciliation table, gap causes, draft journal entries
---
# Reconcile a settlement source

## Purpose
Every outside source (a gateway, a marketplace, a COD courier, an ad platform) pays or bills the brand on its own schedule and its own math. This skill is the dispatcher: it picks the right sub-skill by source and never lets a gap get filed away as rounding.

## Steps
1. Pull the source's statement for the period.
2. Match `select_by.source` to gateway, marketplace, cod-courier or ad-platform-invoices and hand off to that child skill.
3. Run `money.reconciliation` with the source's own unbundling rule (fee, commission, TCS, GST on fee, refund, shipping fee as separate lines).
4. Match the unbundled total to the actual bank credit or the actual ad spend logged.
5. Name a cause for every gap over a small tolerance.
6. Draft the journal entry from the unbundled lines, one entry per settlement.

## Checks
- No gap is left unexplained.
- TCS and GST on fees are always their own lines.
- The matched total ties to a real bank credit, not an assumption.

## Output
A reconciliation table with source, period, matched total, gap total, named gap causes and draft journal entries.

## Example
A Meta invoice of 42,300 rupees for the month is matched against 41,850 rupees logged in the spend dashboard. The 450 rupee gap is named: a late-arriving GST correction from the prior invoice, not rounding.
