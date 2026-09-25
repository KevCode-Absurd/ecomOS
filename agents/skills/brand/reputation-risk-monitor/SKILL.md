---
name: reputation-risk-monitor
owner: BRAND
version: 1
invoke_when: a spike in complaints, viral criticism, or a factual attack is detected, or on demand
inputs: public mention/review monitoring, brand records to verify or refute a claim
outputs: spike alert, fact verification note, draft holding statement, escalation note
---
# Reputation risk monitor

## Purpose
Speed and accuracy both matter in a reputation moment: acting fast on a wrong fact makes things worse. This skill verifies before it drafts, and always routes to the founder before anything goes public.

## Steps
1. Watch public mentions and reviews for a sudden spike in complaint volume, a viral criticism, or a specific factual attack, measured against a real baseline rate, not a single loud post.
2. Verify the underlying claim against the brand's own records before drafting anything; state whether it is true, false, or partially true, with the evidence.
3. Assess how far the criticism has spread and how much real brand or revenue risk it carries, using actual reach numbers where available.
4. Draft a short holding statement that acknowledges the issue and states what happens next, making no claim the verification step does not support, and draft an escalation note naming who needs to see this and what decision they must make.

## Checks
- The spike is measured against a baseline, never triggered by a single post.
- The holding statement never claims more than the fact-verification step actually established.
- Nothing is posted, replied to, or sent without founder review, always.

## Output
`{spike_alert, fact_verification_note, draft_holding_statement, escalation_note}`

## Example
Spike: complaint volume on one SKU up 6x normal rate in 48 hours. Verification: a batch defect is confirmed against internal QC records. Statement drafted acknowledging the specific batch and a stated fix timeline, nothing broader claimed.
