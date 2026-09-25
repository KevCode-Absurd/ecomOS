---
name: destination-qa
owner: ORG
version: 1
invoke_when: every time a post is scheduled, before it goes live
inputs: the scheduled post, its destination link or Story tag, live site status for that page
outputs: pass/hold verdict with the mismatch reason, and a funnel-stage tag
---
# Pre-publish destination and funnel-stage QA

## Purpose
Stop a post from publishing to a dead link, an out-of-stock page shown as in-stock, or a price that no longer matches, and tag every post by funnel stage so it can be tracked and reused later.

## Steps
1. Open the post's destination link or Story product tag directly; never assume it still works from when it was set up.
2. Confirm the page is live, matches the promised product or offer, and shows an honest stock or waitlist state.
3. Confirm the price or offer named in the post matches the live page exactly.
4. Tag the post's funnel stage: awareness, consideration, decision, or retention.
5. Hold any post that fails a check and name the exact mismatch; never publish on a guess that it is probably still fine.

## Checks
- Destination checked live at the moment, not cached.
- Price/offer match is exact.
- Every passing post carries a funnel-stage tag.

## Output
{post_id, destination_status, mismatch_reason, funnel_stage_tag}

## Example
A post promising "20% off, link in bio" is held because the linked collection page shows the discount ended 2 days ago.
