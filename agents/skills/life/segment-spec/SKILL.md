---
name: segment-spec
owner: LIFE
version: 1
invoke_when: building or refreshing any segment the flows or campaigns draw from
inputs: order/ESP event data, metric contract
outputs: segment definition {name, logic, expected_size, refresh_cadence, used_by}
---
# Segment build

## Purpose
Builds and documents every standing segment (RFM tiers, buyer stage, VIP, win-back-
potential, high-potential, location, engaged audience) so flows and campaigns pull
from one shared, current definition instead of a one-off list.

## Steps
1. Score RFM tiers and buyer stage from order recency/frequency/monetary data, in
   code, against a fixed threshold script.
2. Score win-back-potential against the customer's own historical order gap, not a
   flat day count; score high-potential from early LTV-matching traits.
3. Build the location segment from shipping address, not billing.
4. Cross-check every segment against the flows/campaigns that use it.
5. Write the segment definition and push the refreshed membership to the ESP.

## Checks
All scoring in code. Every segment cites the real fields behind it. No segment is
referenced by a flow that no longer exists, or vice versa.

## Output
{name, logic (AND/OR, cited fields), expected_size, refresh_cadence, used_by}

## Example
{"name": "win-back-potential", "logic": "days_since_last_order > 1.5x customer_avg_gap
AND no_open_last_30d = false", "expected_size": 340, "refresh_cadence": "weekly",
"used_by": ["LIFE-W04:win-back"]}
