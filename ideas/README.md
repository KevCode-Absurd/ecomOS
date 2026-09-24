# Idea bank: the playbooks as a source of ideas, not instructions

Date: 24 Sep 2026. Decision by Kevin after two blind tests showed the v2 playbooks do not improve agent output when loaded as instructions. The corpus is kept and used differently: each domain playbook becomes a bank of structured ideas that an agent can draw from, filter by the brand's bottleneck and store type, score with the brand's own numbers, rank, and put in front of the founder for approval before anything is executed.

## The loop this feeds

1. Diagnose: compute the brand's metric contract (below) and compare with benchmarks and the brand's own history to find the bottleneck.
2. Propose: pull ideas for that bottleneck from the bank, drop the ones whose signal does not fire in the brand's data, fill the scoring fields with evidence, rank in code.
3. Approve: the founder approves or rejects each idea with a reason; reasons become weights.
4. Execute: a skill per implementation type turns the approved idea into a brief, copy, page or test. Meta stays read-only.
5. Learn: the experiment registry records the result and updates the effect prior for that brand.

## Files

- `ideas/schema.json`: the record shape (JSON Schema). Every file must validate.
- `ideas/v1/<folder>.json`: one file per domain playbook, an array of idea records. Built by `scripts/extract_ideas.py`-style agents from `playbooks/v2/<folder>/PLAYBOOK.md`, not from cards.json directly.
- `scripts/validate_ideas.py`: schema, enums, card ids against cards.json, rule ids against the playbook, duplicate titles, em dashes. Run on every file before commit.
- `intelligence/ideas.py`: loader, filters, keyword search and the scoring function. Command line: `python3 scripts/ideas.py --bottleneck site_speed --store hero_sku india_mobile`.

## Bottleneck taxonomy (fixed)

| code | means |
|---|---|
| acquisition_volume | not enough qualified traffic |
| acquisition_efficiency | traffic costs too much per order |
| conversion | visitors do not buy |
| aov | orders are too small |
| repeat_retention | customers do not come back |
| margin_cogs | orders do not make enough money |
| cash_inventory | cash is stuck in stock, or stock runs out |
| fulfilment_cx | orders are slow, wrong, or support is behind |
| trust_brand | people do not believe the store |
| site_speed | pages are slow |
| measurement_data | the numbers cannot be trusted |
| team_capacity | the founder or team is the limit |
| risk_compliance | fraud, bots, claims, platform rules |

## Store condition tags (fixed)

`any`, `hero_sku`, `catalogue`, `low_aov`, `high_aov`, `subscription`, `one_off`, `marketplace_heavy`, `dtc_only`, `luxury_considered`, `impulse`, `india_mobile`, `us`, `shopify`, `custom_platform`, `paid_social_led`, `organic_led`, `new_store`, `scaling_store`.

## Metric vocabulary (v0 of the metric contract)

Traffic: `sessions`, `paid_sessions`, `organic_sessions`, `ai_referrals`.
Conversion: `cvr_overall`, `cvr_pdp_to_cart`, `cvr_cart_to_checkout`, `cvr_checkout_to_order`, `bounce_rate_pdp`.
Value: `aov`, `units_per_order`, `discount_rate`.
Retention: `repeat_rate_90d`, `repeat_rate_365d`, `ltv_180d`, `subscription_churn`, `list_size`, `flow_revenue_share`, `email_click_rate`.
Ads: `spend`, `roas_blended`, `roas_prospecting`, `roas_retargeting`, `cpa`, `ncpa`, `ctr`, `cpm`, `frequency`, `hook_rate`, `hold_rate`.
Margin: `gross_margin`, `contribution_margin`, `cogs_per_unit`, `landed_cost`, `return_rate`, `refund_rate`, `defect_rate`.
Cash and stock: `days_of_stock`, `stockout_days`, `inventory_turns`, `cash_conversion_days`, `supplier_lead_days`.
Ops: `fulfilment_days`, `on_time_ship_rate`, `ticket_backlog`, `first_reply_hours`, `csat`, `review_rating`, `review_count`.
Speed: `lcp_mobile_p75`, `inp_mobile_p75`, `cls_mobile_p75`, `ttfb`, `page_weight_kb`, `third_party_kb`.
Measurement: `event_match_quality`, `tracking_coverage`, `attribution_gap`, `bot_share`.
Search: `organic_clicks`, `indexed_pages`, `ai_citations`, `marketplace_share`.

Use `other:<name>` when none fits. The list grows only through this file.

## Rules for idea records

- One idea is one thing a store could do or test. Not a definition, not a warning on its own; turn a mistake into the idea that avoids it.
- Plain language, short sentences, digits, no em dashes. Below tenth-grade reading level.
- `expected_effect.basis` is honest: `measured` only where a source reports a measured result, `source_claim` where a source asserts it, `general_practice` where no source says it.
- No invented numbers. Effect sizes are ranges or words from the source, or "unknown".
- Evidence stays attached: card ids as the playbook cites them, rule ids from the playbook.
- Ideas are brand-agnostic. Brand facts and brand results live in the brand brain and the registry, never in the bank.
