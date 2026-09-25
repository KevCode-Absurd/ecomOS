---
name: build-flow/win-back
owner: LIFE
version: 1
invoke_when: the flow type is win-back (a lapsed customer, timed off the brand's own purchase cadence)
inputs: confirmed trigger event, brand voice, claims tiers
outputs: step list (delay, channel, purpose per step)
---
# Win-back flow

## Purpose
Owns the timing and content logic specific to the win-back flow type, called by the
parent life/build-flow skill once the trigger is confirmed.

## Steps
1. Confirm the win-back trigger fires from real store data.
2. Apply the timing rule: starts when a customer passes 1.5x to 2x their own average order gap, not a flat day count for every brand.
3. Set content focus per step: leads with genuine value or news, not a discount, unless the customer's lapse cause is engagement decay with no other signal; an RTO-caused lapse routes to the trust-rebuild variant instead (see LIFE-W12).
4. Flag where a discount could sit, for life/discount-policy-check to clear.
5. Hand the step list back to life/build-flow for copy drafting and assembly.

## Checks
Trigger is real and recent. Timing matches this type's own rule. Content matches the
customer's actual state at this point, not a generic template.

## Output
Step list: {delay, channel, purpose} per step.

## Example
Customer's average gap is 40 days; no order at day 65 triggers entry. Email 1 (what's new, no discount), SMS at +5 days (soft nudge), email 2 at +10 days (matched offer sized to the customer's own value).
