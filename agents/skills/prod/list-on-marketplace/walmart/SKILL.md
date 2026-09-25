---
name: prod/list-on-marketplace/walmart
owner: PROD
version: 1
invoke_when: the target marketplace is Walmart Marketplace
select_by: {marketplace: walmart}
inputs: product copy, approved claims, keyword list, category node, Walmart's image and attribute spec, GTIN/UPC
outputs: title, key features, image slot briefs, filled category attributes
---
# List on Walmart Marketplace

## Purpose
Walmart's title style, required GTIN/UPC and Content Hub rich-media rules differ from Amazon's, and its search
ranking (grading via the Listing Quality score) weighs different fields. A copy-pasted Amazon listing under-
performs here.

## Steps
1. Place the top keyword in the title, respecting Walmart's own character limit and title-style guide, which
   discourages promotional language Amazon tolerates.
2. Write the key features and long description in Walmart's own field structure, matching its Listing Quality
   scoring criteria.
3. Brief every image slot Walmart allows to its own spec, including any Content Hub rich-media module the
   category supports.
4. Fill every category-specific attribute Walmart requires and confirm a valid GTIN or UPC is attached; a missing
   or invalid GTIN blocks the listing outright.

## Checks
- The title respects Walmart's character limit and style rule for the specific category.
- A valid GTIN/UPC is present; the listing does not go live without one.

## Output
{listing_draft, image_briefs[], attributes{}}

## Example
Category: kitchen. Title kept within Walmart's limit, promotional language removed per its style guide. GTIN
validated against GS1. Attribute "capacity_in_quarts" filled with the exact number, not "large."
