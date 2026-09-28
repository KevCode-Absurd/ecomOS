# Paid social: features

Status: todo | doing | done | parked. One feature per commit. The first round is the skeleton; after that, features come in rounds of 10, stack-ranked by revenue impact, usefulness and how easy they are to build on dummy data.

## Round 0: skeleton

| # | Feature | Status |
|---|---|---|
| 0.1 | Page shell in the shared UI kit: header, simulated-data line, tiles, insights, decision row | done |
| 0.2 | `api.py` (`overview`, `findings`, default brand bombas) from `app/metrics.py`, unavailable states | done |
| 0.3 | Tiles: spend pace vs 28-day run rate, Meta ROAS and MER side by side, CPA; window and freshness on each | done |
| 0.4 | Kill and scale list by rule (kill: 7-day ROAS under break-even, live 7 days, spend over 3 x target CAC; scale: ROAS over target, frequency under 2.5), money not paid back | done |
| 0.5 | Creative table at ad level, shared-image and dynamic flags, verdict per ad | done |
| 0.6 | Fatigue insight: CTR down 20 percent over 14 days while frequency rises | done |
| 0.7 | Chart: daily Meta spend and purchases, 90 days | done |
| 0.8 | `audit.py`: PAID-R01 kill and PAID-R03 fatigue in the audit.md shape, money at stake, unavailable when ad rows are missing | done |

Round 0 notes (28 Sep 2026, Bombas simulated, scale 0.1):
- Break-even ROAS for Bombas falls back to 1 / target gross margin (1.61x). `break_even_roas` needs order rows, and the Bombas finance_inputs SKU keys (`BMB-...`) do not match the generator's SKUs (`BB-...`), so full costs cannot be joined yet. Data-layer fix, not this screen.
- The simulated ad rows have flat CTR and frequency under 2.1, so PAID-R03 fires on nothing for Bombas. The rule is proven on a synthetic account in `tests/test_screen_paid_social.py`. The generator needs a fatigue curve to show it.
- Frequency is impressions over summed daily reach, so it reads low. A period reach pull fixes it.

## Candidates from the jobs-to-be-done table (PRODUCT-PLAN.md 5.3, Meta)

Goal: profitable new-customer acquisition at target CAC and MER, with retention spend kept efficient.

| Job | Who does it today | Data needed | Candidate feature | Status |
|---|---|---|---|---|
| Know where money goes and what it returns | media buyer | insights at ad level, daily, actions and values, MER from orders | spend vs plan (needs a monthly budget), ROAS and CPA by campaign and ad set, MER next to platform ROAS | partly done (pace, ROAS, MER, CPA tiles) |
| Kill and scale | media buyer | 7d and 28d rows, frequency, CTR trend, purchases | ranked kill and scale list with the rule that fired and the dollars at stake; ad set level; 28-day read | partly done (ad level, 7 days) |
| Find winning and losing creative | creative strategist | creatives joined to insights, tagged by angle, hook, format, avatar | creative leaderboard, fatigue alerts, winners by angle and avatar | partly done (table, fatigue rule) |
| Cover the creative map | creative strategist | brain avatars and angles, current ads tagged | coverage grid of avatars by angles by formats, gaps turned into briefs | todo |
| Produce new creative | creative team, agency, UGC creators | brain voice, claims, winners, competitor signals, references | brief generator, script generator, static concepts, variant sets from a winner, claim check | todo (09-creative owns most) |
| Know which audiences and placements work | media buyer | breakdowns by age, gender, placement, geo, device | breakdown tables with significance flags, structure audit (consolidation, Advantage+ versus manual, exclusions) | todo |
| Watch competitors | strategist | Ad Library by page, run length, formats | competitor board, long-running ads as signals, never copied | todo |
| Keep setup healthy | technical marketer | pixel and dataset stats, event match quality, catalog diagnostics | setup audit with fixes | todo |
| Match ad to page | media buyer and CRO | ad promise, landing page content, page speed | message-match audit, ad to page to checkout trace | todo |
| Plan tests | strategist | registry of past tests, current spend | test plan with sample size and read dates, conflicts flagged | todo |
| Report | account manager | everything above | weekly founder summary in plain words | todo |

## Candidates from the room spec (pick 10 per round)

