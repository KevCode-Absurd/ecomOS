---
name: category-ladder-and-xy-map
owner: BRAND
version: 1
invoke_when: a new positioning cycle starts or the competitive set materially changes
inputs: competitor packet, avatar record
outputs: category ladder, competitive set, XY positioning map, open-corner note
---
# Category ladder and XY positioning map

## Purpose
No positioning claim should be written before the field it competes in is actually mapped. This skill covers both the ladder (every rung a shopper could pick) and the map (where every real alternative sits on the two axes that matter).

## Steps
1. List every rung of the category ladder: the category itself, sub-categories, every real product alternative, and doing nothing as a real option a shopper could choose.
2. List the real competitive set: every brand or option a shopper would actually compare against, including at least one indirect or adjacent-category alternative, not only obvious direct rivals.
3. Choose two axes for the map based on what the avatar record shows this customer actually weighs in a decision (never pick axes just to leave an empty, flattering corner for this brand).
4. Plot the brand and every alternative on the two axes, citing the specific fact from the competitor packet that placed each one.
5. Identify empty corners, then check each against real demand evidence before calling it an opportunity rather than a corner nobody wants.

## Checks
- Every plotted point cites a specific fact.
- Axes are drawn from the avatar record's real decision criteria.
- "Doing nothing" appears on the ladder.

## Output
`{category_ladder: [...], competitive_set: [...], xy_positioning_map: {axes, points}, open_corner_note}`

## Example
Axes chosen: "price" and "craft-story strength" (drawn from avatar record showing craft story outweighs brand-name recognition for this buyer). Open corner at high-price/high-craft-story is checked against review data showing real demand for handcrafted detail at this price band.
