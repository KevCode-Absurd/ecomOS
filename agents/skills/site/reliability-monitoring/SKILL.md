---
name: reliability-monitoring
owner: site-specialist
version: 1
invoke_when: gating a theme/app deploy on automated tests, or running continuous uptime and transaction monitoring
inputs: critical-path map, staging theme URL, store URLs by page type, on-call contact
outputs: pass/fail report, visual diff set, bug reports with replay, uptime dashboard, incident log
---
# Automated regression and uptime monitoring

## Purpose
Catch a breaking theme/app change before it ships, and catch a live outage or slow degradation within minutes instead of at the next scheduled hygiene sweep.

## Steps
1. Map the store's critical paths (home, PDP, filter, cart, discount code, checkout, login) into test cases.
2. Run visual diffs across breakpoints and scripted end-to-end flows before and after every deploy, plus nightly.
3. Self-heal a test whose selector changed for a cosmetic reason; flag the ones that fail for a real reason.
4. On failure, capture video replay, console errors and a network trace, and write an actionable bug report.
5. Run synthetic checks every few minutes on home, PDP, cart, checkout and search from more than one region.
6. Run a full transaction walk (add-to-cart through confirmation) on a schedule, not just a page-200 check.
7. Track SSL and DNS separately, and pull real-user page-load data to catch slow-but-not-down degradation.
8. Route any failure or degradation to a human with an escalation path if unacknowledged, logging detect and fix time.

## Checks
- No deploy ships without a green regression run.
- Every incident logs a real detect time and fix time.

## Output
A pass/fail regression report with visual diffs and bug replays, plus an uptime dashboard and incident log.

## Example
"Nightly regression: checkout flow failed on Safari mobile after a tag-manager update. Video replay + network trace attached. Deploy blocked until fixed."
