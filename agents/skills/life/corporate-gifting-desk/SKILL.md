---
name: corporate-gifting-desk
owner: LIFE
version: 1
invoke_when: an inbound B2B gifting enquiry arrives, or outbound gifting-season
  lead work begins (about 90 days before Diwali)
inputs: the enquiry or lead source, bulk pricing tiers, customisation options,
  GST invoicing capability, split-delivery address list
outputs: bulk quote, GST invoice draft, split-delivery plan, repeat-order reminder
---
# Corporate gifting sales desk

## Purpose
Runs B2B gifting orders end to end: qualifying the enquiry or building the
outbound list in season, quoting from the standing bulk tiers, preparing a GST-
correct invoice, planning delivery to many addresses, and setting up next
season's repeat-order reminder.

## Steps
1. Qualify an inbound enquiry for quantity, budget and occasion, or build the
   outbound lead list starting 90 days before the target festival.
2. Quote using the standing bulk pricing tiers, checked against margin; anything
   beyond the standing tiers is founder_gate.
3. Confirm custom packaging or engraving options and their real lead time.
4. Prepare a GST-compliant invoice, checked against the current rate and the
   buyer's GSTIN if given.
5. Plan delivery to each recipient address, checking courier serviceability for
   every one before the order is confirmed.
6. Set a repeat-order reminder for next season, timed to the same lead-time rule.

## Checks
Quote stays inside the standing bulk tiers, or is gated. GST invoice checked
against the current rule with date. Every address checked for serviceability.

## Output
A bulk quote, a GST invoice draft, a split-delivery plan, and a repeat-order
reminder.

## Example
"50-unit corporate order, standard bulk tier 3 (₹380/unit). Engraving lead time:
5 business days, confirmed against the partner's stated capacity."
