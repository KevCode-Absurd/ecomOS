---
name: build-flow
owner: LIFE
version: 1
invoke_when: an approved idea or a scheduled maintenance job calls for a new or rebuilt lifecycle flow
inputs: approved idea/trigger, brand brain, order/event history, registry
outputs: flow brief in the fixed output-contract shape
---
# Build a lifecycle flow

## Purpose
One procedure runs every flow build. The flow type picks the sub-skill; the shape of the
job (confirm trigger, set filters, map steps, draft copy, check discount, assemble brief)
never changes.

## Steps
1. Read the idea or trigger and name the flow type (welcome, browse-cart-abandon,
   post-purchase, win-back, sunset, back-in-stock, replenishment, loyalty-vip).
2. Load the matching sub-skill for that type; it owns the timing and content logic.
3. Confirm the trigger event actually fires in this store's data before building around it.
4. Set entry, exit and re-entry filters against every other live flow.
5. Map delay, channel and purpose per step using the sub-skill's rule.
6. Draft copy per step and channel via life/message; claim-check every step.
7. Set discount eligibility, if any, via life/discount-policy-check.
8. Assemble the flow brief and run the LIFE self-QA checklist.

## Checks
Trigger confirmed. No stage overlap with another flow. Every claim checked. Output
matches the flow-brief shape exactly.

## Output
A flow brief ready for the founder gate, plus the registry stub for the read point.

## Example
Idea: "Win-back flow underperforms; rebuild timing off purchase cadence." Output: a
3-email, 2-SMS win-back brief entering at 1.5x the customer's own average order gap,
exiting on purchase, no discount until email 3, read point 45 days post-launch.
