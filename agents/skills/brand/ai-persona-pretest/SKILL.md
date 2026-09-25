---
name: ai-persona-pretest
owner: BRAND
version: 1
invoke_when: a messaging, naming or concept shortlist needs a cheap sanity check before a real, paid research round
inputs: shortlist to pretest, avatar record, budget ledger
outputs: persona brief, simulated reaction notes, flagged misses, trimmed shortlist
---
# AI-persona pretest

## Purpose
This is a cheap filter, not a substitute for real research. It catches obvious misses (confusing wording, an unintended reading, a flat concept) before money is spent on a real survey, interview round, or test, and it is never allowed to be mistaken for real customer signal.

## Steps
1. Check the budget ledger before running any paid pass.
2. Build the simulated persona strictly from the existing avatar record's job, forces and real quotes; never from a generic stereotype or an assumed demographic.
3. Run the persona against the messaging, naming or concept shortlist and record its reactions.
4. Use the pass only to flag obvious misses; never to rank or declare a winner among the shortlist, since this is simulated, not real, data.
5. State plainly that the planned real survey, interview or test round still happens; this pretest only trims the shortlist first.

## Checks
- The persona is built from real avatar-record evidence, never a stereotype.
- Every output is labeled "simulated, not a real customer" everywhere it is shown.
- The real research round is never skipped because of this pretest.

## Output
`{persona_brief, simulated_reaction_notes, flagged_misses_list, trimmed_shortlist}`

## Example
Pretest flags that tagline candidate B reads, in the simulated persona's reaction, as implying a health claim the brand cannot back: dropped from the shortlist before it reaches the real message test.
