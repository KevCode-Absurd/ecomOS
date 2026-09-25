---
name: prod/daily-shipping-ops
owner: PROD
version: 1
invoke_when: an order needs a courier picked in real time, or today's NDR queue needs same-day resolution
inputs: a live courier rate feed, pincode serviceability data, SLA history per courier per zone, today's NDR queue,
  a customer contact channel
outputs: a per-order courier choice with failover, and today's NDR resolution log
---
# Run daily courier rate-shop and NDR resolution

## Purpose
A fixed default carrier for every shipment ignores real, live differences in rate, serviceability and reliability
by zone. And an NDR left unworked past the courier's attempt window becomes an RTO that did not need to happen.
This skill runs both the routing decision and the same-day NDR response as one daily operating rhythm.

## Steps
1. Pick the courier for each shipment in code, from live rate, pincode serviceability, and the courier's own SLA
   history in that specific zone: never a single fixed default carrier used everywhere.
2. Fail over automatically to a backup courier the moment the primary courier fails serviceability or its SLA for
   that shipment, without waiting for a manual check.
3. Pull every non-delivery report raised today, and confirm the address or reschedule delivery with the customer
   before the courier's own attempt window closes.
4. Log the outcome of every routing decision and every NDR resolution, and flag any zone showing a rising NDR or
   RTO trend for the monthly courier scorecard.

## Checks
- Every courier choice is computed from live data, never defaulted to one fixed carrier.
- Every NDR raised today is worked the same day, before its attempt window closes.

## Output
{courier_choice, failover_event, ndr_outcomes[]}

## Example
Order routed to Courier A on best rate/SLA for pincode 400001; Courier A's API reported non-serviceable mid-day,
failed over automatically to Courier B. Same-day NDR queue: 14 items, 11 resolved by address confirmation, 2
rescheduled, 1 marked RTO after 2 failed contact attempts.
