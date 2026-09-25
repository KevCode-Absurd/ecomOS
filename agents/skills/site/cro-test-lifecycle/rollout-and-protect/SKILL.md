---
name: rollout-and-protect
owner: site-specialist
version: 1
invoke_when: a test has been read as a winner and is ready to ship, or a quarterly check on past winners is due
inputs: result read report, shipped test, registry of past winners
outputs: winner register entry, quarterly protection check report
---
# Roll out winners and protect them over time

## Purpose
Ship a winner properly and prove it stays a winner, since a shipped test can silently regress or get overwritten by a later, unrelated change.

## Steps
1. Ship the winner as the new control for the next challenger test.
2. Re-audit the page after the change ships.
3. Re-verify with fresh session recordings, funnel rate and a re-survey once real post-ship data exists.
4. Run an LTV and returns check before scaling any angle- or claim-driven win, since a short-term lift can mask a long-term return problem.
5. Keep a live-winner register of every shipped test.
6. Re-check quarterly that every past winner is still live and unbroken by a later change.
7. Set founder expectations at a 10-20% win rate for PDP/cart/checkout tests, so a string of inconclusive tests doesn't read as failure.

## Checks
- Re-verification happens after shipping, not assumed from the pre-ship test result.
- Every past winner is re-checked live at least once a quarter.

## Output
A winner register entry per shipped test, and a quarterly protection check report.

## Example
"Q3 protection check: 6 of 7 shipped winners still live and measuring as expected. 1 (free-shipping bar) was overwritten by an unrelated theme update in August; restored and re-verified."
