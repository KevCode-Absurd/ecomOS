---
name: prod/non-standard-ops/offline-retail
owner: PROD
version: 1
invoke_when: the classified non-standard-ops type is offline retail
select_by: {type: offline_retail}
inputs: event dates and location, consignment terms, staff roster
outputs: POS setup, stock transfer log, daily reconciliation, and final settlement
---
# Offline retail, stockist and pop-up operations

## Purpose
A pop-up, exhibition or stockist arrangement moves real physical stock outside the normal warehouse-to-courier
flow, and needs its own POS, its own stock accounting, and its own daily discipline so nothing is lost between
what left the warehouse and what actually sold or came back.

## Steps
1. Set up point-of-sale for the event or the stockist location.
2. Run the stock transfer to the location, and track any returns or unsold stock coming back.
3. Reconcile consignment settlement (what the stockist owes for what actually sold) and daily sales for the
   duration of the event.
4. Run the staff roster for the event, matched to expected footfall.

## Checks
- Daily reconciliation happens every single day of the event, not only at the end.
- Every unit transferred out is matched against a unit sold or a unit returned; nothing is unaccounted for.

## Output
{pos_setup, stock_transfer_log, daily_reconciliation[], settlement}

## Example
3-day pop-up: 400 units transferred. Daily reconciliation each day matched sales against POS records. Final
settlement: 340 sold, 55 returned unsold, 5 flagged as a discrepancy for follow-up with the venue.
