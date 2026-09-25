---
name: discovery-and-personalization
owner: site-specialist
version: 1
invoke_when: making on-site search work better with the store's own real product data
inputs: connector: shopify admin | woocommerce, search app (Klevu/Searchanise-class)
outputs: search configuration spec, no-results report
---
# On-site search and discovery baseline

## Purpose
Turn on-site search into a real conversion lever instead of a plain text box, using the store's own product fields.

## Steps
1. Fill every field a filter needs (color, size, material, use-case) before turning filters on.
2. Turn on search and discovery filters wired to those real product fields.
3. Improve search with predictive text and synonym matching so a common misspelling or alternate term still finds the right product.
4. Audit search as its own funnel: track query volume, no-results rate, and treat autocomplete lag as an everyday interactivity issue, not a separate category.

## Checks
- Every filter tested live to confirm it returns matching products.
- No-results rate tracked as its own number, not folded into overall bounce.

## Output
A search configuration spec and a no-results report.

## Example
"No-results rate on 'jeans' search was 40% because product titles use 'denim'; added a synonym rule, no-results dropped to 3% within a day."
