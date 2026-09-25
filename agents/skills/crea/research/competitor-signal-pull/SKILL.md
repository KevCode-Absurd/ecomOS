---
name: research/competitor-signal-pull
owner: crea-paid-creative-copy
version: 1
invoke_when: a step needs competitor references for layout or mood, never for
  copying text, logo, product or face
inputs: objection map or bottleneck, comp_media.json, competitors.json
outputs: 3 to 8 tagged, layout/mood-only references
---
Purpose: gather real competitor structure signal, cadence, layout and mood,
without ever crossing into using a competitor's actual text, logo, product or
face, and without treating any of it as a proven winner.

Steps
1. Pull competitor ads from the Meta gallery's Competitors tab that match the
   current bottleneck or persona, using the existing tagged competitor data
   (competitors.json, comp_media.json) rather than a fresh scrape.
2. Where the gallery's own set does not have enough range, call the Reference
   Scout for additional swipe material under the same layout/mood-only rule.
3. Write a one-line reason each reference was pulled: what structural or mood
   element it demonstrates, never "because it looks good."
4. Mark every single reference as signal only, explicitly, in the handoff, so
   a downstream skill cannot mistake it for cleared source material.
5. Cap the final set at 3 to 8 references; more than that stops being usable
   in a brief.

Checks: every reference has a fit reason; every reference is tagged signal
only; no reference implies a proven result.

Output: the tagged reference set, ready to attach to a concept or design
brief.

Example: 5 competitor statics are pulled for their shared "before/after split
screen" layout on a skincare bottleneck, none of their headlines or product
shots are carried forward.
