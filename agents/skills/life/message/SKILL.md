---
name: message
owner: LIFE
version: 1
invoke_when: any flow, campaign, support or review step needs drafted copy
inputs: the brief, brand voice, claims tiers, relevant reviews
outputs: draft copy with claims cited, channel-appropriate
---
# Draft channel message copy

## Purpose
One drafting procedure, channel picked by select_by. Keeps subject/preview/body rules
for email separate from the character and consent rules for SMS and WhatsApp.

## Steps
1. Read the brief's purpose, audience and any discount/urgency rule.
2. Load the matching life/message/<channel> sub-skill.
3. Draft at or below tenth-grade reading level, in the brand's voice.
4. Hold discount mentions to the brief's specified position.
5. Cite every factual claim to a brand-record field.
6. Return the draft, flagged for shared/claim-check before it ships anywhere.

## Checks
Reading level under grade 10. No invented number or claim. Channel format matches
the sub-skill's rule (email has subject/preview lines; SMS/WhatsApp do not).

## Output
Draft copy per channel, claims cited, marked as a draft for human edit.

## Example
Brief: cart-abandon step 1, SMS, no discount. Output: "Still thinking about the Aria
necklace? It's saved in your cart. [link]" - short, no discount, one link, consent
footer per policy.
