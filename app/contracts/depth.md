# Depth contract: what every screen must be as an execution surface (28 Sep 2026)

ecomOS is an all-in-one e-commerce execution platform. It is not an analytics platform. A screen exists to answer one question for the brand: what do we build and do next here, and how does it get done. Numbers support that answer. They are never the answer.

This contract is the standard every screen must meet from round 1. It sits beside `audit.md` (findings), `metrics.md` (numbers), `ui-kit.md` (components) and `brand-brain.md` (the brain). The Meta gallery Kevin built for Gehna (`meta_gallery/web/`) is the reference for depth and for how a marketer reads a page and acts. Its rules are folded in below.

## 1. The frame

The brand brain holds who we are. Each screen turns that into things to ship. The orchestrator ranks them across screens. The agents ship them. The founder approves.

A screen is the best person in the world at that job, handed over as a tool: a world-class market researcher, media buyer, CRO lead, CX head. Ask what that person would put in front of the founder on Monday morning, and what they would have their team do by Friday. That is the screen.

An element that only shows a number is not finished. It is finished when it says what to do, who does it, and how.

## 2. Sections a screen has, top to bottom

Every screen has these sections in this order. Names can change; the order and the content cannot. A screen may use tabs for jobs inside sections 5 and 6, never to hide sections 1 to 4.

| # | Section | What it holds | Kit form |
|---|---|---|---|
| 0 | Head | One line: what this screen ships for the brand. The simulated-data badge. Window and freshness. | `.screen-head`, `UI.sampleBadge` |
| 1 | The plan | This screen's next moves: its top 5 to 10 ranked actions, each with title, why in one sentence with the number, owner, stake, rubric total and the decision row. Orientation numbers sit beside the title, small: 3 to 6 numbers that tell the operator where the domain stands (spend, ROAS, CVR, freshness). No tile row above the plan. | `UI.planBoard`, `UI.orientation` |
| 2 | What is wrong, ranked | The audit's open findings for this domain, grouped by bottleneck or stage, severity first. Each finding shows the sentence, the evidence numbers with their baseline and window, confidence, and links to the action that fixes it. | `UI.insight` in a grouped list, or `UI.verdictTable` |
| 3 | Actions | One action card per ranked action: title, why, rubric scores, owner, artefact, time to ship, decision row. Expanding a card shows the implementation block. | `UI.actionCard` |
| 4 | Implementation | For every action: owner (agent does it, agent drafts and a person approves, person does it), the numbered steps with who does each step, the artefact it produces (an ad brief, a page section, an offer spec, an email draft, a test brief, a listing fix, a connector setup), the win rule, the stop rule and the check-again date. When the artefact can be drafted from the brain and the data, the draft is shown here, not described. | inside `UI.actionCard`, or `UI.panel` |
| 5 | The desk | The domain's deep work: the matrices, maps, cohort grids, waterfalls and tables a strategist reads to find the next gaps. Every desk section ends in a line that names the gap and offers the action for it. This is where most of the round-by-round features land. | coverage matrix, positioning map, verdict table, cohort grid, waterfall, trend strip |
| 6 | The audit | The full findings table for this screen with rule ids, and the rule list: what each rule reads, its threshold, its capability, what makes it readable. Resolved findings for 28 days. | `UI.table`, `UI.verdictTable` |
| 7 | Notes and exports | Team notes on entities, CSV of any table, copy brief on any action, print. | `.btn`, `UI.panel` |

The first 1280 by 800 view of a screen shows the plan and the orientation numbers. If a reader has to scroll to learn what to do next, the screen fails.

## 3. Checkable rules: a world-class operator learns something and can act on it

A feature is done when every rule below holds. Tests check the ones marked T against the api and the page.

