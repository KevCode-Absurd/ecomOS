---
name: message/whatsapp
owner: LIFE
version: 1
invoke_when: the message channel is WhatsApp
inputs: brief, brand voice, claims tiers, template approval status
outputs: {template_name_or_freeform, variables, hand_off_point}
---
# WhatsApp message drafting

## Purpose
Writes WhatsApp copy inside Meta's template rules for outbound business-initiated
messages, and designs the reply-inviting opener for two-way conversations. WhatsApp is
a market option (common in India, EU and LATAM) where reach beats SMS and email; SMS
is the default second channel (see life/message/sms).

## Steps
1. Check whether an approved template exists for this message type; never draft
   around one that is missing or rejected.
2. Fill the template's variable slots, or write a free-form opener if the customer
   messaged first.
3. For a two-way conversation, open with a specific, reply-inviting question.
4. Name the point at which a real reply hands off to a human agent.

## Checks
No message sent on an unapproved template. Every two-way opener names its hand-off
point.

## Output
{template_name_or_freeform, variables, hand_off_point}

## Example
Template "order_shipped_v2": "Hi {{1}}, your order has shipped! Track here: {{2}}."
Two-way opener: "Did the resizing guide help, or would you like a hand?" - first
real reply hands off to support.
