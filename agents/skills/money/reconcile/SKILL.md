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
Every outside source (a gateway, a marketplace, a card network dispute, an ad platform, or for an India-selling brand a COD courier) pays, bills or reverses money on its own schedule and its own math. This skill is the dispatcher: it picks the right sub-skill by source and never lets a gap get filed away as rounding.

## Steps
1. Pull the source's statement for the period.
2. Match `select_by.source` to gateway, marketplace, ad-platform-invoices, chargebacks, or cod-courier (India option) and hand off to that child skill.
3. Run `money.reconciliation` with the source's own unbundling rule (fee, commission, facilitator sales tax or GST/TCS on fee, refund, shipping fee as separate lines).
4. Match the unbundled total to the actual bank credit or the actual ad spend logged.
5. Name a cause for every gap over a small tolerance.
6. Draft the journal entry from the unbundled lines, one entry per settlement.

## Checks
- No gap is left unexplained.
- Facilitator sales tax (or TCS and GST for India) on fees are always their own lines.
- The matched total ties to a real bank credit, not an assumption.

## Output
A reconciliation table with source, period, matched total, gap total, named gap causes and draft journal entries.

## Example
A Meta invoice of $4,230 for the month is matched against $4,185 logged in the spend dashboard. The $45 gap is named: a late-arriving credit from the prior invoice, not rounding.
