---
name: build-flow/welcome
owner: LIFE
version: 1
invoke_when: the flow type is welcome (new subscriber, no purchase yet)
inputs: confirmed trigger event, brand voice, claims tiers
outputs: step list (delay, channel, purpose per step)
---
# Welcome flow

## Purpose
Owns the timing and content logic specific to the welcome flow type, called by the
parent life/build-flow skill once the trigger is confirmed.

## Steps
1. Confirm the welcome trigger fires from real store data.
2. Apply the timing rule: front-loaded into the first 72 hours from signup, using the pop-up offer if one exists.
3. Set content focus per step: brand story, best-sellers, social proof, then the offer reminder with any urgency honestly framed.
4. Flag where a discount could sit, for life/discount-policy-check to clear.
5. Hand the step list back to life/build-flow for copy drafting and assembly.

## Checks
Trigger is real and recent. Timing matches this type's own rule. Content matches the
customer's actual state at this point, not a generic template.

## Output
Step list: {delay, channel, purpose} per step.

## Example
Signup at 10am Monday. Email 1 at signup (welcome, offer), email 2 at +24h (best-sellers), SMS at +48h (offer reminder), email 3 at +72h (last call on the offer, real deadline).
