---
name: partnership-screen
owner: BRAND
version: 1
invoke_when: a specific collaboration, licensee, or ambassador proposal needs screening and reputation clearance
inputs: the candidate or proposed partner, brand story
outputs: overlap verdict, narrative fit verdict, reputation check result, collaboration brief
---
# Partnership and reputation screen

## Purpose
This skill screens any proposed relationship with the brand's name attached to someone else's, whether a one-off collaboration, an ongoing licensee, or an ambassador, using the same category-overlap, narrative-fit and reputation checks.

## Steps
1. Check the candidate for direct category overlap; default to treating non-competitive brands as the safer fit.
2. Check narrative fit: does the collaboration tell a story either brand's customer would actually want, not just a co-marketing convenience.
3. Run a public reputation and controversy check on the other party before any agreement moves forward or any ambassador is onboarded; a flag here stops the process for founder review.
4. If screened favorably, draft what the collaboration would look like: format, duration, what each side contributes, rough terms, stating the specific customer value, not just brand exposure.
5. For an already-approved, ongoing relationship (a licensee, an active ambassador), re-run the reputation check yearly, on schedule, not only when a problem is already visible.

## Checks
- Overlap verdict is explicit: none, adjacent, or competing.
- A reputation flag halts the process until the founder reviews it.
- Ongoing relationships get a scheduled yearly re-check, not just a one-time screen at signing.

## Output
`{overlap_verdict, narrative_fit_verdict, reputation_check_result, collaboration_brief}`

## Example
Ambassador candidate screens clean on overlap and narrative fit; reputation check finds a 2-year-old public controversy unrelated to the brand's category: routed to founder for a judgment call rather than an automatic pass or fail.
