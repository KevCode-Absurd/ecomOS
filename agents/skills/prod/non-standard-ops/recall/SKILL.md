---
name: prod/non-standard-ops/recall
owner: PROD
version: 1
invoke_when: the classified non-standard-ops type is a safety-related recall
select_by: {type: recall}
inputs: the defect or regulator notice, affected batch data, customer purchase records
outputs: affected-batch list, sale-stopped confirmation across channels, customer contact log, regulator notice log
---
# Product recall and safety incident procedure

## Purpose
A safety-related defect is the single highest-stakes event this agent can face. This procedure exists to make sure
speed and completeness happen together: sale stops everywhere immediately, every affected buyer is found and
contacted, and every regulator notice is logged, with the founder in the loop from the first step.

## Steps
1. Find every affected batch using the tech pack's own versioning and any production batch codes.
2. Stop sale on every channel: site, every marketplace, quick commerce: immediately, before any other step in
   this procedure proceeds.
3. Contact every buyer who purchased an affected batch, using purchase records, and arrange a return or
   replacement.
4. Log every regulator notice received or filed in connection with the incident.

## Checks
- Sale is stopped on every channel before any other action, with no exception.
- This entire procedure only runs with the founder gate engaged from the first step; nothing here proceeds on
  agent judgment alone.

## Output
{affected_batches[], sale_stopped_channels[], customer_contact_log[], regulator_notices[]}

## Example
A safety notice on a battery-included accessory triggers this procedure. Batches #B-201 through #B-204 identified.
Sale stopped on site, Amazon and 2 quick commerce platforms within the same hour. 340 affected buyers found and
contacted with replacement offers. One regulator notice logged and filed as required.
