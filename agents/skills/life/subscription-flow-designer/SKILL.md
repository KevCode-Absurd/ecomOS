---
name: subscription-flow-designer
owner: LIFE
version: 1
invoke_when: designing the subscription value proposition, perk gating, cadence
  flexibility, or the cancel-flow save offer
inputs: subscription platform data (churn, pause events), COGS, order data,
  cancellation reasons
outputs: subscription offer spec and cancel-flow design
---
# Subscription offer and cancel-flow design

## Purpose
Makes the reason to subscribe stronger than a flat discount, and designs a cancel
flow that is as easy to complete as sign-up but tries a reason-matched
alternative and a costed save offer before the subscriber leaves.

## Steps
1. Compare the subscription's total value (price, perks, flexibility) against the
   plain discount it replaces, in real numbers.
2. Set cadence flexibility and perk gating tied to actual use, not an arbitrary
   spend line.
3. Build the cancel flow as four stages: benefit reminder, exit-reason survey, a
   reason-matched alternative (pause, swap, frequency change), then a conditional,
   costed save offer only if earlier stages fail.
4. Cost the save offer against the subscriber's own order count and value.
5. Cap pause/skip/delay abuse without breaking a genuine flexibility need.
6. Add non-monetary mechanics (streaks, milestone gifts) as an addition, tested
   against a discount-only save, not assumed superior.
7. Set per-stage save-rate tracking so a weak stage can be rewritten specifically.

## Checks
Cancel is as easy to complete as sign-up. Save offer sized in code to the
subscriber's own value. Non-monetary mechanic tested, not assumed.

## Output
A subscription offer spec and a four-stage cancel-flow design with per-stage
save-rate targets.

## Example
"Stage 3 (reason: 'too much product') offers a frequency change to every 8 weeks,
not a discount; only subscribers who still exit reach stage 4's 15% save offer."
