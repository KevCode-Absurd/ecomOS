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
| every screen | briefs handed to a team or another screen | `handoffs` | 09-creative, 10-copy, 07-landing-pages-cro, 14-email-messaging, 00-today |
| 25-experiments | read results and learnings | `registry` | 00-today, 26-reports, every screen's priors |

**Experiment registry (25-experiments, 28 Sep 2026).** One row per test, keyed `id` (`EXP-nnn`, stable) and `brand`. Fields: `hypothesis` (one sentence), `source` `{type, ref, index}` (the brain record, bank idea or finding it came from), `idea_id` (bank id or null), `owner`, `metric` `{name, direction, min_days, registered_on, reason?}` or null (name is a `metrics.md` metric; `registered_on` must be on or before `start`), `variant` `{control, treatment}`, `audience` (list of tags, used for the overlap check), `start`, `read_point`, `end` (dates or null), `status` (`proposed`, `running`, `parked`, `done`), `result` `{read_on, direction up|down|flat|unreadable, lift, unit, note}` or null, `decision` `{choice roll_out|keep|kill|not_now, on, by, rolled_out_on}` or null, `learnings_ref` (the brain `learnings` record written back, or null), `retro` (text or null), `park` `{reason, expires}` or null, and `brain_refs` (brand record ids the test read or touched). Any screen appends a row with status `proposed` when a decision approves a test; only 25-experiments sets results. Until the shared `registry` table exists the seed lives in `screens/25-experiments/fixtures/registry.json` (simulated). Audit rules EXP-R01 to EXP-R10 are owned by 25-experiments.

**Hand-offs (lead, 28 Sep 2026).** `data/handoffs.json`, append-only, served at `GET /api/handoffs` (filters `from_screen`, `to`, `status`, `kind`) and `POST /api/handoffs`. One row per brief a screen hands over: `from_screen` (slug), `to` (a team such as `creative`, `copy`, `landing pages`, `email`, `cx`, or a screen slug), `kind` (an artefact kind from `depth.md` section 5), `title`, `why`, `draft` (the artefact text, up to 20 KB), `win_rule`, `stop_rule`, `check_on`, `capability`, `owner` (`agent`, `agent_drafts`, `person`), `finding_id`, `status` (`proposed`, `decided`, `done`, `dropped`), `time`, and a server-set `id` (`HO-` plus 10 hex). A screen posts a row when a decision approves a brief; the receiving screen reads its rows by `to` and never edits another screen's rows. `MAX_BODY` for POST is 8 MB, so a brain export or a draft travels in one request.
