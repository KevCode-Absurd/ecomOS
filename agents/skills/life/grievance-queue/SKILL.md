---
name: grievance-queue
owner: LIFE
version: 1
invoke_when: a grievance or consumer notice is received, or the weekly statutory
  SLA check runs
inputs: the grievance inbox, the consumer-forum (e-Daakhil) and legal-notice
  tracker, India's E-Commerce Rules SLA (48-hour acknowledgement, 1-month
  resolution)
outputs: a logged grievance queue with SLA clocks, a weekly SLA compliance report
---
# Grievance officer queue and consumer notices

## Purpose
Runs the statutory grievance queue India's E-Commerce Rules require: every
grievance acknowledged in 48 hours and resolved in 1 month, with consumer-forum
and legal notices tracked on their own separate, stricter clock.

## Steps
1. Log every grievance the moment it arrives, starting the statutory clock from
   actual receipt.
2. Send the acknowledgement within 48 hours.
3. Investigate against the order/policy record and prepare the resolution inside
   the 1-month window.
4. Track any e-Daakhil consumer-forum case or legal notice on its own separate
   clock and status, never merged into the ordinary grievance SLA.
5. Run the weekly check across every open item, showing days remaining or days
   breached, in code.
6. Escalate anything nearing or past deadline to the founder immediately, not at
   the next weekly cycle.
7. Log the resolution and closure date against the statutory deadline.

## Checks
Both statutory windows tracked in code. Legal notices never merged into the
ordinary queue. Nothing nearing breach left unescalated.

## Output
A logged queue with SLA clocks, an acknowledgement record, resolution drafts, and
a weekly SLA compliance report.

## Example
"Grievance logged Tuesday 3pm. Acknowledged Thursday 1pm (within 48h). Resolution
due within 30 days; flagged for escalation at day 25 if still open."