1. **Plan first.** (T) The first component in the page body after the head and the badge is the plan board. No tile grid, chart or table precedes it.
2. **Every action has an owner, steps and an artefact.** (T) `rank` returns actions where `owner` is one of `agent`, `agent_drafts`, `person`; `steps` has 2 to 8 entries each with `who`; `artefact.kind` is set. An action missing any of these is not returned.
3. **Every finding ends in an action.** (T) Every open or unavailable finding id from `audit.run` appears in the `finding_ids` of at least one action from `rank`. An unavailable finding maps to a connect action with owner `person`.
4. **The rule and the numbers are visible.** (T) Every recommendation shows the metric, the value, the baseline or threshold, and the window. A sentence with a number whose evidence row is missing fails the audit contract and this one.
5. **Sized, with a stop rule.** An action that changes money or traffic gives the size (dollars a day, percent, count) and a stop or check-again rule with a date or a count. "Raise budget" fails. "Raise Comfort prospecting from $820 to $980 a day. Check on 5 Oct. Stop if CPA passes $110 for 3 days." passes.
6. **Done from where it appears.** (T) Every action card and plan item carries the decision row and at least one of: copy brief, make it (opens the draft), add to tests, open entity, export. A finding without a button is a report.
7. **Unavailable is never zero.** (T) A null value renders as "unavailable" with a reason. A chart breaks at the gap. A rubric dimension with no input shows "n/a" and is scored at the neutral value, written down.
8. **Simulated is labelled once per page** (T) at the top, never in every sentence, and every evidence row carries `simulated: true` until a real connector fills it.
9. **Gaps, not only totals.** Every desk section shows at least one of: what was never tried (an empty cell), a cross-source check (platform number next to store number), or a position against competitors. Totals of what happened are orientation only.
10. **Reads in one pass.** Section headings are imperatives or questions in plain words ("Stop paying for 3 ad sets", "Which angles have we never run on video?"). Under each heading one line states the window and the rule in numbers. Under each block one small line states the caveat.
11. **Brand content, fixed structure.** (T) No brand fact, competitor name, price, claim or threshold is written in a screen's JS or HTML. Everything comes from the brain (`/api/05-brand-brain/...` or the brain store through the screen's api) and the data layer. The same page must render for another brand with only its brain and tables swapped.
12. **Short words.** Sentences under 20 words, digits, "percent", "$3,120", no em dashes, no "should", "consider", "leverage". Below tenth-grade reading level. Never GPT or .env on a page.
13. **Deterministic.** (T) `rank` on the same tables, brain version and window returns the same actions in the same order. No model call in `rank` or `audit.run`. Drafts that need a model are produced by a capability the founder approved, and marked as drafts.
14. **The founder can disagree.** Every plan item and action has "Not now" and it snoozes the finding 14 days through the decisions log. The decision shows on the item with its date.

## 4. The rubric

Each action is scored in code on six dimensions, 0 to 5 each, from fields that already exist. Weights are fixed across screens so the master list compares like with like. No model scores anything.

| Dimension | Weight | Score rule (0 to 5) |
|---|---|---|
| Revenue impact | 30 | From `money_at_stake.usd_revenue` (or `usd` when no margin) as a share of trailing 28-day net revenue: 5 at 5 percent or more, 4 at 2, 3 at 1, 2 at 0.5, 1 above 0. No money: by severity, critical 4, high 3, medium 2, low 1. |
| Profit impact | 20 | Same ladder on `money_at_stake.usd` when it is margin. When only revenue is known, revenue score minus 1 (floor 1). Cost-side entities (returns, chargebacks, fees, shipping, inventory) score revenue score plus 1 (cap 5). |
| Brand reputation | 15 | 5 for a forbidden or unapproved claim live, a legal disclosure gap, a broken policy promise, or a competitor position gap named in the brain. 4 for a review theme in a deal-breaker rung. 3 for copy, creative or positioning findings. 2 for site quality. 1 otherwise. |
| Customer satisfaction | 15 | 5 for a break in the buy or delivery path (checkout, speed on mobile, stock-out on a hero SKU, ticket backlog). 4 for returns and CX themes. 3 for email and post-purchase. 2 for acquisition-side findings. 1 otherwise. |
| Ease | 10 | 5 when owner is `agent` and no connector is missing. 4 for `agent_drafts`. 3 for `person` with the artefact drafted. 2 for `person` with steps only. 1 when a connector must be set up first. |
| Confidence | 10 | `confidence` from the finding times 5, rounded. |

`total` = sum of weight times score divided by 5, so 0 to 100. Ranking: `critical` findings pin to the top in stake order, then by `total`, then severity, then `money_at_stake.usd` (null last), then days open, then upstream position (reach before sessions before checkout). The dimension scores are shown on every action as six small boxes with the total. Ties are visible; the founder breaks them.

A screen may raise reputation or satisfaction for a specific rule by writing the override in its `audit.py` docstring next to the rule. It may not change the weights.

## 5. The rank route

Every screen exposes `GET /api/<slug>/rank?brand=bombas&window=28d`. The orchestrator on the brand brain screen calls all 28 and merges them into the master list at `GET /api/05-brand-brain/master`.

A screen gets the route for free: `app/rank.py` turns its `audit.run` findings into actions with the rubric, a default owner from the capability's autonomy, default steps by artefact kind, and a connect action for each unavailable finding. A screen overrides by exporting `rank(brand, window)` from its `api.py` (or `audit.py`) that returns richer actions: better titles, real steps, a drafted artefact, a merged action for several findings. The override must keep the shape and pass the same tests.

