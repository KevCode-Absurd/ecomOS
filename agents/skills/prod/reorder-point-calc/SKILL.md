---
name: prod/reorder-point-calc
owner: PROD
version: 1
invoke_when: weekly SKU reorder planning is due, across both DTC and Amazon FBA channels
inputs: velocity by channel, lead time per supplier, the safety-stock policy, the committed channel push plan,
  Amazon IPI and storage limits where relevant
outputs: reorder point and safety stock per SKU, a stockout-risk flag, and FBA-specific replenishment sizing
---
# Compute reorder point and channel replenishment

## Purpose
A reorder point sized from trailing sales alone misses two India-specific risks: festive demand spikes and
COD-market RTO reversing what looked like a sale. It also misses that Amazon FBA has its own IPI and storage limits
that can block a restock even when stock is genuinely needed.

## Steps
1. Pull real velocity and real lead time per SKU per channel. A subscription or bundle SKU uses its committed
   cadence (what customers actually signed up for), never trailing sales, since trailing sales lag a subscription's
   real demand.
2. Compute reorder point and safety stock in code, with an explicit adjustment for India-specific spike risk:
   festive-season demand surges and the reversal risk from COD RTO.
3. Compare current stock against the computed reorder point and flag any SKU already below it or projected to fall
   below it within the lead time window.
4. For Amazon SKUs, size the FBA replenishment shipment from a real inventory-cover target, treating a stockout as
   the failure mode to avoid above almost any other cost. Check the current IPI score and storage limits before
   finalizing the shipment size, since a low IPI score can cap how much can be sent in.

## Checks
- Velocity and lead time are real, current numbers, never a stale default.
- The spike-risk adjustment is shown explicitly, not folded silently into the number.
- An IPI or storage-limit flag is raised before it blocks a planned restock, not after.

## Output
{sku, reorder_point, safety_stock, current_stock, status, fba_cover, ipi_flag}

## Example
SKU-1042: velocity 40/day, lead time 18 days, festive-adjusted safety stock +35%. Reorder point 1,080 units;
current stock 950: status: reorder now. FBA cover target 45 days; IPI score 420 (above the 400 threshold): no
restock block.
