---
name: prod/source/us-domestic
owner: PROD
version: 1
invoke_when: the spec's supplier region is US domestic (the brand's default region)
select_by: {region: us-domestic}
inputs: tech pack or open spec, MOQ needs
outputs: verified US-domestic supplier shortlist
---
# Source domestically in the US

## Purpose
US-domestic sourcing runs through different directories and a different first filter than overseas sourcing:
business registration and state licensing matter immediately, and category-specific certification (UL for
electrical goods, FDA for food or cosmetics, CPSC for children's products) gates a supplier before price is
discussed. This is the brand's default sourcing region.

## Steps
1. Search ThomasNet, Maker's Row and, for finished-goods wholesale rather than manufacturing, Faire or Tundra
   against the exact spec, not a loose category term.
2. Filter on business registration, EIN and any state manufacturing or trade licence first: an unregistered
   supplier is a compliance risk before it is a quality risk.
3. Message the shortlist with identical spec text, stating unit pricing and MOQ tiers up front.
4. Verify the top responders with a live video call or a facility visit, and request the certification the
   category requires (UL for electrical/hardware, FDA for food-contact or cosmetics, CPSC for children's
   products).
5. Confirm real production capacity against the stated MOQ: ask for evidence of a comparable past order, not
   just a catalogue claim of capacity.

## Checks
- Business registration and licence status are checked before outreach proceeds.
- The certification checked matches the category's actual requirement, not a generic list.
- Capacity is confirmed with evidence, never assumed from a listing.

## Output
{shortlist[], verified[{name, business_registration, certification, capacity_confirmed}]}

## Example
Spec: FDA-regulated snack packaging. Shortlist of 7 from ThomasNet; 2 verified suppliers both hold current state
food-manufacturing licences (checked against the state registry) and FDA facility registration; one showed a
comparable 5,000-unit order as capacity evidence.