```json
{"screen": "11-paid-social", "brand": "bombas", "window": {"ends_on": "2026-09-27", "days": 28},
 "computed_at": "2026-09-28T09:00:00Z", "brain_version": "a1b2c3d4e5f6", "simulated": true,
 "actions": [{
   "id": "11-paid-social.PAID-R03.adset_23847",
   "finding_ids": ["11-paid-social.PAID-R03.adset_23847"],
   "title": "Refresh the 3 ads in Prospecting, Comfort angle",
   "why": "Frequency is 4.6 against a median of 2.1. Cost per order is up 62 percent this week.",
   "severity": "high", "status": "open", "confidence": 0.8,
   "entity": {"type": "adset", "id": "23847", "label": "Prospecting, Comfort angle"},
   "capability": {"id": "CREA-C15", "autonomy": "agent_does"},
   "owner": "agent",
   "artefact": {"kind": "ad_brief", "label": "3 ad briefs with hooks from the durability ladder", "draft": null},
   "steps": [{"n": 1, "who": "agent", "text": "Pull the 3 ads' hooks and the durability ladder rungs."},
             {"n": 2, "who": "agent", "text": "Write 3 briefs: new first line and first frame, same product and offer."},
             {"n": 3, "who": "person", "text": "Approve the briefs. Creative makes them."},
             {"n": 4, "who": "agent", "text": "Check frequency and CPA on 5 Oct. Stop if CPA passes $110 for 3 days."}],
   "size": {"text": "$8,150 a week at stake", "usd": 3118},
   "stop_rule": "CPA above $110 for 3 days", "check_on": "2026-10-05", "time_to_ship_hours": 6,
   "rubric": {"revenue": 3, "profit": 2, "reputation": 3, "satisfaction": 2, "ease": 5, "confidence": 4, "total": 58},
   "money_at_stake": {"usd": 3118, "formula": "spend_7d - (purchases_7d * cpa_median_4w)", "window": "7d"},
   "brain_refs": ["bombas.learnings.fatigue_threshold_2026_09"],
   "decision": null}]}
```

Owner values: `agent` (agent does it, reports back), `agent_drafts` (agent drafts, a person approves before anything ships), `person` (a person does it from the steps; the agent prepares what it can). The default is autonomy `agent_does` to `agent`, `founder_gate` to `agent_drafts`, `human_assist` to `person`. Any external write is `agent_drafts` at most until Kevin lifts it.

Artefact kinds: `ad_brief`, `creative`, `copy`, `page_section`, `landing_page`, `offer`, `price_change`, `email`, `flow`, `test_brief`, `listing_fix`, `feed_fix`, `budget_move`, `bid_change`, `connector_setup`, `brain_record`, `policy`, `research_note`, `ticket`, `report`. A screen that needs another kind adds it here in a contract commit.

The master list merges by `id`, keeps one action per finding, applies snoozes from `decisions`, ranks by section 4, and returns `top` (the 10 open actions to approve), `connect` (the unavailable findings as connect actions, ranked the same way, shown as their own strip so a missing connector never crowds out work that can start today), and `bottlenecks` (one group per screen: open, unavailable, critical, stake, score, the top action) so the brain screen can show "bottlenecks ranked, unlocks under each, the 10 to approve". A screen's own plan board follows the same split.

## 6. Visual vocabulary and when each form is right

Use the form the question needs. One form per question. Every form ends in an action line.

