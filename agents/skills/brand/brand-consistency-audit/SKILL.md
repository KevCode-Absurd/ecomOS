---
name: brand-consistency-audit
owner: BRAND
version: 1
invoke_when: the monthly consistency walk or the quarterly perception-gap comparison is due
inputs: brand guidelines, voice sheet, live site/ads/email, recent reviews/mentions/survey results
outputs: drift lists, perception-gap note, fix list
---
# Brand consistency and perception-gap audit

## Purpose
Drift compounds quietly: one off-voice email, one guideline-breaking ad, and within months the brand looks inconsistent everywhere. This skill catches it monthly, and quarterly checks the deeper question of whether the stated identity still matches what customers actually believe.

## Steps
1. Crawl key site pages (home, PDP, checkout) using `shared/surface-audit`'s method and check against logo rules, visual language and voice.
2. Check current live ad creative (via the public ad library, read-only) and recent email/SMS sends against the same rules.
3. Score each drift item by visibility and distance from the rule, computed, not gut-felt.
4. Quarterly: compare the positioning statement, voice sheet and claims against what reviews, social mentions and survey results actually say, quoting real customer language.
5. Classify each gap as the brand under-claiming (customers already believe more than the brand says) or over-claiming (customers do not believe what the brand claims); over-claims are the higher priority.
6. Draft a specific fix for each drift or gap item, naming the owning specialist (Site, Media, Creative) who would execute it.

## Checks
- Every drift item cites the exact rule it breaks.
- Every perception-gap note quotes real customer language, not a paraphrase.
- Over-claim gaps are ranked above under-claim gaps.

## Output
`{site_drift_list, ads_email_drift_list, perception_gap_note, fix_list}`

## Example
Drift: PDP hero image on a new SKU uses a font outside the type system (breaks Visual Language rule 2). Perception gap: guidelines claim "handcrafted," but 6 recent reviews describe the finish as "machine-perfect": classified as an over-claim gap, flagged high priority.
