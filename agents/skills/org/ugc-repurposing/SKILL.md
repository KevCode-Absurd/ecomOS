---
name: ugc-repurposing
owner: ORG
version: 1
invoke_when: weekly, when new verified reviews, photos or unboxing moments are available
inputs: verified review/photo export, creator seeding output, usage-rights confirmation, claims tiers
outputs: postable drafts (quote cards, stitched reels, before/after sets) tagged by SKU
---
# UGC and review repurposing

## Purpose
Turn real customer proof into content without ever posting something the brand does not have the right to use, and without letting a customer's opinion slip through as an unchecked brand claim.

## Steps
1. Pull new verified reviews, photos and unboxing videos since the last run; require real text or footage, not a bare star rating.
2. Check usage rights against the buyer or creator agreement; anything unconfirmed goes to the founder before use, not into a draft.
3. Pick the strongest, most specific quotes and images per SKU.
4. Build the draft (quote card, stitched reel, before/after set) with correct source credit.
5. Run the claims-compliance gate on any restated customer claim; a customer's opinion is not automatically an approved brand claim.
6. Add the finished draft to the calendar and asset library, tagged by SKU and funnel stage.

## Checks
- Usage rights confirmed before use.
- Restated customer claims pass the claims gate.
- Every draft tagged by SKU and funnel stage.

## Output
{drafts[], flagged_rights_issues[]}

## Example
A 5-star review quoting "survived 3 monsoons" becomes a quote card credited "verified buyer, Pune, Aug 2026", checked because "survived 3 monsoons" is a durability claim needing a tier match.
