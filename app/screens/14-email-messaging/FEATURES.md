# Email and messaging: features

Status: todo | doing | done | parked. One feature per commit. The first round is the skeleton; after that, features come in rounds of 10, stack-ranked by revenue impact, usefulness and how easy they are to build on dummy data.

## Round 0: skeleton

| # | Feature | Status |
|---|---|---|
| 0.1 | Page shell in the shared UI kit: header, empty-state tiles, insight list, action buttons | done |
| 0.2 | `api.py` serving this screen's metrics from `app/data/` with unavailable states | done |
| 0.3 | 3 metric tiles, 2 insights, 1 chart from the sample brand | done |
| 0.4 | `audit.py`: 15 rules (EMAIL-R01 to R15) in the contract shape, 5 computable, 10 unavailable with the connector that fills them | done |

## JTBD table (room jobs, capabilities and the audit rules that answer them)

| Job | Question | Capability | Rules | On Bombas today |
|---|---|---|---|---|
| design and test the sign-up pop-up | is my pop-up earning its keep | LIFE-C02 | none yet | no pop-up log |
| keep consent and quiet hours correct | am I allowed to send this now | LIFE-C03 | EMAIL-R02, EMAIL-R07 | unavailable: no per-contact send log or consent log |
| turn new subscribers into first buyers | is the welcome flow converting in 72 hours | LIFE-C04 | EMAIL-R10 | runs, needs 3 or more welcome messages; quiet |
| win back browsers and cart abandoners | how much am I recovering, does the discount fire early | LIFE-C05, LIFE-C06 | EMAIL-R06 | unavailable: no flow_defs |
| turn order 1 into order 2 | is post-purchase content working | LIFE-C07 | none yet | flow table shows Post-Purchase revenue |
| win back lapsed buyers, stop mailing dead contacts | is win-back on the brand's cadence | LIFE-C08 | EMAIL-R11, EMAIL-R12 | R12 fires (high, $6,809); R11 unavailable |
| keep subscriptions on schedule | do charge and failed-payment messages land | LIFE-C09 | none | subscription variant later |
| run loyalty, VIP and birthday triggers | do VIPs use the perks | LIFE-C10 | none yet | no loyalty data |
| back-in-stock and post-delivery sends | is every restock alert real | LIFE-C11 | EMAIL-R15 | fires on KC-0342 |
| keep the segmentation model current | are segments stale | LIFE-C12 | EMAIL-R03, EMAIL-R05 | unavailable |
| plan the weekly campaign calendar | am I over-mailing discounts | LIFE-C13 | EMAIL-R14 (honesty, LOOP-C12) | fires on KC-0341 |
| protect sender reputation and list health | is list quality a spam risk | LIFE-C16 | EMAIL-R04, EMAIL-R08 | unavailable: no complaints, no per-contact opens |
| run SMS, WhatsApp and push | SMS or WhatsApp; COD to prepaid | LIFE-C17, LIFE-C22 | EMAIL-R09 | unavailable; COD metric null for US |
| test program and monthly read-out | traffic problem or flow problem | LIFE-C19, LIFE-C20 | EMAIL-R01, EMAIL-R13 | R01 runs, all 6 flows within 15 percent; R13 unavailable |

## Candidates from the room spec (pick 10 per round)

### Questions this screen should answer

- is my pop-up earning its keep or just annoying visitors  (LIFE-C02)
- am I legally allowed to send this message to this person right now  (LIFE-C03)
- is the welcome flow converting inside the first 72 hours  (LIFE-C04)
- how much of my lost cart and browse traffic am I recovering, and does the discount fire too early  (LIFE-C05, LIFE-C06)
- is my post-purchase content actually reducing returns and pulling a second order  (LIFE-C07)
- is win-back timed off this brand's own repurchase cadence or a generic default  (LIFE-C08)
- are charge reminders, pause-or-skip and failed-payment messages actually landing before the problem happens  (LIFE-C09)
- do VIP customers actually notice and use the perks  (LIFE-C10)
- is every back-in-stock alert tied to a real restock, and is the review request timed after delivery, not shipment  (LIFE-C11)
- are my segments still accurate or built on stale rules  (LIFE-C12)
- am I over-mailing discounts and under-mailing everything else  (LIFE-C13)
- is my list quality putting future sends at risk of the spam folder  (LIFE-C16)
- should this message be SMS or WhatsApp, and (for COD markets such as India) is our WhatsApp commerce program converting COD to prepaid  (LIFE-C17, LIFE-C22)
- what changed this month, is it a traffic problem or a flow problem, and what should I test next  (LIFE-C19, LIFE-C20)

### Metrics specified

