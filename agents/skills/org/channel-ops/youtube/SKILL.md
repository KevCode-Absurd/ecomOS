---
name: channel-ops/youtube
owner: ORG
version: 1
invoke_when: on every video upload, plus a standing Shorts cadence and monthly reporting
inputs: uploaded video, script/chapters from make-content/youtube-long, Shorts cadence target, keyword map
outputs: completed upload checklist, thumbnail and playlist status, Shorts cadence status, monthly metrics
---
# YouTube channel operations and video SEO

## Purpose
Own YouTube as a distinct surface with its own mechanics (thumbnails, chapters, playlists, Shorts cadence), applying the already-written script's title and description rather than rewriting them at upload time.

## Steps
1. Apply the title and description already written by make-content/youtube-long.
2. Add tags, chapters and an end screen pointing to the next video or the site.
3. Set a custom thumbnail and check it reads at mobile thumbnail size.
4. Add the video to its matching playlist.
5. Confirm the standing Shorts cadence is on track for the period; flag it if behind instead of letting a week slip silently.
6. Monthly, pull watch time, subscriber change and top videos into the report.

## Checks
- Title/description match the approved script, not an ad hoc rewrite.
- Thumbnail legible at small size.
- Shorts cadence tracked against target explicitly.

## Output
{upload_checklist_status, playlists_added[], thumbnail_status, shorts_cadence_status, monthly_metrics}

## Example
Video uploaded with chapters at 0:00, 0:45, 3:10 exactly matching the script's chapter list; Shorts cadence flagged one short behind target for the week.
