# Phase A: the foundation, in 5 sessions

Each session is fresh. It reads `app/CLAUDE.md`, `app/contracts/` and this file. Nothing else unless named below. Fable for sessions 1, 2 and 5; Opus or Sonnet for 3 and 4. One commit per numbered item. Push after each session.

## Session 1: server and kit

First line to type: `Work in app/. Phase A session 1: build server.py and web/ per app/PHASE-A.md.`

1. `app/server.py`: serves `web/` and each `screens/<slug>/index.html`, routes `/api/<slug>/...` to that screen's `api.py`, `/api/brand` from `data/sample-brand/brand.json`, `/api/metrics/<name>` from the contract, `POST /api/decisions` appending to `data/decisions.json`. Bind 127.0.0.1 only. No credentials. Mirror the shape of `meta_gallery/server.py` (read its docstring and route table only, about 60 lines).
2. `app/web/ui-kit.css` and `ui-kit.js`: the components in `contracts/ui-kit.md`, theme-aware, phone width first.
3. `app/web/charts.js`: bar, line, step, funnel, cohort grid, drawn to scale from plain arrays.
4. `app/web/index.html`: the nav shell from `screens/INDEX.md`, the sample badge, an empty state.
Done when: `python3 app/server.py` opens a shell that lists 28 screens and any screen folder with an `index.html` renders inside it.
Status: done 25 Sep 2026. Server on port 8770, kit demo at `/web/kit.html`, tests in `tests/test_app_server.py`. Session 2 note: `server.py` reads a table from `data/sample-brand/<name>.json` (a list, or `{rows: [...]}`) or `<name>.csv`; `/api/tables/<name>` serves it.

## Session 2: the generator

First line: `Work in app/data. Phase A session 2: build generate.py per app/PHASE-A.md and app/contracts/data-sources.md.`

1. `app/data/generate.py`: from `sample-brand/brand.json` and its seed, write every table in `contracts/data-sources.md` as JSON or CSV under `data/sample-brand/`. Every table, no gaps: Kevin's call on 25 Sep 2026 is that the sample brand has every connector (Shopify, GA4, Meta, Google Ads, Klaviyo, Gorgias, reviews, Amazon, Search Console, speed runs, payouts), so every screen can show its full function to someone. The unavailable state in the kit is for real brands missing a connector, not for the demo. 13 months, weekly seasonality, a Q4 peak, ad-level rows, flows matched to orders, tickets tied to orders, reviews with quotable language, reversed orders in three legs with `rto` null for a US brand.
2. A `data/sample-brand/README.md` that lists each table, its row count and the connector it is shaped like.
Done when: running it twice produces identical files, and `server.py` can read `orders` and `sessions`.

## Session 3: the metric contract in code

First line: `Work in app/. Phase A session 3: implement contracts/metrics.md in server.py.`

1. A `metrics.py` next to `server.py` with one function per metric in `contracts/metrics.md`, each returning value, window, freshness and formula, or unavailable with the reason and the connector that fixes it.
2. `/api/metrics/<name>?window=28d` and `/api/metrics/pipeline` (all pipeline metrics with 4 trailing windows).
Done when: every metric in the contract answers, and a missing table yields unavailable, never 0.

## Session 4: the Today screen, round 0

First line: `Work in app/screens/00-today. Round 0.`

1. `index.html` and `screen.js` composed from the kit: the pipeline drawn as stages with the break marked, money at stake, 3 tiles, 2 insights as rules, the decision row.
2. `api.py`: `/api/00-today/pipeline` from `metrics.py`, `/api/00-today/top10` returning stub cards from the room spec (title, why, capability id, autonomy) until Propose exists.
Done when: opening the app shows the break for Tallgrass Goods, computed from generated data, and pressing a button lands a row in `data/decisions.json`.

## Session 5: review and publish

First line: `Work in app/. Phase A session 5: review the foundation against app/CLAUDE.md and app/contracts, then publish 00-today as a page.`

1. Check every rule in `app/CLAUDE.md` against the code: unavailable never 0, ratios from totals, US defaults, fictional badge on every page, no external writes.
2. Build a self-contained page from the Today screen with the generated data embedded and publish it, the way the speed plan was published.
3. Update `screens/00-today/FEATURES.md` round log and `app/BUILD-PLAN.md` status line.
Done when: the page is published and the round is logged.

## After Phase A

Each further screen is its own session: `Work in app/screens/<slug>. Round 0.` then `Round 1. Give me 10 candidates.` Screens in different phases can run in parallel sessions. Contract changes are their own short session at `app/`, committed first.
