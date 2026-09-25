---
name: ai-build-guardrail
owner: site-specialist
version: 1
invoke_when: an AI coding agent (Wiz, a Claude Code session, or similar) is about to change the storefront
inputs: brand brain full product and policy record, brand voice guide
outputs: AI build brief, QA pass report, change log
---
# AI build-agent guardrail

## Purpose
Keep an AI coding agent's storefront work safe and reviewable: real inputs, one change at a time, private preview, and manual QA before anything the agent wrote reaches a customer.

## Steps
1. Write a brief with the real product, policy and voice inputs the agent needs; never send it in with a bare one-line prompt.
2. Let the agent interview and propose a plan before it starts building.
3. Ask for exactly one storefront change per prompt, and verify each one live before the next.
4. Preview every change privately; never let the agent's output reach the public URL directly.
5. Treat the AI-authored section as a draft: run mobile QA and a claims check (shared/claim-check) on it.
6. Plan long sessions around a possible usage-limit pause so a half-finished change isn't left live.

## Checks
- Every AI-authored section passed a claim check before merge.
- No public URL ever served an unreviewed AI change.

## Output
The AI build brief used to start the session, a QA pass report, and a change log entry per shipped edit.

## Example
"Brief: rebuild the size-chart tab using the real size data in brand.json. Agent proposed a plan, built on a duplicate theme, previewed privately, claim-check passed, merged via reviewed PR."
