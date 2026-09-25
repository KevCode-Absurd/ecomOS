---
name: prod/list-on-marketplace/zepto
owner: PROD
version: 1
invoke_when: the target marketplace is Zepto
select_by: {marketplace: zepto}
inputs: product copy, approved claims, category node, Zepto's thumbnail and pack-size spec
outputs: a short scan-friendly listing, thumbnail brief, and confirmed category placement
---
# List on Zepto

## Purpose
Zepto's listing surface shares quick commerce's thumbnail-first, seconds-to-decide shopping behaviour with
Blinkit, but its own app layout, category tree and thumbnail crop rules are separate and must be checked on their
own terms rather than assumed identical.

## Steps
1. Write a short, scan-friendly title readable at small thumbnail size, stating product and pack size plainly.
2. Confirm pack size and MRP are exact and match the current live price file, since Zepto's own ROAS reporting has
   the same MRP-based distortion Blinkit's does.
3. Brief the thumbnail image to Zepto's own small-format spec, checked for legibility at the actual render size in
   the app, not assumed identical to Blinkit's crop.
4. Confirm the correct dark-store category placement in Zepto's own category tree.

## Checks
- The title is legible and clear at actual thumbnail size in the Zepto app.
- The MRP shown matches the current live price exactly.

## Output
{listing_draft, thumbnail_brief, category_placement}

## Example
Same SKU as the Blinkit listing, built separately for Zepto's own crop and category tree rather than reused as-is,
since a thumbnail crop that works on one app can clip the product on the other.
