---
name: money/security-scan-weekly
owner: MONEY
version: 1
invoke_when: the weekly fraud, bot and abuse scan needs running
inputs: server/CDN logs, order and payment data, chargeback log, COD refusal log, return log, domain records
outputs: traffic baseline, fraud and abuse flags, domain watch result, weekly fix list
---
# Run the weekly fraud, bot and abuse scan

## Purpose
Catch card-testing, bot traffic, return abuse and domain impersonation early, with friction placed at checkout and account changes, never at ordinary browsing.

## Steps
1. Rebuild the bot and AI-agent traffic baseline by agent, endpoint and intent, and re-score risk tiers continuously.
2. Check for card-testing bursts (clusters of small failed authorizations) and review AVS/CVV/3DS settings against the false-decline rate.
3. Set the chargeback alert threshold below the processor's own flag level, and set prepayment triggers for repeat COD refusers.
4. Detect return and refund abuse: wardrobing, serial high-return customers, refunds without a matching return.
5. Watch the domain registrar lock status, DNS for dangling records, and lookalike domains or counterfeit listings.

## Checks
- No rule relies on User-Agent alone.
- Fraud caught is always tracked alongside the false-decline rate.

## Output
The traffic baseline, fraud and return-abuse flags, the domain watch result, and a ranked weekly fix list.

## Example
A burst of 40 small authorizations under 50 rupees each from the same IP range is flagged as card-testing before any of them succeed at a full-value order.
