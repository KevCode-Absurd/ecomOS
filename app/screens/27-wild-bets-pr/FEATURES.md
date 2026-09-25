# Wild bets and PR: features

Status: todo | doing | done | parked. One feature per commit. The first round is the skeleton; after that, features come in rounds of 10, stack-ranked by revenue impact, usefulness and how easy they are to build on dummy data.

## Round 0: skeleton

| # | Feature | Status |
|---|---|---|
| 0.1 | Page shell in the shared UI kit: header, empty-state tiles, insight list, action buttons | todo |
| 0.2 | `api.py` serving this screen's metrics from `app/data/` with unavailable states | todo |
| 0.3 | 3 metric tiles, 2 insights, 1 chart from the sample brand | todo |

## Candidates from the room spec (pick 10 per round)

### Questions this screen should answer

- what unconventional moves are worth considering  (BRAND-C44)
- what is the downside, and when do we call it  (BRAND-C45)
- how do we actually run this at a size we can handle  (BRAND-C46)
- did this bet actually work  (REG-C02)
- who counts as 'us', and how do we run them day to day  (BRAND-C39, BRAND-C55)
- why would someone actually tell a friend about us  (LIFE-C45)
- who should we team up with, and who approached us that we should screen  (BRAND-C41, BRAND-C70)
- could this person or brand embarrass us later  (BRAND-C71)
- what is the story here that a journalist would actually run  (BRAND-C40)
- who exactly should get this pitch  (BRAND-C53)
- is a problem building that we need to get ahead of  (BRAND-C54)
- where should the founder show up, and what are we eligible to win  (BRAND-C60, BRAND-C61)
- what dates matter for PR, events and community this quarter  (LOOP-C05)
- where does our exact customer already gather, and can we show up there  (BRAND-C42)

### Metrics specified

- `active_bets_by_stage`: How many wild bets sit in each stage of the pipeline. count of bets grouped by stage (idea, bounded, executing, at read point, scaled, killed)
- `bet_bound_completeness`: How many of the 8 required bound fields are filled for a bet before launch. filled fields / 8
- `bet_read_point_lift`: How much better or worse the bet did than its control. treated group metric minus control group metric, on the bet's named metric
- `bet_cycle_time_days`: Days a bet has spent in its current stage. today minus stage entry date
- `pr_coverage_count`: Press placements landed. count of confirmed placements per period
- `media_list_coverage`: Verified contacts matched to the current story. count of contacts with a confirmed beat match for this pitch
- `partnership_pipeline_count`: Partnership candidates at each stage. count grouped by stage (sourced, screened, reputation-checked, approved)
- `partnership_reputation_flags`: Open reputation risk flags on a proposed partner. count of unresolved flags per candidate
- `ambassador_active_count`: Ambassadors currently active in the program. count of ambassadors with status active
- `ambassador_content_approval_rate`: Share of submitted ambassador content that passed the guidelines check. approved submissions / total submissions
- `referral_order_share`: Share of orders that came through a referral. orders with a referral code or link / total orders
- `event_attendance`: People who showed up at the last event or pop-up. count of confirmed attendees
- `award_submission_status`: Awards and best-of lists tracked, submitted or won. count grouped by status (eligible, submitted, won)
- `reputation_alert_count`: Open reputation risk alerts needing a response. count of unresolved alerts from the mention spike rule
- `holiday_calendar_readiness`: Upcoming moments in the next 60 days with a brief already prepared. moments with a brief / total moments in the next 60 days

### Insights specified (rules in code)

