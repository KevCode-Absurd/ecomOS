---
name: prod/supplier-relationship-monitor
owner: PROD
version: 1
invoke_when: an active supplier needs its monthly scorecard, or a commodity-priced input needs its scheduled cost
  check
inputs: supplier delivery and defect history, commodity price data, the existing scorecard history
outputs: an updated supplier scorecard, a commodity price-move flag, a risk-weighted cost-down recommendation
---
# Monitor supplier performance and commodity cost

## Purpose
A supplier vetted once at onboarding can still drift. This skill runs the standing, ongoing side of the
relationship: a real scorecard on delivery and quality, and a watch on the commodity inputs that quietly move a
SKU's cost even when the supplier's own price stays flat.

## Steps
1. Score every active supplier on a fixed set of measures: on-time delivery rate, defect rate, responsiveness to
   queries, and price stability over time. Use the supplier's actual order history, never an impression from the
   last conversation.
2. Track the priced-in commodity inputs behind each SKU (cotton, resin, steel, whatever the product depends on) on
   a set monthly cadence, comparing against public commodity price indices.
3. When a cost-down looks possible, weigh it against the relationship-risk cost: a supplier pushed too hard on
   price may cut corners elsewhere or deprioritize the brand's orders during a capacity crunch.
4. Flag the result for the founder where the recommendation is "hold off" rather than "push," since that is the
   less obvious call.

## Checks
- The scorecard is built from real order data, not opinion.
- A commodity flag names the specific input and the specific price move, with its date.
- Any recommendation states which risk it is weighing against which saving.

## Output
{scorecard{on_time, defect_rate, responsiveness, price_stability}, commodity_flags[], risk_recommendation}

## Example
Scorecard: on-time 94%, defect rate 1.2%, responsiveness 18-hour average, price stable 6 months. Commodity flag:
input resin up 9% this month per index. Recommendation: hold on renegotiating this supplier's price given their
strong on-time record; absorb the resin move for one cycle and recheck next month.
