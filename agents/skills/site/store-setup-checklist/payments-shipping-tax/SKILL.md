---
name: payments-shipping-tax
owner: site-specialist
version: 1
invoke_when: configuring a payment gateway, a shipping zone/rate, or a tax jurisdiction
inputs: brand brain markets/margin/AOV/tax jurisdictions, connector read of current config
outputs: configuration + test log {setting, value, test performed, result}
---
# Payments, shipping and tax setup

## Purpose
Configure the 3 setup areas where a wrong number costs real money on day one, and prove every one of them with a real test, not a settings screenshot.

## Steps
1. For payments: verify identity documents exactly, add a second gateway (Shop Pay, PayPal, Apple Pay, a BNPL option such as Affirm, Klarna or Afterpay) and regional methods, set capture and fraud rules.
2. Test every gateway in sandbox, then place and refund one real order before removing the storefront password.
3. For shipping: build zones so every country has an explicit rate, set the free-shipping threshold from real margin and AOV.
4. Test every rate bracket at its edge with a real cart.
5. For tax: confirm real obligations with a professional first, then enable the calculation service per jurisdiction (state nexus and marketplace facilitator rules for the US).
6. Decide inclusive/exclusive display and tax basis per jurisdiction's real rule, and test one product per tax class in 2+ regions.

## Checks
- A real refunded order exists in the gateway dashboard.
- Every shipping bracket boundary was tested with a real cart.
- No tax jurisdiction configured without a professional's sign-off on file.

## Output
One configuration + test log per area, each line naming the setting, the value, the test performed and the result.

## Example
"Free shipping threshold: set at $59, from AOV $46 and 42% margin. Tested at $58.99 (rate shown) and $59.00 (free), both correct."