- bet is overdue at its stage: bet_cycle_time_days exceeds the bet's own planned duration for its current stage → "{bet} has sat in {stage} for {n} days, past its own plan." (action BRAND-C45)
- bet shows no lift at its read point: bet_read_point_lift is at or below zero against control at the bet's own read point date → "{bet} showed no real lift over the control group at its read point." (action REG-C02)
- bet shows a real lift: bet_read_point_lift is positive and above the bet's own pre-set bar at its read point → "{bet} beat its control by {n}. Worth sizing up." (action REG-C02)
- reputation risk building: mention or review volume in the reputation monitor rises more than 2x the trailing average with a negative tilt → "Mentions of the brand jumped {x}x this week with a negative tilt. A holding statement is drafted and waiting." (action BRAND-C54)
- media list going stale: a contact on the current media list has not been reachable or has changed beat since the list was built → "{n} contacts on the {story} list need a re-check before this pitch goes out." (action BRAND-C53)
- holiday moment coming up with no brief: a calendar moment falls within 30 days and has no linked brief → "{moment} is {n} days away with no brief started." (action LOOP-C05)
- partnership candidate flagged: a reputation check on a partnership candidate returns an open flag → "{candidate} has an open reputation flag: {reason}." (action BRAND-C71)
- ambassador content waiting too long: a submission has sat unreviewed longer than the program's own review SLA → "{n} ambassador submissions have waited past the review deadline." (action BRAND-C55)
- award deadline approaching, nothing started: an eligible award's submission deadline falls within 21 days and status is still 'eligible' → "The {award} deadline is {n} days away and nothing is submitted yet." (action BRAND-C61)

### Visuals specified

- bet pipeline board (kanban, one column per stage): every wild bet from idea to bounded to executing to read point to scaled or killed
- read point comparison chart (bar pair per bet): treatment versus control on the bet's own named metric
- PR coverage timeline (reverse-chronological timeline): placements landed, outlet, and reach where available
- US holiday and cultural calendar (calendar view, 90-day rolling window): upcoming dates with brief-ready status color coded
- partnership funnel (funnel chart): candidates sourced, screened, reputation-checked, approved
- reputation risk monitor (line chart with alert markers): mention or review volume over time with spikes marked

### Not in the usual tools

- the bet pipeline enforces an 8-field bound (budget cap, downside limit, control design, cohort, stop rule, read point, legal review, and the bound itself) before a bet can launch, and reads it against a real control in code
- the reputation monitor ties a mention or review spike directly to a drafted holding statement in the same room
- partnership sourcing and reputation screening run in one pipeline, checked against the brand's own non-competitive, same-customer rule
- the media list is built and verified per specific story or launch, matched to real beats
- the US holiday and cultural calendar is scoped to this brand's own category, PR needs, events and community moments, not a generic marketing holiday calendar
- the ambassador program room runs screening, task assignment, content approval and tracking end to end for this brand's own program

### Data this screen needs

- `wild_bets`: brand, bet_id, stage, budget_cap, downside_limit, control_design, cohort, stop_rule, read_point_date, legal_review_status (BRAND-C44, BRAND-C45, BRAND-C46, BRAND-C47)
- `bet_read_points`: bet_id, treatment_value, control_value, lift, decision (scale, kill, retest) (BRAND-C47)
- `pr_coverage`: brand, outlet, story, date, url, reach_estimate (media monitoring feed, BRAND-C40)
- `media_list`: brand, story_id, journalist, outlet, beat, verified_date, contact_status (BRAND-C53)
- `partnership_pipeline`: brand, candidate_name, stage, category_overlap_flag, reputation_flag, notes (BRAND-C41, BRAND-C70, BRAND-C71)
- `ambassador_program`: brand, ambassador_id, status, assigned_task, submission_status, last_activity (BRAND-C55)
- `events_and_popups`: brand, event_id, location, date, attendee_count, cost (BRAND-C42)
- `award_tracking`: brand, award_name, deadline, status, eligibility_note (BRAND-C61)
- `holiday_calendar`: brand, moment_name, date, category_relevance, brief_linked_flag, market (US default; India festival dates optional, markets: IN) (BRAND-C65)
- `reputation_monitor_feed`: brand, mention_volume, sentiment_tilt, date, spike_flag (mention listening feed, BRAND-C54 (shared with brand health))

## Rounds

| Round | Features picked | Date | Notes |
|---|---|---|---|
