---
name: social-listening-digest
owner: ORG
version: 1
invoke_when: continuous monitoring, rolled into a weekly digest
inputs: brand and competitor name list, category keyword list, public social/review/forum sources
outputs: weekly digest of trends and sentiment shifts, postable ideas, same-day risk flags
---
# Social listening for brand, competitor and category trends

## Purpose
Spot a real trend or sentiment shift before it becomes a problem or a missed opportunity, using conversation the brand does not own (public social, reviews, forums), kept separate from AI-answer-engine monitoring.

## Steps
1. Monitor mentions of the brand, named competitors and category terms across public sources.
2. Classify each: sentiment, topic, and whether it is a postable idea or a risk signal.
3. Track shifts week over week; a single post is noise, not a trend.
4. Draft the weekly digest with 3-5 postable ideas, each sourced from a quoted, dated mention.
5. Send anything reading as PR or reputation risk to the founder immediately, not folded into the weekly digest.

## Checks
- Trend claims need a week-over-week pattern, not one post.
- Every idea traces to a real quoted mention.
- Risk flags go out same-day.

## Output
{digest{}, risk_flags[]}

## Example
Three unrelated posts this week compare the brand's price unfavourably to a named competitor's new launch: flagged as a sentiment shift, with a same-day risk note if a fourth appears with high engagement.
