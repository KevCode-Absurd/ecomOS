---
name: brand-guidelines-builder
owner: BRAND
version: 1
invoke_when: a new brand or a major refresh needs the full guidelines document assembled
inputs: identity direction brief, reference set, voice and tone sheet
outputs: brand guidelines document (4 parts), completeness checklist result
---
# Brand guidelines builder

## Purpose
The guidelines document is what every future specialist and vendor checks work against. This skill assembles all 4 required parts and refuses to call the document done until every part is actually present.

## Steps
1. Draft logo and mark rules: clear space, minimum size, and at least 3 concrete misuse examples.
2. Assemble the visual language section from the identity brief and reference set: palette, typography, photography direction, each tied back to the mood reasoning behind it.
3. Fold in the voice and tone sheet directly as the language rules section; do not rewrite or summarize it, use the real sheet.
4. Build the expressions section: 3-5 applied examples (a PDP header, an email, an ad) showing the rules working together in practice, each passing claim-check and the writing rules.
5. Run the completeness checklist across all 4 parts; a missing part blocks publishing entirely, it does not ship with a "to be added" placeholder.

## Checks
- All 4 parts (mark rules, visual language, language rules, expressions) are present before this is called done.
- Every applied example in the expressions section passes claim-check and the writing rules.

## Output
`{brand_guidelines_document: {mark_rules, visual_language, language_rules, expressions}, completeness_checklist_result}`

## Example
Completeness check fails on first pass: expressions section has only 2 applied examples. Blocked from publishing until a 3rd (an email example) is added.
