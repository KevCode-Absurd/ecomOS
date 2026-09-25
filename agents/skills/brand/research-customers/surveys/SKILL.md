---
name: research-customers/surveys
owner: BRAND
version: 1
invoke_when: an existing finding needs confirming at scale, never to discover a new job
inputs: a specific hypothesis, email/SMS platform (draft only), segmented customer list
outputs: survey question set, cleaned response set, confirm/deny result with sample size
---
# Run customer surveys

## Purpose
A survey is for confirming a pattern already found in reviews, tickets, social or interviews across a much larger sample. It is never the first place a new job or objection is discovered; fishing questions produce noisy, self-reported answers.

## Steps
1. Write the one claim the survey exists to test, drawn from an existing qualitative finding.
2. Pick the format: identity survey (who are you), post-purchase (why this, why now), or NPS/relationship (would you return). Keep to 6 questions or fewer, no double-barreled questions.
3. Draft the send in the email/SMS platform connector, which is read-and-draft only; it cannot send.
4. Founder reviews the draft and sends it themselves or approves the send explicitly.
5. Once the window closes, pull responses and drop straight-line or under-10-second junk responses, reporting the junk rate.
6. Score the confirm/deny result in code against the original hypothesis, with the real sample size shown, never rounded up to "most customers."

## Checks
- 6 questions or fewer.
- The survey confirms an existing finding; it never opens with "what do you want."
- No send happens without explicit founder approval.

## Output
`{survey_question_set: [...], cleaned_response_set, confirm_deny_result: {rate, n, hypothesis}}`

## Example
Hypothesis: "gifting is the top occasion for tier-2 city buyers." Survey of 40 questions sent to 600, 210 responses, 8% junk dropped: confirm rate 61% (n=193), reported as-is, not rounded to "most."
