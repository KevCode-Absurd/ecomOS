---
name: make-content/youtube-long
owner: ORG
version: 1
invoke_when: the task calls for a long-form YouTube video (over 3 minutes)
inputs: brand voice file, claims tiers, topic or SKU, watch-time goal, buyer-question map
outputs: title, description, chaptered script, tags, end-screen plan
---
# YouTube long-form script and structure

## Purpose
Long-form succeeds or fails on retention curve, not hook alone; this skill forces a payoff-first open and a chapter structure that survives the edit, distinct from a short-video hook script.

## Steps
1. Pick the single search or watch intent the video serves, sourced from org/buyer-question-mapping (a how-to, a comparison, a founder story).
2. Write the first 15 seconds stating exactly what the viewer gets and why the runtime is worth it.
3. Outline 3-6 chapters with a timestamp label each.
4. Write the script per chapter, one claim per line, tier-checked.
5. Write the title (keyword-forward, under 60 characters) and description, keyword in the first two lines, links after.
6. Suggest tags and an end-screen plan (subscribe, next video, or a site link).

## Checks
- The payoff is stated in the first 15 seconds.
- Chapters cover the whole runtime without a gap.
- Title and first description line both carry the target keyword.

## Output
{title, description, chapters[], script_by_chapter[], tags[], end_screen_plan, claims_used[]}

## Example
Title: "Stroller hinge test: 6 months, 3 US cities" - chapter 2 "0:45 The pothole test" with its own script block and one tiered claim.
