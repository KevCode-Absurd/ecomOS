# Reviews and reports: features

Status: todo | doing | done | parked. One feature per commit. The first round is the skeleton; after that, features come in rounds of 10, stack-ranked by revenue impact, usefulness and how easy they are to build on dummy data.

## Round 0: skeleton

| # | Feature | Status |
|---|---|---|
| 0.1 | Page shell in the shared UI kit: header, empty-state tiles, insight list, action buttons | todo |
| 0.2 | `api.py` serving this screen's metrics from `app/data/` with unavailable states | todo |
| 0.3 | 3 metric tiles, 2 insights, 1 chart from the sample brand | todo |

## Candidates from the room spec (pick 10 per round)

### Questions this screen should answer

- what happened this week and what needs my call  (LOOP-C01, LOOP-C01)
- are we actually going to hit what I said mattered this quarter  (LOOP-C07)
- what do I show this client this month  (ORCH-C07)
- across every client, where is the agency's time actually going, and is that right  (LOOP-C21)
- does this agency's report match what we actually measure  (LOOP-C41)
- did we actually get what this invoice is charging for  (LOOP-C26)
- what do I tell my board or investors this quarter  (LOOP-C11)
- are we having the right meetings, not too many or too few  (LOOP-C20)
- is anyone about to drop something because they have too much on  (LOOP-C21)
- where should the next dollar of budget go, across channels  (LOOP-C03)

### Metrics specified

- `weekly_headline_metric`: The one number that moved most this week and by how much. largest absolute percent change among headline contract fields, week over week
- `shipped_vs_blocked_count`: How many approved items shipped this week versus how many are blocked. count of registry entries moved to status=running or done this week; count stuck with a blocker note
- `okr_progress_pct`: Progress toward each key result this quarter. current value of the tied metric contract field / target value
- `monthly_client_metrics`: The core metrics a client report shows: spend, ROAS, orders, revenue, by brand. period totals and rates from the metric contract
- `portfolio_capacity`: Queue depth per agency person against their available hours, across every brand they work on. sum of estimated hours for open queue items per person / stated available hours
- `invoice_match_rate`: Share of invoice lines matched to a delivered artefact in the registry. matched lines / total invoice lines
- `sow_cadence_adherence_pct`: How closely an agency or freelancer's actual delivery cadence matches their stated scope-of-work commitment. delivered items in period / committed cadence in the SOW
- `agency_report_discrepancy_count`: How many numbers in an agency or platform's own report do not match the metric contract. count of headline figures in the report differing from the matching contract field beyond a rounding tolerance
- `operating_cadence_load`: How many standing recurring reviews the founder is expected to sit through. count of active standing reviews on the cadence calendar
- `board_update_readiness`: Whether this quarter has enough recorded wins, misses and numbers to draft a board update. count of registry results plus contract headline fields available for the quarter
- `channel_headroom`: Estimated room left in each channel before returns drop, feeding next month's budget split. per-channel headroom estimate from each specialist, marginal return curve

### Insights specified (rules in code)

- one number that moved most: largest absolute percent change among headline fields this week → "{field} moved {pct} this week, mostly from {cause}" (action LOOP-C01)
- metric out of band 2+ weeks: a metric sits outside its normal band for 2 consecutive weeks → "{field} has been outside its normal range for 2 weeks running" (action LOOP-C01)
- OKR off track: okr_progress_pct is behind the pace needed to hit the target by quarter end → "{key_result} is at {pct} with {weeks} weeks left; on pace to miss" (action LOOP-C07)
- SOW under-delivery pattern: sow_cadence_adherence_pct falls short for 2 or more periods running → "{vendor} has delivered under its committed cadence for {n} periods running" (action LOOP-C26)
- invoice line unmatched: an invoice line has no matching delivered artefact in the registry → "{invoice_line} on {vendor}'s invoice has no matching delivered work on file" (action LOOP-C26)
- agency report window mismatch: an agency report's stated date range differs from the contract's matching window → "{vendor}'s report uses {their_window} while our contract measures {our_window}; the numbers are not directly comparable" (action LOOP-C41)
- agency metric not in our vocabulary: a reported metric has no matching field in the metric contract → "{vendor} reports '{their_metric}', which likely stands in for {our_field}" (action LOOP-C41)
- person over capacity: portfolio_capacity exceeds 100% for a person this week → "{person} is booked at {pct} of available hours across {n} brands this week" (action LOOP-C21)
- cadence overload: operating_cadence_load exceeds what a solo founder can sit through → "The standing review calendar now has {n} recurring meetings; consider retiring one" (action LOOP-C20)
- channel drifted from agreed split: a channel's actual spend share has moved from the last agreed allocation beyond a set tolerance → "{channel} spend has drifted to {pct} of budget versus the {agreed_pct} last agreed" (action LOOP-C03)

### Visuals specified

- weekly one-pager (single-page summary card): headline number, what shipped, what is blocked, decisions needed this week
- OKR progress bars (horizontal progress bars): each key result against its target, pace-adjusted
- monthly client report cards (metric cards per brand): spend, ROAS, orders, revenue for the reporting month, per brand
- portfolio capacity heatmap (heatmap grid): each agency person (rows) against each brand (columns), shaded by hours booked
- invoice reconciliation table (table with match status): each invoice line, its matching registry artefact if any, and a flag if unmatched
- operating cadence calendar (weekly calendar grid): each standing recurring review, when it happens, who attends, what it covers

### Not in the usual tools

- a weekly review that names the one number that moved most and why, tied to the registry's reads due and the decision log, not a static KPI list
- a portfolio capacity heatmap showing hours booked per agency person across every brand they touch
- an agency or platform's own report reconciled line by line against the brand's own source-of-truth metric contract, with window mismatches and vanity metrics named
- scope-of-work cadence tracked over multiple periods, not just whether one invoice matches one deliverable
- a standing meeting cadence that is itself reviewed for overload as the specialist set grows, rather than fixed once and left alone

### Data this screen needs

- `metric_contract`: brand, field, window, value, freshness (brain.compute_contract)
- `registry_entries`: brand, id, status, read_point, result, blocker_note (registrar)
- `okr_records`: brand, objective, key_result, tied_metric_field, target, quarter (LOOP-C07)
- `person_hours`: person, brand, role, available_hours, booked_hours_estimate (orchestrator.queue_build)
- `vendor_invoices`: brand, vendor, invoice_line, amount, period, matched_artefact_id (LOOP-C26)
- `sow_terms`: brand, vendor, committed_cadence, scope_description (document reader)
- `agency_reports`: brand, vendor, reported_window, reported_metric, reported_value, contract_field, contract_value (LOOP-C41)
- `operating_cadence`: brand, meeting_name, frequency, attendees, agenda_template (LOOP-C20)
- `channel_headroom`: brand, channel, current_spend, headroom_estimate, agreed_split_pct, actual_split_pct (MEDIA/ORG/LIFE headroom estimates)

## Rounds

| Round | Features picked | Date | Notes |
|---|---|---|---|
