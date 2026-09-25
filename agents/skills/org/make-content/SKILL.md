---
name: make-content (dispatcher)
owner: ORG
version: 1
invoke_when: a calendar slot, approved idea or repurposing job needs a real draft written
inputs: calendar slot or idea, format, platform, brand voice file, claims tiers, one named SKU, one named buyer
outputs: the matched child skill's draft plus a claims-check verdict
---
# Make organic content (dispatcher)

## Purpose
Route a content task to the one child skill built for its format, instead of one generic writer trying to do video, carousel, long-form, Pinterest and email equally well. This is the parent node of the make-content family; it holds no drafting logic itself.

## Steps
1. Read the task's format and platform fields.
2. Match to exactly one child: org/make-content/short-video, /carousel, /youtube-long, /pinterest-pin, or /newsletter.
3. Pass the named SKU, named buyer, the objection or question the piece answers, brand voice file, claims tiers, and any Scout references straight through unchanged.
4. Take the child's draft and run shared/claim-check before returning it to the calling workflow.
5. If the task names a format with no child (a new platform), stop and hand a workflow proposal to a person instead of guessing a format.

## Checks
- Exactly one child skill is invoked per task.
- No draft returns without a claims-check verdict attached.
- A format with no matching child stops the run rather than improvising.

## Output
Whatever the matched child returns, wrapped with {claims_check_verdict}.

## Example
A calendar slot marked format: "reel", platform: "instagram" routes to org/make-content/short-video; a slot marked format: "pin" routes to org/make-content/pinterest-pin.
