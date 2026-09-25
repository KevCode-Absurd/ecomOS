---
name: avatar-record-builder
owner: BRAND
version: 1
invoke_when: a new avatar record is assembled, or an existing one is due for cadence refresh/audit
inputs: job statement and forces (build); current record and brief citation log (refresh)
outputs: full avatar record with status field (provisional|confirmed)
---
# Avatar record builder

## Purpose
This is the single procedure that turns scattered research into the one record every other specialist cites, and the same procedure that keeps that record honest over time instead of going stale silently.

## Steps (build mode)
1. Pull the job statement, forces, fired alternative, objection map, 5W profile and trigger moment from the upstream skills and research packets.
2. Assemble them into one record with a full quote set attached to every claim.
3. Check the source-type count: at least 2 independent source types, with at least one first-party source (the brand's own reviews, tickets, or search data) if this is an existing brand with real customers.
4. Set the status flag: "confirmed" only if the source-count bar is met; otherwise "provisional," stated plainly.

## Steps (refresh mode, quarterly cadence)
1. Audit which briefs and pages have cited this record since the last audit.
2. Retrace whether the product still earns the win the record describes (has anything changed: price, formulation, competitor claims).
3. Check evidence freshness; anything older than 2 quarters is flagged.
4. If stale, route back to the research workflow for fresh evidence rather than editing the record from memory or assumption.

## Checks
- Every required field is present or explicitly marked missing, never silently invented.
- The status flag matches the real source count.
- A refresh never rewrites a field without new supporting evidence behind it.

## Output
`{avatar_record: {job, forces, fired_alternative, objection_map, 5w, trigger_moment, quotes, status: provisional|confirmed}}`

## Example
Refresh audit finds the objection map's "delivery delay" pairing cites a policy fixed 14 months ago that has since regressed (returns log shows the same complaint rising again); flagged for a fresh tickets-mining pass before the record is reused.
