---
name: pricing-integrity
owner: site-specialist
version: 1
invoke_when: a competitor price change is detected, or a scheduled weekly check of live anchor-price claims
inputs: competitor price signal feed (public listings only), current PDP comparison claims
outputs: stale-claim flags, proposed corrected comparison copy
---
# Keep anchor-price and comparison claims honest and current

## Purpose
Make sure a PDP's price-comparison claim never goes stale or false, by watching the same public competitor prices already used as signal elsewhere, without ever copying competitor text, images or branding.

## Steps
1. Read only publicly listed competitor prices already treated as signal elsewhere in the system, never scraped account data.
2. Match each PDP anchor-price or comparison claim to the specific competitor price it cites.
3. Flag a claim as stale the moment the cited price changes enough to make the comparison inaccurate.
4. Propose the corrected comparison number for a human to approve before any copy changes.
5. Never let a comparison claim ship without a current, dated source behind it.
6. Keep this entirely separate from the brand's own private cost and margin data.

## Checks
- Every live comparison claim has a current, dated public source.
- No comparison copy ever changes without a human approving the correction first.

## Output
Stale-claim flags and proposed corrected comparison copy, both handed to a human for approval.

## Example
"PDP claims 'save ₹500 vs [competitor]'s listed price of ₹2,499'. Competitor now lists at ₹2,199. Flagged stale; proposed correction: 'save ₹200', pending founder approval."
