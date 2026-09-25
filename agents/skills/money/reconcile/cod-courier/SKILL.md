---
name: money/reconcile/cod-courier
owner: MONEY
version: 1
invoke_when: cash on delivery is collected by a courier and needs matching to what actually reached the bank
inputs: courier COD collection report, courier remittance report, courier SLA cycle, bank statement
outputs: aged COD gap table by courier with escalation notes
---
# Reconcile COD cash and courier remittance

## Purpose
COD cash sits with the courier until it is remitted. This skill ages that gap by courier so a slow remittance is caught before it becomes a cash problem instead of an accounting afterthought.

## Steps
1. Pull the courier's own collection report and remittance report for the period.
2. Match collected cash per order to the remittance that eventually lands in the bank.
3. Age every gap in days, by courier, against that courier's own stated SLA cycle.
4. For any remittance stuck past the SLA, build the escalation note: the order IDs, the amount, and the SLA clause it breaches.
5. Feed the unremitted total into the cash forecast as a receivable, never as cash in hand.

## Checks
- Aging never blends couriers together; each courier has its own SLA cycle.
- An escalation cites the SLA clause by name, not a general complaint.
- Unremitted COD lowers the cash forecast's available cash, it does not inflate it.

## Output
A table by courier: collected, remitted, gap, age in days, SLA cycle days, and an escalation flag with order IDs where the gap exceeds the SLA.

## Example
Courier X's SLA is a 7-day remittance cycle; an 82,000 rupee batch sits at 11 days. The escalation names the 34 order IDs and cites the 7-day clause in the courier's own service agreement.

## Market note
This skill applies only to an India-selling brand that runs cash on delivery. It reads null for a US-only brand, whose payout reconciliation runs through money/reconcile/gateway and money/reconcile/marketplace, with money/reconcile/chargebacks handling disputes.
