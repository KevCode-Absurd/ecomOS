# Customers and avatars: hand-off

For Kevin and the next session on this screen. Written 28 Sep 2026 after 10 rounds, brought up to date after round 11. `FEATURES.md` has every feature by round; this note says how the screen works and what to do next.

## What the screen does

It answers who buys, why they buy, what stops them, and what to build next for each avatar. Every block ends in a move with an owner, steps, a drafted artefact, a size, a stop rule and a check date.

The page reads top to bottom:
1. The plan: the top 10 moves, with 6 orientation numbers beside the title.
2. Connect first: rules that wait on a data source, kept apart from the plan.
3. What is wrong: every finding, grouped by rule.
4. Actions, the next 30 days, proposed tests, decisions, hand-off packs and the inbox of what other screens ask of us.
5. The desk, in 5 tabs: Avatars, Doubts and words, Offers and claims, Retention, Brand and voice.
6. The audit: every rule and finding.

## Files

- `api.py`: the routes, the cached overview and rank, the plans behind each action.
- `audit.py`: 34 rules, CUST-R01 to CUST-R34. Each rule is described in the module docstring.
- `builds.py`: pure builders. Every threshold is a named constant here, with a comment.
- `screen.js`, `index.html`, `screen.css`: the page. No threshold or brand fact lives here.
- `fixtures/sku_lines/<brand>.json`: the local SKU to product-line map.
- `tests/test_screen_customers_avatars.py`: about 200 tests, including a browser smoke test.

## Routes

All under `/api/02-customers-avatars/`, all take `?brand=` and `?today=`.

- `overview`, `rank`, `audit`, `report`, `agenda`, `tests`, `handoff`, `avatar/<key>/brief`.
- Writes: `voice/examples`, `avatars/draft`, `messaging/approve`. `voice/check` writes nothing.
- The page takes `?brand=<slug>` too, and passes it to every call.

## Hand-offs and decisions

- **Sending.** Each pack is also a list of rows in the shared hand-offs table's shape (`events.md`). "Send N to <team>" posts the rows that team does not already have from this screen. The row carries the move's why, stop rule, check date, owner, capability and id. This screen never edits a row once posted.
- **The inbox.** Rows other screens send to this screen, or to the brand or customers team, show under "What have other screens asked of us?". Each has its draft and a decision row keyed to the hand-off's id.
- **Decisions by brand.** `api.decisions_for` reads only this brand's decisions; a row with no brand is the default brand's, as the server reads it.
- **Every block acts.** An unavailable block shows "Fill this block": the drafted move that gets its input.

## How the numbers are made

- **Orientation.** New customers and returning share come from the daily table over 28 days. Repeat in 3 months comes from the latest full cohort. Money at stake sums the open moves that carry a stake.
- **Avatar share.** From reviews first. With 385 survey answers or more, from the survey. Where neither gives one, from sales by line.
- **Share of sales by line.** Each line's sales over 12 full months, split across avatars by their share of that line's linked reviews.
- **Focus score.** Share 40, served poorly 30, no ads 20, open doubts 10, out of 100.
- **Return risk.** From the lines an avatar buys, each line's bad-review share, and its fit or wear complaints.
- **Money at stake.** Only against the brand's own history, never a target.
  - CUST-R07: paid share of returning orders above its own 12-month median.
  - CUST-R08: a retention cliff against the same month last year when the monthly table has it, else against a normal month.
  - CUST-R09: the fall at the age break above the median fall at other ages.
  - CUST-R32: a weak cohort's gap to the median repeat.
  Each stake carries its formula and inputs, so anyone can redo it.
- **Size and stop rule.** Every move that spends money or changes a page has a size from its finding, a stop rule and a check date.
- **Drift in what buyers say.** Each theme's share of praise and complaint reviews, the last 180 days against the 180 before, from dated public reviews. Worse at 5 points with 10 or more mentions; watch with 5 to 9.
- **Mystery shopper run sheet.** 8 checkpoints, each against the brain fact it must match. Message pretests put our line against one in the avatar's own words.

## Thresholds a brand can tune

A `learnings` record with field `threshold_<name>` and a number sets one of 12 thresholds, inside fixed bounds. The list is `builds.TUNABLE`. Anything out of bounds is ignored.

## Contract asks, and what to change when each lands

- **`survey_answers` table.** `audit.load_survey_answers` already reads it by name. Delete nothing; the fixture path stops being used.
- **`customer_paths` aggregate.** `audit.load_paths` reads it. The shape is `builds.PATHS_SHAPE`. The paths block and its rules fill with no page change.
- **SKU to product-line map in the brain.** Point `audit.load_line_sales` at the brain map, then delete `fixtures/sku_lines/`.
- **Tickets and returns by reason and line.** Replace the review proxy in `builds.return_risk` with real return reasons. Keep the proxy as the fallback.
- **Pack prices in the brain offers.** `builds.price_doubts` then fills the per-pair price at each pack.
- **`last_year` baseline kind in `audit.md`.** Change CUST-R08's evidence from `threshold` to `last_year`.
- **An `avatar` entity type in `audit.md`.** Change avatar findings from type `brand` to `avatar`.
- **Angle and avatar tags per ad in `ad_rows`.** CUST-R03 and the ads column in coverage start counting. The naming convention is in the Avatars tab.
- **`situations` brain record per category.** Replace `builds.SITUATIONS` with the record.
- **A `brand` field on hand-off rows.** Drop the default-brand guard in `sendButton` in `screen.js`.
- **The kit's decision row sends `brand`.** Pass the brand from the page; `decisions_for` already reads it.
- **`shopper_runs` and `pretests` tables.** Read results into `builds.shopper_run` in place of `result: None`, and let CUST-R34 resolve once a run is on file.

## Still open

- **Drift of our own assets.** Buyer drift is read. Our site, ads and email need a dated scan each quarter; the scan plan is drafted in the drift block.
- **Shopper and pretest results.** The run sheet and pretests are drafted; results wait on their tables.
- **Trademark, domain and handle watch.** Only lookalike pages from the Ad Library are read.
- **The master list.** None of this screen's moves is in the top 10 today. The sample data is smooth, so no rule shows a money gap against its own past. Real data will change that.

## How to check the screen

- `python3 -m unittest tests.test_screen_customers_avatars -v` runs everything, the browser test included when Playwright is there.
- `python3 app/server.py --port 8770`, then open `/screens/02-customers-avatars/`. Add `?brand=example` for the second brand.
- After a change to `rank`, restart the server: `app/rank.py` caches the screen's module.
