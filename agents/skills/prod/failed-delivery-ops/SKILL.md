---
name: prod/failed-delivery-ops
owner: PROD
version: 1
invoke_when: an order needs a carrier picked in real time, or today's carrier-exception queue needs same-day resolution
inputs: a live carrier rate feed, ZIP code serviceability data, SLA history per carrier per zone, today's carrier-exception queue (undeliverable-as-addressed, failed attempt), a customer contact channel
outputs: a per-order carrier choice with failover, and today's exception-resolution log
---
# Run daily carrier rate-shop and failed-delivery resolution

## Purpose
A fixed default carrier for every shipment ignores real, live differences in rate, serviceability and reliability by zone. And a carrier exception (address issue, failed attempt) left unworked past the delivery window becomes a return-to-sender that did not need to happen. This skill runs both the routing decision and the same-day exception response as one daily operating rhythm. India: the same daily rhythm runs as NDR (non-delivery report) resolution on cash-on-delivery orders (markets: IN, reads null for US brands).

## Steps
1. Pick the carrier for each shipment in code, from live rate, ZIP code serviceability, and the carrier's own SLA history in that specific zone (UPS, USPS, FedEx, or a connected 3PL such as ShipBob or ShipMonk): never a single fixed default carrier used everywhere.
2. Fail over automatically to a backup carrier the moment the primary fails serviceability or its SLA for that shipment, without waiting for a manual check.
3. Pull every carrier exception raised today, run USPS/carrier address validation, and confirm the address or reschedule delivery with the customer by SMS (TCPA consent, quiet hours) or email before the carrier's own attempt window closes (India: pull the aggregator's NDR queue and confirm by SMS or WhatsApp; markets: IN).
4. Log the outcome of every routing decision and every exception resolution, and flag any zone showing a rising return-to-sender trend for the monthly carrier scorecard (India: a rising NDR or RTO trend; markets: IN).

## Checks
- Every carrier choice is computed from live data, never defaulted to one fixed carrier.
- Every exception raised today is worked the same day, before its attempt window closes.

## Output
{carrier_choice, failover_event, exception_outcomes[]}

## Example
Order routed to UPS on best rate/SLA for ZIP 10001; UPS's API reported non-serviceable mid-day, failed over automatically to USPS. Same-day exception queue: 14 items, 11 resolved by address confirmation, 2 rescheduled, 1 marked return-to-sender after 2 failed contact attempts. India: same day's NDR queue for pincode 400001 worked the same way, 1 marked RTO (markets: IN).
