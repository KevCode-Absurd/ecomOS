# Supply and inventory: features

Status: todo | doing | done | parked. One feature per commit. The first round is the skeleton; after that, features come in rounds of 10, stack-ranked by revenue impact, usefulness and how easy they are to build on dummy data.

## Round 0: skeleton

| # | Feature | Status |
|---|---|---|
| 0.1 | Page shell in the shared UI kit: header, empty-state tiles, insight list, action buttons | todo |
| 0.2 | `api.py` serving this screen's metrics from `app/data/` with unavailable states | todo |
| 0.3 | 3 metric tiles, 2 insights, 1 chart from the sample brand | todo |

## Candidates from the room spec (pick 10 per round)

### Questions this screen should answer

- which SKUs run out first  (PROD-C22)
- what do I order, and how much, right now  (PROD-C22)
- what does this SKU actually cost me to land today  (PROD-C23)
- how exposed am I to one supplier or one country failing  (PROD-C23)
- which suppliers are slipping on time, defects or price  (PROD-C69)
- is my warehouse hitting the pick-pack-dispatch times it promised  (PROD-C53, PROD-C52)
- which courier should carry which zone right now  (PROD-C59)
- which failed-delivery orders need action today  (PROD-C56)
- did the carrier pay or bill me correctly  (MONEY-C52)
- what stock is turning into dead weight, and what do I do about it  (PROD-C27)
- which supplier deals need renegotiating soon  (LOOP-C28)
- did I get billed for what I actually received  (MONEY-C53)
- is a cost-down still worth asking for  (PROD-C18)
- am I ready for the Q4/BFCM spike (india: the festive spike)  (PROD-C72)

### Metrics specified

- `stock_cover_days`: How many days of stock are left at current sales pace. current stock units ÷ trailing 14-day average daily units sold
- `reorder_point_units`: The stock level that should trigger a new order. (average daily units sold × lead_time_days) + safety_stock_units
- `safety_stock_units`: Buffer stock held against demand spikes and delays. service-level factor × demand standard deviation × sqrt(lead_time_days)
- `landed_cost_per_unit`: What one unit actually costs after freight, duty and FX. base supplier cost + freight allocated per unit + duty + FX conversion at the rate on the invoice date
- `supplier_concentration_share`: Share of purchase volume from the single largest supplier. largest supplier's purchased units ÷ total purchased units, trailing 12 months
- `country_concentration_share`: Share of purchase volume from the single largest sourcing country. largest country's purchased units ÷ total purchased units, trailing 12 months
- `supplier_scorecard_score`: A supplier's combined on-time, defect and price-stability score. weighted score from on_time_delivery_pct, defect_rate_pct and price_change_frequency over the scoring period
- `fulfilment_sla_adherence_pct`: Share of orders the 3PL dispatched inside its promised time. orders dispatched within contracted SLA window ÷ total orders processed
- `return_to_sender_rate`: Share of shipments a carrier returns to the sender without delivering, by zone. return-to-sender shipments ÷ total shipments for that carrier and zone
- `rto_rate`: Share of cash-on-delivery shipments a courier returns undelivered (RTO), by zone. Reads null for a US brand with no COD orders.. RTO shipments ÷ total COD shipments for that courier and zone
- `chargeback_rate`: Share of paid orders reversed through the card network or PayPal. chargebacks ÷ total paid orders, trailing period
- `dispute_rate`: Share of orders with an open payment dispute awaiting representment. disputed orders ÷ total orders, trailing period
- `payment_method_mix`: Share of orders by payment method: card, wallet (Shop Pay, PayPal, Apple Pay), BNPL (Affirm, Klarna, Afterpay), and, for an India brand, cash on delivery (markets: IN). count of orders by payment_method ÷ total orders, trailing period
- `courier_first_attempt_delivery_rate`: Share of shipments delivered on the courier's first attempt. shipments delivered on attempt 1 ÷ total delivered shipments, by courier and zone
- `courier_delivery_tat_days`: Average days from dispatch to delivery, by courier and zone. mean of (delivered_at − dispatched_at) in days, by courier and zone
- `carrier_exception_open_count`: How many carrier delivery exceptions are open right now (india: non-delivery reports, NDR). count of exception records with status open, grouped by hours remaining in the attempt window
- `cod_remittance_variance`: Difference between what a courier should pay in COD and what it actually paid. Reads null for a US brand with no COD orders.. sum of expected COD amount per order − sum of amount actually remitted, by courier and period
- `dead_stock_value`: Value of stock that is old and barely moving. units aged past the brand's dead-stock threshold × landed_cost_per_unit, summed by SKU
- `price_lock_days_remaining`: Days left before a supplier's price lock or contract expires. contract renewal_date − today, in days
- `three_way_match_exception_count`: How many purchase orders have a quantity or price mismatch against the invoice and goods received. count of PO-invoice-GRN triplets where quantity or unit price differs beyond a set tolerance
- `commodity_input_cost_index`: How the priced-in raw material behind a SKU is trending. current commodity price ÷ price on the date the SKU's cost was last locked, indexed to 100
- `peak_season_readiness_pct`: How ready stock, staffing and systems are for the next Q4/BFCM peak (india: the next festive peak). average of (safety stock vs peak target, warehouse staffing booked vs target, WMS/OMS load-test pass) as percentages
- `exception_to_return_to_sender_rate`: Share of carrier exceptions that end up returned to sender instead of delivering (india: NDRs converting to RTO). orders that end in a return-to-sender after an exception ÷ total orders that had at least one exception, trailing period (india: orders ending in RTO after an NDR ÷ orders with at least one NDR)
- `carrier_billing_variance`: Difference between a carrier's invoiced weight/dimension charge and the packed weight recorded at dispatch. sum of invoiced charge − sum of expected charge from dispatch weight, by carrier and period

