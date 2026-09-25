---
name: plain-english-card
owner: shared (Propose and Orchestrator)
version: 1
invoke_when: anything is shown to a founder as a decision
inputs: proposal record (idea, evidence, effect, effort, cost, risk, metric, read point, owner)
outputs: card text and buttons
---
# Plain-English card

## Purpose
A founder decides in 30 seconds without a call. Heading plus 2 to 4 sentences.

## Steps
1. Heading: the action, 6 to 10 words, no jargon ("Turn off the script setting that delays your menu").
2. Sentence 1: what we saw, with the number and where it came from.
3. Sentence 2: what it would change and how sure we are (measured, source, general practice).
4. Sentence 3: what it costs and what could go wrong, and whether it can be undone.
5. Optional sentence 4: what it needs first (access, photos, a person).
6. Pills: effect basis, effort, risk, needs write, owner.
7. Buttons: "Let the agent do it" (only if autonomy allows), "Send to <person>", "Not now".

## Checks
- No acronym without its plain meaning on first use.
- Reading level under grade 10. Sentences under 20 words.
- No number that is not in the record.
- The heading is an action, not a topic.

## Output
{heading, body, pills[], buttons[], registry_stub}
