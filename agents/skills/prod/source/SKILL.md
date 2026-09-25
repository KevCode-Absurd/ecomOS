---
name: prod/source
owner: PROD
version: 1
invoke_when: a validated spec or SKU needs a supplier found, vetted, or kept under a standing watch
inputs: tech pack or open spec, MOQ needs, supplier region (US domestic, China, or India)
outputs: verified supplier shortlist, agent vetting result, standing watch alert
---
# Source a spec through supplier discovery

## Purpose
This is the parent procedure for finding a supplier. The mechanics of discovery differ sharply by region: different
platforms, different verification norms, different negotiating culture: so this skill routes to a region-specific
child rather than running one generic funnel everywhere. The brand's default sourcing region is US domestic; China
and India are the other two supported regions.

## Steps
1. Read the spec's stated region preference (or the brand's default sourcing region) and select the matching child
   skill: `prod/source/us-domestic`, `prod/source/china`, or `prod/source/india`.
2. Run that child's discovery funnel: broad platform search against the exact spec, messaging a wide shortlist on
   identical terms.
3. Verify every top responder with a live video call and a certification document check: never add a supplier to
   the verified list on written claims alone.
4. If a sourcing agent is used instead of contacting a factory directly, vet the agent to the same standard as a
   factory: verified references, a live call, checkable past shipments.
5. For an open, ongoing spec, leave it running in the background against the region's own major platforms so a
   better or new supplier surfaces without a person re-running the search by hand.

## Checks
- The region-specific child procedure was used, not a generic one.
- Every verified supplier passed a video call and a certification check.
- The background watch only produces an alert; it never contacts a supplier on its own.

## Output
{shortlist[], verified[], agent_vetting[], watch_alert}

## Example
Spec: 500ml insulated bottle, MOQ 3,000. Region: India (markets: IN). Ran `prod/source/india` against IndiaMART;
shortlist of 14, verified 3 by video call and BIS certificate check, one sourcing agent vetted against two of his
past client shipments before being trusted with outreach. For a US-domestic brand, the same spec instead runs
`prod/source/us-domestic` against ThomasNet and Maker's Row.
