---
name: prod/list-on-marketplace/tiktok-shop
owner: PROD
version: 1
invoke_when: the target marketplace is TikTok Shop
select_by: {marketplace: tiktok-shop}
inputs: product copy, approved claims, keyword list, category node, TikTok Shop's video/image spec, creator affiliate terms
outputs: a video-first listing, video cover brief, filled attributes, and a set affiliate commission
---
# List on TikTok Shop

## Purpose
TikTok Shop sells primarily through in-feed video and LIVE shopping, not a browsed catalogue page: the listing
exists to be tagged into video and LIVE content and to support the creator affiliate program, so it needs a video
cover and a commission decision a standard catalogue listing does not.

## Steps
1. Write a short, benefit-led title and description built for a video-first shopping surface, not a dense
   marketplace-style bullet list.
2. Brief the product image and short-form video cover to TikTok Shop's spec, since the cover image is what shows
   in-feed before a viewer taps through.
3. Fill every required attribute and confirm the category placement supports in-feed and LIVE product tagging.
4. Set the creator affiliate commission rate and any GMV Max (TikTok's automated ad) settings the brand approves,
   since affiliate reach is a primary driver of sales here, not organic browse.

## Checks
- The listing is tagged for in-feed/LIVE product linking, not left as a standalone catalogue-only page.
- Every claim appearing in a linked video script or caption is approved or site-backed, same as any other channel.

## Output
{listing_draft, video_cover_brief, attributes{}, affiliate_commission}

## Example
Product: a skincare serum. Title short and benefit-led ("Overnight glow serum"). Video cover briefed to show the
product in use in the first second. Affiliate commission set at 15% to attract creator participation.
