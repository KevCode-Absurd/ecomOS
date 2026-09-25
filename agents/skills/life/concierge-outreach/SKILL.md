---
name: concierge-outreach
owner: LIFE
version: 1
invoke_when: designing proactive live-chat outreach, phone-concierge follow-up,
  or the outbound voice/IVR channel
inputs: site analytics, VIP/segmentation list, cart abandonment data above an AOV
  threshold, consent and quiet-hour rules
outputs: proactive-chat trigger and opener set, ranked call queue and scripts,
  IVR scripts and cadence
---
# Proactive outreach: chat, phone and voice/IVR

## Purpose
Designs the three outbound-initiated concierge channels, proactive chat for a
high-intent visitor, a phone queue for high-AOV abandoners, and automated IVR for
COD confirmation and satisfaction checks, each with its own trigger and channel
fit, never dialling or sending on its own.

## Steps
1. Define the intent signals that qualify a visitor for proactive chat (visit
   count, product viewed, known VIP status).
2. Write a specific opener per signal, never a generic greeting, with a cap on
   how often one visitor is approached.
3. Set the AOV or product-category threshold above which a phone call beats
   email/SMS, from the brand's own AOV distribution.
4. Write call scripts per scenario (cart-abandon, pre-purchase question, VIP
   check-in) and build the ranked daily call queue by value and recency.
5. Choose which events justify automated IVR (COD pre-dispatch confirmation,
   delivery-failure follow-up, post-resolution satisfaction check) and write the
   IVR scripts, matching the quiet-hour rules already set for SMS/WhatsApp.
6. Set outcome logging for chat, call and IVR back into the customer record.

## Checks
Every signal and threshold is specific and evidence-based. IVR quiet hours match
the standing channel policy. A human places every call; nothing auto-dials.

## Output
A proactive-chat opener set, a ranked call queue with scripts, and IVR scripts
with cadence.

## Example
"AOV threshold: ₹15,000 (top decile of orders). Cart-abandon script for this tier
opens: 'Saw you were looking at the sapphire set - happy to answer sizing
questions before you decide.'"
