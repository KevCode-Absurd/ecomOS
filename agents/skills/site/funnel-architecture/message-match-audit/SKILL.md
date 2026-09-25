---
name: message-match-audit
owner: site-specialist
version: 1
invoke_when: an ad creative changes, or a new page needs to be checked against the ad feeding it
inputs: brand brain live ad copy (read-only, via mcp: meta ads), brand brain page copy
outputs: message-match audit report, mismatch fix list
---
# Message-match audit: ad to page to checkout

## Purpose
Confirm the exact promise a shopper clicked on still holds true all the way to checkout, since a broken promise anywhere in the funnel kills conversion.

## Steps
1. Read the live ad's exact promise, persona and offer through the read-only Meta connector.
2. Mirror that promise in the page's hero headline; the page should continue the ad's story, never start a new one.
3. Keep one persona consistent end to end, and match price, discount, guarantee and shipping identically from ad to page to cart to checkout.
4. Match the CTA label to where it actually sends traffic.
5. Match page length to how much the ad already sold (a fully-sold ad needs a short page).
6. Re-run this whole check the moment the feeding ad's creative changes.

## Checks
- Every mismatch found names its exact location (ad line vs page line).
- Re-run triggered same-day on any ad creative change, not on a delay.

## Output
A message-match audit report and a mismatch fix list.

## Example
"Ad promises '2-year warranty'; PDP guarantee block says '1 year'. Mismatch flagged, page fix routed same day."
