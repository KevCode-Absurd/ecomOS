---
name: launch-qa
owner: site-specialist
version: 1
invoke_when: a designed CRO test is about to go live
inputs: test design spec
outputs: launch QA checklist, go/no-go
---
# QA and launch a CRO test

## Purpose
Catch the technical failures that quietly ruin a test before it starts, not after it has run for a week.

## Steps
1. QA the test 2-3 times on real devices, both arms, not the browser dev-tools emulator alone.
2. Confirm tracking fires correctly in both arms, checked with a live event inspector.
3. Check for visual flicker on a slow mobile connection.
4. Check the marketing calendar for any promo or holiday overlap with the test window.
5. Run an A/A test first when starting a new testing programme or switching testing tools.
6. Give a clear go/no-go call.

## Checks
- Tracking confirmed firing in both arms before go-live.
- Test window checked against the promo calendar.

## Output
A launch QA checklist and a go/no-go decision.

## Example
"Flicker check on 3G: variant B's hero swap visible for 180ms before hydration. Fixed with a CSS-only swap before launch, re-tested clean."
