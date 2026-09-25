# Team and ops: features

Status: todo | doing | done | parked. One feature per commit. The first round is the skeleton; after that, features come in rounds of 10, stack-ranked by revenue impact, usefulness and how easy they are to build on dummy data.

## Round 0: skeleton

| # | Feature | Status |
|---|---|---|
| 0.1 | Page shell in the shared UI kit: header, empty-state tiles, insight list, action buttons | todo |
| 0.2 | `api.py` serving this screen's metrics from `app/data/` with unavailable states | todo |
| 0.3 | 3 metric tiles, 2 insights, 1 chart from the sample brand | todo |

## Candidates from the room spec (pick 10 per round)

### Questions this screen should answer

- what are customers actually telling us, and does anyone act on it  (LIFE-C29)
- do we need to hire, and are we hiring the right way  (MONEY-C31, MONEY-C32)
- could a new hire do this job from what is written down  (MONEY-C33)
- are we having the right meetings, and is the team actually functioning  (MONEY-C34, MONEY-C35)
- is this vendor doing what we pay them for  (MONEY-C36)
- is this production run on track, on spec and on one owner's desk  (MONEY-C37)
- do we have enough CS coverage for what is coming, and is it costing more than it should  (MONEY-C38)
- are we paying for software we have outgrown or do not need yet  (MONEY-C39)
- who owns this kind of decision, and was it logged with a metric and a review date  (LOOP-C10)
- is this contractor scoped, paid and offboarded properly  (MONEY-C66)
- are our contracts, handbook and exits all clean and signed  (MONEY-C67, MONEY-C68, MONEY-C69)
- is our warehouse hitting pick, pack and damage targets today  (MONEY-C70)
- are agents using current answers, and how good are their replies  (LIFE-C27)
- which tool renews soon, and should we renegotiate or cancel  (MONEY-C78)

### Metrics specified

- `sop_coverage_rate`: Share of core roles with a current, written SOP. roles with an SOP reviewed in the last 6 months ÷ total core roles
- `time_to_fill`: Days between a hiring trigger firing and an offer accepted. offer_accepted_date − trigger_crossed_date, per role
- `decision_log_completeness`: Share of high-stakes decisions logged with an owner and a review date. decisions logged with owner + metric + review date ÷ decisions the framework says should be logged
- `vendor_sla_hit_rate`: Share of a vendor's SLA terms actually met. SLA metrics hit ÷ SLA metrics measured, per vendor, per period
- `invoice_sla_match_rate`: Share of vendor invoices that match the agreed SLA and rate card. invoices matching contracted rate and SLA ÷ total invoices audited
- `cs_cost_per_ticket`: What one support ticket costs on average. total CS cost in period ÷ tickets resolved in period
- `cs_resolution_time`: Median time to resolve a ticket. median(resolved_at − opened_at), by complexity tier
- `tooling_spend_pct_revenue`: Software spend as a share of revenue. total tooling spend in period ÷ net revenue in period
- `meeting_cadence_adherence`: Share of scheduled trading reviews and check-ins that actually happened. meetings held ÷ meetings scheduled, by type
- `freelancer_completion_rate`: Share of contractor engagements with scope, IP assignment and on-time invoicing all in place. engagements with all 3 items checked ÷ total active engagements
- `contract_redline_turnaround`: Days to get an incoming contract redlined and returned. returned_date − received_date, per contract
- `offboarding_completion_rate`: Share of exits with same-day access revocation and a completed checklist. exits with access revoked same day and checklist complete ÷ total exits
- `saas_renewal_coverage`: Share of upcoming SaaS renewals with a usage review done before the window closes. renewals with a usage review logged before auto-renew date ÷ renewals due in the next 60 days
- `handbook_acknowledgment_rate`: Share of staff who have signed the current handbook version. staff with a signed acknowledgment of the current version ÷ total staff

### Insights specified (rules in code)

- SOP gap: a core role in the silo map has no SOP entry, or its SOP is over 6 months old → "{role} has no current written SOP" (action MONEY-C33)
- hiring trigger crossed: a silo's hiring trigger metric has been past its threshold for over 4 weeks with no open requisition → "{silo} crossed its hiring trigger {n} weeks ago with no req open" (action MONEY-C31)
- vendor SLA breach: vendor_sla_hit_rate for a vendor falls below 90% in the period → "{vendor} missed its {sla_metric} SLA {n} times this month" (action MONEY-C36)
- decision log gap: no new entry was added to the decision log in the same period the weekly review meeting was held → "no decision was logged in {n} weeks despite the weekly review happening" (action LOOP-C10)
- CS cost drift: cs_cost_per_ticket this period exceeds the trailing 90-day average by more than 15% → "cost per ticket rose {pct} versus the last quarter" (action MONEY-C38)
- tooling misfit: tooling_spend_pct_revenue exceeds the brand's own stage benchmark by more than 25% relative → "{tool} costs {pct} of revenue, above what the brand's stage plan allows" (action MONEY-C39)
- offboarding gap: offboarding_completion_rate shows an exited employee with access still active past the same day → "{n} accounts stayed active after {employee} left" (action MONEY-C69)
- SaaS renewal window closing: a contract's auto-renew date is within 30 days and saas_renewal_coverage shows no usage review logged → "{tool} renews in {n} days and nobody has reviewed its usage yet" (action MONEY-C78)

### Visuals specified

- SOP coverage grid (grid, role by status): every core role and whether its SOP is current, aging or missing
- vendor SLA scorecard (table with colored bars per vendor): each vendor's SLA metrics hit vs missed this period
- meeting cadence strip (calendar heat strip): which scheduled meetings actually happened over the last quarter
- hiring trigger timeline (line chart with a threshold band): the trigger metric for each silo against its threshold, with the crossing date marked
- CS cost and time trend (dual line chart): cost per ticket and resolution time over time, by complexity tier
- decision log timeline (timeline of logged decisions): every logged high-stakes decision with its owner, metric and review date

### Not in the usual tools

- SOP coverage tracked against the brand's own role list, with age and gaps flagged automatically
- vendor and 3PL SLA performance scored against the actual written SLA and cross-checked to invoices, in one room
- a hiring trigger shown as a number crossed on a date, next to the org chart
- SaaS renewal renegotiation drafted with the brand's own usage numbers before the auto-renew window closes
- CS cost per ticket and resolution time tied to a complexity definition set before routing, not after

### Data this screen needs

- `sop_register`: role, sop_title, owner, last_reviewed (manual document register)
- `hiring_triggers`: silo, metric, threshold, current_value, crossed_at (manual log against finance data)
- `vendor_sla`: vendor, sla_metric, target, actual, period (vendor invoices + 3PL/agency reports)
- `decision_log`: decision_id, type, owner, date, metric, review_date (manual decision log)
- `cs_tickets`: ticket_id, channel, opened_at, resolved_at, cost, complexity (Gorgias/Zendesk export)
- `tooling_spend`: tool, monthly_cost, revenue_stage_benchmark, owner (card/expense feed)
- `meeting_log`: meeting_type, scheduled_at, held, notes_url (calendar export + manual log)
- `freelancer_contracts`: contractor, scope, rate, milestone, invoice_status (manual contract tracker)
- `hr_records`: employee_id, contract_signed, handbook_ack, exit_date, offboard_checklist_done (HR system export)
- `saas_contracts`: tool, renewal_date, usage_last_90d, cost, auto_renew (billing exports)

## Rounds

| Round | Features picked | Date | Notes |
|---|---|---|---|
