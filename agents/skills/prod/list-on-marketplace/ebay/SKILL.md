---
name: prod/list-on-marketplace/ebay
owner: PROD
version: 1
invoke_when: the target marketplace is eBay
select_by: {marketplace: ebay}
inputs: product copy, approved claims, keyword list, category node, eBay's item specifics and return-policy terms
outputs: title, filled Item Specifics, image slot briefs, and a set return policy
---
# List on eBay

## Purpose
eBay's Best Match ranking weighs Item Specifics, seller performance (Top Rated Seller status), return policy and
handling time as heavily as the listing copy itself, so a listing missing these is invisible in search even with
strong copy.

## Steps
1. Place the top keyword in the title within eBay's character limit, front-loading the most searched term.
2. Fill every Item Specific field the category supports; Best Match rewards completeness here more than on a
   general marketplace.
3. Brief the image slots to eBay's spec: at least 12 images where the category allows, zoomable, no watermarks
   or border text.
4. Set the return policy and handling time explicitly; a shorter handling time and a buyer-friendly return
   policy both lift Best Match ranking and Top Rated Seller eligibility.

## Checks
- Every relevant Item Specific field is filled, none left blank.
- The return policy and handling time are deliberately set, not left at a platform default.

## Output
{listing_draft, image_briefs[], attributes{}, return_policy}

## Example
Category: sporting goods. All 18 available Item Specifics filled. 14 images briefed, zoomable. Return policy set
to 30-day buyer-paid return, handling time set to 1 business day, both chosen to support Top Rated Seller status.
