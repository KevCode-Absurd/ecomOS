---
name: prod/inventory-network-plan
owner: PROD
version: 1
invoke_when: a new sales channel is added, or the annual peak-season readiness plan is due
inputs: the stock pool across site/marketplaces/rapid-delivery platforms/stores, the per-channel buffer policy,
  the US peak-season retail calendar (Black Friday/Cyber Monday, Prime Day, Q4 holidays; india: the festive
  calendar), warehouse staffing and WMS/OMS capacity
outputs: multi-channel sync and routing rules, and a combined peak-season readiness plan
---
# Sync multi-channel stock and plan peak-season capacity

## Purpose
A stock pool split across channels without buffers oversells the moment two channels sell the last unit at once.
And a peak season fails in whichever of stock, staffing or system capacity was not planned for, not necessarily
the one that got the most attention. This skill keeps the pool synced day to day and plans for the season as one
combined picture. India: the same plan is built around the festive calendar (Diwali, wedding season) instead of
BFCM/Q4 (markets: IN).

## Steps
1. Keep one stock pool synced across every channel: site, marketplaces, rapid-delivery platforms, physical stores:
with a stated buffer per channel that prevents any one channel from overselling against real available stock.
2. Set order-routing and split-shipment rules by channel and warehouse, so an order is fulfilled from the right
location without a person deciding case by case.
3. Ahead of Q4/BFCM, project the safety stock the season will need using at least one prior peak cycle's data
where it exists, not a flat percentage bump (India: ahead of the festive season; markets: IN).
4. Check warehouse staffing and WMS/OMS system load against that projected peak volume, expressed as a percentage
of capacity used, not a yes/no guess.
5. Combine stock, staffing and system-load readiness into one plan, since a plan that only covers stock misses the
two failure modes that actually cause a bad peak season.

## Checks
- No channel is allowed to oversell against its stated buffer.
- The readiness plan explicitly covers stock, staffing and system load together, not stock alone.

## Output
{sync_status, routing_rules[], peak_projection, capacity_check, readiness_plan}

## Example
Buffers set: site 5%, marketplaces 8% (slower stock sync), rapid-delivery platforms 15% (fastest depletion risk).
Peak projection: BFCM week needs 2.4x baseline safety stock based on last year's data. Staffing check: current
warehouse shift covers 78% of projected peak pick volume: flagged for an extra shift. India: the same brand's
Diwali-week projection runs on the festive calendar instead (markets: IN).
