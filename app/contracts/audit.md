# Audit contract (S3.1, 28 Sep 2026)

Every screen ships an `audit.py`. It turns the metric contract and the brain into findings: where this screen's part of the pipeline is broken, with proof, money at stake and the capability that fixes it. Findings are the only input Propose reads to build the top 10. Diagnose (`agents/loop/DIAGNOSE.md`) ranks stages across screens the same way and adds nothing an audit did not find. No audit proposes a fix; the capability id is a pointer, not advice.

## 1. The finding record

One JSON object per finding. Field order is the order a founder reads it.

| Field | Type | Rule |
|---|---|---|
| `id` | string | `<screen>.<rule_id>.<entity_id>` (section 4). Stable across runs. |
| `screen` | string | screen slug, for example `11-paid-social`. |
| `rule_id` | string | `<SCREEN>-R<nn>`, defined in the screen's `audit.py` docstring with its threshold and source. |
| `severity` | enum | `critical`, `high`, `medium`, `low` (section 2). Never `info`; a rule with nothing to say emits no finding. |
| `entity` | object | `{type, id, label}`. type is one of `brand`, `stage`, `page`, `device`, `sku`, `campaign`, `adset`, `ad`, `flow`, `offer`, `ladder_rung`, `metric`. |
| `evidence` | list | rows of `{metric, value, unit, window, ends_on, freshness_days, baseline, baseline_kind, source, simulated}`. Every number the sentence quotes appears here. `baseline_kind` is `own_median` (4 trailing windows), `peer_band` (benchmarks file, by store tags) or `threshold` (rule constant). |
| `sentence` | string | what the founder reads, section 7. |
| `capability` | object | `{id, autonomy}` from `agents/catalogue.json`; autonomy is `agent_does`, `founder_gate` or `human_assist`. One capability per finding. A second one is a second finding. |
| `money_at_stake` | object or null | `{usd, formula, inputs, window}` per section 3, or null with `money_reason` when not computable. |
| `confidence` | number | 0 to 1, section 2. |
| `brain_refs` | list | brain record ids the rule read or the fix needs (section 5). |
| `first_seen`, `last_seen` | date | section 4. |
| `status` | enum | `open`, `resolved`, `unavailable`, `snoozed` (section 4). |
| `unavailable` | object or null | `{inputs, connector, fix}` when status is `unavailable`. |

Example (evidence trimmed to one row):
```json
{"id": "11-paid-social.PAID-R03.adset_23847", "screen": "11-paid-social", "rule_id": "PAID-R03",
 "severity": "high", "entity": {"type": "adset", "id": "23847", "label": "Prospecting, Comfort angle"},
 "evidence": [{"metric": "frequency", "value": 4.6, "unit": "x", "window": "7d", "ends_on": "2026-09-27",
   "freshness_days": 1, "baseline": 2.1, "baseline_kind": "own_median", "source": "ad_rows", "simulated": true}],
 "sentence": "This ad set has shown the same 3 ads 4.6 times per person this week. Cost per order is up 62 percent.",
 "capability": {"id": "CREA-C15", "autonomy": "agent_does"},
 "money_at_stake": {"usd": 3118, "formula": "spend_7d - (purchases_7d * cpa_median_4w)", "inputs": {"spend_7d": 8150, "purchases_7d": 61, "cpa_median_4w": 82.5}, "window": "7d"},
 "confidence": 0.8, "brain_refs": ["bombas.learnings.fatigue_threshold_2026_09"],
 "first_seen": "2026-09-24", "last_seen": "2026-09-27", "status": "open", "unavailable": null}
```

## 2. Severity and confidence

Severity is set by the rule from money and reach, never by a model.

| Severity | Definition | Propose treats it as |
|---|---|---|
| `critical` | Revenue is being lost now and the loss grows daily: a broken step in the buy path, a stock-out on a hero SKU, spend on an ad set with no purchases for 3 days, a failed flow. Or money at stake over 5 percent of trailing 28-day net revenue. | must be in the top 10 |
| `high` | A stage is below its own median or peer band with 2 or more windows agreeing, or money at stake over 1 percent of trailing 28-day net revenue. | ranks by stake |
| `medium` | One window below baseline, or a gap with no money formula yet but a known downstream cost (a missing proof, a missing flow). | ranks by stake, then confidence |
| `low` | Hygiene: naming, tracking gaps that do not yet change a number, a record past its shelf life. | listed, rarely in the top 10 |

