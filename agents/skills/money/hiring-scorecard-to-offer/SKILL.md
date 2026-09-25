---
name: money/hiring-scorecard-to-offer
owner: MONEY
version: 1
invoke_when: a hire trigger fires and a structured search needs to run
inputs: silo ownership map, role library, annual budget, candidate applications
outputs: job description, scorecard, job ad, interview questions, or scored candidate table, by stage
---
# Run structured hiring from scorecard to offer

## Purpose
Turn a hiring decision into a repeatable process with one governing metric per role, so a hire is never made on gut feel alone.

## Steps
1. Confirm the hire trigger fired: a stated number crossing a stated threshold.
2. Build the job description naming the silo, the artefacts owned, and one metric the role is judged on.
3. Set the comp band from the role library and the current OPEX budget.
4. Write an honest job ad matching the scorecard exactly, and a sourced interview question set tied to that one metric.
5. Score every candidate against the scorecard, citing the specific answer behind each score.
6. Recommend the top-scored candidate with the score gap to the next candidate, then stop.

## Checks
- The hire trigger is always a number.
- The scorecard names exactly one governing metric.
- No candidate is contacted by this skill; the founder makes every offer and rejection.

## Output
The stage's artefact: job description and scorecard, job ad, interview question set, or scored candidate table with a recommendation.

## Example
Two candidates score close on the interview set; the recommendation states the 4-point gap and which specific answer drove it, leaving the final call to the founder.
