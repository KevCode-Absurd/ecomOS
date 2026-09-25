---
name: build-flow/replenishment
owner: LIFE
version: 1
invoke_when: the flow type is replenishment (one-off reminder) or subscription lifecycle messaging (charge reminder, pause-or-skip, failed payment)
inputs: confirmed trigger event, brand voice, claims tiers
outputs: step list (delay, channel, purpose per step)
---
# Replenishment and subscription lifecycle messaging

## Purpose
Owns the timing and content logic specific to the replenishment flow type, called by the
parent life/build-flow skill once the trigger is confirmed.

## Steps
1. Confirm the replenishment trigger fires from real store data.
2. Apply the timing rule: timed to the product's real use-up cycle for replenishment reminders, and to the actual charge date for subscription messages; use predictive per-customer timing where enough order history exists, falling back to the fixed cycle otherwise.
3. Set content focus per step: replenishment reminders are practical and low-pressure; subscription messages state the charge date, amount and easy pause/skip link plainly, no fine print.
4. Flag where a discount could sit, for life/discount-policy-check to clear.
5. Hand the step list back to life/build-flow for copy drafting and assembly.

## Checks
Trigger is real and recent. Timing matches this type's own rule. Content matches the
customer's actual state at this point, not a generic template.

## Output
Step list: {delay, channel, purpose} per step.

## Example
Product use-up cycle is 30 days. Reminder at day 25 (before running out), a subscription charge reminder 3 days before the card is charged, with a one-tap skip link.
