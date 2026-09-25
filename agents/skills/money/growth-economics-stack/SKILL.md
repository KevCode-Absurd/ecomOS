---
name: money/growth-economics-stack
owner: MONEY
version: 1
invoke_when: CAC, LTV, revenue forecast, subscription economics or the OPEX budget needs computing
inputs: clean order set, ad spend by channel, marketing calendar, subscription history, profit target
outputs: the requested module's report
---
# Report CAC, LTV, revenue forecast and the budget

## Purpose
One engine for the numbers that decide whether to spend the next marketing dollar, so every module uses the same screened order data and the same cohort definitions.

## Steps
1. Screen the order set for fraud and bot-driven orders before any cohort math runs.
2. Compute blended, media-only, paid and fully loaded CAC, each labeled.
3. Build first-order cohorts and compute CAC payback and LTGP:CAC against the metric contract's fixed bands.
4. Forecast new-customer and returning revenue from the spend-efficiency curve, cohort repeat rate and the dated marketing calendar as separate inputs.
5. For a subscription brand, build churn against the correct prior-period base and conservative lifetime estimates.
6. Build the annual OPEX budget sized to the brand's own profit target, separate from the rolling forecast.

## Checks
- LTV is gross profit, never revenue.
- No channel-level CAC substitutes for the blended finance number.
- A short sales history is regressed to the mean, never extrapolated in a straight line.

## Output
The requested module's report: CAC/LTV dashboard, revenue forecast with error bars, subscription unit economics, or the OPEX budget.

## Example
A channel with a great platform-reported ROAS shows a payback period of 11 months once fully loaded CAC and true cohort repeat rate are applied; the scale recommendation holds at current spend, not more.