Confidence is computed, not judged: 0.9 when 4 trailing windows agree and the input is fresh (under 2 days), 0.7 for 2 to 3 windows, 0.5 for 1 window, minus 0.2 when any evidence row is `sampled`, `thresholded` or past its freshness rule in `data-sources.md`, minus 0.2 when the baseline is a `peer_band` rather than the brand's own history. Floor 0.1. A finding with confidence under 0.3 keeps its severity but is labelled "weak evidence" on screen.

## 3. Money at stake

Reuses `money_at_stake` from `metrics.md`: (baseline minus current) times volume at the stage times downstream value per unit, for the current window. The audit fills the three terms from its own evidence rows and writes the formula it used as text plus the inputs as numbers, so a founder can redo the arithmetic. Rules:

- Baseline is the brand's own trailing median when 4 windows exist, else the peer band midpoint, else null. No baseline, no money: `money_at_stake` is null with `money_reason: "no baseline"`.
- Downstream value per unit comes from the metric contract for the window: a session is worth `cvr_overall × aov`, an add to cart is worth `checkout_rate × order completion × aov`, an order is worth `aov`, a paid dollar is worth `period_roas`. Never a hard-coded number.
- Stake is never negative. A stage above baseline gives no finding.
- Stake uses net revenue, not contribution margin, unless `finance_inputs` has margin for the window. Then both are written, `usd` is margin, and `usd_revenue` is added.
- Any input unavailable makes the whole stake null, never a partial sum.

## 4. Identity, dedupe and status

- `id` is `<screen>.<rule_id>.<entity_id>`. Same rule and same entity means the same finding, across runs and across screens. When 2 screens can emit the same rule on the same entity (fatigue on an ad set from 09-creative and 11-paid-social), one screen owns the rule; the other reads it from the findings table. Ownership is written in the rule docstring and in `events.md`.
- A run reads the findings table, matches by `id`, keeps `first_seen`, sets `last_seen` to the window end and overwrites everything else.
- A finding not emitted on a run whose inputs were available flips to `resolved` with `resolved_on`. It stays 28 days, then archives. If it fires again it reopens with a new `first_seen` and the old episode is kept as history.
- A rule whose inputs are missing emits one finding with status `unavailable`, severity as the rule would give if it fired, evidence empty, `unavailable.inputs` naming the tables or columns, `unavailable.connector` naming what fills them and `unavailable.fix` the plain-English step. It is never a 0 and never `resolved`.
- `snoozed` is set only by a founder decision in `decisions` (choice `not_now`) and expires after 14 days.
- A run is deterministic: same tables, same brain version, same window, same output byte for byte. No model call inside `run`. Wording is a template per rule, filled in code.

## 5. References to the brain

- `brain_refs` holds record ids as `brand-brain.md` defines them (`<brand>.<section>.<key>`). Never a copy of the record.
- A rule that reads a brain value (a fatigue threshold in `learnings`, a promo date in `offers`, a red line) lists that record so a stale record explains a stale finding.
- When the fix is copy or an offer, the finding names the `objection_ladders` record and the rung: `brain_refs` carries `bombas.objection_ladders.durability` and `entity` is `{type: "ladder_rung", id: "durability.deal_breaker"}`. The evidence rows carry the rung's counts by star and source.
- A brain record past its shelf life is evidence for a `low` finding on screen 05, not a reason to skip the rule.

## 6. What Propose reads

Propose ranks the top 10 from these fields only, in this order: `severity`, `money_at_stake.usd` (null sorts last inside a severity), `confidence`, days open (`last_seen` minus `first_seen`, older first), then how far upstream the stage sits (reach before sessions before checkout). It never rereads tables. A finding with status `unavailable` is ranked at its severity, so a missing connector can make the top 10 as "connect X". `snoozed` and `resolved` findings are excluded.

