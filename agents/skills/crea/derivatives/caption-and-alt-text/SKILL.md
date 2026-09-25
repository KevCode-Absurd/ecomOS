---
name: derivatives/caption-and-alt-text
owner: crea-paid-creative-copy
version: 1
invoke_when: a video needs burned-in captions since most are watched muted,
  or a static needs descriptive alt text
inputs: finished or resized video/static asset
outputs: captioned video, alt text string per static
---
Purpose: make sure the message survives with the sound off, and that a
screen-reader user gets an honest description, not a repeated sales pitch, as
a fixed QA step before anything ships.

Steps
1. Transcribe the video's spoken line exactly, word for word; a paraphrased
   caption that drifts from the actual audio is a fail even if it reads
   fine.
2. Burn the captions in, timed correctly to when each line is actually
   spoken, not offset or bunched.
3. Write alt text for every static that describes what a sighted viewer
   actually sees, the product, its setting, any visible text on the image,
   rather than restating the ad's selling headline.
4. Do a final pass confirming captions and alt text match the exact finished
   asset, since a last-minute edit to the video or image can leave a caption
   or alt text describing an earlier version.

Checks: captions exact and correctly timed; alt text descriptive, not a
pitch restated.

Output: the captioned video file and the alt text string for each static.

Example: alt text for a shoe ad reads "white running shoe on a wet trail,
side profile, laces untied," not "the most comfortable shoe you'll ever
own."
