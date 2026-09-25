---
name: prod/claims-file
owner: PROD
version: 1
invoke_when: a shipment is marked lost or damaged, or marketplace inventory or fees need reimbursement
inputs: shipment/return-to-sender records (india: RTO records), proof of loss or damage (photos, weight, seal
  condition), marketplace seller console access, fee statements
outputs: filed courier and marketplace claims with proof attached, and a tracked payout status
---
# File courier and marketplace claims

## Purpose
Money owed for a lost, damaged, or wrongly billed unit is only recovered if someone files the claim with proof and
tracks it to payout. This skill covers both carrier-side claims (lost/damaged shipments) and marketplace-side
claims (FBA reimbursements, Walmart/eBay/TikTok Shop claim programs; india: Flipkart SPF, Myntra claims) with the
same discipline: proof first, then file, then track.

## Steps
1. Identify every shipment marked lost, damaged, or wrongly marked return-to-sender in the review period (india:
wrongly marked RTO; markets: IN).
2. Assemble proof for each: photos of the package or product condition, any weight discrepancy against the
   shipping manifest, seal condition on return.
3. File the courier claim with the carrier or aggregator, proof attached, within their stated filing window.
4. Separately, find lost or damaged marketplace inventory and any wrongly charged fee inside each seller console,
   and file the matching reimbursement claim type for that platform (FBA reimbursement, Walmart Seller Center
   claim, eBay/TikTok Shop claim; india: Flipkart SPF, Myntra claim).
5. Track payout against every open claim: a claim is only marked paid once the payout is actually confirmed, not
   simply once it is filed.
6. Escalate any claim that has passed its normal resolution window.

## Checks
- No claim is filed without an attached proof packet.
- Payout status reflects confirmed payment, never an assumption.

## Output
{incident_list[], filed_claims[], payout_tracker[], escalations[]}

## Example
3 shipments this week marked damaged; proof (photos, weight mismatch) assembled and filed with the carrier.
Separately, an FBA reimbursement claim filed for 2 units lost in an Amazon warehouse, confirmed paid within 12
days. One carrier claim escalated after exceeding its 15-day resolution window.
