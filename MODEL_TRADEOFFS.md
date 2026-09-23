# DeepSeek versus OpenAI: intelligence-layer decision

Checked 22 September 2026. Recommendation: evaluate DeepSeek-V4.1-Flash as the bulk extractor, use GPT-5.6 Terra for independent evidence verification, and GPT-5.6 Sol for ambiguous conflicts. Use your existing ChatGPT Pro/Codex allowance for implementation and supervised quality review. No corpus benchmark or paid model run has been performed yet.

## What is verified

DeepSeek's official model ID is `deepseek-flash`, currently serving V4.1-Flash. It supports thinking/non-thinking, JSON output, tools and vision. Standard uncached prices per million input/output tokens are $0.30/$1.20 at peak and $0.15/$0.60 off-peak. Do not assume new source text receives cache-hit rates. The current model is an alias: record returned model identity and rerun regression tests when the provider changes it. [Official pricing](https://api-docs.deepseek.com/quick_start/pricing/?push_animated=1&show_loading=0&theme=light&webview_progress_bar=1).

DeepSeek defaults to thinking with high effort. Explicitly configure effort: start with non-thinking for routing and low for extraction, compare high on difficult sections, and keep the cheapest setting that passes evaluation. Account for reasoning output and retries. [Thinking controls](https://api-docs.deepseek.com/guides/thinking_mode/).

JSON output does not establish factual support or complete schema compliance; validate records and evidence independently. [JSON documentation](https://api-docs.deepseek.com/guides/json_mode/).

OpenAI standard short-context input/output prices per million tokens: Luna $0.20/$1.20; Terra $2/$12; Sol $4/$20. Thus DeepSeek peak is not cheaper than Luna for equivalent token volumes, but could offer better accepted-card economics if it extracts more reliably. This has not been measured. [Official pricing](https://developers.openai.com/api/docs/pricing).

## Stage routing

| Stage | Recommended starting point | Tradeoff |
|---|---|---|
| Parsing, hashes, quote lookup, schema validation | Code | Deterministic, reproducible and no model fee |
| Routing and metadata suggestions | Luna or DeepSeek non-thinking | Compare accuracy; cost difference is tiny at this scale |
| Bulk candidate extraction | DeepSeek low thinking | Strong price proposition; must preserve conditions and provenance |
| Independent claim/evidence validation | Terra | Costs more but protects reusable knowledge; still requires human audit |
| Conflicts and complex playbooks | Sol | Use selectively; a stronger model is not an authority without evidence |
| Embeddings | text-embedding-3-small | Keep retrieval representations separate from generation choice |
| Coding and supervised review | Pro allowance, Sol normally; Astra for difficult design/review | Saves incremental API spending while consuming subscription limits |

Pro includes Codex usage, subject to plan allowances. It can support development and supervised processing in supported product workflows; it does not provide a general-purpose unlimited OpenAI API balance for a hosted multi-client service. API-key use is separately metered. Do not assume one Pro plan covers your future production agents. [Plan and API distinctions](https://learn.chatgpt.com/docs/pricing).

## Apples-to-apples budget

Retain the BUILD_GUIDE workload: 350 sources, 30,000 raw tokens/source, 13.125m extraction input tokens and 2.8m billed extraction output tokens. Hold all other stages and acceptance/retry rates constant. These are illustrative assumptions, not measured corpus volumes.

| Configuration | Extraction only | Whole modeled pipeline, 30% reserve included |
|---|---:|---:|
| Previous Sonnet extraction baseline | $54.25 | $139.98 |
| DeepSeek peak extraction; other stages standard | $7.30 | $78.94 |
| DeepSeek off-peak extraction; other stages standard | $3.65 | $74.20 |
| DeepSeek off-peak; eligible remaining text stages at 50% batch rates | $3.65 | $39.64 |

These numbers replace only the extraction stage, not all processing with DeepSeek. They include the original modeled verification, deduplication, escalation, evaluation, playbooks and embeddings. They exclude subscription fees, engineering, hosting, manual review, taxes, OCR/transcription and external search. Tokenization and reasoning length differ across models; measure actual usage. Off-peak and batch are different discounts and must not both be applied to the same DeepSeek call.

For this library, a hybrid workflow is preferable to optimizing another few dollars out of verification. The greater cost is bad knowledge being reused across many clients. Pure DeepSeek extraction and self-verification is a lower-cost experimental option, but correlated mistakes make it a weaker default before evaluation.

## How to decide whether it is good enough

Compare DeepSeek low/high, Terra and the previous extraction baseline on 100–200 representative passages sampled across all domains. Include long-range qualifications, tables, numeric thresholds, contradictory advice, generated headers and source text containing instructions. This calibration does not reduce the full-library scope.

Blind-review against human-labeled references. Measure supported claims, preserved prerequisites/exclusions, actionable completeness, exact evidence, useful-card recall, schema failures, retries, latency and total cost per accepted card. Include human correction time in total cost. Do not select using general coding/math benchmarks or a model's confidence score.

Proposed release gate: at least 95% supported claims, at least 95% preservation of required conditions, no fabricated evidence or critical numerical distortions in the release test set, and no material degradation against the stronger baseline on held-out examples. These are targets, not achieved results; a clean finite test set is not a guarantee. Keep independent verification and periodic audits after deployment.

Context-window size does not change card design: continue section-based extraction and small task-specific retrieval packets. Never load the entire library simply because a model advertises a large window.

Repository check: `KevCode-Absurd/ecomOS` exists and the connector has push access. It is public. No source documents, private cards or credentials have been uploaded by this analysis.

## CRO folder observations (22 September 2026)

The initial 32,768-token DeepSeek high allowance still produced a confirmed all-reasoning truncation on one CRO batch. A separate OpenAI fallback returned usable candidates, including a relationship error held for repair. Testing 65,536 on new DeepSeek batches returned a usable result that required more than 32,768 completion tokens. This supports a larger allowance for this prompt, not a claim that larger allowances always improve accuracy.

DeepSeek's current [model documentation](https://api-docs.deepseek.com/quick_start/pricing/) lists a maximum output above this allowance and peak Flash rates of $0.30 input/$1.20 output per million tokens. The ledger keeps using those conservative peak rates. Usage, including reasoning, is charged against the shared $10 CRO limit before another request is dispatched.

OpenAI semantic review has caught source-to-rule promotion, omitted power/confidence assumptions, circular exclusions, missing workflow safeguards and broken dependencies. Exact source offsets remain necessary but insufficient. Larger completion allowances do not eliminate semantic errors; separate review remains part of the pipeline.

Transport now runs inside an isolated HTTP subprocess with a 300-second total deadline. Unknown outcomes retain reservations. Explicit cross-provider fallback is recorded separately and does not release or resend the original request.
