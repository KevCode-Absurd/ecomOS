---
name: referral-payment-offer
owner: LIFE
version: 1
invoke_when: designing a give-X-get-X referral program, a non-competing partner
  perk, installment/BNPL terms, or nominal-price trial pricing
inputs: repeat-buyer base data, margin data, partner candidates
outputs: referral offer spec, partner candidate list, BNPL/trial pricing spec
---
# Referral, partner and payment-term offer design

## Purpose
Sizes a referral reward and partner perk from real margin and repeat-buyer value,
and designs installment/BNPL and trial pricing with the real provider fee shown,
never a copied structure from a competitor.

## Steps
1. Size the give-X-get-X reward from the repeat-buyer base's real average value.
2. Set the tracking mechanism (code or link) and the reward-payout trigger, which
   fires only on a confirmed, non-refunded order.
3. Identify partner brands serving the same customer without competing on
   category, for a no-cost cross-promotion perk.
4. Design installment/BNPL terms with the real per-installment price and the
   payment provider's real fee shown against margin.
5. Design a nominal-price trial with a disclosed conversion date and full price.
6. Clear both the referral reward and the trial/BNPL terms through
   life/discount-policy-check.

## Checks
Reward and any bonus sized to real margin. Payment-provider fees are real, not
estimated. Trial conversion terms disclosed to the buyer up front.

## Output
A referral offer spec, a partner candidate list, and a BNPL/trial pricing spec.

## Example
"Give ₹300, get ₹300, capped at 1 reward per order pair, paid only after the
referred order ships without a return - protects margin against return abuse."
