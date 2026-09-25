---
name: prod/list-on-marketplace/nykaa
owner: PROD
version: 1
invoke_when: the target marketplace is Nykaa
select_by: {marketplace: nykaa}
inputs: product copy, approved claims, keyword list, category node, Nykaa's ingredient and claim spec
outputs: title, claim-checked copy, ingredient/texture image briefs, skin-type/concern attributes
---
# List on Nykaa

## Purpose
Beauty and wellness listings carry regulatory exposure a general product listing does not: an unsupported claim
about skin or health effects is a compliance risk, not just a marketing overreach. This skill enforces the claim
check specifically for that category before anything else.

## Steps
1. Write the title with the key ingredient or benefit callout Nykaa's search and shoppers respond to.
2. Run every beauty or wellness claim through the claim-check skill before it goes anywhere near the draft; a
   cosmetic or wellness claim with no approved or site-backed source is removed, never softened and kept.
3. Brief the ingredient-list and texture-shot image slots Nykaa expects for beauty listings.
4. Fill skin-type, concern and ingredient attributes accurately, matching the product's actual formulation.

## Checks
- Every beauty or wellness claim passed the claim-check skill before the listing is considered complete.
- The ingredient attribute matches the real product formulation, never a category-typical guess.

## Output
{listing_draft, image_briefs[], attributes{}}

## Example
Product: a face serum. Claim "reduces the look of fine lines" kept (site-backed by a 4-week user trial on the
brand's own site). Claim "clinically proven" removed (no clinical trial exists in the brand record). Ingredient
attribute filled with the exact INCI list.
