---
name: computed-in-code-offers
owner: site-specialist
version: 1
invoke_when: a PDP image order or an exit-intent/cart-abandonment discount needs to be decided from real data, not a guess
inputs: click-map or session-replay data per PDP, landed cost per SKU, shipping cost, founder's margin floor
outputs: proposed image order with reasoning, confidence flag per SKU, per-cart discount ceiling, exit-intent offer config
---
# Compute image order and discount ceilings in code

## Purpose
Replace two decisions humans normally guess at, a PDP's image order and a flat abandonment discount, with numbers computed in code from the brand's own real data.

## Steps
1. Pull per-image zoom, dwell and skip events from the site's own click-map or session-replay data, never a generic benchmark.
2. Rank the existing image set by which images hold attention longest before a scroll-away or an add-to-cart.
3. Propose a re-sequenced gallery order with the reasoning shown per swap, flagging when session volume is too thin to trust it.
4. For a discount ceiling: read landed cost, shipping cost and any already-applied promo for the exact cart at the moment of exit intent.
5. Compute the maximum discount that cart can take and still clear the founder's margin floor, entirely in code, never estimated by the model.
6. Fall back to no discount, not a guessed one, when a required cost input is missing for that SKU.
7. Send both types of proposal to the founder gate before anything ships live.

## Checks
- Every number is produced by code from real cost or attention data, never a model guess.
- A missing cost input always results in no discount, never a fallback guess.

## Output
A proposed image order with per-swap reasoning, or a per-cart discount ceiling and exit-intent offer config.

## Example
"Cart landed cost ₹620, shipping ₹80, margin floor 25%: maximum discount that still clears the floor is ₹140 (18%). Offer capped there, shown to the founder before going live."
