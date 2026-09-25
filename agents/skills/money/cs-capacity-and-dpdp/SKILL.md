---
name: money/cs-capacity-and-dpdp
owner: MONEY
version: 1
invoke_when: CS staffing needs sizing or a CCPA/CPRA data-subject request arrives (a DPDP request for India-selling brands)
inputs: sales forecast curve, ticket volume and cost, system map, request details
outputs: CS staffing plan and cost per ticket, or a data-subject response with a system-by-system data map
---
# Plan CS capacity and handle CCPA/CPRA data-subject requests (DPDP for India)

## Purpose
Size support to the forecast, not the last headcount, and protect a customer's CCPA/CPRA rights (DPDP rights for an India-selling brand) across every system that holds their data.

## Steps
1. Staff CS tiers from the sales forecast curve and track cost per ticket by tier.
2. Define what counts as a complex ticket before it gets routed to a higher tier.
3. When resolution time rises, trace the cause upstream instead of just adding headcount.
4. On a CCPA/CPRA access, deletion or opt-out request (a DPDP access or erasure request, for India), find every system holding that person's data: ESP, helpdesk, loyalty, subscription, order records.
5. Assemble the data for an access request, or prepare the deletion/erasure plan across every located system, respecting any legal retention obligation.
6. Confirm the response goes out inside the statutory deadline and log the request.

## Checks
- Staffing scales with the forecast curve.
- Every connected system is checked for a data-subject request; none are skipped.
- A deletion or erasure never removes data needed for an open legal or tax obligation.

## Output
The requested task's result: a CS staffing plan with cost per ticket, or a completed data-subject response with its system-by-system data map.

## Example
A deletion request would delete an order record still needed for a live sales-tax audit trail (a GST audit trail for India); the plan erases the customer's marketing and support data while retaining the order record with a stated legal reason.
