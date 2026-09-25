---
name: money/utm-link-hygiene
owner: MONEY
version: 1
invoke_when: campaign links need a fixed convention or an audit against it
inputs: brand channel list, campaign link export, GA4 channel report
outputs: UTM convention, link audit table, cleaned channel table
---
# Write and audit the UTM convention

## Purpose
A missing or inconsistent UTM turns paid traffic into fake organic or direct traffic in every report downstream. This skill keeps the convention fixed and the links clean.

## Steps
1. Write one convention for source, medium, campaign, content and term, with a fixed value set for each.
2. Audit every existing paid and owned link against that convention.
3. List every non-conforming link with its exact fix.
4. Clean the channel table of fake organic or direct rows traced to a broken UTM, before it is published.

## Checks
- Every UTM parameter has a documented, fixed set of allowed values.
- No channel report goes out with a known UTM leak still unflagged.

## Output
The convention document, the link audit table, and the cleaned channel table.

## Example
A large chunk of 'direct' traffic in GA4 traces to an email campaign sent without any UTM; the cleaned table reclassifies it and the audit flags the sending tool's default settings as the cause.
