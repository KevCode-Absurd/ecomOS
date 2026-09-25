---
name: seo-reporting-and-diagnosis
owner: ORG
version: 1
invoke_when: monthly, fixed cadence
inputs: Search Console export, GA4 export, metric contract (organic_sessions, organic_revenue), prior report
outputs: revenue-led monthly report, diagnosis naming the specific mechanism behind any drop
---
# SEO reporting and diagnosis

## Purpose
Run the fixed-cadence Search Console and GA4 read leading with organic revenue, and diagnose a drop by its actual mechanism instead of a vague "the algorithm changed".

## Steps
1. Pull sessions, clicks, impressions, CTR, position and organic revenue from the contract, computed in code.
2. Lead the report with organic revenue.
3. For any drop, check in order: CTR change, device mismatch, bounce/engagement change, ranking-position change.
4. Format the report as what we did, what it did, what is next, compared to the prior month.
5. Show any missing metric as unavailable, never a guess.

## Checks
- Revenue leads, not traffic.
- Diagnosis names a specific mechanism with evidence.
- Missing data marked unavailable.

## Output
{report{}, diagnosis[]}

## Example
Organic revenue fell 8% while sessions held steady: diagnosed as a CTR drop on the top 3 pages after a title change, not "seasonal", with the before/after CTR numbers shown.
