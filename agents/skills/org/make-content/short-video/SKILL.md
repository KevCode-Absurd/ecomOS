---
name: make-content/short-video
owner: ORG
version: 1
invoke_when: the task's format is a short vertical video (Reel, Short, TikTok-style)
inputs: brand voice file, claims tiers, one named SKU, one named buyer, Scout references (structure/mood only)
outputs: hook, body, caption, CTA, claims list, a filmable shot list
---
# Short-video script and shot list

## Purpose
Turn one SKU and one buyer into a script a camera-phone crew can film without asking a follow-up question, sized for 15-45 seconds.

## Steps
1. Name the one reaction, action or takeaway the video proves in its first 3 seconds.
2. Write the hook: 5-8 words, must work with sound off, appears on screen inside the first second.
3. Write the body cutting jargon and repeated synonyms; one claim per line, each checked against the claims tiers.
4. Write a caption addressed to one named buyer (never "you guys"), then the CTA and where it points.
5. Build a shot list: shot number, framing (close/mid/wide), location, which SKU or prop, on-screen text, seconds per shot, totalling the target run time.
6. Flag anything blocking a film day: founder availability, a location not yet scouted, a prop out of stock.

## Checks
- Hook works muted.
- Every factual line traces to a claims tier.
- Shot list seconds sum to the target length.
- Below tenth-grade reading level.

## Output
{hook, body, caption, cta, claims_used[], shot_list[], flags[]}

## Example
Hook: "This stroller survived my building's broken lift." Shot 1: mid shot, lobby, stroller-v2, on-screen text "Day 40", 3s.
