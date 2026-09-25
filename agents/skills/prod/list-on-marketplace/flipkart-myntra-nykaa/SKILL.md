---
name: prod/list-on-marketplace/flipkart-myntra-nykaa
owner: PROD
version: 1
invoke_when: the target marketplace is Flipkart, Myntra or Nykaa (markets: IN; not selected for a US-only brand)
select_by: {marketplace: flipkart|myntra|nykaa}
inputs: product copy, approved claims, keyword list, category node, the platform's own image/attribute/size-chart/ingredient spec
outputs: a complete listing draft matching the chosen platform's own rules
---
# List on Flipkart, Myntra and Nykaa

## Purpose
India only (markets: IN): this skill covers the brand's other major India marketplaces beyond Amazon, in one
grouped child since they share the underlying discipline (a platform-specific title/attribute set, none of them
Amazon) while differing on their specialty. It does not run for a US-only brand, whose non-Amazon options are
Walmart, Target Plus, eBay and TikTok Shop instead.

## Steps
1. Confirm which of the three platforms this listing targets: Flipkart (general marketplace), Myntra
   (fashion-specific), or Nykaa (beauty/wellness-specific), since each has its own title length, attribute set
   and search weighting.
2. Place the top keyword in the title, respecting that platform's own character limit, which is often shorter and
   stricter than a general marketplace.
3. On Myntra, confirm a size chart is present and correct for the category before the listing is considered
   complete: its absence is a common cause of size-related returns. On Nykaa, run every beauty or wellness claim
   through the claim-check skill before it goes near the draft; an unsupported claim about skin or health effects
   is a compliance risk, not just a marketing overreach, and is removed rather than softened.
4. Brief every image slot the platform allows to its own spec, including a mandatory size-chart image for Myntra
   apparel or an ingredient-list/texture-shot image for Nykaa beauty listings.
5. Fill every category-specific attribute the platform requires: fabric/fit/occasion for Myntra, skin-type/
   concern/ingredient for Nykaa (matching the real product formulation, never a category-typical guess), or the
   platform's own generic attribute set for Flipkart.

## Checks
- Every Myntra apparel listing has a size chart present before it is considered complete.
- Every Nykaa beauty or wellness claim passed claim-check before the listing is considered complete.
- Category-specific attributes carry real, specific values, never a generic placeholder.

## Output
{marketplace, listing_draft, size_chart, image_briefs[], attributes{}}

## Example
Marketplace: nykaa. Product: a face serum. Claim "reduces the look of fine lines" kept (site-backed by a 4-week
user trial). Claim "clinically proven" removed (no clinical trial exists in the brand record). Ingredient
attribute filled with the exact INCI list.
