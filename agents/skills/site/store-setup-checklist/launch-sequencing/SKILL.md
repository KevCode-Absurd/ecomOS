---
name: launch-sequencing
owner: site-specialist
version: 1
invoke_when: pre-launch, once every setup workflow has produced its own checklist
inputs: brand brain full setup record, outputs of SITE-W01 through SITE-W07
outputs: launch checklist with pass/fail, go/no-go recommendation
---
# Pre-launch QA and launch sequencing

## Purpose
Prove, with real customer actions, that a store is actually ready to sell, and give one clear go or no-go call before the password comes off.

## Steps
1. Pull every prior setup workflow's result into one dependency-ordered list.
2. For each line, perform the real action a customer would take (browse, add to cart, pay, receive an email) rather than checking a setting.
3. Run a full mobile QA pass across the brand's real device split.
4. Check the logged-out storefront in an incognito window, clicking every visible element.
5. Compile the pass/fail table.
6. Give one clear go or no-go call, naming any blocking failure.
7. Remove the storefront password only once every line passes.

## Checks
- Every line closed with a real action, not an admin-panel glance.
- No password removal before 100% pass.
- The go/no-go call is unambiguous.

## Output
A pass/fail table plus a one-line go/no-go recommendation with any blocker named.

## Example
"38 of 38 checks pass. Go. Password removed 14:02 IST, confirmed by a live incognito purchase test immediately after."
