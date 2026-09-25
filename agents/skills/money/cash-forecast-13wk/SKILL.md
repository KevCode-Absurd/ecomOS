---
name: money/cash-forecast-13wk
owner: MONEY
version: 1
invoke_when: cash needs forecasting or inventory cash and the cash conversion cycle need planning
inputs: bank balance, payroll calendar, ad spend plan, inventory on order, supplier lead times, AP/AR aging
outputs: 13-week cash table, lowest-cash flag, inventory cash plan, cash conversion cycle
---
# Build and monitor the 13-week cash forecast

## Purpose
Find the lowest cash point before it happens, and never let an inventory plan assume cash that will not be there.

## Steps
1. Pull bank balance, payroll calendar, ad spend plan, inventory on order and supplier lead times.
2. Build the rolling 13-week forecast week by week.
3. Reconcile this month's profit to free cash flow and check the 4 known cash traps (inventory build, tax timing, prepaid deposits, return timing).
4. Flag the lowest projected week at least 3 weeks ahead, with a sensitivity range.
5. Roll inventory forward against supplier lead time, targeting days-of-inventory to that lead time.
6. Track the cash conversion cycle (days inventory plus days receivable minus days payable) as one number with its 3 parts shown.

## Checks
- Inventory is never modeled to go negative.
- Profit and cash are reconciled explicitly, not assumed equal.
- The lowest point is flagged with enough lead time to act.

## Output
The 13-week table, the lowest-cash-week flag with sensitivity, the inventory cash plan and the cash conversion cycle.

## Example
Week 9 is flagged as the lowest point due to a supplier deposit and a state sales-tax payment landing the same week; the flag fires in week 5, giving 4 weeks to arrange a bridge.
