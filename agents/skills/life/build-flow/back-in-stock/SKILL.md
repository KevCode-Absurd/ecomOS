---
name: build-flow/back-in-stock
owner: LIFE
version: 1
invoke_when: the flow type is back-in-stock (real restock event) or a post-delivery education trigger
inputs: confirmed trigger event, brand voice, claims tiers
outputs: step list (delay, channel, purpose per step)
---
# Back-in-stock and post-delivery education triggers

## Purpose
Owns the timing and content logic specific to the back-in-stock flow type, called by the
parent life/build-flow skill once the trigger is confirmed.

## Steps
1. Confirm the back-in-stock trigger fires from real store data.
2. Apply the timing rule: back-in-stock fires only from a real restock webhook, never a guessed date; post-delivery education fires on the delivery-confirmed event.
3. Set content focus per step: back-in-stock is a single, factual notification with a direct link; post-delivery education teaches product use and sets up the review request timed in life/review-program.
4. Flag where a discount could sit, for life/discount-policy-check to clear.
5. Hand the step list back to life/build-flow for copy drafting and assembly.

## Checks
Trigger is real and recent. Timing matches this type's own rule. Content matches the
customer's actual state at this point, not a generic template.

## Output
Step list: {delay, channel, purpose} per step.

## Example
Restock webhook fires at 2pm for SKU X. Every waitlisted customer gets one email within the hour, no discount attached unless one was already promised at waitlist signup.
