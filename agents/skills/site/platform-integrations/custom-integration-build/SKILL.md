---
name: custom-integration-build
owner: site-specialist
version: 1
invoke_when: a manual double-entry process is found and no off-the-shelf app covers the connection cleanly
inputs: external system's API docs, field mapping, sandbox credentials
outputs: working integration or Flow, webhook retry log, data contract doc, sync-health alert
---
# Build a custom integration or webhook

## Purpose
Connect the store to an ERP, warehouse system, loyalty ledger, marketplace feed or courier safely, with retries and alerting instead of a silent, brittle one-way sync.

## Steps
1. Map every field that must sync both ways (inventory, order status, tracking number, loyalty points) before writing any code.
2. Build the custom app or Shopify Flow automation and register the needed webhooks.
3. Store API keys and tokens only in the platform's secure app settings or the environment secret store, never in theme code or a public repo.
4. Add retry-with-backoff on failed webhook deliveries, with a dead-letter log for ones that never succeed.
5. Alert a human the moment a sync gap is detected (order count mismatch, stale inventory timestamp).
6. Document the data contract so a future developer does not reverse-engineer it.
7. Test against a sandbox or staging account of the external system before pointing at production.

## Checks
- No credential appears outside the platform's secure settings.
- A deliberately failed test webhook triggers the retry logic and, if it keeps failing, a human alert.

## Output
A working integration or Flow, a retry log, a written data contract, and a sync-health alert rule.

## Example
"Inventory sync to the 3PL's WMS: field-mapped SKU, quantity, location. Retry with exponential backoff up to 5 attempts, dead-letter log after that, Slack alert to ops on any dead-letter entry."
