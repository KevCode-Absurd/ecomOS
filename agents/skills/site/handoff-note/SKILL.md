---
name: handoff-note
owner: site-specialist
version: 1
invoke_when: a store-setup, hygiene, or catalogue audit surfaces a finding outside Site's 4 owned folders
inputs: the finding and its evidence
outputs: one short note per finding, filed to the registry for the owning specialist
---
# Route an out-of-scope finding to the owning specialist

## Purpose
Hand off a finding that belongs to another specialist, with the evidence, instead of quietly dropping it or executing it outside Site's real expertise.

## Steps
1. Name the right owning specialist: Lifecycle (welcome/cart-recovery/win-back automation, VIP segmentation), Organic (organic social cadence, technical SEO), Product (pre-build demand validation), Brand strategist (a full repositioning call), or Money and ops (broader measurement/P&L tracking).
2. Package the observed condition and its evidence, not a finished brief the other specialist didn't ask for.
3. State plainly why this is not Site's job, in one sentence.
4. File the note to the registry so the owning specialist can pick it up on their own schedule.

## Checks
- The note names a specific owning specialist, not a vague "someone should look at this".
- Evidence is attached, not just an assertion.

## Output
One short handoff note per finding: {finding, evidence, which specialist, why it is theirs not Site's}.

## Example
"Finding: no cart-recovery email sends after checkout abandonment (30 days of Shopify data show 0 sends). Evidence: attached export. Routes to: Lifecycle. Why: automated recovery messaging is Lifecycle's folder, not Site's."
