---
name: wild-bet/retail-popup
owner: BRAND
version: 1
invoke_when: the bet's type is a physical retail pop-up, or a channel push (marketplace/retail) needing a packaging and format decision
inputs: target channel, current packaging format, brand guidelines
outputs: feasibility packet, type-specific execution brief
---
# Wild bet: retail pop-up or channel entry

## Purpose
A retail pop-up or a new sales channel often fails on format and packaging fit before it ever fails on demand: a DTC-only box does not survive shelf handling, and a DTC price story does not survive a marketplace price-comparison page. This skill checks channel fit first.

## Steps
1. Decide which product format and packaging fits the target channel: a shelf-ready box for retail, a marketplace-compliant listing format, or the existing DTC format if the channel is another owned or partner site.
2. Brief the specific packaging and identity changes the channel needs (see `packaging-label-brief` for the mandatory-declaration side of this).
3. If this is a physical pop-up, size the activation to what the team can run by hand: staffing, footfall handling, and how sales get logged.
4. Write the execution brief sequencing packaging or listing changes before the buyer pitch or the activation itself; nothing launches in a new channel wearing DTC-only packaging.

## Checks
- Packaging or listing fit is checked against this specific channel's real constraints, not assumed identical to DTC.
- A physical activation is sized to real team capacity, cross-checked with `event-popup-design`.

## Output
`{feasibility_packet: {channel_fit, packaging_brief}, execution_brief}`

## Example
Target channel: a 3-day retail pop-up at a wedding expo. Packaging brief flags the DTC mailer box will not survive being carried by hand at a crowded venue; a compact gift-box format is briefed instead, reusing the existing brand palette.
