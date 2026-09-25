---
name: objection-map-builder
owner: BRAND
version: 1
invoke_when: objections need pairing with their real removers, for a new avatar or a rising objection pattern
inputs: research packet with tagged objections, known product/policy changes
outputs: objection-remover pairs, support macro drafts, confidence-angle flags
---
# Objection map builder

## Purpose
An objection without a proven remover is just a complaint list. This skill pairs every named objection with the specific thing that actually removed it for a real customer, so copy and support both have something real to say back.

## Steps
1. List every named objection from the research packet, with its frequency count across sources.
2. For each objection, search the same research packet (and any product-change or policy-change log) for the specific thing that removed it for a real customer: a review that mentions the fix worked, a support reply that resolved a ticket, a policy change (like a size-exchange guarantee) introduced after the pattern was noticed.
3. Pair each objection with its remover; a remover is not valid without 2 or more quoted sources showing it actually worked.
4. For objections that repeat monthly, draft an update to the standing support macro that answers it directly.
5. Flag any fit, sizing, or delivery-confidence pattern specifically; these often deserve a dedicated confidence angle in copy (a size guide, a fit guarantee callout) rather than just a macro.

## Checks
- Every objection-remover pair has 2 or more quoted sources.
- A remover is something that already happened (a real fix, a real reply), never an invented solution the brand has not actually implemented.

## Output
`{objection_remover_pairs: [{objection, remover, sources}], macro_drafts: [...], confidence_angle_flags: [...]}`

## Example
Objection: "unsure if the chain length suits my height" (11 mentions). Remover: a length-guide image added to the PDP, after which 4 subsequent reviews mention using it successfully. Paired with 4 quoted sources.
