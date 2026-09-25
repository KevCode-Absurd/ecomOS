---
name: community-feedback-mining
owner: ORG
version: 1
invoke_when: monthly, or on a volume spike in one theme
inputs: comments/DMs/reviews export, community-space conversations, prior feedback report
outputs: themed report with quoted counts, trend vs prior period, routed to product/ops
---
# Community and support feedback mining for product and ops

## Purpose
Turn owned conversation into a report Product and Operations can act on, separate from social listening's outward-facing trend digest, and catch a spike in one theme against a real prior number.

## Steps
1. Pull comments, DMs, reviews and community-space conversations for the period.
2. Cluster into themes (a defect, a sizing issue, a delivery complaint, a feature request), each with a quote and a count.
3. Compare each theme's volume against the prior report to catch a real spike.
4. Split content-relevant feedback from operational feedback; route operational themes to Product and Operations, not just into a content idea pile.
5. Write the report with quoted evidence per theme and its routing.

## Checks
- Every theme has a quote and a count.
- A spike claim compares to the prior period's real number.
- Operational themes are actually routed, not left unaddressed.

## Output
{themes[]}

## Example
"Zipper stuck after 2 weeks" appears 14 times this month vs 3 last month, a 4.7x jump, routed to Product with 5 verbatim quotes attached.
