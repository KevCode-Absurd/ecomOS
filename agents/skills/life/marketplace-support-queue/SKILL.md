---
name: marketplace-support-queue
owner: LIFE
version: 1
invoke_when: managing Amazon/Walmart Marketplace buyer-seller messages (Flipkart,
  Myntra for India) or A-to-Z-style guarantee claims
inputs: marketplace seller console access, order and delivery-proof data
outputs: drafted responses within each marketplace's clock, claim-rate trend
---
# Marketplace seller-support queue management

## Purpose
Runs marketplace buyer-seller messages and guarantee claims on each marketplace's
own response clock (about 48 hours for a message, about 72 for a claim), kept
separate from the brand's own helpdesk SLAs and tagging.

## Steps
1. Pull the open queue from each marketplace's own seller console and tag every
   item with its own deadline.
2. Draft the buyer-message response inside that window, in the brand's voice.
3. Assemble the delivery proof and correspondence log a claim needs, matched to
   what that specific marketplace accepts as evidence.
4. Draft the claim response with that evidence, inside the claim's own clock.
5. Track claim rate and reason over time, flagging a rising rate to the
   returns/fulfilment specialist.

## Checks
Every response respects its own marketplace's clock; missing the message-window
deadline can itself trigger a claim right. Queue and SLA tracking stay separate
from the brand's own helpdesk.

## Output
Drafted responses inside each clock, plus a claim-rate trend report.

## Example
"Buyer message at hour 40 of the 48-hour Amazon window: drafted and flagged
urgent. Claim rate this month: 0.4% of orders, flat versus last month. (India:
same process on Flipkart/Myntra's own clock.)"
