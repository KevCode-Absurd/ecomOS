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
| ctr | clicks / impressions (all clicks, as the platform reports them) |

Paid metrics take `by=campaign`, `by=adset`, `by=ad` (Meta only) or `by=day` and return `groups`. Ad groups carry ad set, campaign, format, reach, frequency, ctr, first and last day, `dynamic_creative` (from `is_dynamic` or `is_dynamic_creative`, flagged, never split) and `shared_creative` (another ad runs the same image or video; `creative_id` when the table has no image or video field). Reach is summed from daily rows, so frequency here is approximate. Added 28 Sep 2026 for 11-paid-social.

Google rows (28 Sep 2026, S3.5): paid sums read `google_rows` campaign rows only (`row_kind = campaign`); search term and asset group rows are never added to them. The v2 tables name cost `spend`, the sample brand `cost`; both are read.

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

A brand folder that keeps `finance_inputs.json` beside its aggregates (S2.4) is read when the data layer has no `finance_inputs` table. Margin metrics that need order rows (`break_even_roas`, `contribution_margin`) stay unavailable for a brand read through aggregates.

## Products (01)
| Metric | Formula | Source | Window |
|---|---|---|---|
| units | sum of units | `products_monthly` | whole months inside the window; part months left out |
| product_net_sales | sum of net sales (line subtotal minus discounts) | `products_monthly` | same |

Both take `by=sku`, `by=line`, `by=month` or `by=line_month` and return `groups` with units, net sales, SKUs and net per unit. A line is the SKU title without its pack size ("Ankle Sock 4-Pack" is "Ankle Sock"), read from `products`; without that table the line is the SKU category. Added 28 Sep 2026 for 01-market-research.

## Offers (04)
| Metric | Formula |
|---|---|
| returns_by_reason | returns opened in the window by reason (carrier returns out): count, refunded amount, and returns per paid order placed in the same window. The per-order rate holds at any data scale. |
| order_value_distribution | paid orders in bins of `step` dollars (default 5) by order value: subtotal minus discounts, before tax and shipping. Each bin: orders, share, value, orders that paid shipping, shipping charged. |

A brand folder reads both from `data.sqlite` with one GROUP BY each (the tables are too big to load whole); unavailable when data.sqlite is absent. Added 28 Sep 2026 for 04-offers-pricing (free shipping threshold, returns behind an objection rung).

## Speed (08)
Median of the lab's runs in the window from `speed_runs`, for one page, device and variant (default pdp, mobile, baseline).
| Metric | Formula |
|---|---|
| fully_loaded_ms | median load_ms |
| lcp_ms | median lcp_ms |
| fcp_ms | median fcp_ms |
| bytes | median bytes transferred |
| requests | median request count |

## Words used above
Computed in `app/metrics.py`; its docstring holds the same list.
- **paid order**: financial status paid, partially refunded or refunded, and not cancelled. Voided orders are out.
- **net revenue**: line subtotal minus discounts on paid orders. Before tax, shipping charged and refunds. Refunds count as a returns cost in contribution margin.
- **cohort**: first-time customers by month of first order. A cohort counts only once everyone in it has had the full 90 or 180 days; the last 6 such cohorts are used.
- **platform reported**: purchases and purchase value in the paid group come from Meta and Google, not from orders. Order-matched numbers are named as such.
