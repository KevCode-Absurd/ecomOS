---
name: prod/defect-capa-trace
owner: PROD
version: 1
invoke_when: a customer complaint or return points to a defect above the brand's stated threshold
inputs: the defect complaint record, tech pack version history, production batch or lot records
outputs: a batch trace, root cause, the corrective action and its verification result
---
# Trace a defect to its batch and run CAPA

## Purpose
A defect complaint that only gets logged as "SKU X has issues" cannot be fixed at the source. This skill traces the
complaint to the exact production run, using the tech pack's own version history, and runs a real corrective-action
loop with the supplier rather than accepting a verbal promise.

## Steps
1. Trace the defect complaint back to the exact production batch or lot, using the tech pack's version history and
   any batch codes on the product or packaging.
2. Once the batch is identified, check whether other units from the same batch generated complaints, to size the
   real exposure rather than treating this as an isolated incident.
3. Run the corrective-action loop with the supplier: identify the root cause together, agree the specific fix, and
   set a verification method (a re-inspection, a sample from the next run) before closing the loop.
4. Confirm the fix is actually verified: a supplier's claim that "it's fixed" does not close a CAPA; a checked,
   verified outcome does.

## Checks
- The trace names a specific batch or lot number, never just the SKU.
- The corrective action has a documented root cause, not just a fix.
- The loop only closes once verification confirms the fix, not on the supplier's word alone.

## Output
{batch_trace, root_cause, fix, verification_result}

## Example
3 complaints traced to batch #B-0447 (tech pack v4). Root cause: a die wear issue past its replacement interval.
Fix: die replaced, replacement schedule tightened. Verification: next batch's pre-shipment inspection showed zero
recurrence on the same measurement point.
