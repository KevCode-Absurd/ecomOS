---
name: store-setup-checklist
owner: site-specialist
version: 1
invoke_when: any store setup or configuration task in 05-SET (platform choice, foundation, domain, catalogue, architecture, markets, consent)
inputs: brand brain section relevant to the task, a live connector read, the idea-bank items for that section
outputs: checklist table {item, pass/fail, evidence, fix}, summary line
---
# Store setup checklist

## Purpose
Turn a setup or configuration task into an evidence-based pass/fail list instead of a settings-page glance, so nothing is marked done without being read.

## Steps
1. Pull the idea-bank items and required-state rules for the section in question.
2. Read the live configuration through the platform connector (Shopify Admin, WooCommerce REST API).
3. Compare live state to required state, one field or setting at a time.
4. For every fail, write down the exact evidence (the value read, the value required).
5. Write the fix, sized to whether a person or the founder needs to act.
6. Mark pass only where a live read confirmed it.

## Checks
- No item marked pass from memory or a settings screenshot alone.
- Every fail has a concrete, actionable fix.
- Evidence is dated so staleness is visible later.

## Output
A checklist table plus a one-line summary a founder can read in 10 seconds.

## Example
"Payment capture timing: FAIL. Live value: manual capture. Required: automatic within 3 days. Fix: change capture setting in Shopify Payments settings, 2 minutes, no dependency."
