---
name: campaign-brief
owner: LIFE
version: 1
invoke_when: planning the weekly campaign calendar, or drafting one campaign send
inputs: metric contract, product/launch calendar, segment list, discount policy
outputs: campaign brief {send_date_window, audience_segment, content_framework,
  discount_or_not, draft_copy_ref, success_metric}
---
# Campaign calendar and brief

## Purpose
Plans the non-flow send calendar in two layers, an always-on baseline and event-
based peaks, and turns each planned send into a complete, checked brief.

## Steps
1. Read last week's sends and results, and the upcoming product/event calendar.
2. Plan the week: mostly non-discount content, rotating format (story, UGC,
   education, offer), no repeat of the same segment-plus-format pair in one week.
3. Assign each send a segment from the current segment-spec output and a content
   framework.
4. Run life/discount-policy-check before attaching any discount.
5. Assemble the brief in the fixed shape.

## Checks
Content mostly non-discount. No segment-format repeat within the week. Segment used
is fresh (refreshed this week).

## Output
{send_date_window, audience_segment, content_framework, discount_or_not,
draft_copy_ref, success_metric}

## Example
{"send_date_window": "Tue 10am IST", "audience_segment": "engaged-90d",
"content_framework": "social-proof", "discount_or_not": "none",
"success_metric": "campaign_revenue_per_recipient"}
