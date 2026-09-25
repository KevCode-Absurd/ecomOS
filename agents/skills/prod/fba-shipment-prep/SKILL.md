---
name: prod/fba-shipment-prep
owner: PROD
version: 1
invoke_when: an FBA shipment is being planned and needs dimension checks, a plan and a paper trail
inputs: measured case dimensions, FBA's current hard limits, a saved shipment template if one exists, carton labels
outputs: a checked shipment plan, carton labels, a complete paper trail, and receipt confirmation
---
# Prepare an FBA inbound shipment

## Purpose
FBA's dimension and weight limits change, and an outdated cached limit produces a rejected or delayed shipment.
Keeping the full paper trail matters because it is the only evidence available if inventory goes missing in
Amazon's own warehouse.

## Steps
1. Measure the actual case dimensions and check them against FBA's currently published hard limits, pulled fresh
   rather than from a cached figure from a past shipment.
2. Reuse a saved shipment template whenever this SKU and case size match a shipment already sent successfully,
   to avoid re-deriving the plan from scratch each time.
3. Build the shipment plan: box count, weight per box (checked under the carrier's per-box limit), and carrier
   choice.
4. Generate and check carton labels against FBA's current label specification before printing.
5. Keep the full paper trail: bill of lading, carrier receipt, carton count: so a later lost-inventory claim has
   the evidence it needs.
6. Confirm the shipment against Amazon's inbound dashboard once it is marked received, and flag any discrepancy
   between what was sent and what was received.

## Checks
- The dimension limits used are the currently published ones, not a cached figure.
- The paper trail is complete before the shipment physically leaves.

## Output
{dimension_check, shipment_plan, carton_labels, paper_trail, receipt_confirmation}

## Example
Case dimensions checked against FBA's current oversize threshold: under by 2cm. Template reused from the last
shipment of the same SKU. 40 cartons, weight checked under the carrier's 25kg/box limit. Paper trail filed; receipt
confirmed 6 days later with a 2-unit discrepancy flagged for a claim.
