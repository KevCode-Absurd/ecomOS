---
name: festive-gifting-ops
owner: site-specialist
version: 1
invoke_when: 60 days before a Diwali, Rakhi, wedding-season or other gifting window
inputs: gifting calendar (shared with Lifecycle), brand brain shipping cutoffs by pincode, catalogue
outputs: gift wrap/message configuration, hidden-price invoice flow, pincode delivery cutoff map, gift guide pages
---
# Run festive gifting operations

## Purpose
Turn a store into gift-buying mode on schedule, without ever promising a delivery date the courier can't keep, and turn it back off cleanly afterward.

## Steps
1. Confirm the gifting window and its cutoff dates from the shared gifting calendar 60 days out.
2. Turn on gift wrap and a gift-message option on relevant products.
3. Build a price-hidden gift invoice path so a recipient never sees the price paid.
4. Set delivery-by-date cutoffs per pincode from real courier data, never a flat national promise.
5. Build gift guides grouping the catalogue by recipient and occasion, using only real product and price data.
6. Switch relevant PDPs and the homepage to gifting-mode messaging for the window's duration.
7. QA the full gift-wrap-to-hidden-price-to-delivery-cutoff path as a real gift buyer would experience it.
8. Switch everything back to normal mode the day after the window closes, and log cutoff accuracy for next year.

## Checks
- No gift order ever promises a delivery date the pincode's real cutoff cannot support.
- Gifting mode is confirmed fully reverted after the window.

## Output
Gift wrap/message configuration, a hidden-price invoice flow, a pincode delivery cutoff map, and gift guide pages.

## Example
"Diwali window: cutoff set at 3 days before the festival for metro pincodes, 6 days for others, pulled from real courier transit-time data, not a single national date."
