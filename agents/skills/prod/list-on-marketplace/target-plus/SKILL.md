---
name: prod/list-on-marketplace/target-plus
owner: PROD
version: 1
invoke_when: the target marketplace is Target Plus
select_by: {marketplace: target-plus}
inputs: product copy, approved claims, keyword list, category node, Target's brand style guide and image spec
outputs: title, description, image slot briefs, filled category attributes
---
# List on Target Plus

## Purpose
Target Plus is an invite-only, curated marketplace: Target reviews sellers and listings for brand fit before
and after approval, so copy and images need to match Target's own brand voice and quality bar, not just fill in
required fields.

## Steps
1. Write the title and description in Target's brand-voice style (warm, direct, benefit-led), following its
   published style guide rather than a generic marketplace tone.
2. Confirm the listing meets Target Plus's curated-partner quality bar (complete attributes, no placeholder
   copy, lifestyle imagery) before it is submitted through Partners Online.
3. Brief the on-white and lifestyle image slots to Target's own spec.
4. Fill every category attribute Target requires and confirm the correct category placement in Target's
   taxonomy.

## Checks
- Copy matches Target's brand-voice style guide, not a generic marketplace tone.
- The listing meets the curated-partner quality bar before it is submitted.

## Output
{listing_draft, image_briefs[], attributes{}}

## Example
Category: home decor. Title and description written to Target's warm, direct brand voice. Lifestyle image slot
briefed showing the product styled in a room setting, matching Target's own catalogue look.
