---
name: prod/marketplace-health-monitor
owner: PROD
version: 1
invoke_when: the weekly marketplace-health check is due
inputs: Account Health dashboard data, review history, Buy Box status per listing, reseller pricing across
  marketplaces
outputs: sent review requests, an account health status, a Buy Box report, and any MAP violation flags
---
# Monitor marketplace health: reviews, account health, Buy Box

## Purpose
A policy notice ignored for a week can become a suspension; an unauthorized reseller undercutting on price can
erode a brand's own margin and trust. This skill runs the standing weekly health check that keeps both from
becoming a surprise.

## Steps
1. Request product reviews only through the platform's own permitted request mechanism: never an incentivised or
   off-platform review ask, which risks policy action against the account.
2. Contest any feedback that is misplaced (attached to the wrong product) or violates the platform's own feedback
   policy, through the platform's formal dispute process.
3. Check the Account Health dashboard every single week without exception, so a new policy notice is caught the
   week it appears, not discovered a month later as a suspension.
4. Check who holds the Buy Box across every marketplace listing, and check unauthorised reseller pricing against
   the brand's own MAP (minimum advertised price) policy.
5. Flag any MAP or price-integrity problem to the founder for a decision, rather than changing the brand's own
   price unilaterally in response.

## Checks
- Every review request uses a platform-permitted method.
- No price is changed by this agent in response to a MAP issue; it is always flagged to the founder.

## Output
{review_requests[], account_health_status, buy_box_report, map_violation_flags[]}

## Example
Account Health: clear, no new notices this week. Buy Box: held on 8 of 9 active listings; the 9th lost to an
unauthorized reseller pricing 12% below the brand's MAP: flagged for the founder rather than matching the price.
