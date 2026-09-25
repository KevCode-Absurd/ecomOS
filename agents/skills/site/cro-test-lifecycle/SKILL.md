---
name: cro-test-lifecycle
owner: site-specialist
version: 1
invoke_when: a ranked CRO hypothesis is ready to enter the test lifecycle
inputs: ranked backlog (from Propose/registry), traffic and order volume, metric contract
outputs: test intake note, handoff to the matching stage skill
---
# CRO test lifecycle intake

## Purpose
The entry point into the CRO test lifecycle: confirm a hypothesis is real and testable before spending design effort on it.

## Steps
1. Take the top-ranked hypothesis, confirming it carries at least 2 points of evidence.
2. Check the traffic gate: below the sample-size threshold for a real test, recommend a bigger change instead of a small test.
3. Confirm the hypothesis is stated as a full if-then-because statement, not a vague idea.
4. Route it into site/cro-test-lifecycle/stats-design to begin the formal test design.

## Checks
- No hypothesis enters design without 2+ points of evidence.
- A traffic-starved brand gets a bigger-change recommendation, not a small underpowered test.

## Output
A short intake note confirming the hypothesis is ready, handed to the stats-design stage.

## Example
"Hypothesis: 'If we add a fit-confidence line above the size selector, then PDP-to-cart improves, because scroll-map and ticket data both show sizing doubt at that exact point.' 2 evidence points, traffic sufficient. Proceeding to stats design."
