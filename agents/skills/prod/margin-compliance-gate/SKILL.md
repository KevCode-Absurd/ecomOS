---
name: prod/margin-compliance-gate
owner: PROD
version: 1
invoke_when: any candidate before sourcing spend, or a listing decision before it targets a new channel or market
inputs: unit cost, freight, duty, packaging cost, financing cost, target price, channel fee stack if applicable,
  the brand's own margin floor, claims and compliance category
outputs: pass/fail gate result with the full number breakdown and any compliance flags
---
# Margin, compliance and channel gate

## Purpose
No candidate reaches sourcing or listing spend without a real, computed margin and a clean compliance read. This
gate replaces founder taste and course-learned rules of thumb with the brand's own numbers.

## Steps
1. Pull every cost input from its real source: unit cost from the quote, freight and duty from the landed cost
   model, financing cost from the payment-terms structure. Pull the brand's own stated margin floor, never an
   industry rule of thumb.
2. Compute gross margin and contribution margin in code from these inputs.
3. Run the compliance screen for the category: shelf-life, regulatory certification, labelling requirements. A
   missing certification is a fail, not a caveat.
4. If the candidate targets more than the home market, score each expansion market separately on its own cost and
   price data: never assume the home market's gate result carries over.
5. Apply the remaining go-live gates together: are the claims provable, is there a real owned difference, does the
   candidate clear the brand's own thresholds, is there enough contribution margin left for ad-cost headroom.

## Checks
- Every input has a named source; a missing input blocks the gate outright rather than defaulting to zero or an
  assumption.
- The margin floor is the brand's own, cited to the decision or record that set it.
- No arithmetic is done in prose; everything routes through the landed cost calculator.

## Output
{gate, margin{gross, contribution}, compliance_flags[], per_market[], blocking_inputs[]}

## Example
Gate: fail. Contribution margin 11%, below the brand's 18% floor. Compliance: FDA facility registration not yet filed for this
SKU category: blocking (india: FSSAI licence not yet filed; markets: IN). Recommendation: hold until packaging cost drops or price rises; do not proceed to RFQ.
