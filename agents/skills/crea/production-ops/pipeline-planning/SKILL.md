---
name: production-ops/pipeline-planning
owner: crea-paid-creative-copy
version: 1
invoke_when: the monthly creative slate needs sizing and sequencing from real
  account data
inputs: hit-rate table by format/angle, coverage gap list, monthly budget
  line
outputs: monthly production plan, sequenced pipeline calendar
---
Purpose: size how much creative to make next month from this account's own
real hit rate and budget, rather than a fixed monthly quota that ignores
whether last month's creative actually worked.

Steps
1. Compute next month's target volume from the hit rate (how often a tested
   concept actually wins) and the budget line, shown as an explicit
   calculation the founder can check, not a stated number alone.
2. Lay the month out across its real stages: research, concept, build,
   variations, feedback, launch, each with a calendar date.
3. Assign an owner to every stage, whether that is CREA itself, a specific
   sub-agent, or a human collaborator like a shoot crew.
4. Cross-check the planned volume against the current cost-per-asset trend so
   a likely overrun is visible before the month starts, not discovered at
   month end.

Checks: volume is a shown calculation, not an assertion; every stage has a
date and an owner.

Output: the monthly production plan and its sequenced calendar.

Example: a 22% hit rate and a fixed budget of a stated amount computes to a
target of 18 new concepts this month, laid out across 4 weekly stages.
