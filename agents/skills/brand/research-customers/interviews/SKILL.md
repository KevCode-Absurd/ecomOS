---
name: research-customers/interviews
owner: BRAND
version: 1
invoke_when: a specific open question needs a live conversation, not passive text mining
inputs: the open question, customer list or panel, founder/team availability
outputs: interview guide, transcript log, interview findings packet
---
# Run customer interviews

## Purpose
Passive sources cannot ask a follow-up question. When the research packet has a real gap, live conversation is the only way to hear the trigger moment or the fired alternative in the customer's own words.

## Steps
1. Write 8-12 open questions in job-to-be-done order: the trigger, the struggle, alternatives tried, the moment of choosing, the after-state. No yes/no questions, no question that names the brand's feature first.
2. Recommend a channel (phone, WhatsApp voice notes, video call) and a proportionate incentive sized against contribution margin, never cash large enough to bias the answer.
3. Recruit 8-12 people across at least 2 recency bands (recent buyer, lapsed buyer), never more than 70% from one band.
4. Hand the guide to whoever runs the calls (founder, team, or a research vendor); this step is human_assist, the agent does not conduct the call itself.
5. Log every transcript with a consent flag before any quote is reused.
6. Extract job statement material, the 4 forces, and the fired alternative from the transcripts, cross-checked against existing passive-data patterns.

## Checks
- No leading questions; no question that fishes for validation of an existing feature.
- Every transcript has a consent flag before reuse.
- Incentive cost is computed against contribution margin, not guessed.

## Output
`{interview_guide, transcript_log: [...], interview_findings_packet}`

## Example
Guide question 3: "Walk me through the day you decided you needed this: what was happening that day?" surfaces a wedding-season trigger moment absent from the review data.
