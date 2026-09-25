---
name: prod/non-standard-ops
owner: PROD
version: 1
invoke_when: an order or channel event falls outside the standard sourcing/marketplace/fulfilment playbook
select_by: {type: export|offline_retail|recall|made_to_order}
inputs: the triggering event's details, brand brain policies and certifications
outputs: a type-specific handling packet and a logged outcome
---
# Handle a non-standard operations request

## Purpose
Four event types: a first export order, a pop-up or stockist deal, a safety recall, and a made-to-order sale: 
are each rare enough that no single standard workflow covers them, but common enough across a brand's life that
each deserves its own real procedure rather than being improvised from scratch every time. This parent skill
classifies the request and routes to the matching child.

## Steps
1. Read the triggering event and classify it as exactly one type: export, offline retail, recall, or
   made-to-order. A request that seems to match two types is split into two separate runs.
2. Route to the matching child skill (`prod/non-standard-ops/export`, `/offline-retail`, `/recall`, or
   `/made-to-order`) and run its specific procedure.
3. Run the compliance check appropriate to that type (export duty rules, retail licensing, regulator notification,
   or custom-order terms).
4. Document the full handling, including any customer communication, and log the outcome to the registry.

## Checks
- Exactly one type is classified per request.
- A recall never proceeds past classification without reaching the founder gate first.

## Output
{type, packet, compliance_result, documentation}

## Example
Event: a customer signs up for a pop-up in a new city. Classified: offline_retail. Routed to the offline-retail
child, which set up POS, consignment terms and a daily reconciliation schedule for the event's duration.
