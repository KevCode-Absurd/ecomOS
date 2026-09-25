---
name: ai-shopping-assistant
owner: site-specialist
version: 1
invoke_when: operating the founder-approved, on-site pre-purchase AI shopping assistant
inputs: brand brain claims tiers, catalogue/stock/delivery data, founder approval to run it
outputs: weekly transcript and claims review report, hand-off rate report, candidate FAQ list
---
# Run and govern the on-site AI shopping assistant

## Purpose
Run a pre-purchase chat that only ever answers from real, approved data, hands off anything it can't answer safely, and gets checked every week without fail.

## Steps
1. Confirm the founder has approved turning the assistant on, and confirm the claims tiers were reviewed within the last 30 days.
2. Configure the assistant to answer only from the catalogue, stock and claims-tier data, never open web knowledge about the brand.
3. Set the hand-off rule: any question it cannot answer from approved data routes to a person, it never guesses.
4. Keep this surface distinct from any reporting or CRO-analysis assistant so its scope stays fixed.
5. Log every conversation and flag any answer that touched a forbidden-tier claim.
6. Run the weekly transcript and claims review on a real sample of conversations.
7. Report hand-off rate and common unanswered questions to the founder each week, feeding candidates into page-copy work.
8. Pause the assistant and notify the founder immediately on a found violation, not at the next scheduled review.

## Checks
- No answer ever given outside the catalogue, stock and claims-tier data.
- A claims-tier violation pauses the assistant the same day it is found.

## Output
A weekly transcript and claims review report, a hand-off rate report, and a candidate FAQ list.

## Example
"Weekly review: 312 conversations, 4% hand-off rate, 0 claims-tier violations. Top unanswered question: 'do you ship to Nepal', fed to page-copy as a candidate FAQ/policy addition."
