---
name: prod/quick-commerce-ops
owner: PROD
version: 1
invoke_when: the weekly ad-credit/promo review is due, or the daily dark-store fill-rate check is due
inputs: ad credit balance per platform, organic search performance, the US retail promotional calendar (Q4
  holidays, BFCM, Prime Day; india: the festive promotional calendar), dark-store stock levels
outputs: an ad spend plan, a transaction-value-based ROAS, negotiated promo terms, and a fill-rate flag
---
# Manage rapid-delivery ad credits and dark-store fill rate

## Purpose
Rapid-delivery/quick-commerce platforms typically report ROAS on list/MRP price, which overstates real return by
30 to 50 percent; judging ad spend on that number leads to bad decisions. And a dark-store stockout triggers an
algorithmic ranking penalty that takes real time to recover from, so it needs daily, not weekly, attention.

## Steps
1. Spend each platform's ad tools deliberately rather than leaving credits unused, and pull back spend for a SKU
once its organic search ranking improves and stops needing paid support.
2. Recompute ROAS from actual transaction value, never the platform's own list/MRP-based default, before judging
whether spend is working.
3. Negotiate peak promotional windows (BFCM, Prime Day, Q4 holidays; India: the festive calendar; markets: IN)
ahead of the calendar date, since terms secured early are typically better than what is available once the rush
begins.
4. Watch stock levels across the dark-store network daily, the way a merchandiser walks the shelf, and flag a
stockout before it triggers the platform's own algorithmic ranking penalty, which is slow to recover from once
triggered.

## Checks
- Every ROAS figure used for a decision is recomputed from transaction value, never quoted from the platform's
  list/MRP-based dashboard number.
- A fill-rate flag is raised before the ranking-penalty window closes, not after the penalty has already applied.

## Output
{ad_spend_plan, roas_recomputed, promo_terms, dark_store_report, stockout_flags[]}

## Example
Platform-reported ROAS: 4.2x (list-price-based). Recomputed from transaction value: 2.9x: spend plan adjusted down
for the weakest SKU. Dark-store report: 2 of 40 stores below reorder threshold, flagged same day, ahead of the
platform's ranking-penalty window.
