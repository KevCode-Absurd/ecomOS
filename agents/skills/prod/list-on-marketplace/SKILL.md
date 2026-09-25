---
name: prod/list-on-marketplace
owner: PROD
version: 1
invoke_when: a product needs a listing built or refreshed for any marketplace
select_by: {marketplace: amazon|walmart|target-plus|ebay|tiktok-shop|flipkart-myntra-nykaa|blinkit-zepto}
inputs: product copy, approved claims, keyword list, category node, image slots and specs, the target marketplace
outputs: a complete listing draft ready for a named human to paste into the seller console
---
# Build a marketplace listing

## Purpose
Every marketplace enforces its own title length, bullet rules, image slots and attribute set, and none of them are
the same. This is the parent procedure: it never posts a listing itself, only drafts one, and it always routes to
the platform-specific child before writing a single field. Amazon, Walmart, Target Plus, eBay and TikTok Shop are
the default US-first children; Flipkart/Myntra/Nykaa and Blinkit/Zepto are grouped India-market options (markets:
IN), not selected for a US-only brand.

## Steps
1. Confirm the target marketplace and select the matching child skill
   (`prod/list-on-marketplace/amazon`, `/walmart`, `/target-plus`, `/ebay`, `/tiktok-shop`, or, for an India brand,
   `/flipkart-myntra-nykaa` or `/blinkit-zepto`).
2. Run the child's specific field rules to place the top keyword and write benefit-led, claim-checked copy in the
   platform's own format.
3. Brief every image slot to that platform's own size, crop and content rule: an Amazon main image and a
   TikTok Shop video cover are not interchangeable.
4. Fill every attribute field the platform requires and confirm the correct category node in that platform's own
   taxonomy.
5. Package the finished draft for a named human to paste into the seller console. This skill never posts directly
   to a live listing on any platform.

## Checks
- The marketplace named is one of the seven supported children, matched to its own child procedure.
- No required field is left blank.
- Nothing produced by this skill is ever posted directly; it is always handed to a human.

## Output
{marketplace, listing_draft, image_briefs[], attributes{}, category_node}

## Example
Marketplace: target-plus. Routed to `prod/list-on-marketplace/target-plus`. Title and key callouts placed per
Target's own style guide; 5 image slots briefed to Target's spec; attributes filled; draft handed to the
marketplace manager to paste into Target Plus's Partners Online portal. India: the equivalent nykaa listing routes
to `prod/list-on-marketplace/flipkart-myntra-nykaa` instead (markets: IN).
