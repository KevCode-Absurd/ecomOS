---
name: pricing-audit
owner: BRAND
version: 1
invoke_when: the quarterly pricing position and premium-signal audit is due
inputs: competitor packet category price range, discount_rate from the metric contract
outputs: in-range/out-of-range verdict, premium-signal audit note
---
# Pricing audit

## Purpose
Price drifts out of position slowly, and a premium story quietly gets undercut by discount cadence long before anyone notices in the P&L. This skill checks both every quarter.

## Steps
1. Compare the brand's live price to the category price range established in the latest competitor packet; state which specific competitors set the top and bottom of that range.
2. Audit premium signals if a premium position is claimed: does packaging, page copy and current discount cadence still support it.
3. Flag explicitly where the discount_rate from the metric contract is high enough to undercut a stated premium claim; this is a direct contradiction, not a minor note.

## Checks
- The in/out-of-range verdict names which competitors bound the range, not a vague "seems fine."
- A high discount_rate next to a premium claim is flagged plainly, not smoothed into a softer note.

## Output
`{in_range_verdict, premium_signal_audit_note}`

## Example
Live price $42 sits inside the $36-$58 category range set by 4 named competitors; discount_rate at 22% over the last quarter flagged against the brand's "quiet luxury" positioning claim as an active contradiction.
