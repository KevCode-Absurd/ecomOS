---
name: money/vendor-rfp-evaluation
owner: MONEY
version: 1
invoke_when: a vendor, 3PL or agency needs selecting, or an existing one needs an SLA audit
inputs: candidate vendor list, invoice history, SLA terms
outputs: RFP comparison, written SLA, invoice audit, vendor scorecard
---
# Run a competitive vendor or 3PL RFP

## Purpose
Select and hold vendors to a real, written standard instead of a single quote and a handshake.

## Steps
1. Run the RFP against at least 3 candidate vendors.
2. Run a facility visit for a 3PL, or a reference check for an agency.
3. Put the SLA in writing with a numeric target and a stated consequence for a miss.
4. Audit every incoming invoice against the SLA and the RFP-agreed rate.
5. Score the vendor on a fixed scorecard computed from the SLA data.

## Checks
- At least 3 vendors are compared before a selection.
- Every SLA line has a numeric target and a named consequence.

## Output
The RFP comparison, the written SLA, the invoice audit result, and the vendor scorecard.

## Example
A 3PL's invoice bills a pick-and-pack fee 12 percent above the RFP-agreed rate for 6 straight weeks; the audit flags the exact line before it becomes a pattern nobody caught.
