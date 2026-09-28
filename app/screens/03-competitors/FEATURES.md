# Competitors and market: features

Status: todo | doing | done | parked. One feature per commit. The first round is the skeleton; after that, features come in rounds of 10, stack-ranked by revenue impact, usefulness and how easy they are to build on dummy data.

## Round 0: skeleton

| # | Feature | Status |
|---|---|---|
| 0.1 | Page shell in the shared UI kit: header, simulated and public signal badge, lookalike page warning, decision row | done |
| 0.2 | `api.py` (overview, audit) reading the brain through `store.py`, raw Ad Library records as fallback, and simulated `products_monthly` for brand prices; unavailable states | done |
| 0.3 | 3 tiles (competitors tracked, price position index, competitor active ads), 2 insights as rules (same offer type run longer; price outside the 85 to 115 band), 1 chart (active ads per brand) | done |
| 0.4 | Competitor cards: positioning, price band, what they push, active ads, longest run as a signal, gap to own | done |
| 0.5 | Positioning map to scale: median price per pair (with public band) against a durability or comfort claim score (0 to 3, scored in code from hooks and positioning), open quadrants shaded | done |
| 0.6 | Price ladder table: each brand sock pack per pair against each competitor's median and band | done |
| 0.7 | What they run board: formats and hook types only, no ad text | done |
| 0.8 | `audit.py`: COMP-R01 unclaimed angle, COMP-R02 price gap, COMP-R03 same offer type run longer, COMP-R04 lookalike page; tests in `tests/test_screen_competitors.py` | done |

Round 0 notes (28 Sep 2026): brand price per pair is simulated net sales per unit (after discounts) for the last full month, so it reads lower than list. Competitor bands are one public capture, so price and angle findings are medium with confidence 0.5 or lower; the "2 consecutive captures" part of the price drift rule waits for a second capture. Claim scores are keyword rules, not judgement. Screenshot: `round0.png`.

## Round 1: the execution surface (depth contract)

| # | Feature | Status |
|---|---|---|
| 1.1 | Round 0 anti-patterns out: plan board first with ranked actions from `rank` (`actions.py`: real titles, steps, artefacts and drafts for COMP-R01 to R04), orientation beside it, what is wrong with evidence rows, action cards, desk, audit and rule list at the bottom; tiles, insight cards, the active-ads chart and the lookalike banner removed | done |
| 1.2 | Competitor pills (all, direct, basics and apparel, threats) and the side-by-side table: the 12 pages in the brain's competitive frame plus ours, active ads, format mix, median days live, offer share, offers seen; threat, watch or ignore from 5 counted points with the reason in numbers; row opens a panel with us against them, angle tags with the word that set each, a battlecard draft (BRAND-C57) and a weekly watch (BRN-C11). `pages.py` reads an ad-level snapshot first when one exists | done |
| 1.3 | Creative coverage matrix (`coverage.py`): 10 angles by 5 formats, our share of ads against theirs in every cell, all pages or direct only; gap when they put 3 percent or more and we put none; "Brief it" opens the cell's ad brief (format spec, our proof from the brain, signal pages) and logs a CREA-C06 decision; "Next to try" line; new rule COMP-R05 puts the top 3 gaps with proof on the plan. Estimated from page-level mixes until an ad-level snapshot exists, labelled | done |
| 1.4 | Hook and offer mix (`mix.py`): heatmap of first line kinds per page against ours, offer types seen per page, the offers held in our brain; answers per gap with owner and draft: a hook bank brief (CREA-C04), an offer test for an offer we hold and never say (LIFE-C47), a no-code ad test when most of our ads push a code and direct peers run none (LIFE-C38). New rules COMP-R06, R07, R08 on the plan | done |
| 1.5 | Longest running competitor ads as signals, "use as reference" brief | todo |
| 1.6 | Price ladder and pack ladder against competitors from the brain | todo |
| 1.7 | Positioning map on the kit chart, sized by active ads, empty quadrants with an action | todo |
| 1.8 | Launches and changes timeline with follow, watch or ignore | todo |
| 1.9 | Snapshot freshness and the re-pull button with the Apify estimate first | todo |
| 1.10 | `rank` for every rule, old and new, with tests that every finding maps to an action | todo |