### Questions this screen should answer

- are we pacing to hit the month's budget and margin target  (MEDIA-C46, MEDIA-C47, MEDIA-C42)
- what is actually holding this account back  (MEDIA-C01)
- does Meta's own ROAS agree with what the brand actually made  (MONEY-C23, MEDIA-C06, MEDIA-C56)
- which ad sets do I touch today and by how much  (MEDIA-C17, MEDIA-C15, CREA-C15)
- is the account built the way it should be for our spend  (MEDIA-C09, MEDIA-C10, MEDIA-C11)
- are we wasting reach on bad placements or a bid strategy that fits the wrong stage  (MEDIA-C12, MEDIA-C13, MEDIA-C14)
- is retargeting eating cold budget, and is DPA read the right way  (MEDIA-C19, MEDIA-C20)
- why did yesterday's numbers move so much, and is it us or the market  (MEDIA-C45, MEDIA-C68, SITE-C36, BRN-C11)
- is our tracking clean and are we accepting Meta's suggestions blindly  (MONEY-C21, MEDIA-C07)
- is TikTok set up, scaling and Shop-ready the way the playbook says  (MEDIA-C24, MEDIA-C25, MEDIA-C26, MEDIA-C27, CREA-C20, MEDIA-C29)
- are we ready for the sale date and for buyers outside the US  (MEDIA-C21, MEDIA-C22)
- is anything about to get an ad rejected or a login lost  (MEDIA-C23, MEDIA-C59, MEDIA-C55, MEDIA-C55)
- what is waiting on me right now and why  (ORCH-C03, LOOP-C03, LIFE-C22, MEDIA-C07, MEDIA-C62, MEDIA-C63, MEDIA-C63)

### Metrics specified

- `blended_mer`: Total new-customer revenue for every dollar of ad spend, across all channels. total new customer revenue / total spend (Meta + TikTok + Google)
- `meta_platform_roas`: What Meta itself says it returned. purchase value / spend, period totals only
- `tiktok_platform_roas`: What TikTok itself says it returned. attributed revenue / spend, period totals only
- `new_customer_cac`: What it costs to win one new customer. total spend / new customers acquired
- `frequency_by_segment_30d`: How many times the same person saw an ad in 30 days, by audience, not blended. impressions / reach per audience segment, 30-day window
- `spend_pace_vs_budget`: Are we on track to land on this month's budget. (spend to date / days elapsed) x days in month, vs planned monthly budget
- `month_end_mer_forecast`: Where blended MER is heading if nothing changes. trailing 7-day MER projected across remaining days, weighted by trailing pace
- `adset_verdict`: Keep, watch or kill, read at the ad set level. ROAS vs target read at 3x to 5x target CPA spent (rule set in MEDIA-C17)
- `creative_volume_ratio`: New ads launched against the $1,000-of-spend benchmark. new ads launched in period / (monthly spend / 1000)
- `concept_count_vs_band`: Number of live concepts against the band for this spend tier. count of distinct SKU + pain-point + offer concepts currently live
- `existing_customer_spend_share`: Share of spend protecting existing customers vs winning new ones. spend in the dedicated existing-customer campaign / total spend
- `dpa_7day_click_roas`: Dynamic product ad return, read the way it should be read. attributed value on 7-day click window / DPA ad set spend
- `pixel_capi_match_quality`: How well orders and their value are passing through to Meta. event match quality score + share of purchase events with value populated
- `suggestion_log_status`: How many platform suggestions were applied without a logged test. count of applied Advantage+/automated suggestions with no before/after entry
- `tiktok_spark_authorization_days_left`: Days left on a creator's Spark authorization. 365 - days since authorization code granted, per active Sparked post
- `account_quality_flags`: Open policy rejections or account-quality warnings across Meta and TikTok. count of open disapprovals / quality flags
- `message_match_lag_days`: Days since the best-performing ad's headline last matched the landing page. days since landing page headline was updated to mirror the current top ad's headline
- `stock_pace_risk`: Whether a scaling ad set is about to sell out its product. days of stock left at current sales pace, for products in ad sets tagged Scale
- `competitor_discount_overlap`: Shared products a competitor is discounting 20% or more. count of the brand's ad-featured products also seen discounted 20-30%+ in competitor ad library snapshot
- `marginal_roas_by_channel`: What the next dollar of spend would likely return, by channel. change in value / change in spend over the last 2 comparable budget steps, per channel

