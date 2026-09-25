---
name: churn-risk-score
owner: LIFE
version: 1
invoke_when: the weekly churn/lapse risk read, or a subscription renewal fails
inputs: order interval history, subscription pause/failed-renewal events, support
  ticket and engagement data
outputs: risk-tiered customer list with routing to the correct save program
---
# Churn and lapse risk scoring

## Purpose
Builds a churn-risk score from real decay against the customer's own cadence, not a
flat day count, and routes each risk tier to the save program that actually fits
the cause: ordinary win-back, RTO-trust-rebuild, or subscription cancel-flow save.

## Steps
1. Compute each customer's expected next-order date from their own purchase
   interval; flag anyone past it by a set margin.
2. Pull subscription pause and failed-renewal events, and set the retry/re-auth
   schedule for failed UPI AutoPay or e-mandate renewals per current RBI rules.
3. Pull unresolved support tickets and engagement decay for the same customers.
4. Compute a low/medium/high risk tier per customer in code from the combined
   signals.
5. Route: engagement-decay risk to the ordinary win-back flow; RTO-caused lapse to
   the trust-rebuild variant; active-subscriber risk to the cancel-flow save offer.
6. Report involuntary churn (failed renewals) apart from voluntary cancellations.

## Checks
Order gap always measured against the customer's own cadence. All scoring in code.
RTO-caused lapse never routed to a discount-led win-back first.

## Output
A risk-tiered customer list with the routing decision and its evidence.

## Example
"Customer's avg gap: 35 days. Last order: 70 days ago (high risk). Last delivery
was an RTO -> route to trust-rebuild win-back, not the standard discount flow."
