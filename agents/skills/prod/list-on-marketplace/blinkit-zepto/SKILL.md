---
name: prod/list-on-marketplace/blinkit-zepto
owner: PROD
version: 1
invoke_when: the target marketplace is Blinkit or Zepto (markets: IN; not selected for a US-only brand)
select_by: {marketplace: blinkit|zepto}
inputs: product copy, approved claims, category node, the platform's thumbnail and pack-size spec
outputs: a short scan-friendly listing, thumbnail brief, and confirmed category placement
---
# List on Blinkit and Zepto

## Purpose
India only (markets: IN): quick commerce listings on Blinkit and Zepto are read at thumbnail size on a phone in
seconds, not read in depth like a marketplace product page; this grouped child covers both since they share the
same thumbnail-first discipline while each keeps its own app layout, category tree and crop rule. It does not run
for a US-only brand, whose rapid-delivery/grocery listings (Instacart, DoorDash, Gopuff) are built under the
quick-commerce-onboard skill instead, since those platforms are not part of this marketplace tree.

## Steps
1. Write a short, scan-friendly title that reads clearly even at small thumbnail size: no long benefit strings,
   just what the product is and its pack size.
2. Confirm the pack size and MRP shown are exact and match the brand's current, live pricing; a stale MRP here is
   a common source of the ROAS-distortion problem these platforms' own dashboards create.
3. Brief the thumbnail image to the chosen platform's own small-format spec, checked for legibility at the actual
   render size in the app, not assumed identical between Blinkit and Zepto: a thumbnail crop that works on one can
   clip the product on the other, so each is built separately even for the same SKU.
4. Confirm the correct dark-store category placement in that platform's own category tree.

## Checks
- The title is legible and clear when previewed at actual thumbnail size.
- The MRP shown matches the current live price exactly.

## Output
{marketplace, listing_draft, thumbnail_brief, category_placement}

## Example
Product: 500ml juice bottle. Title: "Brand Fresh Juice 500ml": reads clearly at thumbnail size. MRP confirmed
against the live price file. Built separately for Blinkit's and Zepto's own crop and category tree rather than
reused as-is.
