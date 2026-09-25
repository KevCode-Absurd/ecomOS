---
name: money/reconcile/gateway
owner: MONEY
version: 1
invoke_when: a payment gateway settles a batch of orders to the bank
inputs: gateway settlement file, bank statement, fee schedule
outputs: per-payout reconciliation with bank match
---
# Reconcile payment gateway settlement

## Purpose
A gateway payout is never the same as gross sales. This skill unbundles every payout into its real parts so the books never show one lump deposit.

## Steps
1. Pull the settlement file for the period and the matching bank statement.
2. For each payout, unbundle gross sale, gateway fee, refund, GST charged on the fee, and any FX adjustment for cross-border payments.
3. Match the net figure to the actual bank credit.
4. Age any payout not credited inside the gateway's stated settlement window (typically T+1 to T+3).
5. Draft the journal entry with each unbundled line as its own account.

## Checks
- Fee and GST on fee never merge into one line.
- FX adjustment is separated from the fee, never hidden inside it.
- An aged payout carries a day count, not a vague 'pending' label.

## Output
One row per payout: gross, fee, GST on fee, refund, FX adjustment, net, bank match status, age in days.

## Example
A payout of 118,000 rupees unbundles to 122,500 gross sale, minus 2,100 fee, minus 378 GST on the fee, minus 2,022 refunds, net 118,000, matched to the bank credit dated 2 days later.
