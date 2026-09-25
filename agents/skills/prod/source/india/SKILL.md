---
name: prod/source/india
owner: PROD
version: 1
invoke_when: the spec's supplier region is India
select_by: {region: india}
inputs: tech pack or open spec, MOQ needs
outputs: verified India supplier shortlist
---
# Source from India

## Purpose
India sourcing runs through different platforms and a different first-filter than overseas sourcing: GST and Udyam
status matter immediately, and mandatory certifications (BIS, FSSAI, Legal Metrology) gate a supplier before price
ever gets discussed.

## Steps
1. Search IndiaMART and category-specific B2B directories against the exact spec, not a loose category term.
2. Filter on GST registration and Udyam/MSME status first: an unregistered supplier is a compliance risk before it
   is a quality risk.
3. Message the shortlist with identical spec text, in the terms and format this platform's sellers expect (unit
   pricing, MOQ tiers stated up front).
4. Verify the top responders with a live video call, and check the category's mandatory certification (BIS for
   hardware/toys, FSSAI for food-contact, Legal Metrology for packaged goods).
5. Confirm real production capacity against the stated MOQ: ask for evidence of a comparable past order, not just
   a catalogue claim of capacity.

## Checks
- GST and Udyam status are checked before outreach proceeds.
- The certification checked matches the category's actual mandatory list, not a generic one.
- Capacity is confirmed with evidence, never assumed from a listing.

## Output
{shortlist[], verified[{name, gst, certification, capacity_confirmed}]}

## Example
Spec: FSSAI-regulated snack packaging. Shortlist of 9 from IndiaMART; 2 verified suppliers both hold valid FSSAI
licences (checked against the FSSAI portal) and Udyam registration; one showed a comparable 5,000-unit order as
capacity evidence.
