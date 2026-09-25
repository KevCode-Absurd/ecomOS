---
name: rank-candidates
owner: Propose
version: 1
invoke_when: candidates from bank, audit and web are assembled with evidence fields
inputs: candidates with reach, effect basis and size, brand prior, effort, cost, risk, reversibility, confidence, dependencies, founder weight
outputs: sorted list with score parts, in code
---
# Rank candidates

## Steps
1. Ensure every candidate has every field; a missing field gets the conservative default and a flag.
2. Run the ranker in code (intelligence/ideas.py rank): expected marginal improvement on the break's metric, given the conditions and the candidates already above it.
3. Apply dependencies: an idea whose prerequisite is unmet ranks below its prerequisite.
4. Return the sorted list with the score parts visible.

## Checks
- Source field carries no weight.
- No arithmetic in the model.
- Flags listed for defaulted fields.

## Output
{ranked[{id, score, parts{}, flags[]}]}
