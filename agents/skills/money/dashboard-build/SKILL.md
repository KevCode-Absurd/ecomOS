---
name: money/dashboard-build
owner: MONEY
version: 1
invoke_when: the daily scoreboard, weekly memo, or standing dashboard set needs building or cleanup
inputs: P&L ladder, cash forecast, CM report, existing dashboard export, founder's recent questions
outputs: daily scoreboard, weekly memo inputs, or a cleaned and updated dashboard set
---
# Build and maintain the reporting dashboard set

## Purpose
Keep the numbers everyone reads trustworthy and current, and stop a dashboard from accumulating cards nobody trusts anymore.

## Steps
1. Compute the daily CM scoreboard, with the window ending on the last full day.
2. Compute the weekly profit memo inputs: CM, new versus returning revenue split from cohort data, variance against last week, and inventory risk.
3. Audit the standing dashboards (Shopify home cards, GA4 saved reports, budget scenario views) and name any card that no longer reads correctly.
4. Remove or flag unreliable cards, and add a card only when it answers a question someone actually asked recently.

## Checks
- Revenue, profit and cash never blend into one figure.
- Every card on the dashboard traces to a real question asked.

## Output
The daily scoreboard, the weekly memo inputs, or the cleaned dashboard set.

## Example
A GA4 card showing 'sessions by device' gets removed after nobody has referenced it in 3 months, replaced by a card the founder asked for twice: CM3 by channel this week versus last.
