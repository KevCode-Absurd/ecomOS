---
name: prod/rfq-quote-compare
owner: PROD
version: 1
invoke_when: a validated spec needs supplier outreach for pricing, or quotes have come back and need comparing
inputs: versioned tech pack, verified supplier shortlist, volume tiers to quote, freight and duty assumptions
outputs: RFQ document, quote comparison sheet, a supplier and tier recommendation
---
# Draft RFQ and compare quotes

## Purpose
An RFQ sent with different terms to different suppliers produces quotes that cannot be honestly compared. This
skill enforces one structured request and one apples-to-apples comparison.

## Steps
1. Translate the versioned tech pack into a structured RFQ. State tolerance bands plainly: a supplier who cannot
   hold a tolerance should say so at quote time, not after the first production run.
2. Send the identical RFQ to every supplier on the shortlist, with the same requested volume tiers and the same
   response deadline.
3. Collect quotes across every requested tier. A supplier who only quotes one tier gets asked again before being
   compared.
4. Flag any quote missing a required certification or payment term; exclude it from the comparison until the gap
   is resolved.
5. Build the landed cost per unit for every quote at every tier (working with the landed cost calculator), and
   compare both unit cost and the cash impact of committing to a larger tier. Recommend one supplier and tier with
   the numbers shown, not just a lowest-price pick.

## Checks
- Every RFQ measurement matches the tech pack's own tolerance band.
- Every supplier quoted against the same terms and deadline.
- A flagged, incomplete quote never enters the final recommendation.

## Output
{rfq_document, quotes[{supplier, tier, price, terms}], flags[], recommendation}

## Example
RFQ sent to 4 verified suppliers for tiers 3,000 / 8,000 / 15,000 units. One quote flagged for missing a BIS
certificate. Recommendation: Supplier B at the 8,000 tier: lowest landed cost per unit among complete quotes, and
the cash impact fits the brand's stated cash cover.
