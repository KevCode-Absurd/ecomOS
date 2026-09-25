---
name: ai-agent-governance
owner: LIFE
version: 1
invoke_when: before any AI support agent goes live, and after every policy change
inputs: automation-scope classification, current policy, a sample of real past
  tickets
outputs: operating-procedure document, replay test report, escalation rule set
---
# AI support agent operating-procedure governance

## Purpose
Writes the exact rules an AI support agent may act on for money-moving actions
(refund cap, order-state limits, who approves above the cap), sets escalation
triggers and identity checks, and proves the ruleset works against real tickets
before go-live, and again after every policy change.

## Steps
1. For every agent-can-close contact type touching money or an account change,
   write the hard cap, the approval path above it, and which order states allow
   the action at all.
2. Set the identity-verification step required before any account or payment
   change.
3. Set escalation triggers: negative sentiment, repeated back-and-forth, an
   explicit request for a human, or ticket value above a threshold, with a warm
   hand-off carrying full conversation history.
4. Replay the drafted ruleset against a sample of last quarter's real tickets,
   scoring accuracy and tone before anything goes live.
5. Set a one-step kill switch and rollback plan for if the agent starts producing
   wrong answers.
6. Re-run the replay after every policy or price change; a stale rulebook is how
   an agent promises something the brand no longer offers.

## Checks
Every money-moving rule has a hard cap and an approval path. Replay uses real
tickets. Escalation always carries full history, never a cold restart.

## Output
An operating-procedure document, a replay test report with scores, and an
escalation rule set.

## Example
"Refund cap: ₹2,000 auto-approved if order is delivered and within the return
window; above that, drafts for a human. Replay against 200 past tickets: 94%
correct action, 3 tone flags fixed before go-live."
