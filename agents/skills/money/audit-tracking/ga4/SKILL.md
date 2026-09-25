---
name: money/audit-tracking/ga4
owner: MONEY
version: 1
invoke_when: the tracking audit's surface is GA4
inputs: GA4 property/stream config, GTM container export, sample event log
outputs: GA4-specific checklist result and DebugView test
---
# Audit GA4 tracking

## Purpose
Catch broken or misconfigured GA4 settings before they corrupt a report someone reads with confidence.

## Steps
1. Confirm one property exists per customer journey, not one property doing double duty.
2. Check timezone, data retention window, and that internal and staff traffic is filtered out.
3. Confirm consent mode gating matches the live consent banner's states.
4. Confirm enhanced measurement is on and ecommerce parameters (item, value, currency) are present on purchase events.
5. Confirm key events are the real conversion actions; `page_view` is never marked as one.
6. Fire a real test session and confirm it appears correctly in DebugView.

## Checks
- One property per journey.
- Internal traffic is filtered, confirmed by a live check.
- No `page_view` marked as a key event.

## Output
A checklist result per item plus the DebugView test outcome.

## Example
DebugView shows a purchase event firing with `value: 0` because the ecommerce parameter was not mapped from the checkout's order total; the fix list names the exact parameter to map.
