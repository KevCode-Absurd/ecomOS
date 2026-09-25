---
name: popup-spec
owner: LIFE
version: 1
invoke_when: designing or testing an on-site capture pop-up or form
inputs: brand products, audience, metric contract, current pop-up config
outputs: pop-up spec plus test queue
---
# On-site capture pop-up design

## Purpose
Designs the sign-up pop-up (offer, fields, trigger timing, targeting, layout) and
queues the test order, judged by what the sign-up is worth over time, not the
opt-in rate alone.

## Steps
1. Choose the offer type (percent, flat, gift, non-discount hook) from margin and
   discount policy, before any copy is written.
2. Set the minimum fields to capture, the trigger (time, scroll, exit-intent) and
   exclusions (existing subscribers, checkout page).
3. Draft mobile and desktop copy variants at a skimmable reading level.
4. Sequence the test queue: offer type first, then copy, then design, one variable
   at a time, versus the current control.

## Checks
No hidden or hard-to-find close button. Exclusions cover existing subscribers.
Judged by full-site conversion and list value per visitor, not opt-in rate.

## Output
Pop-up spec (offer, fields, trigger, targeting, copy) plus a sequenced test queue.

## Example
"Offer: free shipping over reference threshold, not 10% off (protects margin).
Trigger: exit-intent, desktop only. Test 1: this offer vs current 10%-off control."
