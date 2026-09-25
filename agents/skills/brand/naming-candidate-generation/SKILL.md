---
name: naming-candidate-generation
owner: BRAND
version: 1
invoke_when: a naming project needs raw candidates across naming types
inputs: category/product/buyer audit, avatar record
outputs: naming brief, raw candidate list (50-100+)
---
# Naming candidate generation

## Purpose
A naming project fails when it generates too few candidates from too narrow a style. This skill forces volume and variety before any human judgment narrows the field.

## Steps
1. Run the audit: category naming conventions already in use, the product's real attributes, and the avatar's own language, so generation starts grounded, not generic.
2. Write the naming brief, explicitly including what the name must not do: no forbidden claim, no sound-alike collision with a named competitor, no meaning that turns negative in a relevant language.
3. Generate far more candidates than feels necessary, spanning naming types: descriptive, suggestive, invented/coined, founder-name-based, and evocative/metaphorical. Use AI generation for volume; apply human judgment only at the review step that follows, never to pre-filter the generation itself.

## Checks
- The candidate list spans at least 3 different naming types, not one flavor repeated 80 times.
- The naming brief's "must not do" list is written before generation starts.

## Output
`{naming_brief, raw_candidate_list: [50-100+ names]}`

## Example
Brief flags: must not sound like [named competitor], must not translate poorly in Hindi, must work as a hashtag. Candidates generated across all 5 types, roughly 20 per type.
