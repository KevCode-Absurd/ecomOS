# Development comparison: what the library changed

Status: qualitative model-assisted review of six synthetic brand scenarios, three context conditions, one Terra-high response per condition. The same brand brief, question and executor instructions were used. Expected answers and scoring criteria were withheld from the executor. No business actions were available.

This does **not** demonstrate a moat or establish production quality. It isolates a known-relevant source packet from a raw excerpt and from general model knowledge. It does not test actual search, independent human preferences, unseen brands, repeated-run stability or commercial outcomes.

## Observed differences

| Scenario | What happened | Interpretation |
|---|---|---|
| Duplicate subscription gift | All three rejected extra recurring product and suggested a complementary gift. | Core decision was not differentiated. Raw text and general knowledge supplied useful delay/skip guidance that the compact packet did not emphasize. |
| Complementary subscription gift | All three accepted the shaker conditionally on feasibility. Raw text produced a more complete billing reminder with charge/date and delay links. | Clearer source citations alone do not prove a better operator result. The curated selection omitted useful adjacent guidance. |
| Low-volume CRO | All three rejected a broad multivariate test. Raw and curated contexts prioritized revenue per session; no-library output used purchase conversion as primary. | A concrete source-specific change in measurement choice. The curated answer also explicitly checked feasibility before committing to a narrower test. |
| Higher-volume CRO | Curated context allowed a conditional factorial design after per-cell/checkout sample checks. Raw and no-library outputs initially advised against the proposed broad test. | Evidence can change the decision boundary. This is not proof the curated choice is universally correct; real test design still needs missing data. |
| Cross-platform ROAS | All three warned against reallocating from prospecting to brand search based solely on reported ROAS. | Broad recommendation was already available from general knowledge; curated evidence made its source and example limitations more inspectable. |
| Within-platform ROAS | The curated answer began by recommending a controlled budget shift, while assuming scalable audience/inventory capacity despite missing spend, volume and economics. The no-library answer more explicitly required checks before scaling. | Regression: supplied advice can make an agent overconfident. Retrieval must not turn directional guidance into permission to act. |

## Required changes before release

1. Treat source-supported knowledge as evidence for a decision, not execution authorization. Require brand-level measurement, economics and operational checks before a live budget change. These operator safeguards are explicitly derived system policy, not claims attributed to these sources.
2. Preserve adjacent practical dependencies when constructing compact packets. In the subscription case, gift selection and order-stage personalization were retained but delay/skip guidance was excluded. A useful compact packet needs the relevant dependency, not every card in the source.
3. Keep warnings and principles available even when an action's prerequisites are unmet. Exclusions must not hide the very warning that explains why an action is inappropriate.
4. Separate semantic extraction review from executor evaluation. Passing exact evidence checks cannot detect a premature recommendation.
5. Add harder, unseen brand cases and independent reference reviews. Do not tune these six examples and report them as held-out success. Keep paired changes to margin, inventory, attribution reliability, platform and customer behavior.

No numerical decision-quality win rate is claimed. The observations above are judgments to investigate, not independent ground truth. Machine-measured cost and prompt-size comparisons are stored separately in `data/agent-ablation-v1/metrics.json`.

## Measured size and cost

| Condition | Six-run prompt tokens | Booked API cost |
|---|---:|---:|
| No library | 1,552 | $0.033520 |
| Raw excerpt | 14,394 | $0.078189 |
| Reviewed cards | 9,030 | $0.066831 |

Reviewed cards reduced total prompt tokens by 37.27% versus raw excerpts. Subtracting the no-library prompt baseline estimates a 41.77% reduction in library-context tokens. These are measurements for these selected packets, not a promised compression ratio for the full library. Curated runs cost about 14.5% less than raw-context runs; generation length varied despite identical limits.

All 18 responses completed and used valid output fields and citation IDs. Three curated responses exceeded the requested 350-word limit; no raw-context or no-library response did. The shared API completion allowance was 8,192 tokens with high reasoning, while the requested visible answer length was 350 words. Exact cited-ID validity is not semantic support, and this protocol deviation further limits comparison.
