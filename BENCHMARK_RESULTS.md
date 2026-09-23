# Ecommerce intelligence benchmark: first pilot

Ten fictional-brand tasks, four conditions, forty eventual usable outputs. Six diagnostic questions and four artifact tasks. No live business was connected and nothing was deployed.

## Findings

Retrieval was not a consistent quality win. DeepSeek improved on five tasks and declined on five in the source-aware automated review. Its diagnostic-question average rose from 88.85 to 91.46, while artifact-task average fell from 85.31 to 78.28. Astra scores clustered near the rubric ceiling with and without retrieval; the small average increase is not evidence of a meaningful business advantage.

| Configuration | Advisory quality /100 | Median estimated total seconds | Mean generation cost, USD | First-pass usable | Eventual usable |
|---|---:|---:|---:|---:|---:|
| DeepSeek Flash high, no retrieval | 87.4 | 58.1 | $0.0152 | 5/10 | 10/10 |
| DeepSeek Flash high, retrieval | 86.2 | 79.5 | $0.0254 | 0/10 | 10/10 |
| GPT-6 Astra medium, no retrieval | 98.9 | 56.5 | $0.0972 | 10/10 | 10/10 |
| GPT-6 Astra medium, retrieval | 99.6 | 56.1 | $0.1841 | 10/10 | 10/10 |

**Do not interpret the scores as percentages of business correctness.** They are weighted editorial ratings from two models, with visible reviewer disagreements and a strong ceiling effect. Costs and total latency above include recovery attempts; scoring cost is separate. Total latency is a standalone estimate made by adding measured generation time to the frozen packet's first retrieval time, not an actual full production-agent trace.

## Important configuration finding

The initial generation cap was 8,192 total completion tokens. DeepSeek produced five usable first-pass answers; fourteen responses were length-limited and one had malformed JSON. Some length-limited runs produced partial output; others exhausted the cap in reasoning. Astra produced all twenty on its first attempt.

A single 32,768-token recovery was allowed for every incomplete run, regardless of model. All fifteen needed recoveries happened to be DeepSeek. One recovered JSON response needed a missing closing bracket inserted; raw text remains unchanged and saved. All forty eventual outputs are available. The recovered results are therefore **not a clean equal-output-limit comparison**. This is a calibration finding and a reason to repeat with appropriate fixed limits before selecting a production model.

Median final-attempt generation times, excluding prior failed attempts, were:
- DeepSeek Flash high, no retrieval: 36.7s.
- DeepSeek Flash high, retrieval: 40.5s.
- GPT-6 Astra medium, no retrieval: 56.5s.
- GPT-6 Astra medium, retrieval: 55.5s.

## Concrete output findings

- Conversion diagnosis: examined answers with and without retrieval correctly calculated overall conversion falling 3% to 2%, mobile conversion 2.67% to 1.5%, and stable 4% desktop conversion. Basic arithmetic did not require the library.
- Discount economics: the test supplied full-price pre-ad contribution of $39.60 and discounted contribution of $24.08 through its inputs. Correctly deriving these is required, not proof of differentiated advice.
- In DeepSeek's retrieved 14-day plan, a proposed $70 CPA stop threshold and $55 graduation threshold exceeded $39.60 pre-ad contribution without a justified loss allowance. It omitted an inventory bridge gate and proposed multiple day-one launches.
- Astra's retrieved plan explicitly calculated 26.25 days of stock, a 70-unit shortage before replenishment, and a 6/day no-buffer bridging rate. It proposed conditional spend and offline research/prototypes. Astra without retrieval also recognized the stock constraint.
- Some retrieved ad benchmarks were real source recommendations, not invented numbers. Their transfer to this brand remained insufficiently justified. This is a source-applicability issue, distinct from fabricated provenance.
- Some creative drafts extrapolated laptop or bottle compatibility beyond supplied facts. Those outputs need operator review before use.

## Retrieval measurements

- Cold engine load: 1411 ms.
- Median first query/packet: 638 ms; median warm query/packet: 64 ms.
- Actual knowledge packets: 3,837–9,620 tokens; 14–32 cards. Focused allowance 8k; artifact allowance 16k. These are the later agreed generous allowances, not the older 2k suggestion.
- Both models received the identical frozen text packet for each retrieval task. Non-retrieval runs received the same task, brand and system prompt, with an empty reference field.
- This tests frozen text retrieval, not model-generated searches, multi-step tool use, automatic freshness verification or live execution. Essential card caveats were included; auxiliary metadata flags were not a separate model input.
- More cards can introduce loosely applicable advice. The next comparison should vary selection/packet size with the model configuration fixed.

## Review method

Rubric written before generation: factual accuracy 30%, brand fit 15%, task completion 20%, actionability 15%, uncertainty/questions 10%, prioritization 10%. Each dimension is scored 0–4 and normalized to 100. Six questions and four artifact tasks have predeclared task-specific criteria. Those criteria were not sent to answer-generating models.

DeepSeek and GPT-5.6 Terra reviewed anonymized A–D answers in opposite orders. Final reviews include the available reference packet, allowing a reviewer to distinguish actual source guidance from unsupported invention. Sources are not ground truth and using them is not rewarded by itself. Original source-blind reviews are retained in judges-v1; the corrected all-task review is in judges-v2. No generated answer was changed in response to a score.