Round 1 notes: `snapshot.py` plans and runs a page-id Ad Library pull through `app/connectors/apify.py` (12 pages with ids, 1,800 items cap, estimate $2.08, inside the $4 run and $30 week caps). The live run was blocked by the session's permission check on 28 Sep, so round 1 builds on the brain's 28 Sep pulls (page-level formats, hook types, offers, run lengths and 3 quoted ads a page) and the page says so.

## Room jobs (JTBD)

| Job | Question | Capability | Round 0 |
|---|---|---|---|
| map every real alternative a shopper compares against, including doing nothing | who or what are we really competing with | BRAND-C18 | competitor set only; no ladder yet |
| see which corners of the market are open | where is there room nobody has taken | BRAND-C19 | positioning map, open quadrants |
| write and test the positioning statement against real shopper frames | does this positioning actually win against the alternative | BRAND-C20 | todo |
| find an unclaimed angle when no slot is open head on | is there a dimension nobody has claimed, or a reframe of the whole category | BRAND-C21 | COMP-R01, gap to own on cards |
| check whether price sits inside or outside the category's learned range | are we priced right, and is discounting undercutting us | BRAND-C24 | price tile, insight, ladder table, COMP-R02 |
| size the market and a candidate niche from the brand's own numbers | is this idea big enough to matter at our numbers | BRAND-C23 | todo |
| watch the tracked competitors for changes and alert only when it matters | what did they change this week that we should know about | BRN-C11 | todo (needs a second capture) |
| turn a verified difference into something support can actually say | what do we say when a customer asks how we compare | BRAND-C57 | todo |
| learn why an almost-buyer chose a named competitor instead | why do we lose the ones we lose, by name | BRAND-C58 | todo |
| read competitor ads, pages, reviews and Q&A as public signal | what is the market doing that we are not seeing | BRAND-C07 | what they run board, lookalike warning |

## Candidates from the room spec (pick 10 per round)

### Questions this screen should answer

- who or what are we really competing with  (BRAND-C18)
- where is there room nobody has taken  (BRAND-C19)
- does this positioning actually win against the alternative  (BRAND-C20)
- is there a dimension nobody has claimed, or a reframe of the whole category  (BRAND-C21)
- are we priced right, and is discounting undercutting us  (BRAND-C24)
- is this idea big enough to matter at our numbers  (BRAND-C23)
- what did they change this week that we should know about  (BRN-C11)
- what do we say when a customer asks how we compare  (BRAND-C57)
- why do we lose the ones we lose, by name  (BRAND-C58)
- what is the market doing that we are not seeing  (BRAND-C07)

### Metrics specified

- `competitors_tracked`: How many named competitor brands are on watch. count of active entries in the competitor set
- `price_position_index`: Where the brand's price sits versus the tracked competitors on a matched product. brand price / median competitor price for the matched product, times 100
- `price_change_count`: How many price moves the tracked competitors made. count of price changes across all competitors
- `new_creative_count`: New competitor ads detected. count of ad creatives first seen this period, per competitor
- `new_launch_count`: New products, collections or channels a competitor entered. count of new SKUs, collections or marketplace listings detected
- `positioning_openness_score`: How much of the positioning map is unclaimed. open quadrants / total quadrants on the map
- `category_ladder_coverage`: How many real alternatives, including doing nothing, are mapped. count of distinct rungs logged on the ladder
- `market_size_estimate`: How many repeat buyers at this brand's own AOV and margin would sustain the business. target profit / (AOV times margin times repeat orders per buyer per year)
- `addressable_niche_size`: Estimated demand for a candidate niche. search or category demand signal for the niche, scaled by the brand's realistic capture rate
- `win_rate_vs_named_competitor`: Share of studied almost-buyers who chose the brand over one named competitor. wins / (wins plus losses) in the win-loss sample
- `battlecard_freshness_days`: Days since a battlecard claim was last verified. today minus last verification date, per claim
- `competitor_activity_share`: Share of tracked competitor ad activity by count, as a public signal only. this competitor's new creatives / total new creatives across all tracked competitors
- `premium_signal_score`: How many premium signals the brand shows versus the category norm. count of premium signals present (packaging, guarantee, service, price anchor) / count expected for the category
- `discount_depth_vs_category`: How deep the brand discounts versus tracked competitors. brand's average discount percent minus competitor median discount percent
- `positioning_test_score`: Which of 2 positioning frames won when tested against each other. share preferring frame A minus share preferring frame B, in the test sample

### Insights specified (rules in code)

