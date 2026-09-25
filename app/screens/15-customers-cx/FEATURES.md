# Customers and CX: features

Status: todo | doing | done | parked. One feature per commit. The first round is the skeleton; after that, features come in rounds of 10, stack-ranked by revenue impact, usefulness and how easy they are to build on dummy data.

## Round 0: skeleton

| # | Feature | Status |
|---|---|---|
| 0.1 | Page shell in the shared UI kit: header, empty-state tiles, insight list, action buttons | todo |
| 0.2 | `api.py` serving this screen's metrics from `app/data/` with unavailable states | todo |
| 0.3 | 3 metric tiles, 2 insights, 1 chart from the sample brand | todo |

## Candidates from the room spec (pick 10 per round)

### Questions this screen should answer

- which touchpoints actually make a customer feel cared for, and which are just broken promises to fix  (LIFE-C23)
- are shipping updates good enough that people stop asking 'where is my order'  (LIFE-C24)
- is what we spend on packaging and inserts earning back attention or reviews  (LIFE-C25)
- is our return, chargeback and (for COD markets) RTO rate normal for this category and market, and is it costing us margin  (LIFE-C26)
- what are people actually contacting us about, and is it getting worse  (LIFE-C27)
- are we asking for reviews at the right moment, replying to the bad ones, and using the good ones anywhere else  (LIFE-C28, LIFE-C28, LIFE-C52)
- is satisfaction moving, and why  (LIFE-C29)
- which customers are actually worth acquiring, on profit, not revenue  (MONEY-C09)
- how much of the budget should go after people who already bought, and at what cost  (LIFE-C32)
- who is about to leave, and which save program should they see  (LIFE-C33)
- are we treating the same customer as 3 different people across channels  (LIFE-C48)
- exactly what can the AI agent refund, change or promise without a human  (LIFE-C49)
- is this 'VIP' customer actually profitable once support, returns and shipping cost are counted  (LIFE-C62)
- can we prove we handled this privacy request and this failed delivery correctly and on time  (LIFE-C66, PROD-C56, LIFE-C55)

### Metrics specified

