---
name: prod/shipment-readiness
owner: PROD
version: 1
invoke_when: a production run is ready to ship and needs inspection, freight mode and 3PL selection before it leaves
inputs: production run details, this SKU's defect history, shipment weight and volume, the launch date, cash cover
  available for freight
outputs: inspection result and disposition log, plus the freight mode and 3PL recommendation
---
# Clear a shipment for departure

## Purpose
A shipment that leaves uninspected, on the wrong freight mode, or with a 3PL picked on price alone turns into a
launch-date or cash problem weeks later. This skill runs the pre-departure checklist as one gate.

## Steps
1. Book third-party inspection before the container leaves the factory: never after it has already shipped.
2. Size the acceptable defect buffer from this specific SKU's own defect history, not an industry-standard flat
   percentage. A SKU with a clean history gets a tighter buffer; one with past issues gets a wider one and closer
   scrutiny.
3. Record a disposition decision for every defective unit the inspection finds: rework, discount-and-ship, or
   discard. No unit is left undecided.
4. Pick the freight mode: air, sea, or a hybrid split: based on the shipment's weight, the launch date it needs
   to hit, and the cash the brand has available to cover air freight's premium.
5. Select the 3PL on service history (on-time rate, damage rate) rather than the lowest quote, and check
   cross-border duty thresholds and paperwork before committing to the booking.

## Checks
- The defect buffer is sized from the SKU's own real history, not a generic figure.
- The 3PL selection cites service history, not just price.
- Cross-border thresholds are checked before the shipment is booked, not discovered at customs.

## Output
{inspection_result, disposition_log[], freight_mode, threepl, threshold_check}

## Example
Inspection found 2.1% defects (buffer was set at 3% from history): all disposed as discount-and-ship. Freight:
hybrid (60% sea to save cash, 40% air to hit the launch date). 3PL selected on a 97% on-time history despite a 4%
higher quote than the cheapest bidder. Duty threshold checked and cleared before booking.