- `revenue_by_flow_order_matched`: Revenue each flow actually produced, counted from real orders, not from a click window. sum of order revenue where the order's contact received a flow send in the N days before the order (N set per flow type, default 5 days email / 3 days SMS-WhatsApp), attributed to the last flow send before the order
- `flow_conversion_rate`: Share of people who got a flow and then bought. orders attributed to flow ÷ unique contacts who entered the flow, trailing window
- `deliverability_inbox_placement`: Share of sends that land in the inbox, not spam or missing. 1 minus (bounce rate + spam complaint rate), proxy when no seed-test data exists
- `list_health_score`: One number for whether the list is getting healthier or riskier to mail. composite of bounce rate, spam complaint rate, and share of contacts with 0 opens in 180 days, each normalized 0 to 1 and averaged
- `popup_conversion_rate`: Share of visitors shown the pop-up who sign up. pop-up sign-ups ÷ pop-up impressions
- `time_to_first_purchase`: How long a new subscriber takes to buy for the first time. median hours between signup timestamp and first order for subscribers who convert within 30 days
- `sms_whatsapp_opt_in_rate`: Share of email subscribers who also opt in to SMS or WhatsApp. contacts with a valid SMS or WhatsApp consent record ÷ contacts with a valid email consent record
- `consent_coverage`: Share of active contacts with a valid, current consent record for every channel they are sent on. contacts with a logged, unexpired consent record for channel X ÷ contacts sent on channel X in the window
- `list_growth_net`: New contacts minus people who leave the list. new opted-in contacts − (unsubscribes + hard bounces + suppressions)
- `unsubscribe_rate_per_send`: Share of people who unsubscribe from a single send. unsubscribes ÷ delivered, per campaign or flow send
- `whatsapp_cod_to_prepaid_conversion`: Share of WhatsApp cart-recovery or order-update messages that convert a COD order to prepaid (a COD market such as India; reads null for US brands). orders switched from COD to prepaid after a WhatsApp nudge ÷ COD orders that received the nudge
- `quiet_hours_violation_count`: Number of sends that went out outside the allowed local hours for that market. count of esp_sends where sent_at local time falls outside the configured quiet-hours window for the contact's market
- `test_win_rate`: Share of tests in the queue that produced a real, pre-registered win. tests marked won ÷ tests completed, where a win required hitting the pre-registered metric and sample size
- `segment_freshness`: Days since a segment's definition was last recomputed against current data. today minus last_computed_at, per segment
- `welcome_flow_completion_rate`: Share of new subscribers who make it through the whole welcome sequence without unsubscribing. contacts reaching final welcome step ÷ contacts entering step 1
- `winback_reactivation_rate`: Share of lapsed contacts in the win-back flow who place another order. orders from win-back flow contacts ÷ contacts entering win-back
- `flow_frequency_conflicts`: Number of contacts who got messages from 2 or more flows on the same day. count of contact-days where esp_sends shows sends from more than one flow_id
- `channel_revenue_mix`: Share of lifecycle revenue coming from email vs SMS vs WhatsApp. order-matched revenue per channel ÷ total order-matched lifecycle revenue

### Insights specified (rules in code)

- flow revenue mismatch: the platform's reported flow revenue differs from order-matched flow revenue by more than 15 percent for a flow with at least 20 orders in the window → "{flow} shows {platform_rev} in your ESP but only {matched_rev} in real orders, a {pct} percent gap" (action LIFE-C20)
- quiet hours breach: quiet_hours_violation_count > 0 in the trailing 7 days → "{n} messages went out outside allowed hours in {market} this week" (action LIFE-C03)
- flow collision: flow_frequency_conflicts for a contact-day pair exceeds a 5 percent share of active contacts in the trailing 7 days → "{n} contacts got messages from {k} flows on the same day this week" (action LIFE-C12)
- deliverability drop: deliverability_inbox_placement falls more than 5 points versus its trailing 30-day average → "inbox placement dropped from {prev} to {now} percent this week" (action LIFE-C16)
- stale segment: segment_freshness exceeds 7 days for a segment used by an active flow, while the underlying source data changed in that window → "{segment} has not recomputed in {n} days but still feeds {flow}" (action LIFE-C12)
- discount fired too early: a cart or checkout abandonment flow's discount step index is at or before step 1 in flow_defs, against the brief's rule to hold discounts back → "{flow} offers a discount on message 1, before the shop-assistant follow-up gets a chance to work without one" (action LIFE-C06)
- consent gap: a contact received a send on a channel with no matching valid consent record → "{n} sends this week went to contacts with no valid consent record on {channel}" (action LIFE-C03)
- list decay: share of contacts with 0 opens or clicks in 180 days rises above 35 percent of the active list → "{pct} percent of your list has not engaged in 6 months, this is dragging deliverability down" (action LIFE-C16)
- WhatsApp underused for high-value sends: a contact has a valid WhatsApp opt-in and a cart or order value above the brand's top quartile, but the send log shows SMS or email used instead → "{n} high-value sends this week used SMS or email even though the contact opted into WhatsApp" (action LIFE-C17)
- welcome flow drop-off: the fall-off between two consecutive welcome steps exceeds twice the average step-to-step drop for that flow → "{pct} percent of new subscribers drop off between step {a} and step {b}" (action LIFE-C04)
- win-back timing off brand cadence: the win-back flow's trigger delay is a fixed platform default rather than a value derived from this brand's own median days-between-orders → "win-back fires at {default} days but this brand's typical repeat buyer reorders at {median} days" (action LIFE-C08)
- sunset not enforced: a contact has 0 opens across the last 6 sends and is still receiving campaigns, with no sunset flow entry logged → "{n} contacts with 6 unopened sends in a row are still being mailed campaigns" (action LIFE-C08)
- test hygiene violation: a test in test_registry is marked complete with a sample size below its pre-registered minimum, or a read window shorter than pre-registered → "{test} was called before it reached {n} contacts or the {days}-day read window" (action LIFE-C19)
- honesty rule breach: a live send contains a countdown timer or stock-scarcity claim with no matching inventory or time-limited-offer record → "{send} claims '{claim}' but there is no matching inventory or expiry record" (action LOOP-C12)
- back-in-stock false trigger: a back-in-stock alert was sent for a SKU with no matching restock event in the inventory feed in the prior 24 hours → "a back-in-stock alert went out for {sku} with no restock event behind it" (action LIFE-C11)

