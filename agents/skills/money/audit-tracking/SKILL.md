---
name: money/audit-tracking
owner: MONEY
version: 1
invoke_when: a tracking surface needs its recurring configuration and event-quality audit
inputs: metric contract key events, the surface's live config, consent config
outputs: checklist result, event mapping, debug test result, ranked fix list
---
# Audit a tracking surface

# Purpose
GA4, Meta pixel and CAPI, Google Ads and server-side tagging each drift on their own schedule. This skill is the dispatcher that sends the audit to the right surface-specific checklist and never applies a fix itself.

## Steps
1. Match `select_by.surface` to ga4, meta-capi, google-ads or server-events and hand off to that child skill.
2. Pull the surface's current live configuration, dated.
3. Run the fixed checklist for that surface.
4. Verify every store event (purchase, add to cart, lead) maps to that surface's own standard or key event, with value passed through.
5. Test the live setup in the surface's own debug tool (DebugView, Test Events, or the Google Ads diagnostics tab).
6. Build the ranked fix list: current setting, proposed setting, and who applies it.

## Checks
- Every checklist item returns pass, fail or unavailable, never skipped.
- No tracking configuration is changed; only the fix list is produced.
- A fix names the surface it touches.

## Output
Surface, checklist result, event mapping table, debug test result and a ranked fix list.

## Example
A GA4 audit finds `page_view` still marked as a key event, inflating the key-event count; the fix list names the exact setting to unmark, for a person with GA4 admin access to apply.
