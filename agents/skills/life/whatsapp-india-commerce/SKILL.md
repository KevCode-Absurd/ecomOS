---
name: whatsapp-india-commerce
owner: LIFE
version: 1
invoke_when: building or refreshing WhatsApp cart recovery, order updates or COD
  conversion for Indian buyers
inputs: India order/RTO data, courier NDR feed, WhatsApp template approval status
outputs: WhatsApp commerce program spec
---
# WhatsApp commerce program for India

## Purpose
Builds the India-specific WhatsApp program: cart recovery, order updates, a costed
COD-to-prepaid nudge, and automatic NDR recovery, where WhatsApp reach beats SMS
and email for Indian buyers.

## Steps
1. Pull COD share, RTO rate and cart abandonment scoped to Indian shipping
   addresses only, never blended with other markets.
2. Build the cart-recovery sequence using life/build-flow/browse-cart-abandon with
   WhatsApp as the lead channel.
3. Set order-update messages against real order-status events.
4. Size the COD-to-prepaid incentive against the RTO cost it measurably avoids.
5. Build the NDR recovery sequence to start the same day a courier logs a failed
   delivery.
6. Confirm every message type has an approved WhatsApp Business template before
   the flow can go live.

## Checks
Every figure scoped to India only. Incentive sizing traces to a real RTO-cost
number. No flow step ships on an unapproved template.

## Output
A WhatsApp commerce program spec covering cart recovery, order updates, COD-to-
prepaid and NDR recovery.

## Example
"RTO costs ₹180 per failed COD order on average. COD-to-prepaid nudge offers ₹50
off - well inside the ₹180 avoided cost - only on pincodes with RTO rate over 12%."
