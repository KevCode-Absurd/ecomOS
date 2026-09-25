---
name: prod/source/china
owner: PROD
version: 1
invoke_when: the spec's supplier region is China
select_by: {region: china}
inputs: tech pack or open spec, MOQ needs
outputs: verified China supplier shortlist
---
# Source from China

## Purpose
China sourcing runs through Alibaba, Global Sources and trade-assurance mechanisms that do not exist the same way
in India sourcing, and certification requirements are about the destination import market, not the origin.

## Steps
1. Search Alibaba and Global Sources against the exact spec, filtering out pure trading companies unless the spec
   explicitly allows one.
2. Filter first on trade assurance eligibility and years verified on-platform: both are a cheap first signal of
   real operating history.
3. Message the shortlist with identical spec text and the same requested volume tiers, so quotes are comparable.
4. Verify the top responders with a live video call and request the third-party certification documents the
   destination market requires (CE, RoHS, BIS for import into India, as relevant to the product category).
5. Confirm whether a backup, second factory exists for any component this supplier is the sole source of, to avoid
   building single-supplier concentration risk into the SKU from day one.

## Checks
- Trade assurance and on-platform verification are checked before outreach, not after a quote arrives.
- The certification requested matches the destination market's import rules, not a generic list.
- A backup factory is identified wherever a component is single-sourced.

## Output
{shortlist[], verified[{name, trade_assurance, certification, backup_identified}]}

## Example
Spec: injection-molded component, MOQ 5,000. Shortlist of 11 from Alibaba; 3 verified with trade assurance and 4+
years on-platform; one held BIS-compliant certification needed for India import; a backup factory for the same mold
was identified in the same province.
