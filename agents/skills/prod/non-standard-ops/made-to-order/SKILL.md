---
name: prod/non-standard-ops/made-to-order
owner: PROD
version: 1
invoke_when: the classified non-standard-ops type is a personalised or made-to-order sale
select_by: {type: made_to_order}
inputs: the order spec captured at checkout, customer proof approval, production tracking
outputs: captured spec, proof approval record, production status, and the shown non-returnable terms
---
# Made-to-order and personalised order workflow

## Purpose
Engraving, custom sizing, and other made-to-order items cannot follow the standard returnable-product flow: the
customer must approve the exact spec before production starts, and the non-returnable nature of the item must be
clear before they pay, not discovered afterward.

## Steps
1. Capture the exact personalisation or made-to-order spec at checkout, in a form both the customer and the
   production team can read unambiguously.
2. Generate a proof from the captured spec and get the customer's explicit approval before any production starts.
3. Track production against the approved proof, checking the finished item matches what was approved.
4. State the non-returnable terms clearly to the customer before payment is taken, not buried in fine print
   discovered after the sale.

## Checks
- The non-returnable term is shown and acknowledged before payment, never only after.
- Production never begins before the customer's proof approval is on record.

## Output
{spec, proof_approval, production_status, non_returnable_terms_shown}

## Example
Custom engraving order: spec captured (name, font, placement). Proof sent and approved by customer via email
before production started. Non-returnable terms shown and checked at checkout. Finished item verified against
the approved proof before shipping.
