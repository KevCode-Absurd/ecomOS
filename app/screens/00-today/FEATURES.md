# Today: features

Status: todo | doing | done | parked. One feature per commit. The first round is the skeleton; after that, features come in rounds of 10, stack-ranked by revenue impact, usefulness and how easy they are to build on dummy data.

## Round 0: skeleton

| # | Feature | Status |
|---|---|---|
| 0.1 | Page shell in the shared UI kit: header, empty-state tiles, insight list, action buttons | todo |
| 0.2 | `api.py` serving this screen's metrics from `app/data/` with unavailable states | todo |
| 0.3 | 3 metric tiles, 2 insights, 1 chart from the sample brand | todo |

## Candidates from the room spec (pick 10 per round)

### Questions this screen should answer

- where is the business actually broken right now  (DIAG-C01, ORCH-C01)
- what is this worth in dollars this week  (DIAG-C01)
- what should I approve, send out, or park  (PROP-C06, ORCH-C03)
- are we actually growing or just booking orders that will be returned or disputed  (LOOP-C23)
- did anything blow past a limit today  (LOOP-C40)
- what needs my decision right now  (ORCH-C02, REG-C08)
- will this new test mess up a read I am already waiting on  (LOOP-C35)
- which client fire do I put out first today  (LOOP-C21)
- what do I need to know walking into this call today  (LOOP-C17)
- can I just reply to decide  (LOOP-C42, LOOP-C42)
- what is due before the next festival or sale window  (LOOP-C05)
- does this one review or one stock issue need my eyes now  (LOOP-C06)
- did we actually cause this, or did something else  (LOOP-C02)
- what can't the system see right now  (DIAG-C02)

### Metrics specified

- `pipeline_stage_table`: Each stage of the funnel (reach, sessions, page loads, product views, add to cart, checkout, orders, AOV, repeat, margin, cash) with today's value, your own trailing median, and stores-like-you's band. current window value; trailing median of 4 prior windows; peer band from benchmarks filtered by store tags
- `money_at_stake_top_break`: What the top broken stage is costing this week, in dollars. (peer or own-trailing value - current value) x volume at the stage x downstream conversion to revenue
- `goal_gap`: How far the current window sits from the founder's stated period goal, by stage. goal value - current value, per stage
- `gross_vs_net_orders`: Orders and revenue you actually keep, after expected returns and chargebacks, next to the gross number. net = gross - (gross x expected return rate) - (gross x expected chargeback rate for the window); COD and prepaid split first
- `same_day_threshold_crossings`: Count of pre-agreed hard triggers crossed today. count of live metric readings today where value crosses its stored threshold
- `pending_decisions_count`: How many cards are waiting for a decision right now. count of registry entries with status = card_shown, not yet decided
- `reads_due_count`: How many running experiments hit their read point this week. count of registry entries where read_point falls within the current week
- `trend_alert_count`: Stages that have moved the same direction for 2 windows running. count of stages where delta sign matches for 2 consecutive trailing windows
- `unreadable_stage_count`: Stages the system cannot honestly call healthy or broken today. count of stages flagged unreadable by Diagnose
- `overlap_flag_count`: Running experiments that share an audience or metric window with another running experiment. pairwise check of registry running entries for audience or window overlap
- `cross_brand_rank`: Where this brand's top item ranks against every other brand the agency runs, today. sort of each brand's top queue item by money at stake and time sensitivity on one scale
- `brand_quiet_days`: Days since the founder last made a decision on this brand. today - date of last decision log entry
- `chargeback_rate`: Share of paid orders reversed through a card dispute in the window. chargebacks opened / paid orders in window
- `seasonal_deadline_countdown`: Days left before the nearest festival or sale window's prep deadline. deadline date - today, per specialist prep item tied to the nearest calendar window

### Insights specified (rules in code)

