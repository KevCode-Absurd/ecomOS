---
name: name-screening-and-packaging
owner: BRAND
version: 1
invoke_when: candidates need scoring to finalists (brand or SKU scope) and packaging into a deliverable
inputs: raw candidate list or a lighter SKU naming need; clearance report once available
outputs: scored shortlist, finalist mock-ups, and for brand scope, the full naming deliverable
---
# Name screening and packaging

## Purpose
This skill covers both a full brand-naming screen and the lighter product/SKU/collection name screen, and carries the winner through to a presentable, packaged deliverable once cleared.

## Steps
1. Set the scope up front: a full brand name needs all 7 quality checks and a full deliverable; a SKU or collection name defaults to a descriptive, benefit-first title unless a real reason calls for a coined name.
2. Score every candidate on the 7 core qualities: distinctive, meaningful, memorable, brief, positive, extendable, protectable. Show all 7 scores per finalist, not a single blended number.
3. Test sound and syllable count by reading candidates aloud; flag acronym traps (unpronounceable or already-claimed initialisms) and generic-name traps (too descriptive to ever be ownable).
4. For the top 2-3, build realistic mock-ups: a PDP title, a packaging mock, a spoken-aloud test, rather than presenting a bare word list. Use the real product photo where accuracy matters.
5. For brand scope only, once trademark/domain clearance comes back clean: write nomenclature notes (why this name, what it signals), a short brand story, and a tagline that passes the strip test.

## Checks
- Every finalist shows all 7 individual scores.
- SKU/collection scope defaults to descriptive naming unless a documented reason overrides it.
- A brand-scope deliverable is only packaged after clearance, never before.

## Output
`{scored_shortlist: [{name, scores_7}], finalist_mockups, naming_deliverable: {nomenclature_notes, story, tagline} | null for SKU scope}`

## Example
SKU scope: candidate "Everyday Gold-Tone Hoops, 18mm" chosen over a coined name "Aura Hoops" since the descriptive title captures 3 real search terms found in on-site search mining.
