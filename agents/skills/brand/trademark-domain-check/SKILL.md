---
name: trademark-domain-check
owner: BRAND
version: 1
invoke_when: a name shortlist needs legal, availability and language-risk screening before it is presented as final
inputs: scored shortlist, target markets and languages
outputs: clearance report per finalist, legal-review flag list
---
# Trademark, domain and language clearance

## Purpose
A name that scores well on the 7 qualities can still be legally unusable or embarrassing in a target market's language. This is the free screening pass; a paid legal opinion or filing is a separate, human_assist step this skill only flags the need for.

## Steps
1. Search the USPTO trademark database (and international equivalents such as the EUIPO or an India registry for any export market) for exact and close matches in this product category.
2. Search "name + industry term" combinations for existing uses that a database search alone would miss.
3. Check domain availability (.com and the relevant local ccTLD) and social handle availability across the platforms the brand actually uses.
4. Check meaning and sound in every relevant market language, including Spanish for the US market and any other market language (Hindi or a regional language for an India-market name) the brand's customer base speaks, for an unintended negative meaning.

## Checks
- Every finalist gets an explicit status: clear, risk, or needs-legal.
- A "risk" or "needs-legal" status is never softened to "probably fine" in the report shown to the founder.

## Output
`{clearance_report_per_finalist: [{name, trademark_status, domain_status, language_check, overall}], legal_review_flag_list}`

## Example
Candidate clears trademark and domain search, but the Spanish phonetic reading is close to an unrelated slang term: flagged "risk: language," recommended against despite scoring well on the 7 qualities.
