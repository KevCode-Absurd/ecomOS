---
name: production-ops/bulk-upload-sheet
owner: crea-paid-creative-copy
version: 1
invoke_when: an approved batch needs turning into the exact file format a
  bulk-upload tool or Ads Manager bulk editor expects
inputs: confirmed approved batch, target platform's current bulk-upload spec
outputs: bulk-upload sheet, spot-check result
---
Purpose: produce a bulk-upload file that actually submits cleanly the first
time, since a platform's own bulk-editor spec changes without notice and a
stale column format fails an entire batch on submission.

Steps
1. Pull the target platform's current bulk-upload documentation and confirm
   the exact columns, required fields and format it expects right now, not
   from memory of a past batch.
2. Build the sheet with exactly one row per ad, filling every required
   column: campaign, ad set, creative filename, headline, primary text, CTA,
   destination link.
3. Confirm no required field is left blank; a blank required field fails
   silently on many bulk-upload tools rather than erroring clearly.
4. Spot-check a sample of rows against the original creative brief for a
   copy or filename mismatch, since a filename typo routes the wrong
   creative to the wrong ad.

Checks: spec checked within 30 days; zero blank required fields; sample
shows zero brief mismatches, or every mismatch is fixed first.

Output: the finished sheet and the spot-check result, ready for the
draft-upload step or a manual submission.

Example: a batch of 12 approved ads becomes a 12-row CSV, each row's
creative filename checked against its brief before the sheet ships.