### Insights specified (rules in code)

- reorder breach: stock_cover_days is less than lead_time_days plus the safety buffer for that SKU → "{sku} has {days} days of cover against a {lead} day lead time. Place the order now." (action PROD-C22)
- landed cost drifted without a margin recheck: landed_cost_per_unit has moved more than 5% since the last margin gate run for that SKU, and the gate has not been rerun → "{sku}'s landed cost moved {pct}% since its margin was last checked. Rerun the gate before the next order." (action PROD-C23)
- supplier concentration risk: supplier_concentration_share exceeds 60% with no backup supplier mapped in a second country → "{pct}% of {sku}'s volume comes from one supplier with no mapped backup. One factory problem stops this SKU." (action PROD-C23)
- supplier scorecard slipping: supplier_scorecard_score falls for 2 consecutive scoring periods → "{supplier}'s scorecard has dropped for {n} periods in a row. Review before the next PO." (action PROD-C69)
- courier underperforming a zone: courier_rto_rate for a courier-zone pair is more than 10 points above the brand's best courier in the same zone → "{courier} runs a {pct} return-to-sender rate in {zone}, {diff} points worse than {best_courier}. Shift volume. (India: read as RTO rate.)" (action PROD-C59)
- carrier exception aging toward its attempt window: an open carrier exception has fewer than 4 hours left before the attempt window closes → "{n} carrier exceptions close their attempt window in under 4 hours. Confirm the address or reschedule now. (India: NDRs.)" (action PROD-C56)
- COD remittance shortfall: cod_remittance_variance is nonzero for a closed remittance cycle → "{courier} remitted {amount} less than expected for {period}. Open a billing dispute. (India only; markets: IN.)" (action MONEY-C52)
- stock turning into dead weight: a SKU's inventory age passes the brand's dead-stock threshold while its sales velocity stays below the brand's slow-mover line → "{sku} has {units} units aged past {days} days with barely any sales. Draft a clearance plan." (action PROD-C27)
- price lock expiring soon: price_lock_days_remaining is under 30 days with no renegotiation started → "{supplier}'s price lock ends in {days} days. Start the renewal conversation now." (action LOOP-C28)
- invoice does not match goods received: three_way_match_exception_count is greater than 0 for a PO ready to pay → "{po_id} has a quantity or price mismatch against what was received. Hold payment and check it." (action MONEY-C53)
- commodity cost spike: commodity_input_cost_index rises more than 8% since the SKU's cost was last locked → "The raw material behind {sku} is up {pct}% since the last price lock. Recheck margin before the next PO." (action PROD-C18)
- peak season not ready: peak_season_readiness_pct is below 80% with fewer than 45 days left to the Q4/BFCM date (india: the festival date) → "Peak-season readiness is {pct}% with {days} days to go. Stock, staffing or systems need attention now." (action PROD-C72)
- carrier exceptions converting to return-to-sender more than usual: exception_to_return_to_sender_rate rises more than 10 points above the brand's trailing 90-day average → "Carrier exceptions are converting to return-to-sender {pct} more than usual this period. Check address-confirmation outreach and carrier performance. (India: NDRs converting to RTO.)" (action PROD-C56)
- chargeback rate rising: chargeback_rate rises above the card networks' excessive-chargeback threshold or more than 50% above the brand's trailing average → "Chargeback rate is {pct}, {diff} above normal. Review dispute reason codes before it risks processor standing." (action MONEY-C52)

