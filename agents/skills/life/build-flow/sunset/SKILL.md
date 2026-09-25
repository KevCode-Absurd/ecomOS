---
name: build-flow/sunset
owner: LIFE
version: 1
invoke_when: the flow type is sunset (stopping mail to people who never engage)
inputs: confirmed trigger event, brand voice, claims tiers
outputs: step list (delay, channel, purpose per step)
---
# Sunset flow

## Purpose
Owns the timing and content logic specific to the sunset flow type, called by the
parent life/build-flow skill once the trigger is confirmed.

## Steps
1. Confirm the sunset trigger fires from real store data.
2. Apply the timing rule: starts after a fixed no-open/no-click window (commonly 90-180 days) with no purchase in the same window.
3. Set content focus per step: one last genuine re-permission ask, honest about the reason, then suppression, never a guilt-trip.
4. Flag where a discount could sit, for life/discount-policy-check to clear.
5. Hand the step list back to life/build-flow for copy drafting and assembly.

## Checks
Trigger is real and recent. Timing matches this type's own rule. Content matches the
customer's actual state at this point, not a generic template.

## Output
Step list: {delay, channel, purpose} per step.

## Example
No open in 120 days. Email 1: 'still want to hear from us?' with a one-click stay button. No click at +7 days: suppressed from regular sends, moved to a low-frequency list.
