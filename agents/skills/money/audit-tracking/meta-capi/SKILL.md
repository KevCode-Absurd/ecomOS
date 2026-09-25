---
name: money/audit-tracking/meta-capi
owner: MONEY
version: 1
invoke_when: the tracking audit's surface is Meta pixel and CAPI
inputs: Meta pixel/CAPI config, dataset quality read, consent config
outputs: dedup, event match quality and standard-event mapping result
---
# Audit Meta pixel and CAPI

## Purpose
A browser pixel and a server-side CAPI event for the same purchase must dedup correctly, or Meta double-counts conversions and the reported ROAS is wrong.

## Steps
1. Read dataset quality and event match quality with the read-only Meta MCP tools (`ads_pixel_event_read`, `ads_get_dataset_quality`, `ads_get_dataset_stats`). Never call a write tool.
2. Check that pixel and CAPI events for the same action share the same event ID for deduplication.
3. Confirm every store event maps to a Meta standard event (Purchase, AddToCart, Lead) with value and currency passed.
4. Confirm consent gating blocks the event until consent is given, matching the banner.
5. Fire a real test event and confirm it appears in Meta's Test Events tool.

## Checks
- Dedup is confirmed by matching event IDs, never assumed from setup screenshots.
- Event match quality is read from the platform, never estimated.
- Only read tools are used; this skill never creates, updates or activates anything.

## Output
Dedup check, event match quality score, standard-event mapping table, consent gating check and test event result.

## Example
Event match quality reads low because the CAPI event sends no phone or email hash; the fix list names the exact hashed parameter to add server-side.
