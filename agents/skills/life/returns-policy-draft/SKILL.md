---
name: returns-policy-draft
owner: LIFE
version: 1
invoke_when: designing the returns/exchange/refund flow or its customer-facing
  policy text
inputs: policy data, failed-delivery/fraud/chargeback data (RTO for India), per-market law
outputs: returns flow spec and policy draft text
---
# Returns and refund flow design

## Purpose
Designs return speed targets, the refund-vs-credit choice, the self-service portal
rules, and failed-delivery/fraud controls (return-to-sender risk for the US;
COD RTO/fraud controls for India), then writes the customer-facing policy text,
checked against law per market.

## Steps
1. Read the live policy and the last quarter's return rate, reasons and refund-
   cycle time from order/support data.
2. Check the legal minimum return window and disclosure per market.
3. Set separate speed targets for time-to-pickup and time-to-refund-after-receipt.
4. Design the refund-vs-credit choice, sizing any credit bonus against real margin.
5. Set self-service rules: what a customer can do alone versus what routes to a
   human (fraud-flagged and high-value returns always route to a human).
6. Set the address-risk/fraud check before a replacement ships (ZIP/address-
   validation history for the US; pincode-level RTO/fraud check for COD orders in
   India).
7. Write the policy text and check it is visible pre-purchase, not just at checkout.
8. Confirm the investment is justified by returners' actual repeat-purchase rate.

## Checks
Policy checked against law per market. Fraud-flagged returns never fully self-
service. Investment level matches the measured repeat-rate lift.

## Output
A returns flow spec plus policy draft text, both dated and market-checked.

## Example
"Time-to-refund target: 3 days after receipt (was 9). Return-to-sender check:
addresses with repeat delivery failures require address confirmation before a
replacement ships. India: pincodes with RTO rate over 15% require ID confirmation
before a COD replacement ships."
