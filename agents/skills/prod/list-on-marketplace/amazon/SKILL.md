---
name: prod/list-on-marketplace/amazon
owner: PROD
version: 1
invoke_when: the target marketplace is Amazon
select_by: {marketplace: amazon}
inputs: product copy, approved claims, keyword list, category node, Amazon's image and attribute spec
outputs: title, 5 bullets, image slot briefs, filled attributes, backend search terms
---
# List on Amazon

## Purpose
Amazon ranks primarily on the title and backend keywords, and converts primarily on the bullets and images. This
skill writes to that structure specifically, not a generic product-page template.

## Steps
1. Place the single highest-priority keyword in the title, positioned where Amazon's search weighs it most, and
   repeat it in the first bullet.
2. Write 5 benefit-led bullets, each carrying exactly one true, tiered claim: never a bullet with two unrelated
   claims stacked together.
3. Brief every image slot Amazon allows (main image on white background, lifestyle, infographic, size/comparison,
   in-use) to Amazon's exact spec for that slot.
4. Fill every backend attribute field completely and set backend search terms with keywords not already used in
   the visible copy, to avoid wasting indexing space.

## Checks
- The top keyword appears in both the title and the first bullet.
- Every bullet's claim is in the approved or site-backed tier, checked before handoff.

## Output
{listing_draft, image_briefs[], attributes{}, backend_keywords[]}

## Example
Title places "leak-proof steel water bottle 1L" with the top keyword first. Bullet 1 repeats it with the leak-proof
claim, cited to the site's own drop-test page. 5 image slots briefed including a size-comparison infographic.
Backend terms add non-duplicate synonyms like "insulated flask."