- `repeat_purchase_rate`: Share of first-time buyers who order again within a set window. customers with a 2nd order within 90 days ÷ customers with a 1st order in the cohort
- `cohort_gross_profit_ltv`: What a cohort of customers is actually worth in profit, not sales, over time. cumulative (order revenue − COGS − payment fees − return/refund cost − shipping cost − support cost allocated to that customer) per customer, grouped by first-order month
- `cac_ltv_ratio`: Whether a customer is worth more than it cost to get them. cohort_gross_profit_ltv at 180 days ÷ blended CAC for that cohort's acquisition channel
- `wismo_ticket_rate`: Share of orders that generate a 'where is my order' contact. tickets tagged as delivery-status ÷ total orders in the same window
- `return_rate`: Share of delivered orders that come back as a return or exchange. returned units ÷ delivered units
- `payment_method_mix`: Share of orders paid by each method: card, wallet (Shop Pay/PayPal/Apple Pay), BNPL (Affirm/Klarna/Afterpay), and (India) cash on delivery. orders by payment_method ÷ total orders
- `failed_and_reversed_orders`: Orders that come back through a failed delivery, a chargeback/dispute, or (for COD markets) a returned-to-origin parcel. group of rates: chargeback_rate = disputed paid orders ÷ total paid orders; dispute_rate = disputes opened ÷ total paid orders; return_to_sender_rate = carrier-returned parcels ÷ total shipped orders; rto_rate (India only) = RTO-flagged COD orders ÷ total COD orders shipped
- `refund_cycle_time`: How long a refund takes from request to money back. median hours between return_requested_at and refund_issued_at
- `nps_score`: Net promoter score from the standing survey. percent promoters (9 to 10) minus percent detractors (0 to 6)
- `support_csat`: Average satisfaction score after a support interaction. mean CSAT score from post-ticket surveys, 1 to 5 or thumbs scale normalized to percent
- `ticket_volume_by_reason`: How many tickets come in for each reason. count of support_tickets grouped by reason_tag
- `first_response_time`: How fast support answers a new ticket. median minutes between ticket opened and first agent or AI reply
- `churn_risk_distribution`: How many customers sit in each churn-risk tier. count of contacts per tier from the churn score (RFM decay + subscription pause events + unresolved tickets + engagement drop)
- `true_customer_profitability`: What a customer is actually worth after every real cost, not just what they spent. customer revenue − returns/refund cost − support cost allocated (tickets × average handle cost) − shipping cost − discount cost given
- `identity_match_rate`: Share of orders, tickets and marketing contacts successfully merged into one profile per real person. records matched to a unified profile ÷ total records checked (orders + tickets + ESP contacts + loyalty)
- `sales_tax_refund_reconciliation_rate`: Share of completed refunds that have a matching, filed tax adjustment (a GST credit note for India). refunds with a linked, filed tax_adjustment_id ÷ total completed refunds
- `privacy_request_sla_compliance`: Share of data access or erasure requests handled inside the legal deadline (CCPA/CPRA and state privacy law for the US; DPDP Act for India). requests resolved on or before their SLA deadline ÷ total requests received
- `failed_delivery_reschedule_success_rate`: Share of failed delivery attempts that get successfully rebooked (a carrier return-to-sender or delivery exception for the US; an NDR'd COD delivery for India). failed-delivery orders successfully redelivered ÷ total failed-delivery orders
- `cx_maturity_score`: Whether CX decisions are random, intentional, or genuinely differentiated. scored checklist against a written experience standard (LIFE-C30), not a computed ratio
- `marketplace_review_rating`: Average public rating on marketplaces and Google, next to the on-site rating for the same product. mean star rating per SKU, per source (Google Business Profile, Amazon, Walmart Marketplace, on-site; Flipkart for India)

### Insights specified (rules in code)

- silent churn risk: a customer's RFM recency decays past their own historical repurchase window, with no support contact and no email/SMS engagement in the same period → "{n} customers are past their usual reorder window with zero contact from us or to us" (action LIFE-C33)
- refund missing tax reversal: a refund is marked completed with no matching sales-tax adjustment after 15 days (India: no linked, filed GST credit note after 15 days, markets IN) → "{n} refunds from the last filing period have no matching tax adjustment on file (GST credit note for India)" (action LIFE-C55)
- unprofitable VIP: a customer tagged VIP by revenue shows negative true_customer_profitability over the trailing 12 months → "{n} of your VIP customers are actually unprofitable once returns and support cost are counted" (action LIFE-C62)
- unanswered negative review: a review rated 2 stars or lower has no response after 5 days → "{n} reviews at 2 stars or below have gone unanswered for over 5 days" (action LIFE-C28)
- failed-delivery loop: the same order has 2 or more failed delivery attempts with no successful reschedule (return-to-sender for US carriers, NDR for India's COD orders) → "order {id} has failed delivery {n} times with no successful rebooking" (action PROD-C56)
- crisis signal: mentions of one complaint theme across public channels (reviews, socials, forums) more than triples the trailing 14-day average in a single day → "mentions of '{theme}' are {n} times the normal rate today" (action BRAND-C54)
- privacy request deadline at risk: an open data request is within 3 days of its legal SLA deadline and not yet resolved (CCPA/state privacy law for the US; DPDP for India) → "request {id} is due in {n} days and is still open" (action LIFE-C66)
- identity fragmentation: the same phone number or email appears on more than one unmerged profile with orders on both → "{n} customers likely have 2 or more unmerged profiles, understating real repeat rate" (action LIFE-C48)
- ticket reason drift: one reason_tag's share of total ticket volume grows more than 10 percentage points month over month → "'{reason}' tickets went from {a}% to {b}% of contacts this month" (action LIFE-C27)
- RTO concentrated in one zone (India): a pincode cluster or courier shows an RTO rate more than double the brand's overall rate, with at least 20 orders in the window; reads null for US brands → "{zone} is running {n}x the average RTO rate on {count} orders this month" (action LIFE-C26)
- return-to-sender concentrated in one zone or carrier: a shipping zone or carrier shows a return-to-sender rate more than double the brand's overall rate, with at least 20 orders in the window → "{zone} is running {n}x the average return-to-sender rate on {count} orders this month" (action LIFE-C26)
- marketplace rating gap: a SKU's marketplace rating is more than 0.5 stars below its on-site rating, with at least 10 marketplace reviews → "{sku} rates {onsite} stars on-site but only {market} on {platform}" (action LIFE-C28)
- AI agent overreach: a logged AI support agent action exceeds its configured autonomy cap (refund amount, address change scope, or action type not on the approved list) → "the AI agent took action '{action}' worth {amount}, above its {cap} cap" (action LIFE-C49)
- marketplace seller queue backlog: marketplace seller-support tickets aging past the marketplace's own SLA and still open → "{n} marketplace buyer messages on {platform} are past SLA and unanswered" (action LIFE-C67)
- WISMO surge in one lane: wismo_ticket_rate for a shipping zone or courier exceeds 2x the brand overall rate → "{zone} is generating {n}x the normal share of 'where is my order' tickets" (action LIFE-C24)

### Visuals specified

- cohort profit curve (cohort heatmap / line chart): cumulative gross-profit LTV by acquisition month, at 30/60/90/180/365 days
- WISMO and delivery funnel (funnel chart): orders shipped, orders delayed, WISMO tickets raised, tickets resolved
- failed-delivery and RTO by zone map (bar chart or choropleth by zone/pincode cluster): return-to-sender rate by shipping zone and carrier (COD RTO rate by pincode and courier for India, markets IN)
- support reason breakdown (stacked bar chart over time): ticket volume by reason tag, monthly
- churn risk tiers (funnel or stacked bar): customers per risk tier and where each tier gets routed (win-back, cancel-save, no action)
- true profitability by tier (waterfall chart): revenue minus returns, support, shipping and discount cost, by loyalty tier
- NPS/CSAT trend (line chart with driver tags): NPS and CSAT over time, annotated with the top driver reason each period

### Not in the usual tools

- Lifetime value is computed on gross profit after returns, support and discount cost, not on revenue
- Failed-delivery, return-to-sender and (India) COD RTO reschedule outcomes are tracked as their own funnel tied to real carrier events
- Support ticket reasons and CSAT are shown next to return, reversed-order (chargebacks, and RTO for COD markets) and true-profitability data in one room
- A single privacy data-request register (CCPA/state privacy law for the US, DPDP for India) that tracks every system holding a person's data, with a legal SLA clock
- One merged customer identity across guest checkouts, phone, WhatsApp numbers, POS and marketplace orders before churn or LTV is scored
- An AI support agent's exact autonomy limits (refund cap, allowed action types) are logged and checked against every action it actually takes

### Data this screen needs

- `orders`: order_id, customer_id, revenue, cogs, payment_method, placed_at, delivered_at, channel (store order export, not yet connected)
- `refunds`: refund_id, order_id, reason, refund_amount, tax_adjustment_id, return_to_sender_flag, carrier, issued_at (store returns/refund export, not yet connected)
- `support_tickets`: ticket_id, customer_id, reason_tag, channel, opened_at, first_response_at, resolved_at, csat_score (helpdesk export (Gorgias or equivalent), not yet connected)
- `reviews`: review_id, source, sku, rating, text, posted_at, responded_at (review platform export + marketplace/Google pulls, not yet connected)
- `nps_survey_responses`: response_id, customer_id, score, comment, sent_at (survey tool export, not yet connected)
- `identity_graph`: profile_id, matched_order_ids, matched_contact_ids, matched_ticket_ids, match_confidence (LIFE-C48 identity resolution job)
- `churn_risk_scores`: customer_id, score, drivers, tier, routed_to, computed_at (LIFE-C33 churn scoring job)
- `tax_adjustments`: adjustment_id, refund_id, jurisdiction, filed_at, amount, credit_note_id (accounting / Avalara-TaxJar export for US sales tax; GST filing export for India (credit_note_id applies to India only, null for US))
- `privacy_requests`: request_id, customer_id, jurisdiction, type, received_at, sla_deadline, resolved_at, systems_checked (manual log until a privacy-request intake form is built (jurisdiction: CCPA/CPRA, other state law, or DPDP for India))
- `marketplace_tickets`: marketplace, ticket_id, status, sla_due, opened_at (marketplace seller console export, not yet connected)
- `ai_agent_action_log`: action_id, customer_id, action_type, amount, cap_at_time, approved_flag, taken_at (AI support agent's own action log, not yet built)
- `carrier_delivery_events`: order_id, carrier, attempt_number, outcome, exception_reason, attempted_at (carrier API or manual export, not yet connected (India: exception_reason also carries the NDR reason code))

## Rounds

| Round | Features picked | Date | Notes |
|---|---|---|---|
