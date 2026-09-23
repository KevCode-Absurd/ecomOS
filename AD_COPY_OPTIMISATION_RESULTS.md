# Ad-copy optimisation results

| Condition | Score /100 | Sol | Luna |
|---|---:|---:|---:|
| v1.1 generic | 62.0 | 57.33 | 66.67 |
| v1.1 playbook | 67.67 | 59.33 | 76.0 |
| v1.1 playbook_cards | 63.17 | 58.0 | 68.33 |
| v1.2 playbook | 77.67 | 73.67 | 81.67 |
| v1.2 playbook_cards | 79.67 | 71.0 | 88.33 |

These are two blinded AI reviewers’ editorial scores, not owner approval or live ad performance. All five conditions were re-rated together in shuffled order under the same frozen rubric. The table uses only the original three matched briefs; the additional brief is reported separately.

New experiment cost estimate: $0.105472, including initial reviews, nine new generations and final reviews. Earlier benchmark cost and reservations remain separate.

## Scope

Six weighted criteria: clarity (20%), visual specificity (20%), pain relevance (15%), benefit (20%), crispness (15%), distinct variants (10%). Ratings 0–5 are converted to /100 by code. Factual issues are separate flags; unsupported claims cannot be justified by a high score. Reviewers receive original brand facts, brief, rubric/source summaries and anonymised customer copy, never writer prompts or condition labels.

The writer is Luna, medium reasoning, three variants per task. Brand facts, length requirements and original task-specific supplemental cards were held fixed. The v1.2 instruction package was frozen before generation. Existing generic outputs are reused, not independently regenerated for the matched briefs. A new same-brand brief received fresh generic/playbook/cards responses; it is a transfer check, not an independent-market holdout. Full-card retrieval is manually selected ID lookup, not a search benchmark.

## Additional brief

- playbook_cards: 73.5/100; individual scores gpt-6-sol: 67.0, gpt-6-luna: 80.0.
- generic: 68.0/100; individual scores gpt-6-sol: 61.0, gpt-6-luna: 75.0.
- playbook: 70.0/100; individual scores gpt-6-sol: 63.0, gpt-6-luna: 77.0.

## Limits and next decision

One brand, one generation per condition, same-family AI reviewers, subjective ordinal ratings and potential optimisation to the rubric. No statistics establish a general lift. Keep versions and failures, avoid repeated rerolls until a score improves, and assess new brands/real owner feedback before rollout. Exact generation and review prompts are in calls; mapping and reviews are retained. Original cards and v1.1 outputs are unchanged.
