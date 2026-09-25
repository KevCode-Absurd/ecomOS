---
name: prod/amazon-fee-model
owner: PROD
version: 1
invoke_when: a monthly review or a pre-launch decision needs the full Amazon fee stack modeled against margin
inputs: the current FBA/FBM fee stack, storage cost schedule, a PPC budget assumption, the DTC price for parity,
  the SKU's landed cost
outputs: a fee-stack model and the net margin per SKU after every fee, with a floor-breach flag where relevant
---
# Model Amazon channel economics

## Purpose
Amazon's referral fee, FBA fee and storage cost stack up in ways that are easy to underestimate from memory. This
skill models the full stack in code against a SKU's real landed cost, so a launch or continuation decision is made
on a real net margin, not a gross-margin illusion.

## Steps
1. Pull the current, dated Amazon fee stack for the category: referral fee percentage, FBA pick-pack-ship fee by
   size tier, and storage cost by month.
2. Model the full fee stack against the SKU's landed cost, computed in code, never estimated.
3. Add a stated PPC budget assumption (clearly labeled as an assumption) and the storage cost for the SKU's actual
   size tier.
4. Check the resulting Amazon price against the brand's DTC price-parity rule, using the current live DTC price,
   not a stale one.
5. Compute net margin after every fee line, in code, and flag any SKU whose net margin falls below the brand's own
   stated floor.

## Checks
- Every fee line is sourced from Amazon's currently published rate card, dated.
- Net margin is computed in code, never estimated in prose.
- Price parity is checked against the live DTC price at the time of the check.

## Output
{fee_stack, net_margin_per_sku[], parity_check, margin_floor_flags[]}

## Example
SKU-1042: referral fee 15%, FBA fee ₹85 (size tier standard), storage ₹12/unit/month. Landed cost ₹210, Amazon
price ₹599. Net margin after all fees and a ₹40 PPC assumption: 19%, above the brand's 15% floor. Parity check:
Amazon price matches DTC within the allowed band.
