---
name: platform-integrations
owner: site-specialist
version: 1
invoke_when: vetting the app stack, wiring a no-code automation, tracking a platform release, or QA-ing a mobile app release
inputs: connector: shopify admin apps list, brand brain app inventory, platform release notes
outputs: app audit report, working automation rules + audit log, adopt-or-ignore memo, app release QA report
---
# Platform, app and automation governance

## Purpose
Keep the store's app stack lean, its small operational rules automated without custom code, and its platform surface current, all under one governance discipline.

## Steps
1. Vet any candidate app against ratings and a real before/after speed test, never install on trust alone.
2. Consolidate apps doing the same job, and search for residual theme code after every uninstall.
3. List recurring manual if-this-then-that actions a store manager does by hand.
4. Wire each into the platform's native automation layer (Shopify Flow or equivalent), never a custom-coded rule for pure logic.
5. Test each rule against a real historical order before turning it on live, and log every action it fires.
6. Read each platform release (Shopify Editions, WooCommerce/WordPress core, app deprecations, API sunsets) on its own schedule.
7. Match new native features against the paid app list to flag a possible retirement, and write a short adopt-or-ignore memo.
8. For a brand with a mobile app, QA the store listing, screenshots, deep links and push opt-in before each release.

## Checks
- Every automation rule tested against a real order before going live, with its actions logged.
- No API key or credential appears anywhere outside the platform's own secure settings.

## Output
An app audit report, working automation rules with an audit log, a short per-release memo, and (when relevant) an app release QA report.

## Example
"Automation rule: auto-tag COD orders over ₹5,000 as 'high-risk-review'. Tested against 20 historical orders, correctly flagged 3 known RTO cases, enabled live."
