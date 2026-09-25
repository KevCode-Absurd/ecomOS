---
name: prod/list-on-marketplace/myntra
owner: PROD
version: 1
invoke_when: the target marketplace is Myntra
select_by: {marketplace: myntra}
inputs: product copy, approved claims, keyword list, category node, Myntra's image and size-chart spec
outputs: title, size chart, model/flat-lay image briefs, fashion-specific attributes
---
# List on Myntra

## Purpose
Myntra is a fashion-specific marketplace: size charts, fit descriptions and fabric attributes carry more listing
weight here than on a general marketplace, and a missing size chart is a common cause of returns and poor ranking.

## Steps
1. Write the title in Myntra's fashion-specific format (brand, product type, key attribute), distinct from a
   generic marketplace title.
2. Confirm a size chart is present and correct for the category: this is close to mandatory for apparel and
   footwear and its absence directly drives size-related returns.
3. Brief the model-shot and flat-lay image slots to Myntra's own spec, including any required background and
   pose conventions.
4. Fill fashion-specific attributes: fabric, fit, occasion, sleeve type, and any others the category requires.

## Checks
- Every apparel listing has a size chart present before it is considered complete.
- Fashion attributes carry real, specific values, not generic placeholders.

## Output
{listing_draft, size_chart, image_briefs[], attributes{}}

## Example
Category: women's kurta. Size chart built from the brand's own measurement sheet, not copied from a competitor.
Attributes filled: fabric "cotton blend," fit "relaxed," occasion "daily wear." Model-shot slot briefed to
Myntra's plain-background convention.
