---
name: channel-ops/audio-and-newsletter
owner: ORG
version: 1
invoke_when: on the podcast's publishing cadence, or the newsletter's send cadence
inputs: recorded episode or drafted issue, guest/topic pipeline, distribution checklist, list health metrics
outputs: podcast pipeline/recording/distribution status, newsletter list-health and send confirmation
---
# Podcast and newsletter channel operations

## Purpose
Run the practical production and distribution mechanics for two owned channels smaller brands often under-operate: a podcast's guest pipeline and multi-platform publish, and a newsletter's list health before every send.

## Steps
1. Confirm the next 2 podcast episodes have a booked guest or topic; flag a pipeline gap rather than let a slot go empty.
2. Check recording logistics before the session: mic check, a backup recording running.
3. Write keyworded show notes and cut 2-3 short clips, or hand the recording to org/video-repurposing-pipeline.
4. Publish to every listed platform and confirm each shows the correct episode.
5. Before every newsletter send, check bounce rate, unsubscribe rate and spam complaints; hold the send if any is outside the normal range.
6. Confirm the drafted issue is queued at its recommended time with a working unsubscribe link and correct sender identity.

## Checks
- Guest pipeline covers 2 episodes ahead.
- List health checked before every send.
- Every platform confirmed showing the right episode.

## Output
{podcast_status{}, newsletter_status{}}

## Example
Episode 14 has no guest booked with 9 days to air: flagged as a pipeline gap; newsletter send held because spam complaints ticked up past the normal range this week.
