---
name: special-formats/payment-delivery-reassurance-messaging
owner: crea-paid-creative-copy
version: 1
invoke_when: an ad or checkout moment needs a line that removes payment
  friction or lowers failed-delivery risk; for a COD brand (markets: IN),
  the same skill nudges a cash-on-delivery order toward prepaid and lowers
  return-to-origin risk
inputs: current payment method mix, failed/reversed-order rates,
  reassurance or prepaid incentive if any, delivery-trust facts
outputs: payment reassurance copy, delivery-trust copy block
---
Purpose: write the lines that build trust in how an order gets paid for and
delivered, using only real incentives and real carrier facts, since this
messaging often touches checkout trust directly. For a COD brand this
includes the India-market option of moving a cash-on-delivery buyer toward
prepaid and lowering the risk of a return-to-origin (RTO); that option
reads null for a US brand.

Steps
1. Pull the account's current payment method mix and failed/reversed-order
   rates (chargeback rate, return-to-sender rate), so the messaging effort
   is sized to how much this actually matters for this brand right now, not
   applied uniformly regardless of the real numbers. For a COD brand, also
   pull the COD share and RTO rate.
2. Write the payment reassurance line as a specific, honest line: a BNPL
   option, a card or wallet trust fact, or, for a COD brand, a real discount
   amount or a real faster-dispatch promise, never a vague "pay online for a
   better experience."
3. Write the delivery-trust line using the real carrier name, the real
   delivery window, and a real tracking or call-before-delivery fact if
   that is actually offered.
4. Check both lines against current operations policy before they ship,
   since a delivery-time, BNPL or discount claim here is a common source of
   drift between what marketing promises and what ops can do.

Checks: discount, BNPL and speed claims match what ops actually offers;
every delivery fact matches current policy.

Output: the payment reassurance line and the delivery-trust copy block.

Example, US brand: "pay in 4 with Klarna, no interest" only ships once ops
confirms the terms are real. Example, India COD brand (markets: IN): "pay
online, save 50 rupees and get it a day faster" only ships once ops
confirms both the discount and the faster timeline are real.
