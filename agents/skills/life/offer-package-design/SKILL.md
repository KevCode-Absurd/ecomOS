---
name: offer-package-design
owner: LIFE
version: 1
invoke_when: designing an offer's value proposition, bundle/ladder pricing, a
  gift-with-purchase, upsell/cross-sell placement, or a guarantee, as one package
inputs: landed cost/COGS, order-value distribution, the buyer's biggest objection,
  refund/return cost history, discount policy
outputs: offer design {package, objection_answered, margin_waterfall_ref,
  contribution_per_order, discount_policy_check, test_plan}
---
# Offer package design from margin and AOV

## Purpose
Builds a full offer package, price, bundle, gift, guarantee and upsell placement,
around the buyer's single biggest objection and the brand's real margin and order-
value distribution, not the average AOV or a copied competitor structure.

## Steps
1. Pull landed cost per SKU and the real order-value distribution (not just the
   average), plus the buyer's stated biggest objection from the brand record.
2. Write the value proposition to answer that specific objection, scored against
   the value equation (dream outcome, likelihood, time, effort).
3. Build the SKU margin waterfall and contribution per order in code.
4. Map the product's use journey into bundle/quantity-ladder tiers, sizing each to
   clear the contribution floor, with a justified reason per tier and a pre-
   selected middle option.
5. Design any gift-with-purchase to help use the core product, sized to lift the
   target tier, never dishonestly framed.
6. Place upsell/cross-sell offers by friction level (cart, checkout, post-
   purchase), anchored high with a cheaper down-sell.
7. Cost the guarantee from real refund data and write it in if-not-X-in-Y-we-will-Z
   form, activated at delivery.
8. Run the whole package through life/discount-policy-check and set the test plan
   (metric, read window) before it launches.

## Checks
Every tier clears the contribution floor. Guarantee cost is real, not assumed. No
revenue-only or ROAS-only justification accepted for go/no-go.

## Output
{package: {price, terms, bundle, gift, guarantee}, objection_answered,
margin_waterfall_ref, contribution_per_order, discount_policy_check, test_plan}

## Example
"3-pack ladder at ₹450/599/750 (per-unit price steps down each tier), middle
pre-selected; GWP: travel pouch on the 3-pack only; guarantee: 'not a perfect fit
in 30 days, free exchange'; contribution/order still clears ₹180 floor on every tier."
