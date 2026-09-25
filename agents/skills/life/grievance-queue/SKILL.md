---
name: grievance-queue
owner: LIFE
version: 1
invoke_when: a complaint or consumer notice is received, or the weekly SLA
  check runs
inputs: the complaint inbox (BBB, state consumer-complaint portal, FTC referral
  for the US; the grievance inbox for India), the consumer-forum (e-Daakhil,
  India) and legal-notice tracker, India's E-Commerce Rules SLA (48-hour
  acknowledgement, 1-month resolution)
outputs: a logged complaint queue with SLA clocks, a weekly SLA compliance report
---
# Consumer-complaint and compliance notice queue

## Purpose
Runs the consumer-complaint and regulatory-notice queue: BBB complaints, state
consumer-complaint portal cases and FTC referrals by default, each on that
channel's own SLA; India only, the statutory grievance queue India's E-Commerce
Rules require instead, every grievance acknowledged in 48 hours and resolved in
1 month. Consumer-forum and legal notices are tracked on their own separate,
stricter clock in both cases.

## Steps
1. Log every complaint the moment it arrives, starting its clock from actual
   receipt.
2. Send the acknowledgement inside the receiving channel's SLA (about 2 weeks for
   BBB/state portals; within 48 hours for India's statutory rule).
3. Investigate against the order/policy record and prepare the resolution inside
   the channel's own window (1-month statutory window for India).
4. Track any BBB case, state consumer-complaint case or legal notice (an
   e-Daakhil consumer-forum case for India) on its own separate clock and status,
   never merged into the ordinary complaint SLA.
5. Run the weekly check across every open item, showing days remaining or days
   breached, in code.
6. Escalate anything nearing or past deadline to the founder immediately, not at
   the next weekly cycle.
7. Log the resolution and closure date against the applicable deadline.

## Checks
Both India statutory windows tracked in code where they apply; BBB/state SLA
tracked in code for the US. Legal notices never merged into the ordinary queue.
Nothing nearing breach left unescalated.

## Output
A logged queue with SLA clocks, an acknowledgement record, resolution drafts, and
a weekly SLA compliance report.

## Example
"Complaint logged Tuesday 3pm. Acknowledged Thursday 1pm. India: within the
48-hour statutory window; resolution due within 30 days, flagged for escalation
at day 25 if still open. US: within the BBB/state portal's own target window."
