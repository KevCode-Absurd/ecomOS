---
name: local-seo-and-reviews
owner: ORG
version: 1
invoke_when: weekly, for any brand with a physical location
inputs: Google Business Profile access, store location list, NAP data, review inflow
outputs: GBP accuracy status, NAP mismatch list, unincentivized review requests, response drafts
---
# Local SEO and reputation program

## Purpose
Run Google Business Profile, local citations and NAP consistency, plus a review-collection program that never pays for a review, since incentivized reviews break platform policy and trust.

## Steps
1. Confirm the brand actually has a physical location before running anything here.
2. Check Google Business Profile accuracy: hours, category, photos, posts, Q&A.
3. Check NAP consistency across directories and flag exact mismatches.
4. Draft unincentivized review requests sent after a verified purchase; never offer payment or a discount for a review.
5. Draft responses to new reviews, especially negative ones, with a real next step.
6. Return the weekly status.

## Checks
- No incentivized review request.
- NAP mismatches named exactly, with the wrong value and the directory.
- Confirmed a physical location exists before running.

## Output
{gbp_status, nap_mismatches[], review_requests_drafted[], review_response_drafts[]}

## Example
Directory "Justdial" shows the old store address; flagged with the exact wrong text and the correct address to submit.
