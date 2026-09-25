---
name: video-repurposing-pipeline
owner: ORG
version: 1
invoke_when: on every new long-form recording (podcast episode, founder talk, livestream)
inputs: long-form file, transcript, target short-form platforms and aspect ratios
outputs: ranked, captioned, correctly-sized clips tagged by source episode
---
# Long-form to short-form video repurposing

## Purpose
Automatically produce a set of ranked short clips from any long recording, so one podcast episode or livestream also feeds the Reels/Shorts calendar without a separate shoot.

## Steps
1. Get or generate a full transcript.
2. Identify candidate moments: a standalone claim, a strong reaction, a quotable line, each with a timestamp.
3. Rank by whether the moment works without the rest of the episode's context.
4. Cut, caption and resize each selected clip for its target platform.
5. Write a short caption and on-screen hook, tier-checking any claim even if the source recording already said it.
6. Route finished clips into the content calendar as fillable slots, tagged by their source episode.

## Checks
- Every clip stands alone.
- Captions are burned in and accurate.
- Claims are tier-checked again at the clip level.

## Output
{clips[], source_episode_id}

## Example
From a 40-minute podcast episode, a 22-second clip at 14:05 where the founder explains the hinge redesign is cut, captioned, resized to 9:16, and queued for the calendar.