## 7. Founder-facing wording

From `app/CLAUDE.md`. The sentence is 2 sentences at most, under 40 words. Short sentences, digits, plain words, no jargon, no em dashes. It names the entity, the number, the baseline and since when. It states what is happening, not what to do. No "should", "try", "consider". Percent is written "percent". Money is "$3,120". Simulated data says so once at the top of the screen, not in every sentence. Never mention GPT or .env.

## 8. The interface

```python
def run(brand: str, window: Window) -> list[Finding]: ...
```

`Window` is `{ends_on, days, trailing}` per `metrics.md`; `ends_on` is the last full day in the brand's timezone. `run` reads only `app/data/` and `app/brain/<brand>/`, calls `app/metrics.py` for every number, never a connector and never a model. It returns findings sorted by severity then stake. The server writes them to the `findings` table with `computed_at` and the brain version, and every screen and Propose read from there. `audit.py` also exposes `RULES`: a list of `{rule_id, name, entity_type, inputs, capability, owner_screen}` so screen 22 can list every rule and what makes it readable.

## 9. Worked examples

**Paid social: fatigue on an ad set.** Rule PAID-R03 on screen 11. Inputs: `ad_rows` for the ad set, 7 days ending 27 Sep, plus 4 trailing 7-day windows. Frequency 4.6 against own median 2.1; CPA $134 against median $82.50; purchases 61. Two windows agree, data 1 day old, not sampled: confidence 0.8. Stake: spend 7d minus purchases times median CPA, $8,150 minus 61 × $82.50 = $3,118, formula and inputs written in. That is under 1 percent of trailing net revenue, but 2 windows agree, so `high`. Capability CREA-C15 (diagnose creative fatigue, agent does). Sentence: "This ad set has shown the same 3 ads 4.6 times per person this week. Cost per order is up 62 percent." Brain ref: the learnings record that set the fatigue threshold. Dynamic creatives in the ad set are flagged in evidence, never split.

**CRO: mobile checkout break.** Rule CRO-R07 on screen 07. Inputs: `sessions` by device for 28 days ending 27 Sep. Mobile checkout to purchase 31 percent against own median 47 percent and desktop 49 percent; 4 windows agree; one day sampled, so confidence 0.9 minus 0.2 = 0.7. Stake: (0.47 minus 0.31) × 9,400 mobile checkouts × $58 AOV = $87,232, over 5 percent of trailing net revenue, so `critical`. Capability SITE-C44 (build and QA pages mobile-first, agent does; the deploy behind it is founder gated in the catalogue). Sentence: "Mobile shoppers who start checkout finish it 31 percent of the time. Desktop is 49 percent and mobile was 47 percent until 3 Sep." Entity `{type: "device", id: "mobile"}`. If `speed_runs` has a mobile checkout run in the window, its LCP is an extra evidence row; if not, the row is absent, not 0.

**Offers: a deal-breaker rung with no proof.** Rule OFFER-R04 on screen 04. Inputs: `objection_ladders` records where the last rung's `proof` is empty or "no public proof", and `reversed_orders` reasons matching the theme. Durability ladder: deal-breaker rung has 31 one-star mentions across 2 sources and no proof; returns with reason `wore through` are 14 in 28 days, own median 9. Money: 14 minus 9 returns × $58 AOV × 0.7 return cost share from `finance_inputs` = $203, but the rung's lost orders cannot be counted, so `money_reason` says "proof gap: returns only, lost orders not measurable" and the value is written as a floor. One window on returns, ladder fresh: confidence 0.5. Severity `medium`. Capability LIFE-C36 (design the offer's value proposition, founder gate). Sentence: "31 one-star reviews say socks wore through and nothing on the site answers it. Returns for wear are 14 this month, up from 9." Entity `{type: "ladder_rung", id: "durability.deal_breaker"}`, brain ref `bombas.objection_ladders.durability`. When the ladder is rebuilt and the rung gets proof, the finding resolves on the next run.
