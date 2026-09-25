---
name: discount-policy-check
owner: LIFE
version: 1
invoke_when: any discount, offer term, or campaign/flow discount placement needs
  clearing against the brand's discount policy
inputs: the discount policy document, founder red lines, the proposed discount
outputs: pass/fail with the exact rule cited
---
# Discount policy and price-integrity check

## Purpose
The single gate every discount, bundle, GWP or campaign-discount decision passes
through, so discounting never quietly trains buyers to wait and never crosses a
founder's stated line.

## Steps
1. Check the proposed discount's frequency against the standing cap for this
   segment and period.
2. Check conditionality: does it require a real condition (minimum order, first-
   time, loyalty tier) rather than a blanket cut.
3. Check framing: is any reference price a real prior selling price, is any
   urgency claim real.
4. Check against every founder red line on record.
5. If a rule is unclear or a red line is missing for this case, fail the check
   and ask the founder rather than guessing.

## Checks
Fails closed on ambiguity. Every failure names the exact rule broken.

## Output
{pass_or_fail, rule_cited, fix_if_failed}

## Example
"FAIL: monthly frequency cap for this segment already used (2 of 2 in policy).
Rule: 'no segment sees more than 2 discount sends per month' (policy v3)."
