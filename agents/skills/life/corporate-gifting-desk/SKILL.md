---
name: corporate-gifting-desk
owner: LIFE
version: 1
invoke_when: an inbound B2B gifting enquiry arrives, or outbound gifting-season
  lead work begins (about 90 days before the Q4 holiday season; Diwali for India)
inputs: the enquiry or lead source, bulk pricing tiers, customisation options,
  sales-tax invoicing capability (GST invoicing capability for India), split-delivery
  address list
outputs: bulk quote, sales-tax invoice draft (GST invoice draft for India),
  split-delivery plan, repeat-order reminder
---
# Corporate gifting sales desk

## Purpose
Runs B2B gifting orders end to end: qualifying the enquiry or building the
outbound list in season, quoting from the standing bulk tiers, preparing a
sales-tax-correct invoice (GST-correct for India), planning delivery to many
addresses, and setting up next season's repeat-order reminder.

## Steps
1. Qualify an inbound enquiry for quantity, budget and occasion, or build the
   outbound lead list starting 90 days before the target Q4 holiday season
   (or festival, for India).
2. Quote using the standing bulk pricing tiers, checked against margin; anything
   beyond the standing tiers is founder_gate.
3. Confirm custom packaging or engraving options and their real lead time.
4. Prepare a sales-tax invoice, checked against state nexus and resale-
   certificate rules; for India, prepare a GST-compliant invoice checked against
   the current rate and the buyer's GSTIN if given.
5. Plan delivery to each recipient address, checking courier serviceability for
   every one before the order is confirmed.
6. Set a repeat-order reminder for next season, timed to the same lead-time rule.

## Checks
Quote stays inside the standing bulk tiers, or is gated. Sales-tax (or GST, for
India) invoice checked against the current rule with date. Every address checked
for serviceability.

## Output
A bulk quote, a sales-tax invoice draft (a GST invoice draft for India), a
split-delivery plan, and a repeat-order reminder.

## Example
"50-unit corporate order, standard bulk tier 3 ($38/unit). Engraving lead time:
5 business days, confirmed against the partner's stated capacity. (India: same
process, quoted in INR with a GST invoice.)"