Reviewers are not independent human experts: DeepSeek also generated candidates, and the other reviewer shares OpenAI's model family. Automated ratings have style and ceiling biases. A narrow arithmetic task should not be penalized for asking no questions. Some judgments also depend on interpreting fictional evidence, such as whether a simulated review count could be displayed. Read the full outputs and reviewer reasons; an independent operator-rating worksheet is included.

## Cost and audit trail

Benchmark generation, fifteen recoveries and both review rounds: **$5.1194** conservative ledger estimate, below the $12 stage cap. Unresolved benchmark reservations: $0.0000.
Project-wide cumulative settled-plus-reserved estimate: **$26.7801**, including earlier unrelated work and unresolved historical reservations. Embedding usage is in that global ledger; it is not included in the generation-only table.
- Per-request logs retain model requested/returned, reasoning setting, prompt/completion/reasoning/cache tokens, request IDs, finish reason, output, original failed attempts, cost and response time.
- Usage-priced generation estimates accounting for reported cache hits/writes are also in metrics.csv. The headline table conservatively books all DeepSeek input at peak noncached rates and Astra input at the cache-write allowance. Actual invoices can be lower. No time-to-first-token measurement was taken.

Pricing/configuration references checked for this run: [OpenAI Astra model](https://developers.openai.com/api/docs/models/gpt-6-astra), [OpenAI pricing](https://developers.openai.com/api/docs/pricing), [DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing/).

## What to do next

1. Fix reasoning/output settings before another model comparison; keep the effective limits consistent across each pair.
2. Test smaller, more selective packets versus the current generous packets. Preserve essential caveats, remove unrelated tactics, and distinguish source heuristics from measured brand evidence.
3. Make inventory, contribution and capacity constraints explicit inputs and validate recommendations against them.
4. Repeat the failed/high-value tasks on held-out scenarios with independent operator review. Then choose model routing by task.
5. Connect a real brand only after this calibration. The viewer is a read-only benchmark comparison, not a production agent or a live brand-input application.

## Files

- [Comparison viewer](C:/Users/kevin/Documents/Codex/2026-09-22/https-drive-google-com-drive-u/outputs/ecom-intelligence/BENCHMARK_COMPARISON.html)
- [Fictional brand profile](C:/Users/kevin/Documents/Codex/2026-09-22/https-drive-google-com-drive-u/outputs/ecom-intelligence/BENCHMARK_BRAND.md)
- [All metrics CSV](C:/Users/kevin/Documents/Codex/2026-09-22/https-drive-google-com-drive-u/outputs/ecom-intelligence/data/ecommerce-benchmark-v1/metrics.csv)
- [Within-model differences](C:/Users/kevin/Documents/Codex/2026-09-22/https-drive-google-com-drive-u/outputs/ecom-intelligence/data/ecommerce-benchmark-v1/paired-deltas.csv)
- [Blank operator ratings](C:/Users/kevin/Documents/Codex/2026-09-22/https-drive-google-com-drive-u/outputs/ecom-intelligence/data/ecommerce-benchmark-v1/operator-rating-template.csv)
- [Operator spot-review notes](C:/Users/kevin/Documents/Codex/2026-09-22/https-drive-google-com-drive-u/outputs/ecom-intelligence/data/ecommerce-benchmark-v1/operator-review-notes.json)
- [Q1: Diagnose conversion decline](C:/Users/kevin/Documents/Codex/2026-09-22/https-drive-google-com-drive-u/outputs/ecom-intelligence/benchmark-results/Q1.md)
- [Q2: Reconcile attribution](C:/Users/kevin/Documents/Codex/2026-09-22/https-drive-google-com-drive-u/outputs/ecom-intelligence/benchmark-results/Q2.md)
- [Q3: Discount unit economics](C:/Users/kevin/Documents/Codex/2026-09-22/https-drive-google-com-drive-u/outputs/ecom-intelligence/benchmark-results/Q3.md)
- [Q4: Diagnose creative fatigue](C:/Users/kevin/Documents/Codex/2026-09-22/https-drive-google-com-drive-u/outputs/ecom-intelligence/benchmark-results/Q4.md)
- [Q5: Assess email performance](C:/Users/kevin/Documents/Codex/2026-09-22/https-drive-google-com-drive-u/outputs/ecom-intelligence/benchmark-results/Q5.md)
- [Q6: Prioritize with inventory constraint](C:/Users/kevin/Documents/Codex/2026-09-22/https-drive-google-com-drive-u/outputs/ecom-intelligence/benchmark-results/Q6.md)
- [A1: Product-page copy and implementation brief](C:/Users/kevin/Documents/Codex/2026-09-22/https-drive-google-com-drive-u/outputs/ecom-intelligence/benchmark-results/A1.md)
- [A2: Five distinct ad concepts](C:/Users/kevin/Documents/Codex/2026-09-22/https-drive-google-com-drive-u/outputs/ecom-intelligence/benchmark-results/A2.md)
- [A3: Abandonment flow draft](C:/Users/kevin/Documents/Codex/2026-09-22/https-drive-google-com-drive-u/outputs/ecom-intelligence/benchmark-results/A3.md)
- [A4: 14-day experiment plan](C:/Users/kevin/Documents/Codex/2026-09-22/https-drive-google-com-drive-u/outputs/ecom-intelligence/benchmark-results/A4.md)
