---
name: consent-governance
owner: LIFE
version: 1
invoke_when: a new market or sign-up form is added, or a channel policy needs its
  consent rule confirmed
inputs: markets sold into, consent records per platform, per-market law reference
outputs: consent rule set, quiet-hours table, unsubscribe SLA
---
# Consent, quiet hours and unsubscribe governance

## Purpose
Keeps every send legal by market: the right opt-in model, the right quiet-hours
window in local time, and an unsubscribe that is honoured immediately.

## Steps
1. List markets from real shipping/billing geography, not assumptions.
2. Research the opt-in model, record-keeping rule and quiet-hours window per market,
   with source and date.
3. Compare current ESP/SMS/WhatsApp consent fields against each market's rule and
   list every gap by name.
4. Set the quiet-hours schedule in local time per market and channel.
5. Set the unsubscribe/STOP SLA at or above the strictest applicable market law.

## Checks
Every legal claim has a URL and date. Quiet hours use local time, not the brand's
home timezone. Unsubscribe SLA meets or beats the legal minimum.

## Output
A consent rule set, a quiet-hours table, and an unsubscribe SLA, each per market.

## Example
"India: DPDP Act needs affirmative opt-in for WhatsApp marketing; quiet hours
9pm-9am IST for SMS. Gap: current form has no separate WhatsApp consent checkbox."
