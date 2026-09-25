---
name: prod/non-standard-ops/export
owner: PROD
version: 1
invoke_when: the classified non-standard-ops type is export
select_by: {type: export}
inputs: destination country, product HS code, shipment value
outputs: IEC/LUT status, HS codes, commercial invoice, chosen incoterm, and export paperwork
---
# Export compliance and international duties

## Purpose
A first international order or a new export market has its own paperwork and duty-exposure decisions that a
domestic shipment never touches. Getting the incoterm wrong surprises the buyer with an unexpected duty bill and
damages the relationship on the very first order.

## Steps
1. Set up IEC (Import Export Code) and LUT (Letter of Undertaking) so exports can be zero-rated for GST.
2. Determine the correct HS code for each shipped product against the destination country's tariff schedule.
3. Prepare the commercial invoice and the courier's export paperwork, matching the HS codes and shipment value
   exactly.
4. Choose DDP (duty paid by the seller) or DDU (duty paid by the buyer) so the buyer's total cost is clear before
   they order, not discovered at their own customs.

## Checks
- HS codes are checked against the actual destination country's schedule, not assumed from the home market's code.
- The incoterm choice is communicated to the buyer before the order ships, not after.

## Output
{iec_lut_status, hs_codes[], commercial_invoice, incoterm, export_paperwork}

## Example
First order to UAE. IEC and LUT confirmed active. HS code checked against UAE's tariff schedule. Incoterm: DDP,
so the buyer sees one all-in price with no duty surprise on delivery.
