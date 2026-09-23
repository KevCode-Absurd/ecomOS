# Copy playbook: what to keep after two further revisions

**Keep v1.2 as the strongest tested candidate.** Preserve v1.3 and v1.4 as experiments, not replacements. The source cards and default workflow loader are unchanged.

We added the requested criteria: natural language, a below-grade-10 writing target, avatar fit, practical benefits and a credible connection between the unwanted situation, the product and the desired improvement. These are now explicit in the experimental playbooks and editor checklists for writing ads, revising copy and handling objections. Only static-ad writing was generation-tested.

## What happened

| Round | Generic | Previous v1.2 | New revision | Interpretation |
|---|---:|---:|---:|---|
| Five briefs; v1.3 | 55.7 | 76.0 | 74.7 | Simpler language, but some scenes displaced the actual buying question. |
| Six briefs; v1.4 | 70.3 | 80.1 | 77.4 | Better task focus, but repeated inventory/price lines weakened the ads. |

Scores are /100 from blinded Sol and Luna reviews of Luna-written copy. Compare conditions **within each row**. Both reviewers ranked v1.2 above v1.4 in the final round: Sol 78.2 versus 75.5; Luna 82.0 versus 79.3. This does not establish a statistically reliable difference or better advertising results.

**Reviewer instability matters.** Re-rating the same five generic sets in the second batch moved their mean from 55.7 to 69.4 without changing their copy. The same five v1.2 sets moved from 76.0 to 80.9. This is a reason to inspect the actual ads and use owner preference; small score changes should not drive automatic prompt updates. The final round's single fresh support-retargeting brief was essentially tied: generic 75, v1.2 76, v1.4 77.

## Readability, usage and cost

Final six-brief averages per request; each request produces three ads:

| Condition | Approx. grade | Input tokens | Output tokens | Seconds | Estimated cost |
|---|---:|---:|---:|---:|---:|
| Generic | 9.6 | 428 | 1,246 | 16.1 | $0.000677 |
| v1.2 | 8.4 | 1,274 | 1,846 | 25.9 | $0.001082 |
| v1.4 | 8.1 | 1,373 | 1,540 | 23.6 | $0.000942 |

Reading grade uses a spelling-based syllable heuristic on English primary text, not a certified reading assessment. Short ads and product names make this noisy. Output tokens include reported reasoning tokens. Old outputs were reused, so latency is descriptive rather than a controlled speed comparison. Costs use conservative input rates, without cache discounts.

**New API spend across both rounds: approximately $0.1454.** This covers 17 new generation calls and four reviewer calls. Historical runs were reused without being charged again. Existing budget controls remained in place.

## What belongs in the working process

1. Answer the customer's actual buying question before choosing a copy formula.
2. Make one credible feature-to-benefit connection for this avatar. The desired improvement can be small; do not manufacture a life transformation.
3. Use natural language and concrete detail when it clarifies that answer. Do not require every ad to start with a scene.
4. Judge each ad as a standalone message, then check whether the set offers genuinely different angles.
5. Check exact claims separately from style. The v1.4 headline “Six childproofing items in one kit” was flagged because a six-part/category kit does not establish an exact piece count. Keep that failed output in the test record; do not present it as publish-ready.
6. Record the owner's preferred wording and reason. Put brand-specific voice/facts into brand context and reusable writing rules into the next version. Do not automatically rewrite cards or chase a reviewer score.

The current evidence supports keeping v1.2 for the next owner-reviewed copy task. The new criteria remain useful editorial checks; the expanded prompts have not earned replacement status. No extra full cards were tested in these two rounds, so there is no new claim about the value of adding cards on top of the playbook.

## Files

- [Final side-by-side comparison](AD_COPY_TASK_FIRST_COMPARISON.html): all 18 sets, exact copy, scores, flags, input/output tokens, cost and latency.
- [First revision comparison](AD_COPY_BRIDGE_COMPARISON.html): all 15 sets, including the v1.3 regression.
- [Working candidate](playbooks/ad-copy-v1.2/README.md).
- [Plain-language revision](playbooks/ad-copy-v1.3/README.md).
- [Task-first revision](playbooks/ad-copy-v1.4/README.md) and [editor checklist](playbooks/ad-copy-v1.4/EDITOR_CHECKLIST.md).
- Raw manifests, prompts, provider responses, blinded label mappings and scores: `data/ad-copy-bridge-v1` and `data/ad-copy-bridge-v2`.

Scope: one brand, hypothetical briefs, saved facts, no fresh website verification, no live ads and no observed conversion results. The other domain playbooks remain unchanged.
