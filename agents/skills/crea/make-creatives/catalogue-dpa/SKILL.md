---
name: make-creatives/catalogue-dpa
owner: crea-paid-creative-copy
version: 1
invoke_when: the job covers many SKUs from the product feed: a new catalogue or
  DPA campaign, or a feed schema change
inputs: product feed, brand kit, reusable copy block set
outputs: overlay template, full variant grid, SKU-level risk flags
---
Purpose: build a price and badge overlay template and generate the full
catalogue-scale ad grid, since these follow a fixed module system unlike a
one-off static, and a template that fails on one SKU fails silently at scale.

Steps
1. Audit the feed's price and image fields for gaps, wrong formats or stale
   data first; building a template on dirty data hides the real problem.
2. Design the overlay: price, discount badge, any urgency badge, tested against
   the single longest real price string in the feed and the smallest real
   product image, not an average case.
3. Write or reuse a small set of copy blocks that plug into any SKU's fields
   without reading oddly for an outlier product name or price.
4. Generate the variant grid by combining template, feed fields and copy
   blocks through the creative studio's variant endpoint.
5. Spot-check a random sample, not just the first few SKUs, for correct price,
   image and copy pairing.
6. Flag every SKU-specific risk by name: a badge overlapping a long price, a
   missing image, a discontinued SKU still marked active.

Checks: template survives the extreme cases in the feed; every risk names a
SKU, not a category.

Output: overlay template file, the generated variant grid, and a risk list.

Example: a Black-Friday-sale badge overlaps a 6-digit price on 4 SKUs out of
800; the audit catches it before the DPA campaign goes live, not after.