### Insights specified (rules in code)

- MER disagrees with platform ROAS: blended MER is 20% or more below Meta or TikTok's own reported ROAS for the same period → "Meta says {platform_roas}x but the brand's own numbers say {blended_mer}x. Check attribution before scaling." (action MONEY-C23)
- kill/keep/scale table: at 3x to 5x target CPA spent with ROAS more than 30% below target and no purchases, mark Kill; within 30% of target, mark Watch; at or above target, mark Scale → "{n} ad sets are ready to kill, {n} to scale." (action MEDIA-C17)
- frequency rising, reach flat: 30-day frequency for a segment up 20% or more while cold reach for that segment is flat or falling → "{segment} frequency hit {freq}x with reach flat. Creative is wearing out, not the audience." (action CREA-C15)
- spend or ROAS anomaly: a day's spend or ROAS moved 50% or more against the trailing 14-day median → "{date} spend moved {pct}% against the last 14 days. {ad_names} caused most of it." (action MEDIA-C45)
- anomaly root cause fan-out: when an anomaly fires, pull same-day site speed, stock level and competitor activity automatically → "The {date} drop lines up with {cause} on the same day." (action MEDIA-C68)
- creative volume below benchmark: new ads launched in 30 days is under 70% of (monthly spend / 1000) → "Only {n} new ads launched this month against a benchmark of {target}." (action CREA-C18)
- DPA in the wrong bucket: a dynamic product ad set is inside the main cold CBO instead of its own capped ad set → "DPA is sharing budget with cold prospecting. Give it its own capped ad set." (action MEDIA-C20)
- naming or purpose gap: a live campaign has no one-line purpose on file or its ad sets do not follow the fixed naming pattern → "{n} campaigns have no purpose line on file." (action MEDIA-C10)
- scaling into a stockout: an ad set marked Scale features a product with under 14 days of stock left → "{ad_set} is scaling {product}, which has {days} days of stock left." (action MEDIA-C42)
- competitor discount on a shared product: a competitor is discounting a product the brand also runs ads for by 20% or more → "{competitor} cut {product} by {pct}%. Consider pulling or de-prioritising it." (action BRN-C11)
- message mismatch: the current top ad's headline has not appeared on the landing page within 1 day of becoming the top ad → "The top ad says '{headline}' but the landing page still says something else, {days} days on." (action SITE-C36)
- unlogged platform suggestion: a platform-applied Advantage+ or automated suggestion has no before/after entry in the suggestion log → "{n} suggestions were applied with no test on record." (action MEDIA-C07)
- Spark authorization expiring: an active Sparked post's creator authorization has 30 days or fewer left → "{creator}'s Spark authorization expires in {days} days." (action MEDIA-C26)
- policy rejection pattern: 2 or more rejections in 30 days cite the same policy clause → "{n} ads were rejected for {clause} this month. Fix the pattern, not just the ad." (action MEDIA-C55)
- founder-gate queue non-empty: any decision the idea bank or catalogue marks founder_gate is open and unresolved → "{n} decisions are waiting on you: {labels}." (action ORCH-C03)

### Visuals specified

- pacing gauge (gauge plus line): month-to-date spend vs planned budget, with a projected end-of-month line
- kill/keep/scale table (table with verdict chips): every live ad set, its ROAS, spend and verdict, ranked by spend at risk
- frequency by segment small multiples (small line charts, one per audience segment): 30-day frequency trend per segment against cold reach
- anomaly strip (calendar heat strip): every day in the range shaded by how far spend or ROAS moved from the 14-day median
- MER bridge (waterfall): Meta ROAS, TikTok ROAS and blended MER side by side with the gap labelled
- change log timeline (vertical timeline): every structure, bid or targeting change with who made it and the before/after read
- TikTok organic-to-Spark timeline (step timeline): post date, 5 to 7 day organic read, Spark date, authorization expiry
- marginal ROAS bars (bar chart): the next-dollar return estimate per channel, side by side

### Not in the usual tools

