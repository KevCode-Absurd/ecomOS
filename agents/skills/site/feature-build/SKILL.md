---
name: feature-build
owner: site-specialist
version: 1
invoke_when: a subscription, loyalty, wishlist, B2B, returns portal, or restock/pre-launch capture feature is being added
inputs: brand brain repeat-purchase rate, wholesale demand, margin data, returns/waitlist app options
outputs: feature setup spec, flow diagram, configured feature, conversion/return-reason report
---
# Repeat-purchase, wholesale and demand-capture feature build

## Purpose
Build a customer-facing feature only where the product and margin genuinely support it, and spec it against real numbers rather than copying a generic app default.

## Steps
1. Check repeat-purchase rate or wholesale demand data before proposing a subscription, bundle, loyalty or B2B path.
2. For subscriptions: build distinct pause, skip, swap and cancel flows, and never pre-select the option in a quiz or at checkout.
3. For B2B: build a separate price list and a minimum-order or net-terms rule, keeping it invisible to consumer pricing.
4. For returns: configure against the brand's real return window and condition rules, and size an exchange-for-credit incentive from real margin.
5. For restock/pre-launch: add a notify-me capture and a password-protected coming-soon page, both feeding the brand's own list.
6. Surface the resulting structured data (return reasons, waitlist conversion) back to product and copy workflows.

## Checks
- No pre-selected option commits a shopper to more than they chose.
- Every financial incentive traces to a real margin number.
- Signups and return data land only in the brand's own systems.

## Output
A feature setup spec and flow diagram, the configured feature, and a report on conversion or return reasons.

## Example
"Exchange-for-credit incentive: 10% bonus credit, sized against the category's 38% margin, still profitable after the bonus and the restocking cost."
