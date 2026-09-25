---
name: funnel-architecture
owner: site-specialist
version: 1
invoke_when: deciding which page type a campaign's traffic should land on, or how a new landing page should be built
inputs: brand brain avatar/awareness stage, ad performance (read-only), page inventory, current app list
outputs: funnel architecture diagram, page-type recommendation, builder decision memo, migration brief
---
# Traffic routing and build-method decisions

## Purpose
Decide where a click should land and how the landing page gets built, both driven by evidence (awareness stage, measured speed cost) rather than habit or the newest tool.

## Steps
1. Classify the SKU's traffic awareness stage and price point before picking a page type.
2. Send high-intent or simple-product traffic straight to the PDP; put an educating page between the ad and PDP for cold or skeptical traffic.
3. Build the advertorial only after a winning ad or written research already exists; build a dedicated campaign page for paid traffic.
4. Decide the build method (native theme Liquid, an AI page-builder app, or headless) from the page's speed budget and the team's coding skill.
5. List the JS/CSS weight each candidate builder adds, measured on the brand's own speed profile.
6. Weigh built-in features (A/B testing, analytics, personalization) against installing a separate app for each.
7. Flag when an existing heavy-builder page is a proven speed-regression cause, and write the migration brief to native code.

## Checks
- Page-type choice is backed by the SKU's real awareness-stage evidence.
- Builder weight numbers come from the brand's own speed profile, not a vendor's claim.

## Output
A funnel architecture diagram, a page-type recommendation, a builder decision memo, and (when needed) a migration brief.

## Example
"SKU is a ₹4,000 considered purchase, cold Meta traffic, no prior ad win: route through an advertorial before the PDP, not straight to product."
