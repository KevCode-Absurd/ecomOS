---
name: money/pnl-close-checklist
owner: MONEY
version: 1
invoke_when: the monthly close needs a P&L ladder and a close checklist run
inputs: chart of accounts, order and cost export, reconciled settlement lines, prior ladder
outputs: P&L ladder, close checklist result, change note
---
# Build the P&L ladder and run the close checklist

## Purpose
Turn raw order and cost exports into a labeled, comparable P&L ladder, and confirm the close is actually complete before anyone reads the numbers.

## Steps
1. Apply the brand's fixed decision tree for what counts as COGS, cost of delivery, marketing cost and OPEX.
2. Build the ladder line by line from gross revenue down to net profit.
3. Run the close checklist: bank reconciliations complete, accruals booked, inventory valuation current, deferred revenue correctly held.
4. Diff this month's ladder against last month's and name the single biggest driver of change.

## Checks
- Every ladder line traces to a source document or a reconciliation output.
- No cost appears in both COGS and OPEX.
- A percent-of-revenue column sits next to every ladder line.

## Output
The P&L ladder, the close checklist with a pass or fail per item, and one paragraph naming the biggest change.

## Example
Net profit percent drops 3 points month over month; the diff names the driver as a spike in carrier shipping fees, not a vague 'costs went up'.
