---
name: prod/sample-qc-gate
owner: PROD
version: 1
invoke_when: a sample is received at any stage and must clear the reference before any downstream spend
inputs: an approved reference sample kept both in-house and at the factory, the tech pack, the new sample
outputs: stage-by-stage pass/hold/reject result with the exact deviation recorded
---
# Run the 3-stage sample gate

## Purpose
No creative shoot, price commitment or launch date happens before a sample from the exact factory clears this gate
against an approved reference. Working from memory or a photo instead of a physical reference produces drift no one
notices until a full production run fails.

## Steps
1. Confirm the approved reference sample is physically in-house before starting any comparison. If it only exists
   at the factory, stop and get it shipped first.
2. Run the 3-stage comparison: pre-production sample against reference, production sample against reference, and a
   pulled sample from the actual shipped batch against reference. Compare side by side on every dimension the tech
   pack specifies.
3. Score the factory's communication and reliability during the round: response time to questions, accuracy of
   what they claimed versus what arrived: separate from the physical sample's quality.
4. Record pass, hold or reject for each stage, with the exact deviation stated as a measurement (e.g., "wall
   thickness 2.1mm vs. spec 3mm ± 0.2mm"), never as an impression.

## Checks
- No stage begins without a confirmed, physical in-house reference.
- Every stage has a recorded result, none skipped.
- Every deviation is a number against the tech pack, not a subjective note.

## Output
{stage_results[{stage, result, deviation}], reliability_score, overall}

## Example
Stage 1: pass. Stage 2: hold: zipper pull 4mm shorter than spec, reference confirmed 6mm minimum. Factory
responded to the flag within 24 hours with a corrected sample. Stage 2 re-run: pass. Overall: pass, logged with the
one recorded deviation and its resolution.
