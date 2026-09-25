# Events between screens

A screen never calls another screen. It writes a row to the data layer; the other screen reads it. This file lists the hand-offs so nobody invents a second path.

| From screen | Writes | To table | Read by |
|---|---|---|---|
| 01-market-research | product candidates with landed cost and go or no-go | `product_candidates` | 04-offers-pricing, 19-supply-inventory |
| 02-customers-avatars | avatars, language bank, objection map | `avatars`, `language_bank` | 09-creative, 10-copy, 07-landing-pages-cro, 14-email-messaging |
| 03-competitors | competitor snapshot, positioning map | `competitor_snapshot` | 02-customers-avatars, 09-creative, 04-offers-pricing |
| 04-offers-pricing | offers, free shipping threshold, discount policy | `offers` | 07-landing-pages-cro, 10-copy, 14-email-messaging, 21-finance-cash |
| 05-brand-brain | claims tiers, decisions, red lines | `claims`, `decisions` | every screen (claim check, red-line check) |
| 08-site-speed | speed runs and fix chain | `speed_runs` | 00-today, 07-landing-pages-cro |
| 09-creative | creative set, audience spec, launch checklist | `creatives`, `audience_specs` | 11-paid-social |
| 11-paid-social, 12-google-ads | fatigue reads, winners and losers by angle | `ad_results` | 09-creative, 10-copy |
| 14-email-messaging | flow performance from orders | `flow_results` | 15-customers-cx, 21-finance-cash |
| 15-customers-cx | support reasons, returns, chargebacks | `tickets`, `reversed_orders` | 04-offers-pricing, 07-landing-pages-cro, 21-finance-cash |
| 19-supply-inventory | stock cover, reorder points, landed cost | `inventory`, `landed_cost` | 21-finance-cash, 11-paid-social (stock-aware pacing), 20-marketplaces |
| 21-finance-cash | contribution margin by SKU and channel | `margin` | 04-offers-pricing, 11-paid-social, 01-market-research |
| 22-measurement | metric freshness, unavailable fields | `contract_status` | 00-today, every screen's empty state |
| every screen | decisions on action buttons | `decisions` | 25-experiments, 00-today |
| 25-experiments | read results and learnings | `registry` | 00-today, 26-reports, every screen's priors |
