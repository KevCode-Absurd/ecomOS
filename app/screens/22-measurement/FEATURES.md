# Measurement and data health: features

Status: todo | doing | done | parked. One feature per commit. The first round is the skeleton; after that, features come in rounds of 10, stack-ranked by revenue impact, usefulness and how easy they are to build on dummy data.

## Round 0: skeleton

| # | Feature | Status |
|---|---|---|
| 0.1 | Page shell in the shared UI kit: header, empty-state tiles, insight list, action buttons | todo |
| 0.2 | `api.py` serving this screen's metrics from `app/data/` with unavailable states | todo |
| 0.3 | 3 metric tiles, 2 insights, 1 chart from the sample brand | todo |

## Candidates from the room spec (pick 10 per round)

### Questions this screen should answer

- is GA4 actually tracking revenue and events correctly  (MONEY-C20)
- is Meta double-counting, under-matching or missing events  (MONEY-C21)
- which of our channels look bigger or smaller than they are because of bad links  (MONEY-C22)
- which number is right when platforms disagree, and did this channel actually add sales  (MONEY-C23)
- do all our systems agree on how many orders we actually got  (MONEY-C24)
- what does this number actually mean, and who owns it  (BRN-C06)
- can I trust yesterday's numbers before I act on them  (BRN-C02)
- where in the funnel are we actually losing people, compared to our own history  (DIAG-C01)
- why did this number move, before anyone reacts to it  (DIAG-C01)
- are the numbers on our dashboards still the ones we trust  (MONEY-C30)
- what is our real return on X, computed from one warehouse instead of five exports  (BRN-C02, ORCH-C04)
- how much does each channel, including untracked ones, actually add to revenue  (MONEY-C63)
- which customers are we winning, keeping or losing right now  (LIFE-C12)
- is our tagging layer itself clean, consented and firing once per event  (MONEY-C65)

### Metrics specified

- `ga4_audit_score`: How many GA4 setup checks pass. checks passed ÷ total checks run (property structure, timezone, retention, consent, key events, ecommerce parameters)
- `capi_match_quality`: How well Meta can match a purchase event to a real person. event match quality score as reported by Meta events manager, per event type
- `event_dedup_rate`: Share of events counted twice, once from the browser and once from the server. duplicate event_id matches ÷ total events sent, browser plus CAPI
- `utm_compliance_rate`: Share of paid clicks that arrive with a valid, convention-following UTM. sessions with a valid utm_source/medium/campaign per the brand's convention ÷ total paid sessions
- `fake_direct_share`: Share of sessions wrongly counted as direct or organic. sessions matching a known paid-link pattern but landing with no UTM ÷ total direct+organic sessions
- `attribution_model_gap`: How far last-click and data-driven attribution disagree, by channel. |last-click attributed revenue − data-driven attributed revenue| ÷ data-driven attributed revenue, per channel
- `incrementality_lift`: How much of a channel's reported sales actually happened because of it. holdout or geo-lift test result: (test group revenue − control group revenue) ÷ control group revenue
- `order_count_variance`: How far GA4, Meta, Shopify and marketplaces disagree on order count. |platform order count − Shopify order count| ÷ Shopify order count, per platform, per day
- `bot_traffic_share`: Share of sessions that look like bots, not buyers. sessions flagged by bot-score threshold ÷ total sessions
- `daily_trust_score`: A pass, warn or fail grade for yesterday's data before anyone reads it. rule-based score across freshness, reconciliation variance and known-bad patterns for every connected source
- `funnel_step_conversion`: Percent of visitors who move to the next funnel step. sessions reaching a step ÷ sessions reaching the step before it, for session→PDP→cart→checkout→purchase
- `metric_definition_drift`: How many numbers have more than one definition in active use. count of metric names with 2 or more distinct stored formulas in the metric contract
- `source_freshness_lag`: How many hours since a connected source last synced. current time − last_sync_at, per source
- `rfm_segment_migration`: How many customers moved segment this period. count of customer_id whose RFM segment label changed between this period and last
- `mmm_vs_platform_gap`: How far the modeled channel contribution differs from what the platform claims. |modeled_contribution − platform_reported| ÷ platform_reported, per channel
- `tag_duplicate_fire_rate`: Share of page loads where a tag fires more than once. duplicate tag fires ÷ total tag fires, per container

### Insights specified (rules in code)

