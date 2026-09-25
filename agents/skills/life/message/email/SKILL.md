---
name: message/email
owner: LIFE
version: 1
invoke_when: the message channel is email
inputs: brief, brand voice, claims tiers
outputs: {subject, preview, body, cta, dynamic_block_ref}
---
# Email message drafting

## Purpose
Writes the email-specific fields a flow or campaign step needs: subject line,
preview text, body and CTA, none of which SMS or WhatsApp carry, and flags any
spam-trigger language before the draft reaches life/deliverability-audit. Email
is still the channel that carries the most product detail and dynamic content, so
this skill also marks where a dynamic block (cart contents, recommended products)
belongs for the build step that follows.

## Steps
1. Write the subject line and the preview text as two separate, complementary
   lines; the preview should add information, not repeat the subject.
2. Write the body at a skimmable length with exactly one clear call to action,
   never two competing links fighting for the same click.
3. Mark where a dynamic product block or personalised image belongs, so the
   email-build step can wire it correctly.
4. Screen the subject line for spam-trigger words, ALL-CAPS and excess
   punctuation before handing the draft on.

## Checks
Subject and preview are both written, never left blank. Exactly one CTA per
email. No unscreened spam-trigger language reaches the build step.

## Output
{subject, preview, body, cta, dynamic_block_ref}

## Example
Subject: "Your Aria necklace is still here." Preview: "Free shipping ends
tonight." Body: three short lines, one button reading "Finish my order," with a
dynamic_block_ref pointing at the customer's actual saved cart.
