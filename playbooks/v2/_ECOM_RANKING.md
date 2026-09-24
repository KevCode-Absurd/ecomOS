# Ecommerce specificity: ranking of the 25 folder playbooks

Date: 24 Sep 2026. Source: one review agent per playbook (`playbooks/v2/<folder>/ECOM_REVIEW.md`). Rules are section 3 decision rules. Columns: (a) store-specific, (b) generic but correctly applied to a store, (c) generic with no store framing, (d) out of scope for a store. Priority block = a ranked 'what matters most for a store' section; none of the 25 had one, every review drafted one.

Ranked from most work needed to least.

| # | Folder | Score | Rules | (a) store | (b) applied | (c) generic | (d) out | Demote (words) |
|---|---|---|---|---|---|---|---|---|
| 1 | 18-COG | 2 | 72 | 3 (4%) | 28 | 41 (56%) | 0 | 400 |
| 2 | 13-ORG | 2 | 174 | 15 (8%) | 21 | 138 (79%) | 0 | large |
| 3 | 16-AEO | 2 | 109 | 24 (22%) | 4 | 77 (70%) | 4 | ~500 |
| 4 | 21-OPS | 2 | 108 | 29 (26%) | 4 | 75 (69%) | 0 | 3000 |
| 5 | 04-BRD | 3 | 150 | 0 (0%) | 60 | 90 (60%) | 0 | ~500 |
| 6 | 11-ADC | 3 | 123 | 1 (0%) | 42 | 80 (65%) | 0 | 1700 |
| 7 | 10-MCR | 3 | 178 | 18 (10%) | 28 | 132 (74%) | 0 | 760 |
| 8 | 23-SEC | 3 | 139 | 38 (27%) | 34 | 67 (48%) | 0 | ~1500 |
| 9 | 24-DEP | 3 | 107 | 31 (28%) | 16 | 60 (56%) | 0 | 3050 |
| 10 | 06-MEA | 3 | 95 | 32 (33%) | 17 | 46 (48%) | 0 | ~400 |
| 11 | 15-SEO | 3 | 146 | 52 (35%) | 23 | 70 (47%) | 1 | 2850 |
| 12 | 07-LPG | 4 | 133 | 30 (22%) | 44 | 56 (42%) | 3 | ~400 |
| 13 | 02-AVT | 4 | 108 | 41 (37%) | 39 | 28 (25%) | 0 | 475 |
| 14 | 08-SPD | 4 | 107 | 43 (40%) | 28 | 36 (33%) | 0 | ~525 |
| 15 | 19-WLD | 4 | 143 | 70 (48%) | 38 | 30 (20%) | 3 | ~400 |
| 16 | 09-CRO | 4 | 137 | 71 (51%) | 13 | 53 (38%) | 0 | 1100 |
| 17 | 14-EML | 4 | 195 | 115 (58%) | 32 | 48 (24%) | 0 | 1600 |
| 18 | 12-GAD | 4 | 143 | 97 (67%) | 22 | 24 (16%) | 0 | 380 |
| 19 | 99-multi | 4 | 112 | 82 (73%) | 23 | 0 (0%) | 7 | 1700 |
| 20 | 05-SET | 4 | 143 | 113 (79%) | 11 | 19 (13%) | 0 | ~475 |
| 21 | 03-OFF | 4 | 151 | 124 (82%) | 20 | 7 (4%) | 0 | 240 |
| 22 | 17-CXP | 4 | 158 | 134 (84%) | 11 | 12 (7%) | 1 | 740 |
| 23 | 20-FIN | 4 | 142 | 122 (85%) | 14 | 6 (4%) | 0 | 290 |
| 24 | 22-AMZ | 4 | 97 | 85 (87%) | 9 | 3 (3%) | 0 | 350 |
| 25 | 01-PRD | 5 | 109 | 81 (74%) | 22 | 6 (5%) | 0 | 175 |

Totals: 3279 rules; 1451 store-specific (44%), 1204 generic with no store framing (36%), 19 out of scope.

## Wave 2: edits applied (24 Sep 2026)

Every one of the 25 playbooks received the structural fix its review asked for, applied by one Sonnet agent per folder using exact text replacement (no rewriting from memory). Rule ids, conditions, sources and card ids are unchanged; cards.json is untouched.

What each playbook now has:

- `### 3.0 Ecommerce priority order`: 12 ranked levers at the top of section 3, with store-type conditions (hero SKU vs catalogue, AOV band, subscription, marketplace-heavy, luxury, mobile-first India vs US). Items that no library source covers are tagged `[general practice]`.
- Reworded rules: the review's list of generic rules, restated in store terms (product page, cart, PDP images, SKU, AOV, returns, marketplace). Typically 10 to 15 per playbook.
- New store levers: 5 to 8 new rules per playbook for gaps the review found, tagged `[general practice]` with "No library source; verify against brand data before use" where no card supports them.
- `## Appendix A. General background`: demoted material (leadership theory, generic SaaS or agency content, textbook definitions) moved after section 12, with one-line pointers left in place so ids still resolve.
- Section 0 gained an "Ecommerce first." paragraph; section 11 gained a dated changelog line.

Checks passed on all 25: zero em dashes, exactly one `### 3.0` heading (formula sub-sections in 03-OFF, 17-CXP, 18-COG and 20-FIN were renamed `3.0b`), Appendix A present, all original card ids present.

Declined by the apply agents (kept as is because a rewrite would have deleted rule content): 21-OPS R65. Others noted in each folder's commit.

Still generic after wave 2: the four lowest-ranked playbooks (18-COG, 13-ORG, 16-AEO, 21-OPS) were fixed at the structure level only. Their rule bodies are still 56% to 79% generic because the sources are books and creator content, not store material. A deeper pass would need a Fable rewrite of section 3 per playbook, using the priority block as the spine and the library cards for evidence, about 300k tokens each.

## Wave 3: deep rewrite of section 3 for the 4 weakest playbooks (24 Sep 2026)

One Fable agent per playbook rewrote every rule body in section 3 for store use: first sentence is the store trigger, then the action on a named store surface, then a check. Rule ids, order, group numbers, conditions, source numbers, conflict codes and card ids are unchanged (verified by script: `deep_verify.py` in the session scratchpad, logic recorded here: old rule ids and card ids must all appear, one `### 3.0` heading, no em dashes, length 0.9x to 1.3x). Examples from outside ecommerce (B2B software, SaaS, corporate leadership fables, named executives, creator-economy cases) were removed or replaced with store examples tagged `[general practice]`. Versions bumped to 2.1-draft with a changelog line in section 11.

| Playbook | Section 3 words before | after | Rules | Non-store examples removed | Notes |
|---|---|---|---|---|---|
| 21-OPS | 6,863 | 8,775 | 101 | 12 | Named executives and fable numbers out; Oodie and Lands' End cases kept as source brands |
| 18-COG | 7,854 | 10,097 | 78 | 1 | Already store material; every rule gained trigger and check; `[general practice]` tags 20 to 57 |
| 13-ORG | 12,422 | 15,974 | 169 | 28 places, about 40 examples | Creator hooks and B2B lead cases replaced with store hooks; source-brand cases kept |
| 16-AEO | 11,451 | 14,727 | 118 (1 new, R118) | 9 | SaaS review sites and sign-up figures moved to Appendix A; 4 wrong cross-references fixed |

Known follow-ups: parenthetical store glosses inside source sentences in 21-OPS carry `[general practice]` by a blanket note in the section 3 intro rather than per sentence. 13-ORG R14 adds "through order peaks" to a cadence condition the sources do not mention. Both are flagged in the agents' reports and can be tightened by hand.
