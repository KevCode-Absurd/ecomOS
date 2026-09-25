---
name: prod/non-standard-ops/export
owner: PROD
version: 1
invoke_when: the classified non-standard-ops type is export or cross-border
select_by: {type: export}
inputs: origin/destination country, product HTS/HS code, shipment value
outputs: customs bond and HTS status, tariff exposure, Section 321 eligibility, commercial invoice, chosen incoterm, and export paperwork
---
# Cross-border compliance: US customs, tariffs and international shipping

## Purpose
A first international sourcing shipment or a first outbound international order each has its own paperwork and
duty-exposure decisions that a domestic shipment never touches. Getting the incoterm wrong surprises the buyer
with an unexpected duty bill and damages the relationship on the very first order; getting an HTS classification
wrong on an inbound shipment causes a customs hold or a duty overpayment. India: the equivalent event is an export
from India, which instead needs IEC and LUT registration for zero-rated GST (markets: IN, reads null for US
brands).

## Steps
1. For an inbound sourcing shipment, secure a customs bond (continuous or single-entry) and classify each product
by its correct HTS code against the current US tariff schedule.
2. Check tariff exposure for that HTS code and country of origin, and whether the shipment qualifies for Section
321 de minimis entry (currently for shipments under $800 per person per day) to avoid duty and formal entry where
eligible.
3. For an outbound international order, prepare the commercial invoice and the carrier's export paperwork,
matching HTS/HS codes and shipment value exactly, and choose DDP (duty paid by the seller) or DDU (duty paid by
the buyer) so the buyer's total cost is clear before they order, not discovered at their own customs.
4. India (markets: IN): set up IEC (Import Export Code) and LUT (Letter of Undertaking) so exports can be
zero-rated for GST, and determine HS codes against the destination country's tariff schedule instead of the US's.

## Checks
- HTS/HS codes are checked against the actual current schedule, not assumed from a prior shipment's code.
- The incoterm choice is communicated to the buyer before the order ships, not after.

## Output
{customs_bond_status, hts_codes[], tariff_exposure, section_321_eligible, commercial_invoice, incoterm, export_paperwork}

## Example
Inbound shipment from a China supplier, value $18,000: continuous customs bond confirmed active, HTS code checked
against the current schedule, tariff exposure computed, does not qualify for Section 321 given per-shipment value.
Outbound order to Canada: incoterm DDP chosen so the buyer sees one all-in price with no duty surprise on
delivery. India: first order to UAE instead runs on IEC/LUT (markets: IN), HS code checked against UAE's tariff
schedule, incoterm DDP chosen the same way.
