---
name: infra-and-scripts
owner: site-specialist
version: 1
invoke_when: third-party scripts, caching/CDN setup, or headless storefront performance need diagnosis
inputs: connector: shopify admin, connector: hosting provider, results/serve.log, custom site repo when headless
outputs: script inventory, delay/removal plan, caching configuration, host brief, framework performance plan
---
# Govern scripts and tune caching, CDN and headless infrastructure

## Purpose
Find and delay or remove scripts that block rendering without breaking tracking, confirm caching is real from the headers, and apply framework-specific fixes on a headless build.

## Steps
1. Inventory every script route (theme, app embed, tag manager, hardcoded) from a real page-load trace.
2. Add defer to blocking scripts and test the exact feature each powers; delay non-critical widgets until first interaction.
3. Never change pixel loading without testing every tracked event on and off.
4. Verify caching and compression directly from response headers, never a plugin's settings page.
5. Confirm cart, checkout, account and any visitor-specific page are never cached.
6. Cache static assets long-term with versioned names, targeting an 80%+ CDN hit rate.
7. Write a host brief with real, specific questions only after front-end fixes are already measured.
8. On a headless/framework storefront: mark only the true LCP image as priority, server-render the buy box, return only needed API fields, and code-split non-critical UI.

## Checks
- Every tracking event tested on and off before a script change ships.
- No visitor-specific page ever cached, confirmed live.

## Output
A script inventory, a delay/removal plan, verified caching configuration, a host brief, and (when headless) a framework performance plan.

## Example
"Review-widget script loaded on every template; scoped to load only on PDP. Confirmed the widget still renders and pixel events still fire, on and off, before shipping."
