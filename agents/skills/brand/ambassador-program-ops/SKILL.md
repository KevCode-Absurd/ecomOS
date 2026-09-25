---
name: ambassador-program-ops
owner: BRAND
version: 1
invoke_when: an approved ambassador or community program needs its weekly operations run
inputs: approved program design, applicant list, brand guidelines/voice sheet, reward schedule and budget cap
outputs: screened applicants, task assignments, approved content list, rewards ledger
---
# Ambassador and advocacy program operations

## Purpose
Once a program is approved, it needs consistent weekly running: the same screening bar for every applicant, the same guideline check on every submission, and a rewards ledger that never quietly exceeds its cap.

## Steps
1. Screen every new applicant against the program's membership criteria, applying the same bar to everyone; any exception needs a founder note, never an ad hoc call.
2. Assign the week's content or advocacy tasks to active ambassadors, matched to what each one does well.
3. Check submitted content against the brand guidelines and voice sheet (via `shared/claim-check` for any factual claim) before it is approved for reward or reposting; a rejection gets a specific, usable reason.
4. Track what each ambassador is owed against what they delivered, computed in code, checked against the program's budget cap.
5. Flag when the program is approaching its budget cap or when submission volume is outpacing the team's capacity to review it, before either limit is actually hit.

## Checks
- The same screening criteria apply to every applicant.
- Rewards are computed in code and checked against a real, approved budget cap.
- A capacity or budget flag is raised proactively, at 90% of the cap, not after it is exceeded.

## Output
`{screened_applicant_list, task_assignments, approved_content_list, rewards_ledger}`

## Example
Week 6: rewards ledger at ₹38,000 of a ₹45,000 monthly cap with 9 days left in the cycle: capacity flag raised for founder awareness before new task assignments go out.
