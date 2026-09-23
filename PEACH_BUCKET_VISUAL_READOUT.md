# Peach Bucket: focused visual benchmark

Completed: six full landing-page drafts, six complete hero-section designs, six square ads and six matching ad-copy sets. Open PEACH_BUCKET_VISUAL_COMPARISON.html to compare each model side by side. All image prompts and render provenance are included. Built-in image generation was used.

## What this test found

Retrieval did not consistently improve the copy. One blinded GPT-6 Sol review, simulating an agency owner, scored Luna 2→2, Sol 4→3 and Astra 3→4 out of 4. These are copy-only judgments, not image scores, customer satisfaction or conversion results. Same-family reviewer bias and one-sample variance apply.

Astra with retrieval has a coherent page/ad campaign: “First crawls. A clear place to start.” Its page includes “The room hasn’t changed. What your child can reach has.” Sol without retrieval also gives a strong, concrete angle: “The cupboards are suddenly interesting.” Luna’s “everyday home touchpoints” is abstract and less natural for parents.

The biggest actionable defect is relevance: Luna received a staff-permissions card in its landing-page search; Sol received a security-abstractions card in its audience search. Other matches were loosely related, including subscription tiers and surprise-and-delight tactics. Eighteen returned cards is not eighteen useful cards.

The shared prompt also needs improvement. It repeatedly emphasizes claim limits, and several drafts sound like an evaluator: “the brand advertises.” That is a prompt-design confound affecting both arms. Keep verified offer facts in a separate fact sheet, ask for direct brand voice, and consolidate necessary eligibility/supervision language.

## Costs, tokens and speed

| Model | Cards | Input tokens | Output tokens | Text cost estimate | Model-call seconds | Search seconds | Copy score /4 |
|---|---|---:|---:|---:|---:|---:|---:|
| gpt-6-luna | none | 12,208 | 6,585 | $0.00482 | 64.7 | 0.00 | 2 |
| gpt-6-luna | cards | 17,451 | 6,364 | $0.00536 | 58.1 | 3.96 | 2 |
| gpt-6-sol | none | 12,179 | 7,850 | $0.10895 | 88.4 | 0.00 | 4 |
| gpt-6-sol | cards | 17,325 | 6,833 | $0.11164 | 78.9 | 2.66 | 3 |
| gpt-6-astra | none | 13,055 | 8,838 | $0.60509 | 229.4 | 0.00 | 3 |
| gpt-6-astra | cards | 18,325 | 10,231 | $0.74061 | 250.8 | 2.23 | 4 |

Text API total, including the blinded review: approximately **$1.43**, with no unresolved text requests in this new round. Query embeddings add only a very small separate charge. These are conservative estimates using published output rates and the maximum short-context input/cache-write rate; actual cache discounts are not applied. The working API limit was $20, below the authorized $25 ceiling.

Image generation used the built-in tool, not the stored API key. That tool does not expose billable tokens or dollar cost here. Image cost is recorded as unknown, not zero; this report cannot certify an all-in invoice total. Image elapsed time is recorded per asset in the gallery; sums are not parallel wall-clock time.

Per-workflow figures include the planning call even though its result was cached and reused for that model’s paired arms. Therefore summing workflow rows differs from actual experiment spend. Output tokens include reasoning. Search timing includes query embedding work; warm caches and run order can influence speed.

## Exact process

1. Download public product listing and original website photos; inspect the kit reference. A corrupt lifestyle PNG was replaced by a verified 1200-pixel CDN rendition of the same photo for later renders. The image tool accepted the original for Luna. This source-resolution difference is a minor visual confound.
2. Give each GPT-6 model identical brand facts, photo descriptions and the same previously collected public audience-research memo. No new browsing was performed in this round.
3. At high reasoning, create the avatar/offer plan and three search queries. Reuse that exact plan across the paired conditions.
4. Retrieval arm: search avatar, landing-page and static-ad guidance, up to six cards and 2,500 estimated knowledge tokens per query. Baseline: no intelligence context.
5. Generate the full page copy, hero-section brief, single static-ad brief and matching copy. The language models receive asset descriptions, not image pixels; the image generator receives the original product references.
6. Render each brief with the same built-in image tool and inspect the actual output. No creative variants were cherry-picked or rewritten after scoring. Failed corrupt-reference attempts produced no usable asset; repaired-reference renders are recorded.
7. Run one anonymized copy-only review; validate all twelve saved images and paired inputs. Preserve all traces for inspection.

## Visual review and next improvement

All six heroes show a recognizable page header, headline, product, price and CTA; all six ads are square. The assets form coherent draft campaigns, but they are concepts, not pixel-exact product composites. The generator redraws packaging/components despite preservation instructions. Sol’s retrieved ad visibly rearranges the kit compartments. In production, keep the original product photo as a locked composited layer and generate the surrounding design.

The Luna retrieved hero is text-heavy; Sol retrieved is cleaner and uses one concise hook, while Sol without cards includes the setup-support differentiator. Astra’s pair both has clear product/offer hierarchy; the retrieved version adds the guarantee beside the CTA. These are visible differences, not evidence of higher conversion.

Next controlled change: route retrieval by task/domain and reject irrelevant matches, deduplicate across the three searches, and improve the shared customer-copy prompt. Then rerun the same fixed brief before choosing a model or connecting autonomous publishing. Keep the current outputs as the baseline.

## Sources and files

[Original product](https://thepeachbucket.com/products/the-peach-bucket-6-in-1-child-safety-kit) · [Official API pricing](https://developers.openai.com/api/docs/pricing)

Gallery: PEACH_BUCKET_VISUAL_COMPARISON.html. Individual PNGs, landing-page copy, ad copy and prompts: data/peach-visual-benchmark/deliverables/. Metrics: data/peach-visual-benchmark/metrics.csv. Full copy review: data/peach-visual-benchmark/copy-review.json.