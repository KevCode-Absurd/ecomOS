---
name: money/gst-tax-compliance
owner: MONEY
version: 1
invoke_when: sales-tax nexus, product tax codes, filing prep or credit memos need tracking ahead of a filing (GST nexus, HSN codes, e-way bills or credit notes for India-selling brands)
inputs: SKU list, Avalara or TaxJar filing status, marketplace facilitator-tax lines, return log, India only: GSTR-2B, dispatch log
outputs: tax-code map, nexus status, filing input pack, facilitator-credit reconciliation, credit-memo reconciliation, India only: e-way bill log
---
# Track US sales tax nexus and filing compliance (GST/HSN for India)

## Purpose
Track the mechanics that feed a state sales-tax filing (a GST filing for India-selling brands) so the brand's own accountant or filing service files correctly and on time; this skill tracks, it does not file.

## Steps
1. Build the SKU-to-product-tax-code map in Avalara or TaxJar and validate every category match (SKU-to-HSN/SAC map for India, where a wrong or short code is a common cause of e-invoice portal rejections).
2. Track sales-tax nexus and registration thresholds per state the brand sells into.
3. Prepare the return-ready sales and exemption data each state's filing needs (GSTR-1 and 3B inputs matched against GSTR-2B, for India).
4. Reconcile marketplace-facilitator sales tax and 1099-K totals against the credit or exclusion actually available (TCS collected under Section 52 and TDS deducted, for India).
5. India only: raise e-way bills for B2B dispatch and stock transfer above the threshold.
6. Check that every completed return or refund has a matching sales-tax credit memo issued and filed on time (a GST credit note, for India).

## Checks
- No SKU ships without a validated tax code.
- Facilitator sales tax (or TCS and GST on fees, for India) are always separate lines.
- A refund without a matching credit memo is flagged before the filing period closes.

## Output
The requested scope's result: tax-code map, nexus status, filing input pack, facilitator-credit reconciliation, credit-memo reconciliation, or (India only) e-way bill log.

## Example
A new SKU crosses economic nexus in a state before its first sale there is registered; the nexus tracker flags the state before the next filing deadline, avoiding an unregistered-collection gap.

## Market note
An India-selling brand runs the HSN/SAC, e-way bill and GSTR path instead, which reads null for a US-only brand.
