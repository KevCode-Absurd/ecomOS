---
name: support-reply-draft
owner: LIFE
version: 1
invoke_when: writing support reply templates and tagging/routing rules, including
  for a marketplace seller-support queue
inputs: ticket data by contact type, brand voice, current policy data
outputs: reply template library and tagging/routing rules
---
# Support reply and ticket-tagging design

## Purpose
Groups real ticket volume into contact types, writes a policy-accurate template
per type, and decides which types are safe to auto-send versus draft-only,
keeping human voice for recovery and VIP moments.

## Steps
1. Read a sample of recent tickets and group into contact types (WISMO, return,
   sizing, damaged/defective, payment, cancel/change, product question,
   complaint), keeping any "other" bucket under 15 percent of volume.
2. Draft a template per type in the brand's voice, citing current policy for every
   factual claim.
3. Classify each type as agent-can-close, agent-can-draft-only, or human-only.
   Recovery and VIP-flagged tickets are never agent-can-close.
4. Write the tagging rule so each incoming ticket maps to exactly one primary tag
   and routes to the right queue and priority.

## Checks
Every claim traces to current policy. Recovery/VIP tickets stay human. No
oversized "other" bucket hiding an uncovered contact type.

## Output
A reply template library plus tagging/routing rules.

## Example
"WISMO template cites the current 5-7 day delivery estimate; agent-can-close if the
order's tracking shows movement, human-only if tracking has been stalled 3+ days."
