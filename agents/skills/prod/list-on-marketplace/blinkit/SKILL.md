---
name: prod/list-on-marketplace/blinkit
owner: PROD
version: 1
invoke_when: the target marketplace is Blinkit
select_by: {marketplace: blinkit}
inputs: product copy, approved claims, category node, Blinkit's thumbnail and pack-size spec
outputs: a short scan-friendly listing, thumbnail brief, and confirmed category placement
---
# List on Blinkit

## Purpose
Quick commerce listings are read at thumbnail size on a phone in seconds, not read in depth like a marketplace
product page. Copy and images that work on Amazon or a DTC site are usually too dense here.

## Steps
1. Write a short, scan-friendly title that reads clearly even at small thumbnail size: no long benefit strings,
   just what the product is and its pack size.
2. Confirm the pack size and MRP shown are exact and match the brand's current, live pricing; a stale MRP here is
   a common source of the ROAS-distortion problem Blinkit's own dashboards create.
3. Brief the thumbnail image to Blinkit's small-format spec, checking it is legible at the size it actually
   renders at, not just at full resolution.
4. Confirm the correct dark-store category placement so the product surfaces in the right in-app browse category.

## Checks
- The title is legible and clear when previewed at actual thumbnail size.
- The MRP shown matches the current live price exactly.

## Output
{listing_draft, thumbnail_brief, category_placement}

## Example
Product: 500ml juice bottle. Title: "Brand Fresh Juice 500ml": reads clearly at thumbnail size. MRP confirmed
against the live price file. Thumbnail brief specifies a bold product-forward crop, checked legible at the app's
actual small-tile size.
