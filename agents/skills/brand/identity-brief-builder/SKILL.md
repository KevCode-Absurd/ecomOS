---
name: identity-brief-builder
owner: BRAND
version: 1
invoke_when: a new identity or a major refresh needs mood, palette, typography and photography direction written
inputs: positioning statement, avatar record's aesthetic and price-tier expectations
outputs: identity direction brief, mood-only reference set
---
# Visual identity brief builder

## Purpose
This agent directs visual identity in words; it never generates the final logo or asset itself. This skill writes a brief specific enough for a designer or the Reference Scout to act on, grounded in the positioning and avatar, not personal taste.

## Steps
1. Describe the intended mood in concrete words tied to the positioning statement and what the avatar record says this customer expects at this price tier (for example, "quiet, not loud; craft-forward, not trend-forward").
2. Direct palette, typography and photography style in words and referenced mood only (cite the kind of reference: "muted jewel tones like X," "editorial photography style like Y"), never a specific competitor asset to imitate directly.
3. Hand the mood brief to the Reference Scout to pull real, mood-only visual references; this agent never sources or generates the final images itself.

## Checks
- The brief is entirely words and mood references; no invented final logo, mark, or asset appears in it.
- Any reference cited is for layout and mood only, never a competitor's actual logo, product photo or face to copy.

## Output
`{identity_direction_brief, reference_set}`

## Example
Brief: "Photography should feel like a personal collection, not a catalogue shoot: closer to editorial jewellery photography with natural light, never a white seamless background." Reference pull requested from Scout on that specific mood.
