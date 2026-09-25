---
name: prod/payment-terms-structure
owner: PROD
version: 1
invoke_when: a sourcing deal is closing and its payment route, split and cash impact need structuring
inputs: the confirmed price and terms, supplier relationship history, the brand's cash position
outputs: chosen payment route and split, with float days, cash-locked figure and financing cost computed in code
---
# Structure payment terms and cash impact

## Purpose
The payment route and split on a sourcing deal is a real cash decision, not paperwork. This skill picks the route
that matches the actual relationship risk and hands Finance the full cash picture at every deal close, never a
verbal estimate.

## Steps
1. Choose the payment route: wire transfer, letter of credit, platform trade assurance, or escrow: based on the
   supplier relationship's real history and risk, not a fixed default used for every deal.
2. Structure the split: advance percentage, balance on shipment or delivery, and any retention held back pending
   the sample or inspection result. Confirm the MOQ this split assumes.
3. Compute, in code, the float days (time cash is committed before goods or revenue arrive), the total cash locked
   up at any point in the cycle, and any financing cost if the route involves one (LC fees, trade-assurance
   charges).
4. Package the full numbers into a packet Finance can act on immediately, without needing to ask a follow-up
   question.

## Checks
- The route chosen matches the relationship's actual risk level, stated explicitly.
- Every float, cash-locked and financing figure is computed, never estimated in prose.

## Output
{route, split{advance, balance, retention}, moq, float_days, cash_locked, financing_cost}

## Example
Route: trade assurance (2-year relationship, but first order above $6,000). Split: 30% advance / 70% on shipment.
MOQ 5,000. Float: 21 days average. Cash locked at peak: $5,750. Financing cost: $0 (no LC needed). Packet sent to
Finance same day as deal close.
