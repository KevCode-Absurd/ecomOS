---
name: production-ops/draft-upload-browser-agent
owner: crea-paid-creative-copy
version: 1
invoke_when: the founder has approved staging approved creatives as paused,
  unpublished drafts directly inside Ads Manager
inputs: bulk-upload sheet, founder approval for this specific account
outputs: paused draft ads inside Ads Manager, draft-ad id list
---
Purpose: get an approved batch into a real, reviewable draft state inside the
platform's own interface, using a browser agent, without ever letting a
draft go live, since CREA's account access stays read-only otherwise.

Steps
1. Confirm the founder has specifically approved this browser-agent step for
   this ad account; this is a founder_gate capability and does not run on a
   standing blanket approval.
2. Drive Ads Manager's own web interface, using the bulk-upload sheet as the
   source, to create exactly one paused, unpublished draft ad per approved
   creative row.
3. Confirm, per draft, that its status is paused and unpublished before
   moving to the next row; a draft that accidentally activates is treated as
   a stop-everything incident, not a minor error.
4. Hand the resulting draft-ad id list to MEDIA, who reviews each real draft
   inside the platform and decides whether to activate it.

Checks: founder approval on file for this account; every single draft
confirmed paused; none ever activated by this skill.

Output: the created draft ads and their platform ids, handed to MEDIA.

Example: 12 approved creatives become 12 paused draft ads inside Meta Ads
Manager, none live, all waiting for a human's go-live decision.
