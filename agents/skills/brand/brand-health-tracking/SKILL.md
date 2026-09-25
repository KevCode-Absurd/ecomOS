---
name: brand-health-tracking
owner: BRAND
version: 1
invoke_when: the monthly brand health line is due
inputs: Google Search Console, review_rating/count, repeat_rate_90d/365d
outputs: branded search trend, review trend, brand health report
---
# Brand health tracking

## Purpose
Brand health is the slow-moving line underneath any single campaign's performance. This skill tracks it consistently every month so a real move is caught early, separate from short-term ad noise.

## Steps
1. Pull branded search query volume and trend from Search Console, covering a rolling 12 months where the connector allows.
2. Pull review_rating and review_count trend from the metric contract using `shared/metric-read`.
3. Check for any collectable public mention or sentiment data; if no real source exists, mark this field unavailable rather than estimating a sentiment score.
4. Pull repeat_rate_90d and repeat_rate_365d trend as a brand-strength proxy, kept separate from campaign-level ROAS reporting.
5. Assemble all series into one dated brand health line using `shared/report-section`, each series carrying its own freshness date.
6. Flag any series that moved more than a stated threshold since last month for founder attention.

## Checks
- Missing data always shows as unavailable, never as zero.
- Every series in the report carries its own date, not one blended "as of" date.
- No sentiment score is ever fabricated without a real source behind it.

## Output
`{branded_search_trend, review_trend_line, brand_health_report}`

## Example
Branded search volume flat at ~1,200/month for 3 months, then a 40% jump following a PR placement (BRAND-W21); flagged as a material move worth noting alongside the placement date.
