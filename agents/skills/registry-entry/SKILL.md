---
name: registry-entry
owner: Registrar
version: 1
invoke_when: a decision is made on a card, or an artefact is delivered
inputs: card id, decision, person, reason; metric, read point, stop and scale rule
outputs: registry entry
---
# Registry entry

## Steps
1. Create or update the entry: idea id (or audit or web source), brand, status, owner, artefact link, metric, read point, kill rule, scale rule, founder reason verbatim, date, person.
2. If parked, set an expiry from the reason using the reasons table; if none applies, 90 days.
3. Link the previous entry for the same idea on this brand.

## Checks
- Metric is a contract field. Read point is a date or a count.
- Reason stored verbatim, weight looked up in code.

## Output
Entry JSON.