| Form | Right when | Wrong when | Kit |
|---|---|---|---|
| Plan board | The top of every screen and the master list: ranked moves with owner and decision. | Anywhere below section 1. | `UI.planBoard` |
| Action card | An action needs its rubric, steps and artefact in view. | Listing more than 10 at once (use the verdict table). | `UI.actionCard` |
| Decision row | Every action and plan item. | On an orientation number. | `UI.decisionRow` |
| Coverage matrix | Two categorical dimensions and a coverage question: angle by format, avatar by channel, keyword group by page, SKU by marketplace. Us against them in each cell. Empty cells are the gaps and carry the "make it" button. | One dimension (use bars) or a measure over time. | `UI.coverageMatrix` |
| Verdict table | Many entities each needing a verdict and a reason: ads, campaigns, pages, SKUs, flows, keywords. Sortable, verdict chip, reason column, action column. | Fewer than 4 rows. | `UI.verdictTable` |
| Positioning map | Where we sit against competitors or where avatars sit against what we serve: two axes from the brain, points labelled, empty quadrants named as gaps. | Axes that are not in the brain or not comparable. | `Charts.positioningMap` |
| Waterfall | A total that decomposes into steps: revenue bridge month to month, margin from price to contribution, budget moves from cut to grow, a fee stack. | A share (use a stacked bar). | `Charts.waterfall` |
| Cohort grid | Behaviour of a group over time since a start: repeat purchase, LTV, retention, subscription survival. | Fewer than 3 cohorts. | `Charts.cohort` |
| Trend strip | Many metrics need orientation in little space: sparkline, last value, change, in rows. Orientation only. | The main content of a section. | `Charts.trendStrip` |
| Funnel | Stage to stage drop with the break marked. | Steps that are not sequential. | `Charts.funnel` |
| Heatmap | Two dimensions and one measure with no us against them: format by age, category by month. | Coverage questions (use the matrix). | `UI.coverageMatrix` with `single: true` |
| Bar and line | One measure over categories or time, with the benchmark drawn. | More than 6 series. | `Charts.bar`, `Charts.line`, `Charts.step` |
| Timeline | Decisions, changes, launches, with the result after each. | Metrics over time. | `.timeline` |
| Phased plan table | A plan by dates: festive ramp, launch, migration. | A single action. | `UI.table` |
| Side panel | One entity's full detail and its actions without leaving the list. | Primary content. | `UI.panel` |
| Filmstrip | Speed before and after, one clock. | Anything not visual over time. | `UI.filmstrip` |
| Printable report | Client or weekly report with plain words. | Working screens. | `@media print`, `report` artefact |

Chart rules: tabular numbers, benchmark line dashed in the warn colour, the selected window shaded, null breaks the line and hatches the bar, a legend only above one series, one note under every chart stating the caveat. Charts read the tokens, never hard-coded colours. Us is `--us`, them is `--them`, series are `--s1` to `--s6` in order.

## 7. Anti-patterns from round 0

These fail review. Managers remove them before adding features.

- **A report.** Head, tiles, insights, chart, table, in that order, with nothing to do. Move the plan to the top and give every block an action.
- **Tiles without a next step.** A KPI row that the eye reads and moves on from. Tiles are orientation only, small, beside the plan.
- **Findings without an owner.** "Add to cart rate is down" with no card that says who fixes it and how.
- **Charts for their own sake.** A records-per-day bar, a spend line with no benchmark, a pie. If removing the chart changes no decision, remove it.
- **Long prose.** Paragraphs a founder must read to find the point. Use section, line, number, button.
- **Buttons that lead nowhere.** A capability id on a chip with no decision row and no artefact.
- **Brand facts in code.** A competitor list, a threshold or a price written in screen.js. Read the brain.
- **Zero for unknown.** A 0 percent that means the connector is not there.
- **One voice for every screen.** Round 0 screens look and read the same. Each screen is its own expert desk: the paid social desk has verdicts and budget moves, the research desk has maps and trends, the CX desk has themes and tickets. Same kit, different work.
- **Asking the founder to pick features.** Build 10, ship, build the next 10.

## 8. Plug and play

Structure is fixed. Content comes from the brain and the data layer only.

- A screen reads brand identity, positioning, products, offers, policies, claims, competitors, avatars and thresholds from the brain through its api. Founder edits on the brain screen write approved records that win the merge, and every screen shows the new value on its next load.
- A screen reads numbers through `app/metrics.py` and the tables in `data-sources.md`. When a real connector fills a table, nothing in the screen changes.
- Rules, thresholds and rubric scores live in code with the brain record they read named in `brain_refs`. A threshold the brand can tune is a brain record (`learnings` or `plans`), not a constant.
- Ideas come from the web pass first, then the idea bank (`python3 scripts/ideas.py`), then the inspiration layer. A screen stores what it took from the bank by idea id, never a copy.
- Simulated data is labelled once per page from `brand.fictional`. A live brand shows "live data, read-only".
- Tests for a screen run against the Bombas brain and tables and against a second brand folder when one exists. A screen that only works for Bombas is not done.

## 9. How a manager applies this each round

1. Read the screen's round 0, list the anti-patterns present, fix them in the first commit of round 1 (plan board at the top, orientation beside it, actions with owner and steps, audit at the bottom).
2. Build `rank` for the screen: real titles, steps and artefacts for every rule the audit has. Add the rules the room spec lists that round 0 skipped.
3. Then build the desk, 10 features a round, each ending in an action line. Screenshot each round at 1280 wide.
4. Each feature is judged by one question: does a world-class operator learn something they could not see before, and can they act on it from here.
