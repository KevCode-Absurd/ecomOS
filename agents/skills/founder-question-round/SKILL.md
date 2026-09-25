---
name: founder-question-round
owner: shared (Keeper, Orchestrator, Brand strategist)
version: 1
invoke_when: 4 or more open questions exist, or one blocks a running item, or onboarding
inputs: open questions with the gap or conflict each comes from; what was already found
outputs: 4 to 6 questions with options and a recommended answer where one exists
---
# Founder question round

## Steps
1. Rank open questions by what they unblock (money at stake, running items, red lines).
2. Take the top 4 to 6. For each: one plain question, what we already found (so the founder corrects rather than repeats), options as chips, a recommended option if evidence supports one, and "kept private" where the answer is sensitive.
3. Ask in one round. Store every answer as a decision with a date through the Keeper.
4. Close questions that the answers settle. Re-rank the rest.

## Checks
- No question the brain can already answer.
- Every question names what it unblocks.
- Under grade 10 reading level.

## Output
{questions[{text, found, options[], recommended, private}]}