- puts ad-set kill/keep/scale verdicts next to same-day stock level and competitor discount data, not performance numbers alone
- computes blended MER from the brand's own contribution margin and reconciles it against Meta's and TikTok's own reported ROAS every time before a scale call
- logs every Advantage+ or automated suggestion applied, with a persisted before/after read attached to it
- fans one spend or ROAS anomaly out to the brand's own site speed, stock level and competitor snapshot from the same day, automatically
- tracks each TikTok Spark creator's 365-day authorization next to the organic post that earned it, with the expiry clock visible
- routes every founder-gate call (scale ceiling, order-confirmation-flow rollout, new-surface pilot, agentic-bidding guardrail) into one queue instead of leaving it split across ad account settings

### Data this screen needs

- `meta_ad_daily`: ad_id, adset_id, campaign_id, date, spend, purchases, purchase_value, impressions, link_clicks, frequency (Meta MCP (read-only) + meta_gallery.refresh)
- `tiktok_ad_daily`: ad_id, adgroup_id, campaign_id, date, spend, conversions, attributed_revenue, impressions, clicks (TikTok Ads Manager API (not yet connected))
- `brand_revenue_ledger`: date, order_id, new_or_existing_customer, revenue, gross_profit (brand brain (not yet built))
- `creator_authorizations`: creator, post_id, authorized_at, expires_at, sparked (brand record, manual entry today)
- `suggestion_log`: date, platform, suggestion, applied_by, before_metric, after_metric (brand record, manual entry today)
- `stock_feed`: sku, on_hand, daily_sales_rate, days_of_stock (brand's inventory system (not yet connected))
- `competitor_snapshot`: brand, ad_id, product, discount_pct, captured_at (Meta Ad Library snapshot (manual pull))
- `landing_page_snapshot`: page, headline, captured_at (site crawl (not yet built))
- `account_activity_log`: platform, date, type, entity, clause, status (Meta and TikTok activity log APIs)
- `founder_decision_queue`: id, capability, label, opened_at, status (brand record (not yet built))

## Rounds

| Round | Features picked | Date | Notes |
|---|---|---|---|
| 0 | 0.1 to 0.8 | 28 Sep 2026 | skeleton on Bombas simulated data |


## Round 1 candidates (ranked 28 Sep 2026 by the lead session)

Ranked by revenue impact, usefulness to a founder deciding alone, and buildable on the simulated data. Kevin picked the 5 screens; the top 5 here are recommended for round 1. One feature per commit, this table updated in the same commit.

| # | Feature | Capability | Why buildable now | Impact |
|---|---|---|---|---|
| 1.1 * | Kill, keep, scale table at ad set level with verdict chips, ranked by spend at risk | MEDIA-C17 | ad_rows has ad set daily spend and value; the rule is fixed at 3x to 5x target CPA | high |
| 1.2 * | MER bridge: Meta ROAS next to blended MER from the brand's own orders and contribution margin, with the disagreement rule | MONEY-C23 | orders and finance inputs exist; the reconciliation before any scale call | high |
| 1.3 * | Pacing gauge: month-to-date spend against budget with an end-of-month MER forecast | MEDIA-C46 | spend by day exists; budget is a founder record | high |
| 1.4 * | Frequency by segment small multiples, with the frequency-rising-reach-flat rule | CREA-C15 | impressions and reach by ad set in ad_rows | medium |
| 1.5 * | Anomaly strip with root-cause fan-out to same-day site speed, stock and competitor activity | MEDIA-C68 | speed_runs, inventory and Ad Library learnings are all in the data layer | high |
| 1.6 | Scaling into a stockout: Scale ad sets checked against days of cover for the featured product | MEDIA-C42 | inventory table plus the ad's product line | medium |
| 1.7 | Creative volume against the 1,000-dollars-of-spend benchmark | CREA-C18 | first date per creative_id in ad_rows | medium |
| 1.8 | Existing-customer spend share and DPA in its own capped ad set | MEDIA-C20 | campaign names carry the structure in the generator | medium |
| 1.9 | Competitor discount overlap from Ad Library offers seen, signals only | BRN-C11 | brain learnings and offers from the 13-page pull | low |
| 1.10 | Founder-gate queue: every waiting decision in one list with the decision row | ORCH-C03 | decisions log exists | low |

\* recommended for round 1
