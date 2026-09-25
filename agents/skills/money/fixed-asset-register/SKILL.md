---
name: money/fixed-asset-register
owner: MONEY
version: 1
invoke_when: a capital purchase happens or the monthly depreciation schedule needs running
inputs: capital purchase invoices, current asset register, useful life policy
outputs: updated register with running depreciation balance
---
# Maintain the fixed asset register and depreciation schedule

## Purpose
Keep one register of every asset the brand owns (equipment, fixtures, website build cost, packaging dies) so depreciation never gets estimated at year end.

## Steps
1. Log any new capital purchase with its date, cost and category.
2. Assign useful life from the brand's stated policy, not a one-off guess.
3. Run the month's depreciation for every asset in the register.
4. Update each asset's running balance.

## Checks
- Every asset carries purchase date, useful life and a running balance.
- No capital purchase this month is missing from the register.

## Output
The updated register with this month's depreciation line per asset.

## Example
A new packaging die purchased for $2,200 with a 3-year useful life adds about $60 of depreciation to this month's P&L ladder automatically.
