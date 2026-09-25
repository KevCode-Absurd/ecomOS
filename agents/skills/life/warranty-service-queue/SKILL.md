---
name: warranty-service-queue
owner: LIFE
version: 1
invoke_when: a resizing, repair, re-plating, warranty or buyback/exchange request
  arrives
inputs: the service request, warranty terms, the repair partner network, courier
  pickup capability
outputs: logged and routed service requests, status update messages, cost-per-
  case tracking, closed case records
---
# Warranty, repair and after-sales service queue

## Purpose
Runs resizing, repair, re-plating, warranty and buyback/exchange requests end to
end: intake, coverage determination, courier pickup, repair-partner routing,
status updates, and cost-per-case tracking against the warranty reserve.

## Steps
1. Log the request type, product and purchase date.
2. Check the purchase date against the warranty window and determine coverage
   (in-warranty, paid out-of-warranty, or buyback/exchange), citing the specific
   clause.
3. Book courier pickup, confirming address and item with the customer first.
4. Route the item to the correct repair partner with a turnaround matched to
   that partner's real stated capacity.
5. Send a status update at intake, at drop-off, and at return dispatch, each
   reflecting a real status change.
6. Track the case's real cost (courier both ways, partner fee, any part) in code
   against the warranty reserve.
7. Close the case once the customer confirms receipt or the exchange completes.

## Checks
Coverage determination cites the specific warranty clause. Turnaround matches the
partner's real capacity. Cost computed in code from real invoices.

## Output
Logged and routed requests, status updates, per-case cost tracking, and closed
case records.

## Example
"Resizing request, purchased 4 months ago (in-warranty). Pickup booked, routed to
in-house jeweller, 3-day turnaround. Cost: $0 to customer, $18 to the reserve."
