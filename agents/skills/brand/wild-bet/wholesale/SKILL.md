---
name: wild-bet/wholesale
owner: BRAND
version: 1
invoke_when: the bet's type is a wholesale buyer entry
inputs: target buyer type, unit economics at wholesale margin, product line
outputs: feasibility packet, type-specific execution brief
---
# Wild bet: wholesale entry

## Purpose
Wholesale changes the brand's margin structure and puts the product's story in someone else's retail environment. This skill checks the deal survives on the numbers before any buyer pitch goes out.

## Steps
1. Recompute unit economics at a realistic wholesale margin cut (commonly 50% off retail); check the deal is still profitable at the brand's real COGS, not the retail-margin COGS assumption.
2. Build the line sheet: SKUs offered, wholesale price per unit, minimum order quantity, and lead time, pulling MOQ and lead time from Product and Supply rather than guessing.
3. Build the buyer-facing pitch deck: brand story, positioning, sell-through data if any exists, and the line sheet.
4. Write the execution brief around the smallest real buyer commitment (one boutique, one small chain) as the pilot, before a broader wholesale push.

## Checks
- Wholesale-margin unit economics are computed in code from real COGS, not the retail-margin figure reused by mistake.
- MOQ and lead time come from Product and Supply's real numbers.

## Output
`{feasibility_packet: {wholesale_unit_economics, line_sheet}, execution_brief: {buyer_pitch_deck, pilot_buyer}}`

## Example
Retail margin is 55%; at a 50% wholesale discount, contribution margin per unit drops from ₹420 to ₹190: still positive, so the pilot proceeds with one boutique buyer at a 25-unit MOQ.
