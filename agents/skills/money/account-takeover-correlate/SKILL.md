---
name: money/account-takeover-correlate
owner: MONEY
version: 1
invoke_when: login events across admin systems need correlating for a signal no single tool sees alone
inputs: Shopify admin, ad account, ESP and payment processor login logs
outputs: matched login sequences, anomaly flags, ranked exposure list
---
# Correlate account-takeover signals across systems

## Purpose
A single system's own alert stays quiet when a login looks normal to it; this skill compares the same person's logins across every admin-level system at once.

## Steps
1. Pull login geography, device and time from Shopify admin, the ad accounts, the ESP and the payment processor.
2. Match login events for the same person across at least 2 systems within a short time window.
3. Flag any sequence where geography or device differs from that person's normal pattern, even if each individual system's own alert stayed quiet.
4. Rank the flag by the worst action that account could take: change payment settings, move ad budget, or export customer data.

## Checks
- A match requires the same person's account across at least 2 systems, not one system's activity alone.
- The ranking states the specific worst action available to that account, not just that a login looked unusual.

## Output
Matched login sequences, anomaly flags, and a ranked exposure list.

## Example
An admin logs into Shopify from a new city at 2am, then into the ad account from the same new city 40 minutes later; the correlation flags it as high exposure because that admin account can move ad budget.
