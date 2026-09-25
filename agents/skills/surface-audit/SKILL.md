---
name: surface-audit
owner: Propose (surface-auditor sub-agent); specialists reuse for their domain
version: 1
invoke_when: a break is chosen, or a specialist starts on an approved item
inputs: the break or item; the surface (pages, account, flows, feed, content); the brain snapshot
outputs: observed conditions with evidence, each tagged with the idea signals it could fire
---
# Surface audit

## Steps
1. Pick the audit tool for the surface: speed lab (pages), crawler (site structure, claims, links), account reader (campaigns, ad sets, ads, results), flow reader (email flows, timing, filters), feed checker (product feed), content inventory (posts, pages).
2. Run it. Collect observations as facts with evidence (a number, a screenshot, a quoted setting, a URL).
3. Do not judge. Each observation is a condition, not a verdict.
4. Tag each condition with the bank's signal vocabulary where it matches.

## Checks
- Every condition has evidence a person could verify.
- No fix language.
- Read-only: nothing on the surface changed.

## Output
{surface, conditions[{what, evidence, signal_tags[]}], tool_runs[]}
