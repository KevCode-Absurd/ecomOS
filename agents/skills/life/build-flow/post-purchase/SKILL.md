---
name: build-flow/post-purchase
owner: LIFE
version: 1
invoke_when: the flow type is post-purchase (after order 1, before order 2)
inputs: confirmed trigger event, brand voice, claims tiers
outputs: step list (delay, channel, purpose per step)
---
# Post-purchase content flow

## Purpose
Owns the timing and content logic specific to the post-purchase flow type, called by the
parent life/build-flow skill once the trigger is confirmed.

## Steps
1. Confirm the post-purchase trigger fires from real store data.
2. Apply the timing rule: starts at delivery confirmation, most of the sequence lands inside the 30-day window toward order 2.
3. Set content focus per step: split by first-time vs returning buyer: use-instructions and reviews-reduce-returns content for first-timers, complementary-product and loyalty content for returners.
4. Flag where a discount could sit, for life/discount-policy-check to clear.
5. Hand the step list back to life/build-flow for copy drafting and assembly.

## Checks
Trigger is real and recent. Timing matches this type's own rule. Content matches the
customer's actual state at this point, not a generic template.

## Output
Step list: {delay, channel, purpose} per step.

## Example
Delivered on day 0. Email at +1 day (how to use it), email at +7 (review request handed to life/review-program), email at +21 (complementary product, first-timer only).
