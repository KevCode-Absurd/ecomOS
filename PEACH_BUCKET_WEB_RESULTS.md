# Peach Bucket web-enabled benchmark

39/48 completed answers; 7/16 valid simulated owner/agency reviews.

| Model | Context | N | Owner score /4 | Mean cost upper estimate | Median seconds | Mean input/output tokens |
|---|---|---:|---:|---:|---:|---:|
| gpt-5.6-luna | web | 8 | 3.09375 | $0.0419 | 51.4 | 27714 / 4160 |
| gpt-5.6-luna | web_cards | 8 | 3.25625 | $0.0453 | 64.4 | 39838 / 4445 |
| gpt-5.6-terra | web | 7 | 3.725 | $0.1595 | 67.0 | 28298 / 5018 |
| gpt-5.6-terra | web_cards | 7 | 3.625 | $0.1904 | 73.1 | 39150 / 5331 |
| gpt-5.6-sol | web | 4 | 3.64375 | $0.2617 | 79.2 | 27879 / 4616 |
| gpt-5.6-sol | web_cards | 5 | 3.5375 | $0.3474 | 80.2 | 43320 / 5038 |

## Preliminary finding

Across four reviewed tasks, cards changed the simulated score from 3.09 to 3.26 for Luna, 3.73 to 3.63 for Terra, and 3.64 to 3.54 for Sol. P1 has one reviewer; P2–P4 have two. This is mixed evidence, not proof of a universal quality improvement. Costs cover all completed runs, so their task counts differ from the scored subset.

There are 19 complete A/B pairs. Median retrieval took 572 ms across 39 searches (maximum 1.38 seconds). Every returned card ID exists in the library, and paired runs received identical brand facts and research. This validates delivery, not recall or correctness of every card.

The run stopped with 9 answers missing after transport failures and conservative budget reservations blocked further research calls. No requests are still running. Estimated settled cost is $6.07; unresolved reservations are $14.58, for $20.66 accounted against the $25 ceiling including negligible query-embedding cost. These reservations are not proven charges. Reconcile them against provider usage before resuming the missing tests.

See PEACH_BUCKET_FINDINGS.md for concrete issues and improvements.

## Interpretation and limits

Quality is primary. Scores are blinded simulated owner/agency judgments, not real customer satisfaction or measured sales lift. One answer per condition is exploratory; model-family judge bias and run variance remain.
Both arms receive identical public research for each model/task. Across models, research can differ. This tests cards after equal research; it does not establish fewer web searches or lower end-to-end cost from replacing research.
Every independent-request estimate includes full research cost, although that shared memo was billed once for the pair. All reasoning tokens are part of output totals. Cache discounts are not applied; billed cost may be lower. Web action items are conservatively counted at $0.01 each. Query embeddings are separate from these request estimates.
Exact API inputs, knowledge context and final outputs are recorded. Hosted search exposes sources/actions and aggregate usage, not all internal search snippets or page-by-page token allocation. Retrieval cannot prove all relevant cards were found; self-reported applied IDs cannot prove causal use.
Known facts: new store; sales reversals were test orders; 39 orders and 34 converted sessions are different metrics. Real customer order count is unknown. ₹2,233.02 at a ₹3,299 selling price is contribution before ads, RTO and other unconfirmed costs, not net profit.
Initial combined web/private run was stopped after automatic approval review rejected possible private-data leakage into search queries. The approved replacement structurally separates public research from private analysis. Old runs are excluded from quality results and retained in budget accounting.

## Budget ledger

{
  "reserved": {
    "requests": 11,
    "usd": 14.582655
  },
  "settled": {
    "requests": 103,
    "usd": 6.074523
  },
  "query_embeddings_upper": {
    "queries": 39,
    "usd": 9.300000000000002e-05
  }
}

Settled amounts are conservative usage estimates. Reserved amounts are unresolved or active requests, not proven charges; they remain counted toward the cap. Check provider billing to reconcile interrupted calls.

Open PEACH_BUCKET_WEB_COMPARISON.html for A/B answers, artifacts, cards and exact traces. Machine-readable metrics are in data/peach-web-benchmark/safe-metrics.csv.