- top break named: highest-stake stage from Diagnose, ranked by stake then confidence then upstream position → "{stage} is costing about {amount} this {window}, since {date}" (action PROP-C06)
- trend alert: a stage's delta sign matches for 2 consecutive trailing windows → "{stage} has moved {direction} for 2 windows running" (action DIAG-C03)
- Reversals widening: the gap between gross and net orders widens for 2 or more windows running → "Gross orders look flat but net orders after returns and chargebacks have fallen {pct} over 2 windows" (action LOOP-C23)
- same-day trigger crossed: a live metric value crosses its stored hard threshold mid-day → "{metric} crossed its {threshold} trigger at {time} today" (action LOOP-C40)
- experiment overlap: two running registry entries share an audience or metric window → "{idea_a} and {idea_b} share the same audience; the newer one is staggered" (action LOOP-C35)
- brand gone quiet: brand_quiet_days exceeds 7 for a brand with an active queue → "{brand} has had no founder decision in {n} days while {m} cards wait" (action LOOP-C21)
- unreadable stage: a stage has no full day of data or a failed connector → "{stage} cannot be called healthy or broken: {source} has not reported since {date}" (action DIAG-C02)
- external cause check: a metric move coincides with a dated external event (platform change, gateway outage, courier strike, festival date shift) → "{stage} moved {pct}, but {event} on {date} may explain part of it" (action LOOP-C02)
- reads due this week: registry entries whose read_point falls in the current week → "{n} experiments hit their read point this week" (action REG-C02)
- seasonal prep at risk: a specialist's pre-window prep item has fewer days left than its own stated lead time → "{item} is due in {n} days for {window} and is not yet marked ready" (action LOOP-C05)
- single-item escalation: an incoming escalation is below the crisis threshold but above the normal queue bar → "{item} needs a look today; it is not a crisis but it is not routine either" (action LOOP-C06)
- chargebacks rising: chargeback_rate rises 2+ windows running or crosses 0.9 percent → "Chargebacks reached {rate} percent of paid orders, up {delta} in {n} windows; representment and the reason codes are in the Money room" (action LOOP-C31)

### Visuals specified

- stage waterfall (waterfall / funnel chart): each pipeline stage with the break marked and the money at stake labelled
- stake bar (horizontal bar chart): money at stake per stage, ranked
- top 10 card stack (card list with inline buttons): the top 10 proposal cards with why-now, effect, effort, risk and 3 buttons each
- trend sparkline row (small multiples of sparklines): each stage's last 5 windows, flagging the 2-window-running movers
- cross-brand rank list (ranked list, agency view only): every brand's top item on one scale of stake and urgency, brand-tagged
- same-day alert ticker (compact alert strip): triggers crossed today with time and metric

### Not in the usual tools

- money-at-stake per stage, computed in code from your own trailing history and a peer band, before any fix is proposed
- gross orders shown net of expected returns and chargebacks and split by payment method before naming a bottleneck
- one ranked list across every brand an agency runs, by stake and urgency on the same scale
- same-day alert on a pre-agreed hard trigger, separate from full crisis mode and from tomorrow's batch ranking
- approve, reject or park a specific card by a single SMS or Slack reply, matched back to its card id
- a test flagged before it starts if it shares an audience or metric window with one already running

### Data this screen needs

- `metric_contract`: brand, stage, window, value, freshness, unavailable_flag (brain.compute_contract)
- `contract_deltas`: brand, stage, current, trailing_median, peer_band_low, peer_band_high, delta, stake_inr, confidence (contract.compute_deltas)
- `registry_entries`: id, brand, idea_id, status, owner, metric, read_point, audience, window, kill_rule (registrar)
- `orders`: brand, order_id, payment_method, cod_confirmed, rto_flag, date, value (order connector)
- `same_day_triggers`: brand, metric, threshold, direction, owner (founder-set config)
- `decision_log`: brand, date, card_id, decision, reason, person (registrar)
- `messaging_channel`: brand, date, channel, sends, delivered, replies, opt_outs, conversions, consent_status (SMS platform API; WhatsApp Business API for brands that use it (markets IN))
- `brand_calendar`: brand, window_name, window_date, prep_item, owner_specialist, deadline, ready_flag (loop.seasonal_calendar)
- `cross_brand_queue`: brand, top_item_id, stake_inr, urgency, last_decision_date (orchestrator.queue_build)

## Rounds

| Round | Features picked | Date | Notes |
|---|---|---|---|
