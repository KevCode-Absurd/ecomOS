---
name: money/reconcile/marketplace
owner: MONEY
version: 1
invoke_when: a marketplace settles a payout cycle
inputs: marketplace settlement report, TCS certificate, order and return data
outputs: per-payout reconciliation with a rate-card check
---
# Reconcile marketplace settlement

## Purpose
Marketplace settlements bury commission, fees, TCS and refunds inside one payout figure. This skill pulls them apart and checks the marketplace charged what it agreed to.

## Steps
1. Pull the settlement report and the marketplace's TCS certificate for the period.
2. Unbundle commission, fixed fee, shipping fee, TCS under Section 52, GST on fees and refunds.
3. Match TCS deducted in the settlement to the certificate the marketplace issues.
4. Match every refund line in the settlement to an actual return in the order data.
5. Check the commission rate charged against the brand's agreed rate card by category.
6. Flag any mismatch with the exact order or SKU it came from.

## Checks
- TCS is never assumed correct; it is matched to the certificate.
- A refund with no matching return is flagged, not silently accepted.
- The commission rate check is per category, since rates vary by category.

## Output
One row per payout with gross, commission, fixed fee, shipping fee, TCS, GST on fees, refunds, net and a rate-card check result.

## Example
A Flipkart payout shows 8.5 percent commission on a category the rate card sets at 7.2 percent; the 1.3 point gap is flagged against the specific SKU category before the settlement is booked.
