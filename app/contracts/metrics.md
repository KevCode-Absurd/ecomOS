# Metric contract (starter)

Every number a screen shows is defined here and computed in `app/server.py` from the tables in `contracts/data-sources.md`. Windows end on the last full day. Missing inputs make the metric unavailable, never 0. Period ratios come from totals, never from averaging breakdowns.

Round 0 lifts the metrics the first screens need. Each screen's `FEATURES.md` lists the metrics its room spec asked for; a screen session proposes additions here in a contract session, never inline.

## Pipeline (00-today)
| Metric | Formula | Source | Window |
|---|---|---|---|
| sessions | count of sessions | `sessions` | last 28 full days, 4 trailing windows |
| product_view_rate | sessions with a product view / sessions | `sessions` | same |
| add_to_cart_rate | sessions with add to cart / sessions | `sessions` | same |
| checkout_rate | sessions reaching checkout / sessions with add to cart | `sessions` | same |
| cvr_overall | orders / sessions | `orders`, `sessions` | same |
| aov | net revenue / orders | `orders` | same |
| repeat_rate_90d | customers with a 2nd order within 90 days / first-time customers in the cohort | `orders` | cohorts, last 6 months |
| money_at_stake | (own trailing median or peer band minus current) × volume at the stage × downstream value per unit | computed | current window |

## Reversed orders (06, 15, 19, 21)
| Metric | Formula | Notes |
|---|---|---|
| return_rate | orders with a return / delivered orders | universal |
| chargeback_rate | chargebacks opened / paid orders | universal, benchmark under 0.9 percent |
| dispute_win_rate | disputes won / disputes closed | universal |
| return_to_sender_rate | carrier returned parcels / shipped orders | universal (US carrier exceptions) |
| rto_rate | RTO parcels / cash-on-delivery orders | markets IN only, null for US |
| payment_method_mix | share of orders by card, wallet, BNPL, cod | cod_share null for US |

## Paid (11, 12, 13)
| Metric | Formula |
|---|---|
| spend, impressions, clicks, purchases, purchase_value | sums at ad level, then rolled up; ad-level rows kept when ads share an image |
| period_roas | total purchase value / total spend for the window |
| mer | total revenue / total marketing spend, all channels |
| cpa | spend / purchases |
| frequency | impressions / reach |

## Retention (14, 15)
| Metric | Formula |
|---|---|
| revenue_by_flow_order_matched | revenue of orders matched to a flow send by customer and time window, from `orders`, not platform attribution |
| list_growth | new subscribers minus unsubscribes and bounces |
| ltv_180d | net revenue per first-time customer over 180 days, by cohort |

## Money (21)
| Metric | Formula |
|---|---|
| contribution_margin | net revenue minus COGS, shipping, payment fees, returns cost, marketing spend |
| cash_runway_weeks | cash on hand / average weekly net burn |
| sales_tax_collected | sum by jurisdiction from `orders` |

Speed metrics (08) come from `speed_runs` as measured by the lab: fully_loaded_ms, lcp_ms, fcp_ms, bytes, requests.
