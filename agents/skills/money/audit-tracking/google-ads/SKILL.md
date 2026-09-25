---
name: money/audit-tracking/google-ads
owner: MONEY
version: 1
invoke_when: the tracking audit's surface is Google Ads
inputs: Google Ads conversion action list, enhanced conversions config, GTM container export
outputs: conversion action and enhanced-conversions checklist result
---
# Audit Google Ads conversion tracking

## Purpose
A wrong or duplicated primary conversion action skews every bid strategy built on it.

## Steps
1. Confirm exactly one primary purchase conversion action is set; flag any duplicate or secondary action miscounted as primary.
2. Confirm enhanced conversions pass the real order value through, not an estimated average order value.
3. Pick the tracking route (native app SDK, GTM, or server-side container) that matches the brand's current spend level; a small brand rarely needs full server-side tagging yet.
4. Check for conflicting or overlapping conversion actions counting the same purchase twice.
5. Confirm the setup in the Google Ads diagnostics tab with a live test conversion.

## Checks
- One primary purchase action, confirmed live.
- Order value is the real total, never an estimate.
- The tracking route is justified by the brand's spend level, not left as whatever was set up first.

## Output
Primary action check, enhanced conversions check, chosen tracking route with justification, duplicate action check and diagnostics result.

## Example
Two conversion actions are both marked primary after a past migration; the fix list names which one to demote so bidding does not double-count purchases.