- GA4 tracking gap: ga4_audit_score has one or more failed critical checks → "{n} GA4 checks failed, including {top_issue}" (action MONEY-C20)
- pixel match quality low: capi_match_quality for an event type falls below Meta's own good-quality band → "Meta match quality for {event} is {score}, below Meta's own good-quality band" (action MONEY-C21)
- UTM leakage: utm_compliance_rate for an active paid campaign falls below 90% → "{pct}% of clicks on {campaign} show up with no valid UTM" (action MONEY-C22)
- attribution gap widening: attribution_model_gap for a channel grew versus the prior period → "{channel}'s last-click and data-driven numbers now differ by {pct}, up from {prior_pct}" (action MONEY-C23)
- bot-driven spend spike: a day's spend or ROAS moved more than 50% versus the 14-day median and bot_traffic_share also moved above its own baseline that day → "{date} had a {pct} spend spike alongside bot traffic {pct2} above normal" (action MONEY-C24)
- order count mismatch: order_count_variance for a platform exceeds 3% for 2 consecutive days → "{platform} shows {n} more orders than Shopify for {period}" (action MONEY-C24)
- metric definition drift: metric_definition_drift is above zero for a metric name in active use → "{metric} is defined two ways in active use: {def1} and {def2}" (action BRN-C06)
- trust check failed: daily_trust_score is warn or fail → "yesterday's data quality check came back {status}: {reason}" (action BRN-C02)
- funnel step decay: a funnel_step_conversion rate fell more than 15% relative to its own trailing 90-day average → "{step} conversion fell {pct} versus your own 90-day average" (action DIAG-C01)
- RFM migration alert: rfm_segment_migration shows a Loyal-to-At-Risk move above the brand's own trailing average count → "{n} customers moved from Loyal to At Risk this month" (action LIFE-C12)
- source gone stale: source_freshness_lag exceeds the source's own stated cadence → "{source} has not refreshed in {hours} hours" (action BRN-C02)

### Visuals specified

- audit scorecard (traffic-light grid): GA4, Meta CAPI and tag-management checks, pass/warn/fail per check
- attribution comparison (grouped bar chart per channel): last-click, data-driven and platform-reported revenue side by side
- funnel with baseline band (step/funnel chart with a shaded baseline range): each funnel step's conversion against its own trailing 90-day band
- data freshness heatmap (heatmap, source by day): how stale each connected source is right now
- RFM segment migration (flow diagram between segment boxes): how many customers moved between RFM segments this period
- daily trust strip (row of pass/warn/fail dots over time): the daily trust score for the last 30 days

### Not in the usual tools

- GA4 config and event audit built into the same room as everything else that reads the brand's numbers
- attribution models reconciled against each other and against a metric contract with one owner and freshness stamp per number
- a daily pass/warn/fail trust score computed before anyone reads yesterday's numbers
- GA4/Meta/Shopify/marketplace order counts reconciled and bot spikes flagged in the same view as spend and attribution
- one metric contract with a single formula, owner and freshness stamp per number, surfaced everywhere that number appears

### Data this screen needs

- `ga4_config_audit`: property_id, check_name, pass_fail, detail, checked_at (GA4 Admin API audit script)
- `pixel_capi_events`: event_name, source, event_id, dedup_key, match_quality, timestamp (Meta MCP (read-only) + server event log)
- `utm_audit`: url, campaign, utm_source, utm_medium, utm_campaign, valid, checked_at (link crawl script against the UTM convention doc)
- `sessions_ga4`: date, channel, sessions, source_medium (GA4 Data API)
- `order_counts`: date, platform, order_count (GA4 + Meta MCP + Shopify + marketplace exports)
- `attribution_models`: channel, model, revenue, period (GA4 + Meta + platform exports)
- `holdout_tests`: test_id, channel, geo, start, end, lift_pct, confidence (manual test log)
- `metric_contract`: metric_name, formula, source, owner, last_updated (internal document or database)
- `data_freshness_log`: source, last_sync_at, expected_cadence (pipeline monitor)
- `rfm_scores`: customer_id, recency, frequency, monetary, segment, period (warehouse query)
- `mmm_outputs`: channel, period, modeled_contribution, platform_reported (marketing mix model script)
- `tag_manager_log`: container_id, tag_name, fire_count, duplicate_flag, date (tag manager or server-side container debug log)

## Rounds

| Round | Features picked | Date | Notes |
|---|---|---|---|
