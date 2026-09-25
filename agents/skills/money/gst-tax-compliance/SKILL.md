---
name: money/gst-tax-compliance
owner: MONEY
version: 1
invoke_when: GST nexus, HSN codes, e-way bills or credit notes need tracking ahead of a filing
inputs: SKU list, GSTR-2B, marketplace TCS lines, dispatch log, return log
outputs: HSN map, nexus status, filing input pack, e-way bill log, credit note reconciliation
---
# Track GST, HSN and tax compliance

## Purpose
Track the mechanics that feed a GST filing so the brand's own accountant files correctly and on time; this skill tracks, it does not file.

## Steps
1. Build the SKU-to-HSN/SAC map and validate every code length and category match, since a wrong or short code is a common cause of e-invoice portal rejections.
2. Track GST or sales-tax nexus and registration thresholds per market the brand sells into.
3. Prepare the sales and credit data GSTR-1 and 3B need, matching input credit claimed against GSTR-2B.
4. Reconcile TCS collected under Section 52 and TDS deducted by marketplaces against the credit actually available.
5. Raise e-way bills for B2B dispatch and stock transfer above the threshold.
6. Check that every completed return or refund has a matching GST credit note issued and filed on time.

## Checks
- No SKU ships without a validated HSN/SAC code.
- TCS and GST on fees are always separate lines.
- A refund without a matching credit note is flagged before the filing period closes.

## Output
The requested scope's result: HSN map, nexus status, GSTR-1/3B input pack, e-way bill log, or credit note reconciliation.

## Example
A new SKU is caught before its first B2B dispatch: its assigned HSN code is only 4 digits where the brand's turnover requires 6, avoiding an e-invoice portal rejection.
