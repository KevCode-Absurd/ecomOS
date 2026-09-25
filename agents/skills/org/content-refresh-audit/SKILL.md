---
name: content-refresh-audit
owner: ORG
version: 1
invoke_when: monthly
inputs: Search Console export, page-level revenue history, product feed, duplicate/cannibalization check
outputs: refresh list ranked by revenue at risk, redirect list, prune list
---
# Content refresh, redirect and pruning audit

## Purpose
Keep existing pages healthy before writing anything new: refresh what is falling, ranked by the revenue it puts at risk rather than traffic alone, handle discontinued pages properly, and remove pages competing against each other for the same target.

## Steps
1. Pull page-level sessions and, where the order-to-session join exists, page-level revenue history.
2. Rank the refresh backlog by revenue at risk first, then traffic-only drops.
3. Check every discontinued or out-of-stock page against the feed; route to a redirect or an honest out-of-stock state, never a silent 404.
4. Find duplicate or cannibalizing pages and recommend a merge or canonical, ranked with shared/rank-candidates.
5. Name the specific problem behind each refresh candidate before recommending a rewrite.
6. Package the refresh, redirect and prune lists.

## Checks
- Ranked by revenue at risk where the data exists.
- No page silently 404s.
- Every candidate names its specific problem.

## Output
{refresh_list[], redirect_list[], prune_list[]}

## Example
Page "toddler-safety-gate" ranks first in the refresh list because it lost 40% of its page-level revenue in 90 days, with the problem named as "price section 6 months stale".
