---
name: prod/marketplace-compliance-check
owner: PROD
version: 1
invoke_when: a regulated-category listing is going live, or a certification is up for renewal
inputs: the product category, current FTC/Care Labeling/Prop 65/CPSC status (india: BIS/hallmarking status), certification renewal dates
outputs: a pass/block result naming exactly which requirement is or is not met
---
# Check US labelling and quality-marking compliance (FTC, Care Labeling, Prop 65)

## Purpose
A marketplace can pull a listing, or worse, penalize the account, for a missing FTC precious-metal quality mark, a missing textile Care Labeling Rule disclosure, or a missing Prop 65 warning. This check runs before a listing is built, not after a takedown notice. India: the same job checks BIS hallmarking and Legal Metrology labelling instead (markets: IN, reads null for US brands).

## Steps
1. Identify which compliance requirement applies to this specific category: the FTC Jewelry Guides quality mark (precious-metal jewellery), the Care Labeling Rule (fibre content, origin, care for textiles), a Prop 65 warning, or a CPSC rule (India: BIS certification for hardware/electronics/toys, hallmarking for jewellery, or Legal Metrology labelling; markets: IN).
2. Confirm the current certification, hallmark or disclosure status and its expiry date from the brand's own compliance record, not from an assumption that "it was fine last time."
3. If a required certification or disclosure is missing or expired, block the listing build entirely until it is resolved; do not proceed with a caveat or a "list now, fix later" workaround.

## Checks
- No listing for a regulated category proceeds to build before this check explicitly clears.
- Certification status is read from a recorded, dated fact, never assumed current.

## Output
{category_requirements[], certification_status, cleared}

## Output note
A real-time India BIS/hallmarking registry API was not found in the wave-2 research pass (markets: IN); that variant of this check reads a human-recorded status (BIS Care app or equivalent, checked by a person) rather than verifying a hallmark itself.

## Example
Category: gold jewellery, US listing. FTC Jewelry Guides quality mark (karat stamp, trademark) on file, documentation current. Cleared: true. India: the same jewellery SKU also needs a BIS hallmark certificate on file (markets: IN); a second SKU in the same batch had none, cleared: false, listing build blocked until resolved.
