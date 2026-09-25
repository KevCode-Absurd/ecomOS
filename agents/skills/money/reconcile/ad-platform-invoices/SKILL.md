---
name: money/reconcile/ad-platform-invoices
owner: MONEY
version: 1
invoke_when: an ad platform's invoice needs matching to what the spend dashboard reports
inputs: platform invoice, spend dashboard export, ad account payment method
outputs: invoice-to-dashboard reconciliation line
---
# Reconcile ad platform invoices to logged spend

## Purpose
Ad platforms bill on their own cycle, which rarely lines up cleanly with a calendar month or with the currency the dashboard reports in. This skill catches the gap before it distorts the P&L's marketing cost line.

## Steps
1. Pull the platform's invoice for the billing period.
2. Pull the dashboard's logged spend for the matching period, as a period total, never an average of daily figures.
3. Compare the two totals directly.
4. If they differ, check for a billing-cycle boundary mismatch, a currency conversion difference, or a credit or refund applied by the platform.
5. Name the exact cause; never file the gap as unexplained variance.

## Checks
- Comparison always uses period totals, never daily averages.
- A currency conversion gap states the rate used on each side.
- The gap becomes a line in the platform-to-books reconciliation, not a silent write-off.

## Output
One line per platform per period: invoiced amount, logged amount, gap, and the named cause.

## Example
Meta's invoice covers the 3rd to the 2nd of the next month, while the dashboard reports calendar months; the resulting $620 shift is named as a billing-cycle boundary, not a spend discrepancy.
