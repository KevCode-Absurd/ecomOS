---
name: community-response-drafting
owner: ORG
version: 1
invoke_when: a new batch of comments or DMs is waiting, daily
inputs: comment/DM queue, brand voice file, policy/FAQ answers, current stock and shipping status
outputs: drafted replies with a concrete next step, flagged items for the founder
---
# Community comment and DM response drafting

## Purpose
Draft fast, specific replies so a human sends within the hour, not a generic "thanks so much!" that answers nothing, while keeping any DM automation inside current platform rules.

## Steps
1. Sort the queue: product question, complaint, praise, spam/bot, sales-ready lead.
2. Draft a specific answer to every product question, linking to the matching page where relevant.
3. Draft complaint replies that acknowledge the specific issue and give a real next step (order lookup, replacement policy, DM), not a scripted apology.
4. Draft the reply plus DM hand-off line for sales-ready leads, using any already-approved comment-to-DM funnel.
5. Check DM automation in use against the current platform's rate-limit and disclosure policy before it fires again.
6. Queue every draft for a human to send; flag PR risk, refund exceptions or legal threats for the founder instead of drafting a reply.

## Checks
- No generic reply on a specific question.
- Every complaint reply names a next step.
- DM automation policy checked, not assumed.

## Output
{drafts[], flagged_for_founder[]}

## Example
Comment "does this fit a Maruti Swift boot?" gets a specific reply with the folded dimensions and a link to the size guide, not "thanks for reaching out!".
