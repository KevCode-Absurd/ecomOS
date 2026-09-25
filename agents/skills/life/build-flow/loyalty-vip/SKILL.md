---
name: build-flow/loyalty-vip
owner: LIFE
version: 1
invoke_when: the flow type is loyalty/VIP (points earned, tier change, redemption, birthday)
inputs: confirmed trigger event, brand voice, claims tiers
outputs: step list (delay, channel, purpose per step)
---
# Loyalty, VIP and birthday triggered flows

## Purpose
Owns the timing and content logic specific to the loyalty-vip flow type, called by the
parent life/build-flow skill once the trigger is confirmed.

## Steps
1. Confirm the loyalty-vip trigger fires from real store data.
2. Apply the timing rule: fires off the loyalty platform's own event webhook (points earned, tier change, redemption, birthday date), not a schedule guess.
3. Set content focus per step: confirms the specific event and reward in plain language, and for a tier change, states what is now unlocked.
4. Flag where a discount could sit, for life/discount-policy-check to clear.
5. Hand the step list back to life/build-flow for copy drafting and assembly.

## Checks
Trigger is real and recent. Timing matches this type's own rule. Content matches the
customer's actual state at this point, not a generic template.

## Output
Step list: {delay, channel, purpose} per step.

## Example
Tier-change webhook fires: customer moves to Gold. Email within the hour naming the new perks unlocked, distinct from a generic marketing send.
