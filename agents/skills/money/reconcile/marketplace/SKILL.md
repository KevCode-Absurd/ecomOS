---
name: money/reconcile/marketplace
owner: MONEY
version: 1
invoke_when: a marketplace settles a payout cycle
inputs: marketplace settlement report, 1099-K or facilitator tax statement (TCS certificate for India), order and return data
outputs: per-payout reconciliation with a rate-card check
---
# Reconcile marketplace settlement

## Purpose
Marketplace settlements bury commission, fees, facilitator sales tax and refunds inside one payout figure. This skill pulls them apart and checks the marketplace charged what it agreed to.

## Steps
1. Pull the settlement report and the marketplace's 1099-K or facilitator tax statement for the period (TCS certificate for India-selling brands).
2. Unbundle commission, fixed fee, shipping fee, marketplace-facilitator sales tax withheld, and refunds (TCS under Section 52 and GST on fees, for India).
3. Match facilitator sales tax withheld (or TCS deducted, for India) in the settlement to the marketplace's own statement or certificate.
4. Match every refund line in the settlement to an actual return in the order data.
5. Check the commission rate charged against the brand's agreed rate card by category.
6. Flag any mismatch with the exact order or SKU it came from.

## Checks
- Facilitator sales tax (or TCS for India) is never assumed correct; it is matched to the marketplace's own statement.
- A refund with no matching return is flagged, not silently accepted.
- The commission rate check is per category, since rates vary by category.

## Output
One row per payout with gross, commission, fixed fee, shipping fee, facilitator tax, refunds, net and a rate-card check result.

## Example
An Amazon payout shows 15 percent commission on a category the rate card sets at 12.5 percent; the 2.5 point gap is flagged against the specific SKU category before the settlement is booked.
