---
name: holiday-gifting-ops
owner: site-specialist
version: 1
invoke_when: 60 days before a holiday or gifting window (Black Friday, Cyber Monday, the Q4 holiday season, Valentine's Day, Mother's Day, Father's Day, back to school; India market option: Diwali, Rakhi or wedding season)
inputs: gifting calendar (shared with Lifecycle), brand brain shipping cutoffs by ZIP code (by pincode for India), catalogue
outputs: gift wrap/message configuration, hidden-price invoice flow, ZIP code delivery cutoff map (pincode map for India), gift guide pages
---
# Run holiday and gifting operations

## Purpose
Turn a store into gift-buying mode on schedule, without ever promising a delivery date the carrier can't keep, and turn it back off cleanly afterward.

## Steps
1. Confirm the gifting window and its cutoff dates from the shared gifting calendar 60 days out.
2. Turn on gift wrap and a gift-message option on relevant products.
3. Build a price-hidden gift invoice path so a recipient never sees the price paid.
4. Set delivery-by-date cutoffs per ZIP code from real carrier data (per pincode where the brand sells in India), never a flat national promise.
5. Build gift guides grouping the catalogue by recipient and occasion, using only real product and price data.
6. Switch relevant PDPs and the homepage to gifting-mode messaging for the window's duration.
7. QA the full gift-wrap-to-hidden-price-to-delivery-cutoff path as a real gift buyer would experience it.
8. Switch everything back to normal mode the day after the window closes, and log cutoff accuracy for next year.

## Checks
- No gift order ever promises a delivery date the ZIP code's (or pincode's) real cutoff cannot support.
- Gifting mode is confirmed fully reverted after the window.

## Output
Gift wrap/message configuration, a hidden-price invoice flow, a ZIP code delivery cutoff map (pincode map for India), and gift guide pages.

## Example
"Black Friday and Cyber Monday window: cutoff set at 3 business days before December 25 for standard shipping zones, 6 days for remote ZIP codes, pulled from real carrier transit-time data, not a single national date. India market option: Diwali window cutoff set at 3 days before the festival for metro pincodes, 6 days for others."
