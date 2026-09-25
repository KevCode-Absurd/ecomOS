---
name: organic-performance-read
owner: ORG
version: 1
invoke_when: monthly
inputs: platform analytics export, metric contract (organic_sessions, cvr_pdp_to_cart, hook_rate, hold_rate), tagged calendar
outputs: monthly report against the store's own baseline, stranger-blind flags, top hooks by conversion
---
# Organic content performance read

## Purpose
Judge organic content against what this store's own account normally does and whether it moved a buyer, not against industry benchmarks or raw view counts.

## Steps
1. Pull SKU- and hook-level numbers from the metric contract.
2. Compute this account's own trailing-90-day baseline in code; every post is judged against it.
3. Flag stranger-blind content: high reach with no lift in sessions or cart adds, meaning it entertained without selling.
4. Flag broad low-value hits landing outside the avatar's demographic where platform data allows the check.
5. Rank the top 3 hooks or formats by the store's own conversion signal, not raw engagement.
6. Write the report in the shared report-section shape: what we did, what it did, what is next.

## Checks
- Comparisons use the store's own baseline.
- Missing fields read as unavailable, never 0.
- No vanity total leads the report.

## Output
{report{}, stranger_blind_flags[], top_hooks[]}

## Example
A reel with 500k views but no lift in organic_sessions for its tagged SKU is flagged stranger-blind; a lower-view post that doubled cvr_pdp_to_cart on its SKU ranks in the top 3.
