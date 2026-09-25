---
name: channel-policy
owner: LIFE
version: 1
invoke_when: setting or refreshing the rules for SMS, WhatsApp or push
inputs: channel cost data, consent state per channel, current channel mix
outputs: channel policy document
---
# Channel policy: SMS, WhatsApp and push

## Purpose
Sets what each non-email channel is for, how often it sends and what it costs to
run, so channels do not duplicate the same message to the same customer.

## Steps
1. Pull real per-message cost and volume for SMS, WhatsApp and push.
2. Check consent coverage per channel; a channel below its market's legal
   threshold is flagged before any cadence policy is set.
3. Assign content scope per channel (SMS: time-sensitive short offers and order
   updates by default; WhatsApp: order updates and high-value recovery where used,
   common in India, EU or LATAM; push: on-site nudges).
4. Set a per-customer weekly cadence cap and a monthly spend cap, sized to the
   real cost data.
5. Where SMS cost per send is high relative to WhatsApp (common in India, EU or
   LATAM), recommend shifting eligible message types, contingent on WhatsApp consent
   and template approval.

## Checks
Caps sized from real cost data, not a round number. No message type duplicated
across two channels to the same customer at once.

## Output
A channel policy document: content scope, cadence caps, cost caps, and any
recommended channel swap.

## Example
"SMS costs 3x WhatsApp per send in India. Move order-update messages to WhatsApp;
keep flash-sale urgency on SMS where WhatsApp template approval would be too slow."
