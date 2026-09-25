---
name: special-formats/mascot-sheet
owner: crea-paid-creative-copy
version: 1
invoke_when: a generated character or mascot needs a fixed reference so
  every future generation reuses the same identity
inputs: approved character concept, brand kit and voice
outputs: reference sheet, versioned character asset, drift check result
---
Purpose: keep a generated character's identity stable across every ad it
appears in, since AI generation drifts without a fixed anchor, and a mascot
that looks slightly different in every ad reads as unfinished, not
intentional.

Steps
1. Fix the character's core traits specifically enough that a wrong
   regeneration is obviously wrong: exact color, proportion, signature
   feature, not a vague description that allows drift.
2. Generate the reference sheet covering the expressions, angles and outfit
   views the pipeline will actually reuse, through the character-sheet
   preset.
3. File and version the sheet under the standing naming schema so every
   later generation can cite the exact version it was built from.
4. Before any new asset uses the character, check it against the current
   reference sheet for drift, catching it before the asset ships rather
   than after a viewer notices.
5. When the founder approves a real change, a new outfit or expression,
   save it as a new version; the old version stays on file rather than
   being overwritten, so past assets remain traceable to what they used.

Checks: traits specific enough to catch drift; old versions preserved, not
overwritten.

Output: the reference sheet, its version id, and the drift check result for
each new use.

Example: version 2 of a mascot adds a festive outfit for the Diwali
campaign; version 1's plain outfit stays on file for assets still using it.
