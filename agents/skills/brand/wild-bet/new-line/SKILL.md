---
name: wild-bet/new-line
owner: BRAND
version: 1
invoke_when: the bet's type is a new product line or category extension
inputs: market sizing memo, avatar overlap read, production feasibility
outputs: feasibility packet, type-specific execution brief
---
# Wild bet: new product line

## Purpose
A new line is the most common wild bet type. The specific risk is building a full range before knowing anyone repeat-buys it; this skill keeps the pilot small and measurable.

## Steps
1. Run the market-sizing skill against the brand's own AOV, margin and repeat-buyer math for this specific candidate line, not the category in general.
2. Check the candidate against the current primary avatar's overlap: does the same customer buy this, or is this really a new-avatar bet in disguise (which changes the read entirely)?
3. Check with Product and Supply the smallest batch that can be produced and would still be a real test, not a token quantity that proves nothing.
4. Write the execution brief around a single pilot batch, sold to the smallest viable cohort by hand, with a named stop rule if the pilot does not sell through in the set window.

## Checks
- Sizing is computed in code from this brand's real numbers, not assumed from a category average.
- The pilot batch size is small enough to be a real test, not a full launch in disguise.

## Output
`{feasibility_packet: {sizing, avatar_overlap, batch_feasibility}, execution_brief}`

## Example
Candidate: a travel-size line for Gehna's existing jewellery avatar. Sizing shows 340 repeat buyers needed at the target price to hit contribution-margin breakeven; pilot batch set at 150 units sold direct via the existing list before any wider stocking.
