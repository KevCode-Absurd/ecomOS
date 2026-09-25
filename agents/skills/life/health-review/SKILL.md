---
name: health-review
owner: LIFE
version: 1
invoke_when: producing the monthly lifecycle health review
inputs: metric contract, registry entries with a read point this month
outputs: monthly lifecycle health report
---
# Monthly lifecycle health review

## Purpose
Reads the full metric chain, tells a volume problem apart from a content problem,
and turns diagnosis into named next actions rather than a status list.

## Steps
1. Pull list growth, opt-in rate, flow and campaign revenue share, deliverability
   and repeat-rate figures for the month from the metric contract.
2. For any weak flow, check whether low entry volume (a segmentation/traffic issue)
   explains it before diagnosing the flow's own content or timing.
3. Pull this month's registry reads; list pending reads as pending, not results.
4. Diagnose the top 2-3 problems with the specific evidence behind each.
5. Recommend the next workflow to run for each diagnosed problem.

## Checks
Volume problems never mis-diagnosed as content problems. No number replaced by an
adjective. Every recommendation names an executing workflow id.

## Output
A monthly report: metric chain, diagnoses with evidence, ranked next actions.

## Example
"Post-purchase flow revenue down 18%: entry volume down 20% (orders down, not the
flow) - fix is order volume, not flow content. No flow change recommended."
