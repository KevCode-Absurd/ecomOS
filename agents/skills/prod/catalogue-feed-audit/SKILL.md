---
name: prod/catalogue-feed-audit
owner: PROD
version: 1
invoke_when: the daily feed needs building, or the weekly cross-channel quality audit is due
inputs: live price and stock records, product records (titles, images, GTIN), each channel's own schema and
  image/video spec, the cross-channel price policy
outputs: a master product feed, a per-channel validation report, and a standing catalogue quality audit
---
# Build, validate and audit the catalogue feed

## Purpose
Media buyer and Organic both depend on one clean feed to plug into shopping ads and marketplace channels, and a
broken image or a duplicate SKU discovered by a channel's own rejection wastes a cycle that a standing audit would
have caught first.

## Steps
1. Keep one clean master product feed: titles, images, prices, availability, and GTIN, with no duplicate SKU and
   no missing GTIN.
2. Validate the feed against each destination channel's own current schema before handing it off: a schema that
   worked last month may have changed.
3. Hand the validated feed to Media buyer and Organic, and confirm it loaded without error on their side.
4. Run a standing audit across every channel's live listings for broken images, missing attributes, and duplicate
   SKUs that may have crept in independently of the feed.
5. Check for the brand's own price mismatch between its site and each marketplace, flagging any gap rather than
   silently reconciling it.
6. Check every new product image and video against each channel's own size, crop and content rule before it is
   pushed, since an Instacart thumbnail and an Amazon main image have entirely different requirements (india: a Blinkit
   thumbnail; markets: IN).

## Checks
- The feed has zero duplicate SKUs and zero missing GTINs before handoff.
- A price mismatch is always flagged, never quietly auto-corrected.
- Image and video specs are checked before push, not discovered via a channel's rejection.

## Output
{master_feed, validation_report, quality_audit_report, price_mismatch_report, asset_spec_flags[]}

## Example
Feed validated clean against Amazon's, Walmart's and Instacart's current schemas. Weekly audit found 3 SKUs with a
broken image link on one marketplace and a $2 price mismatch between site and Walmart: both flagged, neither
auto-corrected. India: the same audit flags a ₹20 price mismatch between site and Flipkart instead (markets: IN).
