---
name: money/reconcile/chargebacks
owner: MONEY
version: 1
invoke_when: a chargeback or dispute opens against an order on a card network, Shopify Payments, Stripe or PayPal
inputs: gateway/processor dispute feed, order and fulfillment records, customer-communication history, reason-code deadline table
outputs: evidence packet per dispute, win-rate report by reason code
---
# Reconcile and represent chargebacks and disputes

## Purpose
A chargeback or dispute is a reversal, not a return: it goes through the card network or PayPal, on their own deadline, and needs its own evidence packet. This skill treats it as a first-class reconciliation source, the same as a gateway or marketplace payout, and never lets a filing deadline slip.

## Steps
1. Pull every open dispute from each gateway or processor (Shopify Payments, Stripe, PayPal), with its reason code, amount and deadline.
2. Assemble the evidence packet the specific reason code calls for: proof of delivery, customer communication, IP/device match, policy acceptance.
3. File representment before the deadline.
4. Track whether the representment won or lost, and log the reason code either way.
5. Roll the result into the win-rate report by reason code and gateway.

## Checks
- No dispute is missing a filing deadline.
- The evidence packet is built for the specific reason code, not a one-size packet.
- Win rate is tracked by reason code and gateway, never blended into one number.

## Output
One row per dispute: gateway, reason code, amount, deadline, evidence packet, and outcome once resolved.

## Example
A Stripe dispute with reason code 'product not received' gets a packet built from the shipping carrier's delivery confirmation and the customer's own delivery-confirmation email, filed two days before the ten-day deadline.

## Market note
An India-selling brand runs the same skill for a UPI dispute, assembling the OTP log alongside delivery proof and support chat.
