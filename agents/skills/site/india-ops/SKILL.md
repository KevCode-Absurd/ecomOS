---
name: india-ops
owner: site-specialist
version: 1
invoke_when: COD share and return-to-origin rate are identified as a real bottleneck for an India-facing brand
inputs: courier serviceability API, brand's historical RTO data, WhatsApp business API access
outputs: PDP serviceability widget, checkout OTP flow, COD fee config, RTO dashboard
---
# COD return-to-origin reduction

## Purpose
Build the site-side half of India's biggest COD margin leak: filter and verify orders before they ship, and measure RTO by the dimensions that actually explain it.

## Steps
1. Show real-time PIN code serviceability on the PDP, using the courier or aggregator API, before the shopper adds to cart.
2. Add address auto-fill and phone OTP verification at checkout for COD orders above a set value.
3. Add a visible COD handling fee as a checkout line item, sized from real impulse-order data to filter without losing genuine buyers.
4. Surface a prepaid discount or free-shipping incentive at the exact step where COD is selected.
5. Trigger an automated WhatsApp order-confirmation message after COD checkout, with an auto-cancel rule if unconfirmed.
6. Replace the generic courier tracking link with a branded tracking page carrying post-purchase upsell content.
7. Pass a buyer risk score (first order, high COD value, prior RTO history) to the fulfilment system for a manual check, without running the logistics NDR process itself.
8. Build an RTO analytics view broken down by courier, PIN code, product and payment method.

## Checks
- Every lever is measured against the brand's own real RTO data, never a generic industry number.
- The COD fee amount is backed by real impulse-order evidence, not a round guess.

## Output
A PDP serviceability widget, a checkout OTP flow, a COD fee config, a WhatsApp confirmation flow, and an RTO dashboard.

## Example
"RTO dashboard shows PIN codes in one region running 3x the average RTO on COD orders over ₹2,000; OTP verification enabled for that region above ₹1,500 instead of the store-wide ₹3,000 threshold."
