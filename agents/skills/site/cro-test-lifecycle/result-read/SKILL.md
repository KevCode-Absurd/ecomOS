---
name: result-read
owner: site-specialist
version: 1
invoke_when: a CRO test has reached its pre-set read point
inputs: test results (registry), metric contract
outputs: result read report, ship/hold/kill recommendation
---
# Read and interpret CRO test results

## Purpose
Turn raw test numbers into an honest verdict, catching the common ways a test result lies: bad luck days, sample mismatch, novelty, and p-value tunnel vision.

## Steps
1. Count conversions on a real confirmation event (a purchase), never a click proxy.
2. Never call a test on the strength of one especially good or bad day.
3. Check sample ratio mismatch at launch and at every planned look.
4. Plot novelty and primacy effects daily before trusting the average.
5. Check the mobile-only and desktop-only splits separately before shipping a win.
6. Apply Twyman's law: audit any surprising win harder than an expected one before celebrating it.
7. Decide from the confidence interval and the real business value together, never p<0.05 alone.
8. Treat a fully powered inconclusive test as a real, useful result, not a failure to hide.

## Checks
- No verdict rests on a p-value alone.
- SRM, novelty and device splits are all checked before a result is trusted.

## Output
A result read report and a clear ship/hold/kill recommendation.

## Example
"Variant B: +11% PDP-to-cart, CI [3%, 19%], SRM clean, no novelty decay by week 2, consistent on mobile and desktop. Recommendation: ship."
