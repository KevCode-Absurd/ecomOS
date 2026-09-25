---
name: report-section
owner: Orchestrator (weekly review, client report)
version: 1
invoke_when: a review or report is assembled
inputs: registry entries in the window; contract fields; the current top 10
outputs: three lists: what we did, what it did, what is next; numbers locked
---
# Report section

## Steps
1. What we did: every registry entry that moved to running or delivered in the window, one line each, with the owner.
2. What it did: every read in the window, one line each with the number and the window. Pending reads listed as pending, never as results.
3. What is next: the current top 10 with who each waits on.
4. Numbers: from the contract only, with windows and freshness. Unavailable stays unavailable.

## Checks
- No number outside the contract or the registry.
- No adjective on a result; the number speaks.
- Reading level under grade 10.

## Output
{did[], did_it[], next[], numbers{}}
