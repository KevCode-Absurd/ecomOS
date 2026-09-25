---
name: money/attribution-survey-build
owner: MONEY
version: 1
invoke_when: the attribution model needs a zero-party data source or a new channel needs proof it drives sales
inputs: attribution gap report, product lines, order volume
outputs: survey question and branching, sample plan, channel-share table
---
# Build the post-purchase attribution survey

## Purpose
Ask the customer directly when platform attribution and GA4 keep disagreeing, and turn the answer into a real number instead of an anecdote.

## Steps
1. Draft the one question: how did you hear about us, in plain language.
2. Branch the answer options by product or customer type where the channel mix genuinely differs.
3. Set the minimum sample size and response window before any channel-share number is trusted.
4. Turn the collected answers into a channel-share percentage, computed in code.

## Checks
- The question stays one sentence.
- Every channel-share percentage is shown with its sample size.

## Output
The survey question and branching, the sample and window plan, and the resulting channel-share table.

## Example
A new influencer channel claims a large share of new customers on the platform's own dashboard; the survey after 400 responses shows only 9 percent of customers cite it, prompting a closer look at the platform's attribution window.
