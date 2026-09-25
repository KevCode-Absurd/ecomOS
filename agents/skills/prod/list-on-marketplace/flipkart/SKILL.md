---
name: prod/list-on-marketplace/flipkart
owner: PROD
version: 1
invoke_when: the target marketplace is Flipkart
select_by: {marketplace: flipkart}
inputs: product copy, approved claims, keyword list, category node, Flipkart's image and attribute spec
outputs: title, key feature list, image slot briefs, filled category attributes
---
# List on Flipkart

## Purpose
Flipkart's title length limits and category-specific attribute sets differ from Amazon's, and its search weighting
favors different fields. A copy-pasted Amazon listing under-performs here.

## Steps
1. Place the top keyword in the title, respecting Flipkart's own character limit for the category, which is often
   shorter and stricter than Amazon's.
2. Write the key feature list in Flipkart's own field structure (Key Features, not bullets styled like Amazon's).
3. Brief every image slot Flipkart allows to its own spec, including any mandatory size-chart image for apparel.
4. Fill every category-specific attribute Flipkart requires; its attribute set is often more granular by category
   than Amazon's generic set.

## Checks
- The title respects Flipkart's character limit for the specific category.
- Category-specific attributes are filled with real values, not left at a generic default.

## Output
{listing_draft, image_briefs[], attributes{}}

## Example
Category: kitchen. Title kept within Flipkart's 200-character limit for the category. Key Features field lists 5
points distinct in wording from the Amazon version. Attribute "capacity_in_litres" filled with the exact number,
not "large."