### Visuals specified

- flow revenue reconciliation (grouped bar chart): platform-reported vs order-matched revenue, per flow
- deliverability trend (line chart): inbox placement and spam complaint rate over the last 90 days
- flow step funnel (step funnel chart): contacts at each step of a chosen flow: entered, delivered, opened, clicked, ordered
- list health meter (gauge/meter): the composite list_health_score with its 3 inputs
- test queue board (kanban-style list with a small bar for win rate): tests planned, running, completed, and win/loss
- channel mix (stacked bar chart): revenue and cost by email, SMS, WhatsApp and push, monthly
- send calendar heatmap (calendar heatmap): campaign and flow sends per day, colored by discount vs non-discount content

### Not in the usual tools

- Revenue by flow is counted from real orders matched to send logs, not from a click-attribution window that counts on send date and gives every touch its own credit
- One consent and quiet-hours record checked before every send across email, SMS and WhatsApp together
- A pre-send honesty check that blocks a scarcity or countdown claim with no matching inventory or expiry record
- Flow revenue mismatch between the platform's own report and real orders is surfaced as its own alert
- Test hygiene (minimum sample, pre-registered read window) is enforced across flows, campaigns and channels in one backlog
- WhatsApp COD-to-prepaid conversion (a COD market such as India) is tracked as its own metric tied to order data

### Data this screen needs

- `esp_sends`: brand, channel, flow_id, campaign_id, contact_id, sent_at, delivered, opened, clicked, bounced (ESP export or API (Klaviyo/Attentive equivalent), not yet connected)
- `orders`: order_id, contact_id, revenue, discount_code, placed_at, utm_source, payment_method (store order export (Shopify or equivalent), not yet connected)
- `consent_log`: contact_id, channel, market, status, updated_at, source (ESP consent API, not yet connected)
- `segments`: segment_id, definition, definition_hash, last_computed_at, member_count (LIFE-C12 segmentation job output)
- `flow_defs`: flow_id, steps, discount_step_index, trigger_rule, quiet_hours_rule (manual entry from the ESP flow builder or ESP API)
- `whatsapp_events`: contact_id, message_type, opt_in_status, cod_flag, converted_to_prepaid, sent_at (WhatsApp Business API or BSP export, not yet connected)
- `test_registry`: test_id, channel, hypothesis, sample_size, start, end, metric, result (LIFE-C19 test program log)
- `inventory_restock_events`: sku, restocked_at, quantity (store inventory feed, not yet connected)

## Rounds

| Round | Features picked | Date | Notes |
|---|---|---|---|
| 0 | 0.1 to 0.4 | 28 Sep 2026 | skeleton, audit, round0.png |

## Round 0 status

1. Built 28 Sep 2026: index.html, screen.js, api.py (overview, findings), audit.py, round0.png at 1280 wide; tests in `tests/test_screen_email.py` (6 pass).
2. Tiles: flow revenue from real orders ($396,439, 11.1 percent of store revenue), net list growth (-976, a negative month), campaign unsubscribe rate (0.30 percent). All simulated.
3. Insights as rules: EMAIL-R01 flow revenue check (quiet, all 6 flows within 15 percent) and EMAIL-R12 sunset proxy (fires). Chart: platform against real-order revenue per flow.
4. Audit fires on Bombas: EMAIL-R12 high ($6,809 at stake), EMAIL-R14 last-call claim with no calendar record, EMAIL-R15 restock send with no restock; 10 rules unavailable with their connector.
5. Contract follow-up for an app-level session: metrics.py reads `flow` and `sent_at`, the generator writes `flow_name` and `send_time` with JSON text ids; `audit.EmailData` bridges it. Add unsubscribe_rate_per_send to metrics.md.
6. Needs a local data.sqlite (scale 0.1 used); Bombas tests skip without it. Next round: welcome 72-hour conversion, discount share of campaigns, send calendar heatmap.