- competitor cut price sharply: a tracked competitor's price on a matched product drops more than 15 percent versus its own trailing 30-day average → "{competitor} cut the price on {product} by {pct} percent." (action BRN-C11)
- competitor tried a new angle: a tracked competitor's new creative uses a hook or product tag not seen from them in the trailing 90 days → "{competitor} is now running a new angle: {angle}." (action BRN-C11)
- competitor entered a new channel: a tracked competitor's product is newly listed on a marketplace or channel it was not on last capture → "{competitor} is now selling on {channel}." (action BRN-C11)
- open quadrant with real demand: a positioning map quadrant has zero competitors plotted and a non-zero demand signal → "No tracked brand is claiming '{quadrant}', and there is real search demand for it." (action BRAND-C19)
- price has drifted outside the category range: price_position_index falls outside the learned range (a set band around the category median) for 2 consecutive captures → "The brand's price is now {pct} percent {above_below} the category range." (action BRAND-C24)
- discounting is undercutting premium positioning: discount_depth_vs_category is positive and premium_signal_score is above the category norm at the same time → "The brand discounts {pct} points deeper than the category while claiming a premium position." (action BRAND-C24)
- the same loss reason keeps repeating: the same coded reason appears in 3 or more win-loss interviews against the same named competitor → "{n} people chose {competitor} over us for the same reason: {reason}." (action BRAND-C58)
- battlecard claim is stale: battlecard_freshness_days exceeds 90 for a claim still in active use → "The claim '{claim}' on the {competitor} battlecard has not been checked in {n} days." (action BRAND-C57)
- a lower rung of the ladder is gaining: public demand signal for a lower-commitment alternative (including doing nothing) rises faster than demand for the category itself → "Interest in '{rung}' is growing faster than interest in the category." (action BRAND-C18)

### Visuals specified

- XY positioning map (scatter plot, 2 axes): brand and every tracked competitor plotted, with open quadrants marked
- price ladder (horizontal band chart): brand and the 7 competitors' prices on a matched product, with the category range shaded
- competitor change feed (reverse-chronological timeline): new creative, price move or launch per competitor, most recent first
- category ladder diagram (vertical ladder): every rung from doing nothing up to the closest direct rival, with the brand's position marked
- battlecard table (comparison table): brand versus one named competitor, verified differences only, with a freshness flag
- win-loss reason breakdown (bar chart): count of losses to a named competitor, grouped by coded reason

### Not in the usual tools

- the positioning map plots the brand against every real shopper alternative, including doing nothing and adjacent categories, not only direct rivals
- the price audit ties price band to the category's own learned range and the brand's premium signals, not just a raw price diff
- competitor watch here reads only public signal (ads, sites, prices, launches) for the 7 brands already in this brand's gallery, and alerts only on real crossings
- win-loss research asks real almost-buyers why they chose a named competitor, producing comparison language no price or ad tool can give
- the category ladder explicitly includes doing nothing and job-based alternatives outside the obvious category
- battlecards here are gated on verified differences with a refresh cadence and a staleness flag

### Data this screen needs

- `competitor_set`: brand, competitor_name, site_url, ad_library_id, marketplace_listings, active_flag (meta_gallery competitors.json, BRAND-C07)
- `competitor_price_capture`: competitor_name, product_match_id, price, price_incl_tax (sales tax for US; GST for an India-market competitor, markets: IN), discount_pct, captured_at (price capture script (not yet built))
- `competitor_ad_capture`: competitor_name, creative_id, first_seen, angle_tag, channel, media_url (meta_gallery comp_media.json, BRAND-C56)
- `category_ladder`: brand, rung_name, rung_type (do_nothing, adjacent, direct), demand_signal (BRAND-C18)
- `positioning_map`: brand_or_competitor, axis_x_score, axis_y_score, quadrant_label (BRAND-C19)
- `battlecards`: brand, competitor_name, claim, evidence, last_verified (BRAND-C57)
- `win_loss_interviews`: brand, respondent_id, outcome (win, loss), named_competitor, reason_code, quote, date (BRAND-C58)
- `brand_own_margin_data`: brand, aov, gross_margin_pct, orders_per_repeat_buyer (store order and finance export, BRAND-C23)

## Rounds

| Round | Features picked | Date | Notes |
|---|---|---|---|
| 0 | 0.1 to 0.8 | 2026-09-28 | Bombas brain and simulated prices |
| 1 | 1.1 to 1.4 | 2026-09-28 | Plan first; rank override; 12 pages side by side; coverage matrix; hook and offer mix |
