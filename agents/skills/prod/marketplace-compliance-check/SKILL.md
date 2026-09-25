---
name: prod/marketplace-compliance-check
owner: PROD
version: 1
invoke_when: a regulated-category listing is going live, or a certification is up for renewal
inputs: the product category, current BIS/hallmarking/labelling status, certification renewal dates
outputs: a pass/block result naming exactly which requirement is or is not met
---
# Check marketplace compliance (BIS, hallmarking, labelling)

## Purpose
A marketplace can pull a listing, or worse, penalize the account, for a missing BIS certification, an unhallmarked
jewellery item, or non-compliant labelling. This check runs before a listing is built, not after a takedown notice.

## Steps
1. Identify which compliance requirement applies to this specific category: BIS certification (many hardware,
   electronics and toy categories), hallmarking (jewellery), or specific labelling rules (textiles, food-adjacent
   categories).
2. Confirm the current certification or hallmark status and its expiry date from the brand's own compliance
   record, not from an assumption that "it was fine last time."
3. If a required certification is missing or expired, block the listing build entirely until it is resolved; do
   not proceed with a caveat or a "list now, fix later" workaround.

## Checks
- No listing for a regulated category proceeds to build before this check explicitly clears.
- Certification status is read from a recorded, dated fact, never assumed current.

## Output
{category_requirements[], certification_status, cleared}

## Output note
A real-time BIS/hallmarking registry API was not found in the wave-2 research pass; this check reads a
human-recorded status (BIS Care app or equivalent, checked by a person) rather than verifying a hallmark itself.

## Example
Category: gold jewellery. Hallmarking required. Status: hallmark certificate on file, valid through next year.
Cleared: true. A second SKU in the same batch had no hallmark certificate on file: cleared: false, listing build
blocked until resolved.
