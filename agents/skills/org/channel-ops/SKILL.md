---
name: channel-ops (dispatcher)
owner: ORG
version: 1
invoke_when: a video is uploaded, a podcast episode is due, or a newsletter send is due
inputs: the channel-specific asset, the channel's operating checklist
outputs: whichever child skill's checklist and output
---
# Owned long-form channel operations (dispatcher)

## Purpose
Route a channel-operations task to the procedure built for that channel's own mechanics, since YouTube, podcast and newsletter each run on a different cadence and a different checklist.

## Steps
1. Read which channel the task names.
2. Dispatch to org/channel-ops/youtube for a video upload, or org/channel-ops/audio-and-newsletter for a podcast episode or newsletter send.
3. Confirm the child skill's standing cadence item (Shorts posting, guest booking, list-health check) was actually done this cycle, not assumed carried over from last time.

## Checks
- Exactly one child is invoked.
- The standing cadence item is confirmed, not assumed.

## Output
Whatever the matched child skill returns.

## Example
A new podcast episode recording routes to org/channel-ops/audio-and-newsletter; a new long-form video routes to org/channel-ops/youtube.
