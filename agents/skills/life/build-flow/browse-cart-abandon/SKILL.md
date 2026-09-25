---
name: build-flow/browse-cart-abandon
owner: LIFE
version: 1
invoke_when: the flow type is browse abandonment or cart/checkout abandonment
inputs: confirmed trigger event, brand voice, claims tiers
outputs: step list (delay, channel, purpose per step)
---
# Browse and cart/checkout abandonment flow

## Purpose
Owns the timing and content logic specific to the browse-cart-abandon flow type, called by the
parent life/build-flow skill once the trigger is confirmed.

## Steps
1. Confirm the browse-cart-abandon trigger fires from real store data.
2. Apply the timing rule: browse abandon starts 1-3 hours after a product view with no add-to-cart; cart/checkout abandon starts 30-60 minutes after cart or checkout start with no order.
3. Set content focus per step: browse abandon reads as a shop-assistant follow-up, not a hard sell; cart/checkout abandon uses dynamic product blocks and holds any discount back to a later step, never the first message.
4. Flag where a discount could sit, for life/discount-policy-check to clear.
5. Hand the step list back to life/build-flow for copy drafting and assembly.

## Checks
Trigger is real and recent. Timing matches this type's own rule. Content matches the
customer's actual state at this point, not a generic template.

## Output
Step list: {delay, channel, purpose} per step.

## Example
Cart abandoned at 3:15pm. SMS at +1h (no discount, just a reminder with the product), email at +4h (dynamic cart block, still no discount), email at +24h (discount appears for the first time, framed against a real reason to buy now).