### Visuals specified

- stock cover heat grid (heat map): each SKU's stock_cover_days against its lead time, colour-coded from safe to breach
- landed cost waterfall (waterfall chart): base cost stepping up through freight, duty and FX to the final landed cost per unit
- courier scorecard bars (grouped bar chart): return-to-sender rate (india: RTO rate), first-attempt delivery rate and TAT per courier, grouped by zone
- supplier scorecard trend (small multiples line chart): each active supplier's on-time, defect and price-stability score over the last 6 scoring periods
- carrier exception funnel (funnel chart): orders raised as a carrier exception, attempted again, resolved, or converted to return-to-sender (india: NDR, RTO)
- dead stock aging bars (stacked bar chart): inventory value by SKU, stacked by age band, with the dead-stock threshold marked
- reversed orders group (grouped bar chart): chargeback_rate, dispute_rate and return_to_sender_rate side by side, with rto_rate shown only for a brand offering COD (markets: IN)

### Not in the usual tools

- recomputes landed cost the moment FX, freight or duty changes, and flags when a margin gate needs a recheck because of it
- joins the carrier scorecard to this brand's own chargeback and return-to-sender cost to decide retry versus acceptance per order (india: COD reversal cost to decide NDR reschedule versus RTO)
- sizes safety stock against peak-season spike risk (Q4/BFCM demand, carrier return-to-sender risk), and against India-specific festive and COD-RTO risk where that applies (markets: IN), in the same screen as the reorder point
- ties a supplier's scorecard directly to its concentration share and backup-factory status in one view
- combines safety stock, warehouse staffing and WMS load readiness against the Q4/BFCM calendar (india: the festive calendar) into one readiness percentage

### Data this screen needs

- `sku_inventory`: sku, channel, stock_units, avg_daily_units_sold, lead_time_days, stock_cover_days, synced_at (inventory or WMS feed)
- `reorder_calc`: sku, reorder_point_units, safety_stock_units, recommended_po_qty, calculated_at (reorder point script (code))
- `landed_cost`: sku, base_cost, freight_per_unit, duty, fx_rate, landed_cost_per_unit, recomputed_at (landed cost script tied to FX and freight feeds)
- `supplier_master`: supplier_id, country, volume_share, backup_supplier_id, backup_country (manual entry plus PO history rollup)
- `supplier_scorecard`: supplier_id, period, on_time_pct, defect_rate_pct, price_change_count, score (scorecard script from PO and inspection records)
- `fulfilment_sla`: threepl_id, metric, target, actual, period (3PL/WMS dispatch log feed)
- `courier_scorecard`: courier, zone, shipments, return_to_sender_rate, rto_rate, first_attempt_rate, tat_days, period (courier or aggregator API feed)
- `carrier_exception_queue`: order_id, courier, raised_at, attempt_window_closes_at, status, resolution (carrier exception feed (india: courier NDR feed))
- `cod_remittance`: courier, period, expected_amount, paid_amount, variance, order_ids (courier remittance file reconciliation script (india only; markets: IN))
- `dead_stock`: sku, age_days, velocity, value, clearance_plan_status (inventory age script joined to sales and landed cost)
- `supplier_contracts`: supplier_id, price_lock_end, renewal_date, terms_summary (manual entry)
- `three_way_match`: po_id, invoice_id, grn_id, qty_variance, price_variance, status (three-way match script against PO, invoice and goods-receipt records)
- `commodity_index`: material, sku_mapped, price_index, last_locked_date, date (commodity price tracking script)
- `peak_season_plan`: peak_window_name, date, safety_stock_target, staffing_target, wms_load_target, readiness_pct (manual plan plus rollup of the metrics above)
- `carrier_billing`: carrier, period, invoiced_amount, dispatch_weight_amount, variance (carrier billing file reconciliation script)
- `payment_disputes`: order_id, payment_method, chargeback_flag, dispute_status, reason_code, opened_at (payment processor chargeback/dispute feed)

## Rounds

| Round | Features picked | Date | Notes |
|---|---|---|---|
