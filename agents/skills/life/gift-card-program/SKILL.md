---
name: gift-card-program
owner: LIFE
version: 1
invoke_when: designing or refreshing the store's own gift card program
inputs: current gift card app data if any, return/refund policy, per-market law
outputs: gift card program design, float-liability model, reminder flow copy
---
# Gift card program design

## Purpose
Designs the gift card as a real product line, denominations, expiry, bulk-gifting
terms, and its interaction with refund credit, while modelling the unredeemed-
balance liability so the founder sees the cash-flow effect before launch.

## Steps
1. Read current denominations and redemption rate if a gift-card app exists.
2. Choose sellable denominations and any bonus-value tier, sized against margin.
3. Set expiry policy checked against each market's legal minimum validity.
4. Design a separate bulk/corporate-gifting tier and process.
5. Set the rule for how a refund-issued store credit interacts with a purchased
   gift card, so a refund credit is never expired like a promotional one.
6. Model the float liability (unredeemed balance) in code from stated sell-through
   assumptions.
7. Write the purchase-confirmation, pre-expiry-reminder and redemption-receipt
   copy.

## Checks
Expiry never conflicts with legal minimums. Float liability computed in code.
Refund credit and purchased gift card follow different expiry rules.

## Output
A gift-card program design, a float-liability model, and the reminder flow copy.

## Example
"₹1,000/2,500/5,000 denominations, no bonus tier at launch. Float liability at
6-month sell-through assumption: ₹4.2L outstanding balance modeled."
