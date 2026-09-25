---
name: message/sms
owner: LIFE
version: 1
invoke_when: the channel is SMS
inputs: brief, brand voice, claims tiers, consent state
outputs: {body, link, opt_out_line}
---
# SMS message drafting

## Purpose
Writes short, compliant SMS copy for a flow or campaign step: brand name up
front, a single link, and the opt-out instruction consent-governance requires,
all inside the quiet-hours window and cadence cap life/channel-policy has
already set for this brand and market. SMS earns its place through urgency and
brevity, not through carrying the same content an email already sent.

## Steps
1. Draft the message inside a carrier-friendly character length, with one link
   at most; a second link splits attention and often breaks link shortening.
2. Put the brand name at the very start of the message and add the opt-out
   instruction at the end, per the consent-governance rule for this market.
3. Check the scheduled send time against the quiet-hours window and the
   per-customer weekly cadence cap before it is queued.
4. Cut any factual claim that cannot be stated accurately inside the space
   available, rather than compressing it into something misleading.

## Checks
Opt-out instruction is present on every send. Quiet hours are respected for the
recipient's own market. Exactly one link appears in the message.

## Output
{body, link, opt_out_line}

## Example
"[Brand] Still want the Aria necklace? Your cart's saved: [link]. Reply STOP to
opt out." - one link, brand-first, opt-out included, sent inside quiet hours.
