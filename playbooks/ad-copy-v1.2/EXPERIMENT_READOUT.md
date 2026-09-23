# Version 1.2: exploratory results and deployment decision

Two blinded AI reviewers (GPT-6 Sol and Luna) scored all original and revised outputs together on a frozen source-informed rubric. Luna wrote the copy in all conditions. Model scoring is not human approval, observed conversion lift or independent research.

## Matched original three briefs

| Condition | Mean /100 | Sol | Luna |
|---|---:|---:|---:|
| Generic | 62.00 | 57.33 | 66.67 |
| v1.1 playbook | 67.67 | 59.33 | 76.00 |
| v1.1 + two cards | 63.17 | 58.00 | 68.33 |
| v1.2 playbook | 77.67 | 73.67 | 81.67 |
| v1.2 + same two cards | 79.67 | 71.00 | 88.33 |

Both reviewers prefer revised playbook copy over the generic and earlier playbook on the matched average. They disagree about adding full cards to version 1.2: Sol prefers the playbook alone, Luna prefers cards. The two-point combined difference is not a reliable deployment signal.

## Dimensions: generic → v1.2 → v1.2 + cards

- Clarity: 86.67 → 86.67 → 86.67.
- Picturable specificity: 46.67 → 76.67 → 80.00.
- Pain relevance: 60.00 → 80.00 → 80.00.
- Supported benefits: 66.67 → 73.33 → 73.33.
- Crispness: 53.33 → 66.67 → 73.33.
- Variant distinction: 50.00 → 83.33 → 86.67.

The revision did not improve every dimension: it retained baseline clarity, and v1.1 playbook clarity scored higher (90). Do not describe the change as universally superior.

## Additional same-brand brief

Generic 68.0; v1.2 70.0; v1.2 + cards 73.5. This brief was generated after freezing the revision, but it shares brand facts and is only one example. Smaller gains argue against generalising the headline improvement to every task or brand.

## Decision

Use v1.2 as the **candidate for further ad-copy testing**, with full cards optional when a concrete decision needs them. Keep the general retrieval service and other playbooks unchanged. Do not automatically publish any ads. The revision remains experimental; no autonomous rollout, silent prompt replacement or owner-reviewed status is implied.

Stop this cycle here instead of repeatedly regenerating until the judges award high scores. The next revision should address weak benefit language (e.g. “add a childproofing measure”) and repetitive sentence shapes, then be tested on fresh briefs or another brand. Changing only the reviewer or excluding poor examples would not be evidence of improvement.

## Budget and audit

This cycle: nine new generation calls + four reviewer calls; conservative estimated cost $0.1054725. Earlier nine outputs were reused. Prior rejected-format reservations remain intact in the earlier ledger. Inputs, raw outputs, source IDs, reviewer mappings, rubric, usage and latency are under data/ad-copy-optimisation-v1. Reviewer severity flags have exact-quote checks recorded in final-scores-audited.json. Absence of reviewer flags is not proof all claims are correct.
