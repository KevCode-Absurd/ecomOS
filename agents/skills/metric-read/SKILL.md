---
name: metric-read
owner: shared
version: 1
invoke_when: any number is quoted to a founder or compared to a rule
inputs: contract field, window
outputs: value with window, freshness and basis, or unavailable
---
# Metric read

## Steps
1. Ask the contract for the field and window. Windows end on the last full day.
2. If missing or unsupported, return unavailable with the source that would provide it.
3. Return value, window start and end, computed at, and the formula name.

## Checks
- Never compute in the model. Never return 0 for missing.
- Period ratios come from totals, never from averaging breakdowns.

## Output
{field, value|unavailable, window, freshness, formula, source_needed}
