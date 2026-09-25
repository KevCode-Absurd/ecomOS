---
name: money/audit-tracking/server-events
owner: MONEY
version: 1
invoke_when: the tracking audit's surface is server-side tagging or the tag manager itself
inputs: tag management container structure, server-side tagging config, consent mode config
outputs: container-level checklist result and dead-tag list
---
# Audit server-side tag management

## Purpose
GA4 and Meta audits check their own tags. This skill checks the container that fires them, since a broken container structure breaks every tag inside it at once.

## Steps
1. Map the full container structure: triggers, variables, and every tag firing from it.
2. Check the server-side tagging setup specifically: which events route through a server container versus the browser, and whether that split still matches the brand's spend level.
3. Confirm consent mode gating is applied at the container level, not per tag inconsistently.
4. Find duplicate tags firing the same event twice, and dead tags pointing at a destination that no longer exists.
5. Confirm the container's last change matches the last known-good state after any recent site or app change.

## Checks
- The container is audited as a whole, not tag by tag with no view of the structure.
- Dead tags are named specifically, not left firing silently and wasting event quota.
- Consent gating is checked at the container level.

## Output
Container structure check, server-side routing check, consent gating check and a named dead-tag list.

## Example
A tag left over from a discontinued email platform still fires on every checkout page; it is named in the dead-tag list for removal.
